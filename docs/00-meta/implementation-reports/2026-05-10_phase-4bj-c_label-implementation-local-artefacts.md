# Phase 4bj-C — Label Implementation + Local Label Artefact Generation

**Phase type:** code + docs + local gitignored label artefact generation
**Branch:** `phase-4bj-c/label-implementation-local-artefacts`
**Base:** `main` at the post-Phase-4bj-B merge-closeout state
**Phase 4bj-B merge commit (verified ancestor):**
`decc6624079ef786d5f360226303ae10a644a237`
**Code commit SHA recorded in label manifest:**
`f73a3db591bb0aa376b21ce0294f24de4acdfee4`
**Selected outcome:** SUCCESSFUL — label implementation merged at branch
level, local Stage-0 label artefacts generated for
`microstructure_labels_aggtrades_v001` BTCUSDT 2025-01-15, validation
PASS 100/100, all 11 upstream artefacts byte-identical pre/post, label
manifest remains `research_eligible=false / eligibility_gate_status=
pending`.

## 1. Phase header

Phase 4bj-C is the project's first code phase to materialise the
finalised Phase 4bj-B v001 label schema as actual local label artefacts.
It produces:

- four new source modules + a narrow `__init__.py` re-export update;
- seven new test files (one shared fixture module + six unit / static
  test modules);
- one local gitignored label parquet + paired `.sha256` sidecar;
- one local gitignored label manifest + paired `.sha256` sidecar;
- this main memo + a closeout memo;
- a narrow `current-project-state.md` paragraph addition + Current
  phase block update.

Phase 4bj-C does not authorise any successor phase, does not flip
`research_eligible` on any actual manifest, does not transition any
manifest's `eligibility_gate_status`, and does not produce a label
gate report or a label successor-state artefact.

## 2. Current state

Phase 4bj-B is merged. The 39-column v001 label schema is finalised.
The label family `microstructure_labels_aggtrades_v001` is locked at
policy level. No labels, label namespace, label manifest, label gate
report, or label successor-state existed at the start of this phase.
The Phase 4az / Phase 4bb-D / Phase 4bb-E / Phase 4bc / Phase 4bd-A /
Phase 4bd / Phase 4be / Phase 4bf-A / Phase 4bf / Phase 4bg-A / Phase
4bg-B / Phase 4bh-A / Phase 4bh-B / Phase 4bh / Phase 4bi-A / Phase
4bi-B / Phase 4bi-C / Phase 4bi-D / Phase 4bj-A / Phase 4bj-B governance
chain is preserved verbatim. All retained verdicts and project locks
remain unchanged.

## 3. Inputs reviewed

