# 2026-11-05 S2补入批次独立范围复核

**33项选定正文：28 include / 3 exclude / 2 borderline。** 另读6项排除候选完整原始摘要（RSI-Dojo定向+seed 20261105随机5项），均建议exclude；6个当日HF交叉仅复用既有独立意见。

**覆盖边界：76个新增S2 ID中独立读39份完整摘要、33项正文选段，37项没有独立初筛。** 本报告items共45项（含6复用）；不把主审76项阅读算成独立阅读。本版精确核验132处正文短引句、6处摘要引句。

**正式决定全部defer、publication_authorized=false。** 既有quality gate 24/28=0.8571低于0.90，本次未付费、未复现实验、未重跑gate、未改canonical、未发布。

## 可复核来源与顺序

33项正文结论冻结稿 SHA256：`212c9a98ec4afc8d7b458c0d92e8ac07b01f13b993246eb08269ecc2bc5a5505`。每项保留官方HTML定位、原始响应与metadata SHA256、摘要来源哈希、实际阅读选段和边界。6个HF复用中2个摘要字节相同，4个仅LaTeX包装/数学或货币符号差异，旧意见与新S2哈希分开保存。7个S2—official摘要差异均只为空白。

原59项主审现66/66引句与59/59范围意见核验通过，绑定primary SHA `b3c0404e6e878d375b53bdc2192d4fc168f37a6fbbd4e46d16012ad41b71b93e`；新增Reglos冻结后gate、Route Anything持留model身份记录已核对。

生产prompt的“主要改进对象”旧限制未应用owner的新边界，本复核按程序工件—反馈—持留判断。

## 重点边界

- CARE：真实程序版本变更存在，但owner/工程师编辑且context change明确不属于自动loop，建议exclude；不因模型贡献为主排除。
- Harness-S：先演化程序、再冻结pool训练模型；RSI-Env则有H0/M0→H1/M0→H1/M1并继续研究的真实双侧版本链。
- Meta²：跨任务保留的是反馈学习的Meta-Skill；在线Harness edits在任务结束即丢弃。
- WASP-Mem：GitLab认证分页/错误恢复程序wiki与代码修订有具体证据；MAPLE主要为UI action-effect事实。
- ModelBlaster保留borderline：实际更改claims/states/hypotheses与UCB统计，但缺清晰持久程序性entry来区别经验内容。
- CogniLife保留borderline：Harness规则设计相关，普通skill候选到active promotion路径未闭合；scope允许理论，未实现不是唯一排除标准。
- TactiNavi仅1/15历史修改事后过gate；Vibetrace量化反馈由verifier模拟；auto_research trusted promotion仍需人。

## 主审比较

已绑定最终主审 SHA `ddec710fe8350e171f8eb488ac743c552eccb70b91ec53c629e37fa5a05b18ea`。33正文范围32一致；6排除摘要抽查、6HF复用各6/6一致，合计44/45。37项未独立初筛不计一致率。主审最终174处引句均独立匹配原始HTML。唯一未决范围为ModelBlaster：主审exclude、独立borderline，协调保留borderline且formal defer。WASP-Mem主审由borderline依据程序性自然语言skill规则改为include，保留本人选读证据与初判历史；未审计原始wiki补丁。RSI-Env范围双方include，但主审evolve_main、独立coevolution；其双侧版本链已明示，标签差异单列JSON。其他辅助标签差异不改范围。

## 45项逐项意见

