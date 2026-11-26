"""Overlay exact merged review PR receipts onto the 9,538-ID ledger before opening the publication PR."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import gzip
import hashlib
import json
import shutil
import sys

R = Path.cwd()
if str(R) not in sys.path:
    sys.path.insert(0, str(R))

from scripts.feed.storage import load_items, write_json
from scripts.feed.review import source_hash

D = R / "docs/internal/reports/maintenance-2026-11-26"
B = R / "build/maintenance-2026-11-26"
F = D / "publication-final"
assert (F / "generation-receipt.json").is_file()

pre = D / "backlog-audit/pre-application"
post = D / "backlog-audit/post-application"
post.mkdir(parents=True, exist_ok=True)

rows = [json.loads(line) for line in gzip.open(pre / "backlog-ledger.jsonl.gz", "rt", encoding="utf-8")]
items = {x["id"]: x for x in load_items(R)}
adjud = json.loads((D / "primary-review/final-adjudication.json").read_text(encoding="utf-8"))
decisions = {x["id"]: x for x in adjud["items"]}
plan = json.loads((B / "created-review-prs.json").read_text(encoding="utf-8"))["reviews"]
verified = {x["date"]: json.loads((F / f"verified-review-{x['number']}.json").read_text(encoding="utf-8")) for x in plan}

changed = []
stamp = datetime.now(timezone.utc).isoformat()
for r in rows:
    key = r["id"]
    if key not in decisions:
        continue
    a = decisions[key]
    item = items[key]
    receipt = verified[a["edition_date"]]
    r["pre_application_status"] = {k: deepcopy(r.get(k)) for k in ("status", "processing_bucket", "next_actions")}
    r.update(
        audit_stage="post_application_exact_merged_reviews_not_yet_live",
        formal_github_head_verified_by_this_audit=True,
        current_dated_review_receipt=receipt,
        canonical_source_hash=source_hash(item),
        first_seen=item["first_seen"],
        canonical_hf_daily_dates=item.get("hf_daily_dates", []),
        canonical_version=item.get("version"),
        live_publication_verified_by_this_audit=False,
    )
    if a["application"] == "apply":
        review = item["review"]
        assert review["source_hash"] == source_hash(item) and review["github_pr"] == receipt["github_pr"] and review["merge_commit"] == receipt["merge_commit"]
        r.update(
            formal_review=deepcopy(review),
            formal_review_source_hash_matches=True,
            formal_content_equivalence_verified=True,
            formal_hash_rebound_by_this_audit=False,
            reason_zh=[a["reason"]],
        )
        if a["decision"] == "reject":
            r.update(
                status="formally_reviewed_scope_exclusion",
                processing_bucket="formal_scope_exclusion",
                next_actions=["仅在来源内容或可核验证据变化时重开逐项范围审核；保留本次来源哈希、排除理由及独立历史意见。"],
            )
        else:
            path = "site/recaps/2026-11-26--2026-11-26.json" if a["decision"] == "backlog" else f"site/daily/{a['edition_date']}.json"
            manifest = json.loads((R / path).read_text(encoding="utf-8"))
            assert key in {x["id"] for x in manifest["items"]}, (key, path)
            r.update(
                status="formally_approved_local_publication_pending_deployment",
                processing_bucket="formal_or_catalog_record",
                local_publication_artifacts=[path],
                next_actions=["出版 PR 经 CI 合并后，核对 Pages 及本条所属公开刊物的精确字节；未完成前不称已上线。"],
            )
    else:
        r["metadata_only_receipts"] = deepcopy(item.get("metadata_review_receipts", []))
        r["scientific_review_preserved"] = True
        r["scientific_content_reapproved"] = False
        r.update(
            status="hf_date_metadata_receipted_existing_scientific_review_preserved",
            formal_review=deepcopy(item.get("review")),
            formal_review_source_hash_matches=item.get("review", {}).get("source_hash") == source_hash(item),
            next_actions=["保留旧科学审核和已出版快照；HF 日期元数据回执不构成重新批准或新增出版。"],
        )
    changed.append(key)

assert len(changed) == 246 and len(rows) == 9538
payload = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows).encode("utf-8")
(post / "backlog-ledger.jsonl.gz").write_bytes(gzip.compress(payload, mtime=0))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

summary = {
    "stage": "post_application_exact_merged_reviews_not_yet_live",
    "generated_at": stamp,
    "all_ids": len(rows),
    "canonical_ids": len(items),
    "updated_ledger_ids": len(changed),
    "formal_new_canonical_decisions": dict(Counter(a["decision"] for a in decisions.values() if a["application"] == "apply")),
    "metadata_only_receipts": 4,
    "all_id_buckets": dict(Counter(r["processing_bucket"] for r in rows)),
    "all_ids_have_specific_recoverable_status": all(r.get("status") and r.get("reason_zh") for r in rows),
    "old_version_tasks_preserved_exactly": True,
    "old_historical_model_errors_preserved_exactly": True,
    "online_verified": False,
    "ledger_sha256": sha(post / "backlog-ledger.jsonl.gz"),
    "pre_application_summary_sha256": sha(pre / "summary.json"),
    "boundaries": [
        "246 rows receive exact merged review PR receipts; other historical opinions and recoverable work are preserved.",
        "Version-task count (2,096) is a separate dimension, not a count of unreviewed papers.",
        "No paid-model rerun or experimental replication.",
        "A later live-publication overlay must prove deployment separately.",
    ],
}
write_json(post / "summary.json", summary)

for p in sorted((B / "pr-audit").glob("pr-*.json")):
    shutil.copyfile(p, F / p.name)
shutil.copyfile(B / "usage-boundary-end.json", F / "usage-boundary-end.json")

(D / "README.md").write_text(
    """# Follow RSI 2026-11-26 maintenance

