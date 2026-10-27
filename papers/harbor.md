# HARBOR

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2604.20938) · [HF](https://huggingface.co/papers/2604.20938)

2026-04 ·  · 1.2 泛化、正则、准入与成本



**分类待复核**：建议候选；固定配置空间的外部贝叶斯优化是否属于自改进，需细读正文。

| 证据字段 | 记录 |
| --- | --- |
| 留出集 | ❔ 未审 |
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

**一句话**：不改代码，而是在固定组件的 Harness 配置空间上做成本感知的贝叶斯优化。

**关键结果**：与 Meta-Harness 类「改代码」路线互补，可作为配置搜索基线。

<details><summary>English</summary>

| Evidence field | Record |
| --- | --- |
| Held-out evaluation | ❔ not yet reviewed |
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

**Summary**: Performs cost-aware Bayesian optimization over a harness configuration space with fixed components, without changing code.

**Key result**: Complements code-editing approaches such as Meta-Harness and can serve as a configuration-search baseline.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [HarnessCompass: Guiding Automatic Harness Evolution toward Generalizable and Effective Agent Harnesses](harnesscompass.md)
- [Bad Genius: Counterfactual-Guided Harness Evolution Beyond Task-Specific Shortcuts (CHASE)](chase.md)
- [HarnessEvolve: Learning from Reference Trajectories for Reliable Agent Self-Evolution](harnessevolve.md)
- [RRSI: Regularized Recursive Harness Self-Improvement](rrsi.md)

<!-- AUTO:RELATED:END -->
