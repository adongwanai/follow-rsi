# 独立来源与范围复核 · 2026-11-07

独立复核支持主审的当前发布范围结论：2 项可作为 Harness 候选，48 项不进入当前 Harness 专题。50 项原始 HF 摘要均已通读；对全部 3 个正例/首轮边界候选复读官方正文关键章节，并重点检查另外 16 项易混淆的排除项。没有逐项范围分歧。

这次审核仅完成来源、范围与两条无数字双语摘要的核验；没有应用正式决定、生成合并凭证或执行发布。论文实验未重跑。

## 可纳入候选

| 论文 | 保留的 HF 日 | 支持方向 | 结论 |
|---|---|---|---|
| PyRUA-REAL · 2611.06768 | 2026-11-05 | harness / component，secondary embodied | 执行反馈修订并保留可执行技能，原技能库用于后续任务。 |
| Harness-S · 2611.04277 | 2026-11-06 | harness / evolve_main | 按失败编辑外部组件，验证后跨代保留；policy training 期间池固定。 |

PyRUA-REAL 的数字需要额外证据：摘要 84.4%、引言 84.82%、结果与表格 84.42% 不一致；91.1% 是跨代码修订的开发成功率，不能写成统一冻结程序测试结果。主审拟用的不带数字摘要没有这个问题。论文也明确记录人工协助，不能写成完全无人干预。

Harness-S 的 profile re-anchoring 更新证据与分配，不等于训练期继续修改 Harness 实现。KernelSeek 的问题库由作者在实验后归纳，替代人类 questioner 的实验明确未开展；它保留 ai4ai/内核优化相关性，但不作为 Harness 演化正例。

## 来源核验

- HF 原始响应绑定：50/50 的 ID、title、summary、JSON pointer 和原始文件 SHA256 一致。11/05 原榜 39 项，11/06 原榜 31 项；本次增量是 46 个新身份和 4 个日期补记。
- 50/50 官方元数据的身份、标题、摘要、published 与 updated 已回到保存的 arXiv Atom XML 核对；4 项既有 first_seen 对照采集前 canonical 快照保持原值。
- 主审 64 条引句的位置、来源文件和已有哈希均核验通过；本报告另绑定 71 条引句并记录每条 quote_sha256。
- 三份正文 TXT 与相应 raw HTML article 文本在空白归一化后一致，HTML 与 TXT 分别保存哈希。
- 2611.06817 的 HF 名称 Open-HumanScale 与官方 v2 名称 Open-HumanWAM 不同，分别保留。另 5 项摘要差异是 TeX/数学符号形式，未改变范围结论。
- 11/07 请求当时返回 not_ready，不能写成空榜或全天无论文；所有历史补记仍属于 11/05、11/06。

## 逐项独立结论

下表 exclude 仅指当前 Harness 发布范围，不否定其他 RSI 方向。所有条目的正式 owner 决定均未由本报告应用。

