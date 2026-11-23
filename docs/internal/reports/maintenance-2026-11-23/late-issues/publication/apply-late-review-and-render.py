from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
import json,yaml,hashlib,subprocess,os,shutil
from scripts.feed.storage import load_items,save_items,write_json
from scripts.feed.review import apply_daily_review,source_hash,daily_editions_for_week,validate_weekly_picks
from scripts.feed.ci import merged_review_requests,human_owner_review
from scripts.feed.digest import publish_day,initialize_public,_directions,_summary_intro,_metrics
R=Path.cwd();B=R/'build/maintenance-2026-11-23';L=B/'late-issues';D=R/'docs/internal/reports/maintenance-2026-11-23/late-issues';O=D/'publication';O.mkdir(exist_ok=True);REPO='adongwanai/follow-rsi';ENV={**os.environ,'GODEBUG':'http2client=0'};STAMP=datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z');h=lambda b:hashlib.sha256(b).hexdigest()
assert not (O/'generation-receipt.json').exists(),'Do not reapply the late review.'
plan=json.loads((L/'review-plan.json').read_text());entry=json.loads((L/'review-pr.json').read_text());number=entry['number'];head=entry['head']
def gh(*a):return json.loads(subprocess.check_output(['gh',*a],text=True,env=ENV))
pr=gh('api',f'repos/{REPO}/pulls/{number}');assert pr['merged'] and pr['head']['sha']==head and pr['base']['ref']=='main'
files=gh('api','--paginate','--slurp',f'repos/{REPO}/pulls/{number}/files?per_page=100');files=[x for page in files for x in page];requests=merged_review_requests({'pull_request':pr},[x['filename'] for x in files],REPO);assert requests==[{'kind':'daily','date':'2026-11-20','path':plan['path']}]
owner=human_owner_review(pr,[],REPO);checkpath=B/f'pr-audit/pr-{number}-checks.json';checks=json.loads(checkpath.read_text());assert checks['head']==head
for name in ['build','validate']:assert max([x for x in checks['checks']['check_runs'] if x['name']==name],key=lambda x:x['id'])['conclusion']=='success'
assert max([x for x in checks['statuses']['statuses'] if x['context']=='Follow RSI owner decisions'],key=lambda x:x['id'])['state']=='success'
path=R/plan['path'];content=subprocess.check_output(['git','show',pr['merge_commit_sha']+':'+plan['path']]);assert content==path.read_bytes() and h(content)==plan['review_sha256']
prov={'github_pr':number,'owner_login':owner,'merge_commit':pr['merge_commit_sha']};receipt={'verified_at':STAMP,'request':requests[0],**prov,'head':head,'review_sha256':h(content),'checks_sha256':h(checkpath.read_bytes()),'standing_owner_authorization':True,'manual_owner_per_paper_reading_claimed':False};write_json(O/'verified-late-review.json',receipt)
before={i['id']:deepcopy(i) for i in load_items(R)};selected=set(plan['new_ids']);assert all(not before[k].get('review') for k in selected)
oldpub=json.loads((R/'site/daily/2026-11-20.json').read_text());assert len(oldpub['items'])==8;write_json(O/'prior-nov20-manifest.json',oldpub)
oldweek=json.loads((R/'site/weekly/2026-W47.json').read_text());assert len(oldweek['items'])==32;write_json(O/'prior-w47-manifest.json',oldweek)
old23=(R/'site/daily/2026-11-23.json').read_bytes();oldprov=json.loads((R/'data/feed/review-provenance/2026-11-20.json').read_text());write_json(O/'prior-nov20-provenance.json',oldprov)
full=yaml.safe_load(content);subset=deepcopy(full);subset['items']=[x for x in full['items'] if x['id'] in selected];subset['lab_updates']=[];assert len(subset['items'])==3
try:
 path.write_text(yaml.safe_dump(subset,allow_unicode=True,sort_keys=False,width=110));changed=apply_daily_review(R,'2026-11-20',now=STAMP,provenance=prov);assert changed==3
 assert apply_daily_review(R,'2026-11-20',now=STAMP,provenance=prov)==0
