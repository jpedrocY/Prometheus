# Phase 4bn-AF — Code-Only ML Dataset Builder Skeleton

## 1. Purpose

This phase implements a **code-only** ML dataset builder skeleton for the
conservative pre-v002-only path, using **synthetic in-memory fixtures and offline
tests only**. It converts three prior governance artefacts into executable,
tested, pure-code invariants:

- the **Phase 4bn-AC** source contract
  (`microstructure_ml_dataset_aggtrades_pre_v002_contract_v001`) — source scope,
  manifest / config / gate-report hashes, the 45-column feature allowlist, the
  forbidden model-matrix columns, target / horizon, filtering, alignment,
  train-only transforms, and the output-namespace posture;
- the **Phase 4bn-AD** builder-readiness controls — no-data-I/O and fail-closed
  design, a new pre-v002-specific skeleton (not a reuse of the v002-terminal
  loader), and the inert output-namespace string;
- the **Phase 4bn-AE** amendment-001 pre-registration layer — evaluation claim
  scope, mandatory metric registry, overlapping-label dependence policy,
  date/month-block reporting, calibration and cost-realism schema, pre-registered
  success thresholds, the strategy/PnL non-authorization boundary, and the
  skeleton amendment obligations.

The skeleton reads no local data, creates no local data, writes no Parquet,
mutates no manifest, produces no `data/research` / `data/microstructure` artefact,
creates no output namespace, and calls no endpoint. It is a set of pure
validators, planners, and proof-schema builders exercised against synthetic
objects.

---

## 2. Authority and repository state

- **Authorized by:** the operator, as Phase 4bn-AF, following the Phase 4bn-AE
  decision
  `RECOMMEND_AUTHORIZE_CODE_ONLY_ML_DATASET_BUILDER_SKELETON__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Branch:** `phase-4bn-af/code-only-ml-dataset-builder-skeleton`.
- **Base `main` SHA:** `3e0e26e00bad5bce4c239d9157349b4acd296702`
  (`docs(phase-4bn-ae): finalize merge closeout shas`).
- **Pre-branch sync:** `HEAD == main == origin/main == 3e0e26e0…` verified.
- **Predecessor chain on `main`:** Phase 4bn-AE SHA-finalization `3e0e26e`,
  merge-closeout `ee067f1`, merge `daae192`, branch `41fb7c1`.
- **Remote:** `https://github.com/jpedrocY/Prometheus.git`.
- **Gitignored namespaces:** `data/microstructure/` (`.gitignore:85`),
  `data/research/` (`.gitignore:88`).

---

## 3. Phase type and strict scope

- **Phase type:** code-only / synthetic-fixture-only / no-data-read / no-output /
  ML dataset builder skeleton / amended-contract encoding / offline tests.
- **Tier:** Tier 1 — Full Phase per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (it converts the
  source contract, readiness decision, and pre-registration amendment into
  executable invariants; an error could later permit data reads, forbidden
  columns, invalid split handling, leakage, improper evaluation interpretation,
  or accidental output creation).

**Strict scope (all enforced):** source + tests + docs only; no data read; no
data created; no inspection of any file under `data/microstructure/` or
`data/research/`; no future output namespace created; no split file / research
matrix / ML dataset / ML config / manifest / gate report / sidecar created; no
training / scoring / predictions / diagnostics / strategy / signals / PnL /
backtests; no `research_eligible` flip; no `eligibility_gate_status` transition;
no `chronological_split_policy` set; no invocation of the Phase 4aw
`flip_research_eligible(...)` invariant; no successor authorization.

---

## 4. Evidence base and input boundary

Written from **committed docs + committed source/tests only**. No local artefact
under `data/microstructure/` or `data/research/` was read. The README is treated
as potentially stale and was not used as a current-state authority.

