# Phase 4bh — AggTrades Feature Schema / Feature Computation Implementation

## Phase header

- **Phase id:** Phase 4bh
- **Phase title:** AggTrades Feature Schema / Feature Computation Implementation
- **Phase type:** code + docs + local gitignored feature artefact implementation, with one real feature-computation execution
- **Branch:** `phase-4bh/aggtrades-feature-computation`
- **Base:** `main` at `e99d2f3e5dcea2ceb8daa3428bbe72fd81d77293`
- **Phase 4bh-B merge ancestor:** `ba3c8d228557af85d1525e673ef869aaa53c2aff`
- **Code commit SHA recorded inside outputs:** `e99d2f3e5dcea2ceb8daa3428bbe72fd81d77293`
- **Status:** complete

## Current state

Phase 4bh implements exactly the Phase 4bh-B finalised feature schema as a code module, runs it once against the real Phase 4az → 4bb-D → 4bd → 4be → 4bf → 4bg-A → 4bg-B → 4bh-A → 4bh-B chain, and validates the result against the Phase 4bh-B contract. The acquired BTCUSDT 2025-01-15 derived family `microstructure_normalized_aggtrades_v001` is the canonical input. The feature artefacts written to disk are local and gitignored. **No upstream artefact was mutated.** **No `research_eligible` flag was flipped.** **No successor phase is authorised by Phase 4bh.**

## Inputs reviewed

- Phase 4bh-A — Feature-Boundary Design Memo
- Phase 4bh-B — Feature Schema Finalization Memo (locked schema and policies)
- Phase 4bg-B — Successor-State Recording (Stage-3 admissibility marker; SHA `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e`)
- Phase 4bf — Derived-Family Eligibility Gate (PASS report; SHA `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6`)
- Phase 4bd — Normalization Implementation (source normalized parquet + manifest)
- Phase 4bb-D — Raw Eligibility Gate (PASS report; SHA `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`)
- Phase 4az — Public AggTrades Archive Acquisition (raw zip + manifest, immutable)
- Phase 4ak — M0 governance, post-null cooldown, cooled-down families list, memo template
- Phase 4al — refined no-rescue rule, §13 boundary, §14 hierarchy
- Phase 3p §4.7 / Phase 3r §8 / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 4j §11 / Phase 4k / Phase 4p / Phase 4q / Phase 4v / Phase 4w governance

## Scope

Phase 4bh:

- implements exactly the Phase 4bh-B finalised feature schema in code under `src/prometheus/research/microstructure/`;
- adds tests for schema constants, I/O path discipline, kernel correctness, manifest construction, validation, and a static no-network / no-credential / no-MCP scan;
- runs the kernel exactly once against the real Phase 4bd normalized parquet for BTCUSDT 2025-01-15 (1,681,098 rows);
- writes the feature parquet, paired SHA256 sidecar, feature manifest, and paired SHA256 sidecar entirely under the gitignored `data/microstructure/` namespace;
- verifies pre/post immutability for all seven upstream artefacts (raw manifest, raw zip, normalized parquet, normalized manifest, Phase 4bb-D gate report, Phase 4bf gate report, Phase 4bg-B successor-state JSON);
- runs the Phase 4bh-B 135-check validation suite end-to-end and records `overall_status = pass`.

## Non-scope

Phase 4bh did NOT:

- acquire data; download data; call any Binance endpoint; open any WebSocket; consult any public endpoint, private endpoint, or authenticated REST; use any credential; read or create `.env`; create or read `.mcp.json`; enable MCP or Graphify;
- rerun the normalizer, raw eligibility gate, or derived-family gate; generate a new gate report; create a new normalized parquet, replacement derived manifest, replacement raw manifest, or any sibling manifest beyond the new feature manifest;
- create labels, targets, signals, ML artefacts, strategy logic, or backtests;
- compute PnL, MFE, MAE, R-multiple, equity, position state, alpha, edge, prediction, model score, decision score, entry / exit, or strategy output;
- modify any prior artefact under `data/microstructure/`;
- modify the Phase 4bg-B successor-state artefact;
- create a new successor-state artefact;
- create or modify any tracked manifest under `data/manifests/`;
- flip `research_eligible` to `True` on the actual feature manifest, the actual derived manifest, or the actual raw manifest;
- transition `eligibility_gate_status` out of `pending` on any actual manifest;
- authorise Stage-4 feature-cleared status, feature-family eligibility-gate execution, ML, strategy, or backtests;
- revise any retained verdict; change any project lock; amend M0;
- authorise Phase 4bi-A, Phase 4bi-B, Phase 4bi-C, Phase 4bi-D, Phase 4bj, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation.

