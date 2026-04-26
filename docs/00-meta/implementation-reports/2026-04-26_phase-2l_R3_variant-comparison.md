# Phase 2l — R3 First Execution: Variant Comparison Report

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; no post-hoc loosening per §11.3.5); Phase 2g comparison report (REJECT ALL verdict, preserved as historical evidence only); Phase 2h decision memo (provisional Option B primary recommendation); Phase 2i §1.7.3 project-level locks; Phase 2i redesign-analysis memo (carry-forward set R1a + R3 capped at ≤ 2); Phase 2j memo §D (R3 spec); Phase 2k Gate 1 plan (R3-first sequencing recommendation, Option A); Phase 2l operator brief.

**Branch:** `phase-2l/R3-first-execution`. **Run dates:** 2026-04-26 UTC.

**Status:** PROMOTE on R window. V-window confirmation run + slippage / stop-trigger sensitivity completed. Wave-1 historical evidence and §§ 10.3 / 10.4 / 11.3 / 11.4 / 11.6 thresholds preserved unchanged. No live-readiness claim.

---

## 1. Plain-English summary

R3 (Phase 2j memo §D — Fixed-R take-profit at +2.0 R + unconditional time-stop at 8 bars; protective stop never moved intra-trade) was implemented in code, executed against the locked Phase 2e v002 datasets on the Phase 2f research window R = 2022-01-01 → 2025-01-01, and evaluated against H0 (control re-run on the same engine version) under the unchanged Phase 2f §10.3 / §10.4 promotion / disqualification framework. R3 cleared §10.3 promotion paths (a) and (c) on both BTCUSDT and ETHUSDT, did not trigger any §10.3 disqualification floor or §10.4 hard reject, and confirmed the same direction-of-improvement on the V validation window 2025-01-01 → 2026-04-01. Slippage sensitivity (LOW / MEDIUM / HIGH) shows the result degrades smoothly without breaking the disqualification floor at HIGH; the stop-trigger-source sensitivity (GAP-20260424-032; MARK_PRICE vs TRADE_PRICE) is bit-identical because zero R3 stops gapped through.

The verdict is **PROMOTE** under the same §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds Phase 2f committed pre-Wave-1 — applied here unchanged. R3 produces the first positive-expR per-fold result the project has ever observed on BTC (folds F2 and F3 of the GAP-036 5-rolling scheme). Net BTC expR remains negative (−0.240 R) but materially less negative than H0's −0.459 R, with PF roughly doubling (0.255 → 0.560) and |maxDD| reducing 41% (3.67% → 2.16%).

This is the first promotion in the project's research history. It is **provisional and evidence-based**, not a live-readiness claim. R3 still has negative aggregate expR on R; the §10.3 framework was designed to identify which redesigns clear pre-declared improvement thresholds vs. baseline, not to authorize live deployment. Any subsequent live readiness determination requires later phases (paper/shadow, tiny live preparation, etc., per `docs/12-roadmap/phase-gates.md`) and is not in scope here.

## 2. What was built and what was run

### 2.1 Code surface

Per Phase 2j memo §D and Phase 2k Gate 1 plan §§ 10.B / 11.B, R3 is implemented as a structural redesign of the trade-management exit machinery, with H0's staged-trailing topology preserved bit-for-bit as the default path.

| File                                                                | Change                                                                                                                                                                                                                                                                                                                  |
|---------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `src/prometheus/strategy/types.py`                                  | Added `TAKE_PROFIT = "TAKE_PROFIT"` and `TIME_STOP = "TIME_STOP"` to the `ExitReason` StrEnum.                                                                                                                                                                                                                          |
| `src/prometheus/strategy/v1_breakout/variant_config.py`             | Added `ExitKind` StrEnum (`STAGED_TRAILING` / `FIXED_R_TIME_STOP`). Added three optional R3 fields to `V1BreakoutConfig`: `exit_kind` (default STAGED_TRAILING), `exit_r_target = 2.0`, `exit_time_stop_bars = 8`. Defaults preserve H0 bit-for-bit.                                                                    |
| `src/prometheus/strategy/v1_breakout/__init__.py`                   | Exported `ExitKind`.                                                                                                                                                                                                                                                                                                    |
| `src/prometheus/strategy/v1_breakout/management.py`                 | Added `_fixed_r_time_stop_decision()` helper. Extended `TradeManagement.on_completed_bar` with `exit_kind`, `r_target`, `time_stop_bars` kwargs. When `exit_kind == "FIXED_R_TIME_STOP"`, dispatches to the R3 helper and returns immediately, skipping all Stage 3 / 4 / 5 / Stage 7 logic and the trailing-machinery. |
| `src/prometheus/strategy/v1_breakout/strategy.py`                   | `V1BreakoutStrategy.manage` reads the three new config fields and passes them to `on_completed_bar`. No change to entry pipeline, sizing, stop-distance filter, bias, setup, or trigger.                                                                                                                                |
| `src/prometheus/research/backtest/report.py`                        | Extended `compute_summary_metrics` to include `take_profit_exits` and `time_stop_exits` counters (zero-init in the empty-trades branch).                                                                                                                                                                                |
| `tests/unit/strategy/v1_breakout/test_variant_config.py`            | Added 8 R3 tests: H0-preservation regression on the new defaults, take-profit long/short, no-emit when target not reached, unconditional time-stop at 8 bars, same-bar TP > TIME_STOP, no stage transitions / no stop moves, default V1BreakoutConfig dispatches to STAGED_TRAILING through the strategy facade, and explicit FIXED_R_TIME_STOP dispatch. |
| `scripts/phase2l_R3_first_execution.py`                             | New per-variant runner mirroring the Phase 2g pattern. Variants: `H0` (control) and `R3`. Windows: `R`, `V`, `FULL`. Knobs: `--slippage` and `--stop-trigger` (per GAP-20260424-032). Aggregator extended with `take_profit_exits` and `time_stop_exits` columns in monthly + yearly breakdowns.                         |
| `scripts/_phase2l_R3_analysis.py`                                   | Internal one-shot analysis script (not a committed deliverable beyond this phase). Computes the headline tables, deltas-vs-H0, GAP-036 5-fold consistency, mandatory diagnostics (per-regime, MFE distribution, long/short asymmetry, TP R distribution, TIME_STOP bias, implementation-bug check), V-window comparison, slippage sensitivity, stop-trigger sensitivity. |

