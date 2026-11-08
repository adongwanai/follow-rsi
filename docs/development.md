# 开发与构建

中文首页是 [README.md](../README.md)，英文是 [README_en.md](../README_en.md)；[README_zh.md](../README_zh.md) 只保留一行中文首页跳转。本文说明源码和生成物如何维护；发现、日期窗口、密钥和 owner 审核见 [运行与审核](feed-setup.md)。

## 安装与本地预览

使用 Python 3.11，与 CI 一致。在仓库根目录执行：

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/validate.py
python scripts/build.py
python -m pytest -q
python -m http.server 8000 --directory site
```

浏览器打开 `http://localhost:8000/`。网站是静态 HTML、CSS、JavaScript，没有 Node 构建步骤；`site/data.js` 支持直接打开本地主页，HTTP 预览便于检查日报、周报和相对链接。

普通构建与单元测试不需要 API key，也不请求论文来源；安装依赖需要访问包仓库。浏览器和图片步骤另装 Playwright。真实信源抓取与 LLM 回归是独立联网操作，不能把离线测试通过写成网络路径全部验证通过。

## 源文件与生成物

| 文件 | 维护方式 |
| --- | --- |
| `data/papers.yaml` | 证据库唯一数据源；维护 `scope`、分类、摘要和证据，数字与证据变更附正文页码或表号。 |
| `data/routes.yaml` | 阅读顺序与可选的 `why` 说明；论文 ID 必须存在。 |
| `site.config.yaml` | 仓库、Pages、作者、订阅与 Discussions 配置。 |
| `README.md`、`README_en.md` | 手写区可编辑；构建只替换成对的 AUTO 区块，保留其他作者文字。 |
| `README_zh.md` | 一行跳转入口，不维护第二份中文正文或 AUTO 区块。 |
| `PAPERS.md` | 由构建生成的完整清单，按 scope 分组；README 只保留必读入口。 |
| `notes/<id>.md` | 手写精读、视频和想法。文件有内容时才拼入论文卡片，不创建空小节。 |
| `papers/<id>.md` | 由数据、notes 和路线生成标题、证据卡、非空笔记和相关论文，不直接修改生成区。 |
| `directions/guide.md`、`directions/open-problems.md`、`site/guide.html` | 有内容的导读与研究空白；双语说明保持一致。未完成的方向页不从公共导航链接。 |
| `site/index.html`、`site/app.js`、`site/style.css` | 主站落地页、证据库、路线、方向图与研究空白交互。 |
| `site/partials/header.html`、`site/header.css`、`site/header.js` | 共用顶栏、语言/主题持久化与导航；通过 `scripts/site_header.py` 渲染。 |
| `scripts/feed/templates/`、`site/weekly/` | 日报、周报、回顾、订阅源模板及出版页样式。 |
| `feed/sources.yaml`、`feed/taxonomy.yaml`、`feed/model.yaml`、`feed/prompts/` | 来源、分类、模型与提示词。 |
| `data/feed/`、`review/`、`daily/`、`digests/`、`site/recaps/` | 运行快照、owner 决定和出版物，按审核流程维护。 |

`scripts/build.py` 校验数据后更新 README AUTO 区块、`PAPERS.md`、论文卡片、JSON、徽章、社交落地页和分类图；它不改 `data/papers.yaml`，不调用 LLM，不把未知证据变成肯定或否定。统计写入 `site/stats.json`，不再维护根目录同名副本。`scope` 将方法、Harness 专项评测/理论、背景与通用 RSI 分开计数，不能把目录总量称为方法数量。

保留 README 的 `<!-- AUTO:...:START -->` / `<!-- AUTO:...:END -->`。主站顶栏使用 `SHARED_HEADER` 标记，导读使用 `AUTO:HEADER` 标记；构建注入同一份顶栏，日报/周报模板也使用该组件。README 的来源说明由实际 `site/feed/status.json` 生成，不手写「四路发现」之类能力声明。

旧论文卡片中真正的手写内容会迁移到 `notes/<id>.md`，空标题与占位被移除。若已有 notes 与旧手写内容冲突，构建直接报错，须人工合并。之后只在 notes 编辑手写内容，避免被重新生成的卡片覆盖。相关论文由同子方向日期相邻条目与共同阅读路线生成。英文摘要只翻译对应中文，数字与出现次数保持一致。

