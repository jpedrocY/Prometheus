# Phase 2g — Gate 2 Pre-Commit Review

**Working directory:** `C:\Prometheus`
**Branch:** `phase-2g/wave1-variant-execution`
**Date:** 2026-04-24
**Reviewer:** Claude Code (Phase 2g)
**Scope:** Pre-commit review of the Phase 2g wave-1 variant-execution work against the Phase 2f Gate 1 plan and the Phase 2g operator brief. No `git add` / `git commit` has been run. Quality gates are green and pytest is at 396 tests passing.

---

## Phase

**Phase 2g — Wave-1 Variant Execution.**

Implements four operator-approved single-axis variants of the locked v1 breakout strategy (H-A1 setup window 8 → 10, H-B2 expansion 1.0 → 0.75 × ATR20, H-C1 EMA pair 50/200 → 20/100, H-D3 break-even +1.5R → +2.0R) and runs them on the Phase 2f research window R (2022-01-01 → 2025-01-01) with the H0 control. Per Phase 2f §11.3 no-peeking discipline, validation-window V and slippage / stop-trigger sensitivity sweeps are conditional on §10.3 promotion; with REJECT ALL outcome on R, neither was performed.

## 1. Files changed

Two-axis grouping: **code** (strategy + backtest config + engine + diagnostics + stops + tests) and **docs / scripts** (runner + reports).

### Modified (10 source files)

| File | Why                                                                                                                                  |
|---|---|
| `src/prometheus/strategy/v1_breakout/__init__.py`        | Export `V1BreakoutConfig`.                                                                                  |
| `src/prometheus/strategy/v1_breakout/setup.py`           | `detect_setup` accepts optional `setup_size: int = SETUP_SIZE`. Default preserves H0.                       |
| `src/prometheus/strategy/v1_breakout/trigger.py`         | `evaluate_long_trigger` / `evaluate_short_trigger` / `_true_range_passes` accept `expansion_atr_mult: float = TRUE_RANGE_ATR_MULT`. Default preserves H0. |
| `src/prometheus/strategy/v1_breakout/management.py`      | `TradeManagement.on_completed_bar` accepts `break_even_r: float = STAGE_4_MFE_R`. Default preserves H0.     |
| `src/prometheus/strategy/v1_breakout/strategy.py`        | `StrategySession` and `V1BreakoutStrategy` accept a `V1BreakoutConfig` (default = baseline). EMA periods, setup-size slicing, warmup floors, re-entry lockout, trigger expansion mult, and break-even R now flow from the session/strategy config. Module-level `MIN_*_BARS_FOR_*` constants kept for backwards-compatible imports. |
| `src/prometheus/research/backtest/config.py`             | New `StopTriggerSource` StrEnum (MARK_PRICE / TRADE_PRICE). New `BacktestConfig` fields `strategy_variant: V1BreakoutConfig` (default = baseline) and `stop_trigger_source: StopTriggerSource = MARK_PRICE`. |
| `src/prometheus/research/backtest/__init__.py`           | Re-export `StopTriggerSource`.                                                                              |
| `src/prometheus/research/backtest/diagnostics.py`        | `_IncrementalIndicators.__init__` accepts `ema_fast_period` / `ema_slow_period`. `run_signal_funnel` accepts `strategy_config: V1BreakoutConfig | None = None`; uses it to size warmup floors, ring buffer, setup-size slicing, and the TR expansion gate. Default preserves H0. |
| `src/prometheus/research/backtest/engine.py`             | Constructs `V1BreakoutStrategy(config.strategy_variant)` and `StrategySession(symbol=..., config=config.strategy_variant)`. Stop-hit evaluation branches on `config.stop_trigger_source` (MARK_PRICE → mark-price kline keyed by 15m open_time; TRADE_PRICE → the 15m trade-price kline). |
| `src/prometheus/research/backtest/stops.py`              | `evaluate_stop_hit.mark_bar` parameter type relaxed from `MarkPriceKline` to `MarkPriceKline | NormalizedKline`; logic unchanged (both kline types share `.open / .high / .low / .open_time / .close_time / .symbol`). |

### Created (5 files)

