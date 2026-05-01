# Phase 4i — V2 Public Data Acquisition and Integrity Validation

## Summary

Phase 4i acquired the six Phase 4h-predeclared minimum dataset
families for V2's first-backtest data plan from public unauthenticated
`data.binance.vision` bulk archives, normalized them to Parquet under
the existing repository partition convention, and ran the Phase 4h §17
strict integrity-check evidence specification on each dataset.

**Verdict — partial pass:**

- **BTCUSDT 30m trade-price klines** — `binance_usdm_btcusdt_30m__v001` —
  **research-eligible.** 74 448 bars; 0 gaps; all integrity checks PASS.
- **ETHUSDT 30m trade-price klines** — `binance_usdm_ethusdt_30m__v001` —
  **research-eligible.** 74 448 bars; 0 gaps; all integrity checks PASS.
- **BTCUSDT 4h trade-price klines** — `binance_usdm_btcusdt_4h__v001` —
  **research-eligible.** 9 306 bars; 0 gaps; all integrity checks PASS.
- **ETHUSDT 4h trade-price klines** — `binance_usdm_ethusdt_4h__v001` —
  **research-eligible.** 9 306 bars; 0 gaps; all integrity checks PASS.
- **BTCUSDT metrics** — `binance_usdm_btcusdt_metrics__v001` —
  **NOT research-eligible** under Phase 4h §17.4 strict gate. 446 555 of
  446 688 expected 5-minute records (133 short); 5 699 intra-day missing
  observations across the 4-year coverage; 0 missing daily archives;
  91 840 records have ≥ 1 NaN in optional ratio columns concentrated in
  early-2022 data.
- **ETHUSDT metrics** — `binance_usdm_ethusdt_metrics__v001` —
  **NOT research-eligible** under Phase 4h §17.4 strict gate. 446 555 of
  446 688 expected records; 3 631 intra-day missing observations;
  0 missing daily archives; 91 841 records have ≥ 1 NaN in optional
  ratio columns concentrated in early-2022 data.

The 4 trade-price kline datasets PASS strictly. The 2 metrics datasets
FAIL the strict gate due to upstream `data.binance.vision` characteristics:
(a) ~133 missing 5-minute observations per symbol (~0.03% of the 4-year
record count) concentrated in known Binance maintenance / pipeline
windows; (b) extensive NaN values in **optional** ratio columns
(count/sum_toptrader_long_short_ratio, count_long_short_ratio,
sum_taker_long_short_vol_ratio) for early-2022 data, with 0 NaN in the
required `sum_open_interest` and `sum_open_interest_value` columns.

Phase 4i does NOT relax the Phase 4h §17.4 strict gate, does NOT silently
patch the gaps, and does NOT mark the metrics datasets as research-eligible.
The metrics manifests record `research_eligible: false`, list the
detected gap windows verbatim in `quality_checks.gap_locations`, and
populate `invalid_windows` for every missing 5-minute observation
(capped at 200 entries per Phase 3q-style reporting precedent).

Per the brief's failure path, Phase 4i **stops here for operator review**.
Trade-price kline datasets ARE locally research-eligible and could
support V2 entry features 1, 2, 3, 4, 5, 6, and 7 (per Phase 4h §27)
immediately. Metrics datasets are NOT eligible under the strict gate
and would block V2 entry feature 8 OI sub-component under current rules.

**Verification (run on the post-Phase-4h-merge tree, captured by Phase 4i):**

- `ruff check .`: **All checks passed!** (whole-repo Ruff quality gate
  fully clean).
- `pytest`: **785 passed in 12.75s.** No regressions.
- `mypy` strict: **Success: no issues found in 82 source files.**

**No retained-evidence verdict revised.** R3 / H0 / R1a / R1b-narrow /
R2 / F1 / D1-A all preserved verbatim. **No project locks changed.**
**No mark-price 30m / 4h acquired.** **No aggTrades acquired.** **No
funding-rate re-acquired** (v002 funding manifests reused per Phase 4h §22).
**No backtest run. No diagnostics run. No V2 implementation. No V2
validation. No paper / shadow / live / exchange-write authorization.**
**Recommended state remains paused.** **No successor phase has been
authorized.**

## Authority and boundary

**Authority:** Phase 4h §6–§17 (data-requirements + integrity-check
predeclaration); Phase 4g (V2 strategy spec); Phase 4f §22 (V2
hypothesis); Phase 3q (precedent for public-bulk-archive acquisition
pattern); Phase 3r §8 (mark-price gap governance — referenced for
analogous metrics gap handling); Phase 3p §4.7 / §6.2 (strict
integrity-gate semantics);
`docs/04-data/dataset-versioning.md` (immutability + manifest policy);
`docs/04-data/timestamp-policy.md` (UTC ms canonical);
`docs/04-data/historical-data-spec.md` (Binance public bulk-archive
convention); `docs/04-data/data-requirements.md` (forbidden patterns:
no forward-fill, no silent gap omission);
`.claude/rules/prometheus-mcp-and-secrets.md` (no credentials, no
MCP, no `.mcp.json`).

**Boundary preserved:** Phase 4i is docs-and-data only. R3
baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 /
D1-A retained research evidence only; R2 FAILED — §11.6
cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS /
FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3
project-level locks all preserved verbatim. Phase 3v § 8
stop-trigger-domain governance, Phase 3w §6 / §7 / §8 break-even / EMA
slope / stagnation governance, Phase 3r §8 mark-price gap governance,
Phase 4f V2 hypothesis, and Phase 4g V2 strategy spec all preserved
verbatim.

## Starting state

```text
branch:           phase-4i/v2-public-data-acquisition-and-integrity-validation
created from:     main @ 4a0edf980c01a1c3c9336ad89dd142685a53a445
v002 manifests:   8 files, untouched
v001-of-5m:       4 files, untouched
v002 raw:         data/raw/binance_usdm/klines/symbol=*/interval=15m/...   untouched
v002 normalized:  data/normalized/klines/symbol=*/interval=15m/...         untouched
v002 markprice:   data/normalized/mark_price_klines/symbol=*/interval=15m/... untouched
v001-of-5m raw:   data/raw/binance_usdm/<klines|markPriceKlines>/symbol=*/interval=5m/... untouched
existing scripts: scripts/phase3q_5m_acquisition.py + scripts/phase3s_5m_diagnostics.py untouched
```

