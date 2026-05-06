# Phase 4ap Merge Closeout — V1-Arc Exit-Path Forensic Plan

## Purpose

This document records the no-fast-forward merge of completed Phase 4ap
into `main`.

This is a docs-only merge closeout. It does not authorize Phase 4aq or
any successor phase. It does not authorize forensic computation,
MFE / MAE computation, realized-R distributions, offline 15m joins,
rerun, backtest, script execution, data acquisition, manifest update,
source / test / script / data changes, strategy proposal, strategy
rescue, R3 optimization, R3-prime / R2-prime / R1a-prime /
R1b-narrow-prime / any successor strategy candidate, 5m thread
reopening, 5m / 1m / aggTrades / tick / mark-price 30m / 4h data
acquisition, paper / shadow, live-readiness, deployment, production
keys, authenticated APIs, private endpoints, public-endpoint calls in
code, user stream, WebSocket, exchange-write, MCP, Graphify,
`.mcp.json`, or credentials.

## Merge Summary

- Phase 4ap title: V1-Arc Exit-Path Forensic Plan
- Merge branch: `phase-4ap/v1-arc-exit-path-forensic-plan`
- Target branch: `main`
- Main before merge: `6c59c5ba6590d2017f873523ceab45c3e5a0139f`
- Phase 4ap memo + current-project-state commit:
  `bf9b8e62d4e9ae97b9d5519a3f369654e7eb0b6e`
- Phase 4ap closeout commit:
  `bc7353fdb771157a6ad0706c7d1b82daad22745f`
- Merge method: `--no-ff`
- Merge commit SHA recorded before final self-reference amend: `d306e5264a264b9cc5c35d41d59052c631dd464b`
- Final live main SHA after self-reference amend: `0a9d68d40d6aaa1f84e01f71f9459ad0d51b0abb`
- Self-reference limitation: a git commit cannot contain its own SHA;
  every `git commit --amend --no-edit` produces a new SHA. The two SHAs
  above are intermediate amend artefacts that document the merge-commit
  evolution. After the final self-reference amend that incorporated the
  `0a9d68d...` line into this file, the live main HEAD on origin/main
  is one further SHA beyond `0a9d68d...`. That live main HEAD SHA is
  reported in the operator chat report rather than recorded in this
  merge-closeout file, because per operator convention this file does
  not amend indefinitely. The `0a9d68d...` SHA is the closest stable
  self-reference: it was the live main HEAD at the moment this line
  was written, and remains a valid traceable reference into the
  reflog / amend chain even after the final amend is performed.
  This convention matches Phase 4ao merge-closeout's accepted
  self-reference handling.

Note on the recorded merge commit SHA: due to the documented git self-
reference artifact (every amend changes the SHA, and a commit cannot
contain its own SHA), the recorded SHA may be one amend cycle behind
the live HEAD on main after the final amend. If self-reference cannot
be made stable, both pre-amend and post-amend SHAs are recorded
explicitly in this section for traceability, consistent with the
Phase 4am / Phase 4an / Phase 4ao merge-closeout convention.

## Files Brought Forward From Phase 4ap

Phase 4ap was docs-only.

Phase 4ap created:

- `docs/00-meta/implementation-reports/2026-05-06_phase-4ap_v1-arc-exit-path-forensic-plan.md`
- `docs/00-meta/implementation-reports/2026-05-06_phase-4ap_closeout.md`

This merge closeout created:

- `docs/00-meta/implementation-reports/2026-05-06_phase-4ap_merge-closeout.md`

This merge also updated narrowly:

- `docs/00-meta/current-project-state.md`

(The `current-project-state.md` update was performed in the Phase 4ap
memo commit `bf9b8e6` on the phase branch and is brought forward by
this merge; the merge-closeout commit itself does not further modify
`current-project-state.md`.)

## Phase 4ap Summary

Phase 4ap was docs-only forensic planning / predeclared methodology.
It defined the exact V1-arc-only computation specification any future
exit-path forensic phase would need to follow before computation. It
did not compute MFE / MAE, did not compute realized-R distributions,
did not perform exit-path forensics, did not run any backtest or
strategy / data-acquisition script, did not run an offline 15m-join
MFE / MAE reconstruction, did not acquire data, did not modify any
data file, manifest, source file, test, or script, did not modify
any retained verdict, project lock, or M0 governance text, did not
amend Phase 3t 5m closure or Phase 3v §8 stop-trigger-domain
governance, did not propose a new strategy or exit system, did not
optimize R3 or any other V1-arc candidate, did not create R3-prime /
R2-prime / R1a-prime / R1b-narrow-prime / any successor candidate,
and did not authorize any successor phase.

