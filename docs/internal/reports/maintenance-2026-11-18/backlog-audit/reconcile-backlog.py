"""One-time Nov 18 per-ID audit. Re-run with a new --stage after apply; no production writes."""
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from scripts.feed.review import source_hash

REPORT = ROOT / 'docs/internal/reports/maintenance-2026-11-18/backlog-audit'
RAW = ROOT / 'data/feed/raw/maintenance-2026-11-18/backlog-audit'
OLD = ROOT / 'data/feed/raw/maintenance-2026-11-15/publication-final/backlog-audit/post-review'
RECOVERY = ROOT / 'data/feed/raw/maintenance-2026-11-15/publication-final/version-source-recovery'
parser = argparse.ArgumentParser()
parser.add_argument('--stage', required=True)
parser.add_argument('--canonical', default='data/feed/items.jsonl')
parser.add_argument('--adjudication', default='docs/internal/reports/maintenance-2026-11-18/primary-review/final-adjudication.json')
args = parser.parse_args()
assert re.fullmatch(r'[a-z0-9-]+', args.stage)
OUT = RAW / args.stage
DOC = REPORT / args.stage
assert not OUT.exists() and not DOC.exists(), 'Each stage is immutable; use a new stage name.'
OUT.mkdir()
DOC.mkdir()
inputs = {}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def relative(path):
    return str(path.relative_to(ROOT))


def read(path):
    path = ROOT / path if not Path(path).is_absolute() else Path(path)
    data = path.read_bytes()
    inputs[relative(path)] = {'sha256': sha(data), 'bytes': len(data)}
    return gzip.decompress(data) if path.suffix == '.gz' else data


def load(path):
    return json.loads(read(path))


def lines(path):
    return [json.loads(line) for line in read(path).splitlines() if line]


def reference(path, index=None):
    key = relative(path) if isinstance(path, Path) else path
    result = {'path': key, 'sha256': inputs[key]['sha256']}
    if index is not None:
        result['index'] = index
    return result


def jsonout(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + '\n')


def jlout(name, rows):
    data = ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows).encode()
    (OUT / name).write_bytes(gzip.compress(data, mtime=0))


def textnorm(value):
    return re.sub(r'\s+', ' ', str(value or '')).strip()


def content_key(row):
    fields = {key: textnorm(row.get(key)) for key in ['version', 'title', 'abstract', 'updated']}
    return row['id'] + ':' + sha(json.dumps(fields, sort_keys=True, ensure_ascii=False).encode())


canonical_path = ROOT / args.canonical
read(Path(__file__))
canonical = {r['id']: r for r in lines(canonical_path)}
baseline_path = ROOT / 'build/maintenance-2026-11-18/source-intake/canonical-baseline.jsonl'
baseline = {r['id']: r for r in lines(baseline_path)}
old_path = OLD / 'backlog-ledger.jsonl.gz'
old_rows = lines(old_path)
old = {r['id']: (index, r) for index, r in enumerate(old_rows)}
assert len(old) == len(old_rows) == 8917 and len(baseline) == 2093
raw_path = ROOT / 'docs/internal/reports/maintenance-2026-11-18/source-intake/all-raw-id-ledger.jsonl.gz'
raw_rows = lines(raw_path)
raw_by_id = defaultdict(list)
for index, row in enumerate(raw_rows):
    raw_by_id[row['id']].append((index, row))
raw_unique_id_count = len(raw_by_id)
hf_path = ROOT / 'docs/internal/reports/maintenance-2026-11-18/source-intake/hf-board-reconciliation.json'
hf = load(hf_path)
hf_dates = defaultdict(set)
for day, board in hf['boards'].items():
    for ident in board['ids']:
        hf_dates[ident].add(day)
integration = load(ROOT / 'docs/internal/reports/maintenance-2026-11-18/source-intake/integration-receipt.json')

