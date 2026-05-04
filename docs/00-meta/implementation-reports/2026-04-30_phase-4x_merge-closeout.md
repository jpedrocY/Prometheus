# Phase 4x Merge Closeout

## Summary

Phase 4x (C1 Backtest Execution; Verdict C HARD REJECT) was merged into `main` via a `--no-ff` merge commit. Phase 4x implemented `scripts/phase4x_c1_backtest.py` exactly under the Phase 4w methodology and ran the predeclared C1 — Volatility-Contraction Expansion Breakout backtest on BTCUSDT primary / ETHUSDT comparison across LOW / MEDIUM / HIGH cost cells over the train (2022-01-01..2023-06-30 UTC) / validation (2023-07-01..2024-06-30 UTC) / OOS holdout (2024-07-01..2026-03-31 UTC) windows; evaluated 32 variants (= 2^5) over five binary axes; computed M1 / M2 / M3 / M4 / M5 with bootstrap (B = 10 000; pinned RNG seed 202604300); computed deflated Sharpe with N = 32, PBO (train→validation rank-based; train→OOS rank-based; CSCV S = 16 with C(16, 8) = 12 870 combinations); evaluated 12 catastrophic-floor predicates (CFP-1..CFP-12); declared Verdict A / B / C / D. **Final Verdict: C — C1 framework HARD REJECT.** Whole-repo quality gates remained clean throughout (ruff PASS; pytest 785 PASS; mypy strict 0 issues across 82 source files). **C1 first-spec is terminally HARD REJECTED as retained research evidence only.** No next phase authorized.

## Files changed

```text
scripts/phase4x_c1_backtest.py                                                    (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4x_c1-backtest-execution.md  (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4x_closeout.md               (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4x_merge-closeout.md         (new; this file)
docs/00-meta/current-project-state.md                                             (narrow Phase 4x sync)
```

No source under `src/prometheus/` modified. No tests modified. No existing scripts modified. No data, manifests, or `.gitignore` modified. Local research outputs under `data/research/phase4x/` are gitignored and NOT committed.

## Phase 4x commits included

```text
33d34f1  phase-4x: C1 backtest execution (Verdict C HARD REJECT)
f37798b  phase-4x: closeout (Verdict C HARD REJECT)
```

## Merge commit

```text
SHA:    e28e34a2878d9a6b602e0f2e26eafdf787cfbb59
Title:  Merge Phase 4x (C1 backtest execution; Verdict C HARD REJECT) into main
Type:   --no-ff merge of phase-4x/c1-backtest-execution into main
```

## Housekeeping commit

The merge-closeout file (this file) and the narrow Phase 4x sync to `docs/00-meta/current-project-state.md` are committed as a single docs-only housekeeping commit on `main` after the merge. The housekeeping commit SHA is recorded below in `Final git log --oneline -8`.

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

## Backtest execution conclusion

- **Phase 4x was docs-and-code in standalone-script mode.**
- Phase 4x implemented `scripts/phase4x_c1_backtest.py` exactly under the Phase 4w methodology.
- Phase 4x executed the C1 first-spec backtest.
- Phase 4x produced **Verdict C — C1 framework HARD REJECT.**
- **C1 first-spec is terminally HARD REJECTED as retained research evidence only.**
- C1 remains:
  - not implemented;
  - not validated;
  - not live-ready;
  - **not a rescue of R3 / R2 / F1 / D1-A / V2 / G1.**
- Phase 4x does NOT authorize Phase 4y.
- Phase 4x does NOT authorize implementation, data acquisition, paper / shadow / live, or exchange-write.
- No retained verdict is revised.
- No project lock is changed.

## Verdict

```text
Verdict       : C — C1 framework HARD REJECT
Binding driver:
  CFP-2 — BTC OOS HIGH train-best mean_R = -0.3633 <= 0
Co-binding / independent drivers:
  CFP-3 — profit_factor = 0.4413 < 0.50
          AND max_drawdown_R = 54.55 > 10R
  CFP-6 — DSR = -20.8173 <= 0
Disposition  : Terminal C1 first-spec rejection.
```

