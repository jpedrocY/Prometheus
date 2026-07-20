# Phase 4bn-AZ — CF-1 Artefact, Leakage, and Split Validation

Companion to `2026-07-17_phase-4bn-az_cf1-execution-and-verdict.md`. Records the exact local
artefact surface, its integrity hashes, the source partitions opened and not opened, and the
timestamp / leakage / split / coverage evidence for the single Phase 4bn-AZ evidence-bearing run.

Verdict recorded by that run: **`CF1_INVALID_RUN`** (augmented-model condition number `> 1e10` in
all seven blocks). Code SHA `05fa63a8bf8c9b1fe386cc4ab67805046ae418b1`; base `main`
`e65feb849c8020b5e157d1c472b1a075244c7d9d`.

## 1. Local artefact root

```
data/research/cf1_realized_volatility_substrate_test_v001/
```

**Gitignored and not committed.** Confirmed by `git check-ignore -v`:

```
.gitignore:88:data/research/	data/research/cf1_realized_volatility_substrate_test_v001/manifests/x.json
```

No local artefact was staged or committed. No raw or normalized market row was committed.
Required subdirectories `proofs/`, `targets/`, `runs/`, `manifests/`, `logs/` were created;
`logs/` is empty (the run emitted no separate log file).

## 2. Artefact inventory with hashes

Six artefacts, each with a paired `.sha256` sidecar in the exact Phase 4bb-F format
`<hex-sha256>␠␠<basename>\n`. Filenames follow
`<family>__<version/context>__<unix_ms>__<short_commit>.<ext>` with short commit `05fa63a8bf8c`.

| # | Relative path | Bytes | SHA256 |
|---|---|---|---|
| 1 | `proofs/cf1_timestamp_boundary_proof_v001__v001__1784558563200__05fa63a8bf8c.json` | 8,556 | `ecdf0fcbad2e192968c0bb9960c8c9117813fd217e94c4a938f201e8aff77248` |
| 2 | `runs/cf1_execution_access_start_v001__v001__1784558563266__05fa63a8bf8c.json` | 11,715 | `66c807976dc43e1d74e697336b91a15a39f54814485197103c4a9878d43c2ed2` |
| 3 | `targets/cf1_realized_variance_target_layer_v001__v001__1784558563266__05fa63a8bf8c.parquet` | 478,424 | `9a7f1a922a02391ac997244e196e12446f56db6deb696ba66d5b8dffcc245010` |
| 4 | `proofs/cf1_leakage_split_coverage_proof_v001__v001__1784559571783__05fa63a8bf8c.json` | 54,262 | `c398d9ac6e1a4dabb86861d4f6d2a9c2c83f651a0d6cd56f090452646b0fba1e` |
| 5 | `manifests/cf1_model_run_manifest_v001__v001__1784558563266__05fa63a8bf8c.json` | 13,905 | `794480596f9623117f576d205f6fc5926769bf33e61f4494ffc023ad7027ebd9` |
| 6 | `manifests/cf1_execution_artifact_inventory_v001__v001__1784559572363__05fa63a8bf8c.json` | 8,251 | `fefc5b51e45b203283ff24f32f793fee6a23580adc142fa52514c626872bc1df` |

**Sidecar re-validation result: `ALL_SIDECARS_VALID: True`** — every artefact's recomputed
SHA256 equals its sidecar digest and every sidecar basename equals its artefact filename.

### 2.1 Family `cf1_paired_model_predictions_v001` — deliberately absent

The per-origin paired predictions Parquet was **not** written, correctly: no block produced a
fitted augmented model, so there are zero paired forecasts and zero per-origin losses. Writing an
empty or partial predictions artefact would have implied a scoring stage that never occurred. Its
absence is recorded here as expected behaviour of the fail-closed path, not as a missing artefact.

## 3. Provenance carried by every JSON artefact

`created_at_unix_ms`; `created_at_utc`;
`base_main_commit_sha = e65feb849c8020b5e157d1c472b1a075244c7d9d`;
`phase_4bn_ay_merge_commit_sha = cd5a3b7128bb7bc8d887fb4c7ea1c1538e5b1305`;
`phase_4bn_ay_contract_tip_sha = 0fb560656aa9b50cf110602e15be8222b7343623`;
`code_commit_sha = 05fa63a8bf8c9b1fe386cc4ab67805046ae418b1`;
`command = uv run python scripts/phase4bn_az_cf1_realized_volatility_execution.py --run`;
`python_version = 3.12.4`; `numpy_version = 2.4.4`; `pyarrow_version = 23.0.1`;
`symbol = BTCUSDT`; the exact 244-date allowlist; the exact forbidden ranges.

