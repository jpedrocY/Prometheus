# Phase 4p Merge Closeout

## Summary

Phase 4p — G1 Strategy-Spec Memo (docs-only) — has been merged into `main` via a no-fast-forward merge commit. Phase 4p translates the Phase 4o G1 — Regime-First Breakout Continuation hypothesis-spec layer into a complete ex-ante strategy specification with exact thresholds across all dimensions (timeframes; composite regime classifier; 4-state regime state machine; inside-regime breakout setup; structural stop with active-regime-derived bounds; fixed-R target; time-stop; position sizing; cost cells; 32-variant threshold grid over 5 binary axes; M1 / M2 / M3 / M4 mechanism-check numeric thresholds; 12 catastrophic-floor predicates; validation windows reused verbatim from Phase 4k; BTCUSDT-primary / ETHUSDT-comparison protocol; stop-trigger-domain and Phase 3w break-even / EMA / stagnation governance labels). Phase 4p also included a small docs-only consistency correction commit clarifying that N_R = 2.0 and T_stop = 16 are fixed (not active Phase 4p threshold-grid axes) and that N_R ∈ {2.0, 2.5} / T_stop ∈ {12, 16} remain only as future G1-extension possibilities requiring separate operator authorization and predeclaration before data is touched. Phase 4p was docs-only. No source code, tests, scripts, data, manifests, or successor memos were created or modified.

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4p_g1-strategy-spec-memo.md   (added by merge)
docs/00-meta/implementation-reports/2026-04-30_phase-4p_closeout.md                 (added by merge)
docs/00-meta/implementation-reports/2026-04-30_phase-4p_merge-closeout.md           (added by housekeeping commit — this file)
docs/00-meta/current-project-state.md                                               (modified by housekeeping commit — narrow Phase 4p paragraph + "Current phase" / "Most recent merge" refresh)
```

No other files modified by Phase 4p or by this merge.

## Phase 4p commits included

```text
50d40da2ef434c7c21c5d0e9d4270d6b4304e0c7   phase-4p: G1 strategy-spec memo (docs-only)
20b577be2a291fd0ad3c0beb42e627e112f78fdd   phase-4p: closeout (G1 strategy-spec memo, docs-only)
0572c1c1ab1282b69df04f02b97b97fec6edd877   docs(phase-4p): clarify fixed target/time-stop versus 32-variant grid
```

## Merge commit

```text
ddfaf0f579d1c2ed99da0abc6480ee79496b6240   Merge Phase 4p (G1 strategy-spec memo, docs-only) into main
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

- Phase 4p was docs-only.
- Phase 4p defines G1 — Regime-First Breakout Continuation as a complete ex-ante strategy specification with all thresholds locked.
- G1 remains pre-research only: not implemented; not backtested; not validated; not live-ready; not a rescue of R3 / R2 / F1 / D1-A / V2.
- Phase 4p does **not** authorize Phase 4q.
- Phase 4p does **not** authorize a backtest, an implementation, data acquisition, paper / shadow / live, or exchange-write.
- No retained verdict is revised by Phase 4p.
- No project lock is changed by Phase 4p.

## Consistency correction summary

- Correction commit `0572c1c1ab1282b69df04f02b97b97fec6edd877` resolved a docs-only target / time-stop axis-vs-fixed-value inconsistency in three locations of the Phase 4p memo (Summary; Target model section; Time-stop model section). The closeout file already correctly recorded the fixed values; no edit was required there.
- G1 first-spec active values are now consistently recorded as:
  - **N_R = 2.0 fixed** (not an active Phase 4p threshold-grid axis);
  - **T_stop = 16 completed 30m bars fixed** (not an active Phase 4p threshold-grid axis);
  - **32 variants total over exactly five binary axes** (E_min, ATR band, V_liq_min, funding band, K_confirm).
- N_R ∈ {2.0, 2.5} and T_stop ∈ {12, 16} are preserved only as **future G1-extension possibilities**, not active Phase 4p axes. They may be activated only via a separately authorized G1-extension memo with predeclaration before any data is touched.

## Strategy name

```text
G1 — Regime-First Breakout Continuation
```

## Data requirements decision

- **No Phase 4q data-requirements memo required** before any future backtest-plan memo. Existing data is sufficient.
- Existing data sufficient:
  - v002 BTCUSDT 15m;
  - v002 ETHUSDT 15m;
  - v002 BTCUSDT 1h-derived;
  - v002 ETHUSDT 1h-derived;
  - Phase 4i `binance_usdm_btcusdt_30m__v001`;
  - Phase 4i `binance_usdm_ethusdt_30m__v001`;
  - Phase 4i `binance_usdm_btcusdt_4h__v001`;
  - Phase 4i `binance_usdm_ethusdt_4h__v001`;
  - v002 BTCUSDT funding history;
  - v002 ETHUSDT funding history.
