# Phase 4bn-BA — Closeout

## 1. Phase name

Phase 4bn-BA — CF-1 Feature-Contract Correction and Re-Preregistration. A **docs-only, no-data,
no-model, no-metric, no-rerun, no-reserve, no-PnL, no-backtest, no-strategy, no-paper/shadow/live,
no-exchange/API** scientific-contract correction phase following the merged Phase 4bn-AZ
`CF1_INVALID_RUN`. Tier 1 / Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md`.

## 2. Branch and base

Branch: `phase-4bn-ba/cf1-feature-contract-correction-repreregistration`.

| Item | SHA |
|---|---|
| Base `main` == `origin/main` at branch creation and at completion | `021e4fc12e2e541aaefd54f562ff9d1a9c9cff52` |
| Phase 4bn-AZ no-fast-forward merge commit | `8e82e185a0def318acd2ec42fcb73337edc67b51` |
| Phase 4bn-AZ evidence-bearing implementation SHA | `05fa63a8bf8c9b1fe386cc4ab67805046ae418b1` |
| Phase 4bn-AY final scientific-contract tip | `0fb560656aa9b50cf110602e15be8222b7343623` |

## 3. Commit history and SHA self-reference convention

| # | SHA | Message | Role |
|---|---|---|---|
| 1 | `af1dbf6725fd31eaf82db9070195750afd172241` | `docs(phase-4bn-ba): correct and repreregister CF-1 feature contract` | `BA_DECISION_COMMIT_SHA`. Initial Decision A memo, the estimability and anti-duplication audit, and the corrected execution-validation checklist |
| 2 | `2fafdd48f435bc3c07e7fbf6e10ebb578a3ec12b` | `docs(phase-4bn-ba): add closeout` | Initial closeout |
| 3 | `f1384a5b61739861790c92537e3af606c38ad213` | `docs(phase-4bn-ba): correct finite-precision feature characterization` | Corrected exact-identity, rank, span, pair-equivalence, relative-error, and valid-origin characterizations across all four BA documents (see §17, Amendment 3) |
| 4 | `97e1d1e65ecff654fcd5e3b7f43e023f64149c33` | `docs(phase-4bn-ba): finalize quotient wording and preflight routing` | Corrected two residual quotient phrases, qualified the Phase 4bn-AZ historical shorthand, and routed a failed pre-data timestamp proof to `PREFLIGHT_FAILURE` (see §17, Amendment 4) |
| 5 | *this commit* | `docs(phase-4bn-ba): synchronize closeout with final corrections` | `FINAL_PHASE_SHA`. Final closeout synchronization; metadata and closeout history only (see §17, Amendment 5). A commit cannot embed its own SHA; per the established convention its exact SHA is recorded in the final operator report and in the Git log after commit |

## 4. Exact files added

Exactly four files added; **no existing file modified, deleted, or renamed.**

```
A  docs/00-meta/implementation-reports/2026-07-20_phase-4bn-ba_cf1-feature-contract-correction-and-repreregistration.md
A  docs/00-meta/implementation-reports/2026-07-20_phase-4bn-ba_cf1-estimability-and-anti-duplication-audit.md
A  docs/00-meta/implementation-reports/2026-07-20_phase-4bn-ba_cf1-corrected-execution-validation-checklist.md
A  docs/00-meta/implementation-reports/2026-07-20_phase-4bn-ba_closeout.md
```

No Phase 4bn-AY document, Phase 4bn-AZ document, source module, test, script, schema, README,
`current-project-state.md`, process standard, manifest, ledger, phase gate, or technical-debt
register was modified. No executable surface changed.

## 5. Exact decision

```
SELECT_CORRECTED_CF1_FEATURE_CONTRACT_FOR_SEPARATE_FUTURE_EXECUTION
```

**Decision A.** Exactly one corrected feature specification was selected and fully re-preregistered.

## 6. Exact result state

```
CF1_CORRECTED_FEATURE_CONTRACT_REPREREGISTERED__ORIGINAL_AZ_INVALID_RUN_PRESERVED__ESTIMABILITY_AND_ANTI_DUPLICATION_AUDIT_PASSED__NO_DATA_OPENED__NO_EXECUTION_AUTHORIZED__RESERVES_UNTOUCHED
```

## 7. Exact selected corrected feature contract

```
CORRECTED_CF1_FEATURE_SET   = { rolling_aggtrade_count_60s , rolling_quantity_sum_60s }
CORRECTED_CF1_FEATURE_COUNT = 2
FEATURE_WINDOW              = 60s, (t_last − 60_000 ms, t_last], trailing_right_open_left
SNAPSHOT_RULE               = last feature row with feature_timestamp_ms ≤ t, row_index_le_R tie
TRANSFORM                   = natural logarithm, then train-only z-score, σ floor 1e-8
AUGMENTED_EQUATION          = y = β0 + β1·ln(RV_h+ε) + β2·ln(RV_d+ε) + β3·ln(RV_w+ε)
                                    + γ1·z1 + γ2·z2 + u
