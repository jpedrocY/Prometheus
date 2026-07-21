# Phase 4bn-BA — Merge Closeout

## 1. Phase identity

Phase 4bn-BA — CF-1 Feature-Contract Correction and Re-Preregistration. A **docs-only** scientific
contract-correction phase following the merged Phase 4bn-AZ `CF1_INVALID_RUN`. It identifies the
algebraic defect in the merged Phase 4bn-AY feature contract, audits the committed feature schema,
selects and fully re-preregisters one corrected feature specification (Decision A), and freezes every
directly dependent execution-bearing field — with no data read and no execution.

- **Source branch:** `phase-4bn-ba/cf1-feature-contract-correction-repreregistration`
- **Target branch:** `main`

## 2. Phase type and risk tier

Docs-only, no-data, no-model, no-metric, no-rerun, no-reserve, no-PnL, no-backtest, no-strategy,
no-paper/shadow/live, no-exchange/API contract-correction phase. **Tier 1 / Full Phase** per
`docs/00-meta/process/phase-risk-tiering-standard.md` — it re-preregisters a merged scientific
contract, so it carries the highest ceremony tier even though its surface is Markdown only and it
mutates no data, manifest, eligibility state, verdict, reserve, or lock.

**This merge is a recordkeeping action only.** It changes no data, no manifest, no eligibility state,
no verdict, no reserve, and no lock. It authorizes no execution.

`Merging Phase 4bn-BA records the corrected preregistration and its governance controls; it does not authorize Phase 4bn-BB or any corrected execution.`

## 3. Source and target branches

- **Source:** `phase-4bn-ba/cf1-feature-contract-correction-repreregistration`
- **Target:** `main`

## 4. Pre-merge `main` / base SHA

`021e4fc12e2e541aaefd54f562ff9d1a9c9cff52` (`HEAD == main == origin/main` at merge time; the tip
after the Phase 4bn-AZ merge-closeout SHA-finalization commit). Verified in sync before any mutation.
The only untracked item was the transient `.claude/scheduled_tasks.lock`, which was not staged,
modified, deleted, cleaned, or committed.

## 5. Complete Phase 4bn-BA source-branch commit history

Five commits on the source branch after the base, preserved exactly — not squashed, reordered,
rebased, amended, or rewritten:

| # | SHA | Commit message | Role |
|---|---|---|---|
| 1 | `af1dbf6725fd31eaf82db9070195750afd172241` | `docs(phase-4bn-ba): correct and repreregister CF-1 feature contract` | Initial corrected preregistration: adds the main decision memo, the estimability and anti-duplication audit, and the corrected future execution-validation checklist. |
| 2 | `2fafdd48f435bc3c07e7fbf6e10ebb578a3ec12b` | `docs(phase-4bn-ba): add closeout` | Adds the initial Phase 4bn-BA closeout. |
| 3 | `f1384a5b61739861790c92537e3af606c38ad213` | `docs(phase-4bn-ba): correct finite-precision feature characterization` | Distinguishes the ideal arithmetic mean from the stored floor-quantized mean; removes universal exact stored-identity, rank, span, pair-equivalence, and relative-error claims; corrects the valid-origin wording to *equal to or a superset*. |
| 4 | `97e1d1e65ecff654fcd5e3b7f43e023f64149c33` | `docs(phase-4bn-ba): finalize quotient wording and preflight routing` | Corrects the final two residual quotient phrases; qualifies the Phase 4bn-AZ identity as historical shorthand; routes a failed or absent pre-data synthetic timestamp proof to `PREFLIGHT_FAILURE`. |
| 5 | `adc06e68cf532e00b0477d0cefca9d97d2287449` | `docs(phase-4bn-ba): synchronize closeout with final corrections` | Records the completed four-commit history and amendments and the pre-data/post-access routing boundary; metadata and closeout history only. Final BA branch tip before merge-closeout creation. |

This merge-closeout is the **sixth** commit on the source branch.

## 6. Final pre-merge Phase 4bn-BA branch-tip SHA

`adc06e68cf532e00b0477d0cefca9d97d2287449` — the approved Phase 4bn-BA contract-correction state at
merge time.