| ID | HF 日 | 独立结论 | 范围建议 | 独立理由 |
|---|---|---|---|---|
| 2611.04408 | 2026-11-05 | supported | exclude (Harness scope) | 被控制的是光网络资源和故障响应；固定预测控制不建立 Agent 外部工件的反馈演化。 |
| 2611.06425 | 2026-11-05 | supported | exclude (Harness scope) | 摘要直接描述草稿模型训练及逐层裁剪，改进对象属于模型与推理实现。 |
| 2611.01926 | 2026-11-05 | supported | exclude (Harness scope) | 工具调用与潜在思维的交错接口服务当前推理；未给出接口工件版本演化。 |
| 2610.41432 | 2026-11-05 | supported | exclude (Harness scope) | HCU 的三种通道、AX 工具和补充技能是预设接口；技能存在本身不证明技能受反馈修订。 |
| 2611.06768 | 2026-11-05 | supported | include | 执行反馈驱动代码修订，研究员保留适用实现为新技能，旧 primitive 库用于新任务；支持 component 并交叉 embodied。 |
| 2611.05648 | 2026-11-05 | supported | exclude (Harness scope) | 修改的是扩散模型的对抗训练表征；文本流不是外部可编辑的 Harness 提示文件。 |
| 2611.03404 | 2026-11-05 | supported | exclude (Harness scope) | 教师学习、轨迹回归和学生蒸馏作用于配音模型，不是持久 Harness 工件。 |
| 2611.03330 | 2026-11-05 | supported | exclude (Harness scope) | 研究模型推理能耗的解析规律，属于一般推理分析，未专门评估 Harness 演化。 |
| 2611.03768 | 2026-11-05 | supported | exclude (Harness scope) | 跨层复用 token 选择并重叠执行是固定稀疏注意力优化；运行时缓存更新不等于工件演化。 |
| 2611.05988 | 2026-11-05 | supported | exclude (Harness scope) | 当前音视频流的滑窗、历史上下文及生成架构不构成跨任务可复用的反馈修改。 |
| 2610.36544 | 2026-11-05 | supported | exclude (Harness scope) | 研究固定 restart/continue 行动的决策价值与统计认证；属于一般 agent 监控分析。 |
| 2611.03517 | 2026-11-05 | supported | exclude (Harness scope) | 优化的可执行对象是 CUDA 任务内核；问题库来自事后人工归纳，自主替代人类尚未测试。 |
| 2611.03852 | 2026-11-05 | supported | exclude (Harness scope) | 实验改写当前推理历史后比较 continuation；未把压缩策略本身的跨任务更新作为研究对象。 |
| 2611.05593 | 2026-11-05 | supported | exclude (Harness scope) | 训练从高斯表示生成图像的 Transformer；研究对象是渲染器和其预测能力。 |
| 2611.04760 | 2026-11-05 | supported | exclude (Harness scope) | Koopman 表征、流匹配和不确定性门控构成预测模型，没有 Agent 工件改写。 |
| 2611.03394 | 2026-11-05 | supported | exclude (Harness scope) | 跨 chunk 保留音视频生成历史是运行状态；模型延续训练不是 Harness 文件更新。 |
| 2611.06042 | 2026-11-05 | supported | exclude (Harness scope) | 通过专家分组、模型容量和路由提升图像修复；非 Agent 外部程序的自修改。 |
| 2611.04949 | 2026-11-05 | supported | exclude (Harness scope) | RAG 伪标签用于翻译领域适配；自生成数据不自动等同于 Harness 演化。 |
| 2611.05029 | 2026-11-05 | supported | exclude (Harness scope) | 跨任务累积的是张量重要性并调节 AdamW 学习率；即使持续学习也属于模型训练对象。 |
| 2611.08449 | 2026-11-06 | supported | exclude (Harness scope) | 视觉 primitive 草稿器通过标注训练并按固定结构条件接受；属于视觉规划模型。 |
| 2611.04277 | 2026-11-06 | supported | include | 失败根因驱动多个外部组件编辑，实测和验证覆盖选择父代并保留有效变体；后续训练池固定。 |
| 2611.00883 | 2026-11-06 | supported | exclude (Harness scope) | 压缩普通模型基准、估计误差并控制高误差风险；不是 Harness 演化专项基准。 |
| 2611.08373 | 2026-11-06 | supported | exclude (Harness scope) | 空间对齐与持续预训练更新 VLA 权重，辅助组件明确只在训练使用。 |
| 2611.07392 | 2026-11-06 | supported | exclude (Harness scope) | 摘要含评估驱动数据迭代，但对象是图像模型和数据引擎；没有外部 Harness 工件演化证据。 |
| 2611.06741 | 2026-11-06 | supported | exclude (Harness scope) | 自有 rollout 监督去噪修正，属于模型的 final-stage training；跨图像轮次效果不改变对象类别。 |
| 2611.03743 | 2026-11-06 | supported | exclude (Harness scope) | RL 将记忆使用经验内化为 policy，并生成当前请求的 reasoning state；不是改写管理代码。 |
| 2611.07854 | 2026-11-06 | supported | exclude (Harness scope) | 非自回归决策模型通过 SFT/RL 训练，产物是模型权重而非版本化 Harness 工件。 |
| 2611.04894 | 2026-11-06 | supported | exclude (Harness scope) | 固定视觉搜索基准评估当前任务的证据组织与检索能力，不专项考察持久 Harness 改写。 |
| 2611.06817 | 2026-11-06 | supported | exclude (Harness scope) | 机器人数据扩展、预训练和不更新权重的 in-context 适应均非外部 Harness 修订。 |
| 2611.06976 | 2026-11-06 | supported | exclude (Harness scope) | 任务奖励训练连接冻结模型的线性桥；桥的可训练参数属于模型适配。 |
| 2611.07909 | 2026-11-06 | supported | exclude (Harness scope) | 优化的保留产物是单一高斯头像；任务对象变好不是 Agent 自身 Harness 变好。 |
| 2611.02660 | 2026-11-06 | supported | exclude (Harness scope) | 跨 episode 保存的是事件与任务历史；跨任务边界的上下文持久化不能替代程序修订证据。 |
| 2611.04527 | 2026-11-06 | supported | exclude (Harness scope) | 固定教师的表征蒸馏与动作模块训练提升机器人策略，改进对象是模型。 |
| 2611.08237 | 2026-11-06 | supported | exclude (Harness scope) | 静态数学建模任务与程序/Lean 验证器评测答案；验证器存在不代表验证器演化。 |
| 2611.08376 | 2026-11-06 | supported | exclude (Harness scope) | 设计线性注意力门控、读出并训练模型；内部 KV 状态不是外部 Harness。 |
| 2611.08089 | 2026-11-06 | supported | exclude (Harness scope) | SAE 用于解释 MoE 专家功能，研究主题是模型机制解释。 |
| 2611.05376 | 2026-11-06 | supported | exclude (Harness scope) | 提出长期认知共生范式，讨论个性化和治理；未专门研究反馈修改 Harness 的机制。 |
| 2611.06982 | 2026-11-06 | supported | exclude (Harness scope) | 固定推测监听算法维护跨 chunk 草稿池并验证，属于当前推理状态和调度。 |
| 2611.04386 | 2026-11-06 | supported | exclude (Harness scope) | 冻结教师监督学生自有 rollout 的蒸馏过程，改变的是扩散模型参数。 |
| 2611.08483 | 2026-11-06 | supported | exclude (Harness scope) | 根据分数迭代并组合科学问题的候选程序，是 ai4ai 的外部成果演化；不进入当前 Harness 专题。 |
| 2610.37739 | 2026-11-06 | supported | exclude (Harness scope) | 研究科学问题和形式证明的再发现，不要求系统在任务间改写自身 Harness。 |
| 2609.37820 | 2026-11-06 | supported | exclude (Harness scope) | LLM 向量用于企业竞争与投资调整的经济分析，非代理系统自改进。 |
| 2611.07298 | 2026-11-06 | supported | exclude (Harness scope) | DUMP 前缀是随对比损失训练的参数；不应当作自然语言提示文件自动编辑。 |
| 2611.07613 | 2026-11-06 | supported | exclude (Harness scope) | LiDAR token 剪枝合并与物理数据增强提升感知模型，非 Agent 自身工件演化。 |
| 2611.08369 | 2026-11-06 | supported | exclude (Harness scope) | 临床知识、纵向病例与诊疗路径推理的通用能力评测，非 Harness 自改进专项。 |
| 2610.41789 | 2026-11-06 | supported | exclude (Harness scope) | 困难样本条件下的注意力正则优化人脸识别模型，非外部工件更新。 |
| 2610.40119 | 2026-11-06 | supported | exclude (Harness scope) | 人脸数据生成与下游微调是数据/模型工作，没有 Harness 修订循环。 |
| 2611.02075 | 2026-11-06 | supported | exclude (Harness scope) | 固定预测器使用不断增加的历史证据；这支持经验条件预测，不支持外部管理工件修改。 |
| 2610.34074 | 2026-11-06 | supported | exclude (Harness scope) | 比较训练随机种子对应的越狱易感性，属于一般模型安全分析。 |
| 2611.06498 | 2026-11-06 | supported | exclude (Harness scope) | 固定知识包完整性验证规则与安全评估；没有反馈驱动验证器版本演化。 |

