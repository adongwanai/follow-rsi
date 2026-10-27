# 可切入的研究空白（每条都有收录论文作为证据）

1. **什么任务值得演化 Harness**：[Rethinking](../papers/rethinking-evaluation.md) 在 TB2.1 上未胜过测试时扩展，[HDA](../papers/hda.md) 把大部分收益归为过拟合与额外计算；但长程游戏上优势明显。「任务对 Harness 的敏感度」本身可以做成系统分析，[Evo-Bench](../papers/evo-bench.md) 的选题指标是起点。

2. **无真值验证器时的准入**：[Evo-Harness](../papers/evo-harness.md) 与 [Self-Authored Verification](../papers/self-authored-verification.md) 都发现自判会误导演化；[Harness²](../papers/harness2.md)、[TTHE](../papers/tthe.md)、[HarnessPro](../papers/harnesspro.md)、[Agent S4](../papers/agent-s4.md) 各给了代理信号方案，但都没有分析代理信号何时失效。

3. **改 Harness 还是改权重**：[SIA](../papers/sia.md) 的选择策略是静态的；[Self-HPO](../papers/self-hpo.md) 显示交替更新优于只改一边，但自我提议（64.8）仍不及强外部提议器（66.3）；[HarnessForge](../papers/harnessforge.md)、[CoEvo-RSI](../papers/coevo-rsi.md)、[Co-Evolving](../papers/co-evolving-harnesses-models.md) 都指向「匹配性」，但怎么度量匹配性仍是空白。

4. **证明元层真的变好**：[Auditing](../papers/auditing-product.md) 统计只有 4/26 的工作做了同起点、同预算的前后代对比；[ARC-AGI-3](../papers/arc-agi-3-controlled.md) 受控研究的留出提升区间跨过零。

5. **证据选择的理论**：[SSR](../papers/ssr.md)、[ActiveSaddler](../papers/activesaddler.md)、[ECDYSIS](../papers/ecdysis.md) 都是实证规则；[REUSE](../papers/reuse.md) 与 [Safe Harness Self-Evolution](../papers/safe-harness-self-evolution.md) 给了部分统计理论，但还没人把「选哪些失败」和泛化界连起来。

6. **稀疏反馈、长程与具身**：[DemoEvolve](../papers/demoevolve.md)、[EMHO](../papers/emho.md)、[HSI](../papers/hsi.md) 都报告了失败或边界；[RiseHarness](../papers/riseharness.md) 用 Pass^r 说明可靠性是和覆盖率不同的优化目标。

7. **安全与可审计**：投毒 benchmark、答案泄露、预算绕过都已被实际观察到；把「自改过程的可审计性」做成可度量指标，目前仍少有人做。 证据：[trusting-trust-revisited](../papers/trusting-trust-revisited.md) · [rsigym](../papers/rsigym.md) · [self-authored-verification](../papers/self-authored-verification.md)。

## English

Machine translation of the Chinese text above.

1. **Which tasks are worth evolving a harness for?** [Rethinking](../papers/rethinking-evaluation.md) does not outperform test-time scaling on TB2.1, and [HDA](../papers/hda.md) attributes most gains to overfitting and extra computation; however, advantages are clear in long-horizon games. Task sensitivity to harness quality can itself be studied systematically, with [Evo-Bench](../papers/evo-bench.md)’s task-selection criteria as a starting point.

2. **Admission without a ground-truth verifier** [Evo-Harness](../papers/evo-harness.md) and [Self-Authored Verification](../papers/self-authored-verification.md) both find that self-judgment can mislead evolution; [Harness²](../papers/harness2.md), [TTHE](../papers/tthe.md), [HarnessPro](../papers/harnesspro.md), and [Agent S4](../papers/agent-s4.md) each offer proxy signals, but none analyzes when those proxies fail.

3. **Change the harness or the weights?** [SIA](../papers/sia.md)’s selection policy is static; [Self-HPO](../papers/self-hpo.md) shows that alternating updates outperform changing only one side, but self-proposal (64.8) still trails a strong external proposer (66.3). [HarnessForge](../papers/harnessforge.md), [CoEvo-RSI](../papers/coevo-rsi.md), and [Co-Evolving](../papers/co-evolving-harnesses-models.md) all point to compatibility, yet how to measure it remains open.

4. **Demonstrate that the meta level really improves** [Auditing](../papers/auditing-product.md) finds that only 4/26 studies compare successive generations from the same starting point and under the same budget; the held-out improvement interval in the [ARC-AGI-3](../papers/arc-agi-3-controlled.md) controlled study crosses zero.

5. **A theory of evidence selection** [SSR](../papers/ssr.md), [ActiveSaddler](../papers/activesaddler.md), and [ECDYSIS](../papers/ecdysis.md) use empirical rules; [REUSE](../papers/reuse.md) and [Safe Harness Self-Evolution](../papers/safe-harness-self-evolution.md) provide some statistical theory, but no one has connected which failures to select with generalization bounds.

6. **Sparse feedback, long horizons, and embodiment** [DemoEvolve](../papers/demoevolve.md), [EMHO](../papers/emho.md), and [HSI](../papers/hsi.md) all report failures or boundaries; [RiseHarness](../papers/riseharness.md) uses Pass^r to show that reliability is a different optimization objective from coverage.

7. **Safety and auditability** Benchmark poisoning, answer leakage, and budget bypassing have all been observed in practice; making the auditability of self-modification a measurable metric is still rarely explored. Evidence: [trusting-trust-revisited](../papers/trusting-trust-revisited.md) · [rsigym](../papers/rsigym.md) · [self-authored-verification](../papers/self-authored-verification.md).
