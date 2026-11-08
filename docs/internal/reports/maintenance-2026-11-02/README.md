# 2026-11-02 维护记录

已实际尝试全部 12 路来源，核实 HF 当日 15 篇，并对本轮 **327 条**新增观察及历史积压留下来源建议或明确的访问阻塞。综合建议 **68 纳入、231 排除、19 边界待定**；另 **9 条**缺原始来源，范围保持 unknown。所有本轮正式决定仍为 defer；没有自动接受或发布。

这不是新增 327 篇论文，也不是全量论文的实验数字认证。规范库现有 **1,300 条**，比原分支增加 94 条：**78 条是已有证据库记录的来源导入，16 条才是去重后的新发现**（13 篇 HF、2 篇 main 上已有的 S2 发现、1 条 RSS 公告）。HF 榜中另 2 篇已在库，仅新增推荐日期观察。

[本轮综合建议](reconciliation.json) · [owner 待审建议单](owner-candidates.yaml) · [1,300 条逐 ID 状态](item-status.jsonl) · [可续跑清单](resume-plan.json)

## 实际采集与来源故障

实际采集时间为 **UTC 05:52:48–06:16:13（北京时间 13:52:48–14:16:13）**，不冒充早上 08:00 已完成。逐路尝试时间、初次失败与重试历史均保存。

| 来源 | 本次返回数 | 结果 |
| --- | ---: | --- |
| HF Daily Papers | 15 原始 / 11 关键词预筛 | 11/2 榜 15 篇全部补入来源审核；11/1 返回空列表 |
| arXiv Harness | 0 | 请求成功、空结果 |
| arXiv RSI | 0 | 请求成功、空结果 |
| arXiv adjacent | 0 | 请求成功、空结果 |
| S2 citations | 1,326 原始 / 589 去重 | 全路成功；与合并后清单相比没有新 ID |
| S2 authors | 不完整 | HTTP 429，正常指数退避重试后仍失败，不能记作零篇结果 |
| RSS Sakana | 6 | 成功；原始日文编码修复后重新抓取 |
| RSS METR | 2 | 成功 |
| RSS OpenAI | 39 | 成功 |
| RSS DeepMind | 3 | 成功 |
| RSS Weco | 0 | 请求成功、空结果 |
| GitHub releases | 0 | 匿名首次 403；用既有 CLI 身份在进程内重试成功 |

表内返回数不是新增篇数或 Harness 收录数。S2 仍为匿名模式，间隔 3.1 秒、最多 5 次指数退避重试；状态中如实记录。没有输出、保存或提交凭据。来源健康中由空结果产生的待提醒动作没有被误写为真实服务故障，也没有另开重复提醒 issue。

[逐路原始尝试](source-attempts.json) · [来源健康](source-health.json) · [清单整合保护回执](integration.json)

## HF 今日与其他来源单列

HF **11/2 推荐榜**的 15 篇，综合建议 **3 纳入、12 排除**。论文原发表日、版本日和推荐日独立保留，未把今天推荐改写成今天首次发表。

| HF 候选 | 原发表日 | 原版本日 | 范围与限制 |
| --- | --- | --- | --- |
| R²Orch | 10/15 | 10/22 | 权重与技能共演化；附录明确技能版本修订、验收和跨训练轮保留。最终部署为零技能，不能声称部署时仍保留技能库 |
| CEPO | 10/26 | 10/26 | 训练执行反馈修订协调者/执行者提示，验证选择后用于测试 |
| RoboArchitect | 10/30 | 10/30 | 冻结策略，反馈修订控制代码，并在未见任务/场景评测；已读实验均为仿真，不能写成真机迁移 |

R²Orch 和 CEPO 是已存在记录；只有 RoboArchitect 是本次新 ID 中的 Harness 纳入建议。R²Orch 初审曾排除，补读附录并对齐 owner 共演化判据后更正；[冻结初审与后续勘误](independent/comparison-errata.json)均保留。

另两篇 S2 补充发现单列：Procedural Skill Cache 的官方摘要已找回，但技能缓存/索引与程序策略改写边界仍待定；外部 interatomic potential 设计属于 AI 研发产物，建议不进当前 Harness 专题。它们不是 HF 11/2 推荐。