Working tree was clean before Phase 4i. No code under `src/prometheus/`
was modified.

## Relationship to Phase 4g / Phase 4h

Phase 4g locked the V2 strategy spec: signal 30m, bias 4h, session /
volume bucket 1h, 8 entry features + 3 exit / regime features,
512-variant threshold grid, M1 / M2 / M3 mechanism-check decomposition,
four governance labels.

Phase 4h translated those choices into a data plan: required dataset
families; public-source availability; dataset-versioning convention;
directory layout; manifest schema; per-family integrity-check rules;
strict `research_eligible` rules; invalid-window handling; alignment /
timestamp policy; future Phase 4i acquisition execution plan preview.

Phase 4i implements Phase 4h's acquisition execution plan preview,
acquiring exactly the six families predeclared by Phase 4h §9 as the
"minimum acquisition set for V2 first backtest" — 30m klines × 2,
4h klines × 2, `metrics` × 2 — and running exactly the integrity
checks predeclared by Phase 4h §17.

Phase 4i does NOT modify Phase 4g or Phase 4h text. Phase 4i does NOT
re-optimize the V2 strategy spec.

## Acquisition scope

Phase 4i acquired only the six Phase 4h §9 minimum dataset families
for the date range 2022-01-01 through 2026-03-31 UTC:

| Family | Symbol | Interval | Source pattern | Archives expected | Archives acquired |
|---|---|---|---|---|---|
| `klines` (30m trade-price) | BTCUSDT | 30m | `data.binance.vision/data/futures/um/monthly/klines/BTCUSDT/30m/<file>.zip` | 51 monthly | 51 |
| `klines` (30m trade-price) | ETHUSDT | 30m | `.../ETHUSDT/30m/<file>.zip` | 51 monthly | 51 |
| `klines` (4h trade-price) | BTCUSDT | 4h | `.../BTCUSDT/4h/<file>.zip` | 51 monthly | 51 |
| `klines` (4h trade-price) | ETHUSDT | 4h | `.../ETHUSDT/4h/<file>.zip` | 51 monthly | 51 |
| `metrics` (5-min OI / taker / long-short ratios) | BTCUSDT | 5m records inside daily archive | `data.binance.vision/data/futures/um/daily/metrics/BTCUSDT/<file>.zip` | 1551 daily (2022-01-01 .. 2026-03-31) | 1551 |
| `metrics` (5-min OI / taker / long-short ratios) | ETHUSDT | 5m records inside daily archive | `.../ETHUSDT/<file>.zip` | 1551 daily | 1551 |
| **Total** | | | | **3306** | **3306** |

Each archive was acquired with paired `.CHECKSUM` SHA256 verification.
Every download was checksum-verified. No partial download was accepted.
No archive was missing.

Acquisition wall-clock: ~11 minutes for 3306 archives at 8 parallel
workers + 50 ms inter-request pacing per worker. Total raw ZIP
footprint ≈ 49 MB; total normalized Parquet footprint ≈ 56 MB.

## Explicitly excluded scope

Phase 4i did **NOT** acquire any of the following per the brief:

- **Mark-price 30m / 4h klines.** DEFERRED to a future
  `mark_price_backtest_candidate` validation pass per Phase 4h §20.
  No mark-price archives downloaded.
- **`aggTrades` (tick-level).** OPTIONAL / DEFERRED per Phase 4h §7.E.
  klines `taker_buy_volume` column is sufficient for V2's predeclared
  taker-imbalance feature. No aggTrades archives downloaded.
- **Funding-rate.** Reuses existing v002 funding manifests
  (`binance_usdm_btcusdt_funding__v002` and
  `binance_usdm_ethusdt_funding__v002`) per Phase 4h §22. No funding
  re-acquisition.
- **Spot data.** v1 is perpetual only. No spot archive consulted.
- **Cross-venue data.** Single-venue (Binance USDⓈ-M) per §1.7.3.
- **Authenticated REST / WebSocket / user-stream / listenKey lifecycle /
  order-book L2 depth.** All forbidden by the brief and by
  `.claude/rules/prometheus-safety.md`.

## Source URLs and archive inventory

The exact URL patterns used:

```text
GET https://data.binance.vision/data/futures/um/monthly/klines/<SYMBOL>/<INTERVAL>/<SYMBOL>-<INTERVAL>-<YYYY>-<MM>.zip
GET https://data.binance.vision/data/futures/um/monthly/klines/<SYMBOL>/<INTERVAL>/<SYMBOL>-<INTERVAL>-<YYYY>-<MM>.zip.CHECKSUM
GET https://data.binance.vision/data/futures/um/daily/metrics/<SYMBOL>/<SYMBOL>-metrics-<YYYY>-<MM>-<DD>.zip
GET https://data.binance.vision/data/futures/um/daily/metrics/<SYMBOL>/<SYMBOL>-metrics-<YYYY>-<MM>-<DD>.zip.CHECKSUM
```

All endpoints are public, unauthenticated. No credentials, no API
keys, no signed requests, no private endpoints, no user stream, no
WebSocket subscription, no exchange-write capability touched.

The full per-archive URL list with paired SHA256 hashes is recorded
in each manifest's `sources` array and `raw_sha256_index` map.

## Dataset families acquired

