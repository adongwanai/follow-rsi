# 10/27–11/2 日报恢复与已批准审核落实

本批使用 owner 2026-11-02 的明确批准，处理已有来源意见，并修复 HF 刊期与实际审核日混用的问题。此目录中的归期审计是修复前快照，后续补证和最终决定须结合对应回执阅读。

- 原始意见批准回执共 680 条：235 纳入范围、396 排除范围、49 待补证。AdaPRA 在后续正文复审中发现跨任务继承疑点，另记更正并继续 defer；不把全批批准解释为抹去反证。
- 补回 17 个原始 HF 记录及 2 个推荐日观察，原科学字段不改。17 个新恢复记录均有摘要范围意见及独立复核，建议排除；不伪造此前人工批准。
- 对 40 条已存在的双重范围审查补齐索引；38 条输入哈希完全匹配，2 条只新增推荐日观察，保留哈希迁移凭据。
- 补刊内容准备：10/28 The Trinity，10/30 VibeGame，11/2 R²Orch、CEPO、RoboArchitect。正式决定和上线状态由日期审核 PR、合并回执及最终出版回执确定，内容草稿本身不代表发布。
- 10/27 保留撤回及历史回顾；10/29 没有符合当前专题的 HF 纳入项；10/31、11/1 为已存请求返回空榜。这不证明其他来源当天没有信息。

## 校验

当前实现全套 pytest 354 项通过；107 篇证据库记录和 9 条路线校验通过；590 个生成文件两次构建字节一致；README 手写部分不变。代码与数据校验不同于模型质量评测：最近完整评测 precision 0.9231、recall 0.8571，召回低于 0.90，继续保留 `[GATE BELOW THRESHOLD]` 告警。

本批没有付费模型调用。新日刊按真实 HF 推荐日归期，同时显示原发表日、版本日和实际审核日。历史日期审核不会改写首次发现日，也不会把旧榜单混入新一期。

## 文件

- `date-audit.json/.md`：恢复前逐日审计。
- `pipeline-audit.md`：逐条发布保护与真实 owner 合并凭据要求。
- `approved-content.yaml`：68 条已有正例的双语内容草稿，均有来源引句；不是发布清单。
- `additional-approved-source-opinions.json`：遗漏的 40 条旧审查和两条输入哈希迁移。
- `oct28-review.json/.md`：Trinity、VibeGame 和 AdaPRA 的定向正文复审。
- `raw-recovery.json`、`r2orch-date-reconciliation.json`：原始记录恢复及观察性标记修正。
- `missing-hf-independent.json`、`missing-hf-reconciliation.json`：17 条补回记录的范围审查。
- `missing-hf-official.json`：保留官方元数据响应的解析结果；与独立报告引用的 `build/publication-recovery-2026-11-02/missing-hf-official.json` 字节相同，便于公开核验。
- `validation.json`：当前测试、构建与手写内容保护回执。
