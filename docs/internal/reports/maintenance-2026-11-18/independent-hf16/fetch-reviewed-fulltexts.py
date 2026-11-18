"""Independent, free, version-bound source inspection for the observed HF Nov 16 board."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,re,time
import requests,fitz
from bs4 import BeautifulSoup
R=Path.cwd(); OUT=Path('docs/internal/reports/maintenance-2026-11-18/independent-hf16'); RAW=Path('data/feed/raw/maintenance-2026-11-18/independent-hf16')
meta=Path('build/maintenance-2026-11-18/source-intake/official-metadata/records.json')
records={x['arxiv_id']:x for x in json.loads(meta.read_text())['records']}
ids=['2611.14505','2611.17814','2611.18338','2611.17820','2611.17440','2611.06866','2611.17955','2611.18359','2611.15789','2611.18442','2611.18130','2611.16661','2611.14487']
sha=lambda b:hashlib.sha256(b).hexdigest(); stamp=lambda:datetime.now(timezone.utc).isoformat()
result={'stage':'independent_source_collection','started_at':stamp(),'metadata_path':str(meta),'metadata_sha256':sha(meta.read_bytes()),'paid_requests':0,'items':[],'requests':[]}
def save():(OUT/'fulltext-index.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
last=None
for aid in ids:
 m=records[aid];v=m['version'];token=f'{aid}v{v}'
 rec={'id':'arxiv:'+aid,'arxiv_id':aid,'version':v,'title':m['title'],'published':m['published'],'updated':m['updated'],'official_metadata':m}
 for ext in ['html','pdf']:
  if last is not None:time.sleep(max(0,3.2-(time.monotonic()-last)))
  url=f'https://arxiv.org/{ext}/{token}';req={'requested_at':stamp(),'url':url};last=time.monotonic()
  try:
   resp=requests.get(url,headers={'User-Agent':'FollowRSI/0.1 (source-bound research review)'},timeout=(10,40));p=RAW/f'{token}.{ext}';p.write_bytes(resp.content)
   req.update(http_status=resp.status_code,final_url=resp.url,path=str(p),sha256=sha(resp.content),bytes=len(resp.content),content_type=resp.headers.get('Content-Type'))
   text='';identity=False
   if resp.status_code==200 and resp.content.startswith(b'%PDF'):
    doc=fitz.open(stream=resp.content,filetype='pdf');text='\n'.join(page.get_text() for page in doc);identity=token in re.sub(r'\s+','',doc[0].get_text());doc.close()
   elif resp.status_code==200:
    soup=BeautifulSoup(resp.content,'html.parser');article=soup.find('article');wm=soup.find(id='watermark-tr');identity=bool(wm and token in wm.get_text());text=article.get_text('\n',strip=True) if article else ''
   if identity and len(text)>1000:
    tp=RAW/f'{token}.txt';tp.write_text(text)
    rec.update(fulltext_status='version_verified',fulltext_url=url,body_path=str(p),body_sha256=sha(resp.content),text_path=str(tp),text_sha256=sha(text.encode()),version_identity_token=token)
  except requests.RequestException as error:req.update(error_type=type(error).__name__,error=str(error))
  req['finished_at']=stamp();result['requests'].append(req);save()
  if rec.get('fulltext_status'):break
 if not rec.get('fulltext_status'):rec.update(fulltext_status='blocked',blocker='Official version-specific full text could not be recovered with a matching version identity.')
 result['items'].append(rec);save();print(aid,rec['fulltext_status'],flush=True)
result['finished_at']=stamp();save()
