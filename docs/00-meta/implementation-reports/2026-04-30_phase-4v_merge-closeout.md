# Phase 4v Merge Closeout

## Summary

Phase 4v — C1 Strategy Spec Memo (docs-only) — has been merged into `main` via a no-fast-forward merge commit. Phase 4v translates the Phase 4u C1 hypothesis-spec layer into a complete ex-ante strategy specification with exact thresholds. C1's first-spec is locked: 30m signal timeframe; compression-box-based contraction measure with rolling-median width comparator; directional close-beyond-compression-box-with-buffer expansion transition with close-location requirement; structural stop derived from compression-box invalidation; measured-move target; time-stop fixed at `2 × N_comp` 30m bars; 0.25% risk / 2× leverage / 1 position max preserved verbatim from §1.7.3; §11.6 = 8 bps HIGH per side preserved verbatim; LOW / MEDIUM / HIGH cost cells with 4 bps taker fee per side; 32-variant grid (= 2^5) over five binary axes (`N_comp` ∈ {8, 12}; `C_width` ∈ {0.45, 0.60}; `B_width` ∈ {0.05, 0.10}; `S_buffer` ∈ {0.10, 0.20}; `T_mult` ∈ {1.5, 2.0}); fixed parameters (`W_width = 240`; `L_delay = 1`; close-location 0.70 / 0.30; `T_stop_bars = 2 × N_comp`; no HTF gate; no funding input; no metrics OI; no volume gate; **no ATR-percentile stop-distance gate**); M1 / M2 / M3 / M4 mechanism-check thresholds with M5 diagnostic-only; opportunity-rate viability floors derived from first principles; 12 catastrophic-floor predicates with C1-specific thresholds (CFP-9 enriched as opportunity-rate / sparse-intersection collapse; CFP-11 enriched as transition-dependency violation); validation windows reused verbatim from Phase 4k; BTCUSDT primary / ETHUSDT comparison; ETH cannot rescue BTC. **C1 remains pre-research only**: not backtest-planned; not implemented; not backtested; not validated; not live-ready; **not a rescue of R3 / R2 / F1 / D1-A / V2 / G1**. Phase 4v was docs-only.

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4v_c1-strategy-spec-memo.md   (added by merge)
docs/00-meta/implementation-reports/2026-04-30_phase-4v_closeout.md                 (added by merge)
docs/00-meta/implementation-reports/2026-04-30_phase-4v_merge-closeout.md          (added by housekeeping commit — this file)
docs/00-meta/current-project-state.md                                               (modified by housekeeping commit — narrow Phase 4v paragraph + "Current phase" / "Most recent merge" refresh)
```

No other files modified by Phase 4v or by this merge.

## Phase 4v commits included

```text
5f4202dd7bc9556747cec6e873aad7d0ca76d698   phase-4v: C1 strategy spec memo (docs-only)
40d86e04451f686166d1b1c5d3fb6cd35b5d93c2   phase-4v: closeout (C1 strategy spec memo)
```

## Merge commit

```text
62290cd9d03550de3577dbc74ba2263ef132e4e2   Merge Phase 4v (C1 strategy spec memo, docs-only) into main
```

## Housekeeping commit

```text
<recorded after this file is committed>
```

## Final git status

(recorded after housekeeping commit and push)

## Final git log --oneline -8

(recorded after housekeeping commit and push)

## Final rev-parse

```text
main          : <recorded after housekeeping push>
origin/main   : <recorded after housekeeping push>
```

## main == origin/main confirmation

(verified after housekeeping push; reported in chat)

## Strategy-spec conclusion

- **Phase 4v was docs-only.**
- Phase 4v defines **C1 — Volatility-Contraction Expansion Breakout** as a complete ex-ante strategy specification.
- **C1 remains pre-research only:**
  - not backtest-planned;
  - not implemented;
  - not backtested;
  - not validated;
  - not live-ready;
  - **not a rescue of R3 / R2 / F1 / D1-A / V2 / G1**.
- **Phase 4v does NOT authorize Phase 4w.**
- Phase 4v does NOT authorize backtest, implementation, data acquisition, paper / shadow / live, or exchange-write.
- **No retained verdict is revised.**
- **No project lock is changed.**

## Relationship to Phase 4u

- Phase 4u created the C1 hypothesis-spec layer only (no strategy spec, no threshold grid, no backtest plan, no backtest, no implementation).
- Phase 4u recommended Phase 4v as primary.
- The operator authorized Phase 4v.
- Phase 4v honored the Phase 4u binding design principles (contraction is local; entry on the transition itself; no top-level state machine; no multi-dimension AND classifier; no broad regime gate), the Phase 4u central anti-G1 discipline, the Phase 4u opportunity-rate viability principle (predeclared *before* any data is touched; intrinsic to the theory; NOT derived from Phase 4r forensic numbers), and the Phase 4u forbidden-rescue interpretations.
- **Phase 4v does NOT modify Phase 4u.** Phase 4u's hypothesis-spec is a binding input.
- Phase 4v does NOT run a backtest, acquire data, write code, or authorize Phase 4w.

## Strategy name

```text
C1 — Volatility-Contraction Expansion Breakout
```

Forbidden alternative names (would imply rescue): V3, G2, H2, G1-prime, G1-extension, G1-narrow, G1-hybrid, R1c, R3-prime, V2-prime, V2-narrow, V2-relaxed.

## Data requirements decision

**Existing data is sufficient.** No Phase 4w-prerequisite data-requirements memo required. **No data acquisition required.** Phase 4v does NOT authorize acquisition.

```text
Primary signal timeframe         : Phase 4i BTCUSDT / ETHUSDT 30m v001
                                    (research-eligible)