## Dataset inputs

```text
Required (research-eligible per Phase 4i; loaded as primary signal):
  binance_usdm_btcusdt_30m__v001
    sha256: 3cdf6fb91ffca8acc2a69ae05a00745a031360c01c585a75f876c64d42230da8
    bars:   74 448 over 2022-01-01..2026-03-31 UTC
  binance_usdm_ethusdt_30m__v001
    sha256: 0a7502c5e09916529e50951bd503e1a2ac95d372e99ba65f4cb3bfb1477e3afd
    bars:   74 448 over 2022-01-01..2026-03-31 UTC

Manifests verified research_eligible=True. SHAs pinned in
run_metadata.json and manifest_references.csv.

Not loaded (excluded from C1 first-spec):
  funding (any version); metrics (any version);
  mark-price (any timeframe); aggTrades; spot; cross-venue;
  order book; optional reporting-context only datasets.
```

## Local result artefacts

`data/research/phase4x/` (gitignored; not committed; reproducible from the script with pinned RNG seed 202604300):

```text
run_metadata.json
tables/   (33 tables; 32 Phase 4w-required + forbidden_work_confirmation.csv)
plots/    (empty; matplotlib unavailable in venv)
```

**Plot absence:** does NOT cause Verdict D because all binding tables are complete and absence is documented (per Phase 4w explicit rule).

## Forbidden input verification

Per `data/research/phase4x/tables/forbidden_work_confirmation.csv` — all audit counters 0 by construction:

```text
metrics_oi_access_count                : 0
optional_ratio_column_access_count     : 0
mark_price_access_count                : 0
aggtrades_access_count                 : 0
spot_access_count                      : 0
cross_venue_access_count               : 0
network_io_attempts                    : 0
credential_reads                       : 0
env_file_reads                         : 0
data_raw_writes                        : 0
data_normalized_writes                 : 0
data_manifest_modifications            : 0
v003_creations                         : 0
src_prometheus_modifications           : 0
test_modifications                     : 0
existing_script_modifications          : 0
```

Static forbidden-import scan: 0 occurrences across all 10 forbidden import names. Static forbidden-data-name scan: occurrences confined to required CFP-12 audit-counter field names per Phase 4w spec; runtime access counts all 0.

## BTCUSDT primary result summary

Train-best variant **id = 21**; label = `B=0.10|C=0.45|N=12|S=0.10|T=2.0` (B_width=0.10, C_width=0.45, N_comp=12, S_buffer=0.10, T_mult=2.0, T_stop_bars=24).

```text
BTC OOS HIGH (train-best variant 21):
  trade_count   : 149
  mean_R        : -0.3633
  total_R       : -54.1258
  max_dd_R      :  54.55
  profit_factor :   0.4413
  sharpe        :  -0.3721
```

**All 32 BTC OOS HIGH variants are loss-making** (mean_R range −0.10 to −0.44).

Cost-cell sensitivity (BTC OOS, train-best variant 21):

```text
LOW    (1bp)  : mean_R = -0.1701
MEDIUM (4bps) : mean_R = -0.2529
HIGH   (8bps) : mean_R = -0.3633
```

**Cost is NOT the binding driver** — the strategy is structurally loss-making even before HIGH cost amplification.

## ETHUSDT comparison result summary

Same train-best variant id = 21:

```text
ETH OOS HIGH:
  trade_count   : 109
  mean_R        : -0.2140
  profit_factor :   0.6252
  sharpe        :  -0.2148
```

**All 32 ETH OOS HIGH variants are loss-making** (mean_R range −0.10 to −0.24).

**ETH cannot rescue BTC** (CFP-4 rule honored; ETH also fails M3-comparator so no false-positive rescue).

## M1 / M2 / M3 / M4 / M5 summary

