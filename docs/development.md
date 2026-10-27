# 开发与构建

仓库默认 README 为中文，英文入口是 [README_en.md](../README_en.md)。本文说明代码与生成物如何修改；运行发现、配置密钥和 owner 审核见 [feed-setup.md](feed-setup.md)。

## 安装与本地预览

使用 Python 3.11，与 CI 保持一致。在仓库根目录执行：

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/validate.py
python scripts/build.py
python -m pytest -q
python -m http.server 8000 --directory site
```

浏览器打开 `http://localhost:8000/`。网站是静态 HTML、CSS、JavaScript；没有 Node 构建步骤。`site/data.js` 也支持直接打开本地主页，HTTP 预览更适合一起检查日报、周报和链接。

`requirements.txt` 包含 PyYAML、jsonschema、Jinja2、pytest，以及 feed 使用的 requests、feedparser 和一个官方 LLM SDK（OpenAI）。普通构建与单元测试不需要 API key，也不请求外部来源；安装依赖本身需要访问包仓库。浏览器和图片步骤另装 Playwright。

## 哪些文件可以直接改

| 文件 | 维护方式 |
| --- | --- |
| `data/papers.yaml` | 证据库论文的唯一数据源；数字与证据变更附正文页码或表号。 |
| `data/routes.yaml` | 阅读路线及顺序；论文 ID 必须存在。 |
| `site.config.yaml` | 仓库、Pages、作者与订阅 URL 的唯一配置。 |
| `README.md`、`README_en.md` | 分别为中文、英文手写源；只在 AUTO 区块外编辑正文。 |
| `README_zh.md` | 中文备用入口；只更新自己的 AUTO 区块，手写内容独立保留。 |
| `papers/<id>.md` | AUTO:CARD 区块由数据生成；区块外保留精读、视频与想法。 |
| `directions/*.md`、`site/guide.html` | 手写方向说明与导读；导读双语 HTML 和 Markdown 要一起同步。 |
| `site/index.html`、`site/app.js`、`site/style.css` | 网站页面与交互源码。 |
| `feed/sources.yaml`、`feed/taxonomy.yaml`、`feed/model.yaml`、`feed/prompts/` | 发现规则、分类、公开模型配置和提示词。 |
| `data/feed/`、`review/`、`daily/`、`digests/` | 运行记录、owner 决定与已生成的出版物，按运行流程维护。 |

`scripts/build.py` 校验数据后更新 README 的 AUTO 区块、论文卡片区块、JSON、徽章、社交落地页和分类图。它不会改写 `data/papers.yaml`，不会调用 LLM，也不会把未知证据改成肯定或否定。保留所有 `<!-- AUTO:...:START -->` / `<!-- AUTO:...:END -->` 标记；缺失、重复或顺序错误会直接失败。

所有 README 生成块外的作者文字必须逐字保留；不以镜像方式覆盖任何一份文件。论文页顶端标题属于手写区，改题名时需同时处理该标题。英文摘要仅翻译对应中文，数字及出现次数保持一致；原有 `needs_reading` 标记不应被生成器隐藏。

## 常规修改与检查

改数据后运行：

```sh
python scripts/validate.py
python scripts/build.py
python -m pytest -q
git diff --check
git diff --stat
```

提交源数据和受影响的生成物。PR 的 `build.yml` 在干净 checkout 中重建，生成文件有差异或产生未提交文件即失败。`tests/test_catalog.py` 检查来源数字、路线引用、手写区保留和重复构建幂等；feed 测试使用录制 fixture 或 mock，不发真实 HTTP、LLM 请求、issue 或 PR。

只改 feed 时可以先跑 `python -m pytest tests/feed -q`；修改集成路径后运行完整测试。实时评测与真实信源抓取是独立操作，不能把离线测试通过写成所有网络路径验证通过。

## 图片与浏览器验收

```sh
python -m pip install playwright
python -m playwright install chromium
python scripts/render_cards.py
python scripts/verify_site.py
```

Linux CI 安装 Chromium 时使用 `python -m playwright install --with-deps chromium`，并安装 Noto CJK 字体。普通开发环境只需要自己系统适用的字体；不同系统字体可能使截图略有差异。

