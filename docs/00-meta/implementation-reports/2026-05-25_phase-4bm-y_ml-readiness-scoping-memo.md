# Phase 4bm-Y — Multi-Day V002 ML-Readiness Scoping Memo

**Phase identity:** Phase 4bm-Y — Multi-Day V002 ML-Readiness Scoping Memo (docs-only governance / methodology scoping memo; the phase separately authorized by the Phase 4bm-X recommendation `RECOMMEND_AUTHORIZE_ML_READINESS_SCOPING_MEMO` that defines the scope, boundaries, criteria, and non-authorizations for any possible future ML-readiness *evaluation* work over the multi-day v002 feature/label family).
**Date:** 2026-05-25.
**Branch:** `phase-4bm-y/multi-day-v002-ml-readiness-scoping-memo`.
**Base SHA:** `main` at `6d149e19ad9574a0fc36f5bbe966e25b839aa036` (Phase 4bm-X merge-closeout SHA-finalization commit `docs(phase-4bm-x): finalize merge closeout shas`; pre-branch `main == origin/main` verified in sync).
**Tier:** **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3. This phase defines the scope, boundaries, and non-authorizations for any possible future ML-readiness evaluation work; it is adjacent to ML training, feature/model selection, threshold tuning, strategy research, backtests, acquisition, and research execution while explicitly authorizing none of them, so it escalates to Tier 1.
**Phase type:** docs-only governance / methodology scoping memo. Adds two new tracked docs files under `docs/00-meta/implementation-reports/` (this memo + the paired closeout) and narrowly updates `docs/00-meta/current-project-state.md`. **No** source / test / committed-script / configuration / manifest / sidecar / gate-report / successor-state mutation. **No** local data artefact created or mutated. **No** diagnostic rerun. **No** acquisition. **No** successor authorization.
**Status:** drafted; pending operator review. Branch-complete only by this work; not merged into `main`; not project-complete.

---

## 0. Required exact phrases

- **Phase 4bm-Y is a docs-only ML-readiness scoping memo.**
- **Phase 4bm-Y does not train ML models.**
- **Phase 4bm-Y does not run ML.**
- **Phase 4bm-Y does not select models.**
- **Phase 4bm-Y does not rank or select features.**
- **Phase 4bm-Y does not tune hyperparameters.**
- **Phase 4bm-Y does not tune thresholds.**
- **Phase 4bm-Y does not define or run strategy.**
- **Phase 4bm-Y does not generate signals.**
- **Phase 4bm-Y does not simulate PnL.**
- **Phase 4bm-Y does not run backtests.**
- **Phase 4bm-Y does not authorize acquisition.**
- **Phase 4bm-Y does not authorize research execution.**
- **Phase 4bm-Y does not create ML artefacts.**
- **Phase 4bm-Y does not create diagnostic artefacts.**
- **Phase 4bm-Y does not create split masks.**
- **Phase 4bm-Y does not use the test holdout for tuning or design.**
- **Phase 4bm-Y does not mutate any manifest.**
- **Phase 4bm-Y does not mutate any successor-state artefact.**
- **Phase 4bm-Y does not commit data/microstructure.**
- **Phase 4bm-Y does not commit data/research.**
- **Any ML-readiness evaluation requires a separately authorized memo phase.**
- **Phase 4bm-Z is not authorized by Phase 4bm-Y.**
- **Recommended state remains paused.**

---

## 1. Phase identity

Phase 4bm-Y answers a single governance question:

> Given that Phase 4bm-X recommends authorizing an ML-readiness scoping memo, what should a future ML-readiness evaluation be allowed to evaluate, what must remain forbidden, and what criteria would need to be satisfied before any future ML-baseline implementation phase could be proposed?

Phase 4bm-Y is **docs-only**. It defines the scope, boundaries, criteria, and non-authorizations for any possible future ML-readiness *evaluation* work over the multi-day v002 BTCUSDT feature/label family `microstructure_labels_aggtrades_v001 @ v002` (90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 rows; horizons 1s / 5s / 15s / 60s), under the Phase 4bm-U recorded chronological split policy `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`. It trains nothing, selects nothing, ranks nothing, tunes nothing, runs nothing, materializes no split mask, mutates no manifest or successor-state artefact, acquires no data, and authorizes no successor implementation. **Phase 4bm-Y is a docs-only ML-readiness scoping memo.** **This phase is not ML. This phase is not an ML-readiness evaluation. This phase is not strategy research. This phase is not backtesting. This phase is not feature/model/threshold selection. This phase is not acquisition. This phase is not research execution.**

