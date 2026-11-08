# 18 篇正文边界复核

以下只陈述已读章节和短引文支持的边界，不把题名自称当成结论。全部 owner 决定为 defer。

## 2610.23656 · ABF-Bench: A Verifiable Benchmark for Agentic Blockchain Forensics

[官方正文](https://arxiv.org/html/2610.23656v1) · 已读：Sections 6–7: working memory, fixed agent comparison and isolated task execution

建议：**exclude**。ABF 是人工设计的固定取证 Harness；working memory 记录当前调查进度，没有反馈驱动的跨任务程序更新。

> A working memory [ 19 ] , maintained by the agent itself [ 20 ] , that represents the progress of the investigation. It comprises three sections: findings , the confirmed operations that constitute th

定位：抽取段落 83；只规范化空白后逐字匹配。

> The harness of Section 6 runs the same model and reasoning effort as Codex, so the comparison with Codex holds the model fixed and varies the harness.

定位：抽取段落 102；只规范化空白后逐字匹配。

## 2610.34298 · Matched Capabilities, Different Behaviors: A Controlled Study of MCP and CLI Interfaces for Language Agents

[官方正文](https://arxiv.org/pdf/2610.34298) · 已读：Section 4.3; Appendices D/E: DART realization repair and unchanged ordinary policy

建议：**exclude**。DART 修复当前动作的接口表达；正文明确公共策略和消息顺序保持固定，没有保留到后续任务的 Harness 新版本。

> If the initial realization fails while 𝑐𝑡remains valid, DART keeps the commitment fixed and issues one preserving correction conditioned on the failed expression and its public feedback. The correctio

定位：抽取段落 139；只规范化空白后逐字匹配。

> The system- level policy and message ordering remain fixed. Interface-specific information enters through the rendered contract, required response surface, and visible interaction context. Outside DAR

定位：抽取段落 757；只规范化空白后逐字匹配。

## 2610.37905 · FilingLoop: Evaluating and Evolving LLM Agents for Corporate Disclosure Review and Revision

[官方正文](https://arxiv.org/html/2610.37905v1) · 已读：Sections 2.3, 3.2.3, 4: batch-locked skill editing, retention and evaluation boundaries

建议：**harness**。已评分批次的要求级反馈改写 Reviewer/Filer 技能，权重固定，新技能只供后续任务使用。

> After first-attempt results are locked, a skill editor receives the evolving arm’s completed-batch feedback: discovery outcomes, applicable requirements, fulfillment decisions, evidence quotations, an

定位：抽取段落 55；只规范化空白后逐字匹配。

> Only later, unattempted tasks use the new guidance. Model weights and base instructions remain fixed, completed cases retain their original scores, and skill updates stop after the penultimate batch.

定位：抽取段落 57；只规范化空白后逐字匹配。

> This is online adaptation with historical scoring feedback, not evaluation on an independent held-out test set. Earlier rounds of a company may inform later rounds; unseen-company generalization requi

定位：抽取段落 57；只规范化空白后逐字匹配。

论文明确这是在线历史反馈适应，不是独立留出集评估；不得把分类通过写成留出证据通过。

## 2610.38174 · Scaling Lean Theorem Proving for Real-World Code Verification

[官方正文](https://arxiv.org/html/2610.38174v1) · 已读：Sections 2, 3.1, evaluation limitations: recursive calls versus retained program edits

建议：**exclude**。递归子代理改的是当前证明和引理；正文描述固定求解架构和基准生成，没有跨任务 Harness 自改机制。

> Agents recursively delegate work to children with separate contexts and workspaces. Completed results return to the parent without waiting for unfinished siblings, which keep running; the search ends

定位：抽取段落 19；只规范化空白后逐字匹配。

> We do not ablate the individual components of the harness, because each configuration requires a full run over the benchmarks. In particular, we do not compare against the same model using Lean as a t

定位：抽取段落 68；只规范化空白后逐字匹配。

## 2610.38266 · Recursive Self-Improvement in Physical AI: Mechanisms, Evidence, and Evaluation

[官方正文](https://arxiv.org/html/2610.38266v1) · 已读：Conceptual framework and L0–L3 rubric: physical RSI and learner/improver boundaries

建议：**other_direction**。综述具身领域的策略、世界模型、记忆、技能和可执行 Harness；整体研究对象是物理 RSI，不是 Harness 专项方法。

> With robot learning and deployment as the main setting, this paper connects two strands of self-improvement in physical AI: how experience becomes persistent capability, and how it changes the process

定位：抽取段落 6；只规范化空白后逐字匹配。

> Recursion can occur within a component of the improver. For example, a system may generate and retain revised reward code, then use it to train the next policy. This establishes inheritance from rewar

定位：抽取段落 24；只规范化空白后逐字匹配。

## 2610.38392 · Masked Erosion: How Acceptance Gates Lose Redundant Safeguards in Self-Improving Agents

[官方正文](https://arxiv.org/html/2610.38392v1) · 已读：Sections 3–4, limitations: accepted-child inheritance, safety gate and model-swap scope

建议：**harness**。专项评估固定模型周围文本 Harness 的接受闸门、继承的编辑及安全冗余损失；应归 Harness 安全评测，不是新方法数量。

> an accepted child becomes the next parent. Bottom left: while another layer blocks the harm, a deletion leaves observed harm low but removes redundancy. Bottom middle: an accepted deletion either buys

定位：抽取段落 21；只规范化空白后逐字匹配。

> A harness H H is text given to a fixed model M M ; it contains a set S S of safeguard layers that the proposer may edit like any other text. Tasks come from a clean pool and a harm pool , whose tasks

定位：抽取段落 23；只规范化空白后逐字匹配。

> We study two environments, each with one harm and four written safeguards, and most loops plant one deletion per generation to isolate the gate. We chose this setting to expose how gates respond to de

定位：抽取段落 85；只规范化空白后逐字匹配。

多数循环人为施加删除压力，GEPA 只有案例研究；不得将结果概括为部署中普遍失效率。

## 2610.38568 · A-RSI: Adaptive Task Refresh for Zero-Data Multimodal Self-Improvement

[官方正文](https://arxiv.org/html/2610.38568v1) · 已读：Sections 3.1–3.4, continuation setup: static templates/pools/controller versus Solver updates

建议：**other_direction**。Solver 多个训练窗口继承权重并自生成 rollout，但模板、候选池和刷新控制器固定；明确非 Harness，广义 RSI 是否达标留给 owner。

> Before training, fixed, model-written templates generate images, questions, and program-computed answers; the pipeline checks candidates and prepares disjoint replacement pools under fixed family quot

定位：抽取段落 24；只规范化空白后逐字匹配。

> only the Solver policy is optimized.

定位：抽取段落 25；只规范化空白后逐字匹配。

> The templates and controller remain fixed. The coefficients λ fmt \lambda_{\mathrm{fmt}} and λ stop \lambda_{\mathrm{stop}} are fixed throughout training. Their values, the response limit, and optimiz

定位：抽取段落 36；只规范化空白后逐字匹配。

存在继承 Solver 权重的多窗口训练，但静态数据生成器/控制器不构成 Harness 递归。广义 RSI 准入建议保留 borderline。

## 2610.38681 · Weaken to Strengthen: Weakening-Induced On-Policy Self-Distillation for Large Reasoning Models

[官方正文](https://arxiv.org/html/2610.38681v1) · 已读：Section 3, Figure 2: fixed scorer pair, trajectories and one student optimization

建议：**exclude**。正文明确原始模型和弱化模型、轨迹与监督在优化中全程固定；属于单轮离线自蒸馏，不因题名自蒸馏纳入 RSI。

> The trajectories and both scoring models remain fixed throughout optimization. The trained student is used alone at inference time.

定位：抽取段落 31；只规范化空白后逐字匹配。

> The frozen pair scores the same self-generated trajectories, and its token-level log-probability contrast provides cached supervision for a student initialized from the original model, without privile

定位：抽取段落 21；只规范化空白后逐字匹配。

## 2610.38728 · From Grind to Grasp

[官方正文](https://arxiv.org/html/2610.38728v1) · 已读：Section 5.2: relative recursive gain under fixed work and evaluation conventions

建议：**other_direction**。给出跨代改进效率的广义 RSI 理论判据，涉及代码解释器但未限定为 Harness 演化。

> Producing a better system is a task whose work requirements can change from one generation to the next. Recursive gain applies our notion of grasp to the improvement task τ Δ \tau^{\Delta} itself, tes

定位：抽取段落 196；只规范化空白后逐字匹配。

> We call positive recursive gain across multiple generations recursive improvement , our criterion for recursive self-improvement. Each successor achieves positive recursive gain over its producer alon

定位：抽取段落 207；只规范化空白后逐字匹配。

## 2610.38796 · Routed Continual Learning

[官方正文](https://arxiv.org/html/2610.38796v1) · 已读：Sections 3–4.3: fixed library/router, bounded adapter configuration and cluster state

建议：**other_direction**。路由提示与记忆系统库固定；选择已有机制、配置和更新簇状态，不生成或改写记忆管理代码或策略。

> The router is prompted rather than trained. Its prompt and memory-system library remain fixed during evaluation, and it receives no source-task labels or rewards.

定位：抽取段落 46；只规范化空白后逐字匹配。

> An adapter supplies only schema-bounded semantic bindings and permitted configuration choices, never parser code or task answers, so online adaptation is limited to routing, bounded configuration, and

定位：抽取段落 54；只规范化空白后逐字匹配。

正文适配器只生成受限 schema 绑定与配置，不生成 parser 代码；不能把选择机制误写成改写机制。

## 2610.39122 · Appreciation Teaches Unauthorized Execution: Self-Evolution Degrades the Robustness of Personal Agents to Indirect Prompt Injection

[官方正文](https://arxiv.org/html/2610.39122v1) · 已读：Sections 3.2–3.3: separate RL/skill branches, learned skill insertion and test-time freeze

建议：**harness**。专项测试反馈写成技能后对后续会话授权判断的影响；技能演化分支符合 Harness，RL 分支单独属于权重更新。

> MetaClaw keeps the foundation model fixed and learns reusable skills from completed sessions [ 19 ] . At the end of each session, a language model called the evolver reads conversation excerpts and wr

定位：抽取段落 38；只规范化空白后逐字匹配。

> In later conversations, the framework retrieves skills and inserts them into the agent’s system prompt. Retrieval selects at most six general skills, ten skills from one task-specific category, and fi

定位：抽取段落 38；只规范化空白后逐字匹配。

> The learned weights or skill library remain fixed throughout the test phase.

定位：抽取段落 32；只规范化空白后逐字匹配。

技能演化与 RL 是两个独立实验分支；不能合并成同一代理的权重/Harness 协同演化。

## 2610.39301 · Youtu-Parsing-Omni: One Encoder, One Schema, All Modalities

[官方正文](https://arxiv.org/html/2610.39301v1) · 已读：Section 4.2.3: OSAD student adapters and teacher refresh between rounds

建议：**other_direction**。OSAD 明确多轮刷新 teacher/student 权重；共同变化的是两个模型状态，没有外部 Harness 工件的协同演化。

> At each round boundary, OSAD merges the learned adapters into the student’s base weights to obtain θ r \theta_{r} , which initializes the next teacher and student:

定位：抽取段落 63；只规范化空白后逐字匹配。

> Teacher parameters are fixed within each round and refreshed between rounds, while reference conditioning remains exclusive to the teacher. This alternation updates both the parser and its supervision

定位：抽取段落 64；只规范化空白后逐字匹配。

> We run six rounds of OSAD. App. C provides the training settings and pseudocode (Alg. 1 ); Subsec. 5.7 evaluates the successive checkpoints.

定位：抽取段落 64；只规范化空白后逐字匹配。

多轮 teacher/student 是模型权重 RSI，不能只因 co-evolve 一词改标 harness/coevolution。

## 2610.39358 · Before the Next Rollout: Diagnosing Skill Utility Shifts from Policy Updates

[官方正文](https://arxiv.org/html/2610.39358v1) · 已读：Sections 3.4, 4 and Appendix B.4: skill edits alongside policy training and paired acceptance

建议：**harness**。更新后的 policy 与文本技能库分别演化；失败轨迹和 readout 指导编辑，配对验证保留新技能库供后续窗口使用。

> A shared LLM editor receives their skill texts and the complete failed trajectories in ℬ t \mathcal{B}_{t} that invoke them. Under a common mutation budget, it may add, modify, delete, or merge skills

定位：抽取段落 52；只规范化空白后逐字匹配。

> The proposal is accepted if it satisfies a predefined acceptance rule; otherwise, the current library is retained. The full editor prompt and revision settings are provided in Appendix B.4 .

定位：抽取段落 52；只规范化空白后逐字匹配。

> Closed-loop experiments allow revisions only at window boundaries. Readouts reuse the window’s initial pre-update training batch, preserving recorded contexts and response prefixes. Independent utilit

定位：抽取段落 111；只规范化空白后逐字匹配。

这是同时迭代 policy 和 skill bank 的协同情形；独立诊断实验固定技能库，闭环实验才修改技能。

## 2610.39417 · Well-Specified and Well-Tested? Assessing SWE-bench-Style Datasets with a Self-Evolving Agent

[官方正文](https://arxiv.org/html/2610.39417v1) · 已读：Sections 3.1–3.2: three memory-entry operations and unchanged retrieval pipeline

建议：**other_direction**。反馈插入、修改或删除可检索经验条目；复用阶段仍用同一 RAG 流程，没有修改检索或记忆管理程序。

> updates the experience bank through three predefined operations: insertion, modification, and deletion. The self-evolution process is implemented via an LLM-driven maintenance procedure, which generat

定位：抽取段落 50；只规范化空白后逐字匹配。

> refreshed experience bank is used for the next round of rollout and reflection, forming a closed loop that continuously improves subsequent predictions. The detailed prompt template for the experience

定位：抽取段落 53；只规范化空白后逐字匹配。

> It shares the same RAG workflow with the rollout stage in the experience accumulation phase (Section 3.1.1 ). Specifically, it first generates three summarized descriptions for a SWE instance and uses

定位：抽取段落 55；只规范化空白后逐字匹配。

经验中包含可操作建议，但存储单元仍为源实例关联的检索条目；固定 RAG 不能仅因经验内容变化改标 Harness。

## 2610.39508 · Compile Away Uncertainty: Self-Evolving Agent Skills via Programmatic Compilation

[官方正文](https://arxiv.org/html/2610.39508v1) · 已读：Sections III-A–III-D: failure feedback, skill skeleton, validated programs and asset reuse

建议：**harness**。执行轨迹和检查错误驱动技能骨架与程序修订；验证过的程序资产及技能被保留给后续任务复用。

> the validated skill knowledge is retained for subsequent reuse. Otherwise, the Skill Optimizer analyzes the failed execution trace to identify problematic operations, guidance, or dependencies and gen

定位：抽取段落 24；只规范化空白后逐字匹配。

> When validation fails, the observed errors and check discrepancies are returned to the Programmer to guide program repair. This synthesis, validation, and repair process continues until a qualified im

定位：抽取段落 39；只规范化空白后逐字匹配。

> Newly synthesized and validated programs are persisted as reusable assets for subsequent skills.

定位：抽取段落 23；只规范化空白后逐字匹配。

## 2610.39714 · MoLRSI: A Recursive Self-Improving AI agent for Molecular Discovery

[官方正文](https://arxiv.org/html/2610.39714v1) · 已读：Sections 4.1, 4.2.2, 4.3.2 and S1: external workflows, memories, initial skill repair and fixed-library controls

建议：**borderline**。主要循环更新外部科学工作流和三类经验记忆；同时描述资源技能的执行修复与保留，是否构成被实证的 Harness 子循环需 owner 裁决。

> Skills that pass execution validation are tagged as validated and retained for reuse. Skills that still fail after repair are removed, so that only validated skills are available for subsequent tasks.

定位：抽取段落 48；只规范化空白后逐字匹配。

> After each execution attempt, MolRSI stores the workflow, its execution status and any available development score in solution memory. It adds the modification and its outcome to refinement memory and

定位：抽取段落 61；只规范化空白后逐字匹配。

> Both conditions used identical resource libraries, candidate data, search controllers, evaluation objectives and procedures, and the per-task budget specified above. Memory was updated during search i

定位：抽取段落 97；只规范化空白后逐字匹配。

> could expand an existing resource library by retrieving additional resources and identifying skills not already present. Existing skills are retained. New skills undergo the same construction checks a

定位：抽取段落 127；只规范化空白后逐字匹配。

主 RSI 对照共享相同资源库与搜索控制器，隔离的是历史经验；需要更具体的持久 Harness 文件变更证据才能把主增益归为 Harness。技能初次执行修复的正证据已保留，不作机械排除。

## 2610.39795 · The Role of Self-Concept In Language Models

[官方正文](https://arxiv.org/html/2610.39795v1) · 已读：Successor scenarios and limitations: stated forced-choice preferences, no enacted RSI loop

建议：**other_direction**。测试自我概念对假设性继任模型选择的影响；是广义 RSI 安全相关研究，正文明确无真实工具行动或自改权重。

> This section tests that assumption, motivated by § 4 : models with a plural self-conception acknowledge other selves, accept substitution by them, and prefer replicating themselves. A successor shares

定位：抽取段落 52；只规范化空白后逐字匹配。

> All evaluations are forced-choice scenarios scored by an LLM judge, showing stated preference under stipulated conditions rather than real-world capability or attempted action. The five self-conceptio

定位：抽取段落 66；只规范化空白后逐字匹配。

> No model acted in a real environment or had access to tools, to its own weights, or to any infrastructure, and we do not test whether the measured preferences carry over into behavior outside these sc

定位：抽取段落 77；只规范化空白后逐字匹配。

所有评估都是假设性单轮强制选择；摘要的 successor 表述不代表模型真正构建或控制继任系统。

## 2610.39884 · KARMA: Training-Free Knowledge-Atomic Harness Evolution for Industrial Advertising Agents

[官方正文](https://arxiv.org/html/2610.39884v1) · 已读：Sections 3–4.6, A/B: typed prompt/rule modules, atomic edits, validation and version reuse

建议：**harness**。成功/失败轨迹触发原子规则与角色、输出协议编辑，规则直接构成系统提示及响应 schema，闸门保留到后续批次。

> Accepted knowledge serves the next training batch.

定位：抽取段落 42；只规范化空白后逐字匹配。

> Role, domain, and output protocol are typed text modules. Experience and constraints are ordered rule lists,

定位：抽取段落 47；只规范化空白后逐字匹配。

> Action descriptions parameterize 𝒴 K \mathcal{Y}_{K} and the local finish tool in Equation 5 .

定位：抽取段落 48；只规范化空白后逐字匹配。

> favors reusable evidence requirements and decision priorities, excludes case-specific identifiers from rule text, and calls for checking knowledge validity after changes. Tool feedback reports invalid

定位：抽取段落 124；只规范化空白后逐字匹配。

可修改角色/协议/动作定义与提示规则，所以不止积累记忆；但可执行代码固定，不能宣称工具代码或控制流演化。