- No new acquisition.
- No manifest modification.
- **G1 first spec does NOT use Phase 4i metrics OI subset.** Phase 4j §11 metrics OI-subset partial-eligibility governance is preserved verbatim but unused by G1 first spec.

## Data inputs

Allowed:

- v002 trade-price klines (15m, 1h-derived) for BTCUSDT and ETHUSDT.
- Phase 4i trade-price klines (30m, 4h) for BTCUSDT and ETHUSDT (research-eligible per Phase 4i).
- v002 funding-rate history for BTCUSDT and ETHUSDT.

Forbidden as G1 first-spec inputs:

- mark-price 30m / 4h;
- mark-price 5m;
- mark-price 15m;
- aggTrades;
- spot data;
- cross-venue data;
- Phase 4i metrics OI subset (governance preserved but unused);
- optional metrics ratio columns (Phase 4j §11.3 forbidden);
- v003 (no v003 created);
- modified Phase 4i / v002 / v001-of-5m manifests;
- authenticated REST / private endpoints / public endpoints in code / user stream / WebSocket / listenKey lifecycle;
- 5m Q1–Q7 diagnostic outputs as strategy features or regime indicators (Phase 3o §6 / Phase 3t §14.2 preserved);
- V2 Phase 4l observed stop-distance failure numbers as design inputs.

## Timeframes

```text
Regime classifier primary timeframe          : 4h
Regime persistence support timeframe         : 1h
Signal timeframe                             : 30m
Entry                                        : at next 30m bar's open after confirmed setup close
Diagnostic-only (not authorized as G1 input) : 5m
```

## Regime classifier formula

Composite classifier on prior-completed bars only, independent of breakout signal:

- 4h EMA(20) / EMA(50) discrete-comparison trend state (`ema_slope_method = discrete_comparison`; Phase 3w §7 preserved).
- 12-bar 4h directional efficiency.
- 30m ATR(20) percentile rank computed over the prior 480 30m bars (10 days).
- 30m relative-volume score vs. the prior 480-bar 30m volume median.
- v002 funding-rate percentile computed over the trailing 90 funding events.

All computed on prior-completed data only. Classifier is independent of any breakout signal evaluation; classifier outputs feed the regime state machine.

## Regime state machine

```text
States:
  regime_inactive
  regime_candidate
  regime_active
  regime_cooldown

Confirmation length:
  K_confirm  in {2, 3}           (axis 5 of threshold grid; consecutive 4h bars)

Cooldown length:
  C_cooldown = 4                 (completed 4h bars; fixed)

Rules:
  - No entries are evaluated outside regime_active.
  - Position lifecycle is independent of regime state after entry
    (Option A: position continues under its own stop / target / time-stop
    rules even if the regime later transitions to cooldown / inactive).
```

## Inside-regime breakout setup

- Evaluated **only** while regime is `regime_active`.
- Entry direction must match active regime direction (LONG-regime-only long entries; SHORT-regime-only short entries).
- 30m Donchian-style breakout:
  - `N_breakout = 12` (lookback in 30m bars).
  - `B_atr = 0.10` (ATR-buffer multiplier).
- Prior high / low excludes the current bar (`high[t-N_breakout..t-1]` and `low[t-N_breakout..t-1]`).
- **No V2 8-feature AND chain.**
- **No R2 pullback-retest.**
- **No F1 mean-reversion.**
- **No D1-A funding-Z-score directional rule.**
- **No 5m features.**

## Stop / target / sizing model

```text
Initial structural stop:
  N_stop      = 12 30m bars
  S_buffer    = 0.10
  long  stop  = min(low[t-N_stop..t-1])  - S_buffer * ATR(20, t)
  short stop  = max(high[t-N_stop..t-1]) + S_buffer * ATR(20, t)

Stop-distance bounds (G1-specific; NOT V1 / V2 inheritance):
  [0.50, 2.20] x ATR(20)
  Out-of-band setups rejected at entry; no stop widening; no V2-stop-distance rescue.

Target:
  N_R          = 2.0  (single fixed value; not a Phase 4p threshold-grid axis)

Time-stop:
  T_stop       = 16 completed 30m bars  (single fixed value; not a Phase 4p
                                         threshold-grid axis; = 8h)

Exit-rule discipline:
  no break-even
  no trailing stop
  same-bar stop / take-profit ambiguity = stop-first conservative
  stop-precedence within a single bar: stop > take-profit > time-stop

Position sizing (preserved verbatim from Section 1.7.3):
  risk_fraction       = 0.0025  (0.25% per trade)
  max_leverage        = 2.0     (2x cap)
  max_positions       = 1
  max_active_stops    = 1
  symbol scope        = BTCUSDT primary; ETHUSDT comparison only
                         (ETH cannot rescue BTC)
  symbol_lot_size     = exchange-rounded down; below-min rejects
```

