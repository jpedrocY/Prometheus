# Phase 4ap — V1-Arc Exit-Path Forensic Plan

## 1. Executive Summary

Phase 4ap is a docs-only forensic plan / predeclared methodology phase.
It defines the exact V1-arc-only computation specification any future
exit-path forensic phase must follow before computation. Phase 4ap does
NOT compute MFE / MAE, does NOT compute realized-R distributions, does
NOT perform exit-path forensics, does NOT run any backtest or strategy /
data-acquisition script, does NOT acquire data, does NOT modify data /
manifests / scripts / source / tests / strategy parameters / thresholds /
project locks / retained verdicts / M0 governance, does NOT propose a
new strategy or exit system, does NOT optimize R3 or any other V1-arc
candidate, does NOT create R3-prime / R2-prime / R1a-prime /
R1b-narrow-prime / any successor strategy candidate, and does NOT
authorize any successor phase.

Phase 4ap only answers:

```text
What exact V1-arc populations, artefacts, fields, metrics, outputs,
exclusions, governance boundaries, and stop conditions would a future
computation phase need to follow before any MFE/MAE or exit-path
computation may be safely authorized?
```

The plan is derived from Phase 4an (inventory baseline), Phase 4ao
(methodology / artefact harmonization), Phase 4al (refined no-rescue
rule + data-resolution hierarchy), Phase 4am (backtest-logic audit
findings), and the Phase 4ak twelve-clause M0 mechanism-admissibility
gate + post-null cooldown rule.

Headline plan conclusions, in plain language:

1. **Population scope**: H0 (framework anchor), R3 (baseline-of-record,
   descriptive context only), R1a (retained — non-leading), R1b-narrow
   (retained — non-leading), R2 (FAILED — §11.6 cost-fragility).
2. **Excluded**: F1, D1-A, V2, G1, C1, and the 5m research thread.
3. **Artefact source**: existing local `trade_log_v1` JSON / Parquet
   under `data/derived/backtests/phase-2*` (gitignored locally) plus
   per-cost-cell variants and trade-price stop-domain variants where
   present. No artefact is modified.
4. **Field schema**: 25 required fields drawn directly from the existing
   `trade_log_v1` schema as listed in §11. No new fields.
5. **Metric definitions**: 14 forensic metrics (MFE_R, MAE_R, net_R,
   gross_R, cost-in-R, fee-in-R, slippage-in-R, funding-in-R, +1R/+2R/+3R
   touch flags, MFE capture ratio, giveback-from-MFE, adverse-before-
   favorable flag, favorable-before-stop flag, bar-resolution ambiguity
   flag) referencing Phase 4ao §6 / §8 verbatim.
6. **Timeframe / data-resolution**: 15m bar-extreme only for first-pass.
   5m, 1m, aggTrades, tick, mark-price 30m / 4h all unauthorized by
   Phase 4ap.
7. **Cost / realized-R**: §11.6 LOCK preserved; LOW / MEDIUM / HIGH
   cost-cell comparisons descriptive only; R2 cost-fragility treated as
   retained failed evidence, not rescue.
8. **Stop-trigger-domain**: `trade_price_backtest` only for V1-arc
   first-pass; `mixed_or_unknown` invalid / fail-closed.
9. **Output specification**: 9 planned output artefacts (8 CSVs + 1
   markdown checklist + the future computation report markdown) defined
   here only as planned outputs; not created by Phase 4ap.
10. **Stop conditions**: 11 fail-closed conditions for any future
    computation phase listed in §17.
11. **Forbidden questions**: 10 explicitly forbidden question forms in
    §9 that any future computation phase must reject if asked.

The recommendation (§19) is **remain paused** as primary, with a
conditional secondary that the operator may later authorize a future
V1-arc-only computation phase exactly under this plan, and a conditional
tertiary that the operator may later authorize a narrower docs-only
refinement (e.g., a Phase 4ao-style §14 template re-validation memo,
an OQ-B-resolution memo, or an F1 / D1-A Route B reconstruction
methodology memo) as alternatives. Phase 4ap does NOT authorize any of
these.

## 2. Scope and Explicit Non-Scope

### 2.1 In scope

- Static repository inspection of Phase 4an inventory baseline, Phase
  4ao methodology / artefact harmonization, Phase 4al §9 / §13 / §14,
  Phase 4am §11.A audit findings, Phase 3v §8 stop-trigger-domain
  governance, Phase 3w §6 / §7 / §8 governance, Phase 4j §11 metrics
  OI-subset rule (preserved; not used), Phase 4k / 4q / 4w backtest-
  plan methodologies, Phase 3t 5m closure, and the Phase 4ak twelve-
  clause M0 gate.
- Definition of V1-arc-only future-computation population scope (§6).
- Explicit R3 baseline boundary (§7).
- Predeclared forensic questions (§8).
- Explicit forbidden questions (§9).
- Artefact source plan (§10).
- Field schema plan (§11).
- Metric definitions for future computation (§12).
- Timeframe / data-resolution plan (§13).
- Cost / realized-R plan (§14).
- Stop-trigger-domain plan (§15).
- Output specification for a future computation phase (§16).
- Future computation stop conditions (§17).
- Governance interpretation boundaries (§18).
- Recommendation (§19).
- Implementation / governance review (§20).
- Research interpretation review (§21).
- Explicit preservation of verdicts, locks, no-rescue (§22).

### 2.2 Explicit non-scope

Phase 4ap does NOT and is NOT authorized to:

- compute MFE / MAE / realized-R / time-to-event / target-before-stop /
  stop-before-target / cost-in-R / fee-in-R / slippage-in-R / funding-in-R
  distributions or any other forensic statistic;
- perform exit-path forensics;
- run any backtest;
- execute any historical strategy or research script
  (`scripts/phase2*.py`, `scripts/phase3d_F1_execution.py`,
  `scripts/phase3j_D1A_execution.py`, `scripts/phase3q_5m_acquisition.py`,
  `scripts/phase3s_5m_diagnostics.py`,
  `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`,
  `scripts/phase4r_g1_backtest.py`, `scripts/phase4x_c1_backtest.py`,
  `scripts/phase4ac_alt_symbol_acquisition.py`,
  `scripts/phase4ae_alt_symbol_substrate_feasibility.py`,
  `scripts/phase4af_alt_symbol_regime_persistence.py`,
  `scripts/phase4ai_single_position_cross_sectional_trend.py`);
- run an offline 15m-join MFE / MAE reconstruction (Phase 4ao Route B);
- run a controlled rerun with excursion instrumentation (Phase 4ao
  Route A);
- acquire any data (no 5m / 1m / aggTrades / tick / mark-price 30m / 4h
  / additional data acquisition);
- modify any data file under `data/raw/`, `data/normalized/`,
  `data/derived/`, or `data/research/`;
- modify any manifest under `data/manifests/`;
- modify any source file under `src/prometheus/`;
- modify any test under `tests/`;
- modify any strategy specification under `docs/03-strategy-research/`;
- modify any validation document under `docs/05-backtesting-validation/`;
- modify any roadmap document under `docs/12-roadmap/`;
- modify any governance document under `docs/00-meta/`
  (`m0-mechanism-admissibility-gate.md`, `ai-coding-handoff.md`,
  `implementation-ambiguity-log.md`);
- modify any retained verdict;
- modify any project lock (§11.6, §1.7.3, Phase 3r §8, Phase 3v §8,
  Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q,
  Phase 4v, Phase 4w);
- propose, name, or pre-design a new strategy or exit system;
- optimize R3 or any other V1-arc candidate;
- create R3-prime / R2-prime / R1a-prime / R1b-narrow-prime / any
  successor strategy candidate;
