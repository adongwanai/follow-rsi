> 当前项目约定（2026-10-27）：仓库为 `adongwanai/follow-rsi`，网站为 https://adongwanai.github.io/follow-rsi/。默认中文入口为 `README.md`，英文入口为 `README_en.md`，`README_zh.md` 是中文镜像。部署配置唯一来源是 `data/site.yaml`。人工审核闸门始终保留；真实接入、测试结果和未完成项分别见 `feed-setup.md`、`acceptance.md`、`data-audit.md`。下文是 owner 提供的任务规范，不能据此宣称验收已经通过。

# 第二期任务：Follow RSI（递归自我改进进展追踪）

## 零、背景与目标

第一期已经搭好仓库 `follow-rsi`（对外品牌 **Follow RSI**）：数据在 `data/papers.yaml`，有生成器、网站和证据卡片。第二期要在同一个仓库里加一套**进展追踪系统**，自动发现 RSI 方向的新论文，做分类、证据速判和摘要，经过人工审核后产出：

1. **今日动态**（每天）：`daily/<YYYY-MM-DD>.md`（中英文）和网站「今日」页，只包含当天审核通过的条目。
2. **每周精选**（每周）：`digests/<YYYY>-W<WW>.md`（中英文）、网站「每周精选」页、一张分享图，以及 RSS/Atom 订阅。
3. **公开 feed**：`site/feed/latest.json`，给以后的 skill 和第三方使用（形式参考 follow-builders 的中心化 feed）。
4. **仓库候选**：审核通过的 Harness 方向论文，自动开 PR，以 `status: candidate` 加入 `data/papers.yaml`。
5. **质量指标**：召回率、准确率、时效、各信源产出，每周公开。

品牌标语：**每天 5 分钟，跟上 RSI 前沿。** 审核闸门不变：每日和每周的所有对外内容，都必须先经过 owner 人工审核。

整个系统围绕三件事设计：**不漏**（多路发现加对照检查）、**不错**（分层判断、数字护栏、人工审核）、**不断**（健康检查、自动报警、幂等重跑）。

---

## 一、硬性规则

1. **数字护栏**：任何自动生成的文字（中英文摘要、周报条目），其中的每个数字都必须原样出现在该论文的标题或摘要里，由程序检查，见第七节。不通过就重试一次，仍不通过则丢弃这段摘要，只保留标题和链接。
2. **证据速判只能判「有」或「未知」**：摘要里没提，不代表论文没做，所以不允许输出 `no`。每个 `yes` 都必须附一段原文引用，程序检查这段引用确实是摘要的子串，否则改成 `unknown`。所有速判结果都标为「自动判断，未核实」。
3. **人工审核前不对外发布**：没经过人工审核的条目，不进入周报、公开 feed 和仓库 PR。精选和点评只由 owner 手写，系统不生成任何「编辑推荐」。
4. **合规**：
   - arXiv API 每 3 秒最多 1 次请求，带上自定义 User-Agent。只存元数据和摘要，不存 PDF 全文。
   - Semantic Scholar 使用 `S2_API_KEY`，遵守它的速率限制。
   - 不抓取 X/Twitter。
   - 所有密钥只从环境变量或 GitHub Secrets 读取。
5. **幂等**：所有抓取和处理任务都可以重复运行，不产生重复条目。LLM 结果按（arXiv id、版本、提示词哈希、模型名）缓存，命中缓存就不再调用。
6. **不编造信源**：本文只列出候选信源的名称。RSS 地址和 API 地址由你核实：能访问且格式正确的才设为 `enabled: true`，找不到的保持 `enabled: false` 并写明原因。
7. **单元测试离线运行**：网络和 LLM 全部用录制好的 fixture 或 mock 代替。

---

## 二、目录结构（在第一期仓库上新增）

```
feed/
  sources.yaml              # 信源登记表（第三节）
  taxonomy.yaml             # 方向分类体系（第五节）
  prompts/                  # 提示词全文（第六节）
    relevance.md  classify.md  evidence.md  summarize.md  translate.md  digest_intro.md
  eval/
    labeled.yaml            # 评测集（第十节）
data/feed/
  items.jsonl               # 所有条目，一行一篇，append-only，合并时以最新为准
  state.json                # 各信源游标、已见 id、上次成功时间
  cache/                    # LLM 结果缓存
  metrics.json              # 指标（第九节）
review/
  daily/<YYYY-MM-DD>.yaml   # 每日审核单（第八节）
  <YYYY>-W<WW>.yaml         # 每周精选单（第八节）
daily/
  <YYYY-MM-DD>.md  <YYYY-MM-DD>.en.md
digests/
  <YYYY>-W<WW>.md  <YYYY>-W<WW>.en.md
site/
  feed/latest.json  feed/atom.xml  daily/index.html  daily/<YYYY-MM-DD>.html  weekly/index.html  weekly/<YYYY>-W<WW>.html
  cards/digest-<YYYY>-W<WW>.png
scripts/feed/
  fetch_arxiv.py  fetch_s2.py  fetch_hf.py  fetch_rss.py  fetch_github.py
  normalize.py  dedupe.py  judge.py  guard.py  review.py  digest.py  promote.py
  health.py  recall_check.py  eval.py  llm.py  cli.py
tests/feed/ ...
skill/follow-rsi/           # 第三阶段（第十三节）
```

