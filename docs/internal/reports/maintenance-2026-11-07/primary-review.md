# HF 来源初审与边界复读 · 2026-11-07

覆盖 46 个新身份与 4 个 HF 日期补记，共 50 项。全部读取完整源摘要，并逐项做第二遍范围复读；这是同一 primary reviewer 的两遍工作，不冒充两位独立审稿人。

建议纳入 2 项，建议范围排除 48 项；没有未读条目或用统一 defer 隐藏的未读材料。正式审核决定未写入。候选仍交由独立复核与 owner 决定。

观察榜单为 11/05 的 39 项与 11/06 的 31 项；本次只处理 reconciliation 指定的增量 50 项。11/07 榜尚未准备好，不能当作空榜或全天结论。

## 需优先复核的候选与边界

- **PyRUA-REAL / 2611.06768：include 建议，harness/component + embodied。** 官方正文给出执行反馈改代码、研究员保留新技能、先前 primitive 库迁移新任务的证据。论文内 RoboDojo 数字 84.82/84.42 与摘要 84.4 有不一致，草稿避用数值；development 与 frozen evaluation 也需分开。
- **Harness-S / 2611.04277：include 建议，harness/evolve_main。** 官方正文明确多轮修改 prompts/skills/context/memory/hooks/tool view，验证选父并保留变体。变体实现随后在 RL 阶段固定，不能说训练期持续共演化。
- **KernelSeek / 2611.03517：第二遍建议 ai4ai 范围排除。** 正文说明 question bank 在实验后由作者归纳，替代人类questioner实验未开展；有手工技能复用，但未建立系统根据反馈更新技能库，主要演化对象仍是任务CUDA内核。
- **EvoMemState / 2611.03743：范围排除。** 摘要明确RL记忆使用策略与请求状态，不把状态更新误作管理代码演化。
- **Open-HumanScale / 2611.06817：元数据差异。** HF保存旧名，官方v2标题已为Open-HumanWAM；原发表日11/04、版本更新日11/05、HF日11/06分别保存。

## 逐项记录

下表的 source hash 是随JSON附带的官方元数据证据快照哈希，不冒充production canonical审核哈希。每项另存HF原始响应哈希、JSON pointer、完整摘要、官方版本日期及可定位引句。

