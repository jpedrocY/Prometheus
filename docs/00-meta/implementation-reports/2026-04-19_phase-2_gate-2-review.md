# Phase 2 — Gate 2 Review

**Date:** 2026-04-19
**Phase:** 2 — Historical Data and Validation Foundation
**Branch:** `phase-2/historical-data-foundation` (off `main` at `fd64041`, not pushed)
**Status at time of report:** Working-tree only. No commits on the Phase 2 branch yet. Awaiting operator Gate 2 approval.

> **Gate 2 operator-requested correction applied (2026-04-19 post-review).** `.gitignore` was extended with a narrow rule for `data/manifests/` to match the `manifests_root: data/manifests` key in `configs/dev.example.yaml`. The block now reads:
>
> ```
> data/raw/**
> data/normalized/**
> data/derived/**
> data/manifests/**
> !data/raw/**/
> !data/normalized/**/
> !data/derived/**/
> !data/manifests/**/
> !data/**/.gitkeep
> ```
>
> No `data/manifests/` skeleton directory is created; no generated manifests are written under `data/manifests/` by Phase 2 (the two committed reference manifests remain under `tests/fixtures/market_data/manifests/`, not `data/manifests/`). Quality gates re-run clean after the edit: ruff + ruff format + mypy + pytest (79 passed in 0.38s).

---

## 1. Purpose

This report is the Gate 2 review artifact for Phase 2. It captures all changes produced by the approved Phase 2 execution plan (plan: `docs/00-meta/implementation-reports/2026-04-19_phase-2_gate-1-plan.md`) so the operator can review before authorizing commits.

All 79 tests pass; ruff, ruff format, and mypy all pass. No network calls. No credentials. No exchange code. No MCP, no Graphify. `phase-2/historical-data-foundation` is 0 commits ahead of `main`; everything below is working-tree state.

---

## 2. Operator conditions at Gate 1 (recap)

| # | Condition | Status |
| --- | --- | --- |
| 1 | Deps: `pyarrow` + `duckdb` + `pydantic` added via uv/pyproject | **Satisfied.** Resolved to `pyarrow==23.0.1`, `duckdb==1.5.2`, `pydantic==2.13.2`. |
| 2 | Synthetic fixtures only, no network except uv resolution | **Satisfied.** No HTTP code. Tests offline. |
| 3 | Module boundary: `src/prometheus/core/` + `src/prometheus/research/data/` only | **Satisfied.** No other packages created. |
| 4 | `configs/dev.example.yaml` narrowly extended with `research_data` block; no loader | **Satisfied.** 9-line addition, documentation-only. |
| 5 | Narrow `.gitignore` updates; preserve existing skeletons | **Satisfied.** 11-line addition mirroring the existing `research/data/` rule. Scope-reduced: no `data/` / `var/` `.gitkeep` skeletons (GAP-005). |
| 6 | Ambiguity log + Gate 2 review report under `implementation-reports/` | **Satisfied.** Six new GAP entries (004-009). This report at the approved path. |
| 7 | Phase boundaries — no Phase 3 start, no real data, no live API, no exchange write | **Satisfied.** |

---

## 3. Pre-flight (Step 0)

```
uv --version      → uv 0.11.7
python --version  → Python 3.12.4
where uv          → C:\Users\jpedr\.local\bin\uv.exe
git branch (head) → main, sync 0/0 with origin
```

One expected untracked file at pre-flight time: the Phase 2 Gate 1 plan (`2026-04-19_phase-2_gate-1-plan.md`). Carried forward into the Phase 2 branch — matches Phase 1 precedent of committing review reports inside their phase branch.

---

## 4. Commands run (in order)

