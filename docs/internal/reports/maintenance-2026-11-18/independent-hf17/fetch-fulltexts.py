"""Free, explicit-version source retrieval for independent November 17 scope review."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import time
import requests
from bs4 import BeautifulSoup

ROOT = Path.cwd()
OUT = ROOT / 'data/feed/raw/maintenance-2026-11-18/independent-hf17'
REPORT = ROOT / 'docs/internal/reports/maintenance-2026-11-18/independent-hf17'
OUT.mkdir(parents=True, exist_ok=True)
metadata_path = ROOT / 'build/maintenance-2026-11-18/source-intake/official-metadata/records.json'
metadata = {x['arxiv_id']: x for x in json.loads(metadata_path.read_text())['records']}
selected = ['2611.07222','2611.20218','2611.20882','2611.14960','2611.19537',
            '2611.17610','2611.20595','2605.09614','2611.11657','2611.16694','2611.21072']
receipts = []
def now():
    return datetime.now(timezone.utc).isoformat()
def sha(data):
    return hashlib.sha256(data).hexdigest()

for aid in selected:
    source = metadata[aid]
    version = source['version']
    url = f'https://arxiv.org/html/{aid}v{version}'
    receipt_path = REPORT / f'{aid}-retrieval.json'
    if receipt_path.exists():
        receipts.append(json.loads(receipt_path.read_text()))
        continue
    receipt = {'id': 'arxiv:' + aid, 'version': version, 'metadata': source,
               'metadata_file_sha256': sha(metadata_path.read_bytes()), 'requests': []}
    for kind, endpoint in [('html',url), ('pdf',f'https://arxiv.org/pdf/{aid}v{version}')]:
        attempt = {'url': endpoint, 'requested_at': now()}
        try:
            response = requests.get(endpoint, timeout=45, headers={'User-Agent':'FollowRSI/0.1 (source-bound independent review)'})
            attempt.update(status=response.status_code, final_url=response.url,
                           content_type=response.headers.get('Content-Type'), finished_at=now())
            body = OUT / f'{aid}v{version}.{kind}'
            body.write_bytes(response.content)
            attempt.update(body_path=body.relative_to(ROOT).as_posix(),body_sha256=sha(response.content),bytes=len(response.content))
            if response.status_code == 200:
                text_path = OUT / f'{aid}v{version}.{kind}.txt'
                if kind == 'html':
                    soup = BeautifulSoup(response.content,'html.parser')
                    for tag in soup(['script','style']):
                        tag.decompose()
                    text = soup.get_text(' ',strip=True)
                else:
                    from pypdf import PdfReader
                    text = '\n\n'.join(page.extract_text() for page in PdfReader(body).pages)
                text_path.write_text(text)
                attempt.update(text_path=text_path.relative_to(ROOT).as_posix(),text_sha256=sha(text_path.read_bytes()))
                receipt.update(body_path=attempt['body_path'],body_sha256=attempt['body_sha256'],text_path=attempt['text_path'],text_sha256=attempt['text_sha256'])
        except requests.RequestException as exc:
            attempt.update(error_type=type(exc).__name__,finished_at=now())
        receipt['requests'].append(attempt)
        if 'text_path' in receipt:
            break
        time.sleep(3.1)
    receipt_path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    receipts.append(receipt)
    print(aid,version,receipt.get('body_sha256'),flush=True)
    time.sleep(3.1)
(REPORT/'source-index.json').write_text(json.dumps({'created_at':now(),'paid_requests':0,'records':receipts},ensure_ascii=False,indent=2)+'\n')
