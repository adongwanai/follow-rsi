# AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2608.23041) · [HF](https://huggingface.co/papers/2608.23041)

2026-08-24 ·  · 1.1 搜索与演化主线

**必读 / MUST READ**

| 证据字段 | 记录 |
| --- | --- |
| 留出集 | ✅ 有 |
| 同预算对照 | ❔ 未审 |
| 跨模型迁移 | ❔ 未审 |
| 报告成本 | ❔ 未审 |
| 不相交演化集 | ❔ 未审 |
| 可靠性指标 | ❔ 未审 |
| 开源代码 | ❔ 未审 |
| 公开演化出的 Harness | ❔ 未审 |
| 谁来改 |  外部改进器 |
| 反馈来源 | ❔ 未审 |
| 改进时机 | ❔ 未审 |
| 演化结构 | ❔ 未审 |

**一句话**：离线 mini-batch：失败轨迹深度诊断 → 覆盖提示、工具、中间件的结构化代码补丁 → 验证集与 EvoDAG 做泛化感知选择。理解完整工程闭环的入口。

**关键结果**：GAIA2、SWE-Bench Pro、TB2.0 相对基础 Harness +9.0/+9.6/+10.0pp，比最强自动化基线高 7.4/4.4/6.7pp；消融支持深度调试、定向修改、泛化选择三要素。

<details><summary>English</summary>

| Evidence field | Record |
| --- | --- |
| Held-out evaluation | ✅ yes |
| Matched-budget baseline | ❔ not yet reviewed |
| Cross-model transfer | ❔ not yet reviewed |
| Cost reported | ❔ not yet reviewed |
| Disjoint evolution set | ❔ not yet reviewed |
| Reliability metric | ❔ not yet reviewed |
| Code released | ❔ not yet reviewed |
| Evolved harness released | ❔ not yet reviewed |
| Who edits |  external |
| Feedback | ❔ not yet reviewed |
| Timing | ❔ not yet reviewed |
| Topology | ❔ not yet reviewed |

**Summary**: Offline mini-batches: deep diagnosis of failure trajectories → structured code patches covering prompts, tools, and middleware → generalization-aware selection using a validation set and EvoDAG. An entry point to the complete engineering loop.

**Key result**: On GAIA2, SWE-Bench Pro, and TB2.0: +9.0/+9.6/+10.0pp over the base harness, and 7.4/4.4/6.7pp above the strongest automated baseline; ablations support deep debugging, targeted edits, and generalization-aware selection.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [StarHarness: Evolving Harnesses with Stratified Search for Enterprise Environments](starharness.md)
- [Ouroboros: A Self-Developing Coding Harness with Reviewed Core Evolution](ouroboros.md)
- [Mendel Gödel Machine: Recursive Self-Improving Coding Agents via Comparative Evolution](mgm.md)
- [ModularRSI: Modular and Generalizable Recursive Harness Self-Improvement](modularrsi.md)
- [RiseHarness: Harness Self-Evolution for Long-Horizon Terminal Agents](riseharness.md)

<!-- AUTO:RELATED:END -->