| Dataset version | Symbol | Family | Records / Bars | First UTC | Last UTC | Eligible |
|---|---|---|---|---|---|---|
| `binance_usdm_btcusdt_30m__v001` | BTCUSDT | klines 30m | 74 448 bars | 2022-01-01 00:00:00 | 2026-03-31 23:30:00 | **YES** |
| `binance_usdm_ethusdt_30m__v001` | ETHUSDT | klines 30m | 74 448 bars | 2022-01-01 00:00:00 | 2026-03-31 23:30:00 | **YES** |
| `binance_usdm_btcusdt_4h__v001` | BTCUSDT | klines 4h | 9 306 bars | 2022-01-01 00:00:00 | 2026-03-31 20:00:00 | **YES** |
| `binance_usdm_ethusdt_4h__v001` | ETHUSDT | klines 4h | 9 306 bars | 2022-01-01 00:00:00 | 2026-03-31 20:00:00 | **YES** |
| `binance_usdm_btcusdt_metrics__v001` | BTCUSDT | metrics 5m | 446 555 / 446 688 records | 2022-01-01 00:00:00 | 2026-03-31 23:55:00 | NO (5 699 missing 5m obs + 91 840 NaN rows in optional ratio fields) |
| `binance_usdm_ethusdt_metrics__v001` | ETHUSDT | metrics 5m | 446 555 / 446 688 records | 2022-01-01 00:00:00 | 2026-03-31 23:55:00 | NO (3 631 missing 5m obs + 91 841 NaN rows in optional ratio fields) |

Expected bar count (klines):

- 30m: 51 months × varying days × 48 = 74 448 bars (no gaps).
- 4h: 51 months × varying days × 6 = 9 306 bars (no gaps).

Expected record count (metrics):

- 5m: 1551 days × 288 = 446 688 records.
- BTCUSDT actual: 446 555 (133 short).
- ETHUSDT actual: 446 555 (133 short).

The 133-record shortfall per symbol corresponds to ~0.03% of the
4-year coverage and is concentrated in documented Binance maintenance /
data-pipeline windows (largest single window: 2024-02-16 13:30 UTC →
2024-02-17 00:00 UTC, ~10.5 hours).

## Local data artefacts created

```text
data/raw/binance_usdm/klines/symbol=BTCUSDT/interval=30m/year=YYYY/month=MM/...    (51 zips, ~3.7 MB)
data/raw/binance_usdm/klines/symbol=ETHUSDT/interval=30m/year=YYYY/month=MM/...    (51 zips, ~3.8 MB)
data/raw/binance_usdm/klines/symbol=BTCUSDT/interval=4h/year=YYYY/month=MM/...     (51 zips, ~636 KB)
data/raw/binance_usdm/klines/symbol=ETHUSDT/interval=4h/year=YYYY/month=MM/...     (51 zips, ~636 KB)
data/raw/binance_usdm/metrics/symbol=BTCUSDT/year=YYYY/month=MM/...                (1551 zips, ~20 MB)
data/raw/binance_usdm/metrics/symbol=ETHUSDT/year=YYYY/month=MM/...                (1551 zips, ~20 MB)

data/normalized/klines/symbol=BTCUSDT/interval=30m/year=YYYY/month=MM/part-0000.parquet  (51 files, ~4.7 MB)
data/normalized/klines/symbol=ETHUSDT/interval=30m/year=YYYY/month=MM/part-0000.parquet  (51 files, ~4.7 MB)
data/normalized/klines/symbol=BTCUSDT/interval=4h/year=YYYY/month=MM/part-0000.parquet   (51 files, ~1.0 MB)
data/normalized/klines/symbol=ETHUSDT/interval=4h/year=YYYY/month=MM/part-0000.parquet   (51 files, ~1.1 MB)
data/normalized/metrics/symbol=BTCUSDT/granularity=5m/year=YYYY/month=MM/part-0000.parquet  (51 files, ~22 MB)
data/normalized/metrics/symbol=ETHUSDT/granularity=5m/year=YYYY/month=MM/part-0000.parquet  (51 files, ~23 MB)

Total raw footprint:        ~49 MB
Total normalized footprint: ~56 MB
Total Phase 4i local data:  ~105 MB
```

**All `data/raw/**` and `data/normalized/**` artefacts are git-ignored**
per `.gitignore`. They are local research evidence reproducible from
the public `data.binance.vision` archive via
`scripts/phase4i_v2_acquisition.py`.

## Manifest files created

Six new manifests under `data/manifests/`:

```text
data/manifests/binance_usdm_btcusdt_30m__v001.manifest.json
data/manifests/binance_usdm_ethusdt_30m__v001.manifest.json
data/manifests/binance_usdm_btcusdt_4h__v001.manifest.json
data/manifests/binance_usdm_ethusdt_4h__v001.manifest.json
data/manifests/binance_usdm_btcusdt_metrics__v001.manifest.json
data/manifests/binance_usdm_ethusdt_metrics__v001.manifest.json
```

Each manifest contains the full Phase 4h §16 evidence schema:

```text
schema_version, dataset_category, dataset_name, dataset_version,
created_at_utc_ms, canonical_timezone (UTC), canonical_timestamp_format
(unix_milliseconds), symbols, market (binance_usdm), instrument_type
(perpetual_futures), intervals (or granularity for metrics), sources
(sorted list of bulk-archive URLs), pipeline_version (prometheus@0.0.0),
partitioning, primary_key, generator (scripts.phase4i_v2_acquisition),
predecessor_dataset_versions, raw_archive_count, raw_sha256_index,
invalid_windows, notes, date_range_start_*_utc_ms,
date_range_end_*_utc_ms, bar_count or record_count, expected_records
(metrics only), quality_checks (per family), research_eligible,
command_used, no_credentials_confirmation: true,
private_endpoint_used: false.
```

`predecessor_dataset_versions`:

- `binance_usdm_btcusdt_30m__v001` → `binance_usdm_btcusdt_15m__v002`.
- `binance_usdm_ethusdt_30m__v001` → `binance_usdm_ethusdt_15m__v002`.
- `binance_usdm_btcusdt_4h__v001` → `binance_usdm_btcusdt_1h_derived__v002`.
- `binance_usdm_ethusdt_4h__v001` → `binance_usdm_ethusdt_1h_derived__v002`.
- `binance_usdm_btcusdt_metrics__v001` → `[]` (no predecessor; new
  family).
- `binance_usdm_ethusdt_metrics__v001` → `[]` (no predecessor; new
  family).

Existing v002 manifests and v001-of-5m manifests are NOT modified.

## Normalization method

**Klines (30m, 4h):**

