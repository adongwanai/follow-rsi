# Follow RSI 修正与改版验收

截至 2026-10-27。本轮修改在 `fix/reviewed-news-and-public-site` 分支，须经 owner 审核 PR 后合并。线上已执行的是错误 10 月 27 日日报的撤回；本地创刊回顾与改版不代表已经上线。旧版验收记录已[存档](internal/acceptance-before-correction.md)。

## 内容与审核

- 真实 HF 每日榜单回放覆盖 10 月 14–27 日，预筛后 277 篇唯一候选。仅采用 owner 明确决定的 8 篇保留及 8 篇补回，生成 16 篇创刊回顾（15 篇方法、1 篇 Harness 专项理论）；其他候选没有自动得到接受决定。[逐日篇数与名单](internal/reports/hf-daily-replay.md)。
- 日期使用实际观测到的 HF 推荐日 `news_date`，另外显示原始发表日 `announced` 和版本更新日。`first_seen` 不用于填充推荐日。普通发现默认 2 天；大于 3 天的补采只能进入补录，超过 30 天的条目不进公开 feed。
- 原始 25 篇逐篇应用 owner 复审：8 保留、1 顺延、10 移出 Harness、6 拒绝；旧审核 YAML 和原审核 provenance 保留。撤回的日期不能重新作为普通日报发布，撤回的论文不能被 correction 恢复。回顾采用独立 Atom 标识与去重记录。
- 104 条书目（98 收录、6 候选）的原字段与 `1930ef8` 完全一致，仅增加 scope、needs_review 和双语建议。98 篇拆为 61 方法、15 Harness 评测/理论、16 背景、6 通用 RSI。**这些是书目分类，不能解释为 61 篇已完成全文证据核验。**
- [20 条分类待核清单](internal/reports/needs-review.json) 保留全部原文和原栏目；[分类边界审计](internal/reports/audit-library-classification.md) 覆盖 104 条目录、16 条公开摘要，全文核验数为 0。必读 20 篇未出现虚假的“已核 20/20”徽章。

## 自动判定与信源

[真实闸门评测](../feed/eval/gate-report.md) 共 45 例：precision **0.9600**，recall **0.8571**；召回低于 0.90，**门槛未通过**。原 25 篇子集 P/R 为 0.875/0.875；排除 10 个 prompt 示例后，35 例为 0.950/0.8261。旧 precision 0.40 来自原自动判为 Harness 的 20 篇，样本口径不同，不能与 45 例直接作同比。

4 个漏判：TokenEconomizer、HARBOR、SkillOpt-Lite、Living-Harness；1 个误判：owner 要求 defer 的 CarryOn (robot)。没有为通过门槛修改标签、放宽引文校验或把未知证据写成 yes。首次运行的 6 次超时记录保存在[初评报告](../feed/eval/gate-report-initial.md)，重试后 45 例无 API/schema 错误。自动审核 PR 标题与首行显式提示门槛未过。

[真实信源运行](internal/reports/source-fetch-audit.md) 共尝试 12 路：10 路成功，S2 citations/authors 两路因 429 失败，失败仍进入状态记录。484 条来源记录经归一与 upsert 得到 427 个唯一条目，新增 152 条；不是 427 条人工接受。[补采迁移](internal/reports/backfill-migration.json) 把全部 411 条未发布记录标为历史补采，16 条已审回顾保持原状态，审核决定和其余字段不变。之前漏掉的 8 篇已由真实 arXiv 查询全部召回。S2 匿名限速、指数退避与有 key 请求头通过离线测试；没有宣称此次 S2 完整分页成功。

## 页面与仓库

- 中文默认，README 从 444 行缩至 177 行；英文同步，README_zh 仅跳转。完整表移到 PAPERS.md；首次按新规范重写之后，构建仍只改 AUTO 块。
- 首页、证据库、方向图、阅读路线、研究空白、今日动态、每周精选、导读和论文抽屉统一导航。仅首页保留大 hero，其他标签页内容顶端不超过 260px；含正文的刊期首卡不超过 400px。
- 摘要仅显示当前语言；未知证据折叠，列表全未知时显示“证据待核”。空笔记、空视频标题和内部审核按钮不出现在公共页面。论文卡支持 BibTeX、路线说明和相关论文。
- [浏览器截图与断言](internal/screenshots/redesign/index.html) 共 52 张截图、8 组验收，覆盖 1440/390px、深浅主题、回顾中英版本、过滤与分组排序、键盘焦点及不透明 srcdoc。原始 owner 的 8 张 SVG 与 make_svgs.py 字节未变。
- [文件迁移清单](internal/reports/file-migrations.json)：旧任务说明、内部审计和截图移至 docs/internal；删除重复的根目录 stats.json。既有手写笔记按内容迁移，不生成空小节。

## 部署与维护者事项

- 真实仓库与网站地址继续由 site.config.yaml 提供。作者使用已配置的 `Adong / 阿东玩 AI`，未编造作者信息或社交账号；GitHub API 确认 Discussions 已开启。
- feed-publish 工作流因错误刊期撤回而仍处于手动禁用状态。**owner 合并本 PR 后再启用**，防止旧版流水线在修正前再次发布。普通代码 PR 合并会部署已审核过的本地生成物；其后日常发布继续要求每日审核 PR 合并。
- docs/internal 当前仍随开源仓库保留，owner 可决定是否另行移出；其中原始任务文档是历史记录，现行要求以本轮修正代码和运行文档为准。
- 20 篇全文证据审读、深度笔记/视频、带来源的论文谱系图、Follow RSI Skill、作者外部账号仍未完成或未提供，不在公共首屏展示完成占位。当前采用 owner 提供的 SVG 与浏览器生成图，没有冒称调用了不可用的 GPT image2.5。

全量 `.venv/bin/python -m pytest -q`：**271 passed**。[两次构建检查](internal/reports/build-verification.json) 完全一致，README 手写区保留，未发现真实密钥或旧仓库名；生成页面的本地资源与链接检查通过（源模板的变量不视为页面 URL）。旧判定错误可重试，周报补录已发布记录不会被历史补采重新标记，均有回归覆盖。

本轮通过标准是：错误刊期不能复活、未审条目不能发布、日期/范围可追溯、原论文数据不变、所有离线回归和构建检查通过。分类召回未达门槛作为明确限制交给 owner 审核，不与工程测试混为一谈。
