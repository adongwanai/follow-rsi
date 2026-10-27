"""Publish reviewed weekly editions, a public feed, and deterministic graphics."""
from datetime import datetime, timedelta, timezone
from html import escape
import json
from pathlib import Path
import shutil
from statistics import median
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

from jinja2 import Environment, FileSystemLoader, select_autoescape
import jsonschema

from scripts.common import ROOT, read_yaml
from scripts.feed.guard import check_intro
from scripts.feed.review import (APPROVED, approved_daily_items, daily_editions_for_week,
                                 day_week, item_week, validate_daily_review,
                                 validate_weekly_picks, week_bounds)
from scripts.feed.storage import load_items
from scripts.feed.scope import archive_counts, direction_of, in_scope, load_scope, require_scope

TEMPLATES = Path(__file__).with_name("templates")
NOTICE = {"zh": "自动判断，未核实", "en": "Automated, unverified"}
CROSS_EN = {"evaluation_benchmark": "Evaluation, benchmarks & attribution",
            "theory_survey": "Theory & surveys", "safety_governance": "Safety & governance"}
EVIDENCE_LABELS = {
    "held_out": ("留出集", "Held-out"), "matched_budget": ("同预算", "Matched budget"),
    "cross_model": ("跨模型", "Cross-model"), "code_released": ("代码", "Code"),
}


def _json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _md(value):
    for char in "\\`*_{}[]<>#|":
        value = str(value).replace(char, "\\" + char)
    return value.replace("\n", " ")


def _links(item):
    links = dict(item.get("links", {}))
    if item.get("arxiv_id"):
        links["arxiv"] = "https://arxiv.org/abs/" + item["arxiv_id"]
    if item.get("code_links") and not links.get("code"):
        links["code"] = item["code_links"][0]
    for name, url in links.items():
        if not isinstance(url, str) or urlsplit(url).scheme not in ("http", "https"):
            raise ValueError(f"{item['id']}: invalid {name} URL")
    # HF is a primary discovery surface; keep its link first when available.
    return {key: links[key] for key in ("hf", "arxiv", "code") if key in links} | {
        key: value for key, value in links.items() if key not in ("hf", "arxiv", "code")}


def _directions(taxonomy):
    return {**{key: {"zh": value["zh"], "en": value["en"]}
               for key, value in taxonomy["directions"].items()},
            **{key: {"zh": value, "en": CROSS_EN[key]} for key, value in taxonomy["cross"].items()}}


def _rank(item, ranking):
    return (len(item.get("seed_hits", [])) * ranking.get("seed_hits", 0)
            + any("author" in key for key in item.get("source_hits", [])) * ranking.get("author_tracked", 0)
            + item.get("hf_upvotes", 0) * ranking.get("hf_upvotes", 0)
            + bool(item.get("code_links") or item.get("links", {}).get("code")) * ranking.get("code_released", 0))


def _summary_intro(week, counts, directions, items, client=None):
    stats = {directions[key]["zh"]: count for key, count in counts.items() if count}
    if client is not None:
        variables = {"counts_by_direction": stats, "titles": [item["title"] for item in items]}
        feedback = None
        for attempt in range(2):
            response = client.run("digest_intro", {"id": "digest:" + week, "version": 1},
                                  variables=variables, feedback=feedback, retry_token=attempt or None)
            data = response["data"]
            result = check_intro(data["intro_zh"], data["intro_en"], stats)
            if result["ok"]:
                return {"zh": data["intro_zh"], "en": data["intro_en"], "source": "guarded-llm"}
            feedback = "以下数字不在输入统计中，或中英文数字不一致：" + json.dumps(result, ensure_ascii=False)
    # Count-only prose uses the explicit program-filled count exception.
    total = sum(counts.values())
    if not total:
        return {"zh": "本期没有通过人工审核的新论文。实验室动态仅展示 owner 勾选的条目。",
                "en": "No new papers were approved for this edition. Lab updates contain only owner-selected entries.",
                "source": "count-template"}
    zh = "、".join(f"{directions[key]['zh']} {value} 篇" for key, value in counts.items() if value)
    en = "; ".join(f"{directions[key]['en']}: {value}" for key, value in counts.items() if value)
    largest = max(counts.values())
    leaders = [key for key, value in counts.items() if value == largest]
    return {"zh": f"本期通过人工审核 {total} 篇论文：{zh}。"
                  + (f"本期论文最多的方向为 {directions[leaders[0]]['zh']}。" if len(leaders) == 1 else "多个方向的收录篇数并列最多。"),
            "en": f"This edition includes {total} owner-reviewed papers: {en}. "
                  + (f"{directions[leaders[0]]['en']} has the most papers in this edition." if len(leaders) == 1 else "Several directions share the largest count."),
            "source": "count-template"}