AUGMENTED_PARAMETER_COUNT   = 6      (1 intercept + 3 HAR + 2 microstructure)
EXPECTED_STRUCTURAL_RANK    = 6      (absence of a source-implied exact dependency; NOT a
                                      guarantee of full numerical rank on any dataset; the
                                      runtime rank / zero-variance / condition-number /
                                      non-finite guards remain the final arbiter)
MIN_TRAINING_ORIGINS        = 60     (10 × 6, the inherited 10 × parameters rule)
MIN_BLOCK_VALID_ORIGINS     = 100    (unchanged)
REMOVED                     = rolling_quantity_mean_60s
```

The Phase 4bn-AY three-feature set is deterministically redundant at the source-definition level and
numerically non-identifiable under the frozen runtime guard after serialization and logarithmic
transformation. It remains marked:

```
STRUCTURALLY_NON_IDENTIFIABLE__PROHIBITED_FOR_FUTURE_EXECUTION
```

**Operational meaning of that label:** a source-defined derived feature whose stored transformed
column produced **effective rank deficiency / catastrophic conditioning under the frozen guard**. It
does **not** assert an exact symbolic rank theorem for every possible serialized dataset.

**The defect corrected.** `rolling_quantity_mean_60s` is produced by the committed **fixed-point
floor quantizer** `mean_int = (sum_int × 10^12) // count`, serialized at the quantity scale plus
twelve decimals. Writing `x3*` for the ideal quotient `x2/x1` and `x3` for the stored column:

```
x3     = x3* − q ,   q ≥ 0 ,  q < one stored least-significant decimal unit,
                     q = 0 only when the quotient is exactly representable at that precision
ln(x3) = ln(x2) − ln(x1) + δ ,   δ ≤ 0 ,  δ = 0 only when q = 0 ,  δ generally nonzero
```

So the ideal identity `ln(x3*) = ln(x2) − ln(x1)` is exact, while the **stored** column is **not
guaranteed** to be an exact affine combination of `ln(x1)` and `ln(x2)`. What *is* established from
source is that `x3` is deterministically derived from `x1` and `x2`, carries **no independent
information**, and after the logarithm is numerically almost collinear with `ln(x2) − ln(x1)`. Phase
4bn-AZ recorded `max|δ| = 3.33e-14` and `mean|δ| = 3.51e-15` on its frozen target layer —
near-machine-precision transformed dependence, cited and **not recomputed** — with augmented
condition numbers ≈ 1e16 exceeding the frozen `> 1e10` guard in all seven blocks. No universal
relative-error bound is asserted, because none is provable from source over the full valid domain.

