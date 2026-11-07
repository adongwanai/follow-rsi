# 2026-11-05 历史积压对账

冻结基线为已部署的 `fa7a628a1a1c720c130159943249979e08e0c0c9`；**本轮新采集的 11/05 来源不混入旧遗漏**。旧基线没有新增 HF 入库或推荐日期遗漏。找到 1 项可免费消除的 Sakana 重复，完整原记录、引用校验和保留旧稳定 ID 的候选已交主任务整合。

## 原始来源与稳定 ID

118 份已保存原始快照全部离线解析，包含 S2 11/04 成功分页的原始 body 哈希验证；0 解析错误。规范表、原始来源、616 条旧发现和审核单的并集仍为 **8,331**：1,598 条规范记录、6,292 条处于所有已存时间窗之外、441 条缺可用 S2 发表日期。未发现新旧遗漏；后两组继续作为来源诊断，不能称为 6,733 条待审新闻。

13 份 HF 快照展开为 **686 个稳定 ID / 686 个推荐日成员**，全部已入规范库且推荐日一致。196 条历史补录的摘要哈希、推荐日与本轮发现时间均核对通过；旧真实抓取时间仍未知。其阅读层级仍是 34 条完整摘要、162 条摘要方法摘录，不能升级为 196 篇全文三轮审核。

昨日 138 个证据输入中 137 个字节哈希不变；唯一变化为已经记录过整合的 `items.jsonl`。旧 1,351 条里只有 Video Generation Meets Agent Harness 与 TinyAstral 的来源哈希变化，逐字段仅 `hf_daily_dates`、`links`、`source_hits`，原科学字段及 owner 决定不变。其余旧意见按原哈希复用。

## 回执与可恢复阶段

682 条范围回执仍为 680 条当前哈希严格一致、2 条已知来源元数据漂移（R²Orch、GEPA-Curator）；AdaPRA 的后续 defer 纠正保留。21 份本地审核 YAML 共涉及 1,250 个唯一 ID，全部可回连规范记录或 alias。32 条历史模型失败均可追溯，其中 20 条仍在当前 retry 阶段，其他项已有后续阶段，未重新探测余额或调用模型。

|可恢复阶段|冻结基线数量|本轮处置|
|---|---:|---|
|旧模型意见待当前规则复核|426|全部来源哈希未变，保留逐 ID 队列|
|已有范围意见、缺双语摘要|187|保留摘要阶段，未伪称完成|
|摘要已齐、待正式出版条件|41|保留质量与正式决定门|
|范围回执要求补工件证据|49|保留具体证据条件|
|当前模型失败重试|20|付费暂停，不重试|
|范围意见与生产标签待对齐|32|保留旧意见，不擅改决定|
|Sakana 来源身份重复|1|已提供安全删除重复行的候选|

这些阶段队列有重叠，不能相加。完整阶段指针和 ID 集合哈希见 [机器回执](backlog-reconciliation.json)；逐项大台账复用 [昨日对账](../maintenance-2026-11-04/backlog-reconciliation.json)，不再复制 5.6 MB 不变内容。

Sakana 的 8 个审核引用为：保留 ID 的 1 条既有范围排除 + 10/29、10/31、11/01、PR37 中的 4 条 defer；被移除 ID 仅在 10/31、11/01、PR37 中有 3 条 defer，均无 note、override 或独立批准。保留旧记录逐字段不变即可保留最早 first_seen、自动范围意见、来源及原批准哈希；绝对 URL ID 已是它的 alias。[重复项核验](backlog-duplicate-reconciliation.json)

另核对 21 个历史公开条目的回执：6 个 source hash 与当前直接一致，15 个 10/27 correction 因后来增加来源 links 而不相同。15/15 原回执均严格匹配原修订提交 `b7c0d68` 的记录；临时仅还原 links 可全部复现原哈希，标题、摘要、日期、版本、科学结论与审核决定均未改变。这是已存在的来源补充，旧哈希与原回执保留，不编造重新批准。[逐项证据](backlog-published-legacy-bindings.json)

## GitHub 与已部署内容

实时 main 仍为冻结提交；#3、#36 已合并，#35 关闭且未合并。#37 保持 open，head 为 `c4bd5af5375f7bb2791f95899bb505043637bd43`：186 篇论文、89 条 lab 条目，275 个决定全部 defer。相对初建 head 仅删一个 backlog `carried_from` 字段，owner 字段未改变。最近 owner-review dispatch 成功，但此 head 的 build/validate 都是 `action_required`，不报告为全 CI 通过。

7 个论文 issue 及更新时间均未出现新变化：#16/#18/#22 受质量门阻塞，#19/#20/#23/#30 受工件证据阻塞。10/30 最近完整真实评测仍为 precision **24/26**、recall **24/28 = 0.8571 < 0.90**；本轮没有重跑。PR37 body 中 0.96 precision 属于旧评测轮次，不当作新测结果。`feed-daily`、`feed-eval`、`feed-publish` 均实际核实为 `disabled_manually`。

21 条正式 accept 与 21 条已公开 feed 逐 ID 对应；实时 `feed/latest.json` 与 `feed/atom.xml` 逐字匹配已部署基线，后者仍为 4 条 Atom 条目。本轮没有新增正式接受、出版或 GitHub 写入。

RSIHub/HarnessDev 仍为 `harness_eval`，HarnessDev 必读；Aspire/S3Gym 为 `general_rsi`。实验设计路线的前四项仍为 Rethinking → HDA → HarnessDev → RSIHub，之后还有 HarnessOpt-Bench、Auditing Product、Trusting Trust Revisited，未将前四项误当整条路线。

本子任务只写报告与 build 内的审计工件，生产数据/代码未写、付费调用为 0。规范表最终计数与重复项实际整合回执由主任务另记；此报告不把候选准备当作已应用。
