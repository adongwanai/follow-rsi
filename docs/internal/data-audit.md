# 原始数据保真核查

核查日期：2026-10-27。对 owner 提供的 papers.yaml 与当前 data/papers.yaml 做了逐字段比较。去除新增的 `summary_en`、`result_en`、`en_machine_translated` 后，两者完全相同。

- 收录 98 篇、候选 6 篇、必读 20 篇。
- 原始中文摘要、结果、日期、机构、数字和证据取值均保留。
- 8 项证据检查记录了 43 / 784 项，即 5.5%；这表示有记录，不表示通过审核。
- 收录论文中 13 篇带 needs_reading。站点、README、证据页和分享卡都保留标记。
- 本次新增的英文文本标为机器翻译；自动检查数字多重集合，语义仍可由贡献者校订。

原始文件 SHA-256：`4cafdca0a0fb686e97b40338c379a870bca6a68c1ed94bb30fdf129555cd0b3d`。这是一份本次迁移的核查记录，不作为阻止将来合法贡献的固定测试。

## 需要 owner 判断的数据问题

真实 arXiv 元数据校验发现以下标题与提供的标签不一致，未擅自改动原数据或评测标签：

1. `2609.08175`：原题为 “Safe Harness Self-Evolution: A Theoretical Analysis of Feasibility and Limits”，接口返回 “A Theory of Reliable Self-Evolution for Agent Harnesses”。可能是改题，需核对。
2. `2607.07007`：curator seed 写 “State-machine fuzz harness generation”，接口返回 “Thinking More, Harnessing Better: State Machine Guided Harness Automatic Generation with Project Digestion and Workflow Decomposition”。seed 使用描述性名称，需确认身份。

评测另有一个 schema 失败样例：Recuris `2608.24876` 的模型理由在一次重试后仍超出 40 字限制。完整日志见 [评测报告](../../feed/eval/report.md)。27 个 curator seeds 仍待 owner 核对。

没有把 HF 摘要自动判断写入原论文证据字段；没有把 unknown 改成 yes/no；没有声称已审完 20 篇必读正文。