issue_path = RAW / 'remote-refresh-v1/open-issues.json'
issues = load(issue_path)
issue_ids = defaultdict(list)
for issue in issues:
    for aid in set(re.findall(r'arxiv.org/(?:abs|html|pdf)/(\d+\.\d+)', issue['body'] or '')):
        issue_ids['arxiv:' + aid].append({'number': issue['number'], 'url': issue['html_url'], 'observed_updated_at': issue['updated_at']})

four_path = REPORT / 'four-issue-evidence-v1.json'
four = {r['id']: r for r in load(four_path)['items']}
blocker_path = REPORT / 'source-blocker-assessments-v1.json'
blockers = {r['id']: r for r in load(blocker_path)['items']}
pair_path = REPORT / 'new-version-readback-v1.json'
pair_readbacks = {r['id']: r for r in load(pair_path)['items']}
existing_issues_path = REPORT / 'existing-issues-v1.json'
existing_issue_checks = {r['issue']: r for r in load(existing_issues_path)['items']}
carryforward_path = RAW / 'pr135-carryforward-v1.jsonl.gz'
carryforward = {r['id']: (i, r) for i, r in enumerate(lines(carryforward_path))}
assert len(carryforward) == 121
saved_reasons = {}
for filename in ['source-reviews.jsonl', 'adjudications.jsonl', 'negative-adjudications.jsonl']:
    path = ROOT / 'docs/internal/reports/maintenance-2026-10-30/independent' / filename
    for index, original in enumerate(lines(path)):
        payload = original.get('data') or original
        if payload.get('reason_zh'):
            saved_reasons[original['id']] = {'reference': reference(path, index), 'reason_zh': payload['reason_zh'], 'reading_limit': original.get('review_level'), 'new_review_claimed': False}
post_reasons_path = ROOT / 'docs/internal/reports/maintenance-2026-10-30/coverage/source-reports/post-model-reviews.json'
for index, original in enumerate(load(post_reasons_path)):
    if (original.get('gate') or {}).get('why_zh'):
        saved_reasons[original['id']] = {'reference': reference(post_reasons_path, index), 'reason_zh': original['gate']['why_zh'], 'reading_limit': 'saved_model_scope_opinion_not_new_independent_adjudication', 'new_review_claimed': False}

pr134 = load(RAW / 'remote-refresh-v1/pr-134.json')
assert pr134['merged'] and pr134['merged_by']['login'] == 'adongwanai'
assert pr134['base']['repo']['full_name'] == 'adongwanai/follow-rsi'
review134_path = RAW / 'remote-refresh-v1/pr-134--review--daily--2026-11-16.yaml'
review134 = yaml.safe_load(read(review134_path))
approved = {r['id']: r for r in review134['items'] + review134['lab_updates']}
assert len(approved) == 15
pr134_receipt = {'github_pr': 134, 'owner_login': pr134['merged_by']['login'], 'merge_commit': pr134['merge_commit_sha'], 'head_sha': pr134['head']['sha'], 'same_repository': True, 'review': reference(review134_path)}
adjudication_path = ROOT / args.adjudication
adjudication = {r['id']: (i, r) for i, r in enumerate(load(adjudication_path)['items'])} if adjudication_path.exists() else {}

local_publications = defaultdict(list)
for directory in ['site/daily', 'site/recaps']:
    for path in sorted((ROOT / directory).glob('*.json')):
        edition = load(path)
        for item in edition.get('items', []):
            local_publications[item['id']].append({'date': edition.get('date'), 'reviewed_on': edition.get('reviewed_on'), 'artifact': reference(path), 'live_verified_by_this_audit': False})

