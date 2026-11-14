# semipy

Write Python logic in natural language. `semipy` generates, validates, and caches real Python functions from your specs — no boilerplate, no hardcoded rules.

```python
from semipy import semiformal, semi, configure

configure(openai_api_key="sk-...")  # or set OPENAI_API_KEY in environment

@semiformal
def parse_log_line(line: str) -> dict:
    #> extract timestamp, level, and message from an Apache log line
    result = ...
    return result

# First call: agent generates a Python function and caches it.
# All later calls: load the cached implementation instantly.
row = parse_log_line('127.0.0.1 - - [10/Oct/2000:13:55:36] "GET /index.html" 200')
```

## Concepts

For the idea behind `semipy` — semi-formal programming, where part of a program's
specification stays informal and only commits to an implementation when it is first
used — and how the pieces fit together, see
[docs/semi-formal-programming.md](docs/semi-formal-programming.md).

## Documentation

- [docs/semi-formal-programming.md](docs/semi-formal-programming.md) — the idea: semi-formal programming.
- [docs/architecture.md](docs/architecture.md) — runtime architecture: call-site/slot identity, the spec-equivalence key, the REUSE/ADAPT/GENERATE/INSTANTIATE decision, and the DAG cache, with math and a worked trace.
- [docs/behavioral-contract.md](docs/behavioral-contract.md) — the contract subsystem that records *why* each regeneration happened and *what its effect was*.
- [docs/effects.md](docs/effects.md) — reified, verifiable, revertable real-world effects (the `fx` capability, shadow worlds, the blast-radius proof, the effect ledger).
- [docs/sketch-library.md](docs/sketch-library.md) — pattern learning and the INSTANTIATE decision (satisfy a new slot by substitution, no LLM call).
- [docs/interpreted-mode.md](docs/interpreted-mode.md) — interpret-until-shape-stable slots (`interpreted=True`): per-call LLM that promotes itself to cached code once a residual reproduces held-out examples.

## Install

The distribution is named `semiformal-py`; you import it as `semipy`.

```bash
pip install semiformal-py
```

For Jupyter notebook display:

```bash
pip install "semiformal-py[jupyter]"
```

For PDF input materialization:

```bash
pip install "semiformal-py[pdf]"
```

## API key

semipy uses the OpenAI API for code generation. Set your key in one of three ways:

**Environment variable** (recommended for scripts):

```bash
export OPENAI_API_KEY=sk-...
```

**`.env` file** at the project root (loaded automatically):

```
OPENAI_API_KEY=sk-...
```

**In code** (overrides env):

```python
from semipy import configure
configure(openai_api_key="sk-...")
```

## Configuration

```python
from semipy import configure

configure(
    openai_api_key="sk-...",       # defaults to OPENAI_API_KEY env var
    openai_model="gpt-4o",         # generation model (default: gpt-5.5)
    verbose=True,                  # rich terminal output during generation (default: True)
    cache_dir=".semiformal",       # where portal JSON and dispatch modules are stored
    max_retries=3,                 # agent retry limit on validation failure
    session_source=None,           # pin portal identity (useful for Jupyter; see below)
)
```

All fields are optional — call `configure()` with only what you want to override.

## Terminal output

When `verbose=True` (the default), semipy prints a live Rich panel showing the agent's reasoning, tool calls, and generated code as they stream in. This works in both terminal and Jupyter.

```
 Implementing code...
 ─────────────────────────────────────────────────
  Reasoning  The function needs to parse a standard Apache
             Combined Log Format line...
 ─────────────────────────────────────────────────
  Draft the function  function drafted
 ─────────────────────────────────────────────────
  Reusing cached implementation; runtime verify passed.
  parse_log_line  GENERATE  a1b2c3d4  examples/logs.py:12
```

To silence all output: `configure(verbose=False)`.

To see full prompt, decision, and tool-call dumps, set the environment variable:

```bash
export SEMIPY_PIPELINE_TRACE=1
```

## Usage patterns

### `@semiformal` with `#>` spec blocks

