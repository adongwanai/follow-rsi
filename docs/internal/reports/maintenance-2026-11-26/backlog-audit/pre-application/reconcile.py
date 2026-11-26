"""Per-stable-ID pre-application backlog reconciliation across Nov 23 baseline + Nov 26 intake."""
from pathlib import Path
from copy import deepcopy
from collections import Counter, defaultdict
from datetime import datetime, timezone
import gzip
import hashlib
import json
import shutil
import sys
import yaml

R = Path.cwd()
if str(R) not in sys.path:
    sys.path.insert(0, str(R))

from scripts.feed.review import source_hash

DAY = "2026-11-26"
OUT = R / "docs/internal/reports/maintenance-2026-11-26/backlog-audit/pre-application"
OUT.mkdir(parents=True, exist_ok=True)

OLD_LEDGER = R / "docs/internal/reports/maintenance-2026-11-23/backlog-audit/post-publication/backlog-ledger.jsonl.gz"
LATE_OVERLAY = R / "docs/internal/reports/maintenance-2026-11-23/late-issues/publication/backlog-overlay-online.json"
VER = R / "docs/internal/reports/maintenance-2026-11-23/backlog-audit/pre-application/version-review-tasks.jsonl.gz"
RAW = R / "docs/internal/reports/maintenance-2026-11-26/source-intake/all-raw-id-ledger.jsonl.gz"
CAN = R / "data/feed/items.jsonl"
BASE = R / "build/maintenance-2026-11-26/source-intake/canonical-baseline.jsonl"
BOARDS = R / "docs/internal/reports/maintenance-2026-11-26/source-intake/hf-board-reconciliation.json"
SCOPE = R / "docs/internal/reports/maintenance-2026-11-26/independent-backlog/review.json"
ADJUD = R / "docs/internal/reports/maintenance-2026-11-26/primary-review/final-adjudication.json"


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def rawbytes(p: Path) -> bytes:
    return gzip.decompress(p.read_bytes()) if p.suffix == ".gz" else p.read_bytes()


def rows(p: Path):
    return [json.loads(line) for line in rawbytes(p).splitlines() if line.strip()]


def ref(p: Path, **extra):
    return {
        "path": str(p.relative_to(R)) if p.is_relative_to(R) else str(p),
        "sha256": sha_bytes(p.read_bytes()),
        **extra,
    }


