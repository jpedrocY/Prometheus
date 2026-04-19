# Implementation Ambiguity Log

## Purpose

This log records ambiguities, specification gaps, doc/disk inconsistencies, unclear API behavior, and pending implementation decisions discovered by Claude Code during phased implementation of Prometheus.

Entries are not issues to be silently patched. They are decisions or questions that deserve operator or ChatGPT review before they shape live-relevant behavior.

This log complements `docs/12-roadmap/technical-debt-register.md`. Safety-relevant open items should also be reflected there. This log is where items are first captured; the debt register is where they graduate if they remain open across phases.

## Entry format

```
## GAP-YYYYMMDD-NNN — Short title

Status:              OPEN | IN_REVIEW | RESOLVED | ACCEPTED_LIMITATION | SUPERSEDED
Phase discovered:    0 | 1 | 2 | ...
Area:                DOCS | TOOLING | STRATEGY | DATA | RISK | EXECUTION | ARCHITECTURE | OPERATIONS | SECURITY | INTERFACE | OTHER
Blocking phase:      NON_BLOCKING | PRE_CODING_START | PRE_DRY_RUN | PRE_PAPER_SHADOW | PRE_TINY_LIVE | PRE_SCALED_LIVE | POST_MVP | FUTURE_RESEARCH
Risk level:          LOW | MEDIUM | HIGH | CRITICAL
Related docs:        <paths>

Description:
<what was found>

Why it matters:
<consequence if ignored>

Options considered:
- Option A: ...
- Option B: ...

Recommended resolution:
<claude code's recommendation>

Operator decision:
<filled by operator or "pending">

Resolution evidence:
<commit hash / file path / command output once resolved>
```

---

## GAP-20260419-001 — Filename mismatch: `first_strategy-comparison.md` vs `first-strategy-comparison.md`

Status:              RESOLVED
Phase discovered:    0 (repository audit)
Area:                DOCS
Blocking phase:      NON_BLOCKING
Risk level:          LOW
Related docs:        `docs/03-strategy-research/first-strategy-comparison.md`, `README.md`, `docs/00-meta/current-project-state.md`, `docs/05-backtesting-validation/cost-modeling.md`

Description:
The on-disk filename was `docs/03-strategy-research/first_strategy-comparison.md` (underscore), while `README.md:243` and `docs/00-meta/current-project-state.md:366` referenced the dashed form `first-strategy-comparison.md`. `docs/05-backtesting-validation/cost-modeling.md:45` contains the natural-language phrase "first strategy comparisons" and is unaffected.

Why it matters:
Broken path references cause confusion during documentation reading and tool indexing, and cost-modeling's natural-language phrase was not part of the inconsistency. The mismatch is documentation-only and does not touch runtime safety, but was logged to leave a clean audit trail of the Phase 1 rename.

Options considered:
- Option A: rename file on disk to match docs (dashed form).
- Option B: edit both docs to match the on-disk underscore form.

Recommended resolution:
Option A — rename `first_strategy-comparison.md` → `first-strategy-comparison.md` using `git mv` (preserves history). After rename, both existing doc references become correct without further edits.

Operator decision:
Approved at Phase 1 gate-1 approval (2026-04-19). Option A.

Resolution evidence:
Rename applied via `git mv` in Phase 1 Step 2 on branch `phase-1/local-dev-foundation`. Will be included in the Phase 1 "docs: rename ..." commit after gate-2 approval.

---

## GAP-20260419-002 — Phase 1 tooling decisions confirmed

Status:              RESOLVED
Phase discovered:    1 (local development foundation)
Area:                TOOLING
Blocking phase:      NON_BLOCKING
Risk level:          LOW
Related docs:        `docs/00-meta/ai-coding-handoff.md` §"Phase 1", `docs/08-architecture/codebase-structure.md`

Description:
Phase 1 requires decisions that were not pre-specified in the handoff: package manager, Python version pin, dev-dependency mechanism, pre-commit/CI scoping. Operator approved each choice explicitly.

Decisions (2026-04-19):
- Package manager: `uv`.
- Python version policy: `>=3.11,<3.13`. Actual pin determined by the interpreter detected in Step 0 pre-flight.
- Pinned `.python-version`: `3.12` (host reports Python 3.12.4).
- Dev dependencies: PEP 735 `[dependency-groups]` in `pyproject.toml` (not `[project.optional-dependencies]`), installed automatically by `uv sync`.
- Pre-commit hooks: deferred. Tooling config in `pyproject.toml` only; no hook install.
- CI (GitHub Actions): deferred to the end of Phase 1; proposed separately once local ruff/mypy/pytest pass.
- Branching: feature branch `phase-1/local-dev-foundation` off `main`. Commits reviewed at Gate 2 before any `git commit`.
- Commit messages: no `Co-Authored-By` trailer unless explicitly requested later.

Why it matters:
These choices shape every subsequent phase. Recording them here gives future phases (and future audits) a single place to check what was decided and when, without spelunking through commit history.

Options considered:
See plan file `C:\Users\jpedr\.claude\plans\approved-to-start-phase-bubbly-whisper.md` §14 and §J for the alternatives weighed.

Recommended resolution:
As decided above.

Operator decision:
Approved 2026-04-19 with corrections (gate-1 corrections J.1–J.3 in the plan file).

Resolution evidence:
- `pyproject.toml` with `[dependency-groups] dev = [...]`.
- `.python-version` pinned to `3.12`.
- `uv.lock` generated by `uv sync`.
- Quality gates pass in Phase 1 Step 11.

---

## GAP-20260419-003 — `.python-version` was git-ignored; narrow `.gitignore` edit authorized

Status:              RESOLVED
Phase discovered:    1 (local development foundation, Step 5)
Area:                TOOLING
Blocking phase:      NON_BLOCKING
Risk level:          LOW
Related docs:        `.gitignore`, `pyproject.toml`, `docs/08-architecture/codebase-structure.md`

