# 第三轮独立复核后的更正与未决边界

最终可供 owner 审核的建议为 **5 篇 Harness（3 篇方法、2 篇专项安全评测）、2 篇边界待审、30 篇本轮不纳入 Harness**。全部正式决定仍为 `defer`，没有任何发布授权。这不等于 10 月 31 日 HF 有 5 篇：该日榜快照为成功空列表；23 篇 HF 迟到条目仍属于 10 月 30 日，其余为非 HF 新发现附录。

原始初审与独立审查都保留：

- [第 1、2 轮初审](review-results.json)
- [独立第 3 轮冻结结果](../independent/frozen-findings.json)
- [合并复核建议与逐项证据](review-reconciled.json)
- [核验记录](verification.json)

两个审查结果在比对前独立记录。归一化为 Harness 准入建议后，初始 36/37 项一致；唯一分歧为 KARMA。以下更正基于正文与图示，未覆盖初审或独立冻结结果。

## KARMA：把接口能力误写成实际发生的改动

初审把“接口支持修改 role、output_protocol、action_descriptions”写成了这些字段已经实际修改，超过已检查证据。正文第 134 段还特别区分 proposal 的预期修改与 mutation journal 的实际修改；第 147 段明确已接受周期添加的是 decision rules。

重新目视核对 [官方 Figure 5](https://arxiv.org/html/2610.39884v1/figures/CaseStudy.png) 后，accepted E17、E18、E19 全部标为 `experience`。尚未找到已接受角色或协议修改的实证补丁，不能仅凭“放进系统提示”跳过 owner 对规则手册的排除边界。

因此将初审的 `harness/component` 改为 `borderline`，主要已展示对象为 `experience_world_model`，保留可能涉及提示组件的正证据。需要 owner 解释边界或提供实际 mutation journal；不以代码冻结作为机械排除理由，不强行纳入或发布。

## SkillCompiler：补充开发阶段的留出数据接触

第 131 段明确写出开发阶段检查过 held-out failure cases，同时报告的 frozen-bank 评估禁止从测试结果持久更新。两者同时记录，不能由后者推断完全独立留出。其 Harness 方法建议不变，held-out 等未逐项审核字段继续 `unknown`。

## 仍需 owner 决定

- KARMA：经验规则与提示/协议组件之间的边界，尚缺已接受程序性字段修改实例。
- MoLRSI：有辅助技能执行修复的正证据，但主要实验隔离的是历史经验；不能把外部科学工作流改进直接算作 Harness 改进。
- A-RSI：明确不是 Harness；其固定模板/控制器下的多窗口权重训练是否达到广义 RSI 门槛，仍保留原初审的 broad-RSI borderline，不计为第三个 Harness 边界。

本轮仅阅读官方摘要、选定正文段落与 KARMA Figure 5；没有复现实验，也没有审定论文数值声明。未修改 canonical feed、论文原始数字或 owner 决定。
