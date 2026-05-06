# Phase 4ao Merge Closeout — Exit-Path Methodology / Artefact Harmonization Memo

## Purpose

This document records the no-fast-forward merge of completed Phase 4ao
into `main`.

This is a docs-only merge closeout. It does not authorize Phase 4ap or
any successor phase. It does not authorize forensic computation, MFE/MAE
computation, realized-R distributions, offline 15m joins, rerun, backtest,
script execution, data acquisition, manifest update, source / test /
script / data changes, strategy proposal, strategy rescue, 5m thread
reopening, 5m / 1m / aggTrades / tick / mark-price 30m / 4h data
acquisition, paper / shadow, live-readiness, deployment, production
keys, authenticated APIs, private endpoints, public-endpoint calls in
code, user stream, WebSocket, exchange-write, MCP, Graphify, `.mcp.json`,
or credentials.

## Merge Summary

- Phase 4ao title: Exit-Path Methodology / Artefact Harmonization Memo
- Merge branch: `phase-4ao/exit-path-methodology-artefact-harmonization`
- Target branch: `main`
- Main before merge: `a73c00b1de878ca9ee020a7942bd9af7ebb831ed`
- Phase 4ao memo + current-project-state commit:
  `6ace04fa6abb69e2ce7eb716c402bb7738ccedce`
- Phase 4ao closeout commit: `c2d7d83f64af55aae0fa20b2140cd37afcca015c`
- Merge method: `--no-ff`
- Merge commit SHA recorded before final self-reference amend: `e0c280d67c027b729e5b58fbdb1e4bb9acfe58e7`
- Final live main SHA after self-reference amend: `eeb69621d7b5c87cbd748b3ddeab651071fd13ad`
- Self-reference limitation: a git commit cannot contain its own SHA;
  every `git commit --amend --no-edit` produces a new SHA. The two SHAs
  above are intermediate amend artefacts that document the merge-commit
  evolution. After the final self-reference amend that incorporated the
  `eeb6962...` line into this file, the live main HEAD on origin/main
  is one further SHA beyond `eeb6962...`. That live main HEAD SHA is
  reported in the operator chat report rather than recorded in this
  merge-closeout file, because per operator convention this file does
  not amend indefinitely. The `eeb6962...` SHA is the closest stable
  self-reference: it was the live main HEAD at the moment this line
  was written, and remains a valid traceable reference into the
  reflog / amend chain even after the final amend is performed.

Note on the recorded merge commit SHA: due to the documented git self-
reference artifact (every amend changes the SHA, and a commit cannot
contain its own SHA), the recorded SHA may be one amend cycle behind
the live HEAD on main after the final amend. If self-reference cannot
be made stable, both pre-amend and post-amend SHAs are recorded
explicitly in the section below for traceability.

## Files Brought Forward From Phase 4ao

Phase 4ao was docs-only.

Phase 4ao created:

- `docs/00-meta/implementation-reports/2026-05-06_phase-4ao_exit-path-methodology-artefact-harmonization.md`
- `docs/00-meta/implementation-reports/2026-05-06_phase-4ao_closeout.md`

This merge closeout created:

- `docs/00-meta/implementation-reports/2026-05-06_phase-4ao_merge-closeout.md`

This merge also updated narrowly:

- `docs/00-meta/current-project-state.md`

(The `current-project-state.md` update was performed in the Phase 4ao
memo commit `6ace04f` on the phase branch and is brought forward by this
merge; the merge-closeout commit itself does not further modify
`current-project-state.md`.)

## Phase 4ao Summary

Phase 4ao was docs-only methodology / artefact harmonization. It defined
how a future exit-path forensic computation would need to be specified
before computation. It did not compute MFE / MAE, did not compute
realized-R distributions, did not perform exit-path forensics, did not
run any backtest or strategy / data-acquisition script, did not run an
offline 15m-join MFE / MAE reconstruction, did not acquire data, did not
modify any data file, manifest, source file, test, or script, did not
modify any retained verdict, project lock, or M0 governance text, did not
amend Phase 3t 5m closure or Phase 3v §8 stop-trigger-domain governance,
and did not authorize any successor phase.

Phase 4ao is derived from the Phase 4an inventory baseline:

- V1-arc populations (H0, R3, R1a, R1b-narrow, R2):
  `RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS`.
- F1, D1-A:
  `RECONSTRUCTABLE_ONLY_WITH_RERUN` for MFE / MAE;
  `RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS` for non-excursion fields.
- V2, G1, C1: `RECONSTRUCTABLE_ONLY_WITH_RERUN`.
- 5m thread: `CLOSED_CONTEXT_ONLY` (Phase 3t).
- Forbidden-rescue-risk: MEDIUM for H0 / R3; HIGH for R1a / R1b-narrow;
  CRITICAL for R2 / F1 / D1-A / V2 / G1 / C1 / 5m thread.

## Harmonization Result

Six headline rules brought forward by this merge:

1. **Population scope for any future first-pass forensics**: V1-arc only
   (H0 / R3 / R1a / R1b-narrow / R2). R3 may be included only as
   baseline-of-record descriptive context, NOT as an optimization target,
   NOT as R3-prime, NOT as R3 rescue, and NOT as a license for baseline-
   of-record revision.

2. **F1 / D1-A MFE / MAE require reconstruction**: Route B offline
   15m-join is governance-preferred over Route A controlled-rerun on
   rescue-risk grounds, because Route B does not modify or re-execute
   strategy code. Neither route is authorized by Phase 4ao. Either
   would require a separately authorized successor phase satisfying
   the §14 18-heading minimum predeclared-methodology template.

