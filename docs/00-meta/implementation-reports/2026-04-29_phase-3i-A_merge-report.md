# Phase 3i-A — Merge Report

**Phase:** 3i-A — D1-A implementation-control phase merged into `main`. Adds primitives, locked config, validation surface, and strategy-family scaffolding while keeping D1-A deliberately non-runnable; proves the new code surface does not perturb existing V1 / R3 / F1 behavior via bit-for-bit control reproduction.

**Date:** 2026-04-29 UTC.

---

## 1. Phase 3i-A branch tip SHA before merge

`e481a88c5329a50272ae5c3520418fec558bb112` on `phase-3i-a/d1a-implementation-controls`.

The branch contained three commits ahead of `main` at merge time:

- `6c61b47` — `phase-3i-A: D1-A implementation controls (non-runnable scaffolding)` — original Phase 3i-A commit (14 files, +2149 / −8).
- `acd6f43` — `phase-3i-A: record commit hash 6c61b47 in closeout report` — closeout commit-hash backfill (1 file, +5 / −1).
- `e481a88` — `phase-3i-A: report consistency cleanup -- nine helpers + 78 tests` — post-review docs-only cleanup of two report wording inconsistencies (2 files, +11 / −11).

## 2. Merge commit hash

`8ba58a4421f0ea189890fc6a58e5dda5cf11de25`.

Created by `git merge --no-ff phase-3i-a/d1a-implementation-controls` from `main` at `ca3810cbf7c04407b5e82bf38ef1a28b03d9eafd` (pre-merge). Merge produced by the `ort` strategy. 14 files changed; 2153 insertions; 8 deletions; 10 new files.

## 3. Merge-report commit hash

To be recorded after this merge-report file is committed to `main` and pushed. The merge-report commit appends this Markdown file under `docs/00-meta/implementation-reports/` and changes nothing else.

## 4. Main / origin sync confirmation

Local `main` and `origin/main` are synced at the merge commit:

```text
local  main         8ba58a4421f0ea189890fc6a58e5dda5cf11de25
origin/main         8ba58a4421f0ea189890fc6a58e5dda5cf11de25
```

Push completed cleanly: `ca3810c..8ba58a4  main -> main`.

## 5. Git status

Working tree clean immediately after the merge and push. No untracked files. No staged changes. No `data/` artifacts staged or tracked.

## 6. Latest 5 commits

```text
8ba58a4 Merge Phase 3i-A (D1-A implementation controls -- non-runnable scaffolding) into main
e481a88 phase-3i-A: report consistency cleanup -- nine helpers + 78 tests
acd6f43 phase-3i-A: record commit hash 6c61b47 in closeout report
6c61b47 phase-3i-A: D1-A implementation controls (non-runnable scaffolding)
ca3810c docs(phase-3h): merge report
```

## 7. Files included in the merge

10 new files plus 4 modified files, all under `src/`, `tests/`, or `docs/00-meta/implementation-reports/`:

**New files (D1-A package + tests + reports):**

- `src/prometheus/strategy/funding_aware_directional/__init__.py` — package public surface (86 lines).
- `src/prometheus/strategy/funding_aware_directional/variant_config.py` — `FundingAwareConfig` Pydantic model + locked module-level constants (180 lines).
- `src/prometheus/strategy/funding_aware_directional/primitives.py` — 9 pure helpers + `FundingEvent` dataclass (287 lines).
- `src/prometheus/strategy/funding_aware_directional/strategy.py` — `FundingAwareStrategy` facade + `FundingAwareEntrySignal` dataclass (196 lines).
- `tests/unit/strategy/funding_aware_directional/__init__.py` — empty test package init.
- `tests/unit/strategy/funding_aware_directional/test_variant_config.py` — locked-spec preservation tests (136 lines).
- `tests/unit/strategy/funding_aware_directional/test_primitives.py` — primitive function tests (390 lines).
- `tests/unit/strategy/funding_aware_directional/test_strategy.py` — facade tests (188 lines).
- `tests/unit/research/backtest/test_engine_d1a_guard.py` — engine-guard tests (88 lines).
- `docs/00-meta/implementation-reports/2026-04-29_phase-3i-A_D1A_implementation-controls.md` — checkpoint report (295 lines).
- `docs/00-meta/implementation-reports/2026-04-29_phase-3i-A_closeout-report.md` — closeout (129 lines).

**Modified files:**

