# Phase 4ah Merge Closeout — Single-Position Cross-Sectional Trend / Relative-Strength Feasibility Memo

## Purpose

This document records the no-fast-forward merge of completed Phase 4ah into `main`.

This is a merge closeout only. It does not authorize Phase 4ai, data acquisition, analysis execution, backtests, strategy diagnostics, fresh-hypothesis discovery, strategy work, implementation, paper/shadow, live-readiness, or exchange-write.

## Merge Summary

- Phase 4ah title: Single-Position Cross-Sectional Trend / Relative-Strength Feasibility Memo
- Merge branch: `phase-4ah/single-position-cross-sectional-trend-feasibility`
- Target branch: `main`
- Main before merge: `fa72870ff38e024e80d2d2987d1820bfa1b48c9c`
- Phase 4ah commit: `e3ca85a2b99fbec149a55f154ee4f0f1f9ded4b1`
- Merge method: `--no-ff`

## Files Brought Forward From Phase 4ah

Phase 4ah was docs-only.

Phase 4ah created:

- `docs/00-meta/implementation-reports/2026-05-04_phase-4ah_single-position-cross-sectional-trend-feasibility.md`
- `docs/00-meta/implementation-reports/2026-05-04_phase-4ah_closeout.md`

This merge closeout created:

- `docs/00-meta/implementation-reports/2026-05-04_phase-4ah_merge-closeout.md`

This merge also updated narrowly:

- `docs/00-meta/current-project-state.md`

## Phase 4ah Summary

Phase 4ah evaluated whether a future Prometheus research lane based on single-position cross-sectional trend / relative-strength / symbol-selection is admissible after Phase 4ag, while preserving the project's `one position max` operational lock.

Phase 4ah defined the future mechanism family as:

```text
Single-position cross-sectional trend / relative-strength symbol selection.
```

Meaning:

- rank a fixed, predeclared symbol universe on predeclared descriptors using prior-completed bars;
- select at most one symbol for future hypothetical consideration;
- allow "no symbol" as a possible output;
- keep ranking separate from entry / exit rules;
- preserve one-position max.

It explicitly does not mean:

- multi-position portfolio trading;
- market-neutral long-short portfolios;
- old-strategy alt-symbol reruns;
- V2 / G1 / C1 breakout rules wrapped in a ranking layer;
- a strategy spec;
- a backtest;
- live symbol rotation.

Phase 4ah recommended that any possible future analysis use the fixed five-symbol Phase 4ac core universe:

```text
BTCUSDT
ETHUSDT
SOLUSDT
XRPUSDT
ADAUSDT
```

and keep the Phase 4aa deferred watchlist deferred:

```text
BNBUSDT
DOGEUSDT
LINKUSDT
AVAXUSDT
```

Phase 4ah recorded five possible future ranking-descriptor families:

1. Multi-horizon relative return.
2. Relative trend state.
3. Volatility-adjusted relative strength.
4. Volume / notional confirmation.
5. Market-state conditional ranking.

It did not compute any descriptors.

Phase 4ah recorded anti-rescue / anti-reduction rules, including:

- no old-strategy alt-symbol reruns;
- no "rank first, then run V2 / G1 / C1 breakout" structure;
- no post-hoc threshold tuning;
- no symbol-mining;
- no multi-position portfolio trading;
- no strategy candidate naming;
- preserve the possibility of "no admissible cross-sectional effect."

## Literature / Web Context

Phase 4ah recorded that external web / literature research was available.

Three narrow searches were used for cross-sectional / relative-strength feasibility context:

- time-series momentum cryptocurrency Han / Kang / Ryu transaction-cost research;
- crypto momentum crash / drawdown / volatility-managed strategy research;
- single-asset symbol-selection versus portfolio momentum factor context.

The literature summary recorded:

- time-series momentum is the better-documented crypto family;
- cross-sectional long-short factor evidence is weaker;
- crash / drawdown risk is real and partly forecastable;
- volatility-managed weighting is typically multi-position and does not directly port to single-position selection;
- practitioner relative-strength models are typically multi-position;
- Prometheus's single-position selection reframe is novel and is its own design problem.

This merge does not authorize further literature expansion, data acquisition, analysis execution, hypothesis discovery, strategy specification, or backtesting.

## M0 Mechanism-Admissibility Gate Status

Phase 4ah applied the Phase 4ag proposed M0 mechanism-admissibility gate as a non-binding diagnostic checklist.

The single-position cross-sectional lane received:

- six PASS / four CONDITIONAL / zero structural FAIL under the non-binding checklist.

M0 was NOT adopted as binding governance by Phase 4ah.

M0 is not adopted by this merge.

Adoption of M0, Phase 4z admissibility redesign, Phase 4m validity-gate reconciliation, or Phase 4t scoring-matrix reconciliation would require separate operator authorization in a future phase.

## Phase 4ah Recommendation

Phase 4ah primary recommendation:

```text
Merge Phase 4ah into main, then remain paused unless the operator separately
authorizes a future Phase 4ai single-position cross-sectional trend feasibility analysis.
```

Conditional secondary:

```text
Future analysis-and-docs Phase 4ai using the fixed five-symbol core universe under
Phase 4ad Rule B1 scope, with predeclared ranking descriptors, predeclared rebalance
frequency, predeclared rank-quality filter, and predeclared falsification criteria.
```

Phase 4ai is not started or authorized by this merge.

## Governance Status

Phase 4ah recommendations are recommendations only.

Phase 4ah does not authorize Phase 4ai.

Phase 4ah does not authorize fresh-hypothesis discovery.

Phase 4ah does not authorize strategy specs.

Phase 4ah does not authorize backtests.

Phase 4ah does not authorize data acquisition.

Phase 4ah does not authorize analysis execution.

Phase 4ah does not authorize paper/shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, MCP, Graphify, `.mcp.json`, or credentials.

Phase 4ah does not adopt M0 as binding governance.

Phase 4ah does not adopt Phase 4z recommendations as binding governance.

Phase 4ah does not adopt the Phase 4aa admissibility framework as binding governance.

Phase 4ah does not adopt Phase 4ab recommendations as binding governance.

Phase 4ah does not broaden Phase 4ac results beyond data / integrity evidence.

Phase 4ah does not broaden Phase 4ad Rules A / B / C beyond prospective analysis-time scope.

Phase 4ah does not broaden Phase 4ae findings beyond descriptive substrate-feasibility evidence.

Phase 4ah does not broaden Phase 4af findings beyond descriptive regime-continuity / directional-persistence evidence.

Phase 4ah does not broaden Phase 4ag recommendations beyond recommendation-only status.

## Boundary Confirmation

This merge did not start:

- Phase 4ai;
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
- multi-position portfolio trading;
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
- Phase 4ah recommendations remain recommendations only.

## Final Recommended State

After this merge, the recommended state is:

```text
remain paused unless the operator separately authorizes a future phase
```

Phase 4ah does not recommend immediate fresh-hypothesis discovery.

Phase 4ah does not recommend immediate strategy work.

Phase 4ah does not authorize Phase 4ai.

No next phase is authorized by this merge.
