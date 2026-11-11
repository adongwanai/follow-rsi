# 2026-11-11 免费来源采集与独立审查交接

交接生成：2026-11-11T00:33:06.846992+00:00。实际维护日为北京时间 2026-11-11，不能将延迟触发的 11/09 heartbeat 日期当作今日。

## 冻结范围与处理状态

本子 agent 只写 build/maintenance-2026-11-11/source-intake；未调用付费模型，未修改 production/data/review/site，未执行 Git/GitHub 写入。主 agent 的并行整合与发布不在此断言范围内。

基线 main/HEAD：`48b8e7a01f35f4808003294ee83f959a9eb9f762`；规范库 1880 条，SHA-256 `93bd42b6d47f74bd0a9dcd4f5ff73579eb1a68a19c31f0c0ec8428fc108bca46`。所有 source/raw、proposal、初稿、终稿已冻结；此交接和 QA 是追加报告。

12 路启用来源全部实际尝试并结束。原始 5874 occurrences / 5575 IDs；配置窗口 437 occurrences / 404 IDs；新入库候选 64 项（57论文、7官方文章）；旧记录 HF 归期增补1项；身份碰撞0。这里的“新”是相对基线规范库，不等于论文今天发表。

64 新项逐条范围建议已完成：纳入 7、排除 54、待补 3。formal_decision 仍 defer，因为这些文件是审查建议而非正式审核凭据；并非64项尚未处理。由主 agent 结合其他审查轮次执行有授权的真实审核、PR与出版流程。

## 来源实测

| 来源 | 状态 | HTTP请求 | 窗口条数/ID | 说明 |
|---|---|---:|---:|---|
| arxiv-harness | ok | 1 | 0 / 0 | 该路本次请求已完成 |
| arxiv-rsi | ok | 1 | 0 / 0 | 该路本次请求已完成 |
| arxiv-adjacent | ok | 1 | 0 / 0 | 该路本次请求已完成 |
| s2-citations | partial | 52 | 314 / 283 | ValueError: BoundedSourceTraversal: source reached the 180-second attempt window; successful responses retained; unvisited coverage is unknown. |
| s2-authors | error | 7 | 0 / 0 | HTTPError: 429 Client Error:  for url: https://api.semanticscholar.org/graph/v1/paper/arXiv:2310.02304?fields=authors |
| hf-daily | historical_boards_ok_today_not_ready | 3 | 71 / 71 | {'2026-11-11': 'not_ready: HTTPError: 400 Client Error: Bad Request for url: https://huggingface.co/api/daily_papers?date=2026-11-11'} |
| rss-sakana | ok | 1 | 2 / 2 | 该路本次请求已完成 |
| rss-metr | ok | 1 | 4 / 4 | 该路本次请求已完成 |
| rss-openai | ok | 1 | 40 / 40 | 该路本次请求已完成 |
| rss-deepmind | ok | 1 | 6 / 6 | 该路本次请求已完成 |
| rss-weco | ok | 1 | 0 / 0 | 该路本次请求已完成 |
| github-releases | ok | 13 | 0 / 0 | 该路本次请求已完成 |

HF 11/11 请求于 00:07:53 UTC 返回 HTTP400 not_ready，并明确 available_through=11/10。完整取回11/10榜37项及11/09榜34项。11/09此前31项，新增晚到成员 2611.09124、2611.10404、2611.01729，全部保留真实推荐日期和实际 first_seen，不重新标为11/11。71名成员全部对账，无关键词预筛。

S2匿名模式：引文52请求（42×200、10×429），180秒有界停止，未遍历部分覆盖未知；窗口314条/283 IDs。collector原报318，另4项日期晚于目标日，已在原始对账中保留并排除窗口。作者7请求（1×200、6×429），未获得论文记录；429在初次失败后最多重试5次。两路共享限速，实测最短dispatch间隔3.101196833秒，满足≥3.1秒。

## 正文、日期与原始证据

官方 arXiv 元数据88/88；56新arXiv的题名、摘要、发表/版本日期、版本号全部对齐。正文52份HTML200，4份HTML404已用官方带版本PDF200补齐（2501.08686、2611.12885、2611.09195、2611.12806）。56份正文版本全部核验。12份原HTML请求未带v且receipt当时版本为空，原receipt保留；另用HTML内嵌版本与官方metadata对照。7篇官方文章均200。

Materials world models 的 DOI/Crossref/出版商PII身份一致；Crossref只有2026-11月份，S2/OpenAlex的11/01不能当作已核实官方日。OpenAlex摘要可读，ScienceDirect403、Elsevier text API401，官方正文仍受阻。单独的 materials-suggested-provenance.json 给出 metadata_pending=true、official_published_day=unknown、official_published_precision=month；没有为此改proposal或source_hash。

32项旧metadata差异不自动覆盖。实际版本变化2项：SplatAnything 2611.08264 v1→v2（摘要也变）、PCBRouteAgent 2611.08175 v1→v2。其余主要为作者姓名格式与comments补充，详见metadata-change-triage.json。

ReproBridge 2611.08452 仅新增HF 11/10 membership。现官方题名、摘要、发表/版本日期与版本号和旧审核一致；旧证据body hash已复核，复用摘要范围排除意见。原first_seen和旧PR/merge/approval hash不变；新来源hash须有新审核条目，不能把旧批准hash改写为新hash。详见review-reuse-delta.json。

SMO 2611.12041存在来源自身数字冲突：官方Atom摘要写59.3× reduction，HTML摘要写59.3% reduction。两种原文原样保留，不修改论文数字。

## 独立审查与纠正历史

初稿在读取主审/第三方结论前冻结（8纳入/54排除/2待补）。终稿在收到反证后直接重读原文，记录每个变更字段，最终7/54/3。终稿不伪称第二次盲审。

