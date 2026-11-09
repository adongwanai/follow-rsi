# 2026-10-30 最终代码与状态交叉检查

本轮先只读检查，随后按主代理明确授权，在 `health.py` 与 `test_health.py` 最小修复实测告警缺陷；未刷新真实数据、改评测标签/阈值或 GitHub 状态。**本代理编写了 HF 与健康告警修复，本报告包含交叉自检，不能算作另一名作者的独立审查。** 主代理另行审阅，并负责全量测试和真实状态刷新。

## 检查结果

HF 修改未发现阻断性问题。修复前采集快照中，source-attempts 最后一次结果与 state 的 `last_ok / last_count / last_error / degraded` 全部一致；网站 status 是 state 去掉 `seen_ids` 的准确投影。未发送来源告警被空刷新清除的问题已在工作区修复，health 测试 10 项通过。标题身份映射仍未实现。

## HF 部分失败与日期

`scripts/feed/fetch_hf.py:35` 逐日请求，在 HTTP、网络、JSON 或外部数据解析错误时记录失败并继续。失败日期不进入 `raw.days`；成功日期与记录保留。非空 `raw.errors` 在 `fetch_arxiv.py:148` 使来源整体 `ok=false`，不会变成全成功。

只有 HTTP 400 且 JSON 明确给出 `date must be less than or equal to ...`、请求日期晚于上限时，才标 `not_ready`。其他 400、429、500 仍为 `error`；都保留响应体与 HTTP 状态。`requested_at / finished_at` 来自真实时钟，不使用批次 `now` 冒充请求时间。

今日真实重抓证据：

| 日期 | 请求结果 | 入库语义 |
| --- | --- | --- |
| 2026-10-30 | 00:14:24 UTC 请求，HTTP 400；HF 明确只开放到 10-29 | `not_ready`，不生成当日空列表 |
| 2026-10-29 | 00:14:24–25 UTC，HTTP 200，原榜 14 条 | 原样保留 10-29 日期，关键词筛后 5 条 |

raw 路径为 `data/feed/raw/hf-daily/2026-10-30.json`，顶层 `status=partial`。该文件名是抓取日期，内部榜单日期仍为 10-29。随后 arXiv 元数据补全遇到 429；`hf-refetch.json` 的 5 条记录均保留 `metadata_pending` 和错误，原始 published/updated 为空，不拿 HF 版本日期或抓取日填补。

测试覆盖普通 HTTP 错误、非开放日期、超时、损坏 JSON、坏响应形状、实际时钟及 dispatcher 的部分失败。此前本次维护执行 sources 38 项、health 8 项均通过；本轮差异未再修改，未重复跑同一测试，`git diff --check` 通过。

## 来源恢复历史与状态

arXiv Harness 查询第一次在 **00:01:55 UTC / 北京 08:01:55** 返回 429；冷却后的重试在 **00:18:20 UTC / 北京 08:18:20** 完成，成功但为零条。state 的 `last_ok=true / last_error=null / consecutive_errors=0` 正确反映最后一次请求，不代表全天没错误。`consecutive_failures=3` 仍保留，因为既有健康规则把空结果也计为一次失败；这里是连续运行次数，不是三个自然日。

初次 429 未从 `source-attempts.json` 和 `arxiv-harness-fetch.json` 删除。它已从仅展示最新尝试的 last-fetch 快照中被替换，因此最终维护记录必须归档完整 attempts。当前 `build/` 被 Git 忽略，只提交最新 state 会丢失可持久回溯的失败过程。

其它未恢复状态也没有被洗掉：HF `last_ok=false`、作者追踪 `s2-authors` 429 / `last_ok=false`、HF 元数据补全 `arxiv-hydration` 429 / `last_ok=false`。S2 citations 成功只证明该入口可用，不能代替 authors 入口恢复。S2 两入口都按匿名模式记录，最小间隔 3.1 秒。

### P2：未发送的健康提醒在汇总刷新中消失（本轮已修复）

修复前快照中，`arxiv-harness`、`github-releases`、`rss-weco`、`s2-authors` 都已有连续 3 次空结果/失败且无 `issue_number`，但 `site/feed/status.json` 的 `pending_issue_actions=[]`。旧 `update_health` 在处理单次 outcomes 时创建 events；随后本次采集脚本调用 `update_health(root, [])`，用空 events 覆盖尚未发送的提醒。

最小修复已将阈值与恢复检查移到统一启用源循环，依据持久状态重新生成全部待办。失败计数、last_run、last_count、weekly 等仍仅由真实 outcomes 更新。单源恢复后只清除该源未发送提醒；已创建 issue 的待关闭动作、未运行告警的恢复关闭动作都能跨空刷新保留，显式 issue_client 仍只创建一次、关闭一次。

有意义回归先在旧代码复现 **3 failed / 7 passed**，修复后 `.venv/bin/python -m pytest tests/feed/test_health.py -q` 为 **10 passed**。覆盖多源保留、整份 state 刷新前后不变、单源恢复、模拟 issue 只发一次/只关一次，以及未运行恢复关闭待办；`diff --check` 通过。本代理未刷新真实健康状态、未调用外部 issue。主代理随后刷新状态并跑全量测试。

## P1：两篇标题身份映射尚未实现

PR #3 的 head 仍为 `e5666c58ab93f946103d5aef6e501580c15193ec`，base 为 `b9246ac880332688cabce1e46a0914c088089b19`。逐函数 AST 对比证实 `verify_metadata_identity()` 完全一致；代码与标签中没有针对两篇论文的有来源映射。

使用 `build/ci-eval-pr3/identity-check.atom` 和当前函数做只读离线复现：

| 记录 | 当前结果 |
| --- | --- |
| 2609.08175 v1，原题名 | 匹配 |
| 2609.08175 v2，A Theory of Reliable Self-Evolution for Agent Harnesses | 不匹配 |
| 2607.07007 v1，Thinking More, Harnessing Better... | 与 curator 简称不匹配 |

因此不能报告成“映射已在 PR 修好，只是 trusted-main 没用到”。准确情况是：映射尚未实现；同时线上 `pull_request_target` 的 `feed-eval.yml` checkout 可信 main，`stage_eval_inputs()` 只导入经过检查的 prompt/model 数据，执行 main 的旧 `run_evaluation(root)` 与 107 例标签。最新运行 40860158711 只评了 105 例，因这两个身份不符而 incomplete，数值阈值本身通过。

PR 的变更是新增 45 例 Harness 选择及闸门评测路径，不是标题映射。即使后续进入可信执行路径，历史 45 例结果的召回率 **24/28=0.8571 < 0.90** 仍是另一独立问题；今天没有重跑该评测。原评测标签、阈值与发布暂停状态均未改动。