def _metrics(root, week, source_items, accepted, published_at):
    from scripts.feed.health import publication_times, timestamp
    path = root / "data/feed/metrics.json"
    metrics = json.loads(path.read_text()) if path.exists() else {"weeks": {}}
    found = [item for item in source_items if item_week(item) == week and item["kind"] not in ("post", "release")
             and not item.get("in_repo")]
    accepted_ids = {item["id"] for item in accepted}
    scope = load_scope(root)
    included = {item["id"] for item in source_items if item.get("llm", {}).get("label") == "include"
                and not item.get("retracted")
                and (item["id"] in accepted_ids or in_scope(direction_of(item), scope))
                and (item["id"] in accepted_ids or (item.get("review", {}).get("week") == week
                     and item["review"]["decision"] in (*APPROVED, "reject")))}
    source_yield = {}
    for item in accepted:
        sources = set(item.get("source_hits", []))
        for source in sources:
            entry = source_yield.setdefault(source, {"accepted": 0, "exclusive": 0})
            entry["accepted"] += 1
            entry["exclusive"] += len(sources) == 1
    published = publication_times(root)
    latencies = [(published[item["id"]] - timestamp(item["published"])).total_seconds() / 86400
                 for item in accepted if item["id"] in published]
    summarized = [item for item in found if item.get("llm", {}).get("label") in ("include", "borderline")]
    value = {**metrics.setdefault("weeks", {}).get(week, {}),
             "found": len(found), "accepted": len(accepted),
             "archive_by_direction": archive_counts(root, week),
             "precision": len(included & accepted_ids) / len(included) if included else None,
             "latency_days": median(latencies) if latencies else None, "source_yield": source_yield,
             "guard_fail_rate": sum(bool(item.get("initial_guard_failed")) for item in summarized) / len(summarized)
                                if summarized else None}
    metrics["weeks"][week] = value
    _json(path, metrics)
    return value


