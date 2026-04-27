# Phase 2r — R1b-narrow Spec Memo (Bias-Strength Redesign)

**Phase:** 2r — Docs-only Spec-Writing for R1b-narrow.
**Branch:** `phase-2r/gate-1-planning-memo` (continuation; spec memo on the same branch as the Gate 1 planning memo per operator authorization).
**Memo date:** 2026-04-27 UTC.
**Working directory:** `C:\Prometheus`.

**Authority:** Phase 2r Gate 1 planning memo (Path B selected: R1b-narrow); Phase 2j memo §C / §D (spec-style template); Phase 2p consolidation memo (R3 = baseline-of-record); Phase 2o asymmetry-review memo (§C.5 directional-bias interaction = best-supported asymmetry mechanism); Phase 2l comparison report (R3 PROMOTE locked); Phase 2i §1.7.3 project-level locks (H0 anchor; BTCUSDT primary); Phase 2f §§ 8–11 thresholds (preserved unchanged per §11.3.5); operator approval to proceed with R1b-narrow spec-writing.

**Status:** Spec memo only. **No code, no runs, no parameter tuning, no candidate-set widening, no Phase 4 / paper-shadow / live-readiness work.** The memo describes a future hypothesis precisely enough that, IF the operator later authorizes a Phase 2j-style execution phase, the implementation is unambiguous and the falsifiability is preserved. Phase 2r itself does **not** authorize execution.

---

## A. Objective / thesis

**R1b-narrow** is a single-axis structural redesign of H0's bias-validity predicate. The redesign replaces the existing **direction-sign** check on the 1h EMA(50) slope-3 measurement with a **magnitude** check using a single committed threshold S. All other H0 rules (setup, trigger, entry timing, stop construction, sizing) and the locked R3 exit machinery (`exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`) remain unchanged.

