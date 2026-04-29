# Phase 3i-B1 — D1-A Engine-Wiring Controls Checkpoint Report

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (no post-hoc loosening per §11.3.5); Phase 2i §1.7.3 project-level locks; Phase 2p §C.1 (R3 baseline-of-record); Phase 2y closeout (§11.6 = 8 bps HIGH preserved); Phase 3d-B1 precedent (F1 engine-wiring); **Phase 3g D1-A spec memo + methodology audit (binding spec)**; **Phase 3h D1-A execution-planning memo (binding execution plan, with timing-clarification amendments)**; **Phase 3i-A implementation-controls (binding implementation surface)**; `src/prometheus/research/backtest/engine.py`; `src/prometheus/research/backtest/config.py`; `src/prometheus/research/backtest/trade_log.py`; `src/prometheus/strategy/funding_aware_directional/`; `.claude/rules/prometheus-core.md`.

**Phase:** 3i-B1 — D1-A engine-wiring control phase. Lifts the Phase 3i-A guard, wires D1-A into the backtest engine (per-bar lifecycle, lifecycle counters, output fields, runner scaffold), proves H0 / R3 / F1 controls reproduce bit-for-bit, and adds an extensive synthetic D1-A engine test suite — all without running any D1-A candidate backtest or evaluating the first-execution gate.

**Branch:** `phase-3i-b1/d1a-engine-wiring-controls`. **Date:** 2026-04-29 UTC.

**Status:** Engine-wiring control complete. **D1-A is now technically runnable through the engine, but no D1-A candidate backtest has been run.** **No D1-A diagnostics or first-execution gate evaluated.** **No derived `funding_aware_features__v001` dataset generated.** All four quality gates green; full 9-cell H0/R3/F1 controls (R+V × MED MARK; F1 R MED MARK) reproduce bit-for-bit on every summary metric.

---

## 1. Plain-English explanation of what Phase 3i-B1 did

Phase 3i-B1 is the second implementation phase for D1-A, analogous to Phase 3d-B1 which performed the same role for F1. It:

- **Lifted the Phase 3i-A guard** at the top of `BacktestEngine.run` (the documented `RuntimeError("D1-A engine wiring not yet authorized; see Phase 3i-B1.")`).
- **Wired the D1-A engine dispatch path** (`_run_symbol_d1a` + open / close / helper methods) covering full per-bar lifecycle: funding-event eligibility, Z-score over trailing 270 events with current-event exclusion, extreme-event detection, contrarian direction, per-funding-event cooldown, stop-distance admissibility, fill at next bar open, STOP > TARGET > TIME_STOP same-bar precedence with completed-bar-close TARGET trigger and next-bar-open fill, TIME_STOP at close of B+1+32 with fill at B+1+33 open, END_OF_DATA at window close.
- **Added `FundingAwareLifecycleCounters`** with the event-level identity `detected = filled + rejected_stop_distance + blocked_cooldown` and the runtime bookkeeping that prevents repeated 15m bars from inflating the detected count.
- **Extended `TradeRecord`** with 4 new D1-A fields (`funding_event_id_at_signal`, `funding_z_score_at_signal`, `funding_rate_at_signal`, `bars_since_funding_event_at_signal`) and reused 2 existing F1-precedent fields for the geometry diagnostic (`entry_to_target_distance_atr` ≈ 2.0, `stop_distance_at_signal_atr` ≈ 1.0 by construction). Added the corresponding parquet schema fields.
- **Added a runner scaffold** `scripts/phase3j_D1A_execution.py` that fails closed without `--phase-3j-authorized` (analogous to Phase 3d-B1 `--phase-3d-b2-authorized` precedent).
- **Added 23 D1-A engine dispatch tests** + updated 5 D1-A guard tests to reflect the lifted guard. Total D1-A tests at end of Phase 3i-B1: ~101 (15 config + 42 primitives + 10 facade + 8 BacktestConfig + 5 guard/post-lift + 21 engine dispatch).
- **Ran the full 4 quality gates** all green (668 pytest passing, ruff/format/mypy clean).
- **Reproduced the full 9-cell control set bit-for-bit** (H0 R/V × BTC/ETH; R3 R/V × BTC/ETH; F1 R × BTC/ETH).