| Upstream artefact | SHA256 | Status |
|---|---|---|
| Feature parquet (Phase 4bh) | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` | OK (1,681,098 rows; 61 cols) |
| Feature manifest (Phase 4bh) | `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718` | `research_eligible=false / pending` |
| Phase 4bi-D successor-state JSON | `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a` | Stage-5 admissible (sibling marker only) |
| Phase 4bi-B feature-family gate report | `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988` | 70/70 PASS |
| Normalized parquet (Phase 4bd) | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` | OK |
| Original derived manifest (Phase 4bd) | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` | `research_eligible=false / pending` |
| Original raw manifest (Phase 4az) | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` | `research_eligible=false / pending` |
| Raw zip (Phase 4az) | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | OK |
| Phase 4bb-D raw gate report | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` | OK |
| Phase 4bf derived gate report | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` | OK |
| Phase 4bg-B successor-state JSON | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` | Stage-3 admissible (sibling marker only) |

All 11 SHAs verified byte-identical pre-run and post-run.

## 4. Scope

Phase 4bj-C is authorised to:

- add five new source modules at `src/prometheus/research/microstructure/`:
  `labels_schema.py`, `labels_io.py`, `labels_compute.py`,
  `labels_manifest.py`, `labels_validation.py`;
- narrowly update the package `__init__.py` to re-export the new
  Phase 4bj-C public API;
- add seven new test files at `tests/research/microstructure/`:
  `_labels_fixtures.py`, `test_labels_schema.py`, `test_labels_io.py`,
  `test_labels_compute.py`, `test_labels_manifest.py`,
  `test_labels_validation.py`, `test_labels_no_network.py`;
- generate exactly four local gitignored output files:
  - `data/microstructure/labels/microstructure_labels_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-labels-aggtrades-2025-01-15.parquet`
  - same path with `.sha256` suffix
  - `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v001.json`
  - same path with `.sha256` suffix;
- add this main memo and a closeout memo under
  `docs/00-meta/implementation-reports/`;
- narrowly update `docs/00-meta/current-project-state.md`.

## 5. Non-scope

Phase 4bj-C does NOT:

- run ML, build models, train classifiers, compute model scores,
  predictions, embeddings, or learned representations;
- create strategy logic, strategy signals, strategy actions, or
  position-state outputs;
- run backtests, compute PnL, MFE, MAE, R-multiple, equity curves,
  alpha, edge, or decision scores;
- create barrier labels, target-before-stop labels, execution-quality
  labels, or cross-symbol / cross-sectional labels;
- create 30s, 5m, or other horizons beyond `1s / 5s / 15s / 60s`;
- acquire data, call any Binance endpoint, open any WebSocket, use
  any credential, read or create `.env`, create `.mcp.json`, or enable
  MCP / Graphify;
- modify any source artefact (feature parquet, feature manifest, Phase
  4bi-B gate report, Phase 4bi-D successor-state, normalized parquet,
  derived manifest, raw manifest, raw zip, Phase 4bb-D gate report,
  Phase 4bf gate report, Phase 4bg-B successor-state);
- rerun the normalizer, raw eligibility gate, derived-family gate,
  feature kernel, or feature-family eligibility gate;
- create a label-family eligibility gate, label gate report, or label
  successor-state artefact;
- flip `research_eligible` on any manifest;
- transition `eligibility_gate_status` on any manifest;
- authorise Phase 4bj-D, 4bj-E, 4bj-F, 4bj-G, 4bb-F, 4bb-G, Phase 5,
  Phase 4 canonical, paper / shadow, live-readiness, deployment,
  exchange-write, production keys, authenticated APIs, private
  endpoints, user stream, or live WebSocket implementation;
- revise retained verdicts;
- change any project lock;
- amend M0;
- commit anything under `data/microstructure/`.

## 6. Phase 4bj-B dependency

Phase 4bj-C implements the Phase 4bj-B-locked v001 label schema verbatim:

- `dataset_family = microstructure_labels_aggtrades_v001`
- `dataset_version = v001`
- `label_schema_version = v001`
- 39 canonical columns (17 lineage / identity / metadata + 8 labels +
  14 support) in the exact Phase 4bj-B order
- 8 labels = 4 regression `forward_log_return_{1s,5s,15s,60s}` + 4
  classification `forward_direction_{1s,5s,15s,60s}`
- 14 support columns: 4 each of `reference_row_index_*`,
  `reference_timestamp_ms_*`, `horizon_censored_flag_*`, plus
  `label_invalid_price_flag` and `label_any_censored_flag`
- horizons `("1s", "5s", "15s", "60s")` paired with
  `(1000, 5000, 15000, 60000)` ms
- right-edge per-horizon censoring at `target_timestamp_ms >
  final_source_normalized_transact_time_ms`
- same-timestamp tie-break: largest `row_index` at that timestamp
- `forward_log_return_H = ln(reference_trade_price_H /
  anchor_trade_price)` with Decimal parsing, Decimal ratio, and
  `float64` cast at the log step only
- `forward_direction_H` strict sign from `forward_log_return_H` only:
  `+1` / `0` / `-1` / `null`
- `label_invalid_price_flag = true` when anchor or reference price is
  `<= 0`
- `label_any_censored_flag = OR(horizon_censored_flag_*)`
- no NaN / inf in any output column
- `chronological_split_policy` default `not_yet_defined`
- `label_config_hash` is SHA256 over canonical-JSON of the locked
  schema-policy fields plus the four upstream lineage SHAs

## 7. Implementation objective

Translate the Phase 4bj-B contract into runnable code and produce
exactly one local gitignored label parquet + manifest pair for the
`(BTCUSDT, 2025-01-15)` cell. Provide an offline read-only validator
that proves the generated artefacts conform to the contract.

## 8. Source files added / modified

| File | Status | Notes |
|---|---|---|
| `src/prometheus/research/microstructure/labels_schema.py` | added | 39-column constants + `build_label_config_hash` |
| `src/prometheus/research/microstructure/labels_io.py` | added | path discipline + atomic Parquet / JSON writers + sidecar writer |
| `src/prometheus/research/microstructure/labels_compute.py` | added | `compute_aggtrade_labels_v001` + `write_label_dataset_v001` |
| `src/prometheus/research/microstructure/labels_manifest.py` | added | `build_label_manifest_v001` with locked governance / boundary blocks |
| `src/prometheus/research/microstructure/labels_validation.py` | added | `validate_label_dataset_v001` (100 checks at full row scale) |
| `src/prometheus/research/microstructure/__init__.py` | narrow update | re-export Phase 4bj-C public API |

## 9. Test files added

| File | Tests | Notes |
|---|---|---|
| `tests/research/microstructure/_labels_fixtures.py` | helpers | `build_normalized_table`, `build_feature_table`, `write_temp_parquet` |
| `tests/research/microstructure/test_labels_schema.py` | 14 | constants, schema order, forbidden-substrings, hash determinism |
| `tests/research/microstructure/test_labels_io.py` | 13 | path discipline, atomic write, refuse-overwrite, sidecar |
| `tests/research/microstructure/test_labels_compute.py` | 12 | anchor, future-reference, tie-break, censoring, sign, invalid-price, write |
| `tests/research/microstructure/test_labels_manifest.py` | 14 | governance keys, boundary keys, locked values, validation rejections |
| `tests/research/microstructure/test_labels_validation.py` | 8 | happy path + 6 negative paths + missing-input path |
| `tests/research/microstructure/test_labels_no_network.py` | 12 | static no-network / no-credential scan over the 5 source modules |

Total new tests: **73** (all passing).

## 10. Public API implemented

Re-exported from `prometheus.research.microstructure`:

- `LabelSchemaError`, `LabelIOError`, `LabelManifestError`,
  `LabelValidationError`, `LabelComputationError`
- `LABEL_DATASET_FAMILY_V001`, `LABEL_DATASET_VERSION_V001`,
  `LABEL_SCHEMA_VERSION_V001`
- `LABEL_HORIZONS_V001`, `LABEL_HORIZON_MS_V001`
- `LABEL_NAMES_V001`, `LABEL_SUPPORT_COLUMN_NAMES_V001`,
  `LABEL_LINEAGE_COLUMNS_V001`
- `LABEL_SCHEMA_V001`, `LABEL_SCHEMA_COLUMNS_V001`
- `FORBIDDEN_LABEL_COLUMN_SUBSTRINGS`
- `ANCHOR_POLICY_V001`, `FUTURE_REFERENCE_POLICY_V001`,
  `DIRECTION_THRESHOLD_POLICY_V001`, `NULL_CENSORING_POLICY_V001`,
  `DTYPE_POLICY_V001`
- `build_label_config_hash`
- `LabelLineage`, `LabelComputationSummary`,
  `compute_aggtrade_labels_v001`, `write_label_dataset_v001`
- `derive_label_output_path`, `derive_label_manifest_output_path`
- `atomic_write_label_parquet`, `atomic_write_label_manifest`,
  `write_label_sha256_sidecar`
- `assert_label_path_under_data_microstructure`,
  `assert_output_path_under_labels`,
  `assert_label_manifest_path_under_manifests`
- `assert_no_forbidden_label_substrings`
- `build_label_manifest_v001`, `REQUIRED_LABEL_GOVERNANCE_KEYS`,
  `REQUIRED_LABEL_BOUNDARY_CONFIRMATIONS`,
  `FORBIDDEN_LABEL_GOVERNANCE_VALUES`
- `validate_label_dataset_v001`, `LabelValidationResult`,
  `LabelCheckResult`, `LabelCheckStatus`

## 11. Label schema implemented

The label parquet has the exact Phase 4bj-B 39-column canonical schema.
Column indices `0..16` are lineage / identity / metadata; `17..24` are
the 8 labels (regression first, then classification); `25..38` are the
14 support columns. Decimal-as-string columns are absent from the
output (the kernel parses anchor and reference prices from the
normalized parquet's `price` column without re-emitting them in label
rows). Float64 columns (`forward_log_return_*`) are nullable. Int8
columns (`forward_direction_*`) are nullable and constrained to
`{-1, 0, 1, null}`. Bool flags are non-nullable.

## 12. Label config hash policy

`build_label_config_hash` builds canonical JSON (sorted keys, ASCII,
no whitespace) over exactly:

- `dataset_family`, `dataset_version`, `label_schema_version`
- `label_list`, `support_column_list`
- `horizon_list`, `horizon_ms_list`
- `anchor_policy`, `future_reference_policy`,
  `direction_threshold_policy`, `null_censoring_policy`, `dtype_policy`
- `source_feature_manifest_sha256`, `source_feature_parquet_sha256`,
  `source_feature_successor_state_sha256`,
  `source_phase_4bi_b_gate_report_sha256`

and SHA256s the UTF-8 encoding. The resulting hex is recorded as the
`label_config_hash` field on every label parquet row (constant) and in
the label manifest's `label_config_hash` field.

Real-run hash for BTCUSDT 2025-01-15:
`fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00`

## 13. Label computation method

`compute_aggtrade_labels_v001`:

1. validates that the feature table has `row_index`, `agg_trade_id`,
   `feature_timestamp_ms`, `source_transact_time_ms`, that
   `row_index == np.arange(n_feat)`, and that
   `feature_timestamp_ms == source_transact_time_ms` per row;
2. validates that the normalized table has the same row count, the same
   `agg_trade_id` per row, the same `transact_time_ms` per row,
   `row_index == np.arange(n_norm)`, and is sorted by
   `transact_time_ms`;
3. parses every `price` string into `Decimal` (`getcontext().prec = 50`);
4. for each horizon `H`, computes
   `insert = np.searchsorted(norm_ts_ms, feat_ts_ms + H_ms,
   side='right')` and uses `insert - 1` as the reference row index;
   sets `horizon_censored_flag_H = true` when `target > final_ts`;
5. builds `forward_log_return_H` per row as
   `math.log(float(Decimal(reference_price) / Decimal(anchor_price)))`,
   skipping censored rows and rows with invalid (≤ 0) prices;
6. derives `forward_direction_H` strictly from the sign of
   `forward_log_return_H`;
7. sets `label_invalid_price_flag = true` and counts the row when
   anchor or any reference price is `<= 0` (defensive; the source
   normalized parquet had zero invalid prices);
8. sets `label_any_censored_flag = OR(horizon_censored_flag_*)`;
9. constructs the pyarrow Table with the canonical 39-column schema
   and per-row arrays in canonical column order;
10. returns `(table, LabelComputationSummary)` where the summary
    records `row_count`, `invalid_price_row_count`, and
    `censored_per_horizon`.

## 14. Future-reference method

For each horizon `H` and feature row `R`:

- `target_timestamp_ms = feature_timestamp_ms[R] + H_ms`
- `final_source_T = norm_ts_ms[-1]` (max in the normalized day)
- if `target > final_source_T`: censored; emit `null` for all five
  per-horizon columns and set the censored flag
- else: `insert = searchsorted(norm_ts_ms, target, side='right')`,
  `reference_row_index = insert - 1`
- `reference_timestamp_ms = norm_ts_ms[reference_row_index]`
- `reference_trade_price = Decimal(norm_prices[reference_row_index])`
- because `row_index == np.arange(n_norm)` and the rows are sorted by
  `(transact_time_ms ASC, row_index ASC)` (Phase 4bd guarantee),
  `insert - 1` is automatically the largest `row_index` at exactly
  that timestamp — same-timestamp tie-break is implicit and verified
  by the `test_future_reference_uses_largest_row_at_or_before_target`
  unit test

## 15. Censoring / null policy

- all feature rows are kept (no row dropping)
- per-horizon independent right-edge censoring
- when censored: `forward_log_return_H = null`,
  `forward_direction_H = null`, `reference_row_index_H = null`,
  `reference_timestamp_ms_H = null`, `horizon_censored_flag_H = true`
- when anchor price `<= 0`: `forward_log_return_*` and
  `forward_direction_*` are null for every horizon;
  `label_invalid_price_flag = true`; the row is counted once in
  `invalid_price_row_count`
- when a non-censored reference price `<= 0`: that horizon's
  `forward_log_return_H` and `forward_direction_H` are null;
  `label_invalid_price_flag = true`
- `label_any_censored_flag = OR(horizon_censored_flag_*)`
- no forward-fill across censored or invalid-price rows
- no NaN / inf in any output column (defensive non-finite check on
  computed log returns funnels to the invalid-price branch)

## 16. Manifest schema implemented

The label manifest is JSON-serialised with sorted keys, two-space
indent, and a trailing newline. Required fields per Phase 4bj-B:

- identity: `dataset_family`, `dataset_version`, `label_schema_version`
- source identity: `source_feature_dataset_family`,
  `source_feature_dataset_version`
- five source SHAs: `source_feature_manifest_sha256`,
  `source_feature_parquet_sha256`,
  `source_feature_successor_state_sha256`,
  `source_phase_4bi_b_gate_report_sha256`,
  `source_normalized_parquet_sha256`
- `label_config_hash`
- locked schema descriptors: `label_list`, `support_column_list`,
  `schema_column_list`, `horizon_list`, `horizon_ms_list`
- `row_count`, `column_count`
- policy descriptors: `nullable_tail_policy`, `reference_price_policy`,
  `direction_threshold_policy`, `dtype_policy`,
  `chronological_split_policy = "not_yet_defined"`
- per-run counts: `invalid_price_row_count`, `censored_per_horizon`
- `files: [{ path, sha256, size_bytes, row_count }]`
- governance labels (10 required keys; `ml=forbidden`,
  `strategy=forbidden`, `backtest=forbidden`,
  `acquisition=unauthorized`, `paper_shadow_live=forbidden`,
  `deployment=forbidden`, `exchange_write=forbidden`,
  `labels=allowed_by_phase_4bj_c`, `targets=allowed_by_phase_4bj_c`,
  `phase_id=4bj-C`)
- `boundary_confirmations` (13 keys, all `true`)
- `research_eligible: false` (locked)
- `eligibility_gate_status: "pending"` (locked)
- `code_commit_sha`, `created_at_unix_ms`, `created_at_utc`

## 17. Local gitignored label outputs

```text
data/microstructure/labels/microstructure_labels_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-labels-aggtrades-2025-01-15.parquet
data/microstructure/labels/microstructure_labels_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-labels-aggtrades-2025-01-15.parquet.sha256
data/microstructure/manifests/microstructure_labels_aggtrades_v001__v001.json
data/microstructure/manifests/microstructure_labels_aggtrades_v001__v001.json.sha256
```

All four files are gitignored under `.gitignore:85: data/microstructure/`
and are NOT committed.

## 18. Real Phase 4bj-C generation result

```text
label_parquet_path        : data/microstructure/labels/microstructure_labels_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-labels-aggtrades-2025-01-15.parquet
label_parquet_sha256      : ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26
label_parquet_size_bytes  : 66,073,234
label_parquet_row_count   : 1,681,098
label_parquet_column_count: 39
label_parquet_sidecar_sha : b9681e6b029901a7f8379909b4d7bc5a753fa07764104519c3eb10e9fb45c78b
label_manifest_path       : data/microstructure/manifests/microstructure_labels_aggtrades_v001__v001.json
label_manifest_sha256     : 181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3
label_manifest_size_bytes : 6,786
label_manifest_sidecar_sha: 3392a3364309e1392b8a790954db3ce5f68829911a477dfe825685fda3448a8d
label_config_hash         : fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00
invalid_price_row_count   : 0
censored_per_horizon      : {"1s": 9, "5s": 42, "15s": 118, "60s": 507}
first_row.row_index       : 0
first_row.agg_trade_id    : 2,516,301,323
first_row.feature_ts_ms   : 1,736,899,205,109
first_row.forward_log_return_1s   : 0.0001502245860383073
first_row.forward_direction_60s   : 1
last_row.row_index        : 1,681,097
last_row.agg_trade_id     : 2,517,982,420
last_row.forward_log_return_1s   : null (right-edge censored)
last_row.horizon_censored_flag_1s : true
last_row.horizon_censored_flag_60s: true
```

Compute kernel wall-clock: ~11.4 s. Atomic write: ~1.7 s. Validation
wall-clock: ~34.3 s.

## 19. Validation result

`validate_label_dataset_v001` returned `overall_status = pass` with
**100 / 100** checks PASS, 0 FAIL, 0 NOT_APPLICABLE. The validator
covers: sidecar SHA parity (parquet + manifest), 16 manifest-content
checks (including `label_list`, `support_column_list`,
`schema_column_list`, horizons, `label_config_hash`, every source SHA,
governance keys, boundary all-true, `files[]` parity), forbidden-
substring scan on column names, row-count parity vs feature parquet
and manifest, per-row alignment with the feature parquet
(`row_index`, `agg_trade_id`, `feature_timestamp_ms`,
`feature_timestamp_ms == source_transact_time_ms`), 11 lineage column
constancy checks plus `symbol` / `utc_date` constancy, 12
per-horizon-label finiteness + direction-domain + sign-match checks,
12 per-horizon-support censoring + reference-index + reference-
timestamp checks, OR-invariant for `label_any_censored_flag`, strict
bool for the three boolean columns, `censored_per_horizon` parity
between manifest and observed counts, `invalid_price_row_count`
parity, 17 lineage-column null-count checks, and 3 upstream-
immutability SHA checks. All 100 checks PASS.

## 20. Hash / immutability evidence

| Artefact | Pre-run SHA | Post-run SHA | Match |
|---|---|---|---|
| feature parquet | `618d9b86…` | `618d9b86…` | OK |
| feature manifest | `624e8c5e…` | `624e8c5e…` | OK |
| normalized parquet | `2b3d6978…` | `2b3d6978…` | OK |
| derived manifest | `f6f0d947…` | `f6f0d947…` | OK |
| raw manifest | `a371edd4…` | `a371edd4…` | OK |
| raw zip | `f560c2e5…` | `f560c2e5…` | OK |
| Phase 4bb-D raw gate report | `96f09159…` | `96f09159…` | OK |
| Phase 4bf derived gate report | `dd4e0c1c…` | `dd4e0c1c…` | OK |
| Phase 4bg-B successor-state | `8bcc7d01…` | `8bcc7d01…` | OK |
| Phase 4bi-B gate report | `aa5d29c2…` | `aa5d29c2…` | OK |
| Phase 4bi-D successor-state | `8176aa3f…` | `8176aa3f…` | OK |

All 11 upstream SHAs are byte-identical pre-run and post-run.

## 21. Boundary confirmations

| Boundary | Status |
|---|---|
| Label parquet writes under `data/microstructure/labels/` only | OK |
| Label manifest writes under `data/microstructure/manifests/` only | OK |
| Refuse-overwrite enforced for all four label output paths | OK |
| No tracked data file changed | OK |
| Label manifest `research_eligible=false / eligibility_gate_status=pending` | OK |
| Feature manifest `research_eligible` unchanged at `false` | OK |
| Original derived manifest `research_eligible` unchanged at `false` | OK |
| Raw manifest `research_eligible` unchanged at `false` | OK |
| No label gate report file created | OK |
| No label successor-state artefact created | OK |
| No ML / strategy / backtest / acquisition activity | OK |
| No network, credential, `.env`, `.mcp.json`, MCP, Graphify | OK |
| No mutation of feature parquet, feature manifest, normalized parquet, derived manifest, raw manifest, raw zip, Phase 4bb-D / 4bf gate reports, Phase 4bg-B / 4bi-B / 4bi-D artefacts | OK |
| No Phase 4 canonical, Phase 5, paper / shadow, live-readiness, deployment, exchange-write authorisation | OK |
| No retained verdict revision | OK |
| No project lock change | OK |
| No M0 amendment | OK |

## 22. What this phase proves

Phase 4bj-C demonstrates that the Phase 4bj-B v001 label schema is
implementable and runnable end-to-end against the real Phase 4bh
feature artefacts. The kernel produces a 39-column, 1,681,098-row
label dataset for the locked BTCUSDT 2025-01-15 cell. The artefacts
pass an independent, deterministic 100-check validator. All 11
upstream artefacts are byte-identical pre/post the run. The label
manifest preserves `research_eligible=false` and
`eligibility_gate_status=pending` exactly as Phase 4bj-B specified.

## 23. What this phase does not prove

Phase 4bj-C does NOT prove that the labels are predictive, profitable,
strategy-relevant, or admissible for ML, strategy, or backtest work.
Labels are not signals. Forward returns are not strategy returns.
Direction accuracy is not profitability. Cost-adjusted expectancy
requires a separately authorized strategy / backtest phase that
applies §11.6 = 8 bps HIGH per side verbatim. The label artefacts are
local gitignored research-time scaffolding only; no successor phase
is authorised, no label-family eligibility gate has been run, no label
successor-state artefact exists, and no Stage transition out of
Stage-0 has occurred for the label family.

## 24. Preserved boundaries

All boundaries from Phase 4az, Phase 4bb-D, Phase 4bb-E, Phase 4bc,
Phase 4bd-A, Phase 4bd, Phase 4be, Phase 4bf-A, Phase 4bf, Phase 4bg-A,
Phase 4bg-B, Phase 4bh-A, Phase 4bh-B, Phase 4bh, Phase 4bi-A, Phase
4bi-B, Phase 4bi-C, Phase 4bi-D, Phase 4bj-A, and Phase 4bj-B are
preserved verbatim. The retained verdict ledger
(H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1 / 5m thread
closure) is unchanged. All project locks (§11.6, §1.7.3, Phase 3p §4.7,
Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase
4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak M0 twelve-clause
gate + post-null cooldown + cooled-down families list, Phase 4al
refined no-rescue rule + §13 boundary + §14 hierarchy) are preserved.

## 25. Recommended future options

- **Primary:** remain paused.
- **Conditional next (NOT authorized by Phase 4bj-C):**
  Phase 4bj-D — Label Artefact Structural QA Memo, analysis-and-docs
  read-only.
- **Conditional if implementation ambiguity is found
  (NOT authorized):** Phase 4bj-B2 — Label Schema Clarification Memo,
  docs-only.
- **Conditional cleanup before repeated gates (NOT authorized):**
  Phase 4bb-F — Gate Report Output Path Hygiene.
- **Conditional raw policy marker (NOT authorized):**
  Phase 4bb-G — Raw Manifest Successor-State Recording.

Phase 4bj-C does NOT authorise any of the above.

## 26. Closeout / lock preservation

Phase 4bj-C is implementation-and-output only at branch level. No
successor phase is authorized. All boundaries listed in §21 hold.
The label artefacts remain local and gitignored. The label manifest
remains `research_eligible=false / eligibility_gate_status=pending`.
The 11 upstream artefacts remain byte-identical. The retained verdict
ledger and project locks are preserved verbatim. The recommended
state remains paused unless the operator separately authorises a
future phase.
