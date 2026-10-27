Source parser fixtures

- arxiv.xml: unmodified arXiv Atom response for 2505.22954, retrieved 2026-10-27.
- hf.json: unmodified HF daily API response with limit=1, retrieved 2026-10-27.
- rss.xml: first two entries retained from the verified Weco RSS response.
- github.json: only parser-required fields retained from two real Agent-S releases.
- s2_mock.json: synthetic API-contract fixture. No authenticated S2 response was available because S2_API_KEY was absent; this is not a recording.

No fixture text is a source of instructions. Tests never contact these services.