**Mechanism coverage.** The ideal arithmetic mean-size contrast is `ln(x2) − ln(x1)`, and the
committed stored mean is a floor-quantized approximation to it. Retaining the two primitive
regressors preserves the intended count and volume primitives and allows the estimator to represent
the ideal mean-size contrast, **without carrying the separately quantized derived column**. No claim
is made that the corrected design exactly reproduces every fitted value of the stored three-feature
design.

**Why this pair (source-only).** `rolling_aggtrade_count_60s` and `rolling_quantity_sum_60s` are the
two primitive committed accumulators; neither is deterministically defined from the other; both are
non-null by construction; both avoid the mean column's floor quantization; and together they preserve
the explicitly preregistered arrival-intensity and unsigned-volume-intensity channels. Removing the
derived mean is the minimum contract change that removes the source-defined numerical redundancy
Phase 4bn-AZ demonstrated. No observed scientific outcome selected the pair, because Phase 4bn-AZ
produced no scientific metric.

The corrected contract contains **no alternate candidate menu, no secondary feature set, no fallback
feature, no "choose later", no conditional drop, no post-data repair logic, no regularization rescue,
no relaxed condition threshold, and no post-hoc ablation path.**

## 8. Exact inherited fields

Every Phase 4bn-AY contract field is inherited unchanged except the feature set and its directly
dependent fields: target family and realized-variance construction; interval semantics `(a, b]`;
`P_at(u)` with `≤ u` and the greatest-`row_index` tie; horizon `H = 60 min`; hourly non-overlapping
cadence; source; development dates (244 UTC dates, 2024-03-01..2024-10-31 excluding 2024-10-01);
the seven evaluation blocks with B7 beginning 2024-10-02; the one-day embargo and one-hour purge;
the HAR-style OLS baseline; the deterministic OLS estimator class; QLIKE with `v = RV + 1e-16` and
`h = max(exp(ŷ), 1e-16)`; equal block weighting; the stratified moving-block bootstrap with
`B = 10,000`, `RNG_SEED = 20260715`, block-specific `ℓ_i`; the P1/P2/P3 pass rule; the fail rule; the
invalid-run rule; the reserve boundary; the anti-tuning rules; the consequence rules; the §33
output-artefact contract including both pre-metric proofs; the §34 provenance fields and the eight
non-authorization flags; and the §35 prohibited-deviation list.

Superseded, for any future corrected experiment only: the feature names; the feature count (3 → 2);
the transformed regressor list (`z1,z2,z3` → `z1,z2`); the augmented equation; the augmented
parameter count (7 → 6); the minimum training-origin count (70 → 60, the `10 × parameters` rule
itself unchanged); the missing-feature validity predicate (restated as `count ≥ 1` and
`quantity_sum > 0`, which excludes every origin the Phase 4bn-AY predicate excluded on those grounds
and is equal to or a superset of the Phase 4bn-AY set, since the corrected contract never forms the
floor-quantized mean); the manifest and checklist feature lists; and the target-layer and manifest
output columns.

Phase 4bn-AY remains historical and merged. Phase 4bn-AZ remains an invalid run. **No past document,
run, metric, or verdict is rewritten.**

## 9. Historical interpretation preserved

`Phase 4bn-AZ remains CF1_INVALID_RUN and is not reclassified, repaired, rerun, or interpreted as a scientific pass or fail.`

`The one authorized Phase 4bn-AZ evidence-bearing run remains consumed.`

`No Phase 4bn-AZ metric is used to select the corrected feature contract because no scientific metric was computed.`

`The correction is based only on committed feature definitions, symbolic estimability, mechanism coherence, and anti-duplication constraints.`

`Phase 4bn-AZ produced CF1_INVALID_RUN, not CF1_VALID_FAIL and not CF1_VALID_PASS.` The run produced
no scientific test of the CF-1 hypothesis; no QLIKE, `d_{i,t}`, `D_i`, `Δ_equal`, `ρ`, MSE,
Mincer–Zarnowitz R², bootstrap distribution, or `LB_95` was computed; P1, P2, and P3 were not
evaluable, and any recorded `false` or zero placeholder is **not** a negative scientific finding; the
Phase 4bn-AY valid-fail consequence does **not** apply; and the aggTrades magnitude lane was **not**
narrowed by Phase 4bn-AZ. **The CF-1 hypothesis remains scientifically untested.**

