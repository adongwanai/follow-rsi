# Follow RSI 运行与审核

Follow RSI 每天发现论文，owner 审核后发布「今日动态」；每周再从已经发布的条目中挑选重点。模型的 `include` 只是待审建议，不会直接进入公开 feed、周报或证据库。

- 仓库：[adongwanai/follow-rsi](https://github.com/adongwanai/follow-rsi)
- 网站：[follow-rsi](https://adongwanai.github.io/follow-rsi/)
- 订阅：[Atom](https://adongwanai.github.io/follow-rsi/feed/atom.xml) · [公开 JSON](https://adongwanai.github.io/follow-rsi/feed/latest.json) · [信源状态](https://adongwanai.github.io/follow-rsi/feed/status.json)
- 本地安装、构建与图片生成见 [开发说明](development.md)。

## 当前验证状态

2026-10-27 的真实 HF 回溯覆盖 14 个日历日，去重后有 275 篇；8 篇已在证据库，其余 267 篇经过 DeepSeek 判断：50 篇 `include`、27 篇 `borderline`、185 篇 `exclude`、5 篇 schema 错误。已生成 77 组中英文摘要，最终数字护栏失败为 0。这是发现与处理结果，不是 owner 已接受的篇数。

当前模型是 `deepseek-flash`。提示词回归的 include recall 为 95.9%、include precision 为 98.9%、主方向准确率为 90.8%；三个数值门槛均达到，但整轮结果仍是 **incomplete**：2 条论文身份待核对，1 条 schema 错误，27 条 curator seed 标签仍需 owner 复核。详见 [评测报告](../feed/eval/report.md) 和 [评测集说明](../feed/eval/README.md)。不能把这些离线评测指标填成本周线上审核准确率。

`LLM_API_KEY` 已配置到当前仓库的 GitHub Secrets。`S2_API_KEY` 尚未配置，Semantic Scholar 使用匿名调用；真实论文元数据请求已验证，完整引用与作者分页抓取仍待验证。已核实的来源与限制见 [信源验证记录](source-verification.md)。

第一阶段只发布 Harness 及明确关联 Harness 的横切研究。初轮 82 条待审经范围过滤后，44 条进入审核队列（其中 5 条分类错误需人工处理），其余 38 条完整双语记录进入月度归档；归档不等于人工接受。首期仍待 owner 审核，公开日报和 Atom 因而没有条目。

## 配置密钥与地址

仓库地址、Pages 地址、作者和订阅入口只在 [site.config.yaml](../site.config.yaml) 配置。模型的非敏感默认值在 [feed/model.yaml](../feed/model.yaml)；同名环境变量可覆盖默认值。

| 名称 | 用途与申请入口 |
| --- | --- |
| `LLM_API_KEY` | 当前使用 [DeepSeek API Keys](https://platform.deepseek.com/api_keys)。也可使用 [OpenAI API Keys](https://platform.openai.com/api-keys)，并同步设置 provider、model、base URL。API 账户需要可用额度。 |
| `S2_API_KEY` | 可选，在 [Semantic Scholar Academic Graph API](https://www.semanticscholar.org/product/api#api-key-form) 申请；无 key 时匿名调用，配置后通过 `x-api-key` 请求头发送。 |
| `GITHUB_TOKEN` | GitHub Actions 自动提供，无需另申请 PAT。工作流按任务声明内容、PR、issue、Actions 和 Pages 权限。 |
| `GH_TOKEN` | 工作流把默认 `GITHUB_TOKEN` 传给 `gh`；本地只读验证可使用自己的 GitHub 登录或令牌。 |

在仓库 [Settings → Secrets and variables → Actions](https://github.com/adongwanai/follow-rsi/settings/secrets/actions) 新建 repository secrets。`LLM_PROVIDER`、`LLM_MODEL`、`LLM_BASE_URL` 可放在同页的 Variables 中；留空时使用版本化的 `feed/model.yaml`。在 Settings → Actions → General 允许 GitHub Actions 创建 PR，并按仓库规则允许工作流写回状态。在 [Pages 设置](https://github.com/adongwanai/follow-rsi/settings/pages) 选择 **GitHub Actions**。

本地复制 `.env.example` 为 `.env.local`，用编辑器填入密钥。该文件已被 Git 忽略；CLI 只读取显式指定的文件，不执行其中的 shell 文本：

```sh
cp .env.example .env.local
python -m scripts.feed.cli --env-file .env.local run --stage all --until summarize --sources hf-daily --days 14 --workers 4
```

`--env-file` 放在子命令之前。配置文件支持示例中的键值与注释，不需要 `source` 文件；密钥不得写入 YAML、截图、日志或 PR。默认模型通过官方 OpenAI SDK 调用 DeepSeek，使用 **JSON-object 输出加本地精确 schema 校验**，不是服务端 strict JSON-schema。调用温度为 0，解析或 schema 失败纠正重试一次，仍失败进入待审错误队列。

## 日常发现与恢复

运行全套每日发现并停在摘要阶段：

```sh
python -m scripts.feed.cli --env-file .env.local run --stage all --until summarize --schedule daily --days 3
```

`--sources hf-daily` 限定信源；`--days 14` 对 HF 会逐日请求 14 个日期，不是只读取今天的列表。HF 使用原始论文标题和 `paper.summary`，不用 `ai_summary`。arXiv 请求共享至少 3 秒的间隔，只保存元数据和摘要。

步骤为 `fetch → normalize → dedupe → judge → summarize → queue → publish`。可用 `run --stage judge` 或 `run --stage summarize` 恢复单步；结果按论文身份、版本、渲染后提示词哈希和模型缓存。`data/feed/items.jsonl` 是追加日志，读取时同一 ID 的最后一条记录生效；同样的数据不重复追加。源码、摘要或自动判断变化会使旧审核失效，必须重新审核。

本地命令不创建 GitHub PR。需要外部 issue 提醒的抓取使用 `--issues`，并需要 GitHub 凭据与 `GITHUB_REPOSITORY`；正常自动化由工作流传入这些值。

## 每日 owner 审核

每天 UTC 03:17 生成 `review/daily/<日期>.yaml`，对应 PR 标题为 `Review: Follow RSI <日期>`。建议每天预留 5–10 分钟；正文核实和积压另计。

1. 打开当天 `feed/review-<日期>` PR，先看 `borderline`、schema 错误、数字护栏失败与低置信度条目。`exclude` 单列在同目录的 `<日期>.excluded.yaml`，供抽查漏判。
2. 将每条 `decision` 改为下表之一。审核的是身份、相关性、分类与摘要；摘要证据速判仍标为「自动判断，未核实」。
3. 运行审核检查，确认所有 `pending` 已处理。owner 合并 PR 后才触发正式发布；模型或机器人不会替 owner 作决定。

| 决定 | 效果 |
| --- | --- |
| `accept` | 接受原分类与经检查的摘要，进入当日发布。 |
| `reject` | 拒绝，不发布。 |
| `move` | 接受并改分类，必须填写 `direction_override`，例如 `harness/improver`。 |
| `defer` | 今天不发布，次日重新变为待审，保留备注与已有修改。 |
| `pending` | 尚未作决定，阻止审核检查与发布。 |

本地可在审核分支上使用辅助界面；以下日期只是命令示例：

```sh
python -m scripts.feed.cli queue --date 2026-10-27
python -m scripts.feed.cli review --date 2026-10-27
python -m scripts.feed.cli check-review --date 2026-10-27
```

交互键为 `a/r/m/s`，分别表示接受、拒绝、移动方向、顺延。`summary_override` 可填写 `{summary_zh: "…", summary_en: "…"}`；两种语言都需检查，英文数字须与中文一致，所有数字必须来自原始标题或摘要。`id`、标题、arXiv ID、`source_hash` 等来源字段不要手改；来源更新后重新生成审核单。

每个证据速判的 `yes` 都必须带原始摘要中的有效短引文，缺少支持降为 `unknown`，不会生成 `no`。最终数字检查重试后仍不通过的条目清空两种摘要；可以留到稍后，或由 owner 核实后只发布标题与链接。

未合并的旧审核 PR 会把条目和 owner 修改带到新 PR；先建立替代 PR，再关闭旧 PR。没有合并就不发布，连续 3 个日历日未合并会更新唯一的 `Review stalled: Follow RSI` issue；积压超过 60 条时在其中列出数量。恢复后关闭提醒。

正式发布还会校验：PR 来自本仓库、合入默认分支、owner 亲自合并或批准准确的 head revision，以及当前审核 YAML 与已批准的合并内容完全一致。手动重跑工作流不会绕过这个检查。

## 每周精选与仓库候选

每周日 UTC 23:41 生成 `review/<ISO 周>.yaml` 和 `Weekly picks: Follow RSI <周>` PR。这里只选本周已经通过每日审核并发布、且决定为 `accept` 的论文，不重新给未审论文开口子。每周可安排约 30 分钟做整理与漏检抽查。

```sh
python -m scripts.feed.cli picks --week 2026-W44
python -m scripts.feed.cli check-review --week 2026-W44
```

owner 填写 0–3 条 `picks`，每条包含 `arxiv_id`、`why_zh`、`why_en`，可补 `editor_note_zh` 和 `editor_note_en`。推荐理由和点评由 owner 手写；不填精选就省略精选一节。周报仅汇总已发布每日快照；通过审核后生成中英文 Markdown、网页、趋势图、1080×1350 分享图，以及标签为 `follow-rsi-<ISO 周>` 的一个 GitHub Release。重跑更新同一期 Release，日报不建 Release。

日报发布后，审核通过的 Harness 论文按 `promote_to_repo: auto` 生成候选 PR；`false` 可关闭。候选使用 `status: candidate`、`section: candidates`、`needs_reading: true`，**全部证据字段仍为 `unknown`**。摘要速判只放在 PR 描述供参考，不能升级成正文证据审计。即使显式填写 `true`，非 Harness 论文也不会进入 Harness 证据库。

## 自动化入口

所有日期与 ISO 周按 UTC 计算。工作流共用状态写入 concurrency 组，避免同时修改队列与日志。

| 工作流 | UTC 时间 / 触发 | 结果 |
| --- | --- | --- |
| `feed-daily.yml` | 每天 02:23 | 抓取、去重、判断、摘要与健康状态，不发布条目。 |
| `feed-review.yml` | 每天 03:17 | 每日待审 PR、旧队列顺延、审核校验。 |
| `feed-weekly.yml` | 周日 21:07 | 已启用的每周信源、版本与撤稿检查、召回对照。 |
| `feed-picks.yml` | 周日 23:41 | 每周 owner 精选 PR。 |
| `feed-publish.yml` | owner 审核 PR 合并 | 发布对应日报或周报，显式调度 Pages。 |
| `feed-eval.yml` | 提示词 / 模型 PR 或手动 | 回归评测与报告；无密钥显示 `eval skipped`。 |

在 GitHub Actions 页选择 **Run workflow** 可重跑。每日发现支持 `days`；每日审核用 `mode=queue` 和可选 `date`，或 `mode=check` 加 `pr_number`；发布只能在 `date`、`week`、`pr_number` 中选一个。bot 创建的 PR 会显式触发检查，公共文件提交后显式触发 `pages.yml`，避免默认 `GITHUB_TOKEN` 不继续触发工作流的问题。

CI 内部命令如下，仅供维护工作流时对照；`scripts.feed.ci` 要求真实 Actions runner 与匹配的 workspace，不能作为本地发布捷径：

```text
python -m scripts.feed.ci queue-daily-pr [--date YYYY-MM-DD]
python -m scripts.feed.ci queue-picks-pr [--week YYYY-WWW]
python -m scripts.feed.ci check-pr --pr-number N
python -m scripts.feed.ci publish [--date YYYY-MM-DD | --week YYYY-WWW | --pr-number N]
```

## 信源、排序与运行状态

信源登记表 [feed/sources.yaml](../feed/sources.yaml) 使用顶层 `publish_scope`、`recall`、`ranking` 和 `sources`；游标与运行状态只写入 `data/feed/state.json`。新增来源时填写唯一 ID、kind、schedule、params、notes，先验证真实接口能返回正确格式，再设 `enabled: true`。停用只改为 `false` 并说明原因，保留历史记录。

`publish_scope.primary: [harness]` 允许 Harness 主方向；横切方向必须同时含 `secondary: [harness]` 才能发布。其他主方向不会因带有 Harness 次标签而自动进入范围。范围外的 `include` 和 `borderline` 仍分类、生成双语摘要，保存在 `data/feed/archive/<YYYY-MM>.jsonl`，不进审核单；发布时再次校验范围。分类错误可进入待审，但修正为范围内方向后才能接受。实验室动态同样需要明确 Harness 方向。

当前启用 arXiv 三组检索、HF、Sakana、METR、OpenAI、DeepMind、Weco 官方 feed、GitHub releases 和 S2。Anthropic、Prime Intellect 未找到经过核实的官方 RSS，保持停用。GitHub release 空列表可以是正常响应。博客带 arXiv 链接时会补取论文元数据；无论文链接的保留为独立实验室动态。

S2 有 key 时请求至少间隔 1.1 秒，无 key 时至少 3.1 秒；HTTP 429 按指数退避，最多重试 5 次，其他错误显式报告。`state.json` 记录每路来源的 `auth_mode` 与 `min_interval_seconds`。匿名元数据请求已实际经历 5 次 429 后成功；这不代表完整分页抓取已验收。

方向内排序权重为 `seed_hits: 3`、`author_tracked: 2`、`hf_upvotes: 0.1`、`code_released: 1`，owner 精选置顶。这些是可解释的发现和热度信号，不是证据评分。S2 按论文 `publicationDate` 检查近 30 天，不能据此知道引用关系是哪天新增的；最后列出的作者只是追踪启发式，不视为已验证的通讯作者。

每个来源连续 3 次为空、失败或降级会触发单个 `Source down: <id>` issue，恢复后关闭。arXiv API 持续失败会使用分类 RSS 做关键词过滤，并记录 `degraded`；不能把降级当作完整 API 覆盖。状态页和徽章显示最近成功抓取的时间，超过 48 小时变红；它表示抓取是否新鲜，不表示当天已经人工审核或发布。

`data/feed/metrics.json` 分周记录发现、人工接受、判断准确率、时效、信源产出、数字护栏首次失败率和 `archive_by_direction`；空样本显示未知，不伪造百分比。时效应结合当期发布快照阅读，不能用最近抓取时间代替。每周 `recall` 只对照 Harness 参考条目：zgcagi/Harness-RSI 全部条目，以及 Prism-Shadow/awesome-rsi 明确标为 `artifact: Harness code` 的条目。参考分类缺失时显式报告失败，不改为全表召回。输出为 `review/<周>.misses.yaml`；关键词只给建议，不自动修改来源配置。

```sh
python -m scripts.feed.cli health
python -m scripts.feed.cli recall --week 2026-W44
```

`health` 重算本地状态与指标；`recall` 会联网读取参考清单。排查未更新时依次看最后一次 Actions 结果、来源错误、待审 PR 和发布工作流。公开站点只来自审核通过的版本；修复抓取故障不会自动批准积压条目。
