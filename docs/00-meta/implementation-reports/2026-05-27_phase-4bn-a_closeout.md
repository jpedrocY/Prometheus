# Phase 4bn-A — Closeout

**Phase 4bn-A is a docs-only / design-only ML-baseline implementation scoping phase.** **Phase 4bn-A does not train ML models.** **Phase 4bn-A does not run ML.** **Phase 4bn-A does not score models.** **Phase 4bn-A does not generate predictions.** **Phase 4bn-A does not select models through results.** **Phase 4bn-A does not rank or select features.** **Phase 4bn-A does not tune hyperparameters.** **Phase 4bn-A does not tune thresholds.** **Phase 4bn-A does not define or run strategy.** **Phase 4bn-A does not generate signals.** **Phase 4bn-A does not simulate PnL.** **Phase 4bn-A does not run backtests.** **Phase 4bn-A does not authorize acquisition.** **Phase 4bn-A does not authorize research execution.** **Phase 4bn-A does not create ML artefacts.** **Phase 4bn-A does not create diagnostic artefacts.** **Phase 4bn-A does not create reusable split masks.** **Phase 4bn-A does not use the test holdout for tuning or design.** **Phase 4bn-A does not mutate any manifest.** **Phase 4bn-A does not mutate any successor-state artefact.** **Phase 4bn-A does not commit data/microstructure.** **Phase 4bn-A does not commit data/research.** **Any ML-baseline implementation requires a separately authorized implementation phase.** **Phase 4bn-B is not authorized by Phase 4bn-A.** **Recommended state remains paused.**

> **Successor-naming note.** Phase 4bm-Z closed the `4bm-` letter-series; this phase opens the `4bn-` series. By the repo's within-series convention the next phase after Phase 4bn-A is `Phase 4bn-B`, named in the required exact phrases as the unauthorized future ML-baseline implementation phase. No successor is authorized under any name.

## 1. Branch name

`phase-4bn-a/multi-day-v002-ml-baseline-implementation-scoping-design`

## 2. Base SHA

`de170ad31b9dd71e9f5c8fac59d4b19472d9e6d0` (Phase 4bm-Z merge-closeout SHA-finalization commit on `main`; `main == origin/main` verified at branch time). Phase 4bm-Z merge commit `5b86ecf496421e86138179f47c8273aa1837dbd1` and merge-closeout commit `b8afee7b4e9762e3880d1a782799631d588e78a1` present on `main`.

## 3. Commit SHA

- Docs commit: recorded by the commit that adds this memo + closeout + narrow current-project-state block (`docs(phase-4bn-a): scope ml-baseline implementation design`); the commit SHA is captured in the final operator report and git log.

## 4. Risk tier

**Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3. Begins the ML arc by defining the exact implementation boundaries for a future ML-baseline implementation; adjacent to ML training / model scoring / prediction generation / feature/model selection / hyperparameter tuning / threshold tuning / strategy research / backtests / acquisition / research execution while authorizing none.

## 5. Files changed

Docs (tracked):

- `docs/00-meta/implementation-reports/2026-05-27_phase-4bn-a_ml-baseline-implementation-scoping-design.md` (new)
- `docs/00-meta/implementation-reports/2026-05-27_phase-4bn-a_closeout.md` (new, this file)
- `docs/00-meta/current-project-state.md` (narrow current-phase block update)

No source, test, committed-script, configuration, manifest, sidecar, gate-report, successor-state, or data artefact was created or modified.

## 6. Design decision result

`RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION`.

This recommends only that a future, separately authorized implementation phase may implement exactly the Phase 4bn-A design. It does not authorize implementation in Phase 4bn-A, model training in Phase 4bn-A, any successor execution by itself, or strategy / signals / PnL simulation / backtests / acquisition / paper / shadow / live-readiness / exchange-write.

## 7. Design criteria results

All twenty-one criteria PASS:

- **A** Phase 4bm-Z completed/merged the docs-only ML-readiness evaluation memo — PASS.
- **B** Phase 4bm-Z recommended ML-baseline implementation scoping/design — PASS.
- **C** Future implementation boundary definable without training models here — PASS.
- **D** Target framing specifiable without using test holdout for tuning/design — PASS.
- **E** Horizon inclusion/deferral specifiable without declaring any horizon strategy-ready — PASS.
- **F** Train/validation/test handling can enforce the Phase 4bm-U split policy — PASS.
- **G** Censored-row handling definable per horizon — PASS.
- **H** Feature surface freezable to v002 feature family without new feature engineering — PASS.
- **I** Transform/preprocessing rules can enforce train-only fitting — PASS.
- **J** Baseline families selectable for first implementation at design level without result-based selection — PASS.
- **K** Metric policy specifiable without computing metrics here — PASS.
- **L** Calibration policy specifiable without fitting calibration here — PASS.
- **M** Cost-aware descriptive evaluation specifiable without strategy/backtest/PnL — PASS.
- **N** Output artefact policy keeps all future outputs local and gitignored — PASS.
- **O** Test/validation requirements specifiable without running implementation — PASS.
- **P** Anti-drift boundaries prevent ML/strategy/backtest/acquisition drift — PASS.
- **Q** No diagnostics rerun — PASS.
- **R** No ML / scoring / predictions / feature-or-model selection / hp/threshold tuning / strategy / backtest occurred — PASS.
- **S** No manifest or successor-state mutation — PASS.
- **T** No data/microstructure or data/research artefact committed — PASS.
- **U** Retained verdicts and project locks unchanged — PASS.

## 8. Phase 4bm-Z decision carried forward

`RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION_SCOPING` (Phase 4bm-Z; criteria A–R PASS). This Phase 4bn-A is its separately authorized realization. Phase 4bm-W diagnostic verdict `DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS` (0 blocking; 4 non-blocking caveats) carried forward as constraints; not re-derived, not rerun.

## 9. Target framing design

Direction classification only; 3-class `{-1, 0, +1}` from the existing v002 label family; zero/flat class kept explicit (not merged, not dropped); no magnitude regression; no ordinal framing; no meta-labeling; per-horizon-independent.

## 10. Horizon inclusion / deferral design

Include 15s and 60s in first baseline; defer 1s and 5s (latency/tradability sensitivity, cost-commensurability risk); 1s/5s revisited only by later separately authorized phases; 60s carries the test-split censoring caveat with per-horizon masking; no horizon strategy-ready; no horizon live-tradable.

## 11. Train / validation / test handling design

`CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`: train 45d / 74,535,688 rows; validation 30d / 56,819,939 rows; test 15d / 23,797,822 rows; total 90d / 155,153,449 rows. Train fits transforms/models (future phase only); validation evaluates/calibrates (future phase only, explicit rules); test sealed/unused unless a later phase authorizes a single terminal holdout eval; no test-holdout tuning/design; no random/shuffled/k-fold/bootstrap/resampling; 60s boundary embargo + boundary-crossing exclusion; split masks local + gitignored, reusable masks not authorized.

## 12. Censored-row handling design

Per-horizon label-unavailable; excluded from supervised loss and metric denominator for that horizon; not imputed; not treated as zero/flat; censored counts reported per split×horizon (v002 aggregate `{1s:14,5s:39,15s:170,60s:634}`, all in test).

## 13. Feature surface design

Existing v002 feature family only; `feature_config_hash 819cfa7a…` preserved; no new engineering/selection/ranking/pruning. Model matrix = the 45 `computed_feature_column_names` (40 rolling features across 1s/5s/15s/60s + `utc_hour`, `utc_minute`, `milliseconds_since_day_start`, `invalid_window_flag`, `rolling_missing_window_flag`), frozen by deterministic rule from manifest evidence. Excluded: 17 lineage/identifier/timestamp/SHA columns, all label columns, split flags.

## 14. Transform / preprocessing design

