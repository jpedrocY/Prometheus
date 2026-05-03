# Phase 4r Closeout

## Summary

Phase 4r implemented `scripts/phase4r_g1_backtest.py` as a standalone research backtest script and ran the Phase 4q-predeclared G1 — Regime-First Breakout Continuation backtest exactly under the Phase 4q methodology over the locked Phase 4k train (2022-01-01..2023-06-30 UTC) / validation (2023-07-01..2024-06-30 UTC) / OOS holdout (2024-07-01..2026-03-31 UTC) windows on BTCUSDT-primary / ETHUSDT-comparison, evaluating all 32 variants of the Phase 4p locked grid across LOW / MEDIUM / HIGH cost cells with §11.6 = 8 bps preserved verbatim. **Final verdict: C — G1 framework HARD REJECT.** Binding catastrophic-floor driver: **CFP-1 critical** (32 / 32 variants below the 30-trade threshold on OOS BTC HIGH; train-best variant produced 0 OOS HIGH trades). Subordinate / structural triggers: **CFP-9** (regime-active fraction 2.03% < 5%), **CFP-3** (mechanical PF = 0 under empty arrays), **CFP-4** (degenerate M3 BTC FAIL with trivial M4 ETH PASS). G1 first-spec is terminally HARD REJECTED as retained research evidence only. Phase 4r was docs-and-code; no `src/prometheus`, tests, existing scripts, data, or manifests modified.

## Files changed

```text
scripts/phase4r_g1_backtest.py                                                         (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4r_g1-backtest-execution.md       (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4r_closeout.md                    (new — this file)
```

Local gitignored outputs under `data/research/phase4r/` (tables only; plots empty in this run because matplotlib was unavailable in the project virtualenv) — **not committed**.

## Backtest execution conclusion

The Phase 4q methodology was implemented exactly: standalone-script boundary at `scripts/phase4r_g1_backtest.py`; pure pyarrow + numpy + stdlib runtime; explicit-column Parquet loaders; deterministic feature computation (4h EMA(20)/(50) Wilder, EMA20 discrete slope vs t-3, 12-bar 4h directional efficiency, 30m ATR(20) Wilder, 480-bar ATR percentile, 480-bar relative-volume, 90-event funding percentile, 12-bar Donchian high/low excluding current bar, structural stop with [0.50, 2.20]×ATR bounds gate); 4-state regime state machine on completed 4h bars; 30m Donchian breakout (N_breakout=12, B_atr=0.10); fixed +2.0R target; T_stop=16; stop > TP > time-stop precedence with same-bar stop-first conservative tie-break; LOW/MEDIUM/HIGH cost cells with §11.6 = 8 bps preserved verbatim; 0.25% risk / 2× leverage / one position max preserved verbatim from §1.7.3; 32-variant deterministic-lexicographic grid; M1/M2/M3/M4 with bootstrap (B=10,000; pinned RNG seed 202604300); PBO train→validation, train→OOS (rank-based proxy); CSCV S=16 with C(16,8)=12,870 combinations; deflated Sharpe with N=32; all 12 catastrophic-floor predicates evaluated. **The train-best variant (id=0) produced 0 G1 trades on BTC OOS HIGH; the always-active baseline produced 124 trades with mean_R = −0.34; the inactive-population pseudo-trades produced 124 trades with mean_R = −0.34 — confirming the breakout-and-stop machinery fires but the regime gate filters out essentially all candidates.**

## Verdict

```text
Final Verdict:    C — G1 framework HARD REJECT
Binding driver:   CFP-1 critical
Independent driver:   CFP-9
Subordinate / mechanical drivers:    CFP-3, CFP-4
M1 / M2 / M3:     FAIL (degenerate; G1 active population is empty for the
                  train-best variant on OOS HIGH)
M4:               trivial PASS (degenerate 0=0 differential under both ETH
                  populations being empty); CFP-4 catches this.
Promotion-bar:    NOT met.
G1 first-spec:    terminally HARD REJECTED as retained research evidence only.
```

