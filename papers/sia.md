# SIA: Self Improving AI with Harness & Weight Updates

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2605.27276) · [HF](https://huggingface.co/papers/2605.27276)

2026-05 · Hexo Labs · Oxford · 四、模型与 Harness 协同进化



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

**一句话**：Feedback-Agent 读完整轨迹，在「改 Harness」和「更新权重」之间选择。局限：选择策略是静态的，两个优化器共用同一验证器，有 Goodhart 风险。

**关键结果**：LawBench 仅改 Harness 50%，加权重更新达 70.1%；CUDA kernel 加速 14.02 倍。

<details><summary>English · machine translation</summary>



**Summary**: A Feedback-Agent reads full trajectories and chooses between modifying the harness and updating weights. Limitations: the selection policy is static, and both optimizers share the same verifier, creating a Goodhart risk.

**Key result**: On LawBench, harness-only changes reach 50%, rising to 70.1% with weight updates; CUDA kernels speed up by 14.02 times.

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