## 10. No data, no local artefact access, no execution

`No market data, target row, feature row, model output, diagnostic output, or local Phase 4bn-AZ artefact was opened or read by Phase 4bn-BA.`

`No QLIKE, bootstrap, model fitting, target generation, feature generation, diagnostic, backtest, PnL analysis, data acquisition, paper, shadow, live, or exchange-write execution is authorized by Phase 4bn-BA.`

Evidence was limited to committed documents, committed source (`features_schema.py`,
`features_schema_v002.py`, `features_compute.py`), committed schema and compute policy constants,
committed process standards, Git metadata, and static symbolic reasoning. `data/microstructure/` and
`data/research/` were not opened or listed for content. No Parquet, JSON artefact, or `.sha256`
sidecar content was opened. The Phase 4bn-AZ algebraic residual was **not** recomputed; the committed
Phase 4bn-AZ report is sufficient evidence. No correlation, condition number, rank, or residual was
computed. No test, linter, type-checker, builder, or script was run — this phase changes no
executable surface. No network, web, API, Binance endpoint, credential, `.env`, MCP, Graphify, or
`.mcp.json` access occurred.

## 11. No reserve

`No evidence reserve is authorized for spending by Phase 4bn-BA.` No evidence reserve was opened or
spent, and no evidence-ledger status transition occurred.

`The v002 terminal window and v002 sealed test remain untouched and excluded.`

`The consumed pre-v002 internal holdout and the 2024-11-01 through 2024-11-15 buffer remain unopened.`

Restated and unchanged: `PRE_V002_INTERNAL_HOLDOUT = CONSUMED`;
`V002_TERMINAL_WINDOW = UNTOUCHED_RESERVED`; `V002_SEALED_TEST = UNTOUCHED_RESERVED`;
`HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE`; `test_rows_loaded = 0`;
`v002_terminal_window_read = false`; `sealed_test_split_touched = false`;
`consumed_holdout_opened = false`; `november_buffer_opened = false`.

## 12. No PnL, no trading

No signal generation, strategy, PnL analysis, backtest, replay, paper, shadow, live, or
exchange-write execution was performed or is authorized. CF-1 is a non-directional
realized-variance magnitude contract; it produces no directional object and no tradable object.
`network_used = false`; `data_acquisition_used = false`; and all eight non-authorization flags
(`ml_authorized`, `diagnostics_authorized`, `strategy_authorized`, `signals_authorized`,
`pnl_authorized`, `backtest_authorized`, `live_authorized`, `exchange_write_authorized`) remain
`false`. This phase does not clear M0 for any strategy.

## 13. Preserved locks

Preserved exactly and unchanged: `STOP_LONGHORIZON_ML_ARC`;
`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`; `REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`;
`PRE_V002_INTERNAL_HOLDOUT = CONSUMED`; `V002_TERMINAL_WINDOW = UNTOUCHED_RESERVED`;
`V002_SEALED_TEST = UNTOUCHED_RESERVED`; `HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE`;
`test_rows_loaded = 0`; `research_eligible = false`; `eligibility_gate_status = pending`; all
authorization flags false; the Phase 4aw always-raising `flip_research_eligible(...)` flip, never
invoked; Phase 4bn-AE §19; the Phase 4ak twelve-clause M0 gate with its §6 cooldown rule and §7
cooled-down-families list; the cooldown and cooled-down-family rules; the 8 bps/side · 16 bps
round-trip cost lock; every prior verdict; every dataset identity and hash; every
split/holdout/sidecar/storage policy; and the evidence-ledger and spending-authority rules.