Each monthly raw ZIP is parsed line-by-line as a 12-column CSV
(Binance bulk format: `open_time, open, high, low, close, volume,
close_time, quote_asset_volume, count, taker_buy_volume,
taker_buy_quote_asset_volume, ignore`). Header rows are detected
(case-insensitive match on `open_time`) and skipped. Numeric columns
are parsed as `int64` for `open_time`, `close_time`, `count`, and
`float64` for the eight float columns. Each row is augmented with
`symbol`, `interval`, and `source` (the source URL).

Per-month rows are written to a single Parquet partition under
`data/normalized/klines/symbol=<SYMBOL>/interval=<INTERVAL>/year=YYYY/month=MM/part-0000.parquet`
with zstd compression level 3. Schema is `kline_v1` (15 fields).

**Metrics:**

Each daily raw ZIP is parsed line-by-line as an 8-column CSV
(`create_time, symbol, sum_open_interest, sum_open_interest_value,
count_toptrader_long_short_ratio, sum_toptrader_long_short_ratio,
count_long_short_ratio, sum_taker_long_short_vol_ratio`). Header rows
are detected (case-insensitive match on `create_time`) and skipped.

`create_time` accepts either integer milliseconds OR ISO-like
`YYYY-MM-DD HH:MM:SS` strings (Binance has emitted both formats over
the years; both are normalized to UTC ms).

Empty / quoted-empty (`""`) numeric values are parsed as `NaN`. The
script does NOT silently substitute zero, forward-fill, or omit rows
with NaN values. Records with NaN values are preserved as-is and the
integrity check counts them via `nonfinite_violations`. Per Phase 4h
§17.4 / §18.1, this fails `research_eligible` for the metrics dataset
without silently patching.

Per-day rows are concatenated into per-month Parquet partitions under
`data/normalized/metrics/symbol=<SYMBOL>/granularity=5m/year=YYYY/month=MM/part-0000.parquet`
(one Parquet file per calendar month, sorted by `create_time`). Schema
is `metrics_v1` (9 fields).

## Integrity-check methodology

Per Phase 4h §17 specification (= Phase 3p §6.2 plus Phase 4h-specific
extensions):

**Klines** (per dataset, computed by reading concatenated month
Parquet partitions in chronological order):

1. `monotone_timestamps`: every consecutive `(open_time[i-1], open_time[i])`
   pair satisfies strict less-than.
2. `duplicate_timestamps`: count of pairs with `open_time[i-1] == open_time[i]`.
3. `boundary_alignment_violations`: count of `open_time` not aligned
   to interval boundary (`open_time mod (interval_ms) != 0`).
4. `close_time_consistency_violations`: count where
   `close_time != open_time + interval_ms - 1`.
5. `gaps_detected`: count of `(open_time[i] - open_time[i-1]) != interval_ms`
   for `i > 0` (with monotone increase).
6. `gap_locations`: list of `{prev_open_time_ms, next_open_time_ms}`
   pairs (capped at 50).
7. `ohlc_sanity_violations`: count where any of `low, open, close,
   high <= 0` OR `low > open` OR `low > close` OR `high < open` OR
   `high < close`.
8. `volume_sanity_violations`: count where `volume < 0` OR
   `quote_asset_volume < 0` OR `count < 0`.
9. `taker_buy_volume_present`: boolean — every row has non-null
   `taker_buy_volume` column.
10. `taker_buy_volume_violations`: count where `taker_buy_volume < 0`
    OR `taker_buy_volume > volume` (within float tolerance).
11. `symbol_consistency_violations`: count where row symbol differs
    from expected.
12. `interval_consistency_violations`: count where row interval differs
    from expected.
13. `date_range_coverage`: boolean — `min(open_time) <=
    1640995200000` (2022-01-01 00:00 UTC) AND `max(open_time) >=
    coverage-required last open` (per interval: 30m → 1774999800000;
    4h → 1774987200000).

A kline dataset is `research_eligible` only if ALL 13 checks pass.

**Metrics** (per dataset, computed by reading concatenated month
Parquet partitions in chronological order):

1. `monotone_timestamps`: as above on `create_time`.
2. `duplicate_timestamps`: as above.
3. `boundary_alignment_violations`: count of `create_time mod 300000 != 0`.
4. `missing_observations`: count of `(create_time[i] - create_time[i-1]) > 300000`.
5. `gap_locations`: capped list of gap intervals.
6. `missing_days`: list of daily archives that returned 404 from
   `data.binance.vision`.
7. `symbol_consistency_violations`.
8. `nonfinite_violations`: count of rows where ANY of the six numeric
   columns (`sum_open_interest`, `sum_open_interest_value`,
   `count_toptrader_long_short_ratio`, `sum_toptrader_long_short_ratio`,
   `count_long_short_ratio`, `sum_taker_long_short_vol_ratio`) is
   NaN or ±Inf.
9. `nonnegative_oi_violations`: count where `sum_open_interest < 0`
   OR `sum_open_interest_value < 0`.
10. `nonnegative_ratio_violations`: count where any of the four ratio
    columns is `< 0`.
11. `date_range_coverage`: boolean — `min(create_time) <=
    1640995200000` (2022-01-01 00:00 UTC) AND `max(create_time) >=
    1775001300000` (2026-03-31 23:55 UTC) AND `missing_days` is
    empty.

A metrics dataset is `research_eligible` only if ALL 11 checks pass.

## Kline integrity results

| Check | BTC 30m | ETH 30m | BTC 4h | ETH 4h |
|---|---|---|---|---|
| `bar_count` | 74 448 | 74 448 | 9 306 | 9 306 |
| `monotone_timestamps` | true | true | true | true |
| `duplicate_timestamps` | 0 | 0 | 0 | 0 |
| `boundary_alignment_violations` | 0 | 0 | 0 | 0 |
| `close_time_consistency_violations` | 0 | 0 | 0 | 0 |
| `gaps_detected` | 0 | 0 | 0 | 0 |
| `ohlc_sanity_violations` | 0 | 0 | 0 | 0 |
| `volume_sanity_violations` | 0 | 0 | 0 | 0 |
| `taker_buy_volume_present` | true | true | true | true |
| `taker_buy_volume_violations` | 0 | 0 | 0 | 0 |
| `symbol_consistency_violations` | 0 | 0 | 0 | 0 |
| `interval_consistency_violations` | 0 | 0 | 0 | 0 |
| `date_range_coverage` | true | true | true | true |
| **`research_eligible`** | **true** | **true** | **true** | **true** |

