# Phase 2v — R2 Gate 1 Execution Plan

**Phase:** 2v — Docs-only Gate 1 execution-planning for R2 (pullback-retest entry).
**Branch:** to be created after Gate 1 approval (proposed: `phase-2v/r2-execution-planning`).
**Plan date:** 2026-04-27 UTC.
**Working directory:** `C:\Prometheus`.

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; no post-hoc loosening per §11.3.5); Phase 2g Wave-1 REJECT ALL (preserved as historical evidence only); Phase 2h decision memo; Phase 2i §1.7 binding test and §1.7.3 project-level locks (H0 anchor; BTCUSDT primary; ETHUSDT research/comparison only; one-position max; one-symbol-only; 0.25% risk; 2× leverage; mark-price stops; v002 datasets); Phase 2j memo §C / §D (spec-style template); Phase 2k Gate 1 plan (R3 execution-planning template); Phase 2l comparison report (R3 PROMOTE locked; baseline-of-record per Phase 2p); Phase 2m comparison report (R1a+R3 retained-for-future-hypothesis-planning per Phase 2p); Phase 2n strategy-review memo; Phase 2o asymmetry-review memo; Phase 2p consolidation memo; Phase 2r R1b-narrow spec memo; Phase 2s R1b-narrow execution comparison report (PROMOTE on R; PASS classification with R3-anchor-neutrality and sample-size caveats); Phase 2t R2 Gate 1 planning memo (GO recommendation conditional on §11.3 discipline locks); Phase 2u R2 spec memo (four sub-parameters committed singularly with non-fitting rationale; M1/M2/M3 mechanism predictions distinct from §10.3 framework verdict); GAP-20260419-015 (stop-distance reference price); GAP-20260424-031 / 032 / 033 / 036 (carried unchanged); operator approval to proceed with Phase 2v Gate 1 execution-planning.

**Status:** Gate 1 plan only. **No code, no runs, no parameter tuning, no sweeps, no candidate-set widening, no Phase 4 / paper-shadow / live-readiness work, no MCP / Graphify / `.mcp.json`, no credentials, no dataset changes, no spec changes.** This plan describes exactly how a future operator-approved Phase 2w execution phase would implement and run R2 against H0 and R3 controls, but Phase 2v itself does **not** authorize implementation or execution. A separate operator Gate 2 review and an explicit operator authorization are required before any code change or run.

