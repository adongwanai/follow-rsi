from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
from collections import Counter
import gzip, hashlib, json, shutil, sys
R=Path.cwd();sys.path.insert(0,str(R))
from scripts.feed.storage import load_items,save_items,write_json
from scripts.feed.review import source_hash
B=R/'build/maintenance-2026-11-23';W=B/'source-intake'
A=R/'data/feed/raw/maintenance-2026-11-23/source-intake'
D=R/'docs/internal/reports/maintenance-2026-11-23/source-intake'
A.mkdir(parents=True,exist_ok=True);D.mkdir(parents=True,exist_ok=True)
stamp=datetime.now(timezone.utc).isoformat();sha=lambda b:hashlib.sha256(b).hexdigest();rel=lambda p:str(p.relative_to(R))
p=json.loads((W/'integration-proposal.json').read_text());base={x['id']:x for x in load_items(R)}
assert len(base)==p['canonical_baseline']['canonical_count']
assert sha((R/'data/feed/items.jsonl').read_bytes())==p['canonical_baseline']['canonical_sha256']
assert not p['identity_collisions']
storage=[];mapping={}
for path in sorted((W/'network').rglob('*.body')):
 data=path.read_bytes();dest=(A/path.relative_to(W)).with_suffix('.body.gz');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(gzip.compress(data,mtime=0))
 assert gzip.decompress(dest.read_bytes())==data
 mapping[rel(path)]=rel(dest);storage.append({'original_path':rel(path),'archive_path':rel(dest),'raw_sha256':sha(data),'archive_sha256':sha(dest.read_bytes()),'compression':'gzip','original_bytes':len(data)})
for folder in ['official-metadata','source-results']:
 shutil.copytree(W/folder,A/folder,dirs_exist_ok=True)
for path in (W/'network').glob('*/attempts.jsonl'):
 dest=A/path.relative_to(W);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,dest)
for name in ['all-source-snapshot.json','all-source-snapshot.md','run-state.json','auth-presence.json','fetch-free-sources.py','reconcile-sources.py','candidate-records.jsonl']:
 shutil.copyfile(W/name,A/name)
write_json(D/'response-storage-index.json',{'generated_at':stamp,'responses':storage,'boundary':'Source hashes bind decompressed original HTTP bytes; original receipt paths resolve through this index.'})
prior=json.loads('{}')
for path in sorted((R/'docs/internal/reports').glob('maintenance-*/source-intake/all-raw-id-ledger.jsonl.gz')):
 if path.parent==D:continue
 for line in gzip.decompress(path.read_bytes()).splitlines():
  row=json.loads(line);when=row.get('evidence',{}).get('requested_at')
  if when and (row['id'] not in prior or when<prior[row['id']]['observed_at']):
   prior[row['id']]={'observed_at':when,'path':rel(path),'evidence':row['evidence']}
new=[];restored=[]
for entry in p['new_items']:
 rec=deepcopy(entry['record']);ident=rec['id'];assert ident not in base
 if ident in prior and prior[ident]['observed_at']<rec['first_seen']:
  restored.append({'id':ident,'collected_at':rec['first_seen'],'prior':prior[ident]});rec['first_seen']=prior[ident]['observed_at'];rec['first_seen_policy']='earliest_saved_raw_source_observation';rec['first_seen_evidence']=prior[ident]
 if not rec.get('arxiv_id'):
  rec.update(source_reported_updated=rec.get('updated'),updated='',updated_source='unknown',version_status='unknown',stored_version_placeholder=0)
  rec['published_source']='official_publisher_rss' if rec['kind']=='post' else 'semantic_scholar';rec['official_metadata_verified']=rec['kind']=='post';rec['metadata_pending']=rec['kind']=='paper'
 evidence=rec.get('official_metadata_evidence')
 if evidence and evidence.get('path','').startswith(rel(W)):
  evidence['path']=evidence['path'].replace(rel(W),rel(A),1);assert sha((R/evidence['path']).read_bytes())==evidence['sha256']
 rec['source_discovery_evidence']={'request_bindings':entry['bindings'],'archived_network_response_index':rel(D/'response-storage-index.json')}
 new.append(rec)
