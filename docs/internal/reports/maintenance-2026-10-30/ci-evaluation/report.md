# Follow RSI prompt evaluation

**Status: incomplete**

Evaluated: 105 / 107; missing metadata: 0; identity mismatches: 2.
Curator seeds awaiting owner review: 27.

| Metric | Measured | Required | Result |
| --- | ---: | ---: | --- |
| include_recall | 0.980 | 0.90 | pass |
| include_precision | 1.000 | 0.80 | pass |
| primary_accuracy | 0.878 | 0.75 | pass |

Borderline predictions: 3
API/schema errors: 0

## Direction confusion matrix

```json
{
  "ai4ai": {
    "ai4ai": 2
  },
  "data_task": {
    "model_weights": 2,
    "data_task": 1
  },
  "embodied": {
    "theory_survey": 1
  },
  "evaluation_benchmark": {
    "evaluation_benchmark": 11,
    "safety_governance": 1,
    "harness": 1
  },
  "experience_world_model": {
    "experience_world_model": 4
  },
  "harness": {
    "harness": 53,
    "meta": 2,
    "model_weights": 4
  },
  "model_weights": {
    "model_weights": 5
  },
  "theory_survey": {
    "theory_survey": 10,
    "harness": 1
  }
}
```

## Mistakes

- 2609.06396: expected include / harness; predicted include / meta. 摘要提出数据、Harness、模型三类算子的多轮自改进框架；Harness编辑外部脚手架，并由失败反馈驱动且收益跨后续模型继承。
- 2609.35738: expected include / harness; predicted include / meta. 提出harness learning，用执行反馈迭代修订外部harness，并保留多轮改进能力，属于方法类RSI。
- 2608.05446: expected include / harness; predicted include / model_weights. 提出可学习的运行时Harness协调机制，通过监督初始化与成本感知GRPO改进，并让外部工作区持续演化以支持后续任务。
- 2610.12176: expected include / harness; predicted include / model_weights. MASS 交替优化多智能体工作流与自生成轨迹微调，由执行自评反馈驱动，多轮循环持续自举，属方法型 RSI。
- 2610.22791: expected include / harness; predicted include / model_weights. 提出Self-HPO递归交替优化harness与policy，用自身失败和困难任务驱动后续轮次，属方法型RSI。
- 2610.31401: expected include / harness; predicted include / model_weights. 持续学习框架在harness侧反复精炼技能并保留失败样例，蒸馏内化经验，跨25阶段任务流评估，符合Harness RSI方法论。
- 2609.17817: expected include / evaluation_benchmark; predicted include / safety_governance. 研究自修改编码智能体自我改进循环遭基准投毒及污染延续，属对持续自改进系统的安全评测。
- 2610.30499: expected include / evaluation_benchmark; predicted include / harness. 受控评测前沿模型能否自主构建并多轮改进任务harness，属Harness自改进评测。
- 2609.00006: expected include / theory_survey; predicted borderline / theory_survey. 对十一个编码Harness做源码解剖与演化审计，未显式体现反馈驱动的持续自改进闭环，相关性存疑。
- 2610.18813: expected include / theory_survey; predicted include / harness. 摘要明确提出对提示、记忆、工作流和可执行组件等Harness工件进行反馈驱动且跨运行保留的自我修订，契合Harness RSI。
- 2607.28568: expected include / ai4ai; predicted borderline / ai4ai. 执行反馈训练进化算子并用于长程搜索，但持久多轮自改进闭环不明确
- 2609.08183: expected include / data_task; predicted include / model_weights. 摘要描述了路由harness驱动的多轮后训练闭环：评估反馈决定下一轮训练混合，形成自改进循环。
- 2610.14118: expected include / data_task; predicted include / model_weights. 多轮闭环：任务合成→训练→诊断反馈再进入下一轮，并将精炼任务迁移至小模型。
- 2610.18842: expected include / embodied; predicted include / theory_survey. 综述兼框架论文，专门研究机器人物理递归自改进（含harness适配与模型训练），提出L0-L5分级并评估现状。
- 2607.20709: expected exclude / —; predicted borderline / harness. 提出用Python对象构建Agent的固定框架，摘要未展示由反馈驱动修改并被后续任务继承的自改进闭环。

## Metadata identity mismatches

- 2609.08175: expected **Safe Harness Self-Evolution: A Theoretical Analysis of Feasibility and Limits**, returned **A Theory of Reliable Self-Evolution for Agent Harnesses**. No label changed; example not scored.
- 2607.07007: expected **State-machine fuzz harness generation**, returned **Thinking More, Harnessing Better: State Machine Guided Harness Automatic Generation with Project Digestion and Workflow Decomposition**. No label changed; example not scored.

Incomplete evaluation is not a passing quality gate.

Recommendations: inspect false negatives for persistence/RSI scope, false positives for static or single-round systems, and direction errors for the object retained between rounds. Keep labels unchanged unless the owner explicitly corrects them.
