# Training the Whole Agent, Not Just the Model (HarnessAdapt-RL)

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2610.28069) · [HF](https://huggingface.co/papers/2610.28069)

2026-10-20 ·  · 四、模型与 Harness 协同进化



| 证据字段 / Evidence field | 值 / Value |
| --- | --- |
| `held_out` | unknown |
| `matched_budget_baseline` | unknown |
| `cross_model_transfer` | unknown |
| `cost_reported` | unknown |
| `disjoint_evolution_set` | unknown |
| `reliability_metric` | unknown |
| `code_released` | unknown |
| `evolved_harness_released` | unknown |
| `who_edits` | unknown |
| `feedback` | unknown |
| `timing` | unknown |
| `topology` | unknown |

**一句话**：RL 期间，一个教师生成任务相关的机制级技能，另一个根据反复出现的交互问题演化工具和 hooks；只保留使通过率或可训练率提高且另一指标不降的修改。

**关键结果**：9B 模型在三个 SWE-bench 上平均 pass@1 比 GRPO 高 9.6pp；部署时去掉演化出的工具和 hooks 最多损失 7.7pp，交付物是模型与 Harness 的组合。

<details><summary>English · machine translation</summary>



**Summary**: During RL, one teacher generates task-related mechanism-level skills, while another evolves tools and hooks from recurring interaction problems; retains only edits that improve pass rate or trainability without lowering the other metric.

**Key result**: A 9B model averages 9.6pp higher pass@1 than GRPO across three SWE-bench benchmarks; removing evolved tools and hooks at deployment loses up to 7.7pp, so the deliverable is a model–harness combination.

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
