# HarnessX: A Composable, Adaptive, and Evolvable Agent Harness Foundry

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2606.14249) · [HF](https://huggingface.co/papers/2606.14249) · [Code](https://github.com/Darwin-Agent/HarnessX)

2026-06 · Xiaomi (Darwin Agent Team) · 四、模型与 Harness 协同进化

**必读 / MUST READ**

| 证据字段 | 记录 |
| --- | --- |
| 留出集 | ❔ 未审 |
| 同预算对照 | ❔ 未审 |
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

**一句话**：类型化 Harness 原语 + 替换代数；AEGIS 把轨迹转成 Harness 更新；同一任务在不同 Harness 版本下的轨迹合并做 GRPO。

**关键结果**：15 个模型—基准配置中 14 个提升，平均 +14.5%（最高 +44.0%）；交替加入权重更新后峰值再 +4.7%。SWE-bench Verified 上 GPT-5.4 在第 3 轮达峰后回落。

<details><summary>English</summary>

| Evidence field | Record |
| --- | --- |
| Held-out evaluation | ❔ not yet reviewed |
| Matched-budget baseline | ❔ not yet reviewed |
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

**Summary**: Typed harness primitives plus a replacement algebra; AEGIS converts trajectories into harness updates; trajectories for the same task under different harness versions are pooled for GRPO.

**Key result**: Improves in 14 of 15 model–benchmark configurations, averaging +14.5% (up to +44.0%); alternating weight updates adds another +4.7% at peak. On SWE-bench Verified, GPT-5.4 peaks in round 3 and then declines.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [HarnessForge: Joint Harness and Policy Evolution for Adaptive Agent Systems](harnessforge.md)
- [Co-Harness: Co-Evolving Harnesses and Model Weights for LLM Agents](co-harness.md)
- [SIA: Self Improving AI with Harness & Weight Updates](sia.md)
- [EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents](evoharness-rl.md)
- [Co-Evolving Harnesses and Models](co-evolving-harnesses-models.md)
- [Self-Evolving Coding Agents via Harness-Policy Optimization (Self-HPO)](self-hpo.md)
- [Training the Whole Agent, Not Just the Model (HarnessAdapt-RL)](harnessadapt-rl.md)

<!-- AUTO:RELATED:END -->
