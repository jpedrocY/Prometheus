# Phase 4bn-BA — CF-1 Estimability and Anti-Duplication Audit

This is the symbolic, source-definition-based companion to the Phase 4bn-BA main memo
(`2026-07-20_phase-4bn-ba_cf1-feature-contract-correction-and-repreregistration.md`). It records the
full candidate audit backing the corrected feature contract.

The audit is **docs-only and static**. No market data, target row, feature row, model output,
diagnostic output, or local Phase 4bn-AZ artefact was opened. No correlation, condition number,
rank, residual, or metric was computed. Every claim below is derived from committed source
definitions, committed schema policy constants, and committed reports.

**Three levels are kept strictly separate throughout this audit and must not be conflated:**

1. **Ideal arithmetic identity** — a statement about the exact quotient `x3* = x2/x1`:
   `ln(x3*) = ln(x2) − ln(x1)`. Exact, but about an ideal quantity, not about any stored column.
2. **Committed stored feature** — a statement about the serialized column
   `x3 = rolling_quantity_mean_60s`, which the committed formatter produces by **floor
   quantization**: `ln(x3) = ln(x2) − ln(x1) + δ`, with `δ ≤ 0`, `δ = 0` only when the quotient is
   exactly representable at the stored precision, and `δ` **generally nonzero**. No exact stored
   identity is claimed anywhere in this audit.
3. **Phase 4bn-AZ empirical evidence** — on the Phase 4bn-AZ frozen target layer, `|δ|` was recorded
   at near machine precision (`max = 3.33e-14`, `mean = 3.51e-15`) and the resulting augmented
   conditioning exceeded the frozen `1e10` guard in all seven blocks. This is **near-machine-precision
   transformed dependence on the Phase 4bn-AZ frozen target layer**, cited from the committed Phase
   4bn-AZ report and **not recomputed**. It is evidence of effective dependence, not a universal
   exact theorem.

---

## 1. Source files inspected

| File | Committed evidence extracted |
|---|---|
| `src/prometheus/research/microstructure/features_schema.py` | `PER_WINDOW_FEATURE_TEMPLATES` (10 templates, lines 68-79); `FEATURE_WINDOWS_MS_V001 = (1000, 5000, 15000, 60000)` (line 57); `FEATURE_WINDOW_LABELS_V001 = ("1s","5s","15s","60s")` (line 60); `FEATURE_NAMES_V001` construction (lines 83-100) — 40 windowed + 3 time-context + 2 quality = 45; `LINEAGE_COLUMNS_V001` (16); `FEATURE_SCHEMA_V001` (61); `DECIMAL_POLICY_V001` (lines 196-204); `NULL_POLICY_V001` (lines 207-214); `INVALID_WINDOW_POLICY_V001`; import-time assertions (lines 410-420) |
| `src/prometheus/research/microstructure/features_schema_v002.py` | `PER_WINDOW_FEATURE_TEMPLATES_V002 = PER_WINDOW_FEATURE_TEMPLATES` (line 129); `FEATURE_WINDOWS_MS_V002 = FEATURE_WINDOWS_MS_V001` (line 123); `FEATURE_WINDOW_LABELS_V002 = FEATURE_WINDOW_LABELS_V001` (line 126); `NULL_POLICY_V002` (lines 192-198); assertions `len(FEATURE_NAMES_V002) == 45`, `len(FEATURE_SCHEMA_V002) == 62` (lines 453-454) |
| `src/prometheus/research/microstructure/features_compute.py` | `_format_mean_as_decimal_string` (lines 141-159); window accumulators `window_count`, `window_qty`, `window_buy`, `window_sell`, `window_buy_count`, `window_sell_count` (lines 327-336); `qty_sum_strs` (lines 338-342); `qty_mean_strs` (lines 343-349); log-return computation (lines 383-387); column assignment (lines 389-397); dtype prefix groups (lines 459-477) |
| Committed reports | Phase 4bn-AY preregistration, contract, checklist, closeout, merge-closeout; Phase 4bn-AZ execution-and-verdict, artefact/leakage/split-validation, closeout, merge-closeout |
| Committed process standards | phase workflow, risk tiering, operator report, merge-closeout, evidence-budget ledger, scarce-reserve spending / late inadmissibility |
| Git metadata | branch, base, lineage SHAs, commit graph |

**Not inspected:** `data/microstructure/`, `data/research/`, any Parquet, any JSON artefact, any
`.sha256` sidecar content, any Phase 4bn-AZ local output. Phase 4bn-AZ implementation code and tests
were treated as committed code evidence only via the committed AZ reports; no artefact they produced
was opened.

## 2. The candidate universe is closed

The committed aggTrades feature schema declares exactly ten per-window templates
(`features_schema.py:68-79`):

