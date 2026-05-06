# Phase 4ap Closeout — V1-Arc Exit-Path Forensic Plan

## 1. Phase Identity

- Name: Phase 4ap — V1-Arc Exit-Path Forensic Plan.
- Type: docs-only forensic plan / predeclared methodology / closeout.
- Date: 2026-05-06.
- Phase memo:
  `docs/00-meta/implementation-reports/2026-05-06_phase-4ap_v1-arc-exit-path-forensic-plan.md`.

## 2. Branch

- Phase branch: `phase-4ap/v1-arc-exit-path-forensic-plan`.
- Forked from: clean main at `6c59c5ba6590d2017f873523ceab45c3e5a0139f`
  (the live Phase 4ao merge tip on main / origin/main).

## 3. Base SHA

- Pre-Phase-4ap main / origin/main:
  `6c59c5ba6590d2017f873523ceab45c3e5a0139f`.
- Note: the Phase 4ao merge-closeout file at
  `docs/00-meta/implementation-reports/2026-05-06_phase-4ao_merge-closeout.md`
  records pre-amend SHA `e0c280d` and post-first-amend SHA `eeb6962`
  per the documented git self-reference artifact (every amend produces
  a new SHA). Both `e0c280d` and `eeb6962` are intermediate amend
  artefacts no longer in any branch's live history; only `6c59c5b` is
  the live merge tip on main.

## 4. Phase Commit SHAs

- Phase 4ap memo + current-project-state commit:
  `bf9b8e62d4e9ae97b9d5519a3f369654e7eb0b6e`
  ("docs(phase-4ap): plan v1-arc exit-path forensics").
- Phase 4ap closeout commit: recorded after this file is staged and
  committed.

## 5. Purpose

Phase 4ap is a docs-only forensic plan / predeclared methodology phase
that defines the exact V1-arc-only computation specification any future
exit-path forensic phase must follow before computation. It is derived
from Phase 4an (inventory baseline) and Phase 4ao (methodology /
artefact harmonization), and inherits the Phase 4al refined no-rescue
rule, the Phase 4al §13 future-Phase-4am-style boundary specification,
the Phase 4al §14 data-resolution hierarchy, the Phase 4am §11.A audit
findings, and the Phase 4ak twelve-clause M0 gate + post-null cooldown
rule + cooled-down families list.

This closeout file is the Phase 4ap closeout per the operator phase-
branch convention. Its purpose is to:

- close out Phase 4ap on the phase branch before any future no-fast-
  forward merge to main;
- record the V1-arc forensic plan result in summary form for
  repository-level governance review;
- preserve the retained verdict ledger and every project lock
  verbatim;
- confirm that Phase 4ap did not modify source / tests / scripts /
  data / manifests / strategy specs / governance docs / retained
  verdicts / project locks / successor authorization;
- confirm that Phase 4ap does not authorize Phase 4aq or any other
  successor phase;
- and produce the closeout artefact required by the operator
  convention for every phase branch prior to merge.

Phase 4ap does NOT and is NOT authorized to: compute MFE / MAE /
realized-R / time-to-event / cost-decomposition distributions or any
forensic statistic; perform exit-path forensics; run any backtest;
execute any historical strategy or research script; run an offline
15m-join MFE/MAE reconstruction; acquire any data; modify any data
file, manifest, source file, test, or script; modify any retained
verdict, project lock, or M0 governance text; amend Phase 3t 5m
closure or Phase 3v §8 stop-trigger-domain governance; propose a new
strategy or exit system; optimize R3 or any other V1-arc candidate;
create R3-prime / R2-prime / R1a-prime / R1b-narrow-prime / any
successor candidate; rescue any rejected or retained-evidence
candidate; authorize any successor phase.

## 6. Plan Result

The Phase 4ap plan defines the following V1-arc-only forensic
computation specification:

### 6.1 Population scope

- **INCLUDED**: H0 (framework anchor context); R3
  (BASELINE-OF-RECORD DESCRIPTIVE CONTEXT ONLY — no optimization,
  R3-prime, R3 rescue, or baseline-of-record revision; R3 forensic
  findings cannot be converted into strategy parameters / thresholds /
  entry / exit logic / new candidates); R1a (RETAINED — NON-LEADING
  descriptive context only); R1b-narrow (RETAINED — NON-LEADING
  descriptive context only); R2 (FAILED — §11.6 cost-fragility
  descriptive context only).
