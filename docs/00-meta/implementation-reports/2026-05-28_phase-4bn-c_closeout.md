# Phase 4bn-C — Closeout

**Phase 4bn-C is a docs-only ML-baseline evidence interpretation / forensic memo.** **Phase 4bn-C does not train ML models.** **Phase 4bn-C does not run ML.** **Phase 4bn-C does not score models.** **Phase 4bn-C does not generate predictions.** **Phase 4bn-C does not select models through results.** **Phase 4bn-C does not rank or select features.** **Phase 4bn-C does not tune hyperparameters.** **Phase 4bn-C does not tune thresholds.** **Phase 4bn-C does not define or run any strategy.** **Phase 4bn-C does not generate trade signals.** **Phase 4bn-C does not simulate PnL.** **Phase 4bn-C does not run backtests.** **Phase 4bn-C does not authorize acquisition.** **Phase 4bn-C does not call any public, authenticated, or private endpoint.** **Phase 4bn-C does not open any WebSocket or user stream.** **Phase 4bn-C does not use credentials, .env, .mcp.json, MCP, or Graphify.** **Phase 4bn-C does not mutate any manifest.** **Phase 4bn-C does not mutate any successor-state artefact.** **Phase 4bn-C does not commit data/microstructure.** **Phase 4bn-C does not commit data/research.** **Phase 4bn-C does not persist model binaries.** **Phase 4bn-C does not persist row-level predictions.** **Phase 4bn-C does not create reusable split masks.** **Phase 4bn-C does not authorize Phase 4bn-D, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, or any successor phase.** **Recommended state remains paused.**

## 1. Phase identity

