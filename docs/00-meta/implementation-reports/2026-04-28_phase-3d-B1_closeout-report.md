# Phase 3d-B1 Closeout Report

**Phase:** 3d-B1 — F1 (mean-reversion-after-overextension) engine wiring + F1 output fields + lifecycle counters + runner scaffolding + tests + quality gates + H0/R3 control reproduction. Phase 3d-B1 deliberately does **not** execute any F1 candidate backtest, evaluate the §7.2 first-execution gate, run the F1 V-window, or compute M1/M2/M3 mechanism predictions.

**Date:** 2026-04-28 UTC.

**Status:** **Phase 3d-B1 PASSED.** F1 engine dispatch is wired into `BacktestEngine` per Phase 3b §4 and Phase 3c §4–§4.7. `BacktestConfig` now accepts `strategy_family=MEAN_REVERSION_OVEREXTENSION` only when `mean_reversion_variant` is non-None and the V1 axes remain at defaults. 25 new tests added (5 BacktestConfig + 20 engine-dispatch); pytest 542 → 567 with no V1 regressions; ruff / format / mypy strict all green; H0/R3 control reproduction passes bit-for-bit on all 48 metric cells. **F1 remains deliberately unrun** — no F1 candidate backtest, §7.2 first-execution gate, M1/M2/M3 mechanism, or V-window run was executed. Phase 3d-B2 not started. Branch `phase-3d-b1/f1-engine-wiring-controls` not pushed and not merged. Awaiting operator review.

---

## 1. Current branch

```
phase-3d-b1/f1-engine-wiring-controls
```

Branched from `main` at `e820acd71d9c9c3384a7c448666d9bcb8159af5c` (the post-Phase-3d-A merge-report tip). Not pushed. Not merged.

## 2. Git status

After all Phase 3d-B1 commits:

```
On branch phase-3d-b1/f1-engine-wiring-controls
nothing to commit, working tree clean
```

(State as of immediately after the final Phase 3d-B1 commit, which includes the implementation files, tests, runner scaffold, and these two reports.)

## 3. Files changed

Total: **8 files** added or modified across the entire Phase 3d-B1 branch (vs `main`):

### 3.1 Modified — engine + config + trade_log (3 files)

- [src/prometheus/research/backtest/config.py](../../../src/prometheus/research/backtest/config.py) (+29 / −12): Lifted Phase 3d-A guard rejecting `MEAN_REVERSION_OVEREXTENSION`; added positive validation requiring `mean_reversion_variant` non-None and forbidding non-default V1 `strategy_variant` on the F1 path.
- [src/prometheus/research/backtest/engine.py](../../../src/prometheus/research/backtest/engine.py) (+480 / −16): F1 engine wiring — `_F1TradeMetadata`, `F1LifecycleCounters`, `_OpenTrade.f1_metadata`, `_SymbolRun.f1_*` fields, `BacktestRunResult.f1_counters_per_symbol`, `BacktestEngine._mean_reversion_strategy`, `is_f1` dispatch in `run`, `_run_symbol_f1` per-bar lifecycle, `_open_f1_trade`, `_close_f1_trade_*` close helpers, F1-field population in `_record_trade`.
- [src/prometheus/research/backtest/trade_log.py](../../../src/prometheus/research/backtest/trade_log.py) (+24 / −0): 4 F1 NaN-default fields on `TradeRecord` and 4 corresponding columns in the parquet schema.

### 3.2 Modified — tests (2 files)

- [tests/unit/research/backtest/test_config.py](../../../tests/unit/research/backtest/test_config.py) (+63 / −0): 5 new F1 BacktestConfig validator tests.
- [tests/unit/research/backtest/test_trade_log.py](../../../tests/unit/research/backtest/test_trade_log.py) (+6 / −0): Added the 4 F1 column names to the parquet schema assertion.

### 3.3 Created — F1 engine tests + runner scaffold + reports (3 files in this changeset, 2 + this closeout)

