"""Make the reviewed Harness focus explicit on four cross-direction studies."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import yaml

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from scripts.feed.scope import load_scope,scope_status
OUT=ROOT/'docs/internal/reports/maintenance-2026-11-18/historical-disposition'
def sha(path): return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
base=OUT/'positive-proposals-v3.json'
payload=json.loads(base.read_text())
rows=yaml.safe_load((OUT/'positive-review-rows-v3.yaml').read_text())
q={r['id']:r for r in rows['items']}
reasons={
 'arxiv:2610.38392':'专项研究可接受文本 Harness 修改导致安全约束逐步侵蚀，接受后的父代继承是直接研究对象。',
 'arxiv:2610.39122':'安全实验明确研究 MetaClaw 将会话反馈转成可复用技能对后续授权行为的影响；与另外的 RL 分支分开，不泛化为所有赞许实验。',
 'arxiv:2610.27889':'专项比较优化前后 Harness 的 pass@k/任务可解范围，诊断 Harness 优化的能力引出或覆盖扩展。',
 'arxiv:2610.34938':'专项研究 retro 提议并实施的持久 Harness 修改在后续任务中是否减少重复工作，含人类选择与作者对照。',
}
amendments=[]
for item in payload['items']:
 id=item['id']
 if id in reasons:
  before=deepcopy(item['direction_override'])
  assert before['primary'] in ['evaluation_benchmark','safety_governance']
  after={**before,'secondary':['harness']}
  item['direction_override']=after;q[id]['direction_override']=after
  q[id]['note']+=' 交叉方向明确 secondary=harness：'+reasons[id]
  amendment={'id':id,'before':before,'after':after,'reason_zh':reasons[id],
    'trigger':'Parent dated-review preflight found missing secondary Harness scope in an otherwise source-reviewed specialized study.',
    'source_sha256':item['source']['source_sha256'],
    'does_not_change_publication_scope_threshold':True}
  item['direction_correction_v4']=amendment;amendments.append(amendment)
scope=load_scope(ROOT)
checks=[{'id':r['id'],'direction':r['direction_override'],
         'scope_status':scope_status(r['direction_override'],scope)} for r in payload['items']]
assert len(amendments)==4 and all(r['scope_status']=='in_scope' for r in checks)
payload['version']=4;payload['created_at']=datetime.now(timezone.utc).isoformat()
payload['supersedes']={'path':str(base.relative_to(ROOT)),'sha256':sha(base.relative_to(ROOT)),'preserved_unchanged':True}
payload['direction_amendments_v4']=amendments
payload['current_scope_checks']=checks
payload['independent_crosscheck_status']='All received content corrections and four explicit Harness secondary directions are applied; final exact-v4 independent crosscheck pending.'
for name in ['positive-proposals-v4.json','positive-review-rows-v4.yaml','positive-amendment-v4.json']:
 assert not (OUT/name).exists(),name
(OUT/'positive-proposals-v4.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
(OUT/'positive-review-rows-v4.yaml').write_text(yaml.safe_dump(rows,allow_unicode=True,sort_keys=False,width=110))
(OUT/'positive-amendment-v4.json').write_text(json.dumps({'created_at':payload['created_at'],'base':payload['supersedes'],'amendments':amendments,'scope_checks':checks},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({name:sha(OUT.relative_to(ROOT)/name) for name in ['positive-proposals-v4.json','positive-review-rows-v4.yaml','positive-amendment-v4.json']},indent=2))