## Phase 4bh-B schema dependency

Phase 4bh implements the Phase 4bh-B v001 contract verbatim:

- 4 trailing windows: `1s = 1000 ms`, `5s = 5000 ms`, `15s = 15000 ms`, `60s = 60000 ms` (deferred: `30s`, `5m`);
- 45 feature / quality columns (40 windowed + 3 time-context + 2 quality);
- 16 lineage / identity / metadata columns;
- 61-column total schema in canonical column order;
- aggressive-side rule: `is_buyer_maker = false → aggressive buy`, `is_buyer_maker = true → aggressive sell`;
- causal trailing window: `(T - window_ms, T]` with same-timestamp tie-break `row_index <= R`;
- log-return rule: prior reference price = last source row with `transact_time_ms <= T - window_ms`; null when no prior reference;
- Decimal-as-string for raw quantity sums / aggressive quantities / imbalances;
- Decimal-as-string nullable for rolling quantity means;
- `float64` nullable for aggressive flow ratios and log returns;
- 26 forbidden column-name substrings preserved verbatim;
- `feature_config_hash = sha256(canonical_json(config))` over locked schema fields.

## Implementation summary

Phase 4bh produces an event-aligned feature dataset with one feature row per source aggTrade row, ordered by `(transact_time_ms ASC, row_index ASC)`. The kernel is offline-only: pyarrow, numpy, and stdlib only. No networking library is imported. No credential is read.

The kernel uses vectorised numpy cumulative sums plus `numpy.searchsorted` to compute rolling counts, sums, and side-aware sums in O(N) time per window. Decimal-as-string outputs are produced in Python loops over scaled int64 values for deterministic precision. Float ratios and log returns are computed via numpy with explicit null handling for zero denominators and missing prior reference prices.

The kernel writes the feature parquet atomically (write-then-rename via `os.replace`) under `data/microstructure/features/microstructure_features_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/`. The paired `.sha256` sidecar is written next to the parquet. The feature manifest is written atomically under `data/microstructure/manifests/`. All writers refuse to overwrite an existing finalised file.

## Source files added or modified

- `src/prometheus/research/microstructure/features_schema.py` (new) — canonical schema constants, `FeatureComputationConfig`, `build_feature_config`, `compute_feature_config_hash`, forbidden-substring detector
- `src/prometheus/research/microstructure/features_io.py` (new) — read-only loaders, atomic Parquet/JSON writers, paired-SHA256 sidecar writer, path discipline (`assert_path_under_data_microstructure`, `assert_output_path_under_features`, `assert_manifest_output_path_under_manifests`)
- `src/prometheus/research/microstructure/features_compute.py` (new) — `compute_aggtrades_features` kernel, `write_feature_dataset`, causal trailing-window aggregation, aggressive-side rule, log-return rule
- `src/prometheus/research/microstructure/features_manifest.py` (new) — `build_feature_manifest`, `REQUIRED_FEATURE_GOVERNANCE_KEYS`, `REQUIRED_BOUNDARY_CONFIRMATIONS`
- `src/prometheus/research/microstructure/features_validation.py` (new) — `validate_feature_dataset`, `FeatureValidationResult`, `FeatureCheckStatus`
- `src/prometheus/research/microstructure/__init__.py` (narrow update) — re-exports the Phase 4bh public API and extends the package docstring with a Phase 4bh section

## Test files added or modified

