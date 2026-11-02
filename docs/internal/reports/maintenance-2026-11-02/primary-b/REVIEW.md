# 2026-11-02 历史积压 B 组初审

本组完成 82/82 条逐篇来源与范围建议：建议纳入 10、建议排除 68、范围待定 4。其中 1 条被 IEEE 原站空响应阻塞，另外 3 条已读方法正文，但程序工件与经验/任务产物边界仍需补证。全部保持 `formal_decision: defer`，没有人工批准或发布授权。

这是独立的 B 组初审冻结结果，不代表三轮审核已经完成。冻结前没有读取 A 组或独立复审的结论。

## 阅读与核验边界

- 79 条 arXiv：重新解析并校验 11 份历史官方 Atom 快照。摘要不是本日新抓取；不把旧论文归入今天 HF 日报。
- 19 条候选/边界项：本日成功获取官方 HTML，阅读正文方法与有关附录。具体零起始段落范围写在各条 `sources` 中；不声称通读全部论文。
- 3 条 S2-only：Crossref 身份核实；2 条取得 bioRxiv/Nature 官方摘要，1 条 IEEE 两次 HTTP 202 且 0 字节。
- 校验 166 条引句、37 个原始来源文件 SHA256；19 份 arXiv 与 2 份出版社 HTML 提取文本均由原始快照重新生成比对。
- 本次不做数字复现实验、不赋予证据卡 yes/no 等级；未知项维持 unknown。反馈与持久化字段描述的是被改对象，记忆/权重/外部产物的 yes 不代表 Harness 纳入。

## 建议纳入（仍需独立复审与人工决定）

| ID | 论文 | 限定范围与理由 |
| --- | --- | --- |
| `arxiv:2609.37725` | Context Language Models | 限定收录 §4.2/§5.2 的文本技能优化分支：执行轨迹改写可复用上下文管理技能，开发集选新版本并冻结测试。另有 RL 分支，不把其权重训练算 Harness。 |
| `arxiv:2610.04008` | SkillScriptBench: Benchmarking Self-Evolution of Executable Agent Skill Packages Beyond Markdown | 专项评测既有可执行 Agent Skill 包的文档/脚本修复和正确行为保留；适用 Harness 评测例外。评测框架本身无需演化。 |
| `arxiv:2610.09684` | From Pareto to Preference: Personalized Test-Time Scaling via Amortized Agentic Policy Discovery | 反馈修改路由、分支、停止和自修正的可执行推理控制器；保留获选代码并跨用户复用，正文明确不更新 Agent 参数。 |
| `arxiv:2610.11552` | Safe, Persistent, and Evolving Agent Harness for Understanding Partially Observable Worlds | 除隐藏规则知识外，正文明确按轨迹反馈改 task/tracking/policy-context/policy-compilation 提示和代码；验证选择 Harness 后留出测试。 |
| `arxiv:2610.12289` | TestPrism: Rethinking Test Evaluation Beyond a Single Reference | 限定 TestHelix 的跨任务策略优化分支：AutoSaddler 根据执行反馈修订策略，独立验证后冻结相同提示/配置用于后续模型评测。 |
| `arxiv:2610.14515` | SEPM: Self-Evolving Procedural Memory Grounded in Task Graphs for Multi-Agent Collaboration | 正文不仅保存经验：版本化程序包含可执行步骤及依赖图，检索后实例化协作任务图；试验净收益门控后升为活动版本并跨任务持久化。 |
| `arxiv:2610.17130` | EvoQuantLab: Training-Free Dual-Loop Evolution for Auditable Quantitative Research | 限定慢外环：按训练/开发执行证据修订搜索和评测协议，补丁版本只在下一研究周期生效；内环 alpha 因子本身仍属外部产物。 |
| `arxiv:2610.23709` | GLOBE: Evolving Structured Agentic Memory for E-commerce Product Optimization in Generative Search | 限定版本化字段编辑行为指令：反馈不止增加事实记忆，还改 instruction、适用条件和允许字段；Curator 提交新策略后供下一批使用并冻结测试。 |
| `arxiv:2610.36618` | Dream-COP: Guiding Algorithm Discovery for Combinatorial Optimization Problems in an Experience World | 主要方法学习支配 discovery Agent 的可执行停止/分支/分配策略；回放反馈修订后下一真实轮执行，另测试跨问题固定代码迁移，明确不改权重。 |
| `arxiv:2610.37276` | Where Should the Evaluation Budget Go in LLM-Driven Agent Scaffold Evolution? | 专项研究反馈驱动 Agent scaffold 演化的搜索期/最终选择评估预算；适用 Harness 评测与方法专项，不把固定 EvalAlloc 当自改进主体。 |

