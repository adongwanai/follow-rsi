# 2026-10-27 原 25 篇日报分类与日期审计

本报告以 owner 的人工复审 YAML 为纠正基准：**保留 Harness 8 篇，待审 1 篇，转其他 RSI 方向 6 篇，相关评测/综述 4 篇，剔除 6 篇**。25 个 ID 全部对应，无重复、无遗漏。仅记录审计，不修改源数据或发布内容。

原自动主类为 Harness 20 篇、评测 4 篇、综述 1 篇。按 owner 本次准入决定，Harness 标签保留 8/20（40%）；其中 1 篇仍待审。这个比例不代表全量检索召回率，也不是完整实验真伪判定。

## 判据与审阅深度

核心 Harness：权重冻结或非主要训练对象；根据执行/评估反馈修改提示、工具/技能、上下文或记忆管理机制、控制流、验证器或改进器；被接受修改在后续任务/轮次复用。模型策略训练、训练系统、外部研究/工程产物、纯经验条目与固定框架不进入核心。

外部适应或 Harness 自改进，不自动等于改进器本身被递归更新。direct_mechanism 只表示作者明示机制，不表示本报告已核实实验增益。

逐篇读了 25 篇摘要；用 HF 元数据 API 对标题、发表时间和摘要逐项核对，全数匹配。另审阅 9 篇的 arXiv HTML 方法/协议段落。以下 42 段摘要引文按原字符串核验，23 段 HTML 引文按 NFKC 与空白归一化核验。没有进行完整性能、代码或证据徽标审计。

## 日期结论

日报按原始 HF 每日响应的 days 键（推荐榜日期）分期，独立展示 HF publishedAt（原发表日期）。本地 first_seen 不是榜单日，publishedAt 也不是榜单日。

**原列表只有 4 篇属于 10/27 的 HF 推荐榜**：Skill^∞（保留 Harness），Δτ-Bench、Continual Learning Exam、Trustworthy RSI survey（相关评测/综述）。其余 21 篇是 10/14–10/26 榜单的推荐；可进入“创刊回顾 10.14–10.27”，不能包装成 10/27 全部新发表。

HF 的 publishedAt 与原日报一致；本报告尚未独立核对 arXiv v1 投稿历史。25 条在缓存原始 days 响应中均只有一个推荐日期，且与 submittedOnDailyAt 的日期一致。

## 需保留的事实与口径差异

- MemPilot 的 10/05 是原发表日，10/20 是推荐榜日；在 HF 回顾窗口内，但仍按 owner single_round_training 剔除。
- DiscoveryRSI 正文明确有独立的 Harness replay 与后继轮次接受。按 owner 归 ai4ai 主类不等于它没有 Harness 更新。
- TokenWorth 正文明确冻结 backbone 并更新外部 memory management policy；按 owner 归经验类，保留“管理策略 vs 代码”边界差异。其 HTML 与 HF 标题不同，版本未另行核对。
- JockeyBench 正文有跨日程序更新、持久化和冻结对照。按 owner off_topic 剔除，但“不评测自改进”不能作为绝对事实。
- CarryOn (robot) 保持 defer；摘要声明恢复技能经失败反思精炼并复用，但未完成正文对照审查。
- code_released 的 owner 输入值仅作为原始决定保存；本次没有独立核查仓库可用性/许可证，未提升为证据徽标。
- 未抓取 PDF 或 X；SwarmRSI 的 HTML 只返回目录/标题，未将 HTTP 200 当作已读全文。

## 25 条映射（按原发表日期升序）

