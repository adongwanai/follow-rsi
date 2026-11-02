# 2026-10-30 公告来源复审

本报告仅提供可追溯的分类建议。全部 owner decision 保持 defer；未修改 feed、审核单或发布内容。

读取 19 / 65 篇全文：全部 4 个模型 Harness 正例、全部 4 个其他方向项、11 个分层排除样本。130 个原始 HTML/提取文本哈希全部通过，48 条本报告引文均为原始文本的连续子串。

四个模型 Harness 正例中，3 条应排除，1 条保留边界待查；本次没有一条达到可验证 Harness 自进化的放行条件。样本有目的地覆盖高风险项，不能将该比例外推为全部模型结果的准确率。

三轮检查包含：快照完整性、全文语境/反证、引文与边界复核；Terminal X 另经第二位同族 Agent 只读复核，结论一致。未进行底层实验复现，不宣称 formal independent audit PASS。

原模型 index 62 的引文在空白归一化后匹配，但不匹配原始提取文本；原句含 4 处换行。分类仍应排除，不应把该条的原始子串验证记成通过。

输入为 65 条抓取与模型结果快照（本地缓存位置保留在 JSON）；[全部官方来源与日期](labs-source-index.json)。快照 SHA-256 `bf0849c60f7611e048b97ea2b9d444307772f17f0eff4bfb503b474ca04adf51`。

