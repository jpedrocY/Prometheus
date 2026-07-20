# Phase 4bn-BA — Corrected CF-1 Execution-Validation Checklist (for a later, separately-authorized phase)

This checklist supersedes the Phase 4bn-AY execution-validation checklist
(`2026-07-15_phase-4bn-ay_cf1-execution-validation-checklist.md`) **only** in its feature-dependent
gates. Every other Phase 4bn-AY gate is inherited verbatim and remains binding. The Phase 4bn-AY
checklist is not modified.

This checklist **authorizes nothing**. It describes the fail-closed gates that a future,
separately-authorized corrected execution phase would have to satisfy. No such phase is authorized
by Phase 4bn-BA.

Every gate below is **fail-closed**: a gate that is not demonstrably PASS is a FAIL, and a FAIL
before any data read is a `PREFLIGHT_FAILURE` (stop, no data opened); a FAIL after data is opened is
`CF1_INVALID_RUN`.

---

## 1. Preflight gates (all must PASS before any data read)

### 1.1 Authorization and repository state

| # | Gate | Pass condition |
|---|---|---|
| 1.1.1 | Separate operator authorization exists for the corrected execution phase | An explicit operator prompt authorizing the corrected execution. Phase 4bn-BA is **not** such an authorization |
| 1.1.2 | Phase 4bn-BA is merged into `main` and its corrected contract is the pinned contract | Corrected execution runs against the merged Phase 4bn-BA contract, not a branch draft |
| 1.1.3 | Base state clean | `HEAD == main == origin/main`; only `.claude/scheduled_tasks.lock` untracked; the lock never staged, modified, deleted, cleaned, or committed |
| 1.1.4 | Implementation committed and pushed **before the first market-data byte is opened** | Local branch == origin branch; no tracked changes; all artefacts stamped with that `code_commit_sha` |
| 1.1.5 | No Phase 4bn-AY, Phase 4bn-AZ, or Phase 4bn-BA document is modified | Zero `M`/`D`/`R` entries against those files |
| 1.1.6 | Global authorization flags unchanged | `research_eligible = false`; `eligibility_gate_status = pending`; `ml_authorized`, `diagnostics_authorized`, `strategy_authorized`, `signals_authorized`, `pnl_authorized`, `backtest_authorized`, `live_authorized`, `exchange_write_authorized` all `false`; Phase 4aw `flip_research_eligible(...)` remains always-raising and is not invoked |

### 1.2 No-rerun and no-reuse gates (new; specific to the corrected experiment)

| # | Gate | Pass condition |
|---|---|---|
| 1.2.1 | **No-rerun rule** | The corrected execution is a **new experiment** under the Phase 4bn-BA contract. It is **not** a Phase 4bn-AZ rerun, continuation, correction-in-place, reuse of the consumed run, or reclassification. `The one authorized Phase 4bn-AZ evidence-bearing run remains consumed.` |
| 1.2.2 | **No Phase 4bn-AZ artefact reused as a scientific metric** | No Phase 4bn-AZ target layer, feature snapshot, proof artefact, manifest, condition number, residual statistic, origin count, or any other Phase 4bn-AZ output is read, imported, cached, or carried forward as an input or as a scientific metric. `No QLIKE, d_{i,t}, D_i, Δ_equal, ρ, MSE, Mincer–Zarnowitz R², bootstrap distribution, or LB_95 was computed by Phase 4bn-AZ`, so none exists to reuse. The recorded `δ` residual statistics are cited in the contract documents as historical diagnostic evidence only and are **not** inputs to any execution. Every target row, feature snapshot, and proof must be **regenerated from source** under the corrected contract's own pinned `code_commit_sha` |
| 1.2.3 | Phase 4bn-AZ not reclassified | `Phase 4bn-AZ remains CF1_INVALID_RUN and is not reclassified, repaired, rerun, or interpreted as a scientific pass or fail.` The corrected run's verdict attaches to the corrected experiment only |
| 1.2.4 | Prior-outcome independence | No Phase 4bn-AZ diagnostic influences any corrected-contract field. The corrected feature set was frozen by Phase 4bn-BA **before** any new execution |

