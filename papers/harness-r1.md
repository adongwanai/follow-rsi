# Harness-R1

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2608.02276) · [HF](https://huggingface.co/papers/2608.02276)

2026-08 · SJTU · Xiaohongshu · 二、改进器自身进化



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

**一句话**：把「根据失败轨迹编辑可执行 Harness」当作策略，冷启动 SFT 后用 GRPO 在线训练。

**关键结果**：WebShop、ALFWorld、DBBench 上把 Qwen3.5-9B 从 44.3% 提到 53.6%。

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

**Summary**: Treats editing an executable harness from failure trajectories as a policy, using online GRPO training after cold-start SFT.

**Key result**: Raises Qwen3.5-9B from 44.3% to 53.6% on WebShop, ALFWorld, and DBBench.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [Meta^n](meta-n.md)
- [Hierarchical Self-Improvement: A Framework for Task-Specific Evolvable Agent Harnesses](hsi.md)
- [Harness Learning Enables Generalizable Test-Time Adaptation](harness-learning-tta.md)
- [MetaRSI / RSI²](metarsi.md)

<!-- AUTO:RELATED:END -->
