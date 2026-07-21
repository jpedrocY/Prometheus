# Phase 4bn-BB — Corrected CF-1 Artefact, Leakage, and Split Validation

Companion evidence-validation report to
`2026-07-21_phase-4bn-bb_cf1-corrected-execution-and-verdict.md`. It records the local (gitignored)
artefact inventory, sidecar validation, provenance, the exact opened/forbidden partitions, and the
leakage / split / coverage / estimability / timestamp proofs for the single Phase 4bn-BB
evidence-bearing run. Implementation commit `0f5942b31e6dfa5ca537ec2c8b962a0ce57c8917`.

## 1. BB output root

```
data/research/cf1_corrected_realized_volatility_substrate_test_v002/
```

Local and **gitignored** (`git check-ignore` confirms). Distinct from the Phase 4bn-AZ v001 root
`data/research/cf1_realized_volatility_substrate_test_v001/`, which was never opened, read, imported,
or reused (`az_output_root_read = false`). No data or artefact file is committed.

## 2. Artefact inventory (paths, bytes, SHA-256)

All eight required artefact families are present, each with a paired `.sha256` sidecar (16 files
total); no duplicate family. SHA-256 recomputed locally and compared against each artefact's own
sidecar — **all match**.

| Family | Relative path | Bytes | SHA-256 (prefix) |
|---|---|---|---|
| symbolic estimability proof | `proofs/cf1_corrected_symbolic_estimability_proof_v002__v002__1784655373235__0f5942b31e6d.json` | 11,603 | `16c3eefba2303810…` |
| timestamp boundary proof | `proofs/cf1_corrected_timestamp_boundary_proof_v002__v002__1784655373337__0f5942b31e6d.json` | 10,203 | `4c0edad0835ca555…` |
| execution access start | `runs/cf1_corrected_execution_access_start_v002__v002__1784655373417__0f5942b31e6d.json` | 12,667 | `59ef6c77094bc6df…` |
| leakage/split/coverage proof | `proofs/cf1_corrected_leakage_split_coverage_proof_v002__v002__1784656173800__0f5942b31e6d.json` | 55,187 | `21a3cd8a814f2ecb…` |
| realized-variance target layer | `targets/cf1_corrected_realized_variance_target_layer_v002__v002__1784656173901__0f5942b31e6d.parquet` | 427,825 | `59422956cb1c1c93…` |
| paired model predictions | `runs/cf1_corrected_paired_model_predictions_v002__v002__1784656173901__0f5942b31e6d.parquet` | 245,688 | `0f46530b8057cce5…` |
| model run manifest | `manifests/cf1_corrected_model_run_manifest_v002__v002__1784656175142__0f5942b31e6d.json` | 17,119 | `f380db6d45a1b7bb…` |
| execution artifact inventory | `manifests/cf1_corrected_execution_artifact_inventory_v002__v002__1784656175216__0f5942b31e6d.json` | 9,881 | `82a86509cbe9ec79…` |

Filename convention: `<family>__v002__<unix_ms>__<short_commit>.<ext>`; sidecar body
`<hex-sha256>␠␠<basename>\n`. The inventory artefact lists the other seven artefacts (it cannot embed
its own digest); `artifact_count = 7`.

## 3. Sidecar validation

Every artefact's recomputed SHA-256 equals the digest in its own BB `.sha256` sidecar, and each
sidecar basename equals the artefact basename. **ALL_SIDECARS_OK = true** (8/8).

## 4. Provenance

Stamped into every JSON artefact:

- `phase_id = phase-4bn-bb`; `symbol = BTCUSDT`; `contract_version = v002`;
- `base_main_commit_sha = e26193e8f61cae797e4cbfab932025b709b74566`;
- `phase_4bn_ba_merge_commit_sha = 7096ce853dd85dfe6bd95ae88942548bc76400dd`;
- `phase_4bn_ba_contract_tip_sha = adc06e68cf532e00b0477d0cefca9d97d2287449`;
- `phase_4bn_ay_contract_tip_sha = 0fb560656aa9b50cf110602e15be8222b7343623`;
- `phase_4bn_az_implementation_sha = 05fa63a8bf8c9b1fe386cc4ab67805046ae418b1`;
- `phase_4bn_az_merge_commit_sha = 8e82e185a0def318acd2ec42fcb73337edc67b51`;
- `code_commit_sha = 0f5942b31e6dfa5ca537ec2c8b962a0ce57c8917`;
- `command = uv run python scripts/phase4bn_bb_cf1_corrected_realized_volatility_execution.py --run`;
- environment: Python 3.12.4, NumPy 2.4.4, PyArrow 23.0.1.

