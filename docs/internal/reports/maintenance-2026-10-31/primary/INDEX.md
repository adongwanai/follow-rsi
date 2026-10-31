> 复核更新：第 3 轮已完成。KARMA 的直接纳入建议已收回；最终为 5 篇 Harness、2 篇边界、30 篇本轮不纳入，全部 defer。请先看 [更正说明](round-3-reconciliation.md) 与 [合并建议](review-reconciled.json)。下文及 review-results.json 保留原初审，便于追溯。

# 2026-10-31 来源核验与 Harness 范围初审

这是第 1、2 轮的来源核验与分类建议；独立第 3 轮和 owner 决定另行记录。全部条目保持 `defer`，没有发布授权。

- HF 10 月 31 日请求成功（HTTP 200），快照内为 0 篇；不能写成“今天没有符合条件的论文”。
- HF 10 月 30 日当前为 39 篇；相对昨日冻结的 16 篇，补入 23 篇。它们仍属于 10 月 30 日推荐榜。
- 远端新增 20 个稳定 ID，与补入 23 篇重叠 6 个；本轮去重审查 37 篇。
- 37 篇均核对官方标题、版本历史及摘要；18 篇另读方法/评估边界章节。未声称整篇通读或复现实验。
- 远端 append-only 行差异按历史版本处理，保留原始快照；本审查没有合并或覆盖主数据。

建议分布：{'exclude': 23, 'harness': 6, 'other_direction': 7, 'borderline': 1}。其中 Harness 为 4 篇方法、2 篇专项安全评测；不混为同一种篇数。

## 核验入口

- [逐篇建议与证据短引文](review-results.json)
- [37 篇简表](review-matrix.md)
- [18 篇边界判读](boundary-notes.md)
- [官方来源、抓取时间与响应哈希](sources.json)
- [日期核对](date-audit.json)

原文缓存在本地 `build/maintenance-2026-10-31/primary/sources/`；此目录只提交短引文和官方链接。
本轮校验 55 个响应哈希、86 处引文；原有论文数字、证据字段与 owner 决定未修改。
未专门逐项审定的 held-out、same-budget、cross-task、open-source 字段保持 unknown；文本边界判断不替代证据评级。

## 需要独立复核的边界

- MoLRSI：正文有资源技能修复的正证据，但主实验对照隔离的是历史经验。是否把辅助技能机制纳入 Harness，保留 borderline。
- A-RSI：明确不属于 Harness；静态模板和控制器下的多窗口 Solver 训练是否达到广义 RSI 门槛，保留 borderline。
- KARMA：修改角色、输出协议、动作定义和提示规则，并非只有被动记忆；可执行代码仍固定。
- Before the Next Rollout：policy 与技能库分别迭代，适用权重/Harness 协同例外。
- ExLabel、Routed CL：固定机制上的经验条目和状态变化，不能因 self-evolving 名称直接判为 Harness。
