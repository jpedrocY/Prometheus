# Phase 3d-B1 — F1 Engine Wiring + H0/R3 Control Reproduction Checkpoint

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; **no post-hoc loosening per §11.3.5**); Phase 2i §1.7.3 project-level locks; Phase 2p §C.1 (R3 V1-breakout baseline-of-record); Phase 2y closeout (§11.6 = 8 bps HIGH preserved); Phase 3b F1 spec memo §§ 1–15 (binding spec); Phase 3c F1 execution-planning memo §§ 1–13 with operator-mandated amendments (§7.2(iv) BTC HIGH expR > 0; §7.3 MECHANISM PASS / FRAMEWORK FAIL — §11.6 cost-sensitivity blocks; §10.4 Phase 3d-A sequencing requirement); Phase 3c closeout + merge reports; Phase 3d-A checkpoint and closeout (F1 module + dispatch surface + locked config; engine path NOT wired; tests + quality gates + H0/R3 controls bit-for-bit).

**Phase:** 3d-B1 — F1 engine wiring + F1 output fields + lifecycle counters + runner scaffolding + tests + quality gates + H0/R3 control reproduction. Phase 3d-B1 deliberately does **not** execute any F1 candidate backtest, evaluate the §7.2 first-execution gate, run the F1 V-window, or compute M1/M2/M3 mechanism predictions. Phase 3d-B1 also does not start Phase 3d-B2.

**Branch:** `phase-3d-b1/f1-engine-wiring-controls`. **Date:** 2026-04-28 UTC.

**Status:** **Phase 3d-B1 PASSED.** F1 engine dispatch is wired into `BacktestEngine`; F1 lifecycle (entry / stop / target / time-stop / cooldown / accounting funnel) is implemented per Phase 3b §4 and Phase 3c §4–§4.7; `BacktestConfig` validator now accepts `strategy_family=MEAN_REVERSION_OVEREXTENSION` only when `mean_reversion_variant` is non-None and the V1 axes remain at defaults. 25 new tests added (5 BacktestConfig + 20 engine-dispatch tests); pytest 542 → 567 with no V1 regressions; ruff / format / mypy strict all green; H0/R3 control reproduction passes bit-for-bit on all 48 metric cells. **F1 remains deliberately unrun** — no F1 candidate backtest, §7.2 first-execution gate, M1/M2/M3 mechanism, or V-window run was executed in Phase 3d-B1. Per §1.1 below, F1 candidate execution and interpretation are reserved exclusively for Phase 3d-B2. **No `data/` artifacts committed.** **No project-lock, threshold, paper/shadow, Phase 4, live-readiness, deployment, MCP, Graphify, or credential change.** Phase 3d-B2 not started.

---

## 1. Plain-English explanation of what Phase 3d-B1 did

Phase 3d-B1 is the **engine-wiring-only** phase that makes F1 runnable through the backtest engine without yet running F1 itself. Phase 3d-A delivered the F1 self-contained module + primitives + locked `MeanReversionConfig` + `StrategyFamily`/`BacktestConfig` dispatch *surface* but kept F1 deliberately non-runnable through a hard validator guard. Phase 3d-B1 lifts that guard, adds the engine dispatch and per-bar lifecycle, the F1-specific TradeRecord fields and lifecycle counters, scaffolds the Phase 3d-B2 runner script, and proves with a fresh H0/R3 control reproduction that the new engine dispatch path does not perturb V1 baselines.

What Phase 3d-B1 explicitly did NOT do per the operator brief:

- No F1 candidate backtest of any kind (R or V; LOW / MED / HIGH; MARK / TRADE_PRICE).
- No F1 first-execution-gate evaluation per Phase 3c §7.2 conditions (i)–(v).
- No F1 mechanism-validation (M1/M2/M3) computation.
- No F1 V-window run.
- No mid-execution run-set expansion or threshold change.
- No Phase 3d-B2 work, paper/shadow planning, Phase 4 runtime/state/persistence work, live-readiness or deployment work.

The implementation strategy followed Phase 3c §4 minimal-contact-surface guidance and Phase 3d-A's pattern: F1 lives in its existing self-contained module; engine integration is a parallel `_run_symbol_f1` dispatch with an `is_f1` family guard at the top of `BacktestEngine.run`. V1 H0/R3/R1a/R1b-narrow/R2 paths are unchanged; bit-for-bit baseline reproduction proves it.

### 1.1 Phase boundary scope-accounting

**Completed in Phase 3d-B1:**

