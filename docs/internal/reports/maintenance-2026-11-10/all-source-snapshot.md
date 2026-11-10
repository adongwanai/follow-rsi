# 2026-11-10 免费来源快照

生成时间 2026-11-10T00:15:47.212516+00:00；12 路中 12 路已结束。本报告只涵盖实际请求得到的响应，失败源未覆盖部分保持未知。

| 来源 | 状态 | 全部原始记录 | 窗口内记录 | 请求/HTTP |
|---|---|---:|---:|---|
| arxiv-harness | ok | 0 | 0 | 1 / {'200': 1} |
| arxiv-rsi | ok | 0 | 0 | 1 / {'200': 1} |
| arxiv-adjacent | ok | 0 | 0 | 1 / {'200': 1} |
| s2-citations | partial | 4127 | 311 | 53 / {'200': 43, '429': 10} |
| s2-authors | error | 0 | 0 | 17 / {'200': 4, '429': 13} |
| hf-daily | historical_boards_ok_today_not_ready | 31 | 31 | 3 / {'400': 1, '200': 2} |
| rss-sakana | ok | 12 | 2 | 1 / {'200': 1} |
| rss-metr | ok | 256 | 4 | 1 / {'200': 1} |
| rss-openai | ok | 1372 | 40 | 1 / {'200': 1} |
| rss-deepmind | ok | 100 | 4 | 1 / {'200': 1} |
| rss-weco | ok | 13 | 0 | 1 / {'200': 1} |
| github-releases | ok | 12 | 0 | 13 / {'200': 13} |

HF 当日状态：not_ready；API 给出的 available_through：2026-11-08。实际成功响应完整榜单及篇数：{'2026-11-09': 31, '2026-11-08': 0}。空数组仅说明该次请求返回空榜，不代表全部来源没有更新。

相对 1838 条 canonical 基线，提议新增 38 条；0 条已知记录有来源/日期补记，0 条有官方元数据差异需审，0 条身份冲突待核对。

全部 raw ID、出处 hash 和时间见 raw-source-id-reconciliation.jsonl。可应用清单见 integration-proposal.json；该清单尚未应用，保留所有旧 first_seen、科学字段、审核和发表状态。

失败或范围限制：
- s2-citations: ValueError: BoundedSourceTraversal: source reached the 180-second attempt window; successful responses retained; unvisited coverage is unknown.
- s2-authors: ValueError: BoundedSourceTraversal: source reached the 180-second attempt window; successful responses retained; unvisited coverage is unknown.
- hf-daily: {'2026-11-10': 'not_ready: HTTPError: 400 Client Error: Bad Request for url: https://huggingface.co/api/daily_papers?date=2026-11-10'}

0 付费调用；未运行 judge、summarize 或 evaluate；未修改 production、commit、push 或 GitHub。
