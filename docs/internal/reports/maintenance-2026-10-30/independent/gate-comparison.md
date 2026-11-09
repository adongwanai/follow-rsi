# 2026-10-30 冻结独立复核与 canonical gate 对照

正式决定全部为 **defer**。本表在独立结论冻结后生成，仅对照 `gate.verdict`；`primary` 和普通 relevance `include` 均不作为 Harness gate。分歧表示需要复核，不是已证明主审核错误，更不是发布批准。

## 覆盖与交叉统计

固定积压 1124 项；canonical 1139 项包含另外 15 个 HF 新条目。50 项 owner/catalog 保护项未进入改写。本表覆盖 388 个已取得来源复核的积压条目：195 项类别一致、13 项明确 gate 分歧、32 项 canonical borderline、15 项已有明确 gate 但独立仍待定、133 项缺少 gate。

| canonical gate | 独立 include | 独立 exclude | 独立 defer | 合计 |
| --- | --- | --- | --- | --- |
| harness | 165 | 5 | 9 | 179 |
| other_direction | 8 | 25 | 4 | 37 |
| exclude | 0 | 5 | 2 | 7 |
| borderline | 23 | 4 | 5 | 32 |
| missing | 11 | 114 | 8 | 133 |

## 现有 gate 与独立建议的分歧（13 项）

其中 6 项经过 Codex 正文逐段裁决，7 项仍只有第三轮模型建议。模型建议含有的数字未经本轮独立性能审计；下表只呈现范围判断。