All four kline datasets PASS Phase 4h §17.1 strict gate. **No gaps.
No anomalies. Full coverage.**

## Metrics integrity results

| Check | BTC metrics | ETH metrics |
|---|---|---|
| `record_count` | 446 555 | 446 555 |
| `expected_records` | 446 688 | 446 688 |
| `monotone_timestamps` | true | true |
| `duplicate_timestamps` | 0 | 0 |
| `boundary_alignment_violations` | 0 | 0 |
| `missing_observations` | **5 699** | **3 631** |
| `missing_days` | 0 | 0 |
| `symbol_consistency_violations` | 0 | 0 |
| `nonfinite_violations` | **91 840** | **91 841** |
| `nonnegative_oi_violations` | 0 | 0 |
| `nonnegative_ratio_violations` | 0 | 0 |
| `date_range_coverage` | true | true |
| **`research_eligible`** | **false** | **false** |

Both metrics datasets FAIL Phase 4h §17.4 strict gate due to two
distinct findings:

### Finding 1 — Intra-day missing 5-minute observations

BTCUSDT: 5 699 missing observations (concatenated as gap intervals).
ETHUSDT: 3 631 missing observations.

Sample (first five gaps; full list in each manifest's
`quality_checks.gap_locations` and `invalid_windows`):

**BTCUSDT:**

```text
2023-09-12 08:35 UTC -> 2023-09-12 08:55 UTC   ( 20 min gap)
2024-02-16 13:30 UTC -> 2024-02-17 00:00 UTC   (630 min gap)
2024-03-03 23:55 UTC -> 2024-03-04 00:05 UTC   ( 10 min gap)
2024-03-04 05:30 UTC -> 2024-03-04 05:35 UTC   (  5 min gap)
2024-03-04 05:35 UTC -> 2024-03-04 05:40 UTC   (  5 min gap)
```

**ETHUSDT:** same windows pattern with minor per-symbol variation
(same upstream maintenance windows).

These windows are intra-day gaps within otherwise-present daily
archives; the daily archives themselves are 100% present (`missing_days
= 0`). The gaps appear to correspond to upstream
`data.binance.vision` maintenance / pipeline windows analogous to the
mark-price 4-gap pattern documented by Phase 3q (which Phase 3r §8
governance addresses).

### Finding 2 — NaN values in optional ratio columns (early-2022 concentration)

NaN values are concentrated in the four ratio columns
(`count_toptrader_long_short_ratio`, `sum_toptrader_long_short_ratio`,
`count_long_short_ratio`, `sum_taker_long_short_vol_ratio`) and are
heavily concentrated in early-2022 data. Sample distribution:

| Symbol | Month | OI cols (NaN/n) | toptrader ratios (NaN/n) | account L/S ratio (NaN/n) | taker imbalance (NaN/n) |
|---|---|---|---|---|---|
| BTCUSDT | 2022-01 | 0 / 8 928 | 8 640 / 8 928 (~97%) | 5 344 / 8 928 (~60%) | 8 640 / 8 928 (~97%) |
| BTCUSDT | 2026-03 | 0 / 8 928 | 0 / 8 928 | 0 / 8 928 | 0 / 8 928 |
| ETHUSDT | 2022-01 | 0 / 8 928 | 8 640 / 8 928 (~97%) | 5 344 / 8 928 (~60%) | 8 640 / 8 928 (~97%) |
| ETHUSDT | 2026-03 | 0 / 8 928 | 0 / 8 928 | 0 / 8 928 | 0 / 8 928 |

**Critical observation:** `sum_open_interest` and
`sum_open_interest_value` are FULLY POPULATED (zero NaN) in both
early-2022 and recent 2026-03 data. The NaN concentration is in
ratio columns that Binance progressively backfilled / extended over
time — these were not part of the public archive at full coverage in
early 2022.

### V2-required vs. V2-optional column impact

Per Phase 4g §28 / Phase 4h §27, V2 entry feature 8 OI sub-component
uses `sum_open_interest` (which has 0 NaN). V2's primary
taker-imbalance source is the kline `taker_buy_volume` column (per
Phase 4h §24), NOT the metrics `sum_taker_long_short_vol_ratio`
column. The metrics ratio columns are documented in Phase 4g §28 as
**optional features documented but NOT activated** by the spec;
specifically the metrics taker ratio is a CROSS-CHECK source only.

So the metrics datasets' strict-gate failure is driven primarily by
NaN values in OPTIONAL fields (toptrader long/short ratio; account
long/short ratio; taker_long_short_vol_ratio cross-check), NOT by
issues in the V2-active fields (`sum_open_interest`).

This is recorded transparently and **does not by itself license
relaxing the strict gate.** Phase 4i preserves Phase 4h §17.4 verbatim.
Whether to permit V2 to use the OI-only subset under a separately
authorized governance memo (analogous to Phase 3r §8 for mark-price)
is an operator decision.

## research_eligible verdicts

```text
binance_usdm_btcusdt_30m__v001:        research_eligible: true
binance_usdm_ethusdt_30m__v001:        research_eligible: true
binance_usdm_btcusdt_4h__v001:         research_eligible: true
binance_usdm_ethusdt_4h__v001:         research_eligible: true
binance_usdm_btcusdt_metrics__v001:    research_eligible: false
binance_usdm_ethusdt_metrics__v001:    research_eligible: false
```

Per the brief: *"If any required check fails, the dataset is not
research-eligible. Do not run diagnostics anyway. Do not relax
requirements. Do not silently patch or forward-fill data. Write a
failure report and stop."* and *"If any family is not research_eligible,
Phase 4i must stop for operator review and must not proceed to any
backtest or successor phase."*