- `tests/research/microstructure/_features_fixtures.py` (new) — shared fixture builder that produces a 19-column normalized parquet, a Phase 4bd-shaped derived manifest, and a Phase 4bg-B-shaped successor-state JSON inside `tmp_path`
- `tests/research/microstructure/test_features_schema.py` (new)
- `tests/research/microstructure/test_features_io.py` (new)
- `tests/research/microstructure/test_features_compute.py` (new)
- `tests/research/microstructure/test_features_manifest.py` (new)
- `tests/research/microstructure/test_features_validation.py` (new)
- `tests/research/microstructure/test_features_no_network.py` (new) — static scan over the five Phase 4bh source modules for forbidden imports and credential-shaped tokens

No prior test file was modified.

## Public API implemented

`prometheus.research.microstructure` exposes the Phase 4bh public API exactly as required by the brief:

- `FEATURE_SCHEMA_V001`
- `FEATURE_NAMES_V001`
- `FEATURE_WINDOWS_MS_V001`
- `FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS`
- `FeatureComputationConfig`
- `FeatureComputationResult`
- `build_feature_config`
- `compute_aggtrades_features`
- `write_feature_dataset`
- `build_feature_manifest`
- `validate_feature_dataset`

Plus supporting types and helpers: `FeatureLineage`, `FeatureSchemaError`, `FeatureIOError`, `FeatureComputationError`, `FeatureManifestError`, `FeatureValidationError`, `FeatureValidationResult`, `FeatureCheckStatus`, `FeatureCheckResult`, `LINEAGE_COLUMNS_V001`, `FEATURE_WINDOW_LABELS_V001`, `PER_WINDOW_FEATURE_TEMPLATES`, `DECIMAL_POLICY_V001`, `NULL_POLICY_V001`, `INVALID_WINDOW_POLICY_V001`, `REQUIRED_FEATURE_GOVERNANCE_KEYS`, `REQUIRED_BOUNDARY_CONFIRMATIONS`, `FORBIDDEN_FEATURE_GOVERNANCE_VALUES`, `compute_feature_config_hash`, `assert_no_forbidden_substrings`, `derive_feature_output_path`, `derive_feature_manifest_output_path`, `assert_output_path_under_features`, `assert_manifest_output_path_under_manifests`, `assert_path_under_data_microstructure`, `atomic_write_feature_parquet`, `atomic_write_feature_manifest`, `write_feature_sha256_sidecar`, `read_normalized_parquet`, `read_source_normalized_manifest`, `read_successor_state`, `hash_source_file`, `resolve_default_manifests_root`.

## Feature schema implemented

61 columns in canonical order:

1. **Lineage / identity / metadata (16):** `dataset_family`, `dataset_version`, `source_dataset_family`, `source_dataset_version`, `source_feature_schema_version`, `symbol`, `utc_date`, `agg_trade_id`, `row_index`, `feature_timestamp_ms`, `source_transact_time_ms`, `source_normalized_parquet_sha256`, `source_normalized_manifest_sha256`, `source_successor_state_sha256`, `source_phase_4bf_gate_report_sha256`, `feature_config_hash`.

2. **Windowed features (40 = 4 windows × 10):** for each of `1s`, `5s`, `15s`, `60s` — `rolling_aggtrade_count_<w>` (int64), `rolling_quantity_sum_<w>` (Decimal-as-string), `rolling_quantity_mean_<w>` (Decimal-as-string nullable), `rolling_aggressive_buy_quantity_<w>` (Decimal-as-string), `rolling_aggressive_sell_quantity_<w>` (Decimal-as-string), `rolling_aggressive_buy_count_<w>` (int64), `rolling_aggressive_sell_count_<w>` (int64), `rolling_aggressive_flow_ratio_<w>` (`float64` nullable), `rolling_aggressive_quantity_imbalance_<w>` (Decimal-as-string), `rolling_log_return_past_window_<w>` (`float64` nullable).

3. **Time-context (3):** `utc_hour` (int8), `utc_minute` (int8), `milliseconds_since_day_start` (int64).

4. **Data-quality (2):** `invalid_window_flag` (bool), `rolling_missing_window_flag` (bool).

