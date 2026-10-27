> 当前项目约定（2026-10-27）：仓库为 `adongwanai/follow-rsi`，网站为 https://adongwanai.github.io/follow-rsi/。默认中文入口为 `README.md`，英文入口为 `README_en.md`，`README_zh.md` 是中文镜像。部署配置唯一来源是 `data/site.yaml`。人工审核闸门始终保留；真实接入、测试结果和未完成项分别见 `feed-setup.md`、`acceptance.md`、`data-audit.md`。下文是 owner 提供的任务规范，不能据此宣称验收已经通过。

# 任务：搭建开源仓库 follow-rsi

你要从零搭建一个开源 GitHub 仓库，对外品牌是 **Follow RSI**（仓库名保持 `follow-rsi`）。第一期做的是品牌下的 **Harness 自进化证据库**：每篇论文都有一张**证据卡片**，经典论文以后会配精读笔记和视频，每个方向有一篇整体解读。第二期会在同一个仓库里加每日动态和每周精选（另有任务说明）。

仓库里已有这些文件（如果不在对应位置，先把它们放过去）：

- `data/papers.yaml`：**唯一数据源**，收录 98 篇论文加 6 篇候选，所有摘要和数字都已人工核对过。
- `design/reference.html`：网站的视觉原型，详见第十二节。
- `README.md`、`README_zh.md`：owner 写好的介绍页，详见第九节。

你的工作是搭建结构、生成器、网页和自动化，**不是**写论文内容。

---

## 一、硬性规则（违反任何一条都算失败）

1. **不编造任何论文信息。** 不新增论文，不新增或改动任何数字、机构、日期、结论。`summary_zh` 和 `result_zh` 原样使用。
2. **未知就是 unknown。** `evidence` 里没写的字段一律是 `unknown`，不要凭摘要或常识去推断成 `yes` 或 `no`。
3. **`needs_reading: true` 的条目**在所有输出里都要显示「待细读 / Needs verification」标记。
4. **英文摘要只能是翻译。** 允许你为每篇生成 `summary_en` 和 `result_en`，但只能翻译对应的中文字段：不增删事实，数字、单位、正负号、百分号逐字保留。这些条目加上 `en_machine_translated: true`。必须有一个测试，检查中英文字段里出现的数字集合完全一致。
5. **联网只用于 CI 里的 arXiv 监控脚本。** 不要在搭建过程中抓网页来「补全」论文数据。
6. 凡是需要人填写的位置（笔记、视频、idea 解读），统一用 `<!-- TODO -->` 占位，不要写示例内容冒充真实内容。

---

## 二、目标目录结构

```
.
├── README.md                 # 英文主页（自动生成的区块 + 手写区块）
├── README_zh.md              # 中文主页
├── data/
│   ├── papers.yaml           # 已有，唯一数据源
│   ├── routes.yaml           # 你新建：阅读路线（内容见第六节）
│   └── schema.json           # 你新建：papers.yaml 的 JSON Schema
├── papers/<id>.md            # 每篇一页，由生成器创建
├── directions/
│   └── open-problems.md      # 研究空白（内容见第七节）
├── checklist.md              # 证据自查清单（内容见第八节）
├── site/                     # GitHub Pages 静态站（可筛选表格）
├── badges/<id>.json          # shields.io endpoint 徽章数据
├── scripts/
│   ├── validate.py           # 按 schema 校验 yaml，检查 id/arXiv 唯一、section 合法
│   ├── build.py              # 生成 README 区块、papers/*.md、site 数据、badges、stats
│   └── arxiv_watch.py        # 按关键词查 arXiv 新论文并开 issue
├── tests/                    # pytest
├── .github/
│   ├── workflows/            # validate.yml、build.yml、pages.yml、arxiv-watch.yml
│   ├── ISSUE_TEMPLATE/       # new-paper.yml、fix-evidence.yml
│   └── pull_request_template.md
├── CONTRIBUTING.md / CONTRIBUTING_zh.md
├── CITATION.cff
├── LICENSE                   # 代码：MIT
└── LICENSE-CONTENT           # 文字内容：CC BY 4.0
```

