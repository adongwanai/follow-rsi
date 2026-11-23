from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
import gzip,json,hashlib,shutil
from scripts.feed.storage import load_items,save_items
from scripts.feed.review import source_hash
R=Path.cwd();B=R/'build/maintenance-2026-11-23/late-issues';D=R/'docs/internal/reports/maintenance-2026-11-23/late-issues';A=R/'data/feed/raw/maintenance-2026-11-23/late-issues'
D.mkdir(exist_ok=True);A.mkdir(exist_ok=True);h=lambda b:hashlib.sha256(b).hexdigest()
records=json.loads((B/'sources/records.json').read_text());before={i['id']:i for i in load_items(R)};ids={i['id'] for i in records};assert not(ids & before.keys())
patterns={k.split(':')[1].encode() for k in ids};scanned=[];matches=[]
for p in sorted((R/'docs/internal/reports').rglob('*.jsonl.gz')):
 raw=gzip.decompress(p.read_bytes());scanned.append({'path':str(p.relative_to(R)),'sha256':h(p.read_bytes())})
 for line in raw.splitlines():
  if any(v in line for v in patterns):matches.append({'path':str(p.relative_to(R)),'row':json.loads(line)})
assert not matches,matches
for p in sorted((B/'sources').iterdir()):
 if p.is_file():shutil.copyfile(p,A/p.name)
for n in [160,162,163]:shutil.copyfile(B/f'issue-{n}-before.json',A/f'issue-{n}-before.json')
req=json.loads((A/'metadata-request.json').read_text());req['body_path']=str((A/'metadata.atom').relative_to(R));assert req['sha256']==h((A/'metadata.atom').read_bytes());(A/'metadata-request.json').write_text(json.dumps(req,indent=2)+'\n')
request_rows=json.loads((A/'requests.json').read_text())
for row in request_rows:row['body_path']=str((A/Path(row['body_path']).name).relative_to(R))
(A/'requests.json').write_text(json.dumps(request_rows,ensure_ascii=False,indent=2)+'\n')
nums={'arxiv:2611.27285':160,'arxiv:2611.27110':162,'arxiv:2611.27006':163}
for i in records:
 n=nums[i['id']];issue=json.loads((A/f'issue-{n}-before.json').read_text());issue=issue.get('issue',issue)
 i.update(first_seen=issue['created_at'],first_seen_policy='earliest_saved_github_monitor_observation',source_observed_at=issue['created_at'],source_discovery_evidence={'issue':n,'url':issue['html_url'],'created_at':issue['created_at'],'path':str((A/f'issue-{n}-before.json').relative_to(R))},official_metadata_verified=True,metadata_pending=False,updated_source='arxiv',official_metadata_evidence=req,intake_review_status='late_candidate_pending_formal_review',hf_daily_dates=[])
 assert i['published'][:10]=='2026-11-20'
changed=save_items(R,records);after={i['id']:i for i in load_items(R)};assert changed==3 and len(after)==2459;assert all(after[k]==v for k,v in before.items());assert save_items(R,records)==0
receipt={'observed_at':datetime.now(timezone.utc).isoformat(),'batch':'late_github_monitor_discovery','prior_intake_snapshot_preserved':True,'canonical_before':2456,'canonical_after':2459,'new_ids':sorted(ids),'prior_historical_ids':9292,'historical_ids_including_this_overlay':9295,'prior_canonical_alias_or_compressed_ledger_matches':matches,'historical_ledger_files_checked':scanned,'all_existing_items_unchanged':True,'second_apply_changed':0,'category_coverage_note':'SIR-Agent and RemoteEvolver are cs.CV only; PhyRSI uses astro-ph/physics.comp-ph. These categories are absent from the current configured arXiv query category filter. The GitHub monitoring issues supplied the late discoveries; this is not a source API failure. No HF recommendation day was observed in the full saved boards.','items':[{'id':i['id'],'issue':nums[i['id']],'source_hash':source_hash(i),'first_seen':i['first_seen'],'published':i['published'],'updated':i['updated'],'version':i['version'],'next_action':'Complete source-bound independent review, merge the actual November 20 dated review, then apply only these new IDs.'} for i in records],'paid_model_requests':0,'generation_tokens':0}
(D/'integration-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
(D/'source-records.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');shutil.copyfile(Path(__file__),D/'integrate-late-sources.py')
print(json.dumps({'new':3,'canonical':len(after),'historical_ids':9295,'ledger_files_checked':len(scanned),'historical_matches':0,'old_items_unchanged':True}))
