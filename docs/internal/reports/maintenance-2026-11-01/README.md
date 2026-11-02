# 2026-11-01 维护记录

本次已完成全部 12 路来源尝试、旧审核单顺延修复、当日待审单生成和本地验证。**成功采集部分新增去重条目为 0；HF 当日榜为空；未发布新日报。** S2 两路失败，不能由此推断所有来源今天都没有相关论文。规范库仍为 1,206 条，原始事实、owner 决定和既有模型结果均保留。

## 实际采集

采集于 **UTC 13:24:47–13:34:58（北京时间 21:24:47–21:34:58）** 运行。这是实际观测时间，不冒充早上 08:00 已完成。本地 heartbeat 配置是每天北京时间 08:00；GitHub 的采集、审核 cron 是另外的计划，今日实际触发延迟及原始运行链接见[流水线审计](pipeline-audit.md)。

HF **2026-11-01、2026-10-31** 均返回 HTTP 200、空列表。只记录“本次接口为空”，不改写为抓取失败，也不把历史推荐或 RSS 旧公告算作今日推荐。原论文发表日、版本日与 HF 推荐日继续分开。

| 来源 | 返回或预筛命中 | 状态 |
| --- | ---: | --- |
| HF Daily Papers | 0 | HTTP 200；两天均为空 |
| arXiv Harness | 0 | 请求成功、空结果 |
| arXiv RSI | 0 | 请求成功、空结果 |
| arXiv adjacent | 0 | 请求成功、空结果 |
| Semantic Scholar citations | 0（未完成整路） | 分页时 TLS EOF，中断；不能当作零篇结果 |
| Semantic Scholar authors | 0（未完成整路） | 429，按既有指数退避策略重试后失败 |
| RSS Sakana | 6 | 成功；arXiv 元数据补全成功 |
| RSS METR | 2 | 成功；arXiv 元数据补全成功 |
| RSS OpenAI | 40 | 成功 |
| RSS DeepMind | 3 | 成功 |
| RSS Weco | 0 | 成功、空结果 |
| GitHub releases | 0 | 成功、空结果 |

表内数量不是 Harness 收录量，也不是新增去重数。10 路主请求成功、2 路失败。S2 本轮是匿名模式，最小请求间隔 3.1 秒；没有可用 S2 key 的事实由 `state.json` 记录，未输出任何密钥。付费模型在前次 HTTP 402 后仍按 owner 指示暂停，本次付费模型调用为 0。

[逐路时间、数量与错误](source-attempts.json) · [来源健康](source-health.json) · [去重及原字段保护](integration.json)

## 审核单和顺延修复