## 常规修改与检查

```sh
python scripts/validate.py
python scripts/build.py
python -m pytest -q
git diff --check
git diff --stat
```

提交源数据和受影响的生成物。`build.yml` 在干净 checkout 重建，未提交差异或新生成文件会使检查失败。测试覆盖数字来源、路线引用、笔记迁移、重复构建幂等与出版边界；feed 测试使用合成 fixture、录制响应或 mock，不发送真实 HTTP、LLM、issue 或 PR。

只改 feed 时可先跑 `python -m pytest tests/feed -q`；更改构建和集成路径后运行完整测试。测试完成后，再进行浏览器验收；不要为文案变更重复真实抓取或付费评测。

## 图片与浏览器验收

```sh
python -m pip install playwright
python -m playwright install chromium
python scripts/render_cards.py
python scripts/verify_site.py
```

Linux CI 使用 `python -m playwright install --with-deps chromium` 并安装 Noto CJK 字体。不同系统字体可能造成轻微截图差异。`render_cards.py` 渲染 1080×1350 论文 PNG、1280×640 社交预览，并更新 `assets/social-preview.png`；可仅更新指定论文：

```sh
python scripts/render_cards.py --ids hda starharness
```

渲染会阻止外部请求，二维码由带许可证的本地 JavaScript 生成；回流 URL 来自 `site.config.yaml`，改地址后需重新生成图片。周报分享 PNG 由 `publish --week <周> --render-card` 生成；没有图片时公共页不显示分享入口。

本轮 [截图目录](internal/screenshots/redesign/index.html) 位于 `docs/internal/screenshots/redesign/`，包含 **52 张截图** 与 [verification.json](internal/screenshots/redesign/verification.json)：十个视图（含撤回说明）的浅/深色 × 1440/390、首页/日报桌面英文和创刊回顾双语。`verify_site.py` 还检查导航 DOM 一致、非首页首个区块位置、固定分组顺序、筛选、抽屉焦点、证据可访问标签、受限 `srcdoc` 预览及 README 行数。实际断言以脚本和该次报告为准，截图不是部署证明。

banner 与 RSI map 的 8 张 owner SVG 是静态素材，普通 build 不重画。修改时先预览：

```sh
python scripts/make_svgs.py build/owner-svg-preview
```

审阅后再用 `python scripts/make_svgs.py assets` 更新。`assets/taxonomy.svg` 是另一张数据生成图，仍由普通 build 维护。

## Feed 开发边界

`--root`、`--env-file` 写在子命令之前，`--stage`、`--until`、`--date`、`--week` 写在对应子命令之后。`run --stage all --until summarize --schedule daily --days 2` 验证发现到摘要；CLI 与每日 workflow 都默认 2 天。`--days > 3` 为回填，所有未发布条目（包括已有 ID）标为 `backfill_only`，不能进入日报；已发布的日报、回顾和周报补录保留原状态。批次元数据随抓取和归一化结果保存，单独恢复 dedupe 或 queue 也会继续应用回填限制。

时间逻辑在 `scripts/feed/window.py`：`announced` 保留原始论文日期；`hf_daily_dates` 只保存实际 HF 日榜观测；`news_date` 优先取本期之前最近的 HF 推荐日，无观测时才用来源更新时间/原始发表日。首次窗口为 `D−2 < news_date ≤ D`，以后下界为前一期结束日，且日报/回顾中的已刊 ID 不重复发布。`first_seen` 不参与论文新鲜度判断。

新审核决定默认 `defer`。`accept` 必须在窗内，`backlog` 只批准周报补录；相对 `news_date` 超过 30 天的 `stale` 写入 `review/backlog/<日期>.yaml`，不出 feed。已入库论文直接使用人工证据库内容，不调用模型，也不跳过窗口检查。

`data/feed/items.jsonl` 已改为按 ID upsert 的最新快照，不是追加事件日志。`save_items` 保留其他 ID，原子替换更新后的文件，顺便压缩旧重复行；完全相同的数据不重写。不要依赖文件行数表示处理次数。来源状态另存在 `data/feed/state.json`，最新整轮结果在 `site/feed/status.json.last_fetch`。截至本轮验证，12 路实际运行中 10 路成功，S2 两路因 429 失败；故障不是成功的空响应。