Governance flags, all verified present and correct in every artefact:

```
v002_terminal_window_read = false
sealed_test_split_touched = false
test_rows_loaded          = 0
consumed_holdout_opened   = false
november_buffer_opened    = false
network_used              = false
data_acquisition_used     = false
```

Non-authorization flags, all `false` (verified): `ml_authorized`, `diagnostics_authorized`,
`strategy_authorized`, `signals_authorized`, `pnl_authorized`, `backtest_authorized`,
`live_authorized`, `exchange_write_authorized`.

## 4. Source partitions opened

**244 partitions per family, exactly the openable set** 2024-03-01 .. 2024-10-31 excluding
2024-10-01:

- `microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o` — `transact_time_ms`,
  `price` (decimal string), `row_index`; **340,447,363 rows read**.
- `microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s` — `feature_timestamp_ms`,
  `row_index`, `rolling_aggtrade_count_60s`, `rolling_quantity_sum_60s`,
  `rolling_quantity_mean_60s`; **340,447,363 rows read**.

Every opened Parquet was verified against its committed `.sha256` sidecar **before** its rows were
read; a mismatch would have raised and aborted. The full per-date sha256 maps are recorded in the
leakage-proof artefact under `normalized_partition_shas` and `feature_partition_shas` (244 entries
each).

Partition selection used an explicit 244-date allowlist and a fail-closed guard
(`assert_partition_allowed`) on every path construction. No glob or broad scan could reach a
forbidden partition: paths for forbidden dates are never constructed, and the guard raises
`Cf1ForbiddenPartitionError` if one is attempted.

## 5. Forbidden partitions — proof of non-opening

Recorded in the leakage proof and independently re-derived from the opened-date list:

| Range | Classification | Opened |
|---|---|---|
| 2024-10-01 | committed `1D_BOUNDARY_EMBARGO` | **false** |
| 2024-11-01 .. 2024-11-15 | `UNUSED_NON_RESERVE_BUFFER` | **false** |
| 2024-11-16 | committed embargo exclusion | **false** |
| 2024-11-17 .. 2024-11-30 | `PRE_V002_INTERNAL_HOLDOUT = CONSUMED` | **false** |
| 2024-12-01 .. 2025-02-28 | `V002_TERMINAL_WINDOW = UNTOUCHED_RESERVED` | **false** |
| 2025-02-14 .. 2025-02-28 | `V002_SEALED_TEST = UNTOUCHED_RESERVED` | **false** |

Proof fields: `october_1_opened = false`; `november_or_later_opened = false`;
`consumed_holdout_opened = false`; `terminal_opened = false`; `sealed_opened = false`;
`partitions_opened_count = 244`. The 2024-10-01 Parquet exists on disk and was **not** opened,
hashed for new scientific use, parsed, or listed for content. No forbidden directory was listed
for content; exclusion was established from committed metadata and the allowlist.

## 6. Timestamp-boundary proof

Emitted and validated **before any market-data file was opened**, over synthetic hard-coded rows
only (`market_data_opened = false`, `feature_data_opened = false`, `reserve_touched = false`),
ending `timestamp_boundary_proof_passed = true`. All 14 checks passed:

| Check | Result |
|---|---|
| `same_timestamp_greatest_row_index_tie` (105 vs 110 at exactly 10:00 → 110) | PASS |
| `interval_0900_1000_captures_boundary_jump` | PASS |
| `rv_h_1000_may_include_exact_1000_trade` | PASS |
| `interval_1000_1100_starts_from_110_no_recount` | PASS |
| `rv_target_1000_excludes_origin_time_jump` (first return exactly 0) | PASS |
| `trade_at_1100_included_in_target_1000_1100` | PASS |
| `feature_snapshot_1000_may_include_1000_row` | PASS |
| `boundary_trade_assigned_exactly_once` | PASS |
| `strict_lt_or_half_open_variant_fails_validation` | PASS |
| `covered_minute_predicate_right_closed` | PASS |
| `oct31_2200_valid_2300_invalid` | PASS |
| `november_1_partition_rejected_before_open` | PASS |
| `october_1_partition_rejected_before_open` | PASS |
| `allowlist_excludes_all_forbidden_partitions` | PASS |

The proof is deterministic: two consecutive invocations produce byte-identical check sets.

## 7. Leakage / split / coverage proof

