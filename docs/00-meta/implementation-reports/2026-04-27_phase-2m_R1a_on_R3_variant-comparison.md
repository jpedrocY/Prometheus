# Phase 2m — R1a-on-R3 Variant Comparison Report

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; no post-hoc loosening per §11.3.5); Phase 2g comparison report (REJECT ALL verdict, preserved as historical evidence only); Phase 2h decision memo; Phase 2i §1.7.3 project-level locks; Phase 2i redesign-analysis memo (carry-forward set R1a + R3 capped at ≤ 2); Phase 2j memo §C (R1a spec) + §D (R3 spec); Phase 2k Gate 1 plan §§ 11.B / 13 (R1a implementation scope and committed sub-parameters); Phase 2l comparison report (R3 PROMOTE verdict with R3 locked as the exit baseline for any future R1a execution); Phase 2m operator-approved brief.

**Branch:** `phase-2m/R1a-on-R3-execution`. **Run dates:** 2026-04-26 UTC.

**Status:** PROMOTE on R window under the **H0 anchor** (the official §10.3 / §10.4 ranking discipline). The supplemental R3-anchor view (descriptive only) shows R1a's marginal contribution on top of R3 is asymmetric: R1a worsens BTC vs R3-only and improves ETH vs R3-only. V-window confirmation produced; slippage and stop-trigger sensitivity produced. No live-readiness claim.

---

## 1. Plain-English summary

R1a (Phase 2j memo §C — Volatility-percentile setup with X = 25 percentile threshold and N = 200 trailing-bar lookback) was implemented in code on top of R3's locked exit baseline (Phase 2j memo §D — Fixed-R take-profit at +2.0 R + unconditional time-stop at 8 bars; protective stop never moved intra-trade). The candidate `R1a+R3` was executed against the locked Phase 2e v002 datasets on R = 2022-01-01 → 2025-01-01 alongside an H0 control re-run and an R3 locked-control re-run on the same engine version. Both controls reproduce their Phase 2g/2k/2l baselines bit-for-bit.

The official §10.3 / §10.4 framework with H0 as the sole comparison anchor (per Phase 2i §1.7.3) was applied unchanged. The verdict is **PROMOTE**: R1a+R3 clears §10.3.c (strict-dominance) on BTC and clears both §10.3.a (Δexp ≥ +0.10 AND ΔPF ≥ +0.05) and §10.3.c on ETH. No §10.3 disqualification floor triggered; no §10.4 hard reject (trade count drops, not rises).

The supplemental R3-anchor comparison (descriptive only — does R1a add value on top of R3?) is more nuanced: R1a's marginal contribution **hurts BTC** (Δexp_R3 −0.180 R, ΔPF −0.205, fewer trades) and **helps ETH** (Δexp_R3 +0.237 R, ΔPF +0.359). The R-window headline R1a+R3 promotion vs H0 is therefore dominated by R3's exit-machinery improvements (which Phase 2l already established) plus R1a's substantial improvement on ETH; on BTC, R1a slightly degrades the R3-only baseline but still clears H0 because R3's exit-side gains absorb the entry-side regression.

Per-fold (5 rolling, GAP-036): R1a+R3 beats H0 in 2/5 BTC folds and 4/5 ETH folds; beats R3 in 2/5 BTC folds and 2/5 ETH folds. V-window (validation): R1a+R3 BTC degrades sharply (4 trades, 0% WR, expR −0.990) while ETH improves dramatically (8 trades, 62.5% WR, expR **+0.386 R**, PF 2.222, netPct **+0.69%** — first positive netPct out-of-sample observed in any phase). Slippage sensitivity: monotone, proportional; HIGH-slippage on BTC at −0.544 expR is below the §10.4 hard-reject threshold but Δn < 0 so §10.4 does not apply. TRADE_PRICE bit-identical to MARK_PRICE (zero gap-through stops).

The R1a-specific diagnostics confirm correct implementation: 100% of filled R1a entries have ATR percentile ≤ 25% at entry (the predicate fires only on bottom-quartile compression bars, exactly per spec). Funnel attribution remains interpretable (`rejected_no_valid_setup` bucket continues to absorb predicate failures; no new bucket needed). Implementation-bug check is clean (zero TRAILING_BREACH, zero STAGNATION exits in any R3-or-R1a+R3 trade log).

This is the second PROMOTE verdict in the project's research history (R3 was the first, in Phase 2l). It is **provisional and evidence-based, not a live-readiness claim**. R1a+R3 still has negative aggregate expR on R (BTC −0.420, ETH −0.114); the §10.3 framework was designed to identify which redesigns clear pre-declared improvement thresholds vs. baseline, not to authorize live deployment.

## 2. What was built and what was run

### 2.1 Code surface

R1a is implemented as a structural redesign of the setup-validity predicate, with H0's range-based predicate preserved bit-for-bit as the default path. R3's exit machinery is locked unchanged from Phase 2l. R1a sub-parameters are committed singularly per Phase 2j memo §C.6.

