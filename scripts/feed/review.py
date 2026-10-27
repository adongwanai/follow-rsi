"""Owner review is the publication boundary for Follow RSI.

Queue generation never accepts an item. ``move`` approves an item in a corrected
direction, and therefore requires a direction override. Picks require ``accept``.
"""
from copy import deepcopy
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re

import jsonschema
import yaml

from scripts.common import ROOT, read_yaml
from scripts.feed.guard import check_summary, enforce_evidence, unknown_evidence
from scripts.feed.storage import load_items, save_items
from scripts.feed.scope import archive_out_of_scope, load_scope, require_scope, scope_status

DECISIONS = ("pending", "accept", "reject", "move", "defer", "backlog")
OWNER_FIELDS = ("decision", "direction_override", "summary_override", "promote_to_repo", "note")
QUICK_FIELDS = ("held_out", "matched_budget", "cross_model", "code_released")
APPROVED = ("accept", "move")
REVIEW_SCHEMA = {
    "type": "object", "required": ["week", "items", "picks", "lab_updates"],
    "additionalProperties": False,
    "properties": {
        "week": {"type": "string", "pattern": r"^\d{4}-W\d{2}$"},
        "items": {"type": "array", "items": {
            "type": "object",
            "required": ["id", "title", "llm", "decision", "source_hash", "promote_to_repo"],
            "properties": {
                "id": {"type": "string", "minLength": 1},
                "arxiv_id": {"type": ["string", "null"]},
                "title": {"type": "string"}, "source_hash": {"type": "string"},
                "llm": {"type": "object"},
                "decision": {"enum": list(DECISIONS)},
                "direction_override": {"type": ["string", "object", "null"]},
                "summary_override": {"type": ["string", "object", "null"]},
                "promote_to_repo": {"enum": ["auto", True, False]},
                "summary_zh": {"type": "string"}, "summary_en": {"type": "string"},
                "note": {"type": "string"}, "evidence_quick": {
                    "type": "object", "additionalProperties": False,
                    "properties": {field: {"type": "object", "required": ["value", "quote"],
                        "additionalProperties": False, "properties": {
                            "value": {"enum": ["yes", "unknown"]},
                            "quote": {"type": ["string", "null"]}}} for field in QUICK_FIELDS}},
            },
        }},
        "picks": {"type": "array", "maxItems": 3, "items": {
            "type": "object", "required": ["arxiv_id", "why_zh", "why_en"],
            "additionalProperties": False,
            "properties": {key: {"type": "string", "minLength": 1}
                           for key in ("arxiv_id", "why_zh", "why_en")},
        }},
        "lab_updates": {"type": "array", "items": {
            "type": "object", "required": ["id", "decision"],
            "properties": {
                "id": {"type": "string"}, "decision": {"enum": ["pending", "accept", "reject"]},
                "note": {"type": "string"}, "source_hash": {"type": "string"},
            },
        }},
    },
}


def week_bounds(week):
    if not re.fullmatch(r"\d{4}-W\d{2}", week):
        raise ValueError("Week must be YYYY-WWW, for example 2026-W44")
    year, number = week.split("-W")
    start = date.fromisocalendar(int(year), int(number), 1)
    return start, start + timedelta(days=6)


def item_week(item):
    value = item.get("first_seen") or item["published"]
    current = date.fromisoformat(str(value)[:10])
    year, week, _ = current.isocalendar()
    return f"{year}-W{week:02d}"


