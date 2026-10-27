# RRSI: Regularized Recursive Harness Self-Improvement

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2609.24972) · [HF](https://huggingface.co/papers/2609.24972)

2026-09 · Google · 1.2 泛化、正则、准入与成本

**必读 / MUST READ**

| 证据字段 / Evidence field | 值 / Value |
| --- | --- |
| `held_out` | yes |
| `matched_budget_baseline` | unknown |
| `cross_model_transfer` | unknown |
| `cost_reported` | yes |
| `disjoint_evolution_set` | unknown |
| `reliability_metric` | unknown |
| `code_released` | unknown |
| `evolved_harness_released` | unknown |
| `who_edits` | unknown |
| `feedback` | unknown |
| `timing` | unknown |
| `topology` | unknown |

**一句话**：退火编辑预算 + critic 筛掉 benchmark 特化提案 + pruner 删掉无效改动。

**关键结果**：五个分布外基准上迁移优于 Meta-Harness、AHE、TTHE、HarnessX，最高 +4.7；单任务 token 2.42M（无正则演化为 3.80M）。

<details><summary>English · machine translation</summary>



**Summary**: Anneals the editing budget, uses a critic to filter benchmark-specific proposals, and a pruner to remove ineffective edits.

**Key result**: Transfers better than Meta-Harness, AHE, TTHE, and HarnessX on five out-of-distribution benchmarks, by up to +4.7; per-task token use is 2.42M (3.80M for unregularized evolution).

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
