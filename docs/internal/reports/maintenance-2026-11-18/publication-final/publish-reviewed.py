"""One-time publication from exact, genuinely merged dated reviews; no paid calls."""
from pathlib import Path
from datetime import datetime, timezone
from copy import deepcopy
import base64
import gzip
import hashlib
import json
import os
import subprocess
import sys
import yaml

from scripts.feed.ci import merged_review_requests, human_owner_review
from scripts.feed.review import (validate_daily_review, validate_weekly_picks,
    apply_daily_review, source_hash, approved_weekly_backlog)
from scripts.feed.digest import (publish_day, publish_week, render_recap, initialize_public,
    _public_item)
from scripts.feed.storage import write_json, load_items, save_items

R = Path.cwd()
B = R / 'build/maintenance-2026-11-18'
D = R / 'docs/internal/reports/maintenance-2026-11-18'
OUT = D / 'publication-final'
REPO = 'adongwanai/follow-rsi'
ENV = {**os.environ, 'GODEBUG': 'http2client=0'}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def gh(endpoint):
    return json.loads(subprocess.check_output(['gh', 'api', endpoint], env=ENV, text=True))

def merged_bytes(path, commit):
    obj = gh(f'repos/{REPO}/contents/{path}?ref={commit}')
    if obj.get('content'):
        return base64.b64decode(obj['content'])
    return base64.b64decode(gh(f'repos/{REPO}/git/blobs/{obj["sha"]}')['content'])

def verify_pr(number, expected_head, expected_sha, expected_path):
    pr = gh(f'repos/{REPO}/pulls/{number}')
    assert pr['merged'] and pr['base']['ref'] == 'main'
    assert pr['head']['sha'] == expected_head and pr['head']['repo']['full_name'] == REPO
    pages = json.loads(subprocess.check_output(['gh', 'api', '--paginate', '--slurp',
        f'repos/{REPO}/pulls/{number}/files?per_page=100'], env=ENV, text=True))
    files = [row for page in pages for row in page]
    assert len(files) == pr['changed_files']
    requests = merged_review_requests({'pull_request': pr}, [row['filename'] for row in files], REPO)
    assert len(requests) == 1 and requests[0]['path'] == expected_path
    owner = human_owner_review(pr, gh(f'repos/{REPO}/pulls/{number}/reviews?per_page=100'), REPO)
    checks = gh(f'repos/{REPO}/commits/{expected_head}/check-runs?per_page=100')['check_runs']
    for name in ('build', 'validate'):
        matches = [row for row in checks if row['name'] == name]
        assert matches and max(matches, key=lambda row: row['id'])['conclusion'] == 'success', (number, name)
    statuses = gh(f'repos/{REPO}/commits/{expected_head}/status')['statuses']
    matches = [row for row in statuses if row['context'] == 'Follow RSI owner decisions']
    assert matches and max(matches, key=lambda row: row['id'])['state'] == 'success'
    content = merged_bytes(expected_path, pr['merge_commit_sha'])
    assert digest(content) == expected_sha, (number, 'review bytes differ')
    if number != 134:
        assert content == (R / expected_path).read_bytes()
    receipt = {'request': requests[0], 'github_pr': number, 'head': expected_head,
        'owner_login': owner, 'merge_commit': pr['merge_commit_sha'],
        'review_sha256': expected_sha, 'verified_at': datetime.now(timezone.utc).isoformat(),
        'authorization': 'Standing owner authorization; account merge is not a claim of manual per-paper reading.'}
    write_json(OUT / f'verified-review-{number}.json', receipt)
    return receipt, content

def provenance(receipt):
    return {key: receipt[key] for key in ('github_pr', 'owner_login', 'merge_commit')}

