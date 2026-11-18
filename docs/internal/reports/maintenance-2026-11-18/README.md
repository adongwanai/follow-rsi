# 2026-11-18 维护与上线回执

11/16–18 三期、W46 与历史回顾已通过 PR #139 合并并真实上线。Pages 对应提交为 `9f62739a91bc446ef8ed0be7e595955d09ea6093`；[部署运行](https://github.com/adongwanai/follow-rsi/actions/runs/44227288937)和 [main 测试](https://github.com/adongwanai/follow-rsi/actions/runs/44227288958)均成功。2026-11-18T03:02:09.663331+00:00 对 26 个真实 URL 逐字节核验，全数匹配。当前回执记录出版完成后的实际状态，归档本回执的后续 PR 及最终开放 PR 数见 [issue #60](https://github.com/adongwanai/follow-rsi/issues/60)。

## 已发布内容

| 页面 | 实际内容与日期边界 |
| --- | --- |
| [11/16 日报](https://adongwanai.github.io/follow-rsi/daily/2026-11-16.html) | 7 篇论文；HF 推荐日或其他来源窗口为 11/16，`reviewed_on=2026-11-18`。MIRIX 为旧发现首次正式出版，不能计作新增 canonical。 |
| [11/17 简报](https://adongwanai.github.io/follow-rsi/daily/2026-11-17.html) | 0 篇新增论文；完整 HF 榜单 41 篇均排除，注明延迟审核。 |
| [11/18 简报](https://adongwanai.github.io/follow-rsi/daily/2026-11-18.html) | 0 篇新增论文；HF 尚未就绪，available_through=11/17，逐路说明采集及不完整覆盖。 |
| [W46](https://adongwanai.github.io/follow-rsi/weekly/2026-W46.html) | 12 篇当周论文、32 条历史条目；历史条目含既有 feed 重叠，不能全部称为首次公开。 |
| [历史回顾](https://adongwanai.github.io/follow-rsi/recaps/2026-11-16--2026-11-18.html) | 33 篇；区间是审核归档区间，原发表日逐项保留，不是 W47 周刊或当日新论文。 |

[线上逐 URL 回执](publication-final/live-verification.json)覆盖三期 HTML/JSON、日报与周刊归档、W46、回顾、latest.json、Atom、status.json、首页与 data.js、中英文 README，以及旧刊/撤回保护页。latest 有 135 个条目，Atom 有 24 个条目，状态简报有实质摘要。10/27 撤回与创刊回顾均保留。

## 发现与审查

全部 12 路启用来源均实际尝试，原始响应和时间见 [来源整合](source-intake/README.md)、[独立核验](source-integration-crosscheck.json)及原始响应索引。11/18 HF not_ready 后继续复抓 11/17 全榜 41、11/16 全榜 40（旧快照 38，晚到 2）、11/15 空榜 0；完整成员与推荐日零漏项。3 路 arXiv 成功且本窗口为 0；5 路 RSS 的窗口数量依次为 Sakana 5、METR 6、OpenAI 47、DeepMind 7、Weco 0；GitHub 13 库均尝试，release 窗口 0。Semantic Scholar citations 窗口出现 277 次 / 246 个 ID，46 次请求中 15 次 429，180 秒截止；authors 身份查询成功但论文遍历 6 次 429，不能称完整覆盖。

严格来源窗口 423 次出现 / 388 个 ID，其中新 122 个；另恢复 7 个历史 issue 候选，共新增 129 个 canonical（110 篇论文、19 篇公告）：6 accept、6 backlog、112 reject、5 defer。三轮来源/身份、Harness 范围、独立正例/边界复核均保留原文与哈希。新增条目的 12 项纳入分为 6 项日报与 6 项历史补录，不能与历史恢复混算。

另落实历史 19 项 backlog、10 项 reject。原 92 项未统一写成 defer：56 编辑待办、14 有界初筛、8 已入目录、3 工件缺证、7 范围缺证、3 外部访问阻塞、1 后续反证，均保留旧判断和恢复入口。

[最终账本 post-review-v4](backlog-audit/post-review-v4/summary.json)覆盖 9,052 个稳定 ID、2,222 个 canonical、4,844 个当前原始出现 / 4,572 个原始 ID。canonical 分桶为 1,168 正式/目录、913 可复用范围意见、58 待证、56 编辑待办、14 有界初筛、13 外部来源阻塞；每项均有原因及后续动作。41 个旧模型错误及 2,096 个版本任务保留。版本更新仅完成身份及部分内容读回的不能冒称完整复核或正式采用。

177 次 apply 对应 175 个唯一 ID；两条公告的旧 #134 决定完整保留在 review_history，当前决定来自 #135，因此 #134 是 13 个当前决定 + 2 个历史决定。2,222 条记录的 first_seen 与 apply 前 source_hash 均保持；来源采集阶段 3 条推荐日补记与哈希变化另有明确回执。EGE 的旧 #111 科学批准、11/12 原刊对象不重绑，11/16 推荐日只作 metadata 记录。RSIHub、HarnessDev、Aspire、S³Gym 分类与路线、21 份旧刊 JSON 字节均保持。

## PR 与 issue 处置

以下合并均核对真实同仓 head、CI、owner 和 merge commit；操作依据持续授权，不能解释为人工逐篇阅读。

| PR | 审定 head | merge commit | owner |
| --- | --- | --- | --- |
| [#118](https://github.com/adongwanai/follow-rsi/pull/118) | `1abd366c9573144dbc8e6f8718adfcbabfed5267` | `1208955ae0ae4c8993860c141c933c864fb0b808` | adongwanai |
| [#134](https://github.com/adongwanai/follow-rsi/pull/134) | `31e46a809ca2f542502d5e7174b5fade803e52a0` | `e6c3b8a7afd0810e968aed41d4ca1621b59bd599` | adongwanai |
| [#135](https://github.com/adongwanai/follow-rsi/pull/135) | `46dfa83f0b95a91676df947e2e02491e33eed28d` | `c9f8f941317cfbdf72d83820e2d344cdb6ef614b` | adongwanai |
| [#136](https://github.com/adongwanai/follow-rsi/pull/136) | `687fe3cd9cf27678852efe7399a41e9885d244a5` | `5e5314680d18e56549f595f07aa4f91026bf1cef` | adongwanai |
| [#137](https://github.com/adongwanai/follow-rsi/pull/137) | `37edf3deb548b3a3659d9867218f1a84436bc6e2` | `1a94dd477f836246dc703894749bf7e572410c27` | adongwanai |
| [#138](https://github.com/adongwanai/follow-rsi/pull/138) | `0baec881ecc46e095e3cc53d6de3f21cb2fa28d9` | `908dc6447039d175bcc9745505b1894a7ee3dbcd` | adongwanai |
| [#139](https://github.com/adongwanai/follow-rsi/pull/139) | `c44ebb9544880836343d9e509c3a72ab330b54f9` | `9f62739a91bc446ef8ed0be7e595955d09ea6093` | adongwanai |

出版后开放 PR 为 0。已根据独立逐项证据关闭 13 个 issue：7 个排除（#120、#121、#122、#125、#129、#130、#132），6 个出版完成（#123、#124、#126、#127、#131、#133）。4 个保留项 #115、#116、#119、#128 已写入本日具体待补理由。真实 comment URL、关闭状态和时间见 [逐项操作回执](publication-final/issue-actions.json)，最新读取的远端快照见 [运行状态](publication-final/operational-state.json)。

剩余 9 个 issue：[#19](https://github.com/adongwanai/follow-rsi/issues/19), [#20](https://github.com/adongwanai/follow-rsi/issues/20), [#23](https://github.com/adongwanai/follow-rsi/issues/23), [#30](https://github.com/adongwanai/follow-rsi/issues/30), [#60](https://github.com/adongwanai/follow-rsi/issues/60), [#115](https://github.com/adongwanai/follow-rsi/issues/115), [#116](https://github.com/adongwanai/follow-rsi/issues/116), [#119](https://github.com/adongwanai/follow-rsi/issues/119), [#128](https://github.com/adongwanai/follow-rsi/issues/128)。#19、#20、#23、#30、#119、#128 分别保留行为工件/补丁/验收/跨任务复用证据缺口；#115、#116 仍需完整 v2 版本与数字独立审查，保留 v1；#60 汇总逐项证据、外部来源阻塞和编辑待办。没有把编辑待办或未完成版本审查说成外部故障。

## 验证及费用边界

完整本地测试 434 passed；新增回顾标签和延迟 intro 的回归检查通过；最终 catalog 17 项通过。日期审核校验使用精确合并的出版前输入，全部通过；生产回顾已生成后不可把窗口变化误作日期失败，详见 [日期校验](publication-final/date-validation.json)。602 个生成产物连续构建字节一致，以 [v2 构建回执](publication-final/build-idempotence-v2.json)为准。工程测试不代表质量评测或实验复现，范围复审也未冒称全部实验数字复算。

全局历史评测仍未完成，recall=0.892857，阈值 0.90；真实告警、错误和反证全部保留。依 owner 11/05 更新后的规则，该告警不单独阻止完成逐项校验的内容和实质简报。三个 workflow feed-daily、feed-eval、feed-publish 均保持 disabled_manually。

本轮新增付费生成请求 0、token 0、usage 日志 0 行。已读 11/02 费用审计；起止余额查询均 HTTP 200，观测窗口内余额减少 CNY 0.01。余额差不是本任务发票，不能将其他账户活动归因本任务；历史“100 多元”仍不能用缺失日志推算。私有余额值未提交；公开证据见 [起始边界](usage-boundary-start.json)与 [结束边界](usage-boundary-end.json)。5 元停止线不变，单请求仍可能越过停止值。

`generation-receipt.json`、独立审查和最终账本中的 `online_verified=false` 等字段是各自冻结时的真实出版前状态，未回写伪造；本页所列实际 Pages 与线上 response 哈希回执补足后续上线证据。