def save(name: str, obj) -> None:
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def save_lines(name: str, data):
    b = b"".join((json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8") for x in data)
    (OUT / name).write_bytes(gzip.compress(b, mtime=0))
    return {
        "path": name,
        "compressed_sha256": sha_bytes((OUT / name).read_bytes()),
        "jsonl_sha256": sha_bytes(b),
        "rows": len(data),
    }


oldrows = rows(OLD_LEDGER)
assert len(oldrows) == 9292
old = {x["id"]: x for x in oldrows}
late = json.loads(LATE_OVERLAY.read_text(encoding="utf-8"))
late_ref = ref(LATE_OVERLAY)
for lr in late["rows"]:
    ident = lr["id"]
    assert ident not in old
    old[ident] = {
        "id": ident,
        "audit_date": "2026-11-23",
        "audit_stage": "post_publication_late_issues_overlay",
        "status": lr["state"],
        "processing_bucket": "formal_scope_exclusion" if lr["decision"] == "reject" else "formal_or_catalog_record",
        "reason_zh": [lr["review"]["note"]],
        "next_actions": [lr["specific_follow_up"]],
        "version_tasks": [],
        "legacy_discovery_and_failure_refs": [],
        "legacy_discovery_member": False,
        "historical_model_error": None,
        "preserved_historical_model_error": None,
        "issue_refs": [lr["issue"]] if lr.get("issue_state") == "open" else [],
        "formal_review": lr["review"],
        "late_overlay_ref": {**late_ref, "id": ident},
    }
assert len(old) == 9295

canonical_rows = rows(CAN)
canonical = {x["id"]: x for x in canonical_rows}
assert len(canonical) == len(canonical_rows) == 2701
baseline = {x["id"]: x for x in rows(BASE)}
assert len(baseline) == 2459

rawrows = rows(RAW)
raw_by_id = defaultdict(list)
rawref = ref(RAW)
for i, x in enumerate(rawrows):
    raw_by_id[x["id"]].append((i, x))

versionrows = rows(VER)
assert len(versionrows) == 2096
old_errors = {k: x for k, x in old.items() if x.get("historical_model_error")}
assert len(old_errors) == 41

backlog_review = json.loads(SCOPE.read_text(encoding="utf-8"))
backlog_by_id = {x["id"]: x for x in backlog_review["items"]}

review_refs = {}
advice = {}
sources = []
for group in ("hf", "other"):
    f = R / f"docs/internal/reports/maintenance-2026-11-26/independent-{group}/final.json"
    payload = json.loads(f.read_text(encoding="utf-8"))
    fr = ref(f, group=group)
    sources.append(fr)
    for i, row in enumerate(payload["items"]):
        assert row["id"] not in advice, row["id"]
        advice[row["id"]] = row
        review_refs[row["id"]] = {**fr, "index": i}

adjud = json.loads(ADJUD.read_text(encoding="utf-8"))
adjud_by_id = {x["id"]: x for x in adjud["items"]}
adjud_ref = ref(ADJUD)

catalog = {p["arxiv"]: p for p in yaml.safe_load((R / "data/papers.yaml").read_text(encoding="utf-8"))["papers"] if p.get("arxiv")}
boards = json.loads(BOARDS.read_text(encoding="utf-8"))
hf_dates = defaultdict(list)
for day, b in boards["boards"].items():
    if isinstance(b, dict):
        member_ids = b.get("ids") or b.get("members") or []
    else:
        member_ids = b
    for ident in member_ids:
        hf_dates[ident].append(day)

missing_firstseen = [
    {"id": i, "before": c["first_seen"], "current": canonical.get(i, {}).get("first_seen")}
    for i, c in baseline.items()
    if canonical.get(i, {}).get("first_seen") != c["first_seen"]
]
assert not missing_firstseen, missing_firstseen

oldref = ref(OLD_LEDGER)
scope_ref = ref(SCOPE)
allids = sorted(set(old) | set(raw_by_id) | set(canonical))
result = []

for ident in allids:
    previous = old.get(ident)
    c = canonical.get(ident)
    a = advice.get(ident)
    adj = adjud_by_id.get(ident)
    br = backlog_by_id.get(ident)
    row = deepcopy(previous) if previous else {
        "id": ident,
        "reason_zh": [],
        "next_actions": [],
        "version_tasks": [],
        "legacy_discovery_and_failure_refs": [],
        "legacy_discovery_member": False,
        "historical_model_error": None,
        "preserved_historical_model_error": None,
        "issue_refs": [],
    }
    if previous:
        row["maintenance_baseline_ledger_ref"] = {**oldref, "id": ident}
    row["audit_date"] = DAY
    row["audit_stage"] = "prepublication_advice_and_current_canonical_reconciliation"
    row["prior_daily_observation"] = {
        k: deepcopy(previous.get(k))
        for k in ("status", "processing_bucket", "current_raw_refs", "current_raw_dispositions", "canonical_source_hash", "formal_review_source_hash_matches")
    } if previous else None
    row["current_raw_refs"] = [
        {**rawref, "index": i, "source_id": x["source_id"], "disposition": x["disposition"]}
        for i, x in raw_by_id.get(ident, [])
    ]
    row["current_raw_dispositions"] = sorted({x["disposition"] for _, x in raw_by_id.get(ident, [])})
    row["in_canonical"] = c is not None
    row["new_to_canonical_this_maintenance"] = ident not in baseline and c is not None
    row["new_to_full_history_ledger"] = previous is None
    row["no_new_paid_model_success_claimed"] = True
    row["live_publication_verified_by_this_audit"] = False
    row["current_hf_board_dates"] = sorted(hf_dates.get(ident, []))
    row["current_scope_advice"] = None
    row["formal_github_head_verified_by_this_audit"] = False

    if c:
        row.update(
            title=c["title"],
            first_seen=c["first_seen"],
            published_original=c.get("published"),
            version_updated=c.get("updated"),
            canonical_version=c.get("version"),
            canonical_source_hash=source_hash(c),
            canonical_hf_daily_dates=c.get("hf_daily_dates", []),
            formal_review=c.get("review"),
            catalog_entry=catalog.get(c.get("arxiv_id")),
        )
        review = c.get("review")
        row["formal_review_source_hash_matches"] = bool(review and review.get("source_hash") == source_hash(c))
        row["existing_first_seen_preserved"] = (ident not in baseline or c["first_seen"] == baseline[ident]["first_seen"])
        row["missing_canonical_hf_dates"] = sorted(set(hf_dates.get(ident, [])) - set(c.get("hf_daily_dates", [])))
        if ident in baseline:
            hashkeys = ("id", "version", "title", "abstract", "links", "retracted", "published", "updated", "summary_zh", "summary_en", "evidence_quick", "llm", "gate", "backfill_only")
            changed = [k for k in hashkeys if c.get(k) != baseline[ident].get(k)]
            row["source_fields_changed_since_intake_baseline_excluding_hf_dates"] = changed
            row["scientific_fields_identical_to_intake_baseline"] = not changed
        if not previous and not a:
            row.update(
                status="new_canonical_without_current_review_advice",
                processing_bucket="pending_evidence",
                next_actions=["Obtain item-specific source-bound scope advice before formal acceptance."],
            )
            row["reason_zh"].append(f"{ident}：来源已规范化，未匹配到本轮范围审核意见，保留待审核；不自动接受。")

    if a:
        assert adj is not None, ident
        decision = adj["decision"]
        assert decision in ("accept", "reject", "defer", "backlog"), decision
        row["current_scope_advice"] = {
            "independent_ref": review_refs[ident],
            "adjudication_ref": {**adjud_ref, "id": ident},
            "independent_decision": a["decision"],
            "adjudicated_decision": decision,
            "edition_date": adj["edition_date"],
            "reason_zh": adj["reason"],
            "direction": adj.get("direction"),
            "publication_action": adj["application"],
            "input_source_hash": a.get("input_source_hash"),
            "source_sha256": a.get("source_sha256"),
            "current_canonical_hash_at_audit": source_hash(c) if c else None,
            "formal_acceptance_or_publication_claim": False,
        }
        row["reason_zh"].append("11/26逐项三轮意见：" + adj["reason"])
        if adj["application"] == "metadata_receipt_only":
            row["status"] = "existing_source_review_reused_recommendation_dates_reconciled"
            row["processing_bucket"] = "formal_or_catalog_record"
            row["next_actions"] = ["Preserve prior scientific review and first_seen; record dated metadata receipt without duplicate publication."]
        elif decision in ("accept", "backlog"):
            row["status"] = "positive_scope_advice_pending_exact_dated_review_and_publication"
            row["processing_bucket"] = "editorial_pending"
            row["next_actions"] = ["将三轮逐项证据纳入对应刊期审核 PR，经 CI 合并与 Pages 部署后逐字节核验；未上线前不称已发布。"]
        elif decision == "reject":
            row["status"] = "scope_exclusion_advice_pending_exact_dated_review"
            row["processing_bucket"] = "reusable_scope_advice"
            row["next_actions"] = ["在真实日期审核 PR 中记录此排除及来源哈希，保留异议和后续新证据重开条件。"]
        else:
            row["status"] = "specific_evidence_gap_in_current_scope_review"
            row["processing_bucket"] = "pending_evidence"
            row["next_actions"] = [a.get("next_step_zh") or "待补外部证据后重审。"]

    if br:
        sr = br.get("source_receipt") or {}
        unchanged = sr.get("identical_body_to_nov23", sr.get("unchanged_since_nov23", True))
        row["current_legacy_issue_crosscheck"] = {
            "ref": scope_ref,
            "issue": br["issue"],
            "status": br["status"],
            "reason_zh": br["reason_zh"],
            "next_action_zh": br["next_action_zh"],
            "source_unchanged_from_nov23": unchanged,
        }
        row["reason_zh"].append("11/26独立开放Issue复核：" + br["reason_zh"])
        if br["issue"] == 160:
            row.update(
                status="published_with_specific_numeric_follow_up",
                processing_bucket="formal_or_catalog_record",
                next_actions=[br["next_action_zh"]],
            )
        else:
            row.update(
                status=br["status"],
                processing_bucket="external_blocked",
                next_actions=[br["next_action_zh"]],
            )

    if not c and not previous:
        ds = row["current_raw_dispositions"]
        source_entries = raw_by_id[ident]
        row["title"] = source_entries[0][1].get("title", ident)
        incomplete = any(x in ds for x in ("missing_publication_date", "needs_official_metadata"))
        row["processing_bucket"] = "source_date_metadata_unavailable" if incomplete else "outside_candidate_window"
        row["status"] = "raw_only_publication_date_unresolved" if incomplete else "raw_only_outside_saved_source_windows"
        row["reason_zh"] = [f"{ident}：原始响应保留，窗口处置为 {', '.join(ds)}；未规范化，不能将窗口过滤当作科学范围排除。"]
        row["next_actions"] = (
            ["从原始来源补齐发表日期或稳定身份后重查真实来源窗口。"]
            if incomplete
            else ["保留原始来源绑定；仅在符合后续真实窗口或明确历史补录任务时重开。"]
        )

    assert row.get("reason_zh"), ident
    assert row.get("status"), ident
    assert "next_actions" in row, ident
    if previous:
        assert row["version_tasks"] == previous["version_tasks"], ident
        assert row.get("historical_model_error") == previous.get("historical_model_error"), ident
        assert row.get("preserved_historical_model_error") == previous.get("preserved_historical_model_error"), ident
    result.append(row)

index = {x["id"]: x for x in result}
assert set(old) <= set(index)
assert sum(len(x["version_tasks"]) for x in result) == 2096
assert sum(bool(x.get("historical_model_error")) for x in result) == 41
assert not [x["id"] for x in result if x.get("missing_canonical_hf_dates")]
assert not [i for i in (set(canonical) - set(baseline)) if i not in advice]

ledger = save_lines("backlog-ledger.jsonl.gz", result)
shutil.copyfile(VER, OUT / "version-review-tasks.jsonl.gz")
errorrecords = [
    {
        "id": i,
        "historical_model_error": x.get("historical_model_error"),
        "preserved_historical_model_error": x.get("preserved_historical_model_error"),
        "new_paid_model_success_claimed": False,
        "prior_ledger_ref": oldref,
    }
    for i, x in old_errors.items()
]
save("historical-model-errors.json", errorrecords)

summary = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "date": DAY,
    "stage": "prepublication_advice_and_current_canonical_reconciliation",
    "universe_ids": len(result),
    "baseline_universe_ids": len(old),
    "new_to_full_history_ids": len(set(index) - set(old)),
    "canonical_ids": len(canonical),
    "baseline_canonical_ids": len(baseline),
    "new_canonical_ids": len(set(canonical) - set(baseline)),
    "new_canonical_ids_absent_from_old_full_ledger": len(set(canonical) - set(old)),
    "current_raw_occurrences": len(rawrows),
    "current_raw_unique_ids": len(raw_by_id),
    "all_id_buckets": dict(Counter(x["processing_bucket"] for x in result)),
    "canonical_buckets": dict(Counter(x["processing_bucket"] for x in result if x["in_canonical"])),
    "current_independent_advice_rows": len(advice),
    "current_adjudicated_counts": dict(Counter(x["decision"] for x in adjud["items"])),
    "new_canonical_advice_counts": dict(Counter(adjud_by_id[i]["decision"] for i in set(canonical) - set(baseline))),
    "current_advice_ref_source_counts": dict(Counter(x["group"] for x in review_refs.values())),
    "existing_first_seen_changed": missing_firstseen,
    "old_ids_missing": [],
    "old_version_task_count": len(versionrows),
    "version_tasks_preserved_exactly": True,
    "version_task_statuses": dict(Counter(x["status"] for x in versionrows)),
    "old_historical_model_errors_preserved": len(errorrecords),
    "all_ids_have_recoverable_status": True,
    "all_ids_without_reason": [],
    "missing_canonical_hf_dates": [],
    "open_issues_external_artifact_or_source_blockers": [19, 20, 23, 30, 60, 119, 128],
    "open_issues_published_numeric_followup_only": [160],
    "anchors_verified": backlog_review.get("anchor_verification", {}),
    "paid_generation_requests": 0,
    "github_writes": 0,
    "production_writes": 0,
    "all_current_publications_live_verified_by_this_audit": False,
    "formal_github_heads_verified_by_this_audit": False,
    "publication_boundary": "Independent advice and current local canonical only. Parent adds exact remote review/merge and live-publication evidence after apply; existing frozen history remains recoverable.",
    "ledger": ledger,
    "inputs": [ref(p) for p in (OLD_LEDGER, LATE_OVERLAY, VER, RAW, CAN, BASE, BOARDS, SCOPE, ADJUD)] + sources,
}
save("summary.json", summary)
save("current-scope-advice-index.json", [
    {
        "id": i,
        "ref": review_refs[i],
        "independent_decision": a["decision"],
        "adjudicated_decision": adjud_by_id[i]["decision"],
        "edition_date": adjud_by_id[i]["edition_date"],
        "reason_zh": adjud_by_id[i]["reason"],
    }
    for i, a in advice.items()
])
print(json.dumps({
    k: summary[k]
    for k in (
        "universe_ids", "canonical_ids", "new_canonical_ids",
        "current_raw_occurrences", "current_raw_unique_ids",
        "current_adjudicated_counts", "old_version_task_count",
        "old_historical_model_errors_preserved",
    )
}, ensure_ascii=False))
