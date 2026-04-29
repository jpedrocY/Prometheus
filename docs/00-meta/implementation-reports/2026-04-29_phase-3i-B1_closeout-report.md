# Phase 3i-B1 — Closeout Report

**Phase:** 3i-B1 — D1-A engine-wiring control phase. Lifts the Phase 3i-A guard, wires D1-A into the backtest engine (per-bar lifecycle, lifecycle counters, output fields, runner scaffold), proves H0 / R3 / F1 controls reproduce bit-for-bit, and adds extensive synthetic D1-A engine tests — without running any D1-A candidate backtest or evaluating the first-execution gate.

**Branch:** `phase-3i-b1/d1a-engine-wiring-controls`.

**Date:** 2026-04-29 UTC.

---

## 1. Current branch

`phase-3i-b1/d1a-engine-wiring-controls`, created from `main` at `4dc15a9a548f472e3246461422b65f7f91c4832c` (Phase 3i-A merge-report commit).

## 2. Git status

Working tree clean after the Phase 3i-B1 commit. No untracked files. No `data/` files staged or tracked.

## 3. Files changed

Modified:

- `src/prometheus/research/backtest/engine.py` — D1-A engine wiring: `_run_symbol_d1a` + `_open_d1a_trade` + close helpers; `_D1ATradeMetadata`; `FundingAwareLifecycleCounters`; `_OpenTrade.d1a_metadata`; `_SymbolRun` D1-A state; `BacktestRunResult.funding_aware_counters_per_symbol`; lifted Phase 3i-A guard; D1-A dispatch in `run()`. V1 / F1 paths unchanged (controls bit-for-bit).
- `src/prometheus/research/backtest/trade_log.py` — 4 new D1-A `TradeRecord` fields with None / NaN / -1 defaults; parquet schema extension.
- `tests/unit/research/backtest/test_engine_d1a_guard.py` — replaced Phase 3i-A guard-raising tests with Phase 3i-B1 dispatch tests.
- `tests/unit/research/backtest/test_trade_log.py` — extended parquet schema assertion to include 4 new D1-A column names.

New files:

- `scripts/phase3j_D1A_execution.py` — Phase 3j D1-A execution runner scaffold (guarded by `--phase-3j-authorized`; fails closed without it; `check-imports` subcommand safe).
- `tests/unit/research/backtest/test_engine_d1a_dispatch.py` — comprehensive D1-A engine dispatch tests (21 tests).
- `docs/00-meta/implementation-reports/2026-04-29_phase-3i-B1_D1A_engine-wiring-controls.md` — checkpoint report.
- `docs/00-meta/implementation-reports/2026-04-29_phase-3i-B1_closeout-report.md` — this file.

## 4. Commit hash(es)

To be recorded after the Phase 3i-B1 commit lands. The Phase 3i-B1 commit message references all changed files and explicitly preserves the Phase 3i-A + Phase 3h + Phase 3g + Phase 3f + Phase 3e + Phase 3d-B2 + Phase 2y + Phase 2x + §1.7.3 / §10.3 / §10.4 / §11.3 / §11.4 / §11.6 = 8 bps HIGH per side discipline.

## 5. Confirmation that Phase 3i-B1 was engine-wiring-control only

Confirmed. Phase 3i-B1 wired the D1-A engine dispatch path, added lifecycle counters and output fields, and added a guarded runner scaffold. It did NOT run any D1-A candidate backtest on real data, evaluate the first-execution gate, compute M1/M2/M3 mechanism checks, or generate the `funding_aware_features__v001` derived dataset. The phase is bounded strictly to "engine wiring + non-runnability of candidate runs + bit-for-bit control reproduction".

## 6. Confirmation that D1-A is now engine-wired but candidate runs were not executed

Confirmed. The Phase 3i-A `RuntimeError` guard at the top of `BacktestEngine.run` is lifted. D1-A dispatches through `_run_symbol_d1a` when `strategy_family == FUNDING_AWARE_DIRECTIONAL`. The dispatch path is exercised by the 21 synthetic engine tests in `test_engine_d1a_dispatch.py` (all passing). However, no D1-A candidate backtest was run on the real v002 dataset. The runner scaffold `scripts/phase3j_D1A_execution.py` requires `--phase-3j-authorized` to proceed AND has a second-gate "run-loop not yet implemented" exit even with the flag — preventing accidental D1-A candidate execution under Phase 3i-B1.

## 7. Confirmation that no D1-A diagnostics, first-execution gate, or V-window were run

Confirmed. The only backtests executed during Phase 3i-B1 were the 5 control re-runs (H0 R/V, R3 R/V, F1 R) for bit-for-bit reproduction verification. None of these are D1-A. No D1-A first-execution gate was evaluated. No D1-A M1 / M2 / M3 mechanism check was computed on real data. No D1-A diagnostic output was produced. No D1-A V-window cell was executed.