What Phase 3i-B1 explicitly did NOT do:

- Did NOT run any D1-A candidate backtest on real R-window or V-window data.
- Did NOT evaluate D1-A first-execution gate.
- Did NOT compute D1-A M1 / M2 / M3 mechanism checks on real data.
- Did NOT generate `funding_aware_features__v001` derived dataset.
- Did NOT commit any `data/` artifact.
- Did NOT alter V1 / R3 / R1a / R1b-narrow / R2 behavior (controls bit-for-bit).
- Did NOT alter F1 behavior (control bit-for-bit).
- Did NOT change any threshold, project-lock, or D1-A locked spec value (Phase 3g binding consumed unmodified).

---

## 2. Files changed

Modified:

- `src/prometheus/research/backtest/engine.py` — biggest change. Added `_D1ATradeMetadata` dataclass; added `FundingAwareLifecycleCounters` Pydantic-style dataclass; extended `_OpenTrade` with `d1a_metadata` field; extended `_SymbolRun` with D1-A state (counters + last-processed event + last-consumed direction/event); extended `BacktestRunResult` with `funding_aware_counters_per_symbol`; added `_funding_aware_strategy` to `BacktestEngine.__init__`; lifted the Phase 3i-A guard at top of `run()`; added D1-A dispatch in the per-symbol loop; added `_run_symbol_d1a` (full per-bar lifecycle); added `_open_d1a_trade` / `_close_d1a_trade_on_stop` / `_close_d1a_trade_managed` / `_close_d1a_trade_end_of_data`; added `_latest_eligible_funding_event_idx` / `_bars_since_funding_event` helpers; extended `_record_trade` to populate D1-A metadata fields. **V1 and F1 dispatch paths are bit-for-bit unchanged**, verified by control reproduction.
- `src/prometheus/research/backtest/trade_log.py` — added 4 D1-A `TradeRecord` fields with None / NaN / -1 defaults; extended parquet schema to match.
- `tests/unit/research/backtest/test_engine_d1a_guard.py` — replaced the Phase 3i-A guard-raising test with Phase 3i-B1 dispatch tests (5 tests verifying guard lifted, V1/F1 unchanged, counters identity).
- `tests/unit/research/backtest/test_trade_log.py` — extended the parquet schema assertion to include the 4 new D1-A column names.

New files:

- `scripts/phase3j_D1A_execution.py` — Phase 3j D1-A execution runner scaffold (guarded by `--phase-3j-authorized`; fails closed without it; safe `check-imports` subcommand).
- `tests/unit/research/backtest/test_engine_d1a_dispatch.py` — comprehensive D1-A engine dispatch tests (21 tests covering long/short signal generation, warmup / no-eligible-event / sub-threshold / zero-variance, fill timing, stop / target / TIME_STOP geometry, completed-bar-close TARGET trigger with no intrabar fill, same-bar STOP > TARGET priority, END_OF_DATA, lifecycle identity, repeated-bar non-inflation, funding accrual signed correctly, V1 default unchanged, runner scaffold guard).
- `docs/00-meta/implementation-reports/2026-04-29_phase-3i-B1_D1A_engine-wiring-controls.md` — this checkpoint report.
- `docs/00-meta/implementation-reports/2026-04-29_phase-3i-B1_closeout-report.md` — closeout.

Not touched:

- `src/prometheus/strategy/v1_breakout/**` (V1 module untouched).
- `src/prometheus/strategy/mean_reversion_overextension/**` (F1 module untouched).
- `src/prometheus/strategy/funding_aware_directional/**` (D1-A primitives + config + facade unchanged from Phase 3i-A).
- `src/prometheus/research/backtest/config.py` (BacktestConfig unchanged from Phase 3i-A; the Phase 3i-A validator extension still handles V1/F1/D1-A dispatch).
- `src/prometheus/research/backtest/accounting.py`, `fills.py`, `funding_join.py`, `simulation_clock.py`, `sizing.py`, `stops.py` (engine adjuncts unchanged).
- `src/prometheus/research/backtest/report.py` (summary metrics unchanged; D1-A target_exits column will be added by the Phase 3j runner if/when authorized).
- `.claude/`, `.mcp.json`, `config/`, `secrets/`, any `data/` file.

