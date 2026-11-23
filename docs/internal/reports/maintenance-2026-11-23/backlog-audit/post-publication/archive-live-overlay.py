from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
import json,gzip,shutil,hashlib,subprocess,os
R=Path.cwd();B=R/'build/maintenance-2026-11-23';D=R/'docs/internal/reports/maintenance-2026-11-23';F=D/'publication-final';ENV={**os.environ,'GODEBUG':'http2client=0'}
load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
live=load(B/'live-verification.json');assert live['online_verified'];merged=load(B/'pr-audit/pr-153-merged.json');assert merged['merged']
pages=load(B/'publication-pages.json');assert pages['conclusion']=='success' and pages['headSha']==merged['merge_commit_sha']
for p in (B/'pr-audit').glob('pr-153-*.json'):shutil.copyfile(p,F/p.name)
for n in ('live-verification.json','publication-pages.json','usage-boundary-end.json','publication-ci-success.json','publication-ci-success.log.gz'):shutil.copyfile(B/n,F/n)
shutil.copyfile('/private/tmp/follow-rsi-live-20261123.py',F/'verify-live.py')
issues=F/'issue-closeout';issues.mkdir(exist_ok=True)
for p in (B/'issue-closeout').iterdir():
 if p.is_file():
  if p.name.endswith(('-before.json','-after.json')):(issues/(p.name+'.gz')).write_bytes(gzip.compress(p.read_bytes(),mtime=0))
  else:shutil.copyfile(p,issues/p.name)
actions=load(issues/'actions.json');assert {r['issue'] for r in actions if r.get('state_after')=='closed'}=={115,116,144}
pre=D/'backlog-audit/post-application';post=D/'backlog-audit/post-publication';post.mkdir(exist_ok=True);rows=[json.loads(l) for l in gzip.open(pre/'backlog-ledger.jsonl.gz','rt')]
verified_paths={r['local_path']:r for r in live['requests'] if r['bytes_match']};decisions={r['id']:r for r in load(D/'primary-review/final-adjudication.json')['items']};affected=0
for r in rows:
 if r['id'] not in decisions:continue
 a=decisions[r['id']];r['post_publication_previous_status']=r['status'];r['audit_stage']='post_publication_exact_reviews_and_live_receipts';r['publication_pull_request']={'github_pr':153,'head':merged['head']['sha'],'merge_commit':merged['merge_commit_sha'],'owner_login':merged['merged_by']['login']};affected+=1
 if a['application']=='apply' and a['decision'] in ('accept','backlog'):
  paths=r['local_publication_artifacts'];assert paths and all(p in verified_paths for p in paths)
  r.update(status='published_with_exact_review_and_live_byte_receipts',live_publication_verified_by_this_audit=True,live_publication_receipts=[verified_paths[p] for p in paths],next_actions=['来源内容、版本或反馈证据变化时再做针对性复审；保留本次摘要限制与原始刊期。'])
 elif a['application']=='apply' and a['decision']=='defer':
  r['issue_tracking_receipt']=next(x for x in actions if x['issue']==60)
 elif r['id'] in ('arxiv:2609.38372','arxiv:2609.34924'):
  number=115 if r['id']=='arxiv:2609.38372' else 116;key='self-evolving-multi-task' if number==115 else 'audit-the-scaffold';path=f'site/p/{key}.html';assert path in verified_paths
  r.update(status='v2_current_card_wording_and_numeric_claims_checked_live',live_publication_verified_by_this_audit=True,live_publication_receipts=[verified_paths[path]],issue_tracking_receipt=next(x for x in actions if x['issue']==number),next_actions=['现行卡片无实验数字声称，质性断言已对照 pinned v2；历史完整版本/数值/证明任务继续保留，不称实验复现。'])
 elif a['application']!='apply':
  r['next_actions']=['本次 HF 日期元数据回执已合并并归档；旧科学审核及既有公开快照保留，仅在来源内容变化时重新审核。']