## 5. Source family and exact columns read

- Prices/RV: `microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o` — columns
  `transact_time_ms`, `price`, `row_index`.
- Features: `microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s` — columns
  `feature_timestamp_ms`, `row_index`, `rolling_aggtrade_count_60s`, `rolling_quantity_sum_60s`.
- Leakage-proof `feature_columns_read` records exactly those four feature columns;
  `prohibited_feature_read = false`.

`rolling_quantity_mean_60s was not read, snapshotted, transformed, emitted, stored, or used in any Phase 4bn-BB scientific decision.`

## 6. Exact opened dates and forbidden ranges

- Partitions opened: **244** UTC dates, first `2024-03-01`, last `2024-10-31`
  (`partitions_opened_count = 244`).
- `october_1_opened = false`; `november_or_later_opened = false`;
  `consumed_holdout_opened = false`; `terminal_opened = false`; `sealed_opened = false`;
  `october_31_23_00_retained = false`.

`No v002 terminal-window row, sealed-test row, consumed-holdout row, or 2024-11-01 through 2024-11-15 buffer row was opened.`

Each opened Parquet was verified against its committed `.sha256` sidecar before any row was read;
partition construction used the exact 244-date allowlist with a fail-closed path guard (no glob or
broad scan can reach a forbidden partition).

## 7. Source row counts

- Normalized rows read: **340,447,363**.
- Feature rows read: **340,447,363**.

## 8. Timestamp-boundary proof (§14)

`cf1_corrected_timestamp_boundary_proof_v002`, synthetic rows only, **20 checks, all passed**
(`timestamp_boundary_proof_passed = true`; `market_data_opened = false`; `reserve_touched = false`).
It inherits the 14 Phase 4bn-AZ boundary cases (greatest-`row_index` tie; boundary-jump capture;
`P_at(t)` terminal inclusion; origin-time-jump exclusion; right-endpoint inclusion; feature snapshot
may include the exact-origin row; single-assignment; strict-`<`/half-open fails; right-closed
coverage predicate; Oct-31 22:00 valid / 23:00 invalid; Nov-1 and Oct-1 partitions rejected before
open; allowlist excludes all forbidden partitions) and adds six corrected-feature cases (snapshot is
exactly count + quantity-sum; no mean column requested; invalid if count < 1; invalid if quantity
sum ≤ 0; a valid positive snapshot accepted; no explicit mean/ratio feature formed).

## 9. Symbolic estimability proof (§13)

`cf1_corrected_symbolic_estimability_proof_v002`, static, pre-data, **22 checks, all passed**
(`symbolic_estimability_proof_passed = true`; `market_data_opened = false`;
`evidence_consumed = false`; `reserve_touched = false`). It records: the exact two-feature list and
count; the closed committed candidate universe and the absence of a committed dispersion feature;
the removed/prohibited mean feature; the floor-quantizer rule `mean_int = (sum_int × 10^12) // count`;
the ideal quotient `x3* = x2/x1` and `ln(x3*) = ln(x2) − ln(x1)`; the stored relation
`ln(x3) = ln(x2) − ln(x1) + δ` with `δ ≤ 0`, generally nonzero; no exact stored identity and no
universal relative-error bound; the retained features as primitive committed accumulators; no
source-implied exact affine dependency between `ln(x1)` and `ln(x2)` and none with the HAR block;
baseline/augmented parameter counts 4/6 and expected rank 6 scoped to source definitions only;
training minimum 60; block minimum 100; runtime guards as final arbiter; the prohibited status of the
original three-feature set. The validator re-checked every frozen field before data access.

## 10. Leakage / split / coverage proof

`cf1_corrected_leakage_split_coverage_proof_v002`, **`leakage_split_coverage_proof_passed = true`**.
Recorded: covered-minute predicate `τ_{k-1} < ts ≤ τ_k`; `coverage_threshold = 30`; feature snapshot
rule `feature_timestamp_ms ≤ t` (greatest `row_index` tie); HAR interval rule `(t − L, t]`;
`embargo_ms = 86_400_000`; `purge_ms = 3_600_000`; block dates B1..B7; the per-block valid-origin
counts; and all boundary flags false (§6).