优先交叉核对 SEPM、EvoQuantLab、GLOBE：本组纳入的依据分别是可执行依赖图、跨周期协议补丁、版本化行为指令；不能只凭 procedural memory、protocol 或 handbook 名称纳入。CLM 仅指其明确的文本技能演化分支。

## 待定或阻塞

| ID | 论文 | 待补证 |
| --- | --- | --- |
| `arxiv:2610.13194` | JANUS: Enhancing Long-Horizon Autonomous Research with Co-Evolving World Models | 需作者代码或工件实例证明 coordination/exploration skills 的持久存储格式、如何进入控制执行以及反馈接受条件；当前正文不足以跨过记忆内容边界。 |
| `arxiv:2610.17488` | Origin Attribution for Unsafe Behavior in Self-Evolving Multi-Agent Coding Systems | 需初始程序/运行接口或作者代码确认 routing functions 控制 Agent 的工具/工作流，而非仅为 OpenEvolve 输出的外部应用；在该身份边界核清前不纳入 Harness 计数。 |
| `arxiv:2610.19386` | STRATA: Self-Maintaining Structured Experience Graphs for Self-Evolving Language Agents | 需真实 atomic code/skill 节点及消费接口，核对其为持续修改的可执行工具/策略文件，而非记忆中的代码文本和经验条目。 |
| `s2:632b5b25ba18a2a2d45a6f62d49f68f3291e2cb7` | Capability-Aware Dynamic Skill Selection for Memory-Augmented Generation | 需可访问的 IEEE 原文/作者公开稿以确认技能路由是否固定；Crossref 日期只有 2026-10，不能核实 canonical 的 2026-10-01 精确日。 |

## 建议排除（不等于已执行 reject）