## 逐项可回验引句

以下引文来自原始 HF 摘要或已绑定官方 HTML 的正文 TXT；每条 SHA256 是引文 UTF-8 字节的哈希。完整文件哈希、JSON pointer、字符位置和日期见配套 JSON。

### 2611.04408 · Halley: A Predictive Control Plane for Optical AI Data Center Networks

结论：supported。HF 日：2026-11-05；原发表：2026-11-03T06:45:50Z；当前 v1 更新：2026-11-03T06:45:50Z。

- abstract_object：Halley gives each layer a predictive controller that defers to the deployed policy when unsure.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/3/paper/summary`；quote SHA256：`75636b7dd7c3f139293e03c532f0d7a42e09f49dc626730fdfdc43faef256113`。

### 2611.06425 · D3D: Decoupled Diffusion Drafting for Asynchronous Speculative Decoding

结论：supported。HF 日：2026-11-05；原发表：2026-11-04T12:27:58Z；当前 v1 更新：2026-11-04T12:27:58Z。

- abstract_object：D3D combines blockwise denoising with auxiliary autoregressive supervision to achieve long accepted prefixes without target hidden states.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/12/paper/summary`；quote SHA256：`5408c22da7ef396a26159bda1b83bd87661e6bc19858e2bf8b28e291b28f5c5e`。

### 2611.01926 · TAC-CoT: Tool-Empowered Implicit Chain-of-Thought via Interleaving Explicit Tokens

结论：supported。HF 日：2026-11-05；原发表：2026-11-01T14:05:15Z；当前 v1 更新：2026-11-01T14:05:15Z。

- abstract_object：This interleaved design enables agentic tool-use without verbalizing every intermediate reasoning step.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/14/paper/summary`；quote SHA256：`0a6dba6e66a6b9b5c34972ca5a1aa41fe31a6cda4bc7380dd99cfdca0ec7792f`。

### 2610.41432 · Hybrid Computer Use: A Unified Programmatic, Semantic, and Visual Interface for General Agents

结论：supported。HF 日：2026-11-05；原发表：2026-10-30T08:38:29Z；当前 v1 更新：2026-10-30T08:38:29Z。

- abstract_object：A supplementary HCU skill guides agents in selecting and coordinating channels to use the unified interface effectively.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/15/paper/summary`；quote SHA256：`4317db172ea9111d9c1c10a49261b3180db292df0e4f0a73b19025c662d0dd98`。

### 2611.06768 · PyRUA-REAL: Robot Exploration and Adaptive Learning through RSI in the Real World

结论：supported。HF 日：2026-11-05；原发表：2026-11-04T16:46:03Z；当前 v1 更新：2026-11-04T16:46:03Z。

- abstract_object：persistent memory and reusable executable skills that inform subsequent exploration and improvement
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/19/paper/summary`；quote SHA256：`b649328fd502f2b17e631f8f035ab7d4ef26cc0c639feedccf5b30a5b185bb2f`。
- feedback_and_model_boundary：With the underlying agent model parameters held fixed, the system develops task programs through code generation, testing, and feedback analysis.
  - 来源：`build/maintenance-2026-11-07/primary-review-sources/2611.06768v1.txt:398`；quote SHA256：`714ffd8c04424cec0ba09af4c2f369b6e9a44583dcbf25fa6311aef4f78645db`。
- retained_implementation：The researcher also decides which adapted implementations to retain as new skills and records their observed applicability and limitations.
  - 来源：`build/maintenance-2026-11-07/primary-review-sources/2611.06768v1.txt:466`；quote SHA256：`99b2fa852921e784d5bf45d0988cb3fa3552ed43d9692417302b46214cf45ed0`。
- cross_task：In a separate eight-task comparison, agents start new-task exploration with or without a primitive-skill library developed on earlier tasks.
  - 来源：`build/maintenance-2026-11-07/primary-review-sources/2611.06768v1.txt:714`；quote SHA256：`cd153ed0f2e0603bda646ef3c1c8a9416ce83f91b0a1bfbddf8b7c9b7cd37860`。
- development_metric：Recorded development success averages 91.1% across tasks. These rates aggregate attempts across code revisions; frozen-program performance is evaluated separately.
  - 来源：`build/maintenance-2026-11-07/primary-review-sources/2611.06768v1.txt:91`；quote SHA256：`5f74428d6c24dacf31a176ae6f0a91177abd044a503a94e2ebfc0d1f7672fb58`。
- numeric_conflict_introduction：Complementary evaluation on 42 RoboDojo tasks yields 84.82% success, averaged equally over five capability groups
  - 来源：`build/maintenance-2026-11-07/primary-review-sources/2611.06768v1.txt:91`；quote SHA256：`00aaf30253a0911f9007e4e3dca68618465432db89c85d04bb9e497b5a434827`。
- numeric_conflict_results：Across 42 RoboDojo tasks, PyRUA-REAL’s frozen programs achieve 84.42% capability-averaged success
  - 来源：`build/maintenance-2026-11-07/primary-review-sources/2611.06768v1.txt:651`；quote SHA256：`91bc32bc1cfd1b0e2530bcc98bd391a1e5b81a337a898fc418b2da779e1e60e1`。
- human_contribution：Human input also resolved an episode in which an agent repeatedly routed around a false contact detection.
  - 来源：`build/maintenance-2026-11-07/primary-review-sources/2611.06768v1.txt:745`；quote SHA256：`04607aae713d6c8788e9133298520abae44800169c5285823e8e9f6ce20f2e78`。

已核验中文摘要：执行反馈推动机器人技能代码修订与保留，既有技能库可用于新任务。
已核验英文摘要：Execution feedback revises reusable robot skills, and retained primitives support development on new tasks.

- supported：Harness component via retained executable robot primitives。

- supported：The supplied number-free Chinese and English draft summaries。

- needs_evidence：A single reconciled RoboDojo aggregate success figure。Abstract 84.4%; introduction 84.82%; results and table 84.42%. Avoid aggregate performance numbers in this publication.

- disagreed：91.1% is an independent frozen-program test result。Text calls it development success aggregated across code revisions.

- disagreed：Fully human-free skill acquisition。Paper explicitly documents human assistance.

### 2611.05648 · NitroFusion2: Bringing Adversarial Loss to the Text Stream of Multimodal Diffusion Transformers

结论：supported。HF 日：2026-11-05；原发表：2026-11-03T21:33:28Z；当前 v1 更新：2026-11-03T21:33:28Z。

- abstract_object：We introduce Text-Stream Adversarial Distillation (TSAD), which exploits intermediate text-token states as a new adversarial representation.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/22/paper/summary`；quote SHA256：`4631a8d1e1364dae25f2162588b960b5cf6c9b669baf3795d463c85016de731b`。