def _trend(editions, week, directions):
    start, _ = week_bounds(week)
    weeks = []
    for offset in range(7, -1, -1):
        year, number, _ = (start - timedelta(weeks=offset)).isocalendar()
        weeks.append(f"{year}-W{number:02d}")
    by_week = {entry["week"]: entry["counts"] for entry in editions}
    maximum = max([sum(by_week.get(key, {}).values()) for key in weeks] + [1])
    colors = ["#6470ff", "#3aab92", "#c882c2", "#e8a653", "#62aadd", "#dd7886", "#9b91d5", "#8fa35c", "#aba39a", "#cb936e"]
    content = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 360" role="img" aria-labelledby="title desc">',
               '<title id="title">Follow RSI: approved papers by direction over eight weeks</title>',
               '<desc id="desc">' + escape("; ".join(key + ": " + str(sum(by_week.get(key, {}).values())) for key in weeks)) + '</desc>',
               '<style>text{font-family:ui-monospace,monospace;font-size:13px;fill:#535967}@media(prefers-color-scheme:dark){text{fill:#cbd0dc}}</style>',
               '<path d="M36 245H940" stroke="#9299a8" stroke-width="1"/>']
    for index, key in enumerate(weeks):
        x, bottom = 60 + index * 112, 245
        total = 0
        for color_index, direction in enumerate(directions):
            count = by_week.get(key, {}).get(direction, 0)
            height = 200 * count / maximum
            if count:
                content.append(f'<rect x="{x}" y="{bottom-height:.1f}" width="62" height="{height:.1f}" fill="{colors[color_index]}"><title>{escape(directions[direction]["en"])}: {count}</title></rect>')
            total += count
            bottom -= height
        content.append(f'<text x="{x+31}" y="{bottom-10:.1f}" text-anchor="middle">{total}</text>')
        content.append(f'<text x="{x+31}" y="269" text-anchor="middle">{key[5:]}</text>')
    for index, (key, label) in enumerate(directions.items()):
        x, y = 36 + (index % 4) * 235, 300 + (index // 4) * 24
        content.extend([f'<rect x="{x}" y="{y-10}" width="9" height="9" fill="{colors[index]}"/>',
                        f'<text x="{x+15}" y="{y}">{escape(label["en"].split(" & ")[0])}</text>'])
    return "".join(content) + "</svg>\n"


def _markdown(edition, lang, directions, config):
    week = edition["week"]
    year, number = week.split("-W")
    title = f"Follow RSI · {year} 第 {int(number)} 周" if lang == "zh" else f"Follow RSI · {week}"
    if "date" in edition:
        title = "Follow RSI · " + edition["date"]
    period = edition["date"] if "date" in edition else f"{edition['start']} → {edition['end']}"
    lines = [f"# {title}", "", period, "", edition["intro"][lang], ""]
    if edition.get("editor_note_" + lang):
        lines += ["## 编辑的话" if lang == "zh" else "## Editor's note", "", edition["editor_note_" + lang], ""]
    if edition["picks"]:
        lines += ["## 本周精选" if lang == "zh" else "## Owner's picks", ""]
        for pick in edition["picks"]:
            item = next(item for item in edition["items"] if item["arxiv_id"] == pick["arxiv_id"])
            links = " ".join(f"[{name}](<{url}>)" for name, url in item["links"].items())
            card = f" [卡片](../papers/{item['repo_id']}.md)" if item.get("repo_id") else ""
            lines.append(f"- **{_md(item['title'])}** — {_md(pick['why_' + lang])} {links}{card}")
        lines.append("")
    for key, names in directions.items():
        chosen = [item for item in edition["items"] if item["direction"]["primary"] == key]
        if not chosen:
            continue
        lines += [f"## {names[lang]} · {len(chosen)}", ""]
        for item in chosen:
            summary = item["summary_" + lang]
            links = " ".join(f"[{name}](<{url}>)" for name, url in item["links"].items())
            card = f" [card](../papers/{item['repo_id']}.md)" if item.get("repo_id") else ""
            evidence = " · ".join(("✅ " if value["value"] == "yes" else "❔ ")
                                  + EVIDENCE_LABELS[field][0 if lang == "zh" else 1]
                                  for field, value in item["evidence_quick"].items())
            lines.append(f"- **{_md(item['short_title'])}**" + (f"：{_md(summary)}" if summary else "")
                         + f" {links}{card} — {evidence}（{NOTICE[lang]}）")
        lines.append("")
    if edition["lab_updates"]:
        lines += ["## 实验室动态" if lang == "zh" else "## Lab updates", ""]
        for item in edition["lab_updates"]:
            # Releases publish the source version string and link, without generated claims.
            label = item.get("release_version") or item["title"]
            url = next(iter(item["links"].values()))
            lines.append(f"- [{_md(label)}](<{url}>)")
        lines.append("")
    if "date" not in edition:
        lines += ["## 近 8 周趋势" if lang == "zh" else "## Eight-week trend", "",
                  f"![Approved papers by direction](../site/weekly/{week}.trend.svg)", ""]
        metrics = edition["metrics"]
        precision = f"{metrics['precision']:.0%}" if metrics["precision"] is not None else "—"
        lines += [(f"本周找到 **{metrics['found']}** 篇 · 收录 **{metrics['accepted']}** 篇 · include 准确率 **{precision}**"
                   if lang == "zh" else f"Found **{metrics['found']}** · Accepted **{metrics['accepted']}** · Include precision **{precision}**"), ""]
    lines += ["[Atom](../site/feed/atom.xml) · [JSON feed](../site/feed/latest.json)"
              + (f" · [Watch on GitHub]({config['repository_url']})" if config.get("repository_url") else " · GitHub URL pending configuration"), ""]
    return "\n".join(lines)


def _public_item(item, row, week, repository):
    repo_id = next((paper["id"] for paper in repository if item.get("arxiv_id")
                    and paper.get("arxiv") == item["arxiv_id"]), None)
    return {"id": item["id"], "arxiv_id": item.get("arxiv_id"), "version": item.get("version"),
            "title": item["title"], "short_title": item["title"].split(":", 1)[0],
            "authors": item.get("authors", []), "published": item["published"],
            "direction": {key: item["llm"].get(key) for key in ("primary", "harness_sub", "secondary")},
            "summary_zh": item["summary_zh"], "summary_en": item["summary_en"],
            "evidence_quick": item["evidence_quick"], "evidence_notice": "Automated, unverified",
            "links": _links(item), "source_hits": item.get("source_hits", []),
            "hf_upvotes": item.get("hf_upvotes", 0),
            "week": week, "review_decision": row["decision"], "repo_id": repo_id}


def _write_feed(root, editions, config, retracted):
    daily = [json.loads(path.read_text()) for path in sorted((root / "site/daily").glob("????-??-??.json"))]
    editions = [*editions, *daily]
    if any(not edition.get("reviewed_only") or edition.get("demo") for edition in editions):
        raise ValueError("Public feeds require reviewed editions; demo artifacts cannot be published")
    scope = load_scope(root)
    for edition in editions:
        for item in [*edition["items"], *edition["lab_updates"]]:
            require_scope(item, scope)
    ordered = sorted(editions, key=lambda row: (row["week"], row.get("date", ""), row["published_at"]), reverse=True)
    cutoff = week_bounds(ordered[0]["week"])[0] - timedelta(weeks=3) if ordered else None
    last = [edition for edition in ordered if week_bounds(edition["week"])[0] >= cutoff]
    items = {item["id"]: item for edition in reversed(last) for item in edition["items"] if item["id"] not in retracted}
    updated = max((entry.get("updated_at", entry["published_at"]) for entry in editions), default=None)
    result = {"version": 1, "reviewed_only": True, "updated_at": updated,
              "weeks": sorted({edition["week"] for edition in last}),
              "dates": sorted({edition["date"] for edition in last if "date" in edition}),
              "items": sorted(items.values(), key=lambda item: (item["published"], item["id"]))}
    schema_path = root / "site/feed/schema.json"
    schema_path.parent.mkdir(parents=True, exist_ok=True)
    schema_path.write_text((TEMPLATES / "feed-schema.json").read_text(), encoding="utf-8")
    jsonschema.validate(result, json.loads(schema_path.read_text()))
    _json(root / "site/feed/latest.json", result)
    namespace = "http://www.w3.org/2005/Atom"
    ET.register_namespace("", namespace)
    feed = ET.Element("{" + namespace + "}feed")
    def element(parent, tag, value=None, **attributes):
        node = ET.SubElement(parent, "{" + namespace + "}" + tag, attributes)
        node.text = value
        return node
    element(feed, "id", "urn:follow-rsi:follow-rsi")
    element(feed, "title", "Follow RSI · Five minutes a day")
    daily_updated = max((entry.get("updated_at", entry["published_at"]) for entry in daily), default=None)
    element(feed, "updated", daily_updated or "1970-01-01T00:00:00Z")
    element(element(feed, "author"), "name", config.get("author_name") or "Follow RSI owner")
    base = (config.get("base_url") or "").rstrip("/")
    element(feed, "link", rel="self", href=(base + "/feed/atom.xml") if base else "atom.xml")
    element(feed, "link", rel="alternate", href=(base + "/daily/") if base else "../daily/")
    if config.get("repository_url"):
        element(feed, "link", rel="related", href=config["repository_url"].rstrip("/") + "/pulls")
    for edition in sorted(daily, key=lambda row: row["date"]):
        period = edition["date"]
        entry = element(feed, "entry")
        element(entry, "id", "urn:follow-rsi:daily:" + period)
        element(entry, "title", "Follow RSI · " + period)
        element(entry, "updated", edition.get("updated_at", edition["published_at"]))
        element(entry, "link", href=(base + "/" if base else "../") + "daily/" + period + ".html")
        element(entry, "summary", edition["intro"]["en"])
    shutil.copyfile(TEMPLATES / "atom.xsl", root / "site/feed/atom.xsl")
    atom = b'<?xml version="1.0" encoding="utf-8"?>\n<?xml-stylesheet type="text/xsl" href="atom.xsl"?>\n'
    (root / "site/feed/atom.xml").write_bytes(atom + ET.tostring(feed, encoding="utf-8"))
    return result


def _render_edition(root, edition, editions, directions, config):
    week = edition["week"]
    (root / "digests").mkdir(exist_ok=True)
    for lang, suffix in (("zh", ".md"), ("en", ".en.md")):
        (root / "digests" / (week + suffix)).write_text(_markdown(edition, lang, directions, config), encoding="utf-8")
    (root / "site/weekly" / f"{week}.trend.svg").write_text(_trend(editions, week, directions), encoding="utf-8")
    env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=select_autoescape(["html", "xml"]))
    context = {"edition": edition, "editions": sorted(editions, key=lambda row: row["week"]),
               "directions": directions, "config": config, "evidence_labels": EVIDENCE_LABELS,
               "hf_discovered": sum("hf-daily" in item.get("source_hits", []) for item in edition["items"])}
    for template, output in (("weekly.html", f"{week}.html"), ("index.html", "index.html"),
                             ("digest-card.html", f"digest-{week}.card.html")):
        (root / "site/weekly" / output).write_text(env.get_template(template).render(**context), encoding="utf-8")


