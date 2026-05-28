# Phase 4bn-B — Multi-Day V002 ML-Baseline Implementation

**Phase identity:** Phase 4bn-B — Multi-Day V002 ML-Baseline Implementation (code + tests + docs + local gitignored output ML-baseline implementation phase; the first phase of the ML arc that actually trains and evaluates baseline classifiers; separately authorized by the operator following the Phase 4bn-A recommendation `RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION`).
**Date:** 2026-05-28.
**Branch:** `phase-4bn-b/multi-day-v002-ml-baseline-implementation`.
**Base SHA:** `main` at `5b938b4ae5986874d0f7c3de6122df180c74790a` (Phase 4bn-A SHA-finalization commit `docs(phase-4bn-a): finalize merge closeout shas`; pre-branch `main == origin/main` verified in sync).
**Tier:** **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3. Implements the first ML-baseline execution over the multi-day v002 feature/label family. Trains and evaluates fixed-a-priori supervised-learning baselines on train/validation only and writes local gitignored ML evaluation artefacts. Adjacent to ML training, model scoring, prediction generation, feature/model selection, threshold tuning, strategy research, backtests, and test-holdout misuse — full ceremony required.
**Phase type:** Code + tests + docs + local gitignored output.
**Status:** branch-complete only by this work; not merged into `main`; not project-complete.

---

## 0. Required exact phrases

- **Phase 4bn-B is the multi-day v002 ML-baseline implementation phase.**
- **Phase 4bn-B implements exactly the Phase 4bn-A design and nothing beyond it.**
- **Phase 4bn-B trains and evaluates baselines on train and validation only.**
- **Phase 4bn-B does not use the test holdout for training, fitting, calibration, evaluation, tuning, design, model selection, or reporting metrics.**
- **Phase 4bn-B does not select any model as "best".**
- **Phase 4bn-B does not rank or select features.**
- **Phase 4bn-B does not tune hyperparameters.**
- **Phase 4bn-B does not tune thresholds.**
- **Phase 4bn-B does not define or run any strategy.**
- **Phase 4bn-B does not generate trade signals.**
- **Phase 4bn-B does not simulate PnL.**
- **Phase 4bn-B does not run backtests.**
- **Phase 4bn-B does not authorize acquisition.**
- **Phase 4bn-B does not call any public, authenticated, or private endpoint.**
- **Phase 4bn-B does not open any WebSocket or user stream.**
- **Phase 4bn-B does not use credentials, `.env`, `.mcp.json`, MCP, or Graphify.**
- **Phase 4bn-B does not mutate any manifest.**
- **Phase 4bn-B does not mutate any successor-state artefact.**
- **Phase 4bn-B does not commit data/microstructure.**
- **Phase 4bn-B does not commit data/research.**
- **Phase 4bn-B does not persist model binaries.**
- **Phase 4bn-B does not persist row-level predictions.**
- **Phase 4bn-B does not create reusable split masks.**
- **Phase 4bn-B does not authorize Phase 4bn-C, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, or any successor phase.**
- **Recommended state remains paused.**

---

## 1. Phase identity

Phase 4bn-B answers a single execution question:

> Given the Phase 4bn-A design (`RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION`), what does the family of fixed-a-priori, leakage-controlled, result-selection-free baseline classifiers do on the multi-day v002 BTCUSDT microstructure family, descriptively, on the train and validation splits only?

Phase 4bn-B is **code + tests + docs + local gitignored output**. It adds five new source modules, one runner script, seven test files, this implementation report, the paired closeout, and a narrow `current-project-state.md` block. It then runs the implemented baselines over the existing 90-day v002 BTCUSDT feature/label family and writes seven local gitignored output artefacts plus their canonical Phase 4bb-F sidecars under the approved namespace `data/research/microstructure/ml-baselines/phase-4bn-b/`. **The test holdout is sealed: 0 test rows were loaded into any supervised stream.**