Phase 4ap is derived from Phase 4an (inventory baseline) + Phase 4ao
(methodology / artefact harmonization) + Phase 4al (refined no-rescue
rule + §13 boundary + §14 data-resolution hierarchy) + Phase 4am
(§11.A audit findings) + Phase 4ak (twelve-clause M0 gate + post-null
cooldown rule + cooled-down families list).

## Plan Result

The Phase 4ap plan defines the following V1-arc-only forensic
computation specification (headline rules):

- **Population scope**: V1-arc only — H0 (framework anchor context);
  R3 (BASELINE-OF-RECORD descriptive context only — no optimization,
  R3-prime, R3 rescue, or baseline-of-record revision; R3 forensic
  findings cannot be converted into strategy parameters / thresholds /
  entry / exit logic / new candidates); R1a (RETAINED — NON-LEADING
  descriptive context only); R1b-narrow (RETAINED — NON-LEADING
  descriptive context only); R2 (FAILED — §11.6 cost-fragility
  descriptive context only).

- **Excluded populations**: F1, D1-A (require Route B reconstruction;
  not in V1-arc first-pass); V2, G1, C1 (rerun governance-risk-
  unresolved under M0 post-null cooldown; defer to OQ-B-resolution
  memo); 5m research thread (CLOSED per Phase 3t; not reopened).

- **First-pass data-resolution**: 15m existing V1-arc artefacts only.
  5m, 1m, aggTrades, tick, and mark-price 30m / 4h are unauthorized.
  5m may be proposed only as a later measurement-layer escalation
  under Phase 4al §14.C >10% / >20% ambiguity bands and Phase 4ao
  §13.3 conservative criterion, and only under separate authorization.

- **Planned future metrics (descriptive only)**: MFE_R, MAE_R, net_R,
  gross_R, cost-in-R, fee-in-R, slippage-in-R, funding-in-R,
  reached_+1R / +2R / +3R touch flags, MFE capture ratio,
  giveback-from-MFE, adverse-before-favorable flag, favorable-
  before-stop flag, and bar-resolution ambiguity flag. All metrics
  reference Phase 4ao §6 / §8 verbatim.

- **Future output artefacts (planned only; NOT created by Phase
  4ap)**: 9 artefacts — population_summary.csv;
  mfe_mae_distribution_by_population.csv;
  realized_r_by_population.csv; cost_in_r_by_population.csv;
  exit_reason_breakdown.csv; excursion_threshold_touch_rates.csv;
  ambiguity_report.csv; forbidden_interpretation_checklist.md;
  v1_arc_forensic_report.md.

- **11 fail-closed stop conditions for any future computation**:
  missing artefact path; missing required field;
  mixed_or_unknown stop-trigger-domain; schema mismatch; attempt to
  include excluded populations; attempt to use 5m / 1m / tick /
  mark-price without separate authorization; attempt to rank V1-arc
  populations for promotion; attempt to propose parameter changes;
  attempt to revise verdict / lock; result requiring strategy
  interpretation rather than descriptive reporting; quality-gate
  failure (ruff / pytest / mypy violation).

- **10 forbidden question forms that any future computation phase
  must reject**: which exit rule would make R3 profitable; which
  TP / SL should replace R3; what is the best take-profit multiple;
  what parameters should we tune; can R2 be rescued if costs are
  lower; can R1a / R1b-narrow become leading; can H0 / R3 be turned
  into R3-prime; can V1-arc be hybridized with F1 / D1-A / V2 / G1 /
  C1; can 5m signals improve exits; any question converting
  descriptive forensics into strategy design / optimization / verdict
  revision / lock revision / baseline revision / framework-anchor
  revision / successor-candidate creation.

The 25-field schema, 14 forensic metrics (Q1–Q14 forensic question
set), and 18-heading minimum predeclared-methodology template
inheritance from Phase 4ao §14 are recorded in detail in the
Phase 4ap main memo (sections §6–§17). This merge brings all of
that forward verbatim.

## Governance Status After Merge

- **M0 mechanism-admissibility gate** (Phase 4ak twelve-clause M0
  governance): unchanged.
- **M0 post-null cooldown rule**: unchanged.
- **M0 cooled-down families list**: unchanged.
- **Phase 4al refined no-rescue rule**: preserved.
- **Phase 4al §13 future-Phase-4am-style boundary specification**:
  preserved.
