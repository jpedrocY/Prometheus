# Phase 4bn-BB — Corrected CF-1 Realized-Volatility Substrate-Test Execution and Verdict

## 1. Phase identity

Phase 4bn-BB — Corrected CF-1 Realized-Volatility Substrate-Test Execution. A **code + tests +
local gitignored artefacts + committed evidence-report** phase executing exactly one new
evidence-bearing corrected CF-1 run under the merged Phase 4bn-BA contract.

`Phase 4bn-BB is a new corrected experiment under the merged Phase 4bn-BA contract, not a rerun or continuation of Phase 4bn-AZ.`

`Phase 4bn-AZ remains CF1_INVALID_RUN and its evidence-bearing run remains consumed.`

Branch: `phase-4bn-bb/corrected-cf1-realized-volatility-substrate-test-execution`.

## 2. Base and lineage SHAs

| Item | SHA |
|---|---|
| Base `main` == `origin/main` at branch creation (Phase 4bn-BA merge-closeout SHA-finalization tip) | `e26193e8f61cae797e4cbfab932025b709b74566` |
| Phase 4bn-BA no-fast-forward merge commit | `7096ce853dd85dfe6bd95ae88942548bc76400dd` |
| Phase 4bn-BA merge-closeout branch commit | `ba6ddf12dfa97a2f4ef04abf2bd35127c7f04274` |
| Phase 4bn-BA final pre-merge contract tip | `adc06e68cf532e00b0477d0cefca9d97d2287449` |
| Phase 4bn-AY final scientific-contract tip | `0fb560656aa9b50cf110602e15be8222b7343623` |
| Phase 4bn-AZ evidence-bearing implementation SHA | `05fa63a8bf8c9b1fe386cc4ab67805046ae418b1` |
| Phase 4bn-AZ no-fast-forward merge SHA | `8e82e185a0def318acd2ec42fcb73337edc67b51` |
| **Phase 4bn-BB implementation commit SHA** | `0f5942b31e6dfa5ca537ec2c8b962a0ce57c8917` |

The only untracked item throughout was `.claude/scheduled_tasks.lock`, never staged, modified,
deleted, cleaned, or committed. `main` and `origin/main` remained at
`e26193e8f61cae797e4cbfab932025b709b74566`.

## 3. New-experiment identity and Phase 4bn-AZ non-reuse

Phase 4bn-BB is a **new experiment** under the Phase 4bn-BA corrected feature contract. It is not a
Phase 4bn-AZ rerun, continuation, correction-in-place, reuse of the consumed run, or
reclassification.

`Phase 4bn-AZ remains CF1_INVALID_RUN and its evidence-bearing run remains consumed.`

No Phase 4bn-AZ local artefact was opened, imported, hashed for BB scientific use, copied, or
reused. The BB implementation lives in new, clearly-versioned modules
(`cf1_corrected_contract_v002`, `cf1_corrected_evaluation_v002`, `cf1_corrected_artifacts_v002`,
`scripts/phase4bn_bb_cf1_corrected_realized_volatility_execution.py`); it reuses only the unchanged,
tested target/timestamp primitives of `cf1_realized_volatility_v001` (RV kernel, `P_at`, allowlist,
synthetic boundary cases) and does **not** import that module's historical three-feature constants.
Every BB target row, feature snapshot, proof, design matrix, model, forecast, loss, metric,
bootstrap replicate, manifest, and inventory was newly generated from the authorized source Parquets
under the BB implementation commit SHA. The runner never reads the Phase 4bn-AZ v001 output root
(`az_output_root_read = false`).

## 4. Exact features

Corrected feature contract, exact and in canonical order:

```
CORRECTED_CF1_FEATURE_SET   = { rolling_aggtrade_count_60s , rolling_quantity_sum_60s }
CORRECTED_CF1_FEATURE_COUNT = 2
```

`The Phase 4bn-BB runner reads exactly rolling_aggtrade_count_60s and rolling_quantity_sum_60s as microstructure model features.`

`rolling_quantity_mean_60s was not read, snapshotted, transformed, emitted, stored, or used in any Phase 4bn-BB scientific decision.`

The requested source feature columns were exactly
`["feature_timestamp_ms", "row_index", "rolling_aggtrade_count_60s", "rolling_quantity_sum_60s"]`
(leakage proof `feature_columns_read`; `prohibited_feature_read = false`). The original Phase 4bn-AY
three-feature set remains `STRUCTURALLY_NON_IDENTIFIABLE__PROHIBITED_FOR_FUTURE_EXECUTION`.

## 5. Exact target / model / loss / split (inherited unchanged)

- **Target:** BTCUSDT last-trade realized variance; `H = 60 min = 3_600_000 ms`; top-of-UTC-hour
  non-overlapping origins; every RV interval the causal completed interval `(a, b]`; sole operator
  `P_at(u)` (`source_transact_time_ms ≤ u`, greatest `row_index` tie); one-minute UTC grid;
  `r_k = ln(G_k/G_{k-1})`; `RV = Σ_{k=1}^{60} r_k²`; `y = ln(RV + 1e-16)`; no annualization.
