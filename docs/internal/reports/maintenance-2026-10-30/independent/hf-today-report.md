# 2026-10-30 HF 条目独立第三轮

16 篇官方摘要、6 篇正文相关章节；16 篇标题、摘要、版本及原始日期均已对齐官方 Atom。15 篇新增，VibeGame 为已有条目。正式决定全部 defer。

建议 1 篇按 Harness 组件候选提交 owner（VibeGame），2 篇仅作相关环境/数据基础设施线索，其余 13 篇排除出 Harness 专题。WorkFactory/WebAnything 的广义 RSI 身份尚无充分证据，不能因存在环境 repair 与下游 SFT 就算递归自改进。

HF 上榜日期与论文原日期分别记录；本期原始发表日横跨 10 月 15 日至 29 日。未认证实验数字，未复现原始运行。

独立性限制：未打开主审报告，但收到主审主动发送的分类摘要和 VibeGame 限制提示，因此不声称 HF 子集完全盲审。以下判断均重新对照原始来源。

|论文|原始发表日|Harness 建议|依据与边界|
|---|---|---|---|
|[Your Benchmark Is an Empirical Measure Over Difficulty](https://arxiv.org/abs/2610.29927)|2026-10-21|exclude|研究难度分布与题目覆盖；BenchFill 改写评测题目，不是外部 Harness 的反馈演化评测。|
|[VibeGame: Prompt-to-Game Development with AI-Native Engine and Self-Evolving Adversarial Agent Team](https://arxiv.org/abs/2610.33106)|2026-10-22|include_suggestion|contract 文档把角色输入输出、依赖与验证规则改成面向后续项目的可复用工作流；它由已验收项目蒸馏并初始化未来运行，满足程序外围策略文件的更新与保留。游戏 skeleton 和普通模块本身仍是任务产物，不能全部算 Harness。|
|[A Broader Look into MLLM's Retrieval Heads](https://arxiv.org/abs/2610.32411)|2026-10-23|exclude|对象为模型注意力头的训练和消融；不是外部执行程序更新。|
|[Co-Design Bench: Multimodal Collaborative Coding Evaluation for Agentic Models](https://arxiv.org/abs/2610.35138)|2026-10-26|exclude|固定共享 Harness 下评测应用修订任务；judge-then-refute 是评测协议，未研究 Harness 版本演化。|
|[WorkFactory: Turning Professional Intents into Executable Work for Scalable Agent Training](https://arxiv.org/abs/2610.37161)|2026-10-27|exclude|反馈修复的是任务资料与环境依赖，随后收集教师轨迹做 SFT。不是 agent 自身 Harness 的更新；也未展示训练后模型再反哺构造的递归能力闭环，不能直接确认为广义 RSI。|
|[WeVisCut: The Whole Editing Room in One Agent From Narration to Long-Form Video](https://arxiv.org/abs/2610.38352)|2026-10-28|exclude|工具反馈驱动当前视频制作与恢复；SFT/RFT/OPD/RL 更新模型策略，生产 Harness 没有被保留式改写。|
|[IntReal: A Real-World Dataset and Benchmark for Multimodal Interleaved Generation](https://arxiv.org/abs/2610.38425)|2026-10-28|exclude|多模态生成数据集与评测，并通过训练提升模型；无 Harness 反馈演化研究对象。|
|[WebAnything: From the Wild Web to Scalable Agent Environments](https://arxiv.org/abs/2610.37786)|2026-10-27|exclude|被修复和保留的是训练用网站环境。执行 Agent 使用固定 Harness；下游 SFT 效用实验不构成更新模型反哺下一轮构造的证据，广义 RSI 仍待证。|
|[AskStream: When and What to Ask Proactively under Uncertainty in Streaming Video Understanding](https://arxiv.org/abs/2610.38678)|2026-10-28|exclude|评测模型何时主动问问题；无外部程序被执行反馈修改并保留。|
|[HairDeck: Animation-Ready Stylized Hair Cards from a Single Image](https://arxiv.org/abs/2610.40599)|2026-10-29|exclude|图像到可动画发片资产生成，改进对象为生成模型与任务产物，不是 Harness RSI。|
|[EditAgent: Rethinking Agentic Image Editing](https://arxiv.org/abs/2610.39664)|2026-10-29|exclude|固定路由/并行候选/裁判协议按反馈重试当前图像；保留的是编辑图与要求，未改写并复用 Agent 自身程序。收集验收会话后的微调属于模型训练。|
|[CoSTA: Compressed Speech Token Adaptation for Efficient Spoken Dialogue Models](https://arxiv.org/abs/2610.21143)|2026-10-15|exclude|压缩词表扩展与发音/对话适配，未呈现外部程序的反馈演化。|
|[After One-Click Video: The Inflow of Service-Type Content, the Failure of the Recommendation Pool Mechanism, and the BoLe System](https://arxiv.org/abs/2610.37695)|2026-10-24|exclude|讨论内容供给与推荐池失灵的社会技术模型，不是 Agent 自改程序研究。|
|[Your LR Schedule May Not Be Principled: Effective Learning Rate Scheduling in Weight-Normalized Training](https://arxiv.org/abs/2610.40362)|2026-10-29|exclude|研究预训练学习率调度与权重训练动力学；不是可复用 Harness 的反馈改写。|
|[Intrinsic Distribution Matching](https://arxiv.org/abs/2610.39633)|2026-10-29|exclude|生成模型的全参数或 LoRA 训练与蒸馏损失设计，不属于外部 Harness。|
|[SO-101 Bench: Accessible Spatial Manipulation](https://arxiv.org/abs/2610.36420)|2026-10-27|exclude|评测机器人操作及多个固定配置的 Harness/模型消融；code-as-policy 为任务执行形式，未给出自身程序反馈演化与保留的实验。|

已校验 33 条连续原文引句及 7 个原始来源文件。逐条哈希、正文路径、局限和后续动作见 hf-today-report.json。
