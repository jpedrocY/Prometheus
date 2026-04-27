# Phase 2u — R2 (Pullback-Retest Entry) Spec Memo

**Phase:** 2u — Docs-only spec-writing for R2 (pullback-retest entry).
**Branch:** to be created by operator (recommended: `phase-2u/r2-spec-memo`).
**Memo date:** 2026-04-27 UTC.
**Working directory:** `C:\Prometheus`.

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; no post-hoc loosening per §11.3.5); Phase 2g comparison report (REJECT ALL preserved as historical evidence only); Phase 2h decision memo; Phase 2i §1.7 binding test for structural-vs-parametric and §1.7.3 project-level locks; Phase 2i §3.2 entry-redesign survey (R2 originally enumerated and deferred); Phase 2j memo §C / §D (spec-style template); Phase 2k Gate 1 plan; Phase 2l comparison report (R3 PROMOTE locked); Phase 2m comparison report (R1a+R3 mixed-PROMOTE preserved as research evidence); Phase 2n strategy-review memo; Phase 2o asymmetry-review memo; Phase 2p consolidation memo (R3 = baseline-of-record; R1a = retained-for-future-hypothesis-planning); Phase 2r R1b-narrow spec memo; Phase 2s R1b-narrow execution comparison report (PROMOTE on R; PASS classification with sample-size and R3-anchor-neutrality caveats); Phase 2t R2 Gate 1 planning memo (GO recommendation conditional on §11.3 discipline locks); operator approval to proceed with R2 spec-writing.

**Status:** Spec memo only. **No code, no runs, no parameter tuning, no candidate-set widening, no Phase 4 / paper-shadow / live-readiness work, no MCP / Graphify / `.mcp.json`, no credentials.** This memo describes a future hypothesis precisely enough that, IF the operator later authorizes a Phase 2j-style execution phase, the implementation is unambiguous and the falsifiability is preserved. Phase 2u itself does **not** authorize execution; a separate operator-approved Gate 1 plan is required.

> **Gate 2 amendment (2026-04-27).** Per the Phase 2v Gate 2 review (`2026-04-27_phase-2v_gate-2-review.md`), this spec is amended in-place to (1) add a STRUCTURAL_INVALIDATION cancellation reason at precedence position 3 in the R2 candidate-lifecycle, completing the pending-state machine for the close-violates-stop-on-non-touch-bar case; (2) clarify that the §P.6 / Phase 2v run #10 limit-at-pullback intrabar fill model is diagnostic-only and never a production / default config path. **No committed sub-parameter values change** — pullback level (`setup_high` / `setup_low`), confirmation rule (close not violating structural stop), validity window (8 bars), and committed fill model (next-bar-open after confirmation) remain as committed in §F. Affected sections: §B, §E.2, §E.6, §F.4, §J.4, §J.5, §L.2, §P.1. See the Gate 2 review for the full finding rationale, verification, and approval recommendation.

This memo follows the Phase 2r §A–§P structure adapted for R2's four-axis topology change.

---

## A. Objective / thesis

**R2 (pullback-retest entry)** is a single-axis structural redesign of H0's entry-lifecycle topology. The redesign replaces the existing **immediate market-on-next-bar-open** entry mechanism with a **conditional-pending pullback-retest** entry mechanism. All other H0 rules (setup, trigger, bias, stop construction, sizing) and the locked R3 exit machinery (`exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`) remain unchanged.

**Thesis.** Phase 2t §3.1 collected the empirical evidence: H0 wave-1 BTC stops out 22 of 41 trades (54%, per Phase 2i §3.2); R3 alone improves the exit-side decomposition but does not change the *initial* entry price or the structural stop level; two filter-axis redesigns (R1a setup-shape, R1b-narrow bias-shape) have been tested and produce trade-count-reduction-driven framework PROMOTEs without per-trade-expectancy improvement on BTC under R3-anchor (Δexp_R3 = −0.180 for R1a+R3; −0.023 for R1b-narrow+R3). The remaining structural axis with a concrete deferred candidate is entry-mechanic topology.

R2's hypothesis is that a non-trivial fraction of H0's BTC stop-outs reflect entering at the breakout-bar's far side from the structural-invalidation reference — that is, at the worst short-term price. Pullback-retest entry attempts to enter closer to the structural-invalidation reference (the setup boundary), reducing stop distance, increasing position size at fixed 0.25% equity risk, and tightening R3's +2 R take-profit to a smaller absolute price distance. Breakouts that never retest expire unfilled (no loss); breakouts that retest and are confirmed by a close that has not violated the structural stop become trades at a better price.

R2 does not chase a directional or regime-conditional asymmetry (those would have high overfitting risk per Phase 2t §9.2); it changes the entry-lifecycle topology itself, which is one of the explicit Phase 2i §1.7.1 verbatim examples of structural redesign.

---

## B. Exact rule shape

The R2 redesign converts H0's single-event entry (signal → market fill at next-bar open) into a two-event entry (signal → register pending candidate → wait for pullback-retest within validity window → confirm and fill, or expire).

**H0 (current, conceptually):**

```
At close of breakout-bar B:
  if all six trigger conditions pass
     AND 1h bias agrees with direction
     AND stop-distance(close_B, structural_stop_level_B, ATR_at_B) ∈ [0.60, 1.80] × ATR_at_B:
       enter MARKET at bar B+1 open
       place protective STOP_MARKET at structural_stop_level_B
       trade enters R3 exit machinery starting at bar B+1
```

**R2 (proposed):**

```
At close of breakout-bar B:
  if all six trigger conditions pass
     AND 1h bias agrees with direction
     AND stop-distance(close_B, structural_stop_level_B, ATR_at_B) ∈ [0.60, 1.80] × ATR_at_B:
       REGISTER PendingCandidate{
         direction:               LONG | SHORT,
         registration_bar_index:  B,
         pullback_level:          setup.setup_high if LONG else setup.setup_low,
         structural_stop_level:   compute_initial_stop(direction, setup, breakout_bar_B, ATR_at_B),
         atr_at_signal:           ATR(20)_15m at close of B,
         validity_expires_at:     B + 8,
       }

For each subsequent completed 15m bar t in (B, B + 8]:
  # Cancellation checks (in order; first-match wins):
  # Precedence: 1. BIAS_FLIP > 2. OPPOSITE_SIGNAL > 3. STRUCTURAL_INVALIDATION > 4. TOUCH+CONFIRMATION > 5. CONTINUE
  bias_at_t = evaluate 1h bias at close of bar t (H0 binary slope rule)
  if bias_at_t != candidate.direction:
      CANCEL with reason BIAS_FLIP

  if at close of bar t a NEW opposite-direction breakout signal would fire
     (independent six-condition trigger evaluation):
      CANCEL with reason OPPOSITE_SIGNAL

  # Structural-invalidation check (NEW per Phase 2v Gate 2 amendment):
  # Fires whenever the close has breached the structural-stop reference,
  # regardless of whether the touch occurred. This closes the pre-amendment
  # gap where a non-touch bar with close-violating-stop continued pending.
  if candidate.direction == LONG and close_t <= candidate.structural_stop_level:
      CANCEL with reason STRUCTURAL_INVALIDATION
  elif candidate.direction == SHORT and close_t >= candidate.structural_stop_level:
      CANCEL with reason STRUCTURAL_INVALIDATION

  # Touch + confirmation check (single bar; same-bar resolution):
  # Note: the "confirmed" predicate at this step is mechanically redundant
  # given that STRUCTURAL_INVALIDATION at step 3 has already verified
  # close not violating stop. Retained for symmetry / readability.
  if candidate.direction == LONG:
      touched     = (low_t  <= candidate.pullback_level)
      confirmed   = (close_t >  candidate.structural_stop_level)
  else:  # SHORT
      touched     = (high_t >= candidate.pullback_level)
      confirmed   = (close_t <  candidate.structural_stop_level)

  if touched AND confirmed:
      # Pending fill at next bar open:
      fill_price = open at bar (t + 1)
      fill_stop_distance = abs(fill_price - candidate.structural_stop_level)

      # Fill-time stop-distance re-check (same band as H0):
      if fill_stop_distance NOT in [0.60, 1.80] × candidate.atr_at_signal:
          CANCEL with reason STOP_DISTANCE_AT_FILL

      # FILL:
      enter at fill_price at bar (t + 1) open
      place protective STOP_MARKET at candidate.structural_stop_level
      trade enters R3 exit machinery starting at bar (t + 1)
      break  # candidate consumed

If no fill or cancel by close of bar (B + 8):
  EXPIRE with reason VALIDITY_WINDOW_ELAPSED
```

The single axis of structural change is the **insertion of a PendingCandidate state** between trigger evaluation and fill. Every other rule (trigger, bias, structural-stop formula, stop-distance band, R3 exit machinery, sizing) is reused verbatim.

---

## C. Exact inputs used

R2 introduces no new datasets, no new indicators, no new state in `StrategySession` beyond the PendingCandidate record. All inputs are already produced by H0:

- **15m completed klines.** Used at registration (breakout-bar B's close, low, high, open) and at every subsequent bar t ∈ (B, B + 8] for touch detection (low_t for LONG, high_t for SHORT) and confirmation (close_t).
- **1h completed klines.** Used by the existing 1h bias evaluation at every bar t ∈ (B, B + 8] for the BIAS_FLIP cancellation check. Same 1h source `evaluate_1h_bias()` H0 already uses.
- **15m Wilder ATR(20).** Computed at close of bar B−1 (same as H0). Frozen at registration as `candidate.atr_at_signal`. **Re-used at fill time without recomputation** to preserve H0's GAP-20260419-015 convention.
- **Setup window (`setup.setup_high`, `setup.setup_low`).** Computed at bar B per H0's existing `detect_setup()` over the prior 8 completed 15m bars. Frozen at registration as `candidate.pullback_level`.
- **Structural-stop level.** Computed at bar B per H0's `compute_initial_stop()` (`min(setup.setup_low, breakout_bar.low) − 0.10 × ATR(20)_15m` for LONG; symmetric for SHORT). Frozen at registration as `candidate.structural_stop_level`.

No mark-price inputs. No funding inputs. No leverage-bracket inputs beyond what H0 sizing already consumes at fill time.

---

## D. Exact timeframes

- **Decision timeframe:** 15m (same as H0). All R2 candidate-state transitions (touch, confirmation, cancellation) are evaluated at completed 15m bar closes.
- **Bias timeframe:** 1h (same as H0). The BIAS_FLIP cancellation check consults `evaluate_1h_bias()` at the most recent completed 1h bar relative to the 15m candidate-evaluation bar.
- **Validity window unit:** 15m completed bars. The window measures elapsed completed 15m bars *strictly after* the registration bar B.
- **Setup window:** 8 × 15m bars (unchanged from H0; used at registration only).

R2 does **not** introduce any new timeframe, sampling cadence, or window length beyond what H0 already maintains.

---

## E. Exact predicate (mathematical form)

Let:
- `B` = the completed 15m breakout-bar at which the trigger evaluation fires.
- `setup_high(B)`, `setup_low(B)` = setup-window high / low computed over the 8 completed 15m bars strictly preceding B.
- `breakout_bar_B` = the completed 15m kline at index B.
- `atr_15m(B)` = Wilder ATR(20) computed at close of B−1 (H0 convention).
- `Stop_long(B) = min(setup_low(B), breakout_bar_B.low) − 0.10 × atr_15m(B)`.
- `Stop_short(B) = max(setup_high(B), breakout_bar_B.high) + 0.10 × atr_15m(B)`.
- `Bias_t` = 1h bias evaluated at the most recent completed 1h bar ≤ close-time of 15m bar t (per H0's `evaluate_1h_bias()`).
- `OppSignal_t` = TRUE iff the six-condition trigger fires for the opposite direction at close of bar t.

### E.1 Registration predicate (LONG; SHORT symmetric)

At close of bar B:

```
R2_register_long(B) :=
    H0_trigger_pass_long(B)
    AND Bias_B == LONG
    AND |close_B − Stop_long(B)| ∈ [0.60, 1.80] × atr_15m(B)
```

If `R2_register_long(B)` is true, register PendingCandidate with `pullback_level = setup_high(B)`, `structural_stop_level = Stop_long(B)`, `atr_at_signal = atr_15m(B)`, `validity_expires_at = B + 8`.

### E.2 Per-bar evaluation predicate (LONG)

For each `t ∈ (B, B + 8]`:

```
Cancel_bias_t        := (Bias_t != LONG)
Cancel_opposite_t    := OppSignal_t (with direction = SHORT)
Cancel_structural_t  := (close_t <= candidate.structural_stop_level)     # NEW (Phase 2v Gate 2 amendment)
Touched_t            := (low_t <= candidate.pullback_level)
Confirmed_t          := (close_t > candidate.structural_stop_level)      # mechanically redundant given step 3 precedence; retained for symmetry
```

Order of evaluation at bar t close (first-match wins):

1. If `Cancel_bias_t` → CANCEL(BIAS_FLIP); stop iterating.
2. Else if `Cancel_opposite_t` → CANCEL(OPPOSITE_SIGNAL); stop iterating.
3. Else if `Cancel_structural_t` → CANCEL(STRUCTURAL_INVALIDATION); stop iterating.    **(NEW)**
4. Else if `Touched_t AND Confirmed_t` → mark candidate as `READY_TO_FILL_AT_T_PLUS_1`; stop iterating.
5. Else continue.

**Precedence rationale (Phase 2v Gate 2 amendment).** The new step 3 STRUCTURAL_INVALIDATION cancellation closes the pre-amendment gap where a bar with `low_t > candidate.pullback_level` (no touch) AND `close_t ≤ candidate.structural_stop_level` (close has breached the structural-stop reference) erroneously continued pending. Under the amended precedence, any bar where the close has crossed the structural-stop reference cancels the candidate, regardless of whether the touch occurred. The `Confirmed_t` predicate at step 4 is mechanically redundant given that step 3 has already enforced `close_t > structural_stop_level` for any bar that reaches step 4; the predicate is retained at step 4 for symmetry with the rule's defining shape ("touch + close-not-violating-stop"). The implementation may keep both checks at step 4 or short-circuit on the precedence guarantee — the committed semantics is identical either way.

For SHORT direction, the predicates are mirrored:

```
Cancel_structural_t  := (close_t >= candidate.structural_stop_level)
Touched_t            := (high_t >= candidate.pullback_level)
Confirmed_t          := (close_t < candidate.structural_stop_level)
```

Same 5-step precedence applies (BIAS_FLIP → OPPOSITE_SIGNAL → STRUCTURAL_INVALIDATION → TOUCH+CONFIRMATION → CONTINUE).

### E.3 Fill predicate (LONG)

At close of bar t where the candidate became `READY_TO_FILL_AT_T_PLUS_1`, deferred to open of bar (t + 1):

```
fill_price                   := open_(t+1)
fill_stop_distance           := |fill_price − candidate.structural_stop_level|

R2_fill_passes_filter        := fill_stop_distance ∈ [0.60, 1.80] × candidate.atr_at_signal
```

If `R2_fill_passes_filter` is true → FILL at `fill_price` at bar (t + 1) open; place protective STOP_MARKET at `candidate.structural_stop_level`; trade enters R3 exit machinery counted from bar (t + 1).

If `R2_fill_passes_filter` is false → CANCEL(STOP_DISTANCE_AT_FILL); no trade.

### E.4 Expiry predicate

If by close of bar `B + 8` no FILL or CANCEL has occurred → EXPIRE(VALIDITY_WINDOW_ELAPSED).

### E.5 Pending uniqueness

While a PendingCandidate is active for a given symbol:
- A new R2_register_long(B') = true for B' ∈ (B, B + 8] with the candidate already pending in direction LONG: **drop new signal silently**. First-registered candidate wins.
- A new R2_register_short(B') = true while a LONG candidate is pending: triggers the OPPOSITE_SIGNAL cancellation of the LONG candidate at bar B' close; then the SHORT registration is evaluated at the same bar's close.
- After CANCEL, EXPIRE, or FILL, the candidate slot is free; the next eligible registration may proceed.

This rule preserves the existing v1 "one-position max, one-symbol-only" invariant: at most one PendingCandidate per direction, and only one trade open at a time downstream.

### E.6 Boundary cases

- **NaN / warmup.** If at bar B `atr_15m(B)` is NaN (warmup not complete) or `Bias_B` is NEUTRAL (warmup or rule-output not LONG/SHORT), `R2_register_*` returns false. No candidate registered. Same warmup discipline as H0.
- **`atr_15m(B) ≤ 0`.** The H0 stop-distance filter and the H0 stop-formula already reject this case. R2 inherits the rejection.
- **Same-bar same-direction re-trigger inside a pending window.** Dropped per §E.5.
- **Same-bar touch + close-violates-stop (LONG: `low_t ≤ pullback_level AND close_t ≤ structural_stop_level`)** *(amended; previously "touch-without-confirmation" continue-pending case)*. Under the Phase 2v Gate 2 amended precedence, step 3 STRUCTURAL_INVALIDATION fires before step 4 TOUCH+CONFIRMATION can be reached. The candidate is CANCELled with reason STRUCTURAL_INVALIDATION. **This is the previously-uncovered bug case; it is now correctly handled.**
- **Non-touch with close-violating-stop (LONG: `low_t > pullback_level AND close_t ≤ structural_stop_level`)** *(NEW under amended precedence)*. Step 3 STRUCTURAL_INVALIDATION fires; candidate CANCELled. Pre-amendment, this bar erroneously continued pending; post-amendment, the candidate is correctly cancelled because the breakout structure has been invalidated regardless of the touch state.
- **Confirmation-without-touch (LONG: `low_t > pullback_level AND close_t > structural_stop_level`).** Step 3 STRUCTURAL_INVALIDATION does not fire (close on the right side of stop). Step 4 TOUCH+CONFIRMATION does not fire (no touch). Step 5 CONTINUE. Behavior unchanged from pre-amendment.
- **Same-bar bias-flip + close-violates-stop.** Step 1 BIAS_FLIP wins (precedence 1 < 3); CANCEL(BIAS_FLIP). Same-bar opposite-signal + close-violates-stop: step 2 OPPOSITE_SIGNAL wins (precedence 2 < 3); CANCEL(OPPOSITE_SIGNAL). Same-bar STRUCTURAL_INVALIDATION + touch: step 3 wins (precedence 3 < 4); CANCEL(STRUCTURAL_INVALIDATION) — touch+confirmation is never reached.
- **Boundary tie at `close_t == structural_stop_level` (LONG).** The `Cancel_structural_t = (close_t ≤ structural_stop_level)` predicate uses non-strict `≤`; a close exactly equal to the structural stop level fires STRUCTURAL_INVALIDATION (cancel). The `Confirmed_t = (close_t > structural_stop_level)` predicate uses strict `>`; a close exactly equal would not satisfy confirmation. Both predicates agree at the boundary: equality means "violated" / "not confirmed", consistent with the H0 protective-stop convention that the stop level itself is the invalidation reference.
- **Fill-time `atr_at_signal == 0`.** `R2_fill_passes_filter` is false (consistent with H0's `passes_stop_distance_filter` returning false on `atr_20_15m <= 0`). Defense-in-depth.

The predicate is deterministic at fixed inputs.

---

## F. Exact committed sub-parameter values

R2 has four sub-parameter axes. Each is committed singularly at one value, with explicit non-fitting rationale anchored to an existing project convention. **No sweeps. No alternatives. No tuning. The values listed here are the values Phase 2u commits; they may not be changed without authorizing a separate operator-approved phase that proposes new values with new non-fitting rationale.**

### F.1 Pullback level — `setup.setup_high` (LONG); `setup.setup_low` (SHORT)

The pullback level is **the breakout level itself**: the same `setup_high` / `setup_low` values used by H0's setup-validity rule and the H0 trigger's `trigger_level = setup.setup_high + 0.10 × ATR(20)_15m` (LONG; symmetric for SHORT).

**Non-fitting rationale.** `setup.setup_high` and `setup.setup_low` are the *structural reference points* of H0's setup-validity definition. They are the values the H0 setup detector outputs (`detect_setup()` in `setup.py`); they are the values the H0 trigger consumes (`trigger_level` in `trigger.py`); they are the values H0's `compute_initial_stop()` consumes. Three independent existing-code sites already use these values as the structural anchor for "the setup boundary". R2's pullback-retest interpretation reuses the same anchor: a pullback retest is a return to the structural reference the setup-and-breakout pattern is built on.

The value is **not** chosen by examining R-window outcomes. It is the project's existing answer to "what is the structural boundary of the breakout pattern?" — re-used unchanged.

Three independent checks against fitting:

1. **The value is taken directly from existing project state** (`SetupWindow.setup_high` / `setup_low`) committed before any R2 research.
2. **The value has not been compared to alternatives.** No backtests have been run with `pullback_level = midpoint of breakout-bar range` or `pullback_level = breakout_bar.open` or any other variant. Phase 2u is docs-only; no parameter sweep is authorized.
3. **The value is symmetric across direction.** LONG uses `setup_high`; SHORT uses `setup_low`. There is no asymmetric specialization.

### F.2 Confirmation rule — bar-close-not-violating-structural-stop

The confirmation rule is satisfied at bar t when `close_t > structural_stop_level` (LONG) or `close_t < structural_stop_level` (SHORT). The bar that touches the pullback level *also* must close above the structural stop on the breakout side; same-bar resolution.

**Non-fitting rationale.** `structural_stop_level` is the project's existing structural-invalidation reference. It is the value `compute_initial_stop()` produces; it is the price level the protective STOP_MARKET is placed at; it is the level whose breach defines the breakout's structural failure. Confirming that the candidate's bar close has not breached the stop reuses the project's existing invalidation convention as the confirmation predicate.

The rule has a clean operational reading: *"the pullback came back to the breakout level, but the bar that touched the breakout level closed above the structural-invalidation level, so the breakout structure is still valid."* If the close has already breached the structural stop, the breakout has already failed; entering at the next bar's open would put the trade immediately in invalidation territory.

The value is **not** chosen by examining R-window outcomes:

1. **The value is taken directly from existing project state** (`compute_initial_stop()` output) computed with H0's existing formula at registration time.
2. **The value has not been compared to alternatives.** No backtests have been run with `confirmation = close-back-above-setup_high` or `confirmation = bar-low-holding-above-stop` or `confirmation = none (passive limit)` or `confirmation = continuation-bar-strength`. Phase 2u is docs-only.
3. **The rule is symmetric across direction.** LONG: `close > structural_stop_level`. SHORT: `close < structural_stop_level`. No asymmetric specialization.

### F.3 Validity window — N = 8 completed 15m bars after registration

The validity window admits bars `(B, B + 8]` — that is, 8 completed 15m bars strictly after the registration bar B. If no FILL or CANCEL has occurred by the close of bar `B + 8`, the candidate EXPIREs.

**Non-fitting rationale.** The value 8 is anchored to **two existing project conventions** that already converge on the same number:

- **`SETUP_SIZE = 8`** in `src/prometheus/strategy/v1_breakout/setup.py`. This is the H0 setup-window length: "the previous 8 completed 15m candles" used to define `setup_high` / `setup_low` and the setup-validity predicate. Eight bars is the project's existing answer to "how long is the setup-relevant time horizon for a 15m breakout pattern?"
- **`exit_time_stop_bars = 8`** as committed in Phase 2j memo §D.6 and locked in Phase 2l for R3. This is the R3 unconditional time-stop horizon: "if a trade has not reached +2 R within 8 bars, exit at market". Eight bars is the project's existing answer to "how long is the post-entry time horizon for a 15m breakout pattern to prove itself?"

Both conventions independently use 8 bars as the relevant time-horizon for breakout-pattern dynamics on the 15m signal timeframe. R2's validity window adopts the same value with the same interpretation: the post-signal time horizon during which a breakout-pattern is expected to either retest or fail is 8 bars. Beyond that horizon, the breakout pattern is no longer fresh; pulling back into it 9+ bars later is mechanically possible but conceptually a different setup.

This is the strongest non-fitting anchor available across the four axes. **Two existing constants converge on 8.**

The value is **not** chosen by examining R-window outcomes:

1. **The value is taken from two existing constants.** `setup_size` and `exit_time_stop_bars`.
2. **The value has not been compared to alternatives.** No backtests have been run with N = 4 or N = 6 or N = 12 or any other value. Phase 2u is docs-only.
3. **The value is symmetric across direction and across symbol.** Same N for LONG / SHORT, same N for BTC / ETH.

### F.4 Fill model — next-bar-open after confirmation

When touch + confirmation occur at bar t close, the FILL is executed at the open of bar `t + 1` as a market order. The fill price is `open_(t+1)`.

**Non-fitting rationale.** This is **H0's existing fill-model convention**: H0's market entry occurs at the next-bar open following the breakout-bar close. R2 inherits the same fill-model convention, applied at the next-bar open following the *confirmation bar* (rather than the breakout bar). The fee model (`taker = 0.0005`), the slippage model (LOW / MED / HIGH per Phase 2f §11.6 cost-sensitivity), and the fill-price computation all reuse H0's existing implementation verbatim.

This is the **most-conservative** of the fill-model options Phase 2t §4.3.4 surveyed:

- **Limit-at-pullback-intrabar** would assume fills at the pullback level on the touch bar itself, requiring bar-high/low look-ahead and a maker-fee path that the project does not currently model. Higher fill rate; lower fill-realism.
- **Bar-close-after-confirmation** would fill at the close of bar t itself, mixing the confirmation event and the fill event at the same price. Intermediate.
- **Next-bar-open-after-confirmation** (committed) cleanly separates the confirmation event (bar t close) from the fill event (bar t+1 open). Reuses H0's existing market-fill code path. Most conservative on the backtest-vs-live realism axis.

The value is **not** chosen by examining R-window outcomes:

1. **The value matches H0's existing fill convention.** No new fill-realism assumption.
2. **The value has not been compared to alternatives within R2.** No backtests have been run with limit-at-pullback or bar-close-after-confirmation. Phase 2u is docs-only.
3. **A fill-model sensitivity diagnostic is mandatory in §P.6**, but only as a sensitivity report cut against the committed value, not as a tuning surface.

**Diagnostic-only sensitivity (Phase 2v Gate 2 clarification).** The §P.6 / Phase 2v run #10 limit-at-pullback intrabar fill model is a **diagnostic-only sensitivity measurement**. It is run once per execution wave for §P.6 reporting purposes and **must never become a production / default config path**. Specifically:

- The committed R2 fill model is next-bar-open after confirmation. This is the only fill model that produces R2 trade records eligible for §10.3 evaluation.
- The implementation must **not** expose the fill model as a configurable knob on `V1BreakoutConfig` (e.g., as an `EntryFillModel` enum field). The committed fill model is hard-coded for `EntryKind.PULLBACK_RETEST`.
- The diagnostic-only sensitivity run is implemented via a **runner-script `--fill-model` argument**, not via a config field, so the production code path always uses the committed model.
- A future operator-approved phase that wants to test alternative fill models must introduce a new candidate (e.g., R2-limit) with its own non-fitting rationale, full §F-style commitment, and full §1.7 binding-test re-evaluation. It cannot be added as a config tweak under R2.

### F.5 Sub-parameter commitment table

| Axis              | Committed value                                 | Non-fitting anchor                                                   | Symbol-symmetric? | Direction-symmetric? |
|-------------------|-------------------------------------------------|----------------------------------------------------------------------|:-----------------:|:--------------------:|
| Pullback level    | `setup.setup_high` (LONG); `setup.setup_low` (SHORT) | H0 setup-validity rule's structural reference (`SetupWindow`)         | YES               | YES (mirrored)       |
| Confirmation rule | `close_t > structural_stop_level` (LONG); `<` (SHORT) | H0 protective-stop level (`compute_initial_stop()`)                   | YES               | YES (mirrored)       |
| Validity window   | N = 8 completed 15m bars                          | `setup_size = 8` AND `exit_time_stop_bars = 8` (two conventions converge) | YES               | YES                  |
| Fill model        | Next-bar-open after confirmation                  | H0's market-on-next-bar-open convention                               | YES               | YES                  |

All four axes commit symmetrically across direction and symbol. All four anchors derive from project values committed before R2 research. No alternative tested. No sweep authorized.

---

## G. Exact relationship to existing setup / trigger / entry / stop / R3-exit logic

R2 only changes entry-lifecycle topology. Everything else is preserved verbatim:

- **Setup detection** (`detect_setup()` in `setup.py`; H0 default `RANGE_BASED` two-clause predicate `range_width <= 1.75 × ATR(20)_15m AND |close[-1] − open[-8]| <= 0.35 × range_width`): **unchanged**. R2 does not combine with R1a's percentile predicate. Setup predicate stays at `setup_predicate_kind = RANGE_BASED`.

- **1h bias** (`evaluate_1h_bias()` in `bias.py`; H0 binary slope direction-sign rule with EMA(50)/EMA(200) and 3-bar slope): **unchanged**. R2 does not combine with R1b-narrow's slope-magnitude check. Bias predicate stays at `bias_slope_strength_threshold = 0.0` (sentinel-based H0 dispatch per Phase 2s).

- **Trigger six-condition cascade** (`trigger.py`: close-broke-level using `BREAKOUT_BUFFER_ATR_MULT = 0.10`, true-range vs ATR using `TRUE_RANGE_ATR_MULT = 1.0`, close-location ratio `CLOSE_LOCATION_RATIO = 0.75`, ATR-regime `ATR_REGIME_MIN = 0.0020`, `ATR_REGIME_MAX = 0.0200`): **unchanged**. The trigger that registers the R2 candidate at bar B is exactly H0's trigger.

- **Initial structural stop** (`compute_initial_stop()` in `stop.py`: `min(setup.setup_low, breakout_bar.low) − STOP_BUFFER_ATR_MULT × ATR(20)_15m` for LONG; symmetric for SHORT): **unchanged in formula and in price level**. The stop level is computed at bar B and frozen at registration as `candidate.structural_stop_level`. The same formula H0 uses; the same price level H0 would have used.

- **Stop-distance band** (`passes_stop_distance_filter()` in `stop.py`: `FILTER_MIN_ATR_MULT = 0.60`, `FILTER_MAX_ATR_MULT = 1.80`): **unchanged**. Applied **twice** under R2: once at registration (using `close_B` as reference price per GAP-20260419-015 convention; rejects candidate registration if outside band) and once at fill time (using actual `fill_price = open_(t+1)` as reference; rejects fill if outside band). Both checks use `candidate.atr_at_signal` (the ATR(20)_15m frozen at bar B), preserving H0's no-look-ahead discipline.

- **R3 exit machinery** (`exit_kind = FIXED_R_TIME_STOP`, `exit_r_target = 2.0`, `exit_time_stop_bars = 8`; same-bar STOP > TAKE_PROFIT > TIME_STOP priority; protective STOP_MARKET never moved intra-trade): **unchanged**. The R3 time-stop horizon **counts from the fill bar**, not from the registration bar. A candidate that fills at bar t+1 begins its R3 8-bar countdown at bar t+1 (R3-consistent interpretation, committed singularly here).

- **Sizing pipeline** (`sizing.compute_size()` with `risk_fraction = 0.0025`, `risk_usage = 0.90`, `max_leverage = 2.0`, `notional_cap = 100_000`, `taker = 0.0005`): **unchanged in shape**. Position size is `risk_amount / stop_distance`; a smaller R2 fill-time `stop_distance` produces a larger position size at fixed equity-risk. The sizing rule is unchanged; the stop-distance input is smaller as a *consequence* of R2's topology change, not as a sizing-rule change.

- **Re-entry lockout** (`StrategySession.can_re_enter` requiring `setup_size = 8` bars after exit before same-direction re-entry): **unchanged after exit**. While a PendingCandidate is active (no exit has occurred), the per-§E.5 pending-uniqueness rule applies: same-direction new signals during the pending phase are dropped silently; opposite-direction new signals trigger OPPOSITE_SIGNAL cancellation of the pending candidate.

- **Phase 2i §1.7.3 project-level locks** (BTCUSDT primary, ETHUSDT research/comparison only, one-position max, one-symbol-only, one-active-protective-stop max, 0.25% risk fraction, 2× max effective leverage, mark-price stops, v002 datasets): **unchanged**.

The R3 time-stop horizon question deserves an explicit commitment: under R2, R3's `exit_time_stop_bars = 8` counts **from the fill bar** (the bar at which the trade is opened), not from the signal bar. A candidate registered at bar B that fills at bar B + 5 begins its R3 8-bar countdown at bar B + 5 and reaches the time-stop at bar B + 13. The end-to-end signal-to-time-stop horizon is thus variable across trades (8 bars for an immediate fill at B + 1 through 16 bars for a fill at B + 8). This "R3-consistent" interpretation is committed singularly in §F.3 above as part of the validity-window definition; the alternative "lifecycle-consistent" interpretation (8 bars from signal regardless of fill bar) is rejected because it would compress R3's exit-machinery time horizon for later-filling candidates and degrade R3's calibration.

---

## H. What H0 rules are replaced

**Only the entry-lifecycle topology.** Specifically:

- H0's "at close of breakout-bar B, fill MARKET at bar B + 1 open" is replaced with the conditional-pending lifecycle described in §B / §E.

The replacement is contained to:

- The decision of *when* a fill occurs (immediately at B + 1 vs at t + 1 for some t ∈ [B + 1, B + 8] vs never).
- The decision of *whether* a fill occurs (always, for any signal that passes registration filters, vs only when touch + confirmation jointly fire within validity window).
- The introduction of a new candidate state (`PendingCandidate`) between trigger evaluation and fill.

No other H0 rule is replaced. No setup-side rule. No bias rule. No trigger condition. No stop formula. No stop-distance band. No exit machinery. No sizing rule. No re-entry rule. No project-level lock.

---

## I. What H0 rules remain unchanged

- The setup-validity predicate (range-width and drift-cap two-clause rule).
- The 8-bar setup window length (`SETUP_SIZE = 8`).
- The 1h EMA(50)/EMA(200) bias regime/position component.
- The 1h slope direction-sign component (binary; `bias_slope_strength_threshold = 0.0`).
- The 3-bar slope-lookback window length (`SLOPE_LOOKBACK = 3`).
- The trigger six-condition cascade (with `BREAKOUT_BUFFER_ATR_MULT = 0.10`, `TRUE_RANGE_ATR_MULT = 1.0`, `CLOSE_LOCATION_RATIO = 0.75`, `ATR_REGIME_MIN = 0.0020`, `ATR_REGIME_MAX = 0.0200`).
- The structural-stop formula (`min(setup_low, breakout_bar.low) − 0.10 × ATR(20)_15m` for LONG; symmetric for SHORT).
- The stop-distance band (`[0.60, 1.80] × ATR(20)_15m`).
- The R3 exit machinery (`exit_kind = FIXED_R_TIME_STOP`, `exit_r_target = 2.0`, `exit_time_stop_bars = 8`; same-bar priority STOP > TAKE_PROFIT > TIME_STOP; protective stop never moved intra-trade).
- The sizing pipeline.
- The re-entry lockout post-exit.
- All Phase 2i §1.7.3 project-level locks.

---

## J. Implementation impact (descriptive only — Phase 2u writes no code)

A future operator-approved execution phase would extend the strategy package roughly as follows. **Phase 2u does not write any of this code; it is described here only so the spec is complete.**

### J.1 Configuration

- **`V1BreakoutConfig`** would gain one new optional enum field: `entry_kind: EntryKind = EntryKind.MARKET_NEXT_BAR_OPEN`. The existing H0 / R3 / R1a / R1b-narrow paths default to `MARKET_NEXT_BAR_OPEN` and preserve bit-for-bit H0 behaviour through the strategy facade. R2 opts in via `entry_kind = EntryKind.PULLBACK_RETEST`.
- The validity window N is **not** a new config field. It is committed at 8 in §F.3 and the implementation should hard-code it as a module-level constant `R2_VALIDITY_WINDOW_BARS = 8` referenced by both the strategy session and tests, with explicit comments referencing its anchoring to `SETUP_SIZE` and `exit_time_stop_bars`.
- The pullback level, confirmation rule, and fill model are **not** new config fields either. They are committed singularly in §F and hard-coded in the R2 entry-lifecycle implementation.

The minimal config surface protects against parameter drift: there is no "tunable knob" for any R2 sub-parameter. A future operator-approved phase that wants to test alternative values must introduce a new config field with its own non-fitting rationale, in a separate phase.

### J.2 New module: `entry_lifecycle.py`

A new module `src/prometheus/strategy/v1_breakout/entry_lifecycle.py` (or equivalent) would contain:

- **`PendingCandidate` dataclass** with frozen fields: `direction`, `registration_bar_index`, `pullback_level`, `structural_stop_level`, `atr_at_signal`, `validity_expires_at`.
- **`evaluate_pending_candidate(candidate, bar_t, bias_t, opposite_signal_t)` function** that returns one of `{CONTINUE, CANCEL_BIAS_FLIP, CANCEL_OPPOSITE_SIGNAL, CANCEL_STRUCTURAL_INVALIDATION, READY_TO_FILL}` *(per Phase 2v Gate 2 amended §E.2)*.
- **`evaluate_fill_at_next_bar_open(candidate, fill_bar_open)` function** that returns one of `{FILL, CANCEL_STOP_DISTANCE_AT_FILL}` and the fill price.

### J.3 `StrategySession` integration

- The session gains an optional `_pending_candidate: Optional[PendingCandidate]` field initialized to None.
- The session's per-bar evaluation logic dispatches:
  - If `entry_kind == MARKET_NEXT_BAR_OPEN`: existing H0/R3 pipeline runs unchanged.
  - If `entry_kind == PULLBACK_RETEST`:
    - If `_pending_candidate is None`: evaluate the trigger pipeline; if it would have produced a market entry, *register* a PendingCandidate instead.
    - If `_pending_candidate is not None`: evaluate `evaluate_pending_candidate()`; on READY_TO_FILL, mark fill at next-bar-open; on cancellation, clear `_pending_candidate`.
- The session's fill execution dispatches to `evaluate_fill_at_next_bar_open()` at next-bar open; on FILL, the trade enters the existing R3 exit pipeline; on CANCEL_STOP_DISTANCE_AT_FILL, `_pending_candidate` is cleared without a trade.

### J.4 Diagnostics funnel

The `run_signal_funnel` in `diagnostics.py` would be extended with new R2-specific buckets:

- **`registered_candidates`.** Count of PendingCandidate objects registered (replaces `entry_intents` for the R2 path; identical semantics as H0's `entry_intents` modulo the topology change).
- **`expired_candidates_no_pullback`.** Count of candidates that EXPIREd at `B + 8` without ever satisfying touch + confirmation (and without any earlier cancellation).
- **`expired_candidates_bias_flip`.** Count of candidates that CANCELled due to bias flip during pending.
- **`expired_candidates_opposite_signal`.** Count of candidates that CANCELled due to opposite-direction signal during pending.
- **`expired_candidates_structural_invalidation`.** *(NEW per Phase 2v Gate 2 amendment.)* Count of candidates that CANCELled due to the close having breached the structural-stop reference on a pending bar, regardless of whether the touch occurred. Captures both same-bar touch + close-violates-stop cases and non-touch + close-violates-stop cases.
- **`expired_candidates_stop_distance_at_fill`.** Count of candidates that touched + confirmed but failed the fill-time stop-distance filter.
- **`trades_filled_R2`.** Count of candidates that filled (= candidates that produced trades). Equivalent to H0's `trades_filled`.

The new buckets allow the **fill rate** (`trades_filled_R2 / registered_candidates`) to be computed and reported.

**Accounting identity** (mandatory invariant, enforced in tests): `registered_candidates = expired_candidates_no_pullback + expired_candidates_bias_flip + expired_candidates_opposite_signal + expired_candidates_structural_invalidation + expired_candidates_stop_distance_at_fill + trades_filled_R2`. Five cancellation buckets + one fill bucket sum to total registrations.

### J.5 Tests

A future execution phase would add tests covering:

- **H0 baseline preservation.** Default `entry_kind = MARKET_NEXT_BAR_OPEN` reproduces H0 + R3 + R1a / R1b-narrow baselines bit-for-bit (sentinel-based dispatch test, mirroring Phase 2s §2.4).
- **R2 registration.** A bar that passes the trigger and stop-distance pre-filter under H0 produces a PendingCandidate when `entry_kind = PULLBACK_RETEST`; the candidate's frozen fields match H0's would-have-been values.
- **R2 touch + confirmation.** A bar within the validity window with `low ≤ pullback_level AND close > structural_stop_level` (LONG) produces READY_TO_FILL.
- **R2 cancellation precedence.** Bias-flip → opposite-signal → structural-invalidation → touch+confirmation evaluation order (5-step precedence per the Phase 2v Gate 2 amended §E.2).
- **R2 STRUCTURAL_INVALIDATION cancellation.** Non-touch bar with close-violating-stop (LONG: `low_t > pullback_level AND close_t ≤ structural_stop_level`) → CANCEL(STRUCTURAL_INVALIDATION); same-bar touch + close-violating-stop (LONG: `low_t ≤ pullback_level AND close_t ≤ structural_stop_level`) → CANCEL(STRUCTURAL_INVALIDATION) wins over touch+confirmation by precedence.
- **R2 expiry.** A candidate with no fill or cancel by `B + 8` close EXPIREs.
- **R2 fill-time stop-distance.** A candidate with fill price producing stop-distance outside `[0.60, 1.80] × atr_at_signal` is CANCELled at fill.
- **R2 pending uniqueness.** Same-direction new signal during pending is dropped silently; opposite-direction new signal triggers OPPOSITE_SIGNAL cancellation of pending candidate.
- **R2 R3 time-stop interaction.** A candidate filling at bar `B + k` (for k ∈ {1, 2, ..., 8}) starts its R3 time-stop countdown at the fill bar; the time-stop fires at `fill_bar + 8`.
- **R2 NaN / warmup handling.** No registration before bias and ATR warmup are complete.
- **R2 H0-baseline preservation under `entry_kind = MARKET_NEXT_BAR_OPEN`.** Sentinel-based dispatch test.

### J.6 Implementation surface estimate

Comparable in scope to Phase 2l's R3 implementation but with more state-machine plumbing:

| Component                                             | Estimated net source/test lines |
|-------------------------------------------------------|--------------------------------:|
| `EntryKind` enum + `V1BreakoutConfig` field           |                            ~30 |
| `entry_lifecycle.py` (PendingCandidate + evaluators)  |                       ~300–400 |
| `StrategySession` integration                          |                       ~150–250 |
| Backtest engine integration (per-bar dispatch)        |                       ~150–250 |
| Diagnostics funnel buckets                            |                          ~100 |
| Unit tests                                            |                       ~600–900 |
| Integration test (H0 + R3 baseline preservation)      |                       ~100–200 |
| **Total estimate**                                    |                  **~1430–2130 lines** |

This is the largest backtester change Phase 2 has contemplated, consistent with Phase 2t §5.6's estimate of ~1500–2500 net lines. The implementation cost is the deferral reason from Phase 2i §3.2 that Phase 2t §11.1 judged justified by exhausted filter-axis alternatives.

---

## K. Expected mechanism of improvement (BTC focus)

The mechanism R2 tests is **entry-timing topology** — specifically that some of H0's BTC stop-outs reflect entering at the breakout-bar's far side from the structural-stop level, where ordinary post-breakout volatility produces a stop-out before the directional follow-through develops.

**Mechanism prediction structure (M1 / M2 / M3, restated from Phase 2t §6.2):**

- **M1 (per-trade expectancy).** Under R2 + R3, BTC per-trade expectancy on R-window improves vs R3 alone: **Δexp_R3 ≥ +0.10 R**. This is the magnitude prediction that distinguishes mechanism-validated improvement from R1b-narrow-style trade-count-reduction-driven framework PROMOTE.
- **M2 (stop-out fraction).** Under R2 + R3, BTC stop-exit count as a fraction of total exits is **strictly lower** than under R3 alone. Trades that R3 would have stopped out due to post-entry whipsaw are either (i) not taken because no pullback retest occurred, or (ii) taken at a smaller stop-distance with proportionally larger position size, hitting the +2 R take-profit before the stop.
- **M3 (R-distance distribution).** Under R2 + R3, BTC mean and median R-distance (entry_price − stop_price, normalized by ATR(20)_15m at signal time) is **strictly smaller** than under R3 alone. This is mechanically guaranteed if R2's pullback-retest entry executes at a price strictly between the breakout-bar close and the structural-stop level.

The expected aggregate effect on BTC: per-trade expectancy improves because filled trades enter at better prices and stop at smaller absolute losses; aggregate edge improves because unfilled candidates incur no loss; trade count drops because some signals never satisfy touch + confirmation within the validity window.

**Mechanism on ETH (secondary):** ETH has a pre-existing direction-asymmetric regime (R3 alone ETH longs −0.934 / shorts +0.028). R2's topology change applies symmetrically; the expected ETH effect is positive but smaller than BTC because ETH's directional regime is already doing most of the work. R2 may improve ETH shorts modestly by entering at better prices; ETH longs may benefit from R2 acting as an implicit filter against breakouts that don't pull back (the worst longs in a bearish-regime ETH window are those that immediately fail without retest). The expected §10.3 path on ETH is §10.3.a or §10.3.c clearance with smaller magnitude than BTC.

---

## L. Expected main failure modes

Phase 2t §7 enumerated nine failure modes; the four most-material are restated here with their mandatory diagnostic mappings.

### L.1 Pullback never comes (low fill rate)

If `trades_filled_R2 / registered_candidates < 30%` on either symbol, the strongest breakouts (which run without retesting) are systematically excluded. R2 trades absolute frequency for per-trade quality. Acceptable if M1 improvement compensates; failed if M1 ≈ 0 and R-window aggregate edge degrades.

**Diagnostic.** §P.1 fill rate; §P.5 intersection-trade comparison vs R3.

### L.2 Pullback exceeds stop / structural invalidation during pending (in-pending rejection rate)

Two distinct failure-mode signatures share the broader "pullback exceeds stop" theme; the Phase 2v Gate 2 amendment separates them cleanly:

- **Structural invalidation during pending** (close has breached the structural stop on a bar within the validity window, with or without touch). Reported under `expired_candidates_structural_invalidation`. If this fraction is high (e.g., > 30% of registered candidates on either symbol), R2's pullback level is too close to bars whose post-breakout volatility carries the close back through the structural stop before any retest+confirmation can happen — the breakout is being invalidated mid-pullback rather than retested.
- **Stop-distance violation at fill time** (touch + confirmation occurred, but the pullback fill price would produce stop_distance outside [0.60, 1.80] × ATR). Reported under `expired_candidates_stop_distance_at_fill`. If this fraction is high (e.g., > 15% of registered candidates on either symbol), the pullback geometry produces too-tight stops on the bars that *did* retest cleanly.

The amended buckets distinguish "the breakout failed before retest" (structural invalidation) from "the retest succeeded but the entry would have been too tight" (stop-distance at fill). These are different mechanism failures with different remediation paths.

**Diagnostic.** §P.1 fill rate decomposed by cancellation reason (now five reasons including STRUCTURAL_INVALIDATION); §P.10 R-distance distribution.

### L.3 Confirmation rule too strict (cancellation rate during pending)

If `expired_candidates_bias_flip + expired_candidates_opposite_signal > expired_candidates_no_pullback`, the bias rule's instability dominates the fill rate, not the geometry of the breakout-pattern. R2's lifecycle is sensitive to bias-rule flicker on intermediate bars, not to genuine pullback dynamics.

**Diagnostic.** §P.1 fill rate decomposed by cancellation reason; §P.7 long/short asymmetry.

### L.4 The stop-out problem isn't entry timing (R3-anchor neutrality on BTC)

If R2 + R3 produces §10.3.a or §10.3.c PROMOTE under H0 anchor but `Δexp_R3 ≈ 0` on BTC (e.g., |Δexp_R3| < 0.05), R2 has reproduced the R1b-narrow pattern: framework PROMOTE driven by trade-count reduction without per-trade expectancy improvement. The BTC failure mode is not entry-timing.

**Diagnostic.** §P.5 intersection-trade comparison vs R3 (the strongest mechanism-validation cut). If R2's improvement on intersection trades is ≈ 0 R per trade, the M1 prediction is falsified despite the framework verdict.

This is the single most strategically important diagnostic. It distinguishes mechanism-validated PROMOTE from trade-count-reduction-driven PROMOTE.

---

## M. Why R2 is structural and not parametric

Phase 2i §1.7.1 binding test enumerates four structural-change criteria. R2 satisfies multiple; it satisfies one verbatim.

### M.1 Rule-shape change (criterion 1)

H0's entry rule has the form *"signal_at_B → fill_at_B+1"* — a function from a single event (the breakout-bar close) to a single output (the next-bar-open fill). The functional shape is **single-event → single-fill**.

R2's entry rule has the form *"signal_at_B → register pending candidate → for each subsequent bar t ∈ (B, B+8], evaluate cancellation and confirmation predicates → fill_at_t+1 OR expire OR cancel"* — a function from a single event to one of three outcomes (fill, expire, cancel) determined by a sequence of subsequent-bar evaluations. The functional shape is **single-event → state-machine → multi-outcome**.

These are different functional forms. The shape changes from a function-of-one-bar to a function-of-up-to-9-bars. Rule-shape change is satisfied.

### M.2 Rule-input domain change (criterion 2)

H0's entry rule consumes the breakout-bar's six-condition trigger state and the next-bar's open price (for fill). The input domain is **{breakout_bar's outputs, next_bar's open}**.

R2's entry rule consumes:
- The breakout-bar's six-condition trigger state (registration).
- For each bar t ∈ (B, B+8]: the bar's low (LONG touch detection), high (SHORT touch detection), close (confirmation), and the 1h bias evaluated at t (cancellation), and the trigger evaluation in the opposite direction at t close (cancellation).
- The fill-bar's open price (fill).

The input domain is **{breakout_bar's outputs, ∀ t ∈ (B, B+8]: (low_t, high_t, close_t, Bias_t, OppSignal_t), fill_bar's open}** — a strict superset of H0's input domain. Rule-input domain change is satisfied.

### M.3 Trade-lifecycle topology change (criterion 4) — verbatim

Phase 2i §1.7.1's example for trade-lifecycle topology change reads:

> Example: replacing "market entry on next-bar open after breakout-bar close" with "limit-order entry at setup boundary, valid for N bars after breakout" — entry topology changes from immediate-fill to conditional-pending.

R2's specification matches this example **verbatim**:

- **From:** "market entry on next-bar open after breakout-bar close" (H0).
- **To:** pullback-retest entry at the **setup boundary** (committed `pullback_level = setup_high / setup_low` per §F.1, which is the setup-validity rule's structural reference), **valid for N = 8 bars after breakout** (committed validity window per §F.3), with confirmation by close-not-violating-stop and fill at next-bar open after confirmation.
- **Topology change:** from immediate-fill (one event triggers fill at next bar) to conditional-pending (one event triggers pending state; subsequent events resolve to fill/cancel/expire).

Trade-lifecycle topology change is satisfied verbatim.

### M.4 Phase 2i §1.7.2 secondary check

Phase 2i §1.7.2 paraphrased: "changing a numeric threshold while keeping the same rule shape" is parametric. R2 introduces:

- A new functional form (single-event → state-machine → multi-outcome).
- New input-domain consumption (subsequent bars' low/high/close, subsequent 1h bias, subsequent opposite-direction trigger evaluations, fill-bar open).
- Three new sub-parameter axes that *parameterize the new form* (pullback level, confirmation rule, validity window) and one fill-model commitment that reuses H0's existing fill convention.

The four sub-parameter values in §F are parameters **of the new form**, not tweaks of an existing parameter. The numeric value 8 (validity window) is a parameter of the new state-machine; H0 has no validity-window threshold to tweak — its entry topology has no concept of validity.

R2 is structural, not parametric. The §1.7 binding test passes cleanly.

### M.5 Comparison to prior structural redesigns

| Candidate    | Axis (Phase 2i family-letter) | Structural change                                                                  |
|--------------|-------------------------------|-------------------------------------------------------------------------------------|
| R1a          | S (setup shape)               | Predicate form (range-based ratio → percentile-based ranking)                       |
| R1b-narrow   | B (bias shape)                | Predicate form (binary direction-sign → magnitude-threshold)                         |
| R3           | X (exit philosophy)           | Exit machinery topology (staged-trailing → fixed-R + time-stop)                      |
| **R2**       | **E (entry mechanic)**        | **Entry-lifecycle topology (immediate-fill → conditional-pending state-machine)**    |

R2 is the fourth of the four structural-redesign axes Phase 2i originally enumerated. It is structurally distinct from the other three; its non-fitting anchors derive from independent project conventions.

---

## N. GAP dispositions

R2 carries-forward existing GAP dispositions and introduces no new GAP entries within Phase 2u. The implementation-ambiguity log is **not** edited in Phase 2u (operator restriction; Phase 2u is docs-only). A future execution phase may surface a new GAP entry for fill-realism in conditional-pending orders if the implementation discovers an ambiguity; that GAP would be created in the execution phase.

| GAP                  | Topic                                                                                          | R2 disposition                                                                                                                                                                                                          |
|----------------------|------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| GAP-20260424-030     | Break-even +1.5R vs +2.0R rule-text conflict                                                    | **CARRIED.** R2 keeps R3 exit logic (no break-even); the conflict stays open. Phase 2l / 2m / 2n / 2o / 2p / 2q / 2r / 2s / 2t dispositions unchanged.                                                                |
| GAP-20260424-031     | EMA slope wording (discrete vs fitted)                                                          | **CARRIED.** R2 does not touch the bias-validity rule; the GAP entry stays open at its Phase 2s disposition.                                                                                                              |
| GAP-20260424-032     | Mark-price stop-trigger sensitivity                                                              | **CARRIED-AND-MORE-RELEVANT.** R2's pullback-retest entry produces strictly smaller stop-distances on filled trades; mark-price proximity to the stop level is a more-sensitive variable than under H0/R3/R1a/R1b-narrow. Required diagnostic in §P.13. |
| GAP-20260424-033     | Stagnation window classification                                                                 | **CARRIED.** R2 keeps R3's exit logic; the GAP-033 disposition is unchanged from Phase 2l.                                                                                                                              |
| GAP-20260424-036     | 5-rolling-fold consistency at sample-size lower bound                                            | **CARRIED.** R2 expected to operate at or below R1b-narrow's per-fold sample-size lower bound. Same caveat-discipline applied.                                                                                            |
| GAP-20260419-015     | stop_distance reference price (close vs fill) ambiguity                                          | **CARRIED-AND-MORE-RELEVANT.** R2 explicitly uses the GAP-015 resolution at registration time (close_B as reference price). At fill time, R2 uses the actual fill_price. Both use the frozen `atr_at_signal`. The dual-check structure is consistent with the GAP-015 resolution and explicit in §G above. |
| **NEW (deferred to execution-phase if needed)** | Fill-realism for conditional-pending orders (limit vs market; maker fees vs taker fees; intra-bar fill discipline) | **NOT CREATED in Phase 2u.** R2 commits the most-conservative fill model (next-bar-open-after-confirmation, market-on-open, taker fees) precisely to avoid a new GAP entry. If a future execution phase discovers an ambiguity in the fill-realism path, the GAP entry is created at that point. |

No GAP changes in Phase 2u.

---

## O. Candidate-specific falsifiable hypothesis

> **R2 hypothesis (pre-committed):** On R = 2022-01-01 → 2025-01-01 with v002 datasets, an R2 variant — H0 setup + H0 trigger + H0 bias + R2 conditional-pending entry topology with sub-parameters committed singularly per §F (`pullback_level = setup.setup_high / setup_low`; `confirmation = close_t > / < structural_stop_level`; `validity_window = 8 bars`; `fill_model = next-bar-open after confirmation`) + R3 exit logic locked + all other rules at H0 defaults — produces a §10.3-passing result vs H0 baseline.
>
> The acceptable §10.3 paths are:
>
> - **§10.3.a** (Δexp ≥ +0.10 R AND ΔPF ≥ +0.05) — the magnitude path. **Expected primary path** under the M1 mechanism prediction.
> - **§10.3.c** (strict dominance: Δexp > 0 AND ΔPF > 0 AND Δ|maxDD| ≤ 0) — the dominance fallback.
> - **§10.3.b** (Δn ≥ +50%) — **mechanically unavailable**; R2's filter geometry reduces trade count.
>
> No §10.3 disqualification floor may be triggered (no worse expR, no worse PF, |maxDD| ≤ 1.5× baseline) on either BTC or ETH per §11.4 ETH-as-comparison rule.
>
> §11.6 cost-sensitivity gate: must clear at HIGH slippage (no §10.3 disqualification floor triggered) on both symbols. R2's smaller stop-distance interacts with slippage differently than H0's market-fill geometry; the HIGH-slippage cut is more material than for prior candidates.
>
> §11.3 V-window: R-window PROMOTE → V-window confirmation run; V-window failure on n < 3 trades does not retroactively change R-window classification but does end the candidate's wave (per Phase 2s precedent).
>
> **The hypothesis is FALSIFIED if** R2 fails §10.3 on BTC OR triggers §10.3 disqualification floor on BTC OR triggers §10.3 disqualification on ETH per §11.4 ETH-as-comparison rule.
>
> **The hypothesis is INDETERMINATE if** R2 clears §10.3 on R but fails on V (per §11.3 no-peeking discipline; failure on V does not retroactively change R-window classification but does end the candidate's wave).
>
> **The mechanism is VALIDATED (separately from the framework verdict) if all three of:**
> - **M1.** Δexp_R3 ≥ +0.10 R on BTC (per-trade expectancy improvement against R3 anchor, not just H0 anchor).
> - **M2.** BTC stop-exit count fraction (`stop_exits / total_exits`) under R2 + R3 is strictly lower than under R3 alone.
> - **M3.** BTC mean R-distance under R2 + R3 is strictly smaller than under R3 alone (mechanically guaranteed if implementation is correct; first-line bug check).
>
> **The mechanism is NOT VALIDATED, but framework verdict may still pass,** if Δexp_R3 < +0.05 R on BTC despite §10.3.a clearance vs H0 (the R1b-narrow pattern: trade-count-reduction-driven framework PROMOTE without per-trade-expectancy improvement). In this case the candidate PROMOTES under §10.3 unchanged but the strategic interpretation is the same as Phase 2s's: framework discipline preserves the formal verdict; absolute-edge case is not strongly supported; operator must independently judge whether to advance any further.

The hypothesis is most-likely-true if BTC's H0/R3 stop-out rate reflects the post-entry whipsaw mechanism and pullback-retest entry materially improves entry-price geometry. It is most-likely-false if BTC's failure mode is structural to the breakout-and-bias filter rather than to the entry-timing; in that case R2 reproduces the R1b-narrow pattern (framework PROMOTE without R3-anchor improvement) and the operator faces the same strategic interpretation question as after Phase 2s.

---

## P. Candidate-specific mandatory diagnostics

A future execution phase must record the following diagnostics. The diagnostics apply to the candidate run alongside H0 and R3 controls (mirroring Phase 2l / 2m / 2s pattern). All numeric values must be reported per-symbol; per-fold and per-regime decompositions are required where noted.

### P.1 Fill rate (core R2 diagnostic)

For each symbol on R-window, report:
- `registered_candidates` (count).
- `expired_candidates_no_pullback`, `expired_candidates_bias_flip`, `expired_candidates_opposite_signal`, `expired_candidates_structural_invalidation`, `expired_candidates_stop_distance_at_fill` (counts; sum = registered − filled).
- `trades_filled_R2` (count).
- **Fill rate** `:= trades_filled_R2 / registered_candidates`.

**Accounting identity** (mandatory; tested per §P.14 implementation-bug check): `registered_candidates = expired_candidates_no_pullback + expired_candidates_bias_flip + expired_candidates_opposite_signal + expired_candidates_structural_invalidation + expired_candidates_stop_distance_at_fill + trades_filled_R2`. Five cancellation buckets (per Phase 2v Gate 2 amended §J.4) + one fill bucket sum to total registrations.

Per-symbol fill-rate is the single most-informative R2-specific diagnostic. Acceptable range (descriptive, not committed): roughly 30–80%; outside this range raises questions about §L.1 / §L.2 / §L.3 failure modes.

### P.2 Pullback-touch distribution (bars-to-touch)

For each filled candidate, record the number of completed 15m bars between registration (bar B) and the first touch + confirmation (bar t). Distribution is `t − B ∈ {1, 2, ..., 8}`.

Per-symbol histogram. Mean / median / quartiles.

If the distribution is concentrated at `t − B = 1` or `t − B = 2`, the validity window is much longer than needed (most fills happen quickly). If concentrated at `t − B ≥ 6`, the validity window is binding for most fills (longer windows would change the candidate's behavior materially). The distribution informs whether the §F.3 anchor (8 bars) is well-chosen.

### P.3 Stop-distance reduction

For each filled R2 candidate, compute the stop-distance ratio:

```
stop_distance_ratio := |R2_fill_price − structural_stop_level| / |R3_would_have_been_entry − structural_stop_level|
```

Where `R3_would_have_been_entry = open at bar B + 1` (the price R3 would have entered at on the same signal under H0/R3 entry timing).

Per-symbol mean / median / quartiles. Expected to be **strictly less than 1.0** (R2 enters at a smaller stop-distance than R3 would have).

If `stop_distance_ratio ≈ 1.0`, R2 is filling at near-H0 prices (pullback was minimal); the topology change is mechanically active but functionally near-equivalent to H0. M3 mechanism prediction is still satisfied trivially but the magnitude of the change is small.

### P.4 Stop-exit fraction comparison

Report `stop_exits / total_exits` per symbol for:
- H0 baseline (locked Phase 2e number).
- R3 alone (locked Phase 2l number).
- R2 + R3 (candidate run).

M2 mechanism prediction: R2 + R3's BTC ratio is strictly lower than R3 alone's BTC ratio. ETH ratio direction informs the §10.3 path on ETH.

### P.5 Intersection-trade comparison vs R3 (strongest mechanism-validation diagnostic)

Define the "intersection set" as candidates that:
- Would have been entered by R3 alone (i.e., the bar passed H0 trigger + bias + stop-distance pre-filter), AND
- Were filled by R2 (i.e., the candidate satisfied touch + confirmation + fill-time stop-distance).

For each trade in the intersection set, compare:
- R2 fill price vs R3 would-have-been entry price.
- R2 R-distance vs R3 R-distance.
- R2 trade outcome (expR per trade) vs R3 hypothetical trade outcome (expR per trade computed by simulating the same exit machinery on the same bar history with R3's entry price).

Per-symbol mean expR difference: `Δexp_intersection := mean(R2_expR) − mean(R3_expR)`.

This is the **strongest M1-validation diagnostic.** If `Δexp_intersection ≥ +0.10 R` on BTC, R2's improvement is genuinely from price-improvement on the same trades, not from selection bias (i.e., R2 picking a different subset of trades from the broader signal pool). If `Δexp_intersection ≈ 0 R`, R2's improvement (if any) is from selection bias (same subset = same results; the trades not in the intersection set are the difference); the R1b-narrow pattern is reproducing.

### P.6 Fill-model sensitivity (cost-realism diagnostic)

Run R2 + R3 on R-window with two fill models:
- **Committed:** next-bar-open after confirmation (per §F.4).
- **Sensitivity cut:** limit-at-pullback-intrabar (fills at `pullback_level` on the touch bar itself, with maker fee = taker fee = 0.0005 for cost-baseline; a separate maker-fee variant is *not* required in Phase 2u).

Report the divergence in expR / PF / netPct / maxDD between the two fill models.

If divergence is small (< 0.05 R per trade), R2's behavior is robust to the fill-model choice and the §F.4 commitment is well-justified. If divergence is large (> 0.10 R per trade), the candidate is fill-model-sensitive and the §F.4 committed conservative model is producing materially different results from the more-aggressive model — this is a flag for backtest-vs-live gap concerns in eventual paper/shadow.

### P.7 Long/short asymmetry

Per-symbol long/short decomposition of `n_trades / WR / expR / PF` for:
- H0 baseline.
- R3 alone.
- R2 + R3.

R1a+R3 introduced direction-asymmetry on ETH that R3 alone did not (Phase 2m); R1b-narrow introduced direction-asymmetry on BTC that R3 alone did not (Phase 2s, n=4 BTC shorts +0.136 was direction-asymmetric vs R3 −0.230). R2's expected direction-symmetry profile is preserved (the entry-mechanic rule is symmetric across direction); deviation is informative.

### P.8 Per-fold consistency (GAP-036)

5 rolling folds, fold-1 partial-train, all test windows inside R. Report per-fold `n_trades`, `expR`, and per-fold deltas vs both H0 and R3 anchors.

Per Phase 2s precedent, per-fold sample sizes may be uninterpretable on R2 BTC. Sample-size caveats applied descriptively; framework verdict on aggregate is the governing reading.

### P.9 Per-regime expR

Realized 1h-vol terciles (trailing 1000 1h-bar Wilder ATR(20), 33/67 splits per Phase 2l / 2m / 2s convention).

Per-regime decomposition for H0 / R3 / R2 + R3 on both symbols. Six regime-symbol cells.

R3 alone improved all 6 regime-symbol cells (Phase 2l). R1a+R3 was regime-localized (ETH low_vol +0.281 / 1.353 was the strongest cell). R1b-narrow was sample-too-small in low_vol cells. R2's per-regime distribution informs whether the entry-mechanic improvement is regime-conditional or broad-based.

### P.10 R-distance distribution

For R2 + R3 candidates, distribution of R-distance (entry_price − stop_price for LONG; symmetric for SHORT) normalized by `atr_at_signal`.

Per-symbol mean / median / quartiles. Compared to R3 alone's R-distance distribution.

M3 mechanism prediction: R2 + R3's mean and median normalized R-distance is strictly less than R3 alone's. Mechanically guaranteed if implementation is correct; serves as first-line bug check.

### P.11 Time-to-fill distribution

Already covered in §P.2. Cross-referenced here as a separate mandatory cut for clarity.

### P.12 MFE / MAE distribution at fill

For each filled R2 candidate, MFE and MAE measured *from the R2 fill price* (not from the signal-bar close).

Per-symbol mean / median / quartiles. Compared to R3 alone's MFE / MAE distribution.

If R2's MFE distribution is approximately preserved relative to R3 (similar shape, similar mean), R2's filled trades have similar best-case behaviour as R3's filled trades — meaning R2's improvement (if any) is from entry-price-improvement and from cancellation-of-bad-trades, not from selecting different best-case trade-quality bars.

If R2's MFE distribution has a smaller mean than R3's, R2 is filtering out the strongest moves (the ones that don't pull back). This is the §L.1 failure mode signature.

### P.13 Mark-price vs trade-price stop-trigger sensitivity (GAP-032)

Required cut. Run R2 + R3 with `stop_trigger_source = MARK_PRICE` (default per Phase 2l / 2m / 2s) and with `stop_trigger_source = TRADE_PRICE`.

Report bit-identicality OR divergence. Expected to be more sensitive than H0/R3/R1a/R1b-narrow because R2's smaller stop-distance brings the protective-stop level closer to the mark-price tracking precision. Measured divergence is descriptive; the candidate must clear §10.3 framework on both trigger sources.

### P.14 Implementation-bug check

- Zero TRAILING_BREACH and zero STAGNATION exits on any R3-or-R2+R3 trade log (R3 exit logic preserved bit-for-bit; R2 does not touch exits).
- H0 control re-run reproduces locked Phase 2e baseline bit-for-bit (default `entry_kind = MARKET_NEXT_BAR_OPEN` preserves H0 behavior).
- R3 control re-run reproduces locked Phase 2l baseline bit-for-bit (R3 exit machinery preserved).
- For R2 + R3: every filled trade has `R2 fill price`, `structural_stop_level`, `R-distance`, `time-to-fill` recorded. Every CANCELled or EXPIREd candidate has its cancellation reason recorded.
- For R2 + R3: every filled trade's protective STOP_MARKET is placed at the candidate's frozen `structural_stop_level`, not at a recomputed value at fill bar.

### P.15 Diagnostic summary table

| Diagnostic                                          | Per-symbol | Per-fold | Per-regime | Per-direction | Mechanism-prediction tested |
|-----------------------------------------------------|:----------:|:--------:|:----------:|:-------------:|:---------------------------:|
| P.1 Fill rate (with cancellation decomposition)      |     ✓      |          |            |               |             —              |
| P.2 Pullback-touch distribution                      |     ✓      |          |            |       ✓       |             —              |
| P.3 Stop-distance reduction (R2 vs R3 same signal)   |     ✓      |          |            |               |       M3 (geometry)         |
| P.4 Stop-exit fraction comparison                    |     ✓      |          |            |               |       M2 (mechanism)        |
| P.5 Intersection-trade comparison vs R3              |     ✓      |          |            |       ✓       |       M1 (per-trade exp)    |
| P.6 Fill-model sensitivity                            |     ✓      |          |            |               |             —              |
| P.7 Long/short asymmetry                              |     ✓      |          |            |       ✓       |             —              |
| P.8 Per-fold consistency (GAP-036)                    |     ✓      |    ✓     |            |               |             —              |
| P.9 Per-regime expR                                   |     ✓      |          |     ✓      |               |             —              |
| P.10 R-distance distribution                          |     ✓      |          |            |       ✓       |       M3 (geometry)         |
| P.11 Time-to-fill distribution (= P.2)                |     ✓      |          |            |               |             —              |
| P.12 MFE / MAE distribution at fill                   |     ✓      |          |            |               |             —              |
| P.13 Mark-price vs trade-price stop-trigger (GAP-032) |     ✓      |          |            |               |             —              |
| P.14 Implementation-bug check                         |     ✓      |          |            |               |             —              |

---

## Threshold preservation

Phase 2f §§ 10.3 / 10.4 / 11.3 / 11.4 / 11.6 thresholds applied unchanged. No post-hoc loosening per §11.3.5. Phase 2j §C.6 R1a sub-parameters preserved (R1a is not part of R2). Phase 2j §D.6 R3 sub-parameters preserved (R3 is the locked exit baseline). Phase 2r §F R1b-narrow sub-parameter preserved (R1b-narrow is not part of R2). GAP-20260424-036 fold convention applied unchanged. GAP-20260424-031 / 032 / 033 carried forward unchanged. GAP-20260419-015 stop-distance reference-price convention applied unchanged (close_B at registration; fill_price at fill-time check; both with `atr_at_signal`). No new GAP entries introduced in Phase 2u. Phase 2i §1.7.3 project-level locks preserved (H0 anchor; BTCUSDT primary; ETHUSDT research/comparison only; one-position max; one-symbol-only; 0.25% risk; 2× leverage; mark-price stops; v002 datasets).

---

## Wave / phase preservation

Phase 2g Wave-1 REJECT ALL preserved as historical evidence only. Phase 2l R3 PROMOTE preserved unchanged (R3 sub-parameters frozen, designated baseline-of-record per Phase 2p). Phase 2m R1a+R3 mixed-PROMOTE preserved unchanged (retained-for-future-hypothesis-planning per Phase 2p §D). Phase 2s R1b-narrow PROMOTE / PASS preserved unchanged (formal-framework-strongest result with explicit per-trade-expectancy and sample-size caveats; bias-strength conclusion: not the missing mechanism per operator + ChatGPT joint interpretation). H0 anchor preserved as the sole §10.3 / §10.4 anchor.

---

## Safety posture

Research-only. No live trading. No exchange-write paths. No production keys. No `.mcp.json`, no Graphify, no MCP server activation. No `.env` changes, no credentials, no Binance API calls (authenticated or public). No edits to `docs/12-roadmap/technical-debt-register.md`. No edits to the implementation-ambiguity log. No edits to `.claude/`. No edits to source files, test files, scripts, datasets, or manifests. No `data/` writes. No Phase 4 work. No paper/shadow planning. No live-readiness claim. No code in Phase 2u. No backtests in Phase 2u. No parameter tuning in Phase 2u. No candidate-set widening in Phase 2u (only R2 is on the spec surface). No multi-axis combination authorized (no R2 + R1a; no R2 + R1b-narrow; no R2 + R1a + R3 except where R3 is the standard locked exit baseline as specified in §G). Mark-price stop-trigger semantic preserved (MARK_PRICE default; TRADE_PRICE only as sensitivity diagnostic in any future execution wave per §P.13). R3 sub-parameters frozen. R1a sub-parameters frozen. R1b-narrow sub-parameter frozen. The 8-bar setup window unchanged. No new structural-redesign candidate exposed beyond H0 / R3 / R1a+R3 / R1b-narrow / R2-as-spec-surface.

---

**End of Phase 2u R2 (pullback-retest entry) spec memo.** Sections A–P complete. Single-axis structural redesign of H0's entry-lifecycle topology — the Phase 2i §1.7.1 verbatim "trade-lifecycle topology change" example. Four sub-parameter values committed singularly with non-fitting rationale: pullback level = `setup.setup_high / setup_low` (anchored to H0 setup-validity rule's structural reference); confirmation = `close_t > / < structural_stop_level` (anchored to H0 protective-stop level via `compute_initial_stop()`); validity window = 8 bars (anchored to `setup_size = 8` AND `exit_time_stop_bars = 8`); fill model = next-bar-open after confirmation (anchored to H0's market-on-next-bar-open convention). R3 exit machinery preserved verbatim with R3-consistent time-stop horizon (8 bars from fill bar). H0 setup, bias, trigger, stop, sizing, re-entry preserved verbatim. Phase 2i §1.7.3 project-level locks preserved. Phase 2f §§ 10.3 / 10.4 / 11.3 / 11.4 / 11.6 thresholds preserved unchanged. GAP dispositions carried; no new GAP entries. Falsifiable hypothesis recorded with M1 / M2 / M3 mechanism-validation predictions distinct from framework verdict. Mandatory diagnostics enumerated in §P.1–P.14. Backtester-implementation surface estimated at ~1430–2130 net lines (descriptive only).

**No code changes after spec drafting; no new runs; no parameter tuning; no candidate-set widening; no Phase 4 / paper-shadow / live-readiness work; no MCP / Graphify / `.mcp.json`; no credentials.** Phase 2u itself does **not** authorize execution; a separate operator-approved Gate 1 plan is required to run R2 against H0 + R3 controls on R-window with V-window confirmation and mandatory diagnostics. Phase 2u is complete and ready for operator/ChatGPT Gate 2 review. Stop after producing this memo.
