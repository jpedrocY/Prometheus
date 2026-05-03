# Phase 4q — G1 Backtest-Plan Memo

**Authority:** Operator authorization for Phase 4q (Phase 4p §"Operator decision menu" Option A primary recommendation: Phase 4q — G1 Backtest-Plan Memo, docs-only). Phase 4p (G1 Strategy Spec Memo); Phase 4o (G1 hypothesis-spec memo); Phase 4n (Candidate B selection); Phase 4m (18-requirement fresh-hypothesis validity gate; forbidden-rescue observations); Phase 4l (V2 backtest execution Verdict C HARD REJECT — terminal for V2 first-spec; root-cause forensic numbers explicitly forbidden as G1 design inputs); Phase 4k (V2 backtest-plan methodology — methodological template); Phase 4j §11 (metrics OI-subset partial-eligibility binding rule, preserved but unused by G1 first spec); Phase 4i (V2 acquisition + integrity validation); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 3r §8 (mark-price gap governance); Phase 3t §12 (validity gate); Phase 3c §7.3 (catastrophic-floor predicate); Phase 2p §C.1 (R3 baseline-of-record); Phase 2i §1.7.3 (project-level locks); `docs/03-strategy-research/v1-breakout-strategy-spec.md`; `docs/03-strategy-research/v1-breakout-backtest-plan.md`; `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`; `docs/04-data/data-requirements.md`; `docs/04-data/timestamp-policy.md`; `docs/04-data/dataset-versioning.md`; `docs/04-data/live-data-spec.md`; `docs/07-risk/stop-loss-policy.md`; `docs/07-risk/position-sizing-framework.md`; `docs/07-risk/exposure-limits.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/ai-coding-handoff.md`; `docs/00-meta/implementation-ambiguity-log.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4q — **G1 Backtest-Plan Memo** (docs-only). Translates the locked Phase 4p G1 strategy spec into a precise, reproducible, fail-closed *future* backtest methodology. **Phase 4q does NOT run a G1 backtest, write G1 backtest code, modify scripts, acquire data, modify data, modify manifests, modify `src/prometheus/`, modify tests, create a runnable strategy, start Phase 4r, or authorize paper / shadow / live / exchange-write.** **Phase 4q is text-only.**

**Branch:** `phase-4q/g1-backtest-plan-memo`. **Memo date:** 2026-05-03 UTC.

---

## Summary

Phase 4q predeclares, before any G1 backtest code or G1 backtest execution exists, the complete future Phase 4r methodology: data inputs and manifest handling; standalone-script boundary; exact command shape; data-loading rules; feature computation algorithms; regime-classifier implementation; regime-state-machine implementation; signal-generation implementation; entry / exit simulation; cost / funding model; position-sizing / exposure rules; threshold-grid handling for the locked Phase 4p 32-variant grid (= 2^5) over the five binary axes; M1 / M2 / M3 / M4 mechanism-check implementation plans with the Phase 4p numeric thresholds; PBO / deflated Sharpe / CSCV plan; chronological train / validation / OOS holdout windows reused verbatim from Phase 4k; BTCUSDT-primary / ETHUSDT-comparison protocol; 12 catastrophic-floor predicates with G1-specific evaluation rules; verdict taxonomy; required reporting tables; required plots; stop conditions; reproducibility requirements; what a future Phase 4r may create; what this memo explicitly does not authorize. The plan is the methodological mirror of Phase 4k applied to the Phase 4p G1 strategy spec, narrowed by G1's smaller (32 vs. 512) variant grid and broadened by G1's explicit regime-state-machine plus negative-test framework.

**Phase 4q is the methodology-predeclaration layer.** The future Phase 4r — G1 Backtest Execution (docs-and-code) is *recommended primary* but **not authorized by this memo**. Phase 4r execution would require a separate explicit operator authorization brief.

## Authority and boundary

- **Authority granted:** docs-only Phase 4q memo creation; future Phase 4r predeclaration; operator decision menu; recommendation to remain paused or to authorize Phase 4r separately.
- **Authority NOT granted:** running G1 backtest; writing G1 backtest code; creating `scripts/phase4r_g1_backtest.py`; modifying any source / test / script / data / manifest; revising any retained verdict; revising any project lock; revising Phase 4p / 4j §11 / 4k / 3v §8 / 3w §6 / §7 / §8 / 3r §8 governance; starting Phase 4r or any successor phase; authorizing paper / shadow / live / exchange-write / production keys / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials.
- **Hard rule:** Phase 4q is text-only. No code is written. No data is touched. No backtest is run.
- **Naming hard rule:** Phase 4q methodology must always refer to G1 — Regime-First Breakout Continuation. Any drift toward names like V3, V2-prime, R3-prime, R1c, R1a-extension, R1b-extension, G1-prime, G1-narrow, or any other rescue-implying label is forbidden.

## Starting state

```text
Branch (Phase 4q):   phase-4q/g1-backtest-plan-memo
main / origin/main:  521915d1ba6fc9c58363dadcd70c99308b1ea1df (unchanged)
Phase 4p memo:       50d40da2ef434c7c21c5d0e9d4270d6b4304e0c7 (merged)
Phase 4p closeout:   20b577be2a291fd0ad3c0beb42e627e112f78fdd (merged)
Phase 4p correction: 0572c1c1ab1282b69df04f02b97b97fec6edd877 (merged)
Phase 4p merge:      ddfaf0f579d1c2ed99da0abc6480ee79496b6240 (merged)
Working-tree state:  clean (no tracked modifications); only gitignored
                     transients .claude/scheduled_tasks.lock and
                     data/research/ are untracked and will not be committed.
Quality gates:       ruff check . PASSED; pytest 785 PASSED;
                     mypy strict 0 issues across 82 source files
                     (verified again at Phase 4q creation time).
```

## Relationship to Phase 4p

- Phase 4p **created the complete G1 strategy spec** including timeframes, regime classifier, regime state machine, inside-regime breakout setup, structural stop, target / time-stop, position sizing, cost model, 32-variant threshold grid over five binary axes, M1 / M2 / M3 / M4 numeric thresholds, 12 catastrophic-floor predicates, validation windows, governance labels, and data-requirements decision.
- Phase 4p **did NOT authorize** backtesting, implementation, data acquisition, paper / shadow / live, or exchange-write.
- The operator now **explicitly authorizes Phase 4q only**. Phase 4q is docs-only.
- **Phase 4q must NOT** run the G1 backtest or write the script. Phase 4q is the plan; Phase 4r (if ever authorized) would be the execution.
- **Phase 4q must NOT** modify or weaken any Phase 4p selection. The 32-variant grid, the five binary axes, the fixed parameters (`N_R = 2.0`; `T_stop = 16`; `N_breakout = 12`; `B_atr = 0.10`; `N_stop = 12`; `S_buffer = 0.10`; stop-distance bounds [0.50, 2.20] × ATR(20); `C_cooldown = 4`; risk fraction 0.25%; leverage cap 2×; one position max) are immutable absent a separately authorized governance amendment.
- **Phase 4q must NOT** activate `N_R ∈ {2.0, 2.5}` or `T_stop ∈ {12, 16}` as backtest axes. They remain future G1-extension possibilities only.

## Backtest purpose

The future Phase 4r G1 backtest is a **research-only test** of:

- whether G1's **regime-first breakout** hypothesis has evidence under the §11.6 HIGH cost gate (8 bps slippage per side; taker fee 4 bps per side; funding included);
- whether **`regime_active` periods outperform `regime_inactive` periods** (M1 negative test) by at least +0.10R mean_R differential with bootstrap 95% CI lower bound > 0;
- whether **regime-gated breakout outperforms always-active breakout** (M2 value-add) by at least +0.05R under HIGH cost with bootstrap 95% CI lower bound > 0;
- whether **inside-regime stop / target / sizing co-design produces adequate OOS trade count and positive expectancy** on BTCUSDT (M3: BTC OOS HIGH mean_R > 0 AND trade_count ≥ 30 AND no CFP-1 / CFP-2 / CFP-3 trigger);
- whether **BTCUSDT primary results are directionally supported by ETHUSDT comparison** (M4: ETH non-negative differential, directional consistency; ETH cannot rescue BTC);
- whether G1 survives **§11.6 HIGH cost** verbatim.

**Explicitly:**

- The future backtest is **not implementation**.
- The future backtest is **not paper-readiness**.
- The future backtest is **not live-readiness**.
- The future backtest does **not authorize exchange-write**.
- A pass verdict (Verdict A) only certifies G1 as **research-promotable**; subsequent paper / shadow / live readiness requires separate phase gates per `docs/12-roadmap/phase-gates.md`.

## Backtest non-goals

The future Phase 4r G1 backtest is **NOT**:

- a discovery exercise (the hypothesis is locked at Phase 4p; no new hypotheses are generated);
- a parameter-tuning exercise (thresholds are predeclared; no outcome-driven threshold selection);
- a rescue exercise (no V2 / F1 / D1-A / R2 rescue; no choosing thresholds from Phase 4l forensic numbers);
- a regime-classifier-discovery exercise (the classifier is predeclared at Phase 4p);
- a multi-symbol-portfolio exercise (BTCUSDT primary; ETHUSDT comparison only; same 32 variants per symbol independently);
- a 5m strategy / hybrid (5m diagnostic findings Q1–Q7 forbidden as features or regime indicators);
- a mark-price-stop validation exercise (`stop_trigger_domain` = `trade_price_backtest` for research; `mark_price_runtime` only applies to a future runtime path that this phase does not authorize);
- a paper / shadow / live test;
- an exchange-write test;
- an authentication / private-endpoint / user-stream / WebSocket exercise;
- a data-acquisition exercise (existing v002 / Phase 4i datasets reused; no new data acquired).

## G1 strategy-spec recap

The Phase 4p G1 strategy spec is the binding source. Phase 4q must not modify it. Recap:

```text
Strategy name:       G1 — Regime-First Breakout Continuation
32 variants total (= 2^5)
5 binary axes:
  1. E_min          in {0.30, 0.40}
  2. ATR band       in {[20, 80], [30, 70]}
  3. V_liq_min      in {0.80, 1.00}
  4. funding band   in {[15, 85], [25, 75]}
  5. K_confirm      in {2, 3} 4h bars

