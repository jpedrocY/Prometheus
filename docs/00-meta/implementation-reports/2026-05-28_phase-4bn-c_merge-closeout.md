# Phase 4bn-C — Merge Closeout

**Phase 4bn-C is now merge-complete on main.** **Phase 4bn-C is a docs-only ML-baseline evidence interpretation / forensic memo.** **Phase 4bn-C does not train ML models.** **Phase 4bn-C does not run ML.** **Phase 4bn-C does not score models.** **Phase 4bn-C does not generate predictions.** **Phase 4bn-C does not select models through results.** **Phase 4bn-C does not rank or select features.** **Phase 4bn-C does not tune hyperparameters.** **Phase 4bn-C does not tune thresholds.** **Phase 4bn-C does not define or run any strategy.** **Phase 4bn-C does not generate trade signals.** **Phase 4bn-C does not simulate PnL.** **Phase 4bn-C does not run backtests.** **Phase 4bn-C does not authorize acquisition.** **Phase 4bn-C does not call any public, authenticated, or private endpoint.** **Phase 4bn-C does not open any WebSocket or user stream.** **Phase 4bn-C does not use credentials, .env, .mcp.json, MCP, or Graphify.** **Phase 4bn-C does not mutate any manifest.** **Phase 4bn-C does not mutate any successor-state artefact.** **Phase 4bn-C does not commit data/microstructure.** **Phase 4bn-C does not commit data/research.** **Phase 4bn-C does not persist model binaries.** **Phase 4bn-C does not persist row-level predictions.** **Phase 4bn-C does not create reusable split masks.** **Phase 4bn-C does not authorize Phase 4bn-D, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, or any successor phase.** **Recommended state remains paused.**

## 1. Phase identity

