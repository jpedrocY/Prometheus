# Phase 3c — F1 Execution-Planning Memo

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; **no post-hoc loosening per §11.3.5**); Phase 2i §1.7.3 project-level locks (H0 anchor for V1 breakout family; BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets); Phase 2j §C.6 / §D.6 / §11.3.5 single-sub-parameter commitment discipline; Phase 2k Gate 1 plan (per-variant runner pattern; quality-gate discipline); Phase 2l comparison report (Phase 2k pattern in execution); Phase 2t Gate 1 planning memo (R2 GO recommendation); Phase 2v Gate 1 execution plan + Gate 2 review (R2 run inventory + Gate 2 amendments); Phase 2w R2 variant-comparison report (R2 framework FAILED — §11.6 cost-sensitivity blocks; M1 + M3 PASS; M2 FAIL); Phase 2x family-review memo (V1 breakout family at useful ceiling); Phase 2y slippage / cost-policy review (§11.6 = 8 bps HIGH preserved); Phase 3a discovery memo §4.1 / §6 (F1 ranked rank-1); **Phase 3b F1 spec memo §§ 1–15 (binding spec, anchor for this Phase 3c plan)**; `docs/03-strategy-research/v1-breakout-strategy-spec.md` (V1 conventions); `docs/05-backtesting-validation/backtesting-principles.md`; `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`; `docs/05-backtesting-validation/cost-modeling.md`; `docs/04-data/data-requirements.md`; `docs/04-data/dataset-versioning.md`; `src/prometheus/research/backtest/config.py:55-87` (canonical cost model and config shape; `BacktestAdapter.FAKE` only in Phase 3).

**Phase:** 3c — Docs-only **execution-planning memo** for any potential Phase 3d execution of F1 (mean-reversion-after-overextension). Phase 2k/2t/2v-style: define implementation surface, dataset/feature plan, exact run inventory, promotion/failure framework, mandatory diagnostics, mechanism-validation computation, quality-gate plan, implementation-risk checklist, GO/NO-GO recommendation for Phase 3d.

**Branch:** `phase-3c/f1-execution-planning`. **Memo date:** 2026-04-27 UTC.

**Status:** Plan drafted. **No code change. No tests. No scripts. No backtest. No variant created. No feature dataset created. No parameter tuned. No threshold changed. No project-level lock changed. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / credentials / `data/` work.** R3 remains V1 baseline-of-record. H0 remains V1 framework anchor. R1a / R1b-narrow / R2 remain retained research evidence. **Phase 3b F1 spec is the binding anchor; Phase 3c does NOT modify it.** Recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

## 1. Plain-English explanation of what Phase 3c is planning

Phase 3c is **execution-planning-only**, not implementation and not execution. It is the natural successor to Phase 3b, which produced the binding F1 specification. Phase 3c's job is to translate that spec into an execution plan that any potential downstream Phase 3d implementation phase could follow without further specification work.

What Phase 3c is asking:

> Given Phase 3b's binding F1 specification, **can a clean Phase 3d execution plan be defined that (a) does not require any spec change, (b) pre-commits the run inventory before any implementation begins, (c) preserves the §11.3.5 single-spec discipline, (d) cleanly distinguishes F1's first-execution gate from the V1-family §10.3 framework, and (e) carries no implementation, threshold, or project-lock change?**

What Phase 3c is **not** asking:

- Not asking to **implement** F1. Phase 3c is docs-only; Phase 3d would be the first phase to authorize source code, tests, scripts, or feature datasets.
- Not asking to **execute** F1. Phase 3d-execution would be a separately-authorized phase after Phase 3d-implementation completes its quality gates.
- Not asking to **revise** the Phase 3b spec. Per §3 below, Phase 3c is bound by Phase 3b verbatim.
- Not asking to **revise any threshold** or lift any §1.7.3 lock.
- Not asking to begin paper/shadow, Phase 4, live-readiness, or deployment work.

The output of Phase 3c is a single execution-planning memo with run-inventory pre-commitment, implementation-surface architecture, dataset/feature plan, mechanism-validation computation specifications, mandatory-diagnostics plan, quality-gate discipline, implementation-risk checklist, and a GO/NO-GO recommendation for downstream Phase 3d.

---

## 2. Phase 3b spec restatement

This section restates the Phase 3b binding spec verbatim from `docs/00-meta/implementation-reports/2026-04-27_phase-3b_F1_mean-reversion-spec-memo.md` §4. Any deviation in Phase 3d implementation from these statements is a spec violation.

### 2.1 Overextension definition (Phase 3b §4.1)

`cumulative_displacement_8bar(B) = close(B) − close(B−8)`. F1 fires an overextension event at bar B's close iff:

```
| cumulative_displacement_8bar(B) |  >  1.75 × ATR(20)(B)
```

with the **direction** of overextension equal to `sign(cumulative_displacement_8bar(B))`. Positive sign = upward overextension → candidate **short** entry. Negative sign = downward overextension → candidate **long** entry.

### 2.2 Mean / reference level (Phase 3b §4.2)

`mean_reference(B) = SMA(8)(B) = (1/8) × Σ_{i=0..7} close(B−i)`. Simple moving average over the same 8 completed 15m bars used by the overextension predicate.

### 2.3 Entry rule (Phase 3b §4.3)

**Market entry at the open of the bar immediately following the overextension-detection bar B.** Entry bar = `B+1`; entry price = `open(B+1)`. **No confirmation candle required.**

### 2.4 Protective stop (Phase 3b §4.4)

- **Long entries:** `initial_stop = lowest_low([B−7, ..., B]) − 0.10 × ATR(20)(B)`.
- **Short entries:** `initial_stop = highest_high([B−7, ..., B]) + 0.10 × ATR(20)(B)`.

Exchange-side `STOP_MARKET` with `closePosition=true`, `workingType=MARK_PRICE`, `priceProtect=TRUE` (identical to V1 protective-stop spec). **Stop is never moved intra-trade** — no trailing, no break-even shift, no widening, no narrowing.

### 2.5 Target exit (Phase 3b §4.5)

Profit target = `mean_reference(B) = SMA(8)(B)`, **frozen at signal-time bar B's close**. Exit triggers when, on a completed 15m bar `t > B`:

- For longs: `close(t) ≥ frozen_mean_reference`.
- For shorts: `close(t) ≤ frozen_mean_reference`.

Exit fill at `open(t+1)`.

### 2.6 Time stop (Phase 3b §4.6)

**Unconditional time-stop at 8 completed 15m bars from entry-fill.** If at the close of bar `B+1+8 = B+9` the trade has not exited via target (§2.5) or stop (§2.4), exit at market at `open(B+10)`.

### 2.7 Cooldown / re-entry (Phase 3b §4.7)

After exit (any reason — target, stop, or time-stop), no new same-direction F1 entry on the same symbol may be initiated until the cumulative displacement predicate (§2.1) re-forms in the same direction **after** at least one completed 15m bar where `| cumulative_displacement_8bar(t) | ≤ 1.75 × ATR(20)(t)` (the overextension state has unwound).

### 2.8 No explicit regime filter (Phase 3b §4.8)

F1 fires whenever the overextension predicate (§2.1) and the stop-distance admissibility rule (§2.9) are simultaneously satisfied, **regardless of prevailing 1h trend bias or volatility regime**. Per-regime decomposition is a §8.3 diagnostic, not an entry gate.

### 2.9 Stop-distance admissibility (Phase 3b §4.9)

Reject the candidate entry at signal-time bar B if the computed stop distance falls outside the band:

```
stop_distance ∈ [0.60, 1.80] × ATR(20)(B)
```

where `stop_distance = |entry_price_estimate(open(B+1) ≈ close(B)) − initial_stop|`. (The de-slipped raw next-bar-open is the reference per Phase 2u §E.3 / Phase 2w P.14 convention.) Rejected entries do not place an order; the cooldown rule (§2.7) does not apply because no trade was opened.

---

## 3. Explicit statement that Phase 3c does not alter the Phase 3b spec

**Phase 3c does not modify any rule in §2 above.** The 9 axes are committed verbatim from Phase 3b §4. Phase 3c's role is to plan the implementation and execution of the Phase 3b spec; it has no authority to revise the spec.

