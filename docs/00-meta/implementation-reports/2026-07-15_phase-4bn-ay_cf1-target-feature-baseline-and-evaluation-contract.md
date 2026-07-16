# Phase 4bn-AY — CF-1 Target / Feature / Baseline / Evaluation Contract (Implementation-Grade, Frozen)

This is the implementation-grade companion to the Phase 4bn-AY main preregistration memo
(`2026-07-15_phase-4bn-ay_cf1-realized-volatility-substrate-test-preregistration.md`). It
freezes every execution-bearing field of the CF-1 realized-volatility magnitude-forecasting
substrate test so that a later, separately-authorized execution phase has **no researcher
freedom**. No field below is left as "TBD", "choose later", "as appropriate", or "reasonable
default". Every fact is derived from committed repository evidence only; **no market data,
feature row, label row, or evidence reserve was opened to write it.**

If any execution-bearing field had been un-fixable from committed evidence without opening data,
this phase would have failed closed with
`STOP_CF1_PREREGISTRATION_INSUFFICIENT_COMMITTED_METADATA`. That did **not** occur: every field
below is fixed from committed source constants and committed reports.

---

## 1. Canonical data identity references (committed; not opened)

| Item | Committed value | Committed source |
|---|---|---|
| Substrate | BTCUSDT USDⓈ-M perpetual aggTrades, pre-v002 segment | Phase 4bn-Y; Phase 4bn-AB |
| Raw family | `microstructure_raw_aggtrades_v001` | Phase 4bb-F §; `pre_v002_split_policy.py` |
| Normalized family | `microstructure_normalized_aggtrades_v001` | `features_schema.py:49` |
| Feature family | `microstructure_features_aggtrades_v001` (`v001`) / `…_v002` | `features_schema.py:43`; `features_schema_v002.py` |
| Short-horizon label family | `microstructure_labels_aggtrades_v001` (`1s/5s/15s/60s`) | `labels_schema_v002.py` |
| Long-horizon label family | `microstructure_labels_longhorizon_aggtrades_v001` (`5m/30m/1h`) | `longhorizon_labels_schema_v001.py:73,76` |
| Pre-v002 span | 2024-03-01 .. 2024-11-30 UTC; 275 dates; 400,001,695 rows | `pre_v002_split_policy.py:76-77`; Phase 4bn-Y |
| On-disk root (gitignored) | `data/microstructure/{raw,normalized,features,labels,manifests,gate-reports,successor-state}/` | Phase 4bn-L; Phase 4bb-F; `.gitignore:85` |

CF-1 requires **only** the admissible non-reserve pre-v002 BTCUSDT aggTrades already on disk. It
requires **no** new data source, **no** acquisition, and **no** evidence-reserve read. The
realized-variance target and the HAR-style baseline lookbacks are **derived quantities** computed
by the future execution phase from those aggTrades; the committed schema contains **no** prior
realized-variance/realized-volatility column or utility (confirmed: the only committed return
primitive is the signed, backward `rolling_log_return_past_window_{w}` feature and the signed
`forward_log_return_{H}` label — neither is a variance), so the CF-1 target formula below is
authored fresh and duplicates nothing.

## 2. Source field and timestamp semantics (committed)

- **Price field:** the canonical raw last-trade price column `price` (stored as a decimal string;
  `DECIMAL_POLICY_V001`), cast to `float64` **only** for logarithm/return arithmetic — exactly the
  committed convention (`features_compute.py` "float prices for log-return computation only";
  `labels_compute_v002.py:452-453` divides prices in `Decimal` then casts to float at the
  `math.log` step). **No VWAP, no mid-price, no bid/ask, no book, no mark/index price** is used or
  produced. `price`/`mid`/`bid`/`ask`/`mark_price`/`index_price` are committed-forbidden as ML
  columns (`pre_v002_ml_dataset_contract.py FORBIDDEN_RAW_PRICE_COLUMNS`).
- **Timestamp:** UTC Unix **milliseconds**, `int64`, **event time**. Canonical policy
  (`docs/04-data/timestamp-policy.md`): "canonical timestamp format is Unix milliseconds …
  canonical timezone … UTC". Microstructure policy
  `TIMESTAMP_POLICY_V002 = "event_aligned_utc_ms_int64"` with
  `feature_timestamp_ms == source_transact_time_ms == transact_time_ms`
  (`features_schema_v002.py:213`). Split assignment is by each row's `source_transact_time_ms` UTC
  date (`pre_v002_split_policy.py:537`).
- **Alignment keys (committed):** `row_index`, `agg_trade_id`, `feature_timestamp_ms`,
  `source_transact_time_ms`, plus `utc_date`. Strict positional alignment, 0 mismatches, no
  join/reorder/fill (Phase 4bn-AH proof over 400,001,695 rows).
- **Same-timestamp tie-break (committed):** canonical sort `(transact_time_ms ASC, row_index ASC)`;
  within equal timestamps include rows with `row_index ≤ R` (`same_timestamp_tie_rule =
  "row_index_le_R"`).
- **Causality (committed):** windows are causal, trailing, half-open `(T − window_ms, T]`
  (`causal_window_rule = "trailing_right_open_left"`; `LEAKAGE_POLICY_V002 =
  "causal_only_no_future_lookahead"`).

## 3. Target formula (frozen)

CF-1 forecasts **future realized variance** of the BTCUSDT last-trade log price over exactly one
horizon. No direction, sign, return-classification, continuation, reversion, liquidation, or
forced-flow target is used.

Let the forecast origin be `t` (a UTC clock instant, §5). Define a **fixed 1-minute UTC clock
grid**. For grid instants `τ` define the causal grid price

