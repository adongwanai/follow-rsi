# 2026-11-14 免费采集与第一轮身份日期交付

本 source-intake 清单已冻结。实际采集开始 2026-11-14 10:46:31 北京时间；不是 08:00 的快照。仅修改本目录，无生产整合、范围接受、付费调用、Git 操作或发布。

- 12/12 已启用源均实际尝试；来源请求 89 次，另 51 次身份/正文补证请求。
- 原始 occurrences 6958 / 唯一 ID 6243；配置窗口 occurrences 524 / 唯一 ID 411。
- 相对 2033 条基线新增 41 条（37 arXiv +1 非 arXiv 论文 +3 官方文章）；2 条已有记录仅增补 HF 来源/推荐日。
- HF 11/14 HTTP200 空列表，实际观察为 0 条；11/13 HTTP200 完整 34 条（此前 not_ready）；11/12 HTTP200 完整 21 条（此前 20），晚到 2611.08538。
- HF 新 ID 共 33：11/13 推荐 32 条、11/12 晚到 1 条；first_seen 均为真实 11/14 观察时间。全部原始 HF 成员已对账，无关键词预筛。
- arxiv:2611.08318 和 arxiv:2611.14256 仅增加真实 11/13 HF 推荐日。08318 既有接受及出版须保留，不作为新论文重复发表；14256 既有排除须保留。未改 first_seen、正文事实或旧批准。
- 37/37 新 arXiv 已以官方 Atom 核实身份、初发表和版本日期；对应版本正文 33 HTML +4 PDF 全部校验。4 个 S2 新 arXiv（2611.13740、2611.09254、2611.05953、2611.10016）均含元数据和正文。
- 22 个已有 HF 成员中，21 个可复用 11/12–11/13 官方元数据，缓存原始哈希和 canonical 科学字段一致；08318 未在这两日元数据档中找到，保留历史审核及基线。这是旧证据复用，不声称今日版本仍最新。
- 3 篇文章均取得官方全文。DeepMind HTML 原始字节和 SHA-256 不变，依据 HTML 明确的 UTF-8 声明修正 txt 解码；原乱码 txt/receipt 保存在 post-fulltexts/encoding-history。
- Semipy DOI 10.1145/3830397.3841889 的 Crossref 题名、2 作者均与 S2 匹配；印刷/出版日 11/02、在线日 11/13 分列。ACM 落地和 PDF 均 HTTP403；同名代码仓库 README 可读，但未绑定该论文 DOI/题名/作者，不能替代正文。摘要和版本仍 unknown。
- S2 引文 partial：58 请求（54 HTTP200、4 HTTP429），180 秒截止；配置窗口 411 条/300 ID，另 5 条未来日期剔除。S2 作者 7 请求（1 HTTP200、6 HTTP429）后失败、0 论文；未访问覆盖 unknown。
- 13/13 第一轮 QA 通过；source-evidence-index 的 41 条原始绑定、37 个官方元数据绑定及 40 个正文/提取文本哈希另经复核。此为身份/日期/来源校验，不等于 scope 批准、实验复算或上线。

## 稳定交付

- integration-proposal.json：41 条未应用新记录及 2 条旧记录来源/推荐日补记。
- source-evidence-index.json：逐项身份、日期、来源绑定、正文哈希和补证边界。
- all-source-snapshot.json / .md：12 路采集时间、数量、实际 HTTP 状态和覆盖限制。
- hf-board-reconciliation.json：3 日完整原始 HF 榜单及晚到差异。
- prior-hf-identity-evidence.json：22 条旧 HF 成员的缓存复用/缺失边界。
- fulltext-version-verification.json、intake-qa.json、review-reuse-deltas.json：逐项校验及旧审核保留。
- additional-official-sources/semipy-identity-audit.json：DOI 身份、日期精度和正文阻塞。
- evidence-manifest.json：本目录全部文件的字节数、SHA-256（不含自身）。

| 来源 | 请求 | 原始条数 | 窗口条数 | 状态 |
| --- | ---: | ---: | ---: | --- |
| arxiv-harness | 1 | 0 | 0 | ok |
| arxiv-rsi | 1 | 0 | 0 | ok |
| arxiv-adjacent | 1 | 0 | 0 | ok |
| s2-citations | 58 | 5123 | 411 | partial |
| s2-authors | 7 | 0 | 0 | error |
| hf-daily | 3 | 55 | 55 | ok |
| rss-sakana | 1 | 12 | 2 | ok |
| rss-metr | 1 | 256 | 4 | ok |
| rss-openai | 1 | 1387 | 44 | ok |
| rss-deepmind | 1 | 100 | 8 | ok |
| rss-weco | 1 | 13 | 0 | ok |
| github-releases | 13 | 12 | 0 | ok |