[远端 PR #13](https://github.com/adongwanai/follow-rsi/pull/13) 原有 144 条记录全部是遗留 `pending`，owner 检查按规则拒绝；另两项 CI 是等待 maintainer 批准执行，0 jobs，并非测试失败。

修复只在新审核单复制旧 owner 字段后，将遗留 `pending` 规范化为 `defer`。owner 的 `accept / reject / move`、备注、方向和摘要覆盖保持；显式 `pending` 的发布校验仍然拒绝，`defer` 也不会获得发布许可。原日期审核单未改写。

本次本地生成 [11 月 1 日滚动待审单](../../../../review/daily/2026-11-01.yaml)：**206 篇论文 + 74 条公告 = 280 条，全部 defer**。另外 [56 条历史积压](../../../../review/backlog/2026-11-01.yaml) 单列，其中 12 条由昨日队列过期转入，条目没有丢失。它们都不是“今日新增”。正式队列基于已有规范分类；原文审查建议独立保留，不伪造成生产模型的成功输出。

[队列验证](queue-verification.json) · [修复和远端失败诊断](pipeline-audit.md)

## 积压审查与续跑

今日针对昨日尚未完成的 **21 篇 S2 论文 + 9 条公告** 做原始来源主审及独立复核。两组先分别冻结，再交叉对照，初始范围判断 **27/30 一致**。最终为 **1 条建议纳入、25 条不进当前 Harness 专题、3 条边界待补证、1 条来源访问受阻**；全部正式决定仍为 `defer`。

- **EvoTeam**：共同建议进入 Harness 候选队列，尚未人工批准。
- **SkillMem、Kernel Optimization、VEvo-Harness**：对权重/潜在记忆、任务产物、经验内容与持久 Harness 修改的区分仍有分歧，保留为边界项。没有按标题直接收录。
- **From observation to generation: A complex-systems perspective on generative Human–AI social systems**：出版方返回 403，Crossref 无摘要；只看到 2026-12 的月份信息。来源中的 2026-12-01 原值保留，具体日期和范围仍未知。

29 条已有基于来源的建议（含 3 条明确的边界意见），另 1 条记录外部访问阻塞。读取范围为官方摘要、部分方法正文和 9 条官方公告，**不声称逐字通读全部论文、复核全部实验数字或完成复现**。独立报告的一处 SkillMem 摘句格式错误通过[单独勘误](independent/quotation-errata.json)更正，冻结原件保留，范围结论未变。

[主审与对照](primary/reconciliation.md) · [独立复核](independent/comparison.md) · [30 条 owner 建议单](owner-candidates.yaml)

10/31 新增的 67 条累计为 **6 条纳入建议、55 条专题外、5 条边界、1 条来源阻塞**。其中 66 条有来源范围建议；生产模型分类、双语摘要及最终人工批准是另外的阶段，没有把范围审查冒充成这些阶段的完成。

[1,206 条逐 ID 当前状态](item-status.jsonl)覆盖全部规范记录，引用冻结历史及[67 条更新状态](new-item-status.jsonl)，保留来源链接、输入哈希、原日期、人工历史与待办原因；不重置历史 owner 决定。

旧账本计数有一项勘误：原 1,124 条中 **163 条**有当批三个阶段且输入匹配，另有 **15 条 HF** 按单独来源审查协议记录三个阶段；这两类应分列，不能把之前的“1,139 条中只有 163 条”当作完整统计，也不能说全量均已三轮审完。原 1,139 与新增 67 的互斥状态、队列交并集见[核算回执](pipeline-audit.json)。旧报告保持冻结，由今日报告补充纠正。

**164 条缺第三轮来源记录属于内部未完成，不能归入外部阻塞。** 其中 158 条也在 369 条摘要续跑队列里。31 条历史模型 API 错误与 8 条出版访问故障是不同问题；完成范围建议、待人工审核和外部故障会重叠，不能做三个互斥桶相加。队列外的 711 条也不能据此认定已完成。

原 369 条论文摘要、31 条模型错误及 57 条新论文规范分类的离线准备队列保留；今日重新核对全部 1,206 条输入和 owner 状态仍匹配，可以继续使用[既有离线入口](../maintenance-2026-10-31/prepare_resume.py)。这是恢复条件验证，不是已续跑模型或已生成摘要。

[当前续跑清单](resume-plan.json)已移除完成的 9 条公告正文和 20 条 S2 范围补审任务，将剩余 1 条移至出版方重试队列，并单列 5 条边界裁决。命名队列共覆盖 486 个不同 ID，任务阶段互相重叠；队列外也不能自动算作完成。旧 164 条第三轮记录和 73 条来源差异等内部工作仍未完成，已明确列出。

## 已有工作复核与发布边界

RSIHub、HarnessDev 保持 `harness_eval`；HarnessDev 为必读，实验设计路线保留 Rethinking → HDA → HarnessDev → RSIHub。Aspire、S³Gym 保持 `general_rsi`，不计入 Harness 方法数。本次没有改论文原始字段或数字。

修复及审查结果同步到既有 [PR #3](https://github.com/adongwanai/follow-rsi/pull/3)，等待 owner 审核。`feed-publish.yml` 仍是 `disabled_manually`。本次没有自动接受、合并或发布，也没有恢复发布工作流。

45 例完整 Harness 评测仍为 **precision 0.9231、recall 0.8571 < 0.90**；旧 trusted-main 的 105/107 身份匹配问题是另一项失败。没有付费重跑、放宽阈值或用工程测试代替评测闸门。

## 验证

**327 项 pytest 通过**；107 篇论文、9 条路线数据校验通过。两次构建一致，README 手写区、论文事实文件及公开日报/Atom/latest 保持。新增来源建议与正式人工裁决分开记录。

[测试日志](pytest-final.log) · [构建回执](build-verification.json) · [最终验证](validation.json)
