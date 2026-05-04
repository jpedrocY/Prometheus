# Phase 4ab Merge Closeout — Alt-Symbol Data-Requirements and Feasibility Memo

## Purpose

This document records the no-fast-forward merge of completed Phase 4ab into `main`.

This is a merge closeout only. It does not authorize Phase 4ac, data acquisition, manifest creation, backtests, diagnostics, strategy work, implementation, paper/shadow, live-readiness, or exchange-write.

## Merge Summary

- Phase 4ab title: Alt-Symbol Data-Requirements and Feasibility Memo
- Merge branch: `phase-4ab/alt-symbol-data-requirements-feasibility`
- Target branch: `main`
- Main before merge: `a8e81bdf86164f86fcf3b09aaac5f40a15f55fc3`
- Phase 4ab commit: `524e4e7323df2e36b05be48423524f42af4d1e5c`
- Merge method: `--no-ff`

## Files Brought Forward From Phase 4ab

Phase 4ab was docs-only.

Phase 4ab created:

- `docs/00-meta/implementation-reports/2026-05-04_phase-4ab_alt-symbol-data-requirements-feasibility.md`
- `docs/00-meta/implementation-reports/2026-05-04_phase-4ab_closeout.md`

This merge closeout created:

- `docs/00-meta/implementation-reports/2026-05-04_phase-4ab_merge-closeout.md`

This merge also updated narrowly:

- `docs/00-meta/current-project-state.md`

## Phase 4ab Summary

Phase 4ab translated the completed Phase 4aa alt-symbol market-selection / admissibility memo into a concrete docs-only data-requirements and feasibility plan for possible future alt-symbol research on Binance USDⓈ-M perpetuals.

Phase 4ab recommended a possible future core acquisition-planning set:

```text
BTCUSDT
ETHUSDT
SOLUSDT
XRPUSDT
ADAUSDT
```

Phase 4ab kept the following optional secondary watchlist deferred:

```text
BNBUSDT
DOGEUSDT
LINKUSDT
AVAXUSDT
```

Phase 4ab recommended the following future data-family requirements / optionality:

1. Standard trade-price klines — REQUIRED at 15m / 30m / 1h / 4h.
2. Funding-rate history — REQUIRED.
3. Mark-price klines — CONDITIONAL REQUIRED.
4. Metrics / open-interest data — OPTIONAL / CONDITIONAL under Phase 4j §11.
5. AggTrades / tick / order-book data — DEFERRED / NOT RECOMMENDED NOW.
6. Exchange metadata snapshots — REQUIRED WHERE AVAILABLE.

Phase 4ab recommended a possible future acquisition date range:

```text
2022-01-01 through the latest fully completed month available at acquisition time
```

with listing-date constraints, common-overlap policy, full-available-history policy, and no fabricated pre-listing data.

Phase 4ab recommendation:

```text
Primary recommendation:
After review, merge Phase 4ab into main, then remain paused unless the operator
separately authorizes a docs-and-data Phase 4ac public alt-symbol acquisition
and integrity-validation phase.

If Phase 4ac is later authorized, keep scope limited to Binance USDⓈ-M perpetuals,
the core five-symbol set (BTCUSDT / ETHUSDT / SOLUSDT / XRPUSDT / ADAUSDT), and
predeclared public unauthenticated data families per Phase 4ab §6.

Do not backtest yet.
Do not create a strategy yet.
Do not rescue prior strategies.
Do not expand market type yet.
```

## Governance Status

Phase 4ab recommendations are recommendations only.

Phase 4ab does not adopt Phase 4z recommendations as binding governance.

Phase 4ab does not adopt the Phase 4aa admissibility framework as binding governance.

Phase 4ab does not convert its own data-requirements or feasibility recommendations into binding project governance. Any future governance adoption requires separate operator authorization.

## Boundary Confirmation

This merge did not start:

- Phase 4ac;
- Phase 5;
- Phase 4 canonical;
- any successor phase;
- data acquisition;
- data download;
- data modification;
- manifest creation;
- manifest modification;
- v003 or any dataset version;
- any backtest;
- any diagnostic;
- Q1–Q7 rerun;
- a new strategy;
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
- Phase 4aa admissibility framework remains recommendation only.
- Phase 4ab recommendations remain recommendations only.

## Final Recommended State

After this merge, the recommended state is:

```text
remain paused unless the operator separately authorizes a future phase
```

Phase 4ab's conditional next recommendation is a future docs-and-data Phase 4ac public alt-symbol acquisition and integrity-validation phase, but that future phase is not authorized by this merge.

No next phase is authorized by this merge.
