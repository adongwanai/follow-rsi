# Source verification

Verified on 2026-10-27 using metadata-only HTTP requests with `FollowRSI/0.1` User-Agent. No PDF or X/Twitter requests were made. Enabled means the endpoint returned a parseable response during verification; it does not promise future availability.

The registry uses `{ranking, sources}` so the requested top-level ranking weights and per-source list can coexist. Health/cursors remain in `data/feed/state.json`.

| Source | Enabled | Evidence |
|---|---|---|
| arXiv harness / RSI / adjacent | yes | API HTTP 200, Atom 1.0, one real metadata entry for 2505.22954. Category RSS also returned RSS 2.0 with 321 entries. Shared 3-second pacing applies to API and fallback RSS. |
| HF Daily Papers | yes | HTTP 200 JSON list. Original title, abstract (`paper.summary`), authors, upvotes and `githubRepo` are present. The pipeline explicitly ignores HF-generated `ai_summary`. |
| Sakana AI | yes | `https://sakana.ai/feed.xml` returned HTTP 200 Atom with 10 entries; `/feed/` was 404. |
| METR | yes | `https://metr.org/feed.xml` returned HTTP 200 RSS with 100 entries. |
| OpenAI | yes | `https://openai.com/news/rss.xml` returned HTTP 200 RSS with 1,325 entries. This is the broad news feed, not a research-only feed. |
| Google DeepMind | yes | `https://deepmind.google/blog/rss.xml` returned HTTP 200 RSS with 100 entries. |
| Weco AI | yes | `https://www.weco.ai/blog/rss.xml` returned HTTP 200 RSS with 13 entries. |
| GitHub releases | yes | Agent-S API returned HTTP 200 and 2 release records; StarHarness API returned HTTP 200 with an empty list. A different unauthenticated Agent-S request returned 403; CI should use GITHUB_TOKEN. The returned empty list is valid data, not proof of active releases. |
| Anthropic research / news | no | Official research/news pages returned HTML without advertised RSS/Atom links. `/rss.xml` and `/news/rss.xml` returned 404. No official feed endpoint was verified. |
| Prime Intellect | no | `/blog/rss.xml`, `/rss.xml` and `/feed.xml` each returned 404. No valid feed was found among tested official endpoints. |
| Semantic Scholar citations / authors | no | S2_API_KEY was absent. No authenticated request was made; endpoint adapters are tested with an explicitly synthetic API-contract fixture. Configure the key, verify a real response and then enable. |

HF is the owner-prioritized discovery source. A 14-day run requests each of the 14 calendar dates, retains the original paper metadata and upvotes, and deduplicates repeated paper IDs. Its keyword prefilter is editable and visible in `feed/sources.yaml`; it deliberately admits broad agent/memory/skill matches so the LLM and owner can decide relevance.

Popularity is not evidence. Sorting weights are seed_hits=3, author_tracked=2, hf_upvotes=0.1, code_released=1, with owner picks ahead of automatic ordering. No classifier confidence or unverifiable quality score is part of ranking.

Semantic Scholar limitations: the adapter filters citation and author results using the paper publicationDate within 30 days; the API does not provide a citation-added timestamp. Undated S2 results stay in the raw response and are not assigned an invented date. The last-listed author is an operational tracking heuristic, not verified corresponding authorship.

RSS posts with arXiv links are hydrated from arXiv metadata before judging; a blog title or prose is never silently treated as a paper abstract. Posts without arXiv links stay `kind: post` for owner-selected lab updates. Releases contain version/link only. Disabled sources are not silently replaced by third-party feeds.

All local tests are offline. Recorded fixtures retain real source fields; `s2_mock.json` is labeled synthetic in the fixture README. No live issue, PR or external message was created by source verification.

Exact registered arXiv query groups were also executed with `max_results=1` and returned valid Atom: harness → 2610.35845; RSI → 2610.35604; adjacent → 2610.35616. These are endpoint/query checks, not owner-approved inclusions.

## Review and publication checks

