# Phase 4v — C1 Strategy Spec Memo

**Authority:** Operator authorization for Phase 4v (Phase 4u §"Operator decision menu" Option A primary recommendation: Phase 4v — C1 Strategy Spec Memo, docs-only). Phase 4u (C1 hypothesis-spec memo); Phase 4t (post-G1 fresh-hypothesis discovery); Phase 4s (post-G1 strategy research consolidation); Phase 4r (G1 backtest execution; Verdict C HARD REJECT — terminal for G1 first-spec); Phase 4q (G1 backtest-plan methodology); Phase 4p (G1 strategy spec); Phase 4o (G1 hypothesis-spec); Phase 4n (post-V2 fresh-hypothesis discovery); Phase 4m (post-V2 consolidation; 18-requirement fresh-hypothesis validity gate); Phase 4l (V2 backtest execution; Verdict C HARD REJECT — terminal for V2 first-spec); Phase 4k (V2 backtest-plan methodology); Phase 4j §11 (metrics OI-subset partial-eligibility binding); Phase 4i (V2 acquisition); Phase 4f (external strategy research landscape memo); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 3r §8 (mark-price gap governance); Phase 3t §12 (validity gate); Phase 2p §C.1 (R3 baseline-of-record); Phase 2i §1.7.3 (project-level locks); `docs/03-strategy-research/v1-breakout-strategy-spec.md`; `docs/03-strategy-research/v1-breakout-backtest-plan.md`; `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`; `docs/04-data/data-requirements.md`; `docs/04-data/live-data-spec.md`; `docs/04-data/timestamp-policy.md`; `docs/04-data/dataset-versioning.md`; `docs/07-risk/stop-loss-policy.md`; `docs/07-risk/position-sizing-framework.md`; `docs/07-risk/exposure-limits.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/ai-coding-handoff.md`; `docs/00-meta/implementation-ambiguity-log.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4v — **C1 Strategy Spec Memo** (docs-only). Translates the Phase 4u C1 hypothesis-spec layer into a complete ex-ante strategy specification with exact timeframes, contraction measure, expansion transition rule, breakout geometry, stop / target / time-stop / sizing model, opportunity-rate floors, mechanism-check thresholds, catastrophic-floor thresholds, threshold-grid policy, data-requirements decision, validation windows, and forbidden rescue interpretations. **Phase 4v does NOT run a backtest, write code, create a runnable strategy, modify `src/prometheus/`, modify tests, modify scripts, acquire data, modify data, modify manifests, create v003, create paper / shadow / live path, authorize exchange-write, or authorize Phase 4w.** **Phase 4v is text-only.**

**Branch:** `phase-4v/c1-strategy-spec-memo`. **Memo date:** 2026-05-03 UTC.

---

## Summary

Phase 4v locks the C1 — Volatility-Contraction Expansion Breakout strategy specification at the ex-ante level. C1 uses a 30m signal timeframe with a compression-box-based contraction measure (high-low range over `N_comp` prior 30m bars compared against a rolling-median width over the prior `W_width` 30m bars), a directional expansion transition (close beyond compression box ± `B_width` × box-width with close-location requirement), a structural stop derived from compression-box invalidation (compression box low/high ± `S_buffer` × box-width), a measured-move target (`T_mult` × box-width), and a time-stop of `2 × N_comp` 30m bars. The threshold grid is **exactly 32 variants over five binary axes** (`N_comp` ∈ {8, 12}; `C_width` ∈ {0.45, 0.60}; `B_width` ∈ {0.05, 0.10}; `S_buffer` ∈ {0.10, 0.20}; `T_mult` ∈ {1.5, 2.0}). Fixed parameters are `W_width = 240`, `L_delay = 1`, close-location fractions `0.70 / 0.30`, time-stop `2 × N_comp`, no HTF gate, no funding input, no metrics OI, no volume gate. Mechanism-check thresholds: M1 ≥ +0.10R contraction-vs-non-contraction differential under HIGH cost with bootstrap 95% CI lower > 0; M2 ≥ +0.05R C1-vs-always-active-same-geometry differential under HIGH cost with bootstrap 95% CI lower > 0 AND C1 ≥ delayed-breakout baseline under HIGH cost; M3 BTC OOS HIGH `mean_R > 0` AND `trade_count ≥ 30` AND no CFP-1 / CFP-2 / CFP-3 trigger; M4 ETH non-negative differential AND directional consistency (ETH cannot rescue BTC). Twelve catastrophic-floor predicates (CFP-1..CFP-12) are predeclared with C1-specific thresholds, including CFP-9 enriched as opportunity-rate / sparse-intersection collapse and CFP-11 enriched as transition-dependency violation. Validation windows reused verbatim from Phase 4k (train 2022-01-01..2023-06-30 UTC; validation 2023-07-01..2024-06-30 UTC; OOS 2024-07-01..2026-03-31 UTC). Data-requirements decision: existing data is sufficient; **no Phase 4w-prerequisite data-requirements memo required**; reuse Phase 4i v001 30m / 4h klines + v002 15m / 1h-derived klines + existing volume column (volume reported diagnostically only, not used in entry / stop / target rules); funding excluded from C1 first-spec. Phase 4v recommends Option A — Phase 4w C1 Backtest-Plan Memo (docs-only) as primary; Option B — remain paused as conditional secondary. **Phase 4v does NOT authorize Phase 4w.** **C1 remains pre-research only:** strategy-spec defined; not backtest-planned; not implemented; not backtested; not validated; not live-ready; **not a rescue of R3 / R2 / F1 / D1-A / V2 / G1**.

## Authority and boundary

- **Authority granted:** create the Phase 4v docs-only strategy-spec memo; create the Phase 4v closeout; choose exact C1 strategy rules; choose exact contraction measure; choose exact expansion transition rule; choose exact signal and context timeframes; choose exact entry / stop / target / time-stop / sizing model; choose exact opportunity-rate viability floors; choose exact mechanism-check thresholds; choose exact CFP thresholds; choose exact threshold grid; decide whether existing data is sufficient; recommend a future docs-only C1 backtest-plan memo (Phase 4w) if justified, or remain-paused.
- **Authority NOT granted:** run a backtest (forbidden); write backtest code (forbidden); write implementation code (forbidden); create a runnable strategy (forbidden); modify `src/prometheus/`, tests, or existing scripts (forbidden); acquire / modify / patch / regenerate / replace data (forbidden); modify manifests (forbidden); create v003 (forbidden); create paper / shadow / live path (forbidden); authorize exchange-write (forbidden); authorize Phase 4w or any successor phase (forbidden); authorize production keys / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials (forbidden).
- **Hard rule:** Phase 4v is text-only. No code is written. No data is touched. No backtest is run.

## Starting state

```text
Branch (Phase 4v):   phase-4v/c1-strategy-spec-memo
main / origin/main:  6862dc3708613109f74c04743c60e6cba78993d9 (unchanged)
Phase 4u merge:      f1b1a30fbc0ae4d120a63c38c9edb9d9b30e734c (merged)
Phase 4u housekeeping: 6862dc3708613109f74c04743c60e6cba78993d9 (merged)
Working-tree state:  clean (no tracked modifications); only gitignored
                     transients .claude/scheduled_tasks.lock and
                     data/research/ are untracked and will not be committed.
