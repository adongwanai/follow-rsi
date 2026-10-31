# 2026-10-29 第三轮独立反向复审

这轮只读8篇原始 HF 标题、摘要和日期字段，未读第一轮结论、其他模型标签或 owner 的 decision。所有结果都是审核建议，不是人工批准；没有改动 decision，没有发布论文。

**范围结论：8篇均不建议进入 Harness 专题；其中 TAO 和 CausGround 已补查 arXiv 方法正文。** 其余6篇仅做范围筛查，不声称完成全文证据审计。

核查判据：必须有外部可复用 Harness 工件、执行/评估反馈驱动其修改，并保留该工件新版本。冻结权重、有工具、持久记忆或算法会按状态作决策均不单独构成 Harness RSI。

## 日期核对

8篇的 `paper.submittedOnDailyAt` 都是 `2026-10-29T00:00:00.000Z`，所以属于10月29日 HF 推荐列表。`publishedAt` 不能代替推荐日，也不能未经核对当作首次发表日。arXiv元数据已对齐8篇身份和版本日期。

| 论文 | HF推荐日 | arXiv首次发表 | 最新版本更新 | 提示 |
|---|---|---|---|---|
| DTCA | 2026-10-29 | 2026-10-26 | 2026-10-26 | 日期分列 |
| Falcon / RealSSA | 2026-10-29 | 2026-10-23 | 2026-10-23 | 日期分列 |
| Sensorimotor Alignment | 2026-10-29 | 2026-10-22 | 2026-10-23 | HF日期对应v2，并非首次发表 |
| OmniShowcase | 2026-10-29 | 2026-10-26 | 2026-10-26 | 日期分列 |
| TAO | 2026-10-29 | 2026-10-27 | 2026-10-27 | 日期分列 |
| HuGe | 2026-10-29 | 2026-10-25 | 2026-10-25 | 日期分列 |
| CausGround | 2026-10-29 | 2026-10-21 | 2026-10-21 | 日期分列 |
| OmniSpectra | 2026-10-29 | 2026-01-21 | 2026-10-23 | HF日期对应v2，并非首次发表 |

