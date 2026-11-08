# TTHE: Test-Time Harness Evolution

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2607.08124) · [HF](https://huggingface.co/papers/2607.08124)

2026-07-09 ·  · 1.1 搜索与演化主线



| 证据字段 | 记录 |
| --- | --- |
| 留出集 | ❔ 未审 |
| 同预算对照 | ❔ 未审 |
| 跨模型迁移 | ✅ 有 |
| 报告成本 | ❔ 未审 |
| 不相交演化集 | ❔ 未审 |
| 可靠性指标 | ❔ 未审 |
| 开源代码 | ❔ 未审 |
| 公开演化出的 Harness | ❔ 未审 |
| 谁来改 |  自身 |
| 反馈来源 |  代理信号 |
| 改进时机 |  测试时 |
| 演化结构 | ❔ 未审 |

**一句话**：测试时只用无标签执行轨迹演化候选 Harness 种群；求解器、提议器、裁判共用一个冻结模型，各有不同 Harness。

**关键结果**：BIRD 执行准确率 12.7%→48.7%（十次投票基线 16.0%）；演化出的 Harness 可迁移到其他模型。

<details><summary>English</summary>

| Evidence field | Record |
| --- | --- |
| Held-out evaluation | ❔ not yet reviewed |
| Matched-budget baseline | ❔ not yet reviewed |
| Cross-model transfer | ✅ yes |
| Cost reported | ❔ not yet reviewed |
| Disjoint evolution set | ❔ not yet reviewed |
| Reliability metric | ❔ not yet reviewed |
| Code released | ❔ not yet reviewed |
| Evolved harness released | ❔ not yet reviewed |
| Who edits |  self |
| Feedback |  proxy |
| Timing |  test_time |
| Topology | ❔ not yet reviewed |

**Summary**: Evolves a population of candidate harnesses at test time using only unlabeled execution trajectories; the solver, proposer, and judge share one frozen model, each with a different harness.

**Key result**: BIRD execution accuracy 12.7%→48.7% (ten-vote baseline 16.0%); the evolved harness transfers to other models.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [HarnessBank: Semantic Gene-Bank Search with Gated Verification for Agent-Harness Self-Evolution](harnessbank.md)
- [RHI: Recursive Harness Self-Improvement](rhi.md)
- [DREvo: Distilling Recalibrated Historical Experience for Harness Self-Evolution](drevo.md)
- [DarwinX: Evolving Agent Harnesses Through Natural Selection](darwinx.md)
- [Harness²: Recursive Agent Harnessing for an Open World](harness2.md)
- [HarnessPro: Recursive Harness Self-Improvement with Pareto Optimization for Performance-Cost Trade-offs](harnesspro.md)
- [Evolving Agent Interfaces (Agent S4)](agent-s4.md)

<!-- AUTO:RELATED:END -->