- **EXCLUDED**: F1, D1-A (require Route B reconstruction; not in
  V1-arc first-pass); V2, G1, C1 (rerun governance-risk-unresolved
  under M0 post-null cooldown; defer to OQ-B-resolution memo); 5m
  research thread (CLOSED per Phase 3t; not reopened).

### 6.2 Predeclared forensic questions (Q1–Q14)

- Q1–Q3 distributional (MFE_R / MAE_R / realized net_R distributions
  by population × symbol × side × exit reason × cost cell);
- Q4–Q5 relationship (MFE_R-vs-net_R; MAE_R-vs-net_R);
- Q6–Q7 threshold-touch (fraction reaching +1R / +2R / +3R; favorable-
  before-stop fraction);
- Q8–Q10 path-anatomy (giveback-from-MFE; adverse-before-favorable;
  favorable-before-stop);
- Q11–Q12 cost-decomposition (cost / fee / slippage / funding-in-R per
  population × cost cell; R2 cost-fragility descriptive without §11.6
  revision);
- Q13 cross-population descriptive comparison (no ranking for
  promotion; baseline-of-record preserved);
- Q14 bar-resolution ambiguity reporting per Phase 4al §14.C bands.

### 6.3 Forbidden questions (F1–F10)

- F1: which exit rule would make R3 profitable?
- F2: which TP / SL should replace R3?
- F3: what is the best take-profit multiple?
- F4: what parameters should we tune?
- F5: can R2 be rescued if costs are lower?
- F6: can R1a / R1b-narrow become leading?
- F7: can H0 / R3 be turned into R3-prime?
- F8: can V1-arc be hybridized with F1 / D1-A / V2 / G1 / C1?
- F9: can 5m signals improve exits?
- F10: any question converting descriptive forensics into strategy
  design / optimization / verdict revision / lock revision / baseline
  revision / framework-anchor revision / successor-candidate creation.

### 6.4 Artefact source

Existing local `trade_log_v1` JSON / Parquet under
`data/derived/backtests/phase-2*` (gitignored, locally present) plus
per-cost-cell variants and trade-price stop-domain variants where
present. Per-population lineage:

- H0: `phase-2e-baseline` + `phase-2g-wave1-h0-r`.
- R3: `phase-2l-r3-r` + `-slip=LOW` / `-slip=HIGH` /
  `-stop=TRADE_PRICE` + `phase-2l-r3-v` validation variant.
- R1a: `phase-2m-r1a-r1a_plus_r3-r` + variants.
- R1b-narrow: `phase-2s-r1b-r1b_narrow-r` + variants.
- R2: `phase-2w-r2-r2_r3-r` + `-slip=LOW` / `-slip=HIGH` /
  `-stop=TRADE_PRICE` / `-fill=limit-at-pullback` +
  `phase-2w-r2-r2_r3-v` validation variant.

No artefact, manifest, source, test, or script is modified by Phase
4ap or any successor V1-arc-only computation phase.

### 6.5 Field schema

25 required fields drawn from `trade_log_v1`: trade_id; population /
candidate_id (inferred from artefact source path); symbol; side /
direction; entry_fill_time_ms; exit_fill_time_ms; entry_fill_price;
exit_fill_price; initial_stop; stop_distance; realized_risk_usdt;
gross_pnl; net_pnl; net_r_multiple; entry_fee; exit_fee; funding_pnl;
fee_rate_assumption; slippage_bucket; exit_reason; bars_in_trade;
mfe_r; mae_r; stop_was_gap_through; stop_trigger_domain. Plus the
timeframe / data-resolution label fixed at `15m`.

### 6.6 Metric definitions

14 forensic metrics (MFE_R; MAE_R; net_R; gross_R; cost-in-R;
fee-in-R; slippage-in-R; funding-in-R; reached_+1R / +2R / +3R flags;
MFE capture ratio; giveback-from-MFE; adverse-before-favorable flag —
RECONSTRUCTABLE_ONLY_WITH_RERUN under existing schema; bar-resolution
ambiguity flag) referencing Phase 4ao §6 / §8 verbatim.