`leakage_split_coverage_proof_passed = true`, `leakage_failure_reason = ""`. Validated **before**
any model fit or metric computation. Recorded contents:

- **Interval semantics:** every RV interval `(a, b]`; single operator `P_at(u)` with
  `source_transact_time_ms ≤ u` and greatest-`row_index` tie; HAR `(t − L, t]`; feature snapshot
  `feature_timestamp_ms ≤ t`. No live `[a, b)`, `P_minus`, `P_start`, strict `<` at an RV boundary,
  mixed operators, or left-limit terminal price exists anywhere in the AZ code (statically asserted
  by the boundary proof and the unit tests).
- **Covered-minute predicate:** `tau_{k-1} < ts <= tau_k`; **threshold 30 of 60**.
- **Embargo / purge:** `embargo_ms = 86,400,000` (1 calendar day); `purge_ms = 3,600,000` (1 hour,
  subsumed).
- **Block dates:** B1 2024-04-01..30; B2 2024-05-01..31; B3 2024-06-01..30; B4 2024-07-01..31;
  B5 2024-08-01..31; B6 2024-09-01..30; B7 2024-10-02..31.
- **`october_31_23_00_retained = false`** — the `2024-10-31T23:00` origin was dropped because its
  target endpoint `2024-11-01T00:00:00.000Z` lies outside execution access, and no November row
  was opened to score it.

## 8. Split, embargo, purge, and preprocessing scope

- **Expanding anchored walk-forward**, one fit per evaluation block, no refit inside a block, no
  random split, no shuffled CV, no resampling across time.
- **Training-origin selection:** all valid origins whose forward target ends at least 24 hours
  before the block start (`target_end_ms <= block_start_ms − 86,400,000`). Verified by unit test
  that no block's evaluation origins appear in its own training set and that every training origin
  satisfies the embargo inequality.
- **Preprocessing scope:** the microstructure log-feature mean and population standard deviation
  (`ddof = 0`) are fitted on that block's training origins only and then applied to the block. No
  global statistic spans training and evaluation; no evaluation block influences preprocessing
  fitted for itself; HAR log-variance regressors are left unstandardized.
- **No stitching:** carry-forward of prices and of the feature snapshot is reset at each
  accessible-segment start, so nothing is stitched across the 2024-10-01 embargo or an outer
  access edge. Segment A = 2024-03-01..2024-09-30; segment B = 2024-10-02..2024-10-31. An origin
  whose 168-hour HAR-week lookback would reach before its own segment start is invalidated rather
  than bridged.

## 9. Origin counts and invalid-origin reasons

| Quantity | Value |
|---|---|
| Candidate hourly origins | 5,854 |
| Valid paired origins | 5,516 |
| Invalid — `har_unavailable` | 336 |
| Invalid — `har_coverage_failure` | 2 |
| Zero-RV origins (retained, not dropped) | 0 |

`har_unavailable` is the deterministic 168-hour warmup at each segment start (segment A from
2024-03-01, segment B from 2024-10-02) plus the endpoint rule; `har_coverage_failure` marks two
origins whose HAR lookback contained an hourly interval below the 30-of-60 coverage threshold. No
origin was manually removed, and no origin was dropped for having `RV = 0`. Reason counts contain
no forbidden-row content.

Per-block valid evaluation origins — B1 720, B2 744, B3 720, B4 744, B5 744, B6 719, B7 550 — are
**all at or above the frozen minimum of 100**. Per-block training origins — 551, 1,271, 2,015,
2,735, 3,479, 4,223, 4,966 — are **all at or above the frozen minimum of 70**.

## 10. Paired baseline / augmented row identity

By construction both models consume the identical `OriginRow` set per block: the same target rows,
the same training origins, the same evaluation origins, the same split, estimator, preprocessing
scope, loss definition, and block assignment; they differ **only** by the three microstructure
columns. Because the augmented fit was refused by the numerical guard in every block, no scored
pair was produced, so paired-row identity is vacuously preserved and no asymmetric drop occurred.

## 11. Target-layer Parquet validation

`targets/cf1_realized_variance_target_layer_v001__v001__1784558563266__05fa63a8bf8c.parquet` —
**5,854 rows × 21 columns**, one compact row per candidate hourly origin. Columns:
`origin_timestamp_ms`, `origin_utc`, `origin_utc_date`, `evaluation_block`,
`target_end_timestamp_ms`, `target_valid`, `target_invalid_reason`, `covered_minute_count`,
`rv_target`, `log_rv_target`, `rv_h`, `rv_d`, `rv_w`, `rolling_aggtrade_count_60s`,
`rolling_quantity_sum_60s`, `rolling_quantity_mean_60s`, `feature_snapshot_timestamp_ms`,
`feature_snapshot_row_index`, `source_segment`, `in_reserve`, `november_or_later_touched`.