```python
from semipy import semiformal

@semiformal
def extract_fields(record: str) -> dict:
    #> extract date, sender, and subject from an email header
    result = ...
    return result
```

The `#>` block is the spec. The `result = ...` is the slot anchor — the agent fills it in.

### Inline `semi()` for expressions

```python
from semipy import semiformal, semi

@semiformal
def classify_rows(rows):
    return [r for r in rows if semi(f"is {repr(r['status'])} a client error?")]
```

### Standalone `semi()` in any function

```python
from semipy import semi

def process(text):
    label = semi(f"classify '{text}' as positive, negative, or neutral")
    return label
```

### Multiple slots in one function

```python
from semipy import semiformal

@semiformal
def analyze(entry: str) -> dict:
    #> extract the IP address from the log entry
    ip = ...

    #> determine if the HTTP status code in the entry indicates an error
    is_error = ...

    return {"ip": ip, "error": is_error}
```

### Interpreted mode (interpret-until-shape-stable)

By default a slot compiles to a Python function on its first call. For operations
whose answer genuinely needs the model on every input (summarize, judge), or that
you want to keep model-backed until they prove they generalize, mark the slot
`interpreted=True`. It calls the LLM per call (memoized), and **promotes itself to a
normal cached function** once a synthesized residual reproduces held-out examples;
after that it runs with no LLM, like any other cached slot.

```python
from typing import Literal
from semipy import semi, semiformal

# extraction/parsing: interprets a few calls, then promotes to cached code
ts = semi(f"extract the bracketed timestamp from: {line}", interpreted=True)

# classification: constrain the labels with a Literal/Enum so it can promote
Family = Literal["scoreboard_child", "worker_env_error", "other"]
fam = semi(f"classify this log body: {body}", expected_type=Family, interpreted=True)

# every #> slot in the function (incl. multi-output blocks)
@semiformal(interpreted=True)
def parse(line: str) -> dict:
    #> extract the bracketed timestamp into ts and the level into level
    ts = ...
    level = ...
    return {"ts": ts, "level": level}

# summarize/judge: never reproduces held-out output, so it stays interpreted (correct)
gist = semi(f"one-sentence summary of: {passage}", interpreted=True)
```

Promotion is gated by **held-out** validation run in the sandboxed gist executor, so
a residual that only memorizes the examples — or an operation that can't be expressed
as a deterministic function — is rejected and the slot keeps interpreting. The
standalone `interpreted(...)` / `InterpretedOp` helper exposes the same loop without
the cache, for experiments. Full detail: [docs/interpreted-mode.md](docs/interpreted-mode.md).

## Reasoning surface (`#<` lines)

After each generation, semipy writes a small set of `#<` comment lines around each slot anchor. These are not part of your spec — they are system-managed traces that describe what the generated implementation decided and why, so you can read and steer it without digging into the cache.

```python
@semiformal
def infer_datetime_formatter(date_str: str) -> str:
    #< intent: infer strptime pattern from observed date text
    #< by: probing a regex-gated candidate table; because the table covers all observed formats
    #< unless: empty or unmatched input raises ValueError
    #> verified: 'Mar 2025' -> {'input_pattern':'%b %Y'}, return error if no match
    input_pattern = ... #> infer the input date regex/strptime pattern from the observed string format in this session.
    output_pattern = "%b %Y"
    return datetime.strptime(str(date_str), input_pattern).strftime(output_pattern)
```

### Placement

`#<` lines appear in two zones around the slot anchor:

- **Zone P (provenance, above the anchor):** `intent`, `given`, `by`, `unless` — why this implementation exists, what it assumes, and how it handles failure.
- **Zone E (effect, below the anchor):** `yields`, `verified` — what the generated code produces and what was observed at runtime.

### Keywords