Reporting context only (NOT rule
inputs)                          : Phase 4i BTCUSDT / ETHUSDT 4h v001
Sanity / fallback only           : v002 BTCUSDT / ETHUSDT 15m
Reporting context only           : v002 BTCUSDT / ETHUSDT 1h-derived
Funding input                    : EXCLUDED from C1 first-spec
Volume input                     : DIAGNOSTIC only (NOT used in
                                    entry / stop / target / time-stop rules)
```

## Timeframes

```text
Signal timeframe                    : 30m
Context timeframe (reporting only)  : 1h optional, NOT a rule input;
                                       4h excluded from first-spec rules
Entry execution                     : at next 30m bar's open after the
                                       completed signal bar
Decision time                       : the close_time of the completed
                                       30m signal bar
Bar discipline                      : completed bars only
```

## Contraction measure

```text
compression_box_high[t]    := max(high[t-N_comp..t-1])
compression_box_low[t]     := min(low[t-N_comp..t-1])
compression_box_width[t]   := high - low
rolling_median_width[t]    := median(width[t-W_width..t-1])
contraction_state[t]       := (width <= C_width × rolling_median_width)

W_width = 240 (fixed); N_comp ∈ {8, 12} (axis 1);
C_width ∈ {0.45, 0.60} (axis 2).
```

## Expansion transition

```text
contraction_recently_active[t] := any(contraction_state[t-L_delay..t])

LONG_TRANSITION[t] :=
    contraction_recently_active[t]
    AND close[t] > compression_box_high[t] + B_width × compression_box_width[t]
    AND close_location_long[t] >= 0.70

SHORT_TRANSITION[t] :=
    contraction_recently_active[t]
    AND close[t] < compression_box_low[t] - B_width × compression_box_width[t]
    AND close_location_short[t] <= 0.30

L_delay = 1 (fixed); B_width ∈ {0.05, 0.10} (axis 3);
close_location_long = 0.70 / close_location_short = 0.30 fixed.
```

## Entry / stop / target / sizing model

```text
Entry           : at next 30m bar's open after confirmed signal close.
                  market entry; no intrabar; no partial fills.
Long stop       : compression_box_low[t] - S_buffer × compression_box_width[t]
Short stop      : compression_box_high[t] + S_buffer × compression_box_width[t]
                  S_buffer ∈ {0.10, 0.20} (axis 4)
Long target     : entry_price + T_mult × compression_box_width[t]
Short target    : entry_price - T_mult × compression_box_width[t]
                  T_mult ∈ {1.5, 2.0} (axis 5)
Time-stop       : 2 × N_comp 30m bars
                  (16 if N_comp=8; 24 if N_comp=12)
Stop-distance   : NO ATR-percentile gate in first-spec.
                  stop_distance_atr reported diagnostically only.
Stop precedence : stop > target > time-stop;
                  same-bar stop/target ambiguity = stop wins.
No break-even.  No trailing stop.  No regime exit.

Position sizing (preserved from §1.7.3 verbatim):
  risk_fraction       = 0.0025
  max_leverage        = 2.0
  max_positions       = 1
  no pyramiding       (subsequent candidates while positioned dropped)
  no reversal in pos  (opposite-direction signals while positioned dropped)
  BTCUSDT primary; ETHUSDT comparison only; ETH cannot rescue BTC.
```

## Opportunity-rate floors

Predeclared **before any data is touched**, derived from first principles, NOT from Phase 4r forensic numbers:

```text
min_candidate_transition_rate_BTC_OOS_HIGH:
  At least 1 candidate transition per 480 30m bars (~10 trading days at 30m).
  Implies ≥64 candidate transitions across the OOS window for the
  train-best variant.

min_executed_trade_count_BTC_OOS_HIGH:
  BTC OOS HIGH executed trade_count >= 30 (preserved from Phase 4q M3
  numeric).

