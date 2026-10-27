# Contributing

Edit curated evidence-base paper information only in `data/papers.yaml`. It is the catalog's single source of truth. Do not manually change generated README blocks, receipt blocks, JSON, badges, or share cards. Reading routes live in `data/routes.yaml`; deployment URLs live in `site.config.yaml`. Feed discovery and owner review have a separate [operating guide](docs/feed-setup.md).

Every number and every evidence change needs a source page or table number in the PR. Changing `unknown` to `yes` or `no` requires explicit supporting evidence. Do not infer evidence from an abstract, a code link, a paper title, or familiarity with a method. Omitted evidence fields become `unknown`. Use `partial` or `na` only with a cited reason. Topology is a descriptive classification, not an evidence score; leave it `unknown` without a source.

`needs_reading: true` means **待细读 / Needs verification** and must remain visible in every generated presentation. New candidates belong to `section: candidates` with `status: candidate`; an arXiv-monitor issue does not add a paper automatically.

English summaries and results are translations of their corresponding Chinese fields only. Keep every fact, digit, sign, percentage, range, and unit; set `en_machine_translated: true`. The tests compare numeric tokens and occurrence counts. They do not replace a semantic translation review. Do not turn Chinese number words into extra Arabic numerals.

You may edit handwritten sections outside `<!-- AUTO:...:START -->` / `<!-- AUTO:...:END -->`, including notes, videos, direction overviews, and ideas. Keep unfilled material as `<!-- TODO -->`. Preserve the AUTO markers. A changed title inside the handwritten page heading must be updated manually; the receipt block updates automatically.

`README.md` is the default Chinese README; `README_zh.md` keeps the alternate Chinese entry point and `README_en.md` is English. The build updates AUTO blocks independently in all three files and preserves every byte outside those blocks, including placeholders.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/validate.py
python scripts/build.py
python -m pytest -q
```

Commit the source edits **and regenerated output**. PR build checks reject stale files and tell you to run `python scripts/build.py`. The builder runs entirely offline and never modifies `papers.yaml`.

## Author badges

Each paper has a shields endpoint at `<pages-url>/badges/<id>.json`, copied into the Pages artifact. Replace both placeholders:

```markdown
![evidence](https://img.shields.io/endpoint?url=<pages-url>/badges/<id>.json)
```

The badge records held-out evaluation, matched budget, cross-model transfer, and cost. All four `yes` gives green; any `unknown` gives gray; otherwise it uses ultramarine. `needs_reading` is shown in the badge message. A badge is a record of reported evidence, not an endorsement or a leaderboard rank.

## Publication

The repository is `adongwanai/follow-rsi` and Pages is `https://adongwanai.github.io/follow-rsi`. For a fork, update `repository`, `repository_url`, `base_url`, author fields and optional `newsletter_url` in `site.config.yaml`, plus author information in `CITATION.cff` and the licenses. Rebuild and rerender cards after changing public URLs. Set Pages to GitHub Actions and upload `assets/social-preview.png` in Settings → Social preview.

Python 3.11 is used in CI. `requirements.txt` includes PyYAML, jsonschema, Jinja2, pytest, requests, feedparser and the official OpenAI SDK, which also handles the configured DeepSeek endpoint. Playwright is optional for the separate screenshot/media step. The QR encoder is vendored JavaScript with its license; it adds no runtime package or network request. See [development notes](docs/development.md).

The separate `arxiv-watch.yml` candidate monitor runs Monday at 01:17 UTC. It searches both titles and abstracts, requires `agent`, excludes known arXiv IDs and existing open/closed issues, and creates at most 15 candidate issues. It posts only the original title, link, and abstract. The Follow RSI daily feed uses its own discovery and owner-review workflows; see the operating guide for their schedules and publication gates. No discovery request is run during local builds or tests.
