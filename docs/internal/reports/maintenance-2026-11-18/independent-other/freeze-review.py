"""Freeze the completed independent source review; no network or canonical writes."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import sys

from bs4 import BeautifulSoup

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
from scripts.feed.guard import check_summary, unknown_evidence
from scripts.feed.review import source_hash

OUT = ROOT / 'docs/internal/reports/maintenance-2026-11-18/independent-other'
RAW = ROOT / 'data/feed/raw/maintenance-2026-11-18/independent-other'
sha = lambda b: hashlib.sha256(b).hexdigest()
norm = lambda s: ' '.join(s.split())
now = datetime.now(timezone.utc).isoformat()
inputs = json.loads((OUT / 'input-records.json').read_text())
sources = json.loads((OUT / 'source-index.json').read_text())
source_by_id = {r['id']: r for r in sources['items']}
input_by_id = {r['id']: r for r in inputs['records']}
canonical = {r['id']: r for r in map(json.loads, (ROOT / 'data/feed/items.jsonl').read_text().splitlines())}
history = {key: canonical[key] for key, r in input_by_id.items() if r['review_group'] == 'existing_open_issue'}
(OUT / 'canonical-existing-bindings.json').write_text(json.dumps({
    'observed_at': now, 'purpose': 'Preserve historical first_seen and bind existing records; extra metadata parser first_seen is only this refetch time.',
    'records': list(history.values())}, ensure_ascii=False, indent=2) + '\n')


def quote(key, selector=None, needle=None, limit=1600):
    src = source_by_id[key]
    text = norm((ROOT / src['text_path']).read_text())
    if selector:
        soup = BeautifulSoup((ROOT / src['body_path']).read_text(), 'html.parser')
        node = soup.find(id=selector)
        assert node is not None, (key, selector)
        section = norm(node.get_text(' ', strip=True))
    else:
        section = text
    if needle:
        assert needle.lower() in section.lower(), (key, selector, needle)
        at = section.lower().index(needle.lower())
        start = max(0, at - 120)
        selected = section[start:start + limit]
    else:
        selected = section[:limit]
    assert selected and selected in text, (key, selector, selected[:100])
    return {'selector': selector or 'normalized extracted full text',
            'text_start': text.index(selected), 'text_end': text.index(selected) + len(selected),
            'quote': selected, 'quote_sha256': sha(selected.encode()),
            'source_text_sha256': src['text_sha256']}


P = {}


def paper(aid, decision, primary, sub, reason, obj, feedback, retention, refs,
          limits, summary_zh=None, summary_en=None, issue=None, missing=None):
    key = 'arxiv:' + aid
    P[key] = dict(suggestion=decision, primary=primary, harness_sub=sub, reason_zh=reason,
                  modification_object=obj, feedback=feedback, retention=retention,
                  quote_specs=refs, limitations_zh=limits, issue_number=issue,
                  missing_evidence_zh=missing, summary_zh=summary_zh, summary_en=summary_en)


paper('2611.21056', 'include', 'harness', 'evolve_main',
      'ELITE 修改并跨代继承可执行 coding-agent scaffold；验收是实际编译、导入和执行协议 smoke checks。纳入边界必须注明没有下游任务成绩或候选任务轨迹反馈。',
      'Executable agent implementation and tool/main-flow mechanisms',
      'Deterministic structural and operational checks, including tool-call and main-flow smoke tests; no downstream capability feedback',
      'Passing integrated descendant becomes the next parent; failures retain parent; evolved scaffolds are transferred without further evolution',
      [('S4.SS2.SSS0.Px3', None, 2000), ('S5.SS3.SSS0.Px1', None, 950), ('S6.SS0.SSS0.Px1', None, 900)],
      ['验收不保证性能单调；正文明确 accepted updates 仍可能性能波动。', '跨模型证据限已测 backbone，不扩展到任意模型。'],
      'ELITE 将并行提出的代码机制整合进可执行代理，并以编译和执行协议检查决定下一代；环内不使用下游任务成绩，已接受修改也可能出现性能波动。',
      'ELITE integrates independently proposed code mechanisms into an executable agent and admits descendants through compilation and execution-protocol checks. The loop uses no downstream task scores, and accepted changes can still fluctuate in performance.')

paper('2611.20533', 'include', 'harness', 'component',
      '可执行 pipeline template/skill document 根据成功失败轨迹进行文本修改，独立 selection gate 严格提升才替换 deployed skill。',
      'Executable pipeline templates and skill instructions',
      'Scored trajectories, cross-trial parameter/reward contrasts, held-out selection score',
      'Accepted skill replaces incumbent; rejected changes remain isolated; final test is separate',
      [('S3.SS2.SSS2', None, 2400), ('S4.SS11', None, 2300)],
      ['工具算子层报告的全部种子均无 adoption，不能称工具成功进化。', '无 LLM 的 retrieval replay 时间不等于完整技能获取成本；不混用两类延时。'],
      'RemeshingAgent 从网格修复轨迹修改可执行流水线模板和技能指令，只有留出选择集改善才替换当前技能，并另作测试；工具算子扩展实验未产生被采用的新算子。',
      'RemeshingAgent revises executable pipeline templates and skill instructions from mesh-repair trajectories, replacing the incumbent only after held-out selection improves and testing separately. Its tool-expansion experiment produced no adopted new operator.')

paper('2611.20856', 'include', 'harness', 'component',
      '将自然语言 skill 编译到 SkIR，执行轨迹定位失效指令并生成 typed patches；验证选中的修改成为下一轮 skill。',
      'Natural-language skill source and its typed intermediate representation',
      'Repair-test execution traces, screened regression/fix outcomes, separate validation pass rate',
      'Accepted source patch becomes the next skill and final skill is evaluated on unseen tests',
      [('S3.SS1', 'One repair iteration.', 1700), ('S3.SS6', 'Ranking and acceptance.', 3100)],
      ['接受标准是 validation 总通过率改善，不是每个旧正确样本都不退化。', '局部影响选择安全性依赖 one-hop locality 假设；文本 span 保留不等于语义绝对不变。'],
      'Synapse 以程序修复方式修改自然语言技能：执行轨迹定位问题，类型化补丁写回技能，再由独立验证集选择保留。接受依据是整体通过率提升，并不保证每个旧样例都不退化。',
      'Synapse repairs natural-language skills using execution traces to locate faults and typed patches to rewrite skill source, with a separate validation suite selecting retained versions. Acceptance requires an improved overall pass rate, not preservation of every previously passing case.')

paper('2611.21373', 'include', 'harness', 'coevolution',
      '视觉 inspector 的 LoRA 与 Report/Ignore role-instruction skill cards 均有反馈更新；card 经 held-out recent calls 验收并在同步点发布，满足权重与 Harness 共演化。',
      'Visual inspector LoRA weights and persistent skill-card role instructions',
      'Labeled wrong inspector calls and held-out recent-call verdicts',
      'Accepted cards replace current cards and new inspector snapshot is published between rollout batches',
      [('S2.SS2.SSS0.Px4', None, 1800), ('S4.SS2.SSS0.Px5', None, 1800), ('S4.SS2.SSS0.Px6', None, 1500)],
      ['audio tools 与 PaddleOCR 固定，不称所有组件共演化。', '不丢正确 verdict 的验收只针对近期留出 calls，不外推所有视频。'],
      'WeVisForensics 同时更新视觉检查器权重和可复用的报告规则；规则修订须在近期留出调用上改善判断并保留既有正确判断，再发布到后续轮次。音频工具与 OCR 保持固定。',
      'WeVisForensics updates both visual-inspector weights and reusable reporting rules. Rule revisions must improve judgments on held-out recent calls without losing previously correct judgments before publication to subsequent rounds. Audio tools and OCR remain fixed.')

paper('2611.20655', 'include', 'harness', 'component',
      '编译器固定，但被反馈修改并持续部署的是可执行 typed GEAR constraints；不是单纯检索经验条目。',
      'Explicit typed GEAR specification compiled into executable action guards',
      'Logged failed/successful trajectory replay, false-block counterexamples, online accumulated failures',
      'Incumbent/candidate/union selection accumulates accepted constraints; online deployment retains them across episodes',
      [('S3.SS2', None, 1800), ('S3.SS3', 'The second check', 1600), ('S3.SS4', 'Constraint union.', 1800), ('S4.SS6', None, 1400)],
      ['deployment retirement monitor 在报告结果中未触发，不能声称已验证自动退役。', '在多个 backbone 分别运行不等于同一 constraint 跨模型迁移；cross_model 保持 unknown。'],
      'MetaAct 从成功与失败轨迹合成可执行动作约束，利用日志回放检查误拦截并将反例用于修订；被接受的约束可持续部署。实验中的编译与拦截机制固定，退役监视器未实际触发。',
      'MetaAct synthesizes executable action constraints from successful and failed trajectories, checks false blocks through log replay, and uses counterexamples for revision. Accepted constraints persist in deployment. Compilation and blocking mechanisms remain fixed, and the retirement monitor was inactive in the reported results.')

paper('2611.19933', 'include', 'harness', 'component',
      '仅 procedural tool 子链纳入：存有 executable code，试运行失效驱动修订，合法版本按 ID 替换并供后题调用。普通 declarative/semantic memories 不自动算 Harness。',
      'Procedural-memory executable function code and applicability conditions',
      'Post-answer reference feedback and construction trial-execution failures',
      'Valid program revision replaces the same identifier and completed revisions serve later questions',
      [('A1.SS4', 'Procedural Memory additionally', 1100), ('A1.SS5', 'Memory updates remain enabled during evaluation.', 1200), ('A1.SS5', 'Feedback and refinement', 1600), ('A1.SS5', 'Procedural memory and execution.', 1600)],
      ['评测期间答后参考反馈仍更新 memory，不能描述为全程 frozen-bank evaluation。', '当前题 reference 在预测后使用，不能暗示预测前读取答案。', '不将普通经验文本整体视为技能代码。'],
      'SAGE-VQA 的程序记忆保存可执行函数，试运行或答后反馈可触发修订，完成的版本供后续问题复用。此处纳入程序工具子链；其评测包含答后记忆更新，并非全程固定记忆库。',
      'SAGE-VQA stores executable functions in procedural memory, revises them through trial execution or post-answer feedback, and reuses completed versions on later questions. The procedural-tool path is the relevant Harness component; evaluation includes post-answer memory updates rather than a fully frozen memory bank.')

paper('2611.19081', 'include', 'harness', 'coevolution',
      'VLA 权重与可执行 failure detectors/recovery FSM 都随轮次反馈修改，恢复程序经 held-out recovery gate 并跨实例复用。',
      'VLA policy weights plus executable failure detectors and shared recovery programs',
      'Current-policy failure rollouts and held-out recovery success',
      'Programs serve all failures of their mode and are revised in later rounds alongside policy training',
      [('S3.SS1', None, 2000), ('S3.SS2.SSS0.Px3', None, 2400), ('S3.SS3.SSS0.Px1.p3.1', None, 1000)],
      ['主要为仿真评测，不声称已获真机或任意机器人迁移证明。', '只保留成功 recovery demonstrations 用于 policy training。'],
      'RoboCoEvo 根据当前机器人策略的失败改写检测器和共享恢复程序，经留出恢复测试后复用，并以成功恢复数据训练策略。程序与策略随后继续迭代，构成仿真中的权重和 Harness 共演化。',
      'RoboCoEvo rewrites failure detectors and shared recovery programs from the current robot policy’s failures, reuses programs after held-out recovery testing, and trains the policy on successful recoveries. Programs and policy then continue evolving together in simulation.')

paper('2611.18856', 'include', 'harness', 'generalize',
      '被持续修改并继承的是 executable Harness H；SIM 记录反馈与代码修改历史，帮助跨模型或数据集后的继续优化。不是改进器自身代码进化。',
      'Executable Harness context, tool, and execution-flow code; accompanying modification-history memory',
      'Evolve-set scores, traces, errors, and code diffs',
      'Accepted H persists; source Harness and SIM are inherited into target optimization',
      [('S3.SS1.SSS0.Px1', None, 2600), ('S3.SS2', None, 2500), ('Sx1.p1.1', None, 1000)],
      ['optimizer 的 planning/search procedures 明确固定，不归 harness/improver。', '跨环境流程包含 target optimization，不把全部结果称为零适配迁移。', '独立重复主要集中 coding，其余域单 run，不能扩大复现覆盖。'],
      'SIM 为可执行 Harness 的修改保留问题、代码尝试与反馈历史，帮助继承的 Harness 在新模型或数据集上继续修订。被改写的是任务 Harness；改进器的规划和搜索程序保持固定。',
      'SIM preserves problem hypotheses, code attempts, and feedback for executable Harness revisions, helping an inherited Harness continue adapting to a new model or dataset. The task Harness changes, while the optimizer’s planning and search procedures remain fixed.')

paper('2611.18723', 'include', 'harness', 'component',
      'ViCoR 通过 set_reflex 改写 Python visual reflex guide，依据跨 episode 分数 checkpoint/restore library，存在可执行工件保留。',
      'Python visual-reflex guide functions, thresholds, crops, and cooldowns',
      'Before/after visual feedback and completed-episode scores',
      'Library checkpoints on improved episode score and supports restore_best; learned reflexes persist between episodes',
      [('S3.SS2', 'reflex', 1800), ('S3.SS5', None, 2500)],
      ['guide 负责触发 fast VLM，而非直接执行动作。', '跨 episode 保留不证明跨游戏迁移；不将局部实时性外推所有操作。'],
      'ViCoR 将视觉条件反射实现为可修改的 Python 引导函数，用视觉反馈调整触发规则，并在回合分数改善时保存技能库供后续回合复用。反射负责唤醒快速视觉模型，动作仍由模型决策。',
      'ViCoR implements visual reflexes as editable Python guide functions, adjusts triggers using visual feedback, and checkpoints the library when episode scores improve for reuse in later episodes. Reflexes wake a fast vision model rather than directly issuing actions.')

paper('2611.15754', 'include', 'harness', 'evolve_main',
      'MULTILOOP 将每个 Harness 版本、训练分数和 rollouts 记入历史，coding agent 据此改代码并选择训练表现最佳版本；有可核验 download_file 新工具修改。',
      'Multi-agent Harness prompts, tool declarations, error propagation, and download tool code',
      'Training-task accuracy and structured orchestrator/subagent rollouts',
      'All evaluated Harness versions retained; best training-accuracy Harness returned, with rollback available',
      [('S2', 'Evaluate Given a harness', 2400), ('S4', 'Harness Changes Made by MultiLoop', 3000)],
      ['训练集小且方法不要求每轮严格改善，不能称所有迭代单调。', '主要是 prompt/tool 层改动，深层 orchestration 失效仍在。', '全优化增加推理工作量，compute-matched comparison 留待后续。'],
      'MULTILOOP 依据训练任务成绩和多代理轨迹修改 Harness，保存版本以便回滚并选择训练表现最佳者。实际改动主要集中于提示、工具声明和下载工具；深层编排问题与额外推理成本仍未消除。',
      'MULTILOOP revises a multi-agent Harness using training-task scores and trajectories, retaining versions for rollback and selecting the best training performer. Observed changes mainly concern prompts, tool declarations, and a download tool; deeper orchestration problems and additional inference costs remain.', issue=123)

paper('2611.13524', 'include', 'evaluation_benchmark', None,
      'RSI Tax 的对象包含 Meta-Harness、RRSI 等持久 Harness 更新，明确 task-before-update 协议并审计改进调用 tokens，属于 Harness 专项评测。',
      'Evaluation and cost attribution of persistent Harness/skill/memory updates',
      'Task outcomes recorded before feedback-driven updates; update-call token accounting',
      'Evaluated methods retain learned state within streams/chains; report tracks subsequent artifact use',
      [('S2.SS1', None, 2200), ('S2.SS2', None, 2600), ('S3.SS3', None, 2600)],
      ['subsequent use 标签不等于 accuracy 因果收益；unused tokens 不是可无损删除的成本。', 'token 占比不是资金账单。', '限所测模型、任务链及固定顺序，不能解释为普遍经济规律。'],
      'RSI Tax 以先记录任务结果、再更新持久状态的协议评测 Harness 等自改方法，并区分任务执行与改进调用的 token 成本。它记录工件是否在后续使用；该标签不证明准确率收益，也不等于实际账单。',
      'RSI Tax evaluates Harness and related self-improvement methods by recording task outcomes before updating persistent state, separating task-execution tokens from improvement tokens. It tracks subsequent artifact use, which does not establish an accuracy benefit or an actual monetary bill.', issue=126)

paper('2611.20049', 'reject', 'model_weights', None,
      '反馈用于生成训练 frontier 并训练 fresh LoRA，跨轮状态是数据集；没有被修改并保留的 Agent Harness。',
      'Self-proposed Lua training data and LoRA weights', 'Interpreter labels and prediction errors',
      'Dataset persists; adapters are retrained from base', [('S1.p2.1', None, 1600), ('S3.SS1.p1.1', None, 2000)],
      ['新考试的逐轮注册条件未满足，迭代相对等量一次训练的优势不确定；不改写论文原始负结果。'])
paper('2611.20976', 'reject', 'experience_world_model', None,
      '更新业务语义和图经验；正文明确 Harness、LLM stack 与 prompts 固定。',
      'Semantic knowledge graph and experience statistics', 'Task answers and correction feedback',
      'Context-layer knowledge persists', [('S4.SS0.SSS0.Px1.p1.1', None, 1100), ('S5.SS3.SSS0.Px1.p1.1', None, 1700)],
      ['保留其真实跨任务语义学习事实；排除理由仅为当前 Harness 范围。'])
paper('2611.20605', 'reject', 'experience_world_model', None,
      '更新文本记忆及每条 utility；noisy-OR、检索、merge/evict 为既定管理规则，没有反馈改写管理代码或策略工件。',
      'Text memory entries and scalar utilities', 'Action-level critic feedback',
      'Memory entries and utility estimates persist', [('S2.SS4', 'noisy-OR', 2600), ('S2.I1.i3.p1.1', None, 1300)],
      ['不否认真实反馈、遗忘与跨任务经验；单 backbone/stream 不能扩展为通用迁移。'])
paper('2611.20927', 'reject', 'experience_world_model', None,
      'LEDGER 保留事实、时效、审计记录与 tombstones；写入/信任/删除规则固定，没有外部 Harness 的反馈更新。',
      'User facts, valid times, audit records, and deletion markers', 'New trusted statements and delete requests',
      'JSON memory state persists', [('S3.SS2.p2.1', None, 1500), ('S3.SS5.p2.1', None, 1500), ('S3.SS6.p1.1', None, 1300)],
      ['不把数据一致性和持久快照误写成机制自进化。'])
paper('2611.19764', 'reject', 'safety_governance', None,
      'CompGuard 是固定 runtime 能力/taint 防御，契约声明为 immutable；非反馈驱动 Harness 进化方法或其专项评测。',
      'Static capability contracts and runtime permissions', 'Security checks, not retained self-modification',
      'No feedback-driven Harness revision established', [('S4.p2.1', None, 2400)],
      ['有 Agent 安全与 runtime 检验不自动落入 Harness evolution。'])
paper('2611.20230', 'reject', 'experience_world_model', None,
      '存储和检索有序步骤/经验，使用既定 consolidation/promotion 规则；未展示运行中改写管理机制。',
      'Ordered goal/step records and matrix memory index', 'External success verification and fixed promotion protocol',
      'Episode/procedure records persist, not self-modified controller', [('S4', 'promotion', 1600), ('S6.p1.1', None, 1700)],
      ['报告测量为 simulation/Python reimplementation，无真实机器人或用户。', '承认明确验证与人批准协议；不能把该协议改写为自主 Harness 更新。'])
paper('2611.19700', 'reject', 'model_weights', None,
      '研究 ICL episode retention 与权重更新；FIFO/Prefix/All/Successful 为固定策略，不是反馈改写的 Harness。',
      'Persistent LoRA and retained episode context', 'Task reward and teacher distributions',
      'Weights/context persist under predefined retention rules', [('S3.SS2.p1.1', None, 1800), ('S3.SS2.p2.1', None, 1800), ('A1.SS1.SSS0.Px1.p1.1', None, 1200)],
      ['不因权重训练排除；缺的是另一个被迭代修改的 Harness 工件。'])
paper('2611.17821', 'reject', 'experience_world_model', None,
      '扩展布局/场景经验与产物库，正文明确不改 skill representation/retrieval/update protocol；缺少程序化 Harness 修改。',
      'Scene recipes, layout/content experience, and generated game scenes', 'Validation and scene-generation feedback',
      'Experience-library entries persist', [('S4.SS3', None, 1500), ('S4.SS4.SSS0.Px1.p1.1', None, 1600)],
      ['生成的场景和可复用案例是任务产物/经验，不因此等同自身控制流更新。'])
paper('2611.18140', 'reject', 'model_weights', None,
      'SFT/GRPO 训练充电 policy，物理反馈驱动动作，外部 safety layer 明确 non-learned；未呈现 Harness 更新。',
      'Battery-control model policy', 'Physical simulation reward',
      'Policy weights persist; safety filter remains fixed', [('S3.p1.1', None, 1800)],
      ['仿真闭环动作自适应不是外部 Agent Harness 演化；不声称真实电池部署。'])
paper('2611.18818', 'reject', 'experience_world_model', None,
      'SPG-Select 保留 SkillBank/ExpeL/Shared Reflexion 的经验条目；schema 为 principle/when_to_apply，与执行工件或管理策略改写证据仍有区别。',
      'Retrieved skill/insight text and cross-task experience', 'Failure-driven skill acquisition and held-out task outcomes',
      'Skill/insight banks persist under fixed adapters', [('A3.SS2.SSS2.p1.1', None, 2200), ('A3.SS3.p7.1', None, 1400), ('A3.SS3.p8.1', None, 1200)],
      ['边界建议需主审整合：不能否认持久 skill guidance 的实际作用。', '附录新 skill 示例是为附录生成的 illustrative output，不是报告实验的演化日志。', 'surrogate 理论不直接给真实技能 regret；额外 ablation 多为单 seed。'])
paper('2611.18157', 'reject', 'ai4ai', None,
      'BPMN pipeline 的 prompt-demo 筛选优化分类准确率，后续固定校验生成 XML/ontology 产物；缺少自身 Agent 控制程序反馈改写的保留链。',
      'Selected few-shot examples and generated BPMN graph/XML', 'Training relation-classification accuracy and graph validity',
      'Selected demonstrations are reused; generated diagrams are external products', [(None, 'accuracy against the training set', 1500)],
      ['承认 BootstrapFewShot feedback，不声称无优化。', '官方 PDF 无 arXiv 水印；身份由版本化 URL、标题和全部作者对应，version_identity_matches 保持 null。'])
paper('2609.04298', 'reject', 'evaluation_benchmark', None,
      '统一适配和一般 Agent benchmark/静态 Harness 对比，不是反馈驱动 Harness evolution 专项。',
      'Benchmark adapters and curated evaluation dataset', 'Adapter parity/audit and benchmark scores',
      'Infrastructure persists; no self-evolving Harness evidence', [('S1.p4.1', None, 1400), ('S1.p6.1', None, 1600)],
      ['评测多个 Harness 不自动成为 Harness evolution 评测；保留原始发表和版本日期，不作新论文。'])
paper('2603.08640', 'reject', 'ai4ai', None,
      'Agent 的交付物是外部 post-trained model，CLI scaffold 对比未提供自身 Harness 演化证据。',
      'External model post-training experiment and weights', 'Target-benchmark score',
      'Produced model is a task artifact', [('S2.p1.1', None, 1700), ('S2.SS1.p1.1', None, 1500)],
      ['自主写训练代码不等于改写自身 Harness；老论文首次发现单列。'])
paper('2505.23836', 'reject', 'evaluation_benchmark', None,
      '检测 eval/deployment awareness 的一般评测；未检验持久 Harness 自改闭环。',
      'Transcript classification benchmark and probe questions', 'Classification outcomes',
      'No retained self-modification claimed', [('S3.SS2.p1.1', None, 1700)],
      ['出现 agent trajectories/scaffolding 关键词不足纳入；保留旧发表/版本日期。'])
paper('2611.17790', 'reject', 'ai4ai', None,
      'AutoRL 确有热/冷修改训练 code/reward/loss 的闭环，但对象是被管理的 RL 训练过程，不是 AutoRL 自己的控制器或工具机制。',
      'Managed RL training code, reward, loss, and data', 'Training metrics, runtime receipts, and fixed evaluation protocol',
      'Training changes and checkpoints persist; self-Harness modification not established', [('S2.SS4', None, 2800), ('S4.SS3', 'Learning-rule ideas rarely reach execution.', 1800)],
      ['不是因训练权重排除；肯定其过程修复与真实 reward-hook patch。', '新增 learning-rule proposals 均未采用，不声称算法创新已验证。'], issue=121)
paper('2611.13818', 'reject', 'model_weights', None,
      'WAM 原文明确该实现不使用 RSI 或 agentic harness；LoRA/进度/路由为固定方案，RSI 是讨论中的未来方向。',
      'World-action model weights and fixed task/progress routing', 'Offline training and challenge evaluation',
      'Fixed trained model/configuration', [('abstract1', 'we use neither', 1400), ('S5', None, 1400)],
      ['不能把 future direction 当已经实现的共演化；保留官方测试与自评差别。'], issue=125)
paper('2611.11273', 'reject', 'experience_world_model', None,
      'CASA 存 anonymisation configs/results 和 coarse lessons，当前任务根据隐私/效用反馈重规划；工具与管理机制无持久修改证明。',
      'Anonymisation configurations and cross-task fine/coarse experience', 'Privacy and utility evaluations',
      'Configurations, results, and lessons retained for later planning', [('Sx1.SSx4.p1.1', None, 1800), ('Sx1.SSx4.p2.1', None, 1700)],
      ['跨任务经验真实存在，排除针对 Harness 范围而非否定方法效果。'], issue=132)

paper('2611.18176', 'defer', 'embodied', None,
      '撤回初读时按 prompt/skill/policy 设计描述作 coevolution 的建议。主三轮实验证明 prompt 和 skill catalog 固定；唯一具体 guidance 修改候选被 reviewer 拒绝，未发布。',
      'Verified: VLA weights; proposed but unverified: persistent prompt/skill edits',
      'Episode feedback and proposed independent prompt review',
      'Main reported evaluation retains fixed prompt/skill catalog; accepted non-weight update not demonstrated',
      [('S6.SS1', 'The three-round policy-learning configuration', 1900), ('A2.SS1', None, 2900)],
      ['不得将主实验成绩归因三者共同演化。', '完整更新机制设计不等于实际被采用并部署的工件修改。'],
      missing='需要一条被接受的 prompt/skill 修改记录、验收依据、后续轮次部署及源版本绑定。')
paper('2611.18006', 'defer', 'model_weights', None,
      'RecurIR 的 estimator、task generator、revision operator/gate 由学习更新，存在独立 transfer/retention 检查；目前未明确可复用外部 Harness 工件如何被修改并部署。',
      'Learned benefit estimator, degradation-task generator, revision operator, and restoration plan',
      'Matched restoration comparisons, generated counterexamples, independent transfer/retention verification',
      'Learned policies/hypotheses persist; external Harness-code persistence is unclear',
      [('S3.SS2', None, 1800), ('S3.SS3', None, 1600), ('S3.SS4', None, 1800), ('S7.SS3.p1.1', None, 1200)],
      ['不否认真实反馈与跨轮学习；frozen restoration tools 不足以证明外部 Harness 自改。'], issue=119,
      missing='需要区分模型参数更新与可执行策略工件的实际 diff，并提供验收及跨任务使用链。')
paper('2611.12288', 'defer', 'ai4ai', None,
      'ForgeSystem 声称反馈修改 context/tool/exploration/testing，实际主要验证 kernel/engine 外部产物；具体可接受并保留 Harness 修改实例及多轮收益仍缺。',
      'Verified external engineering artifacts; claimed Harness context/tool/process updates',
      'Artifact execution and verification feedback',
      'Construction records persist; specific accepted Harness revision and future-task use not established',
      [('S3.SS3.p2.1', None, 1800), ('S9', None, 2000)],
      ['标题或架构描述不能替代实际更新/验收/保留记录；§9 本身保留多轮外循环验证缺口。'], issue=128,
      missing='需要可定位的自身 Harness 修改、对应执行反馈、通过的验收与后续 forging 任务复用记录。')

P['s2:4fe67f25512c1f8580168b21b26c921b42b22a94'] = dict(
    suggestion='defer', primary='theory_survey', harness_sub=None,
    reason_zh='Semantic Scholar metadata 两次实际请求均 429；未取得 DOI/官方全文，不能由摘要确认身份和 Harness 专题范围。',
    modification_object='unknown', feedback='unknown', retention='unknown', quote_specs=[],
    limitations_zh=['仅保存输入 metadata 与错误原文；未声明完成全文审查。'], issue_number=None,
    missing_evidence_zh='补官方身份绑定、完整正文及 Harness 专项分析依据。', summary_zh=None, summary_en=None)

POSTS = {
 'https://sakana.ai/jfinbench/': ('ai4ai', '试验特定转换代码生成金融 benchmark 数据，是外部数据构建产物；共用转录脚本固定，不是自身 Harness 演化。', '汎用スクリプトがVLMで試験PDFを転記し'),
 'https://metr.org/notes/2026-11-16-measuring-alignment-eval-tells/': ('evaluation_benchmark', 'alignment-eval tells 的一般研究，不是 Harness 演化专项；不把模型识别测试环境等同自改。', 'To figure out what features'),
 'https://openai.com/index/introducing-gpt-6-2-astra-sol': ('model_weights', '模型发布及通用职业任务 benchmark，无反馈改写并保留自身 Harness 的实证链。', 'We’re introducing'),
 'https://openai.com/index/strengthening-nato-allied-cyber-defences-ai': ('safety_governance', '网络防御模型部署、授权使用与人员培训案例，未报告 Harness 自改闭环。', 'Through Daybreak'),
 'https://openai.com/index/introducing-chatgpt-for-sales': (None, '销售插件和 ready-to-use workflows 产品发布，无执行反馈改写自身流程并保留的证据。', 'The new Sales plugin from OpenAI gives'),
 'https://openai.com/index/astra-law-6-2': (None, 'research team 根据 practitioner feedback 调整设置/指令与索引，属于人类研发改进，不是已验证自主 Harness 演化。', 'we iteratively refine'),
 'https://openai.com/index/introducing-openai-for-chile': (None, '公共部门 AI 采用、人才与创业支持合作公告，非 RSI/Harness 方法。', 'Today we’re launching'),
 'https://openai.com/index/expanding-chatgpt-for-academic-researchers': (None, '研究人员访问资助计划，非 Harness 自改方法。', 'We’re expanding'),
 'https://openai.com/index/strengthening-online-child-safety': ('safety_governance', '安全检测分类器、支持与合作发布，无 Harness 演化链。', 'Today, we’re releasing'),
 'https://openai.com/index/science-at-the-frontier': ('evaluation_benchmark', '科研用户使用分析和问卷，不是系统根据反馈持久改写 Harness 的研究。', 'OpenAI’s Economic Research team'),
 'https://openai.com/business/customer-stories/revolut': (None, '企业使用 Codex/ChatGPT 的案例，无自身 Harness 修改的验收及跨任务保留证据。', 'With OpenAI models and Codex'),
 'https://openai.com/index/lvmh-media-division-partnership': (None, '媒体合作和企业 AI 部署公告，非 RSI/Harness 方法。', 'strategic agreement'),
 'https://openai.com/index/our-first-phase-of-embedded-assessments': ('safety_governance', '第三方 alignment/safeguards 评估计划，未针对 Harness 演化展开专项方法。', 'Embedded assessments give independent experts'),
 'https://openai.com/index/more-ways-to-move-care-forward-with-chatgpt-for-healthcare': (None, '医疗产品、clinical search 与 plugins 更新，无自身 Harness 反馈演化证据。', 'Today, we’re sharing'),
 'https://openai.com/index/advancing-computer-use-for-healthcare-teams': ('evaluation_benchmark', '医疗 computer-use 的一般表现、安全与成本评测，不是 Harness 演化专项。', 'Today, we’re sharing new results'),
 'https://openai.com/index/the-kings-trust-and-openai': (None, '捐赠与年轻人技能培训计划，非 Harness/RSI 方法。', 'has announced a major partnership'),
 'https://openai.com/business/customer-stories/holiday-extras-dots': (None, '主动报告和助手使用案例，不足以证明反馈改写自己的 Harness 工件。', 'Dots deliver launch reports'),
 'https://openai.com/ads/blog/chatgpt-ads-increases-its-market-presence': (None, '广告 reseller 市场扩展公告，非 Harness/RSI 方法。', 'Starting today, brands'),
 'https://openai.com/ads/customers/vistaprint': (None, '广告投放客户案例，非 Harness/RSI 方法。', 'VistaPrint uses ChatGPT Ads'),
}
for url, (primary, reason, needle) in POSTS.items():
    key = 'post:' + url
    P[key] = dict(suggestion='reject', primary=primary, harness_sub=None, reason_zh=reason,
                  modification_object='No autonomous reusable Harness modification established',
                  feedback='Not a verified Harness evolution loop', retention='Not established for Harness updates',
                  quote_specs=[(None, needle, 1200)], limitations_zh=['结论仅针对当前 Harness 专题范围；网页正文已读取，不以标题关键词代替范围审查。'],
                  issue_number=None, missing_evidence_zh=None, summary_zh=None, summary_en=None)

assert set(P) == set(input_by_id), (set(input_by_id) - set(P), set(P) - set(input_by_id))
items = []
for key, cfg in P.items():
    src = source_by_id[key]
    row = input_by_id[key]
    evidence = [quote(key, selector, needle, limit) for selector, needle, limit in cfg.pop('quote_specs')]
    if src['status'] == 'source_available':
        assert evidence
        for attr in ('body', 'text'):
            assert sha((ROOT / src[f'{attr}_path']).read_bytes()) == src[f'{attr}_sha256'], (key, attr)
    if cfg['summary_zh']:
        guard = check_summary(row['title'], row['abstract'], cfg['summary_zh'], cfg['summary_en'])
        assert guard['ok'], (key, guard)
    else:
        guard = None
    old = history.get(key)
    item = {'id': key, 'title': row['title'], 'kind': row['kind'], 'group': row['review_group'],
            'version': row['version'], 'reviewed_on': '2026-11-18',
            'published': row['published'], 'updated': row.get('updated'),
            'first_seen': old['first_seen'] if old else row.get('first_seen'),
            'first_seen_basis': 'existing canonical record, preserved' if old else 'intake actual observation',
            'metadata_refetch_observed_at': row.get('first_seen') if old else None,
            'hf_daily_dates': row.get('hf_daily_dates', []),
            'publication_date_policy': 'No HF recommendation date assigned; use true source window, keeping older discoveries separate.',
            'input_source_hash': source_hash(row),
            'source_hash_semantics': 'Input before proposed summaries/classification; parent must rebind final owner-visible content.',
            'existing_canonical_source_hash': source_hash(old) if old else None,
            'source_receipt': src, 'original_quotes': evidence,
            **cfg, 'summary_number_guard': guard, 'evidence_quick': unknown_evidence(),
            'verification_scope': 'Official-source identity/date and scope/mechanism review, qualitative summary fact checks; not experimental reproduction or full numerical recomputation.'}
    item['issue_url'] = f"https://github.com/adongwanai/follow-rsi/issues/{cfg['issue_number']}" if cfg['issue_number'] else None
    item['recoverable_state'] = {'include': 'independent_recommendation_ready_for_main_review',
                                 'reject': 'scope_review_complete_preserve_exclusion_evidence',
                                 'defer': 'explicit_evidence_gap_preserved'}[cfg['suggestion']]
    if key == 'post:https://sakana.ai/jfinbench/':
        item['date_note'] = 'Official page November 17; RSS 2026-11-16T15:00:00+00:00 is November 17 in Japan. Both retained without contradiction.'
    if key == 'arxiv:2611.18176':
        item['correction_history'] = [
            {'stage': 'initial reading', 'suggestion': 'include/coevolution',
             'basis': 'Design sections describe prompt, skill, and policy update mechanisms.'},
            {'stage': 'crossreview correction', 'suggestion': 'defer',
             'basis': 'Main §6.1 evaluation fixed prompt and skill catalog; B.1 proposal rejected and unpublished.',
             'supersedes_initial_suggestion': True}]
    assert not item['hf_daily_dates'], (key, 'unexpected HF date')
    items.append(item)

counts = Counter(r['suggestion'] for r in items)
assert counts == {'include': 11, 'reject': 36, 'defer': 4}, counts
report = {'generated_at': now, 'reviewer': 'independent sub-agent /root/nov18_independent_recovery',
          'review_round': 3, 'publication_authority': 'Advisory only; no canonical or formal review writes, PR, merge, or publication by this worker.',
          'source_index_sha256': sha((OUT / 'source-index.json').read_bytes()),
          'input_records_sha256': sha((OUT / 'input-records.json').read_bytes()),
          'canonical_existing_bindings_sha256': sha((OUT / 'canonical-existing-bindings.json').read_bytes()),
          'counts': dict(counts),
          'groups': {g: dict(Counter(r['suggestion'] for r in items if r['group'] == g))
                     for g in sorted({r['group'] for r in items})},
          'source_availability': sources['counts'], 'paid_model_requests': 0,
          'abstract_quick_evidence_policy': 'Fulltext quotes remain fulltext evidence, never reclassified as abstract evidence. Quick evidence left unknown.',
          'number_check_policy': 'Qualitative bilingual summaries contain no new numerical performance claims; deterministic guard is not experimental verification.',
          'items': sorted(items, key=lambda r: (r['group'], r['id']))}
(OUT / 'review-findings.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')

lines = ['# 2026-11-18 非 HF 候选及历史 issue：独立第三轮复核', '',
         '这是子 agent 的逐项范围与来源建议，主审须结合独立反证整合；未直接修改 canonical、正式 review 或生产物，也未创建/合并 PR。', '',
         '- 全部 51 条：建议纳入 11、排除 36、待补 4。',
         '- 44 条新增非 HF 候选：纳入 9、排除 33、待补 2；7 条历史 issue：纳入 2、排除 3、待补 2。',
         '- 官方全文或网页取得 50 条；S2 survey 原请求和一次重试均 429，保留错误原文与逐项原因。',
         '- 11 条建议纳入均有定性中英摘要，来源正文/抽取文本 SHA 和精确原文片段已经校验；这不是实验复现。',
         '- 付费模型请求 0。所有请求回执与原文已持久保存，未重跑历史模型。', '',
         '## 必须保留的反证与日期边界', '',
         '- ESI 的初读共演化建议已撤回：主实验 prompt/skill catalog 固定，具体 guidance 候选未发布。现为 defer。',
         '- ELITE 仅用结构/可操作性反馈，无下游候选任务成绩；RemeshingAgent 工具层无 adoption；Synapse 接受总分改善并非所有旧样例不退化。',
         '- WeVisForensics、RoboCoEvo 有可执行/规则工件与权重双方更新；MetaAct 改的是 executable spec。SAGE-VQA 只纳入程序工具子链，评测期间仍有答后更新。',
         '- SIM 的改进器 planning/search 固定；MULTILOOP 主要提示/工具改动；RSI Tax 的 subsequent use 不是准确率因果收益，tokens 不是账单。',
         '- SPG-Select 排除为经验条目边界建议，需主审整合；其附录示例不是实验演化日志。',
         '- BPMN 官方 PDF 有效，标题和全部作者匹配；无 arXiv 水印的 version_identity_matches 保持 null。',
         '- 历史 issue 的 first_seen 从 canonical 保留；额外 metadata parser 的 11/18 first_seen 只记作本次 refetch，不覆盖历史。',
         '- 所有条目无 HF 推荐日；旧论文首次发现单列，不能顺延为今日新发表。JFinBench RSS 的 UTC 11/16 15:00 对应日本 11/17，保留官方网页日。', '',
         '## 逐项建议', '', '| ID | 建议 | 分类 | 原因 |', '| --- | --- | --- | --- |']
for row in report['items']:
    label = {'include': '纳入建议', 'reject': '排除', 'defer': '待补'}[row['suggestion']]
    cat = (row['primary'] or 'off_topic') + ('/' + row['harness_sub'] if row['harness_sub'] else '')
    lines.append(f"| {row['id']} | {label} | {cat} | {row['reason_zh']} |")
lines += ['', '## 可恢复文件', '',
          '- `review-findings.json`：51 条来源、日期、分类、反馈与持久性、反证、摘要与逐项待补。',
          '- `input-records.json`：冻结输入与原始文件哈希；`canonical-existing-bindings.json`：历史日期绑定。',
          '- `source-index.json`、`source-supplement-receipt.json`：实际免费请求及补充验证回执。',
          '- `file-manifest.json`：本子任务全部原文与报告文件的可恢复 SHA。',
          '- `validation-receipt.json`：唯一 ID、正文/文本哈希、所有引句、双语数字守卫检查。', '']
(OUT / 'README.md').write_text('\n'.join(lines))
receipt = {'checked_at': now, 'unique_ids': len(set(r['id'] for r in items)),
           'expected_total': 51, 'source_available': 50, 'unavailable': 1,
           'source_hashes_verified': 100, 'quote_count': sum(len(r['original_quotes']) for r in items),
           'all_quotes_verified_as_exact_normalized_source_substrings': True,
           'summary_guards_passed': sum(r['summary_number_guard'] is not None for r in items),
           'summary_guard_failures': [], 'paid_requests': 0, 'canonical_writes': 0,
           'formal_review_writes': 0, 'tests_are_not_experimental_reproduction': True,
           'findings_sha256': sha((OUT / 'review-findings.json').read_bytes())}
(OUT / 'validation-receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
files = sorted([p for base in (OUT, RAW) for p in base.rglob('*') if p.is_file() and p.name != 'file-manifest.json'])
manifest = {'generated_at': now, 'file_count': len(files), 'total_bytes': sum(p.stat().st_size for p in files),
            'files': [{'path': str(p.relative_to(ROOT)), 'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())} for p in files]}
(OUT / 'file-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'counts': counts, 'groups': report['groups'], 'validation': receipt,
                  'files': manifest['file_count'], 'bytes': manifest['total_bytes'],
                  'manifest_sha256': sha((OUT / 'file-manifest.json').read_bytes())}, ensure_ascii=False, indent=2))