依赖限于 `requests`、`feedparser`、`pyyaml`、`jsonschema`、`jinja2`、`pytest`，以及一个官方 LLM SDK。`llm.py` 做一层抽象，通过环境变量 `LLM_PROVIDER`、`LLM_MODEL`、`LLM_API_KEY` 选择厂商和模型。所有调用都设 `temperature=0`，按 JSON schema 输出，解析失败就重试一次。

---

## 三、信源：四路发现

`feed/sources.yaml` 的格式：

```yaml
- id: arxiv-harness            # 唯一
  kind: arxiv_query | s2_citations | s2_authors | hf_daily | rss | github_releases
  enabled: true
  schedule: daily | weekly
  params: {...}
  notes: "..."
```

健康状态（上次成功时间、本周抓取数、累计收录数、连续失败次数）写在 `state.json`，不写回这个文件。

### 3.1 arXiv 关键词检索（每日）

分类限定 `cat:cs.AI OR cs.CL OR cs.LG OR cs.MA OR cs.SE OR cs.RO OR cs.NE`。用 `ti:` 和 `abs:` 检索，下面三组各建一个信源：

- **arxiv-harness**：`"harness evolution"`、`"harness optimization"`、`"self-evolving harness"`、`"harness self-improvement"`、`"agent harness" AND (evolv* OR optimiz* OR "self-improv*")`、`scaffold AND "self-improv*"`、`"automated design of agent*"`、`"meta-agent" AND (evolv* OR "self-improv*")`
- **arxiv-rsi**：`"recursive self-improvement"`、`"self-improving agent*"`、`"self-evolving agent*"`、`"self-modifying"`、`"Gödel machine"`、`"Godel machine"`、`"open-ended" AND agent AND "self-improv*"`
- **arxiv-adjacent**：`"skill evolution"`、`"experience-driven" AND agent`、`"automated AI research"`、`"AI scientist" AND "self-improv*"`、`"self-play" AND "zero data"`、`"continual learning" AND agent AND (harness OR skill OR memory)`

每次按 `submittedDate` 降序取最近 3 天，靠已见 id 去重，这样漏跑一天也能补上。`params` 里保存检索式原文，方便以后调整。

### 3.2 引用滚雪球（每周，最关键的一路）

**种子**：`data/papers.yaml` 里所有 `must_read: true` 和 `section: foundations`、且有 arXiv 编号的论文，另加 `hyperagents`、`meta-harness`、`hgm`、`ace`。

用 Semantic Scholar 的 `paper/arXiv:<id>/citations` 接口，抓最近 30 天内首次出现的施引论文。条目里记录它引用了哪些种子（`seed_hits`）：命中的种子越多，越可能相关，这个数会作为排序信号之一。

### 3.3 作者追踪（每周）

从种子论文中取出现两次及以上的作者，再加上每篇种子的通讯作者（即末位作者），总数上限 150 人，用 `author/<id>/papers` 接口抓最近 30 天的新论文。

### 3.4 补充信源

- **hf-daily**（每日）：Hugging Face Daily Papers 接口，用关键词初筛后进入流水线，同时记录 upvotes 作为热度信号。
- **rss-***（每日）：下列实验室和机构的博客或研究页，地址由你核实：Sakana AI、METR、Anthropic（research / news）、OpenAI research、Google DeepMind blog、Prime Intellect、Weco AI。博客文章不是论文：如果文中带 arXiv 链接，就并入对应论文条目；否则作为 `kind: post` 条目，只在周报的「实验室动态」一节出现。
- **github-releases**（每日）：`data/papers.yaml` 里所有 `code` 字段指向的仓库，记录新 release，周报里只列出版本号和链接。

---

## 四、流水线

`python -m scripts.feed.cli run --stage all` 依次执行以下步骤，每一步都可以单独运行：

