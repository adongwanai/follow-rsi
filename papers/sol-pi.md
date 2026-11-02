# SoL-Pi: Recursively Scaling Auto-Research Loops for Efficient Agent Harness

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2609.20519) · [HF](https://huggingface.co/papers/2609.20519)

2026-09 · NVIDIA · MIT · 1.2 泛化、正则、准入与成本



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

**一句话**：在大量环境中扩展 auto-research 循环，筛选 token 效率机制；候选冻结后才做留出评估。

**关键结果**：EdgeBench 性能与 Pi 相当，token 流量降 44.7–49.0%，API 成本降约三分之一。

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

**Summary**: Scales the auto-research loop across many environments to select token-efficient mechanisms; held-out evaluation occurs only after candidates are frozen.

**Key result**: Matches Pi on EdgeBench, reducing token traffic by 44.7–49.0% and API cost by about one third.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [Bad Genius: Counterfactual-Guided Harness Evolution Beyond Task-Specific Shortcuts (CHASE)](chase.md)
- [HarnessEvolve: Learning from Reference Trajectories for Reliable Agent Self-Evolution](harnessevolve.md)
- [RRSI: Regularized Recursive Harness Self-Improvement](rrsi.md)
- [HarnessCompass: Guiding Automatic Harness Evolution toward Generalizable and Effective Agent Harnesses](harnesscompass.md)

<!-- AUTO:RELATED:END -->