- **Phase 4al §14 data-resolution hierarchy**: preserved.
- **Phase 4am §11.A audit findings (F-1 / F-2 / F-3 / F-4)**:
  preserved as documentation for future methodology-harmonization
  scoping.
- **Phase 4an inventory result**: preserved.
- **Phase 4ao harmonization result**: preserved.
- **Phase 4ap forensic plan**: recorded in repository as docs-only
  forensic-plan evidence.
- **Phase 3t 5m closure**: preserved.
- **Phase 3v §8 stop-trigger-domain governance**: preserved.
- **Phase 3r §8 mark-price gap governance**: preserved.
- **Phase 3w §6 / §7 / §8 break-even / EMA-slope / stagnation
  governance**: preserved.
- **Phase 4j §11 metrics OI-subset partial-eligibility rule**:
  preserved.
- **Phase 4k V2 backtest-plan methodology**: preserved.
- **Phase 4p G1 strategy-spec memo**: preserved.
- **Phase 4q G1 backtest-plan methodology**: preserved.
- **Phase 4v C1 strategy-spec memo**: preserved.
- **Phase 4w C1 backtest-plan methodology**: preserved.
- **§11.6 HIGH cost = 8 bps per side**: preserved.
- **§1.7.3 0.25% / 2× / one-position / mark-price stops**: preserved.
- **No retained verdict changed.**
- **No project lock changed.**

## Boundary Confirmation

This merge did NOT start or authorize:

- Phase 4aq;
- Phase 5;
- Phase 4 canonical;
- any successor phase;
- forensic computation;
- MFE / MAE computation;
- realized-R distributions;
- offline 15m join;
- rerun;
- backtest;
- script execution;
- data acquisition;
- manifest update;
- source / test / script / data changes;
- strategy proposal;
- strategy rescue;
- R3 optimization;
- R3-prime;
- R2-prime;
- R1a-prime;
- R1b-narrow-prime;
- 5m thread reopening;
- 5m / 1m / aggTrades / tick / mark-price 30m / 4h data acquisition;
- paper / shadow;
- live-readiness;
- deployment;
- production keys;
- authenticated APIs;
- private endpoints;
- public-endpoint calls in code;
- user stream;
- WebSocket;
- listenKey;
- exchange-write;
- MCP;
- Graphify;
- `.mcp.json`;
- credentials.

This merge did NOT modify:

- source code under `src/prometheus/`;
- tests under `tests/`;
- scripts under `scripts/`;
- raw data under `data/raw/`;
- normalized data under `data/normalized/`;
- derived data under `data/derived/`;
- research data under `data/research/`;
- manifests under `data/manifests/`;
- runtime implementation;
- existing strategy specifications;
- project locks;
- retained verdicts;
- M0 governance text
  (`docs/00-meta/m0-mechanism-admissibility-gate.md`);
- specialist governance files except for the narrow
  `docs/00-meta/current-project-state.md` update brought forward
  from the Phase 4ap memo commit.

## Retained Verdict Ledger

Retained verdicts remain unchanged:

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

No retained verdicts were revised.

## Project Locks

Project locks remain unchanged:

- M0 governance remains binding prospectively only.
- No retained verdict is revised.
- No project lock is changed.
- §11.6 HIGH cost = 8 bps per side; round-trip = 16 bps slippage;
  taker fee = 4 bps per side; no maker rebates; no live fee
  assumption. Any future fee / slippage / funding decomposition may
  be reported descriptively only and must not change the locked
  project-level cost reference or revise historical results.
- §1.7.3 project-level locks:
  - 0.25% risk per trade;
  - 2× leverage cap;
  - one position max;
  - mark-price stops where applicable.
- Phase 3r §8 mark-price gap governance preserved.
- Phase 3v §8 stop-trigger-domain governance preserved.
- Phase 3w §6 / §7 / §8 break-even / EMA-slope / stagnation
  governance preserved.
- Phase 4j §11 metrics OI-subset partial-eligibility rule preserved.
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
- Phase 4ap forensic plan preserved.

## Final Recommended State

After this merge, the recommended state is:

```text
remain paused unless the operator separately authorizes a future phase
```

Phase 4ap does not recommend immediate forensic computation.

Phase 4ap does not recommend immediate strategy work.

Phase 4ap does not authorize Phase 4aq.

No next phase is authorized by this merge.