## Threshold grid

**Exactly 32 variants total.** Five binary axes only:

```text
Axis 1: E_min          in {0.30, 0.40}
Axis 2: ATR band       in {[20, 80], [30, 70]}
Axis 3: V_liq_min      in {0.80, 1.00}
Axis 4: funding band   in {[15, 85], [25, 75]}
Axis 5: K_confirm      in {2, 3}
```

All other parameters (N_breakout, B_atr, N_stop, S_buffer, stop-distance bounds, N_R, T_stop, C_cooldown, HTF EMA pair, ATR period, percentile lookbacks, liquidity lookback, funding lookback) are fixed at the Phase 4p values and are NOT axes.

- Deterministic lexicographic variant ordering (axis name then axis value).
- No grid extension without separate operator authorization and predeclaration before data is touched.
- N_R ∈ {2.0, 2.5} and T_stop ∈ {12, 16} are NOT Phase 4p axes; they are reserved as future G1-extension possibilities only.

## Mechanism-check thresholds

```text
M1 — Regime-validity negative test:
  Pass: G1 active-population mean_R minus G1 inactive-population mean_R
        >= +0.10R AND bootstrap_CI_lower(B = 10 000) > 0.

M2 — Regime-gating value-add (G1 vs always-active baseline):
  Pass: G1 mean_R minus always-active-baseline mean_R
        >= +0.05R on BTC OOS HIGH AND bootstrap_CI_lower(B = 10 000) > 0.

M3 — Inside-regime co-design validity:
  Pass: BTC OOS HIGH mean_R > 0 AND trade_count >= 30.

M4 — Cross-symbol robustness:
  Pass: ETH OOS HIGH mean_R differential non-negative AND directional
        consistency with BTC.
  ETH cannot rescue BTC.

Promotion-bar:  M1 PASS AND M2 PASS AND M3 PASS AND M4 PASS AND
                Section 11.6 HIGH cost-survival AND no CFP triggered.
```

## Catastrophic-floor predicates

Twelve predicates predeclared (CFP-1 .. CFP-12; G1-specific values defined exactly by the Phase 4p memo):

```text
CFP-1   Insufficient trade count (>50% variants below trade_count = 30 on
        OOS BTC HIGH).
CFP-2   Negative OOS expectancy under HIGH cost (any active variant with
        OOS BTC HIGH mean_R <= -0.20R).
CFP-3   Catastrophic drawdown / profit_factor (max_drawdown_R > 10R or
        profit_factor < 0.50 on OOS BTC HIGH).
CFP-4   BTC fails / ETH passes (M3 BTC FAIL AND M4 ETH PASS — ETH cannot
        rescue BTC).
CFP-5   Train-only success / OOS failure (train BTC HIGH > 0 / OOS BTC HIGH
        <= 0).
CFP-6   Excessive PBO (PBO > 0.50 on grid).
CFP-7   Regime / month overconcentration (any single calendar month >50% of
        OOS trades).
CFP-8   Sensitivity-cell failure (exclude-entire-affected-days sensitivity
        cell mean_R degrades by > 0.20R vs main cell).
CFP-9   Excluded-bar-fraction anomaly (>5% of evaluable bars).
CFP-10  Optional-ratio-column access detected (Phase 4j Section 11.3
        forbidden).
CFP-11  Per-bar exclusion algorithm deviation from Phase 4j Section 16.
CFP-12  Forbidden data access (private endpoints / authenticated REST /
        user-stream / spot / cross-venue / mark-price 30m / aggTrades).
```

**Any single CFP triggered = HARD REJECT (Verdict C-equivalent), terminal for G1 first-spec.**

## Validation windows

Reused verbatim from Phase 4k:

```text
Train          :  2022-01-01 00:00:00 UTC .. 2023-06-30 23:30:00 UTC  (~18 months)
Validation     :  2023-07-01 00:00:00 UTC .. 2024-06-30 23:30:00 UTC  (~12 months)
OOS holdout    :  2024-07-01 00:00:00 UTC .. 2026-03-31 23:30:00 UTC  (~21 months;
                                                                      primary G1 evidence cell)
```

No window modification post-hoc. No data shuffling. No leakage. Same 32 variants evaluated independently per symbol; no cross-symbol optimization. ETH cannot rescue BTC.

## Recommended next operator choice

