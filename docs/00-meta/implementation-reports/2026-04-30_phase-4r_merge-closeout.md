# Phase 4r Merge Closeout

## Summary

Phase 4r — G1 Backtest Execution (docs-and-code) — has been merged into `main` via a no-fast-forward merge commit. Phase 4r implemented `scripts/phase4r_g1_backtest.py` as a standalone research backtest script (pyarrow + numpy + stdlib; no `prometheus.runtime/execution/persistence` imports; no exchange adapters; no `requests/httpx/aiohttp/websockets/urllib`; no `.env`; no credentials; no Binance API; no network I/O) and ran the predeclared G1 — Regime-First Breakout Continuation backtest exactly under the Phase 4q methodology. **Final Verdict: C — G1 framework HARD REJECT.** Binding driver: **CFP-1 critical** (32 / 32 variants below the 30-trade threshold on OOS BTC HIGH; the train-best variant produced 0 OOS HIGH trades). Independent driver: **CFP-9** (regime-active fraction 2.03% < 5%). Subordinate / mechanical: **CFP-3** (PF = 0 under empty arrays) and **CFP-4** (degenerate ETH "trivial PASS" — ETH cannot rescue BTC). G1 first-spec is terminally HARD REJECTED as retained research evidence only.

## Files changed

```text
scripts/phase4r_g1_backtest.py                                                         (added by merge)
docs/00-meta/implementation-reports/2026-04-30_phase-4r_g1-backtest-execution.md       (added by merge)
docs/00-meta/implementation-reports/2026-04-30_phase-4r_closeout.md                    (added by merge)
docs/00-meta/implementation-reports/2026-04-30_phase-4r_merge-closeout.md              (added by housekeeping commit — this file)
docs/00-meta/current-project-state.md                                                   (modified by housekeeping commit — narrow Phase 4r paragraph + "Current phase" / "Most recent merge" refresh)
```

No other files modified by Phase 4r or by this merge. Local outputs under `data/research/phase4r/` are gitignored and not committed.

## Phase 4r commits included

```text
a29ed5a5c4035bad2e5633e1b121eb76326e55d6   phase-4r: G1 backtest execution (Verdict C HARD REJECT)
26d8bc9d742404b36cce2326b27bf6edf71cc2b7   phase-4r: closeout (G1 backtest execution; Verdict C HARD REJECT)
```

## Merge commit

```text
24ab8355597c033ae57df25d7c5f8ec0c6a21542   Merge Phase 4r (G1 backtest execution; Verdict C HARD REJECT) into main
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

## Backtest execution conclusion

- Phase 4r was **docs-and-code standalone research execution**.
- Phase 4r implemented only `scripts/phase4r_g1_backtest.py` as a standalone research script (pyarrow + numpy + stdlib).
- Phase 4r ran the locked G1 backtest **exactly under the Phase 4q methodology**.
- Phase 4r did **not** implement G1 in `src/prometheus`.
- Phase 4r did **not** modify runtime, execution, persistence, risk, exchange, or strategy modules.
- Phase 4r did **not** modify tests.
- Phase 4r did **not** modify existing scripts.
- Phase 4r did **not** acquire, modify, patch, regenerate, or replace data.
- Phase 4r did **not** modify manifests.
- Phase 4r did **not** start any successor phase.

## Verdict

```text
Final Verdict:                C — G1 framework HARD REJECT.
Binding driver:               CFP-1 critical
                                (32 / 32 variants below 30 OOS BTC HIGH trades;
                                 BTC train-best variant produced 0 OOS HIGH
                                 trades).
Independent driver:           CFP-9
                                (BTC OOS regime-active fraction 2.03% < 5%).