| 条目 | 现有 gate → 独立建议 | 证据层级 | 范围判断／待核对点 |
| --- | --- | --- | --- |
| arxiv:2609.37989 · TabFM-Auto: Self-Evolving Pipelines for Tabular Foundation Models | harness → exclude | Codex 正文裁决 | TabFM-Auto 用验证分数优化每个表格数据集的处理脚本，冻结 TabFM；产物是该数据集的 ML 解法。运行脚本的 coding-agent Harness 固定，跨数据集可复用操作库仍被列为未来方向，故按 task-artifact 边界排除当前 Harness RSI 专题。 |
| arxiv:2609.40330 · Turbo Harness: Instance-Adaptive Harness Optimization | harness → exclude | 模型建议，待逐段复核 | 该文的可训练对象是一个小型 harness editor（Qwen3.5-9B，GRPO 全参数微调），执行模型 M 全程冻结；反馈回路是：对每个训练实例采样 G 个补丁，实际执行打补丁后的 harness 并据任务得分做 RL 更新 editor。真正被保留下来的是 editor 的权重，而不是一个由反馈迭代更新的外部可复用程序产物：全局 harness H* 来自“已完成的 Meta-Harness 外层搜索”（属于既有工作，本文直接复用其 archive），playbook 由该 archive 一次性总结后“hold it fixed”，不参与迭代；部署期每个实例只生成一个实例专属 harness 补丁，且证据显示它只“在同一 issue 的三次重复运行”内复用，属于面向单任务的产物，而非跨任务/会话/优化轮次持久保留的执行程序。按边界(a)(b)(e)，这里主要是 RL 权重优化加固定经验摘要，缺少“实际被保留的外部程序更新”，因此不构成本项目意义上的 Harness 自改进方法，也不适用共演化例外（执行模型未改权重，且没有与之协同演化的外部 harness 产物）。 |
| arxiv:2610.07787 · OOPMAS: Object-Oriented Multi-Agent Systems for Query-Level Workflow Generation | harness → exclude | Codex 正文裁决 | OOPMAS 按单个 query 生成类与工作流；跨优化轮次积累的 skill library 明确是结构化失败/修复记录，属于固定生成器的上下文记忆。不能把这种记录库或当前任务工作流修复本身等同于自身可复用 Harness 的保留式改写。 |
| arxiv:2610.08902 · Agent Plasticity: Measuring Self-Improvement Through Experience | other_direction → include | 模型建议，待逐段复核 | 该论文是评估型工作，但被评估对象正是 Harness 演化的核心：模型权重冻结，改进只能发生在执行器外部的可复用工件上——Python 工具库、技能文件（SKILL.md）、策略、文本记忆与 CLAUDE.md/AGENTS.md 指令等持久清单。改进回路明确由执行反馈驱动：每个 checkpoint 用训练交互（轨迹、Stockfish/规则诊断、错误、执行轨迹）产生证据，同一模型在 reflection 阶段据此提出清单更新 I_{t+1}=U_M(I_t, E_t)，候选更新须通过结构与可执行校验才被提交并持久化；每个动作 episode 从全新上下文开始，仅继承已提交工件，随后在训练、held-out ID、held-out OOD 上评分并计入学习成本。这构成“反馈驱动的外部 Harness 工件演化 + 跨会话持久化 + 留出集泛化验证”的专门评测，而非一般 RSI/工具基准或模型权重优化，因此归为 harness_evaluation 并建议 include。评测者自身固定并不妨碍资格，因为被研究对象就是工件清单的演化效率、持久性与泛化。 |
| arxiv:2610.10426 · CoTrace: Data Recipes for Training Terminal Agents with Harness-Model Co-Evolution | other_direction → include | Codex 正文裁决 | CoTrace 的失败轨迹用于修改 prompts/processors/tools，并通过 promotion 保留新 runtime，再训练模型进入下轮。依 owner 的 coevolution 例外应保留 Harness 候选；原模型以权重同为主要对象为由排除不正确。 |
| arxiv:2610.18792 · SEAR: Self-Evolving Agentic Robotics | other_direction → include | 模型建议，待逐段复核 | SEAR是面向自演化机器人agent的专门评测/基准，核心持久对象是由执行反馈筛选出的versioned code skills和written memories（以及code-as-policy程序）。LM在CaP中冻结，agent写程序、运行、读取失败并修订，成功技能进入library供后续任务继承；benchmark用best-of-3、no-library、sealed judge、重复运行和T1-T5迁移层级检验“保留经验”而非重采样。虽然包含auto-research微调VLA，但AR checkpoints/data不跨任务保留，跨任务持久的是library，因此权重不是主要干预。作为专门评估Harness式技能/记忆库演化与迁移的研究，可纳入harness_evaluation。 |
| arxiv:2610.19366 · Seeing, Maintaining, and Learning: The Evolution of Multimodal Agent Memory | harness → exclude | Codex 正文裁决 | 该综述的主轴覆盖多模态记忆的表征、静态/动态内容维护以及策略演化；T3 外围策略更新只是其中一层。按专门 Harness 演化的范围要求，更适合作为通用记忆/RSI 背景；没有实验本身不是排除理论综述的理由。 |
| arxiv:2610.20474 · AdaRSI: On-Demand Recursive Self-Improvement for Embodied Agents | other_direction → include | Codex 正文裁决 | AdaRSI 同时保留 Harness 修订和按需训练的低层执行策略，验证反馈进入后续轮次。依 owner 共同迭代例外标 coevolution；不接受“只调用少量微调动作就能证明权重非主要”的推论。 |
| arxiv:2610.22984 · Self-Evolving Agents Can Repair Failures but Struggle to Generalize from Them | other_direction → include | 模型建议，待逐段复核 | 该文是一篇专门评测“外部工件驱动的自进化”的受控研究：执行器（backbone policy）权重全程冻结，进化对象是外部状态 S_t，包括 reasoning memory、skill 文档与运行时 harness（Evo-Harness 把执行经验编译为可复用 harness 指导，由 evolver 决定合并/丢弃并在后续任务中检索使用）。反馈环路由失败轨迹驱动（CFOE：仅失败轨迹进入 updater，verifier 反馈对 agent/updater 隐藏），并以固定 held-out 任务集的多次 checkpoint 评估进化后的 harness/memory/skill 是否保留并在未见任务上生效，因此属于对 harness 工件反馈驱动演化与持续性的专门评测，而非通用 agent/工具基准。论文的负结果（修复有余、泛化不足）不影响其评测资格，只影响证据强度。 |
| arxiv:2610.26020 · Understanding When Reflective Prompt and Skill Optimization Helps on Locally Served Reasoning Models: A Two-Model Study of GEPA and SkillOpt | other_direction → include | 模型建议，待逐段复核 | 研究对象不是模型权重，而是围绕冻结执行器（DeepSeek V4 Flash via DwarfStar、Qwen3.8-27B via LM Studio，均按 checkpoint/量化冻结）的可复用外部工件：GEPA 进化出的 system prompt 与 SkillOpt 训练出的 Markdown skill 文件，属于 Harness 的外部可复用程序工件（系统提示、技能文件）。循环由执行反馈驱动：GEPA 让反思模型读取完整轨迹（输入、推理、输出、逐任务反馈）并以自然语言提出新 prompt，采用 Pareto 前沿选择；SkillOpt 让分析师/优化器模型在评分 rollout 上反思并对 skill 文档做有界增删改，仅在 held-out selection 严格提升时接受，否则进入 rejected-edit buffer。工件持久化明确：SkillOpt 部署时只携带最终 best_skill.md，优化工件带 manifest 版本化并在 held-out 测试集上评估，可供后续任务复用。本文本身不是新方法，而是用官方 GEPA/SkillOpt 实现做两模型、两基准、四条件的受控复现与 held-out 评估，专门考察文本空间优化器演化外部工件是否迁移、验证增益是否在 held-out 反转、选择噪声是否解释小增益，属于对 Harness 工件反馈驱动演化的专门评测，因此归为 harness_evaluation 而非 harness_method。 |
| arxiv:2610.26848 · Where is Physical RSI capability from? An Observational Scaling Law of LLM-as-policy | other_direction → include | 模型建议，待逐段复核 | 该文属于评估型工作，核心研究对象是物理任务中持久 Harness workspace（技能、工具、策略代码、记忆）随执行反馈被修订并保留的过程。每轮物理尝试返回原生分数、成功标志和失败原因，agent 在禁用机器人动作后修订并提交 workspace 供后续轮次使用，且模型权重固定。评估进一步通过清空、冻结和跨任务迁移 workspace 检验保留经验是否在未见过布局和任务上继续有用，因此是专门评估 Harness 演化，而非仅一般 RSI 或工具/agent 基准。 |
| arxiv:2610.29357 · Memory-Centric Continual Learning for AI Agents | harness → exclude | Codex 正文裁决 | MCCL 的研究范围包含固定管理器下的记忆内容适应、离线权重训练及在线策略演化，提出通用记忆持续学习框架。Harness 策略演化是高级子层，不宜把整个框架数为 Harness 专项理论；不是因没有实现而排除。 |
| arxiv:2610.31427 · FastHarness: Experience-Driven Review Scheduling for Vision-Language-Action Policies | other_direction → include | 模型建议，待逐段复核 | 论文把外部执行程序 FastHarness 作为主要改进对象：在冻结的 π0.5 VLA 外层加入基于阶段记忆和错误记忆的审查调度器，并用审查结果更新记忆、审查间隔和恢复控制流。改进发生在 harness 的记忆管理与监督调度逻辑，而不是策略权重；审查反馈驱动调度变化，且记忆跨同一任务链的后续 episode 保留，符合 harness_method。 |