### 2611.03404 · VidDub: Replacement-Aware Distillation for Two-Step Video Dubbing

结论：supported。HF 日：2026-11-05；原发表：2026-11-02T16:33:09Z；当前 v1 更新：2026-11-02T16:33:09Z。

- abstract_object：Matched trajectory regression then transfers the teacher's CFG-guided trajectories to a two-step student, and distribution matching distillation recovers visual quality after step compression.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/23/paper/summary`；quote SHA256：`369fbc0aae6cfe1b10c9017304353113f780cc9b303ea352b873bcc135b32519`。

### 2611.03330 · The SIMPLE Law for Energy Cost of LLM Inference

结论：supported。HF 日：2026-11-05；原发表：2026-11-02T15:51:46Z；当前 v1 更新：2026-11-02T15:51:46Z。

- abstract_object：The SIMPLE law explains as well as predicts: prefill energy grows quadratically with the hidden dimension
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/25/paper/summary`；quote SHA256：`aab1a76ec39c2f888b04902fbaa78ed731fe45d556d16ca8f110fa1dd98f0958`。

### 2611.03768 · Multi-layer Indexer: Overlapping Selection and Attention in DeepSeek Sparse Attention

结论：supported。HF 日：2026-11-05；原发表：2026-11-02T15:46:01Z；当前 v1 更新：2026-11-02T15:46:01Z。

- abstract_object：The resulting Multi-layer Indexer (MLI) needs no retraining and no new weights.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/28/paper/summary`；quote SHA256：`059ecdf8ad5a817807fc916194b43881bb23be33e851a02c66decb4b877ec5af`。

### 2611.05988 · LiveFoley: Dynamic Real-Time Video-to-Audio Generation for Immersive Interactive Worlds

结论：supported。HF 日：2026-11-05；原发表：2026-11-04T05:35:42Z；当前 v1 更新：2026-11-04T05:35:42Z。

- abstract_object：History LocDiT adds past context to improve quality at no latency cost and serves as our default.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/29/paper/summary`；quote SHA256：`c78f83a4abf17cf32ba94c4d545a7f59568c3c8e5a96f33e1ebdab3bf2d95287`。

### 2610.36544 · Monitor Accuracy Isn't the Answer: A Decision-Value Framework for Evaluating AI Agent Restart Monitors

结论：supported。HF 日：2026-11-05；原发表：2026-10-27T02:59:21Z；当前 v1 更新：2026-10-27T02:59:21Z。

- abstract_object：These results motivate evaluating agent monitors through recovery opportunity, decision value, and statistical support, rather than classification performance alone.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/30/paper/summary`；quote SHA256：`b8806a6f3edb5bafd72cf696b064f71576030d873afebb3387d6308390a84c06`。

### 2611.03517 · Ask, Don't Equip: Question-Driven Coding Agents for Deep Kernel Optimization

结论：supported。HF 日：2026-11-05；原发表：2026-11-02T17:51:58Z；当前 v1 更新：2026-11-02T17:51:58Z。

- abstract_object：a question-driven agent that makes an existing CUDA kernel faster with no operator-specific knowledge and no faster implementation to imitate
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/31/paper/summary`；quote SHA256：`0863ecdaface213eacbdc7cdec0225683a5a4ee9ab2ddee26e3e947f780e41e2`。
- posthoc_bank：After the campaigns we distilled the recurring questions into a bank.
  - 来源：`build/maintenance-2026-11-07/primary-review-sources/2611.03517v1.txt:315`；quote SHA256：`351b7d332b9687816b24d765f5a008627a26a1c3deddc8a7d0e8ff36e2370a95`。
- reuse_not_evolution：The skill is parameterized by the seed, the scenario set, and the goal; its questions were reused across the Hopper and Blackwell campaigns nearly verbatim.
  - 来源：`build/maintenance-2026-11-07/primary-review-sources/2611.03517v1.txt:330`；quote SHA256：`6b19f83210ac749d76c2a6e9795e4463b4213a3059c72ed9f3fae4d087aaab48`。
- missing_comparison：Whether the bank can replace the human is the experiment this paper does not contain.
  - 来源：`build/maintenance-2026-11-07/primary-review-sources/2611.03517v1.txt:922`；quote SHA256：`1d8c94660f2348342f8c6cc8214e7bb952676127f5309c1a923d8f5e493f368b`。
- human_direction：The human did have systems expertise and used it to decide which measurement to demand and when; we claim only that the questions, once asked, are short, generic, and now written down.
  - 来源：`build/maintenance-2026-11-07/primary-review-sources/2611.03517v1.txt:922`；quote SHA256：`c17076b3f0204dfa2210415e7f49be16923c1731171926942f2e4e2ef3e9c1cf`。

- supported：Current Harness publication scope exclusion。

- needs_evidence：Autonomous feedback-driven evolution of the question bank。Post-hoc human distillation and reuse are documented; an autonomous update-and-retention loop is not established.

- disagreed：Bank replaces human questioner with demonstrated outcome。The comparison is explicitly described as an experiment the paper does not contain.

### 2611.03852 · Why Pay for Long Reasoning When Rewrite Do Trick? Causal Effects of Reasoning History Compaction on Future Generation and Agent Cost

结论：supported。HF 日：2026-11-05；原发表：2026-11-02T19:21:48Z；当前 v1 更新：2026-11-02T19:21:48Z。

- abstract_object：Our intervention rewrites prior reasoning into compact state records before pending tool results are revealed, then compares continuations from original and compact histories.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/32/paper/summary`；quote SHA256：`431799a97c40f3d2378f4a86496245277d2d61764111bdac5df3c0bfe038ed9f`。

