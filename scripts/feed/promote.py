"""Stage reviewed Harness candidates for a batch PR, without editing seed data."""
from pathlib import Path
import json
import re
import shutil
from tempfile import TemporaryDirectory

import jsonschema
import yaml

from scripts.common import FIELDS, ROOT, read_yaml
from scripts.feed.review import (approved_daily_items, daily_editions_for_week, day_week,
                                 validate_daily_review, validate_weekly_picks)


def promote_candidates(root=ROOT, week=None, output_dir=None, date=None):
    root = Path(root)
    if date:
        week = day_week(date)
        review = validate_daily_review(root, date)
        accepted = approved_daily_items(root, date)
        rows = {row["id"]: row for row in review["items"]}
    else:
        validate_weekly_picks(root, week)
        accepted_by_id, rows = {}, {}
        for edition in daily_editions_for_week(root, week):
            review = validate_daily_review(root, edition["date"])
            published = {item["id"] for item in edition["items"]}
            accepted_by_id.update({item["id"]: item for item in approved_daily_items(root, edition["date"])
                                   if item["id"] in published})
            rows.update({row["id"]: row for row in review["items"]})
        accepted = list(accepted_by_id.values())
    period = date or week
    original_path = root / "data/papers.yaml"
    collection = read_yaml(original_path)
    existing_arxiv = {paper.get("arxiv") for paper in collection["papers"]}
    existing_ids = {paper["id"] for paper in collection["papers"]}
    candidates, quick = [], []
    for item in accepted:
        row = rows[item["id"]]
        if (item["llm"]["primary"] != "harness" or row["promote_to_repo"] is False
                or not item.get("arxiv_id") or item["arxiv_id"] in existing_arxiv):
            continue
        # An explicit true cannot promote a non-Harness paper into this repository.
        key = "feed-" + re.sub(r"[^a-z0-9]+", "-", item["arxiv_id"].lower()).strip("-")
        if key in existing_ids:
            raise ValueError(f"Candidate id already belongs to another record: {key}")
        candidate = {"id": key, "title": item["title"], "arxiv": item["arxiv_id"],
                     "date": item["published"][:10], "section": "candidates", "status": "candidate",
                     "needs_reading": True, "summary_zh": item["summary_zh"],
                     "evidence": {field: "unknown" for field in FIELDS}}
        if item["summary_en"]:
            candidate["summary_en"] = item["summary_en"]
            candidate["en_machine_translated"] = not isinstance(row.get("summary_override"), dict)
        code = item.get("links", {}).get("code") or next(iter(item.get("code_links", [])), None)
        if code:
            candidate["code"] = code
        candidates.append(candidate)
        quick.append({"title": item["title"], "arxiv_id": item["arxiv_id"], "evidence": item["evidence_quick"]})
        existing_ids.add(key)
        existing_arxiv.add(item["arxiv_id"])
    jsonschema.validate({**collection, "papers": collection["papers"] + candidates},
                        json.loads((root / "data/schema.json").read_text()))
    destination = Path(output_dir) if output_dir else root / "build/feed-promotions" / period
    destination.mkdir(parents=True, exist_ok=True)
    proposed = destination / "papers.yaml"
    text = original_path.read_text(encoding="utf-8")
    if candidates:
        if not collection["papers"]:
            text = re.sub(r"^papers:\s*\[\]\s*$", "papers:", text, flags=re.MULTILINE)
        text = text.rstrip() + f"\n\n# Owner-reviewed Follow RSI candidates: {period}\n" + yaml.safe_dump(
            candidates, allow_unicode=True, sort_keys=False, width=110)
    proposed.write_text(text, encoding="utf-8")
    # Validate the exact staged bytes through the catalog's full integrity checks.
    from scripts.validate import validate
    with TemporaryDirectory(prefix="follow-rsi-candidate-check-") as temporary:
        check_root = Path(temporary)
        (check_root / "data").mkdir()
        shutil.copyfile(proposed, check_root / "data/papers.yaml")
        for name in ("schema.json", "routes.yaml"):
            shutil.copyfile(root / "data" / name, check_root / "data" / name)
        validate(check_root)
    title = f"Add {len(candidates)} candidates from Follow RSI {week}" + (f" ({date})" if date else "")
    body = [f"Add {len(candidates)} owner-reviewed Harness papers from Follow RSI {period} as candidates.", "",
            "Every candidate has `needs_reading: true` and all evidence fields set to `unknown`. "
            "The following abstract-only checks are automated and unverified; they are provided for reviewer context and do not enter evidence cards.", ""]
    for item in quick:
        body += [f"### {item['title'].replace(chr(10), ' ')}", "",
                 f"https://arxiv.org/abs/{item['arxiv_id']}", ""]
        for field, value in item["evidence"].items():
            quote = value.get("quote")
            body.append(f"- {field}: {value['value']}" + (f" — {quote}" if quote else ""))
        body.append("")
    body += ["Validation: owner review gate, summary number guard, and paper collection JSON schema.", ""]
    body_path = destination / "pr-body.md"
    body_path.write_text("\n".join(body), encoding="utf-8")
    result = {"week": week, "date": date, "count": len(candidates), "title": title,
              "branch": "feed/candidates-" + period.lower(), "papers_path": str(proposed),
              "body_path": str(body_path), "candidate_ids": [paper["id"] for paper in candidates]}
    (destination / "proposal.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result
