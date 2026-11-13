# 2026-11-13 正式应用与出版前回执

本文件随出版物 PR 提交，记录真实已合并的前置审核与本地验证。出版 PR、Pages 和公共 HTTP 验收尚需在提交后完成，不能用本地 `published=true` 代替上线证明。最终部署回执在 [issue #60](https://github.com/adongwanai/follow-rsi/issues/60) 的 11/13 维护留言中记录。

## 实际合并与应用范围

| PR | 内容 | 审核 head | 真实 merge commit |
| --- | --- | --- | --- |
| [#100](https://github.com/adongwanai/follow-rsi/pull/100) | 来源、元数据和三轮证据 | `9e2cc5e768ade08b564d9827853a361783a22244` | `148cdc77e3e862581cc7a830004f95c74be1f148` |
| [#101](https://github.com/adongwanai/follow-rsi/pull/101) | 11/06 的 6 条变更 | `a1c41265199736850da964192d9d2ac324a419df` | `9e6acb6c6732c2396d890a9958edf7d2f461d307` |
| [#102](https://github.com/adongwanai/follow-rsi/pull/102) | 11/12 晚到 14 项 | `c889a37da38015c3fcb441416c4740588c5d50c8` | `c0a429e7d1b8bc257a7bbe991cf6fc92245b959f` |
| [#103](https://github.com/adongwanai/follow-rsi/pull/103) | 11/13 简报、重绑与勘误 | `a488425fefc10ddd5a19caa563a9791d9c5c0c03` | `c5e682f3d04fafb8275b20b3a1a86529c8ae047a` |

四个 PR 已核实实际合并、准确 head 的 build/validate；三个日期审核同时有真实 owner status。持续授权下使用 owner 账户的合并凭据，不代表 owner 本人逐篇阅读。详见 [远端前置凭据](publication-prerequisites.json) 和 [正式应用记录](publication-generation.json)。

只应用 6 + 14 + 33 = **53 个唯一变更**：24 个新来源项、27 条原正式意见的元数据哈希重绑、2 项摘要纠正。决定为 41 reject、7 backlog、3 defer、1 既有 accept、1 move；不是 53 篇新论文。与冻结的 post-intake 相比，其余 **1980 条记录的 JSONL 行字节完全不变**。原 review_history、first_seen 及日期审核文件完整保留。

11/06 的审核文件有 297 行，只应用获准变化的 6 行，不重放旧决定覆盖后续纠正。GitHub 保留创建时 base，#101 的合并 PR 文件接口实际有 593 个文件、6 页；已读取全部分页并确认唯一正式审核路径，未依赖截断的首屏。初次 owner 检查使用早于 #100 的 main，因来源哈希尚未同步失败；来源合并后重新检查，并重跑原失败运行，`43340184707` attempt 2 已成功。未降低阈值或伪造状态。

## 当期与旧刊保护

11/13 为采集与审核简报，**当日新增论文 0**。08:04–08:10 实际尝试 12 路来源，24 个新稳定 ID 得到 1 项限定纳入、23 项排除；DeCAF 按 11/05 原发表日列入历史 backlog，不冒充今天新论文。今日 HF 未就绪；11/12 的完整 20 篇和 11/11 的 39 篇已全部对账，14 个晚到成员保留 11/12 推荐日及实际 11/13 发现、审核日。S2 限流及超时的覆盖不足仍明确展示。

11/06 仍只有 Harness-S：补充代码链接、同步官方 v1 已核实的作者元数据（包括 Rongying Shan → Rong Shan），实际复核日为 11/13，保留首刊时间、来源快照、摘要、版本、发表与更新日期。11/12 manifest 原样保留，代表昨日采集时点；晚到变化在今日说明。

W45 仅修改 PLVR v1 的双语摘要、双语公开勘误说明及 updated_at，旧刊原样归档；其他条目、选择、计数、metrics、趋势图和卡片保持。PLVR 的原语库准确表述为人工种子与前沿模型从教师轨迹生成。[窄勘误回执](plvr-weekly-erratum.json) 保存前后 SHA 和摘要。DiscoveryRSI 仅纠正 GPT 比较组与语义判分器混淆，6.3/2.5/2.3 保持，仍归 AI4AI/权重。HexaShell 当前 v2 未被 v3 建议替换；RSIHub、HarnessDev、Aspire、S³Gym 的定位和阅读路线不变。

## 最终对账与待办

稳定 ID 并集 **8856**。规范库 **2033 = 943 正式/目录 + 1026 可复用范围意见 + 55 待补证 + 9 外部来源阻塞**；来源漏入、HF 漏推荐日和无状态记录均为 0。27 条元数据正式意见重绑完成，33 条仅建议维持无正式 review，4 项无变化结案。独立 [post-review 台账](backlog-audit/post-review/README.md) 与原始冻结清单保留。

18 项版本/文本任务完成；周扫剩余 374 项，另 2 项只在 daily 表，跨表去重后仍有 **376 项正文比较待办**。该维度与 55 待补证、9 外阻不能相加。9 个正文外阻经过 18 次实际重试仍未恢复；#19、#20、#23、#30 的具体工件缺口继续保留，未用统一 defer 隐藏未处理记录，也不把全文已有的 HexaShell v3 称为来源阻塞。

## 实际验证与费用

三份日期审核 post-apply 校验通过；`scripts/validate.py` 核对 114 篇与 9 条路线。完整 pytest 为 **430 passed in 72.04s**，见 [测试回执](validation-post-review.json) 与日志。来源整合阶段也完整通过 430 项；最早一次 429 过、1 失败来自临时 inventory 含本地目录名，已只移除不应公开的工作 inventory，原始来源字节不清洗，随后完整重跑通过。

构建幂等、README 手写区保全、旧 manifest 边界、509 份原始归档 SHA（189974295 字节）与私密值扫描通过，见 [保护校验](preservation-post-review.json)。[独立终审](independent/rendered-publication-review.json) 记录 32 份本地产物 SHA，结论 `pass_local_render_only`，0 阻断；不是线上验收或实验复现。134 条来源、范围及摘要/版本原文引句已核对，全局模型旧分数与告警仍保留。

DeepSeek 生成请求 **0**、生成 token **0**；00:03:32 至 00:56:45 UTC 的余额观察下降 **0.00 元**，其后没有生成调用。usage 日志 0 行。余额差不是本任务发票，Codex 用量不在此 API 日志内；原余额与密钥仅留本地。详见 [结束费用回执](usage-boundary-end.json)。三个 feed 工作流保持 `disabled_manually`，没有重新启用。
