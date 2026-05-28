# Phase 4bn-C — Multi-Day V002 ML-Baseline Evidence Interpretation / Forensic Memo

**Phase identity:** Phase 4bn-C — Multi-Day V002 ML-Baseline Evidence Interpretation / Forensic Memo (docs-only governance / interpretation / forensic memo; Tier 1 — Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` §3; the first phase of the ML arc that interprets actual ML-baseline implementation evidence; separately authorized by the operator following the Phase 4bn-B merge-closeout `RECORD_EVIDENCE_ONLY` decision).
**Date:** 2026-05-28.
**Branch:** `phase-4bn-c/multi-day-v002-ml-baseline-evidence-interpretation`.
**Base SHA:** `main` at `3c59a323e4f0e506caf63ef73afccaf931b3c631` (Phase 4bn-B SHA-finalization commit `docs(phase-4bn-b): finalize merge closeout shas`; pre-branch `main == origin/main` verified in sync).
**Tier:** **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3. This phase interprets the first actual ML-baseline implementation evidence and may recommend whether the ML arc should remain paused, proceed to a tightly bounded baseline-expansion / design phase, revisit labels / targets, or investigate class imbalance / regime conditioning. It is adjacent to ML expansion, model selection, feature selection, hyperparameter tuning, threshold tuning, strategy research, backtests, and test-holdout misuse while explicitly authorizing none of them.
**Phase type:** docs-only governance / interpretation / forensic memo. Adds two new tracked docs files under `docs/00-meta/implementation-reports/` (this memo + the paired closeout) and narrowly updates `docs/00-meta/current-project-state.md`. **No** source / test / committed-script / configuration / manifest / sidecar / gate-report / successor-state mutation. **No** local data artefact created or mutated. **No** diagnostic rerun. **No** ML rerun. **No** ML artefact. **No** acquisition. **No** successor authorization.
**Status:** drafted; pending operator review. Branch-complete only by this work; not merged into `main`; not project-complete.

---

## 0. Required exact phrases

- **Phase 4bn-C is a docs-only ML-baseline evidence interpretation / forensic memo.**
- **Phase 4bn-C does not train ML models.**
- **Phase 4bn-C does not run ML.**
- **Phase 4bn-C does not score models.**
- **Phase 4bn-C does not generate predictions.**
- **Phase 4bn-C does not select models through results.**
- **Phase 4bn-C does not rank or select features.**
- **Phase 4bn-C does not tune hyperparameters.**
- **Phase 4bn-C does not tune thresholds.**
- **Phase 4bn-C does not define or run any strategy.**
- **Phase 4bn-C does not generate trade signals.**
- **Phase 4bn-C does not simulate PnL.**
- **Phase 4bn-C does not run backtests.**
- **Phase 4bn-C does not authorize acquisition.**
- **Phase 4bn-C does not call any public, authenticated, or private endpoint.**
- **Phase 4bn-C does not open any WebSocket or user stream.**
- **Phase 4bn-C does not use credentials, .env, .mcp.json, MCP, or Graphify.**
- **Phase 4bn-C does not mutate any manifest.**
- **Phase 4bn-C does not mutate any successor-state artefact.**
- **Phase 4bn-C does not commit data/microstructure.**
- **Phase 4bn-C does not commit data/research.**
- **Phase 4bn-C does not persist model binaries.**
- **Phase 4bn-C does not persist row-level predictions.**
- **Phase 4bn-C does not create reusable split masks.**
- **Phase 4bn-C does not authorize Phase 4bn-D, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, or any successor phase.**
- **Recommended state remains paused.**

---

## 1. Phase identity

Phase 4bn-C answers a single governance / interpretation question:

> Given Phase 4bn-B implemented exactly the Phase 4bn-A design and produced `RECORD_EVIDENCE_ONLY` evidence on the train and validation splits of the multi-day v002 BTCUSDT feature/label family — what should the project conclude about the first ML-baseline result, and what (if anything) should be recommended next under strict non-authorization boundaries?

Phase 4bn-C is **docs-only**. It reads the Phase 4bn-B local gitignored outputs read-only, interprets them descriptively, surfaces forensic hypotheses for the weak baseline-vs-prior separation, evaluates five candidate follow-up paths, and records a single recommendation. It trains nothing, scores nothing, predicts nothing, selects nothing, ranks nothing, tunes nothing, runs nothing, materializes no split mask, creates no ML artefact, mutates no manifest or successor-state artefact, acquires no data, and authorizes no successor implementation. **Phase 4bn-C is a docs-only ML-baseline evidence interpretation / forensic memo.** **This is the interpretation step of the ML arc, not ML execution.**

- **Phase name:** Phase 4bn-C — Multi-Day V002 ML-Baseline Evidence Interpretation / Forensic Memo.
- **Phase type:** docs-only governance / interpretation / forensic memo.
- **Branch:** `phase-4bn-c/multi-day-v002-ml-baseline-evidence-interpretation`.
- **Base SHA:** `main` at `3c59a323e4f0e506caf63ef73afccaf931b3c631`.
- **Authorization:** explicit operator authorization for Phase 4bn-C only.

## 2. Branch name

`phase-4bn-c/multi-day-v002-ml-baseline-evidence-interpretation`

## 3. Base SHA

`3c59a323e4f0e506caf63ef73afccaf931b3c631` (Phase 4bn-B SHA-finalization commit, `docs(phase-4bn-b): finalize merge closeout shas`; the head of `main` at branch time; `main == origin/main` verified). The Phase 4bn-B merge commit `97b3f8f50edc6c13241b4adaedd4a1eff332dea1` and merge-closeout commit `b321e5ce4419a0218341b0d35a934a10e4bf0ff0` are present on `main` immediately below this SHA-finalization commit (verified by `git log --oneline -16 --decorate`).

## 4. Predecessor chain

| Phase | Role | Status on `main` | Verdict / result |
| --- | --- | --- | --- |
| **Phase 4bm-W** | Multi-day v002 descriptive diagnostics execution | merge-complete; SHA-finalized | `DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS` (descriptive-only) |
| **Phase 4bm-Z** | Multi-day v002 ML-readiness evaluation memo | merge-complete; SHA-finalized | `RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION_SCOPING` (criteria A–R PASS) |
| **Phase 4bn-A** | Multi-day v002 ML-baseline implementation scoping / design | merge-complete; SHA-finalized | `RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION` (criteria A–U PASS) |
| **Phase 4bn-B** | Multi-day v002 ML-baseline implementation | merge-complete; SHA-finalized | `RECORD_EVIDENCE_ONLY` |

Direct predecessor for this memo:

- **Phase 4bn-B** — the docs + code + tests + local gitignored output ML-baseline implementation phase. Implements exactly the Phase 4bn-A §9 – §20 design and produces local gitignored ML-evaluation evidence under `data/research/microstructure/ml-baselines/phase-4bn-b/`. Decision: **`RECORD_EVIDENCE_ONLY`**. The Phase 4bn-B run loaded train and validation partitions only (test holdout sealed; 0 test rows loaded), trained four fixed-a-priori baseline families once each, and emitted seven JSON / CSV artefacts plus paired canonical Phase 4bb-F sidecars. Phase 4bn-C interprets that evidence and nothing else.

Phase 4bn-B lifecycle SHAs (verified present on `main`): base SHA `5b938b4ae5986874d0f7c3de6122df180c74790a`; implementation commit `2a959793fa0ed888881c7c1554d04a052a3f4e4e`; EOF-style commit / branch tip `7099da6412f6d24cd9e0258b4a031096768535ce`; merge commit `97b3f8f50edc6c13241b4adaedd4a1eff332dea1`; merge-closeout commit `b321e5ce4419a0218341b0d35a934a10e4bf0ff0`; SHA-finalization commit `3c59a323e4f0e506caf63ef73afccaf931b3c631` (this phase's base).

The chain is internally consistent. Each phase preserves the upstream artefacts byte-identically. No verdict has been revised. No project lock has been loosened.

## 5. Evidence reviewed

### 5.1 ML-arc governance evidence (docs)

- Phase 4bn-B merge-closeout, implementation report, and closeout (`RECORD_EVIDENCE_ONLY`; train/validation only; test holdout sealed; no model selected as best; no feature ranked / selected; no hyperparameter / threshold tuned; no strategy / signal / PnL / backtest; canonical Phase 4bb-F sidecars).
- Phase 4bn-A implementation scoping / design memo, closeout, merge-closeout (`RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION`; §9 – §20 design; Phase 4bn-B implements exactly that design, including the documented decision not to implement the optional shallow tree under memory fail-closed conditions).
- Phase 4bm-Z ML-readiness evaluation memo, closeout, merge-closeout (`RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION_SCOPING`; §16 cost-aware §11.6 lock; §11 split-policy restatement).
- Phase 4bm-W descriptive diagnostics report, closeout, merge-closeout (`DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS`; 0 blocking; 4 non-blocking caveats — envelope-terminal censoring asymmetry 857 rows all in test; 538 embargo-excluded earlier-split rows; approximate-quantile method; historical `diagnostics_authorized=false` manifest flag).
- `docs/00-meta/process/merge-closeout-standard.md`; `docs/00-meta/process/phase-risk-tiering-standard.md`; Phase 4bm-A-P1 thin-prompt context-management standard; Phase 4bm-D-P1 lightweight Claude Code workspace standard.
- `docs/00-meta/current-project-state.md`.

### 5.2 Phase 4bn-B local-output evidence (read-only)

Every Phase 4bn-B local gitignored output and every predecessor governed artefact was re-hashed read-only at the start of this phase and matched its expected SHA256 byte-for-byte. None was mutated; none was committed. **No ML was rerun; no diagnostics rerun; no new artefact created.**

| Artefact | Expected SHA256 | Result |
| --- | --- | --- |
| `ml_baseline_run_manifest.json` | `cd436e3823d7c8e5e07431a9b11ebcf72e35e997db9a76ca865ff1885b3cfa13` | IDENTICAL |
| `ml_baseline_run_manifest.json.sha256` | `b13dbedf70f02891df50d9080f904b6327f0569687c257f3840256ec9e02f293` | IDENTICAL |
| `per_horizon_model_summary.json` | `d94f8d72781afd4c229ee7b525e8cd79f2a13a56e5a1d68e42e74724d4c396b0` | IDENTICAL |
| `per_horizon_model_summary.json.sha256` | `23f91cc02a6a272b25b57cd46953f139e58beca7073351dbfa6fae4f150c03cf` | IDENTICAL |
| `metrics_train_validation.csv` | `40cde4a01dde14e4152c4d53b70f57bc330f20d3f2ef6248b9bb18e1c190a7a8` | IDENTICAL |
| `metrics_train_validation.csv.sha256` | `5b3a04fae93df8b73830b83e92addd80a498d9d0061e2e0dd9cdf9fc9b202a34` | IDENTICAL |
| `calibration_summary.csv` | `a0f469d27c90958b2fc308b54753d97bd78830321d5954e7d30649bff4e00138` | IDENTICAL |
| `calibration_summary.csv.sha256` | `1b43de79ae210b5c082c087b17eb5ca9a96c7e6990d04cd82b9e329f16ba6df9` | IDENTICAL |
| `class_balance_summary.csv` | `6e6338bff25bae253d5442763fb960339a31f936e51e58ae2199af5e844df40f` | IDENTICAL |
| `class_balance_summary.csv.sha256` | `41ca08d604e597aaceff0964f720742367801e6c43538539a4265933932294e6` | IDENTICAL |
| `feature_schema_used.json` | `5f3d84b45fe8cc538c39c8ddc093625cfe6f8040a862c2e97ad970114415fac6` | IDENTICAL |
| `feature_schema_used.json.sha256` | `2f99379a21a0bd6937be59b8cd6c7a048f94cba4b20028ea0c7149feca399a42` | IDENTICAL |
| `transform_metadata.json` | `73b455af6698ab6b43536a0f1e3941bdd9d4078b619ce0287cbdc634313286b0` | IDENTICAL |
| `transform_metadata.json.sha256` | `d3b91fb201b047a5e36b669ba0aac63fe225261dfe4283e524146ffecae792dd` | IDENTICAL |
| v002 label manifest | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` | IDENTICAL |
| v002 label manifest sidecar | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` | IDENTICAL |
| v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | IDENTICAL |
| v002 feature manifest sidecar | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` | IDENTICAL |

`git check-ignore -v` confirms the Phase 4bn-B outputs are covered by `.gitignore:88: data/research/`; the microstructure manifests by `.gitignore:85: data/microstructure/`. None appears as a staged or committed change. This memo reads all evidence read-only and reruns nothing.

## 6. Phase 4bn-B decision

`RECORD_EVIDENCE_ONLY` (Phase 4bn-B).

Phase 4bn-B implemented exactly the Phase 4bn-A §9 – §20 design and produced descriptive ML-baseline evidence on the train and validation splits of the multi-day v002 BTCUSDT feature / label family. It selected no model as best, ranked no feature, tuned no hyperparameter, tuned no threshold, designed no strategy, generated no signal, simulated no PnL, ran no backtest, acquired no data, called no endpoint, used no credential, mutated no manifest, mutated no successor-state artefact, persisted no model binary, persisted no row-level prediction, and created no reusable split mask. **0 test rows were loaded into any supervised stream.** The Phase 4bn-B merge-closeout records `RECORD_EVIDENCE_ONLY` verbatim and explicitly authorizes no successor phase.

## 7. Phase 4bn-B implementation boundary

Phase 4bn-B implements *exactly* the Phase 4bn-A §9 – §20 design:

- **Target framing:** direction classification only; 3-class `{-1, 0, +1}`; zero / flat preserved (not merged, not dropped); per-horizon-independent.
- **Horizons:** **15s** and **60s** included; **1s** and **5s** deferred. No horizon is declared strategy-ready or live-tradable.
- **Splits:** `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` enforced verbatim. Train 45d / 74,535,688 rows (74,535,440 supervised per included horizon after 248-row embargo). Validation 30d / 56,819,939 rows (56,819,649 supervised per included horizon after 290-row embargo). Test / final holdout 15d / 23,797,822 rows (sealed; 0 test rows loaded). Per-horizon censored-row exclusion (0 in train and validation for the two included horizons; the global 857-row censoring is concentrated on the final envelope day inside the sealed test split).
- **Feature surface:** the 45 v002 `computed_feature_column_names`. `feature_config_hash 819cfa7a…` preserved. **No new feature engineering. No feature selection. No feature ranking. No feature pruning.**
- **Excluded leakage:** the 17 v002 lineage columns, all label columns, all label-derived fields, any split-flag column, and any column matching `FORBIDDEN_MODEL_MATRIX_SUBSTRINGS`.
- **Preprocessing:** train-only `mean / std` fit; validation-only transform; per-feature epsilon clamp `1e-8`; fixed-zero null-numeric imputation; signed-three-class encoding preserved.
- **Baseline families (each run exactly once with locked SGD hyperparameters):**
  1. `majority_class_prior`
  2. `persistence_past_return_sign`
  3. `multinomial_logistic_regression_l2` (penalty L2, lr 0.1, batch 8 192, epochs 1, strength 1e-4, grad-clip 10.0, RNG seed 20260528)
  4. `multinomial_linear_classifier_l1` (penalty L1 proximal soft-thresholding, otherwise identical settings)
- **Optional shallow tree:** intentionally **not** implemented. `BASELINE_SHALLOW_TREE_INCLUDED = False`. Phase 4bn-B fail-closes on memory rather than running an unbounded tree fit over 74M+ train rows; consistent with Phase 4bn-A §15 "Optionally one shallow tree baseline only if complexity and leakage controls are explicitly bounded". The Phase 4bn-B merge-closeout records this decision verbatim.
- **Metric policy:** descriptive only. **No PnL, no Sharpe, no Sortino, no drawdown, no equity curve, no hit-rate-as-strategy, no threshold-tuned metric, no test-set metric.**
- **Calibration:** validation-only descriptive reliability summary. **No test calibration. No threshold tuning. No probability-to-signal conversion.**
- **Cost-aware descriptive evaluation:** §11.6 = 8 bps per side / 16 bps round trip locked reference. Descriptive only.
- **Outputs:** seven local gitignored artefacts plus paired canonical Phase 4bb-F sidecars under `data/research/microstructure/ml-baselines/phase-4bn-b/`. **No model binaries persisted. No row-level predictions persisted. No reusable split masks persisted.**

## 8. Phase 4bn-B validation and local-output evidence

- `ruff check .` → All checks passed (full repo).
- `pytest tests/research/microstructure/test_ml_baseline_*.py` → 58 passed.
- Full repo `pytest` → 2376 passed, 1 skipped, 2 pre-existing failures (`test_engine_d1a_dispatch.py::test_d1a_runner_scaffold_*`); identical pre-existing state on `main` immediately before branch creation; not introduced by Phase 4bn-B.
- `mypy src` → 86 errors in 11 files (pre-existing baseline 33 errors in 8 files; Phase 4bn-B adds `[type-arg]` / `[no-any-return]` numpy / pyarrow stub annotations of the same categories as the existing v002 modules; no new error category). mypy strict is partially aspirational against the existing baseline; no claim of mypy clean is made.
- `git diff --check` clean.
- `git check-ignore -v` confirms every Phase 4bn-B local output is covered by `.gitignore:88: data/research/`; no `data/research/` or `data/microstructure/` artefact is committed.
- Phase 4bn-B run identity: `ml_baseline_run_manifest.json` SHA256 `cd436e3823d7c8e5e07431a9b11ebcf72e35e997db9a76ca865ff1885b3cfa13`; embeds `test_holdout_sealed: true`, `test_rows_loaded: 0`, `supervised_splits_used: [train, validation]`, `split_partition_counts: {train: 45, validation: 30, test: 15}`, `train_supervised_rows_per_horizon: {15s: 74535440, 60s: 74535440}`, `validation_supervised_rows_per_horizon: {15s: 56819649, 60s: 56819649}`, `train_censored_rows_per_horizon: {15s: 0, 60s: 0}`, `validation_censored_rows_per_horizon: {15s: 0, 60s: 0}`, and a 43-key `non_authorization` block (all flags `false`).

## 9. Interpretation of class prevalence / majority prior dominance

**Reading the actual class balance evidence in `class_balance_summary.csv` / `per_horizon_model_summary.json` (recorded by Phase 4bn-B; not recomputed here) overturns one common assumption about a direction-classification problem on this family.**

| Split × horizon | Down prevalence | Flat prevalence | Up prevalence |
| --- | ---: | ---: | ---: |
| train × 15s | 0.4957 | 0.0109 | 0.4934 |
| train × 60s | 0.5016 | 0.0019 | 0.4965 |
| validation × 15s | 0.4938 | 0.0082 | 0.4980 |
| validation × 60s | 0.4950 | 0.0015 | 0.5036 |

The **`flat` class is small** in this label scheme — between **0.15 % and 1.09 %** of supervised rows across both included horizons in both splits. Direction at 15s / 60s is essentially a near-balanced binary problem in practice (down ≈ up ≈ 0.495 ± 0.005), with a thin sliver of strictly-zero forward returns. This is the opposite of what a casual reading might assume: the flat class is *underrepresented*, not dominant.

Consequences for interpretation:

1. The majority-class baseline accuracy floor on validation is **0.4938 (15s)** and **0.4950 (60s)** — i.e. ~50 %. The majority class is `up` at 15s and `up` at 60s on validation in this run (the marginally larger class). Macro F1 at the majority baseline is **0.2204 (15s)** and **0.2207 (60s)** — the floor on macro F1 is much lower than the floor on accuracy because the majority baseline never predicts the other two classes.
2. **Accuracy alone is a weak indicator in this regime.** A small accuracy lift over 0.4938 might come from learning a tiny class skew rather than from genuine directional signal. Balanced accuracy and macro F1 are more honest indicators, and the prior floors there are 0.3333 and ~0.22 respectively.
3. **Beating the majority prior by a few percentage points of accuracy does not imply usable signal.** The L2 / L1 linear classifiers reach 0.5435 accuracy at 15s (a ~5 pp lift) and 0.5095 at 60s (a ~1.5 pp lift). On macro F1, the lift is more striking (0.3638 vs 0.2204 at 15s, and 0.3291 vs 0.2207 at 60s) — but that lift is structurally driven by the linear models predicting **both** the up and down classes, which the majority baseline never does. None of these lifts is a tradability claim, an edge claim, a profitability claim, or a strategy-readiness claim.
4. **The `flat` class is never predicted by the L2 / L1 linear classifiers** in this run — the per-class precision / recall / F1 for `flat` is `0.0 / 0.0 / 0.0` in every validation block, and the confusion matrix shows `pred_flat: 0` across the board. This is the expected behavior of multinomial softmax on a class with sub-1 % prevalence and no obvious separating feature: argmax never selects it. **No threshold-aware re-balancing was performed and is not authorized here.**
5. **No new metrics are computed by this memo.** All numbers in §9 – §13 are read from the existing Phase 4bn-B local outputs; the Phase 4bn-C interpretation surfaces existing facts.

This memo does **not** convert any of these observations into a model recommendation, a feature recommendation, a threshold recommendation, or a strategy recommendation.

## 10. Interpretation of persistence baseline underperformance

Persistence (`persistence_past_return_sign`) uses the sign of `rolling_log_return_past_window_{horizon}` as its prediction and assigns hard probability 1.0 to that class. On the descriptive metric set:

| Metric | majority 15s | persistence 15s | majority 60s | persistence 60s |
| --- | ---: | ---: | ---: | ---: |
| Accuracy | 0.4938 | 0.5167 | 0.4950 | 0.4973 |
| Balanced accuracy | 0.3333 | 0.3835 | 0.3333 | 0.3391 |
| Macro F1 | 0.2204 | 0.3839 | 0.2207 | 0.3394 |
| Mean log-loss | 0.7355 | **13.353** | 0.7032 | **13.889** |
| Mean Brier | 0.5081 | **0.9665** | 0.5015 | **1.0053** |

Interpretation:

1. On **hard accuracy**, persistence is slightly above majority on both horizons in this run (about +2.3 pp at 15s; +0.2 pp at 60s). The Phase 4bn-B prompt's prior characterization "persistence is below the majority-class floor on validation" was based on probabilistic / proper-scoring-rule metrics, not on hard accuracy; this memo records the precise observation from the local outputs: persistence beats majority on hard accuracy, but **persistence is catastrophically worse on log-loss and Brier** (~18× and ~2× the majority floor respectively).
2. The catastrophic log-loss / Brier gap is structural: persistence emits one-hot probabilities (1.0 on its predicted class), so every miss costs `−log(ε) ≈ 27.6 nats` per row. **This is not negative evidence about momentum / continuation per se; it is direct evidence that hard-class persistence outputs are uncalibrated.** Persistence is **not** a calibrated probabilistic baseline.
3. **This is negative evidence for the naive momentum / continuation assumption at face value** under the current label scheme: a model that simply follows the past-window sign of the same return statistic is only ~2.3 pp better than chance at 15s and barely better than chance at 60s. **This memo does not convert that into a strategy conclusion.** This memo does not recommend a reversal strategy, does not recommend a non-reversal strategy, and does not recommend any strategy at all.
4. The reasonable forensic reading is: any future scoping must be honest that any modest persistence-flavored lift is dominated by class-balance effects and that probabilistic / calibrated baselines are the right reference for comparing against more flexible models, not the persistence baseline.

## 11. Interpretation of L2 / L1 marginal lift

The two SGD-fitted linear softmax baselines (`multinomial_logistic_regression_l2`, `multinomial_linear_classifier_l1`) produce almost identical results in this run (L1 and L2 differ in the fourth significant figure on every metric, which is consistent with the weak penalties `1e-4`; in this regime the L1 proximal soft-thresholding does not produce visibly sparser weights at the metric level):

| Metric | L2 / 15s | L2 / 60s | L2 - majority / 15s | L2 - majority / 60s |
| --- | ---: | ---: | ---: | ---: |
| Accuracy | 0.5435 | 0.5095 | +0.0497 pp | +0.0145 pp |
| Balanced accuracy | 0.3654 | 0.3412 | +0.0321 pp | +0.0079 pp |
| Macro F1 | 0.3638 | 0.3291 | +0.1434 pp | +0.1084 pp |
| Mean log-loss | 0.7259 | 0.7128 | −0.0096 | +0.0095 |
| Mean Brier | 0.5045 | 0.5096 | −0.0036 | +0.0081 |

Train-validation deltas (validation minus train) are small and approximately matched in sign across L1 and L2: accuracy −0.0053 / −0.0025, balanced accuracy −0.0046 / −0.0004, macro F1 −0.0040 / −0.0079, mean log-loss −0.0068 / −0.0039 on 15s / 60s. **The models are not overfitting** at this level of descriptive measurement: train and validation match within roughly half a percentage point on the hard metrics.

Per-class precision / recall on validation (L2):

- **15s:** down (P 0.540 / R 0.560 / F1 0.550) and up (P 0.547 / R 0.536 / F1 0.542); flat (0 / 0 / 0).
- **60s:** down (P 0.504 / R 0.695 / F1 0.584) and up (P 0.522 / R 0.328 / F1 0.403); flat (0 / 0 / 0).

Interpretation:

1. **At 15s, the linear softmax baselines produce a real but small accuracy lift over the majority prior** (~5 pp), distributed evenly across the up / down classes (per-class F1 ≈ 0.54 on each). The lift on macro F1 (~14 pp) is mostly driven structurally by the linear models predicting both classes while the majority baseline predicts one.
2. **At 60s, the lift collapses to ~1.5 pp on accuracy and ~11 pp on macro F1**, and the model becomes strongly down-biased on the predictions (38.8 M `pred_down` rows vs 18.0 M `pred_up` rows on validation). The 60s confusion matrix shows the down / up F1 asymmetry (0.584 / 0.403) directly. **This is descriptive evidence that whatever signal the 45-column linear model has access to is mostly active at 15s and decays sharply by 60s.**
3. **`Statistical descriptive lift` is not the same as `economically useful signal`.** The §11.6 round-trip cost lock is 16 bps, and the validation `|forward_log_return|` distribution at 15s shows only ~6.2 % of rows exceed that threshold (see §13 below). A ~5 pp accuracy lift on a near-50/50 binary problem, in a regime where 94 % of rows have absolute moves smaller than the round-trip cost, is **not a tradability claim**. Phase 4bn-C does not convert it into one.
4. **No model is selected as "best".** Phase 4bn-C does not recommend "use L2 over L1", "use 15s over 60s", "use linear over majority", or any equivalent selection-through-results conclusion. The two linear models are reported alongside each other as the design instructed; neither was tuned; neither was chosen.

## 12. Interpretation of calibration / probability-output evidence

The Phase 4bn-B `calibration_summary.csv` records a 10-bin descriptive reliability summary on validation (the maximum predicted-class probability bin vs. the empirical accuracy for that bin). For the L2 logistic regression at 15s:

| Bin | n_rows | mean max p̂ | empirical acc | reliability gap |
| --- | ---: | ---: | ---: | ---: |
| 0.4 – 0.5 | 1 520 238 | 0.4961 | 0.4904 | −0.0057 |
| 0.5 – 0.6 | 48 889 658 | 0.5478 | 0.5432 | −0.0047 |
| 0.6 – 0.7 | 5 839 614 | 0.6226 | 0.5616 | **−0.0610** |
| 0.7 – 0.8 | 392 090 | 0.7395 | 0.5354 | **−0.2041** |
| 0.8 – 0.9 | 123 119 | 0.8416 | 0.4881 | **−0.3535** |
| 0.9 – 1.0 | 54 930 | 0.9408 | 0.5492 | **−0.3916** |

Interpretation:

1. **~86 % of L2-15s validation predictions live in the 0.5 – 0.6 confidence bin**, and that bin is well calibrated (reliability gap −0.0047). This is consistent with the model hedging close to 50 / 50 across most of the validation distribution.
2. **The high-confidence tail is severely over-confident.** When the model claims 0.84 – 0.94 confidence (~178 K rows total), the empirical accuracy is 0.49 – 0.55 — i.e. *no better than majority*, and in the 0.8 – 0.9 bin actually below the majority floor.
3. **Implication for any future threshold-based or confidence-conditional follow-up:** the obvious "just predict only when confident" idea would *fail under this evidence*; the most-confident validation predictions are not the most-accurate ones. Phase 4bn-C records this descriptively only and **does not tune any threshold, does not propose a confidence cut, and does not convert any probability into a trade signal.**
4. **Persistence calibration** is degenerate by construction: all 56 819 649 validation rows fall in the [0.9, 1.0) bin because persistence emits hard one-hot probabilities; mean max p̂ = 1.0; empirical accuracy = 0.5167; gap = −0.4833. Persistence is **not** a calibrated probabilistic baseline.
5. **No calibration transform is fit, no isotonic / Platt rescaling is performed, and no calibrator is selected.** The reliability summary is descriptive only.

## 13. Interpretation of §11.6 cost-commensurability context

The Phase 4bn-B `cost_commensurability` block (under each baseline's validation block in `per_horizon_model_summary.json`) records the fraction of validation `|forward_log_return|` rows exceeding multiples of the 16 bps round-trip cost (these are identical across baselines because they depend only on the forward-return distribution, not on predictions):

| Multiple of round-trip cost | 15s validation | 60s validation |
| --- | ---: | ---: |
| 0.5× (8 bps) | 0.1888 | 0.3989 |
| 1.0× (16 bps) | 0.0622 | 0.1829 |
| 2.0× (32 bps) | 0.0157 | 0.0578 |
| 5.0× (80 bps) | 0.0016 | 0.0093 |

Interpretation:

1. **At 15s only ~6.2 % of validation rows have `|return| > 1× round-trip cost`.** Even if the model perfectly predicted direction on every row, only 6.2 % of those calls would clear transaction costs before slippage, latency, or any other realistic friction. The cost-commensurability fraction is **descriptive context** — it tells the operator how rarely the cost threshold is exceeded *by raw return magnitudes alone* — and it is **not** a strategy recommendation, a tradability claim, or a backtest result.
2. **At 60s ~18.3 % exceed 1× cost** and ~5.8 % exceed 2× cost; the cost-commensurability fraction grows roughly proportionally to horizon as expected for a roughly-random-walk price process. The 60s descriptive context is more favourable than 15s on this axis — but the L2 accuracy lift at 60s is only ~1.5 pp, so the two effects work in opposite directions.
3. The §11.6 lock is preserved verbatim. **No PnL is simulated.** **No strategy is constructed.** **No entry / exit / threshold / order / position rule is designed.** **No backtest is run.** Phase 4bn-C carries the locked reference forward as descriptive context and nothing more.

## 14. Interpretation of test-holdout protection

- The test split (2025-02-14 .. 2025-02-28; 15 partitions; 23,797,822 rows) is **sealed**. **`test_rows_loaded: 0`** is recorded in `ml_baseline_run_manifest.json`; the dataset module's `iter_partitions(split="test", ...)` raises `MlBaselineDatasetError` because `test ∉ SUPERVISED_SPLITS`, verified by `test_ml_baseline_split_policy_v002.test_test_holdout_iteration_is_forbidden_by_design`.
- Phase 4bn-C **must not** inspect, evaluate, tune, design, model-select, threshold-select, or report any metric on test data. The test holdout remains single-use and is reserved for a future separately authorized terminal-holdout evaluation phase, if one is ever proposed.
- The known envelope-terminal censoring asymmetry (857 rows: 1s 14 / 5s 39 / 15s 170 / 60s 634, all concentrated on 2025-02-28 inside the sealed test split) is carried forward as a non-blocking caveat for any future test-holdout evaluation phase. **It is not addressed by Phase 4bn-C.**
- **Phase 4bn-C reads no test data, references no test metrics, and proposes no test-time evaluation.**

## 15. Forensic hypotheses for weak baseline-vs-prior separation

The weak validation-vs-prior separation evidence in §9 – §13 admits several non-mutually-exclusive forensic hypotheses. **Phase 4bn-C surfaces them; it does not resolve them through execution.**

H1. **Label imbalance / flat-class collapse.** The strict-sign flat class is 0.15 – 1.09 % of supervised rows. Multinomial softmax with no class weighting never predicts flat (per §11). Any descriptive macro-F1 lift over majority is structurally driven by predicting both up and down at all rather than learning a useful flat decision boundary.

H2. **Target definition is too blunt or too noisy.** The strict-sign label `forward_direction_{horizon} = sign(forward_log_return_{horizon})` collapses magnitude information. A 0.0001 bp move and a 100 bp move both contribute the same gradient. Most validation rows have `|return|` well below cost (§13). The signal-to-cost-resolution ratio in the label may be poor for what a useful model would need.

H3. **The included horizons are still not cost-commensurate.** At 15s, only 6.2 % of rows exceed 1× round-trip cost; at 60s, 18.3 % do. A horizon that produces moves above the cost threshold for a larger fraction of rows might admit a more direct cost-aware framing. **This is a question, not a recommendation.**

H4. **The v002 feature surface lacks enough predictive information.** The 40-column rolling-window feature set is derived from aggregated aggTrade microstructure (counts, sums, means, aggressive-side imbalances, past-window log returns) plus 5 deterministic time / flag columns. The linear models extract ~5 pp accuracy at 15s and ~1.5 pp at 60s from this surface. It is possible that linear classifiers cannot project this feature surface onto a usefully separable directional decision boundary, or that the surface itself does not carry enough information.

H5. **Linear / logistic models may be too simple for the underlying structure.** Softmax regression is a single-layer model with no interactions. If the feature-to-direction relationship is non-linear or interaction-driven, a linear baseline will read as weak even if richer-but-still-bounded models could read as marginally less weak. **The Phase 4bn-A design's optional shallow tree was intentionally not implemented under memory fail-closed conditions; that decision is preserved.**

H6. **Class weighting was absent by design.** Phase 4bn-A §15 fixed the baseline scaffolding without class weights. The flat-class collapse and the down-bias at 60s are exactly the behaviours an un-weighted softmax produces in this regime.

H7. **The shallow tree was excluded by memory fail-closed.** A depth-limited tree might (or might not) admit a slightly different decision boundary. **Phase 4bn-A's design boundary for that family — "Optionally one shallow tree baseline only if complexity and leakage controls are explicitly bounded" — is preserved verbatim.** Phase 4bn-C does **not** authorize implementing it.

H8. **Regime heterogeneity.** The 90-day window straddles December 2024 through February 2025. A regime-averaged linear baseline may be averaging across regimes with different conditional class distributions, attenuating the per-regime lift to a small global mean lift. **This is a question for a future scoping phase, not an answer.**

H9. **Time-of-day effects.** The 5 non-windowed features include `utc_hour` and `utc_minute`; the linear models see these directly. A linear baseline can fit at most a per-hour mean effect; if the relevant time effect is non-linear or interacts with the rolling features, the linear model will underuse it.

H10. **Feature stationarity drift.** The linear standardization is fit on train-only mean/std. If the validation period has materially different feature scales, the standardization is mis-applied. The Phase 4bn-B `transform_metadata.json` records the train fit; no validation-vs-train drift comparison is computed by Phase 4bn-B and **none is computed here**.

H11. **Labels may be capturing common no-move behavior more than exploitable directional edge.** The cost-commensurability evidence (§13) suggests that most directional moves at 15s are below the cost threshold. A model can be accurate on direction in a regime where direction is economically irrelevant.

H12. **The market may not contain a simple exploitable edge under this data / label / feature family.** This is a hypothesis, not a verdict. Strategy and tradability are explicitly out of scope for Phase 4bn-C.

The hypotheses above are **not ranked**, **not weighted**, **not resolved**, **not converted into design proposals**, and **not converted into strategy proposals**. They are recorded so that a future separately authorized scoping memo can choose which (if any) to bound and evaluate.

## 16. Decision

**`RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING`.**

This recommends only that a future, separately authorized **docs-only / design-only scoping** phase may scope a bounded baseline-expansion attempt. It does **not** authorize implementation, model training, model scoring, prediction generation, feature ranking / selection, model selection through results, hyperparameter tuning, threshold tuning, strategy, signals, PnL simulation, backtests, acquisition, manifest mutation, successor-state mutation, paper / shadow / live-readiness, deployment, or exchange-write.

## 17. Rationale for chosen decision

Phase 4bn-C considered five candidate decisions (§18). The evidence in §9 – §15 supports `RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING` for the following reasons.

1. **The Phase 4bn-B evidence is non-trivial but not strategy-ready, and the most obvious "next step" idea would fail under the existing evidence.** The L2 / L1 linear classifiers produce a real ~5 pp accuracy lift at 15s and a ~14 pp macro-F1 lift over the majority prior, with controlled train-validation deltas (~0.5 pp). Train-validation stability is small, so the lift is not overfitting at this level of measurement. But the calibration summary (§12) shows the model's high-confidence predictions are *no better than chance*, which means a naive "threshold the probabilities and trade only when confident" follow-up would actively make things worse. The questions to answer next are subtle (class weighting? horizon decay? memory-bounded tree? regime conditioning?). A scoping phase that enumerates exactly which questions could be evaluated, and under what predeclared evaluation rules, is the appropriate next step.
2. **Remaining strictly paused (option 1) over-claims confidence in the negative direction.** The 15s lift is reproducible (controlled train/validation stability), and the macro-F1 lift over majority is large in proportional terms. Concluding "no further ML work is warranted" from this evidence alone would be as much of an over-reading as concluding "the project has predictive edge". A scoping memo is cheaper and more honest than either.
3. **Label / target rework scoping (option 3) is a legitimate question but premature.** The Phase 4bn-B label scheme is exactly what Phase 4bn-A locked. Reworking labels before a baseline-expansion scoping memo runs the risk of explaining away the existing weak-but-real signal rather than understanding it. The hypothesis H2 / H11 questions about label bluntness are real and should be on the scoping menu, but they belong inside a bounded scoping memo rather than as the immediate next phase.
4. **Class-imbalance / regime-conditioning scoping (option 4) is a subset of option 2.** The flat-class collapse (§9), the 60s down-bias asymmetry (§11), and the time-of-day / regime hypotheses (H8 / H9) all motivate this family of questions. They are appropriately scoped as candidate questions inside a bounded baseline-expansion scoping memo, not as a separate concurrent scoping phase.
5. **Stopping further ML work on the current v002 family (option 5) is unwarranted by this evidence.** The Phase 4bn-B evidence does not rule out useful signal under different class-handling / horizon / regime / target framing; it only shows that **the four fixed-a-priori baselines locked by Phase 4bn-A produce a small accuracy lift with poor high-confidence calibration**. A "stop work" verdict needs stronger negative evidence than this.
6. **A bounded ML-baseline expansion scoping memo authorizes nothing executable.** It would be docs-only / design-only, just like Phase 4bn-A. It would enumerate at design level — without running anything — exactly which questions could be evaluated by a possible future implementation phase, under what predeclared decision rules, with what fixed-a-priori settings, and with the test holdout still sealed. The candidate questions §18 lists are real and warrant the discipline of pre-declaration.

**`RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING` means only:** a future, separately authorized docs-only / design-only scoping phase may scope a bounded baseline-expansion attempt. It does not itself authorize any implementation, any ML, any execution, or any successor phase.

## 18. What a future follow-up phase would be allowed to evaluate, if separately authorized

A future, separately authorized **bounded ML-baseline expansion scoping** phase (provisionally `Phase 4bn-D`, **not** authorized here) would be permitted to evaluate, at design level only and without running anything:

- whether class weighting should be evaluated (e.g. inverse-prevalence per-class weights in the softmax loss; declared a priori, not selected through results);
- whether a memory-bounded shallow tree baseline can be specified that respects the Phase 4bn-A §15 boundary and a streaming-safe memory profile (e.g. depth-bounded with a fixed pre-declared `max_depth` and chunked / sampled training that fail-closes on memory rather than implicitly downsampling for headline metrics);
- whether the §17 calibration evidence motivates a descriptive-only validation-side calibration analysis (reliability gaps per bin; per-class reliability; per-horizon reliability) without proposing any threshold tuning or probability-to-signal conversion;
- whether 1s / 5s should remain deferred or be partially included for descriptive parity (acknowledging that 1s / 5s carry latency / tradability sensitivity per Phase 4bm-Z / Phase 4bn-A and remain non-strategy-ready);
- whether 15s / 60s should be re-evaluated under class-weighted softmax losses, without tuning weights through validation;
- whether target balance thresholds (the strict-sign zero-class definition) should be reconsidered at scoping level only (without authorizing any label regeneration);
- whether time-of-day or regime segmentation should be scoped at design level, including how to enforce no train/test leakage and how to avoid using validation distributions to design segments.

The same scoping memo, if it instead recommends label / target rework, would be permitted to evaluate:

- whether the flat-class thresholds in `forward_direction_*` should be revisited (descriptive-only, no regeneration);
- whether magnitude-aware labels (e.g. ordinal bins, residual magnitude, magnitude-conditional direction) should be considered at design level only;
- whether cost-aware labels (where the class threshold is tied to the §11.6 cost lock) should be considered at design level only;
- whether barrier or target-before-stop labels should be considered later (recorded at design level only; no label generation, no acquisition, no strategy or PnL labels);
- whether the included horizons should be revised (descriptive-only).

The same scoping memo, if it instead recommends class-imbalance / regime conditioning, would be permitted to evaluate:

- class weights at design level (no execution);
- per-horizon prevalence thresholds at design level;
- per-time-of-day descriptive summaries at design level;
- validation-only regime summaries at design level;
- no train/test leakage in any proposed segmentation;
- no execution of any of the above.

**Any of these candidate scoping memos must:** keep the test holdout sealed; not train models; not score models; not generate predictions; not select models through results; not rank or select features; not tune hyperparameters or thresholds; not define or run strategy; not generate trade signals; not simulate PnL; not run backtests; not authorize acquisition; not call any endpoint; not use credentials / `.env` / `.mcp.json` / MCP / Graphify; not mutate any manifest; not mutate any successor-state artefact; not commit `data/microstructure/`; not commit `data/research/`; not persist model binaries; not persist row-level predictions; not create reusable split masks; not authorize Phase 5, paper / shadow, live-readiness, deployment, or exchange-write.

## 19. What this phase does not authorize

Phase 4bn-C is docs-only and authorizes **nothing executable**. It does not, and cannot, authorize:

- any ML training, model scoring, prediction generation, feature ranking, feature selection, feature pruning, model selection through results, hyperparameter tuning, threshold tuning, meta-labeling, or ensemble construction;
- any strategy research, strategy design, signal generation, trade-signal generation, PnL simulation, equity-curve construction, Sharpe / Sortino / drawdown / hit-rate / trade-PnL metrics, backtests, or walk-forward optimization;
- any use of the test holdout for training, fitting, calibration, evaluation, tuning, design, model selection, threshold selection, reporting, or inspection;
- any diagnostics rerun, diagnostic artefact creation, ML artefact creation, reusable split-mask materialization, or row-level prediction persistence;
- any data acquisition (no additional days / symbols / families beyond the locked 90-day v002 envelope; no mark-price / spot / cross-venue / order-book / additional aggTrades; no longer-horizon labels; no MFE / MAE / R-multiple / barrier / target-before-stop / PnL labels);
- any public / authenticated / private endpoint call; any WebSocket / user stream; any credential / `.env` / `.mcp.json` / MCP / Graphify use;
- any manifest mutation, successor-state mutation, or change to `research_eligible`, `eligibility_gate_status`, `chronological_split_policy`, `diagnostics_authorized`, or `ml_authorized` on any on-disk manifest;
- any source / test / committed-script / config / `.gitignore` / `pyproject.toml` / `README.md` / MCP-file modification;
- any commit under `data/microstructure/` or `data/research/`;
- Phase 4bn-D or any successor phase; Phase 5; Phase 4 canonical; paper / shadow; live-readiness; deployment; exchange-write; production-key creation;
- any revision of a retained verdict, any loosening of a project lock, or any amendment of M0 / Phase 4al / Phase 4aw / Phase 4bb-F / Phase 4bl-F / Phase 4bm-A-P1 / Phase 4bm-D-P1.

**Phase 4bn-C is a docs-only ML-baseline evidence interpretation / forensic memo.** **Phase 4bn-C does not train ML models.** **Phase 4bn-C does not run ML.** **Phase 4bn-C does not score models.** **Phase 4bn-C does not generate predictions.** **Phase 4bn-C does not select models through results.** **Phase 4bn-C does not rank or select features.** **Phase 4bn-C does not tune hyperparameters.** **Phase 4bn-C does not tune thresholds.** **Phase 4bn-C does not define or run any strategy.** **Phase 4bn-C does not generate trade signals.** **Phase 4bn-C does not simulate PnL.** **Phase 4bn-C does not run backtests.** **Phase 4bn-C does not authorize acquisition.** **Phase 4bn-C does not call any public, authenticated, or private endpoint.** **Phase 4bn-C does not open any WebSocket or user stream.** **Phase 4bn-C does not use credentials, .env, .mcp.json, MCP, or Graphify.** **Phase 4bn-C does not mutate any manifest.** **Phase 4bn-C does not mutate any successor-state artefact.** **Phase 4bn-C does not commit data/microstructure.** **Phase 4bn-C does not commit data/research.** **Phase 4bn-C does not persist model binaries.** **Phase 4bn-C does not persist row-level predictions.** **Phase 4bn-C does not create reusable split masks.** **Phase 4bn-C does not authorize Phase 4bn-D, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, or any successor phase.**

## 20. Retained verdicts preserved

All preserved verbatim:

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL — other
- **5m thread** — OPERATIONALLY CLOSED (per Phase 3t)
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

All prior phase results (Phase 4am .. Phase 4bn-B) preserved verbatim.

## 21. Project locks preserved

All preserved verbatim:

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% risk per trade / 2× leverage cap / one-position max / mark-price stops
- Phase 3p §4.7 strict integrity gate
- Phase 3r §8 mark-price gap governance
- Phase 3v §8 stop-trigger-domain governance
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance
- Phase 4j §11 metrics OI-subset partial-eligibility rule
- Phase 4k / 4p / 4q / 4v / 4w methodology + strategy-spec locks
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (never invoked by Phase 4bn-C)
- Phase 4bb-F canonical sidecar / path policy
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks
- Phase 4bm-A-P1 thin-prompt context-management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace standard

## 22. Recommended next state

**Remain paused.** Phase 4bn-C is branch-complete only by this work. Per the Phase 4bk-A workflow standard, it is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1). The interpretation decision is `RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING`; this is a recommendation only and authorizes nothing. **Phase 4bn-D is not authorized by Phase 4bn-C.** **Any bounded ML-baseline expansion scoping memo requires a separately authorized phase.** **Recommended state remains paused.**

**Conditional next, NOT authorized:** a Phase 4bn-D docs-only / design-only bounded ML-baseline expansion scoping memo is the cleanest non-paused option. It would enumerate, at design level only and without running anything, exactly which §18 candidate questions could be evaluated by a possible future implementation phase, under what predeclared evaluation rules, and with the test holdout still sealed. Phase 4bn-D is **not authorized** by this merge.
