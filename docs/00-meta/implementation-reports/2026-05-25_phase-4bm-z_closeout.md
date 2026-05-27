# Phase 4bm-Z — Closeout

**Phase 4bm-Z is a docs-only ML-readiness evaluation memo.** **Phase 4bm-Z does not train ML models.** **Phase 4bm-Z does not run ML.** **Phase 4bm-Z does not score models.** **Phase 4bm-Z does not generate predictions.** **Phase 4bm-Z does not select models.** **Phase 4bm-Z does not rank or select features.** **Phase 4bm-Z does not tune hyperparameters.** **Phase 4bm-Z does not tune thresholds.** **Phase 4bm-Z does not define or run strategy.** **Phase 4bm-Z does not generate signals.** **Phase 4bm-Z does not simulate PnL.** **Phase 4bm-Z does not run backtests.** **Phase 4bm-Z does not authorize acquisition.** **Phase 4bm-Z does not authorize research execution.** **Phase 4bm-Z does not create ML artefacts.** **Phase 4bm-Z does not create diagnostic artefacts.** **Phase 4bm-Z does not create split masks.** **Phase 4bm-Z does not use the test holdout for tuning or design.** **Phase 4bm-Z does not mutate any manifest.** **Phase 4bm-Z does not mutate any successor-state artefact.** **Phase 4bm-Z does not commit data/microstructure.** **Phase 4bm-Z does not commit data/research.** **Any ML-baseline implementation requires a separately authorized implementation phase.** **Phase 4bn-A is not authorized by Phase 4bm-Z.** **Recommended state remains paused.**

> **Successor-naming note.** `Z` is the terminal letter of the `4bm-` series; by the repo's established convention (the Phase 4bm-Y / 4bm-X memos enumerate `Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-*` as unauthorized successors), the next letter-series is `4bn-A`. The required exact phrases therefore name **`Phase 4bn-A`** as the unauthorized successor. No successor is authorized under any name.

## 1. Branch name

`phase-4bm-z/multi-day-v002-ml-readiness-evaluation-memo`

## 2. Base SHA

`2463ceb716d31c79ef766e9042fd40a3929f3e5c` (Phase 4bm-Y merge-closeout SHA-finalization commit on `main`; `main == origin/main` verified at branch time). Phase 4bm-Y merge commit `5c86c4df9459d1cf854f1c72b2677605745b0e85` and merge-closeout commit `9d90e6aefea82ccbb7d08fb2647985f73c9e6b71` present on `main`.

## 3. Commit SHA

- Docs commit: recorded by the commit that adds this memo + closeout + narrow current-project-state block (`docs(phase-4bm-z): evaluate ml-readiness scope`); the commit SHA is captured in the final operator report and git log.

## 4. Risk tier

**Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3. Evaluates whether a later ML-baseline implementation phase may be proposed; adjacent to ML training / feature/model selection / threshold tuning / strategy research / backtests / acquisition / research execution while authorizing none.

## 5. Files changed

Docs (tracked):

- `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-z_ml-readiness-evaluation-memo.md` (new)
- `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-z_closeout.md` (new, this file)
- `docs/00-meta/current-project-state.md` (narrow current-phase block update)

No source, test, committed-script, configuration, manifest, sidecar, gate-report, successor-state, or data artefact was created or modified.

## 6. Evaluation decision result

`RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION_SCOPING`.

This recommends only that a future, separately authorized, docs-only or design-only ML-baseline implementation *scoping/design* phase *may* be proposed. It authorizes no ML implementation, no model training, no model scoring, no prediction generation, no feature selection, no model selection, no hyperparameter tuning, no threshold tuning, no strategy research, no backtests, no acquisition, and no research execution.

## 7. Evaluation criteria results

All eighteen criteria PASS:

- **A** Phase 4bm-Y completed and merged the docs-only ML-readiness scoping memo — PASS.
- **B** Phase 4bm-Y scope internally complete enough to support a future ML-baseline implementation scoping/design phase — PASS.
- **C** Phase 4bm-W diagnostics have 0 blocking structural failures — PASS.
- **D** Phase 4bm-W non-blocking caveats carried forward as constraints; do not block implementation scoping — PASS.
- **E** Phase 4bm-U split policy sufficient for later ML-baseline design — PASS.
- **F** Train/validation/test usage rules explicit and enforceable — PASS.
- **G** Test holdout remains protected from tuning/design — PASS.
- **H** Leakage controls explicit and enforceable — PASS.
- **I** Candidate metrics scoped without computing them now — PASS.
- **J** Candidate baseline families scoped without training them now — PASS.
- **K** Sample-weighting / imbalance / calibration questions explicitly identified — PASS.
- **L** Cost-aware constraints explicit and include §11.6 8 bps per side / 16 bps round trip — PASS.
- **M** Horizon-specific constraints explicit (1s/5s latency sensitivity; 60s censoring concentration) — PASS.
- **N** No diagnostics rerun — PASS.
- **O** No ML / strategy / backtest work authorized or run — PASS.
- **P** No manifest or successor-state mutation — PASS.
- **Q** No data/microstructure or data/research artefact committed — PASS.
- **R** Retained verdicts and project locks unchanged — PASS.

