# Phase 3d-A Closeout Report

**Phase:** 3d-A — F1 (mean-reversion-after-overextension) implementation + tests + quality gates + H0/R3 control reproduction. **First phase to authorize source code, tests, and scripts on the F1 family.**

**Date:** 2026-04-28 UTC.

**Status:** **Phase 3d-A's implementation-control objective passed.** F1 self-contained module + primitives + locked `MeanReversionConfig` + `StrategyFamily`/`BacktestConfig` dispatch surface guard + `TARGET` ExitReason addition + 68 F1 unit tests added; all 4 quality gates green; all 48 H0/R3 control cells reproduce bit-for-bit. **F1 remains deliberately non-runnable** — the `BacktestConfig` validator hard-rejects `strategy_family=MEAN_REVERSION_OVEREXTENSION` until Phase 3d-B lifts that guard. Several engine-output and execution-integration pieces are **deferred to Phase 3d-B as mandatory work before any F1 result can be produced or interpreted** (see §5 for the explicit Completed-in-3d-A vs Deferred-to-3d-B accounting). **No F1 backtests run.** **No F1 first-execution gate evaluated.** **No F1 V-window run executed.** Phase 3d-B not started. Awaiting operator review and possible merge to `main`.

---

## 1. Current branch

```
phase-3d-a/f1-implementation-controls
```

Branched from `main` at `b477c2d0776220c6390ab4249e471920137f12da` (the post-Phase-3c-merge-report tip). Not pushed. Not merged.

## 2. Git status

After all Phase 3d-A commits:

```
On branch phase-3d-a/f1-implementation-controls
nothing to commit, working tree clean
```

(State as of immediately after the final Phase 3d-A commit, which includes both the implementation files and these two reports. Pre-commit state had the F1 module / tests / V1 modifications as untracked / unstaged for the main thread to inspect.)

## 3. Files changed

Total: **18 files** added or modified across the entire Phase 3d-A branch (vs `main`):

### 3.1 New F1 source module — 7 files (~720 lines)

- `src/prometheus/strategy/mean_reversion_overextension/__init__.py`
- `src/prometheus/strategy/mean_reversion_overextension/variant_config.py`
- `src/prometheus/strategy/mean_reversion_overextension/features.py`
- `src/prometheus/strategy/mean_reversion_overextension/stop.py`
- `src/prometheus/strategy/mean_reversion_overextension/target.py`
- `src/prometheus/strategy/mean_reversion_overextension/cooldown.py`
- `src/prometheus/strategy/mean_reversion_overextension/strategy.py`

### 3.2 New F1 unit tests — 7 files (~975 lines; 68 new tests)

- `tests/unit/strategy/mean_reversion_overextension/__init__.py`
- `tests/unit/strategy/mean_reversion_overextension/test_variant_config.py`
- `tests/unit/strategy/mean_reversion_overextension/test_features.py`
- `tests/unit/strategy/mean_reversion_overextension/test_stop.py`
- `tests/unit/strategy/mean_reversion_overextension/test_target.py`
- `tests/unit/strategy/mean_reversion_overextension/test_cooldown.py`
- `tests/unit/strategy/mean_reversion_overextension/test_strategy.py`

### 3.3 Modified V1 contact surface — 2 files (+46 / −2 lines)

- `src/prometheus/strategy/types.py` (+6 / −2): added `TARGET = "TARGET"` to `ExitReason` StrEnum + docstring update.
- `src/prometheus/research/backtest/config.py` (+40 / 0): added `StrategyFamily` enum + `strategy_family` field + `mean_reversion_variant` field + validator clauses + import.

### 3.4 New documentation reports — 2 files

- [docs/00-meta/implementation-reports/2026-04-27_phase-3d-A_F1_implementation-control-checkpoint.md](2026-04-27_phase-3d-A_F1_implementation-control-checkpoint.md) — Phase 3d-A checkpoint report (13 brief-required items).
- [docs/00-meta/implementation-reports/2026-04-27_phase-3d-A_closeout-report.md](2026-04-27_phase-3d-A_closeout-report.md) — this file (7 brief-required items).

### 3.5 Files NOT touched