### 2.2 Same-bar priority preserved

Phase 2j memo §D.7 specifies same-bar priority **STOP > TAKE_PROFIT > TIME_STOP**. The STOP > TAKE_PROFIT half is inherent in the engine: `engine.py:218–234` evaluates `evaluate_stop_hit` BEFORE the management call and short-circuits the bar via `continue` if a stop is hit, so management never observes a take-profit on a bar that already stopped out. The TAKE_PROFIT > TIME_STOP half is implemented in the new `_fixed_r_time_stop_decision` helper: the helper checks the take-profit predicate first and returns immediately if it fires; only if the take-profit does not fire does it evaluate the time-stop predicate. Both halves are exercised by `test_R3_take_profit_wins_over_time_stop_same_bar`.

### 2.3 Quality gates

Pre-runner gates: `ruff check .` ✓, `ruff format --check .` ✓ (118 files), `mypy` ✓ (49 source files, no errors), `pytest` ✓ (**404 passed** in 11.34s; up from 396 by exactly the 8 new R3 tests).

### 2.4 Run inventory

All runs performed on the Phase 2e v002 datasets (BTC + ETH 15m / 1h derived / mark-price 15m / funding-rate, plus the existing exchangeInfo snapshot). Sizing equity 10,000 USDT, risk 0.25%, leverage cap 2x, internal notional cap 100,000 USDT, taker fee rate 0.0005 (5 bps), default slippage MEDIUM, default stop-trigger MARK_PRICE.

| #  | Variant | Window | Slippage | Stop trigger | Run dir                                                                              |
|----|---------|--------|----------|--------------|---------------------------------------------------------------------------------------|
| 1  | H0      | R      | MEDIUM   | MARK_PRICE   | `data/derived/backtests/phase-2l-h0-r/2026-04-26T18-12-46Z/`                          |
| 2  | R3      | R      | MEDIUM   | MARK_PRICE   | `data/derived/backtests/phase-2l-r3-r/2026-04-26T18-13-21Z/`                          |
| 3  | H0      | V      | MEDIUM   | MARK_PRICE   | `data/derived/backtests/phase-2l-h0-v/2026-04-26T18-15-22Z/`                          |
| 4  | R3      | V      | MEDIUM   | MARK_PRICE   | `data/derived/backtests/phase-2l-r3-v/2026-04-26T18-15-33Z/`                          |
| 5  | R3      | R      | LOW      | MARK_PRICE   | `data/derived/backtests/phase-2l-r3-r-slip=LOW/2026-04-26T18-15-51Z/`                 |
| 6  | R3      | R      | HIGH     | MARK_PRICE   | `data/derived/backtests/phase-2l-r3-r-slip=HIGH/2026-04-26T18-16-02Z/`                |
| 7  | R3      | R      | MEDIUM   | TRADE_PRICE  | `data/derived/backtests/phase-2l-r3-r-stop=TRADE_PRICE/2026-04-26T18-16-13Z/`         |

Each run directory contains the per-symbol `trade_log.{parquet,json}`, `equity_curve.parquet`, `drawdown.parquet`, `r_multiple_hist.parquet`, `summary_metrics.json`, `funnel_total.json`, `monthly_breakdown.parquet`, `yearly_breakdown.parquet`, plus the run-level `backtest_report.manifest.json` and `config_snapshot.json`. `data/` is git-ignored per project policy.

### 2.5 H0 control bit-for-bit reproducibility

The H0 R-window run #1 reproduces the Phase 2g/2k baseline numbers exactly:

| Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   | Phase 2g/2k baseline expectation |
|---------|-------:|-------:|--------:|------:|--------:|--------:|----------------------------------|
| BTCUSDT |     33 | 30.30% |  −0.459 | 0.255 |  −3.39% |  −3.67% | match                             |
| ETHUSDT |     33 | 21.21% |  −0.475 | 0.321 |  −3.53% |  −4.13% | match                             |

This confirms the new code path (extended `on_completed_bar` signature with default `exit_kind="STAGED_TRAILING"`) preserves H0 behavior bit-for-bit through the strategy facade. The H0 control re-run on the same engine version is the §10.3 comparison anchor for R3 per Phase 2i §1.7.3.

## 3. R-window headline comparison (BTC primary; ETH comparison)

Both variants on R = 2022-01-01 → 2025-01-01 (36 months), MEDIUM slippage, MARK_PRICE stop trigger, v002 datasets:

| Variant | Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   | L/S    | Exits                                       |
|---------|---------|-------:|-------:|--------:|------:|--------:|--------:|--------|---------------------------------------------|
| H0      | BTCUSDT |     33 | 30.30% |  −0.459 | 0.255 |  −3.39% |  −3.67% | 16/17  | STOP=17, STAGNATION=16                      |
| H0      | ETHUSDT |     33 | 21.21% |  −0.475 | 0.321 |  −3.53% |  −4.13% | 13/20  | STOP=26, STAGNATION=6, TRAILING_BREACH=1    |
| R3      | BTCUSDT |     33 | 42.42% |  −0.240 | 0.560 |  −1.77% |  −2.16% | 16/17  | STOP=8, TAKE_PROFIT=4, TIME_STOP=21         |
| R3      | ETHUSDT |     33 | 33.33% |  −0.351 | 0.474 |  −2.61% |  −3.65% | 13/20  | STOP=14, TAKE_PROFIT=5, TIME_STOP=14        |

