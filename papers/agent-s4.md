# Evolving Agent Interfaces (Agent S4)

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2610.28601) · [HF](https://huggingface.co/papers/2610.28601) · [Code](https://github.com/simular-ai/Agent-S)

2026-10-20 · Simular · 三、组件级进化



| 证据字段 | 记录 |
| --- | --- |
| 留出集 | ✅ 有 |
| 同预算对照 | ❔ 未审 |
| 跨模型迁移 | ❔ 未审 |
| 报告成本 | ✅ 有 |
| 不相交演化集 | ❔ 未审 |
| 可靠性指标 | ❔ 未审 |
| 开源代码 | ✅ 有 |
| 公开演化出的 Harness | ❔ 未审 |
| 谁来改 | ❔ 未审 |
| 反馈来源 |  代理信号 |
| 改进时机 | ❔ 未审 |
| 演化结构 | ❔ 未审 |

**一句话**：元 Agent 阅读合成任务上的无成功标签轨迹，写入并修订接口仓库；种群选择按元 Agent 看不到的验证任务决定保留哪些仓库。

**关键结果**：OSWorld V2 上 Qwen3.8-27B 达 21.3%，是固定接口的 3.8 倍，高于 Opus 4.8（20.6%）与 GPT-5.5（13.0%）；ScienceBoard 41.4%→58.6%。

<details><summary>English</summary>

| Evidence field | Record |
| --- | --- |
| Held-out evaluation | ✅ yes |
| Matched-budget baseline | ❔ not yet reviewed |
| Cross-model transfer | ❔ not yet reviewed |
| Cost reported | ✅ yes |
| Disjoint evolution set | ❔ not yet reviewed |
| Reliability metric | ❔ not yet reviewed |
| Code released | ✅ yes |
| Evolved harness released | ❔ not yet reviewed |
| Who edits | ❔ not yet reviewed |
| Feedback |  proxy |
| Timing | ❔ not yet reviewed |
| Topology | ❔ not yet reviewed |

**Summary**: A meta agent reads trajectories without success labels on synthetic tasks, writing and revising interface repositories; population selection retains repositories using validation tasks hidden from the meta agent.

**Key result**: On OSWorld V2, Qwen3.8-27B reaches 21.3%, 3.8 times the fixed-interface result, above Opus 4.8 (20.6%) and GPT-5.5 (13.0%); ScienceBoard 41.4%→58.6%.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [Beyond Skill Evolution: Self-Evolving Context Management Policies for Long-Horizon Agent Harnesses (ContextEvo)](contextevo.md)
- [PILOT in the Loop: Live Self-Improvement for Long-Horizon Agents](pilot.md)
- [Living-Harness Is an Interactive-Agent Evolver](living-harness.md)
- [SkillOpt-Lite: Better and Faster Agent Self-evolution via One Line of Vibe](skillopt-lite.md)
- [TTHE: Test-Time Harness Evolution](tthe.md)
- [Harness²: Recursive Agent Harnessing for an Open World](harness2.md)
- [HarnessPro: Recursive Harness Self-Improvement with Pareto Optimization for Performance-Cost Trade-offs](harnesspro.md)

<!-- AUTO:RELATED:END -->
