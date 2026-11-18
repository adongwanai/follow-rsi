# 11/18 historical backlog audit

This audit writes only its report and raw-evidence directories. It does not apply canonical decisions, merge pull requests, close issues, adopt new paper versions, or claim a deployment.

The current frozen stage is `post-intake-v2/`: 9,052 stable IDs, including all previous 8,917 IDs; 2,222 canonical records; 4,844 current raw occurrences representing 4,572 distinct IDs. All current-window and observed HF board members/recommendation dates are represented. Existing `first_seen` values are unchanged. The 41 historical model-error records remain errors.

`STAGE-STATUS.md` identifies the superseded first baseline and the two corrected raw-only classifications. The frozen stages are retained byte-for-byte.

## Original PR135 queue

All 121 original `defer` rows are preserved before replacement, together with their original queue rows, current source snapshots, complete previous ledger rows, true owner receipt indices, and later corrections:

- `data/feed/raw/maintenance-2026-11-18/backlog-audit/pr135-original-v1.yaml.gz`
- `data/feed/raw/maintenance-2026-11-18/backlog-audit/pr135-historical-inventory-v1.jsonl.gz`, SHA256 `f7c62ada667da3c7fbfa121773967733084ec872067548b2c61f0d7a6012c74e`.
- `data/feed/raw/maintenance-2026-11-18/backlog-audit/pr135-carryforward-v1.jsonl.gz`, SHA256 `2d7eba15ab5c1457522a839f7c08837b2819b3d7589967355c84467faea8f16a`.

The prior scope advice is 45 include, 41 exclude, 14 bounded no-Harness-support screens, 9 boundary, 4 unknown, and 8 catalog-only records. This is not a new set of formal decisions. The carryforward file gives each item a specific reason, evidence reference, remaining editorial or source work, and issue reference. The 14 bounded screens must not all be described as full-text exclusions. The source-hash match flags for owner receipts are recomputed: 2610.27100, 2610.35077, and 2610.39714 no longer match those old approval hashes exactly.

`../historical-disposition/` owns the independent actionable decisions for this queue. Its final recommendations should supersede the carryforward work state only where the current source and dated review match.

## Version and source evidence

PR117 is a real owner merge (`c0d867e0a0d686ae5558edce401fb181895e4ee5`, head `dcc105663084e0148430d3e95af2fa81b0b58e9e`). Its actual merged input is `data/feed/raw/arxiv-version-check/2026-11-16.json`: 1,913 observations, of which 1,444 reuse an existing scientific-content task and 469 add a distinct task. The resulting version ledger has 2,096 tasks, preserving the old 1,627 and all 102 separate daily-metadata tasks. No new version is adopted by this audit.

The previous source recovery has 141 old/new body pairs and 196 targets whose original version identity remains unresolved. Fetching bodies did not complete their scientific comparison. Its previous throttling QA warning remains intact. The two fresh v2 readbacks for issues 115 and 116 verify identity and selected textual/table changes only; full independent version/numeric reviews remain pending.

The four long-running paper issues 19, 20, 23, and 30 have current abstract and full HTML bytes identical to the 11/15 snapshots, so their saved scope boundary reviews are reused without claiming a new full-paper review. Their specific artifact-version, admission, and later-consumption evidence gaps remain recorded.

All 13 blocked publisher sources were retried. None returned usable full text. CDST recovered an official abstract, authors and DOI; its first-online date and full-text scope evidence remain unresolved. Elsevier coredata JSON and IEEE subscription HTML are not full-text recovery.

## Merge and issue readbacks

PR134 is a real owner merge (`e6c3b8a7afd0810e968aed41d4ca1621b59bd599`, head `31e46a809ca2f542502d5e7174b5fade803e52a0`): 15 actual daily decisions, comprising 8 backlog, 6 reject and 1 defer. The separate 81-row exclusions file is not that 15-item decision set. Apply verification belongs to the final stage.

Existing issues 122, 129 and 130 have exact-source owner-merged reject decisions; 124 has an owner-merged accept decision and its 11/11 JSON and HTML publication were verified live. These can be closed after the parent rechecks their current issue state. SciMARS, JoMoHa and TRUST have formal backlog receipts, not proof of publication. No issue is closed by this audit.

The backlog evidence refresh made 68 free GETs (31 + 3 + 26 + 8), no paid requests and no GitHub mutations. The four request receipts retain times, status and response hashes.

## Final application check

After the parent applies current dated reviews, run the following with a new immutable stage name:

```sh
.venv/bin/python docs/internal/reports/maintenance-2026-11-18/backlog-audit/reconcile-backlog.py --stage post-review
```

The script binds inputs by hash, preserves the complete original ledger and version tasks, verifies current adjudication hashes, and audits every PR134 decision against its actual merged provenance. A concurrent input change fails the stage; preserve it and rerun with a new name. Final live publication validation is a separate parent responsibility.
