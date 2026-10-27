# Harness-Delta Attribution: Dissecting Gains From Harness Evolution

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2610.22466) · [HF](https://huggingface.co/papers/2610.22466) · [Code](https://github.com/Wenwen-D/HarnessDeltaAttribution)

2026-10-15 ·  · 五、评测、归因与可信度

**必读 / MUST READ**

| 证据字段 | 记录 |
| --- | --- |
| 留出集 | ✅ 有 |
| 同预算对照 | ✅ 有 |
| 跨模型迁移 | ❔ 未审 |
| 报告成本 | ❔ 未审 |
| 不相交演化集 | ❔ 未审 |
| 可靠性指标 | ❔ 未审 |
| 开源代码 | ✅ 有 |
| 公开演化出的 Harness | ❔ 未审 |
| 谁来改 | ❔ 未审 |
| 反馈来源 | ❔ 未审 |
| 改进时机 | ❔ 未审 |
| 演化结构 | ❔ 未审 |

**一句话**：用「算力对齐基线」和「去捷径版演化 Harness」两个对照，把收益拆成过拟合、测试时扩展和剩余的可泛化上界。11 个执行模型、三个演化框架、21 个显著设置中，前两者平均占 54% 和 14%；验证集门控不足以防过拟合。

<details><summary>English</summary>

| Evidence field | Record |
| --- | --- |
| Held-out evaluation | ✅ yes |
| Matched-budget baseline | ✅ yes |
| Cross-model transfer | ❔ not yet reviewed |
| Cost reported | ❔ not yet reviewed |
| Disjoint evolution set | ❔ not yet reviewed |
| Reliability metric | ❔ not yet reviewed |
| Code released | ✅ yes |
| Evolved harness released | ❔ not yet reviewed |
| Who edits | ❔ not yet reviewed |
| Feedback | ❔ not yet reviewed |
| Timing | ❔ not yet reviewed |
| Topology | ❔ not yet reviewed |

**Summary**: Uses a compute-matched baseline and a shortcut-removed evolved harness as two controls to decompose gains into overfitting, test-time scaling, and a remaining upper bound on generalizable gains. Across 11 execution models, three evolution frameworks, and 21 significant settings, the first two account for 54% and 14% on average; validation-set gating is insufficient to prevent overfitting.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [Can LLMs Improve Their Own Harness? A Controlled Study on ARC-AGI-3](arc-agi-3-controlled.md)
- [Auditing the Product, Not the Recursion](auditing-product.md)
- [RSIGym](rsigym.md)
- [EvoHarnessBench](evoharnessbench.md)
- [Rethinking the Evaluation of Harness Evolution for Agents](rethinking-evaluation.md)
- [HarnessOpt-Bench: Evaluating LLMs at Harness Optimization](harnessopt-bench.md)
- [Reflections on Trusting Trust, Revisited](trusting-trust-revisited.md)

<!-- AUTO:RELATED:END -->