def _published(root, kind):
    pattern = "????-??-??.json" if kind == "daily" else "????-W??.json"
    return [json.loads(path.read_text()) for path in sorted((root / "site" / kind).glob(pattern))]


def _render_day(root, edition, editions, directions, config):
    env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=select_autoescape(["html"]))
    ordered = sorted(editions, key=lambda value: value["date"])
    directory = root / "site/daily"
    directory.mkdir(parents=True, exist_ok=True)
    context = {"editions": ordered, "directions": directions, "config": config,
               "evidence_labels": EVIDENCE_LABELS, "withdrawn_editions": load_withdrawn_editions(root)}
    if edition:
        (root / "daily").mkdir(exist_ok=True)
        for lang, suffix in (("zh", ".md"), ("en", ".en.md")):
            (root / "daily" / (edition["date"] + suffix)).write_text(
                _markdown(edition, lang, directions, config), encoding="utf-8")
        (directory / (edition["date"] + ".html")).write_text(
            env.get_template("daily.html").render(edition=edition, **context), encoding="utf-8")
    (directory / "index.html").write_text(
        env.get_template("daily.html").render(edition=ordered[-1] if ordered else None, **context), encoding="utf-8")


def load_withdrawn_editions(root):
    path = Path(root) / "data/feed/withdrawn-editions.json"
    return json.loads(path.read_text()) if path.exists() else {}


