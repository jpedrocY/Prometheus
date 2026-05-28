# Phase 4bn-B — Merge Closeout

**Phase 4bn-B is now merge-complete on main.** **Phase 4bn-B is the multi-day v002 ML-baseline implementation phase.** **Phase 4bn-B implements exactly the Phase 4bn-A design and nothing beyond it.** **Phase 4bn-B trains and evaluates baselines on train and validation only.** **Phase 4bn-B does not use the test holdout for training, fitting, calibration, evaluation, tuning, design, model selection, or reporting metrics.** **Phase 4bn-B does not select any model as "best".** **Phase 4bn-B does not rank or select features.** **Phase 4bn-B does not tune hyperparameters.** **Phase 4bn-B does not tune thresholds.** **Phase 4bn-B does not define or run any strategy.** **Phase 4bn-B does not generate trade signals.** **Phase 4bn-B does not simulate PnL.** **Phase 4bn-B does not run backtests.** **Phase 4bn-B does not authorize acquisition.** **Phase 4bn-B does not call any public, authenticated, or private endpoint.** **Phase 4bn-B does not open any WebSocket or user stream.** **Phase 4bn-B does not use credentials, .env, .mcp.json, MCP, or Graphify.** **Phase 4bn-B does not mutate any manifest.** **Phase 4bn-B does not mutate any successor-state artefact.** **Phase 4bn-B does not commit data/microstructure.** **Phase 4bn-B does not commit data/research.** **Phase 4bn-B does not persist model binaries.** **Phase 4bn-B does not persist row-level predictions.** **Phase 4bn-B does not create reusable split masks.** **Phase 4bn-B does not authorize Phase 4bn-C, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, or any successor phase.** **Recommended state remains paused.**

## 1. Phase identity