Description:
During Phase 1 Step 5, the intended commit of the root `.python-version` file was blocked because `.gitignore:16` excluded the pattern `.python-version` (under a `# Python` section alongside `__pycache__/`, `*.py[cod]`, `.venv/`, etc.). This prevented deterministic reproduction of the interpreter version by uv on fresh clones.

Why it matters:
`.python-version` is the first-class signal uv (and pyenv) read to select the project's Python interpreter. Without committing it, each contributor's environment is determined only by the broader `requires-python = ">=3.11,<3.13"` bound in `pyproject.toml`, which allows silent drift across 3.11/3.12 patch versions and leaves no single shared pin.

Options considered:
- Option A: remove the `.python-version` line from `.gitignore` (simplest, matches uv-first workflow).
- Option B: add `!/.python-version` as an explicit unignore rule at the bottom of `.gitignore` (more defensive if nested `.python-version` files ever appear — not expected here).
- Option C: drop the root `.python-version` pin entirely and rely on `pyproject.toml` `requires-python` only (loses determinism).

Recommended resolution:
Option A — remove the ignore line. Small, targeted edit within the `# Python` section. Root `.python-version` becomes trackable; no nested `.python-version` files are expected in this repo.

Operator decision:
Approved 2026-04-19 — Option A, narrow edit only, no `git add -f` usage. GAP logged in this file.

Resolution evidence:
- `.gitignore`: removed line `.python-version` between `*.pyd` and `.venv/`.
- `git check-ignore -v .python-version` now returns exit code 1 (not ignored).
- `.python-version` pinned to `3.12` per detected Python 3.12.4 interpreter.
- Will be included in Phase 1 Commit 2 (package + tooling foundation) after Gate 2 approval.

---

## GAP-20260419-004 — Phase 2 dependency pins and mypy overrides

Status:              RESOLVED
Phase discovered:    2 (historical data foundation, Steps 2-3)
Area:                TOOLING
Blocking phase:      NON_BLOCKING
Risk level:          LOW
Related docs:        `pyproject.toml`, `uv.lock`

Description:
`uv sync` resolved the three Phase 2 runtime dependencies as `pyarrow==23.0.1`, `duckdb==1.5.2`, `pydantic==2.13.2` (plus `pydantic-core==2.46.2`, `annotated-types==0.7.0`, `typing-inspection==0.4.2` as transitive). Neither `pyarrow` nor `duckdb` ships complete stubs for mypy strict mode, so `pyproject.toml` gained a `[[tool.mypy.overrides]]` block with `ignore_missing_imports = true` for those module namespaces.

Why it matters:
Future readers of the repo should know that calls into `pyarrow.*` and `duckdb.*` are effectively typed `Any` at the boundary. Code in `src/prometheus/research/data/storage.py` is still strictly typed at the Prometheus side; the leakage is limited to the third-party surface.

Options considered:
- Option A: add `ignore_missing_imports` overrides (simple, matches common Python data-project practice).
- Option B: install third-party stub packages (`pyarrow-stubs` or similar) — adds a dev dep with ongoing maintenance cost, and `duckdb` stubs are sparse.

Recommended resolution:
Option A — done.

Operator decision:
Pre-approved via Phase 2 Gate 1 condition 1. Versions within the declared `>=` floors.

Resolution evidence:
- `pyproject.toml`: `[project].dependencies` updated; `[[tool.mypy.overrides]]` added.
- `uv.lock`: regenerated by `uv sync`; 22 packages resolved; 6 new in Phase 2.
- `uv run mypy` passes on 15 source files.

---

## GAP-20260419-005 — Phase 2 scope reduction: no repo-root `data/` or `var/` skeletons created

Status:              RESOLVED
Phase discovered:    2 (historical data foundation, Step 4)
Area:                ARCHITECTURE
Blocking phase:      NON_BLOCKING
Risk level:          LOW
Related docs:        `docs/08-architecture/codebase-structure.md`, `.gitignore`, Phase 2 Gate 1 plan §6.4

Description:
The Phase 2 Gate 1 plan proposed creating `data/{raw,normalized,derived,manifests}/.gitkeep` and `var/{runtime,logs,reports,tmp}/.gitkeep` placeholder skeletons at the repo root. On closer review during execution, Phase 2 does not require any of them to exist pre-run: `storage.write_klines()` creates directories on demand via `Path.mkdir(parents=True, exist_ok=True)`, tests use `tmp_path`, and the `var/` tree is consumed by runtime code that does not yet exist. The `.gitignore` was updated narrowly to guard `data/raw/**`, `data/normalized/**`, `data/derived/**` content in case operators generate locally; `var/` was left untouched because the broad existing patterns (`runtime/`, `logs/`, `tmp/`) already cover it and adding `var/` sub-skeletons would have required layered unignore rules to preserve placeholders.

Why it matters:
If a later phase expects pre-existing `data/` or `var/` subdirectories as a precondition, that phase will need to either (a) `mkdir -p` on bootstrap, (b) re-propose the skeleton creation, or (c) rely on the operator to pre-create them. Phase 4 (runtime persistence) is the natural owner of `var/runtime/`.

Options considered:
- Option A: create all skeleton `.gitkeep` files + layered `.gitignore` overrides (larger diff).
- Option B: create the data/ skeleton only (one `.gitkeep`) plus narrow `.gitignore` rules (moderate).
- Option C: skip skeletons entirely; rely on `mkdir -p` at write time (smallest diff).

Recommended resolution:
Option C.

Operator decision:
Pre-approved via Phase 2 Gate 1 condition 5 ("if needed by the plan"). Scope reduction recorded here for audit.