Phase 4bn-C — Multi-Day V002 ML-Baseline Evidence Interpretation / Forensic Memo. Docs-only governance / interpretation / forensic memo. Tier 1 — Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` §3. **Branch-complete only.** Not merged into `main`; not project-complete. A separately authorized Tier 1 merge phase is required for project completion per `docs/00-meta/process/merge-closeout-standard.md`.

## 2. Branch name

`phase-4bn-c/multi-day-v002-ml-baseline-evidence-interpretation`

## 3. Base SHA

`3c59a323e4f0e506caf63ef73afccaf931b3c631` (Phase 4bn-B merge-closeout SHA-finalization commit `docs(phase-4bn-b): finalize merge closeout shas`; `main == origin/main` verified at branch time). Phase 4bn-B merge commit `97b3f8f50edc6c13241b4adaedd4a1eff332dea1` and merge-closeout commit `b321e5ce4419a0218341b0d35a934a10e4bf0ff0` present on `main`.

## 4. Commit SHA

- Docs commit: recorded by the commit that adds this closeout + the interpretation memo + the narrow `current-project-state.md` block (`docs(phase-4bn-c): interpret ml-baseline evidence`); the commit SHA is captured in the final operator report and `git log`.

## 5. Risk tier

**Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3. Interprets the first actual ML-baseline implementation evidence and may recommend whether the ML arc should remain paused, proceed to a tightly bounded baseline-expansion / design phase, revisit labels / targets, or investigate class imbalance / regime conditioning. Adjacent to ML expansion, model selection, feature selection, hyperparameter tuning, threshold tuning, strategy research, backtests, and test-holdout misuse while authorizing none.

## 6. Files changed

Docs (tracked):

- `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-c_ml-baseline-evidence-interpretation-memo.md` (new)
- `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-c_closeout.md` (new, this file)
- `docs/00-meta/current-project-state.md` (narrow current-phase paragraph + Current-phase block addition; prior Phase 4bn-B paragraph and prior Current-phase blocks preserved as labelled historical context)

No source, test, committed-script, configuration, manifest, sidecar, gate-report, successor-state, or data artefact was created or modified.

## 7. Interpretation decision result

**`RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING`.**

This recommends only that a future, separately authorized docs-only / design-only scoping phase may scope a bounded baseline-expansion attempt. It does not authorize implementation, model training, model scoring, prediction generation, feature ranking / selection, model selection through results, hyperparameter tuning, threshold tuning, strategy, signals, PnL simulation, backtests, acquisition, manifest mutation, successor-state mutation, paper / shadow / live-readiness, deployment, or exchange-write.

## 8. Phase 4bn-B decision carried forward

`RECORD_EVIDENCE_ONLY` (Phase 4bn-B; merge-complete, SHA-finalized, project-complete on `main`). Phase 4bn-B implemented exactly the Phase 4bn-A §9 – §20 design and produced descriptive ML-baseline evidence on the train and validation splits only. The test holdout is sealed (`test_rows_loaded: 0`). The four fixed-a-priori baseline families (`majority_class_prior`, `persistence_past_return_sign`, `multinomial_logistic_regression_l2`, `multinomial_linear_classifier_l1`) were each run exactly once with locked SGD hyperparameters; no model was selected as "best"; no feature was ranked or selected; no hyperparameter or threshold was tuned; no strategy / signal / PnL / backtest exists.

## 9. Interpretation summary

Interpretation findings carried forward from §9 – §15 of the Phase 4bn-C memo:

- **Class prevalence:** the `flat` class is **underrepresented** at 0.15 – 1.09 % across both included horizons and both supervised splits. The directional classes are near-balanced (down ≈ up ≈ 0.495 ± 0.005). Accuracy alone is a weak indicator in this regime; balanced accuracy and macro F1 are more honest reference points (majority floors 0.3333 and ~0.22 respectively).
- **L2 / L1 linear classifiers:** a real ~5 pp accuracy lift at 15s over the majority prior (0.5435 vs 0.4938) and a ~14 pp macro-F1 lift (0.3638 vs 0.2204), with controlled train-validation deltas (~0.5 pp). At 60s the accuracy lift shrinks to ~1.5 pp and the predictions become strongly down-biased. The flat class is never predicted by the L2 / L1 models (per-class P/R/F1 = 0/0/0 on flat in every cell). Phase 4bn-C **does not select** L1 over L2, does not select 15s over 60s, and does not select linear over majority.
- **Persistence:** beats majority on hard accuracy at 15s (+2.3 pp) and at 60s (+0.2 pp) but is catastrophically worse on log-loss (~18× the majority floor) and Brier (~2× the majority floor) due to its hard one-hot probability outputs. **This is not negative evidence about momentum / continuation per se; it is direct evidence that hard-class persistence outputs are uncalibrated.** No strategy conclusion is drawn.
- **Calibration:** the L2 logistic at 15s is well-calibrated in the dominant 0.5 – 0.6 confidence bin (which contains ~86 % of validation rows) but **severely over-confident in the 0.6 – 1.0 tail** (reliability gaps ranging from −0.061 to −0.392). The most-confident predictions are not the most-accurate ones; a naive "threshold the probabilities" follow-up would fail under this evidence. No threshold is tuned; no calibrator is fit.
- **§11.6 cost-commensurability:** at 15s validation only **6.2 %** of `|forward_log_return|` rows exceed 1× the 16 bps round-trip cost (1.6 % at 2×, 0.16 % at 5×); at 60s the corresponding fractions are 18.3 % / 5.8 % / 0.93 %. This is descriptive context only and is **not a tradability claim**.
- **Test holdout:** sealed; `test_rows_loaded: 0`; verified by `test_ml_baseline_split_policy_v002.test_test_holdout_iteration_is_forbidden_by_design`. **Phase 4bn-C does not inspect, evaluate, tune, design, model-select, or report any metric on test data.**

## 10. Weak-separation forensic hypotheses

The memo enumerates twelve non-mutually-exclusive forensic hypotheses (label imbalance / flat-class collapse; target bluntness; horizon-vs-cost mismatch; feature-surface limitations; linear-model simplicity; class-weighting absence by design; shallow-tree memory fail-closed; regime heterogeneity; time-of-day effects; feature-stationarity drift; labels capturing common no-move behavior more than exploitable directional edge; the market may not contain a simple exploitable edge under this family). **None is ranked, weighted, resolved, or converted into a design or strategy proposal.** They are surfaced so that a future separately authorized scoping memo can choose which (if any) to bound.

## 11. Follow-up paths evaluated

The memo evaluates exactly five candidate follow-up paths:

1. `RECOMMEND_REMAIN_PAUSED_ML_ARC` — rejected: over-claims confidence in the negative direction given the reproducible 15s lift with controlled stability deltas.
2. **`RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING` — chosen.** Cheaper and more honest than option 1 or option 5; the obvious next-step ideas (threshold tuning, naive expansion) would fail under the existing evidence, so a scoping memo that enumerates exactly which questions could be evaluated under predeclared evaluation rules is the appropriate next step.
3. `RECOMMEND_AUTHORIZE_LABEL_TARGET_REWORK_SCOPING` — rejected as the *immediate* next phase but listed as a legitimate question family inside option 2's scoping menu (hypotheses H2 / H11).
4. `RECOMMEND_AUTHORIZE_CLASS_IMBALANCE_OR_REGIME_CONDITIONING_SCOPING` — rejected as a separate concurrent phase but listed as a question family inside option 2's scoping menu (hypotheses H1 / H6 / H8 / H9).
5. `DO_NOT_RECOMMEND_FURTHER_ML_WORK_ON_CURRENT_V002_FAMILY` — rejected: the existing evidence does not warrant a "stop work" verdict; the 15s lift is real but small and the calibration / cost evidence raises legitimate scoping-level questions.

## 12. What a future follow-up phase would be allowed to evaluate

Phase 4bn-D, **not** authorized here, could (at design level only, without running anything) evaluate the candidate questions enumerated in §18 of the memo: class weighting; memory-bounded shallow-tree specification; descriptive-only calibration analysis; 1s / 5s deferral revisit; class-weighted softmax re-evaluation at 15s / 60s; target-balance thresholds reconsideration at scoping level; time-of-day or regime segmentation scoping. **No execution. No training. No scoring. No prediction. No selection. No tuning. No strategy. No signals. No PnL. No backtests. No acquisition. Test holdout remains sealed.**

## 13. Boundary confirmations

- no source code modified; no test modified; no committed script modified; no config modified.
- no `.gitignore`, `pyproject.toml`, or `README.md` modified.
- no MCP file modified or read.
- no `data/microstructure/` artefact committed; no `data/research/` artefact committed.
- no manifest mutated; no `research_eligible` flipped; no `eligibility_gate_status` transitioned; no `chronological_split_policy` changed; no `diagnostics_authorized` / `ml_authorized` changed.
- no successor-state artefact mutated (Phase 4bm-S `081730006c…`, Phase 4bm-U `6834ab11…` byte-identical).
- no Phase 4bm-Q gate report mutated (`8a360608…` byte-identical).
- no Phase 4bm-W diagnostic outputs mutated (`f4b825af…`, `ff52873c…`, `ac10061d…`, `644506e3…` byte-identical).
- no Phase 4bn-B local output mutated (`cd436e38…`, `d94f8d72…`, `40cde4a0…`, `a0f469d2…`, `6e6338bf…`, `5f3d84b4…`, `73b455af…` byte-identical, plus all seven `.sha256` sidecars byte-identical).
- no v002 label or feature manifest mutated (`5e17074d…`, `512a0a54…` byte-identical).
- no diagnostics rerun; no diagnostic artefact created.
- no ML rerun; no ML artefact created; no reusable split mask created / materialized; no model binary persisted; no row-level prediction persisted.
- no model training / scoring / prediction generation / feature ranking / feature selection / model selection through results / hyperparameter tuning / threshold tuning.
- no strategy defined or run; no trade signals generated; no PnL simulated; no backtests run; no walk-forward optimization.
- test holdout not used for any reason.
- no data acquired; no public / authenticated / private endpoint called; no Binance API called; no WebSocket / user-stream opened; no credential / `.env` / `.mcp.json` / MCP / Graphify used.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked).
- no retained verdict revised; no project lock loosened; no M0 amendment; no successor authorized.

## 14. Retained verdicts preserved

H0, R3, R1a, R1b-narrow, R2, F1, D1-A, 5m thread, V2, G1, C1 — all preserved verbatim. All prior phase results (Phase 4am .. Phase 4bn-B) preserved verbatim.

## 15. Project locks preserved

§11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 (0.25% / 2× / one-position / mark-price stops); Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k / 4p / 4q / 4v / 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy; Phase 4aw `flip_research_eligible(...)` always-raises invariant (never invoked); Phase 4bb-F canonical sidecar / path policy; Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks; Phase 4bm-A-P1 thin-prompt context-management standard; Phase 4bm-D-P1 lightweight Claude Code workspace standard — all preserved verbatim.

## 16. Recommended state

**Remain paused.** Branch-complete only; not merged; not project-complete. A separately authorized Tier 1 merge phase is required for project completion. The interpretation decision `RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING` authorizes nothing. **Phase 4bn-D is not authorized by Phase 4bn-C.** **Recommended state remains paused.**

## 17. Required exact phrases (verbatim)

- Phase 4bn-C is a docs-only ML-baseline evidence interpretation / forensic memo.
- Phase 4bn-C does not train ML models.
- Phase 4bn-C does not run ML.
- Phase 4bn-C does not score models.
- Phase 4bn-C does not generate predictions.
- Phase 4bn-C does not select models through results.
- Phase 4bn-C does not rank or select features.
- Phase 4bn-C does not tune hyperparameters.
- Phase 4bn-C does not tune thresholds.
- Phase 4bn-C does not define or run any strategy.
- Phase 4bn-C does not generate trade signals.
- Phase 4bn-C does not simulate PnL.
- Phase 4bn-C does not run backtests.
- Phase 4bn-C does not authorize acquisition.
- Phase 4bn-C does not call any public, authenticated, or private endpoint.
- Phase 4bn-C does not open any WebSocket or user stream.
- Phase 4bn-C does not use credentials, .env, .mcp.json, MCP, or Graphify.
- Phase 4bn-C does not mutate any manifest.
- Phase 4bn-C does not mutate any successor-state artefact.
- Phase 4bn-C does not commit data/microstructure.
- Phase 4bn-C does not commit data/research.
- Phase 4bn-C does not persist model binaries.
- Phase 4bn-C does not persist row-level predictions.
- Phase 4bn-C does not create reusable split masks.
- Phase 4bn-C does not authorize Phase 4bn-D, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, or any successor phase.
- Recommended state remains paused.