```
rolling_aggtrade_count_{w}
rolling_quantity_sum_{w}
rolling_quantity_mean_{w}
rolling_aggressive_buy_quantity_{w}
rolling_aggressive_sell_quantity_{w}
rolling_aggressive_buy_count_{w}
rolling_aggressive_sell_count_{w}
rolling_aggressive_flow_ratio_{w}
rolling_aggressive_quantity_imbalance_{w}
rolling_log_return_past_window_{w}
```

instantiated over four windows, plus `utc_hour`, `utc_minute`, `milliseconds_since_day_start`,
`invalid_window_flag`, `rolling_missing_window_flag`. `features_schema_v002.py:129` reuses the same
template tuple by direct import, so **v002 adds no feature template**. There is no other committed
aggTrades feature family, and no committed column outside this list.

The Phase 4bn-AY contract froze the **60s** window (§12), inherited unchanged. The universe under
audit is therefore the ten 60s columns plus the time-context and quality columns.

**No new feature is invented, no feature-builder change is authorized, no other source is used, and
no data is acquired by this audit.**

## 3. Per-candidate audit

Legend: **sign-invariant** = the value is unchanged under relabelling of aggressor side;
**directional** = the value encodes side identity or return sign.

### C1 — `rolling_aggtrade_count_60s`

| Property | Value |
|---|---|
| Exact committed column | `rolling_aggtrade_count_60s` |
| Exact source definition | `window_count = (n_indices + 1) − lo_arr` where `lo_arr = searchsorted(transact_time_ms, T − 60_000, side="right")` (`features_compute.py:327-331`); i.e. the cardinality of the trade set in the trailing window |
| Exact window | `(T − 60_000 ms, T]`, `causal_window_rule = "trailing_right_open_left"` |
| dtype / null policy | `int64`, non-null by construction (`int64_count_prefixes`, `features_compute.py:462-466`); no null-policy entry — never null |
| Sign-invariant | **yes** — counts trades irrespective of aggressor side |
| Directional | no |
| Deterministic function of another candidate | **no** — cardinality is not determined by any other retained candidate |
| Frozen transform creates a linear identity | **no** |
| Duplicates a HAR regressor | **no** — HAR regressors are log realized variances of the price path; this is a trade count |
| Stopped/rejected family | **no** |
| **Admissible** | **YES — RETAINED** |

Mechanism: trade-arrival intensity, the information-arrival rate channel of the CF-1 hypothesis.

### C2 — `rolling_quantity_sum_60s`

| Property | Value |
|---|---|
| Exact committed column | `rolling_quantity_sum_60s` |
| Exact source definition | `window_qty = cum_qty[n_indices+1] − cum_qty[lo_arr]`, rendered by `_format_int_as_decimal_string(window_qty, max_dp_q)`; `"0"` when `window_count == 0` (`features_compute.py:332, 338-342`) |
| Exact window | `(T − 60_000 ms, T]`, `trailing_right_open_left` |
| dtype / null policy | decimal string, **non-null** by construction (`non_null_decimal_prefixes`, `features_compute.py:471-476`); `DECIMAL_POLICY_V001` `raw_quantity_storage = "decimal_string"`; no null-policy entry |
| Sign-invariant | **yes** — sums all quantities irrespective of aggressor side (distinct from the separate buy/sell sums, which are directional) |
| Directional | no |
| Deterministic function of another candidate | **no** — the sum is not determined by the cardinality |
| Frozen transform creates a linear identity | **no** |
| Duplicates a HAR regressor | **no** — traded quantity shares no accumulator or construction step with the price-path RV cascade |
| Stopped/rejected family | **no** |
| **Admissible** | **YES — RETAINED** |

Mechanism: unsigned traded-volume intensity, the liquidity-demand magnitude channel.

### C3 — `rolling_quantity_mean_60s`

| Property | Value |
|---|---|
| Exact committed column | `rolling_quantity_mean_60s` |
| Exact source definition | `None if window_count == 0 else _format_mean_as_decimal_string(window_qty, window_count, max_dp_q)` (`features_compute.py:343-349`), where `_format_mean_as_decimal_string(sum_int, count, max_dp)` returns `sum_int / count` as a fixed-point string with `max_dp + 12` decimals via `mean_int = (sum_int · 10**12) // count` (`features_compute.py:141-159`) |
| Exact window | `(T − 60_000 ms, T]`, `trailing_right_open_left` — **the same window as C1 and C2** |
| dtype / null policy | decimal string, **nullable** — the only nullable column of the three (`nullable_decimal_prefixes = ("rolling_quantity_mean_",)`, `features_compute.py:477`; `NULL_POLICY_V001["rolling_quantity_mean"] = "null_when_empty"`; identical at v002) |
| Sign-invariant | yes |
| Directional | no |
| Deterministic function of another candidate | **YES — deterministically derived from C1 and C2 alone**, via the floor quantizer `mean_int = (sum_int × 10^12) // count`. Same numerator accumulator (`window_qty`), same denominator accumulator (`window_count`), same window. The stored value is `C3 = C3* − q` with `C3* = C2/C1`, `q ≥ 0`, and `q` strictly less than one unit of the stored least-significant decimal place; `q = 0` only when the quotient is exactly representable at that precision. **No universal relative-error bound is asserted**, because the absolute quantization step is bounded but the relative step is not bounded independently of `C3*` |
| Frozen transform creates a linear identity | **Ideally yes, in stored form no.** `ln C3* = ln C2 − ln C1` exactly; the stored column satisfies `ln C3 = ln C2 − ln C1 + δ`, `δ ≤ 0`, generally nonzero. The stored transformed column is therefore **not guaranteed to be an exact affine combination**, but it is **numerically almost collinear** with `ln C2 − ln C1` and supplies **no independent information** |
| Duplicates a HAR regressor | not applicable — rejected earlier |
| Stopped/rejected family | no |
| **Admissible** | **NO — REJECTED: deterministically derived from C1 and C2, contributing no independent information while driving the augmented design to catastrophic conditioning. Its inclusion alongside C1 and C2 is the defect that invalidated Phase 4bn-AZ (condition numbers ≈ 1e16 against a frozen `> 1e10` guard, all seven blocks)** |