|ID / 标题|建议|阅读深度|理由|
|---|---|---|---|
|arxiv:2610.40663 Learning from Expert-Corrected Misdiagnoses: A Self-Evolving Consultation Agent for Traditional Chinese Medicine after Failed Treatment|include|独立完整摘要+正文选段|临床 skill document 是唯一可变程序指导，失败病例与专家分析驱动最小编辑，经held-in/validation准入后继承到后续轮次和sealed test。|
|arxiv:2610.40747 Mage-VL-Cowork: A Full Training Recipe to Learn Hybrid Computer Use From Evolved Harnesses|include|复用今天HF独立意见|先反馈驱动演化教师完整外部执行 Scaffold/接口/提示，再固定教师 Harness 生成轨迹训练学生；外部程序循环足够明确。|
|arxiv:2610.40758 More Rules, Longer Lists? Benchmarking Self-Evolving Agents on a Hidden-Rule Curriculum|include|独立完整摘要+正文选段|CLR-Bench直接对比反馈驱动的持久prompt/skill演化方法，含GEPA和EvoSkill；其记忆化失败是评测结论，不抹掉被研究的程序演化对象。|
|arxiv:2610.41157 Lineage Is Memory: Parent Inheritance and Feedback Disclosure in Short-Budget LLM-Guided Optimization|include|独立完整摘要+正文选段|以系统提示优化为明确研究对象，控制parent继承与失败披露，评分通过的prompt候选保留跨轮并在独立holdout测试；属于Harness演化专项对比。|
|arxiv:2610.41809 Continual Reinforcement Learning Is an Integration Problem|exclude|独立完整摘要抽查|连续RL一般desiderata与持久世界场景概念，不专门研究外部Harness程序反馈演化。|
|arxiv:2611.00180 Learning to Live: A Step Toward Lifelong Embodied Intelligence|include|独立完整摘要+正文选段|EDM将困难任务经验蒸馏为去除硬编码的tools/skills/builders，用execution feedback修订后mount，后续任务调用冻结能力；与memory内容更新明确分开。|
|arxiv:2611.00463 Exo: An Architecture for Self-Improving Systems at Runtime|include|独立完整摘要+正文选段|运行中按执行经验和成本改写executor政策代码，激活新版本并保留历史；后续新账户目标与graded tasks继承自修改，满足整体Harness演化。|
|arxiv:2611.00504 Robustness Starts with the Objective: Designing and Certifying Robust LLM-Generated Heuristics|exclude|独立完整摘要抽查|TAILOR演化GPU admission/VM packing/server placement外部系统heuristic；未展示agent自身可复用执行程序更新。|
|arxiv:2611.00518 Agentic Context Management for Multi-Turn Human-AI Conversations|exclude|独立完整摘要抽查|AC3固定analyzer在会话中重建当前上下文；更新输入内容，无反馈修订并跨任务继承analyzer程序。|
|arxiv:2611.00643 Selecting LLM-Generated Hypotheses Raises Truth Beyond What an LLM Panel Expects: A Pre-registered Study on NAS-Bench-201 and HPOBench|include|独立完整摘要+正文选段|直接检验研究者Harness优化的质量与judge偏好失配；Opus依据scored traces改可复用角色、检索、selection和strategy字段，并严格优于incumbent才继承。|
|arxiv:2611.00752 Reading Between the Chapters: A Graph-Free RAG Rebuilt With AI and Human Feedback|exclude|独立完整摘要+正文选段|LadderRAG有真实反馈驱动代码版本与后续使用，但每项改动由作者提出、AI助手实现、作者审核，属于人工架构设计迭代，未研究系统自己提出并持续演化Harness的机制。|
|arxiv:2611.00960 Self-Refining Prompt Induction for Streaming Text-to-SQL|include|独立完整摘要+正文选段|固定权重的Refiner按生成失败与judge反馈改写可复用dialect prompt，采样回归guard准入，accepted prompt跨轮继承并在推理时冻结。|
|arxiv:2611.01113 CogRSI: Evolving and Auditing Cognitive Reasoning Strategies|include|独立完整摘要+正文选段|失败反馈驱动最多五条短When规则的添加/修订/退役，填入reader的principle slot，经校准准入后形成可复用策略库。|
|arxiv:2611.01351 MAPLE: A Multimodal Mobile Agent with Playbook-Learned Experience|exclude|独立完整摘要+正文选段|MAPLE确有跨episode反馈持留，但Playbook条目明确是UI action-effect declarative fact、embedding和置信计数，固定consolidation只插入/去重事实，未改可复用程序或管理策略文件。|
|arxiv:2611.01386 Learning by Doing: Autonomously Compiling and Curating Agent Skills from Verified Traces|include|独立完整摘要+正文选段|Zep compiler读取verified Traces与既有Skills，Reflector/Curator按证据add/patch/merge程序性Skill，准入生成不可变版本并供下一run加载。|
|arxiv:2611.01695 SPAR: Experience-Driven Strategy Evolution in Multi-Session B2B Sales|include|独立完整摘要+正文选段|销售执行结果经策略归因后触发共享playbook中的条件/决策策略修订、合并和退役，跨merchant继承；不是仅存客户事实。|
|arxiv:2611.01736 RSI-Env: An Open-Ended Environment for Recursive Self-Improvement of Agents|include|独立完整摘要+正文选段|RSI-Env同时支持并展示真实Harness和模型版本更新：H0/M0→H1/M0→H1/M1，更新后的系统继续生成下一次改进，满足owner双侧版本标准。|
|arxiv:2611.01840 Self-Evolving Agentic Workflows via Semantic Decomposition of Complex Tasks|include|独立完整摘要+正文选段|SeaFlow编码agent按执行traces/outcomes修改语义任务树与code/model procedures，候选验证后成为下一轮保留workflow。|
|arxiv:2611.01870 Automated Stateful Specialization for Adaptive Agent Systems|include|独立完整摘要+正文选段|ASpec Architect利用历史架构和执行performance演化specialist身份/方法指令及团队图，保留架构与池供后续query；cultivation记忆是附加机制。|
|arxiv:2611.02017 Switch-SWE: Do Coding Agents Hold Focus When Switching Between Unfinished Tasks?|exclude|复用今天HF独立意见|多任务切换评测和固定上下文模块；更新的是任务状态摘要，未改模块本身。|
|arxiv:2611.02079 ParetoSaddler: Pareto-Guided Optimization of Agent Harnesses for Quality and Cost|include|复用今天HF独立意见|完整 Harness 候选经轨迹诊断修订，质量—成本联合估计控制晋升并保留候选；新贡献重心为噪声下准入与成本权衡。|
|arxiv:2611.02501 SpecPilot: Autonomous Algorithm Discovery and Systems Optimization for Speculative Decoding|exclude|复用今天HF独立意见|程序、反馈、代码记忆和跨部署复用均存在，但演化对象是外部 speculative decoding serving/kernels，非优化 agent 自己的 Harness。|
|arxiv:2611.02516 Cumulative and Audited Guardrail Tool Evolution for LLM Agent Safety|include|独立完整摘要+正文选段|EVOLVE把风险/执行/audit反馈转成Python guardrail工具的融合和修复，审核后保留在lifelong库供未来防护调用。|
|arxiv:2611.02797 SelfImprove-Bench: Evaluating Generalization in Self-Improving Agents|include|独立完整摘要+正文选段|SelfImprove-Bench固定backbone直接评测AHE/HyperAgents等反馈驱动Harness及improver版本修订，追踪跨实例、难度和任务迁移，是明确Harness特定评测。|
|arxiv:2611.02830 Think with Skills: Pseudocode Planning Before Execution for Advanced Reasoners|exclude|独立完整摘要抽查|训练模型将固定expert skills转成当前任务pseudocode；未保留反馈修改的通用程序/skill版本。|
|arxiv:2611.02839 CARE: Grounded Recursive Self-Improvement for Production Customer-Service Agents|exclude|独立完整摘要+正文选段|CARE有真实Skill/SOP/Harness版本变更，但正文把这些编辑交给业务owner/工程师，明确不属于自动学习环；系统反馈链更新模型权重，未展示Agent生成并继承程序修订。|
|arxiv:2611.03434 Optimize the Harness, Not the Model: Fitting a Minimal Agent to a Self-Hostable LLM for Investigative Analysis|include|独立完整摘要+正文选段|CLEO以supervisor LLM自动提出、执行评估并保留Harness版本；已接受tools/guardrails/context/memory policy等更改产生error analysis驱动下一轮。|
|arxiv:2611.03618 Strategist: Evolving Reasoning with Agents|include|独立完整摘要+正文选段|Strategist按候选推理程序的真实样本trace与分数修订blueprint，积累可组合Python推理流程库供后续任务再用。|
|arxiv:2611.03674 ReVi: Recursive Recap Video Generation|include|独立完整摘要+正文选段|ReVi的反馈不止修改视频成品，而是跨小说保留编辑prompt/config与诊断、提案、预算分配meta-policy；候选经固定gate形成下一代程序。|
|arxiv:2611.03685 LOLPlay: Benchmarking Real-Time Visual Agents in League of Legends|exclude|复用今天HF独立意见|实时游戏视觉 Agent 能力评测；不研究 Harness 持久反馈演化。|
|arxiv:2611.03698 Training LLM Agents to Automate LLM Post-Training with RSI-Dojo|exclude|独立完整摘要抽查|摘要说明训练环境/模型训练轨迹与fine-tuning；improved harness只为轨迹采集配置，未给反馈改写持久程序链。|
|arxiv:2611.03868 EvoGroup: A Self-Evolving Harness for Group Agents in Shared Contexts|include|独立完整摘要+正文选段|EvoGroup用置信度与官方任务结果筛trace并归因，改工具实现、retrieval算法、prompt、调度及memory管理，迭代Harness后冻结跨benchmark评测。|
|arxiv:2611.04003 WASP-Mem: Let Agent Organize Procedural Memory. Human Spend Effort on Diagnosis|include|独立完整摘要+正文选段|WASP-Mem的wiki含可复用执行程序/恢复步骤和代码，Agent根据运行及诊断反馈修订页面，下轮运行继承；具体程序修订使其超出普通记忆内容。|
|arxiv:2611.04035 Recursa: Toward Recursively Self-Improving Foundation Model Systems|include|复用今天HF独立意见|Recursa 自称运行时 harness 固定，但其 repository 中的程序性 instructions/skills 经反馈修订、回归验证与合并，符合本项目外部 Harness 工件定义。|
|arxiv:2611.04104 ModelBlaster: Closing the Performance Gap through Learning-Augmented Agents Across Models, Kernels and Hardware Backends|borderline|独立完整摘要+正文选段|ModelBlaster确有持久反馈更新，但当前正文实物主要为性能state/action/outcome/claim与UCB统计，代码演化对象是外部kernel/model；未定位到明确改写的可复用Agent程序策略entry，保留边界。|
|arxiv:2611.04277 Harness-S: Learning from Sibling Harnesses for Generalizable Agent Training|include|独立完整摘要+正文选段|Harness-S先用失败trace对parent prompt/skill/context/memory/hook/toolview产生多代候选，评估选parent并保留sibling程序库；真实Harness演化成立。|
|arxiv:2611.04431 Reducing the arithmetic cost of quantum derivative pricing with language-model circuit design|exclude|独立完整摘要抽查|LLM-assisted circuit搜索修改量子金融线路产物，不是自身Agent工具/策略/编排。|
|arxiv:2611.04437 WiSI: Wireless-in-the-Loop Self-Improvement|include|独立完整摘要+正文选段|WiSI让LLM根据无线执行trace改写自身具身任务agent的solve程序（导航/感知/通信决策），评估选parent，日志与程序继承下一代；非外部无线产品优化。|
|arxiv:2611.04439 DualEvolve: Dual-Level Self-Evolution of Mechanism and Orchestration for Recommendation|include|独立完整摘要+正文选段|DualEvolve外环以过程评分与执行trace修订研究agent的harness/skill规则，下一轮继续使用并可迁移；内环推荐模型产物不是唯一演化对象。|
|arxiv:2611.04466 From Watching to Steering: Enabling Human-Coding Agent Collaboration through Execution Traces|include|独立完整摘要+正文选段|Vibetrace用执行trace与人类/验证器反馈自动蒸馏Context/Decision/Strategy程序性skill，create/revise/merge/remove后跨任务保留。|
|arxiv:2611.04483 CogniLife: Continuous Cognitive Distillation for Deployed Multi-Expert Agent Marketplaces|borderline|独立完整摘要+正文选段|CogniLife提出跨expert归因后持续修订决策规则/程序的Harness设计，但部署版本程序候选停留staging，成对评估到promotion未闭合；作为Harness概念研究可相关，尚非已实现演化证据。|
|arxiv:2611.04772 TactiNavi: Serving and Revising an LLM Game Coach with Explicit Strategy Conditions|include|独立完整摘要+正文选段|TactiNavi根据player反馈trace提出程序性策略适用条件与reply执行规则修改，依赖闭包组成版本包；研究直接评估反馈修订的复用性和发布gate。|
|arxiv:2611.04952 Artifact-to-Capability: Diagnosing Breaks in Capability Formation of Self-Evolving Agents in a Controlled Environment|include|独立完整摘要+正文选段|Artifact-to-Capability在固定模型下直接检查反馈演化的Voyager Python技能/调用程序与DGM code lineage，定义并诊断持久程序能力形成及退化。|
|arxiv:2611.05139 Meta$^2$: Precomputing Reusable Knowledge for Online Harness Evolution in Long-Horizon Agents|include|独立完整摘要+正文选段|Meta²离线将多任务rollout/反馈对比转成持续增删修订的Meta-Skill，冻结后跨任务指导KEEP/EVOLVE；可复用演化决策程序满足持留标准。|
|arxiv:2611.05251 A semi-autonomous multi-agent pipeline for high-energy astrophysics research with enforced provenance and verifiable self-extension|include|独立完整摘要+正文选段|auto_research由Agent提出缺失分析能力并写tool manifest/wrapper/code，拒绝反馈触发修复；经checks和cross-provider review后工具留存供未来分析调用。|

37项未独立初筛ID、每项短引句与counterevidence见 [independent-s2-review.json](independent-s2-review.json)。
