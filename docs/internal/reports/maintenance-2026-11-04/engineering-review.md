独立工程复核：PR #35 大型日报审核文件读取

结论：通过。本次两文件差异未发现阻塞性缺陷。修复恢复大文件的完整内容读取，没有改变人工审批、质量校验或付费流程入口。此结论是本地工程复核，不代表 PR 已合并、CI 已重新运行或内容已获人工接受。

复核时间：2026-11-04T00:25:31.884023+00:00。基线 HEAD：`b199f393e0b11cbb7964163b8d2dac1372444bb4`。

复核范围：`scripts/feed/ci.py`、`tests/feed/test_ci.py` 的当前差异，以及 `pr35-read-failure.json`。调用链只读核对涉及同模块的 queue/check/publish、`scripts/feed/review.py`、`scripts/common.py` 和 `feed-review.yml`；没有改动这些文件。

- **根因与修复吻合。** PR #35 固定 head 为 `262a13f9e37771ba55627bdb18f8cb674793b302`，审核文件 `review/daily/2026-11-03.yaml` 大小为 1,503,947 字节。已存回执显示 Contents API 返回 `encoding=none` 和空 content；原代码因而解码出空文本。当前代码仅在该明确状态下，用返回的 `sha` 请求 Git Blobs API，再按原方式解码 UTF-8 内容。
- **引用没有漂移到分支最新版本。** `queue_daily_pr` 传入先前 PR 的 `headRefOid`；`check_pr` 传入已读取的 `pr.head.sha`。首个请求继续携带这个固定 ref，第二个请求使用该次 Contents 响应的 immutable blob SHA `f7023dde37b0b15c2124c60dd98e8e268f79104c`，没有改为默认分支或新查询的 head。
- **读取内容作为数据处理。** `remote_file` 只请求和解码文本。`check_pr` 在默认分支的可信代码中，仅落盘目标审核 YAML 或证据库 YAML，再调用原有校验；没有 checkout 或执行取回的 PR 脚本。`DataLoader` 继承 `yaml.SafeLoader`。新增分支不包含 eval、exec、shell、模块导入或 PR 代码执行。
- **审批与质量闸门未改。** AST 对比确认生产模块唯一改变的函数是 `remote_file`。`human_owner_review` 的人类 owner/exact-head 要求、`verify_merged_review` 的合并内容一致性检查、`validate_daily_review` 的来源哈希/窗口/Harness 判据等保持原样。完整读取并不使 `defer` 变成 `accept`；后续校验仍可能因真实审核或质量条件失败。
- **免费入口没有新增付费调用。** 此分支仅增加一次 GitHub 只读 GET。`check-pr` 和 `queue-daily-pr` 没有由该读取步骤转入 `FeedLLM`、judge、summarize 或 evaluate；review workflow 对应步骤未配置 LLM 密钥。既有 publication/evaluation 路径没有改动。本次复核未调用或启用工作流，未调用模型接口。

验证结果：

- `.venv/bin/python -m pytest -q tests/feed/test_ci.py`：**34 passed in 0.19s**。新增两例覆盖小文件直接读取和超过 1 MiB、`encoding=none` 后读取 blob；都要求内容逐字相同，并检查固定 ref、blob 路径和调用次数。既有测试覆盖 owner 审批、固定 head 的审核数据读取、拒绝 pending/无效数据、保留顺延决定以及不执行 PR 代码。
- 独立用本地 Git 对象复核实际 PR #35 blob：长度、Git SHA-1 和 SHA-256 均与故障回执一致。SHA-256 为 `ece8c803080e08ef24e98f7bf7894c8f1402a5fd68d7bd154bb87c4381a3ed92`。
- 对实际 1.5 MB blob 做离线模拟 API 往返，当前 `remote_file` 返回原始字节完全一致；安全 YAML 解析得到 `date=2026-11-03`、277 条 `defer`，没有改变决定。GitHub API 全部由 mock 提供，网络和付费调用均为 0。
- `git diff --check -- scripts/feed/ci.py tests/feed/test_ci.py` 通过。未重复跑全仓测试。

复核版本指纹：

| 文件 | SHA-256 |
| --- | --- |
| `scripts/feed/ci.py` | `5abc447aad996f1c2f63d972bc157c6b3cdbc8caf1ba52ad1ac2ba7f3ff94793` |
| `tests/feed/test_ci.py` | `8b037dab5748026a4e67ff98716efe33b4e610c39d551a91d20d367fa6f0113e` |

本次唯一新增文件为此复核报告；未写生产 canonical/state、未修改代码和测试、未提交或执行任何 GitHub 外部写操作。
