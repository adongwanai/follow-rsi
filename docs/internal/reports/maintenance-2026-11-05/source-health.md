# 2026-11-05 免费来源采集

全部 12 路启用来源已真实尝试。正常 11 路，HF 榜单未就绪 0 路，失败/部分失败 1 路。

来源记录 1552 条，窗口合格 intake 1549 条，稳定 ID 去重 764 条；对运行前 1598 条 canonical，新增 ID 138 个，已有 ID 待补 HF 推荐日期 2 个。

| 来源 | 状态 | 原始记录 | 唯一 ID | HTTP 请求 | 原因或限制 |
| --- | --- | ---: | ---: | ---: | --- |
| arxiv-harness | 正常 | 1 | 1 | 1 | — |
| arxiv-rsi | 正常 | 2 | 2 | 1 | — |
| arxiv-adjacent | 正常 | 1 | 1 | 1 | — |
| s2-citations | 正常 | 1399 | 627 | 157 | — |
| s2-authors | 失败/部分失败 | 0 | 0 | 7 | HTTPError: 429 Client Error:  |
| hf-daily | 正常 | 100 | 100 | 3 | — |
| rss-sakana | 正常 | 4 | 4 | 1 | — |
| rss-metr | 正常 | 0 | 0 | 1 | — |
| rss-openai | 正常 | 41 | 41 | 1 | — |
| rss-deepmind | 正常 | 4 | 4 | 1 | — |
| rss-weco | 正常 | 0 | 0 | 1 | — |
| github-releases | 正常 | 0 | 0 | 13 | — |

## HF 榜单与增量

今天 2026-11-05 状态 `ok`；本次最新已开放榜单 2026-11-05，API available_through 响应字段为 None（成功响应无此错误字段）。实际抓取 {'2026-11-03': 45, '2026-11-04': 50, '2026-11-05': 5}，全量保留成员，未进行关键词丢弃。

新增分组：{'recent_arxiv_discovery': 4, 'known_provenance_only': 626, 's2_historical_backfill': 76, 'prior_hf_board_backfill': 48, 'today_hf_discovery': 5, 'recent_news_or_release_discovery': 5}。S2 新身份82个完整保留30天窗口，其中6个与HF交叉重合，其余76个单列历史回补；不重置发表日期、不混入HF归期。

完整题目、原摘要、新 ID 与待补 membership 见 `source-hf-reconciliation.json`。推荐日期不作为论文原发表日或版本日期。

## 内容变化与复核边界

37 个已有 ID 的本次来源标题/摘要与 canonical 有差异；0 个 ID 与昨日同来源观察有文本差异。差异可能来自来源覆盖和格式，尚未确认为科学内容变化；不会因此自动覆盖摘要、日期或人工结论。

已存在条目仅产生来源和推荐归期的补记建议。Intake 保留已存在 first_seen 和 review，原规范日期保存在 inventory；源记录中的日期仅是该来源观测。

## 可恢复产物

逐来源观察：`data/feed/intake/2026-11-05/source-records.jsonl`；逐 ID 清单：`data/feed/intake/2026-11-05/inventory.json`。

原始 HTTP 响应及时间/哈希回执：`build/maintenance-2026-11-05/network`；单源检查点：`build/maintenance-2026-11-05/source-results`。

本次验证 188 次 HTTP 回执，所有已保存返回体哈希吻合。S2 anonymous 模式，实际最小请求间隔 3.097173 秒；最大连续 429 请求 6 次（首次加至多 5 次重试）。

没有模型审核、摘要、评测或付费调用；没有 GitHub 写入、accept、发布或生产 canonical/state 修改。范围筛查与人工审核由主任务继续完成。

## 官方元数据补充完成

新论文规范化建议133项：原HF/API文件57项保持完整，S2独立文件76项（75 arXiv + 1 PRISM出版社）。57+76覆盖全部133个新增paper，另5条news保持来源记录；两个文件ID无重合，first_seen均与intake实际观察一致。S2条目不添加HF刊期。

按主审/独立审核点名的45篇官方HTML已保存（原批12篇、S2批33篇），正文审核仍由各审核者完成。S2 arXiv元数据及正文的108次请求均200，实际最小请求间隔3.083343秒，名义设置3.1秒，满足arXiv 3秒下限；原始时刻和名义间隔偏差如实保留。后25篇正文按前次响应完成后再等3.1秒执行。

PRISM官方DOI/标题/发表日已核实，version=0表示unknown，updated为空，未把网页modified时间当论文修订。全部新增paper都具备可供主任务应用的官方元数据建议，未改变既有canonical科学字段或人工决定。
