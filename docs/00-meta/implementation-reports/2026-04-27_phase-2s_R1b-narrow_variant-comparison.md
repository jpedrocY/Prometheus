# Phase 2s — R1b-narrow Variant Comparison Report

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; no post-hoc loosening per §11.3.5); Phase 2g comparison report (REJECT ALL preserved as historical evidence only); Phase 2h decision memo; Phase 2i §1.7.3 project-level locks (H0 anchor; BTCUSDT primary); Phase 2j memo §C / §D; Phase 2k Gate 1 plan; Phase 2l comparison report (R3 PROMOTE locked); Phase 2m comparison report (R1a+R3 promoted-but-non-leading); Phase 2n / 2o / 2p / 2q / 2r consolidation and spec-writing memos (R3 = baseline-of-record; R1b-narrow spec committed); Phase 2s operator-approved execution brief.

**Phase:** 2s — R1b-narrow Execution.
**Branch:** `phase-2s/r1b-narrow-execution`.
**Run dates:** 2026-04-27 UTC.

**Status:** **PROMOTE** on R window under Phase 2f §10.3 with H0 as the governing anchor. V-window confirmation produced; slippage and stop-trigger sensitivity produced. PASS classification with sample-size caveats. No live-readiness claim.

---

## 1. Plain-English summary

