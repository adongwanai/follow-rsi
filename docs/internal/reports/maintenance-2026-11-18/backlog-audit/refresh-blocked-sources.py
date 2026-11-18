"""One-time free retries of the thirteen recorded source blockers."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[5]
REPORT = ROOT / 'docs/internal/reports/maintenance-2026-11-18/backlog-audit'
RAW = ROOT / 'data/feed/raw/maintenance-2026-11-18/backlog-audit/blocker-retry-v1'
RAW.mkdir(parents=True, exist_ok=True)
OUT = REPORT / 'blocker-retry-v1.json'
assert not OUT.exists(), 'Preserve the existing source observation.'
prior = json.loads((ROOT / 'data/feed/raw/maintenance-2026-11-15/publication-final/backlog-audit/blocker-retry-assessments.json').read_text())
jobs = []
for row in prior['items']:
    jobs.extend((row['id'], n, item['url']) for n, item in enumerate(row['attempts']))
jobs += [
    ('s2:5bdd4b4a33f2207d918e44be0d2cbc4524093cf3', 0, 'https://dl.acm.org/doi/10.1145/3830454.3832577'),
    ('s2:5bdd4b4a33f2207d918e44be0d2cbc4524093cf3', 1, 'https://dl.acm.org/doi/pdf/10.1145/3830454.3832577'),
    ('s2:b26c48ea3f3148be53f71b66fceb48e38b235fd8', 0, 'https://dl.acm.org/doi/10.1145/3858063.3858878'),
    ('s2:b26c48ea3f3148be53f71b66fceb48e38b235fd8', 1, 'https://dl.acm.org/doi/pdf/10.1145/3858063.3858878'),
    ('s2:7872d98d7366afe3ac62a134eb74aa3efdf3018b', 0, 'https://ieeexplore.ieee.org/document/11673196/'),
    ('s2:7872d98d7366afe3ac62a134eb74aa3efdf3018b', 1, 'https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11673196'),
]


def fetch(job):
    ident, index, url = job
    record = {'id': ident, 'url': url, 'requested_at': datetime.now(timezone.utc).isoformat()}
    try:
        response = requests.get(url, headers={'User-Agent': 'follow-rsi-maintenance-source-audit/2026-11-18'}, timeout=30)
    except requests.RequestException as error:
        record.update(error_type=type(error).__name__, error=str(error), finished_at=datetime.now(timezone.utc).isoformat(), recovered_body=False)
        return record
    path = RAW / f'{ident.replace(":", "-")}-{index}.body'
    path.write_bytes(response.content)
    record.update(http_status=response.status_code, final_url=response.url, content_type=response.headers.get('Content-Type'), bytes=len(response.content), sha256=hashlib.sha256(response.content).hexdigest(), body_path=str(path.relative_to(ROOT)), finished_at=datetime.now(timezone.utc).isoformat(), recovered_body=False)
    if response.content.startswith(b'%PDF-'):
        record.update(recovered_body=True, observation='PDF bytes recovered; identity and scope review required before use')
    elif 'api.elsevier.com' in url and response.status_code == 200:
        root = ET.fromstring(response.content)
        content = [{'tag': node.tag.rsplit('}', 1)[-1], 'text': ' '.join(node.itertext()).strip()} for node in root.iter() if node.tag.rsplit('}', 1)[-1].lower() in {'abstract', 'description', 'body', 'originaltext'} and ' '.join(node.itertext()).strip()]
        record.update(content_sections=content, recovered_body=bool(content), observation='Nonempty abstract/body fields found; identity and scope review pending' if content else 'Only metadata; no nonempty abstract, description, body, or originalText')
    else:
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text(' ', strip=True)
        record.update(html_title=soup.title.get_text(' ', strip=True) if soup.title else None, text_excerpt=text[:600], observation='HTTP response is not PDF; inspect challenge/metadata boundary')
    return record


with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(fetch, jobs))
OUT.write_text(json.dumps({'observed_on': '2026-11-18', 'requests': results, 'request_count': len(results), 'paid_requests': 0, 'github_writes': 0}, ensure_ascii=False, indent=2) + '\n')
for row in results:
    print(json.dumps({k: row.get(k) for k in ['id', 'http_status', 'bytes', 'recovered_body', 'observation', 'html_title', 'error_type']}, ensure_ascii=False), flush=True)
