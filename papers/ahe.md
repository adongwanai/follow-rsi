# AHE: Agentic Harness Engineering

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2604.25850) · [HF](https://huggingface.co/papers/2604.25850)

2026-04 · Fudan · 1.1 搜索与演化主线

**必读 / MUST READ**

| 证据字段 | 记录 |
| --- | --- |
| 留出集 | ❔ 未审 |
| 同预算对照 | ❔ 未审 |
| 跨模型迁移 | ✅ 有 |
| 报告成本 | ❔ 未审 |
| 不相交演化集 | ❔ 未审 |
| 可靠性指标 | ❔ 未审 |
| 开源代码 | ❔ 未审 |
| 公开演化出的 Harness | ❔ 未审 |
| 谁来改 |  外部改进器 |
| 反馈来源 | ❔ 未审 |
| 改进时机 | ❔ 未审 |
| 演化结构 | ❔ 未审 |

**一句话**：三个「可观测性」支柱：组件文件化、轨迹分层蒸馏、每次编辑附带可证伪的预测，下一轮核验。

**关键结果**：Terminal-Bench 2 pass@1 十轮从 69.7% 到 77.0%，超过 Codex-CLI；跨模型家族迁移 +5.1–10.1pp。

<details><summary>English</summary>

| Evidence field | Record |
| --- | --- |
| Held-out evaluation | ❔ not yet reviewed |
| Matched-budget baseline | ❔ not yet reviewed |
| Cross-model transfer | ✅ yes |
| Cost reported | ❔ not yet reviewed |
| Disjoint evolution set | ❔ not yet reviewed |
| Reliability metric | ❔ not yet reviewed |
| Code released | ❔ not yet reviewed |
| Evolved harness released | ❔ not yet reviewed |
| Who edits |  external |
| Feedback | ❔ not yet reviewed |
| Timing | ❔ not yet reviewed |
| Topology | ❔ not yet reviewed |

**Summary**: Three pillars of observability: components as files, hierarchical trajectory distillation, and a falsifiable prediction attached to each edit for verification in the next round.

**Key result**: Terminal-Bench 2 pass@1 rises from 69.7% to 77.0% over ten rounds, surpassing Codex-CLI; transfer across model families yields +5.1–10.1pp.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [DemoEvolve](demoevolve.md)
- [Self-Harness: Harnesses That Improve Themselves](self-harness.md)
- [TTHE: Test-Time Harness Evolution](tthe.md)
- [HarnessBank: Semantic Gene-Bank Search with Gated Verification for Agent-Harness Self-Evolution](harnessbank.md)
- [DarwinX: Evolving Agent Harnesses Through Natural Selection](darwinx.md)
- [ModularRSI: Modular and Generalizable Recursive Harness Self-Improvement](modularrsi.md)
- [RRSI: Regularized Recursive Harness Self-Improvement](rrsi.md)

<!-- AUTO:RELATED:END -->
