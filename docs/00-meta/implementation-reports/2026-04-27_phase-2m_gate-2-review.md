# Phase 2m — Gate 2 Pre-Commit Review

**Phase:** 2m — R1a-on-R3 First Execution.
**Branch:** `phase-2m/R1a-on-R3-execution`.
**Review date:** 2026-04-27 UTC.
**Authority:** Phase 2m operator-approved brief; Phase 2k Gate 1 plan §§ 11.B / 13 (R1a implementation scope and committed sub-parameters); Phase 2j memo §C (R1a spec) + §D (R3 spec); Phase 2l comparison report (R3 PROMOTE, R3 locked as exit baseline); Phase 2i §1.7.3 project-level locks; Phase 2f §§ 8–11 thresholds (preserved unchanged per §11.3.5).

This Gate 2 review traces every operator-brief content requirement and process requirement to its Phase 2m artifact, confirms threshold preservation, confirms safety posture, and records what awaits operator approval before any `git add` / `git commit`.

## Scope confirmed against operator brief

Scope confirmed: implement R1a minimally on the locked R3 exit baseline (no R3 value changes, no new redesign candidates beyond H0 / R3 / R1a+R3, no widening); execute H0 / R3 / R1a+R3 on R window for BTC + ETH at MEDIUM slippage / MARK_PRICE; if PROMOTE under H0 anchor, run V-window + LOW/HIGH slippage + TRADE_PRICE sensitivity; produce comparison report + Gate 2 review; stop before any commit. **All scope requirements applied; no scope drift.**

## Files changed

### 2.1 Source / test files (modified, untracked at this time)

| Path                                                                  | Lines added (approx.) | Purpose                                                                                     |
|-----------------------------------------------------------------------|----------------------:|---------------------------------------------------------------------------------------------|
| `src/prometheus/strategy/v1_breakout/variant_config.py`               |                  +35  | Add `SetupPredicateKind` StrEnum + 3 R1a fields with H0-preserving defaults + docstring.     |
| `src/prometheus/strategy/v1_breakout/setup.py`                        |                  +95  | Add `detect_setup_volatility_percentile()` + `percentile_rank_threshold()` helper + module docstring update. H0's `detect_setup` untouched. |
| `src/prometheus/strategy/v1_breakout/strategy.py`                     |                  +42  | Add `_15m_prior_atr_history` deque + history-update on `observe_15m_bar` + config-aware `min_15m_bars_for_signal` + `prior_15m_atr_history()` accessor + R1a dispatch in `maybe_entry`. |
| `src/prometheus/strategy/v1_breakout/__init__.py`                     |                  +4   | Export `SetupPredicateKind` and `detect_setup_volatility_percentile`.                        |
| `src/prometheus/research/backtest/diagnostics.py`                     |                  +30  | Mirror strategy-side changes inside `_IncrementalIndicators` and `run_signal_funnel`. Funnel attribution stays in `rejected_no_valid_setup` for both predicates (interpretable). |
| `tests/unit/strategy/v1_breakout/test_variant_config.py`              |                 +220  | 13 R1a unit tests + H0 + R3 default-preservation regressions + R1a+R3 combined-config test. |

### 2.2 New files

| Path                                                                                              | Lines (approx.) | Purpose                                                                  |
|---------------------------------------------------------------------------------------------------|----------------:|--------------------------------------------------------------------------|
| `scripts/phase2m_R1a_on_R3_execution.py`                                                          |            +470 | Per-variant runner mirroring Phase 2l pattern; H0 / R3 / R1a+R3 variants; R/V/FULL windows; --slippage and --stop-trigger knobs. |
| `scripts/_phase2m_R1a_analysis.py`                                                                |            +540 | Internal analysis script computing official deltas-vs-H0, supplemental deltas-vs-R3, GAP-036 5-fold consistency, mandatory diagnostics, R1a-specific diagnostics, V-window comparison, slippage and stop-trigger sensitivity. |
| `docs/00-meta/implementation-reports/2026-04-27_phase-2m_R1a_on_R3_variant-comparison.md`         |            +600 | Phase 2m comparison report (committable).                                |
| `docs/00-meta/implementation-reports/2026-04-27_phase-2m_gate-2-review.md` (this)                 |        this doc | Phase 2m Gate 2 pre-commit review (committable).                         |