使用 Python 3.11+，只依赖 `pyyaml`、`jsonschema`、`jinja2`、`pytest`，写进 `requirements.txt`。网站用纯 HTML、CSS 和原生 JS，不引入构建工具。

---

## 三、数据与 schema

`data/papers.yaml` 结构为 `meta` 加上 `papers` 列表。每篇的字段：

- 必填：`id`、`title`、`date`、`section`，以及 `arxiv` 和 `url` 至少一个
- 可选：`orgs`、`must_read`、`needs_reading`、`status`（`candidate`）、`tags`、`edit_targets`、`route`、`weight_update`、`kind`、`code`、`summary_zh`、`result_zh`、`evidence`
- `evidence` 的字段（取值 `yes | no | partial | unknown | na`，缺省为 `unknown`）：`held_out`、`disjoint_evolution_set`、`matched_budget_baseline`、`cross_model_transfer`、`cost_reported`、`reliability_metric`、`code_released`、`evolved_harness_released`
- `evidence` 里的分类字段：`who_edits`（`self | external | trained | self_human_reviewed | unknown`），`feedback`（`ground_truth | proxy | self_generated_tests | demonstrations | self_judgment | unknown`），`timing`（`offline | online | test_time | during_run | unknown`）

把以上写成 `data/schema.json`，`validate.py` 用它校验。arXiv 链接一律由 id 拼成 `https://arxiv.org/abs/<arxiv>`，HF 链接为 `https://huggingface.co/papers/<arxiv>`（`cs/` 开头的旧编号不生成 HF 链接）。

---

## 四、生成器 `scripts/build.py`

必须幂等：连续运行两次，第二次不产生任何 diff。

1. **README 区块。** 只改写两个标记之间的内容：`<!-- AUTO:XXX:START -->` 和 `<!-- AUTO:XXX:END -->`，标记之外的手写内容原样保留。需要生成的区块：
   - `STATS`：总篇数、各节篇数、必读篇数、证据字段的已审覆盖率。覆盖率指非 `unknown` 字段的占比，要明确写成 “reviewed so far / 已审”，不能写成「多少篇达标」，避免误导。
   - `MUST_READ`：20 篇必读，按阅读路线顺序排列。
   - `ROUTES`：读取 `routes.yaml` 渲染成表格。
   - `TABLES`：每节一张表，列为 日期 | 论文（链接）| 机构 | 核心机制 | 关键结果 | 证据图标 | 页面链接，按日期升序。中文 README 用中文字段，英文 README 用英文字段。
   - 证据图标：用 ✅ / ◐ / ❌ / ❔ 依次表示 yes / partial / no / unknown，并在表格上方给出图例；只显示 `held_out`、`matched_budget_baseline`、`cross_model_transfer`、`cost_reported` 四项。
2. **`papers/<id>.md`。** 文件不存在时用模板创建；已存在时只刷新 `AUTO` 区块，保留人写的部分。模板：
   ```
   # <title>
   <!-- AUTO:CARD:START -->
   arXiv / HF / Code 链接 · 日期 · 机构 · 所属方向 · 必读 / 待细读标记
   | 证据字段 | 值 |（全部 evidence 字段，含 who_edits / feedback / timing）
   **一句话**：summary_zh
   **关键结果**：result_zh
   <!-- AUTO:CARD:END -->
   ## 精读笔记
   <!-- TODO -->
   ## 视频
   <!-- TODO: B站 / YouTube 链接 -->
   ## 可延伸的 idea
   <!-- TODO -->
   ## 相关论文
   <!-- TODO -->
   ```
   中英文放在同一页：中文在上，英文折叠在 `<details>` 里。
