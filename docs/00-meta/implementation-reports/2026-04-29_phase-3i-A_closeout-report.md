# Phase 3i-A — Closeout Report

**Phase:** 3i-A — D1-A implementation-control phase. Adds primitives, locked config, validation surface, and strategy-family scaffolding while keeping D1-A deliberately non-runnable; proves the new code surface does not perturb existing V1 / R3 / F1 behavior via bit-for-bit control reproduction.

**Branch:** `phase-3i-a/d1a-implementation-controls`.

**Date:** 2026-04-29 UTC.

---

## 1. Current branch

`phase-3i-a/d1a-implementation-controls`, created from `main` at `ca3810cbf7c04407b5e82bf38ef1a28b03d9eafd` (Phase 3h merge-report commit).

## 2. Git status

Working tree clean after the Phase 3i-A commit. No untracked files. No `data/` files staged or tracked.

## 3. Files changed

New files (D1-A package and tests):

- `src/prometheus/strategy/funding_aware_directional/__init__.py`
- `src/prometheus/strategy/funding_aware_directional/variant_config.py`
- `src/prometheus/strategy/funding_aware_directional/primitives.py`
- `src/prometheus/strategy/funding_aware_directional/strategy.py`
- `tests/unit/strategy/funding_aware_directional/__init__.py`
- `tests/unit/strategy/funding_aware_directional/test_variant_config.py`
- `tests/unit/strategy/funding_aware_directional/test_primitives.py`
- `tests/unit/strategy/funding_aware_directional/test_strategy.py`
- `tests/unit/research/backtest/test_engine_d1a_guard.py`

Modified files (engine + config validator):

- `src/prometheus/research/backtest/config.py` — `StrategyFamily.FUNDING_AWARE_DIRECTIONAL` enum; `funding_aware_variant` field; extended `_check` validator.
- `src/prometheus/research/backtest/engine.py` — D1-A dispatch guard at top of `BacktestEngine.run` raising `RuntimeError("D1-A engine wiring not yet authorized; see Phase 3i-B1.")`.
- `tests/unit/research/backtest/test_config.py` — 8 D1-A dispatch validation tests.

New documentation files:

- `docs/00-meta/implementation-reports/2026-04-29_phase-3i-A_D1A_implementation-controls.md` (checkpoint report)
- `docs/00-meta/implementation-reports/2026-04-29_phase-3i-A_closeout-report.md` (this file)

## 4. Commit hash(es)

Single Phase 3i-A commit on `phase-3i-a/d1a-implementation-controls`:

- `6c61b47` — `phase-3i-A: D1-A implementation controls (non-runnable scaffolding)` (14 files, +2149 / −8; 8 new files, 6 modified files; all Phase 3i-A deliverables landed in one commit).