min_executed_trade_count_train_best:
  BTC train-best variant on OOS HIGH must have trade_count >= 30.

min_variant_floor:
  At least 50% of the 32 variants must produce trade_count >= 30 on
  BTC OOS HIGH (otherwise CFP-1 triggers).

stop_distance_pass_rate:
  N/A in first-spec (no ATR-percentile stop-distance gate).
  stop_distance_atr reported diagnostically only.

sparse_intersection_collapse:
  CFP-9 enriched: triggers on candidate-transition rate floor failure
  OR train-best trade_count < 30 OR >50% variants below 30 trades.
```

## Threshold grid

**Exactly 32 variants over five binary axes (= 2^5).** Deterministic lexicographic ordering.

```text
Axis 1: N_comp     in {8, 12}
Axis 2: C_width    in {0.45, 0.60}
Axis 3: B_width    in {0.05, 0.10}
Axis 4: S_buffer   in {0.10, 0.20}
Axis 5: T_mult     in {1.5, 2.0}
```

**Fixed parameters (cardinality 1; not axes):**

```text
W_width                  = 240 30m bars
L_delay                  = 1 30m bar
close_location_long      = 0.70
close_location_short     = 0.30
T_stop_bars              = 2 × N_comp (structurally tied; NOT separate axis)
HTF gate                 = NONE
funding input            = NONE
volume input             = NONE (diagnostic only)
metrics OI               = NONE
ATR-percentile stop gate = NONE (stop_distance_atr diagnostic only)
break_even_rule          = disabled
ema_slope_method         = not_applicable
stagnation_window_role   = not_active
stop_trigger_domain      = trade_price_backtest (research)
risk_fraction            = 0.0025
max_leverage             = 2.0
max_positions            = 1
```

No grid extension. No grid reduction. All 32 variants reported in any future Phase 4w / 4x.

## Mechanism-check thresholds

```text
M1 — Contraction-state validity:
  C1_mean_R - non_contraction_mean_R >= +0.10R on BTC OOS HIGH
  AND bootstrap CI lower (B = 10 000) > 0.

M2 — Expansion-transition value-add:
  C1_mean_R - always_active_same_geometry_mean_R >= +0.05R on
  BTC OOS HIGH AND bootstrap CI lower > 0;
  AND C1_mean_R - delayed_breakout_mean_R >= 0 on BTC OOS HIGH.

M3 — Inside-spec co-design validity:
  BTC OOS HIGH mean_R > 0
  AND BTC OOS HIGH trade_count >= 30
  AND no CFP-1 / CFP-2 / CFP-3 trigger
  AND opportunity-rate floors satisfied.

M4 — Cross-symbol robustness:
  ETH OOS HIGH (G1-vs-baseline) differential non-negative
  AND directional consistency with BTC.
  ETH cannot rescue BTC; CFP-4 enforces.

M5 — Compression-box structural validity (DIAGNOSTIC ONLY in first-spec):
  Stops tied to compression-box invalidation behave better than a
  generic ATR-buffered structural stop on the same setup.
  Phase 4w may upgrade to binding gate if justified.

Promotion-bar:
  M1 PASS AND M2 PASS AND M3 PASS AND M4 PASS AND no CFP triggered.

Bootstrap:
  B = 10 000.
  RNG seed pinned in any future Phase 4w (recommended: 202604300).
```

## Negative-test specification

```text
Required (binding):
  non_contraction_breakout_baseline                 (M1)
  always_active_same_geometry_breakout_baseline     (M2)
  delayed_breakout_baseline                         (M2 detail)
  active_opportunity_rate_diagnostic                (M3 / CFP-9)

Optional (diagnostic only by default; Phase 4w may upgrade):
  random_contraction_baseline                       (specificity check)
```

If non-contraction or always-active baseline performs equally or better → C1 fails M1 / M2. If delayed-breakout outperforms transition-tied → transition-timing claim fails. If random-contraction performs similarly → contraction specificity is weak. If opportunity-rate collapses → CFP-9 triggers.

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
        Trigger if a small predeclared perturbation around any of
        the five structural axes causes a >0.20R degradation in
        OOS HIGH mean_R OR flips mean_R sign for the train-best variant.
        (Predeclared perturbation ranges in the Phase 4v memo.)

CFP-9   ENRICHED — Opportunity-rate / sparse-intersection collapse:
        Trigger if any of:
          - BTC OOS HIGH candidate-transition rate < 1 per 480 30m bars
            (i.e., <64 candidates across the OOS window for the
             train-best variant);
          - BTC OOS HIGH executed trade_count < 30 for the train-best
            variant;
          - >50% of 32 variants have BTC OOS HIGH trade_count < 30.

CFP-10  Forbidden optional ratio access:
        Trigger if any optional metrics ratio column is read.

CFP-11  ENRICHED — Lookahead / transition-dependency violation:
        Trigger if any of:
          - classifier or signal uses any bar with close_time >
            decision_time;
          - signal generated without prior contraction precondition
            (contraction_recently_active[t] = false);
          - entry fired >L_delay bars after contraction state ended;
          - same-bar AND-chain that consults the breakout-trigger
            of the same evaluation;
          - partial-bar consumption.

CFP-12  Data governance violation:
        Trigger if any of: metrics OI loaded; mark-price loaded
        (any timeframe); aggTrades loaded; spot / cross-venue loaded;
        non-binding manifest loaded; network I/O attempted; credentials
        / .env read; write attempted to data/raw/, data/normalized/,
        or data/manifests/; manifest modified; v003 created;
        private / authenticated REST / user-stream / WebSocket /
        listenKey path touched.
```

