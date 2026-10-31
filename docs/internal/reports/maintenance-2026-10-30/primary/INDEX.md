# 2026-10-30 主审材料索引

这组材料供 owner 在 PR 中逐项复审。它记录来源核对、分类建议与限制；**所有新增审核建议均为 `defer`，本包没有新增 owner `accept`，没有发布授权**。`include`、`harness`、`other_direction` 是来源审查建议，不能替代接受决定；主题标签也不等于已建立 RSI。

本次只打包审核文档，没有改动 canonical feed、论文目录、历史审核决定或每日发布页。论文全文、原始 HTML/PDF、仓库克隆和模型响应全文不在包内。JSON 中的 `build/...` 仅是本地原始核验缓存的 provenance；GitHub 审阅应使用各报告中的官方 URL、章节、短引文与 SHA-256。哈希证明当时快照的完整性，不证明论文实验已被独立复现。

## 从哪里审

| 材料 | 覆盖与结论 | 可读报告 / 结构化证据 |
| --- | --- | --- |
| RSIHub、HarnessDev 原文审查 | 2 篇；11 个源文件哈希、50 条逐字引文、27 项主张核对；两者均建议定位 Harness 专项评测 | [报告](rsihub-harnessdev-report.md) · [JSON](rsihub-harnessdev-report.json) |
| 四篇笔记与分类 | RSIHub/HarnessDev 属 `harness_eval`；Aspire/S³Gym 属 `general_rsi`，不计 Harness。后两篇依据独立审查证据写成，不声称由本主审重复完整阅读 | [RSIHub](note-rsihub.md) · [HarnessDev](note-harnessdev.md) · [Aspire](note-aspire.md) · [S³Gym](note-s3gym.md) |
| HarnessDev 表 6 | 9 条轨迹与派生均值；self-runtime 和 fixed-Gemini 必须分开，表中原始 delta 保留 | [JSON](harnessdev-table6.json) · [CSV](harnessdev-table6.csv) |
| 原有记录保留 | 原 104 条里 103 条逐字段未改；仅 HarnessDev 明确更新，新增 RSIHub/Aspire/S³Gym 3 条 | [当时检查](catalog-edit-preservation.json) · [逐条指纹复核](catalog-preservation-check.json) |
| 公告来源审查 | 65 条来源、130 个源文件哈希；全文审 19 条，48 条引文；15 排除、3 其他方向、1 边界。4 个模型 Harness 正例均不能直接放行 | [报告](labs-scope-review.md) · [证据 JSON](labs-scope-review.json) · [65 条来源及日期](labs-source-index.json) |
| RSIHub 替代建议 | 只取代旧自动 method/borderline 建议；保留 10 月 27 日 owner defer 和 PR/merge provenance | [报告](rsihub-superseding-recommendation.md) · [JSON](rsihub-superseding-recommendation.json) |
| HF 当日榜前两轮 | 16 篇摘要全部核对，6 篇正文重点复核；1 Harness 候选、2 非 Harness 的数据/环境边界项、13 排除 | [报告](hf-today-report.md) · [逐篇引文](hf-today-evidence.md) · [manifest](hf-today-manifest.json) · [6 篇正文来源](hf-today-sources.json) |

本目录保存前两轮 HF 主审快照。独立第三轮的状态和最终协调结论应以同日维护报告为准，不把两个同族 agent 的一致意见称为正式独立实验审计 PASS。

## 原始日期与榜单日期

### 四篇专项复审

