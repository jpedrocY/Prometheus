# Phase 4ag Merge Closeout — Research-Program Pivot and Mechanism-Source Triage Memo

## Purpose

This document records the no-fast-forward merge of completed Phase 4ag into `main`.

This is a merge closeout only. It does not authorize Phase 4ah, data acquisition, analysis execution, backtests, strategy diagnostics, fresh-hypothesis discovery, strategy work, implementation, paper/shadow, live-readiness, or exchange-write.

## Merge Summary

- Phase 4ag title: Research-Program Pivot and Mechanism-Source Triage Memo
- Merge branch: `phase-4ag/research-program-pivot-mechanism-source-triage`
- Target branch: `main`
- Main before merge: `25959dd5239a1c3af27e842826eb49589cb1da4d`
- Phase 4ag commit: `47ae76412f7654b1d20ec78bc87d4681ea6ae80f`
- Merge method: `--no-ff`

## Files Brought Forward From Phase 4ag

Phase 4ag was docs-only.

Phase 4ag created:

- `docs/00-meta/implementation-reports/2026-05-04_phase-4ag_research-program-pivot-mechanism-source-triage.md`
- `docs/00-meta/implementation-reports/2026-05-04_phase-4ag_closeout.md`

This merge closeout created:

- `docs/00-meta/implementation-reports/2026-05-04_phase-4ag_merge-closeout.md`

This merge also updated narrowly:

- `docs/00-meta/current-project-state.md`

## Phase 4ag Summary

Phase 4ag evaluated whether Prometheus should continue investigating price-only single-symbol directional continuation or pivot toward a different mechanism-source family after the cumulative evidence through Phase 4af.

The Phase 4ag triage matrix evaluated seven mechanism-source families:

1. Continue price-only single-symbol continuation — `NOT_RECOMMENDED`.
2. Cross-sectional trend / relative-strength / symbol-selection — `ADMISSIBLE_FOR_FUTURE_DOCS_ONLY_STUDY`.
3. Market-state / regime-transition momentum — `CONDITIONAL_ONLY`.
4. Derivatives positioning / funding / OI / liquidation context — `CONDITIONAL_ONLY`.
5. Microstructure / order-flow / liquidity timing — `NOT_RECOMMENDED`.
6. Mark-price stop-domain / execution realism — `NOT_RECOMMENDED` now.
7. Remain paused — `REMAIN_PAUSED`.

Phase 4ag's synthesis:

```text
Price-only directional continuation / substrate research has produced movement evidence,
but not directional-edge evidence.
```

Phase 4ag's primary recommendation:

```text
Option A — remain paused.
```

Phase 4ag's conditional secondary recommendation:

```text
Future docs-only Phase 4ah single-position cross-sectional trend /
relative-strength feasibility memo.
```

This conditional secondary is not started or authorized by this merge.

## External Research Status

Phase 4ag recorded that external web / literature research was available.

Two narrow searches were used for mechanism-source triage:

- cross-sectional crypto momentum / transaction-cost literature;
- crypto perpetual futures funding-rate factor literature.

The memo recorded the external references as triage context only.

The merge does not authorize further web research, data acquisition, literature expansion, analysis execution, hypothesis discovery, strategy specification, or backtesting.

## M0 Mechanism-Admissibility Gate Status

Phase 4ag recorded a proposed ten-clause M0 mechanism-admissibility gate as a recommendation only.

The M0 gate was NOT adopted as binding governance by Phase 4ag.

The M0 gate is not adopted by this merge.

Adoption of any M0 gate, Phase 4z admissibility redesign, Phase 4m validity-gate reconciliation, or Phase 4t scoring-matrix reconciliation would require separate operator authorization in a future phase.

## Governance Status

Phase 4ag recommendations are recommendations only.

Phase 4ag does not authorize Phase 4ah.

Phase 4ag does not authorize fresh-hypothesis discovery.

Phase 4ag does not authorize strategy specs.

Phase 4ag does not authorize backtests.

Phase 4ag does not authorize data acquisition.

Phase 4ag does not authorize analysis execution.

Phase 4ag does not authorize paper/shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, MCP, Graphify, `.mcp.json`, or credentials.

Phase 4ag does not adopt Phase 4z recommendations as binding governance.

Phase 4ag does not adopt the Phase 4aa admissibility framework as binding governance.

Phase 4ag does not adopt Phase 4ab recommendations as binding governance.

Phase 4ag does not broaden Phase 4ac results beyond data / integrity evidence.

Phase 4ag does not broaden Phase 4ad Rules A / B / C beyond prospective analysis-time scope.

Phase 4ag does not broaden Phase 4ae findings beyond descriptive substrate-feasibility evidence.

Phase 4ag does not broaden Phase 4af findings beyond descriptive regime-continuity / directional-persistence evidence.

## Boundary Confirmation

This merge did not start:

- Phase 4ah;
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
- any backtest;
- any strategy diagnostic;
- Q1–Q7 rerun;
- strategy PnL calculation;
- entry/exit strategy-return calculation;
- optimization;
- threshold selection for a future strategy;
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
- R3-prime / R2-prime / F1-prime / D1-A-prime / V2-prime / G1-prime / C1-prime;
- V1-D1 / F1-D1 / any hybrid;
- old-strategy alt-symbol reruns;
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
- specialist governance files except for the narrow current-project-state update required to record the merge.

## Retained Verdict Ledger

Retained verdicts remain unchanged:

- H0 remains FRAMEWORK ANCHOR.
- R3 remains BASELINE-OF-RECORD.
- R1a remains RETAINED — NON-LEADING.
- R1b-narrow remains RETAINED — NON-LEADING.
- R2 remains FAILED — §11.6.
- F1 remains HARD REJECT.
- D1-A remains MECHANISM PASS / FRAMEWORK FAIL.
- 5m thread remains CLOSED operationally.
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
- Phase 4z recommendations remain recommendations only.
- Phase 4aa admissibility framework remains recommendation only.
- Phase 4ab recommendations remain recommendations only.
- Phase 4ac results remain data / integrity evidence only.
- Phase 4ad Rules A / B / C remain prospective analysis-time scope rules only.
- Phase 4ae findings remain descriptive substrate-feasibility evidence only.
- Phase 4af findings remain descriptive regime-continuity / directional-persistence evidence only.
- Phase 4ag recommendations remain recommendations only.

## Final Recommended State

After this merge, the recommended state is:

```text
remain paused unless the operator separately authorizes a future phase
```

Phase 4ag does not recommend immediate fresh-hypothesis discovery.

Phase 4ag does not recommend immediate strategy work.

Phase 4ag does not authorize Phase 4ah.

No next phase is authorized by this merge.