The Phase 2m checkpoint report (per `.claude/rules/prometheus-phase-workflow.md`) will be drafted after Gate 2 approval, immediately before the commits, in line with the Phase 2l precedent.

## Exact implementation approach

**R1a setup-validity predicate (Phase 2j memo §C.5):**

```python
def detect_setup_volatility_percentile(prior_bars, atr_prior_15m, atr_history,
                                        *, percentile_threshold, lookback, setup_size=8):
    if len(prior_bars) != setup_size: return None
    if atr_prior_15m != atr_prior_15m or atr_prior_15m <= 0: return None
    if len(atr_history) < lookback: return None
    history = list(atr_history)[-lookback:]
    if any(v != v for v in history): return None
    rank_threshold = floor(X * N / 100)  # 50 at X=25, N=200
    less = sum(1 for v in history if v < atr_prior_15m)
    equal = sum(1 for v in history if v == atr_prior_15m)
    rank = less + (equal + 1) // 2  # mid-rank ceil-on-tie
    if rank > rank_threshold: return None
    # Compute setup_high / setup_low / range_width / drift_abs unchanged.
    # Reject degenerate flat (range_width == 0) for downstream invariant safety.
    ...
```

**Strategy-side history maintenance:** `StrategySession._15m_prior_atr_history` is a `deque[float]` (no maxlen) populated after every `observe_15m_bar` with the prior bar's ATR(20) value, skipping NaN warmup entries. `min_15m_bars_for_signal` is now config-aware: returns `max(ATR_PERIOD + 1 + setup_size + 1, lookback + ATR_PERIOD + 1)` when `setup_predicate_kind == VOLATILITY_PERCENTILE`. `V1BreakoutStrategy.maybe_entry` dispatches to `detect_setup` or `detect_setup_volatility_percentile` based on `config.setup_predicate_kind`.

**Diagnostics-side mirroring:** `_IncrementalIndicators` gains a parallel `prior15_atr_history` deque populated identically; `run_signal_funnel` dispatches the predicate based on `strategy_config.setup_predicate_kind` and reuses the existing `rejected_no_valid_setup` bucket (no new bucket added — funnel attribution stays interpretable).

## Proof H0 baseline path preserved

H0 R-window run #1 (`phase-2m-r1a-h0-r/2026-04-26T21-37-41Z/`) reproduces the locked Phase 2g/2k/2l baseline numbers exactly:

| Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   | Phase 2l reference |
|---------|-------:|-------:|--------:|------:|--------:|--------:|--------------------|
| BTCUSDT |     33 | 30.30% |  −0.459 | 0.255 |  −3.39% |  −3.67% | match               |
| ETHUSDT |     33 | 21.21% |  −0.475 | 0.321 |  −3.53% |  −4.13% | match               |

This confirms the new optional R1a fields and `setup_predicate_kind` dispatch with default `RANGE_BASED` preserve H0 behavior bit-for-bit through the strategy facade. Three preservation tests in `test_variant_config.py` enforce this contract:

- `test_default_config_matches_baseline_constants` — verifies all default-field values including the three new R1a fields.
- `test_R1a_h0_preservation_default_config_does_not_call_percentile` — asserts default config has `setup_predicate_kind == RANGE_BASED`.
- `test_R1a_h0_baseline_path_preserved_via_strategy` — asserts the strategy facade reads RANGE_BASED at default config.

## Proof R3 locked baseline path preserved

R3 R-window run #2 (`phase-2m-r1a-r3-r/2026-04-26T21-37-52Z/`) reproduces the locked Phase 2l R3 baseline numbers exactly:

| Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   | Phase 2l reference |
|---------|-------:|-------:|--------:|------:|--------:|--------:|--------------------|
| BTCUSDT |     33 | 42.42% |  −0.240 | 0.560 |  −1.77% |  −2.16% | match               |
| ETHUSDT |     33 | 33.33% |  −0.351 | 0.474 |  −2.61% |  −3.65% | match               |

