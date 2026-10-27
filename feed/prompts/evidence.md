只根据摘要，判断这篇论文是否报告了以下实验设计。规则：
- 只有摘要明确写出时才填 "yes"，并在 quote 里给出摘要中支撑它的原文片段（必须逐字复制，长度 5–60 个字符）；
- 摘要没写，一律填 "unknown"，不得填 "no"；
- 不要根据常识或你对论文的记忆推断。

字段：
- held_out：在演化或训练中未见过的任务、基准或划分上评估
- matched_budget：与同等计算或推理预算的基线（如并行采样、测试时扩展）对比
- cross_model：改进结果迁移到其他模型或模型家族
- code_released：摘要或评论中给出了代码或项目链接

摘要：{{ abstract }}
评论字段：{{ comments }}

输出 JSON：
{"held_out": {"value": "yes|unknown", "quote": "...|null"},
 "matched_budget": {"value": "yes|unknown", "quote": "...|null"},
 "cross_model": {"value": "yes|unknown", "quote": "...|null"},
 "code_released": {"value": "yes|unknown", "quote": "...|null"}}

## JSON Schema

```json
{
  "type": "object",
  "properties": {
    "held_out": {
      "type": "object",
      "properties": {
        "value": {
          "type": "string",
          "enum": [
            "yes",
            "unknown"
          ]
        },
        "quote": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "required": [
        "value",
        "quote"
      ],
      "additionalProperties": false
    },
    "matched_budget": {
      "type": "object",
      "properties": {
        "value": {
          "type": "string",
          "enum": [
            "yes",
            "unknown"
          ]
        },
        "quote": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "required": [
        "value",
        "quote"
      ],
      "additionalProperties": false
    },
    "cross_model": {
      "type": "object",
      "properties": {
        "value": {
          "type": "string",
          "enum": [
            "yes",
            "unknown"
          ]
        },
        "quote": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "required": [
        "value",
        "quote"
      ],
      "additionalProperties": false
    },
    "code_released": {
      "type": "object",
      "properties": {
        "value": {
          "type": "string",
          "enum": [
            "yes",
            "unknown"
          ]
        },
        "quote": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "required": [
        "value",
        "quote"
      ],
      "additionalProperties": false
    }
  },
  "required": [
    "held_out",
    "matched_budget",
    "cross_model",
    "code_released"
  ],
  "additionalProperties": false
}
```
