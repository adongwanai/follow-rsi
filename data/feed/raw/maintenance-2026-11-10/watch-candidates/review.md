# Watch-only 候选来源与范围初审（2026-11-10）

本包是来源核验与范围建议，不是批准。四篇均已获得 official arXiv abs 与 versioned HTML；8 次免费来源请求全部 200，没有调用付费模型。原文哈希、逐字引文与定位见 primary-reviews.json。

| 条目 | 来源日期 / 版本 | 仓库最早有证据观察 | 范围建议 |
|---|---|---|---|
| CompressionBench: How can your coding agents compress LLMs? | 2026-11-04T18:14:50Z / v1 | 2026-11-09T08:03:49Z | exclude / evaluation_benchmark |
| Adapting the Process of Adaptation: Darwinian, Lamarckian, and Agent-Directed Evolution in AI | 2026-11-04T19:08:46Z / v1 | 2026-11-09T08:03:48Z | exclude / theory_survey |
| Flex-RSI: Benchmarking Recursive Self-Improvement of Frontier Agents | 2026-11-06T03:51:20Z / v1 | 2026-11-09T08:03:45Z | include / evaluation_benchmark |
| BOXBOX: Recursive Harness Self-Improvement for Long-Running Performance Optimization | 2026-11-06T09:36:00Z / v1 | 2026-11-09T08:03:44Z | include / harness |

## 关键边界

- Flex-RSI：Harness 专项评测，executor / improver 的工件修改与任务产物修改分开；留出测试、冻结 Harness 对照。不要称为所有模型全覆盖或跨任务迁移已证实。
- BOXBOX：程序工件按轨迹修改并进入后续执行/复审，满足当前“后续改进轮次”保留口径；独立跨任务迁移 unknown。摘要单独对未来复审继承写得不够具体，纳入建议来自正文，不伪造摘要闸门成功。
- CompressionBench：压缩权重和推理实现属于外部模型研发产物，不是编码 Agent 的 Harness。
- Adapting the Process：一般演化理论；DGM/AIDE² 引用只是动机，不等于 Harness 专项理论。

日期以 GitHub issue created_at 为最早有证据的仓库观察；不得把论文发表日或今日抓取日冒充 first_seen。此包没有声称 HF 推荐日。独立三轮复审由 root 完成，之后才可进入真实日期审核 PR。

## 可恢复文件

- records.json：官方元数据与原始 HTTP 收据
- normalized-records.json：候选规范记录草案，没有批准字段
- primary-reviews.json：逐项范围、引文、限制和双语摘要建议
- 各 ID/fulltext.html、abs.html：原始字节；.receipt.json 记录请求时间和 SHA-256

本次未重跑论文实验，也未对所有表格数字逐一复算。摘要建议避免无必要数值主张。