## Feature computation semantics

- Trailing window `(T - window_ms, T]` with same-timestamp tie-break `row_index <= R`;
- aggressive-side rule per Binance aggTrades convention (`is_buyer_maker = false → aggressive buy`);
- empty-window policy: counts `0`, quantity sums `"0"`, quantity means `null`, ratio `null` if `buy + sell == 0`, log return `null` if no prior reference price exists;
- log-return prior reference = last row with `T <= T_i - window_ms`; if multiple rows share that timestamp, the largest `row_index` wins;
- `time-context`: `ms_since_day_start = T - day_start_ms`; `utc_hour = ms // 3_600_000`; `utc_minute = (ms % 3_600_000) // 60_000`;
- quality flags: `invalid_window_flag = false` and `rolling_missing_window_flag = false` for every row at v001 because the source manifest's `invalid_windows` is empty.

## Feature config hash

Deterministic SHA256 over canonical-JSON of locked fields (sorted keys, no spaces, ASCII):

- `feature_config_hash = 49b4ec1fd63688cc11d72ea7286af6efe2bad8ac5c29da0438c0f65d571f0c77`

## Real Phase 4bh feature execution result

- **Source normalized parquet:** `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet`
- **Source rows:** 1,681,098
- **Compute time:** 48.8 s wall-clock
- **Write time:** 3.8 s wall-clock
- **Validation overall:** `pass` — 135 / 135 checks pass

## Local gitignored output artefacts

All under `data/microstructure/` and covered by `.gitignore:85: data/microstructure/`. **None committed.**

