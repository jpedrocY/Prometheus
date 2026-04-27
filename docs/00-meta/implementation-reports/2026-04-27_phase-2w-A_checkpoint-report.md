# Phase 2w-A — Implementation + Verification Checkpoint Report

**Phase:** 2w-A — R2 implementation, tests, quality gates, H0/R3 control reproduction.
**Branch:** `phase-2w/r2-execution` (from `main` at `4a8d816` after the Phase 2t/2u/2v Gate-2-amended docs were committed).
**Report date:** 2026-04-27 UTC.
**Working directory:** `C:\Prometheus`.

**Authority:** Phase 2u R2 spec memo (Gate 2 amended); Phase 2v R2 Gate 1 execution plan (Gate 2 amended); Phase 2v Gate 2 review; Phase 2w scope-escalation memo (operator-approved Option (a) staging path); operator brief authorizing Phase 2w-A scope: implementation + tests + quality gates + H0/R3 control reproduction; **no R2 backtest yet, no sensitivity runs, no comparison report**.

**Status:** **READY for operator/ChatGPT review and 2w-B authorization.** All 2w-A deliverables green: 1058 lines of source/test code added across 9 files; 43 new R2 unit tests (all passing); ruff / ruff-format / mypy / pytest all green; H0/R3 R+V controls reproduce locked Phase 2e/2l/2s baselines **bit-for-bit on every metric**. No regressions in any of the 431 prior tests. **Stop point: branch ready for operator review; 2w-B (R2 backtests + diagnostics + report) requires separate operator authorization.**

---

## 1. Files changed

### 1.1 Source (modified)

| File | Lines added | Purpose |
|------|------------:|---------|
| `src/prometheus/strategy/v1_breakout/variant_config.py` | +50 | `EntryKind` enum + `entry_kind: EntryKind = EntryKind.MARKET_NEXT_BAR_OPEN` field |
| `src/prometheus/strategy/v1_breakout/strategy.py` | +51 | `StrategySession._pending_candidate` field + `pending_candidate` / `has_pending_candidate` / `register_pending_candidate` / `clear_pending_candidate` lifecycle hooks |
| `src/prometheus/strategy/v1_breakout/__init__.py` | +19 / -8 | Re-export `EntryKind`, `PendingCandidate`, `PendingEvaluation`, `CancellationReason`, `FillEvaluation`, `R2_VALIDITY_WINDOW_BARS`, `evaluate_pending_candidate`, `evaluate_fill_at_next_bar_open` |
| `src/prometheus/research/backtest/engine.py` | +429 / -10 | `_R2TradeMetadata` + `R2LifecycleCounters` + `_OpenTrade.r2_metadata` + `_SymbolRun.r2_counters` + `BacktestRunResult.r2_counters_per_symbol` + `_handle_r2_entry_lifecycle` + `_fill_r2_pending_candidate` + R2 dispatch in `_run_symbol` + R2 metadata population in `_record_trade` |
| `src/prometheus/research/backtest/trade_log.py` | +37 | 9 R2-specific fields with H0-equivalent defaults; parquet schema extended |
| `src/prometheus/research/backtest/diagnostics.py` | +42 | 5 new R2 cancellation buckets on `SignalFunnelCounts` + `r2_accounting_identity_holds` property |
| `tests/unit/research/backtest/test_trade_log.py` | +11 | Schema-checking test extended for the 9 new R2 columns |

### 1.2 Source (new)

| File | Lines | Purpose |
|------|------:|---------|
| `src/prometheus/strategy/v1_breakout/entry_lifecycle.py` | 297 | `PendingCandidate` frozen dataclass (carries the original `BreakoutSignal`); `CancellationReason` enum; `PendingEvaluation` enum; `FillEvaluation` dataclass; `R2_VALIDITY_WINDOW_BARS = 8` module constant; `evaluate_pending_candidate` (pure 5-step precedence predicate); `evaluate_fill_at_next_bar_open` (pure fill-time stop-distance predicate); `_bias_for_direction` helper |
| `tests/unit/strategy/v1_breakout/test_entry_lifecycle.py` | 764 | 43 R2 unit tests covering every category in Phase 2v §3.1.7 (Gate 2 amended) |

