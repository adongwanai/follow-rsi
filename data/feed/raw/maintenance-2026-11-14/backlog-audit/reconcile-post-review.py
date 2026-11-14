# -*- coding: utf-8 -*-
"""Incremental Nov14 audit. No production/network writes or model requests.

Run after intake/formal application, optionally with --opinion PATH (repeatable)
and --resolution PATH for an explicit independent/adjudicated scope receipt.
"""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import copy
import gzip
import hashlib
import json
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from scripts.feed.review import source_hash
from scripts.feed.fetch_hf import parse_json as parse_hf

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--stage', choices=['post-intake', 'post-review'], required=True)
parser.add_argument('--opinion', action='append', default=[])
parser.add_argument('--resolution', action='append', default=[])
parser.add_argument('--correction-application')
args = parser.parse_args()
OUT = BASE / args.stage
assert not (OUT / 'freeze-manifest.json').exists(), 'Frozen stage cannot be overwritten'
assert not (OUT / 'summary.json').exists(), 'Completed stage cannot be overwritten'
if not OUT.exists():
    OUT.mkdir()
    snapshots = []
    for source, name in [('data/feed/items.jsonl', 'canonical-snapshot.jsonl'), ('data/papers.yaml', 'catalog-snapshot.yaml')]:
        data = (ROOT / source).read_bytes()
        (OUT / name).write_bytes(data)
        snapshots.append({'source': source, 'path': str((OUT / name).relative_to(ROOT)), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
    snapshot_reviews = []
    for path in sorted((ROOT / 'review').rglob('*.yaml')):
        data = path.read_bytes()
        snapshot_reviews.append({'source': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(data).hexdigest(), 'text': data.decode()})
    (OUT / 'review-directory-snapshot.json').write_text(json.dumps(snapshot_reviews, ensure_ascii=False, indent=2) + '\n')
    (OUT / 'stage-input-freeze.json').write_text(json.dumps({'frozen_at': datetime.now(timezone.utc).isoformat(), 'stage': args.stage, 'files': snapshots}, indent=2) + '\n')
now = datetime.now(timezone.utc).isoformat()
manifest = {}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    data = (ROOT / path).read_bytes()
    manifest[str(path)] = {'sha256': sha(data), 'bytes': len(data), 'read_at': datetime.now(timezone.utc).isoformat()}
    return data


def js(path):
    return json.loads(read(path))


def jl(path):
    data = read(path)
    if str(path).endswith('.gz'):
        data = gzip.decompress(data)
    return [json.loads(line) for line in data.splitlines() if line.strip()]


def dump(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n')


def rows_of(document):
    return document if isinstance(document, list) else document.get('items', document.get('rows', document.get('records', [])))


baseline_path = 'build/maintenance-2026-11-14/backlog-audit/prior-ledger.jsonl.gz'
baseline = {row['id']: row for row in jl(baseline_path)}
baseline_summary = js('build/maintenance-2026-11-14/backlog-audit/prior-summary.json')
canonical_path = str((OUT / 'canonical-snapshot.jsonl').relative_to(ROOT))
canonical_bytes = read(canonical_path)
canonical_rows = [json.loads(line) for line in canonical_bytes.splitlines()]
canonical = {row['id']: row for row in canonical_rows}
assert len(canonical_rows) == len(canonical)
old_canonical = {row['id']: row for row in jl('build/maintenance-2026-11-14/backlog-audit/canonical-baseline.jsonl')}
metadata_checks = {}
if args.correction_application:
    corrections = js(args.correction_application)
    for index, change in enumerate(corrections['items']):
        ident = change['id']
        before, after, current = change['before'], change['after'], canonical[ident]
        assert before == old_canonical[ident], ident
        assert source_hash(before) == change['source_hash_before'], ident
        assert source_hash(after) == change['source_hash_after'] == source_hash(current), ident
        assert sha(read(change['source']['file'])) == change['source']['raw_sha256'], ident
        for key in ('id', 'arxiv_id', 'version', 'published', 'updated', 'first_seen', 'hf_daily_dates'):
            assert before.get(key) == after.get(key) == current.get(key), (ident, key)
        old_review = before.get('review')
        assert not old_review or old_review == current.get('review') or old_review in current.get('review_history', []), ident
        formal_bound = current.get('review', {}).get('source_hash') == source_hash(current)
        metadata_checks[ident] = {
            'id': ident, 'fields_applied': change['fields'],
            'source_hash_before': change['source_hash_before'], 'source_hash_current': source_hash(current),
            'source_hash_matches_verified_plan': True, 'current_version_retained': True,
            'prior_review_preserved': True, 'formal_source_bound': formal_bound,
            'formal_rebinding_required': bool(old_review and not formal_bound),
            'no_effective_change': False, 'source_review_ref': args.correction_application,
            'application_index': index, 'scientific_version_binding_correction_not_version_upgrade': True,
            'production_modified_by_this_audit': False,
        }
catalog_bytes = read(str((OUT / 'catalog-snapshot.yaml').relative_to(ROOT)))
catalog = {'arxiv:' + str(row['arxiv']): row for row in yaml.load(catalog_bytes, Loader=yaml.CSafeLoader)['papers'] if row.get('arxiv')}
aliases = js('docs/internal/reports/maintenance-2026-11-08/summary.json')['aliases_resolved']
aliases.update({alias: row['id'] for row in canonical_rows for alias in row.get('aliases', [])})


def cid(ident):
    return ident if ident in canonical or ident in baseline else aliases.get(ident, ident)


records = copy.deepcopy(baseline)
raw_refs = defaultdict(list)
raw_eligibility = defaultdict(set)
sources = {}
raw_path = 'build/maintenance-2026-11-14/source-intake/raw-source-id-reconciliation.jsonl'
raw_rows = jl(raw_path)
for index, row in enumerate(raw_rows):
    ident = cid(row['id'])
    sources[ident] = row.get('record') or row
    raw_eligibility[ident].add(row['disposition'])
    raw_refs[ident].append({'path': raw_path, 'index': index, 'source_id': row.get('source_id'), 'disposition': row['disposition'], 'evidence': row.get('evidence')})

hf_dates = defaultdict(set)
hf_refs = defaultdict(list)
hf_snapshots = []
paths = sorted((ROOT / 'data/feed/raw/hf-daily').glob('*.json'))
paths += sorted((ROOT / 'build/maintenance-2026-11-14/source-intake/data/feed/raw/hf-daily').glob('*.json'))
for path in paths:
    rel = str(path.relative_to(ROOT))
    document = js(rel)
    assert document['format'] == 'hf-json-days', rel
    count = 0
    for day, payload in document['days'].items():
        for index, row in enumerate(parse_hf(payload, 'hf-daily', now=now, daily_date=day)):
            ident = cid(row['id'])
            sources.setdefault(ident, row)
            hf_dates[ident].add(day)
            hf_refs[ident].append({'path': rel, 'date': day, 'index': index})
            count += 1
    hf_snapshots.append({'path': rel, 'memberships': count, 'sha256': manifest[rel]['sha256']})

reviews = defaultdict(list)
review_files = []
for snapshot in js(str((OUT / 'review-directory-snapshot.json').relative_to(ROOT))):
    rel = snapshot['source']
    assert sha(snapshot['text'].encode()) == snapshot['sha256']
    document = yaml.load(snapshot['text'], Loader=yaml.CSafeLoader)
    if not isinstance(document, dict) or '/approvals/' in rel:
        continue
    count = 0
    for field in ('items', 'lab_updates'):
        for index, row in enumerate(document.get(field, [])):
            ident = cid(row['id'])
            reviews[ident].append({'path': rel, 'field': field, 'index': index, 'decision': row.get('decision'), 'source_hash': row.get('source_hash'), 'date': str(document.get('date') or document.get('week') or 'unknown'), 'snapshot_sha256': snapshot['sha256']})
            count += 1
    review_files.append({'path': rel, 'rows': count, 'snapshot_sha256': snapshot['sha256']})

issue_path = 'build/maintenance-2026-11-14/pr-audit/open-issues.json'
issue_refs = defaultdict(list)
issue_rows = rows_of(js(issue_path))
for row in issue_rows:
    for arxiv_id in row.get('arxiv_ids', []):
        ident = cid('arxiv:' + arxiv_id)
        issue_refs[ident].append({'path': issue_path, 'number': row['number'], 'url': row['url'], 'snapshot_updated_at': row.get('updated_at')})
        sources.setdefault(ident, {'id': ident, 'title': row['title']})

legacy_refs = defaultdict(list)
legacy_files = [
    'docs/internal/reports/maintenance-2026-10-29/deferred-discovery.json',
    'data/feed/normalized.json',
    'docs/internal/reports/maintenance-2026-11-08/legacy-error-retry-inputs.jsonl',
    'docs/internal/reports/maintenance-2026-11-08/legacy-error-retry-consolidated.jsonl',
]
legacy_files += [str(path.relative_to(ROOT)) for path in sorted((ROOT / 'data/feed/archive').glob('*.jsonl'))]
legacy_files += [str(path.relative_to(ROOT)) for path in sorted((ROOT / 'data/feed/intake').rglob('*source-records.jsonl'))]
legacy_inventory = []
for path in legacy_files:
    legacy_rows = jl(path) if path.endswith('.jsonl') else rows_of(js(path))
    for index, item in enumerate(legacy_rows):
        ident = cid(item['id'])
        legacy_refs[ident].append({'path': path, 'index': index})
        sources.setdefault(ident, item)
    legacy_inventory.append({'path': path, 'records': len(legacy_rows)})

version_path = 'data/feed/version-candidates/weekly-scan-2026-11-09.jsonl.gz'
versions = jl(version_path)
prior_tasks = jl('build/maintenance-2026-11-14/backlog-audit/supplemental-version-review/progress-version-review-tasks.jsonl.gz')
assert len(versions) == len(prior_tasks) == 1627
assert {row['id'] for row in versions} == {row['id'] for row in prior_tasks}
tasks = []
for task in prior_tasks:
    task = copy.deepcopy(task)
    task['current_source_hash'] = source_hash(canonical[task['id']]) if task['id'] in canonical else None
    task['reused_from'] = 'build/maintenance-2026-11-14/backlog-audit/supplemental-version-review/progress-version-review-tasks.jsonl.gz'
    task['scientific_body_review_performed_by_this_reconciliation'] = False
    task['formal_hash_rebound_by_this_reconciliation'] = False
    if task['id'] in metadata_checks:
        check = metadata_checks[task['id']]
        task['metadata_application_verification'] = check
        if not check['no_effective_change']:
            task['status'] = 'metadata_fields_applied_formal_rebinding_pending' if check['formal_rebinding_required'] else 'metadata_fields_applied_scientific_scope_retained'
            task['required_actions'] = ['obtain_new_exact_hash_formal_receipt_preserve_old_review'] if check['formal_rebinding_required'] else []
            task['fulltext_review_required'] = False
    tasks.append(task)
for candidate in versions:
    assert source_hash(candidate['candidate']) == candidate['candidate_source_hash']

proposal_path = 'build/maintenance-2026-11-14/source-intake/integration-proposal.json'
proposal = js(proposal_path)
metadata_followups = jl('build/maintenance-2026-11-14/backlog-audit/supplemental-version-review/progress-daily-metadata-review-tasks.jsonl.gz')
prior_daily_tasks_count = len(metadata_followups)
for index, item in enumerate(proposal['official_metadata_change_candidates']):
    fields = {key: value['official'] for key, value in item['differences'].items()}
    current = canonical[item['id']]
    metadata_followups.append({
        'id': item['id'], 'kind': 'daily_official_metadata_difference',
        'ref': {'path': proposal_path, 'index': index, 'field': 'official_metadata_change_candidates'},
        'current_source_hash': source_hash(current), 'target_fields': fields,
        'current_fields_already_match': all(current.get(key) == value for key, value in fields.items()),
        'status': 'pending_field_specific_metadata_review',
        'applied_by_this_audit': False,
    })
# Retain earlier field tasks, deduplicate identical target fields, and observe successful
# metadata applications by the maintainer without changing production or old receipts.
metadata_dedup = {}
def field_satisfied(ident, key, value):
    current_value = canonical[ident].get(key)
    if current_value == value:
        return True
    return bool(key in {'published', 'updated'} and current_value == old_canonical[ident].get(key) and str(current_value)[:10] == str(value)[:10])

for task in metadata_followups:
    task.setdefault('kind', 'official_residual_metadata_validation')
    key = (task['id'], json.dumps(task['target_fields'], sort_keys=True, ensure_ascii=False))
    if key in metadata_dedup:
        metadata_dedup[key].setdefault('equivalent_source_refs', []).append(task['ref'])
        continue
    current = canonical[task['id']]
    task['current_source_hash'] = source_hash(current)
    task['current_fields_already_match'] = all(current.get(k) == value for k, value in task['target_fields'].items())
    task['satisfied_fields'] = sorted(k for k, value in task['target_fields'].items() if field_satisfied(task['id'], k, value))
    task['remaining_fields'] = sorted(k for k, value in task['target_fields'].items() if not field_satisfied(task['id'], k, value))
    task['effective_fields_satisfied'] = not task['remaining_fields']
    if task['effective_fields_satisfied']:
        task['status'] = 'satisfied_by_current_canonical_fields' if task['current_fields_already_match'] else 'resolved_same_day_precision_preserve_existing_value'
        task['applied_by_this_audit'] = False
        task['fulltext_review_required'] = False
        if task['id'] in metadata_checks:
            task['metadata_application_verification'] = metadata_checks[task['id']]
    metadata_dedup[key] = task
metadata_followups = list(metadata_dedup.values())
version_progress = js('build/maintenance-2026-11-14/backlog-audit/supplemental-version-review/version-review-progress.json')
version_findings = {row['id']: (index, row) for index, row in enumerate(version_progress['items'])}
for task in metadata_followups:
    if task['remaining_fields'] and task['id'] in version_findings and not version_findings[task['id']][1]['fulltext_review_required']:
        index, finding = version_findings[task['id']]
        assert not finding['fulltext_review_required']
        task['status'] = 'version_comparison_completed_formal_snapshot_retained'
        task['fulltext_review_required'] = False
        task['version_comparison_ref'] = {'path': 'build/maintenance-2026-11-14/backlog-audit/supplemental-version-review/version-review-progress.json', 'index': index}
        task['required_actions'] = finding['next_actions']
    elif task['remaining_fields']:
        task.setdefault('fulltext_review_required', True)

opinion_paths = args.opinion
opinions = defaultdict(list)
resolution = {}
for path in dict.fromkeys(opinion_paths + args.resolution):
    for index, row in enumerate(rows_of(js(path))):
        ident = cid(row['id'])
        suggestion = row.get('suggestion') or row.get('scope_recommendation') or row.get('final_suggestion') or row.get('recommendation') or row.get('decision')
        suggestion = {'accept': 'include', 'reject': 'exclude', 'defer': 'borderline', 'move': 'exclude'}.get(suggestion, suggestion)
        row_hash = row.get('source_hash') or row.get('current_source_hash') or row.get('source_hash_after_metadata_normalization') or row.get('source_hash_of_proposed_record')
        entry = {'path': path, 'index': index, 'file_sha256': manifest[path]['sha256'], 'source_hash': row_hash, 'suggestion': suggestion, 'reason_zh': row.get('reason_zh') or row.get('note'), 'independent_review_required': row.get('independent_review_required', False), 'external_source_blocked': bool(row.get('external_source_blocked') or row.get('external_blocker')), 'exact_source_hash_match': ident in canonical and row_hash == source_hash(canonical[ident]), 'formal_authorization': False}
        opinions[ident].append(entry)
        if path in args.resolution:
            resolution[ident] = entry

retry_path = 'build/maintenance-2026-11-14/backlog-audit/blocker-retry-assessments.json'
retry_rows = js(retry_path)
assert len(retry_rows) == 9
for row in retry_rows:
    for attempt in row['attempts']:
        body = (BASE / attempt['file']).read_bytes()
        assert len(body) == attempt['bytes'] and sha(body) == attempt['sha256']
        assert attempt['file_exists'] is True
    assert not row['required_source_recovered'], 'Recovered source requires new evidence review'
retry = {row['id']: (index, row) for index, row in enumerate(retry_rows)}

universe = set(records) | set(canonical) | set(sources) | set(reviews) | set(issue_refs) | {row['id'] for row in versions} | set(opinions)
hash_changes = []
for ident in sorted(universe):
    current = canonical.get(ident)
    old = baseline.get(ident)
    row = records.setdefault(ident, {'id': ident, 'title': (current or sources.get(ident) or {}).get('title', 'unknown'), 'processing_bucket': 'uncovered', 'status': 'not_yet_classified', 'scope_recommendation': None, 'reason_zh': [], 'next_actions': [], 'source_opinions': [], 'raw_source_refs': [], 'raw_source_eligibility': [], 'current_external_blockers': [], 'latest_scope_advice_reusable': False})
    current_hash = source_hash(current) if current else None
    row.update({'in_canonical': bool(current), 'canonical_source_hash': current_hash, 'canonical_abstract_sha256': sha(current.get('abstract', '').encode()) if current else None, 'first_seen': (current or {}).get('first_seen'), 'published_original': (current or {}).get('published'), 'version_updated': (current or {}).get('updated'), 'canonical_hf_daily_dates': (current or {}).get('hf_daily_dates', []), 'raw_hf_daily_dates': sorted(hf_dates.get(ident, set())), 'missing_canonical_hf_dates': sorted(hf_dates.get(ident, set()) - set((current or {}).get('hf_daily_dates', []))), 'hf_board_refs': hf_refs.get(ident, []), 'review_queue_refs': reviews.get(ident, []), 'issue_refs': issue_refs.get(ident, []), 'formal_review': (current or {}).get('review'), 'live_publication_verified_by_this_audit': False, 'audit_ref': {'date': '2026-11-14', 'baseline_path': baseline_path, 'prior_row_reused': bool(old)}})
    row['title'] = (current or sources.get(ident) or row).get('title', row['title'])
    row['raw_source_refs'] += raw_refs.get(ident, [])
    row['raw_source_eligibility'] = sorted(set(row['raw_source_eligibility']) | raw_eligibility.get(ident, set()) | ({'hf_saved_board_membership'} if ident in hf_dates else set()))
    formal = row['formal_review'] or {}
    row['formal_review_source_hash_matches'] = bool(current_hash and current_hash == formal.get('source_hash'))
    if ident in catalog:
        row['catalog_entry'] = {key: catalog[ident].get(key) for key in ('id', 'scope', 'section', 'must_read')}
    if not current:
        if 'within_requested_source_window' in raw_eligibility.get(ident, set()) or ident in hf_dates or ident in issue_refs or ident in legacy_refs:
            row.update({'processing_bucket': 'pending_intake_integration', 'status': 'raw_or_issue_candidate_missing_canonical', 'next_actions': ['complete_source_identity_date_review_and_intake']})
        elif not old:
            bucket = 'source_date_metadata_unavailable' if 'missing_publication_date' in raw_eligibility.get(ident, set()) else 'outside_candidate_window'
            row.update({'processing_bucket': bucket, 'status': 'raw_source_date_unknown' if bucket == 'source_date_metadata_unavailable' else 'raw_only_outside_saved_source_windows', 'next_actions': ['recover_source_date_before_daily_eligibility'] if bucket == 'source_date_metadata_unavailable' else []})
    elif not old:
        row.update({'processing_bucket': 'pending_evidence', 'status': 'new_canonical_scope_review_not_yet_bound', 'next_actions': ['complete_item_specific_source_scope_review']})
    if current and old and old.get('canonical_source_hash') and old['canonical_source_hash'] != current_hash:
        prior = old_canonical.get(ident)
        keys = sorted(key for key in set(current) | set(prior or {}) if current.get(key) != (prior or {}).get(key))
        science = ('id', 'version', 'title', 'abstract', 'links', 'retracted', 'published', 'updated', 'summary_zh', 'summary_en', 'evidence_quick', 'llm', 'gate', 'backfill_only')
        same_science = prior is not None and all(current.get(key) == prior.get(key) for key in science)
        verified_metadata = metadata_checks.get(ident)
        advice_reusable = same_science or bool(verified_metadata)
        boundary = {'id': ident, 'old_source_hash': old['canonical_source_hash'], 'current_source_hash': current_hash, 'changed_fields': keys, 'scientific_payload_unchanged_except_hf_dates': same_science, 'verified_metadata_application': verified_metadata, 'unchanged_scientific_scope_advice_reusable': advice_reusable, 'formal_authorization_or_hash_refreshed_by_this_audit': False, 'formal_current_source_bound': row['formal_review_source_hash_matches']}
        hash_changes.append(boundary)
        row['incremental_source_binding_audit'] = boundary
        if not row['formal_review_source_hash_matches'] and ident not in catalog:
            pending_scope = old['processing_bucket'] == 'pending_evidence'
            row.update({'processing_bucket': 'reusable_scope_advice' if advice_reusable and not pending_scope else 'pending_evidence', 'status': 'verified_metadata_applied_existing_scope_gap_preserved' if verified_metadata and pending_scope else 'verified_metadata_applied_formal_receipt_pending' if verified_metadata else 'saved_science_reusable_new_metadata_receipt_required' if same_science else 'changed_source_requires_field_specific_review', 'latest_scope_advice_reusable': advice_reusable, 'next_actions': ['preserve_old_formal_hash_and_provenance', 'obtain_new_exact_hash_formal_receipt'] if verified_metadata and verified_metadata['formal_rebinding_required'] else old.get('next_actions', []) if verified_metadata else ['preserve_old_formal_hash_and_provenance', 'verify_changed_source_fields_before_new_dated_receipt']})
        if verified_metadata:
            row['metadata_scope_reuse'] = verified_metadata
    if ident in opinions:
        row['source_opinions'] += opinions[ident]
        valid = [op for op in opinions[ident] if op['exact_source_hash_match'] or op.get('verified_metadata_only_scope_rebinding', {}).get('matches_current_source_hash')]
        resolved = resolution.get(ident)
        if resolved and resolved['exact_source_hash_match']:
            selected = resolved
            pending = selected['suggestion'] not in {'include', 'exclude'}
            row.update({'processing_bucket': 'pending_evidence' if pending else 'reusable_scope_advice', 'status': 'specific_scope_evidence_pending' if pending else 'independently_adjudicated_scope_advice_available', 'scope_recommendation': selected['suggestion'], 'latest_scope_advice_reusable': True, 'effective_scope_opinion_ref': {'path': selected['path'], 'index': selected['index']}, 'independent_scope_status': 'explicit_current_scope_receipt', 'next_actions': ['resolve_recorded_artifact_or_scope_gap'] if pending else ['complete_formal_review_before_publication']})
            if selected['external_source_blocked']:
                row.update({'processing_bucket': 'external_blocked', 'status': 'new_source_blocker_confirmed_by_independent_review', 'current_external_blockers': [selected['reason_zh']], 'next_actions': ['obtain_required_official_original_source_before_scope_decision']})
        elif valid:
            labels = {op['suggestion'] for op in valid if op['suggestion']}
            selected = valid[-1]
            requires_independent = any(op['independent_review_required'] for op in valid)
            pending = requires_independent or len(labels) != 1 or selected['suggestion'] not in {'include', 'exclude'}
            row.update({'processing_bucket': 'pending_evidence' if pending else 'reusable_scope_advice', 'status': 'source_advice_requires_independent_adjudication' if pending else 'source_scope_advice_available', 'scope_recommendation': selected['suggestion'] if len(labels) == 1 else 'borderline', 'latest_scope_advice_reusable': True, 'effective_scope_opinion_ref': {'path': selected['path'], 'index': selected['index']}, 'next_actions': ['independent_scope_crosscheck_or_artifact_boundary'] if pending else ['complete_formal_review_before_publication']})
        row['reason_zh'] += [op['reason_zh'] for op in opinions[ident] if op.get('reason_zh')]
    if ident in retry:
        index, result = retry[ident]
        row.update({'processing_bucket': 'external_blocked', 'status': 'source_blocker_reconfirmed_2026_11_14', 'source_retry_status': result['status'], 'current_retry_ref': {'path': str((BASE / 'blocker-retry-assessments.json').relative_to(ROOT)), 'index': index}, 'next_actions': ['obtain_official_abstract_or_methods_text_from_public_author_source'], 'reason_zh': row['reason_zh'] + [result['assessment_zh']]})
    if current and row['formal_review_source_hash_matches'] and formal.get('decision') in {'accept', 'reject', 'move', 'backlog'}:
        row.update({'processing_bucket': 'formal_or_catalog_record', 'status': 'formal_' + formal['decision'] + '_source_bound'})
        completed_action = 'complete_formal_review_before_publication'
        if completed_action in row['next_actions']:
            row.setdefault('observed_completed_actions', []).append({
                'action': completed_action,
                'basis': 'canonical formal decision is bound to current source hash',
                'review_date': formal.get('date'),
                'github_pr': formal.get('github_pr'),
                'source_hash': current_hash,
                'publication_verified_by_this_audit': False,
            })
            row['next_actions'] = [action for action in row['next_actions'] if action != completed_action]
    elif current and ident in catalog and (not old or old.get('processing_bucket') == 'formal_or_catalog_record'):
        row.update({'processing_bucket': 'formal_or_catalog_record', 'status': 'existing_catalog_record_no_new_publication_claim'})
    if ident == 'arxiv:2610.05533' and ident in metadata_checks:
        row.update({
            'processing_bucket': 'pending_evidence',
            'status': 'v1_metadata_corrected_full_dated_publication_review_pending',
            'scope_recommendation': 'include',
            'latest_scope_advice_reusable': True,
            'external_source_blocked': False,
            'current_external_blockers': [],
            'internal_binding_correction_observed': metadata_checks[ident],
            'next_actions': ['complete_full_current_v1_dated_publication_review', 'do_not_adopt_v3_without_separate_version_bound_review'],
        })
    row['legacy_discovery_and_failure_refs'] = legacy_refs.get(ident, [])
    row['current_metadata_pending_flag'] = bool(current and current.get('metadata_pending'))
    row['preserved_historical_model_error'] = (current or {}).get('llm', {}).get('error')

for index, task in enumerate(tasks):
    records[task['id']]['staged_metadata_revision'] = {'path': str((OUT / 'version-review-tasks.jsonl.gz').relative_to(ROOT)), 'index': index, 'group': task['group'], 'status': task['status'], 'current_review_snapshot_preserved': True}
for index, task in enumerate(metadata_followups):
    records[task['id']].setdefault('incremental_metadata_followups', []).append({
        'path': str((OUT / 'daily-metadata-review-tasks.jsonl.gz').relative_to(ROOT)),
        'index': index, 'kind': task['kind'], 'status': task['status'],
    })
ordered = [records[ident] for ident in sorted(records)]
current_rows = [row for row in ordered if row['in_canonical']]
eligible_missing = [row['id'] for row in ordered if row['processing_bucket'] == 'pending_intake_integration']
uncovered = [row['id'] for row in current_rows if row['status'] in {'new_canonical_scope_review_not_yet_bound', 'not_yet_classified'} or row['processing_bucket'] == 'uncovered']
hf_missing = [{'id': row['id'], 'missing_dates': row['missing_canonical_hf_dates']} for row in ordered if row['missing_canonical_hf_dates']]
source_snapshot = js('build/maintenance-2026-11-14/source-intake/all-source-snapshot.json')
source_counts = {key: source_snapshot.get(key) for key in ('generated_at', 'target_day', 'enabled_sources', 'sources_finished', 'all_sources_attempted_and_finished', 'raw_occurrences', 'raw_unique_ids', 'new_items', 'proposed_new_ids')}
drift = [path for path, entry in manifest.items() if sha((ROOT / path).read_bytes()) != entry['sha256']]
summary = {'schema_version': 3, 'date': '2026-11-14', 'started_at': now, 'completed_at': datetime.now(timezone.utc).isoformat(), 'baseline_path': baseline_path, 'baseline_universe_ids': len(baseline), 'universe_ids': len(ordered), 'new_union_ids': sorted(set(records) - set(baseline)), 'canonical_ids': len(canonical), 'canonical_snapshot': {'path': str((OUT / 'canonical-snapshot.jsonl').relative_to(ROOT)), **manifest[canonical_path]}, 'bucket_partition': dict(Counter(row['processing_bucket'] for row in ordered)), 'canonical_bucket_partition': dict(Counter(row['processing_bucket'] for row in current_rows)), 'canonical_status_partition': dict(Counter(row['status'] for row in current_rows)), 'canonical_pending_evidence_ids': [row['id'] for row in current_rows if row['processing_bucket'] == 'pending_evidence'], 'canonical_external_blocker_ids': [row['id'] for row in current_rows if row['processing_bucket'] == 'external_blocked'], 'eligible_raw_not_in_canonical_ids': eligible_missing, 'uncovered_canonical_ids': uncovered, 'hf_full_membership': {'snapshots': hf_snapshots, 'unique_ids': len(hf_dates), 'missing_memberships': hf_missing, 'total_missing_memberships': sum(len(row['missing_dates']) for row in hf_missing)}, 'review_queues': {'files': review_files, 'unique_ids': len(reviews), 'missing_canonical': sorted(set(reviews) - set(canonical))}, 'issue_reconciliation': {'snapshot_path': issue_path, 'issues': len(issue_rows), 'arxiv_ids': len(issue_refs), 'missing_canonical_ids': sorted(set(issue_refs) - set(canonical))}, 'version_candidates': {'count': len(tasks), 'groups': dict(Counter(row['group'] for row in tasks)), 'full_body_reviews_performed_by_this_reconciliation': 0, 'new_version_comparisons_recorded': version_progress['new_version_pairs_compared'], 'saved_comparisons_reused': version_progress['unchanged_scope_reuse'], 'new_formal_hash_bindings_created_by_this_reconciliation': 0}, 'source_blocker_retries': {'items': len(retry), 'requests': sum(len(row['attempts']) for row in retry_rows), 'recovered_required_sources': 0, 'http_statuses': dict(Counter(a['http_status'] for row in retry_rows for a in row['attempts']))}, 'targeted_suggestions': {ident: {'latest_suggestion': values[-1]['suggestion'], 'current_status': records[ident]['status'], 'scope_receipt': resolution.get(ident)} for ident, values in opinions.items()}, 'incremental_source_hash_changes': hash_changes, 'historical_formal_content_equivalence_verified': baseline_summary['historical_formal_content_equivalence_verified'], 'requested_four_paper_state': {name: {key: catalog[ident].get(key) for key in ('id', 'scope', 'section', 'must_read')} for name, ident in {'rsihub': 'arxiv:2610.32253', 'harnessdev': 'arxiv:2609.01437', 'aspire': 'arxiv:2608.31111', 's3gym': 'arxiv:2608.31100'}.items()}, 'source_collection': source_counts, 'concurrent_input_changes_after_freeze': drift, 'input_manifest': manifest, 'paid_calls': 0, 'production_writes': 0, 'github_writes': 0, 'online_publication_verified': False, 'limits_zh': ['复用Nov11已完成的稳定ID台账，既有来源哈希未变的意见与正式凭据沿用，不重跑全量模型。', '所有当前保存HF榜单、今日完整原始成员、规范库、审核单与实时issue映射均逐ID对账；原始日期缺失或窗口外记录不冒充今日论文。', '1,627项周扫候选已逐项区别正文审查和元数据处理；1171项信息性/同日精度/派生日期重复可保留当前科学快照，64项官方字段已核待哈希应用，392项待版本或文本审查，不刷新正式批准哈希。', '四个旧候选的来源刷新、可复用旧正文证据和具体工件缺口逐项保留；建议不冒充正式决定。', '9项来源阻塞经过18次免费尝试，仍未获得所需正文；具体403、429、超时及200元数据响应见逐项回执。', '本地正式记录不等于本子任务验证了GitHub合并或线上部署。']}
summary['hf_full_membership']['unique_snapshot_payloads'] = len({row['sha256'] for row in hf_snapshots})
summary['legacy_inventory'] = {'files': legacy_inventory, 'unique_ids': len(legacy_refs), 'missing_canonical_ids': sorted(set(legacy_refs) - set(canonical))}
summary['historical_model_errors'] = {
    'count': sum(bool(row['preserved_historical_model_error']) for row in current_rows),
    'current_buckets': dict(Counter(row['processing_bucket'] for row in current_rows if row['preserved_historical_model_error'])),
    'ids': [row['id'] for row in current_rows if row['preserved_historical_model_error']],
    'old_errors_not_erased_by_offline_review': True,
    'new_model_requests': 0,
}
summary['metadata_review_inventory'] = {
    'existing_staged_version_tasks': len(tasks),
    'new_daily_field_review_rows': sum(task['kind'] == 'daily_official_metadata_difference' for task in metadata_followups),
    'old_issue_revision_verified_rows': sum(task['kind'] == 'verified_old_issue_revision' for task in metadata_followups),
    'daily_rows_current_fields_already_match': sum(task['current_fields_already_match'] for task in metadata_followups),
    'unique_ids_with_staged_or_daily_tasks': len({task['id'] for task in tasks + metadata_followups}),
    'canonical_metadata_pending_flags': sum(row['current_metadata_pending_flag'] for row in current_rows),
    'metadata_pending_flags_without_staged_or_daily_task_ids': sorted({row['id'] for row in current_rows if row['current_metadata_pending_flag']} - {task['id'] for task in tasks + metadata_followups}),
    'body_reviews_or_formal_hash_rebindings_by_this_audit': 0,
}
version_progress = js('build/maintenance-2026-11-14/backlog-audit/supplemental-version-review/version-review-progress.json')
summary['stage'] = args.stage
summary['metadata_review_type_triage'] = {
    'weekly_classification': dict(Counter(task['group'] for task in tasks)),
    'weekly_statuses': dict(Counter(task['status'] for task in tasks)),
    'weekly_body_review_required': sum(task['fulltext_review_required'] for task in tasks),
    'weekly_prior_body_or_text_tasks': sum(row.get('fulltext_review_required', False) for row in jl('build/maintenance-2026-11-14/backlog-audit/prior-version-tasks.jsonl.gz')),
    'new_version_pairs_compared': version_progress['new_version_pairs_compared'],
    'saved_body_comparisons_reused': version_progress['unchanged_scope_reuse'],
    'display_only_text_tasks_resolved': 0,
    'completed_scope_comparison_rows': version_progress['scope_comparisons_completed'],
    'retained_prior_daily_rows': prior_daily_tasks_count,
    'deduplicated_daily_task_rows': len(metadata_followups),
    'daily_statuses': dict(Counter(task['status'] for task in metadata_followups)),
    'daily_effective_fields_satisfied': sum(task['effective_fields_satisfied'] for task in metadata_followups),
    'daily_fields_remaining_rows': sum(not task['effective_fields_satisfied'] for task in metadata_followups),
    'daily_remaining_body_review_ids': sorted({task['id'] for task in metadata_followups if task.get('fulltext_review_required')}),
    'daily_completed_comparison_but_formal_version_not_applied_ids': sorted({task['id'] for task in metadata_followups if task['status'] == 'version_comparison_completed_formal_snapshot_retained'}),
    'all_version_body_review_ids_deduplicated': sorted({task['id'] for task in tasks + metadata_followups if task.get('fulltext_review_required')}),
    'all_version_body_review_count_deduplicated': len({task['id'] for task in tasks + metadata_followups if task.get('fulltext_review_required')}),
    'body_comparisons_are_not_formal_version_adoption': True,
    'canonical_fields_modified_by_reconciliation': 0,
    'version_review_progress': 'build/maintenance-2026-11-14/backlog-audit/supplemental-version-review/version-review-progress.json',
}
summary['limits_zh'] = [
    'Reuse Nov13 source-bound stable-ID ledger; no production, paid model or GitHub writes.',
    'All saved HF members, complete today raw IDs, canonical, review queues, legacy discovery/retries and open issues reconciled.',
    'Version work: 39 pairs compared; 24 unchanged-scope reuses and 5 independent changed-pair scope comparisons complete; 10 partial readbacks remain. No version adopted.',
    'Four old issues retain exact artifact gaps; current official body bytes equal prior evidence, so reuse is explicitly labelled.',
    'Nine prior external blockers retried through 18 free requests; none recovered. New blockers are counted separately.',
    'Frozen local formal state is not a claim of GitHub merge or online publication.',
]
summary['stage'] = args.stage
summary['version_review_progress'] = {key: version_progress[key] for key in ('initial_fulltext_union', 'new_version_pairs_compared', 'scope_comparisons_completed', 'unchanged_scope_reuse', 'substantive_comparisons_independently_reviewed', 'changed_pairs_still_requiring_review', 'required_pair_not_yet_available', 'remaining_fulltext_union')}
summary['current_v1_source_normalization_observed'] = {
    'application_path': args.correction_application,
    'items': list(metadata_checks.values()),
    'count': len(metadata_checks),
    'versions_upgraded': 0,
    'production_writes_by_this_audit': 0,
}
assert sum(summary['canonical_bucket_partition'].values()) == len(canonical)
assert sum(summary['bucket_partition'].values()) == len(ordered)
assert len({row['id'] for row in ordered}) == len(ordered)
for name, rows in [('backlog-ledger.jsonl.gz', ordered), ('version-review-tasks.jsonl.gz', tasks), ('daily-metadata-review-tasks.jsonl.gz', metadata_followups)]:
    payload = ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows).encode()
    (OUT / name).write_bytes(gzip.compress(payload, mtime=0))
dump('summary.json', summary)
dump('source-hash-boundaries.json', {'current_changes': hash_changes, 'historical_equivalence': summary['historical_formal_content_equivalence_verified'], 'new_formal_authorizations_created_by_audit': 0})
dump('validation.json', {'stable_id_union': len(ordered), 'canonical_partition_complete': True, 'eligible_raw_missing_canonical': eligible_missing, 'uncovered_canonical': uncovered, 'hf_missing_memberships': hf_missing, 'review_ids_missing_canonical': summary['review_queues']['missing_canonical'], 'version_payload_hashes_verified': len(versions), 'version_followups_preserved': len(tasks), 'blocker_response_hashes_verified': sum(bool(a.get('file')) for row in retry_rows for a in row['attempts']), 'concurrent_input_changes_after_freeze': drift, 'paid_calls': 0, 'production_writes': 0})
lines = ['# 2026-11-14 backlog reconciliation', '', f"Stage: {args.stage}; canonical {len(canonical)}; stable-ID union {len(ordered)}.", '', '| Canonical state | Count |', '|---|---:|']
lines += [f'| {key} | {value} |' for key, value in sorted(summary['canonical_bucket_partition'].items())]
lines += ['', f"Missing eligible raw IDs: {len(eligible_missing)}; uncovered canonical: {len(uncovered)}; missing HF dates: {summary['hf_full_membership']['total_missing_memberships']}.", f"Version work: {version_progress['scope_comparisons_completed']} scope comparisons completed, {version_progress['remaining_fulltext_union']} still require body review; version adoption 0."]
lines += ['- ' + line for line in summary['limits_zh']]
(OUT / 'summary.md').write_text('\n'.join(lines) + '\n')
freeze = {'frozen_at': datetime.now(timezone.utc).isoformat(), 'stage': args.stage, 'files': []}
for path in sorted(OUT.iterdir()):
    if path.is_file():
        payload = path.read_bytes()
        freeze['files'].append({'path': str(path.relative_to(ROOT)), 'sha256': sha(payload), 'bytes': len(payload)})
dump('freeze-manifest.json', freeze)
print(json.dumps({key: summary[key] for key in ('universe_ids', 'canonical_ids', 'canonical_bucket_partition', 'eligible_raw_not_in_canonical_ids', 'uncovered_canonical_ids', 'concurrent_input_changes_after_freeze')}, ensure_ascii=False, indent=2))
