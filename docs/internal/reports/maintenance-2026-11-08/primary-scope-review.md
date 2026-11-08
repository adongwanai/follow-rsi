# 2026-11-08 新候选主审

19 个新身份：{'include_candidate': 2, 'borderline_or_potential': 4, 'exclude_suggestions': 13}。正式 decision 全未接受；状态逐项区分已核对、正文待补、外部身份待补。5 篇已读方法正文，其余排除建议以摘要为依据。

| ID | 建议 | 主审状态 | 理由 |
|---|---|---|---|
| arxiv:2611.07319 | exclude_from_harness | reviewed_fulltext | 原文明确 editor code 与 LLM 固定，循环更新的是科学预测器参数；不是改进器代码或外部 Harness 工件自身演化。 |
| arxiv:2611.07624 | potential_harness_evaluation | abstract_screen_needs_fulltext | 官方摘要明确比较四种 Harness 演化方法并修改 EvoAudit 的 select/analyze/mutate/gate；是优先候选，但主审未读实验正文，暂不能接受。 |
| arxiv:2611.07372 | include_harness_tool_component | reviewed_fulltext | 仅将反馈迭代、跨任务复用的工具访问层/程序归为 Harness component：§2 新工具端点，§4.1 排序/测试程序，§4.4 原环境叠加优化工具对照。一般环境数据与目录重排不计入 Harness；作者固定 runner 不等于工具工件固定。 |
| arxiv:2611.07123 | borderline_judge_prompt_loop | abstract_screen_needs_fulltext | 持久迭代 judge prompt 明确，但需正文确认是否构成 Agent/Harness 环内验证或改进机制，不能仅因 GEPA 或提示优化字样收录。 |
| arxiv:2611.07054 | exclude_from_harness | reviewed_official_abstract | 固定临床文本筛查与输出草稿应用；无依据说明根据执行反馈改写并跨任务保留 Harness。 |
| arxiv:2611.05454 | exclude_from_harness | reviewed_official_abstract | 提出行为合同与发布治理工程方法，示例为构造的工作流；摘要未呈现系统自迭代修改 Harness 的实证。 |
| s2:563e7283598c54f4ade87b809f84eb885f8e18ed | exclude_from_harness_pending_identity | source_metadata_screen_only | S2 摘要为本体学习挑战提交，不见 Harness RSI 闭环；身份和日期尚未用作者/出版社正文复核，必须保留来源待补。 |
| arxiv:2611.08321 | exclude_from_harness | reviewed_official_abstract | 当前请求生成和测试设备 connector/UI 属任务产物；摘要把 connector reuse 列为未来工作，不能算已实现跨任务 Harness 演化。 |
| arxiv:2611.07329 | exclude_from_harness | reviewed_official_abstract | 固定 backbone/prompt/grader 下的长视频 QA 归因审计，不是 Harness 自改进方法或专项评测。 |
| arxiv:2611.07554 | exclude_from_harness | reviewed_official_abstract | 评测记忆内容的跨会话过度泛化风险；没有证据显示修改记忆管理机制或外部可执行技能工件。 |
| arxiv:2611.07595 | borderline_gene_assets | abstract_screen_needs_fulltext | Gene assets 可持久复用且有 feedback-guided evolution；需正文区分被修改的是可执行技能/管理策略还是经验内容，不能只按记忆标签排除。 |
| arxiv:2611.08318 | include_harness_specialized_evaluation | reviewed_fulltext | §3.1 冻结 actor/原语/感知/评分，仅按回合证据迭代 callable skills + memory 库并退化回退；§4.3 跨任务/跨基准复用库，属于外部技能 Harness 专项评测，可标 secondary harness + embodied。 |
| arxiv:2611.07683 | borderline_skill_policy_coevolution | abstract_screen_needs_fulltext | 摘要同时有 intent-specific skill updates 和 policy optimization；需要原文区分可复用外部技能更新与训练参数更新，不能因权重训练而先排除。 |
| arxiv:2611.08452 | exclude_from_harness | reviewed_official_abstract | 保留的是实验复现研究产物（代码库、环境、launcher、guide），不是 Agent 自身的 Harness 演化；不能因后续研究任务可复用而混算。 |
| arxiv:2611.06543 | exclude_from_harness | reviewed_official_abstract | 过程 rubric 是策略训练的 privileged supervision，目标是 GRPO/RL 权重；没有独立外部 Harness 工件迭代证据。 |
| arxiv:2611.06500 | exclude_from_harness | reviewed_fulltext | 训练神经压缩器的 LoRA/adapter；推理期固定组件压缩工具观测，无反馈改写 Harness 工件闭环。详见独立原文绑定主审报告。 |
| arxiv:2611.06863 | exclude_from_harness | reviewed_official_abstract | 固定模板和冻结模型对同一失败场景重试，不将更新后的 Harness 保留到后续任务；是机器人代码自修复评测。 |
| arxiv:2611.05551 | exclude_from_harness | reviewed_official_abstract | 固定临床工作流选择已有 procedural corpus，不见反馈驱动的可复用 Harness 工件演化；不能因题名有 Harness 收录。 |
| arxiv:2611.05450 | exclude_from_harness | reviewed_fulltext | 固定 Hermes 记忆/技能接口，评估结构与规则经验内容的更新/保留；本轮正文证据不足以将它标为 Harness 管理机制或可执行工件演化评测。 |

所有引句均对本地原始来源做规范空白后精确匹配；出处 URL、body_sha256 和规范 source_hash 见 JSON。第三轮独立意见须由 root 整合，不能把本报告直接当发布许可。

0 付费调用；0 生产修改。

## 已完成交接后的团队结论

原始主审快照保留，个人阅读边界仍为 5 篇正文。独立审查与 root 另完成 Beneath、PromptOps、ReferClaw、Evolver 的正文复核，当前团队共 5 项建议纳入、12 项建议排除、1 项边界待补（Evolver）、1 项官方身份待补（ELLMO）。这四篇不计作本主审个人新增正文阅读。

逐项当前意见见 JSON 的 `current_team_resolution`；正式接受和发布由 root 另行处理。

- 独立报告：`independent-review.json`，SHA-256 `f3707fb1c5c62a472d02727689a319489526359b4edd60659736ed5227647763`。
- root 复审：`root-scope-cross-review.json`，SHA-256 `5acac0c1c59b2ad8ce6fc2ae2672f0dd1e0de5e094147faedc56d57f66f7a560`。