### 2611.05593 · GaussianRenderFormer: Transformer-based Rendering of 3D Gaussian Splats

结论：supported。HF 日：2026-11-05；原发表：2026-11-03T20:26:14Z；当前 v1 更新：2026-11-03T20:26:14Z。

- abstract_object：We present GaussianRenderFormer, a transformer that takes a set of Gaussians and a camera and outputs the image directly.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/33/paper/summary`；quote SHA256：`a59d7bf0e0636e4389c8c2983a7148bdfee64fd771e7d297fc9d8da17690d557`。

### 2611.04760 · Koopman Generative Operators for Efficient Probabilistic Time-Series Forecasting

结论：supported。HF 日：2026-11-05；原发表：2026-11-03T12:08:37Z；当前 v1 更新：2026-11-03T12:08:37Z。

- abstract_object：We introduce the Koopman Generative Operator (KGO), a probabilistic forecasting method that conceptualizes prediction as the evolution of structured uncertainty.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/34/paper/summary`；quote SHA256：`a4b66c533f8c85281d754d584d7c537a172397f2046fae0905d1729a23216630`。

### 2611.03394 · TaoMate-HD: Progressive-Resolution Autoregressive Audio-Video Generation

结论：supported。HF 日：2026-11-05；原发表：2026-11-02T16:29:27Z；当前 v1 更新：2026-11-02T16:29:27Z。

- abstract_object：Across text updates, the model retains this history to infer what has already been spoken.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/35/paper/summary`；quote SHA256：`1c2f831e8f25ae9220216e6b628b145dac8951de2816dbc69c3f1200791230be`。

### 2611.06042 · UniRestorer++: Scalable Universal Image Restoration with Multi-Granularity Degradation Modeling

结论：supported。HF 日：2026-11-05；原发表：2026-11-04T06:46:47Z；当前 v1 更新：2026-11-04T06:46:47Z。

- abstract_object：It progressively refines degradation groups and introduces group-specific experts, coupling capacity growth with specialization.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/36/paper/summary`；quote SHA256：`906d02b07f5dd1de55e200886ef0479ea31508cc78e9aa3ba39466b6db2db46a`。

### 2611.04949 · HERIT: Enabling Global Access to Hanja-to-English Historical Translation by Mitigating Temporal Bias

结论：supported。HF 日：2026-11-05；原发表：2026-11-03T14:10:59Z；当前 v1 更新：2026-11-03T14:10:59Z。

- abstract_object：This approach substantially expands the training dataset, mitigating both data scarcity and temporal overfitting across different historical periods.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/37/paper/summary`；quote SHA256：`13f74afebc51406a1d9a610a017b8694afd7f4a782071c1e05f5564a1e69550e`。

### 2611.05029 · DRAP: Dynamics-Risk Adaptive Plasticity for Continual Learning in Physical AI

结论：supported。HF 日：2026-11-05；原发表：2026-11-03T15:05:06Z；当前 v1 更新：2026-11-03T15:05:06Z。

- abstract_object：After each task, risk-weighted squared gradients are accumulated in a tensor-level importance memory.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/38/paper/summary`；quote SHA256：`97fd02654db91e65d41d0d9788454d21605f0fb58cd511eac9de9f4583dd5dac`。

### 2611.08449 · VFlash: Fast, Accurate Visual Planning via Flash Primitive Decoding

结论：supported。HF 日：2026-11-06；原发表：2026-11-05T18:44:43Z；当前 v1 更新：2026-11-05T18:44:43Z。

- abstract_object：VFlash therefore trains on annotated primitives and directly accepts structurally valid predictions without target-token agreement.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/0/paper/summary`；quote SHA256：`b50c4152009e923fc2a7df0bb798b4916ff2163a0d9913b0d48231754db7903e`。

### 2611.04277 · Harness-S: Learning from Sibling Harnesses for Generalizable Agent Training

结论：supported。HF 日：2026-11-06；原发表：2026-11-03T04:03:44Z；当前 v1 更新：2026-11-03T04:03:44Z。

- abstract_object：Directional Harness Evolution develops specialized sibling harnesses along distinct repair directions, forming a reusable Sibling Harness Pool that remains fixed during policy training.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/1/paper/summary`；quote SHA256：`02540c6e563a023cbdfeb9cddac85cec71eb2cf6592e3016c0963bc07b9b4b37`。
- edit_object：edits can alter prompts, skills, context, memory, hooks, or the tool view.
  - 来源：`build/maintenance-2026-11-07/primary-review-sources/2611.04277v1.txt:3264`；quote SHA256：`b4143e5f8c38c316b239692afae883a139df7c5adcc6cdf6b9e4bf9e998d8892`。
- evaluation：Local evaluation tests whether an edit repairs the targeted failures while preserving behavior on successful controls.
  - 来源：`build/maintenance-2026-11-07/primary-review-sources/2611.04277v1.txt:3288`；quote SHA256：`7678d778e8795f9a1cc787972b4fb456b4f559bf2c7bd5b6e35b9f55d03e2cda`。
- retained_pool：The Sibling Harness Pool retains all valid children, including those not selected as parents:
  - 来源：`build/maintenance-2026-11-07/primary-review-sources/2611.04277v1.txt:697`；quote SHA256：`452ad751c4b543ecbc75d14284ea7ebc0b08c6f019ebdea5ce5d02ce59ad4665`。
- next_generation：Selected parents are paired with locally diagnosed root causes for the next round of editing, while the archive retains all executable, protocol-compliant variants.
  - 来源：`build/maintenance-2026-11-07/primary-review-sources/2611.04277v1.txt:3297`；quote SHA256：`0fce8202974117483557bd6a7f42cded9a8521c68311120c7d80c69f4a0d37cb`。
