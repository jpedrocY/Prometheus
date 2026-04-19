# Phase 2 — Gate 1 Plan

**Date:** 2026-04-19
**Phase:** 2 — Historical Data and Validation Foundation
**Current branch:** `main` (after Phase 1 merged via PR #1; commit `fd64041`)
**Status:** PLAN ONLY. No branch created. No files edited. No dependencies installed. Awaiting operator Gate 1 approval.

---

## 1. Executive Summary

Phase 2 builds the historical-data foundation that Phase 3's backtester and Phase 5's validation gates depend on. Its deliverable is a typed, testable, reproducible research-data pipeline that produces versioned, Parquet-backed datasets with deterministic timestamp rules, schema validation, and quality checks — all without touching the network, without Binance credentials, without runtime persistence, and without exchange-write capability.

**Key scoping choices proposed for operator approval:**

- **Synthetic fixtures first, real data later.** Phase 2 uses small synthetic BTCUSDT and ETHUSDT 15m/1h fixtures generated deterministically in Python. The `fetch.py` interface will be **designed but left unimplemented** — actual public Binance historical downloads will be proposed as a separate approval (Phase 2b) because they involve network calls and larger-volume downloads that warrant their own scoping.
- **Place the data layer under `src/prometheus/research/data/`** per `docs/08-architecture/codebase-structure.md`. Shared domain types (`NormalizedKline`, symbol/interval primitives, UTC-ms helpers) go under `src/prometheus/core/`.
- **Three new runtime deps:** `pyarrow`, `duckdb`, `pydantic` (all mainstream, all minimal-transitive). No `pandas`, no `polars`, no networking libs, no Binance client.
- **Commit structure:** 5 small commits + checkpoint, mirroring Phase 1's review cadence.

Runtime capability at end of Phase 2: still zero live behavior. Research capability: small, end-to-end, with passing data-integrity tests.

---

## 2. Current branch/status verification commands

```bash
git -C c:/Prometheus rev-parse --abbrev-ref HEAD     # → main
git -C c:/Prometheus status --short                  # → (clean)
git -C c:/Prometheus log --oneline -6                 # → fd64041 Merge PR #1, then Phase 1 commits
git -C c:/Prometheus rev-list --left-right --count HEAD...@{u}   # → 0  0
git -C c:/Prometheus branch -vv
```

Confirmed at planning time:
- branch: `main`
- working tree: clean
- sync: `0 0` (up-to-date with `origin/main`)
- last commit: `fd64041 Merge pull request #1 from jpedrocY/phase-1/local-dev-foundation`
- `phase-1/local-dev-foundation` still exists locally at `7b9769e` and tracks `origin/phase-1/local-dev-foundation` (can be pruned later — not a Phase 2 concern).

These same commands will be re-run as Phase 2 Step 0 pre-flight before any edit.

---

## 3. Proposed Phase 2 branch name

```
phase-2/historical-data-foundation
```

Branch off the current `main` (`fd64041`). No push during Phase 2 without separate operator approval, per the Phase 1 precedent. PR into `main` after Gate 2.

---

## 4. Exact scope

Phase 2 builds a reproducible research-data layer covering:

1. **Shared domain primitives** in `src/prometheus/core/`:
   - UTC Unix millisecond time helpers.
   - Symbol and interval primitives (`Symbol`, `Interval` types with `BTCUSDT`, `ETHUSDT`, `I_15M`, `I_1H` constants).
   - `NormalizedKline` Pydantic model with the exact schema from `docs/04-data/historical-data-spec.md`.
   - Bar-identity helpers `(symbol, interval, open_time)`.
   - Interval alignment helpers (`is_aligned_open_time`, `bucket_to_1h`).
2. **Research data layer** under `src/prometheus/research/data/`:
   - `manifests.py` — `DatasetManifest` Pydantic model matching `docs/04-data/dataset-versioning.md`, plus read/write helpers (JSON).
   - `storage.py` — Parquet read/write with Hive partitioning `symbol=/interval=/year=/month=/`, PyArrow backend; DuckDB query helpers over the Parquet lake.
   - `normalize.py` — functions that take an in-memory iterable of raw kline rows and produce validated `NormalizedKline` records.
   - `derive.py` — deterministic 15m → 1h standard-bar aggregation (no forward-fill, emits only fully completed 1h buckets).
   - `quality.py` — data-integrity checks (duplicate detection, missing-bar detection, timestamp monotonicity, OHLC sanity, volume sanity, interval alignment, no-forward-fill proof, no-future-leakage proof).
   - `fetch.py` — **interface-only scaffold**. Abstract `HistoricalKlineSource` protocol plus a `FixtureKlineSource` concrete class that reads from `tests/fixtures/market_data/`. No HTTP, no Binance.
3. **Synthetic fixture data** under `tests/fixtures/market_data/`:
   - Two small sample datasets (~100 completed 15m bars each for BTCUSDT and ETHUSDT) generated deterministically by a pytest fixture (seeded RNG walk). Saved as Parquet with the full Hive partition structure. Accompanied by a hand-written sample `manifest.json` per dataset.
4. **Comprehensive tests** under `tests/unit/`, `tests/integration/`, and `tests/fixtures/market_data/`:
   - Unit tests for each `core/` and `research/data/` function.
   - Integration test: fixture-source → normalize → write Parquet → read via DuckDB → derive 1h → quality-check-pass.
   - Negative tests for each failure class (duplicate bars, missing bars, non-monotonic timestamps, partial final bar, local-timezone input, invalid OHLC, partial 1h bucket).
5. **Directory skeletons** (required by `docs/08-architecture/codebase-structure.md` but absent today):
   - `data/raw/`, `data/normalized/`, `data/derived/`, `data/manifests/` — each with `.gitkeep`. Pattern is the "local/generated" layout at repo root, distinct from the versioned fixture copy under `tests/fixtures/`.
   - `var/runtime/`, `var/logs/`, `var/reports/`, `var/tmp/` — each with `.gitkeep`. Required by codebase-structure §6 for runtime artifact placement.
   - These directories will be git-ignored for contents per existing `.gitignore` rules (`runtime/`, `logs/`, `data/runtime/`, `data/secrets/`) — except `.gitkeep`. We may extend `.gitignore` narrowly to cover `data/raw/**`, `data/normalized/**`, `data/derived/**`, `var/runtime/**`, `var/logs/**`, `var/reports/**`, `var/tmp/**`, mirroring the existing `research/data/**` skeleton rule. Each such edit is itemized below and flagged as a separate approval.

Phase 2 is **not** about collecting real market data. It is about proving the research pipeline is correct on known-good fixtures, so that later downloading real BTCUSDT/ETHUSDT 15m history (a bounded, network-dependent task) fits into a trustworthy pipeline.

---

## 5. Explicit non-goals

- No real Binance downloads (historical or live). `fetch.py` will not implement HTTP.
- No live WebSocket code. `market_data/` runtime package remains empty.
- No backtesting engine (that is Phase 3, `src/prometheus/research/backtesting/`).
- No strategy code (`src/prometheus/strategy/` remains absent).
- No risk engine, no runtime DB, no state machine.
- No dashboard, no alerts, no CLI entrypoint.
- No secrets handling, no `.env` usage at runtime, no production credentials.
- No new MCP servers, no `.mcp.json`, no Graphify.
- No modifications to `CLAUDE.md`, `.claude/rules/*`, `.claude/agents/*`, `.claude/settings.json`, or `docs/00-meta/current-project-state.md` (unless a targeted edit is proposed and separately approved, e.g., for stale references surfaced by Phase 2 work).
- No broad rewrite of the technical-debt register. At most: add TD-006-adjacent items as ambiguity-log entries; TD register gets TD-005-style targeted status flips only after their specific evidence exists.
- No tooling changes to ruff/mypy/pytest/uv beyond adding the three dependencies.
- No pre-commit hooks. No CI workflow. Both still deferred per Phase 1 decisions.

---

## 6. Proposed files/directories to create or modify

### 6.1 New source files (under `src/prometheus/`)

```
src/prometheus/core/__init__.py                     # re-exports from time/ids/symbols/intervals/klines
src/prometheus/core/__about__.py                    # (optional) package version constant, avoids circular imports
src/prometheus/core/time.py                         # utc_now_ms(), is_aligned_open_time(ms, interval), floor_to_interval(ms, interval)
src/prometheus/core/symbols.py                     # Symbol enum/Literal + BTCUSDT, ETHUSDT constants, normalization
src/prometheus/core/intervals.py                   # Interval enum + I_15M, I_1H + duration_ms()
src/prometheus/core/klines.py                       # NormalizedKline pydantic model (exact schema from historical-data-spec)
src/prometheus/core/errors.py                       # DataIntegrityError, ManifestError (used by research/data)

src/prometheus/research/__init__.py                 # empty; package marker
src/prometheus/research/data/__init__.py            # empty
src/prometheus/research/data/manifests.py           # DatasetManifest model + read/write JSON helpers
src/prometheus/research/data/storage.py             # Parquet Hive I/O via pyarrow; DuckDB view builder
src/prometheus/research/data/normalize.py           # normalize_rows(raw_iter) -> list[NormalizedKline]
src/prometheus/research/data/derive.py              # derive_1h_from_15m(klines_15m) -> list[NormalizedKline_1h]
src/prometheus/research/data/quality.py             # check_duplicates, check_monotonic, check_no_missing, check_ohlc_sanity, etc.
src/prometheus/research/data/fetch.py               # HistoricalKlineSource protocol + FixtureKlineSource only
```

### 6.2 New test files (under `tests/`)

```
tests/unit/core/__init__.py
tests/unit/core/test_time.py
tests/unit/core/test_symbols.py
tests/unit/core/test_intervals.py
tests/unit/core/test_klines.py

tests/unit/research/__init__.py
tests/unit/research/data/__init__.py
tests/unit/research/data/test_manifests.py
tests/unit/research/data/test_normalize.py
tests/unit/research/data/test_derive.py
tests/unit/research/data/test_quality.py
tests/unit/research/data/test_storage.py

tests/integration/__init__.py
tests/integration/test_fixture_pipeline_end_to_end.py
```

### 6.3 New fixtures (under `tests/fixtures/`)

```
tests/fixtures/__init__.py
tests/fixtures/market_data/__init__.py
tests/fixtures/market_data/conftest.py                      # pytest fixtures that materialize the sample Parquet tree into a temp dir
tests/fixtures/market_data/specs/synthetic_btcusdt_15m.py   # deterministic generator spec (seed, price path, volumes)
tests/fixtures/market_data/specs/synthetic_ethusdt_15m.py   # similar
tests/fixtures/market_data/manifests/
  synthetic_btcusdt_15m__v001.manifest.json
  synthetic_ethusdt_15m__v001.manifest.json
```

No committed Parquet files: the Parquet files get materialized at test time into a `tmp_path`. This avoids committing binary data and keeps the repo small. The manifest JSONs are committed as documentation of what the synthetic datasets promise.

### 6.4 New top-level skeletons

```
data/.gitkeep
data/raw/.gitkeep
data/normalized/.gitkeep
data/derived/.gitkeep
data/manifests/.gitkeep
var/.gitkeep
var/runtime/.gitkeep
var/logs/.gitkeep
var/reports/.gitkeep
var/tmp/.gitkeep
```

These match `docs/08-architecture/codebase-structure.md` §"Target Repository Layout" and §"Root-level policy".

### 6.5 New docs

```
docs/00-meta/implementation-reports/2026-04-19_phase-2_gate-2-review.md     # created at end of Step 12
docs/00-meta/implementation-reports/2026-04-19_phase-2-checkpoint-report.md # created after Gate 2 approval + commits
```

Ambiguity log (`docs/00-meta/implementation-ambiguity-log.md`) gets appended with any new GAP entries discovered; no rewrite of existing entries.

### 6.6 Modifications to existing files

| File | Change | Justification |
| --- | --- | --- |
| `pyproject.toml` | Add `pyarrow>=17`, `duckdb>=1.1`, `pydantic>=2.8` to `[project].dependencies` | Needed for Parquet I/O, DuckDB queries, typed models. |
| `uv.lock` | Regenerated by `uv sync` | Deterministic dep pinning. |
| `configs/dev.example.yaml` | Add (small) `research_data` block with the default local paths (`data_root: data/`, `manifests_root: data/manifests/`) | Documents where Phase 2 writes outputs. Kept safe: no secrets. |
| `.gitignore` | Add `data/raw/**`, `data/normalized/**`, `data/derived/**`, `var/runtime/**`, `var/logs/**`, `var/reports/**`, `var/tmp/**`, plus `!**/.gitkeep` negations | Mirrors existing `research/data/**` rule; prevents accidental commits of large generated datasets or runtime artifacts. **Listed as a separate proposal** — operator can request Option B (narrower) if preferred. |
| `docs/00-meta/implementation-ambiguity-log.md` | Append GAP entries as discovered | Normal ambiguity-log discipline. |

No other existing docs or configs are touched by this plan.

---

## 7. Dependency additions and justification

Three additions to `[project].dependencies` in `pyproject.toml`. All three are mature, well-maintained, and widely used in scientific-Python / data-engineering workflows. None introduce exchange-adjacent or networking behavior.

| Package | Pin | Why |
| --- | --- | --- |
| `pyarrow>=17` | minimum 17 | Canonical Parquet I/O engine. Required by `docs/04-data/historical-data-spec.md` (Parquet storage). Supports Hive partitioning, column pruning, and typed schemas. Already the backend behind DuckDB's Parquet reader. |
| `duckdb>=1.1` | minimum 1.1 | Named explicitly in `docs/04-data/historical-data-spec.md` and `docs/04-data/data-requirements.md` as the local analytical query layer. Provides SQL queries over Parquet without a server. |
| `pydantic>=2.8` | minimum 2.8 | Typed data models for `NormalizedKline`, `DatasetManifest`. Pydantic v2 has strict-mode validation suitable for boundary checks (rejecting malformed rows at ingestion). No networking or exchange exposure. |

Dev-group additions: **none**. `ruff`, `mypy`, `pytest`, `pytest-cov` already cover everything Phase 2 needs.

`uv sync` with these additions is expected to complete offline from the local PyPI cache — if it fails, it falls back to PyPI. No private indices are used.

---

## 8. Data source policy for Phase 2

**Sources Phase 2 is authorized to use:**

- In-repo synthetic fixtures generated deterministically from seeded RNGs in test code. No network.
- Future-proof interface (`HistoricalKlineSource` protocol) that later phases can implement against real data sources.

**Sources Phase 2 is NOT authorized to use:**

- Public Binance REST historical kline endpoints (`/fapi/v1/klines`, `/fapi/v1/markPriceKlines`, etc.).
- Binance public bulk-download CSVs.
- Any live-stream WebSocket feed.
- Any third-party market-data vendor.
- Any endpoint requiring an API key, including testnet.

The decision: **synthetic fixtures first, real data later.** Real-data downloads deserve their own scoped approval (Phase 2b) covering: disk-footprint sizing, bandwidth/rate-limit behavior, resumability after interruptions, invalid-window logging, and host-level DNS/TLS posture. Including that work here would expand Phase 2 beyond what's cleanly reviewable.

---

## 9. Fixture-first vs public-files vs live-download decision

Explicit recommendation: **Fixture-first (this phase). Real public files later (Phase 2b). Live download never (it belongs in Phase 6's runtime scope, not research).**

| Option | Phase 2 | Later phase |
| --- | --- | --- |
| Synthetic fixtures | **YES — proposed here** | Retained as unit-test bedrock |
| Binance public bulk-download ZIPs (monthly CSVs) | no | Phase 2b proposal |
| Binance REST historical klines | no | Phase 2b proposal (alternative to bulk CSVs) |
| Binance user-stream live | no | Phase 6 (dry-run exchange simulation) |

Rationale: fixtures prove the pipeline's correctness *independent* of network availability and *independent* of Binance API stability. Every quality check, every test case, and every derived-bar calculation can be expressed against fixtures with known-good expected outputs. When Phase 2b pulls real history, the same pipeline and the same tests apply — the only new surface is the network-facing `fetch.py` implementation.

---

## 10. Proposed research-data directory conventions

Committed (under `tests/fixtures/market_data/`):
- Spec files (Python) and manifest JSONs only. No Parquet binaries.

Local/generated (under repo-root `data/`, git-ignored):
- `data/raw/binance_usdm/<symbol>/<interval>/year=YYYY/month=MM/*.parquet`
- `data/normalized/klines/symbol=<SYM>/interval=<INTV>/year=YYYY/month=MM/*.parquet`
- `data/derived/bars_1h/standard/symbol=<SYM>/year=YYYY/month=MM/*.parquet`
- `data/manifests/<dataset_name>__v<NNN>.manifest.json`

Path construction is deterministic: `storage.partition_path(root, symbol, interval, year, month)` returns the exact Hive-partitioned subpath. Writers always compute the path; readers never guess.

File naming within a partition directory: `part-0000.parquet` for single-file partitions; multi-file partitions use `part-NNNN.parquet` with monotonic increment. This mirrors PyArrow's default `write_dataset()` behavior.

---

## 11. Parquet storage conventions

- **Compression:** `zstd` at level 3 (good ratio, fast decompress). Passed explicitly via `pyarrow.parquet.write_table(compression="zstd", compression_level=3, ...)`.
- **Row group size:** 64k rows per row group. Tuned for 15m klines (~96 bars/day * 365 days ≈ 35k rows/year/symbol) so a full year fits in a single row group per partition file.
- **Column order:** exactly the order defined in `docs/04-data/historical-data-spec.md`:
  `symbol, interval, open_time, close_time, open, high, low, close, volume, quote_asset_volume, trade_count, taker_buy_base_volume, taker_buy_quote_volume, source`.
- **Column types:**
  - `symbol`, `interval`, `source` → `string`
  - `open_time`, `close_time` → `int64` (UTC Unix ms)
  - `trade_count` → `int64`
  - `open`, `high`, `low`, `close`, `volume`, `quote_asset_volume`, `taker_buy_base_volume`, `taker_buy_quote_volume` → `float64` (decimal semantics are for strategy/runtime, not research storage)
- **File-level metadata:** every Parquet file carries custom key-value metadata with `dataset_version`, `schema_version`, `pipeline_version`, `created_at_utc_ms`. Used by the quality checks to fail loudly if a partition drifts from the manifest.
- **Schema validation:** `storage.write_klines()` rejects any row whose fields don't match the strict schema (via Pydantic `NormalizedKline.model_validate()` per row before batching).

---

## 12. DuckDB query setup

- No persistent DuckDB database file in Phase 2. DuckDB is used in-memory (`duckdb.connect()` with no path).
- A helper `storage.attach_dataset(con, dataset_name, root_path)` registers a `VIEW` over the Parquet tree using DuckDB's `read_parquet(..., hive_partitioning=1)` so queries can filter by `symbol`/`interval`/`year`/`month` via predicate pushdown.
- Common queries exposed as Python helpers (no freeform SQL in business code): `query_completed_bars(con, symbol, interval, start_ms, end_ms)`, `query_count(con, symbol, interval)`.
- Tests verify the DuckDB view returns the same data the Pydantic model validated on write (round-trip integrity).

No DuckDB CLI, no `.duckdb` files, no extensions loaded, no HTTP/S3 extensions.

---

## 13. Dataset manifest format

Pydantic v2 model `DatasetManifest` serialized as JSON. Minimum fields from `docs/04-data/dataset-versioning.md`:

```json
{
  "dataset_name": "synthetic_btcusdt_15m",
  "dataset_version": "synthetic_btcusdt_15m__v001",
  "dataset_category": "normalized_kline",
  "created_at_utc_ms": 1745020800000,
  "canonical_timezone": "UTC",
  "canonical_timestamp_format": "unix_milliseconds",
  "symbols": ["BTCUSDT"],
  "intervals": ["15m"],
  "sources": ["synthetic:spec/synthetic_btcusdt_15m.py"],
  "schema_version": "kline_v1",
  "pipeline_version": "prometheus@0.0.0",
  "partitioning": ["symbol", "interval", "year", "month"],
  "primary_key": ["symbol", "interval", "open_time"],
  "generator": "prometheus.research.data.fetch.FixtureKlineSource",
  "predecessor_version": null,
  "invalid_windows": [],
  "notes": "Deterministic synthetic fixture for Phase 2 pipeline tests. No real market data."
}
```

The `dataset_version` pattern `<dataset_name>__v<NNN>` is enforced by a model validator. Predecessor linkage is enforced (cannot reuse a published version; new corrections must reference their predecessor). The manifest write path refuses to overwrite a file if one already exists at that path, surfacing `ManifestError` instead of silently clobbering — mirroring the "immutability" rule.

---

## 14. Normalized kline schema (Pydantic model)

```python
class NormalizedKline(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    symbol: Symbol
    interval: Interval
    open_time: int      # UTC Unix ms; must be aligned to interval
    close_time: int     # = open_time + interval.duration_ms - 1
    open: float
    high: float
    low: float
    close: float
    volume: float
    quote_asset_volume: float
    trade_count: int
    taker_buy_base_volume: float
    taker_buy_quote_volume: float
    source: str

    @model_validator(mode="after")
    def _validate_ohlc(self):
        # OHLC sanity: high >= max(open, close), low <= min(open, close)
        # volumes non-negative
        # close_time == open_time + interval.duration_ms - 1
        # open_time aligned to interval
```

All constraints enforced at construction time. `normalize.py` refuses to emit a row that fails validation; `quality.py` runs the same checks over the stored Parquet after write, to catch pipeline mistakes.

---

## 15. Derived 1h bar generation plan

`derive.py::derive_1h_from_15m(klines_15m)`:
- Groups 15m bars by their 1h bucket (`bucket_open_time = open_time - (open_time % 3_600_000)`).
- Emits a 1h bar **only when all four expected 15m bars are present for that bucket.** Partial buckets are skipped and returned as an "invalid windows" list.
- The emitted 1h bar has:
  - `open` = first 15m bar's `open`
  - `high` = max of the four highs
  - `low` = min of the four lows
  - `close` = last 15m bar's `close`
  - `volume`, `quote_asset_volume`, `trade_count`, `taker_buy_base_volume`, `taker_buy_quote_volume` = sums of the four
  - `close_time` = bucket_open_time + 3,599,999
  - `source` = `"derived:15m->1h"`
- Pure function; no I/O; deterministic.

A companion helper `derive_1h_from_15m_partition(...)` wraps this with partition-aware writes via `storage.write_klines()` and records the invalid-window list into the dataset manifest.

---

## 16. Timestamp and UTC Unix millisecond validation plan

Enforced at three layers:

1. **Pydantic validators** in `core/klines.py`:
   - `open_time % interval.duration_ms == 0` (bar aligned).
   - `close_time == open_time + interval.duration_ms - 1`.
   - `open_time > 0`.
2. **`quality.check_timestamp_monotonic(klines)`** — asserts strictly increasing `open_time` per `(symbol, interval)` partition.
3. **`quality.check_no_local_timezone_strings(raw_rows)`** — when ingesting from any future CSV-style source, rejects rows whose timestamp fields parse as local-tz-naïve strings. (In Phase 2 with synthetic fixtures, the validator is exercised via a negative unit test that feeds local-timezone strings.)

`core/time.py` provides:
- `utc_now_ms()` — `int(time.time() * 1000)` with a deterministic clock injectable for tests.
- `floor_to_interval(ms, interval)` — `ms - (ms % interval.duration_ms)`.
- `is_aligned_open_time(ms, interval)` — `ms % interval.duration_ms == 0`.
- `interval_duration_ms(interval)` — returns `900_000` for 15m, `3_600_000` for 1h.

Zero use of `datetime.now()` without an explicit UTC tzinfo; `datetime` is used only for formatting diagnostics, never as canonical storage.

---

## 17. Duplicate/missing bar detection plan

`quality.py`:
- `check_no_duplicates(klines)` → returns `list[DuplicateReport]` grouping bars by `(symbol, interval, open_time)`. Empty list is pass.
- `check_no_missing_bars(klines, expected_start_ms, expected_end_ms, interval)` → computes the expected arithmetic progression of `open_time` values between bounds and reports any gaps. Returns `list[MissingWindow]`.
- `check_no_future_bars(klines, now_ms)` → asserts no `open_time > now_ms` (prevents accidental clock-skew contamination in tests and fixtures).
- `check_no_forward_fill(klines)` → detects runs of identical OHLC values with zero volume spanning >N consecutive bars (configurable; default N=3). Not proof but a strong smell test.

Each check returns a structured result; the integration test asserts the synthetic fixtures pass all four checks, and the negative unit tests inject specific failure rows and assert the correct check fires.

---

## 18. 15m/1h alignment test plan

Dedicated test module `tests/unit/research/data/test_derive.py`:

1. **Happy path**: 8 consecutive aligned 15m bars → 2 completed 1h bars, correct OHLC aggregation, correct volume sums. Expected outputs are hand-computed and asserted exactly.
2. **Partial bucket**: 3 of 4 15m bars present in a bucket → that 1h bar is NOT emitted; it appears in the invalid-windows list.
3. **Unaligned 15m input**: a 15m bar with `open_time` not divisible by 900_000 → raises `DataIntegrityError` before aggregation starts.
4. **Strategy-time bias check**: at decision time `t` (the close of a 15m bar), the 1h bias bar selected for `t` has `open_time ≤ t` AND `close_time < t` (i.e., it is fully completed before `t`). Encodes the "completed-bar-only" rule from `timestamp-policy.md`.
5. **No forward leakage**: given 15m bars covering `[t0, t0+2h)`, at any decision time `t` the set of 1h bars visible has `close_time < t`. Encoded as a property-based style test with parameterized `t` values.

Failure class #4 is the single most important Phase 2 correctness test — it is the direct guard against the look-ahead bug described in `docs/04-data/timestamp-policy.md`.

---

## 19. BTCUSDT and ETHUSDT sample-data strategy

Each synthetic dataset:
- **Span:** 24 hours of 15m bars = 96 completed bars. Small enough for fast tests (<50ms fixture build), large enough to exercise month partition boundaries and 1h derivation.
- **Starts at:** `2026-04-01T00:00:00Z` (arbitrary aligned choice; all tests parameterize on this so changing it is a one-line edit).
- **Generator:** deterministic seeded geometric Brownian walk starting at `symbol_start_price` (`BTCUSDT=65000`, `ETHUSDT=3500`) with per-bar volatility `sigma`. Seeds: `hash("btcusdt-synthetic-v001") & 0xFFFFFFFF` and similar for ETH. Each run reproduces bit-identical output.
- **Intervals:** 15m only in the raw spec; 1h derivation is computed at test time via `derive_1h_from_15m()`.
- **Volumes, trade counts, taker volumes:** derived from a second seeded RNG with plausible but arbitrary magnitudes.
- **Manifest:** committed at `tests/fixtures/market_data/manifests/synthetic_btcusdt_15m__v001.manifest.json` (and `_ethusdt_`).

There is no implication about real-market realism. These fixtures exist to verify *pipeline correctness*, not *strategy profitability*.

Real-history datasets (BTCUSDT 15m going back multiple years) are deferred to Phase 2b. Storage sizing estimate for that phase is ~15MB/year per symbol at zstd-level-3, which is well inside home-internet and disk budgets — but the download/resumability story is its own design.

---

## 20. Tests / checks to run

Every test runs via `uv run pytest` with no network. CI is still deferred.

### Quality gates (must pass before Gate 2)

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
```

Expected post-Phase-2 test count: 40–60 tests across unit + integration. Target wall time: under 10 seconds.

### Specific data-layer tests introduced

| Test module | Coverage |
| --- | --- |
| `test_time.py` | `utc_now_ms` injection, `floor_to_interval`, `is_aligned_open_time`, `interval_duration_ms` |
| `test_symbols.py` | parsing, normalization, rejection of unknown strings |
| `test_intervals.py` | enum membership, duration values, serialization |
| `test_klines.py` | Pydantic construction, strict-mode rejections, OHLC/close_time validators |
| `test_manifests.py` | JSON round-trip, version-pattern validation, immutability-check (refuses overwrite), predecessor-linkage rule |
| `test_normalize.py` | raw → validated; malformed row rejection; per-row error reporting |
| `test_derive.py` | happy path, partial bucket, unaligned input, no-forward-leakage, completed-bar-at-decision-time |
| `test_quality.py` | each of the 4 checks: positive and negative cases |
| `test_storage.py` | Parquet write+read round-trip, Hive partitioning, DuckDB view query count, metadata presence |
| `test_fixture_pipeline_end_to_end.py` | fixture → normalize → write → DuckDB read → derive 1h → quality-check all pass |

No test depends on network, no test depends on clock wall time, no test requires real data on disk outside `tmp_path`.

---

## 21. Safety constraints (carried into Phase 2)

All constraints preserved from Phase 1. Explicit Phase 2 posture:

| Check | How Phase 2 preserves it |
| --- | --- |
| Production Binance keys | None — `fetch.py` is scaffold-only; no `requests`/`httpx` added. |
| Real secrets | None — `.env.example` unchanged except possibly a commented `PROMETHEUS_RESEARCH_DATA_ROOT=data/` placeholder. |
| Exchange-write | None — no exchange client anywhere in the tree. |
| `.mcp.json` | Not created. |
| Graphify | Not enabled. |
| Live API calls | None — all tests offline. |
| `.claude/*` | Not modified. |
| Runtime DB | Not touched. Research storage and runtime persistence remain strictly separate (`src/prometheus/research/data/` vs the not-yet-existing `src/prometheus/persistence/`). |
| Destructive git | None — feature branch + `git mv` only. |
| `git add -f` | Not used. |

Boundary enforcement is also mechanical: `mypy` is scoped to `src/prometheus` and `research/data/*.py` will import ONLY from `core/` and the three new deps. Any accidental import of runtime/exchange modules would surface as a type-check failure.

---

## 22. Ambiguity / spec-gap items to log during execution

Seeded GAPs I expect Phase 2 will add to `docs/00-meta/implementation-ambiguity-log.md` (to be recorded as they are actually encountered, not preemptively):

- **GAP-20260419-004** (expected): exact pin choices for `pyarrow`, `duckdb`, `pydantic` once `uv sync` resolves; record whether any yanked/recent version needed to be down-pinned.
- **GAP-20260419-005** (expected): `.gitignore` additions for `data/` and `var/` subdirectories — scoped list presented to operator for approval before edit (mirroring the GAP-003 pattern from Phase 1 for `.python-version`).
- **GAP-20260419-006** (expected): `configs/dev.example.yaml` gained a `research_data:` block — confirm the chosen keys (`data_root`, `manifests_root`) match future-phase expectations, or defer the config block entirely to Phase 4 if safer.
- **GAP-20260419-007** (possible): the empty `py.typed` and `__init__.py` files cause new spurious rename detections under `git log --follow`; not a real problem, but documented so the Phase 2 checkpoint report doesn't rediscover it.
- **GAP-20260419-008** (possible): anything surfaced by `docs/04-data/*` that is internally inconsistent or under-specified when we try to implement it. Route to `prometheus-spec-architect` if it affects safety or data-integrity semantics.

Each GAP, when logged, follows the format established in Phase 1 (Status / Phase / Area / Blocking / Risk / Description / Why / Options / Recommendation / Operator decision / Resolution evidence).

---

## 23. Proposed commit structure

Five commits on `phase-2/historical-data-foundation` plus the Phase 2 checkpoint commit post-Gate-2. Each small, each independently reviewable.

| # | Title | Contents |
| --- | --- | --- |
| 1 | `phase-2: add pyarrow + duckdb + pydantic; top-level data/ var/ skeletons` | `pyproject.toml` dep additions, `uv.lock`, `.gitignore` additions (listed for operator approval), `data/` and `var/` `.gitkeep` trees |
| 2 | `phase-2: core/ primitives — time, symbols, intervals, NormalizedKline` | `src/prometheus/core/*.py` + `tests/unit/core/*` |
| 3 | `phase-2: research/data — manifests and Parquet storage + DuckDB` | `manifests.py`, `storage.py`, matching tests |
| 4 | `phase-2: research/data — normalize, derive, quality` | `normalize.py`, `derive.py`, `quality.py`, matching tests |
| 5 | `phase-2: fixtures, end-to-end integration test, gate-2 review` | `tests/fixtures/market_data/*`, committed manifests, `test_fixture_pipeline_end_to_end.py`, `fetch.py` scaffold (FixtureKlineSource only), Gate 2 review report under `implementation-reports/` |
| 6 (post-Gate-2) | `phase-2: checkpoint report + TD touches` | Checkpoint report; any TD-register flips if their specific evidence is in place |

All commit messages use the Phase 1 convention (no `Co-Authored-By`).

No push, no PR during Phase 2 execution. After Phase 2 checkpoint commit, operator may request a PR into `main` as in Phase 1.

---

## 24. Gate 2 review / checkpoint report format

Gate 2 review: `docs/00-meta/implementation-reports/2026-04-19_phase-2_gate-2-review.md` — same template as the Phase 1 Gate 2 review, with sections for:

1. Purpose
2. Operator decisions recorded at Gate 1 (this file's §'s copied forward)
3. Pre-flight output
4. Commands run
5. Files changed (by commit)
6. `git status`, `git diff --stat`, `git diff` (tracked)
7. `uv sync` output summary
8. Quality gate results (ruff / format / mypy / pytest)
9. Safety checklist verification
10. Ambiguity-log entries created
11. Phase 2 acceptance-criteria self-check (mapped to the handoff's §"Phase 2")
12. Proposed Phase 2 commit list (Commits 1–5)
13. Items explicitly out of scope (confirmed untouched)
14. Recommended next step

Checkpoint report: `docs/00-meta/implementation-reports/2026-04-19_phase-2-checkpoint-report.md` — same template as Phase 1 checkpoint, with Phase 2-specific sections added for "Dataset manifests produced", "Invalid-window log summary", and "DuckDB query smoke-test outputs".

Both reports are commit-ready and must not contain secrets or host-specific paths beyond `c:/Prometheus`.

---

## 25. Approval gates (identical cadence to Phase 1)

1. **Gate 1 — plan approval (right now).** Operator approves this plan as written, or requests revisions / narrower scope.
2. **Gate 2 — pre-commit review.** After Step 12, operator reviews `git diff`, test output, fixture manifests, and approves Commits 1–5.
3. **Optional Gate 3 — push / PR.** Operator decides whether to push the branch and open a PR, or keep local-only.

No edits, no branch creation, no `uv sync`, no file writes until Gate 1 is approved.

**Awaiting operator Gate 1 approval.**