- `src/prometheus/research/backtest/engine.py` — engine dispatch logic untouched; H0/R3 control reproduction proves V1 path bit-for-bit preserved.
- `src/prometheus/strategy/v1_breakout/` — entire V1 module unchanged.
- `src/prometheus/research/backtest/trade_log.py`, `diagnostics.py`, `report.py` — unchanged (F1-specific TradeRecord fields + funnel counters reserved for Phase 3d-B).
- All existing 474 V1 tests — unchanged; pre-existing test surface preserved.
- `scripts/` — no new runner script; existing Phase 2l runner used unmodified for control reproduction.
- `data/`, `.claude/`, `.mcp.json`, configuration / credentials — untouched.
- All existing docs (current-project-state, ai-coding-handoff, phase-gates, technical-debt-register, validation-checklist, cost-modeling, backtesting-principles, data-requirements, dataset-versioning, v1-breakout-strategy-spec, Phase 3a/3b/3c memos and reports) — unchanged.

## 4. Commit hash or hashes

The Phase 3d-A branch contains multiple commits (the original implementation/tests/reports commit; an operator-mandated docs-only scope-accounting clarification commit; this docs-only clerical-fix commit). The full Phase 3d-A commit chain on `phase-3d-a/f1-implementation-controls` (`main` → branch tip):

| Commit | Short SHA | Full SHA | Description |
|--------|-----------|----------|-------------|
| 1 | `06ad2a8` | `06ad2a886653e567a434f64c8dd7a14b84d6da09` | `phase-3d-A: F1 implementation + tests + quality gates + H0/R3 control reproduction` — original Phase 3d-A artifact commit (18 files; +2254 / −2): F1 source module (7 files), F1 unit tests (7 files), V1 contact-surface modifications (2 files), Phase 3d-A checkpoint report, Phase 3d-A closeout report (initial). |
| 2 | `1a53423` | `1a53423e6f8692c4b933025559d6b590cab26128` | `docs(phase-3d-A): clarify implementation-control objective vs Phase 3d-B deferrals` — operator-mandated docs-only scope-accounting clarification commit (2 files; +83 / −42): added explicit Completed-in-Phase-3d-A vs Deferred-to-Phase-3d-B boundary in checkpoint §1.1 and closeout §5; reframed "all objectives met" to "implementation-control objective passed". No code or metric changes. |
| 3 | (this clerical-fix commit) | reported in the final chat response and the Phase 3d-A merge report after the commit lands | `docs(phase-3d-A): clerical fix to closeout §4 commit-hash listing` — this docs-only clerical-fix commit corrects the closeout's §4 to accurately list the multi-commit chain rather than describing the branch as a single-commit branch. No code, tests, scripts, config, data, threshold, parameter, or project-lock change. No alteration of metrics, quality-gate outputs, H0/R3 control reproduction values, scope boundaries, or recommendations. |

**Current branch HEAD full SHA** (visible via `git rev-parse HEAD` after this clerical-fix commit lands; recorded in the final chat response and in the Phase 3d-A merge report on `main` after merge):

```
recorded in Step 3 / Step 4 of the operator's brief, after the clerical-fix commit completes
```

The branch is therefore **3 commits ahead of `main`** at the time the merge into `main` is performed. The `--no-ff` merge will preserve all three commits in history and add a single explicit merge commit.

## 5. Phase 3d-A scope-accounting: explicit Completed-in-3d-A vs Deferred-to-3d-B

Phase 3d-A's **implementation-control objective passed**: the F1 self-contained module is implemented per Phase 3b §4, V1 H0/R3 controls reproduce bit-for-bit, quality gates are green, and the `BacktestConfig` validator hard-rejects F1 invocation until Phase 3d-B lifts that guard. To prevent the "objective passed" framing from obscuring the boundary between this phase and the next, this section enumerates Completed-in-Phase-3d-A and Deferred-to-Phase-3d-B explicitly.

### 5.1 Completed in Phase 3d-A

