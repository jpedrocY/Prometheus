# Phase 2g — Wave-1 Variant Comparison (R Window)

**Working directory:** `C:\Prometheus`
**Branch:** `phase-2g/wave1-variant-execution`
**Window:** Research window R = 2022-01-01 → 2025-01-01 UTC (36 months, exclusive end)
**Datasets:** v002 manifests (frozen from Phase 2e, no changes)
**Cost model:** taker = 5 bps, slippage = MEDIUM (3 bps), funding = historical join — same as Phase 2e baseline
**Stop trigger:** MARK_PRICE (live-aligned default; mark-price sensitivity is conditional on promotion per §10.6 / GAP-20260424-032)
**Date:** 2026-04-24
**Authority:** Phase 2f Gate 1 plan §§ 8, 10, 11 (pre-declared promotion / rejection thresholds; no post-hoc loosening per §11.3.5)

This report is the descriptive comparison of the four operator-approved Phase 2g wave-1 variants (H-A1, H-B2, H-C1, H-D3) against the H0 control, computed on the research window R. Numbers come from `data/derived/backtests/phase-2g-wave1-*-r/<run_id>/<SYMBOL>/` (git-ignored). The H0 row is the baseline configuration (V1BreakoutConfig defaults — bit-for-bit identical to Phase 2e Phase 3 defaults), re-run on R only so the R-window comparison is apples-to-apples.

The Phase 2e FULL-window baseline at `data/derived/backtests/phase-2e-baseline/2026-04-20T23-58-39Z/` remains untouched and is the permanent control.

---

## 1. Headline — wave-1 R-window summary

| Variant | Symbol  | Trades | Long / Short | Win rate | Expectancy (R) | Profit factor | Net PnL (% of 10k) | Max DD |
|---------|---------|-------:|-------------:|---------:|---------------:|--------------:|-------------------:|-------:|
| H0      | BTCUSDT |     33 |      16 / 17 |   30.30% |        −0.459  |          0.26 |             −3.39% | −3.67% |
| H0      | ETHUSDT |     33 |      13 / 20 |   21.21% |        −0.475  |          0.32 |             −3.53% | −4.13% |
| H-A1    | BTCUSDT |     13 |       5 /  8 |   15.38% |        −0.831  |          0.10 |             −2.42% | −2.21% |
| H-A1    | ETHUSDT |     11 |       6 /  5 |   18.18% |        −0.360  |          0.49 |             −0.89% | −1.75% |
| H-B2    | BTCUSDT |     69 |      36 / 33 |   30.43% |        −0.326  |          0.43 |             −5.07% | −5.53% |
| H-B2    | ETHUSDT |     57 |      27 / 30 |   24.56% |        −0.440  |          0.35 |             −5.65% | −6.53% |
| H-C1    | BTCUSDT |     30 |      15 / 15 |   26.67% |        −0.499  |          0.24 |             −3.35% | −3.28% |
| H-C1    | ETHUSDT |     32 |      14 / 18 |   15.62% |        −0.495  |          0.29 |             −3.56% | −3.99% |
| H-D3    | BTCUSDT |     33 |      16 / 17 |   30.30% |        −0.475  |          0.25 |             −3.51% | −3.79% |
| H-D3    | ETHUSDT |     33 |      13 / 20 |   21.21% |        −0.491  |          0.31 |             −3.64% | −4.20% |

`PF` for the Phase 2e FULL-window baseline was BTC 0.32 and ETH 0.42; the R-window subset has lower PF on both symbols because the worst-month subperiods (BTC 2024H1, ETH 2023H1/H2) sit inside R while some better months sit in V.

---

## 2. Deltas vs H0 (R window)

Each row is one variant on one symbol; deltas are variant minus H0.

### BTCUSDT

