from pathlib import Path
from datetime import datetime, timezone
from copy import deepcopy
import json, yaml, hashlib, gzip, shutil, collections
from scripts.feed.storage import load_items
from scripts.feed.review import _review_row, source_hash, validate_daily_review
from scripts.feed.window import daily_metadata
from scripts.feed.dates import daily_section
from scripts.feed.guard import check_summary, unknown_evidence

R=Path.cwd(); B=R/'build/maintenance-2026-11-23'; D=R/'docs/internal/reports/maintenance-2026-11-23'
P=D/'primary-review'; P.mkdir(exist_ok=True); O=B/'reviews'; O.mkdir(exist_ok=True)
def digest(b):return hashlib.sha256(b).hexdigest()
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
items={x['id']:x for x in load_items(R)}
reports={};indices=[]
for kind in ('hf','other'):
    src=Path(f'/private/tmp/follow-rsi-2026-11-23-{kind}-review')
    dst=D/f'independent-{kind}';dst.mkdir(exist_ok=True)
    raw=R/f'data/feed/raw/maintenance-2026-11-23/independent-{kind}'
    names=['final.json'] if kind=='hf' else ['final.json','amendments-v1.json','final-resolved.json','verification.json']
    for name in names:shutil.copyfile(src/name,dst/name)
    report=json.loads((dst/('final.json' if kind=='hf' else 'final-resolved.json')).read_text());reports[kind]=report
    index=[]
    for p in sorted((src/'sources').iterdir()):
        if not p.is_file():continue
        content=p.read_bytes();target=raw/(p.name+'.gz');target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(gzip.compress(content,mtime=0))
        index.append({'original_path':str(p),'archive':str(target.relative_to(R)),'original_sha256':digest(content),'archive_sha256':digest(target.read_bytes()),'bytes':len(content)})
    write(dst/'source-storage-index.json',index);indices.extend(index)
    for p in src.glob('input*.json'):
        target=raw/(p.name+'.gz');target.write_bytes(gzip.compress(p.read_bytes(),mtime=0))

rows=[]
summary_changes={
'arxiv:2611.23774':('在单个episode内依据导航反馈修订策略代码与改进规则，供后续目标复用；独立episode重置。','Within each episode, navigation feedback revises policy code and improvement rules for later goals; independent episodes reset both.'),
'arxiv:2611.22525':('重放环境检查修订过期技能，验收后复用；当前实验只验证一次维护事件。','Environment-check replay guides repairs to stale reusable skills; the experiments evaluate one maintenance event.'),
'arxiv:2611.26007':('联合修订决策模型、状态提示与行为树后测试新对手；未隔离固定权重下的控制器效果。','Decision-model, state-prompt and behavior-tree updates are tested on new opponents; a fixed-weight controller effect is not isolated.'),
'arxiv:2611.23651':('在模拟个人助理环境中从失败轨迹修订指令，经验证与独立采纳决策后用于未来任务。','In a simulated personal-assistant setting, failure traces guide instruction repairs for future tasks, with validation separated from adoption.'),
}
for kind,report in reports.items():
    for r in report['items']:
        item=items[r['id']];decision=r['decision'];action='apply'
        day=(item.get('hf_daily_dates') or [str(item.get('updated') or item.get('published'))[:10]])[-1]
        reason=r['reason_zh'];sm=None;direction=None
        if decision=='accept':
            sm={k:r[k] for k in ('summary_zh','summary_en')};direction=r['direction']
            if item['id'] in summary_changes:sm=dict(zip(('summary_zh','summary_en'),summary_changes[item['id']]))
            if r.get('publication_action')=='metadata_receipt_only':
                decision='defer';action='metadata_receipt_only';sm=None;direction=None
                reason+=' 本行defer只阻止重复出版，不撤回既有accept，也不把旧科学批准改绑新hash。'
            elif day<'2026-11-18':decision='backlog';day='2026-11-23'
        if day not in ('2026-11-18','2026-11-19','2026-11-20','2026-11-23'):day='2026-11-23'
        if r['id']=='arxiv:2611.26414':
            reason='ZeroVLN使用固定慢快导航框架，并通过RL训练脑模型和动作策略；未证明执行反馈会修订并保留外部提示、工具或控制机制。原独立理由的“冻结VLM”措辞不准确，原文明确jointly improve与minor weight changes，故在此纠正，排除结论不变。'
        limits=r.get('limitations_zh',r.get('limitations',[]));reason+=' '+' '.join(limits)
        missing=r.get('missing_evidence',[])
        if decision=='defer' and action=='apply':reason+=' 待补：'+json.dumps(missing,ensure_ascii=False)+' '+r.get('next_step_zh','')
        rows.append({'id':item['id'],'edition_date':day,'reviewed_on':'2026-11-23','source_hash':source_hash(item),'decision':decision,'application':action,'direction':direction,'summary_override':sm,'reason':reason.strip(),'review_source':str((D/f'independent-{kind}'/('final.json' if kind=='hf' else 'final-resolved.json')).relative_to(R)),'evidence':deepcopy(r),'evidence_quick':unknown_evidence()})
