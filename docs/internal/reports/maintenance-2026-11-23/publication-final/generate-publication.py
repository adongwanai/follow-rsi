"""Compile reviewed editions from real merged date PRs and frozen prior publications."""
from pathlib import Path
from datetime import datetime, timezone
from copy import deepcopy
import json, yaml, hashlib, gzip, shutil, subprocess, os
from scripts.feed.ci import merged_review_requests, human_owner_review
from scripts.feed.review import apply_daily_review, source_hash, approved_weekly_backlog, validate_weekly_picks, daily_editions_for_week
from scripts.feed.digest import publish_day, render_recap, initialize_public, _public_item, _directions, _summary_intro, _metrics
from scripts.feed.storage import load_items,save_items,write_json

R=Path.cwd();B=R/'build/maintenance-2026-11-23';D=R/'docs/internal/reports/maintenance-2026-11-23';OUT=D/'publication-final';OUT.mkdir(exist_ok=True)
STAMP=datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z');REPO='adongwanai/follow-rsi';ENV={**os.environ,'GODEBUG':'http2client=0'}
def digest(b):return hashlib.sha256(b).hexdigest()
def gh(*args):return json.loads(subprocess.check_output(['gh',*args],env=ENV,text=True))
def verify(entry):
    n=entry['number'];pr=gh('api',f'repos/{REPO}/pulls/{n}');assert pr['merged'] and pr['base']['ref']=='main' and pr['head']['sha']==entry['head']
    pages=gh('api','--paginate','--slurp',f'repos/{REPO}/pulls/{n}/files?per_page=100');files=[r for p in pages for r in p];assert len(files)==pr['changed_files']
    req=merged_review_requests({'pull_request':pr},[r['filename'] for r in files],REPO);assert len(req)==1 and req[0]['path']==entry['path']
    owner=human_owner_review(pr,[],REPO)
    cp=B/f'pr-audit/pr-{n}-checks.json';checks=json.loads(cp.read_text());assert checks['head']==entry['head']
    for name in ('build','validate'):
        found=[r for r in checks['checks']['check_runs'] if r['name']==name];assert found and max(found,key=lambda r:r['id'])['conclusion']=='success'
    found=[r for r in checks['statuses']['statuses'] if r['context']=='Follow RSI owner decisions'];assert found and max(found,key=lambda r:r['id'])['state']=='success'
    content=subprocess.check_output(['git','show',pr['merge_commit_sha']+':'+entry['path']]);assert digest(content)==entry['sha256'] and content==(R/entry['path']).read_bytes()
    receipt={'request':req[0],'github_pr':n,'head':entry['head'],'owner_login':owner,'merge_commit':pr['merge_commit_sha'],'review_sha256':digest(content),'verified_at':STAMP,'check_receipt_sha256':digest(cp.read_bytes()),'authorization':'Standing owner authorization; not a claim of manual owner per-paper reading.'}
    write_json(OUT/f'verified-review-{n}.json',receipt);write_json(OUT/f'pr-{n}-files.json',files)
    return receipt,content
def prov(r):return {k:r[k] for k in ('github_pr','owner_login','merge_commit')}

