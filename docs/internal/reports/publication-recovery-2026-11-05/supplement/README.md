# 历史出版候选：MemSteer、GEPA-Curator、MetaVul

生成于 2026-11-05T08:44:33.196149+00:00。三篇现有官方缓存、范围主审/独立复审与当前 canonical 已核对；本目录只提供新摘要候选，尚待针对这些精确文本的独立第三轮复核。`supplement-ready` 不是批准或发布状态。

| 候选 | 日期归属 | 方向 | 当前状态 |
|---|---|---|---|
| MemSteer (`2610.39276`) | HF 2026-11-02 历史补登 | harness/component | defer，待摘要独立复核及正式出版条件 |
| GEPA-Curator (`2610.37651`) | HF 2026-11-02 历史补登 | harness/evidence_selection | defer，待摘要独立复核及正式出版条件 |
| MetaVul (`2610.40721`) | HF 日期未验证；历史 issue 候选，暂不分配出版日 | harness/evolve_main | defer，待摘要独立复核及正式出版条件 |

两篇 HF 补登应保留 11/02 原有三篇、真实 first_seen 与原始日期证据，不挪入 11/03、11/04 或今天。MetaVul 的 canonical `hf_daily_dates=[]`，本包没有给它推断推荐日。

本次只读校验了 42 个引句绑定（含重复来源的独立审核绑定）、3 份官方身份/版本/首发历史、2 个 HF 成员身份；三份 canonical 摘要与官方 abs 精确相同。所有新短摘要少于 60 个 Unicode 字符、30 个英文空格分词，未使用结果数字。细节、来源 SHA256、段落/引句 hash、当前 source_hash 和 claim 映射均在 candidate-package.json。

## MemSteer

依据执行失败诊断修订存储、检索与上下文设计，经验证择优保留，并冻结设计跨基准复用。

Revises storage, retrieval, and context designs using execution diagnostics, retains validation improvements, and transfers frozen designs across benchmarks.

官方缓存首发 `2026-10-29T03:28:49Z`，审核版本 v1；当前 source_hash=`5d59b95c1bbe5aaf41d8d3161cacf422d86e6e4631a9c0f8ee0c01a4048bdb97`。中文 41 字符、英文 18 词。

关键边界：收录依据是存储、检索和上下文管理机制的修订；合成 QA 和记忆条目本身不是 Harness 演化。 只描述已在原文核实的设计复用；不宣称普遍泛化、各组件因果贡献或同预算优势。 未审实现代码、复现实验或复算全部数值。短摘要无结果数字。

当前缺口：正式集成前处理 canonical 日期精度：官方首发为 2026-10-29T03:28:49Z，当前 published/updated 仍是 2026-10-29；保留真实 first_seen，任何规范化都重新绑定。

## GEPA-Curator

策展任务与轨迹以修订提示和 Harness 代码，迭代保留候选并按验证表现选优。

Curates tasks and trajectories for feedback-driven prompt and harness-code revisions, carries candidates through iterations, and selects final versions by validation performance.

官方缓存首发 `2026-10-27T17:58:11Z`，审核版本 v1；当前 source_hash=`9933e01e9e4cef966b00ce3b20860bfe8a39d42c38d47aac4eaa333931883a39`。中文 40 字符、英文 21 词。

关键边界：prompt 主实验为单 lineage 的 greedy 版本：每次 mutation 都进入下一 checkpoint，周期验证后最终择优；不能描述成每步只接纳上涨。 代码扩展是 Meta-Harness-Curator：新执行反馈用于修订，子候选均在完整开发集上评价。 固定的 Curator/优化器包装不是改进器自身演化；不标 harness/improver。 正文没有明确证明所有模型参数冻结；该项为 unknown。旧自动 gate 的 model_frozen=yes 是历史输出，不在此升级成已核实事实。 未核代码实现、复现实验、成本公平性或重算数值。

当前缺口：透明保留既有自动 borderline 及 persists_across_tasks=unclear；正文正证支持人工范围建议，但必须通过系统支持的正式审稿/覆盖路线，不能伪造新模型输出。

## MetaVul

用漏洞与修复函数对的反馈修订 Python Harness，保留候选并以冻结版本评测未见数据和模型。

Refines Python harnesses from vulnerable and patched function feedback, retains candidates, and evaluates frozen harnesses on unseen data and models.

官方缓存首发 `2026-10-29T04:30:42Z`，审核版本 v1；当前 source_hash=`eb5d28faa821e09695aebbe16b9c344b54647d033a91bdc78f9e3f336ec2c18f`。中文 50 字符、英文 20 词。

关键边界：独立 Python Harness 包裹检测 Agent，区别于修改外部目标代码的一次性修复循环。 官方 abs 与 HTML 正文摘要存在措辞差异；两种来源分别绑定，正文引句不冒充摘要引句。 Pareto 保留不是每个指标逐步单调提高；held-out/跨模型描述是评测协议，不声称所有候选都提高。 未复现实验或复核所有数值。原文报告的增益上界不能改写为平均增益；本摘要无数字。

当前缺口：没有已证实的 HF 推荐日；保留 hf_edition_date=null 与 canonical hf_daily_dates=[]，走历史候选/issue 正式审核路线，不归入 11/02、11/03、11/04 或 11/05 HF 日报。

MetaVul 当前缓存正文足以支持本包的非数值摘要：Python 工件、成对函数反馈、历史/Pareto 保留和冻结后未见数据/模型评测均有已校验原文。没有将未查的代码实现、完整实验或数值认作已完成；若后续文案加入新主张，须另补对应原文。

三篇共同尚缺：独立复核本包新摘要；实际支持的正式逐项审核/provenance；有效全局质量闸门；最终内容变更后的 hash 绑定；历史发布流程与真实部署核验。MemSteer 日期目前只有日精度，正式集成时若规范化，须显式记录并重新绑定。GEPA 的既有自动 borderline 与正文范围 include 分开保留。

生成时生产 gate 快照：2026-11-05T07:48:01.387561+00:00，thresholds_passed=False，Harness recall=0.8929。主任务的新真实评测由主任务另行处理，本包不执行、不提升该结果。

操作边界：新增/更新本目录的 candidate-package.json 和 README.md；0 网络请求、0 付费调用、0 GitHub 写操作，未修改 canonical、production 或 review。可交独立第三轮复核，复核对象须绑定 candidate-package.json 的精确 hash。

candidate-package.json SHA256: `5e673874f7b43c4b3aa1557cca1dc5a1344b7d6a3c395b0399e9093511f5bf39`