- [tests/unit/research/backtest/test_engine_f1_dispatch.py](../../../tests/unit/research/backtest/test_engine_f1_dispatch.py) (~580 lines): 20 engine-level F1 tests covering dispatch acceptance / no-signal-on-flat / long entry / short entry / below-band rejection / above-band rejection / raw-vs-slipped band reference / target fill timing / target close-confirmation only / time-stop horizon / STOP > TARGET priority / TARGET > TIME_STOP priority / cooldown blocks / cooldown releases / frozen-target invariant / frozen-stop invariant / accounting identity / no V1-only exit reasons / V1 H0 default unchanged / direction-vs-displacement consistency.
- [scripts/phase3d_F1_execution.py](../../../scripts/phase3d_F1_execution.py) (~140 lines): Phase 3d-B1 scaffold. `check-imports` verifies the F1 engine surface imports cleanly. `f1` action accepts the Phase 3d-B2 CLI argument shape but is hard-guarded by `--phase-3d-b2-authorized`; without that flag, exits with status 2 and a "Phase 3d-B1 forbids F1 candidate backtest execution" message.
- [docs/00-meta/implementation-reports/2026-04-28_phase-3d-B1_F1_engine-wiring-control-checkpoint.md](2026-04-28_phase-3d-B1_F1_engine-wiring-control-checkpoint.md) (Phase 3d-B1 checkpoint report; 13 brief-required items).
- [docs/00-meta/implementation-reports/2026-04-28_phase-3d-B1_closeout-report.md](2026-04-28_phase-3d-B1_closeout-report.md) — this file (7 brief-required items).

### 3.4 Files NOT touched

- `src/prometheus/strategy/v1_breakout/` — entire V1 module unchanged.
- `src/prometheus/strategy/mean_reversion_overextension/` — Phase 3d-A primitives preserved verbatim.
- `src/prometheus/research/backtest/diagnostics.py`, `report.py` — unchanged (Phase 3d-B2 will integrate F1 funnel diagnostics + summary metrics).
- `src/prometheus/strategy/types.py` — unchanged (TARGET ExitReason added in Phase 3d-A).
- All existing pre-Phase-3d-B1 tests — preserved bit-for-bit.
- `scripts/` — only `phase3d_F1_execution.py` added; existing runner scripts (`phase2l_R3_first_execution.py` etc.) used unmodified for control reproduction.
- `data/`, `.claude/`, `.mcp.json`, configuration / credentials — untouched.
- All existing docs (current-project-state, ai-coding-handoff, phase-gates, technical-debt-register, validation-checklist, cost-modeling, backtesting-principles, data-requirements, dataset-versioning, v1-breakout-strategy-spec, Phase 3a/3b/3c/3d-A memos and reports) — unchanged.

## 4. Commit hash or hashes

The Phase 3d-B1 branch is built on top of `main` at `e820acd71d9c9c3384a7c448666d9bcb8159af5c` (the post-Phase-3d-A merge-report tip). The full commit chain on `phase-3d-b1/f1-engine-wiring-controls` (`main` → branch tip):

| Commit | Short SHA | Full SHA | Description |
|--------|-----------|----------|-------------|
| 1 | `fd0a9ca` | `fd0a9ca24677a2971639dbd6831d91416c32c5a8` | `phase-3d-B1: F1 engine wiring + tests + quality gates + H0/R3 control reproduction` — original Phase 3d-B1 artifact commit (9 files; +1990 / −28): engine dispatch wiring (`engine.py`), config validator update (`config.py`), TradeRecord F1 fields + parquet schema (`trade_log.py`), 5 BacktestConfig tests + 20 engine tests + parquet-schema test update, runner scaffold (`scripts/phase3d_F1_execution.py`), Phase 3d-B1 checkpoint report (initial), Phase 3d-B1 closeout report (initial). |
| 2 | `1da8748` | `1da87480d73873d95153bb3f0d1e79cff2ffc202` | `docs(phase-3d-B1): clerical fix to closeout §4 commit-hash listing` — docs-only clerical-fix commit recording the actual SHAs of commit 1 in this §4. No code, tests, scripts, config, data, threshold, parameter, or project-lock change. No alteration of metrics, quality-gate outputs, H0/R3 control reproduction values, scope boundaries, or recommendations. |

The branch is therefore **2 commits ahead of `main`** at the time of any future merge. A `--no-ff` merge will preserve both commits in history and add a single explicit merge commit.

