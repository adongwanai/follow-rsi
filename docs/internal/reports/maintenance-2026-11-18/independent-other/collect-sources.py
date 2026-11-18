"""Record free official source responses for this bounded independent review."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import sys
import requests
from bs4 import BeautifulSoup
import fitz

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
from scripts.feed.fetch_arxiv import parse_atom

OUT = ROOT / 'docs/internal/reports/maintenance-2026-11-18/independent-other'
RAW = ROOT / 'data/feed/raw/maintenance-2026-11-18/independent-other'
INTAKE = ROOT / 'build/maintenance-2026-11-18/source-intake'
OUT.mkdir(parents=True, exist_ok=True)
RAW.mkdir(parents=True, exist_ok=True)
now = lambda: datetime.now(timezone.utc).isoformat()
sha = lambda data: hashlib.sha256(data).hexdigest()
rel = lambda path: str(path.relative_to(ROOT))
headers = {'User-Agent': 'FollowRSI independent source audit; public research metadata'}

def get(url, path, params=None):
    record = {'request_url': url, 'params': params, 'requested_at': now()}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=40)
        path.write_bytes(response.content)
        record.update(http_status=response.status_code, final_url=response.url,
            content_type=response.headers.get('Content-Type'), bytes=len(response.content),
            sha256=sha(response.content), path=rel(path), finished_at=now())
        return record, response
    except requests.RequestException as error:
        record.update(error=f'{type(error).__name__}: {error}', finished_at=now())
        return record, None

proposal = json.loads((INTAKE / 'integration-proposal.json').read_text())
candidates = [x['record'] for x in proposal['new_items']]
candidates = [x for x in candidates if not x.get('hf_daily_dates')
              and not any(s.startswith('hf') for s in x.get('source_hits', []))]
assert len(candidates) == 44
assert sum(x['kind'] == 'paper' for x in candidates) == 25
inputs = {}
for path in [INTAKE/'integration-proposal.json', INTAKE/'official-metadata/records.json',
             INTAKE/'official-metadata/extra/records.json', INTAKE.parent/'open-issues.json']:
    inputs[rel(path)] = sha(path.read_bytes())

extra_ids = ['2611.18006','2611.17790','2611.13524','2611.12288','2611.13818','2611.11273','2611.15754']
request_path = RAW / 'issue-extra-metadata.atom'
metadata_receipt, response = get('https://export.arxiv.org/api/query', request_path,
    {'id_list': ','.join(extra_ids), 'max_results': len(extra_ids)})
assert response is not None and response.status_code == 200, metadata_receipt
extra = parse_atom(response.text, source_id='independent-issue-metadata', now=now())
assert {row['arxiv_id'] for row in extra} == set(extra_ids)
for row in extra:
    row['metadata_evidence'] = metadata_receipt
    row['review_group'] = 'existing_open_issue'
for row in candidates:
    row['review_group'] = 'new_non_hf_intake'
rows = candidates + extra
(OUT / 'input-records.json').write_text(json.dumps({'inputs': inputs, 'records': rows}, ensure_ascii=False, indent=2)+'\n')
(OUT / 'extra-metadata-receipt.json').write_text(json.dumps(metadata_receipt, ensure_ascii=False, indent=2)+'\n')

def collect(row):
    key = row['id']
    slug = row.get('arxiv_id') or sha(key.encode())[:16]
    checkpoint = OUT / f'source-{slug}.json'
    if checkpoint.exists():
        return json.loads(checkpoint.read_text())
    result = {'id': key, 'title': row['title'], 'group': row['review_group'], 'version': row['version'],
              'requested_at': now(), 'requests': [], 'status': 'unavailable'}
    if row.get('arxiv_id'):
        token = f"{row['arxiv_id']}v{row['version']}"
        urls = [f'https://arxiv.org/html/{token}', f'https://arxiv.org/pdf/{token}']
    elif row['kind'] == 'post':
        urls = [row['links']['url']]
    else:
        urls = [f"https://api.semanticscholar.org/graph/v1/paper/{key.split(':',1)[1]}?fields=title,authors,externalIds,openAccessPdf,abstract,publicationDate,url"]
    for number, url in enumerate(urls):
        ext = 'pdf' if '/pdf/' in url else 'json' if 'api.semanticscholar.org' in url else 'html'
        path = RAW / f'{slug}v{row["version"]}.{number}.{ext}'
        receipt, response = get(url, path)
        result['requests'].append(receipt)
        if response is None or response.status_code != 200:
            continue
        if ext == 'pdf':
            if not response.content.startswith(b'%PDF'):
                result['requests'][-1]['parse_error'] = 'Expected PDF signature absent'
                continue
            document = fitz.open(stream=response.content, filetype='pdf')
            text = '\n'.join(page.get_text() for page in document)
            title = text[:500]
        elif ext == 'json':
            value = response.json()
            text = json.dumps(value, ensure_ascii=False, indent=2)
            title = value.get('title')
            result['metadata'] = value
        else:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.get_text(' ', strip=True) if soup.title else None
            if row.get('arxiv_id'):
                text = soup.get_text(' ', strip=True)
            else:
                node = soup.find('article') or soup.find('main') or soup
                for child in node.find_all(['script', 'style', 'nav', 'footer']):
                    child.decompose()
                text = node.get_text(' ', strip=True)
        identity = not row.get('arxiv_id') or token in text
        if row.get('arxiv_id') and not identity:
            result['requests'][-1]['parse_error'] = f'Version identity {token} absent'
            continue
        text_path = path.with_suffix(path.suffix+'.txt')
        text_path.write_text(text)
        result.update(status='metadata_only' if ext=='json' else 'source_available',
            body_path=rel(path), body_sha256=sha(response.content), text_path=rel(text_path),
            text_sha256=sha(text.encode()), text_characters=len(text),
            document_title=title, version_identity_matches=identity,
            official_url=url, finished_at=now())
        break
    checkpoint.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    return result

results=[]
with ThreadPoolExecutor(max_workers=3) as pool:
    futures = [pool.submit(collect, row) for row in rows]
    for future in as_completed(futures):
        result=future.result(); results.append(result)
        print(json.dumps({'id':result['id'],'status':result['status'],'version':result['version']}),flush=True)
index={'generated_at':now(),'input_hashes':inputs,'items':sorted(results,key=lambda x:x['id']),
       'counts':{'all':len(results),'source_available':sum(r['status']=='source_available' for r in results),
                 'metadata_only':sum(r['status']=='metadata_only' for r in results),
                 'unavailable':sum(r['status']=='unavailable' for r in results)},
       'paid_requests':0,'canonical_writes':0,'scope_recommendations_frozen':False}
(OUT/'source-index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(index['counts']),flush=True)