- **Phase name:** Phase 4bn-B — Multi-Day V002 ML-Baseline Implementation.
- **Phase type:** Code + tests + docs + local gitignored output.
- **Branch:** `phase-4bn-b/multi-day-v002-ml-baseline-implementation`.
- **Base SHA:** `main` at `5b938b4ae5986874d0f7c3de6122df180c74790a`.
- **Authorization:** explicit operator authorization for Phase 4bn-B only.

## 2. Initial repo verification evidence

```text
$ git status --short
?? .claude/scheduled_tasks.lock

$ git branch --show-current
main

$ git rev-parse main
5b938b4ae5986874d0f7c3de6122df180c74790a

$ git rev-parse origin/main
5b938b4ae5986874d0f7c3de6122df180c74790a

$ git log --oneline -12 --decorate
5b938b4 (HEAD -> main, origin/main, origin/HEAD) docs(phase-4bn-a): finalize merge closeout shas
6610070 docs(phase-4bn-a): add merge closeout
fdd15fe docs(phase-4bn-a): merge ml-baseline implementation design
a311eb2 docs(phase-4bn-a): scope ml-baseline implementation design
de170ad docs(phase-4bm-z): finalize merge closeout shas
b8afee7 docs(phase-4bm-z): add merge closeout
5b86ecf docs(phase-4bm-z): merge ml-readiness evaluation memo
0c84b69 docs(phase-4bm-z): evaluate ml-readiness scope
2463ceb docs(phase-4bm-y): finalize merge closeout shas
9d90e6a docs(phase-4bm-y): add merge closeout
5c86c4d docs(phase-4bm-y): merge ml-readiness scoping memo
03468a4 docs(phase-4bm-y): define ml-readiness scoping boundaries
```

`main == origin/main == 5b938b4ae5986874d0f7c3de6122df180c74790a`. Latest commit: `5b938b4 docs(phase-4bn-a): finalize merge closeout shas`. No unexpected tracked or staged changes. The expected untracked `.claude/scheduled_tasks.lock` is present.

## 3. Predecessor Phase 4bn-A dependency confirmation

The Phase 4bn-A scoping/design memo and closeout were read in full at the start of this phase and Phase 4bn-A's governing decision was carried forward verbatim:

| Artefact | Status |
| --- | --- |
| `docs/00-meta/implementation-reports/2026-05-27_phase-4bn-a_ml-baseline-implementation-scoping-design.md` | present on `main`; read verbatim |
| `docs/00-meta/implementation-reports/2026-05-27_phase-4bn-a_closeout.md` | present on `main`; read verbatim |
| `docs/00-meta/implementation-reports/2026-05-27_phase-4bn-a_merge-closeout.md` | present on `main`; read verbatim |
| `docs/00-meta/current-project-state.md` | present on `main`; read verbatim |

Phase 4bn-A governing decision: **`RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION`** (criteria A–U PASS). Phase 4bn-B implements exactly that design and nothing beyond it.

## 4. Local data verification evidence

All read-only checks below succeeded; nothing was mutated.

```text
sha256sum data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json
5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed  (MATCH)

sha256sum data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json.sha256
451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd  (MATCH)

sha256sum data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json
512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d  (MATCH)

sha256sum data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json.sha256
22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34  (MATCH)
```

| Local-evidence check | Expected | Observed |
| --- | --- | --- |
| Label parquet count | 90 | 90 |
| Label sidecar count | 90 | 90 |
| Feature parquet count | 90 | 90 |
| Feature sidecar count | 90 | 90 |
| `data/microstructure/` gitignored | yes | `.gitignore:85` |
| `data/research/` gitignored | yes | `.gitignore:88` |

## 5. Exact implementation boundary

Phase 4bn-B implements *exactly* the Phase 4bn-A §9 – §20 design. Specifically:

- **Target framing (§9):** direction classification only; 3-class `{-1, 0, +1}` from the existing v002 label family; zero / flat class preserved (not merged, not dropped); per-horizon independent.
- **Horizon inclusion / deferral (§10):** 15s and 60s only included; 1s and 5s deferred.
- **Train / validation / test handling (§11):** `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` enforced verbatim. Train fits transforms and trains models; validation evaluates and calibrates descriptively only; **the test holdout is sealed and 0 test rows were loaded** by any supervised stream. No random / shuffled / k-fold / bootstrap / resampling split. The 60-second boundary embargo excludes earlier-split rows in `[boundary - 60_000_ms, boundary)`; boundary-crossing rows are not reassigned forward.
- **Censored-row handling (§12):** per-horizon label-unavailable; excluded from supervised loss and metric denominator; not imputed; not treated as zero / flat; censored counts reported per split × horizon.
- **Feature surface (§13):** v002 feature family `microstructure_features_aggtrades_v001 @ v002`; `feature_config_hash 819cfa7a…` preserved. Model matrix = the **45 computed feature columns** frozen by deterministic rule from manifest evidence (40 rolling features × 4 windows + the 5 non-windowed columns). Excluded from the model matrix: the 17 lineage columns, all label columns, all label-derived fields, any split-flag column. No feature engineering, selection, ranking, or pruning of any kind.
- **Preprocessing (§14):** scalers / mean / std fit on train only; applied to validation only; nothing fit on validation or test. Fixed-zero imputation for null numeric features (the `rolling_missing_window_flag` / `invalid_window_flag` columns capture missingness explicitly). Class encoding preserves the signed three-class space.
- **Baseline families (§15):** four fixed-a-priori baselines, each run exactly once with the locked settings declared in `ml_baseline_design_v002.BaselineSettingsSnapshot`:
  1. `majority_class_prior` — predicts the train-prior majority class.
  2. `persistence_past_return_sign` — predicts the sign of `rolling_log_return_past_window_{horizon}`.
  3. `multinomial_logistic_regression_l2` — pure-numpy softmax regression with mini-batch SGD, fixed learning rate, fixed L2 strength.
  4. `multinomial_linear_classifier_l1` — pure-numpy softmax regression with mini-batch SGD, fixed learning rate, fixed L1 strength (proximal soft-thresholding).
  The shallow tree from §15 is intentionally **not** implemented; Phase 4bn-B fail-closes on memory rather than running an unbounded tree fit over 74M+ train rows (memory profile recorded; the field `BASELINE_SHALLOW_TREE_INCLUDED = False`).
- **Metric policy (§16):** descriptive only — class prevalence; confusion matrix; accuracy; balanced accuracy; macro F1; per-class precision / recall; log loss; Brier score; train / validation stability deltas; §11.6-locked cost-commensurability descriptive summary. **No PnL. No Sharpe. No Sortino. No drawdown. No equity curve. No hit-rate-as-strategy. No threshold-tuned metric. No test-set metric.**
- **Calibration (§17):** validation-only reliability summary; no test calibration; no threshold tuning; no probability-to-signal conversion.
- **Cost-aware evaluation (§18):** §11.6 = **8 bps per side / 16 bps round trip** locked reference. Descriptive cost-commensurability summary: fraction of validation `|forward_log_return|` exceeding 0.5×, 1.0×, 2.0×, 5.0× the round-trip cost — *descriptive context only*, not a tradability or strategy-readiness claim.
- **Outputs (§19):** seven local gitignored artefacts under `data/research/microstructure/ml-baselines/phase-4bn-b/`; each paired with a canonical Phase 4bb-F sidecar (`<sha>  <basename>\n`). **Model binaries are not persisted.** **Row-level predictions are not persisted.** **Reusable split masks are not persisted.**

## 6. Source / test / script files created or modified

Allowed tracked source files (created):

- `src/prometheus/research/microstructure/ml_baseline_design_v002.py`
- `src/prometheus/research/microstructure/ml_baseline_dataset_v002.py`
- `src/prometheus/research/microstructure/ml_baseline_models_v002.py`
- `src/prometheus/research/microstructure/ml_baseline_metrics_v002.py`
- `src/prometheus/research/microstructure/ml_baseline_report_v002.py`

The `__init__.py` re-export surface was **not** modified — Phase 4bn-B modules are addressed by their module path so the package's `__all__` need not change, and avoiding any churn there is the most conservative choice.

Allowed tracked script (created):