Fit scalers/imputers/encoders on train only; apply to validation only; no fit on validation/test; no target leakage; explicit missingness handling (flag columns + train-fit imputation); class encoding preserves zero/flat class; transform metadata persisted only as local gitignored output.

## 15. Baseline model-family design

A priori (no result-based selection, no search): (1) majority-class/class-prior; (2) naive persistence/naive-direction if leakage-free; (3) (regularized) multinomial logistic regression; (4) regularized linear classifier; (5) optionally one bounded shallow tree (fixed pre-declared depth). No deep learning. Gradient boosting deferred to a later baseline-expansion phase (tuning-sensitivity justification). No hyperparameter search; no model-family selection through results; no ensemble selection.

## 16. Metric policy design

Defined, not computed: class prevalence; confusion matrix; accuracy; balanced accuracy; macro F1; per-class precision/recall; log loss (if probabilistic); Brier/calibration (if probabilistic); train/validation stability; §11.6-locked cost-commensurability descriptive summary. Forbidden: PnL; backtest metrics; Sharpe/Sortino/drawdown; hit-rate-as-strategy; threshold-tuned metrics; test-set metrics in first implementation; any metric used to design strategy or tune trade thresholds.

## 17. Calibration design

Validation-only calibration evaluation in a future phase; no test calibration; no threshold tuning; no probability-to-signal conversion; calibration outputs descriptive / ML-evaluation only; no strategy triggers.

## 18. Cost-aware descriptive evaluation design

§11.6 = 8 bps per side / 16 bps round trip locked reference; descriptive cost-commensurability summaries only; no PnL simulation; no strategy construction; no entry/exit rules; no trade threshold design; no order/position model; no backtest.

## 19. Output artefact design

Future outputs local + gitignored under an approved namespace (e.g. `data/research/microstructure/ml-baselines/phase-4bn-b/`): `ml_baseline_run_manifest.json`(+`.sha256`), `per_horizon_model_summary.json`(+`.sha256`), `metrics_train_validation.csv`, `calibration_summary.csv`, `class_balance_summary.csv`, `feature_schema_used.json`, `transform_metadata.json`, model artefacts only if separately authorized. Canonical Phase 4bb-F sidecar format. No implementation outputs / model artefacts / data/research / data/microstructure committed.

## 20. Test / validation design

Future tests: split-policy enforcement; test-holdout exclusion; train-only transform fitting; no validation/test fit; censored-row exclusion by horizon; feature/label alignment; no leakage columns; no forbidden imports/endpoints/credentials; output sidecar format; local-output gitignore behaviour; no strategy/backtest/PnL functions; deterministic manifest generation; CLI dry-run/small-fixture if applicable.

## 21. Proposed future implementation surface (named only; not created)

Modules: `ml_baseline_design_v002.py`, `ml_baseline_dataset_v002.py`, `ml_baseline_models_v002.py`, `ml_baseline_metrics_v002.py`, `ml_baseline_report_v002.py` (under `src/prometheus/research/microstructure/`). Script: `scripts/phase4bn_b_run_ml_baseline_v002.py`. Tests: `test_ml_baseline_dataset_v002.py`, `test_ml_baseline_split_policy_v002.py`, `test_ml_baseline_no_leakage_v002.py`, `test_ml_baseline_no_network.py`, `test_ml_baseline_outputs_v002.py`. None created by Phase 4bn-A.

## 22. Evidence reviewed

Phase 4bm-Z / 4bm-Y / 4bm-X / 4bm-W reports, closeouts, merge-closeouts; Phase 4bm-V/U/T/S/R/Q/P reports and closeouts; `merge-closeout-standard.md`; `phase-risk-tiering-standard.md`; Phase 4bm-A-P1 / 4bm-D-P1 standards; `current-project-state.md`; v002 feature manifest schema (read-only, for the §13 feature surface). All local diagnostic outputs and predecessor artefacts re-hashed read-only — all MATCH.