1. **fetch**：各信源抓取原始数据，存入 `data/feed/raw/<source>/<date>.json`。
2. **normalize**：统一字段：`arxiv_id`（去掉版本号）、`version`、`title`、`authors`、`abstract`、`categories`、`published`、`updated`、`links`、`source_hits`（列表，记录是从哪些信源发现的）、`seed_hits`、`hf_upvotes`、`code_links`（从摘要和 comments 字段里提取）。
3. **dedupe**：先按 arXiv id 合并；再按标题做模糊匹配（归一化后的 token 集合相似度 ≥ 0.9），把会议版、预印本或改名的版本合并为一条，并记录别名。`data/papers.yaml` 里已有的论文标记 `in_repo: true`，只追踪版本变化，不再重复判断。
4. **judge**：按顺序调用三个提示词：`relevance` → 结果为 `include` 或 `borderline` 时调用 `classify` → `include` 时再调用 `evidence`。结果写进条目的 `llm` 字段，附上模型名和提示词哈希。
5. **summarize**：对 `include` 和 `borderline` 的条目生成中文一句话摘要，翻译成英文，然后过数字护栏。
6. **queue**：每天把新的待审条目写进 `review/daily/<date>.yaml` 并开 PR；前一天没审完或标了 defer 的条目，自动顺延到当天的审核单。详见第八节。
7. **publish**：每日审核 PR 合并后，生成当天的今日动态、网站页面和 feed，并为通过审核的 Harness 论文开仓库 PR；每周精选单合并后，生成周报和分享图。

**版本与撤稿**：已收录的论文（包括 `in_repo` 的）每周检查 arXiv 是否有新版本。有新版本就在条目上标记 `version_changed`；如果它在 `papers.yaml` 里，再开一个 issue「<id> 出了 v<n>，请复核证据卡片中的数字」。发现撤稿时，从公开 feed 中移除并开 issue。

**排序**：周报每个方向内的排序，只看这些可以解释的信号：`seed_hits` 数、是否被作者追踪命中、`hf_upvotes`、是否公开代码，加上 owner 的精选（置顶）。权重写在 `feed/sources.yaml` 顶部的 `ranking:` 字段里，不用任何不透明的打分。

---

## 五、分类体系 `feed/taxonomy.yaml`（照抄）

```yaml
directions:
  harness:
    zh: Harness / 脚手架 RSI
    en: Harness RSI
    def_zh: 模型权重不变或只是辅助，被改进并带入下一轮的主要是提示、工具、记忆、技能、控制流、工作流或改进器代码。
    sub:  # 与 data/papers.yaml 的 section 一致
      evolve_main: 整体 Harness 搜索与演化
      generalize: 泛化、正则、准入与成本
      evidence_selection: 任务与证据选择
      improver: 改进器自身进化
      component: 组件级进化（技能、记忆、上下文、接口）
      coevolution: 模型与 Harness 协同进化
  model_weights:
    zh: 模型 / 权重 RSI
    en: Model-weight RSI
    def_zh: 模型用自己产生的轨迹或数据训练自己（SFT、自蒸馏、RL），下一代模型再产生更好的数据，且至少跑了两轮或明确设计为多轮。
  data_task:
    zh: 数据与任务 RSI
    en: Data & task RSI
    def_zh: 由 Agent 设计训练数据配比、合成任务或课程、自动构建环境，决定模型下一轮学什么。
  ai4ai:
    zh: 训练算法 / AI 研发 RSI
    en: AI-for-AI RSI
    def_zh: Agent 改进训练算法本身、自主做模型研发，或研究 Agent 改进自己做研究的能力。
  experience_world_model:
    zh: 经验、世界模型与探索 RSI
    en: Experience, world-model & exploration RSI
    def_zh: 把经验沉淀为跨任务复用的记忆、规则手册、技能或可执行世界模型，或改进探索策略本身。
  meta:
    zh: 元 RSI
    en: Meta-level RSI
    def_zh: 改进「负责产生改进的机制」本身。若该机制是 Harness，主方向记为 harness/improver，meta 记为次方向。
  embodied:
    zh: 具身与物理 RSI
    en: Embodied & physical RSI
    def_zh: 机器人策略或具身 Agent 在仿真或真机中递归改进。
cross:   # 只能作为次方向，或在评测、理论、安全类论文中作为主方向
  evaluation_benchmark: 评测、基准与归因
  theory_survey: 理论与综述
  safety_governance: 安全与治理
exclude_reasons:
  not_persistent: 只在当前任务内迭代，修改不保留到后续任务（例如测试时反复修正同一个答案）
  static_framework: 提出固定的 Agent 或 Harness 框架，本身不随反馈演化
  different_sense_of_harness: harness 指测试或模糊测试框架（test harness、fuzz harness）等其他含义
  single_round_training: 只做一次训练或蒸馏，没有可迭代的改进闭环
  off_topic: 与 RSI 无关
```

