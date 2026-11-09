# 2026-11-09 来源采集交付

采集实际时间：2026-11-09T04:39:01.591505+00:00 至 2026-11-09T04:43:48.943345+00:00；补充8篇官方abs与HTML全文最迟于04:45 UTC完成。

## 可应用增量

冻结canonical 1830条（b12e626）；新增8篇候选（HF 7，S2 1），既有5条仅补来源/推荐日集合，其中1条新增HF推荐日。不接受、不发布；正式决定仍为defer。

- integration-proposal.json：安全增量。旧source_hash仅记录观察值；主任务恢复有效旧快照后按first_seen及集合并集核对，不覆盖科学字段或旧决定。
- candidate-records.jsonl：404条窗口内去重候选。
- hf-board-reconciliation.json：11/09完整8条，11/08与11/07空榜；11/06复抓仍32条，未增晚到成员。
- all-source-snapshot.json / .md：每路起止、计数、HTTP和缺口。
- raw-source-id-reconciliation.jsonl：全部6542次原始记录出现的稳定ID和凭据。
- official-metadata/records.json、scope-fulltexts/*.txt + *.receipt.json：8篇新候选身份、版本、正文与哈希。
- intake-qa.json：边界检查和S2限速实测偏差。

## 范围与故障

- 三路arXiv查询均429；官方Atom元数据请求也429，已转官方abs核对8篇身份日期。
- S2 citations：50个200成功响应、7个429；4741原始记录出现，400窗口出现/317唯一ID。180秒有界遍历后结束，未覆盖部分未知。
- S2 authors：1个作者元数据响应200、6个429（初次+5次重试），未取得作者论文页。
- HF：4次成功请求，全40个原始成员参加对账；7篇新发现与1篇已知论文形成11/09的8篇完整榜。
- RSS：5路成功，窗口内51次记录出现；GitHub13个仓库成功请求，窗口内release为0。
- S2匿名配置间隔3.1秒；墙钟receipt最短2.975332秒，缺dispatch monotonic无法解释偏差，不能声称实测全部≥3秒。已告知主任务。
- S2有4条源报日期晚于今天，原样留在raw审计，未进入今日窗口或入库提案。

0付费模型调用，未写生产数据、未提交或推送。这里的源码/身份核对不是论文实验复现。