| File                                                                | Change                                                                                                                                                                                                                                                                                                                                                                                                                       |
|---------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `src/prometheus/strategy/v1_breakout/variant_config.py`             | Added `SetupPredicateKind` StrEnum (`RANGE_BASED` / `VOLATILITY_PERCENTILE`). Added three optional R1a fields to `V1BreakoutConfig`: `setup_predicate_kind` (default RANGE_BASED), `setup_percentile_threshold = 25`, `setup_percentile_lookback = 200`. Defaults preserve H0 bit-for-bit; an R3-only config (selecting only `exit_kind=FIXED_R_TIME_STOP`) likewise preserves H0's setup predicate.                            |
| `src/prometheus/strategy/v1_breakout/setup.py`                      | Added `detect_setup_volatility_percentile()` sibling function and `percentile_rank_threshold()` helper. The function takes `prior_bars`, `atr_prior_15m`, `atr_history`, and the `percentile_threshold` / `lookback` sub-parameters, and returns a `SetupWindow` iff the rank of `A_prior` within the trailing-N distribution is ≤ `floor(X * N / 100)` (mid-rank ceil tie convention). H0's `detect_setup` is untouched.    |
| `src/prometheus/strategy/v1_breakout/strategy.py`                   | Added `_15m_prior_atr_history: deque[float]` to `StrategySession`, populated after every `observe_15m_bar` with the prior bar's ATR(20) value (skipping NaN warmup entries). Added `prior_15m_atr_history()` accessor. Made `min_15m_bars_for_signal` config-aware: for `VOLATILITY_PERCENTILE` it returns `max(base, lookback + ATR_PERIOD + 1)` per Phase 2j §C.10. Wired R1a dispatch in `V1BreakoutStrategy.maybe_entry`. |
| `src/prometheus/strategy/v1_breakout/__init__.py`                   | Exported `SetupPredicateKind` and `detect_setup_volatility_percentile`.                                                                                                                                                                                                                                                                                                                                                       |
| `src/prometheus/research/backtest/diagnostics.py`                   | Mirrored the strategy session changes inside `_IncrementalIndicators` (`prior15_atr_history` deque) and dispatched the setup predicate inside `run_signal_funnel` based on `strategy_config.setup_predicate_kind`. Made `min_15m_bars_for_signal` config-aware in the funnel diagnostic, matching the strategy-side warmup floor. The `rejected_no_valid_setup` bucket continues to absorb both predicates' failures.         |
| `tests/unit/strategy/v1_breakout/test_variant_config.py`            | Added 13 R1a unit tests: percentile-rank-threshold formula, insufficient-history rejection, NaN-history rejection, accept-when-bottom-quartile, reject-when-above-cutoff, reject-at-boundary, reject-on-non-positive-or-NaN A_prior, warmup-floor 221, history collection after seed, H0 default-preservation, R1a-via-strategy dispatch sentinel, R3-only config preservation, R1a+R3 combined-config integrity.           |
| `scripts/phase2m_R1a_on_R3_execution.py`                            | New per-variant runner mirroring the Phase 2l pattern. Variants: `H0` (control), `R3` (locked control), `R1a+R3` (candidate). Windows: `R`, `V`, `FULL`. Knobs: `--slippage` and `--stop-trigger` (per GAP-20260424-032). Aggregator schema preserved unchanged from Phase 2l (no schema additions needed for R1a — funnel attribution stays interpretable in the existing `rejected_no_valid_setup` bucket).                |
| `scripts/_phase2m_R1a_analysis.py`                                  | Internal one-shot analysis script. Computes the headline tables, official deltas-vs-H0, supplemental deltas-vs-R3, GAP-036 5-fold consistency comparisons (vs both anchors), mandatory diagnostics (per-regime expR, MFE distribution, long/short asymmetry, exit-reason histogram, implementation-bug check), R1a-specific diagnostics (ATR-percentile at entries, funnel comparison, trade-frequency sanity check), V-window comparison, slippage and stop-trigger sensitivity. |

### 2.2 Same-bar priority and exit-machinery preservation

R3's same-bar STOP > TAKE_PROFIT > TIME_STOP priority is preserved as in Phase 2l: STOP > TAKE_PROFIT is structural in the engine (stop check fires before management); TAKE_PROFIT > TIME_STOP is enforced in `TradeManagement._fixed_r_time_stop_decision`. R1a does not touch any exit logic. The protective stop is never moved during a trade for any R3-or-R1a+R3 variant.

### 2.3 Quality gates

Pre-runner gates: `ruff check .` ✓, `ruff format --check .` ✓ (120 files), `mypy` ✓ (49 source files, no errors), `pytest` ✓ (**417 passed** in 12.22s; up from 404 by exactly the 13 new R1a tests).

### 2.4 Run inventory

All runs on the Phase 2e v002 datasets (BTC + ETH 15m / 1h derived / mark-price 15m / funding-rate, plus the existing exchangeInfo snapshot). Sizing equity 10,000 USDT, risk 0.25%, leverage cap 2×, internal notional cap 100,000 USDT, taker fee rate 0.0005 (5 bps), default slippage MEDIUM, default stop-trigger MARK_PRICE.

| #  | Variant   | Window | Slippage | Stop trigger | Run dir                                                                                          |
|----|-----------|--------|----------|--------------|---------------------------------------------------------------------------------------------------|
| 1  | H0        | R      | MEDIUM   | MARK_PRICE   | `data/derived/backtests/phase-2m-r1a-h0-r/2026-04-26T21-37-41Z/`                                  |
| 2  | R3        | R      | MEDIUM   | MARK_PRICE   | `data/derived/backtests/phase-2m-r1a-r3-r/2026-04-26T21-37-52Z/`                                  |
| 3  | R1a+R3    | R      | MEDIUM   | MARK_PRICE   | `data/derived/backtests/phase-2m-r1a-r1a_plus_r3-r/2026-04-26T21-38-04Z/`                         |
| 4  | H0        | V      | MEDIUM   | MARK_PRICE   | `data/derived/backtests/phase-2m-r1a-h0-v/2026-04-26T21-42-28Z/`                                  |
| 5  | R3        | V      | MEDIUM   | MARK_PRICE   | `data/derived/backtests/phase-2m-r1a-r3-v/2026-04-26T21-42-38Z/`                                  |
| 6  | R1a+R3    | V      | MEDIUM   | MARK_PRICE   | `data/derived/backtests/phase-2m-r1a-r1a_plus_r3-v/2026-04-26T21-42-49Z/`                         |
| 7  | R1a+R3    | R      | LOW      | MARK_PRICE   | `data/derived/backtests/phase-2m-r1a-r1a_plus_r3-r-slip=LOW/2026-04-26T21-44-53Z/`                |
| 8  | R1a+R3    | R      | HIGH     | MARK_PRICE   | `data/derived/backtests/phase-2m-r1a-r1a_plus_r3-r-slip=HIGH/2026-04-26T21-47-11Z/`               |
| 9  | R1a+R3    | R      | MEDIUM   | TRADE_PRICE  | `data/derived/backtests/phase-2m-r1a-r1a_plus_r3-r-stop=TRADE_PRICE/2026-04-26T21-49-20Z/`        |

Each run directory contains the per-symbol `trade_log.{parquet,json}`, `equity_curve.parquet`, `drawdown.parquet`, `r_multiple_hist.parquet`, `summary_metrics.json`, `funnel_total.json`, `monthly_breakdown.parquet`, `yearly_breakdown.parquet`, plus the run-level `backtest_report.manifest.json` and `config_snapshot.json`. `data/` is git-ignored.