Resolution evidence:
- No `data/` or `var/` directories created at the repo root during Phase 2.
- `.gitignore` gained 11 lines mirroring the existing `research/data/` pattern for `data/raw|normalized|derived/**`.

---

## GAP-20260419-006 — `configs/dev.example.yaml` `research_data` block is documentation-only

Status:              RESOLVED
Phase discovered:    2 (historical data foundation, Step 9)
Area:                TOOLING
Blocking phase:      NON_BLOCKING
Risk level:          LOW
Related docs:        `configs/dev.example.yaml`

Description:
Added a `research_data` block to `configs/dev.example.yaml` with keys `data_root`, `derived_root`, `manifests_root`, and `fixture_version`. There is no typed config loader yet — Phase 1 deferred the loader to Phase 4 — so these keys are pure documentation for operators running the pipeline manually. The test `test_dev_config_example_is_safe` continues to verify the safety-critical keys (`runtime_mode_on_start: SAFE_MODE`, `exchange_write_enabled: false`, `real_capital_enabled: false`).

Why it matters:
When Phase 4 introduces the config loader, the `research_data` block must either (a) be adopted by the schema, or (b) be refactored/renamed under a `research.data.*` namespace. If Phase 4 chooses to route research config through a separate file (e.g., `configs/research.example.yaml`), this block may migrate out of `dev.example.yaml`.

Options considered:
- Option A: add the block (documentation-only for now). Chosen.
- Option B: defer any config touching Phase 2 output paths to Phase 4 entirely.

Recommended resolution:
Option A — approved at Gate 1 condition 4.

Operator decision:
Pre-approved. No config loader added in Phase 2.

Resolution evidence:
- Four keys added to `configs/dev.example.yaml` under `research_data:`.
- No loader code in `src/prometheus/research/data/` consumes the block.

---

## GAP-20260419-007 — Top-level `data/` vs legacy `research/data/` tree — both tolerated

Status:              RESOLVED
Phase discovered:    2 (historical data foundation, Step 5)
Area:                DATA / ARCHITECTURE
Blocking phase:      NON_BLOCKING
Risk level:          LOW
Related docs:        `docs/08-architecture/codebase-structure.md`, `docs/04-data/historical-data-spec.md`, `.gitignore`

Description:
The repo's pre-Phase-1 state included a `research/data/{raw,normalized,derived}/` skeleton with matching `.gitignore` rules. `docs/08-architecture/codebase-structure.md` §"Target Repository Layout" specifies a top-level `data/{raw,normalized,derived,manifests}/` directory instead. The two locations conflict only in convention, not in code. Phase 2's `research_data.data_root` default points to the top-level `data/normalized/klines` per `codebase-structure.md`. The legacy `research/data/` skeleton was left in place with its existing `.gitkeep` and `.gitignore` rules; no cleanup performed.

Why it matters:
If a later phase expects the canonical output location to be `research/data/`, there is a documentation inconsistency with `codebase-structure.md`. A one-line clarification in `docs/04-data/historical-data-spec.md` or a cleanup of the legacy tree should be considered when Phase 2b (real data fetch) lands.

Options considered:
- Option A: keep both trees; route new writes to top-level `data/` per `codebase-structure.md`. Chosen.
- Option B: delete the legacy `research/data/` skeleton. Out of Phase 2 scope; requires operator approval.
- Option C: keep writes on `research/data/` and mark `data/` at repo root as deprecated. Contradicts `codebase-structure.md`.

Recommended resolution:
Option A — action deferred. Worth revisiting before Phase 2b to avoid duplication.

Operator decision:
Not yet decided; logged for later cleanup.

Resolution evidence:
- `.gitignore` now has parallel rules for both `research/data/` (existing) and `data/` (Phase 2 new).
- No code references the `research/data/` path.

---

## GAP-20260419-008 — Pydantic v2 strict mode required `BeforeValidator` helpers for JSON round-trip

Status:              RESOLVED
Phase discovered:    2 (historical data foundation, Step 10 test fixes)
Area:                TOOLING / DATA
Blocking phase:      NON_BLOCKING
Risk level:          LOW
Related docs:        `src/prometheus/research/data/manifests.py`, `src/prometheus/research/data/storage.py`

Description:
Two separate strict-mode coercion issues surfaced during test runs:

1. JSON deserialization of `DatasetManifest` returns Python lists for the `symbols`, `intervals`, `sources`, `partitioning`, `primary_key`, `invalid_windows` fields. Pydantic v2 strict mode does not accept `list` where `tuple[...]` is declared, and does not coerce `str` (e.g., `"BTCUSDT"`) to `Symbol.BTCUSDT`. Fix: `typing.Annotated` with `BeforeValidator` helpers (`_as_tuple`, `_as_symbol_tuple`, `_as_interval_tuple`) that coerce list -> tuple and convert string elements to the right `StrEnum` before strict validation runs.
2. Parquet round-trips expose `symbol` and `interval` columns as plain `str`. The `_row_to_kline` helper in `storage.py` now explicitly wraps the row's `symbol` and `interval` in `Symbol(...)` / `Interval(...)` before `NormalizedKline.model_validate(...)`.

Why it matters:
Strict validation is intentional — it guards the ingest boundary against typo'd fields, wrong column types, and silently-coerced values that could mask bugs. The `BeforeValidator` pattern keeps that guarantee while allowing legitimate JSON and Parquet inputs to deserialize cleanly. Future Pydantic models that travel through JSON or Parquet should follow the same pattern instead of loosening `strict`.

Options considered:
- Option A: keep strict mode, add `BeforeValidator` coercion. Chosen.
- Option B: switch fields to `list[X]` and loosen `strict`. Rejected — weaker invariant surface.
- Option C: serialize to a custom JSON schema that preserves types. Overkill for Phase 2.

Recommended resolution:
Option A — done.

