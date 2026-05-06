# Phase 4an Merge Closeout — Historical Trade-Population Exit-Path Inventory Memo

## Purpose

This document records the no-fast-forward merge of completed Phase 4an
into `main`.

This is a merge closeout only. It does not authorize Phase 4ao, data
acquisition, analysis execution, backtests, strategy diagnostics,
fresh-hypothesis discovery, strategy work, implementation, paper / shadow,
live-readiness, or exchange-write.

## Merge Summary

- Phase 4an title: Historical Trade-Population Exit-Path Inventory Memo
- Merge branch: `phase-4an/historical-trade-population-exit-path-inventory`
- Target branch: `main`
- Main before merge: `dfaa26a4e7f9a21957e0e465c7bb7de2e508a784`
- Phase 4an commit (memo): `241d6a71bec61457a8b876572989d7550a9f1423`
- Phase 4an commit (closeout): `13f519bf874965154b00b7be8f3ca086ffd00da5`
- Merge method: `--no-ff`
- Merge commit SHA: `bf3643c5e6b04255e6ed19a074526332d5f35a5c`

## Files Brought Forward From Phase 4an

Phase 4an was docs-only.

Phase 4an created:

- `docs/00-meta/implementation-reports/2026-05-06_phase-4an_historical-trade-population-exit-path-inventory.md`
- `docs/00-meta/implementation-reports/2026-05-06_phase-4an_closeout.md`

This merge closeout created:

- `docs/00-meta/implementation-reports/2026-05-06_phase-4an_merge-closeout.md`

This merge also updated narrowly:

- `docs/00-meta/current-project-state.md`

(The `current-project-state.md` update was performed in the Phase 4an memo
commit `241d6a7` on the phase branch and is brought forward by this merge;
the merge-closeout commit itself does not further modify
`current-project-state.md`.)

## Phase 4an Summary

Phase 4an performed a docs-only static repository inventory of which
historical Prometheus strategy / research populations have sufficient
artefacts to support possible future MFE / MAE, realized-R, exit-path,
stop-path, take-profit, and winner / loser path forensic analysis.

Phase 4an examined ten historical strategy / research populations plus the
closed 5m thread:

```text
H0
R3
R1a
R1b-narrow
R2
F1
D1-A
V2
G1
C1
5m research thread (closed historical context only)
```

Phase 4an methodology was strictly static repository inspection: read
trade-log JSON / Parquet schema fields by inspecting representative files,
read the backtest engine source
(`src/prometheus/research/backtest/`) to determine which strategies
populate `mfe_r` / `mae_r` versus default to `0.0`, read strategy modules
to determine excursion-tracking presence, read standalone research scripts
(`scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`,
`scripts/phase4x_c1_backtest.py`) to determine in-memory MFE / MAE tracking
and persistence behaviour, and read directory listings under
`data/derived/backtests/` and `data/research/phase4l/`,
`data/research/phase4r/`, `data/research/phase4x/`.

No script was run during Phase 4an. No backtest was executed. No data was
modified. No retained verdict was revised. No project lock was changed.

## Inventory Result

- **H0, R3, R1a, R1b-narrow, R2** — `RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS`.
  Local `trade_log_v1` artefacts (gitignored under
  `data/derived/backtests/`) contain `mfe_r` / `mae_r` populated from 15m
  bar excursion via `TradeManagement._update_excursions`, plus all
  realized-R / cost / timing / exit-reason fields. Per-cost-cell variants
  (LOW / MEDIUM / HIGH) and trade-price stop-domain variants exist for
  retained-evidence runs. No rerun is required for first-pass forensics.

- **F1 (Phase 3d-B2), D1-A (Phase 3j)** — `RECONSTRUCTABLE_ONLY_WITH_RERUN`
  for MFE / MAE; `RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS` for
  non-excursion fields. Local `trade_log_v1` artefacts have schema parity
  with V1-arc and all non-excursion fields populated, but `mfe_r` and
  `mae_r` are uniformly `0.0` because the F1
  (`src/prometheus/strategy/mean_reversion_overextension/`) and D1-A
  (`src/prometheus/strategy/funding_aware_directional/`) strategy modules
  contain no excursion-tracking code; engine line 1139–1140 returns `0.0`
  defaults when `active.management is None`. Recovery would require
  controlled rerun under script modification OR offline 15m-join
  reconstruction over each trade's `entry_fill_time_ms` →
  `exit_fill_time_ms` window using v002 BTCUSDT / ETHUSDT 15m bars.