| Variant | Trades       | Δ trades | Expectancy   | Δ expR  | PF        | Δ PF    | maxDD   | Δ maxDD (pp) | maxDD ratio |
|---------|-------------:|---------:|-------------:|--------:|----------:|--------:|--------:|-------------:|------------:|
| H0      |           33 |     —    |       −0.459 |    —    |      0.26 |    —    | 3.67%   |      —       |    1.000×   |
| H-A1    |           13 |  −60.6%  |       −0.831 |  −0.372 |      0.10 |  −0.16  | 2.21%   |   −1.46pp    |    0.602×   |
| H-B2    |           69 | +109.1%  |       −0.326 |  +0.133 |      0.43 |  +0.17  | 5.53%   |   +1.86pp    |    1.505×   |
| H-C1    |           30 |   −9.1%  |       −0.499 |  −0.040 |      0.24 |  −0.02  | 3.28%   |   −0.39pp    |    0.894×   |
| H-D3    |           33 |   +0.0%  |       −0.475 |  −0.016 |      0.25 |  −0.01  | 3.79%   |   +0.12pp    |    1.033×   |

### ETHUSDT

| Variant | Trades       | Δ trades | Expectancy   | Δ expR  | PF        | Δ PF    | maxDD   | Δ maxDD (pp) | maxDD ratio |
|---------|-------------:|---------:|-------------:|--------:|----------:|--------:|--------:|-------------:|------------:|
| H0      |           33 |     —    |       −0.475 |    —    |      0.32 |    —    | 4.13%   |      —       |    1.000×   |
| H-A1    |           11 |  −66.7%  |       −0.360 |  +0.115 |      0.49 |  +0.17  | 1.75%   |   −2.38pp    |    0.424×   |
| H-B2    |           57 |  +72.7%  |       −0.440 |  +0.035 |      0.35 |  +0.03  | 6.53%   |   +2.40pp    |    1.581×   |
| H-C1    |           32 |   −3.0%  |       −0.495 |  −0.020 |      0.29 |  −0.03  | 3.99%   |   −0.14pp    |    0.966×   |
| H-D3    |           33 |   +0.0%  |       −0.491 |  −0.016 |      0.31 |  −0.01  | 4.20%   |   +0.07pp    |    1.017×   |

(All `maxDD` values are absolute pct-of-equity; maxDD ratio = |variant_maxDD| / |H0_maxDD|.)

---

## 3. Per-fold breakdown — Phase 2f §11.2 approved scheme

Five rolling folds, 12-month train / 6-month test, stepping 6 months — all five test windows fit inside R. Per Phase 2f §11.2 a 36-month R window with 5 stepping-6m tests requires fold 1 to begin at month 6 of R, leaving fold 1 with a 6-month notional partial-train front edge (the only arrangement that places exactly 5 stepping-6m tests entirely within R; the alternative "5 folds with 12m train each + step 6m" extends into V, which is forbidden by §11.3). Folds 2–5 each have a full 12-month notional train. No tuning happens in Phase 2g — variants are pre-declared and single-axis — so the train windows are notional; the per-fold metrics that matter are computed on each test window.

| Fold | Test window         | Notional train window                   |
|-----:|---------------------|-----------------------------------------|
|   F1 | 2022-07 → 2022-12   | 2022-01 → 2022-06 (6m partial — front edge) |
|   F2 | 2023-01 → 2023-06   | 2022-01 → 2022-12 (12m)                 |
|   F3 | 2023-07 → 2023-12   | 2022-07 → 2023-06 (12m)                 |
|   F4 | 2024-01 → 2024-06   | 2023-01 → 2023-12 (12m)                 |
|   F5 | 2024-07 → 2024-12   | 2023-07 → 2024-06 (12m)                 |

Trade-count and expectancy (R/trade) per test fold, by variant and symbol. Bucketing is on `entry_fill_time_ms`.

### BTCUSDT — trade count per test fold

