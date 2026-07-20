# Phase 4bn-BA — CF-1 Feature-Contract Correction and Re-Preregistration

## 1. Phase identity

Phase 4bn-BA — CF-1 Feature-Contract Correction and Re-Preregistration. A **docs-only,
no-data, no-model, no-metric, no-rerun** scientific-contract correction phase following the merged
Phase 4bn-AZ `CF1_INVALID_RUN`. Tier 1 / Full Phase per
`docs/00-meta/process/phase-risk-tiering-standard.md` (a change to preregistered scientific
semantics is Tier 1 regardless of the fact that the surface is Markdown only).

This phase adds four new implementation-report documents and modifies no existing file, no source
module, no test, no script, no schema, no manifest, no ledger, and no process standard. It performs
no execution of any kind.

Branch: `phase-4bn-ba/cf1-feature-contract-correction-repreregistration`.

## 2. Base and branch SHAs

| Item | SHA |
|---|---|
| Base `main` == `origin/main` at branch creation (Phase 4bn-AZ merge-closeout SHA-finalization tip) | `021e4fc12e2e541aaefd54f562ff9d1a9c9cff52` |
| Phase 4bn-AZ no-fast-forward merge commit | `8e82e185a0def318acd2ec42fcb73337edc67b51` |
| Phase 4bn-AZ evidence-bearing implementation SHA | `05fa63a8bf8c9b1fe386cc4ab67805046ae418b1` |
| Phase 4bn-AY final scientific-contract tip | `0fb560656aa9b50cf110602e15be8222b7343623` |

The only untracked item present at branch creation was `.claude/scheduled_tasks.lock`, which was
never staged, modified, deleted, cleaned, or committed.

## 3. Exact Phase 4bn-AZ invalid-run lineage (preserved, not reinterpreted)

`Phase 4bn-AZ remains CF1_INVALID_RUN and is not reclassified, repaired, rerun, or interpreted as a scientific pass or fail.`

`The one authorized Phase 4bn-AZ evidence-bearing run remains consumed.`

The recorded post-merge result state of Phase 4bn-AZ, preserved verbatim and unchanged by this
phase:

```
CF1_INVALID_RUN_RECORDED_ON_MAIN__NO_SCIENTIFIC_CLAIM__NO_RERUN_AUTHORIZED__SEPARATE_DOCS_ONLY_CONTRACT_CORRECTION_REQUIRED_IF_CONTINUING__RESERVES_UNTOUCHED
```

The following statements are binding historical interpretation and are restated here exactly:

- `Phase 4bn-AZ produced CF1_INVALID_RUN, not CF1_VALID_FAIL and not CF1_VALID_PASS.`
- `The run produced no scientific test of the CF-1 hypothesis because the preregistered transformed feature set was structurally rank deficient.`
- `The identity ln(rolling_quantity_mean_60s) = ln(rolling_quantity_sum_60s) − ln(rolling_aggtrade_count_60s) made the augmented design non-identifiable under the frozen feature contract.`
- `No QLIKE, d_{i,t}, D_i, Δ_equal, ρ, MSE, Mincer–Zarnowitz R², bootstrap distribution, or LB_95 was computed.`
- `P1, P2, and P3 were not evaluable; any false or zero placeholder is not a negative scientific finding.`
- `The Phase 4bn-AY valid-fail consequence does not apply, and the aggTrades magnitude lane was not narrowed by Phase 4bn-AZ.`
- `The one authorized evidence-bearing run is consumed, and no rerun is authorized.`

Phase 4bn-AY remains historical and merged. Phase 4bn-AZ remains an invalid run. No past document,
run, metric, or verdict is rewritten by this phase.

## 4. Reason for correction (the exact algebraic defect)

The merged Phase 4bn-AY contract §11 froze exactly three microstructure regressors at the 60s
window:

```
x1 = rolling_aggtrade_count_60s
x2 = rolling_quantity_sum_60s
x3 = rolling_quantity_mean_60s
```

and §13 froze the natural logarithm of each, followed by train-only z-scoring (§14).

By the committed feature definition
(`src/prometheus/research/microstructure/features_compute.py:343-349`, which calls
`_format_mean_as_decimal_string(window_qty[i], window_count[i], max_dp_q)` defined at
`features_compute.py:141-159` as `sum_int / count`), the mean column is the quotient of the **same
two committed accumulators** that constitute the other two features, over the **same** 60s trailing
window:

```
x3 = x2 / x1        (exact by construction, up to a fixed-point floor truncation at
                     max_dp + 12 decimal places, i.e. relative error ≤ 1e-12)
```

Therefore

```
ln(x3) ≡ ln(x2) − ln(x1)
```

holds identically at every origin. The three log-transformed regressors span a **two-dimensional**
space. With one intercept, three HAR log-realized-variance regressors, and three transformed
microstructure regressors, the augmented design matrix has **7 columns but structural rank 6**.

This is a defect of the **preregistered design**, not of the data, the implementation, the split,
the timestamp semantics, the substrate, or the sample size. Standardization does not remove it: an
invertible affine rescaling of exactly collinear columns remains exactly collinear.