---

## 六、提示词全文（分别存入 `feed/prompts/*.md`，运行时用 jinja2 填变量）

每个提示词末尾都附上 JSON schema。调用方用 schema 校验输出，不合法就重试一次，仍失败则记为 `error`，进入人工队列。

### 6.1 `relevance.md`

```
你是递归自我改进（RSI）方向的文献编辑。判断下面这篇论文是否应收录进 RSI 进展追踪。

收录标准（两条都满足才算 include）：
1. 系统根据执行、实验或评估反馈，修改它自己的某个部分（权重、数据、提示、工具、记忆、技能、控制流、工作流、改进机制本身之一）；
2. 被接受的修改会保留下来，并在后续任务或后续改进轮次中使用。

也要收录：专门评测、归因、理论分析或综述上述系统的论文（它们自己不改进也算）。

排除（label = exclude，并给出 exclude_reason）：
- not_persistent：只在当前任务内迭代，修改不保留到后续任务
- static_framework：提出固定框架，本身不随反馈演化
- different_sense_of_harness：harness 指测试框架、模糊测试框架等其他含义
- single_round_training：只做一次训练或蒸馏，没有可迭代的改进闭环
- off_topic：与 RSI 无关

拿不准时用 borderline，不要硬判。只根据下面提供的标题和摘要判断，不要使用你对这篇论文的任何其他记忆。

标题：{{ title }}
摘要：{{ abstract }}

输出 JSON：
{"label": "include|borderline|exclude",
 "exclude_reason": "not_persistent|static_framework|different_sense_of_harness|single_round_training|off_topic|null",
 "reason_zh": "不超过 40 字，指出摘要里的哪句话支撑你的判断",
 "confidence": 0.0-1.0}
```

### 6.2 `classify.md`

```
给这篇 RSI 论文分方向。只能使用下面定义的方向，不要自创类别。

{{ taxonomy_definitions }}   # 由程序展开 taxonomy.yaml 中的 directions、sub 与 cross，含 def_zh

规则：
- primary 选「每轮被改进、并带入下一轮的主要对象」所在的方向；
- 若 primary 是 harness，必须给出 harness_sub；
- secondary 最多 2 个，可以包含 cross 类别；
- 评测、基准、归因类论文的 primary 记为 evaluation_benchmark，理论与综述类记为 theory_survey，并在 secondary 里写它所研究的方向；
- 只根据标题和摘要判断。

标题：{{ title }}
摘要：{{ abstract }}

输出 JSON：
{"primary": "...", "harness_sub": "...|null", "secondary": ["..."],
 "improved_object_zh": "被改进并带入下一轮的对象，不超过 15 字",
 "confidence": 0.0-1.0}
```

### 6.3 `evidence.md`

```
只根据摘要，判断这篇论文是否报告了以下实验设计。规则：
- 只有摘要明确写出时才填 "yes"，并在 quote 里给出摘要中支撑它的原文片段（必须逐字复制，长度 5–60 个字符）；
- 摘要没写，一律填 "unknown"，不得填 "no"；
- 不要根据常识或你对论文的记忆推断。

字段：
- held_out：在演化或训练中未见过的任务、基准或划分上评估
- matched_budget：与同等计算或推理预算的基线（如并行采样、测试时扩展）对比
- cross_model：改进结果迁移到其他模型或模型家族
- code_released：摘要或评论中给出了代码或项目链接

摘要：{{ abstract }}
评论字段：{{ comments }}

输出 JSON：
{"held_out": {"value": "yes|unknown", "quote": "...|null"},
 "matched_budget": {"value": "yes|unknown", "quote": "...|null"},
 "cross_model": {"value": "yes|unknown", "quote": "...|null"},
 "code_released": {"value": "yes|unknown", "quote": "...|null"}}
```

### 6.4 `summarize.md`

```
用中文为这篇论文写一句话摘要，给关注 RSI 的研究者看。

要求：
- 40–90 个汉字，一句或两句；
- 先说它改进了什么、怎么改进，再说最重要的一个结果；
- 数字只能使用标题和摘要里原样出现的数字，单位和正负号不变；摘要没给数字就不写数字；
- 不用「首个」「突破性」「显著」等评价性词语，除非摘要原文这样说，且要写成「作者称」；
- 方法名、基准名保留英文原文；
- 不加引号、表情或标签。

标题：{{ title }}
摘要：{{ abstract }}

输出 JSON：{"summary_zh": "..."}
```

