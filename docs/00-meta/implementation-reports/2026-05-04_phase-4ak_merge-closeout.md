# Phase 4ak Merge Closeout — M0 Governance Adoption Phase

## Purpose

This document records the no-fast-forward merge of completed
Phase 4ak into `main`.

This is a merge closeout only. It does not authorize Phase 4al,
data acquisition, analysis execution, backtests, strategy
diagnostics, fresh-hypothesis discovery, strategy work,
implementation, paper/shadow, live-readiness, or exchange-write.

## Merge Summary

- Phase 4ak title: M0 Governance Adoption Phase
- Merge branch: `phase-4ak/m0-governance-adoption`
- Target branch: `main`
- Main before merge: `3ad5cc8cd870f9ade3d345fcd3765b9770edaff2`
- Phase 4ak commit: `065e1b098b2c8accd16cbc8b1a4a2f04c8540437`
- Merge method: `--no-ff`

## Files Brought Forward From Phase 4ak

Phase 4ak was docs-only.

Phase 4ak created:

- `docs/00-meta/m0-mechanism-admissibility-gate.md`
- `docs/00-meta/implementation-reports/2026-05-04_phase-4ak_m0-governance-adoption.md`
- `docs/00-meta/implementation-reports/2026-05-04_phase-4ak_closeout.md`

This merge closeout created:

- `docs/00-meta/implementation-reports/2026-05-04_phase-4ak_merge-closeout.md`

This merge also updated narrowly:

- `docs/00-meta/current-project-state.md`

No `docs/12-roadmap/phase-gates.md` cross-reference was added by
Phase 4ak.

## Phase 4ak Summary

Phase 4ak adopted the **revised twelve-clause M0 mechanism-
admissibility gate** and the **post-null cooldown rule** as
**binding prospective governance**.

The durable governance artifact is:

```text
docs/00-meta/m0-mechanism-admissibility-gate.md
```

### Adopted

- revised twelve-clause M0 gate;
- post-null cooldown rule;
- current cooled-down families list at the Phase 4ak adoption
  boundary;
- required future M0 memo template;
- adoption-limits / non-adoption clarifications.

### Not adopted

- full Phase 4z 32-item proposed admissibility framework;
- Phase 4z proposed M0–M7 mechanism-check redesign wholesale;
- Phase 4z proposed discovery-memo template;
- Phase 4z proposed strategy-spec template additions;
- Phase 4z proposed backtest-plan template additions;
- Phase 4z proposed execution-report template additions;
- Phase 4aa admissibility framework;
- Phase 4ab recommendations.

### Not changed

- Phase 4m 18-requirement fresh-hypothesis validity gate;
- Phase 4t 10-dimension candidate scoring matrix;
- retained verdicts;
- project locks;
- source code;
- tests;
- scripts;
- data;
- manifests.

## Governance Status After Merge

After this merge, M0 and the post-null cooldown rule are **binding
prospective governance** on `main`.

M0 applies prospectively only. It does not revise historical
verdicts, does not retroactively invalidate or alter prior phases,
and does not authorize any strategy, backtest, paper / shadow,
live-readiness, exchange-write, or successor phase.

Any future market-research lane within M0 applicability scope must
clear M0 before discovery / spec / backtest.

Any reopening of cooled-down lanes must clear M0 and justify a
materially new mechanism source.

Passing M0 does not authorize backtests or strategy specs.

Operator authorization remains required for every future phase,
including any future M0 memo.

## Phase 4ak Recommendation

Primary recommendation:

```text
Merge Phase 4ak into main, then remain paused.
```

M0 and the post-null cooldown rule are now binding prospective
governance, but no new market research, fresh-hypothesis discovery,
strategy work, or successor phase is authorized.

Phase 4ak does not authorize Phase 4al.

Phase 4ak does not recommend immediate fresh-hypothesis discovery.

Phase 4ak does not recommend immediate strategy work.

## Governance Boundary Confirmation

This merge did not adopt:

- full Phase 4z 32-item framework;
- Phase 4z M0–M7 mechanism-check redesign wholesale;
- Phase 4aa admissibility framework;
- Phase 4ab recommendations.

This merge did not change:

- Phase 4m 18-requirement gate;
- Phase 4t 10-dimension scoring matrix;
- §11.6;
- §1.7.3;
- Phase 3r §8;
- Phase 3v §8;
- Phase 3w §6 / §7 / §8;
- Phase 4j §11;
- Phase 4k;
- Phase 4p;
- Phase 4q;
- Phase 4v;
- Phase 4w;
- retained verdicts.

## Boundary Confirmation

This merge did not start:

- Phase 4al;
- Phase 5;
- Phase 4 canonical;
- any successor phase;
- data acquisition;
- data download;
- API calls;
- endpoint calls;
- analysis execution;
- data modification;
- manifest creation;
- manifest modification;
- v003 or any dataset version;
- Phase 4ac rerun;
- Phase 4ae rerun;
- Phase 4af rerun;
- Phase 4ag rerun;
- Phase 4ah rerun;
- Phase 4ai rerun;
- Phase 4aj rerun;
- Phase 4ak rerun;
- any new analysis execution;
- any backtest;
- any strategy diagnostic;
- Q1–Q7 rerun;
- strategy PnL calculation;
- entry/exit strategy-return calculation;
- equity curve creation;
- trade ledger creation;
- optimization;
- threshold selection;
- symbol selection;
- a new strategy;
- a strategy-candidate name;
- a fresh-hypothesis discovery memo;
- a hypothesis-spec memo;
- a strategy spec;
- a backtest plan;
- R3 rescue;
- R2 rescue;
- F1 rescue;
- D1-A rescue;
- V2 rescue;
- G1 rescue;
- C1 rescue;
- R3-prime / R2-prime / F1-prime / D1-A-prime / V2-prime /
  G1-prime / C1-prime;
- V1-D1 / F1-D1 / any hybrid;
- old-strategy alt-symbol reruns;
- multi-position portfolio trading;
- rank-then-V2 / G1 / C1 breakout structure;
- paper/shadow;
- live-readiness;
- deployment;
- production-key creation;
- authenticated APIs;
- private endpoints;
- public endpoint calls in code;
- user stream;
- WebSocket;
- exchange-write;
- MCP;
- Graphify;
- `.mcp.json`;
- credentials.

This merge did not modify:

- source code under `src/prometheus/`;
- tests;
- scripts;
- raw data;
- normalized data;
- manifests;
- runtime implementation;
- existing strategy specifications;
- project locks;
- retained verdicts;
- `docs/12-roadmap/phase-gates.md`;
- `docs/12-roadmap/technical-debt-register.md`;
- `docs/00-meta/ai-coding-handoff.md`;
- `docs/00-meta/implementation-ambiguity-log.md`;
- specialist governance files except for the new durable M0
  governance doc (`docs/00-meta/m0-mechanism-admissibility-gate.md`)
  and the narrow current-project-state update required to record
  the merge.

## Retained Verdict Ledger

Retained verdicts remain unchanged:

- H0 remains FRAMEWORK ANCHOR.
- R3 remains BASELINE-OF-RECORD.
- R1a remains RETAINED — NON-LEADING.
- R1b-narrow remains RETAINED — NON-LEADING.
- R2 remains FAILED — §11.6.
- F1 remains HARD REJECT.
- D1-A remains MECHANISM PASS / FRAMEWORK FAIL.
- 5m thread remains operationally CLOSED.
- V2 remains HARD REJECT — terminal for V2 first-spec.
- G1 remains HARD REJECT — terminal for G1 first-spec.
- C1 remains HARD REJECT — terminal for C1 first-spec.

No retained verdicts were revised.

## Project Locks

Project locks remain unchanged, including:

- §11.6 HIGH cost = 8 bps per side.
- §1.7.3 project-level locks:
  - 0.25% risk;
  - 2× leverage;
  - one position max;
  - mark-price stops where applicable.
- Phase 3r §8 preserved.
- Phase 3v §8 preserved.
- Phase 3w §6 / §7 / §8 preserved.
- Phase 4j §11 preserved.
- Phase 4k preserved.
- Phase 4p preserved.
- Phase 4q preserved.
- Phase 4v preserved.
- Phase 4w preserved.
- Phase 4z recommendations remain recommendations only **except
  the specific upstream twelve-clause M0 fragment now adopted by
  Phase 4ak**.
- Phase 4aa admissibility framework remains recommendation only.
- Phase 4ab recommendations remain recommendations only.
- Phase 4ac results remain data / integrity evidence only.
- Phase 4ad Rules A / B / C remain prospective analysis-time scope
  only.
- Phase 4ae findings remain descriptive substrate-feasibility
  evidence only.
- Phase 4af findings remain descriptive regime-continuity /
  directional-persistence evidence only.
- Phase 4ag recommendations remain recommendations only **except
  the specific upstream M0 gate now adopted as revised by
  Phase 4aj and adopted by Phase 4ak**.
- Phase 4ah recommendations remain recommendations only.
- Phase 4ai findings remain descriptive cross-sectional feasibility
  evidence only.
- Phase 4aj recommendations remain recommendations only **except
  the revised twelve-clause M0 gate and the post-null cooldown
  rule now adopted by Phase 4ak**.

## Final Recommended State

After this merge, the recommended state is:

```text
remain paused unless the operator separately authorizes a future phase
```

M0 and the post-null cooldown rule are binding prospective
governance on `main`, but Phase 4ak does not authorize Phase 4al,
fresh-hypothesis discovery, market research, strategy work, data
acquisition, backtesting, paper / shadow, live-readiness,
deployment, or exchange-write.

No next phase is authorized by this merge.
