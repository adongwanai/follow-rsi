# Self-Evolving Coding Agents via Harness-Policy Optimization (Self-HPO)

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2610.22791) · [HF](https://huggingface.co/papers/2610.22791) · [Code](https://github.com/MSR-Orchard/Self-HPO)

2026-10-16 · Microsoft Research · UVA · CMU · 四、模型与 Harness 协同进化



| 证据字段 / Evidence field | 值 / Value |
| --- | --- |
| `held_out` | unknown |
| `matched_budget_baseline` | unknown |
| `cross_model_transfer` | unknown |
| `cost_reported` | unknown |
| `disjoint_evolution_set` | unknown |
| `reliability_metric` | unknown |
| `code_released` | yes |
| `evolved_harness_released` | yes |
| `who_edits` | self |
| `feedback` | unknown |
| `timing` | unknown |
| `topology` | unknown |

**一句话**：H-step 由当前策略分析自身失败并提出 Harness 候选；P-step 在选定 Harness 下做 RL；仍未解决的任务成为下一轮搜索集。

**关键结果**：Qwen3.5-35B-A3B 在三个 SWE-bench 上平均 57.8%→64.8%，优于只改一边；用 Opus 4.8 当外部提议器的 HPO 达 66.3%，自我提议还没追上强外部提议器。

<details><summary>English · machine translation</summary>



**Summary**: In the H-step, the current policy analyzes its own failures and proposes harness candidates; in the P-step, it performs RL under the selected harness; still-unsolved tasks become the next round’s search set.

**Key result**: Qwen3.5-35B-A3B averages 57.8%→64.8% across three SWE-bench benchmarks, outperforming changes to only one side; HPO with Opus 4.8 as an external proposer reaches 66.3%, so self-proposal has not caught up with a strong external proposer.

</details>

<!-- AUTO:CARD:END -->

## 精读笔记

<!-- TODO -->

## 视频

<!-- TODO -->

## 可延伸的 idea

<!-- TODO -->

## 相关论文

<!-- TODO -->
