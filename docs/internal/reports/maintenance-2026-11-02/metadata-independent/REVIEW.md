# 2026-11-02 十篇边界项独立复审

冻结时间：2026-11-02T06:45:49.987029+00:00。范围：10 篇；纳入建议 7，不作为 Harness 主收录建议 2，边界未知 1。全部 decision=defer，未授权发布。

仅依据中立元数据和官方正文独立阅读；冻结前未看 primary-a 的本轮结论。本文所称“纳入/排除”均是范围建议，非人工批准。正文为定向阅读，未复现实验、未认证全部数字或理论证明。

| 论文 | 建议 | 范围与边界 |
| --- | --- | --- |
| Agentic Self-Awareness | include | HarnessX 对提示、处理器、控制流的搜索与留出集评测分支。 |
| Mining the Design Space | include | 对经过反馈搜索演化的 graph.py/prompt.py 工作流进行专项经验研究。 |
| EngramBench | include | 程序性技能抽象与跨项目迁移的 Harness 专项基准。 |
| Learner2Skill | include | 仅 Section 3.2 Executor Calibration 的共享执行协议修改。 |
| EvoSteer | include | 权重与外部程序性技能协同更新；限定到核心方法 Validated Skill Admission。 |
| OptiCom | include | Strategy Adapter 对改进器自己的选择偏好与指令模板做版本化更新。 |
| CUAWright | unknown | 存在任务内工具生成、执行、修订；长期保留条件待补证。 |
| Verification and Self-Improvement | include | 版本化验证接口、改进器继承及后继选择的理论审计合同；尤其 Appendix E/P。 |
| ECG-RSI | exclude | 存在辅助的 generator/operator/skill 版本化修复；主记录仍是 ECG 数据与模型更新。 |
| OmniBrain-0 | exclude | Section 5.1 reminder-policy 是真实 Harness 子循环，全文主贡献是具身模型能力蒸馏和统一。 |

## 易误判的边界

- EvoSteer 的程序性技能晋升是主要方法之一，支持混合权重/Harness 分类；禁止写成全模型冻结。
- Learner2Skill 仅执行协议校准符合 Harness；在线学习者状态更新不符合。
- OptiCom 的策略适配器改自己的模板/选择策略，属于改进器；优化外部任务结果本身不构成理由。
- EngramBench、Mining Design Space 按专项评测/分析审核，无需基准自己在线自改。Verification 按验证接口与后继选择合同理论审核，不当作实际能力升级证明。
- ECG-RSI 和 OmniBrain-0 都有明确的外部 Harness 反馈与保留证据。主收录仍建议保留在模型/具身方向，但应保留 Harness 交叉链接；不能写成“没有 Harness”。
- CUAWright 证据只明确任务内脚本复用，跨任务/后继改进轮次保留仍 unknown。

## 版本与数据观察

最新官方 abs 逐篇重新读取；正文使用精确版本并保存字节哈希，旧 v1 与新版本分开。未修改 canonical 日期、版本、作者、摘要或数字。

- Learner2Skill：canonical v1，官方最新 v2（2026/10/02）；本建议按明确标记的 v2 正文。
- EvoSteer：canonical v1，官方最新 v2（2026/10/22）；本建议按明确标记的 v2 正文。
- OptiCom：canonical v1，官方最新 v2（2026/10/26）；本建议按明确标记的 v2 正文。
- Verification and Self-Improvement：canonical v1，官方最新 v2（2026/10/30）；本建议按明确标记的 v2 正文。
- ECG-RSI：canonical v1，官方最新 v2（2026/10/26）；本建议按明确标记的 v2 正文。

EvoSteer/OptiCom 的 v1/v2 选定文本块提取结果相同，不代表图表或完整 PDF 完全相同。Verification v2 有明显内容重组和扩充，禁止把 v2 引句假记作 v1 证据。

校验通过：61 段逐字引文（只规范空白）、25 份来源哈希、25 份原始 HTML/PDF 文本重新提取；覆盖 10/10。未重复运行主线程已通过的测试。

完整引文、段落索引、来源版本、抓取时间、元数据和不确定性见 findings.json；校验证据见 validation.json。