| ID | HF日 | 原发表 / 当前版本日 | 建议 | 修改对象与理由 |
|---|---|---|---|---|
| 2611.04408 | 2026-11-05 | 2026-11-03 / v1 2026-11-03 | exclude · ai4ai | 光网络控制器：预测控制针对光网络资源；未描述Agent按执行反馈改写并复用自身Harness。 |
| 2611.06425 | 2026-11-05 | 2026-11-04 / v1 2026-11-04 | exclude · model_weights | 推测解码草稿模型：优化扩散草稿模型及层裁剪，非反馈驱动的外部Harness工件演化。 |
| 2611.01926 | 2026-11-05 | 2026-11-01 / v1 2026-11-01 | exclude · model_weights | 固定潜在推理接口：交错潜在推理与工具调用是固定接口设计；未见可保留的Harness修改。 |
| 2610.41432 | 2026-11-05 | 2026-10-30 / v1 2026-10-30 | exclude · harness | 固定多通道计算机接口：预先设计AX工具和技能帮助执行；未见系统从失败反馈迭代这些工件。 |
| 2611.06768 | 2026-11-05 | 2026-11-04 / v1 2026-11-04 | include · harness | 可复用机器人技能代码：执行报告驱动技能代码修订与保留，正文验证旧技能库迁移到新任务。 |
| 2611.05648 | 2026-11-05 | 2026-11-03 / v1 2026-11-03 | exclude · model_weights | 扩散蒸馏模型：对抗蒸馏修改图像生成模型；文本流表征不是外部Harness程序。 |
| 2611.03404 | 2026-11-05 | 2026-11-02 / v1 2026-11-02 | exclude · model_weights | 视频配音教师学生模型：配音教师训练与学生蒸馏；不存在外部可复用Harness改写闭环。 |
| 2611.03330 | 2026-11-05 | 2026-11-02 / v1 2026-11-02 | exclude · theory_survey | 推理能耗分析模型：推导推理能耗规律，未研究Harness工件的反馈演化。 |
| 2611.03768 | 2026-11-05 | 2026-11-02 / v1 2026-11-02 | exclude · model_weights | 固定稀疏注意力执行优化：复用相邻层索引并重叠执行是静态推理优化，不是自改进Harness。 |
| 2611.05988 | 2026-11-05 | 2026-11-04 / v1 2026-11-04 | exclude · model_weights | 固定流式音视频架构：滑窗、历史上下文与音频生成架构改善当前流；无反馈改写Harness。 |
| 2610.36544 | 2026-11-05 | 2026-10-27 / v1 2026-10-27 | exclude · theory_survey | 重启监控决策评估：研究重启或继续的决策价值，不是外部Harness反馈演化专项研究。 |
| 2611.03517 | 2026-11-05 | 2026-11-02 / v1 2026-11-02 | exclude · ai4ai | CUDA任务内核：正文显示问题库事后人工归纳，自问替代人未验证；核心演化对象是CUDA任务产物。 |
| 2611.03852 | 2026-11-05 | 2026-11-02 / v1 2026-11-02 | exclude · evaluation_benchmark | 当前轨迹压缩内容：改写当前推理历史并比较后续生成；未演化可跨任务复用的压缩策略。 |
| 2611.05593 | 2026-11-05 | 2026-11-03 / v1 2026-11-03 | exclude · model_weights | 高斯渲染Transformer：训练神经渲染器，研究表征与解码瓶颈，无Agent Harness演化。 |
| 2611.04760 | 2026-11-05 | 2026-11-03 / v1 2026-11-03 | exclude · model_weights | 时序预测生成模型：Koopman潜在动力学和生成预测模型，非外部Harness自改进。 |
| 2611.03394 | 2026-11-05 | 2026-11-02 / v1 2026-11-02 | exclude · model_weights | 音视频生成模型：跨片段保留的是生成历史状态，不是经反馈改写的跨任务技能。 |
| 2611.06042 | 2026-11-05 | 2026-11-04 / v1 2026-11-04 | exclude · model_weights | 图像修复专家模型：通过退化分组扩容专家模型及路由；未更新外部Harness程序。 |
| 2611.04949 | 2026-11-05 | 2026-11-03 / v1 2026-11-03 | exclude · data_task | 翻译伪标注训练数据：RAG生成伪标签以领域适配，非反馈驱动Harness工件演化。 |
| 2611.05029 | 2026-11-05 | 2026-11-03 / v1 2026-11-03 | exclude · embodied | 机器人策略参数可塑性：跨任务保留张量重要性并调学习率，改的是训练参数而非外部程序工件。 |
| 2611.08449 | 2026-11-06 | 2026-11-05 / v1 2026-11-05 | exclude · embodied | 视觉规划草稿模型：训练视觉primitive草稿模型并固定接受规则，非自演化Harness。 |
| 2611.04277 | 2026-11-06 | 2026-11-03 / v1 2026-11-03 | include · harness | 提示技能上下文等Harness：多轮按失败原因编辑Harness并验证选父、存池复用；训练期池固定。 |
| 2611.00883 | 2026-11-06 | 2026-10-31 / v1 2026-10-31 | exclude · evaluation_benchmark | 基准压缩子集：压缩通用评测集与估计误差，不是Harness演化的专项评测。 |
| 2611.08373 | 2026-11-06 | 2026-11-05 / v1 2026-11-05 | exclude · embodied | 空间语言动作模型：持续预训练和后训练更新VLA权重，辅助组件只在训练使用。 |
| 2611.07392 | 2026-11-06 | 2026-11-05 / v1 2026-11-05 | exclude · model_weights | 统一图像模型与数据：数据迭代和奖励训练作用于图像模型；未描述Harness程序修改。 |
| 2611.06741 | 2026-11-06 | 2026-11-04 / v1 2026-11-04 | exclude · model_weights | 图像编辑模型权重：从自身rollout训练去噪修正，持续的是模型能力，不是外部Harness。 |
| 2611.03743 | 2026-11-06 | 2026-11-02 / v1 2026-11-02 | exclude · experience_world_model | RL记忆使用策略及状态：RL把记忆经验内化为策略并产生请求状态；未改写记忆管理代码。 |
| 2611.07854 | 2026-11-06 | 2026-11-05 / v1 2026-11-05 | exclude · model_weights | 非自回归决策模型：SFT与RL训练决策模型，不是外部Harness工件的反馈更新。 |
| 2611.04894 | 2026-11-06 | 2026-11-03 / v1 2026-11-03 | exclude · evaluation_benchmark | 视觉搜索基准：评测长程视觉搜索与上下文使用，未专门研究Harness工件演化。 |
| 2611.06817 | 2026-11-06 | 2026-11-04 / v2 2026-11-05 | exclude · embodied | 人类机器人预训练模型：人类视频数据与策略预训练；部署适应是in-context，不是Harness改写。 |
| 2611.06976 | 2026-11-06 | 2026-11-04 / v1 2026-11-04 | exclude · model_weights | 跨模型线性桥参数：任务奖励训练连接冻结模型的线性桥；桥参数不是外部程序工件演化。 |
| 2611.07909 | 2026-11-06 | 2026-11-05 / v1 2026-11-05 | exclude · ai4ai | 高斯头像表示：修复头像渲染与优化头像本体，属于目标产物而非Agent自身Harness。 |
| 2611.02660 | 2026-11-06 | 2026-11-02 / v1 2026-11-02 | exclude · experience_world_model | 语言记忆事件与历史：可跨episode保存任务上下文，但更新的是记忆内容而非管理程序。 |
| 2611.04527 | 2026-11-06 | 2026-11-03 / v2 2026-11-04 | exclude · embodied | 预测视觉编码器和动作模块：表示蒸馏与动作训练改权重，非外部Harness迭代修改。 |
| 2611.08237 | 2026-11-06 | 2026-11-05 / v1 2026-11-05 | exclude · evaluation_benchmark | 数学建模验证基准：固定数值与形式验证器评测建模产物，不是反馈演化Harness的基准。 |
| 2611.08376 | 2026-11-06 | 2026-11-05 / v1 2026-11-05 | exclude · model_weights | 线性注意力网络：门控与读出结构优化及模型训练，缓存状态不构成Harness自改进。 |
| 2611.08089 | 2026-11-06 | 2026-11-05 / v1 2026-11-05 | exclude · theory_survey | MoE特征解释分析：训练SAE分析专家分工，未涉及Harness工件反馈演化。 |
| 2611.05376 | 2026-11-06 | 2026-11-03 / v1 2026-11-03 | exclude · theory_survey | 认知共生概念框架：提出长期人机协同范式；未给出具体Harness工件自修改与验收机制。 |
| 2611.06982 | 2026-11-06 | 2026-11-04 / v1 2026-11-04 | exclude · harness | 固定推测监听调度：跨音频块保存待验证草稿是当前推理状态，调度程序本身不演化。 |
| 2611.04386 | 2026-11-06 | 2026-11-03 / v1 2026-11-03 | exclude · model_weights | 扩散学生模型：冻结教师监督学生on-policy蒸馏，非外部Harness工件更新。 |
| 2611.08483 | 2026-11-06 | 2026-11-05 / v1 2026-11-05 | exclude · ai4ai | 科学问题候选程序：潜在swarm迭代候选数学与科学程序；目标产物演化不等于自身Harness。 |
| 2610.37739 | 2026-11-06 | 2026-10-27 / v1 2026-10-27 | exclude · evaluation_benchmark | 科研再发现评测：研究问题语料与形式证明再发现评测，未专项评测Harness反馈演化。 |
| 2609.37820 | 2026-11-06 | 2026-09-29 / v2 2026-11-05 | exclude · theory_survey | 企业竞争经济模型：语言向量辅助企业竞争研究；无Agent Harness自改进机制。 |
| 2611.07298 | 2026-11-06 | 2026-11-05 / v1 2026-11-05 | exclude · model_weights | 检索embedding前缀参数：可训练前缀是梯度优化的参数，不是文本提示工件反馈演化。 |
| 2611.07613 | 2026-11-06 | 2026-11-05 / v1 2026-11-05 | exclude · embodied | LiDAR感知网络与增强：传感器token压缩与训练数据增强，非Agent Harness演化。 |
| 2611.08369 | 2026-11-06 | 2026-11-05 / v1 2026-11-05 | exclude · evaluation_benchmark | 临床路径评测：评测临床证据与纵向状态推理，不是Harness反馈演化研究。 |
| 2610.41789 | 2026-11-06 | 2026-10-30 / v1 2026-10-30 | exclude · model_weights | 人脸识别注意力参数：按难样本正则注意力头，修改模型训练而非外部Harness。 |
| 2610.40119 | 2026-11-06 | 2026-10-29 / v1 2026-10-29 | exclude · data_task | 合成人脸数据：合成人脸数据管线服务训练微调，未描述Harness反馈自修改。 |
| 2611.02075 | 2026-11-06 | 2026-11-01 / v1 2026-11-01 | exclude · experience_world_model | 条件预测历史证据：冻结预测器随历史证据增长改善决策，更新的是证据数据而非管理工件。 |
| 2610.34074 | 2026-11-06 | 2026-10-25 / v1 2026-10-25 | exclude · safety_governance | 越狱敏感性分析：分析不同预训练随机种子的越狱迁移，不研究Harness自演化。 |
| 2611.06498 | 2026-11-06 | 2026-11-04 / v1 2026-11-04 | exclude · safety_governance | 固定RAG完整性验证器：验证离线知识包向量与文本一致性；无反馈改写验证器的演化闭环。 |

## 可恢复证据

