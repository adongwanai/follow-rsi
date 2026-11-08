# 2026-11-04 HF 主审 B

所审为 HF **11/03 推荐榜**，在 11/04 抓取；不改论文原日期。25 条中建议 include 3、exclude 22。正式 decision 全部 defer，没有接受/发布。

- 新正例：NorthCUA（有反馈驱动、独立验证、跨后续任务可用的操作技能）；Continual Harness Evolution（Harness 专项遗忘评测）。
- 复用正例：TinyAstral，摘要严格匹配当前规范记录，复用 11/02 正文和独立审查，不重复计新增。
- 正文排除边界：TAL 的 tutorialbook 与生成器 history 是知识/案例内容更新；SIMIT 修订合成数据并适配上下文或权重，synthesizer 本身固定。
- 其余 20 条只作 HF 摘要范围初筛，未声称逐篇读完全文或复算实验。

|ID|建议|层级|理由|
|---|---|---|---|
|arxiv:2611.02102|include|official_primary_body_scope_review|NorthCUA 的 skill-guided RSI 将失败轨迹转为可执行文字流程，由独立 agent 冻结测试后准入，失败会修订重测，技能持续可用并明确供满足适用条件的后续任务使用。因此 Harness 纳入理由成立。模型训练是后续独立阶段；仅保存 milestone/任务记忆不作为本次纳入依据，也不把整个系统称作权重冻结。|
|arxiv:2611.02332|exclude|hf_returned_paper_abstract_only|LeanGuard 的 Lean 策略和判定程序由作者预先定义；反馈/证明搜索修复的是本次被拒绝的工具调用。摘要未给出按执行反馈改写并跨任务保留 guardrail、策略或控制程序的机制，属于静态运行时安全。|
|arxiv:2610.37826|exclude|hf_returned_paper_abstract_only|DeFT-RAG 改进多跳检索流程，并缓存可复用 QA 答案；新增的是事实/答案内容，摘要未显示反馈驱动修改检索策略、工具或工作流并保留新版本。|
|arxiv:2610.41574|exclude|hf_returned_paper_abstract_only|BYOD 用 LoRA 训练将 AR 模型转换为扩散模型；即使 base 权重冻结，主要更新对象仍是可训练适配器权重，并非 Agent 外部 Harness。|
|arxiv:2611.03526|exclude|hf_returned_paper_abstract_only|LoL 学习动态 transformer 层顺序，属于模型内部结构与路由；不是修改冻结模型周围的工具、控制流或提示机制。|
|arxiv:2610.40293|exclude|hf_returned_paper_abstract_only|MAServeBench 评测多 Agent 协作造成的 serving 工作负载和硬件瓶颈；摘要没有评测 Harness 自进化方法或其持续改写，不能因有多 Agent/benchmark 就纳入专项。|
|arxiv:2610.38623|exclude|hf_returned_paper_abstract_only|CPRC 给冻结骨干附加并训练 residual network，研究跨 querying primitive 一致性；主要优化对象是网络参数，没有 Harness 工件按反馈迭代保留的证据。|
|arxiv:2610.35219|exclude|hf_returned_paper_abstract_only|MACR 依置信度在同一次求解中转移推理所有权，是预设动态协作算法；摘要没有显示协作规则自身被执行反馈改写并跨任务继承。|
|arxiv:2610.38637|exclude|hf_returned_paper_abstract_only|TESD 用环境奖励优化 teacher/student 的训练目标和模型能力；更新对象是模型训练，不是外部 Harness 的可复用程序。|
|arxiv:2610.41296|exclude|hf_returned_paper_abstract_only|研究辅助轨迹偏好用于 online adaptation 和 weighted SFT；改变模型权重/训练监督，未描述可持续更新的外部 Agent 程序。|
|arxiv:2611.03097|exclude|hf_returned_paper_abstract_only|DR Pixel 是页面图像检索与推理系统，并以 counterfactual credit reweighting 训练模型；摘要没有基于轨迹修改并保留外部 Harness 新版本的闭环。|
|arxiv:2611.01460|exclude|official_primary_body_boundary_review|TAL 迭代编辑的是教程章节知识内容，按题库答题反馈接受版本；TOC 选择和 read/write 规则作为固定程序使用。还专门核查了正文的 G_phi reflective revision：附录 A.2 明确它只积累既往题目、教学事件与答案结果到外部 history/context，未给出对通用出题/检索/记忆管理机制本身的可保留改写。按当前证据建议归经验与记忆，不计 Harness。|
|arxiv:2611.00053|exclude|official_primary_body_boundary_review|SIMIT 使用既定、可扩展的 rendering skill library 生成合成图文训练样本；反馈修复的是数据/图像，学习结果进入 few-shot 上下文或 LoRA 权重。正文将 solver/synthesizer 联合更新列为未来工作，并说明现阶段 synthesizer 固定；没有显示技能规范、backend 或通用决策规则自己按反馈演化。因此不属 Harness，归数据/模型权重与上下文适应。|
|arxiv:2610.39278|exclude|hf_returned_paper_abstract_only|WorldFlow 对视频与 3D 轨迹做联合预训练和流匹配，目标是世界模型权重；不是 Agent 外部机制自进化。|
|arxiv:2610.39639|exclude|hf_returned_paper_abstract_only|BedBench 诊断 VLM 的 3D 推理准确性、一致性与视觉依赖，并尝试 fine-tuning；评测对象不是 Harness 演化。|
|arxiv:2611.03219|include|official_primary_body_scope_review|论文直接研究冻结模型上的 Harness 跨数据集持续演化与遗忘。AHE/Meta-Harness 按执行轨迹改写系统提示、agent执行逻辑和工具，保留最佳 Harness 后转到另一类任务继续演化，并分析 code diff/轨迹中的验证、工作流和预算冲突，属于 Harness 专项评测。|
|arxiv:2610.27815|exclude|hf_returned_paper_abstract_only|ProVe 微调大模型成为 proposer，并以 verifier 做加速解码；对象是模型训练及固定解码算法，没有可复用 Agent Harness 更新。|
|arxiv:2611.02782|exclude|hf_returned_paper_abstract_only|History Forcing 是视频扩散模型 on-policy distillation，利用历史条件修正蒸馏目标；历史状态不等于跨任务 Harness 改写。|
|arxiv:2610.32878|exclude|hf_returned_paper_abstract_only|LEMS/KFAC-SVD 搜索模型压缩秩配置并优化分解质量，属于模型压缩/结构；未给出外部 Agent 控制程序的反馈演化。|
|arxiv:2611.02928|exclude|hf_returned_paper_abstract_only|EduVideo2Code 根据执行验证修复的是为用户生成的虚拟实验页面，属于外部任务产物；摘要没有把这些修订沉淀为系统自身可复用 Harness。|
|arxiv:2610.41216|include|reused_unchanged_abstract_prior_primary_and_independent_review|Stage 1 冻结 teacher 权重，由执行轨迹定位失败并修改工具、返回协议、感知和恢复组件；候选经预注册配对门控后进入可复用主线版本。Stage 2 才训练小模型，不能把后阶段蒸馏误当成第一阶段没有 Harness 演化。|
|arxiv:2610.41994|exclude|hf_returned_paper_abstract_only|DAMI 初始化线性注意力的记忆门控参数；这是模型内部状态/参数设计，不是 Agent 的外部记忆管理机制自修改。|
|arxiv:2611.03393|exclude|hf_returned_paper_abstract_only|TaoMate-FVSR 训练音频引导的视频修复模型，处理生成视频中的脸部细节；没有 Agent Harness 自进化机制。|
|arxiv:2610.38252|exclude|hf_returned_paper_abstract_only|音乐音频生成综述覆盖生成模型、训练、采样和评测；研究对象不是 Harness 演化方法/专项评测理论。|
|arxiv:2611.00074|exclude|hf_returned_paper_abstract_only|研究人脸图像质量作为攻击检测分数及跨数据集表现；没有 Agent 自改提示、工具、控制流或更新机制。|

所有正文引句已验证为官方 HTML 归一化段落的精确子串；完整 URL、段落 ID、原响应与抽取文件 SHA256 在 JSON 中。新正例沿用 owner 的条件授权，仍需独立复核、摘要与数字校验及质量闸门。尤其 Continual 的 94.0% 来自抽样子集，不能当成完整 SWE-bench 的结果；未证明独立 heldout。

子类复核：NorthCUA = harness/component（技能组件，另标 model_weights）；Continual = evaluation_benchmark + harness/generalize。初稿过宽/不存在的子类已纠正，理由写在 JSON。