### 6.5 `translate.md`

```
把下面的中文摘要翻译成英文，给研究者看。不增删任何事实；数字、单位、正负号、百分号逐字保留；方法名和基准名保持原样；不超过 45 个英文单词。

中文：{{ summary_zh }}

输出 JSON：{"summary_en": "..."}
```

### 6.6 `digest_intro.md`

```
下面是本周通过人工审核的 RSI 论文统计和标题列表。写一段周报开头，中文 2–3 句：说明本周各方向新增多少篇、哪个方向最集中。只能使用下面给出的数字和名称，不要评价论文好坏，不要推荐论文（推荐由编辑另写）。

本周统计：{{ counts_by_direction }}
本周标题：{{ titles }}

输出 JSON：{"intro_zh": "...", "intro_en": "..."}
```

---

## 七、数字护栏 `scripts/feed/guard.py`

- **提取数字**：先把全角字符转半角，去掉千分位逗号，再用正则提取所有数字 token。正则覆盖整数、小数、百分数和分数：`[-+]?\d+(?:\.\d+)?%?`，以及 `\d+/\d+`。`3.8x`、`1.84×` 这类带倍数符号的写法，取出其中的数字部分。
- **检查规则**：
  - `numbers(summary_zh) ⊆ numbers(title + abstract)`
  - `numbers(summary_en) == numbers(summary_zh)`（作为多重集合比较）
  - `numbers(intro) ⊆ numbers(输入统计)`
- 例外只有一种：计数类数字（篇数、周次）由程序填入模板，不经过 LLM。
- 不通过时：重试一次，在提示词里附上「以下数字不在原文中：…」；再失败就把 `summary_zh` 置空，标记 `guard_failed`，进入人工队列。
- 证据速判的 `quote` 必须是摘要的子串（比较前把连续空白归一为单个空格），否则把该字段改为 `unknown`。
- 必须有单元测试，至少覆盖：百分号、小数、全角数字、范围写法「4–30」、「2.42M」，以及数字被篡改的反例。

---

## 八、人工审核（一切对外发布的闸门）

**每日审核单**：每天 UTC 03:17（当天的抓取和处理结束后），`review.py` 生成 `review/daily/<YYYY-MM-DD>.yaml` 并开 PR，标题为「Review: Follow RSI <date>」。前一天未合并的审核单里的条目顺延进来，旧 PR 自动关闭。格式：

```yaml
date: 2026-10-28
items:
  - arxiv_id: "2610.xxxxx"
    title: "..."
    llm: {label: include, primary: harness, harness_sub: evolve_main, secondary: [], confidence: 0.86}
    summary_zh: "..."
    evidence_quick: {held_out: yes, matched_budget: unknown, cross_model: unknown, code_released: yes}
    links: {arxiv: "...", hf: "...", code: "..."}
    signals: {seed_hits: 3, author_tracked: true, hf_upvotes: 41}
    decision: pending        # owner 改成 accept / reject / move / defer（顺延到次日）
    direction_override: null # 需要改分类时填写
    summary_override: null   # 需要改摘要时填写，同样要过数字护栏
    promote_to_repo: auto    # auto：harness 方向且 accept 时开仓库 PR；也可填 true / false
    note: ""                 # owner 的一句点评，选填
lab_updates: []              # 博客与 release 条目，owner 勾选要展示的
```

**每周精选单**：每周日 UTC 23:41，生成 `review/<YYYY>-W<WW>.yaml` 并开 PR「Weekly picks: Follow RSI <week>」。条目在每日审核时已经审过，这里只需填写：

```yaml
week: 2026-W44
picks:              # owner 手写的本周精选，0–3 篇，只能从本周已 accept 的条目里选；不填就不出现精选一节
  - arxiv_id: ""
    why_zh: ""
    why_en: ""
editor_note_zh: ""  # 选填，一两句本周观察，同样要过数字护栏
editor_note_en: ""
```

- **排列顺序**：`borderline`、`guard_failed`、低置信度（< 0.6）的排在最前；`exclude` 的不放进审核单，单独列在 `review/daily/<date>.excluded.yaml` 里，方便抽查漏判。
- **合并前检查**：每日单里不能还有 `pending`（暂时不想审的标 `defer`）；所有 override 都过了数字护栏；精选单里 `picks` 引用的 id 都已在本周 `accept`。
- **断更处理**：某天没有合并审核单，那天就不发布今日动态，条目顺延，**绝不自动发布**。连续 3 天没有合并时，开一个 issue 提醒 owner，队列积压超过 60 条时在 issue 里写明数量。
- **命令行辅助**：`python -m scripts.feed.cli review --date 2026-10-28` 提供一个交互界面：逐条显示，按 a/r/m/s 处理，结果直接写回 yaml，方便 owner 每天 5–10 分钟审完。
- 审核结果写回 `items.jsonl` 的 `review` 字段（状态、时间、override、备注）。**这些人工决定会作为评测集的增量数据**，见第十节。

