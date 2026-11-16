# 2026-11-16 免费来源快照

生成时间 2026-11-16T00:10:24.167291+00:00；12 路中 12 路已结束。本报告只涵盖实际请求得到的响应，失败源未覆盖部分保持未知。

| 来源 | 状态 | 全部原始记录 | 窗口内记录 | 请求/HTTP |
|---|---|---:|---:|---|
| arxiv-harness | error | 0 | 0 | 1 / {'429': 1} |
| arxiv-rsi | error | 0 | 0 | 1 / {'429': 1} |
| arxiv-adjacent | error | 0 | 0 | 1 / {'429': 1} |
| s2-citations | partial | 1853 | 264 | 40 / {'200': 20, '429': 20} |
| s2-authors | error | 0 | 0 | 25 / {'200': 10, '429': 15} |
| hf-daily | historical_boards_ok_today_not_ready | 34 | 34 | 4 / {'400': 1, '200': 3} |
| rss-sakana | ok | 12 | 1 | 1 / {'200': 1} |
| rss-metr | ok | 256 | 4 | 1 / {'200': 1} |
| rss-openai | ok | 1389 | 39 | 1 / {'200': 1} |
| rss-deepmind | ok | 100 | 8 | 1 / {'200': 1} |
| rss-weco | ok | 13 | 0 | 1 / {'200': 1} |
| github-releases | ok | 12 | 0 | 13 / {'200': 13} |

HF 当日状态：not_ready；API 给出的 available_through：2026-11-13。实际成功响应完整榜单及篇数：{'2026-11-15': 0, '2026-11-14': 0, '2026-11-13': 34}。空数组仅说明该次请求返回空榜，不代表全部来源没有更新。

相对 2090 条 canonical 基线，提议新增 3 条；0 条已知记录有来源/日期补记，0 条有官方元数据差异需审，0 条身份冲突待核对。

全部 raw ID、出处 hash 和时间见 raw-source-id-reconciliation.jsonl。可应用清单见 integration-proposal.json；该清单尚未应用，保留所有旧 first_seen、科学字段、审核和发表状态。