3. **`site/`。** 生成 `site/papers.json`。`site/index.html` 以仓库里的 `design/reference.html` 为视觉标准（见第十二节），功能包括：搜索框（按 `/` 聚焦）；按方向、证据字段、必读、待细读筛选；按日期排序；点击行打开证据小票（receipt）抽屉；「论文 / 阅读路线 / 研究空白」三个视图；中英切换。必须同时支持浅色和深色模式，手机宽度下不出现横向滚动。
4. **`badges/<id>.json`。** 输出 shields.io endpoint 格式，例如 `{"schemaVersion":1,"label":"evidence","message":"held-out ✓ · budget ? · transfer ✓","color":"..."}`。在 `CONTRIBUTING` 里说明论文作者如何把这个徽章嵌进自己的 README。
5. **`stats.json`。** 供 README 和网站共用的统计数据。

---

## 五、自动化

- `validate.yml`：每个 PR 跑 schema 校验和 pytest。
- `build.yml`：每个 PR 运行 `build.py`；如果生成结果和提交的内容不一致就失败，并提示 “run `python scripts/build.py`”。
- `pages.yml`：main 分支有更新时把 `site/` 部署到 GitHub Pages。
- `arxiv-watch.yml`：每周一 UTC 01:17 运行 `arxiv_watch.py`。它调用 arXiv API，在标题和摘要里搜索 `"harness evolution" OR "harness self-evolution" OR "harness optimization" OR "self-evolving harness" OR "recursive self-improvement" AND agent`，按 arXiv id 与 `papers.yaml` 去重，用 `gh` 为每篇新论文开一个带 `candidate` 标签的 issue，标题和正文只放标题、链接和摘要原文。单次最多开 15 个，并要能手动触发。

---

## 六、`data/routes.yaml` 内容（照抄）

```yaml
routes:
  - name_zh: 打基础
    name_en: Foundations
    papers: [adas, dgm, meta-harness, hyperagents]
    question_zh: 「搜索 Agent 设计」与「自改代码」两条源头各自是什么？
  - name_zh: 方法主线
    name_en: Mainline methods
    papers: [ahe, self-harness, darwinx, modularrsi, rrsi]
    question_zh: 最常见的对比基线各自解决了什么？
  - name_zh: 工程闭环与长程可靠性
    name_en: Engineering loop & long-horizon reliability
    papers: [autosaddler, modularrsi, riseharness]
    question_zh: 怎样从失败轨迹定位到代码、控制修改范围、验证跨任务收益？
  - name_zh: 改进器自身进化
    name_en: Evolving the improver
    papers: [hsi, meta-n, aide2, milo, harness2, rsiflow]
    question_zh: 搜索策略或元 Agent 怎样持续更新，证据够不够？
  - name_zh: 没有答案标签
    name_en: No ground-truth labels
    papers: [tthe, harness2, harnesspro, agent-s4]
    question_zh: 用什么代理信号选版本，怎样控制错误反馈？
  - name_zh: 多任务与跨模型泛化
    name_en: Multi-task & cross-model generalization
    papers: [harnesscompass, starharness, mad-rsi, oo-harness]
    question_zh: 怎样避免只适配一组任务或一个模型？
  - name_zh: 任务与证据选择
    name_en: Task & evidence selection
    papers: [activesaddler, ssr, ecdysis, task-coevolve]
    question_zh: 下一轮用哪些任务、哪些失败来驱动修改？
  - name_zh: 模型与 Harness 协同
    name_en: Model–harness co-evolution
    papers: [harnessx, co-evolving-harnesses-models, self-hpo, harnessadapt-rl]
    question_zh: 什么时候改 Harness、什么时候改权重，收益怎样拆分？
  - name_zh: 实验设计（所有人必读）
    name_en: Experimental design (everyone)
    papers: [rethinking-evaluation, hda, harnessopt-bench, auditing-product, trusting-trust-revisited]
    question_zh: 同预算下，收益来自可迁移改进、额外计算还是过拟合？基线有没有泄露答案？
```

`question_en` 由你翻译补上。`validate.py` 要检查这里引用的每个 id 都存在于 `papers.yaml`。

---

## 七、`directions/open-problems.md` 内容（中文照抄，英文翻译放在下方）

标题：可切入的研究空白（每条都有收录论文作为证据）

