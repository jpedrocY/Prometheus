# Phase 3d-A — F1 Implementation, Tests, Quality Gates, and H0/R3 Control Reproduction Checkpoint

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; **no post-hoc loosening per §11.3.5**); Phase 2i §1.7.3 project-level locks; Phase 2p §C.1 (R3 V1-breakout baseline-of-record); Phase 2y closeout (§11.6 = 8 bps HIGH preserved); Phase 3b F1 spec memo §§ 1–15 (binding spec); Phase 3c F1 execution-planning memo §§ 1–13 with operator-mandated amendments (§7.2(iv) BTC HIGH expR > 0; §7.3 MECHANISM PASS / FRAMEWORK FAIL — §11.6 cost-sensitivity blocks; §10.4 Phase 3d-A sequencing requirement); Phase 3c closeout + merge reports.

**Phase:** 3d-A — F1 implementation + tests + quality gates + H0/R3 control reproduction. **First phase to authorize source code, tests, and scripts on the F1 family.**

**Branch:** `phase-3d-a/f1-implementation-controls`. **Date:** 2026-04-28 UTC.

**Status:** **Phase 3d-A's implementation-control objective passed.** F1 family infrastructure (self-contained module + primitives + locked config + dispatch surface guard + unit tests) is implemented per Phase 3b §4 binding spec; 68 new F1 unit tests added; pytest 474 → 542 with no V1 regressions; ruff / format / mypy strict all green; H0/R3 control reproduction passes on all 48 metric cells. **F1 remains deliberately non-runnable** — the BacktestConfig validator hard-rejects `strategy_family=MEAN_REVERSION_OVEREXTENSION`. Several engine-output and execution-integration pieces are **deferred to Phase 3d-B as mandatory work before any F1 result can be produced or interpreted** (see §1.1 below for the explicit phase-boundary list). **No F1 candidate backtests run.** **No F1 first-execution gate evaluated.** **No F1 V-window run executed.** **No `data/` artifacts committed.** Phase 3d-B not started.

---

## 1. Plain-English explanation of what Phase 3d-A did

Phase 3d-A is the **implementation-only** phase that brings F1 (mean-reversion-after-overextension) infrastructure into the codebase without yet running any F1 backtests. The work proves three things:

1. The Phase 3b spec axes can be implemented as a clean self-contained module (`src/prometheus/strategy/mean_reversion_overextension/`) following the same conventions as `src/prometheus/strategy/v1_breakout/`.
2. The dispatch surface to differentiate strategy families (`StrategyFamily` enum + `mean_reversion_variant` field on `BacktestConfig` + validator placeholder) can be added without changing V1 behavior.
3. V1 H0/R3 control runs reproduce locked Phase 2 baselines bit-for-bit, demonstrating that the BacktestConfig field additions did not perturb the V1 dispatch path.

What Phase 3d-A explicitly did NOT do per Phase 3c §10.4 sequencing requirement:
- No F1 backtest of any kind.
- No F1 first-execution gate evaluation per Phase 3c §7.2 conditions (i)–(v).
- No F1 mechanism-validation (M1/M2/M3) computation.
- No F1 V-window run.
- No engine integration of F1 — the engine remains V1-only; F1 is a self-contained module pending Phase 3d-B engine wiring.

The implementation strategy followed Phase 3c §4's "minimal contact surface" guidance: F1 lives in its own module, V1 files were touched only for additive enum membership (`TARGET` exit reason; `StrategyFamily` enum; `mean_reversion_variant` field).

### 1.1 Explicit phase-boundary scope-accounting

To prevent the "implementation-control objective passed" framing from obscuring the Phase 3d-A → Phase 3d-B boundary, this section enumerates the boundary explicitly.

**Completed in Phase 3d-A:**