Subordinate / mechanical:     CFP-3 and CFP-4.
G1 first-spec:                terminal.
G1 retained as:               research evidence only.
G1 rescue:                    not authorized; not proposed.
```

## Dataset inputs

```text
v002 trade-price klines (fallback / sanity only):
  binance_usdm_btcusdt_15m__v002
  binance_usdm_ethusdt_15m__v002
  binance_usdm_btcusdt_1h_derived__v002
  binance_usdm_ethusdt_1h_derived__v002

Phase 4i trade-price klines (research-eligible; primary G1 inputs):
  binance_usdm_btcusdt_30m__v001          (74 448 bars)
  binance_usdm_ethusdt_30m__v001          (74 448 bars)
  binance_usdm_btcusdt_4h__v001           ( 9 306 bars)
  binance_usdm_ethusdt_4h__v001           ( 9 306 bars)

v002 funding history:
  binance_usdm_btcusdt_funding__v002
  binance_usdm_ethusdt_funding__v002

Forbidden inputs (audit-zero by construction):
  - Phase 4i metrics OI subset (Phase 4j §11 governance preserved but unused)
  - Optional metrics ratio columns (Phase 4j §11.3 forbidden; not loaded)
  - Mark-price (any timeframe) (Phase 3r §8 governance preserved)
  - aggTrades (not loaded)
  - Spot data / cross-venue data (not loaded)
  - 5m diagnostic outputs as features (not loaded)
  - Modified manifests / v003 (not modified / not created)
```

All used manifests SHA256-pinned in the local `data/research/phase4r/tables/manifest_references.csv`.

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

`data/research/phase4r/` outputs are **not committed**.

## Forbidden input verification

```text
metrics_oi_access_count                    0
optional_ratio_column_access_count         0
mark_price_access_count                    0
aggtrades_access_count                     0
spot_access_count                          0
cross_venue_access_count                   0
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

The four substring occurrences in the script (`metrics_oi`, `mark_price`, `aggtrades`, `cross_venue`) are **audit-counter field names only**, recording `0` in `forbidden_work_confirmation.csv` and in the CFP-12 detail dict. Per Phase 4q §"Static scan nuance": "If the script must include forbidden names for guard checks, document why and ensure runtime access count is zero." All audited access counts are zero.

## BTCUSDT primary result summary

```text
Train-best variant id:        0
Variant label:                E=0.30|ATR=[20,80]|Vliq=0.80|Fund=[15,85]|K=2

G1 train-best OOS HIGH:
  trade_count                 0
  mean_R                      0
  total_R                     0
  sharpe                      0
  profit_factor               0
  max_dd_R                    0

G1 OOS HIGH (all 32 variants):  every variant has trade_count = 0.
Always-active baseline (id=0, BTC OOS HIGH):  124 trades; mean_R = -0.34.
Inactive-population pseudo (id=0, BTC OOS HIGH):  124 trades; mean_R = -0.34.
BTC OOS regime-active fraction (id=0):  2.03%   (CFP-9 < 5%; triggered).
```

The breakout machinery fired (124 always-active trades on BTC OOS HIGH at mean_R = −0.34 — confirming the breakout-and-stop simulation works), but the regime gate filtered out essentially all candidates.

## ETHUSDT comparison result summary

```text
BTC train-best variant id (carried to ETH):  0
ETH G1 (all windows × all cost cells × train-best):  trade_count = 0.
ETH cannot rescue BTC.
M4 trivial PASS:  degenerate (0=0 differential under empty populations);
                  CFP-4 catches this and triggers because of M3 BTC FAIL
                  combined with the trivial M4 PASS.
```

## M1 / M2 / M3 / M4 summary