Specifically forbidden in Phase 3c:

- Adjusting the overextension threshold (1.75 × ATR(20)) — even if Phase 3c reasoning suggested a different value would be empirically better, that is not Phase 3c's authority.
- Adjusting the 8-bar window length (used for displacement, mean reference, and time-stop horizon).
- Adjusting the [0.60, 1.80] × ATR stop-distance admissibility band.
- Adjusting the 0.10 × ATR stop buffer.
- Introducing a regime filter to "improve" expected results.
- Introducing a confirmation candle requirement to "reduce false signals".
- Adjusting the cooldown rule to permit faster re-entry.
- Switching the target from frozen SMA(8) to a rolling SMA or other reference.
- Switching the entry from market-on-next-bar-open to limit-at-pullback (which Phase 2v Gate 2 designated diagnostic-only for R2; non-applicable for F1).

If during Phase 3c any of these adjustments appears empirically better, the disciplined response is: **document the observation, but do not change the spec.** Such observations become potential evidence for any future F1-prime spec written in a separately-authorized phase, not Phase 3c modifications.

This rule preserves the §11.3.5 binding discipline that distinguishes specification (Phase 3b) from execution-planning (Phase 3c) from execution (Phase 3d).

---

## 4. Implementation surface plan for a future Phase 3d

Phase 3d would be the first phase to authorize source code, tests, scripts, and feature datasets. Phase 3c specifies the **implementation surface** Phase 3d would touch; Phase 3d makes final architectural decisions within these constraints.

### 4.1 New strategy module path

Recommended: `src/prometheus/strategy/mean_reversion_overextension/` — matches the Phase 3b §3.1 family signal name `mean_reversion_overextension`. Phase 3d may select a different but functionally-equivalent path (e.g., `f1_mean_reversion/`).

The new module **must not modify** `src/prometheus/strategy/v1_breakout/` or any of its submodules. F1 is a parallel family, not a V1 variant.

### 4.2 Expected config model

A Pydantic config model for F1, parallel to `V1BreakoutConfig`. Recommended name: `MeanReversionConfig`. Fields would lock the Phase 3b §4 axes:

- `overextension_window_bars: int = 8` — locked at 8.
- `overextension_threshold_atr_multiple: float = 1.75` — locked at 1.75.
- `mean_reference_window_bars: int = 8` — locked at 8.
- `stop_buffer_atr_multiple: float = 0.10` — locked at 0.10.
- `time_stop_bars: int = 8` — locked at 8.
- `stop_distance_min_atr: float = 0.60` — locked at 0.60.
- `stop_distance_max_atr: float = 1.80` — locked at 1.80.

All fields would be Pydantic-frozen; Phase 3d would not introduce parameter sweep mechanics. Alternative parameter values are not part of the F1 spec and must not appear as defaults, kwargs, or config-override paths.

### 4.3 Expected strategy class

Recommended: `MeanReversionStrategy`, parallel to `V1BreakoutStrategy`. Public surface:

- `evaluate_entry_signal(bar_b: NormalizedKline, history: BarHistory, config: MeanReversionConfig) -> MeanReversionSignal | None` — overextension detection at bar B's close.
- `compute_initial_stop(signal: MeanReversionSignal, history: BarHistory, config: MeanReversionConfig) -> float` — structural stop computation.
- `compute_target_reference(signal: MeanReversionSignal, config: MeanReversionConfig) -> float` — frozen SMA(8) target.
- `evaluate_target_exit(bar_t: NormalizedKline, frozen_target: float, direction: Direction) -> bool` — completed-bar close vs frozen target check.
- `evaluate_time_stop(bars_since_fill: int, config: MeanReversionConfig) -> bool` — time-stop check (returns True at bars_since_fill == 8).
- `evaluate_cooldown(latest_bar: NormalizedKline, history: BarHistory, last_exit_direction: Direction, config: MeanReversionConfig) -> bool` — re-entry permission check (per §2.7 unwind condition).

Class architecture parallels `V1BreakoutStrategy` but does not share state, methods, or imports.

### 4.4 Expected feature computation

The `mean_reversion_overextension/` module would expose pure functions (or a small features class) computing:

- `cumulative_displacement_8bar(close: Series, b_index: int) -> float` — `close[b_index] − close[b_index − 8]`.
- `sma_8_close(close: Series, b_index: int) -> float` — `mean(close[b_index − 7 : b_index + 1])`.
- `overextension_predicate(close: Series, atr20: Series, b_index: int, threshold: float = 1.75) -> bool` — `abs(cumulative_displacement_8bar) > threshold * atr20[b_index]`.

These functions would also be the basis for the §5 feature dataset. They use only completed-bar values; no lookahead.

### 4.5 Expected engine dispatch changes

`src/prometheus/research/backtest/engine.py` requires a strategy-family dispatch addition. Two acceptable patterns:

**Pattern A (recommended) — new top-level family enum:**

```python
class StrategyFamily(StrEnum):
    V1_BREAKOUT = "V1_BREAKOUT"
    MEAN_REVERSION_OVEREXTENSION = "MEAN_REVERSION_OVEREXTENSION"
```

`BacktestConfig.strategy_variant` becomes a discriminated union: `V1BreakoutConfig | MeanReversionConfig` keyed by `StrategyFamily`. Engine `_run_symbol` dispatches on family at the per-bar evaluation loop entry point.

**Pattern B (alternative) — separate variant fields with mutual-exclusion validation:**

`BacktestConfig` gains `mean_reversion_variant: MeanReversionConfig | None = None` field; the `_check` validator enforces exactly one of `strategy_variant` or `mean_reversion_variant` is non-None. Engine dispatches on whichever is set.

Phase 3d implementation chooses; Pattern A is recommended for clarity. Pattern A also leaves room for future families (F2 / F6 / etc.) without further architectural change.

`BacktestAdapter.FAKE` stays the only adapter (Phase 3 restriction per `config.py:25-27`).

### 4.6 Expected report / metrics changes

`src/prometheus/research/backtest/report.py` requires:

- `compute_summary_metrics` extended to include F1-specific exit-reason counters: `target_exits` (F1 TARGET reason from §2.5), `stop_exits` (existing), `time_stop_exits` (existing R3 reason; reused for F1).
- `target_exits` is a new exit-reason category; `ExitReason` enum (`src/prometheus/strategy/types.py`) gains `TARGET = "TARGET"` (F1-specific; not used by V1 breakout — V1 uses `TAKE_PROFIT` for R3's fixed-R take-profit, which is a different mechanism).
- The new exit-reason `TARGET` does not affect existing V1 breakout behavior. V1 R3 continues to emit `TAKE_PROFIT` (R3 fixed-R) and `TIME_STOP` (R3 unconditional). H0 continues to emit `STOP`, `TRAILING_BREACH`, `STAGNATION`. F1 emits `STOP`, `TARGET`, `TIME_STOP`.

`src/prometheus/research/backtest/trade_log.py` requires F1-specific TradeRecord fields for diagnostic purposes:

- `overextension_magnitude_at_signal: float | None` — `cumulative_displacement_8bar(B) / ATR(20)(B)`.
- `frozen_target_value: float | None` — SMA(8)(B) at signal time.
- `entry_to_target_distance_atr: float | None` — `|entry_price − frozen_target_value| / ATR(20)(B)`.
- `cooldown_blocked_signal_count: int` — incremented on cooldown-blocked overextension events.
- `stop_distance_at_signal_atr: float | None` — `stop_distance / ATR(20)(B)` at signal-time evaluation.

V1 breakout TradeRecord rows would have these fields as `None` (the engine's existing zero-init / None-init pattern from Phase 2w-A applies).

### 4.7 Expected diagnostics additions

`src/prometheus/research/backtest/diagnostics.py` extension:

- F1-specific `MeanReversionFunnelCounts` analogous to Phase 2w `SignalFunnelCounts.r2_*` fields:
  - `overextension_events_detected: int`
  - `overextension_events_filled: int`
  - `overextension_events_rejected_stop_distance: int`
  - `overextension_events_blocked_cooldown: int`
- F1 accounting identity property: `f1_accounting_identity_holds: bool` returning `events_detected == events_filled + events_rejected_stop_distance + events_blocked_cooldown` for completeness.

### 4.8 No V1 breakout behavior changes

Phase 3d implementation **must not modify**:

- `src/prometheus/strategy/v1_breakout/` (any submodule).
- V1's `EntryKind` enum (Phase 2w-A R2 dispatch).
- V1's `ExitKind` enum (Phase 2l R3 dispatch).
- V1's `V1BreakoutConfig` Pydantic model.
- V1's `V1BreakoutStrategy` class.
- V1's `R2_VALIDITY_WINDOW_BARS` constant.
- V1's `entry_lifecycle.py` PendingCandidate logic.
- V1's `management.py` exit-machinery.
- V1's `strategy.py` evaluation entry point.

H0 / R3 / R1a / R1b-narrow / R2 must reproduce bit-for-bit on R-window after Phase 3d implementation per §10 baseline-preservation discipline.

---

## 5. Dataset / feature plan

### 5.1 v002 raw data sufficiency

Confirmed sufficient. F1's raw inputs are:

- BTCUSDT 15m kline (close, high, low, volume) — present in v002.
- ETHUSDT 15m kline — present in v002.
- 15m ATR(20) — derivable from v002 kline data via existing engine ATR primitive.
- Funding-rate history — present in v002 (used unchanged for cost realism per cost-modeling.md).
- Mark-price kline — present in v002 (used unchanged for stop-trigger evaluation per `config.py:38-49`).
- Exchange metadata snapshot — present in v002 (used unchanged).

No new raw data ingestion required. No external data sources required.

### 5.2 Derived feature dataset names

Per `dataset-versioning.md` §"Recommended naming pattern" (`<dataset_name>__vNNN`):

- `mean_reversion_features_btcusdt_15m__v001`
- `mean_reversion_features_ethusdt_15m__v001`

Phase 3d implementation creates these as new versioned feature datasets. Schema-wise additive change vs `usdm_klines_<symbol>_15m__v001` is breaking (new columns); per `dataset-versioning.md` §"Required rule", the new feature dataset is its own versioned identity.

### 5.3 Manifest requirements

Per `dataset-versioning.md` §"Minimum required manifest fields":

```yaml
dataset_name: mean_reversion_features_btcusdt_15m
dataset_version: v001
dataset_category: derived
creation_timestamp: <UTC ms at generation>
canonical_timezone: UTC
canonical_timestamp_format: Unix milliseconds
symbol: BTCUSDT
interval: 15m
source_endpoints:
  - usdm_klines_btcusdt_15m__v001
  - <atr_features dataset version if separated; or computed inline from klines>
schema_version: 1
transformation_pipeline_version: phase-3c-spec-anchored
partitioning_rules: by symbol + 15m open_time
primary_key: symbol + interval + open_time
generator_identity: phase-3d-implementation
notes: |
  Derived features for F1 mean-reversion-after-overextension strategy
  per Phase 3b spec memo §4 and Phase 3c execution-planning memo §5.
predecessor_version: null
publication_state: draft
```

`publication_state: draft` until Phase 3d implementation publishes the dataset for use in any reported run; transition to `published` is a Phase 3d milestone.

### 5.4 Schema fields

Required columns for `mean_reversion_features_<symbol>_15m__v001`:

| Column | Type | Source / computation |
|--------|------|----------------------|
| `symbol` | str | constant per dataset (BTCUSDT or ETHUSDT) |
| `interval` | str | constant `"15m"` |
| `open_time` | int (UTC Unix ms) | inherited from source kline; canonical bar key |
| `close_time` | int (UTC Unix ms) | inherited from source kline |
| `close` | float | inherited from source kline |
| `atr_20_15m` | float | Wilder ATR(20) on 15m completed bars |
| `cumulative_displacement_8bar` | float | `close − close.shift(8)`; null for first 8 bars |
| `sma_8_close` | float | rolling mean of close over 8 bars; null for first 7 bars |
| `overextension_flag` | bool | `abs(cumulative_displacement_8bar) > 1.75 × atr_20_15m` |
| `overextension_direction` | int (`+1`, `−1`, `0`) | `sign(cumulative_displacement_8bar)` if `overextension_flag` else `0` |

Bar identity per `data-requirements.md` §"Core Data Principles" #3: `symbol + interval + open_time`.

### 5.5 No v003 raw-data bump

Confirmed not required. v002 raw klines, v002 mark-price, v002 funding, v002 exchange metadata all suffice for Phase 3d execution.

A v003 raw-data bump would be a separate operator-policy decision (e.g., for ETH-microstructure depth/spread features per Phase 2y §5.1.3 / §5.1.8); not in Phase 3 scope.

---

## 6. Future Phase 3d run inventory

Phase 3c **pre-commits** the run inventory before any Phase 3d implementation. Run-set expansion mid-execution is forbidden (would violate §11.3.5 single-spec discipline). All runs use Phase 2e v002 datasets, sizing equity 10,000 USDT, risk 0.25%, leverage cap 2×, internal notional cap 100,000 USDT, taker fee rate 0.0005, `BacktestAdapter.FAKE` only.

### 6.1 F1 governing runs

| # | Variant | Window | Slippage | Stop trigger | Purpose |
|---|---------|--------|----------|--------------|---------|
| 1 | F1 | R | MEDIUM | MARK_PRICE | **Governing first F1 run.** §10.3-equivalent + §7 first-execution gate evaluation. |
| 2 | F1 | R | LOW | MARK_PRICE | §11.6 cost-sensitivity sweep — LOW tier. |
| 3 | F1 | R | HIGH | MARK_PRICE | **§11.6 HIGH-slippage cost-sensitivity gate.** Per Phase 2y closeout, 8 bps per side. |
| 4 | F1 | R | MEDIUM | TRADE_PRICE | Stop-trigger sensitivity (GAP-20260424-032). Bit-identical to MARK_PRICE expected if zero gap-throughs. |

Runs 1–4 are **mandatory** for the first-execution gate evaluation. Run 1 is the governing run; runs 2–4 are sensitivity runs.

### 6.2 F1 V-window run (conditional)

| # | Variant | Window | Slippage | Stop trigger | Purpose |
|---|---------|--------|----------|--------------|---------|
| 5 | F1 | V | MEDIUM | MARK_PRICE | **Conditional.** Run only if F1 R-window first-execution gate **passes** (§7). Per Phase 2f §11.3 no-peeking discipline; V is direction-of-improvement confirmation only. |

If the §7 first-execution gate **fails** at the R-window MED-slip evaluation, run 5 is **not** executed (§11.3 V is not consulted; family verdict ends at R).

### 6.3 H0 V1 breakout reference re-runs (descriptive only)

| # | Variant | Window | Slippage | Stop trigger | Purpose |
|---|---------|--------|----------|--------------|---------|
| 6 | H0 | R | MEDIUM | MARK_PRICE | H0 R-window control re-run on the engine version with F1 dispatch added. **Bit-for-bit reproduction of Phase 2e/2l/2w baselines required** per §10.4 baseline-preservation discipline. |
| 7 | H0 | V | MEDIUM | MARK_PRICE | H0 V-window control re-run. Bit-for-bit reproduction of Phase 2s/2w V-window baselines required. |

H0 is **descriptive cross-family reference only**, not F1's governing anchor (per §7.4 below). H0 deltas are reported alongside F1 absolute results without governing the F1 verdict.

### 6.4 R3 V1 breakout reference re-runs (descriptive only)

| # | Variant | Window | Slippage | Stop trigger | Purpose |
|---|---------|--------|----------|--------------|---------|
| 8 | R3 | R | MEDIUM | MARK_PRICE | R3 R-window control re-run on the engine version with F1 dispatch added. **Bit-for-bit reproduction of Phase 2l/2m/2s/2w R3 baseline required.** |
| 9 | R3 | V | MEDIUM | MARK_PRICE | R3 V-window control re-run. Bit-for-bit reproduction of Phase 2s/2w R3 V-window required. |

R3 is **descriptive cross-family reference only**, not F1's governing baseline (per §7.4 below). R3 deltas are reported descriptively.

### 6.5 Run inventory total and exclusions

**9 runs total** if F1 R-window gate passes (runs 1–9). **8 runs total** if F1 R-window gate fails (runs 1–4, 6–9; run 5 V-window omitted).

**Explicitly excluded** from the run inventory:

- F1 R LOW TRADE_PRICE — diagnostic redundancy not justified by §11.6 gate definition.
- F1 R HIGH TRADE_PRICE — same.
- F1 V LOW / V HIGH / V TRADE_PRICE — V is no-peeking direction-of-improvement only at MED.
- Any F1 variant with parameter overrides (different window, different threshold, different target reference). Forbidden per §3.
- Any V1 breakout variant beyond H0 / R3. R1a / R1b-narrow / R2 are research-evidence-only per Phase 2p §D / Phase 2s §13 / Phase 2w §16.3 and not Phase 3d-relevant.
- Any post-execution run-set expansion. Phase 3d execution must use exactly the runs above; mid-execution additions are forbidden.

---

## 7. Promotion / failure framework

### 7.1 Two distinct frameworks

Phase 3 introduces a clean separation:

- **Phase 2 §10.3 framework** = V1 breakout-family **variant-vs-anchor** improvement framework. Designed for variant-vs-H0 deltas with thresholds calibrated for V1-internal comparison. Applied to R3, R1a, R1b-narrow, R2 in Phase 2.
- **Phase 3 F1 first-execution gate** = new-family **first-execution self-anchored** framework. Designed for F1-vs-zero-strategy-null absolute-edge evaluation with descriptive cross-family references to H0 and R3. Defined here in §7.

The two frameworks are **mutually exclusive** for any given candidate. F1 is a new family; F1 is evaluated under Phase 3 framework, not Phase 2 framework. Future F1-prime variants (if any) would be evaluated under a Phase-3-derived variant-vs-F1 framework, not Phase 2 §10.3.

### 7.2 F1 first-execution gate definition

Per Phase 3b §12 / §14.1, F1's first-execution gate is the conjunction of five conditions evaluated on the run-1 governing run (F1 R MED MARK):

**Condition (i) — Absolute BTC edge.** F1 must produce **positive aggregate net-of-cost expR on BTCUSDT** R-window:

```
expR(F1, BTCUSDT, R, MED, MARK) > 0
```

**Condition (ii) — M1 BTC mechanism.** Per Phase 3b §9.1 + §9.2 of this memo:

```
mean post-entry counter-displacement at 8-bar horizon (BTCUSDT)  ≥  +0.10 R per trade
AND
fraction of fired entries with non-negative 8-bar counter-displacement (BTCUSDT)  ≥  50%
```

**Condition (iii) — ETH non-catastrophic per §11.4.** ETH must not catastrophically fail. Adapted §11.4 logic for F1:

```
expR(F1, ETHUSDT, R, MED, MARK)  >  −0.50
AND
PF(F1, ETHUSDT, R, MED, MARK)   >  0.30
```

(I.e., ETH satisfies §10.4-style absolute floor even though ETH is not the primary symbol per §1.7.3.)

**Condition (iv) — §11.6 HIGH-slippage cost-sensitivity gate.** F1 must not §10.4-fail at HIGH slippage on either symbol:

```
expR(F1, BTCUSDT, R, HIGH, MARK)  >  −0.50  AND  PF(F1, BTCUSDT, R, HIGH, MARK)  >  0.30
AND
expR(F1, ETHUSDT, R, HIGH, MARK)  >  −0.50  AND  PF(F1, ETHUSDT, R, HIGH, MARK)  >  0.30
```

This is a **softer §11.6 gate than the V1-internal gate Phase 2v applied to R2.** R2's §11.6 evaluated whether HIGH-slip Δexp_H0 stayed positive (i.e., HIGH-slip improvement vs H0 anchor preserved). For F1, the appropriate §11.6 evaluator is **absolute floor preservation at HIGH** — F1 should not collapse below §10.4 hard-reject thresholds at HIGH, regardless of how F1's HIGH-slip absolute results compare to V1's MED-slip results (which would be a cross-family comparison the §11.6 gate is not calibrated for).

**Condition (v) — §10.4-style hard-reject absolute thresholds.** F1 must not violate the §10.4 absolute floors at MED slippage:

```
expR(F1, BTCUSDT, R, MED, MARK)  >  −0.50  AND  PF(F1, BTCUSDT, R, MED, MARK)  >  0.30
AND
expR(F1, ETHUSDT, R, MED, MARK)  >  −0.50  AND  PF(F1, ETHUSDT, R, MED, MARK)  >  0.30
```

(Note condition (i) already implies positive BTC expR; (v) is the parallel ETH check at MED. Together (iii) and (v) cover ETH MED + HIGH absolute-floor preservation.)

### 7.3 Verdict outcomes

Combining conditions (i)–(v):

| Outcome | Conditions met | Interpretation |
|---------|----------------|----------------|
| **PROMOTE — F1 first-execution PASS** | All five (i, ii, iii, iv, v) | F1 has a clean first-execution result. V-window run 5 is executed for §11.3 direction-of-improvement confirmation. F1 becomes a candidate-of-record for any future F1-internal variant work or paper/shadow consideration (the latter remains operator-policy-deferred). |
| **PROMOTE-with-caveats** | (i, ii, v) AND (iii or iv passed but at-margin) | F1 has positive BTC absolute edge and BTC mechanism support but cost-sensitivity or ETH preservation is borderline. V-window run 5 executed. F1 retained as research evidence with mechanism-level findings. |
| **MECHANISM PASS / FRAMEWORK FAIL** | (ii) PASS, (i) or (iii)/(iv)/(v) FAIL | M1 mechanism-supported but framework gate fails. F1 retained as research evidence per Phase 2x / Phase 2y precedent (mechanism informative even when framework fails). |
| **MECHANISM FAIL** | (ii) FAIL, regardless of (i, iii, iv, v) | M1 mechanism-falsified — F1's central claim refuted. F1 disqualified regardless of other conditions. **Family-research closeout.** |
| **HARD REJECT** | Any §10.4-style absolute-floor violation in (iii), (iv), or (v) | F1 is hard-rejected. V-window run 5 not executed. F1 family research is concluded as failed. |

### 7.4 Cross-family references are descriptive only

Per Phase 3b §12.4 + this memo §6.3 / §6.4: H0 and R3 deltas computed from runs 6–9 are **descriptive cross-family references**, not §7.2 governing conditions.

Specifically forbidden:

- **Forbidden:** "F1 promotes if F1 BTC Δexp_H0 ≥ +0.10 R" — this would apply Phase 2 §10.3.a thresholds to a cross-family comparison. F1's promotion governance is **self-anchored absolute** (condition i), not delta-vs-H0.
- **Forbidden:** "F1 promotes if F1 BTC Δexp_R3 ≥ +0.10 R" — same. R3 is V1-family-specific exit machinery; F1 is a different family with different mechanism.
- **Forbidden:** "F1 disqualifies if F1 BTC Δexp_R3 < 0" — F1 producing absolute positive BTC expR while H0/R3 produces a different absolute value is the expected pattern given different families; cross-family deltas are not §10.3-style verdicts.

Cross-family deltas appear in reports for **interpretation context** (e.g., "F1 produces BTC expR +X R while R3 produces BTC expR −0.240 R; F1's edge magnitude is larger / smaller than R3's edge improvement vs H0") but do not gate any §7.2 verdict.

### 7.5 §11.3 V-window discipline

Run 5 (F1 V MED MARK) is conditional on §7.2 PROMOTE outcome. If executed:

- V-window is **no-peeking** during R-window evaluation. V results are not used to fit any F1 parameter (already pre-committed; no fitting allowed regardless).
- V provides direction-of-improvement confirmation: positive expR on V (or less-negative-than-H0-V cross-family reference) supports the R-window verdict.
- V does **not** retroactively re-classify the R-window outcome per Phase 2f §11.3.5.

### 7.6 §11.3.5 binding rule

No threshold change. No post-hoc loosening of conditions (i)–(v). If F1 fails §7.2 PASS criteria, the framework verdict is FAILED per the same discipline that produced R2's FAILED verdict in Phase 2w.

---

## 8. Mandatory diagnostics plan

Phase 3d execution must produce **all** of the diagnostics below. Phase 3c specifies the computation precisely; Phase 3d implements. Diagnostics are computed per F1 governing run (run 1) and per relevant sensitivity run (runs 2–4); subset relevant per cell.

### 8.1 Trade count and frequency

Per F1 run per symbol:

- Total trade count `n`.
- Trades per month (`n / months_in_window`).
- Trades per week.
- Comparison to H0 / R3 trade count on the same window (descriptive cross-family reference).

### 8.2 Long/short split

Per F1 run per symbol:

- Long count, short count.
- Long expR, long PF, long WR.
- Short expR, short PF, short WR.

### 8.3 Per-regime decomposition

Per F1 run per symbol per regime cell. Regime classifier per Phase 2l §6.1 / Phase 2w §11.9 convention: 1h-volatility tercile classifier; trailing 1000 1h-bar Wilder ATR(20) percentile rank; tercile boundaries at 33rd / 67th; classification at the most recent completed 1h bar before entry-fill.

For each cell (low_vol / med_vol / high_vol):

- `n`, `expR`, `PF`, `WR`.

Compared to H0 and R3 per-regime cells (descriptive cross-family reference).

### 8.4 Per-fold consistency

Per F1 run per symbol per fold. Fold convention per Phase 2f §11.2 / GAP-20260424-036: 5 rolling folds; partial-train front edge first fold; 6-month test windows stepping 6 months.

For each fold-symbol cell:

- `n`, `expR`, `PF`.
- Δ vs H0 same fold, Δ vs R3 same fold (descriptive cross-family reference).

### 8.5 Exit-reason fractions

Per F1 run per symbol:

- `stop_exits / n` (fraction stopped out).
- `target_exits / n` (fraction reached SMA(8) target).
- `time_stop_exits / n` (fraction exited at unconditional 8-bar time-stop).
- `(stop_exits + target_exits + time_stop_exits) / n == 1.0` accounting identity (P.14-style hard block; §8.15).

### 8.6 Overextension magnitude distribution

Per F1 run per symbol:

- `overextension_magnitude_at_signal = | cumulative_displacement_8bar(B) | / ATR(20)(B)` for each fired entry.
- Mean, median, p25, p75, max.
- Histogram with bins of 0.25 × ATR width starting at threshold 1.75 × ATR.

### 8.7 Distance-to-mean distribution

Per F1 run per symbol:

- `distance_to_mean_at_signal = | sma_8_close(B) − open(B+1) | / ATR(20)(B)` for each fired entry. (Approximation: `open(B+1) ≈ close(B)` at signal time; actual `open(B+1)` recorded post-fill.)
- Mean, median, p25, p75, max.

### 8.8 Entry-to-target distance

Per F1 run per symbol:

- `entry_to_target_atr = |frozen_target − actual_fill_price| / ATR(20)(B)` for each fired entry.
- Same expressed in R-multiples: `entry_to_target_R = |frozen_target − actual_fill_price| / stop_distance`. This is the per-trade expected R-multiple at perfect target hit.

### 8.9 Stop-distance distribution

Per F1 run per symbol:

- `stop_distance_atr = stop_distance / ATR(20)(B)` for each fired entry. Constrained to [0.60, 1.80] by §2.9.
- Per direction (long / short).
- Histogram with bins of 0.10 × ATR width.

### 8.10 Cooldown / re-entry attribution

Per F1 run per symbol:

- Count of overextension events that fired an entry.
- Count blocked by §2.9 stop-distance admissibility (rejected at signal time).
- Count blocked by §2.7 cooldown (overextension state still active from prior trade).
- Cooldown duration distribution: per cycle, count of completed bars from prior exit until re-entry permission unwound + re-formed.

### 8.11 Cost sensitivity LOW/MEDIUM/HIGH

Per F1 R-window per symbol per slippage tier (runs 1, 2, 3):

- `expR`, `PF`, `WR`, `netPct`, `|maxDD|` per tier.
- Δ vs H0 same tier (descriptive cross-family reference); Δ vs R3 same tier (descriptive cross-family reference).
- §7.2 condition (iv) HIGH-slippage absolute-floor preservation evaluation per cell.

### 8.12 Mark-price vs trade-price sensitivity

Per F1 R-window per symbol (runs 1, 4):

- `expR(MARK_PRICE) − expR(TRADE_PRICE)`.
- `PF(MARK_PRICE) − PF(TRADE_PRICE)`.
- Trade count under each.
- Gap-through stop count under TRADE_PRICE (expected zero per Phase 2l/2m/2s/2w precedent for non-gap-through windows).

### 8.13 MFE / MAE distribution

Per F1 run per symbol per direction per exit-reason:

- MFE (maximum favorable excursion in R-multiples) per fired entry: max(net-R-multiple at any bar during trade).
- MAE (maximum adverse excursion in R-multiples) per fired entry: min(net-R-multiple at any bar during trade).
- Mean, median, max per (direction × exit-reason) cell.

### 8.14 Cross-family reference comparisons

Per F1 vs H0 per F1 vs R3 per symbol:

- ΔexpR, ΔPF, Δ|maxDD|pp, Δn% (descriptive only; not governing per §7.4).
- Per-regime cell deltas (descriptive only).
- Per-fold cell deltas (descriptive only).
- Long/short split deltas (descriptive only).

The reporting must clearly label each cross-family delta as **descriptive cross-family reference; not §10.3-equivalent governing metric**.

### 8.15 P.14-style implementation-bug checks

Hard-block checks (any failure = Phase 3d execution failed; analysis must halt and bug must be fixed before re-run):

- **Accounting identity:** `n_target_exits + n_stop_exits + n_time_stop_exits + n_open_at_window_end = n_fired_entries`.
- **No exit-reason leakage:** F1 must not produce `TRAILING_BREACH`, `STAGNATION`, or V1-`TAKE_PROFIT` exit reasons. F1 emits only `STOP`, `TARGET`, `TIME_STOP`, `END_OF_DATA`.
- **Stop-distance band enforcement (raw):** all fired F1 entries have `stop_distance_at_signal_atr ∈ [0.60, 1.80]` at signal time (de-slipped raw value per Phase 2u §E.3 / Phase 2w P.14).
- **Cooldown enforcement:** zero F1 same-direction re-entries with overlapping overextension state. Verifiable by computing per-trade pre-trade unwind condition: at the bar before each F1 fired entry (other than the first F1 entry per symbol per direction), there must exist at least one completed bar where `| cumulative_displacement_8bar | ≤ 1.75 × ATR(20)` between the prior exit and the new entry.
- **Frozen target invariant:** F1 trade `frozen_target_value` at exit equals SMA(8) at signal-time bar B's close (recomputed from features dataset; cross-checked).
- **Frozen stop invariant:** F1 protective stop at exit equals structural stop computed at signal-time bar B's close.
- **No look-ahead:** all F1 decisions at bar B use only data with `open_time ≤ open_time(B)` (engine per-bar evaluation discipline; verified by H0 / R3 control bit-for-bit reproduction).
- **H0 / R3 control bit-for-bit reproduction:** runs 6–9 must reproduce locked Phase 2e / Phase 2l / Phase 2s / Phase 2w baselines bit-for-bit on every metric cell. Any divergence is a hard-block engine-correctness issue that must be debugged and fixed before F1 results are interpreted.

---

## 9. Mechanism validation plan

### 9.1 M1 — overextension reversion

**Definition:** for each fired F1 entry, compute the post-entry net counter-displacement at horizons {1, 2, 4, 8} completed bars from entry-fill bar `B+1`.

**Computation:** for each fired F1 entry on bar `B+1`:

```
counter_displacement_h(B+1) = 
    (close(B+1+h) − close(B+1)) × (−direction)

where direction = +1 for long entries (entered after downward overextension)
                = −1 for short entries (entered after upward overextension)

Normalized to R-multiples:
    counter_displacement_h_R = counter_displacement_h(B+1) / stop_distance
```

Compute `counter_displacement_h_R` for `h ∈ {1, 2, 4, 8}` for every fired entry on each symbol.

**Aggregate per symbol per horizon:**

- `mean(counter_displacement_h_R)`.
- `fraction(counter_displacement_h_R ≥ 0)`.

**§7.2 condition (ii) M1 BTC pass criteria:**

```
mean(counter_displacement_8_R, BTCUSDT)            ≥  +0.10 R
AND
fraction(counter_displacement_8_R ≥ 0, BTCUSDT)    ≥  50%
```

**M1 ETH evaluation (informative; not in §7.2 conditions):**

- Same metrics on ETHUSDT for cross-symbol diagnostic interpretation.

**Interpretation:**

- **M1 PASS on BTC:** the overextension-reversion mechanism is operative on BTC. F1's central thesis is mechanism-supported. Combined with §7.2 condition (i), F1 has both absolute edge and mechanism support.
- **M1 FAIL on BTC:** the overextension-reversion mechanism is **falsified** on BTC. F1's central thesis is empirically refuted. This is the strongest evidence outcome — even if §7.2 conditions (i, iii, iv, v) all pass somehow, M1 FAIL means F1's edge (if any) is **not** coming from the predicted mechanism. F1 family research closes per §7.3 MECHANISM FAIL outcome.
- **M1 PARTIAL** (mean ≥ +0.10 R but fraction < 50%, OR mean < +0.10 R but ≥ 0): mechanism partially supported. Combined with §7.2 condition (ii) failure logic, treated as MECHANISM FAIL for §7.2 gating purposes; recorded as PARTIAL in research evidence for any future F1-prime spec consideration.

### 9.2 M2 — chop-regime stop-out fraction

**Definition:** F1's stop-out fraction in the low-vol tercile (chop / range-bound regime per §8.3 classifier) compared to H0's stop-out fraction in the same regime on the same R-window.

**Computation:**

```
F1_stop_out_fraction_lowvol(symbol) = 
    n_stop_exits(F1, symbol, low_vol_regime) / n_trades(F1, symbol, low_vol_regime)

H0_stop_out_fraction_lowvol(symbol) = 
    n_stop_exits(H0, symbol, low_vol_regime) / n_trades(H0, symbol, low_vol_regime)
```

H0 stop-out fractions are already on record from Phase 2l §6.1 (BTC low_vol H0: 30.77% WR → 69.23% non-WR; computed similarly for stop-out fraction). Phase 3d run 6 (H0 R MED MARK control re-run) reproduces these for the engine version with F1 dispatch.

**Aggregate per symbol:**

- `Δ_M2(symbol) = H0_stop_out_fraction_lowvol(symbol) − F1_stop_out_fraction_lowvol(symbol)`.

**M2 BTC pass criterion (descriptive; not in §7.2 conditions):**

```
Δ_M2(BTCUSDT)  ≥  +0.10
```

(I.e., F1's BTC low-vol stop-out fraction is at least 10 percentage points lower than H0's.)

**Interpretation:**

- **M2 PASS:** F1 reduces stop-out fraction in chop regime as predicted. The chop-regime advantage hypothesis (Phase 3b §2.3) is supported.
- **M2 FAIL:** F1 does **not** reduce stop-out fraction in chop regime. The chop-regime advantage hypothesis is unsupported on this evidence. **This does not by itself disqualify F1** — F1 could still produce positive absolute edge from the magnitude of its target-exit gains rather than from stop-out reduction. (R2's Phase 2w precedent: M2 FAIL did not by itself disqualify R2; §11.6 cost-sensitivity was the gating failure.)
- **M2 PARTIAL:** `Δ_M2 ∈ (0, +0.10)` on BTC. Mechanism direction-supported but magnitude below pre-declared threshold.

### 9.3 M3 — target-exit positive contribution

**Definition:** F1's TARGET-exit subset must produce positive aggregate net-of-cost R-multiple contribution per symbol.

**Computation:**

```
For each symbol s ∈ {BTCUSDT, ETHUSDT}:
    target_exit_subset(s) = { trade : trade.exit_reason == TARGET AND trade.symbol == s }
    target_exit_aggregate_R(s) = Σ trade.net_r_multiple for trade in target_exit_subset(s)
    target_exit_count(s) = | target_exit_subset(s) |
    mean_target_exit_R(s) = target_exit_aggregate_R(s) / target_exit_count(s)
```

**M3 pass criteria (descriptive; not in §7.2 conditions):**

```
target_exit_aggregate_R(BTCUSDT)  >  0
AND
target_exit_aggregate_R(ETHUSDT)  >  0
AND
mean_target_exit_R(BTCUSDT)       ≥  +0.30
AND
mean_target_exit_R(ETHUSDT)       ≥  +0.30
```

**Interpretation:**

- **M3 PASS on both symbols:** TARGET-exit subset produces positive aggregate net-of-cost contribution; the SMA(8) target's claimed edge is cost-survivable.
- **M3 FAIL on either symbol:** TARGET-exit subset's aggregate net contribution is ≤ 0 OR mean below +0.30 R. The mean-reversion target's claimed edge does not survive cost realism even when isolated.
- **M3 PARTIAL:** PASS on one symbol, FAIL on the other (often BTC PASS / ETH FAIL given §1.7.3 BTCUSDT-primary alignment).

### 9.4 PASS / FAIL / PARTIAL combined interpretation

Phase 3b §9.4 cross-tabulation applied to F1 with §7.2 governance:

| §7.2 outcome | M1 | M2 | M3 | Interpretation |
|--------------|----|----|----|----------------|
| PROMOTE | PASS | PASS | PASS | **Mechanism FULLY supported + framework PROMOTE.** Strongest possible outcome. F1 V-window run 5 executed; family research continues. |
| PROMOTE | PASS | PASS | FAIL | Mechanism partially supported (M3 fails); framework PROMOTE despite M3 fail (target subset cost-erodes but aggregate clears). |
| PROMOTE | PASS | FAIL | PASS | Mechanism partially supported (M2 fails); framework PROMOTE. |
| PROMOTE | PASS | FAIL | FAIL | Mechanism partially supported (only M1); framework PROMOTE; cost / regime caveats prominent. |
| PROMOTE-with-caveats | PASS | * | * | At-margin §7.2 conditions; mechanism informative for any future F1-prime. |
| MECHANISM PASS / FRAMEWORK FAIL | PASS | * | * | M1 mechanism-supported but framework fails. F1 retained as research evidence. |
| MECHANISM FAIL | FAIL | * | * | M1 falsifies F1's central claim. Family research closes. |
| HARD REJECT | * | * | * | §7.2 condition (iii)/(iv)/(v) absolute-floor violation. Family research closes. |

Phase 3d execution **must report all five §7.2 conditions and all three M1/M2/M3 outcomes** independently; the combined verdict follows mechanically from the table.

---

## 10. Quality-gate plan for future Phase 3d

### 10.1 Code-quality gates

Phase 3d implementation must pass all four standard quality gates before any F1 execution run:

| Gate | Command | Pass criterion |
|------|---------|----------------|
| Test suite | `uv run pytest` | All tests pass (target: existing test count preserved + F1-specific test additions; minimum +30 F1 unit tests covering each axis of §2). |
| Linter | `uv run ruff check .` | All checks pass. |
| Formatter | `uv run ruff format --check .` | All files formatted. |
| Type checker | `uv run mypy src` | No type errors. |

Per Phase 2w-A / 2w-B / 2w-C green-gate discipline.

### 10.2 Baseline-preservation checks for V1 breakout behavior

Phase 3d implementation **must reproduce all locked Phase 2 baselines bit-for-bit on the engine version with F1 dispatch added.** Specifically:

- **H0 R-window MED MARK** (run 6) reproduces the locked Phase 2e/2l baseline:
  - BTCUSDT: n=33, WR=30.30%, expR=−0.459, PF=0.255, netPct=−3.39%, maxDD=−3.67%
  - ETHUSDT: n=33, WR=21.21%, expR=−0.475, PF=0.321, netPct=−3.53%, maxDD=−4.13%
- **H0 V-window MED MARK** (run 7) reproduces the locked Phase 2s baseline:
  - BTCUSDT: n=8, WR=25.00%, expR=−0.313, PF=0.541, netPct=−0.56%, maxDD=−0.87%
  - ETHUSDT: n=14, WR=28.57%, expR=−0.174, PF=0.695, netPct=−0.55%, maxDD=−0.80%
- **R3 R-window MED MARK** (run 8) reproduces the locked Phase 2l baseline:
  - BTCUSDT: n=33, WR=42.42%, expR=−0.240, PF=0.560, netPct=−1.77%, maxDD=−2.16%
  - ETHUSDT: n=33, WR=33.33%, expR=−0.351, PF=0.474, netPct=−2.61%, maxDD=−3.65%
- **R3 V-window MED MARK** (run 9) reproduces the locked Phase 2s baseline:
  - BTCUSDT: n=8, WR=25.00%, expR=−0.287, PF=0.580, netPct=−0.51%, maxDD=−1.06%
  - ETHUSDT: n=14, WR=42.86%, expR=−0.093, PF=0.824, netPct=−0.29%, maxDD=−0.94%

Bit-for-bit means each metric matches to recorded precision (8 metric cells × 4 reference runs = 32 metric cells must match).

**Failure to reproduce any cell is a hard-block** per §8.15. Phase 3d execution must halt; engine bug must be diagnosed and fixed; runs 1–5 must not be executed until baseline preservation is verified.

### 10.3 F1 internal consistency checks during implementation

Phase 3d implementation should also include in-test regressions for:

- F1 default config produces zero F1 entries on bars with `cumulative_displacement_8bar = 0` (overextension predicate gates correctly).
- F1 long entry registered when `cumulative_displacement_8bar < −1.75 × ATR` AND stop-distance admissible.
- F1 short entry registered when `cumulative_displacement_8bar > +1.75 × ATR` AND stop-distance admissible.
- F1 target exit at first completed-bar close ≥ frozen target (long) / ≤ frozen target (short).
- F1 stop exit at protective stop hit (mark-price triggered).
- F1 time-stop exit at close of bar B+9 if neither target nor stop fired.
- F1 cooldown blocks same-direction re-entry until unwind condition met.
- F1 stop-distance band rejection at signal-time bar B.
- Same-bar priority in F1: STOP > TARGET > TIME_STOP (analogous to V1 R3's STOP > TAKE_PROFIT > TIME_STOP).

Estimated F1 unit-test count: 30–50 covering all axes (parallel to Phase 2w R2's 43 R2-specific tests).

---

## 11. Phase 3d implementation-risk checklist

Phase 3d execution must explicitly verify each risk below before reporting any F1 result. Each risk has a corresponding diagnostic / hard-block check from §8.15 or §10 above.

### 11.1 Lookahead leakage

**Risk:** F1 decisions at bar B accidentally use data from bar B+1 or later (e.g., next-bar high/low used in ATR; future SMA(8) value used as frozen target).

**Mitigation:** §8.15 P.14 "no look-ahead" check; H0 / R3 control bit-for-bit reproduction (§10.2); per-bar evaluation discipline inherited from Phase 2v.

**Hard-block trigger:** any divergence in H0 / R3 control reproduction implies engine-level lookahead; must halt + debug.

### 11.2 Frozen target vs rolling target confusion

**Risk:** F1 implementation accidentally uses a rolling SMA(8) (recomputed at each bar t > B) instead of the frozen value at signal-time bar B.

**Mitigation:** §8.15 P.14 "frozen target invariant" check — F1 trade record's exit-time frozen_target_value must equal the SMA(8)(B) re-computed from the features dataset. Phase 3d test surface must include explicit frozen-vs-rolling regression.

**Hard-block trigger:** mismatch between recorded frozen_target_value and re-computed SMA(8)(B).

### 11.3 Cooldown off-by-one

**Risk:** §2.7 cooldown rule incorrectly permits same-direction re-entry one bar before unwind condition is fully met, OR forbids re-entry one bar after unwind has actually re-formed.

**Mitigation:** §8.15 P.14 "cooldown enforcement" check — for each F1 fired entry (other than the first per symbol per direction), verify that at least one completed bar between prior exit and new entry has `| cumulative_displacement_8bar | ≤ 1.75 × ATR(20)`. Phase 3d test surface must include cooldown unit tests covering: just-before unwind (block), exact unwind bar (block), bar-after-unwind with new overextension (allow).

**Hard-block trigger:** cooldown enforcement diagnostic finds violation.

### 11.4 Stop-distance raw-vs-slipped issue

**Risk:** §2.9 stop-distance band check is performed on the post-slippage entry price (which has already had MED slippage applied) instead of on the de-slipped raw `open(B+1)`. This was the exact pattern in Phase 2w R2 (P.14 check 2 trades had post-slip r_distance > 1.80 due to slippage; raw values were within band).

**Mitigation:** §8.15 P.14 "stop-distance band enforcement (raw)" check — band check uses raw next-bar-open per Phase 2u §E.3 / Phase 2w P.14 convention. Post-slip r_distance values may exceed band by slippage-induced amount; raw values must not.

**Hard-block trigger:** raw stop_distance_at_signal_atr falls outside [0.60, 1.80] — engine implementation bug.

### 11.5 Target fill timing

**Risk:** target exit fires intrabar (e.g., on a high or low touch within the bar) instead of at completed-bar close; or fill happens at wrong bar (same bar instead of next-bar open).

**Mitigation:** target check uses `close(t) ≥ frozen_target` (long) / `close(t) ≤ frozen_target` (short); fill at `open(t+1)` per §2.5; matches V1 engine fill convention.

**Test surface:** Phase 3d test surface must include explicit cases of: high touches target intrabar but close does not (no exit); close exactly at target (exit); close above target (exit at next-bar open); fill price = `open(t+1)` not `close(t)`.

### 11.6 Mark-price stop trigger

**Risk:** stop-trigger evaluation uses TRADE_PRICE instead of MARK_PRICE despite default; or applies mark-price logic incorrectly (e.g., uses 15m bar mark-price max-min in a way different from the V1 engine convention).

**Mitigation:** F1 inherits the existing engine's stop-trigger logic unchanged (`config.py:38-49` `StopTriggerSource = MARK_PRICE` default). Phase 3d implementation must NOT fork the stop-trigger evaluation for F1.

**Test surface:** F1 R MED TRADE_PRICE run (run 4) should produce bit-identical results to F1 R MED MARK (run 1) on bars where zero gap-throughs occur — same Phase 2l/2m/2s/2w pattern.

### 11.7 Cost application

**Risk:** F1 trades incorrectly apply slippage / taker fee / funding (e.g., slippage applied only to entry but not exit; funding integrated over wrong period; taker fee rate hardcoded instead of from config).

**Mitigation:** F1 inherits the existing engine cost-application logic unchanged (`config.py:55-87`; `cost-modeling.md` "all validation is net of cost"; engine `_apply_costs` method from Phase 2 development). Phase 3d implementation must NOT fork cost application for F1.

**Test surface:** F1 unit tests must include net_r_multiple computation regression across slippage tiers; bit-identical cost computation between F1 and V1 engines on identical inputs.

### 11.8 Feature-dataset versioning

**Risk:** Phase 3d runs use an unversioned or draft-state feature dataset; reports lack feature-dataset-version linkage; multiple runs use different feature-dataset versions inconsistently.

**Mitigation:** §5.3 manifest requirements; `dataset-versioning.md` §"Experiment Linkage Policy" — every F1 run must record its feature-dataset version in `config_snapshot.json` per existing engine convention. Feature dataset must transition from `draft` to `published` per `dataset-versioning.md` §"Publication States" before any reported F1 run; draft-state datasets must not be cited as evidence.

**Test surface:** Phase 3d run-script validation that feature-dataset version is `published` before run starts; runs 1–9 all use the same feature-dataset version (no version drift across runs).

### 11.9 Cross-family comparison misuse

**Risk:** Phase 3d execution reports accidentally apply Phase 2 §10.3.a / §10.3.c thresholds to F1 vs H0 deltas, treating F1 as if it were a V1 variant. Or §10.4 hard-reject thresholds applied to F1 trade-count delta vs H0 (which would always trigger given F1's expected 80–120 trades vs H0's 33).

**Mitigation:** §7 framework distinction; §7.4 explicit forbidden patterns; cross-family deltas labeled "descriptive cross-family reference; not §10.3-equivalent governing metric" in all reports.

**Test surface:** Phase 3d analysis script must compute §7.2 conditions (i)–(v) as **F1-self-anchored absolute** values; cross-family deltas computed separately and clearly labeled. Phase 3c review should confirm analysis-script logic before Phase 3d execution begins.

---

## 12. GO / NO-GO recommendation for Phase 3d

This recommendation is **provisional and evidence-based, not definitive**. The operator decides whether to authorize a downstream Phase 3d implementation phase.

### 12.1 GO criteria evaluation

The operator brief specifies four GO/NO-GO conditions:

1. **GO only if the plan is internally consistent and implementable without spec changes.** ✓ MET — §2 restates Phase 3b spec verbatim; §3 forbids spec change in Phase 3c; §4 implementation surface is implementable using the engine's existing per-bar evaluation discipline + dispatch pattern from Phase 2w-A.
2. **NO-GO if the Phase 3b spec needs changes.** ✓ MET — no spec changes proposed. F1 axes §2.1–§2.9 stand verbatim.
3. **NO-GO if F1 first-execution gate is ambiguous.** ✓ MET — §7.2 defines five precise conditions (i, ii, iii, iv, v); §7.3 maps outcomes to verdicts; §9.1 defines exact M1 computation.
4. **NO-GO if H0/R3 are accidentally treated as governing anchors.** ✓ MET — §7.4 explicitly forbids treating H0/R3 deltas as governing; cross-family references are labeled descriptive throughout (§6.3, §6.4, §8.14, §11.9).
5. **NO-GO if execution would require threshold or project-lock changes.** ✓ MET — §7 uses Phase 2f §10.4-style absolute floors and §11.6 HIGH-slip absolute-floor preservation; no threshold change. §13 preserves all §1.7.3 locks verbatim.

### 12.2 GO recommendation

**GO** — Phase 3d implementation is **provisionally recommended** as the next downstream phase if and when the operator authorizes it.

Phase 3d would be a Phase 2w-A/B/C-style implementation-and-execution phase:
- Phase 3d-A: implementation + tests + scripts + control reproduction (analogous to Phase 2w-A);
- Phase 3d-B: F1 R-window execution + analysis + first-execution gate evaluation per §7 (analogous to Phase 2w-B);
- Phase 3d-C: V-window run 5 if §7.2 PROMOTE; final variant comparison report (analogous to Phase 2w-C).

Phase 3d is **the first phase to authorize source code, tests, scripts, and feature datasets**. Phase 3d does NOT authorize paper/shadow, Phase 4, live-readiness, or deployment work. Phase 3d's runnable checkpoint is: F1 first-execution gate evaluated; framework verdict recorded; cross-family references reported; Phase 3d closeout report ready for operator review.

Estimated Phase 3d implementation surface: 1500–2500 lines of source + tests + scripts (per Phase 3b §8.2 estimate). Estimated Phase 3d execution time: 1–2 days for implementation, ~30 minutes for run set 1–9 (governing + sensitivity + V + control re-runs).

### 12.3 Phase 3d GO does NOT authorize

- **No paper/shadow planning.** Phase 2p §F.2 / post-Phase-2w / Phase 2x §6 / Phase 2y §8.4 / Phase 3a §7 / Phase 3b §15 deferrals stand.
- **No Phase 4 (runtime / state / persistence).** Same authorities.
- **No live-readiness, deployment, exchange-write, production keys.**
- **No threshold change.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds preserved verbatim per Phase 2f §11.3.5 / Phase 2y closeout.
- **No project-level lock change.** §1.7.3 verbatim.
- **No spec change.** Phase 3b §4 axes locked.
- **No run-set expansion.** §6 inventory pre-committed; mid-execution additions forbidden.
- **No MCP / Graphify / `.mcp.json` / credentials / `data/` commits.**

### 12.4 Alternative: NO-GO and remain paused

If the operator judges that Phase 3d is not the right next step, **remaining paused** is a valid alternative:

- The Phase 3a, 3b, 3c memos preserved on `main` constitute the F1 family-research artifact even without Phase 3d authorization.
- Phase 2x Option A (remain paused after Phase 2y closure) continues to be valid.
- F1's spec + execution plan are preserved for any future revival.

The recommendation is **GO for Phase 3d if any active path is desired**, with **remain-paused as the legitimate alternative** under the operator's discretion.

---

## 13. Explicit project-state preservation statement

Phase 3c explicitly preserves the following:

- **R3 remains the V1 breakout baseline-of-record** per Phase 2p §C.1. Locked sub-parameters: `exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`. Same-bar priority STOP > TAKE_PROFIT > TIME_STOP. R3 is **not** F1's anchor or baseline (§7.4).
- **H0 remains the formal V1 breakout framework anchor** per Phase 2i §1.7.3. H0 is **not** F1's framework anchor (§7.1); F1 uses self-anchoring per §7.2.
- **R1a remains research evidence only** per Phase 2p §D. Retained-for-future-hypothesis-planning.
- **R1b-narrow remains research evidence only** per Phase 2s §13.
- **R2 remains research evidence only** per Phase 2w §16.3. Framework verdict FAILED — §11.6 cost-sensitivity blocks. Mechanism evidence (M1 + M3 PASS; M2 FAIL) preserved as descriptive.
- **No threshold change.** Phase 2f §10.3 / §10.4 / §11.3 / §11.4 / **§11.6 = 8 bps HIGH** preserved verbatim per Phase 2f §11.3.5 / Phase 2y closeout. `src/prometheus/research/backtest/config.py:55-87` unchanged.
- **No project-level lock change.** §1.7.3 BTCUSDT primary, ETHUSDT research/comparison only, one-symbol-only live, one-position max, 0.25% risk per trade, 2× leverage cap, mark-price stops, v002 datasets — all preserved verbatim.
- **No paper/shadow planning is authorized.**
- **No Phase 4 (runtime / state / persistence) is authorized.**
- **No live-readiness work, no deployment work, no exchange-write capability, no production keys, no MCP / Graphify / `.mcp.json` activation, no credentials.**
- **No `data/` commits.**
- **No code change.** No file in `src/`, `tests/`, or `scripts/` is touched by Phase 3c.
- **No tests written.** F1 test suite is Phase 3d work.
- **No scripts written.** F1 runner script is Phase 3d work.
- **No feature dataset created.** F1 feature datasets `mean_reversion_features_<symbol>_15m__v001` are Phase 3d artifacts.
- **No backtest run.** F1 runs 1–9 are Phase 3d-execution work, separately authorized after Phase 3d-implementation.
- **No spec change.** Phase 3b §4 binding axes preserved verbatim per §3.
- **No V1 breakout family revival.** F1 is a new family; V1 R3 remains paused-as-baseline-of-record without active V1-family research.
- **No Phase 3d authorization.** Phase 3c recommends GO for Phase 3d (§12.2) provisionally; the operator separately authorizes Phase 3d (or doesn't).

---

**End of Phase 3c F1 execution-planning memo.** Sections 1–13 complete per the operator brief's required structure. Phase 3b spec restated verbatim; Phase 3c does not modify spec. Implementation surface specified for Phase 3d (new `mean_reversion_overextension/` strategy module; `MeanReversionConfig` + `MeanReversionStrategy`; engine dispatch via new `StrategyFamily` enum or equivalent; F1-specific TradeRecord fields and exit-reason categories; baseline-preservation discipline for V1 unchanged). v002 datasets sufficient; new versioned feature datasets specified per `dataset-versioning.md`. Run inventory pre-committed to 9 runs (4 F1 governing + 1 F1 V conditional + 4 H0/R3 reference re-runs). F1 first-execution gate defined per Phase 3b §12 with five precise conditions; H0/R3 cross-family references are descriptive only. M1/M2/M3 mechanism-validation computation specified exactly. Quality-gate plan + baseline-preservation checks specified for Phase 3d. Implementation-risk checklist enumerated for Phase 3d. **GO (provisional) recommendation for Phase 3d implementation** as the next downstream phase if and when the operator authorizes it; **remain-paused** is the legitimate alternative. Project state preserved verbatim. **NO-GO for any execution / paper-shadow / Phase 4 / live-readiness / deployment / threshold-change / project-lock change.** R3 V1 baseline-of-record / H0 V1 framework-anchor / R1a-R1b-narrow-R2 retained-research-evidence preserved. Awaiting operator review.