### C4–C7 — `rolling_aggressive_buy_quantity_60s`, `rolling_aggressive_sell_quantity_60s`, `rolling_aggressive_buy_count_60s`, `rolling_aggressive_sell_count_60s`

| Property | Value |
|---|---|
| Exact source definitions | `window_buy = cum_buy_qty[...] − cum_buy_qty[lo_arr]`; `window_sell = cum_sell_qty[...] − cum_sell_qty[lo_arr]`; `window_buy_count`, `window_sell_count` analogously (`features_compute.py:333-336`) |
| Exact window | `(T − 60_000 ms, T]` |
| dtype / null policy | buy/sell quantities: decimal string non-null; buy/sell counts: `int64` non-null |
| Sign-invariant | **no** — each carries aggressor-side identity |
| Directional | **yes** |
| Deterministic function of other candidates | partially: `C4 + C5 = C2` and `C6 + C7 = C1` exactly, so admitting any three of `{C1, C2, C4, C5}` or `{C1, C6, C7}` would itself create a new exact linear identity |
| Stopped/rejected family | directional-input prohibition |
| **Admissible** | **NO — REJECTED: explicitly prohibited directional columns (Phase 4bn-AY §11, §16; Phase 4bn-BA mandate §5). Independently rejected: they would reintroduce exact additive identities with the retained columns.** |

### C8 — `rolling_aggressive_flow_ratio_60s`

| Property | Value |
|---|---|
| Exact window / dtype | `(T − 60_000 ms, T]`; `float64` nullable, `NULL_POLICY_V001` `"null_when_zero_denominator"` |
| Sign-invariant | **no** — a signed buy/sell flow ratio |
| Directional | **yes** |
| **Admissible** | **NO — REJECTED: explicitly prohibited directional column** |

### C9 — `rolling_aggressive_quantity_imbalance_60s`

| Property | Value |
|---|---|
| Exact window / dtype | `(T − 60_000 ms, T]`; decimal string, non-null (`non_null_decimal_prefixes`) |
| Sign-invariant | **no** — a signed buy-minus-sell quantity imbalance |
| Directional | **yes** |
| Deterministic function of other candidates | it is an exact linear combination of C4 and C5 |
| **Admissible** | **NO — REJECTED: explicitly prohibited directional column; also algebraically dependent on C4/C5** |

### C10 — `rolling_log_return_past_window_60s`

| Property | Value |
|---|---|
| Exact source definition | `log_return_list[i] = ln(price_float[i] / price_float[prior_idx])`, null when no prior reference or a non-positive price (`features_compute.py:383-387`; `NULL_POLICY_V001` `"null_when_no_prior_reference_or_zero_price"`) |
| Exact window / dtype | `(T − 60_000 ms, T]`; `float64` nullable |
| Sign-invariant | **no** — a signed price return |
| Directional | **yes** |
| Conceptual overlap with HAR | **yes, additionally** — it is a price-path return object, the same primitive from which the HAR realized-variance regressors are constructed |
| **Admissible** | **NO — REJECTED: signed return, explicitly prohibited; and conceptually overlapping the baseline's own construction primitive** |

### C11 — `utc_hour`, `utc_minute`, `milliseconds_since_day_start`

Time-context columns, `int8` / `int64`. Not mechanism features; calendar inputs are explicitly
prohibited by Phase 4bn-AY §16 and by the Phase 4bn-BA mandate. **REJECTED.**

### C12 — `invalid_window_flag`, `rolling_missing_window_flag`

Boolean data-quality flags governed by `INVALID_WINDOW_POLICY_V001`. Not mechanism features; they
describe window validity, not market activity. **REJECTED.**

## 4. Required explicit statement — no independent dispersion column exists

**There is no committed sign-invariant dispersion, standard-deviation, variance, quantile,
range, or higher-moment column of trade size in the aggTrades feature schema at any window.** The
only committed central-moment column is `rolling_quantity_mean_{w}`, and it is exactly the
redundant quotient audited as C3. Phase 4bn-AY §11 recorded the same finding and declined to invent
one; this audit independently confirms it by enumeration of `PER_WINDOW_FEATURE_TEMPLATES` and of
its v002 alias.

