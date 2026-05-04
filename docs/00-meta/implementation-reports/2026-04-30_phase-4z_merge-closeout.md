# Phase 4z Merge Closeout — Post-Rejection Research-Process Redesign Memo

## Purpose

This document records the no-fast-forward merge of completed Phase 4z into `main`.

This is a merge closeout only. It does not adopt Phase 4z recommendations as binding governance and does not start any successor phase.

## Merge Summary

- Phase 4z title: Post-Rejection Research-Process Redesign Memo
- Merge branch: `phase-4z/post-rejection-research-process-redesign`
- Target branch: `main`
- Main before merge: `8e94fb01951e07d428046026750f20197dfe9890`
- Phase 4z report commit: `cb426b127c8fce41e00f9c0684f4d4d7269b82d8`
- Phase 4z closeout / branch HEAD commit: `9968f346e00641a02817fc475491e27d6e5efe2e`
- Merge method: `--no-ff`

## Files Brought Forward From Phase 4z

Phase 4z was docs-only.

Phase 4z created:

- `docs/00-meta/implementation-reports/2026-04-30_phase-4z_post-rejection-research-process-redesign.md`
- `docs/00-meta/implementation-reports/2026-04-30_phase-4z_closeout.md`

This merge closeout created:

- `docs/00-meta/implementation-reports/2026-04-30_phase-4z_merge-closeout.md`

This merge also updated narrowly:

- `docs/00-meta/current-project-state.md`

## Governance Status

Phase 4z recommendations are not adopted governance.

Phase 4z proposed recommendations only, including:

- future admissibility framework concepts;
- design-family-distance concepts;
- explicit M0 theoretical-admissibility gate concept;
- edge-rate viability gate concept;
- template additions for future memos.

Adoption of any Phase 4z proposal remains a separate future operator decision.

## Boundary Confirmation

This merge did not start:

- Phase 5;
- Phase 4aa;
- Phase 4 canonical;
- any successor phase;
- a new strategy;
- C1 rescue;
- V2 rescue;
- G1 rescue;
- R2 rescue;
- F1 rescue;
- D1-A rescue;
- any fresh-hypothesis discovery memo;
- any strategy-spec memo;
- any backtest-plan memo;
- any backtest execution.

This merge did not modify:

- source code;
- tests;
- scripts;
- data;
- manifests;
- runtime implementation;
- existing strategy specifications;
- project locks;
- retained verdicts;
- governance files except for the narrow current-project-state update required to record the merge.

This merge did not involve:

- data acquisition;
- data modification;
- manifest creation;
- manifest modification;
- paper/shadow;
- live-readiness;
- deployment;
- production keys;
- authenticated APIs;
- private endpoints;
- user stream;
- WebSocket;
- exchange-write;
- MCP;
- Graphify;
- `.mcp.json`;
- credentials.

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

## Final Recommended State

After this merge, the recommended state is:

```text
stop / remain paused unless the operator separately authorizes a future phase
```

No next phase is authorized by this merge.
