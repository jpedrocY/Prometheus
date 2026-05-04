# Phase 4af Merge Closeout — Alt-Symbol Regime-Continuity and Directional-Persistence Feasibility Memo

## Purpose

This document records the no-fast-forward merge of completed Phase 4af into `main`.

This is a merge closeout only. It does not authorize Phase 4ag, data acquisition, data modification, manifest changes, new regime-continuity / directional-persistence execution, backtests, strategy diagnostics, strategy work, implementation, paper/shadow, live-readiness, or exchange-write.

## Merge Summary

- Phase 4af title: Alt-Symbol Regime-Continuity and Directional-Persistence Feasibility Memo
- Merge branch: `phase-4af/alt-symbol-regime-continuity-persistence`
- Target branch: `main`
- Main before merge: `c57afa4447ad4e8ae3c12ac2c26891c612f03a57`
- Phase 4af commit: `ed1d62fd12a84c2a588a62159936ea716f54829c`
- Merge method: `--no-ff`

## Files Brought Forward From Phase 4af

Phase 4af was analysis-and-docs only.

Phase 4af created:

- `scripts/phase4af_alt_symbol_regime_persistence.py`
- `docs/00-meta/implementation-reports/2026-05-04_phase-4af_alt-symbol-regime-continuity-persistence.md`
- `docs/00-meta/implementation-reports/2026-05-04_phase-4af_closeout.md`

This merge closeout created:

- `docs/00-meta/implementation-reports/2026-05-04_phase-4af_merge-closeout.md`

This merge also updated narrowly:

- `docs/00-meta/current-project-state.md`

Local analysis outputs under `data/research/phase4af/` remain gitignored and were not committed.

## Phase 4af Summary

Phase 4af computed descriptive regime-continuity and directional-persistence metrics for the Phase 4ac core symbol set under Phase 4ad Rule B1 common post-gap scope.

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

Phase 4af computed 20 symbol × interval cells, with:

```text
0 omitted datasets
0 missing bars in span
```

Phase 4ad Rule B1 was applied verbatim.

Mark-price datasets were not used. Phase 4ad Rule A was deferred.

Metrics / OI were not used.

AggTrades / tick / order-book data were not used.

Funding history was not used.

## Main Findings

Phase 4af findings are descriptive regime-continuity / directional-persistence evidence only.

Key descriptive findings:

- Trend-state self-transition probabilities were uniformly high across all 20 cells:
  ```text
  P(UP self)   = 0.919–0.940
  P(DOWN self) = 0.923–0.940
  ```
  but this was uniform across symbols and did not create a differentiating cross-symbol edge.
- EMA-slope self-transition probabilities were uniformly high:
  ```text
  0.94–0.96
  ```
  in both directions, again with no differentiating edge.
- Post-expansion same-direction follow-through was at or below 0.50 across all 80 tested cells:
  ```text
  5 symbols × 4 intervals × 4 forward windows
  ```
  indicating no same-direction substrate bias.
- Bar-level sign persistence was consistently slightly below 0.50.
- Lag-1 return autocorrelation was near zero on every cell.
- Volatility-regime self-transition probabilities were uniformly high:
  ```text
  0.91–0.94
  ```
  but high-volatility regime was direction-agnostic.
- Cost-adjusted absolute-movement frequencies confirmed the Phase 4ae cost-cushion ranking at coarser intervals:
  ```text
  SOL > ADA > XRP > ETH > BTC
  ```
- UP-state and DOWN-state conditional cost-adjusted-move fractions were within ±2 percentage points of unconditional at every cell.
- Trend conditioning provided no cost-adjusted directional advantage.
- The practical summary was:
  ```text
  the market moves enough, especially on SOL / ADA / XRP,
  but the tested substrate metrics do not tell us which way.
  ```

## Governance Status

Phase 4af results are descriptive regime-continuity / directional-persistence evidence only.

Phase 4af does not create a strategy candidate.

Phase 4af does not authorize a fresh-hypothesis memo.

Phase 4af does not authorize a hypothesis-spec memo.

Phase 4af does not authorize a strategy spec.

Phase 4af does not authorize a backtest plan.

Phase 4af does not authorize backtests, strategy diagnostics, paper/shadow, live-readiness, or exchange-write.

Phase 4af does not modify Phase 4ac manifests.

Phase 4af does not flip any `research_eligible` flag.

Phase 4af does not broaden Phase 4ac results into binding cross-project governance.

Phase 4af does not broaden Phase 4ad Rules A / B / C beyond prospective analysis-time scope.

Phase 4af does not broaden Phase 4ae findings beyond descriptive substrate-feasibility evidence.

Phase 4af does not adopt Phase 4z recommendations as binding governance.

Phase 4af does not adopt the Phase 4aa admissibility framework as binding governance.

Phase 4af does not adopt Phase 4ab recommendations as binding governance.

## Phase 4af Recommendation

Phase 4af primary recommendation:

```text
Option A — remain paused.
```

Conditional secondary:

```text
Option B — future narrower follow-up feasibility memo.
```

This conditional secondary is not started by Phase 4af and requires separate operator authorization.

Phase 4af explicitly records that:

- immediate fresh-hypothesis discovery is not recommended;
- old-strategy alt-symbol reruns remain forbidden;
- direct strategy-spec memo on alt symbols is forbidden;
- backtest / paper / shadow / live work remains forbidden;
- mark-price feasibility work remains not recommended at this time.

## Boundary Confirmation

This merge did not start:

- Phase 4ag;
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
- Phase 4af rerun;
- any new regime-continuity calculation;
- any new directional-persistence calculation;
- any backtest;
- any strategy diagnostic;
- Q1–Q7 rerun;
- strategy PnL calculation;
- entry/exit strategy-return calculation;
- optimization;
- threshold selection for a future strategy;
- a new strategy;
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
- Phase 4ae findings remain descriptive substrate-feasibility evidence only.
- Phase 4af findings remain descriptive regime-continuity / directional-persistence evidence only.

## Final Recommended State

After this merge, the recommended state is:

```text
remain paused unless the operator separately authorizes a future phase
```

Phase 4af does not recommend immediate fresh-hypothesis discovery.

Phase 4af does not recommend immediate strategy work.

Phase 4af does not authorize Phase 4ag.

No next phase is authorized by this merge.
