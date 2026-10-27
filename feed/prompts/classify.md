给这篇 RSI 论文分方向。只能使用下面定义的方向，不要自创类别。

{{ taxonomy_definitions }}   # 由程序展开 taxonomy.yaml 中的 directions、sub 与 cross，含 def_zh

规则：
- primary 选「每轮被改进、并带入下一轮的主要对象」所在的方向；
- 若 primary 是 harness，必须给出 harness_sub；
- secondary 最多 2 个，可以包含 cross 类别；
- 评测、基准、归因类论文的 primary 记为 evaluation_benchmark，理论与综述类记为 theory_survey，并在 secondary 里写它所研究的方向；
- 只根据标题和摘要判断。

标题：{{ title }}
摘要：{{ abstract }}

输出 JSON：
{"primary": "...", "harness_sub": "...|null", "secondary": ["..."],
 "improved_object_zh": "被改进并带入下一轮的对象，不超过 15 字",
 "confidence": 0.0-1.0}

## JSON Schema

```json
{
  "type": "object",
  "properties": {
    "primary": {
      "type": "string",
      "enum": [
        "harness",
        "model_weights",
        "data_task",
        "ai4ai",
        "experience_world_model",
        "meta",
        "embodied",
        "evaluation_benchmark",
        "theory_survey",
        "safety_governance"
      ]
    },
    "harness_sub": {
      "type": [
        "string",
        "null"
      ],
      "enum": [
        "evolve_main",
        "generalize",
        "evidence_selection",
        "improver",
        "component",
        "coevolution",
        null
      ]
    },
    "secondary": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": [
          "harness",
          "model_weights",
          "data_task",
          "ai4ai",
          "experience_world_model",
          "meta",
          "embodied",
          "evaluation_benchmark",
          "theory_survey",
          "safety_governance"
        ]
      },
      "maxItems": 2,
      "uniqueItems": true
    },
    "improved_object_zh": {
      "type": "string",
      "maxLength": 15
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    }
  },
  "required": [
    "primary",
    "harness_sub",
    "secondary",
    "improved_object_zh",
    "confidence"
  ],
  "additionalProperties": false
}
```
