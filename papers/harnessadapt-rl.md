# Training the Whole Agent, Not Just the Model (HarnessAdapt-RL)

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2610.28069) · [HF](https://huggingface.co/papers/2610.28069)

2026-10-20 ·  · 四、模型与 Harness 协同进化



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

**一句话**：RL 期间，一个教师生成任务相关的机制级技能，另一个根据反复出现的交互问题演化工具和 hooks；只保留使通过率或可训练率提高且另一指标不降的修改。

**关键结果**：9B 模型在三个 SWE-bench 上平均 pass@1 比 GRPO 高 9.6pp；部署时去掉演化出的工具和 hooks 最多损失 7.7pp，交付物是模型与 Harness 的组合。

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

**Summary**: During RL, one teacher generates task-related mechanism-level skills, while another evolves tools and hooks from recurring interaction problems; retains only edits that improve pass rate or trainability without lowering the other metric.

**Key result**: A 9B model averages 9.6pp higher pass@1 than GRPO across three SWE-bench benchmarks; removing evolved tools and hooks at deployment loses up to 7.7pp, so the deliverable is a model–harness combination.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [CoEvo-RSI: When Harnesses Evolve, Which Models Should Follow?](coevo-rsi.md)
- [HERD: Harness-Evolving Recursive Distillation for Continual Learning](herd.md)
- [Self-Evolving Coding Agents via Harness-Policy Optimization (Self-HPO)](self-hpo.md)
- [MASS](mass.md)
- [HarnessX: A Composable, Adaptive, and Evolvable Agent Harness Foundry](harnessx.md)
- [Co-Evolving Harnesses and Models](co-evolving-harnesses-models.md)

<!-- AUTO:RELATED:END -->