### 2611.04408 · Halley: A Predictive Control Plane for Optical AI Data Center Networks

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/3/paper`；源响应SHA256 `4afde0d5f69290f329c5c2bd7775ec890c99d124ab7dba62ae8b15122b025fcd`。
- 证据快照 source_hash：`4868085695b0105adef9445c49e6b2f238e92837ae5dade4ce9df66eaaf5b844`；摘要SHA256 `55baddd84d71a33a7d7cc0e43a1ce7c3801e471393fc2e89daab2bbe40afc246`。
- 摘要依据：> Halley gives each layer a predictive controller that defers to the deployed policy when unsure.
- 第一遍：exclude；预测控制针对光网络资源；未描述Agent按执行反馈改写并复用自身Harness。
- 第二遍：exclude；预测控制针对光网络资源；未描述Agent按执行反馈改写并复用自身Harness。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.06425 · D3D: Decoupled Diffusion Drafting for Asynchronous Speculative Decoding

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/12/paper`；源响应SHA256 `4afde0d5f69290f329c5c2bd7775ec890c99d124ab7dba62ae8b15122b025fcd`。
- 证据快照 source_hash：`01e196806196119b96efc5aa07ef435cf8303e847dc7b60d2295553c99539c38`；摘要SHA256 `a6c8a4b5ae1c38f21fa00172c29b27c97e71c3560896016f25ad8011f8810385`。
- 摘要依据：> D3D combines blockwise denoising with auxiliary autoregressive supervision to achieve long accepted prefixes without target hidden states.
- 第一遍：exclude；优化扩散草稿模型及层裁剪，非反馈驱动的外部Harness工件演化。
- 第二遍：exclude；优化扩散草稿模型及层裁剪，非反馈驱动的外部Harness工件演化。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.01926 · TAC-CoT: Tool-Empowered Implicit Chain-of-Thought via Interleaving Explicit Tokens

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/14/paper`；源响应SHA256 `4afde0d5f69290f329c5c2bd7775ec890c99d124ab7dba62ae8b15122b025fcd`。
- 证据快照 source_hash：`4593a70fb7cbb39a21c1efb7edd16d78df92f04d2d7045bc716a59a43b15d837`；摘要SHA256 `e84b0394762a4b252e326da5512afcca8df49da7814abda2b25507cc271c1c6a`。
- 摘要依据：> This interleaved design enables agentic tool-use without verbalizing every intermediate reasoning step.
- 第一遍：exclude；交错潜在推理与工具调用是固定接口设计；未见可保留的Harness修改。
- 第二遍：exclude；交错潜在推理与工具调用是固定接口设计；未见可保留的Harness修改。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2610.41432 · Hybrid Computer Use: A Unified Programmatic, Semantic, and Visual Interface for General Agents

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/15/paper`；源响应SHA256 `4afde0d5f69290f329c5c2bd7775ec890c99d124ab7dba62ae8b15122b025fcd`。
- 证据快照 source_hash：`bbb4336257bf2611133509760a97cec9558ed447cc50beeafe8b5eff5cf0bbca`；摘要SHA256 `9b2f3cc8a0e5e7d677239a63def3f04affb9cfe37f94bd1ce0fe8f7fd2e949bf`。
- 摘要依据：> A supplementary HCU skill guides agents in selecting and coordinating channels to use the unified interface effectively.
- 第一遍：exclude；预先设计AX工具和技能帮助执行；未见系统从失败反馈迭代这些工件。
- 第二遍：exclude；预先设计AX工具和技能帮助执行；未见系统从失败反馈迭代这些工件。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.06768 · PyRUA-REAL: Robot Exploration and Adaptive Learning through RSI in the Real World

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/19/paper`；源响应SHA256 `4afde0d5f69290f329c5c2bd7775ec890c99d124ab7dba62ae8b15122b025fcd`。
- 证据快照 source_hash：`af454767639b7add58de9e2d38a802d008c67b29b7a5fc1403f0a33d4ecb5550`；摘要SHA256 `253b2906f34144e3967506bb012f5442b322cfe2bb1a261fea4189c7e42c3a94`。
- 摘要依据：> persistent memory and reusable executable skills that inform subsequent exploration and improvement
- 第一遍：borderline；摘要说明执行反馈、持久可执行技能与后续复用；需正文区分任务产物与跨任务primitive技能。
- 第二遍：harness；执行报告驱动技能代码修订与保留，正文验证旧技能库迁移到新任务。
- 正文 feedback（`build/maintenance-2026-11-07/primary-review-sources/2611.06768v1.txt:282`）：> Execution feedback guides program revisions, which are evaluated in subsequent tests.
- 正文 retention（`build/maintenance-2026-11-07/primary-review-sources/2611.06768v1.txt:466`）：> The researcher also decides which adapted implementations to retain as new skills and records their observed applicability and limitations.
- 正文 cross_task（`build/maintenance-2026-11-07/primary-review-sources/2611.06768v1.txt:714`）：> In a separate eight-task comparison, agents start new-task exploration with or without a primitive-skill library developed on earlier tasks.
- 正文 held_out（`build/maintenance-2026-11-07/primary-review-sources/2611.06768v1.txt:691`）：> Final programs are evaluated in 18 executions across six held-out layouts, with test outcomes withheld from the revising agent.
- 正文 limitation（`build/maintenance-2026-11-07/primary-review-sources/2611.06768v1.txt:693`）：> Each task–condition pair has one development session, so variability across independent sessions remains unmeasured.
- 尚待：第三轮独立核验与owner正式决定尚未由本报告完成。
- 限制：abstract reports 84.4%; introduction says 84.82%; results section says 84.42%. Do not publish a numeric success claim without reconciliation.
- 限制：Development success aggregates program revisions; frozen-program success is a separate measurement.
- 限制：Feedback comparison has one development session per task-condition; some conditions use privileged ground-truth state.
- 限制：Human assistance and unequal or unspecified benchmark seeds limit autonomous and head-to-head claims.

### 2611.05648 · NitroFusion2: Bringing Adversarial Loss to the Text Stream of Multimodal Diffusion Transformers

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/22/paper`；源响应SHA256 `4afde0d5f69290f329c5c2bd7775ec890c99d124ab7dba62ae8b15122b025fcd`。
- 证据快照 source_hash：`9bf39c2112e0b66a9df627404b30a0ba226cb4cefebf071d20c01f6fec18e362`；摘要SHA256 `6227aecdefe6a815025a6b68513948c959ffbac18596ee0ec9bec14965ec5f64`。
- 摘要依据：> We introduce Text-Stream Adversarial Distillation (TSAD), which exploits intermediate text-token states as a new adversarial representation.
- 第一遍：exclude；对抗蒸馏修改图像生成模型；文本流表征不是外部Harness程序。
- 第二遍：exclude；对抗蒸馏修改图像生成模型；文本流表征不是外部Harness程序。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.03404 · VidDub: Replacement-Aware Distillation for Two-Step Video Dubbing

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/23/paper`；源响应SHA256 `4afde0d5f69290f329c5c2bd7775ec890c99d124ab7dba62ae8b15122b025fcd`。
- 证据快照 source_hash：`85c4d9d0ec63ed06ac2b0519045a0a85d16ad40d1650bc72cd049d127f61a183`；摘要SHA256 `dfce3a202bb16dee7216c8b230080dd9eaf574c1037f679525b4d0d4bf8d43f3`。
- 摘要依据：> Matched trajectory regression then transfers the teacher's CFG-guided trajectories to a two-step student, and distribution matching distillation recovers visual quality after step compression.
- 第一遍：exclude；配音教师训练与学生蒸馏；不存在外部可复用Harness改写闭环。
- 第二遍：exclude；配音教师训练与学生蒸馏；不存在外部可复用Harness改写闭环。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.03330 · The SIMPLE Law for Energy Cost of LLM Inference

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/25/paper`；源响应SHA256 `4afde0d5f69290f329c5c2bd7775ec890c99d124ab7dba62ae8b15122b025fcd`。
- 证据快照 source_hash：`cfc3c364df2cf6391a6f257557d30bcb4c719c4cc6dcdd5ec80a4d18af07fed7`；摘要SHA256 `df15978061c18993718f811386d566d03a8f860023690406ec68ef25eb317a9c`。
- 摘要依据：> The SIMPLE law explains as well as predicts: prefill energy grows quadratically with the hidden dimension
- 第一遍：exclude；推导推理能耗规律，未研究Harness工件的反馈演化。
- 第二遍：exclude；推导推理能耗规律，未研究Harness工件的反馈演化。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.03768 · Multi-layer Indexer: Overlapping Selection and Attention in DeepSeek Sparse Attention

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/28/paper`；源响应SHA256 `4afde0d5f69290f329c5c2bd7775ec890c99d124ab7dba62ae8b15122b025fcd`。
- 证据快照 source_hash：`0304be129c8c51e9a9886dd704526d0d36d9d052e335356ca4a63c9f41bb54c7`；摘要SHA256 `45dad33185a25a47dd0d4deb76b649740c515e75b78506819ec0e39966fe1c0e`。
- 摘要依据：> The resulting Multi-layer Indexer (MLI) needs no retraining and no new weights.
- 第一遍：exclude；复用相邻层索引并重叠执行是静态推理优化，不是自改进Harness。
- 第二遍：exclude；复用相邻层索引并重叠执行是静态推理优化，不是自改进Harness。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.05988 · LiveFoley: Dynamic Real-Time Video-to-Audio Generation for Immersive Interactive Worlds

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/29/paper`；源响应SHA256 `4afde0d5f69290f329c5c2bd7775ec890c99d124ab7dba62ae8b15122b025fcd`。
- 证据快照 source_hash：`245a155afb844ada4617dde199c0f2d1100dbedfbfb636d06ba2e2c65b781e13`；摘要SHA256 `c94edbd24e3e934d30f3e1e74af926ffb369b8a8df93c7bb41f57c20d16a827a`。
- 摘要依据：> History LocDiT adds past context to improve quality at no latency cost and serves as our default.
- 第一遍：exclude；滑窗、历史上下文与音频生成架构改善当前流；无反馈改写Harness。
- 第二遍：exclude；滑窗、历史上下文与音频生成架构改善当前流；无反馈改写Harness。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2610.36544 · Monitor Accuracy Isn't the Answer: A Decision-Value Framework for Evaluating AI Agent Restart Monitors

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/30/paper`；源响应SHA256 `4afde0d5f69290f329c5c2bd7775ec890c99d124ab7dba62ae8b15122b025fcd`。
- 证据快照 source_hash：`48107dabe1d9e592ffbfbb76da560f692b79094b90a8616429c3ea2538af8917`；摘要SHA256 `b20244b19bd1a361d0df6dcef796d46160947825175766412b2ad096d03deaae`。
- 摘要依据：> These results motivate evaluating agent monitors through recovery opportunity, decision value, and statistical support, rather than classification performance alone.
- 第一遍：other_direction；研究重启或继续的决策价值，不是外部Harness反馈演化专项研究。
- 第二遍：other_direction；研究重启或继续的决策价值，不是外部Harness反馈演化专项研究。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.03517 · Ask, Don't Equip: Question-Driven Coding Agents for Deep Kernel Optimization

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/31/paper`；源响应SHA256 `4afde0d5f69290f329c5c2bd7775ec890c99d124ab7dba62ae8b15122b025fcd`。
- 证据快照 source_hash：`63f82bd1450049d5f6988d6c5a321575cb26b34c465161f57a87c2d574216358`；摘要SHA256 `09aac490a8108779f8af525178e73e7848b1ccdcd02cdf79e86aad5eeb5ca5b9`。
- 摘要依据：> a question-driven agent that makes an existing CUDA kernel faster with no operator-specific knowledge and no faster implementation to imitate
- 第一遍：borderline；摘要出现自用question bank，但无法确认是系统反馈更新还是人工事后技能化；需正文。
- 第二遍：other_direction；正文显示问题库事后人工归纳，自问替代人未验证；核心演化对象是CUDA任务产物。
- 正文 bank_provenance（`build/maintenance-2026-11-07/primary-review-sources/2611.03517v1.txt:315`）：> After the campaigns we distilled the recurring questions into a bank.
- 正文 skill_reuse（`build/maintenance-2026-11-07/primary-review-sources/2611.03517v1.txt:330`）：> The skill is parameterized by the seed, the scenario set, and the goal; its questions were reused across the Hopper and Blackwell campaigns nearly verbatim.
- 正文 missing_experiment（`build/maintenance-2026-11-07/primary-review-sources/2611.03517v1.txt:922`）：> Whether the bank can replace the human is the experiment this paper does not contain.
- 正文 untested（`build/maintenance-2026-11-07/primary-review-sources/2611.03517v1.txt:2081`）：> The 72 entries whose provenance is the public sources alone have not yet been exercised by our agent.
- 限制：The question bank was distilled after the campaigns and includes public-source entries not exercised by the agent.
- 限制：Skill reuse across two attention campaigns is described, but autonomous feedback-driven evolution of the question bank is not established.
- 限制：The proposed questioner-versus-human experiment is explicitly absent.

