给这篇 RSI 候选论文分方向。只使用标题、摘要和下面的分类定义；证据不足时保持未知，不根据名称或关键词猜。

{{ taxonomy_definitions }}

先判断“实际被改进并带入下一轮的主要对象”，再选择 primary；不能把实现中使用 Agent、工具或记忆当作 Harness。

Harness 必须同时满足：
- 改的是外部可复用 Harness 工件，如提示、工具代码/工具库、技能文件、记忆或上下文管理的代码/策略、控制流、工作流、环内验证器或改进器；
- 执行/评估反馈驱动工件修改，接受后的版本用于后续任务/改进轮次；
- 权重冻结或不是主要训练对象。
外部 Harness 的对象、反馈与持久复用依据将由独立 harness_gate 再检查。

边界：RL/SFT 训练出的模型 policy → model_weights；训练环境/奖励/用户模拟器 → training_system；外部科研假设、内核或工程代码产物 → research_output；积累的记忆数据、经验价值评分、研究历史 → experience_data；任务进展/当前上下文状态 → task_state。它们不能只因为持久保存就成为 harness_artifact。正文可能有其他机制但摘要未明确时，用 unknown，不补推断。模型与 Harness 协同演化需要两类对象分别有更新证据，两个 neural policy 联合训练不算。

方向规则：
- primary=harness 必须有 harness_sub，其余 primary 的 harness_sub=null；
- secondary 最多 2 个，不重复 primary。没有明确交叉贡献时留空；
- evaluation_benchmark / theory_survey 的 primary 分别用于评测与理论综述。普通 RSI、经验学习或多种系统的评测/综述，不因涵盖或列举 Harness 组件就填 secondary harness；
- 只有摘要明确以 Harness 工件的反馈演化为专项研究对象，才可为评测/综述添加 secondary harness，并由后续闸门检查专项研究依据。不能借用一般 RSI 定义或泛泛的 prompts/memory/tools 枚举；
- 方法中 secondary harness 也需要独立、明确的外部 Harness 修改与持久复用依据。主研究对象为科研/模型时不应被 Harness 的辅助角色取代。

improved_object_zh 不超过 15 字。输出候选方向不会使证据不足的论文自动 include。

标题：{{ title }}
摘要：{{ abstract }}

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
