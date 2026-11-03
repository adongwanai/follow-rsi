# 来源健康 issue 核查（2026-11-02）

基线：`8fe1ba4a8c8bee4077fe0d13c10d33bca4a491b0`。本代理未切换分支、未改生产文件、未写 GitHub；修改只保存在忽略的快照和补丁中。

| Issue | 当前来源事实 | 结论与处理 |
| --- | --- | --- |
| [#8 rss-weco](https://github.com/adongwanai/follow-rsi/issues/8) | 08:37 UTC 重试官方 `www` 与裸域，DNS 成功，两次 HTTP 200；有效 RSS 2.0，各 13 条；最新日期 2026-07-14，近期 0 条 | 来源健康，原告警是“成功空窗”被计作故障。修健康统计，保留来源。 |
| [#9 github-releases](https://github.com/adongwanai/follow-rsi/issues/9) | 08:38 UTC 用既有 gh 凭据只读重试配置中的全部 8 仓库：8/8 HTTP 200；7 个空列表；Agent-S 12 个历史发布、最新 2025-12-16；近期合计 0 | 空 release 列表有效，不能按 outage 计数。今日早些时候的匿名 403 已通过凭据重试恢复；没有暴露或存储令牌。 |
| [#10 arxiv-hydration](https://github.com/adongwanai/follow-rsi/issues/10) | 08:41 UTC 实际请求原报错批次中两个合法 ID，HTTP 200、返回 2/2 对应记录 | SEC `data/1526520` 误识别已由 PR #3 的合法旧归档白名单修复，已有回归测试。旧 issue 仍开着还有辅助源健康状态未参与收尾的原因。 |

最小补丁在 `build/issues-2026-11-02/source-health.patch`：

- HTTP/解析成功且未降级即视为健康，即使近期条目数为 0；开故障单依据真实 error/degraded 连续次数。
- 真实 HTTP/DNS 错误、RSS/API 降级、两天未运行仍保留告警，不隐藏失败。
- 为未单列在来源注册表但实际有记录的辅助源（例如 arxiv-hydration）处理故障及恢复；不对辅助阶段伪造每日必须单独运行的规则。
- `fetch_ids` 在发请求前验证完整 arXiv ID。`data/1526520` 等非法值直接抛错，零网络调用；合法现代 ID、旧格式和版本号仍可用。这个补强不重写已合并的正则修复。

验证：在从基线归档出的隔离快照中运行 `.venv/bin/python -m pytest tests/feed/test_health.py tests/feed/test_sources.py -q`，**62 passed in 0.81s**。测试覆盖成功空窗、真实失败、降级仍报错、辅助源恢复与刷新、非法 ID 请求前拒绝以及 RSS HTTP/DNS 错误传播。实时来源响应和哈希见 `source-health.json` 及 `build/issues-2026-11-02/*-live*`。

当前这三条没有外部阻塞。待主线程应用和集成验证后，可用上述证据处理三个旧 issue；本代理没有评论、关闭 issue 或部署补丁。
