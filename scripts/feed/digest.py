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
from markupsafe import Markup

from scripts.common import ROOT, read_yaml
from scripts.site_header import render_header
from scripts.feed.dates import daily_section
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
    "cross_model": ("跨模型", "Cross-model"), "code_released": ("有代码链接", "Code link"),
}
OBJECT_LABELS_EN = {"system_prompt": "System prompt", "tool_code": "Tool code or library", "skill_files": "Skill files",
                    "context_memory_policy": "Context or memory management policy", "control_flow": "Control flow",
                    "in_loop_verifier": "In-loop verifier", "improver": "The improver itself"}
DAILY_SECTIONS = {
    "hf_today": {"zh": "本期 HF 推荐", "en": "HF recommendations in this edition"},
    "other_today": {"zh": "本期其他信源", "en": "Other sources in this edition"},
    "historical": {"zh": "历史补录 / 延后审核", "en": "Historical additions / delayed review"},
}
DAILY_DATE_NOTE = {
    "zh": "只收本期时间窗内的论文。原始发表日与已核实的 HF 榜单日分别列出；历史补录进入每周精选。",
    "en": "Only papers within this edition's date window appear here. Original publication dates and verified HF list dates are shown separately; historical additions appear in weekly picks.",
}


def _daily_groups(edition, subdirections, directions):
    groups = []
    for key, names in subdirections.items():
        entries = [item for item in edition["items"] if item["direction"]["primary"] == "harness"
                   and item["direction"]["harness_sub"] == key]
        if entries:
            groups.append({"key": key, "names": names, "items": entries})
    for key, names in directions.items():
        if key != "harness":
            entries = [item for item in edition["items"] if item["direction"]["primary"] == key]
            if entries:
                groups.append({"key": key, "names": names, "items": entries})
    return groups


def _subdirections(root):
    taxonomy = read_yaml(root / "feed/taxonomy.yaml")
    sections = read_yaml(root / "data/papers.yaml")["meta"]["sections"]
    return {key: sections[key] for key in taxonomy["directions"]["harness"]["sub"]}


def _announced(item):
    return str(item.get("announced") or item["published"][:10])


def _paper_dates(item, lang):
    hf = ", ".join(item.get("hf_daily_dates", [])) or ("未核实" if lang == "zh" else "Not verified")
    published = item["published"][:10]
    parts = [f"原始发表：{published}", f"HF 推荐：{hf}"] if lang == "zh" else [
        f"Original publication: {published}", f"HF recommendations: {hf}"]
    if item.get("updated") and item["updated"] != item["published"]:
        parts.append(("版本更新：" if lang == "zh" else "Version update: ") + item["updated"][:10])
    return " · ".join(parts)


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