### 2611.03852 · Why Pay for Long Reasoning When Rewrite Do Trick? Causal Effects of Reasoning History Compaction on Future Generation and Agent Cost

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/32/paper`；源响应SHA256 `4afde0d5f69290f329c5c2bd7775ec890c99d124ab7dba62ae8b15122b025fcd`。
- 证据快照 source_hash：`91940fecb7d842a16a70e5b1eaa858611f3cb68159d3950cc2c4740d55e85f48`；摘要SHA256 `0d623dd425db559194ca53b0fd88691a6b84aad440d84e91210ac516047f1230`。
- 摘要依据：> Our intervention rewrites prior reasoning into compact state records before pending tool results are revealed, then compares continuations from original and compact histories.
- 第一遍：other_direction；改写当前推理历史并比较后续生成；未演化可跨任务复用的压缩策略。
- 第二遍：other_direction；改写当前推理历史并比较后续生成；未演化可跨任务复用的压缩策略。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.05593 · GaussianRenderFormer: Transformer-based Rendering of 3D Gaussian Splats

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/33/paper`；源响应SHA256 `4afde0d5f69290f329c5c2bd7775ec890c99d124ab7dba62ae8b15122b025fcd`。
- 证据快照 source_hash：`18166484ca7808625f87188d88d57c1d57401ca4e0a84cda87db7994ed5667c9`；摘要SHA256 `4ae80d1e0417c3f560c7adc587dfb69188a197409ac35e8daede998de69a125c`。
- 摘要依据：> We present GaussianRenderFormer, a transformer that takes a set of Gaussians and a camera and outputs the image directly.
- 第一遍：exclude；训练神经渲染器，研究表征与解码瓶颈，无Agent Harness演化。
- 第二遍：exclude；训练神经渲染器，研究表征与解码瓶颈，无Agent Harness演化。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.04760 · Koopman Generative Operators for Efficient Probabilistic Time-Series Forecasting

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/34/paper`；源响应SHA256 `4afde0d5f69290f329c5c2bd7775ec890c99d124ab7dba62ae8b15122b025fcd`。
- 证据快照 source_hash：`9559d1aa54d278bcca644577d903439f745227ef21e61af9cf0cb2adf391aeaa`；摘要SHA256 `bb618865f5878d6c88a4903deebe35bb6b19ad00cc1105640b966844268787aa`。
- 摘要依据：> We introduce the Koopman Generative Operator (KGO), a probabilistic forecasting method that conceptualizes prediction as the evolution of structured uncertainty.
- 第一遍：exclude；Koopman潜在动力学和生成预测模型，非外部Harness自改进。
- 第二遍：exclude；Koopman潜在动力学和生成预测模型，非外部Harness自改进。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.03394 · TaoMate-HD: Progressive-Resolution Autoregressive Audio-Video Generation

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/35/paper`；源响应SHA256 `4afde0d5f69290f329c5c2bd7775ec890c99d124ab7dba62ae8b15122b025fcd`。
- 证据快照 source_hash：`6aa70e07bd81bdbd105975c4c5182034af046e8cf20c830d0bdde7252271d6c8`；摘要SHA256 `0b94506496d48f57999c5c7c2c5092ba14a0081fbc26198e9008b5d2e6f2840d`。
- 摘要依据：> Across text updates, the model retains this history to infer what has already been spoken.
- 第一遍：exclude；跨片段保留的是生成历史状态，不是经反馈改写的跨任务技能。
- 第二遍：exclude；跨片段保留的是生成历史状态，不是经反馈改写的跨任务技能。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.06042 · UniRestorer++: Scalable Universal Image Restoration with Multi-Granularity Degradation Modeling

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/36/paper`；源响应SHA256 `4afde0d5f69290f329c5c2bd7775ec890c99d124ab7dba62ae8b15122b025fcd`。
- 证据快照 source_hash：`07a4500107f9eaf25b22bcff23f5c2d75a84995998c98b5cc7cf0cfccfb20e60`；摘要SHA256 `32d5ebb9eb867ca539d00a93fb198283424db4649b5516136c78eb287a1bca19`。
- 摘要依据：> It progressively refines degradation groups and introduces group-specific experts, coupling capacity growth with specialization.
- 第一遍：exclude；通过退化分组扩容专家模型及路由；未更新外部Harness程序。
- 第二遍：exclude；通过退化分组扩容专家模型及路由；未更新外部Harness程序。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.04949 · HERIT: Enabling Global Access to Hanja-to-English Historical Translation by Mitigating Temporal Bias

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/37/paper`；源响应SHA256 `4afde0d5f69290f329c5c2bd7775ec890c99d124ab7dba62ae8b15122b025fcd`。
- 证据快照 source_hash：`d4aa535f65b59f3b9c1b3283b8ecc34fd0b2ea3cfde7009fbb2fd7e9d6aeb000`；摘要SHA256 `0ab99a0253b51c6dbbf5fafbdb421dc8bf99a7bfd76d4781bba3b674f3e3927d`。
- 摘要依据：> This approach substantially expands the training dataset, mitigating both data scarcity and temporal overfitting across different historical periods.
- 第一遍：exclude；RAG生成伪标签以领域适配，非反馈驱动Harness工件演化。
- 第二遍：exclude；RAG生成伪标签以领域适配，非反馈驱动Harness工件演化。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.05029 · DRAP: Dynamics-Risk Adaptive Plasticity for Continual Learning in Physical AI

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0003.body#/38/paper`；源响应SHA256 `4afde0d5f69290f329c5c2bd7775ec890c99d124ab7dba62ae8b15122b025fcd`。
- 证据快照 source_hash：`03b996021c17abe9791f28a41b73347df86e1b01ff03fa452a00458fc48840ce`；摘要SHA256 `e0acd95c878a76ad314d6b21cb4e559f5e1d7e0fc220f0e51a6c81bccb57b706`。
- 摘要依据：> After each task, risk-weighted squared gradients are accumulated in a tensor-level importance memory.
- 第一遍：other_direction；跨任务保留张量重要性并调学习率，改的是训练参数而非外部程序工件。
- 第二遍：other_direction；跨任务保留张量重要性并调学习率，改的是训练参数而非外部程序工件。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.08449 · VFlash: Fast, Accurate Visual Planning via Flash Primitive Decoding

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/0/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`4d6422657e717e5fb4c7289d81926bcb995e7b8472397fcadc1a3a4cbb445879`；摘要SHA256 `07a6f4f31bd5721c225dd9dd020ae277a9384a2093b8f19a0b2cbba3ce262084`。
- 摘要依据：> VFlash therefore trains on annotated primitives and directly accepts structurally valid predictions without target-token agreement.
- 第一遍：exclude；训练视觉primitive草稿模型并固定接受规则，非自演化Harness。
- 第二遍：exclude；训练视觉primitive草稿模型并固定接受规则，非自演化Harness。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.04277 · Harness-S: Learning from Sibling Harnesses for Generalizable Agent Training

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/1/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`cd06acf0c772a83dcd3ddc471e17ddf93f7204e812322ba547d169f2ddb27ec6`；摘要SHA256 `c4aaa9ee477243a06f00bdeecc330dd01ed442f2dd08251457def948f55570ee`。
- 摘要依据：> Directional Harness Evolution develops specialized sibling harnesses along distinct repair directions, forming a reusable Sibling Harness Pool that remains fixed during policy training.
- 第一遍：borderline；摘要声称方向化Harness演化和复用池；需正文核对工件、评估选择、池何时冻结。
- 第二遍：harness；多轮按失败原因编辑Harness并验证选父、存池复用；训练期池固定。
- 正文 object（`build/maintenance-2026-11-07/primary-review-sources/2611.04277v1.txt:3264`）：> edits can alter prompts, skills, context, memory, hooks, or the tool view.
- 正文 feedback（`build/maintenance-2026-11-07/primary-review-sources/2611.04277v1.txt:3288`）：> Local evaluation tests whether an edit repairs the targeted failures while preserving behavior on successful controls.
- 正文 retention（`build/maintenance-2026-11-07/primary-review-sources/2611.04277v1.txt:697`）：> The Sibling Harness Pool retains all valid children, including those not selected as parents:
- 正文 next_round（`build/maintenance-2026-11-07/primary-review-sources/2611.04277v1.txt:3297`）：> Selected parents are paired with locally diagnosed root causes for the next round of editing, while the archive retains all executable, protocol-compliant variants.
- 正文 limitation（`build/maintenance-2026-11-07/primary-review-sources/2611.04277v1.txt:3297`）：> The resulting implementations remain fixed during policy training; only their profiles and allocation are updated.
- 尚待：第三轮独立核验与owner正式决定尚未由本报告完成。
- 限制：Offline harness variants evolve; implementations remain fixed during policy training. Do not claim continuous joint harness-policy co-evolution.
- 限制：Router profile refresh changes evidence and allocation, not the fixed harness implementations.