- **Option A — primary recommendation:** Phase 4q — G1 Backtest-Plan Memo (docs-only). Phase 4q would translate the Phase 4p G1 strategy spec into a precise predeclared backtest methodology mirroring Phase 4k's structure (per-feature implementation plans; regime classifier code structure; setup detection algorithm; entry / exit execution model; cost-cell handling; threshold-grid handling policy; deterministic variant ordering; required reporting tables; required plot artefacts; stop conditions; reproducibility requirements; standalone-script pattern at `scripts/phase4r_g1_backtest.py`).
- **Option B — conditional secondary:** remain paused.

**Phase 4q is NOT started by this merge.** Immediate G1 backtest execution is REJECTED (data-snooping risk per Bailey / Borwein / López de Prado / Zhu 2014; Phase 4l Verdict C HARD REJECT showed the cost of insufficient methodology predeclaration). G1 implementation is REJECTED. Paper / shadow / live / exchange-write is FORBIDDEN.

## Verification evidence

Quality gates verified clean during Phase 4p (across the memo commit, the closeout commit, and the consistency-correction commit):

```text
ruff check .   : All checks passed!
pytest         : 785 passed in 13.79s (no regressions)
mypy           : Success: no issues found in 82 source files
```

No code, tests, scripts, data, or manifests were modified by Phase 4p; the quality gates simply confirm that the documentation-only changes did not regress the repository.

## Forbidden-work confirmation

Phase 4p and this merge did NOT do any of the following:

- start Phase 4q or any successor phase;
- create G1 backtest code;
- run a G1 backtest;
- create V3 or any runnable strategy;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- run diagnostics;
- run acquisition scripts;
- modify `src/prometheus` code;
- modify tests;
- modify scripts;
- modify `data/raw`;
- modify `data/normalized`;
- modify `data/manifests`;
- commit `data/research` outputs;
- acquire data;
- download data;
- patch / forward-fill / interpolate / regenerate / modify data;
- create v003;
- modify Phase 4g V2 strategy-spec selections;
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
R2                  : FAILED — Section 11.6 cost-sensitivity blocks (preserved)
F1                  : HARD REJECT (preserved)
D1-A                : MECHANISM PASS / FRAMEWORK FAIL — other (preserved)
V2                  : HARD REJECT (Phase 4l terminal for first-spec; preserved)
G1                  : pre-research only; strategy-spec defined in Phase 4p;
                      not implemented; not backtested; not validated;
                      not live-ready
Section 11.6        : 8 bps HIGH per side (preserved verbatim)
Section 1.7.3       : 0.25% risk / 2x leverage / 1 position / mark-price stops
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
Phase 4f                    : V2 hypothesis predeclaration (preserved)
Phase 4g                    : V2 strategy spec (preserved)
Phase 4h                    : V2 data-requirements / feasibility memo
                              (preserved)
Phase 4i                    : V2 acquisition + integrity report; metrics
                              manifests research_eligible: false (preserved)
Phase 4j §11                : metrics OI-subset partial-eligibility binding
                              rule (preserved; unused by G1)
Phase 4k                    : V2 backtest-plan methodology (preserved)
Phase 4l                    : V2 backtest execution; Verdict C HARD REJECT
                              (preserved)
Phase 4m                    : post-V2 strategy research consolidation memo;
                              18-requirement validity gate (preserved)
Phase 4n                    : fresh-hypothesis discovery memo;
                              Candidate B selected (preserved)
Phase 4o                    : G1 hypothesis-spec layer (preserved)
Phase 4p                    : G1 strategy-spec memo (this phase; merged)
Recommended state           : paused (outside conditional Phase 4q)
```

## Next authorization status

```text
Phase 4q                       : NOT authorized
Phase 4r                       : NOT authorized
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
G1 implementation              : NOT authorized
G1 backtest execution          : NOT authorized
G1 data acquisition            : NOT authorized (none required; existing data sufficient)
G1 backtest-plan memo          : NOT authorized (Phase 4q recommended next; not yet authorized)
G1-prime / G1-extension axes   : NOT authorized; not proposed
V2-prime / V2-variant          : NOT authorized; not proposed
Retained-evidence rescue       : NOT authorized; not proposed
5m strategy / hybrid           : NOT authorized; not proposed
ML feasibility                 : NOT authorized; not proposed
New family research            : NOT authorized beyond Phase 4n Candidate B (G1)
```

The next step is operator-driven: the operator decides whether to authorize Phase 4q (G1 Backtest-Plan Memo, docs-only) or remain paused. Until then, the project remains at the post-Phase-4p G1 strategy-spec boundary.

---

**Phase 4p was docs-only. No source code, tests, scripts, data, manifests, or successor phases were created or modified. Recommended state remains paused outside conditional Phase 4q. No next phase authorized.**