Fixed parameters (cardinality 1; not axes):
  N_breakout                = 12
  B_atr                     = 0.10
  N_stop                    = 12
  S_buffer                  = 0.10
  stop-distance bounds      = [0.50, 2.20] x ATR(20)
  N_R                       = 2.0
  T_stop                    = 16 completed 30m bars
  C_cooldown                = 4 completed 4h bars
  HTF EMA pair              = (20, 50) on 4h
  HTF slope-rising lookback = 3 4h bars
  Trend-persistence lookback= 12 4h bars
  Volatility ATR period     = 20 30m bars
  Volatility percentile lb  = 480 30m bars
  Liquidity median lookback = 480 30m bars
  Funding lookback          = 90 events
  risk_fraction             = 0.0025  (0.25% per trade)
  max_leverage              = 2.0     (2x cap)
  max_positions             = 1

Symbol scope:
  primary    = BTCUSDT
  comparison = ETHUSDT (cannot rescue BTC)

Cost model:
  LOW    = 1 bp slippage per side
  MEDIUM = 4 bps slippage per side
  HIGH   = 8 bps slippage per side  (§11.6 promotion gate; preserved verbatim)
  taker fee = 4 bps per side
  funding cost included in P&L
  no maker rebates
  no live fee assumption

Stop-trigger-domain governance label = trade_price_backtest (research)
break_even_rule       = disabled
ema_slope_method      = discrete_comparison
stagnation_window_role= metric_only
mixed_or_unknown      = invalid; fail-closed at every governance-relevant
                        decision boundary
```

**G1 first-spec does NOT use:**

- Phase 4i metrics OI subset (Phase 4j §11 governance preserved verbatim but unused);
- optional metrics ratio columns (Phase 4j §11.3 forbidden);
- 5m Q1–Q7 diagnostic findings as features or regime indicators;
- mark-price 30m / 4h / 5m / 15m;
- aggTrades;
- spot data;
- cross-venue data;
- private / authenticated / public-endpoint-in-code / user-stream / WebSocket / listenKey lifecycle.

## Data inputs and manifest handling

Future Phase 4r must use **exactly** the following manifests and data inputs:

```text
v002 (research-eligible per the locked v002 retained-evidence trade range):
  binance_usdm_btcusdt_15m__v002          (fallback / sanity only)
  binance_usdm_ethusdt_15m__v002          (fallback / sanity only)
  binance_usdm_btcusdt_1h__v002           (or 1h derived from 15m;
                                           must match v002 1h-derivation rule)
  binance_usdm_ethusdt_1h__v002           (or 1h derived from 15m)
  binance_usdm_btcusdt_funding__v002
  binance_usdm_ethusdt_funding__v002

Phase 4i (research-eligible per Phase 4i):
  binance_usdm_btcusdt_30m__v001
  binance_usdm_ethusdt_30m__v001
  binance_usdm_btcusdt_4h__v001
  binance_usdm_ethusdt_4h__v001
```

Manifest handling rules (binding):

1. Future Phase 4r **must read** each used manifest from `data/manifests/` at startup and **pin its SHA256** in `manifest_references.csv` (see "Required reporting tables").
2. Future Phase 4r **must verify** `research_eligible: true` for each used manifest. If `research_eligible: false`, fail closed via stop condition.
3. Future Phase 4r **must verify** for each underlying parquet file that the file SHA matches the manifest-recorded SHA. If mismatch, fail closed.
4. Future Phase 4r **must NOT** modify any manifest.
5. Future Phase 4r **must NOT** create any new manifest.
6. Future Phase 4r **must NOT** acquire data.
7. Future Phase 4r **must NOT** write to `data/raw/`, `data/normalized/`, or `data/manifests/`.
8. Future Phase 4r **must NOT** patch / forward-fill / interpolate / regenerate / replace data.
9. Future Phase 4r **must NOT** load any manifest not on the binding list above. Loading any other manifest = stop condition (CFP-12 forbidden data access).
10. Future Phase 4r **must NOT** load Phase 4i metrics manifests. Metrics OI is NOT a G1 first-spec input.

## Future script boundary

Predeclared future script path:

```text
scripts/phase4r_g1_backtest.py
```

Future script must:

- be a **standalone research script** only;
- **not** import `prometheus.runtime.*`;
- **not** import `prometheus.execution.*`;
- **not** import `prometheus.persistence.*`;
- **not** import any exchange adapter (real or fake);
- **not** import the existing `prometheus.research.data.*` modules unless those imports are read-only and confined to Parquet / DuckDB loaders that touch only the binding manifest list above;
- **not** use any network I/O;
- **not** import `requests`, `httpx`, `aiohttp`, `urllib3`, `urllib.request`, `websockets`, `websocket`, or any other network-capable library;
- **not** read `.env` files;
- **not** access credentials;
- **not** contact Binance APIs (public or private);
- **not** contact any exchange API;
- **not** consult `data.binance.vision` (the public bulk archive) at runtime;
- **not** write to `data/raw/`, `data/normalized/`, or `data/manifests/`;
- **only** write gitignored local research outputs under `data/research/phase4r/`.

Pure runtime stack expectation (mirroring Phase 4l): `pyarrow` + `numpy` + `stdlib`. If `pandas` is added, it must be justified in the Phase 4r execution brief.

**Phase 4q must NOT create the script.** Phase 4q only predeclares its boundary. Any deviation in a future Phase 4r execution brief from this boundary is a stop condition.

## Future command shape

Predeclared exact future command shape (Windows / bash invocation; preserved verbatim across the v002 / Phase 4i date range):

```text
.venv/Scripts/python scripts/phase4r_g1_backtest.py \
  --start 2022-01-01 \
  --end 2026-03-31 \
  --train-start 2022-01-01 \
  --train-end 2023-06-30 \
  --validation-start 2023-07-01 \
  --validation-end 2024-06-30 \
  --oos-start 2024-07-01 \
  --oos-end 2026-03-31 \
  --symbols BTCUSDT ETHUSDT \
  --primary-symbol BTCUSDT \
  --comparison-symbol ETHUSDT \
  --output-dir data/research/phase4r \
  --rng-seed 202604300
```

If a future Phase 4r execution brief differs from this command shape, the brief must justify the deviation explicitly (e.g., adding `--cscv-subsamples 16`; reducing OOS-end to `2026-03-31` is fixed). Adding flags that activate forbidden inputs (mark-price, aggTrades, metrics OI, optional ratio columns, 5m diagnostic outputs as features) is a stop condition.

## Data-loading plan

Predeclared loaders (must use **explicit column lists**; no `select_all`):

```text
30m klines      (Phase 4i): columns = [open_time, open, high, low,
                                        close, volume, close_time]
4h  klines      (Phase 4i): columns = [open_time, open, high, low,
                                        close, volume, close_time]
1h  klines      (v002):     columns = [open_time, open, high, low,
                                        close, volume, close_time]
15m klines      (v002):     columns = [open_time, open, high, low,
                                        close, volume, close_time]
                            (loaded only as fallback / sanity if needed;
                             not a G1 primary feature input)