assert affected==238 and len(rows)==9292
payload=''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows).encode();(post/'backlog-ledger.jsonl.gz').write_bytes(gzip.compress(payload,mtime=0))
summary={'stage':'post_publication_exact_reviews_and_live_receipts','observed_at':datetime.now(timezone.utc).isoformat(),'universe_ids':len(rows),'canonical_ids':2456,'formal_new_canonical_decisions':{'accept_daily':25,'historical_backlog':4,'reject':202,'defer_specific_evidence':3},'metadata_only_receipts':4,'current_requested_publications_online_verified':True,'all_historical_publications_reverified_this_run':False,'new_publication_item_receipts':29,'v2_card_editorial_live_receipts':2,'all_id_buckets':dict(Counter(r['processing_bucket'] for r in rows)),'all_ids_have_specific_recoverable_status':all(r.get('status') and r.get('reason_zh') for r in rows),'historical_version_tasks_preserved':2096,'historical_model_errors_preserved':41,'pre_application_version_tasks_sha256':sha(D/'backlog-audit/pre-application/version-review-tasks.jsonl.gz'),'ledger_sha256':sha(post/'backlog-ledger.jsonl.gz'),'live_verification_sha256':sha(F/'live-verification.json'),'publication_pr':153,'publication_merge_commit':merged['merge_commit_sha'],'remaining_external_issue_numbers':[19,20,23,30,60,119,128],'closed_issue_numbers':[115,116,144],'scope_review_not_experimental_replication':True,'paid_generation_requests':0,'paid_generation_tokens':0}
(post/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');shutil.copyfile(__file__,post/'archive-live-overlay.py')
operational={}
for key,args in [('open_prs',['pr','list','--repo','adongwanai/follow-rsi','--state','open','--json','number,title,headRefOid,url']),('open_issues',['issue','list','--repo','adongwanai/follow-rsi','--state','open','--limit','100','--json','number,title,url']),('workflows',['api','repos/adongwanai/follow-rsi/actions/workflows'])]:
 operational[key]=json.loads(subprocess.check_output(['gh',*args],env=ENV,text=True))
assert not operational['open_prs']
wf={x['path']:x['state'] for x in operational['workflows']['workflows']}
assert all(wf[f'.github/workflows/{n}']=='disabled_manually' for n in ('feed-daily.yml','feed-eval.yml','feed-publish.yml'))
operational.update(observed_at=datetime.now(timezone.utc).isoformat(),boundary='Snapshot after publication/issue closeout and before creating the archival receipt PR. Final open-PR count must be checked again after that PR merges.')
(F/'pre-archival-pr-operational-snapshot.json').write_text(json.dumps(operational,ensure_ascii=False,indent=2)+'\n')
readme=D/'README.md';readme.write_text(readme.read_text()+f'''\n## Verified publication and closeout\n\nPublication #153 merged at `{merged['merge_commit_sha']}`. The corresponding Pages run succeeded, and {len(live['requests'])} public responses matched the reviewed local bytes. Verified surfaces include all six daily editions, W47, the new historical recap, archives, latest.json, Atom, source status, homepage data, bilingual READMEs, two v2 cards and their images, and the October 27 withdrawal. See `publication-final/live-verification.json` and `backlog-audit/post-publication/summary.json`.\n\nIssues #115, #116 and #144 are closed with bounded explanations. Six older artifact-evidence issues remain open, and #60 records the three new evidence deferrals, source limits and recoverable internal work. The pre-archival snapshot has zero open PRs; the archival receipt PR itself still requires CI and merge, followed by a final live operational check.\n\nThe ending usage boundary confirms zero paid generation requests/tokens and no usage-log additions. Both balance queries succeeded; private raw values are not committed. The observed account decrease did not reach the CNY 5 stop boundary. Account balance changes are not this task's invoice; a single future request can exceed the stopping value.\n''')
print(json.dumps(summary,ensure_ascii=False))
