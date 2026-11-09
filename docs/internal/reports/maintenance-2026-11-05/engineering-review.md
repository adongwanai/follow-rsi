# 2026-11-05 integration engineering review

**Final status: actual integration independently verified; no unresolved substantive engineering finding.** Final check: `2026-11-05T04:24:09.810287+00:00`. The initial and intermediate snapshots below are retained as the audit trail.

Reviewed at `2026-11-05T04:04:19.373482+00:00`. Initial status: **pre-integration review complete**. See the post-integration verification appended below for the current status.

The reviewed integration script has no remaining substantive defect found in the verified merge/accounting scope. Three concrete issues found during review are fixed in the snapshot below. The final primary and independent S2 review schemas are still being completed; this review does not mistake that expected work for a bug and does not claim the integration ran.

## Reviewed artifacts and boundary

- `build/maintenance-primary-2026-11-05/integrate.py` SHA-256: `75a39b3895b62e009ab412a1fe0f17e919ca1b0e35131355db4b75fc8fe6a0d5`.
- `docs/internal/reports/maintenance-2026-11-05/source-universe-reconciliation.json` SHA-256: `18a38a63ff121129bcb59a13e23c1c5687be548c89dfb435fdb8e8b8674d646b`.
- All analysis used local frozen inputs, static code inspection and a pure in-memory merge. No production/source files, network or Git state were changed. Only this review and its JSON companion were written.

## Verified invariants

| Check | Result |
| --- | --- |
| Canonical accounting | 1,598 baseline + 138 new IDs − 1 proven duplicate = **1,735**. New cohorts: 53 HF, 4 arXiv, 76 independent S2 history, 5 news. |
| First observation | Every new record's actual first-seen day is **2026-11-05**; the earliest observed source timestamp is selected. Retained old first-seen values stay unchanged. |
| Official metadata | The disjoint 57 + 76 suggestion files cover all 133 new paper IDs. Publication/update dates remain distinct from observation and HF recommendation dates. |
| Old scientific fields and decisions | Pure merge changes only `source_hits`, `hf_daily_dates`, and `links` for MoLRSI and EvoTeam. All 138 new effective formal decisions remain `defer`. The retained Sakana record is unchanged. |
| Source universe | Prior ledger 8,280 + baseline union = 8,331; all observed-ID union = 8,482; alias resolution = **8,481 = 1,735 canonical + 6,746 source-only**. |
| Filtered partition | Source-only = 6,292 prior + 4 new outside-window IDs, plus 441 prior + 9 new undated IDs = **6,296 + 450**. No old raw-only entry was silently promoted. |
| Publication | The 21 items in `site/feed/latest.json` contain none of the two changed IDs or the removed duplicate. The script grants no publication authority and generates no new daily edition. |
| Source health | 12 actual source attempts: 11 successful, authors failed. One health update resets citation errors to 0 and increments authors errors from 4 to 5. No issue client is supplied. |
| HF daily status | The 11/04 snapshot has 50 items: 4 include suggestions, 45 exclude, 1 borderline. The 11/05 11:15 snapshot has 5 exclusions. Independent results agree; the text explicitly permits later board growth. |

The universe report correctly identifies reuse of the hash-bound prior 118-snapshot ledger and does not claim to have reparsed every current RSS archive or navigation link.

## Issues resolved in the reviewed script

1. **Kev-Bio abstract binding.** The reviewed HF summary hash was `35af4a8f14b3b603001deb71bfebe7254b0ffc939c5eedd68e39a562b6db0ab8`, while the canonical normalized abstract hash is `64cf8b5c6823891e3457b39c61ca4b169b328d142c5575e25291087e025aee74`. The 1,707/1,701-character inputs differ only in whitespace. The script now verifies that relation against the saved HF body and retains both hashes plus the normalization status. Other bindings must match exactly.
2. **Independent RSS reviews.** The two OpenAI body reviews now enter the independent suggestion/level/report join; they will no longer be falsely labeled as not individually rereviewed.
3. **PRISM official links.** New-record metadata merging now retains its verified DOI and publisher URL. The in-memory result contains the S2, DOI and publisher links.

## Explicit approval and archive consequences

Preserving old scientific values and receipt contents does **not** preserve a receipt's valid binding when HF membership or links change: `scripts/feed/review.py::source_hash` includes both fields. The current script records the old/new hashes and `prior_approval_binding_automatically_reused: false`.

| ID | Old source hash | New source hash |
| --- | --- | --- |
| MoLRSI `arxiv:2610.39714` | `4e5b3b73d1bb50ec3bcfade80a9436391d02946d640336e7b576441ecc7086d7` | `059898632feae463a0194b3b17451eef3d56bfe20d9dd282679128e6da86c14c` |
| EvoTeam `arxiv:2610.39813` | `20805d8ad328382ebdf24e01e277aac952bfe93cdcded439dbac8e5299eda501` | `12f3795f72723c0944ef66a1c0363b0382b8e54235d206a7be7d638ac1f7c0aa` |

MoLRSI's `review/approvals/2026-11-02.yaml` scope recommendation is `unknown`; its stored hash matches the baseline and will not match the updated record. The same is true of its deferred rows in `review/daily/2026-10-31.yaml` and `review/daily/2026-11-01.yaml`. No accept decision is being invalidated into a hidden publication approval. Existing receipt files must remain historical evidence; any later review must bind to the new source hash.

Those two archived daily queues also contain the removed absolute Sakana ID, both as `defer`. The surviving record already aliases that ID, but `validate_daily_review` does not resolve aliases and rejects a missing canonical ID. Consequently those historical queues cannot be replayed unchanged after deduplication. Preserve the archived receipts and original-record evidence; regenerate and review a current queue if later publication is requested. The existing 21 published feed items are unaffected.

