# 2026-11-01 独立复审（冻结前结论）

复审对象：10 月 31 日遗留的 30 条 unknown（21 篇论文、9 篇官方文章）。不是 11 月 1 日 HF 推荐榜，也不是今日新论文。

范围建议：2 条 Harness 候选、25 条本专题范围外、3 条仍待定。**正式决定全部 defer，零条获人工批准，零条发布。**

本轮独立判读共享的原始来源缓存；冻结前未读取主审分类。读到官方摘要的论文 20 篇，其中 13 篇另核对方法/边界段落；另外 1 篇出版社正文受阻。9 篇官方文章核对相关正文。不是逐字通读所有论文、不是实验复现。

## 必须保留的边界

- VEvo-Harness、EvoTeam：有反馈、外部技能/规则修改、准入与跨任务留存描述；仅通过范围候选判断，不更改任何证据字段。
- SkillMem：文字技能发现与参数化 reader/latent memory 混合，持续 Harness 工件演化链条不够清楚，unknown。
- Kernel loop：kernel/经验为主，运行中改过搜索规则，但自主修改归因不足，unknown。
- MAS-Loop、EpiAgent、SCOPE：不能把模型参数训练或任务内 MAS patch 当成持久 Harness 共进化。
- EmbodiExp：执行时经验库冻结，更新 Task State；FARMS：产出科学技能不自动等于技能演化。
- Elsevier Human–AI social systems：正文 403、无摘要；Crossref 只有 2026-12 月精度，unknown。
- Frontiers：可见发表日期 2026-10-27；citation_online_date=2026-09-28 实为接受日期。只报告，不改原条目。

## 逐项范围建议