- fixed_during_training：The resulting implementations remain fixed during policy training; only their profiles and allocation are updated.
  - 来源：`build/maintenance-2026-11-07/primary-review-sources/2611.04277v1.txt:3297`；quote SHA256：`083f2c58d238a24a71c25c87f0401760a0c670590ec5e9bf448022772a15294e`。

已核验中文摘要：按失败原因编辑并保留多种Harness，再用固定变体池辅助策略训练。
已核验英文摘要：Failure-guided edits create a reusable harness pool, which stays fixed while supporting policy training.

- supported：Failure-guided external harness evolution with retained generations。

- supported：harness/evolve_main and the supplied bilingual summaries。

- disagreed：Harness implementations keep co-evolving online throughout policy training。Pool implementations stay fixed; only profiles and allocation update during policy training.

### 2611.00883 · Random Is Almost Enough? Stable and Low-Cost Benchmark Compression via BestRand

结论：supported。HF 日：2026-11-06；原发表：2026-10-31T12:36:58Z；当前 v1 更新：2026-10-31T12:36:58Z。

- abstract_object：Benchmark compression reduces the often prohibitive time and cost of model evaluation by evaluating models on a small benchmark subset that closely matches full-benchmark results.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/2/paper/summary`；quote SHA256：`b94948f7daca555d22fbabccc4ebd8538a107a8616a50b078fe944ed6dfcc099`。

### 2611.08373 · SLA: Scaling Spatial-Language-Action Model via Continual Pre-training

结论：supported。HF 日：2026-11-06；原发表：2026-11-05T17:52:16Z；当前 v1 更新：2026-11-05T17:52:16Z。

- abstract_object：All auxiliary components are used only during training, allowing direct reuse of pretrained VLA weights and preserving the original inference architecture.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/3/paper/summary`；quote SHA256：`ca0a329c6a2fe0b5e45a269340e4915f40e4d4f428e7411ba2550199b26c64bd`。

### 2611.07392 · WeLM-Image: A Unified Image Generation Model towards Visual Intelligence

结论：supported。HF 日：2026-11-06；原发表：2026-11-05T03:41:53Z；当前 v1 更新：2026-11-05T03:41:53Z。

- abstract_object：We optimize generation and editing separately with rubric- and checklist-based rewards, then consolidate the specialized policies through noise-aware on-policy distillation.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/4/paper/summary`；quote SHA256：`f1094485941c2b212118fac7177261289f6d033c586bcf1d4d3519012d91fbd6`。
- data_boundary：while training-time evaluation guides iterative data refinement.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/4/paper/summary`；quote SHA256：`dc871f15bc2ee781faf749b815159138334e1b4d964d17aa2550babdb7d81d62`。

### 2611.06741 · TailSteer: Trajectory-Tail Steering for Drift-Resistant Multi-turn Image Editing

结论：supported。HF 日：2026-11-06；原发表：2026-11-04T16:23:24Z；当前 v1 更新：2026-11-04T16:23:24Z。

- abstract_object：These corrections are learned from the editor's own on-policy denoising rollouts, using unchanged source content as a preservation reference without requiring curated ground-truth editing pairs.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/5/paper/summary`；quote SHA256：`86f44f878e8cd7a6762c818e6ddbb2ccc9cfb5452798ca61d60497c27314b317`。

### 2611.03743 · EvoMemState: Evolving Memory State for Personal Agents

结论：supported。HF 日：2026-11-06；原发表：2026-11-02T02:42:04Z；当前 v1 更新：2026-11-02T02:42:04Z。

- abstract_object：RL-Based State Evolution internalizes memory-use experience into a policy through reinforcement learning to generate a request-specific Reasoning State.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/6/paper/summary`；quote SHA256：`d1678b1f2a6180d2f6c8365282c57543579efe933eb2e906899e44032a2ce406`。
- object_boundary：RL-Based State Evolution internalizes memory-use experience into a policy through reinforcement learning to generate a request-specific Reasoning State.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/6/paper/summary`；quote SHA256：`d1678b1f2a6180d2f6c8365282c57543579efe933eb2e906899e44032a2ce406`。

### 2611.07854 · Towards Foundation Decision Models: Drex

结论：supported。HF 日：2026-11-06；原发表：2026-11-05T11:31:13Z；当前 v1 更新：2026-11-05T11:31:13Z。

- abstract_object：Training combines supervised fine-tuning with reinforcement learning from adjusted feedback (RLAF), plus vision tuning for Max.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/7/paper/summary`；quote SHA256：`64cc896bba5e674b5c682bb932f05da6fd63c771efa16af2d7bd14a24b402475`。

### 2611.04894 · VisSearch-Bench: Evaluating Long Horizon Visual Search in Multimodal Agents

结论：supported。HF 日：2026-11-06；原发表：2026-11-03T13:40:41Z；当前 v1 更新：2026-11-03T13:40:41Z。

- abstract_object：This involves organizing and using visual information and linking it to other findings during search.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/8/paper/summary`；quote SHA256：`78c6e13327293e0f20183010a5640f64e806f05d3766fb1cf597ad38d4b6e088`。

### 2611.06817 · Open-HumanWAM: An Open Recipe for Scaling Human and Robot Experience for Embodied Foundation Models

结论：supported。HF 日：2026-11-06；原发表：2026-11-04T17:31:35Z；当前 v2 更新：2026-11-05T16:35:16Z。

- abstract_object：dynamically adapting its manipulation behavior to unseen visual goals without parameter updates
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/9/paper/summary`；quote SHA256：`bd60d657f38f086b9c802f49a7608ae5202cd71a7a8c8e6a89d7d6663d6167f4`。

- supported：Current official title is Open-HumanWAM, while HF raw title is Open-HumanScale。

- supported：HF date 2026-11-06; published 2026-11-04; current v2 updated 2026-11-05。

### 2611.06976 · On the Opportunities and Challenges of Prefill-to-Autoregressive Cross-Model Transfer

结论：supported。HF 日：2026-11-06；原发表：2026-11-04T13:33:47Z；当前 v1 更新：2026-11-04T13:33:47Z。

- abstract_object：We find that trainable bridges can act as parameter-efficient adaptation mechanisms without exploiting useful sender information.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/10/paper/summary`；quote SHA256：`cfc6dd4a89cd2c6f7e012c352354359b16fe4027af35dd9bef40529637561b76`。