## 第三轮模型自身的修正（不能合并计作主审核错误）

正文裁决改变了 20 项模型建议。部分是 exclude 改为 defer：这纠正了排除理由，但没有确认应纳入。初始提示遗漏 coevolution 例外，原始输出与实际 prompt hash 全部保留。

| 条目 | 原模型 → 原文裁决 | 现有 gate | 修正原因 |
| --- | --- | --- | --- |
| arxiv:2610.24453 · Hippo: Training-Free Agent Self-Evolution via Hippocampal Replay | include → exclude | missing | Hippo 修改 L2 经验内容：合并、删改、解决适用条件冲突依然是改记了什么，管理和检索程序没有被反馈重写。模型原建议将条目替换本身视为 Harness，违背当前 taxonomy 的 experience_world_model 边界。 |
| arxiv:2610.19591 · L3M: A Verifiable Harness and Runtime for Self-Extending and Self-Improving Agents | include → defer | borderline | L3M 明确提供可自扩展工具和 persona 发布机制，但实际核心验证是安全运行时。不能把支持的优化用途直接当作已验证的反馈演化方法；是否保留为 background 应由 owner 决定。 |
| arxiv:2610.20344 · Doc2Harness: Benchmarking LLMs on Long-Horizon Harness Engineering of Coding Agents | defer → exclude | other_direction | Doc2Harness 专门评测一次性 Harness 工程构造；不是反馈驱动的 Harness 演化评测。可作为相关构造 benchmark，但不进入 core+harness_eval 数量。 |
| arxiv:2610.34450 · EvolveMAS: A Unified Self-Evolution Framework for Decentralized Multi-Agent Systems | include → exclude | missing | EvolveMAS 的 MemoryAgent 治理协议固定，演化的是 interaction knowledge/partner profiles/规则内容，按当前定义属于 experience_world_model。仅称条目为 skill 或 strategy 不足以证明管理程序/策略文件被修改。 |
| arxiv:2610.32120 · ImageRSI: Verification-Driven Recursive Self-Improvement for Agentic Image Generation | include → defer | missing | ImageRSI 的主过程同时包含任务内 prompt repair、经验条目库与 judge 权重训练。冻结图像生成器不足以证明权重不是主要干预，也不能把固定准入协议管理的经验条目自动当作 Harness 程序变异。 |
| arxiv:2610.29317 · SpatialBrain: Spatial Intelligence Growing from Experience | include → defer | missing | SpatialBrain 正文经验更新多为固定规则下统计、条件关联与可用性调整；附录又声称可 compile/validate new procedures。因此不能直接判为纯记忆，也不能从可编译能力直接推断论文运行确实演化了程序。 |
| arxiv:2610.02687 · Decoupling Memory from Context: Structured Memory for Token-Efficient Test-Time Continual Learning | include → exclude | missing | GraphMemory 改的是节点知识与边的帮助性证据/权重，固定 Curator、Reflector、retriever 管理这些内容。局部图更新或非追加修改不等于管理程序演化，依 owner taxonomy 属 experience_world_model。 |
| arxiv:2610.07663 · Joint Workflow and Prompt Optimization for User Behavior Simulation | include → exclude | borderline | SWORD 确实联合优化 DAG 和 prompts，但被交付优化对象是用户行为模拟器。依 owner 明确排除用户模拟器的边界，不能仅以工作流搜索形式进入 Harness core；可保留为方法关联背景。 |
| arxiv:2609.37105 · VACE: Validation-Gated Alternating Co-Evolution of Agent Models and Harnesses | exclude → include | harness | VACE 是真实权重/Harness 共同迭代，原始第三轮提示词的权重非主要限制遗漏 owner 明确的 coevolution 例外。轨迹提出技能/执行指导变更、在新 checkpoint 固定下验证、保留后进入下一 RL 阶段；应建议 coevolution，不能因权重同时训练一概排除。 |
| arxiv:2610.10426 · CoTrace: Data Recipes for Training Terminal Agents with Harness-Model Co-Evolution | exclude → include | other_direction | CoTrace 的失败轨迹用于修改 prompts/processors/tools，并通过 promotion 保留新 runtime，再训练模型进入下轮。依 owner 的 coevolution 例外应保留 Harness 候选；原模型以权重同为主要对象为由排除不正确。 |
| arxiv:2610.29784 · Evolving with Open Worlds: Towards Recursive Self-Improvement for Future Forecasting | exclude → defer | other_direction | EvoForesight 不应仅因权重共同训练而排除；真正待辨明的是它累积的四层 skills 是否为被修改的策略文件，还是在固定检索/注入机制下增加经验程序描述。正文明确提取、组织、检索 skill 内容，未在本轮读到具体版本化 skill 文件修订证据。 |
| arxiv:2610.36013 · OmniBrain-0: A Unified Agentic Model for Embodied Intelligence | exclude → defer | borderline | OmniBrain-0 同时迭代参数和执行提醒，不能因存在权重训练就排除。正文支持候选提醒在冻结参数下验证并跨轮保留，但已见更新主要表现为 rubric/提醒内容；需确认改变的是可复用提醒策略工件而非固定提醒器的记忆内容。 |
| arxiv:2610.17718 · ECG-RSI: Recursive Self-Improvement through Targeted Electrocardiogram Waveform Evolution | exclude → defer | missing | ECG-RSI 的 construction policy 明确有可版本化 operators/prompts/skills，也与 learner 权重迭代共存，因此原第三轮直接以权重为主排除不成立。但这些改写服务于训练数据/环境生成，和 owner 明确排除 training_env_reward 的边界有交叉，需裁定其是否是 improver 自身程序。 |
| arxiv:2610.21040 · Recursive Reward Improvement via Adversarial Meta-Prompt Evolution | exclude → defer | other_direction | RRI 持久改写 proposer 的两段生成指导，确有 meta-prompt 演化，原第三轮只因 solver GRPO 为主要干预而排除过严。待定点在于改的是训练任务/奖励生成器的程序指导，owner 是否将这一层视为 improver 程序，不能仅凭 rubric 数据变化混为 Harness。 |
| arxiv:2610.28785 · Measure First, Then Allocate: Calibrated Rollout Budgets for MCP Agents in Reinforcement Learning | exclude → include | missing | BRACE 主体是权重训练的采样预算，但同文 DISCORD 是明确的 Harness 修改保留方法/评测：冻结权重比较同一提案流，研究跨轮编辑接受误差。它无需自己生成提案即可构成专门 Harness 演化评测，原第三轮以“不生成提案”排除不恰当。 |
| arxiv:2609.36746 · EASE: Behavior-Adaptive Skill Curation for Self-Evolving Agents | exclude → defer | harness | EASE 的部署阶段 curator 与 executor 都冻结而 skill repository 在线增删改，不能因 curator 预先经过 RL 就否定部署时的外围学习。待定点是 repository 项是否属于 owner 接受的技能文件/策略工件，还是固定策展器管理的经验内容。 |
| arxiv:2609.38661 · EvoSteer: Online Self-Evolving Graph Orchestration via Reference-Anchored Credit Assignment | exclude → defer | harness | EvoSteer 的主要训练对象确为编排器权重，但它还提供跨运行技能准入环节，不能仅凭权重角色否决该组件。当前任务图的原子修改未必跨任务保留；需单独核对保留技能的工件类型与使用范围。 |
| arxiv:2610.20845 · Evolving Together, Failing Apart: The Skill-Policy Co-evolution Trap in Self-Improving Agents | exclude → defer | harness | CODA 是评测协议，不必自己修改 Harness；也不能因被评测系统同时训练权重就排除。真正待辨明的是被扰动的 skill bank 是否由程序/技能文件构成，还是仅为经验内容。正文可确认研究共演化后技能漂移，但尚不足以把全部技能条目自动视为 Harness。 |
| arxiv:2610.36469 · CoHARL: Co-Evolving Agent Policies and Executable Harnesses with Reinforcement Learning | exclude → include | harness | CoHARL 明确让 proposer 读取执行成败轨迹、修订可执行 Harness 代码，接受的版本加入种群并参与后续策略训练。权重与 Harness 同时迭代符合 owner 的 coevolution 例外；初版模型单因权重是主要干预而排除应撤回。 |
| arxiv:2610.10164 · UniSkill: Learning Actor-Aligned Skill Proposals for an Evolving Policy | exclude → defer | harness | UniSkill 确有依据成败轨迹接受 skill 修改、写回 skillbank 并在后续相同任务实例重用的闭环，不能单因 actor 与 proposer 联合训练而排除。待定点是文本技能条目是否属于可复用策略工件，还是固定检索器管理的经验内容；当前正文证据不足以越过此边界。 |