| File | Purpose                                                                                                                        |
|---|---|
| `src/prometheus/strategy/v1_breakout/variant_config.py`              | Frozen pydantic `V1BreakoutConfig` model with five overridable axes; defaults match the locked baseline.                       |
| `tests/unit/strategy/v1_breakout/test_variant_config.py`             | 9 unit tests proving (a) defaults match baseline constants on every axis, (b) frozen + strict + extra-forbid, (c) `ema_fast < ema_slow` validator, (d) default-session warmup floors equal baseline, (e) each of the four wave-1 variants moves the axis it claims (H-A1 setup-size, H-B2 expansion, H-C1 EMA pair, H-D3 break-even R). |
| `scripts/phase2g_variant_wave1.py`                                   | Wave-1 runner. CLI: `--variant {H0, H-A1, H-B2, H-C1, H-D3}`, `--window {R, V, FULL}`, `--slippage {LOW, MEDIUM, HIGH}`, `--stop-trigger {MARK_PRICE, TRADE_PRICE}`. One variant per invocation; mirrors `scripts/phase2e_baseline_backtest.py` artifact set. |
| `scripts/_phase2g_wave1_analysis.py`                                 | Internal analysis script (read-only against existing run dirs) that prints the headline table, deltas vs H0, per-fold breakdown, and §10.3 / §10.4 classification used in the comparison report. Underscore-prefixed to mark its dev-utility role. |
| `docs/00-meta/implementation-reports/2026-04-24_phase-2g_wave1_variant-comparison.md` | Committed comparison markdown. R-window per-variant table, deltas-vs-H0, Phase 2f §11.2 5-rolling-fold breakdown (12m train / 6m test, step 6m, all tests in R) plus a clearly-labeled supplemental 6-half-year appendix (descriptive only), signal-funnel diff, §7.5 frequency-sanity diagnostics, §10.3/§10.4 classification, REJECT-ALL recommendation. |

This file (`2026-04-24_phase-2g_gate-2-review.md`) is the fifth created doc.

### NOT touched

- `docs/12-roadmap/technical-debt-register.md` — operator restriction held.
- `docs/00-meta/implementation-ambiguity-log.md` — no new ambiguity surfaced; GAP-20260424-032's mark-price hook is now wired in code, no log change required.
- Any `data/` or v002 manifest file — datasets unchanged.
- `pyproject.toml` / `uv.lock` — no new dependencies.
- `.claude/`, `.gitignore`, `.gitattributes`, `configs/`, `.env*` — preserved.
- Phase 2e baseline run dir (`data/derived/backtests/phase-2e-baseline/2026-04-20T23-58-39Z/`) — read-only, unchanged.

## 2. Implementation approach

**One config dataclass, threaded through.** A frozen pydantic `V1BreakoutConfig` with five fields (defaults equal the locked baseline) is the single carrier of variant overrides. It nests inside `BacktestConfig.strategy_variant` and is consumed by `StrategySession`, `V1BreakoutStrategy.maybe_entry / .manage`, `evaluate_long_trigger / evaluate_short_trigger`, `detect_setup`, `TradeManagement.on_completed_bar`, and the `run_signal_funnel` diagnostic. Existing call sites pass nothing → all defaults → H0 reproduces bit-for-bit (verified by tests + by re-running H0 on R and confirming the funnel and trade counts match what the engine would have produced on the same window with the prior code).

**Stop-trigger source switch.** `BacktestConfig.stop_trigger_source` is a new `StopTriggerSource` StrEnum (`MARK_PRICE` / `TRADE_PRICE`); default `MARK_PRICE` mirrors the existing live-aligned baseline. `engine._run_symbol`'s stop-hit branch picks the bar stream by enum value; `evaluate_stop_hit`'s parameter type was relaxed to accept either `MarkPriceKline` or `NormalizedKline` (the bodies share `.open / .high / .low / .open_time / .close_time / .symbol`, so the logic is identical). This is the implementation hook for GAP-20260424-032's mark-price-sensitivity report cut. **It is wired but unused in this wave** because no candidate cleared §10.3.

**No structural changes.** No new packages, no refactors outside the variant axes, no removed APIs, no live-trading capability. The strategy's structural rules (15m signal / 1h bias, bar-close confirmation, structural stop formula, exchange-side STOP_MARKET, one-position rule, isolated margin) are unchanged. Sizing pipeline (`risk_fraction`, `max_effective_leverage`, `max_notional_internal`) is unchanged.

**Module-level constants preserved for back-compat imports.** `SETUP_SIZE`, `EMA_FAST`, `EMA_SLOW`, `SLOPE_LOOKBACK`, `TRUE_RANGE_ATR_MULT`, `STAGE_4_MFE_R`, `MIN_1H_BARS_FOR_BIAS`, `MIN_15M_BARS_FOR_SIGNAL` remain as module-level constants. Existing tests that import them still pass; per-variant runs use the active config rather than the constant. This avoids a sweeping rename / churn.