# Keep full old task evidence and separately retain every new raw metadata observation.
old_candidates_path = ROOT / 'data/feed/version-candidates/weekly-scan-2026-11-09.jsonl.gz'
old_candidates = {r['id']: r for r in lines(old_candidates_path)}
old_tasks_path = OLD / 'version-review-tasks.jsonl.gz'
old_tasks = lines(old_tasks_path)
old_daily_path = OLD / 'daily-metadata-review-tasks.jsonl.gz'
daily_tasks = lines(old_daily_path)
progress_path = OLD / 'version-review-progress.json'
progress = load(progress_path)
recovered = {}
for name in ['recovered-version-pairs.json', 'missing-original-version-identity.json']:
    path = RECOVERY / name
    for i, row in enumerate(load(path)['items']):
        recovered[(row['id'], row['target_version'])] = {**reference(path, i), 'status': row['recovery_status'], 'target_version': row['target_version'], 'original_version': row['current_version'], 'body_review_completed': False, 'formal_version_adopted': False}
tasks = {}
for index, task in enumerate(old_tasks):
    task = deepcopy(task)
    candidate = old_candidates[task['id']]['candidate']
    assert source_hash(candidate) == old_candidates[task['id']]['candidate_source_hash']
    task.update(task_key=content_key(candidate), candidate_version=candidate.get('version'), prior_task_ref=reference(old_tasks_path, index), current_source_hash=source_hash(canonical[task['id']]), candidate_scientific_metadata_sha256=content_key(candidate).split(':')[-1], previous_status_retained=True, production_fields_written=False)
    if (task['id'], candidate.get('version')) in recovered:
        task['source_recovery_ref'] = recovered[(task['id'], candidate.get('version'))]
        task['remaining_body_or_version_identity_work'] = True
    tasks[task['task_key']] = task
assert len(tasks) == 1627
pr117 = load(RAW / 'remote-refresh-v1/pr-117.json')
assert pr117['merged'] and pr117['merged_by']['login'] == 'adongwanai' and pr117['base']['repo']['full_name'] == 'adongwanai/follow-rsi'
scan_path = RAW / 'merged-inputs-v1/pr-117--data--feed--raw--arxiv-version-check--2026-11-16.json'
scan = load(scan_path)
assert len(scan['records']) == len(scan['requested_ids']) == 1913
observations = []
scan_reused = 0
for index, candidate in enumerate(scan['records']):
    ident = candidate['id']
    current = canonical[ident]
    key = content_key(candidate)
    metadata_fields = ['version', 'title', 'abstract', 'published', 'updated', 'announced', 'authors', 'retracted', 'links', 'hf_daily_dates']
    changed = {field: {'current': current.get(field), 'candidate': candidate.get(field)} for field in metadata_fields if current.get(field) != candidate.get(field)}
    observation = {'id': ident, 'task_key': key, 'raw_candidate_ref': reference(scan_path, index), 'raw_candidate_sha256': sha(json.dumps(candidate, sort_keys=True, ensure_ascii=False).encode()), 'candidate_version': candidate.get('version'), 'current_version': current.get('version'), 'current_source_hash': source_hash(current), 'field_differences': changed, 'raw_metadata_not_adopted': True, 'absence_of_hf_membership_in_arxiv_scan_is_not_retraction': True, 'first_seen_never_taken_from_rescan': True, 'github_pr': 117, 'owner_login': pr117['merged_by']['login'], 'merge_commit': pr117['merge_commit_sha']}
    observations.append(observation)
    if key in tasks:
        tasks[key].setdefault('matching_scan_refs', []).append(reference(scan_path, index))
        scan_reused += 1
        continue
    body_changed = candidate.get('version') != current.get('version') or any(textnorm(candidate.get(k)) != textnorm(current.get(k)) for k in ['title', 'abstract'])
    if candidate.get('version') != current.get('version'):
        status = 'new_scan_version_body_comparison_required' if current.get('version') else 'new_scan_original_version_identity_unresolved'
        actions = ['verify_original_and_target_version_identity', 'reuse_or_recover_exact_version_bodies', 'complete_scientific_delta_and_independent_cross_review', 'obtain_dated_receipt_before_version_adoption']
    elif body_changed:
        status = 'new_scan_same_version_source_text_delta_requires_field_review'
        actions = ['inspect_exact_title_or_abstract_delta_and_source_identity', 'distinguish_formatting_from_substantive_changes', 'preserve_prior_scope_and_receipts_until_verified']
    else:
        status = 'new_scan_metadata_only_preserve_scientific_snapshot'
        actions = ['validate_recorded_author_date_or_link_differences_before_optional_application', 'preserve_hf_membership_first_seen_and_formal_hash']
    task = {'task_key': key, 'id': ident, 'candidate_version': candidate.get('version'), 'candidate_ref': reference(scan_path, index), 'candidate_scientific_metadata_sha256': key.split(':')[-1], 'current_source_hash': source_hash(current), 'status': status, 'fulltext_review_required': body_changed, 'required_actions': actions, 'version_adopted_by_this_audit': False, 'production_fields_written': False}
    if ident in pair_readbacks and candidate.get('version') == pair_readbacks[ident]['candidate_version']:
        task.update(status=pair_readbacks[ident]['status'], partial_readback_ref={**reference(pair_path), 'id': ident}, required_actions=pair_readbacks[ident]['next_actions'], fulltext_review_required=True)
    tasks[key] = task