- propose a rescue of any rejected or retained-evidence candidate;
- authorize Phase 4aq, Phase 5, Phase 4 canonical, paper / shadow,
  live-readiness, deployment, exchange-write, production-key creation,
  authenticated APIs, private endpoints, public-endpoint calls in code,
  user stream, WebSocket, listenKey, MCP, Graphify, `.mcp.json`, or
  credentials;
- authorize 5m / 1m / aggTrades / tick / mark-price 30m / 4h data use
  in any future computation;
- amend or override Phase 3t 5m closure;
- amend the Phase 4ak twelve-clause M0 gate, the post-null cooldown
  rule, or the cooled-down families list;
- override Phase 4al §9 refined no-rescue rule, §13 future-Phase-4am-
  style boundary specification, or §14 data-resolution hierarchy;
- override Phase 4ao methodology / artefact harmonization rules.

If a question raised in this memo cannot be answered from static
repository inspection, it is classified explicitly as **unresolved
plan risk** rather than triggering execution.

## 3. Repository Verification Summary

Verification commands and results executed at the start of Phase 4ap on
branch `phase-4ap/v1-arc-exit-path-forensic-plan`:

```text
git status                : clean working tree (untracked
                            .claude/scheduled_tasks.lock and
                            data/research/ are gitignored / transient)
git branch --show-current : phase-4ap/v1-arc-exit-path-forensic-plan
git rev-parse main        : 6c59c5ba6590d2017f873523ceab45c3e5a0139f
git rev-parse origin/main : 6c59c5ba6590d2017f873523ceab45c3e5a0139f
```

main and origin/main agree at `6c59c5b` (the live Phase 4ao merge tip
on both local and remote). The Phase 4ao merge-closeout file at
`docs/00-meta/implementation-reports/2026-05-06_phase-4ao_merge-closeout.md`
records pre-amend SHA `e0c280d` and post-first-amend SHA `eeb6962` per
the documented git self-reference artifact (every amend produces a new
SHA). The live Phase 4ao merge commit on main is `6c59c5b`. This does
not change Phase 4ao's content; the difference is purely SHA
bookkeeping for the amend chain.

All three Phase 4ao files exist on main:

- `docs/00-meta/implementation-reports/2026-05-06_phase-4ao_exit-path-methodology-artefact-harmonization.md`;
- `docs/00-meta/implementation-reports/2026-05-06_phase-4ao_closeout.md`;
- `docs/00-meta/implementation-reports/2026-05-06_phase-4ao_merge-closeout.md`.

The branch for this phase (`phase-4ap/v1-arc-exit-path-forensic-plan`)
was created from clean main.

## 4. Methodology

Phase 4ap methodology is **static repository inspection only**.
Specifically:

- Read Phase 4an inventory memo
  (`2026-05-06_phase-4an_historical-trade-population-exit-path-inventory.md`)
  and Phase 4an closeout / merge-closeout for the per-population
  artefact-availability baseline.
- Read Phase 4ao methodology / artefact harmonization memo
  (`2026-05-06_phase-4ao_exit-path-methodology-artefact-harmonization.md`)
  and Phase 4ao closeout / merge-closeout for the methodology and
  field-definition baseline.
- Read Phase 4al main memo for the §9 refined no-rescue rule, §13
  future-Phase-4am-style boundary specification, §14 data-resolution
  hierarchy, and the §14.C ambiguity-rate concept.
- Read Phase 4am main audit report for the §11.A subjects and F-1 /
  F-2 / F-3 / F-4 findings preserved as documentation.
- Cross-reference `docs/00-meta/m0-mechanism-admissibility-gate.md` for
  the Phase 4ak twelve-clause M0 gate, post-null cooldown rule, and
  cooled-down families list.
- Cross-reference Phase 3t 5m closure, Phase 3r §8 mark-price gap
  governance, Phase 3v §8 stop-trigger-domain governance, Phase 3w
  §6 / §7 / §8 governance, and Phase 4j §11 metrics OI-subset rule
  (preserved; not used by V1-arc plan).

No script was run during Phase 4ap. No backtest was executed. No data
was read other than what was already loaded into the documentation
reading context. No data file was modified. No manifest was modified.
No source / tests / scripts modified.

## 5. Phase 4an / Phase 4ao Baseline

Phase 4ap inherits these baselines verbatim:

### 5.1 Phase 4an inventory baseline

- V1-arc (H0, R3, R1a, R1b-narrow, R2):
  `RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS`. Local
  `trade_log_v1` JSON / Parquet artefacts under
  `data/derived/backtests/phase-2*/<run-stamp>/<symbol>/` contain
  populated `mfe_r` / `mae_r` (15m bar-extreme), all entry / exit
  prices and timestamps, fees, slippage cell, funding, gross / net
  PnL, realized R, initial stop, exit-reason fields, and
  bars_in_trade. Per-cost-cell variants (LOW / MEDIUM / HIGH) and
  trade-price stop-domain variants exist for retained-evidence runs.
- F1, D1-A: `RECONSTRUCTABLE_ONLY_WITH_RERUN` for MFE / MAE;
  `RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS` for non-excursion fields.
- V2, G1, C1: `RECONSTRUCTABLE_ONLY_WITH_RERUN`. Aggregate
  variant-level CSVs only; no per-trade ledger.
- 5m thread: `CLOSED_CONTEXT_ONLY` (Phase 3t).
- Forbidden-rescue-risk: MEDIUM for H0 / R3; HIGH for R1a /
  R1b-narrow; CRITICAL for R2 / F1 / D1-A / V2 / G1 / C1 / 5m thread.

### 5.2 Phase 4ao methodology / artefact harmonization baseline

- Future first-pass forensic scope = V1-arc only.
- R3 inclusion as baseline-of-record descriptive context only (no
  optimization / R3-prime / R3 rescue / baseline revision).
- F1 / D1-A MFE / MAE recovery via Route B (offline 15m-join)
  preferred over Route A (controlled rerun) on rescue-risk grounds;
  neither authorized.
- V2 / G1 / C1 rerun-based per-trade forensics governance-risk-
  unresolved under M0 post-null cooldown; defer to OQ-B resolution
  memo; not authorized.
- Cross-population realized-R / cost comparison requires explicit
  separation across seven accounting axes (engine path; fee assumption;
  slippage cell; funding handling; cost-cell label;
  stop-trigger-domain label; per-trade vs aggregate). §11.6 LOCK
  preserved.
- Stop-trigger-domain (Phase 3v §8) preserved.
- 5m boundary (Phase 3t closure) preserved.
- Minimum predeclared-methodology template (Phase 4ao §14) with 18
  required headings is the precondition for any successor computation
  phase.

### 5.3 V1-arc-only first-pass rationale

Phase 4ap adopts V1-arc-only first-pass scope for these reasons,
inherited from Phase 4ao:

- V1-arc populations require no rerun, no offline reconstruction, and
  no data acquisition for first-pass MFE / MAE / realized-R / cost-
  decomposition forensics; all required fields are populated in
  existing local `trade_log_v1` artefacts.
- F1 / D1-A would require Route B offline 15m-join (preferred) or
  Route A rerun (deprecated on rescue-risk grounds); neither is
  authorized and both would require a separately authorized successor
  phase.
- V2 / G1 / C1 rerun is governance-risk-unresolved under M0 and
  requires a separately authorized OQ-B-resolution memo before
  consideration.
- 5m thread is closed; first-pass forensics on V1-arc does not require
  any 5m use.
- A V1-arc-only first-pass plan is the cleanest path for any future
  forensic phase to satisfy the Phase 4al §9 refined no-rescue rule
  and the Phase 4ak twelve-clause M0 gate without crossing any
  rescue-risk boundary.

## 6. Population Inclusion / Exclusion Table

