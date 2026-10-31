# HF 2026-10-30：前两轮来源复审

真实榜单 16 篇全部与官方 arXiv Atom 核对标题、摘要、首次发表和版本日期；全部读过摘要，6 篇另读正文的相关方法/评测/限制章节。此文件是第三轮之前的主审快照；独立复核另列，没有 owner accept 或发布授权。

建议：1 篇 Harness 候选（VibeGame），2 篇明确属于任务/训练环境而不属于 Harness（广义 RSI 是否纳入继续待查），13 篇排除。

HF 推荐日期统一为 2026-10-30，论文原始发表日期仍保留在下表；不将旧论文伪装为当天首次发表。

| 论文 | 首次发表 | Harness 范围建议 | 依据 |
| --- | --- | --- | --- |
| [CoSTA: Compressed Speech Token Adaptation for Efficient Spoken Dialogue Models](https://arxiv.org/abs/2610.21143) | 2026-10-15 | exclude | 语音 token 压缩与 post-hoc 适配训练，不是反馈驱动的 Harness 或多轮 RSI。 |
| [Your Benchmark Is an Empirical Measure Over Difficulty](https://arxiv.org/abs/2610.29927) | 2026-10-21 | exclude | 一般基准难度分布与题目重写，不是自进化系统或 Harness 演化专项评测。 |
| [VibeGame: Prompt-to-Game Development with AI-Native Engine and Self-Evolving Adversarial Agent Team](https://arxiv.org/abs/2610.33106) | 2026-10-22 | harness | 接受项目经无训练蒸馏产生协作 contracts；新项目读取并重新验证，属于可复用 Harness 工作流规则更新。 |
| [A Broader Look into MLLM's Retrieval Heads](https://arxiv.org/abs/2610.32411) | 2026-10-23 | exclude | 优化的是多模态模型 attention heads，属于模型训练；未描述多轮自生成数据/自训练或外部 Harness 修改。 |
| [After One-Click Video: The Inflow of Service-Type Content, the Failure of the Recommendation Pool Mechanism, and the BoLe System](https://arxiv.org/abs/2610.37695) | 2026-10-24 | exclude | 讨论内容供给与推荐机制的产业/平台理论，不是 AI 递归自改进系统。 |
| [Co-Design Bench: Multimodal Collaborative Coding Evaluation for Agentic Models](https://arxiv.org/abs/2610.35138) | 2026-10-26 | exclude | 评测真实用户应用修改能力，在共享固定 harness 下比较模型；不专门研究 Harness 反馈演化。 |
| [SO-101 Bench: Accessible Spatial Manipulation](https://arxiv.org/abs/2610.36420) | 2026-10-27 | exclude | 机器人操控评测并比较固定 Harness/模型选择；当前任务中写控制代码与恢复，不构成跨任务 Harness 演化。 |
| [WorkFactory: Turning Professional Intents into Executable Work for Scalable Agent Training](https://arxiv.org/abs/2610.37161) | 2026-10-27 | other_direction | 探测执行反馈修订任务说明/参考文件，最终生成训练语料；不是 Agent 自身 Harness。是否满足更广义 RSI 的跨任务继承标准仍需第三轮判定。 |
| [WebAnything: From the Wild Web to Scalable Agent Environments](https://arxiv.org/abs/2610.37786) | 2026-10-27 | other_direction | 反馈修补的是可发布网站训练环境；采样与下游评测仍使用固定 Agent harness。环境构建循环是否算广义 RSI 待第三轮确认，不能算 Harness。 |
| [WeVisCut: The Whole Editing Room in One Agent From Narration to Long-Form Video](https://arxiv.org/abs/2610.38352) | 2026-10-28 | exclude | 固定指令/工具/runtime 下训练 9B policy，执行反馈修当前视频状态；多阶段 post-training 不是 Harness 程序自更新，也未证明多轮外层 RSI。 |
| [IntReal: A Real-World Dataset and Benchmark for Multimodal Interleaved Generation](https://arxiv.org/abs/2610.38425) | 2026-10-28 | exclude | 交错图文生成的数据集、指标与模型 post-training，不是 Harness 或递归改进评测。 |
| [AskStream: When and What to Ask Proactively under Uncertainty in Streaming Video Understanding](https://arxiv.org/abs/2610.38678) | 2026-10-28 | exclude | 评测流视频中的 wait/ask/answer 决策，属于普通交互能力基准，不是 Harness 演化。 |
| [Intrinsic Distribution Matching](https://arxiv.org/abs/2610.39633) | 2026-10-29 | exclude | 图像生成分布匹配蒸馏/LoRA，EMA 是训练估计器，不是独立自改进环或 Harness 修改。 |
| [EditAgent: Rethinking Agentic Image Editing](https://arxiv.org/abs/2610.39664) | 2026-10-29 | exclude | 固定工具池/路由/验证记录修订当前图像；训练数据随后单轮 fine-tune 编辑器，不修改可复用 Harness。 |
| [Your LR Schedule May Not Be Principled: Effective Learning Rate Scheduling in Weight-Normalized Training](https://arxiv.org/abs/2610.40362) | 2026-10-29 | exclude | 学习率调度理论及预训练对照，外部固定 schedule 不构成多轮自主修改训练方法或 Harness。 |
| [HairDeck: Animation-Ready Stylized Hair Cards from a Single Image](https://arxiv.org/abs/2610.40599) | 2026-10-29 | exclude | 图像生成可动画发片资产的 diffusion 方法，未研究 Agent 系统或自改进。embodied 仅为邻近主题，不能当 RSI 分类。 |

## VibeGame 的关键限定

纳入依据是会跨项目重用的协作 contracts（角色输入/输出/依赖/验证程序），不是仅复用游戏代码或素材。

主实验没有累计经验；不能将主表提升归为自进化收益。自进化消融让 GPT-6.1-Sol 在 5 个消融集外任务上积累经验，再提供给 GPT-5.6-Luna 做 10 个消融任务，Overall 从 53.45 到 56.37（+2.92）。这不是跨模型家族迁移证据。

Appendix 13 还报告跨游戏类型持续积累经验可能降低性能。24 小时预算相同不代表总 token/search 成本匹配；演化重复次数未知。本次未复现实验，也未验证 GitHub 代码完整发布。

## 证据与后续

44 条证据引文在官方摘要或对应正文段落中逐字匹配；6 篇 HTML 和提取文本的 12 个哈希均通过。逐条来源、章节、哈希、原文和决定边界见 [hf-today-manifest.json](hf-today-manifest.json)。

全部 decision 保持 defer。第三轮重点：VibeGame 规则与实验归因；WorkFactory/WebAnything 的广义 RSI 边界；固定 Harness 与模型训练的区别。

正文来源抓取记录见 [hf-today-sources.json](hf-today-sources.json)；返回 [审核索引](INDEX.md)。
