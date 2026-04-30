# Phase 3q — 5m Data Acquisition and Integrity Validation

## Summary

Phase 3q acquired the four supplemental v001-of-5m dataset families specified by Phase 3p §4 (BTCUSDT 5m trade-price klines, ETHUSDT 5m trade-price klines, BTCUSDT 5m mark-price klines, ETHUSDT 5m mark-price klines) from public unauthenticated `data.binance.vision` monthly bulk archives, normalized them to Parquet under the existing repository partition convention (supplemental v001-of-5m alongside v002 — Phase 3p Option B), and ran the Phase 3p §4.7 / §6.2 integrity-check evidence specification on each dataset.

**Verdict — partial pass:**

- **BTCUSDT 5m trade-price klines** — `binance_usdm_btcusdt_5m__v001` — **research-eligible.** 446 688 bars; 0 gaps; all integrity checks PASS.
- **ETHUSDT 5m trade-price klines** — `binance_usdm_ethusdt_5m__v001` — **research-eligible.** 446 688 bars; 0 gaps; all integrity checks PASS.
- **BTCUSDT 5m mark-price klines** — `binance_usdm_btcusdt_markprice_5m__v001` — **NOT research-eligible** per Phase 3p §4.7 strict gate. 445 819 bars; 4 gaps; all other checks PASS.
- **ETHUSDT 5m mark-price klines** — `binance_usdm_ethusdt_markprice_5m__v001` — **NOT research-eligible** per Phase 3p §4.7 strict gate. 446 106 bars; 4 gaps; all other checks PASS.

The 4 mark-price gaps per symbol are upstream `data.binance.vision` bulk-archive characteristics: 1-day Binance maintenance windows on 2022-07-30/31, 2022-10-02, 2023-02-24, plus a 30-minute window on 2023-11-10 (BTC) — and equivalent windows on 2022-07-12, 2022-10-02, 2023-02-24, 2023-11-10 for ETH. **The same gaps exist in the locked v002 mark-price 15m datasets** (verified by running the same gap-detection logic on `data/normalized/mark_price_klines/symbol=BTCUSDT/interval=15m/...`); v002's manifest `invalid_windows: []` was inaccurate but was accepted at v002 lock time.

Phase 3q does NOT relax the Phase 3p §4.7 strict gate, does NOT silently patch the gaps, and does NOT mark mark-price datasets as research-eligible. The mark-price manifests record `research_eligible: false` and explicitly document the four gap windows in both `quality_checks.gap_locations` and a top-level `invalid_windows` field.

Per the brief's failure path, Phase 3q stops here for operator review. Trade-price datasets ARE locally research-eligible and could support Q1, Q3, Q5 (and the trade-price-side of Q2) immediately. Mark-price datasets are NOT eligible under the strict gate and would block Q6 (mark-vs-trade stop-trigger sensitivity) under current rules.

## Authority and boundary

**Authority:** Phase 3p §4 (data requirements), §5 (versioning approach: supplemental v001-of-5m alongside v002), §6 (manifest + integrity-check evidence); Phase 3o §4 (5m as diagnostics layer only, not strategy signal); Phase 3p §10 (decision menu Option B); `docs/04-data/dataset-versioning.md` (immutability + manifest policy); `docs/04-data/timestamp-policy.md` (UTC ms canonical); `docs/04-data/historical-data-spec.md` (Binance public bulk-archive convention); `docs/04-data/data-requirements.md` (forbidden-patterns: no forward-fill, no silent gap omission); `.claude/rules/prometheus-mcp-and-secrets.md` (no credentials, no MCP, no `.mcp.json`).

**Boundary preserved:** Phase 3q is docs-and-data only. R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks all preserved verbatim.

## Starting git state

```text
branch:           phase-3q/5m-data-acquisition-and-integrity-validation
created from:     main @ 9428b05044d57dbd3a1a5739a2b8b1db418dcade
v002 manifests:   8 files, untouched (Apr 19/20 timestamps)
v002 raw klines:  data/raw/binance_usdm/klines/symbol=*/interval=15m/...  untouched
v002 normalized:  data/normalized/klines/symbol=*/interval=15m/...        untouched
v002 markprice:   data/normalized/mark_price_klines/symbol=*/interval=15m/... untouched
existing scripts: data/derived/backtests/* untouched
```

Working tree was clean before Phase 3q. No code under `src/prometheus/` was modified.

## Data acquisition scope

