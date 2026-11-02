# StarHarness: Evolving Harnesses with Stratified Search for Enterprise Environments

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2608.24804) · [HF](https://huggingface.co/papers/2608.24804) · [Code](https://github.com/ServiceNow/StarHarness)

2026-08-25 · ServiceNow · Mila · 1.1 搜索与演化主线



| 证据字段 | 记录 |
| --- | --- |
| 留出集 | ✅ 有 |
| 同预算对照 | ❔ 未审 |
| 跨模型迁移 | ✅ 有 |
| 报告成本 | ❔ 未审 |
| 不相交演化集 | ✅ 有 |
| 可靠性指标 | ❔ 未审 |
| 开源代码 | ✅ 有 |
| 公开演化出的 Harness | ❔ 未审 |
| 谁来改 |  外部改进器 |
| 反馈来源 | ❔ 未审 |
| 改进时机 | ❔ 未审 |
| 演化结构 | ❔ 未审 |

**一句话**：按基础 Harness 的失败行为分层构造演化池；提议器可见的搜索任务、不可见的选择任务、最终留出任务三者分开。

**关键结果**：ITBench SRE 等三个企业环境上，每个接受 4–12 次修改后全基准 +20–35pp；演化外任务上收益仍在，不重新演化即可迁移到 GPT 与 Qwen 系列。

<details><summary>English</summary>

| Evidence field | Record |
| --- | --- |
| Held-out evaluation | ✅ yes |
| Matched-budget baseline | ❔ not yet reviewed |
| Cross-model transfer | ✅ yes |
| Cost reported | ❔ not yet reviewed |
| Disjoint evolution set | ✅ yes |
| Reliability metric | ❔ not yet reviewed |
| Code released | ✅ yes |
| Evolved harness released | ❔ not yet reviewed |
| Who edits |  external |
| Feedback | ❔ not yet reviewed |
| Timing | ❔ not yet reviewed |
| Topology | ❔ not yet reviewed |

**Summary**: Builds a stratified evolution pool from the base harness’s failure behaviors; separates search tasks visible to the proposer, hidden selection tasks, and final held-out tasks.

**Key result**: Across three enterprise environments including ITBench SRE, each accepts 4–12 edits and gains +20–35pp across the full benchmark; gains persist on tasks outside evolution, and transfer to GPT and Qwen families requires no re-evolution.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces](autosaddler.md)
- [Ouroboros: A Self-Developing Coding Harness with Reviewed Core Evolution](ouroboros.md)
- [Mendel Gödel Machine: Recursive Self-Improving Coding Agents via Comparative Evolution](mgm.md)
- [ModularRSI: Modular and Generalizable Recursive Harness Self-Improvement](modularrsi.md)
- [HarnessCompass: Guiding Automatic Harness Evolution toward Generalizable and Effective Agent Harnesses](harnesscompass.md)
- [MaD-RSI: Model-as-Data for Recursive Self-Improvement of Agent Harnesses](mad-rsi.md)
- [Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design](oo-harness.md)

<!-- AUTO:RELATED:END -->
