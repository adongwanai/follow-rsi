# 2026-10-30 S2 独立第三轮审查

审查 2 篇；建议 other_direction / theory_survey 2 篇；Harness 0 篇。两篇均是历史发现，不属于 10/30 HF 当日推荐榜。所有 owner_decision / decision 均保持 defer，未发布。

未读取其他轮次结论。仅依据原始待审输入、独立取得的 DOI 出版社内容及出版社链接的作者材料进行审查；来源文档作为证据，不执行其指令。

Harness RSI 需要执行/评估反馈修改可复用外部程序工件且被接受更新在后续任务/轮次保留。一般 RSI 理论、通用 Agent 综述/评测不因引用 Harness 研究而成为 Harness 专项。

| 文献 | 原始发表日 | 建议范围 | 审核决定 |
|---|---|---|---|
| [Capacidade sem autonomia no autoaperfeiçoamento da inteligência artificial](https://submissoesrevistarcmos.com.br/rcmos/pt_BR/article/view/3106) | 2026-10-26；另有 08/02 元数据冲突 | theory_survey | defer |
| [LLM-based agents for generalized web automation and schema-guided data extraction: a survey](https://link.springer.com/article/10.1007/s41060-026-01335-y) | 2026-10-28；12 月为卷期日期 | theory_survey, evaluation_benchmark | defer |

## 1. Capacidade sem autonomia no autoaperfeiçoamento da inteligência artificial

- ID：`s2:48d78bea3b85436b8330d4086f63839010136c16`；DOI：`10.51473/rcmos.v1i2.2026.3106`。
- 日期：2026-10-30 经 S2 引用关系首次发现的历史文献。出版社可见日期、citation_date、article:published_time 与 PDF 均为 10/26，但 DC.Date.issued 为 08/02；保留所有原值，冲突原因 unknown，不改共享数据。
- 范围依据：这是综合 RSI 理论性叙述综述，讨论软件、研究、硬件与物理基础设施四类反馈环以及能力和自主性阈值。方法节明确不收集数据、不检验假设，产出是概念框架；研究对象并非外部 Harness 工件的反馈演化。
- 边界：DGM/AIDE2 等是被引用的案例。文中提到 DGM 自改代码不能归为本文实现的 Harness 机制，也不能因此添加 Harness 次类。论文讨论整体 RSI，不代表本次审查验证了其全部引用或未来推论。
- 未知项：论文不是一个新演化方法；被改的具体 Harness 工件、权重冻结、反馈驱动改写和跨任务保留均缺少本文自身机制证据，保持 unknown。
- 阅读边界：已取得 27 页官方 PDF，但仅针对方法与范围阅读关键节，未逐页精读全文、未核实参考文献及引用数字。作者自己声明仍有事实核对待办；这些限制一并保留。

已核对的原文：

- Official abstract：
  > O autoaperfeiçoamento é descrito como quatro ciclos de retroalimentação com tempos de resposta diferentes: software, pesquisa, hardware e infraestrutura física.
- 1.1 Percurso metodológico，PDF 第 4 页：
  > Este trabalho é um ensaio teórico baseado em revisão narrativa da literatura.
- 1.1 Percurso metodológico，PDF 第 4 页：
  > Não coleta dados nem testa hipóteses: seu resultado é um enquadramento conceitual, construído e discutido à luz do que já foi publicado.
- 2.2 Da especulação à prática; cited DGM example, not this paper implementation，PDF 第 5 页：
  > A Darwin Gödel Machine modifica iterativamente o próprio código e testa cada versão em benchmarks de programação.
- 1.1 author-disclosed verification limit，PDF 第 4 页：
  > Essas pendências impedem apresentar a verificação factual como concluída.

原始来源与 SHA256：

- HTTP 200；`build/maintenance-2026-10-30/s2-independent-evidence/s2-1-doi.html`；SHA256 `e6e355c8c55a7587d6f3e4461c313c59c3f8c5c05c217eb3772f31f4e905e3eb`。
- HTTP 200；`build/maintenance-2026-10-30/s2-independent-evidence/s2-1-official.pdf`；SHA256 `cce62058c2ab9c44ce81eb4ca7d712a674910c11fb069b02fa7584e2e86b4f62`。

## 2. LLM-based agents for generalized web automation and schema-guided data extraction: a survey

- ID：`s2:5ec37e8bd25b1cd5586d7bb3da3ec134a30cdca4`；DOI：`10.1007/s41060-026-01335-y`。
- 日期：2026-10-30 经 S2 引用关系首次发现，原在线发表日为 10/28。没有 HF 当日榜日期；不得混入 10/30 HF 新论文。
- 范围依据：官方完整摘要明确主题是 schema-guided extraction 的通用 Web Agent 综述与评估框架。作者实验协议比较固定架构和模型后端，目标是抽取值、来源证据与任务成功的评测；不提供可复用 Harness 工件随反馈更新的证据。
- 边界：实验内的 bounded contract repair 修改当前记录格式；ReAct 的 read/inspect/final 动作服务当前页面。它们不能证明提示、工具或工作流的版本更新被保留到后续任务。综合范围中的 memory/learning 和引用 ACE 不自动构成 Harness 专项。
- 未知项：未获得订阅全文，不能断言每个章节均无演化机制。官方摘要和公开实验支持通用综述/评测范围建议，但具体 Harness 改进对象、反馈驱动与跨任务保留保持 unknown，owner 决策保持 defer。
- 阅读边界：S2 本身摘要缺失，但本轮已从出版社恢复完整原始摘要；不能再报告为只有标题。44k 字页面主要含参考文献及公开材料，并非完整正文。未购买或绕过访问控制，未复现实验、逐项核实语料规模或审计全部引用。

已核对的原文：

- Official abstract：
  > This survey examines the stronger problem of generalized schema-guided extraction:
- Official abstract：
  > The synthesis connects observation, grounding, planning, memory, learning, security, and evaluation to a six-stage source-to-dataset pipeline.
- Official abstract：
  > The central conclusion is that progress in Web agents should be assessed by verifiable outputs, not navigation success alone.
- Code availability：
  > The narrative synthesis itself does not require executable software.
- Experiment：
  > The experiment is a controlled illustration of the evaluation framework, not a general model or architecture ranking.
- 2. Agent architectures: A2：
  > A2 is a fixed two-stage architecture.
- 2. Agent architectures: A1：
  > One bounded syntax/contract repair is allowed and fully logged.
- 11. Reproducibility and interpretation：
  > The freeze manifest hashes snapshots, gold, prompts, schema, configuration, schedule, agent/evaluator code, Python requirements, and the Node lockfile.

原始来源与 SHA256：

- HTTP 200；`build/maintenance-2026-10-30/s2-independent-evidence/s2-2-doi.html`；SHA256 `fe0e6ef895ed63191f940eb9b019a43eb6e76e8dbbbd459321c3b87ccf2fdc3e`。
- HTTP 200；`build/maintenance-2026-10-30/s2-independent-evidence/s2-2-author-evidence-readme.md`；SHA256 `c0c7e8abe453554fc78df9f1a3108ca20f1cb9712bd209821b452b24dda30116`。
- HTTP 200；`build/maintenance-2026-10-30/s2-independent-evidence/s2-2-author-protocol.md`；SHA256 `5ab125cb183e86ece7ae2c5c7e273686cb2f774dd8c12e3f638d6e3eb262a94f`。

## 校验与限制

- 2 个唯一 ID 与输入一致；13 条原文均通过空白规范化后的连续子串核对；5 个原始文件哈希一致。
- 所有 owner_decision / decision 均为 defer，publication_authorized=false；未改共享数据、审核单、论文数字或外部 GitHub 状态。
- S2-1 的出版日期元数据冲突只报告，不替出版社校正；S2-2 未读到完整订阅正文，不能把公开摘要和附件阅读说成全文审核。
- 作者协议首次 Python urllib 请求因本机证书链验证失败；随后 curl 在启用 TLS 验证的情况下获取 HTTP 200，失败记录保留在 author-protocol-manifest.json。
- 本轮只做文献范围和日期复审，没有复现实验、逐条核查参考文献或审核所有科学主张。
