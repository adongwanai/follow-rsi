# 2026-11-07 独立集成审查

审查时间：2026-11-07T00:14:53.917830+00:00。范围：当前未提交发布实现、真实远程 PR41/PR42/main/review workflow；未重复 8+3 篇候选内容审核。除主任务随后明确委派的两项最小修复及其测试外，未改 production 数据；未付费、未外部写入。以下远程状态是本次只读观察，执行合并前应刷新。

## 结论与已修复问题

1. **历史来源快照被后续抓取状态覆盖，已修复。** 原 `publish_day` 每次使用 `_source_snapshot(root,date)`。现有 11/02 manifest 保存 13 个来源，但当前 state 只能重建 1 个 arxiv-hydration，且它的 count/run_at 已改变；历史补刊会丢失原回执。现在已有刊期使用 `previous['sources']`，新刊仍使用当期来源快照。补刊的新来源绑定由候选/独立审核和 publication receipt 单独保存。新增回归覆盖 state 日期前进、同日来源数改变、无内容变化重跑，以及新增一篇后的来源和首次出版时间保持。
2. **CLI 简报拒绝前已写入决定，已修复。** 原 `publish --allow-status` 先 `apply_daily_review`，再检查 receipt；隔离 fixture 缺 receipt 时实际复现 canonical 已改变但 manifest 未生成。现在共用 `require_status_bulletin`，CLI 在没有合格论文或批准 lab 时于 apply 前预检双语状态、匹配日期的 receipt 与禁止替换论文刊期。新增 reject 行回归证明拒绝时 canonical、eval labels 和 manifest 都不被改变。

修改文件仅 `scripts/feed/digest.py`、`scripts/feed/cli.py`、`tests/feed/test_digest.py`、`tests/feed/test_cli.py`，均已向主任务释放所有权，没有 commit/push。首次修复相关 13 tests passed (6.64s)；最后一次同时覆盖两项修复的选择集 14 tests passed (4.85s)，`git diff --check` 通过。根任务应在最终代码、数据与渲染全部完成后跑完整套件；这里不是最终全套验证声明。

## 其余实现判断

- `allow_status=False` 仍保持无批准内容不生成刊期；显式开启后必须有已记录双语状态和日期匹配的合并回执。简报有独立 `kind=daily_status`、零论文 items 和 review counts，HTML、Markdown、首页和 Atom 都标为采集审核简报，不冒充批准新论文。
- `published_at` 已改为始终保留原刊首次时间。真正的内容变化设置 `updated_at`；无变化重跑沿用既有更新时间。已有简报的重跑保持原观察快照，后续 `daily-status` 文案变化不会悄悄改写它。
- `daily_editions` 在 JSON feed 中按刊期升序列出 daily/daily_status，包含 kind、paper_count、reviewed_on、published_at、updated_at 和双语摘要；它与 papers items 分开。Atom 每日一个稳定 ID，并区分 daily_status category。首页和日报索引仍按最新刊期选择，未出现把最早期误作最新期的回归。
- `date` 是真实刊期，`reviewed_on` 是真实审核日，`published_at` 是实际首次生成出版物时刻，`updated_at` 是补刊变化时刻。晚于刊期被发现的论文只能用实际 reviewed_on 校验，不修改 first_seen/HF 日期来过检查。实际远程发布还需部署证据，本地 published=true 不能单独证明。
- 全局模型质量按当前 owner 指令为告警：报告仍是 incomplete，45 例尝试、3 条 API/schema 错误，precision=25/26、recall=25/28，thresholds_passed=false。不得改为 pass。旧 publication-procedure 的全局阻断段落已过时，不能覆盖当前明确授权。
- 当前 `data/feed/daily-status.json` 只到 11/05，11/03、11/04 的历史说明还写质量阻断；真正出版前应更新状态说明并添加有真实来源依据的 11/06、11/07 记录。不能用 11/05 快照声称后两天已采集，也不能把历史 no-edition 文案不加解释地当作当前出版状态。

## 真实远程状态

| 对象 | 本次只读结果 |
|---|---|
| main | `6cb8262adfc844ddedcc149e345c22e042b71445`，2026-11-05T07:55:03Z，PR39 的 merge commit |
| 本地 HEAD | `c98ac0b337d188d03f2f92b400278a57368f2806`，另有当前未提交修改；不能当作已部署 main |
| PR41 | closed，merged=false；head=`53220090ceeb81d8564a66deb6e4fba32d577def`；只改 `review/backlog/2026-11-05.yaml`，没有新日期审核 YAML；reviews=[]。不能作为新 11/05 合并凭据 |
| PR42 | open，merged=false，head=`412fd7dcf99581ea8089d872ccdc7d6bb1da0391`，base=main；修改 11/06 daily YAML、对应 excluded 和 backlog。受识别的正式日期审核路径只有一个，分支 `feed/review-2026-11-06` 匹配 |
| PR42 决定 | 173 paper + 93 lab，266 条全部 defer；YAML SHA256=`93d0cbffffe60b90bc742d4c4e352340596bd6721ef394617701bfc427aa7bfd`。本次观察与当前本地 canonical 比较 0 missing、0 source_hash mismatch；后续 source 集成会改变这一结论，必须再验证 |
| PR42 status | 精确 head 的 `Follow RSI owner decisions=success`；run `42205416536`，workflow_dispatch，completed/success；执行的是 trusted main=`6cb8262...`。该状态证明审核结构/来源有效，不表示论文接受或出版 |
| workflow | feed-daily/feed-eval/feed-publish 均 disabled_manually；feed-review active。保持 bulk workflows 禁用符合当前策略 |