| ID | 论文 | 理由 |
| --- | --- | --- |
| `arxiv:2609.36675` | G\"odel Forest: Balancing Search Depth and Breadth for Data-Centric Recursive Self-Improvement | 核心是用生成数据训练模型参数；持久树和经验记忆不改变其主要训练对象。 |
| `arxiv:2609.36739` | Frontier Autolab: Organizational Memory, Adversarial Dissent and Temporal Leakage in Multi-Agent LLM Firms Across Fifty Years of Technological Change | 评测跨时代组织决策和 Playbook 经验；不是外部 Harness 工件反馈演化专项评测。 |
| `arxiv:2609.37002` | Visual Parallel Search: Learning to Search High-Resolution Images with Parallel Tile Inspection and Adaptive Zoom | 固定视觉检索接口配合 SFT/GRPO 训练控制器和读取模型；未说明反馈修改可复用 Harness。 |
| `arxiv:2609.38662` | CollabFlow: Recursive Self-Improvement of Agent Collaboration | 冻结的是执行器，反馈每轮重训 Collab-Director；不能把训练出的协作策略算外部 Harness。 |
| `arxiv:2609.38883` | Toward Quantum Software Automation: A Quantum-Aware Harness for LLM-Guided Evolution | 量子编译器和运行时策略是被搜索的外部软件产物；量子专用 Harness 是搜索框架。 |
| `arxiv:2609.39022` | From Verification Failures to Reusable Guidance for Coding Agents | 原文是专家诊断与人工指导开发可复用验证指导；未建立自主反馈改写并保留 Harness 的循环。 |
| `arxiv:2609.39143` | RefCon: Iterative Refinement and Contrastive Memory Extraction for Context-Evolving Agent | 迭代精炼对象是抽取出来的记忆；不是记忆管理代码或策略文件的演化。 |
| `arxiv:2609.39392` | Experimental Experience Modeling for Autonomous Research | 积累和检索实验经验记录，未说明改写研究 Agent 的控制流或工具。 |
| `arxiv:2609.39551` | RankEvolve: A Reliable Multi-Agent Auto-Research Harness for Evolving Ranking Models | 主要演化排名模型；EOP 和多 Agent 组合是既定实验执行框架，知识层保存发现。 |
| `arxiv:2609.40258` | Large Language Model-Guided Evolutionary Discovery of Native Neural Architectures for Spiking Sequence Modeling | 被演化代码定义 SNN 神经架构，是研究产物；不是编码 Agent 自身的 Harness。 |
| `arxiv:2609.40358` | Physis-Lang: Self-Evolving Language as a Physical Representation for Video World Model | 正文确有固定 captioner 的提示优化，但用途是视频世界模型训练数据和推理提示；主要贡献/训练对象为视频模型，不据辅助模块将整篇改列 Harness 主类。 |
| `arxiv:2610.00675` | LabBook: Harnessing Experimental History for Efficient LLM-Driven Discovery | LabBook 更新实验记忆并生成外部程序；摘要未把记忆管理机制本身列为可修改对象。 |
| `arxiv:2610.01026` | It Takes Workflows to Evolve Better Workflows | 工作流作为训练支架，主要更新参与生成和执行的模型角色；不是冻结权重的 Harness 演化。 |
| `arxiv:2610.01178` | Recova: Agent-Guided Failure Recovery for Autonomous Robotic Manipulation | 正文包含可复用恢复程序，但真实部署的主要更新是 task/recovery policies 的 DAgger 微调；库扩展服务于权重学习，保留为具身方向相关工作。 |
| `arxiv:2610.01235` | Harness Annealing: Learning to Act with Less External Control | 将外部控制内化到模型能力，主要是带课程的参数训练。 |
| `arxiv:2610.01787` | Not All Experience Belongs in the Weights: Component Routing for Self-Improving GUI Agents | 比较经验进入上下文或权重的效果；是经验/参数归宿评测，不是 Harness 工件演化专项。 |
| `arxiv:2610.02150` | From Knowledge Access to Source Learning: Developing Source-Specific Competence | 更新权威来源的可复用知识表示；没有说明管理代码或可复用控制策略被反馈改写。 |
| `arxiv:2610.02361` | SEDIMA: Cross-Run Hierarchical Insight Memory for Evolutionary Search Agents | 明确保持搜索算子不变，只蒸馏、聚类和检索跨运行洞见。 |
| `arxiv:2610.02945` | Continual Graph Memory for Mathematical Research Agents | 更新数学事实、计划、反例和研究前沿，是研究记忆内容而非 Harness 管理程序。 |
| `arxiv:2610.02996` | Evolutionary Computation for Trustworthy AI: From Attacks and Defenses to Self-Evolving Era | 综述覆盖攻击、防御和可信自进化多方向；不属于 Harness 外部工件反馈演化专项综述。 |
| `arxiv:2610.04555` | $\mathrm{TRIZ}^{a}$: Guiding Agent Evolution from Pattern Recognition to Solution Invention | 正文闭环主要生成领域代码/配置并评测网络安全检测产物；冻结变换协议和控制器对照不等于反馈改写 Agent Harness。 |
| `arxiv:2610.04851` | CURIO: Curiosity-Driven Test-Time Learning for Open-Ended Discovery | 测试时 RL 更新模型参数，ICWM 提供训练奖励；不是外部 Harness 演化。 |
| `arxiv:2610.04927` | Assembling Insights for Agentic Machine Learning Engineering Systems | 评测从 MLE 任务收集与注入洞见的作用，技能/手册是知识载体；并非 Harness 反馈演化专项。 |
| `arxiv:2610.05398` | MMPostTrainBench: Benchmarking Autonomous Research for Multimodal Post-Training | 专项评测多模态模型后训练研究，提交对象是更新模型；不是 Harness 专项。 |
| `arxiv:2610.06257` | SimAuthor: Harnessing Foundation Models for Persistent Scientific Simulator Authoring | 作者明确主要目标是科学模拟器本身；外部模拟器程序不等于 Agent 的 Harness。 |
| `arxiv:2610.06516` | Test-Time Adaptation of Reasoning Strategies with Bayesian Nonparametric Memory | 更新行为记忆的聚类统计和分量，固定贝叶斯检索机制未被改写。 |
| `arxiv:2610.06964` | Principles that Guide, Actions that Inform: Agent Evolution via Knowledge Abstraction | 从经验抽象程序性知识和原则并维护层级记忆；没有管理代码/策略文件演化证据。 |
| `arxiv:2610.06999` | ProactiveVLA: Augmenting Embodied Memory through Proactive Environment Exploration | 冻结 VLA 但变化对象是环境知识与经验记忆；冻结模型本身不足以通过 Harness 判据。 |
| `arxiv:2610.07625` | Stateless Language Agents: Scaling Long-Horizon Automated Research | Harness 固定管理科研状态和角色上下文；持续的是候选方案和结果，非 Harness 新版本。 |
| `arxiv:2610.07650` | Silicon Language: A Robot-Native Knowledge Exchange Framework for Heterogeneous Robots | 本次是操作员辅助知识包迁移；作者明确自主群体演化仍属未来工作。 |
| `arxiv:2610.08048` | DAEDALUS: Bootstrapping Agent Memory from Self-Generated Tasks | 反复验证并保留启发式记忆，不等于反馈改写记忆管理代码或独立策略文件。 |
| `arxiv:2610.08993` | Verify Less, Evolve More: Training Idea-Level Critics for Verification-Efficient ML Evolving Agents | 主要通过 SFT 和 GRPO 训练想法评论模型；即使评论器用于环内，也仍是模型权重。 |
| `arxiv:2610.09218` | RLDISCOVER: LLM-driven co-evolution of reinforcement learning algorithms | 演化的是被研究的深度 RL 算法，供后续模型训练使用；不是研究 Agent 的执行 Harness。 |
| `arxiv:2610.09563` | EvoSignal: LLM-Guided Evolutionary Design of Modular Traffic Signal Control Programs | 反馈优化交通信号控制程序，部署后无需在线 LLM；这是外部控制软件。 |
| `arxiv:2610.09832` | SkillForge: Co-Evolving Skills and Agents via Dynamic Skill Lifecycles | 方法中心是冷启动 SFT 和逐轮 agentic RL，与文本技能库生命周期协同；不能因有技能变异就忽略权重主训练对象。 |
| `arxiv:2610.10129` | When Algorithmic Exploration Becomes Cheap: A Case Study of Agentic Research in EDA | EDA 算法探索与研究产出案例，不是 Agent Harness 反馈演化方法或专项评测。 |
| `arxiv:2610.11152` | Do LLMs Learn from Rewards in Context? : Rethinking the role of reward in In-Context RL | 研究原始轨迹和奖励直接进入上下文的效果；不是改写外部 Harness 工件的评测。 |
| `arxiv:2610.11354` | AdaptEvo: Learning under Imperfect Supervision through Confidence-Adaptive Training with Knowledge Evolution | CA-GRPO 训练策略并更新训练知识/奖励量规；模型参数仍是主要训练对象。 |
| `arxiv:2610.12002` | Agentic-TTT: Training test-time policy for test-time training | 管理 TTT 的策略由训练产生，目标也是模型参数适应；不能把学出的策略视为外部 Harness。 |
| `arxiv:2610.12374` | AgentGarten: Code Worlds for Evolving Agents | 主要贡献是可扩展训练世界与神经渲染，继承的是经验 Playbook；未证实 Harness 管理机制演化。 |
| `arxiv:2610.12602` | Self-Preservation in Language Models | 生成与选择 replay 数据以保护持续训练的模型能力，主要对象为权重。 |
| `arxiv:2610.12789` | EvoBelief: Falsifiable World Models for Self-Improving LLM Agents | 明确改进可验证环境知识/世界规则，属于世界模型内容演化。 |
| `arxiv:2610.14024` | Beyond a Better Score: Long-Horizon Agentic ML Development and Evaluation Protocol for Physics Time Series | 科学时序模型是研究产物；合约、评测协议和能力组合是设计好的研究框架。 |
| `arxiv:2610.14163` | AutoEnvScaling: Automating the Data Flywheel with Terminal Agents | 演化训练环境并训练求解模型，属于数据/任务与权重 RSI。 |
| `arxiv:2610.14625` | From Existing Methods to New Research Ideas: Two Perspectives on Recursive Self-Improvement | 统一讨论参数、记忆、技能、代码等 RSI 设计空间，不是 Harness 专项综述。 |
| `arxiv:2610.15492` | When Skills Remain But Access Fails: Factorized Skill Memory for Continual Skill Internalization | 所谓技能记忆是训练后冻结的 LoRA 执行器和地址模型，实质为参数化技能。 |
| `arxiv:2610.16078` | Heterogeneous Agentic Coevolution | 确有反馈选择交互 Harness，但主要研究对象是 specialist 与 Agent 的互相训练；按协同更新边界，不让辅助 Harness 搜索取代模型/AI4AI 主类。 |
| `arxiv:2610.16812` | DASS: A Solver-Adaptable Dynamic Auxiliary Search Strategy for Symbolic Regression | 更新符号回归的基函数集合与统计搜索子空间，并非改写 Agent 的 Harness。 |
| `arxiv:2610.17804` | Learning from fracture: Teaching language models to design through physical experience | 从物理仿真归纳设计知识并生成材料结构，未改写 Agent 的工具/控制机制。 |
| `arxiv:2610.18427` | Reliable Memory from Unstable Growth: Curating Self-Written Agent Playbooks with Randomized Experiments | RBC 随机实验筛选经验 lesson block；变化的是记忆条目而非其管理机制。 |
| `arxiv:2610.20560` | PhySGA: A Physics-Space Grounded Agentic Framework for Generalizable and Interactive 3D Composition | §3.4 的 skill library 实际检索参考知识并蒸馏规划/诊断经验；Action Router 是固定模块，未写成被反馈改写的工具代码。 |
| `arxiv:2610.20673` | HPCAgent-Bench: A Framework for Sound Benchmarking of Code-Optimizing Agents, Harnesses, and Skills | 比较固定工具/技能干预下内核优化表现，未专项评测 Harness 工件的反馈演化。 |
| `arxiv:2610.22029` | Selection Is Not Learning: Choosing Model Futures | 选择和继承训练后的模型检查点，属于模型权重自改进。 |
| `arxiv:2610.22603` | At the Limits of Computability: Steps Towards Autonomous AI Discovery on the Busy Beaver Frontier | 主要生成并证明 Busy Beaver 数学加速规律；没有 Harness 自修改证据。 |
| `arxiv:2610.22915` | Reward Engine: Reward-Centric Self-Evolution for Open-Ended Tool Agents | 冻结任务 RewardPack 后反复修订任务输出；摘要没有跨任务保留修改后的 Harness。 |
| `arxiv:2610.24355` | Koi: Evidence-Guided, Self-Calibrating Planning for Multi-Cloud, Heterogeneous LLM Inference Fleets | 固定因果图的作用关系被校准，持久化的是部署证据 Playbook；没有控制程序演化证据。 |
| `arxiv:2610.25374` | Mining the Self-Rewriting System: A Vision for Data Mining on AI-Native Infrastructure | 讨论 AI 原生基础设施多表面内生漂移，范围涵盖模型/数据/检索，非 Harness 专项理论。 |
| `arxiv:2610.27714` | When Does Experience Memory Help Closed-Loop LLM Driving Agents? A Controlled Evaluation with Resampled Warmup Pools, Token-Matched Fillers, and Audited Baselines | 控制实验检验经验记忆和注入 token 的效应，非 Harness 工件演化专项。 |
| `arxiv:2610.28706` | SpecEvo: Speculative Evolution with Large Language Models for Cost-Efficient Scientific Discovery | 演化科研候选程序并积累检索指导，协调工作流是固定设计，未证实其自修改。 |
| `arxiv:2610.29588` | SatCraft: Agentic Optimization of Scheduling Policies for Satellite-Cellular Edge Services | 修改并保留网络服务调度代码，属于外部领域控制程序，不是 Agent Harness。 |
| `arxiv:2610.30114` | The End of Consensus Research? | AI-greement 用固定知识库/实现骨架/验证框架发现共识协议，更新对象是外部协议。 |
| `arxiv:2610.30277` | Breaking the high-degree barrier in Lehmer's problem with a human-AI discovery loop | 人机循环产生数学构造及多项式结果；没有反馈保留 Agent Harness 版本的研究。 |
| `arxiv:2610.31352` | Automating quantum circuit optimization with AI agents | 固定评估器与精确验证器下优化量子程序；主要产物是量子编译方案。 |
| `arxiv:2610.32433` | Tempo-Zero: Recursive Self-Play in Executable Worlds for Video Reasoning | 同一策略经执行奖励训练并演化环境课程，主对象是模型和训练环境。 |
| `arxiv:2610.33029` | Lessons from Luck: Do LLM-Written Lessons Carry Chance into an Agent's Next Decision? | 研究单条经验 lesson 将偶然结果传递给后续决策；不是 Harness 工件演化专项。 |
| `arxiv:2610.35453` | Beyond Federated Learning: Decentralized Agentic Systems for Self-Evolving Clinical Intelligence | 医疗多 Agent 分享经验记录的愿景；没有明确 Harness 程序工件反馈改写。 |
| `s2:42b2763a33cead6a99c3a1173c1fc928b199a012` | Agent-optimized GPU polygenic scoring at cohort scale | bioRxiv 官方摘要确认 Agent 优化 GPU 多基因评分程序；修改对象是外部科学计算软件，不是 Agent Harness。 |
| `s2:e3eade0509012afa038f6fa8b8e77e9e2c03d1ce` | Large language models discover complementary heuristics for combinatorial optimization | Nature 官方摘要确认演化组合优化问题的启发式算法组合；这些是任务求解产物，不是调用 LLM 的 Agent Harness。 |

