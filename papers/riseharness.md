# RiseHarness: Harness Self-Evolution for Long-Horizon Terminal Agents

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2610.27435) · [HF](https://huggingface.co/papers/2610.27435)

2026-10-20 ·  · 1.1 搜索与演化主线



| 证据字段 | 记录 |
| --- | --- |
| 留出集 | ✅ 有 |
| 同预算对照 | ❔ 未审 |
| 跨模型迁移 | ❔ 未审 |
| 报告成本 | ❔ 未审 |
| 不相交演化集 | ❔ 未审 |
| 可靠性指标 | ✅ 有 |
| 开源代码 | ❔ 未审 |
| 公开演化出的 Harness | ❔ 未审 |
| 谁来改 | ❔ 未审 |
| 反馈来源 | ❔ 未审 |
| 改进时机 | ❔ 未审 |
| 演化结构 | ❔ 未审 |

**一句话**：针对重复运行时时成时败的任务：结合 Agent 轨迹与运行时内部追踪，用 Harness Handbook 把行为映射到源码，并检索其他框架的实现作参考。

**关键结果**：Pass@1 与 Pass^4（四次全过的任务比例）都提高，Pass@4 只小幅上升，收益主要在可靠性；可迁移到未参与演化的基准。

<details><summary>English</summary>

| Evidence field | Record |
| --- | --- |
| Held-out evaluation | ✅ yes |
| Matched-budget baseline | ❔ not yet reviewed |
| Cross-model transfer | ❔ not yet reviewed |
| Cost reported | ❔ not yet reviewed |
| Disjoint evolution set | ❔ not yet reviewed |
| Reliability metric | ✅ yes |
| Code released | ❔ not yet reviewed |
| Evolved harness released | ❔ not yet reviewed |
| Who edits | ❔ not yet reviewed |
| Feedback | ❔ not yet reviewed |
| Timing | ❔ not yet reviewed |
| Topology | ❔ not yet reviewed |

**Summary**: Targets tasks with inconsistent success across repeated runs: combines agent trajectories and internal runtime traces, maps behavior to source code using a Harness Handbook, and retrieves implementations from other frameworks as references.

**Key result**: Both Pass@1 and Pass^4 (the fraction of tasks passing all four runs) improve, while Pass@4 rises only slightly; gains mainly concern reliability and transfer to benchmarks not used in evolution.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design](oo-harness.md)
- [HGM-Dual: Lineage-Aware Guided Agent Harness Optimization for Long-Horizon Planning](hgm-dual.md)
- [EMHO](emho.md)
- [ModularRSI: Modular and Generalizable Recursive Harness Self-Improvement](modularrsi.md)
- [AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces](autosaddler.md)

<!-- AUTO:RELATED:END -->