CoHARL 与 VACE 的现有 gate 本来就是 harness；独立模型误排后已用原文改回 include，不应把它们汇报为 canonical 错分。CoTrace 同时存在主 gate 分歧和第三轮模型修正，分开记录而不重复计算条目。

RSIHub 的建议仍为 include，但类型从 harness_method 修正为 harness_evaluation；固定 recipe 的实验不能宣传成自适应 recipe 改写已实测。AdaRSI 保留 include 的依据改为真实 coevolution，不用微调次数推断权重非主要；VibeGame 只保留 collaboration contracts 组件，不能把整个游戏产物都当作 Harness。

另有 4 项原模型 defer 经官方摘要筛查建议 exclude（仅摘要层级，不声称正文不存在其他机制）：

| 条目 | 摘要筛查依据 |
| --- | --- |
| arxiv:2610.30043 · TARSphere: A Robot-Oriented Full-Stack Framework for Long-Horizon Embodied Agents in Evolving Physical and Social Environments | 冻结模型通过固定工具/记忆按反馈改当前决策；无跨轮保留新 Harness 的摘要证据。 |
| arxiv:2610.30753 · FilmFlow: Agentic System for 3D Virtual Film Cinematography | 视觉反馈修改摄影计划与镜头轨迹，固定四角色框架未被演化。 |
| arxiv:2610.33396 · Fast Instinct, Slow Reason: A Dual-Speed Agentic Framework for Self-Configuring Multi-Object Tracking in Satellite Video | 离线学习 shortlist/ranker 后每序列选择配置；不是 agent 根据执行反馈持续改写自身程序。 |
| arxiv:2610.35845 · Work Agents: Systems, Capabilities, and Optimization | 综述工作 Agent 的权重/Harness/联合优化，研究对象广于专题；可作 general/background，摘要不足以计入 core。 |