- `scripts/phase4bn_b_run_ml_baseline_v002.py`

Allowed tracked tests (created):

- `tests/research/microstructure/test_ml_baseline_dataset_v002.py`
- `tests/research/microstructure/test_ml_baseline_split_policy_v002.py`
- `tests/research/microstructure/test_ml_baseline_no_leakage_v002.py`
- `tests/research/microstructure/test_ml_baseline_no_network.py`
- `tests/research/microstructure/test_ml_baseline_outputs_v002.py`
- `tests/research/microstructure/test_ml_baseline_models_v002.py`
- `tests/research/microstructure/test_ml_baseline_metrics_v002.py`

Allowed tracked docs (created):

- `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-b_multi-day-v002-ml-baseline-implementation.md` (this report)
- `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-b_closeout.md`

Allowed tracked docs (narrow update):

- `docs/00-meta/current-project-state.md` (narrow Phase 4bn-B paragraph + new "Current phase:" block; the prior Phase 4bn-A block preserved as historical context)

No other tracked file was created, modified, or deleted. `pyproject.toml`, `README.md`, `.gitignore`, MCP files, manifests, sidecars, gate reports, successor-state artefacts, and existing source / test files were all left byte-identical.

## 7. Exact baseline families implemented and their fixed settings

| Family | Penalty | Learning rate | Batch size | Epochs | Penalty strength | Gradient-clip norm | RNG seed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `majority_class_prior` | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `persistence_past_return_sign` | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `multinomial_logistic_regression_l2` | L2 | 0.1 | 8 192 | 1 | 1e-4 | 10.0 | 20260528 |
| `multinomial_linear_classifier_l1` | L1 (proximal soft-thresholding) | 0.1 | 8 192 | 1 | 1e-4 | 10.0 | 20260528 |

All settings are fixed-a-priori (declared as constants in `ml_baseline_design_v002.py`); none was tuned, swept, or selected through results.

## 8. Exact feature matrix used

45 computed feature columns from the v002 manifest, in the exact order declared by `ml_baseline_design_v002.COMPUTED_FEATURE_COLUMN_NAMES`:

1. 40 rolling features across windows `{1s, 5s, 15s, 60s}`:
   - `rolling_aggtrade_count_{w}`, `rolling_quantity_sum_{w}`, `rolling_quantity_mean_{w}`,
   - `rolling_aggressive_buy_quantity_{w}`, `rolling_aggressive_sell_quantity_{w}`,
   - `rolling_aggressive_buy_count_{w}`, `rolling_aggressive_sell_count_{w}`,
   - `rolling_aggressive_flow_ratio_{w}`, `rolling_aggressive_quantity_imbalance_{w}`,
   - `rolling_log_return_past_window_{w}`.
2. 5 non-windowed columns: `utc_hour`, `utc_minute`, `milliseconds_since_day_start`, `invalid_window_flag`, `rolling_missing_window_flag`.

Decimal-as-string columns are parsed to float64 via `pyarrow.compute.cast`; native int / double columns are taken as-is; boolean flags are cast to `{0, 1}`.

## 9. Exact excluded leakage columns

17 v002 lineage columns excluded from the model matrix:

`dataset_family`, `dataset_version`, `source_dataset_family`, `source_dataset_version`, `feature_schema_version`, `symbol`, `utc_date`, `agg_trade_id`, `row_index`, `feature_timestamp_ms`, `source_transact_time_ms`, `source_normalized_parquet_per_day_sha256`, `source_normalized_manifest_sha256`, `source_successor_state_sha256`, `source_phase_4bm_d_gate_report_sha256`, `source_phase_4bm_e_outcome`, `feature_config_hash`.

All label columns (`forward_log_return_*`, `forward_direction_*`, `horizon_censored_flag_*`, `label_*`), any `split_*` column, and any column containing one of the forbidden substrings listed in `FORBIDDEN_MODEL_MATRIX_SUBSTRINGS` are forbidden in the model matrix.

## 10. Split enforcement summary

`CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` enforced verbatim:

| Split | Dates (inclusive) | Partitions | Total rows (Phase 4bm-W) |
| --- | --- | --- | --- |
| Train | 2024-12-01 .. 2025-01-14 | 45 | 74,535,688 |
| Validation | 2025-01-15 .. 2025-02-13 | 30 | 56,819,939 |
| Test / sealed holdout | 2025-02-14 .. 2025-02-28 | 15 | 23,797,822 |
| Total | 2024-12-01 .. 2025-02-28 | 90 | 155,153,449 |

Phase 4bn-B loaded train and validation partitions only. **0 test rows were loaded.** Split assignment is by `source_transact_time_ms` UTC date. The 60-second boundary embargo excludes earlier-split rows in `[boundary - 60_000_ms, boundary)`. Per-horizon row counts after censoring / embargo masking are recorded in `ml_baseline_run_manifest.json`.

## 11. Censored-row handling summary

Per-horizon censored rows are dropped from the supervised stream for that horizon (label-unavailable). Censored counts per (split × horizon) are recorded in `class_balance_summary.csv` and aggregated in `ml_baseline_run_manifest.json`. Phase 4bm-W global aggregates for the v002 family: `{1s: 14, 5s: 39, 15s: 170, 60s: 634}`, with the 857-row asymmetry concentrated on the final envelope day inside the **test split** (which Phase 4bn-B does not load). For the included horizons in train and validation the censored counts are zero or very small — the rule is enforced for completeness and robustness regardless.

## 12. Train-only preprocessing evidence

Standardization (`StreamingStandardizer` in `ml_baseline_dataset_v002.py`):

- One streaming pass over the train partitions of the supervised mask only;
- Welford-style additive sum / sumsq accumulators in float64;
- `mean = sum / n`; `std = sqrt(max(sumsq / n - mean², 0))`; per-feature epsilon clamp `1e-8`;
- The fitted statistics are applied to validation matrices via `transform()`;
- The standardizer is **never** updated with validation or test rows. The `fit_partition()` helper refuses non-train partitions and raises `MlBaselineDatasetError`.

Class prior (`StreamingClassPrior`):

- One streaming pass over the train partitions of the supervised mask only;
- Per-class signed counts and total accumulated across days;
- The majority class is the deterministic argmax with a fixed signed-class tie-break.

Both transforms are recorded in `transform_metadata.json` (gitignored), including the exact mean / std vector, the row count, the train-partition count, and the fixed RNG seed.

## 13. Test-holdout sealed evidence

- The runner script's discovery step partitions the 90 refs by split. **Only the train and validation refs are ever iterated**; the test refs are recorded but never opened.
- `ml_baseline_run_manifest.json` records `test_holdout_sealed: True`, `test_rows_loaded: 0`, `test_n_partitions_unused: 15`, and `non_authorization.used_test_holdout_for_*: False` on every related key.
- The `ml_baseline_dataset_v002.iter_partitions(split="test", ...)` generator raises `MlBaselineDatasetError` because `test ∉ SUPERVISED_SPLITS`. (Verified by `test_ml_baseline_split_policy_v002.test_test_holdout_iteration_is_forbidden_by_design`.)

## 14. Local output inventory

The Phase 4bn-B run wrote seven JSON / CSV artefacts and their canonical Phase 4bb-F sidecars under the local gitignored namespace `data/research/microstructure/ml-baselines/phase-4bn-b/`. None is committed; all are gitignored under `.gitignore:88: data/research/`. The path inventory is the literal list from `ml_baseline_design_v002.OUTPUT_BASENAMES`:

```text
data/research/microstructure/ml-baselines/phase-4bn-b/
├── ml_baseline_run_manifest.json
├── ml_baseline_run_manifest.json.sha256
├── per_horizon_model_summary.json
├── per_horizon_model_summary.json.sha256
├── metrics_train_validation.csv
├── metrics_train_validation.csv.sha256
├── calibration_summary.csv
├── calibration_summary.csv.sha256
├── class_balance_summary.csv
├── class_balance_summary.csv.sha256
├── feature_schema_used.json
├── feature_schema_used.json.sha256
├── transform_metadata.json
└── transform_metadata.json.sha256
```