- **V2 (Phase 4l), G1 (Phase 4r), C1 (Phase 4x)** —
  `RECONSTRUCTABLE_ONLY_WITH_RERUN`. The standalone research scripts emit
  aggregate variant-level CSVs only under `data/research/phase4l/`,
  `data/research/phase4r/`, `data/research/phase4x/`. No per-trade ledger
  is persisted. V2 in-memory tracks `mfe_R` (using 30m bar high / low at
  `phase4l_v2_backtest.py:1224–1226`) but does not persist it per-trade
  and does not track MAE; G1 and C1 do not track MFE / MAE in memory at
  all. Reconstruction requires rerun under script modification, which is
  governance-bounded by Phase 4z / Phase 4m / Phase 4s / Phase 4y
  forbidden-rescue lists.

- **5m research thread** — `CLOSED_CONTEXT_ONLY`. Phase 3o → 3t
  diagnostic-only thread; no strategy ledger ever produced; operationally
  CLOSED per Phase 3t. Phase 4an does NOT reopen it.

Forbidden-rescue-risk profile (per the Phase 4al §9 refined no-rescue
rule and the cumulative Phase 4z / Phase 4m / Phase 4s / Phase 4y
forbidden-rescue lists):

- **MEDIUM**: H0, R3.
- **HIGH**: R1a, R1b-narrow.
- **CRITICAL**: R2, F1, D1-A, V2, G1, C1, 5m thread.

Mark-price path forensics is BLOCKED under §1.7.3 stop-trigger-domain
governance and Phase 3v §8 for live-readiness; Phase 3s Q6 D1-A finding
remains descriptive only.

Lower-timeframe sufficiency for first-pass forensics: 15m / 30m / 1h / 4h
is sufficient for V1-arc and (via offline reconstruction or rerun) for
F1 / D1-A; 5m optional only under Phase 4al §14 if a forensic question
exposes intra-bar sequencing ambiguity; 1m only escalates if 5m exceeds
Phase 4al §14.C >10% / >20% bands; aggTrades / tick remains final
escalation. No lower-timeframe data was acquired by Phase 4an.

Open questions recorded but not answered: OQ-A through OQ-E (per Phase
4an memo §15).

## Governance Status After Merge

- **M0 mechanism-admissibility gate (Phase 4ak)**: unchanged.
- **All twelve M0 clauses M0.1–M0.12**: unchanged.
- **Post-null cooldown rule**: unchanged.
- **Cooled-down families list**: unchanged.
- **Phase 4al refined no-rescue rule**: preserved.
- **Phase 4al §13 future-Phase-4am-style boundary specification**: preserved.
- **Phase 4al §14 data-resolution hierarchy**: preserved.
- **Phase 4am §11.A audit findings (F-1 / F-2 / F-3 / F-4)**: preserved as
  documentation for future methodology-harmonization scoping.
- **Phase 4an inventory result**: recorded in repository as docs-only
  evidence.

## Phase 4an Recommendation (preserved at merge)

Phase 4an primary recommendation:

```text
remain paused.
```

Phase 4an conditional secondary (NOT authorized by Phase 4an or by this
merge):

```text
narrower future docs-only methodology / artefact harmonization memo.
Resolves OQ-C / OQ-D before any computation; does not itself authorize
computation.
```

Phase 4an conditional tertiary (NOT authorized by Phase 4an or by this
merge):

```text
future full exit-path forensic plan only after harmonization, restricted
to V1-arc populations, under Phase 4al §13 boundaries.
```

Phase 4ao is not started or authorized by this merge.

## Boundary Confirmation

This merge did not start:

- Phase 4ao;
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
- any backtest;
- any strategy diagnostic;
- Q1–Q7 rerun;
- strategy PnL calculation;
- entry / exit strategy-return calculation;
- MFE / MAE / time-to-MFE / time-to-stop / target-before-stop /
  realized-R-after-costs distribution computation;