Committed source grounding (read-only): `pre_v002_split_policy.py` (the sole
split authority; lowercase split labels `train`/`validation`/`holdout`/`embargo`),
`features_schema.py` / `features_schema_v002.py` (the 45 causal feature columns
via `FEATURE_NAMES_V002`; the 17-column `LINEAGE_COLUMNS_V002`),
`labels_schema_v002.py` (label / support columns, `DIRECTION_THRESHOLD_POLICY_V002`,
the primary censored flag and invalid-price flag names), and
`ml_baseline_design_v002.py` (read-only, for the **full** rejected v002-terminal
config-hash values `819cfa7a…` / `352bad41…` and the standardization / imputation
rule strings — **not imported**, to avoid pulling in the v002-terminal split
policy). The three new modules import only the standard library plus the inert
schema-constant modules and the inert split-policy artefact.

---

## 5. Phase 4bn-AC source contract encoded

`pre_v002_ml_dataset_contract.py` encodes: contract name + amendment id; symbol /
market / source family; segment dates 2024-03-01..2024-11-30; expected 275/275/275
partition counts and 400,001,695 rows; the eight expected manifest / config /
gate-report SHA256s; the rejected v002-terminal config hashes (full values +
prefixes); the 45-column feature allowlist (imported from the committed schema,
not re-typed); the 17 excluded lineage columns; the forbidden model-matrix
substrings; the forbidden raw-price columns; the strict alignment keys; the
primary `forward_direction_15s` target, `forward_log_return_15s` support, censored
flag, and `label_invalid_price_flag`; the train-only transform rule constants; the
split-policy binding reference and the 214/1/45/1/14 expected split counts.

---

## 6. Phase 4bn-AD skeleton-readiness controls encoded

- **No-data-I/O:** no import-time side effects beyond constant assertions; no
  filesystem read/write calls; no path resolution; no network; validators accept
  only in-memory synthetic arguments. Proven by test category 13 (monkeypatched
  `open` / `Path.mkdir` / `Path.read_text` / `Path.write_text` / `Path.open` /
  `pyarrow.parquet.read_table` / `write_table` all raise, then the full public
  surface runs without tripping them).
- **Inert output namespace:** `OUTPUT_NAMESPACE_PATH` is a string constant; it is
  never created, resolved, or written. Proven by test category 14.
- **New pre-v002-specific skeleton:** the v002-terminal loader
  `ml_baseline_dataset_v002.py` is neither imported, wrapped, nor copied.
- **Fail-closed:** every validator raises `PreV002MlDatasetError` on any
  out-of-segment / v002 / sealed date, manifest / config / gate mismatch (incl.
  the rejected `819cfa7a…` / `352bad41…`), wrong partition count, forbidden
  column, raw-price column, key-alignment mismatch, or non-train transform fit.

---

## 7. Phase 4bn-AE amendment encoded

`MANDATORY_METRICS` (21 entries), `METRIC_GRANULARITIES`
(`aggregate`/`utc_month`/`utc_date`), `ROW_LEVEL_METRICS_DESCRIPTIVE_ONLY=True`,
`DECISION_BLOCK_UNITS=("utc_date","utc_month")`, `DECIMATION_STRIDE=None` +
`DECIMATION_POLICY="reserved_not_adopted"`, `HIGH_CONFIDENCE_THRESHOLD=0.8`,
`LOCKED_COST_BPS_PER_SIDE=8.0` / `LOCKED_ROUND_TRIP_COST_BPS=16.0`, the success
thresholds (`+2.0` pp accuracy / `+1.0` pp balanced accuracy / `+0.03` macro-F1),
`CONTINUE_FOLLOWUP_CATEGORIES`, `CLAIM_SCOPE_ALLOWED` / `CLAIM_SCOPE_FORBIDDEN`,
and `NON_AUTHORIZATION_FLAGS` (all False). `validate_evaluation_schema` enforces
these against a synthetic schema object.

---

## 8. Source modules created

- `src/prometheus/research/microstructure/pre_v002_ml_dataset_contract.py` —
  pure constants + 5 frozen dataclasses (`ContractIdentity`, `SourceScope`,
  `ManifestBinding`, `EvaluationPreregistration`, `NonAuthorizationPosture`);
  imports stdlib + the inert schema modules only.