| Population   | Phase 4an classification                                                         | Phase 4ap inclusion in future computation                          | Role / context                                              |
|--------------|----------------------------------------------------------------------------------|---------------------------------------------------------------------|-------------------------------------------------------------|
| H0           | RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS                                          | INCLUDED                                                            | Framework anchor context                                    |
| R3           | RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS                                          | INCLUDED                                                            | Baseline-of-record DESCRIPTIVE CONTEXT ONLY (see §7)        |
| R1a          | RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS                                          | INCLUDED                                                            | Retained — NON-LEADING descriptive context only             |
| R1b-narrow   | RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS                                          | INCLUDED                                                            | Retained — NON-LEADING descriptive context only             |
| R2           | RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS                                          | INCLUDED                                                            | FAILED — §11.6 cost-fragility descriptive context only      |
| F1           | RECONSTRUCTABLE_ONLY_WITH_RERUN (MFE/MAE) / RECONSTRUCTABLE_WITH_EXISTING (other) | EXCLUDED                                                            | Requires Route B reconstruction; not in V1-arc first-pass   |
| D1-A         | RECONSTRUCTABLE_ONLY_WITH_RERUN (MFE/MAE) / RECONSTRUCTABLE_WITH_EXISTING (other) | EXCLUDED                                                            | Requires Route B reconstruction; not in V1-arc first-pass   |
| V2           | RECONSTRUCTABLE_ONLY_WITH_RERUN                                                  | EXCLUDED                                                            | Rerun governance-risk-unresolved under M0 post-null cooldown |
| G1           | RECONSTRUCTABLE_ONLY_WITH_RERUN                                                  | EXCLUDED                                                            | Rerun governance-risk-unresolved under M0 post-null cooldown |
| C1           | RECONSTRUCTABLE_ONLY_WITH_RERUN                                                  | EXCLUDED                                                            | Rerun governance-risk-unresolved under M0 post-null cooldown |
| 5m thread    | CLOSED_CONTEXT_ONLY                                                              | EXCLUDED                                                            | Phase 3t closure preserved; not reopened                    |

The five included populations are exactly the V1-arc cohort identified
by Phase 4an and confirmed by Phase 4ao §16.2 sample population
eligibility under the §14 template. The six excluded populations match
the Phase 4ao first-pass scope rule.

## 7. Explicit R3 Baseline Boundary

R3 is the project's locked **baseline-of-record** (Phase 2p §C.1; Phase
4y §13.1; Phase 4z; preserved verbatim across all subsequent phases).
R3 inclusion in any future Phase-4ap-derived V1-arc forensic
computation is governance-bounded as follows:

### 7.1 Why R3 may be included

- R3 is the baseline-of-record. Descriptive forensic context on R3 is
  research evidence, NOT optimization input.
- R3 has artefact-ready V1-arc `trade_log_v1` ledgers under
  `data/derived/backtests/phase-2l-r3-r/<run-stamp>/<symbol>/` (and
  per-cost-cell variants `phase-2l-r3-r-slip=LOW`,
  `phase-2l-r3-r-slip=HIGH`, `phase-2l-r3-r-stop=TRADE_PRICE`; plus
  validation-window variants `phase-2l-r3-v`).
- R3 has populated `mfe_r` and `mae_r` fields (15m bar-extreme via the
  V1 management module).
- Excluding R3 would distort any V1-arc cross-population descriptive
  comparison because R3 is the framework reference cell.

### 7.2 Why R3 inclusion is descriptive only

R3 inclusion is **descriptive only**. The future computation phase
must:

- treat R3 forensic distributions (MFE_R, MAE_R, realized net_R,
  cost-in-R, fee-in-R, slippage-in-R, funding-in-R, etc.) as research
  evidence about the R3 trade population AS-IS;
- treat R3 cost-cell variants as research evidence about R3 cost
  sensitivity AS-IS, never as a license to revise §11.6;
- treat R3 trade-price stop-domain variant as research evidence about
  R3 stop-domain behaviour AS-IS, never as a license to revise §1.7.3
  mark-price-stops or Phase 3v §8 stop-trigger-domain governance.

### 7.3 What R3 inclusion does NOT allow

R3 inclusion does NOT allow:

- **R3 optimization** — no parameter tuning on R3 trades; no take-
  profit multiple search; no stop-distance search; no time-stop search;
  no bar-count tuning; no cost-cell selection beyond the existing
  `slippage_bucket` enum.
- **R3-prime** — no new strategy candidate "derived from R3" with
  modified parameters or additional filters.
- **R3 rescue** — no reframing of R3 outcomes as "would have worked
  better with rule X"; no conversion of MFE / MAE patterns into
  rule candidates.
- **Baseline-of-record revision** — R3 remains baseline-of-record
  regardless of forensic findings; no descriptive forensic finding
  may demote R3, promote any other V1-arc candidate, or change R3's
  framework role.
- **Strategy parameter / threshold / entry-rule / exit-rule
  conversion** — R3 forensic distributions cannot be used as inputs
  for any future strategy spec, hypothesis-spec memo, fresh-hypothesis
  discovery memo, or candidate naming.
- **New candidate creation** — Phase 4m's 18-requirement fresh-
  hypothesis validity gate and Phase 4ak's twelve-clause M0 gate
  remain binding; R3 forensic findings are not a predeclared
  hypothesis source.

The same constraints apply to R1a, R1b-narrow, and R2 forensic
inclusion. H0's framework-anchor role remains unchanged regardless of
forensic findings.

## 8. Predeclared Forensic Questions for a Future Computation Phase

Any future V1-arc-only computation phase, if separately authorized,
must answer the following predeclared **descriptive** questions and
nothing else. Each question is a forensic-statistics question, not a
strategy-design question.

### 8.1 Distributional questions

- **Q1**: What are the MFE_R distributions by population (H0 / R3 /
  R1a / R1b-narrow / R2), by symbol (BTCUSDT / ETHUSDT), by side
  (LONG / SHORT), by exit reason (STOP / TAKE_PROFIT / TIME_STOP /
  other), and by cost cell (LOW / MEDIUM / HIGH)? Reported as
  per-cell summary statistics (count, mean, median, stdev, min,
  P25, P50, P75, P90, P95, P99, max).
- **Q2**: What are the MAE_R distributions by the same cells as Q1?
- **Q3**: What are the realized net_R distributions by the same cells
  as Q1?

### 8.2 Relationship questions

- **Q4**: What is the relationship between MFE_R and realized net_R
  by population? Reported as descriptive summary tables; no
  regression / model fitting is required.
- **Q5**: What is the relationship between MAE_R and realized net_R
  by population? Reported as in Q4.

### 8.3 Threshold-touch questions

- **Q6**: What fraction of trades reached MFE_R ≥ 1, ≥ 2, ≥ 3 before
  exit, by population / symbol / side / cost cell? Computed using the
  existing `mfe_r` field. (Note: bar-resolution ambiguity disclaim
  applies per Phase 4al §11.A.11 and Phase 4ao §8.5.)
- **Q7**: What fraction of stopped trades had MFE_R > 0 prior to stop?
  Reported by population / symbol / side / cost cell.

### 8.4 Path-anatomy questions

- **Q8**: What fraction of winners (exit_reason = TAKE_PROFIT or
  net_r_multiple > 0) had MFE_R giveback (defined as MFE_R − net_R)
  greater than 0.25 R, 0.5 R, 1.0 R? Reported by population.
- **Q9**: What fraction of trades had `mae_r > mfe_r` at any point
  during the trade lifetime (adverse-before-favorable)?
- **Q10**: What fraction of trades had `mfe_r ≥ 0.5 R` before being
  stopped (favorable-before-stop)?

### 8.5 Cost-decomposition questions

- **Q11**: How do cost-in-R, fee-in-R, slippage-in-R, and funding-in-R
  vary by population and cost cell? Reported descriptively per Phase
  4ao §11 seven-axis disclaim; no §11.6 revision implied.
