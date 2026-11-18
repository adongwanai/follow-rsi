from pathlib import Path
import json, yaml, hashlib, copy, collections
from datetime import datetime, timezone
from scripts.feed.storage import load_items
from scripts.feed.review import _review_row, source_hash, validate_daily_review
from scripts.feed.window import daily_metadata
from scripts.feed.dates import daily_section
from scripts.feed.guard import check_summary, unknown_evidence
R=Path.cwd(); D=R/'docs/internal/reports/maintenance-2026-11-18'; B=R/'build/maintenance-2026-11-18'
P=D/'primary-review'; P.mkdir(exist_ok=True); O=B/'reviews'; O.mkdir(exist_ok=True)
items={x['id']:x for x in load_items(R)}
paths={'hf16':D/'independent-hf16/independent-review-v1.json','hf17':D/'independent-hf17/final-scope-review.json','other':D/'independent-other/review-findings.json','amendment':D/'independent-other/amendment-spg-wevis.json'}
hf16=json.loads(paths['hf16'].read_text())['items']; hf17=json.loads(paths['hf17'].read_text())['records']; other=json.loads(paths['other'].read_text())['items']; amend=json.loads(paths['amendment'].read_text())['amendments']
for a in amend:
    r=next(x for x in other if x['id']==a['id'])
    for k in ['suggestion','reason_zh','summary_zh','summary_en','missing_evidence_zh','limitations_zh']:
        if k in a:r[k]=copy.deepcopy(a[k])
    r['post_freeze_amendment']=a
rows=[]
for r in hf16:
    item=items[r['id']]; decision=r['recommendation']; action='apply'
    if decision=='reuse_existing':
        if r['id']=='arxiv:2611.12068':decision='accept'
        elif r['id']=='arxiv:2611.13509':decision='reject'
        else:decision='defer';action='metadata_receipt_only'
    reason=r.get('reason_zh',r.get('note_zh'))
    sm=r.get('summary_proposal');direction={'primary':r.get('suggested_primary'),'secondary':r.get('suggested_secondary',[]),'harness_sub':r.get('harness_sub')}
    if r['id']=='arxiv:2611.12068':
        sm=copy.deepcopy(item['review']['summary_override']);direction=copy.deepcopy(item['review']['direction_override']);reason='复用已核实的 AutoDream 程序技能分支审查；补记实际观察的11/16 HF推荐日。这是此前发现论文的首次正式出版，不是新增发现。原批准范围、摘要、first_seen保留，旧回执进入history；新增推荐日用本次日期PR批准。'
    if action=='metadata_receipt_only':reason='仅核实追加11/16 HF推荐日期；科学字段与原11/12已刊条目不变，不重复出版，不把此defer视为撤回旧accept，不将旧批准改绑新hash。追加本次metadata-only回执，原review完整保留。'
    rows.append({'id':r['id'],'edition_date':'2026-11-16','reviewed_on':'2026-11-18','source_hash':source_hash(item),'decision':decision,'application':action,'direction':direction if decision=='accept' else None,'summary_override':sm,'reason':reason,'evidence':copy.deepcopy(r),'review_source':str(paths['hf16'].relative_to(R)),'evidence_quick':unknown_evidence()})
for r in hf17:
    rows.append({'id':r['id'],'edition_date':'2026-11-17','reviewed_on':'2026-11-18','source_hash':source_hash(items[r['id']]),'decision':'reject','application':'apply','direction':None,'summary_override':None,'reason':r['reason_zh'],'evidence':copy.deepcopy(r),'review_source':str(paths['hf17'].relative_to(R)),'evidence_quick':unknown_evidence()})