for task in daily_tasks:
    task['current_source_hash'] = source_hash(canonical[task['id']])
    task['reused_prior_task_without_new_scientific_claim'] = True
task_refs = defaultdict(list)
ordered_tasks = [tasks[key] for key in sorted(tasks)]
for i, task in enumerate(ordered_tasks):
    task_refs[task['id']].append({'path': relative(OUT / 'version-review-tasks.jsonl.gz'), 'index': i, 'task_key': task['task_key'], 'status': task['status'], 'fulltext_review_required': task.get('fulltext_review_required', False)})

ledger = []
source_changes = []
universe = set(old) | set(canonical) | set(raw_by_id) | set(issue_ids) | {r['id'] for r in ordered_tasks}
preserved_keys = ['processing_bucket', 'status', 'scope_recommendation', 'reason_zh', 'next_actions', 'latest_scope_advice_reusable', 'independent_scope_status', 'owner_scope_receipt', 'post_approval_correction', 'formal_content_equivalence_verified', 'legacy_discovery_member', 'legacy_discovery_and_failure_refs', 'historical_model_error', 'preserved_historical_model_error', 'catalog_entry', 'effective_scope_opinion_ref']
science_fields = ['id', 'version', 'title', 'abstract', 'links', 'retracted', 'published', 'updated', 'summary_zh', 'summary_en', 'evidence_quick', 'llm', 'gate', 'backfill_only']
for ident in sorted(universe):
    old_index, prior = old.get(ident, (None, {}))
    current = canonical.get(ident)
    row = {key: deepcopy(prior[key]) for key in preserved_keys if key in prior}
    row.update(id=ident, in_canonical=current is not None, title=(current or prior or (raw_by_id[ident][0][1] if raw_by_id[ident] else {})).get('title', 'unknown'), prior_ledger_ref=reference(old_path, old_index) if prior else None, canonical_source_hash=source_hash(current) if current else None, first_seen=(current or {}).get('first_seen'), published_original=(current or {}).get('published'), version_updated=(current or {}).get('updated'), canonical_version=(current or {}).get('version'), canonical_hf_daily_dates=(current or {}).get('hf_daily_dates', []), formal_review=(current or {}).get('review'), current_raw_refs=[reference(raw_path, i) for i, _ in raw_by_id[ident]], current_raw_dispositions=sorted({r['disposition'] for _, r in raw_by_id[ident]}), issue_refs=issue_ids[ident], version_tasks=task_refs[ident], local_publication_artifacts=local_publications[ident], live_publication_verified_by_this_audit=False, formal_hash_rebound_by_this_audit=False)
    row.setdefault('reason_zh', [])
    row.setdefault('next_actions', [])
    if current and not row['reason_zh']:
        if row.get('catalog_entry'):
            entry = row['catalog_entry']
            row['reason_zh'] = [f"既有目录记录 {entry['id']}，section={entry['section']}，scope={entry['scope']}；目录存在不等于本日新增或日报已出版。"]
        elif ident in saved_reasons:
            row['reason_zh'] = [saved_reasons[ident]['reason_zh']]
            row['restored_saved_reason_ref'] = saved_reasons[ident]
    row['owner_receipt_source_hash_matches_recomputed'] = bool(current and row.get('owner_scope_receipt') and row['owner_scope_receipt']['source_hash'] == row['canonical_source_hash'])
    row['missing_canonical_hf_dates'] = sorted(hf_dates[ident] - set(row['canonical_hf_daily_dates']))
    row['formal_review_source_hash_matches'] = bool(current and row['canonical_source_hash'] == (row['formal_review'] or {}).get('source_hash'))
    if not prior or (current and not prior.get('in_canonical')):
        if current:
            row.update(processing_bucket='pending_evidence', status='current_candidate_awaiting_consolidated_item_specific_review', scope_recommendation=None, reason_zh=['新增或上一维护日新增的规范记录；按当前逐项审核引用继续，不由本对账脚本创造范围意见。'], next_actions=['complete_or_reference_current_three_round_scope_review'])
        else:
            dispositions = row['current_raw_dispositions']
            bucket = 'pending_intake_integration' if 'within_requested_source_window' in dispositions or hf_dates[ident] or issue_ids[ident] else 'source_date_metadata_unavailable' if 'missing_publication_date' in dispositions else 'outside_candidate_window'
            row.update(processing_bucket=bucket, status={'pending_intake_integration': 'raw_or_issue_candidate_missing_canonical', 'source_date_metadata_unavailable': 'raw_source_date_unknown', 'outside_candidate_window': 'raw_only_outside_saved_source_windows'}[bucket], scope_recommendation=None, reason_zh=['原始来源逐ID保留；窗口资格和来源日期状态按当前采集回执，未进行论文范围排除。'], next_actions=['verify_identity_and_source_date_before_intake'] if bucket != 'outside_candidate_window' else [])
    if not current and ('within_requested_source_window' in row['current_raw_dispositions'] or hf_dates[ident] or issue_ids[ident]):
        row.update(processing_bucket='pending_intake_integration', status='raw_or_issue_candidate_missing_canonical', next_actions=['verify_identity_and_source_date_before_intake'])
    if ident in carryforward:
        ci, kept = carryforward[ident]
        row['pr135_preserved_recovery_ref'] = {**reference(carryforward_path, ci), 'archive_source_hash_matches_current': kept['canonical_source_hash_at_archive'] == row['canonical_source_hash']}
        row['owner_receipt_source_hash_matches_recomputed'] = bool(kept['owner_scope_receipt'] and kept['owner_scope_receipt']['receipt']['source_hash'] == row['canonical_source_hash'])
        row['reason_zh'] = list(dict.fromkeys(row['reason_zh'] + kept['reason_zh']))
        row['next_actions'] = kept['next_actions']
        row['status'] = kept['status']
        row['pr135_pending_evidence_or_editorial_checks'] = kept['pending_evidence_or_editorial_checks']
        row['issue_refs'] = list({r['number']: r for r in row['issue_refs'] + kept['issue_refs']}.values())
    if current and prior and prior.get('canonical_source_hash') and prior['canonical_source_hash'] != row['canonical_source_hash']:
        previous = baseline.get(ident)
        same_science = previous is not None and all(current.get(k) == previous.get(k) for k in science_fields)
        delta = {'id': ident, 'prior_source_hash': prior['canonical_source_hash'], 'current_source_hash': row['canonical_source_hash'], 'changed_fields_from_maintenance_baseline': sorted(k for k in set(current) | set(previous or {}) if current.get(k) != (previous or {}).get(k)), 'scientific_payload_unchanged_except_hf_membership': same_science, 'old_formal_review_preserved_not_rebound': current.get('review') == (previous or {}).get('review')}
        source_changes.append(delta)
        row['source_binding_delta'] = delta
        if not row['formal_review_source_hash_matches']:
            row.update(status='saved_science_reusable_new_hf_day_needs_dated_receipt' if same_science else 'changed_source_requires_specific_review', latest_scope_advice_reusable=same_science, next_actions=['retain_original_provenance', 'obtain_exact_current_hash_receipt_before_new_publication'])
    if ident in approved:
        proposal = approved[ident]
        matches = current is not None and row['canonical_source_hash'] == proposal['source_hash']
        row['merged_nov16_decision'] = {'decision': proposal['decision'], 'source_hash': proposal['source_hash'], 'current_hash_matches': matches, 'reason_zh': proposal['note'], 'provenance': pr134_receipt}
        if matches:
            row.update(processing_bucket='approved_change_awaiting_application', status='merged_exact_hash_decision_application_pending', scope_recommendation={'backlog': 'include', 'reject': 'exclude', 'defer': 'borderline'}[proposal['decision']], reason_zh=row['reason_zh'] + [proposal['note']], next_actions=['apply_real_merged_dated_review_and_verify_readback'])
    if ident in adjudication:
        index, proposal = adjudication[ident]
        matches = current is not None and row['canonical_source_hash'] == proposal['source_hash']
        row['current_adjudication_ref'] = {**reference(adjudication_path, index), 'source_hash_matches': matches, 'decision': proposal['decision']}
        if matches:
            row.update(processing_bucket='pending_evidence' if proposal['decision'] == 'defer' else 'actionable_scope_recommendation', status='specific_evidence_gap_retained' if proposal['decision'] == 'defer' else 'three_round_advice_ready_for_dated_application', scope_recommendation={'accept': 'include', 'backlog': 'include', 'reject': 'exclude', 'defer': 'borderline', 'move': 'exclude'}.get(proposal['decision']), reason_zh=row['reason_zh'] + [proposal.get('reason') or proposal.get('reason_zh')], next_actions=['resolve_item_specific_evidence_gap'] if proposal['decision'] == 'defer' else ['complete_dated_approval_apply_and_live_publication_verification'])
    if ident in four:
        row.update(processing_bucket='pending_evidence', status=four[ident]['status'], scope_recommendation='borderline', reason_zh=row['reason_zh'] + [four[ident]['reason_zh']], latest_scope_advice_reusable=True, current_evidence_refresh={**reference(four_path), 'id': ident}, next_actions=[four[ident]['reason_zh']])
    if ident in blockers:
        row.update(processing_bucket='external_blocked', status=blockers[ident]['status'], current_source_retry={**reference(blocker_path), 'id': ident}, reason_zh=row['reason_zh'] + [blockers[ident]['reason_zh']], next_actions=blockers[ident]['required_actions'])
    formal = row['formal_review'] or {}
    latest_advice = adjudication.get(ident, (None, approved.get(ident, {})))[1]
    latest_advice_applied = not latest_advice or (latest_advice.get('source_hash') == row['canonical_source_hash'] and latest_advice.get('decision') == formal.get('decision'))
    if row['formal_review_source_hash_matches'] and formal.get('decision') in {'accept', 'reject', 'backlog', 'move'} and latest_advice_applied:
        row.update(processing_bucket='formal_or_catalog_record', status='formal_' + formal['decision'] + '_source_bound', next_actions=[] if formal['decision'] in {'reject', 'move'} else ['verify_dated_publication_separately'] if formal['decision'] == 'accept' else ['retain_inclusion_scope_and_prepare_separate_eligible_publication'])
    row['new_model_success_claimed'] = False
    row['historical_error_retained_even_if_offline_scope_resolved'] = bool(row.get('historical_model_error') or row.get('preserved_historical_model_error'))
    ledger.append(row)