funding         (v002):     columns = [funding_time, funding_rate, symbol]
```

Loader rules (binding):

1. **No metrics OI loading.** Loading `binance_usdm_btcusdt_metrics__v001` or `binance_usdm_ethusdt_metrics__v001` = stop condition (CFP-12).
2. **No optional ratio columns.** Loading any of `count_toptrader_long_short_ratio`, `sum_toptrader_long_short_ratio`, `count_long_short_ratio`, `sum_taker_long_short_vol_ratio` = stop condition (CFP-10).
3. **No mark-price loading.** Loading any `*_markprice_*` manifest = stop condition (CFP-12).
4. **No aggTrades loading.** Loading any `*_aggTrades_*` source = stop condition (CFP-12).
5. **No spot / cross-venue loading.** Loading any non-Binance-USDⓈ-M futures source = stop condition (CFP-12).
6. **No 5m diagnostic-output loading as features.** The Phase 3s Q1–Q7 outputs MUST NOT be features or regime indicators. Reading them for any other purpose is also forbidden in Phase 4r.
7. **No network access.** All loads come from local Parquet under `data/normalized/` paths recorded in the manifest references.
8. Stable sort on every loaded frame: `(symbol, interval, open_time)` ascending. Duplicate `open_time` rows = stop condition.
9. Timestamp policy: UTC milliseconds, integer; bar identity = `(symbol, interval, open_time)`. Mismatch with `docs/04-data/timestamp-policy.md` = stop condition.
10. Completed-bar discipline: any bar consumed for strategy decisioning must satisfy `close_time <= now_decision`. The "now_decision" point in a backtest is the strategy evaluation moment; partial bars are excluded by construction.

## Feature computation plan

Predeclared exact algorithms (binding for future Phase 4r):

### EMA(20) and EMA(50) on completed 4h close

```text
EMA_n(t) = (close_4h[t] * (2/(n+1))) + (EMA_n(t-1) * (1 - 2/(n+1)))
seed     = SMA over the first n completed 4h bars in the available range
```

Both `EMA_20_4h` and `EMA_50_4h` are computed on completed 4h bars only.

### EMA20 discrete slope-rising state

```text
slope_rising_4h(t) :=  EMA_20_4h[t] > EMA_20_4h[t-3]
                       (3 completed 4h bars earlier;
                        Phase 3w §7 ema_slope_method = discrete_comparison)
slope_falling_4h(t):=  EMA_20_4h[t] < EMA_20_4h[t-3]
slope_neutral_4h(t):=  EMA_20_4h[t] == EMA_20_4h[t-3]   (rare; tie-break = neutral)
```

### 12-bar 4h directional efficiency

```text
numerator   := abs(close_4h[t] - close_4h[t-12])
denominator := sum( abs(close_4h[k] - close_4h[k-1]),  k = t-11 .. t )
DE_4h(t)    := numerator / denominator         (in [0, 1]; 0 if denominator == 0)
```

### 30m ATR(20)

Wilder's ATR with `n = 20`:

```text
TR(t)       := max( high[t] - low[t],
                    abs(high[t] - close[t-1]),
                    abs(low[t]  - close[t-1]) )
ATR_20(t)   := EMA-Wilder of TR with smoothing 1/20;
                seeded by SMA(TR) over the first 20 completed 30m bars.
```

### 30m ATR(20) percentile band over prior 480 completed 30m bars

```text
ATR_pct_480(t)  := percentile rank of ATR_20(t) within
                   { ATR_20(k) : k = t-480 .. t-1 }   (prior-completed only;
                                                       excludes t)
```

The pass test against the variant ATR band `[P_atr_low, P_atr_high]`:

```text
atr_band_pass(t) := P_atr_low <= ATR_pct_480(t) <= P_atr_high
```

### 30m relative-volume score vs. prior 480-bar median

```text
median_v_480(t)        := median( volume_30m[k]: k = t-480 .. t-1 )
relative_volume_30m(t) := volume_30m[t] / median_v_480(t)
                          (NaN if median == 0; treated as fail-closed
                           for liquidity_pass)
liquidity_pass(t)      := relative_volume_30m(t) >= V_liq_min
```

### v002 funding percentile over trailing 90 funding events

For a given completed 4h classifier evaluation timestamp `t_4h`:

```text
let last_funding_event_idx be the largest funding event index whose
    funding_time <= t_4h
let recent_90 := funding_rate values at indices
    [last_funding_event_idx-89 .. last_funding_event_idx]   (inclusive)
funding_pct_90(t_4h)   := percentile rank of funding_rate at
    last_funding_event_idx within recent_90.
```

Funding pathology pass test against `[P_fund_low, P_fund_high]`:

```text
funding_pass(t_4h) := P_fund_low <= funding_pct_90(t_4h) <= P_fund_high
```

### 30m Donchian prior 12-bar high / low excluding current bar

```text
prior_12_high_30m(t) := max( high_30m[k]: k = t-12 .. t-1 )
prior_12_low_30m(t)  := min( low_30m[k] : k = t-12 .. t-1 )
```

### Structural stop over prior 12 30m bars excluding current bar

```text
prior_12_low_30m_stop(t)  := min( low_30m[k] : k = t-12 .. t-1 )
prior_12_high_30m_stop(t) := max( high_30m[k]: k = t-12 .. t-1 )

long  initial stop  := prior_12_low_30m_stop(t)  - 0.10 * ATR_20(t)
short initial stop  := prior_12_high_30m_stop(t) + 0.10 * ATR_20(t)
```

### R calculation

```text
R_long(entry_price, stop_price)  := entry_price - stop_price       (positive)
R_short(entry_price, stop_price) := stop_price  - entry_price      (positive)
R_pct                            := R / entry_price                (signed-positive)
trade_R(realized_exit, entry, stop, side) :=
    side == LONG  ? (realized_exit - entry) / R_long(entry, stop)
  : side == SHORT ? (entry - realized_exit) / R_short(entry, stop)
```

### Stop-distance bounds gate

```text
stop_distance(t) := abs(entry_price - initial_stop)
stop_distance_atr := stop_distance(t) / ATR_20(t)

stop_distance_pass := 0.50 <= stop_distance_atr <= 2.20
```

If `stop_distance_pass` is false, the setup is **rejected at entry**; no trade is generated. Stop widening is forbidden.

### Feature computation hard rules

- All features use **prior-completed bars only**. No current-bar leakage. No future-bar leakage.
- Any feature computation that consults a row whose `close_time > now_decision` = stop condition.
- Any feature that depends (directly or indirectly) on the breakout signal of the same evaluation = stop condition (CFP-11 lookahead).
- All scalar arithmetic uses `numpy.float64`. NaN propagation is fail-closed (a NaN feature value blocks classification / signal at that timestamp).

## Regime classifier implementation plan

Predeclared classifier pseudocode (binding):

```text
input @ completed 4h bar t_4h, with companion 30m features at the
30m bar t_30m corresponding to the 4h bar's close_time:

# (a) HTF trend state
htf_trend_state(t_4h) :=
    (EMA_20_4h(t_4h)  >  EMA_50_4h(t_4h)) AND
    (close_4h(t_4h)   >  EMA_20_4h(t_4h)) AND
    slope_rising_4h(t_4h)
  ? LONG
  : (EMA_20_4h(t_4h)  <  EMA_50_4h(t_4h)) AND
    (close_4h(t_4h)   <  EMA_20_4h(t_4h)) AND
    slope_falling_4h(t_4h)
  ? SHORT
  : NEUTRAL

# (b) trend persistence
trend_persistence_pass(t_4h, E_min) :=
    DE_4h(t_4h) >= E_min

# (c) volatility regime
volatility_pass(t_30m, P_atr_low, P_atr_high) :=
    P_atr_low <= ATR_pct_480(t_30m) <= P_atr_high

# (d) liquidity adequacy
liquidity_pass(t_30m, V_liq_min) :=
    relative_volume_30m(t_30m) >= V_liq_min

# (e) funding pathology
funding_pass(t_4h, P_fund_low, P_fund_high) :=
    P_fund_low <= funding_pct_90(t_4h) <= P_fund_high

# composite
favorable_long(t_4h, t_30m, variant) :=
    htf_trend_state(t_4h) == LONG  AND
    trend_persistence_pass(t_4h, variant.E_min) AND
    volatility_pass(t_30m, variant.P_atr_low, variant.P_atr_high) AND
    liquidity_pass(t_30m, variant.V_liq_min) AND
    funding_pass(t_4h, variant.P_fund_low, variant.P_fund_high)

favorable_short(t_4h, t_30m, variant) := mirror with htf_trend_state == SHORT

unfavorable(t_4h, t_30m, variant) :=
    NOT favorable_long(...) AND NOT favorable_short(...)
```

Classifier hard rules (binding):

- Classifier is **independent of breakout signal**. The classifier MUST NOT inspect the breakout setup, the entry candidate, the stop distance, or any trade outcome.
- Classifier MUST NOT use future bars (any bar with `close_time > now_decision` for the 4h evaluation).
- Classifier MUST NOT use 5m Q1–Q7 diagnostic outputs.
- Classifier MUST NOT use V2 Phase 4l forensic numbers (e.g., the "3–5 × ATR" stop-distance observation) as design inputs. Phase 4q must not import those numbers as thresholds, and Phase 4r must not copy them.
- Classifier evaluation is deterministic given the variant and the data.
- A timestamp `t_4h` whose feature inputs include any NaN (because of insufficient lookback at the start of the date range) classifies as `unfavorable` until enough completed lookback exists (480 30m bars for ATR / liquidity percentile; 90 funding events for funding percentile; 12 4h bars for directional efficiency; 50 4h bars for EMA(50); 3 4h bars for slope-rising lookback). The fail-closed default during warmup is `unfavorable`.

## Regime state-machine implementation plan

Predeclared deterministic state update rules (binding; evaluated **only on completed 4h bar boundaries**; entries are evaluated only on completed 30m bars while the latest completed 4h bar's state is `regime_active`):

```text
Initial state on backtest start:  regime_inactive

