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

- **Modelled quantity:** `y(t) = log realized variance`. Forecasts are produced in `y`-space and
  mapped back to a **variance** forecast `ĥ(t) = exp(ŷ(t))` (positivity guaranteed by
  construction; no ad-hoc bias correction, no truncation).
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
| Daily | Only 259 development dates → far too few block-level observations; feature→target timescale gap extreme. |
| **60 min (selected)** | 60 one-minute returns → well-conditioned RV; non-overlapping hourly origins; clean HAR hour/day/week cascade; directly supported by the committed `1h` horizon; ≈ 6,216 raw hourly origins over 259 days (ample after warmup/embargo). |

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

Any forecast window (or HAR lookback window) that would extend beyond the available admissible
development data, across the outer development-window boundary, across an embargo date, or into the
consumed holdout / v002 terminal / v002 sealed windows is a **partial window → the origin is
invalid** (§10). Partial windows are never truncated, back-filled, or stitched across an envelope
boundary (matching the committed no-cross-envelope-stitch rule).

## 9. Day-boundary treatment (frozen)

- A 1-hour forecast or lookback window **may** cross a UTC-day boundary (all windows `≤ 24h`),
  resolved by the committed current-day-or-next-day reference rule.
- A window may **not** cross the outer development-window boundary, an embargo date, or a
  reserve/holdout boundary (§8, §21–§24).
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
at the hour / day / week timescales available in the 259-day development window). All lookbacks are
computed with the **same 1-minute-grid RV machinery** as the target (§3), strictly past-only,
`(t − L, t]`:

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
inverse). No negative-variance clipping, no flooring of forecasts, no truncation is ever applied.
The target floor `ε = 1e-16` (§3) handles the rare exact-zero RV window before the logarithm.

## 21. Development dates (frozen)

**CF-1 development window = pre-v002 train ∪ validation = 259 admissible UTC dates:**

```
Train region:      2024-03-01 .. 2024-09-30   (214 dates)
Validation region: 2024-10-02 .. 2024-11-15   (45 dates)
```

Committed source: `pre_v002_split_policy.py:76-90`; Phase 4bn-Y; boundary constants
`BOUNDARY_TRAIN_VALIDATION_MS = 1727827200000` (2024-10-02T00:00Z),
`BOUNDARY_VALIDATION_HOLDOUT_MS = 1731801600000` (2024-11-17T00:00Z).

**Excluded dates:**

| Excluded | Dates | Reason |
|---|---|---|
| Boundary embargo | 2024-10-01; 2024-11-16 | committed `1D_BOUNDARY_EMBARGO` purge dates |
| Consumed holdout | 2024-11-17 .. 2024-11-30 (14) | `PRE_V002_INTERNAL_HOLDOUT = CONSUMED`; never a CF-1 evaluation/confirmation set; descriptive-only |
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
- **Reserved buffer (unused; never evaluated, never trained-forward):** 2024-11-01 .. 2024-11-16 —
  left as a clean chronological buffer between the last evaluation block and the consumed-holdout
  boundary (2024-11-17). Recorded as an explicit, deliberate non-use, not a silent drop.
- Blocks are keyed to UTC dates; forecast origins inside a block are the hourly origins whose full
  1h window lies within admissible development data (§8–§10).

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

**QLIKE** (quasi-likelihood), the single primary loss. Per valid origin, with realized variance
`σ²(t) = RV(t)` (floored by `ε`) and forecast variance `ĥ(t)`:

```
L(t) = σ²(t)/ĥ(t) − ln( σ²(t)/ĥ(t) ) − 1        (≥ 0; = 0 iff σ² = ĥ)
```

- **Lower is better.**
- **Aggregation within a block:** arithmetic mean of `L(t)` over the block's valid origins →
  `QLIKE_block`.
