"""One-time, read-only external refresh for the backlog audit; no model calls."""
from datetime import datetime, timezone
import base64
import hashlib
import json
from pathlib import Path
import subprocess
import time
import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[5]
REPORT = ROOT / 'docs/internal/reports/maintenance-2026-11-18/backlog-audit'
RAW = ROOT / 'data/feed/raw/maintenance-2026-11-18/backlog-audit'
OUT = RAW / 'remote-refresh-v1'
OUT.mkdir(parents=True, exist_ok=True)
MANIFEST = REPORT / 'remote-refresh-v1.json'
assert not MANIFEST.exists(), 'Use a separately named refresh to preserve prior evidence.'
receipts = []
session = requests.Session()
session.headers['User-Agent'] = 'follow-rsi-maintenance-source-audit/2026-11-18'
github = requests.Session()
github.headers.update({'Authorization': 'Bearer ' + subprocess.check_output(['gh', 'auth', 'token'], text=True).strip(), 'Accept': 'application/vnd.github+json'})
last_arxiv = None


def now():
    return datetime.now(timezone.utc).isoformat()


def fetch(name, url, params=None):
    global last_arxiv
    if 'arxiv.org/' in url:
        if last_arxiv is not None:
            time.sleep(max(0, 3.25 - (time.monotonic() - last_arxiv)))
        last_arxiv = time.monotonic()
    receipt = {'name': name, 'url': url, 'params': params, 'requested_at': now()}
    try:
        response = (github if url.startswith('https://api.github.com/') else session).get(url, params=params, timeout=35)
        target = OUT / name
        target.write_bytes(response.content)
        receipt.update(http_status=response.status_code, final_url=response.url, body_path=str(target.relative_to(ROOT)), body_sha256=hashlib.sha256(response.content).hexdigest(), bytes=len(response.content), http_date=response.headers.get('Date'), link=response.headers.get('Link'), content_type=response.headers.get('Content-Type'))
        result = response
    except requests.RequestException as e:
        receipt.update(error_type=type(e).__name__, error=str(e))
        result = None
    receipt['finished_at'] = now()
    receipts.append(receipt)
    MANIFEST.write_text(json.dumps({'status': 'running', 'requests': receipts, 'paid_requests': 0}, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: receipt.get(k) for k in ['name', 'http_status', 'bytes', 'error_type']}, ensure_ascii=False), flush=True)
    return result


repo = 'https://api.github.com/repos/adongwanai/follow-rsi'
issues = []
page = 1
while True:
    response = fetch(f'open-issues-page-{page}.json', repo + '/issues', {'state': 'open', 'per_page': 100, 'page': page})
    assert response is not None and response.status_code == 200
    rows = response.json()
    issues.extend(r for r in rows if 'pull_request' not in r)
    if 'next' not in response.links:
        break
    page += 1
(OUT / 'open-issues.json').write_text(json.dumps(issues, ensure_ascii=False, indent=2) + '\n')
for issue in issues:
    if issue['number'] in {19, 20, 23, 30, 60, 115, 116} and issue['comments']:
        fetch(f'issue-{issue["number"]}-comments.json', repo + f'/issues/{issue["number"]}/comments', {'per_page': 100})

for number in [117, 134]:
    response = fetch(f'pr-{number}.json', repo + f'/pulls/{number}')
    assert response is not None and response.status_code == 200
    pr = response.json()
    files = []
    page = 1
    while True:
        file_response = fetch(f'pr-{number}-files-page-{page}.json', repo + f'/pulls/{number}/files', {'per_page': 100, 'page': page})
        assert file_response is not None and file_response.status_code == 200
        files.extend(file_response.json())
        if 'next' not in file_response.links:
            break
        page += 1
    for entry in files:
        path = entry['filename']
        selected = (number == 117 and 'version-candidates/' in path) or (number == 134 and path.startswith('review/daily/'))
        if selected:
            commit = pr['merge_commit_sha'] if pr.get('merged') else pr['head']['sha']
            fetch(f'pr-{number}--' + path.replace('/', '--'), f'https://raw.githubusercontent.com/adongwanai/follow-rsi/{commit}/{path}')

for name, repository in [('omnibrain', 'luo-yc17/OmniBrain-0'), ('molrsi', 'yikunpku/MolRSI')]:
    fetch(name + '-tree.json', f'https://api.github.com/repos/{repository}/git/trees/main', {'recursive': 1})
    response = fetch(name + '-readme.json', f'https://api.github.com/repos/{repository}/readme')
    if response is not None and response.status_code == 200:
        (OUT / (name + '-readme.md')).write_bytes(base64.b64decode(response.json()['content']))

fetch('karma-repository-search.json', 'https://api.github.com/search/repositories', {'q': '2610.39884 in:readme', 'per_page': 20})
fetch('vevo-repository-search.json', 'https://api.github.com/search/repositories', {'q': '2610.39158 in:readme', 'per_page': 20})

ids = ['2610.39884', '2610.39714', '2610.39158', '2610.36013', '2609.38372', '2609.34924']
response = fetch('official-six-metadata.atom', 'https://export.arxiv.org/api/query', {'id_list': ','.join(ids), 'max_results': 20})
if response is not None and response.status_code == 200:
    atom = ET.fromstring(response.content)
    ns = {'a': 'http://www.w3.org/2005/Atom'}
    metadata = []
    for entry in atom.findall('a:entry', ns):
        metadata.append({k: entry.findtext('a:' + k, namespaces=ns) for k in ['id', 'title', 'summary', 'published', 'updated']})
    (OUT / 'official-six-metadata.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n')

for aid in ids[:4]:
    fetch(aid + '-abs.html', f'https://arxiv.org/abs/{aid}')
    response = fetch(aid + '-current.html', f'https://arxiv.org/html/{aid}')
    if response is not None and response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        (OUT / (aid + '-current.txt')).write_text(soup.get_text(' ', strip=True))

for aid in ids[4:]:
    for version in [1, 2]:
        response = fetch(f'{aid}v{version}.html', f'https://arxiv.org/html/{aid}v{version}')
        if response is not None and response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            (OUT / f'{aid}v{version}.txt').write_text(soup.get_text(' ', strip=True))
        else:
            pdf = fetch(f'{aid}v{version}.pdf', f'https://arxiv.org/pdf/{aid}v{version}')
            if pdf is not None and pdf.status_code == 200:
                import fitz
                doc = fitz.open(stream=pdf.content, filetype='pdf')
                (OUT / f'{aid}v{version}.txt').write_text('\n'.join(p.get_text() for p in doc))

MANIFEST.write_text(json.dumps({'status': 'completed', 'finished_at': now(), 'requests': receipts, 'paid_requests': 0, 'github_writes': 0}, ensure_ascii=False, indent=2) + '\n')
