# 2026-10-30 维护与三轮审核

**HF 10 月 30 日榜尚未就绪，今天没有自动发布日报或 Atom 条目。** 本轮新增发现并完成三轮范围审查 12 条：10 月 29 日 HF 后补推荐 7 篇、原日期为 10 月 29 日的实验室公告 3 条、S2 历史论文 2 篇。建议纳入 Harness 0 条、建议不纳入 10 条、模型与独立复审有分歧 2 条；正式决定一律 `defer`，这些建议不是 owner 批准或正式拒绝。

## 日期与去重

北京时间 08:03 和 08:14 的实际请求中，HF API 明确返回 400，当前最大可用日期为 `2026-10-29`。请求 `/papers/date/2026-10-30` 虽返回 200，页面的 `DailyPapers.dateString` 仍为 `2026-10-29`，因此不能算当天列表成功，也不能报告为“当天 0 篇合格”。

10 月 29 日榜从昨日最后观测的 8 篇变为 14 篇：增加 7 篇、移出 DTCA 1 篇、7 篇标题/摘要不变。DTCA 昨日真实出现过的推荐日期仍保留，不删除来源历史。7 篇后补推荐全部按 10 月 29 日归期，只把发现日记为 10 月 30 日。[列表对照](hf-day-comparison.json)

7 篇 HF 的 arXiv ID 与题名均已匹配。首次 arXiv 429 留在第一轮历史报告；后续成功的独立身份核对和原日期见[补充核验](round1-hf-identity-followup.md)。未知字段不由推测补齐。

## 三轮审查与分歧

第一轮读取原始摘要/官方公告、核验来源日期和去重；第二轮用仓库配置的 LLM 独立运行 Harness 闸门，并对 9 篇论文执行正常分类及适用的摘要/数字护栏；第三轮由未读取前两轮结论的独立代理复审全部新增项，定向阅读 5 篇 HF 的正文，以及葡语 S2 论文的方法/理论章节。另一篇 S2 综述只取得官方公开摘要、附录和作者实验协议，未取得订阅全文。

Harness 判据继续要求：外部可复用程序/控制机制是改进对象，执行或评估反馈实际驱动修改，修改被保留并跨任务/轮次复用。通用模型权重训练、记忆事实、任务结果、人工改流程、通用评测与综述不能仅凭提到 Agent/Harness 就算 Harness RSI。

- **监控公告**：第二轮判为 Harness；两个独立复审均未找到系统自主修改自身 Harness 的证据。原文描述团队修补和部署监控系统，agent 负责调查与告警。原始模型输出保留，列为争议待审。
- **法律尽调公告**：第二轮判 borderline；独立复审指出修改者是律师，跨任务自动保留机制未证实，同样列为争议待审。
- **LongZero**：多轮自生成数据闭环在正文 §5 中仍是未来工作，当前方法不能写成已经完成的多轮模型 RSI。
- **DeepSeek 安全报告**：虽然包含 Rust Harness 子任务，研究整体对象仍是模型安全评测，不是 Harness 自进化专项评测。
- **葡语理论论文**：一般 RSI 与物理自主性理论，正常模型分类为 include/theory_survey，但范围过滤将其存入归档；不进入 Harness 审核单或公共 feed。

核对 74 次引文匹配、63 个去重后的条目/引文对，覆盖 12 个新增项及 1 个原文 hash 未变的 Sakana 公告复核。**完整四项全文证据卡审计完成数仍为 0**。[核对过的引文](verified-quotes.json)

[HF 第一轮](round1-hf.md) · [HF 第三轮](round3-hf.md) · [公告第一轮](lab-round1.md) · [公告第三轮](lab-round3.md) · [S2 第一轮](s2-round1.md) · [S2 第三轮](s2-round3.md) · [12 份第二轮原始输出](round2-results/) · [9 篇正常流水线判断](pipeline-judgements/)

## 12 条新增发现

表格按原发表日期正序。所有正式决定均为 defer；“不纳入”是专题范围建议，不表示已由 owner 拒绝。

