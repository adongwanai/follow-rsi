# RSIHub: A Composable Framework for Agent-Evolution Methods

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2610.32253) · [HF](https://huggingface.co/papers/2610.32253) · [Code](https://github.com/simple-agent-lab/RSIHub)

2026-10-23 · University of California, Berkeley · University of Science and Technology of China · Douyin Group · Shanghai Jiao Tong University · Tongji University · Beijing Institute for General Artificial Intelligence · Simple Agent Lab · 五、评测、归因与可信度



| 证据字段 | 记录 |
| --- | --- |
| 留出集 | ✅ 有 |
| 同预算对照 | ❔ 未审 |
| 跨模型迁移 | ❌ 没有 |
| 报告成本 | ❔ 未审 |
| 不相交演化集 | ◐ 部分 |
| 可靠性指标 | ◐ 部分 |
| 开源代码 | ✅ 有 |
| 公开演化出的 Harness | ❔ 未审 |
| 谁来改 |  外部改进器 |
| 反馈来源 |  标准答案 |
| 改进时机 |  离线 |
| 演化结构 | ❔ 未审 |

**一句话**：用于实现和比较 Harness 演化方法的开源框架：以 recipe 和算子接入 AHE、Hyperagents、A-Evolve、GEPA，保护评估边界并保存候选谱系；在同一底模下比较 MiniSWE 与 Codex，并保留 sealed 任务检验泛化。

**关键结果**：TB2 + MiniSWE 中 Hyperagents 与 A-Evolve 从 56.2 到 69.7（+13.5 个百分点）；排名与留出收益随设置变化。效果为单次点估计，split 列按全基准任务数作分母，未确认完整匹配 token 预算。

<details><summary>English</summary>

| Evidence field | Record |
| --- | --- |
| Held-out evaluation | ✅ yes |
| Matched-budget baseline | ❔ not yet reviewed |
| Cross-model transfer | ❌ no |
| Cost reported | ❔ not yet reviewed |
| Disjoint evolution set | ◐ partial |
| Reliability metric | ◐ partial |
| Code released | ✅ yes |
| Evolved harness released | ❔ not yet reviewed |
| Who edits |  external |
| Feedback |  ground_truth |
| Timing |  offline |
| Topology | ❔ not yet reviewed |

**Summary**: An open-source framework for implementing and comparing harness-evolution methods. Recipes compose AHE, Hyperagents, A-Evolve, and GEPA with protected evaluation and candidate lineage; experiments compare MiniSWE and Codex under the same underlying model with separate sealed tasks.

**Key result**: On TB2 with MiniSWE, Hyperagents and A-Evolve improve 56.2 to 69.7 (+13.5 points). Rankings and held-out gains vary. Evolution results are single-run estimates; split columns use full-benchmark denominators, and a fully matched token budget was not established.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:NOTES:START -->

## 精读笔记：RSIHub

核对日期：2026-10-30。核对官方 v1 正文、表格、项目页和公开代码；下列“支持”表示论文这样报告，未独立复现实验。当前收录定位为 Harness 评测与基础设施（harness_eval），不计入 core 方法数。

### 这篇到底改什么

候选可以是提示、技能、工具或整套可运行 Harness。recipe 定义可修改资源和算子，执行反馈驱动候选修改；被保留的 Git commit 和结果进入谱系，供后续代选择。目标与修改者的模型配置固定，没有参数训练步骤。

论文实际比较固定 recipe 下的 AHE、Hyperagents、A-Evolve、GEPA；外层 agent 自适应改 recipe 是框架支持的能力，本文实验没有验证其收益。§3.2 原文明确写：“Our experiments evaluate fixed recipes.”

### 实验设置与分母

- 两种执行 Harness 是 MiniSWE 与 Codex，底层均为 GPT-5.4 high；修改者为 GPT-5.4 xhigh 支持的 Codex agent。两种 Harness 不是两个模型家族。
- Terminal-Bench 2 共 89 题：train 50、gate 19、sealed 20；τ³ Banking 共 97 题：train 50、gate 20、sealed 27。
- 每代一个候选，最多 10 代，每题一次评估，报告 pass@1。
- train 提供修改反馈，gate 支持候选准入；sealed 不进入修改反馈。
- 表 1 的每个 split 列按全基准题数作分母，即 N_pass,split / N_all。不能把它读成该 split 内的成功率。

### 主要结果

| 基准 / 执行 Harness | Seed | AHE | Hyperagents | A-Evolve | GEPA |
|---|---:|---:|---:|---:|---:|
| Terminal-Bench 2 / MiniSWE | 56.2 | 65.2 | 69.7 | 69.7 | 64.0 |
| Terminal-Bench 2 / Codex | 69.7 | 71.9 | 70.8 | 70.8 | 69.7 |
| τ³ Banking / MiniSWE | 27.8 | 28.9 | 33.0 | 27.8 | 29.9 |
| τ³ Banking / Codex | 24.7 | 34.0 | 28.9 | 28.9 | 33.0 |

这些是表 1 的总 pass@1 百分数。Terminal-Bench 2 + MiniSWE 的 +13.5 个百分点由 Hyperagents 和 A-Evolve 共同达到；不是只有 Hyperagents 第一。

τ³ Banking + MiniSWE 的 sealed 列中，AHE 从 9.3 到 5.2，Hyperagents 与 GEPA 从 9.3 到 7.2。下降的 4.1、2.1、2.1 个百分点是对全 97 题 pass@1 的贡献变化，不是 27 道 sealed 题内部的成功率变化。

Codex 增益在 Terminal-Bench 2 较小（+0 至 +2.2），但在 τ³ Banking 仍为 +4.2 至 +9.3。不能从其中一个基准推出“执行 Agent 越强，演化收益就消失”。

### 证据边界

- **留出集：有。** 本次实验 sealed 独立于修改反馈；框架通用合同允许 gate 与 train 重合，不能把三个分区永远不交叠当成所有配置的保证。
- **同预算对照：unknown。** 固定模型配置和最多 10 代，不等于匹配完整 token/计算成本的多采样或顺序修正对照；未确认实际总预算是否相等。
- **跨模型：没有相应测试。** MiniSWE 与 Codex 均使用 GPT-5.4。
- **成本：unknown。** 附录 B.2 报告框架时延，未核到包含模型推理与演化的完整 token/美元成本。
- **可靠性：部分。** 三次重复属于 unchanged-seed 执行保真控制。表 1 的演化增益为单次点估计，不能借控制重复宣布增益稳定或显著。
- **开源：框架代码有，最终演化产物 unknown。** 已核官方仓库和 Apache-2.0 许可；未找到与表 1 对应的最终候选快照及每题原始结果。

### 代码检查

官方仓库：[simple-agent-lab/RSIHub](https://github.com/simple-agent-lab/RSIHub)，检查提交 d6554299c58bf0fe2db04ddda0277f9db67ea680。

源码支持冻结 evaluator、干净候选 checkout、sealed anchor 不进入修改反馈。AHE artifact-valid 和 parent-eligible gate 并不要求严格超过父代分数，因此“候选被准入”不能翻译成“该候选已经证实更好”。当前默认 AHE recipe 使用 30-task 演示配置，不能当作论文全部 89 题实验的复现命令。

本次是阅读代码，未执行演化实验，也不是安全审计。论文 §6 明确说框架不提供敌意代码的隔离 containment。

### 来源与日期

- [论文元数据](https://arxiv.org/abs/2610.32253)：v1 提交 2026-10-23 07:06:07 UTC；PDF 封面写 2026-10-22。目录采用 arXiv 首次提交日。
- [正文 §4.2](https://arxiv.org/html/2610.32253#S4.SS2)：模型、任务分区、分母和重复次数。
- [表 1 与 §4.3](https://arxiv.org/html/2610.32253#S4.T1)：结果、条件差异与稳定性限制，PDF p. 8。
- [§4.4](https://arxiv.org/html/2610.32253#S4.SS4)：执行保真控制不能证明演化增益的显著性。
- [官方项目](https://simpleagentlab.com/rsihub/)。

作者（arXiv 顺序）：Zimu Wang, Xiaobo Wang, Siyu Ye, Jiaqi Li, Silin Chen, Yuling Shi, Ruobing Wang, Jingjing Zhang, Chaofan Wang, Kai Wu, Mengnan Qi, Kai Cai, Xiaodong Gu, Zilong Zheng。

机构（PDF 首页）：University of California, Berkeley; University of Science and Technology of China; Douyin Group; Shanghai Jiao Tong University; Tongji University; Beijing Institute for General Artificial Intelligence; Simple Agent Lab。

正文抓取时间：2026-10-30T03:08:42.299414+00:00。HTML SHA-256：bd8cdbd8bc3af4bb5f4b48e3a715c175163e56f6f83d667851a3675d78600d8c。

<!-- AUTO:NOTES:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [Can LLMs Improve Their Own Harness? A Controlled Study on ARC-AGI-3](arc-agi-3-controlled.md)
- [Harness-Delta Attribution: Dissecting Gains From Harness Evolution](hda.md)
- [Auditing the Product, Not the Recursion](auditing-product.md)
- [RSIGym](rsigym.md)
- [Rethinking the Evaluation of Harness Evolution for Agents](rethinking-evaluation.md)
- [HarnessDev: Can LLMs Create and Evolve Their Own Agent Harness?](harnessdev.md)
- [HarnessOpt-Bench: Evaluating LLMs at Harness Optimization](harnessopt-bench.md)
- [Reflections on Trusting Trust, Revisited](trusting-trust-revisited.md)

<!-- AUTO:RELATED:END -->