assert not (OUT/'generation-receipt.json').exists(),'Do not repeat application; render stored manifests instead.'
plan=json.loads((B/'created-review-prs.json').read_text())
day22={'number':145,'head':'793c83229490ac464d296b5de6d137cf6581ce0d','path':'review/daily/2026-11-22.yaml','sha256':digest((R/'review/daily/2026-11-22.yaml').read_bytes()),'date':'2026-11-22','apply_ids':[],'metadata_only_ids':[]}
week={'number':146,'head':'7d34dc3bc03e4c0aa26aa0324fcdb2e3151d60ce','path':'review/2026-W47.yaml','sha256':digest((R/'review/2026-W47.yaml').read_bytes())}
verified={}
for e in [*plan,day22,week]:verified[e['number']]=(*verify(e),e)
before={x['id']:deepcopy(x) for x in load_items(R)};prior={str(p.relative_to(R)):digest(p.read_bytes()) for f in ('daily','weekly','recaps') for p in (R/'site'/f).glob('*.json')}
old18=R/'site/daily/2026-11-18.json';write_json(OUT/'prior-nov18-observed-status.json',json.loads(old18.read_text()))
write_json(OUT/'prior-canonical-boundaries.json',{k:{'source_hash':source_hash(v),'first_seen':v['first_seen']} for k,v in before.items()})
adjud=json.loads((D/'primary-review/final-adjudication.json').read_text());byid={r['id']:r for r in adjud['items']}
for e in sorted(plan,key=lambda x:x['date']):
    receipt,content,_=verified[e['number']];selected=set(e['apply_ids']);path=R/e['path'];full=yaml.safe_load(content);subset=deepcopy(full)
    for group in ('items','lab_updates'):subset[group]=[r for r in full[group] if r['id'] in selected]
    assert {r['id'] for r in subset['items']+subset['lab_updates']}==selected
    histories=[]
    for key in selected:
        old=deepcopy(before[key])
        if old.get('review'):
            if old['review'] not in old.setdefault('review_history',[]):old['review_history'].append(deepcopy(old['review']))
            histories.append(old)
    save_items(R,histories)
    try:
        path.write_text(yaml.safe_dump(subset,allow_unicode=True,sort_keys=False,width=110));changed=apply_daily_review(R,e['date'],now=STAMP,provenance=prov(receipt))
    finally:path.write_bytes(content)
    write_json(OUT/f'applied-{e["date"]}.json',{'applied':changed,'ids':sorted(selected),'receipt':receipt})
    assert changed==len(selected)
for e in [*plan,day22]:
    receipt=verified[e['number']][0];write_json(R/f'data/feed/review-provenance/{e["date"]}.json',{**receipt['request'],**prov(receipt)})
    for key in e['metadata_only_ids']:
        item=deepcopy(before[key]);r=byid[key]
        meta={**prov(receipt),'kind':r['application'],'date':e['date'],'reviewed_on':'2026-11-23','source_hash':source_hash(item),'previous_approval_source_hash':item.get('review',{}).get('source_hash'),'scientific_review_preserved':True,'scientific_content_reapproved':False,'republished':False,'note':r['reason']}
        item.setdefault('metadata_review_receipts',[]).append(meta);save_items(R,[item]);write_json(OUT/('metadata-'+key.replace(':','-')+'.json'),meta)
snapshot=json.loads((R/'data/feed/raw/maintenance-2026-11-23/source-intake/all-source-snapshot.json').read_text())
state=json.loads((R/'data/feed/state.json').read_text());write_json(OUT/'source-state-before.json',state);public_sources={};fetch=[]
boards={'2026-11-18':39,'2026-11-19':50,'2026-11-20':50,'2026-11-21':0,'2026-11-22':0,'2026-11-23':13}
for s in snapshot['sources']:
    key=s['source_id'];ok=s['status']=='ok';avail='available' if ok else 'partial' if s['status']=='partial' else 'failed';r=state['sources'][key]
    r.update(last_count=s['configured_window_records'],last_run=s['finished_at'],last_ok=ok,last_error=s['error'],availability=avail,degraded=not ok)
    if ok:r.update(last_success=s['finished_at'],consecutive_errors=0,consecutive_failures=0)
    else:
        r['consecutive_errors']=r.get('consecutive_errors',0)+1;r['consecutive_failures']=r.get('consecutive_failures',0)+1
    if key=='hf-daily':r.update(today_board_status='available',today_board_count=13,available_through=None,boards=boards)
    public_sources[key]={'count':s['configured_window_records'],'run_at':s['finished_at'],'error':s['error'],'availability':avail}
    fetch.append({k:s[k] for k in ('source_id','started_at','finished_at','request_count','http_status_counts','source_traversal_complete','error')}|{'ok':ok,'count':s['configured_window_records'],'availability':avail,'degraded':not ok})