### 6.7 Timeframe / data-resolution rule

15m bar-extreme only for first-pass. 5m / 1m / aggTrades / tick /
mark-price 30m / 4h all unauthorized by Phase 4ap. 5m optional
measurement-layer escalation only under Phase 4al §14.C >10% / >20%
ambiguity bands and Phase 4ao §13.3 conservative criterion, and only
under separate authorization.

### 6.8 Cost / realized-R rule

§11.6 LOCK preserved (8 bps slippage per side; round-trip = 16 bps).
Cost-cell descriptive comparisons cannot justify §11.6 relaxation.
R2 cost-fragility = retained failed evidence, not rescue. V1-arc-only
scope avoids the cross-population fee-assumption disclaim because all
included populations share the V1-arc engine path with uniform 5 bps /
side fee assumption.

### 6.9 Stop-trigger-domain rule

`trade_price_backtest` only for V1-arc first-pass. `mixed_or_unknown`
invalid / fail-closed. `mark_price_runtime` is runtime / live only
(not engaged by Phase 4ap). `mark_price_backtest_candidate` not
authorized by Phase 4ap. No mark-price path forensics.

### 6.10 Output specification

9 planned output artefacts:

1. population_summary.csv;
2. mfe_mae_distribution_by_population.csv;
3. realized_r_by_population.csv;
4. cost_in_r_by_population.csv;
5. exit_reason_breakdown.csv;
6. excursion_threshold_touch_rates.csv;
7. ambiguity_report.csv;
8. forbidden_interpretation_checklist.md;
9. v1_arc_forensic_report.md.

NOT created by Phase 4ap.

### 6.11 Stop conditions

11 fail-closed conditions for any future computation phase:

- SC-1: missing artefact path;
- SC-2: missing required field;
- SC-3: mixed_or_unknown stop-trigger-domain;
- SC-4: schema mismatch;
- SC-5: attempt to include excluded populations;
- SC-6: attempt to use 5m / 1m / aggTrades / tick / mark-price without
  separate authorization;
- SC-7: attempt to rank V1-arc populations for promotion;
- SC-8: attempt to propose parameter changes;
- SC-9: attempt to revise verdict / lock;
- SC-10: result requiring strategy interpretation rather than
  descriptive reporting;
