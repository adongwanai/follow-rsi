# ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2610.00906) · [HF](https://huggingface.co/papers/2610.00906)

2026-10-01 · Microsoft · 1.3 任务与证据选择



| 证据字段 | 记录 |
| --- | --- |
| 留出集 | ❔ 未审 |
| 同预算对照 | ✅ 有 |
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

**一句话**：把反复出现的失败抽象成动态增加的失败模式，用非平稳多臂赌博机在已知弱点与新场景间分配任务，课程随 Harness 一起变。

**关键结果**：同一优化器下，相比事先固定任务顺序，GAIA2 与 TB2.0 测试 Pass@1 分别 +4.4、+7.5pp。

<details><summary>English</summary>

| Evidence field | Record |
| --- | --- |
| Held-out evaluation | ❔ not yet reviewed |
| Matched-budget baseline | ✅ yes |
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

**Summary**: Abstracts recurring failures into a dynamically growing set of failure patterns and uses a nonstationary multi-armed bandit to allocate tasks between known weaknesses and new scenarios; the curriculum changes with the harness.

**Key result**: With the same optimizer, test Pass@1 on GAIA2 and TB2.0 improves by +4.4 and +7.5pp respectively over a task order fixed in advance.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [Forging More Tasks into Better Harnesses: Agentic Harness Evolution via Successive Scale Racing (SSR)](ssr.md)
- [ECDYSIS: Efficient and Effective Training of Runtime Harnesses for LLM Agents](ecdysis.md)
- [Task-CoEvolve: Efficient Harness Optimization via Adaptive Validation Task Selection](task-coevolve.md)

<!-- AUTO:RELATED:END -->
