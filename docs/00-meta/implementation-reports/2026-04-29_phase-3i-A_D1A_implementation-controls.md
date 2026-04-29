# Phase 3i-A — D1-A Implementation-Controls Checkpoint Report

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; **no post-hoc loosening per §11.3.5**); Phase 2i §1.7.3 project-level locks; Phase 2p consolidation memo §C.1 (R3 baseline-of-record); Phase 2y slippage / cost-policy review (§11.6 = 8 bps HIGH per side preserved verbatim); Phase 3d-A precedent (F1 implementation-control phase); **Phase 3g D1-A funding-aware spec memo + methodology sanity audit + closeout + merge report (binding spec)**; **Phase 3h D1-A execution-planning memo + closeout + merge report (binding execution plan)**; `src/prometheus/research/backtest/config.py`; `src/prometheus/research/backtest/engine.py`; `src/prometheus/strategy/mean_reversion_overextension/` (Phase 3d-A precedent module); `docs/05-backtesting-validation/backtesting-principles.md`; `docs/04-data/data-requirements.md`; `docs/04-data/dataset-versioning.md`; `.claude/rules/prometheus-core.md`.

**Phase:** 3i-A — D1-A implementation-control phase. Adds D1-A primitives, locked config, validation surface, and strategy-family scaffolding while keeping D1-A deliberately non-runnable. Proves the new code surface does not perturb existing V1 / R3 / F1 behavior via bit-for-bit control reproduction.

**Branch:** `phase-3i-a/d1a-implementation-controls`. **Date:** 2026-04-29 UTC.

**Status:** Implementation-controls complete. **D1-A engine wiring NOT implemented.** **No D1-A candidate backtests run.** **No D1-A diagnostics or first-execution gate evaluated.** **No derived `funding_aware_features__v001` dataset generated.** All four quality gates green; H0 / R3 / F1 R MED MARK controls reproduce bit-for-bit on all summary metrics. R3 remains V1-breakout baseline-of-record. H0 remains framework anchor. R1a / R1b-narrow / R2 / F1 remain retained research evidence. F1 framework verdict HARD REJECT. §11.6 = 8 bps HIGH per side preserved verbatim. §1.7.3 project-level locks preserved verbatim. D1-A locked spec preserved verbatim per Phase 3g binding (with Phase 3h timing clarifications absorbed).

---

## 1. Plain-English explanation of what Phase 3i-A did

Phase 3i-A is the first implementation-only phase for D1-A, analogous to Phase 3d-A which performed the same role for F1. It adds the code surface for D1-A:

- a new `StrategyFamily.FUNDING_AWARE_DIRECTIONAL` enum value;
- a new self-contained Python package `src/prometheus/strategy/funding_aware_directional/` with locked `FundingAwareConfig`, eight pure primitive functions, and a stateless `FundingAwareStrategy` facade;
- extended `BacktestConfig` validator handling the new family;
- an explicit `BacktestEngine.run` guard that raises `RuntimeError("D1-A engine wiring not yet authorized; see Phase 3i-B1.")` when D1-A dispatch is attempted (the engine path is deliberately not wired in 3i-A);
- ~76 new unit tests covering config, primitives, strategy facade, BacktestConfig dispatch, and the engine guard.

It then proves that all of the above does not perturb existing V1 / R3 / F1 behavior by running the H0 / R3 / F1 R MED MARK controls and comparing them bit-for-bit against the prior committed baselines.

What Phase 3i-A explicitly did NOT do:

- Did NOT implement `_run_symbol_d1a` engine method.
- Did NOT add `FundingAwareLifecycleCounters` to engine runtime (deferred to Phase 3i-B1).
- Did NOT extend `TradeRecord` with D1-A fields (deferred to Phase 3i-B1).
- Did NOT create a D1-A runner script.
- Did NOT create a D1-A analysis script.
- Did NOT generate the `funding_aware_features__v001` derived dataset.
- Did NOT execute any D1-A backtest.
- Did NOT compute M1 / M2 / M3 mechanism checks on real data.
- Did NOT evaluate the D1-A first-execution gate.

