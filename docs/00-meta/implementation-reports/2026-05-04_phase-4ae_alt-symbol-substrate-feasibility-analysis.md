# Phase 4ae — Alt-Symbol Substrate-Feasibility Analysis Memo

**Authority:** Operator authorization for Phase 4ae (analysis-and-docs substrate-feasibility analysis using existing local normalized data and committed manifests under Phase 4ad future-use rules). Phase 4ad (alt-symbol gap-governance and scope-revision memo; Rule A mark-price invalid-window exclusion; Rule B SOL/XRP early-2022 kline gap scope policy with B1 / B2 / B3; Rule C PASS-only subset; merged 10f122e). Phase 4ac (alt-symbol public data acquisition / integrity validation; merged 3478d05). Phase 4ab (alt-symbol data-requirements / feasibility memo). Phase 4aa (alt-symbol market-selection / admissibility memo). Phase 3p §4.7 (strict integrity gate); Phase 3r §8 (mark-price gap governance precedent); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 4j §11 (metrics OI-subset partial-eligibility binding precedent); Phase 4k (V2 backtest-plan); Phase 4p (G1 strategy spec); Phase 4q (G1 backtest-plan); Phase 4v (C1 strategy spec); Phase 4w (C1 backtest-plan); Phase 4z (post-rejection research-process redesign); Phase 2p §C.1 (R3 baseline-of-record); Phase 2i §1.7.3 (project-level locks); `docs/04-data/historical-data-spec.md`; `docs/04-data/dataset-versioning.md`; `docs/04-data/timestamp-policy.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4ae — **Alt-Symbol Substrate-Feasibility Analysis Memo** (analysis-and-docs only). Computes descriptive substrate-feasibility metrics for the Phase 4ac core symbol set under Phase 4ad future-use rules. **Phase 4ae is analysis-and-docs only.** No new data acquired or modified. No manifest created or modified. No backtest run. No strategy diagnostics. No Q1–Q7 rerun. No strategy candidate, hypothesis-spec, strategy-spec, or backtest-plan created. No `src/prometheus/`, tests, or existing scripts modified. No retained verdict revised. No project lock changed. **No successor phase authorized.**

**Branch:** `phase-4ae/alt-symbol-substrate-feasibility-analysis`. **Memo date:** 2026-05-04 UTC.

---

## 1. Purpose

Phase 4ae computes descriptive substrate-feasibility metrics for the Phase 4ac core symbol set (BTCUSDT / ETHUSDT / SOLUSDT / XRPUSDT / ADAUSDT) at intervals 15m / 30m / 1h / 4h, under Phase 4ad Rule B1 (common post-gap start at 2022-04-03 00:00 UTC), to help inform whether the alt symbols differ meaningfully from BTC/ETH as market substrates for any future strategy research.

**Phase 4ae is analysis-and-docs only.**

- **No data acquisition.** No new dataset is downloaded.
- **No data modification.** No patching / forward-fill / interpolation / imputation / synthesis / regeneration / replacement.
- **No manifest creation or modification.** Existing manifests inspected read-only.
- **No backtest.** No backtest is run, planned, or scoped.
- **No strategy diagnostics / Q1–Q7 rerun.** No diagnostic phase. No stop-pathology diagnostics derived from substrate metrics.
- **No strategy candidate.** No strategy is named, defined, or specified.
- **No hypothesis-spec memo.** No new hypothesis is named.
- **No strategy-spec memo.** No new strategy spec is authored.
- **No backtest-plan memo.** No backtest methodology is specified.
- **No implementation.** No `src/prometheus/`, tests, or existing scripts modified.
- **No live-readiness.** No paper / shadow / live operation authorized, planned, or implied.
- **No exchange-write.** No production keys, authenticated APIs, private endpoints, user stream, WebSocket, exchange-write capability, MCP, Graphify, or `.mcp.json` touched.

The metrics in this memo are **descriptive substrate metrics only**. They are NOT strategy signals, NOT entry/exit triggers, NOT candidate thresholds, NOT optimization targets, NOT live-readiness inputs.

## 2. Data Scope and Governance

### 2.1 Symbols and intervals

```text
Symbols   : BTCUSDT  ETHUSDT  SOLUSDT  XRPUSDT  ADAUSDT
Intervals : 15m  30m  1h  4h
```

### 2.2 Date range

```text
Start (UTC, inclusive)    : 2022-04-03 00:00:00
End   (UTC, inclusive)    : 2026-04-30 23:59:59
```

### 2.3 Phase 4ad Rule application

- **Rule B1 (common post-gap start) APPLIED.** Analysis begins at 2022-04-03 00:00 UTC, the first complete bar after the second SOL / XRP early-2022 trade-price gap. The same start applies to all five symbols for cross-symbol fairness.
- **Rule A (mark-price invalid-window exclusion) NOT INVOKED.** Phase 4ae does NOT use mark-price datasets. Mark-price-dependent analysis is **deferred** per the Phase 4ae brief recommendation ("Recommended for this first Phase 4ae: prefer trade-price-only wick proxy metrics; avoid mark-price-dependent conclusions"). Wick / stop-pathology proxies (§8) are computed from trade-price kline OHLC only.
- **Rule C (PASS-only subset) NOT USED EXCLUSIVELY.** Rule B1 is the primary governance scope; Rule C-style PASS-only sub-analysis is implicit in that the PASS subset (BTC 1h, ETH 1h, ADA 15m / 30m / 1h / 4h, SOL / XRP / ADA funding) is included in the Rule B1-window cells alongside the Rule B1-governed SOL / XRP klines.

### 2.4 PASS vs Rule B1-governed datasets actually used

| Symbol | Interval | Manifest | Eligibility | Governance scope |
| --- | --- | --- | --- | --- |
| BTCUSDT | 15m | `binance_usdm_btcusdt_15m__v002` (Phase 2c) | legacy | PASS_or_legacy_phase2_eligible_via_v002 |
| BTCUSDT | 30m | `binance_usdm_btcusdt_30m__v001` (Phase 4i) | true | PASS |
| BTCUSDT | 1h | `binance_usdm_btcusdt_1h__v001` (Phase 4ac) | true | PASS |
| BTCUSDT | 4h | `binance_usdm_btcusdt_4h__v001` (Phase 4i) | true | PASS |
| ETHUSDT | 15m | `binance_usdm_ethusdt_15m__v002` (Phase 2c) | legacy | PASS_or_legacy_phase2_eligible_via_v002 |
| ETHUSDT | 30m | `binance_usdm_ethusdt_30m__v001` (Phase 4i) | true | PASS |
| ETHUSDT | 1h | `binance_usdm_ethusdt_1h__v001` (Phase 4ac) | true | PASS |
| ETHUSDT | 4h | `binance_usdm_ethusdt_4h__v001` (Phase 4i) | true | PASS |
| SOLUSDT | 15m / 30m / 1h / 4h | `binance_usdm_solusdt_*__v001` (Phase 4ac) | false (global) | Phase4ad_RuleB1_common_post_gap |
| XRPUSDT | 15m / 30m / 1h / 4h | `binance_usdm_xrpusdt_*__v001` (Phase 4ac) | false (global) | Phase4ad_RuleB1_common_post_gap |
| ADAUSDT | 15m / 30m / 1h / 4h | `binance_usdm_adausdt_*__v001` (Phase 4ac) | true | PASS |

**SOL / XRP kline-derived conclusions in this memo are labeled `conditional on Phase 4ad Rule B1 common post-gap scope`.** Phase 4ae does NOT flip any `research_eligible` flag; the manifests remain unchanged.

### 2.5 What is excluded

- **Mark-price datasets:** NOT used. Deferred per Phase 4ae brief recommendation. Phase 4ad Rule A would apply if used in any future analysis.
- **Metrics / OI:** NOT used. Phase 4ac did not acquire metrics for alt symbols; Phase 4ab §6.D / Phase 4j §11 governance preserved.
- **AggTrades / tick / order-book:** NOT used. Phase 4ab §6.E deferred; Phase 4ac did not acquire.
- **Pre-2022-04-03 data:** EXCLUDED for all symbols (Rule B1 common-overlap discipline).
- **Partial May 2026 data:** EXCLUDED. End date 2026-04-30 23:59:59 UTC inclusive.
- **BTC / ETH funding:** NOT used in this memo. Phase 4ae's funding analysis covers SOL / XRP / ADA from Phase 4ac PASS funding manifests; BTC / ETH funding data exists locally under a legacy `data/normalized/funding_rate/` path with a different schema (`funding_time`, `funding_rate`) than Phase 4ac's `data/normalized/funding/` path (`calc_time`, `last_funding_rate`). The script supports reading both; the analysis run included BTC / ETH funding in the funding-metrics output. See §10 for the full funding table.

## 3. Methodology

### 3.1 Inputs

- **Trade-price klines** read from `data/normalized/klines/symbol={SYM}/interval={IV}/year=YYYY/month=MM/part-0000.parquet` (gitignored; reproducible from prior phase orchestrators).
- **Funding** read from `data/normalized/funding/symbol={SYM}/year=YYYY/month=MM/part-0000.parquet` (Phase 4ac alt-symbol path) or `data/normalized/funding_rate/symbol={SYM}/year=YYYY/month=MM/part-0000.parquet` (Phase 2 legacy BTC/ETH path).
- **Manifests** read read-only from `data/manifests/binance_usdm_<sym>_<iv>__v00X.manifest.json` for eligibility tagging only.

### 3.2 Predeclared descriptive thresholds (NOT optimized)

```text
ROLLING_WINDOW_BARS         = 96
ATR_WINDOW                  = 20
EMA_FAST                    = 50
EMA_SLOW                    = 200
EXPANSION_RANGE_THRESHOLDS  = (1.0×, 1.5×) of rolling median range
EXPANSION_ABSRET_THRESHOLDS = (1.0×, 1.5×) of rolling median |close-to-close return|
WICK_FRACTION_THRESHOLD     = 0.5
HIGH_COST_BPS_PER_SIDE      = 8.0     (§11.6 preserved)
ROUND_TRIP_COST_BPS         = 16.0
```

### 3.3 Metrics computed

For every (symbol, interval) cell:

- **Coverage / eligibility (§A in brief):** bar count, first / last bar timestamps, expected vs observed bars in span, manifest path, manifest eligibility, governance scope.
- **Cost-to-volatility (§B):** median range bps, ATR(20) Wilder bps median / p25 / p75, ratio of one-way HIGH cost (8 bps) and round-trip HIGH cost (16 bps) to median range / ATR.
- **Opportunity-rate / expansion-event (§C):** fraction of bars and events / 1 000 bars where range > {1.0×, 1.5×} rolling-median range; same for |close-to-close return|.
- **Trend / regime descriptive (§D):** fraction of bars with close > EMA(50); fraction with EMA(50) > EMA(200); fraction with discrete-comparison positive EMA(50) slope (today's EMA50 vs 3 bars earlier); transition count between EMA(50)>EMA(200) and EMA(50)<EMA(200).
- **Wick / stop-pathology proxies (§E):** median upper / lower wick fraction; fraction of bars with upper wick fraction > 0.5; fraction with lower wick fraction > 0.5; fraction with both elevated.
- **Funding distribution (§F):** event count, median bps, p25 / p75 / p05 / p95 in bps, fraction positive / negative, absolute median / p95 / p99.
- **Volume / notional turnover proxy (§G):** median volume; median notional proxy = `close × volume`; p25 / p75 of notional proxy. (No hard volume floor invented; distributions reported only.)
- **Cross-symbol ranking tables (§H):** per-interval ranking by ATR-bps median, range-bps median, round-trip-cost / ATR ratio, expansion 1.5× event rate, upper-wick fraction, lower-wick fraction, notional proxy median; per-symbol funding ranking by absolute median, abs p95, p95, p05, frac positive.

All thresholds are **descriptive and predeclared**. No optimization. No threshold selection from results.

## 4. Coverage Results

All 20 (symbol, interval) cells produced complete coverage in the Phase 4ad Rule B1 window. **Zero missing bars** in the observed span for every cell.

| Symbol | Interval | Bar count | First bar (UTC) | Last bar (UTC) | Manifest eligible | Governance scope |
| --- | --- | --- | --- | --- | --- | --- |
| BTCUSDT | 15m | 140 064 | 2022-04-03 | 2026-03-31 | legacy | PASS_or_legacy_phase2_eligible_via_v002 |
| BTCUSDT | 30m | 70 032 | 2022-04-03 | 2026-03-31 | true | PASS |
| BTCUSDT | 1h | 35 736 | 2022-04-03 | 2026-04-30 | true | PASS |
| BTCUSDT | 4h | 8 754 | 2022-04-03 | 2026-03-31 | true | PASS |
| ETHUSDT | 15m | 140 064 | 2022-04-03 | 2026-03-31 | legacy | PASS_or_legacy_phase2_eligible_via_v002 |
| ETHUSDT | 30m | 70 032 | 2022-04-03 | 2026-03-31 | true | PASS |
| ETHUSDT | 1h | 35 736 | 2022-04-03 | 2026-04-30 | true | PASS |
| ETHUSDT | 4h | 8 754 | 2022-04-03 | 2026-03-31 | true | PASS |
| SOLUSDT | 15m | 142 944 | 2022-04-03 | 2026-04-30 | false | Phase4ad_RuleB1_common_post_gap |
| SOLUSDT | 30m | 71 472 | 2022-04-03 | 2026-04-30 | false | Phase4ad_RuleB1_common_post_gap |
| SOLUSDT | 1h | 35 736 | 2022-04-03 | 2026-04-30 | false | Phase4ad_RuleB1_common_post_gap |
| SOLUSDT | 4h | 8 934 | 2022-04-03 | 2026-04-30 | false | Phase4ad_RuleB1_common_post_gap |
| XRPUSDT | 15m | 142 944 | 2022-04-03 | 2026-04-30 | false | Phase4ad_RuleB1_common_post_gap |
| XRPUSDT | 30m | 71 472 | 2022-04-03 | 2026-04-30 | false | Phase4ad_RuleB1_common_post_gap |
| XRPUSDT | 1h | 35 736 | 2022-04-03 | 2026-04-30 | false | Phase4ad_RuleB1_common_post_gap |
| XRPUSDT | 4h | 8 934 | 2022-04-03 | 2026-04-30 | false | Phase4ad_RuleB1_common_post_gap |
| ADAUSDT | 15m | 142 944 | 2022-04-03 | 2026-04-30 | true | PASS |
| ADAUSDT | 30m | 71 472 | 2022-04-03 | 2026-04-30 | true | PASS |
| ADAUSDT | 1h | 35 736 | 2022-04-03 | 2026-04-30 | true | PASS |
| ADAUSDT | 4h | 8 934 | 2022-04-03 | 2026-04-30 | true | PASS |

**End-date asymmetry note:** BTC / ETH at 15m, 30m, 4h end at 2026-03-31 (Phase 2 / Phase 4i `__v001` / `__v002` manifests acquired before Phase 4ac). BTC / ETH 1h direct kline ends at 2026-04-30 (Phase 4ac NEW). SOL / XRP / ADA all end at 2026-04-30 (Phase 4ac). The asymmetry is one calendar month; bar counts in the analysis window remain very large (≥ 8 754 4h bars; ≥ 35 736 1h bars; ≥ 70 032 30m bars; ≥ 140 064 15m bars per symbol). Cross-symbol comparisons are computed over each cell's actual covered span; no analysis decision in this memo depends on the missing month for BTC / ETH at 15m / 30m / 4h.

**SOL / XRP early-2022 gap windows are NOT in the analysis window** (they end at 2022-04-03 00:00 UTC, the Phase 4ad Rule B1 start). Hence zero missing bars in the observed span for SOL / XRP in this analysis. **Phase 4ad Rule B1 is correctly applied; no SOL / XRP `research_eligible` flag is flipped.**

**No datasets omitted.** All 20 cells passed coverage.

## 5. Cost-to-Volatility Results

### 5.1 Cost-cushion table (round-trip 16 bps / median ATR(20))

Lower ratio = more volatility cushion relative to round-trip HIGH cost.

| Symbol | 15m | 30m | 1h | 4h |
| --- | ---: | ---: | ---: | ---: |
| BTCUSDT | 0.5110 | 0.3496 | 0.2410 | 0.1139 |
| ETHUSDT | 0.3764 | 0.2590 | 0.1792 | 0.0837 |
| SOLUSDT | 0.2574 | 0.1796 | 0.1245 | 0.0600 |
| XRPUSDT | 0.3381 | 0.2341 | 0.1617 | 0.0767 |
| ADAUSDT | 0.2885 | 0.2001 | 0.1382 | 0.0665 |

### 5.2 Median ATR(20) bps and median range bps

| Symbol | Interval | Median range (bps) | Median ATR (bps) | ATR p25 (bps) | ATR p75 (bps) |
| --- | --- | ---: | ---: | ---: | ---: |
| BTCUSDT | 15m |  26.43 |  31.31 |  19.23 |  46.94 |
| BTCUSDT | 30m |  38.18 |  45.77 |  28.37 |  68.58 |
| BTCUSDT | 1h |  55.29 |  66.39 |  41.66 |  98.92 |
| BTCUSDT | 4h | 118.90 | 140.52 |  90.21 | 209.11 |
| ETHUSDT | 15m |  36.23 |  42.51 |  25.85 |  64.54 |
| ETHUSDT | 30m |  52.29 |  61.78 |  37.94 |  93.34 |
| ETHUSDT | 1h |  76.19 |  89.31 |  55.20 | 134.11 |
| ETHUSDT | 4h | 166.00 | 191.23 | 121.78 | 285.40 |
| SOLUSDT | 15m |  55.35 |  62.15 |  39.47 |  88.66 |
| SOLUSDT | 30m |  79.12 |  89.07 |  56.31 | 127.92 |
| SOLUSDT | 1h | 114.21 | 128.57 |  82.05 | 184.63 |
| SOLUSDT | 4h | 240.03 | 266.46 | 169.18 | 392.55 |
| XRPUSDT | 15m |  41.76 |  47.33 |  28.03 |  72.66 |
| XRPUSDT | 30m |  59.65 |  68.35 |  41.21 | 105.45 |
| XRPUSDT | 1h |  86.01 |  98.96 |  61.69 | 152.83 |
| XRPUSDT | 4h | 180.33 | 208.51 | 130.55 | 322.73 |
| ADAUSDT | 15m |  49.57 |  55.46 |  35.62 |  78.25 |
| ADAUSDT | 30m |  70.47 |  79.94 |  51.13 | 113.05 |
| ADAUSDT | 1h | 101.50 | 115.76 |  74.34 | 162.85 |
| ADAUSDT | 4h | 212.20 | 240.76 | 152.40 | 348.62 |

### 5.3 Interpretation (descriptive only; not tradability claims)

- **Cost-cushion ranking is consistent across all four intervals: SOL > ADA > XRP > ETH > BTC** (most cushion to least).
- **BTC has the tightest cost cushion** at every interval; round-trip 16 bps consumes ≈ 51% of median 15m ATR but only ≈ 11% at 4h.
- **Higher intervals (1h, 4h) have substantially more cushion than 15m / 30m** for every symbol; this is expected as a structural consequence of how ATR scales with interval size.
- **ADA / SOL / XRP are roughly comparable** in 4h cushion (0.060 / 0.067 / 0.077) — all materially better than BTC's 4h cushion (0.114) or ETH's 4h cushion (0.084).

**These observations are about cost cushion under §11.6 = 8 bps HIGH per side. They do NOT claim any of these symbols would be profitable for any strategy. They do NOT select a strategy. They do NOT optimize parameters.**

## 6. Opportunity-Rate / Expansion Results

### 6.1 Range-expansion frequency (events / 1 000 bars where range > 1.5× rolling-median range, 96-bar window)

| Symbol | 15m | 30m | 1h | 4h |
| --- | ---: | ---: | ---: | ---: |
| BTCUSDT | 242.96 | 256.31 | 262.49 | 259.41 |
| ETHUSDT | 232.86 | 242.45 | 251.77 | 250.52 |
| SOLUSDT | 206.54 | 217.05 | 222.56 | 223.24 |
| XRPUSDT | 212.65 | 226.45 | 233.78 | 244.17 |
| ADAUSDT | 200.95 | 211.14 | 217.73 | 223.69 |

### 6.2 Absolute-return-expansion frequency (events / 1 000 bars where |Δlog(close)| > 1.5× rolling median, 96-bar window)

| Symbol | 15m | 30m | 1h | 4h |
| --- | ---: | ---: | ---: | ---: |
| BTCUSDT | 322.48 | 329.67 | 335.80 | 349.62 |
| ETHUSDT | 321.61 | 328.71 | 334.65 | 350.54 |
| SOLUSDT | 317.52 | 323.53 | 328.65 | 335.94 |
| XRPUSDT | 317.03 | 323.34 | 330.19 | 338.54 |
| ADAUSDT | 320.68 | 321.34 | 326.07 | 339.10 |

### 6.3 Interpretation (descriptive only)

- **Range-expansion frequency:** BTC consistently has the most "outsized-range" bars relative to its own rolling median (≈ 24–26%), with ETH close behind, then XRP / SOL / ADA tied at the bottom (≈ 20–22%). This metric measures *bar-size variability* relative to recent baseline, not *absolute bar size*.
- **Absolute-return-expansion frequency:** much more uniform across symbols (≈ 32–35% of bars exceed 1.5× their rolling-median |return|). This descriptive metric does not strongly differentiate substrates.
- **Per-interval drift:** at higher intervals, expansion-event frequencies rise modestly (more "bursty" character at 4h than 15m), but the cross-symbol ranking is preserved.

**These metrics describe how often substrate behavior deviates from its own recent baseline. They are NOT entry signals, NOT thresholds, and NOT a basis for any strategy candidate.**

## 7. Trend / Regime Results

### 7.1 Fraction of bars with close above EMA(50)

| Symbol | 15m | 30m | 1h | 4h |
| --- | ---: | ---: | ---: | ---: |
| BTCUSDT | 0.5112 | 0.5112 | 0.5113 | 0.5028 |
| ETHUSDT | 0.5062 | 0.5055 | 0.5024 | 0.4765 |
| SOLUSDT | 0.4925 | 0.4871 | 0.4831 | 0.4760 |
| XRPUSDT | 0.4918 | 0.4851 | 0.4772 | 0.4456 |
| ADAUSDT | 0.4817 | 0.4752 | 0.4597 | 0.4109 |

### 7.2 Fraction of bars with EMA(50) > EMA(200) (where both EMAs are valid)

| Symbol | 15m | 30m | 1h | 4h |
| --- | ---: | ---: | ---: | ---: |
| BTCUSDT | 0.5089 | 0.4986 | 0.5170 | 0.5059 |
| ETHUSDT | 0.4987 | 0.4925 | 0.4761 | 0.4608 |
| SOLUSDT | 0.4826 | 0.4754 | 0.4763 | 0.4634 |
| XRPUSDT | 0.4756 | 0.4606 | 0.4461 | 0.4210 |
| ADAUSDT | 0.4575 | 0.4372 | 0.4131 | 0.3405 |

### 7.3 Interpretation (descriptive only)

- **BTC is the most cleanly trending substrate over the analysis window**: ≈ 50–52% of bars have close > EMA(50) and ≈ 50–52% have EMA(50) > EMA(200) at every interval. Balanced across regimes.
- **ADA shows the lowest sustained-uptrend frequency**, especially at higher intervals: at 4h only 41% of bars are above EMA(50) and only 34% have EMA(50) > EMA(200). ADA's analysis-window character is more bearish-tilted at HTF than the other four symbols.
- **XRP** also shows reduced HTF uptrend frequency (4h: 44.6% above EMA(50); 42.1% EMA(50) > EMA(200)) but less extreme than ADA.
- **SOL / ETH** are intermediate (47-50% range).

**These regime-frequency metrics are descriptive only. They are NOT regime filters. They do NOT specify when to be active or inactive. They do NOT authorize any strategy candidate.** The G1 Phase 4r failure mode (regime-gate-meets-setup intersection sparseness) remains a binding cautionary lesson against using regime-frequency descriptive evidence as a strategy-design input.

## 8. Wick / Noise Results

### 8.1 Trade-price-only wick proxies (no mark-price used)

| Symbol | Interval | Median upper wick frac | Median lower wick frac | Frac upper > 0.5 | Frac lower > 0.5 |
| --- | --- | ---: | ---: | ---: | ---: |
| BTCUSDT | 15m | 0.234 | 0.234 | 0.1554 | 0.1670 |
| BTCUSDT | 30m | 0.262 | 0.265 | 0.1604 | 0.1751 |
| BTCUSDT | 1h | 0.276 | 0.276 | 0.1650 | 0.1782 |
| BTCUSDT | 4h | 0.275 | 0.290 | 0.1591 | 0.1875 |
| ETHUSDT | 15m | 0.241 | 0.244 | 0.1565 | 0.1696 |
| ETHUSDT | 30m | 0.262 | 0.266 | 0.1621 | 0.1807 |
| ETHUSDT | 1h | 0.272 | 0.275 | 0.1654 | 0.1835 |
| ETHUSDT | 4h | 0.279 | 0.291 | 0.1629 | 0.1959 |
| SOLUSDT | 15m | 0.235 | 0.236 | 0.1498 | 0.1625 |
| SOLUSDT | 30m | 0.249 | 0.247 | 0.1540 | 0.1681 |
| SOLUSDT | 1h | 0.255 | 0.255 | 0.1554 | 0.1679 |
| SOLUSDT | 4h | 0.258 | 0.275 | 0.1490 | 0.1772 |
| XRPUSDT | 15m | 0.215 | 0.232 | 0.1425 | 0.1680 |
| XRPUSDT | 30m | 0.230 | 0.250 | 0.1485 | 0.1770 |
| XRPUSDT | 1h | 0.243 | 0.265 | 0.1482 | 0.1835 |
| XRPUSDT | 4h | 0.232 | 0.292 | 0.1422 | 0.2004 |
| ADAUSDT | 15m | 0.225 | 0.229 | 0.1465 | 0.1585 |
| ADAUSDT | 30m | 0.248 | 0.250 | 0.1509 | 0.1676 |
| ADAUSDT | 1h | 0.260 | 0.264 | 0.1539 | 0.1706 |
| ADAUSDT | 4h | 0.270 | 0.290 | 0.1510 | 0.1772 |

### 8.2 Interpretation (descriptive only; NOT stop-pathology diagnostics)

- **Median wick fractions are remarkably uniform across symbols** (medians ≈ 0.21–0.29). The substrate-level wick behavior at the median bar is similar.
- **Asymmetry: lower wicks tend to be slightly larger than upper wicks at higher intervals**, especially for XRP at 4h (median lower wick 0.292 vs upper 0.232). This is a descriptive observation about typical bar shape, not a directional bias.
- **Fraction of bars with extreme wicks (> 0.5)** ranges 0.14–0.20 across the table. BTC and ETH have slightly more "extreme upper wick" bars; XRP at 4h has the most "extreme lower wick" bars (≈ 20%).
- **No symbol shows wildly anomalous wick behavior** at the substrate level over this window.

**These are trade-price-only OHLC-derived wick proxies.** They are NOT stop-loss exit diagnostics. They are NOT a Phase 3s Q2 5m diagnostic rerun. They do NOT support any inference about how a strategy's stops would behave. **Per the Phase 4ae brief, mark-price-dependent wick / stop-pathology analysis is deferred under Phase 4ad Rule A.**

## 9. Funding Results

Funding event count, distribution, and tail behavior.

| Symbol | Events | Median (bps) | p25 (bps) | p75 (bps) | p05 (bps) | p95 (bps) | Frac positive | Frac negative | abs median (bps) | abs p95 (bps) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| BTCUSDT | 4 377 | 0.627 | 0.211 | 1.000 | -0.352 | 1.466 | 85.84% | 14.16% | 0.683 | 1.578 |
| ETHUSDT | 4 377 | 0.631 | 0.178 | 1.000 | -0.643 | 1.753 | 82.98% | 17.02% | 0.716 | 2.044 |
| SOLUSDT | 4 542 | 0.481 | -0.331 | 1.000 | -2.777 | 2.075 | 66.34% | 33.66% | 0.983 | 4.507 |
| XRPUSDT | 4 467 | 0.772 | -0.056 | 1.000 | -1.358 | 2.002 | 73.65% | 26.35% | 1.000 | 2.636 |
| ADAUSDT | 4 467 | 1.000 | 0.068 | 1.000 | -1.560 | 1.679 | 76.54% | 23.46% | 1.000 | 2.522 |

### 9.1 Interpretation (descriptive only)

- **BTC and ETH have the most stable / most-carry-positive funding regime:** median ≈ 0.63 bps positive; ≈ 83–86% of events are positive funding (long-side carry-cost / short-side carry-credit); abs p95 ≈ 1.6–2.0 bps. Tight tails.
- **SOL has the widest funding distribution:** p95 = 2.075 bps but p05 = -2.777 bps (largest negative tail); abs p95 = 4.507 bps (≈ 2.5× wider than BTC's 1.578). Only 66.3% of events are positive — funding flips sign more often than for BTC / ETH.
- **XRP and ADA** are intermediate: medians ≈ 0.77–1.00 bps positive; ≈ 74–77% positive; abs p95 ≈ 2.5 bps (somewhat wider than BTC/ETH but materially tighter than SOL).
- **The Phase 4aa idiosyncratic-risk concern about alt funding instability is empirically confirmed for SOL** at the descriptive level. SOL's funding is structurally less stable than the other four.

**Funding is descriptive substrate context only.** It is NOT a directional trigger. It is NOT a strategy signal. The D1-A Phase 3j MECHANISM PASS / FRAMEWORK FAIL governance is preserved verbatim; no D1-A rescue is implied by these descriptive funding distributions.

## 10. Liquidity / Notional Proxy Results

### 10.1 Median notional proxy (close × volume; per-bar USDT-equivalent)

| Symbol | 15m | 30m | 1h | 4h |
| --- | ---: | ---: | ---: | ---: |
| BTCUSDT |  90 993 451 | 191 795 067 | 402 292 612 | 1 801 872 933 |
| ETHUSDT |  58 169 802 | 122 116 072 | 259 310 336 | 1 166 280 002 |
| SOLUSDT |  15 062 151 |  31 431 920 |  65 869 962 |   287 212 773 |
| XRPUSDT |   5 865 478 |  12 143 547 |  25 251 894 |   108 305 064 |
| ADAUSDT |   2 349 994 |   4 889 734 |  10 186 032 |    43 821 046 |

### 10.2 Interpretation (descriptive only; NOT slippage estimates)

- **BTC median notional turnover dwarfs the alts** by ≈ 1–2 orders of magnitude.
- **ETH ≈ 0.65× BTC notional** (consistent with ETH being the second-largest USDⓈ-M perpetual).
- **SOL ≈ 0.16× BTC**, **XRP ≈ 0.06× BTC**, **ADA ≈ 0.025× BTC**. ADA is the thinnest by this proxy at every interval.
- **Per-interval pattern:** notional roughly doubles from 15m to 30m, doubles again to 1h, and roughly 4–5× to 4h (consistent with bar-size aggregation).

**Limitations preserved from the Phase 4ae brief:**

- **Kline notional is NOT order-book depth.** It cannot be used to infer executable slippage at a particular order size.
- **Kline volume includes maker + taker activity.** It does not disambiguate aggressive flow.
- **No slippage conclusions, no live execution conclusions, no fill-quality conclusions** are drawn here. ADA's lower kline notional indicates *lower observed traded volume*, which is *consistent with* lower top-of-book depth but does NOT prove it.
- **No floor / cap is invented.** Distributions reported only.

## 11. Cross-Symbol Feasibility Summary

This section provides a careful substrate-level comparison. **It is NOT a strategy verdict.** It is NOT a symbol selection for live trading. It is NOT a backtest. It does NOT authorize strategy work.

### 11.1 Substrate-feasibility ranking (descriptive only)

The following is a synthesis of §5–§10 metrics. Numbers are descriptive; rankings are NOT authorizations.

#### 11.1.1 Cost-cushion (round-trip 16 bps / median ATR(20))

Best to worst at every interval: **SOL > ADA > XRP > ETH > BTC**. BTC has the tightest cost cushion across all intervals; SOL has the most cushion. Higher timeframes have substantially more cushion than 15m / 30m.

#### 11.1.2 Range-expansion frequency (events / 1 000 bars > 1.5× rolling median range)

Best to worst (highest expansion-event rate) at most intervals: **BTC > ETH > XRP > SOL > ADA**. BTC has the most variable bar-size character (more "outsized" bars relative to its own median); ADA the most uniform.

#### 11.1.3 Absolute-return-expansion frequency

Roughly uniform across symbols (≈ 32–35%). Does not strongly differentiate substrates.

#### 11.1.4 Trend dominance (frac bars with EMA(50) > EMA(200))

Most uptrend-dominated to least, especially at HTF: **BTC > ETH ≈ SOL > XRP > ADA**. BTC alone shows ≈ 50–52% across intervals; ADA at 4h shows only 34%.

#### 11.1.5 Wick proxies

Cross-symbol differences are small at the median. Tail wick fractions are slightly elevated at higher intervals (especially XRP 4h lower wicks).

#### 11.1.6 Funding stability

Most stable to least (narrowest tails): **BTC ≈ ETH > ADA > XRP > SOL**. SOL's abs p95 = 4.5 bps is materially worse than BTC / ETH's 1.6–2.0 bps; SOL also has more frequent funding sign flips.

#### 11.1.7 Liquidity proxy (kline notional turnover)

Highest to lowest: **BTC > ETH > SOL > XRP > ADA**. BTC dwarfs the alts; ADA is by far the thinnest.

### 11.2 Substrate-feasibility composite observations

- **No single symbol is dominant on every dimension.** The ranking depends on which dimension is prioritized.
- **BTC has the worst cost-cushion but the best trend dominance, the highest range-expansion variability, the deepest liquidity proxy, and the most stable funding.** It is the most "boring but liquid" substrate.
- **SOL has the best cost-cushion but the worst funding stability and reduced trend-frequency at HTF.** It is the most "volatile but choppier-funding" substrate.
- **ADA has clean trade-price kline coverage (PASS), good cost-cushion, but the lowest trend dominance at HTF and the thinnest kline-notional proxy.** It looks distinct from BTC / ETH on substrate dimensions but its lower liquidity proxy and weaker HTF trend frequency are caveats.
- **XRP and ETH are intermediate** on most dimensions; XRP has slightly better cost-cushion than ETH but slightly weaker trend dominance.

### 11.3 What this does NOT say

- **This is NOT a strategy verdict for any symbol.** The "fires-and-loses" failure mode of C1 (Phase 4x) and the cost-fragility failure mode of R2 (Phase 2w) preclude inferring tradability from substrate cushion or substrate variability alone.
- **This is NOT a substrate selection for any future strategy candidate.** Selecting the best-cushion symbol (SOL) without first establishing a hypothesis with first-principles edge would repeat the Phase 4z-observed pattern of substrate-blind candidate selection.
- **This is NOT a backtest.** No strategy performance is computed.
- **This does NOT authorize any strategy work.** Any future fresh-hypothesis discovery memo or strategy-spec memo requires separate operator authorization analogous to Phase 4n / Phase 4t / Phase 4o / Phase 4u / Phase 4p / Phase 4v precedents.

## 12. Implications for Future Research

This section records possible future research directions. **Phase 4ae authorizes NONE of them.** Each requires separate operator authorization.

### 12.1 Possible directions

- **Option A — Remain paused (always procedurally valid).** The Phase 4ae descriptive metrics are recorded; the operator may choose not to advance.
- **Option B — Future docs-only Phase 4af fresh-hypothesis discovery memo limited to the most-promising substrate(s).** If the substrate evidence is judged sufficient (it is descriptive; the operator's judgment governs), a future fresh-hypothesis discovery memo could narrow attention. Such a memo must clear the Phase 4m 18-requirement validity gate and the Phase 4z proposed admissibility framework (which is a recommendation, not adopted governance). It must NOT be V2-prime / G1-prime / C1-prime / any rescue. It must NOT be substrate-blind. It must NOT use Phase 4ae forensic numbers as direct optimization targets.
- **Option C — Future narrower follow-up feasibility memo.** If the substrate evidence is judged ambiguous (e.g., asymmetry between cost-cushion and trend-dominance prevents clean ranking), a docs-only follow-up could refine the descriptive analysis (e.g., add intra-day-of-week patterns; conditional volatility regimes; or cross-symbol return-correlation descriptive context). Such a memo would itself be analysis-and-docs only and would NOT authorize strategy work.
- **Option D — Mark-price stop-domain feasibility under Phase 4ad Rule A.** If a future strategy hypothesis would require mark-price stop-domain analysis, a separately authorized memo could apply Phase 4ad Rule A (per-window exclusion test; conclusions labeled "conditional on valid mark-price coverage"). This would extend Phase 4ae but is NOT authorized here.

### 12.2 Phase 4ae primary recommendation

**Phase 4ae primary recommendation: Option A — remain paused.** Substrate-feasibility evidence has been recorded; no strategy candidate is implied. Any further forward motion is operator-driven.

**Phase 4ae conditional secondary: Option C — future narrower follow-up feasibility memo (only if separately authorized).** This option preserves the analysis-only posture and avoids the Phase 4z-observed pattern of substrate-blind candidate selection. **NOT recommended over remain-paused.**

**Phase 4ae NOT recommended:**

- **Option B — fresh-hypothesis discovery memo immediately** — premature; the Phase 4ae descriptive evidence does not by itself justify a candidate, and the project's six-failure topology (R2 / F1 / D1-A / V2 / G1 / C1) advises against substrate-driven candidate selection.

**Phase 4ae FORBIDDEN:**

- old-strategy alt-symbol rerun (Phase 4y / 4aa preserved);
- direct strategy-spec memo on alt symbols;
- backtest / paper / shadow / live;
- mark-price feasibility memo without Phase 4ad Rule A predeclaration.

## 13. Preserved Locks and Boundaries

Phase 4ae preserves every retained verdict and project lock verbatim. **No verdict revised. No project lock changed. No governance file amended (beyond the narrow `current-project-state.md` update).**

```text
H0           : FRAMEWORK ANCHOR (preserved)
R3           : BASELINE-OF-RECORD (preserved)
R1a          : RETAINED — NON-LEADING (preserved)
R1b-narrow   : RETAINED — NON-LEADING (preserved)
R2           : FAILED — §11.6 cost-sensitivity blocks (preserved)
F1           : HARD REJECT (preserved)
D1-A         : MECHANISM PASS / FRAMEWORK FAIL — other (preserved)
5m thread    : OPERATIONALLY CLOSED (Phase 3t; preserved)
V2           : HARD REJECT — terminal for V2 first-spec (preserved)
G1           : HARD REJECT — terminal for G1 first-spec (preserved)
C1           : HARD REJECT — terminal for C1 first-spec (preserved)