HTTP 402 后的 12 项正文直读及 BetterDeck 的无 API 直读另存为原文裁决，不伪称成功模型输出或模型纠错。

## 尚未解决的边界与缺失 gate

已有明确 gate 但独立仍 defer 的 15 项如下。另有 5 项 canonical borderline、8 项缺少 gate 也仍 defer；合计 28 项独立边界未决，完整 ID 见 JSON 的 `resume.independent_unresolved_ids`。

| 条目 | 现有 gate | 复核层级 | 未决点 |
| --- | --- | --- | --- |
| arxiv:2609.36746 · EASE: Behavior-Adaptive Skill Curation for Self-Evolving Agents | harness | official_body_selected_passages | 检查技能资产创建/修订/保留的实现；如果只是固定机制管理经验条目则归 experience_world_model，如果真实技能文件持续改写则可属 component。 |
| arxiv:2609.37221 · OptiCom : A Unified Framework for State-Conditioned Composition in LLM-Driven Optimization | harness | official_body_excerpt_and_abstract | 核查附录 D 及实现：Strategy Adapter 修改后的 selection preferences/operator weights/templates 是否写入可复用存储，是否在同一任务后续迭代之外（跨任务/会话/优化轮次）继续生效，以及更新是否经过接受/验证；确认 LLM 权重始终冻结。 |
| arxiv:2609.38661 · EvoSteer: Online Self-Evolving Graph Orchestration via Reference-Anchored Credit Assignment | harness | official_body_selected_passages | 查实际晋升技能的内容/代码/文件与下一任务重用；若只是经验条目或任务内图则非 core，若外部技能工件真实演化则允许 component/coevolution。 |
| arxiv:2609.39284 · EngramBench: A Capability-Grounded Benchmark for Skill-Evolution Harnesses | harness | official_body_excerpt_and_abstract | 需获取全文核实：(1) 基准是否记录并促成agent对技能文件的反馈驱动写入/修改，而非仅提供静态技能库作对照；(2) 被修改的技能artifact是否跨学习任务与迁移任务持久保留并被复用；(3) 是否明确冻结基座模型权重、把技能/流程artifact作为唯一或主要改进对象；(4) 评测指标是否直接衡量Harness演化（如技能更新的正确性、迁移增益），而非仅编码时间与上下文规模。 |
| arxiv:2610.04116 · CUAWright: A Minimal Unified Interface for Digital Agents | exclude | official_abstract_only | 需获取全文核对：是否有对 harness 自身（工具库/提示/上下文管理/控制流）的自动修改步骤及其触发信号来自执行反馈；动态创建的工具是否被保存、评分、筛选并复用于后续任务或后续优化轮（而非仅在同一任务内使用）；是否存在 in-loop verifier 或 improver 对 harness 工件的接受/拒绝与持久化机制；模型权重是否冻结；以及“evolvable space”具体指任务级工具生成还是跨任务 harness 演化。 |
| arxiv:2610.10164 · UniSkill: Learning Actor-Aligned Skill Proposals for an Evolving Policy | harness | official_body_selected_passages | 核对被接受条目的实际工件、版本差异和读取接口；若仅是经验记忆则排除 core，若是外部策略文件/程序则允许 coevolution。 |
| arxiv:2610.15481 · SkillFusion: Towards Reliable Multi-Skill Composition for LLM Agents | exclude | official_abstract_only | 获取全文，核查：(a) 编译流程是否存在由执行/评测反馈驱动的多轮修订与接受机制，而非单次静态流水线；(b) 对抗式验证器/selective fallback 的输入信号是否为执行结果或任务评测；(c) 合并技能在后续任务/会话/优化轮次中是否被保留并复用，是否有累积性能提升证据；(d) 执行器权重是否冻结、主要干预是否为技能工件而非模型训练。 |
| arxiv:2610.19226 · Agentic Self-Awareness: Aligning Knowing, Acting, and Holding | other_direction | official_abstract_only | 获取全文，核查 harness search 的具体搜索空间与被更新工件、反馈来源（执行/评估信号）、是否在 held-out 或后续任务复用，以及该搜索是论文主贡献还是仅为 ASA 评测中的干预。 |
| arxiv:2610.20845 · Evolving Together, Failing Apart: The Skill-Policy Co-evolution Trap in Self-Improving Agents | harness | official_body_selected_passages | 若被评测的技能属于反馈生成并保留的程序/策略文件，可记 harness_eval；若只是记忆内容共训，则保留 general_rsi/经验方向。 |
| arxiv:2610.21040 · Recursive Reward Improvement via Adversarial Meta-Prompt Evolution | other_direction | official_body_selected_passages | 依据 owner improver 与 training_env_reward 边界裁定；若将 proposer meta-prompt 认作改进器程序，可标 coevolution。 |
| arxiv:2610.21796 · Reflective Compositional Grounding for Natural-Language-to-SPARQL | harness | official_body_excerpt_and_abstract | 需核实：(1) 是否存在跨问题/跨会话保存并复用被接受要求集或映射库（M_t/H_t）的实际实现与实验；(2) 提示重写是否保留显式、累积的规格而非一次性文本重写；(3) 后续版本或附录是否新增跨查询保留评估。若仅有任务内提示重写，则应归为 other_direction 并排除。 |
| arxiv:2610.26554 · BetaMem: Learning to Remember a Changing World for Embodied Agents | other_direction | official_body_excerpt_and_abstract | 核对附录或实验是否实际运行 Algorithm 1，是否报告 held-out replay、接受/拒绝的修复、rollback 与后续 episode 复用；确认 RSI 对 benchmark 的独立贡献，并确认权重在该子机制中固定且非主要干预。 |
| arxiv:2610.28577 · Cache Engineering for Agents | harness | official_body_excerpt_and_abstract | 需核对图 4 及附录：(a) RSI 中被修改的策略以何种可落盘、可复用的形式存在（系统提示 / 配置文件 / 代码），是否成为后续任务默认使用的工件；(b) 评估反馈（成本、准确率、失败轨迹）如何具体转化为策略修改，候选由谁生成、如何筛选与保留；(c) 改进后的策略是否在后续会话/优化轮次中继承并复用于非 BCP 任务；(d) 明确区分“AKV 服务引擎优化”与“agent 自身缓存管理策略演化”哪一个是论文的主要干预对象。 |
| arxiv:2610.29784 · Evolving with Open Worlds: Towards Recursive Self-Improvement for Future Forecasting | other_direction | official_body_selected_passages | 需要 skill 文件或实际可复用策略工件的创建/修订/保留证据，不能以 paper 中 skill 一词自动通过，也不能仅因 GRPO 自动排除。 |
| arxiv:2610.36848 · Evolving Agent Teams | harness | official_body_excerpt_and_abstract | 需核查：(a) 进化出的团队配置、supervisor prompt、LEARNINGS.md/SYNTHESIS.md 是否以可复用文件形式保存，并在新任务或新会话中被加载复用（而非每次 from scratch 重建）；(b) 是否存在跨任务的迁移实验，显示同一进化后的编排/知识管理策略在后续任务上被直接使用并改进；(c) 正文 Section 3 与 Appendix 中 K 的生命周期定义（每任务独立还是全局）；(d) 若仅为任务内多轮团队重构，则应归为 other_direction（任务输出驱动的搜索过程适配）。 |