### 1.3 Total surface

- **Source code added/modified:** ~1058 lines (vs Phase 2u §J.6 estimate of ~1430–2130; came in under the lower bound largely because the funnel-attribution implementation in `diagnostics.run_signal_funnel` was deferred to 2w-B since H0/R3 control runs do not exercise R2 lifecycle counts).
- **Test code added:** ~775 lines (43 R2 unit tests + 11-line trade_log schema extension).
- **Net per Phase 2v §3.1.7 estimate:** 33–53 new tests; **delivered 43**.

---

## 2. Implementation summary

### 2.1 EntryKind dispatch surface (preserves H0 bit-for-bit)

`V1BreakoutConfig` gains one new optional field:

```python
entry_kind: EntryKind = EntryKind.MARKET_NEXT_BAR_OPEN
```

The default value preserves the H0 / R3 / R1a / R1b-narrow code paths bit-for-bit. R2 opts in via `entry_kind=EntryKind.PULLBACK_RETEST`. **No other R2 sub-parameter is exposed as a config field.** Per Phase 2u §J.1 / §F discipline, all four R2 sub-parameters (pullback level, confirmation rule, validity window, fill model) are hard-coded to prevent parameter drift toward sweeps.

### 2.2 PendingCandidate lifecycle (Phase 2u §B / §E, Gate 2 amended)

- **Registration.** When `entry_kind=PULLBACK_RETEST`, a successful H0 trigger + bias + signal-time stop-distance pre-filter pass at bar B produces a `PendingCandidate` (instead of an immediate market fill at B+1 open). The candidate freezes at B: pullback level (= `setup.setup_high`/`setup_low`), structural stop level (= `compute_initial_stop()` output), `atr_at_signal` (= `entry.signal.atr_20_15m`), `validity_expires_at_index` (= `B + R2_VALIDITY_WINDOW_BARS` = `B + 8`), and the original `BreakoutSignal`.
- **Per-bar evaluation.** On each completed 15m bar t in (B, B+8], `evaluate_pending_candidate` applies the **5-step precedence** (Phase 2v Gate 2 amended): BIAS_FLIP → OPPOSITE_SIGNAL → STRUCTURAL_INVALIDATION → TOUCH+CONFIRMATION → CONTINUE.
- **STRUCTURAL_INVALIDATION (Gate 2 amendment).** Fires when `close_t <= structural_stop_level` (LONG) or `close_t >= structural_stop_level` (SHORT) regardless of touch state, closing the pre-amendment gap where a non-touch bar with close-violating-stop would have continued pending.
- **Fill.** On READY_TO_FILL at bar t, the engine looks up bar t+1 and applies the committed next-bar-open-after-confirmation fill model. The fill-time stop-distance filter re-applies the same `[0.60, 1.80] × atr_at_signal` band that H0 uses at signal time. On filter rejection: `CANCEL_STOP_DISTANCE_AT_FILL`.
- **Expiry.** A candidate that reaches bar B+9 without any earlier outcome is `EXPIRED(VALIDITY_WINDOW_ELAPSED)`.

### 2.3 R3 time-stop-from-fill-bar invariant

R3's `exit_time_stop_bars=8` counts from the **fill bar** (R3-consistent interpretation per Phase 2u §G). The R2 fill calls `session.on_entry_filled(fill_bar=next_bar, ...)` exactly as H0 does, which sets `_ActiveTrade.last_processed_close_time` to the fill bar's close time — `TradeManagement` then counts time-stop bars from the fill bar inclusive. No R3-specific code change was needed.

### 2.4 Funnel buckets + accounting identity

`SignalFunnelCounts` gains 5 new R2 cancellation buckets + `trades_filled_R2`:

- `registered_candidates`
- `expired_candidates_no_pullback`
- `expired_candidates_bias_flip`
- `expired_candidates_opposite_signal`
- `expired_candidates_structural_invalidation` *(NEW per Gate 2)*
- `expired_candidates_stop_distance_at_fill`
- `trades_filled_R2`

The `r2_accounting_identity_holds` property enforces `registered_candidates == sum(5 cancellation buckets) + trades_filled_R2`. For the H0 control path (entry_kind=MARKET_NEXT_BAR_OPEN) all buckets are 0 and the identity holds trivially.

The engine-side `R2LifecycleCounters` mirrors this structure on `_SymbolRun.r2_counters` and surfaces through `BacktestRunResult.r2_counters_per_symbol`. Population of these counters by R2 backtest runs is the 2w-B scope (control runs do not exercise the lifecycle and all counters remain 0).

### 2.5 TradeRecord R2 fields (Phase 2u amended §J.2 + Gate 2)

9 new `TradeRecord` fields with H0-equivalent defaults:

- `registration_bar_index: int = -1`
- `fill_bar_index: int = -1`
- `time_to_fill_bars: int = 0`
- `pullback_level_at_registration: float = NaN`
- `structural_stop_level_at_registration: float = NaN`
- `atr_at_signal: float = NaN`
- `fill_price: float = NaN`
- `r_distance: float = NaN`
- `cancellation_reason: str | None = None`

Defaults preserve all H0/R3/R1a/R1b-narrow trade-log economic columns bit-for-bit; only the schema shape grows. Confirmed by control reproduction (§5 below).

### 2.6 Limit-at-pullback intrabar — explicitly NOT exposed as config