**There is likewise no other committed sign-invariant non-directional activity-magnitude column**
outside `{C1, C2, C3}`. Every remaining committed column is directional, a signed return, a
time-context column, or a quality flag.

Adding a dispersion feature would require building a **new committed column** — a new feature
family, a feature-builder change, and a separate feature-contract phase. That is outside a bounded
contract repair and is not done, not proposed, and not authorized here.

## 5. Raw and transformed feature equations

**Raw (committed definitions, 60s window, snapshot at the last feature row with
`feature_timestamp_ms ≤ t`):**

```
x1(t)  = rolling_aggtrade_count_60s(t) = |{ trades u : t_last − 60_000 < ts(u) ≤ t_last }|
x2(t)  = rolling_quantity_sum_60s(t)   = Σ_{u in that window} q(u)
x3*(t) = x2(t) / x1(t)                                   [ideal arithmetic mean]
x3(t)  = rolling_quantity_mean_60s(t)  = floor_scaled( x3*(t) )   [stored committed feature]
       = x3*(t) − q(t) ,   0 ≤ q(t) < one stored least-significant decimal unit
```

**Transformed under the frozen Phase 4bn-AY §13 transform (natural logarithm), before
standardization:**

```
u1(t)  = ln x1(t)
u2(t)  = ln x2(t)
u3*(t) = ln x3*(t) = u2(t) − u1(t)                       [ideal — exact]
u3(t)  = ln x3(t)  = u2(t) − u1(t) + δ(t)                [stored — δ ≤ 0, generally nonzero]
```

`δ(t) = ln(1 − q(t)/x3*(t)) ≤ 0`, and `δ(t) = 0` only when `q(t) = 0`.

**After train-only z-scoring (§14):**

```
z_j(t) = ( u_j(t) − μ_j^train ) / s_j ,   s_j = max(σ_j^train, 1e-8) > 0
```

## 6. Symbolic dependency structure

Writing each transformed candidate in the basis `(1, u1, u2)`:

| Transformed feature | coefficient on `1` | on `u1` | on `u2` | residual term |
|---|---|---|---|---|
| `u1` | 0 | 1 | 0 | — |
| `u2` | 0 | 0 | 1 | — |
| `u3*` (**ideal**) | 0 | **−1** | **+1** | none — exact |
| `u3` (**stored**) | 0 | −1 | +1 | **`+ δ`**, `δ ≤ 0`, generally nonzero |

**At the ideal level** the three rows `(u1, u2, u3*)` form a rank-2 system with the exact null
relation `(+1)·u1 + (−1)·u2 + (+1)·u3* = 0`.

**At the stored level this null relation does not hold exactly.** The corresponding combination
evaluates to `δ(t)`, not to zero, so **no exact null vector is claimed for the stored transformed
columns**, and no exact rank statement is made about the stored three-column block for every possible
serialized dataset.

What *is* established from source: `u3` is deterministically derived from `u1` and `u2` and carries
no independent information; it differs from an exact affine combination of them only by the
deterministic quantization term `δ`. Phase 4bn-AZ recorded `max|δ| = 3.33e-14` and
`mean|δ| = 3.51e-15` on its frozen target layer — near-machine-precision transformed dependence —
and the resulting augmented condition numbers (≈ 1e16) exceeded the frozen `> 1e10` guard in all
seven blocks. That is an **effective**, empirically demonstrated rank deficiency under the frozen
guard, not a universal exact theorem.

**Conclusion.** The Phase 4bn-AY three-feature set is deterministically redundant at the
source-definition level and numerically non-identifiable under the frozen runtime guard after
serialization and logarithmic transformation. It remains marked:

```
STRUCTURALLY_NON_IDENTIFIABLE__PROHIBITED_FOR_FUTURE_EXECUTION
```

**Operational meaning of that label (binding definition).** It denotes a source-defined derived
feature whose stored transformed column produced **effective rank deficiency / catastrophic
conditioning under the frozen guard**. It does **not** assert an exact symbolic rank theorem for
every possible serialized dataset. An equivalent plain-language label for the same condition is
`SOURCE_DERIVED_REDUNDANT__EFFECTIVELY_RANK_DEFICIENT_UNDER_FROZEN_GUARD`; the required label above
remains authoritative and is not replaced.

## 7. Candidate-set comparison

Admissible sets are subsets of `{x1, x2, x3}` (§3 rejects everything else). All eight subsets:

| Set | Source-independent columns | Augmented cols (1 + 3 HAR + k) | Verdict |
|---|---|---|---|
| `{}` | 0 | 4 | rejected — no augmentation; the baseline itself, so the hypothesis is untestable |
| `{x1}` | 1 | 5 | rejected — discards the preregistered volume-intensity channel |
| `{x2}` | 1 | 5 | rejected — discards the preregistered arrival-intensity channel |
| `{x3}` | 1 | 5 | rejected — retains only the floor-quantized derived column and discards **both** primitive mechanism channels as explicit regressors; also the only nullable column |
| `{x1, x2}` | 2 | **6** | **SELECTED** |
| `{x1, x3}` | 2 | 6 | rejected on source-only grounds — retains the floor-quantized, nullable derived column and drops the primitive volume accumulator as an explicit regressor |
| `{x2, x3}` | 2 | 6 | rejected on source-only grounds — retains the floor-quantized, nullable derived column and drops the primitive count accumulator as an explicit regressor |
| `{x1, x2, x3}` | 2 (three columns, one deterministically derived) | 7 | **PROHIBITED — the Phase 4bn-AY contract; source-derived redundancy, demonstrated catastrophic conditioning under the frozen guard** |

**Admissible-cardinality finding.** `x3` is deterministically derived from `x1` and `x2` and
therefore carries **no independent information**; its stored column adds only quantization noise
while driving the augmented design toward the conditioning failure Phase 4bn-AZ demonstrated.
Consequently the **non-redundant** contract has **at most two** features, and the three 2-element
subsets each contain two source-independent columns. **A non-redundant three-feature CF-1
microstructure contract does not exist within the committed universe.** The corrected contract is
therefore the **maximal non-redundant** contract available from committed source, not a discretionary
reduction, and it is not sized to preserve the original count of three.

## 8. Pair selection — a source-only, non-data-driven tie-break

**No all-dataset outcome-equivalence claim is made.** At the *ideal* level the three pairs would span
the same two-dimensional space, since `u3* = u2 − u1`. At the **stored** level they do not: `u3`
carries its own deterministic quantization term `δ`, so the three designs are **not** guaranteed to
produce identical fitted values, identical residuals, or identical decision statistics on every
possible serialized dataset. This audit therefore does **not** assert that data could not, in
principle, distinguish the three admissible pairs.

The selection is instead made on **committed-source properties alone**, which is sufficient and
non-data-driven:

**Tie-break criteria applied (all from committed source, none from data):**

1. **Primitiveness.** `x1` and `x2` are the direct window accumulators (`window_count`,
   `window_qty`, `features_compute.py:331-332`). `x3` is deterministically derived from them, and
   neither `x1` nor `x2` is deterministically defined from the other.
2. **Non-nullability.** `x3` is the **only** nullable column of the three
   (`nullable_decimal_prefixes`, `null_when_empty`); `x1` and `x2` are non-null by construction.
   Retaining only non-null columns removes a null-handling dependency from the contract.
3. **No floor quantization.** `x3` alone is floor-quantized
   (`mean_int = (sum_int · 10**12) // count`, `features_compute.py:158`); `x1` is an exact integer
   and `x2` an exact decimal sum at the committed quantity scale.
4. **Both mechanism channels retained.** `{x1, x2}` is the only pair that keeps both named
   mechanism primitives — arrival intensity and volume intensity — as regressors in their own right,
   and the only pair containing **only** primitive, non-null, non-quantized committed accumulators.
5. **No outcome informed the choice.** Phase 4bn-AZ produced no scientific metric, so none could
   have been consulted.

## 9. Mechanism coverage of the corrected pair

The **ideal** arithmetic mean-size contrast is `ln(x2) − ln(x1)`. The committed stored mean `x3` is a
**floor-quantized approximation** to that contrast, differing from it by the deterministic term `δ`.

Retaining the two primitive regressors therefore preserves the intended count and volume primitives
and allows the estimator to represent the ideal mean-size contrast directly, **without carrying the
separately quantized derived column**. Formally, at the ideal level, for any `(γ1, γ2, γ3)` the
three-feature linear predictor built on `u3*` equals the corrected two-feature linear predictor at
`(γ1', γ2') = (γ1 − γ3, γ2 + γ3)`.

**Scope, stated honestly.** This is a statement about the *ideal* contrast. It is **not** a claim
that the corrected design exactly reproduces every fitted value of the *stored* three-feature
serialized design, and no such claim is made anywhere in this audit. What the correction removes is
a deterministically derived, quantized column that supplies no independent information and that
demonstrably destroyed the conditioning of the augmented design. **The correction removes redundancy,
not a preregistered mechanism channel:** it narrows no mechanism, weakens no hypothesis, and forfeits
neither of the two channels the Phase 4bn-AY contract named.

## 10. Symbolic rank audit of the corrected augmented design

Corrected design matrix columns:

```
X = [ 1 , ln(RV_h+ε) , ln(RV_d+ε) , ln(RV_w+ε) , u1 , u2 ]      (6 columns)
```

**Claim (scoped).** **No exact affine dependency is implied by the committed definitions between
`ln(x1)` and `ln(x2)`**, nor between the microstructure block and the HAR block. On that basis the
corrected design is declared `EXPECTED_AUGMENTED_STRUCTURAL_RANK = 6`.