| Family | Symbols | Date range (months) | Archives expected | Archives acquired |
|--------|---------|---------------------|-------------------|-------------------|
| `klines` (5m trade-price) | BTCUSDT, ETHUSDT | 2022-01 .. 2026-03 (51 months) | 102 | 102 |
| `markPriceKlines` (5m mark-price) | BTCUSDT, ETHUSDT | 2022-01 .. 2026-03 (51 months) | 102 | 102 |
| **Total** | | | **204** | **204** |

Each archive is a `data.binance.vision/data/futures/um/monthly/<family>/<SYMBOL>/5m/<SYMBOL>-5m-<YYYY>-<MM>.zip` file with paired `.CHECKSUM` containing `<sha256hex>  <filename>`. Every download was checksum-verified. No partial download was accepted.

Acquisition wall-clock: ~10 minutes for 204 archives at conservative pacing (100 ms inter-request + ~2.5 s per ZIP+checksum HTTP round-trip). Total raw ZIP footprint ≈ 63 MB; total normalized Parquet footprint ≈ 84 MB.

## Versioning decision

**Phase 3p Option B** (supplemental v001-of-5m alongside v002):

- Existing v002 datasets and manifests are **untouched**.
- No v003 family bump occurred.
- No existing v002 manifest was reissued.
- Four NEW dataset families were created at version `__v001`:
  - `binance_usdm_btcusdt_5m__v001`
  - `binance_usdm_ethusdt_5m__v001`
  - `binance_usdm_btcusdt_markprice_5m__v001`
  - `binance_usdm_ethusdt_markprice_5m__v001`
- Each manifest's `predecessor_dataset_versions` references the corresponding v002 dataset (e.g. `binance_usdm_btcusdt_5m__v001` → predecessor `binance_usdm_btcusdt_15m__v002`).
- v002 verdict provenance preserved exactly. R3 / R2 / F1 / D1-A trade populations remain dataset-version-attributed to v002.

## Source endpoints used

```text
GET https://data.binance.vision/data/futures/um/monthly/klines/<SYMBOL>/5m/<SYMBOL>-5m-<YYYY>-<MM>.zip
GET https://data.binance.vision/data/futures/um/monthly/klines/<SYMBOL>/5m/<SYMBOL>-5m-<YYYY>-<MM>.zip.CHECKSUM
GET https://data.binance.vision/data/futures/um/monthly/markPriceKlines/<SYMBOL>/5m/<SYMBOL>-5m-<YYYY>-<MM>.zip
GET https://data.binance.vision/data/futures/um/monthly/markPriceKlines/<SYMBOL>/5m/<SYMBOL>-5m-<YYYY>-<MM>.zip.CHECKSUM
```

All endpoints are public, unauthenticated. No credentials, no API keys, no signed requests, no private endpoints, no user stream, no WebSocket subscription, no exchange-write capability touched.

The Phase 3p §4.6 brief mentioned `GET /fapi/v1/klines` and `GET /fapi/v1/markPriceKlines` REST endpoints. Phase 3q used the **bulk-archive convention** (`data.binance.vision`) instead, consistent with the existing v002 datasets (Phase 2b / 2c) which were sourced from the same archive. The choice was made for three reasons: (a) it matches the existing repo convention exactly; (b) it provides authoritative monthly aggregations with paired SHA256 checksums; (c) Phase 3p §4.6's REST-endpoint mention is consistent with "any public unauthenticated source", which `data.binance.vision` satisfies. The historical-data-spec at `docs/04-data/historical-data-spec.md` (which this brief required as reading) is the existing canonical source convention.

## Date range determination

The Phase 3q brief required: "If the exact retained-evidence trade date range cannot be determined from existing repo artifacts, stop and write a Phase 3q blocker report instead of guessing or downloading an arbitrary broad range."

Date range was determined by reading every retained-evidence trade-log under `data/derived/backtests/**/trade_log.parquet` (154 files) and computing the global min / max across the union of `signal_bar_open_time_ms` and `exit_fill_time_ms` columns:

```text
Global min trade timestamp:  1641014100000  ->  2022-01-01 05:15:00 UTC
Global max trade timestamp:  1770879600000  ->  2026-02-12 07:00:00 UTC
```

Phase 3q acquired data covering **2022-01 through 2026-03** (51 monthly archives), which is a **strict superset** of the trade range in both directions:

```text
Acquired data first open_time ms: 1640995200000 (2022-01-01 00:00:00 UTC) <= 1641014100000  ✓
Acquired data last  open_time ms: 1775001300000 (2026-03-31 23:55:00 UTC) >= 1770879600000  ✓
```

