# 发布前核验记录

原稿：`为什么 AI 还不会自我进化.md`，2026-10-29，署名 Sarah Eze。
原稿 SHA-256：`28a9b76793a45cd2c72a947de981332449240dacd9752a86359f3ba82dbc07e8`。

2026-10-30 对公开正文与表格进行核验和独立代理复审，随后检查图表、算术、链接与排版。保留署名，原始本地文件未修改。本页是公开资料核对，不是原始运行日志审计或独立实验复现。

## 发布稿的主要修订

| 位置 | 修订与依据 |
| --- | --- |
| 总论 | 保留“稳定、可迁移的改进尚未得到保证”；同时呈现正收益，不把四篇主文与五篇旁证都归成同一个失败结论。 |
| 三步图 | 三步是本文阅读顺序，不代表三个基准构成同一个实验流水线；删除“第三步证据最多”的无依据比较。 |
| 分类 | RSIHub、HarnessDev 为 Harness 专项评测；Aspire、S³Gym 为通用 RSI 评测，不计入 Harness 专题。 |
| Aspire | 终局设置每模型×目标两次独立运行；允许中途看总分的 30 格每格一次。没有中间独立评测的长谱系不能断言逐步变差。 |
| S³Gym 相关性 | −0.010 限于分块事件正反馈一致率 A 与下一 strict 检查点归一化增益 g，不推广到所有自评指标。 |
| S³Gym 记忆 | 0.474 / 16.840 和 548.499 / 33.219 是 History ICL 与 Summary Memory 的 AUC+，不是训练前后得分。 |
| HarnessDev 均值 | +7.2 / +0.5 是表 6 九条轨迹报告增量的无权平均；混合五条 self-runtime 与四条 fixed-Gemini，且两列题集不同。五条 self-runtime 留出增益全部正，均值 +3.11。 |
| HarnessDev 图表 | 保留论文报告 Δ，不用四舍五入后的 H₀ / 末版相减替换。SVG 同目录提供 CSV 和 JSON 抄录。 |
| HarnessDev 噪声与迁移 | ±4.75 是 feedback pair-score 的波动；噪声内不等于真实效应为零。3/4 退步是从头固定 Gemini 的四条演化线，不是优化完成后的直接迁移。53.1% 同向率没有建立与随机无异的检验。 |
| HarnessDev 创建 | 67.8 / 86.2 为不含 MLE-bench 的四基准均值；人工工程参考系统没有统一执行模型，不能把差值全归因于 Harness。专用轨迹接口两次不代表没有其他诊断。 |
| RSIHub 排名与收益 | TB2 + MiniSWE 中 Hyperagents / A-Evolve 并列最高。Codex 在 TB2 仅 +0 到 +2.2，但 Banking 仍为 +4.2 到 +9.3；不推出“强 Agent 收益消失”。 |
| RSIHub 留出分母 | Banking 的 sealed 列以全部 97 题为分母，报告留出题对全基准分数的贡献，不是 27 道留出题内部成功率。 |
| RSIHub 预算与分区 | 未报告完整匹配总 token 预算对照和完整 LLM 成本；不能据此断言实际花费一定不同。三次执行一致性重复不同于完整演化重复。实验分三区，框架允许 gate/train 重合。 |
| HDA | 54% / 14% 限于 21 个搜索集收益显著的设置，不能推广成整个领域的比例。 |
| Rethinking v4 | 区分纯 Harness Evolution 与 Harness Scaling；同时保留长时交互游戏的正面结果。 |
| Auditing | 4/26 是审计样本内“更好的改进器”主张的实验设计计数，不是成功率，也不证明缺少该对照的方法都失败。 |
| ECG-RSI | S7 30.15→46.61，三轮增量 +13.07/+3.01/+0.38，累计数值增益 +16.46。3,000 题的类别/难度表错误数无法对账，只报告差异，不修补原文。 |
| Terminal-RSI v2 | 已确认 SWR100 与训练任务不重叠；更广重叠审计不充分。未验证预先定义的选版规则，不把条件式警告写成确定使用最终测试选版。Mean@3 是推理重复。 |
| 九篇未重读工作 | “还缺什么”中的 StarHarness、RRSI、Bad Genius、MaD-RSI、ECDYSIS、REUSE、Harness²、TTHE、HarnessPro 仍只引库内摘要，不宣称已逐篇复核其失效分析。 |

## 原始资料

- [Aspire 正文](https://arxiv.org/html/2608.31111) · [S³Gym 正文](https://arxiv.org/html/2608.31100)
- [HarnessDev 表 6](https://arxiv.org/html/2609.01437#S4.T6.2) · [统计与局限](https://arxiv.org/html/2609.01437#S6.SS1)
- [RSIHub 实验设置与分母](https://arxiv.org/html/2610.32253#S4.SS2) · [结果](https://arxiv.org/html/2610.32253#S4.SS3)
- [HDA 归因](https://arxiv.org/html/2610.22466#S5) · [Rethinking v4](https://arxiv.org/html/2607.12227v4)
- [Auditing 样本与结论](https://arxiv.org/html/2610.27610#S6.SS2)
- [ECG-RSI v2](https://arxiv.org/html/2610.17718v2) · [Terminal-RSI v2](https://arxiv.org/html/2610.22192v2)

图表生成：`scripts/render_article_figures.py`（需要 matplotlib 与 CJK 字体）；网站构建使用提交的 SVG，不在 CI 中重绘。
