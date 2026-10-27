# Follow RSI prompt evaluation

**Status: incomplete**

Evaluated: 105 / 107; missing metadata: 0; identity mismatches: 2.
Curator seeds awaiting owner review: 27.

| Metric | Measured | Required | Result |
| --- | ---: | ---: | --- |
| include_recall | 0.918 | 0.90 | pass |
| include_precision | 0.989 | 0.80 | pass |
| primary_accuracy | 0.857 | 0.75 | pass |

Borderline predictions: 2
API/schema errors: 7

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
    "harness": 54,
    "<not-classified>": 5
  },
  "model_weights": {
    "model_weights": 5
  },
  "theory_survey": {
    "theory_survey": 8,
    "<not-classified>": 3
  }
}
```

## Mistakes

- 2607.13683: expected include / harness; predicted include / —. Gene Bank 保留演化中高性能 harness 供后续重组筛选
- 2608.07545: expected include / harness; predicted include / —. 验证器反馈选择harness种群并归档谱系，修改可跨任务迁移
- 2608.24876: expected include / harness; predicted error / —. relevance invalid after one retry: 'Meta-Agent依执行证据对Skill Memory做验证门控的持久更新，形成递归闭环' is too long

Failed validating 'maxLength' in schema['properties']['reason_zh']:
    {'type': 'string', 'maxLength': 40}

On instance['reason_zh']:
    'Meta-Agent依执行证据对Skill Memory做验证门控的持久更新，形成递归闭环'
- 2608.26530: expected include / harness; predicted error / —. relevance invalid after one retry: '摘要称live self-evolution把执行经验固化为可复用技能与记忆，持久更新harness' is too long

Failed validating 'maxLength' in schema['properties']['reason_zh']:
    {'type': 'string', 'maxLength': 40}

On instance['reason_zh']:
    '摘要称live self-evolution把执行经验固化为可复用技能与记忆，持久更新harness'
- 2606.14249: expected include / harness; predicted error / —. relevance invalid after one retry: '摘要称轨迹驱动AEGIS进化，将轨迹转为harness更新，持续修改并复用提示、工具、记忆、控制流。' is too long

Failed validating 'maxLength' in schema['properties']['reason_zh']:
    {'type': 'string', 'maxLength': 40}

On instance['reason_zh']:
    '摘要称轨迹驱动AEGIS进化，将轨迹转为harness更新，持续修改并复用提示、工具、记忆、控制流。'
- 2607.24300: expected include / evaluation_benchmark; predicted include / harness. 分析自改代理自写验证失效并提出SEAL审计，接受后保留整个incumbent状态
- 2609.04280: expected include / evaluation_benchmark; predicted borderline / evaluation_benchmark. 评测外部harness演化下的保留与适应，未体现系统自我修改
- 2609.17817: expected include / evaluation_benchmark; predicted include / safety_governance. 评测自修改编码智能体的自我改进过程，污染可跨轮保留
- 2610.30499: expected include / evaluation_benchmark; predicted include / harness. 模型据反馈两次改写harness代码，修改保留并再评测
- 2608.03392: expected include / theory_survey; predicted error / —. relevance invalid after one retry: '综述自进化编程智能体，摘要明言其persistently更新framework、memory、skills与tools' is too long

Failed validating 'maxLength' in schema['properties']['reason_zh']:
    {'type': 'string', 'maxLength': 40}

On instance['reason_zh']:
    '综述自进化编程智能体，摘要明言其persistently更新framework、memory、skills与tools'
- 2609.00006: expected include / theory_survey; predicted exclude / —. 仅源码解剖十一个 harness 架构与设计模式，无自我修改保留闭环
- 2609.11873: expected include / theory_survey; predicted borderline / theory_survey. 摘要提出RSI路线图，属理论讨论而非具体自改系统或评测
- 2610.18813: expected include / theory_survey; predicted error / —. relevance invalid after one retry: '摘要称accepted revisions persist，即修订跨运行保留，含理论分析' is too long

Failed validating 'maxLength' in schema['properties']['reason_zh']:
    {'type': 'string', 'maxLength': 40}

On instance['reason_zh']:
    '摘要称accepted revisions persist，即修订跨运行保留，含理论分析'
- 2610.20431: expected include / ai4ai; predicted include / harness. 用实验反馈变异假设与实现，并保留复用经验形成递归改进闭环
- 2609.08183: expected include / data_task; predicted include / model_weights. 能力引导分配把评估反馈转为下一轮训练配比，闭合评估—选择—更新回路，权重持久更新
- 2610.18842: expected include / embodied; predicted include / theory_survey. 摘要提出L0-L5框架并综述区分能力级与元级更新，属RSI评测分析类
- 2607.21461: expected exclude / —; predicted include / harness. 外循环审计答案并更新压缩改进状态，指导后续研究，属记忆/工作流自我修改并跨轮保留

## Metadata identity mismatches

- 2609.08175: expected **Safe Harness Self-Evolution: A Theoretical Analysis of Feasibility and Limits**, returned **A Theory of Reliable Self-Evolution for Agent Harnesses**. No label changed; example not scored.
- 2607.07007: expected **State-machine fuzz harness generation**, returned **Thinking More, Harnessing Better: State Machine Guided Harness Automatic Generation with Project Digestion and Workflow Decomposition**. No label changed; example not scored.

Incomplete evaluation is not a passing quality gate.

Recommendations: inspect false negatives for persistence/RSI scope, false positives for static or single-round systems, and direction errors for the object retained between rounds. Keep labels unchanged unless the owner explicitly corrects them.
