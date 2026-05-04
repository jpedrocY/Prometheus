# Phase 4x Closeout

## Summary

Phase 4x implemented `scripts/phase4x_c1_backtest.py` exactly under the Phase 4w methodology and ran the predeclared C1 — Volatility-Contraction Expansion Breakout backtest on BTCUSDT primary / ETHUSDT comparison across LOW / MEDIUM / HIGH cost cells over the train (2022-01-01..2023-06-30 UTC) / validation (2023-07-01..2024-06-30 UTC) / OOS holdout (2024-07-01..2026-03-31 UTC) windows; evaluated 32 variants (= 2^5) over five binary axes; computed M1 / M2 / M3 / M4 / M5 with bootstrap (B = 10 000; pinned RNG seed 202604300); computed deflated Sharpe with N = 32, PBO (train→validation rank-based; train→OOS rank-based; CSCV S = 16 with C(16, 8) = 12 870 combinations); evaluated 12 catastrophic-floor predicates (CFP-1..CFP-12); declared Verdict A / B / C / D. **Final Verdict: C — C1 framework HARD REJECT.** Binding catastrophic-floor drivers: CFP-2, CFP-3, CFP-6. Whole-repo quality gates remain clean: ruff PASS; pytest 785 PASS; mypy strict 0 issues across 82 source files. **C1 first-spec is terminally HARD REJECTED as retained research evidence only.** No next phase authorized.

## Files changed

```text
scripts/phase4x_c1_backtest.py                                                    (new; ~2300 lines)
docs/00-meta/implementation-reports/2026-04-30_phase-4x_c1-backtest-execution.md  (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4x_closeout.md               (new; this file)
```

No source under `src/prometheus/` modified. No tests modified. No existing scripts modified. No data, manifests, or `.gitignore` modified. Local research outputs under `data/research/phase4x/` are gitignored and NOT committed.

## Backtest execution conclusion

Phase 4x ran the full predeclared C1 backtest exactly under the Phase 4w methodology — 32 variants × 2 symbols × 3 cost cells × 4 populations (C1 transitions, non-contraction baseline, always-active-same-geometry baseline, delayed-breakout baseline) = 768 simulations — and emitted Verdict C HARD REJECT. The strategy fired 149 BTC OOS HIGH trades for the train-best variant (well above the M3 ≥ 30 floor), 213 OOS candidate transitions, transition rate 3.33 per 480 30m bars (well above the ≥ 1 floor), 100% of variants producing ≥ 30 trades — but the strategy is **structurally loss-making across all 32 variants, all three windows, and all three cost cells**. CFP-1 / CFP-9 explicitly do NOT trigger; the failure mode is "fires-and-loses" (categorically distinct from V2 / G1 zero-trade collapses). Forensic observation: contraction-tied transitions perform 0.244R **worse** than the same close-beyond-buffer rule fired without the contraction precondition (bootstrap CI [-0.4101, -0.0810] strictly negative); contraction is empirically *anti-predictive* in this implementation.

## Verdict

```text
Verdict       : C — C1 framework HARD REJECT
Basis         : CFP triggered (HARD REJECT): CFP-2, CFP-3, CFP-6
M1 pass       : False  (contraction-state validity: -0.244R diff;
                CI [-0.410, -0.081] strictly negative)
M2 pass       : False  (M2.a: -0.220R diff; CI strictly negative;
                M2.b: -0.293R diff; both sub-criteria FAIL)
M3 pass       : False  (BTC OOS HIGH mean_R = -0.3633 <= 0;
                CFP-2 / CFP-3 trigger; opportunity-rate floors PASS)
M4 pass       : False  (ETH non-negative differential FAIL: -0.159R;
                directional consistency YES; ETH cannot rescue BTC)
M5            : DIAGNOSTIC_ONLY (skipped per Phase 4w optional)
Best variant  : id=21, label=B=0.10|C=0.45|N=12|S=0.10|T=2.0
                (B_width=0.10, C_width=0.45, N_comp=12,
                 S_buffer=0.10, T_mult=2.0, T_stop_bars=24)
Run complete  : 2026-05-04T01:09:11.031198+00:00 UTC
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
  mark-price (any timeframe); aggTrades; spot; cross-venue; order book;
  optional reporting-context only datasets (4h v001; 15m v002;
  1h-derived v002).
```

## Local result artefacts

`data/research/phase4x/` (gitignored; not committed; reproducible from the script with pinned RNG seed 202604300):

