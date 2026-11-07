# 57 条旧建议的当前判据复核：独立主审

57 条全部已形成范围建议：**include 0、exclude 57、unknown 0**，无未处理项或外部来源阻塞。这里的 exclude 只是“不进入当前 Harness RSI 专题”的建议，不否认其他方向的价值。全部 `decision=defer`、`publishable=false`，等待独立复审和人工审核。

输入为 `build/maintenance-2026-11-02/prior-rule-input.json`，没有旧 `llm` / `gate` 判断。本次冻结前未读同批另一代理结论。输出中的理由与引句逐条重新选择，未将历史判断当作证据。

## 来源和阅读范围

- 新请求官方 arXiv Atom，取得 52 条与 canonical 相同固定版本的摘要、题名与日期。
- 对 CausGround、What Effort Level Should I Choose?、Rare, Relevant, and Still Wrong 补取并阅读固定版本正文方法段，分别核对因果知识、运行时重试和固定记忆选择策略的边界。
- 1 条综述使用已记录哈希的 Springer 官方摘要；1 条 Sakana 文章使用已记录哈希的官方正文。
- 3 条 OpenAI 资讯使用本轮抓取的官方 RSS 描述，明确标注未读全文，不推断产品内部实现。
- 共保留 78 段连续原文引句；校验覆盖 7 个原始响应文件、60 个摘要/正文文本文件。

常规模型训练、生成模型和领域基准，依据官方摘要明确的主要研究对象完成范围排除，没有把“未读全部正文”写成“已证明不存在任何辅助 Harness”。数值未逐表审计或复现。

## 三个重点边界

| 工作 | 本次建议 | 正文依据 |
| --- | --- | --- |
| CausGround · 2610.29702 | exclude，experience/world model | §3.2–3.3 抽取、留存和检索的是环境动作前置条件与效果；固定框架为冻结 planner 提供世界知识。知识可跨任务复用不等于反馈改写管理代码或策略工件。 |
| What Effort Level Should I Choose? · 2610.34491 | exclude，相关推理预算评测 | §3.4 与附录 H 从既有运行重建固定 laddering：低档失败后高档重试。反馈改变当前任务的重试分支，没有保留新策略程序。 |
| Rare, Relevant, and Still Wrong · 2610.37624 | exclude，相关记忆评测 | 第 3 节比较固定摘要/事实挑选策略对当前讨论决策的影响；不是记忆管理策略经反馈演化的专项评测。 |

基准和理论的排除理由均按研究对象判断，不要求基准本身必须自我修改。

## 数据问题：报告但未改写

`post:/us-midterms-analysis/` 与 `post:https://sakana.ai/us-midterms-analysis/` 指向同一 Sakana 官方文章，标题、摘要、发表时间、更新时间和链接逐字段一致。短 ID 是同一来源的重复记录，不应算两篇或两次新增。详细比对见 `duplicate-report.json`；本次没有合并、删除或修改 canonical。

7 条 canonical 摘要与官方 Atom 有 LaTeX/数学排版差异（如美元符号、`\\emph`、`\\textbf`、`\\times`），逐条保留差异，不修改数字或元数据。

## 交付与校验

`findings.json` 的 `records` 使用主线程要求的字段：`id`、`scope_recommendation`、`reason_zh`、`reading_scope`、`source_quotes`、`external_blockers`、`canonical_source_hash`、`decision`、`publishable`；另外保留来源、类别、重复记录报告和数字审计边界。

`validation.json` 已通过：57 个 ID 恰好覆盖输入，57 个 live canonical hash 不变；52 个官方固定版本条目身份一致，78 个引句为连续原文子串，全部来源哈希通过。前两批 primary-a 与 metadata-reconciliation 报告仍保持冻结。此子任务未改 canonical、代码、Git 或旧报告，未调用付费 API，未进行 GitHub 操作。

`findings.json` SHA256：`10e92401a396e60f2bc79ad8e5ae35174343848d403034ba167798ad27602278`。

来源与可重跑脚本保留在 `build/maintenance-2026-11-02/prior-rule-primary/`；仓库测试和发布闸门由主线程负责。