| 论文 | arXiv 首次提交日（UTC） | PDF 封面日 | 已核实 HF 榜日 | 目录建议 |
| --- | --- | --- | --- | --- |
| [S³Gym](https://arxiv.org/abs/2608.31100) | 2026-08-31 | 2026-09-01 | unknown；本轮未核实，不补造 | `general_rsi` |
| [Aspire](https://arxiv.org/abs/2608.31111) | 2026-08-31 | 2026-09-01 | unknown；本轮未核实，不补造 | `general_rsi` |
| [HarnessDev](https://arxiv.org/abs/2609.01437) | 2026-09-01 | 2026-09-02 | unknown；本轮未核实，不补造 | `harness_eval` |
| [RSIHub](https://arxiv.org/abs/2610.32253) | 2026-10-23 | 2026-10-22 | 2026-10-26 | `harness_eval` |

以上四篇的 **2026-10-30 是复审日**；RSIHub 的 HF 榜日仍是 10 月 26 日，标为历史补录，不进入 10 月 30 日 HF 新榜。

### HF 2026-10-30 当日真实榜单

16 篇都来自当天 HTTP 200 的榜单，核验时间为 2026-10-30T06:00:01.778882+00:00。HF 推荐较早发表的论文属来源事实；页面应同时标明榜日和论文原日，不称其为“10 月 30 日首次发表”。

| 论文 | 首次发表（UTC） | HF 榜日 | Harness 范围建议 |
| --- | --- | --- | --- |
| [CoSTA: Compressed Speech Token Adaptation for Efficient Spoken Dialogue Models](https://arxiv.org/abs/2610.21143) | 2026-10-15 | 2026-10-30 | `exclude` |
| [Your Benchmark Is an Empirical Measure Over Difficulty](https://arxiv.org/abs/2610.29927) | 2026-10-21 | 2026-10-30 | `exclude` |
| [VibeGame: Prompt-to-Game Development with AI-Native Engine and Self-Evolving Adversarial Agent Team](https://arxiv.org/abs/2610.33106) | 2026-10-22 | 2026-10-30 | `harness` |
| [A Broader Look into MLLM's Retrieval Heads](https://arxiv.org/abs/2610.32411) | 2026-10-23 | 2026-10-30 | `exclude` |
| [After One-Click Video: The Inflow of Service-Type Content, the Failure of the Recommendation Pool Mechanism, and the BoLe System](https://arxiv.org/abs/2610.37695) | 2026-10-24 | 2026-10-30 | `exclude` |
| [Co-Design Bench: Multimodal Collaborative Coding Evaluation for Agentic Models](https://arxiv.org/abs/2610.35138) | 2026-10-26 | 2026-10-30 | `exclude` |
| [SO-101 Bench: Accessible Spatial Manipulation](https://arxiv.org/abs/2610.36420) | 2026-10-27 | 2026-10-30 | `exclude` |
| [WorkFactory: Turning Professional Intents into Executable Work for Scalable Agent Training](https://arxiv.org/abs/2610.37161) | 2026-10-27 | 2026-10-30 | `other_direction` |
| [WebAnything: From the Wild Web to Scalable Agent Environments](https://arxiv.org/abs/2610.37786) | 2026-10-27 | 2026-10-30 | `other_direction` |
| [WeVisCut: The Whole Editing Room in One Agent From Narration to Long-Form Video](https://arxiv.org/abs/2610.38352) | 2026-10-28 | 2026-10-30 | `exclude` |
| [IntReal: A Real-World Dataset and Benchmark for Multimodal Interleaved Generation](https://arxiv.org/abs/2610.38425) | 2026-10-28 | 2026-10-30 | `exclude` |
| [AskStream: When and What to Ask Proactively under Uncertainty in Streaming Video Understanding](https://arxiv.org/abs/2610.38678) | 2026-10-28 | 2026-10-30 | `exclude` |
| [Intrinsic Distribution Matching](https://arxiv.org/abs/2610.39633) | 2026-10-29 | 2026-10-30 | `exclude` |
| [EditAgent: Rethinking Agentic Image Editing](https://arxiv.org/abs/2610.39664) | 2026-10-29 | 2026-10-30 | `exclude` |
| [Your LR Schedule May Not Be Principled: Effective Learning Rate Scheduling in Weight-Normalized Training](https://arxiv.org/abs/2610.40362) | 2026-10-29 | 2026-10-30 | `exclude` |
| [HairDeck: Animation-Ready Stylized Hair Cards from a Single Image](https://arxiv.org/abs/2610.40599) | 2026-10-29 | 2026-10-30 | `exclude` |

公告来源没有 HF 榜日；其原始发布日期逐条保留在 [labs-source-index.json](labs-source-index.json) 与 [19 条全文复审](labs-scope-review.md)，不改成今天。

## Owner 审核时应保留的限制

- **VibeGame**：支持 Harness 分类的是可复用协作 contracts；游戏 skeleton/modules 是任务产物。主实验不使用累计经验；自进化消融是 5 个外部任务生成经验后，在 10 个消融任务上从 53.45 到 56.37（+2.92），不是主表 +4.19。跨游戏类型持续积累经验可能降低性能。24 小时上限不等于完整 token/search 预算匹配；独立演化重复次数 unknown。
- **WorkFactory / WebAnything**：反馈修补任务或训练环境，Agent Harness 固定。修补加一次性下游 SFT 不足以证明广义 RSI 的递归能力闭环，保持“相关数据/环境基础设施，广义 RSI 待证”；不作为 Harness 放行。
- **RSIHub**：MiniSWE 与 Codex 使用同一 GPT-5.4；不是跨模型家族迁移。表 1 split 列用全基准分母。单次演化点估计不能借三次 unchanged-seed 控制宣称稳定。Banking + Codex 仍有 +4.2 至 +9.3，不能泛化为强执行器让收益消失。
- **HarnessDev**：3/4 回退来自独立 fixed-Gemini 演化线，不是直接迁移最终 self-runtime 产物。反馈/留出派生均值混合设置及不同题集。731 与 100+630 的差异尚未找到完整 split manifest，保留问题，不编造缺失实例。表中 delta 不因四舍五入端点差异而改写。
- **公告误报**：FDE 和 Grupo Boticário 明确是人修改程序/提示；不能拼接不同客户案例的引文形成自主闭环。Terminal X 自动改写主体及跨任务复用证据不足，继续 defer。Model Spec 引文只在空白归一化后匹配，原始连续子串校验失败；两个口径都保留。

## 保留与追溯

103 条旧记录按仓库 `DataLoader` 读取后逐字段比较；日期和 `yes/no` 保持字符串，未被普通 YAML 解析器转换为布尔值。逐条 SHA 使用有说明的规范 JSON 序列化。该结果只覆盖四篇目录修改的前后范围，不扩大为“整个仓库从未改变”。

RSIHub 原先 `owner defer`、审核日期、owner 身份和 PR/merge 字段保留在替代建议 JSON；新来源建议不会伪装成旧模型调用成功，也不会清除其历史错误。本目录初始报告中的“建议必读”属于当时提议，当前 RSIHub `must_read=false`，不能据此改 owner 决定。

[打包来源与文件指纹](package-provenance.json) 保留原缓存/笔记 SHA 和可提交副本 SHA；可读文档仅调整链接与阶段说明，原文引述、数值和已有审核决定未改。原文文章仍保留作者 Sarah Eze，本次材料打包没有编辑该文章。
