# 2026-11-02：73 条历史来源与元数据差异对账

73 条均已形成来源绑定的范围建议或明确的判据边界：**建议纳入 43、建议排除 28、范围待定 2**。本轮未处理项 0、外部来源阻塞 0；73 条仍待人工审核，正式 `decision` 全为 `defer`，没有接受、合并或发布内容。

64 条在显式对齐摘要、元数据和版本后复用旧范围建议；9 条重新阅读正文指定段落，其中 7 条改变推荐、2 条纠正排除理由但保留原推荐。两条范围待定是已完成检查后的判据问题，不是用统一 `defer` 遮蔽未处理项。

## 范围建议与数字审计分别记录

- 本轮核对 72 个官方 arXiv 条目与 1 个出版商摘要，验证 260 个历史来源文件的哈希和 517 段历史引句。
- 取回 44 篇元数据版本不一致的固定 v1 正文，另补取 CUAWright v1 正文与 EngramBench v1 PDF；共 46 份正文、47 份原始响应。逐篇保留版本差异，44 段旧版支持引句与 31 段新增范围引句均通过连续原文匹配。
- **范围可复用不等于整篇等同，也不等于实验数字重新认证。** 每条 `numerical_audit_status` 均为 `not_recertified_scope_only`；所有跨版本记录的 `numerical_claims_reusable_across_versions` 均为 `false`。本轮没有逐表复查或独立复现实验，不能把本次对账用于升级任何旧数值审计状态。
- canonical 数据及旧审核报告保持原样；现有 73 条 canonical source hash 与任务开始的 baseline 一致。新结论只写入本目录，来源与脚本留在对应 build 目录。

## 9 条正文复核

| 条目 | 旧建议 → 本次建议 | 主要依据与边界 |
| --- | --- | --- |
| Verification and Self-Improvement · 2610.10611 | exclude → exclude | 第 8 节与附录 D 是一般 RSI 验证理论，覆盖权重、提示、工具、记忆；Harness 是映射案例。修正理由：不能要求专项评测/理论自己执行更新循环。 |
| Mining Design Space · 2610.31709 | exclude → include | 专门分析 AFlow 分数反馈下演化的 `graph.py` / `prompt.py`，保留搜索轨迹并按整条搜索留出；属于 Harness 专项评测。 |
| Agentic Self-Awareness · 2610.19226 | defer → include | 正文中的 HarnessX 固定模型、按评价记录改提示/处理器/控制流并跨轮保留。仅其干预评测组件纳入，一般 ASA 基准不自动纳入。 |
| CUAWright · 2610.04116 | defer → exclude | 官方正文说明任务内文件与工具跨交互步骤持续存在，未建立后续任务或独立改进轮次的 Harness 版本留存。 |
| EngramBench · 2609.39284 | defer → include | 官方 PDF 将有执行反馈的历史蒸馏为程序性 SKILL.md，冻结后在隔离新项目复用；属于专项迁移评测，不能称为在线自改方法。 |
| OptiCom · 2609.37221 | defer → include | 附录 D.4 的外部策略模板/算子偏好更新带支持结果和版本，随后 Action Package 使用该版本；仅改进器控制组件纳入，不主张跨任务迁移或单调提升。 |
| Learner2Skill · 2609.37157 | include → exclude | 确有共享 SKILL.md 反馈校准，但主产物是学习者响应模拟器；按当前 taxonomy 归为 `data_task / training_env_reward`。不能误称为仅存记忆。 |
| EvoSteer · 2609.38661 | defer → include | 结构化执行技能经评分轨迹提出、配对反馈晋升/退役、checkpoint 留存且测试冻结复用；按 owner 的协同更新例外纳入技能组件，明确同时训练 LoRA。 |
| Your Policy Is Secretly a Harness · 2610.37255 | exclude → exclude | 研究固定接口下的策略训练/迁移，不是反馈驱动 Harness 候选演化的专项理论。更正排除理由，保留相关理论链接价值。 |