- `src/prometheus/research/microstructure/pre_v002_ml_dataset_builder.py` —
  `PreV002MlDatasetError` + 12 pure validators/planners + `FilterResult`,
  `TransformPlan`, `SkeletonPlan`; imports stdlib + the contract module + the
  split-policy artefact only.
- `src/prometheus/research/microstructure/pre_v002_ml_dataset_proof.py` —
  7 proof dataclasses + `build_dataset_builder_proof` + `validate_dataset_builder_proof`;
  imports stdlib + the contract module + the split-policy artefact + the builder's
  error type only.

---

## 9. Contract constants and metadata

See §5. All hash values are the full committed values from the Phase 4bn-AC memo
and `ml_baseline_design_v002.py`. Import-time assertions verify: 45 allowed
features (unique); 17 excluded lineage columns; primary target /horizon; 275
partition counts; 400,001,695 rows; cost locks; all non-authorization flags
False; and that no allowed feature column contains a forbidden substring.

## 10. Feature allowlist and forbidden-column enforcement

`validate_feature_allowlist` requires exactly the 45 columns (order-independent
input; canonical order returned) and fails closed on missing / extra / duplicate
/ forbidden. `find_forbidden_columns` (non-raising) and `scan_forbidden_columns`
return hits; `assert_no_forbidden_columns` raises. Forbidden = lineage columns,
label/support columns, `FORBIDDEN_MODEL_MATRIX_SUBSTRINGS` matches, or raw-price
columns.

## 11. Source-scope validation

`validate_source_scope` requires symbol=BTCUSDT, market=binance_usdm_futures,
source_family=aggTrades, dates 2024-03-01/2024-11-30; rejects wrong partition
counts (≠275), wrong row count, and the danger flags (`contains_v002_terminal`,
`contains_sealed_test`, `full_envelope`, `private_source`, `authenticated_source`,
`external_source`); fails closed on missing critical keys.

## 12. Manifest/hash/gate validation

`validate_manifest_hashes` verifies the three manifest SHA256s, the feature and
label config hashes, optional gate-report SHA256s and partition counts; rejects
the v002-terminal `819cfa7a…` / `352bad41…` config hashes by full value and
prefix; fails closed on any mismatch or missing critical hash.

## 13. Split-policy binding

`assign_split` delegates to `pre_v002_split_policy.split_for_timestamp_ms`,
returning `train`/`validation`/`holdout`/`embargo` and hard-raising (wrapped as
`PreV002MlDatasetError`) for out-of-segment / v002 / sealed dates.
`should_drop_for_split` drops embargo only. `validate_no_boundary_crossing` uses
the Phase 4bn-AA `is_earlier_split_boundary_crossing` helper for the active
horizon; holdout never crosses; embargo rows fail closed.

## 14. Target filtering

`filter_targets` drops (never imputes) rows by precedence invalid_price →
censored → null_direction → null_log_return, returning `FilterResult` with
`valid_rows` and `dropped_by_reason`. The input mappings are never mutated.

## 15. Strict alignment validation

`assert_strict_alignment` compares mandatory keys (`row_index`, `agg_trade_id`,
`feature_timestamp_ms`, `source_transact_time_ms`) plus optional `symbol` /
`utc_date` per row in order; any length, value, or order mismatch fails closed;
no join repair / reorder / fill / tolerance merge / heuristic dedup.

## 16. Train-only transform planning

`plan_train_only_transform` returns an inert `TransformPlan` fit on the `train`
split only (standardization rule + epsilon, fixed-zero fit-free imputation,
boolean flags unstandardized, applied to validation/holdout). Any non-train
`fit_split` (validation/holdout/test/embargo) fails closed.

## 17. Evaluation schema / metric registry

`validate_evaluation_schema` enforces the full mandatory metric registry, the
three granularities, the descriptive-only flag, the dependence caveat, the null
decimation stride, the pre-registered success constants, the calibration schema,
the cost-descriptive fields, and the no-strategy boundary.

## 18. Dependence / date-month block schema

