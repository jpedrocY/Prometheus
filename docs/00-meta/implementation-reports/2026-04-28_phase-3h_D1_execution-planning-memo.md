# Phase 3h — D1-A Execution-Planning Memo

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; **no post-hoc loosening per §11.3.5**); Phase 2i §1.7.3 project-level locks; Phase 2p consolidation memo §C.1 (R3 baseline-of-record); Phase 2x family-review memo (V1 breakout family at useful ceiling); Phase 2y slippage / cost-policy review (§11.6 = 8 bps HIGH per side preserved verbatim); Phase 3a new-strategy-family discovery memo (F6 funding-aware ranked rank-2 near-term); Phase 3c F1 execution-planning memo (precedent template); Phase 3d-A / 3d-B1 / 3d-B2 reports (F1 HARD REJECT; Phase 3d-B2 terminal-for-F1; staged implementation precedent); Phase 3e post-F1 research consolidation memo; Phase 3f next research-direction discovery memo (D1 ranked rank-1 active path); **Phase 3g D1-A funding-aware spec memo + methodology sanity audit + closeout + merge report (binding spec)**; `docs/03-strategy-research/v1-breakout-strategy-spec.md`; `docs/05-backtesting-validation/backtesting-principles.md`; `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`; `docs/05-backtesting-validation/cost-modeling.md`; `docs/04-data/data-requirements.md`; `docs/04-data/dataset-versioning.md`; `.claude/rules/prometheus-core.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/implementation-ambiguity-log.md`; `src/prometheus/research/backtest/config.py` (existing `StrategyFamily` / `BacktestConfig` / `BacktestAdapter` definitions and dispatch invariants).

**Phase:** 3h — Docs-only **D1-A execution-planning memo (Phase-3c-style).** Defines the exact future implementation, validation, run inventory, diagnostics, hard-block checks, and first-execution gate for D1-A. **Execution-planning-only**, not implementation, not backtesting, not execution, not parameter search, not paper/shadow, not Phase 4, not live-readiness, not deployment. Phase 3h does not authorize any subsequent phase.

**Branch:** `phase-3h/d1-execution-planning`. **Memo date:** 2026-04-28 UTC.

**Status:** Plan drafted. **No code change. No backtest. No variant created. No parameter tuned. No threshold changed. No project-level lock changed. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write proposal.** R3 remains V1-breakout baseline-of-record. H0 remains framework anchor. R1a / R1b-narrow / R2 / F1 remain retained research evidence. F1 framework verdict HARD REJECT. Phase 3d-B2 terminal for F1. D1-A specified per Phase 3g (funding-aware contrarian; |Z_F| ≥ 2.0 over trailing 90 days; 1.0 × ATR(20) stop; +2.0R TARGET; 32-bar time-stop; per-funding-event cooldown; symmetric direction; no regime filter); not implemented. §11.6 = 8 bps HIGH per side preserved verbatim. §1.7.3 project-level locks preserved verbatim. Plan is **provisional and falsifiable**; no implementation or execution authorization follows automatically.

---

## 1. Plain-English explanation of what Phase 3h is deciding

Phase 3h produces a Phase-3c-style execution-planning memo for D1-A. It is the analogue of Phase 3c (the F1 execution-planning memo) for the D1-A family that Phase 3g locked as the binding spec.

What Phase 3h produces:

- A precommitted run inventory (mandatory R-window cells + conditional V-window).
- A first-execution gate definition with PROMOTE / HARD REJECT / FRAMEWORK FAIL / MECHANISM FAIL outcomes (reproducing Phase 3g §13 verbatim).
- M1 / M2 / M3 mechanism check definitions with explicit PASS / FAIL / PARTIAL interpretation.
- Mandatory diagnostics for any future first execution.
- P.14-style hard-block invariants enforcing engine correctness before any verdict is issued.
- An implementation architecture plan (config model, dispatch surface, module layout, output fields, lifecycle counters) that any future Phase 3i-equivalent implementation phase would consume.
- A staged implementation split recommendation analogous to Phase 3d-A / 3d-B1 / 3d-B2 (Phase 3i-A primitives + non-runnable; Phase 3i-B1 engine-wiring + runnable but guarded; Phase 3j candidate runs + first-execution gate).
- An explicit GO / NO-GO recommendation for the next docs-only or implementation phase.

What Phase 3h does **not** decide:

- Not deciding whether to implement D1-A (separate Phase 3i-A authorization required).
- Not deciding whether to run any backtest (separate Phase 3j authorization required after Phase 3i-B1).
- Not deciding whether to begin paper/shadow, Phase 4, live-readiness, or deployment work (forbidden by operator policy).
- Not deciding whether to lift any §1.7.3 project-level lock.
- Not deciding whether to revise any Phase 2f threshold (Phase 2y closed this; preserved through Phase 3e / Phase 3f / Phase 3g).
- Not authorizing F1-prime, F1-target-subset, R1a-prime, R1b-prime, R2-prime, D1-A-prime, D1-B, D1-A-on-V1 hybrid, or any retroactive rescue (forbidden by Phase 3e §8.6 + Phase 3f §5.7 + Phase 3g §14 + Phase 3g methodology audit §5.4).
- Not authorizing any next phase. Phase 3i-A requires its own separately-authorized operator decision.

Phase 3h produces a memo. The operator decides whether to authorize a downstream Phase 3i-A implementation phase, or to remain paused at the post-Phase-3h plan boundary, or to authorize an alternative direction.

---

## 2. Current canonical project state