```text
M1   active_minus_inactive_R           0.0   bootstrap CI [0.0, 0.0]   FAIL
       active n=0; inactive n=124 (mean_R = -0.34);
       differential degenerate; threshold +0.10R AND CI_lower>0 not met.

M2   g1_minus_always_active_R          0.0   bootstrap CI [0.0, 0.0]   FAIL
       G1 n=0; always-active n=124 (mean_R = -0.34);
       differential degenerate; threshold +0.05R AND CI_lower>0 not met.

M3   btc_oos_high_mean_R               0.0   trade_count=0             FAIL
       threshold mean_R > 0 AND trade_count >= 30 not met.

M4   eth_diff_g1_minus_inactive_R      0.0   directional_consistency=true
                                                                       PASS (degenerate)
       Both ETH G1 and ETH inactive populations are empty (0 vs 0);
       CFP-4 catches the degenerate ETH PASS combined with BTC M3 FAIL
       and triggers HARD REJECT.
```

## PBO / DSR / CSCV summary

```text
PBO (train -> validation, rank-based proxy):    0.000
PBO (train -> OOS,        rank-based proxy):    0.000
PBO (CSCV S=16, C(16,8)=12,870 combinations):   0.500   (mechanically trivial
                                                          under widespread
                                                          zero-trade variants)
Deflated Sharpe per variant:    all 0.000  (all 32 variants have train
                                            trade_count < 2; skew/kurtosis
                                            corrections inert under zero
                                            arrays; DSR is methodologically
                                            inert under the zero-trade root
                                            cause).
CSCV S=16; C(16, 8) = 12 870 combinations enumerated exactly.
PBO / DSR / CSCV are methodologically inert under the widespread zero-trade
variants; CFP-6 did not trigger (rank-proxies = 0.0; CSCV = 0.500 not
strictly > 0.50).
```

## Cost sensitivity summary

Across 32 variants × LOW / MEDIUM / HIGH cost cells × train / validation / OOS windows × BTC + ETH, the dominant pattern is `trade_count = 0` for the G1 population. HIGH cost (the §11.6 promotion gate) preserves the same null result: regime-gate exclusion dominates the cost-sensitivity analysis. There is no "HIGH cost survives" finding for any G1 cell. Always-active baseline (no regime gate) on BTC OOS HIGH produces 124 trades with mean_R = −0.34, confirming that even without the regime gate the breakout-and-stop mechanism is not profitable under §11.6 cost realism.

## Regime active-fraction summary

Selected representative rows (train-best variant id=0, BTCUSDT):

```text
window      total_30m  active_30m  long_active  short_active  active_fraction
train       26 208     944         448          496           0.03602
validation  17 568     256         168          88            0.01457
oos         30 672     624         416          208           0.02034   <-- CFP-9
```

Across all 32 variants on OOS, no variant exceeds the 5% active-fraction threshold. The mechanism observation: G1's locked 5-dimension classifier is structurally too narrow under the Phase 4p locked thresholds for the 30m breakout setup.

## Catastrophic-floor predicate summary

```text
CFP-1   TRIGGERED   binding (critical)
                    32 / 32 variants below the 30-trade threshold on
                    OOS BTC HIGH; train-best variant produced 0 OOS HIGH
                    trades.
CFP-2   not triggered     no variant with mean_R <= -0.20R (all G1 means
                          are 0 under zero trades).
CFP-3   TRIGGERED   subordinate / mechanical
                    profit_factor = 0 under empty arrays; PF < 0.50
                    triggered for every variant; subordinate to the
                    zero-trade root cause.
CFP-4   TRIGGERED   subordinate / degenerate
                    M3 BTC FAIL AND degenerate M4 ETH "trivial PASS"
                    (0=0 differential under empty populations).
                    ETH cannot rescue BTC.
CFP-5   not triggered     train mean_R = 0 and OOS mean_R = 0; condition
                          (train > 0 AND oos <= 0) is false.
CFP-6   not triggered     PBOs 0.0 / 0.0 / 0.5; not strictly > 0.50.
CFP-7   not triggered     no OOS HIGH G1 trades; no concentration to
                          assess.
CFP-8   not triggered     sensitivity cells also produce zero trades;
                          degradation 0.0; non-degraded by construction.
CFP-9   TRIGGERED   independent
                    BTC OOS active fraction 2.03% < 5%.
CFP-10  not triggered     audit count = 0 (no optional ratio column reads).
CFP-11  not triggered     no future-bar use; no signal dependency;
                          signal_outside_active_count = 0.
CFP-12  not triggered     audit counts = 0 for all forbidden inputs.
```

