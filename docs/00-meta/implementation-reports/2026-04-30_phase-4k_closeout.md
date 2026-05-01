# Phase 4k Closeout

## Summary

Phase 4k authored the V2 Backtest-Plan Memo (docs-only) at
`docs/00-meta/implementation-reports/2026-04-30_phase-4k_v2-backtest-plan-memo.md`
(commit `c26eb27bda53262cb92742295488b5e23137e5bc` on branch
`phase-4k/v2-backtest-plan-memo`).

The memo predeclares — *before* any V2 backtest is run, any V2
backtest code is written, or any V2 strategy is implemented — every
methodological choice that a future Phase 4l V2 Backtest Execution
phase would be required to honor. It commits the dataset-input set
(4 research-eligible kline datasets + Phase 4i metrics OI-subset
under Phase 4j §11 + v002 funding manifests), the implementation
plan for each of the 11 active V2 features (8 entry + 3 exit /
regime per Phase 4g §28), the per-bar Phase 4j §11 OI-feature-eligibility
test algorithm, the categorical optional-ratio-column prohibition,
the signal-generation truth table, the entry execution model
(MARKET-at-next-30m-open per Phase 4g §13), the exit model (initial
structural stop + ATR buffer; fixed-R take-profit per Phase 4g §29
axis 8; unconditional time-stop per Phase 4g §29 axis 9), the cost
cells (LOW / MEDIUM / HIGH = §11.6 = 8 bps per side preserved
verbatim), the position-sizing constraints (0.25% risk; 2× leverage
cap; one position; BTCUSDT primary; ETHUSDT comparison only), the
threshold-grid handling policy (Phase 4g §29 fixed at 512 variants;
Phase 4k recommends Option B — full PBO / deflated Sharpe / CSCV
with 512-variant reporting and no further reduction), the
chronological train / validation / OOS holdout split with exact UTC
date boundaries (train 2022-01-01..2023-06-30; validation
2023-07-01..2024-06-30; OOS holdout 2024-07-01..2026-03-31), the
BTCUSDT-primary / ETHUSDT-comparison protocol (ETH cannot rescue
BTC failure; no cross-symbol optimization), the M1 / M2 / M3
mechanism-check implementation per Phase 4g §30, 12 catastrophic-floor
predicates (CFP-1..CFP-12 covering insufficient trade count, negative
OOS expectancy under HIGH cost, catastrophic drawdown, BTC-fails-with-ETH-passes,
train-only with OOS-failure, excessive PBO, regime / month
overconcentration, sensitivity-cell failure, excluded-bar-fraction
anomaly, optional-ratio-column access, per-bar-exclusion deviation,
and forbidden data access), the Verdict A / B / C / D classification
taxonomy, 22 required reporting tables, 10 required plot artefacts,
16 stop conditions, the reproducibility requirements (manifest SHA
pinning; pinned RNG seeds; deterministic variant ordering; idempotent
rerun), the standalone-script pattern (`scripts/phase4l_v2_backtest.py`
with no `prometheus.runtime.*` / `prometheus.execution.*` /
network-I/O imports), and the preserved-whole-repo-quality-gate
requirement.

Phase 4k recommends Phase 4l (V2 Backtest Execution, docs-and-code)
as primary; remain paused as conditional secondary. **Phase 4l is
NOT authorized by Phase 4k.** Phase 4l authorization is a separate
operator decision after the Phase 4k merge and review.

**Phase 4k was docs-only.** No source code, tests, scripts, data,
manifests, or strategy docs were modified. No V2 backtest run. No V2
data acquisition. No V2 implementation. No Phase 4g V2 strategy-spec
selection changed. No Phase 4j §11 governance amendment. No prior
verdict revised. No project lock, threshold, parameter, or
governance rule changed.

Whole-repo quality gates remain clean: `ruff check .` passed; `pytest`
785 passed in 12.48s; `mypy --strict` 0 issues across 82 source files.

R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 /
F1 / D1-A retained research evidence only; R2 FAILED — §11.6
cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS /
FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3
project-level locks; mark-price stops; v002 verdict provenance; Phase
3q mark-price 5m manifests `research_eligible: false`; Phase 3r §8
mark-price gap governance; Phase 3v §8 stop-trigger-domain
governance; Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
governance; Phase 4a public API and runtime behavior; Phase 4e
reconciliation-model design memo; Phase 4f V2 hypothesis predeclaration;
Phase 4g V2 strategy spec; Phase 4h V2 data-requirements / feasibility
memo; Phase 4i V2 acquisition + integrity report (partial-pass); Phase
4i metrics manifests `research_eligible: false`; Phase 4j §11 metrics
OI-subset partial-eligibility rule — all preserved verbatim.