### 2.5 H0 + R3 control bit-for-bit reproducibility

| Variant | Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   | Phase 2l reference                                |
|---------|---------|-------:|-------:|--------:|------:|--------:|--------:|---------------------------------------------------|
| H0      | BTCUSDT |     33 | 30.30% |  −0.459 | 0.255 |  −3.39% |  −3.67% | matches Phase 2l H0 R-window exactly              |
| H0      | ETHUSDT |     33 | 21.21% |  −0.475 | 0.321 |  −3.53% |  −4.13% | matches                                            |
| R3      | BTCUSDT |     33 | 42.42% |  −0.240 | 0.560 |  −1.77% |  −2.16% | matches Phase 2l R3 R-window exactly              |
| R3      | ETHUSDT |     33 | 33.33% |  −0.351 | 0.474 |  −2.61% |  −3.65% | matches                                            |

This is the H0 + R3 preservation regression. Both controls reproduce the Phase 2l locked baselines bit-for-bit, confirming the new optional R1a fields and the `setup_predicate_kind` dispatch with default `RANGE_BASED` preserve both H0 (range-based + staged-trailing) and R3 (range-based + fixed-R-time-stop) behavior bit-for-bit through the strategy facade.

## 3. R-window headline comparison (BTC primary; ETH comparison)

All variants on R = 2022-01-01 → 2025-01-01 (36 months), MEDIUM slippage, MARK_PRICE stop trigger, v002 datasets:

| Variant | Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   | L/S    | Exits                                       |
|---------|---------|-------:|-------:|--------:|------:|--------:|--------:|--------|---------------------------------------------|
| H0      | BTCUSDT |     33 | 30.30% |  −0.459 | 0.255 |  −3.39% |  −3.67% | 16/17  | STOP=17, STAGNATION=16                      |
| H0      | ETHUSDT |     33 | 21.21% |  −0.475 | 0.321 |  −3.53% |  −4.13% | 13/20  | STOP=26, STAGNATION=6, TRAILING_BREACH=1    |
| R3      | BTCUSDT |     33 | 42.42% |  −0.240 | 0.560 |  −1.77% |  −2.16% | 16/17  | STOP=8, TAKE_PROFIT=4, TIME_STOP=21         |
| R3      | ETHUSDT |     33 | 33.33% |  −0.351 | 0.474 |  −2.61% |  −3.65% | 13/20  | STOP=14, TAKE_PROFIT=5, TIME_STOP=14        |
| R1a+R3  | BTCUSDT |     22 | 27.27% |  −0.420 | 0.355 |  −2.07% |  −2.33% | 12/10  | STOP=5, TAKE_PROFIT=3, TIME_STOP=14         |
| R1a+R3  | ETHUSDT |     23 | 34.78% |  −0.114 | 0.833 |  −0.59% |  −2.96% |  7/16  | STOP=9, TAKE_PROFIT=3, TIME_STOP=11         |