### 1.3 Data identity and boundaries (inherited unchanged)

| # | Gate | Pass condition |
|---|---|---|
| 1.3.1 | Symbol and families | `BTCUSDT`; `microstructure_normalized_aggtrades_v001` for prices/RV; `microstructure_features_aggtrades_v001` for the feature snapshots |
| 1.3.2 | Primary execution access | Exactly 244 UTC dates: 2024-03-01 .. 2024-10-31 **excluding** 2024-10-01. No other date is opened |
| 1.3.3 | Buffer unopened | No 2024-11-01 .. 2024-11-15 row opened or used, including to form `P_at(2024-11-01T00:00:00.000Z)` |
| 1.3.4 | Embargo dates unopened | 2024-10-01 and 2024-11-16 not opened |
| 1.3.5 | Consumed holdout unopened | 2024-11-17 .. 2024-11-30 not opened; not relabelled as a fresh evaluation or confirmation set |
| 1.3.6 | Reserves untouched | `v002_terminal_window_read = false`; `sealed_test_split_touched = false`; `test_rows_loaded = 0` |
| 1.3.7 | Integrity | Every opened Parquet verified against its committed `.sha256` sidecar before reading; any mismatch fails closed |
| 1.3.8 | No acquisition | `network_used = false`; `data_acquisition_used = false`; no endpoint, credential, `.env`, MCP, or acquisition path |

### 1.4 Frozen target / horizon / cadence (inherited unchanged)

| # | Gate | Pass condition |
|---|---|---|
| 1.4.1 | Target family | BTCUSDT last-trade realized variance; `y(t) = ln(RV(t) + 1e-16)`; no annualization |
| 1.4.2 | Horizon and cadence | `H = 60 minutes`; origins at the top of each UTC hour; non-overlapping |
| 1.4.3 | Interval convention | Every RV interval is a causal completed interval `(a, b]`; boundary trade belongs to the interval **ending** at its timestamp; assigned exactly once |
| 1.4.4 | Grid-price operator | The sole operator `P_at(u)` with `source_transact_time_ms ≤ u`, greatest-`row_index` tie (`row_index_le_R`) |
| 1.4.5 | Minute-return kernel | `τ_k = a + k·60_000`; `G_k = P_at(τ_k)`; `r_k = ln(G_k/G_{k−1})`; `RV(a,b] = Σ_{k=1}^{60} r_k²` |
| 1.4.6 | Prohibited constructs absent | No `P_start`, no `P_minus`, no strict `<` at any RV boundary, no mixed operators, no left-limit terminal price, no `[a,b)` as a live RV interval |
| 1.4.7 | Coverage | Covered-minute predicate `τ_{k−1} < ts ≤ τ_k`; `≥ 30 of 60`; no stitching; zero-RV origins retained |
| 1.4.8 | Origin validity boundary | Entire completed target `(t, t+H]` including its right endpoint inside execution access; `2024-10-31T23:00` invalid; last potentially valid origin `2024-10-31T22:00` |
| 1.4.9 | Deterministic synthetic timestamp-boundary proof | Emitted and PASSED **before any market data is opened**; synthetic rows only; `market_data_opened = false`, `reserve_touched = false`. A failed or absent proof before any market-data read ⇒ `PREFLIGHT_FAILURE`; stop with no market data opened and no scientific result |

### 1.5 Frozen corrected features (SUPERSEDES the Phase 4bn-AY checklist §1.4)

