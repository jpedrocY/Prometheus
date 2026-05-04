# Phase 4w Merge Closeout

## Summary

Phase 4w (C1 Backtest-Plan Memo, docs-only) was merged into `main` via a `--no-ff` merge commit. Phase 4w translated the locked Phase 4v C1 strategy spec into a precise, reproducible, fail-closed *future* Phase 4x backtest methodology: standalone-script boundary at `scripts/phase4x_c1_backtest.py`; data-loading rules with manifest SHA pinning and explicit column lists; feature-computation algorithms (compression-box / rolling-median / contraction-state / contraction_recently_active / close-location / LONG-and-SHORT transitions / structural stop / measured-move target / positive-R guard / ATR(20) Wilder diagnostic-only); signal-generation pseudocode; entry / exit simulation (next-30m-bar-open market entry; stop > target > time-stop precedence; same-bar = stop wins; no break-even; no trailing); cost / funding model preserved verbatim (LOW = 1 bp / MED = 4 bps / HIGH = 8 bps; taker fee 4 bps; funding excluded; §11.6 = 8 bps preserved); position-sizing / exposure rules (0.25% risk; 2× leverage cap; one position max; BTC primary; ETH comparison only; ETH cannot rescue BTC); 32-variant threshold-grid handling with deterministic lexicographic ordering; DSR / PBO / CSCV plan (N = 32; S = 16; C(16, 8) = 12 870 combinations; no silent approximation); M1 / M2 / M3 / M4 / M5 implementation plans with numeric thresholds and bootstrap B = 10 000 RNG seed = 202604300; CFP-1..CFP-12 evaluation algorithms with C1-specific thresholds; Verdict A / B / C / D taxonomy; 32 required reporting tables; 16 required plots; 24-item stop-condition list; reproducibility requirements. **Phase 4w was docs-only.** No source code, tests, scripts, data, manifests, or successor phases were created or modified by Phase 4w. Phase 4w did NOT authorize Phase 4x. Whole-repo quality gates remained clean throughout (ruff PASS; pytest 785 PASS; mypy strict 0 issues across 82 source files). **C1 remains pre-research only:** hypothesis-spec defined (Phase 4u); strategy-spec defined (Phase 4v); backtest-plan methodology defined (Phase 4w); not implemented; not backtested; not validated; not live-ready; **not a rescue of R3 / R2 / F1 / D1-A / V2 / G1**.

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4w_c1-backtest-plan-memo.md   (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4w_closeout.md                (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4w_merge-closeout.md          (new; this file)
docs/00-meta/current-project-state.md                                              (narrow Phase 4w sync)
```

No other source code, test, script, data, or manifest file was created or modified.

## Phase 4w commits included

```text
e38d55f  phase-4w: C1 backtest-plan memo (docs-only)
c90f64e  phase-4w: closeout (docs-only)
```

## Merge commit

```text
SHA:    16336b7abecbb43b3a522c56035ae0d88a8f7763
Title:  Merge Phase 4w (C1 backtest-plan memo, docs-only) into main
Type:   --no-ff merge of phase-4w/c1-backtest-plan-memo into main
```

## Housekeeping commit

The merge-closeout file (this file) and the narrow Phase 4w sync to `docs/00-meta/current-project-state.md` are committed as a single docs-only housekeeping commit on `main` after the merge. The housekeeping commit SHA is recorded below in `Final git log --oneline -8`.

## Final git status

```text
On branch main
Your branch is up to date with 'origin/main'.

Untracked files (gitignored transients only; not committed):
  .claude/scheduled_tasks.lock
  data/research/

nothing added to commit but untracked files present
```

## Final git log --oneline -8

Recorded after the housekeeping commit and push.

## Final rev-parse

Recorded after the housekeeping commit and push.

## main == origin/main confirmation

Confirmed at the housekeeping push step.

## Backtest-plan conclusion

- **Phase 4w was docs-only.**
- Phase 4w defines exactly how a future Phase 4x C1 backtest would be run.
- Phase 4w does NOT authorize Phase 4x.
- Phase 4w does NOT authorize backtest execution, implementation, data acquisition, paper / shadow / live, or exchange-write.
- C1 remains pre-research only:
  - hypothesis-spec defined (Phase 4u);
  - strategy-spec defined (Phase 4v);
  - backtest-plan methodology defined (Phase 4w, this phase);
  - not implemented;
  - not backtested;
  - not validated;
  - not live-ready.
- No retained verdict is revised.
- No project lock is changed.

## Relationship to Phase 4v

- Phase 4v locked the complete C1 strategy spec (timeframes, contraction measure, expansion transition, breakout geometry, stop / target / time-stop / sizing model, opportunity-rate floors, mechanism-check thresholds, CFP thresholds, threshold grid, validation windows, data-requirements decision).
- Phase 4v did NOT authorize backtesting, backtest-plan methodology, implementation, or Phase 4w.
- Phase 4v recommended Phase 4w as conditional primary.
- Phase 4w preserves every Phase 4v locked decision verbatim.
- Phase 4w preserves the Phase 4u central anti-G1 discipline at the methodology level (no top-level state machine; no multi-dimension AND classifier; no broad regime gate; entry rule fires on the contraction-to-expansion transition itself).
- Phase 4w remains docs-only.
- Phase 4w does NOT authorize Phase 4x.

## Future script boundary

- **future path:** `scripts/phase4x_c1_backtest.py`
- standalone research script only;
- no `prometheus.runtime` / `execution` / `persistence` imports;
- no exchange adapters;
- no network I/O;
- no credentials;
- no `.env`;
- no Binance API;
- outputs only to `data/research/phase4x/` (gitignored; not committed);
- pure pyarrow + numpy + stdlib (matplotlib optional; plot-only).

**Phase 4w did NOT create this script.** Any future Phase 4x execution that creates the script requires a separate explicit operator authorization brief.

## Data inputs

**Required (research-eligible per Phase 4i):**

- `binance_usdm_btcusdt_30m__v001` (74 448 bars; primary signal timeframe);
- `binance_usdm_ethusdt_30m__v001` (74 448 bars; ETH comparison signal timeframe).

**Optional (reporting context only; NOT rule inputs):**

- `binance_usdm_btcusdt_4h__v001`;
- `binance_usdm_ethusdt_4h__v001`;
- `binance_usdm_btcusdt_15m__v002`;
- `binance_usdm_ethusdt_15m__v002`;
- `binance_usdm_btcusdt_1h_derived__v002`;
- `binance_usdm_ethusdt_1h_derived__v002`.

**Excluded:**

- funding;
- metrics OI;
- optional metrics ratio columns;
- mark-price (any timeframe);
- aggTrades;
- spot;
- cross-venue;
- order book;
- private / authenticated data.

**No acquisition required.** **No manifests modified.** Manifest handling: read manifest → pin SHA256 → verify `research_eligible` where applicable → verify per-file SHA against manifest where applicable → fail closed on any mismatch.

## Feature computation plan

- compression box: `compression_box_high[t] = max(high[t-N_comp..t-1])`; `compression_box_low[t] = min(low[t-N_comp..t-1])`; `compression_box_width[t] = high - low`;
- rolling-median compression-box width: `rolling_median_width[t] = median(compression_box_width[t-W_width..t-1])` with `W_width = 240`;
- contraction-state predicate: `contraction_state[t] = (compression_box_width[t] <= C_width × rolling_median_width[t])`;
- contraction-recently-active window: `any(contraction_state[k] for k in [t - L_delay, ..., t])` with `L_delay = 1`;
- close-location ratio with epsilon guard;
- LONG_TRANSITION = `contraction_recently_active AND close > cbh + B_width × cbw AND cl_long >= 0.70`;
- SHORT_TRANSITION mirror with `cl_short >= 0.70` (or equivalently `cl_long <= 0.30`);
- structural stop = compression-box invalidation with `S_buffer × box_width`;
- measured-move target = `T_mult × box_width`;
- positive-R guard;
- ATR(20) Wilder diagnostic only — NOT an entry gate.

## Transition / signal generation plan

- evaluate on each completed 30m bar t close (decision_time = `close_time[t]`);
- warmup check: `t >= N_comp + W_width`;
- compute compression box, rolling median, contraction state, contraction_recently_active, close-location;
- generate LONG_TRANSITION / SHORT_TRANSITION;
- defensive degeneracy check (LONG ∧ SHORT both true on same bar = STOP CFP-11);
- if positioned: drop new transitions (no pyramiding; no reversal);
- candidate generation: compute stop / entry / R / target; reject if R ≤ 0;
- hard rules: no signal if insufficient lookback / duplicate timestamp / partial bar / transition fired more than `L_delay` bars after contraction ended / already positioned / R ≤ 0 / forbidden-input access.

## Entry / exit simulation plan

- **entry:** next-30m-bar-open market entry; no intrabar entry; no partial fills; one position max; no pyramiding; no reversal;
- **exit:** stop > target > time-stop precedence; same-bar stop-and-target = stop wins (conservative); time-stop = 2 × N_comp 30m bars; no break-even; no trailing; no regime exit; no funding-driven exit;
- end-of-data time-stop edge case: defaults to `close[t']` if `t'+1` unavailable; logged as `end_of_data_time_stop = true`; not a STOP condition.

## Cost model

- LOW = 1 bp slippage per side;
- MEDIUM = 4 bps slippage per side;
- HIGH = 8 bps slippage per side;
- taker fee = 4 bps per side;
- funding excluded;
- **§11.6 = 8 bps HIGH preserved** verbatim;
- no maker rebates;
- no live-fee assumptions;
- cost applied per side at entry and exit independently;
- realized R computed using executed entry / exit prices and original (pre-cost) stop-distance R denominator;
- promotion blocked if BTC OOS HIGH mean_R ≤ 0 (CFP-2).

## Threshold-grid handling

- exactly **32 variants** (= 2^5);
- five binary axes:
  1. `B_width` ∈ {0.05, 0.10};
  2. `C_width` ∈ {0.45, 0.60};
  3. `N_comp` ∈ {8, 12};
  4. `S_buffer` ∈ {0.10, 0.20};
  5. `T_mult` ∈ {1.5, 2.0};
- fixed parameters (cardinality 1; not axes):
  - `W_width = 240` 30m bars;
  - `L_delay = 1`;
  - close-location = 0.70 long / 0.30 short;
  - `T_stop_bars = 2 × N_comp`;
  - no HTF gate;
  - no funding input;
  - no volume gate;
  - no metrics OI;
  - no ATR-percentile stop-distance gate;
- deterministic lexicographic ordering;
- variant_id ∈ {0, ..., 31} via bit-encoding;
- no extension; no reduction; no early exit; all 32 variants reported;
- train-best identified by DSR-aware criterion on BTC train MEDIUM; raw-Sharpe tie-break; lowest variant_id tie-break; same identifier carried into validation, OOS, ETH comparison.

## M1 / M2 / M3 / M4 / M5 plan

- **M1 (binding):** C1 transition trades vs non-contraction breakout baseline; differential ≥ +0.10R on BTC OOS HIGH AND bootstrap CI lower (B = 10 000) > 0.
- **M2 (binding):** C1 vs always-active-same-geometry baseline; differential ≥ +0.05R on BTC OOS HIGH AND bootstrap CI lower > 0; AND C1 ≥ delayed-breakout baseline on BTC OOS HIGH.
- **M3 (binding):** BTC OOS HIGH mean_R > 0 AND trade_count ≥ 30 AND no CFP-1 / CFP-2 / CFP-3 trigger AND opportunity-rate floors satisfied AND no CFP-9 trigger.
- **M4 (binding):** ETH OOS HIGH non-negative differential AND directional consistency with BTC; ETH cannot rescue BTC; CFP-4 enforces.
- **M5 (diagnostic only):** compression-box invalidation stop vs ATR-buffered alternative on same setup; reportable; not a verdict driver; Phase 4x may skip without affecting verdict.

Bootstrap B = 10 000; pinned RNG seed = 202604300.

## PBO / DSR / CSCV plan

- **DSR with N = 32**: per-variant deflated Sharpe on BTC train MEDIUM; train-best DSR ≤ 0 = CFP-6.
- **PBO train→validation**: rank-based; > 0.50 = CFP-6.
- **PBO train→OOS**: rank-based; > 0.50 = CFP-6.
- **CSCV S = 16**: chronological OOS sub-samples; **C(16, 8) = 12 870 combinations**; ~412 000 sub-evaluations tractable; PBO_cscv > 0.50 = CFP-6.
- **No silent approximation.** If exact CSCV is infeasible, Phase 4x must STOP and emit Verdict D.

## Reporting requirements

- Future Phase 4x must produce **32 binding tables** under `data/research/phase4x/tables/` (run_metadata.json, manifest_references.csv, parameter_grid.csv, split_boundaries.csv, feature_schema.csv, signal_schema.csv, compression_state_summary.csv, compression_box_diagnostics.csv, candidate_transition_rate_by_symbol_window_variant.csv, transition_distribution_by_month.csv, btc_train/validation/oos_variants.csv, eth_train/validation/oos_variants.csv, btc_train_best_variant.csv, btc_train_best_cost_cells.csv, non_contraction_m1.csv, c1_vs_always_active_m2.csv, delayed_breakout_m2.csv, m1_m2_m3_m4_m5_summary.csv, opportunity_rate_summary.csv, cost_sensitivity.csv, pbo_summary.csv, deflated_sharpe_summary.csv, cscv_rankings.csv, trade_distribution_by_month.csv, stop_distance_atr_diagnostics.csv, catastrophic_floor_predicates.csv, verdict_declaration.csv, forbidden_work_confirmation.csv).
- Future Phase 4x should produce **16 plots** under `data/research/phase4x/plots/`.
- **Plot absence does NOT automatically cause Verdict D** if all 32 binding tables are complete and absence is documented.
- `data/research/phase4x/` outputs are **gitignored** and **must NOT be committed**.

## Stop conditions

- manifest mismatch / missing data;
- forbidden inputs (CFP-10 / CFP-12: metrics OI; mark-price; aggTrades; spot; cross-venue; 5m diagnostics as features; non-binding manifest);
- network / credentials / `.env` / writes to `data/raw/` / `data/normalized/` / `data/manifests/`;
- lookahead / transition-dependency violations (CFP-11: future bar consumed; partial bar consumed; signal without contraction precondition; entry beyond `L_delay`; same-bar AND-chain consulting future-bar value; degenerate double-transition; entry-bar gap);
- data integrity issues (timestamp misalignment; duplicate row; bar gap; trade with R ≤ 0);
- methodology violations (validation report incomplete; variant grid expanded or contracted; variant ordering changes between train / validation / OOS; RNG seed not pinned; bootstrap impossible due to sample-size collapse);
- quality-gate failures (ruff fails; pytest fails or test count regresses below 785; mypy strict fails);
- **CSCV silent approximation** (S < 16 or fewer than 12 870 combinations evaluated without explicit Verdict D);
- grid expansion or reduction;
- non-pinned RNG seed.

## Recommended next operator choice

- **Option A — primary recommendation:** Phase 4x — C1 Backtest Execution (docs-and-code; standalone research script).
- **Option B — conditional secondary:** remain paused.

**Phase 4x is NOT started by this merge.**

NOT recommended:

- immediate C1 implementation in `src/prometheus/` — REJECTED;
- data acquisition — REJECTED (Phase 4v determined existing data sufficient);
- paper / shadow / live / exchange-write — FORBIDDEN;
- Phase 4 canonical — FORBIDDEN;
- C1-prime / C1-extension / C1-narrow / C1 hybrid — FORBIDDEN;
- G1 / V2 / R2 / F1 / D1-A rescue — FORBIDDEN.

## Verification evidence

```text
ruff check .                : All checks passed!
pytest                      : 785 passed in 12.84s
mypy strict                 : Success: no issues found in 82 source files
```

(Verified during Phase 4w branch work; no source/test/script changes by Phase 4w; gates remain clean post-merge by construction.)

## Forbidden-work confirmation

Phase 4w (and this merge) did NOT do any of the following:

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
Phase 4e                    : reconciliation-model design memo (preserved)
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q / 4r / 4s / 4t / 4u / 4v
                            : all preserved verbatim
Phase 4w                    : C1 backtest-plan memo (this phase; merged
                              to main; docs-only)
C1                          : pre-research only;
                              hypothesis-spec defined in Phase 4u;
                              strategy-spec defined in Phase 4v;
                              backtest-plan methodology defined in
                              Phase 4w (this merge);
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

The next step is operator-driven: the operator decides whether to authorize Phase 4x (C1 Backtest Execution, docs-and-code) or remain paused. Until then, the project remains at the post-Phase-4w backtest-plan boundary on `main`.

---

**Phase 4w was docs-only and has been merged into `main`. No source code, tests, scripts, data, manifests, or successor phases were created or modified. Recommended state: Phase 4x conditional primary; remain-paused conditional secondary. No next phase authorized.**