def apply_selected(receipt, content, selected):
    request = receipt['request']
    day, path = request['date'], R / request['path']
    restore = path.read_bytes()
    full = yaml.safe_load(content)
    subset = deepcopy(full)
    for group in ('items', 'lab_updates'):
        subset[group] = [row for row in full[group] if row['id'] in selected]
    assert {row['id'] for row in subset['items'] + subset['lab_updates']} == selected
    assert 'arxiv:2611.16378' not in selected
    before = {row['id']: deepcopy(row) for row in load_items(R)}
    histories = []
    for key in selected:
        old = before[key]
        if old.get('review'):
            row = deepcopy(old)
            history = row.setdefault('review_history', [])
            if old['review'] not in history:
                history.append(deepcopy(old['review']))
            histories.append(row)
    save_items(R, histories)
    try:
        path.write_text(yaml.safe_dump(subset, allow_unicode=True, sort_keys=False, width=110))
        count = apply_daily_review(R, day, now=STAMP, provenance=provenance(receipt))
    finally:
        path.write_bytes(restore)
    after = {row['id']: row for row in load_items(R)}
    assert all(after[key] == row for key, row in before.items() if key not in selected)
    assert all(after[key]['review']['source_hash'] == source_hash(after[key]) for key in selected)
    assert all(after[key]['first_seen'] == before[key]['first_seen'] for key in before)
    result = {**receipt, 'selected_ids': sorted(selected), 'applied_records': count,
        'source_scientific_fields_unchanged': all(source_hash(after[key]) == source_hash(row)
            for key, row in before.items()), 'history_saved_before_replacement': True}
    assert result['source_scientific_fields_unchanged']
    write_json(OUT / f'applied-review-{receipt["github_pr"]}.json', result)
    print(json.dumps({'applied_pr': receipt['github_pr'], 'selected': len(selected), 'changed': count}), flush=True)

assert len(sys.argv) == 2, 'Pass the final, locally prepared publication plan JSON.'
plan = json.loads(Path(sys.argv[1]).read_text())
OUT.mkdir(parents=True, exist_ok=True)
STAMP = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
assert not (R / 'site/daily/2026-11-16.json').exists(), 'First application only; inspect saved receipts before resuming.'
before = {row['id']: deepcopy(row) for row in load_items(R)}
protected_ege = deepcopy(before['arxiv:2611.16378']['review'])
prior_manifests = {str(path.relative_to(R)): digest(path.read_bytes())
    for kind in ('daily', 'weekly', 'recaps')
    for path in (R / 'site' / kind).glob('*.json')}
write_json(OUT / 'prior-manifests.json', prior_manifests)
write_json(OUT / 'prior-ege-review.json', protected_ege)
prior_sources = {key: {'source_hash': source_hash(row), 'first_seen': row['first_seen']}
    for key, row in before.items()}
write_json(OUT / 'prior-canonical-boundaries.json', prior_sources)
verified = {}
for entry in plan['reviews']:
    receipt, content = verify_pr(entry['number'], entry['head'], entry['sha256'], entry['path'])
    verified[entry['number']] = (receipt, content, entry)

for number in plan['apply_order']:
    receipt, content, entry = verified[number]
    apply_selected(receipt, content, set(entry['apply_ids']))

for day, number in plan['daily_review_prs'].items():
    receipt = verified[number][0]
    write_json(R / 'data/feed/review-provenance' / f'{day}.json',
        {**receipt['request'], **provenance(receipt)})

current = {row['id']: row for row in load_items(R)}
assert current['arxiv:2611.16378']['review'] == protected_ege
ege = deepcopy(current['arxiv:2611.16378'])
meta_receipt = {**provenance(verified[137][0]), 'kind': 'hf_recommendation_metadata',
    'date': '2026-11-16', 'reviewed_on': '2026-11-18', 'source_hash': source_hash(ege),
    'previous_approval_source_hash': protected_ege['source_hash'],
    'review_preserved': True, 'scientific_content_reapproved': False, 'republished': False,
    'note': 'Additional observed HF recommendation day only; original Nov 12 acceptance, review and publication are preserved.'}
ege.setdefault('metadata_review_receipts', []).append(meta_receipt)
save_items(R, [ege])
write_json(OUT / 'ege-metadata-only-receipt.json', meta_receipt)

