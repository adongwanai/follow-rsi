# 11/07 非 HF 来源独立复审

独立复审时间：2026-11-08T00:09:19.907877+00:00。采集归期仍为 2026-11-07。

14 条全部完成范围复审：**建议纳入 0，建议排除 14，范围待定 0，与初审范围分歧 0**。这里的排除仅指不进入当前 Harness 自进化专题，不评价材料的一般研究价值。没有应用正式审核决定，没有修改 canonical、日报或生产文件。

## 独立证据边界

范围与日期复审，不是实验复现或所有实验数字复算。独立读取了 Sakana 缓存全文、DeepMind 缓存全文、arXiv 完整官方摘要，针对两篇 METR 缓存正文的摘要/方法/限制复核，并独立打开 Cult.fit 官方全文。其余 8 篇 OpenAI 的正文证据限主审存下的引句；仅核验存档的文件、引句和位置，不声称独立验证完整正文。先前 HTTP 403 保存的是失败响应，未当成正文。

8 篇 OpenAI 的有限摘录复核不能写成“第二名审阅者逐篇读完完整正文”。Cult.fit 是本次另行用 Chrome 打开并通读的官方文章，页面日期为 November 5, 2026；它的日志调查与修复 PR 面向业务生产系统，工程师审阅和团队统一开发约定不等于 Agent 自改并继承 Harness。

## 身份和日期

- arxiv:2511.19492 的官方标题为 Forecasting AI Time Horizon Under Compute Slowdowns；v1 发表与版本日期均为 2025-11-23T10:46:10Z。
- 新的 METR 文章是 Independent Assessment of AI R&D Acceleration at Anthropic in October 2026，原发于 2026-11-05T08:00:00+00:00。原始 RSS item[2] 中旧论文链接的锚点是 future compute bottlenecks，两条身份必须分离。
- Sakana 原始 Atom 时间 2026-10-30T00:00:00+09:00 等于 UTC 2026-10-29T15:00:00+00:00，不能当作日期冲突，也不能按 11/07 采集日重置。
- 所有原发表日、版本日与 first_observed 从输入逐字保留；复审日期独立记录。

## 逐条结论

