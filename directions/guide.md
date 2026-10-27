# Harness 自进化导读 / A guide to harness self-evolution

[网站导读 / Website guide](https://adongwanai.github.io/follow-rsi/guide.html) · [论文证据库 / Evidence base](../README.md#证据库)

## 中文

Harness 是模型周围让 Agent 真正完成任务的程序：执行循环、工具接口、上下文与记忆管理、验证器和停止条件。读「自进化」论文时，先找出一轮结束后留下了什么，以及下一轮怎样使用它。一个被保存并复用的代码修改，与仅对当前答案再试一次，需要分别记录。

### 进化什么

- **组件与执行流程。** [AHE](../papers/ahe.md)把组件放进文件，用分层轨迹帮助定位修改，并要求每次编辑给出下一轮可核验的预测。[ModularRSI](../papers/modularrsi.md)将执行循环、工具使用、观测管理、上下文管理、完成检测分别在受限范围内演化，再合并。
- **改进器本身。** [Hyperagents](../papers/hyperagents.md)把任务 Agent 与元 Agent 放入同一个可编辑程序；[HSI](../papers/hsi.md)区分任务 Harness、演化器和元演化器，并保留冻结的最外层锚点。看这一类工作，还要追问：改写编辑流程之后，它是否真的更会改进了？
- **模型与 Harness 协同。** [HarnessX](../papers/harnessx.md)既把轨迹转成 Harness 更新，也将不同版本下的轨迹用于权重训练。读结果时应分别寻找 Harness 更新、权重更新及两者组合的对照。

### 结构是什么

`topology` 描述候选版本之间的关系。**链（chain）**沿一个后继版本继续；**树（tree）**从一个版本分出多个后代；**图（graph）**允许更一般的连接，例如一个候选组合多个祖先的内容。这些词描述搜索结构，不代表证据强弱，也不等于运行时 Agent 之间的通信结构。

目录中没有审定拓扑的条目保留 `unknown`。不能仅凭方法名或摘要里的「种群」二字替论文填入分类。

### 谁来更新

`self` 表示由被研究的 Agent 自身提出修改；`external` 表示由外部编辑 Agent 提出；`trained` 表示使用经过训练的改进器；`self_human_reviewed` 表示自身提出、由人审核。阅读时还应分别确认谁提出、谁验证、谁批准保存：三个角色不一定相同。

例如，[Self-Harness](../papers/self-harness.md)从弱点挖掘开始，提出最小修改，通过回归测试后才接受；[Meta-Harness](../papers/meta-harness.md)由编码 Agent 读取历史候选代码、分数和轨迹，搜索新的 Harness。编辑器是否更强、能看到哪些信息，都影响比较是否公平。

### 何时更新

`offline` 是部署前用一批任务改进；`online` 是随实际使用不断积累反馈并更新；`test_time` 是围绕测试任务进行适应；`during_run` 是在一次任务尚未结束时修改。读论文时把「何时提出修改」和「修改何时生效」分别记下来。

[AutoSaddler](../papers/autosaddler.md)提供一个离线工程闭环：诊断失败轨迹，修改提示、工具或中间件，再用验证集与 EvoDAG 选择版本。[Harness²](../papers/harness2.md)讨论没有真值验证器的开放世界；这时还要看代理反馈是否能可靠地选出更好的版本。

### 证据怎么看

| 问题 | 正文中要找什么 |
| --- | --- |
| 留出集真的留出了吗？ | 演化、选择与最终评估分别用了哪些任务，编辑器能看到哪些答案或轨迹。 |
| 同预算比较了吗？ | 反馈次数、推理计算和搜索开销是否对齐；更高分是否只是用了更多计算。 |
| 改进能迁移吗？ | 新任务、任务分布或执行模型上的独立结果；一次测试上的不退化不等于普遍不退化。 |
| 代价完整吗？ | 演化阶段与部署阶段分别用了多少 token、时间和费用，是否计入失败候选。 |

[StarHarness](../papers/starharness.md)明确分开提议器可见的搜索任务、隐藏的选择任务与最终留出任务；[Rethinking the Evaluation](../papers/rethinking-evaluation.md)和 [Harness-Delta Attribution](../papers/hda.md)帮助追问同预算下收益的来源；[Auditing the Product, Not the Recursion](../papers/auditing-product.md)进一步追问改进流程本身是否变好。

证据卡中的 `yes`、`partial`、`no`、`na` 和 `unknown` 含义不同。`unknown` 表示尚未审定，不等于论文没有做。本文按现有目录组织阅读，不新增任何证据审计结论；每日动态的自动摘要检查也不能替代正文审计。

### 从哪里开始读

1. **打基础：** [ADAS](../papers/adas.md) → [DGM](../papers/dgm.md) → [Meta-Harness](../papers/meta-harness.md) → [Hyperagents](../papers/hyperagents.md)。先理解设计搜索、自改代码与可编辑的改进器。复现 DGM 或 Hyperagents 前，配合阅读 [Reflections on Trusting Trust, Revisited](../papers/trusting-trust-revisited.md) 中的基线泄漏问题。
2. **方法主线：** [AHE](../papers/ahe.md) → [Self-Harness](../papers/self-harness.md) → [DarwinX](../papers/darwinx.md) → [ModularRSI](../papers/modularrsi.md) → [RRSI](../papers/rrsi.md)。比较编辑依据、接受规则与修改范围。
3. **工程实践：** [AutoSaddler](../papers/autosaddler.md) → [ModularRSI](../papers/modularrsi.md) → [RiseHarness](../papers/riseharness.md)。关注从失败轨迹到代码的闭环，以及重复运行时的可靠性。
4. **实验设计：** [Rethinking the Evaluation](../papers/rethinking-evaluation.md) → [HDA](../papers/hda.md) → [HarnessOpt-Bench](../papers/harnessopt-bench.md) → [Auditing the Product](../papers/auditing-product.md) → [Trusting Trust, Revisited](../papers/trusting-trust-revisited.md)。在复现或提出新方法之前读这一条。

完整路线与原始条目见 [routes.yaml](../data/routes.yaml) 和 [papers.yaml](../data/papers.yaml)。

## English

A harness is the program around a model that lets an agent complete tasks: the execution loop, tool interfaces, context and memory management, verifiers, and stopping conditions. When reading a self-evolution paper, first identify what survives a round and how the next round uses it. Record a saved, reusable code change separately from another attempt at the current answer.

### What evolves

- **Components and execution workflows.** [AHE](../papers/ahe.md) exposes components as files, uses hierarchical trajectories to locate edits, and attaches a prediction that can be checked in the next round. [ModularRSI](../papers/modularrsi.md) evolves the execution loop, tool use, observation management, context management, and completion detection within restricted scopes, then merges them.
- **The improver itself.** [Hyperagents](../papers/hyperagents.md) combines the task agent and meta agent in one editable program. [HSI](../papers/hsi.md) distinguishes the task harness, evolver, and meta-evolver while keeping an outermost anchor frozen. Ask whether changing the editing procedure actually makes that procedure better at improving agents.
- **Models and harnesses together.** [HarnessX](../papers/harnessx.md) turns trajectories into harness updates and uses trajectories from different harness versions for weight training. Look for separate controls for harness updates, weight updates, and their combination.

### How candidates are structured

`topology` describes relationships between candidate versions. A **chain** continues through a single successor; a **tree** branches into multiple descendants; a **graph** permits more general connections, such as a candidate combining material from multiple ancestors. These terms describe search structure, not evidence strength or the communication structure of agents at runtime.

Entries whose topology has not been reviewed remain `unknown`. A method name or the word “population” in an abstract is insufficient to assign a category.

### Who updates it

`self` means the agent under study proposes edits; `external` means an external editing agent proposes them; `trained` denotes a trained improver; `self_human_reviewed` means the agent proposes edits and a human reviews them. Separately identify who proposes, validates, and approves a persistent change: these roles can differ.

[Self-Harness](../papers/self-harness.md), for example, mines weaknesses, proposes minimal changes, and accepts them after regression tests. [Meta-Harness](../papers/meta-harness.md) uses a coding agent that reads historical candidate code, scores, and trajectories to search for harnesses. The editor’s capability and access to information affect the fairness of comparisons.

### When updates happen

`offline` means improvement on a task batch before deployment; `online` means accumulating feedback and updating through use; `test_time` means adaptation around test tasks; `during_run` means changing the harness before a task run finishes. Record when an edit is proposed and when it takes effect separately.

[AutoSaddler](../papers/autosaddler.md) illustrates an offline engineering loop: diagnose failure trajectories, patch prompts, tools, or middleware, then select versions using a validation set and EvoDAG. [Harness²](../papers/harness2.md) addresses an open world without a ground-truth verifier, where the reliability of proxy feedback becomes another question.

### How to read the evidence

| Question | What to locate in the paper |
| --- | --- |
| Is the held-out set really held out? | Which tasks are used for evolution, selection, and final evaluation; which answers and trajectories the editor can access. |
| Are budgets matched? | Feedback, inference compute, and search costs; whether a higher score follows from additional computation. |
| Do gains transfer? | Independent results on new tasks, distributions, or execution models; non-regression on one finite set is not a universal guarantee. |
| Are costs complete? | Evolution and deployment tokens, time, and money, including unsuccessful candidates. |

[StarHarness](../papers/starharness.md) separates proposer-visible search tasks, hidden selection tasks, and final held-out tasks. [Rethinking the Evaluation](../papers/rethinking-evaluation.md) and [Harness-Delta Attribution](../papers/hda.md) examine where gains come from under matched budgets. [Auditing the Product, Not the Recursion](../papers/auditing-product.md) asks whether the improvement procedure itself gets better.

Evidence cards distinguish `yes`, `partial`, `no`, `na`, and `unknown`. `unknown` means not yet adjudicated, not that the paper omitted the experiment. This guide organizes the existing catalog and adds no evidence-audit findings. Automatic checks on daily summaries do not replace a full-paper audit.

### Suggested reading routes

1. **Foundations:** [ADAS](../papers/adas.md) → [DGM](../papers/dgm.md) → [Meta-Harness](../papers/meta-harness.md) → [Hyperagents](../papers/hyperagents.md). Follow design search, self-modifying code, and editable improvers. Before reproducing DGM or Hyperagents, read the baseline leakage findings in [Reflections on Trusting Trust, Revisited](../papers/trusting-trust-revisited.md).
2. **Mainline methods:** [AHE](../papers/ahe.md) → [Self-Harness](../papers/self-harness.md) → [DarwinX](../papers/darwinx.md) → [ModularRSI](../papers/modularrsi.md) → [RRSI](../papers/rrsi.md). Compare the evidence used for edits, acceptance rules, and editing scope.
3. **Engineering practice:** [AutoSaddler](../papers/autosaddler.md) → [ModularRSI](../papers/modularrsi.md) → [RiseHarness](../papers/riseharness.md). Follow the loop from failure trajectories to code and examine reliability across repeated runs.
4. **Experimental design:** [Rethinking the Evaluation](../papers/rethinking-evaluation.md) → [HDA](../papers/hda.md) → [HarnessOpt-Bench](../papers/harnessopt-bench.md) → [Auditing the Product](../papers/auditing-product.md) → [Trusting Trust, Revisited](../papers/trusting-trust-revisited.md). Read this route before reproducing or proposing a method.

The complete routes and original entries are in [routes.yaml](../data/routes.yaml) and [papers.yaml](../data/papers.yaml).

## 一分钟讲解 / One-minute introduction

<!-- TODO -->