| # | Command | Exit |
| --- | --- | --- |
| 1 | `git -C c:/Prometheus checkout -b phase-2/historical-data-foundation` | 0 |
| 2 | Edit `pyproject.toml` → add 3 runtime deps | n/a |
| 3 | `cd c:/Prometheus && uv sync` | 0 |
| 4 | Edit `.gitignore` → add narrow `data/...` rules | n/a |
| 5 | Write `src/prometheus/core/*.py` (5 files + `__init__.py`) | n/a |
| 6 | Write `tests/unit/core/*.py` (5 files + `__init__.py`) | n/a |
| 7 | Write `src/prometheus/research/__init__.py` and `src/prometheus/research/data/*.py` (7 files) | n/a |
| 8 | Edit `pyproject.toml` → add `[[tool.mypy.overrides]]` for pyarrow/duckdb | n/a |
| 9 | Write `tests/unit/research/data/*.py` (5 files + `__init__.py`) + `tests/unit/research/__init__.py` | n/a |
| 10 | Edit `pyproject.toml` → extend pytest `pythonpath` to `["src", "."]` | n/a |
| 11 | Write `tests/fixtures/*` (synthetic generator + 2 committed manifests) | n/a |
| 12 | Write `tests/integration/test_fixture_pipeline_end_to_end.py` | n/a |
| 13 | Edit `configs/dev.example.yaml` → add `research_data:` block | n/a |
| 14 | `uv run ruff check .` | 0 (after fixing one E501) |
| 15 | `uv run ruff format .` (auto-format 5 files) | 0 |
| 16 | `uv run ruff format --check .` | 0 |
| 17 | `uv run mypy` | 0 |
| 18 | `uv run pytest` | 0 (after four targeted bug fixes; see §10) |
| 19 | `git status` / `git diff --stat` / `git diff` | 0 |

No push, no commit, no `git add`. No `git add -f`. No destructive git. No credential handling.

---

## 5. `uv sync` output summary

```
Using CPython 3.12.4 interpreter at: C:\Users\jpedr\anaconda3\python.exe
Resolved 22 packages in 451ms
   Building prometheus @ file:///C:/Prometheus
Prepared 7 packages in 4.21s
Installed 7 packages in 410ms
 + annotated-types==0.7.0
 + duckdb==1.5.2
 ~ prometheus==0.0.0 (from file:///C:/Prometheus)
 + pyarrow==23.0.1
 + pydantic==2.13.2
 + pydantic-core==2.46.2
 + typing-inspection==0.4.2
```

Total environment size: 22 packages. `uv.lock` grew by 147 lines to carry the new dependency tree. No wheel / compiler / Windows path issues.

---

## 6. Files changed

### 6.1 Modified tracked files

```
.gitignore                (+11 lines: narrow repo-root data/ rules)
configs/dev.example.yaml  (+9 lines: research_data: block, documentation-only)
pyproject.toml            (+12, -2: runtime deps, mypy overrides, pytest pythonpath)
uv.lock                   (+147 lines: deterministic regeneration by uv sync)
```

### 6.2 Untracked new files (34)

Source (7 files):
```
src/prometheus/core/__init__.py
src/prometheus/core/errors.py
src/prometheus/core/intervals.py
src/prometheus/core/klines.py
src/prometheus/core/symbols.py
src/prometheus/core/time.py
src/prometheus/research/__init__.py
src/prometheus/research/data/__init__.py
src/prometheus/research/data/derive.py
src/prometheus/research/data/fetch.py
src/prometheus/research/data/manifests.py
src/prometheus/research/data/normalize.py
src/prometheus/research/data/quality.py
src/prometheus/research/data/storage.py
```

Tests (17 files):
```
tests/unit/core/__init__.py
tests/unit/core/test_intervals.py
tests/unit/core/test_klines.py
tests/unit/core/test_symbols.py
tests/unit/core/test_time.py
tests/unit/research/__init__.py
tests/unit/research/data/__init__.py
tests/unit/research/data/test_derive.py
tests/unit/research/data/test_manifests.py
tests/unit/research/data/test_normalize.py
tests/unit/research/data/test_quality.py
tests/unit/research/data/test_storage.py
tests/fixtures/__init__.py
tests/fixtures/market_data/__init__.py
tests/fixtures/market_data/manifests/synthetic_btcusdt_15m__v001.manifest.json
tests/fixtures/market_data/manifests/synthetic_ethusdt_15m__v001.manifest.json
tests/fixtures/market_data/synthetic.py
tests/integration/__init__.py
tests/integration/test_fixture_pipeline_end_to_end.py
```