def require_publishable_day(root, date):
    """A withdrawn edition stays unpublished without changing its owner review."""
    withdrawn = load_withdrawn_editions(root)
    if date in withdrawn:
        raise ValueError(f"Daily edition {date} was withdrawn: {withdrawn[date]['reason']}")


def publish_day(root=ROOT, date=None, client=None, now=None):
    """Publish a reviewed daily snapshot. A day without approvals has no edition."""
    root = Path(root)
    require_publishable_day(root, date)
    review = validate_daily_review(root, date)
    accepted = approved_daily_items(root, date)
    labs = [row for row in review["lab_updates"] if row["decision"] == "accept"]
    if not accepted and not labs:
        return {"date": date, "accepted": 0, "published": False, "manifest": None}
    week = day_week(date)
    sources = {item["id"]: item for item in load_items(root)}
    labs.sort(key=lambda row: (sources[row["id"]]["published"], row["id"]))
    config = read_yaml(root / "site.config.yaml")
    directions = _directions(read_yaml(root / "feed/taxonomy.yaml"))
    ranking = read_yaml(root / "feed/sources.yaml")["ranking"]
    accepted.sort(key=lambda item: (item["published"], -_rank(item, ranking), item["id"]))
    repository = read_yaml(root / "data/papers.yaml")["papers"]
    rows = {row["id"]: row for row in review["items"]}
    public = [{**_public_item(item, rows[item["id"]], week, repository), "review_date": date}
              for item in accepted]
    counts = {key: sum(item["llm"]["primary"] == key for item in accepted) for key in directions}
    manifest = root / "site/daily" / f"{date}.json"
    previous = json.loads(manifest.read_text()) if manifest.exists() else None
    stamp = now or (previous["published_at"] if previous else datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"))
    from scripts.feed.review import _direction
    taxonomy = read_yaml(root / "feed/taxonomy.yaml")
    lab_updates = [{"id": row["id"], "title": sources[row["id"]]["title"],
                    "kind": sources[row["id"]]["kind"], "links": _links(sources[row["id"]]),
                    "direction": _direction(sources[row["id"]], {**row, "llm": sources[row["id"]].get("llm", {})}, taxonomy),
                    "release_version": sources[row["id"]].get("release_version")}
                   for row in labs]
    edition = {"date": date, "week": week, "published_at": stamp, "reviewed_only": True,
               "items": public, "counts": counts, "picks": [], "lab_updates": lab_updates,
               "intro": _summary_intro(date, counts, directions, accepted)}
    _json(manifest, edition)
    editions = _published(root, "daily")
    _render_day(root, edition, editions, directions, config)
    feed = _write_feed(root, _published(root, "weekly"), config,
                       {key for key, item in sources.items() if item.get("retracted")})
    # Weekly metrics accumulate daily approvals before the weekly selection is made.
    week_items = {item["id"]: item for day in daily_editions_for_week(root, week) for item in day["items"]}
    _metrics(root, week, list(sources.values()), [sources[key] for key in week_items], stamp)
    return {"date": date, "accepted": len(public), "published": True,
            "feed_items": len(feed["items"]), "manifest": str(manifest)}


def publish_week(root=ROOT, week=None, client=None, now=None, render_card=False):
    """Compile only published daily approvals; weekly review adds picks and notes."""
    root = Path(root)
    review = validate_weekly_picks(root, week)
    daily = daily_editions_for_week(root, week)
    public = list({item["id"]: item for edition in daily for item in edition["items"]}.values())
    source_items = load_items(root)
    sources = {item["id"]: item for item in source_items}
    config = read_yaml(root / "site.config.yaml")
    directions = _directions(read_yaml(root / "feed/taxonomy.yaml"))
    ranking = read_yaml(root / "feed/sources.yaml")["ranking"]
    public.sort(key=lambda item: (item["published"], -_rank(sources[item["id"]], ranking), item["id"]))
    counts = {key: sum(item["direction"]["primary"] == key for item in public) for key in directions}
    manifest = root / "site/weekly" / f"{week}.json"
    previous = json.loads(manifest.read_text()) if manifest.exists() else None
    stamp = now or (previous["published_at"] if previous else datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"))
    start, end = week_bounds(week)
    lab_updates = list({item["id"]: item for edition in daily for item in edition["lab_updates"]}.values())
    lab_updates.sort(key=lambda item: (sources[item["id"]]["published"], item["id"]))
    edition = {"week": week, "start": str(start), "end": str(end), "published_at": stamp,
               "reviewed_only": True, "items": public, "counts": counts, "picks": review["picks"],
               "editor_note_zh": review.get("editor_note_zh", ""), "editor_note_en": review.get("editor_note_en", ""),
               "lab_updates": lab_updates, "intro": _summary_intro(week, counts, directions, public, client),
               "metrics": _metrics(root, week, source_items, [sources[item["id"]] for item in public], stamp)}
    _json(manifest, edition)
    editions = _published(root, "weekly")
    _render_edition(root, edition, editions, directions, config)
    feed = _write_feed(root, editions, config, {item["id"] for item in source_items if item.get("retracted")})
    if render_card:
        render_digest_card(root, week)
    return {"week": week, "accepted": len(public), "feed_items": len(feed["items"]), "manifest": str(manifest)}


def remove_retracted(root=ROOT, render_cards=False, now=None):
    """Remove withdrawn items from daily and weekly outputs without editing reviews."""
    root = Path(root)
    source_items = load_items(root)
    sources = {item["id"]: item for item in source_items}
    withdrawn = {item["id"] for item in source_items if item.get("retracted")}
    archives = {kind: _published(root, kind) for kind in ("daily", "weekly")}
    if not withdrawn:
        return {"removed": 0, "weeks": [], "dates": [], "cards_removed": []}
    directions = _directions(read_yaml(root / "feed/taxonomy.yaml"))
    config = read_yaml(root / "site.config.yaml")
    stamp = now or datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    affected = {"daily": [], "weekly": []}
    removed_ids, cards_removed = set(), []
    for kind, editions in archives.items():
        for edition in editions:
            removed = {item["id"] for item in [*edition["items"], *edition["lab_updates"]] if item["id"] in withdrawn}
            if not removed:
                continue
            if not edition.get("reviewed_only") or edition.get("demo"):
                raise ValueError("Retraction maintenance operates on approved published editions only")
            edition["items"] = [item for item in edition["items"] if item["id"] not in withdrawn]
            edition["lab_updates"] = [item for item in edition["lab_updates"] if item["id"] not in withdrawn]
            remaining = {item["arxiv_id"] for item in edition["items"]}
            edition["picks"] = [pick for pick in edition["picks"] if pick["arxiv_id"] in remaining]
            edition["counts"] = {key: sum(item["direction"]["primary"] == key for item in edition["items"]) for key in directions}
            edition["intro"] = _summary_intro(edition.get("date", edition["week"]), edition["counts"], directions, edition["items"])
            if kind == "weekly":
                edition["metrics"] = _metrics(root, edition["week"], source_items,
                                               [sources[item["id"]] for item in edition["items"]], stamp)
            edition["withdrawn_ids"] = sorted(set(edition.get("withdrawn_ids", [])) | removed)
            edition["updated_at"] = stamp
            period = edition.get("date", edition["week"])
            _json(root / "site" / kind / (period + ".json"), edition)
            affected[kind].append(edition)
            removed_ids.update(removed)
            if kind == "weekly":
                png = root / "site/cards" / ("digest-" + edition["week"] + ".png")
                if png.exists():
                    png.unlink()
                    cards_removed.append(str(png))
    for edition in affected["daily"]:
        _render_day(root, edition, archives["daily"], directions, config)
    for edition in affected["weekly"]:
        _render_edition(root, edition, archives["weekly"], directions, config)
        if render_cards:
            render_digest_card(root, edition["week"])
    if removed_ids:
        for edition in archives["weekly"]:
            (root / "site/weekly" / (edition["week"] + ".trend.svg")).write_text(
                _trend(archives["weekly"], edition["week"], directions), encoding="utf-8")
        _write_feed(root, archives["weekly"], config, withdrawn)
    return {"removed": len(removed_ids), "weeks": [entry["week"] for entry in affected["weekly"]],
            "dates": [entry["date"] for entry in affected["daily"]], "cards_removed": cards_removed}


def render_digest_card(root=ROOT, week=None):
    """The same optional local Playwright screenshot step as paper cards."""
    from playwright.sync_api import sync_playwright
    root = Path(root)
    source = root / "site/weekly" / f"digest-{week}.card.html"
    output = root / "site/cards" / f"digest-{week}.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        page.route("**/*", lambda route: route.continue_() if route.request.url.startswith("file:") else route.abort())
        page.goto(source.resolve().as_uri())
        page.evaluate("document.fonts.ready")
        card = page.locator("#card")
        if not card.evaluate("el => el.scrollHeight <= el.clientHeight && el.scrollWidth <= el.clientWidth"):
            raise ValueError("Weekly card overflow; shorten owner pick titles in the source display layout")
        card.screenshot(path=str(output), animations="disabled")
        browser.close()
    return output


def initialize_public(root=ROOT):
    """Render empty archives honestly without replacing an existing public feed."""
    root = Path(root)
    config = read_yaml(root / "site.config.yaml")
    env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=select_autoescape(["html"]))
    daily = _published(root, "daily")
    daily_target = root / "site/daily/index.html"
    if not daily or not daily_target.exists():
        _render_day(root, None, daily, _directions(read_yaml(root / "feed/taxonomy.yaml")), config)
    editions = _published(root, "weekly")
    target = root / "site/weekly/index.html"
    if not editions or not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(env.get_template("index.html").render(
            editions=sorted(editions, key=lambda row: row["week"]), config=config), encoding="utf-8")
    public = root / "site/feed/latest.json"
    if public.exists():
        current = json.loads(public.read_text())
        if current["weeks"] or current["items"]:
            return
    _write_feed(root, editions, config, {item["id"] for item in load_items(root) if item.get("retracted")})


def publish_demo(root=ROOT, week=None, output_dir=None, render_card=True):
    """Build an explicitly auto-accepted demo entirely inside ignored build/.

    Demo JSON deliberately does not conform to the approved public feed schema.
    It cannot be mistaken for a reviewed feed or deployed by the regular publisher.
    """
    import yaml
    from scripts.feed.review import effective_item, queue_daily_review, queue_weekly_picks
    root = Path(root).resolve()
    week_bounds(week)
    destination = Path(output_dir).resolve() if output_dir else root / "build/demo" / week
    if not destination.is_relative_to(root / "build"):
        raise ValueError("Demo output must stay inside the repository's ignored build/ directory")
    for relative in ("data/papers.yaml", "site.config.yaml", "data/schema.json", "data/routes.yaml",
                     "feed/taxonomy.yaml", "feed/sources.yaml"):
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / relative, target)
    for relative in ("site/style.css", "site/weekly/weekly.css", "site/weekly/weekly.js"):
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    # Demo reruns start from an exact copy of source records, never previous demo decisions.
    (destination / "data/feed").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(root / "data/feed/items.jsonl", destination / "data/feed/items.jsonl")
    for kind in ("daily", "weekly"):
        for path in (destination / "site" / kind).glob("*.json"):
            path.unlink()
    items = {item["id"]: item for item in load_items(destination)}
    included = [item for item in items.values() if item_week(item) == week]
    demo_date = max((str(item.get("first_seen") or item["published"])[:10] for item in included),
                    default=str(week_bounds(week)[1]))
    old_review = destination / "review/daily" / f"{demo_date}.yaml"
    if old_review.exists():
        old_review.unlink()
    review = queue_daily_review(destination, demo_date, items=included)
    taxonomy = read_yaml(destination / "feed/taxonomy.yaml")
    omitted = []
    for row in review["items"]:
        item = items[row["id"]]
        row["decision"] = "reject"
        reason = None
        if row["llm"].get("label") not in ("include", "borderline") or item.get("guard_failed"):
            reason = "LLM error or failed number guard"
        else:
            try:
                effective_item(item, row, taxonomy)
            except ValueError as error:
                reason = str(error)
        if reason:
            omitted.append({"id": row["id"], "reason": reason})
        else:
            row["decision"] = "accept"
    for row in review["lab_updates"]:
        row["decision"] = "reject"
    old_review.write_text(yaml.safe_dump(review, allow_unicode=True, sort_keys=False), encoding="utf-8")
    publish_day(destination, demo_date)
    queue_weekly_picks(destination, week)
    report = publish_week(destination, week)
    warning = "演示用，自动通过 / DEMO — automatically accepted, not published"
    def demo_wording(text):
        for original, replacement in (("owner-reviewed", "demo auto-accepted"),
                                      ("Owner-approved", "Demo auto-accepted"),
                                      ("owner review", "demo processing"),
                                      ("通过人工审核", "演示自动通过"), ("人工收录", "演示收录")):
            text = text.replace(original, replacement)
        return text
    public_json = destination / "site/feed/latest.json"
    for path in [public_json, *(destination / "site/weekly").glob("????-W??.json"),
                 *(destination / "site/daily").glob("????-??-??.json")]:
        data = json.loads(path.read_text())
        data.update(demo=True, reviewed_only=False, notice=warning)
        for item in data["items"]:
            item["review_decision"] = "demo_autoaccept"
        if "intro" in data:
            data["intro"] = {key: demo_wording(value) for key, value in data["intro"].items()}
        _json(path, data)
    for path in [*(destination / "site/weekly").glob("*.html"), *(destination / "site/daily").glob("*.html")]:
        content = path.read_text().replace("<title>", "<title>DEMO · ")
        if path.name.endswith(".card.html"):
            content = content.replace("FOLLOW RSI / WEEKLY LEDGER", "DEMO / 自动通过 · 未经 OWNER 审核")
            content = content.replace("篇论文通过人工审核", "篇仅演示自动通过")
        else:
            content = content.replace("<body>", '<body><aside style="padding:16px;background:#f5cf6d;color:#161616;font-weight:bold;text-align:center">' + warning + "</aside>")
        path.write_text(demo_wording(content.replace("OWNER REVIEWED", "DEMO AUTO-ACCEPTED")), encoding="utf-8")
    for path in [*(destination / "digests").glob("*.md"), *(destination / "daily").glob("*.md")]:
        path.write_text("> " + warning + "\n\n" + demo_wording(path.read_text()), encoding="utf-8")
    atom = destination / "site/feed/atom.xml"
    atom.write_text(demo_wording(atom.read_text().replace("<title>", "<title>DEMO · ")), encoding="utf-8")
    report.update(demo=True, notice=warning, output_dir=str(destination), omitted=omitted)
    _json(destination / "demo-report.json", report)
    if render_card:
        render_digest_card(destination, week)
    return report