def _markdown(edition, lang, directions, config, subdirections=None):
    week = edition["week"]
    year, number = week.split("-W")
    title = f"Follow RSI · {year} 第 {int(number)} 周" if lang == "zh" else f"Follow RSI · {week}"
    if "date" in edition:
        title = "Follow RSI · " + edition["date"]
    retrospective = edition.get("kind") == "retrospective"
    if retrospective:
        title = edition["title_" + lang]
    card_prefix = "../.." if retrospective else ".."
    period = edition["date"] if "date" in edition else f"{edition['start']} → {edition['end']}"
    lines = [f"# {title}", "", period, "", edition["intro"][lang], ""]
    if "date" in edition and not retrospective:
        lines += [("审核日期：" if lang == "zh" else "Review date: ") + edition["date"], "", DAILY_DATE_NOTE[lang], ""]
    if retrospective:
        lines += [("第 0 期 · 历史回顾；下列论文不是当日新增。" if lang == "zh" else
                   "Edition 0 · Historical retrospective; these papers are not today's new publications."), ""]
    if edition.get("editor_note_" + lang):
        lines += ["## 编辑的话" if lang == "zh" else "## Editor's note", "", edition["editor_note_" + lang], ""]
    if edition["picks"]:
        lines += ["## 本周精选" if lang == "zh" else "## Owner's picks", ""]
        for pick in edition["picks"]:
            item = next(item for item in edition["items"] if item["arxiv_id"] == pick["arxiv_id"])
            links = " ".join(f"[{name}](<{url}>)" for name, url in item["links"].items())
            card = f" [卡片]({card_prefix}/papers/{item['repo_id']}.md)" if item.get("repo_id") else ""
            lines.append(f"- **{_md(item['title'])}** — {_md(pick['why_' + lang])} {links}{card}")
            lines.append("  " + _paper_dates(item, lang))
        lines.append("")
    picked = {pick["arxiv_id"] for pick in edition["picks"]}
    groups = _daily_groups(edition, subdirections, directions) if "date" in edition or retrospective else [
        {"names": names, "items": [item for item in edition["items"] if item["direction"]["primary"] == key and item["arxiv_id"] not in picked]}
        for key, names in directions.items()]
    if edition.get("backlog"):
        groups.append({"names": {"zh": "补录（非本周新论文）", "en": "Historical additions (not this week's new papers)"},
                       "items": edition["backlog"]})
    for group in groups:
        names, chosen = group["names"], group["items"]
        if not chosen:
            continue
        lines += [f"## {names[lang]} · {len(chosen)}", ""]
        for item in chosen:
            summary = item["summary_" + lang]
            links = " ".join(f"[{name}](<{url}>)" for name, url in item["links"].items())
            card = f" [card]({card_prefix}/papers/{item['repo_id']}.md)" if item.get("repo_id") else ""
            evidence = " · ".join("✅ " + EVIDENCE_LABELS[field][0 if lang == "zh" else 1]
                                  for field, value in item["evidence_quick"].items() if value["value"] == "yes")
            unresolved = sum(value["value"] != "yes" for value in item["evidence_quick"].values())
            if unresolved:
                evidence += (" · " if evidence else "") + (f"其余 {unresolved} 项待核" if lang == "zh" else f"{unresolved} other checks await verification")
            notice = ("人工整理，详见证据卡" if lang == "zh" else "Curated evidence; see evidence card") if item.get("in_repo") else NOTICE[lang]
            lines.append(f"- **{_md(item['short_title'])}**" + (f"：{_md(summary)}" if summary else "")
                         + f" {links}{card} — {evidence}（{notice}）")
            improved = item.get("gate", {}).get("improved_object_zh") if lang == "zh" else OBJECT_LABELS_EN.get(item.get("gate", {}).get("improved_object"))
            if improved:
                lines.append("  " + ("改了什么：" if lang == "zh" else "Modified: ") + _md(improved))
            lines.append("  " + _paper_dates(item, lang))
        lines.append("")
    if edition["lab_updates"]:
        lines += ["## 实验室与项目动态" if lang == "zh" else "## Lab & project updates", ""]
        for item in edition["lab_updates"]:
            # Releases publish the source version string and link, without generated claims.
            label = item.get("release_version") or item["title"]
            url = next(iter(item["links"].values()))
            published = item.get("published", "")[:10]
            date_label = ("来源日期：" if lang == "zh" else "Source date: ") + published if published else ""
            if item.get("updated") and item["updated"] != item.get("published"):
                date_label += (" · 版本更新：" if lang == "zh" else " · Version update: ") + item["updated"][:10]
            lines.append(f"- [{_md(label)}](<{url}>)" + (f" · {date_label}" if date_label else ""))
        lines.append("")
    if "date" not in edition and not retrospective:
        lines += ["## 近 8 周趋势" if lang == "zh" else "## Eight-week trend", "",
                  f"![Approved papers by direction](../site/weekly/{week}.trend.svg)", ""]
        metrics = edition["metrics"]
        precision = f"{metrics['precision']:.0%}" if metrics["precision"] is not None else "—"
        lines += [(f"本周找到 **{metrics['found']}** 篇 · 收录 **{metrics['accepted']}** 篇 · include 准确率 **{precision}**"
                   if lang == "zh" else f"Found **{metrics['found']}** · Accepted **{metrics['accepted']}** · Include precision **{precision}**"), ""]
    feed_prefix = "../feed" if retrospective else "../site/feed"
    lines += [f"[Atom]({feed_prefix}/atom.xml) · [JSON feed]({feed_prefix}/latest.json)"
              + (f" · [GitHub]({config['repository_url']})" if config.get("repository_url") else ""), ""]
    return "\n".join(lines)


