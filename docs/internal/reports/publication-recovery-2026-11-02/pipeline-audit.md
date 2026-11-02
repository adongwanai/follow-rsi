# 本批人工批准与出版流程核对

核对日期：2026-11-02。基线代码为 `e96b067670dc83cd3d1b66b14179f311e10efc38`。本报告检查现有规则如何落实 owner 对当前批次的明确批准；不将此授权扩展为以后自动接受，不把范围建议全部改成 accept。

## 结论

现有可靠路径是：先形成逐 ID 的明确决定与内容，再由同仓 `feed/review-YYYY-MM-DD` PR 合并到默认分支，使用真实 GitHub owner 合并或对准确 head SHA 的批准记录，最后让 CI 从该 merge commit 核验 YAML 并生成 provenance。PR #3 是修复分支，不能充当日期审核 PR。仅在聊天中批准、手写 `owner_login`，或者直接运行本地 `cli publish`，都不会自动得到 GitHub 合并凭据。

模型召回率未达标是必须保留的评测告警，**按 owner 的原始要求，不是禁止本批人工审核后出版的全局硬条件**。`CODEX_PROMPT_FIX_AUDIT.md` §5.3 要求未达标时仍生成审核 PR，并在标题和首行展示 `[GATE BELOW THRESHOLD]` 与数值；§6 明确哪些逐条 accept 必须拒绝。不得降低阈值、改变负例、假称评测通过，也不应新增原要求没有的全局发布禁令。

## 已核实的条件与实际状态

| 条件 | 实现与当前事实 | 本次处理含义 |
| --- | --- | --- |
| GitHub 出版环境 | `scripts/feed/ci.py:49` 要求 GitHub Actions、正确 workspace 与 repository | 不伪造 CI 环境在本地运行远程提交器 |
| 审核 PR 的身份 | `ci.py:312`、`:341` 只接受同仓、已合并、默认分支及与分支对应的唯一日期/周审核单 | PR #3 的 `fix/reviewed-news-and-public-site` 不匹配；应另外落实日期审核 PR |
| owner 的真实批准 | `ci.py:328` 接受仓库 owner 的 `User` merge；或最后有效 owner review 是针对准确 head SHA 的 `APPROVED` | 在用户已授权的范围内，owner 身份执行的合并可以产生事实凭据；不能编造 merger、review 或 SHA |
| 批准的字节内容 | `ci.py:351` 比较当前审核 YAML 与真实 `merge_commit_sha:path` 的完整内容 | 合并后再改 YAML 必须重新审核；多个日期不能混进一个日期 PR |
| 逐条数据校验 | `review.py:470` 检查 ID、来源哈希、身份、方向、日期窗、撤稿与摘要数字 | `pending` 阻断；`defer` 可以保留且不发布；改过来源/摘要/推荐日后旧 hash 不再有效 |
| Harness 个体闸门 | `review.py:508` 要求 accept/backlog 在范围内；非 Harness gate 需要显式 `direction_override`；canonical `llm.label=exclude` 不能 accept | 人工 override 是已有能力，不能通过它绕过 exclude 的独立限制 |
| 模型质量评测 | `eval.py:22`、`:243` 阈值仍为 precision ≥ .85、recall ≥ .90；`ci.py:242` 负责警告 | `ci.publish` 不读取该 report 作为全局拒绝条件；这是当前设计，不能称为已通过的质量门槛 |
| Oct27 期撤回 | `digest.py:505`、`ci.py:483` 在修改 provenance/owner record 前拒绝恢复撤回日报 | 保留 `withdrawn-editions.json` 的 2026-10-27；不重新生成该日报 |
| 出版工作流 | 只读 GitHub API 核实 `feed-publish.yml` 为 `disabled_manually`，Pages 为 active | 即使批准并合并审核单，停用的 workflow 不会自动启动；一次恢复及后续自动化范围要明确区分 |
| 公开页面部署 | `pages.yml:32` 验证真实 URL、数据并 build，再上传 site；主分支 push 可触发 | 发布工作流停用不等于 main 上的 site 文件不会部署 |

只读远端快照：PR #3、#13（`feed/review-2026-11-01`）、#15（`feed/picks-2026-w45`）均未合并。main 的 legacy branch-protection API 返回 `Branch not protected`，active rules API 返回空列表。因此不能将 PR 中的红色评测视为由仓库强制执行的合并锁；仍须如实保留告警并遵循人工决定。

## 两份评测不能混用