- Lifted the `BacktestConfig` Phase 3d-A guard that hard-rejected `strategy_family=MEAN_REVERSION_OVEREXTENSION`. The validator now requires `mean_reversion_variant` to be a non-None `MeanReversionConfig` and forbids non-default `strategy_variant` (V1 axes) on the F1 path.
- Implemented `BacktestEngine._run_symbol_f1` per-bar lifecycle: F1 entry detection at signal bar B's close (overextension event > 1.75 × ATR(20)(B)), market fill at open(B+1), frozen SMA(8)(B) target, frozen structural stop with 0.10 × ATR buffer, [0.60, 1.80] × ATR stop-distance band evaluated on the de-slipped raw open(B+1), same-bar STOP > TARGET > TIME_STOP priority, unconditional 8-bar time-stop, same-direction cooldown blocking until cumulative-displacement unwind.
- Added `F1LifecycleCounters` (analogous to `R2LifecycleCounters`) with `overextension_events_detected`, `overextension_events_filled`, `overextension_events_rejected_stop_distance`, `overextension_events_blocked_cooldown`, and `accounting_identity_holds` property.
- Added `_F1TradeMetadata` engine-side dataclass and threaded it through `_record_trade` so F1 trade rows populate the new TradeRecord fields with frozen-at-signal values; V1 rows keep NaN defaults and the parquet schema stays additive.
- Added F1 TradeRecord output fields: `overextension_magnitude_at_signal`, `frozen_target_value`, `entry_to_target_distance_atr`, `stop_distance_at_signal_atr` (NaN defaults for V1 rows; populated only on F1-family trades).
- Added 25 new tests: 5 `BacktestConfig` validator tests + 20 engine-dispatch / lifecycle / invariant tests in `tests/unit/research/backtest/test_engine_f1_dispatch.py`.
- Updated `tests/unit/research/backtest/test_trade_log.py` parquet-schema assertion for the four new F1 columns.
- Added a deliberately-guarded Phase 3d runner scaffold (`scripts/phase3d_F1_execution.py`) that imports the new F1 surface and exposes the Phase 3d-B2 CLI argument shape but **refuses to execute any F1 backtest** without a `--phase-3d-b2-authorized` flag.
- All four quality gates green: `uv run pytest` (567 passed), `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy src`.
- H0/R3 control reproduction bit-for-bit on all 48 metric cells (4 control runs × 2 symbols × 6 metrics).

**Deferred to Phase 3d-B2 (mandatory before any F1 result can be produced or interpreted):**

