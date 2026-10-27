下面是本周通过人工审核的 RSI 论文统计和标题列表。写一段周报开头，中文 2–3 句：说明本周各方向新增多少篇、哪个方向最集中。只能使用下面给出的数字和名称，不要评价论文好坏，不要推荐论文（推荐由编辑另写）。

本周统计：{{ counts_by_direction }}
本周标题：{{ titles }}

输出 JSON：{"intro_zh": "...", "intro_en": "..."}

## JSON Schema

```json
{
  "type": "object",
  "properties": {
    "intro_zh": {
      "type": "string"
    },
    "intro_en": {
      "type": "string"
    }
  },
  "required": [
    "intro_zh",
    "intro_en"
  ],
  "additionalProperties": false
}
```
