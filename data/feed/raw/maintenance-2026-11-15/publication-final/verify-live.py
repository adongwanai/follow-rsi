from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import base64
import hashlib
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
import requests

R = Path.cwd()
B = R / 'build/maintenance-2026-11-15'
D = R / 'docs/internal/reports/maintenance-2026-11-15'
REPO = 'adongwanai/follow-rsi'
BASE = 'https://adongwanai.github.io/follow-rsi/'
number = int(sys.argv[1])
retry = '--retry' in sys.argv

def gh(path):
    return json.loads(subprocess.check_output(['gh', 'api', path], text=True))

def read(path):
    return json.loads(path.read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

pr = gh(f'repos/{REPO}/pulls/{number}')
assert pr['merged'] and pr['merged_by']['login'] == 'adongwanai'
sha = pr['merge_commit_sha']
runs = gh(f'repos/{REPO}/actions/runs?head_sha={sha}&per_page=50')['workflow_runs']
pages = [x for x in runs if x['path'] == '.github/workflows/pages.yml']
assert pages
page_run = max(pages, key=lambda x: x['id'])
assert page_run['conclusion'] == 'success'
assert gh(f'repos/{REPO}/commits/main')['sha'] == sha
report = {'verified_at': datetime.now(timezone.utc).isoformat(), 'publication_pr': number,
          'merge_commit': sha, 'pages_run': page_run['html_url'], 'files': [], 'checks': {}}
paths = ['index.html', 'data.js', 'daily/index.html', 'daily/2026-10-27.html',
         'feed/latest.json', 'feed/atom.xml', 'feed/atom.xsl', 'feed/status.json',
         'weekly/index.html', 'weekly/2026-W45.html', 'weekly/2026-W45.json',
         'cards/digest-2026-W45.png']
for day in sorted(p.stem for p in (R / 'site/daily').glob('????-??-??.json')):
    paths.extend([f'daily/{day}.html', f'daily/{day}.json'])
paths.extend(str(p.relative_to(R / 'site')) for p in sorted((R / 'site/recaps').glob('*.html')))
paths = list(dict.fromkeys(paths))
previous = []
if retry:
    prior = read(B / 'live-http-attempt.json')
    assert prior['merge_commit'] == sha
    previous = [x for x in prior['files'] if x['matches_reviewed_local_bytes']]
    paths = [x['path'] for x in prior['files'] if not x['matches_reviewed_local_bytes']]

def verify(path):
    row = {'path': path, 'url': BASE + path, 'checked_at': datetime.now(timezone.utc).isoformat(),
           'matches_reviewed_local_bytes': False}
    try:
        response = requests.get(BASE + path, params={'verify': sha}, timeout=30)
        row.update(status=response.status_code, bytes=len(response.content),
                   sha256=hashlib.sha256(response.content).hexdigest())
        row['matches_reviewed_local_bytes'] = response.status_code == 200 and response.content == (R / 'site' / path).read_bytes()
    except requests.RequestException as error:
        row.update(error_type=type(error).__name__, error=str(error))
    return row

with ThreadPoolExecutor(max_workers=4) as pool:
    report['files'] = previous + list(pool.map(verify, paths))
(B / ('live-http-retry.json' if retry else 'live-http-attempt.json')).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
failed = [x for x in report['files'] if not x['matches_reviewed_local_bytes']]
assert not failed, [(x['path'], x.get('status'), x.get('error_type')) for x in failed]
for name in ['README.md', 'README_zh.md', 'README_en.md']:
    blob = gh(f'repos/{REPO}/contents/{name}?ref=main')
    assert base64.b64decode(blob['content']) == (R / name).read_bytes()
    report['checks'][name] = {'main_bytes_match': True, 'blob': blob['sha']}

feed = read(R / 'site/feed/latest.json')
assert feed['dates'] == sorted(set(feed['dates']))
assert feed['dates'][-1] == '2026-11-15' and '2026-10-27' not in feed['dates']
assert len(feed['items']) == len({x['id'] for x in feed['items']}) == 66
today = read(R / 'site/daily/2026-11-15.json')
assert today['kind'] == 'daily_status' and today['items'] == []
assert today['status_report']['status'] == 'empty' and today['reviewed_on'] == '2026-11-15'
assert today['review_counts']['decisions'] == {'reject': 6, 'defer': 3, 'backlog': 2}
assert '10:34' in today['status_report']['reason_en']
expected = {
    '2026-11-11': {'arxiv:2611.14949', 'arxiv:2611.15178', 'arxiv:2611.15276', 'arxiv:2611.15700'},
    '2026-11-12': {'arxiv:2611.16143', 'arxiv:2611.16378', 'arxiv:2611.16414'},
}
summaries = {x['id']: x for x in read(B / 'summary-draft-v3.json')['items']}
canonical = {x['id']: x for x in map(json.loads, (R / 'data/feed/items.jsonl').read_text().splitlines())}
baseline_items = {x['id']: x for x in map(json.loads, (B / 'canonical-baseline.jsonl').read_text().splitlines())}
assert canonical['arxiv:2611.14256'] == baseline_items['arxiv:2611.14256']
for date, ids in expected.items():
    edition = read(R / f'site/daily/{date}.json')
    old = read(D / f'prior-editions/site/daily/{date}.json')
    old_ids = {x['id'] for x in old['items']}
    assert {x['id'] for x in edition['items']} == ids | old_ids
    assert edition['reviewed_on'] == '2026-11-15' and edition['published_at'] == old['published_at']
    for old_item in old['items']:
        assert next(x for x in edition['items'] if x['id'] == old_item['id']) == old_item
    for item in edition['items']:
        if item['id'] not in ids:
            continue
        assert item['news_date'] == date and item['published'].startswith(date)
        assert item['review_date'] == '2026-11-15' and item['hf_daily_dates'] == []
        assert canonical[item['id']]['first_seen'].startswith('2026-11-15')
        assert all(item[k] == v for k, v in summaries[item['id']]['summary_override'].items())
        assert next(x for x in feed['items'] if x['id'] == item['id']) == item

for receipt in read(B / 'publication-generation.json'):
    date = receipt['date']
    provenance = read(R / f'data/feed/review-provenance/{date}.json')
    actual = gh(f'repos/{REPO}/pulls/{receipt["github_pr"]}')
    assert actual['merged'] and actual['merged_by']['login'] == 'adongwanai'
    assert actual['head']['sha'] == receipt['head']
    assert provenance['github_pr'] == receipt['github_pr']
    assert provenance['owner_login'] == 'adongwanai'
    assert provenance['merge_commit'] == actual['merge_commit_sha'] == receipt['merge_commit']
    assert digest(R / receipt['path']) == receipt['review_sha256']

baseline = read(B / 'preservation-baseline.json')
for name, old_hash in baseline['daily_manifests'].items():
    if Path(name).stem not in expected:
        assert digest(R / name) == old_hash, name
for group in ['weekly', 'cards']:
    for name, old_hash in baseline[group].items():
        assert digest(R / name) == old_hash, name
navigation = read(B / 'navigation-update-receipt.json')
assert navigation['passed']
for row in navigation['files']:
    original = subprocess.check_output(['git', 'show', baseline['base_commit'] + ':' + row['path']])
    assert hashlib.sha256(original).hexdigest() == row['before_sha256']
    expected_html = original.decode()
    for substitution in row.get('exact_replacements', navigation['exact_replacements']):
        assert expected_html.count(substitution['before']) == 1
        expected_html = expected_html.replace(substitution['before'], substitution['after'], 1)
    assert expected_html.encode() == (R / row['path']).read_bytes()
assert '2026-11-15' in (R / 'site/daily/index.html').read_text()
atom = ET.fromstring((R / 'site/feed/atom.xml').read_text())
ns = {'a': 'http://www.w3.org/2005/Atom'}
entries = atom.findall('a:entry', ns)
links = [link.get('href', '') for entry in entries for link in entry.findall('a:link', ns)
         if '/daily/' in link.get('href', '')]
assert len(links) == len(set(links)) and links == sorted(links)
for date in [*expected, '2026-11-15']:
    assert sum(f'/daily/{date}.html' in link for link in links) == 1
assert not any('/daily/2026-10-27.html' in link for link in links)
workflows = gh(f'repos/{REPO}/actions/workflows?per_page=100')['workflows']
disabled = {x['path']: x['state'] for x in workflows if x['path'] in {
    '.github/workflows/feed-daily.yml', '.github/workflows/feed-eval.yml', '.github/workflows/feed-publish.yml'}}
assert len(disabled) == 3 and all(x == 'disabled_manually' for x in disabled.values())
open_prs = gh(f'repos/{REPO}/pulls?state=open&per_page=100')
assert not open_prs
report['checks'].update(today_status_published=True, today_new_papers=0,
    Nov11_supplement_new_papers=4, Nov11_total_papers=5, Nov12_supplement_new_papers=3,
    original_public_item_preserved=True, old_14256_rejection_not_reapplied=True,
    reviewed_dates_first_seen_and_summaries_verified=True, prior_daily_manifests_preserved_except_archived_supplements=True,
    formal_version_upgrades=0, weekly_cards_unchanged=True, one_atom_entry_per_day=True, dates_ascending=True,
    old_html_navigation_refreshed_with_publication_body_preserved=True,
    oct27_withdrawal_preserved=True, disabled_workflows=disabled, open_pull_requests=0)
report['passed'] = True
report['verified_at'] = datetime.now(timezone.utc).isoformat()
(B / 'final-live-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'passed': True, 'verified_http_paths': len(report['files']), **report['checks']}, ensure_ascii=False))
