"""Preserve RSIV counterevidence and the independently verified HSE classification."""
from copy import deepcopy
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import sys
import yaml
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from scripts.feed.guard import check_summary
OUT=ROOT/'docs/internal/reports/maintenance-2026-11-18/historical-disposition'
def sha(path): return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
base=OUT/'positive-proposals-v2.json'
payload=json.loads(base.read_text())
rows=yaml.safe_load((OUT/'positive-review-rows-v2.yaml').read_text())
q={r['id']:r for r in rows['items']}
with gzip.open(ROOT/'data/feed/raw/maintenance-2026-11-18/backlog-audit/pr135-historical-inventory-v1.jsonl.gz','rt') as f:
    inv={r['id']:r for r in map(json.loads,f)}
changes={
'arxiv:2610.35316':{
 'summary_zh':'RSIV-Harness 固定模型权重，依据失败轨迹修改 Harness，以 anchor 和 memory 检查保留或回滚。相对总体结果表中原骨干的静态 Harness，可执行性提高 +28.02 点、图表结构提高 +34.01 点；消融表的基线数值与总体结果表不一致，跨骨干也并非全部指标提升。',
 'summary_en':'RSIV-Harness fixes model weights, revises the harness from failure traces, and uses anchor and memory checks for retention or rollback. Relative to the original-backbone static harness in the overall-results table, executability rises by +28.02 points and chart structure by +34.01. The ablation table reports an inconsistent baseline, and transfer does not improve every metric.',
 'reason_zh':'保留原文反证：Table 3 静态 Harness 的 DeepSeek 可执行性为 64.98，Table 4 H0 却为 51.36。+28.02 对应 Table 3 的 64.98 到 93.00，不能把两个表的基线当成一致或声称矛盾已解决。公开双语摘要明确该限制；不改作者原始数字。',
 'source_ids':['S5.T3','S5.T4'],
},
'arxiv:2610.35616':{
 'summary_zh':'HSE 在冻结编码模型下，分层聚合任务、仓库与跨仓库证据；反馈既演化技能，也更新 writer/evaluator 的外部规则与证据权重，并传给后续轮次。目标基准适配阶段固定这些规则，只更新技能库。',
 'summary_en':'With the coding model frozen, HSE aggregates task, repository, and cross-repository evidence. Feedback evolves skills and also updates the external writer/evaluator rules and evidence weights, which are transferred to later rounds. Target-benchmark adaptation fixes those rules and updates only the skill library.',
 'reason_zh':'正文训练期根据 outcome-transition 和 promotion feedback 更新 writer/evaluator 规则及证据权重，并把更新规则装入下轮；依 taxonomy 应归 harness/improver，meta 为次方向。目标基准适配阶段才冻结规则，不以此替代主方法。不是模型权重训练。',
 'source_ids':['S4.SS4.p1','S4.SS4.p2','S4.SS4.p6','S4.SS5.p2','S4.SS6.p2'],
 'direction_override':{'primary':'harness','secondary':['meta'],'harness_sub':'improver'},
},
}
amendments=[]
for item in payload['items']:
    id=item['id']
    if id not in changes: continue
    change=changes[id]
    source=item['source']
    soup=BeautifulSoup((ROOT/source['source_file']).read_text(),'html.parser')
    quotes=[]
    for key in change['source_ids']:
        node=soup.find(id=key)
        assert node is not None,(id,key)
        quotes.append({'id':key,'quote':node.get_text(' ',strip=True)})
    before=deepcopy(item['summary_override'])
    after={k:change[k] for k in ['summary_zh','summary_en']}
    guard=check_summary(item['title'],inv[id]['canonical_snapshot']['abstract'],after['summary_zh'],after['summary_en'])
    assert guard['ok'],guard
    amendment={'id':id,'independent_reviewer':'/root/nov18_hf17_crossreview',
      'reason_zh':change['reason_zh'],'before':before,'after':after,
      'source_file':source['source_file'],'source_sha256':source['source_sha256'],
      'text_file':source['text_file'],'text_sha256':source['text_sha256'],
      'source_quotes':quotes,'numeric_guard':guard}
    item['summary_override']=after
    item['summary_numeric_guard']=guard
    item['limitations_zh'].append(change['reason_zh'])
    q[id]['summary_override']=after
    q[id]['note']+=' 2026-11-18 独立复核补充：'+change['reason_zh']
    if 'direction_override' in change:
        amendment['direction_before']=deepcopy(item['direction_override'])
        amendment['direction_after']=deepcopy(change['direction_override'])
        item['direction_override']=change['direction_override']
        q[id]['direction_override']=change['direction_override']
        item['taxonomy_source']={'path':'feed/taxonomy.yaml','sha256':sha('feed/taxonomy.yaml'),
          'field':'directions.meta.def_zh','note':'If the improvement mechanism is a Harness, use harness/improver and secondary meta. Catalog is unchanged by this subtask.'}
    if id=='arxiv:2610.35316':
        item['source_discrepancy']={'resolved':False,
         'field':'DeepSeek static baseline executability',
         'overall_table_3':64.98,'ablation_table_4_H0':51.36,
         'RSIV_executability_in_both_tables':93.00,
         'original_reported_gain':'+28.02',
         'interpretation':'The quoted gain is relative to Table 3 only; no author correction or explanation for the cross-table discrepancy is asserted.',
         'public_summary_discloses':True}
    item['semantic_correction_v3']=amendment
    amendments.append(amendment)
payload['version']=3
payload['created_at']=datetime.now(timezone.utc).isoformat()
payload['supersedes']={'path':str(base.relative_to(ROOT)),'sha256':sha(base.relative_to(ROOT)),'preserved_unchanged':True}
payload['semantic_amendments_v3']=amendments
payload['independent_crosscheck_status']='All received semantic corrections are applied; final exact-v3 independent source crosscheck remains pending.'
for name in ['positive-proposals-v3.json','positive-review-rows-v3.yaml','positive-amendment-v3.json']:
    assert not (OUT/name).exists(),name
(OUT/'positive-proposals-v3.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
(OUT/'positive-review-rows-v3.yaml').write_text(yaml.safe_dump(rows,allow_unicode=True,sort_keys=False,width=110))
(OUT/'positive-amendment-v3.json').write_text(json.dumps({'created_at':payload['created_at'],'base':payload['supersedes'],'amendments':amendments},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({name:sha(OUT.relative_to(ROOT)/name) for name in ['positive-proposals-v3.json','positive-review-rows-v3.yaml','positive-amendment-v3.json']},indent=2))