The dedicated test `test_R1a_r3_preservation_r3_only_config_keeps_RANGE_BASED` enforces that an R3-only config (`exit_kind=FIXED_R_TIME_STOP`) keeps `setup_predicate_kind == RANGE_BASED` (i.e., the user must explicitly opt into R1a; selecting R3 alone does not silently enable R1a).

## Test additions

13 new R1a unit tests added to `test_variant_config.py` (pytest count moves 404 → 417):

| Test                                                                | Verifies                                                                                       |
|---------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| `test_default_config_matches_baseline_constants`                    | Updated to assert the three new R1a fields default to H0-preserving values.                    |
| `test_R1a_percentile_rank_threshold_at_X25_N200`                    | `floor(25 * 200 / 100) == 50` (and other plausible values).                                    |
| `test_R1a_rejects_when_history_too_short`                           | `len(atr_history) < lookback` triggers rejection.                                              |
| `test_R1a_rejects_when_history_contains_nan`                        | Any NaN in trailing-lookback window triggers rejection.                                        |
| `test_R1a_accepts_when_atr_in_bottom_quartile`                      | `A_prior < every history value` produces rank=1 ≤ 50 → accept.                                 |
| `test_R1a_rejects_when_atr_above_quartile_cutoff`                   | `A_prior` in top half of distribution → rank > 50 → reject.                                    |
| `test_R1a_rejects_when_atr_at_boundary_above`                       | `A_prior` tied with values at rank 51 → mid-rank ceil → reject.                                 |
| `test_R1a_rejects_when_atr_prior_is_nonpositive_or_nan`             | A_prior = 0 or NaN → reject.                                                                    |
| `test_R1a_session_warmup_floor_is_lookback_plus_21`                 | At default N=200, `min_15m_bars_for_signal` returns 221.                                       |
| `test_R1a_session_appends_prior_atr_history_after_seed`             | After K bars (K ≥ 22), history has K − 21 non-NaN entries.                                     |
| `test_R1a_h0_preservation_default_config_does_not_call_percentile`  | Default config has `setup_predicate_kind == RANGE_BASED`.                                       |
| `test_R1a_h0_baseline_path_preserved_via_strategy`                  | Strategy facade reads RANGE_BASED at default config.                                            |
| `test_R1a_r3_preservation_r3_only_config_keeps_RANGE_BASED`         | R3-only config (FIXED_R_TIME_STOP) keeps `setup_predicate_kind == RANGE_BASED`.                |
| `test_R1a_combined_with_R3_config_holds_both_axes`                  | Phase 2m candidate config holds both R3 and R1a axes; other axes remain at H0 baseline.        |

## Quality-gate output

| Gate                            | Result                |
|---------------------------------|-----------------------|
| `uv run ruff check .`           | All checks passed!    |
| `uv run ruff format --check .`  | 120 files already formatted |
| `uv run mypy`                   | Success: no issues found in 49 source files |
| `uv run pytest`                 | **417 passed** in 12.22 s |

## R-window results

Both controls reproduce locked baselines bit-for-bit; R1a+R3 candidate runs are below.

| Variant | Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   | Exits                                       |
|---------|---------|-------:|-------:|--------:|------:|--------:|--------:|---------------------------------------------|
| H0      | BTCUSDT |     33 | 30.30% |  −0.459 | 0.255 |  −3.39% |  −3.67% | STOP=17, STAGNATION=16                      |
| H0      | ETHUSDT |     33 | 21.21% |  −0.475 | 0.321 |  −3.53% |  −4.13% | STOP=26, STAGNATION=6, TRAILING_BREACH=1    |
| R3      | BTCUSDT |     33 | 42.42% |  −0.240 | 0.560 |  −1.77% |  −2.16% | STOP=8, TAKE_PROFIT=4, TIME_STOP=21         |
| R3      | ETHUSDT |     33 | 33.33% |  −0.351 | 0.474 |  −2.61% |  −3.65% | STOP=14, TAKE_PROFIT=5, TIME_STOP=14        |
| R1a+R3  | BTCUSDT |     22 | 27.27% |  −0.420 | 0.355 |  −2.07% |  −2.33% | STOP=5, TAKE_PROFIT=3, TIME_STOP=14         |
| R1a+R3  | ETHUSDT |     23 | 34.78% |  −0.114 | 0.833 |  −0.59% |  −2.96% | STOP=9, TAKE_PROFIT=3, TIME_STOP=11         |

