# Follow RSI 运行与审核

Follow RSI 每天发现论文，owner 审核后发布「今日动态」；每周再从已发布的条目中挑选重点，并单列经过批准的历史补录。模型的 `include` 和 Harness 闸门结论都是待审建议，不会自动批准出版或正文证据。

- 仓库：[adongwanai/follow-rsi](https://github.com/adongwanai/follow-rsi)
- 网站：[follow-rsi](https://adongwanai.github.io/follow-rsi/)
- 订阅：[Atom](https://adongwanai.github.io/follow-rsi/feed/atom.xml) · [公开 JSON](https://adongwanai.github.io/follow-rsi/feed/latest.json) · [信源状态](https://adongwanai.github.io/follow-rsi/feed/status.json)
- 本地安装、构建与浏览器检查见 [开发说明](development.md)。

## 本轮修复状态（2026-10-27）

旧 `2026-10-27` 日报已撤回，撤回记录保存在 [withdrawn-editions.json](../data/feed/withdrawn-editions.json)。它混入历史回填，且存在 Harness 分类错误；普通发布命令禁止重新发布该日期。本轮依据 [人工复审清单](../review/corrections/2026-10-27.yaml) 生成了独立的 [创刊回顾](../site/recaps/2026-10-14--2026-10-27.html)：**16 条专题论文，其中 15 篇方法、1 篇 Harness 理论**。这是覆盖 10 月 14–27 日 HF 推荐的本地待审版本，不是 10 月 27 日的新增论文，也不表示修复已部署。

当前 `feed-publish.yml` 工作流在 GitHub 端处于禁用状态。须由 owner 审阅并合并本轮修复、确认发布内容后再启用；仓库里的触发器定义仍保留，合并代码不会自动恢复已禁用的工作流。下面的正式发布步骤以工作流重新启用为前提。

最新 [Harness 闸门评测](../feed/eval/gate-report.md) 完成了 45 / 45 个样本，precision **0.9600**、recall **0.8571**，无 API/schema 错误。要求分别为 ≥ 0.85、≥ 0.90，因此 **recall 未过线，整体门槛未通过**。审核 PR 继续生成，但标题带 `[GATE BELOW THRESHOLD]`，正文先列指标与待审统计，人工审核仍保留。该集合包含 25 条人工复审样本及 20 条预选证据库正例，其中 10 条作为提示词校准例可见；它不是盲测分数，也不是线上出版准确率。

本轮 [信源运行快照](../site/feed/status.json) 实际运行 **12 路，10 路成功**。成功来源为 arXiv 三组检索、HF、五路官方 RSS 和 GitHub releases；S2 的 `s2-citations`、`s2-authors` 两路均因 HTTP 429 失败。Weco 与 GitHub 的成功空响应不等于发现了新条目。旧 [report.md](../feed/eval/report.md) 与 `*-initial.*` 文件属于历史评测，不用来说明当前闸门已通过。

## 配置密钥与地址

仓库地址、Pages 地址、作者与订阅入口只在 [site.config.yaml](../site.config.yaml) 配置。公开模型配置在 [feed/model.yaml](../feed/model.yaml)：基础模型和 `classify` 为 `deepseek-flash`，`harness_gate` 独立使用 `deepseek-v4-pro`。如把闸门改回 flash，代码要求至少两次采样并检查一致性。

| 名称 | 用途 |
| --- | --- |
| `LLM_API_KEY` | LLM 凭据；当前 provider 为 DeepSeek，可在 [DeepSeek API Keys](https://platform.deepseek.com/api_keys) 申请。改 provider 时同步修改模型与 base URL。 |
| `S2_API_KEY` | 可选的 [Semantic Scholar API key](https://www.semanticscholar.org/product/api#api-key-form)；无 key 时匿名调用，更容易触发限流。 |
| `GITHUB_TOKEN` | GitHub Actions 自动提供；权限按工作流声明。 |
| `GH_TOKEN` | 工作流传给 `gh` 的令牌；本地 GitHub 操作可使用已登录的 `gh`。 |

在仓库 [Actions Secrets](https://github.com/adongwanai/follow-rsi/settings/secrets/actions) 中配置密钥。`LLM_PROVIDER`、`LLM_MODEL`、`LLM_BASE_URL` 可放在 Variables，覆盖基础默认值；阶段模型由 `feed/model.yaml` 的 `stages` 配置。允许 Actions 创建 PR，并在 [Pages 设置](https://github.com/adongwanai/follow-rsi/settings/pages) 选择 **GitHub Actions**。

本地复制 `.env.example` 为被 Git 忽略的 `.env.local`，用编辑器填入密钥：

```sh
cp .env.example .env.local
python -m scripts.feed.cli --env-file .env.local run --stage all --until summarize --schedule daily --days 2
```

`--env-file` 必须放在子命令之前。CLI 只解析显式指定的键值文件，不执行 shell 文本；无需 `source`。密钥不能写入 YAML、截图、日志或 PR。默认通过官方 OpenAI SDK 调用 DeepSeek，使用 JSON-object 输出加本地 schema 和来源检查；失败会记录并进入待审处理。

## 日期口径与出版窗口

日期按 UTC 计算。抓取时间、原始发表时间与 HF 推荐时间各有用途，不能互相替代：

| 字段 | 含义 |
| --- | --- |
| `published` / `announced` | 原始论文发表时间及对应 UTC 日期；`announced_source` 记录来源。HF 使用论文的 `paper.publishedAt`，只有缺失时才回退到 `hf_submitted_at` 并标明来源。 |
| `updated` | 来源提供的版本更新时间，不能用本次抓取时间填充。 |
| `hf_daily_dates` | 实际抓取的 HF 每日推荐列表中观察到该论文的日期，保留多次观测。 |
| `news_date` | 优先取不晚于本期 D 日的最近一次已核实 HF 推荐日；没有 HF 列表观测时，取来源 `updated`，再取 `announced`。未来榜单日期不会提前收录。 |
| `first_seen` | 本仓库第一次发现该条目的时间，不作为 HF 推荐日或论文发表日。 |

日报使用 `上一期结束日 < news_date ≤ D`；没有前一期时下界为 `D−2`，创刊回顾的 `end` 也参与下界计算。原始 `announced` 用于论文日期展示与排序，**不会覆盖 HF 推荐日**。已经出现在日报或回顾中的 ID 标为 `already_published`，不再次作为日报新增。

窗口外且未超过 30 天的论文标为 `backlog`，须显式批准后进入周报「补录」。相对 `news_date` 超过 30 天的条目标为 `stale`，进入 `review/backlog/<日期>.yaml` 供证据库候选审阅，不进入日报、周报或公开 feed。这意味着一篇较早发表、近期才被 HF 推荐的论文仍可能在窗内；页面分别显示原始发表日和推荐日。

`--days` 只控制抓取范围，CLI 与每日 workflow 默认都是 **2**。大于 3 天是历史回填：所有未发布条目（包括已有 ID）会标为 `backfill_only`，不能进入日报，已经在日报、回顾或周报补录发布的条目保留原状态。抓取批次保存 `lookback_days` 和 `backfill_only`，分阶段恢复运行也不会丢失回填标记；工作流同时在 job summary 提示。例：

```sh
python -m scripts.feed.cli --env-file .env.local run --stage all --until summarize --schedule daily --days 14
```

这会逐日请求 HF 的 14 天列表，并产生待审历史资料，不会把 14 天的论文算作今天新增。

## 发现、存储与 Harness 闸门

流程为 `fetch → normalize → dedupe → judge → summarize → queue → publish`，其中 `judge` 包含相关性判断、分类和 Harness 闸门。`--sources hf-daily` 可限定来源；`run --stage judge`、`run --stage summarize` 可恢复单阶段。已收录证据库的条目照常参与窗口与排序，其分类、摘要和证据直接取人工目录，不调用 LLM。

HF 使用论文原始标题与 `paper.summary`，不用 `ai_summary`。arXiv 请求共享至少 3 秒间隔。`data/feed/items.jsonl` 采用 **按 ID upsert 的完整快照**：同一 ID 更新原记录，重复运行内容不变则不重写；保存时会把旧追加格式压缩为每个 ID 的最新一行。来源、摘要或判断变化使旧 `source_hash` 失效，须重新审核。原始响应在 `data/feed/raw/`，来源游标与运行状态在 `data/feed/state.json`。

Harness 闸门检查三个条件：被修改的是模型周围的可复用程序，修改由执行或评估反馈驱动，接受的版本跨任务或轮次保留。只训练权重、改变训练环境或奖励、改进外部任务产物、只积累记忆条目，都不能据此算 Harness。完整口径见 [taxonomy](../feed/taxonomy.yaml)、[闸门提示词](../feed/prompts/harness_gate.md) 与 [导读](../site/guide.html)。

`publish_scope` 限定 Harness 及明确关联 Harness 的横切研究；评测与理论还需核实 `harness_specific`。范围外的相关论文保存到 `data/feed/archive/<YYYY-MM>.jsonl`，不自动进入专题出版。明确的人工 `direction_override` 仍须通过分类、窗口和范围检查，不能绕过时间窗。

本地命令不创建 GitHub PR。需要 issue 提醒时使用 `--issues`，并提供 GitHub 凭据与 `GITHUB_REPOSITORY`；正常自动化由工作流传入。

## 每日 owner 审核

每天 UTC 03:17 生成 `review/daily/<日期>.yaml` 与审核 PR。审核单先列 `announced`、`news_date`、`window_status`、`in_repo` 和 `gate`；PR 先列窗内、backlog、闸门通过、borderline、已入库的数量。

1. 先核对日期与「改了什么」，再看低置信度、borderline、错误及数字护栏。`<日期>.excluded.yaml` 供抽查漏判。
2. 新条目默认 **`defer`**。只对决定采用的条目填写明确决定；摘要审核与正文证据核验分别处理。
3. 运行检查后，由 owner 审阅并合并 PR。默认顺延不是默认批准；显式 `pending` 仍会阻止发布。

| 决定 | 效果 |
| --- | --- |
| `accept` | 接受窗内条目；必须满足 `window_status: in_window` 及闸门/人工方向修正要求。 |
| `reject` | 拒绝，不发布。 |
| `move` | 必填 `direction_override`；范围内且窗内的条目可出版，移到范围外的不会进专题日报。 |
| `defer` | 今天不发布，保留备注和修改，继续排队。 |
| `backlog` | 显式批准 `window_status: backlog` 的历史条目，只进当周补录。 |
| `pending` | 未决，阻止审核检查和发布。 |

下面日期仅为命令示例，已撤回的 `2026-10-27` 不能用普通发布流程恢复：

```sh
python -m scripts.feed.cli queue --date 2026-10-28
python -m scripts.feed.cli review --date 2026-10-28
python -m scripts.feed.cli check-review --date 2026-10-28
```

交互键 `a/r/m/s` 分别为接受、拒绝、移动、顺延；`backlog` 在审核 YAML 中显式填写。`summary_override` 可填写 `{summary_zh: "…", summary_en: "…"}`，数字必须来自原始标题或摘要，双语数字须一致。不要手改 ID、标题、arXiv ID 或 `source_hash`；来源更新后重新生成审核单。

摘要证据的肯定结论需要有效原文短引文，否则降为 `unknown`。代码字段可引用经过核实的仓库链接：发现链接本身不等于核实开源，需能确认仓库含非 README 文件才记 `yes`，页面称「有代码链接」。已入库论文显示人工证据来源。以上都不替代正文逐项审计。

旧的未合并审核 PR 会把条目及 owner 修改带入新 PR，建立替代 PR 后再关闭旧 PR。连续 3 天未合并会更新 `Review stalled: Follow RSI` issue，积压超过 60 条时提示数量，恢复后关闭。正式发布还核对本仓库 PR、默认分支、owner 对准确 head revision 的合并或批准，以及审核 YAML 与批准内容一致；手动重跑不能绕过这些检查。

## 每周精选、补录与候选

周日 UTC 23:41 生成 `review/<ISO 周>.yaml` 和精选 PR。owner 从本周已发布、决定为 `accept` 的论文中选 0–3 条 `picks`，保持填写顺序；理由为 `why_zh`、`why_en`，可补双语 `editor_note`。不填精选时省略该节。

```sh
python -m scripts.feed.cli picks --week 2026-W44
python -m scripts.feed.cli check-review --week 2026-W44
```

周报普通部分汇总已发布每日快照；明确批准的 `backlog` 单列为「补录」，显示原始发表日并注明不是本周新论文。补录不能混入日报，也不成为每日精选候选。周报生成中英文 Markdown、网页、趋势图和可选分享图；正式 CI 发布使用 `follow-rsi-<ISO 周>` 标签维护一个 GitHub Release，重跑更新同一期，日报不建 Release。

日报发布后，`promote_to_repo: auto` 可为通过审核的 Harness 论文生成证据库候选 PR，`false` 关闭。候选为 `status: candidate`、`section: candidates`、`needs_reading: true`，证据字段全部保持 `unknown`。摘要速判仅供参考，非 Harness 条目不会因此进入 Harness 证据库。

## 自动化入口与运行状态

工作流共用状态写入 concurrency 组，避免同时改写队列与数据。以下是配置中的触发时间；发布工作流当前禁用，见本页开头。

| 工作流 | UTC 时间 / 触发 | 结果 |
| --- | --- | --- |
| `feed-daily.yml` | 每天 02:23 | 运行所有启用的每日信源，判断、摘要与健康状态；不发布条目。 |
| `feed-review.yml` | 每天 03:17 | 待审 PR、旧队列顺延、审核校验与闸门指标提醒。 |
| `feed-weekly.yml` | 周日 21:07 | arXiv 版本与撤稿检查、参考清单召回对照。 |
| `feed-picks.yml` | 周日 23:41 | 每周 owner 精选 PR。 |
| `feed-publish.yml` | owner 审核 PR 合并或受检的手动重跑 | 启用后发布对应日报/周报，调度 Pages；目前禁用。 |
| `feed-eval.yml` | 提示词/模型 PR 或手动 | 实时评测；没有密钥时明确报告跳过。 |

Actions 的手动入口中，每日审核用 `mode=queue` 与可选 `date`，或 `mode=check` 与 `pr_number`；发布只选 `date`、`week`、`pr_number` 之一。bot 创建 PR 后显式触发检查，公共文件提交后显式调度 `pages.yml`。`scripts.feed.ci` 要求真实 Actions runner 与匹配 workspace，不能作为本地发布捷径：

```text
python -m scripts.feed.ci queue-daily-pr [--date YYYY-MM-DD]
python -m scripts.feed.ci queue-picks-pr [--week YYYY-WWW]
python -m scripts.feed.ci check-pr --pr-number N
python -m scripts.feed.ci publish [--date YYYY-MM-DD | --week YYYY-WWW | --pr-number N]
```

[信源登记表](../feed/sources.yaml) 管启用状态与参数，`state.json` 记录每路实际运行结果，成功、空响应和失败都留记录。当前 12 路已启用来源均按每日运行；Anthropic、Prime Intellect 的未核实 RSS 仍停用。S2 有 key 时至少间隔 1.1 秒，匿名至少 3.1 秒；429 按退避重试并最终显式记录失败。一次元数据请求成功不等于两路完整分页抓取成功。

已启用来源连续 2 天没有运行记录会触发缺跑提醒；连续 3 次空、失败或降级会触发来源故障提醒。arXiv API 失败后的 RSS 降级会标明 `degraded`，不能视为完整 API 覆盖。日报页脚展示本期实际来源、条数和审核/发布时间；[status.json](../site/feed/status.json) 的 `last_fetch` 展示最近整轮结果，更新徽章只表示抓取新鲜度。

日报先按 taxonomy 子方向分组，组内已入库在前，其余按 `announced` 从新到旧、再按 rank。周报先保持 owner 精选顺序，其余最新在前。公开 JSON 的 items/weeks/dates、Atom 与历期索引均最新在前。rank 是发现信号，不是证据评分。

`data/feed/metrics.json` 记录每周运行与出版指标，空样本不伪造比例。`recall` 对照 Harness 参考清单，输出 `review/<周>.misses.yaml`，不会自动改来源或批准论文：

```sh
python -m scripts.feed.cli health
python -m scripts.feed.cli recall --week 2026-W44
```

排查未更新时依次看 Actions 结果、实际来源错误、待审 PR 和发布工作流状态。抓取修复、评测完成和本地渲染都不能替代 owner 对公开版本的审阅与合并。