## 3. Proof H0 baseline path is preserved

Multiple lines of evidence:

1. **Unit-level proof.** `tests/unit/strategy/v1_breakout/test_variant_config.py::test_default_config_matches_baseline_constants` asserts `V1BreakoutConfig().setup_size == SETUP_SIZE`, `expansion_atr_mult == TRUE_RANGE_ATR_MULT`, `ema_fast == EMA_FAST`, `ema_slow == EMA_SLOW`, `break_even_r == STAGE_4_MFE_R`. The default `V1BreakoutConfig` IS the baseline by construction.
2. **Session-level proof.** `test_default_session_min_bars_equal_baseline` confirms `session.min_1h_bars_for_bias == EMA_SLOW + SLOPE_LOOKBACK = 203` and `session.min_15m_bars_for_signal == ATR_PERIOD + 1 + SETUP_SIZE + 1 = 30` at default config.
3. **Strategy-level proof.** `test_default_strategy_config_is_baseline` asserts `V1BreakoutStrategy().config` matches every baseline constant.
4. **Regression-suite proof.** Existing 387 tests (Phase 2e baseline) still pass unchanged. Adding optional kwargs with current-value defaults did not break any pre-existing strategy / backtest / engine test. Final test count: **396 passed** (387 baseline + 9 new variant tests).
5. **End-to-end proof on real data.** Re-running H0 on R produces 33 BTC + 33 ETH trades — i.e., the R-window subset of Phase 2e's FULL-window 41 BTC + 47 ETH baseline. The remaining trades fall in the V window 2025-01 → 2026-04, which makes the math add up. Same trade-by-trade signatures, fees, funding, and exit reasons as the Phase 2e baseline for entries that fell within R.

## 4. Test additions

`tests/unit/strategy/v1_breakout/test_variant_config.py` — 9 tests:

- `test_default_config_matches_baseline_constants` — defaults equal locked baseline on all 5 axes.
- `test_default_config_is_frozen_and_strict` — pydantic model is frozen, extra fields rejected.
- `test_ema_fast_must_be_less_than_ema_slow` — `model_post_init` enforces the EMA period ordering.
- `test_default_session_min_bars_equal_baseline` — warmup floors at default config equal `EMA_SLOW + SLOPE_LOOKBACK` and `ATR_PERIOD + 1 + SETUP_SIZE + 1`.
- `test_default_strategy_config_is_baseline` — `V1BreakoutStrategy().config` equals baseline constants.
- `test_HA1_setup_size_10_requires_10_bar_window` — `detect_setup` with `setup_size=10` rejects 8-bar windows and accepts 10-bar windows.
- `test_HB2_expansion_075_admits_smaller_breakouts_than_baseline` — a TR=8 breakout-bar passes `expansion_atr_mult=0.75` (rejected at baseline 1.0).
- `test_HC1_ema_pair_changes_session_alpha` — variant `(20, 100)` reduces the warmup floor from 203 to 103 bars and stores the new periods on the session config.
- `test_HD3_break_even_r_moves_stage_4_trigger` — at MFE = +1.6R, baseline (`break_even_r=1.5`) transitions to STAGE_4_BREAK_EVEN; variant (`break_even_r=2.0`) stays at STAGE_3_RISK_REDUCED.

## 5. Quality-gate output

Run sequence at the pre-commit stop point:

```
$ uv run ruff check .
All checks passed!

$ uv run ruff format --check .
116 files already formatted

$ uv run mypy
Success: no issues found in 49 source files

$ uv run pytest
396 passed in 10.82s
```

Pre-existing 387 tests unchanged; +9 new in `test_variant_config.py`. No regressions, no skips, no warnings.

## 6. Research-window results by variant

