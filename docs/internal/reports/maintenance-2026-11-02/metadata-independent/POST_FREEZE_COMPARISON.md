# 冻结后对照侧记

此文件在独立 findings.json 冻结后读取 A 的结论而作，不能标作盲审；不覆盖原冻结件、元数据或正式审核决定。

发现并纠正了本轮独立初稿的一项规则误用：owner 明确允许权重与 Harness 协同迭代，当前 harness_gate.md 却额外要求 Harness 是主要改进对象。初稿对 ECG/OmniBrain 的主对象排除理由撤回。具体工件仍需与训练数据、用户模拟器和记忆内容区分。

| 论文 | 独立冻结 | 冻结后建议 | 对照说明 |
| --- | --- | --- | --- |
| Agentic Self-Awareness | include | include | 独立冻结结论与 A 一致，保留原限定范围和证据边界。 |
| Mining the Design Space | include | include | 独立冻结结论与 A 一致，保留原限定范围和证据边界。 |
| EngramBench | include | include | 独立冻结结论与 A 一致，保留原限定范围和证据边界。 |
| Learner2Skill | include | exclude | 更正我初稿的 include：真实 SKILL.md 协议优化仍成立，但 owner 明确将用户模拟器列为范围外对象；本论文的直接输出和指标是模拟学习者响应，不能仅凭协议子流程越过这一明确排除项。 |
| EvoSteer | include | include | 独立冻结结论与 A 一致，保留原限定范围和证据边界。 |
| OptiCom | include | include | 独立冻结结论与 A 一致，保留原限定范围和证据边界。 |
| CUAWright | unknown | unknown | 保留我原先 unknown。A 依据已报告机制可作当前范围排除；我仍不将任务内正证加缺失跨任务说明视为“不保留”的定论。两者都不建议当前作为正例发布。 |
| Verification and Self-Improvement | include | exclude | 更正我初稿的 include：具体审计合同确实有用，但理论的 stage 包含权重、提示、工具、记忆，分析一般验证语义和选择错误；针对 Harness 案例的映射仍是 proposed audit questions，不足以确立“专门研究 Harness 演化”的范围。 |
| ECG-RSI | exclude | include | 撤回“权重是主对象所以排除”的附加门槛。新增读取 10.5 的 P5：被修的是数据工厂 operator/prompt/skill 组件版本，验收标准固定，明确 exact revision、同来源/请求/种子/预算比较及 next-round scope；这是生成机制自身修复，与改数据配比或波形产物分开。按 owner 协同更新例外，建议限定该修复子流程纳入。 |
| OmniBrain-0 | exclude | unknown | 撤回“主贡献训练模型所以排除”的附加门槛。论文确证固定模型下提醒验证、反馈修订和跨轮保留；但现有文字同时可表示 rubric/提醒内容累积，未充分区分固定提醒器使用更新经验与可复用策略工件自身变化。 |

冻结后建议：6 include、2 exclude、2 unknown；全部 defer。这是当前 reviewer 建议，不是主线程裁决或人工批准。

## 仍有分歧

- ECG-RSI：A 为 unclear，我在补读 Prompt P5 后建议限定到 construction-component repair 纳入 coevolution；生成器自身的 operator/prompt/skill 版本变化与波形/训练样本产物有文本证据区分，但未查实现版本差异。
- CUAWright：A 建议当前专题排除，我维持 unknown，原因是缺失长期保留描述不能直接转成“不保留”的事实；双方都不建议作为正例发布。

## 已有据更正

- Learner2Skill 改为 data_task：承认协议优化，仍遵守 owner 对用户模拟器的明确排除。
- Verification 改为通用 RSI 理论相关链接：v2 有更具体的接口审计，但仍是跨权重/提示/工具/记忆的通用理论，Harness 案例映射是审计问题。
- OmniBrain 改为 unknown：模型训练不能单独作为排除理由；外部提醒被反馈修订并跨轮保留的正证不变。官方项目仓库当前仅网站，Code: release soon，尚不能确认修改的是策略工件还是提醒内容。

详细规则原句、十条对照、补充引文和来源哈希见 post-freeze-comparison.json。原 FROZEN.sha256 仍完整有效。