**No stopped arc is softened, merged, reinterpreted, reopened, or rescued.** The corrected contract
overlaps no stopped family: it reads no long-horizon label, no top-of-book or bookTicker source, and
substitutes no proxy for an inadmissible source — it retains two of the three columns the Phase
4bn-AY contract already froze.

## 14. Preserved locks — working tree

`.claude/scheduled_tasks.lock` was the only untracked item at branch creation and at completion. It
was never staged, modified, deleted, cleaned, or committed.

## 15. Merge non-authorization

**No merge is performed or authorized by this phase.** No merge-closeout is created. Merging Phase
4bn-BA into `main` requires a **separate operator prompt and decision**. `main` and `origin/main`
remain exactly `021e4fc12e2e541aaefd54f562ff9d1a9c9cff52`; no `main` push and no SHA-finalization
commit were performed. Phase 4bn-BA is **branch-complete, not project-complete**.

## 16. Successor non-authorization

**No successor phase is authorized by this closeout.**

A future corrected CF-1 execution would be a **new experiment** under the Phase 4bn-BA contract — not
a Phase 4bn-AZ rerun, continuation, correction-in-place, reuse of the consumed run, or
reclassification.

Proposed future title, **proposed only**:

```
Phase 4bn-BB — Corrected CF-1 Realized-Volatility Substrate-Test Execution
```

`Phase 4bn-BB or any future corrected execution requires separate operator authorization and a new Claude Code prompt.`

`The corrected feature contract is frozen before any new execution and contains no fallback, ablation, or post-data feature-selection path.`

No data read is authorized. No synthetic proof is run. No implementation is written. No model is
fitted. No metric is computed.

## 17. Amendment history

| # | Commit | Change |
|---|---|---|
| 1 | `af1dbf6725fd31eaf82db9070195750afd172241` | Initial Phase 4bn-BA decision memo, estimability and anti-duplication audit, and corrected execution-validation checklist |
| 2 | `2fafdd48f435bc3c07e7fbf6e10ebb578a3ec12b` | Initial Phase 4bn-BA closeout |
| 3 | `f1384a5b61739861790c92537e3af606c38ad213` — `docs(phase-4bn-ba): correct finite-precision feature characterization` | **Narrow mathematical-precision correction** applied consistently across all four Phase 4bn-BA documents |
| 4 | `97e1d1e65ecff654fcd5e3b7f43e023f64149c33` — `docs(phase-4bn-ba): finalize quotient wording and preflight routing` | **Residual-wording and pre-data routing correction** across the three non-closeout BA documents |
| 5 | *this commit* — `docs(phase-4bn-ba): synchronize closeout with final corrections` | **Closeout synchronization**; metadata and closeout history only. Records amendments 3 and 4 accurately; changes no scientific or execution-bearing field; preserves merge and Phase 4bn-BB non-authorization |

**Scope of amendment 3.** The committed mean formatter is a fixed-point **floor quantizer**
(`mean_int = (sum_int × 10^12) // count`), so the stored `rolling_quantity_mean_60s` is a
deterministic floor-quantized approximation to `rolling_quantity_sum_60s /
rolling_aggtrade_count_60s`, not the exact quotient at the serialized stored-value level. The
original Phase 4bn-BA documents overstated this as a universal exact identity and built several
exact theorems on it. Amendment 3 replaces those overstatements with the precise characterization:
an exact **ideal** identity `ln(x3*) = ln(x2) − ln(x1)`; a **stored** relation
`ln(x3) = ln(x2) − ln(x1) + δ` with `δ ≤ 0` and generally nonzero; and Phase 4bn-AZ's recorded
near-machine-precision residual plus its demonstrated conditioning failure as **empirical evidence**
of effective, not exact, dependence.

