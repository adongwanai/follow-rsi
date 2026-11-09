# 2026-11-09 五篇版本提醒复核

只读审计已完成：四张现有卡片可保持，一张 Hyperagents 卡片需要纠正既有过强概括。没有修改生产、论文原始数据、Git 或远端 issue；没有付费模型调用。

| Issue | 官方版本日（UTC） | 结论 |
| --- | --- | --- |
| [#62 RSIFlow](https://github.com/adongwanai/follow-rsi/issues/62) | v2，2026-11-02 09:12:51 | 新版确实改了多个成绩与 BFCL 计分说明；卡片只写六基准、两模型且标待细读，未引这些数字，可保持。 |
| [#63 The Trinity](https://github.com/adongwanai/follow-rsi/issues/63) | v2，2026-10-30 04:15:41 | 方法正文和表格比对无差异，v2 PDF也核实当前冻结模型外协议模块/跨任务继承/评测技能另行准备的概括。保持候选及 unknown。 |
| [#64 TTHE](https://github.com/adongwanai/follow-rsi/issues/64) | v3，2026-11-04 09:02:27 | v2/v3 仅对应作者标记变化。12.7%→48.7% 为三次运行均值，16.0% 为另一次十次投票控制；数值与跨模型迁移结论仍受正文支持。 |
| [#65 Hyperagents](https://github.com/adongwanai/follow-rsi/issues/65) | v2，2026-11-01 21:28:39 | 当前“编码等四个方向都超过DGM”过强；正文 coding 是 comparable。应修订当前概括后关闭。 |
| [#66 Harness Updating](https://github.com/adongwanai/follow-rsi/issues/66) | v2，2026-11-04 20:26:58 | 77 个 ltx_tr 行完全相同；现有能力拆分结论保留。主要为版式、图表/附录/引用编号变化。 |

建议 Hyperagents 的 `result_zh` 改为：

> 编码任务上的改进与 DGM 相近；在论文评审和机器人奖励设计上优于原始 DGM，元层改进可迁移至奥赛数学批改并跨运行积累。

对应 `result_en`：

> Coding improvements are comparable to DGM; DGM-H outperforms the original DGM in paper review and robotics reward design, while meta-level improvements transfer to Olympiad mathematics grading and accumulate across runs.

这同时删除无可核验引用排名支撑的“最常引的元改进基线”。保留 must_read 和 improver 分类。v2 PDF 第 8 页编码 comparable，第 9 页表明只对原始 DGM 在论文评审和机器人奖励设计上显著胜出；相对手工适配 DGM-custom 的差异不显著。第 11 页新增元 Agent 单独迁移消融支持元改进可迁移。第 2 页新增明确限制：结果不证明无界或自加速改进。

RSIFlow v2 的例示变化只记录在审计中，不能把旧数字用于后续解读：Qwen3-8B Overall 59.86→59.95，平均超过 strongest per-metric baselines 的 +3.11%→+3.42%；BFCL 从按任务数加权的文字说明改为 17 类无权宏平均。当前卡片没有这些结果，保留待细读不自动补入。其模型训练与 Harness/meta-Harness 都有独立更新路径，可保留 Harness 共演化范围，不能因为含 SFT 排除。

TTHE 的数据无需改；如果同步精炼文字，可明确“三次运行均值”与“另一次十次投票控制”，不声称这是严格同预算比较。此建议是补充语境，不是数字纠错。

`version-review.json` 含每项原卡、身份日期、引句定位、原文 SHA、建议和范围边界；`claim-source-paragraphs.json`、`hyperagents-selected-pages.json` 和 `trinity-selected-pages.json` 可作后续独立复核输入。原始HTML/PDF只存本地 build；若需要持久回执，建议提交结构化摘要、引句与 SHA，不必提交所有大 PDF。`manifest.json` 列出文件哈希。

来源边界：Hyperagents v2 HTML 返回404，官方PDF成功；其余官方HTML及 abs 成功。中途曾把 Trinity 相同文件长度/正文diff误说成原始字节相同，并错误查看v1文件标记；最终核查两份HTML SHA不同、版本标记分别正确，v2 PDF也确认。这属于审查者中途误判，不能列成来源故障。所有结论以最终 JSON 为准。

本工作核查的是版本、当前卡片概括与引文，不是全部实验复现、统计重算、所有证据字段完整审核，也不代表已关闭 issue 或完成公开部署。
