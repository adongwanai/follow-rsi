# Follow RSI 验收记录

截至 2026-10-27。仓库为 [adongwanai/follow-rsi](https://github.com/adongwanai/follow-rsi)，网站为 [GitHub Pages](https://adongwanai.github.io/follow-rsi/)。这里区分实际完成的检查、待人工审核的内容和未接入的外部能力。

## 已验证

| 范围 | 结果 |
| --- | --- |
| 原始论文 | 98 篇收录、6 篇候选、20 篇必读；去除新增英译字段后，逐字段与 owner 文件完全一致。 |
| 证据记录 | 8 项检查共 43 / 784 项有记录（5.5%），没有把未审字段伪装成已审。 |
| 构建 | Schema、路线引用、数字一致性、手写区保护通过；连续构建输出相同。 |
| 离线测试 | 128 项通过，覆盖信源解析、缓存、数字与引文护栏、每日审核、周精选、发布、候选、CI 审批与 CLI 集成。 |
| 网站 | 1280 / 400px、浅色 / 深色检查通过；筛选、OR/AND 组合、短名、排序、语言记忆、键盘焦点、详情切换正常。线上方向图与手机布局已验证。 |
| 图片 | 104 张 1080×1350 分享卡及社交预览生成；真实仓库 URL 和二维码已写入。owner 提供的 8 张 SVG 原样保留。 |
| README | 默认中文；README_en.md 为英文，README_zh.md 保留为中文镜像。自动统计与折叠证据库、方向图、阅读路线已接入。 |
| GitHub 自动化 | [128 项测试](https://github.com/adongwanai/follow-rsi/actions/runs/40489111622)、[分享卡生成](https://github.com/adongwanai/follow-rsi/actions/runs/40489111664)与 [Pages 部署](https://github.com/adongwanai/follow-rsi/actions/runs/40489271404)均在真实 Actions runner 上通过。Pages 已切为 workflow 模式。 |
| HF 真实运行 | 回溯 2026-10-14 至 2026-10-27，共 275 篇唯一条目；8 篇已在原库。其余 267 篇得到 50 include、27 borderline、185 exclude、5 schema error。 |
| 摘要 | 77 组中英文摘要，最终数字护栏失败 0；82 篇待审、185 篇排除供抽查。没有替 owner 作出接受决定。 |
| 日报与周报 | 离线验证日报、周精选、Atom、JSON schema、延迟指标、defer 顺延、撤稿与候选提案。真实数据演示仅保存在 Git 忽略的 build/demo/，明确标为自动通过的演示。 |
| 密钥 | LLM 密钥在本地忽略文件和 GitHub Secrets 中；发布前对暂存文件扫描实际密钥，没有命中。 |

首期 [owner 审核 PR #1](https://github.com/adongwanai/follow-rsi/pull/1) 已由 Actions 创建：82 篇待审，185 篇排除项供抽查。审核检查因 `pending` 状态按预期阻止发布；这不是构建或测试失败。线上 `feed/status.json`、徽章、日报与周报入口均返回 HTTP 200，公开 feed 通过 schema 校验且保持 0 篇，未越过人工审核。

浏览器对比见 [截图](screenshots/index.html)。具体运行步骤见 [feed-setup.md](feed-setup.md)，原始数据问题见 [data-audit.md](data-audit.md)。

## 实时评测仍未完全验收

真实模型已评分 105 / 107 条。include recall 95.9%、include precision 98.9%、primary accuracy 90.8%，三个数值门槛达到；完整状态仍为 **incomplete**。两条论文身份需要核对，一条 schema 失败，27 个 curator seeds 需要 owner 复核。没有为提高分数更改标签。详见 [完整评测报告](../feed/eval/report.md)。

## 仍需完成的内容

- 配置并验证 S2_API_KEY，才可启用 Semantic Scholar 引用与作者追踪。当前 14 天真实运行优先覆盖 HF；不能声称完整多信源验收已完成。
- owner 审核真实每日 PR 后，今日动态、公开 feed、周精选和 Release 才有正式内容。首期为空是审核闸门的结果。
- 20 篇必读的全文证据审计没有完成；原始数据中的未知字段保持未知。后续补证据需正文页码或表号。
- 论文精读笔记、视频、方向深度解读与作者的 B 站 / 小红书 / 公众号链接仍待填充。Harness 入门导读已完成。
- 谱系关系图需要逐条引用或对比关系来源；当前方向图不声称论文之间存在未经核实的继承关系。
- 可安装的个性化订阅 skill 属于可选第三阶段，尚未实现。
- 没有调用 GPT image2.5：当前没有可用调用入口和图像 API 密钥；采用 owner 后续提供的 SVG，并用本地浏览器生成卡片，未冒称 AI 生图。
- GitHub 仓库 Social preview 需要 owner 在 Settings 中上传 assets/social-preview.png；图已生成。

Anthropic 和 Prime Intellect 没有找到经过核实的官方 RSS，保持停用。其他来源的逐项验证见 [source-verification.md](source-verification.md)。