## 8. Phase 4bm-Y decision and Phase 4bm-W verdict carried forward

- Phase 4bm-Y scoping decision: `RECOMMEND_AUTHORIZE_ML_READINESS_EVALUATION_MEMO` (this Phase 4bm-Z is its separately authorized realization).
- Phase 4bm-W diagnostic verdict: `DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS` — 0 blocking structural failures; 4 non-blocking caveats (envelope-terminal censoring asymmetry 857 rows all in test; 538 embargo-excluded earlier-split rows; approximate-quantile method; historical `diagnostics_authorized=false` flag). Descriptive-only; not ML / strategy / backtest readiness. Phase 4bm-Z carries these forward as constraints and does not change, re-derive, or rerun them.

## 9. Supervised-learning task-framing evaluation

Classification vs. regression vs. ordinal; horizon-specific vs. multi-horizon; direction-only vs. magnitude-aware (with explicit treatment of the large short-horizon exact-zero mass); censored-row handling per horizon. Scope complete and admissible; **no framing selected** by Phase 4bm-Z.

## 10. Target / horizon admissibility evaluation

1s / 5s / 15s / 60s each discussed separately; **no horizon declared ML-ready**; **no horizon selected**. 1s / 5s carry explicit latency/tradability caveats; 15s / 60s less latency-sensitive but still not strategy-ready; 60s carries the largest censoring concentration (634 of 857), all in the test split.

## 11. Train / validation / test usage evaluation

`CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`: train 45d (74,535,688 rows), validation 30d (56,819,939 rows), test 15d (23,797,822 rows); total 90d / 155,153,449 rows. Train/validation usable only in future separately authorized phases; test/final holdout single-use; no test-holdout tuning/design; no shuffle / random / k-fold / bootstrap / resampling; 60s embargo and boundary-crossing exclusion enforced; split masks not materialized.

## 12. Metrics-policy evaluation

Candidate families defined but not computed: class balance / prevalence; directional classification; regression error; rank / correlation; calibration; cost-aware descriptive; train/validation stability. No PnL / backtest / strategy metrics. Phase 4bm-Z computes none.

## 13. Leakage-controls evaluation

`src_ne_feature_ts = 0`; no future data in features; no boundary-crossing labels in earlier splits; no test-driven decisions; no post-hoc test-based horizon selection; train-only transform fitting; no validation/test-diagnostic-driven feature engineering unless separately authorized; no manifest mutation as governance substitute; censored rows treated as label-unavailable per horizon. Explicit and enforceable.

## 14. Baseline-model-family evaluation

Majority / persistence / naive direction; logistic regression; regularized linear; calibrated tree ensembles; shallow gradient boosting; simple probabilistic references. No deep learning unless a later memo justifies it. No family selected, implemented, or trained.

## 15. Sample-weighting / class-imbalance / calibration evaluation

Sample weighting; class imbalance (incl. exact-zero mass); per-horizon censoring masking; calibration requirement; validation-only calibration; test-holdout calibration-leakage avoidance — all explicitly identified as questions for a future phase; none answered here.

## 16. Cost-aware evaluation

§11.6 = 8 bps per side / 16 bps round trip restated as a locked, non-loosenable constraint; signal horizon vs. transaction-cost commensurability (esp. 1s / 5s); latency sensitivity; slippage / spread caveats (no order-book depth in v002). No strategy design, no PnL simulation, no backtests.

## 17. Future ML-baseline implementation prerequisites

Future ML-baseline implementation scoping/design phase completed and merged; explicit allowed targets/horizons at design level only; explicit leakage controls accepted and operationalized; explicit metric policy accepted; explicit train/validation/test handling accepted (single-use holdout); explicit cost-aware descriptive policy at §11.6 lock; explicit non-use of test holdout for tuning/design; explicit local-output / gitignore storage policy; explicit test-suite and boundary requirements; no unresolved blocking caveat; retained verdicts and locks preserved.

## 18. Evidence reviewed

