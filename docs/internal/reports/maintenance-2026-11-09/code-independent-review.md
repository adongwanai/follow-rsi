# 2026-11-09 代码独立复审

范围：本轮 `scripts/feed/cli.py`、`scripts/feed/ci.py`、`.github/workflows/feed-weekly.yml` 及 `tests/feed/test_cli.py`、`tests/feed/test_ci.py` 的未提交差异。仅静态阅读调用链与测试；未运行付费 API、未重复全量测试、未改生产文件或 Git。

## 已修复 P2：周发现 PR 没有可触发的自动校验

- 位置：`scripts/feed/ci.py:324-329`；`.github/workflows/feed-weekly.yml:42-46`。
- 实际路径：weekly 使用 `secrets.GITHUB_TOKEN` 推送分支并创建/更新 PR，`queue_discovery_pr` 随后直接返回。由该 token 产生的事件不会递归触发普通 `pull_request` 工作流，因此 `validate.yml` 与 `build.yml` 不会自动校验此 PR；weekly 本身也没有验证/构建步骤。
- 现有显式校验通道不能直接复用：`feed-review.yml:33-38` 的分支白名单不含 `feed/discovery-`；`check_pr` 在 `scripts/feed/ci.py:413-416` 也明确拒绝此类分支。新 weekly 权限还移除了 `actions: write`。
- 影响：修复阻止了自动推 main，但新产生的 discovery PR 会缺少与实际 head 对应的检查结果；“检查后合并”仍需人为补充，自动维护不能完整闭环。
- 最小修复方向：为 discovery PR 接入一个确实支持该分支及其变更数据的显式校验入口，记录准确 head 的结果；如使用 `workflow_dispatch`，恢复所需 actions 权限。不要仅调用当前会拒绝 discovery 的 `dispatch_pr_check`。补一条真实调用路径单测，避免仅断言 push 目标分支。

修复后二次复核：`queue_discovery_pr` 在 upsert 成功后，显式向 discovery 分支触发 `build.yml` 和 `validate.yml`（现 `ci.py:328-333`）；两个工作流都增加 `workflow_dispatch`，weekly 恢复 `actions: write`。检查工作流从事件 ref 检出代码，对该次运行的 head 执行构建/数据验证/测试。返回值只称 `checks_dispatched`，任一触发失败直接抛出；单测覆盖两个触发及失败，不再将触发当作检查通过。此 P2 在代码层面已解决，未发现剩余阻断问题。部署本补丁到默认分支后仍须读实际 Actions run 的 head 与结论，不能以本静态审查替代远端 CI。

## 本轮其余重点未发现阻断问题

- 普通版本变化只保存原始候选；不会调用 `save_items` 覆盖已有 canonical 的论文正文、日期、版本、review 或 source hash。
- 对已有 canonical 新检测到的撤回，仅设置 `retracted=true`，旧审查和正文保留；既有撤回不会被新来源复原。随后 `remove_retracted` 按 canonical 标记清除公开日报/周报/订阅中的相应条目。仅在 evidence library 而不在 canonical 的新观察仍停留在 raw/提醒，此路径不自动改写证据卡。
- weekly 先切换到 `feed/discovery-<week>`，队列函数校验当前分支，`commit_paths(push=False)` 后仅显式推 discovery 分支；此次调用链没有直接推 main 或部署 Pages。
- 已有正式非 demo 日报、或同日期真实 MERGED 审核 PR，均在切分支/重建审核单前返回；避免重新打开已经出版或审核过的日期队列。

验证边界：上述为独立代码审查，不宣称再次运行了测试。新增测试覆盖版本不覆盖、canonical 撤回标记、身份异常、防重建、分支推送、discovery 双 CI 触发与触发失败；撤回测试 mock 了公开页面清理，而实际清理已有独立 digest 测试。
