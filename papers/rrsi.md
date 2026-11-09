# RRSI: Regularized Recursive Harness Self-Improvement

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2609.24972) · [HF](https://huggingface.co/papers/2609.24972)

2026-09 · Google · 1.2 泛化、正则、准入与成本

**必读 / MUST READ**

| 证据字段 | 记录 |
| --- | --- |
| 留出集 | ✅ 有 |
| 同预算对照 | ❔ 未审 |
| 跨模型迁移 | ❔ 未审 |
| 报告成本 | ✅ 有 |
| 不相交演化集 | ❔ 未审 |
| 可靠性指标 | ❔ 未审 |
| 开源代码 | ❔ 未审 |
| 公开演化出的 Harness | ❔ 未审 |
| 谁来改 | ❔ 未审 |
| 反馈来源 | ❔ 未审 |
| 改进时机 | ❔ 未审 |
| 演化结构 | ❔ 未审 |

**一句话**：退火编辑预算 + critic 筛掉 benchmark 特化提案 + pruner 删掉无效改动。

**关键结果**：五个分布外基准上迁移优于 Meta-Harness、AHE、TTHE、HarnessX，最高 +4.7；单任务 token 2.42M（无正则演化为 3.80M）。

<details><summary>English</summary>

| Evidence field | Record |
| --- | --- |
| Held-out evaluation | ✅ yes |
| Matched-budget baseline | ❔ not yet reviewed |
| Cross-model transfer | ❔ not yet reviewed |
| Cost reported | ✅ yes |
| Disjoint evolution set | ❔ not yet reviewed |
| Reliability metric | ❔ not yet reviewed |
| Code released | ❔ not yet reviewed |
| Evolved harness released | ❔ not yet reviewed |
| Who edits | ❔ not yet reviewed |
| Feedback | ❔ not yet reviewed |
| Timing | ❔ not yet reviewed |
| Topology | ❔ not yet reviewed |

**Summary**: Anneals the editing budget, uses a critic to filter benchmark-specific proposals, and a pruner to remove ineffective edits.

**Key result**: Transfers better than Meta-Harness, AHE, TTHE, and HarnessX on five out-of-distribution benchmarks, by up to +4.7; per-task token use is 2.42M (3.80M for unregularized evolution).

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [Bad Genius: Counterfactual-Guided Harness Evolution Beyond Task-Specific Shortcuts (CHASE)](chase.md)
- [HarnessEvolve: Learning from Reference Trajectories for Reliable Agent Self-Evolution](harnessevolve.md)
- [SoL-Pi: Recursively Scaling Auto-Research Loops for Efficient Agent Harness](sol-pi.md)
- [HarnessCompass: Guiding Automatic Harness Evolution toward Generalizable and Effective Agent Harnesses](harnesscompass.md)
- [AHE: Agentic Harness Engineering](ahe.md)
- [Self-Harness: Harnesses That Improve Themselves](self-harness.md)
- [DarwinX: Evolving Agent Harnesses Through Natural Selection](darwinx.md)
- [ModularRSI: Modular and Generalizable Recursive Harness Self-Improvement](modularrsi.md)

<!-- AUTO:RELATED:END -->