- **Phase:** Phase 4bn-B — Multi-Day V002 ML-Baseline Implementation.
- **Type:** code + tests + docs + local gitignored output ML-baseline implementation phase (Tier 1 — Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` §3). First phase of the ML arc that actually trains and evaluates baseline classifiers.
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bn-B ML-baseline implementation surface — five new source modules, one runner script, seven test files, the implementation report, the closeout, and the narrow `current-project-state.md` paragraph + Current-phase block — onto `main`, recording the implementation decision `RECORD_EVIDENCE_ONLY` as project state. The phase implements *exactly* the Phase 4bn-A §9 – §20 design and trains and evaluates four fixed-a-priori baseline classifiers on the train and validation splits only of the v002 BTCUSDT feature/label family, for horizons 15s and 60s only, on the frozen 45-column v002 computed-feature matrix, with the test holdout sealed (0 test rows loaded into any supervised stream).
- **Target branch:** `main`.
- **Source branch:** `phase-4bn-b/multi-day-v002-ml-baseline-implementation`.

## 2. SHAs

- **`main` SHA before merge:** `5b938b4ae5986874d0f7c3de6122df180c74790a` (Phase 4bn-A SHA-finalization commit `docs(phase-4bn-a): finalize merge closeout shas`; `main == origin/main` verified pre-merge).
- **Base SHA:** `5b938b4ae5986874d0f7c3de6122df180c74790a`.
- **Branch commit SHAs (in order on the branch):**
  - Implementation commit: `2a959793fa0ed888881c7c1554d04a052a3f4e4e` (`feat(phase-4bn-b): implement multi-day v002 ml baseline`). This single commit added all 5 source modules, the runner script, all 7 tests, both docs files, and the narrow `current-project-state.md` block.
  - EOF-style commit: `7099da6412f6d24cd9e0258b4a031096768535ce` (`style(phase-4bn-b): trim trailing blank lines at EOF`). Two-file pure-whitespace cleanup that removed two trailing blank lines flagged by `git diff --check` at the EOF of `ml_baseline_metrics_v002.py` and `ml_baseline_models_v002.py`. No functional change.
- **Branch tip SHA before merge:** `7099da6412f6d24cd9e0258b4a031096768535ce`.
- **Merge commit SHA:** `97b3f8f50edc6c13241b4adaedd4a1eff332dea1` (`feat(phase-4bn-b): merge ml-baseline implementation`).
- **Merge-closeout commit SHA:** `b321e5ce4419a0218341b0d35a934a10e4bf0ff0` (`docs(phase-4bn-b): add merge closeout`).
- **SHA-finalization commit:** recorded in the final operator report and git log as `docs(phase-4bn-b): finalize merge closeout shas`. Per the repo convention used for Phase 4bn-A / 4bm-Z / 4bm-Y / 4bm-X, the SHA-finalization commit cannot self-reference its own hash inside its own diff; its SHA is captured in the final operator report and git log. After that commit and push, final `main` SHA == final `origin/main` SHA == the SHA-finalization commit.
- **Final `main` / `origin/main` SHA after push:** equals the SHA-finalization commit; recorded in the final operator report.

## 3. Merge method

- `git merge --no-ff` with the `ort` strategy.
- Merge commit message: `feat(phase-4bn-b): merge ml-baseline implementation`.
- No `--no-verify`. No `--no-gpg-sign`. No `-c commit.gpgsign=false`. No force-push.
- Pushed to `origin/main` with no force, no skip-hooks, no skip-signing.

## 4. Files brought forward by the merge

Source (tracked, new):

- `src/prometheus/research/microstructure/ml_baseline_design_v002.py` (added; 454 lines)
- `src/prometheus/research/microstructure/ml_baseline_dataset_v002.py` (added; 559 lines)
- `src/prometheus/research/microstructure/ml_baseline_models_v002.py` (added; 580 lines)
- `src/prometheus/research/microstructure/ml_baseline_metrics_v002.py` (added; 310 lines)
- `src/prometheus/research/microstructure/ml_baseline_report_v002.py` (added; 364 lines)

The package `src/prometheus/research/microstructure/__init__.py` was deliberately **not** modified — Phase 4bn-B modules are addressed by their explicit module paths so the package's public `__all__` need not change.

Script (tracked, new):

- `scripts/phase4bn_b_run_ml_baseline_v002.py` (added; 633 lines)

Tests (tracked, new):

- `tests/research/microstructure/test_ml_baseline_dataset_v002.py` (added; 536 lines)
- `tests/research/microstructure/test_ml_baseline_split_policy_v002.py` (added; 96 lines)
- `tests/research/microstructure/test_ml_baseline_no_leakage_v002.py` (added; 119 lines)
- `tests/research/microstructure/test_ml_baseline_no_network.py` (added; 134 lines)
- `tests/research/microstructure/test_ml_baseline_outputs_v002.py` (added; 175 lines)
- `tests/research/microstructure/test_ml_baseline_models_v002.py` (added; 156 lines)
- `tests/research/microstructure/test_ml_baseline_metrics_v002.py` (added; 98 lines)

Docs (tracked):

- `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-b_multi-day-v002-ml-baseline-implementation.md` (added; 418 lines).
- `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-b_closeout.md` (added; 152 lines).
- `docs/00-meta/current-project-state.md` (modified — narrow Phase 4bn-B paragraph + new Current-phase block addition; prior Phase 4bn-A paragraph and prior Current-phase blocks preserved as labelled historical context; 108 net insertions).

Config: none. **No `pyproject.toml`, `README.md`, `.gitignore`, MCP file, manifest, sidecar, gate report, successor-state artefact, existing source / test / script file, or any `data/microstructure/` artefact was modified.** No prior governance memo was modified beyond the narrow `current-project-state.md` paragraph addition. **No `data/research/` artefact was committed** (the seven Phase 4bn-B local output artefacts + their canonical Phase 4bb-F sidecars remain local-only under `data/research/microstructure/ml-baselines/phase-4bn-b/` and are covered by `.gitignore:88: data/research/`).

The merge-closeout file (this file) is added by the subsequent merge-closeout commit on `main`, not by the merge commit itself.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 108 ++++
 .../2026-05-28_phase-4bn-b_closeout.md             | 152 +++++
 ...-b_multi-day-v002-ml-baseline-implementation.md | 418 ++++++++++++++
 scripts/phase4bn_b_run_ml_baseline_v002.py         | 633 +++++++++++++++++++++
 .../microstructure/ml_baseline_dataset_v002.py     | 559 ++++++++++++++++++
 .../microstructure/ml_baseline_design_v002.py      | 454 +++++++++++++++
 .../microstructure/ml_baseline_metrics_v002.py     | 310 ++++++++++
 .../microstructure/ml_baseline_models_v002.py      | 580 +++++++++++++++++++
 .../microstructure/ml_baseline_report_v002.py      | 364 ++++++++++++
 .../test_ml_baseline_dataset_v002.py               | 536 +++++++++++++++++
 .../test_ml_baseline_metrics_v002.py               |  98 ++++
 .../microstructure/test_ml_baseline_models_v002.py | 156 +++++
 .../test_ml_baseline_no_leakage_v002.py            | 119 ++++
 .../microstructure/test_ml_baseline_no_network.py  | 134 +++++
 .../test_ml_baseline_outputs_v002.py               | 175 ++++++
 .../test_ml_baseline_split_policy_v002.py          |  96 ++++
 16 files changed, 4892 insertions(+)
```

The diff matches the expected change set from the authorization prompt exactly: five new source modules, one new runner script, seven new test files, two new docs files, and one narrow modification to `current-project-state.md`. No deletions. No source / test / script / config / data / manifest / sidecar / gate-report / successor-state change outside this surface.

## 6. Verdict

**LOCAL ARTEFACT PRODUCED — `RECORD_EVIDENCE_ONLY`.**

Phase 4bn-B is the separately authorized ML-baseline implementation phase recommended by Phase 4bn-A. It implements *exactly* the Phase 4bn-A §9 – §20 design: direction classification only with the signed three-class `{-1, 0, +1}` target preserved (zero / flat class explicit, not merged, not dropped); horizons 15s and 60s only (1s / 5s deferred); the Phase 4bm-U `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` enforced verbatim; per-horizon censored-row exclusion; the frozen 45-column v002 computed-feature matrix; the 17 v002 lineage columns excluded from the model matrix; train-only mean/std fitting with fixed-zero null imputation; four fixed-a-priori baseline families run exactly once each (majority-class prior, persistence past-return sign, multinomial logistic regression L2, multinomial linear classifier L1) with locked SGD hyperparameters; descriptive ML metrics only (class prevalence, confusion matrix, accuracy, balanced accuracy, macro F1, per-class precision / recall, log loss, Brier score, train / validation stability deltas); validation-only descriptive reliability summary; §11.6-locked cost-commensurability descriptive summary at 8 bps per side / 16 bps round trip. **The test holdout is sealed:** 0 test rows were loaded into any supervised stream (`test_holdout_sealed = true`, `test_rows_loaded = 0`, `test_n_partitions_unused = 15` recorded in the run manifest). The four baselines are all within a few percentage points of the majority-class floor on validation for both horizons; the persistence baseline falls *below* the majority-class floor; the L2 / L1 softmax classifiers show only marginal lift in some metric × split × horizon cells; **no baseline meaningfully separates from the prior on this descriptive evaluation**. The §11.6 cost-commensurability summary is descriptive context only and is not an edge claim, a tradability claim, a profitability claim, or a strategy-readiness claim. **No model is "best", no feature is "ranked", no threshold is "tuned", and no strategy / signal / PnL / backtest exists.** Implementation decision: **`RECORD_EVIDENCE_ONLY`**. The v002 label/feature manifests remain `research_eligible = false` / `eligibility_gate_status = "pending"`; the label manifest's `chronological_split_policy` remains `"not_yet_defined"` on disk (the split policy is recorded only in the Phase 4bm-U sibling successor-state JSON, which is itself byte-identical pre / post). The lifecycle state is **remain paused**.

### 6.1 Target framing

Direction classification only; 3-class `{-1, 0, +1}` from the existing v002 label family; zero / flat class kept explicit (not merged, not dropped); no magnitude regression; no ordinal framing; no meta-labeling; per-horizon-independent framing.

### 6.2 Horizon inclusion / deferral

Included: **15s** and **60s** only. Deferred: **1s** and **5s**. No horizon is declared strategy-ready or live-tradable.

### 6.3 Train / validation / test handling

`CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`. Train: 2024-12-01 .. 2025-01-14 (45 partitions; 74,535,688 rows observed pre-mask; **74,535,440 train supervised rows per horizon** after the 248-row 60s boundary embargo; per Phase 4bm-W). Validation: 2025-01-15 .. 2025-02-13 (30 partitions; 56,819,939 rows observed pre-mask; **56,819,649 validation supervised rows per horizon** after the 290-row 60s boundary embargo). Test / final holdout: 2025-02-14 .. 2025-02-28 (15 partitions; **0 test rows loaded by Phase 4bn-B**). The dataset module's `iter_partitions(split="test", ...)` raises `MlBaselineDatasetError` because `test ∉ SUPERVISED_SPLITS` — verified by `test_ml_baseline_split_policy_v002.test_test_holdout_iteration_is_forbidden_by_design`.

Bookkeeping note: the on-disk run-manifest fields `train_embargoed_rows = 496` and `validation_embargoed_rows = 580` are per-horizon totals summed across both included horizons (248 × 2 = 496 train; 290 × 2 = 580 validation); the underlying physical 538-row embargo window (248 train + 290 validation; Phase 4bm-W) is counted once per horizon in this field. The supervised row counts above are deduplicated correctly.

### 6.4 Censored-row handling

Per-horizon censored rows are dropped from the supervised stream for that horizon (label-unavailable). The included horizons (15s, 60s) record **0 censored rows** in train and validation in this run (the global v002 aggregate `{1s: 14, 5s: 39, 15s: 170, 60s: 634}` is concentrated on the final envelope day inside the **test split**, which Phase 4bn-B does not load).

### 6.5 Feature surface

Existing v002 feature family only (`microstructure_features_aggtrades_v001 @ v002`); `feature_config_hash = 819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d` preserved. Model matrix = the 45 `computed_feature_column_names` (40 rolling features across windows `{1s, 5s, 15s, 60s}` + `utc_hour`, `utc_minute`, `milliseconds_since_day_start`, `invalid_window_flag`, `rolling_missing_window_flag`), frozen by deterministic rule derived from manifest evidence in `ml_baseline_design_v002.COMPUTED_FEATURE_COLUMN_NAMES`. **No new feature engineering. No feature selection. No feature ranking. No feature pruning.**

### 6.6 Excluded leakage columns

17 v002 lineage columns excluded from the model matrix: `dataset_family`, `dataset_version`, `source_dataset_family`, `source_dataset_version`, `feature_schema_version`, `symbol`, `utc_date`, `agg_trade_id`, `row_index`, `feature_timestamp_ms`, `source_transact_time_ms`, `source_normalized_parquet_per_day_sha256`, `source_normalized_manifest_sha256`, `source_successor_state_sha256`, `source_phase_4bm_d_gate_report_sha256`, `source_phase_4bm_e_outcome`, `feature_config_hash`. All label columns (`forward_log_return_*`, `forward_direction_*`, `horizon_censored_flag_*`, `label_*`), any `split_*` column, and any column containing one of the forbidden substrings in `FORBIDDEN_MODEL_MATRIX_SUBSTRINGS` (`forward_log_return`, `forward_direction`, `horizon_censored_flag`, `label_`, `split_`, `censored_`) are forbidden in the model matrix. Verified statically by `test_ml_baseline_no_leakage_v002`.

### 6.7 Transform / preprocessing

Scalers / mean / std fit on **train only**; applied to validation only. The `StreamingStandardizer.fit_partition()` helper refuses non-train partitions and raises `MlBaselineDatasetError` (verified by `test_train_only_standardizer_refuses_non_train_partition`). Welford-style accumulators in float64; per-feature epsilon clamp `1e-8`; locked rule recorded as `subtract_train_mean_divide_by_max_train_std_epsilon`. Fixed-zero imputation for null numeric features (the `rolling_missing_window_flag` / `invalid_window_flag` columns capture missingness explicitly); locked rule recorded as `fixed_zero_for_null_numeric`. Class encoding preserves the signed three-class space (`preserve_signed_three_class`). Train-only fit recorded in the local gitignored `transform_metadata.json`.

### 6.8 Baseline families implemented

Four fixed-a-priori families, each run exactly once with the locked settings declared in `ml_baseline_design_v002.BaselineSettingsSnapshot`:

| Family | Penalty | Learning rate | Batch size | Epochs | Penalty strength | Gradient-clip norm | RNG seed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `majority_class_prior` | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `persistence_past_return_sign` | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `multinomial_logistic_regression_l2` | L2 | 0.1 | 8 192 | 1 | 1e-4 | 10.0 | 20260528 |
| `multinomial_linear_classifier_l1` | L1 (proximal soft-thresholding) | 0.1 | 8 192 | 1 | 1e-4 | 10.0 | 20260528 |

All settings are fixed-a-priori declared as constants in `ml_baseline_design_v002.py`; none was tuned, swept, or selected through results. **The optional shallow tree from Phase 4bn-A §15 was intentionally NOT implemented:** `BASELINE_SHALLOW_TREE_INCLUDED = False`. Phase 4bn-B fail-closes on memory rather than running an unbounded tree fit over 74M+ train rows; the documented design decision is preserved in `ml_baseline_design_v002.py` and is consistent with Phase 4bn-A's "Optionally one shallow tree baseline only if complexity and leakage controls are explicitly bounded".

### 6.9 Metric policy

Descriptive only — class prevalence; confusion matrix; accuracy; balanced accuracy; macro F1; per-class precision / recall; log loss; Brier score; train / validation stability deltas (`validation - train` per metric); §11.6-locked cost-commensurability descriptive summary. **No PnL, no Sharpe, no Sortino, no drawdown, no equity curve, no hit-rate-as-strategy, no threshold-tuned metric, no test-set metric.**

### 6.10 Calibration

Validation-only descriptive reliability summary (per-family per-horizon decile bins of the max predicted-class probability vs. empirical accuracy). **No test calibration. No threshold tuning. No probability-to-signal conversion.**

### 6.11 Cost-aware descriptive evaluation

§11.6 = 8 bps per side / 16 bps round trip locked reference. Descriptive cost-commensurability summary: fraction of validation `|forward_log_return|` exceeding 0.5× / 1.0× / 2.0× / 5.0× the round-trip cost. **Descriptive context only; not a tradability claim, not a strategy-readiness claim, not a profitability claim.** **No PnL simulation. No strategy construction. No entry / exit rules. No trade threshold design. No order / position model. No backtest.**

## 7. Local gitignored outputs

The Phase 4bn-B run wrote seven JSON / CSV artefacts plus their canonical Phase 4bb-F sidecars under `data/research/microstructure/ml-baselines/phase-4bn-b/`. All are gitignored under `.gitignore:88: data/research/`. **None is committed.** **No model binary is persisted. No row-level prediction is persisted. No reusable split mask is persisted.**

| Artefact | Size (bytes) | SHA256 | `git check-ignore -v` |
| --- | ---: | --- | --- |
| `ml_baseline_run_manifest.json` | 7 433 | `cd436e3823d7c8e5e07431a9b11ebcf72e35e997db9a76ca865ff1885b3cfa13` | `.gitignore:88: data/research/` |
| `ml_baseline_run_manifest.json.sha256` | 96 | `b13dbedf70f02891df50d9080f904b6327f0569687c257f3840256ec9e02f293` | `.gitignore:88: data/research/` |
| `per_horizon_model_summary.json` | 60 345 | `d94f8d72781afd4c229ee7b525e8cd79f2a13a56e5a1d68e42e74724d4c396b0` | `.gitignore:88: data/research/` |
| `per_horizon_model_summary.json.sha256` | 97 | `23f91cc02a6a272b25b57cd46953f139e58beca7073351dbfa6fae4f150c03cf` | `.gitignore:88: data/research/` |
| `metrics_train_validation.csv` | 26 102 | `40cde4a01dde14e4152c4d53b70f57bc330f20d3f2ef6248b9bb18e1c190a7a8` | `.gitignore:88: data/research/` |
| `metrics_train_validation.csv.sha256` | 95 | `5b3a04fae93df8b73830b83e92addd80a498d9d0061e2e0dd9cdf9fc9b202a34` | `.gitignore:88: data/research/` |
| `calibration_summary.csv` | 6 878 | `a0f469d27c90958b2fc308b54753d97bd78830321d5954e7d30649bff4e00138` | `.gitignore:88: data/research/` |
| `calibration_summary.csv.sha256` | 90 | `1b43de79ae210b5c082c087b17eb5ca9a96c7e6990d04cd82b9e329f16ba6df9` | `.gitignore:88: data/research/` |
| `class_balance_summary.csv` | 610 | `6e6338bff25bae253d5442763fb960339a31f936e51e58ae2199af5e844df40f` | `.gitignore:88: data/research/` |
| `class_balance_summary.csv.sha256` | 92 | `41ca08d604e597aaceff0964f720742367801e6c43538539a4265933932294e6` | `.gitignore:88: data/research/` |
| `feature_schema_used.json` | 4 736 | `5f3d84b45fe8cc538c39c8ddc093625cfe6f8040a862c2e97ad970114415fac6` | `.gitignore:88: data/research/` |
| `feature_schema_used.json.sha256` | 91 | `2f99379a21a0bd6937be59b8cd6c7a048f94cba4b20028ea0c7149feca399a42` | `.gitignore:88: data/research/` |
| `transform_metadata.json` | 5 151 | `73b455af6698ab6b43536a0f1e3941bdd9d4078b619ce0287cbdc634313286b0` | `.gitignore:88: data/research/` |
| `transform_metadata.json.sha256` | 90 | `d3b91fb201b047a5e36b669ba0aac63fe225261dfe4283e524146ffecae792dd` | `.gitignore:88: data/research/` |

Sidecar format verified for every output: lowercase 64-character SHA256 + two ASCII spaces + basename + LF only (no CRLF, no BOM, no extra fields). Each sidecar's body bytes equal `f"{sha}  {basename}\n".encode()` exactly, and the recorded SHA matches the actual on-disk SHA of the paired output file. The run manifest itself records the seven artefact SHA256s and their sidecar SHA256s in its `outputs.sha256s` and `outputs.sidecar_sha256s` blocks, so the single run-manifest SHA256 `cd436e3823d7c8e5e07431a9b11ebcf72e35e997db9a76ca865ff1885b3cfa13` acts as a deterministic identity for the full output set.

Run-manifest evidence (selected fields):

```text
phase_id: 4bn-b
test_holdout_sealed: true
test_rows_loaded: 0
supervised_splits_used: [train, validation]
split_partition_counts: {train: 45, validation: 30, test: 15}
train_supervised_rows_per_horizon: {"15s": 74535440, "60s": 74535440}
validation_supervised_rows_per_horizon: {"15s": 56819649, "60s": 56819649}
train_censored_rows_per_horizon: {"15s": 0, "60s": 0}
validation_censored_rows_per_horizon: {"15s": 0, "60s": 0}
run_duration_seconds: 1034.79
label_manifest_sha256: 5e17074d…
feature_manifest_sha256: 512a0a54…
```

## 8. Validation results

- `ruff check .` → **All checks passed!** (full repo)
- `pytest tests/research/microstructure/test_ml_baseline_*.py` → **58 passed, 0 failed** in ~1 s.
- `pytest tests/` (full repo, excluding pre-existing httpx-import collection failures under `tests/unit/research/data/`, `tests/integration/`, and `tests/simulation/`) → **2376 passed, 1 skipped, 2 pre-existing failures** (`tests/unit/research/backtest/test_engine_d1a_dispatch.py::test_d1a_runner_scaffold_requires_authorization_flag` and `::test_d1a_runner_scaffold_check_imports_ok`). These two failures are pre-existing on `main` immediately before branch creation (verified by stashing the work, switching to `main == 5b938b4`, and re-running the same suite); they are unrelated to Phase 4bn-B and were not introduced by this merge. The same 15 pre-existing httpx-missing collection failures under `tests/unit/research/data/` exist on `main` and are excluded the same way; they are not introduced by this merge either.
- `mypy src` → **86 errors in 11 files (checked 148 source files)** — categorized as 55 `[type-arg]`, 10 `[var-annotated]`, 10 `[arg-type]`, 7 `[no-any-return]`, 2 `[import-not-found]`, 1 `[no-untyped-def]`, 1 `[assignment]`. The pre-existing baseline on `main` immediately before branch creation was 33 errors in 8 files. Phase 4bn-B's pure-numpy modules add `[type-arg]` and `[no-any-return]` numpy / pyarrow stub annotations that exactly match the same categories already present in the existing `descriptive_diagnostics_v002.py`, `features_compute_v002.py`, and related v002 modules. **No new error category is introduced.** mypy strict is partially aspirational against the existing baseline; no claim of mypy clean is made.
- `git diff --check main..phase-4bn-b/multi-day-v002-ml-baseline-implementation` → **clean** (no whitespace errors) after the EOF-style commit `7099da6` removed the two trailing blank lines flagged before that fix-up.
- `git diff --name-status` → matches the expected change set exactly: one `M` on `current-project-state.md`; 15 `A` on the new source / script / test / docs files.
- `git status --short` → only the expected pre-existing untracked entry `.claude/scheduled_tasks.lock`. No data file is staged or committed.
- `git check-ignore -v` for every Phase 4bn-B local output → `.gitignore:88: data/research/`. No `data/research/` or `data/microstructure/` artefact is committed.

## 9. Upstream immutability evidence

Every governed predecessor artefact re-hashed read-only pre-merge; all byte-identical (IDENTICAL pre/post — the merge touched none of these):

| Artefact | Expected / pre-merge SHA256 | Post-merge | Result |
| --- | --- | --- | --- |
| v002 label manifest | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` | same | IDENTICAL |
| v002 label manifest sidecar | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` | same | IDENTICAL |
| v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | same | IDENTICAL |
| v002 feature manifest sidecar | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` | same | IDENTICAL |
| Phase 4bm-U split-policy successor-state JSON | `6834ab11a5ac5d93b4d9f14d9b71ef3acb2a279bd8e3189fd22421598675fc9c` | same | IDENTICAL |
| Phase 4bm-U split-policy successor-state sidecar | `fa9ae709add4541111e70cfc03d9126ac40f136ea2ce1aa1abe299d3412ac0b6` | same | IDENTICAL |
| Phase 4bm-S research-use successor-state JSON | `081730006c11360692db0a99d59a0ed499f762ef4f86d6e29bdf3016550abfe7` | same | IDENTICAL |
| Phase 4bm-S research-use successor-state sidecar | `05597fe4d568f5644ad9acc914f8a3b429bc7984cf7df3a2ac3f8c7935e02551` | same | IDENTICAL |
| Phase 4bm-Q gate report | `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` | same | IDENTICAL |
| Phase 4bm-Q gate report sidecar | `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` | same | IDENTICAL |
| Phase 4bm-W `descriptive_diagnostics_summary.json` | `f4b825af2e81734007be06acac5083e2d4048b54b5650bc407d87a6fc246198a` | same | IDENTICAL |
| Phase 4bm-W summary sidecar | `ff52873c983b55cc74a0639d17ea8b3d128cdbee9c77763cd11d2e71b3820473` | same | IDENTICAL |
| Phase 4bm-W `diagnostics_manifest.json` | `ac10061d2f0257002e094d578bcc6149b1a74ca28c604fd0d0a97e5c51c26e45` | same | IDENTICAL |
| Phase 4bm-W manifest sidecar | `644506e392db46da6d27fa46519cac327136b1a05e350e2d9b231c62fce517eb` | same | IDENTICAL |

All 90 v002 label parquets + sidecars and 90 v002 feature parquets + sidecars under `data/microstructure/labels/` / `data/microstructure/features/` remain byte-identical (the runner reads them read-only via `pyarrow.parquet.read_table`).

## 10. Manifest state preservation

- **v002 label manifest** (`5e17074d…`): `research_eligible = false`; `eligibility_gate_status = "pending"`; `chronological_split_policy = "not_yet_defined"`; `label_family_research_use_authorized = false`; `stage_5_label_cleared = false`; `diagnostics_authorized = false` (historical). **No transition occurred.**
- **v002 feature manifest** (`512a0a54…`): `research_eligible = false`; `eligibility_gate_status = "pending"`; `stage_4_feature_cleared = false`. **No transition occurred.**
- Phase 4bm-S, Phase 4bm-U, and Phase 4bm-Q sibling successor-state / gate-report artefacts are byte-identical (see §9). No transition occurred.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked).

## 11. Boundary confirmations

- five new source modules, one new script, seven new tests, two new docs, and one narrow `current-project-state.md` block added; **no existing source file, test file, script, or governance memo modified**.
- no `.gitignore`, `pyproject.toml`, or `README.md` modified.
- no MCP file created or modified; no `.mcp.json` created or read; no Graphify use.
- no `data/microstructure/` artefact committed; no `data/research/` artefact committed.
- no manifest mutated; no `research_eligible` flipped; no `eligibility_gate_status` transitioned; no `chronological_split_policy` changed; no `diagnostics_authorized` / `ml_authorized` changed.
- no successor-state artefact mutated (Phase 4bm-S, Phase 4bm-U byte-identical).
- no Phase 4bm-Q gate report mutated (`8a360608…` byte-identical).
- no diagnostics rerun; no new diagnostic artefact created (the Phase 4bm-W outputs remain byte-identical and local).
- no model selected as "best"; no feature ranked / selected / pruned; no hyperparameter / threshold tuned; no model-family selection through results; no ensemble selection.
- no strategy defined or run; no trade signals generated; no PnL simulated; no backtest run; no walk-forward optimization.
- **no model binary persisted; no row-level prediction persisted; no reusable split mask persisted.**
- **test holdout sealed:** 0 test rows loaded into any supervised stream (`test_holdout_sealed = true`, `test_rows_loaded = 0`).
- no data acquired; no public / authenticated / private endpoint called; no Binance API called; no WebSocket / user-stream opened; no credential / `.env` / `.mcp.json` / MCP / Graphify used.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked).
- no retained verdict revised; no project lock loosened; no M0 amendment; no successor authorized.

## 12. Retained verdict ledger

All preserved verbatim:

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

All preserved verbatim. All prior phase results (Phase 4am .. Phase 4bn-A) preserved verbatim.

## 13. Preserved project locks

All preserved verbatim:

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 3p §4.7
- Phase 3r §8
- Phase 3v §8
- Phase 3w §6 / §7 / §8
- Phase 4j §11
- Phase 4k / 4p / 4q / 4v / 4w
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (never invoked)
- Phase 4bb-F canonical sidecar / path policy
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks
- Phase 4bm-A-P1 thin-prompt context-management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace standard

All prior phase results preserved verbatim.

## 14. No-rescue constraints

The Phase 4bn-B merge does not, and cannot, be construed as authorizing:

- any further ML-baseline expansion, calibration phase, baseline-tuning, hyperparameter sweep, threshold tuning, feature ranking, feature selection, model selection through results, ensemble construction, or "best model" picking;
- meta-labeling, ordinal target framing, regression target framing, or binary collapse of the signed three-class target;
- inclusion of 1s or 5s horizons; running shallow tree, deep-tree, random-forest, gradient-boosting, deep-learning, transformer, or any other forbidden baseline family;
- strategy research; strategy design; signal generation; trade-signal generation; PnL simulation; equity-curve construction; Sharpe / Sortino / drawdown / hit-rate-as-strategy / trade-PnL metrics; backtests; walk-forward optimization;
- use of the test holdout for training, fitting, calibration, evaluation, tuning, design, model selection, threshold selection, reporting metrics, or inspection;
- diagnostics rerun; diagnostic artefact creation; ML artefact creation beyond the Phase 4bn-B local gitignored outputs; reusable split-mask materialization;
- model binary persistence; row-level prediction persistence;
- manifest mutation; successor-state mutation; any `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` / `diagnostics_authorized` / `ml_authorized` transition from this implementation alone;
- data acquisition (no additional days / symbols / families beyond the locked 90-day v002 envelope; no mark-price / spot / cross-venue / order-book / additional aggTrades; no 30s / 5m / 30m / 1h / 4h / longer-horizon label generation; no barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels);
- research execution; paper / shadow / live-readiness / deployment / exchange-write / production keys / authenticated APIs / private endpoints / user stream / WebSockets / MCP / Graphify / `.mcp.json` / credentials;
- Phase 4 canonical; Phase 5; Phase 4bn-C; Phase 4bn-* further successors; Phase 4bo-* / Phase 4bp-*;
- old-strategy alt-symbol rerun, cooled-down-family reopening, or 5m research-thread reopening (Phase 3t closure preserved).

`RECORD_EVIDENCE_ONLY` means only that the Phase 4bn-B run produced descriptive ML-evaluation evidence under the locked design and recorded that evidence locally and gitignored. **No baseline meaningfully separates from the majority-class prior on this descriptive evaluation, and the run produces no edge, tradability, profitability, or strategy-readiness claim.** **Any further ML-baseline expansion / calibration phase / strategy research / feature ranking / model selection / hyperparameter tuning / threshold tuning / strategy / signal / PnL / backtest / paper / shadow / live-readiness / deployment / exchange-write / acquisition phase requires its own separately authorized phase.**

## 15. Successor authorization

**None.**

Not authorized by this merge:

- Phase 4bn-C — any further ML-baseline-expansion / calibration / horizon-expansion / model-family-expansion / hyperparameter-tuning / threshold-tuning / model-selection / feature-ranking / meta-labeling phase
- any strategy research, strategy design, signal generation, PnL simulation, backtest, or walk-forward phase
- any model-selection-through-results phase
- any acquisition phase (additional aggTrades / 5m / 1m / tick / mark-price / order-book / funding / OI / liquidation / cross-venue / spot acquisition)
- any manifest-transition phase (`research_eligible`, `eligibility_gate_status`, `chronological_split_policy`, `diagnostics_authorized`, `ml_authorized`)
- any successor-state-mutation phase
- Phase 4bn-* further successors / Phase 4bo-* / Phase 4bp-* / Phase 5 / Phase 4 canonical
- paper / shadow; live-readiness; deployment; exchange-write; production keys; authenticated APIs; private endpoints; user stream; WebSockets; MCP; Graphify; `.mcp.json`; credentials
- model binary persistence; row-level prediction persistence; reusable split-mask persistence
- any phase that loads the test holdout for any reason

## 16. Recommended state

**Remain paused.**

Phase 4bn-B is now merge-complete on main and, after the SHA-finalization commit and push, project-complete. The implementation decision `RECORD_EVIDENCE_ONLY` records descriptive ML-baseline evidence only and authorizes nothing further. **No baseline meaningfully separates from the majority-class prior on this descriptive evaluation.** **Any further ML-baseline expansion / calibration phase / strategy research / feature ranking / model selection / hyperparameter tuning / threshold tuning / strategy / signal / PnL / backtest / paper / shadow / live-readiness / deployment / exchange-write / acquisition phase requires its own separately authorized phase.** **Phase 4bn-C is not authorized by Phase 4bn-B.** **Recommended state remains paused.**

**Conditional next, NOT authorized:** a Phase 4bn-C ML-baseline-expansion / interpretation memo is one cleanest non-paused option. It would be a docs-only governance / interpretation phase that interprets the Phase 4bn-B descriptive evidence (which shows no meaningful separation from the majority-class prior on either included horizon) and either recommends remain-paused for the ML arc, recommends a separately authorized baseline-expansion phase with explicit pre-declared scope (e.g. add 1s / 5s horizons; add a depth-bounded shallow tree under memory-safe streaming; or add a per-class-weighted softmax variant), or recommends a separately authorized labels-rework / regime-conditioning / cost-aware target-redesign phase. Phase 4bn-C is **not authorized** by this merge. Its scope, target, baselines, and metric policy would be defined entirely by a future separately authorized scoping / design memo, not implied by this evidence.