| Item | State |
|------|-------|
| **R3 (Phase 2j memo §D — Fixed-R + 8-bar TIME_STOP, no trailing)** | **V1 breakout baseline-of-record** per Phase 2p §C.1; locked sub-parameters `exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`; same-bar priority STOP > TAKE_PROFIT > TIME_STOP; protective stop never moved intra-trade. |
| **H0 (Phase 2e locked baseline)** | **V1 breakout framework anchor** per Phase 2i §1.7.3. |
| **R1a / R1b-narrow / R2 / F1** | Retained as **research evidence only**. R2 framework FAILED — §11.6 cost-sensitivity blocks. F1 framework verdict HARD REJECT (Phase 3c §7.3 catastrophic-floor predicate; 5 violations across BTC/ETH × MED/HIGH cells). Phase 3d-B2 terminal for F1. |
| **D1-A (Phase 3g binding spec)** | **Specified, not implemented.** Funding-rate extreme contrarian directional signal; |Z_F| ≥ 2.0 over trailing 90 days; 1.0 × ATR(20) stop never moved; +2.0R TARGET (revised from +1.0R per Phase 3g §5.6 RR/target sanity Option A using R3's non-fitting convention); 32-bar time-stop = one funding cycle; per-funding-event cooldown; symmetric direction; no regime filter. |
| **§1.7.3 project-level locks** | **Preserved verbatim:** BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; one active protective stop max; 0.25% risk per trade; 2× leverage cap; mark-price stops; v002 datasets; one-way mode; isolated margin; no pyramiding; no reversal while positioned; no hedge mode. |
| **Phase 2f thresholds** | **Preserved verbatim:** §10.3.a Δexp ≥ +0.10 R; §10.3.c |maxDD| ratio < 1.5×; §10.4 absolute floors expR > −0.50 AND PF > 0.30; §11.3 V-window no-peeking; §11.4 ETH non-catastrophic; **§11.6 = 8 bps HIGH per side** (Phase 2y closeout). |
| **Paper/shadow planning** | **Not authorized.** |
| **Phase 4 (runtime / state / persistence) work** | **Not authorized.** |
| **Live-readiness / deployment / production-key / exchange-write work** | **Not authorized.** |
| **MCP / Graphify / `.mcp.json`** | **Not activated, not touched.** |
| **Credentials / `.env` / API keys** | **Not requested, not created, not used.** |

Phase 3h operates within the pause posture and the Phase 3g binding D1-A spec; no project-state mutation is authorized.

---

## 3. Phase 3g D1-A locked spec restatement

The Phase 3g spec memo (with both amendments incorporated and the methodology sanity audit confirming structural sanity) is binding. Phase 3h reproduces the locked spec verbatim:

| Axis | Locked rule | Source |
|------|-------------|--------|
| Strategy family | Funding-aware directional / carry-aware (D1-A) | Phase 3g §1 / §6 |
| Funding signal source | Most recent completed Binance USDⓈ-M 8h funding event prior to 15m bar close (00:00 / 08:00 / 16:00 UTC settlement) | Phase 3g §6.1 |
| Threshold | `|Z_F| ≥ 2.0` | Phase 3g §6.1 |
| Lookback | Trailing 90 days of completed funding events (270 events) | Phase 3g §6.2 |
| Lookahead exclusion | Current event excluded from rolling mean μ_F and standard deviation σ_F | Phase 3g §6.1, §6.2 |
| Direction | Contrarian: `Z_F ≥ +2.0` → SHORT; `Z_F ≤ −2.0` → LONG | Phase 3g §6.3 |
| Entry timing | Market entry at next 15m bar open after signal | Phase 3g §6.4 |
| Allowed directionality | Symmetric long and short | Phase 3g §6.5 |
| Timeframe | 15m completed bars; funding events at completed 8h boundaries | Phase 3g §6.6 |
| Stop | `1.0 × ATR(20)` at fill, never moved intra-trade, MARK_PRICE trigger | Phase 3g §6.7 |
| Target | `+2.0 R TARGET` (revised from +1.0R per §5.6 Option A using R3's non-fitting convention); recorded exit reason TARGET (not TAKE_PROFIT) | Phase 3g §6.8, §5.6 |
| Same-bar priority | `STOP > TARGET > TIME_STOP` | Phase 3g §6.8 |
| Time-stop | Unconditional 32 × completed 15m bars from entry fill (= 8h = one funding cycle); triggers at close of bar `B+1+32`; fills at open of bar `B+1+33`; no same-close fill | Phase 3g §6.9 |
| Cooldown | Per-funding-event consumption; same-direction requires fresh event after position close; opposite-direction allowed at any subsequent event | Phase 3g §6.10 |
| Stop-distance admissibility | `[0.60, 1.80] × ATR(20)`; D1-A's 1.0 × ATR is inside the band by construction | Phase 3g §6.11 |
| Funding accrual | Existing engine `apply_funding_accrual` linear-scan unchanged | Phase 3g §6.12 |
| Regime filter | None | Phase 3g §6.13 |
| Funnel counters | Funding-event-level (NOT per-bar): `funding_extreme_events_detected/_filled/_rejected_stop_distance/_blocked_cooldown`; identity preserved | Phase 3g §9.4 (first amendment), §12 |

Forbidden in Phase 3h scope and any future implementation/execution:

- No target sweep (any future researcher proposing alternative `target_r_multiple` values is forbidden post-hoc loosening).
- No threshold sweep on |Z_F| ≥ 2.0.
- No lookback sweep on N=90 days.
- No time-stop sweep on 32 bars.
- No stop-distance sweep on 1.0 × ATR(20).
- No regime-conditional D1-A-prime.
- No D1-B (funding-aware filter on a directional thesis) — Phase 3g §4 explicitly rejected D1-B; structural problems on every base thesis.
- No V1/D1 hybrid (D1-A signal as filter on top of V1 / R3 baseline) — would be either an R-axis variant on closed V1 family or a D1-B disguised proposal; both forbidden.
- No F1/D1 hybrid (D1-A signal applied to F1 overextension subset) — would be F1-prime / target-subset rescue forbidden by Phase 3e §5.4 / §8.6 + Phase 3f §5.7 + Phase 3g §14 + Phase 3g methodology audit §5.4.
- No additional symbols (BTCUSDT primary; ETHUSDT research/comparison only per §1.7.3).

---

## 4. Data and feature plan

### 4.1 v002 raw datasets sufficient

Confirmed. **No v003 raw-data bump is needed** for D1-A research. Phase 3g §8 / methodology audit §3.7 confirmed.

### 4.2 Required raw inputs

All from Phase 2e v002 normalized datasets:

- **15m OHLCV** for BTCUSDT and ETHUSDT (`usdm_klines_btcusdt_15m__v002` / `usdm_klines_ethusdt_15m__v002`).
- **Mark-price 15m data** for stop-trigger evaluation per §1.7.3 mark-price-stops lock.
- **Funding-rate history** for BTCUSDT and ETHUSDT (`usdm_funding_rate__v002`). This is the primary signal source for D1-A.
- **Exchange metadata** (existing v002 `exchangeInfo` snapshot) for tick / step / lot-size constraints.

No 1h derived bars required for D1-A signal logic (D1-A does not use 1h bias filtering). 1h derived bars per Phase 2e remain available for descriptive comparison only (e.g., per-volatility-regime diagnostics).

### 4.3 Derived feature dataset

**One new derived dataset is required** at any future implementation phase:

- Name: `funding_aware_features__v001`
- Category: derived (per `dataset-versioning.md` §"Datasets that must be versioned" → "Derived datasets").
- Predecessors: `usdm_funding_rate__v002`; `usdm_klines_btcusdt_15m__v002`; `usdm_klines_ethusdt_15m__v002`.
- Manifest required (per `dataset-versioning.md` §"Dataset Manifest Policy").

### 4.4 Required derived fields

Each row of the derived dataset captures funding-event-grid and bar-grid features:

| Field | Description | Grid |
|-------|-------------|------|
| `funding_event_id` | Stable identifier for a funding settlement event. Suggested: `f"{symbol}-{funding_time_ms}"`. | Funding-event grid + bar-grid reference |
| `funding_time` | UTC milliseconds timestamp of the completed funding settlement event | Funding-event grid |
| `funding_rate` | Raw funding rate at the event (signed; e.g., +0.0001 = +0.01% per 8h) | Funding-event grid |
| `funding_z_score` | Trailing-90-day Z-score of the funding rate at the event, computed using μ_F and σ_F over the 270 prior completed events (the current event excluded from the rolling mean/std). | Funding-event grid |
| `funding_z_score_at_bar` | Z-score of the most recent completed funding event prior to the 15m bar close. | 15m bar-grid |
| `bars_since_funding_event` | Number of completed 15m bars since the most recent funding settlement (0 at the bar covering the settlement; increments per bar). | 15m bar-grid |
| `funding_event_consumed` | Boolean flag indicating whether a D1-A position has been opened on the most recent extreme funding event prior to the current bar. Set during simulation; not pre-computed in the dataset. | Lifecycle/simulation runtime |

### 4.5 Timestamp and no-lookahead invariants

- **Funding event used at signal must satisfy `funding_time ≤ bar_close_time`.** No 15m bar may use a funding event whose `funding_time > bar_close_time`. Strict inequality if `funding_time == bar_close_time` is treated implementation-defined; Phase 3i should commit to the strict-or-non-strict convention explicitly and document it.
- **Rolling 90-day Z-score excludes the current event.** μ_F and σ_F at event `t` are computed over the 270 prior events `t−1, t−2, …, t−270`; event `t` is *not* used in its own normalization. This is the no-lookahead invariant.
- **Repeated 15m bars referencing the same funding event must not inflate event-level counts.** Funnel counters (`funding_extreme_events_detected` etc.) are at the funding-event level; a unique `funding_event_id` is counted once.
- **All canonical timestamps are UTC Unix milliseconds** per `timestamp-policy.md`.
- **Completed-bar discipline** per `data-requirements.md` §"Core Data Principles" §1: 15m signal evaluation only after the bar has fully closed; no partial-bar inputs to D1-A.

### 4.6 No `data/` artifact may be committed

Per Phase 3g §11 / §16 / Phase 3h preservation: any `data/derived/funding_aware_features__v001/` Parquet output produced by a future implementation phase must remain in the git-ignored `data/` tree. No `data/` files may be staged or committed.

---

## 5. Implementation architecture plan for a future Phase 3i

This section is **descriptive / forward-looking only**. Phase 3h does not authorize any of the implementation work below. A separately-authorized Phase 3i-A is required to begin implementation. Each subsequent phase requires its own operator-decision gate.

### 5.1 New strategy family enum

Add a third value to `prometheus.research.backtest.config.StrategyFamily`:

```python
class StrategyFamily(StrEnum):
    V1_BREAKOUT = "V1_BREAKOUT"
    MEAN_REVERSION_OVEREXTENSION = "MEAN_REVERSION_OVEREXTENSION"
    FUNDING_AWARE_DIRECTIONAL = "FUNDING_AWARE_DIRECTIONAL"  # D1-A (Phase 3g)
```

The default remains `V1_BREAKOUT` so all existing V1 / R3 / R1a / R1b-narrow / R2 backtests continue to dispatch to the V1 path bit-for-bit.

### 5.2 New locked config model

Add a new strategy-config dataclass mirroring `MeanReversionConfig` precedent:

```text
src/prometheus/strategy/funding_aware_directional/variant_config.py
```

containing `FundingAwareConfig` with locked default values per Phase 3g §6:

```text
funding_z_score_threshold = 2.0          # |Z_F| extreme threshold
funding_z_score_lookback_days = 90       # trailing-90-day rolling window
stop_distance_atr_multiplier = 1.0       # 1.0 × ATR(20) at fill
target_r_multiple = 2.0                  # +2.0R TARGET (revised from +1.0R per Phase 3g §5.6 Option A)
time_stop_bars = 32                      # 32 × 15m = 8h = one funding cycle
cooldown_rule = "per_funding_event"      # per-funding-event consumption
stop_distance_admissibility_band = (0.60, 1.80)
direction_logic = "contrarian"
regime_filter = None
```

The model_config should be `frozen=True, strict=True, extra="forbid"` per Phase 3d-A `MeanReversionConfig` precedent. No alternate values configurable at runtime.

### 5.3 New self-contained strategy module

Suggested module path:

```text
src/prometheus/strategy/funding_aware_directional/
├── __init__.py
├── variant_config.py      # FundingAwareConfig (above)
├── primitives.py          # pure functions: Z-score, event detection, signal direction, cooldown
└── strategy.py            # FundingAwareStrategy class with stateful per-symbol session
```

Following the `strategy/mean_reversion_overextension/` Phase 3d-A precedent: self-contained, no V1 imports, no F1 imports, no cross-family coupling.

### 5.4 Expected module functions / methods

| Function | Purpose | Inputs | Output |
|----------|---------|--------|--------|
| `compute_funding_z_score(funding_rates, lookback_events=270)` | Compute trailing-N-event Z-score of the funding rate at the latest event, excluding the current event from μ/σ. | Sequence of (funding_time, funding_rate) tuples | float Z-score (or NaN during warmup) |
| `align_funding_event_to_bar(funding_events, bar_close_time)` | Return the most recent completed funding event with `funding_time ≤ bar_close_time`. | Funding event list; bar close ms | Funding event record or None |
| `funding_extreme_event(z_score, threshold=2.0)` | Return contrarian direction if `|Z_F| ≥ threshold`, else None. | Z-score, threshold | "LONG" / "SHORT" / None |
| `signal_direction(z_score, threshold)` | Map Z_F to entry direction: `Z ≥ +threshold` → SHORT; `Z ≤ −threshold` → LONG. | Z-score, threshold | enum |
| `compute_stop(fill_price, atr20, side)` | Compute structural stop = `fill_price ± 1.0 × atr20`. | fill_price, atr20, side | stop_price |
| `compute_target(fill_price, stop_distance, side)` | Compute +2.0R target = `fill_price ± 2.0 × stop_distance`. | fill_price, stop_distance, side | target_price |
| `time_stop_bar_index(entry_bar_idx, time_stop_bars=32)` | Return `entry_bar_idx + time_stop_bars` (the bar at whose close TIME_STOP triggers). Fill bar is +1 beyond. | int, int | int |
| `can_re_enter(direction, latest_event_id, consumed_event_id, position_open)` | Event-level cooldown gate. Returns True iff `direction` allowed: position not open AND (`latest_event_id != consumed_event_id` OR opposite direction). | enums + ids + bool | bool |

### 5.5 BacktestConfig validation rules

Extend the `BacktestConfig` model_validator (file `src/prometheus/research/backtest/config.py`) to handle the new family:

1. Add `funding_aware_variant: FundingAwareConfig | None = None` field.
2. Validator clauses:
   - When `strategy_family == V1_BREAKOUT`: require `mean_reversion_variant is None` AND `funding_aware_variant is None` (default V1).
   - When `strategy_family == MEAN_REVERSION_OVEREXTENSION`: require `mean_reversion_variant` non-None AND `funding_aware_variant is None`; reject non-default `strategy_variant` (existing F1 invariants).
   - When `strategy_family == FUNDING_AWARE_DIRECTIONAL`: require `funding_aware_variant` non-None AND `mean_reversion_variant is None`; reject non-default `strategy_variant` (D1-A does not consume V1 axes).
3. Default family remains `V1_BREAKOUT`. All existing V1 / F1 backtests must continue to validate and dispatch unchanged.

The default V1 path must be bit-for-bit unchanged after this validator extension. The F1 path must also be bit-for-bit unchanged.

### 5.6 BacktestEngine dispatch plan

Extend `BacktestEngine` (file `src/prometheus/research/backtest/engine.py`) to dispatch the `FUNDING_AWARE_DIRECTIONAL` family to a new `_run_symbol_d1a` method analogous to `_run_symbol_f1`:

- Per-bar lifecycle:
  1. At each completed 15m bar close, query the most recent completed funding event prior to bar close.
  2. Compute the Z-score using the trailing 90-day rolling window (excluding current event).
  3. If `|Z_F| ≥ 2.0` AND the event has not been consumed AND no D1-A position is currently open AND cooldown does not block the candidate direction, register entry candidate at bar `B+1` open.
  4. On fill: compute stop, target, time-stop bar-index; record `funding_event_id`, `funding_z_score_at_signal`, `funding_rate_at_signal`, `bars_since_funding_event_at_signal`, `entry_to_target_distance_atr`, `stop_distance_at_signal_atr`.
  5. Per-bar while position open: check STOP (MARK_PRICE) > TARGET > TIME_STOP precedence at bar close; close position at next-bar open with the chosen exit reason.
  6. On position close: increment funding-event funnel counter; mark `funding_event_consumed = True` for that event id.
- Per-symbol session state:
  - `latest_completed_funding_event_id`
  - `latest_funding_event_consumed_id_long` / `_id_short` (for direction-asymmetric cooldown bookkeeping)
  - `current_position` (LONG / SHORT / FLAT) and metadata (`fill_price`, `stop_distance`, `target_price`, `time_stop_bar_idx`, `entry_funding_event_id`).
  - `funding_aware_lifecycle_counters` (event-level).
- New private method skeleton: `_open_d1a_trade`, `_close_d1a_trade_stop`, `_close_d1a_trade_target`, `_close_d1a_trade_time_stop`, `_close_d1a_trade_eod` (analogous to F1's `_open_f1_trade` / `_close_f1_trade_*`).

### 5.7 TradeRecord field additions

Extend `TradeRecord` (file `src/prometheus/research/backtest/trade_log.py`) with D1-A-specific fields, NaN-default to preserve schema for existing V1/F1 trades:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `funding_event_id_at_signal` | str / None | NaN | Funding event id consumed at entry. |
| `funding_z_score_at_signal` | float | NaN | Z-score of the entry funding event. |
| `funding_rate_at_signal` | float | NaN | Raw funding rate at the entry event. |
| `bars_since_funding_event_at_signal` | int | NaN | Bars elapsed since funding event at entry. |
| `entry_to_target_distance_atr` | float | NaN | `target_distance / atr20 = 2.0 × stop_distance / atr20 = 2.0` by construction. |
| `stop_distance_at_signal_atr` | float | NaN | `stop_distance / atr20 = 1.0` by construction. |

Existing F1 fields (`overextension_magnitude_at_signal`, `frozen_target_value`, etc.) remain NaN for D1-A trades.

The `funding_accrual_total_R` field already exists in the engine's accrual layer; D1-A trades populate it via the same `apply_funding_accrual` path (Phase 3g §6.12 / §9.5).

### 5.8 Lifecycle counter additions

Add `FundingAwareLifecycleCounters` Pydantic model (file `src/prometheus/research/backtest/engine.py` or a peer module):

```text
funding_extreme_events_detected: int
funding_extreme_events_filled: int
funding_extreme_events_rejected_stop_distance: int
funding_extreme_events_blocked_cooldown: int
```

Identity invariant (event-level):

```text
funding_extreme_events_detected
= funding_extreme_events_filled
+ funding_extreme_events_rejected_stop_distance
+ funding_extreme_events_blocked_cooldown
```

Per-run aggregator emits a `funding_aware_lifecycle_total.json` analogous to F1's `f1_lifecycle_total.json`.

### 5.9 Diagnostics / reporting changes

Extend the `_phase3X_D1A_analysis.py` script template (modeled on `_phase3d_F1_analysis.py`) to compute:

- §10 first-execution gate per Phase 3h §11 below.
- §11 M1 / M2 / M3 mechanism checks per Phase 3h §12.
- §12 diagnostics per Phase 3h §13.
- §13 P.14 hard-block invariants per Phase 3h §14.
- §14 cross-family deltas vs H0 / R3 / F1 (descriptive only per Phase 3g §13.1).

The analysis script writes a JSON report to a git-ignored `data/derived/backtests/phase-3X-d1a-analysis-<run_id>.json` location.

---

## 6. Future Phase 3i implementation split recommendation

A safe staged implementation sequence analogous to Phase 3d-A / 3d-B1 / 3d-B2 is recommended. **These are recommendations only**; each phase requires its own separately-authorized operator decision.

### 6.1 Phase 3i-A — D1-A primitives + config + tests + control reproduction; non-runnable

**Scope:**

- Add `StrategyFamily.FUNDING_AWARE_DIRECTIONAL` enum value.
- Implement `FundingAwareConfig` locked variant config.
- Implement `prometheus.strategy.funding_aware_directional.primitives` (pure functions: Z-score, event alignment, signal direction, stop/target computation, cooldown).
- Implement `FundingAwareStrategy` module skeleton (no engine wiring yet).
- Extend `BacktestConfig` validator to accept the new family but with a hard guard that **REJECTS RUNTIME DISPATCH** of D1-A with a `RuntimeError("D1-A engine wiring not yet authorized; see Phase 3i-B1.")`. This mirrors Phase 3d-A's deliberate non-runnability.
- Add unit tests covering all primitives + config validation (per §7 below).
- Run all quality gates (per §8 below).
- Reproduce H0 / R3 / F1 controls bit-for-bit (per §9 below).

**Forbidden:**

- No `_run_symbol_d1a` engine method.
- No D1-A backtest invocation from any script.
- No runner script for D1-A (deferred to Phase 3i-B1).
- No D1-A diagnostics / analysis script.
- No `data/` artifacts.

**Acceptance criteria:**

- 100% of new D1-A unit tests pass.
- All existing V1 / F1 / engine / config / data-loader tests pass unchanged.
- ruff check, ruff format, mypy on `src` all green.
- H0 / R3 / F1 control bit-for-bit reproduction verified.
- D1-A is deliberately non-runnable; an attempt to dispatch raises the documented guard error.

### 6.2 Phase 3i-B1 — D1-A engine wiring + lifecycle counters + output fields + runner scaffold + controls; no D1-A candidate runs

**Scope:**

- Lift the Phase 3i-A guard.
- Implement `_run_symbol_d1a` engine method per §5.6.
- Add `FundingAwareLifecycleCounters` and event-level funnel logic per §5.8.
- Extend `TradeRecord` and parquet schema with D1-A fields per §5.7.
- Implement runner script `scripts/phase3X_D1A_execution.py` analogous to `scripts/phase3d_F1_execution.py`, **hard-guarded by a `--phase-3X-authorized` flag** so no accidental D1-A run can occur until Phase 3j is authorized.
- Add additional unit tests covering the engine dispatch, exit precedence, funnel identity, lookahead invariants (per §7 below).
- Run all quality gates.
- Reproduce H0 / R3 / F1 controls bit-for-bit on the wired engine.

**Forbidden:**

- No D1-A candidate backtest invocation. Phase 3i-B1 produces a runnable engine path but does NOT run any D1-A R-window or V-window cell.
- No first-execution gate evaluation.
- No M1 / M2 / M3 computation on real data.
- No `data/` artifacts beyond the existing git-ignored backtests directory (control re-runs may write to `data/derived/backtests/` but this is git-ignored).

**Acceptance criteria:**

- All Phase 3i-A tests pass + new Phase 3i-B1 engine-wiring tests pass.
- ruff / ruff format / mypy green.
- H0 / R3 / F1 controls reproduce bit-for-bit on all 48+ metric cells (4 control runs × 2 symbols × 6 metrics).
- D1-A engine path executes without raising the Phase 3i-A guard but no candidate run authorized.
- The Phase 3i-B1 runner exits with a non-zero status if invoked without `--phase-3X-authorized`.

### 6.3 Phase 3j (or Phase 3i-B2) — D1-A candidate runs + diagnostics + first-execution gate

**Scope:**

- Execute the Phase 3h §10 precommitted run inventory (4 mandatory R-window cells + 1 conditional V cell).
- Compute the §11 first-execution gate.
- Compute §12 M1 / M2 / M3 mechanism checks.
- Produce §13 mandatory diagnostics.
- Run §14 P.14 hard-block invariants.
- Emit verdict per §11 verdict mapping.
- Produce execution-diagnostics report + closeout + merge-report.

**Forbidden:**

- No threshold sweep. No target sweep. No lookback sweep. No time-stop sweep. No regime-filter exploration.
- No D1-A-prime spec proposal regardless of outcome.
- No paper/shadow / Phase 4 / live-readiness / deployment authorization.
- No `data/` commits.

**Acceptance criteria:**

- All 4 mandatory R-window cells execute end-to-end.
- §14 P.14 hard-block invariants all PASS (otherwise verdict is HALTED, not issued).
- Verdict issued per §11 verdict mapping with full evidence trail.

### 6.4 Recommendation framing

These three phases are **sequential-by-default** and each **requires separate operator authorization**:

- Phase 3h merge does NOT authorize Phase 3i-A.
- Phase 3i-A merge does NOT authorize Phase 3i-B1.
- Phase 3i-B1 merge does NOT authorize Phase 3j.
- Phase 3j outcome (PROMOTE / HARD REJECT / FRAMEWORK FAIL / MECHANISM FAIL) does NOT automatically authorize V-window run, V-window confirmation, paper/shadow, Phase 4, live-readiness, or deployment.

The staged structure mirrors Phase 3d-A / 3d-B1 / 3d-B2 precedent and preserves operator-decision gating at each phase boundary.

---

## 7. Future implementation test plan

Tests required at the Phase 3i-A and Phase 3i-B1 phases, at minimum. Each test name suggests intent only; the implementer may rename per project convention. Tests are listed as the binding test contract for what any future Phase 3i implementation must cover.

### 7.1 Config and primitive tests (Phase 3i-A scope)

| Test | Validates |
|------|-----------|
| `test_funding_aware_config_locked_defaults` | All locked values from §5.2 are present and read-only (frozen Pydantic model). |
| `test_funding_aware_config_rejects_alternate_threshold` | Pydantic validation rejects `funding_z_score_threshold != 2.0` (or model is frozen / extra=forbid prevents post-instantiation mutation). |
| `test_funding_aware_config_rejects_alternate_target` | `target_r_multiple` cannot be set to 1.0, 1.5, or 3.0; only 2.0 (per Phase 3g §5.6 Option A). |
| `test_funding_aware_config_rejects_alternate_lookback` | `funding_z_score_lookback_days != 90` rejected. |
| `test_funding_aware_config_rejects_alternate_time_stop` | `time_stop_bars != 32` rejected. |
| `test_funding_aware_config_rejects_regime_filter` | `regime_filter` field absent or `None`-only. |
| `test_z_score_uses_trailing_90_days` | `compute_funding_z_score` over 271 events uses events 1..270 for μ/σ at event 271; Z-score formula is `(F_271 − μ) / σ`. |
| `test_z_score_excludes_current_event` | Computing Z-score at event 271 with full series of 271 events does NOT include event 271 itself in μ/σ; mathematically equivalent to leave-one-out at the leading position. |
| `test_z_score_warmup` | Computing Z-score at event 50 with only 49 prior events returns NaN (insufficient warmup). |
| `test_signal_no_signal_below_threshold` | `funding_extreme_event(z_score=1.99, threshold=2.0)` returns None; `z_score=−1.99` returns None. |
| `test_signal_positive_extreme_creates_short` | `funding_extreme_event(z_score=2.0, threshold=2.0)` returns SHORT; `z_score=3.5` returns SHORT. |
| `test_signal_negative_extreme_creates_long` | `funding_extreme_event(z_score=−2.0, threshold=2.0)` returns LONG; `z_score=−3.5` returns LONG. |
| `test_event_alignment_strict_lte` | `align_funding_event_to_bar` uses `funding_time ≤ bar_close_time`; an event with `funding_time > bar_close_time` is excluded. |
| `test_event_alignment_no_lookahead` | At bar 1000 (close at t=t_bar_1000_close), the most recent event used is one with `funding_time ≤ t_bar_1000_close`; events at `t > t_bar_1000_close` are not selectable. |
| `test_per_event_cooldown_consumes_event` | After a position opens on `funding_event_id=E1`, `E1` is marked consumed; same-direction signal on `E1` from later bars is blocked. |
| `test_per_event_cooldown_fresh_event_allows_re_entry` | After position closes on `E1`, a fresh event `E2` with `|Z_F| ≥ 2.0` allows new same-direction entry. |
| `test_per_event_cooldown_opposite_direction_allowed` | At a fresh event `E2` with sign-flipped Z_F, opposite-direction entry is allowed even if `E1` was consumed by the same-direction prior position. |
| `test_compute_stop_long` | LONG: `stop_price = fill_price − 1.0 × atr20`. |
| `test_compute_stop_short` | SHORT: `stop_price = fill_price + 1.0 × atr20`. |
| `test_compute_target_long` | LONG: `target_price = fill_price + 2.0 × stop_distance`. |
| `test_compute_target_short` | SHORT: `target_price = fill_price − 2.0 × stop_distance`. |
| `test_stop_distance_admissibility_band` | `stop_distance / atr20 ∈ [0.60, 1.80]` — D1-A's 1.0 is inside; admissibility check passes. |
| `test_time_stop_horizon_32` | TIME_STOP triggers at `entry_bar_idx + 32`. |
| `test_d1a_strategy_family_enum_value` | `StrategyFamily.FUNDING_AWARE_DIRECTIONAL` exists; value `"FUNDING_AWARE_DIRECTIONAL"`. |
| `test_backtest_config_d1a_dispatch_invariant` | `BacktestConfig(strategy_family=FUNDING_AWARE_DIRECTIONAL, funding_aware_variant=None)` raises ValidationError; `mean_reversion_variant` non-None on D1-A path raises; non-default V1 `strategy_variant` on D1-A path raises. |
| `test_v1_breakout_default_unchanged` | Default `BacktestConfig()` produces a V1_BREAKOUT family config that matches Phase 2e baseline bit-for-bit. |
| `test_f1_dispatch_unchanged` | `BacktestConfig(strategy_family=MEAN_REVERSION_OVEREXTENSION, mean_reversion_variant=MeanReversionConfig())` continues to validate per Phase 3d-B1 invariants unchanged. |
| `test_d1a_phase_3i_a_runtime_guard` | Attempting to dispatch D1-A through the engine in Phase 3i-A raises the documented Phase 3i-A guard error (`"D1-A engine wiring not yet authorized..."`). |

### 7.2 Engine wiring tests (Phase 3i-B1 scope)

| Test | Validates |
|------|-----------|
| `test_d1a_long_entry_at_negative_extreme` | A synthetic series with funding events normalized so `Z_F ≤ −2.0` at event N produces a LONG entry at the next 15m bar open after the next 15m bar close that follows event N. |
| `test_d1a_short_entry_at_positive_extreme` | Symmetric for SHORT. |
| `test_d1a_no_entry_below_threshold` | `Z_F = 1.99` at event N produces no entry on the bar following N (or any subsequent bar before a fresh event). |
| `test_d1a_next_bar_open_fill_timing` | Signal at bar B close → fill at bar B+1 open (not bar B close, not bar B+2). |
| `test_d1a_stop_at_one_atr` | LONG stop = fill_price − 1.0 × ATR(20)(at fill bar B+1); SHORT stop = fill_price + 1.0 × ATR(20). |
| `test_d1a_target_at_two_R` | LONG target = fill_price + 2.0 × stop_distance; SHORT target = fill_price − 2.0 × stop_distance. |
| `test_d1a_stop_never_moves` | Stop price recorded at fill stays constant across the trade lifecycle; no intra-trade stop update is invoked. |
| `test_d1a_target_close_fill` | If price reaches target during a bar, position closes with TARGET exit reason at the bar's close. |
| `test_d1a_stop_close_fill` | If MARK_PRICE reaches stop during a bar, position closes with STOP exit reason. |
| `test_d1a_time_stop_at_close_of_b_plus_1_plus_32` | If neither STOP nor TARGET fires by close of bar `B+1+32`, TIME_STOP triggers at that close. |
| `test_d1a_time_stop_fills_at_open_of_b_plus_1_plus_33` | TIME_STOP exit fills at open of bar `B+1+33`, not at close of B+1+32; no same-close fill. |
| `test_d1a_same_bar_priority_stop_before_target` | If same bar contains both STOP-trigger and TARGET-touch, STOP fires first (tested with synthetic high-volatility bar). |
| `test_d1a_same_bar_priority_target_before_time_stop` | If same bar at index B+1+32 contains both TARGET-touch and TIME_STOP-trigger, TARGET fires first. |
| `test_d1a_per_event_cooldown_blocks_same_direction` | Two consecutive 15m bars referencing the same `funding_event_id` produce only one entry candidate (the first); the second is blocked by cooldown. |
| `test_d1a_per_event_cooldown_releases_on_fresh_event` | After position closes, a new event with `|Z_F| ≥ 2.0` allows a fresh same-direction entry. |
| `test_d1a_event_level_funnel_identity` | After a synthetic run, `funding_extreme_events_detected = funding_extreme_events_filled + funding_extreme_events_rejected_stop_distance + funding_extreme_events_blocked_cooldown`. |
| `test_d1a_event_level_counters_no_bar_inflation` | A single funding event referenced by 32 successive 15m bars increments `funding_extreme_events_detected` by exactly 1 (not 32). |
| `test_d1a_funding_accrual_signed_correctly` | A SHORT trade at extreme positive funding (longs paying shorts) accrues positive `funding_accrual_total_R`; LONG at extreme negative funding accrues positive. Same `apply_funding_accrual` linear-scan invoked. |
| `test_d1a_emits_only_allowed_exit_reasons` | A multi-trade synthetic run produces only STOP / TARGET / TIME_STOP / END_OF_DATA exit reasons; zero TRAILING_BREACH / STAGNATION / TAKE_PROFIT. |
| `test_d1a_no_v1_only_exit_reasons` | Synthetic run produces zero TRAILING_BREACH / STAGNATION exit reasons (V1-only). |
| `test_d1a_no_take_profit_exit_reason` | Synthetic run produces zero TAKE_PROFIT exit reasons (V1-family multi-stage exit reason; D1-A uses TARGET instead). |
| `test_h0_control_unchanged_after_d1a_wiring` | H0 R MED MARK on BTC/ETH reproduces Phase 2e v002 baseline bit-for-bit on all 6 summary metrics (n / WR / expR / PF / netPct / maxDD). |
| `test_r3_control_unchanged_after_d1a_wiring` | R3 R MED MARK on BTC/ETH reproduces Phase 2l v002 baseline bit-for-bit. |
| `test_f1_control_unchanged_after_d1a_wiring` | F1 R MED MARK on BTC/ETH reproduces Phase 3d-B2 baseline bit-for-bit. |
| `test_no_lookahead_funding_event_alignment` | Synthetic test where a funding event at `funding_time = bar_B_close + 1ms` is NOT used at bar B's signal evaluation; only used from bar B+1 onward. |
| `test_z_score_excludes_current_event_at_runtime` | At runtime, the rolling Z-score for event N uses events N−1..N−270 only; event N is not in the sample. |
| `test_d1a_runner_requires_authorization_flag` | The Phase 3i-B1 runner script exits with non-zero status if invoked without `--phase-3X-authorized` (analogous to Phase 3d-B1 `--phase-3d-b2-authorized` precedent). |

This is a **non-exhaustive minimum**. The implementer may add further tests as edge cases are discovered.

---

## 8. Required future quality gates

All four pre-execution gates must be green at the conclusion of any future Phase 3i-A and Phase 3i-B1 phase:

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```

Per Phase 3d-A / 3d-B1 / 3d-B2 / 3g precedent. mypy scope is `src/` only (scripts excluded from mypy default scope per project precedent).

If any gate fails at the conclusion of an implementation phase, the phase must NOT be merged; the failure must be diagnosed and resolved before the next phase boundary.

---

## 9. Required future control reproduction before D1-A interpretation

Per Phase 3c §10.2 / Phase 3d-B2 §4 baseline-preservation precedent, the following V1 and F1 control runs must reproduce locked baselines bit-for-bit on all summary metric cells before any D1-A run is interpreted:

| Control | Window | Slippage | Stop trigger | Required to reproduce |
|---------|--------|----------|--------------|------------------------|
| H0 | R | MED | MARK | Phase 2e v002 baseline (BTC: n=33, WR=30.30%, expR=−0.4590, PF=0.2552, netPct=−3.3917%, maxDD=−3.6745%; ETH: n=33, WR=21.21%, expR=−0.4752, PF=0.3207, netPct=−3.5270%, maxDD=−4.1341%) |
| H0 | V | MED | MARK | Phase 2e v002 baseline (BTC: n=8, expR=−0.3132; ETH: n=14, expR=−0.1735) |
| R3 | R | MED | MARK | Phase 2l v002 baseline (BTC: n=33, WR=42.42%, expR=−0.2403, PF=0.5602, netPct=−1.7743%, maxDD=−2.1592%; ETH: n=33, WR=33.33%, expR=−0.3511, PF=0.4736, netPct=−2.6055%, maxDD=−3.6468%) |
| R3 | V | MED | MARK | Phase 2l v002 baseline (BTC: n=8, expR=−0.2873; ETH: n=14, expR=−0.0932) |
| F1 | R | MED | MARK | Phase 3d-B2 baseline (BTC: n=4720, WR=33.05%, expR=−0.5227, PF=0.3697, netPct=−545.56%, maxDD=−552.74%; ETH: n=4826, WR=33.36%, expR=−0.4024, PF=0.4667) |

Total: 9 control cells × 6 metrics each = 54 metric cells must reproduce bit-for-bit.

**If any control fails to reproduce bit-for-bit, future execution must STOP.** The failure indicates the new D1-A wiring perturbed V1 or F1 dispatch, which is a critical correctness regression. The implementing phase must be diagnosed, the regression fixed, and controls re-verified before any D1-A run is interpreted.

The Phase 3i-A control reproduction set is H0/R3/F1 R-window MED only (5 cells). The Phase 3i-B1 control reproduction set is the full 9-cell V+R set above. The Phase 3j control reproduction set is also the full 9-cell set.

---

## 10. Precommitted D1-A run inventory

### 10.1 Mandatory R-window cells (4 runs per Phase 3j)

Per Phase 3c §6.1 / Phase 3d-B2 §5 precedent:

| # | Variant | Window | Slippage | Stop trigger | Run-dir name suggestion |
|---|---------|--------|----------|--------------|-------------------------|
| 1 | D1-A | R | MEDIUM | MARK_PRICE | `phase-3X-d1a-window=r-slip=medium/...` — **governing first run** |
| 2 | D1-A | R | LOW | MARK_PRICE | `phase-3X-d1a-window=r-slip=low/...` — low-cost sensitivity |
| 3 | D1-A | R | HIGH | MARK_PRICE | `phase-3X-d1a-window=r-slip=high/...` — §11.6 HIGH cost gate |
| 4 | D1-A | R | MEDIUM | TRADE_PRICE | `phase-3X-d1a-window=r-slip=medium-stop=trade_price/...` — stop-trigger sensitivity |

Each run produces `trade_log.parquet` + `summary_metrics.json` + `funding_aware_lifecycle_total.json` + `equity_curve.parquet` + `drawdown.parquet` + `r_multiple_hist.parquet` + `monthly_breakdown.parquet` + `backtest_report.manifest.json` + `config_snapshot.json` per run. All artifacts under git-ignored `data/derived/backtests/`.

### 10.2 Conditional V-window cell (1 run)

Per Phase 3c §6.2 / §11.3 conditional rule:

| # | Variant | Window | Slippage | Stop trigger | Conditional on |
|---|---------|--------|----------|--------------|----------------|
| 5 | D1-A | V | MEDIUM | MARK_PRICE | R-window first-execution gate verdict = PROMOTE |

If the R-window verdict is HARD REJECT / MECHANISM FAIL / FRAMEWORK FAIL (any flavor), the V-window run is **NOT executed**. This preserves the Phase 2f §11.3 V-window no-peeking rule.

### 10.3 Explicitly forbidden runs

The following are explicitly NOT authorized at any future Phase 3j or subsequent phase:

- No D1-A V LOW (only MED MARK conditional V).
- No D1-A V HIGH.
- No D1-A V TRADE_PRICE.
- No D1-A R HIGH TRADE_PRICE.
- No D1-A R LOW TRADE_PRICE.
- No threshold sweep (|Z_F| stays at 2.0).
- No target sweep (TARGET stays at +2.0R per Phase 3g §5.6 Option A).
- No lookback sweep (90 days fixed).
- No time-stop sweep (32 bars fixed).
- No stop-distance sweep (1.0 × ATR(20) fixed).
- No regime-conditional D1-A-prime.
- No D1-B (funding-aware filter on a base directional thesis).
- No V1/D1 hybrid.
- No F1/D1 hybrid.
- No additional symbols (BTCUSDT primary; ETHUSDT research/comparison only per §1.7.3).

Forbidden runs must NOT be executed even as "exploratory" or "calibration" runs. Phase 2f §11.3.5 binding rule: any post-hoc parameter exploration is forbidden.

---

## 11. D1-A first-execution gate

Reproducing Phase 3g §13 verbatim. The gate evaluates D1-A against **self-anchored absolute thresholds**, not vs-H0/R3/F1 deltas.

### 11.1 PROMOTE conditions (all required)

| # | Condition | Cell | Threshold |
|---|-----------|------|-----------|
| (i) | Absolute BTC MED edge | BTC R MED MARK | `expR > 0` |
| (ii) | M1 BTC mechanism | BTC | `mean(counter_displacement_32_R) ≥ +0.10 R` AND `fraction(counter_displacement_32_R ≥ 0) ≥ 50%` |
| (iii) | ETH MED non-catastrophic | ETH R MED MARK | `expR > −0.50` AND `PF > 0.30` |
| (iv-1) | BTC HIGH cost-resilience expR | BTC R HIGH MARK | `expR > 0` |
| (iv-2) | BTC HIGH absolute PF floor | BTC R HIGH MARK | `PF > 0.30` |
| (iv-3) | ETH HIGH non-catastrophic expR | ETH R HIGH MARK | `expR > −0.50` |
| (iv-4) | ETH HIGH non-catastrophic PF | ETH R HIGH MARK | `PF > 0.30` |
| (v-1) | BTC MED absolute floor expR | BTC R MED MARK | `expR > −0.50` |
| (v-2) | BTC MED absolute floor PF | BTC R MED MARK | `PF > 0.30` |
| (v-3) | ETH MED absolute floor expR | ETH R MED MARK | `expR > −0.50` |
| (v-4) | ETH MED absolute floor PF | ETH R MED MARK | `PF > 0.30` |

All conditions must PASS for PROMOTE.

### 11.2 Verdict mapping

| Outcome | Definition | Verdict |
|---------|------------|---------|
| **HARD REJECT** | Any catastrophic absolute-floor violation: `expR ≤ −0.50` OR `PF ≤ 0.30` on either symbol at either MED or HIGH slippage on MARK_PRICE cells. | HARD REJECT — no V-window run; D1-A retained as research evidence only; D1-A family research closed. |
| **MECHANISM FAIL** | M1 BTC FAIL (mean < +0.10 R OR fraction < 50% at h=32) AND no catastrophic floor violation. | MECHANISM FAIL — D1-A retained as research evidence; no V-window run; framework verdict FAILED. |
| **MECHANISM PASS / FRAMEWORK FAIL — §11.6 cost-sensitivity blocks** | M1 BTC PASS AND BTC MED expR > 0 AND ETH MED non-catastrophic AND no catastrophic MED violation, BUT BTC HIGH expR ≤ 0 OR BTC HIGH PF ≤ 0.30 OR ETH HIGH catastrophic. | FRAMEWORK FAIL — §11.6 cost-sensitivity blocks; D1-A retained as research evidence; no V-window run; same precedent as R2. |
| **MECHANISM PASS / FRAMEWORK FAIL — other** | M1 BTC PASS but a non-catastrophic non-§11.6 framework condition fails (e.g., BTC MED expR ≤ 0). | FRAMEWORK FAIL — D1-A retained as research evidence; no V-window run. |
| **PROMOTE** | All §11.1 conditions PASS AND no catastrophic-floor violation. | PROMOTE — V-window run authorized for confirmation; D1-A becomes a candidate-of-record candidate (subject to V-window confirmation per Phase 2f §11.3 no-peeking rule). |

**HARD REJECT supersedes MECHANISM PASS** in the verdict mapping: a catastrophic absolute-floor violation is the binding signal regardless of mechanism evidence (same precedent as F1 / R2).

### 11.3 V-window run conditional rule

If R-window verdict is PROMOTE, the V MED MARK cell may be executed for confirmation. The V-window verdict applies §11.3 V-window no-peeking rule: the V-window evidence is post-execution diagnostic, not a re-evaluation of the gate.

If R-window verdict is anything other than PROMOTE, the V-window cell is NOT executed.

### 11.4 §10.4 absolute floors and §11.6 = 8 bps HIGH preserved

No threshold is loosened. §10.4 absolute floors `expR > −0.50 AND PF > 0.30` apply per symbol per MED / HIGH cell. §11.6 = 8 bps HIGH per side preserved verbatim per Phase 2y closeout / Phase 3e §11 / Phase 3f §11 / Phase 3g §16.

---

## 12. Mechanism checks

### 12.1 M1 — Post-entry directional displacement

**Hypothesis:** Contrarian-funding entries should show favorable post-entry directional displacement at funding-cycle horizons.

**Definition:** For each D1-A trade, compute

```text
counter_displacement_h_R = ((close(entry_bar + h) − fill_price) × trade_direction_sign) / stop_distance
```

where:

- `entry_bar` is the fill bar (i.e., bar B+1, the bar whose open is the next-bar-open fill);
- `fill_price` is the actual next-bar-open fill price;
- `trade_direction_sign = +1` for LONG, `−1` for SHORT;
- `stop_distance` is the per-trade ATR-based stop distance (1.0 × ATR(20) at fill per §6.7).

Horizons: `h ∈ {8, 16, 32}` completed 15m bars (= 2h, 4h, 8h = 1/4, 1/2, full funding cycle).

**PASS criterion at h=32:** `mean(counter_displacement_32_R) ≥ +0.10 R` AND `fraction(counter_displacement_32_R ≥ 0) ≥ 50%`, **per symbol**.

**FAIL:** mean < +0.10 R OR fraction < 50% at h=32.

**PARTIAL:** one of (mean / fraction) PASSES and the other FAILS.

**§11 governance:** M1 BTC at h=32 PASS is required for PROMOTE per §11.1(ii).

### 12.2 M2 — Funding-cost benefit

**Hypothesis:** D1-A's contrarian carry-tailwind should contribute a positive funding-accrual benefit per trade on average that materially offsets fee + slippage cost.

**Definition:** For each D1-A trade, compute `funding_benefit_R = funding_accrual_total_R` (engine field, signed by direction; positive when funding flows to the strategy). Aggregate per symbol: `mean(funding_benefit_R)`.

**PASS criterion:** `mean(funding_benefit_R) ≥ +0.05 R per trade per symbol`.

**FAIL:** `mean(funding_benefit_R) < +0.05 R`.

**PARTIAL:** PASS on one symbol, FAIL on the other.

**§11 governance:** M2 is descriptive; it does NOT gate the §11 verdict.

### 12.3 M3 — TARGET-exit subset positive contribution

**Hypothesis:** D1-A's TARGET-exit subset (trades that reach +2.0 R target before any STOP / TIME_STOP) should produce mean ≥ +0.30 R AND aggregate > 0 per symbol.

**Definition:** Filter D1-A trades to TARGET-exit subset only. Compute `mean(net_R)` and `aggregate(net_R)` per symbol.

**PASS criterion:** `mean(net_R) ≥ +0.30 R` AND `aggregate(net_R) > 0` per symbol.

**FAIL:** mean < +0.30 R OR aggregate ≤ 0.

**PARTIAL:** PASS on one symbol, FAIL on the other.

**§11 governance:** M3 is **descriptive only**. M3 PASS-isolated does NOT promote D1-A. M3 PASS-with-framework-FAIL is research evidence; the §11.2 verdict mapping has HARD REJECT / FRAMEWORK FAIL supersede mechanism PASS, matching F1 / R2 precedent. **M3 cannot rescue a framework fail.** Phase 3e §5.4 / §8.6 + Phase 3f §5.7 + Phase 3g §14 + Phase 3g methodology audit §5.4 prohibitions on target-subset rescue apply.

### 12.4 Combined interpretation

The M1 / M2 / M3 verdicts are **descriptive evidence**, not §11.1-equivalent governing thresholds (with the single exception of M1 BTC at h=32 which is condition §11.1(ii) of the gate). They inform the verdict mapping in §11.2 but do NOT supersede the catastrophic-floor predicate.

A combined M1 PASS + M2 PASS + M3 PASS would be the strongest mechanism evidence; it would still require the §11.1 PROMOTE conditions to clear for framework PROMOTE.

A combined M1 PARTIAL / M2 PARTIAL / M3 PASS-isolated outcome (the F1 precedent at HARD REJECT) would be informative research evidence, but if §11.1 absolute-floor conditions are violated catastrophically, the verdict is HARD REJECT regardless.

---

## 13. Mandatory diagnostics

The following diagnostics must be produced for any future Phase 3j first execution. Per Phase 3g §12 and methodology audit §5.3 amendments. Pattern mirrors Phase 3c §8 / Phase 3d-B2 §12 F1 precedent.

| # | Diagnostic | Description |
|---|------------|-------------|
| 1 | Trade count and frequency | total n; per-month / per-week / per-day rates |
| 2 | Long/short split | count of LONG / SHORT entries; LONG % of total |
| 3 | Funding-signal distribution | distribution of `Z_F` at signal events; mean, median, p25, p75, min, max |
| 4 | Funding-rate-at-entry distribution | distribution of `funding_rate` (raw, not Z-scored) at signal events |
| 5 | Funding-event counts | total count of detected funding events with `|Z_F| ≥ 2.0`; per-symbol |
| 6 | Per-funding-regime performance | partition trades by funding-regime tercile (low / mid / high terciles of `|Z_F|`); per-tercile expR / PF / n |
| 7 | Per-volatility-regime performance | partition trades by trailing 1000-bar 1h ATR(20) percentile-rank tercile (Phase 2l §6.1 / Phase 2w §11.9 / Phase 3c §9.2 classifier); per-tercile expR / PF / n |
| 8 | Per-fold consistency | 6 half-year folds (2022H1 / 2022H2 / 2023H1 / 2023H2 / 2024H1 / 2024H2); per-fold n / expR / PF |
| 9 | Exit-reason fractions | STOP / TARGET / TIME_STOP / END_OF_DATA percentages |
| 10 | **mean_R_by_exit_reason** | Per-exit-reason mean R (per Phase 3g methodology audit §5.3 — central to TIME_STOP-subset interpretation) |
| 11 | **aggregate_R_by_exit_reason** | Per-exit-reason aggregate R (per Phase 3g methodology audit §5.3) |
| 12 | TIME_STOP subset mean and aggregate R | Standalone; expected to drive the framework verdict at +2.0R target |
| 13 | Funding-accrual contribution | `mean(funding_accrual_total_R)` per trade per symbol; partition by exit reason |
| 14 | Fee/slippage/funding decomposition | per-trade decomposition of net R into gross-R, fee component, slippage component, funding-accrual component |
| 15 | LOW/MED/HIGH cost sensitivity | execute four cells (R LOW MARK / R MED MARK / R HIGH MARK / R MED TRADE_PRICE per §10.1); report per-symbol expR / PF / netPct / maxDD per cell |
| 16 | Mark-price vs trade-price stop-trigger sensitivity | Compare R MED MARK vs R MED TRADE_PRICE outcomes |
| 17 | MFE/MAE distribution | Maximum Favorable / Adverse Excursion per trade in R-multiples; mean, p25, median, p75, p95 |
| 18 | Stop-distance distribution | Empirical `stop_distance_atr` distribution; should be 1.0 by construction with zero variance |
| 19 | Hold-time distribution | bars-held per trade; mean, median, p25, p75, max. By construction max ≤ 32 |
| 20 | Target reachability / TARGET fraction | Empirical TARGET-exit fraction; expected 5–20% per Phase 3g §5.6.5 tradeoff analysis |
| 21 | Funding-window alignment checks | Verify that funding event used at each entry signal is the most-recent-completed-prior-to-bar-close, with no off-by-one and no lookahead. Check that no signal fires using a funding event whose `funding_time > bar_close_time` |
| 22 | BTC/ETH comparison | Side-by-side per-symbol summaries for all metrics above |
| 23 | H0/R3/F1 descriptive references | H0 / R3 / F1 control runs at MED MARK provide cross-family context. **Descriptive only** per Phase 3g §13.1 / Phase 3d-B2 §15 precedent; not §10.3-equivalent governing metrics |
| 24 | **RR / breakeven realized-vs-expected review** | Compare empirical winner net R / loser net R / breakeven WR to Phase 3g §5.6 RR/target sanity expected values (winner ~+1.47R MED / +1.14R HIGH; breakeven WR ~51% MED / ~62% HIGH without funding); flag material deviations as evidence of fee/slippage/funding modeling drift |

---

## 14. P.14-style hard-block checks

Before any future Phase 3j verdict is issued, the following hard-block invariants must all PASS. If ANY check fails, future execution must STOP and no verdict may be issued. Per Phase 3c §8.15 / Phase 3d-B2 §13 / Phase 3g §12 precedent.

| # | Invariant | Check |
|---|-----------|-------|
| 1 | D1-A emits only allowed exit reasons | STOP / TARGET / TIME_STOP / END_OF_DATA only |
| 2 | Zero V1 / multi-stage exit reasons | Zero TRAILING_BREACH / STAGNATION / TAKE_PROFIT in any D1-A trade log |
| 3 | Exit-reason accounting identity | `STOP + TARGET + TIME_STOP + END_OF_DATA = n` per symbol |
| 4 | Funding-event-level funnel identity | `funding_extreme_events_detected = funding_extreme_events_filled + funding_extreme_events_rejected_stop_distance + funding_extreme_events_blocked_cooldown` per symbol per cell |
| 5 | No bar-level inflation of detected counts | Repeated 15m bars referencing the same `funding_event_id` do NOT increment `funding_extreme_events_detected` more than once |
| 6 | Stop-distance band [0.60, 1.80] enforcement | All filled trades have `stop_distance_atr ∈ [0.60, 1.80]`; D1-A is 1.0 by construction so observed `min ≈ 1.0 ≈ max` |
| 7 | Stop never moves intra-trade | The engine must never invoke `_apply_stop_update` (or equivalent) on the D1-A path |
| 8 | Target remains +2.0R | Empirical `entry_to_target_distance_atr / stop_distance_at_signal_atr = 2.0` for all filled trades |
| 9 | TIME_STOP trigger/fill timing | TIME_STOP triggers at close of bar `B+1+32`; fills at open of bar `B+1+33`; no same-close fill |
| 10 | Same-bar precedence | `STOP > TARGET > TIME_STOP` evaluated per Phase 3b §6 / Phase 3d-A precedent |
| 11 | Cooldown enforcement | No same-event same-direction re-entry; verified by funnel counter `funding_extreme_events_blocked_cooldown > 0` if any same-event re-entry attempts occurred |
| 12 | No look-ahead in funding-event alignment | Funding event used at signal must satisfy `funding_time ≤ bar_close_time`; no event with `funding_time > bar_close_time` is referenced |
| 13 | Rolling 90-day Z-score excludes current event | μ_F and σ_F at event N are computed over events N−1..N−270; event N is not in the sample |
| 14 | M1 displacement uses fill_price | Post-entry displacement formula uses `fill_price` (next-bar-open fill price), not `close(B+1)` |
| 15 | H0 / R3 / F1 controls reproduce bit-for-bit | All 9 control cells reproduce locked baselines on all summary metrics before D1-A interpretation |

---

## 15. Reporting plan for future phases

Each future phase produces required Markdown reports under `docs/00-meta/implementation-reports/`. Pattern mirrors Phase 3d-A / 3d-B1 / 3d-B2 / 3e / 3f / 3g precedent.

### 15.1 Phase 3i-A reports (if authorized)

- `<DATE>_phase-3i-A_D1A_implementation-controls.md` — checkpoint report with code surface summary, quality-gate output, control reproduction (5 cells: H0/R3/F1 R MED MARK), test count delta, files changed.
- `<DATE>_phase-3i-A_closeout-report.md` — closeout report with branch / git status / files changed / commit hashes / docs-only confirmation / preservation confirmation.
- `<DATE>_phase-3i-A_merge-report.md` — merge report after operator-authorized merge into main.

### 15.2 Phase 3i-B1 reports (if authorized)

- `<DATE>_phase-3i-B1_D1A_engine-wiring.md` — checkpoint report with engine surface summary, lifecycle counter introduction, output field additions, full 9-cell control reproduction (H0/R3/F1 × R-V × MED MARK), test count delta, runner scaffold under `--phase-3X-authorized` hard guard.
- `<DATE>_phase-3i-B1_closeout-report.md` — closeout report.
- `<DATE>_phase-3i-B1_merge-report.md` — merge report.

### 15.3 Phase 3j reports (if authorized after Phase 3i-B1 merges)

- `<DATE>_phase-3j_D1A_execution-diagnostics.md` — primary execution-diagnostics report with run inventory, summary metrics, first-execution gate evaluation, M1 / M2 / M3 mechanism checks, §13 mandatory diagnostics, §14 P.14 hard-block check results, verdict (PROMOTE / HARD REJECT / FRAMEWORK FAIL / MECHANISM FAIL).
- `<DATE>_phase-3j_closeout-report.md` — closeout report.
- `<DATE>_phase-3j_merge-report.md` — merge report.

### 15.4 Reporting discipline

This is **planning only**. No report is authorized to be produced before its corresponding phase is operator-authorized. Phase 3h does not authorize Phase 3i-A; Phase 3i-A merge does not authorize Phase 3i-B1; Phase 3i-B1 merge does not authorize Phase 3j.

Each phase's checkpoint and closeout reports must explicitly preserve the project state per Phase 3g §16 / Phase 3h §16 precedent: no threshold change; no project-lock change; no paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write proposal; no MCP / Graphify / `.mcp.json`; no credentials; no `data/` commits.

---

## 16. Explicit project-state preservation

Phase 3h is docs-only and explicitly preserves all of the following verbatim:

- **No threshold changes.** Phase 2f §10.3 / §10.4 / §11.3 / §11.4 / **§11.6 = 8 bps HIGH per side** preserved verbatim per Phase 2f §11.3.5 / Phase 2y closeout / Phase 3e §11 / Phase 3f §11 / Phase 3g §16.
- **No strategy-parameter changes outside the already-merged Phase 3g D1-A spec.** D1-A locked spec (signal threshold |Z_F| ≥ 2.0; 90-day lookback; 1.0 × ATR(20) stop; +2.0R TARGET; 32-bar time-stop; per-funding-event cooldown; symmetric direction; no regime filter; recorded exit reason TARGET; STOP > TARGET > TIME_STOP) is consumed unmodified from Phase 3g. R3 / H0 / R1a / R1b-narrow / R2 / F1 sub-parameters all preserved verbatim.
- **No project-lock changes.** §1.7.3 locks (BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; one active protective stop max; 0.25% risk per trade; 2× leverage cap; mark-price stops; v002 datasets; one-way mode; isolated margin; no pyramiding; no reversal while positioned; no hedge mode) preserved verbatim.
- **No paper/shadow planning is authorized.** Phase 3e §11 / Phase 3f §11 / Phase 3g §16 deferral stands.
- **No Phase 4 (runtime / state / persistence) is authorized.** Phase 3e §11 / Phase 3f §11 / Phase 3g §16 deferral stands.
- **No live-readiness work is authorized.** No deployment, no exchange-write capability, no production keys.
- **No deployment work is authorized.**
- **No credentials.** No production / sandbox / testnet API keys requested, created, or used. No `.env` file modified. No secrets in any committed file.
- **No MCP / Graphify / `.mcp.json` activation.** No MCP server enabled; no Graphify integration; no `.mcp.json` file created or modified.
- **No exchange-write paths.** No exchange-write capability proposed, implemented, or enabled. `BacktestAdapter.FAKE` remains the only adapter type in the engine.
- **No `data/` commits.** Phase 3h commits are limited to two `docs/00-meta/implementation-reports/` files.
- **No code change.** No file in `src/`, `tests/`, `scripts/`, `.claude/` is touched by Phase 3h.
- **No implementation.** Phase 3i-A is NOT authorized by Phase 3h.
- **No execution.** Phase 3j is NOT authorized by Phase 3h.
- **No Phase 3i authorization.** Phase 3i-A requires a separately-authorized operator decision after Phase 3h merges.
- **No existing-spec change.** `v1-breakout-strategy-spec.md`, `v1-breakout-validation-checklist.md`, `cost-modeling.md`, `backtesting-principles.md`, `phase-gates.md`, `technical-debt-register.md`, `data-requirements.md`, `dataset-versioning.md`, `current-project-state.md`, `ai-coding-handoff.md` all preserved.
- **R3 remains V1 breakout baseline-of-record** per Phase 2p §C.1.
- **H0 remains the formal V1 breakout framework anchor** per Phase 2i §1.7.3.
- **R1a / R1b-narrow / R2 / F1 remain retained as research evidence only.** R2 framework verdict FAILED — §11.6 cost-sensitivity blocks. F1 framework verdict HARD REJECT. Phase 3d-B2 terminal for F1.
- **D1-A spec preserved per Phase 3g.** Locked axes binding.

---

## 17. Recommendation

**Recommended next operator decision: authorize Phase 3i-A implementation-control only.**

Rationale:

- Phase 3g methodology sanity audit found Phase 3g safe to merge and recommended GO (provisional) for a future Phase 3h execution-planning memo (which is this memo).
- Phase 3h produces a Phase-3c-style execution-planning memo with precommitted run inventory, first-execution gate, mechanism checks, mandatory diagnostics, and P.14 hard-block invariants. The plan is concrete enough to begin implementation but does not authorize any execution.
- Phase 3i-A is the natural next step: implementation of D1-A primitives + config + tests + control reproduction with deliberate non-runnability (analogous to Phase 3d-A precedent). This carries low risk: no D1-A backtest is run; H0/R3/F1 controls are verified bit-for-bit; the implementation can be reverted cleanly if the operator changes course.
- Phase 3i-A merge does NOT authorize Phase 3i-B1 (engine wiring); Phase 3i-B1 merge does NOT authorize Phase 3j (candidate runs + first-execution gate). Each subsequent phase requires its own separately-authorized operator decision.

Alternative recommendations the operator may select:

- **Remain paused** at the post-Phase-3h plan boundary. Phase 3e §9 default-primary remains a valid posture; Phase 3h does not require an active path. The operator may legitimately prefer to preserve the project state at the post-Phase-3g spec-plus-plan boundary indefinitely.
- **Authorize an alternative direction** consistent with Phase 3f §7 enumeration (e.g., D7 external execution-cost evidence review; or a different operator-driven docs-only direction).
- **Hold for operator strategic choice** without explicit re-authorization. The project state remains at the post-Phase-3h plan boundary until the operator decides.

Phase 3h does **not** recommend:

- Direct execution (Phase 3j without Phase 3i-A and Phase 3i-B1 first).
- Paper/shadow planning (forbidden by operator policy).
- Phase 4 (runtime / state / persistence) work (forbidden).
- Live-readiness / deployment / production-key / exchange-write work (forbidden).
- D1-A-prime / D1-B / V1/D1 / F1/D1 hybrid / target-subset rescue (forbidden by Phase 3g §14 + methodology audit §5.4).
- Threshold revision (forbidden by Phase 2f §11.3.5).
- §1.7.3 lock revision (operator-policy territory; outside Phase 3h scope).

The recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

**End of Phase 3h D1-A execution-planning memo.** Phase 3h produces a Phase-3c-style docs-only execution-planning memo reproducing the Phase 3g binding D1-A spec, defining the data and feature plan (v002 sufficient; one new derived dataset `funding_aware_features__v001`), the implementation architecture plan (`StrategyFamily.FUNDING_AWARE_DIRECTIONAL` enum + `FundingAwareConfig` + `prometheus.strategy.funding_aware_directional` module + `BacktestEngine._run_symbol_d1a` dispatch + TradeRecord field additions + event-level lifecycle counters), the staged Phase 3i-A / 3i-B1 / 3j implementation split recommendation, the future implementation test plan (config + primitive + engine wiring tests; ~50 tests minimum), the required quality gates and 9-cell H0/R3/F1 control reproduction, the precommitted run inventory (4 mandatory R-window cells + 1 conditional V cell; explicitly forbidden runs enumerated), the first-execution gate (analogous to Phase 3c §7.2 F1 gate; §10.4 absolute floors and §11.6 = 8 bps HIGH per side preserved verbatim; BTC HIGH PF > 0.30 explicit at gate level per Phase 3g first amendment), M1 / M2 / M3 mechanism checks, mandatory diagnostics, §14 P.14 hard-block invariants, and the reporting plan for future phases. **Recommended next operator decision: authorize Phase 3i-A implementation-control only.** Phase 3i-A NOT authorized by Phase 3h. Phase 3j (candidate runs + first-execution gate) NOT authorized by Phase 3h. R3 baseline-of-record / H0 framework anchor / R1a-R1b-narrow-R2-F1 retained-research-evidence preserved verbatim. F1 HARD REJECT preserved; Phase 3d-B2 terminal for F1 preserved. §11.6 = 8 bps HIGH per side preserved verbatim. §1.7.3 locks preserved verbatim. D1-A locked spec preserved per Phase 3g. No paper/shadow, no Phase 4, no live-readiness, no deployment, no implementation, no execution, no backtest, no parameter tuning, no threshold change, no project-lock change, no MCP / Graphify / `.mcp.json`, no credentials, no `data/` commits, no code change. No next phase started. Awaiting operator review.