On each completed 4h bar t_4h, given variant V:

if state == regime_inactive:
    if favorable_long(t_4h, ..., V):
        state = regime_candidate, direction = LONG, candidate_count = 1
    elif favorable_short(t_4h, ..., V):
        state = regime_candidate, direction = SHORT, candidate_count = 1
    else:
        state = regime_inactive

elif state == regime_candidate (direction D):
    if favorable_<D>(t_4h, ..., V):
        candidate_count += 1
        if candidate_count >= V.K_confirm:
            state = regime_active, direction = D
    else:
        # any non-favorable_<D> outcome (including direction switch) clears
        state = regime_inactive
        # direction switch handling: do NOT immediately re-enter
        # regime_candidate in the new direction on the same bar; the next
        # 4h bar must independently produce favorable_<other> to re-arm.

elif state == regime_active (direction D):
    if favorable_<D>(t_4h, ..., V):
        state = regime_active                    # continue
    else:
        state = regime_cooldown,
        direction = D,  # cooldown direction = exiting direction
        cooldown_count = 1

elif state == regime_cooldown (direction D):
    cooldown_count += 1
    if favorable_<D>(t_4h, ..., V):
        if cooldown_count >= V.C_cooldown:        # = 4 (fixed)
            state = regime_active                 # resume same direction
        else:
            state = regime_cooldown               # keep waiting
    else:
        if cooldown_count >= V.C_cooldown:
            state = regime_inactive               # cooldown elapsed; reset
        else:
            state = regime_cooldown               # keep waiting
```

State-machine hard rules (binding):

- **No direction switch inside `regime_active`.** A direction-switch favorable signal while in `regime_active` (e.g., `favorable_short` while active LONG) does NOT swap direction; it triggers `regime_active` → `regime_cooldown` (LONG-direction cooldown). The next direction is decided only after `regime_inactive` is reached.
- **No entries outside `regime_active`.** Any 30m signal generated when the latest completed 4h bar's state is not `regime_active` = stop condition (CFP-11 signal-emitted-outside-active).
- **Position lifecycle independent after entry.** Once a position is opened in `regime_active`, the position continues under its own stop / target / time-stop rules even if the regime later transitions to cooldown or inactive (Option A from Phase 4p).
- **Trade exit triggers cooldown.** When a position exits (stop / take-profit / time-stop), the regime transitions to `regime_cooldown` in the position's direction. This dampens immediate re-entry on the same setup.
- The state machine is **per-variant**: each of the 32 variants has its own independent state-machine trace per symbol. State traces MUST NOT be shared across variants or symbols.
- The state machine consumes **only completed 4h bars** for transitions. The 30m bar's signal evaluation reads the latest-completed-4h state at the 30m bar's `close_time`.

## Signal generation implementation plan

Predeclared (binding):

```text
At each completed 30m bar t_30m, with corresponding latest-completed-4h
state s_4h(t_30m), variant V:

if s_4h(t_30m) != regime_active:
    no signal evaluated.

elif s_4h(t_30m) == regime_active and direction == LONG:
    setup_long(t_30m, V) :=
        close_30m(t_30m) > prior_12_high_30m(t_30m) + 0.10 * ATR_20(t_30m)
    if setup_long(t_30m, V):
        candidate_long(t_30m, V) emitted.

elif s_4h(t_30m) == regime_active and direction == SHORT:
    setup_short(t_30m, V) :=
        close_30m(t_30m) < prior_12_low_30m(t_30m)  - 0.10 * ATR_20(t_30m)
    if setup_short(t_30m, V):
        candidate_short(t_30m, V) emitted.

For each emitted candidate:
    compute structural initial stop;
    compute stop_distance_atr;
    if NOT stop_distance_pass: candidate REJECTED at entry (no trade).
    else: candidate accepted; entry simulation runs.
```

Signal hard rules (binding):

- **Long-only when active LONG; short-only when active SHORT.** A LONG-direction `regime_active` MUST NOT emit short candidates (and vice versa). Mixed direction = stop condition.
- **No 5m triggers.** Any signal evaluation that consults 5m bars or 5m diagnostic outputs = stop condition (CFP-11).
- **No V2 8-feature AND chain.** G1 is regime-first; the AND-chain shape of the V2 spec is forbidden as a signal-layer rule.
- **No R2 pullback-retest.** Donchian breakout only.
- **No F1 mean-reversion.** Donchian breakout only.
- **No D1-A funding-Z-score directional rule.** Funding is regime-context only.
- **One signal evaluation per completed 30m bar per variant per symbol.** No intra-bar re-evaluation.
- **No look-ahead.** All inputs to the signal evaluation must satisfy `close_time <= t_30m`.

## Entry simulation plan

Predeclared (binding):

```text
On accepted candidate at t_30m:
  entry_price := open_30m(t_30m + 1)            # next-30m-bar open
  entry_time  := open_time of next 30m bar      # = t_30m's close_time = next bar's open_time
  side        := candidate direction (LONG | SHORT)
  initial_stop:= structural stop computed at t_30m
  R_per_unit  := R_long(entry_price, initial_stop)  if LONG
                 else R_short(entry_price, initial_stop)
  size        := position-sizing rule (see "Position sizing")
  state.position := opened
  state.regime   := unchanged  (Option A — independent lifecycle)
```

Entry hard rules (binding):

- **Market entry assumption.** No limit-order modeling. No conditional / OCO modeling.
- **No intrabar entries.** The entry price is the next 30m bar's open.
- **No partial fills.** Either the entry happens fully at the next-bar open or it does not happen.
- **One position max.** If a position is already open at the time of an accepted candidate, the candidate is dropped.
- **No pyramiding.** Subsequent accepted candidates while positioned are dropped (not stacked).
- **No reversal while positioned.** Subsequent accepted candidates of the opposite direction while positioned are dropped (not used to reverse).
- **BTCUSDT primary; ETHUSDT comparison only.** No portfolio construction. Same 32 variants evaluated independently per symbol.
- Entry timestamp recording: store `entry_open_time` (= the open_time of the bar at which entry happened); this is the bar that the entry's `entry_price` corresponds to.

## Exit simulation plan

Predeclared (binding):

```text
At each subsequent completed 30m bar t_30m_b after entry, while position open:

  bars_in_trade := t_30m_b's bar index minus entry bar index
  is_long := side == LONG

  high  := high_30m(t_30m_b)
  low   := low_30m (t_30m_b)
  close := close_30m(t_30m_b)

  # take-profit price
  if is_long:  tp_price := entry_price + 2.0 * R_per_unit
  else:        tp_price := entry_price - 2.0 * R_per_unit

  stop_price := initial_stop
  time_stop_due := bars_in_trade >= T_stop  (= 16)

  # detect bar-internal touches
  if is_long:
      stop_touched := low  <= stop_price
      tp_touched   := high >= tp_price
  else:
      stop_touched := high >= stop_price
      tp_touched   := low  <= tp_price

  # precedence: stop > take-profit > time-stop
  if stop_touched and tp_touched:
      exit_kind := STOP
      exit_price:= stop_price
  elif stop_touched:
      exit_kind := STOP
      exit_price:= stop_price
  elif tp_touched:
      exit_kind := TAKE_PROFIT
      exit_price:= tp_price
  elif time_stop_due:
      exit_kind := TIME_STOP
      exit_price:= open_30m(t_30m_b + 1)  # next bar open
  else:
      continue
```

Exit hard rules (binding):

- **Initial structural stop fixed at entry.** No re-tightening; no re-widening; no break-even; no trailing.
- **Take-profit at +2.0R.** Single fixed value; no axis.
- **Time-stop after 16 completed 30m bars.** Single fixed value; no axis. Time-stop fires at the bar after the 16th elapsed bar (i.e., exit at next bar's open).
- **Stop precedence within a single bar:** `stop > take-profit > time-stop`. Same-bar stop / take-profit ambiguity = stop wins (conservative).
- **No break-even.** `break_even_rule = disabled` (Phase 3w §6.3).
- **No trailing stop.** Intentional first-spec choice.
- **Position lifecycle independent of regime after entry** (Option A). Regime degradation does NOT force exit.
- **Any exit transitions the regime state to `regime_cooldown`** in the position's direction (handled in the state-machine update logic at the next completed 4h bar boundary).

## Cost and funding model implementation plan

Predeclared (binding; preserved verbatim from §11.6 and Phase 4p):

```text
Slippage cells (per side):
  LOW    = 1   bp
  MEDIUM = 4   bps
  HIGH   = 8   bps     (§11.6 promotion gate)

Taker fee per side:    4 bps
Maker rebate:          NOT used  (no maker assumption)
Live fee assumption:   NOT used  (no live fee modeling)

For each round-trip trade:
  total_cost_bps_per_side(cell) := cell_slippage + taker_fee
  applied to entry and exit independently:
    entry_price_executed_long  := entry_price * (1 + total_cost_bps_per_side / 10000)
    entry_price_executed_short := entry_price * (1 - total_cost_bps_per_side / 10000)
    exit_price_executed_long   := exit_price  * (1 - total_cost_bps_per_side / 10000)
    exit_price_executed_short  := exit_price  * (1 + total_cost_bps_per_side / 10000)
  (Cost is symmetric across LONG / SHORT direction.)

