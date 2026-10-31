# 2026-10-31 维护与同步记录

本次交付是已完成结果及可续跑清单，不是日报发布。规范记录现为 **1,206 条 = 冻结的 1,139 条 + 新增 67 条**。新候选中 37 篇完成三轮范围审查，建议 Harness 纳入 5、排除本专题 30、边界待审 2；另外 21 篇 S2 论文和 9 条公告尚未完成范围审查。所有新正式决定为 `defer`，新增发布为 0。

## AgentGuide 引流已上线

[AgentGuide PR #173](https://github.com/adongwanai/AgentGuide/pull/173) 已合并，四项 CI 通过。在 README 的介绍、快速导航及研究前沿页补入 Follow RSI 的网站、仓库和深度文章入口；合并提交为 `9a68e14bb4e44275c6e144b2e2c86ff4b02457ac`。[上线回执](agentguide-sync.json)

[《为什么 AI 还不会自我进化》](https://adongwanai.github.io/follow-rsi/articles/why-ai-self-improvement.html) 此前已经单独发布，本次没有重复发布。

## 推荐日与采集结果

本次采集于 UTC 03:52–04:03 完成。HF **10 月 31 日**接口返回 HTTP 200、空列表；这只证明抓取时当日榜为空，不能推导为“所有来源均没有合格论文”。HF **10 月 30 日**榜扩为 39 篇，比此前已看过的 16 篇多 23 篇；这些是前一日后补，仍归 10 月 30 日，不作为 10 月 31 日推荐。

所有 12 路启用来源均实际尝试：8 路主请求成功，4 路失败。表内数为该源返回或关键词预筛后的命中数，既非新增去重数，也非 Harness 收录数。

| 来源 | 返回或预筛命中 | 本次状态 |
| --- | ---: | --- |
| HF Daily Papers | 21（另保留完整 39 篇前日榜） | 主请求成功；当日 0；arXiv 元数据补全 429 |
| arXiv Harness | 0 | HTTP 429 |
| arXiv RSI | 0 | HTTP 429 |
| arXiv adjacent | 0 | 请求超时 |
| Semantic Scholar citations | 1,454（源内去重 654） | 成功 |
| Semantic Scholar authors | 0 | HTTP 429 |
| RSS Sakana | 6 | 成功；arXiv 元数据补全 429 |
| RSS METR | 2 | 成功；arXiv 元数据补全 429 |
| RSS OpenAI | 40 | 成功 |
| RSS DeepMind | 3 | 成功 |
| RSS Weco | 0 | 成功、空结果 |
| GitHub releases | 0 | 成功、空结果 |

[逐路开始/结束时间与失败原因](source-attempts.json) · [来源健康](source-health.json) · [本轮计数](intake-summary.json)

## 三轮结果及更正

37 篇来自 23 篇 HF 后补与远端 main 新增 20 篇的并集，重叠 6 篇。第一轮核对官方身份、首发日、版本日与摘要；主审对 18 篇查正文相关段落，独立审查对 13 篇查正文相关段落。独立结论在看到主审建议前冻结，再逐项对照。范围审查不等于完整实验复现或四项证据卡审完。

- **建议纳入 5 篇**：FilingLoop、SkillCompiler（Compile Away Uncertainty）、Before the Next Rollout 三篇方法，以及 Masked Erosion、Appreciation Teaches Unauthorized Execution 两篇 Harness 专项安全评测。
- **边界 2 篇**：KARMA、MoLRSI。KARMA 初审把“接口允许修改角色/协议”推成“实际修改已被接纳”，复看 Figure 5 后收回：展示的 E17–E19 属于 experience 模块，未证明角色/协议的实际变更。初审、冻结意见、更正均保留。
- **本轮不纳入 Harness 30 篇**：包含通用 RSI、权重训练、静态框架、单任务产物等；不等于都不属于 RSI。
- SkillCompiler 开发时检查过 held-out failure，限制已显式保留，不能把该留出集视为完全未触及的独立确认。

[37 篇 owner 候选单](owner-candidates.yaml) · [主审最终报告](primary/review-reconciled.json) · [纠正依据](primary/round-3-reconciliation.md) · [独立对照](independent/comparison.md) · [主审核验](primary/verification.json) · [独立核验](independent/comparison-validation.json)

原 1,139 条的题名、摘要、发表和版本日期、owner 决定、模型输出、摘要及证据字段均未覆盖。仅对新增 37 个 ID 填入已核实的官方元数据，逐字保留原摘要及数字，并保留改动前来源观测。示例 `2609.05881`：官方首发 9 月 5 日、v2 为 10 月 25 日、v3 为 10 月 29 日，HF 推荐日为 10 月 30 日；这些日期各自记录。

[合并及保留字段](integration.json) · [官方元数据集成回执](metadata-integration.json) · [官方元数据与日期证据](primary/official-metadata.json) · [集成前新条目快照](new-intake-before-metadata.jsonl)

## 尚未完成的部分与续跑

新增 67 条全部有状态、来源、建议或明确待补原因：[逐 ID 清单](new-item-status.jsonl)。其中 21 篇额外 S2 论文仅完成采集核对，没有冒充三轮审完；20 篇有来源摘要，1 篇无原始摘要且来源报告未来发表日 **2026-12-01**，保留原值并标为待核实。9 条新公告仍待官方正文和范围审查。[S2 清单](s2-additional-intake-audit.md)

全量旧积压见[冻结覆盖报告](../maintenance-2026-10-30/coverage/README.md)。冻结的 1,139 条都有处理状态，但只有其中 **163 条**达到三阶段记录且输入匹配，不能说全量三轮已完成。独立优先复审包覆盖 199/199 个范围内正例或边界、211/211 个扩展优先项；它与三阶段匹配数使用不同口径。

待续跑任务按阶段列出，彼此有重叠，不能直接相加：

| 阶段 | 条数 | 说明 |
| --- | ---: | --- |
| 旧批次论文双语摘要 | 369 | HTTP 402 后暂停，已有成功结果保留 |
| 模型接口错误 | 31 | 旧批次 11 + 远端 main 已存在的 20；后者为 relevance APIStatusError，非本轮新调用 |
| 旧批次原始摘要补证 | 9 | 8 条出版访问阻塞、1 条 IEEE editorial 无摘要，已有正文不替代原摘要 |
| 旧批次公告摘要 | 1 | Terminal X，独立公告处理路径 |
| 旧批次来源版本或文本对照 | 73 | 逐项核对后才复用旧审查 |
| 旧批次选中项补独立来源审查 | 164 | 未用统一 defer 隐藏未处理工作 |
| 新论文规范分类 | 57 | 58 篇中除 1 篇缺原始摘要；含上述远端 20 个失败项 |
| 新 S2 范围审查 | 21 | 与 57 篇规范分类任务重叠 |
| 新公告正文审查 | 9 | 尚未完成 |
| 新元数据补证 | 1 | 上述未来日期、缺摘要条目 |

[当前续跑计划](resume-plan.json) · [离线准备脚本](prepare_resume.py) · [离线准备核验](resume-verification.json)

离线校验不会调用模型：

```sh
python docs/internal/reports/maintenance-2026-10-31/prepare_resume.py
python docs/internal/reports/maintenance-2026-10-31/prepare_resume.py --queue resume_summary --workdir build/resume-summary-next
```

另可选择 `retry_model_api` 或 `classify_new_papers`，必须使用新的 build 子目录。脚本核对原始输入和 owner 状态后复制独立队列及缓存，不改 canonical、不联网。余额可用后才在准备目录运行现有 `scripts.feed.cli` 的 `judge` 或 `summarize` 阶段；输出须另行审核、核对并集成，脚本不接受、不合并、不发布。

## 审核单与发布边界

生成并校验 [10 月 31 日正式待审单](../../../../review/daily/2026-10-31.yaml)：**218 篇论文 + 74 条公告 = 292 条，全部 defer**。这是滚动待审集合，不是 292 条今日新增。生产队列仅使用 canonical 中已有分类；没有规范分类的项目与代理给出的正文建议单独保留在 67 条清单和 37 条候选单，绝不伪造成付费模型成功输出。`defer` 保存在待审单和建议清单；新增 canonical 项尚无 owner review，未伪造人工裁决。[队列核验](queue-verification.json)

PR #3 仅同步待审结果和修复，不自动合并。`feed-publish.yml` 仍手动禁用。旧 trusted-main 的 105/107 题名身份问题，与新 45 例完整闸门结果是两项问题：后者 **precision 0.9231、recall 0.8571 < 0.90，质量未达标**，本次没有再次付费评测，也没有放宽阈值。[45 例完整评测](../maintenance-2026-10-30/harness-gate-eval/gate-report.md)

最终测试、幂等构建、README 手写区保护与凭据检查见 [validation.json](validation.json)。公开日报、Atom 及 latest 不因本次待审队列生成而新增内容。