**Any single CFP triggered = Verdict C HARD REJECT** in any future Phase 4x backtest, unless a stop-condition / incomplete-methodology issue makes Verdict D more appropriate.

## Validation windows

Reused verbatim from Phase 4k:

```text
Train       : 2022-01-01 00:00:00 UTC .. 2023-06-30 23:30:00 UTC  (~18 months)
Validation  : 2023-07-01 00:00:00 UTC .. 2024-06-30 23:30:00 UTC  (~12 months)
OOS holdout : 2024-07-01 00:00:00 UTC .. 2026-03-31 23:30:00 UTC  (~21 months)
```

No window modification post-hoc. No data shuffling. No leakage. Same 32 variants evaluated independently per symbol; no cross-symbol optimization. ETH cannot rescue BTC.

## Recommended next operator choice

- **Option A — primary recommendation:** Phase 4w — C1 Backtest-Plan Memo (docs-only). Phase 4w would translate the Phase 4v C1 strategy spec into a precise, reproducible, fail-closed future Phase 4x backtest methodology, mirroring Phase 4q's discipline (NOT V2 / G1 numeric thresholds).
- **Option B — conditional secondary:** remain paused.

**Phase 4w is NOT started by this merge.** Phase 4w execution requires a separate explicit operator authorization brief.

NOT recommended:

- immediate C1 backtest — REJECTED;
- immediate C1 implementation — REJECTED;
- data acquisition — REJECTED;
- paper / shadow / live-readiness — FORBIDDEN;
- Phase 4 canonical — FORBIDDEN;
- production-key creation / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials — FORBIDDEN;
- exchange-write capability — FORBIDDEN;
- any G1 / V2 / R2 / F1 / D1-A rescue — FORBIDDEN.

## Verification evidence

Quality gates verified clean during Phase 4v and across the merge:

```text
ruff check .   : All checks passed!
pytest         : 785 passed (no regressions)
mypy           : Success: no issues found in 82 source files
```

No code, tests, scripts, data, or manifests were modified by Phase 4v; the quality gates simply confirm that the documentation-only changes did not regress the repository.

## Forbidden-work confirmation

Phase 4v and this merge did NOT do any of the following:

- start Phase 4w or any successor phase;
- create a C1 backtest-plan memo;
- run a backtest;
- write any code;
- create any script;
- modify any source under `src/prometheus/`;
- modify any test;
- modify any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`);
- modify `data/raw/` / `data/normalized/` / `data/manifests/`;
- commit `data/research/` outputs;
- acquire data;
- download data;
- patch / forward-fill / interpolate / regenerate / replace data;
- create v003;
- use metrics OI as a hypothesis input;
- use optional metrics ratio columns;
- use 5m Q1–Q7 findings as rule candidates;
- use V2 Phase 4l stop-distance failure numbers to choose thresholds;
- use Phase 4r G1 active-fraction numbers to choose thresholds;
- use the G1 always-active 124-trade / −0.34 mean_R result as a candidate-tuning target;
- modify Phase 4p G1 strategy-spec selections;
- modify Phase 4q methodology;
- modify Phase 4j §11 governance;
- modify Phase 4k methodology;
- revise retained verdicts;
- revise project locks, thresholds, parameters, or governance rules;
- change §11.6 / §1.7.3 / Phase 3r governance / Phase 3v governance / Phase 3w governance / Phase 4j governance / Phase 4k methodology;
- start Phase 4 canonical;
- implement reconciliation;
- implement a real exchange adapter;
- implement exchange-write capability;
- place or cancel orders;
- use / request / store credentials;
- add authenticated REST / private endpoints / public endpoint clients / user stream / WebSocket / listenKey lifecycle;
- enable MCP / Graphify or modify `.mcp.json`;
- create `.env` files;
- deploy anything;
- create paper / shadow runtime;
- imply live-readiness.

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
Phase 4v                    : C1 strategy-spec memo (this phase; merged)
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