## 5. Phase 3d-B1 was limited to engine wiring + tests + quality gates + H0/R3 control reproduction

Confirmed. Phase 3d-B1's scope per the operator brief is **engine wiring + F1 output fields + lifecycle counters + runner scaffolding + tests + quality gates + H0/R3 control reproduction**. The completed work matches that scope:

1. **Engine wiring.** `BacktestConfig._check` lifted the Phase 3d-A F1 guard and validates the F1 dispatch surface positively. `BacktestEngine.__init__` constructs `MeanReversionStrategy` only when family is F1. `BacktestEngine.run` dispatches to `_run_symbol_f1` when family is F1. `_run_symbol_f1` implements the full per-bar lifecycle: detect → cooldown gate → stop-distance gate → fill at open(B+1) → STOP/TARGET/TIME_STOP precedence → cooldown state update on exit.
2. **F1 output fields.** `TradeRecord` carries `overextension_magnitude_at_signal`, `frozen_target_value`, `entry_to_target_distance_atr`, `stop_distance_at_signal_atr` with NaN defaults; populated only on F1-family trades. Parquet schema is additive.
3. **Lifecycle counters.** `F1LifecycleCounters` mirrors `R2LifecycleCounters` with `overextension_events_detected / filled / rejected_stop_distance / blocked_cooldown` and `accounting_identity_holds`. The engine's funnel-attribution order (cooldown gate before stop-distance gate) mechanically guarantees the identity.
4. **Runner scaffolding.** `scripts/phase3d_F1_execution.py` is a deliberately-guarded Phase 3d-B2 stub. Its `check-imports` action verifies F1 imports; its `f1` action exits with status 2 and a hard-guard message unless `--phase-3d-b2-authorized` is passed. Phase 3d-B1 ran the `check-imports` action only.
5. **Tests.** 25 new tests (5 BacktestConfig + 20 engine dispatch). Total 567 passing.
6. **Quality gates.** All four green: `pytest` (567 passed), `ruff check`, `ruff format --check`, `mypy src`.
7. **H0/R3 control reproduction.** Bit-for-bit on all 48 metric cells (4 control runs × 2 symbols × 6 metrics).

Phase 3d-B1 did NOT execute any F1 candidate backtest, evaluate any F1 first-execution-gate condition, compute any F1 mechanism prediction (M1/M2/M3), or run the F1 V-window. Phase 3d-B1 also did not commence Phase 3d-B2.

## 6. Confirmation that F1 results were not run or interpreted

Confirmed. Per the operator brief and Phase 3c §10.4 sequencing requirement, F1 result execution and interpretation are reserved for Phase 3d-B2. Specifically:

- **No F1 backtest invoked.** The only backtests executed in Phase 3d-B1 were the four V1 H0/R3 control runs (`phase2l_R3_first_execution.py --variant H0/R3 --window R/V`). The new `scripts/phase3d_F1_execution.py` was used only for `check-imports` (no run-loop) and to verify the `f1` action's hard guard (status 2 without `--phase-3d-b2-authorized`).
- **No F1 first-execution gate computed.** Phase 3c §7.2 conditions (i)–(v) — BTC MED expR > 0; M1 BTC mechanism; ETH non-catastrophic; §11.6 HIGH-slip BTC expR > 0; §10.4-style absolute floors — were not evaluated. No F1 expR / PF / netPct / maxDD on F1 trades exists.
- **No F1 mechanism-validation (M1/M2/M3) computed.** Phase 3c §9 metrics not produced. M1 (post-entry counter-displacement at horizons {1,2,4,8}) not computed. M2 (chop-regime stop-out fraction) not computed. M3 (TARGET-exit aggregate net-of-cost contribution) not computed.
- **No F1 V-window run executed.** Per Phase 3c §6.2, run #5 is conditional on Phase 3d-B2 governing-run §7.2 PROMOTE outcome; no PROMOTE has been computed, so V-window has not been triggered.

The four V1 control runs executed in Phase 3d-B1 reproduced locked Phase 2e/2l/2s baselines bit-for-bit on all 48 metric cells, proving V1 dispatch is unchanged. F1 remains deliberately unrun.

## 7. Whether the branch is ready for operator review