**Thesis.** Phase 2o §C.5 (the most-supported asymmetry explanation alongside §C.1) concluded that R1a's BTC/ETH outcome asymmetry under Phase 2m is most consistent with the breakout-on-bias entry rule interacting with a pre-existing directional-regime asymmetry. ETH was already direction-asymmetric under R3 alone (longs −0.934 / shorts +0.028); BTC was direction-symmetric (longs −0.252 / shorts −0.230). H0's bias rule classifies bars as LONG / SHORT / NEUTRAL using a *binary* slope direction-sign — it does not distinguish strong vs weak directional setups. R1b-narrow's hypothesis is that **filtering out weak-directional bars by requiring a slope-strength magnitude threshold** removes setups whose post-compression follow-through is unreliable. The expected effect is most pronounced on BTC where the bias regime is more directionally muted (more weak-bias setups that pass H0's binary check), and the ETH effect is expected to be modest (ETH's strong-directional regime should still produce strong-bias bars that pass the threshold).

R1b-narrow does not chase the R1a asymmetry mechanically (regime-conditional R1a-prime would do that, with high overfitting risk); it changes the bias-rule shape itself, which is one of the two mechanisms Phase 2o identified as the asymmetry source.

## B. Exact rule shape

At the close of every completed 1h bar the bias-validity predicate is re-evaluated. R1b-narrow modifies the slope-3 component only:

**H0 (current):**
```
LONG iff:
  EMA(50)[now] > EMA(200)[now]
  AND close[now] > EMA(50)[now]
  AND EMA(50)[now] > EMA(50)[now − 3]            # binary direction-sign check

SHORT iff:
  EMA(50)[now] < EMA(200)[now]
  AND close[now] < EMA(50)[now]
  AND EMA(50)[now] < EMA(50)[now − 3]            # binary direction-sign check

NEUTRAL otherwise
```

**R1b-narrow (proposed):**
```
slope_strength_3 = (EMA(50)[now] − EMA(50)[now − 3]) / EMA(50)[now]      # signed % change

LONG iff:
  EMA(50)[now] > EMA(200)[now]
  AND close[now] > EMA(50)[now]
  AND slope_strength_3 ≥ +S                       # magnitude check (NEW)

SHORT iff:
  EMA(50)[now] < EMA(200)[now]
  AND close[now] < EMA(50)[now]
  AND slope_strength_3 ≤ −S                       # magnitude check (NEW)

NEUTRAL otherwise
```

Where `S` is the committed slope-strength magnitude threshold (committed singularly in §F below). The redesign replaces the binary direction-sign comparison with a magnitude comparison anchored to a project-convention constant.

## C. Exact inputs used

- **1h completed klines.** Same window the existing bias rule consumes; no new dataset.
- **1h Wilder-style EMA(50) values.** Already computed by the strategy session (`_1h_ema_fast_latest` and `_1h_ema_fast_history`). No new indicator.
- **EMA(50) value at `now − 3` 1h bars.** Already retained in the existing `_1h_ema_fast_history` slope-lookback ring (`SLOPE_LOOKBACK + 1` capacity in `strategy.py`). No new state.

No new inputs. No new indicators. No 15m or mark-price or funding data introduced. No new state in `StrategySession`.

## D. Exact timeframes

- **Decision timeframe:** 15m (same as H0). Bias is consulted at every 15m signal evaluation.
- **Bias timeframe:** 1h (same as H0). EMA(50)/EMA(200) on completed 1h bars.
- **Slope window:** 3 completed 1h bars (same as H0; `SLOPE_LOOKBACK = 3` in `bias.py`).
- **Setup window:** 8 × 15m bars (unchanged; H0 default; not touched by R1b-narrow).

R1b-narrow does **not** change any timeframe, any window length, or any sampling cadence. Only the slope-comparison form changes (sign → magnitude).

## E. Exact bias-validity predicate (mathematical form)

Let `F_t` denote the 1h EMA(50) value computed at the close of bar `t`. At decision time at the close of bar `B` (the most recent completed 1h bar relative to the 15m signal evaluation), with 1h price close at `C_t`:

```
slope_strength_3(B) = (F_B − F_{B-3}) / F_B

L_ok(B) = [F_B > Slow_B] AND [C_B > F_B] AND [slope_strength_3(B) ≥ +S]
S_ok(B) = [F_B < Slow_B] AND [C_B < F_B] AND [slope_strength_3(B) ≤ −S]

bias(B) =
    LONG    if L_ok(B) AND not S_ok(B)
    SHORT   if S_ok(B) AND not L_ok(B)
    NEUTRAL otherwise
```

Where `Slow_B` is the 1h EMA(200) value at bar `B`.

**Boundary cases:**

- **Insufficient warmup.** If `len(completed_1h_bars) < EMA_SLOW + SLOPE_LOOKBACK` (= 200 + 3 = 203), bias is NEUTRAL. Same warmup as H0; not changed by R1b-narrow.
- **NaN handling.** If any of `F_B`, `Slow_B`, `F_{B-3}` is NaN (warmup not complete), bias is NEUTRAL. Same as H0.
- **`F_B = 0` (degenerate / negative-EMA edge case).** The division `slope_strength_3 = (F_B − F_{B-3}) / F_B` is undefined. Practically, `F_B > 0` is guaranteed once warmup is complete (EMA of strictly-positive prices is strictly positive). The implementation must reject as NEUTRAL if `F_B ≤ 0` for defense in depth (no real-data trigger expected).
- **Zero or near-zero slope.** A slope of exactly 0 satisfies neither `≥ +S` nor `≤ −S` for any positive S; bias is NEUTRAL. This is the desired behaviour — flat conditions produce no bias.
- **Boundary tie at S.** A slope of exactly `+S` satisfies `≥ +S` (LONG admitted); a slope of exactly `−S` satisfies `≤ −S` (SHORT admitted). Strict-inequality ties favoring admission rather than rejection match H0's convention (H0's `>` and `<` are also strict).

The predicate is deterministic at fixed inputs.

## F. Exact committed sub-parameter value

**S = 0.0020 (= 0.20%).**

That is: the slope-strength magnitude threshold `S` is committed at **0.20% relative change in the 1h EMA(50) over the 3-bar slope window**. Decimal form `0.0020`; percentage form `0.20%`.

**Non-fitting rationale.** S is anchored to the project's existing `ATR_REGIME_MIN` constant in `src/prometheus/strategy/v1_breakout/trigger.py`:

```python
ATR_REGIME_MIN = 0.0020  # 0.20%
ATR_REGIME_MAX = 0.0200  # 2.00%
```

`ATR_REGIME_MIN` is the project-convention minimum-allowed normalized 1h ATR (= `ATR(20)_1h / latest_1h_close`) below which the strategy's existing ATR-regime filter rejects entries (see Phase 2j memo §C.7 + `trigger._passes_atr_regime`). It represents "the minimum 1h volatility level the project considers viable for trading". The same numeric value (0.20%) is adopted for R1b-narrow's slope-strength threshold with the following interpretation:

> A 1h EMA(50) slope smaller than 0.20% over the 3-bar window represents a directional movement of the smoothed-price baseline of less than the project's minimum-allowed-volatility level. Below that level, the slope's direction-sign is dominated by noise rather than by a trend; H0's binary direction-sign check does not distinguish noise from trend in that range. R1b-narrow's threshold filters out those noise-dominated cases.

Three independent checks against fitting:

1. **The value is taken directly from an existing constant** committed before any R1b research. The value was not chosen by examining R1a's BTC degradation or ETH improvement.
2. **The value has not been tuned across alternatives.** No backtests have been run with S = 0.0010, S = 0.0030, or any other value. Phase 2r is docs-only; no parameter sweep is authorized.
3. **The value matches the project's existing magnitude convention for "minimum viable volatility"**, applied to a different but conceptually-related quantity (per-bar ATR regime → 3-bar EMA-slope magnitude). The conceptual-mismatch is acknowledged honestly: `ATR_REGIME_MIN` is per-bar ATR, while S is 3-bar slope; they share magnitude convention, not exact unit equivalence.

If a future execution phase produces evidence that S = 0.0020 is the wrong value, the response is **not** to retune within Phase 2r — it is to record the failure, consolidate, and either (a) abandon R1b-narrow with documented evidence, or (b) commission a separate operator-approved phase that proposes a new value with its own non-fitting rationale.

**S is committed singularly. No sweep. No tuning. No alternative values are permitted within R1b-narrow's spec.**

## G. Exact relationship to existing setup / trigger / entry / stop / R3-exit logic

R1b-narrow only changes the bias-validity predicate. Everything else is preserved:

- **Setup detection** (`detect_setup` in `setup.py` with H0 default range_width / drift two-clause predicate): **unchanged**. R1b-narrow does **not** combine with R1a's percentile predicate; the setup predicate stays at H0 default `RANGE_BASED`.
- **Trigger** (six-condition long/short trigger per `trigger.py`: close-broke-level, true-range vs ATR, close-location, ATR-regime, etc.): **unchanged**.
- **Entry timing** (market entry on next-bar open after breakout-bar close): **unchanged**.
- **Initial structural stop** (`compute_initial_stop` in `stop.py`): **unchanged**.
- **Stop-distance band** (0.60 ≤ d ≤ 1.80 × ATR(20)_15m per `passes_stop_distance_filter`): **unchanged**.
- **Sizing pipeline** (`sizing.compute_size` with risk_fraction=0.0025, risk_usage=0.90, max_leverage=2.0, notional_cap=100_000, taker=0.0005): **unchanged**.
- **R3 exit machinery** (`exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`; same-bar STOP > TAKE_PROFIT > TIME_STOP priority; protective stop never moved intra-trade): **unchanged**.
- **Re-entry lockout** (`StrategySession.can_re_enter` requires `setup_size` bars after exit): **unchanged**.
- **Phase 2i §1.7.3 project-level locks** (BTCUSDT primary, one-position max, 0.25% risk, 2× leverage, mark-price stops, v002 datasets): **unchanged**.

## H. What H0 rules are replaced

**Only the slope-3 direction-sign component of the bias-validity predicate.** Specifically:

- H0's `EMA(50)[now] > EMA(50)[now − 3]` (long-side rising-slope check) is replaced with `slope_strength_3 ≥ +S`.
- H0's `EMA(50)[now] < EMA(50)[now − 3]` (short-side falling-slope check) is replaced with `slope_strength_3 ≤ −S`.

The `EMA(50) > EMA(200)` and `close > EMA(50)` (and symmetric) components of H0's bias rule are **unchanged**.

## I. What H0 rules remain unchanged