§11.6                       : 8 bps HIGH per side (preserved verbatim)
§1.7.3                      : project-level locks preserved
                               (0.25% risk; 2× leverage; one position max;
                               mark-price stops where applicable)
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance
                               (preserved)
Phase 4j §11                : metrics OI-subset partial-eligibility rule (preserved;
                               not invoked by Phase 4ae)
Phase 4k                    : V2 backtest-plan methodology (preserved)
Phase 4p                    : G1 strategy spec (preserved)
Phase 4q                    : G1 backtest-plan methodology (preserved)
Phase 4v                    : C1 strategy spec (preserved)
Phase 4w                    : C1 backtest-plan methodology (preserved)
Phase 4z recommendations    : remain recommendations only;
                               NOT adopted as binding governance by 4ae
Phase 4aa admissibility framework : remain recommendation only;
                                    NOT adopted as binding governance by 4ae
Phase 4ab recommendations   : remain recommendations only;
                               NOT adopted as binding governance by 4ae
Phase 4ac results           : remain data / integrity evidence only
Phase 4ad Rules A / B / C   : applied prospectively per Phase 4ad scope only;
                               Phase 4ae used Rule B1 verbatim as default
                               cross-symbol scope; Rule A NOT invoked
                               (mark-price deferred); Rule C-style PASS-only
                               cells included alongside Rule B1-governed cells.
                               No flag flipped. No manifest modified.
