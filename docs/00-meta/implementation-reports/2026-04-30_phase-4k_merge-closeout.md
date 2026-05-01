# Phase 4k Merge Closeout

## Summary

Phase 4k has been merged into `main` via a `--no-ff` merge commit at
SHA `95fd3edaa69369af496800c157e298afa508803e` and pushed to
`origin/main`. The Phase 4k V2 Backtest-Plan Memo and its closeout
artefact are now part of the project record.

Phase 4k authored a complete, predeclared V2 backtest methodology
under the Phase 4j §11 metrics OI-subset partial-eligibility binding
rule, the Phase 4g locked V2 strategy spec, the Phase 4i acquired
data inputs, and the Phase 4h timestamp / no-lookahead discipline.
The methodology binds any future Phase 4l V2 Backtest Execution phase
exactly: dataset inputs (4 research-eligible kline datasets +
Phase 4i metrics OI-subset under per-bar exclusion + v002 funding),
11 active V2 features per Phase 4g §28 (8 entry + 3 exit / regime),
the Phase 4j §11 per-bar exclusion algorithm restated verbatim,
categorical optional-ratio-column non-access enforcement, the
signal-generation truth table per Phase 4g §13, the entry execution
model (MARKET-at-next-30m-open), the exit model (initial structural
stop + 0.10 × ATR(20) buffer; fixed-R take-profit `N_R ∈ {2.0, 2.5}`;
unconditional time-stop `T_stop ∈ {12, 16}` 30m bars), the cost
cells (LOW = 1 bp, MEDIUM = 4 bps, HIGH = 8 bps per side preserved
verbatim per §11.6), the position-sizing constraints (0.25% risk;
2× leverage cap; one position; BTCUSDT primary; ETHUSDT comparison
only), the threshold-grid handling policy (Phase 4g §29 fixed at
512 variants; Phase 4k recommends Option B — full PBO / deflated
Sharpe / CSCV with 512 variants reported and no further reduction),
the chronological train / validation / OOS holdout split with exact
UTC date boundaries (train 2022-01-01..2023-06-30; validation
2023-07-01..2024-06-30; OOS holdout 2024-07-01..2026-03-31), the
BTCUSDT-primary / ETHUSDT-comparison protocol (ETH cannot rescue BTC
failure), the M1 / M2 / M3 mechanism-check implementation per Phase
4g §30, the §11.6 HIGH cost-sensitivity gate preserved verbatim,
12 catastrophic-floor predicates (CFP-1..CFP-12), the Verdict A / B /
C / D classification taxonomy, 22 required reporting tables, 10
required plot artefacts, 16 stop conditions, and the reproducibility
requirements.

Phase 4k recommendation: Phase 4l (V2 Backtest Execution,
docs-and-code) primary; remain paused conditional secondary. **Phase
4l is NOT authorized by this merge.**

**Phase 4k was docs-only.** **No data acquired. No data modified.
No manifests modified. No source code modified. No tests modified.
No scripts modified. No backtests run. No V2 backtest code written.
No V2 implementation. No retained verdict revised. No project lock,
threshold, parameter, or governance rule changed.**

V2 remains **pre-research only**: not implemented; not backtested;
not validated; not live-ready; **not a rescue** of R3 / R2 / F1 /
D1-A.

Whole-repo quality gates remain clean (verified during Phase 4k):
`ruff check .` passed; `pytest` 785 passed in 12.48s; `mypy --strict`
0 issues across 82 source files.

R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 /
F1 / D1-A retained research evidence only; R2 FAILED — §11.6
cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS /
FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3
project-level locks; mark-price stops; v002 verdict provenance;
Phase 3q mark-price 5m manifests `research_eligible: false`; Phase
3r §8 mark-price gap governance; Phase 3v §8 stop-trigger-domain
governance; Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
governance; Phase 4a public API and runtime behavior; Phase 4e
reconciliation-model design memo; Phase 4f V2 hypothesis
predeclaration; Phase 4g V2 strategy spec; Phase 4h V2
data-requirements / feasibility memo; Phase 4i V2 acquisition +
integrity report (partial-pass); Phase 4i metrics manifests
`research_eligible: false`; Phase 4j §11 metrics OI-subset
partial-eligibility rule — all preserved verbatim.