## 8. Confirmation that no `data/` artifacts were committed

Confirmed. `git status` after the Phase 3i-B1 commit shows zero `data/` entries. Control re-run outputs landed under existing git-ignored `data/derived/backtests/phase-2l-h0-r/`, `phase-2l-h0-v/`, `phase-2l-r3-r/`, `phase-2l-r3-v/`, and `phase-3d-f1-window=r-slip=medium/` directories — none of which are tracked.

## 9. Confirmation of preserved scope

| Category | Status |
|----------|--------|
| Phase 2f thresholds (§10.3 / §10.4 / §11.3 / §11.4) | PRESERVED VERBATIM |
| **§11.6 = 8 bps HIGH per side** | PRESERVED VERBATIM (Phase 2y closeout) |
| §1.7.3 project-level locks | PRESERVED VERBATIM |
| H0 / R3 / R1a / R1b-narrow / R2 / F1 sub-parameters | PRESERVED VERBATIM (controls bit-for-bit) |
| **D1-A locked spec values** (Phase 3g binding) | PRESERVED VERBATIM in `FundingAwareConfig`; consumed unmodified by the engine |
| R3 baseline-of-record status (Phase 2p §C.1) | PRESERVED |
| H0 framework anchor status (Phase 2i §1.7.3) | PRESERVED |
| R1a / R1b-narrow / R2 / F1 retained-research-evidence status | PRESERVED |
| R2 framework verdict (FAILED — §11.6 cost-sensitivity blocks) | PRESERVED |
| F1 framework verdict (HARD REJECT) | PRESERVED |
| Phase 3d-B2 terminal-for-F1 status | PRESERVED |
| Paper/shadow planning | NOT AUTHORIZED, NOT PROPOSED |
| Phase 4 (runtime / state / persistence) work | NOT AUTHORIZED, NOT PROPOSED |
| Live-readiness / deployment / production-key / exchange-write work | NOT AUTHORIZED, NOT PROPOSED |
| MCP servers / Graphify / `.mcp.json` | NOT ACTIVATED, NOT TOUCHED |
| Credentials / `.env` / API keys | NOT REQUESTED, NOT CREATED, NOT TOUCHED |
| `src/prometheus/strategy/v1_breakout/**` | UNCHANGED |
| `src/prometheus/strategy/mean_reversion_overextension/**` | UNCHANGED |
| `src/prometheus/strategy/funding_aware_directional/**` | UNCHANGED (Phase 3i-A primitives + config + facade still binding) |
| `src/prometheus/research/backtest/config.py` | UNCHANGED (Phase 3i-A validator already wired) |
| `src/prometheus/research/backtest/accounting.py`, `fills.py`, `funding_join.py`, `simulation_clock.py`, `sizing.py`, `stops.py` | UNCHANGED |
| `src/prometheus/research/backtest/report.py` | UNCHANGED (Phase 3j runner will extend if/when authorized) |
| `.claude/` directory | UNCHANGED |
| `data/` directory | UNCHANGED, NO COMMITS |

No threshold, project lock, paper/shadow plan, Phase 4 work, live-readiness work, deployment work, MCP server, Graphify integration, `.mcp.json` change, credential creation, or exchange-write authorization occurred in Phase 3i-B1.

## 10. Branch ready for operator review and possible merge

**YES.** All four quality gates green; full 9-cell H0 / R3 / F1 controls reproduce bit-for-bit on every summary metric; D1-A engine path is implemented and tested via 21 synthetic engine tests; lifecycle event-level identity enforced; runner scaffold double-gated; no D1-A candidate backtest run; no D1-A diagnostics computed; no derived dataset generated; D1-A locked spec preserved verbatim per Phase 3g binding. The Phase 3i-B1 D1A engine-wiring-controls checkpoint report (`docs/00-meta/implementation-reports/2026-04-29_phase-3i-B1_D1A_engine-wiring-controls.md`) recommends Phase 3j is **safe to consider** after operator review.

If the operator approves Phase 3i-B1:

- The branch may be merged into `main` with `--no-ff` per the prior phase merge-pattern precedent.
- A merge-report commit may follow, modeled on Phase 3i-A's merge report.
- The recommended next operator decision is **authorize Phase 3j** (D1-A candidate runs + diagnostics + first-execution gate evaluation), per Phase 3h §6.3 and Phase 3i-B1 §18. Phase 3j requires its own separately-authorized operator decision.

If the operator does not approve Phase 3i-B1 or prefers a different framing, the branch may be discarded without affecting `main` (Phase 3i-A merge stands; project state remains at `4dc15a9`).

Phase 3i-B1 does NOT recommend Phase 3j authorization itself, paper/shadow, Phase 4, live-readiness, deployment, F1-prime / target-subset rescue, D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, threshold revision, or §1.7.3 lock revision. Awaiting operator review.

---

**End of Phase 3i-B1 closeout report.**