- **Phase name:** Phase 4bm-Y — Multi-Day V002 ML-Readiness Scoping Memo.
- **Phase type:** docs-only governance / methodology scoping memo.
- **Branch:** `phase-4bm-y/multi-day-v002-ml-readiness-scoping-memo`.
- **Base SHA:** `main` at `6d149e19ad9574a0fc36f5bbe966e25b839aa036`.
- **Authorization:** explicit operator authorization for Phase 4bm-Y only.

## 2. Branch name

`phase-4bm-y/multi-day-v002-ml-readiness-scoping-memo`

## 3. Base SHA

`6d149e19ad9574a0fc36f5bbe966e25b839aa036` (Phase 4bm-X merge-closeout SHA-finalization commit, `docs(phase-4bm-x): finalize merge closeout shas`; the head of `main` at branch time; `main == origin/main` verified in sync). The Phase 4bm-X docs/branch-tip commit `199c8c8a840a9614d61f03c93d18df5364559bb4`, merge commit `70e13ebd9133684e6e8c1d24c2c52dec6c2dce2c`, and merge-closeout commit `837c605af616d3bb68ace7eea963e36478bad81d` are present on `main` immediately below this SHA-finalization commit (verified by `git log --oneline -16 --decorate`).

## 4. Predecessor chain

| Phase | Role | Status on `main` | Verdict / result |
| --- | --- | --- | --- |
| **Phase 4bm-Q** | Multi-day v002 label-family eligibility gate | merge-complete; SHA-finalized | `LABEL_GATE_PASS`; 60 / 60 PASS; report-level only |
| **Phase 4bm-R** | Multi-day v002 label-family research-use decision memo | merge-complete; SHA-finalized | `RECOMMEND_LABEL_RESEARCH_USE_AUTHORIZATION` |
| **Phase 4bm-S** | Multi-day v002 label-family research-use successor-state recording | merge-complete; SHA-finalized | `LABEL_FAMILY_RESEARCH_USE_APPROVED_IN_PRINCIPLE` |
| **Phase 4bm-T** | Multi-day v002 chronological split-policy memo | merge-complete; SHA-finalized | `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` (memo-level) |
| **Phase 4bm-U** | Multi-day v002 chronological split-policy successor-state recording | merge-complete; SHA-finalized | `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` (`split_policy_status = "recorded"`) |
| **Phase 4bm-V** | Multi-day v002 diagnostics readiness and scope memo | merge-complete; SHA-finalized | `RECOMMEND_AUTHORIZE_DESCRIPTIVE_DIAGNOSTICS_PHASE` |
| **Phase 4bm-W** | Multi-day v002 descriptive diagnostics execution | merge-complete; SHA-finalized | `DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS` (descriptive-only) |
| **Phase 4bm-X** | Multi-day v002 descriptive diagnostics interpretation memo | merge-complete; SHA-finalized | `RECOMMEND_AUTHORIZE_ML_READINESS_SCOPING_MEMO` |

Direct predecessors for this memo:

- **Phase 4bm-W** — the separately authorized execution of the descriptive / structural diagnostics over the multi-day v002 family. Verdict `DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS`: 0 blocking structural failures; 4 non-blocking caveats. Merge-complete, SHA-finalized, project-complete on `main`.
- **Phase 4bm-X** — interpreted the Phase 4bm-W verdict, found all thirteen ML-readiness scoping criteria A–M PASS on repo evidence, and recommended (but did not authorize) a future docs-only ML-readiness scoping memo (decision `RECOMMEND_AUTHORIZE_ML_READINESS_SCOPING_MEMO`). **This Phase 4bm-Y is that separately authorized scoping memo.**