```
P(τ) = last-trade price of the most recent aggTrade with source_transact_time_ms ≤ τ
       (last-observation-carried-forward; same row-index tie-break as committed:
        the largest row_index among trades with transact_time_ms ≤ τ)
```

Intra-window 1-minute log returns over the forecast window `[t, t + H)`:

```
r_k = ln( P(τ_k) / P(τ_{k-1}) ),   τ_k = t + k·60_000 ms,   k = 1 … M,   M = H / 60_000
```

Realized variance of the forecast window:

```
RV(t) = Σ_{k=1}^{M} r_k²
```

Model target (log realized variance, for positivity and QLIKE compatibility):

```
y(t) = ln( RV(t) + ε ),   ε = 1e-16   (fixed floor, squared-log-return units)
```

- **Modelled quantity:** `y(t) = log realized variance`. Because `y(t) = ln(RV(t) + ε)`, the
  exponentiated forecast `exp(ŷ(t))` forecasts the **strictly positive** quantity `RV(t) + ε`,
  consistent with the log target. Forecasts are mapped back to a **variance** forecast
  `ĥ(t) = exp(ŷ(t))` (positive by construction; no ad-hoc bias correction).
- **Actual variance and forecast floor used by the loss (frozen):** the QLIKE loss (§26) uses the
  actual variance `v(t) = RV(t) + ε` and floors each forecast at `ε`
  (`h(t) = max(exp(ŷ(t)), ε)`) with the **same** `ε = 1e-16`, so the loss is finite even when
  `RV(t) = 0`. **No observation is dropped merely because `RV(t) = 0`.**
- **No annualization.** RV and forecasts are per-1-hour-window variances in squared-log-return
  units. (Annualization is a monotone rescaling that does not affect QLIKE ranking; it is omitted
  to avoid an unnecessary constant.)
- **Prices** are combined in `Decimal` and cast to `float64` only at the `ln` step, matching the
  committed label-compute convention.

## 4. Forecast horizon (frozen: exactly one)

**H = 60 minutes = 3,600,000 ms.** Exactly one horizon. `M = 60` one-minute intra-window returns.

Supported by committed temporal semantics: `1h` is a committed forward-window horizon
(`LONGHORIZON_HORIZON_MS` includes `3_600_000`; `longhorizon_labels_schema_v001.py:76`), all
horizons are `< 1` UTC day so cross-day reference resolution is the committed current-day-or-
next-day rule. No sensitivity horizon is included; no menu of executable horizons is produced.

**Alternatives considered and rejected (recorded, not executable):**

| Horizon | Rejected because |
|---|---|
| 5 min | RV from only 5 one-minute returns is a very noisy variance proxy; QLIKE unstable; heavy microstructure-noise contamination. |
| 15 / 30 min | Fewer intra-window returns (15 / 30) → noisier RV; does not align to a well-conditioned HAR hour/day/week cascade as cleanly as 1h. |
| Daily | Only 244 primary execution-access dates → far too few block-level observations; feature→target timescale gap extreme. |
| **60 min (selected)** | 60 one-minute returns → well-conditioned RV; non-overlapping hourly origins; clean HAR hour/day/week cascade; directly supported by the committed `1h` horizon; ≈ 5,856 raw hourly origins over the 244-date primary execution-access window (ample after warmup/embargo). |

## 5. Forecast cadence (frozen)

- **Cadence:** one forecast origin at the **top of each UTC hour** (`HH:00:00.000`).
- **Overlap:** **non-overlapping.** Window `[HH:00, HH+1:00)` for origin `HH:00`. Consecutive
  forecast windows tile the timeline without overlap, so the target series carries no
  construction-induced overlap dependence (residual serial dependence from volatility persistence
  is handled by the block-bootstrap uncertainty method, §29).

## 6. Interval closure (frozen)

- Forecast window: **right-open** `[t, t + H)`.
- 1-minute grid steps: left-anchored at `τ_{k-1}`, return realized at `τ_k`; grid prices use
  causal LOCF (`≤ τ`), consistent with the committed completed-bar / no-look-ahead rule
  (`timestamp-policy.md` "only completed bars may be used") and the committed trailing right-closed
  window convention.
- HAR lookback windows (§17): **left-open, right-closed** `(t − L, t]`, strictly past-only.

## 7. Missing-grid treatment (frozen)

- A grid instant `τ` with **no** aggTrade at or before it within the same admissible development
  segment → `P(τ)` is carried forward from the last available trade (LOCF); if no prior trade
  exists at all in-segment, the origin is **invalid** (§10).
- A 1-minute step whose interval contains **no** actual aggTrade contributes `r_k` from LOCF
  prices (typically `0`, i.e. no observed price change) and is counted as a **non-covered minute**.
- **Coverage rule:** a forecast window is valid only if **≥ 30 of its 60 one-minute steps contain
  ≥ 1 actual aggTrade** (`min_covered_minute_fraction = 0.50`, frozen). A window failing this is
  **invalid** (§10) — dropped, never imputed. The same coverage rule applies to each HAR lookback
  window (§17). No committed aggTrades maintenance-gap registry exists; this conservative coverage
  rule is the frozen mechanism for exchange gaps / thin periods.

## 8. Partial-window treatment (frozen)

Any forecast window (or HAR lookback window) that would extend beyond the frozen CF-1 primary
execution-access boundary (§21) — i.e. before 2024-03-01, onto the 2024-10-01 embargo date, or
requiring any row dated 2024-11-01 or later (the `UNUSED_NON_RESERVE_BUFFER`, the 2024-11-16 embargo,
the consumed holdout, or the v002 terminal / sealed reserves) — is a **partial window → the origin is
invalid** (§10). Partial windows are never truncated, back-filled, or stitched across an envelope
boundary (matching the committed no-cross-envelope-stitch rule).

