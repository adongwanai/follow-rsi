# RSI-Dojo 独立正文补审

**arxiv:2611.03698：建议仍为exclude，正式决定defer，未授权发布。** 之前仅读完整原始摘要；现补读官方正文方法、采集/评测设置、ablation、行为分析与limitations。

正文中的improved harness是基于观察到的失败模式增加guidance的采集配置；没有描述系统自身生成、验证、接受并继承Harness修订的程序演化链。任务反馈指导目标模型训练，筛选后的轨迹用于agent模型SFT。

原文确有Harness程序与反馈：采集以AutoTrainess的AGENTS.md、skills和hooks为基础，并根据已识别失败模式增加guidance。因此不能以“模型训练为主”或“没有Harness改动”排除。缺少的是系统提出、接受并继承程序修订的版本链。正文描述的是增强前后采集配置对比，筛选出的轨迹用于模型训练；评测时又移除额外采集guidance。

## 可复核原文

- [#S3.SS2.p1.1](https://arxiv.org/html/2611.03698#S3.SS2.p1.1)：The base harness follows AutoTrainess Yu et al. (2026) , which provides task-specific guidance through AGENTS.md , skills , and hooks during the rollout process.
- [#S3.SS2.p1.1](https://arxiv.org/html/2611.03698#S3.SS2.p1.1)：We further augment this harness with additional guidance targeting the identified failure patterns.
- [#S5.SS2.SSS0.Px1.p1.1](https://arxiv.org/html/2611.03698#S5.SS2.SSS0.Px1.p1.1)：We randomly sample 100 trajectories collected with the base harness and 100 trajectories collected after adding our targeted guidance, then analyze their quality.
- [#S4.SS2.p2.1](https://arxiv.org/html/2611.03698#S4.SS2.p2.1)：During evaluation, we do not include the additional guidance introduced for trajectory collection.
- [#S3.SS3.p1.1](https://arxiv.org/html/2611.03698#S3.SS3.p1.1)：The remaining trajectories are then used to train the agent model.
- [#S7.p2.1](https://arxiv.org/html/2611.03698#S7.p2.1)：we do not close the loop by using our trained models to train an improved successor of themselves.
- [#S3.SS1.p2.1](https://arxiv.org/html/2611.03698#S3.SS1.p2.1)：Tasks that pass this execution check are then normalized into a unified evaluation interface, allowing the post-training agent to invoke different tasks through a consistent workflow.

## 边界

- 明确承认外部AGENTS.md/skills/hooks、失败模式驱动guidance增强与跨采集任务使用；不能说没有Harness改动、没有反馈或完全没有持留。
- 不因模型训练是主贡献、Harness是辅助而排除；缺口是系统生成并继承程序修订的演化链。论文we further augment没有明确编辑执行者，不能超出原文断言所有指令都纯手工编写。
- RSI-Craft生成并验证的是post-training benchmark任务环境与统一评测接口；这不单独证明其自身agent执行程序被反馈修订。
- 100+100轨迹对比评估增强前后配置；56% retention rate是轨迹筛选留存率，不是Harness候选接受率。
- 评测移除额外采集guidance，保持standard AutoTrainess配置；不能把采集增强与部署期持续自改混写。
- S7的own-successor未闭合是模型递归边界的补充证据，并非外部Harness排除的唯一理由。
- 只读所列正文方法/边界与结果解释，没有审计代码仓库、配置补丁或复现实验；没有重新批准数值性能结论。

HTML SHA256：`053d4b8806ceeb97d6c39a6dbd3085bc2534d5dee3102f6b0d8b4468f330fcd9`；7条短引句已对原始HTML及paragraphs缓存逐项精确匹配。

本补审不修改冻结主审/S2的来源与范围结论；另按parent明确授权，仅为S2旧选样哈希补充历史快照说明。新增独立S2的唯一ID阅读仍为39/76；正文深度由33升至34项，摘要抽查剩5项，37项仍未独立初筛。未新增范围意见、未付费、未发起网络请求或复现实验。

本稿在读取parent主审补审结论前完成；不预先声明双审一致。
