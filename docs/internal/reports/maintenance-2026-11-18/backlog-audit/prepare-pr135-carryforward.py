"""Preserve per-item PR135 recovery work; no canonical or GitHub writes."""
from collections import Counter
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
DOC = ROOT / 'docs/internal/reports/maintenance-2026-11-18/backlog-audit'
RAW = ROOT / 'data/feed/raw/maintenance-2026-11-18/backlog-audit'
inventory_path = RAW / 'pr135-historical-inventory-v1.jsonl.gz'
output_path = RAW / 'pr135-carryforward-v1.jsonl.gz'
summary_path = DOC / 'pr135-carryforward-v1.json'
assert not output_path.exists() and not summary_path.exists()
inputs = {}


def read(path):
    data = path.read_bytes()
    inputs[str(path.relative_to(ROOT))] = hashlib.sha256(data).hexdigest()
    return gzip.decompress(data) if path.suffix == '.gz' else data


def ref(path, **extra):
    name = str(path.relative_to(ROOT))
    return {'path': name, 'sha256': inputs[name], **extra}


def unique(values):
    return list(dict.fromkeys(value for value in values if isinstance(value, str) and value.strip()))


inventory = [json.loads(line) for line in read(inventory_path).splitlines()]
reports = {}
for filename, field in [
    ('maintenance-2026-10-30/independent/source-reviews.jsonl', None),
    ('maintenance-2026-10-30/independent/adjudications.jsonl', None),
    ('maintenance-2026-10-30/primary/labs-scope-review.json', 'reviews'),
    ('maintenance-2026-10-31/primary/review-reconciled.json', 'items'),
    ('maintenance-2026-11-02/reconciliation.json', 'records'),
]:
    path = ROOT / 'docs/internal/reports' / filename
    data = read(path)
    rows = [json.loads(line) for line in data.splitlines()] if field is None else json.loads(data)[field]
    reports[filename] = {row['id']: (ref(path, index=index, collection=field), row) for index, row in enumerate(rows)}