Encoded as `ROW_LEVEL_METRICS_DESCRIPTIVE_ONLY`, `DECISION_BLOCK_UNITS`,
`DECIMATION_STRIDE=None` / `DECIMATION_POLICY="reserved_not_adopted"`, and the
`dependence_caveat` / `granularities` schema fields required by
`validate_evaluation_schema` and the proof's `EvaluationPreregistrationProof`.

## 19. Calibration / confidence-tail schema

Encoded via `HIGH_CONFIDENCE_THRESHOLD=0.8`, the mandatory metrics
`calibration_reliability_table` / `high_confidence_tail_size` /
`high_confidence_tail_accuracy`, and the proof's `calibration_schema_present` /
`high_confidence_threshold` fields.

## 20. Cost-realism descriptive schema

Encoded via `LOCKED_COST_BPS_PER_SIDE` / `LOCKED_ROUND_TRIP_COST_BPS`, the
`cost_descriptive_fields` schema requirement, and the proof's
`cost_descriptive_fields_present` / `locked_round_trip_cost_bps` fields —
descriptive only; authorizes no trading rule / label / PnL / backtest.

## 21. Success / continue / kill constants

`SUCCESS_ACCURACY_UPLIFT_PP=2.0`, `SUCCESS_BALANCED_ACCURACY_UPLIFT_PP=1.0`,
`SUCCESS_MACRO_F1_UPLIFT=0.03`, and `CONTINUE_FOLLOWUP_CATEGORIES` (four bounded
categories) — frozen constants, encoded and asserted against synthetic fixtures;
not run against data.

## 22. Proof schema and non-authorization flags

`pre_v002_ml_dataset_proof.py` defines `SplitProof`, `AlignmentProof`,
`FilteringProof`, `EvaluationPreregistrationProof`, `BudgetPreflightPlaceholder`
(interface-shape only; `is_placeholder=True`, `measured_disk=False`,
`wrote_output=False`, Phase 4bn-L caps echoed), `NonAuthorizationProof` (all False),
and `DatasetBuilderProof`. `validate_dataset_builder_proof` fails closed on wrong
split counts, `test_rows_loaded≠0`, v002/sealed access, non-empty forbidden scan,
missing metrics/granularities, imputed targets, a non-placeholder budget
preflight, any True non-authorization flag, or a created output namespace.

## 23. No-data-I/O controls

Proven by test category 13: with `builtins.open`, `pathlib.Path.mkdir/read_text/
write_text/open`, and `pyarrow.parquet.read_table/write_table` all monkeypatched
to raise, the entire public surface executes without tripping any guard.

## 24. No-output-namespace proof

Proven by test category 14: the exact future namespace
`data/research/microstructure/ml_datasets/pre_v002_contract_v001/` does not exist
before or after exercising the full surface, and the skeleton never creates it.

## 25. Tests added

`tests/research/microstructure/test_phase4bn_af_pre_v002_ml_dataset_builder_skeleton.py`
— **97 offline, synthetic tests** across the 15 required categories (import/no
side-effects, contract constants, feature allowlist, manifest/hash/gate binding,
source scope, split assignment, boundary-crossing/horizon, target filtering,
strict alignment, train-only transform planning, amendment encoding, proof schema,
no-data-I/O, no-output-namespace, public-API stability).

## 26. Validation commands and results

- `ruff check` (3 modules + test) → **All checks passed** (after removing one
  unused import).
- `pytest …test_phase4bn_af…` → **97 passed**.
- `mypy` (3 new modules) → **0 direct errors in the new modules**; 29 pre-existing
  unrelated errors surface transitively from committed sibling modules
  (`features_compute.py`, `features_compute_v002.py`,
  `multiday_feature_gate_checks.py`) — identical set reproduced by
  `mypy pre_v002_split_policy.py` alone (a committed module), as documented by the
  Phase 4bn-AA closeout. The new modules introduced none.
