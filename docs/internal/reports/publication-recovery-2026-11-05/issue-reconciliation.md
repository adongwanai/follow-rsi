# Issue 与历史补登核对：2026-11-05

核对完成时间：2026-11-05T08:36:43.016048+00:00。范围为 `adongwanai/follow-rsi` 的 #40、#30、#23、#22、#20、#19、#18、#16，以及 11 月 2 日晚到的 MemSteer / GEPA-Curator。这个子任务仅写本报告，没有 GitHub 写操作、生产数据修改、付费 API 或扩大抓取。

本次已读取上述 8 条 issue 正文与全部评论：#40 为 0 条，其余每条各 1 条，返回数量与 issue 的 `comments` 数量一致。初读时 8 条均 open。随后主任务实时核实 #39 的合并信息并成功关闭 #40；下表已纳入这一最新操作回执。论文范围、正式审核、质量评测、合并与公开发布分开判断。

## 结论表

| Issue / 当前状态 | 精确解除条件 | 当前证据及是否满足 | 11/03–04 八篇发布的影响 |
|---|---|---|---|
| [#40 Review stalled](https://github.com/adongwanai/follow-rsi/issues/40) / **主任务已关闭** | `scripts/feed/ci.py` 只计算 head 分支匹配 `^feed/review-(\d{4}-\d{2}-\d{2})$` 的 PR；距最近匹配 PR 的 merge 少于 3 个日历日即解除。待审数大于 60 只增加提醒文本，不是关闭闸门。 | **已满足停滞解除条件。** 主任务实时 API 回执：#39 head=`feed/review-2026-11-05`，merged_at=`2026-11-05T07:55:04Z`，owner=`adongwanai`，merge=`6cb8262adfc844ddedcc149e345c22e042b71445`；主任务 `gh issue close --reason completed` 成功。11/05 距 merge 为 0 天。 | 已由 #39 的匹配 merge 解除，与八篇是否接纳或发表无关。关闭含义仅为**停滞提醒解除，非接受/出版**。 |
| [#30 OmniBrain-0](https://github.com/adongwanai/follow-rsi/issues/30) / open | 补真实 reminder-policy 或 rubric 的版本差异及后续调用，区分可复用执行策略工件与固定提醒器里累积的提醒/规则；核对输入身份并重新独立裁决。 | **未满足。** 既有正文已有冻结参数验证、反馈修订及跨轮保留；仍缺具体策略工件差异与消费实例。不能因别处训练权重就排除。Issue 摘要与官方一致；canonical 曾仅漏 `teachers'` 后空格，这不是科学内容变化。 | **不能关闭。** 不在八篇中；全局 gate pass 也不填补工件缺口。 |
| [#23 VEvo-Harness](https://github.com/adongwanai/follow-rsi/issues/23) / open | 一条 skill 的 schema、旧版、patch、新版、双臂反馈与准入结果、后续实际调用；须证明生成策略指令变化。补证后重新独立裁决。 | **未满足。** v1/v2 已对照，主审/独立审查分歧调和仍为 unknown；成功 prompt、记忆、embedding、评分记录不能代替策略工件。当前没有新增原始实例消除缺口。 | **不能关闭。** 不在八篇中，也不能把一方 include 当成共识。 |
| [#22 MetaVul](https://github.com/adongwanai/follow-rsi/issues/22) / open | 完成本条正式审核、现有质量闸门，保留可核验通过记录，并核验实际发布。正式批准必须绑定最终内容 hash。 | **范围证据满足，出版条件未满足。** 官方摘要/正文和独立复审支持 Python Harness 修订、漏洞/修复函数反馈、历史/Pareto 保留和未见数据/模型迁移。当前 canonical 无正式 review、双语摘要或本条 gate；本地 feed 中不存在。 | **不能随八篇关闭。** MetaVul 不属于该八篇包，且当前 `hf_daily_dates=[]`；须另行完成它自己的正式审核和发布，不能虚构 HF 日期。 |
| [#20 MoLRSI](https://github.com/adongwanai/follow-rsi/issues/20) / open | 一个持续使用中的资源 skill 的旧版→执行错误→修订→验收→不同后续任务调用；证明是 Agent 自身 Harness 持久改写。补证后核对身份并重新独立裁决。 | **未满足。** v1/v2 已审；11/05 intake 明确仍为 `scope_evidence_pending`，承认辅助技能修复/验证/保留的正证，但仍缺实测的跨任务技能版本/消费链。首次工具封装、依赖修复、科研 workflow 和经验统计不足以替代。 | **不能关闭。** 虽有 HF 11/04 成员身份，仍不在八篇包中；该成员身份不会解决工件边界。 |
| [#19 KARMA](https://github.com/adongwanai/follow-rsi/issues/19) / open | 一条实际接纳的 role、output-protocol、action-description 或行为指令工件：旧版、补丁、新版、诊断执行反馈、验收结果、后续任务调用。须区分执行策略和广告领域规则；补证后重新独立裁决。 | **未满足。** 保持 `evidence_required`；当前原始来源/报告没有新增实例消除缺口。外围可执行代码冻结本身不能作为排除理由。 | **不能关闭。** 不在八篇中；其他条目通过审核不能替代它的工件证据。 |
| [#18 Video Generation Meets Agent Harness](https://github.com/adongwanai/follow-rsi/issues/18) / open | 依原 issue 处置完成正式逐项审核和真实质量闸门，并核验实际发布；公开分类保持 Harness 专项理论/综述。 | **范围与摘要草稿检查已满足，正式出版条件未满足。** 八篇包含本条，正文决定性依据来自官方 PDF §5.2/§5.3.2；不能冒充摘要引句。当前 canonical `review=null` 且本地 feed 未含本条。作者未证明改进后的开发程序改善后续开发轮次。 | **有条件可关闭。** 本条真实通过正式审核、gate、合并及公开发布核验后，issue 的原条件可满足；仅生成/审过草稿、全局 gate 单独通过或合并 all-defer PR 都不够。最终方向 `primary=theory_survey, harness_sub=null, secondary=[harness]`。 |
| [#16 TinyAstral](https://github.com/adongwanai/follow-rsi/issues/16) / open | 完成本条正式审核、真实质量闸门和可核验实际发布；保留教师 Harness 演化与后续学生蒸馏的阶段边界。 | **范围与摘要草稿检查已满足，正式出版条件未满足。** 八篇包含本条，冻结教师、执行轨迹反馈、工具/恢复逻辑修改、成对统计准入与后续复用已支持纳入。当前 canonical `review=null` 且本地 feed 未含本条。 | **有条件可关闭。** 完成本条正式审核、gate、合并及公开发布核验后可满足原条件；八篇“准备完成”本身不能关闭。方向 `harness/evolve_main`，secondary=`embodied`。 |

七条论文 issue 的最新公开评论仍是 2026-11-03 的处置说明；#16/#18/#22 评论内的“暂停付费调用”和旧 recall 是当时状态，本报告不把它们当成对主任务已获新授权的限制。四条工件边界问题不能仅因证据未找到而强制 accept/reject；应补原始实例并独立重判。

## #40 的合并与发布边界

实现见 `scripts/feed/ci.py:18,173–211`。本地 Git 也印证 #39：merge commit `6cb8262adfc844ddedcc149e345c22e042b71445`，committer time `2026-11-05T15:55:03+08:00`，正文为 `Merge pull request #39 from adongwanai/feed/review-2026-11-05`，标题仍为 `[GATE BELOW THRESHOLD] Review: Follow RSI 2026-11-05`。主任务的实时 `merged_at` 精确到 UTC `07:55:04Z`，以该 API 回执判断 merge 时间。

#40 原正文的 274 是该提醒当时记载的未出版队列数量，本子任务没有重新计算它。自动规则没有检查该 PR 是否包含 accept，也没有要求 backlog 清零或出版八篇；因此 #40 关闭不能用作这些结果的证据。

## 八篇包与当前 gate

八篇的 HF 归属为：11/03 的 `2610.40191, 2611.02102, 2611.03219, 2610.41216`；11/04 的 `2610.39813, 2611.02079, 2610.40747, 2611.04035`。与上述七条论文 issue 的交集只有 #18、#16。

`docs/internal/reports/publication-recovery-2026-11-05/final-editorial-review.json`（08:13:23Z）记录 8 条双语摘要支持、78 个来源/段落/引句/既有审核绑定通过、7 条方向字段原样通过。`2611.03219` 的 `harness_sub` 需从 `generalize` 显式改成 `null`，因为 primary 是 `evaluation_benchmark`；该次审核并未修改原候选包。写本报告时，durable `prepared-candidate-package.json` 仍为 08:00:48Z 快照，8 个 `formal_decision=defer`，且该方向字段仍为 `generalize`。这些都是快照状态；最终准备/集成需落实修正并重新绑定，不能把本报告当成已经落实的回执。

现有生产 `feed/eval/gate-report.json` 的 `generated_at=2026-10-27T13:50:58.824415+00:00`，status=`complete`，Harness precision=0.9600，recall=0.8571（24/28），required recall=0.90，thresholds_passed=`False`。本次真实评测仍在主任务执行；截至本报告写入时，隔离目录中的新 `quality-eval/run-root/feed/eval/gate-report.json` 和 `quality-eval/usage-summary.json` 尚未落盘，不能预判本次结果。

即使新全局报告达标，仍须完成每条实际支持的正式审核路线、最终摘要/分类/证据来源、当前 hash 绑定和发布核验。编辑审核、离线测试和主任务条件性授权不会自动生成缺失的模型 provenance；也不应捏造它们。

## 11 月 2 日晚到两篇：应该补登，但出版审核未齐

| 项目 | MemSteer (`2610.39276`) | GEPA-Curator (`2610.37651`) |
|---|---|---|
| 已完成范围 | 官方 v1 摘要与方法正文主审、独立范围复审，双方 include；HF 11/02 成员身份已验证。 | 官方 v1 摘要与方法正文主审、独立范围复审，双方 include；HF 11/02 成员身份已验证。 |
| 纳入依据 | MemSteer-Opt 改写可复用存储、索引、检索和上下文设计；执行失败诊断驱动提案，验证准确率严格提高才替换；接受后复用，冻结 ATM-Bench 设计转到 RHELM。 | Curator 策展任务/成功轨迹作为外部 prompt 修订证据；更新沿 checkpoint 保留；§5.3 接到 Harness 代码修订、父版本重跑反馈及开发集选优。 |
| 分类与关键边界 | `harness/component`。合成 QA 和记忆条目本身不等于机制演化，不扩张为普遍泛化或同预算优势。 | `harness/evidence_selection`。greedy lineage 每次 mutation 成为下一 checkpoint，周期验证后选最终最好版本，**不是每步单调准入**。Curator 本身固定，不能叫 improver 自进化；全部模型参数冻结保持 unknown。 |
| 当前 canonical | 没有双语摘要、`llm`、`gate` 或正式 `review`。 | 没有双语摘要或正式 `review`；既有自动标签/gate 仍 borderline，`persists_across_tasks=unclear`。该旧结果没有被本次范围意见改写成通过。 |
| 尚缺出版步骤 | 制作并按原文核对最终双语摘要及方向；补实际支持的逐项审核/provenance 路线；完成有效全局 gate；按最终科学/展示内容重算 hash 并正式决定；生成历史补登并核验部署。 | 同左；还须透明调和旧摘要级 borderline 与正文正证，使用管线支持的正式审稿路径/显式方向覆盖，不能伪写成新模型判定。当前 `review/daily/2026-11-05.yaml` 仍 defer 且要求源变更重审。 |
| 建议 | **值得继续做 11/02 历史补登**，目前不能称为逐项出版审核完整或已可直接发布。 | **值得继续做 11/02 历史补登**，目前不能称为逐项出版审核完整或已可直接发布。 |

两份范围报告都明确 `owner_reviewed=false, publication_authorized=false, formal_decision=defer`；11/03 intake 则将二者标为 `scope_review_complete_quality_gate_blocked`。独立报告在全部四篇范围审查中检查 29 条正文引句和 8 份官方 receipt，这些计数不能写成两篇各自的计数。代码实现、实验复现、完整成本/数值审计没有完成；对于不引用结果数字的短摘要，不把全套复现实验凭空增加为出版前置条件，但任何所用数字与比较仍须逐项查证。

HF 11/02 的已保存完整快照包含 38 条，MemSteer 位于 `/21/paper`、GEPA 位于 `/22/paper`；本次重新核实 ID 和快照 hash `07edcacf5b2600542e81b8545732780aad9dcf3e4b333185dc9c5100a734b094`。首次发现日期与 HF 归属日期分别保留：

| ID | 当前 canonical published | 真实 first_seen | hf_daily_dates |
|---|---|---|---|
| `2610.39276` | `2026-10-29` | `2026-11-03T02:44:36.060428+00:00` | `2026-11-02` |
| `2610.37651` | `2026-10-27T17:58:11Z` | `2026-10-29T09:49:30.896103+00:00` | `2026-11-02` |

MemSteer 官方 v1 精确首发为 `2026-10-29T03:28:49Z`，当前 canonical 仍只有日期 `2026-10-29`。本报告未静默改动它；若正式集成时规范化，需纳入变更与 hash 重新绑定。GEPA 首发 `2026-10-27T17:58:11Z` 已保留。

历史补登应继续归入 **2026-11-02**，保留现有三篇与原始归属，不改作 11/03 或 11/05 新推荐。当前本地 `site/daily/2026-11-02.json` 的 published_at 为 `2026-11-03T02:01:03Z`，仅含 `2610.42141, 2610.34722, 2610.22740`；没有这两篇。`site/feed/latest.json` 有 21 条，没有本报告九个候选；本地也没有 11/03 或 11/04 日报 JSON。以上是本地生成物核对，本子任务没有新做公开 Pages 检查，不能据此替代部署核验。

## 证据位置与绑定

- 既有处置原文：`docs/internal/reports/issues-2026-11-02/candidate-resolution-plan.json` / `.md`。最新公开评论：[16](https://github.com/adongwanai/follow-rsi/issues/16#issuecomment-6593670354)、[18](https://github.com/adongwanai/follow-rsi/issues/18#issuecomment-6593674777)、[19](https://github.com/adongwanai/follow-rsi/issues/19#issuecomment-6593675885)、[20](https://github.com/adongwanai/follow-rsi/issues/20#issuecomment-6593677078)、[22](https://github.com/adongwanai/follow-rsi/issues/22#issuecomment-6593680533)、[23](https://github.com/adongwanai/follow-rsi/issues/23#issuecomment-6593681570)、[30](https://github.com/adongwanai/follow-rsi/issues/30#issuecomment-6593692266)。
- 11/03 范围与归属：`docs/internal/reports/maintenance-2026-11-03/late-hf-primary-review.json`、`late-hf-independent-review.json`、`late-hf-reconciliation.json`、`integration.json`；`data/feed/intake/2026-11-03/review-status.json`。
- 11/04–05 对照：`docs/internal/reports/maintenance-2026-11-04/primary-a-review.json`、`primary-b-review.json`、`independent-review.json`；`docs/internal/reports/maintenance-2026-11-05/primary-review.json`、`independent-review.json`、`integration.json`；`data/feed/intake/2026-11-05/review-status.json`。MoLRSI 最新结论仍为待补工件。
- 八篇草稿与编辑终审：`docs/internal/reports/publication-recovery-2026-11-05/prepared-candidate-package.json`、`prepared-validation.json`、`final-editorial-review.json`。质量结果以上节区分历史生产报告与本次独立 run 的状态。
- MemSteer v1 本文缓存 `build/maintenance-primary-2026-11-03/2610.39276v1.body.html`，本次重算 SHA256=`0d8cd88205828a71c5b83e69a324683a91ae551a2493f3099326a4010302d988`；GEPA `2610.37651v1.body.html`，SHA256=`1ee335bb4ef74898a3e7f518fd05d4c3b51a532de3437cef1000c9e9049af8de`，均与独立复审来源相符。

当前 canonical 的 owner-visible source hash 由生产 `scripts.feed.review.source_hash` 只读重算如下。摘要、方向所依赖的自动内容、gate、HF 归属或科学字段变更都可能改变最终 hash，不能直接沿用旧批准。

| arXiv ID | 当前 source_hash |
|---|---|
| `2610.41216` | `4caf34ec78a48265bcc91fd6d55690272763a17fda2e6634fab23f07287a9091` |
| `2610.40191` | `4b311736b7ea2ed2750ae7cf0d4068ef1125c0f7972b94998421f2771ba49fc4` |
| `2610.40721` | `eb5d28faa821e09695aebbe16b9c344b54647d033a91bdc78f9e3f336ec2c18f` |
| `2610.39884` | `0f916641d261a3caccab3ababaf695a9744af139cb783b68579071be17dd6a43` |
| `2610.39714` | `059898632feae463a0194b3b17451eef3d56bfe20d9dd282679128e6da86c14c` |
| `2610.39158` | `b289a03249109d09deaceaaec019748d64f5bbf9c5a354c5a6c01bcc50768fcd` |
| `2610.36013` | `cc505aa56b610887187e56a11f21c897d5c1dbbbf12ba875cdacc2058292a584` |
| `2610.39276` | `5d59b95c1bbe5aaf41d8d3161cacf422d86e6e4631a9c0f8ee0c01a4048bdb97` |
| `2610.37651` | `9933e01e9e4cef966b00ce3b20860bfe8a39d42c38d47aac4eaa333931883a39` |

相对于 11/03 candidate-resolution-plan，#19/#22/#23/#30 的当前 hash 相同；#16/#18/#20 已变更，旧 hash 不是当前输入的正式批准。两篇历史补登也必须绑定完成摘要与必要规范化后的最终值。