four_path = DOC / 'four-issue-evidence-v1.json'
four = {r['id']: r for r in json.loads(read(four_path))['items']}
blockers_path = DOC / 'source-blocker-assessments-v1.json'
blockers = {r['id']: r for r in json.loads(read(blockers_path))['items']}
rows = []
for index, frozen in enumerate(inventory):
    ident = frozen['id']
    prior = frozen['prior_ledger_row']
    current = frozen['canonical_snapshot']
    receipt = frozen['owner_scope_receipt_ref']
    owner = receipt['receipt'] if receipt else {}
    historical = (prior.get('historical_status') or {}).get('old_pipeline_record') or {}
    corrections = frozen['post_approval_correction_ref']
    reasons = list(prior.get('reason_zh') or [])
    reasons += [owner.get('reason_zh'), historical.get('reason_zh')]
    evidence = []
    limitations = []
    for report in reports.values():
        if ident not in report:
            continue
        location, record = report[ident]
        payload = record.get('data') or record
        reasons += [payload.get('reason_zh'), payload.get('rationale_zh')]
        limitations += [payload.get('limitations_zh'), payload.get('necessary_followup_zh'), payload.get('boundary_note_zh')]
        evidence.append({'reference': location, 'saved_review_record': record, 'new_whole_paper_review_claimed': False})
    if corrections:
        reasons.append(corrections['correction']['reason_zh'])
    catalog = prior.get('catalog_entry')
    if catalog:
        reasons.append(f"已在目录登记为 {catalog['id']}，section={catalog['section']}，scope={catalog['scope']}；目录存在不等于日报已出版。")
    reasons = unique(reasons)
    assert reasons, ident
    scope = frozen['scope_recommendation']
    summary_present = {lang: bool(str(current.get('summary_' + lang) or '').strip()) for lang in ['zh', 'en']}
    levels = unique([op.get('review_level') for op in prior.get('source_opinions', [])])
    old_rounds = historical.get('historical_rounds_matching_input') or []
    owner_hash_matches = bool(receipt and receipt['exact_hash_matches_current'])
    next_actions = []
    missing = []
    if ident in four:
        status = 'specific_harness_evidence_gap_retained'
        missing = [four[ident]['reason_zh']]
        next_actions = ['obtain_the_specific_version_admission_and_later_consumption_evidence']
        evidence.append({'reference': ref(four_path, id=ident), 'saved_review_record': four[ident]})
    elif ident in blockers:
        status = 'external_source_blocker_retained'
        missing = [blockers[ident]['reason_zh']]
        next_actions = blockers[ident]['required_actions']
        evidence.append({'reference': ref(blockers_path, id=ident), 'saved_review_record': blockers[ident]})
    elif corrections and corrections['correction']['effective_decision'] == 'defer':
        status = 'post_approval_counterevidence_retained'
        missing = [corrections['correction']['reason_zh']]
        next_actions = ['resolve_cross_task_inheritance_evidence_before_inclusion']
    elif scope is None or prior['status'] == 'existing_catalog_record_no_new_publication_claim':
        status = 'existing_catalog_entry_retained'
        next_actions = ['retain_existing_catalog_identity_and_reading_route', 'evaluate_a_new_edition_only_with_its_own_date_and_source_receipt']
    elif scope == 'include':
        status = 'reusable_inclusion_scope_editorial_preparation'
        missing = ['missing_summary_' + lang for lang, present in summary_present.items() if not present]
        missing += ['current_dated_formal_review_and_publication_receipt', 'summary_numbers_and_quoted_evidence_final_check']
        next_actions = ['reuse_the_saved_scope_opinion_and_counterevidence', 'finish_the_named_editorial_checks', 'apply_a_real_dated_review_before_publication']
    elif scope == 'exclude':
        status = 'reusable_exclusion_scope_dated_disposition_pending'
        missing = ['current_dated_formal_disposition']
        next_actions = ['use_saved_scope_and_independent_review_evidence_to_resolve_reject_where_complete']
        if old_rounds != [1, 2, 3] and not any('three_round' in level for level in levels):
            missing.append('verify_independent_round_coverage_before_new_formal_disposition')
    elif scope == 'no_harness_support':
        status = 'bounded_source_screen_not_fulltext_exclusion'
        missing = ['scope_evidence_is_limited_to_the_recorded_review_level', 'verify_independent_round_coverage_if_formally_disposed']
        next_actions = ['retain_exact_abstract_or_body_reading_limit', 'resolve_the_specific_object_feedback_and_retention_question_if_more_source_is_available']
    else:
        status = 'specific_scope_boundary_retained'
        missing = unique([owner.get('pending_evidence_zh'), *[op.get('pending_evidence') for op in prior.get('source_opinions', [])], *limitations])
        if not missing:
            missing = reasons
        next_actions = ['resolve_the_preserved_item_specific_counterevidence', 'obtain_independent_scope_resolution_before_inclusion']
    if receipt and not owner_hash_matches:
        missing.append('old_owner_receipt_hash_differs_from_current_source_do_not_rebind_silently')
        next_actions.insert(0, 'verify_recorded_source_delta_and_current_content_binding')
    numbers = {19: 'arxiv:2610.39884', 20: 'arxiv:2610.39714', 30: 'arxiv:2610.36013'}
    issue_refs = [{'number': 60, 'url': 'https://github.com/adongwanai/follow-rsi/issues/60', 'role': 'existing_umbrella_for_remaining_evidence'}]
    issue_refs += [{'number': number, 'url': f'https://github.com/adongwanai/follow-rsi/issues/{number}', 'role': 'specific_harness_evidence_gap'} for number, aid in numbers.items() if ident == aid]
    rows.append({'id': ident, 'title': frozen['title'], 'status': status, 'scope_recommendation': scope,
                 'reason_zh': reasons, 'pending_evidence_or_editorial_checks': unique(missing), 'next_actions': unique(next_actions),
                 'canonical_source_hash_at_archive': frozen['canonical_source_hash'], 'archive_reference': ref(inventory_path, index=index),
                 'original_queue_reference': frozen['original_queue'], 'prior_ledger_reference': frozen['prior_ledger_ref'],
                 'owner_scope_receipt': receipt, 'owner_receipt_hash_recomputed_matches': owner_hash_matches,
                 'post_approval_correction': corrections, 'historical_rounds_reported': old_rounds,
                 'reading_levels_reported': levels, 'saved_review_evidence': evidence, 'summary_present': summary_present,
                 'catalog_entry': catalog, 'issue_refs': issue_refs,
                 'source_hash_is_not_model_excerpt_hash': True, 'source_bodies_refetched_by_this_record': False,
                 'reused_review_is_not_new_whole_paper_or_numeric_replication': True,
                 'new_formal_decision_written': False, 'new_publication_claimed': False})

assert len(rows) == 121
assert all(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest for path, digest in inputs.items())
output_path.write_bytes(gzip.compress(''.join(json.dumps(row, sort_keys=True, ensure_ascii=False) + '\n' for row in rows).encode(), mtime=0))
summary = {'date': '2026-11-18', 'created_at': datetime.now(timezone.utc).isoformat(), 'records': len(rows),
           'counts': dict(Counter(row['status'] for row in rows)), 'inputs': inputs,
           'output': {'path': str(output_path.relative_to(ROOT)), 'sha256': hashlib.sha256(output_path.read_bytes()).hexdigest()},
           'independent_actionable_disposition_directory': 'docs/internal/reports/maintenance-2026-11-18/historical-disposition',
           'all_ids_have_specific_reasons_and_recovery_actions': all(row['reason_zh'] and row['next_actions'] for row in rows),
           'old_queue_removal_does_not_remove_recovery_tasks': True,
           'new_paid_requests': 0, 'new_scientific_review_claimed': False, 'canonical_writes': 0, 'github_writes': 0}
summary_path.write_text(json.dumps(summary, sort_keys=True, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(summary, ensure_ascii=False, indent=2))