- REINS：初稿include→最终exclude。固定模板解释器中新增领域驾驶规则，更新对象为经验内容；Def3.2/3.5/3.6/3.7及§4.2原文提供直接依据。不是将有界模板一概排除。
- Auriga：初稿exclude→最终borderline。确实修改和保留共享Harness，但自动修改者/生成/准入仍unknown；不得据未知认定人工开发。
- ReSkill：维持exclude。自主修订与执行反馈成立，更新的是外部可独立执行的机器人policy，而非开发Agent自身Harness。
- Sage-Taiyi：borderline，概念repertoire自改与实例/未来工作存在证据缺口。Materials：borderline，官方正文受阻。

建议纳入：

- arxiv:2611.12552 — SciMARS: Multi-Agent Recursive Self-Improvement for Closed-Loop Scientific Discovery：SciMARS 明确改变角色规程、协调契约和可选记忆管理策略，执行候选后选择并保留下一轮 Harness；按现行定义“后续任务或改进轮次”，其任务内跨改进轮次的 Harness 更新可收。
- arxiv:2611.11499 — JoMoHa: Joint Model--Harness Optimization with Reinforcement Learning：JoMoHa 不仅训练两个模型：Engineer 根据历史反馈生成可执行 Harness，程序与 Solver 均跨轮保存；不同保存程序在固定 Solver 下被交叉评估，部署选择保存程序。符合权重与外部 Harness 双方反馈更新和保留。
- arxiv:2611.12068 — MIRIX-2.0: Multi-Agent Memory System：仅 AutoDream 的procedural refinement可纳：它根据带原文引用的session outcome创建、编辑或删除可复用skill，改变actor可用的操作指令。语义记录与图索引合并本身不算Harness演化。
- arxiv:2611.12885 — World In-Context Learning for Agentic Robot Manipulation：RoboScript 的§4.1有独立Harness证据：coding agent为动作接口缺口写可复用skills，driver执行原场景与其他布局验证，循环到coverage停止提升后冻结，供Agent后续任务学习与部署调用。Task Memory及反思仍须另标经验内容，不将整篇所有记忆都算Harness。
- arxiv:2611.10542 — When Experience Becomes a Backdoor: Poisoning Self-Evolving LLM Agents via Failure-Aware Task Optimization：BadEvolve 直接评测执行经验如何经trusted evolver变成持久skills后门；evolution、attack validation和test分离，目标就是Harness技能演化，属于专项安全评测。
- arxiv:2611.10787 — Trustworthy Recursive Self-Improvement with Statistical Guarantees：TRUST研究Harness更新的统计准入：迭代候选从reasoning/routing/memory/workflow操作产生，检验决定替换incumbent，保持跨轮历史；可收准入方法与专项理论。
- arxiv:2611.10022 — How Much Skill Orchestration Can LLM Agents Compile Away? Execution-Grounded Specialization for Token-Efficient Skill Use：SkillCache 把执行轨迹编译成模型外可复用capsule程序和步骤，执行replay失败后反馈给compiler修复（最多三轮），通过才用于后续warm调用；不是单纯缓存原答案。

## 实际验证

`.venv/bin/python docs/internal/reports/maintenance-2026-11-11/check-intake.py` 已退出0：20项离线证据校验全通过，273份文件hash、102段独立稿原文引用的位置/原始文本、64项source_hash、56正文版本、71HF成员和first_seen保护均通过。S2请求过滤的QA实现曾误计其他来源的dispatch；已限定Semantic Scholar域名后重跑通过，未改采集数据或放宽阈值。

这证明保存的来源与建议绑定一致，不代表论文实验复现、线上发布完成或所有来源遍历完整。正式测试、构建、审核PR与线上验证由主维护流程执行。

## 关键文件

- `integration-proposal.json` — SHA-256 `2e18fb664483d6a0aa8a1626fc028e4bfd10c355be685a49c059d8f76993dcdd`
- `all-source-snapshot.json` — SHA-256 `b9a7eff8cee6aa3fd400f5a5491657e8e6444ea5c0b188f8dcaaf32e56b3f20d`
- `raw-source-id-reconciliation.jsonl` — SHA-256 `2dd0ab938f1aa16e2c21df03d0a81d71cd8bd4bc5b55a4ad874e6f7796941a75`
- `independent-review-initial.json` — SHA-256 `63308301465bcf779c4b383ab55f306adc4ef7099174f8a0dc8512667f75bc4e`
- `independent-review-final.json` — SHA-256 `4b6098f2713fd60aba200135227b2b84cc9c3c1ecde57d6dd2764b6f7e5fd343`
- `review-reuse-delta.json` — SHA-256 `e9fa25131fbdfea60b836ccaa50bebd3189362932effc5f25743c64440752fc6`
- `hf-board-reconciliation.json` — SHA-256 `c966726ec2cab621d37757e6036e392749221fc0af93225506f69cedfa6d207d`
- `fulltext-version-verification.json` — SHA-256 `224d43337631358b2ff6b7161f68fb8ed28cf2ec89435a7bb2a89d977c6256ec`
- `metadata-change-triage.json` — SHA-256 `6dc3c0f9ecf9ff1f1827dab0ffcf7789c6506c5d4f72049c3c5805028bd0eda4`
- `materials-doi-review.json` — SHA-256 `5e6d5a3931b38c798ce5e11869adb3f5a13c29162985de60857aa04ddc1718b1`
- `materials-suggested-provenance.json` — SHA-256 `85cefbf5888848eba6660abbbf58c882154b9d9f5f202eddf20ba0574f95487f`
- `intake-qa.json` — SHA-256 `888f635e6f0daeaf4884f9ea92046b3fc69464559e5a539fe72ee4ee9214f447`