- **Q12**: How much of R2 failure is visible as cost-in-R fragility
  descriptively, without revising §11.6? Reported as descriptive
  evidence about R2 cost-cell sensitivity; R2 verdict (FAILED — §11.6)
  preserved verbatim regardless of finding.

### 8.6 Cross-population descriptive comparison

- **Q13**: How do H0 / R3 / R1a / R1b-narrow / R2 compare descriptively
  across MFE_R, MAE_R, realized net_R, cost-in-R, exit-reason
  composition, and threshold-touch rates? Reported as cross-population
  tables with explicit accounting-equivalence disclaim per Phase 4ao
  §11 (V1-arc engine path; 5 bps / side fee assumption; LOW / MEDIUM /
  HIGH slippage cells; stop_trigger_domain = trade_price_backtest;
  per-trade granularity). NO ranking for promotion. NO baseline
  revision. R3 remains baseline-of-record regardless of finding.

### 8.7 Bar-resolution ambiguity reporting

- **Q14**: Where does 15m bar-resolution ambiguity prevent
  unambiguous interpretation of stop-vs-target / target-vs-time-stop /
  entry-bar-exit sequencing? Reported as ambiguity-rate by population
  and exit-reason category, per Phase 4al §14.C bands (<2% / 2–10% /
  >10% / >20%). NO 5m / 1m escalation is performed in the future
  computation phase; ambiguity bands above >10% may motivate a
  separately authorized successor phase under Phase 4al §14 hierarchy
  (NOT authorized by Phase 4ap).

These 14 questions exhaust the forensic scope. Any other question is
either out of scope or forbidden (§9).

## 9. Explicit Forbidden Questions

A future V1-arc-only computation phase, if separately authorized, must
**reject** any of the following questions. Each is forbidden because
it converts descriptive forensics into strategy design, optimization,
verdict revision, or lock revision.

- **F1**: Which exit rule would make R3 profitable?
- **F2**: Which TP / SL should replace R3?
- **F3**: What is the best take-profit multiple?
- **F4**: What parameters should we tune?
- **F5**: Can R2 be rescued if costs are lower?
- **F6**: Can R1a / R1b-narrow become leading?
- **F7**: Can H0 / R3 be turned into R3-prime?
- **F8**: Can V1-arc be hybridized with F1 / D1-A / V2 / G1 / C1?
- **F9**: Can 5m signals improve exits?
- **F10**: Any question that converts descriptive forensics into
  strategy design, optimization, verdict revision, lock revision,
  baseline-of-record revision, framework-anchor revision, or successor-
  candidate creation.

The future computation phase must produce a `forbidden_interpretation_checklist.md`
artefact that affirms zero forbidden-question forms were addressed
during execution (§16).

## 10. Artefact Source Plan

Future computation phase, if separately authorized, would source from:

### 10.1 V1-arc trade-log artefacts (existing, gitignored, locally present)

```text
data/derived/backtests/phase-2e-baseline/<run-stamp>/<symbol>/
  trade_log.json
  trade_log.parquet
  summary_metrics.json
  funnel_total.json
  r_multiple_hist.parquet
  equity_curve.parquet
  monthly_breakdown.parquet
  yearly_breakdown.parquet
  drawdown.parquet
```

per-population lineage (per Phase 4an §6):

- **H0**: `data/derived/backtests/phase-2e-baseline/<run-stamp>/<symbol>/`
  and `data/derived/backtests/phase-2g-wave1-h0-r/<run-stamp>/<symbol>/`.
- **R3**: `data/derived/backtests/phase-2l-r3-r/<run-stamp>/<symbol>/`
  + per-cost-cell variants `phase-2l-r3-r-slip=LOW` /
  `phase-2l-r3-r-slip=HIGH` + trade-price stop-domain variant
  `phase-2l-r3-r-stop=TRADE_PRICE` + validation-window variant
  `phase-2l-r3-v`.
- **R1a**: `data/derived/backtests/phase-2m-r1a-r1a_plus_r3-r/<run-stamp>/<symbol>/`
  + per-cost-cell variants and validation-window variants per the
  same naming pattern.
- **R1b-narrow**: `data/derived/backtests/phase-2s-r1b-r1b_narrow-r/<run-stamp>/<symbol>/`
  + per-cost-cell variants and validation-window variants.
- **R2**: `data/derived/backtests/phase-2w-r2-r2_r3-r/<run-stamp>/<symbol>/`
  + per-cost-cell variants `-slip=LOW` / `-slip=HIGH` +
  trade-price stop-domain variant `-stop=TRADE_PRICE` +
  fill-variant `-fill=limit-at-pullback` + validation-window variant
  `phase-2w-r2-r2_r3-v`.

### 10.2 Manifest references (read-only)

The future computation phase would reference manifest entries under
`data/manifests/` for V1-arc dataset provenance (v002 BTCUSDT /
ETHUSDT 15m + 1h-derived). NO manifest is modified.

### 10.3 No artefact modification

Phase 4ap explicitly states: **no manifest, data file, normalized data,
trade ledger, derived artefact, source file, test, or script is to be
modified by Phase 4ap, by any successor V1-arc-only computation phase,
or by any future phase derived from this plan.** The future computation
phase, if separately authorized, must produce ONLY new artefacts under a
predeclared output directory (§16) and must not touch any existing
artefact under `data/raw/`, `data/normalized/`, `data/derived/`,
`data/manifests/`, `src/prometheus/`, `tests/`, or `scripts/`.

## 11. Field Schema Plan

Future computation phase, if separately authorized, would read these 25
required fields from each V1-arc `trade_log_v1` JSON / Parquet artefact:

```text
1.  trade_id                  (string)
2.  population / candidate_id (string; one of H0|R3|R1a|R1b-narrow|R2)
3.  symbol                    (string; BTCUSDT or ETHUSDT)
4.  side / direction          (string; LONG or SHORT)
5.  entry_fill_time_ms        (int64; UTC ms)
6.  exit_fill_time_ms         (int64; UTC ms)
7.  entry_fill_price          (float64)
8.  exit_fill_price           (float64)
9.  initial_stop              (float64)
10. stop_distance             (float64)
11. realized_risk_usdt        (float64)
12. gross_pnl                 (float64; USDT)
13. net_pnl                   (float64; USDT)
14. net_r_multiple            (float64; equivalent to "realized R")
15. entry_fee                 (float64; USDT)
16. exit_fee                  (float64; USDT)
17. funding_pnl               (float64; USDT; signed)
18. fee_rate_assumption       (float64; e.g. 0.0005 = 5 bps/side)
19. slippage_bucket           (string; LOW|MEDIUM|HIGH)
20. exit_reason               (string; STOP|TAKE_PROFIT|TIME_STOP|...)
21. bars_in_trade             (int64; 15m bar count from entry to exit)
22. mfe_r                     (float64; 15m bar-extreme; R-units)
23. mae_r                     (float64; 15m bar-extreme; R-units)
24. stop_was_gap_through      (bool)
25. stop_trigger_domain       (string; trade_price_backtest for V1-arc)
```

Plus the timeframe / data-resolution label (§13) which is fixed at
`15m` for the V1-arc first-pass.

The `population / candidate_id` field is NOT directly stored in
`trade_log_v1`; it must be inferred from the artefact source path (the
`<phase>-r-<id>` directory name encodes the population). The future
computation phase must include this inference step in its predeclared
methodology and must NOT mix populations across artefacts.

If any artefact is missing any of the 25 required fields, OR if the
inferred population does not match an expected V1-arc candidate, the
future computation phase must STOP per §17.

## 12. Metric Definitions for Future Computation

All metrics use Phase 4ao §6 definitions verbatim. The 14 metrics are
listed below; see Phase 4ao §6 / §8 for complete definitions.

