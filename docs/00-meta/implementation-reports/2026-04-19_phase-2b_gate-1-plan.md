# Phase 2b — Gate 1 Plan

**Date:** 2026-04-19
**Phase:** 2b — Real BTCUSDT/ETHUSDT Historical Data Download
**Current branch:** `main` (after Phase 2 merged via PR #2; commit `ddf0013`)
**Status:** PLAN ONLY. No branch created. No files edited. No dependencies installed. No network activity. Awaiting operator Gate 1 approval.

---

## 1. Executive Summary

Phase 2b closes the loop that Phase 2 deliberately left open: fetching **real** BTCUSDT and ETHUSDT historical 15m kline data and feeding it through the Phase 2 pipeline (`normalize_rows` → `write_klines` → `derive_1h_from_15m` → quality checks → `DatasetManifest`). Phase 2 proved the pipeline correct on synthetic fixtures; Phase 2b proves it correct on real data.

**Key scoping choices proposed for operator approval:**

- **Source: Binance public bulk-download ZIPs (`data.binance.vision`), with SHA256 checksum verification.** Preferred over REST klines because monthly ZIPs are (a) immutable once published, (b) ship with `.CHECKSUM` files for integrity verification, (c) have no authentication, (d) avoid the REST endpoint's 1000-bar-per-request limit and rate-limit pressure. REST is documented as a fallback for real-time tail data; not implemented in 2b.
- **Datasets in scope for Gate 2:** standard 15m klines for **BTCUSDT and ETHUSDT only**. Mark-price klines, funding-rate history, exchange-info snapshots, leverage-bracket snapshots, and commission-rate snapshots are each explicitly deferred — see §14.
- **Initial download range for Gate 2 implementation:** a single complete past month (proposal: **2026-03** for both symbols). Small enough for review/iteration, large enough to exercise all code paths including month-partition boundaries. Expanded backfill is a post-Gate-2 operator-run task.
- **Credentials:** **none used.** `data.binance.vision` is a public, unauthenticated endpoint. No API keys created, no `.env` touched.
- **TD-006 (Binance endpoint verification):** this phase owns partial resolution — only for the bulk-CSV path. REST endpoint verification remains Phase 2c / later scope.
- **One new runtime dep:** `httpx`. No other code or tooling changes beyond what Phase 2b directly needs.
- **Commits:** 5 small + checkpoint, same cadence as Phase 2.

Runtime capability at end of Phase 2b: still zero live trading. Research capability: real BTCUSDT + ETHUSDT 15m history ingested, normalized to Parquet, queryable via DuckDB, derived 1h bars generated, manifested, checksum-verified, fully reproducible.

---

## 2. Current branch/status verification commands

```bash
git -C c:/Prometheus rev-parse --abbrev-ref HEAD     # → main
git -C c:/Prometheus status --short                  # → (clean)
git -C c:/Prometheus log --oneline -8                 # → ddf0013 Merge PR #2 (phase-2), then Phase 2 commits
git -C c:/Prometheus rev-list --left-right --count HEAD...@{u}   # → 0  0
git -C c:/Prometheus branch -vv
```

Confirmed at planning time:

- branch: `main`
- working tree: clean
- sync: `0 0` (up-to-date with `origin/main`)
- last commit: `ddf0013 Merge pull request #2 from jpedrocY/phase-2/historical-data-foundation`

These are re-run at Phase 2b Step 0 pre-flight before any edit.

---

## 3. Proposed Phase 2b branch name

```
phase-2b/real-historical-download
```

Branch off the current `main` (`ddf0013`). No push during Phase 2b execution without separate approval. PR into `main` after Gate 2.

---

## 4. Exact scope

Phase 2b introduces a real-data historical fetch implementation that reuses the Phase 2 pipeline end-to-end:

1. **`src/prometheus/research/data/binance_bulk.py`** — the Binance public-bulk-download client.
   - `BulkUrlBuilder` — deterministic URL construction for monthly kline ZIPs and their `.CHECKSUM` siblings.
   - `BulkDownloader` — `httpx`-backed client with retry/backoff, streaming download to disk, SHA256 verification against the `.CHECKSUM` file before extraction, and idempotency (skip work if the artifact is already present and verified).
   - `BinanceBulkKlineSource` — a concrete `HistoricalKlineSource` (the Protocol from Phase 2 `fetch.py`) that yields raw row dicts compatible with `normalize_rows`. Uses `BulkDownloader` under the hood.
   - Per-TD-006: each public URL pattern and each expected ZIP/CSV column layout is documented inline with a citation link to the official Binance data page and the verification date.

2. **`src/prometheus/research/data/ingest.py`** — the pipeline orchestrator.
   - `ingest_monthly_range(source, symbol, interval, start_month, end_month, ...)` — for each month in the range: download → verify checksum → extract CSV → `normalize_rows` → `write_klines` → accumulate into a `DatasetManifest` (with any invalid windows surfaced by quality checks or derivation).
   - `derive_and_write_1h(root, symbol)` — after monthly 15m files land, run `derive_1h_from_15m` over the full symbol range and write to `data/derived/bars_1h/standard/...`.
   - Returns a `IngestResult` Pydantic model with counts, quality-check summaries, invalid-window list, and output paths.

3. **`src/prometheus/research/data/download_state.py`** — resumability state.
   - `DownloadState` Pydantic model persisted as JSON under `data/manifests/_downloads/<dataset_name>__state.json`.
   - Tracks per-(symbol, interval, year, month) status: `PENDING`, `DOWNLOADED`, `VERIFIED`, `EXTRACTED`, `NORMALIZED`, `FAILED_CHECKSUM`, etc.
   - Enables resume after interruption without re-downloading already-verified files.

4. **Recorded-response fixture module** under `tests/fixtures/market_data/binance_bulk/`:
   - Small pre-captured BTCUSDT-15m-2026-03 monthly ZIP (hand-made synthetic ZIP matching the Binance CSV column format).
   - A matching `BTCUSDT-15m-2026-03.zip.CHECKSUM` with the computed SHA256.
   - `respx_recordings.py` (or an in-repo alternative) mapping URL pattern → local fixture file so unit/integration tests never hit the network.

5. **Comprehensive tests** under `tests/unit/research/data/` and `tests/integration/`:
   - `test_binance_bulk.py` — URL construction, retry/backoff behavior on 429/5xx, checksum failure handling, SHA256 computation, stream-to-disk, idempotency.
   - `test_download_state.py` — state transitions, JSON round-trip, concurrent-write rejection.
   - `test_ingest.py` — unit-level orchestrator happy path + failure branches.
   - `test_ingest_end_to_end.py` (integration) — full pipeline against the recorded-fixture `respx` mock: ZIP → normalize → write → read → derive → quality → manifest.

6. **One small doc update:** a new subsection in `docs/00-meta/implementation-ambiguity-log.md` linking the Phase 2b run to TD-006's partial resolution (bulk-path verified) and TD-006's remaining surface (REST paths, user-stream — still open).

Phase 2b is **not** about downloading everything. It is about downloading a bounded real slice, proving the pipeline handles it correctly, and leaving the system in a state where a future operator-run backfill is a configuration change, not a code change.

---

## 5. Explicit non-goals

- **No REST kline endpoint calls.** `/fapi/v1/klines` is a fallback we choose not to implement in 2b. If the operator later needs tail data (post-most-recent-complete-month), that's a focused Phase 2c increment.
- **No mark-price klines, no funding rates, no exchange-info, no leverage-brackets, no commission-rates.** Each is a separate dataset with its own endpoint (and in two cases, its own authentication requirement). Each deserves a scoped proposal.
- **No account-authenticated endpoints.** `/fapi/v1/leverageBracket` and `/fapi/v2/commissionRate` require API keys; Phase 2b does not touch them.
- **No live WebSocket code.** `market_data/` runtime package remains empty.
- **No Binance testnet use.** TD-007 deferred to paper/shadow.
- **No changes to `src/prometheus/core/`** — the Phase 2 primitives remain the single source of truth for `Symbol`, `Interval`, `NormalizedKline`, time helpers.
- **No modifications to `.claude/`, `CLAUDE.md`, `docs/00-meta/current-project-state.md`, or `docs/12-roadmap/technical-debt-register.md`** in Phase 2b execution (operator may request a TD-006 status/evidence update as a post-Phase-2b follow-up).
- **No MCP activation. No `.mcp.json`. No Graphify.**
- **No CLI script under `scripts/`.** The `fetch_historical_data.py` entry point in `docs/08-architecture/codebase-structure.md` is post-2b. For now, `BinanceBulkKlineSource` and `ingest_monthly_range` are callable from a Python REPL or a test.
- **No pre-commit hooks, no CI workflow.** Still deferred.

---

## 6. Proposed files/directories to create or modify

### 6.1 New source files (under `src/prometheus/research/data/`)

```
src/prometheus/research/data/binance_bulk.py     # URL builder, BulkDownloader, BinanceBulkKlineSource
src/prometheus/research/data/download_state.py   # DownloadState Pydantic model + JSON I/O
src/prometheus/research/data/ingest.py           # ingest_monthly_range + derive_and_write_1h orchestrators
```

The existing `src/prometheus/research/data/__init__.py` will re-export the new public names.

### 6.2 New test files (under `tests/`)

```
tests/unit/research/data/test_binance_bulk.py
tests/unit/research/data/test_download_state.py
tests/unit/research/data/test_ingest.py
tests/integration/test_binance_bulk_end_to_end.py
```

### 6.3 New fixtures (under `tests/fixtures/`)

```
tests/fixtures/market_data/binance_bulk/__init__.py
tests/fixtures/market_data/binance_bulk/recordings.py          # URL -> local-file map for respx/httpx mocks
tests/fixtures/market_data/binance_bulk/BTCUSDT-15m-2026-03.zip           # tiny synthetic ZIP (a few rows of CSV)
tests/fixtures/market_data/binance_bulk/BTCUSDT-15m-2026-03.zip.CHECKSUM  # SHA256 hex of the ZIP
tests/fixtures/market_data/binance_bulk/ETHUSDT-15m-2026-03.zip
tests/fixtures/market_data/binance_bulk/ETHUSDT-15m-2026-03.zip.CHECKSUM
```

The committed ZIPs are **synthetic**, not real Binance data. They have the same structure (12-column CSV per Binance's documented format) but a handful of hand-rolled rows, so the total committed binary weight is under 2 KB per file. This keeps the repo small and avoids any question of redistributing Binance-sourced data.

### 6.4 New docs

```
docs/00-meta/implementation-reports/2026-04-19_phase-2b_gate-2-review.md
docs/00-meta/implementation-reports/2026-04-19_phase-2b-checkpoint-report.md
```

Appends to `docs/00-meta/implementation-ambiguity-log.md` (GAP-010 through approximately GAP-013).

### 6.5 Modifications to existing files

| File | Change | Justification |
| --- | --- | --- |
| `pyproject.toml` | Add `httpx>=0.27` to `[project].dependencies` | HTTP client for the bulk downloader. |
| `uv.lock` | Regenerated by `uv sync` | Deterministic dep pinning. |
| `src/prometheus/research/data/__init__.py` | Re-export new names from `binance_bulk`, `download_state`, `ingest` | Keeps public surface discoverable. |
| `configs/dev.example.yaml` | Extend `research_data:` block with `binance_bulk:` subkeys (`base_url`, `raw_root`, `state_root`, `user_agent`) | Documentation-only, matches Phase 2 convention; still no loader consuming these keys. |

No edits to `core/`, no edits to existing Phase 2 modules beyond the `__init__.py` re-exports.

---

## 7. Dependency additions and justification

One addition. No dev-group additions.

| Package | Pin | Why |
| --- | --- | --- |
| `httpx>=0.27` | min 0.27 | Modern HTTP client with streaming, timeouts, retries, and a `MockTransport` that makes offline testing trivial. Chosen over `requests` because `requests` has no first-class streaming-to-disk helper and no official mock-transport story. Chosen over `aiohttp` because Phase 2b is sync-only; async buys nothing here. |

Not adding: `respx` (which uses httpx's `MockTransport` under the hood). We'll use httpx's own `MockTransport` directly to avoid a second test-only dep.

`httpx` pulls in `httpcore`, `anyio`, `idna`, `sniffio`, `certifi` as transitive deps. All widely used.

---

## 8. Official Binance public historical-data source options to verify at implementation time

Per **TD-006** (`docs/12-roadmap/technical-debt-register.md`), Phase 2b must **verify against official Binance documentation at coding time** — endpoint paths, parameters, rate limits, response fields, error codes, and error semantics. Below are the sources the spec docs reference and the format assumptions Phase 2b currently makes:

### 8.1 Bulk public data (primary for Phase 2b)

- **Domain:** `https://data.binance.vision/`
- **Monthly kline path (assumed; must verify at coding):** `https://data.binance.vision/data/futures/um/monthly/klines/<SYMBOL>/<INTERVAL>/<SYMBOL>-<INTERVAL>-<YYYY>-<MM>.zip`
- **Checksum file path (assumed):** `<zip-url>.CHECKSUM` — a single line with `<sha256hex>  <filename>`.
- **CSV columns inside the ZIP (documented by Binance):** `open_time, open, high, low, close, volume, close_time, quote_volume, count, taker_buy_volume, taker_buy_quote_volume, ignore`.
- **Timestamp format:** historically UTC milliseconds since Unix epoch. **Verify this at coding time** — Binance has shipped data with second-precision in the past for non-futures symbols; USDⓈ-M futures is documented as ms but must be checked against the actual file.

### 8.2 Daily public data (alternative / complement)

- **Path:** `https://data.binance.vision/data/futures/um/daily/klines/<SYMBOL>/<INTERVAL>/<SYMBOL>-<INTERVAL>-<YYYY-MM-DD>.zip`
- Out of Phase 2b scope; monthly is sufficient.

### 8.3 REST klines (fallback, NOT implemented in 2b)

- **Endpoint:** `https://fapi.binance.com/fapi/v1/klines`
- **Docs URL (`historical-data-spec.md:798+`):** `https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Kline-Candlestick-Data`
- **Limits to verify:** request weight, per-IP per-minute limits, max `limit` parameter (documented as 1500).
- Deferred to Phase 2c.

### 8.4 Deferred endpoints (NOT Phase 2b scope)

| Endpoint | Purpose | Auth? |
| --- | --- | --- |
| `/fapi/v1/markPriceKlines` | Mark-price klines | Public |
| `/fapi/v1/fundingRate` | Funding rate history | Public |
| `/fapi/v1/exchangeInfo` | Exchange info snapshot | Public |
| `/fapi/v1/leverageBracket` | Notional/leverage brackets | **Account-auth required** — defer |
| `/fapi/v2/commissionRate` | Commission rate | **Account-auth required** — defer |

### 8.5 Verification deliverable in Phase 2b

Inside `binance_bulk.py`, each externally-observable assumption (URL pattern, CSV column order, CSV column types, UTC-ms timestamp format, SHA256 line format, `.CHECKSUM` naming) gets a block comment with:

1. The assumption stated precisely.
2. The official Binance documentation URL or page title that was checked.
3. The calendar date of the verification.
4. If any divergence from the repo docs is found, a GAP entry in `implementation-ambiguity-log.md` with `Risk level: HIGH` and a pause for operator review **before** any real download is run.

This resolves **the bulk-data slice** of TD-006 but not the REST slice. The TD-006 entry in `technical-debt-register.md` will not be closed by Phase 2b — only partially annotated; a separate phase must address REST/user-stream.

---

## 9. Recommendation: bulk vs REST

**Recommendation: bulk CSVs for Phase 2b; REST deferred.**

| Axis | Bulk CSVs (`data.binance.vision`) | REST `/fapi/v1/klines` |
| --- | --- | --- |
| Auth required | No | No (public) but still IP-rate-limited |
| Historical depth | Multi-year, from futures launch | Unlimited via pagination |
| Latency per full year per symbol | A few HTTP requests (~12 monthly files) | ~35 paginated requests (1500-bar limit) |
| Checksum / integrity | SHA256 per file | None |
| Immutability | Files are published once | Endpoint can change shape silently |
| Rate-limit risk | Negligible; plain static HTTP | Weight-based; easy to exceed under naive loops |
| Tail data (latest unfinished month) | Not available until after month close | Available |
| Fit for backfill | Excellent | Acceptable but slower and more fragile |

**Conclusion:** bulk is the right tool for historical backfill. REST becomes relevant only when a later phase needs "data through yesterday" for paper/shadow runs.

**Minor caveat:** `historical-data-spec.md` does not mention `data.binance.vision` explicitly (it lists REST endpoint doc URLs only). Phase 2b will log this as a **GAP** and recommend the operator consider adding a one-paragraph section on bulk data to `historical-data-spec.md` as a post-Phase-2b housekeeping item.

---

## 10. Download scope options (for Gate 1 operator choice)

Three increments are possible. Phase 2b's implementation in the branch handles all three; the only difference is the argument set passed to `ingest_monthly_range`.

| Option | Symbols | Range | Approx raw bytes | Approx normalized Parquet | Runtime | Recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| **A. Tiny smoke** | BTCUSDT only | 1 month (e.g. 2026-03) | ~400 KB | ~150 KB | Seconds | Proposed for Gate 2 demonstration. |
| **B. Bounded pilot** | BTCUSDT + ETHUSDT | 3 months (e.g. 2026-01 → 2026-03) | ~2 MB | ~1 MB | Seconds | Optional Gate 2 demonstration. |
| **C. Full backfill** | BTCUSDT + ETHUSDT | Futures launch → most recent complete month (~6+ years BTCUSDT, ~4.5 years ETHUSDT) | ~15 MB | ~25 MB | Minutes | **NOT in Phase 2b.** Operator-run task post-Gate-2 using the same code. |

The branch ships with the **code that supports all three options**, plus a committed Gate-2-artifact run of **Option A** whose outputs (manifest + invalid-windows report, no Parquet binaries) are included in the checkpoint report.

---

## 11. Proposed initial download range for Gate 2 implementation

**Proposal:** **BTCUSDT 15m, 2026-03** (single complete past month at planning time; verified complete because it ended before 2026-04-01 UTC).

Covers exactly one Hive partition (`symbol=BTCUSDT/interval=15m/year=2026/month=03`). Row count: 31 days × 96 bars/day = 2,976 bars. Small enough for review. Large enough to touch:

- month boundary in partition path (`month=03`)
- `derive_1h_from_15m` on 744 hours → 744 completed 1h bars
- `check_no_missing_bars` on an expected 2,976-row progression
- `check_timestamp_monotonic` on a non-trivial sequence
- manifest write + JSON round-trip with a realistic `sources` entry

**Optionally also:** ETHUSDT 15m, 2026-03. Same volume. The downloader and ingest code are symbol-agnostic; running on ETH costs nothing new beyond runtime. I will include ETHUSDT in the Gate 2 run unless the operator wants BTC-only.

**Not proposed for Gate 2:** any older history, any crossing of year boundary, any mark-price / funding / metadata dataset.

---

## 12. Estimated disk footprint

For the **Gate 2 run** (2026-03, both symbols, 15m standard klines only):

| Artifact | Location | Estimate |
| --- | --- | --- |
| Raw ZIPs + checksums (kept) | `data/raw/binance_usdm/klines/symbol=<SYM>/interval=15m/year=2026/month=03/` | 2 files × ~200 KB = ~400 KB |
| Normalized Parquet | `data/normalized/klines/symbol=<SYM>/interval=15m/year=2026/month=03/part-0000.parquet` | 2 partitions × ~75 KB = ~150 KB |
| Derived 1h Parquet | `data/derived/bars_1h/standard/symbol=<SYM>/year=2026/month=03/part-0000.parquet` | 2 partitions × ~10 KB = ~20 KB |
| Manifests | `data/manifests/*.manifest.json` | 4 files × ~1 KB = ~4 KB |
| Download state | `data/manifests/_downloads/*__state.json` | 2 files × ~500 B = ~1 KB |
| **Total Gate-2 footprint** | under `data/` (all git-ignored) | **~600 KB** |

Full-backfill projection (operator-run, post-Gate-2, Option C):

| Artifact | Estimate |
| --- | --- |
| Raw ZIPs (BTC + ETH, ~6 + ~4.5 years, 126 months total) | ~30 MB |
| Normalized 15m Parquet | ~25 MB |
| Derived 1h Parquet | ~4 MB |
| Manifests + state | under 100 KB |
| **Total full-backfill footprint** | **~60 MB** |

Well inside disk and bandwidth budgets on any reasonable dev machine.

---

## 13. Resumability plan

Resumability is both a correctness property (interruptions must not corrupt data) and an efficiency property (re-runs must be cheap).

**State file schema** (`data/manifests/_downloads/<dataset_name>__state.json`):

```json
{
  "dataset_name": "binance_usdm_btcusdt_15m",
  "schema_version": "download_state_v1",
  "last_updated_utc_ms": 1774300000000,
  "months": {
    "2026-03": {
      "status": "NORMALIZED",
      "zip_sha256": "<hex>",
      "downloaded_at_utc_ms": 1774290000000,
      "verified_at_utc_ms": 1774290100000,
      "normalized_at_utc_ms": 1774290200000,
      "raw_path": "data/raw/binance_usdm/klines/symbol=BTCUSDT/interval=15m/year=2026/month=03/BTCUSDT-15m-2026-03.zip",
      "normalized_path": "data/normalized/klines/symbol=BTCUSDT/interval=15m/year=2026/month=03/part-0000.parquet",
      "row_count": 2976,
      "invalid_windows": []
    }
  }
}
```

**State transitions** for each month:

```
PENDING → DOWNLOADING → DOWNLOADED → VERIFYING → VERIFIED → EXTRACTING → EXTRACTED → NORMALIZING → NORMALIZED
                                    ↘ FAILED_CHECKSUM (re-download once, then raise)
                      ↘ FAILED_DOWNLOAD (retry with backoff, then raise)
```

**Idempotency rules:**

- If a month is in `NORMALIZED` on start, skip entirely.
- If a month is in `VERIFIED`/`EXTRACTED`, resume from extraction.
- If a month is in `DOWNLOADED` but `.CHECKSUM` file is missing on disk, re-fetch the checksum only.
- If the `.CHECKSUM` changes upstream (unexpected since monthly files are immutable), treat it as a GAP-triggered hard stop — do not silently re-download.

**Atomicity:**

- ZIP writes go to a sibling `<name>.zip.partial` file and are `os.rename`-d to the final path only after the full body is received.
- State-file writes go through a `<state>.json.partial` + rename, guarded with an in-process lock to prevent concurrent runs colliding.

---

## 14. Rate-limit / retry / backoff plan

Bulk public data does not advertise a strict rate limit, but Phase 2b still implements defensive client behavior:

- **Timeouts:** connect timeout 10s, read timeout 60s, total timeout 120s per request (tunable).
- **Retry on transient failures:** automatic retry on `5xx`, `429`, `408`, and on `httpx.RequestError` (network-level).
- **Backoff:** exponential with jitter, starting at 1s, doubling up to 30s, maximum 5 attempts. After that: raise and stop.
- **Per-file pacing:** a minimum 100 ms delay between successive requests (configurable). At 12 monthly files per symbol, this adds ~1.2 seconds per year — trivially cheap.
- **No parallel downloads in Phase 2b.** One request at a time, one symbol at a time. Parallelism can come later if operators want faster backfills.
- **User-Agent header:** `Prometheus-Research/0.0.0 (+https://github.com/jpedrocY/Prometheus)` so operators can identify the traffic in any future IP investigation.

**Tests cover:** 429 retry + eventual success, 429 retry + eventual raise after max attempts, read-timeout retry, `.CHECKSUM` mismatch raise, connection-reset raise.

---

## 15. Checksum / file validation plan

- For each monthly kline ZIP, Phase 2b downloads the paired `.CHECKSUM` file first.
- Parses `<hex>  <filename>` (two-space delimiter is Binance's documented format; will be verified at coding time per TD-006).
- After the ZIP is downloaded to `<path>.partial`, computes SHA256 streaming (no full file-in-RAM).
- If checksum matches → rename `<path>.partial` → `<path>`; transition to `VERIFIED`.
- If checksum mismatches → delete the partial, transition to `FAILED_CHECKSUM`, retry once; second failure raises `DataIntegrityError` and stops the whole ingest.
- The verified SHA256 is recorded in the download-state file and in the `DatasetManifest`'s `notes` field alongside the source URL.

**ZIP extraction also performs basic structural checks:**

- Exactly one member in the archive named `<SYMBOL>-<INTERVAL>-<YYYY>-<MM>.csv`.
- CSV line count must match the expected `month_days × 96` for 15m bars (or the quality-check invalid-window path fires for partial months — not relevant for Gate 2's completed-month choice).

---

## 16. Raw data preservation plan

Raw ZIPs and their `.CHECKSUM` files are **preserved indefinitely** under `data/raw/...` (git-ignored by the existing Phase-2 `.gitignore` rule for `data/raw/**`). They are never modified, never re-extracted in-place, and never deleted by the pipeline. Downstream normalization re-opens the ZIP each run.

This means the pipeline is always reproducible from raw artifacts: if the normalized Parquet is ever corrupt, truncated, or written by a buggy version, the operator can delete `data/normalized/` and `data/derived/`, set the download-state entries back to `VERIFIED`, and re-run the `ingest` orchestrator — no re-download needed.

Raw files are not committed to git; they are operator-local artifacts.

---

## 17. Normalized Parquet output plan

Identical to Phase 2:

- `data/normalized/klines/symbol=<SYM>/interval=15m/year=<YYYY>/month=<MM>/part-0000.parquet`
- Schema: the 14-column `NormalizedKline` Phase 2 schema, exactly.
- Compression: zstd-3.
- Row group size: 65,536 rows.
- File metadata: `dataset_version`, `schema_version`, `pipeline_version`.
- Source field in each row: `binance_bulk:BTCUSDT-15m-2026-03.zip` (the actual source file name — per-row provenance, tracing each bar to the exact ZIP it came from).

Raw CSV → `NormalizedKline` mapping:

| CSV column | Target field |
| --- | --- |
| `open_time` | `open_time` (int64 UTC ms) |
| `open, high, low, close` | same (float64) |
| `volume` | `volume` |
| `close_time` | `close_time` |
| `quote_volume` | `quote_asset_volume` |
| `count` | `trade_count` |
| `taker_buy_volume` | `taker_buy_base_volume` |
| `taker_buy_quote_volume` | `taker_buy_quote_volume` |
| `ignore` | discarded |

Each row goes through `normalize_rows` with `symbol`, `interval`, `source` injected — the Phase 2 code path unchanged.

---

## 18. Derived 1h generation plan using the Phase 2 pipeline

After all monthly 15m Parquet files for a symbol land:

1. `read_klines(root, symbol=SYM, interval=I_15M)` loads the full normalized range.
2. `derive_1h_from_15m(klines)` returns `(derived, invalid_windows)` — deterministic, no I/O.
3. `write_klines(derived_root, derived, ...)` writes the 1h Parquet tree.
4. Invalid windows from the derivation are merged into the dataset manifest.

The cross-month boundary case (15m bars at the end of month N contributing to a 1h bucket that completes early in month N+1) is handled correctly by the Phase 2 `derive_1h_from_15m` because the input sequence is the **full** normalized set for the symbol, not per-month chunks. Tests for this already exist in Phase 2's `test_derive.py`.

---

## 19. Dataset manifest / versioning plan

One manifest per symbol per interval per version:

```
data/manifests/binance_usdm_btcusdt_15m__v001.manifest.json
data/manifests/binance_usdm_ethusdt_15m__v001.manifest.json
data/manifests/binance_usdm_btcusdt_1h_derived__v001.manifest.json
data/manifests/binance_usdm_ethusdt_1h_derived__v001.manifest.json
```

Fields:

- `dataset_name`: `binance_usdm_<symbol>_<interval>` (or `..._1h_derived`).
- `dataset_version`: `<dataset_name>__v001` for the Gate 2 run.
- `dataset_category`: `normalized_kline` or `derived_kline`.
- `sources`: `["https://data.binance.vision/data/futures/um/monthly/klines/<SYM>/15m/<SYM>-15m-<YYYY>-<MM>.zip"]` — one entry per month ingested.
- `invalid_windows`: aggregated from quality checks and (for derived manifests) from `derive_1h_from_15m`.
- `notes`: month range, user agent, SHA256 of each ZIP, and the TD-006 verification reference.

Manifest **immutability** enforced by the Phase 2 `write_manifest` which refuses to overwrite — if an operator runs an expanded backfill later, they must bump the version (`__v002`) and reference `__v001` as predecessor.

---

## 20. Invalid-window logging plan

Invalid windows arise from three sources, all collected into the dataset manifest's `invalid_windows`:

1. **Download-level invalidity** (future consideration; not expected in Gate 2 which uses completed months): a month that fails checksum twice, or whose CSV has the wrong row count. Recorded with `reason=checksum_mismatch` or `reason=row_count_off_by_N`.
2. **Quality-check invalidity:** `check_no_missing_bars` over the expected 15m progression within the downloaded range — any gap becomes an `InvalidWindow` in the manifest.
3. **Derivation invalidity:** `derive_1h_from_15m` already emits `InvalidWindow`s for partial 1h buckets — merged into the 1h manifest.

Phase 2b **never forward-fills** or invents bars. Invalid windows are surfaced, not hidden.

---

## 21. UTC Unix millisecond validation plan

Per `timestamp-policy.md`, enforced at three layers (same as Phase 2):

1. **Pydantic validators** in `NormalizedKline` — already in place, reject misaligned open_times and wrong close_times at construction.
2. **`check_timestamp_monotonic`** — runs over each symbol's full range after all months land.
3. **Bulk-specific check:** after ZIP extraction, confirm the first row's `open_time` is divisible by `15 * 60 * 1000` and the column is integer-typed. If Binance ever shipped seconds instead of ms, this catches it before anything else runs. Will be run as a unit test against the recorded fixtures.

---

## 22. Duplicate / missing / malformed bar detection plan

Reuses Phase 2's quality functions, extended where needed:

| Check | Phase 2 function | Phase 2b addition |
| --- | --- | --- |
| Duplicates | `check_no_duplicates` | None. |
| Missing bars | `check_no_missing_bars` | Invoked with bounds derived from `(year, month)` of each downloaded partition. |
| Non-monotonic | `check_timestamp_monotonic` | None. |
| Future bars | `check_no_future_bars` | Invoked with `now_ms = utc_now_ms()` to catch any clock-skew contamination. |
| **Malformed CSV rows** | n/a | **New in Phase 2b:** `_parse_binance_csv_row` raises `DataIntegrityError` on: column-count mismatch, non-numeric numeric fields, empty fields where values are expected. |
| **CSV row count sanity** | n/a | **New in Phase 2b:** expected `(month_days × 96)` for 15m; if off by more than 4 rows, emit a HIGH-risk GAP (Binance may have changed the format). |

All malformed-row detection happens **before** `normalize_rows` gets a chance to build `NormalizedKline` — cheaper, and the error messages cite the CSV line number for operator debugging.

---

## 23. BTCUSDT + ETHUSDT coverage plan

- **BTCUSDT**: Gate 2 downloads 2026-03 15m. Full backfill (Option C) covers 2019-09 → most recent complete month, per USDⓈ-M BTCUSDT futures launch date. Coverage gaps are expected none.
- **ETHUSDT**: Gate 2 downloads 2026-03 15m. Full backfill covers 2019-11 → most recent complete month, per ETHUSDT USDⓈ-M launch. Coverage expected none.
- **Secondary / comparison role** preserved: both symbols are treated identically by the downloader. The strategy spec still treats ETHUSDT as research/comparison only.
- **Per-symbol manifests** keep the two data streams cleanly separable.

Any month with a missing `.zip` upstream (very rare; has happened for exchange downtime days but almost never for full months) gets an `InvalidWindow` entry with the reason and a FAILED_DOWNLOAD state in the download-state file.

---

## 24. Mark-price klines / funding / exchange metadata — deferral decision

**All deferred.** Phase 2b downloads **only** standard 15m klines. Rationale:

- **Mark-price klines**: another public endpoint (`/fapi/v1/markPriceKlines` REST) or a separate bulk-download tree. Schema overlap with standard klines but not identical (no volume columns). Deserves its own small increment (call it Phase 2c-markprice) reusing the same download/verify/ingest skeleton.
- **Funding-rate history**: a different data shape (event-keyed by `funding_time`, not bar-aligned). Needs a separate model (not `NormalizedKline`). Its own Phase 2c increment.
- **Exchange-info**: a snapshot endpoint, not a range. Needs a separate `ExchangeInfo` Pydantic model and its own manifest category. Own increment.
- **Leverage-brackets**: `/fapi/v1/leverageBracket` is **account-authenticated**. Cannot be fetched without a production API key. Blocked by the current no-credentials posture. Own increment after the credential-provisioning phase gate opens.
- **Commission-rate**: similarly account-authenticated. Blocked.

Each of the five is listed as a **future Phase 2c proposal**, to be planned individually.

---

## 25. Tests / checks to run

All tests offline. No network. No credentials.

### 25.1 Quality gates (must pass before Gate 2)

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
```

Expected post-Phase-2b test count: **~110–120** (79 from Phase 2 + ~30–40 new).

### 25.2 Specific Phase 2b tests

| Module | Coverage |
| --- | --- |
| `test_binance_bulk.py` | URL builder for month ranges; BulkDownloader happy path (httpx MockTransport); 429 retry + eventual success; max retries exceeded; read timeout; write-to-disk atomicity; `.partial` → final rename; SHA256 streaming computation; checksum mismatch handling; duplicate download idempotency; User-Agent header presence. |
| `test_download_state.py` | State transitions; JSON round-trip; partial-write-then-rename atomicity; concurrent-write detection (single-process file lock). |
| `test_ingest.py` | `ingest_monthly_range` happy path (mocked source); resume from `NORMALIZED` skips work; resume from `VERIFIED` re-runs from extraction; CSV-row-count sanity; malformed CSV raises `DataIntegrityError`; quality-check integration. |
| `test_binance_bulk_end_to_end.py` (integration) | Full pipeline against committed synthetic ZIP fixtures for BTCUSDT-15m-2026-03 + ETHUSDT-15m-2026-03: download (mocked), verify, extract, normalize, write, read-back, derive 1h, quality-check, write manifest, round-trip manifest. |

Run time target: integration test under 1 second; full suite under 3 seconds.

---

## 26. Safety constraints

All Phase 1 and Phase 2 constraints preserved. Phase 2b-specific posture:

| Check | How Phase 2b preserves it |
| --- | --- |
| Production Binance keys | **Not created, not requested.** Bulk endpoint is public. |
| Real secrets / `.env` | **None touched.** `.env.example` unchanged. |
| Exchange-write capability | **None.** No `POST`, no `PUT`, no `DELETE` anywhere. Only `GET` against `data.binance.vision`. |
| `.mcp.json` | **Not created.** |
| Graphify | **Not enabled.** |
| Live trading API calls | **None.** `/fapi/*` endpoints are **not** touched in Phase 2b. |
| `.claude/*` | **Not modified.** |
| Runtime DB | **Not touched.** |
| Destructive git | **None used.** |
| `git add -f` | **Not used.** |
| Network during tests | **Zero.** httpx `MockTransport` or equivalent ensures tests are airgapped. |
| Binance user-stream / WebSocket | **Not implemented.** |
| Data redistribution | **Committed fixture ZIPs are synthetic** (hand-rolled, not Binance-sourced), so there's no redistribution concern. Real downloaded ZIPs live under git-ignored `data/raw/`. |

Operator can run the Gate 2 code with real network present, but the code will still refuse to talk to any endpoint outside the configured `base_url` and will surface its exact HTTP interactions in the manifest.

---

## 27. Ambiguity / spec-gap items to log during execution

Expected to be added to `docs/00-meta/implementation-ambiguity-log.md` during Phase 2b execution:

- **GAP-20260419-010 (expected):** `historical-data-spec.md` does not mention `data.binance.vision` bulk-download as a canonical source; Phase 2b recommends adding a one-paragraph section on it as a post-Phase-2b doc update.
- **GAP-20260419-011 (expected):** TD-006 partial resolution — bulk CSV path verified against Binance documentation; REST / user-stream paths remain OPEN and belong to later phases. Record the exact Binance doc pages and verification date.
- **GAP-20260419-012 (expected):** `httpx` pinned minor version selected by `uv sync`; ensure no yanked versions selected.
- **GAP-20260419-013 (possible):** CSV column order or timestamp format divergence from spec, if discovered during coding.
- **GAP-20260419-014 (possible):** existence and exact line format of `.CHECKSUM` files (`<hex>  <filename>` vs `<hex> <filename>` vs other variants), if discovered.
- **GAP-20260419-015 (possible):** if Binance serves a 403 or geo-restricted response from the operator's IP (unlikely but worth testing during first real-data run before Gate 2).

Each, when logged, follows the Phase 1/2 format. Safety-relevant findings pause execution and request operator review before any real network call.

---

## 28. Proposed commit structure

Five small reviewable commits on `phase-2b/real-historical-download` plus a post-Gate-2 checkpoint commit.

| # | Title | Contents |
| --- | --- | --- |
| 1 | `phase-2b: add httpx; extend dev config example` | `pyproject.toml` (httpx>=0.27), `uv.lock`, `configs/dev.example.yaml` (`binance_bulk:` subkeys under `research_data`) |
| 2 | `phase-2b: download-state tracking and bulk-download client` | `src/prometheus/research/data/download_state.py`, `src/prometheus/research/data/binance_bulk.py`, unit tests for both |
| 3 | `phase-2b: ingest orchestrator and CSV row parser` | `src/prometheus/research/data/ingest.py` + `_parse_binance_csv_row` helper, unit tests |
| 4 | `phase-2b: recorded-response fixtures, end-to-end integration` | `tests/fixtures/market_data/binance_bulk/*` (synthetic ZIPs + recordings module), integration test, `__init__.py` re-exports |
| 5 | `phase-2b: ambiguity-log entries + Gate-1/Gate-2 reports` | `docs/00-meta/implementation-ambiguity-log.md` (GAP-010..015), both Gate-1 and Gate-2 reports under `implementation-reports/` |
| 6 (post-Gate-2) | `phase-2b: checkpoint report` | Checkpoint report. Any TD-006 status annotation bundled here if operator approves. |

No push. No PR during execution. Operator decides when to push/merge.

---

## 29. Gate 2 review / checkpoint report format

Matching Phase 2 exactly:

- Gate 2 review at `docs/00-meta/implementation-reports/2026-04-19_phase-2b_gate-2-review.md` — operator decisions recap, pre-flight output, commands run, files changed, `git status`/`diff --stat`/`diff`, `uv sync` summary, quality-gate results, safety checklist, ambiguity-log entries, Phase 2b acceptance self-check, proposed commit list, items out of scope, recommended next step.
- Checkpoint at `docs/00-meta/implementation-reports/2026-04-19_phase-2b-checkpoint-report.md` — produced after Gate 2 approval and the five commits, documenting Phase 2b completion and recommending Phase 2c or Phase 3.

A **real Option-A run artifact** (manifest + invalid-window report + download state JSON, no Parquet binaries) will be included in the Gate 2 review report if the operator permits real downloads during Step 10/11. **If not, the Gate 2 review contains only mocked-test evidence** and the first real run becomes a post-merge operator task.

---

## 30. Before-implementation verification requirement (per the Phase 2b planning brief)

Before any code is written that contacts `data.binance.vision`, Phase 2b must:

1. **Open the official Binance USDⓈ-M data documentation page** (e.g., `https://github.com/binance/binance-public-data` README for bulk data; `https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Kline-Candlestick-Data` for REST kline format reference).
2. **Verify each assumption** in §8 — URL pattern, CSV column order, timestamp format, checksum file format.
3. **If any divergence is found** — stop, log a GAP entry with `Risk level: HIGH`, and request operator/ChatGPT review **before** writing `binance_bulk.py`.
4. **Record the verification** as comments in `binance_bulk.py` and as evidence in the Gate 2 review and the checkpoint report.

This satisfies the "verify current official Binance documentation/source format" requirement in the Phase 2b planning brief and the TD-006 partial-resolution deliverable.

---

## 31. Approval gates

Same cadence as Phase 1 and Phase 2:

1. **Gate 1 — plan approval (right now).** Operator approves this plan, requests narrower/broader scope, or redirects.
2. **Gate 2 — pre-commit review.** After implementation and quality gates pass, operator reviews `git diff`, test output, manifests, and approves the five commits.
3. **Optional Gate 3 — push / PR.** Operator decides whether to push the branch and open a PR into `main`.

No edits, no branch creation, no `uv sync`, no file writes until Gate 1 is approved.

**Awaiting operator Gate 1 approval.**
