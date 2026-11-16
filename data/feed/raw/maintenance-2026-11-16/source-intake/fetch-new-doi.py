"""Fetch observed DOI identity and publisher sources, with original response receipts."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import requests

ROOT = Path.cwd()
WORK = ROOT / 'build/maintenance-2026-11-16/source-intake'
OUT = WORK / 'additional-official-sources'
OUT.mkdir(exist_ok=True)
IDENT = 's2:369a7a9f02b9aa1e3150b0747e8de9066625f060'
DOI = '10.1016/j.eswa.2026.135083'


def fetch(label, url):
    receipt_path = OUT / f'household-{label}.receipt.json'
    assert not receipt_path.exists(), 'Do not overwrite an earlier request receipt.'
    receipt = {'id': IDENT, 'doi': DOI, 'request_url': url,
               'requested_at': datetime.now(timezone.utc).isoformat()}
    try:
        response = requests.get(url, timeout=(10, 30),
                                headers={'User-Agent': 'FollowRSI/0.1 (source identity verification)'})
        body = OUT / f'household-{label}.body'
        body.write_bytes(response.content)
        receipt.update(http_status=response.status_code, final_url=response.url,
                       body_path=str(body.relative_to(ROOT)),
                       body_sha256=hashlib.sha256(response.content).hexdigest(),
                       bytes=len(response.content), content_type=response.headers.get('Content-Type'),
                       is_pdf=response.content.startswith(b'%PDF'))
        if response.status_code != 200:
            receipt['error'] = f'HTTP {response.status_code}'
    except requests.RequestException as error:
        receipt['error'] = f'{type(error).__name__}: {error}'
    receipt['finished_at'] = datetime.now(timezone.utc).isoformat()
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(receipt, ensure_ascii=False), flush=True)
    return receipt


crossref = fetch('crossref', 'https://api.crossref.org/works/' + DOI)
fetch('doi-landing', 'https://doi.org/' + DOI)
if crossref.get('http_status') == 200:
    metadata = json.loads((ROOT / crossref['body_path']).read_text())['message']
    assert metadata['DOI'].casefold() == DOI.casefold()
    for index, link in enumerate(metadata.get('link', [])):
        if link.get('content-type') in {'application/pdf', 'text/xml', 'text/plain'}:
            fetch(f'publisher-linked-{index + 1}', link['URL'])