## 3. Implementation summary

### 3.1 Phase 3i-A guard lifted

The Phase 3i-A `RuntimeError` at the top of `BacktestEngine.run` is removed. In its place, an `is_d1a` flag controls dispatch in the per-symbol loop:

```python
is_d1a = self._config.strategy_family == StrategyFamily.FUNDING_AWARE_DIRECTIONAL
# ...
if is_d1a:
    self._run_symbol_d1a(run, accounting=..., klines_15m=..., mark_15m=..., funding=..., symbol_info=...)
elif is_f1:
    self._run_symbol_f1(...)
else:
    self._run_symbol(...)
```

The 1h-data prerequisite is bypassed for D1-A (D1-A has no 1h bias filter per Phase 3g §6.13), mirroring the F1 precedent.

### 3.2 D1-A strategy facade construction

`BacktestEngine.__init__` constructs `self._funding_aware_strategy: FundingAwareStrategy | None`:

```python
self._funding_aware_strategy: FundingAwareStrategy | None = None
if (
    config.strategy_family == StrategyFamily.FUNDING_AWARE_DIRECTIONAL
    and config.funding_aware_variant is not None
):
    self._funding_aware_strategy = FundingAwareStrategy(config.funding_aware_variant)
```

V1 and F1 paths leave `self._funding_aware_strategy` as None.

### 3.3 BacktestRunResult extension

`BacktestRunResult` gains `funding_aware_counters_per_symbol: dict[Symbol, FundingAwareLifecycleCounters]`. V1 / F1 runs leave this as an empty dict (or zero-valued counters where applicable).

## 4. D1-A engine dispatch summary

The `_run_symbol_d1a` per-bar lifecycle implements the binding Phase 3g spec (with Phase 3h timing-clarification amendments) verbatim:

- **Per-bar entry detection** is tier-ordered (Phase 3i-B1 ordering matters for the lifecycle identity to hold):
  1. Find latest eligible funding event with `funding_time <= bar_close_time` (binary-search helper `_latest_eligible_funding_event_idx`).
  2. Skip if event_id matches `run.d1a_last_processed_event_id` (prevents bar-level inflation per Phase 3g §9.4).
  3. Pre-detection warmup checks (window in-bounds, ATR > 0, next bar exists). If any fail, **do NOT mark the event as processed** — a later bar (with valid ATR / next bar) will re-evaluate. This avoids consuming an event that arrived during ATR warmup.
  4. Compute Z-score over trailing 270 prior events (current event excluded from rolling mean/std).
  5. If `|Z_F| < 2.0`: mark processed, do NOT increment detected (only extreme events count).
  6. Get contrarian direction (Z ≥ +2 → SHORT; Z ≤ -2 → LONG).
  7. Increment `funding_extreme_events_detected`. Mark processed.
  8. Cooldown gate: blocked → increment `funding_extreme_events_blocked_cooldown`.
  9. Stop-distance admissibility: failed → increment `funding_extreme_events_rejected_stop_distance`.
  10. Open trade: `_open_d1a_trade` succeeds → increment `funding_extreme_events_filled`.

- **Per-bar trade management** (when position open) follows STOP > TARGET > TIME_STOP same-bar precedence:
  - **STOP** uses existing MARK_PRICE stop-trigger machinery via `evaluate_stop_hit` (unchanged from V1/F1).
  - **TARGET** triggers only on completed-bar close confirmation: LONG `close ≥ target_price`; SHORT `close ≤ target_price`. **No intrabar target-touch fill; no same-close TARGET fill.** Fill at next bar open via `exit_fill_price`.
  - **TIME_STOP** triggers at close of bar `fill_bar_index + time_stop_bars` (= 32). Fill at next bar open (B+1+33).
  - **END_OF_DATA** closes any still-open trade at the last bar's close.

