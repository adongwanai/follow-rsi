# 2026-10-31 S2 新增来源记账

仅核对来源数量和摘要可用性，未执行付费模型、范围分类、正文深审或 canonical 修改。全部正式决定 defer。

S2 返回 1454 次命中，去重为 654 个 ID；相对 1139 条冻结基线新增 27 个，与主审 37 条队列重叠 6 个，另外 21 个需保留独立待审状态。21 条中 20 条有接口摘要，1 条无摘要。接口摘要存在不等于官方身份/原文已核验。

缺摘要的 `s2:33e84e388ed32372fb1a7fbbc251f96f3375a29a` 来源日期为 2026-12-01，同时收到的 metadata_pending=false；需核对正式线上发表日期与期刊期次日期，不能当作今日新论文，也不能伪造为模型 API 错误。

| ID | 来源发表日期 | 摘要字符数 | 状态 |
| --- | --- | ---: | --- |
| arxiv:2610.37739 | 2026-10-27 | 1503 | collected_scope_review_pending |
| arxiv:2610.37935 | 2026-10-27 | 1719 | collected_scope_review_pending |
| arxiv:2610.38120 | 2026-10-28 | 1380 | collected_scope_review_pending |
| arxiv:2610.38329 | 2026-10-28 | 1393 | collected_scope_review_pending |
| arxiv:2610.38391 | 2026-10-28 | 1285 | collected_scope_review_pending |
| arxiv:2610.38407 | 2026-10-28 | 1403 | collected_scope_review_pending |
| arxiv:2610.38468 | 2026-10-28 | 1566 | collected_scope_review_pending |
| arxiv:2610.38946 | 2026-10-28 | 1857 | collected_scope_review_pending |
| arxiv:2610.38960 | 2026-10-28 | 1153 | collected_scope_review_pending |
| arxiv:2610.39158 | 2026-10-29 | 1700 | collected_scope_review_pending |
| arxiv:2610.39180 | 2026-10-29 | 1192 | collected_scope_review_pending |
| arxiv:2610.39352 | 2026-10-29 | 1503 | collected_scope_review_pending |
| arxiv:2610.39380 | 2026-10-29 | 1382 | collected_scope_review_pending |
| arxiv:2610.39813 | 2026-10-29 | 1329 | collected_scope_review_pending |
| arxiv:2610.40227 | 2026-10-29 | 1566 | collected_scope_review_pending |
| arxiv:2610.40276 | 2026-10-29 | 1333 | collected_scope_review_pending |
| arxiv:2610.40490 | 2026-10-29 | 1802 | collected_scope_review_pending |
| arxiv:2610.40560 | 2026-10-29 | 1039 | collected_scope_review_pending |
| arxiv:2610.40565 | 2026-10-29 | 1804 | collected_scope_review_pending |
| s2:33e84e388ed32372fb1a7fbbc251f96f3375a29a | 2026-12-01 | 0 | source_metadata_pending |
| s2:f06ab06359d7364ba2fb78e1142d10ed98167899 | 2026-10-27 | 1822 | collected_scope_review_pending |

完整标题、来源链接、哈希和待补原因见 s2-additional-intake-audit.json。21 条均未完成本轮来源身份/范围复核，余额暂停仅是批次状态。