```text
run_metadata.json
tables/  (33 binding tables; 32 Phase 4w-required + forbidden_work_confirmation.csv)
plots/   (empty; matplotlib unavailable in venv; per Phase 4w, plot
         absence does NOT cause Verdict D when binding tables are
         complete and absence is documented)
```

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

Static forbidden-import scan: 0 occurrences across all 10 forbidden import names (requests, httpx, aiohttp, urllib3, urllib.request, websockets, websocket, prometheus.runtime, prometheus.execution, prometheus.persistence). Static forbidden-data-name scan: occurrences of `metrics`, `mark_price`, `aggTrades`, `spot`, `cross-venue` confined to module docstring, data-loading boundary comment, required CFP-12 audit-counter field names per Phase 4w spec, and required forbidden_work_confirmation.csv row labels per Phase 4w spec; runtime access counts all 0.

## BTCUSDT primary result summary

Train-best variant 21 (`B=0.10|C=0.45|N=12|S=0.10|T=2.0`):

```text
Window         | Cell    | n   | win_rate | mean_R   | total_R   | max_dd_R | PF     | sharpe
---------------+---------+-----+----------+----------+-----------+----------+--------+--------
train          | LOW     |  93 |   33.3 % | -0.3095  |  -28.7789 |   30.51  | 0.5417 | -0.2941
train          | MEDIUM  |  93 |   32.3 % | -0.3816  |  -35.4875 |   37.05  | 0.4715 | -0.3635
train          | HIGH    |  93 |   32.3 % | -0.4778  |  -44.4322 |   45.78  | 0.3912 | -0.4554
validation     | LOW     |  90 |   34.4 % | -0.3688  |  -33.1932 |   33.88  | 0.4636 | -0.3616
validation     | MEDIUM  |  90 |   33.3 % | -0.4733  |  -42.5950 |   42.83  | 0.3815 | -0.4530
validation     | HIGH    |  90 |   30.0 % | -0.6126  |  -55.1306 |   55.23  | 0.2976 | -0.5654
oos            | LOW     | 149 |   41.6 % | -0.1701  |  -25.3422 |   28.46  | 0.6804 | -0.1751
oos            | MEDIUM  | 149 |   38.3 % | -0.2529  |  -37.6780 |   39.05  | 0.5655 | -0.2600
oos            | HIGH    | 149 |   37.6 % | -0.3633  |  -54.1258 |   54.55  | 0.4413 | -0.3721
```

Strategy is loss-making across all windows and all cost cells. Even at LOW cost (1 bp slippage; below the realistic taker-fee floor) the strategy is still loss-making. All 32 BTC OOS HIGH variants are loss-making (mean_R range −0.10 to −0.44).

## ETHUSDT comparison result summary

Same train-best variant_id = 21 carried into ETH:

```text
ETH OOS HIGH:    n=109,  mean_R=-0.2140,  PF=0.6252,  sharpe=-0.2148
```

ETH performs slightly less badly than BTC but is still negative across all 32 variants (mean_R range −0.10 to −0.24). **ETH cannot rescue BTC.** M4 differential is negative; directional consistency holds (both BTC and ETH negative); CFP-4 ((not M3) AND M4) does NOT trigger because M4 also fails.

## M1 / M2 / M3 / M4 / M5 summary

```text
M1   FAIL   diff = -0.2440  CI = [-0.4101, -0.0810]
            (C1 vs non-contraction; threshold >= +0.10R AND CI low > 0)
M2.a FAIL   diff = -0.2201  CI = [-0.3859, -0.0556]
            (C1 vs always-active-same-geometry; threshold >= +0.05R
             AND CI low > 0)
M2.b FAIL   diff = -0.2930
            (C1 vs delayed-breakout; threshold >= 0R)
M2 (combined) FAIL  (M2.a AND M2.b both FAIL)
M3   FAIL   mean_R = -0.3633  trade_count = 149
            (BTC OOS HIGH mean_R > 0 FAIL; trade_count >= 30 PASS;
             CFP-1/9 OK; CFP-2/3 TRIGGER; opportunity-rate floors PASS)
M4   FAIL   eth_diff = -0.1589  btc_diff = -0.2440
            (ETH non-negative differential FAIL;
             directional consistency YES; ETH cannot rescue BTC)
M5   DIAGNOSTIC_ONLY  (skipped per Phase 4w; does not affect verdict)
```

## PBO / DSR / CSCV summary

