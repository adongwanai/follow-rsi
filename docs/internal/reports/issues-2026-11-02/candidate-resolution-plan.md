# 2026-11-02 候选 issue 处置计划

生成时间：2026-11-03T02:02:20.911486+00:00。复用已完成的一手来源和独立审核；本计划没有重新读论文、付费调用、GitHub 写入或修改生产数据。

15 条均有下一步：**5 条范围关闭就绪、3 条等部署验证、3 条等正式质量闸门、4 条待工件证据**。5 条中 #21/#24 原先缺回执，主任务现已补入并通过 hash 核对。GitHub 最后只读检查时全部仍为 OPEN。

| Issue | 论文 | 范围意见 | 处置 |
| --- | --- | --- | --- |
| [#16](https://github.com/adongwanai/follow-rsi/issues/16) | TinyAstral | include | 范围正例，正式发布闸门未通过 |
| [#17](https://github.com/adongwanai/follow-rsi/issues/17) | WeGenEvoStudio / WeGenEditBench | exclude | 可按范围排除关闭 |
| [#18](https://github.com/adongwanai/follow-rsi/issues/18) | Video Generation Meets Agent Harness | include | 范围正例，正式发布闸门未通过 |
| [#19](https://github.com/adongwanai/follow-rsi/issues/19) | KARMA | unknown | 边界项，待具体工件证据 |
| [#20](https://github.com/adongwanai/follow-rsi/issues/20) | MoLRSI | unknown | 边界项，待具体工件证据 |
| [#21](https://github.com/adongwanai/follow-rsi/issues/21) | RecRSI | exclude | 回执遗漏已本地修复，可按范围排除关闭 |
| [#22](https://github.com/adongwanai/follow-rsi/issues/22) | MetaVul | include | 范围正例，正式发布闸门未通过 |
| [#23](https://github.com/adongwanai/follow-rsi/issues/23) | VEvo-Harness | unknown | 边界项，待具体工件证据 |
| [#24](https://github.com/adongwanai/follow-rsi/issues/24) | From Grind to Grasp | exclude | 回执遗漏已本地修复，可按范围排除关闭 |
| [#25](https://github.com/adongwanai/follow-rsi/issues/25) | SceneEvolve | include | 本地完成，待实际部署验证 |
| [#26](https://github.com/adongwanai/follow-rsi/issues/26) | RuHarness | include | 本地完成，待实际部署验证 |
| [#27](https://github.com/adongwanai/follow-rsi/issues/27) | Training for Alignment | exclude | 可按范围排除关闭 |
| [#28](https://github.com/adongwanai/follow-rsi/issues/28) | The Trinity | include | 本地完成，待实际部署验证 |
| [#29](https://github.com/adongwanai/follow-rsi/issues/29) | Work Agents | exclude | 可按范围排除关闭 |
| [#30](https://github.com/adongwanai/follow-rsi/issues/30) | OmniBrain-0 | unknown | 边界项，待具体工件证据 |

## 关闭与发布的边界

#17/#27 的官方来源与独立复审已完成，可以按当前 Harness 范围排除解决候选 issue；不产生 accepted 内容，故不必先运行正例发布闸门。#29 复用已有匹配输入的排除意见及 owner 回执。#21/#24 还需保留本次遗漏修复记录；目前该本地前提已验证满足。

正例 #16/#18/#22 不能因来源复审结束就关闭：目前没有正式质量闸门通过记录，付费调用仍暂停。#18 是 Harness 专项理论/综述，决定性证据来自 PDF，不能冒充摘要引句或写成新方法。

#25/#26 已本地生成历史候选卡片；#28 已按 HF 10/28 恢复本地日报。三项都要实际部署核验后才按 completed 关闭。最后记录的公网检查只见 10/27 日报；它是旧快照，不表示报告生成时已重新检查。

## #21 / #24 回执遗漏修复证明

当前回执为 `review/approvals/2026-11-02.yaml`，计数从 include 235 / exclude 396 / evidence_required 49 变为 **235 / 398 / 49**。保留原 owner 审核时间与 post_approval_corrections；没有新增 accept。以下精确行已由主任务落入本地回执，本计划只核对：

### #21

当前 canonical hash = 已审输入 hash：`b487368b6e5041740927cb95daa33fc8069d59ca69803874c05333c5bd9b5eba`。

证明文件：`docs/internal/reports/maintenance-2026-11-01/independent/input-manifest.json`；文件 SHA256：`600f0daf326bfe0632f1b11756c23dcc5bff15a9dfbd3ebf6b7b06cda0479754`。

```yaml
id: arxiv:2610.39352
source_hash: b487368b6e5041740927cb95daa33fc8069d59ca69803874c05333c5bd9b5eba
scope_recommendation: exclude
scope_decision: rejected_from_harness_scope
disposition: verified_historical_source_opinion
evidence_report: docs/internal/reports/maintenance-2026-11-01/primary/reconciliation.json
reason_zh: 修改推荐模型架构、损失、采样器及训练配方，探针反馈筛选外部训练算法；未修改推荐研究 Agent 自己的可复用推理 Harness。
pending_evidence_zh: null
```

### #24

当前 canonical hash = 已审输入 hash：`bf8f2be86f4de5ed33523a1f24f7444cc672dccdf18be3fdcffef51d457384f5`。

证明文件：`docs/internal/reports/maintenance-2026-10-31/owner-candidates.yaml`；文件 SHA256：`1bd9fe5be0a012cc275dea8b44f301485f22aa19a77d510cb426a59428b75c0e`。

```yaml
id: arxiv:2610.38728
source_hash: bf8f2be86f4de5ed33523a1f24f7444cc672dccdf18be3fdcffef51d457384f5
scope_recommendation: exclude
scope_decision: rejected_from_harness_scope
disposition: verified_historical_source_opinion
evidence_report: docs/internal/reports/maintenance-2026-10-31/primary/review-reconciled.json
reason_zh: 研究工作量、信息、个人与集体递归改进的广义理论，非专门研究 Harness 程序演化。范围排除不以理论论文没有运行闭环为理由。
pending_evidence_zh: null
```

## 逐项评论草稿与完成条件

以下是待发送草稿，不代表已发送。带“部署后”的草稿只有实际核验公开页面后才能使用。

### #16 · TinyAstral

处置：范围正例，正式发布闸门未通过。完成条件：完成新条目的正式审核和现有质量闸门，保留可核验通过记录，再核验实际发布；本报告不代替闸门，不恢复付费调用。

评论草稿：

已完成官方来源核验及独立范围复审，建议作为 Harness 方法候选：冻结教师模型后，利用执行轨迹提出工具和恢复逻辑等改动，经成对检验后保留；后续学生蒸馏是独立阶段，不能混成同一模型的提升。

当前还没有本条正式质量闸门通过记录，暂不写 accept、不宣称发布，保留 issue。下一步是完成正式审核与闸门并核验实际发布目标；现阶段不恢复付费调用。

原文：https://arxiv.org/abs/2610.41216

证据记录：`docs/internal/reports/issues-2026-11-02/new-source-findings.json`；`docs/internal/reports/issues-2026-11-02/new-candidates-independent.json`。

### #17 · WeGenEvoStudio / WeGenEditBench

处置：可按范围排除关闭。完成条件：提交并保留本次来源范围裁决和回执修复记录后，可按 not_planned 关闭候选；范围排除不需要生成 accept 或日报发布证明。

评论草稿：

已完成官方摘要、正文及独立范围复审。WeGenEvoStudio 将失败诊断转成训练数据处方和监督参数更新；正文明确写道 “supervised parameter updates”，并训练 LoRA 适配器。没有发现其依据反馈修改、验证并跨任务保留自身 Harness 程序的证据。

建议按“不纳入当前 Harness 专题”关闭本候选，保留为模型改进方向线索。这里关闭的是范围问题，不代表正式 accept、Harness 论文发布或对通用 RSI 价值的否定；以后出现新的 Harness 工件证据可以重开。

原文：https://arxiv.org/abs/2610.41210

证据记录：`docs/internal/reports/issues-2026-11-02/new-source-findings.json`；`docs/internal/reports/issues-2026-11-02/new-candidates-independent.json`。

### #18 · Video Generation Meets Agent Harness

处置：范围正例，正式发布闸门未通过。完成条件：完成新条目的正式审核和现有质量闸门，保留可核验通过记录，再核验实际发布；本报告不代替闸门，不恢复付费调用。

评论草稿：

已完成官方来源和独立复审，建议归入 Harness 专项理论/综述（harness_eval / theory_survey），不能标为新的自进化方法。决定性依据在官方 PDF §5.2、§5.3.2：讨论跨任务保留的开发流程修订、预算匹配及冻结后的独立评估。作者同时明确尚未证明修改后的开发程序能改善后续开发轮次。

此项仍缺正式质量闸门通过记录；摘要混合产物、状态、权重与程序更新，不能拿 PDF 引句冒充摘要引句。保留 issue，等待依现有规则补足正式审核，暂不 accept 或发布，不恢复付费调用。

原文：https://arxiv.org/abs/2610.40191

证据记录：`docs/internal/reports/issues-2026-11-02/new-source-findings.json`；`docs/internal/reports/issues-2026-11-02/new-candidates-independent.json`。

### #19 · KARMA

处置：边界项，待具体工件证据。完成条件：补足上述原始工件与后续调用证据，复核输入身份并重新独立裁决；不能仅因当前资料缺失就强制 accept/reject。

最小原始补证：一条实际接纳的 role、output protocol 或 action-description / 行为指令工件：旧版、补丁、新版、诊断执行反馈、验证接纳结果及后续任务调用。该实例须能区分可复用执行策略与广告领域知识规则；外围代码冻结本身不能作为排除理由。

评论草稿：

已完成已有原文和范围意见的对照，目前仍有具体工件边界未解决，保持 evidence_required，不强行纳入或排除。

最低补证要求：一条实际接纳的 role、output protocol 或 action-description / 行为指令工件：旧版、补丁、新版、诊断执行反馈、验证接纳结果及后续任务调用。该实例须能区分可复用执行策略与广告领域知识规则；外围代码冻结本身不能作为排除理由。

在补足可复用工件的原始实例后重开范围裁决；本 issue 继续开放。

原文：https://arxiv.org/abs/2610.39884

证据记录：`docs/internal/reports/maintenance-2026-11-02/reconciliation.json`。

### #20 · MoLRSI

处置：边界项，待具体工件证据。完成条件：补足上述原始工件与后续调用证据，复核输入身份并重新独立裁决；不能仅因当前资料缺失就强制 accept/reject。

最小原始补证：一个资源技能在持续使用后的完整生命周期：旧版、执行报错、修订、验收、后续不同任务调用。须证明是持续修改 Agent 自身 Harness，而不只是首次封装工具或修复依赖；科研模型、workflow 产物及经验选择统计不能替代该证据。

评论草稿：

已完成已有原文和范围意见的对照，目前仍有具体工件边界未解决，保持 evidence_required，不强行纳入或排除。

最低补证要求：一个资源技能在持续使用后的完整生命周期：旧版、执行报错、修订、验收、后续不同任务调用。须证明是持续修改 Agent 自身 Harness，而不只是首次封装工具或修复依赖；科研模型、workflow 产物及经验选择统计不能替代该证据。

此前审查包含 v2，本次已对照 canonical 对应的 v1；两个版本都尚未消除上述边界。

在补足可复用工件的原始实例后重开范围裁决；本 issue 继续开放。

原文：https://arxiv.org/abs/2610.39714

证据记录：`docs/internal/reports/maintenance-2026-11-02/reconciliation.json`。

### #21 · RecRSI

处置：回执遗漏已本地修复，可按范围排除关闭。完成条件：提交并保留本次来源范围裁决和回执修复记录后，可按 not_planned 关闭候选；范围排除不需要生成 accept 或日报发布证明。

评论草稿：

已复用与当前 canonical 输入 hash 完全一致的历史来源和独立复审，并补齐本地范围回执遗漏。RecRSI 修改的是推荐模型架构、损失、采样器和训练配方；原文列明 “architecture, loss, sampler, optimizer and schedule”。现有证据不支持把它当作研究 Agent 自己的可复用推理 Harness 演化。

建议按“不纳入当前 Harness 专题”关闭。此结论是范围排除，不是 accept 或发布；若出现可核验的自身 Harness 修改证据可重开。

原文：https://arxiv.org/abs/2610.39352

证据记录：`docs/internal/reports/maintenance-2026-11-01/owner-candidates.yaml`；`docs/internal/reports/maintenance-2026-11-01/primary/reconciliation.json`；`docs/internal/reports/maintenance-2026-11-01/independent/source-review.json`；`docs/internal/reports/maintenance-2026-11-01/independent/input-manifest.json`。

### #22 · MetaVul

处置：范围正例，正式发布闸门未通过。完成条件：完成新条目的正式审核和现有质量闸门，保留可核验通过记录，再核验实际发布；本报告不代替闸门，不恢复付费调用。

评论草稿：

官方摘要、正文和独立复审一致支持 Harness 方法候选。MetaVul 优化包裹检测 Agent 的独立 Python Harness，使用漏洞/修复函数对的反馈修订，保留候选历史并返回 Pareto 前沿，再冻结迁移到未见数据和模型。

但本条尚无正式质量闸门通过记录，不能把来源复审完成等同于 accept 或上线。保留 issue，待正式审核、闸门和实际发布核验；现阶段不恢复付费调用。

原文：https://arxiv.org/abs/2610.40721

证据记录：`docs/internal/reports/issues-2026-11-02/new-source-findings.json`；`docs/internal/reports/issues-2026-11-02/new-candidates-independent.json`。

### #23 · VEvo-Harness

处置：边界项，待具体工件证据。完成条件：补足上述原始工件与后续调用证据，复核输入身份并重新独立裁决；不能仅因当前资料缺失就强制 accept/reject。

最小原始补证：一条 skill 的字段结构及旧版、patch、新版，双臂比较的反馈与准入结果，以及后续任务实际调用。须能核验生成策略指令的变化，而不只是成功 prompt、记忆文本、语义嵌入或评分统计。

评论草稿：

已完成已有原文和范围意见的对照，目前仍有具体工件边界未解决，保持 evidence_required，不强行纳入或排除。

最低补证要求：一条 skill 的字段结构及旧版、patch、新版，双臂比较的反馈与准入结果，以及后续任务实际调用。须能核验生成策略指令的变化，而不只是成功 prompt、记忆文本、语义嵌入或评分统计。

此前主审与独立审查存在分歧，调和结果仍为 unknown；已对照 v1/v2，不能把其中一人的 include 当作共识。

在补足可复用工件的原始实例后重开范围裁决；本 issue 继续开放。

原文：https://arxiv.org/abs/2610.39158

证据记录：`docs/internal/reports/maintenance-2026-11-02/reconciliation.json`。

### #24 · From Grind to Grasp

处置：回执遗漏已本地修复，可按范围排除关闭。完成条件：提交并保留本次来源范围裁决和回执修复记录后，可按 not_planned 关闭候选；范围排除不需要生成 accept 或日报发布证明。

评论草稿：

已复用与当前输入 hash 一致的历史审查，并补齐本地范围回执遗漏。From Grind to Grasp 讨论工作量、信息及个人/集体递归改进的一般理论，并非专门研究 Harness 程序演化。排除理由是研究对象不符，不是因为理论论文没有自行执行改进闭环。

建议按“不纳入当前 Harness 专题”关闭，保留一般 RSI 理论线索。这不是 accept 或 Harness 发布证明；若出现新的专项证据可重开。

原文：https://arxiv.org/abs/2610.38728

证据记录：`docs/internal/reports/maintenance-2026-10-31/owner-candidates.yaml`；`docs/internal/reports/maintenance-2026-10-31/primary/review-reconciled.json`；`docs/internal/reports/maintenance-2026-10-31/independent/source-reviews.jsonl`。

### #25 · SceneEvolve

处置：本地完成，待实际部署验证。完成条件：实际请求公开目标成功，确认论文 ID、日期及候选状态与审核一致，并记录检查时间和发布提交后再关闭。

评论草稿：

既有来源范围意见和 owner 回执支持纳入 Harness：冻结学生外的场景重建 Harness 根据开发集执行/评分反馈更新，最终冻结用于未见场景。已在本地生成 SceneEvolve 历史候选卡片，证据字段继续保持 unknown。

当前尚无实际部署验证，issue 继续保留。完成线上卡片及身份、候选状态核验后再按 completed 关闭；该条是历史补录，不混入今天的 HF 日报。

原文：https://arxiv.org/abs/2610.37046

部署后条件草稿：

仅在记录线上核验时间及发布提交后使用：已验证公开页面 https://adongwanai.github.io/follow-rsi/p/sceneevolve.html 的论文身份、日期与审核记录一致。本项作为历史候选补录，证据未知项仍为 unknown，不计作今日 HF 新闻。据此可按 completed 关闭候选处理 issue。

证据记录：`docs/internal/reports/maintenance-2026-10-30/independent/manifest.json`；`docs/internal/reports/maintenance-2026-11-02/item-status.jsonl`。

### #26 · RuHarness

处置：本地完成，待实际部署验证。完成条件：实际请求公开目标成功，确认论文 ID、日期及候选状态与审核一致，并记录检查时间和发布提交后再关闭。

评论草稿：

既有来源范围意见和 owner 回执支持纳入 Harness：执行轨迹更新 rubric，指导六类可复用 Harness 功能的修订并验证保留。已在本地生成 RuHarness 历史候选卡片；尚未独立核实的证据字段保持 unknown。

当前尚无实际部署验证，issue 继续保留。完成线上卡片身份及候选状态核验后再按 completed 关闭；不把本条历史补录写成今天 HF 新推荐。

原文：https://arxiv.org/abs/2610.36826

部署后条件草稿：

仅在记录线上核验时间及发布提交后使用：已验证公开页面 https://adongwanai.github.io/follow-rsi/p/ruharness.html 的论文身份、日期与审核记录一致。本项作为历史候选补录，证据未知项仍为 unknown，不计作今日 HF 新闻。据此可按 completed 关闭候选处理 issue。

证据记录：`docs/internal/reports/maintenance-2026-10-30/independent/manifest.json`；`docs/internal/reports/maintenance-2026-11-02/item-status.jsonl`。

### #27 · Training for Alignment

处置：可按范围排除关闭。完成条件：提交并保留本次来源范围裁决和回执修复记录后，可按 not_planned 关闭候选；范围排除不需要生成 accept 或日报发布证明。

评论草稿：

官方来源和独立复审一致认为，Training for Alignment 是内生偏好的训练、激励与泛化理论。摘要说明 “an agent with an endogenous bias”；RSI 是应用语境之一，并非专门研究外部 Harness 程序的反馈修订和保留。这里的 bias 也不能擅自写成神经模型权重实验。

建议按“不纳入当前 Harness 专题”关闭，保留一般对齐/RSI 理论线索。关闭仅解决范围归属，不表示正式 accept 或发布；后续有 Harness 专项证据可重开。

原文：https://arxiv.org/abs/2610.40684

证据记录：`docs/internal/reports/issues-2026-11-02/new-source-findings.json`；`docs/internal/reports/issues-2026-11-02/new-candidates-independent.json`。

### #28 · The Trinity

处置：本地完成，待实际部署验证。完成条件：实际请求公开目标成功，确认论文 ID、日期及候选状态与审核一致，并记录检查时间和发布提交后再关闭。

评论草稿：

本条已有匹配来源的范围批准和审核记录，本地已恢复到 HF 推荐日 2026-10-28；论文原发表/版本日仍为 2026-10-26，实际复审日为 2026-11-02。冻结模型外的协议模块依据执行反馈修订并继承，能力树拓扑固定；不把局部接纳都说成分数提高，也不把全部收益归因于模块演化。

目前只确认本地恢复，尚未核验线上部署。保留 issue，待 10/28 日报与卡片上线、日期和证据正确后再按 completed 关闭。

原文：https://arxiv.org/abs/2610.36077

部署后条件草稿：

仅在记录线上核验时间及发布提交后使用：已验证公开页面 https://adongwanai.github.io/follow-rsi/daily/2026-10-28.html 的论文身份、日期与审核记录一致。本项属于 HF 2026-10-28 推荐，原发表/版本日 2026-10-26，复审日 2026-11-02；未归到复审日充作新推荐。据此可按 completed 关闭候选处理 issue。

证据记录：`docs/internal/reports/publication-recovery-2026-11-02/oct28-review.json`；`docs/internal/reports/maintenance-2026-11-02/item-status.jsonl`。

### #29 · Work Agents

处置：可按范围排除关闭。完成条件：提交并保留本次来源范围裁决和回执修复记录后，可按 not_planned 关闭候选；范围排除不需要生成 accept 或日报发布证明。

评论草稿：

已复用与当前输入一致的来源范围裁决及 owner 回执。Work Agents 是工作 Agent 系统、能力和优化的一般综述，涉及模型、Harness 和联合优化，但不是 Harness 演化专项。历史模型意见为 defer，现行范围排除来自另外保存的来源审查与裁决，未改写历史模型结果。

建议按“不纳入当前 Harness 专题”关闭。本项不计入已发布 Harness；出现新的专项证据时可以重开。

原文：https://arxiv.org/abs/2610.35845

证据记录：`docs/internal/reports/maintenance-2026-10-30/independent/manifest.json`；`docs/internal/reports/maintenance-2026-10-30/coverage/item-status.jsonl`；`docs/internal/reports/maintenance-2026-11-02/item-status.jsonl`。

### #30 · OmniBrain-0

处置：边界项，待具体工件证据。完成条件：补足上述原始工件与后续调用证据，复核输入身份并重新独立裁决；不能仅因当前资料缺失就强制 accept/reject。

最小原始补证：一份 reminder policy 或 rubric 的真实版本差异及后续调用，说明被修改的是可复用策略工件，还是固定提醒器中累积的规则/提醒内容。正文已有冻结参数验证、反馈修订和跨轮保留，不能仅凭其他部分训练权重就排除。

评论草稿：

已完成已有原文和范围意见的对照，目前仍有具体工件边界未解决，保持 evidence_required，不强行纳入或排除。

最低补证要求：一份 reminder policy 或 rubric 的真实版本差异及后续调用，说明被修改的是可复用策略工件，还是固定提醒器中累积的规则/提醒内容。正文已有冻结参数验证、反馈修订和跨轮保留，不能仅凭其他部分训练权重就排除。

身份核验：issue 摘要与官方摘要一致；canonical 仅漏了 teachers' 后一个空格，不是版本或科学内容变化。

在补足可复用工件的原始实例后重开范围裁决；本 issue 继续开放。

原文：https://arxiv.org/abs/2610.36013

证据记录：`docs/internal/reports/maintenance-2026-11-02/reconciliation.json`。

## 校验与指令依据

- 覆盖 #16–#30，无重复；动作分组 3 + 2 + 3 + 3 + 4。当前 2 条回执遗漏已修复，因此范围关闭就绪合计 5 条。
- 15 条当前 canonical source hash 与已审输入或原始录入提案一致；#21/#24 的历史 manifest / owner-candidates hash 证明见上文。
- 所有报告引用文件在生成时存在；完整 SHA256 保存在配套 JSON。
- 没有把来源判断写成 formal accept，没有把本地页面写成已上线。
- 以 owner 后发 CODEX_PROMPT_FIX_AUDIT.md 第七节为准：撤销旧正序提交，日报索引从新到旧，证据库默认必读优先；此计划不修改排序。