- The EMA(50) > EMA(200) regime / position component of bias.
- The close > EMA(50) (and symmetric for SHORT) component of bias.
- The 3-bar slope-lookback window length (`SLOPE_LOOKBACK = 3`).
- The EMA(50)/EMA(200) period values (`EMA_FAST = 50`, `EMA_SLOW = 200`).
- The bias warmup floor (`EMA_SLOW + SLOPE_LOOKBACK = 203` bars).
- The 8-bar setup window (`SETUP_SIZE = 8`).
- The setup-validity predicate (range_width ≤ 1.75 × ATR(20)_15m AND |close[-1] − open[-8]| ≤ 0.35 × range_width per H0).
- The trigger six-condition cascade (with `BREAKOUT_BUFFER_ATR_MULT = 0.10`, `TRUE_RANGE_ATR_MULT = 1.0`, `CLOSE_LOCATION_RATIO = 0.75`, `ATR_REGIME_MIN = 0.0020`, `ATR_REGIME_MAX = 0.0200`).
- The entry-timing rule (next-bar open after breakout-bar close).
- The initial-stop formula and stop-distance band.
- The R3 exit machinery (R-target, time-stop, same-bar priority, no stop movement).
- The sizing pipeline.
- The Phase 2i §1.7.3 project-level locks.

## J. Implementation impact (descriptive only — Phase 2r writes no code)

A future operator-approved execution phase would extend the strategy package as follows. **Phase 2r does not write any of this code; it is described here only so the spec is complete.**

- **`V1BreakoutConfig`** would gain one new optional field: `bias_slope_strength_threshold: float = 0.0020`. Default `0.0020` matches the committed S. The field would be validated as `Field(ge=0.0, le=0.10)` (allowing any value in [0%, 10%] — the spec only commits a single value, but pydantic field constraints are conservative). When the new field equals **0.0**, the predicate degenerates to H0's binary direction-sign check (because `slope_strength_3 ≥ 0` is the strict-non-negative version of H0's `>`); a default-of-0.0 path could be the H0-bit-for-bit-preservation choice. **HOWEVER**, the *committed* R1b-narrow value is `0.0020`, not `0.0`. The choice between "default = 0.0 (bit-for-bit H0)" vs "default = 0.0020 (R1b-narrow)" is an implementation-spec decision: bit-for-bit H0 preservation is a strong invariant the project has held through Phase 2l + 2m, so the default should be **0.0** with R1b-narrow opting in via `bias_slope_strength_threshold=0.0020`.

  Caveat: because H0's predicate uses **strict** `>` while a `slope_strength_3 ≥ 0.0` reformulation uses non-strict `≥`, the boundary case where `slope_strength_3` is **exactly zero** (an EMA fixed point) would behave differently. The strict bit-for-bit H0 default may need a sentinel: e.g., the implementation dispatches to H0's binary `>` when `bias_slope_strength_threshold == 0.0`, and to the magnitude check otherwise. This sentinel-based dispatch mirrors the Phase 2l pattern (default `exit_kind=STAGED_TRAILING` preserves H0; explicit `exit_kind=FIXED_R_TIME_STOP` enables R3) and the Phase 2m pattern (default `setup_predicate_kind=RANGE_BASED` preserves H0; explicit `setup_predicate_kind=VOLATILITY_PERCENTILE` enables R1a).

- **`bias.py`** would add a sibling function `evaluate_1h_bias_with_slope_strength(completed_1h_bars, slope_strength_threshold)` that mirrors `evaluate_1h_bias` but performs the magnitude comparison. The original `evaluate_1h_bias` is preserved unchanged. The dispatch happens at `V1BreakoutStrategy.maybe_entry` (or in `StrategySession._update_1h_bias`) based on the config field.

- **`StrategySession._update_1h_bias`** would dispatch to either the H0 binary check or the R1b-narrow magnitude check based on `self.config.bias_slope_strength_threshold`. The dispatch is local to this method; the existing `_1h_ema_fast_history` ring already provides the necessary 3-bar lookback.

- **`run_signal_funnel`** in `diagnostics.py` would mirror the dispatch for funnel attribution. The existing `rejected_neutral_bias` bucket continues to absorb predicate failures; no new bucket needed (NEUTRAL bias outcomes are still counted in `bias_neutral_count` regardless of which predicate is active).

- **Tests** would prove (a) defaults preserve H0 bit-for-bit (sentinel-based dispatch with `bias_slope_strength_threshold == 0.0`), (b) at `bias_slope_strength_threshold = 0.0020` the predicate produces NEUTRAL bias for slopes in `(−0.0020, +0.0020)`, (c) boundary ties at exactly `±0.0020` admit the corresponding direction (favoring admission per H0 strict-inequality convention adapted to non-strict magnitude), (d) NaN warmup produces NEUTRAL, (e) the funnel `rejected_neutral_bias` and `bias_*_count` counters are correctly attributed.