```text
1.  MFE_R                  : maximum favorable excursion in R units
                              (Phase 4ao §6; computed source =
                              mfe_r field)
2.  MAE_R                  : maximum adverse excursion in R units
                              (mae_r field)
3.  net_R                  : realized R (net_r_multiple field)
4.  gross_R                : gross_pnl / realized_risk_usdt
5.  cost-in-R              : (gross_pnl - net_pnl) / realized_risk_usdt
6.  fee-in-R               : (entry_fee + exit_fee) / realized_risk_usdt
7.  slippage-in-R          : descriptive only; specific definition must
                              be predeclared in any future computation
                              phase (Phase 4ao §6); typically derived
                              from cost cell bps × notional / risk
8.  funding-in-R           : funding_pnl / realized_risk_usdt
9.  reached_+1R_flag       : 1 if mfe_r >= 1.0 else 0
10. reached_+2R_flag       : 1 if mfe_r >= 2.0 else 0
11. reached_+3R_flag       : 1 if mfe_r >= 3.0 else 0
12. MFE_capture_ratio      : net_R / mfe_r (only defined for mfe_r > 0;
                              else N/A)
13. giveback_from_MFE      : mfe_r - net_R (in R units; never negative
                              under the definition; describes how much
                              of MFE was given back at exit)
14. adverse_before_favorable_flag : 1 if mae_r > 0 occurred before
                              mfe_r > 0 within the trade lifetime; this
                              is RECONSTRUCTABLE_ONLY_WITH_RERUN under
                              the existing schema because intra-bar
                              order is not preserved (the existing
                              schema preserves only end-of-trade max
                              MFE / max MAE). Future computation must
                              flag this as N/A or as a Phase 4al §14
                              ambiguity case rather than computing it
                              naively.
```

Bar-resolution ambiguity flag (BRA-flag) is NOT a metric per se but a
disclaim category applied per trade where 15m granularity prevents
unambiguous stop-vs-target / target-vs-time-stop / entry-bar-exit
sequencing per Phase 4al §11.A.11 and Phase 4am §11.A.11 F-4. The
future computation phase must record the BRA-flag rate by population
and exit-reason and report it in `ambiguity_report.csv` (§16).

Phase 4ap does NOT compute any of these metrics. The above is a
specification.

## 13. Timeframe / Data-Resolution Plan

### 13.1 First-pass: 15m only

The V1-arc first-pass plan uses existing 15m V1-arc artefacts only:

- 15m bars (v002 BTCUSDT / ETHUSDT 15m manifests are
  `research_eligible: true`; per-cost-cell variants exist).
- 1h-derived bars are reporting context only (NOT used for forensic
  per-trade computation; Phase 4w convention: 1h-derived is
  reporting context).
- 30m / 4h / 5m / 1m / aggTrades / tick / mark-price 30m / 4h / 5m
  data is NOT used in Phase 4ap and NOT used in any future
  Phase-4ap-derived V1-arc first-pass computation.

### 13.2 Lower-timeframe escalation deferred

Per Phase 4al §14 hierarchy and Phase 4ao §13.3 conservative criterion:

- 5m may be proposed only as a later measurement-layer escalation
  if a future computation phase finds bar-resolution ambiguity above
  the Phase 4al §14.C >10% / >20% bands (Q14 ambiguity reporting).
- Even then, 5m use is NOT authorized by Phase 4ap; it would require
  a separately authorized successor phase satisfying Phase 4ao
  §13.3 conservative criterion verbatim:
  - the 5m data is used to resolve a specific predeclared bar-
    resolution ambiguity for an existing strategy population's trade
    ledger;
  - no new 5m strategy or rule is derived;
  - no Q1–Q7 finding is converted into a rule input;
  - the 5m data use is documented in the predeclared forensic
    methodology before computation;
  - the 5m data use is separately authorized by a successor phase.
- 1m is escalation only if 5m exceeds Phase 4al §14.C bands; NOT
  authorized.
- aggTrades / tick is final escalation; NOT authorized.

### 13.3 Mark-price path forensics blocked

Per Phase 3v §8 stop-trigger-domain governance and §1.7.3 mark-price-
stops lock: mark-price path forensics for live-readiness remains
BLOCKED. The future computation phase, if separately authorized, must
NOT attempt mark-price-domain analysis. Mark-price 30m / 4h data is
NOT acquired and NOT authorized.

## 14. Cost / Realized-R Plan

### 14.1 §11.6 LOCK preserved

§11.6 HIGH cost = 8 bps slippage per side; round-trip = 16 bps;
taker fee = 4 bps per side; no maker rebates; no live fee assumption.
Phase 4ap preserves §11.6 verbatim. Any future fee / slippage /
funding decomposition is descriptive only.

### 14.2 Future cost decomposition is descriptive only

Per Phase 4ao §11 and the operator's Phase 4ap brief: any future fee /
slippage / funding decomposition reported by a V1-arc-only computation
phase must be descriptive only. Such decomposition:

- MUST NOT change the locked project-level cost reference (§11.6
  remains 8 bps per side);
- MUST NOT revise any historical result;
- MUST NOT be used as input to any future strategy spec, hypothesis
  spec, threshold revision, or candidate creation;
- MUST report all components (fee-in-R, slippage-in-R, funding-in-R,
  cost-in-R) per the Phase 4ao §6 definitions.

### 14.3 Cost-cell descriptive comparison

LOW / MEDIUM / HIGH cost-cell variants exist on disk for V1-arc
populations. Cross-cost-cell comparison is descriptive only:

- LOW / MEDIUM / HIGH cells correspond to 1 / 4 / 8 bps slippage per
  side (per Phase 4k convention; and matching Phase 4am §11.A.2).
- Per-cost-cell summaries are reported as research evidence about
  cost sensitivity AS-IS.
- Cross-cell outperformance at LOW vs HIGH does NOT justify §11.6
  relaxation; §11.6 LOCK is binding regardless of any descriptive
  finding.

### 14.4 R2 cost-fragility is retained failed evidence

R2 is FAILED — §11.6 cost-sensitivity blocks (Phase 2w §16.1
verdict; preserved across Phase 4y / Phase 4z / Phase 4m / Phase 4n /
Phase 4al / Phase 4am / Phase 4an / Phase 4ao). Any future R2 cost-
fragility forensic finding is **retained failed evidence**, not rescue.
The future computation phase must NOT reframe R2 outcomes as
"would-have-worked-at-lower-cost" or convert R2 cost patterns into
rule candidates. R2 verdict (FAILED — §11.6) is preserved verbatim
regardless of forensic finding.

### 14.5 Fee-assumption disclaim across populations

Per Phase 4ao §11 and Phase 4am §11.A.2: V1-arc / F1 / D1-A use
`fee_rate_assumption = 0.0005` = 5 bps / side; V2 / G1 / C1 use
4 bps / side. The V1-arc-only first-pass scope (Phase 4ap §6) avoids
the cross-population fee-assumption disclaim because it includes only
V1-arc; therefore the V1-arc first-pass uses 5 bps / side fee
assumption uniformly. No fee normalization is required for the V1-arc
first-pass scope. (Cross-population comparison requiring fee
normalization is out of Phase 4ap scope and would need a separately
authorized cross-population computation phase.)

## 15. Stop-Trigger-Domain Plan

### 15.1 V1-arc historical = trade_price_backtest

Per Phase 3v §8 stop-trigger-domain governance and Phase 4am §11.A.5:
all V1-arc historical backtests use `stop_trigger_domain =
trade_price_backtest`. Stop hits are evaluated against kline
trade-price `low` / `high`. No mark-price-domain stop simulation
exists in the V1-arc lineage.

### 15.2 mixed_or_unknown invalid

Per Phase 3v §8: `mixed_or_unknown` is invalid and fails closed at
any decision boundary. The future computation phase must verify each
trade ledger's stop-trigger-domain label (or infer it from the
artefact source if not stored as a field) and STOP if any trade
records `mixed_or_unknown`.

