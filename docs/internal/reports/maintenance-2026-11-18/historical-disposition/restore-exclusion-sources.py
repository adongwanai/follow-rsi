"""Restore primary evidence for ten exact-hash owner-approved scope exclusions."""
import concurrent.futures
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import requests
import fitz
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[5]
OUT = ROOT / 'docs/internal/reports/maintenance-2026-11-18/historical-disposition'
RAW = ROOT / 'data/feed/raw/maintenance-2026-11-18/historical-disposition'
targets = [
 ('arxiv:2610.22990','https://arxiv.org/html/2610.22990v1','html'),
 ('arxiv:2610.38728','https://arxiv.org/html/2610.38728v1','html'),
 ('arxiv:2610.34977','https://arxiv.org/html/2610.34977v1','html'),
 ('s2:c470d4b2c990d73e0b34f5f9e384423fd7c09a14','https://xplorestaging.ieee.org/ielx8/10207/11740818/11740826.pdf?arnumber=11740826','pdf'),
 ('s2:c9b9cd5e0b6447a180914049754459b00b3cf264','https://api.crossref.org/works/10.31234%2Fosf.io%2Fmeuyq_v2','preprint-json'),
 ('s2:c9b9cd5e0b6447a180914049754459b00b3cf264','https://api.crossref.org/works/10.1016%2Fj.cobeha.2026.101684','journal-json'),
 ('post:/us-midterms-analysis/','https://sakana.ai/us-midterms-analysis/','html'),
 ('post:https://openai.com/index/openai-servicenow-partnership-expansion','https://openai.com/index/openai-servicenow-partnership-expansion','html'),
 ('post:https://openai.com/index/the-future-of-the-firm','https://openai.com/index/the-future-of-the-firm','html'),
 ('post:https://openai.com/index/legora','https://openai.com/index/legora','html'),
 ('post:https://sakana.ai/symposium-2026/','https://sakana.ai/symposium-2026/','html'),
]
def now():
    return datetime.now(timezone.utc).isoformat()
def fetch(t):
    id,url,kind=t
    key=hashlib.sha256(url.encode()).hexdigest()[:16]
    receipt=OUT/f'exclusion-source-{key}.json'
    if receipt.exists():
        old=json.loads(receipt.read_text())
        if old['status']=='ok':
            assert hashlib.sha256((ROOT/old['source_file']).read_bytes()).hexdigest()==old['source_sha256']
            return old
    result={'id':id,'source_kind':kind,'url':url,'requested_at':now(),'paid_requests':0}
    path=RAW/f'exclusion-{key}.raw'
    try:
        r=requests.get(url,timeout=35,headers={'User-Agent':'follow-rsi-source-audit/1.0'})
        path.write_bytes(r.content)
        result.update(finished_at=now(),http_status=r.status_code,final_url=r.url,
          source_file=str(path.relative_to(ROOT)),source_sha256=hashlib.sha256(r.content).hexdigest(),
          bytes=len(r.content),content_type=r.headers.get('content-type'))
        if r.status_code!=200:
            result['status']='source_unavailable'
        else:
            if kind=='pdf':
                doc=fitz.open(stream=r.content,filetype='pdf')
                result['pages']=len(doc)
                text='\n'.join(page.get_text() for page in doc)
            elif kind.endswith('json'):
                message=r.json()['message']
                result.update(doi=message.get('DOI'),title=message.get('title'),
                  authors=message.get('author'),relation=message.get('relation'),
                  published=message.get('published'),posted=message.get('posted'))
                text=BeautifulSoup(message.get('abstract',''),'html.parser').get_text(' ',strip=True)
            else:
                soup=BeautifulSoup(r.content,'html.parser')
                title=soup.select_one('.ltx_title_document') or soup.find('h1') or soup.find('title')
                result['observed_title']=title.get_text(' ',strip=True) if title else None
                for n in soup(['script','style','nav']):n.decompose()
                text=(soup.find('article') or soup.find('main') or soup).get_text(' ',strip=True)
            textpath=RAW/f'exclusion-{key}.txt';textpath.write_text(text)
            result.update(status='ok',text_file=str(textpath.relative_to(ROOT)),
              text_sha256=hashlib.sha256(textpath.read_bytes()).hexdigest(),text_characters=len(text))
    except requests.RequestException as exc:
        result.update(status='network_error',finished_at=now(),error_type=type(exc).__name__,error=str(exc))
    receipt.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows=list(pool.map(fetch,targets))
    (OUT/'exclusion-source-index.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    for r in rows: print(r['id'],r['source_kind'],r['status'],r.get('http_status'),r.get('text_characters'))
