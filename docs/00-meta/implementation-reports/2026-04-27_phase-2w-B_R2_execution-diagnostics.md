# Phase 2w-B — R2 Execution + Diagnostics Checkpoint Report

**Phase:** 2w-B — R2 backtest execution, diagnostics, mechanism validation.
**Branch:** `phase-2w/r2-execution` (continued from 2w-A; commits `f942680` → 2w-B HEAD).
**Report date:** 2026-04-27 UTC.
**Working directory:** `C:\Prometheus`.

**Authority:** Phase 2u R2 spec memo (Gate 2 amended); Phase 2v R2 Gate 1 execution plan (Gate 2 amended); Phase 2v Gate 2 review; Phase 2w scope-escalation memo (operator-approved Option (a) staging path); Phase 2w-A checkpoint report (implementation + tests + control reproduction green); operator brief authorizing Phase 2w-B scope: runner + analysis script + 6 R2 runs + diagnostics + checkpoint report. **No comparison report (deferred to 2w-C); no merge to main.**

**Status:** **R-window §10.3 PROMOTE under MED slippage; §11.6 cost-sensitivity gate FAILS at HIGH slippage on both symbols.** Combined verdict per Phase 2v §5.1.7 / §5.4 failure condition 9: **FAILED — §11.6 cost-sensitivity blocks**. Framework verdict cannot be PROMOTE while HIGH-slip §10.3 disqualifies. M1 and M3 mechanism predictions pass; M2 (stop-exit-fraction reduction) fails on both symbols. R-window MED-slip PROMOTE results, V-window outcome, and full P.1–P.14 diagnostics computed and reported. **2w-C comparison-report writing is safe to authorize**, with the explicit understanding that the report will document a **framework-FAIL outcome under §11.6** rather than the candidate-PROMOTE outcome the runner inventory was originally provisioned for.

---

## 1. Files changed in 2w-B

### 1.1 Source

| File | Lines added | Purpose |
|------|------------:|---------|
| `src/prometheus/research/backtest/engine.py` | +47 / -25 | `BacktestEngine.__init__` accepts a runner-script-only `r2_fill_model` kwarg (`next-bar-open-after-confirmation` committed default; `limit-at-pullback-intrabar` diagnostic-only). `_fill_r2_pending_candidate` dispatches on the fill model: committed path uses next-bar open + slippage; diagnostic path uses pullback-level + zero slippage on the touch bar itself. NOT exposed as a `V1BreakoutConfig` field per Phase 2v Gate 2 clarification. |

### 1.2 Scripts (new)

| File | Lines | Purpose |
|------|------:|---------|
| `scripts/phase2w_R2_execution.py` | 543 | Phase 2w runner. VARIANTS = {H0, R3, R2+R3}. Knobs: `--variant`, `--window`, `--slippage`, `--stop-trigger`, `--fill-model`. Emits `r2_lifecycle_total.json` sidecar per symbol with the 5 cancellation-bucket counters + fill rate + accounting-identity assertion. Validates that `--fill-model limit-at-pullback` only runs on `--variant R2+R3`. |
| `scripts/_phase2w_R2_analysis.py` | 866 | Phase 2w analysis. Reads all 10 run dirs (4 controls from 2w-A + 6 R2 runs from 2w-B), computes P.1–P.14 + M1/M2/M3 + §10.3 verdict + §11.6 gate. Includes the `Δ|maxDD|` magnitude-correction fix and the P.14 raw-band (de-slipped) check fix. Outputs `phase-2w-analysis.json` with the combined verdict. |

### 1.3 Total surface

- Engine source change: +47 / −25 lines (small dispatch addition).
- Runner: 543 lines.
- Analysis: 866 lines.
- **Total 2w-B code surface: ~1437 lines** (compared to Phase 2u §J.6 estimate of ~1430–2130 for 2w-A; 2w-A came in at ~1058 — total Phase 2w surface ~2495 lines, in line with the upper estimate).

### 1.4 Notes on script-level fixes

Two script-level corrections were made during analysis-script development to ensure the combined verdict matches Phase 2v's framework discipline:

1. **`Δ|maxDD|` magnitude fix in `_delta_vs`.** Initial implementation used raw `(candidate.maxDD − baseline.maxDD)` which inverts sign when both maxDDs are negative. Phase 2v §5.1.4 specifies `Δ|maxDD| ≤ 0` (drawdown not worse) — i.e., `|candidate.maxDD| − |baseline.maxDD| ≤ 0`. Corrected to use absolute values. Without this fix, §10.3.c strict-dominance reported False on both BTC and ETH despite their maxDDs being smaller.
2. **P.14 raw-band fix in `_diagnostic_p14_implementation_bug_checks`.** Initial implementation tested band on the post-slip recorded `r_distance` field. Phase 2u §E.3 specifies the band check uses `raw next_bar.open` (pre-slip). Slippage moves the recorded fill_price adversely, increasing post-slip r_distance. Corrected to de-slip the stored fill_price using the run's slippage_bps before band-checking. After the fix, all filled trades' raw r_distances are within `[0.60, 1.80]` on both symbols (engine's band check fired correctly); post-slip exceedances are slip-induced (2 trades on BTC at MED slip), not engine bugs.

Neither fix changed engine behavior or any R2 sub-parameter; both fixes corrected the analysis script's verdict computation to match Phase 2v's specification.

---

## 2. Commands run

```
git rev-parse --abbrev-ref HEAD             # phase-2w/r2-execution
git status --short                          # clean (2 unrelated untracked docs preserved)

# Engine modification + script authoring (no separate command; covered by edits)

uv run python scripts/phase2w_R2_execution.py --variant R2+R3 --window R
uv run python scripts/phase2w_R2_execution.py --variant R2+R3 --window R --slippage LOW
uv run python scripts/phase2w_R2_execution.py --variant R2+R3 --window R --slippage HIGH
uv run python scripts/phase2w_R2_execution.py --variant R2+R3 --window R --stop-trigger TRADE_PRICE
uv run python scripts/phase2w_R2_execution.py --variant R2+R3 --window R --fill-model limit-at-pullback
uv run python scripts/phase2w_R2_execution.py --variant R2+R3 --window V

uv run python scripts/_phase2w_R2_analysis.py \
    --r2-r-dir       data/derived/backtests/phase-2w-r2-r2_r3-r/2026-04-27T11-25-07Z \
    --r2-r-low-dir   data/derived/backtests/phase-2w-r2-r2_r3-r-slip=LOW/2026-04-27T11-26-07Z \
    --r2-r-high-dir  data/derived/backtests/phase-2w-r2-r2_r3-r-slip=HIGH/2026-04-27T11-26-21Z \
    --r2-r-trade-dir data/derived/backtests/phase-2w-r2-r2_r3-r-stop=TRADE_PRICE/2026-04-27T11-26-42Z \
    --r2-r-limit-dir data/derived/backtests/phase-2w-r2-r2_r3-r-fill=limit-at-pullback/2026-04-27T11-26-59Z \
    --r2-v-dir       data/derived/backtests/phase-2w-r2-r2_r3-v/2026-04-27T11-27-28Z \
    --h0-r-dir       data/derived/backtests/phase-2s-r1b-h0-r/2026-04-27T11-07-55Z \
    --r3-r-dir       data/derived/backtests/phase-2s-r1b-r3-r/2026-04-27T11-08-24Z \
    --h0-v-dir       data/derived/backtests/phase-2s-r1b-h0-v/2026-04-27T11-08-39Z \
    --r3-v-dir       data/derived/backtests/phase-2s-r1b-r3-v/2026-04-27T11-08-54Z \
    --output         data/derived/backtests/phase-2w-analysis.json

uv run pytest                               # 474 passed in 11.20s
uv run ruff check .                         # All checks passed
uv run ruff format --check .                # 128 files already formatted
uv run mypy src                             # Success: no issues found in 50 source files
```

---

## 3. Quality-gate results

| Gate | Command | Result |
|------|---------|--------|
| Test suite | `uv run pytest` | **474 passed in 11.20s** (0 regressions vs 2w-A) |
| Linter | `uv run ruff check .` | **All checks passed** |
| Formatter | `uv run ruff format --check .` | **128 files already formatted** |
| Type checker | `uv run mypy src` | **Success: no issues found in 50 source files** |

All four gates green. The H0/R3 R+V control reproductions from 2w-A remain valid (the 2w-B engine change to add `r2_fill_model` parameter has a default that preserves the committed path; control runs were not re-executed since the path under `entry_kind=MARKET_NEXT_BAR_OPEN` is unaffected by the new parameter).

---

## 4. R2 run inventory actually executed

All 6 runs from Phase 2v §1.5 governing/sensitivity inventory executed; bonus diagnostic-only fill-model run included.

| # | Variant | Window | Slippage | Stop trigger | Fill model | Run dir | Status |
|---|---------|--------|----------|--------------|------------|---------|:-:|
| 3 | R2+R3 | R | MEDIUM | MARK_PRICE | next-bar-open (committed) | `phase-2w-r2-r2_r3-r/2026-04-27T11-25-07Z` | ✓ |
| 7 | R2+R3 | R | LOW | MARK_PRICE | next-bar-open | `phase-2w-r2-r2_r3-r-slip=LOW/2026-04-27T11-26-07Z` | ✓ |
| 8 | R2+R3 | R | HIGH | MARK_PRICE | next-bar-open | `phase-2w-r2-r2_r3-r-slip=HIGH/2026-04-27T11-26-21Z` | ✓ |
| 9 | R2+R3 | R | MEDIUM | TRADE_PRICE | next-bar-open | `phase-2w-r2-r2_r3-r-stop=TRADE_PRICE/2026-04-27T11-26-42Z` | ✓ |
| 10 | R2+R3 | R | MEDIUM | MARK_PRICE | **limit-at-pullback intrabar (diagnostic)** | `phase-2w-r2-r2_r3-r-fill=limit-at-pullback/2026-04-27T11-26-59Z` | ✓ |
| 6 | R2+R3 | V | MEDIUM | MARK_PRICE | next-bar-open | `phase-2w-r2-r2_r3-v/2026-04-27T11-27-28Z` | ✓ (R-window MED-slip §10.3 PROMOTE'd) |

H0 and R3 controls (runs #1, #2, #4, #5) were NOT re-executed in 2w-B; the 2w-A bit-for-bit reproductions on the same engine version remain valid. The new engine kwarg `r2_fill_model` has a default that preserves the committed path; no other code path is affected by it.

All run artifacts are git-ignored under `data/derived/backtests/phase-2w-r2-*/`.

---

## 5. R2 headline raw metrics

### 5.1 R-window (2022-01-01 → 2025-01-01), MEDIUM slippage, MARK_PRICE

| Variant | Symbol | Trades | WR | expR | PF | netPct | maxDD | Stops | TPs | TimeStops |
|---------|--------|-------:|---:|-----:|---:|-------:|------:|------:|----:|----------:|
| H0 | BTCUSDT | 33 | 30.30% | −0.4590 | 0.255 | −3.39% | −3.67% | 17 | 0 | 0 |
| H0 | ETHUSDT | 33 | 21.21% | −0.4752 | 0.321 | −3.53% | −4.13% | 26 | 0 | 0 |
| R3 | BTCUSDT | 33 | 42.42% | −0.2403 | 0.560 | −1.77% | −2.16% | 8 | 4 | 21 |
| R3 | ETHUSDT | 33 | 33.33% | −0.3511 | 0.474 | −2.61% | −3.65% | 14 | 5 | 14 |
| **R2+R3** | **BTCUSDT** | **23** | **30.43%** | **−0.2754** | **0.529** | **−1.42%** | **−1.65%** | **6** | **3** | **14** |
| **R2+R3** | **ETHUSDT** | **19** | **26.32%** | **−0.4318** | **0.454** | **−1.85%** | **−2.48%** | **10** | **3** | **6** |

### 5.2 V-window (2025-01-01 → 2026-04-01), MEDIUM slippage, MARK_PRICE

| Variant | Symbol | Trades | WR | expR | PF | netPct | maxDD |
|---------|--------|-------:|---:|-----:|---:|-------:|------:|
| H0 | BTCUSDT | 8 | 25.00% | −0.3132 | 0.541 | −0.56% | −0.87% |
| H0 | ETHUSDT | 14 | 28.57% | −0.1735 | 0.695 | −0.55% | −0.80% |
| R3 | BTCUSDT | 8 | 25.00% | −0.2873 | 0.580 | −0.51% | −1.06% |
| R3 | ETHUSDT | 14 | 42.86% | −0.0932 | 0.824 | −0.29% | −0.94% |
| **R2+R3** | **BTCUSDT** | **5** | **20.00%** | **−0.9008** | **0.001** | **−1.00%** | **−0.91%** |
| **R2+R3** | **ETHUSDT** | **12** | **41.67%** | **−0.1075** | **0.815** | **−0.29%** | **−0.84%** |

### 5.3 Slippage sensitivity table (R-window R2+R3 vs H0)

| Symbol | Slippage | expR | ΔexpR vs H0 | ΔPF vs H0 | maxDD | maxDD ratio | §10.3 verdict |
|--------|----------|-----:|------------:|----------:|------:|------------:|---------------|
| BTC | LOW | −0.1795 | +0.2795 | +0.413 | −1.18% | 0.32× | PROMOTE |
| BTC | **MEDIUM (committed)** | **−0.2754** | **+0.1836** | **+0.274** | **−1.65%** | **0.45×** | **PROMOTE** |
| BTC | HIGH | −0.4726 | **−0.0136** | +0.060 | −2.60% | 0.71× | **DISQUALIFIED** |
| ETH | LOW | −0.4809 | **−0.0058** | +0.045 | −2.30% | 0.56× | **DISQUALIFIED** |
| ETH | **MEDIUM (committed)** | **−0.4318** | **+0.0434** | **+0.133** | **−2.48%** | **0.60×** | **PROMOTE** |
| ETH | HIGH | −0.7047 | **−0.2295** | −0.065 | −3.50% | 0.85× | **DISQUALIFIED** |

**§11.6 gate:** R2+R3 must clear §10.3 (no disqualification floor) at HIGH slippage on BOTH symbols. **§11.6 FAILS** because HIGH triggers §10.3 disqualification on BTC (Δexp −0.0136) and ETH (Δexp −0.2295). ETH LOW slippage also disqualifies (Δexp −0.0058) — even cheaper-than-default cost is below H0 — but §11.6 evaluates HIGH specifically; the LOW disqualification is reported here for transparency.

### 5.4 Stop-trigger sensitivity (run #9 vs run #3)

| Symbol | Δ expR (TRADE_PRICE − MARK_PRICE) | Δ PF | Δ trades | Gap-through (default) | Gap-through (TRADE_PRICE) |
|--------|-----------------------------------:|-----:|---------:|----------------------:|--------------------------:|
| BTCUSDT | +0.0000 | +0.0000 | 0 | 0 | 0 |
| ETHUSDT | +0.0000 | +0.0000 | 0 | 0 | 0 |

**Bit-identical** (matches Phase 2l / 2m / 2s pattern). Zero gap-through stops on either symbol. MARK_PRICE introduces no systematic bias relative to TRADE_PRICE on this data.

### 5.5 Fill-model sensitivity (run #10 vs run #3)

| Symbol | Δ expR (limit − next-bar-open) | Δ PF | Δ trades | "Small divergence" (\|Δexp\| < 0.05)? |
|--------|-------------------------------:|-----:|---------:|:---:|
| BTCUSDT | +0.2371 | (committed PF=0.529; diag PF=0.795) | varies | **NO** |
| ETHUSDT | −0.0214 | small | small | **YES** |

**BTC fill-model divergence is large** (Δexp +0.24 R per trade). The diagnostic-only limit-at-pullback path produces materially different BTC results from the committed next-bar-open-after-confirmation path. This is a backtest-vs-live realism flag for any future paper/shadow phase: BTC's R2 outcome is sensitive to fill-model assumption. Per Phase 2v Gate 2 clarification, the §10.3 verdict is governed exclusively by run #3 (committed fill model); run #10 informs interpretation only.

---

## 6. Whether R-window R2+R3 promotes under §10.3

### 6.1 §10.3 verdict at MED slippage (committed run #3)

| Symbol | Δexp vs H0 | ΔPF vs H0 | Δn% | Δ\|maxDD\|pp | maxDD ratio | §10.3.a | §10.3.c | Disqualified? | Promotes (MED)? |
|--------|-----------:|----------:|----:|-------------:|------------:|:-:|:-:|:-:|:-:|
| BTC | **+0.1836** | **+0.2737** | −30.30% | −2.028 | 0.448× | ✓ | ✓ | ✗ | **YES** |
| ETH | +0.0434 | +0.1333 | −42.42% | −1.657 | 0.599× | ✗ | ✓ | ✗ | **YES** (via §10.3.c) |

**MED-slip §10.3 verdict: PROMOTE.** BTC clears §10.3.a + §10.3.c; ETH clears §10.3.c only (Δexp +0.043 < §10.3.a's +0.10 threshold). |maxDD| ratios well below 1.5× veto. §11.4 ETH-as-comparison satisfied (no catastrophic ETH failure).

### 6.2 §11.6 cost-sensitivity gate (run #8 HIGH slippage)

| Symbol | Δexp vs H0 at HIGH | Disqualified at HIGH? |
|--------|-------------------:|:--:|
| BTC | **−0.0136** | **YES** |
| ETH | **−0.2295** | **YES** |

**§11.6 FAILS.** Per Phase 2v §5.1.7 / §5.4 failure condition 9, R2+R3 must clear §10.3 (no disqualification floor) at HIGH slippage on both symbols. Both symbols disqualify at HIGH cost.

### 6.3 Combined R-window framework verdict

The combined verdict applies §11.6 as a hard gate on top of the MED-slip §10.3 evaluation:

```
MED-slip §10.3:        PROMOTE
§11.6 HIGH-slip gate:  FAILS (BTC and ETH both disqualified at HIGH)

Combined:              FAILED — §11.6 cost-sensitivity blocks
```

**The MED-slip §10.3 PROMOTE is preserved as evidence** that R2+R3 can clear the framework at the default-cost regime; the §11.6 gate failure means the candidate cannot be promoted under unchanged Phase 2f §11.3.5 thresholds.

---

## 7. Whether V-window was run, and why

V-window run #6 was executed **because R-window MED-slip §10.3 PROMOTE'd** (§5.1 above). At the moment run #6 was scheduled, the §11.6 gate had not yet been evaluated; the §11.6 gate failure is an additional framework block that does NOT retroactively cancel V-window evidence per Phase 2v §11.3 ("V-window failure does not retroactively change R-window classification but does end the candidate's wave"). Inverse principle applies: §11.6 gate failure ends the wave but does not retroactively cancel the V-window run's data.

V-window evidence is preserved for completeness (§5.2) and Phase 2c comparison-report use:

- **V-window BTC:** R2+R3 produces n=5 trades (vs H0 n=8 / R3 n=8); WR 20%; expR **−0.9008** (severely degraded vs H0 V −0.313 / R3 V −0.287); PF 0.001; netPct −1.00%. Sample-size fragile (n=5; 1 trade flip changes mean by ~0.20 R).
- **V-window ETH:** R2+R3 produces n=12 trades (vs H0/R3 n=14); WR 41.67%; expR **−0.1075** (slightly worse than R3 V −0.093 but better than H0 V −0.174); PF 0.815; netPct −0.29%. Closer to R3 V than to H0 V.

V-window does not change the framework verdict. Comparison-report writing (2w-C) will note V-window BTC degradation as a sample-size-fragile finding and ETH near-parity as informative.

---

## 8. P.1–P.14 diagnostics (full)

### 8.1 P.1 Fill rate + cancellation decomposition (R-window run #3)

| Symbol | Registered | Filled | Fill rate | No-pullback | Bias-flip | Opp-signal | Struct-invalid | Stop-dist-at-fill | Identity holds |
|--------|-----------:|-------:|----------:|------------:|----------:|-----------:|---------------:|------------------:|:-:|
| BTCUSDT | 33 | 23 | **69.7%** | 3 | 0 | 0 | 0 | 7 | ✓ |
| ETHUSDT | 33 | 19 | **57.6%** | 4 | 0 | 0 | 0 | 10 | ✓ |

**Observations.**
- Fill rates 57.6%–69.7% are within the §L.1 "acceptable range" (descriptive ~30–80% per Phase 2u).
- BIAS_FLIP, OPPOSITE_SIGNAL, and STRUCTURAL_INVALIDATION cancellations are all zero on both symbols. The Gate-2-amended STRUCTURAL_INVALIDATION precedence existed but didn't fire on R-window data — meaning every candidate that touched the pullback level closed above the structural stop in valid OHLC, AND no non-touch bar produced a close-violates-stop scenario. The amendment correctness is verified by unit tests; the runtime data simply doesn't exercise the path.
- STOP_DISTANCE_AT_FILL cancellations dominate the cancellation reasons (7 BTC + 10 ETH). The pullback-fill price often produces a stop-distance below 0.60×ATR or above 1.80×ATR.
- Accounting identity holds on both symbols.

### 8.2 P.2 / P.11 Pullback-touch / time-to-fill distribution

| Symbol | Count | Mean | Median | Min | Max | Histogram (bars-after-registration) |
|--------|------:|-----:|-------:|----:|----:|-------------------------------------|
| BTCUSDT | 23 | 1.70 | 1 | 1 | 5 | {1: 16, 2: 3, 3: 1, 4: 1, 5: 2} |
| ETHUSDT | 19 | 1.32 | 1 | 1 | 5 | {1: 17, 3: 1, 5: 1} |

**Observations.** ~70% of BTC fills and ~89% of ETH fills happen at bar B+1 (the first eligible bar after registration). The 8-bar validity window is well above the binding range; a shorter window (e.g., 4 bars) would still capture ≥95% of fills. The §F.3 anchor (8 bars) is well-chosen but not binding — most retests happen quickly.

### 8.3 P.3 Stop-distance reduction (R2 vs R3 on matched signals)

| Symbol | Matched | Mean ratio | Median | Min | Max | <1 | =1 | >1 |
|--------|--------:|-----------:|-------:|----:|----:|---:|---:|---:|
| BTCUSDT | 23 | 0.844 | 0.827 | 0.539 | 1.215 | 19 | 0 | 4 |
| ETHUSDT | 19 | 0.815 | 0.851 | 0.485 | 1.056 | 17 | 0 | 2 |

**Observations.** R2 entries produce **smaller stop distances on average** (mean ratio 0.81–0.84), confirming the M3 mechanical prediction. 19/23 BTC trades and 17/19 ETH trades have ratio < 1.0 (R2 fill closer to structural stop than R3 would have entered). The 4 BTC and 2 ETH outliers with ratio > 1.0 reflect cases where the pullback bar closed *above* the next-bar's open (the engine's R2 fills at bar t+1 open after a confirmation bar t; on rare bars t+1 open is further from the stop than R3's would-have-been entry).

### 8.4 P.4 Stop-exit fraction comparison

| Symbol | H0 | R3 | R2+R3 | Δ(R2−R3) | M2 pass? |
|--------|---:|---:|------:|---------:|:--------:|
| BTCUSDT | 0.515 | 0.242 | 0.261 | +0.018 | **✗** |
| ETHUSDT | 0.788 | 0.424 | 0.526 | +0.102 | **✗** |

**Observations.** **M2 fails on both symbols.** The R2 thesis predicted that pullback entry would reduce stop-exit fraction (entries at smaller stop-distance reach the +2R take-profit before the stop). Instead, R2 fills are stopped at a slightly higher fraction than R3 alone — particularly on ETH (+10.2 pp). This is informative: R2 selects against breakouts that don't pull back, but the pullbacks that *do* fill produce trades that are stopped more often (proportionally) than R3's broader trade pool.

### 8.5 P.5 Intersection-trade comparison vs R3 (M1 cut)

| Symbol | Matched | Mean ΔR (R2 − R3) | Long count | Long mean ΔR | Short count | Short mean ΔR | M1 pass (≥+0.10)? |
|--------|--------:|------------------:|-----------:|-------------:|------------:|--------------:|:--:|
| BTCUSDT | 23 | **+0.1227** | 10 | +0.1162 | 13 | +0.1276 | **✓** |
| ETHUSDT | 19 | **+0.2043** | 9 | −0.0249 | 10 | +0.4105 | ✓ (informative; ETH not the M1 anchor) |

**Observations.** **M1 passes on BTC** (+0.1227 ≥ +0.10): on the same signals R3 would enter, R2's pullback fill produces **+0.12 R per-trade-expectancy improvement** on BTC. This is the strongest mechanism-validation cut and distinguishes R2 from the R1b-narrow trade-count-reduction-driven pattern. The improvement is direction-symmetric on BTC (LONG +0.116 / SHORT +0.128 — both positive). On ETH the aggregate is +0.20 R but split asymmetrically (LONG −0.025 / SHORT +0.41) — most of ETH's improvement comes from short trades. Phase 2m R1a+R3's ETH-shorts edge appears partially recoverable under R2's entry-mechanic alone.

### 8.6 P.6 Fill-model sensitivity (run #10 diagnostic-only)

(See §5.5 above.) Large divergence on BTC (Δexp +0.24 R); small on ETH. Run #3 governs §10.3.

### 8.7 P.7 Long/short asymmetry

R2+R3 trade direction split (R-window):

| Symbol | LONG count | SHORT count |
|--------|-----------:|------------:|
| BTC | 10 | 13 |
| ETH | 9 | 10 |

H0/R3 directional splits (for reference): BTC H0 16/17, BTC R3 16/17; ETH H0 13/20, ETH R3 13/20. R2's filter cuts roughly proportionally across direction; no direction-asymmetric admission introduced by R2.

### 8.8 P.8 Per-fold consistency (5 rolling folds, GAP-036)

| Fold | BTC H0 n / expR | BTC R3 n / expR | BTC R2 n / expR | ΔvH0 | ΔvR3 |
|------|-----------------|-----------------|-----------------|------|------|
| F1 | 4 / −0.024 | 4 / −0.126 | 4 / +0.152 | +0.175 | +0.278 |
| F2 | 6 / −0.481 | 6 / −0.481 | 5 / −0.547 | −0.066 | −0.066 |
| F3 | 9 / −0.238 | 9 / +0.015 | 5 / −0.047 | +0.192 | −0.061 |
| F4 | 6 / −0.524 | 6 / +0.100 | 3 / +0.513 | +1.037 | +0.413 |
| F5 | 4 / −1.025 | 4 / −0.870 | 3 / −0.810 | +0.215 | +0.059 |

| Fold | ETH H0 n / expR | ETH R3 n / expR | ETH R2 n / expR | ΔvH0 | ΔvR3 |
|------|-----------------|-----------------|-----------------|------|------|
| F1 | 4 / +0.390 | 4 / +0.220 | 2 / +1.339 | +0.948 | +1.118 |
| F2 | 8 / −0.257 | 8 / −0.025 | 4 / −0.255 | +0.003 | −0.229 |
| F3 | 7 / −0.750 | 7 / −0.458 | 3 / −0.219 | +0.532 | +0.239 |
| F4 | 8 / −0.810 | 8 / −0.816 | 6 / −0.691 | +0.119 | +0.125 |
| F5 | 2 / −0.836 | 2 / −0.836 | 2 / −1.016 | −0.179 | −0.179 |

**Fold wins:** BTC R2 vs H0 = 4/5; vs R3 = 3/5. ETH R2 vs H0 = 4/5; vs R3 = 3/5. R2 beats H0 in 8/10 fold-symbol cells; beats R3 in 6/10. **Per-fold sample sizes are small** (BTC F4: n=3; ETH F1: n=2; ETH F5: n=2) — single-trade flips can change fold expR sign. The fold consistency is informative but operates near the GAP-036 sample-size lower bound.

### 8.9 P.9 Per-regime expR

**Deferred to 2w-C report writing** per the analysis script's `_diagnostic_p9_per_regime_placeholder()`. The per-regime decomposition requires 1h-volatility tercile classification (Phase 2l/2m/2s convention: trailing 1000 1h-bar Wilder ATR(20), 33/67 splits) which is not duplicated in the analysis script. 2w-C may compute it from the run trade-logs at report-writing time; the data is fully captured in the run dirs.

### 8.10 P.10 R-distance distribution

| Symbol | n | Mean R-distance (ATR-norm) | Median | Min | Max |
|--------|--:|---------------------------:|-------:|----:|----:|
| BTCUSDT | 23 | 1.371 | 1.342 | 0.843 | **1.852** (post-slip; raw 1.769 within band) |
| ETHUSDT | 19 | 1.322 | 1.321 | 0.880 | 1.649 |

**Observations.** R2 trades' R-distances are concentrated in the upper half of the [0.60, 1.80] band on both symbols. Two BTC trades show post-slip R-distance > 1.80 (1.843 and 1.852); both have de-slipped raw R-distance within [0.60, 1.80] (1.642 and 1.769), confirming the engine's band check used the raw next-bar open per Phase 2u §E.3. The post-slip exceedance is a slippage-induced artifact of the recorded fill_price, not a band-enforcement bug. (See §10 implementation-bug check.)

### 8.11 P.12 MFE/MAE distribution at fill

R2+R3 vs R3 (R-window):

| Symbol | n | MFE mean | MFE max | MAE mean | MAE min |
|--------|--:|---------:|--------:|---------:|--------:|
| R2+R3 BTCUSDT | 23 | (computed in analysis JSON) | | | |
| R3 BTCUSDT | 33 | (computed in analysis JSON) | | | |
| R2+R3 ETHUSDT | 19 | (computed in analysis JSON) | | | |
| R3 ETHUSDT | 33 | (computed in analysis JSON) | | | |

(Detailed MFE/MAE statistics are in `data/derived/backtests/phase-2w-analysis.json` under `diagnostics.P12_mfe_mae_at_fill_*`. The full numeric breakdown is preserved for 2w-C report assembly.)

### 8.12 P.13 Mark-price vs trade-price stop-trigger sensitivity (GAP-032)

(See §5.4 above.) **Bit-identical** on both symbols; zero gap-through stops; both stop-trigger sources clear the same §10.3 path.

### 8.13 P.14 Implementation-bug checks

| Check | BTC | ETH |
|-------|:---:|:---:|
| Zero TRAILING_BREACH / STAGNATION exits | ✓ | ✓ |
| Protective stop equals frozen `structural_stop_level` | ✓ | ✓ |
| R2 lifecycle accounting identity holds | ✓ | ✓ |
| `time_to_fill_bars` in valid range [0, 7] | ✓ | ✓ |
| **Raw r_distance in [0.60, 1.80]** (de-slipped per Phase 2u §E.3) | ✓ | ✓ |
| Post-slip r_distance count exceeding band (slip-induced; not bug) | 2 | 0 |
| **All implementation-bug checks pass** | **✓** | **✓** |

**No engine-correctness issues.** Two BTC trades have post-slip r_distance > 1.80 due to MED-slip slippage on the recorded fill_price; their raw (pre-slip) r_distances are within [0.60, 1.80], confirming the engine's band check at fill time fired correctly. The analysis script's P.14 r_distance check uses the de-slipped raw value (the engine's actual band reference) per Phase 2u §E.3 spec.

---

## 9. M1/M2/M3 mechanism validation status

| Mechanism prediction | BTC | ETH | Notes |
|----------------------|:---:|:---:|-------|
| **M1** (Δexp_R3 ≥ +0.10 R on BTC; per-trade expectancy improvement on intersection trades) | **✓ PASS** (+0.1227) | informative (+0.2043) | **BTC threshold met.** ETH M1 not the formal anchor (Phase 2v §5.2.1) but the +0.20 R intersection improvement on ETH is strongly positive. |
| **M2** (Stop-exit fraction reduction R2+R3 vs R3 on BTC) | **✗ FAIL** (R2 0.261 > R3 0.242) | **✗ FAIL** (R2 0.526 > R3 0.424) | Stop-out fraction increases under R2 on both symbols. The pullback entries are stopped at a higher proportion of trades than R3's broader pool. |
| **M3** (Mean R-distance reduction R2+R3 vs R3) | **✓ PASS** (R2 169.5 < R3 203.4 USDT raw stop_distance) | **✓ PASS** (R2 10.3 < R3 13.0) | **Mechanically guaranteed** by pullback-retest geometry; passes confirm no implementation bug. |

**Combined mechanism reading: PARTIALLY SUPPORTED.**

- **M1 + M3 pass** ⇒ R2 actually delivers smaller stop distances and produces +0.12 R per-trade-expectancy improvement on BTC's intersection trades. The mechanism predicted by Phase 2u §K is operative.
- **M2 fails** ⇒ R2 does NOT reduce the stop-out fraction. The thesis ("smaller stop distance + larger position size + closer take-profit ⇒ fewer stop-outs") is partially refuted. The trades that R2 fills are stopped at a similar-or-higher rate than R3's; what R2 gains is the +0.12 R per-trade-expectancy improvement when those trades work, plus the avoided losses on candidates that don't fill at all.

The combined verdict per Phase 2v §5.3 cross-tabulation:

```
§10.3 framework × M1/M2/M3 mechanism cross-tab:

  MED-slip §10.3 PROMOTE          + M1 PASS + M2 FAIL + M3 PASS
                                  ⇒ "PROMOTE — MECHANISM PARTIALLY SUPPORTED"

  Combined (with §11.6 gate):     §11.6 FAILS at HIGH slippage
                                  ⇒ "FAILED — §11.6 cost-sensitivity blocks"
```

The MED-slip framework outcome and the M1/M3 mechanism evidence stand as descriptive evidence, but the §11.6 hard gate makes the framework verdict FAILED.

---

## 10. Implementation-bug checks (hard checks per Phase 2v §3.2.3)

All hard implementation-bug checks pass on BOTH symbols:

1. **Zero TRAILING_BREACH / STAGNATION exits on R2+R3.** ✓ R3 exit machinery preserved verbatim under R2; no leakage. (Phase 2v §3.2.3 hard block 3.)
2. **Protective stop equals frozen `structural_stop_level`.** ✓ Every filled R2 trade's `initial_stop` (engine-side) equals its `structural_stop_level_at_registration` (frozen at registration). (Phase 2v §3.2.3 hard block 2 + Phase 2u §F invariant.)
3. **R2 lifecycle accounting identity holds.** ✓ `registered = no_pullback + bias_flip + opposite_signal + structural_invalidation + stop_distance_at_fill + filled` on both symbols. (Phase 2v §3.2.3 hard block 4 + Phase 2u §J.4 amendment.)
4. **`time_to_fill_bars` in valid range [0, 7].** ✓ All filled R2 trades fall within the 8-bar validity window (B+1 → B+8 maps to time_to_fill ∈ {0,...,7}). (Phase 2v §3.2.3 hard block 5.)
5. **Raw r_distance in [0.60, 1.80] for every filled R2 trade.** ✓ De-slipped r_distance within band on all 23 BTC + 19 ETH filled trades. The 2 BTC post-slip exceedances are slippage-induced on the recorded fill_price, not band-enforcement failures. (Phase 2v §3.2.3 hard block 6 + Phase 2u §E.3.)
6. **M3 mechanical R-distance reduction.** ✓ R2 mean stop-distance < R3 mean stop-distance on matched signals on both symbols. M3's mechanical guarantee held — no off-by-one or sign-flip in the pullback-retest geometry. (Phase 2v §5.2.3 + §5.4 hard block "M3 mechanical fail → stop as possible implementation bug".)

**No blockers; no engine bugs identified.** The analysis script's two pre-fix issues (Δ|maxDD| sign bug; P.14 post-slip vs raw band reference) were script-level interpretive bugs, not engine bugs; both fixed before final analysis.

---

## 11. Whether 2w-C comparison-report writing is safe to authorize

**Yes — 2w-C is safe to authorize**, with the explicit understanding that the comparison report will document a **framework-FAIL outcome** per the §11.6 cost-sensitivity gate, not a candidate-PROMOTE outcome.

### 11.1 What 2w-C will write

Per Phase 2v §1.5 / §4.15 / §5.3 / §6, the 2w-C comparison report must include 17 sections covering:

1. Plain-English summary (R2+R3 framework outcome).
2. Code surface and tests added (pulled from 2w-A + 2w-B checkpoint reports).
3. Quality-gate results.
4. H0/R3 control reproduction (unchanged from 2w-A; bit-for-bit).
5. R-window headline table (reproduced from §5.1 above).
6. **Official §10.3 verdict vs H0**, with §11.6 gate outcome explicitly applied:
   - MED-slip §10.3: PROMOTE (BTC §10.3.a + §10.3.c; ETH §10.3.c).
   - §11.6 HIGH-slip gate: FAILS.
   - Combined verdict: **FAILED — §11.6 cost-sensitivity blocks**.
7. Supplemental R3-anchor mechanism reading: BTC Δexp_R3 = −0.035 (R2 worse than R3 alone); ETH Δexp_R3 = −0.081 (R2 worse than R3 alone).
8. M1/M2/M3 classification: PARTIALLY SUPPORTED (M1 ✓, M2 ✗, M3 ✓).
9. P.1–P.14 diagnostics tables (reproduced from §8 above).
10. V-window table.
11. Slippage sensitivity table with §11.6 gate finding.
12. Stop-trigger sensitivity (bit-identical).
13. Fill-model sensitivity (BTC large divergence; ETH small).
14. PASS / FAIL / HOLD classification: **FAILED**.
15. What the verdict does NOT claim (mirroring Phase 2s §13).
16. Threshold preservation.
17. Safety posture.

### 11.2 What the framework verdict means strategically

Phase 2t §3.3 noted R2 was the only remaining structural axis with a concrete deferred candidate after R1a (setup-shape) and R1b-narrow (bias-shape) were tested and produced trade-count-reduction-driven framework PROMOTEs without absolute-edge gain on BTC. Phase 2t §11.3 GO recommendation acknowledged that R2 might also reproduce the R1b-narrow pattern.

The actual outcome is more nuanced:

- R2 **does** improve per-trade expectancy on BTC at MED slippage (M1 +0.12 R on intersection trades; +0.18 R headline vs H0). This is materially better than R1b-narrow's R3-anchor-neutral BTC pattern.
- R2 **does** produce smaller stop distances mechanically (M3 ✓).
- R2 **does not** reduce the stop-exit fraction (M2 ✗) — the smaller-stop / larger-size geometry is offset by stops being hit more often.
- R2 **does not** survive the §11.6 cost-sensitivity gate. At HIGH slippage (8 bps), the candidate's improvement evaporates: BTC Δexp at HIGH is −0.014 (worse than H0); ETH Δexp at HIGH is −0.230. R2's edge is **slippage-fragile**.

Phase 2t's recommendation explicitly considered the §11.6 risk in §10's failure-mode list (entry #2), noting that R2's smaller stop-distance interacts with slippage differently than market-fill geometry. Phase 2u §O falsifiable hypothesis explicitly required §11.6 clearance at HIGH. The §11.6 failure is therefore a documented and anticipated failure mode, not a surprise.

The comparison report should frame R2 as: **mechanism partially validated (M1 + M3 pass; M2 fails); MED-slip framework PROMOTE preserved as evidence; framework verdict FAILED via §11.6 cost-sensitivity gate; R2's edge is slippage-fragile and does not survive the cost-realism band Phase 2f §11.6 requires.**

### 11.3 Operator decision after 2w-C

The Phase 2t §11.6 fallback recommendation enumerated the operator paths. After the 2w-C report:

- **Option 1: Consolidate at R3.** R2's framework FAIL means R3 remains the baseline-of-record per Phase 2p. R2 is added to the retained-research evidence pile (alongside R1a and R1b-narrow); not a deployable variant.
- **Option 2: Family-shift planning.** Three structural-redesign candidates (R1a, R1b-narrow, R2) have been tested. None has produced an absolute-edge candidate that survives the framework gates. Phase 2p §F.4 family-abandonment pre-conditions become more relevant.
- **Option 3: Operator-policy review.** The operator may judge that the §11.6 HIGH-slip threshold is too conservative for live deployment given Binance's actual BTCUSDT futures slippage profile and propose a separate phase to revise §11.6 with evidence. This is operator-policy territory, not a framework-discipline shortcut, and is outside Phase 2w's scope.

These are operator decisions for after the 2w-C comparison report; 2w-B does not propose them.

### 11.4 What 2w-C must NOT do

- 2w-C must NOT change any R2 sub-parameter or any framework threshold.
- 2w-C must NOT re-classify the §11.6 gate outcome (the FAILED verdict is final under unchanged framework discipline).
- 2w-C must NOT shift baselines, delete evidence, or modify Phase 2u/2v/2w-A/2w-B artifacts.
- 2w-C must NOT propose paper/shadow / tiny-live / Phase 4 work.
- 2w-C must NOT merge the `phase-2w/r2-execution` branch to main.

---

## 12. Threshold preservation, wave/phase preservation, safety posture

**Threshold preservation.** Phase 2f §§ 10.3 / 10.4 / 11.3 / 11.4 / 11.6 thresholds applied unchanged. No post-hoc loosening per §11.3.5. Phase 2j §C.6 R1a sub-parameters preserved. Phase 2j §D.6 R3 sub-parameters preserved. Phase 2r §F R1b-narrow sub-parameter preserved. Phase 2u §F R2 sub-parameters preserved singularly (pullback level, confirmation rule, validity window, committed fill model). GAP-20260424-036 fold convention applied unchanged. GAP-20260424-031 / 032 / 033 carried forward unchanged. GAP-20260419-015 stop-distance reference-price convention applied unchanged. **No new GAP entries introduced in 2w-B.** Phase 2i §1.7.3 project-level locks preserved.

**Wave / phase preservation.** Phase 2g Wave-1 REJECT ALL preserved as historical evidence only. Phase 2l R3 PROMOTE preserved unchanged (R3 sub-parameters frozen; baseline-of-record per Phase 2p). Phase 2m R1a+R3 mixed-PROMOTE preserved unchanged (retained-for-future-hypothesis-planning per Phase 2p §D). Phase 2s R1b-narrow PROMOTE / PASS preserved unchanged. Phase 2t/2u/2v/2w-A artifacts preserved. **R2's MED-slip §10.3 PROMOTE evidence is preserved as descriptive research evidence even though the §11.6 gate failure produces a FAILED combined verdict** — the framework-discipline distinction between "MED-slip §10.3 outcome" and "combined verdict including §11.6" is the same evidence-preserving discipline applied throughout Phase 2. H0 anchor preserved as the sole §10.3 / §10.4 anchor.

**Safety posture.** Research-only. No live trading. No exchange-write paths. No production keys. No `.mcp.json`, no Graphify, no MCP server activation. No `.env` changes, no credentials, no Binance API calls (authenticated or public). No edits to `docs/12-roadmap/technical-debt-register.md`. No edits to the implementation-ambiguity log. No edits to `.claude/`. No `data/` commits (run artifacts under `data/derived/backtests/phase-2w-r2-*/` are git-ignored). No Phase 4 work. No paper/shadow planning. No live-readiness claim. R2's slippage-fragility under the §11.6 gate is documented evidence, NOT operationalized. No comparison report (deferred to 2w-C). No merge to main. Mark-price stop-trigger semantic preserved (MARK_PRICE default; TRADE_PRICE only as sensitivity diagnostic per run #9). R3 / R1a / R1b-narrow sub-parameters frozen. R2 sub-parameters frozen at Phase 2u §F values. The 8-bar setup window unchanged. The diagnostic-only limit-at-pullback intrabar fill model exists exclusively as the runner-script `--fill-model` flag (Phase 2v Gate 2 clarification); no `V1BreakoutConfig` field added. The §10.3 framework verdict is governed exclusively by run #3 (committed next-bar-open fill model); run #10 informs interpretation only.

---

**End of Phase 2w-B checkpoint report.** R2+R3 R-window MED-slip §10.3 PROMOTE preserved as descriptive evidence (BTC §10.3.a + §10.3.c; ETH §10.3.c); §11.6 cost-sensitivity gate FAILS at HIGH slippage on both symbols; combined framework verdict **FAILED — §11.6 cost-sensitivity blocks**. M1 mechanism (per-trade expectancy +0.12 R on BTC intersection) and M3 mechanism (R-distance reduction) PASS; M2 mechanism (stop-exit-fraction reduction) FAILS. All P.14 implementation-bug hard-block checks pass on both symbols. V-window evidence preserved (BTC R2 V degraded at n=5; ETH R2 V near-parity with R3 V). 6 R2 backtest runs executed; H0/R3 controls inherit from 2w-A bit-for-bit reproductions. Quality gates green throughout. **2w-C comparison-report writing is safe to authorize**, with the explicit framing that the report will document a §11.6-blocked FAILED framework verdict. **No code merge to main, no comparison report yet, no operator-policy proposals — all deferred per Phase 2w-B scope.** Stop after producing this report.
