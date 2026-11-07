# HarnessCompass: Guiding Automatic Harness Evolution toward Generalizable and Effective Agent Harnesses

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2608.01918) · [HF](https://huggingface.co/papers/2608.01918)

2026-08-03 ·  · 1.2 泛化、正则、准入与成本



| 证据字段 | 记录 |
| --- | --- |
| 留出集 | ❔ 未审 |
| 同预算对照 | ❔ 未审 |
| 跨模型迁移 | ✅ 有 |
| 报告成本 | ❔ 未审 |
| 不相交演化集 | ❔ 未审 |
| 可靠性指标 | ❔ 未审 |
| 开源代码 | ❔ 未审 |
| 公开演化出的 Harness | ❔ 未审 |
| 谁来改 | ❔ 未审 |
| 反馈来源 | ❔ 未审 |
| 改进时机 | ❔ 未审 |
| 演化结构 | ❔ 未审 |

**一句话**：三条原则：泛化门控限制任务特化修改；第一人称「主动反馈」补充轨迹证据；组件分轨优化再整合，减少相互干扰。

**关键结果**：报告 SWE-bench Verified 五轮提升并检验跨任务、跨模型迁移；但 CHASE 在 OfficeQA 上发现其门控不保证留出提升。

<details><summary>English</summary>

| Evidence field | Record |
| --- | --- |
| Held-out evaluation | ❔ not yet reviewed |
| Matched-budget baseline | ❔ not yet reviewed |
| Cross-model transfer | ✅ yes |
| Cost reported | ❔ not yet reviewed |
| Disjoint evolution set | ❔ not yet reviewed |
| Reliability metric | ❔ not yet reviewed |
| Code released | ❔ not yet reviewed |
| Evolved harness released | ❔ not yet reviewed |
| Who edits | ❔ not yet reviewed |
| Feedback | ❔ not yet reviewed |
| Timing | ❔ not yet reviewed |
| Topology | ❔ not yet reviewed |

**Summary**: Three principles: generalization gates restrict task-specific edits; first-person “active feedback” supplements trajectory evidence; components are optimized on separate tracks and then integrated to reduce interference.

**Key result**: Reports improvement over five rounds on SWE-bench Verified and tests cross-task and cross-model transfer; however, CHASE finds on OfficeQA that its gates do not guarantee held-out gains.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [Bad Genius: Counterfactual-Guided Harness Evolution Beyond Task-Specific Shortcuts (CHASE)](chase.md)
- [HarnessEvolve: Learning from Reference Trajectories for Reliable Agent Self-Evolution](harnessevolve.md)
- [RRSI: Regularized Recursive Harness Self-Improvement](rrsi.md)
- [SoL-Pi: Recursively Scaling Auto-Research Loops for Efficient Agent Harness](sol-pi.md)
- [StarHarness: Evolving Harnesses with Stratified Search for Enterprise Environments](starharness.md)
- [MaD-RSI: Model-as-Data for Recursive Self-Improvement of Agent Harnesses](mad-rsi.md)
- [Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design](oo-harness.md)

<!-- AUTO:RELATED:END -->