## 23. Required exact phrases

- Phase 4bn-A is a docs-only / design-only ML-baseline implementation scoping phase.
- Phase 4bn-A does not train ML models.
- Phase 4bn-A does not run ML.
- Phase 4bn-A does not score models.
- Phase 4bn-A does not generate predictions.
- Phase 4bn-A does not select models through results.
- Phase 4bn-A does not rank or select features.
- Phase 4bn-A does not tune hyperparameters.
- Phase 4bn-A does not tune thresholds.
- Phase 4bn-A does not define or run strategy.
- Phase 4bn-A does not generate signals.
- Phase 4bn-A does not simulate PnL.
- Phase 4bn-A does not run backtests.
- Phase 4bn-A does not authorize acquisition.
- Phase 4bn-A does not authorize research execution.
- Phase 4bn-A does not create ML artefacts.
- Phase 4bn-A does not create diagnostic artefacts.
- Phase 4bn-A does not create reusable split masks.
- Phase 4bn-A does not use the test holdout for tuning or design.
- Phase 4bn-A does not mutate any manifest.
- Phase 4bn-A does not mutate any successor-state artefact.
- Phase 4bn-A does not commit data/microstructure.
- Phase 4bn-A does not commit data/research.
- Any ML-baseline implementation requires a separately authorized implementation phase.
- Phase 4bn-B is not authorized by Phase 4bn-A.
- Recommended state remains paused.

## 24. Boundary confirmations

- No diagnostics rerun; no diagnostic artefact created.
- No ML artefact created; no reusable split mask created/materialized.
- No model training / scoring / prediction generation / feature selection / model selection / feature ranking / hyperparameter tuning / threshold tuning / strategy / signal / PnL / backtest / walk-forward.
- No manifest mutated (v002 label `5e17074d…` / feature `512a0a54…` byte-identical pre/post; re-hash MATCH).
- No successor-state artefact mutated (Phase 4bm-S `081730006c…`, Phase 4bm-U `6834ab11…` byte-identical pre/post; re-hash MATCH).
- No Phase 4bm-Q gate report mutated (`8a360608…` byte-identical pre/post; re-hash MATCH).
- Phase 4bm-W diagnostic outputs unchanged and gitignored (summary `f4b825af…`, summary sidecar `ff52873c…`, manifest `ac10061d…`, manifest sidecar `644506e3…`; re-hash MATCH; `.gitignore:88: data/research/`).
- No `data/microstructure/` artefact created, staged, or committed; no `data/research/` artefact created, staged, or committed.
- Test holdout not used for tuning or design.
- No acquisition; no research execution; no endpoint / WebSocket; no credentials; no `.env`; no `.mcp.json`; no MCP; no Graphify.
- Phase 4aw `flip_research_eligible` always-raises invariant preserved (never invoked).

## 25. Retained verdicts preserved

H0, R3, R1a, R1b-narrow, R2, F1, D1-A, 5m thread, V2, G1, C1 — all preserved verbatim. All prior phase results (Phase 4am .. Phase 4bm-Z) preserved verbatim.

## 26. Project locks preserved

§11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 (0.25% / 2× / one-position / mark-price stops); Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6/§7/§8; Phase 4j §11; Phase 4k/4p/4q/4v/4w; Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy; Phase 4aw `flip_research_eligible(...)` always-raises invariant (never invoked); Phase 4bb-F canonical sidecar / path policy; Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks; Phase 4bm-A-P1 thin-prompt context-management standard; Phase 4bm-D-P1 lightweight Claude Code workspace standard — all preserved verbatim.

## 27. Recommended state

**Remain paused.** Branch-complete only; not merged; not project-complete. A separately authorized Tier 1 merge phase is required for project completion. The design decision `RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION` authorizes nothing. **Any ML-baseline implementation requires a separately authorized implementation phase.** **Phase 4bn-B is not authorized by Phase 4bn-A.** **Recommended state remains paused.**
