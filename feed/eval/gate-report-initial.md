# Follow RSI prompt evaluation

**Status: incomplete**

Evaluated: 45 / 45; missing metadata: 0; identity mismatches: 0.
Curator seeds awaiting owner review: 0.

| Metric | Measured | Required | Result |
| --- | ---: | ---: | --- |
| harness_precision | 0.955 | 0.85 | pass |
| harness_recall | 0.750 | 0.90 | fail |

Borderline predictions: 4
API/schema errors: 6

## Direction confusion matrix

```json
{
  "ai4ai": {
    "ai4ai": 3,
    "experience_world_model": 1
  },
  "data_task": {
    "data_task": 1
  },
  "evaluation_benchmark": {
    "ai4ai": 1,
    "evaluation_benchmark": 2
  },
  "experience_world_model": {
    "experience_world_model": 1
  },
  "harness": {
    "harness": 29
  },
  "theory_survey": {
    "theory_survey": 1
  }
}
```

## Mistakes

Baseline: owner re-review retained 8 of the 20 original Harness labels (precision 0.40).
The new set contains 25 owner decisions plus 20 preselected library positives. Ten calibration examples are visible in the gate prompt; the full-set result is not a blind holdout score.
Library labels are evaluation targets, not new full-text audits. HARBOR remains an owner-flagged scope ambiguity; its preselected positive label has not been changed to improve this score.
The 45-case set has more positives than the historical daily batch; compare the owner-only subset separately.

| Subset | Cases | Precision | Recall | True positives / target positives |
| --- | ---: | ---: | ---: | ---: |
| Full set | 45 | 0.955 | 0.750 | 21 / 28 |
| Owner-reviewed batch | 25 | 0.875 | 0.875 | 7 / 8 |
| Excluding prompt examples | 35 | 0.941 | 0.696 | 16 / 23 |

### Harness gate errors

- 2610.22732 (TokenEconomizer: Experience-Driven Black-Box Cost Control for Coding Agents): expected harness; predicted error / not run. 外部控制器在任务序列中注入技能、剪枝工具并干预失败，但摘要未明示执行反馈驱动其持续改写自身，证据不足。 Source guard: scope_support.feedback_quote.
- 2610.21453 (CarryOn: A Dual-Loop Harness for Personalized and Reliable Robot Assistance): expected borderline; predicted include / harness. 冻结VLA，执行失败经反思细化可复用恢复技能并跨任务重用
- 2608.07545 (DarwinX: Evolving Agent Harnesses Through Natural Selection): expected harness; predicted error / not run. 将自进化定义为对 harness 种群的选择：验证器反馈筛选变体，档案保留谱系，harness 可跨任务迁移。
- 2604.20938 (HARBOR: Automated Harness Optimization): expected harness; predicted borderline / borderline. 相关性依据仍不足，保留待审 Source guard: scope_support.persistence_quote.
- 2608.01918 (HarnessCompass: Guiding Automatic Harness Evolution toward Generalizable and Effective Agent Harnesses): expected harness; predicted error / not run. 自动演化外部 harness：以交互与主动反馈驱动组件级修改，演化结果迁移到新任务和其他模型，属持续性 Harness 改进。
- 2608.24735 (Meta$^n$: Recursive Self-Improvement through Emergent Depth): expected harness; predicted error / not run. Ω固定但递归生成策略层与工具库，轨迹/收敛反馈筛选层链并逐层继承，符合方法型RSI。
- 2607.03451 (SkillOpt-Lite: Better and Faster Agent Self-evolution via One Line of Vibe): expected harness; predicted borderline / borderline. 相关性依据仍不足，保留待审 Source guard: scope_support.persistence_quote.
- 2607.26598 (Living-Harness Is an Interactive-Agent Evolver): expected harness; predicted error / not run. 提出自进化 harness，用评估信号将轨迹转为持久程序性知识，检索复用于未来交互并跨轮累积。 Source guard: scope_support.object_quote.

### Scope and direction errors

- 2610.22732: expected include / harness; predicted error / harness. 外部控制器在任务序列中注入技能、剪枝工具并干预失败，但摘要未明示执行反馈驱动其持续改写自身，证据不足。
- 2610.21453: expected borderline / harness; predicted include / harness. 双环 harness 的恢复技能经执行失败反思改进，并在后续复用，符合方法型持续自改进。
- 2610.17184: expected include / ai4ai; predicted borderline / ai4ai. 共同发现并校验代理评估器yardstick，确认成果传给新agent，似环内验证器改进；但主要为外部目标优化，持久性证据偏弱。
- 2610.24944: expected include / ai4ai; predicted include / experience_world_model. Épi跨会话保留研究历史与分层记忆，并据实验经验演化方法，属持续自改进系统。
- 2610.04184: expected include / evaluation_benchmark; predicted include / ai4ai. 专门评测智能体为RSI自主构建可复用评测器的能力，属相关评测基准。
- 2610.14465: expected exclude / —; predicted borderline / model_weights. 路由与检索器交替训练形成反馈闭环，但未明确持久自改或跨任务继承，故存疑。
- 2610.19589: expected exclude / —; predicted error / evaluation_benchmark. 属任务基准与评测协议，比较可复用程序等脚手架在重复预测任务上的表现，未展示反馈驱动并跨轮继承的Harness修改，归评测类但收录存疑。
- 2608.07545: expected include / harness; predicted error / harness. 将自进化定义为对 harness 种群的选择：验证器反馈筛选变体，档案保留谱系，harness 可跨任务迁移。
- 2604.20938: expected include / harness; predicted borderline / harness. 摘要用贝叶斯优化自动搜索 Harness 配置，并由奖励/安全反馈驱动；但未明确优化结果用于后续任务或多轮自改进。
- 2608.01918: expected include / harness; predicted error / harness. 自动演化外部 harness：以交互与主动反馈驱动组件级修改，演化结果迁移到新任务和其他模型，属持续性 Harness 改进。
- 2608.24735: expected include / harness; predicted error / harness. Ω固定但递归生成策略层与工具库，轨迹/收敛反馈筛选层链并逐层继承，符合方法型RSI。
- 2607.03451: expected include / harness; predicted borderline / harness. 提出SkillOpt-Lite，以技能轨迹反馈和验证门控优化可编辑技能并联通HarnessOpt，属方法型RSI。
- 2607.26598: expected include / harness; predicted error / harness. 提出自进化 harness，用评估信号将轨迹转为持久程序性知识，检索复用于未来交互并跨轮累积。

Incomplete evaluation is not a passing quality gate.

Recommendations: inspect false negatives for persistence/RSI scope, false positives for static or single-round systems, and direction errors for the object retained between rounds. Keep labels unchanged unless the owner explicitly corrects them.