**(a) Within the microstructure block.** Suppose `a·u1 + b·u2 + c = 0` identically. `x1` is the
cardinality of the window's trade set; `x2` is the sum of that set's quantities. The committed
computation derives them from two distinct accumulators — an index difference for the count
(`(n_indices + 1) − lo_arr`) and a cumulative-quantity difference for the sum
(`cum_qty[n_indices+1] − cum_qty[lo_arr]`). The individual quantities `q(u)` are free positive
decimal values not determined by the cardinality: a window of cardinality `n` admits a continuum of
distinct sums. Hence `u2` is not a function of `u1`, and no non-trivial `(a, b, c)` exists. The
source-defined redundancy that did exist in the Phase 4bn-AY set arose only from `x3` being
deterministically derived from `x1` and `x2`, and was removed with `x3`.

**(b) Between the microstructure block and the HAR block.** `ln(RV_h+ε)`, `ln(RV_d+ε)`,
`ln(RV_w+ε)` are constructed from the price path through `P_at(·)` and the minute-return kernel
`r_k = ln(G_k/G_{k−1})`, `RV = Σ r_k²`. `u1` and `u2` are constructed from trade cardinality and
traded quantity. They share **no input column, no accumulator, and no construction step**, and no
committed definition relates them. No algebraic identity connects the blocks.

**(c) Within the HAR block.** Unchanged from Phase 4bn-AY and independently evidenced as
well-behaved: `RV_h`, `RV_d`, `RV_w` are RV at three distinct horizons (1h, 24h mean, 168h mean),
none a deterministic function of the others.

**(d) The intercept.** The intercept is not an affine combination of the five non-constant columns
unless one of those columns is constant, which is exactly the zero-variance condition already
guarded fail-closed.

**Conclusion.** `EXPECTED_AUGMENTED_STRUCTURAL_RANK = 6`, versus the Phase 4bn-AY design's 7 columns
one of which was deterministically derived from two others.

**Scope limit, stated honestly.** This establishes only the **absence of a source-implied exact
dependency**. It is **not** proof that every empirical training matrix will have full numerical rank,
and it is **not** a claim about any numerical condition number on unopened data — no condition number
was computed or estimated in this phase. The runtime rank, zero-variance, condition-number
(`> 1e10`), and non-finite guards are retained **unchanged and unrelaxed** and remain the **final
arbiter** at execution time.

**Corresponding statement for the original three-feature stored design (no universal exact rank
claimed).** It exhibits: source-defined deterministic redundancy; near-machine-precision transformed
dependence as recorded by Phase 4bn-AZ (`max|δ| = 3.33e-14`, `mean|δ| = 3.51e-15`); observed
effective rank deficiency and catastrophic condition numbers (≈ 1e16) under the frozen guard in all
seven blocks; and it is **prohibited for future execution**.

## 11. Standardization does not create or hide a dependency

Let `X` be the corrected design and `X'` the design after train-only z-scoring of `u1, u2`. Then
`X' = X · T` with

```
T = I₆  except  T[5,5] = 1/s1 ,  T[6,6] = 1/s2 ,  T[1,5] = −μ1/s1 ,  T[1,6] = −μ2/s2
s_j = max(σ_j^train, 1e-8) > 0
```

`T` is upper triangular with non-zero diagonal, so `det(T) = 1/(s1·s2) ≠ 0` and `T` is invertible.
Hence `colspace(X') = colspace(X)` and `rank(X') = rank(X)`.

- Standardization **cannot create** a deterministic dependency: an invertible map cannot reduce rank.
- Standardization **cannot hide** one, and **cannot repair near-collinearity**: an invertible column
  rescaling leaves a near-dependent design near-dependent, which is why it did not rescue the Phase
  4bn-AY design — precisely as Phase 4bn-AZ recorded, with the augmented conditioning still ≈ 1e16
  after z-scoring.
- The intercept column absorbs the location shifts exactly, so centring introduces no new constraint.
- `s_j > 0` is guaranteed by the `1e-8` floor, and a genuinely constant training regressor is caught
  independently by the retained zero-variance guard.

## 12. The correction is not data-driven

1. **Closed universe by enumeration.** The admissible universe was fixed by reading
   `PER_WINDOW_FEATURE_TEMPLATES` and its v002 alias, not by scanning data.
2. **Forced cardinality.** `x3` is deterministically derived from `x1` and `x2` and carries no
   independent information (§6), so the non-redundant set size is at most 2 — a source-definition
   fact, not a measurement.
3. **No outcome-indistinguishability claim.** This audit does **not** assert that data could not
   distinguish the three admissible pairs; the stored `x3` is quantized, so such a claim would be
   unproven. The relevant fact is simply that **no data was opened and no outcome entered the
   selection**.
4. **Source-only tie-break.** The selected pair is fixed by primitiveness, non-nullability by
   construction, absence of floor quantization, and direct retention of both preregistered mechanism
   channels — all committed-source properties (§8).