V2 remains pre-research only: not implemented; not backtested; not
validated; not live-ready; **not a rescue** of R3 / R2 / F1 / D1-A.

**Phase 4 canonical remains unauthorized.** **Phase 4l / any
successor phase remains unauthorized.** **Paper / shadow,
live-readiness, deployment, production keys, authenticated APIs,
private endpoints, user stream, WebSocket, MCP, Graphify, `.mcp.json`,
credentials, and exchange-write all remain unauthorized.**

**Recommended state remains paused. No next phase authorized.**

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4k_v2-backtest-plan-memo.md  (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4k_closeout.md               (new — this file)
```

No other files modified. No source code, tests, scripts, data,
manifests, strategy docs, runtime docs, or governance docs touched.

## Backtest-plan conclusion

Phase 4k delivers a complete, predeclared, immutable backtest-plan
methodology that:

- honors Phase 4g V2 strategy spec verbatim (signal 30m / bias 4h /
  session 1h; 8 + 3 features; 512-variant grid; M1 / M2 / M3
  decomposition; four governance labels);
- honors Phase 4j §11 metrics OI-subset partial-eligibility rule
  verbatim and incorporates it as a binding execution constraint;
- honors all Phase 3v / 3w / 3r governance schemes verbatim;
- preserves §11.6 = 8 bps HIGH per side as a non-negotiable promotion
  gate;
- predeclares train / validation / holdout windows BEFORE any
  backtest, eliminating post-hoc window-tuning risk;
- predeclares 12 catastrophic-floor predicates BEFORE any backtest,
  eliminating post-hoc predicate-tuning risk;
- predeclares 22 required reporting tables and 10 required plots
  BEFORE any backtest, eliminating post-hoc reporting-selection risk;
- predeclares 16 stop conditions BEFORE any backtest, ensuring
  fail-closed methodology;
- predeclares the per-bar exclusion algorithm exactly (matching Phase
  4j §16 pseudocode verbatim);
- specifies a single-grid commitment with deterministic variant
  ordering for reproducibility;
- requires deflated-Sharpe / PBO / CSCV correction with 512 variants;
- requires bootstrap-by-trade stat-significance for M2 / M3
  mechanism-check differential calculations;
- requires manifest SHA256 pinning at run-time;
- forbids any code path that imports from `prometheus.runtime.*`,
  `prometheus.execution.*`, `prometheus.persistence.*`, or any
  network-I/O module;
- forbids any access to authenticated APIs, private endpoints, user
  stream, WebSocket, listenKey lifecycle, credentials, `.env`, MCP,
  Graphify, `.mcp.json`, paper / shadow / live;
- forbids any modification of v002 / v001-of-5m / Phase 4i manifests;
- forbids any post-hoc V2 spec amendment, Phase 4j §11 amendment,
  optional-ratio activation, OI-feature removal, mark-price 30m / 4h
  acquisition, aggTrades acquisition, v003 creation, or any
  retained-evidence rescue.

Phase 4k explicitly does NOT authorize V2 backtest execution. It
provides the methodology-discipline contract a future Phase 4l
execution would be required to honor. Whether and when Phase 4l is
authorized is an operator decision after Phase 4k merge and review.

## Data inputs

Per the Phase 4k memo §"Dataset inputs":

- `binance_usdm_btcusdt_30m__v001` (research_eligible: true; 74 448
  bars; 0 gaps; full coverage 2022-01-01..2026-03-31).
- `binance_usdm_ethusdt_30m__v001` (research_eligible: true; 74 448
  bars).
- `binance_usdm_btcusdt_4h__v001` (research_eligible: true; 9 306
  bars).
- `binance_usdm_ethusdt_4h__v001` (research_eligible: true; 9 306
  bars).
- `binance_usdm_btcusdt_metrics__v001` (research_eligible: false
  globally; OI-subset feature-eligible per Phase 4j §11 under per-bar
  exclusion).
- `binance_usdm_ethusdt_metrics__v001` (research_eligible: false
  globally; OI-subset feature-eligible per Phase 4j §11 under per-bar
  exclusion).
- `binance_usdm_btcusdt_funding__v002` (existing v002; reused).
- `binance_usdm_ethusdt_funding__v002` (existing v002; reused).

**Forbidden inputs** (per Phase 4k memo §"Dataset inputs / Forbidden
inputs"): mark-price 30m / 4h klines (DEFERRED); v002 mark-price 15m
(reserved for future `mark_price_backtest_candidate` per Phase 3v
§8.5); v001-of-5m mark-price (`research_eligible: false`); aggTrades
(DEFERRED); spot data (forbidden); cross-venue data (forbidden);
optional metrics ratio columns (forbidden by Phase 4j §11.3 / §14);
v003 (does not exist; not authorized); modified Phase 4i manifests
(preserved); authenticated REST / private endpoints / public endpoints
in code / user stream / WebSocket / listenKey lifecycle (forbidden by
safety rules).

## Feature plan

Per the Phase 4k memo §"Feature implementation plan":

**8 active V2 entry features:**

1. HTF trend bias state (4h EMA(20)/(50) discrete comparison; long
   bias / short bias state).
2. Donchian breakout state (30m, N1 ∈ {20, 40} per Phase 4g §29 axis
   1).
3. Donchian width percentile (compression precondition; P_w max ∈
   {25, 35} per axis 2).
4. Range-expansion ratio (≥ 1.0 fixed).
5. Relative volume + volume z-score (V_rel_min ∈ {1.5, 2.0} per axis
   3; V_z_min ∈ {0.5, 1.0} per axis 4; both pass jointly).
6. Volume percentile by UTC hour (≥ 50; 24 hour buckets; 60-day
   trailing).
7. Taker buy/sell imbalance (kline `taker_buy_volume`; T_imb_min ∈
   {0.55, 0.60} per axis 5; **NO metrics ratio column read**).
8. OI delta direction + funding-rate percentile band:
   - OI delta computed via Phase 4j §17 rule (last 5min OI in current
     30m vs. last 5min OI in previous 30m).
   - OI_dir ∈ {`aligned`, `non_negative`} per axis 6.
   - Funding band ∈ {[20, 80], [30, 70]} per axis 7.

**3 active V2 exit / regime features:**

1. Time-since-entry counter (drives unconditional time-stop; T_stop ∈
   {12, 16} per axis 9).
2. ATR percentile regime (recorded only; not acted on as exit).
3. HTF bias state continuity (recorded only; not acted on as exit).

**Optional features** (documented in Phase 4g §28; **NOT activated**
in V2's first backtest): long/short ratio (account / top-trader);
mark-price-vs-trade-price divergence; breakout close location;
higher-high / higher-low structure.

## Metrics OI exclusion plan

Per the Phase 4k memo §"Metrics OI per-bar exclusion implementation
plan", which restates Phase 4j §16 pseudocode verbatim and binds it
on Phase 4l:

- For each 30m signal bar at `bar_open_time_ms`, the future Phase 4l
  execution checks whether all six aligned 5-minute records (offsets
  0, 5, 10, 15, 20, 25 minutes) are present AND each has non-NaN
  `sum_open_interest` AND non-NaN `sum_open_interest_value`.
- Bars failing the test are excluded from V2 candidate setup
  generation entirely, with reason `metrics_oi_missing_or_invalid`.
- Bars where the previous-window OI record (at `bar_open_time_ms - 5
  × 60 × 1000`) is absent or NaN are excluded with reason
  `metrics_oi_prev_window_missing` (a sub-classification).
- **No forward-fill, interpolation, imputation, or silent omission.**
- Exclusion counts MUST be logged per-symbol, per-day, per-bar, and
  cumulatively.
- Sensitivity analysis MUST compare main-cell vs.
  exclude-entire-affected-days cell.
- Exclusion-rate anomaly trigger: empirical exclusion rate ≥ 5% (vs.
  Phase 4j §15 ~1.3% estimate) flags for operator review BEFORE
  results are claimed valid.

## Validation plan

Per the Phase 4k memo §"Chronological validation plan" and §"Train /
validation / holdout windows":

- **Train window:** 2022-01-01 00:00:00 UTC → 2023-06-30 23:30:00
  UTC (~18 months). Used for variant selection, DSR, CSCV.
- **Validation window:** 2023-07-01 00:00:00 UTC → 2024-06-30
  23:30:00 UTC (~12 months). Used for selection-confirmation; not
  variant re-selection.
- **OOS holdout window:** 2024-07-01 00:00:00 UTC → 2026-03-31
  23:30:00 UTC (~21 months). Primary V2 evidence cell.
- **No data shuffle.** **No leakage.** **No window modification
  post-hoc.**
- **Walk-forward extension** (4 rolling 12-month OOS windows over
  2024-07..2026-03) recommended as secondary; if omitted, must be
  justified.
- **Statistical methodology:** deflated Sharpe correction per Bailey
  & López de Prado (2014); CSCV with S = 16 chronologically-respecting
  sub-samples; PBO computed per Bailey / Borwein / López de Prado /
  Zhu (2014); bootstrap-by-trade B = 10 000 for M2 / M3 differential
  CIs.
- **Cost methodology:** §11.6 HIGH = 8 bps per side preserved verbatim;
  V2 candidates failing §11.6 HIGH on either BTCUSDT or ETHUSDT FAIL
  framework promotion.

## Reporting requirements

Per the Phase 4k memo §"Required reporting tables" and §"Required
plots or diagnostics":

- **22 required tables** covering run metadata, dataset manifest
  references, parameter grid, train / validation / OOS split,
  per-variant trade summaries (BTC + ETH × 3 windows × MEDIUM-slip),
  BTCUSDT-train-best variant identification + cost-cell sensitivity,
  M1 / M2 / M3 mechanism-check tables, cost-sensitivity comparison,
  PBO computation, deflated-Sharpe summary, CSCV S = 16 sub-sample
  rankings, metrics-OI exclusion table, main-cell vs.
  exclude-entire-affected-days sensitivity, trade distribution by
  year / month / regime, verdict declaration, forbidden-work
  confirmation.
- **10 required plot artefacts** covering cumulative-R curves
  (BTC + ETH per window), variant-by-window Sharpe heatmap, DSR
  distribution histograms, PBO sub-sample rank distribution, drawdown
  curve, trade-distribution histogram, monthly-bucketed cumulative-R,
  excluded-bar count timeseries, sensitivity-cell vs. main-cell
  comparison.

## Stop conditions

Per the Phase 4k memo §"Stop conditions": 16 stop conditions binding
on the future Phase 4l execution, including: required manifest
missing; manifest SHA256 mismatch; data file not found / corrupted;
optional ratio column accessed (CFP-10); per-bar exclusion algorithm
deviation (CFP-11); lookahead detected; timestamp misalignment;
trades emitted on excluded bars; trade count insufficient on > 50%
variants (CFP-1); validation report incomplete; authentication-API /
private-endpoint / live-API access (CFP-12); credential read / store
attempt; network I/O outside `data.binance.vision` public bulk;
write attempt to `data/raw/` / `data/normalized/` / `data/manifests/`;
test count regression in pytest; ruff / mypy violation. Each is a
fail-closed boundary; the future Phase 4l execution MUST stop and
produce a failure report on any trigger.

## Candidate next-slice decision

Per the Phase 4k memo §"Operator decision menu":

- **Option A — Remain paused** (procedurally acceptable; conditional
  secondary).
- **Option B — Phase 4l V2 Backtest Execution (docs-and-code)**
  (PRIMARY RECOMMENDATION).
- **Options C / D / E / F / G — methodology refinement / Phase 4j
  §11 amendment / V2 spec amendment / mark-price 30m+4h acquisition /
  aggTrades acquisition** (NOT RECOMMENDED).
- **Option H — Skip Phase 4l and implement V2 directly** (REJECTED).
- **Option I — Paper / shadow / live-readiness / exchange-write**
  (FORBIDDEN).

**Recommended next slice: Phase 4l (Option B) primary; remain paused
(Option A) conditional secondary.** Phase 4l is NOT authorized by
Phase 4k; authorization requires explicit operator decision after
the Phase 4k merge.

## Commands run

```text
git status
git rev-parse main
git rev-parse origin/main
git checkout -b phase-4k/v2-backtest-plan-memo
git branch --show-current
.venv/Scripts/python --version
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m pytest -q
.venv/Scripts/python -m mypy
git add docs/00-meta/implementation-reports/2026-04-30_phase-4k_v2-backtest-plan-memo.md
git status
git commit -m "phase-4k: V2 backtest-plan memo (docs-only)"  # (full message in commit object)
git rev-parse HEAD
git push -u origin phase-4k/v2-backtest-plan-memo
```

The following commands were **NOT** run (per Phase 4k brief
prohibitions):

- No `scripts/phase3q_5m_acquisition.py` execution.
- No `scripts/phase3s_5m_diagnostics.py` execution.
- No `scripts/phase4i_v2_acquisition.py` execution.
- No backtest execution.
- No diagnostic / Q1–Q7 question rerun.
- No data acquisition / download / patch / regeneration.
- No mark-price 30m / 4h acquisition.
- No aggTrades acquisition.
- No spot data acquisition.
- No private / authenticated REST or WebSocket request.

## Verification results

| Check | Result |
|---|---|
| `.venv/Scripts/python --version` | `Python 3.12.4` |
| `.venv/Scripts/python -m ruff check .` | `All checks passed!` |
| `.venv/Scripts/python -m pytest` | `785 passed in 12.48s` |
| `.venv/Scripts/python -m mypy` | `Success: no issues found in 82 source files` |

Whole-repo quality gates remain **fully clean**: zero ruff errors;
785 / 785 tests passing; zero mypy strict issues across 82 source
files. No regressions relative to the post-Phase-4j-merge baseline.

## Commit

```text
Phase 4k memo commit:        c26eb27bda53262cb92742295488b5e23137e5bc
```

The closeout commit SHA will be recorded after this file is committed.

## Final git status

To be appended after closeout commit and push.

## Final git log --oneline -5

To be appended after closeout commit and push.

## Final rev-parse

To be appended after closeout commit and push.

## Branch / main status

Phase 4k is on branch `phase-4k/v2-backtest-plan-memo`. The branch is
pushed to `origin/phase-4k/v2-backtest-plan-memo`. **Phase 4k is NOT
merged to main.** main remains at
`afa225ac0486910f9de675844bfe499115e168cd` (post-Phase-4j-merge
housekeeping commit).

Merge to main is not part of Phase 4k. A separate operator decision
("We are closing out Phase 4k by merging it into main") is required
to merge the branch.

## Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4l / successor phase started.** No
  subsequent phase has been authorized, scoped, briefed, branched, or
  commenced.
- **No V2 implementation.**
- **No V2 backtest.**
- **No V2 data acquisition.**
- **No data acquired.** No `data/` artefact modified. No public
  Binance endpoint consulted in code.
- **No implementation code written.** Phase 4k is text-only.
- **No real exchange adapter implemented.**
- **No exchange-write capability.**
- **No order placement / cancellation.**
- **No Binance credentials used.** No request, no storage, no `.env`
  modification.
- **No authenticated REST / private endpoint / public endpoint /
  user-stream / WebSocket calls.** Phase 4k performs no network I/O.
- **No production alerting / Telegram / n8n production routes.**
- **No MCP enabling / Graphify enabling / `.mcp.json` modification.**
- **No `.env` file creation.**
- **No credential handling modification.**
- **No deployment artefact created.**
- **No paper / shadow runtime created.**
- **No live-readiness implication.**
- **No V1 / R3 / R2 / F1 / D1-A / other strategy implementation.**
  Existing `prometheus.strategy` modules untouched.
- **No strategy rescue proposal.** V2 is a new ex-ante hypothesis,
  NOT a re-parameterized successor of any retained-evidence candidate.
- **No 5m strategy / hybrid / retained-evidence successor / new
  variant created.**
- **No diagnostics run.** No Phase 3o / 3p Q1–Q7 question rerun.
- **No backtests run.**
- **No `scripts/phase3q_5m_acquisition.py` execution.**
- **No `scripts/phase3s_5m_diagnostics.py` execution.**
- **No `scripts/phase4i_v2_acquisition.py` execution.**
- **No data acquisition / download / patch / regeneration /
  modification.** No `data/` artefact modified.
- **No data manifest modification.** All `data/manifests/*.manifest.json`
  preserved verbatim.
- **No v002 dataset / manifest modification.**
- **No Phase 3q v001-of-5m manifest modification.**
- **No Phase 4i manifest modification.**
- **No v003 created.**
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A
  all preserved verbatim.
- **No threshold / parameter / project-lock modifications.**
- **No Phase 3v stop-trigger-domain governance modification.**
- **No Phase 3w break-even / EMA slope / stagnation governance
  modification.**
- **No Phase 3r §8 mark-price gap governance modification.**
- **No Phase 4j §11 metrics OI-subset governance modification.**
- **No Phase 4f / 4g / 4h / 4i / 4j text modification.**
- **No Phase 4g V2 strategy-spec modification.**
- **No `docs/03-strategy-research/v1-breakout-strategy-spec.md`
  substantive change.**
- **No `docs/03-strategy-research/v1-breakout-backtest-plan.md`
  substantive change.**
- **No `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`
  substantive change.**
- **No `docs/07-risk/stop-loss-policy.md` substantive change.**
- **No `docs/06-execution-exchange/binance-usdm-order-model.md`
  substantive change.**
- **No `docs/12-roadmap/phase-gates.md` substantive change.**
- **No `docs/12-roadmap/technical-debt-register.md` substantive change.**
- **No `docs/00-meta/ai-coding-handoff.md` substantive change.**
- **No `docs/09-operations/first-run-setup-checklist.md` substantive
  change.**
- **No `docs/00-meta/implementation-ambiguity-log.md` modification.**
- **No `docs/00-meta/current-project-state.md` modification on the
  Phase 4k branch.** Per the Phase 4k brief.
- **No `.claude/rules/**` modification.**
- **No `pyproject.toml` modification.**
- **No `.gitignore` modification.**
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No `src/prometheus/**` modification.**
- **No `tests/**` modification.**
- **No `scripts/**` modification.**
- **No merge to main.**
- **No successor phase started.**

## Remaining boundary

- **Recommended state:** **paused** for any successor phase. Phase 4k
  deliverables exist as branch-only artefacts pending operator review.
- **Phase 4k output:** docs-only V2 backtest-plan memo + closeout
  artefact on the Phase 4k branch.
- **Repository quality gate state:** **fully clean.** Whole-repo
  `ruff check .` passes; pytest 785 passed; mypy strict 0 issues
  across 82 source files (verified during Phase 4k startup).
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4
  (canonical) remains not authorized. Phase 4a–4j all merged. Phase
  4k V2 backtest-plan memo on this branch.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 +
  enforced in code by Phase 4a (preserved).
- **Break-even rule governance:** RESOLVED by Phase 3w §6 + enforced
  in code by Phase 4a (preserved).
- **EMA slope method governance:** RESOLVED by Phase 3w §7 + enforced
  in code by Phase 4a (preserved).
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 +
  enforced in code by Phase 4a (preserved).
- **Mark-price gap governance:** Phase 3r §8 (preserved).
- **Metrics OI-subset partial-eligibility governance:** Phase 4j §11
  (preserved verbatim and incorporated as binding for Phase 4l).
- **V2 backtest methodology:** Phase 4k §"Backtest purpose" through
  §"Reproducibility requirements" (this branch; immutable from
  Phase 4k merge forward absent a separately authorized governance
  amendment).
- **Reconciliation governance:** Defined by Phase 4e but NOT yet
  enforced in code; awaits separately authorized future implementation
  phase.
- **V2 strategy-research direction:** Predeclared (Phase 4f) +
  operationalized (Phase 4g) + data-requirements (Phase 4h) + data
  acquired (Phase 4i, partial-pass) + governance binding (Phase 4j) +
  backtest-plan binding (Phase 4k, this phase). **NOT implemented;
  NOT backtested; NOT validated.**
- **OPEN ambiguity-log items after Phase 4k:** zero relevant to
  runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0
  framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained
  research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other;
  §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price
  stops; v002 verdict provenance; Phase 3q mark-price 5m manifests
  `research_eligible: false`. All preserved.
- **Branch state:**
  `phase-4k/v2-backtest-plan-memo` exists locally and on
  `origin/phase-4k/v2-backtest-plan-memo`. **NOT merged to main.**

## Next authorization status

**No next phase has been authorized.** Phase 4k's recommendation is
**Option B (Phase 4l V2 Backtest Execution, docs-and-code) as
primary**, with **Option A (remain paused) as conditional secondary**.

Selection of any subsequent phase requires explicit operator
authorization for that specific phase. No such authorization has been
issued.