state['last_fetch']={'run_at':snapshot['generated_at'],'sources':fetch,'snapshot':'data/feed/raw/maintenance-2026-11-23/source-intake/all-source-snapshot.json','report':'docs/internal/reports/maintenance-2026-11-23/source-intake/README.md'}
state['last_hf_supplement']={'observed_at':snapshot['generated_at'],'boards':boards,'available_through':None,'reconciliation_report':'docs/internal/reports/maintenance-2026-11-23/source-intake/hf-board-reconciliation.json'};write_json(R/'data/feed/state.json',state)
zh='11/23北京时间15:53–15:58实际尝试全部12路启用来源；原始4684次出现对应4416个稳定ID，来源窗口内520次出现、471个ID，新增规范记录234条（213篇论文、21篇公告）。三路arXiv窗口分别15、17、2条；五路RSS分别9、7、49、7、0条；13个GitHub仓库release查询均成功，窗口0条。S2 citations共47次请求含19次429，到180秒截止时保留262次窗口出现；authors为8次请求含6次429，仅身份查询部分成功，论文遍历未完成，未访问覆盖仍unknown。'
en='All 12 enabled sources were attempted on Nov 23 at 15:53–15:58 Asia/Shanghai. There were 4,684 raw occurrences across 4,416 stable IDs; 520 window occurrences across 471 IDs added 234 canonical records (213 papers and 21 posts). The three arXiv queries yielded 15, 17 and 2 window records; the five RSS feeds yielded 9, 7, 49, 7 and 0. Release queries succeeded for all 13 GitHub repositories with no window release. S2 citations made 47 requests including 19 rate limits and retained 262 window occurrences before the 180-second cutoff; authors made eight requests including six rate limits, with only partial identity lookup and unfinished paper traversal. Unvisited coverage remains unknown.'
endzh='三轮逐项意见为29篇纳入（25篇按11/18–20真实窗口补刊，4篇历史补录）、202条排除、3条待补。待补为EVA-RSI的实际Harness修改链、DailyBrick跨配置部署链、仅S2截断摘要的综述原文；旧6项外部证据阻塞继续逐项保留。旧全局质量评测recall 0.892857、阈值0.90且未完整结束；没有改阈值或声称通过。付费模型请求0、生成token 0，范围审核不是实验复现。'
enden='Item-specific three-round review yields 29 inclusions (25 in delayed Nov 18–20 editions and four historical additions), 202 exclusions and three evidence deferrals. EVA-RSI needs a demonstrated Harness-edit chain, DailyBrick needs a deployed cross-configuration update, and the S2-only survey needs its full text. Six older external evidence gaps remain itemized. Historical global evaluation has not finished; recall is 0.892857 versus 0.90, without a threshold change or pass claim. Paid model requests and generation tokens are zero; scope review is not experimental replication.'
statuses=json.loads((R/'data/feed/daily-status.json').read_text());assert not any(r['date'] in ('2026-11-21','2026-11-22','2026-11-23') for r in statuses['days'])
for day in ('2026-11-21','2026-11-22','2026-11-23'):
    prefixzh=('本期是11/23审核并补发的状态简报；不冒称当日准时采集。11/23复抓本刊期HF完整榜单返回0条，这只是该时刻榜单快照，不表示所有来源无更新。' if day!='2026-11-23' else '截至11/23采集快照，当日HF完整榜单13篇均经范围审查排除，本期无合格当日论文。已同时复抓11/18–22全榜，分别39、50、50、0、0篇；旧榜正例按原推荐日补刊，不顺延冒充今天。')
    prefixen=('This status bulletin was reviewed and published late on Nov 23, not collected on its edition date. The complete HF board for this edition returned zero on Nov 23. That is an observed board snapshot, not evidence that every source had no update. ' if day!='2026-11-23' else 'At the Nov 23 snapshot, all 13 papers on the complete same-day HF board were excluded after scope review; no same-day paper qualifies. Complete Nov 18–22 boards were also fetched (39, 50, 50, 0 and 0 papers). Qualifying earlier papers retain their recommendation dates rather than being presented as today’s discoveries. ')
    statuses['days'].append({'date':day,'reviewed_on':'2026-11-23','checked_at':snapshot['generated_at'],'status':'no_qualified_content','reason_zh':prefixzh+zh+endzh,'reason_en':prefixen+en+enden,'hf_snapshot':{'observed_on':'2026-11-23','count':boards[day]},'source_snapshot':'data/feed/raw/maintenance-2026-11-23/source-intake/all-source-snapshot.json','collection_report':'docs/internal/reports/maintenance-2026-11-23/primary-review/final-adjudication.json','paid_generation_requests':0,'paid_generation_tokens':0})