def _public_item(item, row, week, repository):
    repo_id = next((paper["id"] for paper in repository if item.get("arxiv_id")
                    and paper.get("arxiv") == item["arxiv_id"]), None)
    return {"id": item["id"], "arxiv_id": item.get("arxiv_id"), "version": item.get("version"),
            "title": item["title"], "short_title": item["title"].split(":", 1)[0],
            "authors": item.get("authors", []), "published": item["published"],
            "updated": item.get("updated"), "hf_daily_dates": sorted(set(item.get("hf_daily_dates", []))),
            "announced": _announced(item), "announced_source": item.get("announced_source"),
            "news_date": item.get("news_date"), "window_status": item.get("window_status"),
            "in_repo": bool(repo_id or item.get("in_repo")),
            "gate": {key: value for key, value in item.get("gate", {}).items()
                     if key in ("verdict", "improved_object_zh", "improved_object", "harness_specific")},
            "direction": {key: item["llm"].get(key) for key in ("primary", "harness_sub", "secondary")},
            "summary_zh": item["summary_zh"], "summary_en": item["summary_en"],
            "evidence_quick": item["evidence_quick"],
            "evidence_notice": "Curated evidence; see evidence card" if repo_id or item.get("in_repo") else "Automated, unverified",
            "links": _links(item), "source_hits": item.get("source_hits", []),
            "hf_upvotes": item.get("hf_upvotes", 0),
            "week": week, "review_decision": row["decision"], "repo_id": repo_id}