- SC-11: quality-gate failure (ruff / pytest / mypy violation
  introduced by future computation phase's code).

## 7. Files Added / Modified (Phase 4ap, including this closeout)

Added by Phase 4ap memo + current-project-state commit `bf9b8e6`:

- `docs/00-meta/implementation-reports/2026-05-06_phase-4ap_v1-arc-exit-path-forensic-plan.md`
  (1260 lines added).

Modified by the same commit:

- `docs/00-meta/current-project-state.md`
  (193 lines added — Phase 4ap narrative paragraph + new "Current
  phase:" block, with the prior Phase 4ao block preserved as
  historical context).

Added by Phase 4ap closeout commit (this file):

- `docs/00-meta/implementation-reports/2026-05-06_phase-4ap_closeout.md`.

## 8. Files Not Modified

Phase 4ap did NOT modify:

- any source file under `src/prometheus/`;
- any test under `tests/`;
- any script under `scripts/`;
- any data file under `data/raw/`, `data/normalized/`,
  `data/derived/`, or `data/research/`;
- any manifest under `data/manifests/`;
- any strategy specification under `docs/03-strategy-research/`;
- any validation document under `docs/05-backtesting-validation/`;
- any roadmap document under `docs/12-roadmap/` (phase-gates,
  technical-debt-register);
- any governance document under `docs/00-meta/`
  (`m0-mechanism-admissibility-gate.md`, `ai-coding-handoff.md`,
  `implementation-ambiguity-log.md`);
- any retained verdict (H0, R3, R1a, R1b-narrow, R2, F1, D1-A, V2,
  G1, C1, 5m thread);
- any project lock (§11.6, §1.7.3, Phase 3r §8, Phase 3v §8,
  Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q,
  Phase 4v, Phase 4w);
- any M0 governance text (Phase 4ak twelve-clause M0 gate, post-null
  cooldown rule, cooled-down families list);
- any successor authorization.

## 9. Docs-Only Confirmation

Phase 4ap is **docs-only**. The phase modifies only Markdown files
under `docs/00-meta/`. No code, tests, scripts, data, manifests,
strategy specs, validation thresholds, or governance documents are
modified by Phase 4ap.

The Phase 4ap closeout (this file) is also docs-only and modifies
only this Markdown file under `docs/00-meta/implementation-reports/`.

## 10. Verification Commands and Outputs

Verification commands run on branch
`phase-4ap/v1-arc-exit-path-forensic-plan` immediately prior to
staging and committing this closeout file:

```text
git status                   : clean working tree (untracked
                                .claude/scheduled_tasks.lock and
                                data/research/ are gitignored /
                                transient)
git branch --show-current    : phase-4ap/v1-arc-exit-path-forensic-plan
git rev-parse main           : 6c59c5ba6590d2017f873523ceab45c3e5a0139f
git rev-parse origin/main    : 6c59c5ba6590d2017f873523ceab45c3e5a0139f
git rev-parse HEAD           : bf9b8e62d4e9ae97b9d5519a3f369654e7eb0b6e
git log --oneline -8         :
                                bf9b8e6 docs(phase-4ap): plan v1-arc exit-path forensics
                                6c59c5b docs(phase-4ao): merge exit-path methodology harmonization
                                c2d7d83 docs(phase-4ao): add closeout
                                6ace04f docs(phase-4ao): harmonize exit-path methodology
                                a73c00b docs(phase-4an): merge historical exit-path inventory
                                13f519b docs(phase-4an): add closeout
                                241d6a7 docs(phase-4an): inventory historical exit-path artefacts
                                dfaa26a docs(phase-4am): merge merge-closeout
git diff --check (pre-each-commit) : clean (no whitespace errors)
git diff --cached --stat (pre-memo): docs/00-meta/current-project-state.md +193;
                                       phase-4ap memo +1260 (2 files; 1453 insertions)
```

After this closeout file is staged and committed, additional
verification commands will be run:

```text
git diff --cached --stat (pre-closeout) : (this file +N lines)
git diff --check                        : clean
git rev-parse HEAD (post-closeout)      : (the new closeout commit
                                           SHA)
git log --oneline -8 (post-closeout)    : (closeout on top of bf9b8e6)
```

`ruff` / `pytest` / `mypy` are NOT run because Phase 4ap is docs-only
with zero code, test, or script changes — repo convention does not
require quality gates for docs-only phases (consistent with Phase
4al, Phase 4am, Phase 4an, Phase 4ao).

## 11. Implementation / Governance Review

### 11.1 What changed?

Phase 4ap added one new file
(`docs/00-meta/implementation-reports/2026-05-06_phase-4ap_v1-arc-exit-path-forensic-plan.md`,
1260 lines) and modified one existing file
(`docs/00-meta/current-project-state.md`, 193 lines added). The Phase
4ap closeout commit additionally adds this file
(`docs/00-meta/implementation-reports/2026-05-06_phase-4ap_closeout.md`).

### 11.2 What did not change?

- `docs/00-meta/m0-mechanism-admissibility-gate.md`: unchanged.
- All twelve M0 clauses M0.1–M0.12: unchanged.
- The post-null cooldown rule: unchanged.
- The cooled-down families list: unchanged.
- All retained verdicts: unchanged.
- All project locks: unchanged.
- All scripts under `scripts/`: unchanged.
- All source files under `src/prometheus/`: unchanged.
- All tests: unchanged.
- All data files: unchanged.
- All manifests: unchanged.
- `docs/12-roadmap/phase-gates.md`,
  `docs/12-roadmap/technical-debt-register.md`,
  `docs/00-meta/ai-coding-handoff.md`,
  `docs/00-meta/implementation-ambiguity-log.md`: unchanged.

### 11.3 Were any locks, verdicts, or safety boundaries affected?

No.

### 11.4 Were any scripts, source files, data, manifests, or tests modified?

No.

### 11.5 Is the phase mergeable as docs-only?

Yes. Phase 4ap is mergeable as docs-only. The only files added or
modified are the new memo, the new closeout (this file), and the
narrow paragraph addition + "Current phase:" block update on
`docs/00-meta/current-project-state.md`. Per operator brief, this
prompt does NOT merge Phase 4ap to main; the merge is operator-driven
in a future prompt.

## 12. Research Interpretation Review

### 12.1 What did this phase prove?

Phase 4ap proved, by static repository inspection only, that:

- A complete V1-arc-only forensic computation specification can be
  authored as a docs-only plan, predeclaring the population scope
  (H0 / R3 / R1a / R1b-narrow / R2), the artefact source, the 25-field
  schema, the 14 forensic metrics, the 14 forensic questions, the 10
  forbidden questions, the 9 output artefacts, the 11 stop conditions,
  the 18-heading minimum predeclared-methodology template inheritance
  from Phase 4ao §14, and the verdict / lock preservation contract —
  without revising any retained verdict, project lock, governance
  text, source code, test, script, data file, or manifest.
- R3 inclusion is governance-bounded as descriptive context only; R3
  optimization, R3-prime, R3 rescue, and baseline-of-record revision
  are explicitly forbidden.
- F1 / D1-A / V2 / G1 / C1 / 5m thread are excluded from V1-arc-only
  first-pass; their inclusion would require separately authorized
  Route B reconstruction (F1 / D1-A) or OQ-B resolution memo (V2 /
  G1 / C1) or are permanently CLOSED_CONTEXT_ONLY (5m thread).
- §11.6 LOCK is preserved verbatim; cost-cell descriptive comparisons
  are research evidence about cost sensitivity, never license for
  §11.6 relaxation.
- Stop-trigger-domain governance and 5m closure remain binding.

### 12.2 What did this phase not prove?

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

### 12.3 Which original questions did it answer?

- The Phase 4ao §16.2 sample population eligibility under the §14
  template: V1-arc-only first-pass scope confirmed.
- The Phase 4ao OQ-D template specification: 18 required headings
  inherited verbatim plus Phase 4ap-specific section headings (§§6–17)
  layered on top.
- The Phase 4ap operator-brief preconditions for any future V1-arc
  computation: §6–§17 collectively answer them.

### 12.4 Which original questions remain open?

- **OQ-A** (offline 15m-join MFE / MAE recovery sufficiency for F1 /
  D1-A): unresolved; out of Phase 4ap scope (V1-arc-only first-pass
  excludes F1 / D1-A).
- **OQ-B** (V2 / G1 / C1 rerun admissibility under M0 post-null
  cooldown): unresolved; out of Phase 4ap scope.
- The Phase 4ap-specific empirical questions (Q1–Q14 of memo §8)
  remain unanswered until a separately authorized computation phase.

### 12.5 What does it mean for strategy research?

It means that any future V1-arc-only forensic phase has a complete,
predeclared, docs-only plan to follow. No strategy research is
unblocked by Phase 4ap. The M0 cooled-down families list is
unchanged.

### 12.6 What does it mean for governance?

It means the V1-arc forensic plan is now on the project record at
the documentation level. Any successor computation phase has a
single plan to follow (this memo) with reference to a single
methodology framework (Phase 4ao) and a single inventory baseline
(Phase 4an). All upstream governance is preserved verbatim.

### 12.7 What is the clean next step?

Remain paused. The plan is on record; no successor phase is
authorized.

### 12.8 What should we not do yet?

Do not start any forensic computation. Do not rerun any strategy
script. Do not run an offline 15m-join. Do not modify any strategy
or backtest code. Do not acquire 5m / 1m / aggTrades / tick / mark-
price 30m / 4h data. Do not reopen the 5m research thread. Do not
propose a new strategy. Do not optimize R3 or any other V1-arc
candidate. Do not authorize Phase 4aq / Phase 5 / Phase 4 canonical /
paper / shadow / live / exchange-write / production keys /
authenticated APIs / private endpoints / user stream / WebSocket /
MCP / Graphify / `.mcp.json` / credentials. Do not modify the M0
governance document. Do not modify any retained verdict. Do not
modify any project lock.

## 13. Preserved Verdicts and Locks

### 13.1 Retained verdicts (preserved verbatim)

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

### 13.2 Project locks (preserved verbatim)

- M0 governance remains binding prospectively only.
- No retained verdict is revised.
- No project lock is changed.
- §11.6 HIGH cost remains preserved (8 bps slippage per side; round-
  trip = 16 bps). Any future fee / slippage / funding decomposition
  may be reported descriptively only and must not change the locked
  project-level cost reference or revise historical results.
- §1.7.3 project-level locks remain:
  - 0.25% risk per trade;
  - 2× leverage cap;
  - one position max;
  - mark-price stops where applicable.
- Phase 3r §8 mark-price gap governance preserved.
- Phase 3v §8 stop-trigger-domain governance preserved.
- Phase 3w §6 / §7 / §8 break-even / EMA-slope / stagnation
  governance preserved.
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

### 13.3 No-rescue constraints (preserved verbatim)

- No R3-prime / R1a-prime / R1b-narrow-prime / R2-prime / F1-prime /
  D1-A-prime / D1-B / V2-prime / V2-narrow / V2-relaxed / V2 hybrid /
  G1-prime / G1-narrow / G1-extension / G1 hybrid / C1-prime /
  C1-narrow / C1-extension / C1 hybrid / V1-D1 / F1-D1 / any
  cross-strategy hybrid.
- No conversion of Phase 4ap plan / forensic-question lists into
  strategy candidates.
- No conversion of Phase 4ap forbidden-rescue-risk classifications
  into parameter-tuning input.
- No reopening of the 5m research thread.
- No M0-governance amendment derived from Phase 4ap reasoning.
- No verdict revision.
- No project-lock revision.

## 14. Recommendation

- **Primary**: remain paused. The Phase 4ap plan is on record; no
  computation is required to proceed; no successor phase is
  authorized.
- **Conditional secondary (NOT authorized by Phase 4ap)**: future
  docs-and-code V1-arc-only computation phase exactly under this
  plan, satisfying Phase 4ao §14 18-heading template + Phase 4al §13
  boundary + Phase 4ap §6–§17. Operator-driven authorization required.
- **Conditional tertiary (NOT authorized by Phase 4ap)**: narrower
  future docs-only refinement memos: Phase 4ao §14 template re-
  validation memo; OQ-B-resolution memo; F1 / D1-A Route B
  reconstruction methodology memo. Each independent. Combining
  secondary with any tertiary in a single successor phase NOT
  recommended.
- **Forbidden**: paper / shadow / live / exchange-write / production
  keys / authenticated APIs / private endpoints / user stream /
  WebSocket / MCP / Graphify / `.mcp.json` / credentials; any
  strategy resurrection; any verdict revision; any project-lock
  revision; any M0-governance amendment derived from Phase 4ap
  reasoning; reopening the 5m research thread; acquisition of 5m /
  1m / aggTrades / tick / mark-price 30m / 4h data without separately
  authorized data-requirements memo.

**Phase 4ap does not authorize any successor phase.** **Phase 4ap
does not authorize computation.**

## 15. Final Status

- Phase 4ap is complete on the phase branch
  `phase-4ap/v1-arc-exit-path-forensic-plan`.
- Phase 4ap is docs-only.
- Phase 4ap memo + current-project-state commit on the phase branch:
  `bf9b8e62d4e9ae97b9d5519a3f369654e7eb0b6e`.
- Phase 4ap closeout commit on the phase branch: recorded after this
  file is staged and committed.
- Phase 4ap is ready for no-fast-forward merge to main after the
  closeout commit lands on the phase branch (operator-driven; not
  performed in this prompt).
- The merge-closeout file
  `docs/00-meta/implementation-reports/2026-05-06_phase-4ap_merge-closeout.md`
  will be created during the no-fast-forward merge per operator
  convention if and when the operator authorizes the merge.
- **No successor phase is authorized.**
- **Phase 4aq / Phase 5 / Phase 4 canonical / any successor phase
  remains unauthorized.**
- **Paper / shadow, live-readiness, deployment, production keys,
  authenticated APIs, private endpoints, public-endpoint calls in
  code, user stream, WebSocket, MCP, Graphify, `.mcp.json`,
  credentials, exchange-write, and 5m / 1m / aggTrades / tick /
  mark-price 30m / 4h data acquisition all remain unauthorized.**
- **Recommended state remains paused** unless the operator separately
  authorizes a future phase.
