"""Freeze the independent recovery review; this does not change production data."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,yaml
from bs4 import BeautifulSoup
from scripts.feed.review import source_hash
from scripts.feed.storage import load_items
from scripts.feed.guard import check_summary

OUT=Path('docs/internal/reports/maintenance-2026-11-18/independent-recovery')
RAW=Path('data/feed/raw/maintenance-2026-11-18/independent-recovery')
path=Path('review/daily/2026-11-16.yaml')
sha=lambda b:hashlib.sha256(b).hexdigest()
review=yaml.safe_load(path.read_text()); canonical={x['id']:x for x in load_items(Path('.'))}
source_index=json.loads((OUT/'source-recovery-index.json').read_text())
assert sha(path.read_bytes())==source_index['review_sha256']
source_by_id={x['id']:x for x in source_index['items']}
interpretations={
'arxiv:2610.22915': {'scope':'harness/component','modified_object':'RewardPack criteria bindings and executable checkers; not actor weights or merely the delivered artifact','feedback':'Executed adversarial/control cases and independently labelled discrepancies trigger scoped checker or obligation repair.','retention':'Accepted verifier versions and the repair ledger carry into subsequent rounds; the across-task constructor meta-loop is described but not evaluated.','limits':['Main section 4.1 says 104 versions / 68 scenarios; Table 12 says 104 / 67. Both are preserved; the qualitative summary includes neither disputed count.','No complete non-overlapping cost ledger; matched_budget remains unknown.','The governance rule only covers observed ledger cases and can preserve a wrong reference label.']},
'arxiv:2610.23288': {'scope':'embodied','modified_object':'Task-specific coordination policies plus reusable experience/exemplar records','feedback':'Physical verifier feedback revises task maneuvers and parameters.','retention':'Experience entries and accepted examples persist, while the capability catalog and verifier do not evolve.','limits':['Executable examples remain subject to current-task constraints; no demonstrated feedback revision of the agent\'s reusable control/tool implementation.','Cross-backbone experience initialization is reported, but unequal banks and no matched empty-memory control preclude a causal transfer benefit.']},
'arxiv:2610.17130': {'scope':'harness/improver','modified_object':'The next-cycle research protocol, search constraints and terminal budgets','feedback':'Training/development execution traces and overfitting diagnostics propose bounded patches after a cycle barrier.','retention':'Accepted child policy is hashed and loaded by the next cycle, with parent lineage; completed cycle scores stay immutable.','limits':['Observed cycle traces establish protocol changes, not isolated causal improvements.','No claim of trading reproduction or complete cost verification.']},
'arxiv:2609.38662': {'scope':'harness/coevolution','modified_object':'Trainable director parameters and separately editable textual skill library','feedback':'Teams\' execution outcomes cause library additions, modifications and deletions.','retention':'Revised skills are bound to agents in later evolution steps.','limits':['Frozen executor and fixed profile definitions do not negate the separately edited skill library.','Skill-edit analysis selects the largest-gain steps while the director also trains; it does not isolate the causal contribution of skill edits.']},
'arxiv:2610.38946': {'scope':'model_weights','modified_object':'Orchestrator/refiner weights trained with GRPO; task-specific generated MAS graph receives a local patch','feedback':'Source/updated task executions supply two training reward batches.','retention':'The learned policies persist; the reviewed version does not show a reusable revised graph retained across independent tasks.','limits':['Graph edits during one task do not by themselves establish persistent Harness evolution.']},
'arxiv:2609.39022': {'scope':'evaluation_benchmark; secondary=harness','modified_object':'Expert-curated versioned procedural guidance, skill and tool interfaces evaluated as fixed resources','feedback':'Experts diagnose verification failures and revise procedures and checking examples.','retention':'Versioned resources are reused; controlled comparisons use a fixed historical core.','limits':['Classified as a Harness-specific evaluation, not an autonomous evolution method.','All four paired effect intervals include zero; prior editor exposure to existing programs is unknown.','Historical 97 Pass + 67 Concerns is distinct from the later repaired 164/164 outcome; no experimental rerun performed.']},
'arxiv:2610.09832': {'scope':'harness/coevolution','modified_object':'External textual skill library plus GRPO policy weights','feedback':'Per-episode rewards accumulate skill fitness; recent failures guide teacher-generated child skills.','retention':'Forge edits the maintained library used by subsequent rollouts.','limits':['Trial-to-active transition is usage-count gated in Eq.9, not reward-threshold gated. The existing summary should be made explicit.','Teacher knowledge and shared episode rewards prevent per-skill causal attribution.']},
'arxiv:2610.22686': {'scope':'harness/component','modified_object':'Editable textual/executable procedures, distinct from spatial notes and working-memory content','feedback':'Later execution outcomes lead to procedure revision or disabling; level_step is disabled after diagnosis of a lava death.','retention':'Procedures such as bridge_north carry across lives, and earlier scripts are installed for new-task experiments.','limits':['No claim that every memory branch is Harness, every task success rate improves, or every retained procedure helps.','Separate evaluations on multiple models do not establish transfer of an evolved artifact across models; reviewed cross_model=unknown is correct.']},
'arxiv:2610.04008': {'scope':'evaluation_benchmark; secondary=harness','modified_object':'SKILL.md behavior specifications and bundled executable scripts','feedback':'Verifier and executed requirement-linked checks guide repair; syntax and preservation checks gate edits.','retention':'Revised skill package is the evaluated artifact; no demonstrated long-horizon cross-task autonomous evolution is claimed.','limits':['Constructed/injected faults and mainly Python packages limit generalization.','Evaluating several models separately does not establish cross-model artifact transfer; reviewed cross_model=unknown is correct.']},
'arxiv:2610.22192': {'scope':'model_weights','modified_object':'RSR actor training and RPR actor/critic parameters','feedback':'Verified task trajectories become cleaned actor supervision, with phase-fixed reward lookups.','retention':'Retained model parameters initialize later phases; private runbooks are removed from actor supervision.','limits':['Terminal task-code repair is an external artifact; the source does not establish a feedback-edited persistent deployment Harness.','Current canonical v2 retained; no candidate version adoption.']},
'arxiv:2610.02196': {'scope':'harness/component','modified_object':'Staged inference-time reward programs, transition conditions and constants','feedback':'Simulator rollouts and verifier criteria drive structural repair and numerical calibration.','retention':'Selected executable programs, constants and verifier records enter a library reused/adapted for later tasks.','limits':['Controller and agent are frozen during evolution; prior motor-model pretraining remains part of the pipeline.','Physical demonstrations reuse simulation-evolved programs, not established autonomous online evolution on a physical robot.']},
'arxiv:2610.24453': {'scope':'experience_world_model','modified_object':'Persistent L2 experience entries and applicability conditions','feedback':'Multiple rollouts and judge diagnoses produce replacement/addition/deletion of experience.','retention':'Selected experiences persist and are injected as hints through a fixed retrieval/injection procedure.','limits':['No observed revision of tool implementations, the management mechanism, or a separately executable reusable skill artifact.','Each run uses one model and starts with an empty memory bank; gains across evaluated base models do not establish cross-model transfer. The review-level cross_model=yes should be unknown.']},
's2:369a7a9f02b9aa1e3150b0747e8de9066625f060': {'scope':'unknown','modified_object':'unknown','feedback':'unknown','retention':'unknown','limits':['Official coredata confirms title/DOI and online date 2026-11-13, not full text.','S2 day 2026-11-01 and Crossref month-only print date remain separately recorded.','Yanchang Cai in publisher-deposited Crossref versus Yan-Qing Cai in S2 remains an identity correspondence gap.','Version 0 is an unknown placeholder, not a real paper revision.']},
'post:https://openai.com/index/our-new-blog-for-science': {'scope':'out_of_scope_announcement','modified_object':'Science-blog launch and summaries of existing external scientific work','feedback':'No described Harness revision loop.','retention':'No described retained Harness artifact.','limits':['Background research links and numbers are not new reviewed papers or reproduced findings.']},
'post:https://openai.com/index/step-toward-defining-the-standard-model': {'scope':'external_scientific_artifact','modified_object':'Candidate particle-physics construction and proof','feedback':'Human/model/expert discussion refines the external scientific result.','retention':'No evidence of feedback-edited and retained self-Harness.','limits':['This is a source/scope check, not validation or reproduction of the physics proof.','The announcement cites an October preprint; it is not a new paper from Nov 16.']},
}
new_summary={
'summary_zh':'SkillForge 同时训练模型并维护外部技能库。它根据执行回报和失败轨迹生成子技能；试用技能达到使用次数门槛后转为活跃状态，稳定与退休再按表现和使用次数管理，更新后的技能库用于后续检索。它符合模型与 Harness 共演化；共享任务回报并不能单独确认每个技能的因果贡献，且教师会带入外部知识。',
'summary_en':'SkillForge trains the model while maintaining an external skill library. Execution rewards and failure trajectories guide child-skill generation. Trial skills become active after a usage threshold; fitness and usage govern stabilization and retirement, and later rollouts retrieve from the revised library. This supports a model-and-Harness coevolution classification. Shared task rewards do not isolate each skill’s causal contribution, and the teacher can introduce external knowledge.'}
amendments={'review_path':str(path),'input_review_sha256':source_index['review_sha256'],'generated_at':datetime.now(timezone.utc).isoformat(),'items':[
{'id':'arxiv:2610.09832','field':'summary_override','proposed':new_summary,'reason':'Make usage-only trial-to-active transition explicit; preserve coevolution scope and all source facts.','evidence_locations':['#S4.SS3.p1','Eq.9','#S4.SS4 Algorithm1 lines1-2']},
{'id':'arxiv:2610.24453','field':'evidence_quick.cross_model','proposed':{'value':'unknown','quote':None},'reason':'Multiple independent single-model runs do not establish transfer of the evolved artifact between models.','evidence_locations':['PDF Appendix C: Model use; SWE-bench Verified protocol'],'canonical_original_must_remain_unchanged':True}
]}
(OUT/'amendments-proposed.json').write_text(json.dumps(amendments,ensure_ascii=False,indent=2)+'\n')
items=[]
for row in review['items']+review['lab_updates']:
 item={'id':row['id'],'title':row['title'],'review_decision':row['decision'],'suggested_decision':row['decision'],'scope_agrees':True,'canonical_source_hash':row['source_hash'],'canonical_hash_matches':source_hash(canonical[row['id']])==row['source_hash'],'facts':interpretations[row['id']]}
 if row['id'] in source_by_id:
  source=source_by_id[row['id']]['source']
  item['body_evidence']={k:source[k] for k in ['path','sha256','bytes','identity_token','identity_found','matches_reviewed_body_sha256','text_path','text_sha256','matches_reviewed_text_sha256']}
  item['quote_count']=len(source['quote_checks']);item['whitespace_normalized_quote_matches']=sum(q['found_in_selected_text'] for q in source['quote_checks'])
  if row['id']=='arxiv:2610.22915':
   soup=BeautifulSoup(Path(source['path']).read_bytes(),'html.parser');node=soup.find(id='S2.SS0.SSS0.Px1.p1')
   for math in node.find_all('math'):math.replace_with(math.get('alttext') or math.get_text())
   item['math_quote_normalization']={'method':'Replace each MathML element with its existing alttext, then normalize whitespace. This avoids duplicated presentation+TeX text.','matched':source['quote_checks'][0]['quote'] in re.sub(r'\s+',' ',node.get_text(' ',strip=True))}
   item['numeric_conflict']={'main_section':'#S4.SS1','main_value':'104 task versions / 68 scenarios','table':'#A5.T12','table_value':'104 versions / 67 scenarios','resolution':'Unresolved in source; preserve both; no performance or count claim in the reviewed summary.'}
 else:
  checks=[]
  for e in row['source_review_evidence']['evidence']:
   p=Path(e['archived_path']); b=p.read_bytes()
   checks.append({'path':str(p),'sha256':sha(b),'matches_reviewed_sha256':sha(b)==e['sha256'],'quote_matches':not e.get('quote') or e['quote'] in b.decode()})
  item['existing_evidence_checks']=checks
 summary=row.get('summary_override')
 if summary:
  item['summary_number_guard']=check_summary(row['title'],row.get('abstract',''),summary['summary_zh'],summary['summary_en'])
  item['bilingual_semantic_review']='Equivalent qualitative mechanism and limitation statements; no experimental-number reproduction claimed.'
 if row['id'] in ['arxiv:2610.09832','arxiv:2610.24453']:item['amendment_required']=True
 else:item['amendment_required']=False
 items.append(item)
result={'generated_at':datetime.now(timezone.utc).isoformat(),'reviewer':'independent subagent /root/nov18_independent_recovery','review_type':'Source-bound independent cross-review and evidence recovery, with access to the prior submitted review; not blind or double-blind.','review_path':str(path),'review_sha256':sha(path.read_bytes()),'original_reviewed_on':review['reviewed_on'],'actual_cross_review_date':'2026-11-18','scope_decisions':{'backlog':8,'reject':6,'defer':1},'scope_decisions_agree':True,'summary_and_evidence_ready':False,'required_amendments_path':str(OUT/'amendments-proposed.json'),'items':items,'source_recovery':{'existing_exact_bodies_reused':3,'new_official_http_requests':9,'bodies_matching_submitted_review_sha256':12,'texts_matching_submitted_review_sha256':12,'canonical_writes':0,'paid_requests':0,'candidate_version_adoptions':0},'limitations':['Individual historical review-receipt files in the missing ignored build directory were not recovered. Their hashes remain in the submitted YAML; the current replay independently verifies available current-version sources.','This review verifies identities, dates already bound in canonical, cited method context, scoped qualitative summaries and selected numerical boundaries. It does not rerun experiments, audit all figures/tables, or prove general benchmark validity.','Merged owner approval, exact final-head CI, application of review-level evidence, rendering and live deployment are separate checks owned by the parent.']}
(OUT/'review-findings-initial.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(OUT/'README.md').write_text('''# 11/16 审核单的 11/18 独立恢复复核

原审核日为 11/17；本次复核日为 11/18，不回填成 11/16 当天完成。范围决定仍为 **8 项历史补录、6 项排除、1 项待补**。12 篇 arXiv 当前版本的正文、抽取文本和版本水印均已核验，正文与原审核单绑定的哈希逐项相同。3 份正文复用已提交归档，9 份由显式版本的官方 URL 免费重取。本子任务付费模型请求为 0，未修改 canonical 或正式审核单。

当前需由主任务落实两处审核层修正：SkillForge 的试用到活跃转换只使用次数门槛，摘要不能暗示回报阈值；Hippo 多模型分别运行不等于演化产物跨模型迁移，`cross_model` 应为 `unknown`。范围决定与原始科学字段不变。具体替代文本和证据见 [amendments-proposed.json](amendments-proposed.json)。

Reward Engine 主文的 104/68 与表 12 的 104/67 冲突继续保留；定性摘要不引用这些数字。MFM 与 SkillScriptBench 的 `cross_model=unknown` 纠正成立。CoEvolve 仍为任务策略和经验条目的更新；两项权重型方法、Hippo 记忆内容更新、两篇公告的排除理由均经当前版本上下文复核。DOI 的正文与作者身份缺口保持 unknown。

这次不是盲审：复核者可见旧审核单。缺失的旧逐篇独立回执没有被伪造恢复；本目录记录当前复核的真实证据。范围核查不等于全部数字重算、代码或实验复现，也不代表已批准、已合并或已上线。
''')
manifest=[]
for p in sorted([*OUT.glob('*'),*RAW.glob('*')]):
 if p.is_file() and p.name!='file-manifest.json':manifest.append({'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
(OUT/'file-manifest.json').write_text(json.dumps({'files':manifest},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'review_sha256':result['review_sha256'],'scope_decisions_agree':True,'required_amendments':len(amendments['items']),'canonical_hash_matches':sum(x['canonical_hash_matches'] for x in items),'file_count':len(manifest),'bytes':sum(f['bytes'] for f in manifest)},ensure_ascii=False))
