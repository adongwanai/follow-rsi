"""Read-only per-stable-ID audit; writes only the requested temporary output directory."""
from pathlib import Path
from copy import deepcopy
from collections import Counter, defaultdict
from datetime import datetime, timezone
import argparse, gzip, hashlib, json, sys, shutil
import yaml

p=argparse.ArgumentParser();p.add_argument('--root',default=str(Path.cwd()));p.add_argument('--output',default='/private/tmp/follow-rsi-2026-11-23-backlog-final');args=p.parse_args()
R=Path(args.root);O=Path(args.output);O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R))
from scripts.feed.review import source_hash
DAY='2026-11-23'
OLD=R/'data/feed/raw/maintenance-2026-11-18/backlog-audit/post-review-v4/backlog-ledger.jsonl.gz'
VER=OLD.parent/'version-review-tasks.jsonl.gz'
RAW=R/'docs/internal/reports/maintenance-2026-11-23/source-intake/all-raw-id-ledger.jsonl.gz'
CAN=R/'data/feed/items.jsonl'
BASE=R/'build/maintenance-2026-11-23/source-intake/canonical-baseline.jsonl'
BOARDS=R/'docs/internal/reports/maintenance-2026-11-23/source-intake/hf-board-reconciliation.json'
SCOPE=R/'docs/internal/reports/maintenance-2026-11-23/independent-backlog/review.json'
CORRECTIONS=R/'docs/internal/reports/maintenance-2026-11-23/independent-backlog/version-corrections.json'
STARTISSUES=R/'docs/internal/reports/maintenance-2026-11-23/pr-audit/open-issues-start.json'
def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def rawbytes(p):return gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes()
def rows(p):return [json.loads(l) for l in rawbytes(p).splitlines()]
def ref(p,**extra):return {'path':str(p.relative_to(R)) if p.is_relative_to(R) else str(p),'sha256':sha_bytes(p.read_bytes()),**extra}
def save(name,obj):(O/name).write_text(json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
def save_lines(name,data):
 b=b''.join((json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n').encode() for x in data)
 (O/name).write_bytes(gzip.compress(b,mtime=0))
 return {'path':name,'compressed_sha256':sha_bytes((O/name).read_bytes()),'jsonl_sha256':sha_bytes(b),'rows':len(data)}

oldrows=rows(OLD);old={x['id']:x for x in oldrows};assert len(old)==len(oldrows)==9052
canonical_rows=rows(CAN);canonical={x['id']:x for x in canonical_rows};assert len(canonical)==len(canonical_rows)
baseline={x['id']:x for x in rows(BASE)}
rawrows=rows(RAW);raw_by_id=defaultdict(list)
rawref=ref(RAW)
for i,x in enumerate(rawrows):raw_by_id[x['id']].append((i,x))
versionrows=rows(VER);assert len(versionrows)==2096
old_errors={x['id']:x for x in oldrows if x.get('historical_model_error')};assert len(old_errors)==41
backlog_review=json.loads(SCOPE.read_text());backlog_by_id={x['id']:x for x in backlog_review['items']}
review_refs={};advice={};advice_history=defaultdict(list);sources=[]
for group in ['hf','other']:
 w=R/'docs/internal/reports/maintenance-2026-11-23'/f'independent-{group}';f=w/'final.json';payload=json.loads(f.read_text());fr=ref(f,group=group)
 sources.append(fr)
 for i,row in enumerate(payload['items']):
  assert row['id'] not in advice,row['id'];advice[row['id']]=row;review_refs[row['id']]={**fr,'index':i}
 for f in sorted(w.glob('amendments-*.json')):
  payload=json.loads(f.read_text());fr=ref(f,group=group);sources.append(fr)
  for i,row in enumerate(payload['items']):
   ident=row['id'];assert ident in advice;advice_history[ident].append({'row':advice[ident],'ref':review_refs[ident]});advice[ident]=row;review_refs[ident]={**fr,'index':i}

catalog={p['arxiv']:p for p in yaml.safe_load((R/'data/papers.yaml').read_text())['papers'] if p.get('arxiv')}
boards=json.loads(BOARDS.read_text());hf_dates=defaultdict(list)
for day,b in boards['boards'].items():
 for ident in b.get('ids',[]):hf_dates[ident].append(day)
missing_firstseen=[{'id':i,'before':c['first_seen'],'current':canonical.get(i,{}).get('first_seen')} for i,c in baseline.items() if canonical.get(i,{}).get('first_seen')!=c['first_seen']]
assert not missing_firstseen,missing_firstseen
oldref=ref(OLD);scope_ref=ref(SCOPE);version_correction_ref=ref(CORRECTIONS)
allids=sorted(set(old)|set(raw_by_id)|set(canonical));result=[]
for ident in allids:
 previous=old.get(ident);c=canonical.get(ident);a=advice.get(ident);br=backlog_by_id.get(ident)
 row=deepcopy(previous) if previous else {'id':ident,'reason_zh':[],'next_actions':[],'version_tasks':[],'legacy_discovery_and_failure_refs':[],'legacy_discovery_member':False,'historical_model_error':None,'preserved_historical_model_error':None,'issue_refs':[]}
 if previous:row['maintenance_baseline_ledger_ref']={**oldref,'id':ident}
 row['audit_date']=DAY;row['audit_stage']='prepublication_advice_and_current_canonical_reconciliation'
 row['prior_daily_observation']={k:deepcopy(previous.get(k)) for k in ['status','processing_bucket','current_raw_refs','current_raw_dispositions','canonical_source_hash','formal_review_source_hash_matches']} if previous else None
 row['current_raw_refs']=[{**rawref,'index':i,'source_id':x['source_id'],'disposition':x['disposition']} for i,x in raw_by_id.get(ident,[])]
 row['current_raw_dispositions']=sorted({x['disposition'] for _,x in raw_by_id.get(ident,[])})
 row['in_canonical']=c is not None
 row['new_to_canonical_this_maintenance']=ident not in baseline and c is not None
 row['new_to_full_history_ledger']=previous is None
 row['no_new_paid_model_success_claimed']=True
 row['live_publication_verified_by_this_audit']=False
 row['current_hf_board_dates']=sorted(hf_dates.get(ident,[]))
 row['current_scope_advice']=None
 row['formal_github_head_verified_by_this_audit']=False
 if c:
  row.update(title=c['title'],first_seen=c['first_seen'],published_original=c.get('published'),version_updated=c.get('updated'),canonical_version=c.get('version'),canonical_source_hash=source_hash(c),canonical_hf_daily_dates=c.get('hf_daily_dates',[]),formal_review=c.get('review'),catalog_entry=catalog.get(c.get('arxiv_id')))
  review=c.get('review')
  row['formal_review_source_hash_matches']=bool(review and review.get('source_hash')==source_hash(c))
  row['existing_first_seen_preserved']=(ident not in baseline or c['first_seen']==baseline[ident]['first_seen'])
  row['missing_canonical_hf_dates']=sorted(set(hf_dates.get(ident,[]))-set(c.get('hf_daily_dates',[])))
  if ident in baseline:
   hashkeys=('id','version','title','abstract','links','retracted','published','updated','summary_zh','summary_en','evidence_quick','llm','gate','backfill_only')
   changed=[k for k in hashkeys if c.get(k)!=baseline[ident].get(k)]
   row['source_fields_changed_since_intake_baseline_excluding_hf_dates']=changed
   row['scientific_fields_identical_to_intake_baseline']=not changed
  if not previous and not a:
   row.update(status='new_canonical_without_current_review_advice',processing_bucket='pending_evidence',next_actions=['Obtain item-specific source-bound scope advice before formal acceptance.'])
   row['reason_zh'].append(f'{ident}：来源已规范化，未匹配到本轮范围审核意见，保留待审核；不自动接受。')
 if a:
  decision=a['decision'];assert decision in ['accept','reject','defer','backlog'],decision
  row['current_scope_advice']={'ref':review_refs[ident],'decision':decision,'reason_zh':a['reason_zh'],'direction':a.get('direction'),'missing_evidence':a.get('missing_evidence',[]),'next_step_zh':a.get('next_step_zh'),'publication_action':a.get('publication_action'),'is_new_science':a.get('is_new_science'),'input_source_hash':a.get('input_source_hash'),'input_record_sha256':a.get('input_record_sha256'),'source_sha256':a.get('source_sha256'),'current_canonical_hash_at_audit':source_hash(c) if c else None,'formal_acceptance_or_publication_claim':False}
  row['current_scope_advice_history']=advice_history.get(ident,[])
  row['reason_zh'].append('11/23逐项范围意见：'+a['reason_zh'])
  if a.get('existing_review_reuse'):
   row['status']='existing_source_review_reused_recommendation_dates_reconciled';row['processing_bucket']='formal_or_catalog_record';row['next_actions']=['Preserve prior scientific review and first_seen; publish only correctly dated provenance if needed.']
  elif decision in ('accept','backlog'):
   row['status']='positive_scope_advice_pending_exact_dated_review_and_publication';row['processing_bucket']='editorial_pending';row['next_actions']=[a.get('next_step_zh') or '将逐项证据与范围意见纳入准确日期审核，绑定真实 PR/head/merge 后决定刊期；未上线前不称已发布。']
  elif decision=='reject':
   row['status']='scope_exclusion_advice_pending_exact_dated_review';row['processing_bucket']='reusable_scope_advice';row['next_actions']=[a.get('next_step_zh') or '在真实日期审核中记录此排除及来源哈希，保留异议和后续新证据重开条件。']
  else:
   missing=a.get('missing_evidence',[]);row['status']='specific_evidence_gap_in_current_scope_review';row['processing_bucket']='external_blocked' if any('完整原始来源' in s or '全文' in s or '出版者' in s for s in missing) else 'pending_evidence';row['next_actions']=[a.get('next_step_zh') or '; '.join(missing)]
  if c and c.get('review',{}).get('reviewed_on')==DAY:
   row['local_current_date_review_receipt']=deepcopy(c['review'])
   row['local_current_date_review_exact_hash']=c['review'].get('source_hash')==source_hash(c)
   row['local_receipt_requires_parent_remote_verification']=True
 if br:
  row['current_legacy_issue_crosscheck']={'ref':scope_ref,'issue':br['issue'],'status':br['status'],'reason_zh':br['reason_zh'],'next_action_zh':br['next_action_zh'],'source_html_bytes_unchanged_from_nov18':br['source_receipt']['identical_body_to_nov18']}
  row['reason_zh'].append('11/23独立边界复核：'+br['reason_zh'])
  if br['issue'] in [115,116]:
   row.update(status='editorial_correction_prepared_pending_merge',processing_bucket='editorial_pending',next_actions=['核对并合并限定措辞的真实审核 PR；保留 v1 科学快照与未完成的 v2 完整数值/版本审核，不在此账本声称正式采用或纳入。'])
   row['prepared_editorial_correction_ref']=version_correction_ref
  else:
   row.update(status=br['status'],processing_bucket='external_blocked',next_actions=[br['next_action_zh']])
 if not c and not previous:
  ds=row['current_raw_dispositions'];source_entries=raw_by_id[ident];row['title']=source_entries[0][1]['title']
  incomplete=any(x in ds for x in ['missing_publication_date','needs_official_metadata'])
  row['processing_bucket']='source_date_metadata_unavailable' if incomplete else 'outside_candidate_window'
  row['status']='raw_only_publication_date_unresolved' if incomplete else 'raw_only_outside_saved_source_windows'
  row['reason_zh']=[f'{ident}：原始响应保留，窗口处置为 {", ".join(ds)}；未规范化，不能将窗口过滤当作科学范围排除。']
  row['next_actions']=['从原始来源补齐发表日期或稳定身份后重查真实来源窗口。'] if incomplete else ['保留原始来源绑定；仅在符合后续真实窗口或明确历史补录任务时重开。']
 assert row.get('reason_zh'),ident
 assert row.get('status'),ident
 assert 'next_actions' in row,ident
 if previous:
  assert row['version_tasks']==previous['version_tasks'],ident
  assert row.get('historical_model_error')==previous.get('historical_model_error'),ident
  assert row.get('preserved_historical_model_error')==previous.get('preserved_historical_model_error'),ident
 result.append(row)

index={x['id']:x for x in result}
assert set(old)<=set(index)
assert sum(len(x['version_tasks']) for x in result)==2096
assert sum(bool(x.get('historical_model_error')) for x in result)==41
assert not [x['id'] for x in result if x.get('missing_canonical_hf_dates')]
ledger=save_lines('backlog-ledger.jsonl.gz',result)
shutil.copyfile(VER,O/'version-review-tasks.jsonl.gz')
errorrecords=[{'id':i,'historical_model_error':x.get('historical_model_error'),'preserved_historical_model_error':x.get('preserved_historical_model_error'),'new_paid_model_success_claimed':False,'prior_ledger_ref':oldref} for i,x in old_errors.items()]
save('historical-model-errors.json',errorrecords)
summary={'generated_at':datetime.now(timezone.utc).isoformat(),'date':DAY,'stage':'prepublication_advice_and_current_canonical_reconciliation','universe_ids':len(result),'baseline_universe_ids':len(old),'new_to_full_history_ids':len(set(index)-set(old)),'canonical_ids':len(canonical),'baseline_canonical_ids':len(baseline),'new_canonical_ids':len(set(canonical)-set(baseline)),'new_canonical_ids_absent_from_old_full_ledger':len(set(canonical)-set(old)),'current_raw_occurrences':len(rawrows),'current_raw_unique_ids':len(raw_by_id),'all_id_buckets':dict(Counter(x['processing_bucket'] for x in result)),'canonical_buckets':dict(Counter(x['processing_bucket'] for x in result if x['in_canonical'])),'current_independent_advice_rows':len(advice),'current_independent_advice_counts':dict(Counter(x['decision'] for x in advice.values())),'new_canonical_advice_counts':dict(Counter(advice[i]['decision'] if i in advice else 'missing' for i in set(canonical)-set(baseline))),'current_advice_ref_source_counts':dict(Counter(x['group'] for x in review_refs.values())),'current_advice_amended_ids':list(advice_history),'existing_first_seen_changed':missing_firstseen,'old_ids_missing':[],'old_version_task_count':len(versionrows),'version_tasks_preserved_exactly':True,'version_task_statuses':dict(Counter(x['status'] for x in versionrows)),'old_historical_model_errors_preserved':len(errorrecords),'all_ids_have_recoverable_status':True,'all_ids_without_reason':[],'missing_canonical_hf_dates':[],'legacy_issues_external_artifact_blockers':[19,20,23,30,119,128],'legacy_issues_editorial_correction_prepared':[115,116],'paid_generation_requests':0,'github_writes':0,'production_writes':0,'all_current_publications_live_verified_by_this_audit':False,'formal_github_heads_verified_by_this_audit':False,'publication_boundary':'Independent advice and current local canonical only. Parent must add exact remote review/merge and live-publication evidence after apply; existing frozen history remains recoverable.','ledger':ledger,'inputs':[ref(p) for p in [OLD,VER,RAW,CAN,BASE,BOARDS,SCOPE,CORRECTIONS,STARTISSUES]]+sources}
save('summary.json',summary)
save('current-scope-advice-index.json',[{'id':i,'ref':review_refs[i],'decision':a['decision'],'reason_zh':a['reason_zh'],'amendment_count':len(advice_history[i])} for i,a in advice.items()])
print(json.dumps({k:summary[k] for k in ['universe_ids','canonical_ids','new_canonical_ids','current_raw_occurrences','current_raw_unique_ids','current_independent_advice_counts','old_version_task_count','old_historical_model_errors_preserved']},ensure_ascii=False));print(str(O/'summary.json'))