| # | Gate | Pass condition |
|---|---|---|
| **1.5.1** | **Exact feature list** | Exactly `["rolling_aggtrade_count_60s", "rolling_quantity_sum_60s"]`, in that canonical order |
| **1.5.2** | **Exact feature count** | `feature_count == 2` |
| **1.5.3** | **`rolling_quantity_mean_60s` absent** | The column is **not** read, not snapshotted, not transformed, not emitted, not stored, and not carried in any artefact. Its presence anywhere in the model path ⇒ `CF1_INVALID_RUN` |
| **1.5.4** | **Three-feature set prohibited** | The Phase 4bn-AY three-feature set is `STRUCTURALLY_NON_IDENTIFIABLE__PROHIBITED_FOR_FUTURE_EXECUTION` — meaning a source-defined derived feature whose stored transformed column produced effective rank deficiency / catastrophic conditioning under the frozen guard, **not** an assertion of an exact symbolic rank theorem for every serialized dataset. Any three-feature microstructure augmentation ⇒ `CF1_INVALID_RUN` |
| 1.5.5 | Window | 60s only: `(t_last − 60_000 ms, t_last]`, `trailing_right_open_left`. No other window; no multi-window stacking; no window search |
| 1.5.6 | Snapshot rule | Last committed feature row with `feature_timestamp_ms ≤ t`, `row_index_le_R` tie. A row timestamped exactly `t` may be used |
| 1.5.7 | Transform | Natural logarithm of each retained feature. No ratios, no interactions, no polynomial expansion, no differencing. The quotient `x2/x1` is **not** formed as an explicit model feature; the ideal mean-size contrast `ln(x2) − ln(x1)` is representable by the estimator from the two retained regressors |
| 1.5.8 | Standardization | `z_j = (ln x_j − μ_j^train)/max(σ_j^train, 1e-8)`, fitted on the expanding training origins of each block only, then applied to that block. No global statistic; no block influences preprocessing fitted for itself. HAR regressors unstandardized |
| 1.5.9 | No clipping | No clipping or winsorization of features or target |
| **1.5.10** | **Origin-validity predicate** | An origin is invalid, and dropped identically from both models, if `rolling_aggtrade_count_60s < 1`, or `rolling_quantity_sum_60s ≤ 0`, or any feature value is null or non-finite. This excludes every origin the Phase 4bn-AY predicate excluded on those grounds; it is **equal to or a superset of** the Phase 4bn-AY valid-origin set, because the corrected contract never forms the floor-quantized mean. No imputation; no forward-fill across invalid windows; no NaN/Inf in any model input |
| 1.5.11 | Directional exclusions absolute | No `rolling_aggressive_*` column, no `rolling_log_return_past_window_*`, no signed return, no direction label, no funding, no calendar, no open interest, no order-book / top-of-book, no liquidation or forced-flow proxy, no mark/index price, no time-context column, no quality flag as a mechanism feature, no newly derived feature, no feature chosen from an observed correlation, coefficient, QLIKE, importance, or subgroup result |

### 1.6 Pre-data symbolic estimability proof (new; explicit gate)

This gate must be satisfied and recorded **before any market data is opened**. It is a symbolic
restatement, not a computation on data.