Specifically removed as live claims: the exact stored quotient; the exact stored logarithmic
identity; the exact null vector for the stored transformed columns; the exact rank-2 stored
transformed block; the exact column-space equality of all three admissible pairs; the claim of
identical fitted values and identical decision statistics for all three pairs on every dataset; the
claim that data could not distinguish the pairs in principle; the exact span-preservation theorem
and exact zero-mechanism-loss claim; the inevitable exact structural rank 6 of the seven-column
stored design; the invented `≤ 1e-12` universal relative-error bound; and the claim that the
corrected valid-origin set is provably identical to the Phase 4bn-AY set (it is equal to or a
superset).

**What amendment 3 did not change.**

- Decision A is **unchanged**: `SELECT_CORRECTED_CF1_FEATURE_CONTRACT_FOR_SEPARATE_FUTURE_EXECUTION`.
- The selected corrected pair is **unchanged**:
  `{ rolling_aggtrade_count_60s , rolling_quantity_sum_60s }`, feature count 2.
- The removed column is **unchanged**: `rolling_quantity_mean_60s`.
- `AUGMENTED_PARAMETER_COUNT = 6`, `MIN_TRAINING_ORIGINS = 60`, `MIN_BLOCK_VALID_ORIGINS = 100`, the
  `> 1e10` condition-number guard, the rank / zero-variance / non-finite guards, the 60s window, the
  snapshot rule, the transform, the standardization rule, and every inherited Phase 4bn-AY field are
  **unchanged**.
- The Phase 4bn-BA result state is **unchanged**, and no new result state was created.
- `STRUCTURALLY_NON_IDENTIFIABLE__PROHIBITED_FOR_FUTURE_EXECUTION` is **retained**, now with an
  explicit operational definition (§7).
- **No scientific or execution-bearing field changed** except the characterization of the removed
  stored mean feature and the justification wording supporting its removal.
- No data was opened, no local artefact was inspected, no residual was recomputed, no test, linter,
  or script was run, and no execution occurred.
- Merge remains **unauthorized**; Phase 4bn-BB remains **unauthorized**.

**Scope of amendment 4** (`97e1d1e65ecff654fcd5e3b7f43e023f64149c33`,
`docs(phase-4bn-ba): finalize quotient wording and preflight routing`). Applied to the three
non-closeout BA documents:

- replaced the two remaining phrases that still described the stored mean as the **exact** or
  **precise** quotient with the deterministically-derived, floor-quantized characterization,
  distinguished from the ideal arithmetic quotient `x3* = x2 / x1`, which alone carries an exact
  identity;
- **qualified the historical Phase 4bn-AZ exact-identity sentence** as historical shorthand whose
  mathematical interpretation is superseded by the ideal-versus-stored finite-precision relation
  `ln(x3) = ln(x2) − ln(x1) + δ` (`δ ≤ 0`, generally nonzero); the `CF1_INVALID_RUN` classification,
  the recorded residual statistics, the recorded condition numbers, and the no-scientific-claim
  consequence remain unchanged and binding;
- corrected gate 1.4.9 and execution-order step 4 of the corrected execution-validation checklist so
  a **failed or absent pre-data deterministic synthetic timestamp-boundary proof routes to
  `PREFLIGHT_FAILURE`** (stop; no market data opened; no scientific result), not `CF1_INVALID_RUN`;
- clarified that `PREFLIGHT_FAILURE` is a **pre-execution gate result, not a fourth scientific
  outcome**, that no market data is opened and no scientific result is produced, and that
  **post-access violations continue to route to `CF1_INVALID_RUN`**;
- added the anti-switching clarification that opening market data after skipping or weakening a proof
  is a post-access violation (`CF1_INVALID_RUN`), while stopping before any market-data read after a
  proof failure is `PREFLIGHT_FAILURE`;
- **preserved** Decision A, the selected pair, the removed column, feature count 2, augmented
  parameter count 6, the training minimum 60, the block minimum 100, the expected-structural-rank
  scope, the result state, the Phase 4bn-AZ verdict and consumed-run status, and every runtime guard.