- `src/prometheus/research/backtest/config.py` — added `StrategyFamily.FUNDING_AWARE_DIRECTIONAL` enum value; added `funding_aware_variant: FundingAwareConfig | None = None` field; extended `_check` validator (V1/F1/D1-A mutually-exclusive variant fields; D1-A rejects non-default V1 strategy_variant).
- `src/prometheus/research/backtest/engine.py` — added a guard at the top of `BacktestEngine.run` raising `RuntimeError("D1-A engine wiring not yet authorized; see Phase 3i-B1.")` when `strategy_family == FUNDING_AWARE_DIRECTIONAL`. V1 and F1 dispatch paths unchanged.
- `tests/unit/research/backtest/test_config.py` — added 8 D1-A dispatch validation tests.

No source code, no tests, no scripts outside the above files were touched. No `.claude/` files, no `.mcp.json`, no configuration, no credentials, no `data/`, no existing-doc modifications.

## 8. Confirmation that Phase 3i-A was implementation-control only

Confirmed. Phase 3i-A added the D1-A implementation surface (primitives + locked config + strategy facade + dispatch validation + engine guard) and the corresponding unit tests. It did NOT implement the D1-A engine path, run any D1-A backtest, generate the derived `funding_aware_features__v001` dataset, compute M1/M2/M3 mechanism checks on real data, or evaluate the first-execution gate. The phase is bounded strictly to "implementation surface + non-runnability proof + bit-for-bit control reproduction".

## 9. Confirmation that D1-A primitives / config / strategy facade / validation / engine guard were added

Confirmed:

- **D1-A primitives** (`src/prometheus/strategy/funding_aware_directional/primitives.py`): 9 pure helpers — `compute_funding_z_score`, `align_funding_event_to_bar`, `funding_extreme_event`, `signal_direction`, `compute_stop`, `compute_target`, `time_stop_bar_index`, `passes_stop_distance_filter`, `can_re_enter` — plus `FundingEvent` dataclass.
- **D1-A locked config** (`variant_config.py`): `FundingAwareConfig` with all 10 Phase 3g §6 + §5.6.5 Option A locked fields (Z-score threshold 2.0; lookback days 90 / events 270; stop multiplier 1.0; target_r 2.0; time-stop 32 bars; cooldown_rule per_funding_event; stop-distance band [0.60, 1.80]; direction_logic contrarian; regime_filter absent via `extra="forbid"`). Frozen + strict + extra=forbid.
- **D1-A strategy facade** (`strategy.py`): `FundingAwareStrategy` with stateless `evaluate_entry_signal` method + `FundingAwareEntrySignal` dataclass.
- **BacktestConfig validation surface** (`config.py`): `StrategyFamily.FUNDING_AWARE_DIRECTIONAL` enum value; `funding_aware_variant` field; validator extension with all D1-A dispatch invariants (V1/F1/D1-A mutually-exclusive variant fields; D1-A rejects non-default V1 strategy_variant per Phase 3g §14 / Phase 3h §3 V1/D1 hybrid prohibition).
- **D1-A engine guard** (`engine.py`): `BacktestEngine.run` raises `RuntimeError("D1-A engine wiring not yet authorized; see Phase 3i-B1.")` on `strategy_family == FUNDING_AWARE_DIRECTIONAL` dispatch. V1 default and F1 dispatch paths unchanged.

## 10. Confirmation that D1-A remains deliberately non-runnable

Confirmed. The D1-A engine dispatch path is NOT wired in Phase 3i-A. `BacktestEngine.run` raises a documented `RuntimeError` when D1-A dispatch is attempted; the guard message contains both `"D1-A engine wiring not yet authorized"` and `"Phase 3i-B1"`. Phase 3i-B1 will lift this guard and add the per-bar D1-A lifecycle.

The non-runnability is verified by `tests/unit/research/backtest/test_engine_d1a_guard.py::test_d1a_dispatch_raises_runtime_error`.

## 11. Confirmation that D1-A engine wiring was not implemented

Confirmed. `BacktestEngine` does NOT contain a `_run_symbol_d1a` method, a `FundingAwareLifecycleCounters` class, or any per-bar D1-A lifecycle implementation. The only D1-A-related change to `engine.py` is the dispatch guard at the top of `run()` (11 lines added). The full F1 dispatch path (`_run_symbol_f1`, F1 lifecycle counters, `_F1TradeMetadata`, etc.) and V1 dispatch path (`_run_symbol`, `V1BreakoutStrategy`, R2 metadata, etc.) remain entirely unchanged.

## 12. Confirmation that no D1-A backtests, diagnostics, first-execution gate, or V-window were run

Confirmed. The only backtests executed during Phase 3i-A were the three control re-runs:

- H0 R MED MARK (BTC + ETH).
- R3 R MED MARK (BTC + ETH).
- F1 R MED MARK (BTC + ETH).

No D1-A R MED, R LOW, R HIGH, R MED TRADE_PRICE, V MED, V LOW, V HIGH, or V TRADE_PRICE cell was executed. No D1-A first-execution gate was evaluated. No D1-A M1 / M2 / M3 mechanism check was computed on real data. No D1-A diagnostic output was produced.