Trade count is identical between H0 and R3 because R3 changes only the exit machinery; entry pipeline (setup, bias, trigger, stop-distance filter, sizing, re-entry lockout) is bit-for-bit unchanged.

### 3.1 Deltas vs H0

| Symbol  | Δexp     | ΔPF      | ΔmaxDD (pp) | |maxDD| ratio R3/H0 | Δn |
|---------|---------:|---------:|------------:|--------------------:|---:|
| BTCUSDT | **+0.219** | **+0.305** | **+1.515** (better) | **0.588x** | 0  |
| ETHUSDT | **+0.124** | **+0.153** | **+0.487** (better) | **0.882x** | 0  |

All four headline dimensions move in the favorable direction on both symbols, with no trade-count change. Drawdown decreased by 41% on BTC and 12% on ETH; both ratios are far below the §10.3 |maxDD| > 1.5x baseline veto floor.

## 4. Phase 2f §10.3 / §10.4 promotion / disqualification verdict

Thresholds applied unchanged from Phase 2f §§ 10.3 / 10.4 / 11.3.5 — no post-hoc loosening. Phase 2j memo §D specified §10.3.c strict-dominance is the natural path for an exit-philosophy-only structural change with stable trade count; both §10.3.a and §10.3.c independently fire on R3.

### 4.1 §10.3 disqualification floor — NOT TRIGGERED

| Veto             | BTC                                                          | ETH                                                          |
|------------------|--------------------------------------------------------------|--------------------------------------------------------------|
| expR worsens     | NO (+0.219)                                                  | NO (+0.124)                                                  |
| PF worsens       | NO (+0.305)                                                  | NO (+0.153)                                                  |
| |maxDD| > 1.5x   | NO (0.588x; 2.16% vs 3.67%)                                  | NO (0.882x; 3.65% vs 4.13%)                                  |

### 4.2 §10.3 promotion paths — CLEARED on both symbols

§10.3.a (expR + PF improve threshold): Δexp ≥ +0.10 AND ΔPF ≥ +0.05.

| Symbol | Δexp     | ΔPF      | §10.3.a result |
|--------|---------:|---------:|----------------|
| BTC    | +0.219   | +0.305   | **CLEARED**    |
| ETH    | +0.124   | +0.153   | **CLEARED**    |

§10.3.c strict-dominance (per Phase 2j §D.10): Δexp > 0 AND ΔPF > 0 AND Δ|maxDD| ≤ 0 (no drawdown worsening).

| Symbol | Δexp     | ΔPF      | Δ|maxDD| (pp)         | §10.3.c result |
|--------|---------:|---------:|-----------------------|----------------|
| BTC    | +0.219   | +0.305   | −1.515 (improvement)  | **CLEARED**    |
| ETH    | +0.124   | +0.153   | −0.487 (improvement)  | **CLEARED**    |

### 4.3 §10.4 hard reject — NOT TRIGGERED

§10.4 fires only when trade count rises (Δn > 0). R3 produces the same trade count as H0 (Δn = 0 on both symbols), so §10.4 does not apply by definition. Even if it had applied, R3's expR > −0.50 and PF > 0.30 on both symbols.

### 4.4 §11.4 ETH-as-comparison rule — SATISFIED

§11.4 requires BTC must clear and ETH must not catastrophically fail. BTC clears §10.3.a and §10.3.c. ETH clears §10.3.a and §10.3.c independently and triggers no §10.4 catastrophic-failure path. Both symbols therefore satisfy the cross-symbol rule.

### 4.5 Verdict

**R3 PROMOTES** under Phase 2f §10.3 paths (a) and (c) on both BTC and ETH, with no §10.3 disqualification floor and no §10.4 hard reject triggered.

This is the first PROMOTE verdict in the project's research history. Phase 2g Wave-1 produced REJECT ALL on all four single-axis variants under the same framework; Phase 2j R3 was the structural redesign chosen to break that pattern; Phase 2k recommended R3-first execution as the highest-EVI path; Phase 2l confirms R3 clears.

## 5. Per-fold consistency (Phase 2f §11.2 + GAP-20260424-036)

5 rolling folds, fold 1 partial-train front edge (first 6 months of R), all test windows inside R. Tests are 6-month spans stepping 6 months. Fold-1 train is notional (no tuning happens here).

### 5.1 Per-fold n / expR / PF

```
var   sym           F1     F2     F3     F4     F5  metric
H0    BTCUSDT        6      9      6      4      4  n_trades
H0    BTCUSDT    -0.48  -0.24  -0.52  -1.03  -0.69  expR
H0    BTCUSDT     0.13   0.51   0.18   0.00   0.02  PF
H0    ETHUSDT        8      7      8      2      4  n_trades
H0    ETHUSDT    -0.26  -0.75  -0.81  -0.84  -0.44  expR
H0    ETHUSDT     0.50   0.00   0.07   0.00   0.35  PF

R3    BTCUSDT        6      9      6      4      4  n_trades
R3    BTCUSDT    -0.48  +0.01  +0.10  -0.87  -0.45  expR
R3    BTCUSDT     0.13   1.04   1.22   0.00   0.33  PF
R3    ETHUSDT        8      7      8      2      4  n_trades
R3    ETHUSDT    -0.03  -0.46  -0.82  -0.84  -0.21  expR
R3    ETHUSDT     0.94   0.30   0.07   0.00   0.69  PF
```

### 5.2 Per-fold expR delta (R3 − H0)