- **Coverage:** covered-minute predicate `τ_{k-1} < ts ≤ τ_k`; threshold `≥ 30 of 60`; no stitching;
  zero-RV origins retained (`zero_rv_origin_count = 0`).
- **Baseline:** `y = β0 + β1·ln(RV_h+ε) + β2·ln(RV_d+ε) + β3·ln(RV_w+ε) + u` (4 params).
- **Augmented:** baseline `+ γ1·z1 + γ2·z2` (6 params), the baseline being exactly `γ1 = γ2 = 0`.
  `z_j = (ln x_j − μ_j^train)/max(σ_j^train, 1e-8)`, population std (`ddof = 0`), train-only per
  block; HAR regressors unstandardized; no clipping.
- **Estimator:** deterministic OLS (`numpy.linalg.lstsq`); no regularization, no hyperparameter, no
  iterative optimizer; one fit per block.
- **Split:** 244 UTC dates 2024-03-01..2024-10-31 excluding 2024-10-01; March warmup train-only;
  seven blocks B1..B7 (B7 begins 2024-10-02); expanding anchored walk-forward; one-calendar-day
  embargo; one-hour purge subsumed; `MIN_TRAIN_ORIGINS = 60`; `MIN_BLOCK_VALID_ORIGINS = 100`.
- **Loss / decision:** QLIKE `v = RV+1e-16`, `h = max(exp(ŷ),1e-16)`, `ratio − ln(ratio) − 1`;
  `d_{i,t} = QLIKE_base − QLIKE_aug`; `D_i = mean_t d_{i,t}`; `Δ_equal = (1/7) Σ_i D_i`;
  `ρ = Δ_equal / QLIKE(base)`; P1 `Δ_equal > 0`; P2 `D_i > 0` in ≥ 6/7 blocks; P3 stratified
  moving-block bootstrap (`ℓ_i = ceil(n_i^{1/3})`, `B = 10,000`, seed `20260715`, one-sided 95%
  `LB_95 > 0`).

## 6. Preflight result

`PREFLIGHT_PASS` (final pre-data preflight, run once standalone; also rerun internally by `--run`).
Gates confirmed: code SHA `0f5942b3…`; base main `e26193e8…`; BA merge/contract and AY SHAs;
BB output root absent/empty; D: free ≈ 1154.2 GiB ≥ 500; all 244 normalized + 244 feature Parquets
and sidecars present; 244-date allowlist with no forbidden date; static symbolic estimability proof
(22 checks) passed; deterministic synthetic timestamp-boundary proof (20 checks) passed; no reserve;
no network. The standalone `--preflight` opened no market-data content and wrote no persistent
artefact (BB output root did not exist afterwards).

## 7. Access-start and evidence-consumption

- Access-start record written at `2026-07-21T17:36:13.417563Z`
  (`market_data_access_started = true`), immediately after the symbolic proof and timestamp proof
  artefacts and immediately before the first market-data byte.
- **Market-data access began; the single Phase 4bn-BB evidence-bearing run is consumed.**
- Wall-clock: ≈ 802.5 s.

`After market-data access begins, any invalidation consumes the single Phase 4bn-BB evidence-bearing run and no rerun is authorized.`

## 8. Source partitions and rows

- Source families: prices/RV
  `microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o` (columns
  `transact_time_ms`, `price`, `row_index`); features
  `microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s` (columns
  `feature_timestamp_ms`, `row_index`, `rolling_aggtrade_count_60s`, `rolling_quantity_sum_60s`).
- Partitions opened: exactly **244** UTC dates, 2024-03-01 .. 2024-10-31, excluding 2024-10-01;
  every Parquet verified against its committed `.sha256` sidecar before any row was read.
- Rows read: normalized **340,447,363**; features **340,447,363**.

`No v002 terminal-window row, sealed-test row, consumed-holdout row, or 2024-11-01 through 2024-11-15 buffer row was opened.`

## 9. Origin counts

- Candidate hourly origins: **5,854**.
- Valid paired origins: **5,516**.
- Invalid origins: **338** — `har_unavailable` 336, `har_coverage_failure` 2 (both are
  warmup-boundary HAR-lookback unavailability; none is a feature-invalidity or a coverage failure of
  the target hour). The corrected valid-origin set is equal to or a superset of the Phase 4bn-AY set,
  as the corrected contract never forms the floor-quantized mean.

## 10. Per-block counts and diagnostics

| Block | n_train | n_eval | baseline rank | augmented rank | baseline cond | augmented cond |
|---|---|---|---|---|---|---|
| B1 | 551 | 720 | 4 | 6 | 6.172e+02 | 6.494e+02 |
| B2 | 1271 | 744 | 4 | 6 | 4.058e+02 | 4.631e+02 |
| B3 | 2015 | 720 | 4 | 6 | 3.807e+02 | 4.388e+02 |
| B4 | 2735 | 744 | 4 | 6 | 3.418e+02 | 4.101e+02 |
| B5 | 3479 | 744 | 4 | 6 | 3.682e+02 | 4.304e+02 |
| B6 | 4223 | 719 | 4 | 6 | 3.442e+02 | 3.983e+02 |
| B7 | 4966 | 550 | 4 | 6 | 3.634e+02 | 4.172e+02 |