| # | 论文 | 原发表日（HF） | HF 推荐榜日 | owner 决定 |
|---|---|---|---|---|
| 1 | [MemPilot](https://huggingface.co/papers/2610.06830) | 2026-10-05 | [2026-10-20](https://huggingface.co/papers/date/2026-10-20) | 剔除 |
| 2 | [FlowState](https://huggingface.co/papers/2609.34565) | 2026-10-08 | [2026-10-21](https://huggingface.co/papers/date/2026-10-21) | 剔除 |
| 3 | [ViewCraft](https://huggingface.co/papers/2610.15915) | 2026-10-11 | [2026-10-14](https://huggingface.co/papers/date/2026-10-14) | 保留 Harness |
| 4 | [EAU](https://huggingface.co/papers/2610.16523) | 2026-10-12 | [2026-10-21](https://huggingface.co/papers/date/2026-10-21) | 转入其他 RSI 方向 |
| 5 | [DuoDiscover](https://huggingface.co/papers/2610.17184) | 2026-10-12 | [2026-10-19](https://huggingface.co/papers/date/2026-10-19) | 转入其他 RSI 方向 |
| 6 | [Socratic Skill Learning](https://huggingface.co/papers/2610.17860) | 2026-10-13 | [2026-10-22](https://huggingface.co/papers/date/2026-10-22) | 保留 Harness |
| 7 | [CarryOn (Pack Light)](https://huggingface.co/papers/2610.18784) | 2026-10-13 | [2026-10-19](https://huggingface.co/papers/date/2026-10-19) | 剔除 |
| 8 | [SwarmRSI](https://huggingface.co/papers/2610.20431) | 2026-10-14 | [2026-10-15](https://huggingface.co/papers/date/2026-10-15) | 转入其他 RSI 方向 |
| 9 | [JockeyBench](https://huggingface.co/papers/2610.19589) | 2026-10-14 | [2026-10-26](https://huggingface.co/papers/date/2026-10-26) | 剔除 |
| 10 | [CarryOn (robot)](https://huggingface.co/papers/2610.21453) | 2026-10-15 | [2026-10-16](https://huggingface.co/papers/date/2026-10-16) | 暂缓，待读正文 |
| 11 | [TokenEconomizer](https://huggingface.co/papers/2610.22732) | 2026-10-15 | [2026-10-19](https://huggingface.co/papers/date/2026-10-19) | 保留 Harness |
| 12 | [Librarian Agents](https://huggingface.co/papers/2610.22273) | 2026-10-15 | [2026-10-19](https://huggingface.co/papers/date/2026-10-19) | 剔除 |
| 13 | [HexaShell](https://huggingface.co/papers/2610.23479) | 2026-10-16 | [2026-10-19](https://huggingface.co/papers/date/2026-10-19) | 保留 Harness |
| 14 | [EvalResearchBench](https://huggingface.co/papers/2610.04184) | 2026-10-16 | [2026-10-23](https://huggingface.co/papers/date/2026-10-23) | RSI 相关评测/综述 |
| 15 | [DiscoveryRSI](https://huggingface.co/papers/2610.23839) | 2026-10-16 | [2026-10-19](https://huggingface.co/papers/date/2026-10-19) | 转入其他 RSI 方向 |
| 16 | [CoRE](https://huggingface.co/papers/2610.14465) | 2026-10-17 | [2026-10-26](https://huggingface.co/papers/date/2026-10-26) | 剔除 |
| 17 | [Épi](https://huggingface.co/papers/2610.24944) | 2026-10-18 | [2026-10-21](https://huggingface.co/papers/date/2026-10-21) | 转入其他 RSI 方向 |
| 18 | [GRSE](https://huggingface.co/papers/2610.27227) | 2026-10-19 | [2026-10-22](https://huggingface.co/papers/date/2026-10-22) | 保留 Harness |
| 19 | [TokenWorth](https://huggingface.co/papers/2610.26453) | 2026-10-19 | [2026-10-20](https://huggingface.co/papers/date/2026-10-20) | 转入其他 RSI 方向 |
| 20 | [TEAL](https://huggingface.co/papers/2610.27327) | 2026-10-19 | [2026-10-21](https://huggingface.co/papers/date/2026-10-21) | 保留 Harness |
| 21 | [SERA](https://huggingface.co/papers/2610.29560) | 2026-10-21 | [2026-10-22](https://huggingface.co/papers/date/2026-10-22) | 保留 Harness |
| 22 | [Δτ-Bench](https://huggingface.co/papers/2610.34238) | 2026-10-25 | [2026-10-27](https://huggingface.co/papers/date/2026-10-27) | RSI 相关评测/综述 |
| 23 | [Continual Learning Exam](https://huggingface.co/papers/2610.33956) | 2026-10-25 | [2026-10-27](https://huggingface.co/papers/date/2026-10-27) | RSI 相关评测/综述 |
| 24 | [Trustworthy RSI survey](https://huggingface.co/papers/2610.35193) | 2026-10-26 | [2026-10-27](https://huggingface.co/papers/date/2026-10-27) | RSI 相关评测/综述 |
| 25 | [Skill^∞](https://huggingface.co/papers/2610.35434) | 2026-10-26 | [2026-10-27](https://huggingface.co/papers/date/2026-10-27) | 保留 Harness |

## 逐篇依据

### 1. MemPilot · 2610.06830

MemPilot: Orchestrating On-Demand Multimodal Memory Curation for LLM Agents

**决定：剔除。** 原发表 2026-10-05；HF 推荐 2026-10-20。

原主类：`harness` / `component`；原理由：摘要称用强化学习优化多步LLM策略，控制记忆检索与整理，策略可持久复用。

暂定机制类别：`model_policy_training`；直接/交叉关系：`no_direct_harness_evolution`。原标签把“训练得到的策略可复用”当成了 Harness 持续改进。摘要的主要优化对象是 LLM policy。

改进对象：由 RL 训练的多步 LLM 记忆整理策略。反馈：多目标 RL 优势与回报。持久复用：训练后策略可复用，但未显示外部 Harness 被反馈改写并跨轮保留。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.06830)）：

> Specifically, we optimize a multi-step LLM policy via reinforcement learning to iteratively choose between retrieving from query-agnostic memory and delegating query-specific curation of raw multimodal history to heterogeneous LLMs and VLMs.

**口径/事实备注：** 保留 single_round_training 剔除决定。日期理由需修正：论文发表于 10/05，但 HF 推荐日为 10/20，处在 10/14–10/27 推荐榜回顾窗口。

不确定项 / 下一步正文核查：若以后重审，应查训练阶段/部署阶段是否另有外部工件的多轮接受与复用；摘要不能证明这种机制。

### 2. FlowState · 2609.34565

FlowState: Execution State as Memory for Long-Horizon LLM Agents

**决定：剔除。** 原发表 2026-10-08；HF 推荐 2026-10-21。

原主类：`harness` / `component`；原理由：ISU 依输入与反馈增量更新状态，且状态跨请求持久保留复用

暂定机制类别：`task_state_management`；直接/交叉关系：`no_direct_harness_evolution`。固定的 ISU/PSA 框架维护任务状态。正文将 Update/Remove 限制为当前请求创建的状态，未显示策略/工具/管理机制的反馈演化。

改进对象：当前请求的执行状态节点与历史观察引用。反馈：输入、环境观察与当前推理反馈。持久复用：状态可跨请求保存；保存状态不等于学习可复用的策略或改写管理器。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2609.34565)）：

> Within a single execution loop, Incremental State Update (ISU) maintains the current state based on new inputs and feedback, while Progressive State Access (PSA) progressively reveals historical states and supporting evidence as needed during reasoning.

正文原文（[2.2 State Operations](https://arxiv.org/html/2609.34565)）：

> apply only to states created during the current request.

不确定项 / 下一步正文核查：若声称 Harness 自进化，需要定位被改写的可复用策略/代码以及跨任务接受实验。

### 3. ViewCraft · 2610.15915

VIEWCRAFT: Evolving What Multimodal Agents See and How They Read It

**决定：保留 Harness。** 原发表 2026-10-11；HF 推荐 2026-10-14。

原主类：`harness` / `component`；原理由：失败轨迹驱动修订，回放与配对评估保留有效改动，学得技能可迁移复用

暂定机制类别：`direct_harness_candidate`；直接/交叉关系：`direct_mechanism_described`。摘要同时给出外部对象、修订反馈、接受机制及复用；符合 owner component 准入。

改进对象：可执行证据接口及其读取过程/技能。反馈：失败轨迹、重放、配对评估。持久复用：有益修改被保留，学习的技能可跨执行器迁移。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.15915)）：

> We introduce ViewCraft, which jointly evolves an executable evidence interface and its reading procedure.

> Failure traces guide revisions, replay and paired evaluation retain useful changes, and interface projection recovers visual edits from eligible rejected joint proposals.

不确定项 / 下一步正文核查：正文仍需核实留出划分、配对预算、接受协议和可复现代码；本报告不核准性能/代码徽标。

### 4. EAU · 2610.16523

EAU: Environment-Agent-User Co-evolution for Training User-Centric Agents

**决定：转入其他 RSI 方向。** 原发表 2026-10-12；HF 推荐 2026-10-21。

原主类：`harness` / `coevolution`；原理由：元智能体诊断失败并修改用户模拟器/环境/奖励/RL配置，且改动跨运行持久保留

暂定机制类别：`training_system_coevolution`；直接/交叉关系：`cross_related_training_system`。确有反馈驱动的持久协同演化，但对象是训练系统；按 owner 归 data_task，次类 model_weights。

改进对象：用户模拟器、训练环境、奖励设计和 RL 配置，同时训练 LLM policy。反馈：训练轨迹、工具日志、奖励与统计。持久复用：验证后的训练设置跨运行保留。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.16523)）：

> During training, EAU monitors trajectories, tool traces, rewards, and training statistics; diagnoses failures and uninformative interactions; and proposes targeted modifications to the user simulator, environment, reward design, and RL configuration.

> These adaptations also persist across runs, so later training can build on previously discovered improvements rather than restarting from a fixed setup.

不确定项 / 下一步正文核查：若扩大到 training Harness，应单独定义范围；当前不并入推理时 Harness 核心数。

### 5. DuoDiscover · 2610.17184

DuoDiscover: Scaling Autonomous Discovery Beyond the Evaluation Bottleneck

**决定：转入其他 RSI 方向。** 原发表 2026-10-12；HF 推荐 2026-10-19。

原主类：`harness` / `evolve_main`；原理由：用保真测试淘汰漂移的代理评估器，并把确认成果传给新智能体，修改被保留

暂定机制类别：`external_artifact_optimization`；直接/交叉关系：`cross_related_evaluator_design`。任务产物优化与评估器协同设计不能直接等同于 Agent 自我改写。读到的 worker 是现成 coding agent；按 owner 转 ai4ai。

改进对象：外部软件/内核/芯片优化目标及其专用代理评估器 yardstick。反馈：真实目标下的保真度检查与代理评分。持久复用：已确认工程成果传给新 worker；尚未显示通用 agent Harness 自身跨任务改写。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.17184)）：

> First, each worker in a fleet of coding agents co-discovers an optimization target and a fast, tailored proxy evaluator, which we call a yardstick.

> Second, since search can exploit gaps between a yardstick and the true objective, fidelity tests continually recheck each yardstick's ranking and invalidate any that drift.

正文原文（[2 DuoDiscover: Co-discovering targets and yardsticks](https://arxiv.org/html/2610.17184)）：

> The building block of DuoDiscover is the worker agent, an off-the-shelf LLM coding agent,

正文原文（[2.2 Co-discovery: Targets and their yardsticks](https://arxiv.org/html/2610.17184)）：

> When optimizing vLLM for performance, one agent targeted the scheduler’s prefill batching and wrote a yardstick that was a simple model of decode-step time, which runs in seconds while the true evaluation takes 85 minutes.

不确定项 / 下一步正文核查：若以后主张其为 Harness 方法，需区分任务专用 yardstick 与可继承的 agent 验证器/控制流，并查跨任务保留证据。

### 6. Socratic Skill Learning · 2610.17860

Socratic Skill Learning: Interleaving Teaching and Practice for Transferable Agent Skills

**决定：保留 Harness。** 原发表 2026-10-13；HF 推荐 2026-10-22。

原主类：`harness` / `component`；原理由：Student 自行编写并修订 Skill，供后续会话复用

暂定机制类别：`direct_harness_candidate`；直接/交叉关系：`direct_mechanism_described`。修改的是外部程序性技能，作者明确给出修订与复用；符合 component。

改进对象：Student 编写、实践并修订的 Skill 文件。反馈：Educator 指导、实践与未解决问题。持久复用：技能在新 solver 会话和留出用例复用。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.17860)）：

> An Educator guides investigation while the Student remains the sole environment operator and Skill author, able to question, test, and adapt advice.

> To test reuse beyond the learning task, we construct SkillTransferBench, with 35 task families and 408 executable cases, pairing public variation specifications with held-out evaluation in fresh solver sessions.

不确定项 / 下一步正文核查：核实教师成本、技能获取阶段和留出任务隔离；不将教师辅助学习写成完全自主递归更新。

### 7. CarryOn (Pack Light) · 2610.18784

Pack Light, CarryOn: Building Object-Oriented Context for Long-Horizon Agents

**决定：剔除。** 原发表 2026-10-13；HF 推荐 2026-10-19。

原主类：`harness` / `component`；原理由：摘要称按绑定证据修订受影响记录、保留未受影响记录，跨折叠维持可复用上下文。

暂定机制类别：`task_state_management`；直接/交叉关系：`no_direct_harness_evolution`。固定 Tracker/Grounder/Compiler 流程维护任务状态，不能因记录有 successor version 就认定 Harness 演化。

改进对象：任务进展对象、续接记录与执行上下文。反馈：原证据和环境条件检查。持久复用：跨同一任务的上下文折叠保留工作进展；尚非跨任务程序性能力学习。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.18784)）：

> CarryOn maintains carrier records across folds, revising affected records against bound evidence and applicable environment checks while carrying forward unaffected records and jointly updating execution context.

正文原文（[3.2 Context View](https://arxiv.org/html/2610.18784)）：

> External objects are work products that exist independently in the environment and can be reopened or modified, such as code files, documents, and spreadsheets.

正文原文（[3.3 Validation and Commitment](https://arxiv.org/html/2610.18784)）：

> These checks guard the runtime against inconsistent or unsupported updates; they do not verify task correctness.

不确定项 / 下一步正文核查：重审须定位跨独立任务学习的技能/策略、被更新的管理规则或工具代码；不能把工作产物状态直接当学习工件。

### 8. SwarmRSI · 2610.20431

SwarmRSI: Recursive Self-Improvement through Evolving Scientific Agent Swarm

**决定：转入其他 RSI 方向。** 原发表 2026-10-14；HF 推荐 2026-10-15。

原主类：`harness` / `evolve_main`；原理由：用实验反馈闭环进化agent群，保留假设跨智能体复用并累积经验

暂定机制类别：`scientific_artifact_evolution`；直接/交叉关系：`harness_scope_unresolved`。摘要明确演化科研对象，未明确说明 agent 的技能、工作流或改进机制被修改。按 owner 主类 ai4ai；独立初审曾保留边界待确认。

改进对象：科学假设与实现程序、可交换研究经验。反馈：其他 agent 的实验反馈及后续实验。持久复用：假设和互补程序跨 agent 复用；摘要声称经验可迁移到留出任务。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.20431)）：

> We devise Feedback-Guided Swarm Mutation to refine hypotheses and their implementations using experimental feedback from other agents.

> Further evaluations show that accumulated research experience improves performance on held-out tasks.

读取限制：HTTP 200 不代表已读全文。本次 SwarmRSI HTML 仅提取到页面控件/目录，未用 PDF 或 X 补抓。

不确定项 / 下一步正文核查：arXiv HTML 返回目录和标题但未取得方法正文；须继续读 3.2–3.4 与 C.2，区分研究状态继承和 Harness 策略继承。

### 9. JockeyBench · 2610.19589

JockeyBench: Evaluating LLM Agents on Horse-Racing Decision-Making

**决定：剔除。** 原发表 2026-10-14；HF 推荐 2026-10-26。

原主类：`evaluation_benchmark` / `None`；原理由：摘要称可复用程序工作流在后续赛次复用LLM写的预测器，配对检验测出修订增益与回退

暂定机制类别：`related_evaluation`；直接/交叉关系：`cross_evidence_of_persistent_program_revision`。它主要是窄领域预测基准，不应并入核心 Harness 方法。但正文确实评估持续程序修订，不能概括成完全不评测自改进。按 owner reject 执行，保留事实分歧。

改进对象：跨日复用的预测程序和证据获取程序。反馈：每日结果、聚合评分与冻结初始程序对照。持久复用：代码、拟合参数及笔记跨会话保存；获取程序根据反馈更新。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.19589)）：

> The protocol combines time-gated evidence, priced tools, paired frozen-program controls, and two workflows: executing an LLM-written predictor or acquiring evidence for a fresh per-race LLM forecast.

> Across 28 model--scaffold configurations on 324 races, paired tests identify seven revision gains and two declines after multiple-testing correction.

正文原文（[3.2 Program workflow and frozen controls](https://arxiv.org/html/2610.19589)）：

> Conversations restart between sessions; only code, fitted parameters, and notes persist, not training data.

正文原文（[3.3 Adaptive Acquisition workflow](https://arxiv.org/html/2610.19589)）：

> an LLM-written acquisition program selects evidence for a fresh per-race LLM forecast.

正文原文（[3.3 Adaptive Acquisition workflow](https://arxiv.org/html/2610.19589)）：

> The program and released aggregate feedback persist across days; per-race forecasting conversations do not.

**口径/事实备注：** 决定保持 reject/off_topic；理由宜写“非本仓库核心主题”。正文 3.2–3.3 存在更新、持久化和冻结对照，因此“不评测自改进系统”过于绝对。

不确定项 / 下一步正文核查：若以后收入相关评测，核实其获取程序是否当作 agent 证据接口，以及修订/冻结对照的统计设计。

### 10. CarryOn (robot) · 2610.21453

CarryOn: A Dual-Loop Harness for Personalized and Reliable Robot Assistance

**决定：暂缓，待读正文。** 原发表 2026-10-15；HF 推荐 2026-10-16。

原主类：`harness` / `component`；原理由：恢复技能经反思精炼并复用，持久上下文随交互修订

暂定机制类别：`deferred_harness_candidate`；直接/交叉关系：`direct_mechanism_claim_needs_fulltext`。独立初筛看到恢复技能的反馈改进声明；owner 要求更高证据门槛，故 defer。固定双环架构本身不等于自进化。

改进对象：固定 VLA 外的恢复技能，以及用户/场景上下文。反馈：执行失败反思、后续观察。持久复用：摘要说精炼后的技能被复用，但须查跨任务范围与自动修订方式。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.21453)）：

> When execution fails, the system invokes reusable control-based recovery skills that restore task progress and are refined through reflection on earlier failures.

> increases recovery success from 13% to 80% when refined skills are reused.

不确定项 / 下一步正文核查：必须读方法、恢复技能实例与对照：谁改技能、修改什么、何时冻结、是否跨任务/场景保留；本次未读正文，不升格。

### 11. TokenEconomizer · 2610.22732

TokenEconomizer: Experience-Driven Black-Box Cost Control for Coding Agents

**决定：保留 Harness。** 原发表 2026-10-15；HF 推荐 2026-10-19。

原主类：`harness` / `component`；原理由：外部控制器按任务序列修剪持久无关工具、注入微技能，属于基于反馈的持久修改

暂定机制类别：`direct_harness_candidate`；直接/交叉关系：`direct_mechanism_described`。正文明确外部 controller 从轨迹学习 repository-specific policy，作用于指令前缀、工具集和事件流；符合 component。

改进对象：注入的微技能、工具可用集、失败循环干预策略。反馈：已完成任务轨迹、技能确认/反证、工具使用记录。持久复用：以仓库状态保存，并只用先前完成任务影响下一任务；技能可激活或退役。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.22732)）：

> To minimize these costs, we introduce TokenEconomizer, an external controller that cuts environment-specific token costs over a sequence of tasks.

> These cuts come from determining (i) which operational micro-skills to inject, (ii) which persistently irrelevant tools to prune, and (iii) when to intervene in unproductive failure loops.

正文原文（[3 TokenEconomizer](https://arxiv.org/html/2610.22732)）：

> an external controller that applies three repository-agnostic meta-strategies to learn repository-specific policies from completed traces.

正文原文（[3.1 Meta-strategy I: Experience-grounded Micro-skills](https://arxiv.org/html/2610.22732)）：

> These records enter S i S_{i} and decide which skills are activated or retired

正文原文（[4 Experiments](https://arxiv.org/html/2610.22732)）：

> Within a repository, tasks run in chronological order, so the controller only learns from work that came earlier in that repository’s history.

不确定项 / 下一步正文核查：后续证据卡需核实总 token 预算是否包括 controller、任务排序与泄漏边界；不把固定 meta-strategy 写成自我改写改进器。

### 12. Librarian Agents · 2610.22273

Librarian Agents: Training LLMs to Curate Long-Context Workspaces that Anticipate Future Queries

**决定：剔除。** 原发表 2026-10-15；HF 推荐 2026-10-19。

原主类：`harness` / `component`；原理由：用强化学习按下游回答准确率优化builder策略，产物可复用

暂定机制类别：`model_policy_training`；直接/交叉关系：`no_direct_harness_evolution`。主要更新对象为 RL 训练的策略，复用的结果是数据工作区；符合 owner single_round_training 剔除。

改进对象：构建知识工作区的 LLM builder policy。反馈：下游回答正确率作为 RL 目标。持久复用：生成的 workspace 供未来查询用；这不是同一 Harness 的多轮反馈修订证据。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.22273)）：

> We formulate workspace construction as a Markov decision process and optimize the builder policy via reinforcement learning to directly maximize downstream answering accuracy.

不确定项 / 下一步正文核查：如要重收，须找到除训练 policy 外的独立持久 Harness 更新循环。

### 13. HexaShell · 2610.23479

HexaShell: A Thin Harness for Exploring the Limits of VLM Agents as Robot Coding Agents

**决定：保留 Harness。** 原发表 2026-10-16；HF 推荐 2026-10-19。

原主类：`harness` / `component`；原理由：每次失败后读日志编写或修复工具，把所学保留为代码并冻结，在新布局上复用测试

暂定机制类别：`direct_harness_candidate`；直接/交叉关系：`direct_mechanism_described`。thin harness 并不排除外部工具库演化；摘要清楚说明失败→写/修工具→保存代码→新布局复用。

改进对象：机器人感知/控制的小程序工具。反馈：失败日志和修复。持久复用：先在十个布局构建工具，再冻结并测试十个新布局。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.23479)）：

> After each failed attempt, the agent reads the log, finds the cause, and writes or fixes small programs called tools.

> We build the tools on only ten layouts of one seed per task, then freeze them and test them on ten new layouts of the same seed.

不确定项 / 下一步正文核查：正文核实 seed/任务隔离、人工干预、预算和失败数据复用；冻结新布局不自动等价于跨任务泛化。

### 14. EvalResearchBench · 2610.04184

EvalResearchBench: Can AI Agents Build Their Own Feedback for Recursive Self-Improvement?

**决定：RSI 相关评测/综述。** 原发表 2026-10-16；HF 推荐 2026-10-23。

原主类：`evaluation_benchmark` / `None`；原理由：agent据pilot反馈修正任务与grader并冻结评估器供后续使用

暂定机制类别：`related_evaluation`；直接/交叉关系：`cross_related_evaluator_design`。是自主评测研究基准。环内验证器是 Harness 相关对象，但未证明研究 agent 自身改进机制被递归更新；按 owner 放相关评测。

改进对象：Agent 产出的评测任务与 grader。反馈：pilot tests 和开发参考。持久复用：生成的 evaluator 冻结后在目标/封存目标上比较。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.04184)）：

> Given target materials, development references, candidate APIs, and fixed time and API budgets, an agent called the researcher selects or synthesizes tasks, implements graders, and revises them in pilot tests before freezing an executable evaluator for coding, co-work, and reasoning.

> Agents repair tasks and graders through pilot feedback, yet their evaluators can still truncate answers, exhaust the evaluation budget, or let a few questions dominate a domain score.

不确定项 / 下一步正文核查：区分被研究的 evaluator 工件与研究者自身 Harness；正文核实封存目标隔离和成本。

### 15. DiscoveryRSI · 2610.23839

DiscoveryRSI: Recursively Learning to Discover Valuable Hypotheses

**决定：转入其他 RSI 方向。** 原发表 2026-10-16；HF 推荐 2026-10-19。

原主类：`harness` / `evolve_main`；原理由：rediscovery 把接受的改进用于新研究，跨轮保留

暂定机制类别：`direct_harness_coevolution_candidate`；直接/交叉关系：`direct_harness_component_with_model_updates`。按 owner 主类 ai4ai、次类 model_weights，不进入核心计数；但正文有独立且持久的 Harness replay 更新机制，不能把它抹去。

改进对象：科研假设、模型权重，以及研究协调/证据访问/复审时机/分工工作流。反馈：研究贡献评价、重复失败诊断、匹配预算开发评估。持久复用：模型与 Harness 候选分别/联合接受，进入下一轮新问题研究。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.23839)）：

> harness replay identifies productive strategies and recurring failures to refine research workflows; and rediscovery applies accepted improvements to new investigations, generating further experience for subsequent learning.

正文原文（[3.4 Harness Replay](https://arxiv.org/html/2610.23839)）：

> Harness replay improves the research workflow while holding model weights fixed.

正文原文（[3.4 Harness Replay](https://arxiv.org/html/2610.23839)）：

> We adapt research coordination, evidence access, review timing, and work allocation on top of that substrate

正文原文（[3.5 Rediscovery](https://arxiv.org/html/2610.23839)）：

> The acceptance procedure evaluates qualifying updates separately and jointly, so the model, harness, both, or neither may change.

正文原文（[3.5 Rediscovery](https://arxiv.org/html/2610.23839)）：

> Scientific restart changes direction within a research run; rediscovery changes the system used for the next run.

**口径/事实备注：** 遵循 ai4ai 主类归档。与初步独立判断差异在“主对象”口径，而不是是否存在 Harness 更新：3.4–3.5 明确描述了后者。

不确定项 / 下一步正文核查：正文/附录还需核实 Harness 独立增益、匹配预算、被接受版本与新研究划分。此次 targeted HTML 不是完整实验审计。

### 16. CoRE · 2610.14465

Co-adaptive Rule Routing and Constraining for Structured Knowledge Retrieval

**决定：剔除。** 原发表 2026-10-17；HF 推荐 2026-10-26。

原主类：`harness` / `coevolution`；原理由：闭环中路由策略与检索器相互提供监督和奖励并持续共适应

暂定机制类别：`neural_component_cotraining`；直接/交叉关系：`no_direct_harness_evolution`。RL 与对比学习的交替训练不自动成为 Harness coevolution。摘要末尾 rule refinement 只是分析所支持方向，不能替代实现证据。

改进对象：规则路由策略和受规则约束的 retriever 参数。反馈：检索性能奖励与规则监督。持久复用：训练好的模型跨数据集使用；未描述外部 Harness 自我改写。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.14465)）：

> Because routing and retrieval are interdependent, CoRE alternates between reinforcement learning for the routing policy and contrastive learning for the rule-constrained retriever.

不确定项 / 下一步正文核查：若以后声称规则文件演化，需找到实际写入、接受与跨周期复用流程；当前按 off_topic 剔除。

### 17. Épi · 2610.24944

Epi: Towards a Persistent, Self-Improving Agent for Autonomous Research

**决定：转入其他 RSI 方向。** 原发表 2026-10-18；HF 推荐 2026-10-21。

原主类：`harness` / `component`；原理由：称其靠累积经验演化方法、跨会话保留研究历史，符合持久自改进

暂定机制类别：`experience_based_research_agent`；直接/交叉关系：`cross_related_persistent_experience`。正文证实固定权重与持久经验更新；owner 明确把经验条目排除于 Harness 核心，因此归 ai4ai + experience_world_model。

改进对象：研究历史、可复用经验/教训和独立复审记录。反馈：固定验证器、实验与复审反馈。持久复用：长期记忆留给后续研究，会随新证据更新。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.24944)）：

> Épi combines persistent research history, hierarchical memory, branching and independent review to maintain research continuity, learn from experiments, and explore and revisit alternative approaches.

正文原文（[2 Research Setting](https://arxiv.org/html/2610.24944)）：

> We keep model weights fixed in the campaigns reported here. The agent adapts its methods through experimental feedback, retrieved memory and independent review.

正文原文（[3.2 Self-improving Research Agents](https://arxiv.org/html/2610.24944)）：

> Short-term memory supports the current investigation, while long-term memory retains experience for subsequent research.

正文原文（[3.2 Self-improving Research Agents](https://arxiv.org/html/2610.24944)）：

> The agent retrieves these records to guide its next experiment and updates them as new evidence becomes available.

**口径/事实备注：** 初筛在宽泛外部经验适应定义下曾列为直接候选；按 owner 明确的“只积累经验条目不算 Harness”边界改归档。

不确定项 / 下一步正文核查：若按更宽的经验型 Harness 范畴纳入，仍需分离学习机制与任务解法搜索贡献；未见完整调度/改进器自改写证据。

### 18. GRSE · 2610.27227

Which Agent's Skill Should Change? Group-Relative Credit Assignment for Evolving Multi-Agent Teams

**决定：保留 Harness。** 原发表 2026-10-19；HF 推荐 2026-10-22。

原主类：`harness` / `component`；原理由：改写可复用技能，且学到的技能可跨多跳任务迁移，修改被保留复用。

暂定机制类别：`direct_harness_candidate`；直接/交叉关系：`direct_mechanism_described`。权重冻结、技能修订、信用分配与迁移均明确；符合 component。

改进对象：多 Agent 可复用技能库。反馈：同题多次执行的相对比较、团队奖励与结构化失败诊断。持久复用：修订技能在后续任务使用，摘要报告多跳任务之间迁移。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.27227)）：

> Cooperative language-model agents can improve without weight updates by revising reusable skills, but only if a shared team reward is traced to the responsible agent and skill.

> Its gains rest on better-grounded retrieval rather than answers given without evidence, and its learned skills transfer between the multi-hop tasks.

不确定项 / 下一步正文核查：核实技能修改/接受规则及所有比较的预算；GRPO 启发不等于模型参数 RL。

### 19. TokenWorth · 2610.26453

Remembering Has a Price: Learning Memory Worth under Resource Constraints

**决定：转入其他 RSI 方向。** 原发表 2026-10-19；HF 推荐 2026-10-20。

原主类：`harness` / `component`；原理由：它从执行反馈学习记忆价值，并持久用于后续检索与记忆管理，构成终身改进闭环

暂定机制类别：`experience_memory_policy_adaptation`；直接/交叉关系：`cross_related_external_memory_policy`。按 owner 归 experience_world_model。正文明确更新管理 policy，不能只写成保存静态记忆；是否算 Harness“策略”需要统一类别边界。

改进对象：记忆条目价值、在线 scorer、外部 memory bank 的检索与管理策略。反馈：稀疏任务执行反馈。持久复用：固定 backbone 下，在线管理策略和记忆 bank 跨任务更新。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.26453)）：

> To address this challenge, we propose TokenWorth, a lightweight online memory framework that learns query-dependent memory worth from sparse execution feedback and applies it consistently to memory retrieval and bounded memory management.

正文原文（[3 Resource-Constrained Lifelong Agents](https://arxiv.org/html/2610.26453)）：

> We focus on a frozen-backbone setting, where experience-driven adaptation occurs through online updates to external memory and its management policy, rather than model parameters.

正文原文（[3 Resource-Constrained Lifelong Agents](https://arxiv.org/html/2610.26453)）：

> Through execution feedback, this policy can adapt how accumulated experience influences future decisions without modifying the backbone.

**口径/事实备注：** 遵循 experience_world_model 归档。owner 判据包括“记忆管理的代码或策略”，但排除此篇的理由偏重“不是代码”；这是分类边界的一处需记录差异，不能据此自动改动名单。

不确定项 / 下一步正文核查：正文标题为 Learning What to Remember: Resource-Efficient Self-Improvement for Lifelong Agents，与 HF 标题不同，版本对应尚未独立查清；需核实 scorer 更新与管理代码/策略的边界。

### 20. TEAL · 2610.27327

Unsupervised Tool Evolution for Coding Agents in Data-Lake Analytics

**决定：保留 Harness。** 原发表 2026-10-19；HF 推荐 2026-10-21。

原主类：`harness` / `component`；原理由：跨任务演化可复用工具库，仅保留Worker复跑能采用的修改

暂定机制类别：`direct_harness_candidate`；直接/交叉关系：`direct_mechanism_described`。完整包含改进对象、反馈、接受与复用，符合 component。

改进对象：可复用工具库和用法技能。反馈：数据湖、Worker 轨迹、重跑采用及答案证据。持久复用：只有通过使用/证据条件的修改保留，库跨问题复用。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.27327)）：

> We propose TEAL (Tool Evolution for Analytics over data Lakes), which evolves a library of tools and usage skills for a given Worker agent without labels.

> A proposed change is kept only if the Worker adopts the tool on a rerun without extra steps and any changed answer is supported by trajectory evidence.

不确定项 / 下一步正文核查：核查无标签接受是否会循环自证、演化/最终测试问题隔离及总体成本；本报告不核准开源状态。

### 21. SERA · 2610.29560

From VLM Planners to Robotic Agents: Self-Evolving Harnesses for History-Dependent Manipulation

**决定：保留 Harness。** 原发表 2026-10-21；HF 推荐 2026-10-22。

原主类：`harness` / `evolve_main`；原理由：自进化修订harness并在留出测试前固定配置，修改得以保留

暂定机制类别：`direct_harness_candidate`；直接/交叉关系：`direct_mechanism_described`。摘要明确区分任务上下文维护与真正的 Harness revision；符合 evolve_main。

改进对象：高层 VLM 规划器可编辑 Harness，低层 VLA 固定。反馈：环境 rollout 和执行经验。持久复用：候选修订被选择，最终配置在留出测试前冻结。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.29560)）：

> We instantiate this approach as SERA (Self-Evolving Robotic Agent), with a fixed VLA executor providing low-level control.

> Self-evolution uses environment rollouts to propose and evaluate harness revisions, with the selected configuration fixed before held-out testing.

不确定项 / 下一步正文核查：核查 revision 的具体字段/代码、自动选择流程及预算；任务 context 更新本身不是唯一纳入理由。

### 22. Δτ-Bench · 2610.34238

Δτ-Bench: Pushing Agents Toward a Moving Capability

**决定：RSI 相关评测/综述。** 原发表 2026-10-25；HF 推荐 2026-10-27。

原主类：`evaluation_benchmark` / `None`；原理由：Steward通过增量技能维护跨任务保留程序性知识，属持久自我修改。

暂定机制类别：`related_evaluation`；直接/交叉关系：`cross_related_skill_maintenance_benchmark`。是具有明确 Harness 关联的评测及示范方法；依 owner 归 related，不计入核心方法数。

改进对象：变动工具生态下的程序性知识与技能维护。反馈：服务/工具变动、任务执行与适应表现。持久复用：Steward 以增量技能维护保留并修订知识。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.34238)）：

> Against this moving capability frontier, we evaluate whether agents can proactively discover efficient tool-use paths and promptly revise their accumulated procedural knowledge, bringing together demands that existing benchmarks fail to examine.

> These findings motivate Steward, an ecosystem manager that jointly manages tools and procedural knowledge through incremental skill maintenance and dynamic provisioning during task execution.

不确定项 / 下一步正文核查：正文需区分临时工具供应、程序性技能修改与跨生态状态复用，并核查评测隔离。

### 23. Continual Learning Exam · 2610.33956

Continual Learning Exam: Benchmarking Long-Horizon RSI and Experiential Learning in LLM Agents

**决定：RSI 相关评测/综述。** 原发表 2026-10-25；HF 推荐 2026-10-27。

原主类：`evaluation_benchmark` / `None`；原理由：CLE 专门评测智能体凭经验积累持续改进，属对可自我改进系统的评测基准

暂定机制类别：`related_evaluation`；直接/交叉关系：`cross_evidence_of_persistent_harness_state`。摘要的“一次修订”不足以单独证明学习，但正文补充了跨任务记忆/技能协议；保留相关评测，不称为新 Harness 自进化方法。

改进对象：固定模型/Harness 实现下的持久 memory/skills 等状态。反馈：任务观察、rubric 反馈和允许的重交。持久复用：正文规定 120 个任务串行，跨任务保留 Harness 状态；各任务外部数据重置。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.33956)）：

> We compare a single-submission setting with one that provides diagnostic feedback after failure and allows one revision.

> Across 17 harness-model configurations using frontier LLMs, feedback and revision yield a median completion gain of 5.3 percentage points.

正文原文（[3.1 Benchmark Design / Block-based evaluation](https://arxiv.org/html/2610.33956)）：

> executed as a single serial stream in a fixed order, with persistent harness state retained across tasks.

正文原文（[3.1 Benchmark Design / Block-based evaluation](https://arxiv.org/html/2610.33956)）：

> This state can include memories, skills, and other knowledge retained outside the model parameters. Model parameters remain fixed, while task-specific input files and application databases are initialised for each new task.

正文原文（[3.3 Problem Formulation](https://arxiv.org/html/2610.33956)）：

> When the next task starts, the environment initialises its files and application databases, while the harness carries retained knowledge into the new task and manages its current context.

不确定项 / 下一步正文核查：核实实际系统保存了什么而不只看形式定义；需消融反馈重试、上下文续接和跨任务学习的各自贡献。

### 24. Trustworthy RSI survey · 2610.35193

Trustworthy Recursive Self-Improvement in the Era of Large Models: Foundation, Risks, Evaluation and Open Challenges

**决定：RSI 相关评测/综述。** 原发表 2026-10-26；HF 推荐 2026-10-27。

原主类：`theory_survey` / `None`；原理由：综述界定RSI为持久自我修改并递归修订改进机制，属专门综述

暂定机制类别：`related_survey`；直接/交叉关系：`cross_related_rsi_theory`。相关理论/综述，明确包含 Harness 类对象，不能计为新增直接方法或性能证据。

改进对象：模型、提示、记忆、工具、工作流及未来更新机制的 RSI 定义与风险。反馈：文献综述，不是本篇新增的执行实验。持久复用：讨论持久更新与后继系统继承。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.35193)）：

> AI systems built around large models increasingly use experience and feedback to make persistent changes to models, prompts, memories, tools, and workflows.

> Recursive self-improvement (RSI) extends this process to inductive biases and to the mechanisms that govern future updates, which can themselves be revised and reused across improvement cycles.

不确定项 / 下一步正文核查：核实引用与定义适用范围；综述对 RSI 的定义不能反向证明被引用系统具有相同能力。

### 25. Skill^∞ · 2610.35434

Skill^{infty}: Recursive Self-Improvement for Agent Skill Optimization

**决定：保留 Harness。** 原发表 2026-10-26；HF 推荐 2026-10-27。

原主类：`harness` / `improver`；原理由：元技能用同一程序优化自身，并在多任务上精炼后复用来优化任务技能

暂定机制类别：`direct_recursive_improver_candidate`；直接/交叉关系：`direct_improver_self_modification_described`。明确“改进器本身”用同一过程优化并后续复用；是这批中递归更新机制描述最直接的条目，符合 improver。

改进对象：任务技能及编码优化流程的 meta-skill。反馈：执行轨迹诊断、候选、独立评审、搜索预算决策。持久复用：meta-skill 在多任务上精炼后用于不同领域技能优化。

摘要原文（[HF 元数据](https://huggingface.co/api/papers/2610.35434)）：

> We present Skill^{infty}, which makes skill optimization recursively self-improving: a meta agent follows a meta-skill to optimize task skills and optimizes the meta-skill itself using the same procedure.

> This meta-skill is also decoupled from task skills, refined on multiple skill optimization tasks and then reused to optimize task skills across diverse domains.

不确定项 / 下一步正文核查：正文需核实 meta-skill 演化/技能优化/最终测试三层分离、预算与多轮消融；摘要机制成立不等于已证实开放式递归增益。

## 校验与来源

- 原 25 条 ↔ owner 25 条：一一映射，组数合计 25；原发表日期升序。
- HF 标题/发表时间/摘要：25/25 匹配；HF raw 推荐日期：25/25 唯一且匹配 submittedOnDailyAt。
- 摘要原文：42 段精确匹配；HTML：23 段归一化匹配。
- 仅输出 ignored build/audit-daily-classification.md 与 .json；未改动源码、数据、审核决定或发布状态。

owner 复审文件：`review/corrections/2026-10-27.yaml`

原日报快照 SHA-256：`d7529a6e09560df31d8ede6603c6dc7b5e19c862166e429088aacf9daff8f5b3`

原始 HF 按日响应：`data/feed/raw/hf-daily/2026-10-27.json`

缓存现场 HF 元数据：`/tmp/follow-rsi-daily-20261027-hf-metadata.json`

本报告中的 HTML 段落索引仅用于定位本地缓存，不冒充论文页码；章节名称以正文为依据。完整结构化引文、日期、原分类、owner 决定和校验结果见同名 JSON。