- `feed/eval/gate-report.json` 是 2026-10-27 的 45/45 例报告，precision 24/25 = .96、recall 24/28 = .8571428571，`thresholds_passed=false`。
- `docs/internal/reports/maintenance-2026-10-30/harness-gate-eval/gate-report.json` 是后续完整报告：precision 24/26 = .9230769231、recall 24/28 = .8571428571，同样未通过。对应 input manifest 记录源提交 `3d7daa4802c4266dc1c03d039cc378f18bfd92a1`。
- 自动 PR 告警目前读取第一份，而最近维护报告说明第二份。若同步告警用的报告，应整体带上真实来源/输入回执，明确“历史评测，未重跑”；不能只把一个数字替换成较新值。此次没有付费重跑或宣称修复后的质量提升。

## 当前批准如何映射成决定

本轮冻结建议是 68 include、231 exclude、19 范围边界、9 原始来源阻塞。对这些建议的统一批准，应落实各自结论：合格条目进入 accept/backlog 或候选处理，排除条目记 reject/move，未知项继续 defer 并保留缺证原因；不能转成 327 个 accept。

当前 68 个 include 建议对应的 canonical 标签为 55 include、12 borderline、1 尚无模型分类，没有 canonical exclude。按 11/2 当前窗口，21 stale、45 backlog、2 in_window；58 条缺中英文摘要。摘要空白会通过现有数字校验，因此 `validate_daily_review` 成功不等于编辑内容完整，仍须补齐已核验的简述，不写入未审数字。

三个 11/2 HF 候选的具体差异：

| 记录 | 当前输入状态 | 现有合法路径 |
| --- | --- | --- |
| R²Orch `2610.22740` | HF 推荐日 11/2，但仍保留 `backfill_only=true`，当前结果是 backlog | 按补录处理；若依据真实本日发现回执纠正这个观察性标记，要留下前后状态与原因，不能为凑日报直接清除 |
| CEPO `2610.34722` | in_window，canonical borderline | 人工确认准确子方向，写显式 `direction_override` 和已核验摘要后可走日期审核 |
| RoboArchitect `2610.42141` | in_window，canonical 尚无 `llm` | 自动 queue 会略过，但可显式准备 owner review 行，`llm: {}` 保留未知，方向与摘要放 owner override；不需要伪造模型成功结果 |

已进行一次不写文件的内存校验：RoboArchitect 以原始 source hash、`llm: {}`、明确 `direction_override` 形成审核行，现有 `validate_daily_review` 可接受。这个实验只证明数据结构可行；示例空摘要也能通过，不能拿它作为可发布正文。

对 canonical exclude 的其他历史记录，现有校验确实拒绝 accept，即使填方向 override 也一样。它们应保留为 reject/待纠正；不能改掉历史模型输出冒充新模型结果。Oct27 专用 correction 有独立覆盖约束，不是任意历史 exclude 的通用转换器。

## 日期、补刊、补录和 Oct27

`window.py:21` 保留原发表日与版本日，取截至刊期的最新已观测 HF 推荐日为 `news_date`；来源首次抓取日不替代推荐日。`daily_metadata` 会排除已经在 daily 或 retrospective 出现的 ID。多次 HF 推荐的数组应完整保留，不能把一个作品拆成多个“新论文”身份。`source_hash` 包含 HF 日期，新增观察会使旧批准快照失效，需要重核。

现有缺口是同一个 `date` 同时承担刊期与审核日：`review.py:491` 要求 first_seen ≤ date；后一天才抓到真实旧榜条目时，不能诚实地补刊。最小兼容方案是给日期审核单增加可选 `reviewed_on`，默认 date，只让发现日与实际审核日比较，并显式要求 reviewed_on ≥ date。时间窗仍根据刊期 date 和真实来源日期计算；manifest、Markdown、HTML 区分两日期，reviewed_on > date 标“补刊 / Published later”。这不允许错日 HF 内容混进当日，也不伪造首次发现时间。本轮已实现该兼容方案：自动 queue 可以显式传入 reviewed_on，重跑同一期会保留既有值；其余日期窗逻辑仍以刊期 date 判断。未填写该字段的旧审核单保持原默认行为。

普通补录已有明确流程：在日期审核单用 `decision: backlog`，`apply_daily_review` 保存批准周，`approved_weekly_backlog` 重核来源后放进周报独立“补录”区。它不会变成日报；超过 30 天的 stale 不能借改 window_status 塞进 feed，应走证据库候选处理。周精选 picks 仅能来自该周已发布 daily 中的 accept，不能用尚未发布补录冒充精选。