1. **什么任务值得演化 Harness**：Rethinking 在 TB2.1 上未胜过测试时扩展，HDA 把大部分收益归为过拟合与额外计算；但长程游戏上优势明显。「任务对 Harness 的敏感度」本身可以做成系统分析，Evo-Bench 的选题指标是起点。
2. **无真值验证器时的准入**：Evo-Harness 与 Self-Authored Verification 都发现自判会误导演化；Harness²、TTHE、HarnessPro、Agent S4 各给了代理信号方案，但都没有分析代理信号何时失效。
3. **改 Harness 还是改权重**：SIA 的选择策略是静态的；Self-HPO 显示交替更新优于只改一边，但自我提议（64.8）仍不及强外部提议器（66.3）；HarnessForge、CoEvo-RSI、Co-Evolving 都指向「匹配性」，但怎么度量匹配性仍是空白。
4. **证明元层真的变好**：Auditing 统计只有 4/26 的工作做了同起点、同预算的前后代对比；ARC-AGI-3 受控研究的留出提升区间跨过零。
5. **证据选择的理论**：SSR、ActiveSaddler、ECDYSIS 都是实证规则；REUSE 与 Safe Harness Self-Evolution 给了部分统计理论，但还没人把「选哪些失败」和泛化界连起来。
6. **稀疏反馈、长程与具身**：DemoEvolve、EMHO、HSI 都报告了失败或边界；RiseHarness 用 Pass^r 说明可靠性是和覆盖率不同的优化目标。
7. **安全与可审计**：投毒 benchmark、答案泄露、预算绕过都已被实际观察到；把「自改过程的可审计性」做成可度量指标，目前仍少有人做。

每条里提到的论文名都要链接到对应的 `papers/<id>.md`。

---

## 八、`checklist.md` 内容（中英双语）

标题：Harness 演化论文证据自查清单。每项一个 `- [ ]`，并注明它对应 `evidence` 里的哪个字段：

- 演化集与评测集分开，评测集在搜索期间不可见 → `held_out`
- 演化任务与下游评测基准不相交 → `disjoint_evolution_set`
- 与同算力的测试时扩展（并行采样、顺序修正）做对比 → `matched_budget_baseline`
- 不重新演化就迁移到其他模型家族 → `cross_model_transfer`
- 报告 token 或美元成本，包括演化本身的成本 → `cost_reported`
- 多次重复运行，报告方差或 Pass^k → `reliability_metric`
- 检查答案泄露：容器 git 历史、benchmark 答案文件、硬编码答案
- 声称改进了「改进流程」时，在同起点、同预算下比较前后两代流程
- 公开代码 → `code_released`；公开演化出的 Harness → `evolved_harness_released`
- 报告失败的设置和收益回落的轮次

每项后面附一句「为什么」，并引用收录论文（例如 HDA、Rethinking、Trusting Trust、Auditing），链接到对应页面。

---

## 九、README（以 owner 提供的文件为准）

`README.md` 和 `README_zh.md` 由 owner 写好，品牌为 **Follow RSI**，标语为「每天 5 分钟，跟上 RSI 前沿」/「Five minutes a day to keep up with recursive self-improvement」。规则：

- **手写部分逐字保留**，不要改写、润色或增删。
- 生成器只改写 `<!-- AUTO:XXX:START -->` 与 `<!-- AUTO:XXX:END -->` 之间的内容。文件里已有 `BADGES`、`METRICS`、`STAR_HISTORY` 三组标记。第四节要求的 `STATS`、`MUST_READ`、`ROUTES`、`TABLES` 区块，追加在「证据卡片长什么样」一节之后的新小节「证据库」里，新小节的标题和一句说明由你按现有文风补上。
- `METRICS` 区块在第二期上线前保持「—」占位；徽章里的篇数从 `stats.json` 生成。
- 两个文件中指向尚不存在页面的链接（`/daily/`、`/weekly/`、`/feed/*`）保留原样，在完成汇报里列出来，等第二期补上。
- `<SITE_URL>`、`<GITHUB_USER>` 是占位符，统一从 `data/site.yaml` 读取并在 build 时替换；配置文件里先填占位值。
- `CITATION.cff` 的标题写 “Follow RSI: Harness Evolution Evidence Base”，作者写 `<AUTHOR_NAME>`。