| 条目 | 原发表日 | HF 推荐日 | 多轮建议 |
| --- | --- | --- | --- |
| [TauIndianBankBench: Procedure-Aware, Action-Oriented Evaluation of Tool-Using Conversational Agents](https://arxiv.org/abs/2610.30161) | 2026-09-30 | 2026-10-29 | 不纳入 Harness |
| [Amortizing Sequential Experimental Design in Reasoning LLMs](https://arxiv.org/abs/2610.20832) | 2026-10-14 | 2026-10-29 | 不纳入 Harness |
| [RealCLI: Toward a Unified Evaluation of Human-Agent Collaboration for CLI Agents](https://arxiv.org/abs/2610.22507) | 2026-10-15 | 2026-10-29 | 不纳入 Harness |
| [LongZero: Enhancing Long-Context Reasoning in LLMs from Zero Data](https://arxiv.org/abs/2610.30132) | 2026-10-21 | 2026-10-29 | 不纳入 Harness |
| [Capacidade sem autonomia no autoaperfeiçoamento da inteligência artificial](https://submissoesrevistarcmos.com.br/rcmos/pt_BR/article/view/3106) | 2026-10-26 | 无 | 不纳入 Harness |
| [Evaluating DeepSeek V4.1 Flash-1017 for loss of control and harmful manipulation risks](https://arxiv.org/abs/2610.35671) | 2026-10-26 | 2026-10-29 | 不纳入 Harness |
| [Instruction Capacity: Behavior and Degradation of Language Models under Controlled Load](https://arxiv.org/abs/2610.36095) | 2026-10-26 | 2026-10-29 | 不纳入 Harness |
| [Know, then Draw: A New Learning Paradigm for Visual Generation](https://arxiv.org/abs/2610.37626) | 2026-10-27 | 2026-10-29 | 不纳入 Harness |
| [LLM-based agents for generalized web automation and schema-guided data extraction: a survey](https://link.springer.com/article/10.1007/s41060-026-01335-y) | 2026-10-28 | 无 | 不纳入 Harness |
| [How Ropes & Gray is developing AI for transactional diligence](https://openai.com/index/ropes-gray-ai-diligence) | 2026-10-29 | 无 | 争议待审（两轮独立复审建议排除） |
| [How we detect frontier model misalignment](https://openai.com/index/how-we-detect-frontier-model-misalignment) | 2026-10-29 | 无 | 争议待审（两轮独立复审建议排除） |
| [An updated Model Spec for more capable and beneficial AI](https://openai.com/index/updated-model-spec) | 2026-10-29 | 无 | 不纳入 Harness |

[逐条候选及三轮对照](candidates.json) · [正式待审单](../../../../review/daily/2026-10-30.yaml) · [建议排除附表](../../../../review/daily/2026-10-30.excluded.yaml)

## 来源健康与积压

12 路启用来源全部实际尝试：10 路完成、HF 部分完成、S2 authors 重试后仍失败。下列是原始来源命中数，含重复引用，不是新增 Harness 论文数。HF 原始前一日列表为 14 条，宽关键词预筛留下 5 条；本轮对全部 7 条后补推荐另外逐篇审核。

| 来源 | 原始命中 | 最终状态 |
| --- | ---: | --- |
| arxiv-harness | 0 | 完成；首次 429，冷却后重试成功 |
| arxiv-rsi | 0 | 完成 |
| arxiv-adjacent | 0 | 完成 |
| s2-citations | 1492 | 完成 |
| s2-authors | 0 | 失败：HTTP 429 |
| hf-daily | 5 | 部分完成：当天榜未就绪 |
| rss-sakana | 6 | 完成 |
| rss-metr | 2 | 完成 |
| rss-openai | 36 | 完成 |
| rss-deepmind | 3 | 完成 |
| rss-weco | 0 | 完成 |
| github-releases | 0 | 完成 |

S2 继续匿名模式，间隔 3.1 秒，429 使用有上限的指数退避。RSS 的两次 arXiv 补全各成功 1 条；之后 HF 批量补全 429 仍保留为失败，不能用另一次成功的 7 篇身份核对覆盖掉该失败。[逐路开始/结束时间与每次结果](source-attempts.json) · [来源健康](source-health.json) · [URL、时间和 hash 清单](source-manifest.json)

规范记录从 1,112 增为 1,124，保留原有全部 ID、owner review 和历史推荐日期。昨日 94 个未决条目全部顺延；正式待审单现在是 **32 篇论文 + 65 条公告 = 97 条**，其中 10 条处于配置新闻窗、87 条为 backlog，这不是“今天新增 97 条”。8 篇新增论文在建议排除附表，1 篇通用理论进入非 Harness 归档，3 条公告进入正式待审单。[集成与逐项保护校验](integration.json)

此前报告的 616 条尚未完成范围审查的历史发现不在本轮 12 条范围内，没有把抓取成功写成审查完成。此前六篇优先候选见[10 月 29 日报告](../maintenance-2026-10-29/README.md#优先待审的六篇)。

## 发现的数据问题

- TauIndianBankBench 的官方 arXiv 数据报告首发为 2026-09-30，虽然 ID 为 `2610.30161`。按来源保留，不根据 ID 推改日期。
- 葡语论文页面可见日期、citation_date、Crossref 和 PDF footer 为 2026-10-26，但网页另有 `DC.Date.issued=2026-08-02`，原因 unknown。两值均记录，没有擅自修正原数据。
- Springer 综述在线发表/Version of record 为 2026-10-28，期刊期次是 12 月；不将期次日期替换为首发日期。
- S2 中既有的 6 条未来书目日期继续保留、暂缓，没有挪到今天充数。

## 代码修复、验证与发布状态

修复 HF 跨日抓取：一个日期失败时保留其他日期的成功数据，逐日记录时间、HTTP 状态和错误正文；只将准确匹配官方最大日期错误的 HTTP 400 判为 not_ready。一般 400、429、500、超时或无效 JSON 仍报错，部分成功不冒充全部成功。现场重抓已经验证前一日数据不再丢失。

修复来源健康汇总：逐源采集后的空刷新会从各启用源的持久状态重新计算待发送告警，保留其他来源的失败提醒，恢复后清除对应待办；不增加失败计数、不改抓取时间。本轮刷新保留了 4 条符合原有阈值的待处理来源告警，其中 3 路是连续空结果，S2 authors 是 HTTP 429，不能都称网络故障。[状态刷新核对](health-refresh.json)

最终 **308 项 pytest 全部通过**，104 篇论文、9 条路线通过数据校验；构建连续两次字节一致，正式待审单校验通过。详见[validation.json](validation.json)。目录论文数字、owner 修正、README 手写区、SVG 与生成脚本、公开日报/Atom 内容均受保护；自动发现与模型建议不会触发发布。

08:10 核查 PR #3：旧 head 的 build/validate 成功，evaluate 失败源于旧 trusted-main 的 107 例评测仅完成 105 例（2 个题名身份不匹配），数值指标本身通过。**当前 PR 也尚未实现这两个标题的有来源别名/版本映射，不能说身份修复已经完成。** 这是独立于 10 月 27 日 45 例 Harness 闸门 recall 0.8571 < 0.90 的另一问题；今天没有重跑该质量基准或改标签/阈值。[CI 核查](pipeline-audit.md) · [实际旧 CI artifact](ci-evaluation/report.md) · [代码交叉检查](final-code-review.md)

`feed-publish.yml` 仍为 `disabled_manually`。今天 owner 接受 0、自动合并 0、发布 0；本轮改动继续集中于 [PR #3](https://github.com/adongwanai/follow-rsi/pull/3)，不直接推 main。距离最近每日审核单合并已 3 个日历日，且积压超过 60 条，已创建[审核积压提醒](https://github.com/adongwanai/follow-rsi/issues/6)，写明 97 条待审数量。

本目录是待审核证据包，不是公开日报。`build/` 开头的文件路径指向本机忽略目录；原始网页/PDF 不复制进 Git，公开复核可使用列出的来源 URL、hash 和引句。