The Phase 4bn-AY contract simultaneously mandated (a) these three features, (b) the log transform,
and (c) the guard `condition number > 1e10 ⇒ CF1_INVALID_RUN` (§19). The conjunction (a) ∧ (b)
necessarily trips (c). The experiment as frozen could not have produced a scientific pass or fail
on any data.

Phase 4bn-AZ confirmed this deterministically: all seven blocks tripped
`augmented_condition_number_exceeded` with augmented condition numbers ≈ 1.02e+16 – 1.09e+16,
against a well-conditioned baseline (3.4e+02 – 6.2e+02, full rank 4/4). Every block met its
valid-origin minimum (n_i between 550 and 744, all ≥ 100) and its training minimum (551 – 4,966,
all ≥ 70), so **the failure was not caused by insufficient sample size**. That is the only use this
phase makes of Phase 4bn-AZ block-level diagnostics, and it is expressly permitted: it documents an
already-proven structural defect and rules out a sample-size explanation. It is **not** used to
select among candidate features.

`No Phase 4bn-AZ metric is used to select the corrected feature contract because no scientific metric was computed.`

`The correction is based only on committed feature definitions, symbolic estimability, mechanism coherence, and anti-duplication constraints.`

## 5. Candidate feature universe

The candidate universe is closed and is restricted to columns already present in the committed
aggTrades feature schema at the time of the Phase 4bn-AY preregistration. No feature is invented; no
feature-builder change is authorized; no new source is used; no data is acquired.

The committed schema (`features_schema.py:68-79`, `PER_WINDOW_FEATURE_TEMPLATES`) declares exactly
**ten** per-window templates, instantiated over the four committed windows
(`FEATURE_WINDOWS_MS_V001 = (1000, 5000, 15000, 60000)`), plus three time-context columns and two
data-quality flags — 45 feature/quality columns in total, 61 columns with lineage.
`features_schema_v002.py:129` sets `PER_WINDOW_FEATURE_TEMPLATES_V002 = PER_WINDOW_FEATURE_TEMPLATES`,
so **v002 introduces no additional feature template**. The universe is therefore identical under
both committed schema versions.

At the frozen 60s window the ten templates classify exhaustively as:

| # | Committed column | Class | Admissible? |
|---|---|---|---|
| 1 | `rolling_aggtrade_count_60s` | trade-arrival intensity; sign-invariant | **yes** |
| 2 | `rolling_quantity_sum_60s` | unsigned traded-volume intensity; sign-invariant | **yes** |
| 3 | `rolling_quantity_mean_60s` | sign-invariant trade-size level; **deterministic quotient of 1 and 2** | no — algebraically redundant |
| 4 | `rolling_aggressive_buy_quantity_60s` | directional (side identity) | no — §16 prohibited |
| 5 | `rolling_aggressive_sell_quantity_60s` | directional (side identity) | no — §16 prohibited |
| 6 | `rolling_aggressive_buy_count_60s` | directional (side identity) | no — §16 prohibited |
| 7 | `rolling_aggressive_sell_count_60s` | directional (side identity) | no — §16 prohibited |
| 8 | `rolling_aggressive_flow_ratio_60s` | directional (signed flow ratio) | no — §16 prohibited |
| 9 | `rolling_aggressive_quantity_imbalance_60s` | directional (signed imbalance) | no — §16 prohibited |
| 10 | `rolling_log_return_past_window_60s` | signed past return | no — §16 prohibited; also a price-return object |
| — | `utc_hour`, `utc_minute`, `milliseconds_since_day_start` | calendar/time context, not a mechanism feature | no — §16 prohibited |
| — | `invalid_window_flag`, `rolling_missing_window_flag` | data-quality flags, not mechanism features | no |

**Explicit statement required by the mandate:** *no committed independent sign-invariant dispersion,
standard-deviation, or variance-of-trade-size column exists in the aggTrades feature schema.* The
only committed central-moment column is `rolling_quantity_mean_{w}`, and it is precisely the
redundant quotient. There is likewise no committed sign-invariant magnitude column outside the
set {count, quantity sum, quantity mean}. A dispersion feature would require building a new
committed column, which is a different feature family and is out of scope for a bounded contract
repair.

**Therefore the entire sign-invariant, non-directional, magnitude candidate universe at the frozen
60s window is exactly `{x1, x2, x3}`, and `x3` is a deterministic function of `x1` and `x2`.**

## 6. Symbolic audit summary

The full audit is recorded in
`2026-07-20_phase-4bn-ba_cf1-estimability-and-anti-duplication-audit.md`. Its decisive results:

1. **Cardinality theorem.** The log-transformed candidate set `{ln x1, ln x2, ln x3}` spans exactly
   two dimensions. Hence **every** linearly independent subset of the admissible universe has
   cardinality at most **2**, and the pairs `{x1,x2}`, `{x1,x3}`, `{x2,x3}` each attain 2. A
   three-feature admissible contract does not exist.