`publish --date <日期>` 检查本地 owner 决定并生成文件；`publish --week <周> --render-card` 汇总日报与显式批准的补录。它们不创建 GitHub PR、不验证 GitHub 身份，不能代替正式 CI。正式 CI 核对已合并 PR 的 owner、准确 revision 和审核文件，并保存 provenance。

旧 `2026-10-27` 日报的撤回保护必须保留。本轮 `site/recaps/2026-10-14--2026-10-27.{json,html,md,en.md}` 来自 `review/corrections/2026-10-27.yaml` 及英文配套文件，是独立的 16 条创刊回顾（15 方法 + 1 理论），目前为本地待审版本。修复不能通过删除撤回记录、改日期或重新运行普通日报发布来恢复旧期。

候选可用 `python -m scripts.feed.cli promote --date <日期>` 暂存到 `build/feed-promotions/<日期>/`，不直接改 `data/papers.yaml`；真正的候选 PR 由 CI 创建，候选证据一律保持 `unknown`。

演示命令只写入被 Git 忽略的 `build/demo/`，带「演示用，自动通过」标记，并继续排除窗外和闸门未通过的条目；不能复制进正式站点或订阅源：

```sh
python -m scripts.feed.cli publish --week 2026-W44 --demo --render-card
```

`scripts.feed.ci` 的 GitHub 写入限定在真实 Actions runner。开发和测试不得伪造 `GITHUB_ACTIONS` 或 `GITHUB_WORKSPACE` 绕过限制，使用 mock 验证外部调用。

## 提示词回归

`feed/model.yaml` 的基础模型和 classify 为 `deepseek-flash`，Harness 闸门单独使用 `deepseek-v4-pro`。修改定义、模型或闸门时，使用 [harness-gate-cases.yaml](../feed/eval/harness-gate-cases.yaml) 的 45 个样本；它包含 25 条人工复审与 20 条预选证据库正例。库内正例标签不是新增全文审计结论。

元数据补取是显式联网操作：

```sh
python -m scripts.feed.eval --fetch-metadata
```

评测 CLI 不自动读取 `.env.local`。使用已配置的环境变量执行 `python -m scripts.feed.eval --workers 4`，或显式复用安全解析函数：

```sh
python - <<'PY'
from scripts.common import ROOT
from scripts.feed.cli import configure
from scripts.feed.eval import main

configure(ROOT, '.env.local')
main()
PY
```

这会真实调用模型并使用按来源、提示词和模型区分的缓存。存在闸门样本集时，当前报告写入 `feed/eval/gate-report.json` 与 `gate-report.md`；旧 `report.*`、`report-initial.*`、`gate-report-initial.*` 是历史结果。没有密钥时显示跳过；门槛未通过时退出非零。

2026-10-27 最终评测完成 45 / 45，precision **0.9600**、recall **0.8571**；目标为 ≥ 0.85、≥ 0.90，故 **完成运行不等于门槛通过**。人工复审批次的历史基线为 8 / 20，即 precision 0.40；新全量评测集与历史批次构成不同，且包含提示词校准例，不能宣称盲测提升。详细子集结果、误判与限制见 [闸门报告](../feed/eval/gate-report.md)。

当前审核 PR 带 `[GATE BELOW THRESHOLD]` 提醒，仍必须由 owner 审核；不通过修改人工标签提高指标，也不因为指标改善就自动发布。

## GitHub Pages 与正式发布

正式地址配置为 `https://adongwanai.github.io/follow-rsi`。`pages.yml` 发布 `site/`，`cards.yml` 单独重画图片并触发 Pages；网站和素材修改后须核对对应 Actions 提交及线上版本。

**截至本轮修复，`feed-publish.yml` 在 GitHub 端仍禁用。** owner 审阅、合并修复并确认出版物后再启用。该状态与 YAML 是否包含触发器是两回事，本地生成回顾和构建成功均不代表已发布。

作者名称维护于 `site.config.yaml`，构建同步 `CITATION.cff`；不编造账号链接。内部需求、审计和截图位于 `docs/internal/`。发布与供稿见 [贡献指南](../CONTRIBUTING_zh.md)，本轮验证和仍需处理的事项见 [验收记录](acceptance.md)。
