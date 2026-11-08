# 2026-11-07 免费来源快照

生成时间 2026-11-07T00:12:35.043397+00:00；12 路中 12 路已结束。本报告只涵盖实际请求得到的响应，失败源未覆盖部分保持未知。

| 来源 | 状态 | 全部原始记录 | 窗口内记录 | 请求/HTTP |
|---|---|---:|---:|---|
| arxiv-harness | ok | 0 | 0 | 1 / {'200': 1} |
| arxiv-rsi | ok | 0 | 0 | 1 / {'200': 1} |
| arxiv-adjacent | ok | 0 | 0 | 1 / {'200': 1} |
| s2-citations | partial | 100 | 7 | 7 / {'200': 1, '429': 6} |
| s2-authors | error | 0 | 0 | 8 / {'429': 7, '200': 1} |
| hf-daily | historical_boards_ok_today_not_ready | 70 | 70 | 3 / {'400': 1, '200': 2} |
| rss-sakana | ok | 10 | 4 | 1 / {'200': 1} |
| rss-metr | ok | 210 | 3 | 1 / {'200': 1} |
| rss-openai | ok | 1368 | 46 | 1 / {'200': 1} |
| rss-deepmind | ok | 100 | 5 | 1 / {'200': 1} |
| rss-weco | ok | 13 | 0 | 1 / {'200': 1} |
| github-releases | ok | 12 | 0 | 13 / {'200': 13} |

HF 11/07 尚未开放；本次完整核对 11/05 与 11/06 已开放榜单，不使用关键词筛选后的数量冒充完整榜单。

相对 1749 条 canonical 基线，提议新增 59 条；5 条已知记录有来源/日期补记，25 条有官方元数据差异需审，0 条身份冲突待核对。

全部 raw ID、出处 hash 和时间见 raw-source-id-reconciliation.jsonl。可应用清单见 integration-proposal.json；该清单尚未应用，保留所有旧 first_seen、科学字段、审核和发表状态。

失败或范围限制：
- s2-citations: HTTPError: 429 Client Error:  for url: https://api.semanticscholar.org/graph/v1/paper/arXiv:cs/0309048/citations?fields=paperId%2Ctitle%2Cabstract%2Cauthors%2CexternalIds%2CpublicationDate%2Curl%2CfieldsOfStudy&offset=100&limit=100
- s2-authors: HTTPError: 429 Client Error:  for url: https://api.semanticscholar.org/graph/v1/paper/arXiv:2310.02304?fields=authors
- hf-daily: {'2026-11-07': 'not_ready: HTTPError: 400 Client Error: Bad Request for url: https://huggingface.co/api/daily_papers?date=2026-11-07'}

0 付费调用；未运行 judge、summarize 或 evaluate；未修改 production、commit、push 或 GitHub。