## Dataset inputs

```text
v002 trade-price klines:
  binance_usdm_btcusdt_15m__v002          (fallback / sanity; not actively used)
  binance_usdm_ethusdt_15m__v002          (fallback / sanity; not actively used)
  binance_usdm_btcusdt_1h_derived__v002   (fallback / sanity; not actively used)
  binance_usdm_ethusdt_1h_derived__v002   (fallback / sanity; not actively used)

Phase 4i trade-price klines (research-eligible):
  binance_usdm_btcusdt_30m__v001          (74 448 bars; used for 30m features)
  binance_usdm_ethusdt_30m__v001          (74 448 bars; used for 30m features)
  binance_usdm_btcusdt_4h__v001           (9 306 bars;  used for 4h regime classifier)
  binance_usdm_ethusdt_4h__v001           (9 306 bars;  used for 4h regime classifier)

v002 funding history:
  binance_usdm_btcusdt_funding__v002      (used for funding percentile feature)
  binance_usdm_ethusdt_funding__v002      (used for funding percentile feature)

Forbidden inputs (audit-zero by construction):
  Phase 4i metrics OI subset           (Phase 4j §11 governance preserved but unused)
  Optional metrics ratio columns       (Phase 4j §11.3 forbidden; not loaded)
  Mark-price (any timeframe)           (Phase 3r §8 governance preserved)
  aggTrades                            (not loaded)
  Spot data / cross-venue data         (not loaded)
  5m diagnostic outputs as features    (not loaded)
  Modified manifests / v003            (not modified / not created)
```

All used manifests SHA256-pinned in `data/research/phase4r/tables/manifest_references.csv`.

## Local result artefacts

All under `data/research/phase4r/` (gitignored; not committed):

```text
run_metadata.json
tables/manifest_references.csv
tables/parameter_grid.csv                  (32 rows)
tables/split_boundaries.csv                (3 rows)
tables/feature_schema.csv                  (12 rows)
tables/regime_state_transitions.csv        (compact transitions)
tables/regime_active_fraction_by_symbol_window.csv  (192 rows)
tables/btc_train_variants.csv              (96 rows)
tables/btc_validation_variants.csv         (96 rows)
tables/btc_oos_variants.csv                (96 rows)
tables/eth_train_variants.csv              (96 rows)
tables/eth_validation_variants.csv         (96 rows)
tables/eth_oos_variants.csv                (96 rows)
tables/btc_train_best_variant.csv          (1 row)
tables/btc_train_best_cost_cells.csv       (9 rows)
tables/active_vs_inactive_m1.csv
tables/g1_vs_always_active_m2.csv
tables/m1_m2_m3_m4_summary.csv             (4 rows)
tables/cost_sensitivity.csv                (576 rows)
tables/pbo_summary.csv                     (3 rows)
tables/deflated_sharpe_summary.csv         (32 rows)
tables/cscv_rankings.csv                   (12 870 rows)
tables/trade_distribution_by_month_regime.csv  (0 rows)
tables/catastrophic_floor_predicates.csv   (12 rows)
tables/verdict_declaration.csv
tables/forbidden_work_confirmation.csv
plots/                                     (empty; matplotlib unavailable)
```

## Forbidden input verification

```text
metrics_oi_access_count                    0
mark_price_access_count                    0
aggtrades_access_count                     0
spot_access_count                          0
cross_venue_access_count                   0
optional_ratio_column_access_count         0
network_io_attempts                        0
credential_reads                           0
env_file_reads                             0
data_raw_writes                            0
data_normalized_writes                     0
data_manifest_modifications                0
v003_creations                             0
src_prometheus_modifications               0
test_modifications                         0
existing_script_modifications              0
```

The four substrings remaining in the script (`metrics_oi`, `mark_price`, `aggtrades`, `cross_venue`) are **audit-counter field names only**, used to record the runtime access count = 0 in `forbidden_work_confirmation.csv` and in the CFP-12 detail dict. Per Phase 4q §"Static scan nuance", this pattern is allowed for guard checks; runtime access count is zero; no other code path can reach those data sources because the loaders use explicit-column lists for klines and funding only.