updates=[];preserved=[]
for entry in p['existing_provenance_updates']:
 old=base[entry['id']];rec=deepcopy(old);assert old['first_seen']==entry['existing_first_seen']
 for field,values in entry['add_to_sets'].items():rec[field]=sorted(set(rec.get(field,[]))|set(values))
 record={'id':rec['id'],'source_hash_before':source_hash(old),'source_hash_after':source_hash(rec),'added':entry['add_to_sets'],'original_review':deepcopy(old.get('review')),'old_review_preserved':True,'first_seen_preserved':True,'scientific_fields_preserved':True,'bindings':entry['bindings'],'boundary':'Only recommendation/source membership added; original approval is not rebound and no republication is implied.'}
 rec.setdefault('source_refresh_history',[]).append(record);updates.append(rec);preserved.append(record)
count=save_items(R,new+updates);after={x['id']:x for x in load_items(R)}
assert len(after)==len(base)+len(new)
assert all(after[k]['first_seen']==v['first_seen'] for k,v in base.items())
assert all(after[k]==v for k,v in base.items() if k not in {x['id'] for x in updates})
assert save_items(R,new+updates)==0
raw=[json.loads(l) for l in (W/'raw-source-id-reconciliation.jsonl').read_text().splitlines()]
compact=[{**{k:x[k] for k in ['source_id','id','title','published_as_reported','disposition','evidence']},'canonical_present_after':x['id'] in after,'resolution':'canonical_present' if x['id'] in after else x['disposition']} for x in raw]
assert all(x['canonical_present_after'] for x in compact if x['disposition']=='within_requested_source_window')
(D/'all-raw-id-ledger.jsonl.gz').write_bytes(gzip.compress((''.join(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n' for x in compact)).encode(),mtime=0))
boards={}
for line in (W/'network/hf-daily/attempts.jsonl').read_text().splitlines():
 receipt=json.loads(line)
 if receipt.get('http_status')!=200:continue
 path=R/receipt['body_path'];body=json.loads(path.read_bytes());day=receipt['params']['date'];ids=['arxiv:'+x['paper']['id'] for x in body]
 assert all(k in after and day in after[k].get('hf_daily_dates',[]) for k in ids)
 boards[day]={'count':len(ids),'ids':ids,'observed_at':receipt['requested_at'],'body_sha256':sha(path.read_bytes()),'archive_path':mapping[rel(path)],'missing_canonical':[],'missing_recommendation_day':[]}
write_json(D/'hf-board-reconciliation.json',{'generated_at':stamp,'boards':boards,'keyword_prefilter_used':False,'nov18_previous_snapshot':'The Nov18 published bulletin truthfully recorded not_ready at its own observation time. These late members were first retrieved on Nov23, not on Nov18.'})
receipt={'generated_at':stamp,'before_count':len(base),'after_count':len(after),'new_candidates':len(new),'new_by_kind':dict(Counter(x['kind'] for x in new)),'existing_updates':preserved,'prior_observations_preserved':restored,'all_existing_first_seen_preserved':True,'raw_occurrences':len(raw),'raw_unique_ids':len({x['id'] for x in raw}),'all_window_ids_present':True,'all_hf_members_and_dates_present':True,'canonical_after_sha256':sha((R/'data/feed/items.jsonl').read_bytes()),'second_apply_changed':0,'paid_generation_requests':0,'scope_boundary':'Source integration only; publication needs dated review PRs and live verification.'}
write_json(D/'integration-receipt.json',receipt)
write_json(A/'effective-integration-proposal.json',{**p,'applied':True,'production_writes':count,'new_items':[{'id':x['id'],'record':x,'source_hash':source_hash(x)} for x in new]})
shutil.copyfile(W/'all-source-snapshot.md',D/'README.md')
shutil.copyfile(Path(__file__),A/'integrate-sources.py')
print(json.dumps({k:receipt[k] for k in ['before_count','after_count','new_candidates','new_by_kind','second_apply_changed']}))
