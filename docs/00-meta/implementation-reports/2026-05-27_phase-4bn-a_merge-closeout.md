# Phase 4bn-A — Merge Closeout

**Phase 4bn-A is now merge-complete on main.** **Phase 4bn-A is a docs-only / design-only ML-baseline implementation scoping phase.** **Phase 4bn-A does not train ML models.** **Phase 4bn-A does not run ML.** **Phase 4bn-A does not score models.** **Phase 4bn-A does not generate predictions.** **Phase 4bn-A does not select models through results.** **Phase 4bn-A does not rank or select features.** **Phase 4bn-A does not tune hyperparameters.** **Phase 4bn-A does not tune thresholds.** **Phase 4bn-A does not define or run strategy.** **Phase 4bn-A does not generate signals.** **Phase 4bn-A does not simulate PnL.** **Phase 4bn-A does not run backtests.** **Phase 4bn-A does not authorize acquisition.** **Phase 4bn-A does not authorize research execution.** **Phase 4bn-A does not create ML artefacts.** **Phase 4bn-A does not create diagnostic artefacts.** **Phase 4bn-A does not create reusable split masks.** **Phase 4bn-A does not use the test holdout for tuning or design.** **Phase 4bn-A does not mutate any manifest.** **Phase 4bn-A does not mutate any successor-state artefact.** **Phase 4bn-A does not commit data/microstructure.** **Phase 4bn-A does not commit data/research.** **Any ML-baseline implementation requires a separately authorized implementation phase.** **Phase 4bn-B is not authorized by Phase 4bn-A.** **Recommended state remains paused.**

> **Successor-naming note.** Phase 4bm-Z closed the `4bm-` letter-series; Phase 4bn-A opens the `4bn-` series. By the repo's within-series convention (`-A`, `-B`, `-C`, …), the next phase after Phase 4bn-A is `Phase 4bn-B`, named in the required exact phrases as the unauthorized future ML-baseline implementation phase. No successor is authorized under any name.

## 1. Phase identity

