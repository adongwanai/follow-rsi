# 2026-11-05 独立第三轮范围复核

本批独立复核 **59 项：8 项建议 include、50 项建议 exclude、1 项 borderline**。其中 55 项来自 11/04–11/05 HF 完整原始摘要，4 项来自其他已配置 arXiv 来源；57 个新 ID 为 7 include /50 exclude，EvoTeam 与 MoLRSI 为已有 ID 补推荐日。

**正式决定全部 defer，publication_authorized=false。** 既有质量闸门召回 24/28=0.8571，未达到 0.90；本次没有付费调用、实验复现、质量闸门重跑或发布。

## 阅读深度与独立性

- 先读 55 份完整 HF `paper.summary` 并冻结初筛；没有使用 `ai_summary`。4 篇其他来源也读完整原始摘要。
- 12 份当前正文响应选段独立核验（含 EvoTeam v2），另对 MoLRSI 复用旧 v2 正文、重哈希并重看相关段落；合计 13 项正文机制/边界核验。HF 中 9 项有正文/复用核验、46 项仅完整摘要筛查；其他来源 4 项均有正文选段。
- 4 个排除项另读正文；6 个针对性排除项及固定随机种子抽出的 PrimeSim、Stock RAG 共 8 项核对摘要原句。
- 旧 11/03 的 45 项只核对原始标题/摘要一致后复用旧意见：4 include /40 exclude /1 borderline。旧轮深度为 8 项选段、2 项旧正文复用、35 项摘要；没有今天重审 45 篇。旧历史 196 项今天未再逐项复核。
- 独立 59 项结论冻结后才读取本轮主审文件：范围意见 59/59 一致，主审 66 处引句均在绑定原始正文中精确匹配。独立正文证据另保存 52 处短引句；会后增加 EvoGuard expert-generator 训练的 1 处核验。

冻结稿 SHA256：`7c7128182609439000f657e4ffbc4465d1ed42bfdba9b4a731344eb185dda029`。旧缓存 33 个绑定中 32 个一致；唯一变化为旧 primary-b-review.json，未将其旧哈希冒充当前主审证据。

生产提示词仍含“外部 Harness 是明确主要改进对象”的旧限制，11/02 共演化修订提案未应用。本审核遵循 owner 最新的程序工件—反馈—持留判据，未改生产 taxonomy、prompt 或 eval。

## 重点结论与边界

### EvoTeam: Multi-Agent Collaboration via Evolving Teams — include (harness/evolve_main)

团队交互规则、个体提示补丁与可复用技能经执行反馈更新，保留到后续团队和任务。

改进对象：团队规则、候选团队组织、个体 prompt patches 和技能文件；非权重。 反馈：reflector 读取推理轨迹、工具输出和中间工件，针对观察到的错误修订。 持留：团队规则在本团队复用，技能由对应 agent 跨团队保留；用于后续任务。