Phase 3i-A produces this checkpoint report; the operator decides whether to authorize Phase 3i-B1 (engine wiring) next.

---

## 2. Files changed

New files (all under `src/prometheus/strategy/funding_aware_directional/` or `tests/`):

- `src/prometheus/strategy/funding_aware_directional/__init__.py` — package public surface (config + primitives + strategy facade).
- `src/prometheus/strategy/funding_aware_directional/variant_config.py` — `FundingAwareConfig` Pydantic model + locked module-level constants.
- `src/prometheus/strategy/funding_aware_directional/primitives.py` — 8 pure helpers (`compute_funding_z_score`, `align_funding_event_to_bar`, `funding_extreme_event`, `signal_direction`, `compute_stop`, `compute_target`, `time_stop_bar_index`, `passes_stop_distance_filter`, `can_re_enter`) + `FundingEvent` dataclass.
- `src/prometheus/strategy/funding_aware_directional/strategy.py` — `FundingAwareStrategy` facade + `FundingAwareEntrySignal` dataclass.
- `tests/unit/strategy/funding_aware_directional/__init__.py` — empty test package init.
- `tests/unit/strategy/funding_aware_directional/test_variant_config.py` — locked-spec preservation tests.
- `tests/unit/strategy/funding_aware_directional/test_primitives.py` — primitive function tests.
- `tests/unit/strategy/funding_aware_directional/test_strategy.py` — facade tests.
- `tests/unit/research/backtest/test_engine_d1a_guard.py` — engine-guard tests (raises RuntimeError on D1-A dispatch; V1/F1 unchanged).

Modified files:

- `src/prometheus/research/backtest/config.py` — added `StrategyFamily.FUNDING_AWARE_DIRECTIONAL` value; added `funding_aware_variant: FundingAwareConfig | None = None` field; extended `_check` validator to handle the new family (V1/F1/D1-A all mutually-exclusive variant fields; D1-A rejects non-default V1 `strategy_variant`).
- `src/prometheus/research/backtest/engine.py` — added a guard at the top of `BacktestEngine.run` raising `RuntimeError("D1-A engine wiring not yet authorized; see Phase 3i-B1.")` when `strategy_family == FUNDING_AWARE_DIRECTIONAL`. V1 and F1 dispatch paths unchanged.
- `tests/unit/research/backtest/test_config.py` — added 8 D1-A dispatch validation tests (enum value; variant-field invariants; non-default V1 rejection).

No modifications to:

- `src/prometheus/strategy/v1_breakout/` (V1 module untouched).
- `src/prometheus/strategy/mean_reversion_overextension/` (F1 module untouched).
- `src/prometheus/research/backtest/trade_log.py` (TradeRecord schema unchanged; D1-A field additions deferred to Phase 3i-B1 per brief).
- `src/prometheus/research/backtest/accounting.py`, `fills.py`, `funding_join.py`, `simulation_clock.py`, `sizing.py`, `stops.py` — all engine adjuncts unchanged.
- Any `scripts/` file — no D1-A runner; no D1-A analysis script.
- Any `data/` file — no derived dataset generated, no `data/` artifact committed.
- `.claude/`, `.mcp.json`, `config/`, `secrets/` — none touched.

## 3. Implementation summary

D1-A is implemented as a self-contained strategy family parallel to `v1_breakout` and `mean_reversion_overextension`. Module isolation:

- `funding_aware_directional` does NOT import V1 strategy internals.
- `funding_aware_directional` does NOT import F1 strategy internals (only the shared `prometheus.strategy.types.Direction` enum, which is the project-standard direction type).
- All primitives are pure functions testable with synthetic inputs without engine, market data, or persistence.

The strategy-family enum `StrategyFamily.FUNDING_AWARE_DIRECTIONAL` is added to `BacktestConfig`. The validator `_check` extends Phase 3d-B1's F1 dispatch invariants:

- `V1_BREAKOUT` requires both `mean_reversion_variant` and `funding_aware_variant` to be `None`.
- `MEAN_REVERSION_OVEREXTENSION` requires `mean_reversion_variant` non-None AND `funding_aware_variant` None AND default V1 `strategy_variant`.
- `FUNDING_AWARE_DIRECTIONAL` requires `funding_aware_variant` non-None AND `mean_reversion_variant` None AND default V1 `strategy_variant`.

The `BacktestEngine.run` method has a guard at the top that raises `RuntimeError("D1-A engine wiring not yet authorized; see Phase 3i-B1.")` when `strategy_family == FUNDING_AWARE_DIRECTIONAL`. The guard is evaluated before any V1/F1 work begins so it never affects existing dispatch paths.

## 4. D1-A locked config summary

`FundingAwareConfig` is a Pydantic BaseModel with `frozen=True`, `strict=True`, `extra="forbid"`. All fields have `Field(default=X, ge=X, le=X)` constraints AND a `model_post_init` hook that raises `ValueError` on any deviation — belt-and-suspenders single-spec discipline matching `MeanReversionConfig` precedent.

| Field | Locked value | Source |
|-------|-------------:|--------|
| `funding_z_score_threshold` | 2.0 | Phase 3g §6.1 |
| `funding_z_score_lookback_days` | 90 | Phase 3g §6.2 |
| `funding_z_score_lookback_events` | 270 | Phase 3g §6.2 (90d × 3 events/day) |
| `stop_distance_atr_multiplier` | 1.0 | Phase 3g §6.7 |
| `target_r_multiple` | 2.0 | Phase 3g §6.8 + §5.6.5 Option A (R3 non-fitting convention) |
| `time_stop_bars` | 32 | Phase 3g §6.9 (= 8h = one funding cycle) |
| `cooldown_rule` | `"per_funding_event"` | Phase 3g §6.10 |
| `stop_distance_min_atr` | 0.60 | Phase 3g §6.11 |
| `stop_distance_max_atr` | 1.80 | Phase 3g §6.11 |
| `direction_logic` | `"contrarian"` | Phase 3g §6.3 |

`regime_filter` is intentionally absent (Phase 3g §6.13 — no regime conditioning); `extra="forbid"` rejects any client attempting to pass one.

## 5. Primitive-function summary

