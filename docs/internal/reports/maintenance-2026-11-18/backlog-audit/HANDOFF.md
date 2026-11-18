# 11/18 historical backlog audit

This audit writes only its report and raw-evidence directories. It does not apply canonical decisions, merge pull requests, close issues, adopt new paper versions, or claim a deployment.

The current frozen stage is `post-review-v4/`: 9,052 stable IDs, including all previous 8,917 IDs; 2,222 canonical records; 4,844 current raw occurrences representing 4,572 distinct IDs. All current-window and observed HF board members/recommendation dates are represented. Existing `first_seen` values are unchanged. The 41 historical model-error records remain errors. Every ID now has a reason and recoverable status; 570 previously blank audit reasons were restored from their existing source-bound formal `review.note`, not newly invented or re-reviewed.

The four dated reviews have 177 application events covering 175 unique IDs. PR134 has 13 current reviews and 2 complete historical reviews; those two OpenAI announcements were subsequently rejected by PR135 and retain both real dated receipts. PR137 contributes 44 other IDs, PR135 applies 72 rows, and PR138 applies 46. All fields of each approved row were checked against either the current review or its preserved history, and every final review matches the last application. All 2,222 pre-apply source hashes and `first_seen` values remain unchanged. EGE keeps its complete original scientific approval; the additional Nov16 HF date has a separate exact-hash metadata receipt and does not rebind that old approval.

Canonical work buckets are 1,168 formal/catalog records, 913 reusable scope recommendations, 58 evidence follow-ups, 56 editorial tasks, 14 bounded source screens, and 13 external source blockers. The 6,830 noncanonical IDs consist of 6,363 outside the saved candidate windows and 467 with unavailable source dates. These are source-window dispositions, not paper-scope exclusions.

The 129 new canonical IDs comprise 110 papers and 19 posts: 6 daily accepts, 6 historical backlog inclusions, 112 rejects, and 5 item-specific deferrals. All 81 HF members (Nov16: 40; Nov17: 41) and their actual recommendation dates are present. The Nov15 rescan was empty. No new record lacks raw-source or issue evidence.

`STAGE-STATUS.md` identifies the superseded first baseline and the two corrected raw-only classifications. The frozen stages are retained byte-for-byte.

## Original PR135 queue

All 121 original `defer` rows are preserved before replacement, together with their original queue rows, current source snapshots, complete previous ledger rows, true owner receipt indices, and later corrections:

- `data/feed/raw/maintenance-2026-11-18/backlog-audit/pr135-original-v1.yaml.gz`
- `data/feed/raw/maintenance-2026-11-18/backlog-audit/pr135-historical-inventory-v1.jsonl.gz`, SHA256 `f7c62ada667da3c7fbfa121773967733084ec872067548b2c61f0d7a6012c74e`.
- `data/feed/raw/maintenance-2026-11-18/backlog-audit/pr135-carryforward-v1.jsonl.gz`, SHA256 `2d7eba15ab5c1457522a839f7c08837b2819b3d7589967355c84467faea8f16a`.

The prior scope advice is 45 include, 41 exclude, 14 bounded no-Harness-support screens, 9 boundary, 4 unknown, and 8 catalog-only records. This is not a new set of formal decisions. The carryforward file gives each item a specific reason, evidence reference, remaining editorial or source work, and issue reference. The 14 bounded screens must not all be described as full-text exclusions. The source-hash match flags for owner receipts are recomputed: 2610.27100, 2610.35077, and 2610.39714 no longer match those old approval hashes exactly.

`../historical-disposition/` owns the independent actionable decisions for this queue. Its final recommendations should supersede the carryforward work state only where the current source and dated review match.