| # | Gate | Pass condition |
|---|---|---|
| 1.6.1 | Candidate universe closed | Recorded: the committed `PER_WINDOW_FEATURE_TEMPLATES` enumeration; the sign-invariant non-directional universe at 60s is exactly `{count, quantity_sum, quantity_mean}`; no committed dispersion column exists |
| **1.6.2** | **Formatter quantization recorded** | Recorded: the committed mean formatter is a **fixed-point floor quantizer**, `mean_int = (sum_int × 10^12) // count`, serialized at the quantity scale plus twelve decimals (`features_compute.py:141-159`). The stored mean is therefore `x3 = x3* − q`, `q ≥ 0`, `q <` one stored least-significant decimal unit, `q = 0` only when the quotient is exactly representable at that precision. **No universal relative-error bound may be asserted** |
| **1.6.3** | **Ideal quotient recorded separately from the stored feature** | Recorded, as two distinct statements: (i) *ideal* — `x3* = x2/x1` and `ln(x3*) = ln(x2) − ln(x1)`, exact; (ii) *stored* — `ln(x3) = ln(x2) − ln(x1) + δ` with `δ ≤ 0`, `δ = 0` only when `q = 0`, `δ` generally nonzero. **No exact stored identity may be claimed** |
| **1.6.4** | **Original set characterized correctly** | Recorded: the Phase 4bn-AY three-feature set is **deterministically redundant at the source-definition level** (`x3` derived from `x1`, `x2`, carrying no independent information) and **numerically non-identifiable under the frozen runtime guard** after serialization and logarithmic transformation — evidenced by the Phase 4bn-AZ residual (`max|δ| = 3.33e-14`, `mean|δ| = 3.51e-15`, cited not recomputed) and by augmented condition numbers ≈ 1e16 exceeding the `> 1e10` guard in all seven blocks. **No universal exact rank theorem for the stored design may be asserted** |
| 1.6.5 | Retained-pair independence | Recorded: **no exact affine dependency is implied by the committed definitions** between `ln(x1)` and `ln(x2)` (cardinality does not determine the quantity sum) |
| 1.6.6 | Cross-block independence | Recorded: the HAR regressors are price-path realized variances; the retained features are trade cardinality and traded quantity; disjoint constructions, no shared accumulator |
| 1.6.7 | Standardization rank preservation | Recorded: `X' = X·T` with `T` upper triangular, `det(T) = 1/(s1·s2) ≠ 0`; `rank(X') = rank(X)`. Also recorded: standardization **cannot repair** near-collinearity, which is why it did not rescue the Phase 4bn-AY design |
| 1.6.8 | Declared structural rank | Recorded: `augmented_parameter_count = 6`; `expected_structural_rank = 6`; `baseline_parameter_count = 4`; `expected_baseline_rank = 4` |
| **1.6.9** | **Scope honesty** | Recorded verbatim: the declared rank asserts only the **absence of a source-implied exact dependency**. It is **not** proof that every empirical training matrix will have full numerical rank, and **not** a claim about any numerical condition number. **The runtime rank, zero-variance, condition-number, and non-finite guards are the final arbiter** |
| 1.6.10 | Failure routing | A failed, absent, or altered estimability record ⇒ `PREFLIGHT_FAILURE` before any data read |

### 1.7 Frozen baseline and augmented models

| # | Gate | Pass condition |
|---|---|---|
| 1.7.1 | Baseline | Exactly one HAR-style OLS baseline: `y = β0 + β1·ln(RV_h+ε) + β2·ln(RV_d+ε) + β3·ln(RV_w+ε) + u`. No baseline shopping, no lag search, no alternate cascade |
| 1.7.2 | HAR lookbacks | `RV_h(t) = RV(t−1h, t]`; `RV_d(t)` = mean of the 24 completed hourly RV intervals tiling `(t−24h, t]`; `RV_w(t)` = mean of the 168 tiling `(t−168h, t]`; same `P_at(·)` operator and same minute-return kernel as the target; each obeys the coverage and boundary rules |
| **1.7.3** | **Augmented equation** | Exactly `y = β0 + β1·ln(RV_h+ε) + β2·ln(RV_d+ε) + β3·ln(RV_w+ε) + γ1·z1 + γ2·z2 + u`. **Two** microstructure terms, not three |
| 1.7.4 | Nesting | Baseline is exactly the augmented model with `γ1 = γ2 = 0`; identical target, geometry, estimator, training window, forecast origins, and preprocessing scope |
| 1.7.5 | No model search | No model-class search, no feature selection, no regularization, no post-hoc interaction, no alternate augmented specification after results |
| 1.7.6 | Estimator | Deterministic OLS via a numerically stable solver; no regularization; no tunable hyperparameter; no iterative optimizer |

### 1.8 Frozen split and leakage controls (inherited unchanged)