## 13. Confirmation that no derived funding-aware dataset was generated or committed

Confirmed. The `funding_aware_features__v001` derived feature dataset (defined in Phase 3h §4.4) was NOT generated by Phase 3i-A. No `data/derived/funding_aware_features__v001/` directory exists. No `data/` artifact was generated for D1-A. `git status` after merge confirms zero `data/` entries staged or tracked.

## 14. Confirmation that quality gates passed

All four pre-merge gates green on the Phase 3i-A branch tip:

| Gate | Command | Result |
|------|---------|--------|
| Test suite | `uv run pytest` | **645 passed** in 12.40s |
| Linter | `uv run ruff check .` | **All checks passed!** |
| Formatter | `uv run ruff format --check .` | **154 files already formatted** |
| Type checker | `uv run mypy src` | **Success: no issues found in 61 source files** |

Pytest count delta: prior 567 (Phase 3d-B2) → after Phase 3i-A 645 = +78 tests, exactly matching the 15 + 42 + 10 + 8 + 3 per-file breakdown of the new D1-A tests verified via `pytest --collect-only`.

## 15. Confirmation that H0 / R3 / F1 R MED MARK controls reproduced bit-for-bit

Confirmed. Each fresh control re-run was bit-for-bit `diff`-compared against the prior committed baseline run on disk:

| Control | Symbol | Fresh run | Prior baseline | `diff` result |
|---------|:------:|-----------|----------------|---------------|
| H0 R MED MARK | BTC | `phase-2l-h0-r/2026-04-29T01-38-18Z/BTCUSDT/summary_metrics.json` | `phase-2l-h0-r/2026-04-28T21-40-58Z/BTCUSDT/summary_metrics.json` | **identical** |
| H0 R MED MARK | ETH | `phase-2l-h0-r/2026-04-29T01-38-18Z/ETHUSDT/...` | `phase-2l-h0-r/2026-04-28T21-40-58Z/ETHUSDT/...` | **identical** |
| R3 R MED MARK | BTC | `phase-2l-r3-r/2026-04-29T01-38-39Z/BTCUSDT/...` | `phase-2l-r3-r/2026-04-28T21-41-20Z/BTCUSDT/...` | **identical** |
| R3 R MED MARK | ETH | `phase-2l-r3-r/2026-04-29T01-38-39Z/ETHUSDT/...` | `phase-2l-r3-r/2026-04-28T21-41-20Z/ETHUSDT/...` | **identical** |
| F1 R MED MARK | BTC | `phase-3d-f1-window=r-slip=medium/2026-04-29T01-39-02Z/BTCUSDT/...` | `phase-3d-f1-window=r-slip=medium/2026-04-28T21-55-59Z/BTCUSDT/...` | **identical** |
| F1 R MED MARK | ETH | `phase-3d-f1-window=r-slip=medium/2026-04-29T01-39-02Z/ETHUSDT/...` | `phase-3d-f1-window=r-slip=medium/2026-04-28T21-55-59Z/ETHUSDT/...` | **identical** |

All 6 control cells reproduce bit-for-bit on every summary metric. The D1-A scaffolding (new enum value, new variant field, new self-contained module, engine guard) does NOT perturb V1 or F1 dispatch.

## 16. Confirmation that no `data/` artifacts were committed

Confirmed. `git status` after merge and push shows zero `data/` entries. The 14 files included in the merge are all under `src/`, `tests/`, or `docs/00-meta/implementation-reports/`. Control re-run outputs landed under existing git-ignored `data/derived/backtests/` directories — none of which are tracked.

## 17. Confirmation that no thresholds, strategy parameters outside Phase 3g D1-A locked spec, project locks, paper/shadow, Phase 4, live-readiness, deployment, MCP, Graphify, `.mcp.json`, credentials, or exchange-write work changed