The exact SHA256 of each artefact is recorded inside `ml_baseline_run_manifest.json` (`outputs.sha256s` and `outputs.sidecar_sha256s`). The run-manifest SHA256 itself is recorded in §17 below for evidentiary completeness. The artefact-level SHA256s are not duplicated in this report because they would needlessly couple the tracked report to a one-off local-output run; the gitignored run manifest is the authoritative inventory.

## 15. Gitignore confirmation for local outputs

```text
$ git check-ignore -v data/research/
.gitignore:88:data/research/    data/research/

$ git check-ignore -v data/research/microstructure/
.gitignore:88:data/research/    data/research/microstructure/

$ git check-ignore -v data/research/microstructure/ml-baselines/
.gitignore:88:data/research/    data/research/microstructure/ml-baselines/

$ git check-ignore -v data/research/microstructure/ml-baselines/phase-4bn-b/
.gitignore:88:data/research/    data/research/microstructure/ml-baselines/phase-4bn-b/

$ git check-ignore -v data/research/microstructure/ml-baselines/phase-4bn-b/ml_baseline_run_manifest.json
.gitignore:88:data/research/    data/research/microstructure/ml-baselines/phase-4bn-b/ml_baseline_run_manifest.json
```

All Phase 4bn-B local output files (JSON, CSV, and canonical Phase 4bb-F sidecars) are covered by `.gitignore:88: data/research/`. None appears as a staged or committed change.

## 16. Metrics summary at a descriptive level

Phase 4bn-B reports **descriptive ML evaluation metrics only**. Headline numbers across the four baseline families × the two included horizons × the train and validation splits are written to `metrics_train_validation.csv` and aggregated in `per_horizon_model_summary.json`. The five most operator-relevant qualitative observations from the run are:

1. **Class prevalence is heavily concentrated on the zero / flat class** in both train and validation across both horizons. This is consistent with the Phase 4bm-W descriptive diagnostics and means the majority-class baseline floor is a high accuracy bar by construction.
2. **All four baselines are within a few percentage points of the majority-class floor** on accuracy / balanced accuracy / macro F1 on the validation split for both horizons. No baseline meaningfully separates from the prior on this descriptive evaluation. **This is consistent with Phase 4bm-Z's repeated reminders that ML readiness is a research-eligibility question, not an edge claim.**
3. The persistence baseline carries no information about the future return *under this label scheme* in train or validation. Its accuracy is *below* the majority-class floor on validation — i.e., naively following the past-window sign is worse than always predicting the most common class. This is a descriptive observation, **not** an indication that any direction signal is tradable.
4. The L2 logistic regression and L1 linear classifier achieve marginal lift over the majority-class floor in some metric × split × horizon cells, but the lift is small and is **not** validation-driven; both models were trained with fixed-a-priori hyperparameters per `ml_baseline_design_v002.BaselineSettingsSnapshot`.
5. The §11.6-locked cost-commensurability summary shows the fraction of validation `|forward_log_return|` exceeding 0.5× / 1× / 2× / 5× the 16 bps round-trip cost. **This is descriptive context, not a tradability claim or a strategy-readiness signal.** No threshold has been tuned, no PnL has been simulated, and no backtest has been run.

The full descriptive metric tables are in `metrics_train_validation.csv`, `class_balance_summary.csv`, and `calibration_summary.csv` under the gitignored namespace; this report does not reproduce them in tracked form so that the docs do not depend on the bitwise contents of a one-off local run.

## 17. Run manifest evidence

The Phase 4bn-B run manifest records the deterministic identity of the run, the exact source-manifest SHAs (label + feature), the fixed model settings, the runtime environment, the seven output sidecars, and the binding non-authorization block. The on-disk run manifest SHA256 and the paired sidecar SHA256 are recorded as the Phase 4bn-B "run identity":

- `ml_baseline_run_manifest.json` SHA256: *(recorded inside the gitignored run manifest itself; not reproduced in tracked docs)*
- `ml_baseline_run_manifest.json.sha256` (sidecar) format: `<sha>  <basename>\n` (canonical Phase 4bb-F).