def _write_feed(root, editions, config, retracted):
    daily = [json.loads(path.read_text()) for path in sorted((root / "site/daily").glob("????-??-??.json"))]
    recaps = _recaps(root)
    editions = [*editions, *daily, *recaps]
    if any(not edition.get("reviewed_only") or edition.get("demo") for edition in editions):
        raise ValueError("Public feeds require reviewed editions; demo artifacts cannot be published")
    scope = load_scope(root)
    for edition in editions:
        for item in [*edition["items"], *edition.get("backlog", []), *edition["lab_updates"]]:
            require_scope(item, scope)
    ordered = sorted(editions, key=lambda row: (row["week"], row.get("date", ""), row["published_at"]), reverse=True)
    cutoff = week_bounds(ordered[0]["week"])[0] - timedelta(weeks=3) if ordered else None
    last = [edition for edition in ordered if week_bounds(edition["week"])[0] >= cutoff]
    items = {item["id"]: item for edition in reversed(last) for item in [*edition["items"], *edition.get("backlog", [])]
             if item["id"] not in retracted}
    updated = max((entry.get("updated_at", entry["published_at"]) for entry in editions), default=None)
    result = {"version": 1, "reviewed_only": True, "updated_at": updated,
              "weeks": sorted({edition["week"] for edition in last}, reverse=True),
              "dates": sorted({edition["date"] for edition in last if "date" in edition}, reverse=True),
              "recaps": [{"period": edition["start"] + "--" + edition["end"], "kind": "retrospective",
                           "start": edition["start"], "end": edition["end"],
                           "title_zh": edition["title_zh"], "title_en": edition["title_en"]}
                          for edition in sorted(last, key=lambda entry: entry.get("start", ""), reverse=True)
                          if edition.get("kind") == "retrospective"],
              "items": sorted(items.values(), key=lambda item: (_announced(item), item["id"]), reverse=True)}
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
    daily_updated = max((entry.get("updated_at", entry["published_at"]) for entry in [*daily, *recaps]), default=None)
    element(feed, "updated", daily_updated or "1970-01-01T00:00:00Z")
    element(element(feed, "author"), "name", config.get("author_name") or "Follow RSI owner")
    base = (config.get("base_url") or "").rstrip("/")
    element(feed, "link", rel="self", href=(base + "/feed/atom.xml") if base else "atom.xml")
    element(feed, "link", rel="alternate", href=(base + "/daily/") if base else "../daily/")
    if config.get("repository_url"):
        element(feed, "link", rel="related", href=config["repository_url"])
    for edition in sorted([*daily, *recaps], key=lambda row: row.get("date", row.get("end")), reverse=True):
        retrospective = edition.get("kind") == "retrospective"
        period = edition["start"] + "--" + edition["end"] if retrospective else edition["date"]
        entry = element(feed, "entry")
        element(entry, "id", ("urn:follow-rsi:recap:" if retrospective else "urn:follow-rsi:daily:") + period)
        element(entry, "title", "Follow RSI · " + ("Edition 0 · " + edition["title_en"] if retrospective else period))
        element(entry, "category", term="retrospective" if retrospective else "daily")
        element(entry, "updated", edition.get("updated_at", edition["published_at"]))
        element(entry, "link", href=(base + "/" if base else "../") + ("recaps/" if retrospective else "daily/") + period + ".html")
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
    context = {"edition": edition, "editions": sorted(editions, key=lambda row: row["week"], reverse=True),
               "archive": sorted([*editions, *_recaps(root)], key=lambda row: row["end"], reverse=True),
               "directions": directions, "config": config, "evidence_labels": EVIDENCE_LABELS,
               "subdirections": _subdirections(root),
               "object_labels": OBJECT_LABELS_EN,
               "has_share_card": (root / "site/cards" / f"digest-{week}.png").exists(),
               "weekly_items": [item for item in edition["items"] if item["arxiv_id"] not in {pick["arxiv_id"] for pick in edition["picks"]}],
               "header": Markup(render_header(config, "weekly", "../")), "recaps": _recaps(root),
               "hf_discovered": sum("hf-daily" in item.get("source_hits", []) for item in edition["items"])}
    for template, output in (("weekly.html", f"{week}.html"), ("index.html", "index.html"),
                             ("digest-card.html", f"digest-{week}.card.html")):
        (root / "site/weekly" / output).write_text(env.get_template(template).render(**context), encoding="utf-8")


def _published(root, kind):
    pattern = "????-??-??.json" if kind == "daily" else "????-W??.json"
    return [json.loads(path.read_text()) for path in sorted((root / "site" / kind).glob(pattern))]


def _recaps(root):
    return [json.loads(path.read_text()) for path in sorted((root / "site/recaps").glob("????-??-??--????-??-??.json"), reverse=True)]


def _source_snapshot(root, date):
    path = root / "data/feed/state.json"
    if not path.exists():
        return {}
    sources = json.loads(path.read_text())["sources"]
    return {name: {"count": source["last_count"], "run_at": source["last_run"], "error": source.get("last_error")}
            for name, source in sources.items() if str(source.get("last_run", ""))[:10] == date}