| Key | Zone | Meaning |
|---|---|---|
| `intent` | above | One-phrase task summary (emitted only when the spec is long or ambiguous). |
| `given` | above | Input-shape assumptions beyond the signature (multi-param slots only). |
| `by` | above | Strategy/mechanism this implementation uses. Embed the reason inline when the choice is non-obvious: `<strategy>; because <reason>`. Always present. |
| `unless` | above | Fallback or exceptional path (emitted only when the generated code has a raise/except). May repeat for distinct failure modes. |
| `yields` | below | Output shape beyond the return annotation (skipped for simple builtins like `str`, `int`). |
| `verified` | below | Sample input → observed output, derived from the validation run (never LLM-generated). |

### Steering

To change what the next generation produces, edit the `#< by:` line (strategy) or the `#< unless:` line (exceptional path). On the next run where the implementation needs to change, semipy reads the override and adapts accordingly.

### Promoting a constraint

To lock an inference note into the contract permanently, flip `#<` to `#>` on the same line. This extends the spec text, causing a new ADAPT on the next run, and suppresses the duplicate `#<` line from being re-emitted.

```python
# Before: system-managed trace
#< by: probing a regex-gated candidate table; because the table covers all observed formats

# After: promoted to user contract — fixes the strategy for future runs
#> by: regex-gated candidate table
```

`#<` lines are stable across runs: semipy only rewrites them when the generated implementation changes. A no-op re-run produces a byte-identical file.

## Caching and reuse

Generated functions are cached **per project** — the folder tree rooted at the
nearest `.semiformal/` directory (found by walking up from your source file, the
way git finds `.git`). All files under that root share one cache, so a learned
implementation in one file can be reused in another, and same-named files in
different projects never collide. You set project boundaries by where you place
`.semiformal/`; if none exists, one is created in your working directory.

- `.semiformal/<session>.portal.json` — versioned DAG of all commits, branches, and decisions for the project.
- `.semiformal/runtime/<module>.semi.py` — compiled Python implementations for import.

On subsequent runs, semipy loads the cached implementation without calling the LLM. It re-verifies when it detects new input shapes, and runs ADAPT (re-generation from the prior commit) when verification fails.

To force regeneration, delete `.semiformal/`, or use the slot CLI below.

> Upgrading from 0.2.x: caches were previously per-file. On the first 0.3 run,
> existing per-file caches are automatically merged into the project cache — you
> keep your learned implementations.

### Managing slots from the CLI

```bash
python -m semipy slots        --portal .semiformal/<session>.portal.json   # list slots (file:line, versions, decision)
python -m semipy reset-slot   --portal <portal> --slot-id <id>             # wipe a slot; the next run regenerates it
python -m semipy reset-version --portal <portal> --slot-id <id> --commit-id <c>   # delete one version
```

The same actions are available in the VS Code extension's slot-history tree
(right-click a slot → **Reset slot**, or a version → **Delete this version**).

## Jupyter

In Jupyter notebooks, semipy detects the `ipykernel` environment automatically. The portal is keyed to `os.getcwd()` so one portal persists across kernel restarts.

Install the optional display extras for inline Rich output:

```bash
pip install "semipy[jupyter]"
```

If multiple notebooks share a working directory and need separate caches:

```python
configure(session_source="/path/to/my_notebook.ipynb")
```

## VS Code extension

The [Semipy VS Code extension](https://marketplace.visualstudio.com/items?itemName=semipy.semipy-vscode) adds:

- Syntax highlighting for `#>` spec lines (teal) and `#<` reasoning lines (green)
- Slot history tree in the Explorer panel
- Split-view to inspect generated `.semi.py` alongside your source
- Inlay hints and CodeLens showing commit id and decision

## Examples

See the `examples/` directory:

- `examples/apache_log_semiformal_stages.py` — staged walkthrough from simple extraction to INSTANTIATE and promotion workflow
- `examples/datetime_test.py` — datetime format inference with observed samples and steered `#<` surface
- `examples/fasta_header_metadata.py` — FASTA header parsing with multiple slots, nested anchors, and standalone `semi()` calls
- `examples/use_contract_intelligence.py` — contract field extraction from PDF
- `examples/use_sponsorship_canonicalizer.py` — entity canonicalization pipeline

## License

MIT