- **Phase:** Phase 4bn-A — Multi-Day V002 ML-Baseline Implementation Scoping / Design.
- **Type:** docs-only / design-only ML-baseline implementation scoping phase (Tier 1 — Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` §3). First phase of the ML arc.
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bn-A ML-baseline implementation scoping/design memo + closeout + the narrow `current-project-state.md` current-phase block onto `main`, recording the design decision `RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION` as project state. The phase defines — at design level only — the exact implementation boundaries for a possible future ML-baseline implementation phase; it trains, scores, predicts, selects, ranks, tunes, and runs nothing.
- **Target branch:** `main`.
- **Source branch:** `phase-4bn-a/multi-day-v002-ml-baseline-implementation-scoping-design`.

## 2. SHAs

- **`main` SHA before merge:** `de170ad31b9dd71e9f5c8fac59d4b19472d9e6d0` (Phase 4bm-Z merge-closeout SHA-finalization commit; `main == origin/main` verified pre-merge).
- **Base SHA:** `de170ad31b9dd71e9f5c8fac59d4b19472d9e6d0`.
- **Branch tip SHA before merge:** `a311eb24031535fddf866fc0dca4aa90ca99c720`.
- **Docs commit SHA:** `a311eb24031535fddf866fc0dca4aa90ca99c720` (`docs(phase-4bn-a): scope ml-baseline implementation design`; the memo + closeout + current-project-state block are a single docs commit, which is also the branch tip).
- **Merge commit SHA:** `fdd15fedb8acbf62f6b0882bed42fda82fd67156` (`docs(phase-4bn-a): merge ml-baseline implementation design`).
- **Merge-closeout commit SHA:** `6610070ed753788fc0ecd4520998aa5457577cfc` (`docs(phase-4bn-a): add merge closeout`).
- **SHA-finalization commit:** recorded in the final operator report and git log as `docs(phase-4bn-a): finalize merge closeout shas`; it is the commit that records these final SHAs into this file. Per the repo convention used for Phase 4bm-Z / 4bm-Y / 4bm-X, the SHA-finalization commit cannot self-reference its own hash inside its own diff; its SHA is captured in the final operator report and git log. After that commit and push, final `main` SHA == final `origin/main` SHA == the SHA-finalization commit.
- **Final `main` / `origin/main` SHA after push:** equals the SHA-finalization commit; recorded in the final operator report.

## 3. Merge method

- `git merge --no-ff` with the `ort` strategy.
- Merge commit message: `docs(phase-4bn-a): merge ml-baseline implementation design`.
- No `--no-verify`. No `--no-gpg-sign`. No `-c commit.gpgsign=false`. No force-push.
- Pushed to `origin/main` with no force, no skip-hooks, no skip-signing.

## 4. Files brought forward by the merge

Docs (tracked):

- `docs/00-meta/implementation-reports/2026-05-27_phase-4bn-a_ml-baseline-implementation-scoping-design.md` (added).
- `docs/00-meta/implementation-reports/2026-05-27_phase-4bn-a_closeout.md` (added).
- `docs/00-meta/current-project-state.md` (modified — narrow current-phase block addition; prior Phase 4bm-Z paragraph preserved as labelled historical context).

Source: none. Tests: none. Scripts: none. Config: none. **No `data/microstructure/` file was modified.** **No `data/research/` file was modified.** No prior governance memo was modified beyond the narrow `current-project-state.md` paragraph addition. No prior source / test / script was modified. The merge-closeout file (this file) is added by the subsequent merge-closeout commit on `main`, not by the merge commit itself.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              |   2 +
 .../2026-05-27_phase-4bn-a_closeout.md             | 178 +++++++++
 ...-a_ml-baseline-implementation-scoping-design.md | 425 +++++++++++++++++++++
 3 files changed, 605 insertions(+)
```

The diff matches the expected change set from the authorization prompt exactly: two added docs files plus one narrow modification to `current-project-state.md`. No source / test / script / config / data / manifest / sidecar / gate-report / successor-state change.

## 6. Verdict

**MEMO RECORDED — `RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION`.**

Phase 4bn-A is the separately authorized docs-only / design-only ML-baseline implementation *scoping/design* phase recommended by Phase 4bm-Z. It defines, at design level only, the exact implementation boundaries (target framing, horizons, train/validation/test handling, censored-row handling, feature surface, transforms, baseline families, metrics, calibration, cost-aware descriptive evaluation, outputs, tests, anti-drift) for a possible future ML-baseline implementation phase. All twenty-one design criteria A–U PASS, so the memo recommends — and only recommends — that a future, separately authorized implementation phase *may* implement exactly this design. **Phase 4bn-A is recommendation-only and authorizes nothing.** It authorizes no implementation in Phase 4bn-A, no ML training, no model scoring, no prediction generation, no feature ranking/selection, no model selection through results, no hyperparameter tuning, no threshold tuning, no strategy research, no signals, no PnL simulation, no backtests, no acquisition, and no research execution. The v002 label/feature manifests remain `research_eligible = false` / `eligibility_gate_status = "pending"`; the label manifest `chronological_split_policy` remains `"not_yet_defined"` on disk (recorded only in the Phase 4bm-U sibling successor-state JSON). The lifecycle state is **remain paused**.

### 6.1 Design criteria A–U — all PASS

| # | Criterion | Result |
| --- | --- | --- |
| A | Phase 4bm-Z completed and merged the docs-only ML-readiness evaluation memo | PASS |
| B | Phase 4bm-Z recommended ML-baseline implementation scoping/design | PASS |
| C | Future implementation boundary definable without training models in this phase | PASS |
| D | Target framing specifiable without using test holdout for tuning/design | PASS |
| E | Horizon inclusion/deferral specifiable without declaring any horizon strategy-ready | PASS |
| F | Train/validation/test handling can enforce the Phase 4bm-U split policy | PASS |
| G | Censored-row handling definable per horizon | PASS |
| H | Feature surface freezable to v002 feature family without new feature engineering | PASS |
| I | Transform/preprocessing rules can enforce train-only fitting | PASS |
| J | Baseline families selectable at design level without result-based selection | PASS |
| K | Metric policy specifiable without computing metrics in this phase | PASS |
| L | Calibration policy specifiable without fitting calibration in this phase | PASS |
| M | Cost-aware descriptive evaluation specifiable without strategy/backtest/PnL | PASS |
| N | Output artefact policy can keep all future outputs local and gitignored | PASS |
| O | Test/validation requirements specifiable without running implementation | PASS |
| P | Anti-drift boundaries can prevent ML/strategy/backtest/acquisition drift | PASS |
| Q | No diagnostics rerun | PASS |
| R | No ML / scoring / predictions / feature-or-model selection / hp/threshold tuning / strategy / backtest occurred | PASS |
| S | No manifest or successor-state mutation occurred | PASS |
| T | No data/microstructure or data/research artefact committed | PASS |
| U | Retained verdicts and project locks unchanged | PASS |

**All design criteria A–U PASS.**

### 6.2 Phase 4bm-Z decision carried forward

`RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION_SCOPING` (Phase 4bm-Z; criteria A–R PASS). This Phase 4bn-A is its separately authorized realization. Phase 4bm-Z authorized no ML implementation, training, scoring, prediction, selection, ranking, tuning, strategy, signals, PnL, backtests, acquisition, or research execution.

### 6.3 Phase 4bm-W diagnostic verdict carried forward

`DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS` (Phase 4bm-W): 0 blocking structural failures; 4 non-blocking caveats; descriptive-only — not ML-readiness, not strategy-readiness, not backtest-readiness. Carried forward unchanged as constraints; not re-derived, not re-issued, not rerun. The four caveats: (1) envelope-terminal censoring asymmetry — 857 censored rows `{1s:14, 5s:39, 15s:170, 60s:634}` all in the test split; (2) 538 embargo-excluded earlier-split rows (train 248, validation 290, test 0); (3) approximate-quantile method (exact moments not approximate); (4) historical `diagnostics_authorized=false` manifest flag (authorization came from the operator prompt, not manifest mutation).

### 6.4 Target framing design

Direction classification only; 3-class `{-1, 0, +1}` from the existing v002 label family; zero/flat class kept explicit (not merged, not dropped); no magnitude regression; no ordinal framing; no meta-labeling; per-horizon-independent framing.

### 6.5 Horizon inclusion / deferral design

Include 15s and 60s in the first baseline; defer 1s and 5s (latency / tradability sensitivity, cost-commensurability risk; revisited only by later separately authorized phases); 60s carries the test-split censoring caveat with per-horizon masking; no horizon strategy-ready; no horizon live-tradable.

### 6.6 Train / validation / test handling design

`CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`: train 45d / 74,535,688 rows; validation 30d / 56,819,939 rows; test 15d / 23,797,822 rows; total 90d / 155,153,449 rows. Train fits transforms/models (future phase only); validation evaluates/calibrates (future phase only, explicit rules); test sealed/unused unless a later phase authorizes a single terminal holdout evaluation; no test-holdout tuning/design; no random / shuffled / k-fold-over-time / bootstrap / post-hoc resampling; rows assigned by `source_transact_time_ms` UTC date; 60s boundary embargo + boundary-crossing exclusion (538 earlier-split excluded — train 248, validation 290, test 0); reusable split masks not authorized.

### 6.7 Censored-row handling design

Per-horizon label-unavailable; excluded from supervised loss and metric denominator for that horizon; not imputed; not treated as zero-return / no-change / flat-class; censored counts reported per split × horizon (v002 aggregate `{1s:14, 5s:39, 15s:170, 60s:634}`, all in test).

### 6.8 Feature surface design

Existing v002 feature family only (`microstructure_features_aggtrades_v001 @ v002`); `feature_config_hash = 819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d` preserved; no new feature engineering / selection / ranking / pruning. Model feature matrix = the 45 `computed_feature_column_names` (40 rolling features across 1s/5s/15s/60s + `utc_hour`, `utc_minute`, `milliseconds_since_day_start`, `invalid_window_flag`, `rolling_missing_window_flag`), frozen by deterministic rule derived from manifest evidence. Excluded: the 17 lineage/identifier/timestamp/SHA columns, all label columns, and split flags.

### 6.9 Transform / preprocessing design

Fit scalers/imputers/encoders on train only; apply to validation only; no fit on validation/test; no target leakage; explicit missingness handling (flag columns + train-fit imputation); class encoding preserves the zero/flat class; transform metadata persisted only as local gitignored output.

### 6.10 Baseline model-family design

A priori (no result-based selection, no search): majority-class/class-prior; naive persistence/naive-direction if leakage-free; (regularized) multinomial logistic regression; regularized linear classifier; optionally one bounded shallow tree (fixed pre-declared depth). No deep learning. Gradient boosting deferred to a later separately authorized baseline-expansion phase (tuning-sensitivity justification). No hyperparameter search; no model-family selection through results; no ensemble selection.

### 6.11 Metric policy design

Defined, not computed: class prevalence by split×horizon; confusion matrix by split×horizon; accuracy; balanced accuracy; macro F1; per-class precision/recall; log loss (if probabilistic); Brier/calibration summary (if probabilistic); train/validation stability; §11.6-locked cost-commensurability descriptive summary. Forbidden: PnL metrics; backtest metrics; Sharpe/Sortino/drawdown; hit-rate-as-strategy; threshold-tuned metrics; test-set metrics in first implementation; any metric used to design strategy or tune trade thresholds.

### 6.12 Calibration design

Validation-only calibration evaluation in a future implementation phase; no test calibration; no threshold tuning; no probability-to-signal conversion; calibration outputs descriptive / ML-evaluation only; no strategy triggers.

### 6.13 Cost-aware descriptive evaluation design

§11.6 = 8 bps per side / 16 bps round trip locked reference; descriptive cost-commensurability summaries only; no PnL simulation; no strategy construction; no entry/exit rules; no trade threshold design; no order/position model; no backtest.

### 6.14 Output artefact design

Future implementation outputs local + gitignored under an approved namespace (e.g. `data/research/microstructure/ml-baselines/phase-4bn-b/`): `ml_baseline_run_manifest.json`(+`.sha256`), `per_horizon_model_summary.json`(+`.sha256`), `metrics_train_validation.csv`, `calibration_summary.csv`, `class_balance_summary.csv`, `feature_schema_used.json`, `transform_metadata.json`, model artefacts only if separately authorized. Canonical Phase 4bb-F sidecar format (`<sha256_lowercase_hex><two spaces><basename><LF>`). No implementation outputs / model artefacts / data/research / data/microstructure committed.

### 6.15 Test / validation design

Future tests: split-policy enforcement; test-holdout exclusion; train-only transform fitting; no validation/test fit; censored-row exclusion by horizon; feature/label row alignment; no leakage columns in feature matrix; no forbidden imports/endpoints/credentials; output sidecar format; local-output gitignore behaviour; no strategy/backtest/PnL functions; deterministic manifest generation; CLI dry-run / small-fixture if applicable.

### 6.16 Proposed future implementation surface (named only; not created)

Modules: `src/prometheus/research/microstructure/ml_baseline_design_v002.py`, `ml_baseline_dataset_v002.py`, `ml_baseline_models_v002.py`, `ml_baseline_metrics_v002.py`, `ml_baseline_report_v002.py`. Script: `scripts/phase4bn_b_run_ml_baseline_v002.py`. Tests: `tests/research/microstructure/test_ml_baseline_dataset_v002.py`, `test_ml_baseline_split_policy_v002.py`, `test_ml_baseline_no_leakage_v002.py`, `test_ml_baseline_no_network.py`, `test_ml_baseline_outputs_v002.py`. None created by Phase 4bn-A.

### 6.17 Future ML-baseline implementation boundaries

A future, separately authorized ML-baseline implementation phase (provisionally `Phase 4bn-B`, **not authorized here**) would implement *exactly* the §6.4–§6.15 design and nothing beyond it: direction-classification baselines on 15s/60s, trained on train, evaluated on validation, with the test holdout sealed, using the frozen 45-column v002 feature matrix, train-only transforms, validation-only calibration, the fixed a-priori baseline families, the descriptive ML metrics + §11.6 cost-commensurability summary, per-horizon censored-row masking, Phase 4bm-U split enforcement, local gitignored outputs, and the specified test suite. It **must not** train/score/predict in this design phase, select features, rank features, select models through results, tune hyperparameters, tune thresholds, design strategy, generate signals, simulate PnL, run backtests, run walk-forward optimization, use the test holdout for tuning/design, materialize reusable split masks unless separately authorized, mutate manifests or successor-state artefacts, or acquire data.

## 7. Local gitignored outputs (if any)

**None produced by Phase 4bn-A.** Phase 4bn-A created no local artefact. The pre-existing predecessor local gitignored artefacts were re-hashed read-only and are unchanged (see §9). They remain gitignored and not committed:

- Phase 4bm-W diagnostic outputs under `data/research/microstructure/diagnostics/phase-4bm-w/` — `git check-ignore -v` → `.gitignore:88: data/research/`.
- Phase 4bm-S / Phase 4bm-U successor-state JSONs + sidecars under `data/microstructure/successor-state/labels/` — `.gitignore:85: data/microstructure/`.
- Phase 4bm-Q gate report + sidecar under `data/microstructure/gate-reports/labels/` — `.gitignore:85: data/microstructure/`.

## 8. Validation results

- `git diff --check main..phase-4bn-a/...` → clean (no whitespace errors).
- `git diff --name-status main..phase-4bn-a/...` → `M docs/00-meta/current-project-state.md`; `A …_phase-4bn-a_closeout.md`; `A …_phase-4bn-a_ml-baseline-implementation-scoping-design.md` (docs only).
- `git diff --stat` for the merge → `3 files changed, 605 insertions(+)`.
- `git status --short` (pre and post merge) → clean working tree; only expected gitignored untracked local outputs (not shown by git).
- `git check-ignore -v data/research/microstructure/diagnostics/phase-4bm-w/descriptive_diagnostics_summary.json` → `.gitignore:88: data/research/`.
- `git check-ignore -v data/research/microstructure/diagnostics/phase-4bm-w/diagnostics_manifest.json` → `.gitignore:88: data/research/`.
- No source / test / script / config changed, so ruff / mypy / pytest were not invoked for this docs-only merge; no source-test/lint/type-check coverage is claimed. No markdown-lint tool is part of the repo standard for these reports; none was invented or run.

## 9. Upstream immutability evidence

Every governed predecessor artefact re-hashed read-only pre-merge and post-merge; all byte-identical (IDENTICAL pre/post):

| Artefact | Expected / pre-merge SHA256 | Post-merge | Result |
| --- | --- | --- | --- |
| `descriptive_diagnostics_summary.json` | `f4b825af2e81734007be06acac5083e2d4048b54b5650bc407d87a6fc246198a` | same | IDENTICAL |
| `descriptive_diagnostics_summary.json.sha256` | `ff52873c983b55cc74a0639d17ea8b3d128cdbee9c77763cd11d2e71b3820473` | same | IDENTICAL |
| `diagnostics_manifest.json` | `ac10061d2f0257002e094d578bcc6149b1a74ca28c604fd0d0a97e5c51c26e45` | same | IDENTICAL |
| `diagnostics_manifest.json.sha256` | `644506e392db46da6d27fa46519cac327136b1a05e350e2d9b231c62fce517eb` | same | IDENTICAL |
| Phase 4bm-U split-policy successor-state JSON | `6834ab11a5ac5d93b4d9f14d9b71ef3acb2a279bd8e3189fd22421598675fc9c` | same | IDENTICAL |
| Phase 4bm-U split-policy successor-state sidecar | `fa9ae709add4541111e70cfc03d9126ac40f136ea2ce1aa1abe299d3412ac0b6` | same | IDENTICAL |
| Phase 4bm-S research-use successor-state JSON | `081730006c11360692db0a99d59a0ed499f762ef4f86d6e29bdf3016550abfe7` | same | IDENTICAL |
| Phase 4bm-S research-use successor-state sidecar | `05597fe4d568f5644ad9acc914f8a3b429bc7984cf7df3a2ac3f8c7935e02551` | same | IDENTICAL |
| v002 label manifest | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` | same | IDENTICAL |
| v002 label manifest sidecar | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` | same | IDENTICAL |
| v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | same | IDENTICAL |
| v002 feature manifest sidecar | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` | same | IDENTICAL |
| Phase 4bm-Q gate report | `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` | same | IDENTICAL |
| Phase 4bm-Q gate report sidecar | `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` | same | IDENTICAL |

## 10. Manifest state preservation

- **v002 label manifest** (`5e17074d…`): `research_eligible = false`; `eligibility_gate_status = "pending"`; `chronological_split_policy = "not_yet_defined"`; `label_family_research_use_authorized = false`; `stage_5_label_cleared = false`; `diagnostics_authorized = false` (historical). No transition occurred.
- **v002 feature manifest** (`512a0a54…`): `research_eligible = false`; `eligibility_gate_status = "pending"`; `stage_4_feature_cleared = false`. No transition occurred.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked).

## 11. Boundary confirmations

- no source code modified; no test modified; no committed script modified; no config modified.
- no `.gitignore`, `pyproject.toml`, or `README.md` modified.
- no `data/microstructure/` artefact committed; no `data/research/` artefact committed.
- no manifest mutated; no `research_eligible` flipped; no `eligibility_gate_status` transitioned; no `chronological_split_policy` changed; no `diagnostics_authorized` / `ml_authorized` changed.
- no successor-state artefact mutated (Phase 4bm-S `081730006c…`, Phase 4bm-U `6834ab11…` byte-identical).
- no Phase 4bm-Q gate report mutated (`8a360608…` byte-identical).
- no diagnostics rerun; no diagnostic artefact created.
- no ML model trained; no ML run; no model scored; no predictions generated; no model selected through results; no features ranked/selected; no hyperparameters tuned; no thresholds tuned.
- no strategy defined or run; no signals generated; no PnL simulated; no backtests run; no walk-forward optimization.
- no reusable split mask created/materialized.
- test holdout not used for tuning or design.
- no data acquired; no public/authenticated/private endpoint called; no Binance API called; no WebSocket / user-stream; no credential / `.env` / `.mcp.json` / MCP / Graphify used.
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

All preserved verbatim. All prior phase results (Phase 4am .. Phase 4bm-Z) preserved verbatim.

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

The Phase 4bn-A merge does not, and cannot, be construed as authorizing:

- ML-baseline implementation execution; ML model training; model scoring; prediction generation; feature ranking; feature selection; model selection through results; hyperparameter tuning; threshold tuning; meta-labeling;
- strategy research; strategy design; signal generation; PnL simulation; backtests; walk-forward optimization;
- diagnostics rerun; diagnostic artefact creation; ML artefact creation; reusable split-mask materialization;
- use of the test holdout for tuning or design;
- manifest mutation; successor-state mutation; any `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` transition from this memo alone;
- data acquisition (no additional days / symbols / families beyond the locked 90-day v002 envelope; no mark-price / spot / cross-venue / order-book / additional aggTrades; no 30s / 5m / 30m / 1h / 4h / longer-horizon label generation);
- research execution; paper / shadow / live-readiness / deployment / exchange-write / production keys / authenticated APIs / private endpoints / user stream / WebSockets / MCP / Graphify / `.mcp.json` / credentials;
- Phase 4 canonical; Phase 5; Phase 4bn-B; any ML-baseline implementation phase;
- old-strategy alt-symbol rerun, cooled-down-family reopening, or 5m research-thread reopening (Phase 3t closure preserved).

`RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION` means only that a future, separately authorized implementation phase *may* implement exactly the Phase 4bn-A design. **Any ML-baseline implementation requires a separately authorized implementation phase.**

## 15. Successor authorization

**None.**

Not authorized by this merge:

- Phase 4bn-B — ML-Baseline Implementation phase (or any phase under any name performing ML-baseline implementation)
- any ML-baseline implementation execution; ML model training; model scoring; prediction generation; feature ranking/selection; model selection through results; hyperparameter tuning; threshold tuning
- strategy research / design; signal generation; PnL simulation; backtests; walk-forward optimization
- diagnostics rerun; diagnostic artefact creation; ML artefact creation; reusable split-mask materialization; test-holdout tuning/design
- manifest mutation; successor-state mutation
- Phase 4bn-* further successors / Phase 4bo-* / Phase 4bp-* / Phase 5 / Phase 4 canonical
- additional aggTrades / 5m / 1m / tick / mark-price / order-book / spot / cross-venue data acquisition
- research execution; paper / shadow; live-readiness; deployment; exchange-write; production keys; authenticated APIs; private endpoints; user stream; WebSockets; MCP; Graphify; `.mcp.json`; credentials

## 16. Recommended state

**Remain paused.**

Phase 4bn-A is now merge-complete on main and, after the SHA-finalization commit and push, project-complete. The design decision `RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION` authorizes nothing. **Any ML-baseline implementation requires a separately authorized implementation phase.** **Phase 4bn-B is not authorized by Phase 4bn-A.** **Recommended state remains paused.**

**Conditional next, NOT authorized:** an ML-baseline implementation phase (provisionally `Phase 4bn-B`) is the cleanest non-paused option. It would implement *exactly* the Phase 4bn-A design — direction-classification baselines on 15s/60s, trained on train and evaluated on validation with the test holdout sealed, on the frozen 45-column v002 feature matrix, with train-only transforms, validation-only calibration, fixed a-priori baseline families, descriptive ML metrics, per-horizon censored-row masking, local gitignored outputs, and the specified test suite — training nothing in design and producing no strategy, signals, PnL, or backtest. That phase is **not authorized** by this merge.
