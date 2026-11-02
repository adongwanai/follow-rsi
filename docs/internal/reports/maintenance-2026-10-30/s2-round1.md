# S2 新发现条目：独立第一轮核验（2026-10-30）

结果：Harness 0、其他方向 1、排除 1。两篇出版社身份与原始发表日期均核对一致；只读完整公开摘要，未声称全文审查。全部保持 defer，未修改共享数据或发布状态。

这批是历史发现：原日期分别为 2026-10-26 与 2026-10-28；2026-10-30 是发现日，两篇均没有 HF 推荐榜日期。

## 逐篇结论

### Capacidade sem autonomia no autoaperfeiçoamento da inteligência artificial

DOI：10.51473/rcmos.v1i2.2026.3106；出版社：https://submissoesrevistarcmos.com.br/rcmos/pt_BR/article/view/3106

原发表日期：2026-10-26；建议：other_direction / theory_survey；harness_specific=no。

宏观 RSI 理论，讨论能力、自主性与物理基础设施闭环；保留一般 RSI 方向，不纳入 Harness 专题。

**实际研究对象**：AI 整体演化中的软件、研究、硬件、物理基础设施四类反馈循环，以及能力与自主性两个门槛。

**三条件**：

- `reusable_harness_program` = `unclear`：理论讨论整体 AI 系统，并未以外部提示、技能、工具或控制程序为明确被演化对象。
- `feedback_driven_program_revision` = `unclear`：宏观四类反馈循环不能替代系统执行反馈修改某个 Harness 程序的证据。
- `persisted_program_revision` = `unclear`：摘要没有描述外部程序版本的接受与跨任务复用；作为宏观理论不能据此补全机制。

**专项评测/理论**：属于整体 RSI/自主性与物理基础设施的理论讨论。研究对象不是外部 Harness 工件的反馈演化，因此不能计入 Harness 专项评测与理论。

**原文引句**：

> O autoaperfeiçoamento é descrito como quatro ciclos de retroalimentação com tempos de resposta diferentes: software, pesquisa, hardware e infraestrutura física.

明确研究的反馈环包括软件、研究、硬件与物理基础设施，范围是整体 AI 演化。

> Argumenta-se que apenas a segunda marcaria o ponto em que a humanidade perderia o controle sobre a evolução da IA; antes dela, há capacidade sem autonomia.

中心论点是能力与自主性门槛，而非某种 Harness 工件优化。

> O laço pode fechar-se por dois caminhos: robôs executam enquanto pessoas ainda decidem, ou a IA decide enquanto pessoas ainda executam.

讨论人类与 AI 在决策和执行中的关系，不能等同 Agent 自修改外围程序。

**来源限制**：首轮阅读的是出版社完整摘要，未阅读 PDF 全文；S2 摘要、出版社摘要与 Crossref 摘要一致。

**日期/元数据备注**：

- 可见 Publicado 26.10.2026、citation_date 与 Crossref published-online/issued 均为 2026-10-26。
- 同一网页另有 DC.Date.issued=2026-08-02，其语义未确认；原字段保留，不用它覆盖文章公开发表日期。

证据提取：`build/maintenance-2026-10-30/s2-source-evidence/rcmos-publisher-extract.json`

### LLM-based agents for generalized web automation and schema-guided data extraction: a survey

DOI：10.1007/s41060-026-01335-y；出版社：https://link.springer.com/article/10.1007/s41060-026-01335-y

原发表日期：2026-10-28；建议：exclude / theory_survey；harness_specific=no。

出版社摘要明确聚焦网页自动化与可验证抽取输出，非 Harness 自进化方法或专项综述。

**实际研究对象**：网页 Agent 的通用自动化和受 schema 约束的数据抽取，重点是字段溯源、结构化结果质量与任务完成率。

**三条件**：

- `reusable_harness_program` = `unclear`：摘要综合规划、记忆、学习等组件用于网页数据流程，没有把可复用 Harness 程序定义为被反馈改写的对象。
- `feedback_driven_program_revision` = `unclear`：所述实验比较三种 Agent 架构与模型后端的抽取表现，未说明执行反馈改写外围程序。
- `persisted_program_revision` = `unclear`：摘要没有说明 Agent 生成并接受的 Harness 新版本供后续任务复用。

**专项评测/理论**：评测关心网页导航/任务完成和字段级数据质量的关系，是一般 Web Agent 综述及任务评估；即使文献涉及 memory、learning 或引用 ACE，也不能证明是 Harness 演化专项。

**原文引句**：

> Large language model (LLM) agents can navigate websites, operate graphical interfaces, and use software tools, but task completion does not guarantee reliable structured data.

研究问题是完成网页任务不等于可靠结构化数据。

> The synthesis connects observation, grounding, planning, memory, learning, security, and evaluation to a six-stage source-to-dataset pipeline.

组件服务于从来源到数据集的流程；列出记忆和学习不是 Harness 演化证据。

> The central conclusion is that progress in Web agents should be assessed by verifiable outputs, not navigation success alone.

核心结论直接说明其评估对象是网页任务输出质量。

**来源限制**：原始 S2 条目未提供摘要；普通 DOI HTTP 200 实际返回 Client Challenge，Crossref API HTTP 429。正常浏览器打开出版社公开页后获得摘要、作者、DOI 和 Published/Version of record 日期；正文为订阅预览，未获取全文。浏览器工具未提供 HTTP 状态，因此不声称浏览器响应为 200。

**日期/元数据备注**：

- 公开页面 Published 和 Version of record 均为 28 October 2026，沿用 2026-10-28 作为原发表日期，不把发现日或卷期日期当成新发表日期。
- S2 中的作者缩写 M. Chadi 与 H. Mousannif 在出版社页面展开为 Mohamed-Amine Chadi 与 Hajar Mousannif；本轮不修改正式作者数据。

证据提取：`build/maintenance-2026-10-30/s2-source-evidence/springer-browser-extract.json`

## 实际访问记录

| 来源 | HTTP | 结果 |
| --- | --- | --- |
| RCMOS DOI → 出版社 | 200 | 可见摘要、作者、DOI、公开发表日期 |
| RCMOS Crossref | 200 | 标题/DOI/摘要/online 日期与出版社一致 |
| Springer DOI → 出版社（普通请求） | 200 | Client Challenge，不能作为文章内容成功 |
| Springer Crossref | 429 | 空响应，原响应及 hash 已保存 |
| Springer 正常浏览器 | 工具未提供 | 公开摘要、作者和发表日期可读；全文需订阅 |

已校验 4 份 HTTP 原响应 SHA256、2 份出版社提取文件 SHA256、6 段连续原文及 200 字符上限。

无分类判断的二轮输入：`build/maintenance-2026-10-30/s2-grounded-input.json`。