Phase 4bm-Y scoping memo / closeout / merge-closeout; Phase 4bm-X interpretation memo / closeout / merge-closeout (criteria A–M PASS); Phase 4bm-W diagnostics report / closeout / merge-closeout (33 passed; `DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS`); Phase 4bm-V / U / T / S / R / Q / P reports and closeouts; `merge-closeout-standard.md`; `phase-risk-tiering-standard.md`; Phase 4bm-A-P1 and Phase 4bm-D-P1 standards; `current-project-state.md`. All local diagnostic outputs and predecessor artefacts re-hashed read-only — all MATCH.

## 19. Required exact phrases

- Phase 4bm-Z is a docs-only ML-readiness evaluation memo.
- Phase 4bm-Z does not train ML models.
- Phase 4bm-Z does not run ML.
- Phase 4bm-Z does not score models.
- Phase 4bm-Z does not generate predictions.
- Phase 4bm-Z does not select models.
- Phase 4bm-Z does not rank or select features.
- Phase 4bm-Z does not tune hyperparameters.
- Phase 4bm-Z does not tune thresholds.
- Phase 4bm-Z does not define or run strategy.
- Phase 4bm-Z does not generate signals.
- Phase 4bm-Z does not simulate PnL.
- Phase 4bm-Z does not run backtests.
- Phase 4bm-Z does not authorize acquisition.
- Phase 4bm-Z does not authorize research execution.
- Phase 4bm-Z does not create ML artefacts.
- Phase 4bm-Z does not create diagnostic artefacts.
- Phase 4bm-Z does not create split masks.
- Phase 4bm-Z does not use the test holdout for tuning or design.
- Phase 4bm-Z does not mutate any manifest.
- Phase 4bm-Z does not mutate any successor-state artefact.
- Phase 4bm-Z does not commit data/microstructure.
- Phase 4bm-Z does not commit data/research.
- Any ML-baseline implementation requires a separately authorized implementation phase.
- Phase 4bn-A is not authorized by Phase 4bm-Z.
- Recommended state remains paused.

## 20. Boundary confirmations

- No diagnostics rerun; no diagnostic artefact created.
- No ML artefact created; no split mask materialized.
- No model training / scoring / prediction generation / feature selection / model selection / feature ranking / hyperparameter tuning / threshold tuning / strategy / signal / PnL / backtest / walk-forward.
- No manifest mutated (v002 label `5e17074d…` / feature `512a0a54…` byte-identical pre/post; re-hash MATCH).
- No successor-state artefact mutated (Phase 4bm-S `081730006c…`, Phase 4bm-U `6834ab11…` byte-identical pre/post; re-hash MATCH).
- No Phase 4bm-Q gate report mutated (`8a360608…` byte-identical pre/post; re-hash MATCH).
- Phase 4bm-W diagnostic outputs unchanged and gitignored (summary `f4b825af…`, summary sidecar `ff52873c…`, manifest `ac10061d…`, manifest sidecar `644506e3…`; re-hash MATCH; `.gitignore:88: data/research/`).
- No `data/microstructure/` artefact created, staged, or committed; no `data/research/` artefact created, staged, or committed.
- Test holdout not used for tuning or design.
- No acquisition; no research execution; no endpoint / WebSocket; no credentials; no `.env`; no `.mcp.json`; no MCP; no Graphify.
- Phase 4aw `flip_research_eligible` always-raises invariant preserved (never invoked).

## 21. Retained verdicts preserved

H0, R3, R1a, R1b-narrow, R2, F1, D1-A, 5m thread, V2, G1, C1 — all preserved verbatim. All prior phase results (Phase 4am .. Phase 4bm-Y) preserved verbatim.

## 22. Project locks preserved

§11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 (0.25% / 2× / one-position / mark-price stops); Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6/§7/§8; Phase 4j §11; Phase 4k/4p/4q/4v/4w; Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy; Phase 4aw `flip_research_eligible(...)` always-raises invariant (never invoked); Phase 4bb-F canonical sidecar / path policy; Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks; Phase 4bm-A-P1 thin-prompt context-management standard; Phase 4bm-D-P1 lightweight Claude Code workspace standard — all preserved verbatim.

## 23. Recommended state

**Remain paused.** Branch-complete only; not merged; not project-complete. A separately authorized Tier 1 merge phase is required for project completion. The evaluation decision `RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION_SCOPING` authorizes nothing. **Any ML-baseline implementation requires a separately authorized implementation phase.** **Phase 4bn-A is not authorized by Phase 4bm-Z.** **Recommended state remains paused.**