失败或范围限制：
- arxiv-harness: HTTPError: 429 Client Error: Unknown Error for url: https://export.arxiv.org/api/query?search_query=%28%28%28cat%3Acs.AI+OR+cat%3Acs.CL+OR+cat%3Acs.LG+OR+cat%3Acs.MA+OR+cat%3Acs.SE+OR+cat%3Acs.RO+OR+cat%3Acs.NE%29+AND+%28%28ti%3Aharness+AND+%28ti%3Aimprov%2A+OR+abs%3Aimprov%2A+OR+ti%3Aevolv%2A+OR+abs%3Aevolv%2A%29%29+OR+%28ti%3A%22harness+evolution%22+OR+abs%3A%22harness+evolution%22%29+OR+%28ti%3A%22harness+optimization%22+OR+abs%3A%22harness+optimization%22%29+OR+%28ti%3A%22self-evolving+harness%22+OR+abs%3A%22self-evolving+harness%22%29+OR+%28ti%3A%22harness+self-improvement%22+OR+abs%3A%22harness+self-improvement%22%29+OR+%28%28ti%3A%22agent+harness%22+OR+abs%3A%22agent+harness%22%29+AND+%28%28ti%3Aevolv%2A+OR+abs%3Aevolv%2A%29+OR+%28ti%3Aoptimiz%2A+OR+abs%3Aoptimiz%2A%29+OR+%28ti%3A%22self-improv%2A%22+OR+abs%3A%22self-improv%2A%22%29%29%29+OR+%28%28ti%3Ascaffold+OR+abs%3Ascaffold%29+AND+%28ti%3A%22self-improv%2A%22+OR+abs%3A%22self-improv%2A%22%29%29+OR+%28ti%3A%22automated+design+of+agent%2A%22+OR+abs%3A%22automated+design+of+agent%2A%22%29+OR+%28%28ti%3A%22meta-agent%22+OR+abs%3A%22meta-agent%22%29+AND+%28%28ti%3Aevolv%2A+OR+abs%3Aevolv%2A%29+OR+%28ti%3A%22self-improv%2A%22+OR+abs%3A%22self-improv%2A%22%29%29%29%29%29%29+AND+submittedDate%3A%5B202611150000+TO+202611162359%5D&sortBy=submittedDate&sortOrder=descending&start=0&max_results=100
- arxiv-rsi: HTTPError: 429 Client Error: Unknown Error for url: https://export.arxiv.org/api/query?search_query=%28%28%28cat%3Acs.AI+OR+cat%3Acs.CL+OR+cat%3Acs.LG+OR+cat%3Acs.MA+OR+cat%3Acs.SE+OR+cat%3Acs.RO+OR+cat%3Acs.NE%29+AND+%28%28ti%3A%22recursive+self-improvement%22+OR+abs%3A%22recursive+self-improvement%22%29+OR+%28ti%3A%22self-improving+agent%2A%22+OR+abs%3A%22self-improving+agent%2A%22%29+OR+%28ti%3A%22self-evolving+agent%2A%22+OR+abs%3A%22self-evolving+agent%2A%22%29+OR+%28ti%3A%22self-modifying%22+OR+abs%3A%22self-modifying%22%29+OR+%28ti%3A%22G%C3%B6del+machine%22+OR+abs%3A%22G%C3%B6del+machine%22%29+OR+%28ti%3A%22Godel+machine%22+OR+abs%3A%22Godel+machine%22%29+OR+%28%28ti%3A%22open-ended%22+OR+abs%3A%22open-ended%22%29+AND+%28ti%3Aagent+OR+abs%3Aagent%29+AND+%28ti%3A%22self-improv%2A%22+OR+abs%3A%22self-improv%2A%22%29%29%29%29%29+AND+submittedDate%3A%5B202611150000+TO+202611162359%5D&sortBy=submittedDate&sortOrder=descending&start=0&max_results=100
- arxiv-adjacent: HTTPError: 429 Client Error: Unknown Error for url: https://export.arxiv.org/api/query?search_query=%28%28%28cat%3Acs.AI+OR+cat%3Acs.CL+OR+cat%3Acs.LG+OR+cat%3Acs.MA+OR+cat%3Acs.SE+OR+cat%3Acs.RO+OR+cat%3Acs.NE%29+AND+%28%28ti%3A%22skill+evolution%22+OR+abs%3A%22skill+evolution%22%29+OR+%28%28ti%3A%22experience-driven%22+OR+abs%3A%22experience-driven%22%29+AND+%28ti%3Aagent+OR+abs%3Aagent%29%29+OR+%28ti%3A%22automated+AI+research%22+OR+abs%3A%22automated+AI+research%22%29+OR+%28%28ti%3A%22AI+scientist%22+OR+abs%3A%22AI+scientist%22%29+AND+%28ti%3A%22self-improv%2A%22+OR+abs%3A%22self-improv%2A%22%29%29+OR+%28%28ti%3A%22self-play%22+OR+abs%3A%22self-play%22%29+AND+%28ti%3A%22zero+data%22+OR+abs%3A%22zero+data%22%29%29+OR+%28%28ti%3A%22continual+learning%22+OR+abs%3A%22continual+learning%22%29+AND+%28ti%3Aagent+OR+abs%3Aagent%29+AND+%28%28ti%3Aharness+OR+abs%3Aharness%29+OR+%28ti%3Askill+OR+abs%3Askill%29+OR+%28ti%3Amemory+OR+abs%3Amemory%29%29%29%29%29%29+AND+submittedDate%3A%5B202611150000+TO+202611162359%5D&sortBy=submittedDate&sortOrder=descending&start=0&max_results=100
- s2-citations: ValueError: BoundedSourceTraversal: source reached the 180-second attempt window; successful responses retained; unvisited coverage is unknown.
- s2-authors: ValueError: BoundedSourceTraversal: source reached the 180-second attempt window; successful responses retained; unvisited coverage is unknown.
- hf-daily: {'2026-11-16': 'not_ready: HTTPError: 400 Client Error: Bad Request for url: https://huggingface.co/api/daily_papers?date=2026-11-16'}

0 付费调用；未运行 judge、summarize 或 evaluate；未修改 production、commit、push 或 GitHub。
