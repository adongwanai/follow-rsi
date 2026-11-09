# 共演化判据补丁（已准备，未应用）

Owner 的修复说明明确：“权重和 Harness 都被迭代修改，算 harness/coevolution”。当前 taxonomy 子类也是这个定义，但 classify/gate 的总条件额外要求权重不是主要对象，gate 更写成“只有外部 Harness 是明确主要改进对象”。这会错误排除有真实外部技能版本循环的共演化工作。

[具体补丁](coevolution-policy-proposal.patch)只消除这一矛盾，保留外部工件、执行反馈、跨轮次保留和逐字引句要求。固定技能 replay、记忆内容、外部科研产物或两个模型联合训练仍不能据此纳入。StateSkill、SkillForge 与 R²Orch 的正文证据见独立补审；R²Orch 最终零技能部署须与训练中的技能版本演化分开陈述。

`git apply --check` 已通过；没有改生产提示词或既有模型结果。提示词变动会触发有密钥的 `pull_request_target` 自动评测；owner 最新要求先同步完成部分与可续跑清单，本轮不申请付费续跑。后续应用补丁后需重跑45例闸门，旧 precision/recall 不能作为新提示词结果。人工审核和暂停发布的边界仍有效。
