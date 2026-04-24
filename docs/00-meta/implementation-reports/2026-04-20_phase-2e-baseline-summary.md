# Phase 2e — Baseline Backtest Summary

**Date:** 2026-04-20
**Window:** 2022-01-01 through 2026-03-31 UTC (51 months)
**Symbols:** BTCUSDT, ETHUSDT (USDⓈ-M perpetual futures)
**Strategy:** v1 breakout (locked Phase 3 defaults; **no tuning**, **no optimization**)
**Status:** Descriptive baseline statistics only. **NOT promotion evidence. NOT live-readiness evidence.**

---

## 0. Scope + disclaimers (read first)

- This report presents **descriptive statistics** produced by running the Phase-3-locked v1 breakout strategy over the widened BTC+ETH 2022-01 through 2026-03 dataset.
- **No parameter was tuned.** All thresholds (EMA periods, setup range/drift caps, breakout/stop buffers, stop-distance filter bounds, trailing multiplier, stagnation window, risk %, leverage cap, notional cap, fee/slippage assumptions) are the Phase 3 locked defaults.
- **Single configuration run** with `risk_fraction=0.0025`, `risk_usage_fraction=0.90`, `max_effective_leverage=2.0`, `max_notional_internal=100_000 USDT`, `taker_fee_rate=0.0005`, `slippage_bucket=MEDIUM`, `adapter=FAKE`. No sensitivity variants executed in Phase 2e (deferred per operator condition 8).
- **No walk-forward validation.** No rolling in-sample/out-of-sample split. No holdout. The full 51-month window is evaluated in a single pass with the Phase-3 engine.
- **No live-trading recommendation.** These numbers describe what the strategy would have done under perfect-execution assumptions (next-bar-open fills, 3 bps slippage MEDIUM, 5 bps taker fee) on historical data, not a forecast or a suggestion to deploy capital.
- **Accepted limitations** (verbatim on every `backtest_report.manifest.json`):
  - GAP-20260419-018: taker commission placeholder; `commissionRate` authenticated endpoint deferred to Phase 2d.
  - GAP-20260419-020: exchangeInfo 2026-04-19 snapshot used as proxy for the full range.
  - GAP-20260419-024: `leverageBracket` + `commissionRate` deferred; not binding at 2x leverage.
  - GAP-20260420-029: Binance `fundingRate` returns empty `markPrice` for pre-2024 events; `mark_price=None` is modeled; funding PnL is unaffected (computed from `funding_rate` + notional).

---

## 1. Dataset Inventory (v002 manifests)

Backfilled via `scripts/phase2e_backfill.py` on 2026-04-20.

| Dataset                                               | Version | Symbols | Range               | Rows / Events |
|-------------------------------------------------------|---------|---------|---------------------|---------------|
| `binance_usdm_btcusdt_15m`                            | v002    | BTCUSDT | 2022-01 → 2026-03   | 148,896 bars  |
| `binance_usdm_ethusdt_15m`                            | v002    | ETHUSDT | 2022-01 → 2026-03   | 148,896 bars  |
| `binance_usdm_btcusdt_1h_derived`                     | v002    | BTCUSDT | 2022-01 → 2026-03   | 37,224 bars   |
| `binance_usdm_ethusdt_1h_derived`                     | v002    | ETHUSDT | 2022-01 → 2026-03   | 37,224 bars   |
| `binance_usdm_btcusdt_markprice_15m`                  | v002    | BTCUSDT | 2022-01 → 2026-03   | 148,607 bars  |
| `binance_usdm_ethusdt_markprice_15m`                  | v002    | ETHUSDT | 2022-01 → 2026-03   | 148,703 bars  |
| `binance_usdm_btcusdt_funding`                        | v002    | BTCUSDT | 2022-01 → 2026-03   | 4,653 events  |
| `binance_usdm_ethusdt_funding`                        | v002    | ETHUSDT | 2022-01 → 2026-03   | 4,653 events  |
| `exchange_info_snapshot` (2026-04-19T21-22-59Z)       | —       | both    | proxy (GAP-020)     | 1 snapshot    |