---

## 十、贡献流程

- `new-paper.yml`：必填 arXiv 链接、所属 section 和一句话机制；可选证据字段，每项都要附出处（页码或表号）。
- `fix-evidence.yml`：论文、字段、新值、出处（页码或表号），并勾选「我是作者 / 我读过正文」。
- PR 模板：要求填写数字的出处；提醒运行 `python scripts/build.py`；只改 `data/` 和人写区块。
- `CONTRIBUTING.md` 写清楚：改数据只改 yaml；任何数字都要带出处；`unknown` 改成 `yes` 或 `no` 时，必须在 PR 里写出依据。

---

## 十一、测试（`tests/`）

- schema 校验通过；id 唯一；arXiv 编号唯一；`routes.yaml` 引用的 id 都存在
- `build.py` 幂等：运行两次后 `git diff --exit-code` 通过
- 数字一致性：每篇的 `summary_zh`、`result_zh` 里的所有数字都原样出现在生成的 README_zh 和 `papers/<id>.md` 里；`summary_en`、`result_en` 的数字集合与中文字段一致
- 手写区块保护：在 `papers/<id>.md` 的 TODO 区写入测试文本后再 build，文本仍然保留
- `needs_reading` 条目在 README 与网站数据里都带标记
- 证据覆盖率统计等于非 `unknown` 字段数除以总字段数

---

## 十二、设计与传播（和数据准确一样重要）

这个仓库要靠转发传播，所以「好看」和「好分享」是硬性要求，不是加分项。

### 12.1 视觉标准

仓库里的 `design/reference.html` 是一个可直接运行的原型，已用真实数据跑通。`site/index.html` 必须**还原它的视觉语言**，而不是另起一套。可以重构代码（拆出 CSS、JS 和数据文件），但不要改设计。要保留的要点：

- **概念**：审计账本加凭证小票。顶栏品牌为「Follow RSI」，首屏眉题为「Follow RSI · Harness 自进化证据库」，主标题是论点「每一篇论文，都要拿出凭证。」，配两张「凭证存根」：HDA 的 54%，以及 Auditing 的 4/26。点击存根打开对应论文。分享卡片页脚统一写「Follow RSI」。
- **配色**：沿用原型 `:root` 里的 token，包括冷灰纸色底、墨色字、唯一强调色群青，以及浅色、深色两套值。证据状态使用独立的语义色（有、部分、没有、未审），并且同时用形状区分（实心方块、半填方块、带叉方框、空心圆），不能只靠颜色。
- **字体**：标题 Noto Serif SC 900，正文 Noto Sans SC，数据和标签 IBM Plex Mono，并配好后备字体栈。不要换成 Inter、Space Grotesk 这类通用字体。
- **结构**：sticky 筛选栏；按方向分组的账本行（日期、标题加机构、两行摘要、四个证据标记）；右侧抽屉打开带锯齿顶边的小票，含 MUST READ 印章、证据字段表、笔记、视频和 idea 三个「筹备中」占位，以及分享卡片预览。
- **克制**：不加渐变大背景、emoji 或滚动触发的动画，也不要给所有块都套圆角加阴影。
- **可访问性**：焦点可见，抽屉按 Esc 关闭并归还焦点，尊重 `prefers-reduced-motion`；所有交互元素都能用键盘操作。
- **链接**：`#p-<id>` 直接打开某篇的小票，`#routes` 和 `#gaps` 打开对应视图，分享时可以精确到篇。视图切换用按钮配合点击处理，不要用 `<a href="#...">`。所有 `history.replaceState` 和 `pushState` 调用都包在 try/catch 里：页面被嵌进沙箱 iframe（如 srcdoc）时这些调用会抛错，失败了也不能影响任何交互。拿不到 http(s) 页面地址时，「复制链接」要给出提示，而不是复制一个无效地址。