snapshot = json.loads((R / 'data/feed/raw/maintenance-2026-11-18/source-intake/all-source-snapshot.json').read_text())
state_path = R / 'data/feed/state.json'
state = json.loads(state_path.read_text())
write_json(OUT / 'source-state-before.json', state)
public_sources, fetch_rows = {}, []
for source in snapshot['sources']:
    key = source['source_id']
    ok = source['status'] == 'ok'
    availability = ('not_ready' if key == 'hf-daily' else 'available' if ok
                    else 'partial' if source['status'] == 'partial' else 'failed')
    row = state['sources'][key]
    row.update(last_count=source['configured_window_records'], last_run=source['finished_at'], last_ok=ok,
        last_error=source['error'], availability=availability,
        degraded=source['status'] == 'partial')
    if ok:
        row.update(last_success=source['finished_at'], consecutive_errors=0, consecutive_failures=0)
    elif availability != 'not_ready':
        row['consecutive_errors'] = row.get('consecutive_errors', 0) + 1
        row['consecutive_failures'] = row.get('consecutive_failures', 0) + 1
    if key == 'hf-daily':
        row.update(today_board_status='not_ready', today_board_count=None,
            available_through='2026-11-17', boards={'2026-11-15': 0, '2026-11-16': 40, '2026-11-17': 41})
    public_sources[key] = {'count': row['last_count'], 'run_at': row['last_run'],
        'error': row['last_error'], 'availability': availability}
    fetch_rows.append({'source_id': key, 'ok': ok, 'count': row['last_count'],
        'availability': availability, 'error': row['last_error'], 'degraded': row['degraded'],
        'started_at': source['started_at'], 'finished_at': source['finished_at'],
        'request_count': source['request_count'], 'http_status_counts': source['http_status_counts'],
        'source_traversal_complete': source['source_traversal_complete']})
state['last_fetch'] = {'run_at': snapshot['generated_at'], 'sources': fetch_rows,
    'report': 'docs/internal/reports/maintenance-2026-11-18/source-intake/README.md',
    'snapshot': 'data/feed/raw/maintenance-2026-11-18/source-intake/all-source-snapshot.json'}
state['last_hf_supplement'] = {'observed_at': snapshot['generated_at'],
    'boards': {'2026-11-15': 0, '2026-11-16': 40, '2026-11-17': 41},
    'available_through': '2026-11-17',
    'reconciliation_report': 'docs/internal/reports/maintenance-2026-11-18/source-intake/hf-board-reconciliation.json'}
write_json(state_path, state)

status_path = R / 'data/feed/daily-status.json'
status = json.loads(status_path.read_text())
bulletins = json.loads((D / 'primary-review/status-bulletins-v2.json').read_text())
assert not any(row['date'] in {'2026-11-17', '2026-11-18'} for row in status['days'])
status['days'].extend(bulletins)
status['updated_at'] = STAMP
write_json(status_path, status)
generation = []
for day in ('2026-11-16', '2026-11-17', '2026-11-18'):
    result = publish_day(R, day, client=None, now=STAMP, allow_status=True)
    edition_path = R / 'site/daily' / f'{day}.json'
    edition = json.loads(edition_path.read_text())
    edition['sources'] = deepcopy(public_sources)
    edition['collection_observed_at'] = snapshot['generated_at']
    edition['collection_date_note'] = 'Sources were observed on Nov 18. Earlier edition dates retain their real HF recommendation or other-source windows; this is a delayed publication.'
    edition['review_provenance'] = {**verified[plan['daily_review_prs'][day]][0]['request'],
        **provenance(verified[plan['daily_review_prs'][day]][0])}
    if day == '2026-11-16':
        assert len(edition['items']) == 7
        edition['intro']['zh'] += ' 本期于11/18完成审核并补发：按11/16真实推荐日纳入2篇HF论文，另有5篇真实来源窗口论文；MIRIX是此前发现论文的首次正式出版。采集时间与实际审核日分别保留。'
        edition['intro']['en'] += ' Reviewed and published late on Nov 18: two papers belong to the actual Nov 16 HF recommendation list, and five come from the true other-source window. MIRIX was discovered earlier and is being published here for the first time. Collection and review dates remain explicit.'
    else:
        assert edition['kind'] == 'daily_status' and not edition['items']
    write_json(edition_path, edition)
    result['manifest'] = str(Path(result['manifest']).relative_to(R))
    generation.append(result)