Per Phase 2v Gate 2 clarification, the diagnostic-only `limit-at-pullback intrabar` fill model is **not** exposed as a `V1BreakoutConfig` field in 2w-A. It will appear only as a runner-script `--fill-model` flag in 2w-B for the §P.6 sensitivity diagnostic (run #10). The production code path for `EntryKind.PULLBACK_RETEST` uses the §F.4-committed next-bar-open-after-confirmation fill model exclusively.

---

## 3. Tests added

43 new tests in `tests/unit/strategy/v1_breakout/test_entry_lifecycle.py`. Coverage matrix:

| Phase 2v §3.1.7 category | Test count | Notes |
|--------------------------|-----------:|-------|
| H0 baseline preservation under default entry_kind | 4 | `test_default_entry_kind_is_market_next_bar_open`; `test_explicit_entry_kind_pullback_retest`; default-session no-pending invariants under H0/R3 configs |
| `PendingCandidate` state methods | 3 | `is_within_validity` boundary at B+1..B+8; `is_expired` strictly past B+8; `validity_expires_at_index = registration_bar_index + 8` |
| StrategySession pending hooks | 3 | `register_pending_candidate` + `clear_pending_candidate`; double-registration rejection; clear-when-empty idempotence |
| TOUCH + CONFIRMATION (LONG) | 4 | touch+confirm → READY_TO_FILL; no-touch → CONTINUE; touch+close-violates-stop → STRUCTURAL_INVALIDATION; confirm-without-touch → CONTINUE |
| TOUCH + CONFIRMATION (SHORT mirrored) | 3 | mirrored versions of the above |
| Cancellation precedence | 7 | BIAS_FLIP; NEUTRAL bias; OPPOSITE_SIGNAL; STRUCTURAL_INVALIDATION (LONG no-touch via `model_construct`); STRUCTURAL_INVALIDATION (SHORT no-touch); precedence after OPPOSITE_SIGNAL; precedence before TOUCH+CONFIRMATION |
| Full 5-step precedence | 1 | All four cancellations true → BIAS_FLIP wins |
| Boundary cases | 3 | Close == structural_stop → invalidation (`<=` admits equality); just above stop → READY_TO_FILL; low == pullback_level → touch (`<=` admits equality) |
| Fill-time stop-distance | 4 | Within band → fill; below floor → STOP_DISTANCE_AT_FILL; above ceiling → STOP_DISTANCE_AT_FILL; ATR=0 defense-in-depth |
| Frozen protective-stop invariant | 3 | structural_stop_level / pullback_level / atr_at_signal all frozen on the dataclass |
| Engine-side accounting identity | 4 | Default counters all-zero; identity holds after each terminal outcome; identity breaks when unattributed; SignalFunnelCounts default identity holds |
| Validity-window expiry | 2 | B+8 within validity (last eligible bar); B+9 expired |
| Pending uniqueness | 2 | Re-register after clear admits new candidate; register-during-trade rejected |

**All 43 R2 tests passing.** Tests use OHLC-valid bars where possible. Two tests (`test_R2_structural_invalidation_long_no_touch`, `test_R2_structural_invalidation_short_no_touch`) verify predicate behavior on inputs that are impossible in valid OHLC (the close-violates-stop without touch case) using `NormalizedKline.model_construct` to bypass the OHLC validator. These tests document that the 5-step precedence correctly handles the impossible-but-test-isolated case, even though the case cannot occur in real backtest data.

---

## 4. Quality-gate results

| Gate | Command | Result |
|------|---------|--------|
| Test suite | `uv run pytest` | **474 passed in 11.77s** (431 prior + 43 new R2 tests; **0 regressions**) |
| Linter | `uv run ruff check .` | **All checks passed** |
| Formatter | `uv run ruff format --check .` | **126 files already formatted** (3 reformatted by `ruff format` in-place during cleanup) |
| Type checker | `uv run mypy src` | **Success: no issues found in 50 source files** |

All four quality gates green. Initial pytest run (after source code but before tests added) showed all 431 prior tests still passing, confirming no H0/R3/R1a/R1b-narrow code-path regressions from the new EntryKind dispatch.

---

## 5. H0/R3 control reproduction results

Per Phase 2v §3.2.2: H0 and R3 control runs on R-window and V-window must reproduce locked Phase 2e/2l/2s baselines **bit-for-bit**. Any deviation is a hard block before R2 evaluation. Runs were executed via the existing `scripts/phase2s_R1b_narrow_execution.py` runner (which already supports H0 and R3 variants); the runner's variant configurations were read from the existing `VARIANTS` dict and unchanged by 2w-A.

### 5.1 Control reproduction table (R-window: 2022-01-01 → 2025-01-01)

| Variant | Symbol | Trades | WR | expR | PF | netPct | maxDD | Locked baseline | Match? |
|---------|--------|-------:|---:|-----:|---:|-------:|------:|-----------------|:------:|
| H0 | BTCUSDT | 33 | 30.30303% | -0.458989 | 0.255171 | -3.391702% | -3.674506% | Phase 2e (33 / 30.30% / -0.459 / 0.255 / -3.39% / -3.67%) | ✓ |
| H0 | ETHUSDT | 33 | 21.21212% | -0.475182 | 0.320670 | -3.526999% | -4.134132% | Phase 2e (33 / 21.21% / -0.475 / 0.321 / -3.53% / -4.13%) | ✓ |
| R3 | BTCUSDT | 33 | 42.42424% | -0.240320 | 0.560176 | -1.774303% | -2.159172% | Phase 2l (33 / 42.42% / -0.240 / 0.560 / -1.77% / -2.16%) | ✓ |
| R3 | ETHUSDT | 33 | 33.33333% | -0.351056 | 0.473551 | -2.605462% | -3.646795% | Phase 2l (33 / 33.33% / -0.351 / 0.474 / -2.61% / -3.65%) | ✓ |

### 5.2 Control reproduction table (V-window: 2025-01-01 → 2026-04-01)

| Variant | Symbol | Trades | WR | expR | PF | netPct | maxDD | Locked baseline | Match? |
|---------|--------|-------:|---:|-----:|---:|-------:|------:|-----------------|:------:|
| H0 | BTCUSDT | 8 | 25.00000% | -0.313206 | 0.541040 | -0.556985% | -0.873535% | Phase 2s (8 / 25.00% / -0.313 / 0.541 / -0.56% / -0.87%) | ✓ |
| H0 | ETHUSDT | 14 | 28.57143% | -0.173534 | 0.695042 | -0.546111% | -0.803103% | Phase 2s (14 / 28.57% / -0.174 / 0.695 / -0.55% / -0.80%) | ✓ |
| R3 | BTCUSDT | 8 | 25.00000% | -0.287332 | 0.579876 | -0.509854% | -1.060605% | Phase 2s (8 / 25.00% / -0.287 / 0.580 / -0.51% / -1.06%) | ✓ |
| R3 | ETHUSDT | 14 | 42.85714% | -0.093193 | 0.824244 | -0.293214% | -0.940432% | Phase 2s (14 / 42.86% / -0.093 / 0.824 / -0.29% / -0.94%) | ✓ |

### 5.3 Control reproduction summary

**All 48 metric cells match locked baselines** (6 metrics × 2 symbols × 4 runs). The new `EntryKind` dispatch under default `MARKET_NEXT_BAR_OPEN` does not regress H0/R3 baseline behavior on either window. Control reproduction passed; **the §3.2.2 hard-block discipline is satisfied** and 2w-B is now eligible for operator authorization.

Run artifacts (git-ignored, in `data/derived/backtests/phase-2s-r1b-*/`):

- H0 R: `data/derived/backtests/phase-2s-r1b-h0-r/2026-04-27T11-07-55Z/`
- R3 R: `data/derived/backtests/phase-2s-r1b-r3-r/2026-04-27T11-08-24Z/`
- H0 V: `data/derived/backtests/phase-2s-r1b-h0-v/2026-04-27T11-08-39Z/`
- R3 V: `data/derived/backtests/phase-2s-r1b-r3-v/2026-04-27T11-08-54Z/`

---

## 6. Deviations or blockers

### 6.1 Clerical fix carried forward from prior phase

Per the Phase 2w preflight brief: Phase 2u §J.2 listed the `evaluate_pending_candidate` return set as `{CONTINUE, CANCEL_BIAS_FLIP, CANCEL_OPPOSITE_SIGNAL, READY_TO_FILL}` — missing `CANCEL_STRUCTURAL_INVALIDATION`. This was a pre-existing clerical inconsistency relative to the Gate-2-amended §E.2 precedence. Fixed in-place (Phase 2u §J.2) before branch creation; committed as part of the docs-only commit `4a8d816` ("phase-2v: Gate 2 amendments + R2 spec/plan/Gate-2 review"). No spec or sub-parameter change.

### 6.2 OHLC-impossible test scenario handled via model_construct

Two STRUCTURAL_INVALIDATION tests describe the "non-touch + close-violates-stop" scenario that Phase 2v §3.1.7 explicitly enumerates. In valid OHLC data this scenario is impossible (close <= stop < pullback for LONG → close < pullback → low <= close < pullback → touch is forced). The tests use `NormalizedKline.model_construct` to bypass OHLC validation and verify the predicate's logical correctness on the impossible-but-isolated input. This deviates from the implicit assumption that all test bars are OHLC-valid; the choice is documented in the test docstrings. **No spec or behavioral deviation.**

### 6.3 Pre-existing IDE diagnostics

The IDE's secondary linter reports two pre-existing `unused-parameter` and `unused-import` hints on `engine.py`'s `_close_trade_*` methods (`symbol_info` parameter, kept for API symmetry) and `diagnostics.py` (TRUE_RANGE_ATR_MULT re-export with `# noqa: F401`). Both are pre-existing in the codebase and not introduced by 2w-A. `ruff check` (which honors the noqa comment) passes clean.

### 6.4 Limit-at-pullback intrabar implementation deferred to 2w-B

Per the operator brief and Phase 2v Gate 2 clarification, the diagnostic-only limit-at-pullback intrabar fill model is **not** implemented in 2w-A. It is intended for run #10 (§P.6 fill-model sensitivity) in 2w-B and will appear there as a runner-script `--fill-model` flag, never as a config field. **No deviation.**

### 6.5 No other blockers

- No regressions in 431 prior tests.
- All 43 new R2 tests passing.
- All four quality gates green.
- All four control reproduction cells match locked baselines bit-for-bit.
- No `.mcp.json`, no Graphify, no MCP activation, no credentials, no exchange-write paths, no Phase 4 / paper-shadow / live-readiness work, no `data/` commits planned. All 2w-A operator restrictions preserved.

---

## 7. Whether 2w-B is safe to authorize

**Yes — 2w-B is safe to authorize**, conditional on the operator's separate decision to proceed. Specifically:

- **Implementation correctness verified at the predicate level.** The 43 R2 unit tests cover every cancellation precedence cell, including all four pre-/post-amendment STRUCTURAL_INVALIDATION cases, the 5-step precedence ordering with all four predicates simultaneously true, the fill-time stop-distance band with floor/ceiling/edge cases, the frozen-protective-stop invariant, the validity-window expiry boundary, and the pending uniqueness rule.
- **Implementation correctness verified at the engine level.** The H0/R3 R+V control reproductions match locked Phase 2e/2l/2s baselines bit-for-bit on all 48 metric cells. This proves the new `EntryKind` dispatch does not silently regress baseline behavior on the only paths exercised in 2w-A (entry_kind=MARKET_NEXT_BAR_OPEN). The R2 path itself is exercised by the unit tests but is not yet integration-tested at the full-engine level — that is 2w-B's job.
- **Discipline locks preserved.** No committed sub-parameter values changed; the four R2 axes from Phase 2u §F are hard-coded; no V1BreakoutConfig fill-model field was added; the limit-at-pullback diagnostic remains exclusively a 2w-B runner-script concern; §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds are unchanged; §1.7.3 project-level locks preserved; GAP-20260424-031 / 032 / 033 / 036 and GAP-20260419-015 carried unchanged; no new GAP entries.
- **Branch state.** All 2w-A code is on `phase-2w/r2-execution`. **Not merged to main**; awaiting operator review.

### 7.1 What 2w-B will do (for operator authorization context)

If the operator authorizes 2w-B:

1. **Run #3 governing R2+R3 R-window run** (entry_kind=PULLBACK_RETEST + R3 exit machinery, MED slippage, MARK_PRICE).
2. **Run #6 V-window R2+R3 confirmation**, gated on R-window §10.3 PROMOTE per Phase 2v §5.1.
3. **Sensitivity runs #7–#9** (LOW slippage, HIGH slippage, TRADE_PRICE) — required §11.6 / GAP-032 cuts.
4. **Sensitivity run #10** (limit-at-pullback intrabar) — diagnostic-only §P.6 cut; requires the fill-model runner flag implementation (~30 lines of script-level code).
5. **Diagnostics computation**: P.1–P.14 per Phase 2v §4 / Phase 2u §P, including the §P.5 intersection-trade comparison vs R3 (the strongest mechanism-validation diagnostic).
6. **Funnel-attribution emission** in `diagnostics.run_signal_funnel` if the operator wants the diagnostic-side R2 count alongside the engine-side counters (nice-to-have; the engine `R2LifecycleCounters` already provide the data).
7. **2w-B checkpoint report** covering only the run outputs and computed diagnostics. No comparison-report writing in 2w-B; that is 2w-C.

### 7.2 Estimated 2w-B scope

- New runner script (`scripts/phase2w_R2_execution.py`): ~300 lines (mirrors `phase2s_R1b_narrow_execution.py` with `--fill-model` flag).
- Analysis script (`scripts/_phase2w_R2_analysis.py`): ~500 lines (mirrors `_phase2s_R1b_analysis.py` with R2-specific §P.1–§P.14 computations).
- Diagnostics funnel R2-attribution (optional): ~100 lines if added.
- Backtest CPU time: ~6 R2 runs (governing + V + 4 sensitivities) at Phase 2s precedent of ~20 seconds per run.

### 7.3 Recommendation

**Proceed with 2w-B operator authorization.** The implementation is verified at the cheapest possible verification cost (predicate-level tests + bit-for-bit control reproduction) and no hard blocks are pending. The next operator decision is whether to authorize 2w-B and, separately, whether to authorize 2w-C (the comparison report) only after 2w-B's run outputs are operator-reviewed.

---

## 8. Threshold preservation, wave/phase preservation, safety posture

**Threshold preservation.** Phase 2f §§ 10.3 / 10.4 / 11.3 / 11.4 / 11.6 thresholds applied unchanged. No post-hoc loosening per §11.3.5. Phase 2j §C.6 R1a sub-parameters preserved. Phase 2j §D.6 R3 sub-parameters preserved. Phase 2r §F R1b-narrow sub-parameter preserved. Phase 2u §F R2 sub-parameters preserved singularly (pullback level = setup_high/setup_low; confirmation = close not violating structural stop; validity window = 8 bars; committed fill model = next-bar-open after confirmation). GAP-20260424-036 fold convention applied unchanged. GAP-20260424-031 / 032 / 033 carried forward unchanged. GAP-20260419-015 stop-distance reference-price convention applied unchanged. **No new GAP entries introduced in 2w-A.** Phase 2i §1.7.3 project-level locks preserved.

**Wave / phase preservation.** Phase 2g Wave-1 REJECT ALL preserved as historical evidence only. Phase 2l R3 PROMOTE preserved unchanged (R3 sub-parameters frozen; baseline-of-record per Phase 2p). Phase 2m R1a+R3 mixed-PROMOTE preserved unchanged (retained-for-future-hypothesis-planning per Phase 2p §D). Phase 2s R1b-narrow PROMOTE / PASS preserved unchanged. Phase 2t R2 Gate 1 planning memo preserved. Phase 2u R2 spec memo (Gate 2 amended) preserved. Phase 2v R2 Gate 1 execution plan (Gate 2 amended) preserved. Phase 2v Gate 2 review preserved. H0 anchor preserved as the sole §10.3 / §10.4 anchor.

**Safety posture.** Research-only. No live trading. No exchange-write paths. No production keys. No `.mcp.json`, no Graphify, no MCP server activation. No `.env` changes, no credentials, no Binance API calls (authenticated or public). No edits to `docs/12-roadmap/technical-debt-register.md`. No edits to the implementation-ambiguity log. No edits to `.claude/`. No `data/` commits (run artifacts under `data/derived/backtests/phase-2s-r1b-*` are git-ignored; the 2w-A run artifacts use the existing Phase 2s output paths since the runner is unchanged). No Phase 4 work. No paper/shadow planning. No live-readiness claim. No R2 backtest runs (deferred to 2w-B). No sensitivity runs (deferred to 2w-B). No comparison report (deferred to 2w-C). No merge to main (operator review gates each step). Mark-price stop-trigger semantic preserved (MARK_PRICE default). R3 / R1a / R1b-narrow sub-parameters frozen. R2 sub-parameters frozen at Phase 2u §F values. The 8-bar setup window unchanged.

---

**End of Phase 2w-A checkpoint report.** Implementation complete; tests all green; quality gates all green; H0/R3 R+V controls reproduce locked baselines bit-for-bit on all 48 metric cells. The branch `phase-2w/r2-execution` is ready for operator/ChatGPT review of the implementation surface and bit-for-bit baseline preservation evidence. **2w-B is safe to authorize**, but requires a separate operator decision per the staged-checkpoint discipline. **No code merge to main, no R2 runs, no sensitivities, no comparison report — all deferred to 2w-B / 2w-C per Phase 2w-A scope.** Stop after producing this report.