## BTCUSDT primary result summary

```text
Train-best variant:    id=0 (E=0.30, ATR=[20,80], V_liq=0.80, Fund=[15,85], K=2)
Selection criterion:   DSR-aware (raw-Sharpe tie-break);
                       all 32 DSRs computed = 0.0; lowest variant-id selected.
BTC OOS HIGH (train-best):  trade_count = 0; mean_R = 0; total_R = 0;
                            sharpe = 0; profit_factor = 0; max_dd_R = 0.
BTC OOS HIGH (all 32):      every variant has trade_count = 0.
BTC train MEDIUM total:     4 trades across 32 variants (sparse).
BTC OOS regime-active fraction (train-best):  2.03%   (CFP-9 < 5%; triggered)
Always-active baseline (id=0, BTC OOS HIGH):  124 trades; mean_R = -0.34.
Inactive-population pseudo (id=0, BTC OOS HIGH):  124 trades; mean_R = -0.34.
```

## ETHUSDT comparison result summary

```text
Train-best variant id (carried from BTC):   0
ETH OOS HIGH (train-best, G1):  trade_count = 0; mean_R = 0.
ETH OOS HIGH (all 32, G1):       every variant has trade_count = 0
                                  (regime gate intersection sparseness).
ETH OOS HIGH (always-active baseline):  also trade_count = 0 in this run for
                                         the train-best variant (signal arrays
                                         under HIGH cost on the train-best
                                         spec produce zero qualifying entries
                                         on ETH; the breakout-and-stop machinery
                                         fires more sparsely on ETH than on BTC
                                         under the locked thresholds).
ETH cannot rescue BTC:           CFP-4 enforces this and triggers because
                                  BTC M3 FAIL with degenerate ETH M4 trivial
                                  PASS (0=0 differential).
```

## M1 / M2 / M3 / M4 summary

```text
M1   active_minus_inactive_R           0.0   bootstrap CI [0.0, 0.0]   FAIL
       (G1 active n=0; inactive n=124; threshold +0.10R + CI_lower>0)
M2   g1_minus_always_active_R          0.0   bootstrap CI [0.0, 0.0]   FAIL
       (G1 n=0; always-active n=124; threshold +0.05R + CI_lower>0)
M3   btc_oos_high_mean_R               0.0   trade_count=0             FAIL
       (threshold mean_R>0 AND n>=30 AND no CFP-1/2/3)
M4   eth_diff_g1_minus_inactive_R      0.0   directional_consistency=true
                                                                       PASS (degenerate)
       (CFP-4 catches BTC FAIL + ETH "trivial PASS" combination)

Promotion-bar:  M1 PASS AND M2 PASS AND M3 PASS AND M4 PASS AND
                §11.6 HIGH cost-survival AND no CFP triggered  ->  NOT met
```

## PBO / DSR / CSCV summary

```text
PBO (train -> validation, rank-based proxy):    0.000
PBO (train -> OOS,        rank-based proxy):    0.000
PBO (CSCV S=16, C(16,8)=12,870 combinations):   0.500   (mechanically trivial
                                                          under widespread
                                                          zero-trade variants)
Deflated Sharpe per variant:    all 0.000  (training trade counts < 2 for
                                            all 32 variants; skew/kurtosis
                                            corrections inert on zero arrays;
                                            DSR is methodologically inert
                                            under the zero-trade root cause)
CFP-6 trigger (PBO > 0.50):     not triggered
                                  (rank-proxies = 0.0; CSCV = 0.500 not
                                  strictly > 0.50)
```

## Cost sensitivity summary

Across 32 variants × LOW / MEDIUM / HIGH cost cells × train / validation / OOS windows × BTC + ETH, the dominant pattern is `trade_count = 0` for the G1 population. HIGH cost (the §11.6 promotion gate) preserves the same null result: the regime-gate exclusion dominates the cost-sensitivity analysis. There is no "HIGH cost survives" finding for any G1 cell. Always-active baseline produces 124 BTC OOS HIGH trades with mean_R = −0.34 (loss-making at HIGH cost), confirming that even without the regime gate the breakout-and-stop mechanism is not profitable under §11.6 cost realism.