Sakana 新公告发表于 11/1 15:00 UTC，是 10/26 活动回顾；11/2 只是发现日。建议归通用 RSI 公告，不计今日 Harness 论文。

[今日原始核验](today-primary/findings.json) · [独立今日复审](independent/today-findings.json) · [公告核验](today-primary/post-supplement.json)

## 历史积压与分歧

| 分组 | 条数 | 纳入建议 | 排除建议 | 边界 | 原始来源受阻 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 旧第三轮来源记录 | 164 | 22 | 130 | 10 | 2 |
| 来源与版本差异 | 73 | 43 | 27 | 3 | 0 |
| 遗留原文/边界补证 | 15 | 0 | 3 | 5 | 7 |
| 旧判据复核标记 | 57 | 0 | 57 | 0 | 0 |
| 今日观察（含 2 篇已在库 HF） | 18 | 3 | 14 | 1 | 0 |

分组互不重叠。318 条已有基于来源的范围意见（包含明确的边界意见），9 条记录原文访问阻塞；全部 327 条新意见尚待 owner 审核。来源完成、生产处理完成和人工批准是不同维度，不能相加成互斥的“完成/待审/失败”桶。

73 条来源对账中，64 条显式复用哈希和内容核对后的历史范围意见，9 条补读正文后复核。对 44 条版本差异取得原版本正文或对应原始文本；**范围可复用不等于实验数字可跨版本复用**。本次数值审计重新认证为 0。后续独立复审又保留 CUAWright 的跨任务复用疑点，综合数与第一轮 43/28/2 因此不同。

共演化规则按 owner 原文“权重和 Harness 都被迭代修改，算 harness/coevolution”。StateSkill、SkillForge、R²Orch 的真实技能更新不能仅因同时训练权重而排除。现有生产提示词附加了更严的“主要改进对象”条件；[具体修正补丁](coevolution-policy-proposal.patch)已准备并通过应用检查，**尚未应用或运行付费评测**，旧 gate 数字不代表该补丁效果。

VEvo-Harness、ETABS、ECG-RSI、OmniBrain、CUAWright 等保留明确的证据边界或审查分歧。ECG 的 Prompt P5 确实支持生成组件版本修复，但其与训练系统对象的范围边界仍待 owner 裁定；OmniBrain 的候选提醒验证和跨轮保留是正证，仍缺策略工件与提醒内容的区分。没有将缺信息写成确定不存在。

Learner2Skill 的共享协议修改予以承认，但 owner 明确排除用户模拟器，因此按该范围划出；Verification v1/v2 作为通用 RSI 理论相关材料，不把“理论自己不演化”当排除理由。各份冻结判断及补读后的侧记保留；便携路径更正有单独前后哈希回执。

最后 57 条是全量扫描时找回的旧判据标记，单独主审与独立复审，不让它们留在队列之外。引用范围以官方摘要为主，对可疑项补读正文；不能声称每篇全文或每个数字均已复核。

[164 条独立复审](independent/README.md) · [73 条来源对账](metadata-reconciliation/README.md) · [重点独立复审及更正](metadata-independent/POST_FREEZE_COMPARISON.md) · [15 条遗留分歧](independent/remaining-comparison.json) · [57 条主审](prior-rule-primary/findings.json) · [57 条独立复审](prior-rule-independent/findings.json) · [主线程调和](root-adjudication.json)

## 可恢复的生产队列

1,300 条均保存当前来源哈希、owner 状态、原日期、已有建议和待办原因。78 条新导入的既有证据库记录受保护；原 1,206 条科学事实、数字、owner 决定和模型结果未改。观察性来源字段合并及两条 HF 推荐日追加单独留痕。

旧 369 条摘要任务中，**162 条可准备离线续跑目录，207 条先暂停摘要并核对范围**。此筛查同时读取本轮意见与输入匹配的历史独立意见，修复“后续已建议排除/待定，但仍继续按旧纳入标签写摘要”的续跑缺口。它没有改生产分类。