Funding cost:
  If a position is open across the close of a completed funding event
  (8h funding cycle on Binance USDⓈ-M futures), apply funding cost:
    funding_cost_per_event(side, fr, position_notional) :=
        side == LONG  ? + fr * position_notional
        side == SHORT ? - fr * position_notional
  (Sign convention: positive funding rate => longs pay shorts;
   the simulation must mirror v002 funding manifest sign convention
   and document any sign convention used.)

  For each completed funding event whose funding_time is strictly between
  entry_open_time and exit_realized_time:
    apply funding_cost_per_event to the running P&L.

  Funding cost is included in trade R computation:
    trade_R := (realized_pnl_after_costs - sum_funding_costs) / R_per_unit
```

Cost / funding hard rules (binding):

- HIGH cost is the §11.6 promotion gate. **Promotion blocked if HIGH cost fails.** R2's failure pattern (§11.6 cost-sensitivity) is preserved verbatim.
- No maker rebates.
- No live fee assumption.
- No regime-dependent cost adjustment.
- Funding cost MUST be applied at every completed funding event the position spans, not at trade-close-only.
- For each cost cell × variant × symbol × window, report `mean_R`, `total_R`, `trade_count`, `sharpe`, `profit_factor`, `max_drawdown_R`, `win_rate`.

## Position sizing and exposure implementation plan

Predeclared (binding; preserved verbatim from §1.7.3):

```text
risk_fraction        = 0.0025      (0.25% of sizing equity per trade)
max_leverage         = 2.0         (2x cap)
max_positions        = 1
max_active_stops     = 1
sizing_equity        = constant equity assumption for backtest;
                       no compounding; equity = 100 000 USDT (notional;
                       the choice is reported but does not affect R-based
                       results since R is stop-distance-relative);
                       must be consistent across variants / symbols / windows.
position_size_units  := (sizing_equity * risk_fraction) / abs(R_per_unit)
position_notional    := position_size_units * entry_price
leverage_used        := position_notional / sizing_equity

if leverage_used > max_leverage:
    cap position_size_units to (max_leverage * sizing_equity / entry_price)
    cap position_notional   to (max_leverage * sizing_equity)
    note: capping reduces effective risk below 0.25% on stops with very
          tight distances; record cap occurrence.

if position_size_units * entry_price < exchange_min_notional:
    REJECT: below-min-notional. Record reject reason.

lot_size rounding: round DOWN to symbol step size; if rounding drops
size to 0, REJECT.
```

Exposure hard rules (binding):

- **One position max.** Any open position blocks new entries.
- **No pyramiding.** Subsequent candidates while positioned are dropped.
- **No reversal while positioned.** Subsequent opposite-direction candidates while positioned are dropped.
- **No portfolio sizing.** BTCUSDT and ETHUSDT are independent backtests. There is no shared equity allocation; results are reported per symbol.
- **No correlation overlay.** Same 32 variants evaluated independently per symbol.

## Threshold-grid handling

Predeclared (binding):

```text
Grid cardinality:    32 variants  (= 2^5)
Five binary axes (Phase 4p locked):
  Axis 1: E_min          in {0.30, 0.40}
  Axis 2: ATR band       in {[20, 80], [30, 70]}
  Axis 3: V_liq_min      in {0.80, 1.00}
  Axis 4: funding band   in {[15, 85], [25, 75]}
  Axis 5: K_confirm      in {2, 3} 4h bars
Variant ordering: deterministic lexicographic by axis name then axis value
                  (axis names sorted alphabetically: ATR_band, E_min,
                   K_confirm, V_liq_min, funding_band — or any deterministic
                   tuple order documented in run_metadata.json).
                  The chosen ordering must be reported in run_metadata.json
                  and must be stable across reruns.
No grid extension:   any addition of variants beyond the 32 = stop condition.
No grid reduction:   all 32 variants must be evaluated; no early exit.
No outcome-driven threshold selection: train-window selection of a
                     "BTC-train-best variant" is allowed for reporting and
                     for the M2 always-active baseline comparison cell, but
                     the train-best variant must be selected by deflated
                     Sharpe / PBO-aware criteria (not raw in-sample Sharpe)
                     and the SAME variant identifier must be used in
                     validation and OOS reporting (no re-selection).
Future G1-extension: any axis activation (N_R, T_stop, or any other) =
                     separately authorized governance amendment; Phase 4r
                     must NOT introduce them.
```

## Search-space control

Predeclared (binding):

- Because the grid is 32 variants, **PBO / DSR / CSCV are required and tractable** within Python-runtime feasibility.
- **CSCV S = 16** (analogous to Phase 4k). The exact `C(16, 8) = 12 870` combinations × 32 variants = ~412 000 sub-evaluations is well within feasibility for a pure pyarrow + numpy implementation. If wall-clock cost in Phase 4r exceeds a documented limit, the future Phase 4r execution brief MUST stop or report the limitation; no silent approximation.
- **Deflated Sharpe must account for 32 variants.** Bailey & López de Prado (2014) deflated Sharpe ratio with `N = 32`.
- **PBO must report both train→validation and train→OOS** sub-sample rank distributions.
- **No alternative complexity-control schemes** without a separately authorized governance amendment.

## M1 mechanism-check implementation plan

Predeclared (binding):

```text
M1 — Regime-validity negative test:

  Active population (per variant V, per symbol S):
    Pseudo-trades = trades that WOULD HAVE BEEN ENTERED if the breakout
    setup had been evaluated only when state == regime_active under V on S.
    This is the SAME population as the actual G1 trades in the OOS HIGH cell
    (since G1 only fires inside regime_active).

  Inactive population (per variant V, per symbol S):
    Pseudo-trades = breakout setups that WOULD HAVE BEEN ENTERED at the same
    rule and same exit model BUT during state in {regime_inactive,
    regime_candidate, regime_cooldown} (i.e., outside regime_active).
    These pseudo-trades use the SAME signal rule, SAME structural stop,
    SAME stop-distance gate, SAME +2.0R target, SAME T_stop=16, SAME costs.
    They are computed separately and reported separately.

  Both populations are computed on BTC OOS HIGH (primary) and ETH OOS HIGH
  (comparison), with mean_R and bootstrap 95% CI lower bound (B = 10 000;
  pinned RNG seed 202604300).

Pass test (per Phase 4p):
  active_mean_R - inactive_mean_R >= +0.10 R    (BTC OOS HIGH primary)
  AND bootstrap_CI_lower(B = 10000) of (active_mean_R - inactive_mean_R) > 0.

Reporting:
  - active_population trade table per variant per symbol per window.
  - inactive_population trade table per variant per symbol per window.
  - active_vs_inactive_m1.csv with differential, CI lower, CI upper, pass/fail.
```

M1 implementation rules:

- **Same exit model.** The inactive-population pseudo-trades MUST use the same exit rules (stop / take-profit / time-stop).
- **No selection bias.** Inactive-population pseudo-trades MUST NOT be filtered to retain only profitable ones.
- **No subset cherry-picking.** All inactive-population candidates that satisfy the breakout setup AND the stop-distance gate must be included.
- **Reported on BTC OOS HIGH primary; ETH OOS HIGH reported but does not rescue.**

## M2 mechanism-check implementation plan

Predeclared (binding):

```text
M2 — Regime-gating value-add (G1 vs always-active baseline):

  G1 trades       (per variant V, per symbol S, per cost cell, per window):
    actual G1 trades produced in the OOS HIGH cell
    (regime-gated; direction matches active-regime direction).

  Always-active baseline (same variant V, same V breakout setup, same
                          structural stop, same stop-distance gate, same
                          +2.0R target, same T_stop=16, same cost cell,
                          same window):
    breakout setups that WOULD HAVE BEEN ENTERED if the regime gate were
    REMOVED entirely (i.e., breakout fired regardless of regime state and
    regardless of HTF direction; long if breakout up; short if breakout down).
    The always-active baseline is NOT regime-direction-tied; it takes both
    directions on their own breakout triggers.
    Same cost cell. Same exit model.

Pass test (per Phase 4p):
  G1_mean_R - always_active_mean_R >= +0.05 R   (BTC OOS HIGH primary)
  AND bootstrap_CI_lower(B = 10000) of differential > 0.

Reporting:
  - g1_vs_always_active_m2.csv with G1 mean_R, always-active mean_R,
    differential, CI lower, CI upper, pass/fail per variant / symbol /
    cost cell.
```

M2 implementation rules:

- **Same variant.** The always-active baseline uses the same variant V (same E_min, same ATR band, same V_liq_min, same funding band, same K_confirm). The only thing removed is the regime-active gate.
- **Same exit model.** Stop / target / time-stop / cost cell identical.
- **No "best variant" cherry-picking** for the always-active baseline; the always-active baseline is computed for every variant and reported.

## M3 mechanism-check implementation plan

Predeclared (binding):

```text
M3 — Inside-regime co-design validity:

  Pass test (BTCUSDT primary):
    BTC OOS HIGH mean_R    > 0.0
    BTC OOS HIGH trade_count >= 30
    AND no CFP-1 / CFP-2 / CFP-3 triggered for the BTC-train-best variant.

  Reporting:
    m1_m2_m3_m4_summary.csv
    btc_oos_variants.csv  (mean_R, trade_count, sharpe, PF, max_DD by variant)
    btc_train_best_variant.csv