`render_cards.py` 通过临时本地 HTTP 服务渲染每篇 1080×1350 的 PNG、1280×640 社交预览，并更新 `assets/social-preview.png`。只重画部分论文可用：

```sh
python scripts/render_cards.py --ids hda starharness
```

渲染期间外部请求被阻止，二维码由带许可证的本地 JavaScript 生成。真实回流 URL 来自 `site.config.yaml`，改地址后需要重画卡片。`verify_site.py` 检查筛选、排序、语言记忆、详情键盘焦点及深浅主题，并写入 `docs/screenshots/`；检查范围与具体断言可直接在脚本中查看。

owner 提供的 8 张 banner / RSI map SVG 是静态素材，普通 build 不会重画。确需更新时显式运行原生成器，先输出到临时构建目录审阅：

```sh
python scripts/make_svgs.py build/owner-svg-preview
```

确认后再使用 `python scripts/make_svgs.py assets` 更新这 8 张图。`assets/taxonomy.svg` 是另外一张数据生成图，仍由普通 build 维护。

## Feed 开发边界

本地 CLI 的 `--root`、`--env-file` 必须写在子命令之前；`--stage`、`--until`、`--date`、`--week` 写在各自子命令之后。`run --stage all --until summarize` 适合验证发现到摘要的流程。只处理单阶段用 `run --stage judge` 或 `run --stage summarize`；`--until` 只适用于 `--stage all`。

`python -m scripts.feed.cli publish --date <日期>` 会检查已有 owner 决定并写入本地日报与公开文件；`publish --week <周> --render-card` 汇总已批准日报并生成周报。它们不创建 GitHub PR、不验证 GitHub 身份，不应代替正式 CI 发布流程。正式 CI 使用已合并 PR 的 owner 身份、准确 revision 和审核文件核验，并保存 provenance。

审核后候选可先用 `python -m scripts.feed.cli promote --date <日期>` 暂存到 `build/feed-promotions/<日期>/`。该命令生成提案与 PR 正文，不直接改当前 `data/papers.yaml`；真正的候选 PR 由 CI 创建，候选证据一律 `unknown`。

演示命令只输出到被 Git 忽略的 `build/demo/`，带「演示用，自动通过」标记；这些内容不能复制进正式站点或订阅源：

```sh
python -m scripts.feed.cli publish --week 2026-W44 --demo --render-card
```

`scripts.feed.ci` 的 GitHub 写入函数限定在 Actions runner 中执行。开发和测试不应伪造 `GITHUB_ACTIONS` 或 `GITHUB_WORKSPACE` 来绕过限制；用离线 mock 检查外部调用。

## 提示词回归

首次补取真实论文元数据是显式联网操作：

```sh
python -m scripts.feed.eval --fetch-metadata
```

评测 CLI 本身不会自动读取 `.env.local`。使用已经配置好的环境变量执行 `python -m scripts.feed.eval --workers 4`；若使用本地环境文件，可复用 CLI 的安全解析函数：

```sh
python - <<'PY'
from scripts.common import ROOT
from scripts.feed.cli import configure
from scripts.feed.eval import main

configure(ROOT, '.env.local')
main()
PY
```

这会真实调用模型，可能产生费用；缓存按来源内容和模型复用。报告写到 `feed/eval/report.json` 与 `report.md`。无密钥会明确显示 `skipped`；未完成、错误或门槛未过时退出非零。即使已评分样本的三个数字达标，也不能忽略身份不匹配和未完成项。不要为提高分数修改 curator 标签；owner 的真实纠正以追加记录保留来源。

## GitHub Pages 与生成物

当前正式地址为 `https://adongwanai.github.io/follow-rsi`，配置在 `site.config.yaml`。`pages.yml` 发布 `site/`，`cards.yml` 负责单独重画图片；新卡片完成后会再部署 Pages。修改网站或地址后，确认 Actions 对应提交成功，再核对线上版本。

GitHub README 的社交预览需在 Settings → Social preview 手动上传 `assets/social-preview.png`。作者信息维护于 `site.config.yaml`、`CITATION.cff` 和许可证，不在页面中编造外部账号链接。发布与供稿细节见 [贡献指南](../CONTRIBUTING_zh.md)。