Phase 4i is therefore **stopping for operator review.**

## Invalid windows and gaps

Each metrics manifest's `invalid_windows` field records the detected
intra-day gap intervals verbatim. The list is capped at 200 entries
per manifest (Phase 3q-style cap to keep manifest sizes reasonable);
the full set of 5 699 (BTC) / 3 631 (ETH) gap intervals is
re-derivable from the underlying Parquet by re-running
`scripts/phase4i_v2_acquisition.py`'s integrity-check function on
the existing local data.

**No forward-fill, interpolation, or silent omission was applied. No
data was patched.**

## Feasibility outcome after acquisition

Phase 4h §10 declared feasibility as POSITIVE under defined boundary,
with the note that the `metrics` family was the only NEW family
required (not just NEW interval). Phase 4i confirms:

- All three NEW kline intervals (30m × 2 + 4h × 2) are research-eligible.
- The NEW `metrics` family is acquirable but NOT research-eligible
  under the strict Phase 4h §17.4 gate due to two upstream
  characteristics: (a) intra-day 5-minute gaps; (b) NaN values in
  optional ratio columns (especially early-2022).

The OI-subset of metrics (`sum_open_interest`, `sum_open_interest_value`)
IS fully populated and IS gap-aligned to the 5-minute boundaries (the
NaN values are in the ratio columns, not OI; the `missing_observations`
gaps span entire records, but those entire records are absent —
including their OI fields). However, the `sum_open_interest` data IS
present at every present 5-minute timestamp, so V2's OI-delta
computation could be derived from the OI subset under an
operator-authorized partial-eligibility governance memo (analogous to
Phase 3r §8 for mark-price).

**Phase 4i does NOT propose any such governance memo.** That is an
operator decision in a future docs-only phase.

## Data-size summary

```text
Raw ZIPs:          ~49 MB total
Normalized Parquet: ~56 MB total
Total local footprint: ~105 MB
```

Per-family breakdown:

| Family | Raw size | Normalized size |
|---|---|---|
| BTCUSDT 30m klines | ~3.7 MB | ~4.7 MB |
| ETHUSDT 30m klines | ~3.8 MB | ~4.7 MB |
| BTCUSDT 4h klines | ~636 KB | ~1.0 MB |
| ETHUSDT 4h klines | ~636 KB | ~1.1 MB |
| BTCUSDT metrics | ~20 MB | ~22 MB |
| ETHUSDT metrics | ~20 MB | ~23 MB |

## Reproducibility notes

- **Public unauthenticated source only.** No credentials.
- **SHA256 verification.** Every raw ZIP was verified against its
  paired `.CHECKSUM` before normalization. Per-archive SHA256 is
  recorded in each manifest's `raw_sha256_index`.
- **Idempotent.** If a raw ZIP already exists with valid SHA256, the
  download step is skipped. If a Parquet partition exists, it is
  regenerated deterministically from the raw ZIP.
- **Public bulk archive only.** No `prometheus.research.data.*`
  modification. No `Interval` enum extension. No new package modules.
- **Standalone script.** `scripts/phase4i_v2_acquisition.py` is the
  only Python file added to the repo; it does not import anything
  from `prometheus.*`.
- **No test modification required.** Tests are not affected.
- **Reproducible from public sources via the orchestrator script.**

## Commands run

```text
git status
git checkout -b phase-4i/v2-public-data-acquisition-and-integrity-validation
.venv/Scripts/python --version
.venv/Scripts/python -m ruff check scripts/phase4i_v2_acquisition.py
.venv/Scripts/python -m mypy scripts/phase4i_v2_acquisition.py
.venv/Scripts/python scripts/phase4i_v2_acquisition.py --start 2022-01 --end 2022-01 --symbols BTCUSDT --families klines_30m metrics --workers 8
.venv/Scripts/python scripts/phase4i_v2_acquisition.py --start 2022-01 --end 2026-03 --symbols BTCUSDT ETHUSDT --families klines_30m klines_4h metrics --workers 8
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m pytest -q
.venv/Scripts/python -m mypy
```

The first invocation of `phase4i_v2_acquisition.py` was a 1-month
BTC-only smoke test (klines_30m + metrics) to verify the script's
parsing, checksum verification, and integrity-check logic before
the full run. The smoke test produced a research_eligible=false
manifest pair (expected: 1-month coverage cannot satisfy the
4-year coverage gate); the manifests were overwritten by the full
run.

The following commands were **NOT** run (per Phase 4i brief
prohibitions):

- No `scripts/phase3q_5m_acquisition.py` execution.
- No `scripts/phase3s_5m_diagnostics.py` execution.
- No backtest execution.
- No diagnostic / Q1–Q7 question rerun.
- No mark-price 30m / 4h acquisition.
- No `aggTrades` acquisition.
- No spot data acquisition.
- No private / authenticated REST or WebSocket request.

## Verification results

| Check | Result |
|---|---|
| `.venv/Scripts/python --version` | `Python 3.12.4` |
| `.venv/Scripts/python -m ruff check .` | `All checks passed!` |
| `.venv/Scripts/python -m pytest` | `785 passed in 12.75s` |
| `.venv/Scripts/python -m mypy` | `Success: no issues found in 82 source files` |

Whole-repo quality gates remain **fully clean**: zero ruff errors;
785 / 785 tests passing; zero mypy strict issues across 82 source
files. No regressions relative to the post-Phase-4h-merge baseline.

## Files changed

Phase 4i adds the following committed files (script + 6 manifests +
report + closeout):

```text
scripts/phase4i_v2_acquisition.py                                                              (new)
data/manifests/binance_usdm_btcusdt_30m__v001.manifest.json                                    (new)
data/manifests/binance_usdm_ethusdt_30m__v001.manifest.json                                    (new)
data/manifests/binance_usdm_btcusdt_4h__v001.manifest.json                                     (new)
data/manifests/binance_usdm_ethusdt_4h__v001.manifest.json                                     (new)
data/manifests/binance_usdm_btcusdt_metrics__v001.manifest.json                                (new)
data/manifests/binance_usdm_ethusdt_metrics__v001.manifest.json                                (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4i_v2-public-data-acquisition-and-integrity-validation.md  (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4i_closeout.md                            (new)
```