- **Phase:** Phase 4bn-C — Multi-Day V002 ML-Baseline Evidence Interpretation / Forensic Memo.
- **Type:** docs-only governance / interpretation / forensic memo (Tier 1 — Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` §3). First phase of the ML arc that interprets actual ML-baseline implementation evidence.
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bn-C interpretation memo + closeout + the narrow `current-project-state.md` paragraph + Current-phase block onto `main`, recording the interpretation decision `RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING` as project state. The phase reads Phase 4bn-B local gitignored outputs read-only, interprets them descriptively, surfaces twelve forensic hypotheses for the weak baseline-vs-prior separation, evaluates five candidate follow-up paths, and records a single recommendation. It trains, scores, predicts, selects, ranks, and tunes nothing.
- **Target branch:** `main`.
- **Source branch:** `phase-4bn-c/multi-day-v002-ml-baseline-evidence-interpretation`.

## 2. SHAs

- **`main` SHA before merge:** `3c59a323e4f0e506caf63ef73afccaf931b3c631` (Phase 4bn-B SHA-finalization commit `docs(phase-4bn-b): finalize merge closeout shas`; `main == origin/main` verified pre-merge).
- **Base SHA:** `3c59a323e4f0e506caf63ef73afccaf931b3c631`.
- **Branch tip SHA before merge:** `148e4dffa49dcc5fa4136ac29d7e3846bcd81b85`.
- **Docs commit SHA:** `148e4dffa49dcc5fa4136ac29d7e3846bcd81b85` (`docs(phase-4bn-c): interpret ml-baseline evidence`; the memo + closeout + current-project-state block are a single docs commit, which is also the branch tip).
- **Merge commit SHA:** `cf6172f4468d3ae28d91a0b3f016a00ba5d9159a` (`docs(phase-4bn-c): merge ml-baseline evidence interpretation`).
- **Merge-closeout commit SHA:** `7fca0d538418293fe9b556a8aa67c26ad6165f52` (`docs(phase-4bn-c): add merge closeout`).
- **SHA-finalization commit:** recorded in the final operator report and git log as `docs(phase-4bn-c): finalize merge closeout shas`. Per the repo convention used for Phase 4bn-B / 4bn-A / 4bm-Z / 4bm-Y / 4bm-X, the SHA-finalization commit cannot self-reference its own hash inside its own diff; its SHA is captured in the final operator report and git log. After that commit and push, final `main` SHA == final `origin/main` SHA == the SHA-finalization commit.
- **Final `main` / `origin/main` SHA after push:** equals the SHA-finalization commit; recorded in the final operator report.

## 3. Merge method

- `git merge --no-ff` with the `ort` strategy.
- Merge commit message: `docs(phase-4bn-c): merge ml-baseline evidence interpretation`.
- No `--no-verify`. No `--no-gpg-sign`. No `-c commit.gpgsign=false`. No force-push.
- Pushed to `origin/main` with no force, no skip-hooks, no skip-signing.

## 4. Files brought forward by the merge

Docs (tracked):

- `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-c_ml-baseline-evidence-interpretation-memo.md` (added).
- `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-c_closeout.md` (added).
- `docs/00-meta/current-project-state.md` (modified — narrow Phase 4bn-C paragraph + new Current-phase block; prior Phase 4bn-B paragraph and prior Current-phase blocks preserved as labelled historical context).

Source: none. Tests: none. Scripts: none. Config: none. **No `pyproject.toml`, `README.md`, `.gitignore`, MCP file, manifest, sidecar, gate report, successor-state artefact, existing source / test / script file, or any `data/microstructure/` artefact was modified.** No prior governance memo was modified beyond the narrow `current-project-state.md` paragraph addition. **No `data/research/` artefact was committed** (the seven Phase 4bn-B local outputs + their canonical Phase 4bb-F sidecars remain local-only and gitignored under `.gitignore:88: data/research/`; the four Phase 4bm-W diagnostic outputs + sidecars remain local-only and gitignored under the same rule). The merge-closeout file (this file) is added by the subsequent merge-closeout commit on `main`, not by the merge commit itself.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 157 ++++++++
 .../2026-05-28_phase-4bn-c_closeout.md             | 134 +++++++
 ...n-c_ml-baseline-evidence-interpretation-memo.md | 412 +++++++++++++++++++++
 3 files changed, 703 insertions(+)
```

The diff matches the expected change set from the authorization prompt exactly: two added docs files plus one narrow modification to `current-project-state.md`. No source / test / script / config / data / manifest / sidecar / gate-report / successor-state change.

## 6. Verdict

**MEMO RECORDED — `RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING`.**

Phase 4bn-C is the separately authorized docs-only / governance / interpretation / forensic memo that interprets the first actual ML-baseline implementation evidence (Phase 4bn-B, `RECORD_EVIDENCE_ONLY`). It carries the Phase 4bn-B decision forward verbatim, reads every Phase 4bn-B local gitignored output read-only (all 14 artefact + sidecar SHA256s IDENTICAL pre/post), reads the v002 manifests and Phase 4bm-S / 4bm-U / 4bm-Q / 4bm-W governed artefacts read-only (all IDENTICAL), surfaces twelve non-mutually-exclusive forensic hypotheses for the weak baseline-vs-prior separation, evaluates five candidate follow-up paths, and records a single recommendation. **Phase 4bn-C is recommendation-only and authorizes nothing.** It authorizes no implementation, no ML training, no model scoring, no prediction generation, no feature ranking / selection, no model selection through results, no hyperparameter / threshold tuning, no strategy / signal / PnL / backtest, no acquisition, no manifest mutation, no successor-state mutation, no paper / shadow / live-readiness / deployment / exchange-write. The v002 label and feature manifests remain `research_eligible = false` / `eligibility_gate_status = "pending"`; the label manifest's `chronological_split_policy` remains `"not_yet_defined"` on disk (recorded only in the Phase 4bm-U sibling successor-state JSON). The lifecycle state is **remain paused**.

### 6.1 Phase 4bn-B decision carried forward

`RECORD_EVIDENCE_ONLY` (Phase 4bn-B; merge-complete, SHA-finalized, project-complete on `main`). Phase 4bn-B implemented exactly the Phase 4bn-A §9 – §20 design and produced descriptive ML-baseline evidence on the train and validation splits only. The test holdout is sealed (`test_rows_loaded: 0`). The four fixed-a-priori baseline families (`majority_class_prior`, `persistence_past_return_sign`, `multinomial_logistic_regression_l2`, `multinomial_linear_classifier_l1`) were each run exactly once with locked SGD hyperparameters; no model was selected as best; no feature was ranked or selected; no hyperparameter or threshold was tuned; no strategy / signal / PnL / backtest exists.

### 6.2 Phase 4bn-C is docs-only and authorizes nothing

Phase 4bn-C is a docs-only governance / interpretation / forensic memo. It adds two new tracked docs files under `docs/00-meta/implementation-reports/` (the memo + the paired closeout) and narrowly updates `docs/00-meta/current-project-state.md`. **No** source / test / committed-script / configuration / manifest / sidecar / gate-report / successor-state mutation. **No** local data artefact created or mutated. **No** ML rerun. **No** diagnostics rerun. **No** ML artefact, diagnostic artefact, reusable split mask, model binary, or row-level prediction created or persisted. **No** acquisition, endpoint call, WebSocket / user stream, or credential / `.mcp.json` / MCP / Graphify use. **No** successor authorization.

### 6.3 Class prevalence / majority prior interpretation

Class balance (read read-only from Phase 4bn-B `class_balance_summary.csv` / `per_horizon_model_summary.json`):

| Split × horizon | Down | Flat | Up |
| --- | ---: | ---: | ---: |
| train × 15s | 0.4957 | 0.0109 | 0.4934 |
| train × 60s | 0.5016 | 0.0019 | 0.4965 |
| validation × 15s | 0.4938 | 0.0082 | 0.4980 |
| validation × 60s | 0.4950 | 0.0015 | 0.5036 |

**The `flat` class is *underrepresented* at 0.15 – 1.09 %** of supervised rows across both included horizons in both splits. Direction at 15s / 60s is essentially a near-balanced binary problem in practice (down ≈ up ≈ 0.495 ± 0.005), with a thin sliver of strictly-zero forward returns. This overturns the casual assumption that flat dominates the direction-classification problem on this family.

Consequences for interpretation: the majority-class baseline accuracy floor on validation is 0.4938 (15s) / 0.4950 (60s) — i.e. ~50 %; the majority macro-F1 floor is ~0.22 because the majority baseline predicts only one of three classes. **Accuracy alone is a weak indicator in this regime; balanced accuracy and macro F1 are more honest references.** Beating majority by a few percentage points of accuracy does not imply usable signal. The flat class is never predicted by the L2 / L1 linear classifiers (per-class P / R / F1 = 0 / 0 / 0 on flat in every cell).

### 6.4 Persistence baseline interpretation

| Metric | majority 15s | persistence 15s | majority 60s | persistence 60s |
| --- | ---: | ---: | ---: | ---: |
| Accuracy | 0.4938 | 0.5167 | 0.4950 | 0.4973 |
| Balanced accuracy | 0.3333 | 0.3835 | 0.3333 | 0.3391 |
| Macro F1 | 0.2204 | 0.3839 | 0.2207 | 0.3394 |
| Mean log-loss | 0.7355 | **13.353** | 0.7032 | **13.889** |
| Mean Brier | 0.5081 | **0.9665** | 0.5015 | **1.0053** |

Persistence beats majority on hard accuracy by +2.3 pp (15s) and +0.2 pp (60s), but is **catastrophically worse** on log-loss (~18× the majority floor) and Brier (~2× the majority floor). The catastrophic gap is structural: persistence emits hard one-hot probabilities (1.0 on its predicted class), so every miss costs ~−log(ε) ≈ 27.6 nats per row. **This is not negative evidence about momentum / continuation per se; it is direct evidence that hard-class persistence outputs are uncalibrated.** Phase 4bn-C draws **no** strategy conclusion: no reversal-strategy recommendation, no momentum-strategy recommendation, no strategy recommendation of any kind.

### 6.5 L2 / L1 linear baseline interpretation

| Metric | L2 / 15s | L2 / 60s | L2 − majority / 15s | L2 − majority / 60s |
| --- | ---: | ---: | ---: | ---: |
| Accuracy | 0.5435 | 0.5095 | +0.0497 pp | +0.0145 pp |
| Balanced accuracy | 0.3654 | 0.3412 | +0.0321 pp | +0.0079 pp |
| Macro F1 | 0.3638 | 0.3291 | +0.1434 pp | +0.1084 pp |

L1 and L2 differ in the fourth significant figure on every metric (consistent with the weak `1e-4` penalties; the L1 proximal soft-thresholding does not produce visibly sparser weights at the metric level). Train-validation deltas (validation minus train) are small and approximately matched in sign across L1 / L2 (~−0.005 / −0.005 on accuracy / balanced-accuracy / macro-F1 at 15s; ~−0.003 / −0.0004 / −0.008 at 60s) — **the models are not overfitting** at this level of descriptive measurement. Per-class P / R on validation (L2): at 15s, down 0.540 / 0.560 and up 0.547 / 0.536 (balanced); at 60s, down 0.504 / 0.695 and up 0.522 / 0.328 (strongly down-biased predictions: 38.8M `pred_down` vs 18.0M `pred_up`). Flat per-class P / R / F1 = 0 / 0 / 0 on every cell. **The 15s lift is real but small; the 60s lift is much smaller and the model becomes asymmetric. Statistical descriptive lift is not the same as economically useful signal.** Phase 4bn-C **does not select** L1 over L2, 15s over 60s, or linear over majority.

### 6.6 Calibration / probability-output interpretation

L2 logistic at 15s validation calibration (10-bin descriptive reliability summary on max predicted probability):

| Bin | n_rows | mean max p̂ | empirical acc | reliability gap |
| --- | ---: | ---: | ---: | ---: |
| 0.4 – 0.5 | 1 520 238 | 0.4961 | 0.4904 | −0.0057 |
| 0.5 – 0.6 | 48 889 658 | 0.5478 | 0.5432 | −0.0047 |
| 0.6 – 0.7 | 5 839 614 | 0.6226 | 0.5616 | **−0.0610** |
| 0.7 – 0.8 | 392 090 | 0.7395 | 0.5354 | **−0.2041** |
| 0.8 – 0.9 | 123 119 | 0.8416 | 0.4881 | **−0.3535** |
| 0.9 – 1.0 | 54 930 | 0.9408 | 0.5492 | **−0.3916** |

**~86 % of L2-15s validation predictions live in the 0.5 – 0.6 bin, and that bin is well-calibrated.** **The high-confidence tail is severely over-confident.** When the model claims 0.84 – 0.94 confidence (~178 K rows total), the empirical accuracy is 0.49 – 0.55 — i.e. *no better than majority*, and in the 0.8 – 0.9 bin actually **below** the majority floor. The naive "trade only when the model is confident" follow-up would fail under this evidence. **No threshold was tuned. No calibrator was fit. No probability was converted into a trade signal.** Persistence calibration is degenerate (all rows in the 0.9 – 1.0 bin; gap −0.4833) because persistence emits hard one-hot probabilities by design.

### 6.7 §11.6 cost-commensurability interpretation

The Phase 4bn-B `cost_commensurability` block records the fraction of validation `|forward_log_return|` exceeding multiples of the 16 bps round-trip cost (these depend only on the forward-return distribution, identical across baselines):

| Multiple of round-trip cost | 15s validation | 60s validation |
| --- | ---: | ---: |
| 0.5× (8 bps) | 0.1888 | 0.3989 |
| 1.0× (16 bps) | 0.0622 | 0.1829 |
| 2.0× (32 bps) | 0.0157 | 0.0578 |
| 5.0× (80 bps) | 0.0016 | 0.0093 |

**At 15s only ~6.2 % of validation rows exceed 1× round-trip cost; at 60s 18.3 %.** **15s has stronger model signal but worse cost / tradability context; 60s has better cost context but weaker model signal.** Descriptive only — not a tradability, edge, profitability, or strategy-readiness claim. The §11.6 lock (8 bps per side / 16 bps round trip) is preserved verbatim.

### 6.8 Test-holdout protection interpretation

The test split (2025-02-14 .. 2025-02-28; 15 partitions; 23,797,822 rows) remains **sealed**. The Phase 4bn-B run manifest records `test_holdout_sealed: true`, `test_rows_loaded: 0`, `test_n_partitions_unused: 15`; the dataset module's `iter_partitions(split="test", ...)` raises `MlBaselineDatasetError` because `test ∉ SUPERVISED_SPLITS`, verified by `test_ml_baseline_split_policy_v002.test_test_holdout_iteration_is_forbidden_by_design`. **Phase 4bn-C inspects no test data and references no test metrics.** The Phase 4bm-W envelope-terminal censoring asymmetry (857 rows: 1s 14 / 5s 39 / 15s 170 / 60s 634, all concentrated on 2025-02-28 inside the sealed test split) is carried forward as a non-blocking caveat for any future test-holdout evaluation phase (not authorized by Phase 4bn-C).

### 6.9 Weak-separation forensic hypotheses

Twelve non-mutually-exclusive forensic hypotheses surfaced:

- **H1.** flat-class underrepresentation / collapse;
- **H2.** target definition too blunt or too noisy;
- **H3.** included horizons still not cost-commensurate;
- **H4.** v002 feature surface may lack enough predictive information;
- **H5.** linear / logistic models may be too simple;
- **H6.** class weighting absent by design;
- **H7.** shallow-tree excluded by memory fail-closed rule;
- **H8.** regime heterogeneity;
- **H9.** time-of-day effects;
- **H10.** feature-stationarity drift;
- **H11.** labels may capture economically irrelevant direction;
- **H12.** market may not contain simple exploitable edge under this family.

**None ranked, weighted, resolved, or converted into a design or strategy proposal.**

### 6.10 Follow-up paths evaluated

Five candidate follow-up paths evaluated:

1. **`RECOMMEND_REMAIN_PAUSED_ML_ARC`** — rejected as too negative given the reproducible 15s lift with controlled stability deltas.
2. **`RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING`** — **chosen.** The obvious next-step idea (threshold tuning for confidence) would actively fail under the existing calibration evidence; the questions to answer next (class weighting? horizon decay? memory-bounded shallow tree? regime conditioning?) are subtle and require predeclaration in a docs-only scoping memo.
3. **`RECOMMEND_AUTHORIZE_LABEL_TARGET_REWORK_SCOPING`** — rejected as the immediate next phase but kept on option 2's scoping menu (H2 / H11 family).
4. **`RECOMMEND_AUTHORIZE_CLASS_IMBALANCE_OR_REGIME_CONDITIONING_SCOPING`** — rejected as a separate concurrent phase but kept on option 2's scoping menu (H1 / H6 / H8 / H9 family).
5. **`DO_NOT_RECOMMEND_FURTHER_ML_WORK_ON_CURRENT_V002_FAMILY`** — rejected; existing evidence does not warrant a stop-work verdict.

### 6.11 Future bounded ML-baseline expansion scoping boundaries (NOT authorized by Phase 4bn-C)

A future, separately authorized **bounded ML-baseline expansion scoping** phase (provisionally `Phase 4bn-D`, **not** authorized here) would be permitted to evaluate, at design level only and without running anything:

- whether class weighting should be evaluated (declared a priori, not selected through results);
- whether a memory-bounded shallow tree baseline can be specified respecting the Phase 4bn-A §15 boundary and a streaming-safe memory profile (depth-bounded with fixed pre-declared `max_depth`; chunked / sampled training that fail-closes on memory rather than implicitly downsampling for headline metrics);
- whether the §17 calibration evidence motivates a descriptive-only validation-side calibration analysis (reliability gaps per bin; per-class reliability; per-horizon reliability) without proposing any threshold tuning or probability-to-signal conversion;
- whether 1s / 5s should remain deferred or be partially included for descriptive parity;
- whether 15s / 60s should be re-evaluated under class-weighted softmax losses, without tuning weights through validation;
- whether target balance thresholds (the strict-sign zero-class definition) should be reconsidered at scoping level only (no label regeneration);
- whether time-of-day or regime segmentation should be scoped at design level, including how to enforce no train/test leakage and how to avoid using validation distributions to design segments;
- how to keep the test holdout sealed.

Any such future scoping memo must: keep the test holdout sealed; not train models; not score models; not generate predictions; not select models through results; not rank or select features; not tune hyperparameters or thresholds; not define or run strategy; not generate trade signals; not simulate PnL; not run backtests; not authorize acquisition; not call any endpoint; not use credentials / `.env` / `.mcp.json` / MCP / Graphify; not mutate any manifest; not mutate any successor-state artefact; not commit `data/microstructure/`; not commit `data/research/`; not persist model binaries; not persist row-level predictions; not create reusable split masks; not authorize Phase 5, paper / shadow, live-readiness, deployment, or exchange-write.

## 7. Local gitignored outputs

**None produced by Phase 4bn-C.** Phase 4bn-C created no local artefact. The pre-existing predecessor local gitignored artefacts were re-hashed read-only and are unchanged (see §9). They remain gitignored and not committed:

- Phase 4bn-B ML-baseline outputs under `data/research/microstructure/ml-baselines/phase-4bn-b/` — `git check-ignore -v` → `.gitignore:88: data/research/`.
- Phase 4bm-W diagnostic outputs under `data/research/microstructure/diagnostics/phase-4bm-w/` — `.gitignore:88: data/research/`.
- Phase 4bm-S / Phase 4bm-U successor-state JSONs + sidecars under `data/microstructure/successor-state/labels/` — `.gitignore:85: data/microstructure/`.
- Phase 4bm-Q gate report + sidecar under `data/microstructure/gate-reports/labels/` — `.gitignore:85: data/microstructure/`.

## 8. Validation results

- `git diff --check main..phase-4bn-c/...` → clean (no whitespace errors).
- `git diff --name-status main..phase-4bn-c/...` → `M docs/00-meta/current-project-state.md`; `A …_phase-4bn-c_closeout.md`; `A …_phase-4bn-c_ml-baseline-evidence-interpretation-memo.md` (docs only).
- `git diff --stat` for the merge → `3 files changed, 703 insertions(+)`.
- `git status --short` (pre and post merge) → clean working tree; only expected gitignored untracked entries (`.claude/scheduled_tasks.lock`, and the gitignored `data/research/` local outputs).
- `git check-ignore -v` for `data/research/microstructure/ml-baselines/phase-4bn-b/ml_baseline_run_manifest.json` and `data/research/microstructure/ml-baselines/phase-4bn-b/metrics_train_validation.csv` → `.gitignore:88: data/research/`.
- No source / test / script / config changed, so ruff / mypy / pytest were not invoked for this docs-only merge; no source-test/lint/type-check coverage is claimed. No markdown-lint tool is part of the repo standard for these reports; none was invented or run.

## 9. Upstream immutability evidence

Every governed predecessor artefact re-hashed read-only pre-merge and post-merge; all byte-identical (IDENTICAL pre/post):

| Artefact | Expected / pre-merge SHA256 | Post-merge | Result |
| --- | --- | --- | --- |
| `ml_baseline_run_manifest.json` | `cd436e3823d7c8e5e07431a9b11ebcf72e35e997db9a76ca865ff1885b3cfa13` | same | IDENTICAL |
| `ml_baseline_run_manifest.json.sha256` | `b13dbedf70f02891df50d9080f904b6327f0569687c257f3840256ec9e02f293` | same | IDENTICAL |
| `per_horizon_model_summary.json` | `d94f8d72781afd4c229ee7b525e8cd79f2a13a56e5a1d68e42e74724d4c396b0` | same | IDENTICAL |
| `per_horizon_model_summary.json.sha256` | `23f91cc02a6a272b25b57cd46953f139e58beca7073351dbfa6fae4f150c03cf` | same | IDENTICAL |
| `metrics_train_validation.csv` | `40cde4a01dde14e4152c4d53b70f57bc330f20d3f2ef6248b9bb18e1c190a7a8` | same | IDENTICAL |
| `metrics_train_validation.csv.sha256` | `5b3a04fae93df8b73830b83e92addd80a498d9d0061e2e0dd9cdf9fc9b202a34` | same | IDENTICAL |
| `calibration_summary.csv` | `a0f469d27c90958b2fc308b54753d97bd78830321d5954e7d30649bff4e00138` | same | IDENTICAL |
| `calibration_summary.csv.sha256` | `1b43de79ae210b5c082c087b17eb5ca9a96c7e6990d04cd82b9e329f16ba6df9` | same | IDENTICAL |
| `class_balance_summary.csv` | `6e6338bff25bae253d5442763fb960339a31f936e51e58ae2199af5e844df40f` | same | IDENTICAL |
| `class_balance_summary.csv.sha256` | `41ca08d604e597aaceff0964f720742367801e6c43538539a4265933932294e6` | same | IDENTICAL |
| `feature_schema_used.json` | `5f3d84b45fe8cc538c39c8ddc093625cfe6f8040a862c2e97ad970114415fac6` | same | IDENTICAL |
| `feature_schema_used.json.sha256` | `2f99379a21a0bd6937be59b8cd6c7a048f94cba4b20028ea0c7149feca399a42` | same | IDENTICAL |
| `transform_metadata.json` | `73b455af6698ab6b43536a0f1e3941bdd9d4078b619ce0287cbdc634313286b0` | same | IDENTICAL |
| `transform_metadata.json.sha256` | `d3b91fb201b047a5e36b669ba0aac63fe225261dfe4283e524146ffecae792dd` | same | IDENTICAL |
| v002 label manifest | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` | same | IDENTICAL |
| v002 label manifest sidecar | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` | same | IDENTICAL |
| v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | same | IDENTICAL |
| v002 feature manifest sidecar | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` | same | IDENTICAL |

Per-prompt evidence carry-forward: Phase 4bm-U split-policy successor-state JSON `6834ab11…` + sidecar `fa9ae709…`; Phase 4bm-S research-use successor-state JSON `081730006c…` + sidecar `05597fe4…`; Phase 4bm-Q gate report `8a360608…` + sidecar `3913a510…`; Phase 4bm-W summary `f4b825af…` + sidecar `ff52873c…`; Phase 4bm-W manifest `ac10061d…` + sidecar `644506e3…` — all known IDENTICAL through the prior Phase 4bn-B merge and unchanged by this docs-only Phase 4bn-C merge (the merge touched none of them).

## 10. Manifest state preservation

- **v002 label manifest** (`5e17074d…`): `research_eligible = false`; `eligibility_gate_status = "pending"`; `chronological_split_policy = "not_yet_defined"`; `label_family_research_use_authorized = false`; `stage_5_label_cleared = false`; `diagnostics_authorized = false` (historical). **No transition occurred.**
- **v002 feature manifest** (`512a0a54…`): `research_eligible = false`; `eligibility_gate_status = "pending"`; `stage_4_feature_cleared = false`. **No transition occurred.**
- Phase 4bm-S, Phase 4bm-U, and Phase 4bm-Q sibling successor-state / gate-report artefacts byte-identical (see §9). No transition occurred.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked).

## 11. Boundary confirmations

- no source code modified; no test modified; no committed script modified; no config modified.
- no `.gitignore`, `pyproject.toml`, or `README.md` modified.
- no MCP file created, read, or modified; no `.mcp.json` created or read; no Graphify use.
- no `data/microstructure/` artefact committed; no `data/research/` artefact committed.
- no manifest mutated; no `research_eligible` flipped; no `eligibility_gate_status` transitioned; no `chronological_split_policy` changed; no `diagnostics_authorized` / `ml_authorized` changed.
- no successor-state artefact mutated (Phase 4bm-S `081730006c…`, Phase 4bm-U `6834ab11…` byte-identical).
- no Phase 4bm-Q gate report mutated (`8a360608…` byte-identical).
- no Phase 4bm-W diagnostic output mutated (all four SHAs byte-identical).
- no Phase 4bn-B local output mutated (all 14 SHAs byte-identical).
- no diagnostics rerun; no new diagnostic artefact created.
- no ML rerun; no ML artefact created.
- no reusable split mask created / materialized; no model binary persisted; no row-level prediction persisted.
- no model training / scoring / prediction generation / feature ranking / feature selection / model selection through results / hyperparameter tuning / threshold tuning.
- no strategy defined or run; no trade signals generated; no PnL simulated; no backtests run; no walk-forward optimization.
- test holdout not used for any reason; Phase 4bn-B `test_rows_loaded: 0` carried forward.
- no data acquired; no public / authenticated / private endpoint called; no Binance API called; no WebSocket / user stream opened; no credential / `.env` / `.mcp.json` / MCP / Graphify used.
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

All preserved verbatim. All prior phase results (Phase 4am .. Phase 4bn-B) preserved verbatim.

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

The Phase 4bn-C merge does not, and cannot, be construed as authorizing:

- any ML rerun; any further ML-baseline expansion; any model training; any model scoring; any prediction generation; any feature ranking; any feature selection; any feature pruning; any model selection through results; any hyperparameter tuning; any threshold tuning; any meta-labeling; any ensemble construction;
- any strategy research; any strategy design; any signal generation; any trade-signal generation; any PnL simulation; any equity-curve construction; any Sharpe / Sortino / drawdown / hit-rate / trade-PnL metrics; any backtests; any walk-forward optimization;
- any use of the test holdout for training, fitting, calibration, evaluation, tuning, design, model selection, threshold selection, reporting, or inspection;
- any diagnostics rerun; any diagnostic artefact creation; any ML artefact creation; any reusable split-mask materialization; any row-level prediction persistence; any model binary persistence;
- any data acquisition (no additional days / symbols / families beyond the locked 90-day v002 envelope; no mark-price / spot / cross-venue / order-book / additional aggTrades; no 30s / 5m / 30m / 1h / 4h / longer-horizon label generation; no barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels);
- any manifest mutation; any successor-state mutation; any `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` / `diagnostics_authorized` / `ml_authorized` transition from this memo alone;
- any public / authenticated / private endpoint call; any WebSocket / user stream; any credential / `.env` / `.mcp.json` / MCP / Graphify use;
- Phase 4 canonical; Phase 5; Phase 4bn-D; any future bounded ML-baseline expansion scoping phase; Phase 4bn-* further successors; Phase 4bo-* / Phase 4bp-*;
- old-strategy alt-symbol rerun, cooled-down-family reopening, or 5m research-thread reopening (Phase 3t closure preserved).

`RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING` means only that a future, separately authorized docs-only / design-only scoping phase may scope a bounded baseline-expansion attempt. **Any bounded ML-baseline expansion scoping memo requires a separately authorized phase.**

## 15. Successor authorization

**None.**

Not authorized by this merge:

- Phase 4bn-D — Multi-Day V002 Bounded ML-Baseline Expansion Scoping Memo (or any phase under any name performing bounded ML-baseline expansion scoping, label / target rework scoping, class-imbalance / regime-conditioning scoping, calibration-only-analysis scoping, or any successor to the Phase 4bn-* arc);
- any ML implementation execution; ML model training; model scoring; prediction generation; feature ranking / selection; model selection through results; hyperparameter tuning; threshold tuning;
- strategy research / design; signal generation; trade-signal generation; PnL simulation; backtests; walk-forward optimization;
- diagnostics rerun; diagnostic artefact creation; ML artefact creation; reusable split-mask materialization; row-level prediction persistence; model binary persistence; test-holdout tuning / design / evaluation / inspection;
- manifest mutation; successor-state mutation;
- Phase 4bn-* further successors / Phase 4bo-* / Phase 4bp-* / Phase 5 / Phase 4 canonical;
- additional aggTrades / 5m / 1m / tick / mark-price / order-book / spot / cross-venue data acquisition;
- research execution; paper / shadow; live-readiness; deployment; exchange-write; production keys; authenticated APIs; private endpoints; user stream; WebSockets; MCP; Graphify; `.mcp.json`; credentials.

## 16. Recommended state

**Remain paused.**

Phase 4bn-C is now merge-complete on main and, after the SHA-finalization commit and push, project-complete. The interpretation decision `RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING` authorizes nothing. **Any bounded ML-baseline expansion scoping memo requires a separately authorized phase.** **Phase 4bn-D is not authorized by Phase 4bn-C.** **Recommended state remains paused.**

**Conditional next, NOT authorized:** a Phase 4bn-D docs-only / design-only bounded ML-baseline expansion scoping memo is the cleanest non-paused option. It would enumerate, at design level only and without running anything, exactly which §6.11 candidate questions could be evaluated by a possible future implementation phase, under what predeclared evaluation rules, and with the test holdout still sealed. Phase 4bn-D is **not authorized** by this merge.

## 17. Known caveats

- The Phase 4bn-B prompt's prior characterization that "persistence is below the majority-class floor on validation" referred to **probabilistic / proper-scoring-rule metrics (log-loss, Brier)**, not hard accuracy. On hard accuracy, persistence is slightly **above** majority on both horizons; the negative gap is on log-loss / Brier where persistence's hard one-hot outputs are intrinsically uncalibrated. Phase 4bn-C records the precise observation from the local outputs.
- The Phase 4bn-B prompt's prior characterization that "L2 / L1 lift is marginal" understates the 15s lift at the accuracy / macro-F1 level — the lift is small but reproducible and structurally meaningful (the flat class is underrepresented; both linear classifiers predict both up and down classes; the majority baseline predicts one class only).
- The L2-15s high-confidence-bin over-confidence (reliability gaps −0.061 to −0.392 in the 0.6–1.0 bins) is a forensically important finding because it implies the most obvious "next step" (threshold tuning for confidence) would actively fail; Phase 4bn-C records this descriptively and **does not tune**.
- mypy `src` baseline (33 errors on `main` before Phase 4bn-B; 86 errors after Phase 4bn-B) is **unchanged** by this docs-only Phase 4bn-C merge; Phase 4bn-C adds no source files.
- The Phase 4bn-B / Phase 4bn-A non-implementation of the optional shallow tree baseline (`BASELINE_SHALLOW_TREE_INCLUDED = False`) is preserved verbatim; it is one of the candidate questions enumerated in §6.11 for any future bounded scoping memo.