1. **F1 self-contained strategy module** + primitives at `src/prometheus/strategy/mean_reversion_overextension/` (7 source files, ~720 lines).
2. **Locked `MeanReversionConfig`** with the seven Phase 3b §4 values via `Field(ge=v, le=v)` constraints and a `model_post_init` defense-in-depth re-check.
3. **F1 feature primitives** (`features.py::cumulative_displacement_8bar`, `sma_8_close`, `overextension_event` with strict `>` boundary).
4. **F1 stop primitives** (`stop.py::compute_initial_stop` long/short with 0.10×ATR buffer; `passes_stop_distance_filter` for the [0.60, 1.80]×ATR(20) admissibility band).
5. **F1 target primitives** (`target.py::compute_target` frozen SMA(8); `target_hit` close-only contract).
6. **F1 cooldown primitives** (`cooldown.py::cooldown_unwound`, `can_re_enter` with same-direction blocking + opposite-direction allowance).
7. **F1 stateless strategy facade** (`strategy.py::MeanReversionStrategy.evaluate_entry_signal` returning a `MeanReversionEntrySignal | None`).
8. **`StrategyFamily` / `BacktestConfig` dispatch surface guard** — `strategy_family: StrategyFamily = V1_BREAKOUT` field; `mean_reversion_variant: MeanReversionConfig | None = None` field; validator hard-rejecting `MEAN_REVERSION_OVEREXTENSION` with `ValueError("Phase 3d-A: F1 strategy_family is reserved; engine dispatch will be wired in Phase 3d-B")`.
9. **`TARGET = "TARGET"` ExitReason addition** (placeholder for Phase 3d-B engine wiring; existing V1 enum values unchanged).
10. **68 F1 unit tests** across 7 test files (542 total pytest passing; +68 over baseline 474; zero V1 regressions).
11. **Quality gates green** — `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy src` all passed.
12. **H0/R3 control reproduction** bit-for-bit on all 48 metric cells (proves V1 dispatch path is unchanged by the BacktestConfig field additions).
13. **F1 deliberately non-runnable** — even an attempted F1 backtest construction would fail at config-validation time. This is the safety guard preserved through Phase 3d-A.

### 5.2 Deferred to Phase 3d-B (mandatory before any F1 result can be produced or interpreted)

These items are **mandatory Phase 3d-B work**. None of the F1 first-execution-gate conditions (Phase 3c §7.2) or mechanism predictions (Phase 3c §9) can be evaluated until they are wired.

1. **Actual `BacktestEngine` F1 dispatch wiring** in `_run_symbol`. Phase 3d-A added the dispatch *surface* (enum + field + validator placeholder); Phase 3d-B must add the engine code path that routes per-bar evaluation to F1 when `strategy_family == MEAN_REVERSION_OVEREXTENSION`.
2. **F1 TradeRecord output fields** (e.g., `overextension_magnitude_at_signal`, `frozen_target_value`, `entry_to_target_distance_atr`, `stop_distance_at_signal_atr`, `cooldown_blocked_signal_count`) added to `trade_log.py` with NaN/None defaults for V1 rows, mirroring the R2 metadata pattern.
3. **F1 lifecycle / funnel counters** (analogous to `R2LifecycleCounters`) for `overextension_events_detected` / `_filled` / `_rejected_stop_distance` / `_blocked_cooldown`, plus the `accounting_identity_holds` property.
4. **F1 time-stop engine integration.** Phase 3d-A locked `time_stop_bars=8` in config and tested the value; Phase 3d-B must add the engine logic that exits at `open(B+10)` if neither target nor stop has fired by close of `B+9`.
5. **F1 same-bar priority engine behavior** — STOP > TARGET > TIME_STOP. Phase 3d-A did not implement same-bar priority; this is engine concern.
6. **F1 target next-bar-open fill integration.** Phase 3d-A's `target.target_hit` returns a boolean on a completed bar's close; Phase 3d-B must wire the fill at `open(t+1)` for that target-cross.
7. **F1 runner script** (e.g., `scripts/phase3d_F1_execution.py`) parallel to `scripts/phase2w_R2_execution.py`.
8. **F1 diagnostics + first-execution-gate analysis** per Phase 3c §8 mandatory diagnostics, §7.2 first-execution-gate conditions (i)–(v), and §9 M1 / M2 / M3 mechanism predictions. This includes the analysis script that consumes per-symbol summary metrics + trade logs and produces the §7.3 verdict outcome.
9. **F1 R/V candidate backtests** — the 4 mandatory F1 R-window governing/sensitivity runs and the 1 conditional F1 V-window run per Phase 3c §6.1 / §6.2 inventory.

### 5.3 What this means in plain English

Phase 3d-A built the F1 toolkit (config, primitives, strategy facade, dispatch enum, unit tests) and proved the toolkit's existence does not perturb V1 behavior. Phase 3d-A did **not** wire the toolkit into the engine, did **not** produce any F1 trade record, and did **not** run any F1 backtest. Producing or interpreting any F1 result is mandatory Phase 3d-B work and cannot be inferred or partially derived from Phase 3d-A artifacts. The BacktestConfig validator's hard-rejection of `MEAN_REVERSION_OVEREXTENSION` enforces this boundary at the type-construction level.

## 6. Confirmation that F1 results were not run or interpreted

Confirmed. Per Phase 3c §10.4 sequencing requirement, F1 result execution and interpretation are reserved for Phase 3d-B. Specifically:

- **No F1 backtest invoked.** The BacktestConfig validator hard-rejects `strategy_family=MEAN_REVERSION_OVEREXTENSION` with `ValueError("Phase 3d-A: F1 strategy_family is reserved; engine dispatch will be wired in Phase 3d-B")`. Even an attempted F1 backtest construction would fail at config-validation time.
- **No F1 first-execution gate computed.** Phase 3c §7.2 conditions (i)–(v) were not evaluated; no expR / PF / netPct / maxDD on F1 trades exists.
- **No F1 mechanism-validation (M1/M2/M3) computed.** Phase 3c §9 metrics not produced.
- **No F1 V-window run executed.** Per Phase 3c §6.2, run 5 is conditional on Phase 3d-B governing run §7.2 PROMOTE outcome; no PROMOTE has been computed.

The only backtests executed in Phase 3d-A were the **four V1 H0/R3 control runs** (per Phase 3c §6.3 / §6.4 reference re-runs) using the existing Phase 2l runner script. These reproduced locked Phase 2e/2l/2s baselines bit-for-bit on all 48 metric cells, proving V1 dispatch is unchanged.

## 7. Whether the branch is ready for operator review

**Ready for review on its scope-limited objective.** Phase 3d-A's implementation-control objective passed; the branch is technically and procedurally ready for operator review and possible merge. However, "ready for review" applies only to the Phase 3d-A scope — see §5 for the explicit boundary between Completed-in-3d-A and Deferred-to-3d-B. Items in §5.2 are mandatory Phase 3d-B work before any F1 result can be produced or interpreted; they are not implied by this branch's readiness.

- **Technically ready (Phase 3d-A scope):**
  - Branch is clean (`nothing to commit, working tree clean` after the Phase 3d-A commit + this docs-only clarification commit).
  - All 4 quality gates green (`pytest`: 542 passed; `ruff check`: All checks passed; `ruff format --check`: 142 files already formatted; `mypy src`: Success no issues).
  - All 48 H0/R3 control cells reproduce bit-for-bit on locked Phase 2 baselines.
  - F1 module is self-contained; V1 modifications are minimal (2 files; +46 / −2) and additive-only.
  - F1 deliberately non-runnable through the BacktestConfig validator until Phase 3d-B lifts that guard.
  - No `data/` commits.
- **Procedurally ready (Phase 3d-A scope):**
  - Phase 3b F1 spec axes locked verbatim in `MeanReversionConfig`.
  - Phase 3c §10.4 Phase 3d-A sequencing requirement satisfied (implement → quality gates pass → H0/R3 reproduction bit-for-bit; F1 results NOT computed because Phase 3d-A does not have engine F1 dispatch wired).
  - Phase 3c §6 run inventory respected (only the 4 V1 control re-runs executed; no F1 R/V runs executed).
  - Phase 3c §7.4 cross-family-fairness preserved (F1 not yet evaluated; cross-family deltas not yet computed).
- **NOT yet ready (deferred to Phase 3d-B per §5.2):** F1 results, F1 first-execution gate evaluation, F1 mechanism (M1/M2/M3) computation, F1 verdict outcome per Phase 3c §7.3. This branch does not produce or interpret any F1 result; it only proves the toolkit exists and does not perturb V1.
- **Merge mechanics if/when operator approves:** would be a `--no-ff` merge commit consistent with the prior Phase 2x / Phase 2y / slippage-cleanup / Phase 3a / Phase 3b / Phase 3c merge pattern, producing a merge commit on `main` of the form `Merge Phase 3d-A (F1 implementation + control reproduction) into main`. Branch ahead by 2 commits after this clarification: the original Phase 3d-A artifact commit + this docs-only clarification commit.
- **Not yet merged.** Per explicit operator instruction in the Phase 3d-A brief: "Do not merge to main."
- **Phase 3d-B not started.** Per explicit operator instruction: "Do not start Phase 3d-B."

**Open Phase 3d-A recommendations (deferred to operator):**

- Phase 3d-A checkpoint §13: **GO (provisional) for Phase 3d-B authorization** if the operator wants to proceed with F1 evaluation. Remain-paused at the Phase 3d-A boundary continues to be the legitimate alternative if the operator prefers to hold indefinitely.
- All Phase 3c-affirmed restrictions stand: no paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write / threshold-change / project-lock change.

The branch can be merged to `main` and pushed when the operator authorizes the merge. No technical blocker exists.

---

**Stopped per operator instruction.** No file modified outside the Phase 3d-A scope. F1 backtests not run. F1 first-execution gate not computed. F1 V-window run not executed. Phase 3d-B not started. Branch `phase-3d-a/f1-implementation-controls` not pushed and not merged. Awaiting operator review.
