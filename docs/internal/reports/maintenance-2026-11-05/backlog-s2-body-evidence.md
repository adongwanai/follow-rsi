# S2 33 项个人关键正文证据

全部 33 项先完成个人关键章节阅读与判断，再对照独立冻结意见。引句从已读段落取精确短摘，完整上下文见 JSON；段落索引为 article 内 h2,h3,h4,p 的零基索引。只声称选读，未复现实验、审核所有数字或批准发布。

主审最终 28 include / 4 exclude / 1 borderline；与独立冻结稿 32 项建议一致，ModelBlaster 分歧保留。

## arxiv:2610.40663 — Learning from Expert-Corrected Misdiagnoses: A Self-Evolving Consultation Agent for Traditional Chinese Medicine after Failed Treatment

摘要初判 `include` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

正文明确唯一可改对象为空白起始的临床技能文档；失败咨询与专家分析驱动增删改，双集合接受门保留编辑并供后续轮次和封存测试病例使用。

来源：[官方正文](https://arxiv.org/html/2610.40663)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2610.40663.html.html`；SHA-256 `a47002b1230118c65bfed42c428bebdc8c2a8dac1bfbb71612962715fabfdcc8`。

- Editable surface.，`#S4.SS0.SSS0.Px1.p1.1`："The agent’s system prompt contains a fixed task description and a skill document , a free-text section of clinical guidance."

- Evolution loop.，`#S4.SS0.SSS0.Px2.p1.1`："We follow the Self-Harness algorithm [ 19 ] and implement it on the SkillOpt environment interface [ 18 ] ."

- Setup.，`#S5.SS0.SSS0.Px1.p1.1`："The consulting agent, the diagnosing and proposing agent, and the judge all use DeepSeek-Flash ( deepseek-flash ) with thinking disabled for the judge; the judge is called directly and kept fixed across all runs."

- The gate selects edits that transfer.，`#S5.SS0.SSS0.Px3.p1.1`："Over 9 rounds, two edits were accepted, at rounds 1 and 6."

范围与证据限制：

- held-out 的153例参与接受门，封存test为141例，两者不能混同。
- 仅阅读方法、设置及继承结果段；结果未独立复算。

## arxiv:2610.40758 — More Rules, Longer Lists? Benchmarking Self-Evolving Agents on a Hidden-Rule Curriculum

摘要初判 `borderline` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

专项评测持久策略/技能自演化如何跨课程继承：GEPA明确演化policy提示，EvoSkill维护技能库，practice反馈更新状态后供test及后续level使用。负结果显示状态多记忆实例，不取消对程序优化机制的评测属性。

来源：[官方正文](https://arxiv.org/html/2610.40758)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2610.40758.html.html`；SHA-256 `c594906e259e03b8752e7f0d65af68ebd777bdd2e2598b03f65c9e6f3b02602d`。

- 6.2. Experimental Settings，`#S6.SS2.p1.1`："All methods, the frozen agent, and the references use GPT-6-Luna with high reasoning effort."

- 7.2.1. Why do the methods not learn?，`#S7.SS2.SSS1.p5.1`："To test whether the methods learn a reusable inference policy, we give the convention in the update step at level 1 only and remove it from level 2 on (Table 8 )."

- A.3. Implementation details，`#A1.SS3.p1.1`："All methods use the official prompts and algorithms with task-specific placeholders filled in; the frozen agent uses the same solver prompt with an empty state."

- A.3. Implementation details，`#A1.SS3.SSS0.Px1.p1.1`："GEPA folds every detail of the practice task into its evolved prompt, including the practice aggregation (largest total), which then overrides the test task (sum)."

范围与证据限制：

- 多数状态只记录实例而非泛化规则，不能将benchmark本身称已解决Harness学习。
- GEPA附加中立反思说明；EvoSkill超context时退回旧state，均应保留实现边界。

## arxiv:2610.41157 — Lineage Is Memory: Parent Inheritance and Feedback Disclosure in Short-Budget LLM-Guided Optimization

摘要初判 `borderline` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

直接比较自然语言系统提示/函数候选的父代继承和反馈披露；当前best按严格改进保留到下轮，并用独立holdout评估。纳入依据包括持久提示优化的专项分析。

来源：[官方正文](https://arxiv.org/html/2610.41157)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2610.41157.html.html`；SHA-256 `9a7a6035acce39fa4cd3b23777f654abd244ed166759707bedce94d36be436d5`。

- 3.1 The P/F/A Optimization Loop，`#S3.SS1.p1.1`："We study iterative optimization over a candidate space 𝒞 \mathcal{C} consisting of natural language system prompts or Python functions, implemented within the AdalFlow optimization framework ( Yin and Wang, 2025 ) ."

- 3.1 The P/F/A Optimization Loop，`#S3.I1.i3.I1.i2.p1.1`："Parent selection ( P P ): Set p t = c 0 p_{t}=c_{0} if P = seed P=\text{seed} , or p t = c t − 1 ∗ p_{t}=c^{*}_{t-1} if P = parent P=\text{parent} ."

- 3.1 The P/F/A Optimization Loop，`#S3.I1.i3.I1.i5.p1.1`："Evaluation ( A A ): Evaluate c t c_{t} on 𝒟 search \mathcal{D}_{\text{search}} , consuming 1 evaluation from cap B B , and cache E ⁡ ( c t , 𝒟 search ) E(c_{t},\mathcal{D}_{\text{search}}) ."

- 3.1 The P/F/A Optimization Loop，`#S3.SS1.p4.1`："Factor 1: Lineage ( P P )."

范围与证据限制：

- 任务同时含外部函数合成，不能将所有实验都称Agent自身Harness演化。
- 构造任务刻意遗漏规则偏向累积；GEPA比较同时改变多个系统因素，非纯反馈聚类因果结论。

## arxiv:2611.00180 — Learning to Live: A Step Toward Lifelong Embodied Intelligence

摘要初判 `borderline` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

EDM蒸馏阶段依据执行反馈修订工具与技能指令，Mount把验证后能力注册到执行环境，冻结能力用于后续问题及held-out episodes；不仅新增记忆事实。

来源：[官方正文](https://arxiv.org/html/2611.00180)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.00180.html.html`；SHA-256 `c3bb5da467acba8703e33af7fd999ec5489f95a5be59229c9432363eb7172665`。

- Identifying Capability Gaps from Task Difficulty，`#S5.SS1.p2.2`："𝒯 \mathcal{T} denotes callable tools, 𝒮 \mathcal{S} denotes skills that guide their use, and ℬ \mathcal{B} denotes builders that generate or update memory fields and indexes; a a and τ \tau are the task output and execution trace."

- Explore, Distill, and Mount，`#S5.SS2.p2.1`："During Distill , effective parts of the exploratory solution are converted into capabilities usable by the execution agent."

- Explore, Distill, and Mount，`#S5.SS2.p3.2`："During Mount , validated tools, skills, and builders are integrated into the execution environment."

- Benchmark Evaluation of Capability Expansion，`#S5.SS3.SSS0.Px2.p3.1`："On held-out episodes 81–90, which were excluded from exploration and distillation, we evaluate reuse of the frozen capabilities."

范围与证据限制：

- EDM及robot-memory结果来自既有ReSight实验，不能描述为LIFE新实验。
- 报告执行开销不含前期探索和能力构建费用。

## arxiv:2611.00463 — Exo: An Architecture for Self-Improving Systems at Runtime

摘要初判 `include` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

执行器策略源代码可读写，包括工具、上下文和进一步自改程序；运行记录/成本支持修订，独立guardian激活后继策略且保留历史，重复目标新账号实验继承自修改。

来源：[官方正文](https://arxiv.org/html/2611.00463)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.00463.html.html`；SHA-256 `b34119e49cc111794c9b4dba3884ad8d1fee779240306d12fb7f1b8604d518a0`。

- 3.1 Collapsing the Optimization Loop，`#S3.SS1.p3.1`："Second, the harness is operationally homoiconic : its policy is code, and that code is represented as files the agent can observe and manipulate with its code-editing tools."

- 3.1 Collapsing the Optimization Loop，`#S3.SS1.p4.1`："Because the policy governing when and how to revise the harness is itself editable, the agent can revise both its task behavior and its strategy for further improvement."

- 4.1 Partitioning Policy and Mechanism，`#S4.SS1.p4.1`："All other harness functionality is expressed in the policy layer, which we call the executor ."

- 4.2 Enabling Runtime Self-Editing，`#S4.SS2.p2.1`："The agent can thus inspect and edit its own implementation during task execution, then request activation of the revised policy ( Fig. 3 (b))."

- 5.3 Transfer of the Specialized Harness，`#S5.SS3.p1.1`："The tools and policies learned during standalone runs remain useful when the agent repeats the objectives on fresh accounts."

范围与证据限制：

- 默认guardian只检查build成功，不能等同于性能或安全改进门。
- 历史保全保证不推出持续进步；新账号重复目标复用不等于任意新任务泛化。

## arxiv:2611.00643 — Selecting LLM-Generated Hypotheses Raises Truth Beyond What an LLM Panel Expects: A Pre-registered Study on NAS-Bench-201 and HPOBench

摘要初判 `include` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

评测对象包含角色、检索、自质疑、选择规则和策略提示组成的Harness；Opus读评分历史提3轮候选并以严格胜出替换incumbent，论文直接分析judge目标与真值精度失配。

来源：[官方正文](https://arxiv.org/html/2611.00643)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.00643.html.html`；SHA-256 `f3d34df1641800a1a4e22fa20aa71344bc5b534dc4d6258dcfad8cc0fdd014b5`。

- 3 Testbed，`#S3.SS0.SSS0.Px5.p1.1`："A harness sets retrieval (none, in-domain, cross-domain), roles (single, or gap finder, innovator and critic), self-challenge, pool size and selection rule, and a free-text strategy of at most 150 words."

- Appendix E Truth definition and harness procedure，`#A5.SS0.SSS0.Px2.p1.1`："The optimizer is a single Opus prompt per round."

- 4.4 A precision check shows the cost of optimizing for judged novelty，`#S4.SS4.p1.1`："We evolved one harness for the judge’s score, in one optimizer run, so this section is a case study of that harness."

- 4.4 A precision check shows the cost of optimizing for judged novelty，`#S4.SS4.SSS0.Px1.p1.1`："The judge prompt asks whether experts would find the hypotheses surprising, and the evolved strategy bans the two claim types most often true, so part of the precision loss follows from base rates."

范围与证据限制：

- judge优化只有一个优化运行，作者明确不能推广为所有judge优化都会如此。
- 部分意外度指标为事后定义，表述需保留预注册与事后分析边界。

## arxiv:2611.00752 — Reading Between the Chapters: A Graph-Free RAG Rebuilt With AI and Human Feedback

摘要初判 `borderline` → 正文建议 `exclude`；独立建议 `exclude`；正式决定 `defer`。

正文说明每次修改由作者依据AI判分和人工分析提出，AI编码助手实施，作者复核后保留；这是有真实程序迭代的人工研发，未展示系统自主提出并演化自身Harness的闭环。

来源：[官方正文](https://arxiv.org/html/2611.00752)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.00752.html.html`；SHA-256 `21859bc407de8a9f1571faf89bda5bbf702f2c6f311d91682fd2a6eb6c92aa50`。

- 5 Redesign from AI and Human Feedback，`#S5.p1.1`："We improved LadderRAG on a single development book, Black Beauty , which both authors know well enough to judge an answer without rereading."

- 5 Redesign from AI and Human Feedback，`#S5.I1.i2.p1.1`："Human feedback."

- 5 Redesign from AI and Human Feedback，`#S5.p1.2`："We proposed each change from these signals, implemented it with the help of an AI coding assistant, and kept it only after reviewing its results."

- v4b: anchors and the ladder.，`#S5.SS0.SSS0.Px5.p1.1`："v4b restores the cards and summaries selected by v2’s plan, and adds two rules: a later part that refers back (“that horse”) keeps the same character, and a line belongs only to the speaker the passage names."

范围与证据限制：

- 不能说没有代码改动或没有反馈；排除依据是修改主体和自动演化机制不足。
- v4b只应用于初版失败子集且保留初版其余输出，未在全样本验证统一替换。

## arxiv:2611.00960 — Self-Refining Prompt Induction for Streaming Text-to-SQL

摘要初判 `include` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

Refiner依据失败SQL和judge解释生成完整替换提示；候选通过目标及抽样回归检查后继承到下轮，最终提示冻结供跨schema和Generator复用。

来源：[官方正文](https://arxiv.org/html/2611.00960)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.00960.html.html`；SHA-256 `e8642f57d6b27ccd3830059b17bdfbf54053da24f5b375021a5be0041f6443ba`。

- Rewrite from a failure.，`#S3.SS0.SSS0.Px2.p1.1`："For a failing example, the Refiner receives the current prompt, fixed user template, question, DDL, reference and generated SQL, judge feedback, and summaries of failed attempts on that example."

- Check earlier successes.，`#S3.SS0.SSS0.Px3.p1.1`："A candidate must first pass the target example."

- Repeat and retain a checkpoint.，`#S3.SS0.SSS0.Px4.p1.1`："Each round scores the induction sample, attempts repairs on up to 40 failing examples, and scores the resulting prompt again."

- Limitations，`#Sx1.p2.1`："Workload coverage and intended generalisation."

范围与证据限制：

- 接受检查允许至多一个抽查样本失败，不是零回归保证。
- 只有一次induction run；模式模板重叠、非生产实证，完整最终提示/逐例日志未提供。

## arxiv:2611.01113 — CogRSI: Evolving and Auditing Cognitive Reasoning Strategies

摘要初判 `include` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

保留至多五条When条件规则作为reader原则槽，失败问题触发增改删及候选比较，后续库迁移至独立BigToM-U；同时专项审计演化规则语义有效性。

来源：[官方正文](https://arxiv.org/html/2611.01113)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.01113.html.html`；SHA-256 `c3821ad8b3f32e27dd892530810f4232fc52a7997fe9edef6c07d929958bb340`。

- Strategies.，`#S4.SS2.SSS0.Px1.p1.1`："The loop keeps a library L L of up to five rules."

- Calibrated registration.，`#S4.SS2.SSS0.Px2.p1.1`："The same principle varies by 2.7 points across trial cohorts of 80 questions."

- Translation and counterexamples.，`#S4.SS3.SSS0.Px2.p1.1`："Two models translate each rule into code: Llama-3.3-70B and Qwen3.5-122B, neither of which wrote the rules."

- Beyond the expert on independent pairs.，`#S5.SS2.SSS0.Px1.p1.1`："On BigToM-U, every learned principle scores above the expert one (Table 1 )."

- Most evolved rules fail somewhere.，`#S5.SS4.SSS0.Px1.p1.1`："The principle loops proposed 573 rules. 286 are invalid: for each, there is a story it claims to cover where following it gives the wrong answer. 44 are valid, 84 are ambiguous because the two translations disagree, and 159 almost never apply."

范围与证据限制：

- 准确率或注册门不能证明规则语义正确；可判定规则中86.7%无效。
- BigToM-U迁移与test Main结果需分别陈述，gated对accuracy-only并无显著收益。

## arxiv:2611.01351 — MAPLE: A Multimodal Mobile Agent with Playbook-Learned Experience

摘要初判 `borderline` → 正文建议 `exclude`；独立建议 `exclude`；正式决定 `defer`。

正文将Playbook条目明确为第三人称UI action-effect陈述事实，按固定流程插入、去重和更新计数；跨episode保留的是界面知识，不是被反馈改写的执行程序或策略文件。

来源：[官方正文](https://arxiv.org/html/2611.01351)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.01351.html.html`；SHA-256 `71e04f4e456fe740fe0ef95b8605895071f3b929c35e6a1220de2bcac3f5bb4f`。

- 3.4 Self-Supervised Hindsight Distillation & Playbook Consolidation，`#S3.SS4.p1.1`："Following action execution a t a_{t} and environment stabilization to observation o t + 1 o_{t+1} , MAPLE enters the hindsight reflection phase."

- Playbook Database Formalization.，`#S3.SS4.SSS0.Px1.p1.1`："We define the Playbook 𝒟 = { d 1 , d 2 , … , d N } \mathcal{D}=\{d_{1},d_{2},\dots,d_{N}\} as a vector-indexed knowledge repository of verified UI mechanics, where each entry is a 5-tuple d i = ( k i , A i , f i , 𝐯 i , c i ) d_{i}=(k_{i},A_{i},f_{i},\mathbf{v}_{i},c_{i}) comprising a generalized task intent template"

- Dual-Output Hindsight Distillation.，`#S3.I1.i2.p1.1`："Universal Declarative Fact ( f new f_{\text{new}} ): An abstracted, third-person action-effect rule defining an invariant UI property (e.g., “The vertical ellipsis icon expands the app configuration menu” )."

- Semantic Consolidation and Deduplication.，`#S3.SS4.SSS0.Px3.p1.2`："where Resolve ​ ( ⋅ ) \text{Resolve}(\cdot) triggers an auxiliary semantic verification check."

范围与证据限制：

- 确有环境反馈及跨任务记忆复用，不能说没有学习或没有持久化。
- “prompt evolution/playbook”命名不足以替代实际改进对象的核查。

## arxiv:2611.01386 — Learning by Doing: Autonomously Compiling and Curating Agent Skills from Verified Traces

摘要初判 `include` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

Reflector/Curator依据验证执行trace、失败对照和旧提案结果增改合并程序性Skill，准入后创建不可变版本，后续run检索并执行该程序。

来源：[官方正文](https://arxiv.org/html/2611.01386)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.01386.html.html`；SHA-256 `1c1654758a361bdb5bfd796ae6989bb7145738fda42f721e3d55352e0dd32c6e`。

- 5.2 Skill representation，`#S5.I1.i2.p1.1`："Procedure fields give the ordered steps, the decisions, the expected observations, the outputs, the completion criteria, the stop conditions, and the failure modes with their recovery."

- 5.3 Compilation，`#S5.SS3.p1.1`："The compiler turns verified Traces into proposed changes to the Skills of one task family."

- 5.3 Compilation，`#S5.SS3.p5.1`："Reflector."

- 5.4 Admission, maturity, and trust，`#S5.SS4.p2.1`："Approval modes."

- 5.4 Admission, maturity, and trust，`#S5.SS4.p4.1`："Group admission and versions."

范围与证据限制：

- Zep服务本身不执行应用代码或evaluation，必须区分声明的门与外部应用提交的验证。
- 程序可先以单来源provisional状态准入；稳定性/因果效用不由检索权重单独证明。

## arxiv:2611.01695 — SPAR: Experience-Driven Strategy Evolution in Multi-Session B2B Sales

摘要初判 `include` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

外环明确区别于商户episodic memory；以交互结果因果归因为门，对跨商户共享策略playbook执行Update/Condition/Add/Merge/Deprecate等修改，后续会话选择非废弃策略。

来源：[官方正文](https://arxiv.org/html/2611.01695)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.01695.html.html`；SHA-256 `a3d840b29b58de2e3bf8d34adf76c3eca84e074cec4b6b72fe6dafc43de59458`。

- 3.2 Framework Overview，`#S3.SS2.p1.1`："SPAR organizes learning as a double-loop architecture , illustrated in Figure 2 ."

- 3.4 Within-Merchant Adaptation，`#S3.SS4.p2.1`："At the start of each session, the agent concatenates the merchant profile p i p_{i} , interaction history M i M_{i} , and the non-deprecated hypothesis set 𝒫 + \mathcal{P}^{+} as selection context."

- Causal Attribution.，`#S3.SS5.SSS0.Px1.p1.1`："The LLM examines the dialogue, merchant profile, outcome, and strategy used, then assigns an attribution label a ⁡ ( e ) ∈ { s , x , u } a(e)\in\{s,x,u\} ."

- Hypothesis Evolution.，`#S3.SS5.SSS0.Px2.p1.2`："where e e is the newly constructed evidence."

范围与证据限制：

- 归因由LLM完成，归因门并不等同于已证明策略因果效应。
- 不可把inner-loop商户记忆单独称为Harness演化依据。

## arxiv:2611.01736 — RSI-Env: An Open-Ended Environment for Recursive Self-Improvement of Agents

摘要初判 `borderline` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

环境允许目标模型与可执行Harness修订，保留运行记录及后继版本；Knowledge Self案例明确H0/M0→H1/M0，再由该后继系统训练M1，形成真实Harness与目标模型共同演进。

来源：[官方正文](https://arxiv.org/html/2611.01736)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.01736.html.html`；SHA-256 `eedec90e9661feca0b996f1960684b86411aa10a1532a9115e87b2763ac3dfde`。

- 3.1 Problem Setup，`#S3.SS1.p1.1`："We formulate RSI as the iterative improvement of an executable agent system, 𝒮 t = ( θ t , H t , 𝒫 t , ℛ ) \mathcal{S}_{t}=(\theta_{t},H_{t},\mathcal{P}_{t};\mathcal{R}) ."

- 3.1 Problem Setup，`#S3.SS1.p2.2`："where 𝒯 \mathcal{T} denotes the transition distribution over successor systems induced by executing the update, allowing for randomness in training or tool execution."

- 3.1 Problem Setup，`#S3.SS1.p3.1`："In the Self configuration, the evolving target model–harness pair also serves as the Improver, so each registered successor generates the next update."

- 4.5 Case Study: Sustained Recursive Improvement，`#S4.SS5.p1.1`："Knowledge Self achieves successive gains as updated systems continue the improvement process (Figure 4 )."

范围与证据限制：

- Host只用validity/executability注册候选，独立能力分数不是中间接受门。
- 需分别报告实验设定的反馈开放程度，不能把所有任务都称有benchmark反馈。

## arxiv:2611.01840 — Self-Evolving Agentic Workflows via Semantic Decomposition of Complex Tasks

摘要初判 `include` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

代码工作流在每次交互固定，执行记录和结果驱动编码agent修改分解、分支与求解过程；被保留候选成为下一轮W并继续收集反馈，符合程序工作流演化。

来源：[官方正文](https://arxiv.org/html/2611.01840)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.01840.html.html`；SHA-256 `28bf1478823d05132cffb3e06a0634d12b51041895be16cb72caccb223c11ef7`。

- 3 Self-Evolving Agentic Workflows，`#S3.p1.1`："Our method separates the workflow that makes decisions from the agent that improves it."

- 3.2 Workflow Evolution，`#S3.SS2.p1.1`："At iteration k k , the agent executes W k W_{k} and collects execution traces and task outcomes D k D_{k} ."

- 3.2 Workflow Evolution，`#S3.SS2.p2.1`："The candidate is evaluated using replay, held-out records, or bounded deployment to assess the targeted behavior and check for regressions (Appendix B )."

- B.1 Revision Protocol，`#A2.SS1.p1.1`："The recurring protocol reconstructed from repository instructions uses a shared history-inspector prompt followed by a strategy prompt and one family-specific routing prompt."

范围与证据限制：

- 历史commit说明和测试修改不能证明每条描述的validation实际执行。
- 未部署的分支及人工审计的选定案例不能泛化为全部revision有效。

## arxiv:2611.01870 — Automated Stateful Specialization for Adaptive Agent Systems

摘要初判 `borderline` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

Architect读取既有架构及performance history，演化专家identity/directive提示和多Agent图；创建/交叉后按性能多样性保留池，架构可留给后续任务。纳入来自这些外部工件，不只specialist记忆。

来源：[官方正文](https://arxiv.org/html/2611.01870)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.01870.html.html`；SHA-256 `195c0e583c908664180ade3535355d33698c37ce26037dc41accc7bd52b8c73a`。

- 2 Preliminaries，`#S2.SS0.SSS0.Px1.p3.1`："A specialist O i S ∈ 𝕆 spec O_{\text{i}}^{S}\in\mathbb{O}_{\text{spec}} extends a base operator O i ∈ 𝕆 base O_{\text{i}}\in\mathbb{O}_{\text{base}} with a learned identity and a persistent memory while inheriting its foundational reasoning structure (e.g., "think step-by-step")."

- 2 Preliminaries，`#S2.SS0.SSS0.Px2.p2.1`："where ℋ t − m : t − 1 \mathcal{H}_{t-m:t-1} is a sliding window of the past m m experiences including the executed architectures and performance outcomes; 𝕆 t − 1 \mathbb{O}_{t-1} is the previous operator pool; and 𝒢 t − 1 \mathcal{G}_{t-1} is the current architecture."

- 3.1 Specialist Discovery，`#S3.SS1.p1.1`："Depicted as stages I and II in Figure 3 , during the specialist discovery phase, the Architect iteratively evolves a pool of specialists using its full action space (detailed in Appendix G.1 )."

- 3.1 Specialist Discovery，`#S3.SS1.SSS0.Px1.p1.1`："Let 𝕆 spec ( 1 ) \mathbb{O}_{\text{spec}}^{(1)} be the pool of specialist operators during the specialist discovery phase and 𝕆 spec ( 2 ) \mathbb{O}_{\text{spec}}^{(2)} be the pool of specialist operators during the cultivation phase."

- 3.1 Specialist Discovery，`#S3.SS1.SSS0.Px3.p1.1`："At the end of the specialist discovery phase, we select the top- k k specialists for cultivation by solving a multi-objective optimization problem that balances performance and diversity:"

范围与证据限制：

- 训练meta-controller另列模型侧；cultivation与评测期operator pool固定，不应声称每个阶段持续修改专家prompt。
- 复杂系统的memory与architecture效应未在此复算。

## arxiv:2611.02516 — Cumulative and Audited Guardrail Tool Evolution for LLM Agent Safety

摘要初判 `include` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

生成Python guardrail工具，复用时融合旧逻辑，依据独立审计的漏洞报告最多三轮修复，只有通过者进入持久工具库供后续防御。

来源：[官方正文](https://arxiv.org/html/2611.02516)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.02516.html.html`；SHA-256 `2b4ca6f56855010af6548399f088b7c7e3532585fc80971a8ddc0e3cbde9ae27`。

- 3.5 Generation: Risk Identification and Tool Creation，`#S3.SS5.p3.1`："Tool Generation."

- 3.6 Reuse: Tool Retrieval and Evolutionary Fusion，`#S3.SS6.p4.1`："Tool Fusion."

- 3.6 Reuse: Tool Retrieval and Evolutionary Fusion，`#S3.SS6.p4.2`："This fusion process is the mechanism through which tools self-evolve: each reuse cycle deepens and extends existing tools rather than leaving them static."

- 3.8 Refinement: Iterative Repair and Adaptive Replanning，`#S3.SS8.p2.1`："Tool Repair."

- 3.8 Refinement: Iterative Repair and Adaptive Replanning，`#S3.SS8.p2.2`："This audit-repair cycle executes at most three rounds; tools that still fail are discarded."

范围与证据限制：

- 协议同时包含Docker执行和LLM模拟sandbox，不能把所有评测都称真实容器执行。
- 独立审计是分离角色机制，非外部独立复现实验或绝对安全保证。

## arxiv:2611.02797 — SelfImprove-Bench: Evaluating Generalization in Self-Improving Agents

摘要初判 `borderline` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

固定backbone下，benchmark执行候选Harness并返回当前任务分数，由各方法选择保留版本再进入下一任务；AHE与HyperAgents明确改prompt/tools/代码及improver，专项测G0–G4泛化和改动过程。

来源：[官方正文](https://arxiv.org/html/2611.02797)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.02797.html.html`；SHA-256 `ffbace212d6bc0e82f1e409290f82942122fb5db1ea5aa418dec0d288f51ab67`。

- 3.1 Evolution Protocol，`#S3.SS1.SSS0.Px3.p1.1`："For each RSI method, the initial task agent is A 0 = ( B , H 0 ) A_{0}=(B,H_{0}) , comprising a common backbone model B B and a method-specific initial harness H 0 H_{0} ."

- 3.1 Evolution Protocol，`#S3.SS1.SSS0.Px4.p1.1`："At step t t , the current agent A t − 1 = ( B , H t − 1 ) A_{t-1}=(B,H_{t-1}) executes τ t ∈ 𝒮 in \tau_{t}\in\mathcal{S}_{\mathrm{in}} through the game’s action interface, producing an interaction trace and task score."

- 3.4 Semantic Process Analysis，`#S3.SS4.SSS0.Px4.p1.1`："These identify whether the change affects contextual artifacts, the execution harness, or the refinement mechanism itself."

- 4.1 Experimental Setup，`#S4.SS1.SSS0.Px1.p1.1`："We evaluate ACE, AHE, and HyperAgents as representative methods of experience-level, harness-level, and meta-level RSI, respectively (Section 2 )."

范围与证据限制：

- 任务重放不触发refinement；候选验证只用held-in，区分其选择规则与最后held-out评估。
- 保留opinion计数不等同代码修改有效性或自动improver改进成功。

## arxiv:2611.02839 — CARE: Grounded Recursive Self-Improvement for Production Customer-Service Agents

摘要初判 `borderline` → 正文建议 `exclude`；独立建议 `exclude`；正式决定 `defer`。

正文明确外部Harness变更确实存在，但由业务owner/工程师按各自日程修订，且3.3写明context change不是CARE循环一步；其自动递归更新对象是模型，未证实Agent生成并保留Harness修订。

来源：[官方正文](https://arxiv.org/html/2611.02839)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.02839.html.html`；SHA-256 `ef0dd1664790bb2583e9c5cf2b9116c0f55e1789f0d20ddf5040727304706971`。

- 3.2 Replacement and improvement criteria，`#Thmdefinition2.p1.2`："Given the current model parameters θ k \theta_{k} , an iteration of CARE generates experience 𝒯 k ∼ π θ k \mathcal{T}_{k}\sim\pi_{\theta_{k}} and produces a candidate model through"

- External intervention.，`#S3.SS3.SSS0.Px1.p1.1`："Definition 2 is narrower than a loop that improves without external intervention."

- Changes to the operating context.，`#S3.SS3.SSS0.Px2.p1.1`："A change of c c is not a step of the loop."

- 9.4 Limitations，`#S9.SS4.p2.1`："The confirmed-bad rate depends on screening recall and is therefore a conservative observed rate, not a calibrated population estimate."

范围与证据限制：

- 不是因模型训练为主而排除，关键是外部工件修改主体与闭环边界。
- 模型更新与人工Harness变化重叠，跨版本提升不能全部归因模型；跨SOP泛化收益尚未测量。

## arxiv:2611.03434 — Optimize the Harness, Not the Model: Fitting a Minimal Agent to a Self-Hostable LLM for Investigative Analysis

摘要初判 `borderline` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

正文明确supervisor自动propose–test–keep，评分改进加通用/精简性检查决定保留，接受的工具、guardrail、compaction和memory policy引发下一轮错误分析。

来源：[官方正文](https://arxiv.org/html/2611.03434)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.03434.html.html`；SHA-256 `b37160bb53ebe45d5b4b1b5e88f6d3442dbada8af55bef537d25652b31f7c4a9`。

- 2.1. Model, Data, and a Minimal Harness，`#S2.SS1.p1.1`："The model."

- 2.1. Model, Data, and a Minimal Harness，`#S2.SS1.p2.1`："Optimization-loop dataset."

- 2.2. The optimization loop，`#S2.SS2.p1.1`："Inspired by autoresearch ( 4 ) , a supervisor model (a frontier LLM - we chose Opus-4.8 ( 12 ) ) drives an automatic propose–test–keep loop over harness versions (Algorithm 1 )."

- 4. Conclusions，`#S4.p1.1`："This work shows that ground-up harness optimization is a practical direction for deploying agentic systems in regulated domains: a minimal harness approaches the accuracy of the strongest out-of-the-box harness with two orders of magnitude less code and capability surface."

范围与证据限制：

- 以单一LLM judge评分并人工spotcheck，未系统验证judge；单一调查领域范围不能外推。
- 240问题封存，32固定+12随机开发问题参与迭代；近似准确率差异不支持排名结论。

## arxiv:2611.03618 — Strategist: Evolving Reasoning with Agents

摘要初判 `include` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

Python blueprint指定模型调用/推理控制流程，真实样本的trace与分数驱动后续提案；每轮把去除任务特定提示的结构与测量卡写入共享库，支持后续任务组合复用。

来源：[官方正文](https://arxiv.org/html/2611.03618)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.03618.html.html`；SHA-256 `d0bb779a19a37fb16dddd1ef4ca6c19ae3c4c5a8a3c204ae62ba6c9dac19e05a`。

- Foundations.，`#S2.SS0.SSS0.Px1.p1.1`："A blueprint is a Python program that captures the structure of a reasoning strategy without the task-specific prompts."

- Step 3: Evaluate.，`#S3.SS0.SSS0.Px3.p1.1`："The system operates at two levels."

- Step 4: Accumulate.，`#S3.SS0.SSS0.Px4.p1.1`："The library stores blueprints, not strategies: it retains the reusable structure while discarding task-specific prompts."

- Overfitting across data splits.，`#S6.SS0.SSS0.Px2.p1.1`："The strategist sees training traces and validation scores at every iteration and could fit noise in them; if it did, the training curve would pull away from the hidden curve."

范围与证据限制：

- hidden split用于选胜者，只有test完全封存，不可称hidden是不参与选择的测试集。
- 库保留各候选结构与测量信息，并非所有入库blueprint都通过性能门。

## arxiv:2611.03674 — ReVi: Recursive Recap Video Generation

摘要初判 `borderline` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

外环依据跨小说production trace与修订archive改版本化editor prompt/config及meta-policy；固定kernel选中后成为下一代，meta-policy按其产生的editor在held-out小说的效用评估。

来源：[官方正文](https://arxiv.org/html/2611.03674)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.03674.html.html`；SHA-256 `9f23d3b40154a03f66c4414cb31d012d81a5a643958a105d772d6a8518df1f88`。

- 2.2 Outer Loop: Recursive Self-Improvement，`#S2.SS2.p1.2`："where θ t \theta_{t} is the editing policy and μ t \mu_{t} guides its improvement."

- Editing Policy.，`#S2.SS2.SSS0.Px1.p1.2`："where the first component governs source interpretation, the next three govern the editing agents, and ρ t \rho_{t} governs coordination and repair."

- Editing-Policy Evolution.，`#S2.SS2.SSS0.Px2.p1.1`："The Meta-Agent aggregates traces across novels and diagnoses recurring failures by inspecting source evidence, intermediate edits, and attempted repairs."

- Meta Policy.，`#S2.SS2.SSS0.Px3.p1.1`："The meta policy μ t \mu_{t} determines how to diagnose failures, propose patches, and allocate a fixed search budget."

- Meta-Policy Evaluation.，`#S2.SS2.SSS0.Px4.p1.3`："Thus Equation equation 4 evaluates a search procedure through the downstream improvement of the editors it produces, as in Hyperagents ( Zhang et al., 2026b ) ."

范围与证据限制：

- 两个演化对象均为外部程序政策，foundation model不改，不能称模型权重/Harness共演化。
- 本次只核机制与协议关键段，未复核视频评分/实验数值。

## arxiv:2611.03868 — EvoGroup: A Self-Evolving Harness for Group Agents in Shared Contexts

摘要初判 `include` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

官方correctness与置信度筛选交互轨迹，逐例和跨类诊断指导Evolve Agent修改operation实现、intervention和policy；演化后Harness冻结迁移GroupMemBench。

来源：[官方正文](https://arxiv.org/html/2611.03868)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.03868.html.html`；SHA-256 `3d634ea0d94bc05e1260b94e6e2b8fe4c0633050636088f2a730f9409ba50bce`。

- 2.2 Confidence-Guided Trajectory Selection，`#S2.SS2.p2.1`："After the interaction, an official evaluator supplies an external correctness signal y i ∈ { 0 , 1 } y_{i}\in\{0,1\} for the answer a i a_{i} ."

- 2.3 Trajectory Analysis，`#S2.SS3.p4.2`："The Analysis Agent first analyzes evidence within each bucket to identify type-specific issues, and then compares the resulting issues across buckets to derive high-level findings."

- 2.4 Harness Revision，`#S2.SS4.p2.1`："Representation."

- 3.1 Setup，`#S3.SS1.p1.1`："Benchmark & Baseline Methods."

范围与证据限制：

- representation含记忆组织，但纳入依据同时有可执行operation及policy修改，不能把记忆内容单独视为演化。
- 当前节选未给出每候选的统一接受阈值；不补写不存在的严格性能晋升门。

## arxiv:2611.04003 — WASP-Mem: Let Agent Organize Procedural Memory. Human Spend Effort on Diagnosis

摘要初判 `borderline` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

反馈驱动wiki认证程序、分页/错误恢复步骤及代码细节的修订，构成模型外可复用操作指令；更新后的store由下一轮执行读取。自然语言程序性技能也符合工件规则，不因底层执行/检索机制固定而排除。

来源：[官方正文](https://arxiv.org/html/2611.04003)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.04003.html.html`；SHA-256 `fa7ccd3203ab0b3085cc485e62296a727d47a88601799dda06fc7b7c8f59be69`。

- 3 Method，`#S3.p1.2`："The goal is to capture residual procedural knowledge not already encoded in the fixed harness."

- 3.1 WASP-Mem Consolidation Method，`#S3.SS1.p1.1`："WASP-Mem is a memory-consolidation and retrieval method for training-free continual learning that organizes execution traces and feedback into persistent, interlinked procedural wiki pages at different granularities and retrieves them to guide future execution, drawing on the idea of an LLM-maintained wiki as a"

- 3.1 WASP-Mem Consolidation Method，`#S3.I1.i1.p1.1`："Ingestion."

- 3.1 WASP-Mem Consolidation Method，`#S3.I1.i3.p1.1`："Lint."

- 4.4 Multi-Round Refinement，`#S4.SS4.p1.1`："This experiment asks whether repeated execution and consolidation continue to close the residual procedural-knowledge gap."

- Appendix E Implementation and Reproducibility，`#A5.SS0.SSS0.Px6.p1.1`："Within each round, all benchmark tasks executed against a frozen memory store and produced one rollout batch."

- Appendix F Limitations and Future Work，`#A6.SS0.SSS0.Px2.p1.1`："R1 to R4 re-executed the same benchmark tasks."

- Table 13，`figure#A4\.T13`："Free Form revises one GitLab authentication wiki page with new pagination and error handling evidence."

- Table 13，`figure#A4\.T13`："Schema Form records step names but drops the code and formatting details retained by Free Form."

范围与证据限制：

- 固定底层Harness本身不是排除理由；正文中的procedure/code细节提示可能存在操作性技能，不能仅凭memory标签否定。
- R1–R4反复执行同一批benchmark任务；单配置一次运行，不是广泛未见分布泛化证明。
- 表13提供作者报告的程序修订实例；本次未审计原始wiki文件或重放每个补丁。

个人正文初判borderline在独立审阅交叉比较和owner明确自然语言程序性指令可纳入后改为include；重新使用本人已读Table13、S4.4和Appendix E证据，不要求独立可执行源码。没有审计原始wiki补丁，Table13是作者报告的程序内容实例。

## arxiv:2611.04104 — ModelBlaster: Closing the Performance Gap through Learning-Augmented Agents Across Models, Kernels and Hardware Backends

摘要初判 `borderline` → 正文建议 `exclude`；独立建议 `borderline`；正式决定 `defer`。

实际改写的可执行程序是外部kernel；持续更新的是硬件/算子优化技巧、状态、假说及证据claims，供固定actor/critic和检索机制取用。称其为mutable policy parameters未提供Agent自身控制程序或可复用操作机制被修改的证据。

来源：[官方正文](https://arxiv.org/html/2611.04104)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.04104.html.html`；SHA-256 `342e84a838de922a6520212dca39b5071c6bc8606cba12b2bf26b37bb6465103`。

- 3.1 Kernel-Level Optimization with MAIC-RL，`#S3.SS1.p1.1`："ModelBlaster optimizes code through inference-time reinforcement learning with persistent memory."

- 3.1.3 Persistent Long-Term Memory，`#S3.SS1.SSS3.p1.1`："The Knowledge Base stores performance states, techniques, hypotheses, evidence-backed claims, outcomes, and verified implementations."

- 3.1.3 Persistent Long-Term Memory，`#S3.SS1.SSS3.p1.2`："where s i s_{i} denotes the performance state, a i a_{i} the optimization action, q i q_{i} its measured or predicted score, z i z_{i} the textual critique, and c i c_{i} the target, numerical, and failure constraints."

- 3.1.4 Actor–Critic Textual Gradient Descent，`#S3.SS1.SSS4.p1.1`："ModelBlaster instantiates MAIC-RL as Actor-Critic Textual Gradient Descent (AC-TGD), an inference-time learning architecture in which natural-language critiques serve as policy-update signals."

- 3.1.4 Actor–Critic Textual Gradient Descent，`#S3.SS1.SSS4.p3.1`："Actor CodeGen Agent and Fix Agent."

- 3.1.4 Actor–Critic Textual Gradient Descent，`#S3.SS1.SSS4.p5.1`："Critic Reflection Agent."

- 3.1.5 Uniform Harness and Cross-Task Instantiation Across Targets，`#S3.SS1.SSS5.p1.1`："To test whether the same persistent memory and text-based reward support cross-task reasoning, we instantiate the same actor and critic loop on problems whose targets differ in instruction-set architecture (ISA), source language, and execution model: CUDA C++ on NVIDIA GPUs, OpenCL C on Qualcomm GPUs, and RVV"

范围与证据限制：

- 存在真实跨任务记忆学习和反馈保留，不应描述成没有学习。
- LLM反作弊检测不保证等价性；CUDA之外的作弊模式未独立审计。

独立不同意见：ModelBlaster确有持久反馈更新，但当前正文实物主要为性能state/action/outcome/claim与UCB统计，代码演化对象是外部kernel/model；未定位到明确改写的可复用Agent程序策略entry，保留边界。

## arxiv:2611.04277 — Harness-S: Learning from Sibling Harnesses for Generalizable Agent Training

摘要初判 `borderline` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

冻结policy后运行父Harness分析失败根因，编辑prompt/skill/context/hooks等工件，以validation互补覆盖选父代并归档有效后代；多代形成的池供后续模型训练长期复用。

来源：[官方正文](https://arxiv.org/html/2611.04277)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.04277.html.html`；SHA-256 `a724d8884d58f40653c685af3d2895fc87a8e2a9366ed84d856960f13b70e47c`。

- 3.2 Directional Harness Evolution，`#S3.SS2.p1.1`："Starting with 𝒫 1 = { H 0 } \mathcal{P}_{1}=\{H_{0}\} , we execute each parent H ∈ 𝒫 g H\in\mathcal{P}_{g} on fresh training tasks to derive repair directions 𝒟 g ​ ( H ) \mathcal{D}_{g}(H) ."

- 3.2 Directional Harness Evolution，`#S3.SS2.p2.1`："Parent selection maximizes joint validation coverage."

- 3.2 Directional Harness Evolution，`#S3.SS2.p3.1`："The Sibling Harness Pool retains all valid children, including those not selected as parents:"

- 3.2 Directional Harness Evolution，`#S3.SS2.p3.2`："After T T generations, ℋ = ℋ T \mathcal{H}=\mathcal{H}_{T} is the fixed pool used for policy training."

- Appendix F Directional Harness Evolution: Prompts and Settings，`#A6.p2.1`："Local evaluation tests whether an edit repairs the targeted failures while preserving behavior on successful controls."

范围与证据限制：

- 池生成后在policy训练期间固定，刷新的是profile及分配；不是权重与Harness反复交替更新。
- 所有有效变体可入archive，不是每个变体都经过单项优于parent的门。

## arxiv:2611.04437 — WiSI: Wireless-in-the-Loop Self-Improvement

摘要初判 `include` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

LLM根据无线执行失败、动作轨迹和任务统计重写Agent自身solve(env,task)程序；共同任务批评估后保留候选为下一代父程序，演化导航/感知/通信控制结构。

来源：[官方正文](https://arxiv.org/html/2611.04437)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.04437.html.html`；SHA-256 `4b4cd426e00c96dd2db48b49716f88804dc11eeabffeec61e857f4ebcfc24f5b`。

- IV-A Wireless-in-the-Loop Self-Improvement，`#S4.SS1.p1.1`："WiSI improves agent programs through repeated execution and evaluation under a wireless environment E E ."

- IV-A Wireless-in-the-Loop Self-Improvement，`#S4.SS1.p1.2`："where ℒ ⁡ ( ⋅ ) \mathcal{L}(\cdot) is the feedback-generation process."

- IV-A Wireless-in-the-Loop Self-Improvement，`#S4.SS1.p2.2`："where U ^ E ​ ( a ) \widehat{U}_{E}(a) denotes the empirical utility measured under E E , and ties favor p g p_{g} ."

- IV-B Program Execution and Evaluation，`#S4.SS2.p1.1`："Agent execution."

- IV-B Program Execution and Evaluation，`#S4.SS2.p2.1`："Program generation and validation."

范围与证据限制：

- 任务执行程序与改进器分离；改的是具身执行Agent，而非LLM改进器本身。
- 主要无线模型为仿真，测量trace重放、真实VLM和held-out房间验证应分开陈述。

## arxiv:2611.04439 — DualEvolve: Dual-Level Self-Evolution of Mechanism and Orchestration for Recommendation

摘要初判 `include` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

外环根据实验过程trace评分提出新增/退休/合并Harness与Skill规则，并用下一轮反馈更新选择；规则指导后续研究轮次且可冻结迁移。内层改推荐模型代码属于外部研究产物。

来源：[官方正文](https://arxiv.org/html/2611.04439)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.04439.html.html`；SHA-256 `5d0aab4e23589a8dee2bb8f66022fcd8a46d1188c35938b9da8a23a0c032917a`。

- 3.1. Task and Editable Objects，`#S3.SS1.p2.1`："Let G G be the number of completed search rounds."

- 4. Methodology，`#S4.p1.1`："DualEvolve alternates mechanism revision under the fixed promotion gate with process-guided updates to the harness and skill rules that shape the next round’s search."

- 4.1.2. Two-Rung Screening and the Promotion Gate，`#S4.SS1.SSS2.p5.1`："The inside wiki retains task-local scores, budgets, and lessons."

- 4.2.2. Thompson-Sampling Action Selection，`#S4.SS2.SSS2.p1.2`："After each round, a menu agent proposes at most one harness edit and one skill edit, each adding, retiring, or merging rules."

- 4.2.2. Thompson-Sampling Action Selection，`#S4.SS2.SSS2.p4.1`："After the selected menu action, a separate stagnation check can append direction guidance to the harness, including when that action is KEEP."

- 5.4. RQ3: Do Evolved Rules Transfer?，`#S5.SS4.p1.1`："We initialize Software/NGCF with source-evolved harness and skill rules or the initial rules (No Transfer), holding them fixed for one target round."

范围与证据限制：

- 内层推荐模型不是Agent自身backbone，不能把“双层”直接标为Agent权重/Harness共演化。
- 外环有LLM过程grader及解析失败fallback，固定promotion gate评价的是推荐候选，不是每条规则直接获得独立性能批准。

## arxiv:2611.04466 — From Watching to Steering: Enabling Human-Coding Agent Collaboration through Execution Traces

摘要初判 `include` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

根据执行trace和用户纠错抽取Context/Decision/Strategy，生成Create/Revise/Merge/Remove技能patch，评分后更新持久技能池并冻结在后续任务评估。

来源：[官方正文](https://arxiv.org/html/2611.04466)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.04466.html.html`；SHA-256 `cbf6190999fe9210afc227f7c1820f3824b60d8d9078578cdb6d3878c4978cb4`。

- IV-C Online Trace-to-Skill Distillation，`#S4.SS3.p6.1`："Skill Patch Distillation."

- IV-C Online Trace-to-Skill Distillation，`#S4.SS3.p6.2`："where Distill ⁡ ( ⋅ ) \operatorname{Distill}(\cdot) is implemented using a large language model."

- IV-C Online Trace-to-Skill Distillation，`#S4.SS3.p8.1`："For a patch q q , the scorer first predicts 𝐡 ⁡ ( q ) ∈ [ 0 , 1 ] 2 \mathbf{h}(q)\in[0,1]^{2} , representing its expected reusability and correctness ."

- IV-C Online Trace-to-Skill Distillation，`#S4.SS3.p8.3`："where ⊕ \oplus denotes applying the selected create, revise, merge, and remove operations."

- V-A Skill-Based Agent Evolving Mechanism，`#S5.SS1.p2.1`："Dataset and Metrics."

- V-A Skill-Based Agent Evolving Mechanism，`#S5.SS1.p4.1`："Baselines."

范围与证据限制：

- skill准入分数是LLM对正确性和节省的预测，不等同实际执行回归门。
- SWE-bench量化实验的Redirect/Outcome Correction由verifier模拟，不能称全部真人反馈。

## arxiv:2611.04483 — CogniLife: Continuous Cognitive Distillation for Deployed Multi-Expert Agent Marketplaces

摘要初判 `borderline` → 正文建议 `borderline`；独立建议 `borderline`；正式决定 `defer`。

提出从交互证据修订决策规则/程序性skills并服务后续调用的生命周期；现有实现将capability failure转为候选并保留staging，但配对评估到active promotion尚未贯通。可作Harness架构/理论讨论候选，不能作为已实现持续技能闭环主方法批准。

来源：[官方正文](https://arxiv.org/html/2611.04483)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.04483.html.html`；SHA-256 `079eb4a8aa09051faa3b875a3185e342fb0263a366e8a9bae94c27cfd5b0b96b`。

- 3.2 Continuous Distillation Lifecycle，`#S3.SS2.p1.1`："Continuous cognitive distillation turns observable communication, stated reasoning, and procedural choices into revisable textual guidance."

- 3.2 Continuous Distillation Lifecycle，`#S3.SS2.p2.1`："The proposed Creator Profile holds transferable creator patterns; the Expert Journal holds listing-specific knowledge and procedures."

- 3.4 Creator-Controlled Refinement，`#S3.SS4.p2.1`："Candidate formation."

- 3.4 Creator-Controlled Refinement，`#S3.SS4.p4.1`："Deployment control."

- Candidate acceptance and version promotion.，`#A6.SS0.SSS0.Px3.p1.1`："The illustrated existing-skill path stages proposed content on an applicable personal or shared row, retaining the preceding active body."

- Platform new-skill exception.，`#A6.SS0.SSS0.Px4.p1.1`："Outside the illustrated marketplace path, the platform subjects profy and profy-distill , when no marketplace-expert record exists, can accept an authorized no-parent proposal by creating an enabled personal skill in the acceptor’s active workspace."

- Different acceptance rules and Soul boundary.，`#A6.SS0.SSS0.Px5.p1.1`："Memory extraction, temporal consolidation, authoring, and skill promotion are separate paths with their own checks."

范围与证据限制：

- 候选准入大多是模型估计；不是已测执行收益。
- no-parent主动skill例外存在，但作者明确它不建立完整自动对话到技能生成闭环。
- Harness专项理论可纳入；保留边界是文献角色与实现证据待owner裁定，不是要求所有理论必须实现。

## arxiv:2611.04772 — TactiNavi: Serving and Revising an LLM Game Coach with Explicit Strategy Conditions

摘要初判 `include` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

反馈触发诊断并提出版本化策略条件与依赖执行规则修订，系统规定held-out release checks和回滚；两轮实际revision的回放专项审计检验修复增益是否可复现。

来源：[官方正文](https://arxiv.org/html/2611.04772)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.04772.html.html`；SHA-256 `53d84772bf70e37e619c3072b3de481c25a6370a0062b4354adfee4fb26ff245`。

- 4.1 Overview，`#S4.SS1.p1.1`："Figure 1 shows TactiNavi as a compiler and two planes that share one representation, together with an evaluator that connects them."

- 4.2 Strategic Knowledge Compiler，`#S4.SS2.p3.1`："Dependency index."

- 4.4 Diagnosis and Repair Evaluator，`#S4.SS4.p4.1`："Repair effect."

- 4.5 Evolution Control Plane，`#S4.SS5.p6.1`："Generality and rollback."

- 5.1 Setup，`#S5.SS1.p2.1`："Periods and replay."

- 5.4 Revision Gains and Release Validation，`#S5.SS4.p2.1`："We then apply the release checks retrospectively to the 15 deployed revision units with criteria fixed in advance."

- 5.4 Revision Gains and Release Validation，`#S5.SS4.p3.1`："Only one deployed unit satisfies the release criteria."

范围与证据限制：

- release gate是对15个历史已部署unit事后应用，仅1个通过；不能声称这些上线前全通过验证。
- replay仅改knowledge和reply-stage rules，固定规划和工具输出，不是全系统重新执行。

## arxiv:2611.04952 — Artifact-to-Capability: Diagnosing Breaks in Capability Formation of Self-Evolving Agents in a Controlled Environment

摘要初判 `include` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

专门诊断持久工件到能力的反馈演化链：同一base model下演化Reflexion记忆、Voyager技能/调用程序、DGM代码谱系，再冻结并按状态、整局、版本谱系检验作用、冲突和保留。

来源：[官方正文](https://arxiv.org/html/2611.04952)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.04952.html.html`；SHA-256 `c1c2c5865e0dd6fa77a1894ab55ef7f2e3e65511f1eeb928c7c20df3b71c37a0`。

- 3.1 Five Diagnostic Properties，`#S3.SS1.p1.1`："In the self-evolution loop (Figure 2 ), the system compresses part of its interaction trajectories into persistent artifacts and invokes them in later decisions."

- 3.1 Five Diagnostic Properties，`#S3.SS1.p2.1`："The dependency structure is 1 → 2 → ( 3 ​ and ​ 4 ) → 5 1\rightarrow 2\rightarrow(3\text{ and }4)\rightarrow 5 ; we call this sequence the capability chain ."

- 3.2 System-Level Unit of Analysis，`#S3.SS2.p1.1`："Our object of diagnosis is the frozen system : all artifacts that actually participate in decision making in a frozen version, taken as a whole."

- 4 Experimental Design，`#S4.p1.1`："The three mechanisms evolve autonomously with the same base model (DeepSeek-V4-Flash), environment, and opponents."

- 4.2 Three Scales，`#S4.SS2.p1.1`："State-level diagnosis."

- 4.2 Three Scales，`#S4.SS2.p3.1`："Lineage-level diagnosis."

- 4.3 Three Mechanisms，`#S4.SS3.p1.1`："The three mechanisms cover three artifact forms; implementation details are in Appendix F ."

- 5.2 Voyager: Compositional Override，`#S5.SS2.p2.1`："In game-level diagnosis, however, Voyager reaches an immediate-win state in all 20 games yet completes five at none of them (0/20), blocking the opponent’s immediate winning point instead and losing every game (Figure 4 )."

- 5.3 DGM: Loss-Only Drift After Capability Formation，`#S5.SS3.p2.1`："Lineage-level diagnosis, however, shows no extension afterward (Table 3 )."

- Limitations，`#Sx1.p1.1`："How the three break types are distributed across mechanisms and tasks requires diagnosis at a larger scale."

范围与证据限制：

- 方法是文中实现的三种机制及五子棋诊断；跨GUI等推广明确为未验证猜想。
- DGM OB-3通过能力形成检查，但后续版本未扩展；不能写为三者均没有任何能力形成。
- 所读段落支持机制与诊断对象；未复算实验数字或复现。

## arxiv:2611.05139 — Meta$^2$: Precomputing Reusable Knowledge for Online Harness Evolution in Long-Horizon Agents

摘要初判 `include` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

离线以A/B/C轨迹和verifier终局反馈反复增改删版本化Meta-Skill中的act/hold/avoid干预规则，跨任务聚合后冻结供evolver后续调用；保留的是改进器决策规则而非在线临时Harness补丁。

来源：[官方正文](https://arxiv.org/html/2611.05139)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.05139.html.html`；SHA-256 `c63870da606fc503d5cb1c71cf86da8ab2e9a58f18b13867cbefccfafe045254`。

- 3 Meta 2 : Precomputing Reusable Knowledge for Online Evolution，`#S3.p1.1`："Meta 2 answers this question by moving the offline stage one level up."

- 3.2 Offline Component: Precomputing Reusable Evolution Knowledge，`#S3.SS2.p2.1`："Optimize the knowledge, not a single harness."

- 3.2 Offline Component: Precomputing Reusable Evolution Knowledge，`#S3.SS2.p3.1`："A/B/C rollouts make terminal feedback informative."

- 3.2 Offline Component: Precomputing Reusable Evolution Knowledge，`#S3.SS2.p4.1`："Five contrast directions."

- 3.2 Offline Component: Precomputing Reusable Evolution Knowledge，`#S3.SS2.p5.1`："From task-level contrasts to reusable rules."

- 3.3 Deployment Component: Frozen Knowledge and Task-Local Edits，`#S3.SS3.p2.1`："Freeze globally, adapt locally."

- B.1 Offline Meta-Skill Construction，`#A2.SS1.p3.1`："Reflection, aggregation, and update."

- B.2 Online Checkpoint Evolution，`#A2.SS2.p2.1`："Decision and edit semantics."

- I.1 Entry Structure，`#A9.SS1.p1.1`："A Meta-Skill is a versioned textual library that guides harness evolution at checkpoints."

范围与证据限制：

- 每个部署run重置seed harness；在线patch和checkpoint对话不跨run保留，Meta-Skill也不在线更新。
- A/B/C为run级对比，轨迹可能早于干预就分叉，不能将终局差异当单一编辑的因果效果。
- accepted online edit验证是edit contract约束，不保证每次干预性能改善。

## arxiv:2611.05251 — A semi-autonomous multi-agent pipeline for high-energy astrophysics research with enforced provenance and verifiable self-extension

摘要初判 `include` → 正文建议 `include`；独立建议 `include`；正式决定 `defer`。

Agent发现缺失能力后编写自身可调用工具的lib与skill包装，测试和独立co-lead反馈触发限次修订，通过两类检查才原子提交到持久toolkit，供后续分析复用；主编排代码受保护。

来源：[官方正文](https://arxiv.org/html/2611.05251)；缓存 `build/maintenance-2026-11-05/s2-primary-bodies/2611.05251.html.html`；SHA-256 `1b88b9145159f078d4ddada0ff18c315014168023406a1607358e1d513485662`。

- 2.1 Design principles，`#S2.SS1.p2.1`："Two repositories."

- 2.1 Design principles，`#S2.SS1.p3.1`："Two halves per tool."

- 2.2 Agent team and infrastructure，`#S2.SS2.p1.1`："auto_research is built on LangGraph [ 26 ] , and the agents exchange typed messages defined with Pydantic [ 27 ] ."

- 3.2 Checks on new tools，`#S3.SS2.p2.1`："The gate checks mechanical properties."

- 5.2 Catch rate of planted defects，`#S5.SS2.p1.1`："We know of no established benchmark for how well checks catch defects in AI-written scientific code, so we built one."

- 5.2 Catch rate of planted defects，`#S5.SS2.p3.1`："Table 4 gives the results for the default configuration."

- 5.3 Reliability and cost of tool writing，`#S5.SS3.p1.1`："To measure the reliability and cost of tool writing, we had the pipeline write the same tool in repeated trials, following Gendreau-Distler et al. [3] ."

- 7 Discussion，`#S7.p1.1`："Unlike systems that write new code for each task [ 4 , 12 , 1 , 13 ] , auto_research keeps the tools that it writes."

- 7 Discussion，`#S7.p2.1`："Our results are based on four analyses of similar data."

范围与证据限制：

- 文中尚未测量后续分析实际复用已提交工具的频率；设计保留与实测复用需分开。
- provenance只核数值来源不保证正确性，co-lead有漏检与误拒。
- 科研结果是外部产物，但更新的工具库与调用manifest成为Agent工具接口，故归组件；不能把冻结主编排误作完全无Harness更新。
