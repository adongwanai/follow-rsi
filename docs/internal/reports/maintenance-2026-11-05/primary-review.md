# 11/05 主审范围核验

55 篇当前新增/补记推荐日 HF 摘要逐篇初筛，4 篇新 arXiv 条目另列。11 篇另读官方正文相关方法与实验边界，EvoTeam复核当前v2选段，MoLRSI复用哈希未变的v2机制证据。不把摘要筛选称为全文审核，不复算全部实验数字。

所有意见是可续跑建议，正式决定和发布门不变。付费模型调用为 0；当前质量召回 24/28 低于 0.90。

|论文|来源推荐日|建议|理由|
|---|---|---|---|
|[GameVerse: A Minute-Scale Gameplay Dataset for Long-Horizon Interactive World Modeling](https://arxiv.org/abs/2610.37257)|2026-11-05|exclude|GameVerse 为交互世界模型提供长视频训练数据；更新训练数据/模型能力，没有反馈改写可复用外部 Harness 的机制。|
|[Solv3R: 3D Looped Transformer as a Multi-view Solver](https://arxiv.org/abs/2611.02857)|2026-11-05|exclude|Solv3R 训练循环几何求解算子，更新当前三维重建状态；模型内部迭代与缓存不等于外部 Harness 跨任务改写。|
|[Human-to-Robot Transfer via Bridging Representation and Action Space in VLAs](https://arxiv.org/abs/2611.04391)|2026-11-05|exclude|H2RB 通过人机协同数据训练 VLA 表征与动作空间；改进对象为策略权重，不是可保留的 Harness 工件。|
|[SpecOPD: Branch-Parallel On-Policy Distillation for Speculative Decoding](https://arxiv.org/abs/2611.02846)|2026-11-05|exclude|SpecOPD 训练 speculative decoding 的 drafter，接受长度与采样加速属于模型蒸馏/推理系统，不是 Harness 自进化。|
|[VeriSpoof: Beyond Real or Fake with One Audio LLM](https://arxiv.org/abs/2611.04634)|2026-11-05|exclude|VeriSpoof 训练音频模型处理检测与归因任务；grounded rationales 可验证不意味着外部验证器自修改。|
|[Route Anything: A Study of Model and Policy Routing for General-Purpose AI Systems](https://arxiv.org/abs/2611.05275)|2026-11-04|exclude|路由理论与监督学习的router/候选选择研究，没有按执行反馈持续改写外部路由程序的闭环。|
|[Words Caught in the Heart: Simulating Person-Specific Expression for Self-Opaque Clients in Psychotherapy](https://arxiv.org/abs/2611.00617)|2026-11-04|exclude|Pandora 更新心理和关系状态以生成单次会话表达；这些是模拟器状态/内容，未改写并保留系统自身规则。|
|[Think Less, Locally: Local Preference Learning for Reasoning Compression](https://arxiv.org/abs/2611.04814)|2026-11-04|exclude|LoCo 对模型自生成轨迹做 DPO 偏好训练；优化对象为推理模型权重。|
|[MoviEdit: Long-form Multi-Shot Video Editing Made Easy](https://arxiv.org/abs/2611.02737)|2026-11-04|exclude|MoviEdit 合成视频编辑数据并训练生成架构；未涉及 Agent Harness 反馈演化。|
|[Behind Video Generation: Observations and Insights on Multimodal Understanding from Kling](https://arxiv.org/abs/2611.04916)|2026-11-04|exclude|Kling 报告的改进是模型数据、conditioning、RL及reward modeling；agentic prompt enhancement服务当前视频，不等于持续改写Harness。|
|[DreamX: Video Diffusion Model is a Universal Latent Action Learner](https://arxiv.org/abs/2611.05377)|2026-11-04|exclude|DreamX 从视频扩散模型学习潜动作表示；共享动作接口是训练所得表征，不是外部程序持续演化。|
|[Factorized MLLM Embeddings for Composed Image Retrieval](https://arxiv.org/abs/2611.05193)|2026-11-04|exclude|FactEmbed 优化 MLLM 检索embedding与训练损失，属于模型表征学习。|
|[RoboColosseum: Evaluating Physical Intelligence at Scale In-The-Wild](https://arxiv.org/abs/2611.02497)|2026-11-04|exclude|RoboColosseum 评测机器人政策和微调适应；研究对象为一般具身能力，不是Harness演化专项评测。|
|[Axion 1.0: Open Agent Foundation Models, Simplified](https://arxiv.org/abs/2611.03233)|2026-11-04|exclude|Axion 三阶段 SFT/RL 训练基础模型；开放工具提示与训练配方不构成这些外部工件的反馈自改进。|
|[ToolSpace: Scaling Tool-Centric Environment Synthesis for Long-Horizon Agents](https://arxiv.org/abs/2611.05036)|2026-11-04|exclude|ToolSpace 从执行轨迹合成训练环境、任务和工具组合图，更新训练资源及权重；未说明Agent自身Harness持续改写。|
|[YANAMI: A Large-Scale Multimodal Dataset and Benchmark for Multiturn Stateful Interaction](https://arxiv.org/abs/2611.05280)|2026-11-04|exclude|YANAMI 更新多模态会话状态并用数据微调模型；状态变化和视觉生成不等于Harness规则演化。|
|[VidUEU-Agent: A Data-Curation Agent for Multimodal Understanding, Editing, and Unified Tasks](https://arxiv.org/abs/2611.04418)|2026-11-04|exclude|VidUEU 根据下游训练反馈迭代数据分布，主要对象是instruction数据，不是自身可复用Harness。|
|[EvoTeam: Multi-Agent Collaboration via Evolving Teams](https://arxiv.org/abs/2610.39813)|2026-11-04|include|按执行经验修改团队编制、交互规则和技能，并明确带入后续任务；本轮新增真实11/04推荐日，原first_seen和旧决定保留。|
|[WebHarbor: Docking Real Websites for Evolving GUI Agent Environments](https://arxiv.org/abs/2611.03634)|2026-11-04|exclude|WebHarbor 由人机协作扩展网站环境和任务，用于评测/RL；演化对象是环境，不是执行Agent的Harness。|
|[MoLRSI: A Recursive Self-Improving AI agent for Molecular Discovery](https://arxiv.org/abs/2610.39714)|2026-11-04|borderline|辅助技能执行修复、验证后保留确有正证；主循环与对照隔离的是科研工作流及经验记忆，尚缺实测的跨任务技能版本/消费链，保持待补。|
|[SpecPilot: Autonomous Algorithm Discovery and Systems Optimization for Speculative Decoding](https://arxiv.org/abs/2611.02501)|2026-11-04|exclude|反馈优化的是外部 speculative decoding 算法和服务系统；保存可重放的优化代码与记忆不等于 Agent 自身 Harness 被迭代修改。|
|[ParetoSaddler: Pareto-Guided Optimization of Agent Harnesses for Quality and Cost](https://arxiv.org/abs/2611.02079)|2026-11-04|include|固定执行模型，以执行轨迹和质量/成本反馈修改提示、工具、中间件及控制流；获准候选保留到档案并继续迭代。|
|[Mage-VL-Cowork: A Full Training Recipe to Learn Hybrid Computer Use From Evolved Harnesses](https://arxiv.org/abs/2610.40747)|2026-11-04|include|教师权重固定，authoring agent 按任务成功率、token成本和执行反馈修订完整教师 Harness；选定后固定，用于多轮数据生成与学生训练。|
|["Shall We Approve?" Consequence-Aware Approval for Autonomous Coding Agents](https://arxiv.org/abs/2610.40753)|2026-11-04|exclude|Caper 在快照沙箱执行命令、批准或回滚，反馈用于当前提案；摘要未显示审批规则自身按反馈改写并跨任务继承。|
|[Recursa: Toward Recursively Self-Improving Foundation Model Systems](https://arxiv.org/abs/2611.04035)|2026-11-04|include|运行反馈驱动指令和程序技能的诊断、编辑与验证，通过回归检查后保留到后续任务；属于可复用 Harness 组件。|
|[Every Token Needs Its Own Teacher: Multi-teacher Adaptive On-policy Self-distillation](https://arxiv.org/abs/2610.40574)|2026-11-04|exclude|MTA-OPSD 在训练时选择不同teacher监督token，属于模型权重自蒸馏。|
|[FlowTranslator: Training-Free In-Image Machine Translation with Flow-Based Editing](https://arxiv.org/abs/2611.04303)|2026-11-04|exclude|FlowTranslator 用固定轨迹控制做图像翻译；训练免费不等于Harness通过反馈持续演化。|
|[Are Frontier VLM Agents Ready to Be Robot Generalists? An Empirical Study with the Embodied Agent Arena](https://arxiv.org/abs/2610.00854)|2026-11-04|exclude|Embodied Agent Arena 用最小固定Harness评估VLM具身任务；同次执行恢复和self-review不算Harness自改进专项评测。|
|[You don't need long context](https://arxiv.org/abs/2611.05306)|2026-11-04|exclude|固定压缩策略和当前上下文状态的实验，未给出根据执行反馈持久改写压缩程序的机制。|
|[PrimeSim: A Generalist World Model Simulator from Large-Scale Cross-Embodiment Demonstrations](https://arxiv.org/abs/2611.04870)|2026-11-04|exclude|PrimeSim 训练世界模型和时序记忆，更新网络及模拟状态，不是Agent外部程序。|
|[Can AI Reviewers See Your Efforts to Improve Your Paper? A Large-Scale Study of Paper Revision Trajectories](https://arxiv.org/abs/2611.02244)|2026-11-04|exclude|PaperTrajectory 研究AI审稿器对论文修改的打分；迭代对象为论文外部产物，评测非Harness演化专项。|
|[Near-Zero Token Embeddings Silently Stall Training in Gated Sequence Models](https://arxiv.org/abs/2611.04449)|2026-11-04|exclude|Near-Zero Token Embeddings 研究模型训练数值问题和梯度修复，非Harness演化。|
|[Adversarial Speculative Reasoning Improves Long Horizon Agents](https://arxiv.org/abs/2611.05345)|2026-11-04|exclude|以反向DPO训练drafter；target模型和verification rule不变，改进对象是draft模型权重，没有外部Harness持续自改。|
|[Dory1.0-4B: A Looped Normalized-GPT](https://arxiv.org/abs/2611.03998)|2026-11-04|exclude|Dory 为循环模型预训练和后训练；latent loop是网络结构，不是外部Harness的反馈更新。|
|[RoboTryOn: Synthesizing Dexterous Robot Demonstrations from Human Videos via Virtual Try-On](https://arxiv.org/abs/2611.05163)|2026-11-04|exclude|RoboTryOn 合成机器人示范并训练政策；更新数据与策略权重。|
|[Switch-SWE: Do Coding Agents Hold Focus When Switching Between Unfinished Tasks?](https://arxiv.org/abs/2611.02017)|2026-11-04|exclude|Switch-SWE 评测未完成任务切换并提出固定context管理模块；摘要无模块自身反馈改写/持久继承，属于一般代理评测。|
|[LOLPlay: Benchmarking Real-Time Visual Agents in League of Legends](https://arxiv.org/abs/2611.03685)|2026-11-04|exclude|LOLPlay 测实时视觉Agent能力和reasoning effort，未评测Harness自进化机制。|
|[SeMo3D: Unifying 3D Generation, Editing, and Completion via Selective Modeling](https://arxiv.org/abs/2611.02568)|2026-11-04|exclude|SeMo3D 训练三维资产生成编辑模型；编辑产物是任务对象，作为工具使用不等于工具自身演化。|
|[BEND 2.0: Benchmarking the Capabilities Needed to Design DNA](https://arxiv.org/abs/2611.03806)|2026-11-04|exclude|BEND 2.0 评测基因模型及序列设计，非Harness演化专项。|
|[Muon Makes the First Mixture-of-Experts Layer Harder to Balance](https://arxiv.org/abs/2610.37914)|2026-11-04|exclude|Muon 研究MoE网络优化器和路由器内部负载，非外部Harness。|
|[Every Pixel Is an Option: A System One Model for Medical Ultrasound Biometry](https://arxiv.org/abs/2611.03360)|2026-11-04|exclude|Kev-Bio 训练超声视觉语言模型的landmark定位，非Agent程序演化。|
|[Do We Need an LLM to Know Why Sources Conflict? Decision Models for Knowledge-Conflict Typing in RAG](https://arxiv.org/abs/2610.36915)|2026-11-04|exclude|Knowledge-Conflict Typing 比较分类器和固定级联路由配置；没有持续反馈改写Agent程序，属于RAG分类/路由分析。|
|[Is Your Long-Horizon Benchmark Really Deep? Measuring and Synthesizing Depth in Terminal Tasks](https://arxiv.org/abs/2611.01927)|2026-11-04|exclude|DEPTH 评测和合成终端任务深度并训练模型；当前生成任务属于外部训练数据，非Harness演化。|
|[What We Keep of What We Forget: Replacement Operators and Routing Semantics in Training-Free MoE Expert Pruning](https://arxiv.org/abs/2610.41366)|2026-11-04|exclude|MoE pruning 比较专家剪枝与替换算子，模型内部路由和压缩非Harness。|
|[Is Forgetting Unified? Exploring Concept Unlearning in Unified Multimodal Models](https://arxiv.org/abs/2611.04467)|2026-11-04|exclude|UniForget 对多模态模型概念去学习，更新模型权重并评测遗忘，非Harness专项。|
|[Where to Learn and How Far to Roll Out: Efficient Adaptive Training for GUI Agents](https://arxiv.org/abs/2610.39251)|2026-11-04|exclude|Adaptive GUI training 用中间检查点分配RL训练预算；可复用checkpoint是环境状态，学习对象为政策权重。|
|[Cross-Prompt Reuse of Entity-Replacement Responses](https://arxiv.org/abs/2611.00352)|2026-11-04|exclude|Cross-Prompt Reuse 注入隐藏态研究事实替换的迁移；模型冻结不意味着外部可复用程序被改写。|
|[SphereFlow: Missing Modality Imputation via Geometric Transport on Hypersphere](https://arxiv.org/abs/2611.04414)|2026-11-04|exclude|SphereFlow 训练跨模态插补传输/解码模型，非Harness。|
|[Kierston & KierstonBench: Simulation of Allentown, PA and Evaluation of Language Models in Crime Investigation and Surveillance Tasks](https://arxiv.org/abs/2611.04785)|2026-11-04|exclude|KierstonBench 评测案件调查能力，环境及记录接口固定，非Harness演化专项。|
|[GigaSpeech 3: Scaling Multi-Dialect Arabic Speech Recognition with Weakly Labeled Data](https://arxiv.org/abs/2611.02476)|2026-11-04|exclude|GigaSpeech 迭代弱标签数据和语音模型权重，属于模型/数据自训练。|
|[Auto-Research Agent on MSA Organization to Improve Protein-Protein Complex Structure Prediction](https://arxiv.org/abs/2611.03183)|2026-11-04|exclude|Auto-Research MSA 按目标反馈修改蛋白科研输入和配对，属于当前科学任务产物；未显示Agent自身通用程序跨任务改写。|
|[Going Deeper With Memories](https://arxiv.org/abs/2611.05255)|2026-11-04|exclude|DeepMem 为字节语言模型内部快权重记忆架构；内部state不是Agent外部memory-policy工件。|
|[Enhancing Stock Market Information Retrieval with Retrieval-Augmented Generation](https://arxiv.org/abs/2611.03747)|2026-11-04|exclude|Stock Market RAG 为金融检索与回答系统，未提供反馈自改外部Harness的机制。|
|[Say the Same, Act Differently: Diagnosing and Steering Text-Action Divergence in Reasoning VLAs](https://arxiv.org/abs/2611.04166)|2026-11-04|exclude|TNAS 诊断VLA隐藏态与动作攻击，修改输入扰动而非Harness；安全评测非演化专项。|
|[FinForesight: A Diagnostic Backtesting Benchmark for Deep Research Systems in Financial Forecasting](https://arxiv.org/abs/2611.01621)|2026-11-04|exclude|FinForesight 评测金融深度研究与检索时间控制，harness-compatible不等于评测Harness自身反馈演化。|
|[HarnessFlow: MCTS-Guided Harness Optimization for LLM Agents](https://arxiv.org/abs/2611.06254)|arXiv，未观察到HF成员身份|include|MCTS 选择父版本，coding agent 按验证分数和执行记录修改完整可执行 Harness；代码与父子关系保留在树和经验档案中供后续迭代。|
|[EnzymeRSI: A dual-loop recursive self-improvement system for enzyme design](https://arxiv.org/abs/2611.06321)|arXiv，未观察到HF成员身份|include|外层按执行失败和成对评估修改版本化的技能、MCP访问、subagents与系统提示；采用版本需记录下一轮真实消费，失败回滚。|
|[Reglos: A Self-Evolving Personal Memory Agent with Recursive Self-Improvement](https://arxiv.org/abs/2611.06049)|arXiv，未观察到HF成员身份|include|外层 coding agent 按失败轨迹修改记忆检索、过滤排序和上下文组织的程序，经独立critic与固定评测筛选；跨用户持续部署该程序。|
|[EvoGuard: Mitigating Degradation in Online Skill Evolution](https://arxiv.org/abs/2611.06444)|arXiv，未观察到HF成员身份|include|每项任务后按轨迹重写可复用技能，固定selector选择是否替换，下一任务继续消费同family技能；在线executor/generator/selector都不训练。|

详细原文、哈希、版本差异、分类理由和实验边界见 [机器可读逐项报告](primary-review.json)。
