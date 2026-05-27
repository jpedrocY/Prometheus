# Phase 4bm-Y — Closeout

**Phase 4bm-Y is a docs-only ML-readiness scoping memo.** **Phase 4bm-Y does not train ML models.** **Phase 4bm-Y does not run ML.** **Phase 4bm-Y does not select models.** **Phase 4bm-Y does not rank or select features.** **Phase 4bm-Y does not tune hyperparameters.** **Phase 4bm-Y does not tune thresholds.** **Phase 4bm-Y does not define or run strategy.** **Phase 4bm-Y does not generate signals.** **Phase 4bm-Y does not simulate PnL.** **Phase 4bm-Y does not run backtests.** **Phase 4bm-Y does not authorize acquisition.** **Phase 4bm-Y does not authorize research execution.** **Phase 4bm-Y does not create ML artefacts.** **Phase 4bm-Y does not create diagnostic artefacts.** **Phase 4bm-Y does not create split masks.** **Phase 4bm-Y does not use the test holdout for tuning or design.** **Phase 4bm-Y does not mutate any manifest.** **Phase 4bm-Y does not mutate any successor-state artefact.** **Phase 4bm-Y does not commit data/microstructure.** **Phase 4bm-Y does not commit data/research.** **Any ML-readiness evaluation requires a separately authorized memo phase.** **Phase 4bm-Z is not authorized by Phase 4bm-Y.** **Recommended state remains paused.**

## 1. Branch name

`phase-4bm-y/multi-day-v002-ml-readiness-scoping-memo`

## 2. Base SHA

`6d149e19ad9574a0fc36f5bbe966e25b839aa036` (Phase 4bm-X merge-closeout SHA-finalization commit on `main`; `main == origin/main` verified at branch time). Phase 4bm-X merge commit `70e13ebd9133684e6e8c1d24c2c52dec6c2dce2c` and merge-closeout commit `837c605af616d3bb68ace7eea963e36478bad81d` present on `main`.

## 3. Commit SHA

- Docs commit: recorded by the commit that adds this memo + closeout + narrow current-project-state block (`docs(phase-4bm-y): define ml-readiness scoping boundaries`); the commit SHA is captured in the final operator report and git log.

## 4. Risk tier

**Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3. Defines the scope, boundaries, and non-authorizations for any possible future ML-readiness evaluation; adjacent to ML training / feature/model selection / threshold tuning / strategy research / backtests / acquisition / research execution while authorizing none.

## 5. Files changed

Docs (tracked):

- `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-y_ml-readiness-scoping-memo.md` (new)
- `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-y_closeout.md` (new, this file)
- `docs/00-meta/current-project-state.md` (narrow current-phase block update)

No source, test, committed-script, configuration, manifest, sidecar, gate-report, successor-state, or data artefact was created or modified.

## 6. Scoping decision result

`RECOMMEND_AUTHORIZE_ML_READINESS_EVALUATION_MEMO`.

This recommends only that a future, separately authorized, docs-only ML-readiness *evaluation* memo *may* be proposed. It authorizes no ML, no model training, no feature selection, no model selection, no hyperparameter tuning, no threshold tuning, no strategy research, no backtests, no acquisition, and no research execution.

## 7. Scope of future ML-readiness evaluation

A future evaluation memo would answer (at memo/governance level only) the admissibility questions defined in §9–§18 of the memo and decide whether a later ML-baseline implementation phase may be *proposed*. Strict one-way ordering: Phase 4bm-Y (scoping) → future Phase 4bm-Z-class (evaluation memo, still docs-only) → (only if separately authorized) ML-baseline implementation.

## 8. Admissible supervised-learning task-framing questions

Classification vs. regression vs. ordinal framing; horizon-specific vs. multi-horizon framing; direction-only vs. magnitude-aware targets; whether censored rows must be excluded per horizon; whether all horizons may be evaluated or whether any horizon should be deferred at evaluation-memo level; whether the task is per-horizon independent or shared-representation only at a later stage. Defined as questions only; Phase 4bm-Y selects no framing.

## 9. Target / horizon admissibility questions

1s / 5s / 15s / 60s each discussed separately. No horizon declared ML-ready. The memo may define what evidence would be required to evaluate each horizon later. 1s / 5s carry explicit latency/tradability caveats; 15s / 60s described as operationally less latency-sensitive but still not strategy-ready (60s also carries the largest censoring concentration, all in the test split).

## 10. Train / validation / test usage rules

Train and validation usable only in future separately authorized evaluation phases; test/final holdout single-use; no test-holdout tuning/design; no shuffled CV; no random split; no bootstrap split; no k-fold-over-time; no post-hoc temporal resampling; boundary embargo and boundary-crossing exclusion enforced; split masks not materialized unless separately authorized. Splits: train 45d (74,535,688 rows), validation 30d (56,819,939 rows), test 15d (23,797,822 rows); total 90d / 155,153,449 rows under `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`.

## 11. Metrics allowed at scoping level

Candidate families defined but not computed: class balance / prevalence; directional classification; regression error; rank / correlation; calibration; cost-aware descriptive; stability across train/validation only. No PnL metrics; no backtest metrics; no strategy metrics.

## 12. Leakage controls

Feature timestamp at or before label start (`src_ne_feature_ts = 0`); no future data in features; no boundary-crossing labels in earlier splits; no test-driven feature/model/threshold decisions; no post-hoc horizon selection based on test; no fitting scalers/imputers/encoders on validation or test; no feature engineering based on validation/test diagnostics unless separately authorized; no manifest mutation as a substitute for governance; censored rows treated as label-unavailable per horizon.

## 13. Baseline model families considered later without training

