# 其它来源补录：第一轮独立审查

**8 条：2 篇 Harness 候选、1 篇边界项、1 篇其他方向、4 篇排除。** 全部是来源补录，不计入 10-29 HF 当日推荐。

本轮仅使用原始摘要，全文审读 0 篇。全部 decision=defer，未发生人工接收或发布。后续轮次若获得新证据，需保留与本轮结论的差异。

| 条目 | 首发日期 | 建议 | 原因 |
| --- | --- | --- | --- |
| [iPrefBench: A User-Centric Benchmark for Personalized Mobile Use Agents](https://arxiv.org/abs/2610.34735v1) | 2026-10-26 | exclude / evaluation_benchmark / 无 | 评测推断用户偏好和询问缺失信息的能力，不研究反馈驱动的 Harness 演化。 |
| [ReGE: Stronger Agents through Experience Synthesis](https://arxiv.org/abs/2610.33861v1) | 2026-10-24 | exclude / experience_world_model / 无 | 把任务执行记录整理为同任务新尝试的指导；没有跨任务保留的 Harness 工件演化证据。 |
| [How Far Can Coding Agents Go in Visual Generation?](https://arxiv.org/abs/2610.19025v1) | 2026-10-13 | exclude / evaluation_benchmark / 无 | 研究编码 Agent 的绘图能力和内部表征；可执行绘图程序是任务产物，不是 Harness 自更新。 |
| [CRM-Agent-Bench: Benchmarking Tool-Using Agents in Stateful Enterprise Environments](https://arxiv.org/abs/2610.32004v1) | 2026-10-23 | exclude / evaluation_benchmark / 无 | 评测有状态企业任务的执行正确性、成本与合规，没有专门评测 Harness 自演化。 |
| [When the Critic Falls Behind: Co-Evolving Rubrics and Harnesses for Continual Agent Self-Improvement](https://arxiv.org/abs/2610.36826v1) | 2026-10-27 | harness / harness / improver | 执行轨迹推动 rubric 重审并指导 Harness 更新，改进机制自身跨演化轮次变化。 |
| [OmniBrain-0: A Unified Agentic Model for Embodied Intelligence](https://arxiv.org/abs/2610.36013v1) | 2026-10-26 | other_direction / model_weights / 无 | 摘要的主要闭环是执行证据生成训练材料、更新专家，再经蒸馏统一模型。 |
| [GEPA-Curator: Curated Learning for Self Improving Agents](https://arxiv.org/abs/2610.37651v1) | 2026-10-27 | borderline / harness / evidence_selection | 明确筛选给提示优化器的经验反馈，但摘要未明确优化后提示的新版本如何保留复用。 |
| [Skill Dreaming: Evolving Repository Skills through Pull Request Streams](https://arxiv.org/abs/2610.36188v1) | 2026-10-26 | harness / harness / component | 验证过的 PR 提炼为可执行技能，技能指导后续 PR，其结果继续修订技能库。 |

## 逐篇依据

### iPrefBench: A User-Centric Benchmark for Personalized Mobile Use Agents

- 方向建议：evaluation_benchmark / 无；对象：无演化对象：个性化交互评测。
- 判定理由：交互模拟用户、活动历史和可执行 iOS 环境属于评测设置；摘要没有 Agent 修改并保留自己的提示、工具代码、工作流或记忆管理机制。
- 对象引句：a benchmark for evaluating the infer and ask capabilities of personal mobile-use agents in an executable iOS environment with an interactive simulated user.
- 反馈：unclear；无可直接支持的原文，保留未知。
- 保留/复用：unclear；无可直接支持的原文，保留未知。
- 待核：仅读摘要，未审正文。

### ReGE: Stronger Agents through Experience Synthesis

- 方向建议：experience_world_model / 无；对象：同任务重试的经验指导。
- 判定理由：摘要明确 student 从该任务初始环境重新开始，并把 task-specific findings 汇成 guidance。变化的是当前任务的经验指导，不是已证明跨任务复用的系统提示/技能程序；不因 fresh attempt、无参数更新或 guidance 文本就当 Harness。按摘要所述范围建议 not_persistent；若全文有跨任务程序性技能更新证据，应在后续轮次重新审。
- 对象引句：a single coach call to jointly synthesize bounded execution records and available artifacts into self-contained guidance, connecting task-specific findings with proposed actions and relevant pitfalls.
- 反馈：yes；Repeated attempts at interactive tasks uncover facts, useful operations, and failures that can inform subsequent execution.
- 保留/复用：unclear；无可直接支持的原文，保留未知。
- 待核：仅读摘要，未审正文。；没有证明可执行程序工件或更新版本跨任务保留；广义经验 RSI 的持续复用范围也不明确。

### How Far Can Coding Agents Go in Visual Generation?

- 方向建议：evaluation_benchmark / 无；对象：生成图像的任务代码。
- 判定理由：摘要提到 demonstration-derived procedural skills 和 cross-harness drawing，但没有执行反馈更新 Agent 自身工件并跨后续任务保留的机制；接口比较和世界一致性不能替代自进化证据。
- 对象引句：general-purpose coding agents that construct images through executable programs.
- 反馈：unclear；无可直接支持的原文，保留未知。
- 保留/复用：unclear；无可直接支持的原文，保留未知。
- 待核：仅读摘要，未审正文。

### CRM-Agent-Bench: Benchmarking Tool-Using Agents in Stateful Enterprise Environments

- 方向建议：evaluation_benchmark / 无；对象：无演化对象：CRM 任务评测。
- 判定理由：可执行任务契约和系统级评估是固定基准的检查机制，不构成基于反馈修改并保留 Agent 程序的演化过程。
- 对象引句：We evaluate the complete agent system through these contracts and report scored coverage, latency, and cost.
- 反馈：unclear；无可直接支持的原文，保留未知。
- 保留/复用：unclear；无可直接支持的原文，保留未知。
- 待核：仅读摘要，未审正文。

### When the Critic Falls Behind: Co-Evolving Rubrics and Harnesses for Continual Agent Self-Improvement

- 方向建议：harness / improver；对象：演化 rubric 与 Harness 更新。
- 判定理由：摘要同时指向演化 Harness 和演化其监督准则，执行经验改变用于下一轮的改进标准与目标更新。因此建议 improver，改进对象为环内验证/评价准则以及被它指导的外部 Harness。co-evolution 在这里是 rubric 与 Harness，不是模型权重+Harness，不能仅凭词面归 coevolution。
- 对象引句：a rubric--harness co-evolution framework for continual agent self-improvement.
- 反馈：yes；discovers and reassesses behavioral criteria from execution trajectories, prioritizes the most relevant unresolved weaknesses, and uses them to guide targeted harness updates
- 保留/复用：yes；adaptive rubric prioritization tracks shifting weaknesses and supports more sustained improvement and stable generalization across evolution rounds.
- 待核：仅读摘要，未审正文；具体 Harness 工件格式、rubric 版本保留实现、准入和独立留出设置仍需全文核查。；摘要未明确模型冻结，保留 unclear；主要宣称的演化对象是外部 rubric/Harness。

### OmniBrain-0: A Unified Agentic Model for Embodied Intelligence

- 方向建议：model_weights / 无；对象：具身专家与统一模型权重。
- 判定理由：第一轮只看摘要：rubrics 和 step-level reminders 被描述为 data flywheel 中用于 domain-expert updates 的材料，随后 MOPD reconsolidation 指向模型权重更新。摘要没有独立说明可复用 reminder-policy 等外部程序在冻结模型时如何修订、接受并带到后续轮次，因此本轮不判 Harness/coevolution。此结论不排除正文提供额外外部工件证据，后续轮次应单独记录而不覆盖本轮。
- 对象引句：Unification therefore occurs within the learned decision model rather than only at the tool interface.
- 反馈：yes；a Meta-Agent turns execution evidence into refined rubrics, step-level reminders, and verified trajectories for domain-expert updates
- 保留/复用：yes；before their reconsolidation into OmniBrain-0 through MOPD.
- 待核：仅读摘要，未审正文。；需全文核实 refined rubrics / step-level reminders 是训练数据，还是也形成被持久更新的独立外部策略工件。

### GEPA-Curator: Curated Learning for Self Improving Agents

- 方向建议：harness / evidence_selection；对象：候选：提示优化的证据选择。
- 判定理由：主要改进对象可合理定位为系统提示，研究任务/证据选择如何提高提示优化；这与单纯检索当前任务经验不同。但不能凭 GEPA 名称或 self-improving 标题补出外部提示跨任务/轮次保留机制。prior success retrieval 明说复用的是历史轨迹，不等于更新后的提示版本被持续复用；摘要层面保留 borderline / evidence_selection。
- 对象引句：a framework that augments the prompt optimizer to select which agent experiences should shape prompt optimization.
- 反馈：yes；task curation, which filters out tasks that are likely to provide noisy or unreliable learning signals
- 保留/复用：unclear；无可直接支持的原文，保留未知。
- 待核：仅读摘要，未审正文。；需核实提示候选的验证、接受与跨任务/后续改进轮次复用；摘要未给出相应持久化引句。；保留模型冻结 unclear，不借用对 GEPA 算法的先验记忆。

### Skill Dreaming: Evolving Repository Skills through Pull Request Streams

- 方向建议：harness / component；对象：随 PR 结果修订的可执行技能库。
- 判定理由：被保留复用的是 repository-specific executable skill library，而不仅是外部仓库代码产物或 PR 经验条目。摘要明确给出 validated PRs → 技能持续修订 → future PRs → outcomes 反馈更新，符合组件级 Harness 演化。仍需全文确认技能工件格式以及验证/拒绝不良技能的机制。
- 对象引句：builds a repository-specific skill library by extracting executable knowledge from validated PRs and continuously refines the skills as new PR information becomes available.
- 反馈：yes；incorporating subsequent PR outcomes into future skill updates.
- 保留/复用：yes；This creates a mutually reinforcing cycle: PRs provide knowledge for updating skills, while these skills improve future PRs, maintain repositories, and support further skill evolution.
- 待核：仅读摘要，未审正文；技能文件的实际格式及可执行性仍需确认。；模型冻结与独立评估、成本公平性没有明确陈述，保持未知。

## 来源与核验

- 8/8 arXiv 标题匹配；原始发表/更新日期独立核实，原输入日期另行原样保留。
- 4 条旧 HF 输入没有 HF 推荐日字段；没有用 first_seen=10-28 推造推荐日。
- 所有非空引句为原始摘要连续子串，长度均不超过 200 字符。
- 本轮保留 OmniBrain-0 的摘要判断：主要是模型/数据飞轮，尚无明确外部策略版本保留证据。正文若出现独立 reminder-policy 演化，应作为后续轮次的新证据处理。
- 未写队列、论文库或来源原始数据，未调用付费模型，未 commit/push。
