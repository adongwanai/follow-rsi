# 2026-11-04 维护与全量来源对账

今天没有调用付费模型，没有新增正式接受或出版。规范库由 1,351 条增至 **1,598 条**：新增来源发现 51 条，另补回历史 HF 漏入规范库的 196 条。两批分别保存，不把旧榜单、补录或范围建议写成今日新论文。

## 今日来源与审核

12 路已启用来源全部实际尝试：6 路正常；HF 11/04 榜未就绪；3 路 arXiv 查询超时或 429，2 路 Semantic Scholar 部分失败。S2 匿名调用，成功分页保留，最小请求间隔 3.105 秒，429 最多重试 5 次；当前环境和本地配置没有非空 S2 key。详见 [来源健康](source-health.md) 和 [请求回执](source-attempts.json)。

HF 明确只开放至 11/03。本次完整保存该日 **45 篇**，其中 43 个新 ID，另为 Video Generation Meets Agent Harness、TinyAstral 补记推荐日。两条旧记录的正文、摘要、原日期、first_seen 和审核决定保留。8 个新增官方 RSS 条目单列，未混入 HF 日报。

45 篇 HF 都核对了官方身份与提交历史；44 篇日期一致性通过，SIMIT 的 `2611.00053` 编号与官方 v1 的 **2026-10-11 15:59:08 UTC** 存在异常。两份官方响应一致，本次只报告原值并阻塞日期自动规范化，不猜改日期。8 篇 HF 与 arXiv 摘要有字面差异，未据此声称发生科学内容改变。[官方元数据核验](hf-official-metadata.md)

两位主审与独立复审对完整 45 篇 HF 摘要做了范围判断，其中 8 篇另读了相关正文、2 篇复用来源哈希未变的旧正文审核。最终为 **4 项纳入建议、40 项排除建议、1 项范围分歧**；4 项纳入建议中只有 2 项是新 ID。8 篇 RSS 当前均无充分 Harness 纳入依据，其中 DeepMind 化学工作流核对了正文，其余以官方摘要为限。

- **NorthCUA**：纳入依据限于技能组件的失败反馈、修订、独立测试与后续任务复用，分类为 `harness/component`；不把整个模型训练结果归给 Harness。
- **Can Coding Agents Sustain Continual Evolution without Forgetting?**：建议作为 Harness 专项评测纳入；其中 94% 来自 50 题抽样，不写成完整 SWE-bench 或独立留出成绩。
- **Avatar Intelligence**：主审认为是通用个人 Agent 议程，独立复审认为其中 Rehearsal 与 Harness 规则更新构成边界理论关联。保留分歧，不强行排除或接受。
- Video Generation Meets Agent Harness 与 TinyAstral 复用旧范围意见；新增推荐日会改变审核来源哈希，不能把旧批准自动移植。

所有范围意见都与正式决定分开。当前真实评测召回 **24/28 = 0.8571，低于 0.90**，付费评测继续暂停，新的正例建议仍被发布门阻塞。未把范围阅读说成复现或复算全部实验数字。

[主审 A](primary-a-review.md) · [主审 B](primary-b-review.md) · [独立复审](independent-review.md) · [RSS 初筛](rss-review.md) · [逐项续跑状态](../../../../data/feed/intake/2026-11-04/review-status.json)

## 历史遗漏与剩余工作

历史原始响应、规范库、旧发现及待审清单对账得到 **8,280 个稳定 ID**，不能把它们都称作未审候选。其中 6,292 条不在任何已存来源时间窗内，441 条 S2 记录没有合格的日期证据；196 条是 10/14–10/26 九个 HF 日榜中被旧关键词预筛漏掉的成员。

这 196 条已逐项保存原始摘要、来源位置、哈希及排除建议，并补入规范库；其中 34 条复读完整摘要，其他项为方法段初筛。独立复审抽查了 7 条高风险词项和 2 条固定随机项，9 篇完整摘要均支持排除；它们不是 196 篇全文三轮审核。旧快照没有真实抓取时间回执，无法反推 first_seen；新规范记录使用本轮发现时间，并单独保存原始抓取时间 `unknown` 与真实 HF 推荐日期。

加上本轮 51 个新来源 ID，来源并集为 **8,331**：1,598 条已规范化，余下 6,733 条是上述时间窗外或日期证据不足的来源记录。每项都有可恢复状态，没有用统一 defer 掩盖未处理阶段。

旧规范库中仍有 426 条只具备历史模型范围意见、缺当前三轮复核；187 条已获范围意见但缺双语摘要，41 条摘要已有但缺正式出版条件。这些队列有重叠，不能相加当成未处理总数。付费摘要/重试继续暂停；质量、正文工件证据与日期缺失分别保留原因。682 条旧范围回执仍保留，AdaPRA 后续纠正未被旧批准覆盖。

[完整历史对账与分阶段队列](backlog-reconciliation.md) · [9 条独立抽查](historical-hf-independent-review.md) · [196 条逐项意见](../../../../data/feed/intake/2026-11-04/historical-hf-review-status.json) · [规范库整合回执](integration.json)

## 审核 PR 的实际故障

PR #35 的审核 YAML 有 **1,503,947 字节**。GitHub Contents API 对其返回 `encoding=none` 和空 `content`，旧读取函数把空字符串当 YAML，导致 `None is not of type object`。修复只在该返回形态下按固定内容 blob SHA 读取原字节；同仓、固定 head、可信默认分支代码、审核和质量门都保留。

实际 blob 与本地 Git 对象逐字一致，277 条 defer 决定未改。新增大文件回归测试，独立工程复核通过；没有为排查故障启用付费工作流。[故障回执](pr35-read-failure.json) · [工程复核](engineering-review.md)

PR #3 已合并；本轮开始时 7 个论文 issue 仍分别受质量或工件证据阻塞，PR #35 仍待审。`feed-daily.yml`、`feed-eval.yml`、`feed-publish.yml` 均实际核实为手动暂停，保持暂停。RSIHub/HarnessDev 仍属 Harness 评测，HarnessDev 为必读；Aspire/S³Gym 为通用 RSI，实验设计路线保持 Rethinking → HDA → HarnessDev → RSIHub。

网站只更新来源健康与每日更新记录。已出版的 21 条内容和 4 条 Atom 条目保留；11/03、11/04 均不生成新日报或空 Atom 条目。当前状态和后续部署凭据以本次校验及上线回执为准。

## 统一验证

全仓 `pytest`：**384 passed，54.01 秒**；114 篇论文及 9 条路线数据校验通过。两次构建的 **631 个文件完全一致**，README 手写部分逐字保留。所有旧规范条目的科学字段、决定和 first_seen 保留；数据目录未产生付费用量日志。已变更 JSON/JSONL 均能解析，凭据模式扫描无命中，`git diff --check` 通过。[验证回执](integration-validation.json)
