# 2026-11-23 免费来源快照

生成时间 2026-11-23T08:06:34.486752+00:00；12 路中 12 路已结束。本报告只涵盖实际请求得到的响应，失败源未覆盖部分保持未知。

| 来源 | 状态 | 全部原始记录 | 窗口内记录 | 请求/HTTP |
|---|---|---:|---:|---|
| arxiv-harness | ok | 15 | 15 | 1 / {'200': 1} |
| arxiv-rsi | ok | 17 | 17 | 1 / {'200': 1} |
| arxiv-adjacent | ok | 2 | 2 | 1 / {'200': 1} |
| s2-citations | partial | 2673 | 262 | 47 / {'200': 28, '429': 19} |
| s2-authors | error | 0 | 0 | 8 / {'200': 2, '429': 6} |
| hf-daily | ok | 152 | 152 | 6 / {'200': 6} |
| rss-sakana | ok | 15 | 9 | 1 / {'200': 1} |
| rss-metr | ok | 263 | 7 | 1 / {'200': 1} |
| rss-openai | ok | 1422 | 49 | 1 / {'200': 1} |
| rss-deepmind | ok | 100 | 7 | 1 / {'200': 1} |
| rss-weco | ok | 13 | 0 | 1 / {'200': 1} |
| github-releases | ok | 12 | 0 | 13 / {'200': 13} |

HF 当日状态：ok；API 给出的 available_through：None。实际成功响应完整榜单及篇数：{'2026-11-23': 13, '2026-11-22': 0, '2026-11-21': 0, '2026-11-20': 50, '2026-11-19': 50, '2026-11-18': 39}。空数组仅说明该次请求返回空榜，不代表全部来源没有更新。

相对 2222 条 canonical 基线，提议新增 234 条；2 条已知记录有来源/日期补记，0 条有官方元数据差异需审，0 条身份冲突待核对。

全部 raw ID、出处 hash 和时间见 raw-source-id-reconciliation.jsonl。可应用清单见 integration-proposal.json；该清单尚未应用，保留所有旧 first_seen、科学字段、审核和发表状态。

失败或范围限制：
- s2-citations: ValueError: BoundedSourceTraversal: source reached the 180-second attempt window; successful responses retained; unvisited coverage is unknown.
- s2-authors: HTTPError: 429 Client Error:  for url: https://api.semanticscholar.org/graph/v1/paper/arXiv:2310.03714?fields=authors

0 付费调用；未运行 judge、summarize 或 evaluate；未修改 production、commit、push 或 GitHub。
