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


