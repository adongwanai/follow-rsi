# 2026-10-28 HF 昨日积压：第一轮独立审查

**50 篇全量摘要审读：1 篇 Harness 候选、2 篇边界待核、7 篇其他方向、40 篇排除。**

**这是 10-28 的积压审核，不能混入 10-29 当日推荐。全部仅为自动建议，decision 维持 defer；全文审读 0 篇。**

## 优先交叉复审

| 条目 | 建议 | 需要下一轮核实 |
| --- | --- | --- |
| The Trinity · 2610.36077 | Harness / evolve_main | 能力模块格式、验证准入与留出/预算证据 |
| Your Policy Is Secretly a Harness · 2610.37255 | 理论边界候选 | 是否真正研究反馈驱动自演化，否则应为一般 Harness 背景 |
| AdaPRA · 2610.33245 | borderline / component / in_loop_verifier | rubric 是否是被反馈修订、接受并保留的跨任务工件 |

## 全量逐篇判断

| # | 论文 | 首次发表 | 最新版本 | 建议 | 简短理由 |
| --- | --- | --- | --- | --- | --- |
| 1 | [The Trinity:Capability-Driven Recursive Self-Improvement for Multimodal Agents](https://arxiv.org/abs/2610.36077v1) | 2026-10-26 | 2026-10-26 | Harness 候选 | 验证后累积并继承可复用能力模块，明确构成外部 Harness 的迭代演化。 |
| 2 | [Multiscale Policy Optimization for Long-Horizon LLM Agents](https://arxiv.org/abs/2610.35013v1) | 2026-10-26 | 2026-10-26 | 排除 | MPO 改的是 RL 优势估计与模型策略更新，不是外部 Harness 工件。 |
| 3 | [ChronoReplay: One Answer Interface Is Not Enough for Streaming Spatial Intelligence](https://arxiv.org/abs/2610.34283v1) | 2026-10-25 | 2026-10-25 | 排除 | ChronoReplay 改空间 VLM 的监督训练；固定推理阶段选帧不等于程序自演化。 |
| 4 | [VibeVideoBench: Evaluating Multimodal Agents on Code-Driven Video Generation](https://arxiv.org/abs/2610.35864v2) | 2026-10-26 | 2026-10-27 | 排除 | 评测 Agent 写视频代码的任务能力；任务产物的渲染流水线不是 Agent 自己的 Harness 演化。 |
| 5 | [Memory Tax: Dissecting the Net Value of Agent Memory](https://arxiv.org/abs/2610.34073v1) | 2026-10-25 | 2026-10-25 | 排除 | 比较固定记忆系统与 RAG 的净价值，没有专门评估反馈驱动的 Harness 版本演化。 |
| 6 | [PDRVLA: A Vision-Language-Action Model with Physical Dynamics Representations](https://arxiv.org/abs/2610.37381v1) | 2026-10-27 | 2026-10-27 | 排除 | PDRVLA 训练物理表征与动作模型；冻结辅助世界模型不代表 Harness 自修改。 |
| 7 | [Can Test-Time Memory Evolution Outperform Test-Time Training for Scientific Discovery?](https://arxiv.org/abs/2610.32046v1) | 2026-10-23 | 2026-10-23 | 其他方向 | TTME 迭代蒸馏并复用科研经验记忆；摘要未说修改记忆管理代码或策略文件。 |
| 8 | [Hy-Nomas: Towards Free-form Interactive World Generation](https://arxiv.org/abs/2610.36729v1) | 2026-10-27 | 2026-10-27 | 排除 | 交互视频世界生成模型的多阶段训练与缓存历史，不是 Agent 的递归程序改进。 |
| 9 | [Can Discrete Tokens Serve as Semantically Lossless Representations of Visual Signals?](https://arxiv.org/abs/2610.37662v1) | 2026-10-27 | 2026-10-27 | 排除 | 研究离散视觉表征和量化器，未研究 RSI。 |
| 10 | [HABIT-Bench: Evaluating Habit Induction from Longitudinal Weak Evidence in Agent Memory](https://arxiv.org/abs/2610.24520v2) | 2026-10-17 | 2026-10-20 | 排除 | 评测从长期对话推断用户习惯，改的是可检索记忆数据，未评测 Harness 演化。 |
| 11 | [Rollback: Experience Backtracking in World Models for Policy Improvement](https://arxiv.org/abs/2610.36068v1) | 2026-10-26 | 2026-10-26 | 其他方向 | 真实经验更新世界模型 LoRA，再改善机器人策略；这是模型/具身闭环，非外部程序改写。 |
| 12 | [ThinkWorld: World Imagination Reinforces Chain-of-Dynamics Reasoning](https://arxiv.org/abs/2610.37666v1) | 2026-10-27 | 2026-10-27 | 排除 | ThinkWorld 用世界想象和 RL 训练动作表征，没有外部可复用程序版本演化。 |
| 13 | [CodeCap-Bench: Can Code Serve as a Good Video Caption?](https://arxiv.org/abs/2610.37341v1) | 2026-10-27 | 2026-10-27 | 排除 | 代码作为视频描述是任务输出；基准不评测 Agent 自己的 Harness 改进。 |
| 14 | [LociArt: A Unified Paradigm for Free-Style Local Video Stylization](https://arxiv.org/abs/2610.36456v1) | 2026-10-27 | 2026-10-27 | 排除 | 局部视频风格化模型、数据集和评测，与 RSI 无关。 |
| 15 | [Zooming without Zooming v2: From Seeing Details to Connecting Evidence for Generalizable Multimodal Perception](https://arxiv.org/abs/2610.37037v1) | 2026-10-27 | 2026-10-27 | 排除 | 固定数据合成与质检流程后用 RLVR 训练 VLM；未出现 Agent 迭代修改 Harness。 |
| 16 | [RSI Arena: Towards Recursive Self-Improvement with Human Feedback](https://arxiv.org/abs/2610.33624v1) | 2026-10-24 | 2026-10-24 | 其他方向 | 训练 Agent 依据人类投票继续训练模型，主要改进对象为模型研发和权重。 |
| 17 | [EmbeddingGemma 2: Unified and Efficient Multimodal Representations](https://arxiv.org/abs/2610.37364v1) | 2026-10-27 | 2026-10-27 | 排除 | 多模态嵌入模型与训练课程，不是 RSI。 |
| 18 | [MatAnyone-E: Sparse Memory Propagation for Efficient High-Resolution Video Matting](https://arxiv.org/abs/2610.35724v1) | 2026-10-26 | 2026-10-26 | 排除 | 视频抠像中的特征记忆检索和固定稀疏计算，不是 Agent 记忆机制自演化。 |
| 19 | [h1: A Taste of the Bitter Lesson in Automated Theorem Proving](https://arxiv.org/abs/2610.35962v1) | 2026-10-25 | 2026-10-25 | 排除 | h1 是固定 Lean 反馈接口；自反思推进当前证明，未把 Harness 修改保留给后续任务。 |
| 20 | [Omni-InteractScope: Benchmarking Proactive and Agentic Interaction in Continuous Omnimodal Streams](https://arxiv.org/abs/2610.35439v1) | 2026-10-26 | 2026-10-26 | 排除 | 评测连续音视频交互、工具调用与提醒能力，不是 Harness 演化专项评测。 |
| 21 | [Channel Selection for Mixture-of-Experts Decoding Needs No Calibration Data](https://arxiv.org/abs/2610.37386v1) | 2026-10-27 | 2026-10-27 | 排除 | 固定 MoE 通道选择、稀疏读取与解码加速，不涉及 RSI。 |
| 22 | [What Effort Level Should I Choose? On the Economics of Reasoning Effort in LLM Agents](https://arxiv.org/abs/2610.34491v1) | 2026-10-25 | 2026-10-25 | 排除 | 比较推理努力的成本与效果；失败后提升当前任务 effort 是固定策略，非跨任务程序更新。 |
| 23 | [On the SPOT: Enhancing Speculative Decoding for Diffusion Language Models via Commit-Order Prediction](https://arxiv.org/abs/2610.22543v2) | 2026-10-15 | 2026-10-26 | 排除 | 训练草拟模型并以固定规则验证候选 token；解码自校验不是 Harness 自进化。 |
| 24 | [Nemotron-Labs-Diffusion-Uni: Elastic Self-Refining Unified Diffusion LLM with Cross-Paradigm On-Policy Distillation](https://arxiv.org/abs/2610.36466v1) | 2026-10-27 | 2026-10-27 | 排除 | 蒸馏训练与单次推理内的 token 自细化，不是跨任务的 Harness 改进循环。 |
| 25 | [Cross-modal Steering Vectors Exist Across Both Image and Text Generation](https://arxiv.org/abs/2610.36269v1) | 2026-10-26 | 2026-10-26 | 排除 | 研究跨模态 steering vectors 的表征与控制；没有反馈驱动的程序版本更新。 |
| 26 | [The Lexical Imprint of Pre-training Data](https://arxiv.org/abs/2602.10657v2) | 2026-02-11 | 2026-10-26 | 排除 | 测量语料词汇对齐并用于固定文档选择/路由规则，没有递归改进机制。 |
| 27 | [RynnWorld-Latent: A Cross-Embodiment World Model Conditioned on Universal Latent Actions](https://arxiv.org/abs/2610.36791v1) | 2026-10-27 | 2026-10-27 | 排除 | 跨具身世界模型预训练与后训练、合成示范提升策略；无外部 Harness 自改写。 |
| 28 | [Benchmarking Obstacle-Conditioned Safety in Household Robot Navigation](https://arxiv.org/abs/2610.34674v1) | 2026-10-26 | 2026-10-26 | 排除 | 家庭机器人安全运动评测；人工加入参数推断步骤不是反馈驱动的程序演化。 |
| 29 | [Your Policy Is Secretly a Harness: The Decision Geometry of Agent Interfaces](https://arxiv.org/abs/2610.37255v1) | 2026-10-27 | 2026-10-27 | 边界待核 | 理论研究 Harness 更换与权重适配；尚未证明研究的是反馈驱动的 Harness 自演化。 |
| 30 | [SearchHorizonBench: A Benchmark for Search Value in AI Agents](https://arxiv.org/abs/2610.34714v1) | 2026-10-26 | 2026-10-26 | 排除 | 评测搜索价值估计与执行经验，不是外部 Harness 工件演化的专项评测。 |
| 31 | [Can LLMs Uncover Hidden Physical Laws through Free Exploration?](https://arxiv.org/abs/2610.37649v1) | 2026-10-27 | 2026-10-27 | 其他方向 | 探索记录驱动模拟场景演化；变化的是科研探索环境，非探索 Agent 自身的程序。 |
| 32 | [Timestral](https://arxiv.org/abs/2610.37585v1) | 2026-10-27 | 2026-10-27 | 排除 | 时间序列基础模型与预训练/后训练配方，不是 RSI。 |
| 33 | [OvisOCR3 Technical Report](https://arxiv.org/abs/2610.33066v1) | 2026-10-20 | 2026-10-20 | 排除 | OCR 模型多阶段训练、教师蒸馏和 RL；没有外部 Harness 或多代自改进的证据。 |
| 34 | [Harness-Model Collaboration for Long-Horizon Continual Learning](https://arxiv.org/abs/2610.34724v1) | 2026-10-26 | 2026-10-26 | 其他方向 | HaMo 积累策略经验卡并持续训练模型；没有修改记忆管理程序，不能归 Harness 协同演化。 |
| 35 | [Rare, Relevant, and Still Wrong: How Memory Fails LLM Group Decisions](https://arxiv.org/abs/2610.37624v1) | 2026-10-27 | 2026-10-27 | 排除 | 比较群体决策的固定记忆筛选规则；没有评测反馈更新程序的演化循环。 |
| 36 | [Vision-Language-Action or World-Action? Just Action Models](https://arxiv.org/abs/2610.37219v1) | 2026-10-27 | 2026-10-27 | 排除 | JAM 统一动作模型训练目标；未来监督提升策略，不是 Harness 改写。 |
| 37 | [Learning and Reasoning with Geometry: How Generation Helps Spatial Understanding](https://arxiv.org/abs/2610.36022v1) | 2026-10-26 | 2026-10-26 | 排除 | GeoUG 的证据生成决策通过 RL 训练；变的是模型权重，不是外部推理程序。 |
| 38 | [What Outcome RL Buys: Finishing, Reliability, Rarely Reach](https://arxiv.org/abs/2610.34894v1) | 2026-10-26 | 2026-10-26 | 排除 | 分析 outcome RL 的权重训练收益；不研究 Harness 演化。 |
| 39 | [How Much Does the Hint Matter? Scope Conditions for Hindsight Self-Distillation in Financial Reasoning](https://arxiv.org/abs/2610.36082v1) | 2026-10-26 | 2026-10-26 | 排除 | Fin-SD 用自评提示进行权重自蒸馏；摘要未建立多代闭环，也未演化外部程序。 |
| 40 | [MLE-World: Predicting Machine Learning Experiment Outcomes with a Learned World Model](https://arxiv.org/abs/2610.37175v1) | 2026-10-27 | 2026-10-27 | 其他方向 | MLE-World 帮科研 Agent 搜索更好的 ML 任务程序；被改进的是外部实验产物。 |
| 41 | [Sub-monolayer tracking of molecular states at buried interfaces](https://arxiv.org/abs/2610.31924v1) | 2026-10-22 | 2026-10-22 | 排除 | 分子界面的光学模型与实验解析，与 Agent RSI 无关。 |
| 42 | [Beyond the Estimate: Wiener-Informed Decoding for Easier Training of Pixel-Space Flow Models](https://arxiv.org/abs/2610.36192v1) | 2026-10-26 | 2026-10-26 | 排除 | 像素空间生成模型的统计初始化与联合训练，与 Harness 演化无关。 |
| 43 | [Self-Assessment Reinforcement Learning for Search-State Awareness in Retrieval-Augmented Large Language Models](https://arxiv.org/abs/2610.30435v1) | 2026-10-21 | 2026-10-21 | 排除 | SARL 用双奖励训练检索策略，摘要明确无推理阶段 scaffolding；不是 Harness 更新。 |
| 44 | [Quaternion Approximate Networks for Enhanced Image Classification and Oriented Object Detection](https://arxiv.org/abs/2509.05512v2) | 2025-09-05 | 2026-10-27 | 排除 | 四元数视觉网络及 CUDA 实现，不涉及 RSI。 |
| 45 | [AlphaBet: Reinforcement Learning for LLM Event Forecasting Agents](https://arxiv.org/abs/2610.22684v1) | 2026-10-15 | 2026-10-15 | 排除 | AlphaBet 用 GRPO 训练预测 Agent 权重，多预测日期不等于跨代 Harness 改进。 |
| 46 | [T-DIG: Text-Conditioned Diversity for Image Generation](https://arxiv.org/abs/2610.29003v1) | 2026-10-21 | 2026-10-21 | 排除 | T-DIG 虽冻结图像生成器，但主要训练产生提示的 LLM policy；外部提示不是被保留的程序版本。 |
| 47 | [Truncate or Not? A Scaling Study of Looped Transformers with Truncated Backpropagation](https://arxiv.org/abs/2610.26030v2) | 2026-10-19 | 2026-10-20 | 排除 | 循环 Transformer 的反向传播与缩放律，网络内部循环不是 Agent RSI。 |
| 48 | [PhysEvolve: Verifier-grounded Self-evolution for Physical Reasoning with Executable Worlds](https://arxiv.org/abs/2610.34921v1) | 2026-10-26 | 2026-10-26 | 其他方向 | 验证器反馈更新 GRPO 策略与物理课程；生成世界/训练任务属于数据与模型协同改进。 |
| 49 | [MoveBench: A Rubric-Based Benchmark for Evaluating Large Language Models in Sports and Health Coaching](https://arxiv.org/abs/2610.26185v2) | 2026-10-19 | 2026-10-26 | 排除 | 体育健康辅导能力与安全基准，不研究 Harness 演化。 |
| 50 | [AdaPRA: Process Reward Agents with Adaptive Rubrics for Data Science](https://arxiv.org/abs/2610.33245v1) | 2026-10-23 | 2026-10-23 | 边界待核 | 存在 rubric 适配和跨任务复用线索，但其反馈修订/接受与保留范围未写清。 |

## 候选与易误判条目的原文证据

### The Trinity:Capability-Driven Recursive Self-Improvement for Multimodal Agents

- ID：arxiv:2610.36077；建议：harness / harness / evolve_main。
- 对象：可复用能力模块与 Harness 树（control_flow）。
- 理由：正例依据是能力模块被持续演化、选择性继承，验证后的更新累积到后续迭代，且最终得到可路由的 Harness 树。不是因为标题含 Harness，也不是因为 Creator 生成训练世界。主对象记外部控制流/能力模块，子方向 evolve_main；世界生成是相邻的数据/任务方向，摘要未写权重更新，不归 coevolution。
- 对象原文：Explorer progressively evolves reusable capability modules through selective inheritance
- 反馈：yes；forming a Harness tree whose validated updates accumulate across iterations within a fixed topology.
- 保留/复用：yes；Explorer progressively evolves reusable capability modules through selective inheritance, forming a Harness tree whose validated updates accumulate across iterations within a fixed topology.
- 待核：仅读摘要，未审正文；模型是否完全冻结未知，但主要宣称的持久改进对象为外部能力模块。；具体模块工件格式、准入阈值、独立留出和预算公平性仍待正文核验。

### Can Test-Time Memory Evolution Outperform Test-Time Training for Scientific Discovery?

- ID：arxiv:2610.32046；建议：other_direction / experience_world_model / 无子方向。
- 对象：科研经验记忆条目（memory_entries）。
- 理由：摘要明确复用的是蒸馏经验得到的 external memory；没有说改写记忆管理代码、工具或可执行策略文件。科研发现产物与记忆数据不因测试时演化、冻结权重就变为 Harness。外部记忆如何由成功/失败反馈更新、更新在哪些跨任务范围保留仍需正文确认。
- 对象原文：TTME continually updates the external memory by distilling the experience to guide subsequent discovery without updating model weights.
- 反馈：unclear；未明，保留 unknown。
- 保留/复用：yes；TTME continually updates the external memory by distilling the experience to guide subsequent discovery without updating model weights.
- 待核：仅读原始摘要，未读全文；未陈述的机制保持未知。

### Rollback: Experience Backtracking in World Models for Policy Improvement

- ID：arxiv:2610.36068；建议：other_direction / embodied / 无子方向。
- 对象：世界模型 LoRA 与机器人策略（model_weights）。
- 理由：有真实反馈驱动的递归循环，但被改写的是世界模型/机器人策略权重。回滚和分支是固定训练系统提供的搜索操作，摘要没有系统改写自身的工具或工作流。
- 对象原文：real transitions from the policy it trains correct its dynamics through a lightweight LoRA pipeline.
- 反馈：yes；real-world experience continually sharpens the world model, and a sharper world model in turn drives further policy improvement.
- 保留/复用：yes；forming a self-reinforcing cycle: real-world experience continually sharpens the world model, and a sharper world model in turn drives further policy improvement.
- 待核：仅读原始摘要，未读全文；未陈述的机制保持未知。

### RSI Arena: Towards Recursive Self-Improvement with Human Feedback

- ID：arxiv:2610.33624；建议：other_direction / ai4ai / 无子方向。
- 对象：训练研发产出的模型权重（model_weights）。
- 理由：这是依据人类比较反馈继续训练前一阶段模型的自主研发研究；训练程序是完成模型研发任务的外部产物。摘要没有说训练 Agent 自身的 Harness 被反馈修订并保留，不能以自主写训练代码推为 Harness。
- 对象原文：independently selecting data, implementing training procedures, and choosing checkpoints.
- 反馈：yes；In Stage 2, each agent receives the comparison records and votes involving its Stage 1 model and is given three additional days for further training.
- 保留/复用：yes；we observe an improvement from Stage 1 to Stage 2 in the style-adjusted relative rating of eight of the ten models.
- 待核：仅读原始摘要，未读全文；未陈述的机制保持未知。

### Your Policy Is Secretly a Harness: The Decision Geometry of Agent Interfaces

- ID：arxiv:2610.37255；建议：borderline / theory_survey / 无子方向。
- 对象：研究 Harness 改动与策略失配（none）。
- 理由：论文确实专门研究外部 Harness 的更换、模型后训练与 ceiling/mismatch 归因，故值得作为 Harness 理论候选继续读正文。但摘要中的 Harness 修订是研究背景，实验比较改动和再训练并没有明确建立反馈驱动的自主工件演化。不能当方法正例；是否满足 harness_eval 的自演化专项范围尚不确定。
- 对象原文：Language model agents are post-trained and deployed through a harness, the prompts, tools, and control logic that present a task to the model and execute its outputs.
- 反馈：unclear；未明，保留 unknown。
- 保留/复用：unclear；未明，保留 unknown。
- 待核：仅读摘要，未审正文。；须检查理论与实验是否直接覆盖递归/反馈驱动 Harness 更新；否则应归一般 Harness 工程背景。；不能把模型在新 Harness 下继续训练等同外部工件也被持续演化。

### Can LLMs Uncover Hidden Physical Laws through Free Exploration?

- ID：arxiv:2610.37649；建议：other_direction / data_task / 无子方向。
- 对象：供科研探索的模拟世界与场景（training_env_reward）。
- 理由：明确有探索记录推动下一轮场景演化，但被演化对象是探索环境；探索者生成工具用于研究物理问题，摘要未证明工具成为 Agent 自身跨任务复用的演化工件。主方向建议 data_task，科研探索可作 ai4ai 次方向。
- 对象原文：These records guide scene evolution for further exploration, allowing the full cycle to run without human intervention.
- 反馈：yes；These records guide scene evolution for further exploration, allowing the full cycle to run without human intervention.
- 保留/复用：yes；These records guide scene evolution for further exploration, allowing the full cycle to run without human intervention.
- 待核：仅读原始摘要，未读全文；未陈述的机制保持未知。

### Harness-Model Collaboration for Long-Horizon Continual Learning

- ID：arxiv:2610.34724；建议：other_direction / model_weights / 无子方向。
- 对象：策略经验卡与模型权重（model_weights）。
- 理由：快路径变化是经验卡数据，慢路径变化是模型的 continual learning 权重。摘要没有记忆管理程序、工具代码或技能文件作为独立工件被反馈修订，因此不符合外部 Harness 与模型双更新的 coevolution 判据。策略级经验文字不能自动当可执行技能文件。
- 对象原文：HaMo distills trajectories into strategy-level experience cards for immediate retrieval
- 反馈：unclear；未明，保留 unknown。
- 保留/复用：yes；jointly preserving procedural experience and internalizing the competence to transfer and execute it across tasks.
- 待核：仅读摘要，未审正文；训练与经验更新的具体多轮安排仍需全文核验。；experience cards 的数据/程序属性要以实际格式确认，当前摘要仅支持可检索经验。

### MLE-World: Predicting Machine Learning Experiment Outcomes with a Learned World Model

- ID：arxiv:2610.37175；建议：other_direction / ai4ai / 无子方向。
- 对象：外部 ML 任务候选程序（external_artifact）。
- 理由：世界模型预测外部候选程序的报错和得分，固定搜索策略据此比较或修改程序；研究的是用较少真实实验找到更好 ML 解，不是改 Agent 自己的 Harness。科研方向建议与是否构成跨任务递归自改进分开；摘要未证明后者。
- 对象原文：AI research agents can propose, execute, and improve programs that solve machine learning tasks.
- 反馈：yes；compare several candidates per step by their predicted outputs: Sequential revision, Best-of-N, Pairwise judging, Fusion, and a UCB style rule
- 保留/复用：unclear；未明，保留 unknown。
- 待核：仅读摘要，未审正文；跨任务持续自改进未由摘要证明，不因科研 Agent 搜索就自动接收为广义 RSI。

### PhysEvolve: Verifier-grounded Self-evolution for Physical Reasoning with Executable Worlds

- ID：arxiv:2610.34921；建议：other_direction / data_task / 无子方向。
- 对象：模拟训练任务/课程与 VLM 策略（training_env_reward）。
- 理由：世界程序是训练环境，模拟器生成训练题，验证器反馈更新模型权重和课程。不是改 Agent 控制流/工具库；不能因为 executable worlds、verifier 或 self-evolving 字样纳入 Harness。
- 对象原文：At each round, a shared VLM proposes executable world programs and evidence schemas
- 反馈：yes；Exact verifier feedback from task solving updates both the shared policy via GRPO and an adaptive curriculum over physical intents.
- 保留/复用：yes；Exact verifier feedback from task solving updates both the shared policy via GRPO and an adaptive curriculum over physical intents.
- 待核：仅读摘要，未审正文。；HF 摘要中方法名称位置出现空白（We introduce , / Starting ... , achieves），须对照正文；不补造原文。

### AdaPRA: Process Reward Agents with Adaptive Rubrics for Data Science

- ID：arxiv:2610.33245；建议：borderline / harness / component。
- 对象：候选：环内过程监督 rubric（in_loop_verifier）。
- 理由：有可成为 Harness 工件的过程监督 rubric，且有从容易任务 seed 到困难任务、跨模型监督的线索。但摘要未说明执行反馈如何修订/接受 rubric 新版本，以及适配后的版本是否继承到后续任务。明确的 persistent knowledge 仅是同一任务的跨尝试状态。保留 borderline，建议 component / in_loop_verifier，不能靠 persistent harness 标题措辞通过。
- 对象原文：Our process reward agent audits the agent's trajectory and workspace by executing checks, and adapts its rubrics to each task.
- 反馈：unclear；Our process reward agent audits the agent's trajectory and workspace by executing checks, and adapts its rubrics to each task.
- 保留/复用：unclear；We find that rubrics seeded from easier tasks generalize to harder tasks, with rubric adaptation further improving performance.
- 待核：仅读摘要，未审正文。；需确认 rubric 是可执行/可复用的监督策略工件，还是当前任务临时检查表。；需确认修改由执行反馈驱动，且接受后的新 rubric 版本带到后续任务或改进轮次。；跨任务 generalize 与跨模型监督是复用线索，仍不能替代版本保留及接受机制的直接证据。

## 日期核验与限制

全部 50 个标题与 arXiv API 一致；全部 HF submittedOnDailyAt 为 10-28；无重复 ID。下列 7 条 HF paper.publishedAt 不能直接当成首发日：

| ID | arXiv 首发 | arXiv 更新 | HF paper.publishedAt |
| --- | --- | --- | --- |
| arxiv:2610.35864 | 2026-10-26 | 2026-10-27 | 2026-10-27 |
| arxiv:2610.24520 | 2026-10-17 | 2026-10-20 | 2026-10-20 |
| arxiv:2610.22543 | 2026-10-15 | 2026-10-26 | 2026-10-26 |
| arxiv:2602.10657 | 2026-02-11 | 2026-10-26 | 2026-10-26 |
| arxiv:2509.05512 | 2025-09-05 | 2026-10-27 | 2026-10-27 |
| arxiv:2610.26030 | 2026-10-19 | 2026-10-20 | 2026-10-20 |
| arxiv:2610.26185 | 2026-10-19 | 2026-10-26 | 2026-10-26 |

仅写本报告及配套 JSON。没有修改主数据、队列或论文数字，没有调用付费 API，也没有 commit/push。
JSON 包含完整 arXiv 元数据、原始 HF 日期、全量摘要和引句，便于独立下一轮复核。
