# 冻结后对照：2026-11-01

初始粗范围判断 27 / 30 一致。`other_direction` 与 `exclude` 对齐为“不进入当前 Harness 专题”，细分类原样保留。对照没有改写双方冻结结果。

共同处置：**1 个 Harness 候选（EvoTeam）、25 个当前专题范围外、4 个待定**。待定包括 3 个边界分歧和 1 个出版社来源受阻。正式全部 `defer`，没有人工批准或发布。

| 分歧 | 初审 | 独立轮 | 共同处置 |
| --- | --- | --- | --- |
| SkillMem | exclude | unknown | unknown，需区分持久 procedure 演化与单轮参数蒸馏 |
| Kernel-Optimization loop | other_direction | unknown | unknown，需补管理规则改变的归因/工件/留存证据 |
| VEvo-Harness | borderline | include candidate | unknown，需技能/提示工件及执行实例，区分可执行行为修改与规则记忆更新 |

双方同意保留这些边界，不以强行统一标签替代证据。Elsevier Human–AI social systems 因正文 403、无摘要继续未知。

## 具体补证要求

### SkillMem: Compact External Skill Memory for Latent Multi-Agent Reasoning

初审按主方法训练 latent memory/reader、未演示递归技能更新而排除；独立轮认为成功/失败轨迹抽取并保留文字 procedure 是实质边界，缺乏证据时不宜写成确定无 Harness。双方事实认识基本相同，处置强度不同。

展示外部 procedure/技能库在后续改进轮中被反馈修订、准入与复用的记录；区分这条工件演化链与 latent-vector/reader 参数蒸馏。仅提供 frozen backbone 声明不足。

### A Case Study of a Multi-Agent Kernel-Optimization Loop That Learns a New AI Accelerator

两轮均确认 kernel 与 DSL 经验是主要改进对象，也均看到 single-head/验收规则改变；缺少改变由 Agent 自主提出及验证、持久保存的归因。初审建议 ai4ai 范围外，独立轮保留 unknown。

loop 策略/提示/验证程序的实际 diff、触发该修改的执行反馈、提出者与人工介入记录、修改准入及后续运行复用证据。Agent 写过全部代码不能替代演化链。

### VEvo-Harness: Causally-Guarded Self-Evolving Harness for Agentic Image Generation

独立轮根据冻结生成器、可执行技能、causal patch admission 与后续复用给出候选；初审指出正文细节主要为语义 embedding、置信度、EMA 与规则记忆，没有具体可编辑工件格式。正面机制主张存在，但不足以排除纯规则记忆更新解释。共同处置为待补证，不能把方法描述当作已查验实现。

至少一个技能/提示工件的 before/after、代码或文件 schema、执行入口、反馈生成并准入 patch 的实例，以及后续任务实际加载修改的记录；若只有策略向量/经验条目更新，应归经验方向。无需以文件扩展名判定，关键是可执行行为规范与持久更新。

所有主张仅涉及专题范围；论文实验数字未改，四类证据字段未批准。不能把这些 10 月 31 日补审条目包装成 11 月 1 日 HF 推荐。
