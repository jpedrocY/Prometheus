# Phase 4ae Merge Closeout — Alt-Symbol Substrate-Feasibility Analysis Memo

## Purpose

This document records the no-fast-forward merge of completed Phase 4ae into `main`.

This is a merge closeout only. It does not authorize Phase 4af, data acquisition, data modification, manifest changes, new substrate-feasibility execution, backtests, strategy diagnostics, strategy work, implementation, paper/shadow, live-readiness, or exchange-write.

## Merge Summary

- Phase 4ae title: Alt-Symbol Substrate-Feasibility Analysis Memo
- Merge branch: `phase-4ae/alt-symbol-substrate-feasibility-analysis`
- Target branch: `main`
- Main before merge: `10f122e7be70a4080b181573e07a73c88227b0bb`
- Phase 4ae commit: `3a8bf4acdbd1d26fc520dfb649cb34f4be38c8a2`
- Merge method: `--no-ff`

## Files Brought Forward From Phase 4ae

Phase 4ae was analysis-and-docs only.

Phase 4ae created:

- `scripts/phase4ae_alt_symbol_substrate_feasibility.py`
- `docs/00-meta/implementation-reports/2026-05-04_phase-4ae_alt-symbol-substrate-feasibility-analysis.md`
- `docs/00-meta/implementation-reports/2026-05-04_phase-4ae_closeout.md`

This merge closeout created:

- `docs/00-meta/implementation-reports/2026-05-04_phase-4ae_merge-closeout.md`

This merge also updated narrowly:

- `docs/00-meta/current-project-state.md`

Local analysis outputs under `data/research/phase4ae/` remain gitignored and were not committed.

## Phase 4ae Summary

Phase 4ae computed descriptive substrate-feasibility metrics for the Phase 4ac core symbol set under Phase 4ad Rule B1 common post-gap scope.

Symbols analyzed:

```text
BTCUSDT
ETHUSDT
SOLUSDT
XRPUSDT
ADAUSDT
```

Intervals analyzed:

```text
15m
30m
1h
4h
```

Analysis window:

```text
2022-04-03 00:00 UTC through 2026-04-30 23:59:59 UTC
```

Phase 4ae computed 20 symbol × interval cells, with:

```text
0 omitted datasets
0 missing bars in span
```

Phase 4ad Rule B1 was applied verbatim.

Mark-price datasets were not used. Phase 4ad Rule A was deferred.

Metrics / OI were not used.

AggTrades / tick / order-book data were not used.

## Main Findings

Phase 4ae findings are descriptive substrate-feasibility evidence only.

Key descriptive findings:

- Cost-cushion ranking was consistent across all four intervals:
  ```text
  SOL > ADA > XRP > ETH > BTC
  ```
  from most cushion to least.
- BTC had the tightest cost cushion at every interval.
- BTC was the most cleanly trending substrate by simple EMA regime proxies.
- BTC had the deepest kline-notional proxy and the most stable funding profile.
- SOL had the strongest cost cushion but the widest funding distribution and more frequent funding sign flips.
- ADA had clean kline coverage and good cost cushion, but lower kline-notional proxy and weaker higher-timeframe trend dominance.
- XRP and ETH were generally intermediate across most dimensions.
- No single symbol dominated on every dimension.
- Wick-fraction differences across symbols were small at the median.
- Mark-price stop-pathology behavior remained unmeasured and deferred under Phase 4ad Rule A.

## Governance Status

Phase 4ae results are descriptive substrate-feasibility evidence only.

Phase 4ae does not create a strategy candidate.

Phase 4ae does not authorize a fresh-hypothesis memo.

Phase 4ae does not authorize a strategy spec.

Phase 4ae does not authorize a backtest plan.

Phase 4ae does not authorize backtests, strategy diagnostics, paper/shadow, live-readiness, or exchange-write.

Phase 4ae does not modify Phase 4ac manifests.

Phase 4ae does not flip any `research_eligible` flag.

Phase 4ae does not broaden Phase 4ac results into binding cross-project governance.

Phase 4ae does not broaden Phase 4ad Rules A / B / C beyond prospective analysis-time scope.

Phase 4ae does not adopt Phase 4z recommendations as binding governance.

Phase 4ae does not adopt the Phase 4aa admissibility framework as binding governance.

Phase 4ae does not adopt Phase 4ab recommendations as binding governance.

## Phase 4ae Recommendation

Phase 4ae primary recommendation:

```text
Option A — remain paused.
```

Conditional secondary:

```text
Option C — future narrower follow-up feasibility memo.
```

This conditional secondary is not recommended over remaining paused.

Phase 4ae explicitly records that:

- immediate fresh-hypothesis discovery is premature;
- old-strategy alt-symbol reruns remain forbidden;
- direct strategy-spec memo on alt symbols is forbidden;
- backtest / paper / shadow / live work remains forbidden;
- mark-price feasibility work would require Phase 4ad Rule A predeclaration.

## Boundary Confirmation

This merge did not start:

- Phase 4af;
- Phase 5;
- Phase 4 canonical;
- any successor phase;
- data acquisition;
- data download;
- API calls;
- endpoint calls;
- data modification;
- manifest creation;
- manifest modification;
- v003 or any dataset version;
- Phase 4ac rerun;
- Phase 4ae rerun;
- any new substrate-feasibility calculation;
- any backtest;
- any strategy diagnostic;
- Q1–Q7 rerun;
- strategy PnL calculation;
- entry/exit strategy-return calculation;
- optimization;
- threshold selection for a future strategy;
- a new strategy;
- a fresh-hypothesis memo;
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

- source code under `src/prometheus/`;
- tests;
- existing scripts;
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
- Phase 4ad Rules A / B / C remain prospective future-use scope rules only.

## Final Recommended State

After this merge, the recommended state is:

```text
remain paused unless the operator separately authorizes a future phase
```

Phase 4ae does not recommend immediate fresh-hypothesis discovery.

Phase 4ae does not recommend immediate strategy work.

Phase 4ae does not authorize Phase 4af.

No next phase is authorized by this merge.