canonical borderline 共 32 项（独立 include 23、exclude 4、defer 5），都是边界的后续建议，不作明确 gate 错误统计。缺少 gate 的 133 项中，独立建议 include 11、exclude 114、defer 8；这些条目不能被统计成 Harness 假阴性或假阳性。

### AgentBug-Smith：待重开组件审核

`arxiv:2609.37864` 现有 relevance 标签为 exclude，但没有 gate。Appendix I 的技能蒸馏会根据训练失败修改 `SKILL.md` 与 pattern scanners，再冻结用于留出测试；因此建议仅重开这个 Harness 组件的审核。原始 bug reproduction／外部补丁任务本身不自动符合 Harness RSI，当前正式决定仍为 defer。

> is a human-readable SKILL.md document paired with a set of lightweight pattern scanners.

> When the agent fails on a training issue, the pipeline diagnoses whether the failure matches a recognizable bug shape.

> If a failure matches a known shape, the skill is updated by adding or tightening a generic scanner:

> No further updates are made before evaluation on the held-out test set.


来源：https://arxiv.org/html/2609.37864v1；逐段裁决记录见 `adjudications.jsonl`。这属于上游 relevance 排除后发现附加组件，不是已有负 gate 被证伪。

## 身份与输入版本限制

按 ID 对齐不等于两轮使用相同输入。canonical 和官方来源可能存在摘要或来源版本差异；应用建议前必须结合 pipeline 的输入指纹报告检查。原始模型 source hash 与 Codex 来源包 hash 分开保存。发现的两个题名字符串差异如下，仅记录排版差异，不宣称身份错配：