Quality gates (verified at memo creation):
  ruff check . PASS
  pytest 785 PASS
  mypy strict 0 issues across 82 source files
```

## Relationship to Phase 4u

- Phase 4u created the C1 hypothesis-spec layer only.
- Phase 4u did NOT create a strategy spec, threshold grid, backtest plan, backtest, or implementation.
- Phase 4u recommended Phase 4v as primary.
- The operator now explicitly authorized Phase 4v.
- Phase 4v remains docs-only.
- Phase 4v MUST NOT run a backtest, acquire data, write code, or authorize Phase 4w.
- Phase 4v MUST honor the Phase 4u binding design principles, the central anti-G1 discipline (no top-level state machine; no multi-dimension AND classifier; no broad regime gate), the Phase 4u opportunity-rate viability principle (predeclared *before* any data is touched; intrinsic to the theory; NOT derived from Phase 4r forensic numbers), and the Phase 4u forbidden-rescue interpretations (no G1 / V2 / R2 / F1 / D1-A rescue; no use of Phase 4r / Phase 4l forensic numbers; no use of microstructure / mark-price / aggTrades / metrics OI / 5m diagnostic outputs).

## Strategy name

```text
C1 — Volatility-Contraction Expansion Breakout
```

**Forbidden alternative names:** V3, G2, H2, G1-prime, G1-extension, G1-narrow, G1-hybrid, R1c, R3-prime, V2-prime, V2-narrow, V2-relaxed.

## Strategy thesis

C1's strategy thesis (operationalized from Phase 4u's hypothesis-spec):

> **BTCUSDT trend-continuation breakouts are more meaningful and more cost-resilient when the breakout fires from the directional release of a recent local volatility-contraction state.** A *compression box* defined over the prior `N_comp` 30m bars (excluding the current bar) bounds the contraction state. A contraction state is *active* when the compression box is narrow relative to the rolling 240-bar median compression-box width on the same instrument. The candidate setup fires only when a completed 30m bar's close *exits the compression box directionally* with a buffer (`B_width × box_width`) and a close-location consistent with the breakout direction (close in the upper / lower fraction of the bar's range). The structural stop is the *opposite* compression-box edge minus an `S_buffer × box_width` buffer (compression invalidation). The target is a measured-move multiple `T_mult × box_width` from entry. A time-stop of `2 × N_comp` 30m bars protects against post-transition stagnation. There is **no top-level regime state machine**, **no multi-dimension AND classifier**, **no per-bar volatility-percentile bolt-on filter**, **no V1 / V2 / G1 inherited setup geometry**, and **no funding-as-direction**. The hypothesis layer's central anti-G1 discipline (Phase 4u) is honored at the implementation-rule level: the candidate setup fires *only at the moment* the compression releases (`L_delay = 1` bar), not over the duration of the contraction state.

## Why this is not a rescue

C1's strategy spec is sharply distinguished from each prior rejected line. Phase 4u's binding distinctions are reaffirmed here at the operationalized rule level:

**vs G1 (regime-gate-meets-setup intersection sparseness):**

- G1 used a five-dimension AND classifier with a top-level state machine that suppressed entry evaluation on most bars (causing 2.03% active-fraction outcome).
- C1's contraction-box compression check is a **single-dimension local precondition** that fires the candidate setup *at the moment of compression release*, not over the duration of the contraction state. The candidate is generated by the *transition*, not by the *state*.
- C1 must NOT use Phase 4r forensic numbers (the 2.03% active fraction; the K_confirm ∈ {2, 3} confirmation lengths; the ATR percentile band {[20, 80], [30, 70]}; the V_liq_min ∈ {0.80, 1.00}; the funding band {[15, 85], [25, 75]}; the 124 always-active baseline trades; the −0.34 mean_R always-active outcome).

**vs R1a (volatility as a per-bar bolt-on filter to R3):**

- R1a applied a volatility-percentile predicate per-bar to the same R3 breakout setup.
- C1's contraction state is a **compression-box width check**, not a volatility-percentile filter; the compression-box itself defines the breakout geometry (the entry / stop / target levels are *all* derived from the compression box). The breakout geometry is **redesigned** from first principles, not augmented from R3.

**vs V2 (design-stage incompatibility):**

- V2 used a 20/40-bar Donchian setup combined with the V1-inherited 0.60–1.80 × ATR(20) stop-distance filter.
- C1 does NOT use the 20/40-bar Donchian shape; the `N_comp ∈ {8, 12}` compression window is shorter and serves a different role (compression measurement, not channel-breakout pattern). C1 does NOT use the 0.60–1.80 × ATR(20) stop-distance bound; in C1 first-spec there is **no ATR-percentile stop-distance gate at all** — the stop is structurally derived from the compression box.
- C1 must NOT use Phase 4l forensic numbers (the "3–5 × ATR" stop-distance observation; V2's locked Phase 4g axes).

**vs D1-A (mechanism / framework mismatch):**

- D1-A used trailing-90-day funding-rate Z-score as a contrarian directional trigger.
- C1 does NOT use funding as a directional trigger. **Funding is excluded from C1 first-spec entirely.**

**vs F1 (catastrophic-floor / mean-reversion):**

- F1 was a mean-reversion-after-overextension strategy.
- C1 is **continuation / expansion**, opposite directional intent. Compression releases follow the directional close beyond the compression box, by construction.

**vs R2 (cost-fragility / pullback-retest):**

- R2 was a pullback-retest entry that failed §11.6 cost-sensitivity.
- C1 is **expansion entry on transition**, not pullback retest. C1 preserves §11.6 = 8 bps HIGH per side verbatim; no cost-model relaxation.

## Preserved verdicts and locks

```text
H0           : FRAMEWORK ANCHOR (preserved)
R3           : BASELINE-OF-RECORD (preserved)
R1a          : RETAINED — NON-LEADING (preserved)
R1b-narrow   : RETAINED — NON-LEADING (preserved)
R2           : FAILED — §11.6 (preserved)
F1           : HARD REJECT (preserved)
D1-A         : MECHANISM PASS / FRAMEWORK FAIL — other (preserved)
5m thread    : OPERATIONALLY CLOSED (preserved)
V2           : HARD REJECT — terminal for V2 first-spec (preserved)
G1           : HARD REJECT — terminal for G1 first-spec (preserved)

