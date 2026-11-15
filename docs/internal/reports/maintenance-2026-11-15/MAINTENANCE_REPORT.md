# 2026-11-15 维护、补刊与积压审查

本报告冻结在出版 PR 提交前。来源 PR [#109](https://github.com/adongwanai/follow-rsi/pull/109) 与日期审核 PR [#110](https://github.com/adongwanai/follow-rsi/pull/110)、[#111](https://github.com/adongwanai/follow-rsi/pull/111)、[#112](https://github.com/adongwanai/follow-rsi/pull/112) 已由真实账户 `adongwanai` 合并，精确 head 的检查通过。合并动作依据 owner 持续授权，不代表 owner 手工逐篇阅读。出版合并、Pages 与线上字节核验是后续独立步骤，最终回执记录在 [证据跟进 issue #60](https://github.com/adongwanai/follow-rsi/issues/60)。

## 当日简报与补刊

实际维护开始于北京时间 10:31，来源采集开始于 10:34；没有把这次采集称为 08:00 快照。全部 12 路启用来源已尝试，路线请求共 98 次。HF 11/15、11/14 均为 HTTP 200 空列表；11/13 完整 34 个成员没有晚到 ID 或推荐日遗漏。S2 引文有局部结果、限流与超时，作者路线未取得作者论文页，缺失覆盖未知。逐路时间、数量和错误见 [来源报告](SOURCE_REVIEW.md)。

新增候选 16 个稳定 ID，经来源、主审与独立复审后为 7 纳入、6 排除、3 待补官方正文。7 篇按官方原发表日分别补入 11/11、11/12，发现日与审核日均为 11/15；没有 HF 推荐日期的论文没有伪造榜单归期。今天发布实质采集与审核简报，0 篇当日新论文，不把旧论文计作今天新增。

| 期次 | 本次内容 | 日期边界 |
| --- | --- | --- |
| [11/15](https://adongwanai.github.io/follow-rsi/daily/2026-11-15.html) | 采集、审核与阻塞简报；0 篇新论文 | 本次采集时点，不代表全天所有来源无更新 |
| [11/11](https://adongwanai.github.io/follow-rsi/daily/2026-11-11.html) | 补入 RSI-PDEbench、Verify by Doing、HyperSkill、AskALCF；整期 5 篇 | 原有 World In-Context Learning 整条 public item 保留，原审核日仍为 11/12 |
| [11/12](https://adongwanai.github.io/follow-rsi/daily/2026-11-12.html) | 补入 Migration Agent、EGE、SLM routing；整期 3 篇 | 整期 reviewed_on 为 11/15，旧 published_at 保留 |

三张日期审核单共 19 行变化，仅 18 行正式应用：7 accept、6 reject、3 defer、2 backlog。旧 `2611.14256` 只重绑旧审核单的来源快照，没有重新 apply，现行 11/13 reject 完整保留。上述页面链接是部署目标；此冻结报告本身不证明上线。

9 条中英文摘要经过原文绑定、数字 guard 与独立范围复核。论文限制明确保留：Verify by Doing 跨任务重置；Migration Agent 限 Study 3 人工监督修复且原始工件未公开；HyperSkill 限失败反馈形成的协议指令；EGE 只含合成实验；AskALCF 的自动生成知识变更尚未获准合并到部署语料并重建索引。没有把这些审查称为实验复现或所有数字重新计算。

## 历史积压与版本工作

规范库从 2,074 增至 2,090；所有原始来源、历史发现、审核单和重试记录按稳定 ID 对账后的并集为 8,917。窗口内来源漏入、规范记录未覆盖、审核单 ID 遗漏与 HF 推荐日遗漏均为 0。最终分区如下；正式记录包含排除和历史 backlog，不能读作全部接受或全部已刊。

| 规范记录状态 | 数量 |
| --- | ---: |
| 已有正式决定或目录记录 | 1,001 |
| 可复用范围建议，仍需相应正式流程 | 1,023 |
| 待补范围或身份证据 | 53 |
| 外部正文阻塞 | 13 |
| 合计 | 2,090 |

Harness Repair 和 D-Skill 按当前 v1 完成历史 backlog 决议；不升级版本，也不计入今天新论文。D-Skill 的教师/学生执行轨迹能提供离线执行反馈，形成跨任务复用的操作协议，因此纠正了“没有新的在线评价就不能纳入”的初稿理由；默认流程与另有验证门的 SkillOpt 变体分别保留。Harness Repair 旧版数字混绑已纠正，本次使用无数字摘要。

版本范围比较累计完成 39 项，本次新增 10 项；其中累计 24 项复用有效审查、15 项完成实质正文交叉。10 对新交叉的初稿与纠正均保留，包括 ProAS 数值标签、Chess 同版优化差异、ROI v2 的记忆替换效果、ASENA baseline 限制与 Drafting v2 成本变化。RSI4EO 只有 v2 新增的 LRS-GRO 能有限纳入 Harness，当前 v1 排除仍保持。正式版本采用为 0。

剩余 337 项版本内容/范围比较没有宣称完成。已恢复 478 个明确版本正文：141 对旧新正文齐全；196 项仅目标正文齐全，原版身份未知。对这 196 项的原始哈希和 223 次 HF 出现已逐条核对，原始来源没有版本字段或带版本 URL，不能反推 v1。明确版本恢复失败、未尝试均为 0，但取回正文不等于完成内容审查。

版本恢复实际免费请求 461 次：448 次 HTTP 200，13 次 HTML 404 后由官方带版本 PDF 成功；30 个版本复用缓存。节流记录有 5 个间隔略低于自定 3.2 秒目标，最小 3.1886705 秒；保留 `all_checks_passed=false` 的运营告警，不改日志或阈值。请求没有重叠，原文身份、完整性和哈希阻断检查通过。

完整 177,212,761 字节版本正文包仅保留本地，SHA-256 为 `dfb9804ed5fef17e1d27bfcdef22e29c5f3226cca6b730793a295b8be8798e7b`；没有上传、分块或提交 Git。该恢复批次公开归档 481 个元数据、脚本和请求回执，约 6.28 MB。仅已完成审查确实引用的 21 份历史正文选择性归档或复用已有归档；未审整批正文保持 local_cache_only。归档映射不会把本地快照或正文路径伪装成公开文件。

旧 10 项外部阻塞经过 20 次免费重试仍未恢复；新增 3 项 DOI 阻塞单列：Financial RAG、Brain IoT、DRIP。ACM 正文返回 403；IEEE PDF 端点 HTTP 200 实为订阅元数据 HTML。Brain IoT 的原发表日保持 unknown，显示/插入日期与刊期分开。旧 issues #19、#20、#23、#30 的证据未变，逐项保留工件缺口，不强行关闭。

## 验证与费用

本地出版内容独立复审 68 项通过，37 个输入文件哈希保持；初稿对首页额外 URL 字段的严格对象比较失败与后续修正均留档。旧 18 个 HTML 页只更新共用导航，正文保留；11/11、11/12 的旧刊及旧审核单已归档。README 手写部分、周刊与卡片保持。不能声称所有旧 HTML 整页字节不变。

本阶段完整本地测试 430 项通过（85.79 秒）；新增归档后仓库路径检查 1 项通过。114 篇/9 路线校验、三张日期审核单、9 条摘要数字 guard、904 份原始文件哈希与私密值扫描、构建幂等均通过。结果记录在 `publication-static-checks.json`，并以出版 PR 的真实 CI 为准。此前来源阶段完整测试曾出现 429 通过、1 项本地路径规范化失败，修复后定向检查通过；没有把初次运行改写成全部成功。

DeepSeek 本轮生成请求 0、token 0，真实 usage 日志起止均为空。起止余额请求均 HTTP 200，观察到账户余额下降 0.21 元；这不是本任务发票，不能把账户差额归给本轮，也不包含 Codex 本身的用量。私密余额原值与密钥没有提交。

11/05 旧质量评测仍为 incomplete，recall 0.892857 小于 0.90 阈值；没有重测、降低阈值或将工程检查替代模型评测。依 owner 11/05 更新的授权，该全局告警不单独阻断逐篇核验内容与真实简报。`feed-daily.yml`、`feed-eval.yml`、`feed-publish.yml` 保持手动禁用。

可恢复入口：`backlog-audit/post-review/summary.json`、原始压缩台账与逐项任务见 `publication-archive-index.json`；独立审查见 `independent/completed-handoff-index.json`；日期合并凭据见 `publication-generation.json`。最后部署结果与所有开放 PR 的实时处置见 issue #60 的 2026-11-15 部署回执，不以本地 `published=true` 代替线上验证。