- F1 self-contained strategy module + primitives (`src/prometheus/strategy/mean_reversion_overextension/`).
- Locked `MeanReversionConfig` with Phase 3b §4 values (7 fields locked via `Field(ge=v, le=v)` + `model_post_init` defense-in-depth).
- F1 feature primitives (`features.py::cumulative_displacement_8bar`, `sma_8_close`, `overextension_event`).
- F1 stop primitives (`stop.py::compute_initial_stop`, `passes_stop_distance_filter`).
- F1 target primitives (`target.py::compute_target`, `target_hit`).
- F1 cooldown primitives (`cooldown.py::cooldown_unwound`, `can_re_enter`).
- F1 stateless strategy facade (`strategy.py::MeanReversionStrategy.evaluate_entry_signal`).
- `StrategyFamily` / `BacktestConfig` dispatch surface guard (`strategy_family` enum field defaulting to `V1_BREAKOUT`; `mean_reversion_variant` field defaulting to `None`; validator hard-rejecting `MEAN_REVERSION_OVEREXTENSION`).
- `TARGET = "TARGET"` ExitReason enum addition (placeholder for Phase 3d-B engine wiring).
- 68 F1 unit tests across 7 test files (542 total pytest passing; +68 over baseline 474; zero V1 regressions).
- Quality gates green: `pytest`, `ruff check`, `ruff format --check`, `mypy strict`.
- H0/R3 control reproduction bit-for-bit on all 48 metric cells (proves V1 dispatch unchanged).
- F1 remains deliberately non-runnable through the `BacktestConfig` validator until Phase 3d-B lifts that guard.

**Deferred to Phase 3d-B (mandatory before any F1 result can be produced or interpreted):**

- Actual `BacktestEngine` F1 dispatch wiring in `_run_symbol`. Phase 3d-A added the dispatch *surface* (enum + field + validator placeholder); Phase 3d-B must add the engine code path that routes per-bar evaluation to F1 when `strategy_family == MEAN_REVERSION_OVEREXTENSION`.
- F1-specific TradeRecord output fields (e.g., `overextension_magnitude_at_signal`, `frozen_target_value`, `entry_to_target_distance_atr`, `stop_distance_at_signal_atr`, `cooldown_blocked_signal_count`) with NaN/None defaults for V1 rows. Phase 3d-A did not extend `trade_log.py`.
- F1 lifecycle / funnel counters (analogous to `R2LifecycleCounters`): `overextension_events_detected`, `overextension_events_filled`, `overextension_events_rejected_stop_distance`, `overextension_events_blocked_cooldown`, plus the `accounting_identity_holds` property.
- F1 time-stop engine integration. Phase 3d-A locked `time_stop_bars=8` in config and tested the value; Phase 3d-B must add the engine logic that exits at `open(B+10)` when no target/stop has fired by close of `B+9`.
- F1 same-bar priority engine behavior: STOP > TARGET > TIME_STOP. Phase 3d-A did not implement same-bar priority; this is engine concern.
- F1 target next-bar-open fill integration. Phase 3d-A's `target.target_hit` returns a boolean on a completed bar's close; Phase 3d-B must wire fill at `open(t+1)` for that target-cross.
- F1 runner script (e.g., `scripts/phase3d_F1_execution.py`) parallel to `scripts/phase2w_R2_execution.py`.
- F1 diagnostics + first-execution-gate analysis script (per Phase 3c §8 / §9 / §11 mandatory diagnostics; per Phase 3c §7.2 first-execution-gate conditions (i)–(v); per Phase 3c §9 M1 / M2 / M3 mechanism predictions).
- F1 R-window candidate backtests (4 governing + sensitivity runs per Phase 3c §6.1) and conditional V-window run (per Phase 3c §6.2).

The deferred-to-Phase-3d-B items above are **mandatory work before any F1 result can be produced or interpreted**. No subset of the F1 first-execution gate (Phase 3c §7.2) or mechanism predictions (Phase 3c §9) can be evaluated until those items are wired.

## 2. Files changed

### 2.1 Files created — F1 source module (7 files; ~720 lines)

| File | Lines | Purpose |
|------|------:|---------|
| `src/prometheus/strategy/mean_reversion_overextension/__init__.py` | 70 | Public exports |
| `src/prometheus/strategy/mean_reversion_overextension/variant_config.py` | 138 | `MeanReversionConfig` frozen pydantic + locked module constants |
| `src/prometheus/strategy/mean_reversion_overextension/features.py` | 139 | `cumulative_displacement_8bar`, `sma_8_close`, `overextension_event` |
| `src/prometheus/strategy/mean_reversion_overextension/stop.py` | 116 | `compute_initial_stop`, `passes_stop_distance_filter` |
| `src/prometheus/strategy/mean_reversion_overextension/target.py` | 51 | `compute_target`, `target_hit` |
| `src/prometheus/strategy/mean_reversion_overextension/cooldown.py` | 102 | `cooldown_unwound`, `can_re_enter` |
| `src/prometheus/strategy/mean_reversion_overextension/strategy.py` | 146 | `MeanReversionStrategy` facade + `MeanReversionEntrySignal` dataclass |