| Category | Status |
|----------|--------|
| Phase 2f thresholds (§10.3 / §10.4 / §11.3 / §11.4) | UNCHANGED |
| **§11.6 = 8 bps HIGH per side** | UNCHANGED (Phase 2y closeout preserved verbatim) |
| §1.7.3 project-level locks (BTCUSDT-primary; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets; one-way mode; isolated margin; no pyramiding; no reversal while positioned; no hedge mode) | UNCHANGED |
| H0 baseline parameters | UNCHANGED |
| R3 sub-parameters (`exit_kind=FIXED_R_TIME_STOP`; `exit_r_target=2.0`; `exit_time_stop_bars=8`; same-bar priority STOP > TAKE_PROFIT > TIME_STOP) | UNCHANGED |
| R1a / R1b-narrow / R2 sub-parameters | UNCHANGED |
| F1 spec axes | UNCHANGED |
| **D1-A locked spec values** (Phase 3g binding) | PRESERVED VERBATIM in `FundingAwareConfig` (single source of truth; consumed unmodified) |
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
| Existing strategy / validation / cost / data / phase-gate / ai-coding-handoff / current-project-state specs | UNCHANGED |
| `docs/12-roadmap/technical-debt-register.md` | UNCHANGED |
| `docs/00-meta/implementation-ambiguity-log.md` | UNCHANGED |
| `docs/00-meta/current-project-state.md` | UNCHANGED |
| `docs/00-meta/ai-coding-handoff.md` | UNCHANGED |
| Source code (`src/prometheus/strategy/v1_breakout/**`) | UNCHANGED |
| Source code (`src/prometheus/strategy/mean_reversion_overextension/**`) | UNCHANGED |
| Source code (`src/prometheus/research/backtest/trade_log.py`) | UNCHANGED (D1-A field additions deferred to Phase 3i-B1) |
| Source code (`src/prometheus/research/backtest/accounting.py`, `fills.py`, `funding_join.py`, `simulation_clock.py`, `sizing.py`, `stops.py`) | UNCHANGED |
| Scripts (`scripts/**`) | UNCHANGED (no D1-A runner; no D1-A analysis script) |
| `.claude/` directory | UNCHANGED |
| `data/` directory | UNCHANGED, NO COMMITS |

The only locked-axis "additions" under Phase 3i-A are:

- `StrategyFamily` enum gains a new value `FUNDING_AWARE_DIRECTIONAL`.
- `BacktestConfig` gains a new field `funding_aware_variant: FundingAwareConfig | None = None` defaulting to None.
- `BacktestConfig._check` validator extends to handle the new family invariants.
- `BacktestEngine.run` adds the D1-A dispatch guard.
- New `funding_aware_directional` package added with locked spec values consumed unmodified from Phase 3g.

None of these constitute a Phase 2f-framework threshold change, §1.7.3 project-lock change, or a change to existing locked sub-parameters of H0 / R3 / R1a / R1b-narrow / R2 / F1.

## 18. Confirmation that Phase 3i-B1 was not started

Confirmed. Phase 3i-A merged into `main` is terminal-as-of-now. **No Phase 3i-B1** (engine wiring + lifecycle counters + output fields + runner scaffold + full 9-cell control reproduction) and no implementation phase has been started. Phase 3i-A's checkpoint report (§16) and closeout report (§10) explicitly recommend Phase 3i-B1 is **safe to consider** after operator review, but Phase 3i-B1 is NOT authorized by Phase 3i-A — it requires a separately-authorized operator decision.

The recommended next operator decision is one of:

1. Authorize Phase 3i-B1 (D1-A engine wiring) — Phase 3i-A primary recommendation.
2. Remain paused at the post-Phase-3i-A boundary.
3. Authorize an alternative direction (e.g., D7 external cost-evidence review per Phase 3f §7.7) or any other operator-driven docs-only direction.
4. Any other operator-driven decision consistent with Phase 3e / Phase 3f / Phase 3g / Phase 3h / Phase 3i-A restrictions.

Until the operator authorizes one of those decisions, the project remains at the post-Phase-3i-A consolidation boundary. No paper/shadow planning, no Phase 4 runtime work, no live-readiness work, no deployment work, no production-key creation, no exchange-write capability — all remain unauthorized.

---

**End of Phase 3i-A merge report.** Phase 3i-A D1-A implementation-controls + checkpoint + closeout (with post-review report cleanup) merged into `main` at `8ba58a4421f0ea189890fc6a58e5dda5cf11de25`. D1-A primitives / config / strategy facade / validation / engine guard added; D1-A remains deliberately non-runnable; D1-A engine wiring NOT implemented; no D1-A backtest run; no D1-A diagnostics computed; no derived dataset generated; quality gates all green (645 pytest passing; ruff/format/mypy clean); H0 / R3 / F1 R MED MARK controls reproduce bit-for-bit. R3 V1-breakout baseline-of-record / H0 framework anchor / R1a-R1b-narrow-R2-F1 retained-research-evidence preserved verbatim. F1 HARD REJECT preserved; Phase 3d-B2 terminal for F1 preserved. §11.6 = 8 bps HIGH per side preserved verbatim. §1.7.3 locks preserved verbatim. D1-A locked spec preserved verbatim per Phase 3g binding. No paper/shadow, no Phase 4, no live-readiness, no deployment, no MCP / Graphify / `.mcp.json`, no credentials, no `data/` commits. **Phase 3i-B1 NOT authorized; no next phase started.** Awaiting operator review.
