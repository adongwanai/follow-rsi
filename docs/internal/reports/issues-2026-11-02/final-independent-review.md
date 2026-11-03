# 2026-11-02 集成改动独立复审

结论：本次检查范围内没有剩余阻塞问题。5 篇日报收录与 owner 实际合并的审核单一致，没有把未审核候选混入公开日报。已完成 85 项针对性测试。该结论不代表线上部署完成，也不代表全量模型评估闸门通过。

独立核验及测试执行于 2026-11-02；报告于 2026-11-03 补记。核验基准 HEAD 为 `513da4029b743886c38afa483185b77c88c18e1c`，分支为 `publish/recover-daily-2026-11-02`。本次恢复工作只整理已完成的检查及新增用量日志代码审阅，没有重读论文、重跑验收或调用付费模型。主任务负责后续集成、完整测试、构建和部署。

## 人工批准与审核单原文

通过 GitHub 只读查询核实，下面三项 PR 均由 `adongwanai` 合并，账号 `is_bot=false`。本地审核单字节与对应合并提交中的文件一致。

| 日报期次 | PR | 合并时间 UTC | 合并提交 | 决定数 |
| --- | --- | --- | --- | --- |
| 2026-10-28 | [#4](https://github.com/adongwanai/follow-rsi/pull/4) | 2026-11-02T08:36:55Z | `c158d28ad16b9f640f25ec965da49a765a5131be` | 1 accept / 48 reject / 1 defer |
| 2026-10-30 | [#11](https://github.com/adongwanai/follow-rsi/pull/11) | 2026-11-02T08:38:30Z | `209e4a20bc1f38e4d95d53e7f3788e28677a20ee` | 1 accept / 38 reject |
| 2026-11-02 | [#31](https://github.com/adongwanai/follow-rsi/pull/31) | 2026-11-02T08:39:54Z | `513da4029b743886c38afa483185b77c88c18e1c` | 3 accept / 12 reject |

审核单 SHA256：

| 源文件 | SHA256 |
| --- | --- |
| `review/daily/2026-10-28.yaml` | `6fb4a662b36e421fa0b0359bced6b1a4afc6abbd9bdb7b8513896fc0e49831d3` |
| `review/daily/2026-10-30.yaml` | `aadc6959191260863342f557d732684caf9332e78af574fbe0ff0ac0bfae86ae` |
| `review/daily/2026-11-02.yaml` | `aa9f9ac2c0d92a8ced744c0986ad3c8deaad538652fa4b6533d925b4adb10c62` |

对应回执位于 `data/feed/review-provenance/2026-10-28.json`、`data/feed/review-provenance/2026-10-30.json`、`data/feed/review-provenance/2026-11-02.json`；生成记录位于 `docs/internal/reports/publication-recovery-2026-11-02/publication-generation.json`。

## 日报内容与日期

三个 `site/daily/<date>.json` 的条目 ID 与已合并审核单中的 accept 集合精确相等。

| HF 推荐榜期次 | 论文 | 稳定 ID | 原发表日期 | 已核验版本日期 |
| --- | --- | --- | --- | --- |
| 2026-10-28 | The Trinity | `arxiv:2610.36077` | 2026-10-26 | 本表不补填 |
| 2026-10-30 | VibeGame | `arxiv:2610.33106` | 2026-10-22 | 本表不补填 |
| 2026-11-02 | RoboArchitect | `arxiv:2610.42141` | 2026-10-30 | 本表不补填 |
| 2026-11-02 | CEPO | `arxiv:2610.34722` | 2026-10-26 | 本表不补填 |
| 2026-11-02 | R²Orch | `arxiv:2610.22740` | 2026-10-15 | 2026-10-22 |

五条记录均保留与期次一致的 HF 日期及 `news_date`，均为 `window_status: in_window`、`review_decision: accept`。原发表日期没有被推荐榜日期覆盖。

三个期次各自的 `daily/<date>.md`、`daily/<date>.en.md`、`site/daily/<date>.html`、`site/daily/<date>.json` 共 12 个产物均存在且非空。生成器写入的 `published_at` 均为 `2026-11-02T08:41:08Z`；这是本地渲染元数据，不能作为线上部署成功的证明。

`site/feed/latest.json` 包含 21 条记录，即原有 16 条回顾记录和新增 5 条日报记录。`dates` 为 `2026-11-02`、`2026-10-30`、`2026-10-28`。已撤回的 10 月 27 日日报没有重新进入该日期集合；回顾记录独立保留，撤回页仍显示撤回。

## 数据完整性与候选隔离

- `data/feed/items.jsonl` 从 1317 条增至 1322 条，无删除。104 条既有记录只改变 `review` 字段：98 条从无决定变为 reject，5 条变为 accept，1 条变为 defer。既有 accept 未被覆盖。
- 新发现的 `2610.40191`、`2610.40684`、`2610.40721`、`2610.41210`、`2610.41216` 均未获得正式 `review`，没有伪造模型结果、评估闸门或标签。其来源为 `arxiv-candidate-issue`，HF 日期为空，均未出现在公开日报和 latest 输出中。
- `feed/eval/labeled.yaml` 从 107 条增至 210 条。新增 103 条为 owner 审核的 98 个 exclude 和 5 个 include，均附实际合并来源；旧标签未删除或改写，defer 没有转成评估标签。
- `data/papers.yaml` 中全部 107 条既有论文记录保持原样，包括原始事实和数字。新增 7 条均为 `section: candidates`、`status: candidate`、待读全文，证据字段保持 `unknown`。
- 新目录 ID 为 `feed-2610-36077`、`feed-2610-33106`、`feed-2610-42141`、`feed-2610-34722`、`feed-2610-22740`、`sceneevolve`、`ruharness`。后两项是历史范围审核候选，没有当作今日新论文。
- 总目录数从 107 增至 114，候选从 6 增至 13；正式收录仍为 101，方法和研究类数量未被候选抬高。`PAPERS.md` 如实标注候选及待核验状态。

目录集成依据保存在 `docs/internal/reports/issues-2026-11-02/catalog-and-source-integration.json` 和 `docs/internal/reports/issues-2026-11-02/historical-catalog-candidates.yaml`。

## README、笔记与分享图

去除 AUTO 生成区块后，`README.md` 和 `README_en.md` 与基准 HEAD 中的手写内容逐字节一致。公开论文数据中，既有条目唯一变化为 HarnessPro 的 `note_url`。

`notes/harnesspro.md` 与已独立审查的 `build/issues-2026-11-02/harnesspro-note.md` 逐字节一致，生成页 `papers/harnesspro.md` 包含同一笔记。笔记保留 +2.0 个百分点和 26.1% 的原始数字，明确 v2 日期为 10 月 20 日，并说明等权基准平均与执行 token 费用的边界。版本核验见 `docs/internal/reports/issues-2026-11-02/harnesspro-version-audit.json` 及同名 Markdown 报告。

七个新增目录 ID 对应的 `site/cards/<id>.png` 均已生成。已目视检查 `site/og.png`、`site/cards/sceneevolve.png`、`site/cards/feed-2610-22740.png`：候选/待核验标记、未知证据、真实仓库地址及二维码齐全，未发现阻塞性截断或布局问题。

非阻塞显示问题：此前 R²Orch 分享图和 README 展示原始 TeX `R$^2$Orch`。主任务负责显示层修正；无需改写论文规范标题。本报告不提前宣称该后续修正已验收。

## 来源健康与故障保留

审阅了 `scripts/feed/health.py`、`scripts/feed/fetch_arxiv.py`、`scripts/feed/digest.py`、`scripts/verify_site.py` 及对应测试。修复把成功的空结果识别为健康；实际失败或 degraded 连续出现仍触发告警；辅助 `arxiv-hydration` 的恢复可被处理；已禁用的注册来源不会被错误处理。完整 arXiv ID 在请求前校验。RSS 解析器已有 `feed.version` 检查，没有把任意 HTTP 200 HTML 当成合法空 RSS。

核对了 11 份已保存在线响应的 SHA256 与回执，全部匹配，HTTP 状态均为 200：Weco 两个入口、配置的全部 8 个 GitHub 仓库及一次 arXiv hydration 请求。完整请求时间、URL、响应路径和哈希见 `docs/internal/reports/issues-2026-11-02/source-health.json`。

| 响应文件，均位于 `build/issues-2026-11-02/` | SHA256 |
| --- | --- |
| `weco-live-0.xml` | `faae35fcb0b38379bc4dcd784fcaa9d097fedd90f6e5014701625b52cbc426f7` |
| `weco-live-1.xml` | `23376b40777f50bae65c95d0b35dd5086ef2e1913928940cfda27ccf926663e7` |
| `github-releases-live-0.json` 至 `github-releases-live-5.json`，以及 `github-releases-live-7.json`，共 7 份空列表 | `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570` |
| `github-releases-live-6.json` | `3b2795c20501f7751d595ae5ff556caa1afb1543ec305cb6afbc0002bf29555c` |
| `arxiv-hydration-live.xml` | `9fde1161d1d430cb74d552f213545956d11814d1120c6d143fce6f78b5ff9ddb` |

Weco 返回 13 条历史记录，当前窗口内 0 条；8 个 GitHub 仓库均成功响应，当前窗口内 0 条；arXiv 两个有效 ID 均返回。成功空窗没有被充作当天新增。

`site/feed/status.json` 保留待关闭告警 #10（arxiv-hydration）、#9（github-releases）、#8（rss-weco）。本复审未执行远程关闭。集成记录见 `docs/internal/reports/issues-2026-11-02/source-health-integration.json`。

S2 authors 的 HTTP 429 仍作为真实故障保留：`last_ok=false`，`consecutive_errors=2`，没有伪称该来源恢复。

## 历史排除回执的纠正记录

此前发现新增两条历史排除回执时需要区分原批准记录与事后补记。该问题已通过明确的 `post_approval_corrections` 和 `approval_reconciliation` 解决。

- `arxiv:2610.39352` 对应 issue #21，源内容哈希为 `b487368b6e5041740927cb95daa33fc8069d59ca69803874c05333c5bd9b5eba`。
- `arxiv:2610.38728` 对应 issue #24，源内容哈希为 `bf8f2be86f4de5ed33523a1f24f7444cc672dccdf18be3fdcffef51d457384f5`。
- 原批准记录时间 `2026-11-02T07:48:08+00:00` 保留；纠正时间为 `2026-11-02T09:10:13.886303+00:00`，动作标为 `restore_omitted_historical_exclusion`。
- 原 `approved_exclude=396` 与纠正后 `398` 分别记录，并链接已有 11 月 1 日、10 月 31 日证据报告。这次补记不新增正例，也不声称模型闸门通过。

完整记录见 `docs/internal/reports/issues-2026-11-02/historical-approval-reconciliation.json`。本轮来源追溯问题已解决。

## 排序依据

撤回最初对倒序的疑问。owner 后续的 `CODEX_PROMPT_FIX_AUDIT.md` 第七节明确要求：日报按分类分组，组内最新在前；latest items/weeks/dates 和 Atom 最新在前；日报首页指向最新一期；论文库默认必读优先，再按最新排序，保留最早优先选项。当前排序符合这份后续要求，不作为缺陷。

## 新增 LLM 用量日志只读审阅

快速审阅了 `scripts/feed/llm.py` 和 `tests/feed/test_llm.py` 的新增 diff，未发现阻塞缺陷。未执行付费调用，也未在本复审中运行新增日志测试。

- `FeedLLM.record_usage` 将实际 API 调用结果追加至 `data/feed/usage.jsonl`，记录 UTC 时间、stage/model/provider/item_id/cache_key/attempt、SDK usage、请求及响应 ID、错误类型和 HTTP 状态。
- 不记录提示词、模型正文、API 密钥或错误消息原文。无 usage 时记录 null，不伪造零消耗。
- 缓存命中在传输和日志之前返回；schema 重试分别记录各次真实调用；402 仍终止批次，不转成成功缓存或审核标签。
- 进程内锁覆盖既有线程池并发追加。新增测试覆盖 usage 有/无、缓存命中、8 线程、schema 重试和错误脱敏；本报告仅确认这些测试的代码存在，不报告其运行通过。

## 已执行验证与结论边界

2026-11-02 已实际运行：

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest tests/feed/test_health.py tests/feed/test_sources.py tests/feed/test_digest.py -q -p no:cacheprovider
```

结果：**85 passed in 13.60s**，退出码 0。`git diff --check` 当时亦为退出码 0。报告补记时未重复运行。

GitHub 只读查询确认 `.github/workflows/feed-publish.yml` 当时仍为 `disabled_manually`，其他工作流 active；所审 diff 没有修改工作流，本复审没有恢复自动发布。

完整测试套件、build 幂等、浏览器验收和新增日志测试由主任务负责，本报告不冒认执行。未独立核验当前线上部署，未调用全量付费模型评估，未宣称全局 evaluator 或质量闸门通过。复审期间没有提交、推送、合并、发评论或关闭 issue。
