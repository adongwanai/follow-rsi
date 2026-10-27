# Prompt regression data

`labeled.yaml` contains 80 automatically imported repository records and the 27 exact user-provided curator seeds. “After 2026-04” means **2026-05 onward**. Foundations and candidates are excluded from automatic import. Curator seeds retain `labeled_by: curator-seed` and `needs_owner_review: true`; their labels are not changed to improve a score.

Titles and abstracts belong in `metadata/<arxiv-id>.json` (`/` in old arXiv identifiers becomes `_`). Only metadata returned by arXiv is cached. Curated summaries are never used to invent an abstract. Fetching is explicit and uses the shared arXiv adapter's three-second request interval:

```sh
python -m scripts.feed.eval --fetch-metadata
python -m scripts.feed.eval
```

Raw arXiv Atom responses are retained in `raw/`. Each example's name is checked against its returned title before scoring: punctuation and `RSI` expansion are normalized, curator prefixes and parenthetical nicknames are handled, and a short method name can be supported by an exact case-preserving occurrence in the abstract. The report retains the matching method and any supporting excerpt. Unmatched titles and empty abstracts are flagged for owner verification and are not scored; labels remain unchanged. `--workers 4` evaluates independent model examples concurrently while metadata requests remain serial.

The second command uses `LLM_PROVIDER`, `LLM_MODEL`, `LLM_API_KEY`, and optionally `LLM_BASE_URL`. It does not load environment files automatically. The supported providers use the official OpenAI SDK: `openai`, `openai-compatible`, and `deepseek`. DeepSeek uses JSON-object mode with the exact prompt schema validated locally; the other providers request JSON-schema mode. Every call uses temperature zero. JSON/schema failures retry once; API failures remain explicit errors.

The report writes `report.json` and `report.md`. Missing credentials produce **eval skipped**, without claiming any quality threshold passed. Missing metadata, API errors, and unresolved contradictory labels make a run incomplete. Borderline predictions are listed separately and count as missed includes when computing include recall. Direction accuracy counts unclassified positive examples as incorrect, preventing a classifier from inflating its score by excluding difficult papers.

The required gates are include recall ≥ 0.90, include precision ≥ 0.80, and primary-direction accuracy ≥ 0.75. The CLI exits nonzero for incomplete runs or failed gates. A skipped run exits zero so credential-free contributions can still run offline tests; CI must display its skipped state explicitly.

Review overrides and rejections are appended with `labeled_by: owner` and their review provenance. A stable decision hash prevents duplicate additions. Earlier labels remain in the file; the most recent explicit owner decision takes precedence during evaluation. Contradictory curator/import labels without an owner decision are reported for resolution and are never silently relabeled.

LLM responses are cached by identity, version, rendered prompt hash, and model. The rendered hash includes supplied source text and correction feedback, so a corrected Chinese summary cannot reuse a translation of the earlier text. Numeric guard failures retry the bilingual pair once, then clear both languages. Quick-evidence quotes must be 5–60 characters from the normalized abstract; comments alone cannot support a public `yes` under the hard quote rule.