- F1 R-window candidate backtests: F1 R MED MARK (governing run #1), F1 R LOW MARK (#2 LOW cost-sensitivity), F1 R HIGH MARK (#3 §11.6 HIGH cost-sensitivity gate), F1 R MED TRADE_PRICE (#4 stop-trigger sensitivity).
- F1 V-window run #5 (F1 V MED MARK), conditional on §7.2 PROMOTE outcome at run #1.
- F1 first-execution-gate evaluation per Phase 3c §7.2 conditions (i)–(v).
- F1 M1 / M2 / M3 mechanism computation per Phase 3c §9.
- F1 Phase 3c §8 mandatory diagnostics (trade count, long/short split, per-regime decomposition, per-fold consistency, exit-reason fractions, overextension-magnitude / distance-to-mean / entry-to-target / stop-distance distributions, cost-sensitivity, mark-vs-trade-price sensitivity, MFE/MAE distributions, cross-family reference comparisons, P.14 hard-block checks).
- The Phase 3d-B2 runner script's full run-loop, dataset-citation wiring, and report writer.
- The Phase 3d-B2 analysis script that consumes F1 summary metrics + trade logs and produces the §7.3 verdict.

The deferred items above are mandatory Phase 3d-B2 work. No F1 first-execution-gate condition or mechanism prediction can be evaluated until those items are implemented, executed, and reviewed.

## 2. Files changed

### 2.1 Files modified — engine + config + trade_log (3 files)

| File | Change | Why |
|------|-------:|-----|
| `src/prometheus/research/backtest/config.py` | +29 / −12 | Replaced the Phase 3d-A guard that hard-rejected `MEAN_REVERSION_OVEREXTENSION` with a positive-validation rule: F1 dispatch requires `mean_reversion_variant` non-None and forbids non-default `strategy_variant`; updated `StrategyFamily` enum docstring to reflect Phase 3d-B1 dispatch. |
| `src/prometheus/research/backtest/engine.py` | +480 / −16 | Added `import math`, `wilder_atr` import, `MeanReversionStrategy` / `can_re_enter` / `overextension_event` imports, `StrategyFamily` import. Added `_F1TradeMetadata`, `F1LifecycleCounters`, `_OpenTrade.f1_metadata`, `_SymbolRun.f1_counters`/`f1_last_exit_*`, `BacktestRunResult.f1_counters_per_symbol`. Added `BacktestEngine._mean_reversion_strategy` constructed only when family is F1. Dispatch in `BacktestEngine.run` based on `strategy_family`. Added `_run_symbol_f1`, `_open_f1_trade`, `_close_f1_trade_on_stop`, `_close_f1_trade_managed`, `_close_f1_trade_end_of_data`. Extended `_record_trade` to populate F1 TradeRecord fields when `f1_metadata` is set. |
| `src/prometheus/research/backtest/trade_log.py` | +24 / −0 | Added 4 F1 fields to `TradeRecord` (`overextension_magnitude_at_signal`, `frozen_target_value`, `entry_to_target_distance_atr`, `stop_distance_at_signal_atr`) defaulting to NaN. Added the corresponding 4 columns to the parquet schema. |

### 2.2 Files modified — tests (2 files)

| File | Change | Why |
|------|-------:|-----|
| `tests/unit/research/backtest/test_config.py` | +63 / −0 | 5 new F1 BacktestConfig validator tests. |
| `tests/unit/research/backtest/test_trade_log.py` | +6 / −0 | Added the 4 F1 column names to the parquet schema assertion. |

### 2.3 Files created — F1 engine tests + runner scaffold (2 files)

| File | Lines | Content |
|------|------:|---------|
| `tests/unit/research/backtest/test_engine_f1_dispatch.py` | ~580 | 20 engine-level F1 tests: dispatch acceptance / no-signal-on-flat / long entry / short entry / below-band rejection / above-band rejection / raw-vs-slipped band reference / target fill at next-bar open / target close-confirmation only / time-stop at 8-bar horizon / STOP > TARGET priority / TARGET > TIME_STOP priority / cooldown blocks same-direction re-entry / cooldown releases after unwind / frozen target invariant / frozen stop invariant / accounting identity / no V1-only exit reasons / V1 H0 default unchanged / direction-vs-displacement-sign consistency. |
| `scripts/phase3d_F1_execution.py` | ~140 | Deliberate Phase 3d-B1 scaffold. `check-imports` verifies the F1 engine surface imports cleanly. `f1` action accepts the Phase 3d-B2 CLI argument shape (`--variant F1`, `--window R/V`, `--slippage LOW/MED/HIGH`, `--stop-trigger MARK_PRICE/TRADE_PRICE`) but is hard-guarded by `--phase-3d-b2-authorized`; without that flag, `f1` exits with status 2 and a "Phase 3d-B1 forbids F1 candidate backtest execution" message. |

### 2.4 Files NOT modified

- `src/prometheus/strategy/v1_breakout/` — entire V1 module unchanged.
- `src/prometheus/strategy/mean_reversion_overextension/` — entire F1 strategy module unchanged (Phase 3d-A primitives preserved verbatim).
- `src/prometheus/research/backtest/diagnostics.py` — unchanged (Phase 3c-mandated F1 funnel diagnostics integration is Phase 3d-B2 scope).
- `src/prometheus/research/backtest/report.py` — unchanged (Phase 3d-B2 will extend `compute_summary_metrics` for F1 exit-reason counters).
- `src/prometheus/strategy/types.py` — unchanged (TARGET ExitReason was added in Phase 3d-A).
- All existing pre-Phase-3d-B1 tests — preserved bit-for-bit.
- `data/`, `.claude/`, `.mcp.json`, configuration / credentials — untouched.
- All existing docs (current-project-state, ai-coding-handoff, phase-gates, technical-debt-register, validation-checklist, cost-modeling, backtesting-principles, data-requirements, dataset-versioning, v1-breakout-strategy-spec, Phase 3a/3b/3c/3d-A memos and reports) — unchanged.

## 3. Implementation summary

### 3.1 BacktestConfig — F1 dispatch acceptance

`BacktestConfig._check` now positively validates the F1 family:

- `strategy_family == V1_BREAKOUT` ⇒ `mean_reversion_variant` must be None (unchanged from Phase 3d-A).
- `strategy_family == MEAN_REVERSION_OVEREXTENSION` ⇒ `mean_reversion_variant` must be a non-None `MeanReversionConfig` AND `strategy_variant` must equal the default `V1BreakoutConfig()` (F1 does not consume V1 axes).

The validator's previous Phase 3d-A `ValueError("Phase 3d-A: F1 strategy_family is reserved; engine dispatch will be wired in Phase 3d-B")` guard is removed; F1 backtests are now constructible and runnable through the engine.

### 3.2 Engine dispatch surface

`BacktestEngine.__init__` constructs `self._mean_reversion_strategy: MeanReversionStrategy | None`. It is non-None only when `config.strategy_family == MEAN_REVERSION_OVEREXTENSION` and `config.mean_reversion_variant is not None`. This mirrors the V1 path's `self._strategy = V1BreakoutStrategy(config.strategy_variant)` which remains constructed unconditionally to preserve V1 default behavior.

`BacktestEngine.run` adds a single guard:

```python
is_f1 = self._config.strategy_family == StrategyFamily.MEAN_REVERSION_OVEREXTENSION
```

When `is_f1` is True, per-symbol iteration calls `_run_symbol_f1`; when False, the existing `_run_symbol` path is preserved bit-for-bit. Since F1 has no 1h bias filter (Phase 3b §4.8), the engine skips the 1h-data-missing warning when `is_f1`. All other input-presence warnings are unchanged.

### 3.3 F1 per-bar lifecycle (`_run_symbol_f1`)

The F1 lifecycle precomputes per-symbol arrays once (`closes`, `highs`, `lows`, `wilder_atr(.., period=20)`, and 8-bar displacement history) then iterates bars in ascending `open_time`:

1. **Open trade — STOP check first.** If a trade is open, evaluate the protective stop on the configured stop-trigger source (mark-price or trade-price 15m bar). On stop hit, close via `_close_f1_trade_on_stop` (updates `f1_last_exit_direction`/`f1_last_exit_idx` for cooldown tracking). Continue to the next bar; entry is not evaluated.
2. **Open trade — TARGET / TIME_STOP after STOP.** Same-bar priority STOP > TARGET > TIME_STOP. TARGET fires when the bar's close crosses the frozen SMA(8)(B) (long: close ≥ target; short: close ≤ target); fill at next-bar open. TIME_STOP fires when `idx_15m - fill_bar_index >= time_stop_bars` (= 8); fill at next-bar open. End-of-data branch is END_OF_DATA at the current bar's close. Both TARGET and TIME_STOP only evaluate on bars `t > B` (signal bar), per Phase 3b §4.5 / §4.6.
3. **No open trade — entry evaluation.** Skip if outside the window or before the 8-bar warmup. Compute `overextension_event(...)` first (drives the funnel `detected` counter). Cooldown gate (`can_re_enter`) is checked next: cooldown-blocked events count `blocked_cooldown` and skip without invoking the strategy facade. Stop-distance admissibility is verified via `MeanReversionStrategy.evaluate_entry_signal(reference_price=raw_open(B+1))` — the de-slipped raw next-bar open per Phase 3b §4.9 / Phase 3c §11.4. Rejected entries count `rejected_stop_distance`. Filled entries count `filled` and call `_open_f1_trade`.
4. **End-of-window.** If a trade remains open at the last bar, close as END_OF_DATA at the last bar's close.

The funnel-counter ordering (cooldown gate before stop-distance gate) mechanically guarantees the accounting identity `detected = filled + rejected_stop_distance + blocked_cooldown`.

### 3.4 F1 trade open and close helpers

`_open_f1_trade` applies the engine's existing `entry_fill_price` slippage convention to the next bar's raw open, computes post-slip stop_distance for sizing, runs `compute_size`, and constructs `_OpenTrade` with `_F1TradeMetadata` carrying frozen signal-time values. Sizing rejection at fill time decrements the `filled` counter and increments `rejected_stop_distance`, preserving the accounting identity (mirroring R2's fill-time rejection handling).

`_close_f1_trade_on_stop`, `_close_f1_trade_managed`, and `_close_f1_trade_end_of_data` are F1-specific so they avoid `run.session.on_exit_recorded(...)` (which would crash for F1 because the V1 session has no active trade on the F1 path). They each call `_record_trade` (which now populates the F1 fields when `f1_metadata` is set), clear `run.open_trade`, and update `f1_last_exit_direction` / `f1_last_exit_idx` for cooldown tracking.

### 3.5 F1 TradeRecord fields and parquet schema

Four NaN-defaulting fields added to `TradeRecord` and the parquet schema:

- `overextension_magnitude_at_signal = |displacement(B)| / ATR(20)(B)`
- `frozen_target_value = SMA(8)(B)`
- `entry_to_target_distance_atr = |entry_fill_price - frozen_target_value| / ATR(20)(B)`
- `stop_distance_at_signal_atr = stop_distance / ATR(20)(B)` (raw, de-slipped per §11.4)

V1 rows keep NaN values; the parquet schema is purely additive so reading a Phase-3d-A trade-log file with a Phase-3d-B1 reader is forward-compatible (the new columns appear as NaN in old data).

## 4. Test summary

### 4.1 New tests added in Phase 3d-B1: 25

#### 4.1.1 `tests/unit/research/backtest/test_config.py` (5 new tests)

| Test | Covers |
|------|--------|
| `test_default_strategy_family_is_v1_breakout` | Default config preserves V1_BREAKOUT and `mean_reversion_variant=None`. |
| `test_v1_breakout_rejects_mean_reversion_variant` | V1 family + `mean_reversion_variant` raises ValidationError. |
| `test_f1_family_accepts_mean_reversion_variant` | F1 family + `MeanReversionConfig()` constructs cleanly. |
| `test_f1_family_requires_mean_reversion_variant` | F1 family without variant raises ValidationError (replaces the Phase 3d-A "F1 reserved" guard test). |
| `test_f1_family_rejects_non_default_v1_strategy_variant` | F1 family + non-default `V1BreakoutConfig` raises ValidationError. |

#### 4.1.2 `tests/unit/research/backtest/test_engine_f1_dispatch.py` (20 new tests)

| Operator-brief test ID | Test name | Covers |
|---|---|---|
| 5 (long) | `test_f1_engine_long_entry_on_downward_overextension` | F1 LONG fills on a downward overextension event. |
| 6 (short) | `test_f1_engine_short_entry_on_upward_overextension` | F1 SHORT fills on an upward overextension event. |
| 7 | `test_f1_engine_rejects_below_band_stop_distance` | Below-band stop_distance rejects entry; `rejected_stop_distance++`. |
| 8 | `test_f1_engine_rejects_above_band_stop_distance` | Above-band stop_distance rejects entry; `rejected_stop_distance++`. |
| 9 | `test_f1_engine_uses_raw_open_for_admissibility_not_slipped` | HIGH-slip fill where post-slip would land outside band but raw stays inside fills correctly; recorded `stop_distance_at_signal_atr` is in band. |
| 10 | `test_f1_engine_target_fills_at_next_bar_open` | Long target hit at close(t) ≥ frozen_target fills at open(t+1); `frozen_target_value` matches SMA(8)(B). |
| 11 | `test_f1_engine_target_requires_close_confirmation` | Intrabar wick above target without close confirmation does NOT exit. |
| 12 | `test_f1_engine_time_stop_fires_at_8_bars_from_fill` | TIME_STOP fires at `idx = fill_idx + 8` and fills at open of `idx + 1`. |
| 13 (STOP > TARGET) | `test_f1_engine_stop_takes_priority_over_target` | Same-bar STOP > TARGET. |
| 13 (TARGET > TIME_STOP) | `test_f1_engine_target_takes_priority_over_time_stop` | Same-bar TARGET > TIME_STOP at the time-stop bar. |
| 14 | `test_f1_engine_cooldown_blocks_same_direction_reentry` | Continuous-drop scenario blocks all post-stop same-direction overextension events; `blocked_cooldown >= 1`. |
| 15 | `test_f1_engine_cooldown_releases_after_unwind` | Flat-zone unwind allows a second fresh same-direction fill; `filled >= 2`. |
| 16 | `test_f1_engine_frozen_target_invariant` | Recorded `frozen_target_value` equals SMA(8)(B=28) = 95.5. |
| 17 | `test_f1_engine_frozen_stop_invariant` | Recorded `initial_stop` equals lowest_low([B-7..B]) − 0.10×ATR(20)(B). |
| 18 | `test_f1_engine_accounting_identity_holds_across_runs` | `accounting_identity_holds` post-run. |
| 19 | `test_f1_engine_emits_only_allowed_exit_reasons` | F1 emits only STOP / TARGET / TIME_STOP / END_OF_DATA on both long and short series; never TRAILING_BREACH / STAGNATION / TAKE_PROFIT. |
| 20 | `test_v1_h0_default_path_unchanged_with_f1_module_imported` | V1 default config produces no F1 strategy and empty F1 counters; the engine surface is non-perturbing. |
| 1–2 (engine warmup) | `test_f1_engine_accepts_dispatch_with_zero_warmup` | F1 engine returns gracefully on a too-short series with no overextension. |
| 1–2 (no-signal flat) | `test_f1_engine_no_signal_on_flat_series` | Flat series produces no overextension event. |
| Direction symmetry | `test_f1_signal_direction_consistency_with_overextension_sign` | +1 displacement → SHORT; −1 → LONG (both directions exercised end-to-end). |

### 4.2 pytest summary

- Pre-Phase-3d-B1 baseline: **542 tests** (Phase 3d-A merged state).
- Post-Phase-3d-B1: **567 tests** (delta = +25 = exactly the new tests).
- All tests pass: `567 passed in 11.29s`.
- Zero V1 regressions.

## 5. Quality-gate results

| Gate | Command | Result | Output |
|------|---------|--------|--------|
| Test suite | `uv run pytest` | **PASS** | `567 passed in 11.29s` |
| Linter | `uv run ruff check .` | **PASS** | `All checks passed!` |
| Formatter | `uv run ruff format --check .` | **PASS** | `144 files already formatted` |
| Type checker | `uv run mypy src` | **PASS** | `Success: no issues found in 57 source files` |

All four quality gates green. Per Phase 3c §10.4 sequencing requirement, quality gates passing is a precondition for proceeding to control reproduction; that precondition is satisfied.

## 6. H0/R3 control reproduction results

Per Phase 3c §10.2 baseline-preservation discipline + Phase 3c §10.4 Phase 3d-A/B1 sequencing requirement, the four V1 control runs reproduce locked Phase 2e/2l/2s baselines bit-for-bit on all 48 metric cells (4 runs × 2 symbols × 6 metrics = 48 cells).

### 6.1 H0 R MED MARK

| Symbol | Locked baseline | Phase 3d-B1 reproduction | Match |
|--------|-----------------|---------------------------|:-----:|
| BTCUSDT | n=33, WR=30.30%, expR=−0.459, PF=0.255, netPct=−3.39%, maxDD=−3.67% | n=33, WR=30.30%, expR=−0.4590, PF=0.2552, netPct=−3.39%, maxDD=−3.67% | ✓ |
| ETHUSDT | n=33, WR=21.21%, expR=−0.475, PF=0.321, netPct=−3.53%, maxDD=−4.13% | n=33, WR=21.21%, expR=−0.4752, PF=0.3207, netPct=−3.53%, maxDD=−4.13% | ✓ |

### 6.2 H0 V MED MARK

| Symbol | Locked baseline | Phase 3d-B1 reproduction | Match |
|--------|-----------------|---------------------------|:-----:|
| BTCUSDT | n=8, WR=25.00%, expR=−0.313, PF=0.541, netPct=−0.56%, maxDD=−0.87% | n=8, WR=25.00%, expR=−0.3132, PF=0.5410, netPct=−0.56%, maxDD=−0.87% | ✓ |
| ETHUSDT | n=14, WR=28.57%, expR=−0.174, PF=0.695, netPct=−0.55%, maxDD=−0.80% | n=14, WR=28.57%, expR=−0.1735, PF=0.6950, netPct=−0.55%, maxDD=−0.80% | ✓ |

### 6.3 R3 R MED MARK

| Symbol | Locked baseline | Phase 3d-B1 reproduction | Match |
|--------|-----------------|---------------------------|:-----:|
| BTCUSDT | n=33, WR=42.42%, expR=−0.240, PF=0.560, netPct=−1.77%, maxDD=−2.16% | n=33, WR=42.42%, expR=−0.2403, PF=0.5602, netPct=−1.77%, maxDD=−2.16% | ✓ |
| ETHUSDT | n=33, WR=33.33%, expR=−0.351, PF=0.474, netPct=−2.61%, maxDD=−3.65% | n=33, WR=33.33%, expR=−0.3511, PF=0.4736, netPct=−2.61%, maxDD=−3.65% | ✓ |

### 6.4 R3 V MED MARK

| Symbol | Locked baseline | Phase 3d-B1 reproduction | Match |
|--------|-----------------|---------------------------|:-----:|
| BTCUSDT | n=8, WR=25.00%, expR=−0.287, PF=0.580, netPct=−0.51%, maxDD=−1.06% | n=8, WR=25.00%, expR=−0.2873, PF=0.5799, netPct=−0.51%, maxDD=−1.06% | ✓ |
| ETHUSDT | n=14, WR=42.86%, expR=−0.093, PF=0.824, netPct=−0.29%, maxDD=−0.94% | n=14, WR=42.86%, expR=−0.0932, PF=0.8242, netPct=−0.29%, maxDD=−0.94% | ✓ |

### 6.5 Verdict

**All 48 metric cells reproduce bit-for-bit within recorded precision** (|delta| < 0.001 for expR/PF/netPct/maxDD; exact for n and WR%). The new F1 dispatch surface, lifecycle, counters, TradeRecord fields, and parquet schema additions are non-disturbing under the V1 default. V1 H0/R3 dispatch is preserved.

Generated control-run directories (git-ignored under `data/derived/backtests/`):
- `phase-2l-h0-r/2026-04-28T17-55-16Z/`
- `phase-2l-h0-v/2026-04-28T17-55-39Z/`
- `phase-2l-r3-r/2026-04-28T17-55-50Z/`
- `phase-2l-r3-v/2026-04-28T17-56-01Z/`

Per Phase 2u §J.6 / Phase 2w-A precedent / Phase 3d-A precedent, run artifacts in `data/derived/backtests/` are git-ignored; **no `data/` commit was made.**

## 7. Touched V1 files and why

Two V1-shared files were modified, both with **engine-internal additive changes only** that do not alter V1 control-flow under the V1 default:

### 7.1 `src/prometheus/research/backtest/engine.py` (+480 / −16)

The diff is large because Phase 3d-B1's primary work lives here: F1 imports, `_F1TradeMetadata`, `F1LifecycleCounters`, `_OpenTrade.f1_metadata`, `_SymbolRun.f1_*` fields, `BacktestRunResult.f1_counters_per_symbol`, `BacktestEngine._mean_reversion_strategy`, the `is_f1` dispatch in `run`, `_run_symbol_f1` per-bar lifecycle, `_open_f1_trade`, `_close_f1_trade_*` methods, and the F1-field population in `_record_trade`. **None of these alter the V1 dispatch path.**

V1 H0/R3 control reproduction (§6) directly proves V1 dispatch is bit-for-bit preserved.

### 7.2 `src/prometheus/research/backtest/trade_log.py` (+24)

Added 4 NaN-defaulting F1 fields to `TradeRecord` and 4 corresponding columns to the parquet schema. Field defaults are `float("nan")`, so V1 rows produced by the V1 dispatch path read identically to pre-Phase-3d-B1 (the new columns are NaN). The parquet schema-shape change is additive (4 new float64 columns at the end); old reports written before Phase 3d-B1 are forward-readable with the new schema (the new columns appear NaN), but the existing on-disk Phase 2 / Phase 3d-A artifacts under `data/derived/backtests/` are not rewritten — they remain on the old schema. Phase 3d-B1's H0/R3 control re-runs (§6) wrote fresh artifacts under the new schema.

### 7.3 `src/prometheus/research/backtest/config.py` (+29 / −12)

Replaced the Phase 3d-A guard that hard-rejected `MEAN_REVERSION_OVEREXTENSION` with a positive-validation rule. V1 default construction (no `strategy_family` keyword) is unchanged; the V1_BREAKOUT path's invariant (`mean_reversion_variant` must be None) is preserved.

**No other V1 source file was touched.**

## 8. Confirmation that no F1 candidate backtests were run

Confirmed. The only backtests executed in Phase 3d-B1 were the four V1 control runs (H0 R MED MARK, H0 V MED MARK, R3 R MED MARK, R3 V MED MARK) using the existing Phase 2l runner script. No invocation of the F1 strategy through the engine occurred. The `scripts/phase3d_F1_execution.py` scaffold was used only for `check-imports` (verifies the F1 surface imports cleanly) and to verify the `f1` action's hard guard; no F1 backtest was attempted under the `--phase-3d-b2-authorized` flag.

## 9. Confirmation that no F1 first-execution gate was evaluated

Confirmed. The Phase 3c §7.2 first-execution gate has five conditions (i)–(v):
- (i) Absolute BTC edge at MED slippage — NOT EVALUATED
- (ii) M1 BTC mechanism — NOT EVALUATED
- (iii) ETH non-catastrophic per §11.4 — NOT EVALUATED
- (iv) §11.6 HIGH-slippage cost-sensitivity — NOT EVALUATED
- (v) §10.4-style hard-reject absolute thresholds — NOT EVALUATED

None of these were computed in Phase 3d-B1. They are reserved for Phase 3d-B2 execution + analysis.

## 10. Confirmation that no F1 V-window run was executed

Confirmed. Per Phase 3c §6.2, run #5 (F1 V MED MARK) is conditional on Phase 3d-B2 governing-run §7.2 PROMOTE outcome. Phase 3d-B1 executed only V1 H0/R3 R-window and V-window controls (runs 6–9 from the §6 inventory), not run #5.

## 11. Confirmation that no `data/` artifacts were committed

Confirmed. `git status` shows zero `data/` entries. The four control runs wrote into the git-ignored `data/derived/backtests/` tree only. No `git add data/` was executed.

## 12. Confirmation that no forbidden areas changed

Confirmed across all forbidden categories per the Phase 3d-B1 operator brief:

| Category | Status |
|----------|--------|
| Phase 3b F1 spec axes (overextension window 8 / threshold 1.75 / mean-reference window 8 / stop-buffer 0.10 / time-stop 8 / stop-distance band [0.60, 1.80]) | LOCKED VERBATIM in `MeanReversionConfig` (Phase 3d-A) and consumed unmodified by Phase 3d-B1 engine code |
| Phase 3d-A F1 module + primitives + locked config | PRESERVED VERBATIM (no change to `src/prometheus/strategy/mean_reversion_overextension/`) |
| V1 breakout strategy module (`src/prometheus/strategy/v1_breakout/`) | UNCHANGED |
| V1 strategy logic, V1 entry/exit machinery, V1 setup predicate, V1 bias filter | UNCHANGED (control reproduction proves bit-for-bit) |
| Phase 2f thresholds (§10.3 / §10.4 / §11.3 / §11.4 / §11.6 = 8 bps HIGH) | PRESERVED VERBATIM |
| Strategy parameters (R3 sub-parameters; H0 baseline; R1a / R1b-narrow / R2 sub-parameters) | PRESERVED VERBATIM |
| §1.7.3 project-level locks (BTCUSDT-primary; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets) | PRESERVED VERBATIM |
| Phase 3c §6 run inventory | PRESERVED (no run-set expansion; F1 candidate runs reserved for Phase 3d-B2) |
| MCP / Graphify / `.mcp.json` | NOT ACTIVATED, NOT TOUCHED |
| Credentials / `.env` / API keys | NOT REQUESTED, NOT CREATED, NOT TOUCHED |
| Paper/shadow planning | NOT PROPOSED, NOT AUTHORIZED |
| Phase 4 (runtime / state / persistence) work | NOT PROPOSED, NOT AUTHORIZED |
| Live-readiness work, deployment, exchange-write capability, production keys | NOT PROPOSED, NOT AUTHORIZED |
| `docs/12-roadmap/technical-debt-register.md` | UNCHANGED |
| `docs/00-meta/implementation-ambiguity-log.md` | UNCHANGED |
| `.claude/` directory | UNCHANGED |
| Existing strategy / validation / cost / data / phase-gate / ai-coding-handoff / current-project-state specs | UNCHANGED |

**Project-state preservation:** R3 V1-breakout baseline-of-record per Phase 2p §C.1 stands; H0 V1-breakout framework anchor per Phase 2i §1.7.3 stands; R1a / R1b-narrow / R2 retained-research-evidence stand; R2 framework verdict FAILED — §11.6 cost-sensitivity blocks stands; §11.6 = 8 bps HIGH numerical threshold per Phase 2y closeout stands; Phase 2f §11.3.5 binding rule preserved; Phase 3b F1 spec preserved verbatim per Phase 3c §3 / Phase 3d-A scope.

## 13. Whether Phase 3d-B2 is safe to authorize

**Phase 3d-B2 is technically safe to authorize**, conditional on operator decision. The Phase 3d-B1 precondition for F1 candidate execution is met:

- Engine wiring is complete and tested through 25 new tests + 542 preserved tests.
- All four quality gates are green.
- V1 H0/R3 control reproduction is bit-for-bit on all 48 metric cells, proving the new dispatch path does not perturb V1.
- F1 funnel-counter accounting identity is enforced and tested.
- F1 emits only the spec'd exit reasons (STOP / TARGET / TIME_STOP / END_OF_DATA) — no V1-only exit-reason leakage.
- F1 frozen-target / frozen-stop invariants hold and are tested.
- F1 cooldown gating is correctly implemented (block-then-release tested end-to-end).
- F1 same-bar exit priority STOP > TARGET > TIME_STOP holds.
- The Phase 3d-B2 runner script is scaffolded and hard-guarded against accidental F1 execution.

**What Phase 3d-B2 (if authorized) would do:**

- Implement the runner script's full run-loop, dataset citation, and per-symbol report writer to support runs #1–#4 (and conditional #5).
- Execute the four mandatory F1 governing/sensitivity runs (F1 R MED MARK, F1 R LOW MARK, F1 R HIGH MARK, F1 R MED TRADE_PRICE) per Phase 3c §6.1.
- Execute the conditional F1 V MED MARK run (run #5) only if §7.2 PROMOTE.
- Compute the §7.2 first-execution gate, §9 mechanism predictions M1/M2/M3, and the full §8 mandatory diagnostics.
- Produce the Phase 3d-B2 variant-comparison report with the §7.3 verdict.

**What Phase 3d-B2 should NOT do:**

- No paper/shadow planning. No Phase 4. No live-readiness. No deployment. No production keys. No exchange-write capability. No threshold change. No project-lock change. No spec change to Phase 3b §4.

**Recommendation:** GO (provisional) for Phase 3d-B2 if the operator wants to proceed with F1 evaluation. Remain-paused at the Phase 3d-B1 boundary continues to be the legitimate alternative if the operator prefers to hold indefinitely. Either choice preserves project state.

---

**End of Phase 3d-B1 checkpoint report.** **Phase 3d-B1 PASSED:** F1 engine dispatch wired into `BacktestEngine`; F1 lifecycle (entry / stop / target / time-stop / cooldown / accounting funnel) implemented and tested; F1 TradeRecord output fields + lifecycle counters + runner scaffolding added; pytest 542 → 567 with no V1 regressions; ruff / format / mypy strict all green; H0/R3 control reproduction bit-for-bit on all 48 metric cells. **F1 remains deliberately unrun** — the runner's `f1` action is hard-guarded by `--phase-3d-b2-authorized`. Per §1.1, the deferred-to-Phase-3d-B2 items (F1 R-window candidate runs, conditional V-window run, §7.2 first-execution-gate evaluation, §9 M1/M2/M3 mechanism computation, §8 mandatory diagnostics, runner full run-loop, analysis script, variant-comparison report) are mandatory Phase 3d-B2 work before any F1 result can be produced or interpreted. **No F1 candidate backtests run; no F1 first-execution gate evaluated; no F1 V-window run executed; no `data/` commits.** Phase 3d-B2 not started; the operator decides whether to authorize it. R3 V1-breakout baseline-of-record / H0 V1-breakout framework anchor / R1a-R1b-narrow-R2 retained-research-evidence preserved. §11.6 = 8 bps HIGH per Phase 2y closeout preserved. §1.7.3 project-level locks preserved verbatim. Phase 3b F1 spec preserved verbatim per Phase 3c §3 / Phase 3d-A scope. Awaiting operator review.