> **Gate 2 amendment (2026-04-27).** Per the Phase 2v Gate 2 review (`2026-04-27_phase-2v_gate-2-review.md`), this plan is amended in-place to (1) propagate the new STRUCTURAL_INVALIDATION cancellation reason from the amended Phase 2u §B / §E.2 / §E.6 / §J.4 / §P.1 into the implementation checklist, diagnostics funnel, per-trade record schema, test list, accounting identity, and risk checklist; (2) strengthen the diagnostic-only framing of the limit-at-pullback intrabar fill model (Phase 2v run #10 / §4.6 / §6.2). **No committed sub-parameter values change**; **no §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds change**; **no run inventory entries are added or removed** (10 runs unchanged). Affected sections: §1.5 (run #10 row note), §3.1.2, §3.1.5, §3.1.6, §3.1.7, §3.2.3, §4.1, §4.6, §6.1, §6.2. See the Gate 2 review for the full finding rationale, verification, and approval recommendation.

This plan covers the six sections required by the operator's brief:

1. Execution scope (datasets, symbols, time windows, cost model).
2. Control variants (H0 baseline, R3 baseline, R2 + R3 candidate).
3. Backtest requirements (implementation checklist, validation requirements).
4. Diagnostics plan (exact computation of P.1–P.14, reporting structure).
5. Gate criteria (§10.3 thresholds, mechanism validation M1/M2/M3, failure conditions).
6. Risk checklist (fill-model sensitivity, sample size, BTC vs ETH interpretation).

Threshold preservation, wave/phase preservation, and safety posture sections close the plan.

---

## 1. Execution scope

### 1.1 Datasets

The execution phase uses **only the locked Phase 2e v002 datasets**. No new downloads. No new dataset versions. No manifest changes. No pre-processing changes. The datasets are:

| Dataset                                       | Symbols           | Source                            |
|-----------------------------------------------|-------------------|-----------------------------------|
| 15m completed klines (`klines_15m`)            | BTCUSDT, ETHUSDT  | Binance USDⓈ-M futures (v002)     |
| 1h derived klines (`klines_1h_derived`)        | BTCUSDT, ETHUSDT  | derived from 15m per Phase 2e     |
| Mark-price 15m bars (`mark_price_15m`)          | BTCUSDT, ETHUSDT  | Binance USDⓈ-M futures (v002)     |
| Funding-rate history (`funding_rate`)          | BTCUSDT, ETHUSDT  | Binance USDⓈ-M futures (v002)     |
| Exchange-info snapshot                         | BTCUSDT, ETHUSDT  | v002                              |

The `data/` tree is git-ignored; all run artifacts under `data/derived/backtests/phase-2w-*/` (or whatever name the future execution phase commits to) remain git-ignored.

### 1.2 Symbols

- **BTCUSDT — primary.** The §10.3 / §10.4 governing comparison anchor is BTC. §11.4 ETH-as-comparison rule requires BTC must clear; ETH must not catastrophically fail.
- **ETHUSDT — secondary / comparison only.** Per Phase 2i §1.7.3 lock, ETH remains research/comparison only and is not a deployable target.

Both symbols are run in every phase of the plan. ETH metrics are reported alongside BTC for §11.4 evaluation but ETH does not by itself promote or demote the candidate.

### 1.3 Time windows (R + V)

Per Phase 2f §11.1 split, preserved unchanged through Phases 2g–2u:

- **R-window** = 2022-01-01 00:00:00 UTC → 2025-01-01 00:00:00 UTC. **36 months.** Used for the §10.3 governing evaluation.
- **V-window** = 2025-01-01 00:00:00 UTC → 2026-04-01 00:00:00 UTC. **15 months.** Used for §11.3 V-window confirmation only after R-window PROMOTE.

R-window is run for all three variants (H0, R3, R2+R3). V-window is run only if R2 + R3 PROMOTES on R (per Phase 2f §11.3 no-peeking discipline).

### 1.4 Cost model

Per Phase 2f §11.6 cost-sensitivity gate. The cost model has two dimensions:

- **Slippage tier**: `LOW` (1 bps), `MEDIUM` (3 bps; default), `HIGH` (8 bps). Authoritative values per `src/prometheus/research/backtest/config.py` `DEFAULT_SLIPPAGE_BPS[SlippageBucket.HIGH] = 8.0`. All Phase 2w runs used the canonical code value (8.0 bps for HIGH). Applied symmetrically as taker-side slippage on entry and exit fills. *(Note: a prior draft of this plan stated HIGH ≈ 3× MED ≈ 9 bps; the canonical code value is 8 bps. The plan wording is corrected here for consistency with the code; no metrics, verdicts, thresholds, or interpretations change — every Phase 2 run since the canonical value was committed has used 8 bps.)*
- **Stop trigger**: `MARK_PRICE` (default per §1.7.3 mark-price-stops lock), `TRADE_PRICE` (sensitivity diagnostic per GAP-20260424-032).

Default cost model for the governing R-window run: **MEDIUM slippage + MARK_PRICE stop trigger**.

Per-symbol fee assumptions are unchanged from Phase 2s and prior phases:

- `taker_fee = 0.0005` (5 bps; Binance USDⓈ-M futures taker tier).
- No maker-fee path is committed in Phase 2v — the §F.4 fill model commits to next-bar-open after confirmation, which is a market fill at next-bar open and uses taker fees on both legs.
- Funding cost computed from `funding_rate` dataset, applied per-funding-window during held positions.

Sizing parameters unchanged from Phase 2s and prior:

- `sizing_equity = 10,000 USDT`.
- `risk_fraction = 0.0025` (0.25% per trade; §1.7.3 lock).
- `risk_usage = 0.90` (research-default; below-90% buffer for cost overhead).
- `max_leverage = 2.0` (§1.7.3 lock).
- `notional_cap = 100,000 USDT` (research-default; one-position-max under §1.7.3).
- `min_qty_step` and `min_notional` from exchange-info v002 snapshot per symbol.

### 1.5 Run inventory

The run inventory is fully enumerated below. Each row is one independent backtest run with deterministic config; no run depends on the output of another (so all R-window control runs may be parallelized; V-window runs are gated on R-window PROMOTE).

| #  | Variant     | Window | Slippage | Stop trigger | Fill model (R2 only)              | Notes                                                  |
|----|-------------|--------|----------|--------------|-----------------------------------|--------------------------------------------------------|
| 1  | H0          | R      | MEDIUM   | MARK_PRICE   | (n/a)                             | Baseline reproduction; expected bit-for-bit match       |
| 2  | R3          | R      | MEDIUM   | MARK_PRICE   | (n/a)                             | R3 baseline reproduction; expected bit-for-bit match    |
| 3  | R2 + R3     | R      | MEDIUM   | MARK_PRICE   | next-bar-open after confirmation  | **Governing run.** Drives §10.3 / §11.4 verdict        |
| 4  | H0          | V      | MEDIUM   | MARK_PRICE   | (n/a)                             | V-window control                                       |
| 5  | R3          | V      | MEDIUM   | MARK_PRICE   | (n/a)                             | V-window R3 control                                    |
| 6  | R2 + R3     | V      | MEDIUM   | MARK_PRICE   | next-bar-open after confirmation  | **Run only if R-window PROMOTES** (§11.3 gating)       |
| 7  | R2 + R3     | R      | LOW      | MARK_PRICE   | next-bar-open after confirmation  | §11.6 slippage sensitivity (LOW)                       |
| 8  | R2 + R3     | R      | HIGH     | MARK_PRICE   | next-bar-open after confirmation  | §11.6 slippage sensitivity (HIGH); must clear §10.3    |
| 9  | R2 + R3     | R      | MEDIUM   | TRADE_PRICE  | next-bar-open after confirmation  | GAP-032 stop-trigger sensitivity                       |
| 10 | R2 + R3     | R      | MEDIUM   | MARK_PRICE   | **limit-at-pullback intrabar** *(diagnostic-only; runner-script flag, never a config field)* | §P.6 fill-model sensitivity diagnostic                 |

Total: **10 runs**, comparable to Phase 2s's 9. Runs 1–6 are the governing + control + V-window set. Runs 7–9 are the cost-sensitivity / stop-trigger-sensitivity required cuts. Run 10 is the R2-specific fill-model sensitivity diagnostic (no precedent; covered in §4.6 below).

**Run #10 is diagnostic-only (Phase 2v Gate 2 clarification).** The limit-at-pullback intrabar fill model exists solely as a runner-script `--fill-model` argument for §P.6 sensitivity reporting. It must **not** be exposed as a `V1BreakoutConfig` field; the production code path always uses the §F.4-committed next-bar-open-after-confirmation fill model. No R2 trade record produced under run #10 is eligible for §10.3 evaluation; only run #3's output drives the framework verdict.

---

## 2. Control variants

### 2.1 H0 control

**Configuration.** All `V1BreakoutConfig` fields at H0 defaults:

- `setup_predicate_kind = RANGE_BASED` (H0 default; H0 setup-validity rule).
- `setup_size = 8`.
- `bias_slope_strength_threshold = 0.0` (sentinel-based H0 dispatch per Phase 2s §2.4; preserves H0 binary direction-sign check bit-for-bit).
- `exit_kind = STAGED_TRAILING` (H0 default; staged risk reduction + trailing).
- `entry_kind = MARKET_NEXT_BAR_OPEN` (the new field introduced by R2; default value preserves H0).
- All other H0 defaults unchanged.

**Expected R-window numbers (Phase 2e baseline; locked through Phase 2g / 2l / 2m / 2s):**

| Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   |
|---------|-------:|-------:|--------:|------:|--------:|--------:|
| BTCUSDT |     33 | 30.30% | −0.459  | 0.255 | −3.39%  | −3.67%  |
| ETHUSDT |     33 | 21.21% | −0.475  | 0.321 | −3.53%  | −4.13%  |

**Expected V-window numbers (Phase 2s locked):**

| Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   |
|---------|-------:|-------:|--------:|------:|--------:|--------:|
| BTCUSDT |      8 | 25.00% | −0.313  | 0.541 | −0.56%  | −0.87%  |
| ETHUSDT |     14 | 28.57% | −0.174  | 0.695 | −0.55%  | −0.80%  |

**Validation requirement.** All H0 control numbers reproduce **bit-for-bit** (exact decimal match on Trades, WR, expR, PF, netPct, maxDD per symbol per window). Any deviation indicates the new `EntryKind` enum and dispatch logic silently regressed H0 behaviour. **Block execution-phase progression until reproduction is bit-for-bit.**

### 2.2 R3 control

**Configuration.** R3 sub-parameters per Phase 2j memo §D.6 / Phase 2l locked:

- `setup_predicate_kind = RANGE_BASED` (H0 default; R3 does not touch setup).
- `setup_size = 8`.
- `bias_slope_strength_threshold = 0.0` (H0 default; R3 does not touch bias).
- `exit_kind = FIXED_R_TIME_STOP` (R3 commit).
- `exit_r_target = 2.0` (R3 commit; matches `STAGE_5_MFE_R = 2.0`).
- `exit_time_stop_bars = 8` (R3 commit; matches `STAGNATION_BARS = 8`).
- `entry_kind = MARKET_NEXT_BAR_OPEN` (default; preserves R3 baseline exit-only structural change).
- All other H0 defaults unchanged.

**Expected R-window numbers (Phase 2l locked):**

| Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   |
|---------|-------:|-------:|--------:|------:|--------:|--------:|
| BTCUSDT |     33 | 42.42% | −0.240  | 0.560 | −1.77%  | −2.16%  |
| ETHUSDT |     33 | 33.33% | −0.351  | 0.474 | −2.61%  | −3.65%  |

**Expected V-window numbers (Phase 2s locked):**

| Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   |
|---------|-------:|-------:|--------:|------:|--------:|--------:|
| BTCUSDT |      8 | 25.00% | −0.287  | 0.580 | −0.51%  | −1.06%  |
| ETHUSDT |     14 | 42.86% | −0.093  | 0.824 | −0.29%  | −0.94%  |

**Validation requirement.** All R3 control numbers reproduce **bit-for-bit**. Same blocking discipline as §2.1 H0 control.

### 2.3 R2 + R3 candidate

**Configuration.** R2 sub-parameters per Phase 2u memo §F (committed singularly):

- `setup_predicate_kind = RANGE_BASED` (H0 default; R2 does not touch setup).
- `setup_size = 8`.
- `bias_slope_strength_threshold = 0.0` (H0 default; R2 does not touch bias).
- `exit_kind = FIXED_R_TIME_STOP` (R3 locked exit baseline).
- `exit_r_target = 2.0` (R3 locked).
- `exit_time_stop_bars = 8` (R3 locked; counted from fill bar per Phase 2u §F.3 / §G).
- `entry_kind = PULLBACK_RETEST` (R2 commit; the single-axis structural change).
- Pullback level: `setup.setup_high` for LONG, `setup.setup_low` for SHORT (Phase 2u §F.1; hard-coded in implementation, not a config field).
- Confirmation rule: `close_t > structural_stop_level` for LONG, `close_t < structural_stop_level` for SHORT (Phase 2u §F.2; hard-coded).
- Validity window: `R2_VALIDITY_WINDOW_BARS = 8` (Phase 2u §F.3; hard-coded).
- Fill model: next-bar-open after confirmation (Phase 2u §F.4; hard-coded as the default for `EntryKind.PULLBACK_RETEST`).
- All other H0 defaults unchanged.

**Expected R-window numbers.** **No expected numbers committed in Phase 2v.** R2 has not been run; pre-committing predicted values would conflict with §11.3.5 no-post-hoc-loosening discipline. The candidate's R-window output is observed once at execution time and evaluated against §10.3 thresholds without adjustment.

The Phase 2u §K mechanism predictions (M1: Δexp_R3 ≥ +0.10 R BTC; M2: lower BTC stop-exit fraction; M3: smaller mean R-distance) are **not** §10.3 thresholds — they are mechanism-validation diagnostics. The framework verdict is governed by §10.3 unchanged; the mechanism verdict is a separate report cut.

**Validation requirement.** No pre-committed numeric expectation. The implementation must produce reproducible R2 output (deterministic at fixed inputs; same seeds; same dataset version); rerunning the same run inventory must produce bit-identical results.

---

## 3. Backtest requirements

### 3.1 Implementation checklist

The future execution phase implements the surface described descriptively in Phase 2u §J. The exact checklist:

#### 3.1.1 Configuration surface

- [ ] Add `EntryKind` enum to `src/prometheus/strategy/v1_breakout/variant_config.py` with values `MARKET_NEXT_BAR_OPEN` (default; preserves H0 / R3 / R1a / R1b-narrow bit-for-bit) and `PULLBACK_RETEST` (R2 opt-in).
- [ ] Add `entry_kind: EntryKind = EntryKind.MARKET_NEXT_BAR_OPEN` field to `V1BreakoutConfig`.
- [ ] Hard-code R2 sub-parameters as module constants:
  - `R2_VALIDITY_WINDOW_BARS = 8` (with comment referencing `SETUP_SIZE = 8` and `exit_time_stop_bars = 8` co-anchors).
  - Pullback-level computation hard-coded as `candidate.pullback_level = setup.setup_high if direction == LONG else setup.setup_low` at registration.
  - Confirmation-rule predicate hard-coded as `close_t > structural_stop_level` (LONG) / `<` (SHORT).
  - Fill-model hard-coded as `fill_price = open_(t+1)` (for `EntryKind.PULLBACK_RETEST`) at fill-bar.
- [ ] **Do NOT add config fields for any of the four R2 sub-parameters.** The values are committed singularly; exposing them as config would invite future drift toward sweeps.

#### 3.1.2 New module: `entry_lifecycle.py`

- [ ] Create `src/prometheus/strategy/v1_breakout/entry_lifecycle.py`.
- [ ] Define `PendingCandidate` frozen dataclass with fields per Phase 2u §J.2.
- [ ] Define `evaluate_pending_candidate(candidate, bar_t, bias_t, opposite_signal_t) -> PendingEvaluation` returning one of `{CONTINUE, CANCEL_BIAS_FLIP, CANCEL_OPPOSITE_SIGNAL, CANCEL_STRUCTURAL_INVALIDATION, READY_TO_FILL}` *(per Phase 2v Gate 2 amended §E.2)*.
- [ ] Define `evaluate_fill_at_next_bar_open(candidate, fill_bar_open) -> FillEvaluation` returning `{FILL(fill_price), CANCEL_STOP_DISTANCE_AT_FILL}`.
- [ ] **Cancellation precedence at bar t close (5-step; first-match wins per Phase 2v Gate 2 amended §E.2):** 1. BIAS_FLIP → 2. OPPOSITE_SIGNAL → 3. STRUCTURAL_INVALIDATION → 4. TOUCH+CONFIRMATION → 5. CONTINUE.
- [ ] STRUCTURAL_INVALIDATION predicate: `close_t <= candidate.structural_stop_level` (LONG); `close_t >= candidate.structural_stop_level` (SHORT). Fires regardless of touch state.
- [ ] Same-bar resolution of touch + confirmation per Phase 2u §B / §E. Note: confirmation predicate at step 4 is mechanically redundant given step 3 precedence; retained for symmetry.

#### 3.1.3 `StrategySession` integration

- [ ] Add `_pending_candidate: Optional[PendingCandidate]` field initialized to None.
- [ ] Per-bar dispatch:
  - If `entry_kind == MARKET_NEXT_BAR_OPEN`: existing H0/R3 pipeline runs unchanged; **no behavior change for default config**.
  - If `entry_kind == PULLBACK_RETEST`: registration on signal-bar close; `_pending_candidate` evaluation on subsequent bars; fill at next-bar open after READY_TO_FILL; clear `_pending_candidate` on FILL / EXPIRE / CANCEL.
- [ ] Pending uniqueness rule per Phase 2u §E.5: same-direction new signal during pending → drop; opposite-direction new signal → cancel pending then evaluate new.

#### 3.1.4 Backtest engine integration

- [ ] Per-bar evaluation order updated to handle PendingCandidate state alongside existing trade-state (open / closed) handling.
- [ ] Fill-bar handling: when a candidate becomes READY_TO_FILL at bar t close, the engine schedules a fill at bar t+1 open. The fill is recorded with `fill_price = open_(t+1)` and `fill_stop_distance = abs(fill_price − candidate.structural_stop_level)`. If `fill_stop_distance` is outside [0.60, 1.80] × `candidate.atr_at_signal`, the fill is cancelled (no trade).
- [ ] Fee/slippage applied at fill per existing taker-fee path.
- [ ] R3 exit machinery counts from fill bar (R3-consistent interpretation per Phase 2u §G).

#### 3.1.5 Diagnostics funnel

- [ ] Extend `run_signal_funnel` in `diagnostics.py` with new buckets per Phase 2u §J.4 (as amended by Phase 2v Gate 2):
  - `registered_candidates`.
  - `expired_candidates_no_pullback`.
  - `expired_candidates_bias_flip`.
  - `expired_candidates_opposite_signal`.
  - `expired_candidates_structural_invalidation`. *(NEW per Phase 2v Gate 2 amendment.)*
  - `expired_candidates_stop_distance_at_fill`.
  - `trades_filled_R2`.
- [ ] For `entry_kind == MARKET_NEXT_BAR_OPEN`, the new buckets are zero / not populated (preserves H0 / R3 / R1a / R1b-narrow funnel attribution unchanged).
- [ ] For `entry_kind == PULLBACK_RETEST`, the existing `entry_intents` and `trades_filled` buckets remain populated (`registered_candidates` ≡ `entry_intents` for the R2 path; `trades_filled_R2` ≡ `trades_filled`); the new buckets supply the cancellation decomposition.

#### 3.1.6 Per-trade record schema

- [ ] Each filled R2 trade record includes:
  - `registration_bar_index` (= candidate's B).
  - `fill_bar_index` (= t + 1 where t is the touch + confirmation bar).
  - `time_to_fill_bars` (= `fill_bar_index − registration_bar_index − 1`; 0–7 inclusive).
  - `pullback_level_at_registration`.
  - `structural_stop_level_at_registration`.
  - `atr_at_signal`.
  - `fill_price` (= `open_(t+1)`).
  - `r_distance` (= `abs(fill_price − structural_stop_level) / atr_at_signal`).
  - `cancellation_reason` field on cancelled / expired records (one of `BIAS_FLIP`, `OPPOSITE_SIGNAL`, `STRUCTURAL_INVALIDATION`, `STOP_DISTANCE_AT_FILL`, `VALIDITY_WINDOW_ELAPSED`, or `null` for filled trades). *(STRUCTURAL_INVALIDATION added per Phase 2v Gate 2 amendment.)*

#### 3.1.7 Tests

- [ ] H0 baseline preservation tests:
  - `test_default_entry_kind_is_market_next_bar_open` — `V1BreakoutConfig().entry_kind == EntryKind.MARKET_NEXT_BAR_OPEN`.
  - `test_market_next_bar_open_preserves_H0_baseline_R_window` — full H0 run on R-window reproduces locked Phase 2e numbers bit-for-bit.
  - `test_market_next_bar_open_preserves_R3_baseline_R_window` — full R3 run on R-window reproduces locked Phase 2l numbers bit-for-bit.
- [ ] R2 registration tests:
  - `test_R2_registers_candidate_on_signal_bar_close` — bar with passing trigger + bias + stop-distance pre-filter under `entry_kind = PULLBACK_RETEST` produces a PendingCandidate with frozen fields matching expected values.
  - `test_R2_does_not_register_during_warmup` — bias-NEUTRAL or ATR-NaN at bar B → no candidate.
- [ ] R2 touch + confirmation tests (per Phase 2v Gate 2 amended §E.2 5-step precedence):
  - `test_R2_long_touch_and_confirm_at_bar_t` — bar t with `low_t ≤ pullback_level AND close_t > structural_stop_level` produces READY_TO_FILL.
  - `test_R2_long_close_violates_stop_triggers_structural_invalidation` *(replaces the pre-amendment `test_R2_long_touch_without_confirm_continues_pending`)* — bar t with `low_t ≤ pullback_level AND close_t ≤ structural_stop_level` → CANCEL(STRUCTURAL_INVALIDATION) at step 3 (touch+confirmation at step 4 is never reached).
  - `test_R2_long_confirm_without_touch_continues_pending` — bar t with `low_t > pullback_level AND close_t > structural_stop_level` continues pending (step 3 does not fire; step 4 has no touch; step 5 CONTINUE).
  - SHORT-side mirrored versions.
- [ ] R2 cancellation tests:
  - `test_R2_bias_flip_cancels_candidate` — bias change during pending → CANCEL(BIAS_FLIP).
  - `test_R2_opposite_signal_cancels_candidate` — opposite-direction trigger during pending → CANCEL(OPPOSITE_SIGNAL).
  - `test_R2_structural_invalidation_long` *(NEW per Phase 2v Gate 2 amendment)* — non-touch bar with `low_t > pullback_level AND close_t ≤ structural_stop_level` (LONG) → CANCEL(STRUCTURAL_INVALIDATION).
  - `test_R2_structural_invalidation_short` *(NEW per Phase 2v Gate 2 amendment)* — non-touch bar with `high_t < pullback_level AND close_t ≥ structural_stop_level` (SHORT) → CANCEL(STRUCTURAL_INVALIDATION).
  - `test_R2_structural_invalidation_precedence_after_opposite_signal` *(NEW per Phase 2v Gate 2 amendment)* — bar where opposite-signal AND structural-violation both fire → CANCEL(OPPOSITE_SIGNAL) wins (precedence position 2 < 3).
  - `test_R2_structural_invalidation_precedence_before_touch_confirmation` *(NEW per Phase 2v Gate 2 amendment)* — touch bar with `low_t ≤ pullback_level AND close_t ≤ structural_stop_level` → CANCEL(STRUCTURAL_INVALIDATION) wins at step 3; touch+confirmation at step 4 is never reached.
  - `test_R2_cancellation_precedence` *(updated)* — covers the full 4-step ordering: bias-flip > opposite-signal > structural-invalidation > touch+confirmation. Bar t with bias-flip AND structural-violation AND touch+confirmation simultaneously → BIAS_FLIP wins (first-match precedence).
- [ ] R2 fill-time stop-distance test:
  - `test_R2_fill_rejected_if_stop_distance_below_floor` — fill price producing `stop_distance < 0.60 × atr_at_signal` → CANCEL(STOP_DISTANCE_AT_FILL).
  - `test_R2_fill_rejected_if_stop_distance_above_ceiling` — fill price producing `stop_distance > 1.80 × atr_at_signal` → CANCEL(STOP_DISTANCE_AT_FILL).
- [ ] R2 expiry test:
  - `test_R2_expires_at_validity_window_close` — candidate with no fill or cancel by `B + 8` close → EXPIRE(VALIDITY_WINDOW_ELAPSED).
- [ ] R2 pending uniqueness tests:
  - `test_R2_drops_same_direction_signal_during_pending` — second LONG signal while LONG pending → dropped silently.
  - `test_R2_opposite_signal_cancels_then_registers` — SHORT signal while LONG pending → CANCEL(OPPOSITE_SIGNAL) of LONG; SHORT registered at same bar close.
- [ ] R2 R3 time-stop interaction test:
  - `test_R2_R3_time_stop_counts_from_fill_bar` — candidate filling at bar `B + k` for `k ∈ {1, 2, ..., 8}` reaches R3 time-stop at `fill_bar + 8 = B + k + 8`.
- [ ] Implementation-bug tests:
  - `test_R2_no_trailing_breach_or_stagnation_exits` — every R2 + R3 trade closes with one of `{STOP, TAKE_PROFIT, TIME_STOP, END_OF_DATA}` (R3 exits unchanged).
  - `test_R2_protective_stop_at_frozen_level` — every filled R2 trade has its protective STOP_MARKET at `candidate.structural_stop_level`, not at a recomputed value.

Estimated test count: **33–53 new R2 unit tests** (per Phase 2v Gate 2 amendment: one removed, four added, one renamed, one updated; net +3–5 tests over the pre-amendment 30–50 estimate). Vs Phase 2s's 14 R1b-narrow tests, Phase 2m's 13 R1a tests. Larger surface reflects the larger state-machine implementation.

#### 3.1.8 Runner and analysis scripts

- [ ] Create `scripts/phase2w_R2_execution.py` (or whatever phase-name the operator approves) mirroring the Phase 2s `phase2s_R1b_narrow_execution.py` pattern. Variants: H0 / R3 / R2+R3. Windows: R / V / FULL. Knobs: `--slippage`, `--stop-trigger`, `--fill-model` (NEW: `next-bar-open` (default) | `limit-at-pullback`).
- [ ] Create `scripts/_phase2w_R2_analysis.py` mirroring the Phase 2s `_phase2s_R1b_analysis.py` pattern. Computes: official deltas-vs-H0 (governing); supplemental deltas-vs-R3 (mechanism-validation); GAP-036 5-fold consistency; mandatory diagnostics §P.1–P.14.

### 3.2 Validation requirements (baseline reproduction)

#### 3.2.1 Pre-runner gates

Before any R2 + R3 run is executed, the following pre-runner gates must pass (mirroring Phase 2s §2.2):

- [ ] `ruff check .` clean.
- [ ] `ruff format --check .` clean.
- [ ] `mypy` clean on default scope (source files; scripts out of mypy default scope per project precedent).
- [ ] `pytest` clean. Test count = current count (Phase 2s baseline 431) + 33–53 new R2 tests *(per Phase 2v Gate 2 amended §3.1.7)* = **expected ~464–484 tests passing**. Any failing test blocks execution-phase progression.

#### 3.2.2 Control reproduction

- [ ] Run #1 (H0 / R / MED / MARK) reproduces Phase 2e baseline numbers per §2.1 bit-for-bit.
- [ ] Run #2 (R3 / R / MED / MARK) reproduces Phase 2l baseline numbers per §2.2 bit-for-bit.
- [ ] Run #4 (H0 / V / MED / MARK) reproduces Phase 2s V-window numbers per §2.1 bit-for-bit.
- [ ] Run #5 (R3 / V / MED / MARK) reproduces Phase 2s V-window numbers per §2.2 bit-for-bit.

Any deviation in control reproduction is a **hard block**. The execution phase does not proceed to §10.3 evaluation until all four control reproductions are bit-for-bit.

#### 3.2.3 Implementation-bug check

- [ ] Run #3 (R2 + R3 / R / MED / MARK) trade log: zero TRAILING_BREACH and zero STAGNATION exits (R3 exit machinery preserved verbatim).
- [ ] Run #3 trade log: every filled trade has its protective STOP_MARKET placed at `candidate.structural_stop_level` (frozen at registration).
- [ ] Run #3 funnel: `registered_candidates = expired_candidates_no_pullback + expired_candidates_bias_flip + expired_candidates_opposite_signal + expired_candidates_structural_invalidation + expired_candidates_stop_distance_at_fill + trades_filled_R2` *(amended accounting identity per Phase 2v Gate 2; five cancellation buckets + one fill bucket)*.
- [ ] Run #3 trade log: every filled trade has `time_to_fill_bars ∈ {0, 1, 2, ..., 7}` (validity window respected).
- [ ] Run #3 trade log: for every filled R2 trade, `r_distance = abs(fill_price − structural_stop_level) / atr_at_signal ∈ [0.60, 1.80]` (fill-time stop-distance filter respected).

Any failure in these checks is a **hard block** before §10.3 evaluation.

#### 3.2.4 Determinism

- [ ] Run #3 produces bit-identical results when re-run with the same inputs and seed (deterministic backtest discipline).
- [ ] Multi-run dispatch order does not affect results (all runs are stateless w.r.t. each other).

---

## 4. Diagnostics plan

The execution phase must compute and report each of P.1–P.14 from Phase 2u §P. This section maps each diagnostic to its exact computation and reporting structure.

### 4.1 P.1 — Fill rate

**Computation.** Per symbol, on R-window run #3:

- `registered_candidates` (count of PendingCandidates registered).
- `expired_candidates_no_pullback`, `expired_candidates_bias_flip`, `expired_candidates_opposite_signal`, `expired_candidates_structural_invalidation`, `expired_candidates_stop_distance_at_fill` (counts) *(STRUCTURAL_INVALIDATION bucket added per Phase 2v Gate 2 amendment)*.
- `trades_filled_R2` (count).
- `fill_rate = trades_filled_R2 / registered_candidates`.

**Reporting structure.** A **6-row × 2-column** table *(per Phase 2v Gate 2 amendment; 5 cancellation reasons + filled)* — rows: NO_PULLBACK, BIAS_FLIP, OPPOSITE_SIGNAL, STRUCTURAL_INVALIDATION, STOP_DISTANCE_AT_FILL, FILLED; columns: BTC count, ETH count. Final row: fill rate as a percentage. Repeated for V-window (run #6) if R promotes.

### 4.2 P.2 — Pullback-touch distribution

**Computation.** For each filled R2 candidate on run #3, record `time_to_fill_bars = fill_bar_index − registration_bar_index − 1`. Bin into 8 cells (0, 1, 2, ..., 7).

**Reporting structure.** Per-symbol histogram (8 cells); mean / median / quartiles. Same diagnostic restated as P.11 (cross-referenced).

### 4.3 P.3 — Stop-distance reduction

**Computation.** For each filled R2 candidate on run #3, compute the stop-distance ratio:

```
stop_distance_ratio = |R2_fill_price − structural_stop_level| / |R3_would_have_entered_at − structural_stop_level|
```

Where `R3_would_have_entered_at = open_(B+1)` (the price R3 would have entered at on the same signal). This requires the engine to record `open_(B+1)` for every R2 candidate at registration (so it can be compared against the actual fill_price downstream).

**Reporting structure.** Per-symbol mean / median / quartiles. Histogram of ratio values.

**Pass criterion (mechanical).** Mean ratio < 1.0 (R2 enters at smaller stop-distance than R3 would). If ratio ≈ 1.0, the implementation is mechanically active but functionally near-equivalent to R3.

### 4.4 P.4 — Stop-exit fraction comparison

**Computation.** Per symbol, on R-window:

```
stop_exit_fraction(variant) = stop_exits(variant) / total_exits(variant)
```

Computed for H0 (run #1), R3 (run #2), R2 + R3 (run #3).

**Reporting structure.** Per-symbol 3-row table (H0, R3, R2+R3); columns: stop_exits, total_exits, fraction.

**M2 mechanism prediction:** R2+R3 BTC fraction strictly less than R3 BTC fraction.

### 4.5 P.5 — Intersection-trade comparison vs R3 (strongest mechanism-validation diagnostic)

**Computation.** Define the intersection set:

- `Intersection = {bars B : H0 trigger + bias + stop-distance pre-filter passes at bar B}` (this is exactly the set of bars where R3 alone would have entered; same set R2 sees as eligible signals for registration).

For each bar in Intersection:

- If R2 + R3 filled this signal (i.e., the candidate satisfied touch + confirmation + fill-time stop-distance): record R2's fill_price and R2's actual trade outcome (R-multiple).
- If R3 alone was run on the same bar: record R3's entry_price (= open_(B+1)) and R3's actual trade outcome.

Compute per-trade R-multiple difference for the intersection's filled-by-both subset:

```
intersection_filled = {B ∈ Intersection : R2 + R3 filled AND R3 alone filled (always true for R3 alone)}
delta_expR_per_trade(B) = R2_R-multiple(B) − R3_R-multiple(B)
mean_delta_expR_intersection = mean over intersection_filled of delta_expR_per_trade(B)
```

**Reporting structure.** Per-symbol single number (mean Δexp on intersection). Per-symbol quartile distribution of `delta_expR_per_trade(B)`. Per-direction (LONG / SHORT) breakdown.

**M1 mechanism prediction:** `mean_delta_expR_intersection ≥ +0.10 R` on BTC.

### 4.6 P.6 — Fill-model sensitivity

**Computation.** Run #10 is R2 + R3 on R / MED / MARK with **limit-at-pullback intrabar** fill model. Compute the same headline metrics (Trades, WR, expR, PF, netPct, maxDD) and compare to run #3 (next-bar-open after confirmation; the committed fill model).

The limit-at-pullback intrabar fill model:

- Detects touch on bar t (low_t ≤ pullback_level for LONG); confirmation on the same bar (close_t > structural_stop_level).
- Fills at exactly `pullback_level` on bar t (intra-bar fill; assumes resting limit-order fills perfectly at the level).
- Same fee structure as run #3 (taker fee 0.0005; no maker-fee path).
- Slippage model: zero (limit fills are makers; this is the most-aggressive realism assumption).

**Diagnostic-only — never a production / default config path (Phase 2v Gate 2 clarification).** The limit-at-pullback intrabar model exists solely as a **runner-script `--fill-model` argument** for §P.6 sensitivity reporting. It must **not** be exposed as a `V1BreakoutConfig` field (e.g., as an `EntryFillModel` enum). The production code path for `EntryKind.PULLBACK_RETEST` always uses the §F.4-committed next-bar-open-after-confirmation fill model. No R2 trade record produced under run #10 is eligible for §10.3 evaluation; run #3 alone drives the framework verdict. A future operator-approved phase that wants to test alternative fill models must introduce a new candidate (e.g., R2-limit) with its own non-fitting rationale, full §F-style commitment, and full Phase 2i §1.7 binding-test re-evaluation. It cannot be added as a config tweak under R2.

**Reporting structure.** Side-by-side comparison table for both symbols. Computed divergence: `Δexp(committed − sensitivity)`, `ΔPF`, `Δ|maxDD|`.

**Pass criterion (interpretive, not §10.3).** Small divergence (`|Δexp| < 0.05` per trade) → §F.4 commitment is well-justified. Large divergence (`|Δexp| > 0.10`) → fill-model-sensitivity flag for backtest-vs-live realism concerns. Either way, the §10.3 verdict is governed by run #3 (committed fill model); run #10 informs interpretation only.

### 4.7 P.7 — Long/short asymmetry

**Computation.** Per symbol on R-window, decompose run #1 (H0), run #2 (R3), run #3 (R2+R3):

- Per direction: count, WR, expR, PF.

**Reporting structure.** Per-symbol 3-variant × 2-direction table (6 cells per symbol). Direction-asymmetry comparison: Δ(LONG expR vs SHORT expR) per variant.

### 4.8 P.8 — Per-fold consistency (GAP-036)

**Computation.** 5 rolling folds per GAP-20260424-036 convention (fold-1 partial-train; all test windows inside R = 2022-01-01 → 2025-01-01).

For each fold: compute n_trades, expR for each of H0, R3, R2+R3 per symbol.

Per-fold deltas:
- `delta_expR_vs_H0_fold_i = R2+R3 expR(fold i) − H0 expR(fold i)`.
- `delta_expR_vs_R3_fold_i = R2+R3 expR(fold i) − R3 expR(fold i)`.

**Reporting structure.** Per-symbol 5-fold × 3-variant table (15 cells per symbol). Fold-wins count: `R2+R3 vs H0 wins / 5` and `R2+R3 vs R3 wins / 5`.

**Sample-size caveat (mandatory in report).** If any per-fold count is < 3, the fold-level expR is uninterpretable; the framework verdict on aggregate is governing.

### 4.9 P.9 — Per-regime expR

**Computation.** Realized 1h-vol terciles (trailing 1000 1h-bar Wilder ATR(20), 33/67 splits per Phase 2l / 2m / 2s convention). Per regime per symbol per variant: count, expR, PF, WR.

**Reporting structure.** Per-symbol 3-regime × 3-variant table (9 cells per symbol).

### 4.10 P.10 — R-distance distribution

**Computation.** For each R2+R3 filled trade (run #3), compute `r_distance = abs(fill_price − structural_stop_level) / atr_at_signal`. For each R3 filled trade (run #2), compute `r_distance = abs(open_(B+1) − structural_stop_level) / atr_at_signal`.

**Reporting structure.** Per-symbol mean / median / quartiles for R3 and R2+R3. Histogram comparison (overlay).

**M3 mechanism prediction:** R2+R3 mean r_distance strictly less than R3 mean r_distance on BTC. Mechanically guaranteed if implementation is correct.

### 4.11 P.11 — Time-to-fill distribution

Same as P.2; cross-referenced for clarity.

### 4.12 P.12 — MFE / MAE distribution at fill

**Computation.** For each R2+R3 filled trade, MFE and MAE measured *from R2 fill_price* (not from signal-bar close). For each R3 filled trade, MFE / MAE from R3 entry_price.

**Reporting structure.** Per-symbol mean / median / quartiles for R3 and R2+R3.

**Failure-mode signature.** R2+R3 mean MFE materially smaller than R3 mean MFE → R2 is filtering out the strongest moves (§L.1 failure mode).

### 4.13 P.13 — Mark-price vs trade-price stop-trigger sensitivity (GAP-032)

**Computation.** Run #9 is R2+R3 on R / MED / TRADE_PRICE. Compare headline metrics to run #3 (R2+R3 on R / MED / MARK_PRICE). Report bit-identicality OR divergence.

**Reporting structure.** Side-by-side comparison table; gap-through-stops count.

**Pass criterion.** Both stop-trigger sources must clear §10.3 framework.

### 4.14 P.14 — Implementation-bug check

Per §3.2.3 above. Reported as a separate one-page bug-check summary.

### 4.15 Reporting structure (overall)

The execution-phase comparison report (mirroring Phase 2s comparison report structure) must contain:

- §1: Plain-English summary.
- §2: What was built and what was run (code surface; quality gates; run inventory; H0 + R3 control bit-for-bit reproducibility).
- §3: R-window headline comparison (3-variant × 2-symbol headline table).
- §4: Official ranking (H0 anchor — Phase 2f §10.3 / §10.4) with explicit §10.3.a / §10.3.c / disqualification-floor / §11.4 evaluations.
- §5: Supplemental ranking (R3 anchor — descriptive only) including §P.5 intersection-trade comparison.
- §6: Per-fold consistency (§P.8).
- §7: Mandatory common diagnostics: per-regime (§P.9), MFE/MAE (§P.12), long/short (§P.7), implementation-bug check (§P.14).
- §8: R2-specific diagnostics: fill rate (§P.1), pullback-touch (§P.2 / P.11), stop-distance reduction (§P.3), stop-exit fraction (§P.4), intersection-trade (§P.5), R-distance (§P.10).
- §9: V-window confirmation (only if R promotes).
- §10: Slippage sensitivity (§11.6; runs #7, #8).
- §11: Stop-trigger sensitivity (§P.13; run #9).
- §12: Fill-model sensitivity (§P.6; run #10).
- §13: PASS / FAIL / HOLD classification.
- §14: What the verdict does NOT claim (mirroring Phase 2s §13).
- §15: Threshold preservation (§11.3.5).
- §16: Wave / phase preservation.
- §17: Safety posture.

Total expected report length: comparable to or slightly longer than Phase 2s's 16 sections / ~440 lines.

---

## 5. Gate criteria

### 5.1 §10.3 thresholds (governing — applied vs H0 anchor)

Applied unchanged per Phase 2f §11.3.5 (no post-hoc loosening). Same thresholds as Phases 2g / 2l / 2m / 2s.

#### 5.1.1 §10.3 disqualification floor

R2 + R3 fails framework if **any** of:

- Δexp_R2+R3 vs H0 < 0 on BTC OR ETH (worse expectancy than H0 on either symbol).
- ΔPF_R2+R3 vs H0 < 0 on BTC OR ETH (worse profit factor than H0 on either symbol).
- |maxDD| ratio (R2+R3 / H0) > 1.5× on BTC OR ETH (drawdown > 1.5× worse).

### 5.1.2 §10.3.a magnitude path

R2 + R3 PROMOTES if **both**:

- Δexp_R2+R3 vs H0 ≥ +0.10 R on BTC.
- ΔPF_R2+R3 vs H0 ≥ +0.05 on BTC.

(§11.4 ETH-as-comparison: ETH must not catastrophically fail; ETH §10.3.a clearance is desirable but not required.)

### 5.1.3 §10.3.b rising-trade-count path — mechanically unavailable

§10.3.b requires Δn ≥ +50%. R2 reduces trade count by design (signals that don't pullback expire unfilled). Δn is expected negative; §10.3.b path is not applicable.

### 5.1.4 §10.3.c strict-dominance path

R2 + R3 PROMOTES if **all**:

- Δexp_R2+R3 vs H0 > 0 on BTC.
- ΔPF_R2+R3 vs H0 > 0 on BTC.
- Δ|maxDD| (R2+R3 − H0) ≤ 0 on BTC (drawdown not worse).

(Same fallback path R3 took in Phase 2l and R1a+R3 took on BTC in Phase 2m.)

#### 5.1.5 §10.4 hard reject — mechanically inapplicable

§10.4 fires only when Δn > 0 AND expR / PF worsen. R2 has Δn < 0; §10.4 does not apply.

#### 5.1.6 §11.4 ETH-as-comparison

R2 + R3 must **not trigger §10.3 disqualification on ETH**. ETH §10.3.a or §10.3.c clearance is desirable but not required. ETH catastrophic failure (e.g., §10.3 disqualification floor on either expR or PF or |maxDD|) blocks the BTC PROMOTE.

#### 5.1.7 §11.6 cost-sensitivity

R2 + R3 must clear §10.3 (no disqualification floor triggered) at HIGH slippage. Run #8 governs this.

#### 5.1.8 §11.3 V-window

If R-window PROMOTES, V-window run (run #6) is executed. V-window failure does not retroactively change R-window classification but does end the candidate's wave per Phase 2s precedent.

### 5.2 Mechanism validation (M1, M2, M3 — supplemental, applied vs R3 anchor)

These are **separate from the §10.3 framework verdict**. They are diagnostic cuts that interpret the framework verdict.

#### 5.2.1 M1 — Per-trade expectancy improvement

**Pass.** `mean_delta_expR_intersection ≥ +0.10 R` on BTC (per §P.5 intersection-trade comparison).

**Fail.** `mean_delta_expR_intersection < +0.05 R` on BTC. R2's improvement (if any) under the framework verdict is from selection (trade-count reduction); the R1b-narrow pattern is reproducing.

**Indeterminate.** `+0.05 R ≤ mean_delta_expR_intersection < +0.10 R`. Mechanism partially supported; magnitude smaller than §10.3.a's anchor.

#### 5.2.2 M2 — Stop-out fraction reduction

**Pass.** `stop_exit_fraction(R2+R3, BTC) < stop_exit_fraction(R3, BTC)` strictly (per §P.4).

**Fail.** `stop_exit_fraction(R2+R3, BTC) ≥ stop_exit_fraction(R3, BTC)`. R2 does not address the BTC stop-out failure mode the way the thesis predicted.

#### 5.2.3 M3 — R-distance reduction

**Pass.** `mean_r_distance(R2+R3, BTC) < mean_r_distance(R3, BTC)` strictly (per §P.10).

**Fail.** `mean_r_distance(R2+R3, BTC) ≥ mean_r_distance(R3, BTC)`. **Implementation bug suspected** — mechanically the pullback-retest fill should produce strictly smaller R-distance unless the implementation is broken. M3 failure blocks §10.3 evaluation pending implementation review.

### 5.3 Combined verdict classification

| §10.3 framework | M1 mechanism | M2 mechanism | M3 mechanism | Combined verdict                                        |
|-----------------|--------------|--------------|--------------|---------------------------------------------------------|
| PROMOTE (§10.3.a or §10.3.c on BTC; §11.4 ETH OK) | Pass         | Pass         | Pass         | **PROMOTE — MECHANISM VALIDATED** (strongest outcome)   |
| PROMOTE         | Indeterminate| Pass         | Pass         | **PROMOTE — MECHANISM PARTIALLY SUPPORTED**             |
| PROMOTE         | Fail         | (any)        | Pass         | **PROMOTE — MECHANISM NOT VALIDATED** (R1b-narrow pattern; framework verdict stands; absolute-edge interpretation weakened) |
| PROMOTE         | (any)        | (any)        | Fail         | **HOLD pending implementation review** (M3 mechanical failure → bug suspected)                  |
| §10.3 disqualification on BTC | (any)        | (any)        | (any)        | **FAILED** (framework rejects)                          |
| §10.3 PROMOTE on R; V-window failure (n ≥ 3 trades, §10.3 disqualification on V) | (any)        | (any)        | (any)        | **PROMOTE on R; INDETERMINATE on V; wave ends**         |
| §10.3 PROMOTE on R; V-window n < 3 trades (uninterpretable on n=1) | (any)        | (any)        | (any)        | **PROMOTE on R; V-window uninterpretable; wave ends**   |
| §10.3 disqualification on ETH (catastrophic) per §11.4 | (any)        | (any)        | (any)        | **FAILED** (§11.4 blocks BTC PROMOTE)                   |
| §10.3 disqualification at HIGH slippage (run #8) per §11.6 | (any)        | (any)        | (any)        | **FAILED** (cost-sensitivity blocks)                    |

### 5.4 Failure conditions — enumerated

The candidate FAILS framework if any of:

1. H0 control (run #1) does not reproduce Phase 2e numbers bit-for-bit. **Hard block before §10.3 evaluation.**
2. R3 control (run #2) does not reproduce Phase 2l numbers bit-for-bit. **Hard block.**
3. R2 + R3 (run #3) trade log shows TRAILING_BREACH or STAGNATION exits. **Hard block.**
4. R2 + R3 (run #3) accounting identity (§3.2.3) fails. **Hard block.**
5. M3 mechanism prediction fails (R2+R3 R-distance ≥ R3 R-distance). **Hard block — bug suspected.**
6. R2 + R3 R-window §10.3 disqualification floor triggered on BTC.
7. R2 + R3 R-window §10.3 disqualification floor triggered on ETH (§11.4 catastrophic).
8. R2 + R3 R-window does not clear §10.3.a OR §10.3.c on BTC.
9. R2 + R3 R-window §11.6 HIGH slippage triggers §10.3 disqualification.

Failure conditions 1–5 are hard blocks (implementation-correctness gates); failure conditions 6–9 are framework rejections.

### 5.5 What the verdict does NOT claim

(Mirroring Phase 2s §13.)

- A PROMOTE verdict is not a live-readiness claim. R-window aggregate expR is expected to remain negative for all variants (consistent with prior phases).
- A PROMOTE verdict does not replace R3 as the baseline-of-record. Phase 2p committed R3 as baseline-of-record; R2 + R3 PROMOTING is grounds for the operator to reconsider in a separate phase, not for the execution phase to silently reassign.
- A MECHANISM-VALIDATED verdict (M1/M2/M3 all pass) does not authorize paper/shadow / Phase 4 / live work. Operator deferrals stand.
- A MECHANISM-NOT-VALIDATED PROMOTE (R1b-narrow pattern) confirms two filter-axis paths AND one entry-mechanic path produced the same outcome shape — informative, but not actionable without operator policy review.

---

## 6. Risk checklist

### 6.1 Implementation risks

| Risk                                                                                                                                             | Mitigation                                                                                                                                                                     | Owner             |
|--------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| New `EntryKind` dispatch silently regresses H0 / R3 / R1a / R1b-narrow baseline behaviour.                                                       | Bit-for-bit baseline reproduction tests in §3.1.7 + §3.2.2. Hard block on any deviation.                                                                                       | Execution phase   |
| PendingCandidate state-machine has a cancellation-precedence bug.                                                                               | Explicit precedence test (`test_R2_cancellation_precedence`); precedence pinned in §3.1.2 / Phase 2u §E.2 (5-step ordering: BIAS_FLIP > OPPOSITE_SIGNAL > STRUCTURAL_INVALIDATION > TOUCH+CONFIRMATION > CONTINUE).                                                                    | Execution phase   |
| **STRUCTURAL_INVALIDATION precedence not enforced correctly** *(NEW per Phase 2v Gate 2 amendment)* — implementation either fires the new step 3 cancellation in the wrong order (e.g., after touch+confirmation), forgets to fire it on non-touch bars, or fails to detect close-violates-stop on same-bar touch+violation cases. | Dedicated tests `test_R2_structural_invalidation_long`, `test_R2_structural_invalidation_short`, `test_R2_structural_invalidation_precedence_after_opposite_signal`, `test_R2_structural_invalidation_precedence_before_touch_confirmation`. Funnel `expired_candidates_structural_invalidation` bucket presence is a runtime check; accounting identity (§3.2.3) catches missing bucket attribution. | Execution phase   |
| Same-bar resolution of touch + confirmation produces off-by-one in fill-bar-index.                                                              | Explicit single-bar resolution test; fill_bar_index = touch_bar + 1 enforced in code.                                                                                          | Execution phase   |
| No-look-ahead violation in conditional-fill path (e.g., recomputing ATR at fill bar).                                                            | `atr_at_signal` frozen at registration; explicit test that fill-time stop-distance uses `atr_at_signal`, not `atr_at_fill`. GAP-20260419-015 convention preserved.            | Execution phase   |
| Pending uniqueness rule inconsistent (e.g., same-direction signal not silently dropped).                                                         | Explicit pending-uniqueness tests; first-registered-wins enforced in code.                                                                                                     | Execution phase   |
| R3 time-stop horizon counts from signal bar instead of fill bar (lifecycle-consistent vs R3-consistent).                                          | Phase 2u §G commits "from fill bar" (R3-consistent); explicit test `test_R2_R3_time_stop_counts_from_fill_bar`.                                                              | Execution phase   |
| Diagnostics funnel accounting identity (registered = filled + cancellations) breaks.                                                             | §3.2.3 accounting-identity check; explicit funnel-attribution test.                                                                                                            | Execution phase   |

### 6.2 Fill-model sensitivity risk

The §F.4 commitment is the most-conservative fill model (next-bar-open after confirmation). The §P.6 sensitivity diagnostic compares against the most-aggressive option (limit-at-pullback intrabar with zero slippage and taker fees).

**Risk.** Large divergence between the two fill models would indicate that the candidate's behaviour is fill-model-sensitive — backtest-vs-live realism becomes a concern in any future paper/shadow phase.

**Mitigation.** Run #10 is mandatory. The divergence is reported in the comparison report §12. If divergence exceeds 0.10 R per trade on either symbol, the report records a fill-model-sensitivity flag for operator awareness; framework verdict (§10.3 on run #3) is unaffected.

**Acceptable range** (descriptive, not committed): `|Δexp(committed − sensitivity)| < 0.05 R per trade` on both symbols indicates the committed model is well-justified. `0.05 R ≤ |Δexp| < 0.10 R` is acceptable but flagged. `|Δexp| ≥ 0.10 R` is a material concern and should be raised in the operator Gate 2 review.

**Diagnostic-only — never a production / default config path (Phase 2v Gate 2 clarification).** The limit-at-pullback intrabar fill model is a **runner-script `--fill-model` argument**, not a `V1BreakoutConfig` field. The production code path for `EntryKind.PULLBACK_RETEST` always uses the §F.4-committed next-bar-open-after-confirmation model. The §10.3 framework verdict is governed exclusively by run #3 (committed fill model); run #10 informs interpretation only. A future operator-approved phase that wants to test alternative fill models must introduce a new candidate (e.g., R2-limit) with its own non-fitting rationale, full §F-style commitment, and full §1.7 binding-test re-evaluation. It cannot be added as a config tweak under R2. This boundary protects the §F.4 commitment from drifting into a tunable surface and preserves the discipline distinction between "committed value" and "configurable knob".

### 6.3 Sample-size risk

Per Phase 2t §8 and Phase 2s precedent, R2's trade count is expected to drop materially below H0's 33 trades per symbol on R-window. Plausible range: 10–25 trades per symbol on R; 0–10 trades per symbol on V (for BTC, V may have n=0 or n=1 — uninterpretable on n ≤ 2).

**Risks:**

- **Per-fold sample sizes may be uninterpretable.** GAP-036 5-rolling-fold convention requires meaningful per-fold n; some folds may have n < 3.
- **V-window BTC may have n ≤ 1.** Single-trade V-window evidence is uninterpretable (Phase 2s precedent).
- **§10.3.a magnitude path threshold (Δexp ≥ +0.10 R) is sensitive to single-trade flips at small n.**

**Mitigations:**

- Per-fold consistency reported descriptively (not as a §10.3 gate); sample-size caveats explicit in the report.
- V-window failure on n ≤ 2 records "INDETERMINATE; wave ends" per Phase 2s precedent; does not retroactively change R verdict.
- The §10.3.a magnitude threshold is preserved unchanged per §11.3.5; no adjustment for sample size.
- The §P.5 intersection-trade comparison is robust to selection effects (it compares the *same trades* under R2 and R3) but is itself sensitive to small intersection sizes; report the intersection-set size alongside the mean Δexp.

### 6.4 BTC-vs-ETH interpretation risk

Per Phase 2s precedent, the framework verdict and the R3-anchor mechanism reading can diverge:

- Framework verdict (governing, vs H0): may PROMOTE on §10.3.a or §10.3.c on BTC even when per-trade expectancy is unchanged.
- Mechanism reading (supplemental, vs R3): tests whether per-trade expectancy actually improved.

**Risk.** Operator may interpret "framework PROMOTE" as "absolute edge case supported" when in fact the improvement is trade-count-reduction-driven.

**Mitigation.** The §P.5 intersection-trade comparison is the strongest mechanism-validation cut and must be reported alongside the §10.3 framework verdict. The combined verdict classification table in §5.3 explicitly distinguishes "PROMOTE — MECHANISM VALIDATED" from "PROMOTE — MECHANISM NOT VALIDATED" (R1b-narrow pattern). The execution-phase comparison report §13 (PASS/FAIL/HOLD classification) must use this combined verdict, not the §10.3 verdict alone.

### 6.5 ETH-as-comparison interpretation risk

Per Phase 2m / 2o precedent, ETH has a pre-existing direction-asymmetric regime that filter-axis redesigns amplify. R2's entry-mechanic redesign is direction-symmetric; ETH's expected behaviour:

- ETH shorts: small-to-modest improvement (entering at better prices on bear-regime breakouts).
- ETH longs: small-to-modest improvement (R2's filter implicitly rejects breakouts that don't retest, which on a bearish-regime ETH window may filter out the worst longs).

**Risk.** ETH's direction-asymmetric regime may produce ETH-shorts §10.3.a-style improvement that is not present on BTC. This would make the candidate look "ETH-favorable" similar to R1a+R3.

**Mitigation.** §11.4 ETH-as-comparison rule applies: BTC must clear §10.3 for the candidate to PROMOTE; ETH catastrophic failure blocks but ETH success alone does not promote. The comparison report §4 explicitly evaluates BTC §10.3 paths and §11.4 ETH-as-comparison separately.

### 6.6 Backtester implementation surface risk

Per Phase 2u §J.6, the R2 implementation is the largest backtester change Phase 2 has done (~1430–2130 net lines). The state-machine plumbing (PendingCandidate registration, per-bar evaluation, fill-bar dispatch) introduces new failure surface that prior filter-axis redesigns did not have.

**Risks:**

- Pending-state leak across symbols (one symbol's PendingCandidate accidentally observed by another).
- Pending-state leak across phases (candidate not cleared on FILL).
- Iteration-order dependence (cancellation-check order or candidate-evaluation order changing results).

**Mitigations:**

- Per-symbol StrategySession isolation enforced by existing project structure (one StrategySession per symbol).
- Explicit `_pending_candidate = None` assignment on FILL / CANCEL / EXPIRE; tested via `test_R2_*_clears_pending_candidate`.
- Determinism test (§3.2.4) catches iteration-order dependence.
- Pre-runner gates (§3.2.1) enforce ruff / format / mypy / pytest cleanliness before any run.

### 6.7 Risks NOT mitigated by the execution phase

Some risks are operator-level concerns that the execution phase cannot resolve and should not attempt to:

- **Whether the absolute-edge gap on BTC is closeable from within the breakout family.** R2 is the third structural redesign tested; if it produces another mechanism-not-validated PROMOTE (R1b-narrow pattern), the operator must judge whether further structural work is justified or whether family-shift planning becomes the right path.
- **Whether paper/shadow / Phase 4 / live work should resume.** Operator policy deferrals; not the execution phase's place to lift.
- **Whether the operator's strategic interpretation of a MECHANISM-VALIDATED PROMOTE warrants policy change (e.g., lifting paper/shadow restriction).** Operator decision.

These are recorded in §6.7 explicitly so the execution-phase comparison report does not stray into operator-policy territory.

---

## Threshold preservation

Phase 2f §§ 10.3 / 10.4 / 11.3 / 11.4 / 11.6 thresholds applied unchanged. No post-hoc loosening per §11.3.5. Phase 2j §C.6 R1a sub-parameters preserved (R1a is not part of R2). Phase 2j §D.6 R3 sub-parameters preserved (R3 is the locked exit baseline). Phase 2r §F R1b-narrow sub-parameter preserved (R1b-narrow is not part of R2). Phase 2u §F R2 sub-parameters preserved singularly (no sweep authorized in execution phase). GAP-20260424-036 fold convention applied unchanged. GAP-20260424-031 / 032 / 033 carried forward unchanged. GAP-20260419-015 stop-distance reference-price convention applied unchanged. No new GAP entries introduced in Phase 2v. Phase 2i §1.7.3 project-level locks preserved.

---

## Wave / phase preservation

Phase 2g Wave-1 REJECT ALL preserved as historical evidence only. Phase 2l R3 PROMOTE preserved unchanged (R3 sub-parameters frozen; baseline-of-record per Phase 2p). Phase 2m R1a+R3 mixed-PROMOTE preserved unchanged (retained-for-future-hypothesis-planning per Phase 2p §D). Phase 2s R1b-narrow PROMOTE / PASS preserved unchanged. Phase 2u R2 spec-memo §F sub-parameters preserved singularly (no execution-phase modification). H0 anchor preserved as the sole §10.3 / §10.4 anchor.

---

## Safety posture

Research-only. No live trading. No exchange-write paths. No production keys. No `.mcp.json`, no Graphify, no MCP server activation. No `.env` changes, no credentials, no Binance API calls (authenticated or public). No edits to `docs/12-roadmap/technical-debt-register.md`. No edits to the implementation-ambiguity log. No edits to `.claude/`. No edits to source files, test files, scripts, datasets, or manifests **in Phase 2v**. No `data/` writes. No Phase 4 work. No paper/shadow planning. No live-readiness claim. No code in Phase 2v. No backtests in Phase 2v. No parameter tuning. No sweeps. No spec changes. No new ideas introduced. No candidate-set widening (only R2 + H0 + R3 controls in the run inventory). No multi-axis combination (no R2 + R1a; no R2 + R1b-narrow). Mark-price stop-trigger semantic preserved (MARK_PRICE default; TRADE_PRICE only as sensitivity diagnostic per run #9). R3 sub-parameters frozen. R1a sub-parameters frozen. R1b-narrow sub-parameter frozen. R2 sub-parameters frozen at Phase 2u §F values. The 8-bar setup window unchanged. No new structural-redesign candidate exposed beyond H0 / R3 / R1a+R3 / R1b-narrow / R2-on-execution-surface.

---

**End of Phase 2v R2 Gate 1 execution plan.** Sections 1–6 complete. Execution scope locks the Phase 2e v002 datasets, BTCUSDT primary / ETHUSDT secondary, R-window 2022-01-01 → 2025-01-01 + V-window 2025-01-01 → 2026-04-01, MEDIUM/MARK_PRICE default with LOW/HIGH and TRADE_PRICE sensitivity per §11.6 / GAP-032. Three control variants (H0 / R3 / R2+R3) across 10 runs. Backtest implementation checklist enumerates 7 component areas (config, entry-lifecycle module, StrategySession integration, engine integration, diagnostics funnel, per-trade record schema, tests) with bit-for-bit baseline-reproduction validation gates. Diagnostics plan maps each of P.1–P.14 to exact computation and reporting structure. Gate criteria preserve §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds unchanged and add a separate M1/M2/M3 mechanism-validation classification distinct from the framework verdict. Risk checklist enumerates implementation, fill-model, sample-size, BTC-vs-ETH, ETH-as-comparison, and backtester-surface risks with explicit mitigations.

**No code changes after plan drafting; no new runs; no new evidence; no spec changes; no new ideas.** Phase 2v itself does **not** authorize execution. A separate operator-approved Gate 2 review and explicit execution authorization are required. Phase 2v is complete and ready for operator/ChatGPT Gate 2 review. Stop after producing this plan.