§11.6        : 8 bps HIGH per side (preserved verbatim)
§1.7.3       : 0.25% risk / 2× leverage / 1 position / mark-price stops
v002 verdict provenance : preserved
Phase 3q manifests      : research_eligible: false for mark-price 5m
Phase 3r §8             : mark-price gap governance
Phase 3v §8             : stop-trigger-domain governance
Phase 3w §6 / §7 / §8   : break-even / EMA slope / stagnation governance
Phase 4j §11            : metrics OI-subset partial-eligibility (binding)
Phase 4k                : V2 backtest-plan methodology (binding)
Phase 4p / Phase 4q     : G1 strategy-spec / methodology (binding)
Phase 4u                : C1 hypothesis-spec layer (binding)
```

## Data requirements decision

**Existing data is sufficient.** Phase 4v decides:

- **No Phase 4w-prerequisite data-requirements memo required.**
- **No data acquisition required.** Phase 4v does NOT authorize acquisition.
- C1 first-spec uses only existing trade-price klines and existing volume.

## Data inputs

```text
Phase 4i (research-eligible per Phase 4i):
  binance_usdm_btcusdt_30m__v001          (74 448 bars; primary signal timeframe)
  binance_usdm_ethusdt_30m__v001          (74 448 bars; ETH comparison)
  binance_usdm_btcusdt_4h__v001           (9 306 bars; reporting-context only;
                                            NOT a rule input)
  binance_usdm_ethusdt_4h__v001           (9 306 bars; reporting-context only)

v002 (research-eligible):
  binance_usdm_btcusdt_15m__v002          (sanity / fallback; NOT a rule input)
  binance_usdm_ethusdt_15m__v002          (sanity / fallback; NOT a rule input)
  binance_usdm_btcusdt_1h_derived__v002   (1h reporting-context only;
                                            NOT a rule input in first-spec)
  binance_usdm_ethusdt_1h_derived__v002   (same)

Optional (excluded from first-spec):
  binance_usdm_btcusdt_funding__v002      (NOT used in C1 first-spec)
  binance_usdm_ethusdt_funding__v002      (NOT used in C1 first-spec)
```

Volume column (already present on klines): **reported diagnostically only**. C1 first-spec does NOT use volume in entry / stop / target rules.

## Timeframes

```text
Signal timeframe                    : 30m
Context timeframe (reporting only)  : 1h optional, NOT a rule input;
                                       4h excluded from first-spec rules
Entry execution                     : at next 30m bar's open after the
                                       completed signal bar
Decision time                       : the close_time of the completed
                                       30m signal bar (= open_time of the
                                       next 30m bar)
Bar discipline                      : completed bars only; no partial-bar
                                       consumption
```

## Contraction measure specification

C1's primary contraction measure is the **compression-box width** on completed 30m bars.

**Compression box (per completed 30m bar t, prior-completed only):**

```text
compression_box_high[t]    := max(high[t-N_comp] .. high[t-1])
compression_box_low[t]     := min(low[t-N_comp]  .. low[t-1])
compression_box_width[t]   := compression_box_high[t] - compression_box_low[t]
```

`N_comp ∈ {8, 12}` is **axis 1 of the threshold grid**.

**Width reference (rolling 240-bar median, prior-completed only):**

```text
rolling_median_width[t]    := median(compression_box_width[t-W_width] ..
                                      compression_box_width[t-1])
```

`W_width = 240` 30m bars (≈ 5 trading days at 30m). Fixed parameter (not an axis).

**Contraction-state predicate:**

```text
contraction_state[t] := (compression_box_width[t]
                        <= C_width × rolling_median_width[t])
```

`C_width ∈ {0.45, 0.60}` is **axis 2 of the threshold grid**.

The contraction state is **local** (a single-bar predicate evaluated on the prior `N_comp`-bar compression-box width vs. the rolling 240-bar median). It is **NOT a regime gate**. It does NOT suppress entry evaluation across most bars by itself — the binding entry-generating event is the **transition** (next section), not the state.

## Expansion transition specification

The candidate setup fires when a completed 30m bar's close *exits the compression box directionally* with a `B_width × compression_box_width` buffer AND a close-location requirement. A maximum delay `L_delay` from the contraction state is enforced.

**Long transition (per completed 30m bar t):**

```text
LONG_TRANSITION[t] :=
    contraction_recently_active[t]
    AND close[t] > compression_box_high[t] + B_width × compression_box_width[t]
    AND close_location_long[t] >= 0.70

where:
    contraction_recently_active[t] :=
        any(contraction_state[k] for k in [t - L_delay, ..., t])
        # i.e., the contraction state was active on bar t or within the
        # most recent L_delay bars before bar t
    close_location_long[t] :=
        (close[t] - low[t]) / max(high[t] - low[t], epsilon)
```

`B_width ∈ {0.05, 0.10}` is **axis 3 of the threshold grid**. `L_delay = 1` (fixed; the contraction state must be active on the same bar or the immediately prior completed bar). The 0.70 close-location threshold is fixed.

**Short transition (mirror):**

```text
SHORT_TRANSITION[t] :=
    contraction_recently_active[t]
    AND close[t] < compression_box_low[t] - B_width × compression_box_width[t]
    AND close_location_short[t] <= 0.30

where:
    close_location_short[t] := (close[t] - low[t]) / max(high[t] - low[t], epsilon)
```

The transition is **bounded in time**: with `L_delay = 1` the entry rule fires on the bar that completes the compression-to-expansion transition, or on the immediately following bar. After `L_delay` expires, the transition opportunity is gone (Phase 4u-mandated bounded-delay discipline).

## Directional breakout specification

- **LONG only on `LONG_TRANSITION[t] = true`.**
- **SHORT only on `SHORT_TRANSITION[t] = true`.**
- **No HTF directional gate.** Optional 1h context may be reported but does NOT gate signals in first-spec.
- **Breakout geometry is derived from `compression_box_high` / `compression_box_low`**, NOT from V1 / V2 / G1 Donchian / fixed-bar geometry.

## Entry rules

```text
Evaluation         : on each completed 30m bar t close
Entry timing       : at next 30m bar's open after a confirmed signal close
Order type         : market entry (no limit-order modeling)
Intrabar entry     : forbidden
Partial fills      : forbidden
One position max   : enforced
Pyramiding         : forbidden
Reversal in pos    : forbidden (subsequent opposite-direction signals while
                     positioned are dropped, not used to reverse)