def source_hash(item):
    # Only owner-visible content invalidates an earlier decision; counters do not.
    keys = ("id", "version", "title", "abstract", "links", "retracted", "published", "updated", "hf_daily_dates", "summary_zh",
            "summary_en", "evidence_quick", "llm", "gate", "backfill_only")
    payload = {key: item.get(key) for key in keys}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _write_yaml(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and read_yaml(path) == value:
        return  # Retain owner formatting and comments on an unchanged queue.
    path.write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")


def _review_row(item):
    return {
        "id": item["id"], "title": item["title"],
        "announced": item.get("announced") or str(item["published"])[:10],
        "window_status": None, "in_repo": bool(item.get("in_repo")),
        "gate": deepcopy(item.get("gate", {})),
        "llm_primary": (item.get("llm", {}).get("primary") or "") +
                       (" / " + item["llm"]["harness_sub"] if item.get("llm", {}).get("harness_sub") else ""),
        "decision": "defer", "arxiv_id": item.get("arxiv_id"),
        "version": item.get("version"), "source_hash": source_hash(item),
        "published": item["published"], "updated": item.get("updated", item["published"]),
        "hf_daily_dates": item.get("hf_daily_dates", []),
        "abstract": item.get("abstract", ""), "llm": deepcopy(item.get("llm", {})),
        "summary_zh": item.get("summary_zh", ""), "summary_en": item.get("summary_en", ""),
        "evidence_quick": deepcopy(item.get("evidence_quick", {})),
        "evidence_notice": "自动判断，未核实 / Automated, unverified",
        "links": deepcopy(item.get("links", {})),
        "signals": {"seed_hits": len(item.get("seed_hits", [])),
                    "author_tracked": any("author" in source for source in item.get("source_hits", [])),
                    "hf_upvotes": item.get("hf_upvotes", 0)},
        "guard_failed": bool(item.get("guard_failed")),
        "direction_override": None, "summary_override": None, "promote_to_repo": "auto", "note": "",
    }


def queue_review(root=ROOT, week=None, items=None):
    root = Path(root)
    if week is None:
        year, number, _ = datetime.now(timezone.utc).isocalendar()
        week = f"{year}-W{number:02d}"
    week_bounds(week)
    source_items = load_items(root) if items is None else items
    scope = load_scope(root)
    archive_out_of_scope(root, source_items)
    path = root / "review" / f"{week}.yaml"
    previous = read_yaml(path) if path.exists() else {"items": [], "picks": [], "lab_updates": []}
    old = {row["id"]: row for row in previous["items"]}
    labs_old = {row["id"]: row for row in previous["lab_updates"]}
    rows, excluded, labs = [], [], []
    for item in source_items:
        if item_week(item) != week or item.get("retracted"):
            continue
        if item["kind"] in ("post", "release"):
            row = {"id": item["id"], "title": item["title"], "kind": item["kind"],
                   "links": item.get("links", {}), "source_hash": source_hash(item),
                   "decision": "pending", "note": ""}
            if item["id"] in labs_old:
                prior = labs_old[item["id"]]
                row["note"] = prior.get("note", "")
                if prior.get("source_hash") == row["source_hash"]:
                    row["decision"] = prior["decision"]
            labs.append(row)
            continue
        label = item.get("llm", {}).get("label")
        if label == "exclude":
            excluded.append(_review_row(item))
            continue
        if label not in ("include", "borderline", "error"):
            continue  # Fetch-only runs have not produced a reviewable judgement.
        if label != "error" and scope_status(item.get("llm", {}), scope) == "out_of_scope":
            continue
        row = _review_row(item)
        if item["id"] in old:
            prior = old[item["id"]]
            for field in OWNER_FIELDS:
                row[field] = deepcopy(prior.get(field, row[field]))
            if prior["source_hash"] != row["source_hash"]:
                row["decision"] = "pending"
                row["review_required_reason"] = "Source or automatic content changed after the last review."
        rows.append(row)
    rows.sort(key=lambda row: (
        not (row["llm"].get("label") == "borderline" or row["guard_failed"]
             or row["llm"].get("confidence", 0) < .6 or row["llm"].get("label") == "error"),
        row["llm"].get("confidence", 0), row["id"]))
    result = {"week": week, "items": rows, "picks": previous["picks"], "lab_updates": labs}
    _write_yaml(path, result)
    _write_yaml(root / "review" / f"{week}.excluded.yaml", {"week": week, "items": excluded})
    return result


def _direction(item, row, taxonomy):
    llm = row["llm"]
    result = {"primary": llm.get("primary"), "harness_sub": llm.get("harness_sub"),
              "secondary": llm.get("secondary", [])}
    override = row.get("direction_override")
    if isinstance(override, str):
        primary, _, sub = override.partition("/")
        result.update(primary=primary, harness_sub=sub or None)
    elif isinstance(override, dict):
        if set(override) - {"primary", "harness_sub", "secondary"}:
            raise ValueError(f"{item['id']}: invalid direction override fields")
        result.update(override)
    allowed = set(taxonomy["directions"]) | set(taxonomy["cross"])
    if result["primary"] not in allowed:
        raise ValueError(f"{item['id']}: invalid primary direction {result['primary']!r}")
    if result["primary"] == "harness":
        if result["harness_sub"] not in taxonomy["directions"]["harness"]["sub"]:
            raise ValueError(f"{item['id']}: harness requires a valid harness_sub")
    else:
        result["harness_sub"] = None
    if not isinstance(result["secondary"], list) or len(result["secondary"]) > 2 or any(
        value not in allowed or value == result["primary"] for value in result["secondary"]
    ):
        raise ValueError(f"{item['id']}: invalid secondary directions")
    return result


def _summary_fields(item, row):
    if item.get("in_repo") and not row.get("summary_override"):
        return {key: item.get(key, "") for key in ("summary_zh", "summary_en")}
    result = {"summary_zh": row.get("summary_zh", ""), "summary_en": row.get("summary_en", "")}
    override = row.get("summary_override")
    if isinstance(override, str):
        result["summary_zh"], result["summary_en"] = override, ""
    elif isinstance(override, dict):
        if set(override) != {"summary_zh", "summary_en"} or not all(isinstance(v, str) for v in override.values()):
            raise ValueError(f"{item['id']}: summary_override needs summary_zh and summary_en strings")
        result.update(override)
    checked = check_summary(item["title"], item.get("abstract", ""), result["summary_zh"],
                            result["summary_en"] or None)
    if not checked["ok"]:
        raise ValueError(f"{item['id']}: summary number guard failed: {checked}")
    if result["summary_en"] and not result["summary_zh"]:
        raise ValueError(f"{item['id']}: English summary requires a Chinese source summary")
    return result


def effective_item(item, row, taxonomy):
    result = deepcopy(item)
    result["llm"] = {**row["llm"], **_direction(item, row, taxonomy)}
    result.update(_summary_fields(item, row))
    result["evidence_quick"] = (deepcopy(item["evidence_quick"]) if item.get("in_repo")
        else enforce_evidence(item.get("abstract", ""),
            {**unknown_evidence(), **row.get("evidence_quick", {})},
            code_evidence=item.get("evidence_quick", {}).get("code_released")))
    result["owner_note"] = row.get("note", "")
    return result


def validate_review(root=ROOT, week=None):
    root = Path(root)
    week_bounds(week)
    review = read_yaml(root / "review" / f"{week}.yaml")
    jsonschema.validate(review, REVIEW_SCHEMA)
    if review["week"] != week:
        raise ValueError("Review week does not match its filename")
    items = {item["id"]: item for item in load_items(root)}
    taxonomy = read_yaml(root / "feed/taxonomy.yaml")
    scope = load_scope(root)
    seen = set()
    accepted = {}
    for row in review["items"]:
        key = row["id"]
        if key in seen or key not in items:
            raise ValueError(f"Duplicate or unknown review item: {key}")
        seen.add(key)
        item = items[key]
        if row["decision"] == "pending":
            raise ValueError(f"{key}: pending review blocks publication")
        if row["source_hash"] != source_hash(item):
            raise ValueError(f"{key}: source changed; regenerate the queue and review it again")
        if row["title"] != item["title"] or row.get("arxiv_id") != item.get("arxiv_id"):
            raise ValueError(f"{key}: immutable source identity changed")
        if item.get("retracted") and row["decision"] in APPROVED:
            raise ValueError(f"{key}: retracted items cannot be published")
        if row["decision"] == "move" and not row.get("direction_override"):
            raise ValueError(f"{key}: move requires direction_override")
        if row["decision"] in APPROVED or row.get("summary_override") is not None:
            checked = effective_item(item, row, taxonomy)
            if row["decision"] in APPROVED:
                require_scope(checked, scope)
                accepted[key] = checked
    accepted_arxiv = {row.get("arxiv_id") for row in review["items"] if row["decision"] == "accept"}
    picked = [pick["arxiv_id"] for pick in review["picks"]]
    if len(set(picked)) != len(picked) or any(key not in accepted_arxiv for key in picked):
        raise ValueError("Picks must reference distinct items with decision: accept")
    for row in review["lab_updates"]:
        key = row["id"]
        if key in seen or key not in items or items[key]["kind"] not in ("post", "release"):
            raise ValueError(f"Invalid lab update: {key}")
        seen.add(key)
        if row["decision"] == "pending":
            raise ValueError(f"{key}: pending lab update blocks publication")
        if row.get("source_hash") != source_hash(items[key]):
            raise ValueError(f"{key}: lab update source changed")
        if items[key].get("retracted") and row["decision"] == "accept":
            raise ValueError(f"{key}: retracted updates cannot be published")
        if row["decision"] == "accept":
            direction = _direction(items[key], {**row, "llm": items[key].get("llm", {})}, taxonomy)
            require_scope({"id": key, "direction": direction}, scope)
    return review


def approved_items(root=ROOT, week=None):
    review = validate_review(root, week)
    items = {item["id"]: item for item in load_items(root)}
    taxonomy = read_yaml(Path(root) / "feed/taxonomy.yaml")
    return [effective_item(items[row["id"]], row, taxonomy) for row in review["items"]
            if row["decision"] in APPROVED]


def apply_review(root=ROOT, week=None, now=None):
    root = Path(root)
    review = validate_review(root, week)
    items = {item["id"]: item for item in load_items(root)}
    changed = []
    stamp = now or datetime.now(timezone.utc).isoformat()
    for row in [*review["items"], *review["lab_updates"]]:
        item = deepcopy(items[row["id"]])
        decision = {field: deepcopy(row.get(field)) for field in OWNER_FIELDS}
        decision.update(week=week, source_hash=row["source_hash"])
        previous = item.get("review", {})
        if {key: value for key, value in previous.items() if key != "reviewed_at"} == decision:
            continue
        decision["reviewed_at"] = stamp
        item["review"] = decision
        changed.append(item)
    count = save_items(root, changed)
    from scripts.feed.eval import add_owner_labels
    add_owner_labels(root, [item for item in changed if item["kind"] not in ("post", "release")])
    return count


def interactive_review(root=ROOT, week=None, input_fn=input, output_fn=print):
    root = Path(root)
    path = root / "review" / f"{week}.yaml"
    review = read_yaml(path)
    for row in [*review["items"], *review["lab_updates"]]:
        if row["decision"] not in ("pending", "defer"):
            continue
        output_fn(f"\n{row['title']}\n{row.get('summary_zh', '')}\n{row.get('links', {})}")
        while True:
            command = input_fn("[a] accept / [r] reject / [m] move direction / [s] skip: ").strip().lower()
            if command not in ("a", "r", "m", "s"):
                output_fn("Enter a, r, m, or s.")
                continue
            if command == "m" and row in review["lab_updates"]:
                output_fn("Lab updates support accept, reject, or skip.")
                continue
            break
        if command == "s":
            continue
        row["decision"] = {"a": "accept", "r": "reject", "m": "move"}[command]
        if command == "m":
            row["direction_override"] = input_fn("Direction (for example harness/improver): ").strip()
        _write_yaml(path, review)
    pending = sum(row["decision"] == "pending" for row in [*review["items"], *review["lab_updates"]])
    output_fn(f"Saved {path}. {pending} pending; run validate-review before publishing.")
    return review


DAILY_SCHEMA = {
    "type": "object", "required": ["date", "items", "lab_updates"], "additionalProperties": False,
    "properties": {
        "date": {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}$"},
        "items": deepcopy(REVIEW_SCHEMA["properties"]["items"]),
        "lab_updates": deepcopy(REVIEW_SCHEMA["properties"]["lab_updates"]),
    },
}
DAILY_SCHEMA["properties"]["lab_updates"]["items"]["properties"]["decision"]["enum"].append("defer")
PICKS_SCHEMA = {
    "type": "object", "required": ["week", "picks"], "additionalProperties": False,
    "properties": {
        "week": deepcopy(REVIEW_SCHEMA["properties"]["week"]),
        "picks": deepcopy(REVIEW_SCHEMA["properties"]["picks"]),
        "editor_note_zh": {"type": "string"}, "editor_note_en": {"type": "string"},
    },
}


def day_week(value):
    current = date.fromisoformat(value)
    if current.isoformat() != value:
        raise ValueError("Date must be YYYY-MM-DD")
    year, number, _ = current.isocalendar()
    return f"{year}-W{number:02d}"


def queue_daily_review(root=ROOT, date=None, items=None, carried_reviews=None):
    """Roll forward unresolved work, retaining edits recovered from unmerged PRs."""
    from scripts.feed.dates import daily_section
    from scripts.feed.window import daily_metadata
    root = Path(root)
    day = date or datetime.now(timezone.utc).date().isoformat()
    day_week(day)
    directory = root / "review/daily"
    previous = [read_yaml(path) for path in sorted(directory.glob("????-??-??.yaml"))
                if path.stem <= day]
    previous += list(carried_reviews or [])
    source_items = load_items(root) if items is None else items
    scope = load_scope(root)
    taxonomy = read_yaml(root / "feed/taxonomy.yaml")
    archive_out_of_scope(root, source_items)
    old = {}
    for review in sorted(previous, key=lambda value: value["date"]):
        if review["date"] <= day:
            for row in [*review["items"], *review["lab_updates"]]:
                old[row["id"]] = (review["date"], row)
    rows, excluded, labs, stale = [], [], [], []
    for item in source_items:
        if str(item.get("first_seen") or item["published"])[:10] > day:
            continue
        if item.get("retracted"):
            continue
        applied = item.get("review", {})
        prior_day = old.get(item['id'], ('', {}))[0]
        if (applied.get('kind') in ('daily', 'correction') and applied.get('date', '') <= day
                and applied.get('date', '') >= prior_day):
            # A correction supersedes the original file, including a decision to
            # defer. Replaying that file must never resurrect its old acceptance.
            old[item['id']] = (applied['date'], applied)
        timing = daily_metadata(root, item, day)
        if timing['window_status'] == 'already_published':
            continue
        if (applied.get("kind") in ("daily", "correction")
                and (applied.get("date") != day or applied.get("kind") == "correction")
                and applied.get("decision") in (*APPROVED, "reject", "backlog")
                and applied.get("source_hash") == source_hash(item)):
            continue
        lab = item["kind"] in ("post", "release")
        if lab:
            row = {"id": item["id"], "title": item["title"], "kind": item["kind"],
                   "links": item.get("links", {}), "source_hash": source_hash(item),
                   "llm": deepcopy(item.get("llm", {})), "direction_override": None,
                   "decision": "defer", "note": ""}
        else:
            label = item.get("llm", {}).get("label")
            if label == "exclude":
                excluded.append(_review_row(item))
                continue
            if label not in ("include", "borderline", "error"):
                continue
            row = _review_row(item)
        if item["id"] in old:
            prior_day, prior = old[item["id"]]
            for field in OWNER_FIELDS:
                if field in row and field in prior:
                    row[field] = deepcopy(prior[field])
            for field in ("carried_from", "review_required_reason"):
                if field in prior:
                    row[field] = prior[field]
            if prior["source_hash"] != row["source_hash"]:
                row["decision"] = "defer"
                row["review_required_reason"] = "Source or automatic content changed after the last review."
            if prior_day < day:
                row["carried_from"] = prior.get("carried_from", prior_day)
        if row.get("llm", {}).get("label") != "error":
            direction = row.get("llm", {})
            if row.get("direction_override"):
                direction = _direction(item, row, taxonomy)
            if scope_status(direction, scope) == "out_of_scope":
                continue
        row["published"] = item["published"]
        row["updated"] = item.get("updated", item["published"])
        row["hf_daily_dates"] = item.get("hf_daily_dates", [])
        row.update(timing)
        row["daily_section"] = daily_section({**item, **timing}, day)
        (stale if timing['window_status'] == 'stale' else labs if lab else rows).append(row)
    rows.sort(key=lambda row: (
        not (row["llm"].get("label") in ("borderline", "error") or row["guard_failed"]
             or row["llm"].get("confidence", 0) < .6), row["llm"].get("confidence", 0), row["id"]))
    result = {"date": day, "items": rows, "lab_updates": labs}
    _write_yaml(directory / f"{day}.yaml", result)
    _write_yaml(directory / f"{day}.excluded.yaml", {"date": day, "items": excluded})
    if stale:
        _write_yaml(root / 'review/backlog' / f'{day}.yaml', {'date': day, 'items': stale})
    return result


def validate_daily_review(root=ROOT, date=None):
    from scripts.feed.window import daily_metadata
    root = Path(root)
    day_week(date)
    review = read_yaml(root / "review/daily" / f"{date}.yaml")
    jsonschema.validate(review, DAILY_SCHEMA)
    if review["date"] != date:
        raise ValueError("Review date does not match its filename")
    sources = {item["id"]: item for item in load_items(root)}
    taxonomy = read_yaml(root / "feed/taxonomy.yaml")
    scope = load_scope(root)
    seen = set()
    for lab, rows in ((False, review["items"]), (True, review["lab_updates"])):
        for row in rows:
            key = row["id"]
            if key in seen or key not in sources:
                raise ValueError(f"Duplicate or unknown daily review item: {key}")
            seen.add(key)
            item = sources[key]
            if (item["kind"] in ("post", "release")) != lab:
                raise ValueError(f"{key}: invalid daily item kind")
            if str(item.get("first_seen") or item["published"])[:10] > date:
                raise ValueError(f"{key}: item was discovered after this review date")
            if row["decision"] == "pending":
                raise ValueError(f"{key}: pending review blocks publication; use defer to carry it forward")
            if row["source_hash"] != source_hash(item):
                raise ValueError(f"{key}: source changed; regenerate the queue and review it again")
            if row.get("title", item["title"]) != item["title"] or (not lab and row.get("arxiv_id") != item.get("arxiv_id")):
                raise ValueError(f"{key}: immutable source identity changed")
            if item.get("retracted") and row["decision"] in APPROVED:
                raise ValueError(f"{key}: retracted items cannot be published")
            if not lab:
                if row["decision"] == "move" and not row.get("direction_override"):
                    raise ValueError(f"{key}: move requires direction_override")
                if row.get("direction_override") is not None:
                    _direction(item, row, taxonomy)
                if row.get("summary_override") is not None:
                    _summary_fields(item, row)
                effective = effective_item(item, row, taxonomy) if row['decision'] in (*APPROVED, 'backlog') else None
                publishable = effective is not None and scope_status(effective['llm'], scope) == 'in_scope'
                if row['decision'] == 'accept' or row['decision'] == 'backlog' or publishable:
                    require_scope(effective, scope)
                    timing = daily_metadata(root, item, date)
                    required = 'backlog' if row['decision'] == 'backlog' else 'in_window'
                    if timing['window_status'] != required or row.get('window_status') != required:
                        raise ValueError(f"{key}: {row['decision']} requires window_status={required}; use backlog for historical papers")
                    if item.get('llm', {}).get('label') == 'exclude':
                        raise ValueError(f"{key}: excluded items cannot be accepted")
                    if item.get('gate', {}).get('verdict') != 'harness' and not row.get('direction_override'):
                        raise ValueError(f"{key}: Harness gate did not pass; an explicit direction_override is required")
                    if (effective['llm']['primary'] in ('evaluation_benchmark', 'theory_survey')
                            and item.get('gate', {}).get('harness_specific') != 'yes'
                            and not row.get('direction_override')):
                        raise ValueError(f"{key}: evaluation/theory must be Harness-specific")
            elif row.get("direction_override") is not None or row["decision"] == "accept":
                direction = _direction(item, {**row, "llm": item.get("llm", {})}, taxonomy)
                if row["decision"] == "accept":
                    require_scope({"id": key, "direction": direction}, scope)
                    if daily_metadata(root, item, date)['window_status'] != 'in_window':
                        raise ValueError(f'{key}: lab update is outside the daily window')
    return review


def approved_daily_items(root=ROOT, date=None):
    from scripts.feed.window import daily_metadata
    review = validate_daily_review(root, date)
    sources = {item["id"]: item for item in load_items(root)}
    taxonomy = read_yaml(Path(root) / "feed/taxonomy.yaml")
    scope = load_scope(root)
    result = []
    for row in review['items']:
        if row['decision'] in APPROVED:
            item = effective_item(sources[row['id']], row, taxonomy)
            item.update(daily_metadata(root, item, date))
            if item['window_status'] == 'in_window' and scope_status(item['llm'], scope) == 'in_scope':
                result.append(item)
    return result


def approved_weekly_backlog(root=ROOT, week=None):
    from scripts.feed.window import daily_metadata
    result = []
    taxonomy = read_yaml(Path(root) / 'feed/taxonomy.yaml')
    scope = load_scope(root)
    for item in load_items(root):
        review = item.get('review', {})
        if review.get('decision') != 'backlog' or review.get('week') != week:
            continue
        if review['source_hash'] != source_hash(item):
            raise ValueError(f"{item['id']}: source changed after backlog review")
        row = {**_review_row(item), **review}
        effective = effective_item(item, row, taxonomy)
        effective.update(daily_metadata(root, item, review['date']))
        if effective['window_status'] == 'backlog':
            require_scope(effective, scope)
            result.append(effective)
    return result


def apply_daily_review(root=ROOT, date=None, now=None, provenance=None):
    root = Path(root)
    review = validate_daily_review(root, date)
    sources = {item["id"]: item for item in load_items(root)}
    stamp = now or datetime.now(timezone.utc).isoformat()
    changed = []
    for row in [*review["items"], *review["lab_updates"]]:
        item = deepcopy(sources[row["id"]])
        previous = item.get("review", {})
        decision = {field: deepcopy(row.get(field)) for field in OWNER_FIELDS}
        decision.update(kind="daily", date=date, week=day_week(date), source_hash=row["source_hash"])
        if provenance is not None:
            decision.update(provenance)
        elif previous.get("date") == date and previous.get("source_hash") == row["source_hash"]:
            decision.update({key: previous[key] for key in ("github_pr", "owner_login", "merge_commit") if key in previous})
        if {key: value for key, value in previous.items() if key != "reviewed_at"} == decision:
            continue
        decision["reviewed_at"] = stamp
        item["review"] = decision
        changed.append(item)
    count = save_items(root, changed)
    from scripts.feed.eval import add_owner_labels
    add_owner_labels(root, [item for item in changed if item["kind"] not in ("post", "release")
                            and item["review"]["decision"] != "defer"])
    return count


def interactive_daily_review(root=ROOT, date=None, input_fn=input, output_fn=print):
    root = Path(root)
    day_week(date)
    path = root / "review/daily" / f"{date}.yaml"
    review = read_yaml(path)
    for row in [*review["items"], *review["lab_updates"]]:
        if row["decision"] not in ("pending", "defer"):
            continue
        output_fn(f"\n{row['title']}\n{row.get('summary_zh', '')}\n{row.get('links', {})}")
        while True:
            command = input_fn("[a] accept / [r] reject / [m] move direction / [s] defer until tomorrow: ").strip().lower()
            if command not in ("a", "r", "m", "s"):
                output_fn("Enter a, r, m, or s.")
            else:
                break
        row["decision"] = {"a": "accept", "r": "reject", "m": "move", "s": "defer"}[command]
        lab = row in review["lab_updates"]
        if command == "m" or (command == "a" and lab and not row.get("direction_override")):
            row["direction_override"] = input_fn("Direction (for example harness/improver): ").strip()
        if command == "m" and lab:
            row["decision"] = "accept"
        _write_yaml(path, review)
    output_fn(f"Saved {path}. Deferred entries return in the next daily queue.")
    return review


def daily_editions_for_week(root=ROOT, week=None):
    start, end = week_bounds(week)
    withdrawn = {item["id"] for item in load_items(root) if item.get("retracted")}
    editions = []
    scope = load_scope(root)
    for path in sorted((Path(root) / "site/daily").glob("????-??-??.json")):
        if str(start) <= path.stem <= str(end):
            edition = json.loads(path.read_text())
            if not edition.get("reviewed_only") or edition.get("demo"):
                raise ValueError("Weekly editions require daily owner-approved publications")
            for item in [*edition["items"], *edition["lab_updates"]]:
                require_scope(item, scope)
            edition["items"] = [item for item in edition["items"] if item["id"] not in withdrawn]
            edition["lab_updates"] = [item for item in edition["lab_updates"] if item["id"] not in withdrawn]
            editions.append(edition)
    return editions


def queue_weekly_picks(root=ROOT, week=None):
    root = Path(root)
    week_bounds(week)
    path = root / "review" / f"{week}.yaml"
    previous = read_yaml(path) if path.exists() else {}
    result = {"week": week, "picks": previous.get("picks", []),
              "editor_note_zh": previous.get("editor_note_zh", ""),
              "editor_note_en": previous.get("editor_note_en", "")}
    _write_yaml(path, result)
    return result


def validate_weekly_picks(root=ROOT, week=None):
    root = Path(root)
    week_bounds(week)
    review = read_yaml(root / "review" / f"{week}.yaml")
    jsonschema.validate(review, PICKS_SCHEMA)
    if review["week"] != week:
        raise ValueError("Review week does not match its filename")
    items = {item["id"]: item for edition in daily_editions_for_week(root, week) for item in edition["items"]}
    accepted = {item["arxiv_id"] for item in items.values() if item["review_decision"] == "accept"}
    picked = [pick["arxiv_id"] for pick in review["picks"]]
    if len(picked) != len(set(picked)) or any(key not in accepted for key in picked):
        raise ValueError("Picks must reference distinct daily-approved accept items published in this week")
    taxonomy = read_yaml(root / "feed/taxonomy.yaml")
    counts = {key: sum(item["direction"]["primary"] == key for item in items.values())
              for key in [*taxonomy["directions"], *taxonomy["cross"]]}
    counts["total"] = len(items)
    allowed = " ".join([str(value) for value in counts.values()] + [item["title"] + " " + item["summary_zh"] + " " + item["summary_en"] for item in items.values()])
    checked = check_summary("", allowed, review.get("editor_note_zh", ""), review.get("editor_note_en") or None)
    if not checked["ok"]:
        raise ValueError(f"Weekly editor note number guard failed: {checked}")
    if review.get("editor_note_en") and not review.get("editor_note_zh"):
        raise ValueError("English editor note requires a Chinese source note")
    return review