2. **Equivalence theorem.** The three admissible pairs span the *same* two-dimensional column
   space. Adjoined to the intercept and the three HAR regressors, they therefore produce **identical
   fitted values, identical residuals, identical QLIKE, identical `d_{i,t}`, `D_i`, `Δ_equal`, `ρ`,
   and identical bootstrap distributions**. The choice among the three pairs is scientifically
   immaterial and **cannot** be a data-driven selection even in principle, because no observable
   outcome can distinguish them.
3. **Span-preservation theorem.** `span{ln x1, ln x2} = span{ln x1, ln x2, ln x3}`. The corrected
   two-feature contract represents **every** linear combination the invalid three-feature contract
   could have represented, including the trade-size-level channel, which is exactly the contrast
   `ln x2 − ln x1`. **No mechanism content is lost by the correction.**
4. **Independence.** Nothing in the committed definitions implies any affine identity between
   `ln x1` and `ln x2`: `x1` is the window cardinality and `x2` is the sum of the window's
   quantities, and the quantity values are free positive decimals not determined by the cardinality.
   No deterministic relation exists in source.
5. **Standardization safety.** Train-only z-scoring is an invertible affine column map (`σ > 0`
   enforced by the retained zero-variance guard), so it neither creates nor conceals a deterministic
   dependency; column space and rank are preserved exactly.
6. **Anti-duplication vs HAR.** The HAR regressors are log realized variances constructed from the
   price path; `x1` and `x2` are trade counts and traded quantity. They share no accumulator, no
   construction, and no algebraic relation. Conceptual association (the mixture-of-distributions
   intuition linking activity to volatility) is precisely the hypothesis under test and is not
   duplication; empirical correlation is not measured in this phase and is not the criterion.
7. **Tie-break is non-data-driven.** Because the three pairs are outcome-equivalent (result 2), the
   pair is selected on committed-source properties alone: `x1` and `x2` are the **primitive**
   accumulators (`window_count`, `window_qty`), both **non-null by construction**
   (`features_compute.py:462-476`), and both free of the fixed-point floor truncation that the
   derived mean carries; `x3` is the **only** nullable column of the three
   (`nullable_decimal_prefixes = ("rolling_quantity_mean_",)`, `NULL_POLICY_V001`
   `"rolling_quantity_mean": "null_when_empty"`) and the **only** one with quantization loss.

The original three-feature transformed set is marked:

```
STRUCTURALLY_NON_IDENTIFIABLE__PROHIBITED_FOR_FUTURE_EXECUTION
```

## 7. Exact decision

```
SELECT_CORRECTED_CF1_FEATURE_CONTRACT_FOR_SEPARATE_FUTURE_EXECUTION
```

**Decision A.** Exactly one corrected feature specification is selected and fully re-preregistered:
the Phase 4bn-AY feature set with the redundant derived column `rolling_quantity_mean_60s`
**removed**, retaining the two primitive committed sign-invariant columns.

This is the minimum bounded change that makes the specification estimable: exactly one column is
removed, the removal is **forced** by the cardinality theorem (§6.1), and by the span-preservation
theorem (§6.3) it removes **no** mechanism content.

The corrected specification is **not** selected to preserve the original feature count of three; a
three-feature admissible contract provably does not exist, and the smaller two-feature
specification is the maximal estimable contract available from committed source.

## 8. Corrected hypothesis boundary (unchanged)

The CF-1 hypothesis is preserved exactly as preregistered by Phase 4bn-AY:

> Can predeclared non-directional aggTrades activity variables improve future realized-volatility
> magnitude forecasts beyond the fixed HAR-style baseline?

The correction does not broaden, narrow, or restate the mechanism. It does not add a sensitivity
test, relax a guard, improve the model, or introduce a new feature family. By §6.3 the corrected
augmented model has exactly the same representational capacity on the microstructure axis as the
invalid contract intended.

## 9. Exact inherited Phase 4bn-AY contract (unchanged)

Every field of the Phase 4bn-AY contract
(`2026-07-15_phase-4bn-ay_cf1-target-feature-baseline-and-evaluation-contract.md`, final tip
`0fb560656aa9b50cf110602e15be8222b7343623`) is inherited **unchanged** except the feature-set
specification and its directly dependent fields enumerated in §11.

Inherited unchanged, in full:

**Target and timestamps.** BTCUSDT last-trade realized variance; `H = 60 minutes = 3,600,000 ms`;
top-of-UTC-hour origins; target interval `(t, t + H]`; every RV interval a causal completed interval
`(a, b]`; the sole canonical grid-price operator `P_at(u)` = price of the canonical last aggTrade
with `source_transact_time_ms ≤ u`, ties resolved by greatest canonical `row_index`
(`row_index_le_R`); fixed 1-minute UTC clock grid; `τ_k = a + k × 60_000 ms`; `G_k = P_at(τ_k)`;
`r_k = ln(G_k / G_{k-1})`; `RV(a,b] = Σ_{k=1}^{60} r_k²`; `y(t) = ln(RV(t) + 1e-16)`; no
annualization; a boundary trade belongs to the interval **ending** at its timestamp and is assigned
exactly once; `P_start`, `P_minus`, strict `<` at any RV boundary, mixed endpoint operators,
left-limit terminal prices, and `[a, b)` as a live RV interval remain prohibited.