```

## 14. Explicit Non-Authorization Statement

Phase 4ae does NOT authorize:

- **Phase 4af** (any kind);
- **Phase 5;**
- **Phase 4 canonical;**
- **any other named successor phase;**
- **data acquisition;**
- **data download;**
- **API calls;**
- **endpoint calls;**
- **data modification;**
- **manifest creation;**
- **manifest modification;**
- **v003 or any other dataset version;**
- **backtests** (any kind);
- **strategy diagnostics;**
- **Q1–Q7 rerun;**
- **strategy specs;**
- **hypothesis specs;**
- **backtest plans;**
- **implementation** (no `src/prometheus/` modification);
- **old-strategy rescue** (R3 / R2 / F1 / D1-A / V2 / G1 / C1 on any symbol);
- **R3-prime / R2-prime / F1-prime / D1-A-prime / V2-prime / G1-prime / C1-prime / V1-D1 / F1-D1 / any cross-strategy hybrid;**
- **paper / shadow / live operation;**
- **live-readiness;**
- **deployment;**
- **production-key creation;**
- **authenticated APIs;**
- **private endpoints;**
- **public endpoint calls in code;**
- **user stream / WebSocket / listenKey lifecycle;**
- **exchange-write capability;**
- **MCP tooling;**
- **Graphify tooling;**
- **`.mcp.json` creation or modification;**
- **credentials;**
- **adoption of Phase 4z recommendations as binding governance;**
- **adoption of Phase 4aa admissibility framework as binding governance;**
- **adoption of Phase 4ab recommendations as binding governance;**
- **broadening of Phase 4ac results into binding cross-project governance;**
- **broadening of Phase 4ad Rules A / B / C beyond their prospective analysis-time scope;**
- **modification of any specialist governance file** (`docs/12-roadmap/phase-gates.md`, `docs/12-roadmap/technical-debt-register.md`, `docs/00-meta/ai-coding-handoff.md`, `docs/00-meta/implementation-ambiguity-log.md`, or any specialist document) **except** the narrow `docs/00-meta/current-project-state.md` update required to record Phase 4ae;
- **successor phase.**

**Phase 4ae output:**

- `scripts/phase4ae_alt_symbol_substrate_feasibility.py` (this analysis script; standalone; no network I/O; no API calls; no `prometheus.runtime/execution/persistence` imports);
- `docs/00-meta/implementation-reports/2026-05-04_phase-4ae_alt-symbol-substrate-feasibility-analysis.md` (this memo);
- `docs/00-meta/implementation-reports/2026-05-04_phase-4ae_closeout.md` (closeout);
- narrow update to `docs/00-meta/current-project-state.md` recording Phase 4ae (no broad documentation refresh);
- local outputs under gitignored `data/research/phase4ae/tables/` (NOT committed): `coverage.csv`, `kline_metrics.csv`, `funding_metrics.csv`, `omitted_datasets.csv`, `cross_symbol_rankings.csv`, `funding_rankings.csv`, plus `data/research/phase4ae/run_metadata.json`.

**Phase 4ae is preserved on its feature branch unless and until the operator separately instructs a merge.** main remains unchanged at `10f122e7be70a4080b181573e07a73c88227b0bb` after Phase 4ae branch creation.

---

**Phase 4ae is analysis-and-docs only. No source code under `src/prometheus/` modified. No tests modified. No existing scripts modified. No existing manifests modified. No data acquired. No data modified. No new manifest created. No backtest. No strategy diagnostic / Q1–Q7 rerun. No strategy candidate, hypothesis-spec, strategy-spec, or backtest-plan created. No old strategy rescued. No retained verdict revised. No project lock changed. No governance file amended (beyond the narrow `current-project-state.md` update). Phase 4z, Phase 4aa, Phase 4ab recommendations all remain recommendations only — not binding governance. Phase 4ac results remain data / integrity evidence only. Phase 4ad Rules A / B / C remain prospective future-use scope rules only; Phase 4ae used Rule B1 verbatim as default cross-symbol scope and deferred mark-price (Rule A) per brief recommendation. C1 / V2 / G1 first-specs remain terminally HARD REJECTED. R3 remains BASELINE-OF-RECORD. H0 remains FRAMEWORK ANCHOR. Recommended state: remain paused (primary; Option A). No next phase authorized.**