## 数据差异：只报告，未修改

13 条 canonical 的 updated/version 落后于已存官方 Atom；首发日均不因此改动：

| ID | canonical updated / version | 官方 updated / version |
| --- | --- | --- |
| `arxiv:2609.36675` | 2026-09-29 / 1 | 2026-10-13T03:00:01Z / 2 |
| `arxiv:2609.37002` | 2026-09-29 / 1 | 2026-09-30T11:24:23Z / 2 |
| `arxiv:2609.38662` | 2026-09-29 / 1 | 2026-10-22T13:45:52Z / 3 |
| `arxiv:2609.39022` | 2026-09-30 / 1 | 2026-10-07T05:03:31Z / 3 |
| `arxiv:2609.40258` | 2026-09-30 / 1 | 2026-10-10T12:02:57Z / 2 |
| `arxiv:2610.04008` | 2026-10-02 / 1 | 2026-10-09T20:00:53Z / 2 |
| `arxiv:2610.09563` | 2026-10-07 / 1 | 2026-10-11T08:28:40Z / 2 |
| `arxiv:2610.09832` | 2026-10-07 / 1 | 2026-10-14T04:01:48Z / 2 |
| `arxiv:2610.11152` | 2026-10-08 / 1 | 2026-10-14T08:09:07Z / 3 |
| `arxiv:2610.11354` | 2026-10-08 / 1 | 2026-10-15T08:10:11Z / 3 |
| `arxiv:2610.12374` | 2026-10-08 / 1 | 2026-10-10T08:16:13Z / 2 |
| `arxiv:2610.17130` | 2026-10-12 / 1 | 2026-10-14T04:54:13Z / 2 |
| `arxiv:2610.22603` | 2026-10-15 / 1 | 2026-10-19T11:28:50Z / 2 |