for r in other:
    item=items[r['id']];decision={'include':'accept','reject':'reject','defer':'defer'}[r['suggestion']]
    if decision=='accept':
        day='2026-11-16' if daily_metadata(R,item,'2026-11-16')['window_status']=='in_window' else '2026-11-18'
        if day=='2026-11-18':decision='backlog'
    else:day='2026-11-18'
    direction={'primary':r['primary'],'harness_sub':r['harness_sub'],'secondary':['harness'] if r['primary']=='evaluation_benchmark' else ['embodied'] if r['harness_sub']=='coevolution' and r['id']=='arxiv:2611.19081' else []}
    sm={k:r[k] for k in ['summary_zh','summary_en']} if decision in ['accept','backlog'] else None
    rows.append({'id':r['id'],'edition_date':day,'reviewed_on':'2026-11-18','source_hash':source_hash(item),'decision':decision,'application':'apply','direction':direction if sm else None,'summary_override':sm,'reason':r['reason_zh']+' '+' '.join(r['limitations_zh'])+(' 待补：'+r['missing_evidence_zh'] if r['suggestion']=='defer' else ''),'evidence':copy.deepcopy(r),'review_source':str(paths['other'].relative_to(R)),'evidence_quick':r.get('evidence_quick',unknown_evidence())})
assert len(rows)==132 and len({r['id'] for r in rows})==132
queues={day:{'date':day,'reviewed_on':'2026-11-18','items':[],'lab_updates':[]} for day in ['2026-11-16','2026-11-17','2026-11-18']}
original=yaml.safe_load((R/'review/daily/2026-11-16.yaml').read_text());queues['2026-11-16']=copy.deepcopy(original)
checks=[]
for r in rows:
    item=items[r['id']];day=r['edition_date'];timing=daily_metadata(R,item,day)
    row=_review_row(item);row.update(timing);row['daily_section']=daily_section({**item,**timing},day);row['decision']=r['decision'];row['note']=r['reason']+' 三轮来源/范围复核见 '+str(P.relative_to(R))+'/final-adjudication.json。未复现实验，未全表重算。';row['promote_to_repo']=False;row['evidence_notice']='逐项来源、身份、日期、范围与摘要交叉核实；不代表实验复现。';row['evidence_quick']=r['evidence_quick']
    if r['summary_override']:
        row['summary_override']=r['summary_override'];row['direction_override']=r['direction'];guard=check_summary(item['title'],item.get('abstract',''),**r['summary_override']);assert guard['ok'],(item['id'],guard);checks.append({'id':item['id'],'guard':guard})
    group='lab_updates' if item['kind'] in ['post','release'] else 'items';queues[day][group].append(row)
validation=[]
for day,q in queues.items():
    data=yaml.safe_dump(q,allow_unicode=True,sort_keys=False,width=110).encode();out=O/f'{day}.yaml';out.write_bytes(data);p=R/f'review/daily/{day}.yaml';prior=p.read_bytes() if p.exists() else None
    try:p.write_bytes(data);validate_daily_review(R,day)
    finally:
        if prior is None:p.unlink()
        else:p.write_bytes(prior)
    validation.append({'date':day,'reviewed_on':'2026-11-18','items':len(q['items']),'lab_updates':len(q['lab_updates']),'counts':dict(collections.Counter(v['decision'] for v in q['items']+q['lab_updates'])),'sha256':hashlib.sha256(data).hexdigest(),'apply_ids':[r['id'] for r in rows if r['edition_date']==day and r['application']=='apply'],'metadata_only_ids':[r['id'] for r in rows if r['edition_date']==day and r['application']=='metadata_receipt_only']})
report={'generated_at':datetime.now(timezone.utc).isoformat(),'reviewer':'parent Codex agent, under standing owner authorization; not a claim of manual owner per-paper reading','round1':'Complete raw/canonical stable ID, identity, dates, first_seen, source hashes and dedup reconciliation; official fulltexts for positive and ambiguous cases.','round2':'Parent read all scope proposals and key original method/evaluation paragraphs; kept feedback object, persistence and experimental limits distinct. SPG and ESI corrections retain original contrary evidence.','round3':'Independent scope reviews and subsequent narrow amendments are bound below. Exact publication draft review follows separately.','source_inputs':{str(v.relative_to(R)):hashlib.sha256(v.read_bytes()).hexdigest() for v in paths.values()},'counts':dict(collections.Counter(r['decision'] for r in rows)),'per_date':validation,'summary_guards':checks,'not_experimental_replication':True,'model_quality_evaluation_not_rerun':True,'global_quality_warning':{'date':'2026-11-05','complete':False,'recall':0.892857,'threshold':0.90},'paid_model_calls':0,'items':rows}
(P/'final-adjudication.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(B/'review-preflight.json').write_text(json.dumps({'reviews':validation},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(validation,ensure_ascii=False));print('ALL',report['counts'])
