# Phase 3i-B1 — Merge Report

**Phase:** 3i-B1 — D1-A engine-wiring control phase merged into `main`. Lifts the Phase 3i-A guard, wires D1-A into the backtest engine (per-bar lifecycle, lifecycle counters, output fields, runner scaffold), proves H0 / R3 / F1 controls reproduce bit-for-bit, without running any D1-A candidate backtest or evaluating the first-execution gate.

**Date:** 2026-04-29 UTC.

---

## 1. Phase 3i-B1 branch tip SHA before merge

`b3b71eaa788e2977edf521ddb98c27670a5d6b65` on `phase-3i-b1/d1a-engine-wiring-controls`.

The branch contained three commits ahead of `main` at merge time:

- `fb7afa7` — `phase-3i-B1: D1-A engine wiring + lifecycle counters + runner scaffold` — original Phase 3i-B1 commit (8 files, +2242 / −47).
- `5f47d13` — `phase-3i-B1: record commit hash fb7afa7 in closeout report` — closeout commit-hash backfill (1 file, +5 / −1).
- `b3b71ea` — `phase-3i-B1: report consistency cleanup -- control wording + test counts` — pre-merge docs-only wording cleanup (2 files, +14 / −9).

## 2. Merge commit hash

`9a9764c9e47c25bb84e0892a1e35c10a350f8e6c`.

Created by `git merge --no-ff phase-3i-b1/d1a-engine-wiring-controls` from `main` at `4dc15a9a548f472e3246461422b65f7f91c4832c` (pre-merge). Merge produced by the `ort` strategy. 8 files changed; 2251 insertions; 47 deletions; 4 new files.

## 3. Merge-report commit hash

To be recorded after this merge-report file is committed to `main` and pushed. The merge-report commit appends this Markdown file under `docs/00-meta/implementation-reports/` and changes nothing else.

## 4. Main / origin sync confirmation

Local `main` and `origin/main` are synced at the merge commit:

```text
local  main         9a9764c9e47c25bb84e0892a1e35c10a350f8e6c
origin/main         9a9764c9e47c25bb84e0892a1e35c10a350f8e6c
```

Push completed cleanly: `4dc15a9..9a9764c  main -> main`.

## 5. Git status

Working tree clean immediately after the merge and push. No untracked files. No staged changes. No `data/` artifacts staged or tracked.

## 6. Latest 5 commits

```text
9a9764c Merge Phase 3i-B1 (D1-A engine wiring + lifecycle counters + runner scaffold) into main
b3b71ea phase-3i-B1: report consistency cleanup -- control wording + test counts
5f47d13 phase-3i-B1: record commit hash fb7afa7 in closeout report
fb7afa7 phase-3i-B1: D1-A engine wiring + lifecycle counters + runner scaffold
4dc15a9 docs(phase-3i-A): merge report
```

## 7. Files included in the merge

8 files (4 new + 4 modified):

**New files:**

- `scripts/phase3j_D1A_execution.py` — Phase 3j D1-A execution runner scaffold (guarded by `--phase-3j-authorized`; fails closed without it; `check-imports` subcommand safe). 169 lines.
- `tests/unit/research/backtest/test_engine_d1a_dispatch.py` — 21 comprehensive D1-A engine dispatch tests (synthetic in-memory). 797 lines.
- `docs/00-meta/implementation-reports/2026-04-29_phase-3i-B1_D1A_engine-wiring-controls.md` — checkpoint report. 351 lines.
- `docs/00-meta/implementation-reports/2026-04-29_phase-3i-B1_closeout-report.md` — closeout. 106 lines.

**Modified files:**

- `src/prometheus/research/backtest/engine.py` — D1-A engine wiring (+742 / −): lifted Phase 3i-A guard; added `_run_symbol_d1a` + open / close helpers; `_D1ATradeMetadata`; `FundingAwareLifecycleCounters`; D1-A state on `_OpenTrade` / `_SymbolRun` / `BacktestRunResult`; D1-A dispatch in `run()`. V1 and F1 dispatch paths bit-for-bit unchanged.
- `src/prometheus/research/backtest/trade_log.py` — 4 new D1-A `TradeRecord` fields with None / NaN / -1 defaults; parquet schema extension. +23 lines.
- `tests/unit/research/backtest/test_engine_d1a_guard.py` — replaced 3 Phase 3i-A guard-raising tests with 5 Phase 3i-B1 dispatch tests (net +2). +103 / −47.
- `tests/unit/research/backtest/test_trade_log.py` — extended parquet schema assertion to include 4 new D1-A column names. +7 lines.

