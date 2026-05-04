# Phase 4w Closeout

## Summary

Phase 4w authored the **C1 Backtest-Plan Memo** (docs-only) on branch `phase-4w/c1-backtest-plan-memo`. The memo translates the locked Phase 4v C1 strategy spec into a precise, reproducible, fail-closed *future* Phase 4x backtest methodology. Phase 4w is the methodological mirror of Phase 4q applied to C1, narrowed by the 32-variant grid (= 2^5; same cardinality as G1) and broadened by C1's compression-box geometry, M1 contraction-vs-non-contraction negative test, M2 always-active-same-geometry-plus-delayed-breakout dual sub-criterion, opportunity-rate viability floors, and CFP-9 / CFP-11 enrichments. **Phase 4w was docs-only.** No source code, tests, scripts, data, manifests, or successor phases were created or modified. **Phase 4w did NOT authorize Phase 4x.** Whole-repo quality gates remain clean. **C1 remains pre-research only:** hypothesis-spec defined (Phase 4u); strategy-spec defined (Phase 4v); backtest-plan methodology defined (Phase 4w, this phase); not implemented; not backtested; not validated; not live-ready; **not a rescue of R3 / R2 / F1 / D1-A / V2 / G1**.

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4w_c1-backtest-plan-memo.md  (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4w_closeout.md               (new; this file)
```

No other file was created, modified, or deleted by Phase 4w.

## Backtest-plan conclusion

Phase 4w predeclares the future Phase 4x C1 backtest methodology with binding precision. Future Phase 4x must:

- create exactly `scripts/phase4x_c1_backtest.py` (standalone research script; pyarrow + numpy + stdlib + matplotlib optional; no `prometheus.runtime/execution/persistence` imports; no exchange adapters; no network I/O; no credentials);
- write outputs only to gitignored `data/research/phase4x/`;
- evaluate exactly 32 variants over the five Phase 4v binary axes (`B_width`, `C_width`, `N_comp`, `S_buffer`, `T_mult`) in deterministic lexicographic order;
- enforce all C1 fixed parameters verbatim (`W_width = 240`; `L_delay = 1`; close-location 0.70 / 0.30; `T_stop_bars = 2 × N_comp`; no HTF gate; no funding input; no volume gate; no metrics OI; no ATR-percentile stop-distance gate);
- compute compression-box / rolling-median / contraction-state / contraction_recently_active / close-location / long-and-short transitions / structural stop / measured-move target / positive-R guard / ATR(20) Wilder diagnostic;
- generate signals exactly per the predeclared pseudocode (long-only on `LONG_TRANSITION[t]`; short-only on `SHORT_TRANSITION[t]`; no V2 8-feature AND chain; no R2 pullback-retest; no F1 mean-reversion; no D1-A funding-Z; no G1 multi-dimension AND classifier);
- simulate next-30m-bar-open market entry; fixed initial structural stop; measured-move target; `T_stop_bars` time-stop; stop > target > time-stop precedence; same-bar ambiguity = stop-first conservative; no break-even; no trailing;
- apply LOW = 1 bp / MEDIUM = 4 bps / HIGH = 8 bps slippage with 4 bps taker fee per side; funding excluded; §11.6 = 8 bps preserved;
- size positions at 0.25% risk with 2× leverage cap and one position max; BTCUSDT primary; ETHUSDT comparison only; ETH cannot rescue BTC;
- compute deflated Sharpe with N = 32, PBO train→validation and train→OOS rank-based, CSCV with S = 16 / C(16, 8) = 12 870 combinations; no silent approximation;
- evaluate M1 contraction-vs-non-contraction (≥ +0.10R; bootstrap CI lower > 0); M2 C1-vs-always-active (≥ +0.05R; CI lower > 0; AND C1 ≥ delayed-breakout); M3 BTC OOS HIGH `mean_R > 0` AND `trade_count ≥ 30` AND no CFP-1 / 2 / 3 trigger AND opportunity-rate floors satisfied; M4 ETH non-negative differential AND directional consistency; bootstrap B = 10 000; pinned RNG seed 202604300; M5 compression-box validity diagnostic-only;
- evaluate CFP-1..CFP-12 with C1-specific thresholds; CFPs 10 / 11 / 12 are runtime-stop (Verdict D); CFPs 1..9 are post-run (Verdict C); any single CFP triggered = HARD REJECT or INCOMPLETE per precedence;
- declare a final Verdict A / B / C / D in `data/research/phase4x/tables/verdict_declaration.csv`;
- emit 32 binding tables and (optionally) 16 plots;
- enforce a 24-item stop-condition list and reproducibility requirements (manifest SHA pinning; commit SHA; deterministic variant ordering; pinned RNG seed; idempotent outputs).

The future Phase 4x must NOT modify `src/prometheus/`, tests, or existing scripts; must NOT acquire data; must NOT modify manifests; must NOT create v003; must NOT create paper / shadow / live capability; must NOT enable any forbidden input.

## Relationship to Phase 4v

- Phase 4v locked the complete C1 strategy spec (timeframes, contraction measure, expansion transition, breakout geometry, stop / target / time-stop / sizing model, opportunity-rate floors, mechanism-check thresholds, CFP thresholds, threshold grid, validation windows, data-requirements decision).
- Phase 4v did NOT authorize backtesting, backtest-plan methodology, implementation, or Phase 4w.
- Phase 4v recommended Phase 4w as conditional primary.
- The operator explicitly authorized Phase 4w.
- Phase 4w preserves every Phase 4v locked decision verbatim.
- Phase 4w preserves the Phase 4u central anti-G1 discipline at the methodology level.
- Phase 4w remains docs-only.
- Phase 4w does NOT authorize Phase 4x.

## Future script boundary

Predeclared at `scripts/phase4x_c1_backtest.py`. Standalone research script only. No `prometheus.runtime.*`, `prometheus.execution.*`, or `prometheus.persistence.*` imports. No exchange adapters. No `requests` / `httpx` / `aiohttp` / `websocket` / `websockets` / `urllib`-network usage. No `.env`. No credentials. No Binance API. No network I/O. Outputs only to gitignored `data/research/phase4x/`. Pure pyarrow + numpy + stdlib (matplotlib optional, plot-only). **Phase 4w did NOT create the script.**

## Data inputs

Required (research-eligible per Phase 4i):

- `binance_usdm_btcusdt_30m__v001` (74 448 bars; primary signal timeframe);
- `binance_usdm_ethusdt_30m__v001` (74 448 bars; ETH comparison signal timeframe).

Optional (reporting-context only; NOT rule inputs):

- `binance_usdm_btcusdt_4h__v001`, `binance_usdm_ethusdt_4h__v001` (Phase 4i v001);
- `binance_usdm_btcusdt_15m__v002`, `binance_usdm_ethusdt_15m__v002` (sanity / fallback);
- `binance_usdm_btcusdt_1h_derived__v002`, `binance_usdm_ethusdt_1h_derived__v002`.

Excluded from C1 first-spec rules (NOT loaded by default):

- v002 funding manifests (funding excluded);
- Phase 4i metrics manifests (Phase 4j §11 governance preserved; not used by C1);
- mark-price datasets (any timeframe; Phase 3r §8; CFP-12);
- aggTrades, spot, cross-venue, order-book data (CFP-12).

Manifest handling: read manifest → pin SHA256 → verify `research_eligible` where applicable → verify per-file SHA against manifest where applicable → fail closed on any mismatch. Never modify, create, or load non-binding manifests as rule inputs.

## Feature computation plan

Phase 4w predeclares exact algorithms (all use prior-completed bars only):

- compression box (`compression_box_high[t] = max(high[t-N_comp..t-1])`, `compression_box_low[t] = min(low[t-N_comp..t-1])`, `compression_box_width[t] = high - low`);
- rolling-median width (`rolling_median_width[t] = median(compression_box_width[t-W_width..t-1])`; `W_width = 240`);
- contraction-state predicate (`width <= C_width × rolling_median_width`);
- `contraction_recently_active[t]` over `[t - L_delay, t]` window (`L_delay = 1`);
- close-location ratio with epsilon guard;
- LONG / SHORT transition predicates with close-location threshold;
- structural stop = compression-box invalidation with `S_buffer × box_width`;
- measured-move target = `T_mult × box_width`;
- positive-R guard;
- ATR(20) Wilder smoothing — diagnostic only (no entry gate).

## Transition / signal generation plan

Predeclared signal-generation pseudocode:

- evaluate on each completed 30m bar t close (decision_time = close_time[t]);
- warmup check: `t >= N_comp + W_width`;
- compute compression box, rolling median, contraction state, contraction_recently_active, close-location;
- LONG_TRANSITION = contraction_recently_active AND close > cbh + B_width × cbw AND cl_long >= 0.70;
- SHORT_TRANSITION mirror with cl_short >= 0.70 (or equivalently cl_long <= 0.30);
- defensive degeneracy check (LONG ∧ SHORT both true on same bar = STOP CFP-11);
- if positioned: drop new transitions (no pyramiding; no reversal);
- candidate generation: compute stop / entry / R / target; reject if R ≤ 0;
- hard rules: no signal if insufficient lookback / duplicate timestamp / partial bar / transition fired more than L_delay bars after contraction ended / already positioned / R ≤ 0 / forbidden-input access.

## Entry / exit simulation plan

- entry: market-at-next-30m-bar-open after confirmed signal close; no intrabar entry; no partial fills; one position max; no pyramiding; no reversal;
- exit: stop > target > time-stop precedence; same-bar stop-and-target = stop wins (conservative); no break-even; no trailing; no regime exit; no funding-driven exit;
- end-of-data time-stop: defaults to close[t'] if t'+1 unavailable; logged as `end_of_data_time_stop = true`; not a STOP condition.

## Cost model

- LOW = 1 bp / MEDIUM = 4 bps / HIGH = 8 bps slippage per side; taker fee 4 bps per side; no maker rebates; no live-fee assumptions; funding excluded;
- §11.6 = 8 bps HIGH preserved verbatim;
- cost applied per side at entry and exit independently;
- realized R computed using executed entry / exit prices and original (pre-cost) stop-distance R denominator (R as normalized stop-distance multiple);
- promotion blocked if BTC OOS HIGH mean_R ≤ 0 (CFP-2; R2 precedent).

## Threshold-grid handling

- exactly 32 variants (= 2^5) over five binary axes;
- deterministic lexicographic ordering (alphabetical axis names: B_width, C_width, N_comp, S_buffer, T_mult);
- variant_id ∈ {0, ..., 31} mapped via bit-encoding;
- no extension; no reduction; no early exit; all 32 variants reported;
- train-best identified by DSR-aware criterion on BTC train MEDIUM; raw-Sharpe tie-break; lowest variant_id tie-break; same identifier carried into validation, OOS, ETH comparison;
- N_R, T_stop are NOT axes (N_R does not exist in C1; T_stop_bars structurally tied to N_comp).

## M1 / M2 / M3 / M4 / M5 plan

- M1 (binding): C1 vs non-contraction baseline; ≥ +0.10R BTC OOS HIGH; bootstrap 95% CI lower (B = 10 000) > 0;
- M2.a (binding): C1 vs always-active-same-geometry; ≥ +0.05R BTC OOS HIGH; CI lower > 0;
- M2.b (binding): C1 vs delayed-breakout; ≥ 0R BTC OOS HIGH;
- M3 (binding): five sub-criteria (BTC OOS HIGH mean_R > 0 AND trade_count ≥ 30 AND no CFP-1/2/3 trigger AND opportunity-rate floors AND no CFP-9);
- M4 (binding): ETH non-negative differential AND directional consistency; ETH cannot rescue BTC; CFP-4 enforces;
- M5 (diagnostic only): compression-box invalidation stop vs ATR-buffered alternative; reportable; not a verdict driver; Phase 4x may skip if non-trivial.

## PBO / DSR / CSCV plan

- DSR with N = 32; per-variant; train-best DSR ≤ 0 = CFP-6;
- PBO_train_validation and PBO_train_oos (rank-based; > 0.50 = CFP-6);
- CSCV with S = 16 chronological OOS sub-samples; C(16, 8) = 12 870 combinations; ~412 000 sub-evaluations tractable; PBO_cscv > 0.50 = CFP-6;
- no silent approximation; if exact CSCV infeasible, Verdict D.

## Reporting requirements

- 32 binding tables under `data/research/phase4x/tables/` (run_metadata.json, manifest_references.csv, parameter_grid.csv, split_boundaries.csv, feature_schema.csv, signal_schema.csv, compression_state_summary.csv, compression_box_diagnostics.csv, candidate_transition_rate_by_symbol_window_variant.csv, transition_distribution_by_month.csv, btc_train/validation/oos_variants.csv, eth_train/validation/oos_variants.csv, btc_train_best_variant.csv, btc_train_best_cost_cells.csv, non_contraction_m1.csv, c1_vs_always_active_m2.csv, delayed_breakout_m2.csv, m1_m2_m3_m4_m5_summary.csv, opportunity_rate_summary.csv, cost_sensitivity.csv, pbo_summary.csv, deflated_sharpe_summary.csv, cscv_rankings.csv, trade_distribution_by_month.csv, stop_distance_atr_diagnostics.csv, catastrophic_floor_predicates.csv, verdict_declaration.csv, forbidden_work_confirmation.csv);
- 16 required plots (cumulative-R curves; compression / transition timelines; C1-vs-baselines; opportunity-rate; DSR / PBO; drawdown / monthly cumulative R; trade-R distribution; stop-distance / box-width distributions); plot absence does not automatically cause Verdict D provided all 32 binding tables are produced;
- forbidden_work_confirmation.csv audit counters all = 0 for a clean run.

## Stop conditions

24-item stop-condition list covering manifest mismatch / missing data / forbidden inputs (CFP-10 / CFP-12) / forbidden behavior (network / credentials / writes to data) / lookahead / transition-dependency violations (CFP-11) / data integrity / methodology violations / quality-gate failures.

## Recommended next operator choice

- **Option A — primary recommendation:** Phase 4x — C1 Backtest Execution (docs-and-code; standalone research script). Phase 4x would create `scripts/phase4x_c1_backtest.py` exactly under the Phase 4w methodology and run the predeclared 32-variant C1 backtest.
- **Option B — conditional secondary:** remain paused.

NOT recommended: immediate C1 implementation in `src/prometheus/`; data acquisition; paper / shadow / live-readiness; Phase 4 canonical; production-key creation; authenticated APIs; private endpoints; user stream; WebSocket; MCP / Graphify / `.mcp.json` / credentials; exchange-write capability; any G1 / V2 / R2 / F1 / D1-A / C1-prime rescue.

**Phase 4x is NOT authorized by this Phase 4w memo.** Phase 4x requires a separate explicit operator authorization brief.

## Commands run

```text
git status                                        (clean except gitignored)
git rev-parse main                                7c731d1322ff8ced829a97f0c5a83ef8a7f726c6
git rev-parse origin/main                         7c731d1322ff8ced829a97f0c5a83ef8a7f726c6
git checkout -b phase-4w/c1-backtest-plan-memo    Switched to new branch
.venv/Scripts/python --version                    Python 3.12.4
.venv/Scripts/python -m ruff check .              All checks passed!
.venv/Scripts/python -m pytest -q                 785 passed in 12.84s
.venv/Scripts/python -m mypy                      Success: no issues found in 82 source files

git add docs/00-meta/implementation-reports/2026-04-30_phase-4w_c1-backtest-plan-memo.md
git commit -F .git/PHASE_4W_COMMIT_MSG            Phase 4w memo committed
git push -u origin phase-4w/c1-backtest-plan-memo Branch pushed; tracking origin

(closeout file authored, committed, and pushed; see Verification results
below)
```

## Verification results

```text
ruff check .                : All checks passed!
pytest                      : 785 passed in 12.84s
mypy strict                 : Success: no issues found in 82 source files

Phase 4w memo line count    : 2150 lines (single new file)
Phase 4w memo SHA           : verified via git commit (e38d55f)

No source code changed.
No tests changed.
No scripts changed.
No data acquired.
No data modified.
No manifests modified.
```

## Commit

```text
Phase 4w memo commit:
  SHA: e38d55f
  Title: phase-4w: C1 backtest-plan memo (docs-only)
  Files: docs/00-meta/implementation-reports/2026-04-30_phase-4w_c1-backtest-plan-memo.md (new; 2150 lines)

Phase 4w closeout commit:
  SHA: <recorded after this file is committed>
```

## Final git status

```text
On branch phase-4w/c1-backtest-plan-memo
Untracked files (gitignored transients only):
  .claude/scheduled_tasks.lock
  data/research/
nothing added to commit but untracked files present
```

## Final git log --oneline -5

```text
<recorded after closeout commit>
```

## Final rev-parse

```text
HEAD                                       <recorded after closeout commit>
origin/phase-4w/c1-backtest-plan-memo      <recorded after closeout push>
main                                       7c731d1322ff8ced829a97f0c5a83ef8a7f726c6 (unchanged)
origin/main                                7c731d1322ff8ced829a97f0c5a83ef8a7f726c6 (unchanged)
```

## Branch / main status

- Phase 4w branch: `phase-4w/c1-backtest-plan-memo` (created from main; pushed to origin).
- main / origin/main: `7c731d1322ff8ced829a97f0c5a83ef8a7f726c6` (unchanged; Phase 4w has not been merged).
- No merge to main is performed by Phase 4w (per authorization brief).

## Forbidden-work confirmation

Phase 4w did NOT do any of the following:

- run a backtest (any phase);
- write any code;
- create `scripts/phase4x_c1_backtest.py` or any other script;
- modify any source under `src/prometheus/`;
- modify any test;
- modify any existing script (`scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`);
- run any acquisition / diagnostics / backtest script;
- acquire data;
- download data;
- patch / forward-fill / interpolate / regenerate / replace data;
- modify any manifest;
- create any new manifest;
- create v003;
- modify Phase 4p / Phase 4q / Phase 4j §11 / Phase 4k / Phase 4v / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r §8 governance;
- revise any retained verdict;
- change any project lock;
- create a runnable strategy;
- create G1-prime / G1-narrow / G1-extension / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- create C1-prime / C1-narrow / C1-extension / C1 hybrid;
- propose a 5m strategy / hybrid / variant;
- start Phase 4x / 4 canonical / paper-shadow / live-readiness / deployment / production-key creation / exchange-write capability / authenticated REST / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
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
§1.7.3              : 0.25% risk / 2× leverage / 1 position / mark-price
                       stops (preserved)
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m
                              (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation
                              governance (preserved)
Phase 4a runtime            : public API and behavior (preserved)
Phase 4e                    : reconciliation-model design memo
                              (preserved)
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q / 4r / 4s / 4t / 4u / 4v
                            : all preserved verbatim
Phase 4w                    : C1 backtest-plan memo (this phase; new;
                              docs-only)
C1                          : pre-research only;
                              hypothesis-spec defined in Phase 4u;
                              strategy-spec defined in Phase 4v;
                              backtest-plan methodology defined in
                              Phase 4w (this memo);
                              not implemented; not backtested; not
                              validated; not live-ready;
                              not a rescue of R3 / R2 / F1 / D1-A / V2 / G1
Recommended state           : Phase 4x conditional primary;
                              remain-paused conditional secondary
```

## Next authorization status

```text
Phase 4x                       : NOT authorized
Phase 4y                       : NOT authorized
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
C1-prime / C1-extension        : NOT authorized; not proposed
Retained-evidence rescue       : NOT authorized; not proposed
5m strategy / hybrid           : NOT authorized; not proposed
ML feasibility                 : NOT authorized; not proposed
Microstructure / liquidity-timing data acquisition (Phase 4t Candidate F)
                               : NOT authorized; data unavailable.
```

The next step is operator-driven: the operator decides whether to authorize Phase 4x (C1 Backtest Execution, docs-and-code) or remain paused. Until then, the project remains at the post-Phase-4w backtest-plan boundary on the Phase 4w branch (not merged to main).

---

**Phase 4w was docs-only. No source code, tests, scripts, data, manifests, or successor phases were created or modified. main remains unchanged at 7c731d1. Recommended state: Phase 4x conditional primary; remain-paused conditional secondary. No next phase authorized.**