---

## 九、健康检查、指标与召回对照

**健康检查** `health.py`，在每天的抓取之后运行：

- 任一信源连续 3 次运行抓到 0 条或报错，就开 issue「Source down: <id>」，并附上最后一次错误信息。同一个信源同时最多只开一个 issue，恢复后自动关闭。
- 写出 `site/feed/status.json` 和一个 shields endpoint 徽章 `badges/feed-updated.json`，内容为「feed: updated <n>h ago」，超过 48 小时变红。
- arXiv API 连续失败时，自动降级到 arXiv 分类 RSS 再做关键词过滤，并在 `state.json` 里记录降级。

**指标** `data/feed/metrics.json`，按周累计：

| 指标 | 定义 |
| --- | --- |
| `found` / `accepted` | 本周进入流水线的篇数 / 人工通过的篇数 |
| `precision` | LLM 判为 include 的条目中，被人工 accept 的比例 |
| `recall_vs_reference` | 召回对照中，参考清单里有、我们漏掉的篇数和原因 |
| `latency_days` | arXiv 首次提交到进入周报的天数中位数 |
| `source_yield` | 每个信源贡献的 accepted 篇数；只由该信源独家发现的单独计数 |
| `guard_fail_rate` | 数字护栏首次失败的比例 |

周报页脚展示其中三项：本周找到多少篇、收录多少篇、准确率。

**召回对照** `recall_check.py`，每周运行：

- 从 GitHub 拉取这些参考清单，提取 arXiv 编号：`zgcagi/Harness-RSI` 的 `README.md`，`Prism-Shadow/awesome-rsi` 的 `site/src/data/papers.js` 与 `site/src/data/methods.js`，以及本仓库的 `data/papers.yaml`。
- 对照近 60 天的条目：参考清单有、我们 feed 没有的，逐条记录漏掉的原因。原因自动判断为以下之一：从未被任何信源抓到、被判为 exclude、被判为 borderline 后人工拒绝。
- 生成 `review/<week>.misses.yaml` 给 owner 看，并在 PR 描述里附一段统计：「本周漏判 n 篇，其中 k 篇从未被抓到 → 建议新增关键词：…」。关键词只是建议，**不自动修改**检索式。

---

## 十、评测集与提示词回归

`feed/eval/labeled.yaml` 由两部分组成：

1. **自动导入**：`data/papers.yaml` 里日期在 2026-04 之后的非 `foundations`、非 `candidates` 论文，全部标为 `include`。方向的对应关系：
   - `evolve_main`、`generalize`、`evidence_selection`、`improver`、`component`、`coevolution` → `primary: harness`，`harness_sub` 取原 section
   - `evaluation` → `evaluation_benchmark`
   - `survey_theory` → `theory_survey`
2. **手工标注**（下面这些照抄进文件，并注明 `labeled_by: curator-seed, needs_owner_review: true`）：