weekly_receipt = verified[118][0]
validate_weekly_picks(R, '2026-W46')
write_json(R / 'data/feed/review-provenance/2026-W46.json',
    {**weekly_receipt['request'], **provenance(weekly_receipt)})
result = publish_week(R, '2026-W46', client=None, now=STAMP)
result['manifest'] = str(Path(result['manifest']).relative_to(R))
generation.append(result)
weekly_path = R / 'site/weekly/2026-W46.json'
weekly = json.loads(weekly_path.read_text())
weekly['review_provenance'] = {**weekly_receipt['request'], **provenance(weekly_receipt)}
for row in weekly.get('backlog', []):
    review = {item['id']: item for item in load_items(R)}[row['id']]['review']
    row['review_date'] = review.get('reviewed_on', review['date'])
write_json(weekly_path, weekly)

sources = {row['id']: row for row in load_items(R)}
repository = yaml.safe_load((R / 'data/papers.yaml').read_text())['papers']
backlog = approved_weekly_backlog(R, '2026-W47')
public = [{**_public_item(item, {'decision': 'backlog'}, '2026-W47', repository),
    'review_date': item['review'].get('reviewed_on', item['review']['date']),
    'window_status': 'backlog'} for item in backlog]
assert public and len({row['id'] for row in public}) == len(public)
edition = {'start': '2026-11-16', 'end': '2026-11-18', 'published_at': STAMP,
    'title_zh': '历史补录 · 11 月 16–18 日审核',
    'title_en': 'Historical additions reviewed November 16–18',
    'reviewed_only': True, 'items': public, 'lab_updates': [], 'picks': [],
    'sources': public_sources, 'reviewed_on': '2026-11-18',
    'review_provenance': [value[0] for value in verified.values() if value[0]['request']['kind'] == 'daily'],
    'intro': {'zh': f'本次逐项复核并补录 {len(public)} 篇较早论文。11月16–18日是审核归档区间，不是论文发表日；每篇保留原发表、版本和HF推荐日期。此回顾单列历史成果，不计作当天新增论文，也不是尚未结束的W47周刊。',
        'en': f'This retrospective adds {len(public)} previously published papers after item-specific review. November 16–18 is the review filing period, not the papers’ publication dates. Original publication, version and HF recommendation dates remain explicit. These historical additions are separate from daily new papers and are not a W47 weekly edition.',
        'source': 'source-bound-editorial-review'}}
result = render_recap(R, edition)
for key in ('manifest', 'html'):
    result[key] = str(Path(result[key]).relative_to(R))
generation.append(result)
initialize_public(R)

after = {row['id']: row for row in load_items(R)}
assert len(after) == len(before)
assert after['arxiv:2611.16378']['review'] == protected_ege
assert all(after[key]['first_seen'] == row['first_seen'] and source_hash(after[key]) == source_hash(row)
    for key, row in before.items())
for path, sha in prior_manifests.items():
    assert digest((R / path).read_bytes()) == sha, path
assert not (R / 'site/daily/2026-10-27.json').exists()
write_json(OUT / 'generation-receipt.json', {'generated_at': STAMP, 'generation': generation,
    'prior_manifests_byte_identical': True, 'canonical_count': len(after),
    'first_seen_and_scientific_source_hashes_unchanged': True,
    'ege_original_review_preserved_exactly': True, 'paid_generation_requests': 0,
    'paid_generation_tokens': 0, 'quality_warning': {'date': '2026-11-05',
        'complete': False, 'recall': 0.892857, 'threshold': 0.90},
    'online_verified': False, 'boundary': 'Local generation only; publication PR, Pages deployment and live verification remain required.'})
print(json.dumps(generation, ensure_ascii=False), flush=True)