## 9. Day-boundary treatment (frozen)

- A 1-hour forecast or lookback window **may** cross a UTC-day boundary (all windows `≤ 24h`),
  resolved by the committed current-day-or-next-day reference rule.
- A window may **not** cross the frozen CF-1 primary execution-access boundary (§21), an embargo
  date, the `UNUSED_NON_RESERVE_BUFFER`, or a reserve/holdout boundary (§8, §21–§24).
- `utc_date` for split assignment is derived from `source_transact_time_ms` per the committed rule.

## 10. Valid-target minimum observations (frozen)

A forecast origin `t` yields a **valid** target iff **all** hold:

1. The full window `[t, t+H)` lies inside admissible development data (§21) with no reserve/embargo
   crossing (§8, §9).
2. `≥ 30 of 60` one-minute steps contain `≥ 1` actual aggTrade (§7).
3. All grid prices used are strictly positive and finite (else `label_invalid_price_flag`-style
   invalidation; matches committed null-when-price≤0 rule).
4. The origin's baseline lookbacks (§17) and microstructure snapshot (§11) are all computable and
   valid (§15).

Origins failing any condition are **dropped from both the baseline and the augmented evaluation
identically** (paired sets), never imputed. **Invalid-target rule:** a null/partial/under-covered
target is excluded, not filled.

## 11. Exact feature names (frozen)

The CF-1 microstructure augmentation is **exactly three** committed, sign-invariant feature
columns at the **60s** window, snapshotted causally at the forecast origin:

| # | Committed column | Family | Committed dtype | Rationale |
|---|---|---|---|---|
| x1 | `rolling_aggtrade_count_60s` | trade-arrival intensity | int64 non-null | information-arrival / activity |
| x2 | `rolling_quantity_sum_60s` | unsigned traded-volume intensity | decimal string non-null | liquidity-demand magnitude |
| x3 | `rolling_quantity_mean_60s` | mean trade size (level) | decimal string, `null_when_empty` | trade-size level |

- **Snapshot rule:** the value of each column on the **last aggTrade with
  `source_transact_time_ms ≤ t`** (causal last-observation snapshot; same `row_index_le_R`
  tie-break). Every feature is therefore available at or before the forecast origin.
- **Maximum feature count = 3.** One window (60s) only. No other windows, no other columns.
- **Explicitly excluded directional / non-sign-invariant committed columns:**
  `rolling_aggressive_flow_ratio_{w}`, `rolling_aggressive_quantity_imbalance_{w}`,
  `rolling_aggressive_buy_quantity_{w}`, `rolling_aggressive_sell_quantity_{w}`,
  `rolling_aggressive_buy_count_{w}`, `rolling_aggressive_sell_count_{w}` (buy/sell magnitudes and
  counts carry side identity and are barred as directional inputs), and
  `rolling_log_return_past_window_{w}` (signed return). Also excluded: the time-context columns
  (`utc_hour`, `utc_minute`, `milliseconds_since_day_start`) and quality flags
  (`invalid_window_flag`, `rolling_missing_window_flag`), which are not mechanism features.
- **No dispersion / standard-deviation feature is used, because none exists in the committed
  schema.** The only committed central-moment column is `rolling_quantity_mean`; there is **no**
  `rolling_quantity_std` / variance column. Per the Phase 4bn-AY mandate, a dispersion feature is
  **not invented** during this phase; a smaller three-feature contract supported by existing
  columns is used instead. If a future arc wants a sign-invariant dispersion feature, that requires
  a **separate feature-contract phase** (build a new committed column) — it is out of scope here.

## 12. Feature lookbacks (frozen)