### 12.2 每篇一张分享卡片（传播主力）

- 新增 `site/card.html?id=<id>`，按原型里的「分享卡片」样式渲染 1080×1350 的卡片：深色底配点阵纹理、论文短名、一句话、四格证据（✓ ◐ ✕ ?）、关键结果，页脚是 arXiv 编号和仓库名。
- 新增 `scripts/render_cards.py`：用 Playwright 截图 `card.html`，输出 `site/cards/<id>.png`。另做一张 1280×640 的 `site/og.png`，作为仓库的 social preview。
- 新增 `.github/workflows/cards.yml`：`papers.yaml` 变化时重新生成卡片并提交。CI 里要安装 Noto CJK 字体，确保中文不会渲染成方块。
- 抽屉里提供「复制链接」和「下载分享卡片」（直接链到 PNG）两个按钮。
- 为每篇生成静态页 `site/p/<id>.html`，带 `og:title`、`og:description`、`og:image`（即该篇卡片）和 `twitter:card=summary_large_image`，打开后跳转到 `index.html#p-<id>`。这样链接发到 X、微信、Slack 时都会显示预览图。

### 12.3 GitHub README 的观感

- **横幅和方向图已由 owner 提供，不要重画**：`assets/` 下有 8 个 SVG（`banner-{light,dark}.svg`、`banner-zh-{light,dark}.svg`、`rsi-map-{light,dark}.svg`、`rsi-map-zh-{light,dark}.svg`），以及生成它们的 `scripts/make_svgs.py`。README 已经引用好了。改文案时改脚本再重新生成，不要手改 SVG。
- 网站新增「方向图」视图（hash `#map`，README 里已链接）：沿用 `rsi-map` 的版式，用 HTML 重做成可交互版本。每个方向格子显示收录篇数，点击后切到论文视图，并按该方向筛选。证据库目前只覆盖 Harness，其他方向的格子先显示「第二期上线后接入每日动态」。
- 横幅下面放一行 shields 徽章（论文数、必读数、最近更新日期、License），颜色统一使用强调色和墨色。
- 证据图标在 README 里用 ✅ ◐ ❌ ❔，表格上方给出一行图例。
- 首屏控制在一屏之内：横幅、一句话、三句说明、快速入口。长表格放在折叠区或下方。
- 在 `assets/` 里放一个 `social-preview.png`（即上面的 og.png），并在 README 的手写区注明：去 Settings → Social preview 上传它。

### 12.4 作者徽章

`badges/<id>.json` 的颜色规则：四项全部 yes 时用绿色，有 unknown 时用灰色，其余用强调色。`CONTRIBUTING` 里给出可复制的 Markdown 片段：`![evidence](https://img.shields.io/endpoint?url=<pages-url>/badges/<id>.json)`。

---

## 十三、完成标准

1. `pip install -r requirements.txt && python scripts/validate.py && python scripts/build.py && pytest` 全部通过。
2. 本地打开 `site/index.html` 可以筛选、搜索、切换中英文，深色模式下文字清晰可读。
3. README 与 README_zh 的表格条数分别等于 98（正文）和 6（候选单独一节）。
4. 不新增任何论文信息；`git diff data/papers.yaml` 只出现新增的 `summary_en`、`result_en`、`question_en`、`en_machine_translated` 字段。
5. 设计还原：用 Playwright 截取 `site/index.html` 与 `design/reference.html`，各取桌面 1280 宽和手机 400 宽、浅色和深色共四张，放进 `docs/screenshots/` 并排对比，视觉上应当一致。
6. `site/cards/` 下 98 张卡片 PNG 与 `site/og.png` 生成成功，中文正常显示；随机抽查 3 张，数字与 yaml 一致。
7. `site/p/<id>.html` 的 og 标签齐全，`og:image` 指向存在的 PNG。

完成后用中文汇报：做了什么；测试结果；还有哪些 `<!-- TODO -->` 需要我手动补；有没有发现 `papers.yaml` 里的数据问题（只报告，不要自行修改）。