Operator decision:
Pre-approved via Phase 2 Gate 1 condition 3 (module boundary and correct model typing).

Resolution evidence:
- `manifests.py` gained three `_as_*_tuple` helpers + three `Annotated[..., BeforeValidator(...)]` type aliases.
- `storage.py::_row_to_kline` converts `str -> Symbol` and `str -> Interval` before `model_validate`.
- All 79 tests pass; both the JSON round-trip test and the Parquet round-trip test exercise this path.

---

## GAP-20260419-010 — Binance USD-M bulk CSVs DO have a header row (contrary to Phase 2b TD-006 assumption)

Status:              RESOLVED
Phase discovered:    2b (historical download, Step 11 real bounded run)
Area:                DATA / EXCHANGE_API
Blocking phase:      PRE_PHASE_2B_COMPLETION (blocks the bounded real run)
Risk level:          HIGH (per Phase 2b Gate 1 condition 3: any divergence from verified source assumptions is logged at HIGH risk and escalated)
Related docs:        `src/prometheus/research/data/ingest.py`, `src/prometheus/research/data/binance_bulk.py` (TD-006 evidence block), `docs/00-meta/implementation-reports/2026-04-19_phase-2b_gate-1-plan.md`

Description:
During Phase 2b Step 11 (bounded real download of BTCUSDT 15m 2026-03 from `data.binance.vision`), the first real pipeline run failed at CSV parsing with:

```
DataIntegrityError: CSV line 1: failed to cast numeric field
  (invalid literal for int() with base 10: 'open_time')
```

Inspection of the downloaded ZIP confirmed it was checksum-verified correctly and contains a single member `BTCUSDT-15m-2026-03.csv`. The first line of that CSV is a column-name header:

```
open_time,open,high,low,close,volume,close_time,quote_volume,count,taker_buy_volume,taker_buy_quote_volume,ignore
```

Data rows follow from line 2 onward with valid UTC-ms timestamps, the expected 12 columns, and data starting at `2026-03-01T00:00:00Z` as expected.

The TD-006 verification evidence block in `binance_bulk.py` currently asserts **"No header row"** — this was an inference from the github.com/binance/binance-public-data README example (which shows column names in a table but does not explicitly state whether the CSV is row-1 header or row-1 data). The real on-disk file has a header, so the inference was wrong.

Secondary observations (not currently blocking):
- The header row's column names are slightly different from the README table labels (e.g., `quote_volume` in the file vs `Quote asset volume` in the README; `count` vs `Number of trades`; `taker_buy_volume` vs `Taker buy base asset volume`). Because `parse_binance_csv_row` parses by POSITION, not name, this does not affect correctness once the header is skipped.
- The ZIP's internal member name is `BTCUSDT-15m-2026-03.csv` (the ZIP filename with `.zip` replaced by `.csv`), matching the convention I tested for in `extract_rows_from_zip` by opening the single member regardless of name.

Why it matters:
The parser currently fails closed (correctly) but prevents the bounded real run from completing. All subsequent months and symbols would fail identically until the parser handles a header row.

Downloaded artifact that IS on disk (safe, checksum-verified, git-ignored):
- `data/raw/binance_usdm/klines/symbol=BTCUSDT/interval=15m/year=2026/month=03/BTCUSDT-15m-2026-03.zip`
- Size: 145,250 bytes
- SHA256 matches the published `.CHECKSUM`.

No normalized Parquet, no derived 1h, no manifest, no state file was written (parser failed before state update).

Options considered:
- **Option A:** skip the first CSV line if its first field is not a valid integer (minimal, defensive — works whether a header is present or not). Single-line change in `extract_rows_from_zip`.
- **Option B:** unconditionally skip the first line (assumes header always present, simpler, but brittle if Binance ever removes the header).
- **Option C:** validate the header against an expected set of column names before skipping (strictest — fails closed if column order changes).
- **Option D:** revert the 2b scope, abandon the real run, leave the downloader as mock-only.

Recommended resolution:
**Option A** — defensive first-line detection. Conditional on whether the first field parses as an int. Works on files with or without a header. Keeps `parse_binance_csv_row` unchanged and contained; the fix lives in `extract_rows_from_zip`.

Secondary fix: update the `## TD-006 verification evidence` docstring in `binance_bulk.py` to correct the "No header row" assertion and to cite this GAP entry.

Operator decision:
Approved 2026-04-19 — Option A with stricter header detection. Recognized header requires 12 comma-separated columns AND first field normalized/lowercased equals `open_time`. Non-numeric non-header first rows must fail loudly (no silent skipping of arbitrary malformed content).

Resolution evidence:
- `src/prometheus/research/data/ingest.py`: added `_is_kline_csv_header` helper and modified `extract_rows_from_zip` to skip the first row only if it is a recognized header; other non-numeric first rows raise `DataIntegrityError` as before.
- `src/prometheus/research/data/binance_bulk.py`: TD-006 evidence block updated. The "No header row" assertion is removed and replaced with a documented correction citing this GAP. Runtime detection and behavior described inline.
- `tests/unit/research/data/test_ingest.py`: added 9 new tests covering header detection and extraction paths — `test_is_header_recognizes_open_time`, `test_is_header_case_insensitive`, `test_is_header_rejects_numeric_first_field`, `test_is_header_rejects_wrong_column_count`, `test_is_header_rejects_similar_but_wrong_name`, `test_extract_skips_header_row`, `test_extract_works_without_header`, `test_extract_header_skip_preserves_data_rows`, `test_extract_rejects_non_numeric_non_header_first_row`, `test_extract_rejects_wrong_column_count_first_row`.
- Full test suite: **136 passed** in 0.85s (was 126 before the fix).
- Real bounded ingest completed successfully for both BTCUSDT and ETHUSDT 15m 2026-03:
  * BTCUSDT ZIP SHA256 `ea25e84ddffdcc8b7ba68fb47363daee6a9ef53941f152c9ebf6d4e165d32bf8` (matched pre-verified WebFetch checksum); 2976 × 15m bars, 744 × 1h derived bars, 0 invalid windows.
  * ETHUSDT ZIP SHA256 `8070870b512ab7c312329a7fc1a45217fc7aff5ed7bbb4f805d96caf7c99fd5d` (matched pre-verified WebFetch checksum); 2976 × 15m bars, 744 × 1h derived bars, 0 invalid windows.