- Every microstructure feature is the committed **60s** trailing-window value
  (`(t_last − 60_000 ms, t_last]`, `trailing_right_open_left`, where `t_last` is the snapshot
  trade's `transact_time_ms ≤ t`).
- No other lookback, no window search, no multi-window stacking.

## 13. Feature transformations (frozen)

- Each of `x1, x2, x3` is transformed by **natural logarithm** `ln(·)` (all three are strictly
  positive at any valid origin — a valid origin requires `rolling_quantity_mean_60s` non-null,
  which by the committed `null_when_empty` policy implies `≥ 1` trade in the 60s window, hence
  `count ≥ 1`, `quantity_sum > 0`, `quantity_mean > 0`). The log matches the multiplicative,
  heavy-tailed nature of counts/volumes and the log-variance target space.
- Then **train-only z-score standardization** (§14, §25).
- No other transform. No interactions, no polynomial expansion, no ratios, no differencing.

## 14. Scaling / clipping (frozen)

- **Standardization (microstructure features only):** `z_j = (ln x_j − μ_j^train) /
  max(σ_j^train, 1e-8)`, with `μ_j^train`, `σ_j^train` fitted on the **expanding training origins
  only** for each evaluation block (§23, §25). `STANDARDIZATION_EPSILON = 1e-8`, matching the
  committed `ml_baseline_design_v002` standardization epsilon.
- **No clipping, no winsorization** of features or target (frozen: none). Extreme values are
  retained; QLIKE robustness (§26) and the log transforms already temper tails.
- **HAR log-RV regressors are left unstandardized** in `ln(RV+ε)` units; OLS forecasts are
  invariant to linear rescaling of regressors, and leaving them raw keeps the baseline auditable.

## 15. Missing-feature treatment (frozen)

- If the origin's microstructure snapshot column `rolling_quantity_mean_60s` is null
  (`null_when_empty` — no trade in the 60s window) → the origin is **invalid** (§10) and dropped
  from **both** models.
- No imputation of any feature. No forward-fill of feature values across invalid windows (matches
  committed `no_imputation_across_invalid_windows`). No NaN/Inf permitted in any model input
  (matches committed `no_nan_no_inf_for_floats`); a non-finite input → invalid origin.

## 16. Directional-feature exclusions (frozen, absolute)

CF-1 uses **no** directional information. The following are prohibited as features or targets:
signed aggressor imbalance; buy/sell directional flow ratio; separate aggressive buy vs sell
quantities or counts; forward return sign; signed returns; momentum; continuation; reversion;
funding-directional triggers; liquidation or forced-flow proxies; the CF-3 calendar/funding/OI
bundle; open interest; order-book / top-of-book / bookTicker data; any newly acquired data; any
feature family not present in the committed schema; any feature selected by observed
correlation/importance; interaction searches; polynomial expansion; arbitrary window search;
feature ablation used to rescue a failure.

## 17. Baseline equation / specification (frozen)

A simple, auditable **HAR-style realized-variance** baseline (heterogeneous autoregressive cascade
at the hour / day / week timescales available in the 244-date primary execution-access window, §21).
All lookbacks are computed with the **same 1-minute-grid RV machinery** as the target (§3), strictly
past-only, `(t − L, t]`:

```
RV_h(t) = realized variance over the previous 1 hour   [t − 1h,   t)   (60 one-minute r_k²)
RV_d(t) = mean of the 24 trailing hourly RVs over       [t − 24h,  t)
RV_w(t) = mean of the 168 trailing hourly RVs over      [t − 168h, t)   (7 days)
```

Baseline model (OLS in log space):

```
y(t) = β0 + β1·ln(RV_h(t)+ε) + β2·ln(RV_d(t)+ε) + β3·ln(RV_w(t)+ε) + u(t)
ŷ_base(t) = β̂0 + β̂1·ln(RV_h+ε) + β̂2·ln(RV_d+ε) + β̂3·ln(RV_w+ε)
ĥ_base(t) = exp( ŷ_base(t) )        (variance forecast; positive by construction)
```

- **Exactly one baseline. No baseline shopping; no alternate baseline promoted after execution.**
- Each lookback window obeys the §7 coverage rule and §8 partial-window rule; an origin whose HAR
  lookbacks are not all computable/valid is **invalid**. The week lookback requires ≥ 168h of prior
  admissible data → a warmup of the first ~7 days of the development window is train-only /
  non-evaluable.
- **Intercept included.** No tuning, no lag search, no alternate cascade. Estimation §19.

## 18. Augmented equation / specification (frozen)

A **nested, low-complexity** extension of the baseline adding only the three §11 sign-invariant
microstructure features (identical target, identical training window, identical estimation,
identical forecast origin, identical preprocessing scope):

```
y(t) = β0 + β1·ln(RV_h+ε) + β2·ln(RV_d+ε) + β3·ln(RV_w+ε)
            + γ1·z1(t) + γ2·z2(t) + γ3·z3(t) + u(t)
ĥ_aug(t) = exp( ŷ_aug(t) )
```

where `z1,z2,z3` are the train-standardized log microstructure features (§13, §14).

- **Nesting:** the baseline is exactly the augmented model with `γ1=γ2=γ3=0`. This isolates
  **incremental microstructure information** rather than model-class superiority — the two models
  share target, geometry, estimator, training window, forecast origins, and preprocessing; they
  differ **only** by the three microstructure regressors.
- **No model-class search, no feature selection, no regularization search, no post-hoc interaction,
  no alternate augmented specification after results.** Exactly one augmented model.

## 19. Estimation method (frozen)

- **Ordinary least squares (OLS)** via the normal equations (or an equivalent numerically-stable
  linear solver), closed-form and deterministic. No regularization; **no tunable hyperparameter**;
  no iterative optimizer; hence no learning rate, epochs, batch size, or seed for estimation.
- If a regularization parameter were ever deemed necessary it would violate the "no tunable
  hyperparameter" rule; the frozen choice is a model requiring **no** tunable hyperparameter (plain
  OLS), so no ex-ante tuning rule is needed.
- **Numerical guards (fail-closed → CF1_INVALID_RUN, §31):** training design-matrix condition
  number `> 1e10`, any zero-variance training regressor, a singular normal-equations matrix,
  non-finite coefficients, or fewer than `10 × (#parameters)` training origins (i.e. `< 70` for the
  augmented model) each make the run an **invalid run**, never a silently-simplified model and
  never a scientific pass or fail.

## 20. Positivity handling (frozen)

Variance forecasts are `ĥ(t) = exp(ŷ(t)) > 0` by construction (log-space modelling + exponential
inverse). As a **numerical safeguard only**, the QLIKE loss (§26) evaluates each forecast as
`h(t) = max(exp(ŷ(t)), ε)` with the same `ε = 1e-16`, guaranteeing a strictly-positive, finite
denominator even under floating-point underflow; this floor can only raise an already-positive
value away from an underflow-to-zero and is **not** a tunable choice. The actual variance used by
the loss is `v(t) = RV(t) + ε` (§3, §26), also strictly positive. **No negative-variance clipping,
and no post-hoc clipping of the QLIKE ratio or loss, is ever applied.** The target floor `ε = 1e-16`
(§3) additionally handles the rare exact-zero RV window before the logarithm. The floor `ε` is the
single frozen constant shared by the target, the actual, and the forecast; no alternative floor may
be chosen during execution.

## 21. Development dates (frozen)