| ID | 独立来源题名 | canonical 题名 | 有本轮来源复核 |
| --- | --- | --- | --- |
| arxiv:2609.36675 | Gödel Forest: Balancing Search Depth and Breadth for Data-Centric Recursive Self-Improvement | G\"odel Forest: Balancing Search Depth and Breadth for Data-Centric Recursive Self-Improvement | False |
| arxiv:2610.21082 | Sci$Π$vot: Benchmarking Principal-Investigator Judgment at Pivotal Moments of Scientific AutoResearch Agents | SciΠvot: Benchmarking Principal-Investigator Judgment at Pivotal Moments of Scientific AutoResearch Agents | True |

## 冻结绑定

- canonical SHA256：`e9632c353f3285cda18b8f0592e6f7517245778a1dc07e27ebab8ec7a434f820`

- 归档 manifest SHA256：`331ac6dc1a4d2a0cfef720333cf162a790af65066bf31bb260f6a2664efc56c8`

- 冻结建议 SHA256：`7779f3d0295437cc52235968ea49308bc13592d17b349b733fd12a15291a9df3`

`build/` 中的 in-progress manifest 不作为归档终态。原始冻结文件没有改写。后续事项见 [resume-checklist.md](resume-checklist.md)，可核算数据见 [gate-comparison.json](gate-comparison.json)。
