# METR post identity correction

All changes in this folder are proposals or isolated verification. This worker did not write production, call a model, or execute commit/push/GitHub actions.

## Apply the narrow data correction

From the repository root:

```sh
.venv/bin/python -B build/maintenance-2026-11-07/metr-identity-fix/apply-correction.py
.venv/bin/python -B build/maintenance-2026-11-07/metr-identity-fix/apply-correction.py --apply
```

The script validates both records and the exact raw response before writing. It changes only `arxiv:2511.19492`, adds the real METR post, and archives the correction receipt. It does not edit source state, other records, daily-review files or historical publication manifests.

- Historical paper remains **Forecasting AI Time Horizon Under Compute Slowdowns**, published `2025-11-23T10:46:10Z`, with `backfill_only=true` and its original `first_seen`. Its misleading `links.post` is removed. The article URL, title and date move into `discovery_referrers[url]` with `relation=cited_by_post`, exact RSS SHA-256 and `/rss/channel/item[2]`. The article's `source_published` is removed from the paper's top level. Corrected `source_hash`: `4366a4d9fc7c8f068ecbcb34d1f12274521a2683400789d70e335c90b813dd56`.
- New identity: `post:https://metr.org/blog/2026-11-05-anthropic-ai-rd-acceleration-assessment/`. Title **Independent Assessment of AI R&D Acceleration at Anthropic in October 2026**. The original RSS `Thu, 05 Nov 2026 00:00:00 -0800` becomes `2026-11-05T08:00:00+00:00`; actual `first_seen` remains `2026-11-07T00:08:00.116833+00:00`. Its own text is retained once; references `2609.36054` and `2511.19492` are explicitly references. `source_hash`: `147cb0b7cbddc4b5aec775c83705a1585d0b39b9de58231429302d755defe9db`.

The original 59-item source increment becomes 60 discovered canonical additions after recovering this missing post. The archived collector counts remain a record of the original parser output. This correction does not silently rewrite those raw receipts or pretend an additional network request occurred. Do not replay the original full source-delta importer after this correction; its content-drift guard should reject the superseded paper record.

## Apply the prospective parser fix

```sh
git apply --check build/maintenance-2026-11-07/metr-identity-fix/rss-identity-code.patch
git apply build/maintenance-2026-11-07/metr-identity-fix/rss-identity-code.patch
.venv/bin/python -B -m pytest tests/feed/test_sources.py tests/feed/test_storage.py -q
```

The patch touches only `fetch_rss.py`, `normalize.py`, `dedupe.py` and their existing two test files. It does not migrate historical records.

The root cause was `fetch_rss.parse_feed`: when any arXiv identifier appeared in the RSS entry link or body, it produced a paper record for **every** identifier and suppressed the actual post. It used the blog's title and `links.post` for each cited paper. `normalize_record` then correctly assigned each supplied arXiv identifier a paper identity; the mistake was the RSS inference before normalization. This is not a first-link-only bug.

The fix always retains an ordinary webpage's post identity. Body citations remain separate metadata-pending paper discoveries with explicit `discovery_referrers`, without assigning the blog title or `links.post` to those papers. A direct arXiv RSS entry uses only its own URL identifier. Deduplication adds referrer URLs while retaining the first recorded evidence for an existing URL.

The real historical METR entry **Frontier Risk Report (February to March 2026)** contains the redacted strings `https://[redacted]` and `https://api.[redacted]`. When newly retaining that post, the existing code-link scanner raised `ValueError: Invalid IPv6 URL`. The patch catches only URL parsing `ValueError` at that external-text boundary, emits a warning, skips only the malformed URL candidate, and retains the article and valid code links.

Verification: `78 passed in 0.30s` in the isolated code copy; `git apply --check` passed. Replaying the complete saved METR feed produced 256 normalized records, retained the redacted-URL post, emitted two warnings, and reproduced the real recovered post's date and source hash. The two-record data correction produced 1808 → 1809 records in the isolated data copy; a second apply was byte-identical. Evidence is in `verification.json` and `real-rss-code-verification.json`.

## Scope handoff

`nov05_backlog` read the official RSS full text, including methods, limitations, interviews and the AEF appendix, saved at `other-source-review-sources/02-rss-source.txt`. Its preliminary advice is to exclude the real post from the current Harness scope (`ai4ai` / `evaluation_benchmark` / `safety_governance`); discussion of agent scaffolds does not establish persistent feedback-driven Harness evolution. It separately recommends excluding the historical paper as `theory_survey`. These are preliminary suggestions, not formal decisions; this correction writes no review decision.