原文短证据（[#S3.SS3.SSS0.Px3.p1.2](https://arxiv.org/html/2610.39813v2#S3.SS3.SSS0.Px3.p1.2)）：“It may add a useful procedure to the skill set or revise an existing skill to address an observed error.”

- 当前官方最新 v2 与旧 v1 整页字节不同；上述四段标准化正文相同，按 v2 复核，不称整页哈希复用。
- 任务内招募、规划和重分配属于执行；不据此单独认定持久演化。
- 官方 v1/v2 日期与 canonical 旧元数据的差异单报，未在本审核中改写。

### MoLRSI: A Recursive Self-Improving AI agent for Molecular Discovery — borderline (ai4ai)

正文既有靠经验记录改变有效搜索策略的主循环，也有新构建技能执行修复并保留；仍缺少跨任务研究者 Harness 版本链，保留边界。

改进对象：科研 workflow、模型架构、搜索记忆为主；另有 resource-library 技能代码修复的真实反证。 反馈：development score、execution errors 与 repair outcomes 进入记忆；技能首次执行报错触发代码/依赖修复。 持留：workflow/修改/执行记录保留；验证通过的技能也保留复用，但其是否构成持续 Harness 版本循环尚不清楚。

原文短证据（[#S4.SS1.SSS3.p7.1](https://arxiv.org/html/2610.39714v2#S4.SS1.SSS3.p7.1)）：“After each execution attempt, MolRSI stores the workflow, its execution status and any available development score in solution memory.”

- 不能写成仅有记忆、完全没有技能代码修复，也不能因首次 skill bootstrap 验证就自动纳入。
- 需要实际技能版本、后续任务调用链与基于反馈再修订的证据，以区分科研工具初建与研究者 Harness 持续演化。
- 当前官方 abs 与 11/02 缓存字节一致，最新仍为 v2；本次没有新抓取正文，重哈希并重看旧 v2 选定段落。

### ParetoSaddler: Pareto-Guided Optimization of Agent Harnesses for Quality and Cost — include (harness/generalize)

完整 Harness 候选经轨迹诊断修订，质量—成本联合估计控制晋升并保留候选；新贡献重心为噪声下准入与成本权衡。

改进对象：提示、工具、middleware、控制逻辑组成的完整 Harness；基础模型固定。 反馈：执行轨迹及配对 quality/cost 观测指导定向程序修订，重复评估与 Bayesian bootstrap 控制晋升。 持留：development 评估过的候选持续保留，包括当前 Pareto archive 之外的候选。

原文短证据（[#S3.SS0.SSS0.Px1.p1.1](https://arxiv.org/html/2611.02079#S3.SS0.SSS0.Px1.p1.1)）：“An agent harness comprises the prompts, tools, middleware, and control logic surrounding the underlying LLM”

- subtype 独立初判为 generalize，taxonomy 明列泛化、正则、准入与成本；修改对象仍是完整 Harness。
- 数字只核对正文和表格，不是复现实验或重新计算全部 bootstrap/统计检验。
- 数字边界：PS-Pareto Q：ClawMark 70.86%→81.35%，$1.17→$1.01/task；GAIA2 56.22%→62.89%，$0.78→$0.45/task。
- 数字边界：正文 14.8% / 11.9% 是相对收益，不是百分点；测试三次重复，报告均值与样本标准差。

### Mage-VL-Cowork: A Full Training Recipe to Learn Hybrid Computer Use From Evolved Harnesses — include (harness/evolve_main)

先反馈驱动演化教师完整外部执行 Scaffold/接口/提示，再固定教师 Harness 生成轨迹训练学生；外部程序循环足够明确。

改进对象：教师 scaffold、工具接口、提示和执行环境；教师权重固定，学生训练另记次方向。 反馈：authoring agent 使用 rubric success、token cost、execution feedback、channel statistics 选择修订。 持留：选出的教师 Harness 在后续数据生成轮次基本固定并被复用。

原文短证据（[#S3.SS1.p2.1](https://arxiv.org/html/2610.40747#S3.SS1.p2.1)）：“We improve the teacher’s hybrid execution by evolving its external harness while keeping the underlying model weights fixed.”

- 独立摘要初判 component，经正文确认多项完整教师执行部件共同演化后修正为 evolve_main。
- 教师 Harness 演化后训练学生是顺序流程；未证明模型与 Harness 交替迭代，不标 coevolution。
- 最终学生模型效果不能全部归因给 Harness；成本下降只含 recurring generation cost，排除一次性 authoring/debugging。
- 数字边界：同 GPT-5.4 教师、672 个 held-out 多应用任务：beta1/beta2 教师 92.0%/89.6%，相应学生 37.6%/25.1%，学生差 12.5 个百分点。
- 数字边界：最终 4B 学生的 OSWorld-Verified 66.0% 为 50 steps 设定，不是上述 beta 对照。
- 数字边界：生成 recurring cost $0.906→$0.158，下降 82.6%；未纳入 authoring/debugging 一次性成本。

### Recursa: Toward Recursively Self-Improving Foundation Model Systems — include (harness/component)

Recursa 自称运行时 harness 固定，但其 repository 中的程序性 instructions/skills 经反馈修订、回归验证与合并，符合本项目外部 Harness 工件定义。

改进对象：领域 instructions 与按需加载的程序技能（可含 scripts）；单纯 memory 内容不是纳入理由。 反馈：诊断失败轨迹，编辑 instructions/skills，重跑受影响任务及已通过样本；无回归才保留。 持留：父 learner 合并子修订，后续学习任务从合并后的组件继续。

原文短证据（[#S2.I1.i1.I1.i2.p1.1](https://arxiv.org/html/2611.04035#S2.I1.i1.I1.i2.p1.1)）：“each holds instructions and may bundle scripts and reference materials.”

- 论文自身将 runtime 与知识库分开命名；纳入依据是程序性指令/技能，不是声称其 runtime code 或 improver 自己演化。
- 递归 learner 调度不等于 improver 本身持久自改。
- 实验修改了 30 个任务中的 46 条 rubric，结果使用修订 rubric，不能称完全未修改的原始基准。
- 数字边界：150 train /100 test；DeepSeek test all-pass 30→55，Qwen 35→46；若以 bootstrap 后为起点则分别 33→55、34→46。
- 数字边界：两模型不同，最终分别采用 K2 与 K1；数字仅原文核对，无复现实验。

### HarnessFlow: MCTS-Guided Harness Optimization for LLM Agents — include (harness/evolve_main)

固定模型/环境下，用验证反馈和执行记录搜索完整可执行 Harness；树中保留候选与替代修订路径供后续搜索。

改进对象：上下文构造、状态、工具使用、终止条件与完整执行结构的可执行代码。 反馈：coding agent 按父候选与经验档案中的代码差异、验证分数和轨迹提出修订。 持留：MCTS refinement tree 保留已评估候选代码、分数和执行记录。

原文短证据（[#S2.SS0.SSS0.Px1.p1.1](https://arxiv.org/html/2611.06254#S2.SS0.SSS0.Px1.p1.1)）：“Refinements may modify mechanisms for context construction, state management, tool use, and termination”

- 相同 15 次候选评估预算并不自动证明总 tokens、美元、算力完全相同。
- 仅核对方法、选择/持留、holdout 叙述和主结果；未复现实验。
- 数字边界：六个 benchmark 均值 69.48%，较 initial +10.89 个百分点，较 MetaHarness +3.95 个百分点。
- 数字边界：15 candidates、5 repeats、coding agent 不接触 test tasks；与 baseline 对齐的是 candidate attempts。

### EnzymeRSI: A dual-loop recursive self-improvement system for enzyme design — include (harness/evolve_main)

外环对 prompts/pipelines/skills/subagents 做非参数版本演化；失败轨迹形成变更包，经匹配对照后登记并由下一次运行消费。

改进对象：研究者外部 Harness 程序资产；内环另做科学 predictor/训练方法等任务产物。 反馈：development failure trajectories 触发明确假设与最小变更包，以同模型/权限/数据/预算比较。 持留：采用后更新 version register，记录下一 run 实际消费的版本。

原文短证据（[#Sx2.SSx1.p1.1](https://arxiv.org/html/2611.06321#Sx2.SSx1.p1.1)）：“The outer loop (Harness RSI) performs non-parametric version evolution over prompts, pipelines, skills and subagents, and does not modify model weights.”

- 内环科学模型工作不等于 foundation model 与 Harness 交替共演化。
- 云实验 commission/execution/receipt 路径为规定协议；未完成端到端多轮 dry-to-wet campaign。
- 协议中的 ≥3 independent seeds 不能当成已执行实验；独立演化 seed 仍列下一步。
- 数字边界：五个 assays 的平均 Spearman +0.044 来自 development set；CD19 的 0.335/第一名由外环产出，OPSD 0.683/第一名主要源于初始配置。
- 数字边界：RLuc gap 未由内环闭合；三个 wet tests 评估决策行为，不构成多轮闭环增益证明。

### Reglos: A Self-Evolving Personal Memory Agent with Recursive Self-Improvement — include (harness/component)

外环根据失败轨迹修补冻结任务模型与 memory kernel 之间的程序，并继承 accepted Harness；每用户记忆累积是另一内环。

改进对象：extraction/retraction/recall/evidence construction/answer policy 的 Harness 代码与提示。 反馈：coding proposer 读取 raw failures，另一模型 critic 独立检查，固定 evaluator 决策。 持留：继承 accepted harness 及候选/决策记录；本文实验使用冻结 v3。

原文短证据（[#S3.SS3.p1.1](https://arxiv.org/html/2611.06049#S3.SS3.p1.1)）：“The harness is the program that sits between the memory kernel and the frozen task model and determines what the model reads.”

- 严格的双 persona-half 与 second-reader gate 在 freeze 后采用；不能声称之前五步均通过此 gate。
- inner per-user record 是状态/记忆数据，不是纳入 Harness 的依据。
- improver/verifier 固定，不称其自递归继承演化。
- 数字边界：54.2→60.7 为 1,317 validation questions 的开发轨迹，不是官方 test 增益。
- 数字边界：Persona/LME：Qwen 61.3/84.0，GPT 57.5/87.2；官方 5,000-question test 在 freeze 后运行。

### EvoGuard: Mitigating Degradation in Online Skill Evolution — include (harness/component)

固定 executor 和 generator 基于当前任务轨迹/结果重写程序性 SKILL.md，选择结果保留给同 family 后续任务。

改进对象：含 workflow、decision rules、recovery/pitfalls 的 SKILL.md；不是事实记忆条目。 反馈：生成器输入旧 skill、执行 trajectory 和 outcome，selector 判定保留旧版或新版。 持留：选中 skill 只影响之后同 family 的任务，不改变已完成任务结果。

原文短证据（[#S4.SS1.p1.1](https://arxiv.org/html/2611.06444#S4.SS1.p1.1)）：“The sections are When to use , Workflow , Decision rules , and Recovery and pitfalls .”

- offline selector LoRA 训练与 online skill evolution 分开；无交替更新证据，不标 coevolution。
- 跨任务仅同 family，非跨 family；每 benchmark 一个 selector，非通用跨域 selector。
- private skill-utility labels 的任务与 generation/online 任务分离；不能把 label set 当最终 online test。
- offline 造池不仅训练 selector：ALFWorld、ScienceWorld、WebShop 的 expert generator 从 Qwen3-4B 用 GRPO 训练；LiveCodeBench 第二来源是 GPT-6.1-sol。在线执行、生成与选择仍固定。此前建议不改变；不能把顺序 offline 训练+online技能改写标为权重/Harness交替共演化。
- 数字边界：四种 4B/8B seen/unseen 配置均值 56.5，AcceptAll 45.5，约 +11.0 个百分点；三 seeds。
- 数字边界：Table 3 science 15.3−9.4=5.9 个百分点，code 28.4−25.7=2.7 个百分点；摘要百分号此处为绝对差。

### SpecPilot: Autonomous Algorithm Discovery and Systems Optimization for Speculative Decoding — exclude (ai4ai)

程序、反馈、代码记忆和跨部署复用均存在，但演化对象是外部 speculative decoding serving/kernels，非优化 agent 自己的 Harness。

改进对象：外部推理系统的算法、kernel 和 serving patches。 反馈：correctness、token forcing 和 paired timing 驱动 patch 晋升；controller scripts 不允许 agent 修改。 持留：validated code deltas 连同 dependencies/contracts 跨 deployment 复用；此持久性不改变外部产物归属。

原文短证据（[#S3.SS2.p1.1](https://arxiv.org/html/2611.02501#S3.SS2.p1.1)）：“A sub-agent implements each direction as patches , code changes behind options whose defaults reproduce stock.”

- 不可写成无反馈、无代码或只有文本记忆；排除理由是被优化对象属于外部系统。
- 选读 3.2–3.4、5.3、6.1；没有复现实验或完整性能审计。

### Adversarial Speculative Reasoning Improves Long Horizon Agents — exclude (model_weights)

target 冻结但 draft model 在其 hidden-state features 上离线训练；实际改动对象为参数，未展示外部 Harness 版本演化。

改进对象：draft model trainable parameters。 反馈：用 continuation reward/target hidden states 训练 drafter。 持留：训练后参数被部署；不是外部程序工件反馈改写。

原文短证据（[#S4.SS4.p1.1](https://arxiv.org/html/2611.05345#S4.SS4.p1.1)）：“train the draft model offline on these features.”

- 不能因为 target model 冻结就声称整套模型未训练；trainable fractions 相对 target-plus-draft 整体。

### You don't need long context — exclude (evaluation_benchmark)

比较预设 context-management regimes；任务状态压缩循环不构成反馈驱动的持久程序更新，非 Harness 演化专项研究。

改进对象：固定 full-history/compaction/SAC 策略及任务内 compact state。 反馈：执行观测更新当前 semantic state；未展示更新管理程序或策略文件。 持留：fresh conversation 复用当前任务 compact state，系统提示和底层 Harness 不变。

原文短证据（[#S2.SS4.SSS1.Px2.p1.1](https://arxiv.org/html/2611.05306#S2.SS4.SSS1.Px2.p1.1)）：“pre-specified compaction threshold”

- 存在手工设计 context policy 与对照实验，但没有外部程序的反馈修订/持留链。
- 固定测试框架不妨碍 Harness 专项评测纳入；此处排除在于研究对象不是 Harness 演化。

### Route Anything: A Study of Model and Policy Routing for General-Purpose AI Systems — exclude (evaluation_benchmark)

路由统一理论/评测、训练型 router 与模型身份记忆写入均有；没有执行反馈改写并保留路由程序，非 Harness 演化专项研究。

改进对象：trained classifier、拟合 lookup table、outcome regressor；另有反馈验证后的 modelidentity store。 反馈：router 参数由训练数据拟合；半合成在线实验在验证接受后写入 model identity。 持留：同 cell 后续任务用最新模型身份记录；保留的是记录，不是新版本 routing code/policy artifact。

原文短证据（[#S4.SS1.SSS0.Px1.p1.1](https://arxiv.org/html/2611.05275#S4.SS1.SSS0.Px1.p1.1)）：“A Qwen3.5-4B classifier, trained on all benchmarks at once, predicts the leaf”

- 不能写成完全没有反馈或持久 memory；反馈记忆写入确实存在。
- Appendix router memory 的理论和在线记录，不等于可复用 routing 程序被改写。

## 分类差异与解决

ParetoSaddler 独立初判 generalize，主审初判 evolve_main；双方按准入与成本这一新贡献采用 generalize，范围无分歧。Mage-VL-Cowork 独立摘要初判 component，经正文确认完整教师执行程序修改后采用 evolve_main；不是 coevolution。EnzymeRSI 独立报告额外保留 ai4ai 次方向，主审暂未标次方向；不影响 include 及其外环依据。

EvoGuard 的 expert generator 在离线造池阶段确有 GRPO 训练，原文经主审提示后独立核验并补记；不将其与在线技能演化混写为权重和 Harness 的交替循环。

## 59 项逐条记录

|ID / 标题|来源推荐日|建议|深度|理由|
|---|---|---|---|---|
|[arxiv:2610.37257](https://arxiv.org/abs/2610.37257) GameVerse: A Minute-Scale Gameplay Dataset for Long-Horizon Interactive World Modeling|2026-11-05|exclude|完整原始摘要|游戏视频数据集和世界模型训练；未展示自身程序工件反馈演化。|
|[arxiv:2611.02857](https://arxiv.org/abs/2611.02857) Solv3R: 3D Looped Transformer as a Multi-view Solver|2026-11-05|exclude|完整原始摘要|训练循环 Transformer 求解几何；复用的是重建状态和表征，未改外部程序。|
|[arxiv:2611.04391](https://arxiv.org/abs/2611.04391) Human-to-Robot Transfer via Bridging Representation and Action Space in VLAs|2026-11-05|exclude|完整原始摘要|人机共训练 VLA 表征和动作解码；技能迁移属于训练策略能力。|
|[arxiv:2611.02846](https://arxiv.org/abs/2611.02846) SpecOPD: Branch-Parallel On-Policy Distillation for Speculative Decoding|2026-11-05|exclude|完整原始摘要|并行 on-policy distillation 训练 drafter；没有外部 Harness 版本循环。|
|[arxiv:2611.04634](https://arxiv.org/abs/2611.04634) VeriSpoof: Beyond Real or Fake with One Audio LLM|2026-11-05|exclude|完整原始摘要|音频模型参数训练及任务评测，不是 Harness 演化专项评测。|
|[arxiv:2611.05275](https://arxiv.org/abs/2611.05275) Route Anything: A Study of Model and Policy Routing for General-Purpose AI Systems|2026-11-04|exclude|正文选段/版本复核|路由统一理论/评测、训练型 router 与模型身份记忆写入均有；没有执行反馈改写并保留路由程序，非 Harness 演化专项研究。|
|[arxiv:2611.00617](https://arxiv.org/abs/2611.00617) Words Caught in the Heart: Simulating Person-Specific Expression for Self-Opaque Clients in Psychotherapy|2026-11-04|exclude|完整原始摘要|按治疗对话更新心理和关系状态；表达规划为固定机制，无跨任务程序修订。|
|[arxiv:2611.04814](https://arxiv.org/abs/2611.04814) Think Less, Locally: Local Preference Learning for Reasoning Compression|2026-11-04|exclude|完整原始摘要|DPO 训练局部推理停止偏好；被优化对象是模型参数。|
|[arxiv:2611.02737](https://arxiv.org/abs/2611.02737) MoviEdit: Long-form Multi-Shot Video Editing Made Easy|2026-11-04|exclude|完整原始摘要|多镜头视频编辑的数据、模型和评测，不涉及自身 Harness 改写。|
|[arxiv:2611.04916](https://arxiv.org/abs/2611.04916) Behind Video Generation: Observations and Insights on Multimodal Understanding from Kling|2026-11-04|exclude|完整原始摘要|视频理解/生成堆栈；prompt enhancement 的 RL 和单故事修订未证明可复用控制程序版本。|
|[arxiv:2611.05377](https://arxiv.org/abs/2611.05377) DreamX: Video Diffusion Model is a Universal Latent Action Learner|2026-11-04|exclude|完整原始摘要|从视频扩散特征学习潜在动作表示，不是外部程序演化。|
|[arxiv:2611.05193](https://arxiv.org/abs/2611.05193) Factorized MLLM Embeddings for Composed Image Retrieval|2026-11-04|exclude|完整原始摘要|对比学习和蒸馏优化图像检索表征，不是 Harness。|
|[arxiv:2611.02497](https://arxiv.org/abs/2611.02497) RoboColosseum: Evaluating Physical Intelligence at Scale In-The-Wild|2026-11-04|exclude|完整原始摘要|物理机器人策略及微调评测，未专门研究 Harness 持久反馈改写。|
|[arxiv:2611.03233](https://arxiv.org/abs/2611.03233) Axion 1.0: Open Agent Foundation Models, Simplified|2026-11-04|exclude|完整原始摘要|SFT/RL 和任务数据构建训练基础模型；开放 prompts/代码不等于其自动演化。|
|[arxiv:2611.05036](https://arxiv.org/abs/2611.05036) ToolSpace: Scaling Tool-Centric Environment Synthesis for Long-Horizon Agents|2026-11-04|exclude|完整原始摘要|真实工具轨迹构造训练环境、数据和任务；执行检查保留的是合成样本。|
|[arxiv:2611.05280](https://arxiv.org/abs/2611.05280) YANAMI: A Large-Scale Multimodal Dataset and Benchmark for Multiturn Stateful Interaction|2026-11-04|exclude|完整原始摘要|多轮多模态对话状态数据和评测；状态更新与模型微调不等于程序版本更新。|
|[arxiv:2611.04418](https://arxiv.org/abs/2611.04418) VidUEU-Agent: A Data-Curation Agent for Multimodal Understanding, Editing, and Unified Tasks|2026-11-04|exclude|完整原始摘要|下游训练结果驱动数据分布调整，改进对象是训练数据。|
|[arxiv:2610.39813](https://arxiv.org/abs/2610.39813) EvoTeam: Multi-Agent Collaboration via Evolving Teams|2026-11-04|include|正文选段/版本复核|团队交互规则、个体提示补丁与可复用技能经执行反馈更新，保留到后续团队和任务。|
|[arxiv:2611.03634](https://arxiv.org/abs/2611.03634) WebHarbor: Docking Real Websites for Evolving GUI Agent Environments|2026-11-04|exclude|完整原始摘要|人机协作扩建网页训练/评测环境；环境代码为外部产物，非 GUI agent 自身 Harness。|
|[arxiv:2610.39714](https://arxiv.org/abs/2610.39714) MoLRSI: A Recursive Self-Improving AI agent for Molecular Discovery|2026-11-04|borderline|正文选段/版本复核|正文既有靠经验记录改变有效搜索策略的主循环，也有新构建技能执行修复并保留；仍缺少跨任务研究者 Harness 版本链，保留边界。|
|[arxiv:2611.02501](https://arxiv.org/abs/2611.02501) SpecPilot: Autonomous Algorithm Discovery and Systems Optimization for Speculative Decoding|2026-11-04|exclude|正文选段/版本复核|程序、反馈、代码记忆和跨部署复用均存在，但演化对象是外部 speculative decoding serving/kernels，非优化 agent 自己的 Harness。|
|[arxiv:2611.02079](https://arxiv.org/abs/2611.02079) ParetoSaddler: Pareto-Guided Optimization of Agent Harnesses for Quality and Cost|2026-11-04|include|正文选段/版本复核|完整 Harness 候选经轨迹诊断修订，质量—成本联合估计控制晋升并保留候选；新贡献重心为噪声下准入与成本权衡。|
|[arxiv:2610.40747](https://arxiv.org/abs/2610.40747) Mage-VL-Cowork: A Full Training Recipe to Learn Hybrid Computer Use From Evolved Harnesses|2026-11-04|include|正文选段/版本复核|先反馈驱动演化教师完整外部执行 Scaffold/接口/提示，再固定教师 Harness 生成轨迹训练学生；外部程序循环足够明确。|
|[arxiv:2610.40753](https://arxiv.org/abs/2610.40753) "Shall We Approve?" Consequence-Aware Approval for Autonomous Coding Agents|2026-11-04|exclude|完整原始摘要|命令沙箱预执行与审批是固定防护机制，反馈纠正当前命令而非改写审批程序。|
|[arxiv:2611.04035](https://arxiv.org/abs/2611.04035) Recursa: Toward Recursively Self-Improving Foundation Model Systems|2026-11-04|include|正文选段/版本复核|Recursa 自称运行时 harness 固定，但其 repository 中的程序性 instructions/skills 经反馈修订、回归验证与合并，符合本项目外部 Harness 工件定义。|
|[arxiv:2610.40574](https://arxiv.org/abs/2610.40574) Every Token Needs Its Own Teacher: Multi-teacher Adaptive On-policy Self-distillation|2026-11-04|exclude|完整原始摘要|按 token 选择教师训练学生模型，是权重自蒸馏。|
|[arxiv:2611.04303](https://arxiv.org/abs/2611.04303) FlowTranslator: Training-Free In-Image Machine Translation with Flow-Based Editing|2026-11-04|exclude|完整原始摘要|固定免训练图像翻译流程和轨迹控制，不显示执行反馈改写控制规则。|
|[arxiv:2610.00854](https://arxiv.org/abs/2610.00854) Are Frontier VLM Agents Ready to Be Robot Generalists? An Empirical Study with the Embodied Agent Arena|2026-11-04|exclude|完整原始摘要|最小静态 Harness 下评测具身能力和当前任务恢复，非 Harness 演化专项。|
|[arxiv:2611.05306](https://arxiv.org/abs/2611.05306) You don't need long context|2026-11-04|exclude|正文选段/版本复核|比较预设 context-management regimes；任务状态压缩循环不构成反馈驱动的持久程序更新，非 Harness 演化专项研究。|
|[arxiv:2611.04870](https://arxiv.org/abs/2611.04870) PrimeSim: A Generalist World Model Simulator from Large-Scale Cross-Embodiment Demonstrations|2026-11-04|exclude|完整原始摘要|世界模型预训练/后训练及运行记忆，改的是模型参数和预测状态。|
|[arxiv:2611.02244](https://arxiv.org/abs/2611.02244) Can AI Reviewers See Your Efforts to Improve Your Paper? A Large-Scale Study of Paper Revision Trajectories|2026-11-04|exclude|完整原始摘要|研究论文修订与 AI 审稿评价，不是 Agent Harness 演化。|
|[arxiv:2611.04449](https://arxiv.org/abs/2611.04449) Near-Zero Token Embeddings Silently Stall Training in Gated Sequence Models|2026-11-04|exclude|完整原始摘要|梯度裁剪、门函数及训练失效修复，非代理运行时程序自演化。|
|[arxiv:2611.05345](https://arxiv.org/abs/2611.05345) Adversarial Speculative Reasoning Improves Long Horizon Agents|2026-11-04|exclude|正文选段/版本复核|target 冻结但 draft model 在其 hidden-state features 上离线训练；实际改动对象为参数，未展示外部 Harness 版本演化。|
|[arxiv:2611.03998](https://arxiv.org/abs/2611.03998) Dory1.0-4B: A Looped Normalized-GPT|2026-11-04|exclude|完整原始摘要|循环语言模型架构、预训练和 RLVR；潜在循环不等于外部程序演化。|
|[arxiv:2611.05163](https://arxiv.org/abs/2611.05163) RoboTryOn: Synthesizing Dexterous Robot Demonstrations from Human Videos via Virtual Try-On|2026-11-04|exclude|完整原始摘要|由人类视频合成机器人演示并训练策略，非可复用控制程序演化。|
|[arxiv:2611.02017](https://arxiv.org/abs/2611.02017) Switch-SWE: Do Coding Agents Hold Focus When Switching Between Unfinished Tasks?|2026-11-04|exclude|完整原始摘要|多任务切换评测和固定上下文模块；更新的是任务状态摘要，未改模块本身。|
|[arxiv:2611.03685](https://arxiv.org/abs/2611.03685) LOLPlay: Benchmarking Real-Time Visual Agents in League of Legends|2026-11-04|exclude|完整原始摘要|实时游戏视觉 Agent 能力评测；不研究 Harness 持久反馈演化。|
|[arxiv:2611.02568](https://arxiv.org/abs/2611.02568) SeMo3D: Unifying 3D Generation, Editing, and Completion via Selective Modeling|2026-11-04|exclude|完整原始摘要|3D 生成编辑模型和工具能力，非工具程序自身反馈改写。|
|[arxiv:2611.03806](https://arxiv.org/abs/2611.03806) BEND 2.0: Benchmarking the Capabilities Needed to Design DNA|2026-11-04|exclude|完整原始摘要|DNA 模型预测/设计能力评测，与 Harness 演化无专项关系。|
|[arxiv:2610.37914](https://arxiv.org/abs/2610.37914) Muon Makes the First Mixture-of-Experts Layer Harder to Balance|2026-11-04|exclude|完整原始摘要|MoE router 及网络优化器负载均衡研究；此 routing 位于模型参数内。|
|[arxiv:2611.03360](https://arxiv.org/abs/2611.03360) Every Pixel Is an Option: A System One Model for Medical Ultrasound Biometry|2026-11-04|exclude|完整原始摘要|超声测量模型端到端训练，非外部 Agent 程序演化。|
|[arxiv:2610.36915](https://arxiv.org/abs/2610.36915) Do We Need an LLM to Know Why Sources Conflict? Decision Models for Knowledge-Conflict Typing in RAG|2026-11-04|exclude|完整原始摘要|固定冲突分类与置信度级联评测，未展示路由代码随执行结果改写保留。|
|[arxiv:2611.01927](https://arxiv.org/abs/2611.01927) Is Your Long-Horizon Benchmark Really Deep? Measuring and Synthesizing Depth in Terminal Tasks|2026-11-04|exclude|完整原始摘要|终端任务深度测量和逐段任务合成，优化的是训练任务。|
|[arxiv:2610.41366](https://arxiv.org/abs/2610.41366) What We Keep of What We Forget: Replacement Operators and Routing Semantics in Training-Free MoE Expert Pruning|2026-11-04|exclude|完整原始摘要|MoE 专家裁剪的算子和路由语义，属模型结构/推理研究。|
|[arxiv:2611.04467](https://arxiv.org/abs/2611.04467) Is Forgetting Unified? Exploring Concept Unlearning in Unified Multimodal Models|2026-11-04|exclude|完整原始摘要|统一多模态模型概念遗忘及基准，不是 Harness 程序演化。|
|[arxiv:2610.39251](https://arxiv.org/abs/2610.39251) Where to Learn and How Far to Roll Out: Efficient Adaptive Training for GUI Agents|2026-11-04|exclude|完整原始摘要|GRPO 训练位置和 rollout 长度分配；可恢复 checkpoint 是环境状态，不是程序版本。|
|[arxiv:2611.00352](https://arxiv.org/abs/2611.00352) Cross-Prompt Reuse of Entity-Replacement Responses|2026-11-04|exclude|完整原始摘要|冻结权重上的隐状态变换跨提示迁移，未改外部可复用 Harness 工件。|
|[arxiv:2611.04414](https://arxiv.org/abs/2611.04414) SphereFlow: Missing Modality Imputation via Geometric Transport on Hypersphere|2026-11-04|exclude|完整原始摘要|跨模态生成表示和流匹配训练，非 Harness。|
|[arxiv:2611.04785](https://arxiv.org/abs/2611.04785) Kierston & KierstonBench: Simulation of Allentown, PA and Evaluation of Language Models in Crime Investigation and Surveillance Tasks|2026-11-04|exclude|完整原始摘要|记录调查/监控能力评测，未专门评测 Harness 演化。|
|[arxiv:2611.02476](https://arxiv.org/abs/2611.02476) GigaSpeech 3: Scaling Multi-Dialect Arabic Speech Recognition with Weakly Labeled Data|2026-11-04|exclude|完整原始摘要|多轮 noisy-student 数据标注和语音模型训练；闭环不自动变成 Harness。|
|[arxiv:2611.03183](https://arxiv.org/abs/2611.03183) Auto-Research Agent on MSA Organization to Improve Protein-Protein Complex Structure Prediction|2026-11-04|exclude|完整原始摘要|冻结 AF3 上对每个蛋白目标迭代 MSA/配对产物；未见跨任务程序修订。|
|[arxiv:2611.05255](https://arxiv.org/abs/2611.05255) Going Deeper With Memories|2026-11-04|exclude|完整原始摘要|字节模型层级架构与 fast-weight memory，不是外部程序工件。|
|[arxiv:2611.03747](https://arxiv.org/abs/2611.03747) Enhancing Stock Market Information Retrieval with Retrieval-Augmented Generation|2026-11-04|exclude|完整原始摘要|股票 RAG 固定系统及响应质量/时延评测，无反馈演化程序。|
|[arxiv:2611.04166](https://arxiv.org/abs/2611.04166) Say the Same, Act Differently: Diagnosing and Steering Text-Action Divergence in Reasoning VLAs|2026-11-04|exclude|完整原始摘要|VLA 视觉扰动和文本动作失配诊断，未涉及 Harness 持久改写。|
|[arxiv:2611.01621](https://arxiv.org/abs/2611.01621) FinForesight: A Diagnostic Backtesting Benchmark for Deep Research Systems in Financial Forecasting|2026-11-04|exclude|完整原始摘要|金融预测回测与检索时点控制评测；harness-compatible 不等于 Harness 演化专项。|
|[arxiv:2611.06254](https://arxiv.org/abs/2611.06254) HarnessFlow: MCTS-Guided Harness Optimization for LLM Agents|其他 arXiv；无 HF 推荐日|include|正文选段/版本复核|固定模型/环境下，用验证反馈和执行记录搜索完整可执行 Harness；树中保留候选与替代修订路径供后续搜索。|
|[arxiv:2611.06321](https://arxiv.org/abs/2611.06321) EnzymeRSI: A dual-loop recursive self-improvement system for enzyme design|其他 arXiv；无 HF 推荐日|include|正文选段/版本复核|外环对 prompts/pipelines/skills/subagents 做非参数版本演化；失败轨迹形成变更包，经匹配对照后登记并由下一次运行消费。|
|[arxiv:2611.06049](https://arxiv.org/abs/2611.06049) Reglos: A Self-Evolving Personal Memory Agent with Recursive Self-Improvement|其他 arXiv；无 HF 推荐日|include|正文选段/版本复核|外环根据失败轨迹修补冻结任务模型与 memory kernel 之间的程序，并继承 accepted Harness；每用户记忆累积是另一内环。|
|[arxiv:2611.06444](https://arxiv.org/abs/2611.06444) EvoGuard: Mitigating Degradation in Online Skill Evolution|其他 arXiv；无 HF 推荐日|include|正文选段/版本复核|固定 executor 和 generator 基于当前任务轨迹/结果重写程序性 SKILL.md，选择结果保留给同 family 后续任务。|

完整引句、HTML locator、原始响应哈希、官方版本日期、旧意见复用、主审逐项比较见 [independent-review.json](independent-review.json)。

主审当前文件 SHA256：`b3c0404e6e878d375b53bdc2192d4fc168f37a6fbbd4e46d16012ad41b71b93e`；新增 Reglos 冻结后 gate 与 Route Anything 模型身份记忆引句已独立逐段匹配。

后续 S2 历史补入批次与 RSS 抽核独立成文，不计入本 59 项的阅读或一致率。