```

M3 implementation rules:

- **BTC OOS HIGH is the primary cell.** No substitution of MEDIUM or LOW for the M3 pass test.
- **Trade count threshold = 30** (mirroring Phase 4k's 30-trade DSR sufficiency rule).
- **CFP gate.** Even with positive mean_R and ≥ 30 trades, a CFP-1 / CFP-2 / CFP-3 trigger fails M3.

## M4 mechanism-check implementation plan

Predeclared (binding):

```text
M4 — Cross-symbol robustness:

  ETH OOS HIGH metrics computed for the SAME BTC-train-best variant:
    eth_mean_R_diff     := eth_g1_mean_R - eth_always_active_mean_R
                            (must be non-negative)
    eth_directional_sign:= sign(eth_g1_mean_R - eth_inactive_mean_R)
                            == sign(btc_g1_mean_R - btc_inactive_mean_R)

  Pass test:
    eth_mean_R_diff >= 0
    AND eth_directional_sign == True

  ETH cannot rescue BTC.  CFP-4 covers BTC fails / ETH passes.
```

M4 implementation rules:

- **Same variant identifier as BTC train-best.** No re-selection on ETH.
- **Directional consistency.** Sign of (G1 minus inactive) on ETH must match BTC.
- **ETH is a comparison cell only.** A passing ETH cannot make a failing BTC pass.

## Negative-test implementation plan

Predeclared (binding):

```text
Required:
  - active_vs_inactive (M1).
  - g1_vs_always_active (M2).

Optional secondary diagnostic:
  - random-regime baseline.
    If included: same active fraction as the real classifier in the
    given window (computed empirically per variant per symbol per window);
    separate RNG seed; same breakout setup, stop, target, time-stop, cost.
    Report as DIAGNOSTIC ONLY in random_regime_baseline.csv;
    NOT a promotion gate by Phase 4q's choice.

Phase 4q decision:
  Random-regime baseline = DIAGNOSTIC ONLY.
  Reasoning: M1 active-vs-inactive already captures the core null
  ("regime gate adds nothing"). The random-regime baseline is a useful
  sanity check on classifier specificity but is not a binding promotion
  gate; promoting it to a gate would compound complexity at first-spec
  stage and risk Verdict-D outcomes from sample-size collapse on the
  random-regime cell.
```

If a future Phase 4r execution brief wishes to promote the random-regime baseline to a binding gate, that is a separately authorized governance amendment.

## PBO / deflated Sharpe / CSCV plan

Predeclared (binding):

```text
PBO (Bailey / Borwein / López de Prado / Zhu, 2014):
  - Train-to-validation: rank 32 variants by Sharpe in train window;
    rank by Sharpe in validation window;
    PBO_train_validation := P(rank_validation > median | rank_train == best).
  - Train-to-OOS:        rank by Sharpe in train; rank by Sharpe in OOS;
    PBO_train_oos        := P(rank_oos > median | rank_train == best).
  - Report both PBO values in pbo_summary.csv with bootstrap 95% CI.
  - CFP-6 triggers if PBO_train_validation > 0.50 OR PBO_train_oos > 0.50.

Deflated Sharpe (Bailey & López de Prado, 2014):
  - For each variant, compute Sharpe per window per symbol per cost cell.
  - Compute deflated Sharpe with N = 32, M = 1 (single in-sample-best
    selection) and the standard skew/kurtosis correction.
  - Train-best variant must have train-window deflated Sharpe documented;
    if train-window trade count < 30, deflated Sharpe is reported as N/A
    and CFP-1 may trigger.

CSCV S = 16 sub-samples:
  - Partition the OOS holdout window into 16 chronologically-respecting
    sub-samples (each ~1.3 months of the ~21 months OOS).
  - Enumerate C(16, 8) = 12 870 train/test combinations.
  - For each combination, identify the train-half-best variant by Sharpe;
    compute its rank in the test-half;
    record rank.
  - cscv_rankings.csv (or compressed parquet equivalent) reports the full
    distribution.
  - PBO_cscv := mean(rank_test_half > median | train_half_best).

Compute budget:
  - 32 variants x 12 870 combinations = ~412 000 evaluations.
  - Each evaluation reuses precomputed per-variant per-bar trade tables;
    no re-simulation.
  - Estimated wall-clock budget for Phase 4r: well under 1 hour for the
    CSCV stage on a modern laptop. If the budget exceeds the limit, Phase
    4r MUST stop or report the limitation explicitly; silent approximation
    is forbidden.
```

## Chronological validation plan

Predeclared (binding; reused verbatim from Phase 4k):

```text
Train          : 2022-01-01 00:00:00 UTC .. 2023-06-30 23:30:00 UTC  (~18 months)
Validation     : 2023-07-01 00:00:00 UTC .. 2024-06-30 23:30:00 UTC  (~12 months)
OOS holdout    : 2024-07-01 00:00:00 UTC .. 2026-03-31 23:30:00 UTC  (~21 months;
                                                                     primary G1
                                                                     evidence cell)

Discipline rules (binding):
  - No data shuffling.
  - No leakage between windows.
  - No window modification post-hoc.
  - No window expansion.
  - No window contraction.
  - All 32 variants evaluated on all three windows.
  - Train-best variant identified once; same variant used in validation
    and OOS reporting.
  - BTC and ETH evaluated independently; no cross-symbol optimization.
  - Same RNG seed across windows.

Optional walk-forward (deferred):
  - 4 rolling 12-month OOS windows: not required by Phase 4q. If a future
    execution brief omits walk-forward, that is acceptable; if included,
    must be predeclared in the execution brief and not derived from
    observed Phase 4r outcomes.
```

## BTCUSDT primary / ETHUSDT comparison protocol

Predeclared (binding):

- **BTCUSDT is the primary symbol.** All M1 / M2 / M3 promotion gates use BTC OOS HIGH primarily.
- **ETHUSDT is comparison only.** ETH metrics are reported in `eth_*` tables and informant the M4 pass/fail check.
- **ETH cannot rescue BTC.** A passing ETH does NOT make a failing BTC pass. CFP-4 enforces this.
- **No cross-symbol optimization.** The same 32 variants are evaluated independently per symbol. No "BTC-tuned but ETH-checked" reordering.
- **No portfolio P&L.** No combined BTC+ETH portfolio metrics; results are per-symbol.
- **Same RNG seed across symbols.**

## Catastrophic-floor predicate implementation plan

Predeclared exact evaluation algorithms for CFP-1 .. CFP-12 (binding):

```text
CFP-1   Insufficient trade count:
        Trigger if OOS BTC HIGH trade_count < 30 across > 50% of the 32
        variants. Train-best variant trade_count < 30 also triggers CFP-1.

CFP-2   Negative OOS expectancy under HIGH cost:
        Trigger if any active variant on OOS BTC HIGH has mean_R <= -0.20R.

CFP-3   Catastrophic drawdown / profit_factor floor:
        Trigger if any active variant on OOS BTC HIGH has
        max_drawdown_R > 10R OR profit_factor < 0.50.

CFP-4   BTC fails / ETH passes:
        Trigger if M3 BTC FAIL AND M4 ETH PASS (ETH cannot rescue BTC).

CFP-5   Train-only success / OOS failure:
        Trigger if train BTC HIGH mean_R > 0 BUT OOS BTC HIGH mean_R <= 0
        for the train-best variant.

CFP-6   Excessive PBO:
        Trigger if PBO_train_validation > 0.50 OR PBO_train_oos > 0.50.

CFP-7   Regime / month overconcentration:
        Trigger if any single calendar month accounts for > 50% of total
        OOS trades for the train-best variant on BTCUSDT.

CFP-8   Regime sensitivity failure:
        Trigger if a sensitivity cell that varies regime activation
        threshold within a small documented neighborhood produces
        > 0.20R degradation in mean_R vs main cell on BTC OOS HIGH.
        (Phase 4q specifies the sensitivity neighborhood as
        E_min +/- 0.05 (using the closer of {0.30, 0.40} as the anchor)
        and ATR-band-edge +/- 5 percentile points, evaluated only as a
        sensitivity cell — NOT as new active variants.)

CFP-9   Regime excludes too much data / sample-size collapse:
        Trigger if average regime_active fraction across OOS for the
        train-best variant on BTCUSDT < 5% of OOS bars.
        (A < 5% active fraction on a ~21-month OOS gives < ~1 month of
        active time; trade counts will collapse and reliable mechanism
        evidence is impossible.)

CFP-10  Forbidden input access (optional ratio columns):
        Trigger if any of count_toptrader_long_short_ratio,
        sum_toptrader_long_short_ratio, count_long_short_ratio,
        sum_taker_long_short_vol_ratio is read at any time during the
        run. Detection layers: static scan of script source; explicit-
        column-list verification at load time; runtime introspection
        of dataframe columns post-load.