另有 **70 条待规范分类、32 条历史/新增处理错误待重试**；后者包含不同处理阶段错误，不等于全部都余额不足。共有 293 条生产标签与来源意见需核对、40 条边界待裁定（含已存在的有效历史意见）。队列互相重叠，共涉及 551 个 ID。队列外记录也不自动等于本轮三轮全文审查完成。

9 条原始来源仍不可得；已找回原文但 canonical 摘要缺失的 4 条另列为元数据补证提案，不偷偷覆写原值。1 条原有官方公告摘要及新 Sakana 公告的生产处理状态仍明确记录。

按 owner 最近要求，付费模型阶段保持暂停，本轮付费 API 调用为 **0**。历史 HTTP 402 没有再探测，不推断当前余额。离线入口只检查输入/owner 状态或准备隔离目录，不会调用模型、修改 canonical 或发布：

```bash
.venv/bin/python docs/internal/reports/maintenance-2026-11-02/prepare_resume.py
```

## 代码修复、队列与既有工作

- 修复每周日 UTC 23:41 的任务延迟到周一执行时被错归下一周；scheduled picks 使用最近一个周日所属 ISO 周，手工和显式指定周保持各自含义。
- 修复 RSS 根据 HTTP 猜测编码错误导致日文乱码；按响应字节及 XML 声明解析，并用真实 `requests.Response` 回归用例验证。
- [11/2 滚动审核单](../../../../review/daily/2026-11-02.yaml)为 **206 篇论文 + 75 条公告 = 281 条，全部 defer**；[历史积压单](../../../../review/backlog/2026-11-02.yaml)为 114 条。13 篇没有生产模型分类的新 HF 论文在来源建议单中，不伪造 llm 成功输出。281 和 114 都不是今日新增数；78 条既有库导入中 53 条进入 backlog、4 条进入滚动单，已明确为旧记录。
- 远端 PR #13 仍有 144 条遗留 pending 的 owner gate 失败；PR #15 的 W45 标题问题来自延迟运行。未替 owner 改判、合并或关闭这些待审单。既有提醒 issue #6 不重复创建。
- RSIHub、HarnessDev 的 Harness 评测定位、HarnessDev 必读及 Rethinking → HDA → HarnessDev → RSIHub 路线已存在，保持；Aspire、S³Gym 仍为通用 RSI。

[队列验证](queue-verification.json) · [main 来源合并对账](main-reconciliation.json) · [远端流水线快照](pipeline-audit.json)

## 数据问题与验证边界

版本、发表日期、作者名、链接来源差异只报告、不改论文原值。例如 Procedural Skill Cache 的 DOI 仅确认到 2026-10 月，原记录 10/05 的具体日尚未确认；Musubito 的 Crossref 刊期为 2027-02，与原记录不同；VEvo/MoLRSI 已有 v2 而 canonical 仍 v1。最后 57 条还发现 Multiscale Policy Optimization 的作者名差异，详情在该组身份回执。Sakana 的 `post:/us-midterms-analysis/` 与完整 URL ID 的来源、标题、摘要和日期一致，已列入[重复身份报告](prior-rule-primary/duplicate-report.json)和后续核对队列；保留两条历史记录，不把 1,300 个 ID 宣称为 1,300 个不同作品。保留首次观测和后续纠正，不能把元数据 HTTP 200 当成找回摘要。

**333 项 pytest 通过**（54.83 秒），107 篇论文、9 条路线校验通过；两次构建的 580 个生成文件字节一致。README 手写部分、原论文事实以及公开 daily/Atom/latest 均保持。本轮后续只新增审核报告和离线清单，没有在这些代码通过后继续修改生产实现。

45 例完整 Harness 闸门仍为 **precision 0.9231、recall 0.8571 < 0.90**（10/30 的结果，本轮未重跑）。旧 trusted-main 105/107 身份匹配失败是另一件事。工程测试通过不等于质量门槛通过。

工作同步至既有 [PR #3](https://github.com/adongwanai/follow-rsi/pull/3) 待 owner 审核；`feed-publish.yml` 保持 `disabled_manually`。公开日报和 Atom 没有自动增加条目，未自动合并、接受或发布。

[测试日志](pytest-final.log) · [构建回执](build-verification.json) · [最终验证](validation.json)