| # | Gate | Pass condition |
|---|---|---|
| 1.8.1 | Blocks | Exactly seven: B1 2024-04-01..04-30; B2 05-01..05-31; B3 06-01..06-30; B4 07-01..07-31; B5 08-01..08-31; B6 09-01..09-30; B7 10-02..10-31 |
| 1.8.2 | Warmup | 2024-03-01..2024-03-31 train-only, never evaluated |
| 1.8.3 | Walk-forward | Expanding anchored; one fit per block; no re-fit inside a block; a block never fits its own model |
| 1.8.4 | Embargo and purge | One calendar day embargo before each block; the 1h purge is subsumed |
| 1.8.5 | Preprocessing scope | Training-only, per block; no global statistic; no future block pooled |
| **1.8.6** | **Block minimum** | `MIN_BLOCK_VALID_ORIGINS = 100` valid paired evaluation origins per block — **unchanged**. Any block below ⇒ `CF1_INVALID_RUN` |
| **1.8.7** | **Training minimum** | `MIN_TRAINING_ORIGINS_AUGMENTED = 10 × 6 = 60` valid training origins per block. Fewer ⇒ `CF1_INVALID_RUN`. (Supersedes the Phase 4bn-AY value of 70; the `10 × parameters` rule itself is unchanged) |
| 1.8.8 | Leakage / split / coverage proof | Emitted and PASSED **before any metric is computed**: chronological block boundaries; embargo/purge applied; per-block `n_i`; `≥ 30/60` coverage enforced; access boundary respected; `october_1_opened = false`; `november_or_later_opened = false`; `consumed_holdout_opened = false`; `terminal_opened = false`; `sealed_opened = false`; `october_31_23_00_retained = false` |

### 1.9 Runtime numerical guards (retained unchanged and unrelaxed)

| # | Gate | Fail-closed condition ⇒ `CF1_INVALID_RUN` |
|---|---|---|
| **1.9.1** | **Condition number** | Training design-matrix condition number `> 1e10`. The threshold is **not** relaxed, widened, or made conditional. It applies to the baseline and to the augmented design |
| **1.9.2** | **Rank guard** | Augmented training design rank `< 6`, or baseline rank `< 4` |
| 1.9.3 | Zero-variance guard | Any zero-variance training regressor |
| 1.9.4 | Singularity | Singular normal-equations matrix |
| 1.9.5 | Non-finite | Any non-finite coefficient, input, actual, forecast, ratio, logarithm, or QLIKE value |
| 1.9.6 | Training size | Fewer than 60 valid training origins in any block |
| 1.9.7 | **No rescue on a tripped guard** | A tripped guard is a **technical invalidation**, never a silently-simplified model, never a dropped feature, never a relaxed threshold, never a regularization fallback, and never a scientific pass or fail |

### 1.10 Frozen loss, uncertainty, and decision (inherited unchanged)

| # | Gate | Pass condition |
|---|---|---|
| 1.10.1 | Loss | QLIKE only; `v = RV + 1e-16`; `h = max(exp(ŷ), 1e-16)`; `QLIKE = ratio − ln(ratio) − 1`; same `ε` and same formula for both models; no post-hoc clipping; no observation dropped merely because `RV = 0` |
| 1.10.2 | Aggregation | Block arithmetic mean, then **equal-weighted** seven-block mean. No origin-count weighting, no pooling across blocks, at any decision stage |
| 1.10.3 | Primary estimand | `d_{i,t} = QLIKE_base − QLIKE_aug`; `D_i = (1/n_i) Σ_t d_{i,t}`; `Δ_equal = (1/7) Σ_i D_i`; `ρ = Δ_equal / QLIKE(base)` descriptive only |
| 1.10.4 | P1 | `Δ_equal > 0` (strict; no materiality floor) |
| 1.10.5 | P2 | `D_i > 0` in `≥ 6 of 7` blocks; not replaceable by the bootstrap |
| 1.10.6 | P3 | Stratified-by-block moving-block bootstrap of the same `Δ_equal` estimand; `ℓ_i = ceil(n_i^(1/3))`; `B = 10,000`; `RNG_SEED = 20260715`; one-sided 95% percentile `LB_95 > 0`; no resampling across block boundaries; not replaceable by P2 |
| 1.10.7 | Routing | Invalid-run conditions first; then `CF1_VALID_PASS` iff P1 ∧ P2 ∧ P3 ∧ validity; otherwise `CF1_VALID_FAIL`. No borderline, promising, weak, or partial pass; no pass on a secondary metric or a post-hoc subset |

