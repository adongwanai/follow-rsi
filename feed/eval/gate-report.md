# Follow RSI prompt evaluation

**Status: complete**

Evaluated: 45 / 45; missing metadata: 0; identity mismatches: 0.
Curator seeds awaiting owner review: 0.

| Metric | Measured | Required | Result |
| --- | ---: | ---: | --- |
| harness_precision | 0.960 | 0.85 | pass |
| harness_recall | 0.857 | 0.90 | fail |

Borderline predictions: 7
API/schema errors: 0

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
    "evaluation_benchmark": 3
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
| Full set | 45 | 0.960 | 0.857 | 24 / 28 |
| Owner-reviewed batch | 25 | 0.875 | 0.875 | 7 / 8 |
| Excluding prompt examples | 35 | 0.950 | 0.826 | 19 / 23 |

### Harness gate errors

- 2610.22732 (TokenEconomizer: Experience-Driven Black-Box Cost Control for Coding Agents): expected harness; predicted borderline / borderline. 相关性依据仍不足，保留待审 Source guard: scope_support.feedback_quote.
- 2610.21453 (CarryOn: A Dual-Loop Harness for Personalized and Reliable Robot Assistance): expected borderline; predicted include / harness. 冻结VLA，执行失败经反思细化可复用恢复技能并跨任务重用
- 2604.20938 (HARBOR: Automated Harness Optimization): expected harness; predicted borderline / borderline. 相关性依据仍不足，保留待审 Source guard: scope_support.persistence_quote.
- 2607.03451 (SkillOpt-Lite: Better and Faster Agent Self-evolution via One Line of Vibe): expected harness; predicted borderline / borderline. 相关性依据仍不足，保留待审 Source guard: scope_support.persistence_quote.
- 2607.26598 (Living-Harness Is an Interactive-Agent Evolver): expected harness; predicted borderline / borderline. 相关性依据仍不足，保留待审 Source guard: scope_support.object_quote.

### Scope and direction errors

- 2610.22732: expected include / harness; predicted borderline / harness. 外部控制器在任务序列中注入技能、剪枝工具并干预失败，但摘要未明示执行反馈驱动其持续改写自身，证据不足。
- 2610.21453: expected borderline / harness; predicted include / harness. 双环 harness 的恢复技能经执行失败反思改进，并在后续复用，符合方法型持续自改进。
- 2610.17184: expected include / ai4ai; predicted borderline / ai4ai. 共同发现并校验代理评估器yardstick，确认成果传给新agent，似环内验证器改进；但主要为外部目标优化，持久性证据偏弱。
- 2610.24944: expected include / ai4ai; predicted include / experience_world_model. Épi跨会话保留研究历史与分层记忆，并据实验经验演化方法，属持续自改进系统。
- 2610.14465: expected exclude / —; predicted borderline / model_weights. 路由与检索器交替训练形成反馈闭环，但未明确持久自改或跨任务继承，故存疑。
- 2610.19589: expected exclude / —; predicted borderline / evaluation_benchmark. 属任务基准与评测协议，比较可复用程序等脚手架在重复预测任务上的表现，未展示反馈驱动并跨轮继承的Harness修改，归评测类但收录存疑。
- 2604.20938: expected include / harness; predicted borderline / harness. 摘要用贝叶斯优化自动搜索 Harness 配置，并由奖励/安全反馈驱动；但未明确优化结果用于后续任务或多轮自改进。
- 2607.03451: expected include / harness; predicted borderline / harness. 提出SkillOpt-Lite，以技能轨迹反馈和验证门控优化可编辑技能并联通HarnessOpt，属方法型RSI。
- 2607.26598: expected include / harness; predicted borderline / harness. 提出自进化 harness，用评估信号将轨迹转为持久程序性知识，检索复用于未来交互并跨轮累积。

Recommendations: inspect false negatives for persistence/RSI scope, false positives for static or single-round systems, and direction errors for the object retained between rounds. Keep labels unchanged unless the owner explicitly corrects them.
