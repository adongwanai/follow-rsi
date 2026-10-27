# Follow RSI prompt evaluation

**Status: incomplete**

Evaluated: 105 / 107; missing metadata: 0; identity mismatches: 2.
Curator seeds awaiting owner review: 27.

| Metric | Measured | Required | Result |
| --- | ---: | ---: | --- |
| include_recall | 0.959 | 0.90 | pass |
| include_precision | 0.989 | 0.80 | pass |
| primary_accuracy | 0.908 | 0.75 | pass |

Borderline predictions: 2
API/schema errors: 1

## Direction confusion matrix

```json
{
  "ai4ai": {
    "harness": 1,
    "ai4ai": 1
  },
  "data_task": {
    "model_weights": 1,
    "data_task": 2
  },
  "embodied": {
    "theory_survey": 1
  },
  "evaluation_benchmark": {
    "evaluation_benchmark": 10,
    "harness": 2,
    "safety_governance": 1
  },
  "experience_world_model": {
    "experience_world_model": 4
  },
  "harness": {
    "harness": 58,
    "<not-classified>": 1
  },
  "model_weights": {
    "model_weights": 5
  },
  "theory_survey": {
    "theory_survey": 9,
    "<not-classified>": 1,
    "harness": 1
  }
}
```

## Mistakes

- 2608.24876: expected include / harness; predicted error / —. relevance invalid after one retry: '摘要称固定Meta-Agent将执行证据转为对技能记忆的门控更新，形成递归演化闭环' is too long

Failed validating 'maxLength' in schema['properties']['reason_zh']:
    {'type': 'string', 'maxLength': 40}

On instance['reason_zh']:
    '摘要称固定Meta-Agent将执行证据转为对技能记忆的门控更新，形成递归演化闭环'
- 2607.24300: expected include / evaluation_benchmark; predicted include / harness. 分析自改代理自写验证失效并提出SEAL审计，接受后保留整个incumbent状态
- 2609.04280: expected include / evaluation_benchmark; predicted borderline / evaluation_benchmark. 评测外部harness演化下的保留与适应，未体现系统自我修改
- 2609.17817: expected include / evaluation_benchmark; predicted include / safety_governance. 评测自修改编码智能体的自我改进过程，污染可跨轮保留
- 2610.30499: expected include / evaluation_benchmark; predicted include / harness. 模型据反馈两次改写harness代码，修改保留并再评测
- 2609.00006: expected include / theory_survey; predicted exclude / —. 仅源码解剖十一个 harness 架构与设计模式，无自我修改保留闭环
- 2609.11873: expected include / theory_survey; predicted borderline / theory_survey. 摘要提出RSI路线图，属理论讨论而非具体自改系统或评测
- 2610.18813: expected include / theory_survey; predicted include / harness. 摘要称自演化修改提示、记忆、工作流与代码，且接受的修改跨运行保留
- 2610.20431: expected include / ai4ai; predicted include / harness. 用实验反馈变异假设与实现，并保留复用经验形成递归改进闭环
- 2609.08183: expected include / data_task; predicted include / model_weights. 能力引导分配把评估反馈转为下一轮训练配比，闭合评估—选择—更新回路，权重持久更新
- 2610.18842: expected include / embodied; predicted include / theory_survey. 摘要提出L0-L5框架并综述区分能力级与元级更新，属RSI评测分析类
- 2607.21461: expected exclude / —; predicted include / harness. 外循环审计答案并更新压缩改进状态，指导后续研究，属记忆/工作流自我修改并跨轮保留

## Metadata identity mismatches

- 2609.08175: expected **Safe Harness Self-Evolution: A Theoretical Analysis of Feasibility and Limits**, returned **A Theory of Reliable Self-Evolution for Agent Harnesses**. No label changed; example not scored.
- 2607.07007: expected **State-machine fuzz harness generation**, returned **Thinking More, Harnessing Better: State Machine Guided Harness Automatic Generation with Project Digestion and Workflow Decomposition**. No label changed; example not scored.

Incomplete evaluation is not a passing quality gate.

Recommendations: inspect false negatives for persistence/RSI scope, false positives for static or single-round systems, and direction errors for the object retained between rounds. Keep labels unchanged unless the owner explicitly corrects them.