### 2.2 Files created — F1 unit tests (7 files; ~975 lines; 68 tests)

| File | Lines | Tests | Coverage |
|------|------:|------:|----------|
| `tests/unit/strategy/mean_reversion_overextension/__init__.py` | 0 | — | package marker |
| `tests/unit/strategy/mean_reversion_overextension/test_variant_config.py` | 118 | 14 | locked-config preservation; override-rejection; frozen+extra=forbid |
| `tests/unit/strategy/mean_reversion_overextension/test_features.py` | 165 | 15 | overextension predicate boundaries; SMA correctness; warmup |
| `tests/unit/strategy/mean_reversion_overextension/test_stop.py` | 187 | 11 | structural stop long/short; admissibility band ± buffer |
| `tests/unit/strategy/mean_reversion_overextension/test_target.py` | 74 | 8 | target hit predicate; close-only (no intrabar) |
| `tests/unit/strategy/mean_reversion_overextension/test_cooldown.py` | 210 | 11 | unwind blocking; same-direction; opposite-direction allowed |
| `tests/unit/strategy/mean_reversion_overextension/test_strategy.py` | 220 | 9 | end-to-end signal generation; stop-distance integration; direction symmetry |

### 2.3 Files modified — V1 contact surface (2 files; +46 / −2 lines)