## Final execution gates

- Finish the planned primary selected-body and independent S2 reports, then validate their final schemas and the 140 joined status rows.
- Retain each reviewer's suggestion, actual reading level and unresolved evidence blockers. Independent body reading must not imply the primary read that body. Preserve disagreements.
- Execute the per-item abstract binding assertions with those final reports before production writes; retain the two explicit old/new approval-hash transitions.
- Verify the actual 1,735-record result, source-health transition, daily statuses, and unchanged published editions after integration. **This report only verifies the proposed merge and does not claim those writes occurred.**

Machine-readable details and exact input hashes are in `engineering-review.json`.

## Post-integration read-only verification — 2026-11-05T04:21:05.679490+00:00

**Core integration checks passed on actual files; the RSI-Dojo addendum/status refresh is still being finalized.** This extends, rather than retroactively changes, the initial static/in-memory review.

- Independently re-counted **1,735 canonical records, 138 new IDs and 140 status rows**. Advice is **36 include / 101 exclude / 3 borderline**, with **35 / 101 / 2** among new records. Every new first-seen timestamp equals the earliest actual intake observation; new formal decisions remain defer, with no fabricated model-stage outputs.
- Compared every retained baseline record: only MoLRSI and EvoTeam changed, only in HF membership, source provenance and links. The removed Sakana ID is absent and the surviving stable record is byte-for-field equivalent to its baseline. All observed HF memberships are present.
- Verified all 140 primary abstract bindings, including the exact saved Kev-Bio raw-to-canonical whitespace relation; checked the separate primary/independent suggestions and reading levels. ModelBlaster remains a visible disagreement. The two independent RSS body reviews and PRISM DOI/publisher links are present. Forty records truthfully state that they were not individually rereviewed.
- Reconfirmed the **21 published items and four protected files** are unchanged. Compared all seven dated daily files to HEAD: the 10/27 withdrawal page changes only its shared publication-update-log; all other bytes and dated files are unchanged. The old 11/02 approval receipt and 10/31, 11/01 daily queues are also byte-identical to HEAD, so no old review hash was silently rebound.
- Recomputed all 12 source-health transitions, seen-ID unions and weekly fresh-ID deltas. Citations errors are **0**, authors errors **5**, and S2 authentication remains anonymous. Daily statuses are 11/04 quality-gate-blocked and 11/05 no-eligible-HF with the observed-snapshot caveat.
- The author recorded two idempotent builds; this review independently hashed **all 631 current outputs** against that manifest, without rerunning the build.

The evidence-file scan found 275 current matches among 277 distinct path/hash pairs. One remaining pair is explicitly the previous HF primary report, with a separate correct current binding. The other is the S2 selection-time primary-report hash; its historical snapshot meaning needs to be explicit if the same path now names a revised report. These historical hashes must not be represented as current-file hashes.

The final pass also identified RSI-Dojo's explicit priority body-evidence gap despite an initially empty blocker list. After parent authorization, one free official HTML GET succeeded (HTTP 200), saving original HTML, text, paragraphs and a receipt under `build/maintenance-2026-11-05/s2-priority-exclusion/`. All **264 frozen source files** checked before/after remain hash-identical; the original 188 discovery-request statistics and source-health artifacts were not changed. No scientific or formal decision was applied by this reviewer. Parent/independent selected-body addenda and the final status refresh will be checked before final signoff.

## Final addendum and actual-state verification — 2026-11-05T04:24:09.810287+00:00

**Passed.** The final actual state remains **1,735 canonical records, 138 new IDs and 140 scope-status rows**; suggestions remain **36 include / 101 exclude / 3 borderline** (new records **35 / 101 / 2**). The source-health state and daily statuses have not been replayed or changed by the supplemental body review. All new canonical discovery-screen reading levels match their final status rows. The only retained old-record changes are still the two explicitly documented HF provenance patches, and the stable Sakana record remains unchanged.

RSI-Dojo now links both completed selected-body addenda and preserves its previous abstract-only reading level. The primary and independent review levels are distinct and accurately copied into the final status; the canonical discovery-screen level matches the primary. The reason was updated, the body-evidence gap is explicitly resolved and its temporary blocker was removed. Both reviewers retain the exclusion suggestion and formal defer. This engineering pass independently reverified all **6 primary + 7 independent exact quotes** against the saved paragraph hashes and text. Independent selected-body S2 coverage is now 34, with 37 new S2 records still explicitly outside independent screening.

RSI-Env and Meta² retain their two **taxonomy_subtype_disagreement** blockers while both reviewers still recommend inclusion. ModelBlaster retains the separate scope disagreement. No data-task classification or model-training fact was used here to manufacture a scientific approval.

The final evidence scan verified **280 distinct current file/hash bindings** and found no unexplained mismatch. The prior HF comparison hash is explicitly historical and has a valid current counterpart. The S2 sampling hash is now explicitly marked as a selection-time snapshot whose old bytes were not saved and cannot be recovered from the current path; it is not represented as a currently verifiable file binding. This historical evidence limit remains visible.

All 631 build-manifest outputs still match current files. The parent's saved test log reports **384 passed in 59.80s**; this reviewer inspected that log and did not rerun tests or builds. The four protected files, old-review preservation and dated-page checks from the core pass remain applicable. The 21 published feed items, formal accept count and existing dated editions remain unchanged. There are **zero new formal accepts or publication authorizations**, and old approval hashes were not rebound.

No production file was written by this engineering reviewer. The only extra network operation was the explicitly authorized, separately receipted RSI-Dojo GET described above. This signoff completes engineering verification of the local integrated artifacts and does not claim a commit, push, PR merge or live deployment.
