import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import requests
from pypdf import PdfReader

report = Path('docs/internal/reports/maintenance-2026-11-18/independent-other')
raw = Path('data/feed/raw/maintenance-2026-11-18/independent-other')
index_path = report / 'source-index.json'
original = index_path.read_bytes()
index = json.loads(original)
records = {r['id']: r for r in json.loads((report / 'input-records.json').read_text())['records']}
now = lambda: datetime.now(timezone.utc).isoformat()
sha = lambda b: hashlib.sha256(b).hexdigest()
changes = []

for item in index['items']:
    if item['id'] == 'arxiv:2611.18157':
        pdf_path = raw / '2611.18157v1.1.pdf'
        pdf = PdfReader(pdf_path)
        pages = [p.extract_text() or '' for p in pdf.pages]
        text = '\n\n'.join(f'## PDF page {i+1}\n{t}' for i, t in enumerate(pages))
        text_path = raw / '2611.18157v1.manual-extract.txt'
        text_path.write_text(text)
        r = records[item['id']]
        first = ' '.join(pages[0].split())
        title_match = ' '.join(r['title'].split()) in first
        author_matches = {a: a in first for a in r['authors']}
        assert title_match and all(author_matches.values())
        item.update(status='source_available', body_path=str(pdf_path), body_sha256=sha(pdf_path.read_bytes()),
                    text_path=str(text_path), text_sha256=sha(text.encode()), text_characters=len(text),
                    official_url='https://arxiv.org/pdf/2611.18157v1', document_title=r['title'],
                    version_identity_matches=None,
                    identity_binding={'method': 'official_version_url_and_arxiv_metadata_title_all_authors',
                        'title_matches': title_match, 'authors_match': author_matches,
                        'metadata_evidence': r['official_metadata_evidence'],
                        'pdf_watermark_present': False,
                        'limitation': 'PDF has no searchable arXiv version stamp; requested official v1 URL is retained; no claim of stamp match.'})
        changes.append({'id': item['id'], 'action': 'manual_pdf_identity_binding', 'observed_at': now(), 'page_count': len(pages)})
    elif item['id'].startswith('s2:'):
        url = item['requests'][0]['request_url']
        started = now()
        response = requests.get(url, timeout=25)
        path = raw / 's2-survey-retry.json'
        path.write_bytes(response.content)
        receipt = {'request_url':url, 'requested_at':started, 'finished_at':now(),
            'http_status':response.status_code, 'final_url':response.url,
            'content_type':response.headers.get('Content-Type'), 'bytes':len(response.content),
            'sha256':sha(response.content), 'path':str(path)}
        item['requests'].append(receipt)
        changes.append({'id':item['id'], 'action':'single_free_metadata_retry', 'receipt':receipt})
        if response.status_code == 200:
            (report/'s2-survey-metadata.json').write_text(json.dumps(response.json(),ensure_ascii=False,indent=2)+'\n')

index['counts'] = {'total':len(index['items']),
    'source_available':sum(x['status']=='source_available' for x in index['items']),
    'unavailable':sum(x['status']=='unavailable' for x in index['items']),
    'arxiv':sum(x['id'].startswith('arxiv:') for x in index['items'])}
index['supplemented_at'] = now()
index_path.write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
(report/'source-supplement-receipt.json').write_text(json.dumps({'original_index_sha256':sha(original),
    'changes':changes, 'result_index_sha256':sha(index_path.read_bytes()), 'paid_requests':0},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'counts':index['counts'], 'supplements':changes},ensure_ascii=False))
