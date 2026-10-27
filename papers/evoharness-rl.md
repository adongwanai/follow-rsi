# EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2608.05446) · [HF](https://huggingface.co/papers/2608.05446)

2026-08 · UIUC · Meta · 四、模型与 Harness 协同进化



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

**一句话**：不是改 Harness 代码，而是训练模型在运行时读写和整合 Belief、Progress、Experience 三类外部状态。

**关键结果**：ALFWorld 上 Qwen3-8B 从 47.9% 到 96.9%（未见任务 86.6%）；观察到「Harness 退火」，调用频率降到每回合约一次。

<details><summary>English · machine translation</summary>



**Summary**: Trains the model to read, write, and integrate three types of external state at runtime, Belief, Progress, and Experience, rather than editing harness code.

**Key result**: On ALFWorld, Qwen3-8B rises from 47.9% to 96.9% (86.6% on unseen tasks); “harness annealing” is observed, with calls falling to about once per episode.

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
