# RHI: Recursive Harness Self-Improvement

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2607.15524) · [HF](https://huggingface.co/papers/2607.15524)

2026-07-17 · Sakana AI · UC Berkeley · 1.1 搜索与演化主线



| 证据字段 | 记录 |
| --- | --- |
| 留出集 | ❔ 未审 |
| 同预算对照 | ❔ 未审 |
| 跨模型迁移 | ❔ 未审 |
| 报告成本 | ✅ 有 |
| 不相交演化集 | ❔ 未审 |
| 可靠性指标 | ❔ 未审 |
| 开源代码 | ❔ 未审 |
| 公开演化出的 Harness | ❔ 未审 |
| 谁来改 |  外部改进器 |
| 反馈来源 | ❔ 未审 |
| 改进时机 | ❔ 未审 |
| 演化结构 | ❔ 未审 |

**一句话**：Harness 写成提示级规范，用自身修订历史上的成对反馈迭代；收益主要来自上下文管理与 Agent 间信息流。被递归修改的是任务 Harness，不是改进器。

**关键结果**：30 个合成 ML 研究任务上，低推理强度 Agent 超过最高推理强度设置，成本最多降 60%。

<details><summary>English</summary>

| Evidence field | Record |
| --- | --- |
| Held-out evaluation | ❔ not yet reviewed |
| Matched-budget baseline | ❔ not yet reviewed |
| Cross-model transfer | ❔ not yet reviewed |
| Cost reported | ✅ yes |
| Disjoint evolution set | ❔ not yet reviewed |
| Reliability metric | ❔ not yet reviewed |
| Code released | ❔ not yet reviewed |
| Evolved harness released | ❔ not yet reviewed |
| Who edits |  external |
| Feedback | ❔ not yet reviewed |
| Timing | ❔ not yet reviewed |
| Topology | ❔ not yet reviewed |

**Summary**: Expresses the harness as a prompt-level specification and iterates using paired feedback from its own revision history; gains mainly come from context management and information flow between agents. The task harness is recursively modified, not the improver.

**Key result**: On 30 synthetic ML research tasks, a low-reasoning-effort agent exceeds the highest-reasoning-effort setting, reducing cost by up to 60%.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [HarnessBank: Semantic Gene-Bank Search with Gated Verification for Agent-Harness Self-Evolution](harnessbank.md)
- [TTHE: Test-Time Harness Evolution](tthe.md)
- [DREvo: Distilling Recalibrated Historical Experience for Harness Self-Evolution](drevo.md)
- [DarwinX: Evolving Agent Harnesses Through Natural Selection](darwinx.md)

<!-- AUTO:RELATED:END -->