This implementation surface is comparable in size to R1a's (Phase 2m commit 1: ~470 lines net source/tests). No new dependencies. No structural changes to the engine or backtest config beyond the new optional field.

## K. Expected mechanism of improvement (BTC focus)

The mechanism R1b-narrow tests is **bias-strength filtering** — specifically that some of H0's BTC LONG / SHORT entries fire on weak-directional bars where the EMA(50) slope direction is technically the right sign but the magnitude is small enough that follow-through is unreliable. R1b-narrow's threshold rejects those bars (NEUTRAL bias → no entry) and only admits bars where the directional gradient is at least 0.20% of EMA(50) over 3 bars.

The Phase 2o §C.5 evidence supporting this mechanism:

- **R3 alone BTC** (Phase 2l): direction-symmetric (longs −0.252 / shorts −0.230). Both directions admit comparable trade counts and produce comparable (negative) outcomes. This is consistent with H0's bias rule admitting many weak-bias BTC bars in both directions.

- **R3 alone ETH** (Phase 2l): direction-asymmetric (longs −0.934 / shorts +0.028). ETH's R-window regime had a sustained bearish bias that produced strong-magnitude SHORT-bias bars; H0's binary check admits both strong and weak SHORT bias bars on ETH but the sample is dominated by strong-bias periods.

- **R1a+R3 amplifies the asymmetry without creating it** (Phase 2m): R1a's compression filter further selects for "compression precedes breakout" bars within the bias-direction subset; the BTC bias bars R1a selects don't follow through (because they were weak-bias); the ETH bias bars R1a selects often do follow through (because ETH's strong-bias regime produced compression-then-expansion patterns). R1a is a *subset filter*; the bias rule determines the *parent set*. If the parent set includes too many weak-bias bars on BTC, the subset inherits that weakness.

R1b-narrow's expected effect on BTC: trade-count reduction concentrated in the weak-bias subset; remaining trades have stronger directional context; expR should improve, especially on BTC. The improvement should be most visible in the regime decomposition: H0 BTC high_vol expR was −0.688 (under R3 alone BTC high_vol −0.472); high-vol regimes likely contain more strong-bias bars (because volatility correlates with directional moves), so R1b-narrow's filter should preferentially cut weak-bias trades from low_vol and med_vol regimes while leaving high_vol approximately intact.

R1b-narrow's expected effect on ETH: smaller magnitude; ETH's strong-bias regime should largely pass the threshold. Trade-count reduction should be smaller than BTC (ETH bias bars are mostly strong-bias by virtue of the underlying regime). expR should improve modestly or stay roughly equal.

The **falsifiable prediction** is therefore: BTC Δexp ≥ +0.10 R AND ΔPF ≥ +0.05 (the §10.3.a magnitude path), or some combination of strict-dominance gains across §10.3.c that clears the framework. ETH should not degrade on either dimension and should likely improve modestly.

## L. Expected main failure mode

The most-likely failure mode: **the threshold S = 0.20% is too small to filter meaningfully on BTC**.

If H0's BTC weak-bias bars predominantly have slope_strength in the [+0.0%, +0.20%] band, R1b-narrow's threshold will exclude only a small fraction of them; the BTC trade-count reduction would be modest, and the BTC expR improvement would be smaller than §10.3.a's +0.10 R magnitude threshold. The framework would issue a §10.3.c-only PROMOTE (similar to R1a+R3's BTC clearance) or a HOLD verdict.

**Why this can't be addressed by tuning S in Phase 2r.** The non-fitting rationale (§F) anchors S to a specific project-convention constant. If S = 0.20% is too small, the disciplined response is **not** to retune within R1b-narrow — it is to record the failure and either (a) abandon R1b-narrow with documented evidence ("a slope-strength threshold at the project's minimum-volatility convention is insufficient to filter weak-bias setups; the bias-strength mechanism does not address the asymmetry at this magnitude"), or (b) commission a separate operator-approved phase proposing a different threshold with a different non-fitting rationale.

**Less likely failure modes:**

