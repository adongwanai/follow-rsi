# Aspire: Can Models Self-Evolve from Vague Goals?

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2608.31111) · [HF](https://huggingface.co/papers/2608.31111)

2026-08-31 · ByteDance Seed · Singapore University of Technology and Design · M-A-P · TokenWave.AI · 五、评测、归因与可信度



| 证据字段 | 记录 |
| --- | --- |
| 留出集 | ◐ 部分 |
| 同预算对照 | ❔ 未审 |
| 跨模型迁移 | ❔ 未审 |
| 报告成本 | ◐ 部分 |
| 不相交演化集 | ❔ 未审 |
| 可靠性指标 | ◐ 部分 |
| 开源代码 | ❔ 未审 |
| 公开演化出的 Harness | ❔ 未审 |
| 谁来改 | ❔ 未审 |
| 反馈来源 | ❔ 未审 |
| 改进时机 |  离线 |
| 演化结构 | ❔ 未审 |

**一句话**：通用 RSI 基准，主体评测模型从模糊目标选择数据并进行参数训练；另有一次 Harness 创建实验，尚未测试新 Harness 继续创建下一代。不计入 Harness 方法数。

**关键结果**：Final-only 的 12 个模型–目标组合各跑 2 次，只有 1 个组合的均值高于基座（+2.67）；adaptive-feedback 的 30 格只有 1 格保留提升（+2.24），该分数受同一评估集反馈选优影响。

<details><summary>English</summary>

| Evidence field | Record |
| --- | --- |
| Held-out evaluation | ◐ partial |
| Matched-budget baseline | ❔ not yet reviewed |
| Cross-model transfer | ❔ not yet reviewed |
| Cost reported | ◐ partial |
| Disjoint evolution set | ❔ not yet reviewed |
| Reliability metric | ◐ partial |
| Code released | ❔ not yet reviewed |
| Evolved harness released | ❔ not yet reviewed |
| Who edits | ❔ not yet reviewed |
| Feedback | ❔ not yet reviewed |
| Timing |  offline |
| Topology | ❔ not yet reviewed |

**Summary**: A general RSI benchmark centered on choosing data and training model parameters from vague goals. It also tests a single harness-creation step, without testing the created harness as the developer of another generation; excluded from harness method counts.

**Key result**: Each of 12 model–goal pairs has 2 final-only runs; only 1 pair has a mean above the base (+2.67). Among 30 adaptive-feedback cells, only 1 retains a gain (+2.24), selected using feedback from the same evaluation set.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:NOTES:START -->

## 精读笔记：Aspire

核对日期：2026-10-30。依据独立审查对官方 v1 的方法、主要结果及相关附录逐项核对；没有审核原始逐次实验日志。归为 general_rsi，不计入 Harness 方法数。

### 为什么不是整篇 Harness 自进化

主体让 Agent 从模糊目标选择或构造数据并运行参数训练，改变的是数据与权重。RQ3 另测创建下一代 Harness：从 H0 生成 H1 后交给冻结评估器，但没有让 H1 再创建 H2。不能因为存在 Harness 子实验，就把整篇收为新的 core Harness 演化方法；也不能否认 RQ3 确实生成了可运行 Harness。

### 训练与评测的统计单位

- RQ2 训练预算上限为每次 run 或每个 configuration–goal cell 的 40 GPU-hours，不是所有实验实际用满，也不包含推理、评判、部署或 controller 空闲时间。
- 520 个专家编写隐藏条目覆盖 6 个目标；各目标在自己的切片评估，不能说每条轨迹都跑全部 520 题。
- Final-only 为 12 个模型–目标对，每对 2 次独立终局运行，共 24 次。唯一正的组合均值为 Qwen3.5-9B 科学推理，45.33 → 48.00（+2.67）；单次看则 3/24 个终局超过 base。
- Adaptive-feedback 为 30 个配置–目标 cell，每格一条运行。只有 Terra / Qwen3.5-4B 数学的 17.86 → 20.10（+2.24）通过准入并保留。该值被同一评估切片的聚合反馈反复用于选优，缺少独立确认切片，不能当作独立复现的能力提升。

### 失败案例与 Harness 子实验

Qwen3.5-4B Self 的 32 次数据导入中，30 次使用 GSM8K 或 Hendrycks 数学数据，包括目标是科学、逻辑和写作的运行。数字标签 MMLU SFT 的 5 个检查点得分为 0、0、0、6.141、0：是 4 个零，不是 5 个零。长的 16–20 training-job 链没有中间隐藏评估，不能画成已观察到逐步下降的性能轨迹。

RQ3 固定 Qwen3.5-4B runtime。Sol 创建的 successor 的 task-macro 为 27.22，原 Qwen-Agent 为 28.64；example-micro 为 25.97 对 27.65。每个冻结 Harness 在同一 20 条目运行 3 次，但只有一条创建轨迹，且未报告执行离散度；不能当作 3 次独立递归进化或显著差异。

### 证据边界

- 留出集 partial：final-only 使用隐藏终局评价，但 adaptive 设置会暴露同一切片的聚合分数并据此选择。
- 成本 partial：报告训练 GPU-hours，但不是包含推理与评判的完整成本。
- 可靠性 partial：final-only 每对 2 次终局，adaptive 每格一次；RQ3 的 3 次执行不是 3 次独立创建。
- 匹配总预算基线、跨模型迁移、代码与最终产物等本次未确认项保持 unknown。
- 这篇与 S³Gym、HarnessDev 属于 Self-Developing Agents 同一项目；同系列不代表同一改进对象。

### 来源与日期

- [arXiv 元数据](https://arxiv.org/abs/2608.31111)：v1 首次提交 2026-08-31 17:14:59 UTC；PDF 封面为 2026-09-01。
- [§3.2](https://arxiv.org/html/2608.31111#S3.SS2)：520 条与按目标评分。
- [§4.3](https://arxiv.org/html/2608.31111#S4.SS3)：final-only、adaptive 和训练案例。
- [§4.4](https://arxiv.org/html/2608.31111#S4.SS4)：一次 Harness 创建及其局限。
- [附录 C.3](https://arxiv.org/html/2608.31111#A3.SS3)：数字标签检查点；[附录 C.6](https://arxiv.org/html/2608.31111#A3.SS6)：训练成本排除项。
- [官方系列项目](https://self-developing-agents.github.io/)。

机构（PDF 首页）：ByteDance Seed；Singapore University of Technology and Design；M-A-P；TokenWave.AI。

正文抓取时间：2026-10-30T03:08:24.694422+00:00。HTML SHA-256：b111da59c78d8e9ebe3806c3379f1f9387777c92f6acfded6e60c7f26811d858。

<!-- AUTO:NOTES:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [S3Gym: Can LLMs Turn Self-Testing and Self-Judging into Self-Improvement?](s3gym.md)
- [EvoHarnessBench](evoharnessbench.md)
- [HarnessDev: Can LLMs Create and Evolve Their Own Agent Harness?](harnessdev.md)
- [REUSE](reuse.md)

<!-- AUTO:RELATED:END -->