Oct27 保持三层历史：原审核单和原 provenance、撤回原因、`kind: retrospective` 的 10/14–10/27 回顾。`corrections.py:16` 要求 correction 恰好覆盖原刊所有 accept/move，并保留 correction 文件 SHA；`:86` 检查回顾窗内真实 HF 推荐。`publish_corrected_recap` 是该既定纠错用途，不应改日期复用为普通补刊，更不能把新的 327 条塞进旧回顾。回顾与日报在 Atom 有不同 ID/category，旧 Oct27 日报链接继续显示撤回说明。

## 最小执行顺序与验证

1. 先把修复与待审来源数据进入可信默认分支，保持历史报告、论文原值、撤回记录。PR #3 的代码合并与各日期 owner review 的批准是两件事。
2. 根据当前用户授权生成具体逐 ID 决定，补齐真正可展示的中英文摘要。边界/原始来源阻塞继续记录事实，不通过全量 accept 消除待办。
3. 按真实 HF 刊期及其他来源日期分配，显式标补刊审核日；旧内容进入补录/候选，按时间从早到晚准备及验证各刊期，防止前面尚未出版导致后面跨窗吸入旧内容。
4. 使用现有 `feed/review-<date>` / `feed/picks-<week>` 分支规则，真实 owner 合并或 exact-head approval；核验合并到 main 的准确 YAML。CI 自动写 `review-provenance/<edition>.json` 与逐条 `github_pr / owner_login / merge_commit / reviewed_at`，不预填虚构 PR/SHA。
5. 出版前明确解决 workflow 手动停用状态。当前批次授权与未来常态自动接受不可混为一谈；本审计不启用 workflow、不合并、不发布。
6. 每日分支 `ci.publish` 不执行摘要生成模型。每周分支在存在 LLM key 时会把 client 传入 `digest_intro`，因此恢复无付费出版应使用已有 `client=None` 的统计模板路径；不能携带现存 secrets 悄悄触发付费调用。需要运行器显式不注入该 key，或在获授权的最小变更中令本次周报使用已有确定性模板。

已阅读对应测试：`test_ci.py:115` owner/exact-head；`:130` merge 字节一致；`:146` 未合并拒绝；`:326` 撤回先于 provenance 修改；`test_daily.py:144` 决定幂等与改版重审；`test_window.py:21` HF/原日期、`:78` 跨刊窗口、`:91` backlog；`test_digest.py:366` 日报/周报补录分离、`:442` 回顾与撤回保留。此审计未重跑全套测试。后续 reviewed_on 测试应覆盖默认仍拒绝后来发现、明确补刊可通过、反向日期拒绝、审核日晚不放宽 HF 刊期与 Oct27 撤回。

本报告只读核查了代码、数据和 GitHub 元数据；没有模型调用、没有远程写入，没有修改原始数据或审核决定。


## 补刊实现与离线验证结果

- `scripts/feed/review.py` 增加可选 `reviewed_on`，检查有效日期且不早于刊期；发现日检查使用实际审核日，保存决定时仍保留原 `date`、`week` 和真实 provenance。
- `scripts/feed/digest.py`、`scripts/feed/templates/daily.html` 在 manifest、双语 Markdown 和 HTML 分别显示刊期及实际审核日期。只有 `reviewed_on > date` 才标“补刊 / Published later”。公开 feed 已有 `review_date` 字段使用实际审核日，feed 的 `dates` 仍是刊期。
- 可选 `data/feed/daily-status.json` 的 `days` 会在日报页以“更新记录 / Update log”折叠展示，按日期正序说明空榜、无合格论文等状态；不制造空日报或 Atom 条目。该数据文件由主线程维护。
- 新增回归覆盖：未指定实际审核日的晚发现拒绝、合法补刊、反向与无效日期拒绝、错误 HF 刊期即使修改审核行也无法通过、默认/同日/补刊三种渲染、重建幂等、空日说明不增加公开条目。原跨日 owner-edit 保留测试的合成来源改为确实观察到两日榜单，避免以旧榜单为次日可发布样本。
- 实际命令：`.venv/bin/python -m pytest tests/feed/test_daily.py tests/feed/test_digest.py tests/feed/test_ci.py tests/feed/test_window.py -q`，结果 **97 passed in 22.51s**。首次调用系统 `python3` 因缺 `jsonschema` 在收集阶段失败，改用项目已有虚拟环境后通过；未安装或升级依赖。
- 本代理只修改上述实现、`tests/feed/test_daily.py` 和本报告；未修改 Oct27 撤回数据、论文原值或审核决定，未调用付费模型，未执行远程提交/合并/发布。全库构建及集成验证由主线程另行执行，本结果不代表已上线。