### 2611.00883 · Random Is Almost Enough? Stable and Low-Cost Benchmark Compression via BestRand

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/2/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`2e7d87e0bd228d5c96d59d5e4cfdb3835e476a0a26fb4e2ac2bcd391ba34861d`；摘要SHA256 `30ec7d2bf06de6f3774e1ce3bc7d6b37d73074aba110d418b85a0c312e00cdc8`。
- 摘要依据：> Benchmark compression reduces the often prohibitive time and cost of model evaluation by evaluating models on a small benchmark subset that closely matches full-benchmark results.
- 第一遍：other_direction；压缩通用评测集与估计误差，不是Harness演化的专项评测。
- 第二遍：other_direction；压缩通用评测集与估计误差，不是Harness演化的专项评测。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.08373 · SLA: Scaling Spatial-Language-Action Model via Continual Pre-training

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/3/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`892524d319aa45e72f981f6a16e18a2a0fe4c57684cad9a1bd7c42f446435c98`；摘要SHA256 `3cff212cc1ede7796f4f65c2a81fe4e8bd5522a0755319075ca275ef0afa6573`。
- 摘要依据：> All auxiliary components are used only during training, allowing direct reuse of pretrained VLA weights and preserving the original inference architecture.
- 第一遍：exclude；持续预训练和后训练更新VLA权重，辅助组件只在训练使用。
- 第二遍：exclude；持续预训练和后训练更新VLA权重，辅助组件只在训练使用。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.07392 · WeLM-Image: A Unified Image Generation Model towards Visual Intelligence

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/4/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`305670d7c3d46b7b15fc4e7ed4f1b3c906b6fadd3580088719c3eeb7d0d9d458`；摘要SHA256 `1dbddbcc75278220b2d47edbad71c3102d758eb9a4a5a6fbb460cb21678c03bf`。
- 摘要依据：> We optimize generation and editing separately with rubric- and checklist-based rewards, then consolidate the specialized policies through noise-aware on-policy distillation.
- 第一遍：exclude；数据迭代和奖励训练作用于图像模型；未描述Harness程序修改。
- 第二遍：exclude；数据迭代和奖励训练作用于图像模型；未描述Harness程序修改。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.06741 · TailSteer: Trajectory-Tail Steering for Drift-Resistant Multi-turn Image Editing

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/5/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`7adee3e4b5a2ebb4b151edb3539a72b80eb3ac97cdc4409be81a87438825c80e`；摘要SHA256 `72dd1ca8d091cffb8db8e2d5dd88f60a6ca80ac48fcbf025e96e85d8056293d6`。
- 摘要依据：> These corrections are learned from the editor's own on-policy denoising rollouts, using unchanged source content as a preservation reference without requiring curated ground-truth editing pairs.
- 第一遍：exclude；从自身rollout训练去噪修正，持续的是模型能力，不是外部Harness。
- 第二遍：exclude；从自身rollout训练去噪修正，持续的是模型能力，不是外部Harness。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.03743 · EvoMemState: Evolving Memory State for Personal Agents

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/6/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`546389f7a08221170fe7c0093b80762a8b9a9ffaec2dc3719207a8acfab1c3b4`；摘要SHA256 `202b7617387c789f94377c580cf95de9fd3e845ae264cc1ebfeaba74c61c5b6c`。
- 摘要依据：> RL-Based State Evolution internalizes memory-use experience into a policy through reinforcement learning to generate a request-specific Reasoning State.
- 第一遍：exclude；RL把记忆经验内化为策略并产生请求状态；未改写记忆管理代码。
- 第二遍：exclude；RL把记忆经验内化为策略并产生请求状态；未改写记忆管理代码。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.07854 · Towards Foundation Decision Models: Drex

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/7/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`2ff25f94b2f658e7790b070af971e1b8ce72c20fba60dff4f9136b28f0ba4848`；摘要SHA256 `a2c919e6a73a86f2ad67cd614791743fcc01e9eca09517a43c9225a4c1b74679`。
- 摘要依据：> Training combines supervised fine-tuning with reinforcement learning from adjusted feedback (RLAF), plus vision tuning for Max.
- 第一遍：exclude；SFT与RL训练决策模型，不是外部Harness工件的反馈更新。
- 第二遍：exclude；SFT与RL训练决策模型，不是外部Harness工件的反馈更新。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.04894 · VisSearch-Bench: Evaluating Long Horizon Visual Search in Multimodal Agents

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/8/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`4895c6f5f33b624f9147b722cf516603ed4ab8c24f3624ed076883be81bbd9c6`；摘要SHA256 `1d4d2d1ec3017e91411d2295c2122312f5002d7d1d9166b8530fdec38e3030ce`。
- 摘要依据：> This involves organizing and using visual information and linking it to other findings during search.
- 第一遍：other_direction；评测长程视觉搜索与上下文使用，未专门研究Harness工件演化。
- 第二遍：other_direction；评测长程视觉搜索与上下文使用，未专门研究Harness工件演化。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.06817 · Open-HumanWAM: An Open Recipe for Scaling Human and Robot Experience for Embodied Foundation Models

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/9/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`3d77cec3b006d24baf8ec3581cc280b4da855f68c1343e4fb35274d932cf4af4`；摘要SHA256 `0d07179f8b8ffed442700bca531b9124f2ef182920a3d228dde8528653e0b2ae`。
- 摘要依据：> dynamically adapting its manipulation behavior to unseen visual goals without parameter updates
- 第一遍：exclude；人类视频数据与策略预训练；部署适应是in-context，不是Harness改写。
- 第二遍：exclude；人类视频数据与策略预训练；部署适应是in-context，不是Harness改写。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.06976 · On the Opportunities and Challenges of Prefill-to-Autoregressive Cross-Model Transfer

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/10/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`f3c1e740f8454c8db5180091d044dc2992010f7aad0309d1e3c82edd1f769f60`；摘要SHA256 `316ba1ebe857718224f4ea7d4cee46ba18651ec503e007a643f66d2e18971561`。
- 摘要依据：> We find that trainable bridges can act as parameter-efficient adaptation mechanisms without exploiting useful sender information.
- 第一遍：exclude；任务奖励训练连接冻结模型的线性桥；桥参数不是外部程序工件演化。
- 第二遍：exclude；任务奖励训练连接冻结模型的线性桥；桥参数不是外部程序工件演化。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.07909 · EDGAR: Efficient Diffusion-Driven Gaussian Avatar Refinement via Synthetic Failure

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/11/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`2bded0eb9d514a0f79416920928f9426eb7dabdcf20c8bd8992e97b6d12dfd21`；摘要SHA256 `26c40aecfc57817e2c42296f684951682ff90e4bc0364664ed8a525a1cb9cbf7`。
- 摘要依据：> The refined multi-view renderings are subsequently used as pseudo-targets to optimize a single underlying Gaussian avatar
- 第一遍：exclude；修复头像渲染与优化头像本体，属于目标产物而非Agent自身Harness。
- 第二遍：exclude；修复头像渲染与优化头像本体，属于目标产物而非Agent自身Harness。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.02660 · HeLM: Hierarchical Explicit Language Memory for Non-Markovian Manipulation

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/12/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`5175d08a823a1f2219e3b9db878529063a9a18f3bcf02877345a1bf7a6f9d7fb`；摘要SHA256 `6702b22fc10bfad026b6217f61d49b2135600f25be92bd391c9fbeb544bd5e79`。
- 摘要依据：> a hierarchical VLA framework that maintains task-relevant history in explicit language through factorized event detection and event-triggered memory updates
- 第一遍：other_direction；可跨episode保存任务上下文，但更新的是记忆内容而非管理程序。
- 第二遍：other_direction；可跨episode保存任务上下文，但更新的是记忆内容而非管理程序。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.04527 · Future Representation Distillation for Imagination-free World Action Models

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/13/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`a6895d06b1d031670b5e8370805361a3d36457326d41355c1901eea663064216`；摘要SHA256 `c4fefeb86cf9a1a710b5efdca630c9fc1ba2cc7cfe521a33b787a73834f497fc`。
- 摘要依据：> The visual encoder learns to predict a frozen video diffusion model's representation using only the current observation.
- 第一遍：exclude；表示蒸馏与动作训练改权重，非外部Harness迭代修改。
- 第二遍：exclude；表示蒸馏与动作训练改权重，非外部Harness迭代修改。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.08237 · Terminal-style Mathematical Modeling Bench: The First Agentic and Verifiable Benchmark for Mathematical Modeling

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/14/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`719023b518dfaa257e8e91217fc006124f1b1ab7c98427adbbf1c839b96e108d`；摘要SHA256 `5b77d6e4232775ceaa7ada9b3df697b3e7e1cf87fa082a4c089e1dd8bdc69fbe`。
- 摘要依据：> Each task ships the verbatim statement, official attachments, and figures in a containerized terminal
- 第一遍：other_direction；固定数值与形式验证器评测建模产物，不是反馈演化Harness的基准。
- 第二遍：other_direction；固定数值与形式验证器评测建模产物，不是反馈演化Harness的基准。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.08376 · Muir: Linear Attention with Sensitivity-Allocated Gating and Matched-Filter Readout

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/15/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`53a2cad69da7694f3292752e336d061892f709c9edf12a05d0786c905c35ecfa`；摘要SHA256 `bb72df0ddfdeb608182448121116dcb39390cd86237b16e580bd867a02379c67`。
- 摘要依据：> Linear attention compresses context into a fixed-size key-value state for linear-time training and constant-memory inference.
- 第一遍：exclude；门控与读出结构优化及模型训练，缓存状态不构成Harness自改进。
- 第二遍：exclude；门控与读出结构优化及模型训练，缓存状态不构成Harness自改进。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.08089 · SAE Interprets MoE: Sparse AutoEncoders Reveal That MoE Experts Exhibit Human-Interpretable Fine-Grained Specialization

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/16/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`6adadaa8df025d04819eeb824daf3b17aa5ad008ceda46a9f4fe77789ff642c9`；摘要SHA256 `10316a4c75d8d5d4eb98340440dc99ed3b7581754155e0363744aa93de4e4117`。
- 摘要依据：> We instead study specialization in feature space by training a sparse autoencoder (SAE) on the output of an MoE layer.
- 第一遍：exclude；训练SAE分析专家分工，未涉及Harness工件反馈演化。
- 第二遍：exclude；训练SAE分析专家分工，未涉及Harness工件反馈演化。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.05376 · From Autonomous Agents to Cognitive Symbionts: Toward AI-Augmented Human Intelligence

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/17/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`16d7723e40be7ded5285016d0c09044e62de59a962f2209c1631b489a29318ff`；摘要SHA256 `2460611cefc6861496d4ba23b9ffa5d4daead63a1d131ed445142562b9033e99`。
- 摘要依据：> keeps their context across years, models their situation and their mind, takes part in their thinking at the right moment
- 第一遍：other_direction；提出长期人机协同范式；未给出具体Harness工件自修改与验收机制。
- 第二遍：other_direction；提出长期人机协同范式；未给出具体Harness工件自修改与验收机制。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.06982 · Decode Before You Hear: Speculative Listening for Chunk-Interleaved Full-Duplex Speech Language Models

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/18/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`761cf1e28e77346d720950c9e8825b715bb40120c54a97d3ba0b63e24ecbe1d1`；摘要SHA256 `eeb8995e1aae4057971cadc3fec6efbe9fcf8ba8cbeea9b89bd009097a63c6e0`。
- 摘要依据：> It keeps all drafts in a cross-chunk hypothesis pool and verifies them when the audio arrives.
- 第一遍：exclude；跨音频块保存待验证草稿是当前推理状态，调度程序本身不演化。
- 第二遍：exclude；跨音频块保存待验证草稿是当前推理状态，调度程序本身不演化。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.04386 · StepX-OPD: Rethinking Multi-Teacher On-Policy Distillation in Diffusion Models

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/19/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`9a4b40d56b28120caef9deaf672a27a2aae114a07fa94563a8e2ec98cd8ebc07`；摘要SHA256 `23c351e2e869b6f77c8b94c2cc8f3d312ec8cb98c6acb7f1d3015c9e0f79e84c`。
- 摘要依据：> one student acquires every capability while learning to sample in a few steps
- 第一遍：exclude；冻结教师监督学生on-policy蒸馏，非外部Harness工件更新。
- 第二遍：exclude；冻结教师监督学生on-policy蒸馏，非外部Harness工件更新。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.08483 · SwarmEvolve: Latent Agent Swarms for Evolutionary Discovery and Optimization

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/20/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`32f0d357612e5a5aa9c2e6383f9ca841c3f04b1b63dd713e1bc6b3cded6f3814`；摘要SHA256 `5d0eb79fa395242bca9c1bd2f8fa9301c3fc8d257833f237aaf4cf8b300e0e48`。
- 摘要依据：> LLM-guided evolutionary search uses AI agents to improve programs for mathematical and computational problems by iteratively refining solutions and combining high-scoring methods.
- 第一遍：other_direction；潜在swarm迭代候选数学与科学程序；目标产物演化不等于自身Harness。
- 第二遍：other_direction；潜在swarm迭代候选数学与科学程序；目标产物演化不等于自身Harness。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2610.37739 · OpenFrontiers: A Collection of Open Research Problems and a Benchmark for Scientific Rediscovery

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/21/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`fbc16a32bbf566a01046e7ffd3b7f14740f8bf861e587538a3b1fd8824c7dc36`；摘要SHA256 `3fe4a9e62f2325e4a7ad960ee8d04ac3db523d53adbff95f8100e54e3019c00a`。
- 摘要依据：> Our evaluation protocol grades formal proofs with two independent checkers in an isolated sandbox under closed-book, frozen-retrieval, and live-web conditions.
- 第一遍：other_direction；研究问题语料与形式证明再发现评测，未专项评测Harness反馈演化。
- 第二遍：other_direction；研究问题语料与形式证明再发现评测，未专项评测Harness反馈演化。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2609.37820 · Information Games: Strategic Crowding and Firm Repositioning in Language-Model Space

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/22/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`ba4cc4f54e4cb0631bccd304901302ebd6983093c9727d74d774484a84d3a4c2`；摘要SHA256 `c3971da87e9c4fdfc20d00c73825542c394862e08398752e6696acc99eff46ea`。
- 摘要依据：> These measurements let researchers represent these news articles as clouds of dense vectors whose information geometry reflects the dissimilarity of firms over time.
- 第一遍：exclude；语言向量辅助企业竞争研究；无Agent Harness自改进机制。
- 第二遍：exclude；语言向量辅助企业竞争研究；无Agent Harness自改进机制。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.07298 · Reducing Representational Interference in Retrieval Embeddings with Trainable Prefix Tokens

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/23/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`e5355bd0fa379ef99d591b1fedabadfbf10090eef00c675f6efd3675d7b5c779`；摘要SHA256 `e2156f5dadf6bcc5194c3383680ca048ca97a1475b034593c179c6e8b797855a`。
- 摘要依据：> The method keeps the model architecture, pooling strategy, and training loss unchanged, while optimizing the added tokens through the standard contrastive retrieval objective.
- 第一遍：exclude；可训练前缀是梯度优化的参数，不是文本提示工件反馈演化。
- 第二遍：exclude；可训练前缀是梯度优化的参数，不是文本提示工件反馈演化。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.07613 · Towards Real-Time Full-Waveform LiDAR Transformers via Intensity-Guided Token Reduction and Physics-Aware Augmentation

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/24/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`fc3f02d2a81b2264624b9eea3034f243cd34b1f2775a5d4869c0f144e6cafd57`；摘要SHA256 `11ffbb7eb4ff5599c0a260826d79969f200807c8518c387f1c5db4320212af3e`。
- 摘要依据：> First, we propose FWL-ToPM, a token pruning and merging mechanism that leverages intensity distributions to selectively reduce tokens while retaining critical waveform content.
- 第一遍：exclude；传感器token压缩与训练数据增强，非Agent Harness演化。
- 第二遍：exclude；传感器token压缩与训练数据增强，非Agent Harness演化。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.08369 · NPCBench: A Clinical Apprenticeship Benchmark for Multimodal Care-Pathway Reasoning in Nasopharyngeal Carcinoma

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/25/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`d23e2e8d34183a727310e569b094b4e8cd0e278e789866f90f42a3973e6df380`；摘要SHA256 `6d913bc8683f75004ba0af91736fa2f288d294c8b79da1bd2f8b93a8eac3220b`。
- 摘要依据：> The episode-level evaluation tests whether diagnostic and care answers are jointly correct within a care pathway.
- 第一遍：other_direction；评测临床证据与纵向状态推理，不是Harness反馈演化研究。
- 第二遍：other_direction；评测临床证据与纵向状态推理，不是Harness反馈演化研究。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2610.41789 · Hard Sample-Conditioned Decorrelated Attention for Robust Face Recognition

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/26/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`c05bc8ce66aa0a663c7a66dac50046ba6e5df11e05ed19f0d29f73192638b78a`；摘要SHA256 `f2094a6be5376b2979aece059adaa25bafc20750857e43a4ba8980d49d399c5a`。
- 摘要依据：> we propose ViT-HarDis, which conditions attention head disentanglement on sample difficulty
- 第一遍：exclude；按难样本正则注意力头，修改模型训练而非外部Harness。
- 第二遍：exclude；按难样本正则注意力头，修改模型训练而非外部Harness。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2610.40119 · SynthFaces: Balanced Large Scale Human Dataset

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/27/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`91537c177e18ed37471be057105ed9f7b0c23062cd2deadf74b944bfd7ff289b`；摘要SHA256 `d40c3890c8bcf43889a944fcdef5067b683f2706b029ef62209680b38b2be347`。
- 摘要依据：> In this work we propose a pipeline for controllable generation of dataset with diverse faces for generative models training and finetuning.
- 第一遍：exclude；合成人脸数据管线服务训练微调，未描述Harness反馈自修改。
- 第二遍：exclude；合成人脸数据管线服务训练微调，未描述Harness反馈自修改。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.02075 · Decoupled Predictive Decision Making: A Shared Conditional Predictor for Agents

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/28/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`cd889df2f71899e8143517c27b6253e516376f6f8aabbef406be336804d32538`；摘要SHA256 `ae049abaa2933c1ce1f66cdc9c00b9d3b7ca4f890d9682bb64cea29e9fccf5ff`。
- 摘要依据：> deployment evidence instantiates problem-specific predictions without updating either model's neural parameters
- 第一遍：other_direction；冻结预测器随历史证据增长改善决策，更新的是证据数据而非管理工件。
- 第二遍：other_direction；冻结预测器随历史证据增长改善决策，更新的是证据数据而非管理工件。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2610.34074 · Identically Trained Language Models Break on Different Jailbreaks

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/29/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`d97683c0f05e05f4697d383b53130239dd7a72684951e4f7be884c87d139ce9a`；摘要SHA256 `9992a4d3a77ba9c5c952ca30199e0ec5ddfd5338a7651557b31b7abf6524c7e8`。
- 摘要依据：> These results indicate that which jailbreaks break a checkpoint depends much more on its pretraining run than on its data
- 第一遍：exclude；分析不同预训练随机种子的越狱迁移，不研究Harness自演化。
- 第二遍：exclude；分析不同预训练随机种子的越狱迁移，不研究Harness自演化。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

