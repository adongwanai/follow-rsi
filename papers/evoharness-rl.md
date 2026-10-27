# EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2608.05446) · [HF](https://huggingface.co/papers/2608.05446)

2026-08 · UIUC · Meta · 四、模型与 Harness 协同进化



**分类待复核**：建议主方向 model_weights；原摘要描述训练模型读写外部状态，需正文确认 Harness 是否独立演化。

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

**一句话**：不是改 Harness 代码，而是训练模型在运行时读写和整合 Belief、Progress、Experience 三类外部状态。

**关键结果**：ALFWorld 上 Qwen3-8B 从 47.9% 到 96.9%（未见任务 86.6%）；观察到「Harness 退火」，调用频率降到每回合约一次。

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

**Summary**: Trains the model to read, write, and integrate three types of external state at runtime, Belief, Progress, and Experience, rather than editing harness code.

**Key result**: On ALFWorld, Qwen3-8B rises from 47.9% to 96.9% (86.6% on unseen tasks); “harness annealing” is observed, with calls falling to about once per episode.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [HELIX](helix.md)
- [Co-Evolving Harnesses and Models](co-evolving-harnesses-models.md)
- [Co-Harness: Co-Evolving Harnesses and Model Weights for LLM Agents](co-harness.md)
- [SafeEvolve](safeevolve.md)

<!-- AUTO:RELATED:END -->
