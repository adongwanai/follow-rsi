<!-- follow-rsi-maintenance-2026-11-23-final -->
11/23 维护已完成本轮采集、三轮范围审核及线上出版。全部 12 路已启用来源均有真实请求；HF 全榜为 11/18–23 的 39/50/50/0/0/13 篇。S2 citations 47 次请求含 19 次 429，authors 8 次请求含 6 次 429，论文遍历未完成，未访问覆盖仍为 unknown。

公开结果：[https://adongwanai.github.io/follow-rsi/daily/2026-11-23.html](https://adongwanai.github.io/follow-rsi/daily/2026-11-23.html)。新增 234 条规范记录：25 篇按 11/18–20 原窗口补刊、4 篇历史补录、202 条排除、3 条待补。

本次三条待补（均有正式日期审核，不是批量 defer）：

- `arxiv:2611.23890`：EVA-RSI 明确迭代训练/合并评估器权重并可调推理设置；现有 champion 表显示帧数和分辨率变化，但尚不足以确认实际反馈保留了可复用 Agent Harness 提示或代码机制。  待补：["已采纳版本中独立于模型权重的 Harness 工件 diff", "该工件在后续任务或改进轮次真实加载和保留的记录"] 补查 champion 推理适配代码/提示及版本轨迹；若确有外部工件反馈迭代则改判 coevolution，不因权重训练而排除。 来源哈希 `156476b634752453b710295c486b3a2b64e4165a79fcf456500fcbbfc42ebb0f`。

- `arxiv:2611.22132`：DailyBrick 单次执行固定 Γ 并修订当前组装产物；跨 run 的提示/技能/SDK 更新写为候选和 later configuration 流程，已呈现实验未给实际激活的跨任务版本。  待补：["跨 run 接受并激活的配置版本、提示/技能/SDK diff", "后续不同请求使用该更新的执行与回归结果"] 获取跨配置更新记录后逐项复审；保留任务产物修复和真正 Harness 更新的区别。 来源哈希 `9241abcb2a974848a004e3fbdb36279934b082c7bff6329fd2d9dd1ec28c8460`。

- `s2:e7937455bba30333bb9fe486e6fda9f2bc171c70`：仅有 Semantic Scholar 的截断摘要和通用具身智能综述标题，未取得足以确认 Harness 演化专项章节的原文。  待补：["完整原始来源与可核验正文", "Harness 演化专项主题而非一般具身智能综述的证据"] 先解析出版者原文/DOI并补全文，再决定范围；现有片段不足以纳入。 来源哈希 `3a1b875c7206323e91c909f4bec54e4f271c9a875bcab647dba5385d2f02925e`。

旧外部阻塞继续在 #19、#20、#23、#30、#119、#128 保留具体工件与调用链缺口；8 篇旧正文均 HTTP 200 且与 11/18 哈希相同。本轮不把内容未变重复计算成新发现。#115/#116 的现行卡片文字/数字复核已完成，完整版本任务与实验复现边界继续保留。

全历史覆盖 9,292 个稳定 ID、2,456 条规范记录；[逐条正式审核后的账本](https://github.com/adongwanai/follow-rsi/blob/main/docs/internal/reports/maintenance-2026-11-23/backlog-audit/post-application/summary.json)给出原因和下一步，保留 2,096 个版本任务及 41 条旧模型错误。56 条内部编辑工作不冒充外部阻塞；旧范围意见仅在来源哈希未变时复用。后续线上回执将单独追加，不改写原来 online_verified=false 的本地生成快照。

历史全局评测保持 recall 0.892857 / threshold 0.90，且未完整结束，不宣称通过。付费模型请求 0、生成 token 0；范围审核不是实验复现。
