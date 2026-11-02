# 2026-11-01 队列与流水线审计

本地已修复遗留 `pending` 在顺延时重新进入新审核单的问题，相关 **62 项测试通过**。远端 PR #13、main、原审核单和公开内容均未修改。机器状态与引用回执见 [pipeline-audit.json](pipeline-audit.json)。

## PR #13 的 owner 检查为什么失败

[PR #13](https://github.com/adongwanai/follow-rsi/pull/13) 的 head 为 `06ebb67720d30cf0024705c91df243bb48616a36`，包含 75 篇论文、69 条公告，合计 144 条，决定全部为 `pending`。此前 10 月 31 日远端队列也是同样的 144 条 `pending`。错误对应的 `arxiv:2507.11473` 两天的 source hash 相同，`carried_from` 均为 10 月 30 日，没有 owner 备注。

[失败运行 41297323897](https://github.com/adongwanai/follow-rsi/actions/runs/41297323897) 执行 trusted main `0734286c6d389cd6bd392b0e6a08dd3a0dbd4ebe`，在 `validate_daily_review` 抛出：

```text
ValueError: arxiv:2507.11473: pending review blocks publication; use defer to carry it forward
```

这次拒绝符合发布规则。远端 main 仍用旧逻辑生成 `pending`，并会把顺延的 `defer` 重置为 `pending`。本地修复分支虽然已默认 `defer`，却仍在复制 `OWNER_FIELDS` 时将旧单的 `pending` 覆盖回来。因此，即使只合并先前的默认值修复，历史队列也可能继续失败。

本次只在 `queue_daily_review` 复制 owner 字段之后增加两行：将新行里的 `pending` 规范化为 `defer`。保留 `accept / reject / move`、方向和摘要覆盖、推广设置、owner 备注；原日期审核单及传入的未合并 PR 数据不变。没有修改发布验证器，显式 `pending` 仍阻断论文和公告校验；`defer` 不成为发布批准。

## 两个 action_required 的原始原因

- [Validate data and tests：41297323223](https://github.com/adongwanai/follow-rsi/actions/runs/41297323223)
- [Check generated files：41297323256](https://github.com/adongwanai/follow-rsi/actions/runs/41297323256)

两页均返回 HTTP 200，并明确显示：

> This workflow is awaiting approval from a maintainer in #13

API 对两个运行都返回 **0 jobs、0 check runs**，触发者为 `github-actions[bot]`。因此它们尚未执行测试或构建，与上面的 owner-decision 异常是两项独立问题。仓库的 fork PR approval policy 当前为 `first_time_contributors`；这些 API 信息不足以进一步断言平台内部如何给本次 bot 触发分类。本次没有批准 workflow、改审批设置或重跑远端任务。

## 计划时间与实际运行

本地 `$CODEX_HOME/automations/follow-rsi/automation.toml` 中 heartbeat 为 `ACTIVE`，配置每天 08:00，prompt 明确 `Asia/Shanghai`；本次只核对了配置，没有核实 heartbeat 的实际执行历史。

远端 main 的两个 GitHub cron 没有时区覆盖，按 UTC 解释，与本地 08:00 是不同计划：

| 工作流 | cron 对应北京时间 | 11 月 1 日实际运行创建时间（北京） | 相对 cron 时间的差值 |
| --- | --- | --- | --- |
| Follow RSI daily | 10:23 | 17:22:57 | 6 小时 59 分 57 秒 |
| Follow RSI owner review | 11:17 | 18:23:38 | 7 小时 6 分 38 秒 |

对应运行：[41292895944](https://github.com/adongwanai/follow-rsi/actions/runs/41292895944)、[41297291395](https://github.com/adongwanai/follow-rsi/actions/runs/41297291395)。job 分别在创建后 2 秒、3 秒启动。现有 API 回执没有解释为何调度事件晚于 cron；不能把该差值归因于测试执行耗时。本次未改时间配置。

## 验证与待处理

新增回归先复现 `pending != defer`，修复后执行：

```sh
.venv/bin/python -m pytest tests/feed/test_daily.py tests/feed/test_review.py tests/feed/test_ci.py tests/feed/test_corrections.py tests/feed/test_window.py -q
```

结果：**62 passed in 20.80s**。新增 6 组覆盖磁盘旧单和未合并 PR、owner 的接受/拒绝/改分类、论文和公告顺延、原审核单含 YAML 注释逐字保留、输入对象不变，以及显式 `pending` 继续拒绝。全仓测试由主任务统一执行，本审计未重复运行。

本地修复尚未进入 main，不能将它表述为 PR #13 已恢复通过。后续需在主任务批准的集成流程中更新代码、重新生成队列，再核验 owner 检查；两个 `action_required` 仍需 maintainer 批准执行。全程没有付费模型调用、Git 提交/推送、审核批准、合并或发布。

## 冻结批次的覆盖统计勘误

以下核算仅针对 [10 月 30 日逐条台账](../maintenance-2026-10-30/coverage/item-status.jsonl)、[覆盖汇总](../maintenance-2026-10-30/coverage/coverage-ledger.json)、[续跑计划](../maintenance-2026-10-30/coverage/resume-plan.json)、[模型终态](../maintenance-2026-10-30/coverage/model-run-final-status.json)，以及 [10 月 31 日新增台账](../maintenance-2026-10-31/new-item-status.jsonl) 和 [续跑计划](../maintenance-2026-10-31/resume-plan.json)。这 6 个文件保持原字节不变，SHA256 保存在本报告 JSON 中。11 月 1 日进行中的 30 条复核不计入此冻结快照。

可互斥相加的是批次和保存状态：**1,206 = 1,139 条冻结记录 + 67 条后续新增**，两批 ID 没有交集；其中 **1,139 = 原 1,124 条 + 单列 HF 新增 15 条**。冻结记录的完整状态分布如下；前 9 行属于原 1,124 条，最后一行属于 HF 新增 15 条。

| 保存状态 | 原 1,124 条 | HF 新增 15 条 | 合计 |
| --- | ---: | ---: | ---: |
| `current_three_round_advice` | 163 | 0 | 163 |
| `model_advice_only` | 787 | 0 | 787 |
| `protected_owner_correction` | 33 | 0 | 33 |
| `new_curated_catalog_source` | 1 | 0 | 1 |
| `protected_curated_catalog` | 17 | 0 | 17 |
| `official_body_model_advice` | 47 | 0 | 47 |
| `source_blocked` | 9 | 0 | 9 |
| `prior_three_round_reuse_candidate` | 56 | 0 | 56 |
| `model_error_pending` | 11 | 0 | 11 |
| `hf_three_phase_source_advice` | 0 | 15 | 15 |
| 总计 | 1,124 | 15 | 1,139 |

后续新增 67 条的保存状态也是互斥分区：37 条 `three_round_scope_recommendation_owner_pending`、21 条 `source_scope_review_pending`、9 条 `official_post_body_review_pending`。37 条范围建议为 5 条 include、30 条 exclude、2 条 defer；这些记录仍缺生产用分类／双语摘要步骤，范围复核完成不代表可以发布。

此前把「163 条匹配三阶段」直接描述为整个 1,139 条的覆盖数，口径不完整。**163 条来自原 1,124 条的流水线协议**，核对来源身份／日期、模型及所需正文、独立来源范围复核；**15 条 HF 新增采用另一套三阶段来源审查协议**。按 `rounds_with_matching_input` 是否完整包含 1、2、3 计数，整个 1,139 条实际有 **178 = 163 + 15** 条。178 只是阶段编号与输入匹配记录数，不能据此声称采用同一协议全部审完、有 3 位独立审核人、owner 已批准，或证据卡片已完整审计；后续的 37 条范围建议也须单列。

原 163 条中，`arxiv:2610.32046`、OpenAI 的 `updated-model-spec` 与 `how-we-detect-frontier-model-misalignment` 仍带历史证据等价性说明，不能在汇总时抹去这一限制。

### 审核完成、等待 owner 与故障记录不是互斥桶

37 条已完成范围建议的记录，正好也是 37 条等待 owner 裁决的记录，其中 20 条同时保留历史模型 API 错误。三者描述不同阶段，不能相加成互斥总数。全部 1,206 条审计建议台账的正式决定均为 `defer`，`publication_authorized=false`；这也不等于 1,206 条都已形成新一轮可交付 owner 的完整审核单。

冻结 1,139 条的历史 owner 决定另存为：未记录 1,087、defer 20、move 10、accept 16、reject 6。原批次中受保护的 50 条是 33 条 owner 更正加 17 条既有证据库记录。本轮没有新增 owner 批准或发布，也没有覆盖这些历史决定。

### 续跑计划列的是阶段任务

10 月 31 日续跑计划的各队列如下，同一 ID 可以出现多次。

| 阶段队列 | 任务条数 |
| --- | ---: |
| `resume_summary` | 369 |
| `retry_model_api` | 31（旧 11 + 新 20） |
| `retrieve_original_abstract` | 9 |
| `complete_official_post_summary` | 1 |
| `reconcile_source_version_or_text` | 73 |
| `independent_source_review_not_yet_recorded` | 164 |
| `classify_new_papers` | 57 |
| `new_source_scope_review` | 21 |
| `new_official_post_body_review` | 9 |
| `new_metadata_confirmation` | 1 |

以上 **735 个任务归属去重后为 495 条记录 = 旧 428 + 新 67**。其余 **711 条未进入这些命名队列不代表已完成**：其中 163 条当前三阶段建议、384 条仅模型建议、33 条受保护的 owner 更正、17 条受保护的既有证据库记录、46 条官方正文模型建议、53 条历史三阶段复用候选、15 条 HF 单列三阶段来源建议。

**164 条缺第三轮来源复核是内部未完成工作，不能归入外部阻塞。** 其中 158 条同时在 369 条摘要队列内；与 31 条历史模型 API 错误、9 条原摘要缺口、73 条来源版本／正文协调队列的交集均为 0。

### 外部故障只能按已有回执表述

历史文件记录了 31 条模型 API 错误和 8 条出版方访问阻断，二者无交集，合计 **39 条有历史外部故障证据的记录**；其中 20 条也在上述 37 条已完成范围建议内。本次没有重试网络或模型，因此不能声称这 39 条在 11 月 1 日仍全部阻塞。

旧批次 9 条缺原摘要中，8 条有访问阻断回执，另 1 条是官方 IEEE 编辑文章本来没有摘要（`s2:c470d4b2c990d73e0b34f5f9e384423fd7c09a14`），不能算访问失败。新增另有 1 条 S2 记录缺摘要且发表日期在未来（`s2:33e84e388ed32372fb1a7fbbc251f96f3375a29a`），需要确认来源和日期，没有记录访问失败。可把这两类合报为 10 条来源／元数据缺口，但不能称为 10 条访问故障。

保存的 HTTP 402 是自动模型阶段的共同依赖问题：369 条论文摘要暂停、1 条公告摘要待处理。它不证明每条尚未尝试的来源审查都受到外部阻断。来源阅读和范围复核可以独立继续。此统计勘误只写入今日报告，未修改旧报告、正式数据或历史决定，也未重复运行测试或调用付费 API。