CFP-11  Regime classifier lookahead OR dependency on signal:
        Trigger if classifier inputs include any value with
        close_time > now_decision; OR if classifier consults the
        breakout signal of the same evaluation; OR if a signal is
        emitted outside regime_active.

CFP-12  Data governance violation:
        Trigger if metrics OI is loaded; OR mark-price (any timeframe)
        is loaded; OR aggTrades is loaded; OR spot / cross-venue is
        loaded; OR any non-binding manifest is loaded; OR network I/O
        is attempted; OR credentials are read; OR write is attempted to
        data/raw / data/normalized / data/manifests; OR
        Phase 4i / v002 / v001-of-5m manifest is modified; OR v003 is
        created; OR private endpoints / authenticated REST / user-stream
        / WebSocket / listenKey lifecycle is touched.
```

CFP evaluation hard rules:

- **All 12 CFPs are evaluated** in every Phase 4r run. None may be skipped.
- **Order:** CFP-10 / CFP-11 / CFP-12 are evaluated as **runtime stop conditions** (the run aborts on the first detection; no completion). CFP-1 .. CFP-9 are evaluated as **post-run verdict predicates**.
- **Any single CFP triggered = HARD REJECT** unless a stop-condition / incomplete-methodology issue makes Verdict D more appropriate (see "Verdict taxonomy").
- **No CFP relaxation.** Adjusting CFP thresholds based on Phase 4r observed outcomes = stop condition.

## Verdict taxonomy

Predeclared (binding):

```text
Verdict A — G1 framework PASS:
  - All M1 / M2 / M3 / M4 PASS;
  - No CFP triggers;
  - HIGH cost survives.
  Effect: G1 first-spec is research-promotable (NOT live-readiness).

Verdict B — G1 framework PARTIAL PASS:
  - Some mechanisms PASS but not all (e.g., M1 PASS / M2 PASS / M3 PASS /
    M4 FAIL with no CFP-4);
  - No CFP triggers;
  - Limited research evidence.
  Effect: G1 first-spec retained as research evidence; non-leading;
          no rescue authorized; no parameter change authorized;
          consolidation memo recommended (analogous to Phase 4m).

Verdict C — G1 framework HARD REJECT:
  - Any single CFP triggers;
  - OR all four mechanism checks FAIL.
  Effect: G1 first-spec is terminally rejected as retained research
          evidence only; no G1-prime / G1-narrow / G1-extension authorized;
          consolidation memo recommended.

Verdict D — G1 framework INCOMPLETE:
  - A methodology / governance / data / implementation stop condition
    halted the run before all required reporting was produced;
  - OR a deviation from Phase 4q methodology is detected post-hoc;
  - OR sample sizes are insufficient for required statistics
    (e.g., bootstrap impossible due to N < 5 active trades) and the
    reason is methodological rather than CFP-1 quantitative.
  Effect: no verdict-driven retained-evidence label; the methodology
          gap must be resolved before any G1 backtest evidence is
          interpretable.
```

## Required reporting tables

Future Phase 4r must produce under `data/research/phase4r/tables/` (gitignored; reproducible from the orchestrator):

```text
run_metadata.json                       run id; UTC timestamps; commit SHA;
                                        Python version; package versions;
                                        RNG seed; pinned manifest SHA refs;
                                        variant ordering tuple
manifest_references.csv                 per used manifest:
                                          name; version; SHA256 from
                                          manifest; verified file SHA256;
                                          research_eligible flag
parameter_grid.csv                      32 rows; one per variant;
                                          variant_id; E_min; P_atr_low;
                                          P_atr_high; V_liq_min;
                                          P_fund_low; P_fund_high; K_confirm
split_boundaries.csv                    train / validation / OOS UTC
                                          start/end (ms; ISO-8601)
feature_schema.csv                      feature name; type; lookback;
                                          dependencies; source
regime_state_transitions.csv            per symbol per variant per 4h bar:
                                          state_before; state_after;
                                          direction; cause
regime_active_fraction_by_symbol_window.csv
                                        per symbol per variant per window:
                                          active_fraction; candidate_fraction;
                                          cooldown_fraction; inactive_fraction
btc_train_variants.csv                  per variant: trade_count; mean_R;
                                          total_R; sharpe; PF; max_DD;
                                          win_rate; cost cells (LOW/MED/HIGH)
btc_validation_variants.csv             same structure on validation
btc_oos_variants.csv                    same structure on OOS
eth_train_variants.csv                  same structure on ETH train
eth_validation_variants.csv             same structure on ETH validation
eth_oos_variants.csv                    same structure on ETH OOS
btc_train_best_variant.csv              the single train-best variant
                                          identified by deflated Sharpe;
                                          full metric set on train,
                                          validation, OOS for all 3 cost
                                          cells
btc_train_best_cost_cells.csv           cost-cell sensitivity for the
                                          train-best variant
active_vs_inactive_m1.csv               M1 numeric: active_mean_R;
                                          inactive_mean_R; differential;
                                          bootstrap CI lower; CI upper;
                                          pass/fail
g1_vs_always_active_m2.csv              M2 numeric: g1_mean_R;
                                          always_active_mean_R;
                                          differential; bootstrap CI lower;
                                          CI upper; pass/fail
m1_m2_m3_m4_summary.csv                 four mechanism pass/fail rows;
                                          binding promotion-bar evaluation
cost_sensitivity.csv                    per variant per cost cell per
                                          symbol per window: mean_R
pbo_summary.csv                         PBO_train_validation;
                                          PBO_train_oos;
                                          PBO_cscv;
                                          bootstrap CIs
deflated_sharpe_summary.csv             per variant per window per cost
                                          cell: raw_sharpe; n_variants_used;
                                          deflated_sharpe; pass thresholds
cscv_rankings.csv                       (or compressed parquet equivalent)
                                          C(16,8)x32 sub-evaluation results
trade_distribution_by_month_regime.csv  per train-best variant per symbol
                                          per OOS month: trade_count;
                                          mean_R; cumulative_R;
                                          regime_active_fraction
catastrophic_floor_predicates.csv       12 rows; one per CFP:
                                          predicate_id; description;
                                          numeric inputs;
                                          triggered (bool); detail
verdict_declaration.csv                 final verdict (A / B / C / D);
                                          decision basis; binding driver;
                                          notes
forbidden_work_confirmation.csv         summary of static scan + runtime
                                          checks for forbidden inputs
                                          (mark-price, aggTrades, metrics
                                          OI, optional ratio columns,
                                          5m diagnostics, network, creds,
                                          src/prometheus mods, test mods,
                                          script mods, manifest mods,
                                          data mods)
```

## Required plots

Future Phase 4r should produce under `data/research/phase4r/plots/` (gitignored):

```text
cumulative_R_BTC_train_validation_oos.png      cumulative R curve for the
                                                train-best variant on BTC
                                                across all three windows;
                                                MEDIUM-cost reference line
cumulative_R_ETH_train_validation_oos.png      same for ETH (comparison)
regime_state_timeline_BTC.png                  per-bar state timeline for
                                                the train-best variant on
                                                BTCUSDT over the OOS window
regime_state_timeline_ETH.png                  same for ETH OOS
active_vs_inactive_R_distribution.png          M1 distributions histogram
g1_vs_always_active_mean_R.png                 M2 grouped bar across cost
                                                cells per symbol
dsr_distribution.png                           deflated Sharpe distribution
                                                across 32 variants
pbo_rank_distribution.png                      CSCV rank distribution
btc_oos_drawdown.png                           drawdown curve for BTC OOS
                                                train-best variant
monthly_cumulative_R_BTC_oos.png               monthly-bucketed cumulative
                                                R for BTC OOS
trade_R_distribution.png                       trade-R histogram BTC + ETH

If any required plot cannot be produced (e.g., zero trades), the future
report MUST state why and whether this affects Verdict D.
```

## Stop conditions

Future Phase 4r MUST immediately stop and produce a failure report if any of the following is detected:

```text
- required manifest missing
- manifest SHA mismatch
- research_eligible mismatch
- local data file missing
- local data file corrupted
- forbidden input accessed:
    * metrics OI loaded
    * optional ratio column accessed
    * mark-price loaded (any timeframe)
    * aggTrades loaded
    * spot / cross-venue loaded
    * 5m diagnostic outputs loaded as features or regime indicators
    * any non-binding manifest loaded
- private / authenticated / API / WebSocket / network path touched
- credential read / store attempted
- .env read attempted
- write attempted to data/raw, data/normalized, data/manifests
- write attempted to existing src/ files
- modification of existing tests
- modification of existing scripts
- classifier uses future bars
- classifier depends on breakout signal
- signal emitted outside regime_active
- trade emitted despite stop-distance rejection
- multi-direction emission while regime is single-direction-active
- timestamp misalignment (open_time != close_time of prior bar)
- duplicate (symbol, interval, open_time) row
- partial-bar consumption for strategy decision
- validation report incomplete (any required table or plot missing)
- ruff check . fails
- pytest -q fails (test count regression below 785)
- mypy strict fails
- pytest test count increases without an authorized test addition
- variant grid expanded beyond 32 or contracted below 32
- variant ordering changes between train / validation / OOS
- random RNG seed (not 202604300) used without authorization
- bootstrap impossible because of insufficient sample (Verdict D path)
```

A stop condition during runtime aborts the run and produces a failure report; no fallback / silent approximation is permitted.

## Reproducibility requirements

Future Phase 4r must:

```text
- pin every used manifest SHA256 in run_metadata.json and
  manifest_references.csv;