[当日HF列表](https://huggingface.co/papers/date/2026-10-29)。OmniSpectra于1月首次发表，10月23日更新v2；Sensorimotor Alignment于10月22日首次发表、23日更新v2。这里报告源数据语义问题，不修改论文原始数据。

## 逐篇反向复核

### 1. DTCA — 不纳入Harness

[DTCA: Denoising Token Credit Assignment for Reinforcement Learning in Diffusion Language Models](https://arxiv.org/abs/2610.35201v1)

**改进对象：** `model_weights`；**权重冻结：** `no`；**实际对象由反馈驱动：** `yes`；**实际对象跨任务保留：** `unknown`。这些字段不代表Harness合格；8篇都缺少符合判据的Harness工件改写。

改进对象是扩散语言模型的RL训练信号与权重。去噪迭代不是Harness工件的跨任务更新；摘要未建立模型生成数据再训练自身的多轮RSI闭环。

> These contribution weights are used to select informative denoising timesteps and assign token-level learning signals during RL training.

摘要来源：[HF](https://huggingface.co/papers/2610.35201)。

**反向质疑：** token credit assignment和policy updates容易被误读为反思改进器，但它们是梯度训练中的信用分配。

**是否还需正文核查才能判断Harness范围：** 否。摘要明确不属Harness演化；不为排除无关论文执行无必要的全文证据审计。

### 2. Falcon / RealSSA — 不纳入Harness

[Efficient Streaming Audio-Visual Target Speaker Extraction for Real-World Acoustic Scenes](https://arxiv.org/abs/2610.32749v1)

**改进对象：** `model_weights`；**权重冻结：** `no`；**实际对象由反馈驱动：** `unknown`；**实际对象跨任务保留：** `unknown`。这些字段不代表Harness合格；8篇都缺少符合判据的Harness工件改写。

实时视听目标说话人分离模型和评测集，优化架构与监督训练目标；没有Agent外部工件演化。

> We train Falcon with an encoder-space speaker contrastive loss.

摘要来源：[HF](https://huggingface.co/papers/2610.32749)。

**反向质疑：** 反复调用小型separator只是已有方法的计算方式，不能据此判为递归自改进。

**是否还需正文核查才能判断Harness范围：** 否。摘要明确不属Harness演化；不为排除无关论文执行无必要的全文证据审计。

### 3. Sensorimotor Alignment — 不纳入Harness

[Sensorimotor Alignment: A Platonic Proxy for Embodied Policy Success](https://arxiv.org/abs/2610.31670v2)

**改进对象：** `none`；**权重冻结：** `yes`；**实际对象由反馈驱动：** `no`；**实际对象跨任务保留：** `unknown`。这些字段不代表Harness合格；8篇都缺少符合判据的Harness工件改写。

提出机器人基础模型的离线表征评估指标；既不更新Harness，也未专门评测Harness演化。模型选择与冻权重本身不足以成为RSI。

> a training-free offline metric that measures how well a model's sensory representation aligns with the geometry of physical motion.

摘要来源：[HF](https://huggingface.co/papers/2610.31670)。

**反向质疑：** 指标可用于优选VLM骨干，但这是用途，不是已实现的反馈驱动Harness改写。

**是否还需正文核查才能判断Harness范围：** 否。摘要明确不属Harness演化；不为排除无关论文执行无必要的全文证据审计。

### 4. OmniShowcase — 不纳入Harness

[OmniShowcase: Omnidirectional Subject-Consistent Video Generation from Multi-View Images](https://arxiv.org/abs/2610.35684v1)

**改进对象：** `external_artifact`；**权重冻结：** `unknown`；**实际对象由反馈驱动：** `unknown`；**实际对象跨任务保留：** `unknown`。这些字段不代表Harness合格；8篇都缺少符合判据的Harness工件改写。

合成多视角训练数据并为视频模型提供几何条件，目标是视频主体一致性。自动化数据流水线不是根据执行反馈改写Agent自身Harness。

> a fully automated data synthesis pipeline that produces training videos along diverse camera trajectories

摘要来源：[HF](https://huggingface.co/papers/2610.35684)。

**反向质疑：** 自动化数据生成也不能自动归为data_task RSI；摘要没有递归改进数据设计机制的证据。

**是否还需正文核查才能判断Harness范围：** 否。摘要明确不属Harness演化；不为排除无关论文执行无必要的全文证据审计。

### 5. TAO — 不纳入Harness

[TAO: Tool-Aware Joint Scheduling for LLM-Based Agentic Serving](https://arxiv.org/abs/2610.37230v1)

**改进对象：** `none`；**权重冻结：** `unknown`；**实际对象由反馈驱动：** `yes`；**实际对象跨任务保留：** `unknown`。这些字段不代表Harness合格；8篇都缺少符合判据的Harness工件改写。

固定的动态规划调度算法读取工具完成时间、缓存和token占用来分配请求；状态与历史统计变化，不是调度程序/提示/控制流自我改写。

> a dynamic program jointly selects and places waiting sessions under capacity constraints.

摘要来源：[HF](https://huggingface.co/papers/2610.37230)。

**反向质疑：** 工具时长历史和执行状态影响决策，虽属于反馈，但不修改可复用算法。文中evaluation interface可扩展是设计能力，不能当成已运行的自改进闭环。

> The evaluation triplet’s order remains fixed while its values evolve over time.

[正文](https://arxiv.org/html/2610.37230v1#S3.SS2)：固定规则对动态状态求值，非规则工件迭代。

> The predictor combines these hints, parsed sleep commands, and historical tool durations, using direct timing evidence first and falling back to the tool-specific history, global history, or a five-second default

[正文](https://arxiv.org/html/2610.37230v1#S3.SS4)：历史时长只是既定预测器的输入。

**是否还需正文核查才能判断Harness范围：** 否。无待决的Harness范围判断；仅已检查所列方法段落，未宣称全文证据审计。

### 6. HuGe — 不纳入Harness

[HuGe: Scaling Humanoid Generalist Vision-Language-Action Models with Egocentric Experience](https://arxiv.org/abs/2610.34186v1)

**改进对象：** `model_weights`；**权重冻结：** `no`；**实际对象由反馈驱动：** `unknown`；**实际对象跨任务保留：** `unknown`。这些字段不代表Harness合格；8篇都缺少符合判据的Harness工件改写。

具身VLA预训练、适配和微调改变模型权重。三阶段训练不等同于跨代自改进，更没有外部Harness工件的反馈更新。

> a three-stage training pipeline that combines egocentric pre-training, humanoid adaptation, and downstream fine-tuning.

摘要来源：[HF](https://huggingface.co/papers/2610.34186)。

**反向质疑：** 标题的experience指人类/机器人示范训练数据，不能将其视为Agent自主反馈积累或工具技能代码演化。

**是否还需正文核查才能判断Harness范围：** 否。摘要明确不属Harness演化；不为排除无关论文执行无必要的全文证据审计。

### 7. CausGround — 不纳入Harness

[CausGround: Causal Interaction Grounding for Adaptive Embodied Planning](https://arxiv.org/abs/2610.29702v1)

**改进对象：** `memory_entries`；**权重冻结：** `yes`；**实际对象由反馈驱动：** `yes`；**实际对象跨任务保留：** `yes`。这些字段不代表Harness合格；8篇都缺少符合判据的Harness工件改写。

成功/失败轨迹生成可复用因果知识记录，正文明确任务执行时因果子图固定、只更新局部世界状态。复用知识数据不等于反馈改写技能程序、记忆管理策略或Harness。

> a non-parametric causal interaction grounding framework that distills interaction experience into reusable action-centered causal knowledge.

摘要来源：[HF](https://huggingface.co/papers/2610.29702)。

**反向质疑：** 无参数更新、可复用action规则、反馈和规划全都具备，但被保留的是环境因果知识；不能把它直接包装为Harness RSI，也不能未经进一步证据就声称多轮经验型RSI。

> We construct the CausGround library from environment interaction experience, using different causal identification protocols according to the intervention capability of each environment.

[正文](https://arxiv.org/html/2610.29702v1#A3.SS3.SSS1)：持久对象是环境交互因果知识库。

> The retrieved knowledge contains relevant action conditions, effects, and producer dependencies, and is loaded once at the beginning of each episode rather than reconstructed at every planning step.

[正文](https://arxiv.org/html/2610.29702v1#A3.SS3.SSS2)：知识跨任务可复用，但任务内按既定机制加载。

> After execution, the new observation and public success/failure history update the local world state for the next decision, while the retrieved causal subgraph itself remains fixed.

[正文](https://arxiv.org/html/2610.29702v1#A3.SS3.SSS2)：明确区分动态状态与固定知识图；没有Harness工件更新。

**是否还需正文核查才能判断Harness范围：** 否。无待决的Harness范围判断；仅已检查所列方法段落，未宣称全文证据审计。

### 8. OmniSpectra — 不纳入Harness

[OmniSpectra: A Unified Foundation Model for Universal Spectra Representation Learning](https://arxiv.org/abs/2601.15351v2)

**改进对象：** `model_weights`；**权重冻结：** `no`；**实际对象由反馈驱动：** `unknown`；**实际对象跨任务保留：** `unknown`。这些字段不代表Harness合格；8篇都缺少符合判据的Harness工件改写。

光谱表征基础模型，改模型架构/预训练，不涉及Agent或Harness演化。

> a wavelength-native foundation model for spectral representation learning: a continuous-coordinate masked autoencoder that discards the integer pixel indexing of sequence modeling.

摘要来源：[HF](https://huggingface.co/papers/2601.15351)。

**反向质疑：** 物理结构与参数规模的取舍不构成自改进循环。

**是否还需正文核查才能判断Harness范围：** 否。摘要明确不属Harness演化；不为排除无关论文执行无必要的全文证据审计。

## 保留的边界与动作

- CausGround可以作为经验/具身方向的相关线索，但正文的固定知识子图不能被描述成Harness自动进化；也没有据此自动归档为已证实的其他RSI方法。
- TAO的工具历史、缓存反馈和动态规划是静态调度机制输入/状态，不能当作Harness版本迭代。
- 日期报告需明确“HF推荐于10月29日；论文首次发表于……；最新版本更新于……”。
- 今天HF无合格Harness正例不等于所有来源无结果；仍需检查其他来源。不能为了“每天更新”补入错类论文。
- 本轮未调用付费模型、未改论文数字、未改decision、未发布内容。

原始证据已保存于 `build/maintenance-2026-10-29/round3-evidence/`：8篇arXiv Atom元数据、TAO和CausGround的HTML；JSON报告包含来源URL、抓取时间和SHA-256。已核验所有正文引文为原文连续子串、所有章节锚点存在。