5. **No metric existed.** `No Phase 4bn-AZ metric is used to select the corrected feature contract because no scientific metric was computed.`
6. **No measurement performed.** No correlation, coefficient, importance, QLIKE, condition number,
   or subgroup result was computed, consulted, or estimated in this phase.
7. **Permitted AZ facts only.** The only Phase 4bn-AZ observations used are the deterministic
   source-defined dependency and its recorded near-machine-precision residual, the numerical
   invalidation, the absence of scientific metrics, and the
   successful timestamp/split/leakage/data-integrity pipeline — the last used solely to confirm the
   failure was not a sample-size failure (per-block `n_i` 550–744 all ≥ 100; training origins
   551–4,966 all ≥ 70). No block condition-number variation, target-layer value, or origin count was
   used to choose among candidates.

## 13. Anti-rescue analysis

| Anti-rescue test | Finding |
|---|---|
| Is this a rerun, continuation, or repair-in-place of Phase 4bn-AZ? | **No.** Phase 4bn-AZ remains `CF1_INVALID_RUN`, consumed, and unmodified. A future corrected execution would be a **new experiment** under a new contract. |
| Is any remedy selected after seeing performance? | **No.** No performance was ever produced. The run fail-closed at the numerical guard before any loss was computed. |
| Is a guard relaxed, widened, or made conditional? | **No.** The `> 1e10` condition-number threshold, the rank guard, the zero-variance guard, the non-finite guard, the `≥ 100` block minimum, and the `10 × parameters` training rule are all retained unchanged in form. Only the arithmetic value `10 × 6 = 60` moves with the parameter count. |
| Is regularization, ensembling, or model-class change introduced? | **No.** Plain deterministic OLS with no tunable hyperparameter, unchanged. |
| Is the model improved, the mechanism broadened, or a sensitivity test added? | **No.** One deterministically derived column is removed; nothing is added. By §9 both preregistered mechanism channels are retained and the ideal trade-size contrast remains representable. |
| Is a fallback, ablation path, or post-data feature-selection path created? | **No.** The contract freezes exactly one set with no alternate, no secondary set, no "choose later", no conditional drop, and no post-data repair logic. |
| Is the loss, target, horizon, cadence, split, embargo, bootstrap, or pass rule altered? | **No.** All inherited unchanged. |
| Is an adverse date, block, or subgroup excluded? | **No.** The corrected valid-origin predicate excludes every origin the Phase 4bn-AY predicate excluded on those grounds; it is equal to or a superset of the Phase 4bn-AY set (main memo §10.10). No origin is excluded that Phase 4bn-AY would have retained. |
| Is the hypothesis restated to be easier? | **No.** The hypothesis is preserved verbatim, and §9 shows no preregistered channel is forfeited. |
| Could this correction have been motivated by a favourable result? | **No result exists.** Phase 4bn-AZ computed no scientific metric, and no data was opened by this phase, so no outcome could have motivated the selection. |

**Anti-rescue verdict: PASS.** The correction is a forced, minimal, outcome-independent removal of a
source-defined redundancy that produced demonstrated non-identifiability under the frozen guard, made
before any data is opened and with every guard intact.

## 14. Anti-duplication analysis

| Duplication test | Finding |
|---|---|
| Algebraic dependence among retained features | **None.** §10(a). |
| Algebraic dependence between retained features and HAR regressors | **None.** §10(b) — disjoint constructions, no shared accumulator or input column. |
| Conceptual overlap with the HAR baseline | The retained features are **activity** measures; HAR regressors are **price-variation** measures. Association between activity and volatility is precisely the CF-1 hypothesis under test, so it is the object of the experiment, not duplication. The nesting design (baseline = augmented with `γ = 0`) is what isolates *incremental* information, and it is unchanged. |
| Conceptual overlap between the two retained features | Both are 60s activity magnitudes, so they are conceptually related — but conceptual relatedness is neither algebraic dependence nor grounds for exclusion. `x1` counts events; `x2` sums their sizes. Neither determines the other. |
| Empirical correlation between retained features | **Not measured, and deliberately so.** Correlation is not the admissibility criterion, and measuring it would require opening data, which this phase does not do and is not authorized to do. |
| Duplication of a previously stopped or rescued family | **None** — see §15. |
| Duplication of the original invalid contract | The corrected set is a strict subset of it; the prohibited three-feature set is explicitly marked and barred. |

**The audit explicitly distinguishes four notions:** *source-defined deterministic derivation* (one
column computed from others by the committed builder — the disqualifying criterion, and the sole
basis for rejecting `x3`); *exact algebraic identity at the stored level* (**not** claimed for `x3`,
because of the floor quantization); *conceptual overlap* (shared mechanism intuition — recorded,
never disqualifying on its own); and *empirical correlation* (a data property — not measured, not
used, not a criterion).

## 15. Stopped-family overlap analysis