Docs (2 files, both under `docs/00-meta/implementation-reports/`):
```
docs/00-meta/implementation-reports/2026-04-19_phase-2_gate-1-plan.md
docs/00-meta/implementation-reports/2026-04-19_phase-2_gate-2-review.md   ← this file
```

Plus a pending update: `docs/00-meta/implementation-ambiguity-log.md` has new entries GAP-004 through GAP-009 (not shown as a separate path here; it was already tracked from Phase 1, appears under "modified" once staged).

---

## 7. `git status`

```
On branch phase-2/historical-data-foundation
Changes not staged for commit:
  modified:   .gitignore
  modified:   configs/dev.example.yaml
  modified:   docs/00-meta/implementation-ambiguity-log.md
  modified:   pyproject.toml
  modified:   uv.lock

Untracked files:
  docs/00-meta/implementation-reports/2026-04-19_phase-2_gate-1-plan.md
  docs/00-meta/implementation-reports/2026-04-19_phase-2_gate-2-review.md
  src/prometheus/core/
  src/prometheus/research/
  tests/fixtures/
  tests/integration/
  tests/unit/core/
  tests/unit/research/
```

No staged changes. Zero files outside the Gate 1 manifest (after the recorded scope reductions).

---

## 8. `git diff --stat` (tracked files only, uv.lock excluded for brevity)

```
 .gitignore               | 11 +++++++++++
 configs/dev.example.yaml |  9 +++++++++
 pyproject.toml           | 12 ++++++++++--
 3 files changed, 30 insertions(+), 2 deletions(-)
```

`uv.lock` separately: +147 lines. Full listing available via `git diff uv.lock`.

---

## 9. `git diff` (tracked files only, uv.lock excluded)

```diff
diff --git a/.gitignore b/.gitignore
@@ -46,6 +46,17 @@ research/data/derived/**
 !research/data/derived/**/
 !research/data/**/.gitkeep

+# Phase 2: repo-root data/ output root (same pattern as research/data/).
+# Parquet datasets and derived artifacts generated locally must not be committed.
+# Track any .gitkeep placeholders if operators choose to materialize the skeleton.
+data/raw/**
+data/normalized/**
+data/derived/**
+!data/raw/**/
+!data/normalized/**/
+!data/derived/**/
+!data/**/.gitkeep
+
 # Generated artifacts
 artifacts/

diff --git a/configs/dev.example.yaml b/configs/dev.example.yaml
@@ -13,3 +13,12 @@ symbol: BTCUSDT
 risk_fraction: 0.0025
 max_effective_leverage: 2.0
 internal_notional_cap_usdt: null   # must be set explicitly before any live stage
+
+# Phase 2 research-data output paths (local, git-ignored).
+# Example values only; there is no config loader yet, so these keys are
+# documentation for operators running the pipeline manually.
+research_data:
+  data_root: data/normalized/klines
+  derived_root: data/derived
+  manifests_root: data/manifests
+  fixture_version: v001

diff --git a/pyproject.toml b/pyproject.toml
@@ -6,7 +6,11 @@ readme = "README.md"
 requires-python = ">=3.11,<3.13"
 license = { text = "Proprietary" }
 authors = [{ name = "Prometheus operator" }]
-dependencies = []
+dependencies = [
+    "pyarrow>=17",
+    "duckdb>=1.1",
+    "pydantic>=2.8",
+]

@@ -48,7 +52,11 @@ strict = true
 files = ["src/prometheus"]
 warn_unused_configs = true

+[[tool.mypy.overrides]]
+module = ["pyarrow", "pyarrow.*", "duckdb", "duckdb.*"]
+ignore_missing_imports = true
+
 [tool.pytest.ini_options]
 testpaths = ["tests"]
 addopts = "-q --strict-markers"
-pythonpath = ["src"]
+pythonpath = ["src", "."]
```