**Coverage.** Covered-minute sub-interval `(τ_{k-1}, τ_k]`, covered iff at least one aggTrade
satisfies `τ_{k-1} < source_transact_time_ms ≤ τ_k`; threshold `≥ 30 of 60`
(`min_covered_minute_fraction = 0.50`); no stitching across any embargo, buffer, holdout, terminal,
or sealed boundary; zero-RV origins retained (no observation dropped merely because `RV = 0`).

**Baseline.** Exactly one HAR-style OLS baseline with intercept and the three log realized-variance
regressors `ln(RV_h+ε)`, `ln(RV_d+ε)`, `ln(RV_w+ε)`, where `RV_h(t) = RV(t−1h, t]`, `RV_d(t)` is the
mean of the 24 completed hourly RV intervals tiling `(t−24h, t]`, and `RV_w(t)` is the mean of the
168 completed hourly RV intervals tiling `(t−168h, t]`; HAR intervals use the same `P_at(·)`
operator and the same minute-return formula as the target; no baseline shopping; no lag search; no
alternate cascade.

**Estimator.** Deterministic OLS via a numerically stable linear solver; no regularization; no
tunable hyperparameter; no iterative optimizer; rank guard; zero-variance-regressor guard;
condition-number guard `> 1e10`; singular-normal-equations guard; non-finite-coefficient guard.

**Dates and split.** Primary execution-access boundary 2024-03-01 through 2024-10-31 UTC excluding
2024-10-01 (244 dates); March 2024 warmup and initial training history, train-only and never
evaluated; seven fixed full-calendar-month evaluation blocks B1–B7 (2024-04-01..2024-04-30,
2024-05-01..2024-05-31, 2024-06-01..2024-06-30, 2024-07-01..2024-07-31, 2024-08-01..2024-08-31,
2024-09-01..2024-09-30, 2024-10-02..2024-10-31); B7 begins 2024-10-02; the `2024-10-31T23:00:00.000Z`
origin is invalid; the last potentially valid origin is `2024-10-31T22:00:00.000Z`;
2024-11-01..2024-11-15 remains `UNUSED_NON_RESERVE_BUFFER`, unused and unopened; 2024-11-16 remains
an excluded committed embargo date; the consumed pre-v002 internal holdout (2024-11-17..2024-11-30)
is excluded and descriptive-only; the v002 terminal window (2024-12-01..2025-02-28) and the v002
sealed test (2025-02-14..2025-02-28) are excluded and `UNTOUCHED_RESERVED`; expanding anchored
walk-forward with one fit per block; one-calendar-day embargo; one-hour purge subsumed by the
embargo; training-only preprocessing; `MIN_BLOCK_VALID_ORIGINS = 100` valid paired origins per
block.

**Loss and decision.** QLIKE as the single primary loss; `v(t) = RV(t) + ε`;
`h_m(t) = max(exp(ŷ_m(t)), ε)`; `ε = 1e-16` shared by target, actual, and forecast;
`QLIKE_m(t) = ratio − ln(ratio) − 1`; block-level arithmetic mean; equal-weighted seven-block
`Δ_equal = (1/7) Σ_i D_i` as the sole primary estimand, with `D_i = (1/n_i) Σ_t d_{i,t}` and
`d_{i,t} = QLIKE_baseline − QLIKE_augmented`; `ρ = Δ_equal / QLIKE(base)` descriptive only; P2 block
consistency requiring `D_i > 0` in ≥ 6 of 7 blocks; P3 stratified-by-block moving-block bootstrap of
the same `Δ_equal` estimand with block-specific `ℓ_i = ceil(n_i^(1/3))`, `B = 10,000`,
`RNG_SEED = 20260715`, one-sided 95% percentile lower bound `LB_95`, passing iff `LB_95 > 0`; no
pooling across blocks; no origin-count weighting; no resampling across block boundaries; the
pass / fail / invalid-run routing of contract §31 unchanged; no materiality floor.

**Consequences.** A valid pass remains magnitude-only and establishes no direction, no economic
materiality, no profitability, no ability to clear the locked 16 bps round trip, and no
tradability. A valid fail closes or narrows only the corrected preregistered magnitude lane. An
invalid run supports no scientific claim. No direction, PnL, trading, or reserve conclusion follows
from any outcome.

**Also inherited unchanged:** the target family and realized-variance construction; interval
semantics; `P_at`; horizon; cadence; source; development dates; blocks; embargo; purge; baseline;
estimator class; QLIKE; equal block weighting; bootstrap; pass rule; fail rule; invalid-run rule;
reserve boundary; anti-tuning rules; consequence rules; the §33 output-artefact contract (including
the deterministic synthetic timestamp-boundary proof and the leakage/split/coverage proof, both
validated before any metric is computed); the §34 sidecar/provenance fields and the eight
non-authorization flags; and the §35 prohibited-deviation list.

## 10. Exact corrected feature contract (frozen)