The acquired range matches the v002 dataset range exactly (`2022-01 to 2026-03` per v002 manifest notes), preserving cross-dataset comparability.

## Dataset families created

| Dataset version | Bars | Date range start (UTC) | Date range end (UTC) | Eligible |
|---|---|---|---|---|
| `binance_usdm_btcusdt_5m__v001` | 446 688 | 2022-01-01 00:00:00 | 2026-03-31 23:55:00 | **YES** |
| `binance_usdm_ethusdt_5m__v001` | 446 688 | 2022-01-01 00:00:00 | 2026-03-31 23:55:00 | **YES** |
| `binance_usdm_btcusdt_markprice_5m__v001` | 445 819 | 2022-01-01 00:00:00 | 2026-03-31 23:55:00 | NO (4 gaps) |
| `binance_usdm_ethusdt_markprice_5m__v001` | 446 106 | 2022-01-01 00:00:00 | 2026-03-31 23:55:00 | NO (4 gaps) |

Expected bar count for the 51-month range (sum of `days_in_month × 288`):
- 2022 (365 days): 105 120
- 2023 (365 days): 105 120
- 2024 (366 days, leap): 105 408
- 2025 (365 days): 105 120
- 2026-01 (31 days): 8 928
- 2026-02 (28 days): 8 064
- 2026-03 (31 days): 8 928
- **Total: 446 688**

Trade-price 5m datasets match the expected count exactly (no gaps). Mark-price 5m datasets are 869 bars (BTC) / 582 bars (ETH) short, accounted for entirely by the four gap windows.

## File paths and sizes

```text
data/raw/binance_usdm/klines/symbol=BTCUSDT/interval=5m/year=YYYY/month=MM/BTCUSDT-5m-YYYY-MM.zip          (51 zips, 20 MB)
data/raw/binance_usdm/klines/symbol=ETHUSDT/interval=5m/year=YYYY/month=MM/ETHUSDT-5m-YYYY-MM.zip          (51 zips, 20 MB)
data/raw/binance_usdm/markPriceKlines/symbol=BTCUSDT/interval=5m/year=YYYY/month=MM/BTCUSDT-5m-YYYY-MM.zip (51 zips, 12 MB)
data/raw/binance_usdm/markPriceKlines/symbol=ETHUSDT/interval=5m/year=YYYY/month=MM/ETHUSDT-5m-YYYY-MM.zip (51 zips, 11 MB)

data/normalized/klines/symbol=BTCUSDT/interval=5m/year=YYYY/month=MM/part-0000.parquet          (51 files, 26 MB)
data/normalized/klines/symbol=ETHUSDT/interval=5m/year=YYYY/month=MM/part-0000.parquet          (51 files, 26 MB)
data/normalized/mark_price_klines/symbol=BTCUSDT/interval=5m/year=YYYY/month=MM/part-0000.parquet (51 files, 16 MB)
data/normalized/mark_price_klines/symbol=ETHUSDT/interval=5m/year=YYYY/month=MM/part-0000.parquet (51 files, 16 MB)

data/manifests/binance_usdm_btcusdt_5m__v001.manifest.json
data/manifests/binance_usdm_ethusdt_5m__v001.manifest.json
data/manifests/binance_usdm_btcusdt_markprice_5m__v001.manifest.json
data/manifests/binance_usdm_ethusdt_markprice_5m__v001.manifest.json
```

Total filesystem footprint added by Phase 3q: ≈ 147 MB. **All `data/` artifacts are git-ignored** by `/.gitignore` (the same convention applied to v002); they are local research evidence reproducible from the public `data.binance.vision` archive via `scripts/phase3q_5m_acquisition.py`.

Files committed to git by Phase 3q: this report + the orchestrator script + an optional minimal `current-project-state.md` update. Data is NOT committed per the brief's "Do not commit data/ artifacts" forbidden clause and per the `data/**` `.gitignore` rules.

## Manifest summary

Each new manifest contains the full Phase 3p §6.1 / §6.2 evidence:

```text
schema_version, dataset_category, dataset_name, dataset_version,
created_at_utc_ms, canonical_timezone (UTC), canonical_timestamp_format (unix_milliseconds),
symbols, intervals (["5m"]), sources (sorted list of 51 ZIP URLs),
pipeline_version (prometheus@0.0.0), partitioning, primary_key,
generator (scripts.phase3q_5m_acquisition),
predecessor_dataset_versions (-> v002),
invalid_windows (populated for mark-price; empty for trade-price),
notes (Phase 3p Option B framing),
date_range_start_open_time_utc_ms, date_range_end_open_time_utc_ms, bar_count,
quality_checks: {
  gaps_detected, gap_locations,
  monotone_timestamps, boundary_alignment_violations, close_time_consistency_violations,
  ohlc_sanity_violations, volume_sanity_violations,
  symbol_consistency_violations, interval_consistency_violations,
  date_range_coverage, coverage_required_first_open_time_ms, coverage_required_last_open_time_ms,
  research_eligible
}
```

## Integrity-check results

Per Phase 3p §4.7 / §6.2 specification:

| Check | BTC 5m klines | ETH 5m klines | BTC 5m markprice | ETH 5m markprice |
|---|---|---|---|---|
| `gaps_detected` | 0 | 0 | **4** | **4** |
| `monotone_timestamps` | true | true | true | true |
| `boundary_alignment_violations` (`open_time mod 300000 != 0`) | 0 | 0 | 0 | 0 |
| `close_time_consistency_violations` (`close_time != open_time + 299999`) | 0 | 0 | 0 | 0 |
| `ohlc_sanity_violations` | 0 | 0 | 0 | 0 |
| `volume_sanity_violations` | 0 | 0 | n/a (no volume) | n/a (no volume) |
| `symbol_consistency_violations` | 0 | 0 | 0 | 0 |
| `interval_consistency_violations` | 0 | 0 | 0 | 0 |
| `date_range_coverage` (≥ Phase 3p §4.3 strict superset) | true | true | true | true |
| **`research_eligible`** | **true** | **true** | **false** | **false** |

Mark-price gap windows (each gap reported as `prev_open_time_ms` → `next_open_time_ms`):

**BTCUSDT mark-price 5m:**

```text
1445 min  2022-07-30T23:55:00 UTC  ->  2022-08-01T00:00:00 UTC
1445 min  2022-10-01T23:55:00 UTC  ->  2022-10-03T00:00:00 UTC
1445 min  2023-02-23T23:55:00 UTC  ->  2023-02-25T00:00:00 UTC
  30 min  2023-11-10T03:35:00 UTC  ->  2023-11-10T04:05:00 UTC
```

**ETHUSDT mark-price 5m:**

```text
  10 min  2022-07-12T13:10:00 UTC  ->  2022-07-12T13:20:00 UTC
1445 min  2022-10-01T23:55:00 UTC  ->  2022-10-03T00:00:00 UTC
1445 min  2023-02-23T23:55:00 UTC  ->  2023-02-25T00:00:00 UTC
  30 min  2023-11-10T03:35:00 UTC  ->  2023-11-10T04:05:00 UTC
```

These windows are recorded verbatim in the manifest `invalid_windows` field and `quality_checks.gap_locations`. **No forward-fill, interpolation, or silent omission was applied.** No data was patched.

## Research eligibility verdict

- **Trade-price datasets (`__klines`):** PASS Phase 3p §4.7 strict gate. `research_eligible: true`.
- **Mark-price datasets (`__markprice`):** FAIL Phase 3p §4.7 strict gate (gaps_detected ≠ 0). `research_eligible: false`.

Per the brief: *"If any required check fails, the dataset is not research-eligible. Do not run diagnostics anyway. Do not relax requirements. Do not silently patch or forward-fill data. Write a failure report and stop."*

Phase 3q is therefore stopping for operator review.

## v002 precedent

For full transparency: the **same four gap windows exist in the locked v002 mark-price 15m datasets** (`binance_usdm_btcusdt_markprice_15m__v002`, `binance_usdm_ethusdt_markprice_15m__v002`). Verified by running equivalent gap-detection logic against `data/normalized/mark_price_klines/symbol=BTCUSDT/interval=15m/...`:

```text
v002 BTC markprice 15m bars=148607 gaps=4
  1455 min: 2022-07-30T23:45:00 UTC -> 2022-08-01T00:00:00 UTC
  1455 min: 2022-10-01T23:45:00 UTC -> 2022-10-03T00:00:00 UTC
  1455 min: 2023-02-23T23:45:00 UTC -> 2023-02-25T00:00:00 UTC
    30 min: 2023-11-10T03:30:00 UTC -> 2023-11-10T04:00:00 UTC
```

The v002 mark-price 15m manifest's `invalid_windows: []` is technically inaccurate (it does not record these four gaps) but the v002 dataset has been used in all retained-evidence backtests (Phase 2e through Phase 3j) without operator-flagged issue. The retained-evidence verdict population produced under v002 was accepted with these gaps present in the underlying mark-price data.

