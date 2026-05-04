# Phase 4ad Merge Closeout — Alt-Symbol Gap-Governance and Scope-Revision Memo

## Purpose

This document records the no-fast-forward merge of completed Phase 4ad into `main`.

This is a merge closeout only. It does not authorize Phase 4ae, data acquisition, data modification, manifest changes, substrate-feasibility execution, backtests, diagnostics, strategy work, implementation, paper/shadow, live-readiness, or exchange-write.

## Merge Summary

- Phase 4ad title: Alt-Symbol Gap-Governance and Scope-Revision Memo
- Merge branch: `phase-4ad/alt-symbol-gap-governance-scope-revision`
- Target branch: `main`
- Main before merge: `3478d05d97c43ee9ef885ae3defa4d1559189605`
- Phase 4ad commit: `7b4a0d9f949692cefe36cbd757ef8414166d6071`
- Merge method: `--no-ff`

## Files Brought Forward From Phase 4ad

Phase 4ad was docs-only.

Phase 4ad created:

- `docs/00-meta/implementation-reports/2026-05-04_phase-4ad_alt-symbol-gap-governance-scope-revision.md`
- `docs/00-meta/implementation-reports/2026-05-04_phase-4ad_closeout.md`

This merge closeout created:

- `docs/00-meta/implementation-reports/2026-05-04_phase-4ad_merge-closeout.md`

This merge also updated narrowly:

- `docs/00-meta/current-project-state.md`

## Phase 4ad Summary

Phase 4ad resolved how future alt-symbol substrate-feasibility work may treat Phase 4ac gap / invalid-window findings before any substrate-feasibility analysis, strategy discovery, backtest, diagnostics, or strategy work is allowed.

Phase 4ad defined three future-use scope rules for prospective analysis-time use of Phase 4ac data:

### Rule A — Mark-Price Invalid-Window Exclusion Rule

Future mark-price-dependent analysis must exclude any bar, trade, candidate event, diagnostic window, stop-domain window, or analysis window intersecting known mark-price invalid windows.

Conclusions must be labeled:

```text
conditional on valid mark-price coverage
```

Rule A is analogous to the Phase 3r §8 mark-price gap-governance precedent.

### Rule B — SOL/XRP Early-2022 Kline Gap Scope Rule

Future SOL/XRP trade-price kline analysis must choose exactly one predeclared policy before analysis begins:

- **Policy B1 — Common post-gap start**
  - Default recommendation.
  - Use `2022-04-03 00:00 UTC` as the common post-gap start for cross-symbol substrate-feasibility analysis.
- **Policy B2 — Full-history with invalid-window exclusion**
  - Allowed only with explicit exclusion counting / reporting.
- **Policy B3 — PASS-only subset**
  - Conservative fallback; excludes SOL/XRP kline data until a future acquisition/governance change exists.

### Rule C — PASS-Only Subset Rule

Conservative fallback restricted to the 9 Phase 4ac PASS datasets:

```text
binance_usdm_btcusdt_1h__v001
binance_usdm_ethusdt_1h__v001
binance_usdm_adausdt_15m__v001
binance_usdm_adausdt_30m__v001
binance_usdm_adausdt_1h__v001
binance_usdm_adausdt_4h__v001
binance_usdm_solusdt_funding__v001
binance_usdm_xrpusdt_funding__v001
binance_usdm_adausdt_funding__v001
```

## Governance Status

Phase 4ad rules apply prospectively to future Phase 4ae-equivalent substrate-feasibility analysis only.

Phase 4ad does not modify Phase 4ac manifests.

Phase 4ad does not flip any Phase 4ac `research_eligible` flag.

Phase 4ad does not revise any retained verdict.

Phase 4ad does not change any project lock.

Phase 4ad does not broaden Phase 4ac results into binding cross-project governance.

Phase 4ad does not adopt Phase 4z recommendations as binding governance.

Phase 4ad does not adopt the Phase 4aa admissibility framework as binding governance.

Phase 4ad does not adopt Phase 4ab recommendations as binding governance.

## Boundary Confirmation

This merge did not start:

- Phase 4ae;
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
- any backtest;
- any diagnostic;
- Q1–Q7 rerun;
- substrate-feasibility execution;
- cost-to-volatility calculations;
- ATR / median range calculations;
- expansion-event calculations;
- trend-regime calculations;
- wick / stop-pathology calculations;
- funding-rate distribution calculations;
- volume / notional turnover calculations;
- common-overlap coverage tables;
- event-count sufficiency summaries;
- cross-symbol descriptive comparisons;
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
- Phase 4ac results remain data / integrity evidence only except for Phase 4ad future-use scope rules.

## Final Recommended State

After this merge, the recommended state is:

```text
remain paused unless the operator separately authorizes a future phase
```

Phase 4ad's conditional next recommendation is a future docs-only Phase 4ae substrate-feasibility analysis memo.

Phase 4ae is not authorized by this merge.

No next phase is authorized by this merge.