## 8. Confirmation that Phase 3i-B1 was engine-wiring-control only

Confirmed. Phase 3i-B1 wired the D1-A engine dispatch path, added lifecycle counters and output fields, and added a guarded runner scaffold. It did NOT run any D1-A candidate backtest on real data, evaluate the first-execution gate, compute M1/M2/M3 mechanism checks, or generate the `funding_aware_features__v001` derived dataset. The phase is bounded strictly to "engine wiring + non-runnability of candidate runs + bit-for-bit control reproduction".

## 9. Confirmation that D1-A is now engine-wired

Confirmed. The Phase 3i-A `RuntimeError` guard at the top of `BacktestEngine.run` is lifted. D1-A dispatches through `_run_symbol_d1a` when `strategy_family == FUNDING_AWARE_DIRECTIONAL`. The dispatch path is fully implemented per the binding Phase 3g spec (with Phase 3h timing-clarification amendments) and verified by 21 synthetic engine tests in `test_engine_d1a_dispatch.py` + 5 dispatch / counters tests in `test_engine_d1a_guard.py`.

## 10. Confirmation that lifecycle counters, TradeRecord fields, and runner scaffold were added

Confirmed:

- **Lifecycle counters**: `FundingAwareLifecycleCounters` dataclass with event-level identity `detected = filled + rejected_stop_distance + blocked_cooldown`. Per-symbol `d1a_last_processed_event_id` ensures repeated 15m bars referencing the same `funding_event_id` do NOT inflate the detected count. Identity verified by `test_d1a_lifecycle_identity_holds` and `test_funding_aware_lifecycle_counters_identity_holds_when_zero`.
- **TradeRecord D1-A fields**: 4 new fields (`funding_event_id_at_signal`, `funding_z_score_at_signal`, `funding_rate_at_signal`, `bars_since_funding_event_at_signal`) with None / NaN / -1 defaults for V1 / F1 rows. Parquet schema extended; verified by `test_trade_log.py::test_table_schema_has_expected_columns`. Reused `entry_to_target_distance_atr` ≈ 2.0 (D1-A target geometry) and `stop_distance_at_signal_atr` ≈ 1.0 (D1-A stop geometry).
- **Runner scaffold**: `scripts/phase3j_D1A_execution.py` double-gated. Subcommand `d1a` requires `--phase-3j-authorized` AND has a second-gate "run-loop not yet implemented in Phase 3i-B1 scaffold" exit. Verified by `test_d1a_runner_scaffold_requires_authorization_flag` and `test_d1a_runner_scaffold_check_imports_ok`.

## 11. Confirmation that D1-A candidate backtests were not run

Confirmed. No D1-A R MED, R LOW, R HIGH, R MED TRADE_PRICE, V MED, V LOW, V HIGH, or V TRADE_PRICE cell was executed on the real v002 dataset. The only D1-A engine invocations during Phase 3i-B1 were:

- 21 synthetic in-memory tests in `test_engine_d1a_dispatch.py` (~22 warmup bars + a handful of post-warmup bars each).
- The `check-imports` subcommand of the runner scaffold (no engine run).

No real-dataset D1-A backtest occurred. The runner scaffold's `d1a` subcommand exits non-zero without `--phase-3j-authorized` AND exits non-zero even with the flag (Phase 3i-B1 double-gate).

## 12. Confirmation that D1-A diagnostics, first-execution gate, and V-window were not run

Confirmed. Phase 3i-B1 did not compute any of: M1 / M2 / M3 mechanism checks; per-funding-regime performance; per-volatility-regime performance; mean_R_by_exit_reason; aggregate_R_by_exit_reason; TIME_STOP-subset mean R; funding-accrual contribution decomposition; LOW/MED/HIGH cost sensitivity for D1-A; mark-price vs trade-price for D1-A; first-execution gate verdict mapping. **No D1-A V-window cell was run** (V-window is conditional on R-window PROMOTE per Phase 3h §10.2; R-window itself is not authorized in Phase 3i-B1). All are reserved for Phase 3j (or a subsequent operator-authorized phase) per the Phase 3h §6 / §15 staged plan.

