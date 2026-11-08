# HERD: Harness-Evolving Recursive Distillation for Continual Learning

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2610.31401) · [HF](https://huggingface.co/papers/2610.31401)

2026-10-22 ·  · 四、模型与 Harness 协同进化

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
| 谁来改 | ❔ 未审 |
| 反馈来源 | ❔ 未审 |
| 改进时机 | ❔ 未审 |
| 演化结构 | ❔ 未审 |

**一句话**：Harness 侧持续修订技能，并在有界记忆里保留技能解释不了的高残差样例；参数侧用双锚点（上一检查点与基座）约束漂移，把经验吸收进权重。

**关键结果**：在 25 阶段的 TRACE+17 任务流上显著减少遗忘；定量结果待细读。

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

**Summary**: On the harness side, continually revises skills and retains high-residual examples unexplained by the skills in bounded memory; on the parameter side, two anchors, the previous checkpoint and the base model, constrain drift while absorbing experience into weights.

**Key result**: Significantly reduces forgetting on a 25-stage TRACE+17 task stream; quantitative results need close reading.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [Training the Whole Agent, Not Just the Model (HarnessAdapt-RL)](harnessadapt-rl.md)
- [CoEvo-RSI: When Harnesses Evolve, Which Models Should Follow?](coevo-rsi.md)
- [Self-Evolving Coding Agents via Harness-Policy Optimization (Self-HPO)](self-hpo.md)
- [MASS](mass.md)

<!-- AUTO:RELATED:END -->