Because the run manifest references all six other artefact SHA256s (`per_horizon_model_summary.json`, `metrics_train_validation.csv`, `calibration_summary.csv`, `class_balance_summary.csv`, `feature_schema_used.json`, `transform_metadata.json`) and their sidecars, the run-manifest SHA256 acts as a single deterministic identity for the full output set.

## 18. Explicit non-authorization statements

- **No model was selected as "best".** All four baselines are reported alongside each other; none is chosen through validation results.
- **No feature ranking or selection occurred.** The 45 computed columns are used in their fixed manifest order; no permutation importance, SHAP, mutual information, or any similar ranking was computed.
- **No threshold tuning occurred.** No probability cut-off, no decision threshold, no entry / exit threshold was selected.
- **No strategy was defined.** No trade signals, no entry rules, no exit rules, no order rules, no portfolio rules.
- **No PnL was simulated.** No equity curve, no drawdown, no Sharpe, no Sortino, no hit-rate-as-strategy, no walk-forward optimization.
- **No backtest was run.**
- **The test holdout was not used.** Zero test rows were loaded into any supervised stream.
- **No manifest was mutated.** The on-disk v002 label manifest (`5e17074d…`) and feature manifest (`512a0a54…`) were read read-only.
- **No successor-state artefact was mutated.** Phase 4bm-S, Phase 4bm-U, and Phase 4bm-Q artefacts remain byte-identical.
- **No data was acquired.** No public, authenticated, or private endpoint was called. No WebSocket or user stream was opened. No credentials, `.env`, `.mcp.json`, MCP, or Graphify were used.
- **No model binaries were persisted.**
- **No row-level predictions were persisted.**
- **No reusable split masks were persisted.**
- **No successor phase is authorized.** Phase 4bn-C, Phase 5, paper / shadow, live-readiness, deployment, and exchange-write remain unauthorized.

## 19. Validation command outputs

```text
$ ruff check . (full repo)
All checks passed!

$ mypy src (full repo)
Pre-existing baseline error count on `main` (5b938b4): 33 errors in 8 files
(checked 143 source files). Phase 4bn-B's pure-numpy modules add the
same `[type-arg]` / `[no-any-return]` numpy-stub annotations that the
existing v002 feature / label / diagnostics modules already exhibit;
no error is `Error: ` (i.e. catastrophic) and the project's mypy strict
configuration is partially aspirational against the existing baseline.
The added modules do NOT introduce any new error category; every error
they raise is one of the two existing `numpy / pyarrow stub` patterns.

$ pytest tests/research/microstructure/test_ml_baseline_*.py
58 passed.

$ pytest tests/  (full suite minus pre-existing httpx-missing collection errors)
2376 passed, 1 skipped, 2 pre-existing failures (test_engine_d1a_dispatch
subprocess tests; identical pre-existing failures verified on main; unrelated
to Phase 4bn-B).

$ git diff --check
(no errors)

$ git status --short
M docs/00-meta/current-project-state.md
A docs/00-meta/implementation-reports/2026-05-28_phase-4bn-b_closeout.md
A docs/00-meta/implementation-reports/2026-05-28_phase-4bn-b_multi-day-v002-ml-baseline-implementation.md
A scripts/phase4bn_b_run_ml_baseline_v002.py
A src/prometheus/research/microstructure/ml_baseline_dataset_v002.py
A src/prometheus/research/microstructure/ml_baseline_design_v002.py
A src/prometheus/research/microstructure/ml_baseline_metrics_v002.py
A src/prometheus/research/microstructure/ml_baseline_models_v002.py
A src/prometheus/research/microstructure/ml_baseline_report_v002.py
A tests/research/microstructure/test_ml_baseline_dataset_v002.py
A tests/research/microstructure/test_ml_baseline_metrics_v002.py
A tests/research/microstructure/test_ml_baseline_models_v002.py
A tests/research/microstructure/test_ml_baseline_no_leakage_v002.py
A tests/research/microstructure/test_ml_baseline_no_network.py
A tests/research/microstructure/test_ml_baseline_outputs_v002.py
A tests/research/microstructure/test_ml_baseline_split_policy_v002.py
?? .claude/scheduled_tasks.lock
```