This section is the re-preregistration. It is frozen in full and contains no menu, no secondary
set, no fallback, no "choose later", no conditional drop, no post-data repair path, no
regularization rescue, no relaxed threshold, and no ablation path.

### 10.1 Exact feature names and count

**Exactly two** committed, sign-invariant, non-directional feature columns at the 60s window:

| # | Committed column | Family | Committed dtype / null policy | Mechanism role |
|---|---|---|---|---|
| x1 | `rolling_aggtrade_count_60s` | trade-arrival intensity | `int64`, non-null by construction | information-arrival rate |
| x2 | `rolling_quantity_sum_60s` | unsigned traded-volume intensity | decimal string, non-null by construction | liquidity-demand magnitude |

```
CORRECTED_CF1_FEATURE_SET = { rolling_aggtrade_count_60s, rolling_quantity_sum_60s }
CORRECTED_CF1_FEATURE_COUNT = 2
```

`rolling_quantity_mean_60s` is **removed** and is prohibited for any future CF-1 execution under this
contract, together with the original three-feature transformed set, which is marked
`STRUCTURALLY_NON_IDENTIFIABLE__PROHIBITED_FOR_FUTURE_EXECUTION`.

All directional exclusions of Phase 4bn-AY §16 remain absolute and unchanged.

### 10.2 Exact feature window

The committed **60s** trailing window only:
`(t_last − 60_000 ms, t_last]`, `causal_window_rule = "trailing_right_open_left"`, where `t_last` is
the snapshot row's `transact_time_ms ≤ t`. No other window, no window search, no multi-window
stacking.

### 10.3 Exact snapshot rule

Unchanged from Phase 4bn-AY §11: the value of each column on the **last committed feature row with
`feature_timestamp_ms ≤ t`** (equivalently `source_transact_time_ms ≤ t`; the committed schema sets
`feature_timestamp_ms == source_transact_time_ms`), using the committed `row_index_le_R` tie rule
(greatest canonical `row_index` among rows at timestamp `t`). A feature row timestamped exactly at
`t` is available at the origin and may be used. This reads the same origin information set as
`G_0 = P_at(t)` and the HAR terminal price `P_at(t)`.

### 10.4 Exact transformation

Natural logarithm of each retained feature:

```
u1(t) = ln( rolling_aggtrade_count_60s(t) )
u2(t) = ln( rolling_quantity_sum_60s(t) )
```

No other transform. No interactions, no polynomial expansion, no ratios, no differencing. In
particular the quotient `x2 / x1` is **not** formed as a feature; the contrast `u2 − u1` lies inside
the retained span and is available to the estimator as a linear combination, which is exactly why no
mechanism content is lost.

**Positivity at a valid origin.** A valid origin requires `rolling_aggtrade_count_60s ≥ 1` and
`rolling_quantity_sum_60s > 0`, so both logarithms are finite. See §10.9.

### 10.5 Exact standardization rule

Unchanged in form from Phase 4bn-AY §14, applied to the two retained features:

```
z_j(t) = ( u_j(t) − μ_j^train ) / max( σ_j^train , 1e-8 ),   j ∈ {1, 2}
```

with `μ_j^train`, `σ_j^train` fitted on the **expanding training origins of each evaluation block
only** (population standard deviation), then applied to that block.
`STANDARDIZATION_EPSILON = 1e-8`. No clipping, no winsorization of features or target. HAR log-RV
regressors remain unstandardized in `ln(RV+ε)` units. No global statistic; no evaluation block
influences any preprocessing fitted for itself.

### 10.6 Exact augmented equation

```
y(t) = β0 + β1·ln(RV_h(t)+ε) + β2·ln(RV_d(t)+ε) + β3·ln(RV_w(t)+ε)
            + γ1·z1(t) + γ2·z2(t) + u(t)

ŷ_aug(t) = β̂0 + β̂1·ln(RV_h+ε) + β̂2·ln(RV_d+ε) + β̂3·ln(RV_w+ε) + γ̂1·z1 + γ̂2·z2
ĥ_aug(t) = exp( ŷ_aug(t) )
```

The baseline equation is unchanged and is exactly this model with `γ1 = γ2 = 0`. Nesting is
preserved: the two models share target, geometry, estimator, training window, forecast origins, and
preprocessing scope, and differ **only** by the two microstructure regressors. Exactly one augmented
model; no model-class search, no feature selection, no regularization, no post-hoc interaction, and
no alternate augmented specification after results.

### 10.7 Exact parameter count

```
AUGMENTED_PARAMETER_COUNT = 1 (intercept) + 3 (HAR) + 2 (microstructure) = 6
BASELINE_PARAMETER_COUNT  = 1 (intercept) + 3 (HAR)                     = 4
EXPECTED_AUGMENTED_STRUCTURAL_RANK = 6   (full column rank)
```

Superseded value: the Phase 4bn-AY augmented parameter count of **7** with structural rank **6**.

### 10.8 Exact minimum training-origin count

The Phase 4bn-AY rule `10 × (#parameters)` is retained unchanged in form; only its arithmetic
consequence moves with the parameter count:

```
MIN_TRAINING_ORIGINS_AUGMENTED = 10 × 6 = 60
```

Superseded value: `70`. Fewer than 60 valid training origins in any block ⇒ `CF1_INVALID_RUN`.
`MIN_BLOCK_VALID_ORIGINS = 100` valid paired evaluation origins per block is **unchanged**.

### 10.9 Exact estimability proof (symbolic, pre-data)

**Claim.** Under the committed definitions, the corrected augmented design has full column rank 6,
and no exact affine identity among its columns is implied by source.

**Step 1 — the redundancy is removed.** The unique algebraic identity present in the Phase 4bn-AY
transformed set is `ln x3 = ln x2 − ln x1`, which arises solely because
`x3 = x2 / x1` by construction. Removing `x3` removes the sole identity. No remaining pair of
retained columns stands in any functional relation declared or implied by
`features_schema.py`, `features_schema_v002.py`, or `features_compute.py`.

**Step 2 — `u1` and `u2` are not affinely dependent.** Suppose constants `(a, b, c)` with
`a·u1(t) + b·u2(t) + c = 0` for all admissible origins. `x1` is the cardinality of the trade set in
the 60s window (`window_count`); `x2` is the sum of that set's quantities (`window_qty`). The
committed computation derives them from two independent cumulative accumulators (`cum_qty` and the
index difference), and the individual quantities are free positive decimal values not determined by
the cardinality: a window of cardinality `n` admits a continuum of distinct quantity sums.
Consequently `u2` is not a function of `u1`, and no such `(a, b, c) ≠ (0,0,0)` exists. This argument
is purely definitional and opens no data.

**Step 3 — no dependence on the HAR block.** `ln(RV_h+ε)`, `ln(RV_d+ε)`, `ln(RV_w+ε)` are built from
the price path via `P_at(·)` and the minute-return kernel. `u1` and `u2` are built from trade
cardinality and traded quantity. They share no accumulator, no input column, and no construction
step; no algebraic identity connects the two groups. (Conceptual association between activity and
volatility is the hypothesis under test, not an identity; empirical correlation is not measured in
this phase and is not the criterion.)

**Step 4 — standardization preserves rank.** Let `X = [1, ln(RV_h+ε), ln(RV_d+ε), ln(RV_w+ε), u1, u2]`
and let `X'` be the design after train-only z-scoring of the last two columns. Then `X' = X · T`
where `T` is the 6×6 upper-triangular matrix that is the identity except for
`T[5,5] = 1/s1`, `T[6,6] = 1/s2`, `T[1,5] = −μ1/s1`, `T[1,6] = −μ2/s2`, with
`s_j = max(σ_j^train, 1e-8) > 0`. `det(T) = 1/(s1·s2) ≠ 0`, so `T` is invertible,
`colspace(X') = colspace(X)` and `rank(X') = rank(X)`. Standardization therefore **cannot** create
or conceal a deterministic dependency. The intercept column absorbs the location shift exactly.

**Step 5 — validity domain.** At a valid origin `rolling_aggtrade_count_60s ≥ 1` and
`rolling_quantity_sum_60s > 0` (§10.10), so `u1` and `u2` are finite real numbers and no
non-finite input can enter the design.

**Conclusion.** The corrected augmented design is **structurally identifiable** with expected
column rank 6. This is a symbolic proof of the absence of *structural* rank deficiency; it is not a
claim about any numerical condition number on unopened data. The runtime rank, zero-variance,
condition-number, and non-finite guards of §10.11 are retained **unchanged and unrelaxed** as the
fail-closed backstop, exactly as in Phase 4bn-AY.

**Non-data-driven proof.** The correction is forced by algebra, not chosen from outcomes: (i) the
admissible universe is closed at three columns by enumeration of the committed schema; (ii) the
maximal linearly independent subset has cardinality 2 (cardinality theorem); (iii) all three
admissible pairs span the identical column space and therefore yield identical fitted values and
identical values of every decision statistic, so **no observable outcome could distinguish them**
and no data-driven selection is possible even in principle; (iv) the specific pair is fixed by
committed-source properties only — primitiveness, non-nullability, and absence of quantization loss.
No Phase 4bn-AZ metric was consulted, and none exists.

### 10.10 Exact invalidation guards (inherited; feature-dependent clauses restated)

All Phase 4bn-AY §19 and §31 invalidation conditions are inherited **unchanged and unrelaxed**. The
condition-number threshold remains `> 1e10`; it is **not** relaxed, widened, or made conditional.
The feature-dependent clauses read, under the corrected contract:

- fewer than **60** valid training origins in any block ⇒ `CF1_INVALID_RUN`;
- training design-matrix condition number `> 1e10` ⇒ `CF1_INVALID_RUN`;
- any zero-variance training regressor ⇒ `CF1_INVALID_RUN`;
- a rank-deficient augmented training design (rank `< 6`) ⇒ `CF1_INVALID_RUN`;
- a singular normal-equations matrix or non-finite coefficient ⇒ `CF1_INVALID_RUN`;
- **origin validity:** an origin is invalid, and dropped identically from both models, if
  `rolling_aggtrade_count_60s < 1` or `rolling_quantity_sum_60s ≤ 0` at the snapshot, or if any
  feature value is null or non-finite. This predicate is **equivalent** to the Phase 4bn-AY §15
  predicate: by the committed `null_when_empty` policy, `rolling_quantity_mean_60s` is null exactly
  when `window_count = 0`, and a zero quantity sum with `count ≥ 1` would have produced
  `ln(x3) = −∞` and tripped the Phase 4bn-AY non-finite guard. **The corrected contract therefore
  selects the same valid-origin set as the invalid contract**;
- no imputation of any feature; no forward-fill across invalid windows; no NaN/Inf in any model
  input;
- using `rolling_quantity_mean_60s`, or any three-feature microstructure set, or any feature outside
  `CORRECTED_CF1_FEATURE_SET`, is a feature-contract violation ⇒ `CF1_INVALID_RUN`;
- relaxing the condition-number threshold, adding regularization, or dropping a feature after seeing
  a diagnostic is a contract violation ⇒ `CF1_INVALID_RUN`.

### 10.11 Exact output columns

The Phase 4bn-AY §33 output-artefact contract is inherited unchanged except that the target layer
and the model-run manifest carry **two** microstructure snapshot columns instead of three:

- target layer, per valid origin: `RV(t)`, `y(t)`, `RV_h`, `RV_d`, `RV_w`, the snapshot columns
  `rolling_aggtrade_count_60s` and `rolling_quantity_sum_60s`, the split/block assignment, and the
  origin-validity fields. The column `rolling_quantity_mean_60s` is **not** emitted, not carried,
  and not stored;
- model-run manifest: frozen constants including
  `feature_list = ["rolling_aggtrade_count_60s", "rolling_quantity_sum_60s"]`,
  `feature_count = 2`, `augmented_parameter_count = 6`, `min_training_origins = 60`;
- all other §33 and §34 artefacts, sidecars, provenance fields, and the eight non-authorization
  flags (`ml_authorized`, `diagnostics_authorized`, `strategy_authorized`, `signals_authorized`,
  `pnl_authorized`, `backtest_authorized`, `live_authorized`, `exchange_write_authorized`, all
  `false`) are unchanged.

### 10.12 Exact future execution checklist changes

Recorded in full in
`2026-07-20_phase-4bn-ba_cf1-corrected-execution-validation-checklist.md`. In summary: the feature
list becomes the two retained columns; the augmented parameter count becomes 6; the training minimum
becomes 60; a pre-data symbolic estimability restatement is added as a fail-closed gate; the runtime
rank / zero-variance / condition-number guards are retained unchanged; the no-rerun rule and the
prohibition on reusing any Phase 4bn-AZ artefact as a scientific metric are added explicitly. Every
other Phase 4bn-AY gate is inherited verbatim.

### 10.13 Exact supersession statement

- **Phase 4bn-AY remains historical and merged.** Its documents are not modified, rewritten, or
  withdrawn.
- **Phase 4bn-AZ remains an invalid run.** Its verdict, result state, reports, and artefacts stand
  exactly as recorded.
- **The Phase 4bn-BA corrected feature contract supersedes only the Phase 4bn-AY original
  feature-set specification and its directly dependent fields** — namely: the exact feature names
  (§11); the feature count (§11); the augmented equation (§18); the augmented parameter count and
  the `10 × parameters` training minimum (§19, §23); the feature transformation table (§13); the
  standardization scope enumeration (§14); the missing-feature validity predicate (§15); the
  feature-dependent clauses of the numerical and invalidation guards (§19, §31); the manifest and
  checklist feature lists; the target-layer and manifest output columns (§33); and the estimability
  proof requirements tied to those fields — **for any future corrected experiment only.**
- **Every other Phase 4bn-AY field remains inherited unchanged**, as enumerated in §9.
- **No past document, run, metric, or verdict is rewritten.**

## 11. Fields superseded (exhaustive)

| Field | Phase 4bn-AY value | Phase 4bn-BA corrected value |
|---|---|---|
| Feature names | `rolling_aggtrade_count_60s`, `rolling_quantity_sum_60s`, `rolling_quantity_mean_60s` | `rolling_aggtrade_count_60s`, `rolling_quantity_sum_60s` |
| Feature count | 3 | 2 |
| Transformed regressors | `z1, z2, z3` | `z1, z2` |
| Augmented equation | `… + γ1·z1 + γ2·z2 + γ3·z3` | `… + γ1·z1 + γ2·z2` |
| Augmented parameter count | 7 | 6 |
| Expected augmented structural rank | 6 (deficient) | 6 (full) |
| Minimum training origins (`10 × params`) | 70 | 60 |
| Missing-feature validity predicate | `rolling_quantity_mean_60s` non-null | `count ≥ 1` and `quantity_sum > 0` (equivalent set) |
| Manifest / checklist feature list | three columns | two columns |
| Target-layer snapshot columns | three | two |

Everything not in this table is inherited unchanged.

## 12. Future execution identity