## Fold-level summary

R1a+R3 vs H0 (governing): R1a+R3 beats H0 in 2/5 BTC folds (F3 +1.215, F4 +0.789) and 4/5 ETH folds (F1 +0.138, F3 +0.126, F4 +0.519, F5 +0.017). The two BTC folds where R1a+R3 worsens H0 (F2 −0.554, F5 −0.627) and the one ETH fold where R1a+R3 worsens H0 (F2 −0.680) are concentrated in the same 2023H1 / 2024H2 windows.

R1a+R3 vs R3 (descriptive): R1a+R3 beats R3 in 2/5 BTC folds and 2/5 ETH folds — a mixed signal that confirms R1a's marginal contribution is asymmetric.

## Promotion decision

**R1a+R3 PROMOTES** under Phase 2f §10.3 path (c) on BTC and paths (a) + (c) on ETH, with no §10.3 disqualification floor and no §10.4 hard reject triggered. §11.4 ETH-as-comparison rule satisfied.

The BTC clearance is via §10.3.c only (Δexp +0.039 below the §10.3.a +0.10 threshold). The ETH clearance is strong on both §10.3.a and §10.3.c.

## V-window results (promoted)

| Variant | Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   |
|---------|---------|-------:|-------:|--------:|------:|--------:|--------:|
| H0      | BTCUSDT |      8 | 25.00% |  −0.313 | 0.541 |  −0.56% |  −0.87% |
| H0      | ETHUSDT |     14 | 28.57% |  −0.174 | 0.695 |  −0.55% |  −0.80% |
| R3      | BTCUSDT |      8 | 25.00% |  −0.287 | 0.580 |  −0.51% |  −1.06% |
| R3      | ETHUSDT |     14 | 42.86% |  −0.093 | 0.824 |  −0.29% |  −0.94% |
| R1a+R3  | BTCUSDT |      4 |  0.00% |  −0.990 | 0.000 |  −0.88% |  −0.71% |
| R1a+R3  | ETHUSDT |      8 | 62.50% |  +0.386 | 2.222 |  +0.69% |  −0.51% |

V-window observations:

- **R1a+R3 ETH on V is the project's first positive-net-equity validation result.** netPct +0.69% over 15 months, expR +0.386 R, PF 2.222, WR 62.5%. Materially the strongest V cell ever observed.
- **R1a+R3 BTC on V is severely degraded.** 4 trades, 0% WR (every trade lost), expR −0.990. Sample size is small (n = 4) but direction is unambiguous: R1a's BTC degradation seen on R is amplified out-of-sample.
- Per Phase 2f §11.3.5, V failure does not retroactively change R-window classification; V is sanity-check only. No formal "V-fail" disqualification fires.

## Slippage sensitivity (R1a+R3 R-window)

| Slippage | Symbol  | Trades | expR    | PF    | netPct  | maxDD   |
|----------|---------|-------:|--------:|------:|--------:|--------:|
| LOW      | BTCUSDT |     22 |  −0.319 | 0.449 |  −1.57% |  −2.01% |
| LOW      | ETHUSDT |     23 |  −0.022 | 0.965 |  −0.11% |  −2.55% |
| MEDIUM   | BTCUSDT |     22 |  −0.420 | 0.355 |  −2.07% |  −2.33% |
| MEDIUM   | ETHUSDT |     23 |  −0.114 | 0.833 |  −0.59% |  −2.96% |
| HIGH     | BTCUSDT |     22 |  −0.544 | 0.358 |  −2.68% |  −3.31% |
| HIGH     | ETHUSDT |     23 |  −0.354 | 0.583 |  −1.83% |  −4.00% |