- All Phase 2b/2c v001 manifests preserved on disk as audit trail.
- All v002 manifests + v002 data files are **git-ignored** under `data/`.
- Invalid-window counts (per-ingest result): **0** across all four kline/mark-price datasets for both symbols.
- Derived 1h bars produced without any partial-bucket invalid windows (0 across all 8 v002 datasets).

### Funding `mark_price` coverage (per GAP-20260420-029)

| Symbol  | Total events | `mark_price` populated | `mark_price` is None |
|---------|--------------|------------------------|----------------------|
| BTCUSDT | 4,653        | 2,648                  | 2,005                |
| ETHUSDT | 4,653        | 2,648                  | 2,005                |

The ~2000 None events correspond to pre-2024 funding events where Binance returns `"markPrice": ""`. The backtester's funding accrual uses `funding_rate` and position notional only; None `mark_price` does not affect funding math.

---

## 2. Baseline Backtest Configuration

| Parameter                        | Value          | Source                 |
|----------------------------------|----------------|------------------------|
| experiment_name                  | phase-2e-baseline | script default      |
| run_id                           | `<UTC timestamp>` | per-run              |
| symbols                          | (BTCUSDT, ETHUSDT) | operator allowlist  |
| window_start_ms                  | 1_640_995_200_000 (2022-01-01 UTC) | plan |
| window_end_ms                    | 1_775_001_600_000 (2026-04-01 UTC) | plan |
| sizing_equity_usdt               | 10,000.0       | GAP-021                |
| risk_fraction                    | 0.0025         | Phase 3 locked default |
| risk_usage_fraction              | 0.90           | GAP-022                |
| max_effective_leverage           | 2.0            | v1 locked              |
| max_notional_internal_usdt       | 100,000.0      | GAP-023                |
| taker_fee_rate                   | 0.0005         | GAP-018 primary        |
| slippage_bucket                  | MEDIUM (3 bps) | Phase 3 locked default |
| adapter                          | FAKE           | Phase 3 locked enum    |

---

## 3. Baseline Results (per symbol, 2022-01 → 2026-03)

Run ID: `2026-04-20T23-58-39Z`.

### BTCUSDT

- Total trades: **41**
- Long / Short split: **21** / **20**
- Win / Loss count: 12 / 29
- Win rate: **29.27%**
- Expectancy (per-trade avg R): **−0.43**
- Profit factor: **0.32**
- Total net PnL: **−394.87 USDT** (**−3.95%** of 10,000 starting equity)
- Max drawdown: **−424.23 USDT** (**−4.23%**)
- Fees paid: **197.73 USDT** (entry+exit combined)
- Funding net: **−1.13 USDT**
- Exit-reason distribution: STOP=**22** / TRAILING_BREACH=**0** / STAGNATION=**19** / END_OF_DATA=**0**
- Stop gap-through events: **0**

### ETHUSDT

- Total trades: **47**
- Long / Short split: **18** / **29**
- Win / Loss count: 11 / 36
- Win rate: **23.40%**
- Expectancy (per-trade avg R): **−0.39**
- Profit factor: **0.42**
- Total net PnL: **−407.31 USDT** (**−4.07%** of 10,000 starting equity)
- Max drawdown: **−490.62 USDT** (**−4.89%**)
- Fees paid: **177.04 USDT**
- Funding net: **+0.61 USDT**
- Exit-reason distribution: STOP=**35** / TRAILING_BREACH=**1** / STAGNATION=**11** / END_OF_DATA=**0**
- Stop gap-through events: **0**

---

## 4. Signal Funnel (overall, per symbol)

Per-(symbol, year, month) funnel counts are available in
`data/derived/backtests/phase-2e-baseline/<run_id>/<SYMBOL>/funnel_total.json`
and `monthly_breakdown.parquet` (git-ignored). Overall totals:

| Stage                              | BTCUSDT | ETHUSDT |
|------------------------------------|---------|---------|
| 15m bars loaded                    | 148,896 | 148,896 |
| 1h bars loaded                     | 37,224  | 37,224  |
| Warmup excluded (15m)              | 29      | 29      |
| Warmup excluded (1h-equivalent)    | 811     | 811     |
| **Decision bars evaluated**        | **148,085** | **148,085** |
| Bias long / short / neutral        | 48,280 / 45,264 / 54,541 | 44,744 / 47,824 / 55,517 |
| Valid 8-bar setups detected        | 8,064   | 7,837   |
| Long breakout candidates           | 327     | 308     |
| Short breakout candidates          | 294     | 320     |
| Reject — neutral bias              | 54,541  | 55,517  |
| Reject — no valid setup            | 85,480  | 84,731  |
| Reject — no close-break            | 7,443   | 7,209   |
| Reject — TR < ATR                  | 216     | 173     |
| Reject — close location            | 157     | 173     |
| Reject — ATR regime                | 4       | 21      |
| Reject — stop-distance filter      | 203     | 214     |
| Reject — sizing failed             | 0       | 0       |
| End-of-data (no fill)              | 0       | 0       |
| **Entry intents produced**         | **41**  | **47**  |
| Trades filled / closed             | 41      | 47      |

Accounting invariant (per Phase 3 diagnostic test): decision_bars_evaluated = sum of rejection buckets + entry_intents_produced.

- BTCUSDT: 54,541 + 85,480 + 7,443 + 216 + 157 + 4 + 203 + 0 + 0 + 41 = **148,085** ✓
- ETHUSDT: 55,517 + 84,731 + 7,209 + 173 + 173 + 21 + 214 + 0 + 0 + 47 = **148,085** ✓

Sizing filter never bound (0 rejections for both symbols) — at 10k equity, 0.25% risk, 2x leverage cap, 100k notional cap, and BTCUSDT/ETHUSDT stepSize = 0.001, every candidate that reached sizing produced a valid `quantity > minQty` and `notional > minNotional`.

---

## 5. Per-year rollup

| Year | Symbol  | Trades | Long | Short | Wins | Losses | Net PnL (USDT) | Fees (USDT) | Funding (USDT) | Exit: STOP/TRAIL/STAG |
|------|---------|--------|------|-------|------|--------|----------------|-------------|----------------|-----------------------|
| 2022 | BTCUSDT | 10     | 4    | 6     | 4    | 6      | −66.96         | 45.89       | +1.18          | 2 / 0 / 8             |
| 2022 | ETHUSDT | 12     | 2    | 10    | 4    | 8      | −11.17         | 42.33       | +0.25          | 11 / 1 / 0            |
| 2023 | BTCUSDT | 15     | 7    | 8     | 5    | 10     | −118.63        | 83.51       | −1.24          | 9 / 0 / 6             |
| 2023 | ETHUSDT | 15     | 7    | 8     | 2    | 13     | −263.91        | 75.88       | +0.45          | 11 / 0 / 4            |
| 2024 | BTCUSDT | 8      | 5    | 3     | 1    | 7      | −153.57        | 31.21       | −0.79          | 6 / 0 / 2             |
| 2024 | ETHUSDT | 6      | 4    | 2     | 1    | 5      | −77.63         | 21.60       | −0.26          | 4 / 0 / 2             |
| 2025 | BTCUSDT | 7      | 5    | 2     | 2    | 5      | −51.07         | 34.57       | −0.28          | 5 / 0 / 2             |
| 2025 | ETHUSDT | 12     | 5    | 7     | 3    | 9      | −96.69         | 32.20       | +0.12          | 7 / 0 / 5             |
| 2026 | BTCUSDT | 1      | 0    | 1     | 0    | 1      | −4.63          | 2.55        | 0.00           | 0 / 0 / 1             |
| 2026 | ETHUSDT | 2      | 0    | 2     | 1    | 1      | +42.08         | 5.02        | +0.06          | 2 / 0 / 0             |

Per-month detail in `data/derived/backtests/phase-2e-baseline/<run_id>/<SYMBOL>/monthly_breakdown.parquet` (git-ignored).

---

## 6. Cost-impact breakdown (per symbol)

| Metric                         | BTCUSDT    | ETHUSDT    |
|--------------------------------|------------|------------|
| Net PnL (USDT)                 | **−394.87** | **−407.31** |
| Total fees (entry+exit)        | 197.73     | 177.04     |
| Total funding (signed)         | −1.13      | +0.61      |
| Gross PnL (= net + fees − funding) | −198.27 | −230.88    |

Slippage is implicit in entry/exit fill prices (3 bps × notional × 2 fills); the engine does not emit a separate "total slippage" field. Funding net is small in both symbols because many 2022–2023 events have `mark_price=None` (GAP-029) but `funding_rate` is applied normally — the small magnitudes reflect the v1 holding style (short-duration, small notional) rather than missing data.

