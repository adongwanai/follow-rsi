# 15 篇晚到 HF 论文的官方日期与版本核对

官方查询：2026-11-05T07:46:14.460170+00:00，HTTP 200，单个批量请求返回全部 15 个 ID。

HF 推荐日、HF paper/record reported 时间、arXiv Atom published（首次提交）与 updated（最新版本提交）分别保存；没有从编号、HF日期或未带版本的HTML URL推测官方日期或版本。

官方 Atom SHA256：`d0ebc3afa79fbeadf06bed2299f489d3a757ac9f7c15fb440d16ec71ae333930`。所有版本号均来自明确带 vN 的 Atom entry id，并与解析记录核对。

| ID | arXiv 首次提交 UTC | arXiv 最新提交 UTC | 最新版 | HF paper reported 时间 |
|---|---|---|---:|---|
| arxiv:2611.06910 | 2026-11-04T18:56:22Z | 2026-11-04T18:56:22Z | 1 | 2026-11-04T00:00:00.000Z |
| arxiv:2611.06918 | 2026-11-04T18:59:58Z | 2026-11-04T18:59:58Z | 1 | 2026-11-04T18:59:58.000Z |
| arxiv:2611.05320 | 2026-11-03T18:25:14Z | 2026-11-03T18:25:14Z | 1 | 2026-11-03T18:25:14.000Z |
| arxiv:2611.06483 | 2026-11-04T13:24:54Z | 2026-11-04T13:24:54Z | 1 | 2026-11-04T13:24:54.000Z |
| arxiv:2611.01120 | 2026-10-31T17:08:13Z | 2026-10-31T17:08:13Z | 1 | 2026-10-31T00:00:00.000Z |
| arxiv:2611.06518 | 2026-11-04T13:43:09Z | 2026-11-04T13:43:09Z | 1 | 2026-11-04T00:00:00.000Z |
| arxiv:2611.06796 | 2026-11-04T17:14:20Z | 2026-11-04T17:14:20Z | 1 | 2026-11-04T00:00:00.000Z |
| arxiv:2611.03228 | 2026-11-02T14:48:09Z | 2026-11-02T14:48:09Z | 1 | 2026-11-02T00:00:00.000Z |
| arxiv:2610.41104 | 2026-10-30T00:50:49Z | 2026-10-30T00:50:49Z | 1 | 2026-10-30T00:00:00.000Z |
| arxiv:2610.40131 | 2026-10-29T14:22:51Z | 2026-11-03T14:34:07Z | 3 | 2026-11-03T00:00:00.000Z |
| arxiv:2611.06728 | 2026-11-04T16:16:27Z | 2026-11-04T16:16:27Z | 1 | 2026-11-04T00:00:00.000Z |
| arxiv:2611.06083 | 2026-11-04T07:25:06Z | 2026-11-04T07:25:06Z | 1 | 2026-11-04T00:00:00.000Z |
| arxiv:2610.40516 | 2026-10-29T17:26:02Z | 2026-10-29T17:26:02Z | 1 | 2026-10-29T00:00:00.000Z |
| arxiv:2611.05304 | 2026-11-03T18:16:29Z | 2026-11-03T18:16:29Z | 1 | 2026-11-03T18:16:29.000Z |
| arxiv:2611.05609 | 2026-11-03T20:53:26Z | 2026-11-03T20:53:26Z | 1 | 2026-11-03T00:00:00.000Z |

版本分布：v1 14 篇，v3 1 篇（VideoMemBench，arxiv:2610.40131）。

PyRUA 科学字段与旧 canonical 完全一致：False；first_seen 保留 `2026-11-05T03:16:28.653735+00:00`。
PyRUA HF title/abstract 与 canonical 一致：True / False。

records[].first_seen is the metadata-read timestamp supplied to the parser, not an authorized replacement for tracker first_seen. New late HF identities were observed at the source-specific actual_observed_at; preserve existing canonical first_seen for PyRUA.

本次补查 1 次免费 metadata API；晚到复核累计 1 次 HF + 2 次 arXiv HTML + 1 次 arXiv metadata = 4 次网络请求，全部 HTTP 200，付费调用 0。生产文件与 Git 状态未由本子任务修改。