Two distinct boundaries must not be conflated:

**(a) Committed non-reserve eligibility envelope** (what committed split metadata classifies as
pre-v002 non-reserve development-eligible) = pre-v002 train ∪ validation = **259 admissible UTC
dates**:

```
Train region:      2024-03-01 .. 2024-09-30   (214 dates)
Validation region: 2024-10-02 .. 2024-11-15   (45 dates)
```

Committed source: `pre_v002_split_policy.py:76-90`; Phase 4bn-Y; boundary constants
`BOUNDARY_TRAIN_VALIDATION_MS = 1727827200000` (2024-10-02T00:00Z),
`BOUNDARY_VALIDATION_HOLDOUT_MS = 1731801600000` (2024-11-17T00:00Z).

**(b) Frozen CF-1 primary execution-access boundary** (what the primary CF-1 experiment may open and
use) = **`2024-03-01 through 2024-10-31 UTC, excluding 2024-10-01`** = **244 UTC dates**. Within it:
March 2024 supplies warmup and initial expanding-window training history; April–October 2024 supply
the seven fixed evaluation blocks (§22); 2024-10-01 is the fixed one-calendar-day embargo before the
October evaluation block, which begins 2024-10-02. That committed metadata classifies dates through
2024-11-15 as non-reserve **does not** authorize their use in the frozen CF-1 primary experiment.
The last October forecast window's terminal 1-minute grid instant (2024-11-01T00:00:00.000Z) is
resolved by causal LOCF from **in-access** trades only (`source_transact_time_ms ≤ 2024-10-31
T23:59:59.999Z`); **no** 2024-11-01..2024-11-15 row is opened for it.

**Frozen: `2024-11-01 through 2024-11-15 = UNUSED_NON_RESERVE_BUFFER`.** This buffer **is not** part
of any training set, any evaluation block, the bootstrap, a confirmation set, a holdout, a fallback
block, preprocessing, threshold choice, or diagnostics; it is **not** plotted or interpreted; and it
**must not be opened or loaded** by the primary execution phase.

**Excluded / non-access dates:**

| Item | Dates | Reason |
|---|---|---|
| October boundary embargo | 2024-10-01 | committed `1D_BOUNDARY_EMBARGO` purge date; outside execution access |
| **Unused non-reserve buffer** | **2024-11-01 .. 2024-11-15 (15)** | `UNUSED_NON_RESERVE_BUFFER`; non-reserve-eligible but **unopened and unused**; outside the frozen CF-1 primary experiment |
| Validation/holdout boundary embargo | 2024-11-16 | committed `1D_BOUNDARY_EMBARGO` purge date; outside the primary experiment |
| Consumed holdout | 2024-11-17 .. 2024-11-30 (14) | `PRE_V002_INTERNAL_HOLDOUT = CONSUMED`; never a CF-1 evaluation/confirmation set; must not be opened for CF-1 confirmation; descriptive-only |
| v002 terminal window | 2024-12-01 .. 2025-02-28 (90) | `UNTOUCHED_RESERVED`; excluded; `v002_terminal_window_read = false` |
| v002 sealed test | 2025-02-14 .. 2025-02-28 (15) | `UNTOUCHED_RESERVED` highest protection; excluded; `test_rows_loaded = 0` |

`test_rows_loaded = 0` is preserved. The consumed pre-v002 internal holdout is **not** relabeled
into a fresh CF-1 evaluation or confirmation set; it may be cited descriptively only.

## 22. Evaluation-block dates (frozen)

**K = 7 contiguous, non-overlapping, full UTC calendar-month evaluation blocks:**

| Block | Dates | Notes |
|---|---|---|
| B1 | 2024-04-01 .. 2024-04-30 | |
| B2 | 2024-05-01 .. 2024-05-31 | |
| B3 | 2024-06-01 .. 2024-06-30 | |
| B4 | 2024-07-01 .. 2024-07-31 | |
| B5 | 2024-08-01 .. 2024-08-31 | |
| B6 | 2024-09-01 .. 2024-09-30 | |
| B7 | 2024-10-02 .. 2024-10-31 | October; 2024-10-01 excluded (committed embargo date) |

- **Warmup / initial training history (train-only, never evaluated):** 2024-03-01 .. 2024-03-31
  (provides the ≥168h HAR-week warmup and initial fit rows).
- **`UNUSED_NON_RESERVE_BUFFER` (never opened, never trained, never evaluated, never bootstrapped):**
  2024-11-01 .. 2024-11-15 — outside the frozen CF-1 primary execution-access boundary (§21). An
  explicit, deliberate non-use, not a silent drop.
- **Committed embargo exclusion:** 2024-11-16 remains excluded under committed split/embargo
  metadata and is outside the primary experiment.
- The last evaluation block is B7 (October); no evaluation block, training set, or bootstrap uses any
  date on or after 2024-11-01.
- Blocks are keyed to UTC dates; forecast origins inside a block are the hourly origins whose full
  1h window lies within the frozen CF-1 primary execution-access boundary (§8–§10, §21).

## 23. Training-window rule (frozen)

- **Expanding (anchored) walk-forward.** For evaluation block `B_i` beginning at `d_i` 00:00 UTC,
  fit both models on **all admissible development origins whose forecast window ends `≤ d_i` 00:00
  UTC minus the embargo gap** (§24). Training always precedes the evaluated block in time.
- **Minimum training history:** the augmented model has 7 parameters; require `≥ 70` valid training
  origins (§19). Satisfied from B1 onward (the March warmup alone yields hundreds of hourly
  origins after the 168h week-warmup and 1-day embargo).
