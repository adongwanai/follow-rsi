# 11/18 PR #135 历史处置交接

本目录只生成建议、来源收据与可恢复状态；未写 canonical、未做 Git/GitHub 操作、未付费调用，也未声称已合并或上线。

本次可决候选为 **19 条历史 backlog + 10 条 reject**。父任务应采用下列精确稿，绑定独立交叉核验，取得真实日期审核 PR 合并后再 apply：

- `positive-review-rows-v4.yaml`，SHA256 `00d288088b8acad04993c32fc41b8ba560926b40e8381a89e640dc806b446d89`。
- `positive-proposals-v4.json`，SHA256 `ee6683a9d201b99ded0eef8e976a519ec2319c52784ed36da7db0d7fae3863ce`。
- `exclusion-review-rows-v1.yaml`，SHA256 `df206eb8de1d18119b2da84696005d2c6083d67f6bd17d0200433cf509560c14`。
- `exclusion-proposals-v1.json`，SHA256 `373720956c9cb4070de300d1128e3e17c4b4c92544da946ea3e0263e46907b26`。

建议刊期 `2026-11-17`、实际审核日 `2026-11-18`，均为历史补录，不改 `first_seen`，不冒充 11/18 新论文。14 条正例和全部 10 条排除有 exact canonical-source-hash 的 11/02 范围回执；其余 5 条依当前持续授权，仍需真实日期审核 PR。范围回执不是人工逐篇阅读、模型成功或已出版凭据。

## 来源与摘要

本轮定向恢复 30 个官方来源请求，均为免费 GET：19 篇正例 HTML、10 条排除的 11 个来源。19 篇正例原 HTML 均与旧审查原始 SHA 完全一致；10/30 的原 SHA 存在 `maintenance-2026-10-30/independent/source-provenance.json` 的 `items[].body_receipt.attempts[].sha256`，旧 build 路径失效不等于原来源收据缺失。重新提取的 text hash 单独保存，不声称与旧提取器字节一致。

77 条正例旧引句、25 条排除引句完成边界明确的核验；个别 HTML/Atom 标点或摘要版本差异在逐项记录中区分。IEEE 编辑短文为完整 3 页；self-generated goals 只核对明确关联的作者预印本摘要及 reciprocal DOI relation，不宣称取得期刊全文。五篇 post 的站点 HTML 不宣称与历史逐字节相同。

`handoff-local-verification-v2.json` 对 29 份 JSON/YAML ID、source_hash、摘要、分类、evidence 及 30 个 raw/text hash 直接核验；19 份最终双语摘要均通过 `check_summary(...)["ok"]`。数字 guard 只查字面数字与语言一致性，语义、分母和基线另按原文核实。

保留 v1、v2、v3 及 amendment，最终 v4 包含以下重要纠正：

- Budgeted RSI 的 87.0% 是被返回节点的 held-out HumanEval+ 得分，不是“87% 节点被返回”。
- retro 的评估由 11 个提案导出 adaptations 加 1 个人写对照构成；公开摘要明确分开。
- Phronix 的 93–95% 首次成功率仅以冷启动已解决的任务为分母。
- RSIV 总体结果表的静态基线可执行性为 64.98，消融表 H0 为 51.36。公开中英摘要披露此未解决矛盾；+28.02 只绑定总体结果表，不改作者原数字。
- HSE 训练期依据反馈更新并继承 writer/evaluator 规则与证据权重，应为 `harness/improver`、次方向 `meta`；目标适配期才固定这些规则。未改 catalog。
- ReSight 的 matched budget 仅指同基准在线执行预算，不能扩展为包括独立探索的总成本匹配。
- RSI-Opt held-out 描述访问、HarnessMM 整体配置归因、FilingLoop 在线反馈、Compile Away 开发期看过留出失败等限制均保留。仅多模型运行不等于跨模型迁移。

v4 另为 4 篇 Harness 专项 safety/evaluation 明确 `secondary: [harness]`；全部 19 个方向通过当前 `scope_status`，未改 taxonomy 或发布范围。

## 原 121 条全部保全

`data/feed/raw/maintenance-2026-11-18/historical-disposition/disposition-ledger-v2.jsonl.gz`：SHA256 `1e37b9d95567d7ec7fa8616ae5ae7a2564c9dce7987887cac3e5ff18fcc6a004`。人读表为 `disposition-table-v1.md`，统计为 `disposition-summary-v2.json`。

每条保存原队列/完整旧意见/owner 回执/后续反证/现有 review 对象及其日期、PR、merge commit、hash、具体缺口、下一动作和 issue 入口。所有 121 个原 canonical.review 均为既有 defer 收据；只推进上述 29 条。其余 **92 条必须 `keep_canonical_review_unchanged`**，不要重写为今天的统一 defer。

92 条工作状态分开记录：25 项已有纳入范围意见但仍需编辑准备；31 项已有排除范围意见但需内容绑定或独立覆盖核验；14 项只到有界初筛；8 项保留已有 catalog；10 项有具体工件/范围证据缺口；3 项外部来源访问阻塞；1 项 AdaPRA 后续反证。前 56 项是仍待完成的编辑工作，不能借称“外部阻塞”。

保留 RSIHub 的 `harness_eval` 最新正确分类；旧模型 `harness_method` 仅作历史。AdaPRA 按后续正文纠正暂缓。旧 scope hash 与当前不一致的 2610.27100、2610.39714、2610.35077 不静默重绑。所有 issue 入口均继承保全审计中的已有 issue；本子任务未创建或关闭 issue。

最终独立核验回执位于同日 `publication-crosscheck/`，由 `/root/nov18_hf17_crossreview` 单独冻结；父任务以其精确 v4/v1 核验结果为准。本目录中的 `pending` 字段保留生成时状态，不能独立当作已上线证明。