### 2611.07909 · EDGAR: Efficient Diffusion-Driven Gaussian Avatar Refinement via Synthetic Failure

结论：supported。HF 日：2026-11-06；原发表：2026-11-05T12:25:51Z；当前 v1 更新：2026-11-05T12:25:51Z。

- abstract_object：The refined multi-view renderings are subsequently used as pseudo-targets to optimize a single underlying Gaussian avatar
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/11/paper/summary`；quote SHA256：`0ca30f48cf3a5f54d3ce5ec2d14b8c0b1eed8c9b95ed07751617ac3e314b0a02`。

### 2611.02660 · HeLM: Hierarchical Explicit Language Memory for Non-Markovian Manipulation

结论：supported。HF 日：2026-11-06；原发表：2026-11-02T07:20:12Z；当前 v1 更新：2026-11-02T07:20:12Z。

- abstract_object：a hierarchical VLA framework that maintains task-relevant history in explicit language through factorized event detection and event-triggered memory updates
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/12/paper/summary`；quote SHA256：`e5687cb1982565a71c822c3aedae04e3aa226cc2646972dbab052feb12091e63`。
- persistence_boundary：including five newly formulated inter-episode tasks that require persistent context across task boundaries.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/12/paper/summary`；quote SHA256：`11bfc360da47a49b3df196df2481fcd89d744a445607fc24970488be89739aa8`。

### 2611.04527 · Future Representation Distillation for Imagination-free World Action Models

结论：supported。HF 日：2026-11-06；原发表：2026-11-03T08:55:03Z；当前 v2 更新：2026-11-04T11:04:43Z。

- abstract_object：The visual encoder learns to predict a frozen video diffusion model's representation using only the current observation.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/13/paper/summary`；quote SHA256：`db91c5f1936405fc0fac5bd2f4bece645d1c5079ec668998609b335730fe7b99`。

### 2611.08237 · Terminal-style Mathematical Modeling Bench: The First Agentic and Verifiable Benchmark for Mathematical Modeling

结论：supported。HF 日：2026-11-06；原发表：2026-11-05T16:18:35Z；当前 v1 更新：2026-11-05T16:18:35Z。

- abstract_object：Each task ships the verbatim statement, official attachments, and figures in a containerized terminal
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/14/paper/summary`；quote SHA256：`496d3870c43adb2b652c9120bfc36c74dcae07e848f8eba05e3adc27e1057b80`。

### 2611.08376 · Muir: Linear Attention with Sensitivity-Allocated Gating and Matched-Filter Readout

结论：supported。HF 日：2026-11-06；原发表：2026-11-05T17:53:49Z；当前 v1 更新：2026-11-05T17:53:49Z。

- abstract_object：Linear attention compresses context into a fixed-size key-value state for linear-time training and constant-memory inference.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/15/paper/summary`；quote SHA256：`9aae0092ff9f9ec788b0f02dc85bd88e1f0922e750693a5761e2c0e2971ea2dc`。

### 2611.08089 · SAE Interprets MoE: Sparse AutoEncoders Reveal That MoE Experts Exhibit Human-Interpretable Fine-Grained Specialization

结论：supported。HF 日：2026-11-06；原发表：2026-11-05T14:35:08Z；当前 v1 更新：2026-11-05T14:35:08Z。

- abstract_object：We instead study specialization in feature space by training a sparse autoencoder (SAE) on the output of an MoE layer.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/16/paper/summary`；quote SHA256：`bceb43c007363958ce0d8fb25c455e00434780a0c6e41c31564c804c58a0ceb0`。

### 2611.05376 · From Autonomous Agents to Cognitive Symbionts: Toward AI-Augmented Human Intelligence

结论：supported。HF 日：2026-11-06；原发表：2026-11-03T18:59:52Z；当前 v1 更新：2026-11-03T18:59:52Z。

- abstract_object：keeps their context across years, models their situation and their mind, takes part in their thinking at the right moment
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/17/paper/summary`；quote SHA256：`39d6bd21b9b36b7bfc6de128fd50a68688d206e02770f7fc5ac251e12c16c3a3`。

### 2611.06982 · Decode Before You Hear: Speculative Listening for Chunk-Interleaved Full-Duplex Speech Language Models

结论：supported。HF 日：2026-11-06；原发表：2026-11-04T15:16:15Z；当前 v1 更新：2026-11-04T15:16:15Z。

- abstract_object：It keeps all drafts in a cross-chunk hypothesis pool and verifies them when the audio arrives.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/18/paper/summary`；quote SHA256：`dfd6285b0af52645a5cdf27f7b9d2f33053d7bea33b21f5a96fc60349f222941`。

### 2611.04386 · StepX-OPD: Rethinking Multi-Teacher On-Policy Distillation in Diffusion Models

结论：supported。HF 日：2026-11-06；原发表：2026-11-03T06:16:16Z；当前 v1 更新：2026-11-03T06:16:16Z。

- abstract_object：one student acquires every capability while learning to sample in a few steps
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/19/paper/summary`；quote SHA256：`4cad12e4e345686366818f607eb3de30b5eff1cb438ab2fa0957106cac00b166`。

### 2611.08483 · SwarmEvolve: Latent Agent Swarms for Evolutionary Discovery and Optimization

结论：supported。HF 日：2026-11-06；原发表：2026-11-05T18:59:29Z；当前 v1 更新：2026-11-05T18:59:29Z。

- abstract_object：LLM-guided evolutionary search uses AI agents to improve programs for mathematical and computational problems by iteratively refining solutions and combining high-scoring methods.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/20/paper/summary`；quote SHA256：`34922f9bd46c9b3c1f495ec3641030c2d27bad1b73e31f3a9cb63c1953a13096`。
- external_program：LLM-guided evolutionary search uses AI agents to improve programs for mathematical and computational problems by iteratively refining solutions and combining high-scoring methods.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/20/paper/summary`；quote SHA256：`34922f9bd46c9b3c1f495ec3641030c2d27bad1b73e31f3a9cb63c1953a13096`。