逐条的章节、可核验引句、源 URL、正文哈希和限制见 `new-scope-reviews.jsonl` 与 `findings.json`。

## 两条明确待定

- **ECG-RSI · 2610.17718：** v1/v2 正文已取得；需由 owner 判断可版本化的数据构造 operator/prompt/skill 属于 improver 自身控制程序，还是 `training_env_reward` 主产物。不能只因存在权重训练就排除。
- **OmniBrain-0 · 2610.36013：** 现有文字能证明 reminder 被保留，但尚需实际策略文件、版本差异与跨轮调用证据区分“修改可复用策略程序”和“累积提醒内容”。来源不是当前阻塞；本轮保留范围待定。

## 发现但未覆写的数据问题

1. **ASA 来源包不等于历史模型输入。** 旧审核 bundle 的哈希只对应“官方摘要 + 换行”；随后 provenance 才附上正文 receipt。两种 payload 和哈希分别保留，本轮另外读正文，不倒推旧审核已读全文。
2. **EngramBench 旧 `body_acquired` 不成立为有效正文阅读。** 旧正文只有 35 字符 LaTeX 宏。已改从固定 v1 官方 PDF 补证，共 19 页、59,825 字符；旧 receipt 原样保留并标记问题。
3. **版本与时间精度差异。** canonical 常保留 v1，而旧审核取了 v2/v3/v4；首次发表日的午夜值与官方精确时间也有差异。只报告，不直接改写论文元数据。
4. **SkillMarker 摘要有实质新增结果。** v2 新增结果句及数字，不能将差异统称为空格排版；仍属水印/所有权方向，不复制新数字到 v1。
5. **正文修订不止摘要。** What Does a Harness Repair、ROI、The Last EO Model、Scale and Selection 等有明显正文/实验扩充。保留旧版支持当前范围的引句，同时明确不跨版迁移结果或新增机制。

## 文件与聚合字段

- `findings.json`：顶层 `records` 为 73 条，按输入原顺序；`summary` 为聚合数量。
- `records[].current_suggestion.recommendation`：`include / exclude / defer`，只表示范围建议。
- `records[].source_advice_disposition`：`reuse_after_source_reconciliation` 64、`changed_after_fresh_review` 7、`fresh_rationale_correction_same_recommendation` 2。
- `records[].reconciliation_status`：`reusable_with_explicit_reconciliation` 64、`reconciled_with_fresh_scope_review` 9。
- `records[].processing_state`：71 条 `completed_advice`、2 条 `completed_with_explicit_scope_boundary`。
- `canonical_source_hash` 绑定当前完整记录；摘要哈希、历史模型 bundle 与现存 receipt bundle 分开存储。
- `metadata_changes`、`abstract_changes`、`version_reconciliation` 说明差异；`verified_historical_citations`、`current_source_quotes` 为旧/新引句。
- `source-provenance.json`：原始摘要、历史来源收据与文件哈希；`new-scope-reviews.jsonl`：9 条新范围复核。
- `validation.json`：本轮完整性校验结果；`package-hashes.json`：交付文件与复核脚本哈希。

## 验证

`build/maintenance-2026-11-02/metadata-reconciliation/validate.py` 已通过：73 个唯一 ID 恰好覆盖输入、73 个 live canonical hash 不变、所有历史/新增引句匹配、260 个历史来源文件与 46 份新增正文哈希相符、ASA payload 差异可重建、Engram PDF 身份与 19 页提取可核对。上一批 primary-a 的 82 条报告 SHA256 仍为 `8613d1d38ce0bdc7be782e7da34a0bcfb0d749ca7e4782a37c2184113adf19eb`。

本批 `findings.json` SHA256：`68669f5ca6954bc48966924add4ec84f5b0d752edecde8f48f72b156a910b21f`。

此子任务仅做证据文件校验；仓库测试、构建和第三轮独立审查由主线程汇总。任何本轮建议均不替代人工批准。
