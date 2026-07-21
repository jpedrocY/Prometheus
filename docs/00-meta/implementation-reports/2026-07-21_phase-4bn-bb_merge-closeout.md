# Phase 4bn-BB — Merge Closeout

## 1. Phase identity and risk tier

Phase 4bn-BB — Corrected CF-1 Realized-Volatility Substrate-Test Execution. A code + tests + local
gitignored artefacts + committed evidence-report phase that executed exactly one new evidence-bearing
corrected CF-1 run under the merged Phase 4bn-BA contract and recorded `CF1_VALID_PASS`. **Tier 1 /
Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` — it runs a preregistered
scientific experiment against the merged contract and consumes an authorized evidence-bearing run,
so it carries the highest ceremony tier.

**This merge is a recordkeeping action only.** It records the corrected implementation, the evidence,
the valid-pass verdict, and the governance controls on `main`. It changes no data, no manifest, no
eligibility state, no reserve, and no lock, and it authorizes no successor phase.

`Merging Phase 4bn-BB records the corrected implementation, evidence, valid-pass verdict, and governance controls; it authorizes no successor phase.`

## 2. Source and target branches

- **Source:** `phase-4bn-bb/corrected-cf1-realized-volatility-substrate-test-execution`
- **Target:** `main`

## 3. Pre-merge `main` / base SHA

`e26193e8f61cae797e4cbfab932025b709b74566` (`HEAD == main == origin/main` at merge time; the Phase
4bn-BA merge-closeout SHA-finalization tip). Verified in sync before any mutation. The only untracked
item was the transient `.claude/scheduled_tasks.lock`, never staged, modified, deleted, cleaned, or
committed.

## 4. Complete Phase 4bn-BB source-branch commit history

Three commits on the source branch after the base, preserved exactly — not squashed, reordered,
rebased, amended, or rewritten:

| # | SHA | Commit message | Role |
|---|---|---|---|
| 1 | `0f5942b31e6dfa5ca537ec2c8b962a0ce57c8917` | `feat(phase-4bn-bb): implement corrected CF-1 execution` | Three corrected source modules, one new BB runner, five BB tests; no historical AY/AZ/BA modification. |
| 2 | `6ba76b56a514cb0abaeac0480a59a688a7cdebeb` | `research(phase-4bn-bb): record corrected CF-1 execution verdict` | One evidence-bearing execution; exact `CF1_VALID_PASS`; execution-and-verdict and artefact/leakage/split validation reports. |
| 3 | `345165710ddb17622d6c679e2d350f2779022068` | `docs(phase-4bn-bb): add closeout` | Final source-branch closeout; one-run-consumed boundary; scientific consequence and non-authorization state. |

This merge-closeout is the **fourth** commit on the source branch.

## 5. Final pre-merge Phase 4bn-BB branch-tip SHA

`345165710ddb17622d6c679e2d350f2779022068` — the approved Phase 4bn-BB state at merge time.

## 6. Merge-closeout branch commit SHA

`4214c658fea625be1d626af99324c5c0babea57c` — the commit on the BB branch that adds this
merge-closeout file (`docs(phase-4bn-bb): add merge closeout`). This is the **fourth** commit on the
source branch.

## 7. No-fast-forward merge commit SHA

`0200d576884ae8461f75768b97b8ad9d938a8a9b` — the commit created by `git merge --no-ff` on `main`
(`research(phase-4bn-bb): merge corrected CF-1 valid-pass execution`).

## 8. SHA-finalization convention

This merge-closeout is created on the BB source branch with the §6 and §7 SHAs as placeholders.
After the `--no-ff` merge into `main`, one narrow SHA-finalization commit on `main`
(`docs(phase-4bn-bb): finalize merge closeout shas`) replaces those placeholders with the actual
merge-closeout branch commit SHA (§6) and the actual `--no-ff` merge commit SHA (§7).

```text
SHA-finalization commit SHA:
this update (`docs(phase-4bn-bb): finalize merge closeout shas`);
its exact SHA equals the resulting final main / origin/main tip and is
recorded in the final operator report and Git log.
```

A commit cannot embed its own SHA; the finalization commit's own SHA equals the resulting final
`main` / `origin/main` tip and is recorded in the final operator report and the Git log after commit.

## 9. Exact source-branch file set (twelve added files)

Relative to pre-merge `main`, the BB branch adds exactly these twelve files — **additions only, no
`M`/`D`/`R`, no whitespace error**:

**Source (3):**

- `src/prometheus/research/microstructure/cf1_corrected_contract_v002.py`
- `src/prometheus/research/microstructure/cf1_corrected_evaluation_v002.py`
- `src/prometheus/research/microstructure/cf1_corrected_artifacts_v002.py`

**Script (1):**

- `scripts/phase4bn_bb_cf1_corrected_realized_volatility_execution.py`

**Tests (5):**

- `tests/research/microstructure/test_cf1_corrected_contract_v002.py`
- `tests/research/microstructure/test_cf1_corrected_evaluation_v002.py`
- `tests/research/microstructure/test_cf1_corrected_artifacts_v002.py`
- `tests/research/microstructure/test_cf1_corrected_no_network_v002.py`
- `tests/research/microstructure/test_phase4bn_bb_cf1_corrected_execution.py`

**Reports (3):**

- `docs/00-meta/implementation-reports/2026-07-21_phase-4bn-bb_cf1-corrected-execution-and-verdict.md`
- `docs/00-meta/implementation-reports/2026-07-21_phase-4bn-bb_cf1-corrected-artefact-leakage-and-split-validation.md`
- `docs/00-meta/implementation-reports/2026-07-21_phase-4bn-bb_closeout.md`

## 10. Thirteenth added file

- `docs/00-meta/implementation-reports/2026-07-21_phase-4bn-bb_merge-closeout.md` (this file).

## 11. Additions-only confirmation

Relative to pre-merge `main` `e26193e8f61cae797e4cbfab932025b709b74566`, the merged change set is
**additions only**: the twelve BB files plus this merge-closeout (thirteen added files), with no
modification, deletion, or rename of any pre-existing path. The one later modification of this
merge-closeout is the narrow SHA-finalization update described in §8. No `data/microstructure/` or
`data/research/` file is modified or committed. No Phase 4bn-AY, Phase 4bn-AZ, or Phase 4bn-BA
document is modified; no historical AZ orchestration/evaluation/artifact module is modified.

## 12. Lineage

| Item | SHA |
|---|---|
| Phase 4bn-BA main finalization / BB base | `e26193e8f61cae797e4cbfab932025b709b74566` |
| Phase 4bn-BA no-fast-forward merge | `7096ce853dd85dfe6bd95ae88942548bc76400dd` |
| Phase 4bn-BA merge-closeout branch | `ba6ddf12dfa97a2f4ef04abf2bd35127c7f04274` |
| Phase 4bn-BA final contract tip | `adc06e68cf532e00b0477d0cefca9d97d2287449` |
| Phase 4bn-AY contract tip | `0fb560656aa9b50cf110602e15be8222b7343623` |
| Phase 4bn-AZ implementation | `05fa63a8bf8c9b1fe386cc4ab67805046ae418b1` |
| Phase 4bn-AZ merge | `8e82e185a0def318acd2ec42fcb73337edc67b51` |
| Phase 4bn-BB implementation | `0f5942b31e6dfa5ca537ec2c8b962a0ce57c8917` |
| Phase 4bn-BB result | `6ba76b56a514cb0abaeac0480a59a688a7cdebeb` |
| Phase 4bn-BB closeout / pre-merge branch tip | `345165710ddb17622d6c679e2d350f2779022068` |

Phase 4bn-AY remains historical and merged; its documents are not modified. Phase 4bn-BA remains the
merged corrected contract; its documents are not modified.

## 13. New-experiment identity and Phase 4bn-AZ non-reuse

`Phase 4bn-BB is a new corrected experiment under the merged Phase 4bn-BA contract, not a rerun or continuation of Phase 4bn-AZ.`

`Phase 4bn-AZ remains CF1_INVALID_RUN and its evidence-bearing run remains consumed.`

Phase 4bn-BB reused only the unchanged, tested target/timestamp primitives of
`cf1_realized_volatility_v001` (RV kernel, `P_at`, allowlist, synthetic boundary cases) and did
**not** import that module's historical three-feature constants. Every BB target row, feature
snapshot, proof, design matrix, model, forecast, loss, metric, bootstrap replicate, manifest, and
inventory was newly generated from the authorized source Parquets under the BB implementation commit
SHA. The runner never read the Phase 4bn-AZ v001 output root (`az_output_root_read = false`); no
Phase 4bn-AZ artefact was opened, imported, hashed for BB scientific use, copied, or reused.

## 14. Exact feature contract

```
CORRECTED_CF1_FEATURE_SET   = { rolling_aggtrade_count_60s , rolling_quantity_sum_60s }
CORRECTED_CF1_FEATURE_COUNT = 2
```

Canonical model-feature order:

1. `rolling_aggtrade_count_60s`
2. `rolling_quantity_sum_60s`

`The Phase 4bn-BB runner reads exactly rolling_aggtrade_count_60s and rolling_quantity_sum_60s as microstructure model features.`

## 15. Prohibited mean boundary

Prohibited feature: `rolling_quantity_mean_60s`.

`rolling_quantity_mean_60s was not read, snapshotted, transformed, emitted, stored, or used in any Phase 4bn-BB scientific decision.`

The requested source feature columns were exactly `feature_timestamp_ms`, `row_index`,
`rolling_aggtrade_count_60s`, `rolling_quantity_sum_60s`; the leakage proof records
`prohibited_feature_read = false`; the target-layer and manifest schemas carry exactly two feature
columns. The original Phase 4bn-AY three-feature set remains
`STRUCTURALLY_NON_IDENTIFIABLE__PROHIBITED_FOR_FUTURE_EXECUTION`.

## 16. Exact target / model / loss / split (inherited unchanged)

- **Target:** BTCUSDT last-trade realized variance; `H = 60 min = 3_600_000 ms`; top-of-UTC-hour
  non-overlapping origins; every RV interval the causal completed interval `(a, b]`; sole operator
  `P_at(u)` (`source_transact_time_ms ≤ u`, greatest `row_index` tie); one-minute UTC grid;
  `r_k = ln(G_k/G_{k-1})`; `RV = Σ_{k=1}^{60} r_k²`; `y = ln(RV + 1e-16)`; no annualization.
- **Coverage:** predicate `τ_{k-1} < ts ≤ τ_k`; `≥ 30 of 60`; no stitching; zero-RV origins retained.
- **Baseline:** `y = β0 + β1·ln(RV_h+ε) + β2·ln(RV_d+ε) + β3·ln(RV_w+ε) + u` (4 columns).
- **Augmented:** baseline `+ γ1·z1 + γ2·z2` (6 columns), baseline being exactly `γ1 = γ2 = 0`.
  Train-only z-score (`ddof = 0`, `σ`-floor `1e-8`); HAR unstandardized; no clipping.
- **Estimator:** deterministic OLS (`numpy.linalg.lstsq`); no regularization / hyperparameter /
  iterative optimizer; one fit per block.
- **Split:** 244 UTC dates 2024-03-01..2024-10-31 excluding 2024-10-01; March warmup train-only;
  blocks B1..B7 (B7 begins 2024-10-02); expanding anchored walk-forward; one-day embargo; one-hour
  purge subsumed; `MIN_TRAIN_ORIGINS = 60`; `MIN_BLOCK_VALID_ORIGINS = 100`; condition guard
  `> 1e10`.
- **Loss / decision:** QLIKE `v = RV+1e-16`, `h = max(exp(ŷ),1e-16)`, `ratio − ln(ratio) − 1`;
  `Δ_equal = (1/7) Σ_i D_i`; `ρ = Δ_equal / QLIKE(base)`; P1 `Δ_equal > 0`; P2 `D_i > 0` in ≥ 6/7;
  P3 stratified moving-block bootstrap (`ℓ_i = ceil(n_i^{1/3})`, `B = 10,000`, seed `20260715`,
  one-sided 95% `LB_95 > 0`).

## 17. Test / lint / type results

Reproduced during merge review (non-data checks only):

- BB unit tests (all five files): **PASS**.
- Full `tests/research/microstructure`: **PASS**.
- `ruff check` over the nine new code/test files: **All checks passed**.
- `mypy --strict` over the three corrected source modules: **Success: no issues found in 3 source
  files**.

Committed pre-merge full-suite result: two **pre-existing, unrelated** failures in
`tests/simulation/test_backtest_real_2026_03.py` (`KeyError: 'trade_count'` in historical kline
storage); no BB-related failure. The full suite was not rerun during merge.

(Note: the `uv run pytest` / `uv run mypy` console-script trampolines error in this environment;
the identical checks were run via `uv run python -m pytest` / `uv run python -m mypy`.)

## 18. Execution accounting

- Standalone `--preflight` invocations: **1** → `PREFLIGHT_PASS` (also rerun internally by `--run`).
- Evidence-bearing `--run` invocations: **exactly 1**.
- Access-start artefact written `2026-07-21T17:36:13.417563Z`, immediately before the first
  market-data byte.
- **The single Phase 4bn-BB evidence-bearing run is consumed. No rerun is authorized.**

## 19. Exact data and origin counts

- Partitions opened: exactly **244** UTC dates, 2024-03-01 .. 2024-10-31, excluding 2024-10-01; each
  verified against its committed `.sha256` sidecar before any row was read.
- Source families: `microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o` (columns
  `transact_time_ms`, `price`, `row_index`); `microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s`
  (columns `feature_timestamp_ms`, `row_index`, `rolling_aggtrade_count_60s`,
  `rolling_quantity_sum_60s`).
- Rows read: normalized **340,447,363**; features **340,447,363**.
- Candidate hourly origins: **5,854**; valid paired origins: **5,516**; invalid: **338**
  (`har_unavailable` 336, `har_coverage_failure` 2); zero-RV origins **0**.

`No v002 terminal-window row, sealed-test row, consumed-holdout row, or 2024-11-01 through 2024-11-15 buffer row was opened.`

## 20. Per-block rank / condition results

| Block | n_train | n_eval | baseline rank | augmented rank | baseline cond | augmented cond |
|---|---:|---:|---:|---:|---:|---:|
| B1 | 551 | 720 | 4 | 6 | 6.172e+02 | 6.494e+02 |
| B2 | 1271 | 744 | 4 | 6 | 4.058e+02 | 4.631e+02 |
| B3 | 2015 | 720 | 4 | 6 | 3.807e+02 | 4.388e+02 |
| B4 | 2735 | 744 | 4 | 6 | 3.418e+02 | 4.101e+02 |
| B5 | 3479 | 744 | 4 | 6 | 3.682e+02 | 4.304e+02 |
| B6 | 4223 | 719 | 4 | 6 | 3.442e+02 | 3.983e+02 |
| B7 | 4966 | 550 | 4 | 6 | 3.634e+02 | 4.172e+02 |

Every baseline design was full rank 4/4 and every augmented design full rank 6/6; all condition
numbers were far below the frozen `> 1e10` guard — the decisive contrast with Phase 4bn-AZ's
augmented condition numbers ≈ 1e16 under the redundant three-feature design.

## 21. QLIKE and block differentials

| Block | QLIKE baseline | QLIKE augmented | `D_i` |
|---|---:|---:|---:|
| B1 | 0.328289 | 0.325487 | +2.801856e-03 |
| B2 | 0.299225 | 0.277698 | +2.152699e-02 |
| B3 | 0.377876 | 0.362673 | +1.520265e-02 |
| B4 | 0.390596 | 0.388103 | +2.492981e-03 |
| B5 | 0.369661 | 0.355433 | +1.422829e-02 |
| B6 | 0.294830 | 0.286185 | +8.644941e-03 |
| B7 | 0.219701 | 0.201027 | +1.867419e-02 |

`All seven block loss differentials were positive.`

## 22. Aggregate metrics

- Equal-weighted `QLIKE(baseline)` = **0.32573980348957254**.
- Equal-weighted `QLIKE(augmented)` = **0.31380095965814664**.
- `Δ_equal` = **0.011938843831425896**.
- Descriptive `ρ` = **0.036651473671709504**.
- MSE-on-variance (equal-weighted): baseline **4.002837163249114e-09**, augmented
  **3.833081052943428e-09**.
- Mincer–Zarnowitz R² (equal-weighted): baseline **0.5335359599299953**, augmented
  **0.5549789834981532**.

## 23. Bootstrap

- Stratified-by-block non-circular moving-block bootstrap of `Δ_equal`; block lengths
  **[9, 10, 9, 10, 10, 9, 9]**; replicates **10,000**; NumPy `PCG64`; seed **20260715**; one-sided
  95% lower percentile, linear quantile method; run exactly once.

`The one-sided 95 percent bootstrap lower bound was 0.006273843055395148, above zero.`

## 24. P1 / P2 / P3 / validity

- **P1** (`Δ_equal > 0`): true. **P2** (`D_i > 0` in ≥ 6/7): true (**7/7**). **P3** (`LB_95 > 0`):
  true. **Validity**: true (all seven blocks valid — full rank, condition ≪ 1e10, no zero-variance,
  finite, `n_train ≥ 60`, `n_eval ≥ 100`, finite QLIKE).

`Phase 4bn-BB produced CF1_VALID_PASS because validity, P1, P2, and P3 all passed under the frozen contract.`

## 25. Exact outcome

```
CF1_VALID_PASS
```

## 26. Exact branch result state

```
CF1_CORRECTED_VALID_PASS__DEVELOPMENT_LEVEL_INCREMENTAL_VOLATILITY_MAGNITUDE_INFORMATION_SUPPORTED__DOCS_ONLY_FILTER_ASSESSMENT_ONLY__NO_DIRECTION_OR_PNL_AUTHORIZED__RESERVES_UNTOUCHED
```

## 27. Exact merged result state

```
CF1_CORRECTED_VALID_PASS_MERGED_TO_MAIN__DEVELOPMENT_LEVEL_INCREMENTAL_VOLATILITY_MAGNITUDE_INFORMATION_SUPPORTED__NO_RERUN_AUTHORIZED__DOCS_ONLY_FILTER_ASSESSMENT_REQUIRED_BEFORE_ANY_DOWNSTREAM_ACTION__NO_DIRECTION_OR_PNL_AUTHORIZED__RESERVES_UNTOUCHED
```

## 28. Scientific consequence

`The valid pass supports development-level incremental one-hour realized-volatility magnitude information only.`

It establishes no price direction, no trading signal, no strategy, no economic materiality, no
profitability, no transaction-cost clearance, no ability to clear the locked 8 bps/side · 16 bps
round trip, no tradability, no M0 clearance, no reserve-period confirmation, and no terminal/sealed
generalization.

`No direction, signal, strategy, PnL, backtest, paper, shadow, live, or exchange-write authorization follows from Phase 4bn-BB or from its merge.`

## 29. Artefact and sidecar validation

The committed artefact/leakage/split-validation report records: eight required artefact families;
eight paired `.sha256` sidecars (16 files total); all eight recomputed digests matched their own
sidecars; no duplicate family; the target layer carried exactly two feature columns; the prohibited
mean column absent from every schema/payload/manifest; no data or artefact committed.

## 30. Local gitignored artefact status

The BB output root `data/research/cf1_corrected_realized_volatility_substrate_test_v002/` is local
and **gitignored**. It was not opened, inspected, hashed, staged, modified, deleted, or cleaned
during this merge, and the Phase 4bn-AZ artefact root was not opened. No data or artefact file is
committed.

## 31. No-rerun boundary

`The single Phase 4bn-BB evidence-bearing run is consumed and no rerun is authorized.` No second seed,
second feature set, second bootstrap, or second evidence-bearing invocation is authorized. The merge
did not run the BB runner, market-data workflows, QLIKE, bootstrap, model fitting, or artefact
generation, and did not recompute or reinterpret any recorded value.

## 32. Reserve and preserved locks

No reserve was opened or spent; no evidence-ledger transition is authorized. Preserved exactly and
unchanged: `STOP_LONGHORIZON_ML_ARC`; `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`;
`REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`; `PRE_V002_INTERNAL_HOLDOUT = CONSUMED`;
`V002_TERMINAL_WINDOW = UNTOUCHED_RESERVED`; `V002_SEALED_TEST = UNTOUCHED_RESERVED`;
`HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE`; `test_rows_loaded = 0`;
`research_eligible = false`; `eligibility_gate_status = pending`; all authorization flags false; the
Phase 4aw always-raising `flip_research_eligible(...)` flip (never invoked); Phase 4bn-AE §19; the
Phase 4ak twelve-clause M0 gate with its cooldown and cooled-down-family rules; 8 bps/side and 16 bps
round trip; every prior verdict; every dataset identity/hash; all split/holdout/sidecar/storage
policies; and the evidence-ledger and spending-authority rules. **No stopped arc is softened, merged,
reinterpreted, reopened, or rescued.**

## 33. No direction / strategy / PnL

This merge authorizes no direction, signal, strategy, position state, entry/exit logic, backtest,
PnL, paper, shadow, live-readiness, deployment, or exchange-write work, and no ML/strategy/backtest
implementation.

## 34. No Phase 4bn-BC authorization

`Phase 4bn-BC — CF-1 Valid-Pass Filter-Admissibility and Consequence Assessment remains proposed only and requires a separate operator prompt.`

No successor phase is authorized by this merge and no successor prompt is created.

## 35. Merge-is-recordkeeping-only

`Merging Phase 4bn-BB records the corrected implementation, evidence, valid-pass verdict, and governance controls; it authorizes no successor phase.`

The merge records the corrected CF-1 valid-pass execution and its governance controls on `main` and
authorizes no execution, data read, rerun, or downstream action.

## 36. Paused posture and next operator action

Post-merge posture: **paused.** A docs-only Phase 4bn-BC filter-admissibility and consequence
assessment, if separately authorized, is the only proposed continuation and would require a new
operator prompt. Recommended next operator action: return this Phase 4bn-BB merge-closeout and the
final operator report for review; then decide separately whether to remain paused or authorize the
proposed docs-only Phase 4bn-BC. Default recommendation: **remain paused.**

`Remaining paused is a valid operator choice.`
