# Evolving Agent Interfaces (Agent S4)

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2610.28601) · [HF](https://huggingface.co/papers/2610.28601) · [Code](https://github.com/simular-ai/Agent-S)

2026-10-20 · Simular · 三、组件级进化



| 证据字段 / Evidence field | 值 / Value |
| --- | --- |
| `held_out` | yes |
| `matched_budget_baseline` | unknown |
| `cross_model_transfer` | unknown |
| `cost_reported` | yes |
| `disjoint_evolution_set` | unknown |
| `reliability_metric` | unknown |
| `code_released` | yes |
| `evolved_harness_released` | unknown |
| `who_edits` | unknown |
| `feedback` | proxy |
| `timing` | unknown |
| `topology` | unknown |

**一句话**：元 Agent 阅读合成任务上的无成功标签轨迹，写入并修订接口仓库；种群选择按元 Agent 看不到的验证任务决定保留哪些仓库。

**关键结果**：OSWorld V2 上 Qwen3.8-27B 达 21.3%，是固定接口的 3.8 倍，高于 Opus 4.8（20.6%）与 GPT-5.5（13.0%）；ScienceBoard 41.4%→58.6%。

<details><summary>English · machine translation</summary>



**Summary**: A meta agent reads trajectories without success labels on synthetic tasks, writing and revising interface repositories; population selection retains repositories using validation tasks hidden from the meta agent.

**Key result**: On OSWorld V2, Qwen3.8-27B reaches 21.3%, 3.8 times the fixed-interface result, above Opus 4.8 (20.6%) and GPT-5.5 (13.0%); ScienceBoard 41.4%→58.6%.

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