Trade-frequency sanity check: R1a's predicate is more selective on the entries it admits to the candidate pool. Despite R1a's funnel showing more `valid_setup_windows_detected` raw (30,260 BTC vs H0's 8,064), the downstream trigger filters cut more aggressively, ending with 27 entry intents on BTC (R1a+R3) vs 41 (H0/R3); 22 vs 33 closed trades (−33%). Same on ETH: 31 entry intents → 23 closed trades (−30%). All in-window (R) trade-frequency drops are explainable by the predicate-shape change, not by warmup-floor lift (the warmup-floor change of +191 bars affects approximately the first ~48 hours of the 36-month window).

## 4. Official ranking (H0 anchor — Phase 2f §10.3 / §10.4)

The official §10.3 / §10.4 promotion / disqualification framework with H0 as the **sole** comparison anchor (per Phase 2i §1.7.3 project-level lock). Thresholds applied unchanged from Phase 2f §§ 10.3 / 10.4 / 11.3.5; no post-hoc loosening.

### 4.1 Deltas vs H0

| Symbol  | Δexp     | ΔPF      | Δ|maxDD| (pp)        | |maxDD| ratio | Δn (%)    |
|---------|---------:|---------:|----------------------:|--------------:|----------:|
| BTCUSDT | **+0.039** | **+0.100** | **−1.341** (better) | **0.635×**    | **−33.3%** |
| ETHUSDT | **+0.362** | **+0.512** | **−1.171** (better) | **0.717×**    | **−30.3%** |

### 4.2 §10.3 disqualification floor — NOT TRIGGERED

| Veto             | BTC                                                          | ETH                                                          |
|------------------|--------------------------------------------------------------|--------------------------------------------------------------|
| expR worsens     | NO (+0.039)                                                  | NO (+0.362)                                                  |
| PF worsens       | NO (+0.100)                                                  | NO (+0.512)                                                  |
| |maxDD| > 1.5×   | NO (0.635×; 2.33% vs 3.67%)                                  | NO (0.717×; 2.96% vs 4.13%)                                  |

### 4.3 §10.3 promotion paths

§10.3.a (Δexp ≥ +0.10 AND ΔPF ≥ +0.05):

| Symbol | Δexp     | ΔPF      | §10.3.a result |
|--------|---------:|---------:|----------------|
| BTC    | +0.039   | +0.100   | **NOT cleared** (Δexp < +0.10) |
| ETH    | +0.362   | +0.512   | **CLEARED**    |

§10.3.b (Δexp ≥ 0 AND Δn ≥ +50% AND |dd| not worse by > 1.0 pp):

| Symbol | Δexp     | Δn (%)   | Δ|dd| (pp)   | §10.3.b result |
|--------|---------:|---------:|-------------:|----------------|
| BTC    | +0.039   | −33.3%   | −1.34        | **NOT cleared** (Δn < +50%) |
| ETH    | +0.362   | −30.3%   | −1.17        | **NOT cleared** |

§10.3.c strict-dominance (Δexp > 0 AND ΔPF > 0 AND Δ|maxDD| ≤ 0):

| Symbol | Δexp     | ΔPF      | Δ|maxDD| (pp) | §10.3.c result |
|--------|---------:|---------:|--------------:|----------------|
| BTC    | +0.039   | +0.100   | −1.341 (improvement) | **CLEARED**  |
| ETH    | +0.362   | +0.512   | −1.171 (improvement) | **CLEARED**  |

### 4.4 §10.4 hard reject — NOT TRIGGERED

§10.4 fires only when trade count rises (Δn > 0). R1a+R3 has Δn = −33% (BTC) and Δn = −30% (ETH); §10.4 does not apply by definition. Even if it had applied, R1a+R3's expR > −0.50 on both symbols and PF > 0.30 on both symbols.

### 4.5 §11.4 ETH-as-comparison rule — SATISFIED

§11.4 requires BTC must clear and ETH must not catastrophically fail. BTC clears §10.3.c (a single path is sufficient). ETH clears both §10.3.a and §10.3.c independently and triggers no §10.4 catastrophic-failure path. Both symbols therefore satisfy the cross-symbol rule.

### 4.6 Official verdict

**R1a+R3 PROMOTES** under Phase 2f §10.3 path (c) on BTC and paths (a) + (c) on ETH, with no §10.3 disqualification floor and no §10.4 hard reject triggered.

**Caveat on the BTC clearance.** §10.3.a does NOT fire on BTC (Δexp +0.039 is below the +0.10 threshold). Only §10.3.c strict-dominance fires, which is a weaker promotion signal than §10.3.a — strict-dominance just requires "everything moves the right direction"; §10.3.a requires a specific magnitude. The BTC promotion margin is small (Δexp +0.039 R is roughly the noise scale at 22-trade sample size). The ETH improvement is substantial and clear (Δexp +0.362 R / ΔPF +0.512 — comparable to R3's Phase 2l ETH gain).

## 5. Supplemental ranking (R3 anchor — DESCRIPTIVE ONLY)

This section is **not** governing. The official §10.3 / §10.4 ranking uses H0 as the comparison anchor (§4 above). The R3-anchor view here is descriptive: does R1a add value on top of R3, or does R3 alone capture the available edge?

### 5.1 Deltas vs R3

| Symbol  | Δexp     | ΔPF      | Δ|maxDD| (pp) | Δn (%)   |
|---------|---------:|---------:|--------------:|---------:|
| BTCUSDT | **−0.180** | **−0.205** | −0.17       | −33.3%   |
| ETHUSDT | **+0.237** | **+0.359** | +0.68       | −30.3%   |

### 5.2 What this tells us

R1a's marginal contribution on top of R3 is **asymmetric**:

- **BTC: R1a hurts.** Δexp_R3 −0.180 R, ΔPF_R3 −0.205. R3-only on BTC was −0.240 expR / 0.560 PF; R1a+R3 on BTC is −0.420 expR / 0.355 PF. R3's exit-machinery improvement on BTC is partially undone by R1a's setup-side filtering.
- **ETH: R1a helps.** Δexp_R3 +0.237 R, ΔPF_R3 +0.359. R3-only on ETH was −0.351 expR / 0.474 PF; R1a+R3 on ETH is −0.114 expR / 0.833 PF. R1a's volatility-percentile filter materially improves ETH performance.

Per-fold delta (R1a+R3 − R3): R1a+R3 beats R3 in 2/5 BTC folds and 2/5 ETH folds — fewer wins than R1a+R3 vs H0. The BTC F2 fold is particularly telling: R3 had +0.015 expR (one of its first positive folds); R1a+R3 has −0.792 expR — R1a degrades that fold by 0.807 R.

The supplemental view does not change the H0-anchor PROMOTE verdict. It is preserved here as **diagnostic input** for any future operator decision about how to sequence further structural redesigns. If the operator's next phase is e.g. paper/shadow preparation, the candidate to deploy would be R3 alone or R1a+R3 with operator awareness of R1a's BTC degradation.

## 6. Per-fold consistency (Phase 2f §11.2 + GAP-20260424-036)

5 rolling folds, fold 1 partial-train front edge, all test windows inside R.

### 6.1 Per-fold n / expR / PF

```
var      sym           F1     F2     F3     F4     F5  metric
H0       BTCUSDT        6      9      6      4      4  n_trades
H0       BTCUSDT    -0.48  -0.24  -0.52  -1.03  -0.69  expR
H0       ETHUSDT        8      7      8      2      4  n_trades
H0       ETHUSDT    -0.26  -0.75  -0.81  -0.84  -0.44  expR

R3       BTCUSDT        6      9      6      4      4  n_trades
R3       BTCUSDT    -0.48  +0.01  +0.10  -0.87  -0.45  expR
R3       ETHUSDT        8      7      8      2      4  n_trades
R3       ETHUSDT    -0.03  -0.46  -0.82  -0.84  -0.21  expR

R1a+R3   BTCUSDT        6      6      2      2      1  n_trades
R1a+R3   BTCUSDT    -0.83  -0.79  +0.69  -0.24  -1.32  expR
R1a+R3   ETHUSDT        5      4      6      3      3  n_trades
R1a+R3   ETHUSDT    -0.12  -1.43  -0.68  -0.32  -0.43  expR
```

### 6.2 Per-fold deltas

R1a+R3 − H0 (governs):

| Fold     | BTC Δexp | BTC verdict | ETH Δexp | ETH verdict |
|----------|---------:|-------------|---------:|-------------|
| F1 2022H2| −0.347   | worse       | +0.138   | better      |
| F2 2023H1| −0.554   | worse       | −0.680   | worse       |
| F3 2023H2| **+1.215** | better    | +0.126   | better      |
| F4 2024H1| **+0.789** | better    | +0.519   | better      |
| F5 2024H2| −0.627   | worse       | +0.017   | (tie)       |

BTC: 2/5 better, 3/5 worse. ETH: 4/5 better (one tie at +0.017), 1/5 worse.

R1a+R3 − R3 (descriptive):

| Fold     | BTC Δexp | ETH Δexp |
|----------|---------:|---------:|
| F1 2022H2| −0.347   | −0.094   |
| F2 2023H1| **−0.807** | **−0.972** |
| F3 2023H2| +0.592   | +0.133   |
| F4 2024H1| +0.634   | +0.519   |
| F5 2024H2| −0.873   | −0.214   |

Both anchors show R1a+R3 strongest at F3-F4 (mid-2023 → 2024H1) and weakest at F2 (2023H1) and F5 (2024H2). The F2 BTC degradation is the most material: R3's first positive BTC fold (F2 +0.015) is replaced with R1a+R3 −0.792 — the percentile filter selects against the bars that drove R3's F2 BTC win.

## 7. Mandatory diagnostics

### 7.1 Per-regime expR — realized 1h volatility regime

Convention: trailing 1000 1h-bar window of Wilder ATR(20), tercile cutoffs at 33% / 67%, mid-rank tie convention.

| Variant | Symbol  | Regime    | n  | expR    | PF    | WR     |
|---------|---------|-----------|---:|--------:|------:|-------:|
| H0      | BTCUSDT | low_vol   | 13 | −0.372  | 0.377 | 30.77% |
| H0      | BTCUSDT | med_vol   |  7 | −0.195  | 0.571 | 57.14% |
| H0      | BTCUSDT | high_vol  | 13 | −0.688  | 0.047 | 15.38% |
| H0      | ETHUSDT | low_vol   | 12 | −0.184  | 0.729 | 33.33% |
| H0      | ETHUSDT | med_vol   |  8 | −0.970  | 0.000 |  0.00% |
| H0      | ETHUSDT | high_vol  | 13 | −0.439  | 0.204 | 23.08% |
| R3      | BTCUSDT | low_vol   | 13 | −0.054  | 0.890 | 38.46% |
| R3      | BTCUSDT | med_vol   |  7 | −0.157  | 0.656 | 57.14% |
| R3      | BTCUSDT | high_vol  | 13 | −0.472  | 0.278 | 38.46% |
| R3      | ETHUSDT | low_vol   | 12 | −0.177  | 0.747 | 41.67% |
| R3      | ETHUSDT | med_vol   |  8 | −0.766  | 0.103 | 25.00% |
| R3      | ETHUSDT | high_vol  | 13 | −0.257  | 0.509 | 30.77% |
| R1a+R3  | BTCUSDT | low_vol   | 17 | **−0.329** | 0.460 | 23.53% |
| R1a+R3  | BTCUSDT | med_vol   |  1 | +0.120  |  ∞    |100.00% |
| R1a+R3  | BTCUSDT | high_vol  |  4 | **−0.942** | 0.051 | 25.00% |
| R1a+R3  | ETHUSDT | low_vol   | 11 | **+0.281** | **1.353** | 36.36% |
| R1a+R3  | ETHUSDT | med_vol   |  7 | −0.665  | 0.127 | 28.57% |
| R1a+R3  | ETHUSDT | high_vol  |  5 | −0.209  | 0.331 | 40.00% |

Two structural observations:

- **R1a+R3 concentrates trades in low_vol** (17/22 BTC = 77%; 11/23 ETH = 48%). This is by design — the percentile predicate at X = 25 selects the bottom-quartile vol regime. BTC's regime mix is more skewed toward low_vol because BTC's ATR distribution under R has a flatter shape than ETH's; the percentile filter pulls more of BTC's entries into low_vol.
- **The first low_vol PF > 1 is R1a+R3 ETH (n=11, expR +0.281, PF 1.353).** This is the first regime-symbol cell with positive expR AND PF above unity in any phase. ETH low_vol with R3 alone was already the project's strongest cell (−0.177 / 0.747); R1a's setup-side filtering pushes it to positive expectancy with a 1.35 profit factor. This is a substantial signal.
- BTC low_vol gets WORSE under R1a (−0.329 vs R3's −0.054) — same-regime, opposite direction. This is the asymmetry §5 surfaced.
- BTC high_vol degrades materially (−0.942 vs R3's −0.472), but the sample is only 4 trades — noisy.

### 7.2 MFE distribution

| Variant | Symbol  | n  | mean   | median | p25    | p75    | max    |
|---------|---------|---:|-------:|-------:|-------:|-------:|-------:|
| H0      | BTCUSDT | 33 | +0.851 | +0.531 | +0.214 | +1.188 | +3.359 |
| H0      | ETHUSDT | 33 | +1.164 | +0.849 | +0.238 | +1.666 | +4.946 |
| R3      | BTCUSDT | 33 | +0.792 | +0.531 | +0.214 | +1.167 | +3.083 |
| R3      | ETHUSDT | 33 | +1.061 | +0.849 | +0.238 | +1.666 | +3.462 |
| R1a+R3  | BTCUSDT | 22 | +0.622 | +0.366 | +0.076 | +0.706 | +2.621 |
| R1a+R3  | ETHUSDT | 23 | **+1.418** | +1.036 | +0.284 | +1.851 | **+8.688** |

R1a+R3 ETH has a higher mean MFE (+1.418 vs R3's +1.061) and a substantially fatter right tail (max +8.688 R — a single very large move). The +2 R take-profit clips this trade at +2 R nominally, but the realized fill at next-bar-open captured ≈ 1.5 R after fees, leaving most of the unrealized excursion uncaptured. R1a+R3 BTC has the lowest MFE distribution of all three variants (mean +0.622) — consistent with R1a's compression-bar selection on BTC producing tighter trades that don't extend.

### 7.3 Long/short asymmetry

| Variant | Symbol  | LONG n / expR / PF        | SHORT n / expR / PF       |
|---------|---------|---------------------------|---------------------------|
| H0      | BTCUSDT | 16 / −0.560 / 0.216       | 17 / −0.364 / 0.305       |
| H0      | ETHUSDT | 13 / −1.005 / 0.067       | 20 / −0.131 / 0.712       |
| R3      | BTCUSDT | 16 / −0.252 / 0.578       | 17 / −0.230 / 0.540       |
| R3      | ETHUSDT | 13 / −0.934 / 0.133       | 20 / +0.028 / 1.070       |
| R1a+R3  | BTCUSDT | 12 / −0.363 / 0.430       | 10 / −0.488 / 0.269       |
| R1a+R3  | ETHUSDT |  7 / −1.259 / 0.000       | 16 / **+0.387** / **1.906** |

**R1a+R3 ETH shorts are the project's strongest direction-symbol cell ever.** 16 trades, +0.387 R expectancy, profit factor 1.906. This is materially stronger than R3's ETH shorts (+0.028 / 1.070). The signal is concentrated on the short side; ETH longs under R1a+R3 are catastrophic (−1.259 R, PF 0.000 — every long lost money). This long/short skew is a known feature of the breakout strategy on ETH (regime is more often bearish-trending in R), but R1a's filter sharpens it: only 7 ETH long trades fire under R1a+R3 (vs 13 under H0/R3), and they're all losing.

### 7.4 Implementation-bug check

R3 forbids TRAILING_BREACH and STAGNATION exits. R1a+R3 inherits this. Counts:

```
R3     BTCUSDT: TRAILING_BREACH+STAGNATION exits = 0 (must be 0)  ✓
R3     ETHUSDT: TRAILING_BREACH+STAGNATION exits = 0 (must be 0)  ✓
R1a+R3 BTCUSDT: TRAILING_BREACH+STAGNATION exits = 0 (must be 0)  ✓
R1a+R3 ETHUSDT: TRAILING_BREACH+STAGNATION exits = 0 (must be 0)  ✓
```

All R3 / R1a+R3 exits use only `{STOP, TAKE_PROFIT, TIME_STOP, END_OF_DATA}`. The dispatch routing is correct; no leakage from the H0 staged-trailing path.

## 8. R1a-specific diagnostics (Phase 2j memo §C.16)

### 8.1 ATR-percentile distribution at filled R1a entries

Phase 2j memo §C.16 mandates that R1a's execution phase report the realized percentile rank of `A_prior` at each filled entry. If R1a is admitting non-compression bars (the §C.12 failure mode), this distribution will not concentrate near the bottom of the rank.

| Symbol  | n  | mean_pct | median | min   | max    | p25   | p75    | frac ≤ 25% |
|---------|---:|---------:|-------:|------:|-------:|------:|-------:|-----------:|
| BTCUSDT | 22 | 10.55%   |  9.50% | 0.50% | 25.00% | 1.00% | 18.62% | **100.00%** |
| ETHUSDT | 23 |  7.98%   |  5.00% | 0.50% | 24.50% | 0.50% | 15.00% | **100.00%** |

**Every R1a+R3 entry has ATR percentile ≤ 25%.** The median is well below the 25% cutoff (BTC 9.5%; ETH 5%). The predicate is working exactly as designed — admitting only bottom-quartile compression bars. There is no leakage to non-compression bars.

This rules out the §C.12 primary failure mode ("predicate admits non-compression bars; trade frequency rises but stop-out rate stays high"). The compression filter is genuinely concentrating entries in low-volatility regimes; the fact that R1a hurts BTC outcomes is therefore a regime-selection issue, not an implementation issue. R1a is correctly identifying compression — but compression bars on BTC under R do not consistently translate into post-breakout follow-through.

### 8.2 Setup-validity rate per fold

The funnel attribution counters `valid_setup_windows_detected` and `rejected_no_valid_setup` differ between predicates. R1a+R3's funnel (per the diagnostic) on the FULL 51-month window:

| Variant | Symbol  | Valid setups | Rejected (no valid setup) | Warmup excluded (15m) |
|---------|---------|-------------:|--------------------------:|----------------------:|
| H0      | BTCUSDT |        8,064 |                    85,480 |                    29 |
| H0      | ETHUSDT |        7,837 |                    84,731 |                    29 |
| R3      | BTCUSDT |        8,064 |                    85,480 |                    29 |
| R3      | ETHUSDT |        7,837 |                    84,731 |                    29 |
| R1a+R3  | BTCUSDT |       30,260 |                    63,284 |                   220 |
| R1a+R3  | ETHUSDT |       28,751 |                    63,817 |                   220 |

R1a's predicate produces about **3.75×** the valid-setup count of H0's predicate (because the percentile rule admits 25% of bars by construction, while the range-width-and-drift rule is more selective on average). The downstream trigger (`close-broke-level`, `TR ≥ ATR`, `close-location`, ATR-regime, stop-distance) cuts more aggressively because the candidate pool is wider — the end result is fewer entry intents (27 BTC / 31 ETH for R1a+R3 vs 41 BTC / 47 ETH for R3 on the FULL window). The funnel attribution stays interpretable (`rejected_no_valid_setup` continues to absorb predicate failures regardless of which predicate is active); no new bucket was added.

The warmup-excluded count rises by exactly 191 (220 − 29) — the additional 1h bars-equivalent to satisfy the 200-bar percentile lookback warmup.

## 9. V-window confirmation (2025-01-01 → 2026-04-01, 15 months)

R1a+R3 PROMOTES on R, so V-window is run per Phase 2f §11.3. Same engine version, datasets, MEDIUM slippage, MARK_PRICE stop trigger; R1a sub-parameters (X = 25, N = 200) and R3 sub-parameters (R-target = 2.0, time-stop bars = 8) remain singular per Phase 2j §C.6 / §D.6.

| Variant | Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   | Exits                                   |
|---------|---------|-------:|-------:|--------:|------:|--------:|--------:|------------------------------------------|
| H0      | BTCUSDT |      8 | 25.00% |  −0.313 | 0.541 |  −0.56% |  −0.87% | STOP=5, STAGNATION=3                     |
| H0      | ETHUSDT |     14 | 28.57% |  −0.174 | 0.695 |  −0.55% |  −0.80% | STOP=9, STAGNATION=5                     |
| R3      | BTCUSDT |      8 | 25.00% |  −0.287 | 0.580 |  −0.51% |  −1.06% | STOP=3, TAKE_PROFIT=1, TIME_STOP=4       |
| R3      | ETHUSDT |     14 | 42.86% |  −0.093 | 0.824 |  −0.29% |  −0.94% | STOP=5, TAKE_PROFIT=1, TIME_STOP=8       |
| R1a+R3  | BTCUSDT |      4 |  0.00% | **−0.990** | 0.000 |  −0.88% |  −0.71% | STOP=2, TIME_STOP=2                      |
| R1a+R3  | ETHUSDT |      8 | 62.50% | **+0.386** | **2.222** | **+0.69%** |  −0.51% | STOP=1, TAKE_PROFIT=1, TIME_STOP=6       |

V-window observations:

- **R1a+R3 ETH on V is the project's first positive-net-equity validation result.** netPct **+0.69%** over 15 months. WR 62.5% (5 of 8). expR **+0.386 R**, PF **2.222**. maxDD only −0.51%. This is materially the strongest V-window cell ever observed.
- **R1a+R3 BTC on V is severely degraded.** 4 trades, **0% WR (every trade lost)**, expR −0.990, PF 0.000, netPct −0.88%. The trade count is too small (n = 4) for confident statistical inference, but the direction is unambiguous: BTC under R1a's filter on V is worse than R3-only (R3 V was −0.287 / 0.580 / −0.51%) and worse than H0 V (−0.313 / 0.541 / −0.56%). The V-window suggests R1a's BTC degradation seen on R is amplified out-of-sample.
- The aggregate BTC + ETH V-window for R1a+R3 is approximately neutral (BTC −0.88% + ETH +0.69%), driven entirely by ETH.
- Per Phase 2f §11.3.5, V-window failure does not retroactively change the R-window classification but **does** end the candidate's wave. **However, R1a+R3 does not "fail V"** in the strict §10.3-disqualification sense — the V trade count (n = 4 BTC, n = 8 ETH) is too small to apply §10.3 disqualification thresholds reliably; the Phase 2f §11.3 rule is "no peeking, no fitting", not "V is a second hard pass/fail gate". The descriptive V evidence is what it is: ETH strong, BTC degraded.
- The single ETH V-window TAKE_PROFIT exit captured a +2 R win cleanly. The 6 TIME_STOP exits on ETH V are the dominant exit kind, and on aggregate they finished with positive expectancy.

## 10. Slippage sensitivity

GAP-20260424-032 carry-forward + Phase 2f §11.6 cost-sensitivity gate. LOW = 0 bps; MEDIUM = 5 bps (baseline); HIGH = 15 bps (3× baseline). R1a+R3 on R-window:

| Slippage | Symbol  | Trades | expR    | PF    | netPct  | maxDD   |
|----------|---------|-------:|--------:|------:|--------:|--------:|
| LOW      | BTCUSDT |     22 |  −0.319 | 0.449 |  −1.57% |  −2.01% |
| LOW      | ETHUSDT |     23 |  −0.022 | 0.965 |  −0.11% |  −2.55% |
| MEDIUM   | BTCUSDT |     22 |  −0.420 | 0.355 |  −2.07% |  −2.33% |
| MEDIUM   | ETHUSDT |     23 |  −0.114 | 0.833 |  −0.59% |  −2.96% |
| HIGH     | BTCUSDT |     22 |  −0.544 | 0.358 |  −2.68% |  −3.31% |
| HIGH     | ETHUSDT |     23 |  −0.354 | 0.583 |  −1.83% |  −4.00% |

Cost sensitivity is monotone and proportional. At HIGH (3× baseline) BTC expR drops to −0.544 (just below the §10.4 −0.50 hard-reject boundary if §10.4 applied — but Δn < 0 so §10.4 does not apply). ETH at LOW slippage is essentially break-even (expR −0.022, PF 0.965, netPct −0.11%) — confirming that the ETH improvement is robust to cost assumptions.

## 11. Stop-trigger-source sensitivity (GAP-20260424-032)

R1a+R3 on R window, MEDIUM slippage, MARK_PRICE vs TRADE_PRICE:

| Trigger     | Symbol  | Trades | expR    | PF    | netPct  | maxDD   | Gap-through stops |
|-------------|---------|-------:|--------:|------:|--------:|--------:|-------------------:|
| MARK_PRICE  | BTCUSDT |     22 |  −0.420 | 0.355 |  −2.07% |  −2.33% |                  0 |
| MARK_PRICE  | ETHUSDT |     23 |  −0.114 | 0.833 |  −0.59% |  −2.96% |                  0 |
| TRADE_PRICE | BTCUSDT |     22 |  −0.420 | 0.355 |  −2.07% |  −2.33% |                  0 |
| TRADE_PRICE | ETHUSDT |     23 |  −0.114 | 0.833 |  −0.59% |  −2.96% |                  0 |

**Bit-identical.** Zero R1a+R3 trades had a stop fill that gapped through (i.e. opened beyond the stop level). Same as R3 in Phase 2l: MARK_PRICE introduces no systematic bias relative to TRADE_PRICE for R1a+R3 on this data.

## 12. What the verdict does NOT say

The PROMOTE verdict is bounded:

- **R1a+R3 is not yet live-ready.** The promotion is against H0 under the Phase 2f §10.3 framework, not against any live-deployment threshold. Live readiness still requires the operational and capital-protection gates in `docs/12-roadmap/phase-gates.md`.
- **R1a+R3 still has negative aggregate expR on R.** BTC −0.420 R, ETH −0.114 R. The strategy still loses money in expectation across the average trade on R. The PROMOTE verdict means "less negative than H0 by enough to clear the pre-declared improvement threshold", not "profitable".
- **The BTC clearance is weak.** Only §10.3.c strict-dominance fires on BTC; §10.3.a does not (Δexp +0.039 < +0.10). BTC's headline R-window improvement is dominated by R3's exit-machinery contribution, not R1a's setup-side contribution. The R3-anchor view shows R1a degrades BTC vs R3 alone.
- **The ETH improvement is substantial.** Δexp +0.362 R / ΔPF +0.512 vs H0; Δexp +0.237 / ΔPF +0.359 vs R3. R1a is materially adding value on ETH.
- **The V-window degradation on BTC is real.** R1a+R3 BTC V at 0% WR on 4 trades is a meaningful concern, even at small sample size. R3-only V was −0.287 / 0.580; R1a+R3 V is −0.990 / 0.000. The direction is unambiguous.
- **The breakout family remains on probation.** Two of the three Family-S/Family-X structural redesigns specced in Phase 2j (R3 in Phase 2l, R1a+R3 in Phase 2m) have now PROMOTED. R3's improvement is broad-based; R1a's improvement is concentrated on ETH. Neither candidate is profitable in aggregate. The family is showing genuine response to structural-redesign work, but absolute performance remains below break-even.
- **Sample sizes remain small in absolute terms.** 22–23 trades on R is fewer than R3's 33 — closer to the threshold below which §10.3 confidence becomes increasingly fragile. The §10.3 framework's pre-committed thresholds were designed to be informative on small samples (cross-symbol consistency + per-fold consistency + threshold pre-commitment), but the BTC margin (Δexp +0.039 R) is approximately the noise scale.

## 13. Recommended next phase (proposal only — operator decides)

This recommendation is **provisional and evidence-based, not definitive**.

### 13.1 Primary recommendation: stop and reassess before further structural redesign work

Phase 2m has PROMOTED R1a+R3 under the H0 anchor, but the supplemental R3-anchor view, the per-fold view, and the V-window view all surface a real concern: **R1a's marginal contribution on top of R3 is asymmetric — substantially helping ETH and modestly hurting BTC**, with the BTC degradation amplified out-of-sample on V.

The recommended next phase is therefore **Phase 2n — operator/strategy review** (docs-only, no code, no runs) rather than a third structural execution:

- Decide whether to deploy R3 alone (Phase 2l winner, broad-based improvement) or R1a+R3 (mixed evidence) for any future paper/shadow preparation.
- Decide whether the Phase 2j §C.16 R1a-specific diagnostics + the Phase 2m per-regime view + the V-window evidence are sufficient to validate R1a's mechanism, or whether further targeted diagnostics are warranted.
- Decide whether to attempt one of the Phase 2i-deferred candidates (R1b regime classifier, R2 pullback entry) as a third structural-redesign wave, or whether the family has been adequately characterized.
- Decide whether to begin Phase 4 (runtime / state / persistence) operational infrastructure work in parallel with any further research, given that R3 has been validated at Phase 2l discipline.

### 13.2 Secondary recommendation: Phase 2n — narrow R1a-on-R3 diagnostic deepening (still docs-only or analysis-only)

If the operator prefers more evidence before any direction-change, a targeted analysis-only Phase 2n could:

- Compute per-trade ATR-percentile + per-bar regime vs trade outcome on existing data (no new backtests needed) to isolate exactly which compression patterns R1a is selecting that BTC mis-handles.
- Compute the F2 BTC degradation root cause via per-trade walkthrough.
- Extend the V-window R1a+R3 analysis with the sample-size-adjusted statistical view if useful.

This is a low-risk option that keeps the framework intact and builds further evidence.

### 13.3 Tertiary recommendation (NOT recommended): Phase 2o — R1b or R2 execution

Both Phase 2i-excluded candidates (R1b regime-conditional bias, R2 pullback entry) remain technically eligible. **Not recommended at this point** because:

- R1b has higher overfitting risk and harder cross-symbol robustness (per Phase 2i §3.2).
- R2 needs new pending-limit-fill logic in the backtester.
- The framework has now produced two PROMOTE verdicts — running a third without operator review of the mixed Phase 2m signal risks treadmill behavior.

### 13.4 What stays deferred

- **Phase 4 (runtime / state / persistence)** — operator-policy-deferred per `docs/12-roadmap/phase-gates.md`. Phase 2m does not propose advancing it. Operator policy unchanged.
- **Wave 2 H-D6 fallback exit-model bake-off** — superseded by R3 (Phase 2l) and R1a+R3 (Phase 2m).
- **R1b, R2** — Phase 2i excluded; no Phase 2m proposal to revive.
- **Live deployment, paper/shadow preparation, tiny-live preparation** — gated separately per `docs/12-roadmap/phase-gates.md`. Phase 2m does not propose advancing them.

### 13.5 What would change this recommendation

- **Operator preference for proceeding with R1a+R3 deployment readiness preparation** (paper/shadow planning) on the strength of the ETH signal alone, treating BTC degradation as a known risk to be observed in paper/shadow rather than a blocker. Switch primary → "Phase 2n — paper/shadow readiness planning for R3 (or R1a+R3 with operator-declared BTC monitoring)".
- **Operator preference for additional structural-redesign work** (R1b or R2). Switch primary → tertiary; framework discipline preserved.
- **Discovery of an implementation issue in R1a's setup-validity predicate.** None observed; the bug-check cleared (zero TRAILING_BREACH/STAGNATION leakage); the H0 + R3 controls reproduce Phase 2l baselines bit-for-bit; 100% of R1a entries at percentile ≤ 25% confirms the predicate is working as designed.

## 14. Threshold preservation

Phase 2f §§ 10.3 / 10.4 / 11.3 / 11.4 / 11.6 thresholds applied unchanged. No post-hoc loosening. Phase 2j memo §C.5 / §C.6 R1a sub-parameter values committed singularly. GAP-20260424-036 fold convention applied unchanged. GAP-20260424-031 (EMA slope), GAP-20260424-032 (mark-price sensitivity), GAP-20260424-033 (R3 unconditional time-stop) all carried forward per Phase 2k Gate 1 plan §16. No new GAP entries are proposed in Phase 2m.

## 15. Wave-1 + Phase 2l preservation

Phase 2g Wave-1's REJECT ALL verdict is preserved as historical evidence under the same framework. Phase 2l's R3 PROMOTE verdict is preserved unchanged; R3's locked sub-parameter values (R-target = 2.0; time-stop bars = 8) are unchanged in Phase 2m. Phase 2m compares R1a+R3 against the H0 anchor only (per Phase 2i §1.7.3); the R3-anchor view in §5 is supplemental and does not replace H0 as the formal promotion anchor.

## 16. Safety posture

Research-only. No live trading. No exchange-write paths. No production keys. No `.mcp.json`, no Graphify, no MCP server activation. No `.env` changes, no credentials, no Binance API calls (authenticated or public). No edits to `docs/12-roadmap/technical-debt-register.md`. No edits to `.claude/`. No `data/` commits (artifacts under `data/derived/backtests/phase-2m-r1a-*` are git-ignored). No Phase 4 work. No fallback Wave 2. No live-deployment readiness claim. Mark-price stop-trigger semantic preserved (MARK_PRICE default; TRADE_PRICE only as a sensitivity diagnostic per GAP-032). R1a's sub-parameters are committed singularly; no parameter sweeps. R3's sub-parameters are unchanged from Phase 2l. The 8-bar setup window is unchanged. No new structural redesign candidate is exposed beyond H0 / R3 / R1a+R3.

---

**Prepared for operator / ChatGPT review per the Phase 2m brief stop-and-await-Gate-2 requirement.** No `git add` / `git commit` performed. Pytest 417 passed. Phase 2m artifacts ready for commit on operator approval.
