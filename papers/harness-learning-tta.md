# Harness Learning Enables Generalizable Test-Time Adaptation

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2609.35738) · [HF](https://huggingface.co/papers/2609.35738)

2026-09 ·  · 二、改进器自身进化

 **待细读 / Needs verification**

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
| 谁来改 |  训练出的改进器 |
| 反馈来源 | ❔ 未审 |
| 改进时机 | ❔ 未审 |
| 演化结构 | ❔ 未审 |

**一句话**：用修订后 Harness 的任务表现作奖励，强化学习训练 Harness 提案者。

**关键结果**：训练后的提案者在多轮测试时适配中持续改进，并能泛化到新的适配上下文；定量结果待细读。

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
| Who edits |  trained |
| Feedback | ❔ not yet reviewed |
| Timing | ❔ not yet reviewed |
| Topology | ❔ not yet reviewed |

**Summary**: Uses task performance under the revised harness as a reward to train a harness proposer with reinforcement learning.

**Key result**: The trained proposer keeps improving over multiple rounds of test-time adaptation and generalizes to new adaptation contexts; quantitative results need close reading.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [MetaRSI / RSI²](metarsi.md)
- [Mixture of Self-Improving Branches for Agent Harness Optimization](mixture-branches.md)
- [AIDE²: Recursive Self-Improvement of AI Research Agents](aide2.md)
- [Hierarchical Self-Improvement: A Framework for Task-Specific Evolvable Agent Harnesses](hsi.md)

<!-- AUTO:RELATED:END -->