Its `disposition-ledger-v2.jsonl.gz` is now consumed by the final audit. The 29 actionable historical dispositions were applied through the exact merged PR135: 19 backlog inclusions and 10 rejects. Their previous reviews remain in history; resolved editorial or approval steps are no longer presented as current blockers. The other 92 complete canonical review objects remain unchanged: 56 editorial tasks (25 inclusion preparation and 31 exclusion disposition tasks), 14 bounded screens, 8 existing catalog records, 3 artifact-evidence gaps, 7 scope-evidence gaps, 3 external access blockers, and 1 post-approval counterevidence case. They are not all external blockers and were not overwritten with fresh blanket defers.

## Version and source evidence

PR117 is a real owner merge (`c0d867e0a0d686ae5558edce401fb181895e4ee5`, head `dcc105663084e0148430d3e95af2fa81b0b58e9e`). Its actual merged input is `data/feed/raw/arxiv-version-check/2026-11-16.json`: 1,913 observations, of which 1,444 reuse an existing scientific-content task and 469 add a distinct task. The resulting version ledger has 2,096 tasks, preserving the old 1,627 and all 102 separate daily-metadata tasks. No new version is adopted by this audit.

The previous source recovery has 141 old/new body pairs and 196 targets whose original version identity remains unresolved. Fetching bodies did not complete their scientific comparison. Its previous throttling QA warning remains intact. The two fresh v2 readbacks for issues 115 and 116 verify identity and selected textual/table changes only; full independent version/numeric reviews remain pending.

The four long-running paper issues 19, 20, 23, and 30 have current abstract and full HTML bytes identical to the 11/15 snapshots, so their saved scope boundary reviews are reused without claiming a new full-paper review. Their specific artifact-version, admission, and later-consumption evidence gaps remain recorded.

All 13 blocked publisher sources were retried. None returned usable full text. CDST recovered an official abstract, authors and DOI; its first-online date and full-text scope evidence remain unresolved. Elsevier coredata JSON and IEEE subscription HTML are not full-text recovery.

## Merge and issue readbacks

PR134 is a real owner merge (`e6c3b8a7afd0810e968aed41d4ca1621b59bd599`, head `31e46a809ca2f542502d5e7174b5fade803e52a0`): 15 actual daily decisions, comprising 8 backlog, 6 reject and 1 defer. The separate 81-row exclusions file is not that 15-item decision set. Final application verification records 13 current objects plus 2 complete historical objects, as explained above.

At the fresh 02:37:39 UTC issue readback, all 22 original issues were still open. Issues 120, 121, 122, 125, 129, 130 and 132 have exact-source owner-merged reject decisions; 124 has an owner-merged accept decision and its Nov11 JSON and HTML publication were already verified live. Those 8 may be closed after the parent rechecks current state. Issues 123, 126, 127, 131 and 133 have valid inclusions and local publication artifacts; close them only after this publication PR, Pages deployment and exact-item live JSON/HTML verification. Issues 19, 20, 23, 30, 60, 115, 116, 119 and 128 retain their specific evidence/version work. No issue is closed by this audit.

The backlog evidence refresh made 68 free GETs (31 + 3 + 26 + 8). The pre-publication PR118 exact-head check added 2 free GETs, and the post-application issue readback added 1, for 71 in this audit work. There were no paid requests or GitHub mutations. Saved request receipts retain times, status and response hashes.

## Final application check

The completed invocation was:

```sh
.venv/bin/python docs/internal/reports/maintenance-2026-11-18/backlog-audit/reconcile-backlog.py --stage post-review-v4 --post-application
```

The script binds inputs by hash, preserves the complete original ledger and version tasks, verifies all 132 current adjudication hashes, and audits every application event against exact approved bytes and actual merged provenance. It reads the existing compression index and uses a durable gzip copy of the 2,093-record maintenance-start canonical snapshot, so its baseline is no longer only in `build/`. No input drift occurred. A later run must use a new immutable stage name. `post-review/` and `post-review-v2/` preserve checker failures; `post-review-v3/` has valid decision/count checks but is superseded by v4's completed reason fields. Final live publication validation remains a separate parent responsibility.