- **No rolling-window variant, no re-fit inside a block** (one fit per block, applied to all origins
  in that block). No look-ahead: a block is never used to fit its own model.

## 24. Purge and embargo (frozen)

- **Embargo = 1 calendar day (24h)** between the end of each expanding training window and the
  start of its evaluation block: training origins whose forecast window ends within the 24h
  immediately preceding `d_i` 00:00 UTC are dropped. This matches the committed
  `CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO` 1-day-boundary convention and
  exceeds the 1h horizon.
- **Purge = the forecast horizon (1h)**, subsumed by the 1-day embargo: no training origin's 1h
  forward window may overlap the embargo gap or the evaluation block.
- **Maximum feature lookback at boundaries:** the 168h HAR-week lookback of an early
  block-`B_i` origin reaches back into training data — this is **past data and is permitted** (not
  leakage). The embargo constrains only the **forward** direction. No evaluation origin's lookback
  may reach across the outer development-window start (2024-03-01); the first ~7 days are therefore
  warmup-only.
- **No-overlap rule:** training and evaluation origin sets are disjoint (embargo); evaluation
  forecast windows are mutually non-overlapping (hourly, 1h); no window spans a train/eval boundary.
- **No randomization; no resampling across time; no shuffled CV; no k-fold-over-time.** Purely
  chronological, matching the committed split policy.

## 25. Preprocessing fit scope (frozen)

- **All preprocessing is fitted on the training origins of each block only** (the expanding window
  up to the embargo), then applied to that block. This covers the microstructure-feature
  `μ^train, σ^train` (§14).
- **No global statistic** is computed across training and evaluation periods; **no evaluation block
  influences any preprocessing fitted for itself**; no statistic pools any future block.
- HAR regressors are unstandardized (§14), so they carry no fitted preprocessing state.

## 26. Primary loss formula (frozen)

**QLIKE** (quasi-likelihood), the single primary loss, with a fixed zero-RV safeguard so the loss is
always finite. Per valid origin `t`, for model `m ∈ {B (baseline), A (augmented)}`, using the same
`ε = 1e-16` throughout:

```
v(t)         = RV(t) + ε                       # actual variance used by the loss (strictly positive)
h_m(t)       = max( exp(ŷ_m(t)), ε )           # forecast variance, floored at ε (strictly positive)
ratio_m(t)   = v(t) / h_m(t)
QLIKE_m(t)   = ratio_m(t) − ln( ratio_m(t) ) − 1        (≥ 0; = 0 iff v = h)
```

- **Lower is better.**
- **Frozen numerical requirements:** `v(t) > 0`; `h_m(t) > 0`; `ratio_m(t)`, `ln(ratio_m(t))`, and
  `QLIKE_m(t)` must all be finite. The **same** `ε` and the **same** formula apply to **both**
  models. Any non-finite actual, forecast, ratio, logarithm, or QLIKE value is a **technical
  invalidation condition** (`CF1_INVALID_RUN`, §31). **No observation may be silently dropped solely
  because `RV(t) = 0`** (the `ε` floor keeps it well-defined); **no alternative floor** may be chosen
  during execution; **no post-hoc clipping** of the ratio or loss is permitted.
- **Aggregation within a block:** arithmetic mean of `QLIKE_m(t)` over block `i`'s `n_i` valid
  paired origins → `QLIKE_block,i(m)`.
- **Aggregation across blocks (the primary estimand):** **equal-weighted mean of the 7
  `QLIKE_block,i(m)` values** → `QLIKE(m)` (per model). Equal block weighting prevents any single
  large block dominating. **An origin-count-weighted "pooled" mean over all origins is NOT used in
  any decision**; if reported at all it is descriptive-only and is never the primary or the bootstrap
  estimand.
- **Why QLIKE:** it is one of the two loss functions (with MSE) that are *robust* — i.e. yield
  consistent forecast rankings under a **noisy** volatility proxy (Patton, 2011) — and, unlike
  MSE, QLIKE is far less sensitive to the heavy right tail of realized variance and is invariant
  to the volatility scale, matching a magnitude-forecasting question over a regime-varying
  development window. It is a proper scoring rule for variance forecasts. The choice is justified
  independently of any external reviewer; **Fable's illustrative 3–5% QLIKE margin is not adopted.**

## 27. Relative-improvement formula and primary estimand (frozen)

The primary statistic is an **equal-weighted mean of the seven block-level mean loss differentials**.
For evaluation block `i ∈ {1,…,7}` and valid forecast origin `t` within block `i`:

```
d_{i,t} = QLIKE_baseline(i,t) − QLIKE_augmented(i,t)        # positive ⇒ augmented better

D_i     = (1 / n_i) · Σ_t d_{i,t}                          # block-i mean differential; n_i = valid paired origins in block i

Δ_equal = (1 / 7) · Σ_{i=1}^{7} D_i                        # PRIMARY equal-weighted point estimate
```

`Δ_equal` is identically the equal-weighted-block-mean improvement previously written
`ΔQLIKE_blockmean` (`Δ_equal ≡ (1/7) Σ_i ( QLIKE_block,i(base) − QLIKE_block,i(aug) )`); the two names
denote the **same** estimand and `Δ_equal` is the frozen symbol used by the pass rule.

- **Primary pass condition P1:** `Δ_equal > 0` (strict; zero-floor per §28).
- **Relative improvement (descriptive only):** `ρ = Δ_equal / QLIKE(base)` — reported for
  interpretability; it does **not** enter the pass rule.

The primary decision uses `Δ_equal` (point estimate, P1), block consistency (§30, P2), and the
stratified moving-block bootstrap of the **same** `Δ_equal` estimand (§29, P3). No origin-count
weighting and no cross-block pooling is used at any decision stage.

