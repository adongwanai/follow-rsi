# 2026-11-04 免费来源采集

全部 12 路启用来源已真实尝试。正常 6 路，HF 榜单未就绪 1 路，失败/部分失败 5 路。

来源记录 102 条，稳定 ID 去重 102 条；对运行前 1351 条 canonical，新增 ID 51 个，已有 ID 待补 HF 推荐日期 2 个。

| 来源 | 状态 | 原始记录 | 唯一 ID | HTTP 请求 | 原因或限制 |
| --- | --- | ---: | ---: | ---: | --- |
| arxiv-harness | 失败/部分失败 | 0 | 0 | 1 | ReadTimeout: HTTPSConnectionPool(host='export.arxiv.org', port=443): Read timed out. (read timeout=45) |
| arxiv-rsi | 失败/部分失败 | 0 | 0 | 1 | HTTPError: 429 Client Error: Unknown Error |
| arxiv-adjacent | 失败/部分失败 | 0 | 0 | 1 | ReadTimeout: HTTPSConnectionPool(host='export.arxiv.org', port=443): Read timed out. (read timeout=45) |
| s2-citations | 失败/部分失败 | 7 | 7 | 14 | HTTPError: 429 Client Error: ；保留 2 个成功分页 |
| s2-authors | 失败/部分失败 | 0 | 0 | 11 | HTTPError: 429 Client Error:  |
| hf-daily | 榜单未就绪 | 45 | 45 | 2 | {'2026-11-04': 'not_ready: HTTPError: 400 Client Error: Bad Request |
| rss-sakana | 正常 | 5 | 5 | 1 | — |
| rss-metr | 正常 | 1 | 1 | 1 | — |
| rss-openai | 正常 | 39 | 39 | 1 | — |
| rss-deepmind | 正常 | 5 | 5 | 1 | — |
| rss-weco | 正常 | 0 | 0 | 1 | — |
| github-releases | 正常 | 0 | 0 | 13 | — |

## HF 榜单与增量

今天 2026-11-04 状态 `not_ready`；API 明确开放至 2026-11-03。实际抓取 {'2026-11-03': 45}，全量保留成员，未进行关键词丢弃。

完整题目、原摘要、新 ID 与待补 membership 见 `source-hf-reconciliation.json`。推荐日期不作为论文原发表日或版本日期。

## 内容变化与复核边界

6 个已有 ID 的本次来源标题/摘要与 canonical 有差异；1 个 ID 与昨日同来源观察有文本差异。差异可能来自来源覆盖和格式，尚未确认为科学内容变化；不会因此自动覆盖摘要、日期或人工结论。

已存在条目仅产生来源和推荐归期的补记建议。Intake 保留已存在 first_seen 和 review，原规范日期保存在 inventory；源记录中的日期仅是该来源观测。

## 可恢复产物

逐来源观察：`data/feed/intake/2026-11-04/source-records.jsonl`；逐 ID 清单：`data/feed/intake/2026-11-04/inventory.json`。

原始 HTTP 响应及时间/哈希回执：`build/maintenance-2026-11-04/network`；单源检查点：`build/maintenance-2026-11-04/source-results`。

本次验证 48 次 HTTP 回执，所有已保存返回体哈希吻合。S2 匿名模式，实际最小请求间隔 3.105449 秒；最大连续 429 请求 6 次（首次加至多 5 次重试）。

没有模型审核、摘要、评测或付费调用；没有 GitHub 写入、accept、发布或生产 canonical/state 修改。范围筛查与人工审核由主任务继续完成。