- **Aggregation across blocks:** **equal-weighted mean of the 7 `QLIKE_block` values** →
  `QLIKE` (per model). Equal block weighting prevents any single large block dominating. (The
  origin-pooled mean is additionally reported as a descriptive figure only.)
- **Why QLIKE:** it is one of the two loss functions (with MSE) that are *robust* — i.e. yield
  consistent forecast rankings under a **noisy** volatility proxy (Patton, 2011) — and, unlike
  MSE, QLIKE is far less sensitive to the heavy right tail of realized variance and is invariant
  to the volatility scale, matching a magnitude-forecasting question over a regime-varying
  development window. It is a proper scoring rule for variance forecasts. The choice is justified
  independently of any external reviewer; **Fable's illustrative 3–5% QLIKE margin is not adopted.**

## 27. Relative-improvement formula (frozen)

Per origin loss differential (positive ⇒ augmented better):

```
d(t) = L_base(t) − L_aug(t)
```

Point estimates:

```
ΔQLIKE_blockmean = (1/7) Σ_i ( QLIKE_block,i(base) − QLIKE_block,i(aug) )   ← primary point estimate
ρ                = ΔQLIKE_blockmean / QLIKE(base)                            ← relative improvement (descriptive)
```

The primary decision uses `ΔQLIKE_blockmean` (point estimate), block consistency (§30), and the
bootstrap CI (§29). `ρ` is reported for interpretability only and does not enter the pass rule.

## 28. Materiality floor or zero-floor rationale (frozen)

- **No nonzero materiality floor is adopted.** No committed project logic supplies a principled
  QLIKE materiality threshold, and Fable's illustrative 3–5% margin is explicitly not repository
  policy and not adopted.
- **Zero-floor rule:** the pass rule requires **strictly positive** improvement (`ΔQLIKE_blockmean
  > 0`) plus block consistency (§30) plus the bootstrap lower-bound criterion (§29).
- **Explicit caveat (frozen):** a small strictly-positive result establishes only **statistical
  incremental information** on the magnitude axis; it establishes **no** economic materiality, **no**
  direction, **no** profitability, **no** ability to clear the locked 16 bps round-trip, and **no**
  tradability.

## 29. Uncertainty procedure (frozen: exactly one)

**Moving-block bootstrap** of the per-origin QLIKE loss-differential series, chosen to be
compatible with serially-dependent chronological forecast errors (RV persistence):

| Field | Frozen value |
|---|---|
| Comparison statistic | pooled mean `d̄` of `d(t)` over all valid paired origins (chronological concatenation across B1..B7) |
| Method | moving-block bootstrap (fixed non-overlapping-position resampling of contiguous blocks of `d(t)`) |
| Resampling unit | contiguous blocks of the per-origin `d(t)` series |
| Block length | `ℓ = ⌈ n^(1/3) ⌉`, `n` = number of valid paired origins (deterministic; standard rule) |
| Number of resamples | `B = 10_000` |
| Confidence level | one-sided **95%** |
| Interpretation | one-sided (H1: augmented better ⇒ `E[d] > 0`) |
| Exact null | `H0: E[d(t)] = 0` (equal expected QLIKE) |
| Decision direction | PASS-support iff the one-sided 95% bootstrap **lower bound of `d̄` is > 0** |
| Random-seed policy | fixed `RNG_SEED = 20260715` (frozen; date-derived, matching the committed seed convention); the bootstrap is the **only** stochastic step |
| Aggregation across blocks | the block structure is preserved by the moving-block resampling; block consistency (§30) is enforced separately and is **not** replaced by this test |

- **Not** IID bootstrap / IID standard errors (incompatible with serially-dependent forecasts).
- The uncertainty method is **fixed here, before any residual is seen**; exactly one test is run;
  **no** competing test is run and the most favorable selected. A Diebold–Mariano/Newey–West
  statistic may be **reported descriptively** but is **not** the frozen decision test and cannot
  override the moving-block bootstrap.

## 30. Block-consistency rule (frozen)