| Artefact | Path | SHA256 | Size |
| --- | --- | --- | --- |
| feature parquet | `data/microstructure/features/microstructure_features_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-features-aggtrades-2025-01-15.parquet` | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` | 224,382,279 B |
| feature parquet sidecar | same path with `.sha256` suffix | (sidecar matches above) | 158 B |
| feature manifest | `data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json` | `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718` | 3,851 B |
| feature manifest sidecar | same path with `.sha256` suffix | (sidecar matches above) | 137 B |

## Feature manifest summary

- `dataset_family = microstructure_features_aggtrades_v001`
- `dataset_version = v001`
- `feature_schema_version = v001`
- `symbol = BTCUSDT`, `utc_date = 2025-01-15`
- `feature_list` matches `FEATURE_NAMES_V001` exactly (45 items)
- `window_list = ["1s", "5s", "15s", "60s"]`
- `window_ms_list = [1000, 5000, 15000, 60000]`
- `row_count = 1681098`
- `invalid_windows = []`
- `feature_config_hash = 49b4ec1f…571f0c77`
- `source_normalized_manifest_sha256 = f6f0d947…21897b8e9b9`
- `source_normalized_parquet_sha256 = 2b3d6978…01778808f6fa`
- `source_successor_state_sha256 = 8bcc7d01…0446dddedb39e`
- `source_phase_4bf_gate_report_sha256 = dd4e0c1c…710bd4ae6`
- `governance_labels = { phase_id: "4bh", feature_computation: "allowed_by_phase_4bh", labels: "forbidden", ml: "forbidden", strategy: "forbidden", backtest: "forbidden", acquisition: "unauthorized", stop_trigger_domain: "trade_price_backtest_candidate" }`
- `research_eligible = false`
- `eligibility_gate_status = pending`
- `code_commit_sha = e99d2f3e5dcea2ceb8daa3428bbe72fd81d77293`
- `boundary_confirmations`: all 11 keys true (`no_labels`, `no_targets`, `no_signals`, `no_ml`, `no_strategy`, `no_backtest`, `no_acquisition`, `no_network`, `no_credentials`, `no_manifest_mutation`, `no_source_artefact_mutation`)

## Validation evidence

`validate_feature_dataset` ran end-to-end against the real feature parquet, feature manifest, and source normalized parquet:

- 135 checks total, 0 failures
- sidecar SHA matches feature parquet bytes
- sidecar SHA matches feature manifest bytes
- 61-column schema and order match `FEATURE_SCHEMA_V001`
- `feature_list / window_list / window_ms_list / feature_config_hash / source_*_sha256` all match
- governance labels keys present and values locked
- boundary confirmations all true
- `files[0].sha256` matches recomputed parquet SHA, `files[0].row_count` matches manifest `row_count`
- row count parity: parquet rows = manifest `row_count` = source rows = 1,681,098
- lineage hash columns constant across all rows
- `agg_trade_id`, `row_index`, `source_transact_time_ms` parity with source
- `feature_timestamp_ms == source_transact_time_ms` for every row
- count columns non-negative int64
- ratio columns null or in `[0, 1]` and finite
- Decimal-as-string columns parse via `Decimal(...)` for every value
- `utc_hour ∈ [0, 23]`, `utc_minute ∈ [0, 59]`, `milliseconds_since_day_start ∈ [0, 86_399_999]`
- `invalid_window_flag` and `rolling_missing_window_flag` are strict bool

## Hash / immutability evidence

Pre/post-run SHA256 for every upstream artefact, recomputed inside the orchestrator:

| Artefact | SHA256 (pre) | SHA256 (post) | Match |
| --- | --- | --- | --- |
| original derived manifest | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` | MATCH |
| normalized parquet | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` | MATCH |
| raw manifest | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` | MATCH |
| raw zip | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | MATCH |
| Phase 4bb-D gate report | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` | MATCH |
| Phase 4bf gate report | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` | MATCH |
| Phase 4bg-B successor-state | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` | MATCH |

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant was preserved end-to-end (never invoked by Phase 4bh).

## Boundary confirmations

All 11 keys recorded `true` in the feature manifest:

- `no_labels`
- `no_targets`
- `no_signals`
- `no_ml`
- `no_strategy`
- `no_backtest`
- `no_acquisition`
- `no_network`
- `no_credentials`
- `no_manifest_mutation`
- `no_source_artefact_mutation`

## Feature-stage interpretation

Per Phase 4bh-A's feature-stage model (mirrors the Phase 4ba data-eligibility ladder):

- **Feature Stage-0 schema designed** — Phase 4bh-A.
- **Feature Stage-1 implementation merged** — Phase 4bh implementation.
- **Feature Stage-2 feature artefacts exist locally with manifest** — reached by Phase 4bh.
- **Feature Stage-3 structurally QA-passed** — NOT reached by Phase 4bh. Requires a separately authorised future Phase 4bi-A.
- **Feature Stage-4 feature-family eligibility-gate-passed** — NOT reached.
- **Feature Stage-5 research-use / ML-use decision** — NOT reached.

## What this phase proves

- The Phase 4bh-B locked feature schema is implementable, runnable, and produces a deterministic 61-column event-aligned feature dataset for the BTCUSDT 2025-01-15 normalized aggTrades input.
- Causal windowing semantics, aggressive-side conventions, log-return prior-reference logic, and Decimal-as-string formatting are correct under the Phase 4bh-B test contract.
- The kernel preserves all seven upstream artefacts byte-for-byte and the validator's 135 checks all pass.
- Path discipline restricts every write under `data/microstructure/`; no tracked file outside the Phase 4bh source / test / docs scope was modified.
- Whole-repo `ruff check .` passes; whole-repo `mypy` strict passes (`Success: no issues found in 106 source files`); whole-repo `pytest` reports `1372 passed, 2 failed` where the two failures are the unchanged pre-existing simulation `KeyError: 'trade_count'` failures.

## What this phase does not prove

- The feature artefacts are NOT structurally QA-passed at Phase 4bi-A scope.
- The feature family is NOT research-use approved or ML-use approved.
- No edge claim is made.
- No baseline-superiority claim is made.
- No predictive validity is established.
- No labels, targets, or signals exist.
- No ML model is trained.
- No strategy is implemented.
- No backtest is run.
- No paper / shadow / live-readiness path is implied.
- Stage-4, Stage-5, paper / shadow / live, exchange-write, production keys, authenticated APIs, private endpoints, user stream, and live WebSocket all remain unauthorised.

## Preserved boundaries

- Original raw manifest remains `research_eligible=false / eligibility_gate_status=pending`.
- Original derived manifest remains `research_eligible=false / eligibility_gate_status=pending`.
- New feature manifest is `research_eligible=false / eligibility_gate_status=pending`.
- Phase 4bg-B successor-state JSON is unchanged.
- Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved.
- M0 (Phase 4ak) twelve-clause gate, post-null cooldown, cooled-down families list, and memo template preserved.
- Phase 4al refined no-rescue rule, §13 boundary, §14 hierarchy preserved.
- §11.6 = 8 bps per side, round-trip = 16 bps preserved.
- §1.7.3 0.25% / 2× / one-position / mark-price stops preserved.
- Phase 3p §4.7 / Phase 3r §8 / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 4j §11 / Phase 4k / Phase 4p / Phase 4q / Phase 4v / Phase 4w preserved.

## Recommended future options

- **Primary (NOT authorised by Phase 4bh):** remain paused.
- **Conditional next (NOT authorised by Phase 4bh):** Phase 4bi-A — Feature Artefact Structural QA Memo (analysis + docs; verifies 61-column schema, row-count parity, lineage SHA constancy, Decimal-as-string parseability, ratio range, log-return causality structure on the real feature parquet at descriptive QA scope; does not authorise Stage-3 feature transition).
- **Conditional later (NOT authorised by Phase 4bh):** Phase 4bi-B — Feature-Family Eligibility-Gate Design + Execution; Phase 4bi-C — Research-Use Decision; Phase 4bi-D — Successor-State Recording.
- **Conditional cleanup (NOT authorised by Phase 4bh):** Phase 4bh-C — Feature Schema Finalization Review / Red-Team Memo; Phase 4bb-F — Gate Report Output Path Hygiene; Phase 4bb-G — Raw Manifest Successor-State Recording.

Phase 4bh does NOT authorise any successor.

## Closeout / lock preservation

All retained verdicts preserved verbatim:

- H0 FRAMEWORK ANCHOR
- R3 BASELINE-OF-RECORD
- R1a / R1b-narrow RETAINED — NON-LEADING
- R2 FAILED — §11.6
- F1 HARD REJECT
- D1-A MECHANISM PASS / FRAMEWORK FAIL
- 5m thread OPERATIONALLY CLOSED per Phase 3t
- V2 HARD REJECT — terminal for V2 first-spec
- G1 HARD REJECT — terminal for G1 first-spec
- C1 HARD REJECT — terminal for C1 first-spec

All Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak M0 + post-null cooldown + cooled-down families list + memo template, Phase 4al refined no-rescue + §13 + §14, Phase 4am §11.A audit findings, Phase 4an inventory result, Phase 4ao harmonization result, Phase 4ap forensic plan, Phase 4aq computation result, Phase 4ar interpretation result, Phase 4as mechanism-map result, Phase 4at availability / capture-feasibility result, Phase 4au capture-design result, Phase 4av implementation-plan result, Phase 4aw scaffold result, Phase 4ax aggTrades-only collector skeleton, Phase 4ay authorisation-boundary, Phase 4az acquisition + integrity, Phase 4ba eligibility-gate review, Phase 4bb-A structural QA, Phase 4bb-B execution-plan, Phase 4bb-C eligibility-gate primitive, Phase 4bb-D real-run gate result, Phase 4bb-E successor-state policy, Phase 4bc normalization design, Phase 4bd-A normalization implementation plan, Phase 4bd normalization implementation, Phase 4be derived structural QA, Phase 4bf-A derived gate design, Phase 4bf derived gate implementation + run, Phase 4bg-A research-eligibility decision, Phase 4bg-B successor-state recording, Phase 4bh-A feature-boundary design, and Phase 4bh-B feature-schema finalization governance preserved verbatim.

**No project lock changed by Phase 4bh.** **No retained verdict revised by Phase 4bh.** **No successor authorised by Phase 4bh.** **Recommended state: remain paused.**