Phase 4i does NOT commit `data/raw/**` or `data/normalized/**`
artefacts; they are local research evidence reproducible from the
public bulk archive via the orchestrator script.

Phase 4i does NOT modify any existing v002 manifest, v001-of-5m
manifest, source-code module, test, or specification document. The
only changes are: the standalone acquisition script; the six new
manifest files; the Phase 4i report; the Phase 4i closeout.

## What this does not authorize

Phase 4i explicitly does NOT authorize, propose, or initiate any of
the following:

- **V2 backtest.** Forbidden until two metrics datasets are either
  research-eligible OR a separately authorized governance memo permits
  partial-eligibility for OI-only metrics use (analogous to Phase 3r
  §8 for mark-price). Phase 4i does NOT propose such a governance
  memo.
- **V2 implementation.** Forbidden until V2 backtest evidence is in
  AND a separately authorized implementation phase exists.
- **V2 strategy implementation.** Forbidden.
- **V2 strategy / execution / risk module modification.** Forbidden.
- **Phase 4 (canonical).** Per `docs/12-roadmap/phase-gates.md`.
- **Phase 4j or any successor phase.** Phase 4i is docs-and-data only;
  successor authorization is a separate operator decision.
- **Mark-price 30m / 4h acquisition.** DEFERRED per Phase 4h §20.
- **`aggTrades` acquisition.** DEFERRED per Phase 4h §7.E.
- **v003 dataset creation.** Phase 4i is `__v001` (new families) and
  preserves v002 / v001-of-5m verbatim.
- **v002 / v001-of-5m manifest modification.** Preserved.
- **§11.6 / §1.7.3 / Phase 3r §8 / Phase 3v §8 / Phase 3w §6 / §7 / §8
  governance modification.** All preserved verbatim.
- **Phase 4f / Phase 4g / Phase 4h text modification.** All preserved.
- **R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A revision.** All
  preserved verbatim.
- **Lock change.**
- **Live exchange-write capability, production Binance keys,
  authenticated APIs, private endpoints, user stream, WebSocket,
  listenKey lifecycle, production alerting, Telegram / n8n production
  routes, MCP, Graphify, `.mcp.json`, credentials.** None touched,
  enabled, or implied.

## Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4j / successor phase started.** No
  subsequent phase has been authorized, scoped, briefed, branched, or
  commenced.
- **No V2 implementation.**
- **No V2 backtest.**
- **No V2 validation.**
- **No diagnostics run.** No Phase 3o / 3p Q1–Q7 question rerun.
- **No backtests run.**
- **No `scripts/phase3q_5m_acquisition.py` execution.**
- **No `scripts/phase3s_5m_diagnostics.py` execution.**
- **No mark-price 30m / 4h acquisition.**
- **No `aggTrades` acquisition.**
- **No spot data acquisition.**
- **No cross-venue acquisition.**
- **No funding-rate re-acquisition** (v002 funding manifests reused).
- **No v002 dataset / manifest modification.**
- **No v001-of-5m dataset / manifest modification.**
- **No v003 created.**
- **No Phase 3p §4.7 amendment.**
- **No Phase 3r §8 mark-price gap governance modification.**
- **No Phase 3v `stop_trigger_domain` governance modification.**
- **No Phase 3w `break_even_rule` / `ema_slope_method` /
  `stagnation_window_role` governance modification.**
- **No Phase 4f text modification.**
- **No Phase 4g V2 strategy-spec modification.**
- **No Phase 4h text modification.**
- **No `src/prometheus/**` modification.**
- **No `tests/**` modification.**
- **No existing `scripts/**` modification.** (`scripts/phase4i_v2_acquisition.py`
  is new and standalone.)
- **No `prometheus.research.data.*` extension.**
- **No `Interval` enum extension.**
- **No `pyproject.toml` modification.**
- **No `.gitignore` modification.**
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No `.env` file creation.**
- **No credential storage / request / use.**
- **No authenticated REST / private endpoint / public endpoint /
  user-stream / WebSocket calls.**
- **No production alerting / Telegram / n8n production routes.**
- **No MCP enabling / Graphify enabling.**
- **No deployment artefact created.**
- **No paper / shadow runtime created.**
- **No live-readiness implication.**
- **No order placement / cancellation.**
- **No real exchange adapter implementation.**
- **No exchange-write capability.**
- **No reconciliation implementation.**
- **No retained-evidence verdict revision.**
- **No project-lock revision.**
- **No threshold / parameter modification.**
- **No `docs/00-meta/implementation-ambiguity-log.md` modification.**
- **No `docs/00-meta/current-project-state.md` modification on the
  Phase 4i branch.** Per the Phase 4i brief.
- **No `.claude/rules/**` modification.**
- **No merge to main.**
- **No successor phase started.**

## Remaining boundary

- **Recommended state:** **paused** for any successor phase. Phase 4i
  deliverables (script + 6 manifests + this report) exist as
  branch-only artefacts pending operator review.
- **Phase 4i output:** docs-and-data acquisition + integrity report on
  the Phase 4i branch.
- **Repository quality gate state:** **fully clean.** Whole-repo `ruff
  check .` passes; pytest 785 passed; mypy strict 0 issues across 82
  source files (verified during Phase 4i).
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4
  (canonical) remains not authorized. Phase 4a–4h all merged. Phase
  4i V2 public data acquisition + integrity validation on this branch.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 +
  enforced in code by Phase 4a (preserved through Phase 4i).
- **Break-even rule governance:** RESOLVED by Phase 3w §6 + enforced
  in code by Phase 4a (preserved).
- **EMA slope method governance:** RESOLVED by Phase 3w §7 + enforced
  in code by Phase 4a (preserved).
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 +
  enforced in code by Phase 4a (preserved).
- **Mark-price gap governance:** Phase 3r §8 (preserved).
- **Reconciliation governance:** Defined by Phase 4e but NOT yet
  enforced in code; awaits separately authorized future implementation
  phase.
