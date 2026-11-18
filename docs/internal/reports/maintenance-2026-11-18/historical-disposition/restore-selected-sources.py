"""Restore only source bodies needed for actionable PR135 historical decisions.

No paid calls, canonical edits, or Git mutations. Existing frozen reviews stay intact.
"""
import concurrent.futures
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[5]
OUT = ROOT / 'docs/internal/reports/maintenance-2026-11-18/historical-disposition'
RAW = ROOT / 'data/feed/raw/maintenance-2026-11-18/historical-disposition'
RAW.mkdir(parents=True, exist_ok=True)
with gzip.open(ROOT / 'data/feed/raw/maintenance-2026-11-18/backlog-audit/pr135-historical-inventory-v1.jsonl.gz', 'rt') as f:
    inventory = [json.loads(line) for line in f]

first_group = {
    'arxiv:2610.37905', 'arxiv:2610.38392', 'arxiv:2610.39122',
    'arxiv:2610.39358', 'arxiv:2610.39508',
}
selected = [r for r in inventory if r['id'] in first_group or (
    r['scope_recommendation'] == 'include'
    and r['canonical_snapshot'].get('summary_en')
    and r['id'] != 'arxiv:2610.32253'
)]

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def restore(row):
    item = row['canonical_snapshot']
    aid = item['arxiv_id']
    version = str(item.get('version') or 1).removeprefix('v')
    url = f'https://arxiv.org/html/{aid}v{version}'
    path = RAW / f'{aid}v{version}.html'
    receipt_path = OUT / f'restored-{aid}.json'
    if receipt_path.exists():
        old = json.loads(receipt_path.read_text())
        if old.get('status') == 'ok' and path.exists():
            assert hashlib.sha256(path.read_bytes()).hexdigest() == old['source_sha256']
            return old
    result = {'id': row['id'], 'title': row['title'], 'url': url,
              'canonical_source_hash': row['canonical_source_hash'],
              'requested_at': now(), 'paid_requests': 0,
              'reason': 'Restore missing official body for selected actionable historical scope/summary checks; not a full-history refetch.'}
    try:
        response = requests.get(url, timeout=35, headers={'User-Agent': 'follow-rsi-source-audit/1.0'})
        result.update(finished_at=now(), http_status=response.status_code,
                      final_url=response.url, content_type=response.headers.get('content-type'))
        path.write_bytes(response.content)
        result.update(source_file=str(path.relative_to(ROOT)),
                      source_sha256=hashlib.sha256(response.content).hexdigest(), bytes=len(response.content))
        if response.status_code == 200 and 'html' in response.headers.get('content-type', '').lower():
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.select_one('.ltx_title_document') or soup.find('h1') or soup.find('title')
            result['observed_title'] = title.get_text(' ', strip=True) if title else None
            for node in soup(['script', 'style', 'nav']):
                node.decompose()
            body = soup.find('article') or soup.find('main') or soup
            text = body.get_text(' ', strip=True)
            txt = RAW / f'{aid}v{version}.txt'
            txt.write_text(text, encoding='utf-8')
            result.update(status='ok', text_file=str(txt.relative_to(ROOT)),
                          text_sha256=hashlib.sha256(txt.read_bytes()).hexdigest(), text_characters=len(text))
        else:
            result['status'] = 'source_unavailable'
    except requests.RequestException as exc:
        result.update(status='network_error', finished_at=now(), error_type=type(exc).__name__, error=str(exc))
    receipt_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    return result

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(restore, selected))
    (OUT / 'restored-source-index.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    for r in results:
        print(r['id'], r['status'], r.get('http_status'), r.get('text_characters'))
