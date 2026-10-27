你是递归自我改进（RSI）方向的文献编辑。判断下面这篇论文是否应收录进 RSI 进展追踪。

收录标准（两条都满足才算 include）：
1. 系统根据执行、实验或评估反馈，修改它自己的某个部分（权重、数据、提示、工具、记忆、技能、控制流、工作流、改进机制本身之一）；
2. 被接受的修改会保留下来，并在后续任务或后续改进轮次中使用。

也要收录：专门评测、归因、理论分析或综述上述系统的论文（它们自己不改进也算）。

排除（label = exclude，并给出 exclude_reason）：
- not_persistent：只在当前任务内迭代，修改不保留到后续任务
- static_framework：提出固定框架，本身不随反馈演化
- different_sense_of_harness：harness 指测试框架、模糊测试框架等其他含义
- single_round_training：只做一次训练或蒸馏，没有可迭代的改进闭环
- off_topic：与 RSI 无关

拿不准时用 borderline，不要硬判。只根据下面提供的标题和摘要判断，不要使用你对这篇论文的任何其他记忆。

标题：{{ title }}
摘要：{{ abstract }}

输出 JSON：
{"label": "include|borderline|exclude",
 "exclude_reason": "not_persistent|static_framework|different_sense_of_harness|single_round_training|off_topic|null",
 "reason_zh": "不超过 40 字，指出摘要里的哪句话支撑你的判断",
 "confidence": 0.0-1.0}

## JSON Schema

```json
{
  "type": "object",
  "properties": {
    "label": {
      "type": "string",
      "enum": [
        "include",
        "borderline",
        "exclude"
      ]
    },
    "exclude_reason": {
      "type": [
        "string",
        "null"
      ],
      "enum": [
        "not_persistent",
        "static_framework",
        "different_sense_of_harness",
        "single_round_training",
        "off_topic",
        null
      ]
    },
    "reason_zh": {
      "type": "string",
      "maxLength": 40
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    }
  },
  "required": [
    "label",
    "exclude_reason",
    "reason_zh",
    "confidence"
  ],
  "additionalProperties": false
}
```
