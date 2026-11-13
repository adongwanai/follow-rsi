# 2026-11-13 全量积压审计交付

本子任务仅修改本目录，付费模型调用、生产数据修改和 Git 写操作均为 0。范围判断和元数据对照不等于实验复现、正式批准或线上发布。

- 64 项官方元数据候选：46 项代码链接与14 项原空日期可应用，4 项 no-op 保留原快照结案。父维护 agent 已应用 60 项，本目录 post-intake 验证了原文哈希、逐字段变更、first_seen 与旧 review 保留；其中 27 条旧正式 review 需要真实的新哈希回执，另 33 条没有伪造接收。
- 原周扫 392 项正文/文本任务：今天读了 7 对前后版本正文，复用 8 个已验证来源的既有比较，排除 3 个纯公式排版误报，共完成 18 项。周扫尚余 374 项；daily 单另有 2 项不在周扫中，跨表去重后真实剩余为 376 项。
- 9 项外部来源重试共 18 次，未取得所需全文。7 个 Elsevier HTTP 200 实为仅 coredata 元数据，不冒充全文恢复；其余为空体 202、非 PDF 418、8 个403和1个429。
- 4 项旧 issue 的8 个官方 abs/html响应完整且与上一有效源逐字节一致；OmniBrain 与 MoLRSI 的仓库 tree/README blob 也未变。已有具体工件缺口保持，不重复伪称今日重新全文审核。
- 新来源全量并集及原始HF成员通过 post-intake 对账：8856 个稳定 ID，规范库2033，合格原始遗漏0、未覆盖规范项0、缺失HF推荐日0。来源窗口外6358、发表日缺失465均保留可恢复状态。

## 需本轮正式纠正的已公开描述

1. PLVR：旧 v1 公开概括把原语和规则库都归为人工建立，v1 明确包含人工种子、模型编写原语及模型从教师轨迹挖规则。仅修正摘要的构建来源；version1和原刊期保持。见 `focused-version-corrections.json` 与独立回执。
2. DiscoveryRSI：2.5% 比较组在正文和附录叫 GPT；GPT-6 Luna 在另一段是语义评分器。仅将此比较组名称收紧，所有数字和 AI4AI move 范围保持。见 `discovery-summary-correction.json` 和 `../independent/summary-correction-review.json`。

HexaShell v2 的失败后写/修工具、冻结用于新布局的历史摘要保持。v3 已完成独立的有限技能策略分支纳入建议，但 canonical 不升级：操作流程和失败处理是跨轮保留的控制策略，固定API/loop/sandbox不称自演化；每份技能均有人审、跨新任务类别迁移和自动采纳未知。152/420开发回放及七任务尺寸捷径单独保存，不能用新版成绩覆盖旧分支反证。详见 `../version-boundary-review/hexashell-v3-independent-review.json`。

## 可复跑输出

- `reconcile.py --stage post-intake|post-review`：仅读生产输入，写本目录对应阶段。
- `post-intake/summary.json`、`backlog-ledger.jsonl.gz`：全来源稳定 ID、状态与逐项原因。
- `post-intake/version-review-tasks.jsonl.gz`：1627项周扫元数据/正文任务。
- `post-intake/daily-metadata-review-tasks.jsonl.gz`：102项去重字段任务，已比较但保留旧版本的3项与仍需正文的5项分开。
- `post-intake/metadata-application-verification.json`：60项应用和4项no-op的逐项核验，待正式绑定数单列。
- `version-review-progress.json`、`progress-version-review-tasks.jsonl.gz`：7对新比较、8个复用比较、3个排版结案；已比较不等于正式新版采纳。

最终正式绑定与发布以父任务的真实审核PR/merge/部署回执为准；本目录不声称已上线。