**Any single CFP triggered = HARD REJECT.** G1 has multiple triggers; binding drivers are CFP-1 (critical) and CFP-9 (independent / structural).

## Required tables / plots summary

- All 25 required reporting tables produced under `data/research/phase4r/tables/` (gitignored; not committed).
- All 11 required plots attempted but **skipped** because matplotlib was unavailable in the project virtualenv. The script's plot helpers are guarded with try-import and degrade gracefully.
- Plot absence does **not** change Verdict C: verdict-driving evidence (tables, mechanism checks, CFP results, verdict declaration) is complete and unaffected.
- `data/research/phase4r/` outputs are not committed; they are reproducible from `scripts/phase4r_g1_backtest.py` with the pinned RNG seed 202604300.

## Verification evidence

```text
Python version             : 3.12.4
ruff check . (initial)     : All checks passed!
pytest (initial)           : 785 passed
mypy (initial)             : Success: no issues found in 82 source files
Backtest run               : completed successfully; verdict C reported.
Static forbidden-import scan : 0 forbidden imports.
Static forbidden-data scan : audit-counter field names only;
                              runtime access count = 0.
ruff check . (final)       : All checks passed!
pytest (final)             : 785 passed in 13.33s
mypy (final)               : Success: no issues found in 82 source files
```

## Forbidden-work confirmation

Phase 4r and this merge did NOT do any of the following:

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
Phase 4r                    : G1 backtest execution; Verdict C HARD REJECT
                              (this phase; merged)
Recommended state           : paused
```

## Operator decision menu

- **Option A — recommended next:** Phase 4s — Post-G1 Strategy Research Consolidation Memo (docs-only), analogous to Phase 4m (post-V2) / Phase 3e (post-F1) / Phase 3k (post-D1-A) precedents. Phase 4s would consolidate the G1 outcome into the project's research record, document the four-fold rejection topology now on file (R2 cost-fragility; F1 catastrophic-floor; D1-A mechanism-vs-framework mismatch; V2 design-stage incompatibility; G1 regime-gate-meets-setup intersection sparseness), preserve forbidden-rescue observations, and either recommend remain-paused or recommend a new fresh-hypothesis discovery memo under the Phase 4m 18-requirement validity gate.
- **Option B — conditional secondary:** remain paused.

NOT recommended:

- G1 rescue (G1-prime / G1-narrow / G1-extension / classifier amendment / K_confirm amendment / band amendment / E_min amendment / breakout-rule amendment / stop-distance bound amendment); REJECTED;
- immediate G1 implementation; REJECTED;
- immediate data acquisition; REJECTED;
- paper / shadow / live-readiness; FORBIDDEN;
- Phase 4 canonical; FORBIDDEN;
- exchange-write / production keys / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work; FORBIDDEN;
- V2 / F1 / D1-A / R2 rescue; FORBIDDEN.

Any new family research requires a separately authorized fresh-hypothesis discovery memo under the Phase 4m 18-requirement validity gate.

**Phase 4s is NOT started by this merge.** Phase 4s execution requires a separate explicit operator authorization brief.

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
```

The next step is operator-driven: the operator decides whether to authorize Phase 4s (G1 post-mortem consolidation memo, docs-only) or remain paused. Until then, the project remains at the post-Phase-4r G1 backtest-execution boundary.

---

**Phase 4r was docs-and-code. Verdict C — G1 framework HARD REJECT is the binding research outcome. G1 first-spec is terminally rejected as retained research evidence only. No project lock changed. No retained verdict revised. Recommended state remains paused. No next phase authorized.**