```text
M1 FAIL:
  diff = -0.2440R
  CI   = [-0.4101, -0.0810]   (strictly negative)
  C1 transitions perform 0.244R worse than non-contraction baseline.
  Threshold: diff >= +0.10R AND CI lower > 0.

M2 FAIL:
  M2.a diff = -0.2201R
  M2.a CI   = [-0.3859, -0.0556]   (strictly negative)
  M2.b diff = -0.2930R
  C1 transitions worse than always-active-same-geometry baseline AND
  worse than delayed-breakout baseline.

M3 FAIL:
  BTC OOS HIGH mean_R = -0.3633 <= 0
  trade_count = 149 (>= 30; PASS on this leg)
  opportunity-rate floors PASS
  CFP-2 / CFP-3 trigger.

M4 FAIL:
  ETH differential = -0.1589
  Directional consistency YES (both BTC and ETH negative)
  ETH cannot rescue BTC.

M5 DIAGNOSTIC_ONLY:
  Skipped per Phase 4w optional handling.
  No verdict effect.
```

## PBO / DSR / CSCV summary

```text
PBO_train_validation : 0.375    (below 0.50)
PBO_train_oos        : 0.219    (below 0.50)
PBO_cscv             : 0.094    (below 0.50)
All PBO values below 0.50 threshold.

DSR (train-best, N=32) : -20.8173
DSR <= 0 triggers CFP-6.

CFP-6 triggers via DSR, NOT via PBO.
```

PBO does not detect overfitting because the strategy is loss-making across nearly all variants (no "lucky" overfit subset to detect). DSR magnifies the negative train-best raw Sharpe (-0.363) into a strongly negative DSR.

## Cost sensitivity summary

```text
Cost cell      | mean_R   | profit_factor | sharpe
---------------+----------+---------------+---------
LOW   (1bp)    | -0.1701  | 0.6804        | -0.1751
MEDIUM (4bps)  | -0.2529  | 0.5655        | -0.2600
HIGH  (8bps)   | -0.3633  | 0.4413        | -0.3721
```

Cost is NOT the binding driver of the failure.

## Opportunity-rate summary

```text
total_30m_bars                       : 30 672
oos_total_transitions                : 213
transition_rate_per_480_bars         : 3.33    (>= 1.0; OK)
train-best OOS HIGH executed trades  : 149     (>= 30; OK)
variants with >= 30 BTC OOS HIGH trades : 32 / 32 (100.0%; >= 50%; OK)

CFP-1 NOT triggered.
CFP-9 NOT triggered.
```

**The failure is not opportunity-rate collapse.** C1's opportunity-rate framework is empirically validated as healthy.

## Catastrophic-floor predicate summary

```text
CFP-1  | OK
CFP-2  | TRIGGER  (binding driver: BTC OOS HIGH train-best mean_R <= 0)
CFP-3  | TRIGGER  (PF=0.4413 < 0.50; max_dd_R=54.55 > 10R)
CFP-4  | OK       (BTC fail AND ETH fail; no rescue scenario)
CFP-5  | OK       (train HIGH already negative; OOS-only failure absent)
CFP-6  | TRIGGER  (DSR=-20.8173 <= 0; PBO all below 0.50)
CFP-7  | OK
CFP-8  | OK
CFP-9  | OK
CFP-10 | OK
CFP-11 | OK
CFP-12 | OK
```

**Any triggered CFP = Verdict C HARD REJECT.** **Binding driver is CFP-2** (lowest-numbered triggered CFP per Phase 4w precedence). CFP-3 and CFP-6 are co-binding independent drivers.

## Categorical comparison with V2 / G1