Majority / persistence / naive direction baselines; logistic regression; regularized linear models; calibrated tree ensembles; shallow gradient boosting; simple probabilistic baselines. No deep learning unless a later memo justifies it. No model family selected in Phase 4bm-Y.

## 14. Sample-weighting / class-imbalance / calibration questions

Whether class imbalance requires weighting; whether per-horizon censoring requires masking; whether calibration should be required for probability outputs; whether validation-only calibration is allowed; how to avoid test-holdout calibration leakage. Defined as questions only; Phase 4bm-Y answers none.

## 15. Cost-aware evaluation questions

§11.6 8 bps per side / 16 bps round trip; signal horizon vs. transaction costs; latency sensitivity (especially 1s / 5s); slippage and spread caveats. No strategy design, no PnL simulation, no backtests.

## 16. Future ML-readiness evaluation prerequisites

Future ML-readiness evaluation memo completed and merged; explicit allowed targets/horizons selected at memo level only; explicit leakage controls accepted; explicit metric policy accepted; explicit train/validation/test handling accepted; explicit cost-aware evaluation policy accepted; explicit non-use of test holdout for tuning/design; no unresolved blocking caveat; retained verdicts and locks preserved.

## 17. Phase 4bm-X decision and Phase 4bm-W verdict carried forward

- Phase 4bm-X decision: `RECOMMEND_AUTHORIZE_ML_READINESS_SCOPING_MEMO` (this Phase 4bm-Y is its separately authorized realization).
- Phase 4bm-W diagnostic verdict: `DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS` — 0 blocking structural failures; 4 non-blocking caveats (envelope-terminal censoring asymmetry 857 rows all in test; 538 embargo-excluded earlier-split rows; approximate-quantile method; historical `diagnostics_authorized=false` flag). Descriptive-only; not ML / strategy / backtest readiness. Phase 4bm-Y carries these forward as constraints and does not change, re-derive, or rerun them.

## 18. Required exact phrases

- Phase 4bm-Y is a docs-only ML-readiness scoping memo.
- Phase 4bm-Y does not train ML models.
- Phase 4bm-Y does not run ML.
- Phase 4bm-Y does not select models.
- Phase 4bm-Y does not rank or select features.
- Phase 4bm-Y does not tune hyperparameters.
- Phase 4bm-Y does not tune thresholds.
- Phase 4bm-Y does not define or run strategy.
- Phase 4bm-Y does not generate signals.
- Phase 4bm-Y does not simulate PnL.
- Phase 4bm-Y does not run backtests.
- Phase 4bm-Y does not authorize acquisition.
- Phase 4bm-Y does not authorize research execution.
- Phase 4bm-Y does not create ML artefacts.
- Phase 4bm-Y does not create diagnostic artefacts.
- Phase 4bm-Y does not create split masks.
- Phase 4bm-Y does not use the test holdout for tuning or design.
- Phase 4bm-Y does not mutate any manifest.
- Phase 4bm-Y does not mutate any successor-state artefact.
- Phase 4bm-Y does not commit data/microstructure.
- Phase 4bm-Y does not commit data/research.
- Any ML-readiness evaluation requires a separately authorized memo phase.
- Phase 4bm-Z is not authorized by Phase 4bm-Y.
- Recommended state remains paused.

## 19. Boundary confirmations

- No diagnostics rerun; no diagnostic artefact created.
- No ML artefact created; no split mask materialized.
- No feature selection / model selection / feature ranking / hyperparameter tuning / threshold tuning / strategy / signal / PnL / backtest / walk-forward.
- No manifest mutated (v002 label `5e17074d…` / feature `512a0a54…` byte-identical pre/post; re-hash MATCH).
- No successor-state artefact mutated (Phase 4bm-S `081730006c…`, Phase 4bm-U `6834ab11…` byte-identical pre/post; re-hash MATCH).
- No Phase 4bm-Q gate report mutated (`8a360608…` byte-identical pre/post; re-hash MATCH).
- Phase 4bm-W diagnostic outputs unchanged and gitignored (summary `f4b825af…`, summary sidecar `ff52873c…`, manifest `ac10061d…`, manifest sidecar `644506e3…`; re-hash MATCH; `.gitignore:88: data/research/`).
- No `data/microstructure/` artefact created, staged, or committed; no `data/research/` artefact created, staged, or committed.
- Test holdout not used for tuning or design.
- No acquisition; no research execution; no endpoint / WebSocket; no credentials; no `.env`; no `.mcp.json`; no MCP; no Graphify.
- Phase 4aw `flip_research_eligible` always-raises invariant preserved (never invoked).

## 20. Retained verdicts preserved

H0, R3, R1a, R1b-narrow, R2, F1, D1-A, 5m thread, V2, G1, C1 — all preserved verbatim. All prior phase results (Phase 4am .. Phase 4bm-X) preserved verbatim.

## 21. Project locks preserved

§11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 (0.25% / 2× / one-position / mark-price stops); Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6/§7/§8; Phase 4j §11; Phase 4k/4p/4q/4v/4w; Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy; Phase 4aw `flip_research_eligible(...)` always-raises invariant (never invoked); Phase 4bb-F canonical sidecar / path policy; Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks; Phase 4bm-A-P1 thin-prompt context-management standard; Phase 4bm-D-P1 lightweight Claude Code workspace standard — all preserved verbatim.

## 22. Recommended state

**Remain paused.** Branch-complete only; not merged; not project-complete. A separately authorized Tier 1 merge phase is required for project completion. The scoping decision `RECOMMEND_AUTHORIZE_ML_READINESS_EVALUATION_MEMO` authorizes nothing. **Any ML-readiness evaluation requires a separately authorized memo phase.** **Phase 4bm-Z is not authorized by Phase 4bm-Y.** **Recommended state remains paused.**