- Manifests written: 4 × ~0.9 KB under `data/manifests/`. Download state files: 2 × 0.775 KB under `data/manifests/_downloads/`. All git-ignored.

---

## GAP-20260419-011 — DatasetManifest accepts empty intervals tuple (event-type datasets)

Status:              RESOLVED
Phase discovered:    2c (public market data completion, funding-rate ingest)
Area:                DATA / ARCHITECTURE
Blocking phase:      NON_BLOCKING
Risk level:          LOW
Related docs:        `src/prometheus/research/data/manifests.py`, `src/prometheus/research/data/ingest.py::ingest_funding_range`

Description:
Phase 2c funding-rate events are not bar-indexed and have no interval dimension. The Phase 2 :class:`DatasetManifest` model has a `symbols` non-empty validator but does not require `intervals` to be non-empty. Phase 2c confirmed that `intervals=()` is accepted by the model and round-trips through JSON write/read correctly.

Why it matters:
Future event-type datasets (open-interest, liquidation streams, etc.) can reuse the existing `DatasetManifest` without model changes.

Resolution evidence:
- Funding manifests `binance_usdm_btcusdt_funding__v001.manifest.json` and `binance_usdm_ethusdt_funding__v001.manifest.json` written successfully during the Phase 2c bounded run with `intervals=()` in each.

---

## GAP-20260419-012 — Binance fundingRate shares 500/5min/IP limit with fundingInfo

Status:              RESOLVED
Phase discovered:    2c (public market data completion, Step 3 TD-006 verification)
Area:                EXCHANGE_API / DATA
Blocking phase:      NON_BLOCKING
Risk level:          LOW
Related docs:        `src/prometheus/research/data/binance_rest.py`, `src/prometheus/research/data/funding_rate.py`

Description:
Operator flagged at Phase 2c Gate 1 condition 4 that `/fapi/v1/fundingRate` uses an IP-based request-count rate limit shared with `/fapi/v1/fundingInfo`, not a per-request weight. WebFetch of the official Get-Funding-Rate-History page on 2026-04-19 confirmed the verbatim wording: `"share 500/5min/IP rate limit with GET /fapi/v1/fundingInfo"`. 500 requests / 300 seconds / IP ~= 1.67 requests per second peak.

Resolution evidence:
- `binance_rest.py`: default `pace_ms=1000` (1 req/sec) chosen for ~40% margin below the documented peak.
- `funding_rate.py` module docstring cites the verbatim rate-limit wording.
- `configs/dev.example.yaml` `research_data.funding.pace_ms: 1000` with a comment referencing the verified limit.
- Bounded real run of BTC + ETH funding-rate for 2026-03 completed without 429 responses at the 1s pacing.

---

## GAP-20260419-013 — Mark-price bulk CSV column layout undocumented; parsed positionally

Status:              RESOLVED (by runtime observation)
Phase discovered:    2c (public market data completion, Step 3 source verification)
Area:                EXCHANGE_API / DATA
Blocking phase:      NON_BLOCKING
Risk level:          LOW
Related docs:        `src/prometheus/research/data/mark_price.py`

Description:
The github.com/binance/binance-public-data README does NOT document the CSV column layout for mark-price kline bulk files (confirmed via WebFetch 2026-04-19). The REST `/fapi/v1/markPriceKlines` endpoint returns 12-element arrays where volume-related fields are placeholder zeros; the bulk CSV was assumed to mirror that layout. `mark_price.py::parse_mark_price_csv_row` enforces 12 columns and extracts only the 6 meaningful positional fields (open_time, open, high, low, close, close_time).

Runtime verification during Phase 2c bounded run:
- BTCUSDT-15m-2026-03 mark-price ZIP parsed cleanly, 2976 rows extracted, all `MarkPriceKline` invariants passed.
- ETHUSDT-15m-2026-03 identical.
- SHA256s byte-for-byte match the WebFetch-captured values.

Resolution evidence:
- BTC mark-price SHA256 `79edfb409a35630cfb8894b883c2bcc4d5a3d6f78bf4d449585cc9e6e8f475e3` — captured via pre-run WebFetch and verified against the downloaded ZIP on 2026-04-19.
- ETH mark-price SHA256 `d30d71f35e0935783bedadcbc905537153c1e8980c1336a7c0403be12ba73762` — same.
- If Binance ever changes the column layout, `parse_mark_price_csv_row`'s column-count check raises `DataIntegrityError` loudly.

---

## GAP-20260419-009 — pytest `pythonpath` extended to include the repo root

Status:              RESOLVED
Phase discovered:    2 (historical data foundation, Step 8)
Area:                TOOLING
Blocking phase:      NON_BLOCKING
Risk level:          LOW
Related docs:        `pyproject.toml`, `tests/fixtures/market_data/synthetic.py`, `tests/integration/test_fixture_pipeline_end_to_end.py`

Description:
The Phase 2 end-to-end integration test imports the deterministic synthetic generator via `from tests.fixtures.market_data.synthetic import synthetic_15m_spec`. With `[tool.pytest.ini_options].pythonpath = ["src"]` alone, the `tests` package is not on `sys.path` when pytest collects it, so the import would fail. Fix: extend `pythonpath` to `["src", "."]` so tests can import other tests-tree modules.