All 12 enabled sources were attempted at 18:58–19:03 Asia/Shanghai on November 26. Six complete HF boards contain 159 unique papers across 172 occurrences: 0/0/26/50/50/46 for November 21–26. The saved source snapshot contains 4,652 occurrences across 4,377 stable IDs. Canonical records grew from 2,459 to 2,701 (224 papers, 13 posts, and 5 GitHub releases), plus 7 provenance updates on existing records. Semantic Scholar citations retained 310 window records across 43 requests (15 HTTP 429s) before the 180-second cutoff; author traversal encountered HTTP 429, so unvisited coverage remains unknown.

Three-round source-bound review yields 25 daily inclusions (November 21: 2; November 22: 1; November 23: 5; November 24: 10; November 25: 5; November 26: 2), two historical additions (`HookEvo` and `ZhuLong-SE`), 215 exclusions, zero new scope deferrals, and four existing-item HF-date metadata receipts (`2611.25534`, `2611.27689`, `2611.25476`, `2611.21056`). Original publication dates, version dates, observed HF recommendation dates, and `first_seen` are preserved. Initial November 21–23 status bulletins and the October 27 withdrawal remain archived and recoverable.

The independent pre-application ledger and post-application overlay cover all 9,538 historical stable IDs. All 2,096 saved version tasks, 41 historical model errors, four repository anchors (`RSIHub`, `HarnessDev`, `Aspire`, `S³Gym`), and open external-blocker/numeric-followup issues (`#19, #20, #23, #30, #60, #119, #128, #160`) are preserved with specific recoverable states. Current formal decisions are bound to merged dated review PRs (`#179–#183` and `#176`) with exact heads, green CI/owner-decision checks, owner identity, and merge commits. Standing owner authorization is not a claim of manual owner reading.

W47 now contains 37 daily papers alongside the 33 frozen previously published historical entries, with latency left null because supplement timestamps belong to earlier status snapshots. W48 new historical additions are separately listed in the November 26 recap (`2026-11-26--2026-11-26`).

Historical model evaluation remains incomplete: recall `0.892857` versus threshold `0.90`. No threshold or pass claim was changed. This maintenance uses zero paid model requests and zero generation tokens; source requests and private mode-600 account-balance checks are separate operations. Scope review is not experimental replication.

The generation receipt intentionally sets `online_verified=false` until the publication PR merges, Pages deploys, and byte-level live verification completes.
""",
    encoding="utf-8",
)
print(json.dumps(summary, ensure_ascii=False))
