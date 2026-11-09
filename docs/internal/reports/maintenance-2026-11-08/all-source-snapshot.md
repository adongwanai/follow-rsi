# 2026-11-08 免费来源快照

生成时间 2026-11-08T00:14:04.219492+00:00；12 路中 12 路已结束。本报告只涵盖实际请求得到的响应，失败源未覆盖部分保持未知。

| 来源 | 状态 | 全部原始记录 | 窗口内记录 | 请求/HTTP |
|---|---|---:|---:|---|
| arxiv-harness | error | 0 | 0 | 1 / {'network_error': 1} |
| arxiv-rsi | error | 0 | 0 | 1 / {'network_error': 1} |
| arxiv-adjacent | error | 0 | 0 | 1 / {'429': 1} |
| s2-citations | partial | 2919 | 327 | 62 / {'200': 31, '429': 31} |
| s2-authors | error | 0 | 0 | 7 / {'200': 1, '429': 6} |
| hf-daily | historical_boards_ok_today_not_ready | 32 | 32 | 3 / {'400': 1, '200': 2} |
| rss-sakana | ok | 12 | 4 | 1 / {'200': 1} |
| rss-metr | ok | 256 | 4 | 1 / {'200': 1} |
| rss-openai | ok | 1368 | 46 | 1 / {'200': 1} |
| rss-deepmind | ok | 100 | 5 | 1 / {'200': 1} |
| rss-weco | ok | 13 | 0 | 1 / {'200': 1} |
| github-releases | ok | 12 | 0 | 13 / {'200': 13} |

HF 当日状态：not_ready；API 给出的 available_through：2026-11-06。实际成功响应完整榜单及篇数：{'2026-11-07': 0, '2026-11-06': 32}。空数组仅说明该次请求返回空榜，不代表全部来源没有更新。

相对 1809 条 canonical 基线，提议新增 19 条；9 条已知记录有来源/日期补记，0 条有官方元数据差异需审，0 条身份冲突待核对。

全部 raw ID、出处 hash 和时间见 raw-source-id-reconciliation.jsonl。可应用清单见 integration-proposal.json；该清单尚未应用，保留所有旧 first_seen、科学字段、审核和发表状态。

失败或范围限制：
- arxiv-harness: ReadTimeout: HTTPSConnectionPool(host='export.arxiv.org', port=443): Read timed out. (read timeout=45)
- arxiv-rsi: ReadTimeout: HTTPSConnectionPool(host='export.arxiv.org', port=443): Read timed out. (read timeout=45)
- arxiv-adjacent: HTTPError: 429 Client Error: Too Many Requests for url: https://export.arxiv.org/api/query?search_query=%28%28%28cat%3Acs.AI+OR+cat%3Acs.CL+OR+cat%3Acs.LG+OR+cat%3Acs.MA+OR+cat%3Acs.SE+OR+cat%3Acs.RO+OR+cat%3Acs.NE%29+AND+%28%28ti%3A%22skill+evolution%22+OR+abs%3A%22skill+evolution%22%29+OR+%28%28ti%3A%22experience-driven%22+OR+abs%3A%22experience-driven%22%29+AND+%28ti%3Aagent+OR+abs%3Aagent%29%29+OR+%28ti%3A%22automated+AI+research%22+OR+abs%3A%22automated+AI+research%22%29+OR+%28%28ti%3A%22AI+scientist%22+OR+abs%3A%22AI+scientist%22%29+AND+%28ti%3A%22self-improv%2A%22+OR+abs%3A%22self-improv%2A%22%29%29+OR+%28%28ti%3A%22self-play%22+OR+abs%3A%22self-play%22%29+AND+%28ti%3A%22zero+data%22+OR+abs%3A%22zero+data%22%29%29+OR+%28%28ti%3A%22continual+learning%22+OR+abs%3A%22continual+learning%22%29+AND+%28ti%3Aagent+OR+abs%3Aagent%29+AND+%28%28ti%3Aharness+OR+abs%3Aharness%29+OR+%28ti%3Askill+OR+abs%3Askill%29+OR+%28ti%3Amemory+OR+abs%3Amemory%29%29%29%29%29%29+AND+submittedDate%3A%5B202611070000+TO+202611082359%5D&sortBy=submittedDate&sortOrder=descending&start=0&max_results=100
- s2-citations: BoundedSourceTraversal: anonymous historical citation paging stopped after 62 requests to finish all enabled source attempts for this maintenance; successful pages retained; unvisited pages unknown.
- s2-authors: HTTPError: 429 Client Error:  for url: https://api.semanticscholar.org/graph/v1/paper/arXiv:2310.02304?fields=authors
- hf-daily: {'2026-11-08': 'not_ready: HTTPError: 400 Client Error: Bad Request for url: https://huggingface.co/api/daily_papers?date=2026-11-08'}

0 付费调用；未运行 judge、summarize 或 evaluate；未修改 production、commit、push 或 GitHub。