## 13. Confirmation that no derived funding-aware dataset was generated or committed

Confirmed. The `funding_aware_features__v001` derived feature dataset (defined in Phase 3h §4.4) was NOT generated by Phase 3i-B1. No `data/derived/funding_aware_features__v001/` directory exists. No `data/` artifact was generated for D1-A. `git status` after merge confirms zero `data/` entries staged or tracked.

## 14. Confirmation that quality gates passed

All four pre-merge gates green on the Phase 3i-B1 branch tip:

| Gate | Command | Result |
|------|---------|--------|
| Test suite | `uv run pytest` | **668 passed** in 12.56s |
| Linter | `uv run ruff check .` | **All checks passed!** |
| Formatter | `uv run ruff format --check .` | **156 files already formatted** |
| Type checker | `uv run mypy src` | **Success: no issues found in 61 source files** |

Pytest count delta: prior 645 (Phase 3i-A) → after Phase 3i-B1 668 = **+23 net** (21 new tests in `test_engine_d1a_dispatch.py` + 2 net from replacing 3 guard tests with 5 dispatch tests in `test_engine_d1a_guard.py`).

## 15. Confirmation that H0 / R3 / F1 controls reproduced bit-for-bit

Confirmed. **Full control set (5 named controls / 10 symbol-level cells)** reproduces bit-for-bit via `diff` against prior committed baselines:

| Control | Window | Slippage | Stop trigger | Symbol | `diff` result |
|---------|--------|----------|--------------|:------:|---------------|
| H0 | R | MED | MARK | BTC | **identical** |
| H0 | R | MED | MARK | ETH | **identical** |
| H0 | V | MED | MARK | BTC | **identical** |
| H0 | V | MED | MARK | ETH | **identical** |
| R3 | R | MED | MARK | BTC | **identical** |
| R3 | R | MED | MARK | ETH | **identical** |
| R3 | V | MED | MARK | BTC | **identical** |
| R3 | V | MED | MARK | ETH | **identical** |
| F1 | R | MED | MARK | BTC | **identical** |
| F1 | R | MED | MARK | ETH | **identical** |

All 10 cells reproduce bit-for-bit on every summary metric. The D1-A engine wiring (new dispatch path, new lifecycle counters, new TradeRecord fields, engine guard lifted) does NOT perturb V1 or F1 dispatch.

## 16. Confirmation that no `data/` artifacts were committed

Confirmed. `git status` after merge and push shows zero `data/` entries. The 8 files included in the merge are all under `src/`, `tests/`, `scripts/`, or `docs/00-meta/implementation-reports/`. Control re-run outputs landed under existing git-ignored `data/derived/backtests/` directories — none of which are tracked.

## 17. Confirmation that no thresholds, strategy parameters outside Phase 3g D1-A locked spec, project locks, paper/shadow, Phase 4, live-readiness, deployment, MCP, Graphify, `.mcp.json`, credentials, or exchange-write work changed

| Category | Status |
|----------|--------|
| Phase 2f thresholds (§10.3 / §10.4 / §11.3 / §11.4) | UNCHANGED |
| **§11.6 = 8 bps HIGH per side** | UNCHANGED (Phase 2y closeout preserved verbatim) |
| §1.7.3 project-level locks | UNCHANGED |
| H0 baseline parameters | UNCHANGED |
| R3 sub-parameters (`exit_kind=FIXED_R_TIME_STOP`; `exit_r_target=2.0`; `exit_time_stop_bars=8`; same-bar priority STOP > TAKE_PROFIT > TIME_STOP) | UNCHANGED |
| R1a / R1b-narrow / R2 sub-parameters | UNCHANGED |
| F1 spec axes | UNCHANGED |
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
| Existing strategy / validation / cost / data / phase-gate / ai-coding-handoff / current-project-state specs | UNCHANGED |
| `docs/12-roadmap/technical-debt-register.md` | UNCHANGED |
| `docs/00-meta/implementation-ambiguity-log.md` | UNCHANGED |
| `docs/00-meta/current-project-state.md` | UNCHANGED |
| `docs/00-meta/ai-coding-handoff.md` | UNCHANGED |
| Source code (`src/prometheus/strategy/v1_breakout/**`) | UNCHANGED |
| Source code (`src/prometheus/strategy/mean_reversion_overextension/**`) | UNCHANGED |
| Source code (`src/prometheus/strategy/funding_aware_directional/**`) | UNCHANGED (Phase 3i-A primitives + config + facade still binding) |
| Source code (`src/prometheus/research/backtest/config.py`) | UNCHANGED (Phase 3i-A validator already wired) |
| Source code (`src/prometheus/research/backtest/accounting.py`, `fills.py`, `funding_join.py`, `simulation_clock.py`, `sizing.py`, `stops.py`) | UNCHANGED |
| Source code (`src/prometheus/research/backtest/report.py`) | UNCHANGED |
| `.claude/` directory | UNCHANGED |
| `data/` directory | UNCHANGED, NO COMMITS |

