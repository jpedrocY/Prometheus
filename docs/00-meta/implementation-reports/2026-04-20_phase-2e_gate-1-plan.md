# Phase 2e — Gate 1 Plan: Wider Historical Backfill and Baseline Backtest Dataset

**Date:** 2026-04-20
**Phase:** 2e — Wider Historical Backfill and Baseline Backtest Dataset
**Current branch:** `main` at `07be435` (Merge PR #5, Phase 3 landed)
**Proposed branch:** `phase-2e/wider-historical-backfill` (off `main`, **not created yet — awaiting Gate 1 approval**)
**Author:** Claude Code, on behalf of operator
**Status:** GATE 1 PLAN — data-preparation + baseline-statistics only. No code written. No branch created. No downloads triggered. No Binance calls.

---

## 0. Executive Summary

Phase 3 proved the v1 breakout engine, sizing pipeline, and report layer all work end-to-end (manufactured trade-path test produces a closed LONG trade + per-symbol artifacts on unchanged v1 defaults). The real 2026-03 run produced 0 trades because of strict filters + short sample size, not a pipeline bug. **Phase 2e widens the historical dataset so the locked v1 strategy can be exercised across a statistically meaningful window and produce diagnostic baseline statistics — with zero threshold tuning.**

**Key properties:**

- **Zero new runtime dependencies.** Existing Phase 2b / 2c machinery (`BulkDownloader`, `BinanceRestClient`, `ingest_monthly_range`, `ingest_mark_price_monthly_range`, `ingest_funding_range`, `derive_1h_from_15m`, storage helpers, manifests, data-quality checks) already handles month iteration; Phase 2e re-runs it over a wider range.
- **Zero new core source files likely.** Possibly a small aggregation helper if per-month/year breakdowns move into `research.backtest`; otherwise everything is script-level + docs.
- **Default backfill range: 2022-01 through 2026-03** (51 months) for BTCUSDT + ETHUSDT USDⓈ-M perpetual futures: standard 15m klines, derived 1h bars, mark-price 15m klines, funding-rate events. ExchangeInfo snapshot reused (2026-04-19, already cited as GAP-020 proxy).
- **Dataset versions bumped v001 → v002** for all eight existing manifests to preserve Phase 2b/2c immutability audit trail; v002 covers the wider range and declares v001 superseded.
- **Estimated footprint:** ~30–50 MB disk, ~500 HTTP requests to `data.binance.vision`, ~10 REST requests to `fapi.binance.com`, ~5–10 minutes wall-clock including 1000ms fundingRate pacing.
- **Baseline statistics output** per (symbol, year, month): trade count, signal-funnel counts, entry-intents vs filled trades, win rate, expectancy, R-multiple distribution, drawdown, fees/funding/slippage impact, long/short split, exit-reason distribution. Aggregated by year and overall. **Run with locked Phase 3 v1 defaults; no tuning.**
- **Phase 2e does NOT tune parameters.** It does not optimize thresholds. It does not make live-trading recommendations. It prepares a defensible data foundation and a baseline metrics snapshot that Phase 4+ can reference.

**Commits expected: 3–4 + checkpoint.** Runner scripts under `scripts/`, a short baseline summary under `docs/00-meta/implementation-reports/`, ambiguity-log updates, Gate-1/Gate-2 docs, checkpoint report.

**Ambiguity items to surface (3):** GAP-20260419-026 (manifest v002 versioning + v001 supersession), GAP-20260419-027 (per-symbol futures listing-date lower bound on the backfill range), GAP-20260419-028 (where baseline aggregation helpers live — scripts vs `research.backtest`).

**Operator decisions requested:** default range confirmation (2022-01 vs a smaller alternative), ExchangeInfo snapshot handling, manifest-v002 versioning scheme, scripts-only vs promote-aggregators-to-package, and whether to emit the baseline summary Markdown as a committed artifact.

---

## 1. Plain-English Explanation

**Why now.** Phase 3 shipped the strategy + backtester + reports + diagnostics. The real 2026-03 smoke produced 0 trades; the Phase 3 signal-funnel proved that was strict-filter + short-window behavior, not a bug. The manufactured-trade-path test confirmed the full positive path works under unchanged v1 defaults. **What the system needs next is data, not code**: enough history to let the locked filters produce real trade counts so the operator + ChatGPT can look at baseline statistics before deciding anything about Phase 4, parameter review, or risk-increase discussions.

**What Phase 2e is.** It is a *data preparation phase* with a *research-only backtest run* at the end that produces descriptive baseline statistics. It answers: "how many trades does the locked v1 strategy produce over 2022–2026 on BTC and ETH, and how are they distributed across the signal funnel?" It does not answer "should we change any threshold" (that would be a later parameter-review phase with its own gate) or "is the strategy good enough for live capital" (that is Phase 8+ and requires paper/shadow evidence the Phase 2e run cannot provide).

**What Phase 2e is NOT.** It is not Phase 4 (runtime state / persistence / kill-switch — separate phase). It is not a walk-forward validation layer (requires design choices beyond Phase 2e; can be a later task). It is not a parameter optimization or tuning layer — the strategy runs with Phase 3 locked defaults only, and any follow-up parameter sensitivity work is a separate phase with its own gate.

**How light is the footprint.** Existing Phase 2b + 2c + 3 code already handles month iteration, idempotent downloads, checksum verification, manifest writes, quality checks, backtesting, report writing, and the signal-funnel diagnostic. Phase 2e adds at most one script (a two-file wrapper calling existing orchestrators and the backtest engine) and one aggregation helper. It **does not** add new core runtime code.

---

## 2. Current Branch / Status Verification Commands

Run before branch creation; all read-only.

```bash
git -C c:/Prometheus rev-parse --abbrev-ref HEAD           # expect: main
git -C c:/Prometheus status --short                         # expect: (empty)
git -C c:/Prometheus log --oneline -5                       # expect: top = 07be435 (PR #5 Phase 3 merge)
git -C c:/Prometheus rev-list --left-right --count HEAD...@{u}   # expect: 0  0

uv --version       # expect: uv 0.11.7
python --version   # expect: Python 3.12.4
```

**Abort gate.** Any unexpected output → stop and produce a ChatGPT Setup Escalation Prompt. No Phase 2e action until the working tree is clean + `main` is current.

---

## 3. Proposed Branch Name

`phase-2e/wider-historical-backfill`

Rationale: matches Phase 2 / 2b / 2c naming; clearly signals this is a 2-family data phase rather than a new phase number. Phase 2e is distinct from Phase 2d (authenticated endpoints, deferred) and leaves 2d's slot available.

---

## 4. Exact Scope

### 4.1 Phase 2e SHALL

1. **Extend the historical dataset range for BTCUSDT and ETHUSDT USDⓈ-M perpetual futures to cover 2022-01 through 2026-03** (51 months), with these datasets:
   - Standard 15m klines
   - Derived 1h bars (from the 15m klines, using existing `derive_1h_from_15m`)
   - Mark-price 15m klines
   - Funding-rate events
   - ExchangeInfo snapshot (reused unchanged from Phase 2c; no new fetch)

2. **Bump all eight existing Phase 2b/2c dataset manifests from v001 → v002** to preserve immutability audit trail. v001 remains on disk as a historical artifact covering 2026-03 only. v002 covers 2022-01 through 2026-03.

3. **Run the locked Phase 3 v1 backtester over the widened dataset** with `risk_fraction=0.0025`, `risk_usage_fraction=0.90`, `max_effective_leverage=2.0`, `max_notional_internal_usdt=100_000.0`, `taker_fee_rate=0.0005`, `slippage_bucket=MEDIUM`. **No parameter changes from Phase 3.**

4. **Produce baseline statistics per (symbol, year, month) and per (symbol, year)**:
   - Trade count
   - Signal-funnel counts (using Phase 3's `SignalFunnelCounts` — decision bars, bias split, valid setups, breakout candidates, rejection buckets)
   - Entry intents produced vs trades filled
   - Win rate, expectancy (R), profit factor
   - R-multiple distribution
   - Max drawdown (absolute + fraction)
   - Fees / funding / slippage impact
   - Long-vs-short split
   - Exit-reason distribution (STOP / TRAILING_BREACH / STAGNATION / END_OF_DATA)

5. **Emit a per-run backtest report** under `data/derived/backtests/phase-2e-baseline/<run_id>/` with the full Phase 3 artifact bundle (per-symbol `trade_log.parquet` + JSON, `equity_curve.parquet`, `drawdown.parquet`, `r_multiple_hist.parquet`, `summary_metrics.json`, top-level `backtest_report.manifest.json` + `config_snapshot.json`) plus two new breakdown artifacts (`monthly_breakdown.parquet`, `yearly_breakdown.parquet`).

6. **Commit only aggregate summary markdown + manifests, never raw data.** A `docs/00-meta/implementation-reports/2026-04-20_phase-2e-baseline-summary.md` captures the top-line numbers per (symbol, year) and overall. All `data/` outputs remain git-ignored via existing `data/**` / `data/derived/**` patterns.

7. **Pre-verify current official Binance public-data behavior.** Before any real downloads, re-run the TD-006-style WebFetch checks for 2–3 sample months in the new range (one from 2022, one from 2024) to confirm:
   - Monthly ZIP URL pattern unchanged
   - CSV column layout matches current parser
   - CHECKSUM SHA256 format unchanged
   - fundingRate endpoint still 500/5min/IP shared with fundingInfo

### 4.2 Phase 2e SHALL NOT

Non-goals. A Phase 2e PR that touches any of the following should be rejected on scope grounds.

| # | Non-goal | Rationale / owning phase |
|---|----------|--------------------------|
| 1 | Change any v1 strategy threshold | Threshold review is a separate future phase with its own Gate |
| 2 | Optimize / grid-search / sensitivity-sweep v1 parameters | Contaminates Layer-A→C discipline per walk-forward-validation.md |
| 3 | Make profitability, robustness, or live-readiness claims | Phase 2e is descriptive statistics, not promotion evidence |
| 4 | Live trading of any kind | Phases 6–9 |
| 5 | Exchange adapter | Phase 6+ |
| 6 | Authenticated Binance endpoints (`leverageBracket`, `commissionRate`, account/*) | Phase 2d (deferred); GAP-024 accepted limitation |
| 7 | Credentials, `.env`, production keys | Never in research phases |
| 8 | `.mcp.json` / MCP servers / Graphify | Phase-0 policy retained |
| 9 | Dashboard / UI / manual trading controls | Phase 5 |
| 10 | Phase 4 runtime state (SAFE_MODE / kill switch / SQLite persistence) | **Phase 4** |
| 11 | Edit `docs/12-roadmap/technical-debt-register.md` without explicit operator approval | Per operator directive carried from Phases 2c/3 |
| 12 | Edit `.claude/**`, `CLAUDE.md`, `current-project-state.md` | Agent pack + root state are operator-gated |
| 13 | New runtime dependencies | The existing stack covers every need |
| 14 | Run Phase 2e across symbols other than BTCUSDT + ETHUSDT | Research allowlist per `docs/07-risk/exposure-limits.md` |
| 15 | Commit generated backtest artifacts under `data/` | `.gitignore` covers; Phase 2e enforces by adding only aggregated summaries to docs |
| 16 | Walk-forward validation (Layer B), holdout (Layer C), or exit-model comparison | Higher-layer validation work; separate phase if pursued |
| 17 | Parameter sensitivity across fee rates / slippage buckets / risk fractions as promotion evidence | Can be run as *diagnostic sensitivity* only; never as optimization |

---

## 5. Code Changes Needed

**Assessment: minimal. Ideally zero source-code changes; at most one small aggregation helper + two operator-facing scripts.**

### 5.1 Existing machinery already covers

| Need | Existing module / function | Evidence |
|---|---|---|
| Monthly iteration over kline ZIPs | `research.data.ingest.ingest_monthly_range` | Phase 2b; idempotent via state file in `data/manifests/_downloads/` |
| Monthly iteration over mark-price ZIPs | `research.data.ingest.ingest_mark_price_monthly_range` | Phase 2c; same idempotency model |
| Funding-rate pagination across date range | `research.data.ingest.ingest_funding_range` | Phase 2c; ascending-cursor pagination with stuck-cursor safeguard |
| Checksum verification of ZIPs | `research.data.binance_bulk.BulkDownloader.download_month` | Phase 2b; SHA256 match against published CHECKSUM file |
| Normalized Parquet writes (Hive partitioned) | `research.data.storage.write_klines` / `write_mark_price_klines` / `write_funding_rate_events` | Phase 2 / 2b / 2c |
| Derived 1h bars | `research.data.derive.derive_1h_from_15m` | Phase 2; emits `InvalidWindow` for partial buckets |
| Quality checks (duplicates, missing bars, magnitude, monotonicity) | `research.data.quality.check_*` | Phase 2 / 2c |
| Dataset manifests with version policy `<name>__vNNN` | `research.data.manifests.DatasetManifest` + `write_manifest` | Phase 2; write_manifest is immutable |
| Phase 3 backtester (BacktestEngine) | `research.backtest.engine.BacktestEngine` | Phase 3; runs over any Hive-partitioned Parquet root |
| Signal-funnel diagnostic | `research.backtest.diagnostics.run_signal_funnel` | Phase 3; already emits per-symbol counts |
| Report writer (trade log, equity, drawdown, hist, metrics, manifest) | `research.backtest.report.write_report` | Phase 3 |

### 5.2 Proposed new code

1. **`scripts/phase2e_backfill.py`** (operator-facing runner, ~120 lines): iterates months from config, calls existing orchestrators with `dataset_version_*="..._v002"`, logs coverage per (symbol, year, month). Not committed to the core package.

2. **`scripts/phase2e_baseline_backtest.py`** (operator-facing runner, ~150 lines): loads the widened data via existing `storage.read_*` helpers, runs `BacktestEngine.run`, calls `run_signal_funnel` per symbol, aggregates results per (symbol, year, month) + per (symbol, year), writes breakdown Parquets alongside the standard Phase 3 artifacts, and prints a condensed terminal summary. Not committed to core.

3. **(Optional) `src/prometheus/research/backtest/monthly_aggregates.py`** (~80 lines) with a small `aggregate_trades_by_month(trades, accounting)` function + per-year wrapper. Promotes the aggregation logic into the package so future phases can reuse it. **Operator decision at Gate 1 §11 (D3)**: keep in `scripts/` for Phase 2e minimalism, or promote to `research.backtest` with tests. Default recommendation: keep in `scripts/` this phase, promote if a future phase needs it.

### 5.3 No changes to

- `src/prometheus/strategy/**` (locked)
- `src/prometheus/core/**` (stable)
- `src/prometheus/research/data/**` core orchestrators (Phase 2b/2c surface unchanged)
- `src/prometheus/research/backtest/**` engine / report / diagnostics (Phase 3 surface unchanged)
- `configs/dev.example.yaml` strategy and backtest defaults (locked from Phase 3)
- `.gitignore` (existing `data/**` and `data/derived/**` rules already cover new artifacts)

---

## 6. Dependency Additions

**None proposed.** numpy, pyarrow, duckdb, pydantic, httpx are all already pinned. No new direct or transitive runtime dep is required for a wider-range re-run of existing code paths. If Gate-2 execution uncovers a missing capability (e.g., progress-bar library for long-running downloads), it will be surfaced as a new ambiguity item; nothing should be added silently.

---

## 7. Proposed Default Backfill Range + Alternatives

### 7.1 Default: **2022-01 through 2026-03 (51 months)**

Rationale:
- **Starts well after symbol listing.** BTCUSDT USDⓈ-M perpetual futures listed 2019-09-10; ETHUSDT shortly after. 2022-01 is 2.3 years post-listing — no early-listing edge-case months.
- **Covers multiple market regimes.** 2022 bear, 2023 chop, 2024 rally, 2025 macro, 2026-Q1 current. Important for baseline statistics to reflect regime diversity even though Phase 2e is NOT claiming walk-forward validity.
- **Reasonable runtime.** ~5–10 minutes wall-clock for download + normalize + derive + backtest.
- **Reasonable storage.** ~30–50 MB total data/ footprint. Keeps the repo + local dev environment small.
- **Statistically meaningful sample for baseline diagnostics.** At ~0 trades per month observed in the Phase 3 2026-03 smoke (strict filters), a 51-month window is expected to yield at most a few dozen trades per symbol (order-of-magnitude estimate from the funnel: ~14 candidates in 2165 BTC 2026-03 decision bars; over 51 months that scales to perhaps ~300–700 candidates; roughly 10–50 that survive all filters given Phase 3's observed candidate-survival ratio). Those numbers are illustrative — Phase 2e reports actual counts.

### 7.2 Alternatives

| Option | Range | Months | Expected data/ disk | Expected wall time | Rationale |
|---|---|---|---|---|---|
| **A (default)** | 2022-01 to 2026-03 | 51 | ~30–50 MB | 5–10 min | Recommended |
| B (mid) | 2024-01 to 2026-03 | 27 | ~18–25 MB | 3–6 min | Lighter; covers 2024 rally + 2025 + 2026-Q1 |
| C (small) | 2025-01 to 2026-03 | 15 | ~10–15 MB | 2–4 min | Smallest meaningful; single year + Q1 |
| D (staged) | year-by-year: 2022, then 2023, … | 12 / iteration | grows | 1–3 min per year | Lets operator validate each year before proceeding |

**Operator approves exactly one range at Gate 1.** Default recommendation is A.

### 7.3 Estimated disk footprint by dataset (default range A)

Based on measured Phase 2b/2c 2026-03 file sizes:

| Dataset | Per-month size | Months × symbols | Total |
|---|---|---|---|
| Raw kline ZIPs | ~145 KB | 51 × 2 = 102 | ~15 MB |
| Raw mark-price ZIPs | ~85 KB | 51 × 2 = 102 | ~9 MB |
| Raw CHECKSUM files | ~70 bytes | 204 | ~15 KB |
| Normalized klines Parquet | ~20 KB / month-symbol | 102 | ~2 MB |
| Normalized mark-price Parquet | ~15 KB / month-symbol | 102 | ~1.5 MB |
| Derived 1h Parquet | ~6 KB / month-symbol | 102 | ~0.6 MB |
| Normalized funding Parquet | ~3 KB / month-symbol | 102 | ~0.3 MB |
| Manifests (8 v002 + 2 state files) | ~1 KB each | ~10 | ~10 KB |
| Backtest report artifacts | ~100 KB total | 1 run | ~0.1 MB |

**Total ≈ 28 MB.** Slack ~50 MB. All git-ignored via existing `data/` rules.

### 7.4 Expected network requests (default range A)

- `data.binance.vision` monthly ZIPs: 51 × 2 × 2 (kline + mark-price) = **204 HTTP requests**
- `data.binance.vision` CHECKSUM files: **204 HTTP requests** (one per ZIP)
- `fapi.binance.com /fapi/v1/fundingRate` REST: ~5 pagination pages × 2 symbols = **~10 REST requests**
- `fapi.binance.com /fapi/v1/exchangeInfo`: **0 new requests** (reuse 2026-04-19 snapshot)

**Total: ~418 network requests.** At the conservative pace_ms settings (100ms bulk, 1000ms fundingRate), total wall time is bounded by serialization + request latency. Estimated 5–10 minutes for the full download + normalize pipeline.

---

## 8. Resumability / Idempotency / Partial-Download Recovery

### 8.1 Existing machinery

- **Bulk downloader:** `BulkDownloader.download_month` is idempotent. If the target ZIP already exists with matching SHA256, it's reused. If SHA256 mismatches, the partial file is deleted and re-downloaded. If checksum fetch fails mid-ZIP, the `.partial` file is cleaned up.
- **State files:** `data/manifests/_downloads/<dataset_name>__state.json` tracks each month's status (`PENDING` / `VERIFIED` / `NORMALIZED`). `ingest_monthly_range` skips `NORMALIZED` months.
- **Manifest immutability:** Once a v001 manifest is written, it cannot be overwritten. Phase 2e writes v002 manifests; v001 remains as audit trail.
- **Normalized Parquet writes:** `storage.write_klines` creates partitions via `Path.mkdir(parents=True, exist_ok=True)`; re-writing the same partition is a no-op at the partition level but the orchestrator's state guard prevents re-processing `NORMALIZED` months.

### 8.2 Phase 2e plan

1. **Run the backfill in one pass.** If it fails midway (network flake, disk full), re-run the script. The state file picks up where it left off.
2. **No mid-run cleanup.** If a month ends up with only a raw ZIP but no normalized Parquet (`VERIFIED` status in state), re-running completes the normalization.
3. **v001 manifests preserved.** The Phase 2e runner script passes `dataset_version_*="..._v002"` so existing v001 manifests are never touched.
4. **Explicit "resumable" checklist in operator script.** The runner prints per-month status before touching any network, so the operator can see what's already on disk and what's about to be fetched.

### 8.3 Partial-download recovery

- **Detection.** Checksum mismatch in `BulkDownloader` → file deleted, retry.
- **Recovery.** Re-run the runner script. State file reflects only `VERIFIED` (SHA256 match) months; re-runs re-attempt `PENDING` or `DOWNLOADING` months.
- **Escalation.** If a particular month fails repeatedly (e.g., data.binance.vision rate-limiting us), operator + ChatGPT review with the full error log before retrying.

---

## 9. Data-Quality + Integrity Plan

### 9.1 Bulk ZIP checksum verification

Already enforced by `BulkDownloader`:

1. Fetch ZIP and CHECKSUM files in parallel.
2. Compute local SHA256 from the downloaded ZIP bytes.
3. Parse the published CHECKSUM (format: `<sha256>  <filename>`).
4. Assert match; if mismatch, delete local ZIP and raise `BulkChecksumError`.

**Phase 2e does not change this behavior.** The runner script logs matched SHA256s per (symbol, month) for the Gate 2 report.

### 9.2 REST pacing (fundingRate)

Already enforced by `BinanceRestClient`:

- Default `pace_ms=1000` (1 request/sec).
- Documented rate limit per GAP-20260419-012: `500 requests / 5 min / IP` shared with `/fapi/v1/fundingInfo`.
- At 1 req/sec: ~300 requests in 5 minutes, well below the 500 limit (40% margin).
- Exponential backoff on 429 with jitter from stdlib `random.Random`.

**Phase 2e does not change pacing.** The baseline backfill for 2022-01 through 2026-03 needs only ~10 fundingRate REST requests total, well below any rate concern.

### 9.3 Raw data preservation

- Raw ZIPs persisted under `data/raw/binance_usdm/klines/symbol=.../interval=.../year=.../month=.../*.zip` and `data/raw/binance_usdm/markPriceKlines/...` — same layout as Phase 2b/2c.
- Raw files are never deleted by Phase 2e code paths (except mid-download partial-cleanup on checksum failure).
- Operator can purge `data/raw/` manually after successful normalization if disk pressure requires; the state file records SHA256 so re-download is deterministic.

### 9.4 Normalized Parquet output

- Partitioned by `(symbol, interval, year, month)` for klines and mark-price; by `(symbol, year, month)` for funding.
- Each row validated against `NormalizedKline` / `MarkPriceKline` / `FundingRateEvent` on write and on read.
- `storage.read_*` helpers normalize partition-column types (string → enum) via the Phase 2 `BeforeValidator` pattern (GAP-008).

### 9.5 Derived 1h generation

- `derive_1h_from_15m` runs AFTER all monthly 15m partitions are written.
- For every 1h bucket `[H, H + 3_600_000)`, the helper requires all four 15m bars at `H`, `H+900_000`, `H+1_800_000`, `H+2_700_000` to be present.
- Missing or misaligned buckets → recorded as `InvalidWindow` and excluded; the derived 1h bar is NOT emitted.
- `InvalidWindow` entries are accumulated and included in the 1h derived manifest.

### 9.6 Dataset manifest / versioning plan

- **v001 preserved unchanged** on disk. Source URLs + "Phase 2b/2c ..." notes remain as historical audit trail.
- **v002 written** for each of the 8 datasets covering the wider range:
  - `binance_usdm_btcusdt_15m__v002.manifest.json`
  - `binance_usdm_ethusdt_15m__v002.manifest.json`
  - `binance_usdm_btcusdt_1h_derived__v002.manifest.json`
  - `binance_usdm_ethusdt_1h_derived__v002.manifest.json`
  - `binance_usdm_btcusdt_markprice_15m__v002.manifest.json`
  - `binance_usdm_ethusdt_markprice_15m__v002.manifest.json`
  - `binance_usdm_btcusdt_funding__v002.manifest.json`
  - `binance_usdm_ethusdt_funding__v002.manifest.json`
- **v002 manifest `predecessor_version`** field set to `"binance_usdm_<symbol>_<dataset>__v001"` for each — provides machine-readable upgrade trail (fixes GAP-20260419-003's predecessor_version-null observation for this new version).
- **Notes field** states: "Phase 2e wider backfill. Range: 2022-01 through 2026-03. Supersedes v001 (which covered 2026-03 only)."

### 9.7 Invalid-window logging plan

- `derive_1h_from_15m` continues to emit `InvalidWindow` entries for partial 1h buckets.
- `ingest_monthly_range` aggregates them into the v002 1h derived manifest.
- The backtester already respects `InvalidWindow` entries via the data-quality check `check_no_missing_bars` when the operator runs it.
- **Phase 2e adds** a per-dataset coverage summary in the runner's terminal output: "BTCUSDT 15m: 102/102 months, 0 invalid windows. 1h derived: 4896 bars, 0 invalid buckets." (numbers illustrative).

### 9.8 Duplicate / missing / malformed detection

- `quality.check_no_duplicates` runs automatically during normalization in `ingest_monthly_range` per Phase 2b pattern.
- `quality.check_timestamp_monotonic` runs per monthly partition.
- `quality.check_no_missing_bars` can be run post-ingest by the operator script with `expected_start_ms`/`expected_end_ms` = month boundaries.
- Malformed bars (OHLC invariant violations, negative volumes) → `DataIntegrityError` raised by `NormalizedKline._validate_invariants`; operator intervention required.

### 9.9 UTC Unix millisecond validation

- Every timestamp field (`open_time`, `close_time`, `funding_time`) stored as Python `int` in Parquet `int64` columns (Phase 2 guarantee).
- `NormalizedKline._validate_invariants` enforces `close_time == open_time + interval_ms - 1` on every bar.
- `is_aligned_open_time` enforces `open_time % interval_ms == 0`.
- Funding events enforce `funding_time > 0` and reasonable funding_rate magnitude (< 100%).
- Phase 2e does not add new timestamp logic; it relies on existing model invariants.

---

## 10. Baseline Backtest Readiness + Statistics Plan

### 10.1 Readiness

After the backfill completes, readiness requires:

- [ ] All 8 v002 manifests written and validated against Pydantic `DatasetManifest` model
- [ ] BTCUSDT + ETHUSDT coverage: 51 consecutive months × 4 datasets each, zero invalid months
- [ ] `check_no_duplicates` green on all 8 datasets over the full range
- [ ] `check_timestamp_monotonic` green per-partition
- [ ] `check_funding_events_within_window` green with `expected_start_ms` = 2022-01-01 00:00:00 UTC, `expected_end_ms` = 2026-04-01 00:00:00 UTC
- [ ] ExchangeInfo snapshot at `data/derived/exchange_info/2026-04-19T21-22-59Z.json` loadable via `ExchangeInfoSnapshot.model_validate`

### 10.2 Baseline run configuration (locked Phase 3 defaults; no tuning)

```
experiment_name:        phase-2e-baseline
run_id:                 <UTC timestamp>
symbols:                (BTCUSDT, ETHUSDT)
window_start_ms:        2022-01-01T00:00:00Z (as UTC ms)
window_end_ms:          2026-04-01T00:00:00Z (as UTC ms, exclusive)
sizing_equity_usdt:     10_000.0     # per GAP-021
risk_fraction:          0.0025       # per GAP-R4; 0.25%
risk_usage_fraction:    0.90         # per GAP-022
max_effective_leverage: 2.0          # v1 locked
max_notional_internal:  100_000.0    # per GAP-023
taker_fee_rate:         0.0005       # per GAP-018 primary baseline
slippage_bucket:        MEDIUM       # 3 bps per side
adapter:                FAKE         # mechanically the only option
```

**Sensitivity variants are OPTIONAL and allowed only as separately-labeled runs**:
- `taker_fee_rate ∈ {0.0005, 0.0004, 0.0002}` — per GAP-018
- `slippage_bucket ∈ {LOW, MEDIUM, HIGH}` — per Phase 3 plan §11.A.A5
- `risk_usage_fraction ∈ {0.90, 1.00}` — per GAP-022

Each sensitivity run is a separate `run_id`, does not affect the primary baseline, and is explicitly labeled in the summary markdown. **This is sensitivity reporting, not optimization.**

### 10.3 Statistics to emit (per symbol)

Aggregated in three granularities:

**(a) Overall (per symbol across 2022-01 through 2026-03):**
- Total trades; long count; short count
- Win rate; expectancy (R); profit factor; avg winner (R); avg loser (R); median R
- Total net PnL (USDT and %); total fees; total funding; total slippage
- Max drawdown (USDT + %); worst losing streak
- Exit-reason distribution (STOP / TRAILING_BREACH / STAGNATION / END_OF_DATA)
- Signal-funnel totals: decision bars, bias split, valid setups, candidates, rejections by reason

**(b) Per year (4 years + partial Q1):**
- Same metrics per calendar year

**(c) Per month (51 rows):**
- Trade count, win count, net PnL, max drawdown within month, signal-funnel counts

### 10.4 Output layout

```
data/derived/backtests/phase-2e-baseline/<run_id>/
├── backtest_report.manifest.json             # top-level, cites v002 manifests + ExchangeInfo
├── config_snapshot.json                      # exact BacktestConfig
├── BTCUSDT/
│   ├── trade_log.parquet                     # Phase 3 schema
│   ├── trade_log.json                        # sidecar
│   ├── equity_curve.parquet
│   ├── drawdown.parquet
│   ├── r_multiple_hist.parquet
│   ├── summary_metrics.json
│   ├── funnel_total.json                     # SignalFunnelCounts aggregated over full range
│   ├── funnel_by_month.parquet               # NEW: per-month funnel counts (51 rows)
│   ├── monthly_breakdown.parquet             # NEW: per-month trade/pnl/dd stats (51 rows)
│   └── yearly_breakdown.parquet              # NEW: per-year stats (5 rows: 2022/2023/2024/2025/2026)
└── ETHUSDT/
    └── ... (same layout)
```

**All under `data/derived/backtests/**` which is git-ignored** via existing `data/derived/**` pattern.

### 10.5 Committed aggregate summary

`docs/00-meta/implementation-reports/2026-04-20_phase-2e-baseline-summary.md` — a committable Markdown that captures aggregate numbers only, no trade-by-trade data. Rough template:

```
# Phase 2e Baseline Summary

Window: 2022-01-01 to 2026-03-31 UTC. Locked Phase 3 v1 defaults.
Datasets: binance_usdm_{btc,eth}usdt_{15m,1h_derived,markprice_15m,funding}__v002.
ExchangeInfo snapshot: 2026-04-19T21-22-59Z (GAP-020 accepted proxy).

## BTCUSDT (51 months)

- Trades: 27 (19 long, 8 short)
- Win rate: 44.4%; Expectancy: +0.18 R/trade
- Net PnL: +4.3% | Gross +5.1% | Fees -0.4% | Funding -0.3% | Slippage -0.1%
- Max drawdown: -2.1% | Worst streak: 4 losses
- Exit reasons: STOP=11, STAGNATION=9, TRAILING=5, END_OF_DATA=2
- Signal funnel: 147,260 decision bars → 78,412 directional-bias → 4,127 valid setups
  → 85 candidates → 27 fills. Dominant rejection: no-valid-setup (68% of decision bars).

## ETHUSDT (same layout)

## Per-year / per-month tables (illustrative)

| Year | Symbol | Trades | Win% | Net% | MaxDD% |
|------|--------|--------|------|------|--------|
| 2022 | BTCUSDT | 6 | 33.3 | -0.8 | -1.5 |
| 2023 | BTCUSDT | 8 | 50.0 | +1.9 | -0.7 |
| … etc. |
```

Numbers above are **illustrative**. Actual Phase 2e run produces real values.

---

## 11. Ambiguity / Spec-Gap Items to Log

Upon Gate 1 approval, append to `docs/00-meta/implementation-ambiguity-log.md`:

### GAP-20260419-026 — Dataset manifest versioning scheme for wider backfill: v001 → v002

- **Status:** OPEN — operator decision at Gate 1.
- **Area:** DATA / ARCHITECTURE.
- **Description:** Phase 2b / 2c wrote v001 manifests for each of the 8 datasets covering only 2026-03. Phase 2e needs to extend coverage to 2022-01 through 2026-03. `write_manifest` is immutable (Phase 2 GAP-008 design). Three options:
  - **A (recommended):** Bump to v002 for all 8 datasets; v001 preserved as audit trail. `predecessor_version` field on v002 points to v001.
  - B: Delete v001 and re-write v001 covering wider range. Loses audit trail; violates Phase 2 immutability spirit.
  - C: Emit per-month manifests. Increases manifest count 8× and requires manifest-reader changes. Over-engineering for Phase 2e scope.
- **Recommendation:** Option A.

### GAP-20260419-027 — Binance USDⓈ-M perpetual futures listing-date lower bound

- **Status:** OPEN — informational; the default 2022-01 start is safely after listing, so no blocker.
- **Area:** DATA / EXCHANGE_API.
- **Description:** BTCUSDT USDⓈ-M perpetual futures listed 2019-09-10; ETHUSDT listed 2019-11-27. If Phase 2e extends start date earlier than these, the bulk downloader will receive 404 for non-existent months. The default 2022-01 is safely 2+ years after both listings. If operator selects an alternative range starting before 2020-Q1, the Gate-2 execution must handle 404s gracefully (option: skip missing months + record `InvalidWindow` entries).
- **Recommendation:** Default range 2022-01 avoids this concern entirely.

### GAP-20260419-028 — Location of baseline aggregation helpers

- **Status:** OPEN — operator decision at Gate 1.
- **Area:** ARCHITECTURE.
- **Description:** Phase 2e needs `aggregate_trades_by_month`, `aggregate_trades_by_year`, and per-month signal-funnel aggregation. Two placements:
  - **A (recommended for Phase 2e):** Keep in `scripts/phase2e_baseline_backtest.py` as private helpers. Keeps Phase 2e scope minimal; no new core source file.
  - B: Promote to `src/prometheus/research/backtest/monthly_aggregates.py` with unit tests. Better if Phase 4/5 needs them; more Phase 2e code to review.
- **Recommendation:** Option A for Phase 2e. If a later phase needs re-use, promote then.

---

## 12. Technical-Debt Register Items Affected

**No direct edits to `docs/12-roadmap/technical-debt-register.md` by Phase 2e.** Per operator directive carried from Phases 2c and 3.

For reference only — items Phase 2e will touch or graduate:

- **GAP-20260419-025 (Phase 2e wider historical backfill; DEFERRED)** — graduates toward RESOLVED upon Phase 2e completion. Ambiguity log entry will be updated with Resolution evidence pointing to v002 manifests + baseline summary markdown.
- **GAP-20260419-020 (ExchangeInfo 2026-04-19 snapshot as 2026-03 proxy; ACCEPTED_LIMITATION)** — widens in scope to cover 2022-01 through 2026-03 backtest window. The accepted-limitation text on each Phase 2e baseline manifest explicitly notes the proxy span. No register edit; the accepted limitation already covers this class.
- **GAP-20260419-018 (taker commission placeholder; ACCEPTED_LIMITATION)** — unchanged. Baseline uses 0.05% primary; optional sensitivity runs use 0.04% / 0.02% as separate `run_id`s.
- **GAP-20260419-024 (Phase 2d deferred; ACCEPTED_LIMITATION)** — unchanged. Phase 2e does not touch authenticated endpoints.
- **TD-016 (statistical thresholds require evidence)** — Phase 2e produces descriptive baseline statistics, NOT promotion-grade statistics. TD-016 remains OPEN; Phase 2e is a prerequisite data foundation, not the statistical evidence.
- **TD-018 (tiny-live notional cap TBD)** — unchanged. Phase 2e uses the research cap (100,000 USDT) per GAP-023.

If operator approves a separate follow-up commit to update the TD-register, Phase 2e's completion could annotate:
- TD-016: "Phase 2e baseline statistics captured; promotion-grade walk-forward work still required."
- New potential entry: TD-022 (Phase 2e baseline — descriptive only; walk-forward not performed).

**Phase 2e proposal does NOT edit the register. Flagged here for operator consideration only.**

---

## 13. Safety Constraints

| Constraint | Phase 2e behavior |
|---|---|
| Production Binance API keys | **Not created, not requested, not used.** All endpoints are public. |
| `.env` / credentials | **None.** |
| Authenticated endpoints | **Not touched.** `leverageBracket`, `commissionRate`, account/* all remain Phase 2d (deferred). |
| REST calls | Only public `/fapi/v1/fundingRate` (~10 calls) and reuse of existing `/fapi/v1/exchangeInfo` snapshot (0 new calls). |
| Bulk download calls | Only public `data.binance.vision` CDN (~408 calls). |
| WebSocket / user stream | **None.** |
| Third-party market-data sources | **None.** Only Binance public data. |
| `.mcp.json` / MCP / Graphify | **Not created / not enabled.** |
| Dashboard / UI / manual trading controls | **None added.** |
| Phase 4 runtime state (SAFE_MODE / kill switch / SQLite persistence) | **Not implemented.** |
| Exchange adapter | **None.** BacktestAdapter remains FAKE-only per Phase 3. |
| Parameter tuning / optimization | **Forbidden.** Primary baseline uses Phase 3 locked defaults. |
| Profitability claims | **Forbidden.** Summary markdown explicitly labels outputs as "descriptive baseline, not promotion evidence." |
| Live-trading recommendations | **Forbidden.** |
| Generated artifacts outside `data/derived/backtests/phase-2e-baseline/` | **None.** Write scope is strictly bounded. |
| Committing real market data | **Forbidden.** Raw ZIPs + normalized Parquet + backtest artifacts all git-ignored via `data/**` rules. |
| Edits to `docs/12-roadmap/technical-debt-register.md` | **None** (operator directive). |
| Edits to `.claude/`, `CLAUDE.md`, `current-project-state.md` | **None.** |
| Destructive git | **None.** Only branch creation + add + commit. |
| `--force` / `--no-verify` / `git add -f` | **Never.** |
| Mechanical import-graph guardrail | **Still enforced** via existing `test_import_graph.py`; Phase 2e adds zero forbidden imports. |

---

## 14. Proposed Commit Structure

**Target: 4 commits + checkpoint.** Small, independently reviewable.

| # | Theme | Files (indicative) |
|---|---|---|
| 1 | Backfill runner script | `scripts/phase2e_backfill.py` (+ minimal smoke test if in scope) |
| 2 | Baseline backtest runner script | `scripts/phase2e_baseline_backtest.py` (+ minimal smoke test if in scope) |
| 3 | Baseline summary markdown (aggregate-only, committable) | `docs/00-meta/implementation-reports/2026-04-20_phase-2e-baseline-summary.md` |
| 4 | Ambiguity log + Gate-1 plan + Gate-2 review + optional configs annotation | `docs/00-meta/implementation-ambiguity-log.md`, `docs/00-meta/implementation-reports/2026-04-20_phase-2e_gate-1-plan.md`, `docs/00-meta/implementation-reports/2026-04-20_phase-2e_gate-2-review.md` |
| 5 (post-approval) | Phase 2e checkpoint report | `docs/00-meta/implementation-reports/2026-04-20_phase-2e-checkpoint-report.md` |

**Zero commits to core source code** under this plan (assuming GAP-028 Option A).

**Zero commits to generated data** under `data/**` — all artifacts stay git-ignored.

**Every commit tip passes quality gates.** Scripts are small and self-contained; smoke tests (if added) exercise argparse + config-build only, no real network.

---

## 15. Gate 2 Review Format

At Gate 2 (pre-commit review), produce `docs/00-meta/implementation-reports/2026-04-20_phase-2e_gate-2-review.md` with:

1. **Executive summary** — 1 paragraph
2. **Backfill command + output excerpt** — `uv run python scripts/phase2e_backfill.py ...` with coverage-per-month summary table
3. **v002 manifest inventory** — 8 files + paths + byte sizes
4. **Quality-gate results** — `ruff check`, `ruff format --check`, `mypy`, `pytest` output
5. **Backfill verification checklist** — §10.1 readiness items ticked
6. **Baseline backtest run output** — trade counts per symbol, overall + per-year summary
7. **Signal-funnel breakdown** — totals + per-year across both symbols
8. **Sensitivity runs (if any)** — labeled separately, same schema
9. **Scope verification vs §4.1** — item-by-item
10. **Non-goal verification vs §4.2** — item-by-item
11. **Safety constraints verification** — §13 table with PASS/observed columns
12. **Dataset citations** — all 16 v002 + v001 manifest paths cited
13. **Ambiguity decisions applied** — GAP-026 / GAP-027 / GAP-028 outcomes
14. **git diff --stat** over the commits
15. **Proposed final commit order** (4 commits)
16. **Request for Gate 2 approval**

Following Gate 2 approval, commits are executed in sequence, and a **Phase 2e Checkpoint Report** is produced with the format required by `.claude/rules/prometheus-phase-workflow.md`.

---

## 16. Tests / Checks to Run

### Pre-execution (Gate 2 readiness)

- `git status` clean on the branch
- `uv sync` clean
- `uv run ruff check .`
- `uv run ruff format --check .`
- `uv run mypy`
- `uv run pytest` — 374 tests (Phase 3 baseline) must still pass unchanged. Phase 2e may add 0–3 smoke tests (argparse + config validation for the runner scripts).

### During backfill execution

- `BulkDownloader` logs every SHA256 match per (symbol, month) — must equal 204 matches.
- State file for each dataset reaches `NORMALIZED` status for every month in range.
- `derive_1h_from_15m` runs end-to-end with invalid_windows count reported.
- `check_no_duplicates`, `check_timestamp_monotonic`, `check_no_missing_bars` all green on all 8 v002 datasets.
- `ingest_funding_range` completes without 429 responses.
- Zero unexpected files appear in `git status`.

### During baseline backtest run

- `BacktestEngine.run` completes with `result.warnings == []` for both symbols.
- `run_signal_funnel` bucket-accounting invariant holds on both symbols (the `_invariants` check from Phase 3 diagnostic tests).
- Report writer emits all expected artifacts per symbol (the Phase 3 manufactured-trade-path test schema).
- Trade records validate against the `TradeRecord` Pydantic model.
- Summary markdown numeric consistency: per-symbol trade counts = sum of per-year counts = sum of per-month counts.

### Post-execution (commit prep)

- Quality gates green again (identical to pre-execution).
- `git check-ignore -v data/derived/backtests/phase-2e-baseline/<run_id>/...` confirms run artifacts are ignored.
- `git diff --stat` shows only docs + scripts changes.

---

## 17. Gate 1 Approval Requests

Operator, please respond on the following so Phase 2e implementation can begin:

1. **Overall plan approval** — accept, modify, or reject.
2. **Branch name** — `phase-2e/wider-historical-backfill` acceptable?
3. **Backfill range** — §7.2 Option A (2022-01 to 2026-03) recommended. Confirm or pick alternative B / C / D.
4. **Manifest versioning (GAP-20260419-026)** — confirm Option A (bump to v002, preserve v001).
5. **Listing-date edge case (GAP-20260419-027)** — default 2022-01 avoids; confirm no earlier start.
6. **Aggregation helper placement (GAP-20260419-028)** — keep in `scripts/` (Option A) or promote to `research.backtest.monthly_aggregates` (Option B)?
7. **Baseline summary markdown** — commit a condensed aggregate-only Markdown (recommended) or keep summary in `data/derived/` only?
8. **Sensitivity runs** — include {fee-rate, slippage-bucket, risk-usage} sensitivity variants in Phase 2e scope, or defer them to a separate follow-up?
9. **ExchangeInfo** — reuse existing 2026-04-19 snapshot (recommended) or fetch a fresh one?
10. **Commit granularity** — 4 commits + checkpoint acceptable? Preference for fewer / more?
11. **TD-register follow-up** — approve a separate small TD-register update (not in Phase 2e commits) to note GAP-025 resolution + TD-016 context? Recommended but strictly out-of-Phase-2e-scope.
12. **Additional non-goals or constraints** — anything to add before Phase 2e execution begins?

**No implementation will start until all of the above are explicitly answered.**

---

## Appendix A — Existing Machinery Inventory (Reuse Evidence)

**Data layer (Phase 2 / 2b / 2c):**

- `src/prometheus/research/data/binance_bulk.py` — `BulkDownloader`, `BulkFamily` (KLINES, MARK_PRICE_KLINES)
- `src/prometheus/research/data/binance_rest.py` — `BinanceRestClient` with 1000ms default pacing, auth-surface mechanical guardrails
- `src/prometheus/research/data/funding_rate.py` — `fetch_funding_events_raw`, `normalize_funding_events`
- `src/prometheus/research/data/exchange_info.py` — `parse_exchange_info`, `fetch_exchange_info_snapshot`
- `src/prometheus/research/data/ingest.py` — `ingest_monthly_range`, `ingest_mark_price_monthly_range`, `ingest_funding_range`
- `src/prometheus/research/data/storage.py` — `write_klines`/`read_klines`, `write_mark_price_klines`/`read_mark_price_klines`, `write_funding_rate_events`/`read_funding_rate_events`, `attach_dataset_view`, `query_completed_bars`
- `src/prometheus/research/data/derive.py` — `derive_1h_from_15m`
- `src/prometheus/research/data/quality.py` — `check_no_duplicates`, `check_timestamp_monotonic`, `check_no_missing_bars`, `check_no_future_bars`, `check_no_duplicate_funding_events`, `check_funding_events_within_window`, `check_funding_rate_magnitude`
- `src/prometheus/research/data/manifests.py` — `DatasetManifest`, `read_manifest`, `write_manifest`
- `src/prometheus/research/data/download_state.py` — `MonthDownloadState`, `DownloadStatus`

**Backtest layer (Phase 3):**

- `src/prometheus/research/backtest/engine.py` — `BacktestEngine`, `BacktestRunResult`
- `src/prometheus/research/backtest/config.py` — `BacktestConfig`, `BacktestAdapter` (FAKE-only)
- `src/prometheus/research/backtest/diagnostics.py` — `SignalFunnelCounts`, `run_signal_funnel`
- `src/prometheus/research/backtest/report.py` — `BacktestReportManifest`, `DatasetCitation`, `write_report`, `compute_equity_curve`, `compute_drawdown_series`, `compute_r_multiple_histogram`, `compute_summary_metrics`
- `src/prometheus/research/backtest/trade_log.py` — `TradeRecord`, `write_trade_log`

**Strategy layer (Phase 3):**

- `src/prometheus/strategy/v1_breakout/strategy.py` — `V1BreakoutStrategy`, `StrategySession`
- `src/prometheus/strategy/types.py` — intents + enums

**All re-used as-is by Phase 2e.** No modifications.

---

## Appendix B — File Provenance

This plan was produced from:

- `docs/00-meta/current-project-state.md`
- `docs/00-meta/ai-coding-handoff.md`
- `docs/12-roadmap/phase-gates.md`
- `docs/12-roadmap/technical-debt-register.md`
- `docs/00-meta/implementation-ambiguity-log.md` (entries 001–025)
- `docs/00-meta/implementation-reports/2026-04-19_phase-3-checkpoint-report.md`
- `docs/00-meta/implementation-reports/2026-04-19_phase-3_gate-2-review.md`
- `docs/04-data/{data-requirements,historical-data-spec,timestamp-policy,dataset-versioning}.md`
- `docs/05-backtesting-validation/{v1-breakout-validation-checklist,backtesting-principles,walk-forward-validation,cost-modeling}.md`
- `docs/03-strategy-research/{v1-breakout-strategy-spec,v1-breakout-backtest-plan}.md`
- `docs/08-architecture/codebase-structure.md`
- `.claude/rules/prometheus-{core,safety,phase-workflow,mcp-and-secrets}.md`
- Phase 2 / 2b / 2c / 3 source code at `src/prometheus/research/{data,backtest}/`, `src/prometheus/strategy/`, `src/prometheus/core/`
- Phase 2 / 2b / 2c / 3 test patterns at `tests/unit/**`, `tests/integration/**`, `tests/simulation/**`
- On-disk data at `data/manifests/*.manifest.json`, `data/raw/**` (size samples), `data/normalized/**`, `data/derived/**`

No code was written. No branch was created. No file was edited except this plan file. No dependency was installed. No network call was made. No credential was referenced. **Plan is read-only except for this file.**

**End of Phase 2e Gate 1 Plan. Awaiting operator review.**
