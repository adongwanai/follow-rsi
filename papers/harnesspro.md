# HarnessPro: Recursive Harness Self-Improvement with Pareto Optimization for Performance-Cost Trade-offs

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2610.26770) · [HF](https://huggingface.co/papers/2610.26770)

2026-10-19 ·  · 1.2 泛化、正则、准入与成本



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
| 反馈来源 |  自生成测试 |
| 改进时机 | ❔ 未审 |
| 演化结构 | ❔ 未审 |

**一句话**：无标签：用模型生成的测试评价候选，不访问标准答案或官方测试；按性能与成本的不同偏好产出 lite、medium、heavy 三档。

**关键结果**：GPT-5.5 + Codex 配置下，heavy 相对 RHO 平均通过率 +2.0pp，单任务成本降 26.1%。

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
| Feedback |  self_generated_tests |
| Timing | ❔ not yet reviewed |
| Topology | ❔ not yet reviewed |

**Summary**: Label-free: evaluates candidates with model-generated tests, without accessing standard answers or official tests; produces lite, medium, and heavy tiers for different performance–cost preferences.

**Key result**: With GPT-5.5 + Codex, heavy improves average pass rate by +2.0pp over RHO and reduces per-task cost by 26.1%.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [MaD-RSI: Model-as-Data for Recursive Self-Improvement of Agent Harnesses](mad-rsi.md)
- [Bad Genius: Counterfactual-Guided Harness Evolution Beyond Task-Specific Shortcuts (CHASE)](chase.md)
- [HarnessEvolve: Learning from Reference Trajectories for Reliable Agent Self-Evolution](harnessevolve.md)
- [RRSI: Regularized Recursive Harness Self-Improvement](rrsi.md)
- [TTHE: Test-Time Harness Evolution](tthe.md)
- [Harness²: Recursive Agent Harnessing for an Open World](harness2.md)
- [Evolving Agent Interfaces (Agent S4)](agent-s4.md)

<!-- AUTO:RELATED:END -->
