# 2026-10-29 HF 第一轮独立审查

**结论：HF 当日 8 篇，明确 Harness 0 篇，Harness 边界候选 0 篇。** 本文件仅为自动审核建议，所有条目均保持 defer，不能作为 owner 审核通过。

抓取：2026-10-29 09:49:42 UTC（北京时间 17:49:42），HF API HTTP 200。全量逐篇读摘要，未依赖已有模型标签、未关键词预筛。arXiv API 核对 8/8 身份。全文审读：0。

## 日期与去重

- 8 篇均有 HF submittedOnDailyAt=2026-10-29；原始发表日期在下表单列。
- 无当日重复 ID，当前本地 feed 与论文库没有同 ID。
- HF paper.publishedAt 对 OmniSpectra 和 Sensorimotor Alignment 对应更新日，而非首发日。原始发表日期来自 arXiv API published。

| 条目 | 原始发表 | 最新版本 | HF 推荐 | 建议 | 理由 |
| --- | --- | --- | --- | --- | --- |
| [DTCA: Denoising Token Credit Assignment for Reinforcement Learning in Diffusion Language Models](https://arxiv.org/abs/2610.35201v1) | 2026-10-26 | 2026-10-26 (v1) | 2026-10-29 | 排除 | 主要是扩散语言模型的 RL 信用分配与权重训练，没有外部 Harness 工件自改写。 |
| [Efficient Streaming Audio-Visual Target Speaker Extraction for Real-World Acoustic Scenes](https://arxiv.org/abs/2610.32749v1) | 2026-10-23 | 2026-10-23 (v1) | 2026-10-29 | 排除 | 音视频目标说话人提取模型与评测集，不研究 RSI 或 Harness 演化。 |
| [Sensorimotor Alignment: A Platonic Proxy for Embodied Policy Success](https://arxiv.org/abs/2610.31670v2) | 2026-10-22 | 2026-10-23 (v2) | 2026-10-29 | 排除 | 机器人表征的离线能力代理指标，不是 Harness 自进化专项评测。 |
| [OmniShowcase: Omnidirectional Subject-Consistent Video Generation from Multi-View Images](https://arxiv.org/abs/2610.35684v1) | 2026-10-26 | 2026-10-26 (v1) | 2026-10-29 | 排除 | 多视角视频生成的数据合成与几何条件方法，不是反馈驱动的 Harness 更新。 |
| [TAO: Tool-Aware Joint Scheduling for LLM-Based Agentic Serving](https://arxiv.org/abs/2610.37230v1) | 2026-10-27 | 2026-10-27 (v1) | 2026-10-29 | 排除 | 固定的 Agent 服务调度框架；动态调度会话不等于演化调度程序。 |
| [HuGe: Scaling Humanoid Generalist Vision-Language-Action Models with Egocentric Experience](https://arxiv.org/abs/2610.34186v1) | 2026-10-25 | 2026-10-25 (v1) | 2026-10-29 | 排除 | 人形机器人 VLA 的预训练、适配和微调；三阶段训练不是 Harness 递归改进。 |
| [CausGround: Causal Interaction Grounding for Adaptive Embodied Planning](https://arxiv.org/abs/2610.29702v1) | 2026-10-21 | 2026-10-21 (v1) | 2026-10-29 | 其他方向（待审） | 复用的是交互经验提炼的因果知识，未见管理机制或工具/技能程序被改写。 |
| [OmniSpectra: A Unified Foundation Model for Universal Spectra Representation Learning](https://arxiv.org/abs/2601.15351v2) | 2026-01-21 | 2026-10-23 (v2) | 2026-10-29 | 排除 | 物理光谱表征学习模型，不研究 Agent 或 RSI。 |

## 逐篇记录

### DTCA: Denoising Token Credit Assignment for Reinforcement Learning in Diffusion Language Models

- ID：arxiv:2610.35201；建议：exclude；方向：model_weights；子方向：无。
- 改进对象：扩散语言模型权重（model_weights）。
- 判定：训练奖励、token 学习信号与 policy updates 明确指向模型参数。摘要没有给出自生数据推动下一代模型再改进的递归闭环；迭代去噪和常规 RL 更新不能当作 Harness 自进化。
- 对象原文："DTCA further calibrates these learning signals according to token-level entropy changes induced by policy updates."
- 反馈证据：yes；"These contribution weights are used to select informative denoising timesteps and assign token-level learning signals during RL training."
- 持续复用证据：unclear；摘要未给出可直接引用的相应 Harness 版本保留证据。
- 不确定性：仅读原始摘要，未审正文；递归模型改进是否另有证据未知。

### Efficient Streaming Audio-Visual Target Speaker Extraction for Real-World Acoustic Scenes

- ID：arxiv:2610.32749；建议：exclude；方向：不分配 RSI 方向；子方向：无。
- 改进对象：音视频分离模型（model_weights）。
- 判定：贡献是 AVTSE 数据集、固定网络结构和对比训练目标；没有反馈驱动的外部程序工件更新。
- 对象原文："We train Falcon with an encoder-space speaker contrastive loss."
- 反馈证据：unclear；摘要未给出可直接引用的相应更新闭环。
- 持续复用证据：unclear；摘要未给出可直接引用的相应 Harness 版本保留证据。
- 不确定性：仅读原始摘要，未审正文。

### Sensorimotor Alignment: A Platonic Proxy for Embodied Policy Success

- ID：arxiv:2610.31670；建议：exclude；方向：evaluation_benchmark；子方向：无。
- 改进对象：无演化对象：离线评测指标（none）。
- 判定：指标用于预测机器人模型成功率和选择 VLM 骨干。closed-loop evaluation 指机器人任务评估，不表示模型周围程序被持续修改。
- 对象原文："we propose Sensorimotor Alignment (S^2), a training-free offline metric that measures how well a model's sensory representation aligns with the geometry of physical motion."
- 反馈证据：unclear；摘要未给出可直接引用的相应更新闭环。
- 持续复用证据：unclear；摘要未给出可直接引用的相应 Harness 版本保留证据。
- 不确定性：仅读原始摘要，未审正文。；HF paper.publishedAt 为 10-23；arXiv 原始发表为 10-22，10-23 是 v2 更新日期。

### OmniShowcase: Omnidirectional Subject-Consistent Video Generation from Multi-View Images

- ID：arxiv:2610.35684；建议：exclude；方向：不分配 RSI 方向；子方向：无。
- 改进对象：视频训练数据与几何条件（training_env_reward）。
- 判定：自动数据合成流水线是固定训练方法；摘要没有反馈更新合成规则、课程或 Agent 程序的循环，不能因 pipeline 和自动化字样纳入 RSI。
- 对象原文："a fully automated data synthesis pipeline that produces training videos along diverse camera trajectories"
- 反馈证据：unclear；摘要未给出可直接引用的相应更新闭环。
- 持续复用证据：unclear；摘要未给出可直接引用的相应 Harness 版本保留证据。
- 不确定性：仅读原始摘要，未审正文；没有把训练数据方法推断为数据 RSI。

### TAO: Tool-Aware Joint Scheduling for LLM-Based Agentic Serving

- ID：arxiv:2610.37230；建议：exclude；方向：不分配 RSI 方向；子方向：无。
- 改进对象：固定调度器的运行时决策（none）。
- 判定：TAO 根据工具就绪、缓存与容量实时选择会话，变化的是服务状态和调度输出。摘要没有执行反馈改写控制流/策略文件、评估接受新版本并在后续任务复用的证据。不能因 tool-aware、Agentic 或 dynamic program 认定 Harness RSI。
- 对象原文："a dynamic program jointly selects and places waiting sessions under capacity constraints."
- 反馈证据：unclear；摘要未给出可直接引用的相应更新闭环。
- 持续复用证据：unclear；摘要未给出可直接引用的相应 Harness 版本保留证据。
- 不确定性：仅读原始摘要，未审正文；模型权重是否冻结不影响其固定框架排除结论。

### HuGe: Scaling Humanoid Generalist Vision-Language-Action Models with Egocentric Experience

- ID：arxiv:2610.34186；建议：exclude；方向：embodied；子方向：无。
- 改进对象：人形机器人 VLA 权重（model_weights）。
- 判定：被改进的是模型策略，数据来自人和机器人示范。摘要未写模型反复自产新训练数据形成代际改进，更没有外部可复用 Harness 工件自改写。
- 对象原文："we introduce a three-stage training pipeline that combines egocentric pre-training, humanoid adaptation, and downstream fine-tuning."
- 反馈证据：unclear；摘要未给出可直接引用的相应更新闭环。
- 持续复用证据：unclear；摘要未给出可直接引用的相应 Harness 版本保留证据。
- 不确定性：仅读原始摘要，未审正文；三阶段不能证明多代 RSI 闭环。

### CausGround: Causal Interaction Grounding for Adaptive Embodied Planning

- ID：arxiv:2610.29702；建议：other_direction；方向：experience_world_model；子方向：无。
- 改进对象：可复用动作因果知识（memory_entries）。
- 判定：该方法将交互经验沉淀为动作前提与效果，再以固定推理框架用于后续规划。非参数方法和跨环境知识复用本身不满足 Harness 判据：摘要未写修改系统提示、工具代码、技能文件、记忆管理程序或控制流。可建议归经验/世界模型方向，但持续递归知识更新与接受机制仍需正文确认。不能进入第一阶段 Harness 日报。
- 对象原文："CausGround identifies action preconditions and effects and organizes them in a factorized world-state representation capturing object attributes and inter-object relations."
- 反馈证据：unclear；摘要未给出可直接引用的相应更新闭环。
- 持续复用证据：yes；"a non-parametric causal interaction grounding framework that distills interaction experience into reusable action-centered causal knowledge."
- 不确定性：仅读原始摘要，未审正文。；未明确执行/评估反馈如何触发并接受因果知识修订；反馈驱动字段保留 unclear。；作为广义经验 RSI 是否有多轮闭环仍需正文审核；other_direction 是建议归类，不是自动接收。

### OmniSpectra: A Unified Foundation Model for Universal Spectra Representation Learning

- ID：arxiv:2601.15351；建议：exclude；方向：不分配 RSI 方向；子方向：无。
- 改进对象：光谱基础模型权重与架构（model_weights）。
- 判定：贡献为连续坐标编码、物理条件解码器和光谱预训练；无 Harness 工件的反馈更新。
- 对象原文："a wavelength-native foundation model for spectral representation learning: a continuous-coordinate masked autoencoder that discards the integer pixel indexing of sequence modeling."
- 反馈证据：unclear；摘要未给出可直接引用的相应更新闭环。
- 持续复用证据：unclear；摘要未给出可直接引用的相应 Harness 版本保留证据。
- 不确定性：仅读原始摘要，未审正文。；HF paper.publishedAt 为 10-23；arXiv 原始发表为 01-21，10-23 是 v2 更新日期。

## 验证与边界

- 所有非空引句均由脚本校验为 HF 原始摘要连续子串，且不超过 200 字符。
- 无 Harness 正例，不生成 accept、不拿早日报条目填充今日。CausGround 不进入 Harness 日报。
- 日期核验来源：`https://export.arxiv.org/api/query`，按全部 8 个 ID 请求，HTTP 200。
- 此为当前时点快照，HF 当日后续可能补充；未读正文不构成完整证据审计。
- 系统 Python 首次遇到本机证书链错误；仓库 venv 的 requests 在正常证书验证下成功，无关闭 TLS 验证。
- 原始 HF 响应 SHA-256：`d26fb4a5fc3bfdf6e8538db8a29ab3e977a00fa4f670128a1d96a4167f489ad9`。
