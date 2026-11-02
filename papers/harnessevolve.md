# HarnessEvolve: Learning from Reference Trajectories for Reliable Agent Self-Evolution

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2609.00829) · [HF](https://huggingface.co/papers/2609.00829)

2026-09 ·  · 1.2 泛化、正则、准入与成本



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

**一句话**：把「给定标准答案后重放」得到的参考轨迹与失败轨迹对齐做信用分配；质量门过滤答案硬编码与提示膨胀，性能门防遗忘。

**关键结果**：消融：去掉参考轨迹后 CloudCoreNetwork-QA 从 86.9 跌到 57.8。

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

**Summary**: Aligns reference trajectories obtained by replaying with standard answers against failed trajectories for credit assignment; a quality gate filters hardcoded answers and prompt bloat, while a performance gate prevents forgetting.

**Key result**: Ablation: removing reference trajectories drops CloudCoreNetwork-QA from 86.9 to 57.8.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [Bad Genius: Counterfactual-Guided Harness Evolution Beyond Task-Specific Shortcuts (CHASE)](chase.md)
- [RRSI: Regularized Recursive Harness Self-Improvement](rrsi.md)
- [SoL-Pi: Recursively Scaling Auto-Research Loops for Efficient Agent Harness](sol-pi.md)
- [HarnessCompass: Guiding Automatic Harness Evolution toward Generalizable and Effective Agent Harnesses](harnesscompass.md)

<!-- AUTO:RELATED:END -->
