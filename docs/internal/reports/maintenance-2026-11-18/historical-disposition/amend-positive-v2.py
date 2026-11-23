"""Apply explicitly recorded independent semantic corrections while retaining v1."""
from copy import deepcopy
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import sys
import yaml
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from scripts.feed.guard import check_summary
OUT = ROOT / 'docs/internal/reports/maintenance-2026-11-18/historical-disposition'
def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
with gzip.open(ROOT / 'data/feed/raw/maintenance-2026-11-18/backlog-audit/pr135-historical-inventory-v1.jsonl.gz','rt') as f:
    inv = {r['id']:r for r in map(json.loads,f)}
base_path = OUT / 'positive-proposals-v1.json'
payload = json.loads(base_path.read_text())
rows = yaml.safe_load((OUT / 'positive-review-rows-v1.yaml').read_text())
q = {r['id']:r for r in rows['items']}
amendments = []
corrections = {
'arxiv:2610.34938': {
 'zh':'研究让 retro 回顾 Claude Code 在 30 个 SWE-bench Verified 问题上的会话并提出 Harness 修改，研究者选择实施 24 个提案；其中可评估的变更与一个作者另写的对照一起用于后续任务评测。多数遇到目标问题的评估未减少重复工作；这是含人工选择的专项评测。',
 'en':'The study uses retro to review Claude Code sessions on 30 SWE-bench Verified issues and propose harness changes. Researchers select 24 proposals for implementation and evaluate the resulting eligible changes alongside an author-written comparison on later tasks. Most evaluations encountering the target problem show no reduction in repeated work; selection involves humans.',
 'reason_zh':'原 v1 的“评估 12 个变更”未说明组成，容易把全部归于 retro。正文明确 11 个 resulting adaptations 加 1 个 author-written comparison；公开摘要删去聚合 12，保留作者另写对照的区分。',
 'paragraph_ids':['S3.p1','S3.p5'],
},
'arxiv:2610.31789': {
 'zh':'Phronix 通过 predictor-validator-corrector 循环，依据工具执行结果改进并保留 MCP 工具与关联技能。对冷启动已解决的任务，继承其能力库的热启动运行首次尝试成功率为 93-95%；该比例的分母不包括冷启动未解决的任务。',
 'en':'Phronix uses a predictor-validator-corrector loop to refine and retain MCP tools and associated skills from execution outcomes. Among tasks already solved during cold-start runs, warm-start runs inheriting the capability store achieve 93-95% first-attempt success; tasks not solved in cold-start runs are outside that denominator.',
 'reason_zh':'原 v1 把条件成功率写成所有重复任务的首次成功率。正文度量定义及结果明确分母是冷启动已解决的任务；双语补齐条件，不改原始数字。',
 'paragraph_ids':['S5.SS1.SSS5.p1','S5.SS3.SSS1.p1','S5.SS3.SSS1.p2'],
}}
oldprov_path = 'docs/internal/reports/maintenance-2026-10-30/independent/source-provenance.json'
oldprov = json.loads((ROOT/oldprov_path).read_text())['items']
oldbyid = {r['id']:(i,r) for i,r in enumerate(oldprov)}
for item in payload['items']:
    id = item['id']
    if id in oldbyid:
        index, prior = oldbyid[id]
        oldraws = [a['sha256'] for a in prior['body_receipt']['attempts'] if a.get('sha256')]
        assert item['source']['source_sha256'] in oldraws
        item['historical_raw_source_hash_reference'] = {
          'path':oldprov_path,'file_sha256':sha(oldprov_path),'collection':'items','index':index,
          'field':'body_receipt.attempts[].sha256',
          'raw_source_sha256':item['source']['source_sha256'],
          'text_extractor_note':'Restored raw HTML bytes match; extracted text hashes may differ with extractor. No assertion of historical text-byte equivalence.'}
    if id in corrections:
        change = corrections[id]
        soup=BeautifulSoup((ROOT/item['source']['source_file']).read_text(),'html.parser')
        paragraphs=[]
        for pid in change['paragraph_ids']:
            node=soup.find(id=pid)
            assert node is not None, (id,pid)
            paragraphs.append({'id':pid,'quote':node.get_text(' ',strip=True)})
        before=deepcopy(item['summary_override'])
        after={'summary_zh':change['zh'],'summary_en':change['en']}
        guard=check_summary(item['title'],inv[id]['canonical_snapshot']['abstract'],change['zh'],change['en'])
        assert guard['ok'], guard
        item['summary_override']=after
        item['summary_numeric_guard']=guard
        item['limitations_zh'].append(change['reason_zh'])
        q[id]['summary_override']=after
        q[id]['note']+=' 2026-11-18 独立交叉复核更正：'+change['reason_zh']
        item['semantic_correction_v2']={'independent_reviewer':'/root/nov18_hf17_crossreview',
            'reason_zh':change['reason_zh'],'original_summary':before,
            'corrected_summary':after,'source_paragraphs':paragraphs,
            'source_raw_sha256':item['source']['source_sha256'],
            'source_text_sha256':item['source']['text_sha256'],
            'numeric_guard_scope':'Literal numbers only; semantic denominator/composition checked in cited original paragraphs.'}
        amendments.append({'id':id,**item['semantic_correction_v2']})
    if id=='arxiv:2610.33487':
        clarification='ReSight 的 matched_budget=yes 仅对应同一 benchmark 的 online budget；探索计算预算独立，不能理解为计入探索与构建后的总成本相同。'
        item['limitations_zh'].append(clarification)
        item['evidence_scope_clarification']={'field':'matched_budget','value':'yes',
          'scope':'same-benchmark online execution budget only',
          'total_budget_including_exploration_matched':'unknown',
          'source_quote':'Exploration has a compute budget independent of the execution agent’s per-query call limit, accommodating model preparation, memory processing, and debugging.'}
        text=(ROOT/item['source']['text_file']).read_text()
        assert item['evidence_scope_clarification']['source_quote'] in text
        q[id]['note']+=' '+clarification
        amendments.append({'id':id,'reason_zh':clarification,
                           'evidence_scope_clarification':item['evidence_scope_clarification']})

payload['version']=2
payload['created_at']=datetime.now(timezone.utc).isoformat()
payload['supersedes']={'path':str(base_path.relative_to(ROOT)), 'sha256':sha(base_path.relative_to(ROOT)),
                       'preserved_unchanged':True}
payload['semantic_amendments']=amendments
payload['counts']['current_summary_independent_pending']=19
payload['independent_crosscheck_status']='Corrections requested by the independent reviewer are applied; final exact-v2 signed source crosscheck remains pending.'
for name in ['positive-proposals-v2.json','positive-review-rows-v2.yaml','positive-amendment-v2.json']:
    assert not (OUT / name).exists(),name
(OUT/'positive-proposals-v2.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
(OUT/'positive-review-rows-v2.yaml').write_text(yaml.safe_dump(rows,allow_unicode=True,sort_keys=False,width=110))
(OUT/'positive-amendment-v2.json').write_text(json.dumps({'created_at':payload['created_at'],'base':payload['supersedes'],'amendments':amendments},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({name:sha(OUT.relative_to(ROOT)/name) for name in ['positive-proposals-v2.json','positive-review-rows-v2.yaml','positive-amendment-v2.json']},indent=2))