## Regime active-fraction summary

Selected representative rows (train-best variant id=0, BTCUSDT):

```text
window      total_30m  active_30m  long_active  short_active  active_fraction
train       26 208     944         448          496           0.03602
validation  17 568     256         168          88            0.01457
oos         30 672     624         416          208           0.02034   <-- CFP-9 trigger
```

Across all 32 variants, no variant exceeds the 5% active-fraction threshold on OOS. The mechanism observation: G1's locked 5-dimension classifier is structurally too narrow under the Phase 4p locked thresholds for the 30m breakout setup.

## Catastrophic-floor predicate summary

```text
CFP-1   TRIGGERED   Insufficient trade count (32/32 variants < 30; train-best 0)
CFP-2   not triggered
CFP-3   TRIGGERED   PF = 0 on empty arrays (mechanical; subordinate)
CFP-4   TRIGGERED   M3 BTC FAIL AND degenerate M4 ETH trivial PASS (subordinate)
CFP-5   not triggered   (train and OOS mean_R both 0)
CFP-6   not triggered   (PBOs 0.0 / 0.0 / 0.5)
CFP-7   not triggered   (no OOS trades; no concentration)
CFP-8   not triggered   (sensitivity cells produce zero trades; degradation 0)
CFP-9   TRIGGERED   regime-active fraction 2.03% < 5%
CFP-10  not triggered   audit count = 0 (no optional ratio column reads)
CFP-11  not triggered   (no future-bar use; no signal dependency;
                         signal_outside_active_count = 0)
CFP-12  not triggered   audit counts = 0 (no forbidden data access)
```

**Binding (independent) drivers: CFP-1 critical and CFP-9.** **Subordinate / mechanical: CFP-3 and CFP-4.** Any single CFP triggered = HARD REJECT (Phase 4q §"Verdict taxonomy").

## Commands run

```text
git status
git checkout -b phase-4r/g1-backtest-execution
.venv/Scripts/python --version
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m pytest -q (-> pytest)
.venv/Scripts/python -m mypy
# wrote scripts/phase4r_g1_backtest.py
.venv/Scripts/python -m ruff check scripts/phase4r_g1_backtest.py
.venv/Scripts/python -m ruff check . (final)
# static forbidden-import / forbidden-data scan via Python one-liner
.venv/Scripts/python scripts/phase4r_g1_backtest.py \
    --start 2022-01-01 --end 2026-03-31 \
    --train-start 2022-01-01 --train-end 2023-06-30 \
    --validation-start 2023-07-01 --validation-end 2024-06-30 \
    --oos-start 2024-07-01 --oos-end 2026-03-31 \
    --symbols BTCUSDT ETHUSDT --primary-symbol BTCUSDT \
    --comparison-symbol ETHUSDT --output-dir data/research/phase4r \
    --rng-seed 202604300
.venv/Scripts/python -m ruff check . (final post-run)
.venv/Scripts/python -m pytest (final post-run)
.venv/Scripts/python -m mypy (final post-run)
git add scripts/phase4r_g1_backtest.py docs/.../2026-04-30_phase-4r_g1-backtest-execution.md
git commit -m "phase-4r: G1 backtest execution (Verdict C HARD REJECT)"
git push -u origin phase-4r/g1-backtest-execution
```

No acquisition, diagnostics, or other backtest scripts were run.

## Verification results

```text
Python version             : 3.12.4
ruff check . (initial)     : All checks passed!
pytest (initial)           : 785 passed
mypy (initial)             : Success: no issues found in 82 source files
Backtest run               : completed successfully; verdict C reported.
Static forbidden-import scan : 0 forbidden imports.
Static forbidden-data scan : 4 audit-counter-only occurrences;
                              all guarded; runtime access count = 0.
ruff check . (final)       : All checks passed!
pytest (final)             : 785 passed in 13.33s
mypy (final)               : Success: no issues found in 82 source files
```

