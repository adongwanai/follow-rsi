# Rethinking the Evaluation of Harness Evolution for Agents

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2607.12227) · [HF](https://huggingface.co/papers/2607.12227) · [Code](https://github.com/rethinking-harness-evolution)

2026-07-14 · AI2 · UW · 五、评测、归因与可信度

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

**一句话**：同等反馈与推理预算下，TB2.1 上 Harness 演化未胜过并行采样和顺序修正；留出任务上 Opus 4.6 只 +1.2、GPT-5.4 不变。但在反馈更细、动态更多的长程游戏上优势明显。

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

**Summary**: With equal feedback and inference budgets, harness evolution on TB2.1 does not beat parallel sampling or sequential revision; on held-out tasks, Opus 4.6 gains only +1.2 and GPT-5.4 is unchanged. However, it has a clear advantage in long-horizon games with finer feedback and more dynamics.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [AutoHarnessBench](autoharnessbench.md)
- [Self-Authored Verification Is Unreliable](self-authored-verification.md)
- [Evo-Bench: Can Language Models Improve Agent Harness?](evo-bench.md)
- [HarnessOpt-Bench: Evaluating LLMs at Harness Optimization](harnessopt-bench.md)
- [Harness-Delta Attribution: Dissecting Gains From Harness Evolution](hda.md)
- [HarnessDev: Can LLMs Create and Evolve Their Own Agent Harness?](harnessdev.md)
- [RSIHub: A Composable Framework for Agent-Evolution Methods](rsihub.md)
- [Auditing the Product, Not the Recursion](auditing-product.md)
- [Reflections on Trusting Trust, Revisited](trusting-trust-revisited.md)

<!-- AUTO:RELATED:END -->