## 7. Merge-closeout branch commit SHA

`ba6ddf12dfa97a2f4ef04abf2bd35127c7f04274` — the commit on the BA branch that adds this
merge-closeout file (`docs(phase-4bn-ba): add merge closeout`). This is the **sixth** commit on the
source branch.

## 8. No-fast-forward merge commit SHA

`7096ce853dd85dfe6bd95ae88942548bc76400dd` — the commit created by `git merge --no-ff` on `main`
(`docs(phase-4bn-ba): merge corrected CF-1 feature contract`).

## 9. SHA-finalization convention

This merge-closeout was created on the BA source branch with the §7 and §8 SHAs as placeholders.
After the `--no-ff` merge into `main`, this single narrow SHA-finalization commit on `main`
(`docs(phase-4bn-ba): finalize merge closeout shas`) replaces those placeholders with the actual
merge-closeout branch commit SHA (`ba6ddf12dfa97a2f4ef04abf2bd35127c7f04274`, §7) and the actual
`--no-ff` merge commit SHA (`7096ce853dd85dfe6bd95ae88942548bc76400dd`, §8).

**SHA-finalization commit SHA:** this update (`docs(phase-4bn-ba): finalize merge closeout shas`). A
commit cannot embed its own SHA; the SHA-finalization commit's own SHA equals the resulting final
`main` / `origin/main` tip and is recorded in the final operator report and the Git log after commit.

## 10. Final `main` / `origin/main` statement

After the SHA-finalization push, `HEAD == main == origin/main`, and that tip is the canonical
"project is now at this SHA" marker for Phase 4bn-BA. Pre-merge `main` was
`021e4fc12e2e541aaefd54f562ff9d1a9c9cff52`; `main` advances only by the `--no-ff` merge commit and
the one SHA-finalization commit.

## 11. Merge method

- `git merge --no-ff` with the default `ort` strategy.
- Merge commit message: `docs(phase-4bn-ba): merge corrected CF-1 feature contract`.
- Pushed to `origin/main` with **no force, no skip-hooks, no skip-signing**.

## 12. Files brought forward by the merge

**Docs (five added files; additions only):**

- `docs/00-meta/implementation-reports/2026-07-20_phase-4bn-ba_cf1-feature-contract-correction-and-repreregistration.md`
- `docs/00-meta/implementation-reports/2026-07-20_phase-4bn-ba_cf1-estimability-and-anti-duplication-audit.md`
- `docs/00-meta/implementation-reports/2026-07-20_phase-4bn-ba_cf1-corrected-execution-validation-checklist.md`
- `docs/00-meta/implementation-reports/2026-07-20_phase-4bn-ba_closeout.md`
- `docs/00-meta/implementation-reports/2026-07-21_phase-4bn-ba_merge-closeout.md` (this file)

**Source:** none. **Tests:** none. **Scripts:** none. **Config:** none. **No `data/microstructure/`
file was modified.** No Phase 4bn-AY or Phase 4bn-AZ document was modified. No manifest, ledger,
process standard, README, `current-project-state.md`, phase gate, or technical-debt register was
modified.

## 13. Additions-only confirmation

Relative to the pre-merge `main` SHA `021e4fc12e2e541aaefd54f562ff9d1a9c9cff52`, the merged change
set is **additions only**: five added files, and no modification, deletion, or rename of any
pre-existing path. The one later modification of this merge-closeout is the narrow SHA-finalization
update described in §9.

## 14. Diff summary

`git diff --stat 021e4fc12e2e541aaefd54f562ff9d1a9c9cff52..<merge>` (five added BA documents; the
merge-closeout line reflects the placeholder state before SHA finalization):

```text
 docs/00-meta/implementation-reports/2026-07-20_phase-4bn-ba_cf1-corrected-execution-validation-checklist.md   | 245 +++
 docs/00-meta/implementation-reports/2026-07-20_phase-4bn-ba_cf1-estimability-and-anti-duplication-audit.md     | 555 +++++++
 docs/00-meta/implementation-reports/2026-07-20_phase-4bn-ba_cf1-feature-contract-correction-and-repreregistration.md | 719 ++++++++++
 docs/00-meta/implementation-reports/2026-07-20_phase-4bn-ba_closeout.md                                        | 397 ++++++
 docs/00-meta/implementation-reports/2026-07-21_phase-4bn-ba_merge-closeout.md                                  | (this file)
```

