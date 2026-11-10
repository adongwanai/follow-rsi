# 2026-11-10 免费来源抓取交付

本文件只报告已实际抓取的来源、身份/日期/哈希核验与增量提案；不等同正式接受或发布。

基线 main：`0f9de911ee1ee33f68b6ffc8c9a22876ca82a1f2`，canonical 1838 条；基线 SHA-256 `2d366e0eb92b15c8c8a9dc19e943a3858534219f2ba01f8715e8402f3405f6b2`。

12/12 路已尝试并结束。配置来源共 94 次真实请求；官方元数据和全文补抓另存独立回执，不混入该数。

| 来源 | 状态 | 请求 | 原始出现 | 窗口出现 | 窗口去重 |
|---|---|---:|---:|---:|---:|
| arxiv-harness | ok | 1 | 0 | 0 | 0 |
| arxiv-rsi | ok | 1 | 0 | 0 | 0 |
| arxiv-adjacent | ok | 1 | 0 | 0 | 0 |
| s2-citations | partial | 53 | 4127 | 311 | 278 |
| s2-authors | error | 17 | 0 | 0 | 0 |
| hf-daily | historical_boards_ok_today_not_ready | 3 | 31 | 31 | 31 |
| rss-sakana | ok | 1 | 12 | 2 | 2 |
| rss-metr | ok | 1 | 256 | 4 | 4 |
| rss-openai | ok | 1 | 1372 | 40 | 40 |
| rss-deepmind | ok | 1 | 100 | 4 | 4 |
| rss-weco | ok | 1 | 13 | 0 | 0 |
| github-releases | ok | 13 | 12 | 0 | 0 |

## 日期与晚到成员

- 11/10 HF HTTP 400 / not_ready，错误响应宣称 available_through=11/08。
- 显式请求 11/09 返回 HTTP 200、31 篇；相对昨日 8 篇新增 23 个晚到成员。完整原始榜单对账未用关键词预筛。
- 11/08 HTTP 200、空榜。保留 API 日期提示与已成功 11/09 榜的矛盾；不能据错误提示断言 11/09 不存在。
- 23 个晚到成员的推荐日为 11/09，实际来源观察为 11/10；不能冒充 11/10 推荐。
- RSI-ESA 首次观察保留仓库 issue #71 的 2026-11-09T08:03:44Z；今日 S2 再观察单独记录。

## 对账与受阻

- 成功响应恢复 5,923 次原始出现、5,622 个稳定 ID；配置窗口内 392 次出现、358 个 ID。
- 新 canonical 提案 38 项：34 篇论文、4 篇官方文章。旧记录 provenance/HF 日期增量 0，身份冲突 0，待补官方元数据 0。
- S2 citations 53 请求（43×200、10×429），恢复窗口内 311 次出现、278 个 ID；采集器原计数 315 中 4 条晚于目标日期，已从窗口排除。
- S2 authors 17 请求（4×200、13×429），未获得论文页；两路分别在约 180 秒边界结束，未遍历覆盖仍 unknown。
- S2 匿名模式，70 次请求间实际 monotonic 最小间隔 3.101154542 秒。429 指数退避最多 5 次重试，受单路剩余时间约束。
- METR/RSS 原文包含畸形 IPv6 URL，解析器实际给出警告并忽略该链接候选；来源条目和原始响应仍保留。

## 核验与交接

- 34 篇官方 arXiv 身份、原发表日、更新日、版本全部对应；33 份 HTML 正文和 1 份官方 PDF 文本可读，另 4 篇官方文章全文可读。
- 195 个引用源文件 SHA-256 已逐项验证；个别 arXiv HTML 的 title 转换异常已留档，未据此篡改官方标题。PDF 文本可提取但未做视觉表格复核。
- `intake-qa.json` 为实际离线检查结果，`integration-proposal.json`/`candidate-records.jsonl` 为未应用提案。
- 四篇 watch-only 由另一个 agent 负责，本目录不重复追加。
- 正式 data/review/site 写入 0，付费模型调用 0，无接受、合并、发布动作。
- 范围第三轮独立意见另交 `independent-review.json`；所有提案 formal_decision=defer，是否落实由主 agent 依持续授权与逐项检查决定。