```yaml
- {arxiv: "2609.14858", name: Dream-RSI,        label: include, primary: experience_world_model}
- {arxiv: "2609.15364", name: RSIAgent,         label: include, primary: experience_world_model}
- {arxiv: "2610.11794", name: Memento 3,        label: include, primary: experience_world_model}
- {arxiv: "2610.13912", name: RSI-Anything,     label: include, primary: experience_world_model}
- {arxiv: "2610.20431", name: SwarmRSI,         label: include, primary: ai4ai}
- {arxiv: "2607.28568", name: Frontis-MA1,      label: include, primary: ai4ai}
- {arxiv: "2609.08183", name: NeoHorse-1,       label: include, primary: data_task}
- {arxiv: "2610.14118", name: ClawLoop,         label: include, primary: data_task}
- {arxiv: "2609.36675", name: Gödel Forest,     label: include, primary: data_task}
- {arxiv: "2610.15772", name: RSIPO,            label: include, primary: model_weights}
- {arxiv: "2610.22192", name: Terminal-RSI,     label: include, primary: model_weights}
- {arxiv: "2609.39306", name: ReSAIL,           label: include, primary: model_weights}
- {arxiv: "2609.30652", name: RSI via On-Policy Distillation, label: include, primary: model_weights}
- {arxiv: "2609.05295", name: RISE,             label: include, primary: model_weights}
- {arxiv: "2609.17523", name: ScienceBuddy,     label: include, primary: harness, harness_sub: coevolution}
- {arxiv: "2610.18842", name: Who Improves the Robot?, label: include, primary: embodied, secondary: [theory_survey]}
- {arxiv: "2609.00137", name: Recursive Criticality,   label: include, primary: theory_survey}
- {arxiv: "2609.15802", name: Economics of RSI,        label: include, primary: theory_survey}
- {arxiv: "2610.14625", name: Two Perspectives on RSI, label: include, primary: theory_survey}
- {arxiv: "2607.21461", name: AREX,             label: exclude, exclude_reason: not_persistent}
- {arxiv: "2609.38288", name: AREX-2,           label: exclude, exclude_reason: not_persistent}
- {arxiv: "2608.01964", name: LongHorizon-Harness, label: exclude, exclude_reason: static_framework}
- {arxiv: "2608.05013", name: OneDayAgent,      label: exclude, exclude_reason: static_framework}
- {arxiv: "2608.27969", name: openJiuwen,       label: exclude, exclude_reason: static_framework}
- {arxiv: "2607.20709", name: NVIDIA OO Agents (NOOA), label: exclude, exclude_reason: static_framework}
- {arxiv: "2607.07007", name: State-machine fuzz harness generation, label: exclude, exclude_reason: different_sense_of_harness}
- {arxiv: "2609.27242", name: LLMs + Genetic Search for ARC-AGI-2, label: exclude, exclude_reason: off_topic}
```

`eval.py`：

- 标题和摘要通过 arXiv API 拉取，缓存成 fixture 后离线复用。
- 对每条运行 relevance 和 classify，输出：
  - include 与 exclude 的准确率和召回率（borderline 单独统计）
  - 方向分类准确率和混淆矩阵
  - 每条判错的样例，附 LLM 给出的理由
- **门槛**：include 召回率 ≥ 0.90，include 准确率 ≥ 0.80，primary 方向准确率 ≥ 0.75。
- CI：`feed/prompts/**` 或 `LLM_MODEL` 有变动时运行 eval，低于门槛就让 PR 失败，并把报告贴进 PR 评论。没有 `LLM_API_KEY` 时跳过，并写明「eval skipped」。
- **持续扩充**：每次审核 PR 合并后，owner 做过 override 或 reject 的条目，自动追加到 `feed/eval/labeled.yaml`，标注 `labeled_by: owner`，让评测集随审核一起变大。

---

## 十一、发布物

0. **今日动态**：每日审核单合并后，生成 `daily/<date>.md`、`daily/<date>.en.md` 和 `site/daily/<date>.html`。按方向列出当天 accept 的条目（格式同周报的「各方向新进展」），附当天勾选的实验室动态。当天没有 accept 条目时不生成页面，`site/daily/index.html` 始终显示最近一期，标注日期。每日条目同时写入 `latest.json` 和 atom（atom 每天一个条目）。

以下由每周精选单合并后的 `digest.py` 生成：

1. **周报 `digests/<week>.md`（中文）和 `.en.md`（英文）**，结构如下：
   - 标题「Follow RSI · <YYYY> 第 <WW> 周」，再加一行日期范围
   - 开头 2–3 句，由 `digest_intro` 生成，过数字护栏
   - **本周精选**：只有 owner 填了 `picks` 才出现。每篇写明标题、owner 的 why、链接，以及仓库证据卡片链接（如果有）
   - **各方向新进展**：按 taxonomy 的顺序，每个方向一个小标题加篇数；每条一行，格式为「短名：一句话摘要」，后接链接 [arXiv] [HF] [Code]，再加证据速判图标（✅ 有、❔ 未知，并标「自动速判」）。已进仓库的论文加「卡片」链接
   - **实验室动态**：owner 勾选的博客和 release
   - **趋势**：一张 SVG 柱状图，展示近 8 周各方向篇数。图由程序按数据生成，深色和浅色主题都要清晰可读
   - **页脚**：本周找到、收录、准确率三项指标，加订阅方式（RSS、仓库 Watch）
