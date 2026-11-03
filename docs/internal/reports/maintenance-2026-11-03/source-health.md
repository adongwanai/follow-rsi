# 2026-11-03 免费信源维护

12 路已启用来源全部实际尝试：**正常 6，HF 当日榜未就绪 1，抓取失败或部分失败 5**。采集开始 2026-11-03T02:06:25.854276+00:00。

保留 **164 条来源记录 / 156 个稳定 ID / 8 条新增**。S2 从 7 个成功引用分页离线恢复 113 条记录（105 个 ID），随后限流仍记为整源未完成；另有 1 个作者种子元数据响应保留，不冒充作者论文页。

| 来源 | 状态 | 保留条数 | HTTP 请求 | 限制 |
| --- | --- | ---: | ---: | --- |
| arxiv-harness | 失败 | 0 | 1 | HTTP 429，完整请求和错误见 JSON |
| arxiv-rsi | 失败 | 0 | 1 | HTTP 429，完整请求和错误见 JSON |
| arxiv-adjacent | 失败 | 0 | 1 | HTTP 429，完整请求和错误见 JSON |
| s2-citations | 部分失败 | 113 | 20 | HTTP 429，完整请求和错误见 JSON；成功 7 页已恢复，遍历未完成 |
| s2-authors | 失败 | 0 | 7 | HTTP 429，完整请求和错误见 JSON；1 个种子元数据 200，未完成作者论文采集 |
| hf-daily | 当日榜未就绪 | 0 | 1 | HTTP 400，可用至 11/2 |
| rss-sakana | 正常 | 5 | 1 | — |
| rss-metr | 正常 | 1 | 1 | — |
| rss-openai | 正常 | 41 | 1 | — |
| rss-deepmind | 正常 | 4 | 1 | — |
| rss-weco | 正常 | 0 | 1 | — |
| github-releases | 正常 | 0 | 13 | — |

HF 请求 11/3 榜，API 明确只开放至 11/2。**这是榜未就绪，不是“今日无合格论文”**；未借用前日推荐。原发表/版本日期不从 HF publishedAt 或 S2 单一日期推定。

8 条新增均有独立的可恢复处理状态：6 条官方 RSS 摘要目前不支持按 Harness 收录；Operon-S1 的 S2 摘要更像决策模型训练，需原文确认；TSFLab 的 workbench 资源维护和 Harness 修改边界待原文工件。没有最终 accept/reject，也没有发表新文章。

新增逐项意见与最小补证：`docs/internal/reports/maintenance-2026-11-03/new-source-screen.json`。全文未读项均明确注明，只对返回摘要中的内容做初筛。

候选队列：`build/maintenance-2026-11-03/candidate-inventory.json`；所有来源变体：`build/maintenance-2026-11-03/data/feed/source-records.jsonl`。逐路检查点与 HTTP 回执在 `source-results/` 和 `network/`，完整 URL 仅放 JSON。

本轮未执行 arXiv 补全文献日期：原生完整源结果无 pending 项；S2 部分恢复后才出现的待补元数据 ID 记录在 JSON，未再发起抓取。未知日期仍未知。

只写隔离 root 与内部报告，生产 canonical/state/日报未由本脚本修改。模型调用 0，GitHub 写入 0，新增发布 0。