statuses['updated_at']=STAMP;write_json(R/'data/feed/daily-status.json',statuses)
generation=[]
for day in ('2026-11-18','2026-11-19','2026-11-20','2026-11-21','2026-11-22','2026-11-23'):
    result=publish_day(R,day,client=None,now=STAMP,allow_status=True);p=R/f'site/daily/{day}.json';edition=json.loads(p.read_text());edition['sources']=deepcopy(public_sources);edition['collection_observed_at']=snapshot['generated_at'];edition['review_provenance']=json.loads((R/f'data/feed/review-provenance/{day}.json').read_text())
    if day<='2026-11-20':
        expected={'2026-11-18':7,'2026-11-19':10,'2026-11-20':8}[day];assert len(edition['items'])==expected
        edition['intro']['zh']+=' 本期于11/23审核并补刊；HF论文按实际推荐日，其他论文按真实来源窗口归期。采集发生于11/23，不冒称此前已观察到。'+(' 11/18最初简报记录的not_ready为当时真实快照，原记录保存在本次审计中；本次是后续补抓更新。' if day=='2026-11-18' else '')
        edition['intro']['en']+=' Reviewed and published late on Nov 23. HF papers retain their observed recommendation dates; other papers retain their true source windows. Sources were collected on Nov 23.'+(' The initial Nov 18 not_ready bulletin was truthful at its snapshot and is preserved in the audit; this is a later collection update.' if day=='2026-11-18' else '')
    else:assert edition['kind']=='daily_status' and not edition['items']
    write_json(p,edition);result['manifest']=str(Path(result['manifest']).relative_to(R));generation.append(result)

