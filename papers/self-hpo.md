# Self-Evolving Coding Agents via Harness-Policy Optimization (Self-HPO)

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2610.22791) · [HF](https://huggingface.co/papers/2610.22791) · [Code](https://github.com/MSR-Orchard/Self-HPO)

2026-10-16 · Microsoft Research · UVA · CMU · 四、模型与 Harness 协同进化



| 证据字段 | 记录 |
| --- | --- |
| 留出集 | ❔ 未审 |
| 同预算对照 | ❔ 未审 |
| 跨模型迁移 | ❔ 未审 |
| 报告成本 | ❔ 未审 |
| 不相交演化集 | ❔ 未审 |
| 可靠性指标 | ❔ 未审 |
| 开源代码 | ✅ 有 |
| 公开演化出的 Harness | ✅ 有 |
| 谁来改 |  自身 |
| 反馈来源 | ❔ 未审 |
| 改进时机 | ❔ 未审 |
| 演化结构 | ❔ 未审 |

**一句话**：H-step 由当前策略分析自身失败并提出 Harness 候选；P-step 在选定 Harness 下做 RL；仍未解决的任务成为下一轮搜索集。

**关键结果**：Qwen3.5-35B-A3B 在三个 SWE-bench 上平均 57.8%→64.8%，优于只改一边；用 Opus 4.8 当外部提议器的 HPO 达 66.3%，自我提议还没追上强外部提议器。

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
| Evolved harness released | ✅ yes |
| Who edits |  self |
| Feedback | ❔ not yet reviewed |
| Timing | ❔ not yet reviewed |
| Topology | ❔ not yet reviewed |

**Summary**: In the H-step, the current policy analyzes its own failures and proposes harness candidates; in the P-step, it performs RL under the selected harness; still-unsolved tasks become the next round’s search set.

**Key result**: Qwen3.5-35B-A3B averages 57.8%→64.8% across three SWE-bench benchmarks, outperforming changes to only one side; HPO with Opus 4.8 as an external proposer reaches 66.3%, so self-proposal has not caught up with a strong external proposer.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [CoEvo-RSI: When Harnesses Evolve, Which Models Should Follow?](coevo-rsi.md)
- [Training the Whole Agent, Not Just the Model (HarnessAdapt-RL)](harnessadapt-rl.md)
- [HERD: Harness-Evolving Recursive Distillation for Continual Learning](herd.md)
- [MASS](mass.md)
- [HarnessX: A Composable, Adaptive, and Evolvable Agent Harness Foundry](harnessx.md)
- [Co-Evolving Harnesses and Models](co-evolving-harnesses-models.md)

<!-- AUTO:RELATED:END -->
