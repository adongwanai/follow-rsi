把下面的中文摘要翻译成英文，给研究者看。不增删任何事实；数字、单位、正负号、百分号逐字保留；方法名和基准名保持原样；不超过 30 个英文单词（按空白分词）。如超限，重新简写并保留完整事实，不要截断句子。

中文：{{ summary_zh }}

输出 JSON：{"summary_en": "..."}

## JSON Schema

```json
{
  "type": "object",
  "properties": {
    "summary_en": {
      "type": "string",
      "minLength": 1
    }
  },
  "required": [
    "summary_en"
  ],
  "additionalProperties": false
}
```
