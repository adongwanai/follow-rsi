# 2026-10-30 元数据阻塞复核

核对时间：2026-10-30T06:34:31.209993+00:00。读取当前 feed 的 9 条 `llm.error.stage=metadata`，先复用已存在的官方来源请求记录；没有重复联网请求，也没有修改 canonical、旧 owner 决定或发布内容。

**结论：8 条仍缺官方摘要；1 条 IEEE 编者按已有官方全文、但没有摘要节；另发现 TAO 的 pending/429 是成功核实后的残留状态。** 本轮新增摘要 0 条。缺摘要不等于被证明无关，更不能仅凭标题判定 Harness RSI。

## 仍缺摘要的 8 条

这些条目此前均已尝试 Crossref、DOI 跳转、ScienceDirect 与 Elsevier 官方 API。ScienceDirect 返回 403/CAPTCHA；Crossref 无 abstract，API XML 没有非空 abstract/description。复验全部 35 份历史 HTTP 响应的 SHA-256 通过（包含下方 IEEE 3 份）；本轮不重复已经明确阻塞的请求。

| 论文 | DOI | feed 保存日期 | 官方日期口径 | 处理 |
| --- | --- | --- | --- | --- |
| Self-generated goals in the age of foundation models: artificial autotelic agents and their implications for cognitive science | [10.1016/j.cobeha.2026.101684](https://doi.org/10.1016/j.cobeha.2026.101684) | 2026-12-01 | 卷期 2026-12；API：December 2026 | 保持来源阻塞 / defer |
| From world model capability to continued play intention: The mediating role of perceived NPC intelligence and the moderating role of anthropomorphism | [10.1016/j.entcom.2026.101258](https://doi.org/10.1016/j.entcom.2026.101258) | 2026-12-01 | 卷期 2026-12；API：December 2026 | 保持来源阻塞 / defer |
| Giving stateless agents a sense of time: A reconsolidating episodic–semantic memory architecture | [10.1016/j.knosys.2026.117193](https://doi.org/10.1016/j.knosys.2026.117193) | 2026-11-01 | 卷期 2026-11；API：4 November 2026 | 保持来源阻塞 / defer |
| Liability for rogue behaviors of agentic AI | [10.1016/j.telpol.2026.103339](https://doi.org/10.1016/j.telpol.2026.103339) | 2026-11-01 | 卷期 2026-11；API：November 2026 | 保持来源阻塞 / defer |
| Artificial intelligence design agent for automated operation of structural software using knowledge graphs and numerical models | [10.1016/j.autcon.2026.107144](https://doi.org/10.1016/j.autcon.2026.107144) | 2026-10-01 | 卷期 2026-10；API：October 2026 | 保持来源阻塞 / defer |
| Musubito: Deterministic Execution Lineage for AI-Enabled Python Workflows | [10.1016/j.scico.2026.103571](https://doi.org/10.1016/j.scico.2026.103571) | 2026-10-01 | 卷期 2027-02；API：February 2027 | 保持来源阻塞 / defer |
| Mechanism design meets large language models: Foundations and frontiers | [10.1016/j.slads.2026.100033](https://doi.org/10.1016/j.slads.2026.100033) | 2026-10-01 | 卷期 2026-10；API：Available online 7 October 2026 | 保持来源阻塞 / defer |
| Agentic AI: Philosophical, Technical, Psychological, and Marketplace Perspectives on Delegated Agency | [10.1016/j.copsyc.2026.102487](https://doi.org/10.1016/j.copsyc.2026.102487) | 2026-10-01 | 卷期 2026-10；API：Available online 26 October 2026 | 保持来源阻塞 / defer |

日期问题只报告，不自动修值：Crossref 对这批条目只给卷期月份，不能补成 1 日。Musubito 的 feed 为 2026-10-01，但官方卷期为 2027-02；Mechanism design 与 Agentic AI 的 API 分别明确写 Available online 7 October 和 26 October 2026，应与卷期、S2 原值分列。其它 coverDate 不是已核实首次上线日。

## 已有全文、没有摘要节的 IEEE 编者按

[Agents Act. Who Decides? [Editor's Remarks]](https://doi.org/10.1109/mci.2026.3726101)，DOI `10.1109/mci.2026.3726101`。官方 [3 页 PDF](https://xplorestaging.ieee.org/ielx8/10207/11740818/11740826.pdf?arnumber=11740826) 在之前的请求中已返回 200；PDF SHA-256 `8a2d0ac6eb4180ea7f25627ecf509e1c4008faec2039686525827da8f22e7518`。

已读现有三页提取全文，正文为 Editor’s Remarks，没有独立 Abstract 节。因此它的阻塞来自“每条必须有摘要”的处理方式，不是全文来源不可得。不能将自写摘要伪装成原始 abstract；若流程支持，应该用明确标注的官方全文进入单独范围审查。

> Date of current version: 8 October 2026

该句逐字存在于 PDF 第 1 页；卷期为 November 2026。当前版本日、卷期月份和首次上线日是三个不同字段，首次上线日仍 unknown。没有新增 owner accept。


**全文范围建议：不纳入 Harness 专题，仍为 defer。** 这是一篇计算智能与 Agent 决策的编者评论，回顾搜索、优化、能耗和可信决策。它引用程序搜索、AlphaEvolve 等既有研究，没有提出或专项评测新的反馈驱动 Harness 持续改写机制。此建议只针对当前专题，不扩展为“与所有广义 RSI 无关”。

原文短引文（仅合并换行；JSON 保留逐字原文、页码和提取哈希）：

> We have gotten very good at building systems that act, and much less good at making sure they decide well.

PDF 第 1 页。

> evolutionary loops are being wrapped around the models themselves

PDF 第 2 页。

> new mathematical constructions found by program search [6]

PDF 第 2 页。

> The Question for 2027

PDF 第 2 页。


## TAO：成功核实后残留的状态

[TAO: Tool-Aware Joint Scheduling for LLM-Based Agentic Serving](https://arxiv.org/abs/2610.37230v1) 的官方 Atom 已于 2026-10-30T03:11:30.792824+00:00 成功返回。本轮复验标题、完整摘要、published、updated 与当前记录均逐字段一致，Atom SHA-256 为 `6faa2b7bada4af601b0bf6f491782c9aa9f6283fae30a31fd1f8f9023cb579f7`。

- 原始提交 / 版本日期：2026-10-27T13:38:44Z。
- HF 推荐榜日：2026-10-29，不是本轮复核日 10 月 30 日。
- 当前仍残留 `metadata_pending=true` 和旧 arXiv 请求的 HTTP 429。
- 建议把 pending 置为 false，将旧错误保留在核验历史后清除活动错误；已有摘要、日期、分类与 owner 决定保持原样。本文件只给修正建议，未写 canonical。

## 来源记录与复核边界

[metadata-blockers.json](metadata-blockers.json) 保留全部 9 条的官方 URL、请求时间、HTTP 状态、SHA、月份精度、旧字段和阻塞原因，并附 TAO 成功 Atom 证据。`build/...` 路径只表示本地核验缓存，审阅无需依赖缓存才能看到官方入口。

没有发现“已有可用官方摘要却尚未尝试”的剩余条目；该结论限于现有来源记录，不等于证明互联网上绝无其他作者版本。全部新建议保持 defer；元数据身份核实不代表 Harness 分类或发表已获批准。
