# 2026-11-13 免费采集与第一轮身份日期交付

清单已冻结；仅修改本 source-intake 目录，无生产整合、正式分类、付费请求、Git 操作或发布。

- 12/12 已启用源均实际尝试；源请求 99 次，另33次身份/正文补证请求。
- 原始 occurrences 6634 / 唯一 ID 6119；配置窗口 occurrences 494 / 唯一 ID 417。
- 相对 2009 条基线新增 24 条（18 arXiv +1 非 arXiv 论文 +5 官方文章）；1 条已有记录仅补来源标签，0 HF 推荐日补记。
- 11/13 HF HTTP400 not_ready，明确 available_through=11/12；11/12 完整20条，较昨日6条新增14个晚到成员；11/11完整39条，与昨日无变化。
- 14个晚到新ID推荐日仍为11/12；first_seen保留11/13真实观察时间。全部原始HF成员已对账，无关键词预筛。
- 18/18新 arXiv 已官方Atom核实身份/初发表/版本日期并取得对应版本正文（14 HTML、4 PDF）。原先59-ID Atom的timeout和429保留，缩小18-ID后HTTP200。
- 45个已有HF成员复用昨日官方身份数据，原数据哈希一致、canonical科学字段一致；此复用不宣称今日重新验证或不存在新版本。
- 5篇文章均取得官方全文。UniCommerce作者repo README可读，Crossref DOI题名和作者匹配；官方仅2026-11月精度，S2所报11/01的具体日为unknown。IEEE落地HTTP202空正文；不能声称全文或数字审计。
- S2引文partial：57请求，50 HTTP200、6 HTTP429、1最终超时；配置窗口380条/304 ID，另4条未来日期剔除。S2作者18请求（6 HTTP200、12 HTTP429）后180秒截止，无论文返回；未访问覆盖unknown。
- 13/13第一轮QA通过（原始哈希、日期保留、身份去重、版本、请求间隔）；不等于所有来源遍历完成，不等于scope批准、实验复算或上线。

## 可供主审/独立复审的稳定文件

- `integration-proposal.json`：未应用的24条新记录和1条旧来源补记。
- `source-evidence-index.json`：每条源绑定、正文路径/哈希、官方日期与版本证据。
- `all-source-snapshot.json` / `.md`：12路时间、数量、HTTP状态、覆盖限制。
- `hf-board-reconciliation.json`：完整榜单与晚到差异。
- `prior-hf-identity-evidence.json`：45条昨日官方身份复用边界。
- `fulltext-version-verification.json`、`intake-qa.json`、`review-reuse-deltas.json`：逐项校验。
- `additional-official-sources/unicommerce-identity-audit.json`：DOI/作者repo与日期精度边界。
- `evidence-manifest.json`：归档前路径、字节数、SHA-256（不含自身）。

| 来源 | 请求 | 原始条数 | 窗口条数 | 状态 |
| --- | ---: | ---: | ---: | --- |
| arxiv-harness | 1 | 0 | 0 | ok |
| arxiv-rsi | 1 | 0 | 0 | ok |
| arxiv-adjacent | 1 | 0 | 0 | ok |
| s2-citations | 57 | 4797 | 380 | partial |
| s2-authors | 18 | 0 | 0 | error |
| hf-daily | 3 | 59 | 59 | historical_boards_ok_today_not_ready |
| rss-sakana | 1 | 12 | 2 | ok |
| rss-metr | 1 | 256 | 4 | ok |
| rss-openai | 1 | 1385 | 42 | ok |
| rss-deepmind | 1 | 100 | 7 | ok |
| rss-weco | 1 | 13 | 0 | ok |
| github-releases | 13 | 12 | 0 | ok |