---

## 10. Quality-gate results (Step 10)

```
$ uv run ruff check .
All checks passed!                                          (ec=0)

$ uv run ruff format --check .
36 files already formatted                                  (ec=0)

$ uv run mypy
Success: no issues found in 15 source files                 (ec=0)

$ uv run pytest
........................................................................ [ 91%]
.......                                                                  [100%]
79 passed in 0.37s                                          (ec=0)
```

Test count went from 2 (end of Phase 1) to **79** (end of Phase 2). Added coverage spans:

- `core/`: intervals (4), symbols (2), time (9), klines (12) — 27 tests
- `research/data/manifests`: 11 tests (round-trip, overwrite refusal, version pattern, predecessor linkage, extra-field rejection, invalid-window backwards range)
- `research/data/normalize`: 4 tests (happy path, row-index error reporting, unaligned rows)
- `research/data/derive`: 9 tests (empty input, single/two complete buckets, partial bucket, mixed, unaligned input, symbol-mix rejection, no-forward-leakage at decision time)
- `research/data/quality`: 14 tests (duplicates, monotonic, missing detection including run detection, no-future-bars)
- `research/data/storage`: 10 tests (partition_path format + month validation, write/read round-trip, custom file metadata, expected columns, multi-symbol partition split, symbol filter on read, empty-root behavior, DuckDB row count, DuckDB predicate filter, view-name validation)
- `integration`: 2 tests (BTCUSDT 24h end-to-end + ETHUSDT parallel)

### Test failures encountered during development (all fixed before this report)

Four failure classes hit during the first full pytest run; all resolved with targeted fixes documented in GAP-008:

1. `_row_to_kline` strict-mode `str → Symbol/Interval` coercion — added explicit enum construction.
2. `DatasetManifest` JSON round-trip needed list→tuple and str→enum coercion — added `BeforeValidator` helpers.
3. `pq.read_table(single_file)` failing with "incompatible types: string vs dictionary<string>" when the path contained Hive-style segments — switched that test to `pq.ParquetFile(path).read()`.
4. DuckDB's `read_parquet` rejecting a parameterized path argument — inlined the path (with a `'`-containing-path guard against injection).

Runtime: 0.37s for the full suite. Very fast — no network, no large datasets.

---

## 11. Phase 2 Gate 1 acceptance-criteria self-check

From `docs/00-meta/ai-coding-handoff.md` §"Phase 2" and the Gate 1 plan §F:

| Criterion | Result |
| --- | --- |
| Historical data path is reproducible | **Pass** — Hive-partitioned Parquet, deterministic synthetic generator, full round-trip test. |
| Timestamp policy is enforced in tests | **Pass** — `test_time.py`, `test_klines.py`, `test_derive.py::test_derived_1h_bar_close_time_is_strictly_before_next_hour`, `test_derive.py::test_no_forward_leakage_past_decision_time`. |
| Data integrity checks exist | **Pass** — `check_no_duplicates`, `check_timestamp_monotonic`, `check_no_missing_bars`, `check_no_future_bars`; 14 tests. |
| Dataset versioning is represented | **Pass** — `DatasetManifest` with `<name>__v<NNN>` version pattern, immutability, predecessor linkage. |
| BTCUSDT and ETHUSDT research requirements supported in design | **Pass** — both symbols covered by `_SYMBOL_CONFIG`, both integration tests pass, both committed manifests reference the symbol's canonical metadata. |
| No live runtime state is mixed into research storage | **Pass** — `src/prometheus/research/data/` is self-contained; does not import `persistence`, `runtime`, `execution`, `exchange`, or `operator` modules (none of which exist anyway). |

Additional safety criteria (from plan §21):

| Check | Result |
| --- | --- |
| Production Binance keys | None. |
| Real secrets | None. |
| Exchange-write code | None. |
| `.mcp.json` | Not created. |
| Graphify | Not enabled. |
| Live API calls | None — all tests offline. |
| `.claude/*` | Not modified. |
| Runtime DB | Not touched (Phase 4 scope). |
| Destructive git | None. |
| `git add -f` | Not used. |

---

## 12. Ambiguity-log entries created (Phase 2)

Appended to `docs/00-meta/implementation-ambiguity-log.md`:

| ID | Area | Status | Summary |
| --- | --- | --- | --- |
| GAP-20260419-004 | TOOLING | RESOLVED | Dep pins + mypy ignore_missing_imports overrides for pyarrow/duckdb. |
| GAP-20260419-005 | ARCHITECTURE | RESOLVED | Phase 2 scope reduction — no `data/`/`var/` skeleton dirs created; only .gitignore rules added. |
| GAP-20260419-006 | TOOLING | RESOLVED | `configs/dev.example.yaml` `research_data` block is documentation-only; no loader. |
| GAP-20260419-007 | DATA / ARCHITECTURE | RESOLVED | Top-level `data/` vs legacy `research/data/` — both tolerated; Phase 2 writes route to top-level per codebase-structure.md. Worth revisiting at Phase 2b. |
| GAP-20260419-008 | TOOLING / DATA | RESOLVED | Pydantic v2 strict mode required `BeforeValidator` helpers for JSON round-trip of enum-typed tuples. |
| GAP-20260419-009 | TOOLING | RESOLVED | pytest `pythonpath` extended to include `.` so `tests.fixtures.*` modules are importable. |

All six are NON_BLOCKING, LOW risk. No CRITICAL items. No safety-relevant unresolved gaps at end of Phase 2.

---

## 13. Proposed commit structure (awaiting Gate 2 approval)

Five small commits on `phase-2/historical-data-foundation`, plus a post-Gate-2 checkpoint commit. Each groups logically; none exceeds a reviewable size. Order matters because later commits depend on earlier ones passing type-check + tests.

### Commit 1 — `phase-2: add pyarrow + duckdb + pydantic; narrow .gitignore rules`

Staging:

```
pyproject.toml         (runtime deps + mypy overrides + pytest pythonpath)
uv.lock                (regenerated)
.gitignore             (narrow data/** additions)
```

Message:

```
phase-2: add pyarrow + duckdb + pydantic; narrow .gitignore rules

Adds runtime dependencies pyarrow>=17, duckdb>=1.1, pydantic>=2.8 for
historical data storage and validation (resolved by uv sync as
pyarrow==23.0.1, duckdb==1.5.2, pydantic==2.13.2). Adds
ignore_missing_imports overrides for pyarrow.* and duckdb.* since
neither ships complete stubs (GAP-20260419-004). Extends pytest
pythonpath to ["src", "."] so fixture modules under tests/ are
importable from other test files (GAP-20260419-009).

Extends .gitignore with narrow rules for data/raw|normalized|derived/**
mirroring the existing research/data/** pattern. No data/ or var/
skeleton directories are created (scope reduction per
GAP-20260419-005); directories will be created on demand by
storage.write_klines().
```

### Commit 2 — `phase-2: core primitives (time, symbols, intervals, NormalizedKline)`

Staging:

```
src/prometheus/core/__init__.py
src/prometheus/core/errors.py
src/prometheus/core/intervals.py
src/prometheus/core/klines.py
src/prometheus/core/symbols.py
src/prometheus/core/time.py
tests/unit/core/__init__.py
tests/unit/core/test_intervals.py
tests/unit/core/test_klines.py
tests/unit/core/test_symbols.py
tests/unit/core/test_time.py
```

Message:

```
phase-2: core primitives (time, symbols, intervals, NormalizedKline)

Adds src/prometheus/core/ per docs/08-architecture/codebase-structure.md:
  - time.py: UTC ms helpers (utc_now_ms, floor_to_interval,
    is_aligned_open_time, close_time_for) with injectable clock.
  - intervals.py: Interval StrEnum (I_15M, I_1H) + duration lookup.
  - symbols.py: Symbol StrEnum (BTCUSDT, ETHUSDT).
  - klines.py: NormalizedKline Pydantic model matching the exact
    14-column schema from docs/04-data/historical-data-spec.md;
    frozen, strict, extra=forbid, with OHLC/alignment/close_time
    invariants enforced at construction.
  - errors.py: PrometheusError / DataIntegrityError / ManifestError.

27 tests cover happy paths and strict-mode rejections.
```

### Commit 3 — `phase-2: research/data — manifests, Parquet storage, DuckDB view`

Staging:

```
src/prometheus/research/__init__.py
src/prometheus/research/data/__init__.py
src/prometheus/research/data/manifests.py
src/prometheus/research/data/storage.py
tests/unit/research/__init__.py
tests/unit/research/data/__init__.py
tests/unit/research/data/test_manifests.py
tests/unit/research/data/test_storage.py
```

Message:

```
phase-2: research/data manifests, Parquet storage, DuckDB view

Adds the storage half of the Phase 2 research data pipeline:

  - manifests.py: DatasetManifest + InvalidWindow Pydantic models
    matching docs/04-data/dataset-versioning.md. Version pattern
    <name>__v<NNN>, predecessor linkage enforced, JSON round-trip
    via BeforeValidator helpers (GAP-20260419-008), immutable
    writes refuse to overwrite (ManifestError).
  - storage.py: Hive-partitioned Parquet writer
    (symbol=/interval=/year=/month=/) with zstd-level-3 + 64k
    row groups + custom file metadata (dataset/schema/pipeline
    version). read_klines via pyarrow.dataset; DuckDB view via
    read_parquet(hive_partitioning=1) with inlined path
    (DuckDB rejects prepared params for table paths).

21 tests covering round-trips, filters, partition splits,
metadata preservation, and view queries.
```

### Commit 4 — `phase-2: research/data — normalize, derive, quality, fetch`

Staging:

```
src/prometheus/research/data/derive.py
src/prometheus/research/data/fetch.py
src/prometheus/research/data/normalize.py
src/prometheus/research/data/quality.py
tests/unit/research/data/test_derive.py
tests/unit/research/data/test_normalize.py
tests/unit/research/data/test_quality.py
```

Message:

```
phase-2: research/data normalize, derive, quality, fetch scaffold

Adds the pipeline half of the Phase 2 research data layer:

  - normalize.py: normalize_rows validates raw dict rows into
    NormalizedKline, reporting row-index on failure.
  - derive.py: derive_1h_from_15m aggregates 15m bars into
    completed 1h bars; partial buckets return as InvalidWindow
    rather than silently filled.
  - quality.py: check_no_duplicates, check_timestamp_monotonic,
    check_no_missing_bars (with contiguous-gap detection),
    check_no_future_bars.
  - fetch.py: HistoricalKlineSource Protocol + FixtureKlineSource
    concrete implementation. No network code - real fetchers are
    deferred to a separate Phase 2b approval.

27 tests; no-forward-leakage-at-decision-time test encodes the
timestamp-policy.md rule directly.
```

### Commit 5 — `phase-2: synthetic fixtures, end-to-end integration test, gate-1/2 reports`

Staging:

```
configs/dev.example.yaml
tests/fixtures/__init__.py
tests/fixtures/market_data/__init__.py
tests/fixtures/market_data/synthetic.py
tests/fixtures/market_data/manifests/synthetic_btcusdt_15m__v001.manifest.json
tests/fixtures/market_data/manifests/synthetic_ethusdt_15m__v001.manifest.json
tests/integration/__init__.py
tests/integration/test_fixture_pipeline_end_to_end.py
docs/00-meta/implementation-ambiguity-log.md
docs/00-meta/implementation-reports/2026-04-19_phase-2_gate-1-plan.md
docs/00-meta/implementation-reports/2026-04-19_phase-2_gate-2-review.md
```

Message:

```
phase-2: synthetic fixtures, end-to-end integration, reports

Adds the deterministic BTCUSDT/ETHUSDT synthetic generator
(tests/fixtures/market_data/synthetic.py) plus committed reference
manifests for both fixture datasets. No Parquet binaries committed.

Integration test exercises the full pipeline offline:
  FixtureKlineSource -> normalize_rows -> write_klines (Parquet +
  Hive + metadata) -> read_klines round-trip -> attach_dataset_view
  (DuckDB) -> query_completed_bars -> derive_1h_from_15m ->
  quality checks -> DatasetManifest write/read (immutability).

Adds research_data block to configs/dev.example.yaml as
documentation-only (GAP-20260419-006). Appends GAP-004..009 to
the implementation-ambiguity-log. Saves the Phase 2 Gate 1 plan
and Gate 2 review under docs/00-meta/implementation-reports/ for
the project audit trail.
```

### Commit 6 (post-Gate-2) — `phase-2: checkpoint report`

After Commit 5 lands, I will produce the Phase 2 checkpoint report at `docs/00-meta/implementation-reports/2026-04-19_phase-2-checkpoint-report.md` and commit it separately, matching the Phase 1 precedent. TD register flips (if any) can be bundled in.

No push. No PR during Phase 2 execution. Operator decides when to push and merge.

---

## 14. Items explicitly out of scope (confirmed untouched)

- `CLAUDE.md`
- `README.md`
- `docs/00-meta/current-project-state.md`
- All specialist docs under `docs/03-strategy-research/`, `docs/04-data/`, `docs/05-backtesting-validation/`, `docs/06-execution-exchange/`, `docs/07-risk/`, `docs/08-architecture/`, `docs/09-operations/`, `docs/10-security/`, `docs/11-interface/`, `docs/12-roadmap/`
- `.claude/` (agents, rules, settings)
- `.mcp.example.json`, `.mcp.graphify.template.json` (templates untouched)
- `.mcp.json` — not created (confirmed by `git check-ignore` and `ls`).
- `research/`, `infra/`, `notebooks/` top-level directories — untouched; their `.gitkeep` files preserved.
- No strategy, risk, execution, exchange, persistence, operator, runtime, dashboard, or market_data runtime modules introduced.
- No existing tests broken. Phase 1's two smoke tests still pass (`test_package_importable`, `test_dev_config_example_is_safe`).

---

## 15. Recommended next step

Operator reviews this report and §§6–10 above. If approved (Gate 2):

1. I run the five `git commit` commands in §13 in order.
2. I verify `git log --oneline -8` shows the new commits stacked on `fd64041`.
3. I produce the Phase 2 checkpoint report at `docs/00-meta/implementation-reports/2026-04-19_phase-2-checkpoint-report.md` and commit it (Commit 6). Any TD-register closures (if specific evidence is in place — TD-005 already closed in Phase 1; none pending from Phase 2) go in the same commit.
4. I propose **Phase 2b — Real BTCUSDT/ETHUSDT Historical Download** as a plan-only proposal, awaiting its own Gate 1 approval. (Not Phase 3 yet — real-data ingestion is a natural separate increment before the backtester.)

Alternatively, if the operator prefers to jump directly to Phase 3 (backtesting engine) using real data, Phase 2b can be deferred and Phase 3's backtester can initially consume synthetic fixtures for development, then swap to real data once Phase 2b lands.

If redirected at Gate 2 — scope narrowing, refactoring, additional tests, or a different commit split — I apply the changes on the working tree (still pre-commit) and re-produce this review.

**Awaiting operator Gate 2 approval.**