- offline 15m-join MFE / MAE reconstruction;
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
- R3-prime / R1a-prime / R1b-narrow-prime / R2-prime / F1-prime /
  D1-A-prime / D1-B / V2-prime / V2-narrow / V2-relaxed / V2 hybrid /
  G1-prime / G1-narrow / G1-extension / G1 hybrid / C1-prime / C1-narrow /
  C1-extension / C1 hybrid;
- V1-D1 / F1-D1 / any cross-strategy hybrid;
- old-strategy alt-symbol reruns;
- multi-position portfolio trading;
- 5m strategy or reopening of the 5m research thread;
- 5m / 1m / aggTrades / tick / mark-price 30m / 4h data acquisition;
- paper / shadow;
- live-readiness;
- deployment;
- production-key creation;
- authenticated APIs;
- private endpoints;
- public endpoint calls in code;
- user stream;
- WebSocket;
- listenKey;
- exchange-write;
- MCP;
- Graphify;
- `.mcp.json`;
- credentials.

This merge did not modify:

- source code under `src/prometheus/`;
- tests under `tests/`;
- scripts under `scripts/`;
- raw data under `data/raw/`;
- normalized data under `data/normalized/`;
- derived data under `data/derived/`;
- research data under `data/research/`;
- manifests under `data/manifests/`;
- runtime implementation;
- existing strategy specifications;
- project locks;
- retained verdicts;
- M0 governance text (`docs/00-meta/m0-mechanism-admissibility-gate.md`);
- specialist governance files except for the narrow current-project-state
  update brought forward from the Phase 4an memo commit.

## Retained Verdict Ledger

Retained verdicts remain unchanged:

- H0 remains FRAMEWORK ANCHOR.
- R3 remains BASELINE-OF-RECORD.
- R1a remains RETAINED — NON-LEADING.
- R1b-narrow remains RETAINED — NON-LEADING.
- R2 remains FAILED — §11.6.
- F1 remains HARD REJECT.
- D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other.
- 5m research thread remains operationally CLOSED per Phase 3t.
- V2 remains HARD REJECT — terminal for V2 first-spec.
- G1 remains HARD REJECT — terminal for G1 first-spec.
- C1 remains HARD REJECT — terminal for C1 first-spec.

No retained verdicts were revised.

## Project Locks

Project locks remain unchanged:

- §11.6 HIGH cost = 8 bps per side; round-trip = 16 bps slippage; taker
  fee = 4 bps per side; no maker rebates; no live fee assumption.
- §1.7.3 project-level locks:
  - 0.25% risk per trade;
  - 2× leverage cap;
  - one position max;
  - mark-price stops where applicable.
- Phase 3r §8 mark-price gap governance preserved.
- Phase 3v §8 stop-trigger-domain governance preserved.
- Phase 3w §6 / §7 / §8 break-even / EMA-slope / stagnation governance
  preserved.
- Phase 4j §11 metrics OI-subset partial-eligibility rule preserved.
- Phase 4k V2 backtest-plan methodology preserved.
- Phase 4p G1 strategy-spec memo preserved.
- Phase 4q G1 backtest-plan methodology preserved.
- Phase 4v C1 strategy-spec memo preserved.
- Phase 4w C1 backtest-plan methodology preserved.
- Phase 4ak twelve-clause M0 mechanism-admissibility gate preserved.
- Phase 4ak post-null cooldown rule preserved.
- Phase 4ak cooled-down families list preserved.
- Phase 4al refined no-rescue rule preserved.
- Phase 4al §13 boundary specification preserved.
- Phase 4al §14 data-resolution hierarchy preserved.
- Phase 4am §11.A audit findings (F-1 / F-2 / F-3 / F-4) preserved.

## Final Recommended State

After this merge, the recommended state is:

```text
remain paused unless the operator separately authorizes a future phase
```

Phase 4an does not recommend immediate forensic computation.

Phase 4an does not recommend immediate strategy work.

Phase 4an does not authorize Phase 4ao.

No next phase is authorized by this merge.
