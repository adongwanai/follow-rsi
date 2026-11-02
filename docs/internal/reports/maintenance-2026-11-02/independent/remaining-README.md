# 2026-11-02 遗留来源与边界：独立复审

本批 15 条已全部给出建议或明确外部阻塞。在冻结前未读主审的 remaining-source-review/findings.json。所有 decision 为 defer，不构成人工批准或自动发布。

结果：**1 include / 3 exclude / 11 unknown**。其中 8 条取得论文/关联预印本/作者仓库内容并完成评估，7 条只有身份元数据、缺原始摘要或正文而外部阻塞；另 4 条虽有内容仍有分类边界待补证。这些状态分开记录，没有用统一 defer 掩盖缺证。

| 记录 | 建议 | 理由与缺口 |
| --- | --- | --- |
| `arxiv:2610.37935` | exclude | SkillMem 的可训练对象为每个技能的潜向量和共享神经 reader；文本技能先由校准轨迹抽取再做行为蒸馏。已读方法与附录没有外部程序按后续执行反馈反复修订的环；冻结 backbone 不等于没有训练模型组件。 |
| `arxiv:2610.38329` | unknown | 主要接受对象是加速器 kernel，编译规则属于目标知识。正文还记录从 beam 转 single-head、判断器与 anti-cheating 规则调整，且代理写过 loop 代码；但作者同时写明 operator 请求/批准，公开仓库缺编排代码和运行记录，无法独立归因于反馈驱动的自主 Harness 版本迭代。 |
| `arxiv:2610.39158` | include | VEvo-Harness 将修复轨迹蒸馏为可路由技能和生成指令，对候选技能 patch 做图像反事实对照后才写入持久库，并按后续使用反馈保护/修订技能内容。外部行为工件、执行反馈与跨后续生成保留均有正文支持。 |
| `arxiv:2610.39714` | unknown | MoLRSI 的搜索主循环以分子模型/科研 workflow 为产出，所谓 effective search policy 通过三类经验记忆更新，选择公式本身未改。正文另有资源技能的执行报错修复、验收和保留，不能简单归为只有经验；但尚不清楚这是一次工具构建验证，还是跨任务持续修改研究 Harness 的实际方法。 |
| `arxiv:2610.39884` | unknown | KARMA 对六类文本模块提供原子编辑，包含 role、output protocol 与 action descriptions，理论上可改执行指令/输出协议。但已展示的 Figure 5 修改集中于经验规则 E17–E19/E06–E07 等商业判断知识，周围执行代码与编辑算法固定。需区分真实协议/行为工件更新与领域规则手册更新。 |
| `s2:33e84e388ed32372fb1a7fbbc251f96f3375a29a` | unknown | Crossref 和出版社返回的精确题名/DOI 可确认身份，但无摘要或正文。出版社 API 的 HTTP 200 只有 coredata；ScienceDirect 摘要页为 HTTP 403。未按标题分类。 |
| `s2:49ad0fe5faace488338fac1c6abaabfadf667313` | unknown | Crossref 和出版社返回的精确题名/DOI 可确认身份，但无摘要或正文。出版社 API 的 HTTP 200 只有 coredata；ScienceDirect 摘要页为 HTTP 403。未按标题分类。 |
| `s2:773091ca2ccbd0ed969aa97a87b14b78d07ca381` | unknown | 作者仓库可核对精确论文 DOI，说明公开 Python 文件是代理产出的 ETABS 操作脚本，并非规划/检索/生成/调试代理的实现。当前证据指向固定系统生成工程任务产物，但文章正文仍不可得，不能将仓库说明扩大为完整方法的排除证明。 |
| `s2:8cc760d359b67956686aecabb7e893fffaa9b4ea` | unknown | Crossref 和出版社返回的精确题名/DOI 可确认身份，但无摘要或正文。出版社 API 的 HTTP 200 只有 coredata；ScienceDirect 摘要页为 HTTP 403。未按标题分类。 |
| `s2:a0be1e7c48baddf41925889139801ecc4ee0e217` | unknown | Crossref 和出版社返回的精确题名/DOI 可确认身份，但无摘要或正文。出版社 API 的 HTTP 200 只有 coredata；ScienceDirect 摘要页为 HTTP 403。未按标题分类。 |
| `s2:c470d4b2c990d73e0b34f5f9e384423fd7c09a14` | exclude | 已读 IEEE 官方三页编辑短文：内容讨论计算智能、搜索、效率和责任在 agentic 系统中的作用，是广义研究议程。没有提出或专项评测可持久修改 Harness 的方法，不计 Harness 专题。 |
| `s2:c9b9cd5e0b6447a180914049754459b00b3cf264` | exclude | Crossref 明确把 OSF v2 预印本关联到期刊 DOI，摘要已核。主题是自发目标生成、认知科学与人机共同目标探索，是通用 autotelic agent 视角，未描述 Harness 程序反馈修订/保留的专项方法或评测。 |
| `s2:d2a3044796ca89b338647373f7346f7094936832` | unknown | Crossref 和出版社返回的精确题名/DOI 可确认身份，但无摘要或正文。出版社 API 的 HTTP 200 只有 coredata；ScienceDirect 摘要页为 HTTP 403。未按标题分类。 |
| `s2:de09009a196ca566fe3903a6ddaffdf6c7dd7462` | unknown | Crossref 和出版社返回的精确题名/DOI 可确认身份，但无摘要或正文。出版社 API 的 HTTP 200 只有 coredata；ScienceDirect 摘要页为 HTTP 403。未按标题分类。 |
| `s2:e63c2a03c7b79972ea64fba61ee2fd4156fb2364` | unknown | Crossref 和出版社返回的精确题名/DOI 可确认身份，但无摘要或正文。出版社 API 的 HTTP 200 只有 coredata；ScienceDirect 摘要页为 HTTP 403。未按标题分类。 |

## 来源与日期问题

- 五篇 arXiv 的题名和摘要与官方页面逐字一致；VEvo-Harness、MoLRSI 官方已有 10 月 30 日 v2，canonical 仍记 10 月 29 日 v1。仅报告差异。
- 七条完全缺正文/摘要：出版社 API 虽返回 HTTP 200，实际仅 coredata；摘要页面为 HTTP 403。没有按标题分类。ETABS 论文额外取得作者仓库，仍未取得出版全文。
- Musubito 的 Crossref 刊期为 2027-02，与 canonical 2026-10-01 不同；所有 Crossref 月精度与 publisher coverDate 均不能确认实际首发日。
- IEEE 编辑短文正文注明 2026-10-08 current version，属于 November 2026 期号。Autotelic 论文相关 OSF v2 为 2026-09-24，期刊为 December 2026；不得称为本日新论文。

## 校验

覆盖 15/15 唯一稳定 ID；59 次来源请求及派生文件的现存哈希全部匹配；22 条精确引句子串通过。未改 canonical、审核单、生产代码/提示词、论文数字或公开页面，未调用付费 API，未做 Git 操作。

remaining-findings.json 为冻结结果；remaining-validation.json 为本批校验；remaining-checksums.json 为交付摘要。之后若与主审比较并改建议，应另建 sidecar，不能覆盖本件。