| # | 条目 | 结论 | 主要原因 |
| --- | --- | --- | --- |
| 1 | Intelligence Report: SNSのAI分析からみる米中間選挙 | 排除 | 读完缓存的官方 RSS 正文后，修改对象是叙事、研究假设和选举分析报告。多个模型互评与原文核对属于任务求解质量控制；没有把经反馈修改的提示、技能或编排沉淀成后续任务的 Harness。 |
| 2 | Review of the "Risks from automated R&D" section in Anthropic's Risk Report (August 2026) | 排除 | 缓存正文的摘要、阈值定义和结论讨论 AI 研发替代、加速归因及风险报告的不确定性。评测对象不是 Harness 修改的效果或其专项风险，不能因为评估 AI R&D 而计入当前专题。 |
| 3 | Forecasting AI Time Horizon Under Compute Slowdowns | 排除 | 官方 arXiv v1 元数据及完整摘要说明它是 2025 年算力减速下能力时间跨度的预测。METR 新帖中的链接是参考文献锚点，不是新帖的论文身份。没有 Harness 迭代对象、验收与继承机制。 |
| 4 | Partnering with Hacktron to find vulnerabilities in OpenAI’s systems | 排除 | 官方 RSS 与既存正文引句描述合作方选择安全测试范围，Agent 进行代码审查、渗透测试和红队测试。改进目标是被测系统的安全，没有证据表明 Agent 按反馈修改并继承自身 Harness。 |
| 5 | Measuring how AI agents handle everyday wet-lab science | 排除 | 官方 RSS 将 BioBasicsBench 定义为湿实验原始数据解释能力基准；既存正文引句说明任务及评分标准由科学家编写。它是领域能力评测，不是专门比较 Harness 演化或检验这种演化的泛化。 |
| 6 | Australian universities are creating AI-native graduates | 排除 | 官方 RSS 和既存正文引句明确是大学扩大 ChatGPT 使用、教学实践及学生能力培养。课程与使用规范不是 Agent 可执行 Harness 的自修改对象。 |
| 7 | Cult.fit builds operational muscle with Codex | 排除 | 本次独立打开并通读官方正文：公司选择 Codex 作为统一开发平台；SRE Agent 聚合观测日志、调查事故并提交目标系统修复 PR 给工程师审阅。正文的 skills 和 feedback loops 是团队共享约定，没有描述 Agent 自改技能/策略并跨任务继承。 |
| 8 | GPT‑6 Cyber: Advancing the frontier of aligned cybersecurity agents | 排除 | 官方 RSS 和既存正文引句支持专项模型训练、授权范围遵守及合作方安全反馈；尚无外部 Harness 被系统迭代修改的证据。排除依据是缺少 Harness 机制或专项评测，而非单纯因为同时训练权重。 |
| 9 | Merge builds product and business tools with OpenAI technology | 排除 | 官方 RSS 和既存正文引句将代码审阅反馈、产品决策、实现、验证和发布分别归给 Codex 与 Merge 员工；可复用业务工作流由员工构建。产品开发与人类维护流程不能据此升级为 Harness RSI。 |
| 10 | Setting a new standard for responsible AI infrastructure | 排除 | 官方 RSS 及既存正文引句讨论算力园区的社区承诺、公共资源、就业和电网成本责任，属于基础设施政策，与 Harness 演化范围无关。 |
| 11 | Flipsnack grows product signups with conversion optimization | 排除 | 官方 RSS 和既存正文引句把变化归给营销团队的活动目标与竞价设置。保留的是广告配置，并非执行 Agent 的程序工件。效果数字不在本次范围结论中推广。 |
| 12 | Franklin Templeton uses OpenAI to support investment research | 排除 | 官方 RSS 及既存正文引句说明投资团队和 AI 推动者开发受治理、可复用的平台与业务工作流。平台可复用并不证明它根据执行反馈自行修改 Harness；没有具体更新对象、验收和继承记录。 |
| 13 | Gemini Omni 1.2 Flash: Fast and cost-effective with longer clips | 排除 | 读完缓存的官方文章正文后，多轮反馈修改的是同一段视频和其生成条件，输出保持一致是视频编辑能力。没有跨任务可复用 Harness 的演化；产品版本发布也不能直接作为训练权重发生何种变化的证据。 |
| 14 | Independent Assessment of AI R&D Acceleration at Anthropic in October 2026 | 排除 | 缓存正文的执行摘要、方法及局限性讨论 AI 辅助研发、公司能力增长和归因，不是 Harness 工件演化的专项测试。明确区分 AI assistance 与 autonomous contributions，并保留关键证据被删改、公开材料无法独立复现归因的局限。 |

## 分类表述修正建议

- Cult.fit、Merge、Franklin Templeton 的初审 direction=harness 只是工程上下文。正式整合时必须保留范围排除，不能将这些标签计入 Harness RSI 篇数。
- Gemini Omni 的文章支持视频产品升级和外部视频产物编辑；具体权重训练变化仍为 unknown，不能从版本号自行补出训练机制。
- METR 的员工自述提速、公司能力进步和全自主研发贡献是不同指标；关键证据被删改的限制需要保留。本次不推广或重新计算这些结果数字。

## 校验

- 4 路原始 feed 文件 SHA-256、各条目的标题/链接/发表时间已独立解析核验。
- 14 个 source_hash 按 scripts/feed/review.py 的字段集重算一致；仅绑定初审快照，不断言与后来 canonical 哈希相同。
- 29 条原有引句的文件哈希、引句哈希、字符位置或 JSON pointer 全部一致。
- 旧论文官方 Atom ID、标题、发表/更新时间和 METR 引用锚点一致；输入快照哈希一致。
- 没有付费模型调用、GitHub 写入、正式审核决定或生产数据修改。

初审 JSON SHA-256：`6cd78ea398be5e2d143a865a96eb2d3b3491e7efb1b8a25571376c194dcf2b24`。

机器可读逐条引句、哈希、阅读覆盖、具体补证条件和复审时间见同目录 other-source-independent.json。