5 条摘要逐字差异均为排版：

- `arxiv:2610.02945`：LaTeX 与 Unicode Erdős 排版差异。
- `arxiv:2610.08048`：LaTeX \tau 与 Unicode τ 排版差异。
- `arxiv:2610.09832`：agents 后的空格排版差异。
- `arxiv:2610.30114`：引号周边空格排版差异。
- `arxiv:2610.30277`：LaTeX \alpha 与 Unicode α 排版差异。

IEEE 的 Crossref 只有 2026-10；canonical 的 2026-10-01 精确日期尚未核定。没有把月份默认为已核实的某一天。

## 文件与校验

- `findings.json`：82 条逐篇建议、canonical source hash、身份/日期差异、来源 URL/路径/SHA、逐字引句。
- `validation.json`：逐条校验结果。
- `FROZEN.sha256`：冻结文件摘要。
- 原始快照和提取器位于 `build/maintenance-2026-11-02/primary-b/`。
- 重验命令：`python3 build/maintenance-2026-11-02/primary-b/validate_findings.py`。

冻结 SHA256：`ce2546b0c35b6f43e957fb5f9985d5272ddb230916e6ebd56572edef23f4a850`。

本组没有修改 canonical、生产审核单、日报、网站或发布状态，没有执行 git 命令或收费模型调用。