Discretionary      : forbidden
BTCUSDT primary    : yes
ETHUSDT comparison : yes (comparison only; no portfolio sizing across symbols)
```

## Structural stop model

**Long stop (compression invalidation):**

```text
long_stop[t] := compression_box_low[t] - S_buffer × compression_box_width[t]
```

**Short stop (mirror):**

```text
short_stop[t] := compression_box_high[t] + S_buffer × compression_box_width[t]
```

`S_buffer ∈ {0.10, 0.20}` is **axis 4 of the threshold grid**. The stop is **fixed at entry** and is NOT widened, trailed, or moved to break-even.

**Stop-distance discipline (C1-specific):**

- The stop represents **compression-box invalidation**: the trade is invalidated if price re-enters the compression box and breaches the opposite edge.
- **No ATR-percentile stop-distance gate** in C1 first-spec. Phase 4l V2 forensic stop-distance numbers (the 0.60–1.80 × ATR(20) bound; the "3–5 × ATR" observation) are forbidden as design inputs.
- `stop_distance_atr` may be **reported diagnostically** by any future Phase 4w / 4x backtest, but is NOT a binding entry gate in first-spec.
- **R per unit:**
  ```text
  R_long  = entry_price - long_stop
  R_short = short_stop  - entry_price
  ```

## Target model

**Long target (measured-move):**

```text
long_target[t] := entry_price + T_mult × compression_box_width[t]
```

**Short target (mirror):**

```text
short_target[t] := entry_price - T_mult × compression_box_width[t]
```

`T_mult ∈ {1.5, 2.0}` is **axis 5 of the threshold grid**.

The target is a **measured move** of `T_mult` times the compression-box width at entry, *not* a fixed-R target. The implied R-multiple varies with the box-width / stop-distance ratio; it is reported diagnostically alongside trade results, but the target is fundamentally a structural measured-move.

## Time-stop model

```text
T_stop_bars := 2 × N_comp
```

If `N_comp = 8`, `T_stop_bars = 16`. If `N_comp = 12`, `T_stop_bars = 24`.

The time-stop is **fixed by the structural relationship** to `N_comp` (not a separate axis). It exits at the next 30m bar's open after `T_stop_bars` 30m bars have elapsed since entry.

- **No break-even.**
- **No trailing stop.**
- **No regime-driven exit** (because there is no regime state machine).

## Position sizing and exposure rules

Preserved verbatim from §1.7.3:

```text
risk_fraction               = 0.0025  (0.25% per trade)
max_leverage                = 2.0     (2× cap)
max_positions               = 1
max_active_protective_stops = 1
sizing equity               = constant assumption (e.g., 100 000 USDT;
                              R-relative results; no compounding)

position_size_units = sizing_equity × risk_fraction / abs(R_per_unit)

if position_notional > max_leverage × sizing_equity:
    cap position_size_units to (max_leverage × sizing_equity / entry_price)

below-min-notional handling: rejects (when exchange metadata is available);
                              R-based research sizing otherwise.

BTCUSDT primary; ETHUSDT comparison only;
ETH cannot rescue BTC; no portfolio sizing across symbols.
```

Stop-trigger-domain governance (Phase 3v §8): research = `trade_price_backtest`; future runtime = `mark_price_runtime`; future mark-price validation = `mark_price_backtest_candidate`; `mixed_or_unknown` invalid / fail-closed.

Break-even / EMA / stagnation governance (Phase 3w §6 / §7 / §8): C1 uses `break_even_rule = disabled` (preserved), `ema_slope_method = not_applicable` (C1 does not use EMA slope; this label is recorded explicitly), `stagnation_window_role = not_active` (C1 has a fixed time-stop, not a stagnation rule).

## Cost model

Preserved verbatim from §11.6 / Phase 4k / Phase 4q:

```text
LOW    = 1   bp slippage per side
MEDIUM = 4   bps slippage per side
HIGH   = 8   bps slippage per side    (§11.6 promotion gate; preserved)
Taker fee per side = 4 bps
Maker rebate     = NOT used
Live fee model   = NOT used
Funding cost     = NOT used in C1 first-spec (funding excluded)

Cost application (per round-trip trade):
  total_cost_bps_per_side(cell) := cell_slippage + taker_fee
  applied to entry and exit independently:
    long  entry_executed = entry_price × (1 + cost / 10 000)
    long  exit_executed  = exit_price  × (1 - cost / 10 000)
    short entry_executed = entry_price × (1 - cost / 10 000)
    short exit_executed  = exit_price  × (1 + cost / 10 000)

Promotion blocked if HIGH cost fails (R2 pattern preserved).
```

## Opportunity-rate viability floors

Predeclared **before any data is touched**, derived from first principles, NOT from Phase 4r forensic numbers:

```text
min_candidate_transition_rate_BTC_OOS_HIGH:
  At least 1 LONG_TRANSITION[t] OR SHORT_TRANSITION[t] event per 10 trading
  days equivalent (i.e., per 480 completed 30m bars), measured on the
  BTCUSDT 30m kline series for the OOS window. With a ~21-month OOS
  window of ~30 672 30m bars, this implies at least ~64 candidate
  transitions across all variants on BTC OOS HIGH.

min_executed_trade_count_BTC_OOS_HIGH:
  BTC OOS HIGH executed trade_count >= 30 (preserved from Phase 4q M3
  numeric; binding floor).

min_executed_trade_count_train_best:
  BTC train-best variant on OOS HIGH must have trade_count >= 30
  (binding for promotion).

min_variant_floor:
  At least 50% of the 32 variants must produce trade_count >= 30 on
  BTC OOS HIGH. (If <50% pass, CFP-1 triggers.)

stop_distance_pass_rate:
  N/A in first-spec (no ATR-percentile stop-distance gate). Future
  Phase 4w / 4x must report the empirical distribution of
  stop_distance_atr diagnostically; if the distribution is extreme
  (e.g., median > 5 × ATR), Phase 4w must flag it for operator review
  but cannot self-license a rescue.

sparse_intersection_collapse:
  CFP-9 enriched: triggers if any of:
    - candidate-transition rate floor fails on BTC OOS HIGH;
    - BTC OOS HIGH executed trade_count < 30 for the train-best variant;
    - >50% of 32 variants below 30 BTC OOS HIGH executed trades.
```

**These floors are intrinsic to C1's contraction-to-expansion theory** (BTCUSDT 30m bars typically exhibit local compression-and-release cycles on the order of multiple times per week; expecting at least one candidate transition per ~10 trading days is conservative). **They are NOT derived from Phase 4r G1 active-fraction numbers (the 2.03% observation), the 124 always-active baseline trades, or the −0.34 mean_R outcome.**

## Threshold grid

**Exactly 32 variants over five binary axes (= 2^5).** Deterministic lexicographic ordering.

```text
Axis 1: N_comp     in {8, 12}                 (compression-box lookback)
Axis 2: C_width    in {0.45, 0.60}            (contraction-width threshold
                                                vs rolling-median width)
Axis 3: B_width    in {0.05, 0.10}            (expansion-trigger buffer
                                                as fraction of box-width)
Axis 4: S_buffer   in {0.10, 0.20}            (stop buffer as fraction of
                                                box-width beyond box edge)
Axis 5: T_mult     in {1.5, 2.0}              (target multiplier of
                                                box-width)
```

**Fixed parameters (cardinality 1; not axes):**

```text
W_width                  = 240    (30m bars; ≈ 5 trading days at 30m)
L_delay                  = 1      (30m bars; max delay from contraction
                                    end to breakout trigger)
close_location_long      = 0.70   (long requires close in upper 30% of bar)
close_location_short     = 0.30   (short requires close in lower 30% of bar)
T_stop_bars              = 2 × N_comp
                           (16 if N_comp=8; 24 if N_comp=12; structurally
                            tied to N_comp — NOT a separate axis)
HTF gate                 = NONE   (no 1h or 4h gate)
funding input            = NONE   (excluded from first-spec)
volume input             = NONE   (reported diagnostically only)
metrics OI               = NONE   (Phase 4j §11 governance preserved;
                                    not used by C1)
