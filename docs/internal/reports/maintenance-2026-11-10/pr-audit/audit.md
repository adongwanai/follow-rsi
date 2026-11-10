# PR 与出版状态核验（2026-11-10）

取证时间：2026-11-10 00:06:16 UTC；以下是当时快照，正式处置前应重读当前值。证据：initial-audit.json、open-prs.json、open-issues.json、workflows.json、runs.json 和 live/。

- 本地 main 与 origin/main 均为 `0f9de911ee1ee33f68b6ffc8c9a22876ca82a1f2`，当时工作树干净。
- 开放 PR 为 0；开放 issue 为 20，其中 15 个为新 arxiv-watch 候选。没有可供复用的未合并 PR。
- PR #3 已于 11/02 08:27:25 UTC 合并，merge SHA `1eff06bc1df40b6072e512a859ea4760331237d5`，不再视为阻塞。
- `feed-daily.yml`、`feed-eval.yml`、`feed-publish.yml` 仍为手动暂停状态，符合要求。
- 当前 main 的 Pages run 42570430224 和 Validate run 42570430205 成功。
- 昨日定时 Daily review run 42608862558 真实日志返回 `date=2026-11-09,status=already_published`，旧审核单防重建修复已在实际 CI 生效。
- 当前首页、日报归档、11/09 HTML/JSON、W45 HTML/JSON、latest、Atom、status、两份 README 的线上字节与当前 main 对齐；11/10 HTML 仍 404，不能称今日已发布。
- 11/09 一篇为 HEELO（arxiv:2611.07461）；W45 为 20 篇日报论文、15 篇明确历史补录；latest 55 篇；Atom 每刊一期、时间正序；10/27 撤回版保持不在日期列表。
- 11/09 sources.hf-daily.count=40 是多日采集汇总，不是 11/09 榜单成员数；当时实际榜单为 8。后续晚到对账以今日 source-intake 的原始快照为准。

## 晚到补刊与今日简报的代码约束

现有 `review.py/window.py/digest.py/ci.py` 支持 `date=2026-11-09, reviewed_on=2026-11-10` 的明确补刊。必须保留真实 first_seen、实际 HF 推荐日及旧审核记录。

`publish_day` 从当前审核单重建整期；不能只用新增条目覆盖旧审核单，否则会丢掉已发 HEELO。`queue_daily_pr` 会按预期返回 already_published；自动 queue 也可能因为旧条目 llm 为空而漏旧批准行。应复制完整旧审核单，保留旧行并追加新行，经新精确 head 的真实日期审核 PR 完整复审。旧审核单、provenance 与 canonical review receipts 先归档。

现有已发布日期保留初始 published_at 和原采集 sources，内容改变写 updated_at，Atom 仍保持该日一个条目。新观察快照应明确列为本次补充采集，不把初始 sources 静默改称今天抓取。

若 11/10 没有本日可核实论文，可在真实日期审核单、真实合并 provenance、双语 daily-status 的基础上调用 `publish_day(..., allow_status=True)` 发布有实质来源/审核信息的状态简报。不能把无内容空页或本地 published 标志当线上出版。

`build/maintenance-2026-11-09/publish-reviewed.py` 可借鉴但不能未改直接运行：它固定 Nov9 输出目录。应核对同仓 main 合并、精确期望 head、owner 合并或精确 head 批准、真实 CI、merge blob 与当前 YAML 一致，再保存真实 `github_pr/owner_login/merge_commit`；审查与出版分 PR，不直接推 main。manifest 路径使用仓库相对路径，避免违反旧仓库名全仓检查。

## 新 issue 对账

issue-canonical-mapping.json 保存完整映射。五篇 watch-only 为 #77 CompressionBench、#76 Adapting the Process、#73 Flex-RSI、#72 BOXBOX、#71 RSI-ESA，其余十篇已在 canonical，不能重复新建。watch 候选 first_seen 至少以 issue 的真实 created_at 为证据，而非论文原日期或今日抓取时间。

四篇 watch-only 原文与初审已写入 watch-candidates/，RSI-ESA 由 source agent 处理。所有范围意见都是建议，正式批准仍由真实日期审核 PR 记录。
