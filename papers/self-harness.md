# Self-Harness: Harnesses That Improve Themselves

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2606.09498) · [HF](https://huggingface.co/papers/2606.09498)

2026-06 · Shanghai AI Lab · 1.1 搜索与演化主线

**必读 / MUST READ**

| 证据字段 | 记录 |
| --- | --- |
| 留出集 | ✅ 有 |
| 同预算对照 | ❔ 未审 |
| 跨模型迁移 | ◐ 部分 |
| 报告成本 | ❔ 未审 |
| 不相交演化集 | ❔ 未审 |
| 可靠性指标 | ❔ 未审 |
| 开源代码 | ❔ 未审 |
| 公开演化出的 Harness | ❔ 未审 |
| 谁来改 |  自身 |
| 反馈来源 | ❔ 未审 |
| 改进时机 | ❔ 未审 |
| 演化结构 | ❔ 未审 |

**一句话**：弱点挖掘 → 最小化修改提案 → 回归测试后才接受；不依赖更强的外部模型。

**关键结果**：TB2.0 留出集：MiniMax M2.5 40.5%→61.9%，Qwen3.5-35B-A3B 23.8%→38.1%，GLM-5 42.9%→57.1%。

<details><summary>English</summary>

| Evidence field | Record |
| --- | --- |
| Held-out evaluation | ✅ yes |
| Matched-budget baseline | ❔ not yet reviewed |
| Cross-model transfer | ◐ partial |
| Cost reported | ❔ not yet reviewed |
| Disjoint evolution set | ❔ not yet reviewed |
| Reliability metric | ❔ not yet reviewed |
| Code released | ❔ not yet reviewed |
| Evolved harness released | ❔ not yet reviewed |
| Who edits |  self |
| Feedback | ❔ not yet reviewed |
| Timing | ❔ not yet reviewed |
| Topology | ❔ not yet reviewed |

**Summary**: Mine weaknesses → propose minimal edits → accept only after regression tests; does not rely on a stronger external model.

**Key result**: TB2.0 held-out set: MiniMax M2.5 40.5%→61.9%, Qwen3.5-35B-A3B 23.8%→38.1%, GLM-5 42.9%→57.1%.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [DemoEvolve](demoevolve.md)
- [TTHE: Test-Time Harness Evolution](tthe.md)
- [HarnessBank: Semantic Gene-Bank Search with Gated Verification for Agent-Harness Self-Evolution](harnessbank.md)
- [RHI: Recursive Harness Self-Improvement](rhi.md)
- [AHE: Agentic Harness Engineering](ahe.md)
- [DarwinX: Evolving Agent Harnesses Through Natural Selection](darwinx.md)
- [ModularRSI: Modular and Generalizable Recursive Harness Self-Improvement](modularrsi.md)
- [RRSI: Regularized Recursive Harness Self-Improvement](rrsi.md)

<!-- AUTO:RELATED:END -->
