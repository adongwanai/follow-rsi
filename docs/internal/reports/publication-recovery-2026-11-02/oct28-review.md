# 2026-11-02 发布恢复：10/28 两篇与 10/30 VibeGame 定向复核

生成时间：2026-11-02T08:00:57.453809+00:00。这是一份独立 agent 的来源复核建议，不代替人工 decision；本轮没有调用付费接口、修改 canonical 数据或执行发布。

结果：The Trinity 支持原 include；VibeGame 支持范围收窄后的 include，归 HF 10/30；AdaPRA 保留争议并回到 unknown/defer。

| 论文 | HF 推荐日 | 论文原发表/版本日（UTC） | 本轮建议 | 依据边界 |
| --- | --- | --- | --- | --- |
| AdaPRA | 2026-10-28 | 2026-10-23 / v1 | unknown | 在线执行检查可以修改 rubric，但其版本只在单个任务的后续 attempts 保留；离线发现的 seed rubric 跨任务迁移时保持不变。不能把两阶段拼成已经验证的跨任务 Harness 自进化。 |
| The Trinity | 2026-10-28 | 2026-10-26 / v1 | include | 冻结模型外六类协议的模块接口、配置或实现根据成功/失败轨迹修改；宿主检查证据、接口和版本谱系，Explorer 保留节点模块供后续路由，Creator 合并为下一轮 Base Harness。符合 Harness 方法范围。 |
| VibeGame | 2026-10-30 | 2026-10-22 / v1 | include | 支持 Harness 范围的是从已验证开发经历提炼并在后续开发任务中检索的 collaboration contracts：它们修改角色输入输出、依赖与验证流程。游戏 skeleton 和 gameplay module 是外部产物，不能一并认定为 Harness。 |

HF 期次、原发表日和审核日分别保留。AdaPRA 与 The Trinity 的 first_seen 是 10/29，若恢复 10/28 期，必须另行保留“延后发现/审核”的事实；不能通过修改原始日期掩盖。本报告不修改或绕过日期保护。

## 来源与旧审核的有效性

读取 10/30 缓存的官方 arXiv v1 正文并定向复核。32 条原文引句逐字匹配（HTML 空白规范化后连续子串），15 项记录文件哈希核对通过。三个 canonical 标题、摘要、发表日与版本日均与官方 Atom 对应；旧模型记录与冻结清单哈希一致。没有声称重新拉取最新版本或复现实验。

旧记录 reviewer_type 为 independent_llm_not_human，formal_decision 为 defer。2026-11-02 resume-plan 中 input_matches_current=true 仅说明输入未变；它不消除旧推理错误。旧模型 source_hash 与当前 canonical_source_hash 的输入模式不同，不能要求两者相等，也不能混用为人工批准。

## AdaPRA：unknown

2026-10-29 的定向正文复核为 borderline；2026-10-30 的独立模型为 include。来源内容未变仍不代表后者推理有效：后者将固定 workspace 持久化误写为 control-flow 修改，并把同任务 rubric 适配与离线 seed 迁移拼接。保留争议，回到 unknown/defer。

在线执行检查可以修改 rubric，但其版本只在单个任务的后续 attempts 保留；离线发现的 seed rubric 跨任务迁移时保持不变。不能把两阶段拼成已经验证的跨任务 Harness 自进化。

每任务 rubric store 明确隔离；离线反馈生成的 seed verifier 有跨任务适用性，但没有显示在线接受的新版本继承到独立任务。宽口径若将同任务 attempts 算后续改进轮次可能得出不同意见，不能隐藏这一口径差异。

关键原文：