This is reported transparently and **does not by itself revise the v002 verdicts or relax Phase 3p §4.7 for Phase 3q.** The v002 verdicts remain locked. The Phase 3q strict gate verdict for mark-price is FAIL until the operator either (a) explicitly authorizes alternative gap-handling rules for diagnostics-only mark-price work, or (b) decides not to proceed with Q6 (mark-vs-trade stop-trigger sensitivity) at all.

## What Phase 3q does not authorize

Phase 3q does NOT authorize, propose, or initiate any of the following:

- **5m diagnostics execution.** Q1–Q7 are not answered. No diagnostic table, plot, or computation produced. Phase 3o §10 / Phase 3p §7 outputs are not generated.
- **5m strategy.** No 5m strategy family. No 5m variant of V1, R2, F1, or D1-A. No hybrid spec.
- **5m diagnostics-execution plan.** Phase 3p §10 Option C is not started.
- **Strategy changes.** R3 / R2 / F1 / D1-A specs preserved verbatim.
- **Parameter changes.** Locked sub-parameters preserved verbatim.
- **Threshold optimization.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 preserved verbatim.
- **Backtests.** No backtest run. No control rerun. No fold scoring, walk-forward analysis, cost-sensitivity sweep, mechanism-check rerun, or aggregate-metric computation.
- **v002 modification.** v002 datasets and manifests untouched.
- **v003 creation.** No v003 family bump.
- **Implementation.** No runtime / strategy / execution / risk / persistence / dashboard / observability code changed. The Phase 3q orchestrator script is research-data-only; it does not implement strategy, runtime, or execution behavior.
- **Paper/shadow planning.** Not authorized.
- **Phase 4 work.** No runtime / state / persistence / risk-runtime work.
- **Live-readiness work.** Not authorized.
- **Deployment work.** Not authorized.
- **Production-key creation.** No production keys requested, generated, stored, or referenced.
- **Exchange-write capability.** No exchange-write paths exist or were touched.
- **MCP enablement.** No MCP servers added, configured, or used.
- **Graphify / `.mcp.json`.** Not enabled.
- **Credentials.** None requested. None used. None stored. None referenced.

## Forbidden-work confirmation

- **No Q1–Q7 diagnostics.** Confirmed; no Phase 3o / 3p question answered.
- **No diagnostic tables, plots, or classifications.** Confirmed.
- **No backtests.** Confirmed; no H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A run.
- **No v002 trade population modification.** Confirmed; trade lists untouched.
- **No v002 dataset / manifest modification.** Confirmed; v002 manifests and partitions untouched (filesystem timestamps unchanged).
- **No v003.** Confirmed.
- **No strategy / threshold / parameter / project-lock modifications.** Confirmed; §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / §1.7.3 preserved verbatim.
- **No prior-verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A verdicts unchanged.
- **No 5m strategy / hybrid creation.** Confirmed.
- **No paper/shadow / Phase 4 / live-readiness / deployment / production keys / credentials / authenticated APIs / MCP / Graphify / `.mcp.json` / exchange-write touched.** Confirmed.
- **No private Binance endpoints / user stream / WebSocket.** Confirmed; only public unauthenticated bulk archive endpoints.
- **No secrets stored or requested.** Confirmed.
- **No `data/` artifact committed.** Confirmed; per repository `.gitignore` convention all `data/raw/**`, `data/normalized/**`, `data/derived/**`, `data/manifests/**` files are git-ignored. Phase 3q's commits include only the orchestrator script under `scripts/` and this Phase 3q report under `docs/`. The acquired data and manifests are local filesystem evidence reproducible from public sources.

## Remaining boundary

- **Branch:** `phase-3q/5m-data-acquisition-and-integrity-validation`. Not merged to main.
- **main:** unchanged at `9428b05044d57dbd3a1a5739a2b8b1db418dcade`.
- **Recommended state:** **paused.**
- **5m research thread:** Phase 3o predeclared Q1–Q7 + forbidden forms + diagnostic terms + analysis boundary; Phase 3p added data-requirements + dataset-versioning approach + manifest specification + per-question outputs + outcome-interpretation rules; Phase 3q has now physically acquired the data and run integrity checks. Trade-price datasets are research-eligible. Mark-price datasets are NOT research-eligible under the strict gate.
- **Project locks preserved:** R3 baseline-of-record; H0 framework anchor; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks preserved verbatim.
- **Operator decision required** before any successor phase. Phase 3q stops here for review.