### 2611.06498 · Signed but Steerable: Measuring and Closing the Text-Vector Integrity Gap in Offline Retrieval-Augmented Generation

- 来源：`build/maintenance-2026-11-07/network/hf-daily/0002.body#/30/paper`；源响应SHA256 `03f49b541e7f5d6c0fa231ba7a132e6780e3599eee27bc55a04b10f7ea8e4f30`。
- 证据快照 source_hash：`1f7c75476e41bda02072da91344343c436a973fbbea78ad66ee9b3385d38eb68`；摘要SHA256 `54eecdd45003baea190bd30a3d12969b3116bc4bba4712f027b81e4c5314b9ca`。
- 摘要依据：> A signature proves who published a pack, not that its vectors encode its text.
- 第一遍：exclude；验证离线知识包向量与文本一致性；无反馈改写验证器的演化闭环。
- 第二遍：exclude；验证离线知识包向量与文本一致性；无反馈改写验证器的演化闭环。
- Harness反馈与跨任务保留：未由摘要建立，记为 unclear/null；排除依据是上述对象和范围，不把缺失证据冒称反证。

## 核验与边界

已验证 64 个引用均为所列摘要或正文文本的连续原文子串，单引句不超过200字符；HF原始响应、官方metadata响应及3篇正文hash匹配。
没有调用付费API，没有生成或改写production、没有应用accept/reject/defer决定，也没有GitHub写操作。目录内 primary-review-sources 保存正文、请求收据与本报告构建脚本。
reconciliation还列出 arxiv:2611.05320 的文本变更，它不在本次46+4增量中，留待另外复核。