## 11. Feature snapshot rule

Per valid origin, the two retained columns are read from the last committed feature row with
`feature_timestamp_ms ≤ t` (greatest `row_index` tie); a row timestamped exactly at `t` may be used;
the upstream 60-second window must not cross an inaccessible segment start. A valid origin requires
`rolling_aggtrade_count_60s ≥ 1`, `rolling_quantity_sum_60s > 0`, both finite. Transform:
`u_j = ln(x_j)`, then train-only z-score.

## 12. Candidate / valid / invalid and per-block counts

- Candidate hourly origins: **5,854**; valid paired origins: **5,516**; invalid: **338**
  (`har_unavailable` 336, `har_coverage_failure` 2 — warmup-boundary HAR-lookback unavailability
  only). `zero_rv_origin_count = 0`.

| Block | training origins | evaluation origins |
|---|---|---|
| B1 | 551 | 720 |
| B2 | 1271 | 744 |
| B3 | 2015 | 720 |
| B4 | 2735 | 744 |
| B5 | 3479 | 744 |
| B6 | 4223 | 719 |
| B7 | 4966 | 550 |

All blocks satisfy `n_train ≥ 60` and `n_eval ≥ 100`.

## 13. Target-layer schema and paired-prediction schema

- **Target layer** (`5,854` rows — every candidate origin) columns: `origin_timestamp_ms`,
  `origin_utc`, `origin_utc_date`, `evaluation_block`, `target_end_timestamp_ms`, `target_valid`,
  `target_invalid_reason`, `covered_minute_count`, `rv_target`, `log_rv_target`, `rv_h`, `rv_d`,
  `rv_w`, **`rolling_aggtrade_count_60s`**, **`rolling_quantity_sum_60s`**,
  `feature_snapshot_timestamp_ms`, `feature_snapshot_row_index`, `source_segment`, `in_reserve`,
  `november_or_later_touched`. **Exactly two** feature columns; `rolling_quantity_mean_60s` absent.
- **Paired predictions** (`4,941` rows = Σ per-block valid origins) columns:
  `origin_timestamp_ms`, `evaluation_block`, `yhat_baseline`, `yhat_augmented`, `qlike_baseline`,
  `qlike_augmented`, `loss_differential`. Written because ≥ 1 block produced valid paired forecasts;
  no mean column.

## 14. Manifest fields

`cf1_corrected_model_run_manifest_v002` carries: the full frozen contract (interval, `P_at`,
coverage predicate/threshold, `ε`, feature list = two columns, `feature_count = 2`,
`prohibited_feature = rolling_quantity_mean_60s`, HAR lags, OLS, baseline/augmented parameter counts
4/6, expected ranks 4/6, `condition_number_max = 1e10`, `min_training_origins = 60`,
`min_block_valid_origins = 100`, QLIKE safeguard, `n_blocks = 7`, embargo/purge, bootstrap
method/seed/replicates/quantile); the counts (partitions, rows, candidate/valid/invalid, per-block
train/valid, zero-RV, bootstrap block lengths); the per-block metrics; the aggregate metrics; the
verdict `CF1_VALID_PASS` and its long result state; `scored = true`.

## 15. Governance and non-authorization flags

- Governance: `no_october_1`, `no_november`, `no_holdout`, `no_terminal`, `no_sealed`, `no_network`,
  `no_acquisition`, `no_az_output_root_read`, `no_prohibited_mean_feature`, `no_pnl`, `no_direction`
  — all **true**.
- Non-authorization flags (eight): `ml_authorized`, `diagnostics_authorized`, `strategy_authorized`,
  `signals_authorized`, `pnl_authorized`, `backtest_authorized`, `live_authorized`,
  `exchange_write_authorized` — all **false**.

## 16. No AZ reuse, no reserve, no network

`Phase 4bn-AZ remains CF1_INVALID_RUN and its evidence-bearing run remains consumed.` No Phase 4bn-AZ
artefact, target, snapshot, proof, manifest, condition number, residual, origin count, prediction, or
metric was read, imported, hashed for BB scientific use, or reused. No evidence reserve was opened or
spent (`PRE_V002_INTERNAL_HOLDOUT = CONSUMED`; `V002_TERMINAL_WINDOW`/`V002_SEALED_TEST =
UNTOUCHED_RESERVED`; `test_rows_loaded = 0`). No network, API, endpoint, credential, `.env`, MCP, or
data acquisition occurred.