```text
PBO_train_validation (rank-based)  : 0.375   (below 0.50; CFP-6 OK on this leg)
PBO_train_oos (rank-based)         : 0.219   (below 0.50; CFP-6 OK on this leg)
PBO_cscv (S=16; C(16,8)=12 870)    : 0.094   (below 0.50; CFP-6 OK on this leg)
DSR (train-best, N=32)             : -20.8173  (<= 0; CFP-6 TRIGGERED via DSR)
```

PBO does not detect overfitting because the strategy is loss-making across nearly all variants (no "lucky" overfit subset to detect). DSR triggers CFP-6 because the train-best raw Sharpe is -0.363 and the deflation magnifies the negative value.

## Cost sensitivity summary

Train-best variant 21 BTC OOS:

```text
Cost cell      | mean_R   | profit_factor | sharpe
---------------+----------+---------------+---------
LOW   (1bp)    | -0.1701  | 0.6804        | -0.1751
MEDIUM (4bps)  | -0.2529  | 0.5655        | -0.2600
HIGH  (8bps)   | -0.3633  | 0.4413        | -0.3721
```

Cost is NOT the binding driver of the failure; the strategy is structurally loss-making before costs are amplified.

## Opportunity-rate summary

```text
BTC OOS window:
  total_30m_bars                       : 30 672
  oos_total_transitions (long+short)   : 213
  transition_rate_per_480_bars         : 3.33  (>= 1.0; OK)
  train-best OOS HIGH trade_count      : 149   (>= 30; OK)
  variants with >= 30 BTC OOS HIGH trades : 32 / 32 (100.0%; >= 50%; OK)
  CFP-9 (sparse-intersection collapse) : NOT TRIGGERED
```

C1's opportunity-rate framework is empirically validated as healthy. The strategy fires plenty of candidates. **The failure is not "no opportunity," it is "the opportunity is loss-making."**

## Catastrophic-floor predicate summary

```text
CFP   | Result    | Driver / detail
------+-----------+----------------------------------------------------------------
CFP-1 | OK        | train-best 149 trades; 0/32 variants below 30
CFP-2 | TRIGGER   | BTC OOS HIGH train-best mean_R = -0.3633 <= 0
CFP-3 | TRIGGER   | profit_factor = 0.4413 < 0.50; max_dd_R = 54.55 > 10R
CFP-4 | OK        | M3 BTC FAIL AND M4 ETH FAIL; no rescue scenario
CFP-5 | OK        | train HIGH already negative; OOS-only failure absent
CFP-6 | TRIGGER   | DSR = -20.8173 <= 0
                  | (PBO all below 0.50: 0.375 / 0.219 / 0.094)
CFP-7 | OK        | max-month 2025-06 11 trades = 7.4% (well below 50%)
CFP-8 | OK        | worst sensitivity degrade 0.155R (axis N_comp=6); below 0.20R
CFP-9 | OK        | transition_rate 3.33; 149 trades; 100% pass fraction
CFP-10| OK        | optional-ratio-column access count = 0
CFP-11| OK        | no future-bar / partial-bar / signal-without-contraction /
                  | entry-beyond-L_delay / degenerate-double-transition
CFP-12| OK        | all forbidden-input audit counters = 0
```

Binding driver: **CFP-2** (lowest-numbered triggered CFP). CFP-3 and CFP-6 are co-binding independent drivers.

## Commands run

```text
git status                                            (clean except gitignored)
git rev-parse main                                    5105a74a28778b22b30e9dc2b9da788615672eb7
git rev-parse origin/main                             5105a74a28778b22b30e9dc2b9da788615672eb7
git checkout -b phase-4x/c1-backtest-execution        Switched to new branch
.venv/Scripts/python --version                        Python 3.12.4

# Pre-execution quality checks (with new script):
.venv/Scripts/python -m ruff check .                  All checks passed!
.venv/Scripts/python -m pytest -q                     785 passed in 12.58s
.venv/Scripts/python -m mypy                          Success: no issues in 82 source files

# Static forbidden scans (run after script created):
- forbidden imports: 0 occurrences across all 10 forbidden import names
- forbidden data names: occurrences confined to required CFP-12 audit
  field names per Phase 4w spec; runtime access counts all 0

# Phase 4x backtest:
.venv/Scripts/python scripts/phase4x_c1_backtest.py \
  --start 2022-01-01 --end 2026-03-31 \
  --train-start 2022-01-01 --train-end 2023-06-30 \
  --validation-start 2023-07-01 --validation-end 2024-06-30 \
  --oos-start 2024-07-01 --oos-end 2026-03-31 \
  --symbols BTCUSDT ETHUSDT \
  --primary-symbol BTCUSDT --comparison-symbol ETHUSDT \
  --output-dir data/research/phase4x \
  --rng-seed 202604300

# Final quality checks (after script + report committed):
.venv/Scripts/python -m ruff check .                  All checks passed!
.venv/Scripts/python -m pytest -q                     785 passed in 12.95s
.venv/Scripts/python -m mypy                          Success: no issues in 82 source files

git add scripts/phase4x_c1_backtest.py
        docs/00-meta/implementation-reports/2026-04-30_phase-4x_c1-backtest-execution.md
git commit -F .git/PHASE_4X_COMMIT_MSG                Phase 4x memo+code committed (33d34f1)
git push -u origin phase-4x/c1-backtest-execution     Branch pushed; tracking origin
```

