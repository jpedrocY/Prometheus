# Phase 4q Closeout

## Summary

Phase 4q translated the locked Phase 4p G1 strategy spec into a precise, reproducible, fail-closed *future* Phase 4r backtest methodology, predeclared before any G1 backtest code, data acquisition, or execution exists. The memo specifies, for the future Phase 4r execution: data inputs and manifest handling; standalone-script boundary at `scripts/phase4r_g1_backtest.py`; exact future command shape; explicit-column data-loading rules; exact feature-computation algorithms; regime-classifier pseudocode; deterministic regime-state-machine update rules; signal-generation rules; entry / exit simulation; cost / funding model; position-sizing / exposure rules; threshold-grid handling for the locked Phase 4p 32-variant grid (2^5) over five binary axes; M1 / M2 / M3 / M4 mechanism-check implementation plans with the Phase 4p numeric thresholds; PBO / deflated Sharpe / CSCV plan; chronological train / validation / OOS holdout windows reused verbatim from Phase 4k; BTCUSDT-primary / ETHUSDT-comparison protocol; 12 catastrophic-floor predicates with G1-specific evaluation rules (CFPs 10 / 11 / 12 are runtime-stop; CFPs 1..9 are post-run verdict predicates); Verdict A / B / C / D taxonomy; required reporting tables; required plots; 24-item stop-condition list; reproducibility requirements with pinned RNG seed 202604300 and manifest SHA pinning; what a future Phase 4r may create; what this memo explicitly does not authorize. Phase 4q was docs-only.

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4q_g1-backtest-plan-memo.md   (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4q_closeout.md                 (new — this file)
```

No other files modified by Phase 4q.

## Backtest-plan conclusion

The Phase 4q methodology is the methodological mirror of Phase 4k applied to the Phase 4p G1 strategy spec, narrowed by G1's 32 (vs. V2's 512) variant grid and broadened by G1's regime-state-machine plus M1 active-vs-inactive negative-test framework. The plan is complete: every step from data load to verdict declaration is predeclared, with explicit fail-closed boundaries at every governance-relevant decision. Phase 4q does not authorize Phase 4r execution; Phase 4r requires a separate explicit operator authorization brief. G1 remains pre-research only: not implemented; not backtested; not validated; not live-ready; not a rescue of R3 / R2 / F1 / D1-A / V2.

## Relationship to Phase 4p

Phase 4p created the complete G1 strategy spec (timeframes, regime classifier, regime state machine, inside-regime breakout setup, structural stop, target / time-stop, position sizing, cost model, 32-variant threshold grid over five binary axes, M1 / M2 / M3 / M4 numeric thresholds, 12 catastrophic-floor predicates, validation windows, governance labels, data-requirements decision). Phase 4p did NOT authorize backtesting or implementation. The operator authorized Phase 4q only. Phase 4q is the docs-only methodology layer; it must NOT run a backtest, write the script, modify any Phase 4p selection, or activate `N_R ∈ {2.0, 2.5}` / `T_stop ∈ {12, 16}` as backtest axes (those remain future G1-extension possibilities only).

## Future script boundary

```text
Path:      scripts/phase4r_g1_backtest.py    (NOT created by Phase 4q)
Pattern:   standalone research script only
Imports:   no prometheus.runtime.*; no prometheus.execution.*;
           no prometheus.persistence.*; no exchange adapters;
           no requests / httpx / aiohttp / websockets / urllib3 / urllib.request
Stack:     pyarrow + numpy + stdlib (mirroring Phase 4l)
Network:   forbidden
Credentials: forbidden
.env:      forbidden to read
Writes:    only to data/research/phase4r/ (gitignored; not committed);
           never to data/raw/, data/normalized/, or data/manifests/
RNG seed:  202604300 (pinned)
Output dir: data/research/phase4r/
```

## Data inputs

Future Phase 4r must use exactly:

```text
v002 (research-eligible per the locked v002 retained-evidence trade range):
  binance_usdm_btcusdt_15m__v002         (fallback / sanity only)
  binance_usdm_ethusdt_15m__v002         (fallback / sanity only)
  binance_usdm_btcusdt_1h__v002          (or 1h derived from 15m)
  binance_usdm_ethusdt_1h__v002          (or 1h derived from 15m)
  binance_usdm_btcusdt_funding__v002
  binance_usdm_ethusdt_funding__v002

Phase 4i (research-eligible per Phase 4i):
  binance_usdm_btcusdt_30m__v001
  binance_usdm_ethusdt_30m__v001
  binance_usdm_btcusdt_4h__v001
  binance_usdm_ethusdt_4h__v001
```

Forbidden inputs: Phase 4i metrics OI subset; optional metrics ratio columns; mark-price (any timeframe); aggTrades; spot data; cross-venue data; 5m diagnostic outputs as features or regime indicators; modified Phase 4i / v002 / v001-of-5m manifests; v003; private / authenticated REST / public-endpoint-in-code / user stream / WebSocket / listenKey lifecycle.

## Feature computation plan

Predeclared algorithms (binding for Phase 4r):

- 4h EMA(20), 4h EMA(50) Wilder-style on completed 4h close.
- EMA20 discrete slope-rising state vs. 3 completed 4h bars earlier (Phase 3w §7 `ema_slope_method = discrete_comparison`).
- 12-bar 4h directional efficiency = `|close[t] - close[t-12]| / sum(|close[k] - close[k-1]|, k=t-11..t)`.
- 30m ATR(20) Wilder.
- 30m ATR(20) percentile rank over the prior 480 completed 30m bars.
- 30m relative volume vs. prior 480-bar median.
- v002 funding-rate percentile over trailing 90 funding events.
- 30m Donchian prior 12-bar high / low excluding current bar.
- Structural stop = 12-bar low (long) / 12-bar high (short) ± 0.10 × ATR(20).
- R = `|entry_price − initial_stop|`.
- Stop-distance bounds gate: `0.50 ≤ stop_distance / ATR(20) ≤ 2.20` (else reject at entry).

All features use prior-completed bars only. Warmup classifies as `unfavorable` until enough lookback exists.

## Regime classifier plan

Composite, prior-completed bars only, independent of breakout signal:

```text
favorable_long   := htf_trend_state == LONG
                    AND DE_4h(t) >= E_min
                    AND P_atr_low <= ATR_pct_480 <= P_atr_high
                    AND relative_volume_30m >= V_liq_min
                    AND P_fund_low <= funding_pct_90 <= P_fund_high

favorable_short  := mirror with htf_trend_state == SHORT

unfavorable      := NOT favorable_long AND NOT favorable_short
```

Forbidden inputs (binding): future bars; breakout signal; 5m Q1–Q7 outputs; V2 Phase 4l forensic stop-distance numbers; mark-price; aggTrades; spot / cross-venue; private / authenticated data; discretionary / manual labels.

## State-machine plan

Four states (`regime_inactive`, `regime_candidate`, `regime_active`, `regime_cooldown`); transitions evaluated only on completed 4h bar boundaries; per-variant per-symbol independent traces. Key rules:

- `regime_inactive` → `regime_candidate` on `favorable_<D>` (direction = D, candidate_count = 1).
- `regime_candidate (D, C)` → `regime_active (D)` once `C >= K_confirm` (K_confirm ∈ {2, 3} from grid).
- `regime_candidate (D)` → `regime_inactive` on any non-favorable_<D> outcome (including direction switch — does not auto-swap).
- `regime_active (D)` → `regime_cooldown (D, count=1)` on first non-favorable_<D> bar OR on trade exit.
- `regime_cooldown (D, C)` → `regime_active (D)` if `C >= C_cooldown = 4` AND favorable_<D> persists; → `regime_inactive` if `C >= C_cooldown` AND non-favorable.
- **No direction switch inside `regime_active`.**
- **No entries outside `regime_active`** (CFP-11 stop condition).
- **Position lifecycle independent after entry** (Option A).

## Signal / entry / exit plan

```text
Signal (only when latest-completed-4h state == regime_active):
  long  setup := close_30m(t) > prior_12_high_30m(t) + 0.10 * ATR_20(t)
                 (only when active LONG)
  short setup := close_30m(t) < prior_12_low_30m(t)  - 0.10 * ATR_20(t)
                 (only when active SHORT)
  if stop_distance_atr not in [0.50, 2.20]: REJECT at entry.

Entry:
  market entry at next 30m bar's open.
  one position max; no pyramiding; no reversal while positioned.

Exit (per completed 30m bar after entry):
  stop precedence: stop > take-profit > time-stop.
  same-bar ambiguity: stop wins (conservative).
  take-profit at +2.0R fixed.
  time-stop at 16 completed 30m bars; exit at next bar's open.
  initial structural stop fixed at entry (no break-even; no trailing).
  any exit -> regime_cooldown in position direction.
```

Forbidden: V2 8-feature AND chain; R2 pullback-retest; F1 mean-reversion; D1-A funding-Z-score directional rule; 5m triggers; intrabar entries; partial fills; limit-order modeling; reversal while positioned; portfolio construction.

## Cost model

```text
LOW    = 1   bp slippage per side
MEDIUM = 4   bps slippage per side
HIGH   = 8   bps slippage per side    (§11.6 promotion gate; verbatim)
taker fee per side = 4 bps
maker rebate     = NOT used
live fee model   = NOT used
funding cost     = applied at every completed funding event the position
                   spans; sign convention preserved from v002 manifest.
HIGH cost survival is the binding promotion gate (R2 pattern preserved).
```

## Threshold-grid handling

```text
32 variants (= 2^5).
5 binary axes (Phase 4p locked):
  Axis 1: E_min          in {0.30, 0.40}
  Axis 2: ATR band       in {[20, 80], [30, 70]}
  Axis 3: V_liq_min      in {0.80, 1.00}
  Axis 4: funding band   in {[15, 85], [25, 75]}
  Axis 5: K_confirm      in {2, 3} 4h bars

Deterministic lexicographic variant ordering (documented in run_metadata.json).
No grid extension; no grid reduction; no early exit; all 32 variants reported.
Train-best variant by deflated Sharpe; same variant identifier carried into
validation and OOS reporting (no re-selection).
N_R, T_stop, and any other parameter extension = separately authorized
governance amendment; Phase 4r must NOT introduce them.
```

## M1 / M2 / M3 / M4 plan

```text
M1 — Regime-validity negative test:
  active_mean_R - inactive_mean_R >= +0.10R (BTC OOS HIGH)
  AND bootstrap_CI_lower(B=10,000) of differential > 0.

M2 — Regime-gating value-add (G1 vs always-active baseline):
  G1_mean_R - always_active_mean_R >= +0.05R (BTC OOS HIGH)
  AND bootstrap_CI_lower(B=10,000) of differential > 0.

M3 — Inside-regime co-design validity:
  BTC OOS HIGH mean_R > 0 AND trade_count >= 30 AND no CFP-1/2/3.

M4 — Cross-symbol robustness:
  ETH OOS HIGH mean_R differential non-negative AND directional consistency
  with BTC. ETH cannot rescue BTC. CFP-4 enforces this.

Bootstrap RNG seed: 202604300 (pinned).
```

Negative-test framework: M1 active-vs-inactive (binding); M2 always-active baseline (binding); random-regime baseline = diagnostic only (Phase 4q decision; not a binding promotion gate).

## PBO / DSR / CSCV plan

```text
PBO_train_validation : rank-32 train vs rank-32 validation Sharpe;
                        report with bootstrap 95% CI.
PBO_train_oos        : same on train vs OOS.
CFP-6 trigger        : either PBO > 0.50.

Deflated Sharpe (DSR): Bailey & López de Prado 2014; N=32; M=1;
                        skew/kurtosis correction.
                        Train-best variant DSR documented; if train-window
                        trade_count < 30, DSR reported N/A and CFP-1
                        may trigger.

CSCV S = 16 sub-samples on the OOS window;
  C(16, 8) = 12,870 combinations;
  32 variants x 12,870 = ~412,000 sub-evaluations;
  estimated wall-clock < 1 hour on a modern laptop using cached
  per-variant per-bar trade tables;
  if budget exceeded, Phase 4r MUST stop or report explicitly;
  silent approximation forbidden.
```

## Reporting requirements

Required tables (under `data/research/phase4r/tables/`, gitignored):

```text
run_metadata.json                       manifest_references.csv
parameter_grid.csv                      split_boundaries.csv
feature_schema.csv                      regime_state_transitions.csv
regime_active_fraction_by_symbol_window.csv
btc_train_variants.csv                  btc_validation_variants.csv
btc_oos_variants.csv                    eth_train_variants.csv
eth_validation_variants.csv             eth_oos_variants.csv
btc_train_best_variant.csv              btc_train_best_cost_cells.csv
active_vs_inactive_m1.csv               g1_vs_always_active_m2.csv
m1_m2_m3_m4_summary.csv                 cost_sensitivity.csv
pbo_summary.csv                         deflated_sharpe_summary.csv
cscv_rankings.csv                       trade_distribution_by_month_regime.csv
catastrophic_floor_predicates.csv       verdict_declaration.csv
forbidden_work_confirmation.csv
```

Required plots (under `data/research/phase4r/plots/`, gitignored):

```text
cumulative_R_BTC_train_validation_oos.png
cumulative_R_ETH_train_validation_oos.png
regime_state_timeline_BTC.png             regime_state_timeline_ETH.png
active_vs_inactive_R_distribution.png     g1_vs_always_active_mean_R.png
dsr_distribution.png                      pbo_rank_distribution.png
btc_oos_drawdown.png                      monthly_cumulative_R_BTC_oos.png
trade_R_distribution.png
```

If any required plot cannot be produced (e.g., zero trades), the future report must state why and whether this affects Verdict D.

## Stop conditions

Future Phase 4r MUST immediately stop and produce a failure report on any of: required manifest missing; manifest SHA mismatch; `research_eligible` mismatch; local data file missing or corrupted; metrics OI loaded; optional ratio column accessed; mark-price (any timeframe) loaded; aggTrades loaded; spot / cross-venue loaded; 5m diagnostic outputs loaded as features or regime indicators; non-binding manifest loaded; private / authenticated / API / WebSocket / network path touched; credential read or store attempted; `.env` read; write attempted to `data/raw/`, `data/normalized/`, or `data/manifests/`; modification of existing `src/` / tests / scripts; classifier uses future bars; classifier depends on breakout signal; signal emitted outside `regime_active`; trade emitted despite stop-distance rejection; multi-direction emission while regime is single-direction-active; timestamp misalignment; duplicate `(symbol, interval, open_time)` row; partial-bar consumption for strategy decision; validation report incomplete; ruff fail; pytest fail or test-count regression below 785; mypy strict fail; variant grid expanded beyond 32 or contracted below 32; variant ordering changes between train / validation / OOS; non-pinned RNG seed; bootstrap impossible due to insufficient sample (Verdict D path).

## Recommended next operator choice

- **Option A — primary recommendation:** Phase 4r — G1 Backtest Execution (docs-and-code).
- **Option B — conditional secondary:** remain paused.

NOT recommended: immediate G1 implementation; immediate data acquisition; paper / shadow / live; Phase 4 canonical; G1-prime / G1-extension axis activation; V2 / F1 / D1-A / R2 rescue.

**Phase 4r is NOT authorized by this memo or this closeout.** Phase 4r execution requires a separate explicit operator authorization brief.

## Commands run

```text
git status
git rev-parse main
git rev-parse origin/main
git checkout -b phase-4q/g1-backtest-plan-memo
.venv/Scripts/python --version
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m pytest -q (-> pytest)
.venv/Scripts/python -m mypy
git add docs/00-meta/implementation-reports/2026-04-30_phase-4q_g1-backtest-plan-memo.md
git commit -m "phase-4q: G1 backtest-plan memo (docs-only)"
git push -u origin phase-4q/g1-backtest-plan-memo
```

(No acquisition, diagnostics, or backtest scripts were run.)

## Verification results

```text
Python version       : 3.12.4
ruff check .         : All checks passed!
pytest               : 785 passed in 13.69s (no regressions)
mypy                 : Success: no issues found in 82 source files
git status (initial) : clean working tree (only gitignored
                       .claude/scheduled_tasks.lock and data/research/
                       untracked; not committed)
git rev-parse main          : 521915d1ba6fc9c58363dadcd70c99308b1ea1df
git rev-parse origin/main   : 521915d1ba6fc9c58363dadcd70c99308b1ea1df
```

Whole-repo quality gates remain clean. No regressions vs. main HEAD.

## Commit

```text
Phase 4q memo commit:      44e0fde6eb9ac44d24da710c49ceaecc5454c961
Phase 4q closeout commit:  <recorded after this file is committed>
```

## Final git status

(recorded after closeout commit and push)

## Final git log --oneline -5

(recorded after closeout commit and push)

## Final rev-parse

```text
HEAD                                       : <recorded after closeout commit>
origin/phase-4q/g1-backtest-plan-memo      : <recorded after closeout push>
main                                       : 521915d1ba6fc9c58363dadcd70c99308b1ea1df (unchanged)
origin/main                                : 521915d1ba6fc9c58363dadcd70c99308b1ea1df (unchanged)
```

## Branch / main status

`main` remains unchanged at `521915d1ba6fc9c58363dadcd70c99308b1ea1df`. Phase 4q is authored exclusively on the `phase-4q/g1-backtest-plan-memo` branch. Phase 4q is **not** merged to main by this closeout. Any future merge to main requires a separate explicit operator authorization brief (analogous to prior phase merge closeouts).

## Forbidden-work confirmation

Phase 4q did NOT do any of the following:

- run a G1 backtest;
- write G1 backtest code;
- create `scripts/phase4r_g1_backtest.py` or any other script;
- modify any existing script;
- modify any source file under `src/prometheus/`;
- modify any test;
- acquire data;
- download data;
- modify any `data/raw/`, `data/normalized/`, or `data/manifests/` content;
- modify any manifest;
- create v003 or any new dataset;
- run any acquisition / diagnostics / backtest script;
- modify the Phase 4i acquisition script or execute it;
- modify the Phase 4l backtest script or execute it;
- modify the Phase 4j §11 metrics OI-subset partial-eligibility binding rule;
- modify the Phase 3r §8 mark-price gap governance;
- modify the Phase 3v §8 stop-trigger-domain governance;
- modify the Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance;
- modify the Phase 4k V2 backtest-plan methodology;
- modify the Phase 4p G1 strategy spec;
- revise any retained verdict (R3 / R2 / F1 / D1-A / V2 / H0 / R1a / R1b-narrow);
- change any project lock (§11.6 / §1.7.3 / mark-price stops / v002 verdict provenance);
- propose any 5m strategy / hybrid / variant;
- propose any V2-prime / V2-rescue;
- propose any retained-evidence rescue;
- propose any G1-prime / G1-extension axes activation;
- start Phase 4r / Phase 4 canonical / paper-shadow / live-readiness / deployment / production-key creation / exchange-write capability / authenticated REST / private endpoints / user-stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- consult any private endpoint / user stream / WebSocket / authenticated REST in code;
- store, request, or display any secret.

## Remaining boundary

```text
R3                  : V1 breakout baseline-of-record (preserved)
H0                  : framework anchor (preserved)
R1a / R1b-narrow    : retained research evidence; non-leading (preserved)
R2                  : FAILED — §11.6 cost-sensitivity blocks (preserved)
F1                  : HARD REJECT (preserved)
D1-A                : MECHANISM PASS / FRAMEWORK FAIL — other (preserved)
V2                  : HARD REJECT (Phase 4l terminal for first-spec; preserved)
G1                  : pre-research only; strategy-spec defined in Phase 4p;
                      backtest-plan defined in Phase 4q;
                      not implemented; not backtested; not validated;
                      not live-ready
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
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p
                            : all preserved verbatim
Phase 4q                    : G1 backtest-plan methodology (this phase; new)
Recommended state           : paused (outside conditional Phase 4r)
```

## Next authorization status

```text
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
G1 data acquisition            : NOT authorized (none required;
                                                 existing data sufficient)
G1-prime / G1-extension axes   : NOT authorized; not proposed
V2-prime / V2-variant          : NOT authorized; not proposed
Retained-evidence rescue       : NOT authorized; not proposed
5m strategy / hybrid           : NOT authorized; not proposed
ML feasibility                 : NOT authorized; not proposed
New family research            : NOT authorized beyond Phase 4n
                                  Candidate B (G1)
```

The next step is operator-driven: the operator decides whether to authorize Phase 4r (G1 Backtest Execution, docs-and-code) or remain paused. Until then, the project remains at the post-Phase-4q G1 backtest-plan boundary.

---

**Phase 4q was docs-only. No source code, tests, scripts, data, manifests, or successor phases were created or modified. Recommended state remains paused outside conditional Phase 4r. No next phase authorized.**