# W47 compiles exact previously published records. The SIM metadata-only HF addition
# must not rebind its old science approval or force a second backlog approval.
wr=verified[146][0];validate_weekly_picks(R,'2026-W47');write_json(R/'data/feed/review-provenance/2026-W47.json',{**wr['request'],**prov(wr)})
daily=daily_editions_for_week(R,'2026-W47');public=list({x['id']:deepcopy(x) for e in daily for x in e['items']}.values());assert len(public)==32
frozen_path=R/'site/recaps/2026-11-16--2026-11-18.json';frozen=json.loads(frozen_path.read_text());assert digest(frozen_path.read_bytes())==prior[str(frozen_path.relative_to(R))] and len(frozen['items'])==33
backlog=[{**deepcopy(x),'window_status':'backlog','daily_section':'historical','edition_kind':'weekly_backlog'} for x in frozen['items']]
assert not ({r['id'] for r in public}&{r['id'] for r in backlog})
directions=_directions(yaml.safe_load((R/'feed/taxonomy.yaml').read_text()));counts={k:sum(r['direction']['primary']==k for r in public) for k in directions};picks=yaml.safe_load((R/'review/2026-W47.yaml').read_text())
weekly={'week':'2026-W47','start':'2026-11-16','end':'2026-11-22','published_at':STAMP,'reviewed_only':True,'items':public,'backlog':backlog,'counts':counts,'picks':picks['picks'],'editor_note_zh':'本周日报含32篇；11/18–20补刊于11/23完成审核。另列33篇此前已发布的历史补录，保留当时审核与来源快照，不计为本周新论文。','editor_note_en':'Daily editions contain 32 papers; Nov 18–20 supplements were reviewed on Nov 23. A separate section preserves 33 previously published historical additions and their original review/source snapshots; these are not new papers this week.','lab_updates':[],'intro':_summary_intro('2026-W47',counts,directions,public),'review_provenance':{**wr['request'],**prov(wr)},'daily_review_provenance':[e.get('review_provenance') for e in daily if e.get('review_provenance')],'historical_snapshot_provenance':{'manifest':str(frozen_path.relative_to(R)),'sha256':digest(frozen_path.read_bytes()),'prior_review_provenance':frozen.get('review_provenance'),'policy':'Already published, frozen scientific snapshots; added HF metadata does not rebind old reviews.'},'metrics':_metrics(R,'2026-W47',load_items(R),[before[x['id']] for x in public],STAMP)}
write_json(R/'site/weekly/2026-W47.json',weekly);generation.append({'week':'2026-W47','accepted':32,'historical_previously_published':33,'manifest':'site/weekly/2026-W47.json'})
repo=yaml.safe_load((R/'data/papers.yaml').read_text())['papers'];backlog_new=approved_weekly_backlog(R,'2026-W48');assert len(backlog_new)==4
public_new=[{**_public_item(x,{'decision':'backlog'},'2026-W48',repo),'review_date':x['review']['reviewed_on'],'window_status':'backlog'} for x in backlog_new]
recap={'start':'2026-11-23','end':'2026-11-23','published_at':STAMP,'title_zh':'历史补录 · 11 月 23 日审核','title_en':'Historical additions reviewed November 23','reviewed_only':True,'items':public_new,'lab_updates':[],'picks':[],'sources':public_sources,'reviewed_on':'2026-11-23','review_provenance':verified[next(x['number'] for x in plan if x['date']=='2026-11-23')][0],'intro':{'zh':'本次单列4篇较早论文；11/23是实际审核与补录日，不是论文发表日，也不计为11/23当日新增论文。技能评测协议尚无结果、技能维护仅验证一次事件等限制均保留。','en':'Four earlier papers are listed separately. Nov 23 is the actual review and retrospective-publication date, not their publication date or a same-day discovery claim. Limits, including pending benchmark results and a single maintenance event, remain explicit.','source':'source-bound-editorial-review'}}
from scripts.feed.health import update_health
update_health(R,[],now=snapshot['generated_at'])
result=render_recap(R,recap);generation.append({k:(str(Path(v).relative_to(R)) if k in ('manifest','html') else v) for k,v in result.items()});initialize_public(R)
after={x['id']:x for x in load_items(R)};assert len(after)==len(before)
assert all(after[k]['first_seen']==v['first_seen'] and source_hash(after[k])==source_hash(v) for k,v in before.items())
for key in ('arxiv:2611.18856','arxiv:2611.21373'):assert before[key]['review']==after[key]['review']
for p,sha in prior.items():
    if p!='site/daily/2026-11-18.json':assert digest((R/p).read_bytes())==sha,p
assert not (R/'site/daily/2026-10-27.json').exists()
shutil.copyfile('/private/tmp/follow-rsi-2026-11-23-publication-crosscheck.json',OUT/'independent-publication-crosscheck.json')
write_json(OUT/'generation-receipt.json',{'generated_at':STAMP,'generation':generation,'canonical_count':len(after),'first_seen_and_scientific_source_hashes_unchanged_during_apply':True,'old_hf_scientific_reviews_preserved':True,'prior_nov18_status_archived':True,'paid_generation_requests':0,'paid_generation_tokens':0,'quality_warning':{'recall':0.892857,'threshold':0.90,'complete':False},'online_verified':False,'boundary':'Local generation from verified merged reviews. Publication PR, Pages and public byte verification still required.'})
print(json.dumps(generation,ensure_ascii=False),flush=True)
