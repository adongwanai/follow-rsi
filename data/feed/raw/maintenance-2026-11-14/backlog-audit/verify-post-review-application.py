# -*- coding: utf-8 -*-
"""Verify the separately frozen Nov14 application; never edit a stage or production."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import sys
import yaml

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
RUN = BASE.parent
sys.path.insert(0, str(ROOT))
from scripts.feed.review import OWNER_FIELDS, source_hash


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def js(path):
    return json.loads(path.read_text())


def jl(path):
    payload = path.read_bytes()
    if path.suffix == '.gz':
        payload = gzip.decompress(payload)
    return [json.loads(line) for line in payload.splitlines()]


def rel(path):
    return str(path.relative_to(ROOT))


manifests = []
for path in (BASE / 'archive-handoff.json', BASE / 'post-intake/freeze-manifest.json',
             BASE / 'supplemental-version-review/freeze-manifest.json',
             BASE / 'post-review/freeze-manifest.json'):
    document = js(path)
    for entry in document['files']:
        original = ROOT / entry['path']
        assert sha(original) == entry['sha256'], entry['path']
        assert original.stat().st_size == entry['bytes'], entry['path']
    manifests.append({'path': rel(path), 'sha256': sha(path), 'verified_files': len(document['files'])})

before_rows = jl(BASE / 'post-intake/canonical-snapshot.jsonl')
after_rows = jl(BASE / 'post-review/canonical-snapshot.jsonl')
assert [row['id'] for row in before_rows] == [row['id'] for row in after_rows]
before = {row['id']: row for row in before_rows}
after = {row['id']: row for row in after_rows}
assert len(before) == len(after) == 2074
assert all(row.get('first_seen') == after[ident].get('first_seen') for ident, row in before.items())
expected = deepcopy(before)
corrections = js(RUN / 'current-v1-metadata-application.json')
for change in corrections['items']:
    ident = change['id']
    assert change['before'] == before[ident]
    assert source_hash(change['before']) == change['source_hash_before']
    assert source_hash(change['after']) == change['source_hash_after']
    assert sha(ROOT / change['source']['file']) == change['source']['raw_sha256']
    assert change['before']['review'] in change['after']['review_history']
    expected[ident] = deepcopy(change['after'])

applications = js(RUN / 'publication-generation.json')
applied = []
review_bindings = []
allowed_yaml_changes = set()
for application in applications:
    number = application['github_pr']
    merged = js(RUN / f'pr-{number}-merged.json')
    checks = js(RUN / f'pr-{number}-checks.json')
    assert merged['number'] == number and merged['merged'] is True
    assert merged['head']['sha'] == checks['head'] == application['head']
    assert merged['head']['repo']['full_name'] == merged['base']['repo']['full_name'] == 'adongwanai/follow-rsi'
    assert merged['merge_commit_sha'] == application['merge_commit']
    assert merged['merged_by']['login'] == application['owner_login'] == 'adongwanai'
    assert checks['required_passed']
    for name in ('validate', 'build', 'validate-owner-decisions'):
        assert checks['checks'][name]['status'] == 'completed'
        assert checks['checks'][name]['conclusion'] == 'success'
    review_path = ROOT / application['path']
    assert sha(review_path) == application['review_sha256']
    document = yaml.load(review_path.read_text(), Loader=yaml.CSafeLoader)
    review_rows = {row['id']: row for row in document['items'] + document['lab_updates']}
    assert str(document['date']) == application['date']
    assert application['applied_records'] == len(application['applied_ids'])
    for ident in application['applied_ids']:
        assert ident not in applied
        record = after[ident]
        review = record['review']
        row = review_rows[ident]
        assert source_hash(record) == row['source_hash'] == review['source_hash']
        assert all(review.get(key) == row.get(key) for key in OWNER_FIELDS)
        assert review['date'] == application['date']
        assert review.get('reviewed_on') == str(document['reviewed_on'])
        assert all(review[key] == application[key] for key in ('github_pr', 'owner_login', 'merge_commit'))
        expected[ident]['review'] = deepcopy(review)
        applied.append(ident)
    allowed_yaml_changes.add(application['path'])
    review_bindings.append({'date': application['date'], 'github_pr': number,
                           'head': application['head'], 'merge_commit': application['merge_commit'],
                           'owner_login': application['owner_login'], 'review_sha256': sha(review_path),
                           'applied_ids': application['applied_ids'],
                           'saved_github_merge_response_sha256': sha(RUN / f'pr-{number}-merged.json'),
                           'saved_ci_response_sha256': sha(RUN / f'pr-{number}-checks.json')})

metadata = js(RUN / 'metadata-rebinding-application.json')
ident = metadata['id']
assert ident not in applied
assert metadata['applied'] and not metadata['republication']
assert before[ident]['review'] == metadata['review_before']
assert after[ident]['review'] == metadata['review_after']
receipt = metadata['receipt']
assert source_hash(after[ident]) == receipt['new_source_hash']
assert receipt['old_source_hash'] == metadata['review_before']['source_hash']
assert sha(ROOT / receipt['attachment_path']) == receipt['attachment_sha256']
assert receipt in metadata['review_after']['metadata_rebindings']
assert metadata['review_after']['github_pr'] == metadata['review_before']['github_pr'] == 52
old_review = metadata['review_before']
new_review = metadata['review_after']
assert {k: v for k, v in old_review.items() if k not in ('source_hash', 'metadata_rebindings')} == {
    k: v for k, v in new_review.items() if k not in ('source_hash', 'metadata_rebindings')}
app107 = next(app for app in applications if app['github_pr'] == receipt['github_pr'])
assert all(receipt[key] == app107[key] for key in ('head', 'merge_commit', 'owner_login'))
for entry in metadata['protected_original_files']:
    assert sha(ROOT / entry['path']) == entry['sha256']
expected[ident]['review'] = deepcopy(new_review)
assert expected == after, [ident for ident in after if expected[ident] != after[ident]]
assert len(applied) == 46

prior_reviews = js(BASE / 'post-intake/review-directory-snapshot.json')
preserved_yaml = []
for entry in prior_reviews:
    if entry['source'] in allowed_yaml_changes:
        continue
    assert sha(ROOT / entry['source']) == entry['sha256'], entry['source']
    preserved_yaml.append(entry['source'])

supplemental_ids = {'arxiv:2610.02687', 'arxiv:2610.14018'}
for name in ('progress-version-review-tasks.jsonl.gz', 'progress-daily-metadata-review-tasks.jsonl.gz'):
    original = jl(BASE / name)
    incremental = jl(BASE / 'supplemental-version-review' / name)
    assert [r['id'] for r in original] == [r['id'] for r in incremental]
    for old, new in zip(original, incremental):
        if old['id'] not in supplemental_ids:
            assert old == new
        else:
            assert old['fulltext_review_required'] and not new['fulltext_review_required']
            assert source_hash(after[new['id']]) == new['current_source_hash']

summary = js(BASE / 'post-review/summary.json')
assert summary['metadata_review_inventory']['all_version_body_review_count_deduplicated'] == 347
assert summary['version_review_progress']['scope_comparisons_completed'] == 29
assert not summary['eligible_raw_not_in_canonical_ids']
assert not summary['uncovered_canonical_ids']
assert not summary['concurrent_input_changes_after_freeze']
assert summary['hf_full_membership']['total_missing_memberships'] == 0
changed = [{'id': ident, 'fields': sorted(key for key in set(before[ident]) | set(after[ident])
                                       if before[ident].get(key) != after[ident].get(key))}
           for ident in before if before[ident] != after[ident]]
assert len(changed) == 47
result = {
    'verified_at': datetime.now(timezone.utc).isoformat(),
    'manifests_verified': manifests, 'canonical_ids': len(after),
    'stable_id_order_and_first_seen_preserved': True,
    'source_field_corrections': 3, 'source_field_correction_receipt': rel(RUN / 'current-v1-metadata-application.json'),
    'formal_records_applied': len(applied),
    'formal_applied_decisions': dict(Counter(after[ident]['review']['decision'] for ident in applied)),
    'dated_review_bindings': review_bindings,
    'metadata_only_records_rebound': 1, 'metadata_original_acceptance_pr_retained': 52,
    'metadata_addition_authorized_by_pr': receipt['github_pr'],
    'metadata_protected_files_unchanged': len(metadata['protected_original_files']),
    'metadata_legacy_replay_limitation': metadata['legacy_replay_limitation'],
    'preserved_prior_review_yaml_count': len(preserved_yaml),
    'changed_rows': changed, 'unexplained_canonical_changes': [],
    'final_bucket_partition': summary['canonical_bucket_partition'],
    'scope_comparisons_complete': 29, 'remaining_version_body_review': 347,
    'version_adoptions': 0, 'production_writes': 0, 'paid_calls': 0, 'github_writes': 0,
    'live_github_requests_by_this_verification': 0,
    'evidence_boundary': 'Verified saved actual GitHub merge/CI responses, exact current dated-review bytes and frozen canonical application. Parent performed the live checks; this audit did not rerun historical validators, approve content or verify online deployment.',
    'online_publication_verified_by_this_audit': False,
}
output = BASE / 'post-review-application-verification.json'
assert not output.exists()
output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + '\n')
print(json.dumps({key: result[key] for key in ('canonical_ids', 'formal_records_applied', 'formal_applied_decisions',
                                             'final_bucket_partition', 'scope_comparisons_complete',
                                             'remaining_version_body_review')}, ensure_ascii=False, indent=2))