- **The threshold is too large.** S = 0.20% might exclude many bars that H0 would admit, dropping trade count below GAP-036 fold-consistency thresholds (~10–15 trades per fold becomes fragile). Symptoms: trade count drops by > 50%; per-fold expR distributions become noisy.
- **The bias-strength mechanism is not the actual asymmetry source.** Phase 2o §C.5 was the most-supported explanation but not the only one; if the asymmetry is dominantly §C.1 (symbol-specific market behaviour independent of bias rule), R1b-narrow has no leverage on it. Symptoms: trade-count reduction without expR improvement on either symbol.
- **R1b-narrow disproportionately rejects ETH-shorts.** ETH's bias regime might have many strong-magnitude SHORT-bias bars but also some moderate-magnitude SHORT-bias bars in the compression filter's sweet spot; if R1b-narrow rejects the latter, ETH-shorts edge could erode. Symptoms: ETH expR worsens; ETH-shorts cell loses its first-positive-PF status.
- **Implementation-bug check fails.** If the magnitude check is implemented incorrectly (e.g., wrong sign convention; off-by-one in slope window; NaN handling regression), the test suite catches the bug and the spec phase fails before any execution.

## M. Why R1b-narrow is structural and not parametric

Per Phase 2i §1.7.1 binding test (paraphrased: parametric = "changing a numeric threshold while keeping the same rule shape"; structural = changing the rule shape itself):

- **Rule shape changes from "binary direction-sign" to "magnitude comparison".** H0's predicate evaluates `EMA(50)[now] > EMA(50)[now − 3]` (a comparison operator that returns Boolean from sign of difference). R1b-narrow evaluates `(EMA(50)[now] − EMA(50)[now − 3]) / EMA(50)[now] ≥ S` (a comparison operator that returns Boolean from a magnitude relative to a threshold). These are different functional forms of a comparison: one is sign-only (a step function at zero), one is magnitude (a threshold function at S). Different predicate shape.
- **Rule input domain changes.** H0's slope-3 component consumes only the *sign* of the EMA(50)[now] − EMA(50)[now − 3] difference. R1b-narrow consumes the **magnitude relative to EMA(50)[now]** as a percentage. The functional input is different.
- **The threshold S is not a "tweak" of an existing threshold.** H0 has no slope-strength threshold to tweak — its slope-3 check is binary direction-sign. The introduction of S is the introduction of a new functional form, not a parameter change on an existing one.

The contrast to a parametric R1b would be: changing `EMA_FAST` from 50 to 30 while keeping the binary direction-sign rule. That would be parametric (same rule shape, different value). R1b-narrow is structural — same EMA periods, same window length, same warmup; **different predicate form**.

Per Phase 2i §1.7.2 secondary check ("changing a numeric threshold while keeping the same rule shape" is parametric), the introduction of a *new* threshold (S) along with a *new functional form* (magnitude comparison) is not parametric; the value S is the parameter of the new form, not a tweak of an existing parameter.

R1b-narrow passes the Phase 2i §1.7 binding test.

## N. GAP dispositions

R1b-narrow does not touch any existing GAP disposition. Carry-forward unchanged:

| GAP                  | Topic                                                                                          | R1b-narrow disposition |
|----------------------|------------------------------------------------------------------------------------------------|------------------------|
| GAP-20260424-030     | Break-even +1.5R vs +2.0R rule-text conflict                                                    | **CARRIED** — R1b-narrow keeps R3 exit logic, which has no break-even; the conflict stays open. Phase 2l / 2m / 2n / 2o / 2p / 2q dispositions unchanged. |
| GAP-20260424-031     | EMA slope wording (discrete vs. fitted)                                                          | **CARRIED-AND-MORE-RELEVANT** — R1b-narrow keeps the same discrete-comparison EMA[now] vs EMA[now − 3] convention from Phase 2g, but **adds magnitude semantics**. The GAP's underlying ambiguity (whether the spec means a discrete-comparison or a fitted-slope) is partially clarified by R1b-narrow's explicit discrete-comparison-with-magnitude form. The GAP entry stays open; R1b-narrow's spec memo is one more piece of evidence that the discrete-comparison interpretation is the project's working convention. |
| GAP-20260424-032     | Mark-price stop-trigger sensitivity                                                              | **CARRIED — required report cut for any future R1b-narrow execution wave** per Phase 2i §2.5.5. The execution phase, if and when authorized, must run R1b-narrow with `stop_trigger_source=TRADE_PRICE` and report comparison vs. MARK_PRICE. |
| GAP-20260424-033     | Stagnation window classification                                                                 | **CARRIED** — R1b-narrow keeps R3 exit logic; the GAP-033 disposition is unchanged from Phase 2l (R3 unconditional time-stop). |

