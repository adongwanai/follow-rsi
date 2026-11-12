# 2026-11-12 免费来源第一轮交接

生成 2026-11-12T06:37:56.013911+00:00。实际采集 06:24:43–06:29:27 UTC（北京时间14:24–14:29），不是08:00执行。具体逐次时间以network receipts为准。

本子agent只写docs/internal/reports/maintenance-2026-11-12。没有付费模型请求，未改production、data、review或site，未commit、push或写GitHub。主agent并行操作不在此断言内。

## 完成内容

规范基线1944项、main 0329b9ce4d6a436a94abe9794adf2af430fddcc2。全部12路已启用来源均实际请求；原始5499次出现/5211唯一ID，配置窗口456次/421ID。65新增ID=58论文+7官方文章；所有58新论文官方arXiv身份、题名、摘要、原发表和版本日期对齐，96个metadata目标全部返回。无identity collision。

全部HF响应禁用关键词预筛，84成员全部对账：11/12榜6篇、11/11榜39篇、11/10榜39篇。11/10比前一快照37篇多出2611.05927与2611.11994，真实推荐日保持11/10。今日返回200可用快照，不是not_ready；同日仍可能晚到，不能宣称全日最终榜。11/11此前not_ready不能被当成0篇，因此不把39篇全标“迟到”。

唯一旧provenance补记为RoboScript 2611.12885：新增hf-daily来源和真实11/11推荐日。当前official title/abstract/published/updated/version与旧科学字段一致。原first_seen和review不变，新source_hash须新日期审核，不将旧批准hash改写为新hash。review-reuse-deltas.json只是来源/哈希核对，不是重新范围审查。

旧metadata差异仅ReproBridge 2611.08452作者姓名格式；metadata-change-triage中保留为提案，不自动应用。

## 来源健康

|来源|状态|窗口记录/ID|HTTP|
|---|---|---:|---|
|arxiv-harness|ok|0 / 0|{'200': 1}|
|arxiv-rsi|ok|0 / 0|{'200': 1}|
|arxiv-adjacent|ok|0 / 0|{'200': 1}|
|s2-citations|partial|318 / 285|{'200': 38, '429': 15}|
|s2-authors|error|0 / 0|{'200': 1, '429': 6}|
|hf-daily|ok|84 / 84|{'200': 3}|
|rss-sakana|ok|2 / 2|{'200': 1}|
|rss-metr|ok|4 / 4|{'200': 1}|
|rss-openai|ok|41 / 41|{'200': 1}|
|rss-deepmind|ok|7 / 7|{'200': 1}|
|rss-weco|ok|0 / 0|{'200': 1}|
|github-releases|ok|0 / 0|{'200': 13}|

S2引文53请求（38×200/15×429），180秒窗口后保留成功页面，剩余覆盖unknown。collector322条含4条晚于目标日，原始记录未删；最终窗口318条/285ID。作者查询7请求（1×200/6×429），0论文。全体S2请求按anonymous≥3.1秒共享限速，429初次后最多5次指数退避；详见intake-qa。三路arXiv查询均HTTP200、0条；五路RSS窗口54条；GitHub13仓库均HTTP200、窗口release0条。

## 正文证据

58新arXiv正文都已取得并验证版本：55 HTML、3官方带版本PDF回退（2611.13348、2611.13885、2611.14382）。5份HTML在metadata补齐前以不带v路径请求，原始receipt保留None，后用HTML内嵌版本与官方metadata核对，不回写请求历史。7官方文章均HTTP200，body/text hash receipts俱全。

潜在正例和边界材料均在scope-fulltexts/<arxiv_id>.html/.txt，PDF正文为.pdf/.pdf.txt：EmoHarness2611.11994、ReTrace2611.14492、LASER2611.14113、SAT2611.13144、NCP2611.13236、RoboACE2611.13034、FGSE2611.14326、Synapse-Control2611.13615、WikiTrace2611.14320、FINCOSMOS2611.07464、Survey2611.14256、BVSR2611.12184、Micius2611.10015、LEASH2611.14115、DyCraft2610.40754。由主审及独立第三轮判断范围，本交接不给正式接受意见。

第一轮离线QA 13项通过：原始body/text哈希、官方metadata、58正文版本、84 HF成员、first_seen、S2间隔/重试上限等。不是论文实验复现或数字重算，也不是正式接受/上线。

## 冻结文件

- `integration-proposal.json` — SHA256 `038d6f640c1ea2de4cac9d74ce7fdb670b9a2cf1ea5681e6780858449f2f851b`
- `all-source-snapshot.json` — SHA256 `bd3980f46d1fab577852d003b4a386219d14e5d4f5c659a6c1a703b83bdeae50`
- `raw-source-id-reconciliation.jsonl` — SHA256 `2eb0f263f7dbe34a3f13386ab9bd9bf7b29821d9e6c5ecec70bb8506392a6f6f`
- `hf-board-reconciliation.json` — SHA256 `57ef8d14ec12975b26f90ffee7b61e3e44669d89e0dcc0e7bc28f69e2e453d3f`
- `metadata-change-triage.json` — SHA256 `9fb92affe6e74f51ff60b9624dc667c04122ed6238f44fce101d19fb8006786a`
- `review-reuse-deltas.json` — SHA256 `13889f48f681c4eecce1573be342c510e6871bb290f679027e8c6777c750bd88`
- `fulltext-version-verification.json` — SHA256 `de30b4756f9d97a707f8c358d7d322e9f5326ba32039e100fc1eab8056fdc5c4`
- `intake-qa.json` — SHA256 `3055d362aad380ff6f51035e146dcf981108f21f99d8c87bfac287aa012a9fe8`

源证据目录：network/、source-results/、data/feed/raw/、official-metadata/、scope-fulltexts/、post-fulltexts/。原始HTTP和页面字节保留；报告对比只读官方及保存响应。
