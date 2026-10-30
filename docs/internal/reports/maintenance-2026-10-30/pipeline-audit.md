# 2026-10-30 流水线与审核闸门核查

GitHub 状态核查时间：2026-10-30 08:10 北京时间（00:10 UTC）。本报告只读核查；没有重跑模型评测、修改标签或阈值、合并 PR、恢复发布。

## 结论

PR #3 的构建与测试通过；`evaluate` 红灯来自旧版 **107 例评测不完整（105/107）**。仓库另存的 **45 例 Harness 闸门召回率 24/28 = 0.8571，低于 0.90**，这是不同评测的独立质量问题。修好标题身份核对，只能修复第一项，不能宣称已解决第二项。

`feed-publish.yml` 当前仍为 `disabled_manually`，应继续保留。PR #3 没有正式 GitHub review，待审内容不能因构建通过而发布。

## 当前 PR 与 CI

- PR：https://github.com/adongwanai/follow-rsi/pull/3 ，OPEN / MERGEABLE / UNSTABLE。
- head：`e5666c58ab93f946103d5aef6e501580c15193ec`；base：`b9246ac880332688cabce1e46a0914c088089b19`。
- `build`（40860162945）、`validate`（40860162610）：SUCCESS。
- `evaluate`（40860158711）：FAILURE；失败步骤为 `Evaluate trusted code with proposed prompt inputs`。
- `validate-owner-decisions` 与 `queue`：SKIPPED，当前是修复分支，不是每日 review 分支。
- 当前仅 PR #3 打开；PR #5 已关闭并由 #3 接续；无打开的 issue。最新 Pages 部署 40843884548 成功，部署的是上述 main base。

实际失败运行：https://github.com/adongwanai/follow-rsi/actions/runs/40860158711 。其 `pull_request_target` 策略只把 PR 中检查过的 prompt/model 当作数据，执行可信 main。日志确认 checkout `main` 后 SHA 为 `b9246ac...`。因此当前 CI 执行旧 `ci.evaluate()` 与 `feed/eval/labeled.yaml` 的 107 例；PR 上新增的 45 例选择逻辑尚未成为可信执行代码。

最新 artifact：`pr3-evaluation-40860158711/report.json`，生成于 2026-10-29 10:46:36 UTC：

| 指标 | 本次结果 |
| --- | --- |
| 完整性 | incomplete，105/107 |
| 缺失元数据 / 标题身份不符 / API 或 schema 错误 | 0 / 2 / 0 |
| include precision | 1.0000 |
| include recall | 96/98 = 0.9796 |
| primary accuracy | 86/98 = 0.8776 |
| 旧数值阈值 | 全部通过；总闸门因不完整而失败 |
| 待 owner 复核的 curator seeds | 27 |

历史 0.9694 召回率不是本次运行结果，不应继续引用。

## 两个标题身份问题

独立 arXiv 元数据证据保存在 `build/ci-eval-pr3/identity-check.atom`。

1. `2609.08175`：v1 为 **Safe Harness Self-Evolution: A Theoretical Analysis of Feasibility and Limits**，v2 正式改名为 **A Theory of Reliable Self-Evolution for Agent Harnesses**。v1 发表于 2026-09-08，v2 更新于 2026-09-28。应保留原始书目信息并引入有来源的版本标题映射，不能放宽全局身份匹配。
2. `2607.07007`：curator 简称 **State-machine fuzz harness generation** 与正式题名 **Thinking More, Harnessing Better: State Machine Guided Harness Automatic Generation with Project Digestion and Workflow Decomposition** 不同。摘要明确研究 gray-box fuzzing harness，方法名 SynapseFlow，涉及 OSS-Fuzz-Gen / CKGFuzzer / PromeFuzz；其 `different_sense_of_harness` 负类判断有依据，不应为了 CI 更改标签。

可修方案是小范围、可核验的标题/版本别名映射，并保留精确 ID 核对。只在 PR 修改执行代码不会影响当前可信 main 的 CI 逻辑；需要按审核流程落地后再验证，不能绕过可信执行边界。

## 独立的 Harness 闸门

版本化的 `feed/eval/gate-report.json` 生成于 **2026-10-27 13:50:58 UTC**，今天未重跑，不能报告为今日评测。

| 范围 | 数量 | Precision | Recall |
| --- | ---: | ---: | ---: |
| 全部 | 45 | 24/25 = 0.9600 | 24/28 = 0.8571 |
| owner 复审子集 | 25 | 0.8750 | 0.8750 |
| 去掉 prompt 示例 | 35 | 0.9500 | 0.8261 |

元数据和 API/schema 完整，但 Harness recall 未达到 0.90（precision 要求 0.85）。四个假阴性为 TokenEconomizer（2610.22732）、HARBOR（2604.20938）、SkillOpt-Lite（2607.03451）、Living-Harness（2607.26598）；假阳性 CarryOn（2610.21453）按 owner 复审仍为 borderline/defer。

10 个案例已进入 prompt，20 个库内正例不是本轮全文审计，不能称盲测留出集。HARBOR 仍有 owner 指出的 scope 歧义，须保留问题，不能重标以提高分数。后续需要有证据支持的模型/提示词修正及真实复跑，单纯让 owner 按批准不能修复召回率。

## 今日调度与发布边界

截至 08:10 尚无 10 月 30 日 GitHub 运行，这符合当前 cron：daily 是 **UTC 02:23 / 北京 10:23**，review 是 **UTC 03:17 / 北京 11:17**。桌面 08:00 维护与 GitHub cron 是不同调度，不能把尚未到点报告成任务漏跑。

Oct 29 的另一失败 40853168538 是已关闭 PR #5 的 `pending review blocks publication; use defer to carry it forward`，是审核闸门按预期阻止 pending 条目，与本次 PR #3 的标题身份失败无关。

后续保持发布暂停；逐项保留 owner 决策、来源和证据。只有经 owner 审核的内容及适用质量闸门满足后，才推进日报发布。本次没有执行任何外部写入。
