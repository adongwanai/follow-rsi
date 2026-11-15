# 2026-11-15 历史版本正文恢复

本次源文件恢复覆盖冻结清单的 337 项；其中 337 项明确版本请求/缓存处理完毕，0 项尚未处理。

- 实际免费 HTTP 请求：461；HTTP 状态：{'200': 448, '404': 13}。
- 有效正文响应：448；新增恢复版本：448；缓存复用版本：30。
- 141 项明确原版/目标版本中，141 对正文已齐；失败版本 0，尚未尝试的明确版本 0。
- 单边正文已恢复的条目：196；其中原版身份未知但目标正文已恢复：196。
- 196 项原始版本身份仍未知；这些条目的目标版本状态见 missing-original-version-identity.json，不假定原版为 v1。
- backlog 子任务已离线复核这 196 项的原始 source_hash 与 223 条 HF 成员/摘要命中，但 0 条具有明确版本字段或带版本 URL；因此它们是身份证据缺口，不是未开展原始来源核对。回执哈希见 original-version-identity-audit-reference.json。
- 既有 10 对正文未重复请求；所有成功必须有完整 arXiv article 与对应页面 watermark，或有效指定版本 PDF（详细版本绑定方式逐项保留）。HTTP 200 元数据页不算正文。
- 全局停止原因：none。
- 节流审计：目标仍为 3.2 秒，实际记录的最小间隔 3.1886705 秒，5 个间隔未达到目标；该检查明确保留为失败告警，all_checks_passed=false。请求前日志与限流参考计时点不同，不能据此声称精确的网络发出时刻。所有前请求完成均早于下一请求记录；不重写历史日志或降低目标。
- 原文字节包：version-source-bodies.tar.gz，177212761 字节；展开成员 1431 个，共 455138209 字节。逐成员解包 SHA-256 校验通过，索引见 body-archive-members.json。
- 正文与提取文本、完整 tar.gz 均为 local_cache_only，留在忽略的 build 目录，不是公开附件，也未额外分块。仓库最小归档仅含逐项官方 URL/版本/原始 SHA、请求回执、提取结果索引、冻结核验和本地包 SHA，见 minimal-publication-files.json。
- 本恢复批次 0 项完成实质正文审查，因此本目录没有可自动纳入公开证据的整批正文。正式纳入或实质版本审查确实引用的正文，由整合方按相应完成审核单选择性归档并保持原始字节及 SHA。
- 0 付费调用，0 canonical 修改，0 新内容审查完成，0 正式版本采用。

恢复正文仅让后续版本对照成为可能。必须另行完成变更段落/表格/数字核对与独立范围复审；本目录不改变原先审核或发表结论。

交接入口：progress.json、recovery-accounting.json、recovery-state.json、recovered-version-pairs.json、missing-original-version-identity.json、request-failures.json、not-yet-attempted-known-versions.json、requests.jsonl、recovery-qa.json。