```text
V2 (Phase 4l):
  Failure mode    : design-stage incompatibility
  Binding driver  : CFP-1 critical (zero trades from stop-distance filter)
  Trade count     : 0 BTC OOS HIGH C1 trades for train-best variant

G1 (Phase 4r):
  Failure mode    : regime-gate-meets-setup intersection sparseness
  Binding driver  : CFP-1 critical (zero qualifying trades from broad
                     regime gate)
  Independent     : CFP-9 (regime active fraction 2.03% < 5%)
  Trade count     : 0 BTC OOS HIGH G1 trades for train-best variant

C1 (Phase 4x; THIS PHASE):
  Failure mode    : "fires-and-loses" / contraction anti-validation
                    (categorically distinct from V2 / G1)
  Binding driver  : CFP-2 (negative BTC OOS HIGH expectancy)
  Co-binding      : CFP-3 (PF / drawdown), CFP-6 (DSR)
  Trade count     : 149 BTC OOS HIGH C1 trades for train-best variant
                    (well above 30-trade floor)
  Opportunity rate: 3.33 transitions per 480 bars (well above 1.0
                    floor); 100% of variants produce >= 30 trades
                    (CFP-1 / CFP-9 explicitly do NOT trigger)
  Anti-validation : contraction-tied transitions perform 0.244R
                    worse than non-contraction baseline (CI strictly
                    negative); 0.220R worse than always-active
                    baseline; 0.293R worse than delayed-breakout
                    baseline. Contraction is empirically
                    anti-predictive in this implementation.
```

**C1's new rejection mode: "fires-and-loses" / contraction anti-validation.** No C1 rescue is authorized.

## Recommended next operator choice

- **Option A — primary recommendation:** remain paused. Phase 4x has produced a clean Verdict C HARD REJECT for C1 first-spec. The project record now contains six terminal strategy verdicts (R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL; V2 HARD REJECT; G1 HARD REJECT; C1 HARD REJECT) plus the H0 framework anchor and R3 baseline-of-record (with R1a / R1b-narrow as retained non-leading research evidence). No new ex-ante hypothesis is currently under consideration. Remaining paused gives the operator time to review the post-C1 evidence before authorizing any successor phase.
- **Option B — conditional secondary:** Phase 4y — Post-C1 Strategy Research Consolidation Memo (docs-only), analogous to Phase 4s (post-G1) and Phase 4m (post-V2). Phase 4y would consolidate Phase 4x findings into the project's strategy-research record, update the rejection topology with C1's distinct failure mode (fires-and-loses; contraction anti-validation), and reaffirm every retained verdict / project lock without authorizing rescue or successor. **Phase 4y is NOT started by this merge.**

NOT recommended:

- immediate C1 implementation in `src/prometheus/` — REJECTED;
- immediate C1 rerun — REJECTED;
- C1-prime / C1-extension / C1-narrow / C1 hybrid — FORBIDDEN;
- C1 spec amendment based on Phase 4x forensic numbers — FORBIDDEN;
- Phase 4w methodology amendment based on Phase 4x forensic numbers — FORBIDDEN;
- data acquisition — REJECTED;
- paper / shadow / live / exchange-write — FORBIDDEN;
- Phase 4 canonical — FORBIDDEN.

## Verification evidence

```text
ruff check .                : All checks passed!
pytest                      : 785 passed (no regressions)
mypy strict                 : Success: no issues in 82 source files
```

(Verified during Phase 4x branch work and after the no-ff merge to main; gates remain clean post-merge by construction since no source / test / script changes occurred.)

## Forbidden-work confirmation

Phase 4x (and this merge) did NOT do any of the following:

- modify `src/prometheus/`;
- modify any test;
- modify any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`);
- run any acquisition / diagnostics / prior-phase backtest script;
- acquire data;
- download data;
- patch / forward-fill / interpolate / regenerate / replace data;
- modify any manifest;
- create any new manifest;
- create v003;
- modify Phase 4p / Phase 4q / Phase 4j §11 / Phase 4k / Phase 4v / Phase 4w / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r §8 governance;
- revise any retained verdict;
- change any project lock;
- create a runnable strategy under `src/prometheus/`;
- create G1-prime / G1-narrow / G1-extension / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- create C1-prime / C1-narrow / C1-extension / C1 hybrid;
- propose a 5m strategy / hybrid / variant;
- start Phase 4y / 4 canonical / paper-shadow / live-readiness / deployment / production-key creation / exchange-write capability / authenticated REST / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- consult any private endpoint / user stream / WebSocket / authenticated REST in code;
- store, request, or display any secret;
- perform web research that collected market data, downloaded archives, called Binance APIs, called `data.binance.vision`, scraped prices, created datasets, or imported online thresholds as adopted project values;
- use Phase 4x C1 forensic numbers to choose new C1 thresholds.

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
                       binding; CFP-9 independent; terminal for G1 first-spec)
C1                  : HARD REJECT (Phase 4x — Verdict C; CFP-2 binding;
                       CFP-3 / CFP-6 co-binding; terminal for C1 first-spec)
5m diagnostic thread : OPERATIONALLY CLOSED (Phase 3t)
§11.6               : 8 bps HIGH per side (preserved verbatim)
§1.7.3              : 0.25% risk / 2× leverage / 1 position / mark-price
                       stops (preserved)
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m
                              (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance
                              (preserved)
Phase 4a runtime            : public API and behavior (preserved)
Phase 4e                    : reconciliation-model design memo (preserved)
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q / 4r / 4s / 4t / 4u / 4v / 4w
                            : all preserved verbatim
Phase 4x                    : C1 backtest execution; Verdict C HARD REJECT
                              (this phase; merged to main; docs-and-code)
C1                          : pre-research only;
                              hypothesis-spec defined in Phase 4u;
                              strategy-spec defined in Phase 4v;
                              backtest-plan methodology defined in Phase 4w;
                              backtest executed in Phase 4x (this phase);
                              terminally HARD REJECTED;
                              not implemented; not validated; not live-ready;
                              not a rescue of R3 / R2 / F1 / D1-A / V2 / G1
Recommended state           : remain paused;
                              post-C1 consolidation memo (Phase 4y, analogous
                              to Phase 4s post-G1) conditional secondary
```

## Next authorization status

```text
Phase 4y (post-C1 consolidation): NOT authorized
Phase 4z and beyond              : NOT authorized
Phase 4 (canonical)              : NOT authorized
Paper / shadow                   : NOT authorized
Live-readiness                   : NOT authorized
Deployment                       : NOT authorized
Production-key creation          : NOT authorized
Authenticated REST               : NOT authorized
Private endpoints                : NOT authorized
User stream / WebSocket          : NOT authorized
Exchange-write capability        : NOT authorized
MCP / Graphify                   : NOT authorized
.mcp.json / credentials          : NOT authorized
C1 implementation                : NOT authorized; terminal-rejected
C1 rerun                         : NOT authorized; terminal-rejected
C1 spec amendment                : NOT authorized; FORBIDDEN
Phase 4w methodology amendment   : NOT authorized; FORBIDDEN
G1 / V2 / R2 / F1 / D1-A rescue  : NOT authorized; FORBIDDEN
G1-prime / G1-extension axes     : NOT authorized; FORBIDDEN
V2-prime / V2-variant            : NOT authorized; FORBIDDEN
C1-prime / C1-extension          : NOT authorized; FORBIDDEN
Retained-evidence rescue         : NOT authorized; FORBIDDEN
5m strategy / hybrid             : NOT authorized; not proposed
ML feasibility                   : NOT authorized; not proposed
Microstructure / liquidity-timing data acquisition (Phase 4t Candidate F)
                                 : NOT authorized; data unavailable
Mark-price / aggTrades / spot / cross-venue acquisition
                                 : NOT authorized; FORBIDDEN
```

The next step is operator-driven: the operator decides whether to remain paused or authorize Phase 4y (Post-C1 Strategy Research Consolidation Memo, docs-only). Until then, the project remains at the post-Phase-4x C1 HARD REJECT boundary on `main`.

---

**Phase 4x is docs-and-code in standalone-script mode and has been merged into `main`. No source code, tests, existing scripts, data, manifests, or successor phases were created or modified. Final Verdict: C — C1 framework HARD REJECT (CFP-2 binding; CFP-3 / CFP-6 co-binding; terminal for C1 first-spec). Recommended state: remain paused; post-C1 consolidation memo (Phase 4y) conditional secondary. No next phase authorized.**