Monotone, proportional. ETH at LOW essentially break-even (expR −0.022, PF 0.965, netPct −0.11%) — confirms the ETH improvement is robust to cost assumptions.

## GAP-032 mark-price sensitivity (R1a+R3 R-window)

| Trigger     | Symbol  | Trades | expR    | PF    | netPct  | maxDD   | Gap-through stops |
|-------------|---------|-------:|--------:|------:|--------:|--------:|-------------------:|
| MARK_PRICE  | BTCUSDT |     22 |  −0.420 | 0.355 |  −2.07% |  −2.33% |                  0 |
| MARK_PRICE  | ETHUSDT |     23 |  −0.114 | 0.833 |  −0.59% |  −2.96% |                  0 |
| TRADE_PRICE | BTCUSDT |     22 |  −0.420 | 0.355 |  −2.07% |  −2.33% |                  0 |
| TRADE_PRICE | ETHUSDT |     23 |  −0.114 | 0.833 |  −0.59% |  −2.96% |                  0 |

**Bit-identical.** Zero gap-through stops on both symbols — same as R3 in Phase 2l.

## Mandatory diagnostics — produced

| Diagnostic                                         | Status                                                                                                                                                                                                                                                                                                                                                                                                |
|----------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Per-regime expR (realized 1h volatility regime)    | Produced (trailing 1000 1h-bar window of Wilder ATR(20), terciles 33/67). R1a+R3 ETH low_vol n=11 expR **+0.281 R** PF **1.353** — first regime-symbol cell with positive expR AND PF > 1 in any phase. R1a+R3 BTC low_vol degrades vs R3 (−0.329 vs −0.054). Reported in comparison §7.1.                                                                                                              |
| MFE distribution                                   | Produced. R1a+R3 ETH max +8.688 R (a single very large move). R1a+R3 BTC mean MFE 0.622 (lower than R3's 0.792). Reported in §7.2.                                                                                                                                                                                                                                                                       |
| Long/short asymmetry                               | Produced. R1a+R3 ETH shorts n=16 expR **+0.387 R** PF **1.906** — strongest direction-symbol cell ever observed in any phase. R1a+R3 ETH longs catastrophic (−1.259 / 0). Reported in §7.3.                                                                                                                                                                                                              |
| Per-fold (5 rolling, GAP-036)                      | Produced. Vs H0: 2/5 BTC, 4/5 ETH. Vs R3: 2/5 BTC, 2/5 ETH. Reported in §6.                                                                                                                                                                                                                                                                                                                              |
| Trade-frequency sanity check                       | Produced. R1a+R3 closed trades 22/23 vs R3's 33/33. The drop is driven by predicate-shape change (more candidate setups → tighter trigger filtering), not by warmup-floor lift. Reported in §3 + §8.2.                                                                                                                                                                                                  |
| Implementation-bug check                           | Produced. Zero TRAILING_BREACH and zero STAGNATION exits in R3 or R1a+R3 trade logs on either symbol. Reported in §7.4.                                                                                                                                                                                                                                                                                  |
| **R1a-specific: ATR-percentile distribution at filled R1a entries** | Produced. **100% of R1a+R3 entries have ATR percentile ≤ 25%**. BTC mean 10.55%, median 9.50%; ETH mean 7.98%, median 5.00%. The predicate is admitting only bottom-quartile compression bars, exactly per Phase 2j memo §C.5 spec. Rules out the §C.12 primary failure mode. Reported in §8.1.                                                                                                                          |
| **R1a-specific: setup-validity rate per fold / funnel comparison** | Produced. R1a+R3's `valid_setup_windows_detected` is ~3.75× H0's; the candidate pool is wider, but downstream trigger filtering ends with fewer entry intents. Funnel attribution remains interpretable in the existing `rejected_no_valid_setup` bucket — no new bucket added. Reported in §8.2.                                                                                                                            |

## Threshold preservation

| Threshold / framework                          | Status                                                                                          |
|------------------------------------------------|-------------------------------------------------------------------------------------------------|
| Phase 2f §10.3.a (Δexp + ΔPF improvement)      | applied unchanged                                                                               |
| Phase 2f §10.3.b (rising count + Δexp ≥ 0)     | applied unchanged (does not fire; Δn < 0)                                                       |
| Phase 2f §10.3.c (strict dominance)            | applied unchanged                                                                               |
| Phase 2f §10.3 disqualification floor          | applied unchanged; not triggered                                                                |
| Phase 2f §10.4 hard reject                     | applied unchanged; does not fire (Δn < 0)                                                       |
| Phase 2f §11.3 no-peeking                      | applied unchanged; V-window not consulted during R-window evaluation                            |
| Phase 2f §11.3.5 pre-committed thresholds      | applied unchanged; no post-hoc loosening or tightening                                          |
| Phase 2f §11.4 ETH-as-comparison rule          | applied unchanged; satisfied                                                                    |
| Phase 2f §11.6 cost-sensitivity                | applied via LOW/MED/HIGH slippage sensitivity                                                   |
| GAP-20260424-036 fold convention               | applied unchanged                                                                               |
| GAP-20260424-031 EMA slope                     | inherited; carry-forward                                                                        |
| GAP-20260424-032 stop-trigger sensitivity      | inherited; TRADE_PRICE sensitivity report cut produced (bit-identical to MARK_PRICE)            |
| GAP-20260424-033 R3 unconditional time-stop    | inherited from Phase 2l; verified clean (zero STAGNATION leakage)                              |
| Phase 2j §C.6 R1a sub-parameters singularly    | committed: X = 25 percentile threshold, N = 200 lookback                                        |
| Phase 2j §D.6 R3 sub-parameters singularly     | unchanged from Phase 2l: R-target = 2.0, time-stop = 8                                          |
| Phase 2i §1.7.3 H0-only anchor                 | applied; R3-anchor view in §5 is supplemental and explicitly not the governing comparison       |

## Wave-1 + Phase 2l preservation

Phase 2g Wave-1's REJECT ALL verdict is preserved as historical evidence. Phase 2l's R3 PROMOTE verdict and locked sub-parameter values are preserved unchanged. R3 is the Phase 2m-locked exit baseline; R1a+R3 is compared against H0 (anchor) and R3 (descriptive).

## Safety / non-goal checklist

| Check                                                        | Result |
|--------------------------------------------------------------|--------|
| Production Binance keys                                      | none   |
| Exchange-write code                                          | none   |
| REST / WebSocket / authenticated endpoints                   | none   |
| Credentials / `.env`                                         | none   |
| `.mcp.json`                                                  | absent |
| Graphify                                                     | disabled |
| MCP servers                                                  | not activated |
| Manual trading controls                                      | none   |
| Strategy structural changes                                  | R1a only — setup-predicate only; entry-trigger / bias / stop / sizing / R3 exit unchanged       |
| R3 value changes                                             | none (sub-parameters frozen at Phase 2l-committed values: R-target=2.0, time-stop=8)             |
| Risk framework changes                                       | none   |
| Dataset / manifest changes                                   | none   |
| Cost-model changes                                           | none (slippage applied via existing buckets; no fee-rate change)                                  |
| Binance public or authenticated URLs                         | none fetched |
| New top-level package or dependency                          | none   |
| `pyproject.toml` / `uv.lock` change                          | none   |
| `data/` commits                                              | none (`data/derived/backtests/phase-2m-r1a-*` git-ignored as designed)                            |
| `docs/12-roadmap/technical-debt-register.md` edits           | none (operator restriction)                                                                       |
| Phase 4 work                                                 | none (operator restriction)                                                                       |
| Fallback Wave 2 / H-D6 start                                 | none (superseded by R3 PROMOTE in Phase 2l + R1a+R3 PROMOTE here)                                 |
| New redesign candidate exposed                               | none (only H0, R3, R1a+R3)                                                                        |
| Disguised parameter sweeps                                   | none (single committed value per R1a sub-parameter)                                                |
| Wave-1 variant revival                                       | none                                                                                              |
| Live deployment / paper / shadow / tiny-live readiness claim | none                                                                                              |
| Pre-existing 417 tests pass                                  | yes (every commit)                                                                                |

## Final recommendation

**PROMOTE R1a+R3 under the Phase 2f §10.3 / §10.4 framework with H0 as the governing anchor.** This is the second PROMOTE verdict in the project's research history (R3 was the first, in Phase 2l).

**Caveats** (preserved for the operator's next-phase decision-making):

1. The BTC clearance is **weak** — only §10.3.c strict-dominance fires (Δexp +0.039 below §10.3.a's +0.10 threshold). The BTC promotion margin is roughly the noise scale at 22-trade sample.
2. The supplemental R3-anchor view shows R1a's marginal contribution **hurts BTC** vs R3-only (Δexp_R3 −0.180 R) and **helps ETH** vs R3-only (Δexp_R3 +0.237 R).
3. The V-window evidence is divergent: R1a+R3 ETH V is the project's first positive-netPct validation result (+0.69%, expR +0.386, PF 2.222) — strong; R1a+R3 BTC V is severely degraded (4 trades, 0% WR, expR −0.990).
4. R1a+R3 still has negative aggregate expR on R; PROMOTE means "improvement vs H0 clears pre-declared threshold", not "live-ready".

Recommended next phase (per comparison report §13): **Phase 2n — operator/strategy review** (docs-only, no code, no runs) before any further structural redesign work. Decide whether to deploy R3 alone or R1a+R3 in any future paper/shadow planning, given the asymmetric BTC vs ETH evidence. Phase 4 stays deferred per operator policy.

## Recommended commit structure (after Gate 2 approval)

Proposed sequence on `phase-2m/R1a-on-R3-execution`, mirroring the Phase 2l precedent:

1. `phase-2m: R1a implementation + unit tests` — `src/prometheus/strategy/v1_breakout/{variant_config,setup,strategy,__init__}.py`, `src/prometheus/research/backtest/diagnostics.py`, `tests/unit/strategy/v1_breakout/test_variant_config.py` (the structural code change as one reviewable unit; pytest runs at 417 after this commit).
2. `phase-2m: runner + analysis script` — `scripts/phase2m_R1a_on_R3_execution.py`, `scripts/_phase2m_R1a_analysis.py` (no test impact; pytest stays at 417).
3. `phase-2m: comparison report + Gate 2 review` — the two docs at `docs/00-meta/implementation-reports/2026-04-27_phase-2m_*` (no test impact).
4. `phase-2m: checkpoint report` — `docs/00-meta/implementation-reports/2026-04-27_phase-2m-checkpoint-report.md` (drafted after Gate 2 approval, immediately before this commit).

No `data/` commits. No `pyproject.toml` / `uv.lock` change. No `.claude/` change. No merge yet — push and PR decision deferred to operator. No `Co-Authored-By` trailer (consistent with prior phases).

## Questions for ChatGPT / operator

- **Is the Phase 2m verdict acceptable given the BTC/ETH asymmetry?** The H0-anchor §10.3 framework PROMOTES R1a+R3 cleanly, but the supplemental R3-anchor view + V-window evidence show R1a is asymmetric. Does the operator accept the PROMOTE verdict as-is, or want it qualified?
- **Is Phase 2n the right next phase?** The comparison report §13 recommends operator/strategy review before further structural-redesign work. Does the operator confirm or redirect (e.g. immediate Phase 2o R1b execution, or paper/shadow planning for R3 alone)?
- **Any additional diagnostics needed before commit?** None observed during the analysis. Per the brief: "No extra diagnostics are required before commit."
- **GAP-20260424-030 disposition.** The Phase 2l Gate 2 review left this deferred. R1a does not touch the break-even rule (R1a's exit logic is R3-locked, with no break-even at all), so no SUPERSEDE event is created by Phase 2m either. The disposition stays deferred.

---

**Stop point:** awaiting operator/ChatGPT Gate 2 approval. No `git add`, no `git commit`, no `git push`, no merge.