break_even_rule          = disabled
ema_slope_method         = not_applicable
stagnation_window_role   = not_active
stop_trigger_domain (research) = trade_price_backtest
risk_fraction            = 0.0025
max_leverage             = 2.0
max_positions            = 1
```

**Variant ordering (deterministic lexicographic):** sort axes alphabetically (`B_width`, `C_width`, `N_comp`, `S_buffer`, `T_mult`); within each axis, sort values numerically ascending. The exact ordering tuple is to be documented in any future Phase 4w `run_metadata.json`.

## Search-space control

```text
Variant cardinality:    32 (= 2^5)
Variant ordering:       deterministic lexicographic (documented in
                         run_metadata.json)
Train-best selection:   by deflated-Sharpe-aware criterion on BTC train
                         MEDIUM cost cell (analogous to Phase 4q's
                         DSR-aware selection); raw-Sharpe tie-break;
                         lowest variant-id tie-break
Same identifier:        carried into validation and OOS reporting
                         (no re-selection)
Grid extension:         FORBIDDEN; if Phase 4w wants to extend, requires
                         separate operator authorization
Grid reduction:         FORBIDDEN; all 32 variants reported
Early exit:             FORBIDDEN; no outcome-driven shortcut
PBO / DSR / CSCV:       REQUIRED in any future backtest-plan / execution
DSR with N = 32         (Bailey & López de Prado 2014; skew/kurtosis correction)
PBO train→validation    (rank-based proxy)
PBO train→OOS           (rank-based proxy)
CSCV S = 16             (C(16, 8) = 12 870 combinations; analogous to
                         Phase 4k / Phase 4q)
RNG seed (pinned)       to be specified in Phase 4w; recommended same as
                         Phase 4r (202604300) unless operator chooses
                         a fresh seed.
```

## Signal generation logic

Conceptual pseudocode (any future Phase 4w / 4x must implement exactly):

```text
At each completed 30m bar t (decision time = close_time[t] = open_time[t+1]):

  # 1. Warmup check: require enough lookback
  if t < max(N_comp, W_width, ...): skip; no signal.

  # 2. Compression box (prior-completed bars only)
  cbh := max(high[t-N_comp..t-1])
  cbl := min(low[t-N_comp..t-1])
  cbw := cbh - cbl

  # 3. Rolling median of compression-box width over prior W_width bars
  rmw := median(compression_box_width[t-W_width..t-1])

  # 4. Contraction-state predicate (local; per-bar)
  contraction_state[t] := (cbw <= C_width × rmw)

  # 5. Recent-contraction window (bounded delay)
  contraction_recently_active[t] :=
      any(contraction_state[k] for k in [t - L_delay, ..., t])

  # 6. Long-transition predicate
  long_transition[t] :=
      contraction_recently_active[t]
      AND close[t] > cbh + B_width × cbw
      AND (close[t] - low[t]) / max(high[t] - low[t], epsilon) >= 0.70

  # 7. Short-transition predicate (mirror)
  short_transition[t] :=
      contraction_recently_active[t]
      AND close[t] < cbl - B_width × cbw
      AND (close[t] - low[t]) / max(high[t] - low[t], epsilon) <= 0.30

  # 8. Position state
  if positioned: drop any new transitions (no pyramiding; no reversal).

  # 9. Candidate generation
  if long_transition[t] and not positioned:
      stop  := cbl - S_buffer × cbw
      entry := open[t+1]   # next 30m bar open
      R_per_unit := entry - stop
      if R_per_unit > 0:
          target := entry + T_mult × cbw
          schedule entry; record entry_bar = t+1; side = LONG.

  if short_transition[t] and not positioned:
      stop  := cbh + S_buffer × cbw
      entry := open[t+1]
      R_per_unit := stop - entry
      if R_per_unit > 0:
          target := entry - T_mult × cbw
          schedule entry; record entry_bar = t+1; side = SHORT.

  # 10. Hard rules
  no signal if:
    insufficient lookback;
    duplicate (symbol, interval, open_time);
    timestamp policy violation;
    current bar is partial;
    transition fired more than L_delay bars after contraction ended;
    already positioned;
    R_per_unit <= 0 (degenerate).
