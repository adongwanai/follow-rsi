# Harness 演化论文证据自查清单

每个结论都应附正文页码或表号；尚未核实就保留 `unknown`。这是一份评测设计清单，不是对收录论文的新增判定。

- [ ] 演化集与评测集分开，评测集在搜索期间不可见 → `held_out`。为什么：避免搜索集收益被当作泛化收益；参见 [HDA](../../papers/hda.md)。
- [ ] 演化任务与下游评测基准不相交 → `disjoint_evolution_set`。为什么：任务复用可能放大评测收益；参见 [ModularRSI](../../papers/modularrsi.md)。
- [ ] 与同算力的测试时扩展（并行采样、顺序修正）做对比 → `matched_budget_baseline`。为什么：需要区分 Harness 改进与额外算力的作用；参见 [Rethinking](../../papers/rethinking-evaluation.md)。
- [ ] 不重新演化就迁移到其他模型家族 → `cross_model_transfer`。为什么：检查收益是否依赖特定执行模型；参见 [Meta-Harness](../../papers/meta-harness.md)。
- [ ] 报告 token 或美元成本，包括演化本身的成本 → `cost_reported`。为什么：只报告最终推理成本不能说明完整预算；参见 [HDA](../../papers/hda.md)。
- [ ] 多次重复运行，报告方差或 Pass^k → `reliability_metric`。为什么：一次成功不能说明重复执行的可靠性；参见 [RiseHarness](../../papers/riseharness.md)。
- [ ] 检查答案泄露：容器 git 历史、benchmark 答案文件、硬编码答案 → 当前 `evidence` 无独立字段，在 PR 中附审计记录。为什么：泄露会破坏评测有效性；参见 [Trusting Trust, Revisited](../../papers/trusting-trust-revisited.md)。
- [ ] 声称改进了「改进流程」时，在同起点、同预算下比较前后两代流程 → 当前 `evidence` 无独立字段，不等同于 `matched_budget_baseline`。为什么：需要把改进器变化与起点、预算变化分开；参见 [Auditing](../../papers/auditing-product.md)。
- [ ] 公开代码 → `code_released`；公开演化出的 Harness → `evolved_harness_released`。为什么：优化器代码和最终执行产物共同支撑复现；参见 [HarnessOpt-Bench](../../papers/harnessopt-bench.md)。
- [ ] 报告失败的设置和收益回落的轮次 → 当前 `evidence` 无独立字段，在 PR 中说明。为什么：失败边界帮助确定方法适用范围；参见 [HSI](../../papers/hsi.md) 与 [HarnessX](../../papers/harnessx.md)。

## English

Attach a page or table reference to each assessment; retain `unknown` until verified. These are evaluation-design checks, not new assessments of the included papers.

- [ ] Separate evolution and evaluation sets, keeping evaluation hidden during search → `held_out`. Why: search-set gains should not be mistaken for generalization; see [HDA](../../papers/hda.md).
- [ ] Keep evolution tasks disjoint from downstream evaluation benchmarks → `disjoint_evolution_set`. Why: reused tasks can inflate measured gains; see [ModularRSI](../../papers/modularrsi.md).
- [ ] Compare against compute-matched test-time scaling, including parallel sampling and sequential revision → `matched_budget_baseline`. Why: separate harness improvements from extra computation; see [Rethinking](../../papers/rethinking-evaluation.md).
- [ ] Transfer to other model families without re-evolution → `cross_model_transfer`. Why: test dependence on a particular execution model; see [Meta-Harness](../../papers/meta-harness.md).
- [ ] Report token or dollar costs, including evolution itself → `cost_reported`. Why: final inference cost alone does not describe the total budget; see [HDA](../../papers/hda.md).
- [ ] Repeat runs and report variance or Pass^k → `reliability_metric`. Why: a single success does not establish repeatability; see [RiseHarness](../../papers/riseharness.md).
- [ ] Check for leaked answers in container git history, benchmark answer files, and hardcoded answers → no dedicated `evidence` field; attach audit notes to the PR. Why: leakage undermines evaluation validity; see [Trusting Trust, Revisited](../../papers/trusting-trust-revisited.md).
- [ ] When claiming to improve the improvement process, compare successive generations from the same starting point and budget → no dedicated `evidence` field; this is distinct from `matched_budget_baseline`. Why: isolate the improver from changes in initialization and budget; see [Auditing](../../papers/auditing-product.md).
- [ ] Release code → `code_released`; release the evolved harness → `evolved_harness_released`. Why: reproducibility needs both the optimizer and its final execution artifact; see [HarnessOpt-Bench](../../papers/harnessopt-bench.md).
- [ ] Report failed settings and rounds where gains decline → no dedicated `evidence` field; describe them in the PR. Why: failure boundaries help identify where a method applies; see [HSI](../../papers/hsi.md) and [HarnessX](../../papers/harnessx.md).
