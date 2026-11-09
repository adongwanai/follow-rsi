# 2026-11-09 PR 与周发现审计

审计基线为 `b12e626724ea32a0146c58d9ea98349c45ccd7fe`；本子任务没有外部写操作、提交、推送或付费调用。原始 API、PR 文件、逐字段差异和隔离渲染记录均在本目录。

## PR #61：关闭重复审核队列

Head `7246eb8517b661d3faefd7c8ac3496c218bedfac`。当前正式 11/08 审核单为 467 条（434 reject、15 backlog、18 defer），该 PR 变为 242 条（46 reject、3 backlog、193 defer）。它遗漏 413 个正式原行，包含 388 reject、12 backlog、13 defer；共有 54 行的决定与哈希未变。新增到这张单的 188 行全部已在 11/08 台账：12 个正式/目录记录、165 个可复用意见、11 个待补证，漏项为 0。不能用重建单覆盖已合并审批与出版回执。

建议主任务核对最新 SHA 后执行 `gh pr close 61 --repo adongwanai/follow-rsi`，保留现有 canonical 与台账状态；不把关闭 PR 声称 188 条已重新批准。

## PR #67：空 picks 合法，先修复元数据漂移再合并出版

Head `4d876abdc650c00b31416690b9fab7e4448e6cd5`；唯一变更是四行 `review/2026-W45.yaml`，picks 和编辑说明均为空。隔离 fixture 使用 4c0a54c 正式 canonical 和 PR 的 YAML，validate_weekly_picks 及 publish_week(client=None) 通过：20 篇周内日刊论文、15 篇已批准历史补录，交集 0。生成了本地 Markdown/HTML/JSON，不生成图片、不调用模型、不冒充线上出版。

在 b12e626 原状态下，approved_weekly_backlog 明确失败于 source changed after backlog review；15 篇 backlog 的旧 hash 原来都匹配、现在全失配。因此当前 owner-decisions 成功并不证明周报出版可执行：该检查仅验证 picks，并不遍历 backlog 来源绑定。

## CI 证据

两个 PR 的 exact head check-runs 均为 0，只有 Follow RSI owner decisions commit status。自动队列用 GITHUB_TOKEN 建 PR/推送，普通 pull_request 工作流不会被这类事件触发；ci.dispatch_pr_check 仅主动分派 feed-review.yml。build.yml 无 workflow_dispatch，validate.yml 也无。

最小不改内容的触发方法是使用现有 owner gh 凭据依次关闭、重新打开 #67：

```sh
gh pr close 67 --repo adongwanai/follow-rsi
gh pr reopen 67 --repo adongwanai/follow-rsi
gh pr checks 67 --repo adongwanai/follow-rsi
```

随后核实实时 head SHA、Actions 对应 PR 和 build/validate 结果；pull_request 实际测试 GitHub 的合并提交，应核对该合并提交包含准确的目标 head，不能把别的 main 测试结果填上。

## b12e626 的实际变化

1,828→1,830 个 canonical ID，新增 Aspire 与 S³Gym，无删除。1,627 个既有记录变动、1,236 个来源哈希变动。first_seen、review、retracted 完全未变。84 个 hf_daily_dates 仅由缺字段/null 补成 []，未新增或删除真实推荐日。

published 改 1,122 条，其中 893 条同日补时间精度、229 条日期不同（含原空值/旧 HF 版本日纠正）；updated 改 1,148 条，其中 758 条同日、390 条跨日。另有 386 处版本号、83 处摘要、14 处标题、74 处链接变化。不能统称数据错误，也不能未经核验继承旧批准。22 个代表样本的官方 API 复取在 45 秒超时，本审计不声称已逐条确证新元数据。

父提交保留已审快照；建议归档 b12 的完整版本候选与差异后，恢复其修改的既有 canonical 到父提交，保留新目录身份和今日独立来源增量。此次无新增撤回，因此不会因恢复掩盖撤稿。新版本候选另行按来源与正文审核，不篡改旧 first_seen 或批准 hash。

直接更新 main 来自 feed-weekly.yml：默认分支 checkout 后执行 versions，check_versions 将 dedupe 合并结果保存到 items.jsonl，末步调用 ci commit 默认 push=True 并部署 Pages。

## 最小修复与回归验证

已在分配的五个文件实现：版本巡检保存原始 metadata 候选与告警，保留 canonical 审批内容；身份缺漏、意外 ID、重复 ID 失败并留原始快照；明确撤回仍置 retracted 并执行公开内容清理。周发现先准备独立分支，最后开/更新 discovery PR，不直推 main、不提前触发 Pages。日审核队列遇到正式出版或同日已合并审核时跳过，保留原决定。

离线回归测试覆盖日期/版本/摘要/hash/first_seen 保留、来源身份错误、撤回处理、PR 路由、拒绝从 main 推周发现、无变更不建 PR、已出版与已审日队列防回退。`.venv/bin/python -m pytest -q tests/feed/test_cli.py tests/feed/test_ci.py`：73 passed（最终复跑 10.59s），git diff --check 通过。测试中的模拟 CI 环境仅是 pytest fixture，不是实际 CI 成功凭据。
