# 2026-11-02：旧建议按新判据的独立盲审

本批 57 条（52 篇 arXiv、1 篇期刊综述、4 篇官方文章）全部完成范围建议：**57 exclude / 0 include / 0 unknown**。这里的 exclude 只表示不进入 Harness 演化发布范围，不代表文章无价值。全部仍为 `decision: defer`、`publishable: false`、`human_approved: false`。

`findings.json` 在查看本批主审结果前冻结；每条保留中性输入的 `canonical_source_hash`、已读层级和 1–3 条原文引句。76 条引句及对应文件哈希逐项验证。没有调用付费 API，没有修改 canonical、审核决策、生产提示词或发布内容。

## 已读来源与边界

- 52 篇官方 arXiv 摘要，标题、日期、版本均匹配。45 篇摘要逐字一致，7 篇只有 LaTeX 展示标记差异。没有把摘要核查写成全文精读。
- CausGround：补读方法及附录的知识库构造、检索和执行流程。保留的是环境动作前提/效果知识；执行时检索因果子图保持固定。
- Reasoning effort economics：补读路由、laddering 方法及相关分析。预设规则按失败反馈重试同一任务，没有跨任务修订的 Harness 版本。
- CrossProfile / Rare, Relevant, and Still Wrong：补读引言、任务构造与记忆策略。对比固定策略，不研究策略的反馈演化。
- 4 篇官方文章均核对官方 RSS 标题、摘要、日期。完整阅读 Sakana 情报案例、Legora 客户案例和 ServiceNow 合作公告；经济随笔阅读引言及组织层级场景，未声称全文通读。
- 期刊综述直接核对 Springer 完整摘要、数据/代码可用性，以及 Crossref DOI/标题/上线日期。页面明确是订阅预览，未获得论文全文；其通用 Web Agent 研究对象在完整摘要中已清楚，因此范围建议不受此访问限制阻塞。

## 数据问题（只报告）

`arxiv:2610.35013` 的 canonical 作者名单有若干差异。除连字符外，`Kun Ding` 对应官方 `Kunbao Ding`，`Feng-Jie Chang` 对应官方 `Feng Chang`。本次实时获取的官方 abs metadata 与原 Atom 一致。标题、摘要、日期、版本均匹配；原始作者数据未改。

## 文件

- `findings.json`：冻结结果。
- `validation.json`：57 条全量覆盖、76 条逐字引文校验及冻结哈希。
- `official-abstract-manifest.json`、`post-identity-checks.json`、`publisher-identity.json`：身份/摘要核对。
- `source-attempts.json`、`reused-body-sources.json`、`author-discrepancy-current-check.json`：5 次免费官方请求与缓存正文复用记录。
- `checksums.json`：来源文件和报告哈希；原文缓存位于同日期的 `build/.../prior-rule-independent/`，沿用来源定位，不复制到公开论文事实文件。
