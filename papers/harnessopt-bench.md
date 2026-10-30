# HarnessOpt-Bench: Evaluating LLMs at Harness Optimization

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2608.06301) · [HF](https://huggingface.co/papers/2608.06301)

2026-08-06 · Scale AI · 五、评测、归因与可信度



| 证据字段 | 记录 |
| --- | --- |
| 留出集 | ❔ 未审 |
| 同预算对照 | ❔ 未审 |
| 跨模型迁移 | ❔ 未审 |
| 报告成本 | ❔ 未审 |
| 不相交演化集 | ❔ 未审 |
| 可靠性指标 | ❔ 未审 |
| 开源代码 | ❔ 未审 |
| 公开演化出的 Harness | ❔ 未审 |
| 谁来改 | ❔ 未审 |
| 反馈来源 | ❔ 未审 |
| 改进时机 | ❔ 未审 |
| 演化结构 | ❔ 未审 |

**一句话**：优化器拿到种子 Harness 和固定评估预算，提交后在搜索期间不可见的测试集上计分。5 个前沿模型、111 次运行：优化器模型本身比它用的编码 Harness 更重要，原生 Harness 并不总是更好。

<details><summary>English</summary>

| Evidence field | Record |
| --- | --- |
| Held-out evaluation | ❔ not yet reviewed |
| Matched-budget baseline | ❔ not yet reviewed |
| Cross-model transfer | ❔ not yet reviewed |
| Cost reported | ❔ not yet reviewed |
| Disjoint evolution set | ❔ not yet reviewed |
| Reliability metric | ❔ not yet reviewed |
| Code released | ❔ not yet reviewed |
| Evolved harness released | ❔ not yet reviewed |
| Who edits | ❔ not yet reviewed |
| Feedback | ❔ not yet reviewed |
| Timing | ❔ not yet reviewed |
| Topology | ❔ not yet reviewed |

**Summary**: The optimizer receives a seed harness and a fixed evaluation budget; after submission it is scored on a test set hidden during search. Across 5 frontier models and 111 runs, the optimizer model itself matters more than its coding harness, and native harnesses are not always better.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [Evo-Bench: Can Language Models Improve Agent Harness?](evo-bench.md)
- [Rethinking the Evaluation of Harness Evolution for Agents](rethinking-evaluation.md)
- [Aspire: Can Models Self-Evolve from Vague Goals?](aspire.md)
- [S3Gym: Can LLMs Turn Self-Testing and Self-Judging into Self-Improvement?](s3gym.md)
- [Harness-Delta Attribution: Dissecting Gains From Harness Evolution](hda.md)
- [HarnessDev: Can LLMs Create and Evolve Their Own Agent Harness?](harnessdev.md)
- [RSIHub: A Composable Framework for Agent-Evolution Methods](rsihub.md)
- [Auditing the Product, Not the Recursion](auditing-product.md)
- [Reflections on Trusting Trust, Revisited](trusting-trust-revisited.md)

<!-- AUTO:RELATED:END -->