Why it matters:
Any future test that wants to reuse a fixture module by direct import (rather than via a conftest fixture) depends on `.` being on `pythonpath`. The alternative — promoting every such helper to a conftest fixture — is viable but more verbose. Keeping `.` in `pythonpath` costs nothing at test time and avoids conftest plumbing.

Options considered:
- Option A: extend `pythonpath` to `["src", "."]`. Chosen.
- Option B: expose the synthetic generator as a conftest fixture (session-scoped). Rejected — the generator is stateless and benefits from direct importability in docstrings and review.
- Option C: put the generator under `src/prometheus/research/data/` as production code. Rejected — fixture data has no place in the production package.

Recommended resolution:
Option A — done.

Operator decision:
Implicit; the choice falls inside the Phase 2 Gate 1 scope ("Phase 2 data-layer pipeline with tests").

Resolution evidence:
- `pyproject.toml`: `pythonpath = ["src", "."]`.
- `tests/integration/test_fixture_pipeline_end_to_end.py` imports `tests.fixtures.market_data.synthetic`.
- `uv run pytest` passes.

---

## GAP-20260419-014 — 1h normalized ATR filter uses 1h ATR(20) and latest 1h close

Status:              RESOLVED
Phase discovered:    3 (Phase 3 Gate 1 plan §11.A.A1)
Area:                STRATEGY
Blocking phase:      NON_BLOCKING
Risk level:          MEDIUM
Related docs:        `docs/03-strategy-research/v1-breakout-strategy-spec.md`, `src/prometheus/strategy/v1_breakout/trigger.py`