## 28. Materiality floor or zero-floor rationale (frozen)

- **No nonzero materiality floor is adopted.** No committed project logic supplies a principled
  QLIKE materiality threshold, and Fable's illustrative 3–5% margin is explicitly not repository
  policy and not adopted.
- **Zero-floor rule:** the pass rule requires **strictly positive** improvement (`Δ_equal > 0`, §27)
  plus block consistency (§30) plus the bootstrap lower-bound criterion `LB_95 > 0` (§29).
- **Explicit caveat (frozen):** a small strictly-positive result establishes only **statistical
  incremental information** on the magnitude axis; it establishes **no** economic materiality, **no**
  direction, **no** profitability, **no** ability to clear the locked 16 bps round-trip, and **no**
  tradability.

## 29. Uncertainty procedure (frozen: exactly one)

**Stratified-by-evaluation-block moving-block bootstrap** that estimates uncertainty for the **same**
`Δ_equal` estimand as the primary point estimate (§27), and is compatible with serially-dependent
chronological forecast errors (RV persistence). It keeps the seven evaluation blocks separate and
never pools origins across blocks or weights blocks by their origin counts.

**Exact procedure:**

1. Keep the seven evaluation blocks separate.
2. Within each block `i`, preserve chronological order and form the series `{d_{i,t}}` (§27).
3. Use a **block-specific** moving-block length `ℓ_i = ceil(n_i^(1/3))` (`n_i` = valid paired origins
   in block `i`; deterministic).
4. For bootstrap replicate `b`, resample moving blocks **within each evaluation block independently**
   until `n_i` observations are obtained; truncate the final sampled block to exactly `n_i`. No
   moving block ever spans an evaluation-block boundary.
5. Compute `D_i^(b) = mean( d_{i,*}^{(b)} )` for each block `i`.
6. Compute the bootstrap primary statistic `Δ_equal^(b) = (1/7) · Σ_{i=1}^{7} D_i^(b)`.
7. Repeat for exactly `B = 10,000` replicates using `RNG_SEED = 20260715`.
8. Define the one-sided 95% percentile lower bound `LB_95 = empirical_quantile({Δ_equal^(b)}, 0.05)`.
9. **P3 passes iff `LB_95 > 0`.**

| Field | Frozen value |
|---|---|
| Estimand | the equal-weighted seven-block `Δ_equal` (§27) — the **same** as the primary point estimate |
| Method | stratified-by-block moving-block bootstrap; within-block resampling only |
| Resampling unit | contiguous moving blocks of `{d_{i,t}}` **within** each evaluation block |
| Block length | block-specific `ℓ_i = ceil(n_i^(1/3))` |
| Recombination | equal-weighted average of the seven bootstrap block means `D_i^(b)` |
| Number of resamples | `B = 10,000` |
| Confidence level | one-sided **95%** |
| Exact null | `H0: E[d_{i,t}] = 0` (equal expected QLIKE) |
| Decision direction | PASS-support iff `LB_95 = quantile({Δ_equal^(b)}, 0.05) > 0` |
| Random-seed policy | fixed `RNG_SEED = 20260715` (frozen); the bootstrap is the **only** stochastic step |

**Frozen rules:**

- **No pooling** of all per-origin observations into one sequence.
- **No weighting** of evaluation months by their number of valid origins (equal-weight the 7 block
  means, exactly as the primary estimand).
- **No resampling across evaluation-block boundaries.**
- **Not** an IID bootstrap / IID standard errors (incompatible with serially-dependent forecasts).
- **No alternate bootstrap, analytical standard error, IID test, Diebold–Mariano variant, or residual
  diagnostic may replace this method after execution.** A Diebold–Mariano/Newey–West figure may be
  **reported descriptively** but is **not** the frozen decision test.
- **Block consistency P2 (§30) remains separate:** at least 6 of the 7 observed `D_i` values must be
  strictly positive. The bootstrap may not replace the 6-of-7 rule, and the 6-of-7 rule may not
  replace the bootstrap.

## 30. Block-consistency rule (frozen)

- Compute `D_i = QLIKE_block,i(base) − QLIKE_block,i(aug)` for each of the 7 blocks (§27).
- **Block consistency holds iff `D_i > 0` (augmented strictly better) in ≥ 6 of the 7 blocks.**
- All 7 block values are recorded regardless. Block consistency is a **required, independent** pass
  condition; it is **not** replaceable by the stratified moving-block bootstrap (§29), and the
  bootstrap is **not** replaceable by block consistency.

## 31. Pass / fail / invalid pseudocode (frozen)

```text
# Preconditions: run executed exactly per this contract at the pinned preregistration SHA,
# on admissible development data only, reserves untouched.

if any INVALID_RUN condition holds:
    #  target-contract violation; feature-contract violation; split leakage;
    #  reserve access (terminal / sealed / consumed-holdout-as-confirmation);
    #  any 2024-11-01..2024-11-15 buffer row opened or used (§21, §22);
    #  preprocessing leakage (global stats or eval-block-fitted preprocessing);
    #  timestamp misalignment; a missing required block, or any block with
    #    < MIN_BLOCK_VALID_ORIGINS = 100 valid paired origins;
    #  material implementation mismatch vs this contract;
    #  numerical failure (singular matrix, zero-variance regressor, condition number > 1e10,
    #    non-finite actual / forecast / ratio / logarithm / QLIKE / coefficient value,
    #    < 70 training origins) preventing the preregistered comparison;
    #  any unauthorized change of model / metric / horizon / cadence / threshold / feature / window / loss.
    verdict = CF1_INVALID_RUN            # no scientific claim; separate corrective phase + new operator authorization

elif ( Δ_equal > 0 )                                            # P1 strict positive improvement (§27)
     and ( count_i[ D_i > 0 ] >= 6 of 7 )                       # P2 block consistency (§30)
     and ( LB_95 > 0 ):                                         # P3 uncertainty: stratified boot lower bound (§29)
    verdict = CF1_VALID_PASS

else:                                                          # any valid run failing P1, P2, or P3
    verdict = CF1_VALID_FAIL
```

