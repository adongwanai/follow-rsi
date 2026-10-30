# Can LLMs Improve Their Own Harness? A Controlled Study on ARC-AGI-3

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2610.30499) · [HF](https://huggingface.co/papers/2610.30499)

2026-10-21 ·  · 五、评测、归因与可信度



| 证据字段 | 记录 |
| --- | --- |
| 留出集 | ✅ 有 |
| 同预算对照 | ❔ 未审 |
| 跨模型迁移 | ❔ 未审 |
| 报告成本 | ❔ 未审 |
| 不相交演化集 | ❔ 未审 |
| 可靠性指标 | ❔ 未审 |
| 开源代码 | ❔ 未审 |
| 公开演化出的 Harness | ❔ 未审 |
| 谁来改 | ❔ 未审 |
| 反馈来源 | ❔ 未审 |
| 改进时机 | ❔ 未审 |
| 演化结构 | ❔ 未审 |

**一句话**：模型从最小仓库构建完整 Harness，在 5 个开发游戏上运行并修改两次，再在 20 个留出游戏上评估。27 条谱系中两次修改平均留出 RHAE 只 +2.80，95% 区间 [-1.44, 7.35]，开发集提升高估了泛化。

<details><summary>English</summary>

| Evidence field | Record |
| --- | --- |
| Held-out evaluation | ✅ yes |
| Matched-budget baseline | ❔ not yet reviewed |
| Cross-model transfer | ❔ not yet reviewed |
| Cost reported | ❔ not yet reviewed |
| Disjoint evolution set | ❔ not yet reviewed |
| Reliability metric | ❔ not yet reviewed |
| Code released | ❔ not yet reviewed |
| Evolved harness released | ❔ not yet reviewed |
| Who edits | ❔ not yet reviewed |
| Feedback | ❔ not yet reviewed |
| Timing | ❔ not yet reviewed |
| Topology | ❔ not yet reviewed |

**Summary**: The model builds a full harness from a minimal repository, runs it on 5 development games and modifies it twice, then evaluates it on 20 held-out games. Across 27 lineages, the two modifications yield only +2.80 mean held-out RHAE, with a 95% interval of [-1.44, 7.35]; development-set gains overestimate generalization.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [RSIHub: A Composable Framework for Agent-Evolution Methods](rsihub.md)
- [Harness-Delta Attribution: Dissecting Gains From Harness Evolution](hda.md)
- [Auditing the Product, Not the Recursion](auditing-product.md)
- [RSIGym](rsigym.md)

<!-- AUTO:RELATED:END -->