- **V2 strategy-research direction:** Predeclared by Phase 4f as
  *Participation-Confirmed Trend Continuation*; operationalized by
  Phase 4g (strategy spec) and Phase 4h (data requirements). Phase 4i
  acquired 6 of 6 minimum dataset families; 4 of 6 are research-eligible;
  2 of 6 (metrics) are NOT research-eligible under the strict gate.
  V2 is **NOT implemented; NOT backtested; NOT validated; NOT
  live-ready; NOT a rescue.**
- **OPEN ambiguity-log items after Phase 4i:** zero relevant to
  runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0
  framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained
  research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other;
  §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price
  stops; v002 verdict provenance; Phase 3q mark-price 5m manifests
  `research_eligible: false`. All preserved.
- **Branch state:**
  `phase-4i/v2-public-data-acquisition-and-integrity-validation`
  exists locally and (after push) on `origin`. NOT merged to main.

## Operator decision menu

The operator now has Phase 4i's evidence: 4 of 6 datasets pass; 2 of 6
fail Phase 4h §17.4 strict gate due to upstream `data.binance.vision`
metrics characteristics (intra-day 5-minute gaps + NaN values in
optional ratio columns). The next operator decision is operator-driven
only.

### Option A — Remain paused, accept Phase 4i partial-pass evidence (PRIMARY recommendation)

Take no further action. Phase 4i acquisition + integrity-check evidence
is recorded. The 6 dataset manifests are committed. Trade-price 30m and
4h klines are research-eligible; metrics datasets are NOT
research-eligible under the strict gate. No backtest is run. No
successor phase authorized.

**Reasoning:**

- Phase 4i acquisition + integrity-check value is realized: the project
  now has on-disk evidence of exactly which V2 data exists and exactly
  which integrity property holds for each family.
- The metrics gap finding is a genuine evidence pattern (analogous to
  Phase 3q's mark-price gap finding for v001-of-5m).
- The metrics NaN pattern is concentrated in OPTIONAL columns; the
  V2-required `sum_open_interest` column is fully populated. This is
  documentary evidence the operator may use in a future
  governance-memo decision but does NOT license relaxation here.
- Selecting Option A preserves all locks; preserves Phase 4h §17.4
  predeclaration discipline; produces no V2 backtest; does not relax
  any gate.

### Option B — Authorize a future Phase 4i-followup governance memo (CONDITIONAL secondary)

Authorize a docs-only memo (analogous to Phase 3r §8 for mark-price
gaps) that formally proposes:

1. A `metrics_ineligibility_governance` rule analogous to Phase 3r §8:
   metrics datasets remain `research_eligible: false`; intra-day gaps
   are documented in `invalid_windows`; NaN values are documented per
   column; future V2 backtests must apply per-bar exclusion when an
   alignment-required metrics record is missing OR when any required
   metrics field at the alignment timestamp is NaN.
2. OR a partial-eligibility scheme: V2 entry feature 8 OI sub-component
   may use the OI subset (`sum_open_interest`, `sum_open_interest_value`
   only) without requiring the optional ratio columns to be finite at
   the alignment timestamp; the V2 backtest brief must predeclare this
   subset before any backtest is run.

**Phase 4i does NOT propose either of these as a recommendation** —
proposing either is the operator's decision. Phase 4i merely
acknowledges that an analogous Phase 3r §8 governance pattern is
available if the operator authorizes a future memo.

### Option C — Acquire mark-price 30m / 4h to enable mark_price_backtest_candidate path (NOT RECOMMENDED before V2 first backtest)

Mark-price 30m / 4h was deferred by Phase 4h §20 specifically because
it is not required by V2's first backtest. Acquiring it before V2's
first backtest evidence would invert the standard ordering. NOT
recommended at this boundary.

### Option D — Acquire `aggTrades` (NOT RECOMMENDED)

`aggTrades` is OPTIONAL / DEFERRED per Phase 4h §7.E. Phase 4i confirms
that klines `taker_buy_volume` is fully populated for V2 entry feature 7.
NOT recommended.

### Option E — Run V2 first backtest immediately (REJECTED)

The brief explicitly forbids this: *"If any family is not
research_eligible, Phase 4i must stop for operator review and must not
proceed to any backtest or successor phase."* REJECTED.

### Option F — V2 implementation (REJECTED)

Requires successful backtest evidence (which does not exist). REJECTED.

### Option G — Paper / shadow / live-readiness / exchange-write (FORBIDDEN)

Per `docs/12-roadmap/phase-gates.md`, none of these gates is met.
FORBIDDEN.

## Next authorization status

**No next phase has been authorized.** Phase 4i's primary
recommendation is **Option A (remain paused, accept partial-pass
evidence)**, with **Option B (authorize a future docs-only governance
memo addressing the metrics gap / NaN handling) as conditional
secondary**. Options C / D are not recommended at this boundary.
Options E / F / G are rejected / forbidden.

Selection of any subsequent phase requires explicit operator
authorization for that specific phase. No such authorization has been
issued.

The 5m research thread remains operationally complete and closed (per
Phase 3t). The implementation-readiness boundary remains reviewed (per
Phase 3u). All four Phase 3u §8.5 pre-coding governance blockers
remain RESOLVED at the governance level (per Phase 3v + Phase 3w).
The Phase 4a safe-slice scope is implemented (per Phase 4a). The
Phase 4b script-scope quality-gate restoration is complete (per Phase
4b). The Phase 4c state-package quality-gate residual cleanup is
complete (per Phase 4c). The Phase 4d post-4a/4b/4c review is complete
(per Phase 4d). The Phase 4e reconciliation-model design memo is
complete (per Phase 4e). The Phase 4f V2 hypothesis predeclaration is
complete (per Phase 4f). The Phase 4g V2 strategy spec is complete
(per Phase 4g). The Phase 4h V2 data-requirements / feasibility memo
is complete (per Phase 4h). The Phase 4i V2 public data acquisition
+ integrity validation is complete on this branch (this phase) with
**partial-pass verdict** (4 of 6 datasets research-eligible).
**Recommended state remains paused.**