## Verification results

```text
ruff check .                : All checks passed!
pytest                      : 785 passed in 12.95s (no regressions)
mypy strict                 : Success: no issues in 82 source files

Phase 4x script line count  : ~2300 lines (single new file)
Phase 4x report line count  : ~600 lines (single new file)
Variant grid cardinality    : exactly 32 (verified: build_variants returns 32)
RNG seed                    : 202604300 (pinned)
CSCV combinations           : C(16, 8) = 12 870 (computed exactly)
Bootstrap iterations        : 10 000 (M1 and M2.a)
Total simulations           : 768 (32 variants × 2 symbols × 3 cost cells × 4 populations)

No source code modified.
No tests modified.
No existing scripts modified.
No data acquired or modified.
No manifests modified.
No v003 created.
```

## Commit

```text
Phase 4x memo+code commit:
  SHA: 33d34f1
  Title: phase-4x: C1 backtest execution (Verdict C HARD REJECT)
  Files: scripts/phase4x_c1_backtest.py (new; ~2300 lines)
         docs/00-meta/implementation-reports/2026-04-30_phase-4x_c1-backtest-execution.md (new)

Phase 4x closeout commit:
  SHA: <recorded after this file is committed>
```

## Final git status

```text
On branch phase-4x/c1-backtest-execution
Untracked files (gitignored transients only):
  .claude/scheduled_tasks.lock
  data/research/
nothing added to commit but untracked files present
```

## Final git log --oneline -5

Recorded after the closeout commit and push.

## Final rev-parse

```text
HEAD                                  <recorded after closeout commit>
origin/phase-4x/c1-backtest-execution <recorded after closeout push>
main                                  5105a74a28778b22b30e9dc2b9da788615672eb7 (unchanged)
origin/main                           5105a74a28778b22b30e9dc2b9da788615672eb7 (unchanged)
```

## Branch / main status

- Phase 4x branch: `phase-4x/c1-backtest-execution` (created from main; pushed to origin).
- main / origin/main: `5105a74a28778b22b30e9dc2b9da788615672eb7` (unchanged; Phase 4x has not been merged).
- No merge to main is performed by Phase 4x (per authorization brief).

## Forbidden-work confirmation

Phase 4x did NOT do any of the following:

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
                              (this phase; new; docs-and-code; not merged)
C1                          : pre-research only;
                              hypothesis-spec defined in Phase 4u;
                              strategy-spec defined in Phase 4v;
                              backtest-plan methodology defined in Phase 4w;
                              backtest executed in Phase 4x;
                              terminally HARD REJECTED;
                              not implemented; not validated; not live-ready;
                              not a rescue of R3 / R2 / F1 / D1-A / V2 / G1
Recommended state           : remain paused;
                              post-C1 consolidation memo (analogous to
                              Phase 4s post-G1) conditional secondary
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

The next step is operator-driven: the operator decides whether to remain paused or authorize Phase 4y (Post-C1 Strategy Research Consolidation Memo, docs-only). Until then, the project remains at the post-Phase-4x C1 HARD REJECT boundary on the Phase 4x branch (not merged to main).

---

**Phase 4x is docs-and-code in standalone-script mode. No source code, tests, existing scripts, data, manifests, or successor phases were created or modified. main remains unchanged at 5105a74. Final Verdict: C — C1 framework HARD REJECT (CFP-2 binding; CFP-3 / CFP-6 co-binding; terminal for C1 first-spec). Recommended state: remain paused; post-C1 consolidation memo conditional secondary. No next phase authorized.**
