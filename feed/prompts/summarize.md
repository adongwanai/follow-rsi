用中文为这篇论文写一句话摘要，给关注 RSI 的研究者看。

要求：
- 40–90 个汉字，一句或两句；
- 先说它改进了什么、怎么改进，再说最重要的一个结果；
- 数字只能使用标题和摘要里原样出现的数字，单位和正负号不变；摘要没给数字就不写数字；
- 不用「首个」「突破性」「显著」等评价性词语，除非摘要原文这样说，且要写成「作者称」；
- 方法名、基准名保留英文原文；
- 不加引号、表情或标签。

标题：{{ title }}
摘要：{{ abstract }}

输出 JSON：{"summary_zh": "..."}

## JSON Schema

```json
{
  "type": "object",
  "properties": {
    "summary_zh": {
      "type": "string",
      "minLength": 1
    }
  },
  "required": [
    "summary_zh"
  ],
  "additionalProperties": false
}
```
