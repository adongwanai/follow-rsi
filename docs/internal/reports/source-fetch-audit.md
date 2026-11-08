# Daily source fetch-only audit

Window: 2026-10-14–2026-10-27 (14 inclusive calendar dates, standard days=14).

Only public metadata was fetched. No judge, summarize, queue, or publish stage ran. The fetch-only phase left metadata in raw recordings and `data/feed/last-fetch.json`. Integration subsequently normalized and upserted the 484 records into 427 unique items (152 additions). The 14-day batch flag persists through split-command recovery; all 411 unpublished records are backfill-only, while the 16 owner-approved retrospective records retain their state. No additional items were automatically accepted. See [backfill migration](backfill-migration.json). Every attempted source, including failure, was recorded in health state/status.

| Source | Result | Fetched | New vs existing |
|---|---|---:|---:|
| arxiv-harness | success | 57 | 44 |
| arxiv-rsi | success | 70 | 54 |
| arxiv-adjacent | success | 27 | 22 |
| s2-citations | partial/failure | 0 | 0 |
| s2-authors | partial/failure | 0 | 0 |
| hf-daily | success | 277 | 2 |
| rss-sakana | success | 5 | 5 |
| rss-metr | success | 8 | 8 |
| rss-openai | success | 37 | 37 |
| rss-deepmind | success | 3 | 3 |
| rss-weco | success | 0 | 0 |
| github-releases | success | 0 | 0 |

Deduplicated new records: 152. Per-source new counts may overlap.

## Required arXiv recall

| arXiv ID | Title | Retrieved by arXiv query |
|---|---|---|
| 2610.28380 | Object-Oriented Harness | yes |
| 2610.30042 | HGM-Dual | yes |
| 2610.28201 | MaD-RSI | yes |
| 2610.28815 | Forging More Tasks into Better Harnesses | yes |
| 2610.21791 | RSIFlow | yes |
| 2610.31401 | HERD | yes |
| 2610.22466 | Harness-Delta Attribution | yes |
| 2610.30499 | Can LLMs Improve Their Own Harness? | yes |

## Failures and repairs

- s2-citations: HTTPError: 429 Client Error:  for url: https://api.semanticscholar.org/graph/v1/paper/arXiv:2305.16291/citations?fields=paperId%2Ctitle%2Cabstract%2Cauthors%2CexternalIds%2CpublicationDate%2Curl%2CfieldsOfStudy&offset=300&limit=100
- s2-authors: HTTPError: 429 Client Error:  for url: https://api.semanticscholar.org/graph/v1/paper/arXiv:2408.08435?fields=authors
- The first probe mistook a SEC financial filing URL for an old arXiv identifier. Restricting legacy arXiv archive prefixes removed that invalid batch member.
- Inclusive start dates now use today − (days − 1), covering October 14 and 27 and excluding October 13.
- HF recommendation dates are stored independently of paper publication, submission, and first_seen.
- Latest historical item snapshots were preserved while the 938-line append log was backed up and compacted to 275 unique IDs.