---

## 7. Interpretation

**Observed, not a conclusion.** The locked v1 breakout with Phase 3 defaults, applied to 51 months of real BTCUSDT + ETHUSDT 15m data, produced **88 trades (41 BTC + 47 ETH)** with both symbols net negative (**−3.95%** BTC / **−4.07%** ETH) under the accepted-limitation assumptions (2026-04-19 exchangeInfo proxy, placeholder 5 bps taker, MEDIUM 3 bps slippage, funding applied from `funding_rate` with `mark_price=None` handled cleanly for pre-2024 events).

Key structural observations (no parameter-change implied):

1. **Trade frequency**: ~1 trade per symbol per ~3 months on average. This is a property of the strict six-condition trigger + stop-distance band, not a bug. Phase 3's single-month 2026-03 smoke had 0 trades; widening to 51 months produces the expected low frequency.

2. **Dominant rejection**: "no valid setup" alone accounts for ~58% of all decision bars (BTC 85,480 / 148,085 ≈ 57.7%; ETH 84,731 / 148,085 ≈ 57.2%). The 8-bar compression + drift filter is doing the heavy lifting, consistent with Phase 3's funnel shape extrapolated to a wider window.

3. **Sizing never binds**: 0 sizing rejections on both symbols. At 10k equity, 0.25% risk, 2x leverage cap, and 100k notional cap, every candidate that survived the earlier filters produced a valid quantity/notional.

4. **Gap-through stops**: 0 on both symbols. MEDIUM slippage (3 bps) at 2x leverage on BTC/ETH mark-price bars did not trigger any adverse-open stop fills in 51 months.

5. **Per-year: losses are concentrated in 2023 / 2024** for both symbols. BTC's worst year is 2024 (−153 USDT on 8 trades). ETH's worst year is 2023 (−264 USDT on 15 trades). 2026-Q1 is nearly flat by design (only ~3 months of evaluation). None of this is a forecast.

6. **Expectancy**: BTC −0.43 R/trade, ETH −0.39 R/trade. Profit factor: BTC 0.32, ETH 0.42. Win rate: BTC 29.3%, ETH 23.4%. **These numbers describe the baseline; they do not support any threshold-modification proposal.** Follow-up work (walk-forward, sensitivity, exit-model comparison) is a separate future phase.

7. **Exit-reason shape**: BTC — 22 STOP, 0 TRAILING, 19 STAGNATION, 0 END_OF_DATA. ETH — 35 STOP, 1 TRAILING, 11 STAGNATION, 0 END_OF_DATA. ETH took more stops; BTC more stagnations. Zero trailing breaches except one ETH event — consistent with losses preventing MFE from reaching +2R where trailing would engage.

---

## 8. Reproducibility

To reproduce these numbers on a clean checkout with the same data:

```bash
# 1. Backfill (same v002 outputs).
uv run python scripts/phase2e_backfill.py

# 2. Baseline backtest with a fresh run_id.
uv run python scripts/phase2e_baseline_backtest.py
```

Both scripts are deterministic given identical on-disk data. The `run_id` is a UTC timestamp chosen at script start; trade records contain a UUID suffix for uniqueness but the per-trade OHLC entry/exit/PnL values are deterministic.

---

## 9. Related documents

- `docs/00-meta/implementation-reports/2026-04-20_phase-2e_gate-1-plan.md` — approved Phase 2e plan
- `docs/00-meta/implementation-reports/2026-04-20_phase-2e_gate-2-review.md` — Gate 2 pre-commit review
- `docs/00-meta/implementation-reports/2026-04-19_phase-3_gate-2-review.md` — Phase 3 Gate 2 (engine + diagnostic)
- `docs/00-meta/implementation-ambiguity-log.md` — especially GAP-20260420-029 (empty markPrice resolution)
- `docs/03-strategy-research/v1-breakout-strategy-spec.md` — authoritative strategy spec
- `docs/07-risk/position-sizing-framework.md` — sizing pipeline

---

**End of baseline summary. Descriptive baseline statistics. Not promotion evidence. Not live-readiness evidence.**