The repository is [adongwanai/follow-rsi](https://github.com/adongwanai/follow-rsi). Discovery runs daily at 02:23 UTC; citation/author discovery and recall checks run Sunday at 21:07 UTC. The daily review queue runs at 03:17 UTC and the weekly picks queue runs Sunday at 23:41 UTC. All six feed workflows support manual dispatch and share one repository write lock.

Daily rollover reads the YAML from each older open PR's current head, so unmerged owner edits survive. The new review PR must exist before older PRs are closed. Deferred items return to the next day's queue without being published. After three calendar days without a merged daily review, one `Review stalled: Follow RSI` issue reports the queue size; it explicitly flags more than 60 waiting items and closes after review merges resume.

CI publication verifies the merged PR through GitHub's API. A human repository-owner merge, or the owner's approval of the exact head revision, is required. The review must have merged into the default branch, and its current YAML must exactly match the approved merge. Manual date/week reruns resolve a merged PR and use the same checks. Publication records the PR number, owner login and merge commit in `data/feed/review-provenance/`. These checks were tested offline with mocked GitHub responses; this document does not claim a live owner-approved publication has occurred.

Daily merges create daily pages, feed entries and a separate `feed/candidates-YYYY-MM-DD` PR. Weekly merges collect approved daily snapshots, then create or update one Release tagged `follow-rsi-YYYY-WWW`, with Chinese digest notes and the rendered share image. Daily publication does not create a Release.

Because `GITHUB_TOKEN` pushes do not trigger ordinary push/PR workflows, new review/candidate PRs explicitly dispatch a trusted-default-branch data check. Publication explicitly dispatches `pages.yml` after committing its outputs. Discovery also dispatches Pages when its health-state commit changes files. Health writes identical endpoint badges to `badges/feed-updated.json` and `site/badges/feed-updated.json`; pending discoveries remain outside the public feed.

Precision uses completed human decisions and excludes `pending` and `defer`. Publication latency uses the first actual approved daily snapshot's `published_at` timestamp; demo files and review timestamps do not count.

## HTTP observations

| Endpoint | Status | Parsed format | Entries |
|---|---:|---|---:|
| https://export.arxiv.org/api/query?id_list=2505.22954&max_results=1 | 200 | atom10 | 1 |
| https://rss.arxiv.org/rss/cs.AI | 200 | rss20 | 321 |
| https://huggingface.co/api/daily_papers?limit=1 | 200 | list | 0 |
| https://sakana.ai/feed/ | 404 | text/html; charset=utf-8 | 0 |
| https://metr.org/feed.xml | 200 | rss20 | 100 |
| https://www.anthropic.com/research | 200 | text/html; charset=utf-8 | 0 |
| https://www.anthropic.com/news | 200 | text/html; charset=utf-8 | 0 |
| https://openai.com/news/rss.xml | 200 | rss20 | 1325 |
| https://deepmind.google/blog/rss.xml | 200 | rss20 | 100 |
| https://www.primeintellect.ai/blog/rss.xml | 404 | text/html; charset=utf-8 | 0 |
| https://weco.ai/blog/rss.xml | 200 | rss20 | 13 |
| https://api.github.com/repos/simular-ai/Agent-S/releases?per_page=1 | 403 | application/json; charset=utf-8 | 0 |
| https://sakana.ai/feed.xml | 200 | atom10 | 10 |
| https://www.primeintellect.ai/rss.xml | 404 | text/html; charset=utf-8 | 0 |
| https://www.primeintellect.ai/feed.xml | 404 | text/html; charset=utf-8 | 0 |
| https://api.github.com/repos/ServiceNow/StarHarness/releases?per_page=1 | 200 | application/json; charset=utf-8 | 0 |
| https://github.com/simular-ai/Agent-S/releases.atom | 200 | atom10 | 10 |
| https://www.anthropic.com/rss.xml | 404 | text/html; charset=utf-8 | 0 |
| https://www.anthropic.com/news/rss.xml | 404 | text/html; charset=utf-8 | 0 |
| https://api.github.com/repos/simular-ai/Agent-S/releases?per_page=2 | 200 | list | 2 |
