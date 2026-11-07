# 2026-11-04 历史积压对账

冻结规范表基线为 **1,351** 个稳定 ID。主任务后续新增采集与规范化单列；本报告不修改 canonical/review/state/site，也没有调用付费模型。

## 原始快照并不等于待审新闻

原始来源、旧发现、规范表及待审清单按稳定 ID 合并后共有 **8,280** 项。非规范库的 **6,929** 项现已拆清：

|分类|数量|处置|
|---|---:|---|
|每个已保存来源时间窗之外|6,292|原始归档保留，不算漏处理新闻|
|S2 无可纳入的发表日期|441|按现有采集器规则留原始诊断；不猜日期|
|旧 HF 完整榜单未入库成员|196|逐项补范围初筛：196 exclude 建议|

196 条都是有效格式的 `arxiv:<id>`；与规范表 ID、arxiv_id、alias及规范化同名比对为0映射，未把 S2 paperId/DOI/release ID 冒充 arXiv。它们的 HF 推荐归期实际为 10/14–10/26，不能包装成今天新闻。34个易混淆项复读完整摘要，其余162逐项阅读摘要方法段；**不声称196篇完成全文或三轮审核**。独立 reviewer 另抽查边界与随机排除项。

旧 HF 快照缺实际抓取时间回执。新记录以本轮发现时间作为 first_seen，旧实际 first_seen 保持 unknown；原推荐日、原摘要和每个快照 SHA256 均保留在 `data/feed/intake/2026-11-04/historical-hf-*`。

## 规范库的阶段状态

- 已发布 feed：21项，与21条正式 accept逐ID对应；原始发表日字段不当作发布状态。
- 11/02原始范围回执682项：include235、exclude398、待证49。保留AdaPRA后续纠正后，有效include234、exclude398、待证49、defer1。
- 除已发布或已有catalog记录，有范围批准但缺双语摘要187项；摘要已齐但待正式审核/质量闸门41项。
- 426项已有模型建议，但缺当前判据下的三轮复核；不是全未处理，也不是已通过审核。
- 其余来源意见、历史付费失败、待补证与正式非接受状态按ID记录，任务可重叠。当前有条件授权继续适用，缺证据、摘要或质量闸门不伪装成需要重新征求人审许可。

|互斥状态|数量|
|---|---:|
|`existing_catalog_record_no_new_publication_claim`|96|
|`owner_scope_exclusion_recorded`|398|
|`historical_model_advice_only`|384|
|`historical_hf_scope_exclusion_suggested`|196|
|`historical_formal_nonaccept_retained`|16|
|`scope_approved_missing_bilingual_summary`|187|
|`scope_approved_summary_present_wait_formal_gate`|41|
|`owner_evidence_required`|49|
|`historical_stage_work_remaining`|37|
|`published_reviewed_feed`|21|
|`later_source_advice_pending_owner`|22|
|`historical_protected_owner_correction`|1|
|`source_advice_pending_owner`|29|
|`post_approval_evidence_correction`|1|
|`historical_official_body_model_advice`|42|
|`historical_current_three_round_advice`|18|
|`historical_independent_source_scope_advice_owner_pending`|9|

## 来源复用与发布闸门

范围回执680项source hash严格一致，2项有可追溯的日期/链接元数据漂移：R²Orch修正backfill标记；GEPA-Curator追加HF11/02归期与来源链接。论文标题、摘要、版本等未因这两项被本轮改写。旧恢复计划1300条保护条件中1193全部一致、103仅review改变、4涉及source hash；不能重放旧review覆盖后续决定。

- 质量issue：#16 TinyAstral、#18 Video Generation Meets Agent Harness、#22 MetaVul；另有11/03的3个正例建议也等待正式闸门，不混淆issue数与候选数。
- 工件证据issue：#19 KARMA、#20 MoLRSI、#23 VEvo-Harness、#30 OmniBrain-0。
- 最近完整真实评测（10/30，45/45）：precision24/26=0.9231，recall24/28=0.8571，召回仍低于0.90。本轮没重跑；旧10/27报告precision0.96属于不同轮次。
- 历史HTTP402不当作本次余额实测；本轮无付费调用。GitHub PR/issue/工作流的实时状态由主任务核验。

四篇指定内容仍正确：RSIHub、HarnessDev为harness_eval；HarnessDev必读；Aspire、S3Gym为general_rsi。实验设计路线保持Rethinking→HDA→HarnessDev→RSIHub。

## 校验

原始108个来源快照全部完成本地解析，0解析错误（Sakana相对链接使用注册的feed URL解析）。本轮没有联网重抓历史响应。全部8,280 ID唯一、状态分区加总一致；各项来源与可续跑任务见JSON。raw-only使用`source_snapshot_indices`引用顶层路径索引，降低重复体积。新增报告/intake文件通过JSON、来源哈希、摘录子串和条目计数校验；pytest/build由主任务统一执行。

## 本轮整合完成后

主任务的 [integration.json](integration.json) 已将本次51个新发现与196个旧HF补筛条目加入规范表：**1,351→1,598**，另补记2个已知条目的HF推荐归期。完整并集随今日新源变为8,331；剩余源快照独有6,733项恰为6,292时间窗外与441无可用S2日期。196的逐项建议见 [historical-hf-review-status.json](../../../../data/feed/intake/2026-11-04/historical-hf-review-status.json)。本报告前文与JSON的基线计数保持冻结；规范入库不等于三轮审核或公开发布。
