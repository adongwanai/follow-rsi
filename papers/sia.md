# SIA: Self Improving AI with Harness & Weight Updates

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2605.27276) · [HF](https://huggingface.co/papers/2605.27276)

2026-05 · Hexo Labs · Oxford · 四、模型与 Harness 协同进化



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

**一句话**：Feedback-Agent 读完整轨迹，在「改 Harness」和「更新权重」之间选择。局限：选择策略是静态的，两个优化器共用同一验证器，有 Goodhart 风险。

**关键结果**：LawBench 仅改 Harness 50%，加权重更新达 70.1%；CUDA kernel 加速 14.02 倍。

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

**Summary**: A Feedback-Agent reads full trajectories and chooses between modifying the harness and updating weights. Limitations: the selection policy is static, and both optimizers share the same verifier, creating a Goodhart risk.

**Key result**: On LawBench, harness-only changes reach 50%, rising to 70.1% with weight updates; CUDA kernels speed up by 14.02 times.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [HarnessForge: Joint Harness and Policy Evolution for Adaptive Agent Systems](harnessforge.md)
- [HarnessX: A Composable, Adaptive, and Evolvable Agent Harness Foundry](harnessx.md)
- [Co-Harness: Co-Evolving Harnesses and Model Weights for LLM Agents](co-harness.md)
- [EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents](evoharness-rl.md)

<!-- AUTO:RELATED:END -->