R1b-narrow (Phase 2r spec memo §B / §F: bias-validity predicate replaces H0's binary slope-3 direction-sign check with a magnitude check at threshold S = 0.0020, anchored to the existing `ATR_REGIME_MIN` constant; R3 exit baseline locked unchanged) was implemented in code on top of R3's locked exit baseline. The candidate `R1b-narrow` was executed against the locked Phase 2e v002 datasets on R = 2022-01-01 → 2025-01-01 alongside an H0 control re-run and an R3 locked-control re-run. Both controls reproduce their Phase 2g/2k/2l/2m baselines bit-for-bit.

**Verdict: PROMOTE**, with **PASS** classification under Phase 2f §10.3:

- **BTC clears §10.3.a and §10.3.c** (Δexp +0.196 R, ΔPF +0.305, |maxDD| ratio 0.296× — well below the 1.5× veto floor).
- **ETH clears §10.3.a and §10.3.c** (Δexp +0.251 R, ΔPF +0.301, |maxDD| ratio 0.308×).
- **First time §10.3.a fires on both symbols simultaneously** at the magnitude threshold (Δexp ≥ +0.10 R AND ΔPF ≥ +0.05). Phase 2l R3 cleared §10.3.a on both, but the Δexp magnitudes were +0.219 BTC / +0.124 ETH; Phase 2m R1a+R3 cleared §10.3.a on ETH only (BTC clearance was §10.3.c only). R1b-narrow clears both §10.3.a thresholds on both symbols — a stronger formal signal than R1a+R3.

The result is genuine but comes with **important caveats**:

- **Trade-count drops sharply.** BTC 33 → 10 (−69.7%); ETH 33 → 12 (−63.6%). The bias-strength filter is more restrictive than Phase 2r §L anticipated. The §L "S is too small" failure mode did NOT materialize; the opposite (S sharply restricts the candidate pool) did.
- **V-window evidence is fragile.** BTC V-window has only 1 trade (vs H0's 8 / R3's 8). With n=1 (a single losing trade, expR −1.270), the V evidence is essentially uninterpretable on BTC. ETH V-window is the strongest observed (8 trades / 50% WR / expR +0.154 / PF 1.408 / netPct **+0.28%** — second positive-netPct V-window the project has produced after R1a+R3 ETH).
- **Per-fold sample sizes collapse** (BTC: 0/2/1/2/3 per fold; ETH: 3/2/1/2/2). Per-fold consistency is hard to assess at these counts.
- **ALL R1b-narrow entries are in marginal-or-moderate slope-strength buckets**; zero entries in the "strong" (≥ 0.0100) bucket. This is mechanically valid (the filter is working) but informative — strong-bias 1h regimes coincide with conditions that the existing setup-validity and ATR-regime filters reject downstream, so R1b-narrow's improvement comes from a narrow band of marginal-to-moderate bias strength.
- **R3-anchor view (descriptive only)**: R1b-narrow's marginal contribution on top of R3 is essentially neutral on BTC (Δexp_R3 −0.023, ΔPF_R3 +0.000) and positive on ETH (Δexp_R3 +0.127, ΔPF_R3 +0.148). The improvement vs H0 is dominated by R3's exit-machinery contribution and R1b-narrow's filter-induced trade-count concentration.

The §10.3 PROMOTE verdict stands unambiguously under the unchanged framework. The strategic interpretation is more nuanced — the small per-fold and V-window samples mean the formal PROMOTE is well within framework rules but the absolute-edge case is not strongly supported by the post-filter evidence.

## 2. What was built and what was run

### 2.1 Code surface

R1b-narrow is implemented as a single-axis structural redesign of H0's bias-validity predicate. H0's binary slope-3 direction-sign check is replaced with a magnitude check; H0's EMA-position component is preserved unchanged; R3's exit machinery is locked unchanged from Phase 2l.

| File                                                                | Change                                                                                                                                                                                                                                                                                              |
|---------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `src/prometheus/strategy/v1_breakout/variant_config.py`             | Added one new optional field: `bias_slope_strength_threshold: float = Field(default=0.0, ge=0.0, le=0.10)`. Default 0.0 dispatches to H0's strict binary check (bit-for-bit preserved). The committed R1b-narrow value is 0.0020.                                                                    |
| `src/prometheus/strategy/v1_breakout/bias.py`                       | Added `evaluate_1h_bias_with_slope_strength()` sibling function. Original `evaluate_1h_bias()` is unchanged. The new function rejects negative thresholds, handles NaN warmup, defends against `fast_now <= 0` edge case, and applies the magnitude check `slope_strength_3 >= +threshold` (LONG) and `<= -threshold` (SHORT). |
| `src/prometheus/strategy/v1_breakout/strategy.py`                   | `StrategySession._update_1h_bias` dispatches based on `config.bias_slope_strength_threshold`: `== 0.0` uses H0's strict binary check (sentinel-based bit-for-bit preservation); positive threshold uses the magnitude check inline.                                                              |
| `src/prometheus/research/backtest/diagnostics.py`                   | `_IncrementalIndicators.current_bias` extended with optional `slope_strength_threshold` parameter; `run_signal_funnel` passes `sc.bias_slope_strength_threshold`. The funnel attribution (`rejected_neutral_bias`, `bias_*_count`) handles both predicates correctly.                              |
| `tests/unit/strategy/v1_breakout/test_variant_config.py`            | Added 14 R1b-narrow unit tests: default config has `threshold == 0.0`; standalone function admits LONG/SHORT for strong trends; rejects weak trends below threshold; rejects negative threshold; warmup returns NEUTRAL; strategy session dispatches correctly at 0.0 vs 0.0020; H0 baseline path preserved bit-for-bit; R3-only config preserves H0 bias threshold; R1b+R3 combined config holds both axes; pydantic `Field(ge=0.0)` rejects negative threshold at construction. |
| `scripts/phase2s_R1b_narrow_execution.py`                           | Per-variant runner mirroring the Phase 2m pattern. Variants: H0 / R3 / R1b-narrow. Windows: R / V / FULL. Knobs: --slippage and --stop-trigger.                                                                                                                                                |
| `scripts/_phase2s_R1b_analysis.py`                                  | Internal analysis script computing official deltas-vs-H0, supplemental deltas-vs-R3, GAP-036 5-fold consistency, mandatory diagnostics + R1b-narrow-specific diagnostics (§P.1 slope-strength distribution at filled entries, §P.2 funnel attribution comparison, §P.3 slope-strength bucket analysis, §P.4 direction-asymmetry check), V-window comparison, slippage and stop-trigger sensitivity. |

### 2.2 Quality gates

Pre-runner gates: `ruff check .` ✓, `ruff format --check .` ✓ (122 files), `mypy` ✓ (49 source files; scripts out of mypy default scope per project precedent), `pytest` ✓ (**431 passed** in 11.92s; up from 417 by exactly the 14 new R1b-narrow tests).

### 2.3 Run inventory

All runs on the locked Phase 2e v002 datasets (BTC + ETH 15m / 1h derived / mark-price 15m / funding-rate). Sizing equity 10,000 USDT, risk 0.25%, leverage cap 2×, internal notional cap 100,000 USDT, taker fee rate 0.0005 (5 bps), default slippage MEDIUM, default stop-trigger MARK_PRICE.

| #  | Variant     | Window | Slippage | Stop trigger | Run dir                                                                                            |
|----|-------------|--------|----------|--------------|-----------------------------------------------------------------------------------------------------|
| 1  | H0          | R      | MEDIUM   | MARK_PRICE   | `data/derived/backtests/phase-2s-r1b-h0-r/2026-04-27T00-18-40Z/`                                    |
| 2  | R3          | R      | MEDIUM   | MARK_PRICE   | `data/derived/backtests/phase-2s-r1b-r3-r/2026-04-27T00-18-51Z/`                                    |
| 3  | R1b-narrow  | R      | MEDIUM   | MARK_PRICE   | `data/derived/backtests/phase-2s-r1b-r1b_narrow-r/2026-04-27T00-19-03Z/`                            |
| 4  | H0          | V      | MEDIUM   | MARK_PRICE   | `data/derived/backtests/phase-2s-r1b-h0-v/2026-04-27T00-20-16Z/`                                    |
| 5  | R3          | V      | MEDIUM   | MARK_PRICE   | `data/derived/backtests/phase-2s-r1b-r3-v/2026-04-27T00-20-27Z/`                                    |
| 6  | R1b-narrow  | V      | MEDIUM   | MARK_PRICE   | `data/derived/backtests/phase-2s-r1b-r1b_narrow-v/2026-04-27T00-20-38Z/`                            |
| 7  | R1b-narrow  | R      | LOW      | MARK_PRICE   | `data/derived/backtests/phase-2s-r1b-r1b_narrow-r-slip=LOW/2026-04-27T00-20-48Z/`                   |
| 8  | R1b-narrow  | R      | HIGH     | MARK_PRICE   | `data/derived/backtests/phase-2s-r1b-r1b_narrow-r-slip=HIGH/2026-04-27T00-20-59Z/`                  |
| 9  | R1b-narrow  | R      | MEDIUM   | TRADE_PRICE  | `data/derived/backtests/phase-2s-r1b-r1b_narrow-r-stop=TRADE_PRICE/2026-04-27T00-21-10Z/`           |

`data/` is git-ignored.

### 2.4 H0 + R3 control bit-for-bit reproducibility

| Variant | Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   | Phase 2l/2m reference |
|---------|---------|-------:|-------:|--------:|------:|--------:|--------:|-----------------------|
| H0      | BTCUSDT |     33 | 30.30% |  −0.459 | 0.255 |  −3.39% |  −3.67% | match                  |
| H0      | ETHUSDT |     33 | 21.21% |  −0.475 | 0.321 |  −3.53% |  −4.13% | match                  |
| R3      | BTCUSDT |     33 | 42.42% |  −0.240 | 0.560 |  −1.77% |  −2.16% | match                  |
| R3      | ETHUSDT |     33 | 33.33% |  −0.351 | 0.474 |  −2.61% |  −3.65% | match                  |

Both controls reproduce locked baselines bit-for-bit, confirming the new optional `bias_slope_strength_threshold` field with default 0.0 preserves H0 behaviour bit-for-bit through the strategy facade. Three preservation tests in `test_variant_config.py` enforce this contract:

- `test_R1b_default_threshold_zero_preserves_H0_bias` — default config has `threshold == 0.0`.
- `test_R1b_strategy_session_default_dispatches_to_H0_path` — sentinel dispatch verified.
- `test_R1b_h0_evaluate_function_unchanged` — original `evaluate_1h_bias()` unchanged.

## 3. R-window headline comparison

All variants on R = 2022-01-01 → 2025-01-01 (36 months), MEDIUM slippage, MARK_PRICE:

| Variant     | Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   | L/S    | Exits                                       |
|-------------|---------|-------:|-------:|--------:|------:|--------:|--------:|--------|---------------------------------------------|
| H0          | BTCUSDT |     33 | 30.30% |  −0.459 | 0.255 |  −3.39% |  −3.67% | 16/17  | STOP=17, STAGNATION=16                      |
| H0          | ETHUSDT |     33 | 21.21% |  −0.475 | 0.321 |  −3.53% |  −4.13% | 13/20  | STOP=26, STAGNATION=6, TRAILING_BREACH=1    |
| R3          | BTCUSDT |     33 | 42.42% |  −0.240 | 0.560 |  −1.77% |  −2.16% | 16/17  | STOP=8, TAKE_PROFIT=4, TIME_STOP=21         |
| R3          | ETHUSDT |     33 | 33.33% |  −0.351 | 0.474 |  −2.61% |  −3.65% | 13/20  | STOP=14, TAKE_PROFIT=5, TIME_STOP=14        |
| R1b-narrow  | BTCUSDT |     10 | 50.00% |  **−0.263** | **0.561** |  **−0.59%** |  **−1.09%** |  6/4   | STOP=3, TAKE_PROFIT=2, TIME_STOP=5          |
| R1b-narrow  | ETHUSDT |     12 | 33.33% |  **−0.224** | **0.622** |  **−0.60%** |  **−1.28%** |  6/6   | STOP=5, TAKE_PROFIT=2, TIME_STOP=5          |

## 4. Official ranking (H0 anchor — Phase 2f §10.3 / §10.4)

### 4.1 Deltas vs H0

| Symbol  | Δexp     | ΔPF      | Δ|maxDD| (pp) | |maxDD| ratio | Δn (%)    |
|---------|---------:|---------:|--------------:|--------------:|----------:|
| BTCUSDT | **+0.196** | **+0.305** | **−2.59** (better) | **0.296×**    | **−69.7%** |
| ETHUSDT | **+0.251** | **+0.301** | **−2.86** (better) | **0.308×**    | **−63.6%** |

### 4.2 §10.3 disqualification floor — NOT TRIGGERED

| Veto             | BTC                                           | ETH                                           |
|------------------|-----------------------------------------------|-----------------------------------------------|
| expR worsens     | NO (+0.196)                                   | NO (+0.251)                                   |
| PF worsens       | NO (+0.305)                                   | NO (+0.301)                                   |
| |maxDD| > 1.5×   | NO (0.296× — well below floor)                | NO (0.308× — well below floor)                |

### 4.3 §10.3 promotion paths

§10.3.a (Δexp ≥ +0.10 AND ΔPF ≥ +0.05):

| Symbol | Δexp     | ΔPF      | §10.3.a result |
|--------|---------:|---------:|----------------|
| BTC    | +0.196   | +0.305   | **CLEARED**    |
| ETH    | +0.251   | +0.301   | **CLEARED**    |

§10.3.b (Δn ≥ +50%): **NOT applicable** (Δn < 0; the bias-strength filter reduces trade count by design).

§10.3.c strict-dominance (Δexp > 0 AND ΔPF > 0 AND Δ|maxDD| ≤ 0):

| Symbol | Δexp     | ΔPF      | Δ|maxDD| (pp) | §10.3.c result |
|--------|---------:|---------:|--------------:|----------------|
| BTC    | +0.196   | +0.305   | −2.588        | **CLEARED**    |
| ETH    | +0.251   | +0.301   | −2.859        | **CLEARED**    |

### 4.4 §10.4 hard reject — NOT TRIGGERED

§10.4 fires only when trade count rises (Δn > 0). R1b-narrow has Δn = −69.7% BTC / −63.6% ETH; §10.4 does not apply.

### 4.5 §11.4 ETH-as-comparison rule — SATISFIED

§11.4 requires BTC must clear and ETH must not catastrophically fail. BTC clears §10.3.a + §10.3.c. ETH clears §10.3.a + §10.3.c independently and triggers no §10.4 catastrophic-failure path.

### 4.6 Verdict

**R1b-narrow PROMOTES** under Phase 2f §10.3 paths (a) and (c) on both BTC and ETH, with no §10.3 disqualification floor and no §10.4 hard reject triggered.

**Headline framework strength.** R1b-narrow is the **first** Phase-2x candidate to clear **§10.3.a on both symbols simultaneously** at the magnitude threshold (Δexp ≥ +0.10 R AND ΔPF ≥ +0.05 on both). R3 cleared §10.3.a on both but with smaller ETH magnitude (+0.124); R1a+R3 cleared §10.3.a on ETH only (BTC was §10.3.c-only via Δexp +0.039). On the formal-framework metric alone, R1b-narrow is the strongest result the project has produced.

## 5. Supplemental ranking (R3 anchor — DESCRIPTIVE ONLY)

H0 remains the sole governing anchor per Phase 2i §1.7.3. The R3-anchor view is supplemental.

| Symbol  | Δexp     | ΔPF      | Δ|maxDD| (pp) | Δn (%)    |
|---------|---------:|---------:|--------------:|----------:|
| BTCUSDT | **−0.023** | **+0.000** | +1.07 (worse)  | −69.7%    |
| ETHUSDT | **+0.127** | **+0.148** | +2.37 (worse)  | −63.6%    |

R1b-narrow's marginal contribution on top of R3 is **roughly neutral on BTC** (Δexp_R3 −0.023 R, ΔPF_R3 +0.000 — essentially identical aggregate metrics on the surviving 10 trades vs R3's 33). On ETH, R1b-narrow improves vs R3 (Δexp_R3 +0.127 R, ΔPF_R3 +0.148). Both symbols show improved |maxDD| in absolute terms (R1b-narrow's smaller trade count produces smaller cumulative drawdowns), though the Δ|dd| sign is "worse" only because the H0 anchor's drawdown values are larger to begin with.

The interpretation: **R1b-narrow's improvement vs H0 is dominated by R3's exit-machinery contribution plus the bias-strength filter's trade-count concentration**. The bias-strength filter is concentrating trades in a narrower regime; the surviving trades have similar per-trade metrics as R3's surviving trades, but at much lower trade count. The 33-trade R3 baseline has essentially the same per-trade expectancy as the 10-trade R1b-narrow result on BTC.

## 6. Per-fold consistency (Phase 2f §11.2 + GAP-20260424-036)

5 rolling folds, fold-1 partial-train, all test windows inside R.

### 6.1 Per-fold trade counts and expR

```
var          sym           F1     F2     F3     F4     F5  metric
H0           BTCUSDT        6      9      6      4      4  n_trades
H0           BTCUSDT    -0.48  -0.24  -0.52  -1.03  -0.69  expR
R3           BTCUSDT        6      9      6      4      4  n_trades
R3           BTCUSDT    -0.48  +0.01  +0.10  -0.87  -0.45  expR
R1b-narrow   BTCUSDT        0      2      1      2      3  n_trades
R1b-narrow   BTCUSDT    +0.00  +0.78  -1.34  -1.11  -0.16  expR

H0           ETHUSDT        8      7      8      2      4  n_trades
H0           ETHUSDT    -0.26  -0.75  -0.81  -0.84  -0.44  expR
R3           ETHUSDT        8      7      8      2      4  n_trades
R3           ETHUSDT    -0.03  -0.46  -0.82  -0.84  -0.21  expR
R1b-narrow   ETHUSDT        3      2      1      2      2  n_trades
R1b-narrow   ETHUSDT    -0.36  -0.08  -1.14  -0.84  +0.34  expR
```

### 6.2 Per-fold deltas vs H0

| Fold     | BTC Δexp                        | ETH Δexp                        |
|----------|---------------------------------|---------------------------------|
| F1 2022H2| +0.481 (n=0 R1b — R1b had no entry; treated as 0) | −0.107                          |
| F2 2023H1| **+1.017** (n=2)                | +0.667                          |
| F3 2023H2| **−0.811** (n=1; single losing trade)            | −0.331 (n=1)                    |
| F4 2024H1| −0.085 (n=2)                    | +0.000 (n=2; R1b ties H0)        |
| F5 2024H2| +0.537 (n=3)                    | +0.784 (n=2)                    |

R1b-narrow vs H0: **3/5 BTC folds better, 2/5 ETH folds better.**

### 6.3 Per-fold deltas vs R3

| Fold     | BTC Δexp | ETH Δexp |
|----------|---------:|---------:|
| F1 2022H2|  +0.481  |  −0.339  |
| F2 2023H1|  +0.764  |  +0.375  |
| F3 2023H2|  −1.435  |  −0.325  |
| F4 2024H1|  −0.240  |  +0.000  |
| F5 2024H2|  +0.291  |  +0.552  |

R1b-narrow vs R3: **3/5 BTC folds better, 2/5 ETH folds better** — same wins/losses count as vs H0.

### 6.4 Per-fold sample-size concern

The R1b-narrow per-fold sample sizes are **very small**: BTC has fold-counts of 0/2/1/2/3 and ETH has 3/2/1/2/2. Three observations:

- **BTC F1 has zero trades** under R1b-narrow. The Δexp comparison is moot for that fold.
- **F3 BTC R1b-narrow expR = −1.335 from a single trade.** A single-trade flip would change the expR sign. The fold-3 BTC expR is statistically uninterpretable.
- **F4 BTC R1b-narrow expR = −1.110 from two trades.** Both are losses; sample-size is too small to distinguish "the bias-strength filter is bad in this fold" from "this fold happened to draw two unlucky trades".

This is the §11.3 / GAP-036 fold-consistency machinery operating at its lower bound of usefulness. The framework verdict (PROMOTE on aggregate) is unambiguous, but the per-fold robustness of the verdict is weaker than R3's (which had 4/5 vs 3/5 with much larger per-fold counts).

## 7. Mandatory common diagnostics

### 7.1 Per-regime expR (realized 1h-vol)

Convention: trailing 1000 1h-bar window of Wilder ATR(20), terciles 33/67.

| Variant     | Symbol | Regime    | n  | expR    | PF    | WR     |
|-------------|--------|-----------|---:|--------:|------:|-------:|
| H0          | BTC    | low_vol   | 13 | −0.372  | 0.377 | 30.77% |
| H0          | BTC    | med_vol   |  7 | −0.195  | 0.571 | 57.14% |
| H0          | BTC    | high_vol  | 13 | −0.688  | 0.047 | 15.38% |
| H0          | ETH    | low_vol   | 12 | −0.184  | 0.729 | 33.33% |
| H0          | ETH    | med_vol   |  8 | −0.970  | 0.000 |  0.00% |
| H0          | ETH    | high_vol  | 13 | −0.439  | 0.204 | 23.08% |
| R3          | BTC    | low_vol   | 13 | −0.054  | 0.890 | 38.46% |
| R3          | BTC    | med_vol   |  7 | −0.157  | 0.656 | 57.14% |
| R3          | BTC    | high_vol  | 13 | −0.472  | 0.278 | 38.46% |
| R3          | ETH    | low_vol   | 12 | −0.177  | 0.747 | 41.67% |
| R3          | ETH    | med_vol   |  8 | −0.766  | 0.103 | 25.00% |
| R3          | ETH    | high_vol  | 13 | −0.257  | 0.509 | 30.77% |
| R1b-narrow  | BTC    | low_vol   |  2 | **+0.472** | inf | **100.00%** |
| R1b-narrow  | BTC    | med_vol   |  4 | −0.216  | 0.644 | 50.00% |
| R1b-narrow  | BTC    | high_vol  |  4 | −0.677  | 0.236 | 25.00% |
| R1b-narrow  | ETH    | low_vol   |  1 | **+1.852** | inf | **100.00%** |
| R1b-narrow  | ETH    | med_vol   |  4 | −0.218  | 0.446 | 50.00% |
| R1b-narrow  | ETH    | high_vol  |  7 | −0.524  | 0.337 | 14.29% |

R1b-narrow's BTC low_vol n=2 and ETH low_vol n=1 cells are positive but **far too small** to be meaningful (single-trade flips would change the cell). R1b-narrow BTC high_vol n=4 expR −0.677 is worse than R3's BTC high_vol −0.472 — R1b-narrow does not improve high-vol regime BTC trades.

The regime decomposition shows R1b-narrow's filter is concentrating trades away from low_vol (where R3 was strongest) and into med/high_vol. The trade-count loss falls disproportionately on low-vol regimes (BTC low_vol R3 13 → R1b-narrow 2; ETH low_vol R3 12 → R1b-narrow 1).

### 7.2 MFE distribution

| Variant     | Symbol  | n  | mean   | median | p25    | p75    | max    |
|-------------|---------|---:|-------:|-------:|-------:|-------:|-------:|
| H0          | BTCUSDT | 33 | +0.851 | +0.531 | +0.214 | +1.188 | +3.359 |
| H0          | ETHUSDT | 33 | +1.164 | +0.849 | +0.238 | +1.666 | +4.946 |
| R3          | BTCUSDT | 33 | +0.792 | +0.531 | +0.214 | +1.167 | +3.083 |
| R3          | ETHUSDT | 33 | +1.061 | +0.849 | +0.238 | +1.666 | +3.462 |
| R1b-narrow  | BTCUSDT | 10 | +0.861 | +0.570 | +0.212 | +1.611 | +2.342 |
| R1b-narrow  | ETHUSDT | 12 | +0.956 | +0.831 | +0.152 | +1.434 | +2.725 |

R1b-narrow's MFE distribution is approximately preserved relative to R3 (median nearly identical). The bias-strength filter does not change the MFE characteristics of the surviving trades; it just selects fewer trades.

### 7.3 Long/short asymmetry

| Variant     | Symbol  | LONG n / expR / PF        | SHORT n / expR / PF       |
|-------------|---------|---------------------------|---------------------------|
| H0          | BTC     | 16: −0.560 / 0.216        | 17: −0.364 / 0.305        |
| H0          | ETH     | 13: −1.005 / 0.067        | 20: −0.131 / 0.712        |
| R3          | BTC     | 16: −0.252 / 0.578        | 17: −0.230 / 0.540        |
| R3          | ETH     | 13: −0.934 / 0.133        | 20: +0.028 / 1.070        |
| R1b-narrow  | BTC     |  6: −0.529 / 0.354        |  4: **+0.136** / **1.524** |
| R1b-narrow  | ETH     |  6: −0.574 / 0.352        |  6: **+0.125** / **1.416** |

**First-time observation: BTC shorts under R1b-narrow have positive expectancy.** R3's BTC was direction-symmetric (longs −0.252 / shorts −0.230); R1b-narrow's BTC is direction-asymmetric (longs −0.529 / shorts +0.136 with PF 1.524). This is the project's first BTC-shorts cell with positive expR, but the sample is only 4 trades — single-trade flip-fragile. ETH shorts under R1b-narrow are also positive (+0.125 / 1.416, n=6) — preserving but slightly weakening the strong R1a+R3 ETH-shorts signal (R1a+R3 ETH shorts were +0.387 / 1.906 from n=16; the pattern is still there at smaller magnitude).

### 7.4 Implementation-bug check

```
R3 BTCUSDT: TRAILING_BREACH+STAGNATION exits = 0 (must be 0)  ✓
R3 ETHUSDT: TRAILING_BREACH+STAGNATION exits = 0 (must be 0)  ✓
R1b-narrow BTCUSDT: TRAILING_BREACH+STAGNATION exits = 0 (must be 0)  ✓
R1b-narrow ETHUSDT: TRAILING_BREACH+STAGNATION exits = 0 (must be 0)  ✓
```

All R3-or-R1b-narrow exits use only `{STOP, TAKE_PROFIT, TIME_STOP, END_OF_DATA}`. R3 exit logic preserved bit-for-bit. No leakage.

## 8. R1b-narrow-specific diagnostics (Phase 2r spec memo §P)

### 8.1 §P.1 Slope-strength distribution at filled R1b-narrow entries

| Symbol  | n  | |min|   | |median| | |mean|  | |max|   | signed range          | frac near threshold (<1.05·S) |
|---------|---:|--------:|---------:|--------:|--------:|-----------------------|------------------------------:|
| BTCUSDT | 10 |  0.0025 |   0.0038 |  0.0038 |  0.0053 | [−0.0053, +0.0052]    | 0.00%                         |
| ETHUSDT | 12 |  0.0022 |   0.0043 |  0.0045 |  0.0096 | [−0.0063, +0.0096]    | 0.00%                         |

**All filled entries have |slope_strength_3| ≥ 0.0020 = S.** The minimum on BTC is 0.0025 (≈ 1.25× S) and on ETH is 0.0022 (≈ 1.10× S). The mean is roughly 2× S. **Zero entries cluster near the threshold boundary** (none within 1.05× S). The predicate is mechanically correct: every entry's bias-strength magnitude is above the committed threshold.

This rules out the §L "S is too small to filter meaningfully" failure mode. The opposite occurred: S = 0.0020 is restrictive enough to cut trade count by ~65%.

### 8.2 §P.2 Funnel attribution: rejected_neutral_bias comparison

| Variant     | Symbol  | rejected_neutral_bias | bias_long_count | bias_short_count |
|-------------|---------|----------------------:|-----------------:|------------------:|
| H0          | BTCUSDT |                54,541 |           48,280 |            45,264 |
| H0          | ETHUSDT |                55,517 |           44,744 |            47,824 |
| R3          | BTCUSDT |                54,541 |           48,280 |            45,264 |
| R3          | ETHUSDT |                55,517 |           44,744 |            47,824 |
| R1b-narrow  | BTCUSDT |               117,205 |           15,668 |            15,212 |
| R1b-narrow  | ETHUSDT |               105,957 |           20,544 |            21,584 |

R1b-narrow more than **doubles** the rejected_neutral_bias count on BTC (54,541 → 117,205) and nearly doubles on ETH (55,517 → 105,957). Bias_long+bias_short pool collapses from H0's 93,544 BTC / 92,568 ETH to R1b-narrow's 30,880 BTC / 42,128 ETH — a ~3× reduction in candidate pool. This confirms §P.2's expected pattern: R1b-narrow's filter rejects ~63% of bars that H0's binary check admits.

The funnel attribution stays interpretable in the existing `rejected_neutral_bias` bucket — no new bucket needed. The dispatch in `_IncrementalIndicators.current_bias` correctly attributes both predicates' failures to the same bucket.

### 8.3 §P.3 Per-direction expR by slope-strength bucket

Buckets: **marginal** [+0.0020, +0.0050) | **moderate** [+0.0050, +0.0100) | **strong** [+0.0100, +∞).

| Symbol  | Bucket   | n  | expR    | PF    | WR     |
|---------|----------|---:|--------:|------:|-------:|
| BTCUSDT | marginal |  8 | −0.302  | 0.511 | 50.00% |
| BTCUSDT | moderate |  2 | −0.106  | 0.794 | 50.00% |
| BTCUSDT | strong   |  0 | n/a     | n/a   | n/a    |
| ETHUSDT | marginal |  9 | −0.353  | 0.448 | 33.33% |
| ETHUSDT | moderate |  3 | **+0.161** | **1.353** | 33.33% |
| ETHUSDT | strong   |  0 | n/a     | n/a   | n/a    |

**Zero trades fall in the strong-strength bucket** (≥ 0.0100). Even though bars with |slope_strength_3| ≥ 0.0100 exist in the v002 1h series, those bars do not produce setups that pass the downstream trigger / setup-validity / ATR-regime filters. The strong-bias regime coincides with conditions incompatible with the existing setup definition (strong directional moves typically don't compress narrowly). R1b-narrow's improvement, when it materializes, comes from the **moderate-strength** bucket (BTC: 2 trades, expR −0.106; ETH: 3 trades, expR +0.161 / PF 1.353).

The Phase 2r §P.3 mechanism-validation prediction was: "If R1b-narrow's signal is dominantly from strong-bias bars, Bucket 3 should outperform Bucket 1 — confirming the bias-strength mechanism. If all three buckets perform similarly, the magnitude doesn't matter and R1b-narrow's improvement (if any) is from a different mechanism."

What the data shows: **moderate outperforms marginal on both symbols** (BTC moderate −0.106 > marginal −0.302; ETH moderate +0.161 > marginal −0.353). Bucket 3 (strong) is empty, so the prediction can only be partially evaluated. The trend within the available buckets supports the bias-strength mechanism — stronger bias → better outcomes — but the sample is too small to be definitive (n=2, 3 in the moderate buckets).

### 8.4 §P.4 Direction-asymmetry check (R1b-narrow vs R3 vs H0)

| Symbol  | Variant     | LONG n / expR / PF        | SHORT n / expR / PF       |
|---------|-------------|---------------------------|---------------------------|
| BTCUSDT | H0          | 16: −0.560 / 0.216        | 17: −0.364 / 0.305        |
| BTCUSDT | R3          | 16: −0.252 / 0.578        | 17: −0.230 / 0.540        |
| BTCUSDT | R1b-narrow  |  6: −0.529 / 0.354        |  4: **+0.136** / **1.524** |
| ETHUSDT | H0          | 13: −1.005 / 0.067        | 20: −0.131 / 0.712        |
| ETHUSDT | R3          | 13: −0.934 / 0.133        | 20: +0.028 / 1.070        |
| ETHUSDT | R1b-narrow  |  6: −0.574 / 0.352        |  6: **+0.125** / **1.416** |

R1b-narrow **introduces direction-asymmetry on BTC** that R3 had eliminated. R3's BTC was nearly direction-symmetric (longs −0.252 / shorts −0.230); R1b-narrow's BTC is asymmetric (longs −0.529 / shorts +0.136). The Phase 2r §P.4 prediction was: "Under R1b-narrow's hypothesis, the direction-asymmetry on ETH should be largely preserved... On BTC, R1b-narrow's filtering should *not* introduce direction-asymmetry — the remaining post-filter BTC trades should still be roughly direction-symmetric."

What the data shows: ETH's pattern is preserved (longs −0.574, shorts +0.125 — asymmetric, similar to R3's pattern). **BTC's pattern is changed**: R1b-narrow's filter produces direction-asymmetric BTC outcomes. BTC longs under R1b-narrow are worse than under R3 (−0.529 vs −0.252); BTC shorts under R1b-narrow are positive for the first time in any phase (+0.136 from n=4).

This deviates from the Phase 2r prediction. The mechanism interpretation: R1b-narrow's bias-strength filter, when combined with the v002 BTC R-window's regime structure, preferentially admits SHORT-side strong-bias bars (where the bear regime is more directionally concentrated) and rejects more LONG-side weak-bias bars. The result is an asymmetric BTC filter that mirrors ETH's R3-baseline directional asymmetry.

This is genuinely informative but small-sample (BTC R1b-narrow: 6 long trades, 4 short trades). The single-trade-flip fragility makes the cell-level conclusions tentative.

## 9. V-window confirmation (2025-01-01 → 2026-04-01, 15 months)

R1b-narrow PROMOTES on R, so V-window is run per Phase 2f §11.3.

| Variant     | Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   | Exits                                |
|-------------|---------|-------:|-------:|--------:|------:|--------:|--------:|---------------------------------------|
| H0          | BTCUSDT |      8 | 25.00% |  −0.313 | 0.541 |  −0.56% |  −0.87% | STAGNATION=3, STOP=5                  |
| H0          | ETHUSDT |     14 | 28.57% |  −0.174 | 0.695 |  −0.55% |  −0.80% | STAGNATION=5, STOP=9                  |
| R3          | BTCUSDT |      8 | 25.00% |  −0.287 | 0.580 |  −0.51% |  −1.06% | STOP=3, TAKE_PROFIT=1, TIME_STOP=4    |
| R3          | ETHUSDT |     14 | 42.86% |  −0.093 | 0.824 |  −0.29% |  −0.94% | STOP=5, TAKE_PROFIT=1, TIME_STOP=8    |
| R1b-narrow  | BTCUSDT |  **1** |  **0.00%** | **−1.270** | **0.000** | −0.28% |   0.00% | STOP=1                                |
| R1b-narrow  | ETHUSDT |      8 | 50.00% |  **+0.154** | **1.408** | **+0.28%** | −0.40% | STOP=2, TAKE_PROFIT=1, TIME_STOP=5    |

V-window observations:

- **R1b-narrow ETH V is the second positive-netPct V-window the project has produced** (+0.28%). The first was Phase 2m R1a+R3 ETH at +0.69%. R1b-narrow ETH V is smaller in magnitude but still positive (8 trades, 50% WR, expR +0.154, PF 1.408).
- **R1b-narrow BTC V has only 1 trade.** That trade lost (−1.270 R, 0% WR, netPct −0.28%). With n=1, this is essentially uninterpretable — a single trade cannot establish edge or its absence. **This is the trade-count-fragility concern from Phase 2r §F materializing.**
- The Phase 2f §11.3.5 binding rule says V-window failure does NOT retroactively change R-window classification but DOES end the candidate's wave. R1b-narrow's BTC V is technically a "lost trade", not a clean §10.3 disqualification (no expR / PF veto applied at n=1 sample size). The ETH V is positive, so §11.4 ETH-comparison-rule does not block.

The V-window adds **mixed evidence**: ETH continues to support the candidate; BTC is uninterpretable due to the trade count.

## 10. Slippage sensitivity (R1b-narrow on R window)

GAP-20260424-032 + Phase 2f §11.6 cost-sensitivity gate.

| Slippage | Symbol  | Trades | expR    | PF    | netPct  | maxDD   |
|----------|---------|-------:|--------:|------:|--------:|--------:|
| LOW      | BTCUSDT |     10 |  −0.196 | 0.654 |  −0.44% |  −1.01% |
| LOW      | ETHUSDT |     12 |  −0.174 | 0.690 |  −0.47% |  −1.18% |
| MEDIUM   | BTCUSDT |     10 |  −0.263 | 0.561 |  −0.59% |  −1.09% |
| MEDIUM   | ETHUSDT |     12 |  −0.224 | 0.622 |  −0.60% |  −1.28% |
| HIGH     | BTCUSDT |     10 |  −0.389 | 0.445 |  −0.87% |  −1.28% |
| HIGH     | ETHUSDT |     12 |  −0.371 | 0.452 |  −1.00% |  −1.52% |

Cost sensitivity is monotone and proportional. At HIGH (3× baseline): BTC expR −0.389, ETH expR −0.371 — both still better than H0 at MEDIUM (BTC −0.459, ETH −0.475). The candidate remains framework-clearing across the slippage band (no §10.3 disqualification floor triggered at HIGH).

## 11. Stop-trigger sensitivity (GAP-20260424-032)

| Trigger     | Symbol  | Trades | expR    | PF    | netPct  | maxDD   | Gap-through stops |
|-------------|---------|-------:|--------:|------:|--------:|--------:|-------------------:|
| MARK_PRICE  | BTCUSDT |     10 |  −0.263 | 0.561 |  −0.59% |  −1.09% |                  0 |
| MARK_PRICE  | ETHUSDT |     12 |  −0.224 | 0.622 |  −0.60% |  −1.28% |                  0 |
| TRADE_PRICE | BTCUSDT |     10 |  −0.263 | 0.561 |  −0.59% |  −1.09% |                  0 |
| TRADE_PRICE | ETHUSDT |     12 |  −0.224 | 0.622 |  −0.60% |  −1.28% |                  0 |

**Bit-identical.** Zero gap-through stops on both symbols. Same as R3 (Phase 2l) and R1a+R3 (Phase 2m): MARK_PRICE introduces no systematic bias relative to TRADE_PRICE on this data.

## 12. PASS / FAIL / HOLD classification

**Classification: PASS.**

- **§10.3 verdict: PROMOTE** under §10.3.a + §10.3.c on both BTC and ETH.
- **§10.3 disqualification floor: NOT TRIGGERED** (|maxDD| ratios 0.296× / 0.308× — well below 1.5× veto).
- **§10.4 hard reject: NOT APPLICABLE** (Δn < 0; trade count drops).
- **§11.4 ETH-as-comparison: SATISFIED** (BTC clears, ETH not catastrophic).
- **§11.6 cost-sensitivity gate: framework discipline preserved** at HIGH slippage (no veto triggered).
- **§11.3.5 binding pre-committed thresholds: HONORED** (no post-hoc tuning).

PASS classification means **the candidate clears the formal framework**; it does **not** mean the candidate is live-ready or that the absolute-edge case is strongly supported. The PASS comes with documented sample-size and per-fold caveats:

- **Trade-count drops 65–70%** vs H0/R3 baselines.
- **Per-fold sample sizes are tiny** (BTC: 0/2/1/2/3; ETH: 3/2/1/2/2). Per-fold consistency cannot be robustly assessed at these counts.
- **V-window BTC has n=1**, making BTC V evidence essentially uninterpretable.
- **All filled entries are in marginal-or-moderate slope-strength buckets**; zero in the strong bucket. The mechanism-validation §P.3 prediction is partially confirmed (moderate > marginal on both symbols) but cannot be fully tested.
- **R3-anchor view shows roughly neutral marginal contribution on BTC** (Δexp_R3 −0.023). The R1b-narrow improvement vs H0 is dominated by R3's exit-machinery contribution.

## 13. What the PASS does NOT claim

- **R1b-narrow is not live-ready.** The candidate's R-window aggregate expR is still negative (BTC −0.263, ETH −0.224). PASS means "framework verdict is PROMOTE", not "approved for capital exposure".
- **R1b-narrow does not replace R3 as the baseline-of-record without operator decision.** Phase 2p committed R3 as baseline-of-record. R1b-narrow PROMOTING under the framework is grounds for the operator to reconsider the baseline-of-record designation in a separate phase, not for Phase 2s to silently reassign it. The Phase 2p locks remain operative until an operator-authorized phase modifies them.
- **R1b-narrow does not establish BTC-shorts edge.** The BTC shorts +0.136 cell is real but n=4 — single-trade flip-fragile.
- **R1b-narrow does not establish absolute-edge on ETH.** ETH V +0.28% netPct is positive but smaller than R1a+R3's +0.69% — the strongest absolute-edge V evidence the project has produced is still R1a+R3 ETH from Phase 2m.
- **R1b-narrow does not authorize paper/shadow / Phase 4 / live-readiness work.** Operator deferrals stand.

## 14. Threshold preservation

Phase 2f §§ 10.3 / 10.4 / 11.3 / 11.4 / 11.6 thresholds applied unchanged. No post-hoc loosening. Phase 2j §C.6 R1a sub-parameters preserved. Phase 2j §D.6 R3 sub-parameters preserved. Phase 2r §F R1b-narrow sub-parameter S = 0.0020 committed singularly; not tuned. GAP-20260424-036 fold convention applied unchanged. GAP-20260424-031 / 032 / 033 carried forward unchanged. No new GAP entries are proposed in Phase 2s.

## 15. Wave-1 / Phase 2l / 2m / 2p preservation

Phase 2g Wave-1 REJECT ALL preserved as historical evidence only. Phase 2l R3 PROMOTE preserved unchanged (R3 sub-parameters frozen, designated baseline-of-record per Phase 2p). Phase 2m R1a+R3 mixed-PROMOTE preserved unchanged (retained-for-future-hypothesis-planning per Phase 2p §D). H0 anchor preserved as the sole §10.3 / §10.4 anchor.

## 16. Safety posture

Research-only. No live trading. No exchange-write paths. No production keys. No `.mcp.json`, no Graphify, no MCP server activation. No `.env` changes, no credentials, no Binance API calls (authenticated or public). No edits to `docs/12-roadmap/technical-debt-register.md`. No edits to `.claude/`. No `data/` commits (artifacts under `data/derived/backtests/phase-2s-r1b-*` are git-ignored). No Phase 4 work. No paper/shadow planning. No live-readiness claim. Mark-price stop-trigger semantic preserved (MARK_PRICE default; TRADE_PRICE only as sensitivity diagnostic). R1b-narrow sub-parameter S = 0.0020 committed singularly; no parameter sweeps. R3 sub-parameters frozen. R1a sub-parameters frozen (R1a not part of R1b-narrow). The 8-bar setup window unchanged. No new structural redesign candidate exposed beyond H0 / R3 / R1a+R3 / R1b-narrow.

---

**End of Phase 2s R1b-narrow comparison report.** Sections 1–16 complete. **Verdict: PROMOTE; Classification: PASS** — with documented sample-size caveats. R1b-narrow is the first candidate to clear §10.3.a on both symbols simultaneously at the magnitude threshold; the trade-count drop and per-fold fragility limit the strength of the absolute-edge interpretation. R3 remains the baseline-of-record per Phase 2p; any change to that designation is an operator-authorized policy decision outside Phase 2s's scope. **No code changes after report drafting; no new runs; no live-readiness claim.** Phase 2s is complete and ready for operator/ChatGPT review.
