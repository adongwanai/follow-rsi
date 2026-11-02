# 37 篇逐项建议

时间按首次提交日期正序；推荐日期、更新日期与审查日期分开保留。全部 `defer`。

| 首次发表 | ID / 论文 | HF 推荐 | 建议 | 理由 |
|---|---|---|---|---|
| 2026-09-05 | [2609.05881 · Broken on Arrival: Non-Functional Quantized LLM Artifacts in Public Model Registries and How to Catch Them](https://arxiv.org/abs/2609.05881) | 2026-10-30 | exclude / evaluation_benchmark | 评估公开量化权重文件的功能损坏；没有系统根据反馈修订并继承自身 Harness 的机制。 |
| 2026-10-16 | [2610.22990 · PersonaCUABench: Benchmarking Computer-Use Agents Serving Diverse Personas](https://arxiv.org/abs/2610.22990) | 未从本次 HF 榜核实 | exclude / evaluation_benchmark | 固定任务与用户画像条件下评估电脑使用代理；研究的是用户需求与任务完成度，不是 Harness 演化。 |
| 2026-10-16 | [2610.23656 · ABF-Bench: A Verifiable Benchmark for Agentic Blockchain Forensics](https://arxiv.org/abs/2610.23656) | 2026-10-30 | exclude / evaluation_benchmark | ABF 是人工设计的固定取证 Harness；working memory 记录当前调查进度，没有反馈驱动的跨任务程序更新。 |
| 2026-10-18 | [2610.25276 · Holo4D: Holistic 4D Reconstruction as Geometric Control for Video Diffusion](https://arxiv.org/abs/2610.25276) | 2026-10-30 | exclude / ai4ai | 重建场景轨迹作为视频生成条件；改变的是外部场景和输出，不是可继承的代理 Harness。 |
| 2026-10-19 | [2610.27100 · LOB-Impact Benchmark: Emergent Market Impact in Generative Limit Order Book Models](https://arxiv.org/abs/2610.27100) | 未从本次 HF 榜核实 | exclude / evaluation_benchmark | 评估订单簿生成模型的市场冲击，未研究递归改进或 Harness 演化。 |
| 2026-10-25 | [2610.34298 · Matched Capabilities, Different Behaviors: A Controlled Study of MCP and CLI Interfaces for Language Agents](https://arxiv.org/abs/2610.34298) | 2026-10-30 | exclude / evaluation_benchmark | DART 修复当前动作的接口表达；正文明确公共策略和消息顺序保持固定，没有保留到后续任务的 Harness 新版本。 |
| 2026-10-27 | [2610.36671 · Look Only When Needed: Certificate-Guided Visual Routing for Efficient Diffusion VLMs](https://arxiv.org/abs/2610.36671) | 2026-10-30 | exclude / harness | 固定解码规则按当前步预测一致性选择是否看图；逐步自适应不等于反馈修改并继承路由程序。 |
| 2026-10-27 | [2610.37905 · FilingLoop: Evaluating and Evolving LLM Agents for Corporate Disclosure Review and Revision](https://arxiv.org/abs/2610.37905) | 未从本次 HF 榜核实 | harness / harness | 已评分批次的要求级反馈改写 Reviewer/Filer 技能，权重固定，新技能只供后续任务使用。 |
| 2026-10-28 | [2610.38174 · Scaling Lean Theorem Proving for Real-World Code Verification](https://arxiv.org/abs/2610.38174) | 2026-10-30 | exclude / evaluation_benchmark | 递归子代理改的是当前证明和引理；正文描述固定求解架构和基准生成，没有跨任务 Harness 自改机制。 |
| 2026-10-28 | [2610.38266 · Recursive Self-Improvement in Physical AI: Mechanisms, Evidence, and Evaluation](https://arxiv.org/abs/2610.38266) | 未从本次 HF 榜核实 | other_direction / theory_survey | 综述具身领域的策略、世界模型、记忆、技能和可执行 Harness；整体研究对象是物理 RSI，不是 Harness 专项方法。 |
| 2026-10-28 | [2610.38293 · EPSBench: Benchmarking LLM Agents for Earnings Forecasting](https://arxiv.org/abs/2610.38293) | 2026-10-30 | exclude / evaluation_benchmark | 同一固定 Harness 与共享会计计算器上的财报预测评测，不涉及程序自进化。 |
| 2026-10-28 | [2610.38331 · Multi-Token Prediction Done Right](https://arxiv.org/abs/2610.38331) | 2026-10-30 | exclude / model_weights | 改变多 token 预训练梯度与自蒸馏目标；未描述多代模型产生新数据的外层递归，亦未改 Harness。 |
| 2026-10-28 | [2610.38342 · Investor's Last Exam: Can AI Agents Do Equity Investment Without Seeing the Future?](https://arxiv.org/abs/2610.38342) | 2026-10-30 | exclude / evaluation_benchmark | 冻结时点数据上的投资研究基准；评估代理能力，不评估其自进化机制。 |
| 2026-10-28 | [2610.38392 · Masked Erosion: How Acceptance Gates Lose Redundant Safeguards in Self-Improving Agents](https://arxiv.org/abs/2610.38392) | 未从本次 HF 榜核实 | harness / safety_governance | 专项评估固定模型周围文本 Harness 的接受闸门、继承的编辑及安全冗余损失；应归 Harness 安全评测，不是新方法数量。 |
| 2026-10-28 | [2610.38568 · A-RSI: Adaptive Task Refresh for Zero-Data Multimodal Self-Improvement](https://arxiv.org/abs/2610.38568) | 2026-10-30 | other_direction / model_weights | Solver 多个训练窗口继承权重并自生成 rollout，但模板、候选池和刷新控制器固定；明确非 Harness，广义 RSI 是否达标留给 owner。 |
| 2026-10-28 | [2610.38681 · Weaken to Strengthen: Weakening-Induced On-Policy Self-Distillation for Large Reasoning Models](https://arxiv.org/abs/2610.38681) | 2026-10-30 | exclude / model_weights | 正文明确原始模型和弱化模型、轨迹与监督在优化中全程固定；属于单轮离线自蒸馏，不因题名自蒸馏纳入 RSI。 |
| 2026-10-28 | [2610.38728 · From Grind to Grasp](https://arxiv.org/abs/2610.38728) | 未从本次 HF 榜核实 | other_direction / theory_survey | 给出跨代改进效率的广义 RSI 理论判据，涉及代码解释器但未限定为 Harness 演化。 |
| 2026-10-28 | [2610.38796 · Routed Continual Learning](https://arxiv.org/abs/2610.38796) | 未从本次 HF 榜核实 | other_direction / experience_world_model | 路由提示与记忆系统库固定；选择已有机制、配置和更新簇状态，不生成或改写记忆管理代码或策略。 |
| 2026-10-29 | [2610.39122 · Appreciation Teaches Unauthorized Execution: Self-Evolution Degrades the Robustness of Personal Agents to Indirect Prompt Injection](https://arxiv.org/abs/2610.39122) | 未从本次 HF 榜核实 | harness / safety_governance | 专项测试反馈写成技能后对后续会话授权判断的影响；技能演化分支符合 Harness，RL 分支单独属于权重更新。 |
| 2026-10-29 | [2610.39264 · Online Dense Reinforcement Learning with Planning-Grounding Agent for UI Navigation on Live IOS Apps](https://arxiv.org/abs/2610.39264) | 2026-10-30 | exclude / model_weights | 固定规划/grounding 框架内做 PPO 在线训练；没有反馈改写可复用 Harness，也未建立多代自改进外循环。 |
| 2026-10-29 | [2610.39287 · OpenFlyV2: An onboard vision-language-action model for aerial perception and navigation](https://arxiv.org/abs/2610.39287) | 2026-10-30 | exclude / embodied | 训练机载 VLA 并维护飞行时序状态；闭环飞行不构成跨任务 Harness 自改进。 |
| 2026-10-29 | [2610.39293 · Unlocking Any-Order Generation in Pretrained Autoregressive Image Models](https://arxiv.org/abs/2610.39293) | 2026-10-30 | exclude / model_weights | 用预设课程和位置编码适配图像生成器，未展示反馈修改并继承改进程序。 |
| 2026-10-29 | [2610.39301 · Youtu-Parsing-Omni: One Encoder, One Schema, All Modalities](https://arxiv.org/abs/2610.39301) | 2026-10-30 | other_direction / model_weights | OSAD 明确多轮刷新 teacher/student 权重；共同变化的是两个模型状态，没有外部 Harness 工件的协同演化。 |
| 2026-10-29 | [2610.39302 · Proving and Improving the Platonic Representation Hypothesis with JEPAs](https://arxiv.org/abs/2610.39302) | 2026-10-30 | exclude / model_weights | 研究跨模态表示理论与训练正样本设计，不是递归自改进机制。 |
| 2026-10-29 | [2610.39358 · Before the Next Rollout: Diagnosing Skill Utility Shifts from Policy Updates](https://arxiv.org/abs/2610.39358) | 未从本次 HF 榜核实 | harness / harness | 更新后的 policy 与文本技能库分别演化；失败轨迹和 readout 指导编辑，配对验证保留新技能库供后续窗口使用。 |
| 2026-10-29 | [2610.39417 · Well-Specified and Well-Tested? Assessing SWE-bench-Style Datasets with a Self-Evolving Agent](https://arxiv.org/abs/2610.39417) | 未从本次 HF 榜核实 | other_direction / experience_world_model | 反馈插入、修改或删除可检索经验条目；复用阶段仍用同一 RAG 流程，没有修改检索或记忆管理程序。 |
| 2026-10-29 | [2610.39423 · FDSML: Formula-Driven Supervised Metric Learning with Parameter-Aware Triplet Loss](https://arxiv.org/abs/2610.39423) | 2026-10-30 | exclude / model_weights | 公式合成预训练数据和度量损失；未描述多代自生成反馈闭环或 Harness 更新。 |
| 2026-10-29 | [2610.39508 · Compile Away Uncertainty: Self-Evolving Agent Skills via Programmatic Compilation](https://arxiv.org/abs/2610.39508) | 未从本次 HF 榜核实 | harness / harness | 执行轨迹和检查错误驱动技能骨架与程序修订；验证过的程序资产及技能被保留给后续任务复用。 |
| 2026-10-29 | [2610.39663 · AB-Attention: Accurate Block Attention for Accelerating Video Diffusion Transformers](https://arxiv.org/abs/2610.39663) | 2026-10-30 | exclude / harness | 固定训练无关注意力近似和算子优化；输入相关稀疏选择不是程序自身的递归改进。 |
| 2026-10-29 | [2610.39714 · MoLRSI: A Recursive Self-Improving AI agent for Molecular Discovery](https://arxiv.org/abs/2610.39714) | 未从本次 HF 榜核实 | borderline / ai4ai | 主要循环更新外部科学工作流和三类经验记忆；同时描述资源技能的执行修复与保留，是否构成被实证的 Harness 子循环需 owner 裁决。 |
| 2026-10-29 | [2610.39795 · The Role of Self-Concept In Language Models](https://arxiv.org/abs/2610.39795) | 未从本次 HF 榜核实 | other_direction / safety_governance | 测试自我概念对假设性继任模型选择的影响；是广义 RSI 安全相关研究，正文明确无真实工具行动或自改权重。 |
| 2026-10-29 | [2610.39884 · KARMA: Training-Free Knowledge-Atomic Harness Evolution for Industrial Advertising Agents](https://arxiv.org/abs/2610.39884) | 未从本次 HF 榜核实 | harness / harness | 成功/失败轨迹触发原子规则与角色、输出协议编辑，规则直接构成系统提示及响应 schema，闸门保留到后续批次。 |
| 2026-10-29 | [2610.40453 · PhysInsert: Physically Plausible Object Insertion with Geometric Priors and Bidirectional Object-Scene Interactions](https://arxiv.org/abs/2610.40453) | 2026-10-30 | exclude / model_weights | 训练物体插入模型并编辑外部图像，未描述递归改进或 Harness 更新。 |
| 2026-10-29 | [2610.40454 · Glance: The Generator Is Its Own Reranker](https://arxiv.org/abs/2610.40454) | 2026-10-30 | exclude / model_weights | 一次任务适配器微调让同一 backbone 完成重排；自重排不等于系统根据反馈自我改进。 |
| 2026-10-29 | [2610.40564 · Training Foundation Models with a Single Algorithm](https://arxiv.org/abs/2610.40564) | 2026-10-30 | exclude / model_weights | 统一预训练、SFT 与 RL 的固定优化算法和混合数据系统；未建立改进程序自改或多代自生数据闭环。 |
| 2026-10-29 | [2610.40614 · L3G-World: Real-Time Infinite World Generation with Latent 3D Gaussian Memory](https://arxiv.org/abs/2610.40614) | 2026-10-30 | exclude / experience_world_model | 更新的是当前生成场景的高斯记忆表示；没有跨任务继承的代理能力或记忆管理策略更新。 |
| 2026-10-29 | [2610.40647 · Read, Allocate, Route: Role-Coupled Tokenization for Pixel-Space Generative Transformers](https://arxiv.org/abs/2610.40647) | 2026-10-30 | exclude / model_weights | 固定频段 token 化和注意力结构的图像模型训练，不涉及 Harness 自进化。 |

`borderline` 是待 owner 裁决，不计为 Harness 或排除完成。`other_direction` 不进入 Harness 日报。
