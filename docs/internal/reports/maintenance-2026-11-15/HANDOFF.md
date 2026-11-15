# 2026-11-15 source intake — frozen handoff

第一轮免费来源、身份、日期和原文归档已完成。此包没有范围接受意见，不是发表回执；父任务负责二/三轮审核及 canonical/PR/出版。

## Integration entry points

- Use `effective-integration-proposal.json` (SHA-256 `d4bc134d94281eb02d6f6c468a4265c44b2a493cb46795231f1ee47275af83d2`). It includes all 16 new records and 2 source-label updates, preserves raw S2 fields, and applies explicit publisher-metadata corrections only in the unapplied proposal.
- `source-evidence-index.json` (SHA-256 `6deef8cfe9544b30614c741b84ff3a57b7e4c2962fe626f3a10ecf713ca750ff`) binds every ID to source URLs, dates, raw body and text hashes, versions and limitations.
- `integration-proposal.json` is the unmodified discovery/official-arXiv proposal. Do not copy its three DOI date/author fields over the effective proposal.
- `candidate-records.jsonl` is a raw-source reconciliation view, not an integration input; it can contain S2 dates or stale RSS values.
- `doi-identity-date-audit.json`, `intake-qa.json`, `handoff-verification.json`, `hf-board-reconciliation.json`, `hf-board-source-delta.json`, `cache-reuse-audit.json`, `review-reuse-deltas.json`, `rss-date-evidence-reuse.json`, and `all-source-snapshot.json` retain the detailed evidence.

## Actual collection

- Actual run date is 2026-11-15. Baseline captured 02:34:16 UTC (10:34:16 Beijing); source collection began 02:34:18 UTC. This is not an 08:00 capture.
- Baseline: 2074 records, exact bytes SHA-256 `97f89d3f7a93e81c3606b45d998268fec0411a0231879cb723bf06e2011abd93`. Production bytes still match at freeze.
- All 12 enabled routes attempted: 98 recorded route requests; 10 routes completed without traversal error, S2 citations retained partial results and S2 authors exhausted its bounded attempt window.
- Raw responses: 5867 record occurrences / 5559 unique IDs. Configured window: 371 occurrences / 336 unique IDs. These window counts use the discovery sources as reported, before DOI date reconciliation.
- New canonical candidates: 16 (13 arXiv and 3 DOI-only papers), not 16 accepted or newly published papers. No new RSS post or release.
- Existing provenance updates: only `source_hits += s2-citations` for arxiv:2611.16409 and arxiv:2611.16009. No old science, first_seen, decision or source hash change is proposed.
- Identity collisions: 0. HF recommendation date additions: 0.

| Source | Outcome | Requests | Raw records | Window records |
|---|---|---:|---:|---:|
| arxiv-harness | ok | 1 | 0 | 0 |
| arxiv-rsi | ok | 1 | 0 | 0 |
| arxiv-adjacent | ok | 1 | 0 | 0 |
| s2-citations | partial | 55 | 4053 | 280 |
| s2-authors | error | 19 | 0 | 0 |
| hf-daily | ok | 3 | 34 | 34 |
| rss-sakana | ok | 1 | 12 | 1 |
| rss-metr | ok | 1 | 256 | 4 |
| rss-openai | ok | 1 | 1387 | 44 |
| rss-deepmind | ok | 1 | 100 | 8 |
| rss-weco | ok | 1 | 13 | 0 |
| github-releases | ok | 13 | 12 | 0 |

- S2 citations: 55 requests (42 HTTP 200, 12 HTTP 429, 1 timeout), 180-second bound; original collector count 283 included 3 future-dated records, corrected source-window count is 280.
- S2 authors: 19 requests (5 HTTP 200 seed-metadata replies, 14 HTTP 429), 180-second bound; no successful author-paper page. Unvisited coverage remains unknown.
- S2 shared anonymous spacing measured minimum 3.101755833 seconds, required 3.1 seconds. No paid API/model requests.

## HF and cache reuse

- 11/15: HTTP 200 empty list; 11/14: HTTP 200 empty list; 11/13: HTTP 200 with all 34 IDs. No late IDs or missing canonical recommendation dates relative to yesterday.
- This is observed emptiness, not `not_ready` and not a claim that all sources had no updates.
- 11/13 payload differences affect 3 authors’ HF account/profile objects only. Author names/order, title, abstract and date fields are unchanged. Full raw differences remain archived.
- The 34 unchanged HF members reuse prior identity/review evidence; current arXiv versions were not refetched. New 13 arXiv body/metadata cache inventory found no older matching ID files or metadata records, but that inventory was checked after these requests, not before.
- DeepMind weather RSS still reports 11/10. Keep the already-corrected canonical 11/13 page date, exact prior page evidence, and its existing review. No overwrite from raw RSS.

## Original-source verification and DOI boundaries

- All 13 new arXiv metadata records are official v1; 11 versioned HTML bodies and 2 versioned PDFs succeeded. Official metadata, version tokens/URLs, normalized document titles, body hashes and extracted text hashes were checked. All first_seen values retain earliest observed source time.
- Financial RAG: Crossref publisher deposit explicitly gives online 2026-11-13 and print 2026-11-14; S2 reported 11/14. Four author positions differ beyond punctuation/case/diacritics. Effective authors follow the publisher deposit while all raw S2 variants remain. ACM landing/PDF both HTTP 403; no arXiv title result. Original body and author equivalence remain unverified.
- DRIP: Crossref explicitly gives online 2026-11-14 and print 2026-11-15. The author `Jin Dong` versus `Jin Song Dong` difference remains unresolved. ACM landing/PDF both HTTP 403; no arXiv title result. Original body unavailable.
- Brain IoT: Crossref only provides a 2026-11 print/issued month and no online day. IEEE metadata confirms the DOI, title, authors and abstract, with displayPublicationDate/dateOfInsertion 2026-08-31 and issue date 2026-11-15. Original/online date stays **unknown**. `published` and `updated` are empty in the effective canonical proposal; publisher dates and S2 11/15 are separate fields. Do not label it newly published today. A PDF endpoint returned HTTP 200 HTML with subscriber metadata, not a PDF or full paper.
- Unknown DOI revision dates remain empty/unknown; repository numeric version 0 is the existing unknown sentinel. No publication number or claimed experimental result was altered.
- One IEEE response contained a server-generated anonymous session suffix. The archived body and final URL redact only that suffix; the receipt records the pre-redaction response hash and redaction details. All scientific/document metadata is unchanged.

## Validation and parent boundary

- Source intake QA: 13/13 checks passed. Additional handoff checks verify all 16 entries, 13 body-title/version/hash bindings, the 3 DOI metadata distinctions, unchanged production bytes, and Python script syntax.
- These are source/identity/date checks. No claim of scope acceptance, independent third-round review, empirical replication, CI, merge or online publication is made.
- No production edit, Git operation, model call, balance query or paid usage occurred in this child task. Parent is responsible for any account-level budget record.
- Files are frozen after the manifest. Parent may archive/remap paths and integrate the effective proposal; preserve source timestamps and the above limitations.