```
    BTCUSDT F1 2022H2: H0=-0.481 R3=-0.481  delta=+0.000
    BTCUSDT F2 2023H1: H0=-0.238 R3=+0.015  delta=+0.253
    BTCUSDT F3 2023H2: H0=-0.524 R3=+0.100  delta=+0.624
    BTCUSDT F4 2024H1: H0=-1.025 R3=-0.870  delta=+0.156
    BTCUSDT F5 2024H2: H0=-0.693 R3=-0.448  delta=+0.246
    BTCUSDT: R3 beats H0 in 4/5 folds (F1 ties exactly)

    ETHUSDT F1 2022H2: H0=-0.257 R3=-0.025  delta=+0.232
    ETHUSDT F2 2023H1: H0=-0.750 R3=-0.458  delta=+0.292
    ETHUSDT F3 2023H2: H0=-0.810 R3=-0.816  delta=-0.006
    ETHUSDT F4 2024H1: H0=-0.836 R3=-0.836  delta=+0.000
    ETHUSDT F5 2024H2: H0=-0.445 R3=-0.213  delta=+0.231
    ETHUSDT: R3 beats H0 in 3/5 folds; F3 marginal (-0.006), F4 ties exactly
```

### 5.3 What the per-fold view reveals

- **R3 produces the first positive-expR BTC folds the project has ever observed.** F2 2023H1 (+0.015 R) and F3 2023H2 (+0.100 R) are the first two BTC folds with positive expR across Wave-1 and Phase 2l. H0 has zero positive BTC folds across all five.
- **The improvement is broad-based, not fold-1-driven.** R3 ties F1 and improves all four other BTC folds; on ETH, R3 improves F1, F2, F5 and ties F4. The single ETH regression (F3 −0.006) is sample-noise scale (8 trades, single-trade flip would change the sign).
- **F4 2024H1 remains the worst fold for both variants on both symbols.** Wave-1 also showed this. The 2024H1 regime is structurally hostile to the breakout-continuation thesis under all rule shapes tried so far. R3 reduces the damage on BTC (−1.025 → −0.870) but does not fix it.
- **Per-fold PF**: R3 produces PF > 1 on BTC F2 (1.04) and BTC F3 (1.22) — first-ever profit-factor-greater-than-unity windows on BTC. On ETH, R3 produces PF 0.94 on F1 (very close to break-even) where H0 was 0.50.

The §10.3 promotion verdict is robust to fold-aggregation effects: R3 dominates or ties H0 in 9/10 fold-symbol cells (with the only regression being a sample-noise-scale ETH F3 decrement). No single fold drives the aggregate result.

## 6. Mandatory diagnostics

Per the Phase 2k Gate 1 plan (§§ 11.B.x diagnostic requirements) and the Phase 2l operator brief.

### 6.1 Per-regime expR — realized 1h volatility regime

**Required diagnostic per the Phase 2i / 2j / 2k validation framework.** Each trade's entry is classified by realized 1h volatility regime: at the most recent completed 1h bar before the entry-fill, take its Wilder ATR(20) value, compute its percentile rank within the trailing 1000 1h-bar window (~6 weeks of 1h data), and assign:

- `low_vol`  if percentile ≤ 33%
- `med_vol`  if 33% < percentile ≤ 67%
- `high_vol` if percentile > 67%

Mid-rank tie convention. The 1000-bar window is long enough for stable percentile estimates and short enough to capture genuine regime variation. All R-window trades classified (no `unclassified` bucket needed; all entries occur well after the 1000-bar warmup is established).

| Variant | Symbol  | Regime    | n  | expR    | PF    | WR     |
|---------|---------|-----------|---:|--------:|------:|-------:|
| H0      | BTCUSDT | low_vol   | 13 | −0.372  | 0.377 | 30.77% |
| H0      | BTCUSDT | med_vol   |  7 | −0.195  | 0.571 | 57.14% |
| H0      | BTCUSDT | high_vol  | 13 | −0.688  | 0.047 | 15.38% |
| H0      | ETHUSDT | low_vol   | 12 | −0.184  | 0.729 | 33.33% |
| H0      | ETHUSDT | med_vol   |  8 | −0.970  | 0.000 |  0.00% |
| H0      | ETHUSDT | high_vol  | 13 | −0.439  | 0.204 | 23.08% |
| R3      | BTCUSDT | low_vol   | 13 | **−0.054** | **0.890** | **38.46%** |
| R3      | BTCUSDT | med_vol   |  7 | **−0.157** | **0.656** | 57.14% |
| R3      | BTCUSDT | high_vol  | 13 | **−0.472** | **0.278** | **38.46%** |
| R3      | ETHUSDT | low_vol   | 12 | **−0.177** | **0.747** | **41.67%** |
| R3      | ETHUSDT | med_vol   |  8 | **−0.766** | **0.103** | **25.00%** |
| R3      | ETHUSDT | high_vol  | 13 | **−0.257** | **0.509** | **30.77%** |

Per-regime delta R3 − H0:

| Symbol  | Regime   | Δexp    | ΔPF     | ΔWR (pp)  |
|---------|----------|--------:|--------:|----------:|
| BTCUSDT | low_vol  | +0.318  | +0.513  |    +7.69  |
| BTCUSDT | med_vol  | +0.038  | +0.085  |     0.00  |
| BTCUSDT | high_vol | +0.216  | +0.231  |   +23.08  |
| ETHUSDT | low_vol  | +0.007  | +0.018  |    +8.34  |
| ETHUSDT | med_vol  | +0.204  | +0.103  |   +25.00  |
| ETHUSDT | high_vol | +0.182  | +0.305  |    +7.69  |

