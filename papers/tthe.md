# TTHE: Test-Time Harness Evolution

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2607.08124) · [HF](https://huggingface.co/papers/2607.08124)

2026-07-09 ·  · 1.1 搜索与演化主线



| 证据字段 / Evidence field | 值 / Value |
| --- | --- |
| `held_out` | unknown |
| `matched_budget_baseline` | unknown |
| `cross_model_transfer` | yes |
| `cost_reported` | unknown |
| `disjoint_evolution_set` | unknown |
| `reliability_metric` | unknown |
| `code_released` | unknown |
| `evolved_harness_released` | unknown |
| `who_edits` | self |
| `feedback` | proxy |
| `timing` | test_time |
| `topology` | unknown |

**一句话**：测试时只用无标签执行轨迹演化候选 Harness 种群；求解器、提议器、裁判共用一个冻结模型，各有不同 Harness。

**关键结果**：BIRD 执行准确率 12.7%→48.7%（十次投票基线 16.0%）；演化出的 Harness 可迁移到其他模型。

<details><summary>English · machine translation</summary>



**Summary**: Evolves a population of candidate harnesses at test time using only unlabeled execution trajectories; the solver, proposer, and judge share one frozen model, each with a different harness.

**Key result**: BIRD execution accuracy 12.7%→48.7% (ten-vote baseline 16.0%); the evolved harness transfers to other models.

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