| Variant |  F1 |  F2 |  F3 |  F4 |  F5 | Σ test |
|---------|----:|----:|----:|----:|----:|-------:|
| H0      |   6 |   9 |   6 |   4 |   4 |     29 |
| H-A1    |   4 |   5 |   0 |   1 |   1 |     11 |
| H-B2    |   9 |  13 |  14 |  14 |  10 |     60 |
| H-C1    |   4 |   6 |   6 |   4 |   5 |     25 |
| H-D3    |   6 |   9 |   6 |   4 |   4 |     29 |

(Σ test < total R trades because months 2022-01 → 2022-06 sit in fold 1's notional train front edge; H0 BTC's 33 R-window trades = 29 test-fold + 4 in 2022H1 not covered by any 5-rolling-fold test window.)

### BTCUSDT — expectancy (R/trade) per test fold

| Variant |    F1   |    F2   |    F3   |    F4   |    F5   |
|---------|--------:|--------:|--------:|--------:|--------:|
| H0      |  −0.48  |  −0.24  |  −0.52  |  −1.03  |  −0.69  |
| H-A1    |  −1.04  |  −0.44  |  +0.00  |  −1.38  |  −1.32  |
| H-B2    |  −0.37  |  −0.47  |  −0.26  |  −0.38  |  −0.41  |
| H-C1    |  −0.75  |  −0.00  |  −0.58  |  −1.03  |  −0.68  |
| H-D3    |  −0.48  |  −0.24  |  −0.57  |  −1.03  |  −0.76  |

### ETHUSDT — trade count per test fold

| Variant |  F1 |  F2 |  F3 |  F4 |  F5 | Σ test |
|---------|----:|----:|----:|----:|----:|-------:|
| H0      |   8 |   7 |   8 |   2 |   4 |     29 |
| H-A1    |   1 |   3 |   3 |   1 |   1 |      9 |
| H-B2    |  11 |  12 |  17 |   5 |   6 |     51 |
| H-C1    |   7 |   5 |   8 |   2 |   7 |     29 |
| H-D3    |   8 |   7 |   8 |   2 |   4 |     29 |

### ETHUSDT — expectancy (R/trade) per test fold

| Variant |    F1   |    F2   |    F3   |    F4   |    F5   |
|---------|--------:|--------:|--------:|--------:|--------:|
| H0      |  −0.26  |  −0.75  |  −0.81  |  −0.84  |  −0.44  |
| H-A1    |  −1.28  |  −0.57  |  −1.32  |  −0.34  |  −0.57  |
| H-B2    |  −0.10  |  −0.62  |  −0.74  |  −0.52  |  −0.37  |
| H-C1    |  −0.41  |  −0.72  |  −0.95  |  −0.84  |  −0.27  |
| H-D3    |  −0.29  |  −0.79  |  −0.81  |  −0.84  |  −0.44  |

### Fold-consistency notes (5 rolling folds)

- **H0 BTC**: expectancy is negative on all 5 folds; F4 (2024H1) is the worst at −1.03 R. Pattern unchanged from Phase 2e's 2024 worst-year flag.
- **H0 ETH**: expectancy is negative on all 5 folds; F2/F3/F4 (2023H1, 2023H2, 2024H1) are the worst.
- **H-A1**: trade count collapses (Σ test = 11 BTC, 9 ETH) and expectancy is severely negative on most folds; one fold (BTC F3) has zero trades. Fold-consistency cannot be evaluated meaningfully.
- **H-B2**: trades distribute evenly across all 5 folds (BTC: 9 / 13 / 14 / 14 / 10; ETH: 11 / 12 / 17 / 5 / 6) but expectancy is **negative on every fold of every symbol**. Quantity is consistent; quality is consistently bad.
- **H-C1**: per-fold counts mirror H0 closely on both symbols (a few-trade differences); expectancies sit between H0 and slightly worse on most folds.
- **H-D3**: identical fold-level entry/exit counts to H0 (entries unchanged by definition; only intra-trade stop trajectory differs); per-fold expectancies sit at H0 or marginally worse.