远程 main 的 `.github/workflows/feed-review.yml` 与本地相同，SHA256=`fa62ba7aae0b185ca58f6f70d89d9c99415f042d75180616d19647cc907fe888`；`scripts/feed/ci.py` 与本地相同，SHA256=`5abc447aad996f1c2f63d972bc157c6b3cdbc8caf1ba52ad1ac2ba7f3ff94793`。均从真实 Contents→immutable git blob 读取核对。

PR41/42 返回的非空 merge_commit_sha 在 merged=false 时不是已完成合并凭据，不能采用。`mergeable_state=unstable` 也不能替代精确 head 检查、required checks 或最终 merge 事实。

## 最小安全的真实日期审核与来源回执流程

1. **先确定 final canonical 和实现。** 实现/来源修复经过完整测试和生成文件检查后进入真实 main；review workflow 执行 trusted default-branch 代码，只从 PR 暂存日期审核 YAML，不会替 PR 暂存尚未合入 main 的 canonical 变更。因此需要依赖 canonical 的日期审核 PR 应在这些来源变更可用后重做准确 hash 检查。
2. **逐日真实审核 PR。** 每个分支严格为 `feed/review-YYYY-MM-DD`，只含一个受识别的正式 `review/daily/YYYY-MM-DD.yaml`（对应 excluded/backlog 不计作第二个正式日期）。保留已有决策和来源史，使用真实 reviewed_on，检查孤儿行与变化 source_hash。`validate_daily_review` 和 `require_publishable_day` 均通过；明确本日批准 items 或全 defer 状态简报。PR42 可刷新同一 branch；不能把它当作 11/05 或 11/07 的回执。PR41 已关闭未合并，无需再假定它阻塞，11/05 如有新内容应有新的真实日期 PR。
3. **真实 CI、合并和精确结果。** 用已有 review workflow 的 check 模式验证具体 PR（该流程不调用 paid model），要求目标 head 的 owner-decisions status 成功，并完成必要工程检查。用户持续授权允许主任务执行真实 merge；获取实际 merged=true、base=当前 default branch、same-repo head 和 merge_commit_sha。持续授权不是用户逐篇人工阅读的证据。
4. **本地只读 provenance 核验，不伪造 runner。** 用 `subprocess.run(['gh','api',...],check=True,...)` 获取实际 repo metadata、PR、分页 files/reviews。调用纯函数 `merged_review_requests({'pull_request': pr}, paths, repository)`，结果必须恰为本日；核对 base 为真实 default branch。调用 `human_owner_review(pr,reviews,repository)`：真实 owner User merger 或 exact final head 的有效 owner approval 才满足已有函数。读取 merge commit 下日期 YAML 的 Contents 元信息，再读取 immutable git blob 并 base64 decode，与本地最终 YAML **逐字节相同**。大 YAML 的 Contents 可能 encoding=none，直接 blob 路径避免空正文误判。再次执行 `validate_daily_review` 和 `require_publishable_day`。
5. **保存可复核 receipt 后再应用。** 保存真实 PR/head/merge/base/owner、review YAML SHA256、核验时间与所用源码/来源快照哈希。标准 `data/feed/review-provenance/DATE.json` 至少有 kind/date/path/github_pr/owner_login/merge_commit；精确核验回执另存或增加明确字段。`require_status_bulletin` 只检查本地 receipt 结构和日期，不联网证明其真实性；CLI 也不代替本步骤。不得凭旧同日 receipt 授权已改变的 YAML，更不能把 PR42 未合并的试算 merge SHA 写入。
6. **按既有授权本地生成。** `apply_daily_review(root,date,provenance={github_pr,owner_login,merge_commit})` 后调用 `publish_day(root,date,allow_status=True)`；有合格论文时仍生成论文期，零篇时生成有真实双语采集状态的简报。保持 feed-publish 禁用，不设置 GITHUB_ACTIONS/GITHUB_WORKSPACE 假扮 CI，不调用 ci.py 的外部写入包装。`publish_day` 的 now 不填历史时间。已有刊期保留原 published_at/sources；补刊新来源哈希单列回执。
7. **出版物 PR→真实 Pages 验证。** 最终 build、完整测试、schema/日期/数量/历史元数据检查全部通过后，生成出版物 PR，完成真实合并和 Pages。读取线上 dated page、daily index、home data、JSON feed、Atom，逐一对比期号、kind、items/summary、实际时间与产物哈希。只有真实部署/线上核对完成才报告每日已发布。所有 open PR 都要有已核验 merge 或有理由关闭；本报告未执行这些外部动作。

本地直接调用 `verify_merged_review` 或 `publication_pr` 会经 `default_branch/gh` 进入 require_ci；应使用上述真实只读 gh 数据与纯函数组合，不用假环境变量绕过。当前 `ci.publish` 也没有传 allow_status，且 workflow 保持禁用；本次授权路径依赖显式本地生成和后续出版物 PR，不承诺停用工作流会自动出简报。