**Scope of amendment 5** (this commit,
`docs(phase-4bn-ba): synchronize closeout with final corrections`). Metadata and closeout history
only:

- records the complete five-entry Phase 4bn-BA commit history by exact SHA, replacing the earlier
  `this commit` placeholder for `f1384a5b61739861790c92537e3af606c38ad213` with its actual SHA;
- records amendments 3 and 4 accurately, and records the pre-data proof routing correction (below);
- **changes no scientific or execution-bearing field**, opens no data, inspects no local artefact,
  recomputes no residual, runs no test/linter/script/proof/model/metric, and performs no execution;
- preserves the Phase 4bn-BA result state, all inherited fields, all locks, merge non-authorization,
  and Phase 4bn-BB non-authorization.

### Execution-routing record (the only execution-bearing clarification since the initial closeout)

The Phase 4bn-BA corrected execution-validation checklist now distinguishes pre-data gate failure
from post-access invalidation. A failed or absent deterministic synthetic timestamp-boundary proof
before any market-data read is `PREFLIGHT_FAILURE`: no market data is opened, no evidence is
consumed, and no scientific result exists. A contract violation after market-data access is
`CF1_INVALID_RUN`. `PREFLIGHT_FAILURE` is not a fourth scientific outcome.

This is a **routing consistency correction, not a relaxation.** The three scientific execution
outcomes are unchanged and remain `CF1_VALID_PASS`, `CF1_VALID_FAIL`, and `CF1_INVALID_RUN`. The
checklist authorizes nothing.

**The only execution-bearing clarification after the initial closeout was the routing of a failed or
absent pre-data deterministic synthetic timestamp-boundary proof to `PREFLIGHT_FAILURE` rather than
`CF1_INVALID_RUN`. No model, metric, data, feature, target, split, guard, or scientific decision
field changed.** (The amendment-3 characterization of the removed stored-mean feature was a wording
and mathematical-interpretation correction, not a change to any execution-bearing field.)

### What amendments 3, 4, and 5 did not change (cumulative)

None of amendments 3, 4, or 5 changed: Decision A
(`SELECT_CORRECTED_CF1_FEATURE_CONTRACT_FOR_SEPARATE_FUTURE_EXECUTION`); the selected pair
`{ rolling_aggtrade_count_60s , rolling_quantity_sum_60s }`; the removal and prohibition of
`rolling_quantity_mean_60s`; feature count 2; augmented parameter count 6; minimum training origins
60; minimum block valid origins 100; the expected-structural-rank scope (absence of a source-implied
exact dependency only); the runtime rank guard; the zero-variance guard; the non-finite guard; the
condition-number threshold `> 1e10`; the target; the interval semantics; the horizon; the cadence;
the split; the embargo; the purge; the HAR baseline; the OLS estimator; QLIKE; equal block
weighting; the bootstrap; the pass/fail/invalid routing; the reserve boundaries; the stopped arcs;
the Phase 4bn-AZ historical verdict; the Phase 4bn-AZ consumed-run status; the Phase 4bn-BA result
state; merge non-authorization; or Phase 4bn-BB non-authorization.

## 18. Recommended next operator action

1. Review the four Phase 4bn-BA documents on the branch — in particular the symbolic estimability
   and anti-duplication audit, and the corrected feature contract §10 of the main memo.
2. Decide whether to authorize a **separate merge phase** for Phase 4bn-BA.
3. Independently, and only after a merge decision, decide whether to authorize
   `Phase 4bn-BB — Corrected CF-1 Realized-Volatility Substrate-Test Execution`. It is not
   authorized here and requires a new operator authorization and a new Claude Code prompt.
4. Return the corrected four Phase 4bn-BA documents and the final operator report for final merge
   review and a separate Phase 4bn-BA merge prompt.
5. `Remaining paused is a valid operator choice.`

Recommended state: **paused**, pending operator review and a separate merge decision.