The diff matches the expected change set from the authorization prompt: exactly the four BA phase
documents plus this merge-closeout, additions only.

## 15. Phase 4bn-AY lineage

Phase 4bn-AY — CF-1 Realized-Volatility Substrate-Test Preregistration. Final scientific-contract tip
`0fb560656aa9b50cf110602e15be8222b7343623`. Phase 4bn-AY remains historical and merged; its documents
are not modified, rewritten, or withdrawn by this phase. Phase 4bn-BA inherits every Phase 4bn-AY
field except the feature-set specification and its directly dependent fields (§19–§20).

## 16. Phase 4bn-AZ lineage

Phase 4bn-AZ — CF-1 Realized-Volatility Substrate-Test Execution. No-fast-forward merge commit
`8e82e185a0def318acd2ec42fcb73337edc67b51`; evidence-bearing implementation SHA
`05fa63a8bf8c9b1fe386cc4ab67805046ae418b1`. Phase 4bn-AZ produced the one authorized evidence-bearing
run and recorded `CF1_INVALID_RUN`. `Phase 4bn-AZ remains CF1_INVALID_RUN, its evidence-bearing run remains consumed, and the CF-1 hypothesis remains scientifically untested.` Its verdict, result state,
reports, and artefacts stand exactly as recorded and are not modified by this phase.

## 17. Exact decision

```
SELECT_CORRECTED_CF1_FEATURE_CONTRACT_FOR_SEPARATE_FUTURE_EXECUTION
```

**Decision A.** Exactly one corrected feature specification was selected and fully re-preregistered.

## 18. Exact corrected feature contract

```
CORRECTED_CF1_FEATURE_SET   = { rolling_aggtrade_count_60s , rolling_quantity_sum_60s }
CORRECTED_CF1_FEATURE_COUNT = 2
FEATURE_WINDOW              = 60s, (t_last − 60_000 ms, t_last], trailing_right_open_left
SNAPSHOT_RULE               = last feature row with feature_timestamp_ms ≤ t, greatest row_index tie
TRANSFORM                   = natural logarithm, then train-only z-score, σ floor 1e-8
AUGMENTED_EQUATION          = y = β0 + β1·ln(RV_h+ε) + β2·ln(RV_d+ε) + β3·ln(RV_w+ε)
                                    + γ1·z1 + γ2·z2 + u
BASELINE_PARAMETER_COUNT    = 4
AUGMENTED_PARAMETER_COUNT   = 6      (1 intercept + 3 HAR + 2 microstructure)
EXPECTED_STRUCTURAL_RANK    = 6      (absence of a source-implied exact dependency only)
MIN_TRAINING_ORIGINS        = 60     (10 × 6, the inherited 10 × parameters rule)
MIN_BLOCK_VALID_ORIGINS     = 100
REMOVED                     = rolling_quantity_mean_60s
```

No third feature, no directional feature, no newly derived feature, no explicit ratio feature, no
interaction, no alternate window. No clipping, no winsorization.

`Phase 4bn-BA selects and freezes rolling_aggtrade_count_60s and rolling_quantity_sum_60s as the corrected CF-1 feature contract.`

`rolling_quantity_mean_60s remains removed and prohibited because it is a deterministic floor-quantized derived feature whose transformed stored column produced catastrophic conditioning under the frozen guard.`

**Valid-origin predicate.** An origin is invalid if `rolling_aggtrade_count_60s < 1`, or
`rolling_quantity_sum_60s ≤ 0`, or either retained feature is null or non-finite. The corrected
valid-origin set is **equal to or a superset of the Phase 4bn-AY valid-origin set**, because the
corrected contract does not form the floor-quantized mean; the two are **not** described as
guaranteed identical.

**Runtime guards (unchanged and unrelaxed):** rank guard, zero-variance guard, non-finite guard,
singularity guard, condition number `> 1e10`, minimum training count, minimum evaluation-block count,
and no rescue after a tripped guard.

