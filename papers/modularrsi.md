# ModularRSI: Modular and Generalizable Recursive Harness Self-Improvement

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2609.14857) · [HF](https://huggingface.co/papers/2609.14857)

2026-09-14 ·  · 1.1 搜索与演化主线

**必读 / MUST READ**

| 证据字段 | 记录 |
| --- | --- |
| 留出集 | ✅ 有 |
| 同预算对照 | ❔ 未审 |
| 跨模型迁移 | ✅ 有 |
| 报告成本 | ❔ 未审 |
| 不相交演化集 | ✅ 有 |
| 可靠性指标 | ❔ 未审 |
| 开源代码 | ❔ 未审 |
| 公开演化出的 Harness | ❔ 未审 |
| 谁来改 | ❔ 未审 |
| 反馈来源 | ❔ 未审 |
| 改进时机 | ❔ 未审 |
| 演化结构 | ❔ 未审 |

**一句话**：Harness 拆成执行循环、工具使用、观测管理、上下文管理、完成检测五模块，受限范围内独立演化再合并；成功与失败轨迹对比；2,000 个与评测不相交的演化任务。

**关键结果**：TB2.0 47.57→52.43，SWE-Bench Verified 73.40→76.45；跨模型迁移有效。

<details><summary>English</summary>

| Evidence field | Record |
| --- | --- |
| Held-out evaluation | ✅ yes |
| Matched-budget baseline | ❔ not yet reviewed |
| Cross-model transfer | ✅ yes |
| Cost reported | ❔ not yet reviewed |
| Disjoint evolution set | ✅ yes |
| Reliability metric | ❔ not yet reviewed |
| Code released | ❔ not yet reviewed |
| Evolved harness released | ❔ not yet reviewed |
| Who edits | ❔ not yet reviewed |
| Feedback | ❔ not yet reviewed |
| Timing | ❔ not yet reviewed |
| Topology | ❔ not yet reviewed |

**Summary**: Splits the harness into five modules: execution loop, tool use, observation management, context management, and completion detection; evolves each within a restricted scope, then merges them; contrasts successful and failed trajectories; uses 2,000 evolution tasks disjoint from evaluation.

**Key result**: TB2.0 47.57→52.43, SWE-Bench Verified 73.40→76.45; cross-model transfer is effective.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [EMHO](emho.md)
- [StarHarness: Evolving Harnesses with Stratified Search for Enterprise Environments](starharness.md)
- [AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces](autosaddler.md)
- [Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design](oo-harness.md)
- [AHE: Agentic Harness Engineering](ahe.md)
- [Self-Harness: Harnesses That Improve Themselves](self-harness.md)
- [DarwinX: Evolving Agent Harnesses Through Natural Selection](darwinx.md)
- [RRSI: Regularized Recursive Harness Self-Improvement](rrsi.md)
- [RiseHarness: Harness Self-Evolution for Long-Horizon Terminal Agents](riseharness.md)

<!-- AUTO:RELATED:END -->