```

## Exit logic

```text
At each completed 30m bar t' after entry (entry_bar < t'):

  bars_in_trade := t' - entry_bar

  # Stop precedence: stop > target > time-stop
  if side == LONG:
      stop_touched := low[t']  <= stop
      tp_touched   := high[t'] >= target
  else:  # SHORT
      stop_touched := high[t'] >= stop
      tp_touched   := low[t']  <= target

  time_due := bars_in_trade >= T_stop_bars

  if stop_touched and tp_touched:
      # Same-bar ambiguity: stop wins (conservative)
      exit_reason := STOP
      exit_price  := stop
  elif stop_touched:
      exit_reason := STOP
      exit_price  := stop
  elif tp_touched:
      exit_reason := TARGET
      exit_price  := target
  elif time_due:
      exit_reason := TIME_STOP
      exit_price  := open[t'+1]  # next 30m bar open
  else:
      continue holding.

# Apply costs (LOW / MEDIUM / HIGH cells)
# No break-even
# No trailing stop
# No regime exit (no regime state machine)
```

## Funding / volume / context handling

```text
Funding (v002 funding manifests):
  Excluded from C1 first-spec rules. Phase 4w / 4x may report funding
  cost as a diagnostic if entries occur on completed funding events,
  but no funding cost adjustment is applied to the trade R in C1
  first-spec because no position is held across funding events long
  enough to make funding cost material relative to slippage + fees
  on a 16-24-bar (8-12 hour) typical position. If the operator
  separately chooses to include funding cost in Phase 4w, this is
  acceptable but must be predeclared in the Phase 4w memo before
  data is touched.

Volume (existing column on klines):
  Reported diagnostically only. Not used in entry / stop / target /
  time-stop rules. Phase 4w / 4x must record the OOS distribution
  of volume on candidate-transition bars for diagnostic purposes
  but cannot license a rescue based on the diagnostic.

HTF context (1h, 4h):
  No gate. No rule input. May be used for stratified reporting only
  (e.g., "C1 OOS HIGH performance by 1h trend regime") if Phase 4w
  predeclares the stratification.

All rule inputs use prior-completed bars only.
```

## Forbidden inputs

```text
mark-price (any timeframe)              -- Phase 3r §8 governance preserved;
                                           NOT used in C1
aggTrades                                -- not loaded; NOT used in C1
spot data                                -- not loaded; NOT used in C1
cross-venue data                         -- not loaded; NOT used in C1
order book                               -- not loaded; NOT used in C1
private / authenticated data             -- forbidden by §1.7.3 / §10.1
user stream / WebSocket / listenKey      -- forbidden by Phase 4u
metrics OI                               -- Phase 4j §11 preserved;
                                           NOT used by C1
optional metrics ratio columns           -- Phase 4j §11.3 forbidden;
                                           NOT used by C1
5m Q1–Q7 diagnostic outputs              -- Phase 3o §6 / Phase 3t §14.2
                                           preserved; NOT used by C1
V2 Phase 4l forensic stop-distance       -- forbidden by Phase 4u as
  numbers / "3–5 × ATR" observation        tuning targets
G1 Phase 4r active-fraction (2.03%) /    -- forbidden by Phase 4u as
  124 always-active trades / -0.34         tuning targets
  mean_R / G1 locked Phase 4p axes
online thresholds / parameters from      -- forbidden as adopted project
  external sources                         values
```

## Mechanism-check thresholds

```text
M1 — Contraction-state validity:
  C1 (entries fired by transitions tied to contraction) must outperform
  a non-contraction breakout baseline (entries fired by the same close-
  beyond-compression-box-with-buffer rule, on bars where contraction
  was NOT recently active in the L_delay window). Same stop / target /
  time-stop / cost cell.

  Pass: C1_mean_R - non_contraction_mean_R >= +0.10R on BTC OOS HIGH
        AND bootstrap CI lower (B = 10 000) > 0.

M2 — Expansion-transition value-add:
  C1 must outperform an always-active-same-geometry breakout baseline
  (same close-beyond-compression-box-with-buffer rule, but without
  the contraction precondition). Same stop / target / time-stop / cost.

  Pass: C1_mean_R - always_active_same_geometry_mean_R >= +0.05R on
        BTC OOS HIGH AND bootstrap CI lower (B = 10 000) > 0.

  AND: C1_mean_R - delayed_breakout_mean_R >= 0 on BTC OOS HIGH
       (delayed-breakout = same setup but entries that fire >L_delay
       bars after contraction ended; transition timing claim).

M3 — Inside-spec co-design validity:
  BTC OOS HIGH mean_R > 0
  AND BTC OOS HIGH trade_count >= 30
  AND no CFP-1 / CFP-2 / CFP-3 trigger
  AND opportunity-rate floors satisfied (min_candidate_transition_rate
       AND min_executed_trade_count_train_best AND min_variant_floor).

M4 — Cross-symbol robustness:
  ETH OOS HIGH (G1-vs-baseline) differential non-negative
  AND directional consistency with BTC.
  ETH cannot rescue BTC. CFP-4 enforces this.

M5 — Compression-box structural validity (DIAGNOSTIC ONLY in first-spec):
  Stops tied to compression-box invalidation behave better than a
  generic ATR-buffered structural stop on the same setup. Diagnostic
  only in first-spec; Phase 4w may upgrade to binding gate if justified.

Promotion-bar:
  M1 PASS AND M2 PASS AND M3 PASS AND M4 PASS AND no CFP triggered.

Bootstrap:
  B = 10 000.
  RNG seed pinned in Phase 4w (recommended: 202604300).
```

## Negative-test specification

```text
Required (binding):
  non_contraction_breakout_baseline
    Same close-beyond-compression-box-with-buffer rule, but on bars
    where contraction was NOT active in the L_delay window. Same stop /
    target / time-stop / cost. PURPOSE: M1 validity.

  always_active_same_geometry_breakout_baseline
    Same close-beyond-compression-box-with-buffer rule, applied on
    every bar (no contraction precondition). Same stop / target /
    time-stop / cost. PURPOSE: M2 value-add.

  delayed_breakout_baseline
    Same setup but entries that fire >L_delay bars after contraction
    ended. Same stop / target / time-stop / cost. PURPOSE: M2 detail
    (transition-timing claim).

  active_opportunity_rate_diagnostic
    Measures candidate-transition rate, executed trade count, and
    by-month / by-symbol distributions. PURPOSE: M3 / CFP-9.

Optional (diagnostic only by default; Phase 4w may upgrade):
  random_contraction_baseline
    Same active-fraction as real contraction-state, but on randomly-
    selected bars (separate RNG seed derived from main seed). Same
    stop / target / time-stop / cost. PURPOSE: contraction specificity
    check.

If the non-contraction or always-active baseline performs equally well or
better, C1 fails M1 / M2.
If delayed-breakout outperforms transition-tied, the transition-timing
claim fails.
If random-contraction performs similarly to real contraction, the
contraction specificity is weak.
If opportunity-rate collapses (CFP-9), C1 fails at the viability layer.
```

## Catastrophic-floor predicates

```text
CFP-1   Insufficient trade count:
        Trigger if BTC train-best variant OOS HIGH trade_count < 30
        OR more than 50% of the 32 variants have BTC OOS HIGH
        trade_count < 30.

CFP-2   Negative BTC OOS HIGH expectancy:
        Trigger if BTC train-best variant OOS HIGH mean_R <= 0
        OR any selected promotion candidate has mean_R <= 0.

CFP-3   Catastrophic profit-factor / drawdown:
        Trigger if BTC train-best variant OOS HIGH profit_factor < 0.50
        OR max_drawdown_R > 10R.

CFP-4   BTC failure with ETH pass:
        Trigger if M3 BTC FAILS AND M4 ETH PASSES
        (ETH cannot rescue BTC).

CFP-5   Train-only success / OOS failure:
        Trigger if train HIGH mean_R > 0 BUT OOS HIGH mean_R <= 0
        for the train-best variant.

CFP-6   Excessive PBO / DSR failure:
        Trigger if PBO_train_validation > 0.50
        OR PBO_train_oos > 0.50
        OR PBO_cscv > 0.50
        OR train-best DSR <= 0.

CFP-7   Regime / month overconcentration:
        Trigger if any single calendar month accounts for >50% of
        total OOS BTC HIGH trades for the train-best variant.

CFP-8   Sensitivity fragility:
        Trigger if a small predeclared perturbation around any of the
        five structural axes causes a >0.20R degradation in OOS HIGH
        mean_R OR flips mean_R sign for the train-best variant.
        Perturbation ranges (predeclared in Phase 4w):
          N_comp:     {6, 10, 14}      (extending {8, 12} by ±2)
          C_width:    {0.40, 0.65}     (extending {0.45, 0.60} by ±0.05)
          B_width:    {0.025, 0.15}    (extending {0.05, 0.10})
          S_buffer:   {0.05, 0.30}     (extending {0.10, 0.20})
          T_mult:     {1.0, 2.5}       (extending {1.5, 2.0})
        Sensitivity cells are diagnostic / CFP-8 checks; NOT new
        active variants.

CFP-9   Opportunity-rate / sparse-intersection collapse:
        Trigger if any of:
          (a) BTC OOS HIGH candidate-transition rate < 1 per 480 30m
              bars (i.e., <64 candidates across the OOS window for the
              train-best variant);
          (b) BTC OOS HIGH executed trade_count < 30 for the train-best
              variant;
          (c) >50% of 32 variants have BTC OOS HIGH trade_count < 30
              (this overlaps with CFP-1; CFP-1 binds if so).

CFP-10  Forbidden optional ratio access:
        Trigger if any of count_toptrader_long_short_ratio,
        sum_toptrader_long_short_ratio, count_long_short_ratio, or
        sum_taker_long_short_vol_ratio is read at any time during the
        run.

CFP-11  Lookahead / transition-dependency violation:
        Trigger if any of:
          (a) classifier or signal uses any bar with close_time >
              decision_time;
          (b) signal generated without prior contraction precondition
              (contraction_recently_active[t] = false);
          (c) entry fired >L_delay bars after contraction state ended;
          (d) same-bar AND-chain that consults the breakout-trigger
              of the same evaluation;
          (e) partial-bar consumption.

CFP-12  Data governance violation:
        Trigger if any of:
          - metrics OI is loaded;
          - mark-price (any timeframe) is loaded;
          - aggTrades is loaded;
          - spot / cross-venue data is loaded;
          - non-binding manifest is loaded;
          - network I/O attempted;
          - credentials / .env read;
          - write attempted to data/raw/, data/normalized/, or
            data/manifests/;
          - manifest modified;
          - v003 created;
          - private / authenticated REST / user-stream / WebSocket /
            listenKey path touched.
```

**Any single CFP triggered = Verdict C HARD REJECT** in any future Phase 4x backtest, unless a stop-condition / incomplete-methodology issue makes Verdict D more appropriate.

## Validation windows

Reused verbatim from Phase 4k:

```text
Train          : 2022-01-01 00:00:00 UTC .. 2023-06-30 23:30:00 UTC  (~18 months)
Validation     : 2023-07-01 00:00:00 UTC .. 2024-06-30 23:30:00 UTC  (~12 months)
OOS holdout    : 2024-07-01 00:00:00 UTC .. 2026-03-31 23:30:00 UTC  (~21 months;
                                                                     primary C1
                                                                     evidence cell)
```

No window modification post-hoc. No data shuffling. No leakage. Same 32 variants evaluated independently per symbol; no cross-symbol optimization. ETH cannot rescue BTC.

## BTCUSDT primary / ETHUSDT comparison protocol

```text
Primary symbol:        BTCUSDT
Comparison symbol:     ETHUSDT
ETH cannot rescue BTC  (CFP-4 enforces this binding rule).
No portfolio sizing across symbols; results are reported per symbol.
Same 32 variants evaluated independently per symbol;
no cross-symbol optimization.
Same RNG seed across symbols (in any future Phase 4x).
Train-best variant identified on BTC train MEDIUM by DSR-aware
criterion; same variant identifier carried into ETH comparison.
```

## Required future backtest artefacts

A future Phase 4w C1 Backtest-Plan Memo (docs-only) would need to specify exactly (analogous to Phase 4q for G1):

- exact future script boundary (e.g., `scripts/phase4x_c1_backtest.py`; standalone research script; no `prometheus.runtime/execution/persistence` imports; no exchange adapters; no `requests/httpx/aiohttp/websockets/urllib`; no `.env`; no credentials; no Binance API; no network I/O);
- exact future command shape (date ranges; window boundaries; primary / comparison symbols; output dir; pinned RNG seed);
- exact data-loading rules with explicit column lists (klines: `open_time`, `close_time`, `open`, `high`, `low`, `close`, `volume`; v002 funding NOT loaded by default in C1 first-spec);
- exact feature computation algorithms (compression-box high/low/width; rolling-median width; contraction-state predicate; transition predicates with close-location; structural stop; measured-move target);
- exact signal generation pseudocode (matching the "Signal generation logic" section above verbatim);
- exact entry / exit simulation (matching the "Entry rules" and "Exit logic" sections above verbatim);
- exact cost / funding model (LOW / MEDIUM / HIGH cells; taker fee 4 bps; no maker rebate; funding excluded);
- exact position-sizing / exposure rules (matching the "Position sizing" section above verbatim);
- exact 32-variant grid handling with deterministic lexicographic ordering;
- exact PBO / DSR / CSCV plan (DSR with N = 32; PBO train→validation, train→OOS rank-based; CSCV S = 16 / C(16, 8) = 12 870 combinations);
- exact M1 / M2 / M3 / M4 mechanism-check implementation plans with the numeric thresholds locked in this memo;
- exact negative-test implementation plan (non-contraction; always-active-same-geometry; delayed-breakout; opportunity-rate diagnostic; random-contraction optional);
- exact CFP-1..CFP-12 evaluation algorithms with the numeric thresholds locked in this memo;
- exact Verdict A / B / C / D taxonomy;
- exact required reporting tables (analogous to Phase 4q's 25-table list, adapted for C1);
- exact required plots (analogous to Phase 4q's 11-plot list, adapted for C1);
- exact stop-condition list (manifest mismatch; forbidden-input access; lookahead detection; write attempts; ruff/pytest/mypy fail; etc.);
- exact reproducibility requirements (manifest SHA pinning; commit SHA pinning; deterministic variant ordering; pinned RNG seed; idempotent outputs).

**Phase 4v does NOT create any of these artefacts.** They are the responsibility of a future, separately-authorized Phase 4w.

## Stop conditions for future backtest

Any future Phase 4x C1 backtest MUST immediately stop and produce a failure report on any of:

```text
- required manifest missing
- manifest SHA mismatch
- research_eligible mismatch (where applicable)
- local data file missing or corrupted
- forbidden input accessed:
    metrics OI loaded
    optional ratio column accessed
    mark-price (any timeframe) loaded
    aggTrades loaded
    spot / cross-venue loaded
    5m diagnostic outputs loaded as features
    non-binding manifest loaded
- private / authenticated / API / WebSocket / network path touched
- credential read or store attempted
- .env read
- write attempted to data/raw/, data/normalized/, or data/manifests/
- modification of existing src/ / tests / scripts
- classifier / signal uses future bars
- entry fires without prior contraction precondition
- entry fires more than L_delay bars after contraction state ended
- multi-direction emission while positioned
- timestamp misalignment
- duplicate (symbol, interval, open_time) row
- partial-bar consumption for strategy decision
- validation report incomplete
- ruff fail
- pytest fail or test-count regression below 785
- mypy strict fail
- variant grid expanded beyond 32 or contracted below 32
- variant ordering changes between train / validation / OOS
- non-pinned RNG seed
- bootstrap impossible due to insufficient sample (Verdict D path)
- opportunity-rate collapse beyond CFP-9 floors
```

A stop condition aborts the run and produces a failure report; no fallback / silent approximation is permitted.

## What future Phase 4w / 4x would need to do

Recommended future sequence:

- **Phase 4w — C1 Backtest-Plan Memo (docs-only)** — translates the Phase 4v strategy spec into the exact future Phase 4x methodology (data-loading; feature computation; signal generation; trade simulation; cost / funding; grid handling; PBO / DSR / CSCV; M1 / M2 / M3 / M4; CFPs; required tables and plots; stop conditions; reproducibility). Phase 4w must be docs-only.
- **Phase 4x — C1 Backtest Execution (docs-and-code, standalone research script)** — only if Phase 4w is separately authorized and merged. Phase 4x would create `scripts/phase4x_c1_backtest.py` exactly under the Phase 4w methodology, run the backtest, and emit a verdict per the Phase 4w verdict taxonomy.

If Phase 4w determines data is insufficient (which Phase 4v judges unlikely under the recommended path), Phase 4w should instead be a **C1 Data Requirements Memo (docs-only)**. **Phase 4v does NOT acquire data.**

**Phase 4v does NOT authorize Phase 4w.** Phase 4w execution requires a separate explicit operator authorization brief.

## What this does not authorize

Phase 4v does NOT authorize:

- Phase 4w execution (must be separately authorized);
- a backtest run;
- writing of code;
- creation of a script;
- creation of a runnable strategy;
- modification of `src/prometheus/`, tests, or existing scripts;
- modification of `data/raw/`, `data/normalized/`, or `data/manifests/`;
- creation of new manifests or v003;
- data acquisition;
- paper / shadow / live / exchange-write / production keys / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- start of Phase 4 canonical;
- amendment of any project lock (§11.6 / §1.7.3 / mark-price stops / v002 verdict provenance);
- amendment of any governance rule (Phase 3r / 3v / 3w / 4j §11 / 4k);
- amendment of any retained verdict (R3 / R2 / R1a / R1b-narrow / F1 / D1-A / V2 / G1 / H0).

## Forbidden-work confirmation

Phase 4v did NOT do any of the following:

- run a backtest (any phase);
- write any code;
- create any script;
- modify any source under `src/prometheus/`;
- modify any test;
- modify any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`);
- run `scripts/phase4r_g1_backtest.py`;
- run any acquisition / diagnostics / backtest script;
- acquire data;
- download data;
- patch / forward-fill / interpolate / regenerate / replace data;
- modify any manifest;
- create any new manifest;
- create v003;
- modify Phase 4p / Phase 4q / Phase 4j §11 / Phase 4k / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r §8 governance;
- revise any retained verdict;
- change any project lock;
- create a runnable strategy;
- create V3 / H2 / G2 / any runnable candidate name beyond C1;
- create G1-prime / G1-narrow / G1-extension / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- propose a 5m strategy / hybrid / variant;
- start Phase 4w / 4 canonical / paper-shadow / live-readiness / deployment / production-key creation / exchange-write capability / authenticated REST / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- consult any private endpoint / user stream / WebSocket / authenticated REST in code;
- store, request, or display any secret;
- perform web research that collected market data, downloaded archives, called Binance APIs, called `data.binance.vision`, scraped prices, created datasets, or imported online thresholds as adopted project values.

## Remaining boundary

```text
R3                  : V1 breakout baseline-of-record (preserved)
H0                  : framework anchor (preserved)
R1a / R1b-narrow    : retained research evidence; non-leading (preserved)
R2                  : FAILED — §11.6 cost-sensitivity blocks (preserved)
F1                  : HARD REJECT (preserved)
D1-A                : MECHANISM PASS / FRAMEWORK FAIL — other (preserved)
V2                  : HARD REJECT (Phase 4l terminal for first-spec; preserved)
G1                  : HARD REJECT (Phase 4r — Verdict C; CFP-1 critical
                       binding driver; CFP-9 independent driver;
                       terminal for G1 first-spec)
5m diagnostic thread : OPERATIONALLY CLOSED (Phase 3t)
§11.6               : 8 bps HIGH per side (preserved verbatim)
§1.7.3              : 0.25% risk / 2× leverage / 1 position / mark-price stops
                      (preserved)
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m
                              (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance
                              (preserved)
Phase 4a runtime            : public API and behavior (preserved)
Phase 4e                    : reconciliation-model design memo (preserved)
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q / 4r / 4s / 4t / 4u
                            : all preserved verbatim
Phase 4v                    : C1 strategy-spec memo (this phase; new; docs-only)
C1                          : pre-research only;
                              hypothesis-spec defined in Phase 4u;
                              strategy-spec defined in Phase 4v;
                              not backtest-planned;
                              not implemented; not backtested; not validated;
                              not live-ready;
                              not a rescue of R3 / R2 / F1 / D1-A / V2 / G1
Recommended state           : Phase 4w conditional primary;
                              remain-paused conditional secondary
```

## Operator decision menu

- **Option A — primary recommendation:** Phase 4w — C1 Backtest-Plan Memo (docs-only). Phase 4w would translate the Phase 4v C1 strategy spec into a precise, reproducible, fail-closed future Phase 4x backtest methodology, mirroring Phase 4q's discipline (NOT V2 / G1 numeric thresholds). Phase 4w would be docs-only; would NOT acquire data; would NOT run a backtest.
- **Option B — conditional secondary:** remain paused.

NOT recommended:

- immediate C1 backtest — REJECTED;
- immediate C1 implementation — REJECTED;
- data acquisition — REJECTED;
- paper / shadow / live-readiness — FORBIDDEN;
- Phase 4 canonical — FORBIDDEN;
- production-key creation / authenticated APIs / private endpoints / user stream / WebSocket — FORBIDDEN;
- MCP / Graphify / `.mcp.json` / credentials — FORBIDDEN;
- exchange-write capability — FORBIDDEN;
- any G1 / V2 / R2 / F1 / D1-A rescue — FORBIDDEN.

**Phase 4w is NOT authorized by this Phase 4v memo.** Phase 4w execution requires a separate explicit operator authorization brief.

## Next authorization status

```text
Phase 4w                       : NOT authorized
Phase 4x                       : NOT authorized
Phase 4 (canonical)            : NOT authorized
Paper / shadow                 : NOT authorized
Live-readiness                 : NOT authorized
Deployment                     : NOT authorized
Production-key creation        : NOT authorized
Authenticated REST             : NOT authorized
Private endpoints              : NOT authorized
User stream / WebSocket        : NOT authorized
Exchange-write capability      : NOT authorized
MCP / Graphify                 : NOT authorized
.mcp.json / credentials        : NOT authorized
C1 implementation              : NOT authorized
C1 backtest execution          : NOT authorized
C1 data acquisition            : NOT authorized (none required)
G1 / V2 / R2 / F1 / D1-A rescue: NOT authorized; not proposed
G1-prime / G1-extension axes   : NOT authorized; not proposed
G1-narrow / G1 hybrid          : NOT authorized; not proposed
V2-prime / V2-variant          : NOT authorized; not proposed
Retained-evidence rescue       : NOT authorized; not proposed
5m strategy / hybrid           : NOT authorized; not proposed
ML feasibility                 : NOT authorized; not proposed
Microstructure / liquidity-timing data acquisition (Phase 4t Candidate F)
                               : NOT authorized; data unavailable.
```

The next step is operator-driven: the operator decides whether to authorize Phase 4w (C1 Backtest-Plan Memo, docs-only) or remain paused. Until then, the project remains at the post-Phase-4v strategy-spec boundary.

---

**Phase 4v was docs-only. No source code, tests, scripts, data, manifests, or successor phases were created or modified. Recommended state: Phase 4w conditional primary; remain-paused conditional secondary. No next phase authorized.**