| Lock | Overlap with the corrected contract |
|---|---|
| `STOP_LONGHORIZON_ML_ARC` | **None.** That arc concerns long-horizon directional-label ML (`microstructure_labels_longhorizon_aggtrades_v001`, 5m/30m/1h). CF-1 uses **no label family at all**: it constructs its own non-directional realized-variance target from price, and its model is a 6-parameter OLS HAR extension. No long-horizon label is read, and none of the stopped arc's objects are reused. |
| `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE` | **None.** No top-of-book, bookTicker, order-book, or quote data is used or proposed. `HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE` is preserved. |
| `REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH` | **None.** No proxy is substituted for an inadmissible source. The retained columns are two of the three columns the Phase 4bn-AY contract already froze — not a substitute family introduced to stand in for something unavailable. |
| Phase 4ak twelve-clause M0 gate, §6 cooldown, §7 cooled-down families | **No cooled-down family is reopened.** CF-1 is a non-strategy, non-directional substrate mechanism test that does not clear M0 for any strategy; `research_eligible = false` and `eligibility_gate_status = pending` are preserved. |
| Phase 4bn-AE §19 M0 boundary | Preserved and unweakened; this phase authorizes no M0 mapping and no strategy. |
| `PRE_V002_INTERNAL_HOLDOUT = CONSUMED` | Preserved; the holdout is not relabelled into a fresh evaluation or confirmation set and remains unopened and descriptive-only. |
| `V002_TERMINAL_WINDOW`, `V002_SEALED_TEST = UNTOUCHED_RESERVED` | Preserved, excluded, and unopened. |

**No stopped arc is softened, merged, reinterpreted, reopened, or rescued by this audit.**

## 16. Final selected set

```
CORRECTED_CF1_FEATURE_SET  = { rolling_aggtrade_count_60s , rolling_quantity_sum_60s }
CORRECTED_CF1_FEATURE_COUNT = 2
FEATURE_WINDOW              = 60s, (T − 60_000 ms, T], trailing_right_open_left
TRANSFORM                   = natural logarithm, then train-only z-score (σ floor 1e-8)
AUGMENTED_PARAMETER_COUNT   = 6      (1 intercept + 3 HAR + 2 microstructure)
EXPECTED_STRUCTURAL_RANK    = 6      (absence of a source-implied exact dependency;
                                      NOT a guarantee of full numerical rank on any dataset;
                                      runtime rank / zero-variance / condition-number /
                                      non-finite guards remain the final arbiter)
MIN_TRAINING_ORIGINS        = 60     (10 × 6)
REMOVED                     = rolling_quantity_mean_60s  (deterministically derived,
                                      floor-quantized, nullable)
PROHIBITED                  = the Phase 4bn-AY three-feature set,
                              STRUCTURALLY_NON_IDENTIFIABLE__PROHIBITED_FOR_FUTURE_EXECUTION
                              (operational meaning per §6)
```

**Why this pair, restated from source only:** `rolling_aggtrade_count_60s` and
`rolling_quantity_sum_60s` are the two primitive committed accumulators; neither is deterministically
defined from the other; both are non-null by construction; both avoid the mean column's floor
quantization; and together they preserve the explicitly preregistered arrival-intensity and
unsigned-volume-intensity mechanism channels. Removing the derived mean is the minimum contract
change that removes the source-defined numerical redundancy Phase 4bn-AZ demonstrated. No observed
scientific outcome selected the pair, because Phase 4bn-AZ produced no scientific metric.

**Estimability and anti-duplication audit result: PASSED.**

## 17. Proof that no data was opened

- Only committed documents, committed source files, committed schema/compute policy constants, Git
  metadata, and static symbolic reasoning were used. The complete list of source files read is §1.
- `data/microstructure/` and `data/research/` were **not** opened, listed for content, hashed,
  sampled, parsed, or inspected. No Parquet, JSON artefact, `.sha256` sidecar content, or Phase
  4bn-AZ local output was opened.
- No target row, feature row, label row, model output, or diagnostic output was read.
- No correlation, condition number, rank, residual, coefficient, QLIKE value, bootstrap replicate,
  or any other numerical quantity was computed on data. The algebraic residual of the Phase 4bn-AZ
  identity was **not** recomputed; the Phase 4bn-AZ committed report is cited as sufficient evidence.
- No model was fitted, no target or feature was generated, no synthetic proof was run, no bootstrap
  was run.
- No test, linter, type-checker, builder, or script was executed: this phase changes no executable
  surface.
- No network, web, API, Binance endpoint, credential, `.env`, MCP, Graphify, or `.mcp.json` access
  occurred; no data was acquired.
- No PnL, backtest, replay, paper, shadow, live, or exchange operation was run.

`No market data, target row, feature row, model output, diagnostic output, or local Phase 4bn-AZ artefact was opened or read by Phase 4bn-BA.`

`The v002 terminal window and v002 sealed test remain untouched and excluded.`

`The consumed pre-v002 internal holdout and the 2024-11-01 through 2024-11-15 buffer remain unopened.`

`No evidence reserve is authorized for spending by Phase 4bn-BA.`
