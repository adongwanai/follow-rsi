# Co-Evolving Harnesses and Models

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2609.09134) · [HF](https://huggingface.co/papers/2609.09134)

2026-09 ·  · 四、模型与 Harness 协同进化

**必读 / MUST READ**

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

**一句话**：先用弱模型演化 Harness；发现让弱模型模仿强模型完整轨迹会破坏契合；改为只让专家重写弱模型自己轨迹中出错的那一轮。

**关键结果**：7 个企业任务上，全轨迹模仿导致 4–30 分退化；在策略纠正在不破坏 Harness 增益的前提下继续提升。

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

**Summary**: First evolves a harness using a weak model; finds that making the weak model imitate a strong model’s full trajectories breaks their fit; instead, the expert rewrites only the erroneous turn in the weak model’s own trajectory.

**Key result**: Across 7 enterprise tasks, full-trajectory imitation causes declines of 4–30 points; on-policy correction further improves performance without destroying harness gains.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [SafeEvolve](safeevolve.md)
- [MASS](mass.md)
- [EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents](evoharness-rl.md)
- [HELIX](helix.md)
- [HarnessX: A Composable, Adaptive, and Evolvable Agent Harness Foundry](harnessx.md)
- [Self-Evolving Coding Agents via Harness-Policy Optimization (Self-HPO)](self-hpo.md)
- [Training the Whole Agent, Not Just the Model (HarnessAdapt-RL)](harnessadapt-rl.md)

<!-- AUTO:RELATED:END -->