### 1.11 Frozen outputs and provenance

| # | Gate | Pass condition |
|---|---|---|
| **1.11.1** | **Target-layer columns** | Per valid origin: `RV(t)`, `y(t)`, `RV_h`, `RV_d`, `RV_w`, **two** snapshot columns (`rolling_aggtrade_count_60s`, `rolling_quantity_sum_60s`), split/block assignment, origin-validity fields. `rolling_quantity_mean_60s` is **not** emitted |
| **1.11.2** | **Manifest feature fields** | `feature_list = ["rolling_aggtrade_count_60s", "rolling_quantity_sum_60s"]`; `feature_count = 2`; `augmented_parameter_count = 6`; `min_training_origins = 60` |
| 1.11.3 | Manifest remainder | All other frozen constants (`H`, cadence, `ε = 1e-16`, HAR spec, OLS, QLIKE safeguard, bootstrap seed / `B` / `ℓ_i`); per-block `QLIKE_block,i(base)`, `QLIKE_block,i(aug)`, `D_i`; equal-weighted `QLIKE(base)`, `QLIKE(aug)`, `Δ_equal`, `ρ`; `LB_95`; secondary metrics; P1/P2/P3 booleans; the single verdict |
| 1.11.4 | Storage | All artefacts local and gitignored under `data/research/…`; no data file committed; per-Parquet `.sha256` sidecars plus inventory |
| 1.11.5 | Provenance | `created_at_unix_ms`, `created_at_utc`, `code_commit_sha` (40-char), `base_main_commit_sha` (40-char); committed filename conventions |
| 1.11.6 | Non-authorization flags | All eight `false` |

### 1.12 Frozen anti-switching preflight

The corrected execution phase may **not**: change the interval convention, `P_at(·)`, the coverage
predicate, or the right-endpoint validity rule; reintroduce `P_start`, `P_minus`, strict `<`, mixed
operators, a left-limit terminal price, or `[a,b)`; retain the `2024-10-31T23:00` origin; skip or
weaken either proof (proceeding to open market data having skipped or weakened a proof is a
post-access violation ⇒ `CF1_INVALID_RUN`; stopping at a failed pre-data proof without opening market
data is `PREFLIGHT_FAILURE` per §1.4.9); change the target family, RV estimator, sampling grid, or
`ε = 1e-16`; change
the QLIKE safeguard or clip the ratio or loss; drop an observation solely because `RV = 0`; change
the horizon, cadence, or window closure; **add, remove, re-window, transform differently, or select
features**; introduce any directional / signed / funding / calendar / OI / order-book / forced-flow /
liquidation input; switch either model class; add regularization, ensembling, trees, or neural nets;
tune any hyperparameter; change the loss or promote a secondary metric; change the block count,
boundaries, embargo, or purge; open or use any buffer row; extend execution access beyond
2024-10-31; exclude adverse dates or blocks post hoc; mine subgroups or regimes; reclassify an
invalid run as a fail or pass; use the consumed holdout as fresh confirmation; read the v002
terminal or sealed reserves; pool or weight blocks, resample across block boundaries, or alter the
bootstrap seed / `B` / `ℓ_i`; run multiple uncertainty tests and select the best; or interpret any
result before the artefact hashes and the leakage/split proof validate. **Any such deviation ⇒
`CF1_INVALID_RUN`.**

