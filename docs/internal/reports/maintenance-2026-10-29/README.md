# 2026-10-29 维护与三轮审核

今天 HF 推荐榜的 8 篇全部核对，**0 篇建议纳入 Harness 自进化专题**。前期候选另有 4 篇建议纳入、2 篇争议待定；它们不是 10-29 新推荐。没有发布今天的日报或 Atom 条目，全部正式队列决定保持 `defer`。

## 审查范围与限制

本轮完成范围判定的三轮审查共 66 篇：10-29 HF 8 篇、10-28 HF 50 篇、额外来源补录 8 篇。第一轮逐篇看原摘要并核对 arXiv 身份；第二轮使用仓库配置的 DeepSeek 做独立分类、闸门与数字护栏；第三轮独立反向复审并对疑似项定向查正文。原始轮次结论分别保留，不能把三轮一致性称为 owner 人工批准，也不把方法章节定向阅读称为完成四项全文证据审计。

- 今日榜中 TAO 是固定调度框架，CausGround 复用因果知识，未建立自身 Harness 程序的持久改写。
- OmniSpectra 首发 2026-01-21、Sensorimotor Alignment 首发 2026-10-22；HF 的 10-23 是二者的版本日期。昨日榜另外发现 7 处同类日期差异。
- GEPA-Curator 摘要闸门保留 borderline，正文复审建议纳入；保留分歧，需要 owner 显式裁决。
- OmniBrain-0 摘要模型判断为 embodied；正文有冻结参数下修订、保留 reminder policy 的路径，转为 coevolution 争议候选。
- AdaPRA 模型闸门曾通过，但在线 stores 按任务隔离，离线 seed 的复用不能直接证明在线更新跨任务保留，已降为 borderline。
- Your Policy Is Secretly a Harness 研究接口与参数适配理论，不据此计作 Harness RSI 专项理论。

14 篇疑似或边界论文定向阅读了正文方法章节，41 段引文已逐段与保存的原文核对。**完整四项证据卡审计完成数仍为 0**。

轮次记录：[第一轮今日](round1-hf.md) · [第一轮昨日](round1-backlog-2026-10-28.md) · [第一轮其他来源](round1-other-backlog.md) · [第二轮 66 份模型输出](round2-results/) · [第三轮今日](round3-independent.md) · [第三轮积压](round3-backlog.md) · [原文摘录](verified-excerpts.json)。原始网页保存在本地忽略目录；本审核包提供公开来源 URL、引文和 SHA-256，见 [来源清单](source-manifest.json)。

## 优先待审的六篇

| 候选 | 新闻/来源日期 | 多轮建议 | 正式决定 |
| --- | --- | --- | --- |
| [The Trinity](https://arxiv.org/abs/2610.36077) | 2026-10-28（HF推荐） | 建议纳入 | defer |
| [RuHarness](https://arxiv.org/abs/2610.36826) | 2026-10-27（原始来源） | 建议纳入 | defer |
| [GEPA-Curator](https://arxiv.org/abs/2610.37651) | 2026-10-27（原始来源） | 正文支持纳入，摘要闸门未通过 | defer |
| [Skill Dreaming](https://arxiv.org/abs/2610.36188) | 2026-10-26（原始来源） | 建议纳入 | defer |
| [OmniBrain-0](https://arxiv.org/abs/2610.36013) | 2026-10-26（原始来源） | 有分歧，需 owner 确认 | defer |
| [AdaPRA](https://arxiv.org/abs/2610.33245) | 2026-10-28（HF推荐） | 有分歧，需 owner 确认 | defer |

今天的正式文件是 [review/daily/2026-10-29.yaml](../../../../review/daily/2026-10-29.yaml)。审核队列包含顺延历史条目，不等于“今日新增”：32 篇论文中 2 篇是 10-28 推荐、30 篇为 backlog；另有 62 条实验室消息待审。94 个决定全部为 defer，自动摘要和 scope 建议不会批准出版。旧 PR #4 中 85 个未决条目的可用备注与决定已按新来源 hash 规则顺延，身份或内容变化的继续待审。定时任务随后创建的旧流程 PR #5 有 103 条 pending、没有 owner 决定或备注；全部 ID 已保留，[逐条对账](superseded-review-reconciliation.json)列明其现状。本轮待审包集中在 PR #3，旧流程审核单由本包取代。

## 实验室消息补审

本期窗口还发现 5 条实验室消息。两名独立审查者读取全部官方正文，另由配置的 DeepSeek 独立运行 Harness 闸门；三轮均建议排除。它们分别涉及选举分析、企业合作、组织经济、法律产品应用和模型发布，正文没有建立反馈修改并跨任务保留自身 Harness 的完整机制。此判断只针对本次公告的证据。

[第一轮](lab-round1.md) · [第二轮原始输出](lab-round2-results/) · [第三轮](lab-round3.md) · [核对过的原文摘录](lab-verified-excerpts.json)。这 5 条在正式审核单中仍为 `defer`，没有代替 owner 作 reject 决定。

Sakana 公告的 RSS 时间戳为 10-29 15:00 UTC，网页显示日本时间 10-30 00:00；两者一致，但晚于本次 10:34 UTC 抓取。原日期保留，标为来源时间待核。另已修复 6 个 Sakana 相对链接，保持原稳定 ID 和审核记录；未来抓取的绝对 URL 可正确去重，见 [修复清单](rss-link-repairs.json)。

## 来源与历史积压

10-29 18:30（北京时间）再次核对 HF 当日榜：仍为 8 篇，标题和摘要无变化，见 [最终抓取快照](hf-final-snapshot.json)。

全部 12 路启用来源实际尝试，11 路成功；S2 authors 在重试后仍为 HTTP 429。S2 citations 返回 1,630 条引用命中（含重复引用）；HF 2 天原始列表共 58 篇，宽关键词预筛保留 28 条。RSS 返回实验室帖子，不能把“抓到了”算作 Harness 新闻。arXiv 10-28—29 三路提交日期检索返回 0；这只是该查询窗的结果。

合并与去重后本地保存 1112 个唯一记录，保留远端 main 的全部 387 个唯一 ID。本轮新增 685 个唯一记录；其中 616 条历史发现或实验室消息尚未完成范围审查，逐条记录于 [deferred-discovery.json](deferred-discovery.json)，不进入今日出版。S2 的未来书目日期原样保留并暂缓，不伪造为今天。

## 维护修复与验证

1. HF 版本日期不再冒充首次发表：保留原 reported date，使用同 ID 的 arXiv 元数据核对日期和版本；失败明确记录并保持未知。
2. 真正被当日 HF 新推荐的旧回填条目可重新进入待审，历史列表重放不放行，已发表条目不重复发布。
3. 抓取快照使用仓库相对路径，避免把本机 checkout 名称写入版本化产物。

最终 296 项 pytest 通过，104 篇论文和 9 条路线校验通过。构建幂等与作者手写 README 保护见 [验证记录](validation.json)。data/papers.yaml、owner 的原始复审结论与 8 张 SVG/生成脚本不变。

既有 45 样本闸门 recall 0.8571 仍低于 0.90，不能写成已过发布阈值。PR #3 的旧 trusted-main 评测身份问题也没有借本轮改标签或放宽校验来消除。feed-publish 工作流仍手动禁用，待 owner 审核修复与内容。

北京时间每天 08:00 的本对话自动维护已创建并启用；它每日发现、核查、准备待审结果，仍保留人工审核后发布的边界。