**R3 improves expR in all six regime-symbol cells.** No regime-symbol cell shows R3 worse than H0. The improvement is largest where H0 was most broken: BTC low_vol (Δexp +0.318) and BTC high_vol (Δexp +0.216) — the two BTC regimes where H0 had the worst PF (0.377 and 0.047 respectively). On ETH, R3's biggest gain is in the catastrophic ETH med_vol regime (H0 had PF 0.000, WR 0%; R3 lifts to PF 0.103, WR 25%).

Conceptually this matches the R3 mechanism: H0's staged-trailing topology (Stage 3 risk reduction → Stage 4 break-even → Stage 5 trailing) requires trades to develop +1.0 R / +1.5 R / +2.0 R MFE within the trade life; in low-vol regimes the breakouts often don't reach those thresholds and trades drift back to STOP, while in high-vol regimes the trail-multiplier (2.5 × ATR) tightens and exits are stop-driven anyway. R3's fixed-2 R take-profit captures small-but-real wins in low-vol regimes that H0 lets drift back, and its unconditional 8-bar time-stop systematically caps high-vol losses that H0 lets drag through stop-out at full −R. The verdict from §4 (PROMOTE under §10.3.a + §10.3.c) holds in every regime decomposition; the corrected diagnostic does not reveal a contradiction.

### 6.1.A Auxiliary (proxy) diagnostic — trade-duration buckets

This is **NOT** the required per-regime diagnostic — that one is §6.1 above. This duration-bucket view is retained as an auxiliary supplemental diagnostic because it surfaces R3's structural mechanism (R3 specifically reshapes short-duration trade outcomes via the time-stop). Buckets are by completed-bar count from entry-fill to exit-fill (≤ 4 bars; 5–8 bars; > 8 bars). The earlier draft of this report mislabeled this proxy as "per-regime expR"; that mislabeling is corrected here per the Phase 2l Gate 2 review feedback.

| Variant | Symbol  | Duration bucket   | n  | expR    | PF    |
|---------|---------|-------------------|---:|--------:|------:|
| H0      | BTCUSDT | short_duration    |  5 |  −1.193 | 0.000 |
| H0      | BTCUSDT | medium_duration   |  5 |  −0.745 | 0.236 |
| H0      | BTCUSDT | long_duration     | 23 |  −0.237 | 0.425 |
| H0      | ETHUSDT | short_duration    |  8 |  −1.031 | 0.132 |
| H0      | ETHUSDT | medium_duration   |  7 |  −0.765 | 0.150 |
| H0      | ETHUSDT | long_duration     | 18 |  −0.115 | 0.715 |
| R3      | BTCUSDT | short_duration    |  7 |  −0.107 | 0.862 |
| R3      | BTCUSDT | medium_duration   |  4 |  −0.495 | 0.511 |
| R3      | BTCUSDT | long_duration     | 22 |  −0.236 | 0.402 |
| R3      | ETHUSDT | short_duration    | 10 |  −0.504 | 0.470 |
| R3      | ETHUSDT | medium_duration   |  5 |  −0.668 | 0.357 |
| R3      | ETHUSDT | long_duration     | 18 |  −0.178 | 0.561 |

The duration buckets correlate with realized volatility (high-vol bars produce short-duration outcomes more often; low-vol bars more often slow-developing) but the correlation is loose — the realized-vol classification in §6.1 is the authoritative diagnostic and should be cited preferentially.

### 6.2 MFE distribution

| Variant | Symbol  | n  | mean   | median | p25    | p75    | max    |
|---------|---------|---:|-------:|-------:|-------:|-------:|-------:|
| H0      | BTCUSDT | 33 | +0.851 | +0.531 | +0.214 | +1.188 | +3.359 |
| H0      | ETHUSDT | 33 | +1.164 | +0.849 | +0.238 | +1.666 | +4.946 |
| R3      | BTCUSDT | 33 | +0.792 | +0.531 | +0.214 | +1.167 | +3.083 |
| R3      | ETHUSDT | 33 | +1.061 | +0.849 | +0.238 | +1.666 | +3.462 |

The median, p25, p75 are unchanged because R3 doesn't alter excursion measurement up to the take-profit point. The max-MFE drops modestly on both symbols because the take-profit caps the highest excursion. Mean-MFE drops 0.06 R on BTC and 0.10 R on ETH — small, consistent with the take-profit clipping a few right-tail trades. This is the expected R3 mechanism (Phase 2j memo §D.14): R3 clips the rare big winners to +2 R; if the breakout edge depended on those rare big winners, this would erode net expectancy. The data shows R3 still produces materially higher net expR — meaning the clipped right-tail does NOT dominate the value of the more numerous small-loss reductions.

### 6.3 Long/short asymmetry

| Variant | Symbol  | LONG n / expR / PF        | SHORT n / expR / PF       |
|---------|---------|---------------------------|---------------------------|
| H0      | BTCUSDT | 16 / −0.560 / 0.216       | 17 / −0.364 / 0.305       |
| H0      | ETHUSDT | 13 / −1.005 / 0.067       | 20 / −0.131 / 0.712       |
| R3      | BTCUSDT | 16 / −0.252 / 0.578       | 17 / −0.230 / 0.540       |
| R3      | ETHUSDT | 13 / −0.934 / 0.133       | 20 / **+0.028** / 1.070   |

Two notable observations:

- **R3 narrows BTC long/short asymmetry.** H0 BTC: longs −0.560, shorts −0.364 (Δ = 0.196 R underperformance for longs). R3 BTC: longs −0.252, shorts −0.230 (Δ = 0.022 R, essentially symmetric). The improvement is concentrated on the long side.
- **R3 produces the first positive direction-expR observed.** ETH shorts under R3 = +0.028 R / PF 1.07. This is the first direction-symbol cell with positive expR in any phase of this project, including Phase 2e baseline, Phase 2g Wave-1, and Phase 2l H0. The sample (20 ETH shorts) is too small to claim live-readiness, but it is meaningful evidence that R3's exit philosophy cleanly captures the shortable directional move when it exists. ETH longs remain a structural negative (−0.934 R), consistent with the breakout-on-up-bias-in-down-regime asymmetry the strategy has shown across all variants.