No new GAP entries are proposed in Phase 2r.

## O. Candidate-specific falsifiable hypothesis

> **R1b-narrow hypothesis (pre-committed):** On R = 2022-01-01 → 2025-01-01 with v002 datasets, an R1b-narrow variant — H0 setup + H0 trigger + bias-validity predicate per §B with `S = 0.0020` (committed singularly per §F) + R3 exit logic locked + all other rules at H0 defaults — produces a §10.3-passing result vs H0 baseline. The acceptable §10.3 paths are:
>
> - **§10.3.a** (Δexp ≥ +0.10 R AND ΔPF ≥ +0.05) — the magnitude path.
> - **§10.3.b** (Δexp ≥ 0 AND trades + ≥ 50% AND |maxDD| not worse by > 1.0 pp) — note: §10.3.b requires *rising* trade count, which is unlikely under R1b-narrow (the threshold filter is expected to *reduce* trade count); §10.3.b is therefore not the expected path.
> - **§10.3.c** (strict dominance: Δexp > 0 AND ΔPF > 0 AND Δ|maxDD| ≤ 0) — the dominance path; would fire if R1b-narrow improves all three dimensions but Δexp falls short of §10.3.a's +0.10 R.
>
> No §10.3 disqualification floor may be triggered (no worse expR, no worse PF, |maxDD| ≤ 1.5× baseline).
>
> **The hypothesis is FALSIFIED if** R1b-narrow fails §10.3 on BTC OR triggers §10.3 disqualification on BTC, OR triggers §10.3 disqualification on ETH per §11.4 ETH-as-comparison rule.
>
> **The hypothesis is INDETERMINATE if** R1b-narrow clears §10.3 on R but fails on V (per §11.3 no-peeking discipline; failure on V does not retroactively change R-window classification but does end the candidate's wave).

The hypothesis is most-likely-true if the post-compression follow-through asymmetry Phase 2o diagnosed is dominantly driven by H0's binary bias rule admitting too many weak-directional setups. It is most-likely-false if the asymmetry is dominantly driven by §C.1 symbol-specific market behaviour independent of bias-rule shape (in which case the bias-strength threshold would not be the leverage point).

## P. Candidate-specific mandatory diagnostics

In addition to the common framework's per-regime expR / MFE distribution / long-short asymmetry / mark-price sensitivity (per Phase 2i §2.5.5, restated in any execution phase), R1b-narrow's execution phase must record:

### P.1 Slope-strength distribution at filled R1b-narrow entries

For each filled R1b-narrow entry, record `slope_strength_3` at the bias-evaluation time. The distribution should:

- Have minimum absolute value `≥ 0.0020` (= S; mechanically guaranteed if implementation is correct; first-line bug check).
- Have mean / median / quartiles materially **above** the H0-side average for filtered-out bars (whose mean would by definition be `< 0.0020` in absolute value; this comparison requires recording bias evaluations at all decision bars, not just filled-entry bars — see §P.2).

If filled-entry slope-strength distribution shows entries near `±0.0020` boundary heavily clustered (i.e., R1b-narrow is admitting marginal cases), this is a sign that the threshold S is at the right magnitude (catching the marginal noise-vs-trend boundary). If the distribution is concentrated at high magnitudes (`> 0.005`), this suggests the threshold is functionally inactive (most filled entries would have passed even a much higher threshold) and R1b-narrow is producing minimal change vs H0.

### P.2 Funnel attribution: NEUTRAL-bias rejection comparison vs H0

The diagnostic funnel (`run_signal_funnel`) must record `rejected_neutral_bias` count for both predicates:

- **H0 (control):** baseline H0 funnel rejected-bias count at the same v002 datasets.
- **R1b-narrow (candidate):** rejected-bias count under R1b-narrow's predicate.

The expected pattern: R1b-narrow's rejected-bias count > H0's, with the increase concentrated in bars whose `slope_strength_3` is in the `(−0.0020, +0.0020)` band (i.e., bars that would have passed H0's binary direction-sign check but are below R1b-narrow's magnitude threshold).

Per-symbol decomposition required:
- Total bars in `(−0.0020, +0.0020)` band by symbol (a measure of how much filtering happens).
- Count of those bars that would have produced a downstream entry under H0 (i.e., would have passed the trigger and stop-distance filter) — this measures the **reduction in candidate pool**.

If R1b-narrow's filtering does not reduce candidate pool meaningfully (i.e., very few bars fall in the band, or the bars that do fall in the band were already rejected downstream by trigger / ATR-regime / stop-distance filters), R1b-narrow has no leverage on the asymmetry. This is the §L "S is too small" failure mode confirmation.

### P.3 Per-direction expR by slope-strength bucket

Decompose filled R1b-narrow entries by bucket of `|slope_strength_3|`:
- Bucket 1: `[+0.0020, +0.0050)` — marginal-strength
- Bucket 2: `[+0.0050, +0.0100)` — moderate-strength
- Bucket 3: `[+0.0100, +∞)` — strong-strength

Report per-bucket expR / PF / WR for each symbol and each direction. If R1b-narrow's signal is dominantly from strong-bias bars, Bucket 3 should outperform Bucket 1 — confirming the bias-strength mechanism. If all three buckets perform similarly, the magnitude doesn't matter and R1b-narrow's improvement (if any) is from a different mechanism.

This is the **strongest mechanistic-validation diagnostic** for the R1b-narrow thesis. If marginal-strength bars (Bucket 1) outperform strong-strength bars (Bucket 3), the bias-strength thesis is contradicted.

### P.4 R1b-narrow vs R3-only direction-asymmetry check

Phase 2m showed R1a+R3 ETH is direction-asymmetric (shorts +0.387 / longs −1.259) while BTC is direction-symmetric. R3-only (Phase 2l) had ETH shorts +0.028 (already positive); BTC roughly symmetric.

Under R1b-narrow's hypothesis, the direction-asymmetry on ETH should be largely preserved (ETH's strong-bias regime passes the threshold; ETH-shorts retain their PF > 1 character). On BTC, R1b-narrow's filtering should *not* introduce direction-asymmetry — the remaining post-filter BTC trades should still be roughly direction-symmetric, just with better expR on both sides (because both directions had their weak-bias subset filtered).