A variant that "wins only one fold" is the discipline check Phase 2f §11.2 specifies; **no variant wins (positive expR on) any fold on BTC**, and on ETH only some F1 readings (H0 +0.39, H-A1 +1.94, H-B2 +0.16, H-C1 +0.57) cross zero. H-A1 ETH F1's +1.94 is on **one** trade and is not a sample-size-credible signal.

### 3.A Supplemental appendix — 6 non-overlapping half-year folds

This is **not** the Phase 2f §11.2 approved scheme. It is provided as a descriptive complement so every R month is covered (the §11.2 5-rolling-folds scheme leaves 2022-01 → 2022-06 inside fold 1's notional train front edge and uncovered by any test fold). It must not be used to rank or promote variants. The Gate 2 §10.3 / §10.4 classification is computed against the full R window (per §11.3); the 5 rolling folds are the consistency check.

#### BTCUSDT — half-year supplemental

| Variant |  2022H1  |  2022H2  |  2023H1  |  2023H2  |  2024H1  |  2024H2  | trades total |
|---------|---------:|---------:|---------:|---------:|---------:|---------:|-------------:|
| H0      |   4 / −0.024 |   6 / −0.481 |   9 / −0.238 |   6 / −0.524 |   4 / −1.025 |   4 / −0.693 |   33 |
| H-A1    |   2 / −0.869 |   4 / −1.038 |   5 / −0.442 |   0 /  0.000 |   1 / −1.381 |   1 / −1.320 |   13 |
| H-B2    |   9 / −0.022 |   9 / −0.365 |  13 / −0.465 |  14 / −0.257 |  14 / −0.379 |  10 / −0.406 |   69 |
| H-C1    |   5 / −0.195 |   4 / −0.752 |   6 / −0.003 |   6 / −0.580 |   4 / −1.031 |   5 / −0.675 |   30 |
| H-D3    |   4 / −0.024 |   6 / −0.481 |   9 / −0.238 |   6 / −0.569 |   4 / −1.025 |   4 / −0.758 |   33 |

Cells are `n / expR (R/trade)`.

#### ETHUSDT — half-year supplemental

| Variant |  2022H1  |  2022H2  |  2023H1  |  2023H2  |  2024H1  |  2024H2  | trades total |
|---------|---------:|---------:|---------:|---------:|---------:|---------:|-------------:|
| H0      |   4 / +0.390 |   8 / −0.257 |   7 / −0.750 |   8 / −0.810 |   2 / −0.836 |   4 / −0.445 |   33 |
| H-A1    |   2 / +1.940 |   1 / −1.281 |   3 / −0.566 |   3 / −1.316 |   1 / −0.345 |   1 / −0.569 |   11 |
| H-B2    |   6 / +0.157 |  11 / −0.104 |  12 / −0.620 |  17 / −0.743 |   5 / −0.520 |   6 / −0.370 |   57 |
| H-C1    |   3 / +0.571 |   7 / −0.410 |   5 / −0.717 |   8 / −0.946 |   2 / −0.836 |   7 / −0.266 |   32 |
| H-D3    |   4 / +0.390 |   8 / −0.290 |   7 / −0.788 |   8 / −0.810 |   2 / −0.836 |   4 / −0.445 |   33 |

Half-year notes (descriptive only):

- **2022H1** is the only consistent winning sub-period across all variants on ETH and a near-zero sub-period on BTC. It is also the sub-period that the §11.2 5-rolling-folds scheme leaves out of every test fold (inside fold 1's notional train front edge); having it here as a supplemental cut makes that visible.
- **2023H1 / 2023H2 / 2024H1** are persistently negative on both symbols across every variant — the same regime that drove the Phase 2e baseline ETH 2023 / BTC 2024 worst-year flags.
- The supplemental view does not change the §10.3 disqualification verdict — that verdict is computed on the full R window, not on per-fold subsets.

---

## 4. Signal-funnel comparison

Funnel counts come from each variant's `funnel_total.json`. The funnel walks the full 51-month dataset; the engine then filters fills to the R window. Differences in `valid_setup_windows_detected` and `entry_intents_produced` reflect the variant's axis change.

### Funnel deltas vs H0 (full 51-month dataset, both symbols summed)

| Funnel stage                     | H0      | H-A1   | H-B2   | H-C1   | H-D3   |
|----------------------------------|--------:|-------:|-------:|-------:|-------:|
| Decision bars evaluated          | 296,170 | 296,168 | 296,170 | 296,170 | 296,170 |
| Bias neutral (rejected)          | 110,058 | 110,058 | 110,058 | (Δ)*   | 110,058 |
| Valid setup windows detected     |  15,901 | 13,094 |  15,901 | (Δ)*   |  15,901 |
| Long + short breakout candidates |   1,249 |  1,003 |  1,249  | (Δ)*   |   1,249 |
| Entry intents produced           |      88 |      45 |    180  | (Δ)*   |      88 |

\*H-C1 changes the EMA pair, which changes the bias counts upstream of the setup filter; the funnel deltas for H-C1 differ from baseline at the bias step. H-D3 changes only intra-trade stop trajectory, so the funnel is identical to H0 (entries unchanged; only stops differ). Per-symbol funnel JSONs in each run directory carry the full numbers.

The funnel's `entry_intents_produced` count is NOT the same as the engine's `trades_filled` after window filtering (R is 36 of 51 months); the engine's trade counts in §1 are the authoritative R-window comparison.

---

## 5. Trade-frequency sanity-check appendix (per Phase 2f Gate 1 §7.5)

Required diagnostics per symbol, per variant. Numbers computed from the per-variant `trade_log.json` against the full R window.

### BTCUSDT — frequency diagnostics

| Variant | Trades / month — min | median | max | mean    | Zero-trade months R | Median hold (15m bars) | Setup→entry %  | Candidate→entry %    |
|---------|---------------------:|-------:|----:|--------:|--------------------:|-----------------------:|---------------:|---------------------:|
| H0      |                    0 |      1 |   3 |  0.917  |             16 / 36 |                      8 |  41/8,064=0.51% |  41/621=6.60%       |
| H-A1    |                    0 |      0 |   3 |  0.361  |             24 / 36 |                      9 |  21/6,495=0.32% |  21/471=4.46%       |
| H-B2    |                    0 |      2 |   6 |  1.917  |              7 / 36 |                      8 |  98/8,064=1.22% |  98/789=12.42%      |
| H-C1    |                    0 |      1 |   4 |  0.833  |             19 / 36 |                      8 | (variant funnel)|(variant funnel)     |
| H-D3    |                    0 |      1 |   3 |  0.917  |             16 / 36 |                      8 |  41/8,064=0.51% |  41/621=6.60%       |

(H-C1's funnel ratios differ because EMA-pair change shifts the bias upstream of the setup filter; see H-C1 funnel JSON. For H-A1 and H-B2 the conversion-rate numerators are full-51-month entries from the variant's funnel; the denominators are the variant's full-51-month setup/candidate counts, so ratios are like-for-like comparable.)

### ETHUSDT — frequency diagnostics

| Variant | Trades / month — min | median | max | mean    | Zero-trade months R | Median hold (15m bars) | Setup→entry %  | Candidate→entry %    |
|---------|---------------------:|-------:|----:|--------:|--------------------:|-----------------------:|---------------:|---------------------:|
| H0      |                    0 |      1 |   2 |  0.917  |             14 / 36 |                      7 |  47/7,837=0.60% |  47/628=7.48%       |
| H-A1    |                    0 |      0 |   2 |  0.306  |             24 / 36 |                      8 |  18/6,236=0.29% |  18/468=3.85%       |
| H-B2    |                    0 |      1 |   5 |  1.583  |              9 / 36 |                      6 |  92/7,837=1.17% |  92/799=11.51%      |
| H-C1    |                    0 |      1 |   3 |  0.889  |             16 / 36 |                      7 | (variant funnel)|(variant funnel)     |
| H-D3    |                    0 |      1 |   2 |  0.917  |             14 / 36 |                      7 |  47/7,837=0.60% |  47/628=7.48%       |

Interpretation per Phase 2f §7.5:

- **H-A1** is **too sparse**: trades-per-month median drops to 0 and zero-trade months rise from 16/36 to 24/36 on both symbols. Per-fold sample is insufficient for confident edge assessment regardless of the per-trade quality.
- **H-B2** is **becoming too noisy / overtraded** in the §7.5 framing: trade count rises but expectancy stays clearly negative (BTC −0.326 R, ETH −0.440 R), and the overall losses widen relative to baseline (−5.07% vs −3.39% on BTC; −5.65% vs −3.53% on ETH). The candidate-to-entry conversion rises from ~7% to ~12%, but added candidates are not net-additive to expectancy.
- **H-C1** is **balanced but flat**: frequency near baseline, expectancy and PF near baseline.
- **H-D3** is **identical** in entry/exit count and frequency to H0 (only intra-trade stop trajectory differs), with marginally worse expR and PF on both symbols.

---

## 6. Pre-declared §10.3 / §10.4 classification

Per Phase 2f Gate 1 plan §10.3 (promotion paths + disqualification floor), §10.4 (hard reject when trades rise + expR < −0.50 or PF < 0.30), §11.3 (no-peeking validation discipline), §11.3.5 (thresholds pre-committed; no post-hoc loosening), §11.4 (BTC must clear; ETH must not catastrophically fail).

| Variant | Disqualification check (BTC)                                                                       | §10.3 promotion (BTC) | §10.4 hard-reject (BTC) | Decision                  |
|---------|----------------------------------------------------------------------------------------------------|----------------------:|------------------------:|---------------------------|
| H-A1    | expR worsens (−0.831 vs −0.459); PF worsens (0.10 vs 0.26)                                          | none triggered        | n/a (trades fell)       | **DISQUALIFY**            |
| H-B2    | \|maxDD\| > 1.5× baseline (5.53% vs 3.67% → ratio 1.505x)                                           | §10.3.a passes (Δexp=+0.133, ΔPF=+0.17); §10.3.b fails (Δ\|dd\|=+1.86pp > 1.0pp) | n/a (PF=0.43 ≥ 0.30, expR=−0.326 ≥ −0.50) | **DISQUALIFY**            |
| H-C1    | expR worsens (−0.499 vs −0.459); PF worsens (0.24 vs 0.26)                                          | none triggered        | n/a (trades fell)       | **DISQUALIFY**            |
| H-D3    | expR worsens (−0.475 vs −0.459); PF worsens (0.25 vs 0.26)                                          | none triggered        | n/a (trades flat)       | **DISQUALIFY**            |

**All four wave-1 variants are disqualified per the pre-declared §10.3 floor.** Per §11.3 the validation window V is reserved for the top-1–2 surviving variants. With zero survivors, V is not run in this wave.

H-B2 is the closest case: it passes §10.3.a's expectancy + PF improvement bars (Δexp=+0.133, ΔPF=+0.17) and would qualify as a candidate but for the maxDD ratio (1.505x) crossing the 1.5x disqualification veto by 0.005x. Per §11.3.5 the threshold is pre-committed and cannot be loosened after seeing the result.

---

## 7. Slippage and stop-trigger sensitivity

Per Phase 2f Gate 1 plan §10.2 + §11.6, slippage sensitivity (LOW / HIGH) is required only for variants that **clear** the base MEDIUM-slippage §10.3 pass. Per the Phase 2g operator brief item 10 + GAP-20260424-032, mark-price stop-trigger sensitivity is required only for **promoted** variants.

With **REJECT ALL** outcome on R, no candidate proceeds to either sensitivity sweep. The infrastructure exists in this branch (`BacktestConfig.slippage_bucket` and `BacktestConfig.stop_trigger_source`) and is exercised by the runner CLI, but no sensitivity runs were performed because there are no promoted variants to test. This is the disciplined §11.3 outcome, not a deferral.

---

## 8. Recommendation

**Reject all four wave-1 variants.** Per the pre-declared §10.3 disqualification floor, no variant qualifies for V-window validation in this wave.

Wave 2 is **not implicit**. Per Phase 2f Gate 1 §3.6 and §11.3.5, wave 2 requires a fresh operator approval. If the operator wishes to revisit any of the wave-1 axes:

- **H-A1 (setup window length).** Wave-1 result: too sparse. A wave-2 hypothesis could test 12 / 14 / 16 bars with the explicit acknowledgement that frequency is expected to drop further, OR a different setup-logic axis (e.g., H-A2 range-width ceiling, H-A3 drift cap) that targets the same 58% "no valid setup" bottleneck without losing trade flow.
- **H-B2 (expansion threshold 0.75).** Wave-1 result: §10.3.a economics improved but |maxDD| ratio 1.505x narrowly exceeded the 1.5x veto. A wave-2 hypothesis could pair the 0.75 expansion with a tighter stop-distance band (e.g., 0.50–1.40 × ATR20) to keep expectancy + PF improvements while reducing tail drawdown — but that would be a **bundled variant**, which Phase 2f §9.1 forbids in single-axis wave 1. Wave 2 would need explicit operator approval to reintroduce it.
- **H-C1 (EMA pair 20/100).** Wave-1 result: marginally worse on both symbols. Likely no wave-2 follow-up unless paired with a different slope-rule axis.
- **H-D3 (break-even +2.0 R).** Wave-1 result: indistinguishable from H0 (trade entries are identical; intra-trade stop trajectory differs slightly). A wave-2 hypothesis could pair this with a tighter trailing multiplier (H-D4) to make the break-even change relevant, but that is again a bundled variant.

The cleanest message of this wave is: the locked v1 strategy's economics are dominated by the **edge problem** (expectancy below zero across regimes for both symbols), not by single-axis filter parameter choices. The four single-axis changes that targeted the dominant funnel rejections did not translate into a PF > 1 / positive expectancy variant on BTC. The recommendation per Phase 2g is to honor the pre-declared §10.3 result and **not advance any variant to V or to live capital**, then return to the operator for the next-boundary decision.

---

## 9. What remains untouched

- Phase 2e baseline run directory `data/derived/backtests/phase-2e-baseline/2026-04-20T23-58-39Z/` — read-only, unchanged.
- Phase 2e baseline summary, Gate 2 review, checkpoint report — unchanged.
- v002 dataset manifests and partitions — unchanged.
- `docs/12-roadmap/technical-debt-register.md` — unchanged (operator restriction).
- `docs/00-meta/implementation-ambiguity-log.md` — no GAP entries appended in 2g (no new ambiguities discovered; GAP-20260424-032's mark-price sensitivity hook is now wired in code but unused per REJECT ALL).

---

## 10. Reproducibility

To reproduce the headline numbers:

```bash
# H0 control (R window)
uv run python scripts/phase2g_variant_wave1.py --variant H0   --window R
# Variants
uv run python scripts/phase2g_variant_wave1.py --variant H-A1 --window R
uv run python scripts/phase2g_variant_wave1.py --variant H-B2 --window R
uv run python scripts/phase2g_variant_wave1.py --variant H-C1 --window R
uv run python scripts/phase2g_variant_wave1.py --variant H-D3 --window R

# Internal analysis (loads run dirs and prints the §10.3/§10.4 classification)
uv run python scripts/_phase2g_wave1_analysis.py
```

Each run is deterministic at fixed inputs; same v002 data + same `BacktestConfig` produces the same `trade_log.json` byte-for-byte (modulo `trade_id`'s UUID suffix per `engine.py:474`).

---

**End of variant-comparison report. No promotion. No V-window run. Awaiting operator decision on the next boundary.**
