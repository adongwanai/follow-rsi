# 432 条历史模型意见的本轮逐项复核

本表区分范围建议、来源绑定和正式决定；不把本地复核报告称为论文出版。

- 冻结输入与主审：432 / 432；原始身份绑定 432 / 432。
- 最终范围建议：{"exclude": 413, "include": 12, "borderline": 7}。
- 正文补读主审：24 个 ID；独立逐项复审：46 个 ID。
- 初始非排除项 25 个，全部独立复审；其余排除复审为抽样，386 个没有逐项独立复读。
- 未解决意见分歧：0；待定范围不计为未阅读。
- 验证了全部引句、冻结来源哈希、正文补读章节哈希，以及 52 份官方原始 HTML 与重提取正文。
- 来源身份补取 9 个均成功；其中一项封面日期与首次上线日期不同、一项旧博客别名关系未证实，逐项保留而未改原始日期或别名。

## 已读后的边界待补

| ID | 题名 | 结论 |
|---|---|---|
| post:https://openai.com/index/terminal-x | Terminal X matches senior investor judgment 88.6% with GPT-6.1 | 官方全文明确失败会变成 workflow instruction/test case，亦明确 engineers 把 Memory 变成 workflow；未交代自动修订/激活机制与准入。保留可能 Harness 的边界，不能从营销的 learning 直接认定自动进化。 |
| arxiv:2610.06274 | What May an Agent Change About Itself? A Containment Floor for Self-Configuring Agent Runtimes | Containment Floor 检查 Agent 通过自身配置工具写持久 manifest 扩权的安全边界；配置下次启动生效，是真外部控制工件，但实验由普通配置请求触发，固定六规则无性能反馈演化，meta-agent 部分明确仅设计论证。可相关安全阅读，暂不称完整 Harness RSI 专项实验。 |
| arxiv:2610.07376 | MemCo: Memory-Centric Collaboration for Generalizing LLM Agents to Unseen Environments | MemCo 的 typed global memory 含行为顺序、前置条件和修复规则，按各 episode 执行证据晋级/删除并跨任务复用，再渲染为当前动作指导，不能当纯事实记忆。但存取/门槛/渲染机制固定，变的是结构化记忆内容而非独立版本控制程序；暂保程序性记忆与 Harness 技能边界，交 root 按当前专题口径裁定。 |
| arxiv:2610.15788 | Agent Sociodrama: Social-Dynamics-Guided Persona Recasting for LLM Agent Teams | TPR 的角色重分配是根据多轮真实交互反馈调整的持久 casting，不能说只有情绪状态变化；但正文仍固定同一任务情景/私有知识，反复测同一情景，未见跨独立任务保留或迁移。维持待补，不将循环存在直接当成 Harness 核心证据。 |
| arxiv:2610.21412 | JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs | JevAgentHarness 从真实 shadow-mode 任务轨迹拟合持久路由阈值、固定脚本选组合后新任务测试，不能说纯权重工作；但外部机制是预设统计校准，未见反复修改规则/提示/程序的闭环。暂待 core 口径裁定，SFT/GRPO 分列。 |
| arxiv:2610.22319 | A team of Gemini 4 Argon agents beats Minecraft | 正文新增明确正证：自建 helper 与修复在后续数百程序被多 agent 调用；不是仅临时任务代码。但仅一个 Minecraft 运行内跨子任务持留，不能声称跨独立任务的 Harness 继承。按 root 裁定保留边界待补。 |
| arxiv:2610.28914 | D-Skill: Distilling Teacher Knowledge through Agent Skills | 离线 teacher/student 轨迹差异会生成可复用的 SKILL.md 行为规则，并按 chunk 修改保留；主方法明确不再次调用执行环境或评估，因此不能称递归在线自进化。另接 SkillOpt 后端保留验证门，可视作改进器输入组件；是否仅此窄范围收录交由主审核协调，不因自然语言技能或离线处理本身排除。 |

## 证据与行为边界

- 432 条均有逐项来源范围意见；这不是 432 条全部通过完整出版审核。
- 第三轮覆盖所有初始非排除项和追加的分层负例；未逐条独立复核的排除项单独计数，不冒称全部三人复核。
- 已完整阅读但仍有程序性记忆、固定校准、单次运行继承等边界的条目列为已读待裁，不算未处理。
- 来源哈希来自初始冻结输入；若主任务后来改摘要等 owner-visible 字段，须保留此意见链并另做准确内容绑定。
- 官方正文机制引用仅证明所述范围与版本协议，没有复算论文全部实验数字或重跑实验。
- 本报告不修改 formal review、不接受、不拒绝、不发布内容；最终正式决定和线上核验由主任务负责。