2. **网站**：`site/weekly/index.html` 列出历期周报，`site/weekly/<week>.html` 是单期页，沿用第一期 `design/reference.html` 的视觉语言（账本风格、Noto Serif SC 标题、IBM Plex Mono 数据），每期页都带 og 标签。主站顶栏新增「每周进展」入口。
3. **分享图 `site/cards/digest-<week>.png`**，1080×1350：展示本周各方向篇数（小柱状图）、精选标题（如果有）、仓库名和网址，复用第一期的卡片渲染流程。
4. **订阅源**：`site/feed/atom.xml` 每期一个条目；`site/feed/latest.json` 收录最近 4 周通过审核的条目，字段包括 id、title、authors、published、direction、summary_zh、summary_en、evidence_quick、links、week，作为公开 feed 的格式，写一份 JSON schema 放在 `site/feed/schema.json`。
5. **仓库 PR**：`promote.py` 把 accept 的 Harness 方向条目追加到 `data/papers.yaml`，设 `status: candidate`、`section: candidates`、`needs_reading: true`、`summary_zh` 为审核后的摘要，开一个 PR「Add <n> candidates from Follow RSI <week>」。证据字段一律保持 `unknown`：速判结果只写进 PR 描述里给 owner 参考，**不写入证据卡片**。

---

## 十二、自动化（GitHub Actions）

| workflow | 时间（UTC） | 内容 |
| --- | --- | --- |
| `feed-daily.yml` | 每天 02:23 | arxiv-*、hf-daily、rss-*、github-releases → normalize → dedupe → judge → summarize → health |
| `feed-weekly.yml` | 周日 21:07 | s2-citations、s2-authors、版本检查、recall_check |
| `feed-review.yml` | 每天 03:17 | 生成每日审核单并开 PR，顺延未审条目，检查断更 |
| `feed-picks.yml` | 周日 23:41 | 生成每周精选单并开 PR |
| `feed-publish.yml` | 审核单或精选单合并时 | 今日动态或周报 → 网站与订阅源 → 分享图 → promote PR → 部署 Pages |
| `feed-eval.yml` | 改动 prompts 或模型的 PR | eval 与门槛 |

所有 workflow 都要支持 `workflow_dispatch` 手动触发，设置 `concurrency` 防止重叠执行，中间产物通过 commit 回仓库来保存状态。需要的 secrets：`LLM_API_KEY`、`S2_API_KEY`，以及默认的 `GITHUB_TOKEN`。在 `docs/feed-setup.md` 里写清楚每个 secret 怎么申请。

---

## 十三、第三阶段（可选，最后做）：`skill/follow-rsi/`

仿照 follow-builders 的形态，做一个 Claude Code 和 OpenClaw 都能装的 skill：

- `SKILL.md`：首次运行时用对话方式完成配置，包括关注哪些方向（从 taxonomy 中多选）、语言（中文、英文或双语）、频率（每天或每周），配置保存在 `~/.follow-rsi/config.json`。之后读取公开的 `latest.json`，按用户偏好筛选并重新组织，在对话里展示。用户不需要任何 API key。
- 提示词放在 `skill/follow-rsi/prompts/`，用户可以通过对话修改。skill 只做重组，不新增事实；数字规则与第七节相同（只能用 feed 里已有的数字）。
- 第一版只在对话里展示，不做 Telegram 或邮件推送。README 写清楚安装方式。

---

## 十四、测试 `tests/feed/`

- 每种信源一个解析测试，用录制的 fixture：arXiv Atom、S2 JSON、HF JSON、RSS、GitHub releases JSON。
- 去重：同一篇的 v1 和 v2、会议版与预印本、改名后的标题。
- 数字护栏：第七节列出的全部正例和反例。
- 证据 quote 子串校验。
- `judge` 用假 LLM：验证缓存命中、schema 校验失败后重试、出错时进入人工队列。
- 审核单：有 `pending` 时 CI 失败；override 也要过数字护栏；`picks` 只能引用已 accept 的条目。
- 发布：没有 `picks` 时不出现精选一节；promote 不改动证据字段；`latest.json` 符合 schema。
- 健康检查：连续 3 次 0 条时开 issue，恢复后关闭，并且不重复开 issue（用 mock 的 gh）。
- 幂等：同一天的 pipeline 跑两次，`items.jsonl` 内容不变。

---

## 十五、完成标准

1. `pytest` 全部通过（离线）。
2. 用一个真实的 `LLM_API_KEY` 和 `S2_API_KEY` 对最近 14 天跑一遍完整 pipeline，生成一份样例审核单。你**不能**替 owner 做审核决定：样例周报要用一个标明「演示用，自动通过」的测试开关生成，并且只在 PR 里展示，不发布。
3. 运行 eval 并附上报告：三个门槛是否达标；没达标就列出主要的错误类型和改进建议，**不要为了过门槛去改评测集标签**。
4. `docs/feed-setup.md` 写清楚：怎么申请和配置 secrets，每周审核的完整流程（预计 30 分钟），怎么新增或停用信源，怎么看指标和健康状态。
5. 用中文汇报：做了什么；哪些信源核实后启用、哪些因找不到地址而停用；eval 结果；还有哪些地方需要 owner 决定。