- Compute `ΔQLIKE_block,i = QLIKE_block,i(base) − QLIKE_block,i(aug)` for each of the 7 blocks.
- **Block consistency holds iff `ΔQLIKE_block,i > 0` (augmented strictly better) in ≥ 6 of the 7
  blocks.**
- All 7 block values are recorded regardless. Block consistency is a **required, independent** pass
  condition; it is **not** replaceable by the pooled uncertainty test (§29).

## 31. Pass / fail / invalid pseudocode (frozen)

```text
# Preconditions: run executed exactly per this contract at the pinned preregistration SHA,
# on admissible development data only, reserves untouched.

if any INVALID_RUN condition holds:
    #  target-contract violation; feature-contract violation; split leakage;
    #  reserve access (terminal / sealed / consumed-holdout-as-confirmation);
    #  preprocessing leakage (global stats or eval-block-fitted preprocessing);
    #  timestamp misalignment; a missing required block, or any block with
    #    < MIN_BLOCK_VALID_ORIGINS = 100 valid paired origins;
    #  material implementation mismatch vs this contract;
    #  numerical failure (singular matrix, zero-variance regressor, condition number > 1e10,
    #    non-finite loss/coefficient, < 70 training origins) preventing the preregistered comparison;
    #  any unauthorized change of model / metric / horizon / cadence / threshold / feature / window / loss.
    verdict = CF1_INVALID_RUN            # no scientific claim; separate corrective phase + new operator authorization

elif ( ΔQLIKE_blockmean > 0 )                                   # P1 strict positive improvement
     and ( count_i[ ΔQLIKE_block,i > 0 ] >= 6 of 7 )            # P2 block consistency (§30)
     and ( movingblock_bootstrap_oneSided95_lowerBound(d̄) > 0 ):# P3 uncertainty (§29)
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
  block boundaries; embargo/purge applied; per-block valid-origin counts; `≥30/60` coverage
  enforced; `v002_terminal_window_read = false`; `sealed_test_split_touched = false`;
  `test_rows_loaded = 0`; consumed-holdout not used;
- a **model-run manifest**: the frozen constants of this contract (H, cadence, ε, feature list,
  HAR spec, OLS, QLIKE, bootstrap seed/`B`/`ℓ`); per-block and pooled `QLIKE(base)`, `QLIKE(aug)`,
  `ΔQLIKE_block,i`, `ΔQLIKE_blockmean`, `ρ`; the bootstrap CI; the two secondary metrics (§ main
  memo); the P1/P2/P3 booleans; and the single `CF1_VALID_PASS | CF1_VALID_FAIL | CF1_INVALID_RUN`
  verdict;
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
floor `ε`; change the horizon (1h), cadence (hourly non-overlapping), or window closure; add,
remove, transform-differently, re-window, or select features; introduce any directional / signed /
funding / calendar / OI / order-book / forced-flow / liquidation input; switch the baseline or the
augmented model class; add regularization, ensembling, trees, or neural nets; tune any
hyperparameter; change the loss, add a competing loss as decision-primary, or switch to a secondary
metric as primary; change the block count / boundaries / embargo / purge; exclude adverse dates or
blocks post hoc; mine subgroups / regimes; reclassify an invalid run as a fail or pass; use the
consumed holdout as fresh confirmation; read the v002 terminal or sealed reserves; alter the
bootstrap seed / `B` / `ℓ` or run multiple uncertainty tests and select the best; or interpret any
result before the artefact hashes and the leakage/split proof validate. Any such deviation makes the
run `CF1_INVALID_RUN` (§31).

---

**No market data, feature row, label row, model output, diagnostic output, or evidence reserve was
opened or read to author this contract. No target generation, feature generation, model fitting,
diagnostic, backtest, PnL analysis, data acquisition, paper, shadow, live, or exchange-write
execution is authorized by this contract. This contract freezes the CF-1 development experiment but
does not authorize it to run.**