Phase 4bm-X lifecycle SHAs (verified present on `main`): base SHA `e4067c08c88e6dd8354a15bc90e90aa55ddada39`; docs/branch-tip commit `199c8c8a840a9614d61f03c93d18df5364559bb4`; merge commit `70e13ebd9133684e6e8c1d24c2c52dec6c2dce2c`; merge-closeout commit `837c605af616d3bb68ace7eea963e36478bad81d`; SHA-finalization commit `6d149e19ad9574a0fc36f5bbe966e25b839aa036` (latest finalized `main` state and this phase's base).

The chain is internally consistent. Each phase preserves the upstream artefacts byte-identically. No verdict has been revised. No project lock has been loosened.

## 5. Evidence reviewed

### 5.1 Phase 4bm-X interpretation evidence (docs)

- Phase 4bm-X interpretation memo `2026-05-25_phase-4bm-x_descriptive-diagnostics-interpretation-memo.md` (interpretation decision `RECOMMEND_AUTHORIZE_ML_READINESS_SCOPING_MEMO`; criteria A–M all PASS; §19 pre-description of what a future scoping memo could evaluate).
- Phase 4bm-X closeout `2026-05-25_phase-4bm-x_closeout.md` and merge-closeout `2026-05-25_phase-4bm-x_merge-closeout.md`.

### 5.2 Phase 4bm-W execution evidence (docs)

- Phase 4bm-W implementation report `2026-05-25_phase-4bm-w_multi-day-v002-descriptive-diagnostics.md` (verdict `DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS`; eight diagnostic groups; split-policy application; embargo; censoring; distribution; alignment; missingness; holdout protection).
- Phase 4bm-W merge-closeout `2026-05-25_phase-4bm-w_merge-closeout.md` (accurate re-verified pytest count **33 passed**; upstream immutability table) and closeout `2026-05-25_phase-4bm-w_closeout.md`.

### 5.3 Predecessor governance / methodology evidence (docs)

- Phase 4bm-V readiness/scope memo, closeout, merge-closeout (allowed/forbidden diagnostics categories; split-policy/holdout constraints; local-output constraints).
- Phase 4bm-U chronological split-policy successor-state report, closeout, merge-closeout.
- Phase 4bm-T chronological split-policy memo, closeout, merge-closeout.
- Phase 4bm-S label-family research-use successor-state report, closeout, merge-closeout.
- Phase 4bm-R label-family research-use decision memo, closeout, merge-closeout.
- Phase 4bm-Q label-family eligibility-gate report, closeout, merge-closeout (60 / 60 PASS; report-level only).
- Phase 4bm-P multi-day v002 label artefact structural QA memo and merge-closeout (`LABEL_STRUCTURAL_QA_PASS`).

### 5.4 Governance / process artefacts reviewed

- `docs/00-meta/process/merge-closeout-standard.md` (Tier 1 merge-closeout ceremony — applies to a future, separately authorized merge phase, not to this branch work).
- `docs/00-meta/process/phase-risk-tiering-standard.md` (§3 escalation; reusable non-authorization blocks).
- `2026-05-17_phase-4bm-a-p1_context-management-standard.md` (thin-prompt context-management standard; honored).
- `2026-05-17_phase-4bm-d-p1_lightweight-claude-code-workspace-standard.md` (lightweight Claude Code workspace standard; honored).
- `docs/00-meta/current-project-state.md` (current-phase narrative and project locks).

### 5.5 Local-evidence verification (read-only)

The Phase 4bm-W local gitignored diagnostic outputs and all predecessor governed evidence artefacts were re-hashed read-only at the start of this phase and matched their expected values byte-for-byte. None was mutated; none was committed.

| Artefact | Expected SHA256 | Result |
| --- | --- | --- |
| `descriptive_diagnostics_summary.json` | `f4b825af2e81734007be06acac5083e2d4048b54b5650bc407d87a6fc246198a` | MATCH (gitignored `data/research/`) |
| `descriptive_diagnostics_summary.json.sha256` | `ff52873c983b55cc74a0639d17ea8b3d128cdbee9c77763cd11d2e71b3820473` | MATCH (gitignored `data/research/`) |
| `diagnostics_manifest.json` | `ac10061d2f0257002e094d578bcc6149b1a74ca28c604fd0d0a97e5c51c26e45` | MATCH (gitignored `data/research/`) |
| `diagnostics_manifest.json.sha256` | `644506e392db46da6d27fa46519cac327136b1a05e350e2d9b231c62fce517eb` | MATCH (gitignored `data/research/`) |
| Phase 4bm-U split-policy successor-state JSON | `6834ab11a5ac5d93b4d9f14d9b71ef3acb2a279bd8e3189fd22421598675fc9c` | MATCH |
| Phase 4bm-U split-policy successor-state sidecar | `fa9ae709add4541111e70cfc03d9126ac40f136ea2ce1aa1abe299d3412ac0b6` | MATCH |
| Phase 4bm-S research-use successor-state JSON | `081730006c11360692db0a99d59a0ed499f762ef4f86d6e29bdf3016550abfe7` | MATCH |
| Phase 4bm-S research-use successor-state sidecar | `05597fe4d568f5644ad9acc914f8a3b429bc7984cf7df3a2ac3f8c7935e02551` | MATCH |
| v002 label manifest | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` | MATCH |
| v002 label manifest sidecar | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` | MATCH |
| v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | MATCH |
| v002 feature manifest sidecar | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` | MATCH |
| Phase 4bm-Q gate report | `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` | MATCH |
| Phase 4bm-Q gate report sidecar | `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` | MATCH |

`git check-ignore -v` confirms the diagnostic outputs are covered by `.gitignore:88: data/research/` and the microstructure artefacts by `.gitignore:85: data/microstructure/`; neither the diagnostic outputs nor any `data/microstructure/` artefact appears as a staged or committed change. This memo reads all evidence read-only and reruns nothing.

## 6. Phase 4bm-X decision

`RECOMMEND_AUTHORIZE_ML_READINESS_SCOPING_MEMO` (Phase 4bm-X).

This recommended only that a future, separately authorized, docs-only ML-readiness scoping memo *may* be proposed. The present Phase 4bm-Y is the separately authorized realization of that recommendation. Phase 4bm-X authorized no ML, no training, no selection, no tuning, no strategy, no backtests, no acquisition, and no research execution; it explicitly stated `Phase 4bm-Y is not authorized by Phase 4bm-X`, and the present phase exists solely because the operator separately authorized it.

## 7. Phase 4bm-W diagnostic verdict

`DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS` (Phase 4bm-W).

This verdict is **descriptive-only**. It is **not** an ML-readiness, strategy-readiness, or backtest-readiness signal. Phase 4bm-Y does not change, re-derive, or re-issue this verdict; it carries it forward as the evidential baseline for scoping.

- **0 blocking structural failures.** Every structural and alignment violation counter in the Phase 4bm-W summary aggregates to zero.
- **4 non-blocking caveats**, all understood and bounded, each carried forward in §13/§17 as an explicit stated constraint:
  1. **Envelope-terminal censoring asymmetry** — 857 censored rows total (`{1s:14, 5s:39, 15s:170, 60s:634}`), all on the final envelope day (2025-02-28) which lands entirely inside the test / final holdout; train and validation have zero censored rows.
  2. **538 embargo-excluded earlier-split rows** — train 248, validation 290, test 0; per-row masks only; the 90 v002 label parquets are never rewritten.
  3. **Approximate-quantile method** — fixed-width histogram (range ±0.02, bin width 1e-05); exact additive moments (mean / std / min / max) are *not* approximate.
  4. **`diagnostics_authorized=false` historical manifest flag** — predates Phase 4bm-W; authorization derives from the operator prompt, not from manifest mutation; manifests left byte-identical.

## 8. Scope of future ML-readiness evaluation

A future, separately authorized **docs-only ML-readiness *evaluation* memo** (provisionally a "Phase 4bm-Z"-class phase, **not** authorized here) would be the *next* governance step after this scoping memo — and would itself remain docs-only, training nothing and running nothing. Its scope, as bounded by this memo, would be to *answer at memo/governance level* the admissibility questions enumerated in §9–§18 and to decide whether any later **ML-baseline implementation** phase may be *proposed*. The ordering is strict and one-way:

```text
Phase 4bm-Y (this memo: ML-READINESS SCOPING — defines the questions and boundaries)
   → Phase 4bm-Z-class (future, separately authorized: ML-READINESS EVALUATION MEMO — answers the questions, still docs-only)
      → (only then, if and only if separately authorized) ML-BASELINE IMPLEMENTATION phase
```

This memo defines the *questions* a future evaluation memo must answer and the *boundaries* it must not cross. It does **not** answer those questions, does **not** select any target/horizon, does **not** declare any horizon ML-ready, and does **not** authorize the evaluation memo. **Any ML-readiness evaluation requires a separately authorized memo phase.**

## 9. Admissible supervised-learning task-framing questions

A future ML-readiness evaluation memo may consider, at memo/governance level only and **without training, selecting, ranking, tuning, or running anything**:

- **Classification vs. regression vs. ordinal framing** — whether the target should be framed as directional classification (sign of forward return), magnitude regression (forward log-return), or ordinal/binned framing; the trade-offs of each at scoping level only.
- **Horizon-specific vs. multi-horizon framing** — whether each horizon (1s / 5s / 15s / 60s) is framed as an independent task, or whether a shared representation is considered only at a later, separately authorized stage.
- **Direction-only vs. magnitude-aware targets** — whether `forward_direction_H ∈ {-1, 0, +1}` is the target, or whether the continuous forward return is the target; how the exact-zero-return mass (large at short horizons) is treated.
- **Censored-row handling per horizon** — whether censored rows must be excluded per horizon (treated as label-unavailable, never as a class or a zero), given the envelope-terminal censoring asymmetry concentrated in the test split.
- **Horizon admissibility scope** — whether all horizons may be evaluated, or whether any horizon should be deferred at evaluation-memo level (e.g., latency-sensitive horizons).
- **Per-horizon-independent vs. shared-representation** — whether the task should be per-horizon independent for any future baseline, with shared representation considered only at a strictly later separately authorized stage.

These are *questions to be answered later*, not decisions made here. Phase 4bm-Y selects no framing.

## 10. Target / horizon admissibility questions

Each horizon must be discussed **separately**. This memo does **not** declare any horizon ML-ready; it defines what evidence a future evaluation memo would need to evaluate each horizon.

- **1s horizon** — must include explicit latency/tradability caveats at scoping level: at a 1-second forward horizon, signal-to-execution latency, order placement, fill latency, and the 16 bps round-trip cost (§16) dominate; a future evaluation memo must require that any later baseline framing for 1s explicitly account for whether the horizon is operationally realizable at all before it could be considered.
- **5s horizon** — must also include latency/tradability caveats: less extreme than 1s, but still latency-sensitive; the future evaluation memo must require the same latency/cost-realizability discussion.
- **15s horizon** — may be described as operationally *less* latency-sensitive than 1s/5s, but **still not strategy-ready**; a future evaluation memo would define what evidence would be needed to evaluate it.
- **60s horizon** — may be described as operationally *least* latency-sensitive of the four, but **still not strategy-ready**; censoring concentration is largest at 60s (634 of 857 censored rows) and is entirely in the test split, so a future evaluation memo must define horizon-availability-by-split as a constraint for 60s in particular.

For every horizon: the future evaluation memo **may define what evidence would be required to evaluate that horizon later**, and **must not declare any horizon ML-ready**. Phase 4bm-Y declares no horizon ML-ready and selects no horizon.

## 11. Train / validation / test usage rules

The Phase 4bm-U policy `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` governs all future ML-readiness evaluation and any later implementation:

| Split | UTC dates (inclusive) | Partitions | Rows (observed, Phase 4bm-W) |
| --- | --- | --- | --- |
| Train | 2024-12-01 .. 2025-01-14 | 45 | 74,535,688 |
| Validation | 2025-01-15 .. 2025-02-13 | 30 | 56,819,939 |
| Test / final holdout | 2025-02-14 .. 2025-02-28 | 15 | 23,797,822 |
| **Total** | 2024-12-01 .. 2025-02-28 | **90** | **155,153,449** |

Binding usage rules a future evaluation memo must restate and enforce:

- **Train and validation** may be used **only in future, separately authorized evaluation phases** — never in this scoping memo.
- **Test / final holdout remains single-use** and may **not** be used for feature selection, model selection, hyperparameter selection, threshold tuning, strategy design, diagnostic iteration, eligibility rescue, or any tuning/design loop.
- **No test-holdout tuning/design.**
- **No shuffled cross-validation.** **No random split.** **No bootstrap split.** **No k-fold-over-time.** **No post-hoc temporal resampling.**
- Rows assigned by `source_transact_time_ms` UTC date.
- **Boundary embargo and boundary-crossing exclusion must be enforced** — minimum 60-second embargo at train/validation (`T_TV = 2025-01-15T00:00:00Z`) and validation/test (`T_VT = 2025-02-14T00:00:00Z`) boundaries; boundary-crossing rows excluded from the earlier split; never reassigned forward; per-row masks only (no parquet rewrite).
- **Split masks must not be materialized for future use unless separately authorized.** Phase 4bm-Y creates no split mask.

## 12. Metrics allowed at scoping level

This phase may define candidate metric families that a future evaluation memo could consider, but **must not compute any of them**. Permitted candidate metric families (definition only, no computation):

- **Class balance / prevalence metrics** — directional class prevalence per split×horizon (descriptive only).
- **Directional classification metrics** — accuracy, balanced accuracy, precision/recall, F1, ROC-AUC, PR-AUC, MCC (as *candidate* families a future memo may select among).
- **Regression error metrics** — MAE, RMSE, MAPE-style error on forward returns (candidate families).
- **Rank / correlation metrics** — Spearman / Kendall rank correlation, information coefficient (candidate families).
- **Calibration metrics** — reliability diagrams, Brier score, expected calibration error (candidate families).
- **Cost-aware descriptive metrics** — return-net-of-cost descriptive summaries at the §16 cost level, *descriptive only* (candidate families).
- **Stability metrics across train/validation only** — distribution / metric stability between train and validation, never touching the test holdout (candidate families).

Explicitly **excluded** at every level: **no PnL metrics; no backtest metrics; no strategy metrics.** Phase 4bm-Y computes no metric of any kind.

## 13. Leakage controls

A future evaluation memo must adopt and enforce these leakage controls (carried forward from Phase 4bm-W/X evidence):

- **Feature timestamp must be at or before label start** — Phase 4bm-W confirmed `source_transact_time_ms == feature_timestamp_ms` for every row (`src_ne_feature_ts = 0`); features are not constructed from future data.
- **No future data in features.**
- **No boundary-crossing labels in earlier splits** — enforced by the 60-second embargo (538 earlier-split rows excluded; test 0).
- **No test-driven feature/model/threshold decisions.**
- **No post-hoc horizon selection based on test.**
- **No fitting scalers / imputers / encoders on validation or test** — any such transforms a future baseline might use must be fit on train only.
- **No feature engineering based on validation/test diagnostics** unless separately authorized and documented.
- **No manifest mutation as a substitute for governance authorization** — authorization is operator-prompt-driven and recorded in docs/successor-state; the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved.
- **Censored rows treated as label-unavailable** per horizon (never a class, never a zero), carrying forward the envelope-terminal censoring caveat.

## 14. Baseline model families that may be considered later without training

A future evaluation memo **may list** model families to consider in a later, separately authorized implementation phase, but **must not implement or train them**. Candidate families (named for future consideration only):

- **Majority / persistence / naive direction baselines** — the mandatory reference floor any later baseline must beat.
- **Logistic regression** (directional framing).
- **Regularized linear models** (L1 / L2 / elastic-net for regression or classification framing).
- **Calibrated tree ensembles** (e.g., random forests with calibration).
- **Shallow gradient boosting** (depth-limited).
- **Simple probabilistic baselines** (e.g., class-prior / kernel-density references).

**No deep learning** unless a later memo explicitly justifies it. **No model family may be selected in Phase 4bm-Y.** Phase 4bm-Y names families for *future consideration only* and selects, implements, and trains none.

## 15. Sample-weighting / class-imbalance / calibration policy questions

A future evaluation memo must answer (at memo level only):

- **Sample weighting** — whether class imbalance or per-row importance requires sample weighting, and if so what weighting scheme, decided at memo level before any implementation.
- **Class imbalance** — whether the directional class distribution (including the large exact-zero mass at short horizons) requires weighting, resampling discipline (train-only), or threshold-free metric choices.
- **Per-horizon censoring masking** — whether per-horizon censoring requires masking (treating censored rows as label-unavailable per horizon), given the envelope-terminal asymmetry.
- **Calibration requirement** — whether calibration should be *required* for any probability outputs a later baseline might produce.
- **Validation-only calibration** — whether calibration is allowed to be fit on validation only (never test), and how to document it.
- **Test-holdout calibration leakage** — how to avoid test-holdout calibration leakage (the test holdout must never be used to fit or tune calibration).

Phase 4bm-Y answers none of these; it only requires that a future evaluation memo answer them before any implementation could be proposed.

## 16. Cost-aware evaluation questions, without strategy or backtesting

A future evaluation memo may define that future evaluation should account for cost realism **without designing strategy, simulating PnL, or running backtests**:

- **§11.6 cost lock** — 8 bps per side / 16 bps round trip; any cost-aware descriptive evaluation must use this locked cost level and may not loosen it.
- **Signal horizon vs. transaction costs** — whether the descriptive return distribution at a given horizon is even commensurate with 16 bps round-trip cost (especially the 1s / 5s horizons).
- **Latency sensitivity** — explicit treatment of latency sensitivity, especially at 1s and 5s.
- **Slippage and spread caveats** — descriptive caveats on slippage and spread, noting that the v002 family does not contain order-book depth.
- **Boundary** — these are *cost-aware descriptive evaluation questions only*. A future evaluation memo **must not** design strategy, generate signals, simulate PnL, or run backtests; cost-awareness at evaluation level is descriptive, not a strategy or backtest.

## 17. Explicitly forbidden activities

The following are forbidden in **this** phase and, where stated, in any future ML-readiness *evaluation* memo (which would also remain docs-only):

- training any ML model; running any ML; scoring or evaluating predictions;
- selecting any model; ranking or selecting features; tuning hyperparameters; tuning thresholds; meta-labeling;
- defining or running strategy; generating signals; simulating PnL; running backtests; running walk-forward optimization;
- using the test holdout for tuning or design; eligibility rescue; post-hoc horizon selection based on test;
- materializing split masks for future use (Phase 4bm-Y creates none);
- creating ML artefacts; creating diagnostic artefacts; rerunning Phase 4bm-W diagnostics;
- mutating any manifest, the Phase 4bm-S successor-state artefact, the Phase 4bm-U successor-state artefact, the Phase 4bm-Q gate report, or any other `data/microstructure/` or `data/research/` artefact;
- changing `chronological_split_policy`, `research_eligible`, `eligibility_gate_status`, `diagnostics_authorized`, or `ml_authorized` on any on-disk manifest;
- acquiring data (no additional days / symbols / data families beyond the locked 90-day v002 envelope; no mark-price / order-book / funding / OI / liquidation / cross-venue / additional aggTrades);
- research execution; any public / authenticated / private endpoint call; any WebSocket / user-stream; any credential / `.env` / `.mcp.json` / MCP / Graphify use;
- committing `data/microstructure` or `data/research`.

## 18. Future ML-readiness evaluation prerequisites

Before any later **ML-baseline implementation** phase may be *proposed*, all of the following must be true:

- a **future ML-readiness evaluation memo completed and merged** (separately authorized; docs-only; the Phase 4bm-Z-class step);
- **explicit allowed targets/horizons selected at memo level only** (which of 1s / 5s / 15s / 60s; direction vs. magnitude framing) — chosen in the evaluation memo, never in this scoping memo;
- **explicit leakage controls accepted** (§13);
- **explicit metric policy accepted** (§12);
- **explicit train/validation/test handling accepted** (§11), including single-use holdout protection;
- **explicit cost-aware evaluation policy accepted** (§16);
- **explicit non-use of the test holdout for tuning/design** confirmed;
- **no unresolved blocking caveat** (the four Phase 4bm-W caveats remain understood, bounded, non-blocking, and carried forward as constraints);
- **retained verdicts and project locks preserved** (§25–§26).

A future ML-baseline implementation phase would, in addition, require its own separately authorized operator prompt, its own branch, its own implementation report + closeout, and (separately) a Tier 1 merge-closeout. None of this is authorized by Phase 4bm-Y.

## 19. Decision

`RECOMMEND_AUTHORIZE_ML_READINESS_EVALUATION_MEMO`.

## 20. Rationale for the chosen decision

Phase 4bm-X found all thirteen ML-readiness scoping criteria A–M PASS on current repo evidence, and recommended this scoping memo. This Phase 4bm-Y has now defined the full scope, boundaries, criteria, and non-authorizations for any possible future ML-readiness *evaluation* (§8–§18) without performing, selecting, ranking, tuning, or running anything:

- The Phase 4bm-W diagnostics passed with **0 blocking structural failures** and **4 fully characterized, non-blocking caveats** (§7) that require no remediation before an evaluation memo, only carry-forward as stated constraints.
- The Phase 4bm-U split policy is leakage-correct and can govern future evaluation; the test holdout was protected; feature/label alignment is strict 1:1 across all 90 days; label availability/censoring is understood; distributions reveal no structural impossibility; missingness/value-domain checks all passed (carried forward from Phase 4bm-W/X).
- The local diagnostic outputs and all predecessor artefacts re-hash to their recorded SHAs (§5.5); no manifest or successor-state artefact was mutated; no ML / strategy / backtest work has been authorized or run; all retained verdicts and project locks are preserved verbatim (§25–§26).

Because the descriptive diagnostics passed with only understood, non-blocking caveats, and because an ML-readiness *evaluation* memo is itself a docs-only governance artefact that trains nothing, selects nothing, tunes nothing, and runs nothing, the appropriate recommendation is to authorize — separately and in a future phase — a docs-only ML-readiness evaluation memo only, bounded by §8–§18. No prerequisite is missing and no drift was detected, so neither `DEFER_ML_READINESS_EVALUATION_PENDING_SPECIFIC_REMEDIATION` nor `DO_NOT_RECOMMEND_ML_READINESS_EVALUATION` is warranted. The recommendation is a *recommendation only*; it does not itself authorize any evaluation memo, any ML, or any execution.

**`RECOMMEND_AUTHORIZE_ML_READINESS_EVALUATION_MEMO` means only:** a future, separately authorized, docs-only memo may *evaluate* (at memo/governance level) the admissibility questions this scoping memo defines, and decide whether a later ML-baseline implementation phase may be *proposed*. It does **not** mean ML is authorized, model training is authorized, feature selection is authorized, model selection is authorized, hyperparameter tuning is authorized, threshold tuning is authorized, strategy research is authorized, backtests are authorized, acquisition is authorized, or research execution is authorized.

## 21. What a future ML-readiness evaluation memo would be allowed to evaluate, if separately authorized

A future, separately authorized **docs-only ML-readiness evaluation memo** (provisionally a "Phase 4bm-Z"-class phase, **not** authorized here) would be permitted to evaluate, at memo / governance level only:

- the admissible supervised-learning task-framing questions (§9);
- target / horizon admissibility per horizon, including the 1s/5s latency caveats and the 15s/60s less-latency-sensitive-but-not-strategy-ready framing (§10);
- train / validation / test usage rules, restating the Phase 4bm-U policy and single-use holdout protection (§11);
- the metric families allowed at scoping level, *without computing them* (§12);
- the leakage controls to be enforced (§13);
- the baseline model families to consider later *without training them* (§14);
- sample-weighting / class-imbalance / calibration policy questions (§15);
- cost-aware evaluation questions *without strategy or backtesting* (§16);
- whether a later ML-baseline implementation phase may be *proposed* (§18).

A future ML-readiness evaluation memo **must not**: train any model; run any ML; select any model; select or rank features; tune hyperparameters; tune thresholds; design strategy; generate signals; simulate PnL; run backtests; run walk-forward optimization; use the test holdout for tuning/design; materialize split masks; mutate manifests or successor states; or acquire data. It would carry forward the four Phase 4bm-W caveats (§7) as explicit stated constraints, and would require its own separately authorized operator prompt, its own branch, its own implementation report + closeout, and (separately) a Tier 1 merge-closeout. **Any ML-readiness evaluation requires a separately authorized memo phase.**

## 22. What this phase does not authorize

Phase 4bm-Y defines an ML-readiness scoping and a single governance recommendation only. It does **not**, and **cannot**, authorize:

- any ML-readiness evaluation memo (it only *recommends* that one may be separately authorized); any diagnostics rerun; any new diagnostic artefact; any ML artefact; any split-mask materialization;
- any ML training / model selection / feature ranking / feature selection / hyperparameter selection / threshold tuning / meta-labeling; any strategy specification / implementation / signal construction; any PnL simulation / backtest / walk-forward optimization;
- any use of the test window for tuning or design; any eligibility rescue;
- any mutation of any manifest, the Phase 4bm-S successor-state artefact, the Phase 4bm-U successor-state artefact, the Phase 4bm-Q gate report, or any other `data/microstructure/` or `data/research/` artefact;
- any change to `chronological_split_policy`, `research_eligible`, `eligibility_gate_status`, `diagnostics_authorized`, or `ml_authorized` on any on-disk manifest;
- any data acquisition (no additional days / symbols / data families beyond the locked 90-day v002 envelope; no mark-price / order-book / funding / OI / liquidation / cross-venue / additional aggTrades);
- any public / authenticated / private endpoint call; any WebSocket / user-stream; any credential / `.env` / `.mcp.json` / MCP / Graphify use;
- Phase 4bm-Z or any successor phase; Phase 5; Phase 4 canonical; paper / shadow; live-readiness; deployment; exchange-write; production-key creation;
- any revision of a retained verdict, any loosening of a project lock, or any amendment of M0 / Phase 4al / Phase 4aw / Phase 4bb-F / Phase 4bl-F / Phase 4bm-A-P1 / Phase 4bm-D-P1.

**Phase 4bm-Y is a docs-only ML-readiness scoping memo.** **Phase 4bm-Y does not train ML models.** **Phase 4bm-Y does not run ML.** **Phase 4bm-Y does not select models.** **Phase 4bm-Y does not rank or select features.** **Phase 4bm-Y does not tune hyperparameters.** **Phase 4bm-Y does not tune thresholds.** **Phase 4bm-Y does not define or run strategy.** **Phase 4bm-Y does not generate signals.** **Phase 4bm-Y does not simulate PnL.** **Phase 4bm-Y does not run backtests.** **Phase 4bm-Y does not authorize acquisition.** **Phase 4bm-Y does not authorize research execution.** **Phase 4bm-Y does not create ML artefacts.** **Phase 4bm-Y does not create diagnostic artefacts.** **Phase 4bm-Y does not create split masks.** **Phase 4bm-Y does not use the test holdout for tuning or design.** **Phase 4bm-Y does not mutate any manifest.** **Phase 4bm-Y does not mutate any successor-state artefact.** **Phase 4bm-Y does not commit data/microstructure.** **Phase 4bm-Y does not commit data/research.** **Any ML-readiness evaluation requires a separately authorized memo phase.** **Phase 4bm-Z is not authorized by Phase 4bm-Y.**

## 23. (reserved — see §21)

This section intentionally consolidated into §21 ("What a future ML-readiness evaluation memo would be allowed to evaluate, if separately authorized") to avoid duplication.

## 24. (reserved — see §22)

This section intentionally consolidated into §22 ("What this phase does not authorize").

## 25. Retained verdicts preserved

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

All prior phase results (Phase 4am .. Phase 4bm-X) preserved verbatim.

## 26. Project locks preserved

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
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (never invoked by Phase 4bm-Y)
- Phase 4bb-F canonical sidecar / path policy
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks
- Phase 4bm-A-P1 thin-prompt context-management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace standard

## 27. Recommended next state

**Remain paused.** Phase 4bm-Y is branch-complete only by this work. Per the Phase 4bk-A workflow standard, it is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1). The scoping decision is `RECOMMEND_AUTHORIZE_ML_READINESS_EVALUATION_MEMO`; this is a recommendation only and authorizes nothing. **Any ML-readiness evaluation requires a separately authorized memo phase.** **Phase 4bm-Z is not authorized by Phase 4bm-Y.** **Recommended state remains paused.**