## Commit

```text
Phase 4r script + execution report commit:    a29ed5a5c4035bad2e5633e1b121eb76326e55d6
Phase 4r closeout commit:                     <recorded after this file is committed>
```

## Final git status

(recorded after closeout commit and push)

## Final git log --oneline -5

(recorded after closeout commit and push)

## Final rev-parse

```text
HEAD                                          : <recorded after closeout commit>
origin/phase-4r/g1-backtest-execution         : <recorded after closeout push>
main                                          : e019bee97edb689d5b36d5270bb577de04b2a24a (unchanged)
origin/main                                   : e019bee97edb689d5b36d5270bb577de04b2a24a (unchanged)
```

## Branch / main status

`main` remains unchanged at `e019bee97edb689d5b36d5270bb577de04b2a24a`. Phase 4r was authored exclusively on the `phase-4r/g1-backtest-execution` branch. Phase 4r is **not** merged to main by this closeout. Any future merge to main requires a separate explicit operator authorization brief (analogous to prior phase merge closeouts).

## Forbidden-work confirmation

Phase 4r did NOT do any of the following:

- start Phase 4s or any successor phase;
- implement G1 inside `src/prometheus/`;
- modify runtime / execution / persistence / risk / exchange / strategy code;
- modify any test;
- modify any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`);
- modify `data/raw/` / `data/normalized/` / `data/manifests/`;
- create new manifests;
- create v003;
- acquire data;
- download data;
- patch / forward-fill / interpolate / regenerate / replace data;
- run acquisition scripts;
- run diagnostics;
- rerun Q1–Q7;
- acquire mark-price data;
- acquire aggTrades;
- acquire spot data;
- acquire cross-venue data;
- use metrics OI;
- use optional metrics ratio columns;
- use 5m Q1–Q7 findings as regime indicators;
- use V2 Phase 4l stop-distance failure numbers to choose thresholds;
- modify Phase 4p G1 strategy-spec selections;
- modify Phase 4q methodology;
- modify Phase 4j §11 governance;
- modify Phase 4k methodology;
- revise retained verdicts;
- revise project locks, thresholds, parameters, or governance rules;
- change §11.6 / §1.7.3 / Phase 3r governance / Phase 3v governance / Phase 3w governance / Phase 4j governance / Phase 4k methodology;
- start Phase 4 canonical;
- create G1-prime / G1-extension / G1-narrow / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
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
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q
                            : all preserved verbatim
Phase 4r                    : G1 backtest execution Verdict C HARD REJECT
                              (this phase; new)
Recommended state           : paused
```

## Next authorization status

```text
Phase 4s                       : NOT authorized
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
G1-prime / G1-extension axes   : NOT authorized; not proposed
G1-narrow / G1 hybrid          : NOT authorized; not proposed
V2-prime / V2-variant          : NOT authorized; not proposed
Retained-evidence rescue       : NOT authorized; not proposed
5m strategy / hybrid           : NOT authorized; not proposed
ML feasibility                 : NOT authorized; not proposed
New family research            : NOT authorized at this boundary; would
                                  require a separately authorized
                                  fresh-hypothesis discovery memo under
                                  the Phase 4m 18-requirement validity
                                  gate.
Phase 4s post-mortem memo      : NOT authorized (recommended next; not yet
                                  authorized)
```

The next step is operator-driven: the operator decides whether to authorize Phase 4s (G1 post-mortem consolidation memo, docs-only, analogous to Phase 4m) or remain paused. Until then, the project remains at the post-Phase-4r G1 backtest-execution boundary.

---

**Phase 4r is docs-and-code. Verdict C — G1 framework HARD REJECT is the binding research outcome. G1 first-spec is terminally rejected as retained research evidence only. No project lock changed. No retained verdict revised. Recommended state remains paused. No next phase authorized.**