`The corrected expected structural rank of six records only the absence of a source-implied exact dependency; runtime rank, zero-variance, non-finite, and condition-number guards remain the final arbiter.`

## 19. Exact superseded fields

Superseded, for any future corrected experiment only: the feature names; the feature count (3 → 2);
the transformed regressor list (`z1,z2,z3` → `z1,z2`); the augmented equation; the augmented
parameter count (7 → 6); the minimum training-origin count (70 → 60, the `10 × parameters` rule
itself unchanged); the missing-feature validity predicate (restated as `count ≥ 1` and
`quantity_sum > 0`, equal to or a superset of the Phase 4bn-AY set); the manifest and checklist
feature lists; and the target-layer and manifest output columns.

## 20. Exact inherited fields

Every Phase 4bn-AY field is inherited unchanged except the feature set and its directly dependent
fields in §19: BTCUSDT last-trade realized variance; `H = 60 minutes`; top-of-UTC-hour origins;
target `(t, t+H]`; all RV intervals `(a, b]`; `P_at(u)` with `source_transact_time_ms ≤ u` and the
greatest-`row_index` tie; the one-minute UTC grid; the exact RV construction; `y = ln(RV + 1e-16)`;
no annualization; the covered-minute predicate; `≥ 30 of 60`; no stitching; zero-RV retention; the
HAR-style OLS baseline; deterministic OLS with no regularization; March warmup; the seven Apr–Oct
evaluation blocks with B7 beginning 2024-10-02; the one-day embargo; the one-hour purge;
training-only preprocessing; QLIKE; equal block weighting; 6-of-7 block consistency; the stratified
moving-block bootstrap with `B = 10,000`, seed `20260715`, and `LB_95 > 0`; the pass/fail/invalid
rules; the evidence and reserve boundaries; the anti-tuning and anti-switching rules; the consequence
rules; the output-artefact and provenance rules; and all non-authorization flags. No field outside
the documented BA supersession set changes.

## 21. Exact finite-precision interpretation

The committed mean formatter is a fixed-point **floor quantizer** (`mean_int = (sum_int × 10^12) //
count`). The Phase 4bn-AZ historical statement
`ln(rolling_quantity_mean_60s) = ln(rolling_quantity_sum_60s) − ln(rolling_aggtrade_count_60s)` is
preserved **only as historical shorthand**. The live mathematical interpretation is:

- `x3* = x2 / x1` is the ideal arithmetic mean;
- `x3` is the committed stored floor-quantized mean;
- `x3 = x3* − q`, with `q ≥ 0`;
- `ln(x3) = ln(x2) − ln(x1) + δ`, `δ ≤ 0`, `δ` generally nonzero;
- **no exact stored-feature identity is claimed;**
- **no universal relative-error bound is claimed.**

Phase 4bn-AZ recorded, without recomputation in Phase 4bn-BA: `max|δ| = 3.33e-14`;
`mean|δ| = 3.51e-15`; augmented condition numbers ≈ 1e16; all seven blocks exceeded the frozen
`> 1e10` guard. The original three-feature set remains
`STRUCTURALLY_NON_IDENTIFIABLE__PROHIBITED_FOR_FUTURE_EXECUTION`, meaning a source-defined derived
feature whose stored transformed column produced effective rank deficiency / catastrophic
conditioning under the frozen guard — **not** a universal exact symbolic-rank theorem for every
possible serialized dataset.

## 22. Estimability and anti-duplication audit result

**PASSED.** The corrected two-feature contract removes the sole source-defined redundancy; no exact
affine dependency is implied by the committed definitions between `ln(x1)` and `ln(x2)`, nor between
the microstructure block and the HAR block; standardization is an invertible column map that
preserves rank and cannot repair near-collinearity; the selection is fixed by committed-source
properties (primitiveness, non-nullability by construction, absence of floor quantization, retention
of both preregistered mechanism channels) and by no observed outcome, because none exists. No stopped
family is reopened or rescued.

`No Phase 4bn-AZ metric is used to select the corrected feature contract because no scientific metric was computed.`

