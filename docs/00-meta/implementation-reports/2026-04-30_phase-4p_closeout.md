# Phase 4p Closeout — G1 Strategy-Spec Memo (docs-only)

## Summary

Phase 4p translated the Phase 4o G1 hypothesis-spec layer into a complete ex-ante strategy specification with exact thresholds across all dimensions before any G1 backtest code, data acquisition, or execution exists. The memo predeclares the G1 — Regime-First Breakout Continuation strategy as a precise, bounded, structurally-distinct hypothesis with a 32-variant threshold grid, a 4-state regime state machine, a composite regime classifier across five dimensions (HTF trend, trend persistence, volatility regime, liquidity, funding pathology), an inside-regime breakout setup, a structural stop with bounds derived from active-regime structure, a fixed-R target, a time-stop, position sizing preserved from §1.7.3, cost cells preserved from §11.6 verbatim, M1 / M2 / M3 / M4 mechanism-check numeric thresholds, twelve catastrophic-floor predicates, and validation windows reused verbatim from Phase 4k. Phase 4p was docs-only. No source code, tests, scripts, data, manifests, or successor memos were created or modified.

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4p_g1-strategy-spec-memo.md   (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4p_closeout.md                 (new — this file)
```

No other files modified by Phase 4p.

## Strategy-spec conclusion

G1 — Regime-First Breakout Continuation is now fully specified as a bounded, predeclared, ex-ante strategy hypothesis with all thresholds locked. G1 is structurally distinct from R3 / R2 / F1 / D1-A / V2 along the regime-as-primary categorical dimension: G1 only operates inside a confirmed regime; the regime classifier is the gating primary, not a filter; the breakout setup is the secondary inside-regime trigger; setup-stop-target-sizing co-design is preserved; ETH cannot rescue BTC. The 32-variant threshold grid (2^5 binary axes) keeps PBO / DSR / CSCV computation tractable and avoids V2-style overbreadth. Mechanism-check numeric thresholds (M1 ≥ +0.10R active-vs-inactive; M2 ≥ +0.05R G1-vs-always-active at HIGH cost; M3 BTC OOS HIGH mean_R > 0 with ≥ 30 trades; M4 ETH non-negative differential with directional consistency) and twelve catastrophic-floor predicates are predeclared. G1 is pre-research only: not implemented; not backtested; not validated; not live-ready; not a rescue of R3 / R2 / F1 / D1-A / V2.

## Strategy name

```text
G1 — Regime-First Breakout Continuation
```

## Data requirements decision

Reuse Phase 4i acquired research-eligible datasets without modification, plus Phase 4j §11 metrics OI-subset partial-eligibility rule, plus existing v002 funding history. No new acquisition, no mark-price 30m / 4h, no aggTrades, no new dataset family required by Phase 4p. Specifically:

- `binance_usdm_btcusdt_30m__v001` (research-eligible per Phase 4i)
- `binance_usdm_ethusdt_30m__v001` (research-eligible per Phase 4i)
- `binance_usdm_btcusdt_4h__v001` (research-eligible per Phase 4i)
- `binance_usdm_ethusdt_4h__v001` (research-eligible per Phase 4i)
- BTCUSDT and ETHUSDT 1h derivable from existing 30m via on-the-fly resampling (no new acquisition)
- `binance_usdm_btcusdt_metrics__v001` and `binance_usdm_ethusdt_metrics__v001` used only via Phase 4j §11 OI subset (per-bar exclusion algorithm preserved verbatim)
- v002 funding history reused per Phase 4h §22

## Timeframes

```text
Regime classifier:    4h
Signal:               30m (inside-regime breakout)
Support:              1h (used only when needed for liquidity / volume context;
                          in current spec, no 1h-specific feature is active)
Diagnostic-only:      5m (not authorized as primary signal layer)
```

## Regime classifier formula

Composite AND across five dimensions, evaluated on completed bars only:

```text
regime_long_candidate(bar_t)  := all of:
  - HTF_trend_state(bar_t)             == LONG
  - directional_efficiency(bar_t, 12)  >= E_min
  - ATR(20)_percentile(bar_t)          in [P_atr_low, P_atr_high]
  - liquidity_score(bar_t)             >= V_liq_min
  - funding_pathology(bar_t)           in [P_fund_low, P_fund_high]

regime_short_candidate(bar_t) := all of:
  - HTF_trend_state(bar_t)             == SHORT
  - directional_efficiency(bar_t, 12)  >= E_min
  - ATR(20)_percentile(bar_t)          in [P_atr_low, P_atr_high]
  - liquidity_score(bar_t)             >= V_liq_min
  - funding_pathology(bar_t)           in [P_fund_low, P_fund_high]
```

Definitions:

```text
HTF_trend_state          :=  4h EMA(20) vs 4h EMA(50) discrete-comparison state
                              (Phase 3w break-even/EMA-slope rule preserved:
                               ema_slope_method = discrete_comparison)
directional_efficiency   :=  abs(close[t] - close[t-12]) / sum(|close[k] - close[k-1]|, k=t-11..t)
                              over the trailing 12 4h bars; in [0, 1]
ATR(20)_percentile       :=  rolling 30m ATR(20) percentile rank within trailing
                              90-day distribution
liquidity_score          :=  30m relative volume vs trailing 30m baseline
funding_pathology        :=  trailing 90-day funding-rate Z-score percentile
```

## Regime state machine

Four states with deterministic transitions on completed-bar evaluation only:

```text
Initial state:  regime_inactive

regime_inactive
  + regime_long_candidate  : true on bar_t  -> regime_candidate (direction = LONG, candidate_count = 1)
  + regime_short_candidate : true on bar_t  -> regime_candidate (direction = SHORT, candidate_count = 1)

regime_candidate (direction D, candidate_count C)
  + regime_<D>_candidate true     -> regime_candidate (candidate_count = C+1) ;
                                     if C+1 >= K_confirm -> regime_active (direction = D)
  + regime_<D>_candidate false    -> regime_inactive (candidate cleared)

regime_active (direction D)
  + regime_<D>_candidate true     -> regime_active (continue)
  + regime_<D>_candidate false    -> regime_cooldown (direction = D, cooldown_count = 1)

regime_cooldown (direction D, cooldown_count C)
  + cooldown_count < C_cooldown   -> regime_cooldown (cooldown_count = C+1)
  + cooldown_count >= C_cooldown  -> regime_inactive (cooldown cleared)

K_confirm   in {2, 3}   4h bars
C_cooldown  = 4         4h bars
```

Position-vs-regime: Option A (independent lifecycle once entered). A position opened while regime is active continues under its own stop / target / time-stop rules even if the regime later transitions to cooldown / inactive. Inside-regime breakout entries are only permitted while the regime is in `regime_active`.

## Inside-regime breakout setup

Evaluated on completed 30m bars only, only while regime is `regime_active`:

```text
N_breakout      = 12  30m bars (Donchian-style high/low lookback)
B_atr           = 0.10  ATR-buffer multiplier

setup_long(bar_t)   := regime_active(direction=LONG)  AND
                       close[t] > max(high[t-N_breakout..t-1]) + B_atr * ATR(20, t)

setup_short(bar_t)  := regime_active(direction=SHORT) AND
                       close[t] < min(low[t-N_breakout..t-1])  - B_atr * ATR(20, t)
```

Entry on the next 30m bar's open after a confirmed setup close. Completed-bar discipline preserved.

## Stop / target / sizing model

```text
Initial structural stop:
  N_stop      = 12   30m bars
  S_buffer    = 0.10 ATR-buffer multiplier
  long  stop  = min(low[t-N_stop..t-1])  - S_buffer * ATR(20, t)
  short stop  = max(high[t-N_stop..t-1]) + S_buffer * ATR(20, t)

Stop-distance bounds:
  [0.50, 2.20] x ATR(20, t)
  Bounds derived from active-regime structural lookback; out-of-band setups
  rejected at entry (no stop widening).

Target:
  N_R         = 2.0   (single value; fixed-R take-profit at +2.0R from entry)

Time-stop:
  T_stop      = 16   30m bars (8 hours; unconditional close at next 30m open
                     after T_stop bars elapsed since entry)

Stop precedence (within a single bar):  stop > take-profit > time-stop
Conservative tie-break:                  stop-first

Position sizing (preserved verbatim from Section 1.7.3):
  risk_fraction        = 0.0025  (0.25% of sizing equity)
  max_leverage         = 2.0     (2x cap)
  max_positions        = 1
  max_active_stops     = 1
  symbol_lot_size      = exchange-rounded down; below-min rejects
```

Stop-trigger-domain governance: research = `trade_price_backtest`; future runtime = `mark_price_runtime`; future mark-price validation = `mark_price_backtest_candidate`; `mixed_or_unknown` invalid / fail-closed.

## Threshold grid

32 variants (2^5) over 5 binary axes:

```text
Axis 1: E_min          in {0.30, 0.40}
Axis 2: ATR band       in {[20, 80], [30, 70]}
Axis 3: V_liq_min      in {0.80, 1.00}
Axis 4: funding band   in {[15, 85], [25, 75]}
Axis 5: K_confirm      in {2, 3} 4h bars
```

Fixed values (not in grid):

```text
N_breakout    = 12
B_atr         = 0.10
N_stop        = 12
S_buffer      = 0.10
N_R           = 2.0
T_stop        = 16
C_cooldown    = 4
```

Total: 32 variant × 2 symbols × 3 cost cells = 192 simulation cells (vs. V2's 3 072). Deterministic lexicographic variant ordering. No outcome-driven reduction.

## Mechanism-check thresholds

```text
M1 — Regime-validity negative test:
  Compute G1 candidate-trigger-only equivalent population (breakout fired
  without regime gate) over OOS BTC HIGH cost cell.
  Pass: (G1_active_only_mean_R - G1_inactive_only_mean_R) >= +0.10R
        AND bootstrap_CI_lower(B=10000) > 0.0
  Fail: differential below threshold OR CI crosses zero OR sample insufficient

M2 — Regime-gating value-add (vs always-active breakout):
  Pass: (G1_mean_R - always_active_breakout_mean_R) >= +0.05R
        on BTC OOS HIGH AND bootstrap_CI_lower(B=10000) > 0.0
  Fail: regime gate adds no marginal expectancy under HIGH cost

M3 — Inside-regime co-design validity:
  Pass: BTC OOS HIGH mean_R > 0.0 AND trade_count >= 30
  Fail: BTC OOS HIGH expectancy <= 0 OR trade_count < 30

M4 — Cross-symbol robustness:
  Pass: ETH OOS HIGH (G1_mean_R - inactive_baseline_mean_R) >= 0.0
        AND directional consistency with BTC (same sign of differential)
  Fail: ETH negative differential OR opposite directional sign vs BTC

Promotion-bar:  M1 PASS AND M2 PASS AND M3 PASS AND M4 PASS AND
                Section 11.6 HIGH cost-survival AND no CFP triggered
```

## Catastrophic-floor predicates

Twelve CFPs predeclared (G1-specific values):

```text
CFP-1   Insufficient trade count:  any window with active variants having
        OOS_BTC_HIGH trade_count < 30 across > 50% of grid -> reject
CFP-2   Negative OOS expectancy under HIGH cost:  any active variant with
        OOS_BTC_HIGH mean_R <= -0.20R -> reject
CFP-3   Catastrophic drawdown:  any active variant with max_drawdown_R > 10R
        OR profit_factor < 0.50 on OOS_BTC_HIGH -> reject
CFP-4   BTC-fails-with-ETH-passes:  M3 BTC FAIL AND M4 ETH PASS -> reject
        (ETH cannot rescue BTC)
CFP-5   Train-only success with OOS failure:  train BTC HIGH mean_R > 0 BUT
        OOS BTC HIGH mean_R <= 0 -> reject
CFP-6   Excessive PBO:  PBO > 0.50 on grid -> reject
CFP-7   Regime/month overconcentration:  any single calendar month accounting
        for > 50% of total OOS trades -> reject
CFP-8   Sensitivity-cell failure:  exclude-entire-affected-days sensitivity
        cell shows mean_R degradation > 0.20R vs main cell -> reject
CFP-9   Excluded-bar-fraction anomaly:  metrics OI per-bar exclusion fraction
        > 5% of evaluable bars -> reject
CFP-10  Optional-ratio-column access detected (Phase 4j §11.3 forbidden) -> reject
CFP-11  Per-bar exclusion algorithm deviation from Phase 4j §16 -> reject
CFP-12  Forbidden data access (private endpoints / authenticated REST /
        user-stream / spot data / cross-venue data / mark-price 30m /
        aggTrades) -> reject
```

Any CFP triggered = HARD REJECT (Verdict C-equivalent), terminal for G1 first-spec.

## Validation windows

Reused verbatim from Phase 4k:

```text
Train          :  2022-01-01 00:00:00 UTC .. 2023-06-30 23:30:00 UTC  (~18 months)
Validation     :  2023-07-01 00:00:00 UTC .. 2024-06-30 23:30:00 UTC  (~12 months)
OOS holdout    :  2024-07-01 00:00:00 UTC .. 2026-03-31 23:30:00 UTC  (~21 months;
                                                                      primary G1 evidence cell)
```

No window modification post-hoc. No data shuffling. No leakage. Optional walk-forward extension: 4 rolling 12-month OOS windows (justify if omitted). BTCUSDT primary / ETHUSDT comparison only — same 32 variants evaluated independently per symbol; no cross-symbol optimization.

## Recommended next operator choice

Phase 4q G1 Backtest-Plan Memo (docs-only) — primary recommendation. Phase 4q would translate the Phase 4p G1 strategy spec into a precise predeclared backtest methodology mirroring Phase 4k's structure: per-feature implementation plans; regime classifier code structure; setup detection algorithm; entry / exit execution model; cost-cell handling; threshold-grid handling policy (Option B — full PBO / DSR / CSCV with 32 variants, no further reduction); deterministic lexicographic variant ordering; required reporting tables (regime-active / regime-inactive trade summaries; M1 / M2 / M3 / M4 tables; PBO; DSR; CSCV S=16 sub-sample rankings; metrics-OI exclusion table; main-vs-sensitivity cell comparison; trade distribution by year / month / regime-state; verdict declaration; forbidden-work confirmation); required plot artefacts; stop conditions; reproducibility requirements; standalone-script pattern at `scripts/phase4r_g1_backtest.py`.

Conditional secondary: remain paused.

NOT recommended: Phase 4q immediate G1 backtest execution skipping the backtest-plan memo (data-snooping risk per Bailey / Borwein / López de Prado / Zhu 2014; Phase 4l Verdict C HARD REJECT showed the cost of insufficient methodology predeclaration); revise G1 strategy spec post-hoc; immediate G1 implementation; paper / shadow / live-readiness / exchange-write FORBIDDEN.

Phase 4q execution is **NOT** authorized by this Phase 4p memo or this closeout. Phase 4q execution would require a separate explicit operator authorization brief.

## Commands run

```text
git status
git rev-parse main
git rev-parse origin/main
.venv/Scripts/python --version
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m pytest -q
.venv/Scripts/python -m mypy
git add docs/00-meta/implementation-reports/2026-04-30_phase-4p_g1-strategy-spec-memo.md
git commit -m "phase-4p: G1 strategy-spec memo (docs-only)"
git push -u origin phase-4p/g1-strategy-spec-memo
```

## Verification results

```text
Python version       : 3.12.4
ruff check .         : All checks passed!
pytest -q            : 785 passed in 13.87s (no regressions)
mypy                 : Success: no issues found in 82 source files
git status (initial) : clean working tree (Phase 4p memo and closeout untracked
                       prior to staging; .claude/scheduled_tasks.lock and
                       data/research/ untracked-but-gitignored)
git rev-parse main          : 74eda85d8b3ae55c7944de2d883eeece0f24da65
git rev-parse origin/main   : 74eda85d8b3ae55c7944de2d883eeece0f24da65
```

Whole-repo quality gates remain clean. No regressions vs. main HEAD.

## Commit

```text
Phase 4p memo commit:      50d40da2ef434c7c21c5d0e9d4270d6b4304e0c7
Phase 4p closeout commit:  <recorded after this file is committed>
```

## Final git status

(recorded after closeout commit and push)

## Final git log --oneline -5

(recorded after closeout commit and push)

## Final rev-parse

```text
HEAD                                       : <recorded after closeout commit>
origin/phase-4p/g1-strategy-spec-memo      : <recorded after closeout push>
main                                       : 74eda85d8b3ae55c7944de2d883eeece0f24da65 (unchanged)
origin/main                                : 74eda85d8b3ae55c7944de2d883eeece0f24da65 (unchanged)
```

## Branch / main status

`main` remains unchanged at `74eda85d8b3ae55c7944de2d883eeece0f24da65`. Phase 4p was authored exclusively on the `phase-4p/g1-strategy-spec-memo` branch. Phase 4p is **not** merged to main by this closeout. Any future merge to main requires a separate explicit operator authorization brief (analogous to prior phase merge closeouts).

## Forbidden-work confirmation

Phase 4p did NOT do any of the following:

- write G1 backtest code or any backtest code
- run G1 backtests or any backtests
- author Phase 4q backtest-plan memo, data-requirements memo, acquisition orchestrator, or any other successor memo
- acquire data; modify data; modify manifests
- modify Phase 4f / 4g / 4h / 4i / 4j / 4k / 4l / 4m / 4n / 4o / Phase 3 retained-evidence text
- modify the Phase 4i acquisition script or execute it
- modify the Phase 4l backtest script or execute it
- modify the Phase 4j §11 metrics OI-subset partial-eligibility binding rule
- modify the Phase 3r §8 mark-price gap governance
- modify the Phase 3v §8 stop-trigger-domain governance
- modify the Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance
- revise any retained verdict (R3 / R2 / F1 / D1-A / V2 / H0 / R1a / R1b-narrow)
- change any project lock (§11.6 = 8 bps HIGH per side; §1.7.3 risk / leverage / position locks; mark-price stops; v002 verdict provenance)
- propose any 5m strategy / hybrid / variant
- propose any V2-prime / V2-rescue
- propose any retained-evidence rescue
- propose any G1-prime / G1-variant
- start Phase 4q / Phase 4r / Phase 4 canonical / paper-shadow / live-readiness / deployment / production-key creation / exchange-write capability / authenticated REST / private endpoints / user-stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work
- consult any private endpoint / user stream / WebSocket / authenticated REST in code
- store, request, or display any secret

## Remaining boundary

```text
R3                  : V1 breakout baseline-of-record (preserved)
H0                  : framework anchor (preserved)
R1a / R1b-narrow    : retained research evidence; non-leading (preserved)
R2                  : FAILED — Section 11.6 cost-sensitivity blocks (preserved)
F1                  : HARD REJECT (preserved)
D1-A                : MECHANISM PASS / FRAMEWORK FAIL — other (preserved)
V2                  : HARD REJECT (Phase 4l terminal for first-spec; preserved)
G1                  : pre-research only; strategy-spec defined; not implemented;
                      not backtested; not validated; not live-ready
Section 11.6        : 8 bps HIGH per side (preserved verbatim)
Section 1.7.3       : 0.25% risk / 2x leverage / 1 position / mark-price stops (preserved)
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance (preserved)
Phase 4a runtime            : public API and behavior (preserved)
Phase 4e                    : reconciliation-model design memo (preserved)
Phase 4f                    : V2 hypothesis predeclaration (preserved)
Phase 4g                    : V2 strategy spec (preserved)
Phase 4h                    : V2 data-requirements / feasibility memo (preserved)
Phase 4i                    : V2 acquisition + integrity report; metrics manifests
                              research_eligible: false (preserved)
Phase 4j §11                : metrics OI-subset partial-eligibility binding rule (preserved)
Phase 4k                    : V2 backtest-plan methodology (preserved)
Phase 4l                    : V2 backtest execution; Verdict C HARD REJECT (preserved)
Phase 4m                    : post-V2 strategy research consolidation memo;
                              18-requirement validity gate (preserved)
Phase 4n                    : fresh-hypothesis discovery memo; Candidate B selected (preserved)
Phase 4o                    : G1 hypothesis-spec layer (preserved)
Phase 4p                    : G1 strategy-spec memo (this phase; new)
Recommended state           : paused
```

## Next authorization status

```text
Phase 4q                    : NOT authorized
Phase 4r                    : NOT authorized
Phase 4 (canonical)         : NOT authorized
Paper / shadow              : NOT authorized
Live-readiness              : NOT authorized
Deployment                  : NOT authorized
Production-key creation     : NOT authorized
Authenticated REST          : NOT authorized
Private endpoints           : NOT authorized
User stream / WebSocket     : NOT authorized
Exchange-write capability   : NOT authorized
MCP / Graphify              : NOT authorized
.mcp.json / credentials     : NOT authorized
G1 implementation           : NOT authorized
G1 backtest execution       : NOT authorized
G1 data acquisition         : NOT authorized (none required; Phase 4i datasets reused)
G1 backtest-plan memo       : NOT authorized (Phase 4q recommended next; not yet authorized)
V2-prime / V2-variant       : NOT authorized; not proposed
G1-prime / G1-variant       : NOT authorized; not proposed
Retained-evidence rescue    : NOT authorized; not proposed
5m strategy / hybrid        : NOT authorized; not proposed
ML feasibility              : NOT authorized; not proposed
New family research         : NOT authorized beyond Phase 4n Candidate B (G1)
```

The next step is operator-driven: the operator decides whether to authorize Phase 4q (G1 backtest-plan memo, docs-only) or remain paused. Until then, the project remains at the post-Phase-4p G1 strategy-spec boundary.

---

**Phase 4p was docs-only. No source code, tests, scripts, data, manifests, or successor phases were created or modified. Recommended state remains paused. No next phase authorized.**
