"""Restore only the current-version bodies bound by the Nov 16 review."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, re, time
import yaml, requests, fitz
from bs4 import BeautifulSoup

ROOT=Path.cwd()
RAW=Path('data/feed/raw/maintenance-2026-11-18/independent-recovery')
OUT=Path('docs/internal/reports/maintenance-2026-11-18/independent-recovery')
REVIEW=Path('review/daily/2026-11-16.yaml')
expected='9c117cc76cfc2cb5e11ca17a47342e4611babe8dfc30e61381884d68cc60bd03'
sha=lambda content:hashlib.sha256(content).hexdigest()
stamp=lambda:datetime.now(timezone.utc).isoformat()
assert sha(REVIEW.read_bytes())==expected
review=yaml.safe_load(REVIEW.read_text())
rows=[r for r in review['items'] if r['id'].startswith('arxiv:')]
existing=[p for start in ('data/feed/raw','docs/internal/reports') for p in Path(start).rglob('*') if p.is_file() and any(r['arxiv_id'] in p.name for r in rows)]
result={'review_path':str(REVIEW),'review_sha256':expected,'started_at':stamp(),'paid_requests':0,'items':[],'requests':[]}
last=None

def save():
 (OUT/'source-recovery-index.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')

def inspect(path,row):
 content=path.read_bytes(); token=f"{row['arxiv_id']}v{row['version']}"
 rec={'path':str(path),'bytes':len(content),'sha256':sha(content),'matches_reviewed_body_sha256':sha(content)==row['source_review_evidence']['body_sha256']}
 if content.startswith(b'%PDF'):
  doc=fitz.open(stream=content,filetype='pdf'); text='\n'.join(p.get_text() for p in doc); first=doc[0].get_text(); doc.close()
  rec.update(kind='pdf',identity_token=token,identity_found=token in re.sub(r'\s+','',first),title_first_page=first[:300])
 else:
  soup=BeautifulSoup(content,'html.parser'); article=soup.find('article'); watermark=soup.find(id='watermark-tr')
  text=article.get_text('\n',strip=True) if article else ''
  rec.update(kind='html',identity_token=token,identity_found=bool(watermark and token in watermark.get_text(' ',strip=True)),title=soup.title.get_text(' ',strip=True) if soup.title else None)
 textpath=RAW/f"{token}.{rec['kind']}.txt"
 textpath.write_text(text)
 rec.update(text_path=str(textpath),text_sha256=sha(text.encode()),matches_reviewed_text_sha256=sha(text.encode())==row['source_review_evidence']['extracted_text_sha256'],text_characters=len(text))
 norm=lambda s:re.sub(r'\s+',' ',s).strip()
 checks=[]
 for q in row['source_review_evidence']['quotes']:
  node=soup.find(id=q['location'].removeprefix('#')) if rec['kind']=='html' and q['location'].startswith('#') else None
  node_text=node.get_text(' ',strip=True) if node else text
  checks.append({'location':q['location'],'quote':q['quote'],'found_in_selected_text':norm(q['quote']) in norm(node_text),'found_in_full_text':norm(q['quote']) in norm(text),'node_text':node_text[:7000] if node else None})
 rec['quote_checks']=checks
 return rec

for row in rows:
 rec={'id':row['id'],'version':row['version'],'decision':row['decision'],'expected_body_sha256':row['source_review_evidence']['body_sha256']}
 match=next((p for p in existing if row['arxiv_id'] in p.name and sha(p.read_bytes())==rec['expected_body_sha256']),None)
 if match:
  rec.update(method='reused_committed_exact_hash_body',source=inspect(match,row));result['items'].append(rec);save();continue
 urls=[row['source_review_evidence']['official_url']]
 if '/html/' in urls[0]:urls.append(urls[0].replace('/html/','/pdf/'))
 for n,url in enumerate(urls):
  if last is not None:time.sleep(max(0,3.2-(time.monotonic()-last)))
  request={'id':row['id'],'request_url':url,'requested_at':stamp()};last=time.monotonic()
  try:
   response=requests.get(url,timeout=(10,35),headers={'User-Agent':'FollowRSI/0.1 (current-version evidence recovery)'})
   ext='pdf' if response.content.startswith(b'%PDF') else 'html'
   path=RAW/f"{row['arxiv_id']}v{row['version']}.{n}.{ext}"
   path.write_bytes(response.content)
   request.update(http_status=response.status_code,final_url=response.url,content_type=response.headers.get('Content-Type'),bytes=len(response.content),path=str(path),sha256=sha(response.content))
   if response.status_code==200:
    source=inspect(path,row)
    if source['identity_found'] and source['text_characters']>1000:rec.update(method='official_versioned_refetch',source=source)
  except requests.RequestException as error:
   request.update(error_type=type(error).__name__,error=str(error))
  request['finished_at']=stamp();result['requests'].append(request);save()
  if rec.get('source'):break
 if not rec.get('source'):rec.update(method='unrecovered',blocker='No usable current-version full text recovered from the official version URL.')
 result['items'].append(rec);save()
 print(row['id'],rec['method'],rec.get('source',{}).get('matches_reviewed_body_sha256'),flush=True)
result['finished_at']=stamp();save()
print(json.dumps({'items':len(result['items']),'reused':sum(x['method'].startswith('reused') for x in result['items']),'requests':len(result['requests']),'unrecovered':[x['id'] for x in result['items'] if x['method']=='unrecovered']},ensure_ascii=False))
