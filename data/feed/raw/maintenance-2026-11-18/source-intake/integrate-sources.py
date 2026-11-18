"""Apply the observed Nov 18 intake, retaining original responses and old decisions."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
from collections import Counter
import gzip
import hashlib
import json
import re
import shutil
import sys

R = Path.cwd()
sys.path.insert(0, str(R))
from scripts.feed.storage import load_items, save_items, write_json
from scripts.feed.review import source_hash

B = R / 'build/maintenance-2026-11-18'
W = B / 'source-intake'
A = R / 'data/feed/raw/maintenance-2026-11-18/source-intake'
D = R / 'docs/internal/reports/maintenance-2026-11-18/source-intake'
A.mkdir(parents=True, exist_ok=True)
D.mkdir(parents=True, exist_ok=True)
now = datetime.now(timezone.utc).isoformat()
sha = lambda b: hashlib.sha256(b).hexdigest()
rel = lambda p: str(p.relative_to(R))
proposal = json.loads((W / 'integration-proposal.json').read_text())
base = {x['id']: x for x in load_items(R)}
assert len(base) == proposal['canonical_baseline']['canonical_count'] == 2093
assert sha((R / 'data/feed/items.jsonl').read_bytes()) == proposal['canonical_baseline']['canonical_sha256']
assert not proposal['identity_collisions']

# Recover only the public candidate listing, never the surrounding session or credentials.
session = Path('/Users/mac/.codex/sessions/2026/10/27/rollout-2026-10-27T16-44-43-01a17c88-82d3-7902-8ed3-8acb1f13d18a.jsonl')
observations = {}
for line in session.open():
    if '2026-11-17T00:09:41.783Z' not in line[:100]:
        continue
    event = json.loads(line)
    if event['type'] != 'event_msg':
        continue
    output = event['payload']['item']['aggregated_output']
    for value in output.splitlines():
        match = re.match(r'((?:arxiv:|post:)[^ ]+) ([^ ]+) (.+)', value)
        if match:
            ident, reported_date, title = match.groups()
            observations[ident] = {'id': ident, 'observed_no_later_than': event['timestamp'],
                'reported_publication_date_in_old_output': reported_date, 'title_in_old_output': title,
                'source_event_id': event['payload']['item']['id'],
                'observation_kind': 'recovered_completed_command_output',
                'exact_original_http_time': 'unknown'}
assert len(observations) >= 50
write_json(D / 'recovered-nov17-observations.json', {
    'recovered_at': now, 'source_session_id': '01a17c88-82d3-7902-8ed3-8acb1f13d18a',
    'items': list(observations.values()),
    'boundary': 'Original uncommitted Nov 17 files are missing. This public-ID listing proves observation by this timestamp, not the exact lost HTTP observation time or completed scope review.'})

# Archive original network bytes losslessly; source hashes refer to decompressed bytes.
mapping, storage = {}, []
for path in sorted((W / 'network').rglob('*.body')):
    data = path.read_bytes()
    dest = A / path.relative_to(W)
    dest = dest.with_suffix(dest.suffix + '.gz')
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(gzip.compress(data, mtime=0))
    assert gzip.decompress(dest.read_bytes()) == data
    mapping[rel(path)] = rel(dest)
    storage.append({'original_path': rel(path), 'archive_path': rel(dest),
        'raw_sha256': sha(data), 'archive_sha256': sha(dest.read_bytes()),
        'compression': 'gzip', 'original_bytes': len(data), 'raw_bytes_unchanged': True})
for folder in ['official-metadata', 'source-results']:
    shutil.copytree(W / folder, A / folder, dirs_exist_ok=True)
for path in sorted((W / 'network').glob('*/attempts.jsonl')):
    dest = A / path.relative_to(W)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, dest)
for name in ['all-source-snapshot.json', 'all-source-snapshot.md', 'run-state.json',
             'auth-presence.json', 'fetch-free-sources.py', 'reconcile-sources.py']:
    shutil.copyfile(W / name, A / name)
write_json(D / 'response-storage-index.json', {'generated_at': now, 'responses': storage,
    'boundary': 'Original request receipts retain their collection paths. Resolve them through this index and decompress gzip before checking the original response SHA256.'})

issues = json.loads((B / 'open-issues.json').read_text())
issue_by_id = {}
for issue in issues:
    for ident in set(re.findall(r'arxiv\.org/(?:abs|html|pdf)/(\d{4}\.\d{4,5})', issue['body'])):
        issue_by_id['arxiv:' + ident] = issue
write_json(D / 'open-issues-at-start.json', issues)
metadata = {x['id']: x for x in json.loads((W / 'official-metadata/records.json').read_text())['records']}
meta_receipt = json.loads((W / 'official-metadata/receipt.json').read_text())
new = {x['id']: deepcopy(x) for x in proposal['new_items']}
extra = ['2611.18006', '2611.17790', '2611.13524', '2611.12288', '2611.13818', '2611.11273', '2611.15754']
for aid in extra:
    ident = 'arxiv:' + aid
    assert ident not in base and ident not in new
    issue = issue_by_id[ident]
    rec = deepcopy(metadata[ident])
    rec.update(kind='paper', hf_daily_dates=[], code_links=[], hf_upvotes=0,
        in_repo=False, aliases=[], seed_hits=[], author_tracked=False,
        retracted=False, source_hits=['github-issue'], first_seen=issue['createdAt'],
        source_observed_at=issue['createdAt'], first_seen_policy='repository_issue_created_at',
        announced=rec['published'][:10], announced_source='arxiv',
        official_metadata_verified=True, metadata_pending=False,
        official_metadata_record_id=ident, official_metadata_evidence=deepcopy(meta_receipt),
        intake_review_status='unreviewed_free_source_candidate')
    new[ident] = {'id': ident, 'record': rec, 'bindings': [
        {'request_url': issue['url'], 'observed_at': issue['createdAt'],
         'observation_kind': 'repository_issue_created_at', 'issue_number': issue['number']}],
        'formal_decision': 'not_yet_reviewed', 'paid_stages_run': False}

first_seen_changes = []
for ident, entry in new.items():
    rec = entry['record']
    assert ident not in base
    prior_seen = rec['first_seen']
    if ident in observations and observations[ident]['observed_no_later_than'] < rec['first_seen']:
        rec['first_seen'] = observations[ident]['observed_no_later_than']
        rec['first_seen_policy'] = 'earliest_recoverable_observation_upper_bound'
        rec['first_seen_evidence'] = rel(D / 'recovered-nov17-observations.json')
    if ident in issue_by_id and issue_by_id[ident]['createdAt'] < rec['first_seen']:
        rec['first_seen'] = issue_by_id[ident]['createdAt']
        rec['first_seen_policy'] = 'repository_issue_created_at'
        rec['first_seen_evidence'] = issue_by_id[ident]['url']
    if rec['first_seen'] != prior_seen:
        first_seen_changes.append({'id': ident, 'new_request_observed_at': prior_seen,
            'retained_earlier_observation': rec['first_seen'], 'policy': rec['first_seen_policy']})
    if not rec.get('arxiv_id'):
        rec.update(source_reported_updated=rec.get('updated'), updated='',
            updated_source='unknown', version_status='unknown', stored_version_placeholder=0)
        rec['published_source'] = 'official_publisher_rss' if rec['kind'] == 'post' else 'semantic_scholar'
        rec['official_metadata_verified'] = rec['kind'] == 'post'
        rec['metadata_pending'] = rec['kind'] == 'paper'
    evidence = rec.get('official_metadata_evidence')
    if evidence and evidence.get('body_path', '').startswith(rel(W)):
        evidence['body_path'] = evidence['body_path'].replace(rel(W), rel(A), 1)
        assert sha((R / evidence['body_path']).read_bytes()) == evidence['body_sha256']
    rec['source_discovery_evidence'] = {'request_bindings': entry['bindings'],
        'archived_network_response_index': rel(D / 'response-storage-index.json')}
    entry['source_hash'] = source_hash(rec)

updates, preservation = [], []
for entry in proposal['existing_provenance_updates']:
    old = base[entry['id']]
    assert old['first_seen'] == entry['existing_first_seen']
    updated = deepcopy(old)
    for field, values in entry['add_to_sets'].items():
        updated[field] = sorted(set(updated.get(field, [])) | set(values))
    delta = {field: {'before': old.get(field), 'after': updated.get(field)}
             for field in set(old) | set(updated) if old.get(field) != updated.get(field)}
    assert set(delta) <= {'source_hits', 'hf_daily_dates'}
    record = {'id': entry['id'], 'source_hash_before': source_hash(old),
        'source_hash_after': source_hash(updated), 'changed_fields': delta,
        'first_seen_preserved': True, 'scientific_fields_preserved': True,
        'old_review_preserved': old.get('review') == updated.get('review'),
        'original_review': deepcopy(old.get('review')), 'bindings': entry['bindings'],
        'boundary': 'Recommendation provenance only. Old exact-source approval is preserved, not forged as approval of the new hash; any new publication needs a new dated receipt.'}
    updated.setdefault('source_refresh_history', []).append(deepcopy(record))
    updates.append(updated)
    preservation.append(record)

count = save_items(R, [x['record'] for x in new.values()] + updates)
after = {x['id']: x for x in load_items(R)}
assert len(after) == len(base) + len(new) == 2222
changed_old = {x['id'] for x in updates}
assert all(after[k] == v for k, v in base.items() if k not in changed_old)
assert all(after[k]['first_seen'] == v['first_seen'] for k, v in base.items())
assert save_items(R, [x['record'] for x in new.values()] + updates) == 0
raw = [json.loads(x) for x in (W / 'raw-source-id-reconciliation.jsonl').read_text().splitlines()]
compact = [{**{k: x[k] for k in ['source_id', 'id', 'title', 'published_as_reported', 'disposition', 'evidence']},
    'canonical_present_after': x['id'] in after,
    'resolution': 'canonical_present' if x['id'] in after else x['disposition']} for x in raw]
assert all(x['canonical_present_after'] for x in compact if x['disposition'] == 'within_requested_source_window')
index_bytes = ''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in compact).encode()
(D / 'all-raw-id-ledger.jsonl.gz').write_bytes(gzip.compress(index_bytes, mtime=0))
hf = json.loads((W / 'source-results/hf-daily.json').read_text())
boards = {}
for path in sorted((W / 'network/hf-daily').glob('*.body')):
    body = json.loads(path.read_bytes())
    if not isinstance(body, list):
        continue
    attempts = [json.loads(x) for x in (path.parent / 'attempts.jsonl').read_text().splitlines()]
    attempt = next(x for x in attempts if x.get('body_path') == rel(path))
    day = attempt['params']['date']
    ids = ['arxiv:' + x['paper']['id'] for x in body]
    assert all(k in after and day in after[k].get('hf_daily_dates', []) for k in ids)
    boards[day] = {'count': len(ids), 'ids': ids, 'body_sha256': sha(path.read_bytes()),
        'archive_path': mapping[rel(path)], 'missing_canonical': [], 'missing_recommendation_day': []}
write_json(D / 'hf-board-reconciliation.json', {'generated_at': now, 'today': hf['hf_today'],
    'boards': boards, 'keyword_prefilter_used': False, 'source_only_not_publication': True})
write_json(A / 'effective-integration-proposal.json', {**proposal, 'new_items': list(new.values()),
    'applied': True, 'production_writes': count, 'extra_issue_candidates': ['arxiv:'+x for x in extra]})
write_json(D / 'integration-receipt.json', {'generated_at': now, 'before_count': len(base),
    'after_count': len(after), 'new_candidates': len(new), 'new_by_kind': dict(Counter(x['record']['kind'] for x in new.values())),
    'source_intake_new': len(proposal['new_items']), 'additional_issue_candidates': len(extra),
    'existing_updates': preservation, 'new_candidate_earlier_observations_restored': first_seen_changes,
    'all_existing_first_seen_preserved': True, 'unchanged_existing_records': len(base)-len(updates),
    'raw_occurrences': len(raw), 'raw_unique_ids': len({x['id'] for x in raw}),
    'all_window_ids_present': True, 'all_hf_members_and_dates_present': True,
    'canonical_after_sha256': sha((R/'data/feed/items.jsonl').read_bytes()),
    'second_apply_changed': 0, 'paid_generation_requests': 0,
    'scope_boundary': 'Source integration only. No new formal decisions or publication; exact old approvals retained.'})
shutil.copyfile(Path(__file__), A / Path(__file__).name)
print(json.dumps({'new_candidates': len(new), 'after_count': len(after), 'existing_updates': len(updates),
    'restored_nov17_observations': len(observations), 'first_seen_restored': len(first_seen_changes),
    'hf_counts': {k:v['count'] for k,v in boards.items()}, 'second_apply_changed': 0}, ensure_ascii=False))