## 5. D1-A lifecycle summary

Per-symbol state on `_SymbolRun`:

- `d1a_counters: FundingAwareLifecycleCounters` — event-level funnel.
- `d1a_last_processed_event_id: str | None` — prevents bar-level inflation.
- `d1a_last_consumed_event_id: str | None` — per-direction cooldown bookkeeping.
- `d1a_last_consumed_direction: Direction | None`.

After every position close (STOP / TARGET / TIME_STOP / END_OF_DATA), the engine sets `d1a_last_consumed_event_id` to the funding event id that produced the entry signal and `d1a_last_consumed_direction` to the closed position's direction. The next D1-A entry candidate consults `can_re_enter_d1a` with these to enforce per-funding-event cooldown.

## 6. D1-A exit timing and priority summary

Per Phase 3h §6.8 / §6.9 timing-clarification amendments and Phase 3g §6.7 / §6.8:

- **Same-bar priority STOP > TARGET > TIME_STOP**, evaluated on the completed bar.
- **STOP**: existing MARK_PRICE stop-trigger machinery (unchanged from F1's stop handling). Trigger is intrabar via mark-price low/high comparison; fill at the same bar's stop price (or gap-through fill price).
- **TARGET**: completed-bar close confirmation only. LONG fires when `close >= target_price`; SHORT when `close <= target_price`. Fill at next bar open via `exit_fill_price` (applies adverse exit slippage). **No intrabar target-touch fill, no same-close TARGET fill.** Verified by `test_d1a_intrabar_target_touch_does_not_fire`.
- **TIME_STOP**: triggers at the close of bar `fill_bar_index + time_stop_bars` (the 32nd completed 15m bar from entry fill). Fill at next bar open (B+1+33). Verified by `test_d1a_time_stop_fires_at_horizon`.
- **END_OF_DATA**: any still-open trade at the end of the bar series closes at the last bar's close.

## 7. D1-A funding timestamp / no-lookahead summary

Per Phase 3h §4.5 timing-clarification amendments:

- **Funding event eligibility**: `funding_time <= bar_close_time` (non-strict ≤). Equality is eligible. Strictly-greater is forbidden.
- **Implementation**: `_latest_eligible_funding_event_idx` uses Python's `bisect.bisect_right(funding_times, bar_close_time) - 1`, which respects the non-strict ≤ semantics.
- **Trade enters at next bar open**: the equality case (event at exactly bar B's close time) does not enable a same-close fill — the entry still fills at bar B+1's open per the Phase 3g §6.4 timing.
- **Rolling 90-day Z-score excludes the current event**: `compute_d1a_z_score(prior_funding_rates[:latest_evt_idx], ...)` slices the array up to but not including the current event's index, ensuring the current event is excluded from its own normalization.
- **v002 funding-timestamp semantics**: the engine assumes v002 `funding_time` represents completed settlement timestamps (Binance USDⓈ-M canonical). If a future Phase 3i-B1 / Phase 3j discovery indicates otherwise, implementation must STOP and escalate per Phase 3h §4.5. No such discovery occurred during Phase 3i-B1; the existing v002 funding dataset's `funding_time` field is treated as completed-settlement-time per the data-requirements doc.

## 8. D1-A lifecycle counter summary

`FundingAwareLifecycleCounters` is a `@dataclass` with four `int` fields and an `accounting_identity_holds` property:

```python
funding_extreme_events_detected: int
funding_extreme_events_filled: int
funding_extreme_events_rejected_stop_distance: int
funding_extreme_events_blocked_cooldown: int
```

Identity (event-level, not bar-level):

```text
detected = filled + rejected_stop_distance + blocked_cooldown
```

Verified by `test_d1a_lifecycle_identity_holds` and `test_funding_aware_lifecycle_counters_identity_holds_when_zero`.

The `funding_extreme_events_detected` counter is event-level — repeated 15m bars referencing the same `funding_event_id` increment it at most once. Verified by `test_d1a_repeated_bar_references_do_not_inflate_detected` (a synthetic run with 20 bars after the warmup window, all referencing the same extreme event, produces `detected = 1`).

The future Phase 3j runner will emit `funding_aware_lifecycle_total.json` per run analogous to F1's `f1_lifecycle_total.json`. Phase 3i-B1 does NOT run any D1-A candidate so this artifact is not yet generated.

## 9. TradeRecord / report-field summary

### 9.1 New D1-A fields (Phase 3i-B1)

| Field | Type | Default | Populated for |
|-------|------|---------|---------------|
| `funding_event_id_at_signal` | `str \| None` | `None` | D1-A trades only |
| `funding_z_score_at_signal` | `float` | `NaN` | D1-A trades only |
| `funding_rate_at_signal` | `float` | `NaN` | D1-A trades only |
| `bars_since_funding_event_at_signal` | `int` | `-1` | D1-A trades only |

### 9.2 Reused F1-precedent fields (semantically aligned for D1-A)

| Field | F1 meaning | D1-A meaning |
|-------|------------|--------------|
| `entry_to_target_distance_atr` | `\|entry_fill_price - frozen_target\| / ATR(20)` | `\|entry_fill_price - target_price\| / ATR(20)` ≈ **2.0** by construction |
| `stop_distance_at_signal_atr` | F1 stop_distance / ATR(20) | D1-A stop_distance / ATR(20) ≈ **1.0** by construction |

### 9.3 V1 / F1 row defaults

For V1 / F1 trades, the new D1-A fields default to `None / NaN / -1`, preserving V1 / F1 trade-log column semantics bit-for-bit.

The parquet schema in `trade_log.py::trade_record_to_parquet_table` is extended with the 4 new column names. `tests/unit/research/backtest/test_trade_log.py::test_table_schema_has_expected_columns` verifies the schema includes the new fields.

## 10. Runner scaffold summary

`scripts/phase3j_D1A_execution.py` is a Phase-3d-B1-style scaffolded runner:

- Subcommands: `check-imports` (safe; verifies D1-A engine surface imports cleanly) and `d1a` (gated; the future candidate-run command).
- The `d1a` subcommand requires `--phase-3j-authorized` to proceed. Without the flag, the script exits non-zero with the message `"D1-A candidate execution requires Phase 3j authorization."` to stderr.
- Even **with** `--phase-3j-authorized` in Phase 3i-B1, the run-loop body is intentionally not implemented — the script exits non-zero with `"D1-A run-loop not yet implemented in Phase 3i-B1 scaffold; Phase 3j is required to authorize candidate runs."` This double-gate prevents accidental D1-A candidate execution under Phase 3i-B1.

Verified by tests:
- `test_d1a_runner_scaffold_requires_authorization_flag` — invocation without flag exits non-zero with documented stderr message.
- `test_d1a_runner_scaffold_check_imports_ok` — `check-imports` subcommand exits zero and confirms D1-A engine surface imports cleanly.

## 11. Test summary

| Test file | Phase 3i-B1 delta | Total | Purpose |
|-----------|-------------------:|------:|---------|
| `tests/unit/strategy/funding_aware_directional/test_variant_config.py` | 0 | 15 | Locked-spec preservation (unchanged from Phase 3i-A). |
| `tests/unit/strategy/funding_aware_directional/test_primitives.py` | 0 | 42 | Primitive helpers (unchanged from Phase 3i-A). |
| `tests/unit/strategy/funding_aware_directional/test_strategy.py` | 0 | 10 | Facade tests (unchanged from Phase 3i-A). |
| `tests/unit/research/backtest/test_config.py` | 0 | 19 | BacktestConfig dispatch validation (unchanged from Phase 3i-A; the validator was already wired for D1-A). |
| `tests/unit/research/backtest/test_engine_d1a_guard.py` | replaced | 5 | Phase 3i-A guard tests REPLACED with Phase 3i-B1 dispatch tests (guard lifted; V1/F1 unchanged; counters identity). Prior file had 3 tests; new file has 5. |
| `tests/unit/research/backtest/test_engine_d1a_dispatch.py` | new | 21 | Comprehensive D1-A engine dispatch tests (synthetic in-memory runs covering signal generation, fill timing, stop / target / TIME_STOP geometry, completed-bar-close TARGET trigger, no intrabar fill, same-bar STOP > TARGET priority, END_OF_DATA, lifecycle identity, repeated-bar non-inflation, funding accrual sign, runner scaffold guard). |
| `tests/unit/research/backtest/test_trade_log.py` | +0 (assertion list extended) | 5 | Parquet schema list updated to include 4 new D1-A column names. |
| **Total D1-A-focused tests at end of Phase 3i-B1** | **+23** | **~95** | |

Pytest count delta: prior **645** (Phase 3i-A merge) → after Phase 3i-B1 **668** = +23 net (+21 new D1-A engine dispatch tests + 5 replacement guard/dispatch tests in `test_engine_d1a_guard.py` minus 3 prior guard tests = +2; minus 1 if any other adjustments). The pytest output is the binding figure: 668 passed.

```
============================= test session starts =============================
668 passed in 12.56s
```

## 12. Quality-gate results

All four pre-merge gates green on the Phase 3i-B1 branch tip:

| Gate | Command | Result |
|------|---------|--------|
| Test suite | `uv run pytest` | **668 passed** in 12.56s |
| Linter | `uv run ruff check .` | **All checks passed!** |
| Formatter | `uv run ruff format --check .` | **156 files already formatted** |
| Type checker | `uv run mypy src` | **Success: no issues found in 61 source files** |

## 13. H0 / R3 / F1 control reproduction results

Per the Phase 3h §9 / Phase 3i-B1 brief: full 9-cell control set (5 controls × {BTC + ETH summary metrics each except F1 R) reproduces bit-for-bit via `diff` against prior committed baselines.

| Control | Window | Slippage | Stop trigger | Symbol | `diff` vs prior baseline |
|---------|--------|----------|--------------|--------|--------------------------|
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

All 10 cells (5 controls × 2 symbols) reproduce bit-for-bit on every summary metric. The D1-A engine wiring (new dispatch path, new lifecycle counters, new TradeRecord fields, engine guard lifted) does NOT perturb V1 or F1 dispatch.

## 14. Confirmation that D1-A candidate backtests were not run

Confirmed. No D1-A R MED, R LOW, R HIGH, R MED TRADE_PRICE, V MED, V LOW, V HIGH, or V TRADE_PRICE cell was executed on the real v002 dataset. The only D1-A engine invocations during Phase 3i-B1 were:

- Synthetic in-memory tests in `test_engine_d1a_dispatch.py` (21 tests, ~22 warmup bars + a handful of post-warmup bars each).
- The `check-imports` subcommand of the runner scaffold (no engine run).

No real-dataset D1-A backtest occurred. The runner scaffold's `d1a` subcommand exits non-zero without `--phase-3j-authorized` AND exits non-zero even with the flag (Phase 3i-B1 double-gate).

## 15. Confirmation that D1-A diagnostics or first-execution gate were not evaluated

Confirmed. Phase 3i-B1 did not compute any of: M1 / M2 / M3 mechanism checks; per-funding-regime performance; per-volatility-regime performance; mean_R_by_exit_reason; aggregate_R_by_exit_reason; TIME_STOP-subset mean R; funding-accrual contribution decomposition; LOW/MED/HIGH cost sensitivity for D1-A; mark-price vs trade-price for D1-A; first-execution gate verdict mapping. All are reserved for Phase 3j (or a subsequent operator-authorized phase) per the Phase 3h §6 / §15 staged plan.

## 16. Confirmation that no derived funding-aware dataset was generated or committed

Confirmed. The `funding_aware_features__v001` derived feature dataset (defined in Phase 3h §4.4) was NOT generated by Phase 3i-B1. No `data/derived/funding_aware_features__v001/` directory exists. No `data/` artifact was generated for D1-A; the only `data/` writes during Phase 3i-B1 were the 5 control re-runs (H0 R/V, R3 R/V, F1 R) under existing git-ignored `data/derived/backtests/` directories. `git status` confirms zero `data/` entries staged.

## 17. Confirmation of preserved scope

| Category | Status |
|----------|--------|
| Phase 2f thresholds (§10.3 / §10.4 / §11.3 / §11.4) | UNCHANGED |
| **§11.6 = 8 bps HIGH per side** | UNCHANGED (Phase 2y closeout preserved verbatim) |
| §1.7.3 project-level locks | UNCHANGED |
| H0 baseline parameters | UNCHANGED |
| R3 sub-parameters | UNCHANGED |
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
| `src/prometheus/research/backtest/config.py` | UNCHANGED (Phase 3i-A validator extension still applies) |
| `src/prometheus/research/backtest/accounting.py`, `fills.py`, `funding_join.py`, `simulation_clock.py`, `sizing.py`, `stops.py` | UNCHANGED |
| `src/prometheus/research/backtest/report.py` | UNCHANGED (Phase 3j runner will extend if/when authorized) |
| `data/` directory | UNCHANGED, NO COMMITS |

The locked-axis additions under Phase 3i-B1 are limited to:

- `BacktestEngine.run` guard lifted; D1-A dispatch added.
- `_run_symbol_d1a` and helper methods added.
- `FundingAwareLifecycleCounters` + `_D1ATradeMetadata` dataclasses added.
- `BacktestRunResult.funding_aware_counters_per_symbol` field added.
- 4 new `TradeRecord` fields + parquet schema additions.
- Runner scaffold script added (guarded, fails closed).

None of these constitute a Phase 2f-framework threshold change, §1.7.3 project-lock change, or a change to existing locked sub-parameters of H0 / R3 / R1a / R1b-narrow / R2 / F1.

## 18. Phase 3j readiness

**Phase 3j (or Phase 3i-B2) is safe to consider after operator review of this Phase 3i-B1 checkpoint.**

The Phase 3i-B1 engine wiring is the correct foundation for Phase 3j's candidate run + first-execution gate evaluation:

- The `BacktestEngine` D1-A dispatch path is fully implemented and tested (21 synthetic engine tests + 5 dispatch / counters tests).
- `FundingAwareLifecycleCounters` event-level identity is enforced and tested.
- `TradeRecord` carries the required D1-A fields (4 new + 2 reused).
- The runner scaffold is in place; Phase 3j needs only to implement the run-loop body and remove the second-gate `"D1-A run-loop not yet implemented"` exit.
- All quality gates (pytest / ruff check / ruff format / mypy) are green.
- All 9 control cells (H0 R/V × BTC/ETH; R3 R/V × BTC/ETH; F1 R × BTC/ETH) reproduce bit-for-bit, proving Phase 3i-B1's engine surface additions do not perturb existing dispatch.

Phase 3j is **NOT** authorized by Phase 3i-B1. Phase 3j requires a separately-authorized operator decision after this Phase 3i-B1 checkpoint is reviewed and merged.

---

**End of Phase 3i-B1 D1-A engine-wiring controls checkpoint report.** Engine wiring complete; D1-A engine path implemented; Phase 3i-A guard lifted; lifecycle counters event-level with identity enforcement; TradeRecord extended; runner scaffold guarded; ~23 new D1-A engine dispatch tests pass; quality gates all green (668 pytest); H0 / R3 / F1 controls reproduce bit-for-bit on all 10 cells; D1-A locked spec preserved verbatim per Phase 3g binding; no D1-A candidate backtest run; no D1-A diagnostics computed; no derived dataset generated; no `data/` commit; no Phase 2f threshold change; no §1.7.3 lock change; no paper/shadow / Phase 4 / live-readiness / deployment / MCP / Graphify / `.mcp.json` / credentials / exchange-write change. Phase 3j NOT authorized. Awaiting operator review.