- `git diff --check` → clean.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`; `data/research/`
  → `.gitignore:88`.
- No acquisition / gate / ML / diagnostics / backtest script run; no endpoint;
  no local data read or created.

## 27. Remaining blockers before data reads

Code-level builder bound to the passed gates (`3452fd9d…` / `db731d1b…` /
`ffb5b09…`), manifests, hashes, and the split artefact (this skeleton encodes the
bindings as validators over synthetic inputs; it does not yet read data); leakage
proof + Phase 4bn-L budget preflight bound into a **data-reading** builder;
separate data-read authorization (`source_admissible_for_data_read=false`).

## 28. Remaining blockers before real dataset builder

The Phase 4bn-AD readiness decision (done — code-only first); this passing
code-only skeleton (done); leakage proof + budget preflight designed into the
data-reading builder; separate builder authorization
(`source_admissible_for_dataset_builder=false`).

## 29. Remaining blockers before ML training

All data-read + dataset-builder blockers; target/horizon/filtering locked (done)
and the evaluation/dependence/success-kill layer pre-registered (Phase 4bn-AE,
done) and now encoded (this phase); a committed end-to-end pre-v002 trainer (does
**not** exist); separate ML authorization (`ml_authorized=false`).

## 30. Selected next recommendation

`RECOMMEND_AUTHORIZE_DATA_READING_ML_DATASET_BUILDER_AUTHORIZATION_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
— the next step is a docs-only authorization memo for the data-reading builder
(Phase 4bn-AG), which must resolve `source_admissible_for_data_read` /
`source_admissible_for_dataset_builder` and bind the leakage proof + budget
preflight before any data is read. A **current-state consolidation memo** remains
a recommended near-term parallel docs-only option (the state doc is large /
partially stale) but is not a blocker.

## 31. Explicit non-authorizations

This phase does not, and does not authorize anyone to: read or create local data;
inspect any file under `data/microstructure/` or `data/research/`; read the v002
terminal window; touch the sealed test (`test_rows_loaded=0`); create the future
output namespace; build a dataset; produce a real proof sidecar; create a
manifest / gate report / research matrix / ML config; train / score / predict;
run diagnostics / strategy / signals / PnL / backtests; flip `research_eligible`;
transition `eligibility_gate_status` / `chronological_split_policy` /
`diagnostics_authorized` / `ml_authorized`; invoke the Phase 4aw
`flip_research_eligible(...)` invariant; or authorize any successor. Every
retained verdict and project lock is preserved verbatim.

## 32. Result state

`CODE_ONLY_ML_DATASET_BUILDER_SKELETON_IMPLEMENTED__SYNTHETIC_TESTS_PASS__NO_DATA_READ__REMAIN_PAUSED`

## 33. Decision

`RECOMMEND_AUTHORIZE_DATA_READING_ML_DATASET_BUILDER_AUTHORIZATION_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`

## 34. Recommended state and successor options

**Remain paused. No next phase authorized.** Options (each separately
authorized): remain paused; request a merge prompt for Phase 4bn-AF; separately
authorize a data-reading ML dataset builder authorization memo (Phase 4bn-AG,
preferred); separately authorize a current-state consolidation memo; separately
authorize additional skeleton hardening; separately authorize a
source-admissibility gate artefact; reject further ML-baseline successors and
close the ML arc.

## 35. Current-project-state update summary

`current-project-state.md` is updated **additively only**: one new Phase 4bn-AF
paragraph after the Phase 4bn-AE paragraph, and one new `Current phase:` block
ahead of the Phase 4bn-AE block. All prior content is preserved verbatim. No
manifest field, eligibility flag, or split-policy field is set. The update records:
three new source modules + one offline test module (97 tests, all passing); ruff
clean; 0 direct mypy errors (29 pre-existing sibling errors); no data read; no
data created; no output namespace created; result
`CODE_ONLY_ML_DATASET_BUILDER_SKELETON_IMPLEMENTED__SYNTHETIC_TESTS_PASS__NO_DATA_READ__REMAIN_PAUSED`;
decision
`RECOMMEND_AUTHORIZE_DATA_READING_ML_DATASET_BUILDER_AUTHORIZATION_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
remain paused; no successor authorized.
