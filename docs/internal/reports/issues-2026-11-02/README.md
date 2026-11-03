# Issue 核查、补刊和部署结果

2026-11-03：[#33](https://github.com/adongwanai/follow-rsi/pull/33) 已合并，Pages 部署成功并实际请求验证。合并提交 `4289c884493efc2c5235f23f7edb29fcebdbc364`；线上检查时间 `2026-11-03T02:12:05Z`。

## 已完成

- 已恢复 [10/28](https://adongwanai.github.io/follow-rsi/daily/2026-10-28.html)、[10/30](https://adongwanai.github.io/follow-rsi/daily/2026-10-30.html)、[11/02](https://adongwanai.github.io/follow-rsi/daily/2026-11-02.html) 三期，分别1、1、3篇。原HF日期和实际审核日期分开，10/27撤回记录保留。
- Atom含3期日报及1期创刊回顾；latest含21条已审记录。日期列表不再把回顾当日报。
- 7条已批准历史论文补入候选目录，保留unknown证据。107条原论文事实和README手写区域未改写。
- 修复成功空结果误报故障、arXiv非法ID请求、辅助来源恢复收尾，补充HarnessPro v2数字说明。
- 增加不含凭据和提示词正文的API用量日志；付费工作流继续暂停。

## Issue结果

本批20个issue已有13个关闭：#6先由恢复审核的自动流程关闭；本轮实际关闭#8、#9、#10、#14、#17、#21、#24、#25、#26、#27、#28、#29。所有关闭及评论已用GitHub实际状态核验。

保留7个：#16、#18、#22等待质量闸门通过；#19、#20、#23、#30等待具体Harness工件及复用证据。每项都已在issue中说明阻塞及完成条件。重复旧日期队列#32、过时空精选单#15已关闭并保留历史；这不表示未知论文被接收或空周报已发布。

## 验证与证据

- 本地完整测试370项通过；展示短名调整后的目录/日报测试38项通过。
- 浏览器8组验收、52张截图，无控制台错误；629个生成文件构建幂等。
- PR33的GitHub build与validate通过；Pages实际部署与16个线上资源核验通过。
- 历史模型召回0.8571仍低于0.90；本轮未执行付费评测，也未改变阈值。此次出版依据仅限已明确批准的历史恢复批次。

[线上部署回执](deployment-verification.json) · [GitHub逐项结果](github-resolution-results.json) · [候选处置与补证要求](candidate-resolution-plan.md) · [独立复审](final-independent-review.md) · [测试与构建](final-validation.json) · [用量审计](paid-usage-audit.md) · [工作流暂停记录](paid-workflows-paused.json)

早先报告中的“尚未部署”“待关闭”是当时检查快照，后续真实结果以本页和关联回执为准。