Description:
The v1 breakout spec entry trigger condition 6 requires `0.20% <= ATR(20) / close <= 2.00%`, labeled "1h normalized ATR filter." The spec is ambiguous about which ATR (15m or 1h) and which close (15m signal bar's close or latest 1h close) to use.

Options considered:
- Option A: use 15m ATR(20) and 15m breakout-bar close (literal reading of the trigger context).
- Option B: use 1h ATR(20) and latest completed 1h close (literal reading of the "1h" label).

Operator decision:
Option B — use 1h ATR(20) and latest completed 1h close.

Resolution evidence:
- `src/prometheus/strategy/v1_breakout/trigger.py::_passes_atr_regime` accepts `atr_20_1h` and `latest_1h_close` parameters.
- `src/prometheus/strategy/v1_breakout/strategy.py::V1BreakoutStrategy.maybe_entry` sources `atr_20_1h` from `session.current_1h_atr_20()` and `latest_1h_close` from `session.latest_1h_close()`.
- `tests/unit/strategy/v1_breakout/test_trigger.py::test_normalized_atr_out_of_range_rejects` asserts rejection when `atr_20_1h / latest_1h_close < 0.20%`.

---

## GAP-20260419-015 — Stop-distance filter uses signal-bar close as reference

Status:              RESOLVED
Phase discovered:    3 (Phase 3 Gate 1 plan §11.A.A2)
Area:                STRATEGY
Blocking phase:      NON_BLOCKING
Risk level:          LOW
Related docs:        `src/prometheus/strategy/types.py`, `src/prometheus/strategy/v1_breakout/stop.py`, `src/prometheus/strategy/v1_breakout/strategy.py`

Description:
The stop-distance filter rejects trades with `stop_distance < 0.60 * ATR(20)` or `> 1.80 * ATR(20)`, where `stop_distance = abs(entry_price - initial_stop)`. In backtest, `entry_price` (next-bar open) is not known at signal-bar close time. A reference price must be chosen for the pre-fill filter evaluation.

Operator decision:
Option A — use the 15m signal bar's CLOSE as the reference price. All information available at signal time; avoids making trade approval depend on an as-yet-unobserved fill price.

Resolution evidence:
- `src/prometheus/strategy/v1_breakout/strategy.py::V1BreakoutStrategy.maybe_entry` sets `reference_price = breakout_bar.close`.
- `EntryIntent.reference_price` is documented as the signal-bar close proxy.

---

## GAP-20260419-016 — Managed-exit fills at next bar's open (same as entry)

Status:              RESOLVED
Phase discovered:    3 (Phase 3 Gate 1 plan §11.A.A3)
Area:                STRATEGY / BACKTEST
Blocking phase:      NON_BLOCKING
Risk level:          LOW
Related docs:        `src/prometheus/research/backtest/fills.py`, `src/prometheus/research/backtest/engine.py`

Description:
The backtest plan says managed exits (stagnation, trailing breach) fill at "the next available executable price." The phrase is ambiguous: either next-bar open or the close of the triggering bar.

Operator decision:
Option A — next-bar open, consistent with the entry fill baseline and the backtest plan's conservative philosophy.

Resolution evidence:
- `src/prometheus/research/backtest/fills.py::exit_fill_price` applies slippage to `next_bar.open`.
- `engine.py::_close_trade_managed` sources the exit price from `exit_fill_price(next_bar=...)`.

---

## GAP-20260419-017 — Gap-through stop rule: fill at bar open if gap, else stop level

Status:              RESOLVED
Phase discovered:    3 (Phase 3 Gate 1 plan §11.A.A4)
Area:                BACKTEST / EXECUTION
Blocking phase:      NON_BLOCKING
Risk level:          MEDIUM (materially affects tail losses)
Related docs:        `src/prometheus/research/backtest/stops.py`

Description:
When a mark-price bar crosses the stop level, two fill conventions are possible: (A) always fill at the stop level; (B) fill at the bar open if the bar opens BEYOND the stop (adverse gap), else at the stop level.

Operator decision:
Option B — realistic for STOP_MARKET behavior, which fills at market on trigger and will realize the adverse open price if the market has already gapped.

Resolution evidence:
- `src/prometheus/research/backtest/stops.py::evaluate_stop_hit` returns `StopHit.was_gap_through` flag and fills at `mark_bar.open` when the bar opens beyond the stop.
- `tests/unit/research/backtest/test_stops.py::TestLongStopHit::test_gap_through_fills_at_bar_open` and the short mirror assert the behavior.

---

## GAP-20260419-018 — Taker commission rate parameterized {0.05%, 0.04%, 0.02%}; primary 0.05%

Status:              ACCEPTED_LIMITATION
Phase discovered:    3 (Phase 3 Gate 1 plan §11.A.A5, §11.C.D2)
Area:                BACKTEST / EXCHANGE_API
Blocking phase:      PRE_TINY_LIVE (resolution requires Phase 2d authenticated endpoints)
Risk level:          MEDIUM
Related docs:        `src/prometheus/research/backtest/config.py`, `docs/03-strategy-research/v1-breakout-backtest-plan.md`

Description:
The authenticated `GET /fapi/v2/commissionRate` endpoint is deferred to Phase 2d. Phase 3 cannot query the live account's actual taker rate. The backtester parameterizes `taker_fee_rate` across {0.05%, 0.04%, 0.02%} (standard, small-discount, BNB-discount), with 0.05% as the primary conservative baseline. Sensitivity is reported via separate runs (different `run_id`).

Operator decision:
Accept as Phase 3 limitation. Documented as an accepted limitation in every `BacktestReportManifest.accepted_limitations` produced. Resolves fully when Phase 2d lands authenticated commissionRate fetch.

Resolution evidence:
- `BacktestConfig.taker_fee_rate` is a required configurable field; default 0.0005 in CLI.
- `DatasetCitation` and `accepted_limitations` fields on `BacktestReportManifest` allow per-run documentation of the placeholder.

---

## GAP-20260419-019 — Funding event join window inclusive both ends

Status:              RESOLVED
Phase discovered:    3 (Phase 3 Gate 1 plan §11.A.A6)
Area:                BACKTEST / DATA
Blocking phase:      NON_BLOCKING
Risk level:          LOW
Related docs:        `src/prometheus/research/backtest/funding_join.py`

Description:
The join predicate for applying a `FundingRateEvent` to an open position is `funding_time ∈ [entry_fill_time, exit_fill_time]`. The boundary convention (inclusive both ends vs. exclusive either side) is not specified in the data or backtest docs.

Operator decision:
Inclusive both ends: `T_entry <= funding_time <= T_exit`.

Resolution evidence:
- `src/prometheus/research/backtest/funding_join.py::apply_funding_accrual` uses the predicate `if entry_fill_time_ms <= event.funding_time <= exit_fill_time_ms`.
- `tests/unit/research/backtest/test_funding_join.py::test_inclusive_both_ends` asserts events exactly at entry time and exactly at exit time are included.

---

## GAP-20260419-020 — ExchangeInfo 2026-04-19 snapshot used as proxy for 2026-03 backtest window

Status:              ACCEPTED_LIMITATION
Phase discovered:    3 (Phase 3 Gate 1 plan §11.A.A7, §11.C.D1)
Area:                DATA / EXCHANGE_API
Blocking phase:      NON_BLOCKING for Phase 3 conformance; PRE_TINY_LIVE for live
Risk level:          LOW
Related docs:        `data/derived/exchange_info/2026-04-19T21-22-59Z.json`, `src/prometheus/research/backtest/report.py::DatasetCitation`

Description:
Phase 2c captured a single exchangeInfo snapshot on 2026-04-19. The backtester uses this for per-symbol filters (tickSize, stepSize, minNotional, precisions) when running on the 2026-03 window. If Binance changed any filter between 2026-03 and 2026-04-19, rounding assumptions could be marginally off. BTCUSDT filters change rarely; the proxy is acceptable for Phase 3 conformance but not for long-horizon promotion evidence.

Additionally, the snapshot does not currently have a `DatasetManifest` — it lives as a timestamp-named JSON under `data/derived/exchange_info/`. The validation-checklist Gate-1 "exchange metadata snapshots are available" criterion reads the snapshot via path + sha256 rather than a manifest version.

Operator decision:
Accept both (a) the snapshot-date proxy and (b) the absent-manifest handling as Phase 3 limitations, documented in every backtest report manifest.

Resolution evidence:
- `BacktestReportManifest.dataset_citations` accepts a `raw_file_path + raw_file_sha256` variant for the exchangeInfo snapshot.
- `accepted_limitations` field on the manifest records both limitations on every run.
- `tests/simulation/test_backtest_real_2026_03.py` loads `ExchangeInfoSnapshot` from the on-disk JSON and filters per symbol.

---

## GAP-20260419-021 — Phase 3 starting sizing_equity_usdt = 10,000 USDT (flat/non-compounding)

Status:              RESOLVED
Phase discovered:    3 (Phase 3 Gate 1 plan §11.B.R1)
Area:                RISK / BACKTEST
Blocking phase:      NON_BLOCKING
Risk level:          LOW
Related docs:        `src/prometheus/research/backtest/config.py`, `src/prometheus/research/backtest/accounting.py`

Description:
The risk docs define sizing_equity as `min(account_equity, strategy_allocated_equity)` but do not fix a numeric starting value. For Phase 3 research, a specific starting number is needed. The operator also specified the primary variant is FLAT (sizing_equity unchanged across trades; compounding variant may be reported as sensitivity only).

Operator decision:
`sizing_equity_usdt = 10_000.0` as the Phase 3 research default, with flat (non-compounding) sizing as the primary variant.

Resolution evidence:
- `BacktestConfig.sizing_equity_usdt` required positive float; CLI default 10_000.0.
- `Accounting.start(starting_equity=...)` holds the flat base; `equity` updates per trade but sizing math reads `sizing_equity_usdt` from config (not from `Accounting.equity`), preserving the flat variant.
- `docs/00-meta/implementation-reports/2026-04-19_phase-3_gate-1-plan.md` §11.B.R1 records the decision.

---

## GAP-20260419-022 — Risk-usage fraction in backtest: 0.90 primary, 1.00 sensitivity

Status:              RESOLVED
Phase discovered:    3 (Phase 3 Gate 1 plan §11.B.R2)
Area:                RISK / BACKTEST
Blocking phase:      NON_BLOCKING
Risk level:          LOW
Related docs:        `src/prometheus/research/backtest/sizing.py`, `docs/07-risk/position-sizing-framework.md`

Description:
The sizing framework's `risk_usage_fraction` default for initial live is 0.90 (a 10% buffer for friction). For backtest research the doc allows 1.00 as a "pure risk" sweep variant but does not mandate a choice.

Operator decision:
Primary = 0.90 (matches live sizing). Sensitivity runs may use 1.00 with different `run_id`.

Resolution evidence:
- `BacktestConfig.risk_usage_fraction` required in (0, 1]; CLI default 0.90.
- `sizing.py::compute_size` applies `risk_budget = risk_amount * risk_usage_fraction`.

---

## GAP-20260419-023 — Research internal notional cap = 100,000 USDT (not the live cap)

Status:              RESOLVED
Phase discovered:    3 (Phase 3 Gate 1 plan §11.B.R3)
Area:                RISK / BACKTEST
Blocking phase:      NON_BLOCKING for Phase 3; live notional cap remains TD-018
Risk level:          LOW
Related docs:        `src/prometheus/research/backtest/config.py`, `docs/12-roadmap/technical-debt-register.md#TD-018`

Description:
TD-018 defers the tiny-live notional cap value to pre-tiny-live. For Phase 3 research, a cap value must still be configured so the cap-binding behavior in `sizing.py` is exercised. A research cap of 100_000 USDT is high enough to not bind for typical BTC/ETH sizes at 0.25% risk with 10k equity, low enough to catch configuration typos.

Operator decision:
`max_notional_internal_usdt = 100_000.0` as the Phase 3 research default. Distinct from the live tiny-live cap (TD-018 remains OPEN).

Resolution evidence:
- `BacktestConfig.max_notional_internal_usdt` required positive; CLI default 100_000.0.
- Summary metrics report `sizing_limited_by` so it is observable when the cap binds.
- TD-018 is NOT resolved or edited by this entry.

---

## GAP-20260419-024 — Validation Gate 1 "leverageBracket + commissionRate snapshots" accepted as placeholder limitation

Status:              ACCEPTED_LIMITATION
Phase discovered:    3 (Phase 3 Gate 1 plan §11.C.D2)
Area:                DATA / EXCHANGE_API / BACKTEST
Blocking phase:      PRE_TINY_LIVE (resolution requires Phase 2d authenticated endpoints)
Risk level:          MEDIUM
Related docs:        `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`, `docs/03-strategy-research/v1-breakout-backtest-plan.md`

Description:
Validation checklist Gate 1 requires "leverage bracket snapshots are available" and "commission-rate assumptions are explicit and documented." Both endpoints are authenticated (`/fapi/v1/leverageBracket`, `/fapi/v2/commissionRate`) and were deferred to Phase 2d. Phase 3 proceeds with:
- no leverage-bracket check (v1 cap of 2x effective leverage is far below any published bracket threshold for BTCUSDT/ETHUSDT, so not exercising the check does not create unsafe assumptions)
- parameterized commissionRate sensitivity per GAP-20260419-018

This is a strict reading of Gate 1 noncompliance, accepted explicitly by operator at Phase 3 Gate 1 approval.

Operator decision:
Accept as Phase 3 limitation. Documented on every `BacktestReportManifest.accepted_limitations`. NOT silently resolved. Phase 2d remains OPEN as a separate operator-approved task.

Resolution evidence:
- `BacktestReportManifest.accepted_limitations` field records the limitation text per run.
- `docs/00-meta/implementation-reports/2026-04-19_phase-3_gate-1-plan.md` §11.C.D2 records the operator approval.
- `docs/00-meta/implementation-reports/2026-04-19_phase-3_gate-1-plan.md` §0 Executive Summary flags this explicitly.

---

## GAP-20260419-025 — Phase 2e wider historical backfill proposed; Phase 3 completes on 2026-03 only

Status:              DEFERRED
Phase discovered:    3 (Phase 3 Gate 1 plan §11.D.DS1)
Area:                DATA / ROADMAP
Blocking phase:      PRE_VALIDATION_GATES_4_6 (walk-forward, robustness, ETH comparison at scale)
Risk level:          HIGH if conflated with Phase 3 scope; NON_BLOCKING for Phase 3 conformance scope
Related docs:        `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`, `docs/05-backtesting-validation/walk-forward-validation.md`, Phase 3 Gate 1 plan §11.D

Description:
2026-03 real data (31 days) is sufficient to demonstrate Phase 3 strategy conformance and backtester mechanics. It is insufficient for Validation Gates 4 (walk-forward), 5 (BTC/ETH robustness comparison), and 6 (exit-model comparison). Those gates require multi-year history.

Operator decision:
Defer. Phase 3 makes NO profitability, robustness, or walk-forward promotion claims from the 2026-03 sample. A separate operator-approved "Phase 2e — wider historical backfill" task will propose BTC + ETH 15m bulk for a wider range (e.g., 2022-01 through 2026-03) using the existing `BulkDownloader` before walk-forward validation begins.

Resolution evidence:
- `docs/00-meta/implementation-reports/2026-04-19_phase-3_gate-1-plan.md` §11.D.DS1 records the operator-approved deferral and the Phase 2e proposal.
- `BacktestReportManifest.accepted_limitations` records the 31-day-only scope per run.
- No Phase 3 tests attempt Gate 4/5/6 validation.

---