## Operator decision menu

The operator now has Phase 3q's evidence: 2 of 4 datasets pass; 2 of 4 fail Phase 3p §4.7 strict gap-zero gate due to upstream Binance maintenance-window characteristics that also exist in v002 mark-price 15m. The next operator decision is operator-driven only.

### Option A — Remain paused, accept Phase 3q partial-pass evidence (PRIMARY recommendation)

Take no further action. Phase 3q acquisition and integrity-check evidence is recorded. The 4 dataset manifests are committed to local filesystem. Trade-price 5m data is research-eligible; mark-price 5m data is NOT research-eligible under the strict gate. No diagnostics are run. No successor phase authorized.

**Reasoning:**
- The Phase 3q acquisition + integrity-check value is realized: the project now has on-disk evidence of exactly which 5m data exists and exactly which integrity property holds for each family.
- The mark-price 5m gap finding is a genuine evidence pattern (and a v002-precedent pattern that was not previously surfaced).
- Selecting Option A preserves all locks; preserves the Phase 3o / 3p predeclaration discipline; produces no diagnostic output; does not revise any v002 verdict; does not relax §4.7.
- Five docs-only / docs-and-data phases on the 5m thread (3k / 3l / 3m / 3n / 3o / 3p / 3q) have now produced complete predeclaration + acquisition. Whether to *act on* the acquisition is a separate operator-strategic decision.

### Option B — Authorize a future Phase 3q-followup memo to formally document the mark-price gap-handling decision (CONDITIONAL secondary alternative)

Authorize a docs-only memo that formally proposes one of:
1. Treating the four mark-price gap windows as known invalid windows (similar to how v002 implicitly did), and updating Phase 3p §4.7 to allow `research_eligible: true` if `invalid_windows` is fully documented and gaps fall outside trade-population coverage windows.
2. Excluding any retained-evidence trade whose holding period intersects an `invalid_window` from any future Q6 mark-vs-trade analysis.
3. Ruling out Q6 entirely, retaining the four other Q1 / Q2 / Q3 / Q5 / Q7 questions for a possible future diagnostics-execution phase.

**Reasoning if selected:** Option B is a docs-only governance decision about how to handle a real upstream-data characteristic. It does NOT relax §4.7 silently; it forces the operator to make an explicit, documented governance choice. It does NOT authorize Q1–Q7 execution.

**Pre-conditions if selected:** Operator commits ex-ante to anti-circular-reasoning discipline. Operator commits that the followup memo cannot itself authorize diagnostics execution.

### Option C — Authorize 5m diagnostics-execution phase (Phase 3p §10 Option C) (CONDITIONAL tertiary alternative)

Authorize a future docs-only phase that runs Q1, Q2, Q3, Q5 (which depend only on trade-price 5m data and v002 funding events) and either skips Q6 or runs it with explicit gap exclusion.

**Reasoning if selected:** This is the operational endpoint of the 5m research thread for trade-price-only diagnostics. It produces the actual answers to Q1, Q2, Q3, Q5, Q7 under the predeclared rules.

**Pre-conditions if selected:** Same as Phase 3p §10 Option C plus: explicit decision about Q6 (skip or gap-excluded). All Phase 3o §6 forbidden question forms remain forbidden. All Phase 3p §8 outcome-interpretation rules remain immutable.

### Option D — Reject Phase 3q on integrity grounds and seek alternative mark-price data source (NOT RECOMMENDED)

The brief's strict reading would mandate rejecting Phase 3q for the mark-price-data failure. However, the gap windows are upstream Binance maintenance characteristics that propagate through ANY data.binance.vision archive (and likely through `GET /fapi/v1/markPriceKlines` REST as well — Binance simply did not publish mark-price data during those maintenance windows). No alternative source is known to fill these gaps. Option D would effectively rule out Q6 indefinitely.

### Option E — Strategy rescue / new strategy / regime-first / ML / paper-shadow / Phase 4 / live-readiness / deployment (NOT RECOMMENDED)

Strongly not recommended. Phase 3q's acquisition does not change the post-Phase-3p strategic boundary.

### Recommendation

**Phase 3q recommends Option A (remain paused) as primary,** with Option B (docs-only governance memo) as the most natural conditional secondary if the operator wishes to formally close out the mark-price gap-handling question before any potential diagnostics-execution phase. Option C is acceptable only after an explicit Q6 disposition decision.

Phase 3q does NOT merge to main. Phase 3q stops here. The operator decides what (if anything) follows.