finally:path.write_bytes(content)
after={i['id']:i for i in load_items(R)};assert all(after[k]==v for k,v in before.items() if k not in selected);assert all(after[k]['first_seen']==v['first_seen'] and source_hash(after[k])==source_hash(v) for k,v in before.items());write_json(R/'data/feed/review-provenance/2026-11-20.json',{**requests[0],**prov})
publish_day(R,'2026-11-20',now=STAMP,client=None);p=R/'site/daily/2026-11-20.json';day=json.loads(p.read_text());assert len(day['items'])==10 and day['published_at']==oldpub['published_at']
for key in ['sources','collection_observed_at']:day[key]=deepcopy(oldpub[key])
day['review_provenance']={**requests[0],**prov};day['review_provenance_history']=[oldprov];day['late_source_addendum']={'observed_at':STAMP,'source':'github_monitor_issues','issue_numbers':[160,162,163],'new_source_ids':sorted(selected),'accepted_ids':sorted(k for k in selected if after[k]['review']['decision']=='accept'),'source_publication_date':'2026-11-20','reviewed_on':'2026-11-23','report':'docs/internal/reports/maintenance-2026-11-23/late-issues/primary-review.json'}
day['intro']['zh']+=' 本期于11/23审核并补刊；HF论文按实际推荐日，其他论文按真实来源窗口归期。晚到监控另发现SIR-Agent与RemoteEvolver，均按11/20来源日纳入；SIR-Agent的混合退化场景计数对应仍待核，摘要未复述该数字。'
day['intro']['en']+=' Reviewed and published late on Nov 23. HF papers retain their observed recommendation dates; other papers retain their actual source windows. Late monitoring added SIR-Agent and RemoteEvolver to their Nov 20 source window. The SIR-Agent mixed-degradation scenario count remains unverified and is not repeated in its summary.'
write_json(p,day)
validate_weekly_picks(R,'2026-W47');daily=daily_editions_for_week(R,'2026-W47');public=list({x['id']:deepcopy(x) for e in daily for x in e['items']}.values());assert len(public)==34
weekly=deepcopy(oldweek);weekly['items']=public;directions=_directions(yaml.safe_load((R/'feed/taxonomy.yaml').read_text()));weekly['counts']={k:sum(x['direction']['primary']==k for x in public) for k in directions};weekly['intro']=_summary_intro('2026-W47',weekly['counts'],directions,public);weekly['updated_at']=STAMP;weekly['daily_review_provenance']=[x['review_provenance'] for x in daily if x.get('review_provenance')];weekly['metrics']=_metrics(R,'2026-W47',list(after.values()),[after[x['id']] for x in public],STAMP);weekly['metrics']['latency_days']=None
weekly['editor_note_zh']=oldweek['editor_note_zh'].replace('含32篇','含34篇')+' 晚到监控补充的SIR-Agent与RemoteEvolver按11/20来源日归期，11/23复审；SIR-Agent的混合退化场景计数对应仍待核。'
weekly['editor_note_en']=oldweek['editor_note_en'].replace('contain 32 papers','contain 34 papers')+' Late monitor additions SIR-Agent and RemoteEvolver retain their Nov 20 source date and Nov 23 review date; the SIR-Agent mixed-degradation scenario count remains unverified.'
assert weekly['backlog']==oldweek['backlog'] and len(weekly['backlog'])==33 and weekly['published_at']==oldweek['published_at'];write_json(R/'site/weekly/2026-W47.json',weekly)
metrics=R/'data/feed/metrics.json';m=json.loads(metrics.read_text());m['weeks']['2026-W47']['latency_days']=None;write_json(metrics,m)
initialize_public(R);assert (R/'site/daily/2026-11-23.json').read_bytes()==old23
base=R/'docs/internal/reports/maintenance-2026-11-23/backlog-audit/post-publication/backlog-ledger.jsonl.gz';overlay={'observed_at':STAMP,'base_ledger':str(base.relative_to(R)),'base_ledger_sha256':h(base.read_bytes()),'base_ids':9292,'added_ids':3,'current_ids':9295,'canonical_count':2459,'previous_234_snapshot_preserved':True,'combined_current_run_decisions':{'new_canonical':237,'accept_daily':27,'historical_additions':4,'reject':203,'defer':3},'rows':[{'id':k,'issue':{'arxiv:2611.27285':160,'arxiv:2611.27110':162,'arxiv:2611.27006':163}[k],'decision':after[k]['review']['decision'],'review':after[k]['review'],'state':'ready_for_publication' if after[k]['review']['decision']=='accept' else 'formal_scope_exclusion','specific_follow_up':'Unverified abstract scenario-count mapping remains tracked in issue 160; public summary has no such claim.' if k.endswith('27285') else 'Reopen only with new source evidence affecting the scope decision.','online_verified':False} for k in sorted(selected)]};write_json(O/'backlog-overlay.json',overlay)
write_json(O/'generation-receipt.json',{'generated_at':STAMP,'review':receipt,'applied_ids':sorted(selected),'application_count':3,'second_apply_changed':0,'old_canonical_rows_unchanged':True,'all_source_hashes_and_first_seen_preserved':True,'nov20_count':10,'w47_daily_count':34,'w47_prior_historical_count':33,'nov23_status_snapshot_unchanged':True,'w47_latency_days':None,'paid_requests':0,'generation_tokens':0,'online_verified':False,'boundary':'Local artifacts only until publication PR, Pages and exact public-byte verification.'})
shutil.copyfile(Path(__file__),O/'apply-late-review-and-render.py');print(json.dumps({'applied':3,'nov20_count':10,'w47':34,'old_records_unchanged':True,'source_hashes_and_first_seen_preserved':True,'online_verified':False}))