| 索引 | 条目 | 模型建议 | 复审建议 | 依据 |
| --- | --- | --- | --- | --- |
| 30 | [What FDE means at OpenAI](https://openai.com/index/forward-deployed-engineering-means) | harness | exclude | 人工工程迭代，不是 Harness 自进化 |
| 35 | [Terminal X matches senior investor judgment 88.6% with GPT-6.1](https://openai.com/index/terminal-x) | harness | borderline | 有反馈到指令的线索，但自动改写与执行复用仍待确认 |
| 60 | [How Grupo Boticário uses AI to strengthen human connections](https://openai.com/index/grupo-boticario) | harness | exclude | 人工业务团队调提示词，不是系统自动改进 |
| 64 | [How we detect frontier model misalignment](https://openai.com/index/how-we-detect-frontier-model-misalignment) | harness | exclude | 监控与安全工程，未证实监控器自改写 |
| 7 | [Sakana Chatが覚えていることを見てみよう：メモリを可視化する新機能「My Fish」](https://sakana.ai/my-fish/) | other_direction | other_direction | 跨会话记忆产品，非 Harness 程序演化 |
| 25 | [How we built ChatGPT’s novel ad stack for user trust and relevance](https://openai.com/index/building-chatgpt-ad-stack) | other_direction | other_direction | 反馈训练广告模型，非 Harness 更新 |
| 33 | [Securing our frontier model training environment](https://openai.com/index/securing-our-frontier-model-training-environment) | other_direction | exclude | AI 红队加人工安全修复，不是数据/任务 RSI |
| 53 | [How Third Moment Research runs 10,000 agents for 36+ hours](https://openai.com/index/third-moment-research) | other_direction | other_direction | 失败驱动合成场景；未证实 Harness 演化 |
| 2 | [Red-Teaming OpenAI's Internal Agent Monitoring Systems](https://metr.org/blog/2026-10-22-red-teaming-openai-agent-monitoring/) | exclude | exclude | 人工独立监控红队评估 |
| 4 | [オントロジーを基盤に、意思決定・実行を支援するAIエージェントプラットフォーム「Sakana Aquarium」](https://sakana.ai/aquarium-release/) | exclude | exclude | 固定 Agent 平台；更新机制属于未来开发 |
| 8 | [GPT-6.1 Sol helps CodeRabbit strengthen security across complex codebases](https://openai.com/index/gpt-6-1-sol-coderabbit-code-security) | exclude | exclude | 审查和修复客户代码 |
| 9 | [Greptile takes bug detection beyond code review with GPT-6 Astra](https://openai.com/index/greptile-code-review-codex-astra) | exclude | exclude | 代码测试与知识索引产品 |
| 10 | [How an assessor could investigate evidence of acceleration from the automation of AI R&D](https://metr.org/blog/2026-10-14-ai-rd-acceleration-assessment-proposal/) | exclude | exclude | AI 研发加速评估提案，非 Harness 专项 |
| 27 | [Using thousands of AI agents to uncover new leads in biological data](https://openai.com/index/scaling-ai-research-for-complex-biological-data) | exclude | exclude | 固定多 Agent 生物数据分析 |
| 38 | [Amp puts AI agents to work beyond code with OpenAI models](https://openai.com/index/amp-beyond-coding) | exclude | exclude | Agent 产品能力与模型选择 |
| 43 | [How Block is building AI-powered security with OpenAI technology](https://openai.com/index/block-ai-powered-security) | exclude | exclude | 人工指导安全系统与外部代码修复 |
| 51 | [Accelerating the search for antimicrobial peptides with Google Antigravity](https://deepmind.google/blog/accelerating-antimicrobial-discovery/) | exclude | exclude | 人引导的抗菌肽发现工作流 |
| 61 | [Gemini 4 Carbon: Our next frontier model](https://deepmind.google/blog/gemini-4-carbon-our-next-frontier-model/) | exclude | exclude | 模型发布与能力评测 |
| 62 | [An updated Model Spec for more capable and beneficial AI](https://openai.com/index/updated-model-spec) | exclude | exclude | 人修订 Model Spec 并训练模型 |

## 30. What FDE means at OpenAI

重构主体明确是 FDE。模型所引 feedback 句来自 Tax AI 案例，复用句来自半导体案例，不能拼成同一个自动更新闭环；固定权重也未得到证明。

原始发布日期：2026-10-22T06:00:00+00:00。建议主题为 `harness`，仅为分类信息；不代表确立 RSI。

来源：[官方全文](https://openai.com/index/forward-deployed-engineering-means)；核验提取文本 SHA-256 `ed2b868c15152d9ca366cec0909100ebc09d4982978a08c8ec93cddada86ef16`。下列行号指当时的提取文本，全文缓存未打包。

> One FDE tested rebuilding their application around it, then worked with the team to move the use cases onto a common harness with Codex at its core.

原文起始行 56；精确换行保存在 JSON 引文中。

> Custom applications became plugins and skills built on common Codex primitives.

原文起始行 57；精确换行保存在 JSON 引文中。

> One of the hardest challenges was automating rental-property returns, which required six weeks of engineering and practitioner review to reach 90% precision and recall.

原文起始行 77；精确换行保存在 JSON 引文中。

待明确/边界：自动编辑主体未证实；不同客户案例的引文不可拼接；模型冻结未证实。

Owner decision: `defer`；publication authorized: `false`。

## 35. Terminal X matches senior investor judgment 88.6% with GPT-6.1

每个失败被编码成 Memory、新 workflow instruction 或 test case，属于应继续查证的线索。然而文中明确说工程师把 Memory 变为工作流，分析师纠错；没有说明 Agent 自动改写并将新程序用于后续独立任务。88.6% 等是模型比较，不是反馈演化效果的隔离实验。

原始发布日期：2026-10-20T07:00:00+00:00。建议主题为 `harness`，仅为分类信息；不代表确立 RSI。

来源：[官方全文](https://openai.com/index/terminal-x)；核验提取文本 SHA-256 `17cd0a45348c412c7eda975c76091020f11942bdf7a2ec54c93b86a23493d523`。下列行号指当时的提取文本，全文缓存未打包。

> Engineers turn each Memory into a repeatable workflow on Terminal X’s platform, where every production query is auditable with its full trail: the steps taken, sources retrieved, model used, and the reasoning.

原文起始行 38；精确换行保存在 JSON 引文中。

> Every fail includes a one-line reason and a better source or corrected text and becomes a Memory.

原文起始行 43；精确换行保存在 JSON 引文中。

> For example, a missed source, a wrong comparable, or a thesis that drifts from the house view is encoded as a new workflow instruction or a new test case for that desk.

原文起始行 43；精确换行保存在 JSON 引文中。

> Every answer gets eval’d, and whatever the analyst corrects teaches the system a little more about how that firm works

原文起始行 44；精确换行保存在 JSON 引文中。

待明确/边界：自动编辑主体不明；指令与测试用例两种更新未区分；更新后程序的后续执行证据不足；权重冻结未证实。

Owner decision: `defer`；publication authorized: `false`。

## 60. How Grupo Boticário uses AI to strengthen human connections

标题和业务中的自主服务能力不能代替自进化证据。原文明说由业务团队管理提示词和 A/B 测试，更新主体是人。

原始发布日期：2026-10-16T00:00:00+00:00。建议主题为 `harness`，仅为分类信息；不代表确立 RSI。

来源：[官方全文](https://openai.com/index/grupo-boticario)；核验提取文本 SHA-256 `e69b510b27860a9bdb48f6282126dd7687862b031aace7a0aa075995908a5cdf`。下列行号指当时的提取文本，全文缓存未打包。

> One of the operation’s distinguishing features is organizational rather than technical: the business team manages prompts on the platform.

原文起始行 54；精确换行保存在 JSON 引文中。

> Sales, customer service, and support teams began managing their own prompts, with continuous incremental improvements based on feedback from daily use.

原文起始行 57；精确换行保存在 JSON 引文中。

> Establish a routine of prompt A/B testing run by business teams.

原文起始行 77；精确换行保存在 JSON 引文中。

待明确/边界：自动编辑被原文中的人工编辑主体反证。

Owner decision: `defer`；publication authorized: `false`。

## 64. How we detect frontier model misalignment

自动调查、告警、暂停任务是固定系统的执行功能。持续评估和部署变更的主体是研究/安全团队；未描述监控程序自动修改自身并保留新版本，也不是专门研究 Harness 演化的评测。

原始发布日期：2026-10-29T09:00:00+00:00。建议主题为 `safety_governance`，仅为分类信息；不代表确立 RSI。

来源：[官方全文](https://openai.com/index/how-we-detect-frontier-model-misalignment)；核验提取文本 SHA-256 `b11986a78160bfeb8dc816aec9bf3c64eafb50cacd1a5a27b72c8f1ca591920f`。下列行号指当时的提取文本，全文缓存未打包。

> In order to make sure that it remains effective, we continually evaluate and improve our monitoring system.

原文起始行 78；精确换行保存在 JSON 引文中。

> We track recall at each threshold on a central dashboard and test how proposed changes to the monitoring system affect recall before deploying them.

原文起始行 79；精确换行保存在 JSON 引文中。

> We believe that some of Sol’s advantage comes from the fact that we optimized the monitoring prompt for it.

原文起始行 99；精确换行保存在 JSON 引文中。

待明确/边界：自动修改监控工件未证实；监控 RL 训练不等于冻结模型的自改进；普通安全评测不是 Harness 演化专项评测。

Owner decision: `defer`；publication authorized: `false`。

## 7. Sakana Chatが覚えていることを見てみよう：メモリを可視化する新機能「My Fish」

原文支持保存事实、偏好并跨会话读取；没有修改记忆管理代码/策略文件的证据，也未建立评估反馈驱动的 RSI 机制。可作为记忆方向产品信息归档，不应宣称已验证 RSI。

原始发布日期：2026-10-14T15:00:00+00:00。建议主题为 `experience_world_model`，仅为分类信息；不代表确立 RSI。

来源：[官方全文](https://sakana.ai/my-fish/)；核验提取文本 SHA-256 `9015eddd0264b1961115e46f08e8bc9be219be1c71d39d6c428c9af0b865a1de`。下列行号指当时的提取文本，全文缓存未打包。

> Memory helps Sakana Chat carry useful context from one conversation to the next.

原文起始行 74；精确换行保存在 JSON 引文中。

> The History view provides a detailed timeline of every read and write.

原文起始行 99；精确换行保存在 JSON 引文中。

> Whenever Sakana Chat reads or saves a memory while composing a response, its thinking process now displays a small chip.

原文起始行 103；精确换行保存在 JSON 引文中。

待明确/边界：修改对象是记忆内容；质量评估驱动更新未证实。

Owner decision: `defer`；publication authorized: `false`。

## 25. How we built ChatGPT’s novel ad stack for user trust and relevance

自改进环明确通过更强模型评价并训练 post-trained LLM/小模型。执行时调用广告检索工具不证明工具或编排自身被自动改写。

原始发布日期：2026-10-21T07:00:00+00:00。建议主题为 `model_weights`，仅为分类信息；不代表确立 RSI。

来源：[官方全文](https://openai.com/index/building-chatgpt-ad-stack)；核验提取文本 SHA-256 `3c48a96e28a4a42ec49e269112d3153294d381edaabfe33532fd9550c941a4b0`。下列行号指当时的提取文本，全文缓存未打包。

> Beyond these reporting and optimization tools, we deploy a high quality model to evaluate our delivery and train other ads models, creating a powerful self-improvement loop.

原文起始行 73；精确换行保存在 JSON 引文中。

> The idea behind model-based evaluation is that our strongest, highest-reasoning models watch and judge the results of our system, then improve the post-trained LLM by training it to perform better.

原文起始行 83；精确换行保存在 JSON 引文中。

待明确/边界：主要更新对象是模型权重；具体训练实验与效果分解未给出。

Owner decision: `defer`；publication authorized: `false`。

## 33. Securing our frontier model training environment

自动发现、去重漏洞与修复训练设施是安全工程；没有根据模型学习反馈自动演化训练任务/奖励，也没有 Agent 自身的可复用 Harness 自动修改闭环。

原始发布日期：2026-10-23T10:00:00+00:00。建议主题为 `safety_governance`，仅为分类信息；不代表确立 RSI。

来源：[官方全文](https://openai.com/index/securing-our-frontier-model-training-environment)；核验提取文本 SHA-256 `0aa3154159fe99af923bcdec8bd2e23ab128fdc4a274215a98fcd4df93e0e41f`。下列行号指当时的提取文本，全文缓存未打包。

> These findings led to software patches, tighter network restrictions, and disclosures to the relevant software maintainers and vendors.

原文起始行 65；精确换行保存在 JSON 引文中。

> We built an automated pipeline to help triage and deduplicate the vulnerabilities and misconfigurations they discovered, with our security and infrastructure teams reproducing findings and verifying fixes to our configurations.

原文起始行 69；精确换行保存在 JSON 引文中。

> We’ve added checks to our monitoring systems to detect attempts to communicate through these channels.

原文起始行 184；精确换行保存在 JSON 引文中。

待明确/边界：安全设施不是文中自动演化的训练任务/奖励；人工复现、验证及修补不可冒充自主 RSI。

Owner decision: `defer`；publication authorized: `false`。

## 53. How Third Moment Research runs 10,000 agents for 36+ hours

正文明确自动生成薄弱点对应的 synthetic scenarios，再由团队用其改进 agents；具体训练手段未知。Codex 优化回测代码是环境/任务产物，固定外层重试逻辑也不等于它会改写自己。

原始发布日期：2026-10-14T07:00:00+00:00。建议主题为 `data_task`，仅为分类信息；不代表确立 RSI。

来源：[官方全文](https://openai.com/index/third-moment-research)；核验提取文本 SHA-256 `546901316e08b4b46dbb117ee40acac81165ada67f5afe29d58b2e1585760eff`。下列行号指当时的提取文本，全文缓存未打包。

> The company is building a self-improving AI system around that idea, using OpenAI’s latest models to understand agent behavior, identify recurring weaknesses, and automatically create thousands of synthetic scenarios around those problems.

原文起始行 32；精确换行保存在 JSON 引文中。

> The team uses those scenarios to improve agents, repeating the process as new issues emerge.

原文起始行 32；精确换行保存在 JSON 引文中。

> The outer harness examines the trajectory when a task is left unfinished and determines whether to retry, terminate the job, or escalate to human review.

原文起始行 44；精确换行保存在 JSON 引文中。

待明确/边界：训练/参数更新方法未知；没有 Harness 修改后保留的证据；未来计划不能当已实现结果。

Owner decision: `defer`；publication authorized: `false`。

## 2. Red-Teaming OpenAI's Internal Agent Monitoring Systems

研究人员测试历史监控覆盖与漏洞，不是 Harness 自改进评测。论文/公告中的后续修复是被测机构声明，METR 明确没有再验证。

原始发布日期：2026-10-22T07:00:00+00:00。建议主题为 `safety_governance`，仅为分类信息；不代表确立 RSI。

来源：[官方全文](https://metr.org/blog/2026-10-22-red-teaming-openai-agent-monitoring/)；核验提取文本 SHA-256 `c0a2db46d0fb3d09dfea1d1fc34d6675d5afef47a1efd6230fe1dc3acebc9cb8`。下列行号指当时的提取文本，全文缓存未打包。

> primarily focused on estimating the fraction of agentic inference that is monitored, and whether agents could in principle disable or subvert the monitoring system.

原文起始行 78；精确换行保存在 JSON 引文中。

> Our findings describe the historical system we assessed on and before July 21st, rather than the expanded system’s current coverage, which this exercise did not establish.

原文起始行 87；精确换行保存在 JSON 引文中。

> We have not evaluated these claims.

原文起始行 107；精确换行保存在 JSON 引文中。

待明确/边界：不是 Harness 演化专项评测。

Owner decision: `defer`；publication authorized: `false`。

## 4. オントロジーを基盤に、意思決定・実行を支援するAIエージェントプラットフォーム「Sakana Aquarium」

平台有 ontology、workflow 和共享基础设施，但未展示依反馈自动改写 Harness 的现有循环。末段更新 ontology/agents 的机制写为正在开发，不能提前收作实现。

原始发布日期：2026-10-22T15:00:00+00:00。建议主题为 `harness`，仅为分类信息；不代表确立 RSI。

来源：[官方全文](https://sakana.ai/aquarium-release/)；核验提取文本 SHA-256 `7c4c57f0ee2856b8e156ff368a4504a1ce1da0a2e88bca87c6370cf230314ea1`。下列行号指当时的提取文本，全文缓存未打包。

> 情報の参照、AIによる判断、関数の実行、人の承認をワークフローとして記述するだけでデプロイでき、エージェントのライフサイクル全体を管理します。

原文起始行 13；精确换行保存在 JSON 引文中。

> 運用の中で生まれる修正や判断を取り込み、組織の変化に合わせてオントロジーとエージェントを更新し続ける仕組みや、エージェントの構築そのものをAIが支援する仕組みの開発も進めています。

原文起始行 38；精确换行保存在 JSON 引文中。

待明确/边界：未来机制不可按现有闭环收录。

Owner decision: `defer`；publication authorized: `false`。

## 8. GPT-6.1 Sol helps CodeRabbit strengthen security across complex codebases

改进对象是用户代码库的漏洞，且发布由人审核；没有修改安全 Agent 自身 Harness 的证据。

原始发布日期：2026-10-26T13:45:00+00:00。建议主题为 `safety_governance`，仅为分类信息；不代表确立 RSI。

来源：[官方全文](https://openai.com/index/gpt-6-1-sol-coderabbit-code-security)；核验提取文本 SHA-256 `58ed582347a3e734a7ee0af6a2db3308059150aa02b803263461d7776aee13ce`。下列行号指当时的提取文本，全文缓存未打包。

> For supported issues, it can draft a pull request with a proposed fix for a person to review and approve.

原文起始行 13；精确换行保存在 JSON 引文中。

> Human reviewers remain responsible for deciding which changes to ship.

原文起始行 14；精确换行保存在 JSON 引文中。

待明确/边界：外部任务产物不等于自身 Harness。

Owner decision: `defer`；publication authorized: `false`。

## 9. Greptile takes bug detection beyond code review with GPT-6 Astra

MCP 提供客户代码知识、减少 revert，以及公司使用 Codex 开发自身软件，都未说明从执行反馈自动更新并保留 Agent 工件。

原始发布日期：2026-10-26T22:00:00+00:00。建议主题为 `harness`，仅为分类信息；不代表确立 RSI。

来源：[官方全文](https://openai.com/index/greptile-code-review-codex-astra)；核验提取文本 SHA-256 `02f6c07379105c0c2ebc29153e3188cd31e10508c4b72db0f2b438c151e1e01f`。下列行号指当时的提取文本，全文缓存未打包。

> Greptile’s Knowledge Base indexes a company’s codebase and documents how it works in a form people and agents can read.

原文起始行 34；精确换行保存在 JSON 引文中。

> Greptile also uses Codex to build its own software and agents.

原文起始行 37；精确换行保存在 JSON 引文中。

待明确/边界：工具使用或开发软件本身不是反馈自改进闭环。

Owner decision: `defer`；publication authorized: `false`。

## 10. How an assessor could investigate evidence of acceleration from the automation of AI R&D

提案研究模型能力、数据、算法、算力与人员的归因测量，可作一般 AI 研发背景；未专门研究 Harness 工件的反馈演化，不能进入 Harness 日报。

原始发布日期：2026-10-14T07:00:00+00:00。建议主题为 `theory_survey`，仅为分类信息；不代表确立 RSI。

来源：[官方全文](https://metr.org/blog/2026-10-14-ai-rd-acceleration-assessment-proposal/)；核验提取文本 SHA-256 `8f38ebcfc698121762323aece1ea6e89c51ef758ba9785c862d3d08faa3c7276`。下列行号指当时的提取文本，全文缓存未打包。

> This article discusses how an assessor could study whether capabilities progress could accelerate dramatically due to AI-driven acceleration of AI R&D.

原文起始行 61；精确换行保存在 JSON 引文中。

> How much of the acceleration in algorithmic progress or data is attributable to AI assistance/automation versus other inputs like experiment compute and labor?

原文起始行 95；精确换行保存在 JSON 引文中。

待明确/边界：讨论 AI 研发不自动构成 Harness 演化专项研究。

Owner decision: `defer`；publication authorized: `false`。

## 27. Using thousands of AI agents to uncover new leads in biological data

任务结果是生物机制解释和候选实验，未改进这些 Agent 自身的 Harness。分布式与单 Agent 对照并非演化前后对照。

原始发布日期：2026-10-21T04:50:00+00:00。建议主题为 `ai4ai`，仅为分类信息；不代表确立 RSI。

来源：[官方全文](https://openai.com/index/scaling-ai-research-for-complex-biological-data)；核验提取文本 SHA-256 `45f600e85e62389d2bd4aeec5e2c410fe719f65dab6c6bc022f01038525e7f46`。下列行号指当时的提取文本，全文缓存未打包。

> Each agent investigated a gene disruption, analyzed cellular responses, searched scientific literature, and proposed explanations for the results.

原文起始行 38；精确换行保存在 JSON 引文中。

> Their reports were combined into a reasoning atlas linking genes, cellular effects, relevant publications, and possible biological mechanisms.

原文起始行 38；精确换行保存在 JSON 引文中。

> Could a single agent given the entire dataset do just as well as thousands of agents working in parallel? We tested this while keeping the model and resources fixed.

原文起始行 53；精确换行保存在 JSON 引文中。

待明确/边界：科研任务产物非 Agent 自身工件。

Owner decision: `defer`；publication authorized: `false`。

## 38. Amp puts AI agents to work beyond code with OpenAI models

模型升级、多 Agent 启动、设计/写作/编程能力均没有形成可验证的 Harness 持续改写闭环。

原始发布日期：2026-10-14T12:00:00+00:00。建议主题为 `harness`，仅为分类信息；不代表确立 RSI。

来源：[官方全文](https://openai.com/index/amp-beyond-coding)；核验提取文本 SHA-256 `5203b03c0172f7e5ee1bbe23529864ddd97e0d0d3fe93df345eac10e1102560c`。下列行号指当时的提取文本，全文缓存未打包。

> Amp chooses and recommends models based on what works best for its users, and OpenAI models account for the majority of tokens used in Amp.

原文起始行 21；精确换行保存在 JSON 引文中。

> Users can ask Puck to start an agent to investigate a bug, coordinate several agents, or find a previous conversation about a technical problem.

原文起始行 35；精确换行保存在 JSON 引文中。

待明确/边界：多 Agent 编排功能不是编排自修改。

Owner decision: `defer`；publication authorized: `false`。

## 43. How Block is building AI-powered security with OpenAI technology

有历史遥测回放评估和 Agent 验证，但团队调整方案，人类指导并部署代码；未证实 Agent 根据反馈演化自身 Harness。

原始发布日期：2026-10-14T07:00:00+00:00。建议主题为 `safety_governance`，仅为分类信息；不代表确立 RSI。

来源：[官方全文](https://openai.com/index/block-ai-powered-security)；核验提取文本 SHA-256 `085750469ebadba9970d97dfbec935bbc662bedf3f67184264c14cec4778cf1b`。下列行号指当时的提取文本，全文缓存未打包。

> The team continually evaluates these systems against internal benchmarks and real-world performance, adjusting its approach when needed, including routing work to human review when that is the responsible path.

原文起始行 34；精确换行保存在 JSON 引文中。

> You propose a patch, you confirm exploitability, and then you verify that you have fixed it, with a human in the loop guiding it and deploying the code changes.

原文起始行 40；精确换行保存在 JSON 引文中。

待明确/边界：被评估的固定 Harness 不等于自进化 Harness。

Owner decision: `defer`；publication authorized: `false`。

## 51. Accelerating the search for antimicrobial peptides with Google Antigravity

交互式科学分析中人选问题和证据，Agent 完成数据库、结构与文献分析。产物是待湿实验验证的候选肽，没有 Agent 程序更新。

原始发布日期：2026-10-15T16:08:03+00:00。建议主题为 `ai4ai`，仅为分类信息；不代表确立 RSI。

来源：[官方全文](https://deepmind.google/blog/accelerating-antimicrobial-discovery/)；核验提取文本 SHA-256 `2fcaaae0356daf32fd9c24aab9802d47d0e57115d497405513d14107786c6715`。下列行号指当时的提取文本，全文缓存未打包。

> During an interactive, multi-turn session the researcher steers the scientific strategy, deciding which questions to ask and what evidence to collect, while the agent handles the heavy lifting of cross-database orchestration, structural analysis, and literature synthesis.

原文起始行 25；精确换行保存在 JSON 引文中。

> The candidate we uncover in this walkthrough represents a biologically plausible lead backed by structural and genomic evidence but it still requires wet lab validation.

原文起始行 44；精确换行保存在 JSON 引文中。

待明确/边界：当前任务中的多轮分析不是跨任务程序改进。

Owner decision: `defer`；publication authorized: `false`。

## 61. Gemini 4 Carbon: Our next frontier model

更新的是模型能力与训练；长时任务持续执行没有证明自改写 Harness，也没有在公告中隔离 RSI 环路。

原始发布日期：2026-10-28T17:00:58+00:00。建议主题为 `model_weights`，仅为分类信息；不代表确立 RSI。

来源：[官方全文](https://deepmind.google/blog/gemini-4-carbon-our-next-frontier-model/)；核验提取文本 SHA-256 `8c4fe8bb04e9f2c2929286a64b55e3be15eaa859a8a523c03eea80fd3b9b6f82`。下列行号指当时的提取文本，全文缓存未打包。

> Today, we’re announcing the next frontier model: Gemini 4 Carbon, our strongest model with state-of-the-art cybersecurity and long horizon capabilities.

原文起始行 18；精确换行保存在 JSON 引文中。

> With Carbon, we challenged ourselves to go a step further on alignment, and trained the model to respond to complex or high-pressure tasks in the right way.

原文起始行 57；精确换行保存在 JSON 引文中。

待明确/边界：模型发布不是 Harness 演化。

Owner decision: `defer`；publication authorized: `false`。

## 62. An updated Model Spec for more capable and beneficial AI

原文主体是 OpenAI 写规范和训练模型，无自主 Harness 更新。模型引文仅在空白归一化后匹配，原始文本严格子串校验失败，需记录验证口径。

原始发布日期：2026-10-29T17:00:00+00:00。建议主题为 `safety_governance`，仅为分类信息；不代表确立 RSI。

来源：[官方全文](https://openai.com/index/updated-model-spec)；核验提取文本 SHA-256 `374c8cf5aff2218f793483a1b54cbcb2a4d1c65ded56223e9626c3e2beca1acd`。下列行号指当时的提取文本，全文缓存未打包。

> OpenAI writes the Spec, sets boundaries, and trains models to respect them; developers direct applications within those boundaries; and users direct the model’s work subject to those constraints.

原文起始行 35；精确换行保存在 JSON 引文中。

> This update is another step in our work to refine the Spec through research, experience deploying models, public feedback on the Spec and model behavior, and discussions with users and outside experts.

原文起始行 28；精确换行保存在 JSON 引文中。

待明确/边界：原始子串与空白归一化匹配需区分。

Owner decision: `defer`；publication authorized: `false`。

结构化证据及原始模型建议见 [labs-scope-review.json](labs-scope-review.json)；返回 [审核索引](INDEX.md)。
