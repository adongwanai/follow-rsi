# Reflections on Trusting Trust, Revisited

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2609.17817) · [HF](https://huggingface.co/papers/2609.17817)

2026-09 ·  · 五、评测、归因与可信度



**分类待复核**：保留 Harness 专项评测，建议加 safety_governance 关联。

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

**一句话**：用投毒 benchmark 污染自修改编码 Agent；顺带发现 DGM 与 Hyperagents 的容器里可从 git 历史拿到答案，已被作者确认。复现这两个基线前必看。

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

**Summary**: Contaminates self-modifying coding agents using poisoned benchmarks; also discovers that answers can be obtained from git history inside DGM and Hyperagents containers, confirmed by their authors. Essential reading before reproducing these two baselines.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [EvoHarnessBench](evoharnessbench.md)
- [HarnessDev: Can LLMs Create and Evolve Their Own Agent Harness?](harnessdev.md)
- [REUSE](reuse.md)
- [Aspire: Can Models Self-Evolve from Vague Goals?](aspire.md)
- [Rethinking the Evaluation of Harness Evolution for Agents](rethinking-evaluation.md)
- [Harness-Delta Attribution: Dissecting Gains From Harness Evolution](hda.md)
- [RSIHub: A Composable Framework for Agent-Evolution Methods](rsihub.md)
- [HarnessOpt-Bench: Evaluating LLMs at Harness Optimization](harnessopt-bench.md)
- [Auditing the Product, Not the Recursion](auditing-product.md)

<!-- AUTO:RELATED:END -->