- **fixed_task_workspace** · [S3.SS2.p1](https://arxiv.org/html/2610.33245v1#S3.SS2.p1)：Our harness keeps one workspace per task
- **fixed_task_workspace** · [S3.SS2.p1](https://arxiv.org/html/2610.33245v1#S3.SS2.p1)：and only the model context resets.
- **offline_feedback** · [S3.SS3.p1](https://arxiv.org/html/2610.33245v1#S3.SS3.p1)：We discover rubrics offline from past harness-only runs of the base agent, using the leaderboard percentile of each attempt to contrast stronger and weaker attempts
- **seed_transfer_unchanged** · [S3.SS3.SSS0.Px2.p1](https://arxiv.org/html/2610.33245v1#S3.SS3.SSS0.Px2.p1)：used in every configuration and applied unchanged to DSPredict-Hard.
- **editable_verifier** · [S3.SS5.p1](https://arxiv.org/html/2610.33245v1#S3.SS5.p1)：Add creates a rubric only after the PRA has run and recorded a check for it in the same review, update rewrites a rubric’s specification, and retire deactivates a rubric and records the reason.
- **counterevidence_cross_task** · [S3.SS5.p1](https://arxiv.org/html/2610.33245v1#S3.SS5.p1)：Stores are isolated across tasks, so that results do not depend on the order in which tasks are run.
- **same_task_persistence** · [S3.SS5.p1](https://arxiv.org/html/2610.33245v1#S3.SS5.p1)：initialized with the seed set and kept across the task’s attempts, so a failure found in one attempt becomes an explicit criterion in later reviews.
- **future_work** · [S7.p1](https://arxiv.org/html/2610.33245v1#S7.p1)：harness evolution like Meta-Harness Lee et al. (2026) could further improve our persistent harness.

限制：

- 固定的单任务 workspace 持久化仅证明任务状态/产物留存，不证明管理代码或控制流自己改写。
- 离线 seed 从运行结果归纳并迁移到 DSPredict-Hard，是相关的 verifier 设计证据；不能据此声称在线 adapted rubrics 跨任务继承。
- 旧模型理由中对 rubric 新增数有 77 与 177 的内部冲突，本次不复用该数字、不修改原论文数字。
- 本轮只解决 scope 争议；不是全文所有实验数字和证据卡字段的审计。

后续：如仍拟收录，需明确是离线 feedback-derived verifier 方法还是在线 Harness RSI，并提供被接受的新版本在独立任务复用的原文/工件。

canonical source hash：`21b87d8c5e5c34130e673283d1fac0c32023ac2f9c7228fe102192d05b8605b0`；原正文 SHA-256：`51e6d93890b5be1cefee43d19f93bf36829b8a520eaa37314190d4bb1b71dc6b`。

## The Trinity：include

2026-10-29 与 2026-10-30 的 include 均有正文支持，本轮维持建议；将“必然提高性能”“树拓扑演化”和“skills 自演化”等过宽表述排除。

冻结模型外六类协议的模块接口、配置或实现根据成功/失败轨迹修改；宿主检查证据、接口和版本谱系，Explorer 保留节点模块供后续路由，Creator 合并为下一轮 Base Harness。符合 Harness 方法范围。

Explorer 保留版本化模块并沿能力树继承，Creator 的已验证模块汇入下一轮共享 Base Harness；不是仅追加任务经历。

关键原文：

- **frozen_backbone** · [S4.SS1.p2](https://arxiv.org/html/2610.36077v1#S4.SS1.p2)：and a frozen Claude Opus 5 backbone
- **feedback** · [S3.SS4.p1](https://arxiv.org/html/2610.36077v1#S3.SS4.p1)：Evolver compares successful and failed trajectories using public observations, actions, and host-assigned outcomes to identify node-specific improvements.
- **modified_artifact** · [S3.SS4.p1](https://arxiv.org/html/2610.36077v1#S3.SS4.p1)：It develops reusable modules through host-registered bindings in the six-protocol library
- **modified_artifact** · [S3.SS4.p1](https://arxiv.org/html/2610.36077v1#S3.SS4.p1)：refining interfaces, bounded configurations, or implementations.
- **persistence** · [S2.SS2.p3](https://arxiv.org/html/2610.36077v1#S2.SS2.p3)：Explorer retains node modules; Creator uses the same tree structure and consolidates its next Base Harness.
- **topology_boundary** · [S3.SS1.p1](https://arxiv.org/html/2610.36077v1#S3.SS1.p1)：accumulating validated updates in a fixed-topology Harness tree
- **admission_boundary** · [S3.SS5.SSS0.Px3.p1](https://arxiv.org/html/2610.36077v1#S3.SS5.SSS0.Px3.p1)：local admission requires no score increase.
- **creator_reuse** · [A3.SS2.p1](https://arxiv.org/html/2610.36077v1#A3.SS2.p1)：The consolidated library becomes the Base Harness of the next iteration; it is shared by all nodes and exposed as a single tool that runs one module per call.
- **concrete_verifier_modules** · [A3.SS2.p2](https://arxiv.org/html/2610.36077v1#A3.SS2.p2)：predicate programs over one kind of host measurement learned from rejected worlds
- **skills_boundary** · [S2.SS2.p3](https://arxiv.org/html/2610.36077v1#S2.SS2.p3)：Evaluation-time skills are prepared separately (Section 4.1 ); they are not stored, evolved, inherited, or routed in the tree.
- **module_only_ablation** · [S4.SS2.SSS0.Px1.p1](https://arxiv.org/html/2610.36077v1#S4.SS2.SSS0.Px1.p1)：Base uses initial modules; Module Only evolves them; Skill Only adds skills to Base; Ours combines both and performs best on Train and Unseen.
- **embodied_attribution** · [S4.SS6.SSS0.Px3.p1](https://arxiv.org/html/2610.36077v1#S4.SS6.SSS0.Px3.p1)：These comparisons evaluate complete Harness–skill configurations and do not isolate the effects of module evolution and skill preparation.

限制：

- 能力树拓扑固定；自修改对象是模块绑定、配置或实现。
- Parent registry 的继承要求更高 host-verified performance；local admission 只检查可执行性和证据，不要求分数增加。不能把所有接纳都写成验证过的收益。
- 评测期 skills 单独准备并冻结，不在树里演化。论文有第一轮 module-only/skill-only 消融，但整体迭代/具身对比仍不能全归因于模块演化。
- Router 记忆是经验 Append，agent/prompt/retrieval 等固定；不把记忆追加本身当作管理策略自修改。
- 本轮读了方法与模块附录，没有执行开源代码、复现实验或审计全部表格数字。

后续：可支持原 Harness 收录建议；发布摘要应写清固定拓扑、skills 准备和 local admission 的收益边界，原论文数字保持原样。

canonical source hash：`c7605ce4c99bd7a1c5be7fa7c389d6291304514c527c4b4b298ba113af82ca44`；原正文 SHA-256：`e5fedaf7ae2f0b934743e532a8ec9fe160515266b6983318c160a042e03b57d7`。

## VibeGame：include

维持 2026-10-30 的 include，但缩窄成立依据到可复用协作契约及开发验证策略；旧理由把固定引擎、固定八角色团队与游戏产物全列作被演化 Harness，表述过宽。HF 推荐日为 10/30，不得放进 10/28 当日栏。

支持 Harness 范围的是从已验证开发经历提炼并在后续开发任务中检索的 collaboration contracts：它们修改角色输入输出、依赖与验证流程。游戏 skeleton 和 gameplay module 是外部产物，不能一并认定为 Harness。

正文明确将 validated projects 蒸馏为经验并初始化 future development runs，消融将独立任务产生的经验迁移到不同模型的 ablation tasks；契约是程序性流程文件，区别于仅累积游戏素材。

关键原文：

- **training_free_reuse** · [S3.SS3.p1](https://arxiv.org/html/2610.33106v1#S3.SS3.p1)：VibeGame distills reusable experience from these validated projects with a training-free self-evolution mechanism and uses it to initialize future development runs, preserving implicit development knowledge that general-purpose agents lose across independent runs.
- **workflow_artifact** · [S3.SS3.p4](https://arxiv.org/html/2610.33106v1#S3.SS3.p4)：A contract is a document that adapts the general AAT workflow to a recurring feature or development pattern.
- **workflow_artifact** · [S3.SS3.p4](https://arxiv.org/html/2610.33106v1#S3.SS3.p4)：It specifies the role-specific inputs, outputs, dependencies, and verification criteria required to implement that feature, enabling agents to coordinate through a validated procedure rather than relying only on the generic build-and-review loop.
- **external_artifact_boundary** · [S3.SS3.p2](https://arxiv.org/html/2610.33106v1#S3.SS3.p2)：A skeleton is a runnable project template associated with a particular game type.
- **external_artifact_boundary** · [S3.SS3.p3](https://arxiv.org/html/2610.33106v1#S3.SS3.p3)：A module is a self-contained behavior script that can be attached to any node
- **feedback** · [S8.SS1.p2](https://arxiv.org/html/2610.33106v1#S8.SS1.p2)：using the task rubrics and the vision-language model (VLM) judge scores in place of user feedback.
- **cross_task_reuse** · [S8.SS1.p2](https://arxiv.org/html/2610.33106v1#S8.SS1.p2)：We then add the evolved artifacts to the initial project of VibeGame with GPT-5.6-Luna and let it build the ablation tasks.
- **evolution_tasks** · [S8.SS1.p2](https://arxiv.org/html/2610.33106v1#S8.SS1.p2)：build and self-evolve on 5 tasks randomly sampled from outside the ablation set
- **evaluation_tasks** · [S7.p1](https://arxiv.org/html/2610.33106v1#S7.p1)：The ablation set is a 10-task subset of the test set.
- **aggregate_experience_result** · [S4.SS2.SSS0.Px3.p1](https://arxiv.org/html/2610.33106v1#S4.SS2.SSS0.Px3.p1)：Adding the experience evolved by GPT-6.1-Sol to GPT-5.6-Luna raises the overall score by 2.92 points
- **main_experiment_boundary** · [S13.p1](https://arxiv.org/html/2610.33106v1#S13.p1)：the main experiments use VibeGame without any accumulated experience, and we evaluate self-evolution separately in the ablation study.
- **negative_transfer** · [S13.p1](https://arxiv.org/html/2610.33106v1#S13.p1)：We observe that when VibeGame continuously develops games of different types, the experience accumulated by self-evolution can instead lower agent performance.

限制：

- skeleton 是游戏模板；module 是附在游戏节点上的行为脚本。即使带静态自检规则，也不能仅靠可复用一词把游戏代码算 Agent Harness。
- 主实验使用无积累经验的 VibeGame；主实验 +4.19 是固定系统的整体比较，不是自演化收益。
- 经验消融由 5 个 ablation set 外任务产生工件，在 10 个 ablation tasks 上评测；+2.92 是 skeleton/module/contracts 合并包的效果，不能单独归因 contracts。
- 论文明确报告跨游戏类型连续开发时经验积累可能降低表现，不能描述为持续单调进步。
- 本轮未克隆/执行代码，也未核验契约的每次文件 diff；收录依据是论文方法和消融协议，不是独立复现。

后续：仅用于 10/30 HF 期或明确标注日期的历史补录；摘要应区分契约演化与游戏产物，并保留经验消融和负迁移限制。

canonical source hash：`899924f633f630a95d87afb6feef83295a7340ed8ac1e901502b0e5a070f0de8`；原正文 SHA-256：`31d8ff8394d85823b020b293698ceda436c6de5d22c8ad9edd8bea5c83d9b85d`。

## 数据问题（只报告）

- arxiv:2610.33245：canonical 为 Carolyn P. Rosé，官方 Atom 为 Carolyn Rosé；是中间名表示差异，本轮只报告，不据此判为身份错误。
- arxiv:2610.36077：Wangbo Zhao Kaipeng Zhang 在 canonical 与官方 Atom 都作为同一 author name 出现；是上游也存在的连写，不自行拆分。
- arxiv:2610.33245：10/30 模型报告 reason 写 77 次新增，limitations 写 177 次新增，内部矛盾；不复用该数值。

完整逐项证据、旧结论和哈希见 [oct28-review.json](oct28-review.json)。所有本报告 formal_decision 保持 defer；是否使用 owner 既有批准由主流程单独核对，不由本报告自动授予。