3. **V2 / G1 / C1 rerun-based per-trade forensics remain governance-
   risk-unresolved** under the M0 post-null cooldown rule and are not
   recommended for first-pass forensics. Any consideration would
   require a separately authorized OQ-B-resolution memo first.

4. **Cross-population realized-R / cost comparison requires explicit
   separation across seven accounting axes**: engine path; fee
   assumption (V1-arc / F1 / D1-A 5 bps / side vs V2 / G1 / C1 4 bps /
   side; both research-conventions); slippage cell (HIGH = 8 bps / side
   preserved verbatim per §11.6); funding handling (V2 right-inclusive,
   G1 strictly between, C1 excluded per Phase 4w); cost-cell label;
   stop-trigger-domain label (Phase 3v §8); per-trade vs aggregate.
   §11.6 LOCK is preserved verbatim. Any future fee / slippage /
   funding decomposition is descriptive only and must not change the
   locked project-level cost reference or revise historical results.

5. **Stop-trigger-domain governance (Phase 3v §8) preserved**:
   `trade_price_backtest`, `mark_price_runtime`,
   `mark_price_backtest_candidate` remain valid; `mixed_or_unknown`
   fails closed; mark-price path forensics for live-readiness remains
   BLOCKED under §1.7.3.

6. **5m research thread remains closed (Phase 3t)**: existing 5m data
   may only be referenced as a forensic measurement layer under the
   conservative §13.3 criterion (predeclared bar-resolution-ambiguity
   question; no new 5m strategy or rule; no Q1–Q7 conversion to rule
   input; documented in predeclared methodology; separately authorized
   successor phase). The 5m strategy thread is NOT reopened. Q1–Q7
   outputs are NOT rule-input candidates.

The minimum predeclared-methodology template is specified in Phase 4ao
§14 with 18 required headings (population(s) included; population(s)
excluded; reason for inclusion; artefact source; field definitions;
cost assumptions; stop-trigger-domain label; timeframe / data-resolution
label; MFE / MAE definition; bar-ambiguity handling; lower-timeframe
escalation rule; forbidden interpretations; allowed interpretations;
no-rescue statement; verdict / lock preservation statement; outputs to
produce; stop conditions; merge / closeout requirements).

## Open Question Status After Phase 4ao

- **OQ-A** (offline 15m-join MFE / MAE recovery sufficiency for F1 /
  D1-A): remains open until a separately authorized computation phase.
  Route B preferred if ever authorized.
- **OQ-B** (V2 / G1 / C1 rerun under M0 post-null cooldown): remains
  formally unresolved. Phase 4ao conservatively classifies it as
  governance-risk-unresolved and would require a separately authorized
  docs-only OQ-B-resolution memo to clarify whether audit-only rerun
  is admissible.
- **OQ-C** (Phase 4am V2 cost-application limitations and cross-
  population realized-R comparisons): answered YES, harmonization spec
  required; seven accounting axes specified per Phase 4ao §11.
- **OQ-D** (minimum-sufficient predeclared-methodology template):
  answered; specified per Phase 4ao §14 with 18 required headings.
- **OQ-E** (forensic-measurement-layer vs reopened-thread boundary
  for 5m): conservatively framed; measurement-layer boundary defined
  per Phase 4ao §13.3 without reopening Phase 3t 5m closure.

## Governance Status After Merge

- **M0 mechanism-admissibility gate** (Phase 4ak twelve-clause M0
  governance): unchanged.
- **M0 post-null cooldown rule**: unchanged.
- **M0 cooled-down families list**: unchanged.
- **Phase 4al refined no-rescue rule**: preserved.
- **Phase 4al §13 future-Phase-4am-style boundary specification**:
  preserved.
- **Phase 4al §14 data-resolution hierarchy**: preserved.
- **Phase 4am §11.A audit findings (F-1 / F-2 / F-3 / F-4)**: preserved
  as documentation for future methodology-harmonization scoping.
- **Phase 4an inventory result**: preserved.
- **Phase 4ao harmonization result**: recorded in repository as docs-
  only methodology evidence.
- **Phase 3t 5m closure**: preserved.
- **Phase 3v §8 stop-trigger-domain governance**: preserved.
- **Phase 3r §8 mark-price gap governance**: preserved.
- **Phase 3w §6 / §7 / §8 break-even / EMA-slope / stagnation
  governance**: preserved.
- **Phase 4j §11 metrics OI-subset partial-eligibility rule**: preserved.
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

- Phase 4ap;
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
  `docs/00-meta/current-project-state.md` update brought forward from
  the Phase 4ao memo commit.

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
- §11.6 HIGH cost = 8 bps per side; round-trip = 16 bps slippage; taker
  fee = 4 bps per side; no maker rebates; no live fee assumption.
  Any future fee / slippage / funding decomposition may be reported
  descriptively only and must not change the locked project-level cost
  reference or revise historical results.
- §1.7.3 project-level locks:
  - 0.25% risk per trade;
  - 2× leverage cap;
  - one position max;
  - mark-price stops where applicable.
- Phase 3r §8 mark-price gap governance preserved.
- Phase 3v §8 stop-trigger-domain governance preserved.
- Phase 3w §6 / §7 / §8 break-even / EMA-slope / stagnation governance
  preserved.
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

## Final Recommended State

After this merge, the recommended state is:

```text
remain paused unless the operator separately authorizes a future phase
```

Phase 4ao does not recommend immediate forensic computation.

Phase 4ao does not recommend immediate strategy work.

Phase 4ao does not authorize Phase 4ap.

No next phase is authorized by this merge.
