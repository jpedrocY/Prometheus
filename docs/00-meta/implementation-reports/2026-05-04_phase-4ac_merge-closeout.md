# Phase 4ac Merge Closeout — Alt-Symbol Public Data Acquisition and Integrity Validation

## Purpose

This document records the no-fast-forward merge of completed Phase 4ac into `main`.

This is a merge closeout only. It does not authorize Phase 4ad, backtests, diagnostics, strategy work, implementation, paper/shadow, live-readiness, or exchange-write.

## Merge Summary

- Phase 4ac title: Alt-Symbol Public Data Acquisition and Integrity Validation
- Merge branch: `phase-4ac/alt-symbol-public-data-acquisition`
- Target branch: `main`
- Main before merge: `9db120741413ec9cb5b02ffd9622d0f43a1d8c57`
- Phase 4ac commit: `e3018a9c085deab04432f3df039933bc487d340b`
- Merge method: `--no-ff`

## Files Brought Forward From Phase 4ac

Phase 4ac was docs-and-data acquisition / integrity validation only.

Phase 4ac created:

- `scripts/phase4ac_alt_symbol_acquisition.py`
- `docs/00-meta/implementation-reports/2026-05-04_phase-4ac_alt-symbol-public-data-acquisition.md`
- `docs/00-meta/implementation-reports/2026-05-04_phase-4ac_closeout.md`
- 35 new manifests under `data/manifests/`

This merge closeout created:

- `docs/00-meta/implementation-reports/2026-05-04_phase-4ac_merge-closeout.md`

This merge also updated narrowly:

- `docs/00-meta/current-project-state.md`

## Phase 4ac Summary

Phase 4ac acquired the predeclared Phase 4ab core alt-symbol public datasets from public unauthenticated `data.binance.vision` bulk archives only.

Core symbol set:

```text
BTCUSDT
ETHUSDT
SOLUSDT
XRPUSDT
ADAUSDT
```

Deferred secondary watchlist not acquired:

```text
BNBUSDT
DOGEUSDT
LINKUSDT
AVAXUSDT
```

Phase 4ac acquired 35 dataset families, covering 52 monthly archives each, for a total of:

```text
1,820 monthly archives
```

All 1,820 archives were SHA256-verified against `.CHECKSUM` companions with zero mismatches.

Phase 4ac committed 35 manifests:

- 9 datasets with `research_eligible: true`
- 26 datasets with `research_eligible: false`

Research-eligible true datasets:

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

Research-eligible false datasets include:

- BTCUSDT / ETHUSDT mark-price 30m / 1h / 4h datasets with known upstream mark-price gaps.
- SOLUSDT / XRPUSDT trade-price klines at 15m / 30m / 1h / 4h due to early-2022 archive gaps.
- SOLUSDT / XRPUSDT / ADAUSDT mark-price klines at 15m / 30m / 1h / 4h due to upstream mark-price gaps.

Invalid windows were recorded verbatim in the affected manifests. No patching, forward-fill, interpolation, imputation, synthesis, replacement, or silent omission occurred.

## Governance Status

Phase 4ac results are data / integrity evidence only.

Phase 4ac does not adopt Phase 4z recommendations as binding governance.

Phase 4ac does not adopt the Phase 4aa admissibility framework as binding governance.

Phase 4ac does not adopt Phase 4ab recommendations as binding governance.

Phase 4ac does not convert its own data/integrity results or recommendations into binding project governance.

Any future governance decision, including any SOL/XRP early-2022 kline-gap exclusion rule or mark-price partial-eligibility rule, requires separate operator authorization.

## Boundary Confirmation

This merge did not start:

- Phase 4ad;
- Phase 5;
- Phase 4 canonical;
- any successor phase;
- new data acquisition;
- new data download;
- new API call;
- new endpoint call;
- data modification;
- manifest modification beyond bringing forward Phase 4ac-created manifests;
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

- source code under `src/prometheus/`;
- tests;
- existing scripts;
- existing manifests;
- raw data;
- normalized data;
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

## Final Recommended State

After this merge, the recommended state is:

```text
remain paused unless the operator separately authorizes a future phase
```

Phase 4ac's conditional next recommendation is a future docs-only Phase 4ad gap-governance / scope-revision memo, or a docs-only Phase 4ad-B PASS-subset substrate-feasibility analysis memo.

Phase 4ad is not authorized by this merge.

No next phase is authorized by this merge.