The locked-axis additions under Phase 3i-B1 are limited to:

- `BacktestEngine.run` guard lifted; D1-A dispatch added.
- `_run_symbol_d1a` and helper methods added.
- `FundingAwareLifecycleCounters` + `_D1ATradeMetadata` dataclasses added.
- `BacktestRunResult.funding_aware_counters_per_symbol` field added.
- 4 new `TradeRecord` fields + parquet schema additions.
- Runner scaffold script added (guarded, fails closed).

None of these constitute a Phase 2f-framework threshold change, §1.7.3 project-lock change, or a change to existing locked sub-parameters of H0 / R3 / R1a / R1b-narrow / R2 / F1.

## 18. Confirmation that Phase 3j was not started

Confirmed. Phase 3i-B1 merged into `main` is terminal-as-of-now. **No Phase 3j** (D1-A candidate runs + diagnostics + first-execution gate evaluation) has been started. Phase 3i-B1's checkpoint report (§18) and closeout report (§10) explicitly recommend Phase 3j is **safe to consider** after operator review, but Phase 3j is NOT authorized by Phase 3i-B1 — it requires a separately-authorized operator decision.

The runner scaffold `scripts/phase3j_D1A_execution.py` is committed but double-gated: it requires `--phase-3j-authorized` AND has a second-gate "run-loop not yet implemented" exit even with the flag. Phase 3j must implement the run-loop body and lift the second gate; that work is not part of Phase 3i-B1.

The recommended next operator decision is one of:

1. Authorize Phase 3j (D1-A candidate runs + diagnostics + first-execution gate) — Phase 3i-B1 primary recommendation.
2. Remain paused at the post-Phase-3i-B1 boundary.
3. Authorize an alternative direction (e.g., D7 external cost-evidence review per Phase 3f §7.7) or any other operator-driven docs-only direction.
4. Any other operator-driven decision consistent with Phase 3e / Phase 3f / Phase 3g / Phase 3h / Phase 3i-A / Phase 3i-B1 restrictions.

Until the operator authorizes one of those decisions, the project remains at the post-Phase-3i-B1 consolidation boundary. No paper/shadow planning, no Phase 4 runtime work, no live-readiness work, no deployment work, no production-key creation, no exchange-write capability — all remain unauthorized.

---

**End of Phase 3i-B1 merge report.** Phase 3i-B1 D1-A engine wiring + lifecycle counters + runner scaffold + checkpoint + closeout (with post-review wording cleanup) merged into `main` at `9a9764c9e47c25bb84e0892a1e35c10a350f8e6c`. D1-A is now engine-wired; lifecycle counters + TradeRecord fields + runner scaffold added. **No D1-A candidate backtest run; no D1-A diagnostics computed; no first-execution gate evaluated; no V-window run; no derived dataset generated; no `data/` commit.** Quality gates all green (668 pytest passing; +23 net since Phase 3i-A). Full control set (5 named controls / 10 symbol-level cells) reproduces bit-for-bit. R3 V1-breakout baseline-of-record / H0 framework anchor / R1a-R1b-narrow-R2-F1 retained-research-evidence preserved verbatim. F1 HARD REJECT preserved; Phase 3d-B2 terminal for F1 preserved. §11.6 = 8 bps HIGH per side preserved verbatim. §1.7.3 locks preserved verbatim. D1-A locked spec preserved verbatim per Phase 3g binding. No paper/shadow, no Phase 4, no live-readiness, no deployment, no MCP / Graphify / `.mcp.json`, no credentials, no exchange-write change. **Phase 3j NOT authorized; no next phase started.** Awaiting operator review.