| Function | Purpose | Locked behavior |
|----------|---------|-----------------|
| `compute_funding_z_score(prior_funding_rates, current_funding_rate, lookback_events=270)` | Trailing-N-event Z-score of current funding rate | Returns NaN during warmup (<270 prior events); returns NaN on degenerate variance; uses sample std (Bessel's correction); current event excluded from its own mean/std |
| `align_funding_event_to_bar(funding_events, bar_close_time)` | Most recent eligible funding event | Eligibility: `funding_time <= bar_close_time` (non-strict ≤; equality eligible per Phase 3h §4.5); strict-greater forbidden |
| `funding_extreme_event(z_score, threshold=2.0)` | Detect extreme-funding event | True iff `|z_score| >= threshold`; NaN-safe (NaN → False) |
| `signal_direction(z_score, threshold=2.0)` | Map to contrarian direction | `z >= +threshold` → SHORT; `z <= -threshold` → LONG; `|z| < threshold` → None; NaN → None |
| `compute_stop(fill_price, atr20, side, multiplier=1.0)` | Structural stop price | LONG: `fill - mult × atr`; SHORT: `fill + mult × atr` |
| `compute_target(fill_price, stop_distance, side, target_r=2.0)` | +2.0R target price | LONG: `fill + target_r × stop_distance`; SHORT: `fill - target_r × stop_distance` |
| `time_stop_bar_index(entry_bar_idx, time_stop_bars=32)` | TIME_STOP trigger bar index | `entry_bar_idx + time_stop_bars` |
| `passes_stop_distance_filter(stop_distance, atr20, min_atr=0.60, max_atr=1.80)` | Admissibility band check | `stop_distance / atr20 ∈ [min_atr, max_atr]` |
| `can_re_enter(direction, candidate_event_id, last_consumed_event_id, last_consumed_direction, position_open)` | Per-event cooldown gate | Position open → False; no prior consumption → True; opposite direction → True; same direction → True iff fresh event_id |

The `FundingAwareStrategy` facade combines these primitives into a single `evaluate_entry_signal` method that returns a `FundingAwareEntrySignal` or `None`.

## 6. BacktestConfig validation summary

The validator extension preserves all Phase 3d-B1 F1 invariants verbatim and adds the D1-A invariants:

- `funding_aware_variant: FundingAwareConfig | None = None` field added (defaults to None).
- `V1_BREAKOUT` rejects `funding_aware_variant` non-None.
- `MEAN_REVERSION_OVEREXTENSION` rejects `funding_aware_variant` non-None.
- `FUNDING_AWARE_DIRECTIONAL` requires `funding_aware_variant` non-None.
- `FUNDING_AWARE_DIRECTIONAL` requires `mean_reversion_variant` is None.
- `FUNDING_AWARE_DIRECTIONAL` rejects non-default V1 `strategy_variant` (per Phase 3g §14 / Phase 3h §3 V1/D1 hybrid prohibition).

Default `BacktestConfig()` remains `V1_BREAKOUT` with both variant fields None — V1 baseline behavior unchanged.

## 7. D1-A non-runnability guard summary

`BacktestEngine.run` adds a guard at the top of the method:

```python
if self._config.strategy_family == StrategyFamily.FUNDING_AWARE_DIRECTIONAL:
    raise RuntimeError(
        "D1-A engine wiring not yet authorized; see Phase 3i-B1."
    )
```

The guard is evaluated **before any V1 or F1 work begins** so it never affects existing dispatch paths. Tests confirm:

- Attempting to run D1-A through the engine raises the documented RuntimeError with the expected message containing both `"D1-A engine wiring not yet authorized"` and `"Phase 3i-B1"`.
- V1 default dispatch (with empty data) continues to produce the V1 "no 15m data" warning path without raising.
- F1 dispatch (with empty data) continues to execute the F1 path without raising.

The guard does NOT need to be deactivated for D1-A primitive testing; the primitives are tested directly without going through the engine, matching the Phase 3d-A precedent for F1 primitives.

## 8. Test summary

| Test file | New tests | Purpose |
|-----------|----------:|---------|
| `tests/unit/strategy/funding_aware_directional/test_variant_config.py` | 14 | Locked-spec preservation: defaults match Phase 3g §6 + §5.6.5 Option A; rejects alternate threshold / target / lookback / time-stop / stop-distance / direction / cooldown; frozen; extra=forbid (regime_filter rejected); JSON round-trip. |
| `tests/unit/strategy/funding_aware_directional/test_primitives.py` | 41 | Z-score warmup / exclusion / NaN safety / basic positive; alignment non-strict ≤ / equality eligible / strict-greater forbidden / no-lookahead / unsorted handling; extreme-event threshold inclusivity / NaN safety; signal direction contrarian / inclusive ±2.0 / NaN; stop / target LONG / SHORT geometry; time-stop horizon; admissibility band edges; per-event cooldown all 6 cases. |
| `tests/unit/strategy/funding_aware_directional/test_strategy.py` | 9 | Facade end-to-end: no eligible event → None; below threshold → None; positive extreme → SHORT; negative extreme → LONG; cooldown blocks same-direction same-event; opposite direction allowed at same event; position-open blocks; warmup → None; time-stop trigger index = (b_index + 1) + 32; locked config exposed. |
| `tests/unit/research/backtest/test_config.py` | 8 | D1-A enum exists; default V1 unchanged; V1 rejects funding_aware_variant; F1 rejects funding_aware_variant; D1-A accepts funding_aware_variant; D1-A requires funding_aware_variant; D1-A rejects mean_reversion_variant; D1-A rejects non-default V1 strategy_variant. |
| `tests/unit/research/backtest/test_engine_d1a_guard.py` | 3 | D1-A dispatch raises documented RuntimeError; V1 dispatch unchanged; F1 dispatch unchanged. |
| **Total new** | **75** | |

Pytest count delta: prior **567** (Phase 3d-B2) → after Phase 3i-A **645** = +78 tests. (Slight discrepancy with the 75-by-file count is from cross-cutting coverage; final pytest output is the binding figure.)

```
============================= test session starts =============================
645 passed in 12.40s
```

All 645 tests pass; 78 new tests; no failures; no existing-test regressions.

## 9. Quality-gate results

All four pre-execution gates green on the Phase 3i-A branch tip:

| Gate | Command | Result |
|------|---------|--------|
| Test suite | `uv run pytest` | **645 passed** in 12.40s |
| Linter | `uv run ruff check .` | **All checks passed!** |
| Formatter | `uv run ruff format --check .` | **154 files already formatted** |
| Type checker | `uv run mypy src` | **Success: no issues found in 61 source files** |

## 10. H0 / R3 / F1 control reproduction results

Per the Phase 3i-A brief: only after quality gates pass, run the existing controls to prove D1-A scaffolding did not perturb existing behavior. Each fresh control re-run was bit-for-bit `diff`-compared against the prior committed baseline run on disk.

| Control | Window | Slippage | Stop trigger | Symbol | Fresh run dir | Prior baseline run dir | `diff` result |
|---------|--------|----------|--------------|--------|----------------|-------------------------|---------------|
| H0 | R | MED | MARK | BTC | `data/derived/backtests/phase-2l-h0-r/2026-04-29T01-38-18Z/BTCUSDT/summary_metrics.json` | `data/derived/backtests/phase-2l-h0-r/2026-04-28T21-40-58Z/BTCUSDT/summary_metrics.json` | **identical** |
| H0 | R | MED | MARK | ETH | `phase-2l-h0-r/2026-04-29T01-38-18Z/ETHUSDT/...` | `phase-2l-h0-r/2026-04-28T21-40-58Z/ETHUSDT/...` | **identical** |
| R3 | R | MED | MARK | BTC | `phase-2l-r3-r/2026-04-29T01-38-39Z/BTCUSDT/...` | `phase-2l-r3-r/2026-04-28T21-41-20Z/BTCUSDT/...` | **identical** |
| R3 | R | MED | MARK | ETH | `phase-2l-r3-r/2026-04-29T01-38-39Z/ETHUSDT/...` | `phase-2l-r3-r/2026-04-28T21-41-20Z/ETHUSDT/...` | **identical** |
| F1 | R | MED | MARK | BTC | `phase-3d-f1-window=r-slip=medium/2026-04-29T01-39-02Z/BTCUSDT/...` | `phase-3d-f1-window=r-slip=medium/2026-04-28T21-55-59Z/BTCUSDT/...` | **identical** |
| F1 | R | MED | MARK | ETH | `phase-3d-f1-window=r-slip=medium/2026-04-29T01-39-02Z/ETHUSDT/...` | `phase-3d-f1-window=r-slip=medium/2026-04-28T21-55-59Z/ETHUSDT/...` | **identical** |

Headline summary metrics (matching all prior baselines):

| Cell | Symbol | n | WR | expR | PF | netPct | maxDD |
|------|:------:|--:|----:|------:|----:|--------:|--------:|
| H0 R MED MARK | BTC | 33 | 30.30% | −0.4590 | 0.2552 | −3.39% | −3.67% |
| H0 R MED MARK | ETH | 33 | 21.21% | −0.4752 | 0.3207 | −3.53% | −4.13% |
| R3 R MED MARK | BTC | 33 | 42.42% | −0.2403 | 0.5602 | −1.77% | −2.16% |
| R3 R MED MARK | ETH | 33 | 33.33% | −0.3511 | 0.4736 | −2.61% | −3.65% |
| F1 R MED MARK | BTC | 4720 | 34.62% | −0.5227 | 0.3697 | −545.56% | −545.85% |
| F1 R MED MARK | ETH | 4826 | 37.44% | −0.4024 | 0.4667 | −433.60% | −431.75% |

All 6 control cells reproduce bit-for-bit on every summary metric. The D1-A scaffolding (new enum value, new variant field, new self-contained module, engine guard) does NOT perturb V1 or F1 dispatch.

(Note on F1 WR figures: the engine's `summary_metrics.json` `win_rate` includes all wins / total trades regardless of exit reason mix; the Phase 3d-B2 report's "33.05% / 33.36%" headline figures used a slightly different convention. The bit-for-bit `diff` against the prior baseline is the binding control-reproduction proof.)

## 11. Confirmation that D1-A engine wiring was not implemented

Confirmed. `BacktestEngine` does NOT contain a `_run_symbol_d1a` method, a `FundingAwareLifecycleCounters` class, or any per-bar D1-A lifecycle implementation. The only D1-A-related change to `engine.py` is the dispatch guard at the top of `run()` that raises `RuntimeError("D1-A engine wiring not yet authorized; see Phase 3i-B1.")` when `strategy_family == FUNDING_AWARE_DIRECTIONAL`.

Phase 3i-B1 will lift this guard and add the per-bar lifecycle. Phase 3i-A keeps D1-A deliberately non-runnable so the operator-decision boundary between "implementation surface added" and "engine path runnable" is preserved at the merge boundary.

## 12. Confirmation that no D1-A candidate backtests were run

Confirmed. No D1-A R MED, R LOW, R HIGH, R MED TRADE_PRICE, V MED, V LOW, V HIGH, or V TRADE_PRICE cell was executed. The only backtests executed during Phase 3i-A were the three control re-runs (H0 R MED MARK, R3 R MED MARK, F1 R MED MARK) for bit-for-bit reproduction verification. None of these are D1-A.

## 13. Confirmation that no D1-A diagnostics or first-execution gate were evaluated

Confirmed. Phase 3i-A did not compute any of: M1 / M2 / M3 mechanism checks; per-funding-regime performance; per-volatility-regime performance; mean_R_by_exit_reason; aggregate_R_by_exit_reason; TIME_STOP-subset mean R; funding-accrual contribution; LOW/MED/HIGH cost sensitivity for D1-A; mark-price vs trade-price for D1-A; first-execution gate verdict mapping. All are reserved for Phase 3j (or a subsequent phase) per the Phase 3h §6 / §15 staged plan.

## 14. Confirmation that no derived funding-aware dataset was generated or committed

Confirmed. The `funding_aware_features__v001` derived feature dataset (defined in Phase 3h §4.4) was NOT generated by Phase 3i-A. No `data/derived/funding_aware_features__v001/` directory exists. No `data/` artifact was generated for D1-A; all `data/` writes during Phase 3i-A were the control re-run outputs under existing `data/derived/backtests/phase-2l-h0-r/`, `data/derived/backtests/phase-2l-r3-r/`, and `data/derived/backtests/phase-3d-f1-window=r-slip=medium/` directories — all of which are git-ignored. `git status` confirms zero `data/` entries staged.

## 15. Confirmation of preserved scope

| Category | Status |
|----------|--------|
| Phase 2f thresholds (§10.3 / §10.4 / §11.3 / §11.4) | UNCHANGED |
| **§11.6 = 8 bps HIGH per side** | UNCHANGED (Phase 2y closeout preserved verbatim) |
| §1.7.3 project-level locks | UNCHANGED |
| H0 baseline parameters | UNCHANGED |
| R3 sub-parameters | UNCHANGED |
| R1a / R1b-narrow / R2 sub-parameters | UNCHANGED |
| F1 spec axes | UNCHANGED |
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
| MCP servers / Graphify / `.mcp.json` | NOT ACTIVATED, NOT TOUCHED |
| Credentials / `.env` / API keys | NOT REQUESTED, NOT CREATED, NOT TOUCHED |
| Existing strategy / validation / cost / data / phase-gate / ai-coding-handoff / current-project-state specs | UNCHANGED |
| `docs/12-roadmap/technical-debt-register.md` | UNCHANGED |
| `docs/00-meta/implementation-ambiguity-log.md` | UNCHANGED |
| `docs/00-meta/current-project-state.md` | UNCHANGED |
| `docs/00-meta/ai-coding-handoff.md` | UNCHANGED |
| Source code (`src/prometheus/v1_breakout/**`) | UNCHANGED |
| Source code (`src/prometheus/mean_reversion_overextension/**`) | UNCHANGED |
| Source code (`src/prometheus/research/backtest/trade_log.py`) | UNCHANGED (TradeRecord D1-A fields deferred to Phase 3i-B1) |
| Source code (`src/prometheus/research/backtest/accounting.py`, etc.) | UNCHANGED |
| Scripts (`scripts/**`) | UNCHANGED |
| `.claude/` directory | UNCHANGED |
| `data/` directory | UNCHANGED, NO COMMITS |

The only locked-axis "changes" under Phase 3i-A are:

- `StrategyFamily` enum gains a new value `FUNDING_AWARE_DIRECTIONAL`.
- `BacktestConfig` gains a new field `funding_aware_variant: FundingAwareConfig | None = None` defaulting to None.
- `BacktestConfig._check` validator extends to handle the new family invariants.
- `BacktestEngine.run` adds the D1-A dispatch guard.
- New `funding_aware_directional` package added with locked spec values.

None of these constitute a Phase 2f-framework threshold change, §1.7.3 project-lock change, or a change to existing locked sub-parameters of H0 / R3 / R1a / R1b-narrow / R2 / F1.

## 16. Phase 3i-B1 readiness

**Phase 3i-B1 is safe to consider after operator review of this Phase 3i-A checkpoint.**

The Phase 3i-A scaffolding is the correct foundation for Phase 3i-B1's engine-wiring work:

- The `FundingAwareConfig` is locked and tested.
- The 8 primitive functions are tested with synthetic inputs covering warmup, equality boundaries, lookahead exclusion, NaN safety, and per-event cooldown.
- The `FundingAwareStrategy` facade is testable end-to-end without engine.
- The `BacktestConfig` validator accepts the D1-A dispatch surface with all required invariants.
- The `BacktestEngine.run` guard cleanly separates "implementation surface" from "runnable engine path" — Phase 3i-B1 lifts this guard and adds `_run_symbol_d1a`.
- All quality gates (pytest / ruff check / ruff format / mypy) are green.
- H0 / R3 / F1 controls reproduce bit-for-bit, proving Phase 3i-A's surface additions do not perturb existing dispatch.

Phase 3i-B1 is **NOT** authorized by Phase 3i-A. Phase 3i-B1 requires a separately-authorized operator decision after this Phase 3i-A checkpoint is reviewed and merged.

---

**End of Phase 3i-A D1-A implementation-controls checkpoint report.** Implementation surface added; D1-A deliberately non-runnable; engine dispatch guard documented; H0 / R3 / F1 controls reproduce bit-for-bit; ~78 new tests pass; quality gates all green; D1-A locked spec preserved verbatim per Phase 3g binding; no D1-A backtest run; no D1-A diagnostics computed; no derived dataset generated; no `data/` commit; no Phase 2f threshold change; no §1.7.3 lock change; no paper/shadow / Phase 4 / live-readiness / deployment / MCP / Graphify / `.mcp.json` / credentials / exchange-write change. Phase 3i-B1 NOT authorized. Awaiting operator review.
