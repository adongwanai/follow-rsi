# 2026-11-10 独立第三轮复审及分歧补证

38 项最终建议：Harness 范围纳入 6、排除 31、待定 1。正式 decision 仍 defer，由主 agent 依授权与逐项检查落实。0付费调用，无正式库写入。

初稿独立完成时为 8 纳入/30 排除；收到主审对三项边界的质疑后重新查正文，保留初稿与逐项review_history。没有抹去原判断。

- RSI-ESA：由纳入修正为范围外；实证只优化领域调度配置，工具构建是未来方向。
- WAAC：限定typed policy-cache分支纳入；有成功验证准入、跨workflow策略迁移、fusion实际控制后续上下文的证据。
- Where Should Learning Live：由纳入改待定；固定候选选择理论与Harness工件演化的专项界线仍需明确，暂作相关链接。

| ID | 建议 | 理由/范围边界 |
|---|---|---|
| arxiv:2611.09318 | exclude | 补读实证边界后修正：已实现case仅按反馈搜索六维频谱调度配置，预定义领域组件生成外部调度版本；未证明执行LLM Agent自身工具、提示或管理机制被修改。概念架构列出的tool organization与未来工具构建不能当作已实现Harness证据。 |
| arxiv:2611.09454 | include | 只将§7 agent reward-loop作为Harness证据：writer依据任务成功反馈跨轮改写可复用skill document；训练writer或读取LoRA本身不能单独算Harness演化。 |
| arxiv:2611.09701 | borderline | 确实针对语言模型系统的text/parameter配置、反馈选择与历史状态做归因理论，但S1明确只更新预构造候选的selection probabilities，不构造或扩展prompt/adapter。它是Harness演化的相关选择理论，严格核心范围是否足够专项仍有疑问，暂不自动计入Harness。 |
| arxiv:2611.09291 | include | AutoRefine 直接改写部署用judge prompt，执行/工作流结果与teacher可解释筛选提供反馈，独立validation选择保留prompt；修改的是环内验证器。 |
| arxiv:2611.08932 | exclude | ODD+LLM是对prompt/memory/parsing/retry等配置的文档规范与人为multiverse变体比较，未建立反馈驱动Harness持续更新。 |
| arxiv:2611.08865 | include | WAAC保留的不是单纯经历文本：成功验证后将字段级context-retention policies和依赖分析结果写入typed policy cache，后续工作流匹配并转移这些策略，构成上下文管理策略的反馈筛选与保留。 |
| arxiv:2611.09472 | exclude | ENGRAM更新模型权重并选择保留/释放经验记录，固定admission/verification gate不随反馈改写；不得因记忆图和skill标签就称Harness共演化。 |
| arxiv:2611.09892 | include | 只纳AMP1+学习部分：二值任务结果驱动反思，Agent持续修订memory和可导入调用的Python工具库，并跨任务携带。仅AMP1固定零样本框架不算RSI，普通notes也不足以成立。 |
| arxiv:2611.09030 | exclude | 该controlled study以固定self-learning harness生成和修订外部机器人task-policy/技能实现；评测是robot policy improvement，未证明跨任务更新Agent自己的Harness。 |
| arxiv:2611.09348 | include | 专项追踪SkillOpt反馈如何经reflection/edit/selection变成持久Skill后门，并在分离触发/clean题测试。研究对象就是可复用Harness skill的反馈演化，因此可纳专项安全评测。 |
| arxiv:2611.08763 | exclude | CrowdDirector将用户自然语言转成场景directive，运行时更新人群场景；graph policy离线训练，未由执行反馈改写持久Harness。 |
| arxiv:2611.08264 | exclude | 3D生成模型方法，与RSI无关。 |
| arxiv:2611.03953 | exclude | 两组可训练参数不能叫Harness共演化。 |
| arxiv:2611.06856 | exclude | LongBanana评测长参考图像合成、固定agent harness与任务内request/image revision，不是Harness持久自进化专项。 |
| arxiv:2611.08175 | exclude | PCBRouteAgent通过执行反馈改当前PCB的routing guides并保留已布线部分，改的是任务产物，不是跨任务可复用Agent Harness。 |
| arxiv:2611.06808 | exclude | 通用模型知识/泄漏评测，不是Harness RSI专项。 |
| arxiv:2611.01182 | exclude | 推理算子优化不是Harness自进化。 |
| arxiv:2611.07025 | exclude | 模型内部KV压缩不是反馈演化的外部上下文管理机制。 |
| arxiv:2611.09017 | exclude | coding agent benchmark评的是3D产物，不是Harness演化。 |
| arxiv:2611.08290 | exclude | 自动压缩模型不能仅因自动化纳Harness RSI。 |
| arxiv:2611.09634 | exclude | 冻结base不代表Harness：被训练的是adapter参数。 |
| arxiv:2611.09891 | include | CPU-ARC 根据运行与judge反馈反复重写语义函数，合格函数注册到系统级缓存供后续推理复用；这是可执行工具组件的持久改变。 |
| arxiv:2611.02775 | exclude | 理论与方法性贡献没有新增实证，亦非Harness RSI专项。 |
| arxiv:2610.41711 | exclude | 网络宽度结构研究，非Agent RSI。 |
| arxiv:2611.09113 | exclude | AgentDrift/ADB测试固定模型与框架的执行授权偏移，SERS迭代生成评测任务；不是Harness自改、学习后回归或持久更新的专项安全评测。 |
| arxiv:2611.01362 | exclude | 科学检索测量，不是Harness RSI。 |
| arxiv:2610.36896 | exclude | 模型训练和外部照片编辑产物，与Harness RSI无关。 |
| arxiv:2611.08647 | exclude | IWIBench可归一般模型权重编辑评测，不能因为编辑器是Agent就收入Harness。 |
| arxiv:2611.08179 | exclude | teacher feedback是训练监督，非Harness演化。 |
| arxiv:2611.04720 | exclude | 推荐系统训练不是Harness RSI。 |
| arxiv:2611.09055 | exclude | 3D模型与编辑方法，不是Harness RSI。 |
| arxiv:2611.00448 | exclude | evolve为动态系统演化，非recursive self-improvement。 |
| arxiv:2611.06844 | exclude | 模型内部动态路径不等Harness演化。 |
| arxiv:2611.07723 | exclude | scaffolding为蛋白结构语义，不是Harness RSI。 |
| post:https://openai.com/index/chatgpt-enterprise-aws-marketplace | exclude | 商业发布，与Harness RSI无关。 |
| post:https://openai.com/index/control-room | exclude | 安全基础设施说明，不是Harness演化研究。 |
| post:https://openai.com/index/coderabbit-codex-daybreak | exclude | 企业案例不能作为Harness自进化证据；公司自报生产力数字未独立验证。 |
| post:https://openai.com/index/kuken | exclude | 工业搜索案例，与Harness RSI无关。 |

完整原文、paragraph定位、文件哈希、真实日期和数字边界见independent-review.json。审查不等于论文实验复现或全部数字复算。