def render_recap(root, edition):
    """Render an independently reviewed retrospective; never republish a daily date."""
    root = Path(root)
    if not edition.get("reviewed_only") or edition.get("demo"):
        raise ValueError("A public retrospective requires an independently reviewed edition")
    period = edition["start"] + "--" + edition["end"]
    edition = {**edition, "kind": "retrospective", "week": day_week(edition["end"]),
               "picks": edition.get("picks", []), "lab_updates": edition.get("lab_updates", []),
               "sources": edition.get("sources", _source_snapshot(root, edition["end"])),
               "items": sorted(({**item, "daily_section": "historical", "edition_kind": "retrospective",
                                 "recap_period": period} for item in edition["items"]),
                               key=lambda item: (_announced(item), item["id"]), reverse=True)}
    config = read_yaml(root / "site.config.yaml")
    directions = _directions(read_yaml(root / "feed/taxonomy.yaml"))
    subdirections = _subdirections(root)
    edition["counts"] = {key: sum(item["direction"]["primary"] == key for item in edition["items"])
                         for key in directions}
    directory = root / "site/recaps"
    _json(directory / (period + ".json"), edition)
    env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=select_autoescape(["html"]))
    context = {"edition": edition, "editions": sorted(_published(root, "daily"), key=lambda row: row["date"], reverse=True), "directions": directions,
               "config": config, "evidence_labels": EVIDENCE_LABELS, "object_labels": OBJECT_LABELS_EN,
               "subdirections": subdirections,
               "withdrawn_editions": load_withdrawn_editions(root),
               "daily_date_note": DAILY_DATE_NOTE, "daily_groups": _daily_groups(edition, subdirections, directions),
               "header": Markup(render_header(config, "weekly", "../")), "recaps": _recaps(root)}
    (directory / (period + ".html")).write_text(env.get_template("daily.html").render(**context), encoding="utf-8")
    for lang, suffix in (("zh", ".md"), ("en", ".en.md")):
        (directory / (period + suffix)).write_text(_markdown(edition, lang, directions, config, subdirections), encoding="utf-8")
    daily = _published(root, "daily")
    _render_day(root, None, daily, directions, config)
    _render_weekly_index(root, _published(root, "weekly"), config)
    feed = _write_feed(root, _published(root, "weekly"), config,
                       {item["id"] for item in load_items(root) if item.get("retracted")})
    return {"period": period, "accepted": len(edition["items"]), "feed_items": len(feed["items"]),
            "manifest": str(directory / (period + ".json")), "html": str(directory / (period + ".html"))}


def _render_weekly_index(root, editions, config):
    env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=select_autoescape(["html"]))
    target = root / "site/weekly/index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(env.get_template("index.html").render(
        editions=sorted(editions, key=lambda row: row["week"], reverse=True), config=config, recaps=_recaps(root),
        archive=sorted([*editions, *_recaps(root)], key=lambda row: row["end"], reverse=True),
        header=Markup(render_header(config, "weekly", "../"))), encoding="utf-8")