`The corrected specification is a new preregistration and any future execution is a new experiment, not a rerun or continuation of Phase 4bn-AZ.`

A future corrected CF-1 execution would be a **new experiment under the Phase 4bn-BA contract**. It
is explicitly **not**:

- a Phase 4bn-AZ rerun;
- a Phase 4bn-AZ continuation;
- a Phase 4bn-AZ correction-in-place;
- a reuse of the consumed Phase 4bn-AZ evidence-bearing run;
- a reclassification of Phase 4bn-AZ.

Proposed future title, **proposed only**:

```
Phase 4bn-BB — Corrected CF-1 Realized-Volatility Substrate-Test Execution
```

**Phase 4bn-BB is not authorized.** No data read is authorized. No synthetic proof is run. No
implementation is written. No model is fitted. No metric is computed.

`The corrected feature contract is frozen before any new execution and contains no fallback, ablation, or post-data feature-selection path.`

`Phase 4bn-BB or any future corrected execution requires separate operator authorization and a new Claude Code prompt.`

## 13. No-data and no-execution boundary

`No market data, target row, feature row, model output, diagnostic output, or local Phase 4bn-AZ artefact was opened or read by Phase 4bn-BA.`

`No QLIKE, bootstrap, model fitting, target generation, feature generation, diagnostic, backtest, PnL analysis, data acquisition, paper, shadow, live, or exchange-write execution is authorized by Phase 4bn-BA.`

Evidence used by this phase was limited to: committed documents; committed source
(`features_schema.py`, `features_schema_v002.py`, `features_compute.py`); committed schema/compute
policy constants; Git metadata; and static symbolic reasoning. `data/microstructure/` and
`data/research/` were not opened or listed for content. No local Phase 4bn-AZ artefact was opened.
No correlation, condition number, or residual was computed. No test, linter, type-checker, builder,
or script was run: this phase changes no executable surface.

`The v002 terminal window and v002 sealed test remain untouched and excluded.`

`The consumed pre-v002 internal holdout and the 2024-11-01 through 2024-11-15 buffer remain unopened.`

`No evidence reserve is authorized for spending by Phase 4bn-BA.`

Reserve statuses restated and unchanged: `PRE_V002_INTERNAL_HOLDOUT = CONSUMED`;
`V002_TERMINAL_WINDOW = UNTOUCHED_RESERVED`; `V002_SEALED_TEST = UNTOUCHED_RESERVED`;
`HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE`; `test_rows_loaded = 0`;
`v002_terminal_window_read = false`; `sealed_test_split_touched = false`;
`consumed_holdout_opened = false`; `november_buffer_opened = false`. No evidence-ledger status
transition occurs.

## 14. Consequences

- **This phase makes no scientific claim.** It tests nothing, measures nothing, and narrows no lane.
  The CF-1 hypothesis remains **scientifically untested**.
- The aggTrades magnitude lane remains **open and unnarrowed**; Phase 4bn-AZ did not narrow it, and
  Phase 4bn-BA does not narrow it.
- Phase 4bn-AZ remains `CF1_INVALID_RUN` and its evidence-bearing run remains consumed. No rerun of
  Phase 4bn-AZ is authorized by anything in this phase.
- A future corrected execution, if separately authorized, would produce exactly one of
  `CF1_VALID_PASS`, `CF1_VALID_FAIL`, or `CF1_INVALID_RUN` under the inherited routing. A valid pass
  would remain magnitude-only and would establish no direction, no economic materiality, no
  profitability, no ability to clear the locked 8 bps/side · 16 bps round trip, and no tradability.
  A valid fail would close or narrow only the corrected preregistered magnitude lane.
- This phase does not clear M0 for any strategy. `research_eligible = false`;
  `eligibility_gate_status = pending`; all authorization flags remain `false`; the Phase 4aw
  `flip_research_eligible(...)` always-raising behaviour is preserved and was not invoked.
- No stopped arc is softened, merged, reinterpreted, reopened, or rescued.

`Remaining paused is a valid operator choice.`

## 15. Result state

```
CF1_CORRECTED_FEATURE_CONTRACT_REPREREGISTERED__ORIGINAL_AZ_INVALID_RUN_PRESERVED__ESTIMABILITY_AND_ANTI_DUPLICATION_AUDIT_PASSED__NO_DATA_OPENED__NO_EXECUTION_AUTHORIZED__RESERVES_UNTOUCHED
```

## 16. Next operator action

1. Review the four Phase 4bn-BA documents on the branch, in particular the estimability and
   anti-duplication audit and the corrected feature contract in §10 above.
2. Decide whether to authorize a **separate merge phase** for Phase 4bn-BA. No merge is performed or
   authorized by this phase, and no merge-closeout is created.
3. Independently and only after a merge decision, decide whether to authorize
   `Phase 4bn-BB — Corrected CF-1 Realized-Volatility Substrate-Test Execution`, which would require
   a new operator authorization and a new Claude Code prompt. It is not authorized here.
4. `Remaining paused is a valid operator choice.` Recommended state: **paused**, pending operator
   review and a separate merge decision.