Diagnostic: report long/short trade counts, expR, PF for R1b-narrow vs R3 (and vs H0). Compare:
- ETH shorts under R1b-narrow vs R1a+R3 (R1a+R3 was the strongest cell): should be similar magnitude if bias-strength is the asymmetry source; should be weaker if R1a's compression filter was the necessary lift.
- BTC longs/shorts under R1b-narrow: should both improve modestly; should remain roughly symmetric.

If R1b-narrow ETH-shorts cell is markedly weaker than R1a+R3 ETH-shorts, this argues the compression filter (not just bias strength) was the key lift on ETH — and R1b-narrow alone is not the right path forward.

### P.5 Common framework diagnostics

Standard Phase 2i §2.5.5 diagnostics (also required for H0 + R3 control re-runs alongside R1b-narrow):

- Realized 1h volatility regime expR (trailing 1000 1h-bar window of Wilder ATR(20), terciles 33/67) — same convention as Phase 2l / 2m corrected diagnostic.
- MFE distribution.
- Long/short asymmetry (covered in §P.4 above).
- Per-fold (5 rolling, GAP-036) consistency comparison vs both H0 and R3.
- Trade-frequency sanity-check.
- Implementation-bug check (zero TRAILING_BREACH / STAGNATION exits in any R3-or-R1b-narrow trade log; H0 must reproduce its locked baseline bit-for-bit).
- Slippage sensitivity (LOW / MED / HIGH) — only if the candidate PROMOTES on R-window MED.
- Stop-trigger source sensitivity (MARK_PRICE vs TRADE_PRICE per GAP-20260424-032) — only if PROMOTES.
- V-window confirmation — only if PROMOTES.

---

**End of Phase 2r R1b-narrow spec memo.** Sections A–P complete. Single-axis structural redesign of H0's bias-validity predicate; one new committed sub-parameter (S = 0.0020) with project-convention non-fitting rationale; R3 exit machinery preserved; H0 setup and trigger preserved; Phase 2i §1.7.3 project-level locks preserved; Phase 2f §§ 8–11 thresholds preserved unchanged; falsifiable hypothesis recorded; mandatory R1b-narrow-specific diagnostics enumerated. **No code, no runs, no parameter tuning, no candidate-set widening, no Phase 4 / paper-shadow / live-readiness work.** Phase 2r itself does **not** authorize execution; a separate operator-approved phase (Phase 2s or later) is required to run R1b-narrow. Stop after producing this memo.