by_id = {r['id']: r for r in ledger}
issue_audit = []
for issue in issues:
    ids = sorted(ident for ident, refs in issue_ids.items() if any(r['number'] == issue['number'] for r in refs))
    item = {'number': issue['number'], 'url': issue['html_url'], 'title': issue['title'], 'state_when_refreshed': issue['state'], 'observed_updated_at': issue['updated_at'], 'ids': ids, 'item_statuses': [{'id': ident, 'status': by_id[ident]['status'], 'source_hash': by_id[ident]['canonical_source_hash'], 'reason_zh': by_id[ident]['reason_zh'], 'next_actions': by_id[ident]['next_actions']} for ident in ids], 'github_write_performed': False, 'recommend_close': False}
    if issue['number'] in existing_issue_checks:
        item['prior_verified_disposition'] = existing_issue_checks[issue['number']]
        item['recommend_close'] = existing_issue_checks[issue['number']]['recommend_close']
    if issue['number'] == 60:
        item.update(status='umbrella_evidence_followup_retained', blocker_ids=sorted(blockers), remaining_scope_evidence_ids=[r['id'] for r in ledger if r['in_canonical'] and r['processing_bucket'] == 'pending_evidence'])
    if issue['number'] in {115, 116}:
        item.update(status='version_pair_recovered_partial_readback_full_review_pending', partial_version_readback={**reference(pair_path), 'id': ids[0]})
    issue_audit.append(item)