## 23. Exact preflight / post-access routing

The corrected execution-validation checklist distinguishes a pre-data gate failure from a post-access
invalidation:

`A failed or absent mandatory pre-data proof is PREFLIGHT_FAILURE: no market data is opened, no evidence is consumed, and no scientific result exists.`

This covers a failed or absent pre-data symbolic estimability record **and** a failed or absent
deterministic synthetic timestamp-boundary proof.

`A contract violation after market-data access is CF1_INVALID_RUN and supports no scientific claim.`

Opening market data after skipping or weakening a mandatory pre-data proof is a post-access contract
violation and routes to `CF1_INVALID_RUN`; stopping before any market-data read after a proof failure
routes to `PREFLIGHT_FAILURE`.

## 24. Exact scientific outcome set

`PREFLIGHT_FAILURE is not a fourth scientific outcome.` The three scientific execution outcomes
remain:

- `CF1_VALID_PASS`
- `CF1_VALID_FAIL`
- `CF1_INVALID_RUN`

The corrected execution-validation checklist authorizes nothing.

## 25. Exact Phase 4bn-BA result state (branch)

```
CF1_CORRECTED_FEATURE_CONTRACT_REPREREGISTERED__ORIGINAL_AZ_INVALID_RUN_PRESERVED__ESTIMABILITY_AND_ANTI_DUPLICATION_AUDIT_PASSED__NO_DATA_OPENED__NO_EXECUTION_AUTHORIZED__RESERVES_UNTOUCHED
```

## 26. Exact merged result state

```
CF1_CORRECTED_FEATURE_CONTRACT_MERGED_TO_MAIN__ORIGINAL_AZ_INVALID_RUN_PRESERVED__NO_DATA_OPENED__NO_EXECUTION_AUTHORIZED__PHASE_4BN_BB_NOT_AUTHORIZED__RESERVES_UNTOUCHED
```

## 27. No data / no execution / no reserve

`No market data, local Phase 4bn-AZ artefact, target row, feature row, model output, or diagnostic output was opened or read by Phase 4bn-BA or by its merge.`

`No QLIKE, bootstrap, model fitting, target generation, feature generation, diagnostic, backtest, PnL analysis, data acquisition, paper, shadow, live, or exchange-write execution is authorized by this merge.`

`No evidence reserve was opened or spent by Phase 4bn-BA or by its merge.`

`The v002 terminal window and v002 sealed test remain untouched and excluded.`

`The consumed pre-v002 internal holdout and the 2024-11-01 through 2024-11-15 buffer remain unopened.`

No test, linter, type-checker, script, builder, synthetic proof, model, or metric was run by this
phase or its merge; no executable surface changed. No network, web, API, Binance endpoint, credential,
`.env`, MCP, Graphify, or `.mcp.json` access occurred.

## 28. Boundary confirmations

- no source modified
- no test modified
- no script modified
- no schema modified
- no manifest modified
- no ledger modified
- no process standard modified
- no README or `current-project-state.md` modified
- no phase gate or technical-debt register modified
- no Phase 4bn-AY document modified
- no Phase 4bn-AZ document modified
- no `data/microstructure/` file modified or committed
- no `data/research/` file opened or committed
- no local Phase 4bn-AZ artefact opened
- no target or feature row read; no residual recomputed; no condition number computed
- no model trained; no signal computed; no backtest run; no QLIKE or bootstrap computed
- no data acquired; no public endpoint, Binance API, or WebSocket called
- no credential / `.env` / `.mcp.json` / MCP / Graphify used
- no `research_eligible` flipped; no `eligibility_gate_status` transitioned
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked)
- no retained verdict revised
- no project lock loosened
- no M0 amendment
- no evidence reserve opened or spent
- no successor authorized

## 29. Retained verdict ledger

