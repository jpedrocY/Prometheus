# Phase 4aa Merge Closeout — Alt-Symbol Market-Selection and Strategy-Admissibility Memo

## Purpose

This document records the no-fast-forward merge of completed Phase 4aa into `main`.

This is a merge closeout only. It does not authorize a successor phase, data acquisition, backtests, strategy work, implementation, paper/shadow, live-readiness, or exchange-write.

## Merge Summary

- Phase 4aa title: Alt-Symbol Market-Selection and Strategy-Admissibility Memo
- Merge branch: `phase-4aa/alt-symbol-market-selection-admissibility`
- Target branch: `main`
- Main before merge: `6fb0c6c8ab0e634684a80e7b339c9c96f3a56b02`
- Phase 4aa commit: `b8adb9e59471c7584081349f0c4df5eb235d3c64`
- Merge method: `--no-ff`

## Files Brought Forward From Phase 4aa

Phase 4aa was docs-only.

Phase 4aa created:

- `docs/00-meta/implementation-reports/2026-05-04_phase-4aa_alt-symbol-market-selection-admissibility.md`
- `docs/00-meta/implementation-reports/2026-05-04_phase-4aa_closeout.md`

This merge closeout created:

- `docs/00-meta/implementation-reports/2026-05-04_phase-4aa_merge-closeout.md`

This merge also updated narrowly:

- `docs/00-meta/current-project-state.md`

## Phase 4aa Summary

Phase 4aa evaluated whether future strategy research should remain restricted to BTCUSDT / ETHUSDT or consider liquid large-cap Binance USDⓈ-M perpetual alt symbols.

The core candidate comparison universe recorded by Phase 4aa was:

```text
BTCUSDT
ETHUSDT
SOLUSDT
XRPUSDT
ADAUSDT
```

The optional secondary watchlist recorded by Phase 4aa was:

```text
BNBUSDT
DOGEUSDT
LINKUSDT
AVAXUSDT
```

Phase 4aa defined a recommended pre-backtest symbol-admissibility framework with eight gates:

1. Listing / continuity gate.
2. Public-data availability gate.
3. Cost-to-volatility gate.
4. Opportunity-rate gate.
5. Liquidity / execution-risk gate.
6. Wick / stop-pathology gate.
7. Idiosyncratic-risk gate.
8. Governance-label compatibility gate.

Phase 4aa recommendation:

```text
Primary recommendation:
Proceed next, if operator authorizes, with a docs-only alt-symbol data-requirements
and feasibility memo.

Do not backtest yet.
Do not acquire data yet unless separately authorized.
Do not rescue prior strategies.
Do not expand market type yet.
Keep research on Binance USDⓈ-M perpetuals for clean attribution.
```

## Governance Status

Phase 4aa recommendations are recommendations only.

Phase 4aa does not adopt Phase 4z recommendations as binding governance.

Phase 4aa does not convert its proposed symbol-admissibility framework into a binding project governance update. Any future governance adoption requires separate operator authorization.

## Boundary Confirmation

This merge did not start:

- Phase 4ab;
- Phase 5;
- Phase 4 canonical;
- any successor phase;
- data acquisition;
- data modification;
- manifest creation;
- manifest modification;
- any backtest;
- any diagnostic;
- Q1–Q7 rerun;
- a new strategy;
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
- paper/shadow;
- live-readiness;
- deployment;
- production-key creation;
- authenticated APIs;
- private endpoints;
- user stream;
- WebSocket;
- exchange-write;
- MCP;
- Graphify;
- `.mcp.json`;
- credentials.

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

## Final Recommended State

After this merge, the recommended state is:

```text
remain paused unless the operator separately authorizes a future phase
```

Phase 4aa's conditional secondary recommendation is a future docs-only alt-symbol data-requirements / feasibility memo, but that future phase is not authorized by this merge.

No next phase is authorized by this merge.
