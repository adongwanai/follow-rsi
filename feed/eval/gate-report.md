# Follow RSI prompt evaluation

**Status: incomplete**

Evaluated: 45 / 45; missing metadata: 0; identity mismatches: 0.
Curator seeds awaiting owner review: 0.

| Metric | Measured | Required | Result |
| --- | ---: | ---: | --- |
| harness_precision | 0.962 | 0.85 | pass |
| harness_recall | 0.893 | 0.90 | fail |

Borderline predictions: 3
API/schema errors: 3

## Direction confusion matrix

```json
{
  "ai4ai": {
    "ai4ai": 3,
    "experience_world_model": 1
  },
  "data_task": {
    "<not-classified>": 1
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
| Full set | 45 | 0.962 | 0.893 | 25 / 28 |
| Owner-reviewed batch | 25 | 0.889 | 1.000 | 8 / 8 |
| Excluding prompt examples | 35 | 0.952 | 0.870 | 20 / 23 |

### Harness gate errors

- 2610.21453 (CarryOn: A Dual-Loop Harness for Personalized and Reliable Robot Assistance): expected borderline; predicted include / harness. 失败反馈驱动恢复技能反思更新并复用，冻结VLA
- 2604.20938 (HARBOR: Automated Harness Optimization): expected harness; predicted borderline / borderline. 摘要明确自动优化 harness 配置，但未说明修改在后续任务保留复用证据 Source guard: scope_support.persistence_quote.
- 2609.18366 (Bad Genius: Counterfactual-Guided Harness Evolution Beyond Task-Specific Shortcuts): expected harness; predicted error / not run. CHASE以反事实基准生成约束，驱动Proposer多轮改写提示、记忆、工具等Harness，并把有效反事实存入档案。
- 2609.09134 (Co-Evolving Harnesses and Models: On-Policy Correction Helps Weaker Models Catch Up Where Imitation Fails): expected harness; predicted borderline / borderline. 明显有 harness 演化与权重共同更新，但反馈驱动细节未明

### Scope and direction errors

- 2610.21453: expected borderline / harness; predicted include / harness. 提出双环Harness：规划环持续更新用户/场景上下文，恢复技能经失败反思改进并在后续被复用，构成外部可复用工件的改进闭环。
- 2610.16523: expected include / data_task; predicted exclude / —. EAU改写训练环境、奖励、用户模拟器与RL配置，并非外部推理Harness。
- 2610.24944: expected include / ai4ai; predicted include / experience_world_model. 摘要表明 Épi 跨会话保留研究历史，依实验积累经验进化方法，并将方法延续到后续研究，符合持续自改进方法。
- 2610.04184: expected include / evaluation_benchmark; predicted error / evaluation_benchmark. 专门评测AI智能体自主设计评估器，为RSI构建反馈，属该方向评测基准。
- 2610.34238: expected include / evaluation_benchmark; predicted error / evaluation_benchmark. 基准专门评测智能体在工具生态演化下持续修正积累的程序性知识的能力，属评测持续自改进系统。
- 2610.22273: expected exclude / —; predicted include / model_weights. 构建可复用工作区，以RL按下游准确率优化构建策略，工作区跨重复查询复用。
- 2610.14465: expected exclude / —; predicted include / model_weights. 规则路由与检索器交替训练，检索表现反馈更新路由，选出的规则监督检索器，形成闭环共同自适应。
- 2610.19589: expected exclude / —; predicted borderline / evaluation_benchmark. 赛马预测评测基准，含可复用预测程序工作流与修订增益，但未明确展示跨轮持续自改进闭环，属评测边界。
- 2604.20938: expected include / harness; predicted borderline / harness. 提出用贝叶斯优化自动搜索 harness 配置，奖励驱动搜索明确；但摘要未说明优化结果用于后续任务或改进轮次，持久性存疑。
- 2609.18366: expected include / harness; predicted error / harness. CHASE以反事实基准生成约束，驱动Proposer多轮改写提示、记忆、工具等Harness，并把有效反事实存入档案。
- 2609.09134: expected include / harness; predicted borderline / harness. 先自动进化 harness，再依据专家轨迹训练回退的实验反馈，提出 on-policy 纠错管线并保留规划风格，属协同改进方法。

Incomplete evaluation is not a passing quality gate.

Recommendations: inspect false negatives for persistence/RSI scope, false positives for static or single-round systems, and direction errors for the object retained between rounds. Keep labels unchanged unless the owner explicitly corrects them.