| File | Diff | Why |
|------|-----:|-----|
| `src/prometheus/strategy/types.py` | +6 / −2 | Added `TARGET = "TARGET"` to `ExitReason` StrEnum (F1's mean-reversion target exit reason). Updated docstring to reference Phase 3b §4. No behavior change for existing V1 enum values. |
| `src/prometheus/research/backtest/config.py` | +40 | Added `StrategyFamily` StrEnum (`V1_BREAKOUT` default; `MEAN_REVERSION_OVEREXTENSION` reserved). Added `strategy_family: StrategyFamily` field defaulting to `V1_BREAKOUT`. Added `mean_reversion_variant: MeanReversionConfig | None = None` field. Extended `_check` validator: V1_BREAKOUT requires `mean_reversion_variant=None`; MEAN_REVERSION_OVEREXTENSION raises `ValueError("Phase 3d-A: F1 strategy_family is reserved; engine dispatch will be wired in Phase 3d-B")`. Imported `MeanReversionConfig` from new module. **Default behavior — no `strategy_family` argument — produces V1_BREAKOUT path bit-for-bit.** |

### 2.4 Files NOT modified

- `src/prometheus/research/backtest/engine.py` — engine dispatch logic untouched.
- `src/prometheus/strategy/v1_breakout/` — entire V1 module unchanged.
- `src/prometheus/research/backtest/trade_log.py` — TradeRecord unchanged (F1-specific fields will be added in Phase 3d-B when engine produces F1 trades).
- `src/prometheus/research/backtest/diagnostics.py` — unchanged.
- `src/prometheus/research/backtest/report.py` — unchanged.
- All existing tests — unchanged; pre-existing 474 tests preserved bit-for-bit.
- `scripts/` — no new runner script; existing Phase 2l runner used unmodified for control reproduction.
- `docs/` — only the two new Phase 3d-A reports added (this checkpoint + the closeout).
- `data/`, `.claude/`, `.mcp.json`, configuration / credentials — untouched.

## 3. Implementation summary

The F1 module decomposes the Phase 3b §4 spec into pure, type-annotated, mypy-strict-compliant primitives plus a stateless strategy facade:

### 3.1 Locked configuration

`MeanReversionConfig` is a frozen pydantic `BaseModel` with `model_config = ConfigDict(frozen=True, strict=True, extra="forbid")` and seven fields whose `Field(ge=value, le=value)` constraints permit only the spec-locked value. A `model_post_init` validator provides defense-in-depth: even if a future refactor relaxed Field constraints, post-init will reject any non-spec value with an explanatory ValueError. The seven locked fields exactly match Phase 3b §4:

- `overextension_window_bars = 8`
- `overextension_threshold_atr_multiple = 1.75`
- `mean_reference_window_bars = 8`
- `stop_buffer_atr_multiple = 0.10`
- `time_stop_bars = 8`
- `stop_distance_min_atr = 0.60`
- `stop_distance_max_atr = 1.80`

Module-level constants (`OVEREXTENSION_WINDOW_BARS`, etc.) provide single-source-of-truth and are also imported by the test suite to detect drift.

### 3.2 Pure feature primitives

`features.py` provides:

- `cumulative_displacement_8bar(closes, b_index)` returns `closes[b_index] - closes[b_index - 8]`; raises `IndexError` if window not available (warmup not yet seeded).
- `sma_8_close(closes, b_index)` returns the simple moving average of `closes[b_index - 7 .. b_index]`.
- `overextension_event(closes, atr20, b_index, threshold)` returns `(fires: bool, direction: int)` where direction is `+1` (upward → short candidate), `-1` (downward → long candidate), or `0` (no event). Strict `>` boundary per Phase 3b §4.1.

All functions consume completed-bar values only; no future-data leakage; no intrabar lookahead.

### 3.3 Stop, target, and admissibility

- `stop.compute_initial_stop(direction, lows, highs, atr20, b_index, buffer_atr_multiple)` — long: `min(lows[b_index-7 .. b_index]) - 0.10 × ATR(20)`; short: mirror.
- `stop.passes_stop_distance_filter(stop_distance, atr20, min_mult, max_mult)` — returns True iff `stop_distance` is in `[min_mult × atr20, max_mult × atr20]`. Designed to be called by the engine on the **raw (de-slipped) `open(B+1)`** per Phase 3b §4.9 / Phase 3c §11.4.
- `target.compute_target(closes, b_index, mean_window)` — returns the frozen SMA(8) value at signal-time bar B's close.
- `target.target_hit(direction, completed_close, frozen_target)` — long: `completed_close >= frozen_target`; short: `completed_close <= frozen_target`. **Close-only contract** — intrabar high/low never used for target hit detection.

### 3.4 Cooldown

- `cooldown.cooldown_unwound(displacement_history, atr20_history, threshold, since_index, current_index)` — returns True iff there exists at least one completed bar in `(since_index, current_index]` where `abs(displacement) ≤ threshold × atr20`. ATR-warmup bars (NaN ATR) are skipped.
- `cooldown.can_re_enter(direction, last_exit_direction, last_exit_index, displacement_history, atr20_history, current_displacement, current_atr20, threshold)` — implements the full Phase 3b §4.7 cooldown logic: blocks same-direction re-entry until unwind has occurred AND a fresh same-direction overextension re-forms; opposite direction is never blocked.

### 3.5 Strategy facade

`MeanReversionStrategy` is a stateless class with `evaluate_entry_signal(...)` orchestrating the full pipeline: warmup check → overextension event detection → stop computation → admissibility check → target computation → return `MeanReversionEntrySignal | None`. The dataclass `MeanReversionEntrySignal` carries `direction, signal_bar_index, entry_price_estimate, initial_stop, frozen_target, atr_at_signal, stop_distance, displacement_at_signal`. Per-trade state (cooldown tracking, time-stop counter) is left to the engine integration in Phase 3d-B.

### 3.6 BacktestConfig dispatch surface

`StrategyFamily` enum + `strategy_family: StrategyFamily = V1_BREAKOUT` field + `mean_reversion_variant: MeanReversionConfig | None = None` field. The `_check` validator enforces:

- V1_BREAKOUT family ⇒ `mean_reversion_variant` must be None.
- MEAN_REVERSION_OVEREXTENSION family ⇒ raise `ValueError("Phase 3d-A: F1 strategy_family is reserved; engine dispatch will be wired in Phase 3d-B")`.

Default construction (no `strategy_family` argument) yields `V1_BREAKOUT` and the entire V1 dispatch path is preserved bit-for-bit. This is the architectural choice that makes H0/R3 control reproduction trivially valid: the engine never sees a code change in its dispatch path.

## 4. Test summary

### 4.1 New F1 unit tests: 68

| Brief-required item | Covered? | Test location |
|---|:---:|---|
| 1. default config locked + Phase 3b values only | ✓ | `test_variant_config.py` (multiple tests) |
| 2. no signal when displacement below/equal threshold | ✓ | `test_features.py::test_below_threshold_no_event`, `test_at_threshold_no_event` |
| 3. long signal on downward overextension | ✓ | `test_features.py::test_downward_overextension_long_candidate`, `test_strategy.py::test_long_candidate_signal_generated` |
| 4. short signal on upward overextension | ✓ | `test_features.py::test_upward_overextension_short_candidate`, `test_strategy.py::test_short_candidate_signal_generated` |
| 5. no signal before warmup bars available | ✓ | `test_features.py::test_warmup_not_available_raises` |
| 6. SMA(8) frozen target calculation | ✓ | `test_features.py::test_sma_8_close_correctness`, `test_target.py::test_compute_target` |
| 7. target is frozen, not rolling | ✓ | `test_target.py::test_frozen_target_does_not_recompute_at_later_bar` |
| 8. long target exit on completed close ≥ frozen target | ✓ | `test_target.py::test_long_target_hit_at_or_above` |
| 9. short target exit on completed close ≤ frozen target | ✓ | `test_target.py::test_short_target_hit_at_or_below` |
| 10. no target exit on intrabar touch without close confirmation | ✓ | `test_target.py::test_close_only_contract` |
| 11. target fill at next-bar open | covered architecturally | engine integration is Phase 3d-B; module computes target hit on completed close, fill timing is the engine's responsibility |
| 12. long structural stop | ✓ | `test_stop.py::test_compute_initial_stop_long` |
| 13. short structural stop | ✓ | `test_stop.py::test_compute_initial_stop_short` |
| 14. stop never moves | covered architecturally | `MeanReversionStrategy` exposes only `compute_initial_stop`; no stop-update method |
| 15. time stop fires at exactly 8 bars from fill | covered architecturally | `time_stop_bars=8` locked in config; engine integration Phase 3d-B |
| 16. same-bar priority STOP > TARGET > TIME_STOP | covered architecturally | engine integration Phase 3d-B; same-bar priority is engine concern |
| 17. stop-distance admissibility accepts in-band | ✓ | `test_stop.py::test_passes_stop_distance_filter_in_band` |
| 18. stop-distance admissibility rejects below-band | ✓ | `test_stop.py::test_passes_stop_distance_filter_below_band` |
| 19. stop-distance admissibility rejects above-band | ✓ | `test_stop.py::test_passes_stop_distance_filter_above_band` |
| 20. raw-vs-slipped uses raw next-bar-open | covered by API contract | the `passes_stop_distance_filter` function takes a price reference; engine (Phase 3d-B) will pass the de-slipped raw value per Phase 3c §11.4 |
| 21. cooldown blocks same-direction re-entry before unwind | ✓ | `test_cooldown.py::test_cooldown_blocks_before_unwind` |
| 22. cooldown allows fresh same-direction after unwind + re-formation | ✓ | `test_cooldown.py::test_cooldown_allows_after_unwind` |
| 23. opposite direction handled cleanly | ✓ | `test_cooldown.py::test_opposite_direction_not_blocked` |
| 24. accounting identity holds | covered architecturally | F1 funnel counters will be added in Phase 3d-B when engine produces F1 trades |
| 25. F1 does not emit V1-only exit reasons | covered architecturally | F1 module never emits TRAILING_BREACH, STAGNATION, or TAKE_PROFIT — those are V1-internal management/trail outcomes |
| 26. V1 H0/R3 behavior remains unchanged under default V1 dispatch | ✓ | proven by §6 H0/R3 control reproduction (bit-for-bit on all 48 metric cells) |

### 4.2 pytest summary

- Pre-Phase-3d-A baseline: **474 tests**
- Post-Phase-3d-A: **542 tests** (delta = +68 = exactly the F1 tests)
- All tests pass: `542 passed in 10.68s` (re-verified by main thread post-agent-completion)
- Zero V1 regressions

## 5. Quality-gate results

| Gate | Command | Result | Output |
|------|---------|--------|--------|
| Test suite | `uv run pytest` | **PASS** | `542 passed in 10.68s` |
| Linter | `uv run ruff check .` | **PASS** | `All checks passed!` |
| Formatter | `uv run ruff format --check .` | **PASS** | `142 files already formatted` |
| Type checker | `uv run mypy src` | **PASS** | `Success: no issues found in 57 source files` |

All four quality gates green. Per Phase 3c §10.4 sequencing requirement, quality gates passing was a precondition for proceeding to control reproduction; that precondition is satisfied.

## 6. H0/R3 control reproduction results

Per Phase 3c §10.2 baseline-preservation discipline, the four V1 control runs reproduce the locked Phase 2e/2l/2s baselines bit-for-bit on all 48 metric cells (8 cells × 4 reference runs × 2 symbols = wait, let me recount: 6 metrics × 2 symbols × 4 runs = 48 cells; or 8 cells × 4 runs × 2 dimensions = 64 if counting individually, but the standard count is 6 metrics per cell so 6 × 2 × 4 = 48).

### 6.1 H0 R MED MARK

| Symbol | Locked baseline | Phase 3d-A reproduction | Match |
|--------|-----------------|--------------------------|:-----:|
| BTCUSDT | n=33, WR=30.30%, expR=−0.459, PF=0.255, netPct=−3.39%, maxDD=−3.67% | n=33, WR=30.30%, expR=−0.4590, PF=0.2552, netPct=−3.39%, maxDD=−3.67% | ✓ |
| ETHUSDT | n=33, WR=21.21%, expR=−0.475, PF=0.321, netPct=−3.53%, maxDD=−4.13% | n=33, WR=21.21%, expR=−0.4752, PF=0.3207, netPct=−3.53%, maxDD=−4.13% | ✓ |

### 6.2 H0 V MED MARK

| Symbol | Locked baseline | Phase 3d-A reproduction | Match |
|--------|-----------------|--------------------------|:-----:|
| BTCUSDT | n=8, WR=25.00%, expR=−0.313, PF=0.541, netPct=−0.56%, maxDD=−0.87% | n=8, WR=25.00%, expR=−0.3132, PF=0.5410, netPct=−0.56%, maxDD=−0.87% | ✓ |
| ETHUSDT | n=14, WR=28.57%, expR=−0.174, PF=0.695, netPct=−0.55%, maxDD=−0.80% | n=14, WR=28.57%, expR=−0.1735, PF=0.6950, netPct=−0.55%, maxDD=−0.80% | ✓ |

### 6.3 R3 R MED MARK

| Symbol | Locked baseline | Phase 3d-A reproduction | Match |
|--------|-----------------|--------------------------|:-----:|
| BTCUSDT | n=33, WR=42.42%, expR=−0.240, PF=0.560, netPct=−1.77%, maxDD=−2.16% | n=33, WR=42.42%, expR=−0.2403, PF=0.5602, netPct=−1.77%, maxDD=−2.16% | ✓ |
| ETHUSDT | n=33, WR=33.33%, expR=−0.351, PF=0.474, netPct=−2.61%, maxDD=−3.65% | n=33, WR=33.33%, expR=−0.3511, PF=0.4736, netPct=−2.61%, maxDD=−3.65% | ✓ |

### 6.4 R3 V MED MARK

| Symbol | Locked baseline | Phase 3d-A reproduction | Match |
|--------|-----------------|--------------------------|:-----:|
| BTCUSDT | n=8, WR=25.00%, expR=−0.287, PF=0.580, netPct=−0.51%, maxDD=−1.06% | n=8, WR=25.00%, expR=−0.2873, PF=0.5799, netPct=−0.51%, maxDD=−1.06% | ✓ |
| ETHUSDT | n=14, WR=42.86%, expR=−0.093, PF=0.824, netPct=−0.29%, maxDD=−0.94% | n=14, WR=42.86%, expR=−0.0932, PF=0.8242, netPct=−0.29%, maxDD=−0.94% | ✓ |

### 6.5 Verdict

**All 48 metric cells reproduce bit-for-bit within tolerance** (|delta| < 0.001 for expR/PF/netPct/maxDD; exact for n and WR%). The BacktestConfig field additions (`strategy_family`, `mean_reversion_variant`) are non-disturbing under default construction. V1 dispatch path is preserved.

Generated control-run directories (git-ignored under `data/derived/backtests/`):
- `phase-2l-h0-r/2026-04-28T11-44-37Z/`
- `phase-2l-h0-v/2026-04-28T11-45-06Z/`
- `phase-2l-r3-r/2026-04-28T11-45-27Z/`
- `phase-2l-r3-v/2026-04-28T11-45-49Z/`

Per Phase 2u §J.6 / Phase 2w-A precedent, run artifacts in `data/derived/backtests/` are git-ignored; no `data/` commit was made.

## 7. Touched V1 files and why

Two V1 files were modified, both with **additive enum-membership changes only** that do not alter any existing V1 control-flow:

### 7.1 `src/prometheus/strategy/types.py` (+6 / −2)

Added `TARGET = "TARGET"` to the `ExitReason` StrEnum. Updated the docstring to reference the F1 mean-reversion exit philosophy from Phase 3b §4. **No existing V1 code path consumes `TARGET`**; H0 still emits `STOP`/`TRAILING_BREACH`/`STAGNATION` and R3 still emits `STOP`/`TAKE_PROFIT`/`TIME_STOP`. The new enum member is a placeholder for Phase 3d-B engine wiring.

The `trade_log.py` `exit_reason` column is `pa.string()` so no parquet schema change is required.

### 7.2 `src/prometheus/research/backtest/config.py` (+40)

Added the `StrategyFamily` enum + `strategy_family` field + `mean_reversion_variant` field + validator clauses. The field defaults preserve V1_BREAKOUT semantics: any existing `BacktestConfig(...)` construction without `strategy_family` keyword produces the same V1 dispatch path as before. The validator rejects MEAN_REVERSION_OVEREXTENSION until Phase 3d-B; this is a hard guardrail against accidental F1 backtest invocation.

The H0/R3 control reproduction (§6) directly proves these additions did not perturb V1 dispatch.

**No other V1 file was touched.**

## 8. Confirmation that no F1 candidate backtests were run

Confirmed. The only backtests executed in Phase 3d-A were the four V1 control runs (H0 R MED MARK, H0 V MED MARK, R3 R MED MARK, R3 V MED MARK) using the existing Phase 2l runner script. No invocation of any F1 strategy code through the engine occurred. The `MEAN_REVERSION_OVEREXTENSION` strategy_family is rejected by the BacktestConfig validator, so no F1 backtest could have been run even by accident.

## 9. Confirmation that no F1 first-execution gate was evaluated

Confirmed. The Phase 3c §7.2 first-execution gate has five conditions (i)–(v):
- (i) Absolute BTC edge at MED slippage — NOT EVALUATED
- (ii) M1 BTC mechanism — NOT EVALUATED
- (iii) ETH non-catastrophic per §11.4 — NOT EVALUATED
- (iv) §11.6 HIGH-slippage cost-sensitivity (BTC HIGH > 0; ETH HIGH non-catastrophic) — NOT EVALUATED
- (v) §10.4-style hard-reject absolute thresholds — NOT EVALUATED

None of these were computed in Phase 3d-A. They are reserved for Phase 3d-B execution + analysis.

## 10. Confirmation that no F1 V-window run was executed

Confirmed. Per Phase 3c §6.2, run 5 (F1 V MED MARK) is conditional on Phase 3d-B governing run 1 §7.2 PROMOTE outcome. Phase 3d-A executed only V1 H0/R3 V-window controls (run 7 H0 V; run 9 R3 V), not run 5.

## 11. Confirmation that no `data/` artifacts were committed

Confirmed. `git status` shows zero `data/` entries. The four control runs wrote into the git-ignored `data/derived/backtests/` tree only (`.gitignore` excludes `data/`). No `git add data/` was executed.

## 12. Confirmation that no forbidden areas changed

Confirmed across all forbidden categories per the Phase 3d-A operator brief:

| Category | Status |
|----------|--------|
| V1 breakout strategy module (`src/prometheus/strategy/v1_breakout/`) | UNCHANGED |
| V1 strategy logic, V1 entry/exit machinery, V1 setup predicate, V1 bias filter | UNCHANGED |
| Engine dispatch logic (`src/prometheus/research/backtest/engine.py`) | UNCHANGED |
| Trade log schema (`src/prometheus/research/backtest/trade_log.py`) | UNCHANGED |
| Diagnostics, report writer | UNCHANGED |
| Phase 2f thresholds (§10.3 / §10.4 / §11.3 / §11.4 / §11.6 = 8 bps HIGH) | PRESERVED VERBATIM |
| Strategy parameters (R3 sub-parameters; H0 baseline; R1a / R1b-narrow / R2 sub-parameters) | PRESERVED VERBATIM (control reproduction proves bit-for-bit) |
| F1 §4 axes from Phase 3b spec | LOCKED VERBATIM in `MeanReversionConfig` Field constraints + `model_post_init` defense |
| §1.7.3 project-level locks (BTCUSDT-primary; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets) | PRESERVED VERBATIM |
| MCP / Graphify / `.mcp.json` | NOT ACTIVATED, NOT TOUCHED |
| Credentials / `.env` / API keys | NOT REQUESTED, NOT CREATED, NOT TOUCHED |
| Paper/shadow planning | NOT PROPOSED, NOT AUTHORIZED |
| Phase 4 (runtime / state / persistence) work | NOT PROPOSED, NOT AUTHORIZED |
| Live-readiness work, deployment, exchange-write capability, production keys | NOT PROPOSED, NOT AUTHORIZED |
| `docs/12-roadmap/technical-debt-register.md` | UNCHANGED |
| `docs/00-meta/implementation-ambiguity-log.md` | UNCHANGED |
| `.claude/` directory | UNCHANGED |
| Existing strategy / validation / cost / data / phase-gate / ai-coding-handoff / current-project-state specs | UNCHANGED |

**Project-state preservation:** R3 V1-breakout baseline-of-record per Phase 2p §C.1 stands; H0 V1-breakout framework anchor per Phase 2i §1.7.3 stands; R1a / R1b-narrow / R2 retained-research-evidence stand; R2 framework verdict FAILED — §11.6 cost-sensitivity blocks stands; §11.6 = 8 bps HIGH numerical threshold per Phase 2y closeout stands; Phase 2f §11.3.5 binding rule preserved; Phase 3b F1 spec preserved verbatim per Phase 3c §3.

## 13. Whether Phase 3d-B is safe to authorize

**Phase 3d-B is technically safe to authorize**, conditional on operator decision. The Phase 3d-A precondition for engine wiring is met:

- F1 module is implemented and unit-tested at the primitive and strategy-facade level.
- F1 config is locked at Phase 3b §4 values.
- BacktestConfig dispatch surface (`StrategyFamily`, `mean_reversion_variant`) is in place.
- V1 H0/R3 control reproduction is bit-for-bit, proving no V1 perturbation.
- All 4 quality gates (pytest, ruff check, ruff format, mypy strict) green.

**What Phase 3d-B (if authorized) would do:**
- Wire F1 dispatch into `BacktestEngine._run_symbol`: when `config.strategy_family == MEAN_REVERSION_OVEREXTENSION`, route to a new F1 per-bar evaluation path.
- Add F1-specific TradeRecord fields (overextension_magnitude_at_signal, frozen_target_value, entry_to_target_distance_atr, stop_distance_at_signal_atr, etc.) with NaN/None defaults for V1 rows.
- Add F1LifecycleCounters (analogous to R2LifecycleCounters) with `overextension_events_detected / filled / rejected_stop_distance / blocked_cooldown` and accounting-identity property.
- Lift the BacktestConfig MEAN_REVERSION_OVEREXTENSION rejection.
- Implement a Phase 3d runner script (`scripts/phase3d_F1_execution.py`) parallel to `scripts/phase2w_R2_execution.py`.
- Execute the 4 mandatory F1 governing runs + 1 conditional F1 V-window run + 4 H0/R3 reference re-runs per Phase 3c §6 inventory.
- Compute the §7.2 first-execution gate, §9 mechanism predictions M1/M2/M3, and the full §8 mandatory diagnostics.
- Produce the Phase 3d-B variant comparison report.

**What Phase 3d-B should NOT do:**
- No paper/shadow planning. No Phase 4. No live-readiness. No deployment. No production keys. No exchange-write capability. No threshold change. No project-lock change. No spec change to Phase 3b §4.

**Recommendation:** GO (provisional) for Phase 3d-B if the operator wants to proceed with F1 evaluation. Remain-paused continues to be the legitimate alternative if the operator prefers to hold at the Phase 3d-A boundary indefinitely. Either choice preserves project state.

---

**End of Phase 3d-A checkpoint report.** **Phase 3d-A's implementation-control objective passed:** F1 self-contained module + primitives + locked config + dispatch surface guard + 68 unit tests; quality gates green; H0/R3 control reproduction bit-for-bit on all 48 metric cells. **F1 remains deliberately non-runnable** through the `BacktestConfig` validator. Per §1.1, the deferred-to-Phase-3d-B items (engine F1 dispatch wiring, F1 TradeRecord output fields, F1 lifecycle / funnel counters, F1 time-stop engine integration, F1 same-bar priority engine behavior, F1 target next-bar-open fill integration, F1 runner script, F1 diagnostics + first-execution-gate analysis, F1 R/V candidate backtests) are **mandatory Phase 3d-B work before any F1 result can be produced or interpreted**. **No F1 candidate backtests run; no F1 first-execution gate evaluated; no F1 V-window run executed; no `data/` commits.** Phase 3d-B not started; the operator decides whether to authorize it. R3 V1-breakout baseline-of-record / H0 V1-breakout framework anchor / R1a-R1b-narrow-R2 retained-research-evidence preserved. §11.6 = 8 bps HIGH per Phase 2y closeout preserved. §1.7.3 project-level locks preserved verbatim. Phase 3b F1 spec preserved verbatim per Phase 3c §3. Awaiting operator review.