All retained verdicts preserved verbatim: **H0** — FRAMEWORK ANCHOR; **R3** — BASELINE-OF-RECORD;
**R1a** — RETAINED — NON-LEADING; **R1b-narrow** — RETAINED — NON-LEADING; **R2** — FAILED — §11.6;
**F1** — HARD REJECT; **D1-A** — MECHANISM PASS / FRAMEWORK FAIL; **5m thread** — OPERATIONALLY
CLOSED; **V2** — HARD REJECT — terminal for V2 first-spec; **G1** — HARD REJECT — terminal for G1
first-spec; **C1** — HARD REJECT — terminal for C1 first-spec. Plus the Phase 4bn-AZ verdict
`CF1_INVALID_RUN`, preserved verbatim. All preserved verbatim.

## 30. Preserved project locks

Preserved exactly and unchanged: `STOP_LONGHORIZON_ML_ARC`;
`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`; `REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`;
`PRE_V002_INTERNAL_HOLDOUT = CONSUMED`; `V002_TERMINAL_WINDOW = UNTOUCHED_RESERVED`;
`V002_SEALED_TEST = UNTOUCHED_RESERVED`; `HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE`;
`test_rows_loaded = 0`; `research_eligible = false`; `eligibility_gate_status = pending`; all
authorization flags false; the Phase 4aw always-raising `flip_research_eligible(...)` flip (never
invoked); Phase 4bn-AE §19; the Phase 4ak twelve-clause M0 gate with its post-null cooldown rule and
cooled-down-families list; the cooldown and cooled-down-family rules; §11.6 = 8 bps per side;
round-trip = 16 bps; §1.7.3; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6/§7/§8; Phase 4j
§11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4al refined no-rescue rule + §13
boundary + §14 hierarchy; every prior verdict; every dataset identity/hash; all
split/holdout/sidecar/storage policies; and the evidence-ledger and spending-authority rules. All
prior phase results preserved verbatim.

**No stopped arc is softened, merged, reinterpreted, reopened, or rescued.**

## 31. No-rescue constraints

The Phase 4bn-BA merge does not, and cannot, be construed as authorizing:

- ML model training, model selection, strategy hypothesis generation, or any conversion of features
  into signals;
- strategy signal construction, strategy logic, position state, entry/exit rules, or backtest design;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorization;
- any corrected CF-1 execution, target generation, feature generation, synthetic proof, model fit,
  QLIKE, diagnostic, or bootstrap computation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation;
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels;
- mark-price / spot / cross-venue / order-book / additional aggTrades acquisition;
- old-strategy alt-symbol rerun or cooled-down-family reopening;
- 5m research-thread reopening;
- transitioning any manifest's `research_eligible` or `eligibility_gate_status` from this evidence
  alone;
- opening or spending any evidence reserve;
- reclassifying, repairing, rerunning, or continuing Phase 4bn-AZ.

## 32. Successor authorization

**None.**

Candidate successors that are **not** authorized:

- `Phase 4bn-BB — Corrected CF-1 Realized-Volatility Substrate-Test Execution` (proposed title only);
- any corrected CF-1 execution, target/feature generation, model fit, QLIKE, or bootstrap run;
- ML implementation, strategy implementation, backtest implementation;
- paper / shadow / live-readiness / deployment / exchange-write;
- additional aggTrades / 5m / 1m / tick / mark-price / order-book data acquisition;
- production keys, authenticated APIs, private endpoints, user stream;
- MCP / Graphify / `.mcp.json` / credentials.

`Merging Phase 4bn-BA records the corrected preregistration and its governance controls; it does not authorize Phase 4bn-BB or any corrected execution.`

## 33. Merge-is-recordkeeping-only, paused posture, and next action

This merge is a recordkeeping action only: it records the corrected CF-1 preregistration and its
governance controls on `main` and authorizes no execution. Post-merge posture: **paused.**
`Remaining paused is a valid operator choice.`

**A future corrected CF-1 execution requires a separate future operator prompt and a new Claude Code
authorization.** It would be a **new experiment** under the Phase 4bn-BA contract — not a Phase
4bn-AZ rerun, continuation, correction-in-place, reuse of the consumed run, or reclassification. No
data read, synthetic proof, model fit, or metric computation is authorized here.

**Recommended next operator action:** return this Phase 4bn-BA merge-closeout and the final operator
report for review; then decide separately whether to remain paused or authorize Phase 4bn-BB. Default
recommendation: **Remain paused.**