Phase 4 canonical remains unauthorized. Phase 4l / any successor
phase remains unauthorized. Paper/shadow, live-readiness, deployment,
production keys, authenticated APIs, private endpoints, user stream,
WebSocket, MCP, Graphify, `.mcp.json`, credentials, and exchange-write
all remain unauthorized.

Recommended state remains paused. No next phase authorized.

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4k_v2-backtest-plan-memo.md   (new; introduced by Phase 4k branch)
docs/00-meta/implementation-reports/2026-04-30_phase-4k_closeout.md                (new; introduced by Phase 4k branch)
docs/00-meta/implementation-reports/2026-04-30_phase-4k_merge-closeout.md          (new; this file; introduced by housekeeping commit)
docs/00-meta/current-project-state.md                                              (modified; narrow Phase 4k sync; introduced by housekeeping commit)
```

No other files modified by Phase 4k or this merge / housekeeping.
No source code, tests, scripts, data, manifests, strategy docs,
runtime docs, or governance docs touched.

## Phase 4k commits included

```text
Phase 4k memo commit:        c26eb27bda53262cb92742295488b5e23137e5bc
Phase 4k closeout commit:    352a9fbfdded244fa281f43e5afa9356364fa9fe
```

Both commits are now in `main`'s history via the merge.

## Merge commit

```text
Merge commit:                95fd3edaa69369af496800c157e298afa508803e
Merge title:                 Merge Phase 4k (V2 backtest-plan memo, docs-only) into main
Merge type:                  --no-ff merge of phase-4k/v2-backtest-plan-memo into main
Branch merged from:          phase-4k/v2-backtest-plan-memo
Branch merged into:          main
```

## Housekeeping commit

To be appended after the housekeeping commit lands.

## Final git status

To be appended after the housekeeping commit and push.

## Final git log --oneline -8

To be appended after the housekeeping commit and push.

## Final rev-parse

To be appended after the housekeeping commit and push.

## main == origin/main confirmation

To be appended after the housekeeping commit and push.

## Backtest-plan conclusion

- **Phase 4k was docs-only.** No source code, tests, scripts, data,
  manifests, or strategy docs were modified.
- **Phase 4k predeclares a complete V2 backtest methodology.** The
  methodology covers dataset inputs, feature implementation,
  per-bar exclusion algorithm, optional-ratio-column prohibition,
  signal generation, entry / exit model, cost / slippage cells,
  position sizing, threshold-grid handling, chronological
  train / validation / OOS holdout split, cross-symbol protocol,
  M1 / M2 / M3 mechanism-check implementation, catastrophic-floor
  predicates, Verdict A / B / C / D taxonomy, required reporting
  tables, required plots, stop conditions, and reproducibility
  requirements.
- **Phase 4k does not authorize Phase 4l.** Phase 4l authorization
  is a separate operator decision.
- **Phase 4k does not run a V2 backtest.** No backtest code was
  written or executed.
- **Phase 4k does not implement V2.** No `prometheus.strategy.*`
  modification.
- **Phase 4k does not modify data or manifests.** All Phase 4i
  manifests preserved verbatim. No v002 / v001-of-5m manifest
  modification. No data acquisition.
- **V2 remains not implemented, not backtested, not validated, not
  live-ready, and not a rescue** of R3 / R2 / F1 / D1-A.

## Dataset inputs

The Phase 4k methodology binds the future Phase 4l execution to use
exactly the following datasets (per Phase 4k memo §"Dataset inputs"):

### Four research-eligible Phase 4i kline datasets

- `binance_usdm_btcusdt_30m__v001` (74 448 bars; full coverage
  2022-01-01..2026-03-31; manifest `research_eligible: true`).
- `binance_usdm_ethusdt_30m__v001` (74 448 bars; manifest
  `research_eligible: true`).
- `binance_usdm_btcusdt_4h__v001` (9 306 bars; manifest
  `research_eligible: true`).
- `binance_usdm_ethusdt_4h__v001` (9 306 bars; manifest
  `research_eligible: true`).

### Two globally non-research-eligible Phase 4i metrics datasets

- `binance_usdm_btcusdt_metrics__v001` (manifest globally
  `research_eligible: false`).
- `binance_usdm_ethusdt_metrics__v001` (manifest globally
  `research_eligible: false`).

### Metrics use limited to the OI subset under Phase 4j §11

The future V2 backtest may consume only the OI subset
(`create_time`, `symbol`, `sum_open_interest`,
`sum_open_interest_value`) of the metrics datasets, under the
Phase 4j §11 binding per-bar exclusion test. The metrics manifests
remain globally `research_eligible: false`. Phase 4k does NOT
amend Phase 4j §11.

### Funding manifests reused

- `binance_usdm_btcusdt_funding__v002` (existing v002; reused).
- `binance_usdm_ethusdt_funding__v002` (existing v002; reused).

### Datasets NOT used by the V2 first backtest

- **Mark-price 30m / 4h klines:** DEFERRED per Phase 4h §20.
- **`aggTrades`:** DEFERRED per Phase 4h §7.E.
- **Optional metrics ratio columns:** categorically forbidden by
  Phase 4j §11.3 / §14.
- **Spot data, cross-venue data:** forbidden by §1.7.3.
- **Authenticated REST / private endpoints / user stream / WebSocket /
  listenKey lifecycle:** forbidden by safety rules.

## Feature plan

Per Phase 4g §28 + Phase 4k methodology:

### 8 active entry features

1. **HTF trend bias state** (4h EMA(20)/EMA(50) discrete comparison).
2. **Donchian breakout state** (30m, N1 ∈ {20, 40} per Phase 4g §29
   axis 1).
3. **Donchian width percentile** (compression precondition; P_w max
   ∈ {25, 35} per axis 2).
4. **Range-expansion ratio** (≥ 1.0 fixed).
5. **Relative volume + volume z-score** (V_rel_min ∈ {1.5, 2.0} per
   axis 3; V_z_min ∈ {0.5, 1.0} per axis 4).
6. **Volume percentile by UTC hour** (≥ 50; 24 hour buckets;
   60-day trailing).
7. **Taker buy/sell imbalance** (kline `taker_buy_volume`; T_imb_min
   ∈ {0.55, 0.60} per axis 5; **NO metrics ratio column read**).
8. **OI delta direction + funding-rate percentile band** (Phase 4j
   §17 OI-delta rule; OI_dir ∈ {`aligned`, `non_negative`} per axis
   6; funding band ∈ {[20, 80], [30, 70]} per axis 7).

### 3 active exit / regime features

1. **Time-since-entry counter** (drives unconditional time-stop;
   T_stop ∈ {12, 16} per axis 9).
2. **ATR percentile regime** (recorded only; not acted on as exit).
3. **HTF bias state continuity** (recorded only; not acted on as
   exit).

## Metrics OI exclusion plan

Per Phase 4k methodology §"Metrics OI per-bar exclusion implementation
plan", binding from this merge forward:

- **Phase 4j §11 is binding.** Phase 4k does NOT amend Phase 4j §11.
- **Each 30m signal bar requires six aligned 5m metrics records** at
  offsets 0, 5, 10, 15, 20, 25 minutes from the bar's `open_time`.
- **All six records must have non-NaN OI fields**
  (`sum_open_interest` AND `sum_open_interest_value`).
- **Bars failing the rule are excluded from candidate setup
  generation** entirely (the bar produces zero V2 candidate setups,
  regardless of other features' values).
- **Exclusion logged with reason `metrics_oi_missing_or_invalid`**
  (or `metrics_oi_prev_window_missing` sub-classification).
- **Optional ratio columns are categorically forbidden** for V2's
  first backtest (Phase 4j §11.3 / §14). Static-analysis and runtime
  introspection MUST verify zero access.
- **Main-cell versus exclude-entire-affected-days sensitivity is
  required.** The future V2 backtest report MUST include both cells.
- **No forward-fill, interpolation, imputation, synthetic data, or
  silent omission** is allowed at any point in the V2 feature
  pipeline.

## Validation plan

Per Phase 4k methodology §"Train / validation / holdout windows":

- **Train window:** 2022-01-01 00:00:00 UTC through 2023-06-30
  23:30:00 UTC (~18 months).
- **Validation window:** 2023-07-01 00:00:00 UTC through 2024-06-30
  23:30:00 UTC (~12 months).
- **OOS holdout window:** 2024-07-01 00:00:00 UTC through 2026-03-31
  23:30:00 UTC (~21 months — primary V2 evidence cell).
- **BTCUSDT primary.**
- **ETHUSDT comparison only.** ETH cannot rescue BTC failure. No
  cross-symbol optimization.
- **512-variant grid** (Phase 4g §29 fixed; Phase 4k recommends
  Option B).
- **PBO / deflated Sharpe / CSCV reporting required** per Bailey /
  Borwein / López de Prado / Zhu (2014). CSCV S = 16
  chronologically-respecting sub-samples (12 870 combinations).
  Bootstrap-by-trade B = 10 000.
- **M1 / M2 / M3 mechanism checks required** per Phase 4g §30.
- **§11.6 HIGH (8 bps per side) cost survival required** on BTCUSDT.

## Reporting requirements

Per Phase 4k methodology §"Required reporting tables" and §"Required
plots or diagnostics":

- **22 required tables** (run metadata; dataset manifest references
  with SHA256 pinning; parameter grid; train / validation / OOS split;
  per-variant trade summaries BTC + ETH × 3 windows × MEDIUM-slip;
  BTC-train-best variant identification + cost-cell sensitivity;
  M1 / M2 / M3 mechanism-check tables; cost-sensitivity comparison;
  PBO computation; deflated-Sharpe summary; CSCV S = 16 sub-sample
  rankings; metrics-OI exclusion table; main-cell vs.
  exclude-entire-affected-days sensitivity; trade distribution by
  year / month / regime; verdict declaration; forbidden-work
  confirmation).
- **10 required plot artefacts** (cumulative-R curves BTC + ETH per
  window; variant-by-window Sharpe heatmap; DSR distribution
  histograms; PBO sub-sample rank distribution; drawdown curve;
  trade-distribution histogram; monthly-bucketed cumulative-R;
  excluded-bar count timeseries; sensitivity-cell vs. main-cell
  mean_R).

## Stop conditions

Per Phase 4k methodology §"Stop conditions":

- 16 binding stop conditions (manifest missing / SHA mismatch; data
  file not found / corrupted; CFP-10 optional-ratio-column access;
  CFP-11 per-bar exclusion deviation; CFP-12 forbidden data access;
  lookahead detected; timestamp misalignment; trades on excluded
  bars; trade-count-insufficient on > 50% variants; validation
  report incomplete; authentication-API / private-endpoint / live-API
  access attempt; credential read / store attempt; network I/O
  outside `data.binance.vision` public bulk; write attempt to
  `data/raw/` / `data/normalized/` / `data/manifests/`; pytest test
  count regression; ruff / mypy violation).
- Each is a fail-closed boundary; the future Phase 4l execution MUST
  stop and produce a failure report on any trigger.

## Candidate next-slice decision

Per Phase 4k methodology §"Operator decision menu":

- **Phase 4l V2 Backtest Execution (docs-and-code) — PRIMARY
  RECOMMENDATION.** Phase 4l would implement
  `scripts/phase4l_v2_backtest.py` standalone, run the 512-variant
  V2 backtest under the Phase 4k methodology, and produce the V2
  backtest report.
- **Remain paused — CONDITIONAL SECONDARY.** Procedurally
  acceptable; preserves predeclaration purity without committing
  to V2 backtest execution.
- **Phase 4l is NOT started by this merge.** Authorization for
  Phase 4l requires a separate operator decision.
- **Immediate V2 implementation REJECTED.** V2 implementation
  requires successful backtest evidence (which does not exist).
- **Paper / shadow / live-readiness / exchange-write FORBIDDEN.**
  Per `docs/12-roadmap/phase-gates.md`, none of these gates is met.

## Verification evidence

Verification commands run during Phase 4k startup (on the
post-Phase-4j-merge tree):

| Check | Result |
|---|---|
| `.venv/Scripts/python --version` | `Python 3.12.4` |
| `.venv/Scripts/python -m ruff check .` | `All checks passed!` |
| `.venv/Scripts/python -m pytest` | `785 passed in 12.48s` |
| `.venv/Scripts/python -m mypy` | `Success: no issues found in 82 source files` |

Whole-repo quality gates remain **fully clean**: zero ruff errors;
785 / 785 tests passing; zero mypy strict issues across 82 source
files. No regressions relative to the post-Phase-4j-merge baseline.

## Forbidden-work confirmation

- **No Phase 4l / successor phase started.** Phase 4l authorization
  is a separate operator decision after this merge.
- **No V2 implementation.**
- **No V2 backtest run.**
- **No V2 backtest code written.**
- **No data acquired.**
- **No data modified.**
- **No manifests modified.**
- **No source code modified.**
- **No tests modified.**
- **No scripts modified.**
- **No diagnostics run.**
- **No Q1–Q7 rerun.**
- **No `scripts/phase3q_5m_acquisition.py` execution.**
- **No `scripts/phase3s_5m_diagnostics.py` execution.**
- **No `scripts/phase4i_v2_acquisition.py` execution.**
- **No mark-price 30m / 4h acquisition.**
- **No `aggTrades` acquisition.**
- **No spot data acquisition.**
- **No cross-venue data acquisition.**
- **No funding-rate re-acquisition.**
- **No v002 / v001-of-5m / Phase 4i manifest modification.**
- **No v003 created.**
- **No `prometheus.research.data.*` extension.**
- **No `Interval` enum extension.**
- **No `pyproject.toml` modification.**
- **No `.gitignore` modification.**
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No `.env` file creation.**
- **No credential storage / request / use.**
- **No authenticated REST / private endpoint / public endpoint /
  user-stream / WebSocket calls.**
- **No production alerting / Telegram / n8n production routes.**
- **No MCP enabling / Graphify enabling.**
- **No deployment artefact created.**
- **No paper / shadow runtime created.**
- **No live-readiness implication.**
- **No order placement / cancellation.**
- **No real exchange adapter implementation.**
- **No exchange-write capability.**
- **No reconciliation implementation.**
- **No V1 / R3 / R2 / F1 / D1-A / other strategy implementation.**
- **No strategy rescue proposal.**
- **No 5m strategy / hybrid / retained-evidence successor / new
  variant created.**
- **No retained-evidence verdict revision.**
- **No project-lock revision.**
- **No threshold / parameter modification.**
- **No §11.6 / §1.7.3 / Phase 3r §8 / Phase 3v §8 / Phase 3w §6 /
  §7 / §8 / Phase 4j §11 governance modification.**
- **No Phase 4f / 4g / 4h / 4i / 4j text modification.**
- **No Phase 4g V2 strategy-spec modification.**
- **No optional ratio-column activation.**
- **No OI feature removal.**
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
- **No `docs/12-roadmap/technical-debt-register.md` substantive
  change.**
- **No `docs/00-meta/ai-coding-handoff.md` substantive change.**
- **No `docs/09-operations/first-run-setup-checklist.md` substantive
  change.**
- **No `docs/00-meta/implementation-ambiguity-log.md` modification.**
- **No `.claude/rules/**` modification.**

## Remaining boundary

- **Recommended state:** **paused** for any successor phase. Phase 4k
  is now part of `main`. No successor phase has been authorized.
- **Phase 4k output:** docs-only V2 backtest-plan memo + closeout
  artefact + this merge-closeout artefact + narrow Phase 4k sync of
  `docs/00-meta/current-project-state.md`.
- **Repository quality gate state:** **fully clean.** Whole-repo
  `ruff check .` passes; pytest 785 passed; mypy strict 0 issues
  across 82 source files (verified during Phase 4k).
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4
  (canonical) remains not authorized. Phase 4a through Phase 4k all
  merged.
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
  (preserved verbatim).
- **V2 backtest methodology governance:** Phase 4k §"Backtest purpose"
  through §"Reproducibility requirements" (binding from this merge
  forward; immutable absent a separately authorized governance
  amendment).
- **Reconciliation governance:** Defined by Phase 4e but NOT yet
  enforced in code; awaits separately authorized future implementation
  phase.
- **V2 strategy-research direction:** Predeclared (Phase 4f) +
  operationalized (Phase 4g) + data-requirements (Phase 4h) + data
  acquired (Phase 4i, partial-pass) + governance binding (Phase 4j) +
  backtest-plan binding (Phase 4k). **NOT implemented; NOT
  backtested; NOT validated.**
- **OPEN ambiguity-log items after Phase 4k:** zero relevant to
  runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0
  framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained
  research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other;
  §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price
  stops; v002 verdict provenance; Phase 3q mark-price 5m manifests
  `research_eligible: false`. All preserved.
- **Branch state:** `phase-4k/v2-backtest-plan-memo` exists locally
  and on `origin/phase-4k/v2-backtest-plan-memo`. The branch is now
  merged into `main`.

## Operator decision menu

The next operator decision is operator-driven only.

### Option A — Remain paused (PROCEDURALLY ACCEPTABLE)

Take no further action. Phase 4k methodology is recorded in `main`;
Phase 4l execution is not authorized.

### Option B — Phase 4l: V2 Backtest Execution (docs-and-code) (PRIMARY RECOMMENDATION per Phase 4k §"Operator decision menu")

Authorize a separate Phase 4l execution phase that implements the
Phase 4k methodology exactly. Phase 4l would:

1. Implement `scripts/phase4l_v2_backtest.py` standalone (no
   `prometheus.runtime.*` / `prometheus.execution.*` /
   `prometheus.persistence.*` / network-I/O imports).
2. Run the 512-variant V2 backtest on the predeclared train /
   validation / OOS holdout windows.
3. Apply Phase 4j §11 per-bar exclusion exactly.
4. Compute M1 / M2 / M3 + DSR + PBO + CSCV + cost-cell sensitivity.
5. Produce the V2 backtest report with all required tables and
   plots.
6. Stop. Phase 4l does NOT recommend any successor phase by design.

### Option C / D / E / F / G — methodology refinement / Phase 4j §11 amendment / V2 spec amendment / mark-price 30m+4h acquisition / aggTrades acquisition (NOT RECOMMENDED)

Per Phase 4k §"Operator decision menu" Options C / D / E / F / G,
none of these are recommended at this boundary.

### Option H — Skip Phase 4l and implement V2 directly (REJECTED)

V2 implementation requires successful backtest evidence (which does
not exist).

### Option I — Paper / shadow / live-readiness / exchange-write (FORBIDDEN)

Per `docs/12-roadmap/phase-gates.md`, none of these gates is met.

## Next authorization status

**No next phase has been authorized.** Phase 4k's recommendation is
**Option B (Phase 4l V2 Backtest Execution, docs-and-code) as
primary**, with **Option A (remain paused) as conditional secondary**.

Selection of any subsequent phase requires explicit operator
authorization for that specific phase. No such authorization has
been issued.