## 2. Execution-order gates (fail-closed, in order)

1. Verify authorization, repository state, and the no-rerun / no-reuse gates (§1.1, §1.2). FAIL ⇒
   stop, no data opened.
2. Record the pre-data symbolic estimability proof (§1.6). FAIL ⇒ `PREFLIGHT_FAILURE`.
3. Commit and push the implementation; verify local == origin. FAIL ⇒ stop.
4. Emit and validate the deterministic synthetic timestamp-boundary proof (§1.4.9), synthetic rows
   only. FAIL ⇒ `PREFLIGHT_FAILURE`; stop with no market data opened and no scientific result.
5. Open **only** the 244 authorized partitions, verifying each `.sha256` sidecar. Any mismatch or any
   forbidden partition ⇒ stop.
6. Build the realized-variance target layer and the **two** feature snapshots per origin.
7. Emit and validate the leakage / split / coverage proof **before any metric is computed** (§1.8.8).
   FAIL ⇒ `CF1_INVALID_RUN`.
8. Per block: assemble the training design; evaluate the runtime numerical guards (§1.9) **before**
   fitting. Any trip ⇒ `CF1_INVALID_RUN`, recorded as a technical invalidation with no rescue.
9. Fit both models; compute QLIKE, `d_{i,t}`, `D_i`, `Δ_equal`, `ρ`, and the secondary metrics.
10. Run the stratified moving-block bootstrap exactly once with the frozen seed and `B`.
11. Validate artefact hashes; then and only then route the verdict.

## 3. Outcome classification

Exactly one of:

- `CF1_VALID_PASS` — a valid run meeting P1 ∧ P2 ∧ P3. Magnitude-only. Establishes no direction, no
  economic materiality, no profitability, no ability to clear the locked 8 bps/side · 16 bps round
  trip, and no tradability.
- `CF1_VALID_FAIL` — a valid run failing P1, P2, or P3. Closes or narrows **only** the corrected
  preregistered magnitude lane.
- `CF1_INVALID_RUN` — any invalidation condition. **No scientific claim.** Neither a pass nor a fail.
  Requires a separate corrective phase and a new operator authorization; it may never be converted
  into a pass or a fail.

There is no fourth outcome, no borderline result, and no post-hoc subset result.

**`PREFLIGHT_FAILURE` is not a fourth scientific outcome.** It is a **pre-execution gate result**:
the run stops before any market-data byte is opened, produces **no** scientific pass, fail, or
invalid-run result, consumes no evidence, and makes no claim about the CF-1 hypothesis. It is
recorded as a gate failure, never as a verdict, and never converted into one.

The routing boundary is therefore:

- a failed gate **before** any market-data read ⇒ `PREFLIGHT_FAILURE` (stop; no market data opened;
  no scientific result). This includes a failed or absent deterministic synthetic timestamp-boundary
  proof (§1.4.9) and a failed or absent pre-data symbolic estimability record (§1.6);
- a failed gate or contract violation **after** market-data access ⇒ `CF1_INVALID_RUN` (a scientific
  outcome carrying no scientific claim).

## 4. Non-authorization

**This checklist authorizes no execution.**

`Phase 4bn-BB or any future corrected execution requires separate operator authorization and a new Claude Code prompt.`

`No QLIKE, bootstrap, model fitting, target generation, feature generation, diagnostic, backtest, PnL analysis, data acquisition, paper, shadow, live, or exchange-write execution is authorized by Phase 4bn-BA.`

`No market data, target row, feature row, model output, diagnostic output, or local Phase 4bn-AZ artefact was opened or read by Phase 4bn-BA.`

`The v002 terminal window and v002 sealed test remain untouched and excluded.`

`The consumed pre-v002 internal holdout and the 2024-11-01 through 2024-11-15 buffer remain unopened.`

`No evidence reserve is authorized for spending by Phase 4bn-BA.`

`Remaining paused is a valid operator choice.`