def _render_day(root, edition, editions, directions, config):
    env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=select_autoescape(["html"]))
    ordered = sorted(editions, key=lambda value: value["date"], reverse=True)
    subdirections = _subdirections(root)
    directory = root / "site/daily"
    directory.mkdir(parents=True, exist_ok=True)
    context = {"editions": ordered, "directions": directions, "config": config,
               "evidence_labels": EVIDENCE_LABELS, "object_labels": OBJECT_LABELS_EN,
               "subdirections": subdirections,
               "withdrawn_editions": load_withdrawn_editions(root),
               "daily_date_note": DAILY_DATE_NOTE, "header": Markup(render_header(config, "daily", "../")),
               "recaps": _recaps(root)}
    if edition:
        (root / "daily").mkdir(exist_ok=True)
        for lang, suffix in (("zh", ".md"), ("en", ".en.md")):
            (root / "daily" / (edition["date"] + suffix)).write_text(
                _markdown(edition, lang, directions, config, subdirections), encoding="utf-8")
        (directory / (edition["date"] + ".html")).write_text(
            env.get_template("daily.html").render(edition=edition, daily_groups=_daily_groups(edition, subdirections, directions), **context), encoding="utf-8")
    latest = ordered[0] if ordered else None
    (directory / "index.html").write_text(
        env.get_template("daily.html").render(edition=latest, daily_groups=_daily_groups(latest, subdirections, directions) if latest else [], **context), encoding="utf-8")
    for day, withdrawal in context["withdrawn_editions"].items():
        (directory / (day + ".html")).write_text(
            env.get_template("daily.html").render(edition=None, daily_groups=[], withdrawn_date=day,
                                                   withdrawal=withdrawal, **context), encoding="utf-8")


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
    labs.sort(key=lambda row: (sources[row["id"]]["published"], row["id"]), reverse=True)
    config = read_yaml(root / "site.config.yaml")
    directions = _directions(read_yaml(root / "feed/taxonomy.yaml"))
    ranking = read_yaml(root / "feed/sources.yaml")["ranking"]
    sub_order = list(_subdirections(root))
    accepted.sort(key=lambda item: (_announced(item), _rank(item, ranking), item["id"]), reverse=True)
    accepted.sort(key=lambda item: (sub_order.index(item["llm"]["harness_sub"]) if item["llm"]["primary"] == "harness" else len(sub_order),
                                    not item.get("in_repo", False)))
    repository = read_yaml(root / "data/papers.yaml")["papers"]
    rows = {row["id"]: row for row in review["items"]}
    public = [{**_public_item(item, rows[item["id"]], week, repository), "review_date": date, "edition_kind": "daily",
               "daily_section": daily_section(item, date)}
              for item in accepted]
    counts = {key: sum(item["llm"]["primary"] == key for item in accepted) for key in directions}
    manifest = root / "site/daily" / f"{date}.json"
    previous = json.loads(manifest.read_text()) if manifest.exists() else None
    stamp = now or (previous["published_at"] if previous else datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"))
    from scripts.feed.review import _direction
    taxonomy = read_yaml(root / "feed/taxonomy.yaml")
    lab_updates = [{"id": row["id"], "title": sources[row["id"]]["title"],
                    "kind": sources[row["id"]]["kind"], "links": _links(sources[row["id"]]),
                    "published": sources[row["id"]]["published"], "updated": sources[row["id"]].get("updated"),
                    "direction": _direction(sources[row["id"]], {**row, "llm": sources[row["id"]].get("llm", {})}, taxonomy),
                    "release_version": sources[row["id"]].get("release_version")}
                   for row in labs]
    edition = {"date": date, "week": week, "published_at": stamp, "reviewed_only": True,
               "items": public, "counts": counts, "picks": [], "lab_updates": lab_updates,
               "sources": _source_snapshot(root, date),
               "reviewers": sorted({item["review"]["owner_login"] for item in accepted if item.get("review", {}).get("owner_login")}),
               "reviewed_at": max((item["review"]["reviewed_at"] for item in accepted if item.get("review", {}).get("reviewed_at")), default=None),
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
    from scripts.feed.review import approved_weekly_backlog
    root = Path(root)
    review = validate_weekly_picks(root, week)
    daily = daily_editions_for_week(root, week)
    public = list({item["id"]: item for edition in daily for item in edition["items"]}.values())
    source_items = load_items(root)
    sources = {item["id"]: item for item in source_items}
    config = read_yaml(root / "site.config.yaml")
    directions = _directions(read_yaml(root / "feed/taxonomy.yaml"))
    ranking = read_yaml(root / "feed/sources.yaml")["ranking"]
    public.sort(key=lambda item: (_announced(item), _rank(sources[item["id"]], ranking), item["id"]), reverse=True)
    pick_order = [pick["arxiv_id"] for pick in review["picks"]]
    public.sort(key=lambda item: pick_order.index(item["arxiv_id"]) if item["arxiv_id"] in pick_order else len(pick_order))
    repository = read_yaml(root / "data/papers.yaml")["papers"]
    backlog = [{**_public_item(item, {"decision": "backlog"}, week, repository),
                "window_status": "backlog", "daily_section": "historical", "edition_kind": "weekly_backlog"}
               for item in approved_weekly_backlog(root, week)]
    backlog.sort(key=lambda item: (_announced(item), item["id"]), reverse=True)
    counts = {key: sum(item["direction"]["primary"] == key for item in public) for key in directions}
    manifest = root / "site/weekly" / f"{week}.json"
    previous = json.loads(manifest.read_text()) if manifest.exists() else None
    stamp = now or (previous["published_at"] if previous else datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"))
    start, end = week_bounds(week)
    lab_updates = list({item["id"]: item for edition in daily for item in edition["lab_updates"]}.values())
    lab_updates.sort(key=lambda item: (sources[item["id"]]["published"], item["id"]), reverse=True)
    edition = {"week": week, "start": str(start), "end": str(end), "published_at": stamp,
               "reviewed_only": True, "items": public, "backlog": backlog, "counts": counts, "picks": review["picks"],
               "editor_note_zh": review.get("editor_note_zh", ""), "editor_note_en": review.get("editor_note_en", ""),
               "lab_updates": lab_updates, "intro": _summary_intro(week, counts, directions, public, client),
               "metrics": _metrics(root, week, source_items, [sources[item["id"]] for item in public], stamp)}
    _json(manifest, edition)
    editions = _published(root, "weekly")
    _render_edition(root, edition, editions, directions, config)
    feed = _write_feed(root, editions, config, {item["id"] for item in source_items if item.get("retracted")})
    if render_card:
        render_digest_card(root, week)
        _render_edition(root, edition, editions, directions, config)
    return {"week": week, "accepted": len(public), "backlog": len(backlog), "feed_items": len(feed["items"]), "manifest": str(manifest)}


def remove_retracted(root=ROOT, render_cards=False, now=None):
    """Remove withdrawn items from daily and weekly outputs without editing reviews."""
    root = Path(root)
    source_items = load_items(root)
    sources = {item["id"]: item for item in source_items}
    withdrawn = {item["id"] for item in source_items if item.get("retracted")}
    archives = {kind: _published(root, kind) for kind in ("daily", "weekly")}
    archives["recaps"] = _recaps(root)
    if not withdrawn:
        return {"removed": 0, "weeks": [], "dates": [], "cards_removed": []}
    directions = _directions(read_yaml(root / "feed/taxonomy.yaml"))
    config = read_yaml(root / "site.config.yaml")
    stamp = now or datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    affected = {"daily": [], "weekly": [], "recaps": []}
    removed_ids, cards_removed = set(), []
    for kind, editions in archives.items():
        for edition in editions:
            removed = {item["id"] for item in [*edition["items"], *edition.get("backlog", []), *edition["lab_updates"]] if item["id"] in withdrawn}
            if not removed:
                continue
            if not edition.get("reviewed_only") or edition.get("demo"):
                raise ValueError("Retraction maintenance operates on approved published editions only")
            edition["items"] = [item for item in edition["items"] if item["id"] not in withdrawn]
            if "backlog" in edition:
                edition["backlog"] = [item for item in edition["backlog"] if item["id"] not in withdrawn]
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
            period = edition["start"] + "--" + edition["end"] if kind == "recaps" else edition.get("date", edition["week"])
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
            _render_edition(root, edition, archives["weekly"], directions, config)
    for edition in affected["recaps"]:
        render_recap(root, edition)
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
    daily = _published(root, "daily")
    daily_target = root / "site/daily/index.html"
    if not daily or not daily_target.exists():
        _render_day(root, None, daily, _directions(read_yaml(root / "feed/taxonomy.yaml")), config)
    editions = _published(root, "weekly")
    target = root / "site/weekly/index.html"
    if not editions or not target.exists():
        _render_weekly_index(root, editions, config)
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
    for relative in ("site/style.css", "site/header.css", "site/header.js", "site/weekly/weekly.css", "site/weekly/weekly.js"):
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
        elif row["window_status"] != "in_window":
            reason = "Outside the daily publication window"
        elif item.get("gate", {}).get("verdict") != "harness":
            reason = "Harness gate did not pass"
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