assert len(rows)==236 and len({x['id'] for x in rows})==236
assert collections.Counter(r['decision'] for r in rows)=={'accept':25,'backlog':4,'reject':202,'defer':5}
corrections=json.loads((D/'independent-backlog/version-corrections.json').read_text())
for r in corrections['items']:
    item=items[r['id']]
    assert source_hash(item)==r['source_hash_after']
    rows.append({'id':item['id'],'edition_date':'2026-11-23','reviewed_on':'2026-11-23','source_hash':source_hash(item),'decision':'defer','application':'version_metadata_only','direction':None,'summary_override':None,'reason':'历史目录版本/文字纠正：官方v2身份、摘要和限制已核实；原版本存入version_history，first_seen和原范围状态保留。本行批准纠正记录，不声称新论文纳入，也不替代未来完整科学准入。详见独立backlog报告。','review_source':str((D/'independent-backlog/version-corrections.json').relative_to(R)),'evidence':r,'evidence_quick':unknown_evidence()})
queues={day:{'date':day,'reviewed_on':'2026-11-23','items':[],'lab_updates':[]} for day in ('2026-11-18','2026-11-19','2026-11-20','2026-11-21','2026-11-23')}
checks=[]
for r in rows:
    item=items[r['id']];day=r['edition_date'];timing=daily_metadata(R,item,day)
    row=_review_row(item);row.update(timing);row['daily_section']=daily_section({**item,**timing},day)
    row.update(decision=r['decision'],promote_to_repo=False,evidence_quick=r['evidence_quick'],evidence_notice='三轮来源与范围交叉审查；未实验复现。',note=r['reason']+' 三轮证据见 docs/internal/reports/maintenance-2026-11-23/primary-review/final-adjudication.json。')
    if r['summary_override']:
        row.update(summary_override=r['summary_override'],direction_override=r['direction'])
        g=check_summary(item['title'],item.get('abstract',''),**r['summary_override']);assert g['ok'],(item['id'],g)
        checks.append({'id':item['id'],'guard':g,'summary_contains_numeric_claims':False})
    queues[day]['lab_updates' if item['kind'] in ('post','release') else 'items'].append(row)
validation=[]
for day,q in queues.items():
    data=yaml.safe_dump(q,allow_unicode=True,sort_keys=False,width=110).encode();(O/f'{day}.yaml').write_bytes(data)
    p=R/f'review/daily/{day}.yaml';prior=p.read_bytes() if p.exists() else None
    if prior: (P/f'prior-review-{day}.yaml').write_bytes(prior)
    try:p.write_bytes(data);validate_daily_review(R,day)
    finally:
        if prior is None:p.unlink()
        else:p.write_bytes(prior)
    validation.append({'date':day,'reviewed_on':'2026-11-23','path':str(p.relative_to(R)),'items':len(q['items']),'lab_updates':len(q['lab_updates']),'counts':dict(collections.Counter(x['decision'] for x in q['items']+q['lab_updates'])),'sha256':digest(data),'apply_ids':[x['id'] for x in rows if x['edition_date']==day and x['application']=='apply'],'metadata_only_ids':[x['id'] for x in rows if x['edition_date']==day and x['application']!='apply']})
shutil.copyfile(O/'2026-11-23.yaml',R/'review/daily/2026-11-23.yaml')
sample_ids=['arxiv:2611.27193','arxiv:2611.26414','arxiv:2611.00911','arxiv:2611.24651','arxiv:2611.23499','arxiv:2611.21152','arxiv:2611.24077','arxiv:2611.27804','arxiv:2611.23067','arxiv:2611.24697','arxiv:2611.23346','arxiv:2503.14499','arxiv:2611.27780','arxiv:2611.24395','post:https://openai.com/business/learn/daybreak-blue-onboarding-demo']
write(P/'final-adjudication.json',{'generated_at':datetime.now(timezone.utc).isoformat(),'reviewed_on':'2026-11-23','reviewer':'Parent Codex under standing owner authorization; no claim of manual owner per-paper reading','round1':'Full stable ID/raw/canonical reconciliation plus official arXiv identities and dates.','round2':'Parent read the positive and boundary source quotations, update objects, feedback and reuse; corrected limits and source windows.','round3':'Independent HF, other-source and historical backlog reviews archived with exact source bytes and preserved contrary opinions.','parent_exclusion_spotchecks':sample_ids,'parent_corrections':['ZeroVLN reason does not call its jointly RL-trained brain frozen.','Great Listeners external action-gate search accepted after independent table verification.','Explicit within-episode, single-maintenance-event, simulated-environment and confounded-controller limits added to summaries.'],'counts':dict(collections.Counter(x['decision'] for x in rows)),'new_intake_counts':{'total':234,'accept_daily':25,'historical_backlog':4,'reject':202,'defer':3},'metadata_only_existing_hf':2,'historical_version_corrections':2,'per_date':validation,'summary_guards':checks,'scope_review_not_replication':True,'paid_model_calls':0,'paid_tokens':0,'global_quality_warning':{'recall':0.892857,'threshold':0.90,'complete':False,'rerun':False},'items':rows})
write(B/'review-preflight.json',{'reviews':validation})
print(json.dumps([{k:v for k,v in x.items() if not k.endswith('_ids')} for x in validation],ensure_ascii=False))
