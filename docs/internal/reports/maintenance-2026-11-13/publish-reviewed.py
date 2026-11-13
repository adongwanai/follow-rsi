from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
import json,subprocess,hashlib,base64,sys,yaml
from scripts.feed.ci import merged_review_requests,human_owner_review
from scripts.feed.review import validate_daily_review,apply_daily_review,validate_weekly_picks
from scripts.feed.digest import publish_day,publish_week
from scripts.feed.storage import write_json,load_items,save_items
ROOT=Path.cwd();OUT=ROOT/'build/maintenance-2026-11-13';REPO='adongwanai/follow-rsi'
def gh(endpoint):return json.loads(subprocess.check_output(['gh','api',endpoint],text=True))
receipts=[]
preflight={x['date']:x for x in json.loads((OUT/'review-preflight.json').read_text())['reviews']}
for argument in sys.argv[1:]:
 number,expected_head=argument.split(':');number=int(number);pr=gh(f'repos/{REPO}/pulls/{number}')
 assert pr['merged'] and pr['base']['ref']=='main' and pr['head']['repo']['full_name']==REPO
 assert pr['head']['sha']==expected_head
 pages=json.loads(subprocess.check_output(['gh','api','--paginate','--slurp',f'repos/{REPO}/pulls/{number}/files?per_page=100'],text=True))
 files=[item for page in pages for item in page];assert len(files)==pr['changed_files']
 requests=merged_review_requests({'pull_request':pr},[f['filename'] for f in files],REPO);assert len(requests)==1
 owner=human_owner_review(pr,gh(f'repos/{REPO}/pulls/{number}/reviews?per_page=100'),REPO)
 checks=gh(f'repos/{REPO}/commits/{expected_head}/check-runs?per_page=100')['check_runs']
 for name in ['build','validate']:
  matches=[x for x in checks if x['name']==name];assert matches and max(matches,key=lambda x:x['id'])['conclusion']=='success',(number,name)
 statuses=gh(f'repos/{REPO}/commits/{expected_head}/status')['statuses']
 matches=[x for x in statuses if x['context']=='Follow RSI owner decisions'];assert matches and matches[0]['state']=='success'
 request=requests[0];file=gh(f'repos/{REPO}/contents/{request["path"]}?ref={pr["merge_commit_sha"]}')
 blob=gh(f'repos/{REPO}/git/blobs/{file["sha"]}');content=base64.b64decode(blob['content'])
 assert content==(ROOT/request['path']).read_bytes()
 provenance={'github_pr':number,'owner_login':owner,'merge_commit':pr['merge_commit_sha']}
 name=request.get('date') or request['week']
 write_json(ROOT/'data/feed/review-provenance'/f'{name}.json',{**request,**provenance})
 if request['kind']=='daily':
  full_review=validate_daily_review(ROOT,name)
  assert hashlib.sha256(content).hexdigest()==preflight[name]['draft_sha256']
  selected=set(preflight[name]['changed_ids_only_to_apply'])
  subset=deepcopy(full_review)
  for group in ['items','lab_updates']:subset[group]=[x for x in full_review[group] if x['id'] in selected]
  assert {x['id'] for x in subset['items']+subset['lab_updates']}==selected
  before={x['id']:deepcopy(x) for x in load_items(ROOT)}
  history=[]
  for ident in selected:
   old=before[ident]
   if old.get('review'):
    updated=deepcopy(old);prior=updated.setdefault('review_history',[])
    if old['review'] not in prior:prior.append(deepcopy(old['review']))
    history.append(updated)
  save_items(ROOT,history)
  try:
   (ROOT/request['path']).write_text(yaml.safe_dump(subset,allow_unicode=True,sort_keys=False,width=110))
   changed=apply_daily_review(ROOT,name,provenance=provenance)
  finally:(ROOT/request['path']).write_bytes(content)
  after={x['id']:x for x in load_items(ROOT)}
  assert all(after[ident]==old for ident,old in before.items() if ident not in selected)
  assert all(after[ident]['review']['source_hash']==next(x['source_hash'] for x in subset['items']+subset['lab_updates'] if x['id']==ident) for ident in selected)
  result=publish_day(ROOT,name,allow_status=True)
 else:
  validate_weekly_picks(ROOT,name);changed=0;result=publish_week(ROOT,name,render_card=True)
 if result.get('manifest'):result['manifest']=str(Path(result['manifest']).relative_to(ROOT))
 receipt={**request,**provenance,'head':expected_head,'review_sha256':hashlib.sha256(content).hexdigest(),'verified_at':datetime.now(timezone.utc).isoformat(),'applied_records':changed,'applied_ids':sorted(selected) if request['kind']=='daily' else [],'application_boundary':'Full approved bytes and exact head verified; only the approved changed rows applied, other existing decisions preserved.','local_generation':result,'authorization':'Owner standing automatic review/merge/publication instruction; account merge receipt does not imply owner personally read each paper.','boundary':'Generated locally after real approved merge and exact-head CI; Pages deployment not yet verified.'}
 receipts.append(receipt);write_json(OUT/'publication-generation.json',receipts);print(json.dumps(receipt),flush=True)