Authoritative numbers (entries filtered to R = 2022-01-01 → 2025-01-01 by the engine's `window_start_ms` / `window_end_ms`; full table in `2026-04-24_phase-2g_wave1_variant-comparison.md` §1):

| Variant | BTC trades / WR / expR / PF / netPct / maxDD                          | ETH trades / WR / expR / PF / netPct / maxDD                          |
|---------|-----------------------------------------------------------------------|-----------------------------------------------------------------------|
| H0      | 33 / 30.30% / −0.459 / 0.26 / −3.39% / 3.67%                          | 33 / 21.21% / −0.475 / 0.32 / −3.53% / 4.13%                          |
| H-A1    | 13 / 15.38% / −0.831 / 0.10 / −2.42% / 2.21%                          | 11 / 18.18% / −0.360 / 0.49 / −0.89% / 1.75%                          |
| H-B2    | 69 / 30.43% / −0.326 / 0.43 / −5.07% / 5.53%                          | 57 / 24.56% / −0.440 / 0.35 / −5.65% / 6.53%                          |
| H-C1    | 30 / 26.67% / −0.499 / 0.24 / −3.35% / 3.28%                          | 32 / 15.62% / −0.495 / 0.29 / −3.56% / 3.99%                          |
| H-D3    | 33 / 30.30% / −0.475 / 0.25 / −3.51% / 3.79%                          | 33 / 21.21% / −0.491 / 0.31 / −3.64% / 4.20%                          |

## 7. Fold-level summary — Phase 2f §11.2 approved scheme

**Fold-scheme correction applied per Gate 2 reviewer feedback (2026-04-24).** The earlier draft of this report used six non-overlapping half-year folds; the approved Phase 2f §11.2 scheme is **five rolling folds, 12-month train / 6-month test, stepping 6 months, all tests within R**. Comparison report §3 has been re-built around this scheme. Six half-year folds are retained as a clearly-labeled supplemental descriptive cut in §3.A only — they do not rank or promote variants, and the §10.3 / §10.4 verdict (which is computed on the full R window per §11.3) is unchanged.

Five rolling test folds:

| Fold | Test window         | Notional train window                   |
|-----:|---------------------|-----------------------------------------|
|   F1 | 2022-07 → 2022-12   | 2022-01 → 2022-06 (6m partial — only arrangement that places 5 stepping-6m tests fully inside R) |
|   F2 | 2023-01 → 2023-06   | 2022-01 → 2022-12 (12m)                 |
|   F3 | 2023-07 → 2023-12   | 2022-07 → 2023-06 (12m)                 |
|   F4 | 2024-01 → 2024-06   | 2023-01 → 2023-12 (12m)                 |
|   F5 | 2024-07 → 2024-12   | 2023-07 → 2024-06 (12m)                 |

Phase 2g has no parameter tuning — variants are pre-declared and single-axis — so the train windows are notional. The relevant per-fold metric is the test-window expectancy + trade count.

Cross-fold pattern (variant-comparison report §3 has the full tables):

- **H0**: expectancy negative on every fold of both symbols. F4 (2024H1) is the worst on BTC (−1.03 R) and on ETH (−0.84 R).
- **H-A1**: trade count collapses across folds (BTC test totals 11; ETH 9). One fold (BTC F3) has zero trades. Sample size insufficient for fold-consistency assessment.
- **H-B2**: trades distribute evenly across all 5 folds (BTC: 9 / 13 / 14 / 14 / 10; ETH: 11 / 12 / 17 / 5 / 6), and **expectancy is negative on every fold of every symbol** — quantity rises consistently, quality stays consistently bad.
- **H-C1**: per-fold counts mirror H0 closely; per-fold expectancies sit at H0 or marginally worse.
- **H-D3**: identical fold-level entry/exit counts to H0 (entries unchanged by definition); per-fold expectancies sit at H0 or marginally worse on a small number of folds.

No variant produces a positive expectancy on **any** BTC fold. On ETH, only F1 has positive readings (H0 +0.39 from 8 trades is the most credible; H-A1 +1.94 is from a single trade and is not a sample-size-credible signal). The 5-rolling-folds view confirms the full-R verdict: no consistent fold-level edge across the wave-1 variants.

The supplemental 6-half-year appendix in §3.A surfaces 2022H1 (uncovered by any §11.2 test fold) for completeness — the cleanest sub-period for every variant — but is not used in §10.3 / §10.4 ranking and does not change the disqualification verdict.

## 8. Top 1–2 promotion decision

**Zero variants promoted.** Per Phase 2f Gate 1 plan §10.3 disqualification floor (expR worsens, PF worsens, |maxDD| > 1.5x baseline) and §11.3 no-peeking discipline:

| Variant | Disqualification reason (BTC, the gating symbol per §11.4)                                                                                              |
|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| H-A1    | expR worsens (−0.831 vs −0.459); PF worsens (0.10 vs 0.26).                                                                                              |
| H-B2    | \|maxDD\| 5.53% > 1.5 × 3.67% = 5.505% (ratio 1.505x). §10.3.a passes (Δexp = +0.133, ΔPF = +0.17) but the disqualification veto on |maxDD| takes precedence per §10.3 wording. |
| H-C1    | expR worsens (−0.499 vs −0.459); PF worsens (0.24 vs 0.26).                                                                                              |
| H-D3    | expR worsens (−0.475 vs −0.459); PF worsens (0.25 vs 0.26).                                                                                              |

H-B2 is the closest case (would have qualified under §10.3.a alone), but the maxDD ratio exceeds the 1.5x bar by 0.005x. Per Phase 2f §11.3.5 — "operators cannot tighten or loosen [the thresholds] after seeing results" — the threshold is binding.

## 9. Validation-window results for promoted variants only

**None.** No candidate promoted; per §11.3 V is reserved for the top-1–2 surviving variants. The validation window 2025-01-01 → 2026-03-31 remains untouched in this wave and continues to be the holdout for any future approved wave.

## 10. LOW / HIGH slippage sensitivity for promoted variants

**None.** Per Phase 2f §11.6, slippage sensitivity is required only for variants that clear the base MEDIUM-slippage §10.3 pass. Zero promoted → no sensitivity sweep. The `--slippage {LOW, MEDIUM, HIGH}` runner flag is wired and exercised by the runner CLI but not used in this wave.

## 11. Mark-price sensitivity section for promoted variants

**None.** Per Phase 2g operator brief item 10 + GAP-20260424-032, mark-price stop-trigger sensitivity is required only for promoted variants. Implementation note: the `--stop-trigger {MARK_PRICE, TRADE_PRICE}` switch is fully wired (`BacktestConfig.stop_trigger_source` + engine routing + relaxed `evaluate_stop_hit` typing). It is **available** for any future approved wave that produces a promoted variant; it is **unused** in this wave.

The escalation-gate check from the Phase 2g brief item 10 ("if this requires more than narrow additional implementation, stop and escalate before proceeding") is closed as "narrow" per the original assessment: the existing engine already evaluates stops against `mark_bar`; adding a TRADE_PRICE branch was a ~30-line change in `engine.py` plus a parameter-type relaxation in `stops.py`.

## 12. Final recommendation

**REJECT ALL.** Wave 1 produces no promotion to V. Per Phase 2f §11.3 and §11.3.5, this is the disciplined outcome of the pre-declared rules. No live deployment, no runtime expansion, no capital increase is implied or proposed.

The Phase 2g comparison report's §8 also notes that none of the four single-axis changes converted the baseline's edge problem (expR < 0 on both symbols across regimes). A future operator-approved wave 2 — if proposed — should consider whether the right next move is (a) a different setup-logic axis (H-A2 range-width ceiling, H-A3 drift cap), (b) a bundled variant (e.g., H-B2 paired with a tighter stop-distance band) that requires explicit Phase 2f §9.1 deviation approval, or (c) acknowledging that single-axis variants are unlikely to convert the locked v1 strategy and proposing a different research direction. None of these are recommendations from Phase 2g; they are options the operator may choose among.

## 13. Safety / non-goal checklist

Per Phase 2g operator brief restrictions, all preserved:

| Check | Status |
|---|---|
| No live trading | passed (no exchange code; `BacktestAdapter.FAKE` only) |
| No exchange adapter, REST, or WebSocket | passed |
| No credentials / `.env` / production keys | passed |
| No new data downloads | passed (used existing v002 manifests + datasets) |
| No Binance API calls (authenticated or public) | passed |
| No dataset / manifest changes | passed |
| MCP not enabled | passed (no `.mcp.json`, no Graphify) |
| Phase 4 (risk / state / persistence) not started | passed |
| No threshold tuning | passed (only the four operator-approved single-axis changes) |
| No bundled variants | passed |
| No additional / unapproved variants | passed (exactly H-A1, H-B2, H-C1, H-D3 + H0 control) |
| `docs/12-roadmap/technical-debt-register.md` not edited | passed |
| `docs/00-meta/implementation-ambiguity-log.md` unchanged | passed |
| No new top-level package, no `pyproject.toml` change, no dependency add | passed |
| No `git add` / `git commit` / `git push` before this Gate 2 review | passed (this stop point is pre-commit) |
| Baseline Phase 2e artifacts untouched | passed (read-only access for diagnostics only) |
| Phase 2e v002 manifests untouched | passed |
| H0 reproduces baseline behavior bit-for-bit | passed (tests + R-window subset trade counts) |
| Pytest 387 (baseline) → 396 (with +9 variant tests); 0 regressions | passed |
| Ruff / format / mypy green | passed |

## 14. Stop point

The branch contains all source changes, tests, scripts, run artifacts (under git-ignored `data/`), and committed-by-design markdown reports (variant-comparison.md and this Gate 2 review). No `git add` or `git commit` has been run. Awaiting operator / ChatGPT Gate 2 approval.