- A **valid pass** requires **all** of P1, P2, P3 **and** run validity simultaneously.
- A **valid fail** is every scientifically valid run not meeting the full pass rule. There is **no**
  borderline / promising / weak / partial pass, **no** pass on a secondary metric, and **no** pass
  on a post-hoc subset.
- An **invalid run** is not interpretable scientifically (neither pass nor fail); it requires a
  separate corrective phase and a new operator authorization.

## 32. Random-seed policy (frozen)

- OLS estimation is deterministic (no seed).
- The moving-block bootstrap uses `RNG_SEED = 20260715` (frozen). This is the only stochastic step;
  results are reproducible bit-for-bit given the seed, `B`, and `ℓ`.

## 33. Output artefact contract for a later phase (frozen; nothing produced now)

A future, separately-authorized execution phase must emit (all **local / gitignored** under
`data/research/…`; **no data file committed**; Phase 4bn-L caps respected):

- a **realized-variance target layer** (per-origin `RV(t)`, `y(t)`, HAR lookbacks `RV_h/RV_d/RV_w`,
  the three microstructure snapshots, split/block assignment) — compact Parquet;
- a **leakage / split / coverage proof** validated **before** any metric is computed: chronological
  block boundaries; embargo/purge applied; per-block valid-origin counts `n_i`; `≥30/60` coverage
  enforced; primary execution-access boundary respected (no 2024-11-01..2024-11-15 buffer row opened,
  §21); `v002_terminal_window_read = false`; `sealed_test_split_touched = false`;
  `test_rows_loaded = 0`; consumed-holdout not used;
- a **model-run manifest**: the frozen constants of this contract (H, cadence, `ε = 1e-16`, feature
  list, HAR spec, OLS, QLIKE with the `v = RV+ε` / `h = max(exp(ŷ),ε)` safeguard, bootstrap
  `seed = 20260715` / `B = 10,000` / block-specific `ℓ_i`); per-block `QLIKE_block,i(base)`,
  `QLIKE_block,i(aug)`, and `D_i`; the equal-weighted `QLIKE(base)`, `QLIKE(aug)`, `Δ_equal`, `ρ`;
  the bootstrap `LB_95`; the two secondary metrics (§ main memo); the P1/P2/P3 booleans; and the
  single `CF1_VALID_PASS | CF1_VALID_FAIL | CF1_INVALID_RUN` verdict;
- per-Parquet `.sha256` sidecars + inventory (Phase 4bb-F).

## 34. Required sidecar / provenance fields for a later phase (frozen)

Per Phase 4bb-F, every emitted JSON artefact carries: `created_at_unix_ms`, `created_at_utc` (ISO
8601 µs + `Z`), `code_commit_sha` (40-char), `base_main_commit_sha` (40-char); every Parquet has a
`.sha256` sidecar `<json-sha256>␠␠<basename>\n`; gate-report / successor-state filenames follow the
committed `<family>__<version>__…__<unix_ms>__<short_commit>.json` convention; and the
non-authorization flags `ml_authorized`, `diagnostics_authorized`, `strategy_authorized`,
`signals_authorized`, `pnl_authorized`, `backtest_authorized`, `live_authorized`,
`exchange_write_authorized` are all **`false`**.

## 35. Explicit prohibited deviations (frozen)

The future execution phase may **not**: change the target family / RV estimator / sampling grid /
floor `ε = 1e-16` (shared by target, actual `v`, and forecast `h`); change the QLIKE safeguard
(`v = RV+ε`, `h = max(exp(ŷ),ε)`) or apply post-hoc clipping to the ratio or loss; drop an
observation solely because `RV = 0`; change the horizon (1h), cadence (hourly non-overlapping), or
window closure; add, remove, transform-differently, re-window, or select features; introduce any
directional / signed / funding / calendar / OI / order-book / forced-flow / liquidation input;
switch the baseline or the augmented model class; add regularization, ensembling, trees, or neural
nets; tune any hyperparameter; change the loss, add a competing loss as decision-primary, or switch
to a secondary metric as primary; change the block count / boundaries / embargo / purge; **open or
use any 2024-11-01..2024-11-15 buffer row** (§21, §22), or extend the primary execution access beyond
2024-10-31; exclude adverse dates or blocks post hoc; mine subgroups / regimes; reclassify an invalid
run as a fail or pass; use the consumed holdout as fresh confirmation; read the v002 terminal or
sealed reserves; pool origins across blocks, weight blocks by origin count, resample across
evaluation-block boundaries, alter the bootstrap seed / `B` / block-specific `ℓ_i`, or run multiple
uncertainty tests and select the best; or interpret any result before the artefact hashes and the
leakage/split proof validate. Any such deviation makes the run `CF1_INVALID_RUN` (§31).

---

**No market data, feature row, label row, model output, diagnostic output, or evidence reserve was
opened or read to author this contract. No target generation, feature generation, model fitting,
diagnostic, backtest, PnL analysis, data acquisition, paper, shadow, live, or exchange-write
execution is authorized by this contract. This contract freezes the CF-1 development experiment but
does not authorize it to run.**