### 2610.37739 · OpenFrontiers: A Collection of Open Research Problems and a Benchmark for Scientific Rediscovery

结论：supported。HF 日：2026-11-06；原发表：2026-10-27T16:49:33Z；当前 v1 更新：2026-10-27T16:49:33Z。

- abstract_object：Our evaluation protocol grades formal proofs with two independent checkers in an isolated sandbox under closed-book, frozen-retrieval, and live-web conditions.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/21/paper/summary`；quote SHA256：`e8abf0e579f8c6c056d8e28c7174920c98a4871ae76087a5cd77144519753456`。

### 2609.37820 · Information Games: Strategic Crowding and Firm Repositioning in Language-Model Space

结论：supported。HF 日：2026-11-06；原发表：2026-09-29T15:30:02Z；当前 v2 更新：2026-11-05T17:56:23Z。

- abstract_object：These measurements let researchers represent these news articles as clouds of dense vectors whose information geometry reflects the dissimilarity of firms over time.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/22/paper/summary`；quote SHA256：`0d274434b1fef379ead7dbee0e12caefdecfe6ad2cedacd35853618a2a1e818d`。

### 2611.07298 · Reducing Representational Interference in Retrieval Embeddings with Trainable Prefix Tokens

结论：supported。HF 日：2026-11-06；原发表：2026-11-05T01:30:28Z；当前 v1 更新：2026-11-05T01:30:28Z。

- abstract_object：The method keeps the model architecture, pooling strategy, and training loss unchanged, while optimizing the added tokens through the standard contrastive retrieval objective.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/23/paper/summary`；quote SHA256：`bafa0868ee6d938dfdb15db7bcf23fd0b120dae0af5fd09004fd2e4afaad26cb`。

### 2611.07613 · Towards Real-Time Full-Waveform LiDAR Transformers via Intensity-Guided Token Reduction and Physics-Aware Augmentation

结论：supported。HF 日：2026-11-06；原发表：2026-11-05T07:56:01Z；当前 v1 更新：2026-11-05T07:56:01Z。

- abstract_object：First, we propose FWL-ToPM, a token pruning and merging mechanism that leverages intensity distributions to selectively reduce tokens while retaining critical waveform content.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/24/paper/summary`；quote SHA256：`9703563b6d1aedab433145a60819ee0b756e5d7893e14eff142409ba6a978483`。

### 2611.08369 · NPCBench: A Clinical Apprenticeship Benchmark for Multimodal Care-Pathway Reasoning in Nasopharyngeal Carcinoma

结论：supported。HF 日：2026-11-06；原发表：2026-11-05T17:48:55Z；当前 v1 更新：2026-11-05T17:48:55Z。

- abstract_object：The episode-level evaluation tests whether diagnostic and care answers are jointly correct within a care pathway.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/25/paper/summary`；quote SHA256：`65d23f700ba2f63f60047bb9ab8ea69bcc32375a48ba00d212d64d47b21dabc4`。

### 2610.41789 · Hard Sample-Conditioned Decorrelated Attention for Robust Face Recognition

结论：supported。HF 日：2026-11-06；原发表：2026-10-30T14:21:43Z；当前 v1 更新：2026-10-30T14:21:43Z。

- abstract_object：we propose ViT-HarDis, which conditions attention head disentanglement on sample difficulty
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/26/paper/summary`；quote SHA256：`c0f17dc549a6008f569f12b69e593a682a06e0ac12b1f19998b556828996b858`。

### 2610.40119 · SynthFaces: Balanced Large Scale Human Dataset

结论：supported。HF 日：2026-11-06；原发表：2026-10-29T14:17:06Z；当前 v1 更新：2026-10-29T14:17:06Z。

- abstract_object：In this work we propose a pipeline for controllable generation of dataset with diverse faces for generative models training and finetuning.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/27/paper/summary`；quote SHA256：`57bef0d289806eeca3c4edd13261f4fc1a3c3952f5897988b8b947158b500625`。

### 2611.02075 · Decoupled Predictive Decision Making: A Shared Conditional Predictor for Agents

结论：supported。HF 日：2026-11-06；原发表：2026-11-01T17:27:21Z；当前 v1 更新：2026-11-01T17:27:21Z。

- abstract_object：deployment evidence instantiates problem-specific predictions without updating either model's neural parameters
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/28/paper/summary`；quote SHA256：`ed78c7a0edeb7dee8bcc6c2e3d70f861bed0efb8a15956d83ccfcdd1682d3636`。
- frozen_predictor：A single frozen LimiX-2 predictor serves all five task categories.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/28/paper/summary`；quote SHA256：`2be4c235e173748633dbb88cb8f167b8e44d76516877d8e255f9bf33dbbdc5f2`。

### 2610.34074 · Identically Trained Language Models Break on Different Jailbreaks

结论：supported。HF 日：2026-11-06；原发表：2026-10-25T05:30:02Z；当前 v1 更新：2026-10-25T05:30:02Z。

- abstract_object：These results indicate that which jailbreaks break a checkpoint depends much more on its pretraining run than on its data
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/29/paper/summary`；quote SHA256：`065916995f819cc95095d0931c062923db1fbc18593a5f32e9bc78908ed922ce`。

### 2611.06498 · Signed but Steerable: Measuring and Closing the Text-Vector Integrity Gap in Offline Retrieval-Augmented Generation

结论：supported。HF 日：2026-11-06；原发表：2026-11-04T13:32:04Z；当前 v1 更新：2026-11-04T13:32:04Z。

- abstract_object：A signature proves who published a pack, not that its vectors encode its text.
  - 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/30/paper/summary`；quote SHA256：`f1050b30dbb1ff93f39293556e07cac68f0becbff22e3b2e2e263beb532df2e6`。

## 证据边界

这是对缓存原始材料的独立来源复核，未再次下载，也未调用付费模型、执行实验、修改生产数据或对外写入。主审 source_hash 是证据快照哈希，不冒充集成后生产 canonical 的正式审核哈希。后续日期审核、工程 CI、真实合并凭证与部署验证由发布流程分别完成。