**Ready for review on its scope-limited objective.** Phase 3d-B1's engine-wiring objective passed; the branch is technically and procedurally ready for operator review and possible merge. However, "ready for review" applies only to the Phase 3d-B1 scope — the deferred-to-Phase-3d-B2 items (F1 R-window candidate runs, conditional V-window, §7.2 first-execution-gate evaluation, §9 mechanism predictions, §8 mandatory diagnostics, runner full run-loop, analysis script, variant-comparison report) are mandatory Phase 3d-B2 work before any F1 result can be produced or interpreted; they are not implied by this branch's readiness.

- **Technically ready (Phase 3d-B1 scope):**
  - Branch is clean (`nothing to commit, working tree clean` after the Phase 3d-B1 commit).
  - All 4 quality gates green (`pytest`: 567 passed; `ruff check`: All checks passed; `ruff format --check`: 144 files already formatted; `mypy src`: Success no issues).
  - All 48 H0/R3 control cells reproduce bit-for-bit on locked Phase 2 baselines.
  - F1 engine path is wired and tested through 25 new tests covering brief-required items 1–22 (BacktestConfig acceptance / rejection; long / short signals; band rejection; raw-vs-slipped; target fill at next-bar open; close-only target confirmation; time-stop horizon; same-bar STOP > TARGET > TIME_STOP priority; cooldown block + release; frozen invariants; accounting identity; allowed-only exit reasons; V1 H0 unchanged).
  - Runner scaffold present and hard-guarded against accidental F1 execution.
  - No `data/` commits.
- **Procedurally ready (Phase 3d-B1 scope):**
  - Phase 3b F1 spec axes consumed verbatim from Phase 3d-A `MeanReversionConfig` (no spec change).
  - Phase 3c §3 forbidden adjustments not made (no overextension-threshold / window-length / stop-distance band / stop-buffer / regime-filter / confirmation-candle / cooldown / target-reference / entry-fill-model change).
  - Phase 3c §10.4 Phase 3d-A/B sequencing requirement satisfied (implement → quality gates pass → H0/R3 reproduction bit-for-bit; F1 results NOT computed because Phase 3d-B1 does not run F1 candidates).
  - Phase 3c §6 run inventory respected (only the 4 V1 control runs executed; F1 candidate runs reserved for Phase 3d-B2).
  - Phase 3c §7.4 cross-family-fairness preserved (F1 not yet evaluated; cross-family deltas not yet computed).
- **NOT yet ready (deferred to Phase 3d-B2):** F1 R/V candidate run results, F1 §7.2 first-execution gate evaluation, F1 §9 mechanism (M1/M2/M3) computation, F1 §8 mandatory diagnostics, F1 §7.3 verdict outcome, F1 variant-comparison report. This branch does not produce or interpret any F1 result; it only proves the engine path exists, behaves to spec, and does not perturb V1.
- **Merge mechanics if/when operator approves:** would be a `--no-ff` merge commit consistent with the prior Phase 2x / Phase 2y / Phase 3a / Phase 3b / Phase 3c / Phase 3d-A merge pattern, producing a merge commit on `main` of the form `Merge Phase 3d-B1 (F1 engine wiring + control reproduction) into main`.
- **Not yet merged.** Per explicit operator instruction in the Phase 3d-B1 brief: "Do not merge to main."
- **Phase 3d-B2 not started.** Per explicit operator instruction: "Do not start Phase 3d-B2."

**Open Phase 3d-B1 recommendations (deferred to operator):**

- Phase 3d-B1 checkpoint §13: **GO (provisional) for Phase 3d-B2 authorization** if the operator wants to proceed with F1 evaluation. Remain-paused at the Phase 3d-B1 boundary continues to be the legitimate alternative if the operator prefers to hold indefinitely.
- All Phase 3c-affirmed restrictions stand: no paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write / threshold-change / project-lock change.

The branch can be merged to `main` and pushed when the operator authorizes the merge. No technical blocker exists.

---

**Stopped per operator instruction.** No file modified outside the Phase 3d-B1 scope. F1 backtests not run. F1 first-execution gate not computed. F1 V-window run not executed. Phase 3d-B2 not started. Branch `phase-3d-b1/f1-engine-wiring-controls` not pushed and not merged. Awaiting operator review.