- pin commit SHA of the repository at run start in run_metadata.json;
- use deterministic lexicographic variant ordering and document the
  ordering tuple in run_metadata.json;
- pin RNG seed = 202604300 for all bootstrap / CSCV / random-regime
  baseline operations;
- stable-sort all input frames by (symbol, interval, open_time);
- write idempotent outputs under data/research/phase4r/ (rerunning the
  orchestrator must overwrite files identically);
- not use network;
- not access credentials;
- report exact command line used in run_metadata.json;
- report Python version, pyarrow version, numpy version in run_metadata.json;
- report SHA256 of every emitted CSV / parquet table where feasible
  (report partial / streaming hashes for large CSCV tables if needed).
```

## What future Phase 4r may create

Future Phase 4r, *if separately authorized*, may create:

```text
scripts/phase4r_g1_backtest.py                                    (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4r_g1-backtest-execution.md  (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4r_closeout.md               (new)
data/research/phase4r/                                            (gitignored;
                                                                   not committed)
```

## What this does not authorize

Phase 4q does NOT authorize:

```text
- Phase 4r execution (must be separately authorized)
- writing scripts/phase4r_g1_backtest.py
- running any G1 backtest
- creating V3 or any runnable strategy
- creating G1-prime / G1-narrow / G1-extension
- creating V2-prime / V2-narrow / V2-relaxed / V2 hybrid
- creating F1 / D1-A / R2 rescue
- modifying src/prometheus
- modifying tests
- modifying scripts
- modifying scripts/phase4l_v2_backtest.py
- modifying data/raw
- modifying data/normalized
- modifying data/manifests
- committing data/research outputs
- acquiring data
- downloading data
- patching / forward-filling / interpolating / regenerating / replacing data
- creating v003
- running scripts/phase3q_5m_acquisition.py
- running scripts/phase3s_5m_diagnostics.py
- running scripts/phase4i_v2_acquisition.py
- running scripts/phase4l_v2_backtest.py
- running diagnostics
- rerunning Q1-Q7
- using optional metrics ratio columns
- using metrics OI in G1 first-spec
- using 5m Q1-Q7 findings as regime indicators
- using V2 Phase 4l stop-distance failure numbers to choose thresholds
- modifying Phase 4p G1 strategy-spec selections
- modifying Phase 4g V2 strategy-spec selections
- modifying Phase 4j §11 governance
- modifying Phase 4k methodology
- revising retained verdicts
- revising project locks, thresholds, parameters, or governance rules
- changing §11.6, §1.7.3, Phase 3r governance, Phase 3v governance,
  Phase 3w governance, Phase 4j governance, or Phase 4k methodology
- starting Phase 4 canonical
- implementing reconciliation
- implementing a real exchange adapter
- implementing exchange-write capability
- placing or cancelling orders
- using / requesting / storing credentials
- adding authenticated REST / private endpoints / public endpoint clients /
  user stream / WebSocket / listenKey lifecycle
- enabling MCP / Graphify or modifying .mcp.json
- creating .env files
- deploying anything
- creating paper / shadow runtime
- implying live-readiness
```

## Forbidden-work confirmation

Phase 4q does NOT do any of the following:

- run a G1 backtest;
- write G1 backtest code;
- create `scripts/phase4r_g1_backtest.py` or any other script;
- modify any existing script;
- modify any source file under `src/prometheus/`;
- modify any test;
- acquire data;
- download data;
- modify any `data/raw/`, `data/normalized/`, or `data/manifests/` content;
- modify any manifest;
- create v003 or any new dataset;
- run any acquisition script;
- run any diagnostics script;
- run any backtest script;
- modify Phase 4p / Phase 4o / Phase 4n / Phase 4m / Phase 4l / Phase 4k / Phase 4j / Phase 4i / Phase 4h / Phase 4g / Phase 4f / Phase 4e / Phase 4a / Phase 3 retained-evidence text;
- modify the Phase 4i acquisition script or execute it;
- modify the Phase 4l backtest script or execute it;
- modify the Phase 4j §11 metrics OI-subset partial-eligibility binding rule;
- modify the Phase 3r §8 mark-price gap governance;
- modify the Phase 3v §8 stop-trigger-domain governance;
- modify the Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance;
- modify the Phase 4k V2 backtest-plan methodology;
- modify the Phase 4p G1 strategy spec;
- revise any retained verdict (R3 / R2 / F1 / D1-A / V2 / H0 / R1a / R1b-narrow);
- change any project lock (§11.6 / §1.7.3 / mark-price stops / v002 verdict provenance);
- propose any 5m strategy / hybrid / variant;
- propose any V2-prime / V2-rescue;
- propose any retained-evidence rescue;
- propose any G1-prime / G1-extension axes activation;
- start Phase 4r / Phase 4 canonical / paper-shadow / live-readiness / deployment / production-key creation / exchange-write capability / authenticated REST / private endpoints / user-stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- consult any private endpoint / user stream / WebSocket / authenticated REST in code;
- store, request, or display any secret.

## Remaining boundary

```text
R3                  : V1 breakout baseline-of-record (preserved)
H0                  : framework anchor (preserved)
R1a / R1b-narrow    : retained research evidence; non-leading (preserved)
R2                  : FAILED — §11.6 cost-sensitivity blocks (preserved)
F1                  : HARD REJECT (preserved)
D1-A                : MECHANISM PASS / FRAMEWORK FAIL — other (preserved)
V2                  : HARD REJECT (Phase 4l terminal for first-spec; preserved)
G1                  : pre-research only; strategy-spec defined in Phase 4p;
                      backtest-plan defined in Phase 4q;
                      not implemented; not backtested; not validated;
                      not live-ready
§11.6               : 8 bps HIGH per side (preserved verbatim)
§1.7.3              : 0.25% risk / 2× leverage / 1 position / mark-price stops
                      (preserved)
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m
                              (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance
                              (preserved)
Phase 4a runtime            : public API and behavior (preserved)
Phase 4e                    : reconciliation-model design memo (preserved)
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p
                            : all preserved verbatim
Recommended state           : paused (outside conditional Phase 4r)
```

## Operator decision menu

- **Option A — primary recommendation:** Phase 4r — G1 Backtest Execution (docs-and-code standalone research script). Phase 4r would create `scripts/phase4r_g1_backtest.py` exactly under the Phase 4q methodology, run the backtest, and emit a verdict (A / B / C / D) per Phase 4q's verdict taxonomy.
- **Option B — conditional secondary:** remain paused. Acceptable if the operator prefers not to commit to G1 evidence collection at this time.

NOT recommended:

- immediate G1 implementation (skipping the backtest); REJECTED;
- immediate data acquisition (no new acquisition required);
- paper / shadow / live-readiness; FORBIDDEN;
- Phase 4 canonical; FORBIDDEN;
- G1-prime / G1-extension axis activation; FORBIDDEN without separate governance amendment;
- V2 / F1 / D1-A / R2 rescue; FORBIDDEN.

**Phase 4r is NOT authorized by this Phase 4q memo.** Phase 4r execution requires a separate explicit operator authorization brief.

## Next authorization status

```text
Phase 4r                       : NOT authorized
Phase 4 (canonical)            : NOT authorized
Paper / shadow                 : NOT authorized
Live-readiness                 : NOT authorized
Deployment                     : NOT authorized
Production-key creation        : NOT authorized
Authenticated REST             : NOT authorized
Private endpoints              : NOT authorized
User stream / WebSocket        : NOT authorized
Exchange-write capability      : NOT authorized
MCP / Graphify                 : NOT authorized
.mcp.json / credentials        : NOT authorized
G1 implementation              : NOT authorized
G1 backtest execution          : NOT authorized (Phase 4r required;
                                                 not yet authorized)
G1 data acquisition            : NOT authorized (none required)
G1-prime / G1-extension axes   : NOT authorized; not proposed
V2-prime / V2-variant          : NOT authorized; not proposed
Retained-evidence rescue       : NOT authorized; not proposed
5m strategy / hybrid           : NOT authorized; not proposed
ML feasibility                 : NOT authorized; not proposed
New family research            : NOT authorized beyond Phase 4n
                                  Candidate B (G1)
```

The next step is operator-driven: the operator decides whether to authorize Phase 4r (G1 Backtest Execution, docs-and-code) or remain paused. Until then, the project remains at the post-Phase-4q G1 backtest-plan boundary.

---

**Phase 4q is docs-only. No source code, tests, scripts, data, manifests, or successor phases were created or modified. Recommended state remains paused outside conditional Phase 4r. No next phase authorized.**