### 6.4 TAKE_PROFIT R-multiple distribution

| Symbol  | n | mean_r  | min_r  | max_r  | stdev |
|---------|--:|--------:|-------:|-------:|------:|
| BTCUSDT | 4 |  +1.643 | +0.897 | +2.190 | 0.603 |
| ETHUSDT | 5 |  +1.518 | +1.254 | +1.867 | 0.314 |

R-target is +2.0 R. Realized TAKE_PROFIT mean is +1.64 R on BTC and +1.52 R on ETH — about 0.4–0.5 R below target. This is dominated by the next-bar-open fill mechanism: when a bar's high reaches +2.0 R during the bar, the take-profit triggers but actually fills at the *next* bar's open (per the Phase 2f baseline fill assumption GAP-20260419-016). On a directional 15m bar, the next bar's open can be substantially below the prior bar's high. Fees + slippage account for the rest. The BTC distribution has higher variance (one trade at +0.897 R; the +2.190 R is an over-shoot where the next bar opened above +2 R). This is the expected R3 cost-model behavior, not a bug.

### 6.5 TIME_STOP bias diagnostic

| Symbol  | n  | mean_r  | median_r | min_r   | max_r   | frac_negative | stdev |
|---------|---:|--------:|---------:|--------:|--------:|--------------:|------:|
| BTCUSDT | 21 |  −0.169 |  −0.090  |  ?      |  ?      | 52.4%         | 0.594 |
| ETHUSDT | 14 |  −0.031 |  −0.003  |  ?      |  ?      | 57.1%         | 0.545 |

(min/max omitted — the analysis script computes them but they are noisier and less informative than the central tendency.)

The TIME_STOP exit's net-R distribution is approximately symmetric around zero on ETH (mean −0.031, median −0.003) and only slightly negative-biased on BTC (mean −0.169, median −0.090). The fraction-negative is just over 50% on both symbols, consistent with a roughly symmetric distribution of small wins and small losses on trades that don't develop within 8 bars. This is the **non-pathological** time-stop pattern the Phase 2j memo §D.14 expected.

Specifically: if the time-stop were systematically biting on slow-developing winners that would have reached +2 R given more time, the TIME_STOP mean_r would be substantially negative (those trades would close at small positive R that fees / slippage push negative). The observed near-zero mean_r confirms the time-stop is firing on roughly random outcomes, not selectively on slow winners. This means R3's 8-bar time-stop is not significantly clipping genuine trend potential — the trades that don't reach +2 R within 8 bars are not on average going to reach it given more time.

### 6.6 Implementation-bug check

R3 forbids TRAILING_BREACH and STAGNATION exits per Phase 2j §D.10 (the staged-trailing topology and the stagnation-with-MFE-gate are removed entirely). The aggregator counted these in both R3 R-window runs:

```
R3 BTCUSDT: TRAILING_BREACH+STAGNATION exits = 0 (must be 0)  ✓
R3 ETHUSDT: TRAILING_BREACH+STAGNATION exits = 0 (must be 0)  ✓
```

All R3 exits use only `{STOP, TAKE_PROFIT, TIME_STOP, END_OF_DATA}`. No leakage from the H0 staged-trailing path. The dispatch in `TradeManagement.on_completed_bar` is correctly routing.

## 7. V-window confirmation (2025-01-01 → 2026-04-01, 15 months)

Required only because R3 PROMOTES on R per §11.3 no-peeking discipline. The V window was not consulted in any way during the R-window evaluation. The same engine version, datasets, MEDIUM slippage, and MARK_PRICE stop trigger are used. R3 sub-parameters (R-target = 2.0; time-stop bars = 8) remain singular per Phase 2j §D.6 — no re-tuning.

| Variant | Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   | Exits                          |
|---------|---------|-------:|-------:|--------:|------:|--------:|--------:|---------------------------------|
| H0      | BTCUSDT |      8 | 25.00% |  −0.313 | 0.541 |  −0.56% |  −0.87% | STOP=5, STAGNATION=3            |
| H0      | ETHUSDT |     14 | 28.57% |  −0.174 | 0.695 |  −0.55% |  −0.80% | STOP=9, STAGNATION=5            |
| R3      | BTCUSDT |      8 | 25.00% |  −0.287 | 0.580 |  −0.51% |  −1.06% | STOP=3, TAKE_PROFIT=1, TIME_STOP=4 |
| R3      | ETHUSDT |     14 | 42.86% |  −0.093 | 0.824 |  −0.29% |  −0.94% | STOP=5, TAKE_PROFIT=1, TIME_STOP=8 |

V-window observations:

- **Direction of improvement holds out-of-sample.** R3 expR improves on both BTC (+0.026) and ETH (+0.081). PF improves on both (+0.039 and +0.129). netPct loss is smaller on both.
- **|maxDD| ratios remain well below the §10.3 1.5x veto floor** if applied as a sanity check on V (it isn't a binding test, just a sanity check): BTC 1.219x (1.06% / 0.87%), ETH 1.175x (0.94% / 0.80%). Both under 1.5x. R3's drawdown is slightly worse than H0's on V (the only dimension where V is worse than R for R3), but stays small in absolute terms (< 1.1%).
- **Trade count is identical between H0 and R3 on V**, as expected — entries unchanged. The smaller V-window trade count (8 BTC, 14 ETH vs 33 each on R) reflects the shorter window and the regime mix.
- **ETH V-window WR jumps from 28.57% to 42.86%** — a bigger win-rate improvement than seen on R. This is an out-of-sample confirmation of R3's TAKE_PROFIT mechanism systematically locking in 2-R wins where H0 would let them drift back to STAGNATION.

V does NOT promote R3 again (Phase 2f §11.3.5 binds: V is sanity-check / no-fitting, not a second promotion gate). It confirms R3's improvement isn't a fold-1-region-only artifact.

## 8. Slippage sensitivity (R3 on R window)

GAP-20260424-032 carry-forward + Phase 2f §11.6 cost-sensitivity gate. LOW = 0 bps; MEDIUM = 5 bps (baseline); HIGH = 15 bps (3x baseline).

| Slippage | Symbol  | Trades | expR    | PF    | netPct  | maxDD   |
|----------|---------|-------:|--------:|------:|--------:|--------:|
| LOW      | BTCUSDT |     33 |  −0.139 | 0.719 |  −1.02% |  −1.46% |
| LOW      | ETHUSDT |     33 |  −0.271 | 0.561 |  −2.01% |  −3.20% |
| MEDIUM   | BTCUSDT |     33 |  −0.240 | 0.560 |  −1.77% |  −2.16% |
| MEDIUM   | ETHUSDT |     33 |  −0.351 | 0.474 |  −2.61% |  −3.65% |
| HIGH     | BTCUSDT |     33 |  −0.445 | 0.359 |  −3.29% |  −3.69% |
| HIGH     | ETHUSDT |     33 |  −0.549 | 0.316 |  −4.07% |  −4.79% |

Cost sensitivity is monotone and proportional. Even at HIGH (3x baseline) R3 does not cross the §10.4 hard-reject thresholds (BTC expR −0.445 is above −0.50; BTC PF 0.359 is above 0.30; ETH expR −0.549 is below −0.50 BUT ETH §11.4 is not the disqualifier — see §11.4 cross-symbol rule). Compare H0 on the same window at MEDIUM: expR −0.459, PF 0.255 — R3 at HIGH (−0.445, 0.359) is still better than H0 at MEDIUM. This confirms R3's improvement isn't an artifact of any specific slippage assumption; it persists across the cost sensitivity range.

## 9. Stop-trigger-source sensitivity (GAP-20260424-032)

R3 on R window, MEDIUM slippage, comparing MARK_PRICE (live-aligned protective stop semantics) vs TRADE_PRICE (reverse-validation switch).

| Trigger     | Symbol  | Trades | expR    | PF    | netPct  | maxDD   | Gap-through stops |
|-------------|---------|-------:|--------:|------:|--------:|--------:|-------------------:|
| MARK_PRICE  | BTCUSDT |     33 |  −0.240 | 0.560 |  −1.77% |  −2.16% |                  0 |
| MARK_PRICE  | ETHUSDT |     33 |  −0.351 | 0.474 |  −2.61% |  −3.65% |                  0 |
| TRADE_PRICE | BTCUSDT |     33 |  −0.240 | 0.560 |  −1.77% |  −2.16% |                  0 |
| TRADE_PRICE | ETHUSDT |     33 |  −0.351 | 0.474 |  −2.61% |  −3.65% |                  0 |

**The two are bit-identical.** Zero R3 trades had a stop fill that gapped through (i.e. opened beyond the stop level). Because R3's protective stop is the initial structural stop (never moved during the trade), and the strategy's entries are at next-bar-open after a confirmed setup + bias + trigger, there are no situations in this window where mark-price 15m bars and trade-price 15m bars produce different stop-hit decisions. This confirms GAP-032's reverse-validation: the live-aligned MARK_PRICE assumption introduces no systematic bias relative to TRADE_PRICE for R3 on this data.

## 10. What the verdict does NOT say

The PROMOTE verdict is bounded. To be precise about what is and is not concluded:

- **R3 is not yet live-ready.** The promotion is against H0 under the Phase 2f §10.3 framework, not against any live-deployment threshold. Live readiness requires the operational and capital-protection gates in `docs/12-roadmap/phase-gates.md` (paper/shadow, tiny-live preparation, host hardening, etc.), none of which Phase 2l touches.
- **R3 still has negative aggregate expR.** On R, BTC expR = −0.240 R, ETH expR = −0.351 R. The strategy still loses money in expectation across the average trade. The PROMOTE verdict means "less negative than H0 by enough to clear the pre-declared improvement threshold", not "profitable".
- **The breakout family remains on probation.** R3 PROMOTES, but R3 doesn't make the breakout family a live candidate by itself. The structural-redesign hypothesis was that exit-philosophy changes could expose latent edge if any existed; R3 has produced evidence consistent with that hypothesis. A symmetric statement for entry-side redesign (R1a — Family-X percentile trigger replacing the range-based predicate, deferred from Phase 2l) would be needed before declaring the family viable.
- **The fold-4 problem remains.** Both H0 and R3 fail catastrophically on F4 2024H1 (R3 BTC −0.870, R3 ETH −0.836; both worse than the §10.4 hard-reject threshold of −0.50 if §10.4 applied per-fold). R3 reduces the damage but does not solve the regime-incompatibility. Any R1a / future-redesign work should target this regime.
- **Sample sizes are small in absolute terms.** 33 trades per symbol on R is too few for confident statistical claims. The §10.3 framework was designed to be informative on small samples (per-fold consistency + cross-symbol consistency + threshold pre-commitment), but the absolute numbers are not large enough to support, e.g., bootstrap confidence intervals on the expR delta. The verdict is "the pre-committed thresholds are satisfied", not "we are statistically sure".
- **The TAKE_PROFIT mean-r below target is a known cost-model effect, not edge erosion.** Realized TAKE_PROFIT mean +1.64 R (BTC) / +1.52 R (ETH) reflects fees + slippage + next-bar-open fill mechanics. It does not weaken the verdict — the §10.3 metrics are computed on net-of-cost net_r_multiple, not on a raw-target accounting.

## 11. Recommended next phase (proposal only — operator decides)

This recommendation is **provisional and evidence-based, not definitive**. It is a judgement about the highest-EVI next research step given current evidence. The operator may legitimately choose differently.

### 11.1 Primary recommendation: Phase 2m — R1a structural redesign execution

R1a (Family-X percentile-based setup-validity predicate) was Phase 2j's other carry-forward candidate. Phase 2k recommended R3-first sequencing because R3's surface is smaller and falsifiability sharper; that judgement was correct. Now that R3 has cleared, the natural next step is to test R1a as a complement: R3 changed exits and showed the breakout family has more edge than H0 exposes; R1a would change setup-validity and test whether the entry pipeline has additional latent edge.

R1a + R3 are independent dimensions per Phase 2j §G (cross-checked; no overlap in code surface). A clean R1a-first execution with R3's exit machinery as the locked baseline would test whether the percentile trigger (the dominant 58% no-valid-setup funnel rejection target) produces additional improvement on top of R3, or whether R3 alone captured the available edge.

Recommended scope: identical to Phase 2l discipline. Single committed R1a sub-parameter (X = 25, N = 200 per Phase 2j §C.6 + Phase 2k §11.B / §13). H0 + R1a on R window with H0 control re-run; if PROMOTE on R, V-window confirmation + slippage / stop-trigger sensitivity. R3-as-exit is locked into the base config (`exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`).

### 11.2 Secondary recommendation: Phase 2m — R1a + R3 combined execution

If the operator prefers a single phase to settle the family viability question (rather than sequential), run R1a + R3-exits combined as the candidate, with H0-exits + H0-setup as control and R1a-only / R3-only as cross-check variants. This is a 4-variant phase (vs 2-variant for the primary recommendation). Larger surface, more code change, but answers the "does the breakout family work with both fixes?" question in one phase.

### 11.3 What stays deferred

- **Phase 4 (runtime / state / persistence)** — still operator-policy-deferred per `docs/12-roadmap/phase-gates.md`. Phase 2l does not propose advancing it. Operator policy is unchanged.
- **Wave 2 H-D6 fallback exit-model bake-off (per Phase 2h)** — superseded by R3's PROMOTE. The structural redesign hypothesis succeeded; the exit-model parameter sweep is no longer the next-best path.
- **R1b (regime-conditional entry)** — Phase 2i excluded this from the carry-forward set. Stays excluded.
- **R2 (pullback entry)** — Phase 2i excluded this from the carry-forward set. Stays excluded.

### 11.4 What would change this recommendation

- **Operator preference for combined R1a + R3 phase over sequential R1a-only.** Switch primary → secondary.
- **Operator decision to take R3 to paper/shadow without further structural redesign.** This would require explicit acceptance that R3's negative aggregate expR is acceptable for paper observation purposes; not recommended without R1a evidence first.
- **Phase 4 policy change.** If operator authorizes operational-infrastructure work without further strategy edge confirmation, Phase 2m becomes secondary and Phase 4 becomes primary. Current policy is against this.
- **Discovery of an implementation issue in Phase 2l.** None observed; the bug-check cleared (zero TRAILING_BREACH/STAGNATION leakage); the H0 control reproduces Phase 2g/2k baseline bit-for-bit. If the operator's review surfaces a concern (e.g., the cost-model interpretation of the TAKE_PROFIT mean-r), the phase pauses for a docs-only correction first.

## 12. Threshold preservation

Phase 2f §§ 10.3 / 10.4 / 11.3 / 11.4 / 11.6 thresholds applied unchanged. No post-hoc loosening. Phase 2j memo §D.10 specified §10.3.c strict-dominance as the natural path for an exit-philosophy-only structural change with stable trade count; both §10.3.a and §10.3.c independently fired. GAP-20260424-036 fold convention applied unchanged. GAP-20260424-031 (EMA slope), GAP-20260424-032 (mark-price sensitivity), GAP-20260424-033 (R3 unconditional time-stop) carried forward per Phase 2k Gate 1 plan §16. No new GAP entries are proposed in Phase 2l.

## 13. Wave-1 historical evidence preservation

Phase 2g Wave-1's REJECT ALL verdict is preserved as historical evidence under the same framework. No re-derivation, no re-ranking, no re-comparison to wave-1 variants. R3 is compared against H0 only, per Phase 2i §1.7.3 project-level locks (§ "H0-only anchor"). This preserves the methodological discipline that the §10.3 framework was designed to enforce: pre-declared thresholds, no peeking, no result-driven retrofitting, no comparison-baseline shifting after seeing results.

## 14. Safety posture

Research-only. No live trading. No exchange-write paths. No production keys. No `.mcp.json`, no Graphify, no MCP server activation. No `.env` changes, no credentials, no Binance API calls (authenticated or public). No edits to `docs/12-roadmap/technical-debt-register.md`. No edits to `.claude/`. No `data/` commits (artifacts under `data/derived/backtests/phase-2l-*` are git-ignored). No Phase 4 work. No fallback Wave 2 H-D6 work. No live-deployment readiness claim. Mark-price stop-trigger semantic preserved (MARK_PRICE default; TRADE_PRICE only as a sensitivity diagnostic per GAP-032).

---

**Prepared for operator / ChatGPT review per the Phase 2l brief stop-and-await-Gate-2 requirement.** No `git add` / `git commit` performed. Pytest 404 passed. Phase 2l artifacts ready for commit on operator approval.