Verified on the frozen file:

- `max(origin_timestamp_ms)` = **2024-10-31T22:00:00Z** — the last potentially valid October origin.
- `max(target_end_timestamp_ms)` = **2024-10-31T23:00:00Z**.
- `any origin >= 2024-11-01` → **False**; `any target_end > 2024-11-01` → **False**.

**No 2024-11 timestamp appears anywhere in the target layer**, and no prediction rows exist.

## 12. Independent arithmetic validation of the frozen output

Permitted lightweight validation using the frozen compact output and identical formulas; it read
no new market data, altered no result, and is recorded as validation, not a second experiment.

Across all 5,516 valid origins in the frozen target layer:

```
max | ln(rolling_quantity_mean_60s) − ( ln(rolling_quantity_sum_60s) − ln(rolling_aggtrade_count_60s) ) | = 3.33e-14
mean| … |                                                                                                = 3.51e-15
```

This confirms to machine precision that the frozen third feature is an exact log-linear
combination of the other two, that the augmented design is structurally rank 6 of 7, and that the
recorded augmented condition numbers (1.019e+16 – 1.087e+16, against the frozen `1e10` threshold)
are the correct and unavoidable consequence — not an implementation artefact. The baseline design
was well conditioned throughout (3.418e+02 – 6.172e+02, full rank 4).

**No second scientific implementation was run to "confirm" the answer.** No metric was recomputed
by an alternate path; only artefact hashes were recomputed.

## 13. Verdict-route verification

The deterministic route was re-derived from the recorded fields: every block carries `ok = false`
with reason `augmented_condition_number_exceeded`, therefore the routing yields `CF1_INVALID_RUN`
before P1/P2/P3 are meaningful. The verdict recorded by the script equals that re-derived route.
`P4 = false`; `P1 = P2 = P3 = false` are uninitialised placeholders, not measured outcomes.

## 14. No plots, no exploratory output

Scan of the artefact root for `.png`, `.jpg`, `.svg`, `.ipynb`, `.html`: **empty**. No plot, no
notebook, no ad-hoc exploratory query, no subgroup/regime/date/volatility-quantile/feature-ablation
metric, and no second run exist. No interpretation was made before the artefact hashes and the
leakage/split proof validated.

## 15. Quality and test results

| Gate | Result |
|---|---|
| CF-1 targeted tests (4 modules) | 56 passed |
| `tests/research/microstructure` | all passed |
| Full `pytest` | 3342 passed, 2 failed, 1 skipped (83.8 s) |
| `ruff check` (8 AZ files) | All checks passed |
| `ruff format --check` (8 AZ files) | 8 files already formatted |
| `mypy --strict` | 12 errors, none in AZ code |
| `git diff --check` | clean |

**Baseline comparison.** AZ modified zero existing tracked files, so at gate time the tracked tree
was byte-identical to base `main`. The 2 `pytest` failures
(`tests/simulation/test_backtest_real_2026_03.py`, `KeyError: 'trade_count'` in
`src/prometheus/research/data/storage.py:232`) and the 12 `mypy --strict` errors (in
`labels_manifest_v002.py`, `multiday_feature_gate_checks.py`, `ml_baseline_models_v002.py`,
`ml_baseline_dataset_v002.py`, `feature_drift_v002.py`) are therefore the exact base-`main`
baseline. **AZ introduced 0 new failures and 0 new type errors** and added 56 passing tests.
Repo-wide `ruff format --check .` reports 235 pre-existing non-conforming files; none is an AZ file.

## 16. Boundary confirmations

- No network, API, Binance endpoint, WebSocket, credential, `.env`, `.mcp.json`, MCP, Graphify, or
  external reviewer was used; statically asserted by `test_cf1_no_network_v001.py` over all four
  AZ code files.
- No data was acquired or downloaded.
- No existing dataset, manifest, sidecar, split policy, feature schema, eligibility code, project
  lock, `pyproject.toml`, `uv.lock`, README, `current-project-state.md`, or prior report was
  modified.
- No Phase 4bn-AY file was modified.
- No local artefact was staged or committed; `data/research/` remains gitignored.
- `.claude/scheduled_tasks.lock` was never staged, modified, deleted, cleaned, or committed.