Every block: baseline full rank 4/4, augmented full rank 6/6; augmented condition numbers
≈ 4.0e+02 – 6.5e+02, far below the `> 1e10` guard. This is the decisive contrast with Phase 4bn-AZ's
augmented condition numbers ≈ 1e16 under the redundant three-feature design: removing the
deterministically derived, floor-quantized mean column restored conditioning. All seven blocks met
`n_train ≥ 60` and `n_eval ≥ 100`. `zero_rv_count = 0` in every block.

## 11. QLIKE per block and `D_i`

| Block | QLIKE baseline | QLIKE augmented | `D_i` (base − aug) |
|---|---|---|---|
| B1 | 0.328289 | 0.325487 | +2.801856e-03 |
| B2 | 0.299225 | 0.277698 | +2.152699e-02 |
| B3 | 0.377876 | 0.362673 | +1.520265e-02 |
| B4 | 0.390596 | 0.388103 | +2.492981e-03 |
| B5 | 0.369661 | 0.355433 | +1.422829e-02 |
| B6 | 0.294830 | 0.286185 | +8.644941e-03 |
| B7 | 0.219701 | 0.201027 | +1.867419e-02 |

All seven `D_i > 0`.

## 12. Aggregate metrics

- Equal-weighted `QLIKE(baseline)` = **0.32573980348957254**.
- Equal-weighted `QLIKE(augmented)` = **0.31380095965814664**.
- `Δ_equal` = **0.011938843831425896**.
- `ρ` = **0.036651473671709504** (descriptive; ≈ 3.67 % relative QLIKE improvement).
- Descriptive secondary metrics (frozen; non-decision-bearing): equal-weighted MSE-on-variance
  baseline **4.002837163249114e-09**, augmented **3.833081052943428e-09**; equal-weighted
  Mincer–Zarnowitz R² baseline **0.5335359599299953**, augmented **0.5549789834981532**.

## 13. Bootstrap configuration and result

- Stratified-by-block non-circular moving-block bootstrap of `Δ_equal`; block lengths
  `ℓ_i = ceil(n_i^{1/3})` = **[9, 10, 9, 10, 10, 9, 9]** for `n_i` = [720, 744, 720, 744, 744, 719,
  550]; replicates **10,000**; RNG NumPy `PCG64`; seed **20260715**; one-sided 95% lower percentile,
  linear quantile method; run exactly once.
- `LB_95` = **0.006273843055395148** > 0.

## 14. P1 / P2 / P3 and validity

- **P1** (`Δ_equal > 0`): **True** (0.011938843831425896 > 0).
- **P2** (`D_i > 0` in ≥ 6/7 blocks): **True** (positive block count = **7/7**).
- **P3** (`LB_95 > 0`): **True** (0.006273843055395148 > 0).
- **Validity**: **True** — all seven blocks valid (full rank, condition ≪ 1e10, no zero-variance,
  finite, `n_train ≥ 60`, `n_eval ≥ 100`, finite QLIKE).

## 15. Exact scientific outcome

```
CF1_VALID_PASS
```

Routing: invalid conditions first (none); then `CF1_VALID_PASS` iff validity ∧ P1 ∧ P2 ∧ P3 (all
true).

## 16. Exact long result state

```
CF1_CORRECTED_VALID_PASS__DEVELOPMENT_LEVEL_INCREMENTAL_VOLATILITY_MAGNITUDE_INFORMATION_SUPPORTED__DOCS_ONLY_FILTER_ASSESSMENT_ONLY__NO_DIRECTION_OR_PNL_AUTHORIZED__RESERVES_UNTOUCHED
```

## 17. Consequence

A valid pass supports **development-level incremental one-hour realized-volatility magnitude
information only**. It establishes no direction, no signal, no profitability, no ability to clear the
locked 8 bps/side · 16 bps round trip, no tradability, and no M0 clearance. The recommended next
action is a **separate docs-only filter-admissibility and consequence assessment**; no strategy,
signal, or PnL phase is automatically authorized.

`No direction, signal, strategy, PnL, backtest, paper, shadow, live, or exchange-write authorization follows from Phase 4bn-BB.`

## 18. Non-authorization and reserve status

- No rerun of the evidence-bearing command is authorized (the single run is consumed).
- All eight authorization flags remain `false`; `research_eligible = false`;
  `eligibility_gate_status = pending`; the Phase 4aw always-raising `flip_research_eligible(...)`
  behaviour preserved and not invoked.
- `PRE_V002_INTERNAL_HOLDOUT = CONSUMED`; `V002_TERMINAL_WINDOW = UNTOUCHED_RESERVED`;
  `V002_SEALED_TEST = UNTOUCHED_RESERVED`; `test_rows_loaded = 0`;
  `v002_terminal_window_read = false`; `sealed_test_split_touched = false`;
  `consumed_holdout_opened = false`; `november_buffer_opened = false`; no reserve opened or spent.
- No network, API, endpoint, credential, `.env`, MCP, or data acquisition occurred.

`Remaining paused is a valid operator choice.`