jlout('backlog-ledger.jsonl.gz', ledger)
jlout('version-review-tasks.jsonl.gz', ordered_tasks)
jlout('weekly-metadata-observations.jsonl.gz', observations)
jlout('daily-metadata-review-tasks.jsonl.gz', daily_tasks)
jsonout(DOC / 'issue-disposition.json', {'snapshot': reference(issue_path), 'items': issue_audit, 'closures_performed': 0})
jsonout(DOC / 'source-hash-boundaries.json', {'items': source_changes, 'formal_hashes_rebound_by_this_audit': 0})
jsonout(DOC / 'approved-nov16-application-audit.json', {'provenance': pr134_receipt, 'items': [{'id': ident, 'approved_decision': proposal['decision'], 'approved_source_hash': proposal['source_hash'], 'canonical_source_hash': by_id[ident]['canonical_source_hash'], 'applied_with_exact_provenance': bool((canonical[ident].get('review') or {}).get('github_pr') == 134 and (canonical[ident].get('review') or {}).get('merge_commit') == pr134['merge_commit_sha'] and (canonical[ident].get('review') or {}).get('source_hash') == proposal['source_hash'] and (canonical[ident].get('review') or {}).get('decision') == proposal['decision'])} for ident, proposal in approved.items()]})
current_rows = [r for r in ledger if r['in_canonical']]
summary = {'date': '2026-11-18', 'stage': args.stage, 'finished_at': datetime.now(timezone.utc).isoformat(), 'canonical_input': reference(canonical_path), 'old_ledger': reference(old_path), 'universe_ids': len(ledger), 'canonical_ids': len(canonical), 'prior_canonical_ids': sum(r['in_canonical'] for r in old_rows), 'baseline_canonical_ids': len(baseline), 'canonical_buckets': dict(Counter(r['processing_bucket'] for r in current_rows)), 'all_id_buckets': dict(Counter(r['processing_bucket'] for r in ledger)), 'all_ids_have_recoverable_status': all(r.get('status') and 'next_actions' in r for r in ledger), 'old_ids_missing': sorted(set(old) - set(by_id)), 'old_discovery_members_preserved': sum(bool(r.get('legacy_discovery_member')) for r in ledger), 'old_historical_model_errors_preserved': sum(r['historical_error_retained_even_if_offline_scope_resolved'] for r in ledger), 'source_hash_changes_from_nov15': len(source_changes), 'existing_first_seen_changed': [ident for ident in baseline if ident in canonical and baseline[ident].get('first_seen') != canonical[ident].get('first_seen')], 'missing_current_window_ids': [ident for ident, occurrences in raw_by_id.items() if any(r['disposition'] == 'within_requested_source_window' for _, r in occurrences) and ident not in canonical], 'missing_hf_ids_or_dates': [{'id': r['id'], 'missing_dates': r['missing_canonical_hf_dates']} for r in ledger if r['missing_canonical_hf_dates']], 'current_raw_occurrences': len(raw_rows), 'current_raw_unique_ids': len(raw_by_id), 'old_version_task_count': len(old_tasks), 'new_weekly_metadata_observation_count': len(observations), 'scan_observations_reusing_same_content_task': scan_reused, 'combined_version_task_count': len(ordered_tasks), 'version_task_statuses': dict(Counter(t['status'] for t in ordered_tasks)), 'old_daily_metadata_task_count': len(daily_tasks), 'old_version_scope_comparisons_completed': progress['scope_comparisons_completed'], 'old_fulltext_or_original_identity_pending': len(recovered), 'old_recovered_version_pairs': sum(r['status'] == 'recovered' for r in recovered.values()), 'old_missing_original_version_identity': sum(r['status'] == 'missing_original_version_identity' for r in recovered.values()), 'new_version_pair_partial_readbacks': len(pair_readbacks), 'new_complete_scientific_version_reviews_by_this_audit': 0, 'formal_version_adoptions_by_this_audit': 0, 'approved_nov16_decisions': dict(Counter(r['decision'] for r in approved.values())), 'current_adjudicated_rows': len(adjudication), 'open_issue_snapshot_count': len(issues), 'recommended_issue_closures_from_existing_verified_evidence': [r['number'] for r in issue_audit if r['recommend_close']], 'source_blocker_retries': len(blockers), 'all_current_publications_live_verified': False, 'paid_requests': 0, 'production_writes': 0, 'github_writes': 0}
assert not summary['old_ids_missing'] and not summary['existing_first_seen_changed']
assert summary['old_historical_model_errors_preserved'] == 41
summary['current_raw_unique_ids'] = raw_unique_id_count
summary['legacy_discovery_or_failure_ids_with_refs'] = sum(bool(r.get('legacy_discovery_and_failure_refs')) for r in ledger)
summary['pr135_original_defer_ids_preserved'] = sum(bool(r.get('pr135_preserved_recovery_ref')) for r in ledger)
summary['canonical_ids_in_raw_only_buckets'] = [r['id'] for r in current_rows if r['processing_bucket'] in {'outside_candidate_window', 'source_date_metadata_unavailable', 'pending_intake_integration'}]
summary['current_adjudication_source_hash_mismatches'] = [ident for ident, (_, proposal) in adjudication.items() if ident not in canonical or source_hash(canonical[ident]) != proposal['source_hash']]
summary['restored_saved_item_specific_reasons'] = sum(bool(r.get('restored_saved_reason_ref')) for r in ledger)
assert summary['pr135_original_defer_ids_preserved'] == 121
assert not summary['canonical_ids_in_raw_only_buckets']
summary['input_drift'] = [path for path, evidence in inputs.items() if sha((ROOT / path).read_bytes()) != evidence['sha256']]
assert not summary['input_drift'], 'An input changed while reading; preserve this failed stage and rerun with a new name.'
jsonout(DOC / 'summary.json', summary)
jsonout(DOC / 'input-manifest.json', inputs)
manifest = {relative(path): {'sha256': sha(path.read_bytes()), 'bytes': path.stat().st_size} for path in sorted(list(OUT.iterdir()) + list(DOC.iterdir()))}
jsonout(DOC / 'freeze-manifest.json', manifest)
print(json.dumps(summary, ensure_ascii=False, indent=2))