The Phase 3i-A commit message references all changed files and explicitly preserves the Phase 3h + Phase 3g + Phase 3f + Phase 3e + Phase 3d-B2 + Phase 2y + Phase 2x + §1.7.3 / §10.3 / §10.4 / §11.3 / §11.4 / §11.6 = 8 bps HIGH per side discipline. No subsequent commit is added by Phase 3i-A itself; an operator-authorized merge into `main` would add a separate `--no-ff` merge commit (and an optional follow-on merge-report commit modeled on Phase 3h's pattern).

## 5. Confirmation that Phase 3i-A was implementation-control only

Confirmed. Phase 3i-A added the D1-A implementation surface (primitives + locked config + strategy facade + dispatch validation + engine guard) and the corresponding unit tests. It did NOT implement the D1-A engine path, run any D1-A backtest, generate the derived `funding_aware_features__v001` dataset, compute M1/M2/M3 mechanism checks on real data, or evaluate the first-execution gate. The phase is bounded strictly to "implementation surface + non-runnability proof + bit-for-bit control reproduction".

## 6. Confirmation that D1-A remains deliberately non-runnable

Confirmed. `BacktestEngine.run` raises `RuntimeError("D1-A engine wiring not yet authorized; see Phase 3i-B1.")` when `strategy_family == FUNDING_AWARE_DIRECTIONAL`. The guard is verified by `tests/unit/research/backtest/test_engine_d1a_guard.py::test_d1a_dispatch_raises_runtime_error`. V1 default and F1 dispatch paths remain unchanged (verified by `test_v1_breakout_dispatch_unchanged_by_d1a_guard` and `test_f1_dispatch_unchanged_by_d1a_guard`).

## 7. Confirmation that no D1-A backtests, diagnostics, first-execution gate, or V-window were run

Confirmed. The only backtests executed during Phase 3i-A were the three control re-runs:

- H0 R MED MARK (BTC + ETH) — bit-for-bit identical to prior baseline.
- R3 R MED MARK (BTC + ETH) — bit-for-bit identical to prior baseline.
- F1 R MED MARK (BTC + ETH) — bit-for-bit identical to prior baseline.

No D1-A R MED, R LOW, R HIGH, R MED TRADE_PRICE, V MED, V LOW, V HIGH, or V TRADE_PRICE cell was executed. No D1-A first-execution gate was evaluated. No D1-A M1 / M2 / M3 mechanism check was computed on real data. No derived `funding_aware_features__v001` dataset was generated.

## 8. Confirmation that no `data/` artifacts were committed

Confirmed. `git status` after the Phase 3i-A commit shows zero `data/` entries. Control re-run outputs landed under existing git-ignored `data/derived/backtests/phase-2l-h0-r/`, `data/derived/backtests/phase-2l-r3-r/`, and `data/derived/backtests/phase-3d-f1-window=r-slip=medium/` directories — none of which are tracked.

## 9. Confirmation of preserved scope

| Category | Status |
|----------|--------|
| Source code outside the D1-A package + minimal config/engine extensions | UNCHANGED |
| `src/prometheus/strategy/v1_breakout/**` | UNCHANGED |
| `src/prometheus/strategy/mean_reversion_overextension/**` | UNCHANGED |
| `src/prometheus/research/backtest/trade_log.py` | UNCHANGED (D1-A field additions deferred to Phase 3i-B1) |
| `src/prometheus/research/backtest/accounting.py`, `fills.py`, `funding_join.py`, `simulation_clock.py`, `sizing.py`, `stops.py` | UNCHANGED |
| Scripts (`scripts/**`) | UNCHANGED (no D1-A runner; no D1-A analysis script) |
| `.claude/` directory | UNCHANGED |
| `.mcp.json` | NOT CREATED, NOT MODIFIED |
| MCP servers / Graphify | NOT ACTIVATED |
| Credentials / `.env` / API keys | NOT REQUESTED, NOT CREATED, NOT MODIFIED |
| Production / sandbox / testnet keys | NONE EXIST, NONE PROPOSED |
| Exchange-write paths | NOT PROPOSED, NOT ENABLED |
| `data/` directory | UNCHANGED, NO COMMITS |
| Phase 2f thresholds (§10.3 / §10.4 / §11.3 / §11.4) | PRESERVED VERBATIM |
| **§11.6 = 8 bps HIGH per side** | PRESERVED VERBATIM |
| §1.7.3 project-level locks | PRESERVED VERBATIM |
| H0 / R3 / R1a / R1b-narrow / R2 / F1 sub-parameters | PRESERVED VERBATIM |
| **D1-A locked spec values** (Phase 3g binding) | PRESERVED VERBATIM in `FundingAwareConfig` (single source of truth) |
| R3 baseline-of-record status (Phase 2p §C.1) | PRESERVED |
| H0 framework anchor status (Phase 2i §1.7.3) | PRESERVED |
| R1a / R1b-narrow / R2 / F1 retained-research-evidence status | PRESERVED |
| R2 framework verdict (FAILED — §11.6 cost-sensitivity blocks) | PRESERVED |
| F1 framework verdict (HARD REJECT) | PRESERVED |
| Phase 3d-B2 terminal-for-F1 status | PRESERVED |
| Paper/shadow planning | NOT AUTHORIZED, NOT PROPOSED |
| Phase 4 (runtime / state / persistence) work | NOT AUTHORIZED, NOT PROPOSED |
| Live-readiness / deployment / production-key / exchange-write work | NOT AUTHORIZED, NOT PROPOSED |
| Existing strategy / validation / cost / data / phase-gate / ai-coding-handoff / current-project-state specs | UNCHANGED |
| `docs/12-roadmap/technical-debt-register.md` | UNCHANGED |
| `docs/00-meta/implementation-ambiguity-log.md` | UNCHANGED |
| `docs/00-meta/current-project-state.md` | UNCHANGED |
| `docs/00-meta/ai-coding-handoff.md` | UNCHANGED |

No threshold, strategy parameter (outside the Phase 3g D1-A locked spec which is consumed unmodified), project lock, paper/shadow plan, Phase 4 work, live-readiness work, deployment work, MCP server, Graphify integration, `.mcp.json` change, credential creation, or exchange-write authorization occurred in Phase 3i-A.

## 10. Branch ready for operator review and possible merge

**YES.** All four quality gates green; H0 / R3 / F1 R MED MARK controls reproduce bit-for-bit on every summary metric; D1-A is deliberately non-runnable through the engine via the documented `RuntimeError` guard; ~78 new unit tests pass; total `pytest` count 645 passed (up from 567 at Phase 3d-B2 baseline). The Phase 3i-A D1A implementation-controls checkpoint report (`docs/00-meta/implementation-reports/2026-04-29_phase-3i-A_D1A_implementation-controls.md`) recommends Phase 3i-B1 is **safe to consider** after operator review.

If the operator approves Phase 3i-A:

- The branch may be merged into `main` with `--no-ff` per the Phase 3d-B2 / Phase 3e / Phase 3f / Phase 3g / Phase 3h merge-pattern precedent.
- A merge-report commit may follow, modeled on `docs/00-meta/implementation-reports/2026-04-28_phase-3h_merge-report.md`.
- The recommended next operator decision is **authorize Phase 3i-B1** (engine wiring + lifecycle counters + output fields + runner scaffold + full 9-cell control reproduction) per Phase 3h §6.2 and Phase 3i-A §16.

If the operator does not approve Phase 3i-A or prefers a different framing, the branch may be discarded without affecting `main` (Phase 3h merge stands; project state remains at `ca3810c`).

Phase 3i-A does NOT recommend implementation of the D1-A engine path, backtesting, paper/shadow, Phase 4, live-readiness, deployment, F1-prime / target-subset rescue, D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, threshold revision, or §1.7.3 lock revision. Awaiting operator review.

---

**End of Phase 3i-A closeout report.**