### 15.3 mark_price_runtime is runtime / live only

`mark_price_runtime` is the §1.7.3 lock for any future runtime /
paper / live operation. Phase 4ap is docs-only and does not engage
with `mark_price_runtime` operationally.

### 15.4 mark_price_backtest_candidate not authorized

`mark_price_backtest_candidate` is a research label for any future
backtest that explicitly models mark-price stop-domain. No such
research run exists for V1-arc. Phase 4ap does NOT authorize creation
of any `mark_price_backtest_candidate` run for V1-arc or any other
population.

### 15.5 No mark-price path forensics

Phase 4ap explicitly prohibits mark-price path forensics in any
Phase-4ap-derived V1-arc first-pass computation. The future
computation phase, if separately authorized, must use only
trade-price domain artefacts.

## 16. Output Specification for a Future Computation Phase

Future V1-arc-only computation phase, if separately authorized, would
produce these 9 output artefacts under a predeclared output directory
(e.g., `data/derived/forensics/phase-<id>/` or
`data/research/phase-<id>/`; final path to be predeclared in the
successor phase's methodology):

```text
1.  population_summary.csv
    Columns: population, symbol, side, cost_cell, exit_reason,
             trade_count, mean_net_R, median_net_R, stdev_net_R,
             mean_mfe_R, mean_mae_R, mean_bars_in_trade.

2.  mfe_mae_distribution_by_population.csv
    Columns: population, symbol, side, cost_cell, exit_reason,
             metric (mfe_R | mae_R), count, mean, median, stdev,
             min, P25, P50, P75, P90, P95, P99, max.

3.  realized_r_by_population.csv
    Columns: population, symbol, side, cost_cell, exit_reason,
             count, mean_net_R, median_net_R, stdev_net_R,
             P5_net_R, P25_net_R, P75_net_R, P95_net_R,
             win_rate (% with net_R > 0), profit_factor.

4.  cost_in_r_by_population.csv
    Columns: population, symbol, side, cost_cell, count,
             mean_cost_in_R, mean_fee_in_R, mean_slippage_in_R,
             mean_funding_in_R, stdev_cost_in_R.

5.  exit_reason_breakdown.csv
    Columns: population, symbol, side, cost_cell, exit_reason,
             count, share, mean_net_R_for_reason, mean_mfe_R_for_reason,
             mean_mae_R_for_reason.

6.  excursion_threshold_touch_rates.csv
    Columns: population, symbol, side, cost_cell, threshold (1R | 2R |
             3R), count_reached, share_reached.

7.  ambiguity_report.csv
    Columns: population, symbol, side, cost_cell, exit_reason,
             ambiguity_category (Phase 4al §14.C: <2% | 2-10% |
             >10% | >20%), count, share.

8.  forbidden_interpretation_checklist.md
    Affirmation that:
    - no Phase 4ap §9 forbidden question form was addressed;
    - no R3 optimization / R3-prime / R3 rescue / baseline-of-record
      revision was attempted;
    - no R2 rescue / §11.6 relaxation interpretation was attempted;
    - no R1a / R1b-narrow promotion was attempted;
    - no V1-arc hybridization with F1 / D1-A / V2 / G1 / C1 was
      attempted;
    - no 5m / 1m / aggTrades / tick / mark-price 30m / 4h data was
      used or consulted;
    - no manifest, data file, source file, test, or script was
      modified;
    - no successor phase was authorized.

9.  v1_arc_forensic_report.md
    The future computation phase report markdown. Must include:
    - phase identity, branch, base SHA, commit SHA;
    - population scope (H0 / R3 / R1a / R1b-narrow / R2);
    - 14 forensic question answers (§8.1–§8.7) with reference to
      output CSVs;
    - explicit no-rescue statement (verbatim from Phase 4al §9);
    - explicit verdict / lock preservation statement (verbatim from
      Phase 4ap §22);
    - Phase 4ap-style closeout + merge-closeout per operator
      convention.
```

Phase 4ap does NOT create these output artefacts. The above is a
specification only.

## 17. Future Computation Stop Conditions

Any future V1-arc-only computation phase, if separately authorized,
must STOP and produce a fail-closed report rather than continue
computation, on any of these 11 conditions:

```text
SC-1.  Missing artefact path for any included population.
SC-2.  Missing required field (any of the 25 fields in §11) in any
       loaded trade ledger.
SC-3.  mixed_or_unknown stop-trigger-domain on any trade.
SC-4.  Unexpected schema mismatch (e.g., schema_version != trade_log_v1
       or column type drift).
SC-5.  Attempt to include any excluded population (F1 / D1-A / V2 / G1 /
       C1 / 5m thread).
SC-6.  Attempt to use 5m / 1m / aggTrades / tick / mark-price 30m / 4h
       / additional data without separate authorization.
SC-7.  Attempt to rank V1-arc populations for promotion (§9 F6, F7).
SC-8.  Attempt to propose parameter changes (§9 F1, F2, F3, F4, F5).
SC-9.  Attempt to revise any retained verdict or any project lock
       (§22).
SC-10. Any computation result that requires strategy interpretation
       rather than descriptive reporting (§9 F10).
SC-11. Quality-gate failure — ruff/ pytest/ mypy violation introduced
       by the future computation phase's code (per Phase 4al §13
       boundary specification).
```

## 18. Governance Interpretation Boundaries

Phase 4ap preserves the following governance verbatim and does NOT
amend any of them:

- **Phase 4ak twelve-clause M0 mechanism-admissibility gate** (M0.1–M0.12).
- **Phase 4ak post-null cooldown rule**.
- **Phase 4ak cooled-down families list** (price-only single-symbol
  directional continuation DEPLETED; cross-sectional trend / relative-
  strength symbol selection under Phase 4ai descriptors COOLED_DOWN
  AFTER_NOT_SUPPORTED; derivatives-context directional CONDITIONAL_ONLY
  HIGH_D1-A_RESCUE_RISK; microstructure / order-flow NOT_RECOMMENDED_NOW;
  mark-price stop-domain NOT_RECOMMENDED_NOW).
- **Phase 4al refined no-rescue rule** (§9): forbidden activities
  (parameter tuning on rejected / retained populations; retrofitting
  exit rules; converting descriptive observations into strategy
  candidates; verdict revision; live-readiness implication) vs allowed
  activities (predeclared forensic audit; descriptive distributions;
  realized-R / cost decomposition; bar-ambiguity audit; backtest-logic
  audit) subject to §9.C predeclaration discipline.
- **Phase 4al §13 future-Phase-4am-style boundary specification**:
  standalone-script mode; no `prometheus.runtime/execution/persistence`
  imports; no exchange adapters; no network I/O; no credentials; no
  Binance API; allowed scope = §9.B / §10.A / §11.A activities subject
  to predeclaration; forbidden scope = §9.A / §10.B / §11.B activities;
  required predeclaration content (12 items); required reporting
  content (9 items).
- **Phase 4al §14 data-resolution hierarchy**: 15m / 30m / 1h / 4h
  signal/event context; 5m measurement-layer escalation under
  ambiguity threshold; 1m escalation if 5m exceeds bands; aggTrades /
  tick final escalation; mark-price stop-domain blocked.
- **Phase 4am §11.A audit findings (F-1 / F-2 / F-3 / F-4)**: preserved
  as documentation for future methodology-harmonization scoping; not
  applicable to V1-arc backtest engine accounting (which uses the
  executed-price formula consistent with Phase 4q / 4w; V2's
  flat-`entry_price` cost approximation is V2-specific).
- **Phase 4an inventory result**: V1-arc
  RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS; F1 / D1-A
  RECONSTRUCTABLE_ONLY_WITH_RERUN for MFE / MAE; V2 / G1 / C1
  RECONSTRUCTABLE_ONLY_WITH_RERUN; 5m thread CLOSED_CONTEXT_ONLY;
  forbidden-rescue-risk profile preserved.
- **Phase 4ao methodology / artefact harmonization result**: six
  headline rules + 18-heading minimum predeclared-methodology template
  preserved.
- **Phase 3t 5m research thread closure**: preserved.
- **Phase 3v §8 stop-trigger-domain governance**: preserved.
- **Phase 3r §8 mark-price gap governance**: preserved.
- **Phase 3w §6 / §7 / §8 break-even / EMA-slope / stagnation
  governance**: preserved.
- **Phase 4j §11 metrics OI-subset partial-eligibility rule**:
  preserved (not used by V1-arc plan).
- **Phase 4k V2 backtest-plan methodology**: preserved.
- **Phase 4p G1 strategy-spec memo**: preserved.
- **Phase 4q G1 backtest-plan methodology**: preserved.
- **Phase 4v C1 strategy-spec memo**: preserved.
- **Phase 4w C1 backtest-plan methodology**: preserved.
- **§11.6 HIGH cost = 8 bps per side**: preserved.
- **§1.7.3 0.25% / 2× / one-position / mark-price stops**: preserved.

Phase 4ap does NOT amend any of the above. Any successor V1-arc-only
computation phase must operate within these boundaries.

## 19. Recommendation

### 19.1 Primary

**Remain paused.** Phase 4ap records the V1-arc-only forensic plan on
the project record. No computation is required to proceed; no successor
phase is authorized.

### 19.2 Conditional secondary (NOT authorized by Phase 4ap)

The operator may later authorize a future docs-and-code V1-arc-only
exit-path computation phase exactly under this plan. If so, the
successor phase MUST satisfy the Phase 4ao §14 18-heading minimum
predeclared-methodology template, the Phase 4al §13 boundary
specification (standalone-script mode; no
`prometheus.runtime/execution/persistence` imports; no network I/O; no
credentials), the Phase 4ap §6 V1-arc-only population scope, the
Phase 4ap §11 25-field schema, the Phase 4ap §12 14 metric definitions,
the Phase 4ap §13 15m-only timeframe rule, the Phase 4ap §14 §11.6-LOCK
cost rules, the Phase 4ap §15 trade-price-only stop-trigger-domain rule,
the Phase 4ap §16 9 output artefacts, the Phase 4ap §17 11 stop
conditions, the Phase 4ap §18 governance preservation, and the Phase 4ap
§7 explicit R3 baseline boundary (descriptive only; NO optimization,
R3-prime, R3 rescue, or baseline-of-record revision).

### 19.3 Conditional tertiary (NOT authorized by Phase 4ap)

The operator may later authorize a future docs-only narrower refinement
memo such as:

- a Phase 4ao-style §14 18-heading template re-validation memo
  (validating that the template captures all preconditions for the
  successor phase before code is written);
- an OQ-B-resolution memo addressing V2 / G1 / C1 rerun admissibility
  under M0 post-null cooldown (would unlock V2 / G1 / C1 forensics
  consideration only; would NOT authorize V1-arc forensics);
- an F1 / D1-A Route B reconstruction methodology memo (would specify
  the offline 15m-join script boundary; would NOT authorize execution).

Each of these is independent of the V1-arc-only first-pass and of each
other; combining them into a single successor phase is NOT recommended.

### 19.4 Not recommended

- Starting V1-arc forensic computation without satisfying Phase 4ao §14
  + Phase 4ap §6 / §7 / §8–§17 in a separately authorized successor
  phase.
- Treating Phase 4ap's allowed-questions list (§8) as authorization to
  compute.
- Using Phase 4ap's V1-arc inclusion as license to revisit R3 / R1a /
  R1b-narrow / R2 verdicts, parameters, or candidates.
- Combining the conditional secondary with any of the tertiary memos
  in a single successor phase.

### 19.5 Forbidden

- Paper / shadow / live / exchange-write / production-key creation /
  authenticated APIs / private endpoints / public-endpoint calls in
  code / user stream / WebSocket / MCP / Graphify / `.mcp.json` /
  credentials.
- Any strategy resurrection (R3-prime / R1a-prime / R1b-narrow-prime /
  R2-prime / F1-prime / D1-A-prime / D1-B / V2-prime / V2-narrow /
  V2-relaxed / V2 hybrid / G1-prime / G1-narrow / G1-extension / G1
  hybrid / C1-prime / C1-narrow / C1-extension / C1 hybrid / V1-D1 /
  F1-D1 / any cross-strategy hybrid).
- Any verdict revision; any project-lock revision; any §11.6
  relaxation; any §1.7.3 relaxation; any M0 amendment derived from
  Phase 4ap reasoning; any Phase 3v §8 / Phase 3w §6 / §7 / §8 /
  Phase 3r §8 / Phase 4j §11 / Phase 4k / 4q / 4w / Phase 4p / 4v
  amendment; reopening the 5m research thread; acquisition of 5m / 1m /
  aggTrades / tick / mark-price 30m / 4h data without separately
  authorized data-requirements memo.

**Phase 4ap does not authorize any successor phase.** **Phase 4ap does
not authorize computation.**

## 20. Implementation / Governance Review

### 20.1 What changed?

Phase 4ap added two new files:

```text
docs/00-meta/implementation-reports/2026-05-06_phase-4ap_v1-arc-exit-path-forensic-plan.md
docs/00-meta/implementation-reports/2026-05-06_phase-4ap_closeout.md
```

and added a narrow paragraph + "Current phase:" block update to:

```text
docs/00-meta/current-project-state.md
```

recording the Phase 4ap plan result and reaffirming preserved verdicts
and locks.

### 20.2 What did not change?

- `docs/00-meta/m0-mechanism-admissibility-gate.md` (Phase 4ak
  governance): unchanged.
- All twelve M0 clauses M0.1–M0.12: unchanged.
- The post-null cooldown rule: unchanged.
- The cooled-down families list: unchanged.
- All retained verdicts: unchanged.
- All project locks: unchanged (§11.6, §1.7.3, Phase 3r §8, Phase 3v §8,
  Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q,
  Phase 4v, Phase 4w).
- All scripts under `scripts/`: unchanged.
- All source files under `src/prometheus/`: unchanged.
- All tests under `tests/`: unchanged.
- All data files under `data/raw/`, `data/normalized/`, `data/derived/`,
  `data/research/`: unchanged.
- All manifests under `data/manifests/`: unchanged.
- `docs/12-roadmap/phase-gates.md`: unchanged.
- `docs/12-roadmap/technical-debt-register.md`: unchanged.
- `docs/00-meta/ai-coding-handoff.md`: unchanged.
- `docs/00-meta/implementation-ambiguity-log.md`: unchanged.

### 20.3 Were any locks, verdicts, or safety boundaries affected?

No. All locks, verdicts, and safety boundaries are preserved verbatim.

### 20.4 Were any scripts, source files, data, manifests, or tests modified?

No.

### 20.5 Is the phase mergeable as docs-only?

Yes. Phase 4ap is mergeable as docs-only. Per operator brief, this
prompt does NOT merge Phase 4ap to main; the merge is operator-driven
in a future prompt.

## 21. Research Interpretation Review

### 21.1 What did this phase prove?

Phase 4ap proved, by static repository inspection only, that:

- A complete V1-arc-only forensic computation specification can be
  authored as a docs-only plan, predeclaring the population scope (H0 /
  R3 / R1a / R1b-narrow / R2), the artefact source (existing
  `trade_log_v1` JSON / Parquet under `data/derived/backtests/`), the
  25-field schema, the 14 forensic metrics, the 14 forensic questions,
  the 10 forbidden questions, the 9 output artefacts, the 11 stop
  conditions, the 18-heading minimum predeclared-methodology template
  inheritance from Phase 4ao §14, and the verdict / lock preservation
  contract — without revising any retained verdict, project lock,
  governance text, source code, test, script, data file, or manifest.
- R3 inclusion is governance-bounded as descriptive context only; R3
  optimization, R3-prime, R3 rescue, and baseline-of-record revision
  are explicitly forbidden.
- F1 / D1-A / V2 / G1 / C1 / 5m thread are excluded from V1-arc-only
  first-pass; their inclusion would require separately authorized
  Route B reconstruction (F1 / D1-A) or OQ-B resolution memo (V2 / G1 /
  C1) or are permanently CLOSED_CONTEXT_ONLY (5m thread).
- §11.6 LOCK is preserved verbatim; cost-cell descriptive comparisons
  are research evidence about cost sensitivity, never license for
  §11.6 relaxation.
- Stop-trigger-domain governance and 5m closure remain binding.

### 21.2 What did this phase not prove?

Phase 4ap did NOT prove:

- the actual MFE / MAE / realized-R / cost-decomposition distributions
  on any V1-arc population (no computation done);
- whether descriptive forensic findings on V1-arc would be
  scientifically interesting or methodologically uninteresting;
- whether bar-resolution ambiguity would exceed Phase 4al §14.C bands
  in practice (only authorized computation can determine);
- which V1-arc population's forensic distributions are most
  informative;
- any specific numerical claim about R3 / R1a / R1b-narrow / R2 cost
  sensitivity, MFE giveback, threshold-touch rates, or exit-reason
  composition.

### 21.3 Which original questions did it answer?

- The Phase 4ao §16.2 sample population eligibility under the §14
  template: V1-arc-only first-pass scope confirmed.
- The Phase 4ao OQ-D template specification: 18 required headings
  inherited verbatim plus Phase 4ap-specific section headings (§§6–17)
  layered on top.
- The Phase 4ap operator-brief preconditions for any future V1-arc
  computation: §6–§17 collectively answer them.

### 21.4 Which original questions remain open?

- **OQ-A** (offline 15m-join MFE / MAE recovery sufficiency for F1 /
  D1-A): unresolved; out of Phase 4ap scope (V1-arc-only first-pass
  excludes F1 / D1-A).
- **OQ-B** (V2 / G1 / C1 rerun admissibility under M0 post-null
  cooldown): unresolved; out of Phase 4ap scope.
- The Phase 4ap-specific empirical questions (Q1–Q14 of §8) remain
  unanswered until a separately authorized computation phase.

### 21.5 What does it mean for strategy research?

It means that any future V1-arc-only forensic phase has a complete,
predeclared, docs-only plan to follow. No strategy research is
unblocked by Phase 4ap. The M0 cooled-down families list is unchanged.

### 21.6 What does it mean for governance?

It means the V1-arc forensic plan is now on the project record at the
documentation level. Any successor computation phase has a single plan
to follow (this memo) with reference to a single methodology framework
(Phase 4ao) and a single inventory baseline (Phase 4an). All upstream
governance (Phase 4ak M0; Phase 4al refined no-rescue rule; Phase 3v §8;
Phase 3t 5m closure; §11.6; §1.7.3) is preserved verbatim.

### 21.7 What is the clean next step?

Remain paused. The plan is on record; no successor phase is
authorized; the operator may later authorize a future docs-and-code
V1-arc-only computation phase exactly under this plan, or one of the
narrower docs-only tertiary refinement memos, or none of these.

### 21.8 What should we not do yet?

Do not start any forensic computation. Do not rerun any strategy
script. Do not run an offline 15m-join. Do not modify any strategy or
backtest code. Do not acquire 5m / 1m / aggTrades / tick / mark-price
30m / 4h data. Do not reopen the 5m research thread. Do not propose a
new strategy. Do not optimize R3 or any other V1-arc candidate. Do not
authorize Phase 4aq / Phase 5 / Phase 4 canonical / paper / shadow /
live / exchange-write / production keys / authenticated APIs / private
endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` /
credentials. Do not modify the M0 governance document. Do not modify
any retained verdict. Do not modify any project lock.

## 22. Explicit Preservation of Verdicts, Locks, and No-Rescue Constraints

**Retained verdicts (preserved verbatim):**

- H0 remains FRAMEWORK ANCHOR.
- R3 remains BASELINE-OF-RECORD.
- R1a remains RETAINED — NON-LEADING.
- R1b-narrow remains RETAINED — NON-LEADING.
- R2 remains FAILED — §11.6 cost-sensitivity blocks.
- F1 remains HARD REJECT.
- D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other.
- 5m research thread remains operationally CLOSED per Phase 3t.
- V2 remains HARD REJECT — terminal for V2 first-spec.
- G1 remains HARD REJECT — terminal for G1 first-spec.
- C1 remains HARD REJECT — terminal for C1 first-spec.

**Project locks (preserved verbatim):**

- M0 governance remains binding prospectively only.
- No retained verdict is revised.
- No project lock is changed.
- §11.6 HIGH cost remains preserved (8 bps slippage per side; round-trip
  = 16 bps; taker fee = 4 bps per side; no maker rebates; no live fee
  assumption). Any future fee / slippage / funding decomposition may be
  reported descriptively only and must not change the locked project-
  level cost reference or revise historical results.
- §1.7.3 project-level locks remain:
  - 0.25% risk per trade;
  - 2× leverage cap;
  - one position max;
  - mark-price stops where applicable.
- Phase 3r §8 mark-price gap governance preserved.
- Phase 3v §8 stop-trigger-domain governance preserved.
- Phase 3w §6 / §7 / §8 break-even / EMA-slope / stagnation governance
  preserved.
- Phase 4j §11 metrics OI-subset partial-eligibility rule preserved
  (not used by V1-arc plan).
- Phase 4k V2 backtest-plan methodology preserved.
- Phase 4p G1 strategy-spec memo preserved.
- Phase 4q G1 backtest-plan methodology preserved.
- Phase 4v C1 strategy-spec memo preserved.
- Phase 4w C1 backtest-plan methodology preserved.
- Phase 4ak twelve-clause M0 mechanism-admissibility gate preserved.
- Phase 4ak post-null cooldown rule preserved.
- Phase 4ak cooled-down families list preserved.
- Phase 4al refined no-rescue rule preserved.
- Phase 4al §13 boundary specification preserved.
- Phase 4al §14 data-resolution hierarchy preserved.
- Phase 4am §11.A audit findings (F-1 / F-2 / F-3 / F-4) preserved.
- Phase 4an inventory result preserved.
- Phase 4ao harmonization result preserved.

**No-rescue constraints (preserved verbatim):**

- No R3-prime / R1a-prime / R1b-narrow-prime / R2-prime / F1-prime /
  D1-A-prime / D1-B / V2-prime / V2-narrow / V2-relaxed / V2 hybrid /
  G1-prime / G1-narrow / G1-extension / G1 hybrid / C1-prime /
  C1-narrow / C1-extension / C1 hybrid / V1-D1 / F1-D1 / any
  cross-strategy hybrid.
- No conversion of Phase 4ap plan / forensic-question lists into
  strategy candidates.
- No conversion of Phase 4ap forbidden-rescue-risk classifications into
  parameter-tuning input.
- No reopening of the 5m research thread.
- No M0-governance amendment derived from Phase 4ap reasoning.
- No verdict revision.
- No project-lock revision.

Phase 4 (canonical) remains unauthorized.

Phase 4aq / Phase 5 / any successor phase remains unauthorized.

Paper / shadow, live-readiness, deployment, production keys, authenticated
APIs, private endpoints, public-endpoint calls in code, user stream,
WebSocket, MCP, Graphify, `.mcp.json`, credentials, exchange-write, and
5m / 1m / aggTrades / tick / mark-price 30m / 4h data acquisition all
remain unauthorized.

**Recommended state remains paused.**

**No next phase authorized.**
