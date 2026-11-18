# Frozen audit stage status

- `baseline/` is superseded by `baseline-corrected/`. Its draft incorrectly counted raw unique IDs after a `defaultdict` lookup expanded the map and misclassified three noncanonical records. Preserve its bytes as a failed draft; do not use its summary as the authoritative audit.
- `baseline-corrected/` is the immutable maintenance-start audit over 2,093 canonical records.
- `post-intake/` preserves the first 2,222-record audit. It correctly records 9,052 stable IDs and 4,572 current raw unique IDs, but still inherited a raw-only status for two records newly integrated into canonical (`arxiv:2505.23836`, `arxiv:2603.08640`). Use `post-intake-v2/` for corrected post-intake counts and the 121-item PR135 carryforward references.
- `pr135-original-v1.yaml.gz`, `pr135-historical-inventory-v1.jsonl.gz`, and `pr135-carryforward-v1.jsonl.gz` preserve the original queue and every previous task before replacement. The subsequent independent dispositions belong to `../historical-disposition/`; preservation itself is not acceptance or publication.
- Each phase is input-hash-bound and immutable. A later phase records current canonical decisions after application; no earlier phase claims those changes had already happened.