| 条目 | 建议 | 核对结论 |
| --- | --- | --- |
| OpenFrontiers: A Collection of Open Research Problems and a Benchmark for Scientific Rediscovery | exclude | 研究问题库与科学再发现评测；摘要描述的是固定协议下的证明/检索评估，未给出反馈改写并保留 Agent 自身 Harness 的机制。不能把一般科研评测标成 Harness 演化。 |
| SkillMem: Compact External Skill Memory for Latent Multi-Agent Reasoning | unknown | SkillMem 确实从成功/失败轨迹抽取可复用文字程序，并构建技能库；实际主要优化对象却是潜在技能向量与可训练 reader。正文未证明外部程序库经过持续反馈修改/准入并带入下一改进轮。冻结骨干不等于没有参数训练，暂不判为 Harness core 或模型-Harness 共进化。需 owner 判定离线技能发现与参数编译的边界。 |
| Post-Training Large Language Models with LLMON | exclude | 核心是通过 SFT 与 RL 教会模型指令/数据分离和执行语义，变化落在模型参数；未见反馈更新可复用外部 Harness 工件。此处方向仅表示相邻主题，不断言已满足多轮权重 RSI。 |
| A Case Study of a Multi-Agent Kernel-Optimization Loop That Learns a New AI Accelerator | unknown | 主要接受对象是 NPU kernel，持久知识包括合法性规则和 notebook，不能据此纳入 Harness。方法段也记载 beam search/3% 门槛改为 single-head/device 验收，但未清楚交代该管理规则改变是否由 Agent 根据反馈自主提出、验证并保留。所有 loop 代码由 Agent 写过也不能替代这条归因链；需补代码历史/操作者记录后裁决。 |
| SCOPE: Selective Critical-Step On-Policy Self-Distillation for Agentic Reinforcement Learning | exclude | 纠错 skill 在当前在线训练轮次为 self-teacher 提供特定错误步骤的蒸馏上下文；持久改进经 GRPO 和梯度传到学生参数。未描述独立技能工件跨轮准入与演化，不是 Harness coevolution。 |
| Holistic Diversity Management in LLM-Guided Evolutionary Search | exclude | 反馈选择、迁移的是待优化程序及其分数；island selection/migration 的更新遵循论文预设公式。任务程序种群演化与固定搜索器的自适应状态，不等于搜索器或 Agent 自己 Harness 的反馈改写。 |
| Cinematize from Unreal: Agentic Choreography for Controllable World Simulation | exclude | CineU 的可执行/持久对象是 Unreal 场景、镜头与时间线，反馈修复当前世界生成任务。摘要未证明修改可跨任务复用的 Harness；持久 world state 不能直接视为 Harness 自进化。 |
| MAS-Loop: Beyond One-Shot Orchestration towards Self-Evolving Multi-Agent Systems | exclude | Refiner 确实修改 MAS 图，但每个 source MAS 只接收一次决定并重跑，流程由当前任务单独采样。跨轮保留的是 Orchestrator/Refiner 的 GRPO 参数更新；未见修订 MAS 工件在后续任务/改进轮被复用，不能因两个策略共同训练标为 Harness coevolution。 |
| Efficient Agentic Audio-Visual Question Answering through Toolset Pruning and Modality Consolidation | exclude | 作者通过分阶段对照实验删减工具并得到固定两工具 AVQA 框架；摘要未描述系统在运行反馈下持续修改、接受并保留工具集合。人工设计/消融得到的小工具集不是自进化。 |
| VEvo-Harness: Causally-Guarded Self-Evolving Harness for Agentic Image Generation | include | 冻结生成模型；视觉验证/根因反馈产生技能 patch，经 patched/unpatched counterfactual 检验后纳入持久技能库，供后续生成使用，并包含保留/冲突处理机制。具备外部技能工件、反馈、准入与留存链条，可作为 Harness component 候选。仅确认范围，不背书 causal 或性能结论。 |
| EmbodiExp: Compositional Experience Transfer for Embodied Agents | exclude | 先从已有轨迹构建子目标经验库，执行期明确冻结该库，更新的是当前 Task State。POLICY 字段是经验指导，不能仅凭字段名判为技能文件/管理机制的反馈演化；归入经验迁移相邻主题。 |
| Try Before You Evolve: Ranking-Scored Trials for Recursive Self-Improvement of Recommender Systems | exclude | Agent 根据 ranking feedback 修改推荐模型训练 recipe（结构、loss、sampler、optimizer），promotion 保留的是外部训练算法，evaluation code 明确固定。属于训练算法/AI 研发；记录实验经验不构成额外 Harness 更新。 |
| Learning to Formulate: Agentic Hardware-Software Co-Design of AI Infrastructure through Progressive Optimization and Verification | exclude | 改写和验证对象是芯片/软件设计优化模板与约束，属于外部设计产物。论文明确将全流程拆成部分实验，长期 template population 增长为未来工作；不能把提出的循环或 reusable task template 冒充已运行的 Harness 自进化。 |
| EvoTeam: Multi-Agent Collaboration via Evolving Teams | include | 执行轨迹和反馈分别更新可复用团队 roster、team-specific interaction rules、prompt patches/skills；修改进入团队/技能库并影响后续任务，底层 LLM 参数固定。方法与附录明确区分当前任务重分配和持久更新，可作为整体 Harness 演化候选。 |
| EpiAgent: Epistemic Self-Play for LLM Agents | exclude | Epistemic Self-Play 交替以 policy gradient 更新同一预训练 LLM 的 belief/action 参数。当前任务 belief state 不是持久外部 Harness；两阶段优化也不是模型与 Harness 工件共进化。 |
| TaskFrame: Connecting Task-Level Planning with Frame-Level Control for Game Agents | exclude | TaskFrame 训练 planner/controller 并缓存当前指令的 goal embeddings；摘要未描述反馈修改复用 Harness。缓存当前任务状态与模型训练均不能据此纳入。 |
| Fast and accurate neural triage decoding of ultra-high-rate quantum LDPC codes | exclude | 量子 LDPC 的神经解码和自适应算力分配；与 Agent 自身 Harness 的反馈持久更新无关。不能因 adaptive 或 iteration 字样纳入。 |
| FARMS: A Verifiable Foundation for Automated Computational Science | exclude | FARMS 以固定角色流程修复数学形式化结果，再由选定命题/证明组装科学计算技能。正文并未表明 Agent 通过运行这些技能的反馈自改并保留自身 Harness；有可执行 skill 不等于有 skill 演化闭环。 |
| Gym-Anything for Robotics: Scaling physical simulations with digital agents | exclude | creation-audit loop 迭代的是机器人训练仿真、任务、reward/verifier；这些是训练系统对象。学习实验分别为同任务上下文尝试、经验迁移及 code-policy 示范训练 VLA；未有 Harness 管理/改进器的持久反馈改写证据。 |
| Community safety report and new protections for teens | exclude | 社区安全报告、产品政策和未成年人保护公告；人工制定边界/安全训练不是反馈驱动的外部 Harness 自修改。 |
| Credit Saison achieves 954% ROI in a ChatGPT Enterprise pilot | exclude | 企业 ChatGPT 采用案例；ROI 是客户报告数值，本轮不审计其效果。正文没有执行反馈自动修改可复用 Harness 的证据。 |
| Fair use benefits everyone | exclude | 版权/fair-use 法律立场与法庭意见摘录；不属于 Harness RSI。 |
| Making it easier for websites to express AI training preferences | exclude | 通过 robots.txt 表达训练内容偏好的标准/政策公告，不是 Agent Harness 演化。 |
| Sakana API Platform、エンタープライズ向けにアーリーアクセスプログラムを開始 | exclude | 企业 API/访问与管理能力发布，介绍多模型编排产品，但没有该系统根据执行反馈自改、接受并保留 Harness 的具体机制。 |
| オントロジーを基盤に、意思決定・実行を支援するAIエージェントプラットフォーム「Sakana Aquarium」 | exclude | Ontology 平台与企业 Agent 产品介绍；根据运营修正持续更新 ontology/agent 的段落明确写为未来开发。当前内容不能证明部署了 Harness 自进化，产品规划不能当已实现成果。 |
| 【イベントレポート】Sakana AI Engineer Open House 2026 | exclude | 工程团队活动与岗位/平台工作介绍；提到 Harness、长期记忆和人类工程改进，不等于系统自主反馈改写 Harness。 |
| Intelligence Report: SNSのAI分析からみる米中間選挙 | exclude | AI 辅助舆情假设与分析报告，输出是研究任务结果；未见可复用 Harness 的反馈持久更新。 |
| Taking Japan-Born AI Products to the World: An Interview with Sakana AI’s VP of GTM | exclude | 人类 FDE 将客户经验反馈到产品的组织流程，不是 Agent 自身的 Harness 演化；多模型编排介绍也没有自动更新机制。 |
| From observation to generation: A complex-systems perspective on generative Human–AI social systems | unknown | DOI/标题可由 Crossref 对齐；原 S2 和 Crossref 均无摘要，出版社正文 HTTP 403。不能只凭标题推断不是 Harness，也不能纳入。保持未知，待可读官方摘要/全文。 |
| Solutions for frontier AI safety: the case for science-driven international cooperation and standardization at a time of radical transformations | exclude | 国际 AI 安全科学合作、工具和标准的政策建议；官方摘要没有具体 Harness 自进化对象/反馈/留存机制。一般 AI 安全治理不能仅因谈及工具而纳入 Harness。 |

短引文、段落索引、来源哈希、实际阅读范围与限制见 source-review.json；原始下载只保留在 build。范围建议需与主审进行冻结后对照，任何分歧都不能自动转为 accept。