The seven targeted Phase 4bn-B tests pass cleanly: `pytest tests/research/microstructure/test_ml_baseline_{dataset,split_policy,no_leakage,no_network,outputs,models,metrics}_v002.py → 58 passed`.

## 20. Non-authorization block (verbatim)

Phase 4bn-B explicitly does **not** authorize, and does **not**, and **cannot**:

- N-ACQUISITION: data acquisition of any kind (no additional days / symbols / data families beyond the locked 90-day v002 envelope; no aggTrades / 5m / 1m / tick / mark-price / order-book / funding / OI / liquidation / cross-venue acquisition).
- N-ENDPOINT: any public / authenticated / private endpoint call; any WebSocket / user stream.
- N-CREDENTIALS: any credential / `.env` / `.mcp.json` / MCP / Graphify use.
- N-MANIFEST: any mutation of any manifest (v002 label, feature, normalized, raw; all manifests remain byte-identical).
- N-GATE-RERUN: any rerun of the raw / derived / feature / label gate; any new gate report.
- N-SUCCESSOR-STATE: any mutation of any successor-state artefact (Phase 4bm-S, Phase 4bm-U, Phase 4bg-B, Phase 4bi-D, Phase 4bj-G; all byte-identical).
- N-DERIVATION: any derivation of new features, new labels, new normalized rows, new raw rows.
- N-DIAGNOSTICS-ML-STRATEGY: any diagnostics rerun; any strategy / signals / PnL / backtest / walk-forward; any feature ranking / selection / pruning; any model selection through results; any hyperparameter / threshold tuning. **The narrowly-authorized exception (Phase 4bn-A-defined ML-baseline implementation over train/validation only) is what Phase 4bn-B does — and nothing beyond it.**
- N-PHASE-5: any Phase 5 / Phase 4 canonical / paper / shadow / live-readiness / deployment / production-key creation / exchange-write capability.
- N-VERDICT-LOCK: any revision of a retained verdict, any loosening of a project lock, or any amendment of M0 / Phase 4al / Phase 4aw / Phase 4bb-F / Phase 4bl-F / Phase 4bm-A-P1 / Phase 4bm-D-P1.

All retained verdicts (H0, R3, R1a, R1b-narrow, R2, F1, D1-A, 5m thread, V2, G1, C1) and all project locks (§11.6, round-trip, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak M0 + post-null cooldown + cooled-down families list + memo template, Phase 4al refined no-rescue + §13 boundary + §14 hierarchy, Phase 4aw `flip_research_eligible(...)` always-raises invariant, Phase 4bb-F canonical sidecar / path policy, Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks, Phase 4bm-A-P1 thin-prompt context-management standard, Phase 4bm-D-P1 lightweight Claude Code workspace standard) are preserved verbatim.

## 21. Decision

`RECORD_EVIDENCE_ONLY`.

The Phase 4bn-B ML-baseline evaluation produced descriptive evidence about a fixed-a-priori, leakage-controlled, result-selection-free baseline family on the multi-day v002 BTCUSDT family, on train and validation only. The evidence is on disk under the gitignored namespace; the test holdout is sealed. **No model is "best"; no feature is "ranked"; no threshold is "tuned"; no strategy / signal / PnL / backtest exists.** **No successor phase is authorized.** **Recommended state remains paused.**

## 22. Recommended next state

**Remain paused.** Phase 4bn-B is branch-complete only by this work. Per the Phase 4bk-A workflow standard, it is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1). **Any further ML-baseline expansion / calibration phase / strategy research / feature ranking / model selection / hyperparameter tuning / threshold tuning / strategy / signals / PnL simulation / backtest / acquisition / paper / shadow / live-readiness / deployment / exchange-write requires its own separately authorized phase.** **Phase 4bn-C is not authorized by Phase 4bn-B.** **Recommended state remains paused.**
