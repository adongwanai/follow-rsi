"""Read live publication and merged-review evidence for already processed issues."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

import requests
import yaml

ROOT = Path(__file__).resolve().parents[5]
REPORT = ROOT / 'docs/internal/reports/maintenance-2026-11-18/backlog-audit'
RAW = ROOT / 'data/feed/raw/maintenance-2026-11-18/backlog-audit/existing-issues-v1'
RAW.mkdir(parents=True, exist_ok=True)
OUT = REPORT / 'existing-issues-v1.json'
assert not OUT.exists()
baseline = {r['id']: r for r in map(json.loads, (ROOT / 'build/maintenance-2026-11-18/source-intake/canonical-baseline.jsonl').read_text().splitlines())}
issues = json.loads((ROOT / 'data/feed/raw/maintenance-2026-11-18/backlog-audit/remote-refresh-v1/open-issues.json').read_text())
records = []
for issue in issues:
    if 119 <= issue['number'] <= 133:
        aid = re.search(r'arxiv.org/abs/(\d+\.\d+)', issue['body']).group(1)
        ident = 'arxiv:' + aid
        records.append({'issue': issue['number'], 'id': ident, 'issue_url': issue['html_url'], 'existing_before_maintenance': ident in baseline, 'baseline_formal_review': baseline.get(ident, {}).get('review')})
session = requests.Session()
session.headers['User-Agent'] = 'follow-rsi-existing-issue-audit/2026-11-18'
gh = requests.Session()
gh.headers.update({'Authorization': 'Bearer ' + subprocess.check_output(['gh', 'auth', 'token'], text=True).strip(), 'Accept': 'application/vnd.github+json'})
receipts = []


def get(name, url):
    response = (gh if url.startswith('https://api.github.com/') else session).get(url, timeout=35)
    path = RAW / name
    path.write_bytes(response.content)
    receipts.append({'url': url, 'http_status': response.status_code, 'finished_at': datetime.now(timezone.utc).isoformat(), 'body_path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(response.content).hexdigest(), 'bytes': len(response.content)})
    response.raise_for_status()
    return response


for number in sorted({r['baseline_formal_review']['github_pr'] for r in records if r['baseline_formal_review']}):
    response = get(f'pr-{number}.json', f'https://api.github.com/repos/adongwanai/follow-rsi/pulls/{number}')
    pr = response.json()
    assert pr['merged'] and pr['merged_by']['login'] == 'adongwanai' and pr['base']['repo']['full_name'] == 'adongwanai/follow-rsi'
    dates = {r['baseline_formal_review']['date'] for r in records if (r['baseline_formal_review'] or {}).get('github_pr') == number}
    for day in dates:
        review_response = get(f'pr-{number}-{day}.yaml', f'https://raw.githubusercontent.com/adongwanai/follow-rsi/{pr["merge_commit_sha"]}/review/daily/{day}.yaml')
        review = yaml.safe_load(review_response.text)
        by_id = {r['id']: r for r in review['items'] + review.get('lab_updates', [])}
        for record in records:
            formal = record['baseline_formal_review']
            if formal and formal['github_pr'] == number and formal['date'] == day:
                original = by_id[record['id']]
                record['merged_original_review_matches'] = original['decision'] == formal['decision'] and original['source_hash'] == formal['source_hash'] and pr['merge_commit_sha'] == formal['merge_commit']
                record['merged_review_provenance'] = {'github_pr': number, 'owner_login': pr['merged_by']['login'], 'merge_commit': pr['merge_commit_sha'], 'head_sha': pr['head']['sha'], 'url': pr['html_url'], 'path': str((RAW / f'pr-{number}-{day}.yaml').relative_to(ROOT))}
                assert record['merged_original_review_matches']

page_json = get('2026-11-11.json', 'https://adongwanai.github.io/follow-rsi/daily/2026-11-11.json').json()
page_html = get('2026-11-11.html', 'https://adongwanai.github.io/follow-rsi/daily/2026-11-11.html').text
published_ids = {r['id'] for r in page_json['items']}
for record in records:
    formal = record['baseline_formal_review']
    if not formal:
        record.update(disposition='new_candidate_needs_current_three_round_review', publication_claim=False, recommend_close=False)
    elif formal['decision'] == 'reject':
        record.update(disposition='existing_merged_source_bound_exclusion', publication_claim=False, recommend_close=True, reason='Existing merged review already rejected the unchanged source; keep the exact receipt and avoid duplicate scope review.')
    elif formal['decision'] == 'backlog':
        record.update(disposition='existing_merged_backlog_not_publication', publication_claim=False, recommend_close=False, reason='A valid inclusion/backlog scope decision exists, but no dated publication is established. Preserve recommendation; publication task remains.')
    elif formal['decision'] == 'accept':
        verified = record['id'] in published_ids and record['id'].split(':', 1)[1] in page_html
        record.update(disposition='existing_publication_live_verified' if verified else 'accepted_publication_unverified', publication_claim=verified, recommend_close=verified, publication_url='https://adongwanai.github.io/follow-rsi/daily/2026-11-11.html')

OUT.write_text(json.dumps({'observed_at': datetime.now(timezone.utc).isoformat(), 'items': records, 'requests': receipts, 'paid_requests': 0, 'github_writes': 0, 'existing_canonical_count': sum(r['existing_before_maintenance'] for r in records)}, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'items': [{k: r.get(k) for k in ['issue', 'id', 'existing_before_maintenance', 'disposition', 'recommend_close']} for r in records]}, ensure_ascii=False, indent=2))
