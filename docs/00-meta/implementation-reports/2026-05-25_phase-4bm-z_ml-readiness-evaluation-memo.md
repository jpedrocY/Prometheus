# Phase 4bm-Z — Multi-Day V002 ML-Readiness Evaluation Memo

**Phase identity:** Phase 4bm-Z — Multi-Day V002 ML-Readiness Evaluation Memo (docs-only governance / methodology evaluation memo; the phase separately authorized by the Phase 4bm-Y recommendation `RECOMMEND_AUTHORIZE_ML_READINESS_EVALUATION_MEMO`, which scoped the admissible questions and boundaries for any possible ML-readiness *evaluation* over the multi-day v002 feature/label family).
**Date:** 2026-05-25.
**Branch:** `phase-4bm-z/multi-day-v002-ml-readiness-evaluation-memo`.
**Base SHA:** `main` at `2463ceb716d31c79ef766e9042fd40a3929f3e5c` (Phase 4bm-Y merge-closeout SHA-finalization commit `docs(phase-4bm-y): finalize merge closeout shas`; pre-branch `main == origin/main` verified in sync).
**Tier:** **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3. This phase evaluates whether a later ML-baseline implementation phase may be proposed; it is adjacent to ML training, feature/model selection, threshold tuning, strategy research, backtests, acquisition, and research execution while explicitly authorizing none of them, so it escalates to Tier 1.
**Phase type:** docs-only governance / methodology evaluation memo. Adds two new tracked docs files under `docs/00-meta/implementation-reports/` (this memo + the paired closeout) and narrowly updates `docs/00-meta/current-project-state.md`. **No** source / test / committed-script / configuration / manifest / sidecar / gate-report / successor-state mutation. **No** local data artefact created or mutated. **No** diagnostic rerun. **No** acquisition. **No** successor authorization.
**Status:** drafted; pending operator review. Branch-complete only by this work; not merged into `main`; not project-complete.

---

## 0. Required exact phrases

- **Phase 4bm-Z is a docs-only ML-readiness evaluation memo.**
- **Phase 4bm-Z does not train ML models.**
- **Phase 4bm-Z does not run ML.**
- **Phase 4bm-Z does not score models.**
- **Phase 4bm-Z does not generate predictions.**
- **Phase 4bm-Z does not select models.**
- **Phase 4bm-Z does not rank or select features.**
- **Phase 4bm-Z does not tune hyperparameters.**
- **Phase 4bm-Z does not tune thresholds.**
- **Phase 4bm-Z does not define or run strategy.**
- **Phase 4bm-Z does not generate signals.**
- **Phase 4bm-Z does not simulate PnL.**
- **Phase 4bm-Z does not run backtests.**
- **Phase 4bm-Z does not authorize acquisition.**
- **Phase 4bm-Z does not authorize research execution.**
- **Phase 4bm-Z does not create ML artefacts.**
- **Phase 4bm-Z does not create diagnostic artefacts.**
- **Phase 4bm-Z does not create split masks.**
- **Phase 4bm-Z does not use the test holdout for tuning or design.**
- **Phase 4bm-Z does not mutate any manifest.**
- **Phase 4bm-Z does not mutate any successor-state artefact.**
- **Phase 4bm-Z does not commit data/microstructure.**
- **Phase 4bm-Z does not commit data/research.**
- **Any ML-baseline implementation requires a separately authorized implementation phase.**
- **Phase 4bn-A is not authorized by Phase 4bm-Z.**
- **Recommended state remains paused.**

> **Successor-naming note.** The repository's active microstructure-thread phase letter-series ran `…4bm-Q, 4bm-R, 4bm-S, 4bm-T, 4bm-U, 4bm-V, 4bm-W, 4bm-X, 4bm-Y, 4bm-Z`. `Z` is the terminal letter of the `4bm-` series, so by the repo's established convention the next letter-series is `4bn-A` (the Phase 4bm-Y and Phase 4bm-X memos both already enumerate `Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-*` as unauthorized successors). This memo therefore uses **`Phase 4bn-A`** as the next-phase name in the required exact phrases. No successor is authorized by this phase under any name.

---

## 1. Phase identity

Phase 4bm-Z answers a single governance question:

> Given that Phase 4bm-Y scoped the admissible questions and boundaries for ML-readiness evaluation, do current repo evidence, diagnostics, split policy, leakage controls, cost constraints, and horizon-specific constraints support proposing a future ML-baseline implementation phase, and under what restrictions?

Phase 4bm-Z is **docs-only**. It *evaluates*, at memo / governance level only, the admissibility questions defined by the Phase 4bm-Y scoping memo (§9–§18 of that memo) over the multi-day v002 BTCUSDT feature/label family `microstructure_labels_aggtrades_v001 @ v002` (90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 rows; horizons 1s / 5s / 15s / 60s), under the Phase 4bm-U recorded chronological split policy `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`. It trains nothing, scores nothing, predicts nothing, selects nothing, ranks nothing, tunes nothing, runs nothing, materializes no split mask, mutates no manifest or successor-state artefact, acquires no data, and authorizes no successor implementation. **Phase 4bm-Z is a docs-only ML-readiness evaluation memo.** **This phase is not ML. This phase is not an ML-baseline implementation. This phase is not strategy research. This phase is not backtesting. This phase is not feature/model/threshold selection. This phase is not acquisition. This phase is not research execution.**

- **Phase name:** Phase 4bm-Z — Multi-Day V002 ML-Readiness Evaluation Memo.
- **Phase type:** docs-only governance / methodology evaluation memo.
- **Branch:** `phase-4bm-z/multi-day-v002-ml-readiness-evaluation-memo`.
- **Base SHA:** `main` at `2463ceb716d31c79ef766e9042fd40a3929f3e5c`.
- **Authorization:** explicit operator authorization for Phase 4bm-Z only.

## 2. Branch name

`phase-4bm-z/multi-day-v002-ml-readiness-evaluation-memo`

## 3. Base SHA

`2463ceb716d31c79ef766e9042fd40a3929f3e5c` (Phase 4bm-Y merge-closeout SHA-finalization commit, `docs(phase-4bm-y): finalize merge closeout shas`; the head of `main` at branch time; `main == origin/main` verified in sync). The Phase 4bm-Y docs/branch-tip commit `03468a453828fa8dc8b67f62c729e85761bece9d`, merge commit `5c86c4df9459d1cf854f1c72b2677605745b0e85`, and merge-closeout commit `9d90e6aefea82ccbb7d08fb2647985f73c9e6b71` are present on `main` immediately below this SHA-finalization commit (verified by `git log --oneline -16 --decorate`).

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
| **Phase 4bm-Y** | Multi-day v002 ML-readiness scoping memo | merge-complete; SHA-finalized | `RECOMMEND_AUTHORIZE_ML_READINESS_EVALUATION_MEMO` |

Direct predecessors for this memo:

- **Phase 4bm-W** — the separately authorized execution of the descriptive / structural diagnostics over the multi-day v002 family. Verdict `DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS`: 0 blocking structural failures; 4 non-blocking caveats. Merge-complete, SHA-finalized, project-complete on `main`.
- **Phase 4bm-X** — interpreted the Phase 4bm-W verdict, found all thirteen ML-readiness scoping criteria A–M PASS on repo evidence, and recommended (but did not authorize) a future docs-only ML-readiness scoping memo (decision `RECOMMEND_AUTHORIZE_ML_READINESS_SCOPING_MEMO`).
- **Phase 4bm-Y** — defined the full scope, boundaries, criteria, and non-authorizations for any possible future ML-readiness *evaluation* (its §8–§18) and recommended (but did not authorize) a future docs-only ML-readiness evaluation memo (decision `RECOMMEND_AUTHORIZE_ML_READINESS_EVALUATION_MEMO`). **This Phase 4bm-Z is that separately authorized evaluation memo.**

Phase 4bm-Y lifecycle SHAs (verified present on `main`): base SHA `6d149e19ad9574a0fc36f5bbe966e25b839aa036`; docs/branch-tip commit `03468a453828fa8dc8b67f62c729e85761bece9d`; merge commit `5c86c4df9459d1cf854f1c72b2677605745b0e85`; merge-closeout commit `9d90e6aefea82ccbb7d08fb2647985f73c9e6b71`; SHA-finalization commit `2463ceb716d31c79ef766e9042fd40a3929f3e5c` (latest finalized `main` state and this phase's base).

The chain is internally consistent. Each phase preserves the upstream artefacts byte-identically. No verdict has been revised. No project lock has been loosened.

## 5. Evidence reviewed

### 5.1 Phase 4bm-Y scoping evidence (docs)

- Phase 4bm-Y scoping memo `2026-05-25_phase-4bm-y_ml-readiness-scoping-memo.md` (scoping decision `RECOMMEND_AUTHORIZE_ML_READINESS_EVALUATION_MEMO`; §8 one-way ordering; §9 task-framing questions; §10 horizon admissibility; §11 train/validation/test usage rules; §12 metric families; §13 leakage controls; §14 baseline families; §15 weighting/imbalance/calibration; §16 cost-aware questions incl. §11.6; §17 forbidden activities; §18 prerequisites).
- Phase 4bm-Y closeout `2026-05-25_phase-4bm-y_closeout.md` and merge-closeout `2026-05-25_phase-4bm-y_merge-closeout.md`.

### 5.2 Phase 4bm-X interpretation evidence (docs)

- Phase 4bm-X interpretation memo `2026-05-25_phase-4bm-x_descriptive-diagnostics-interpretation-memo.md` (criteria A–M all PASS; §7 blocking-failure review; §8 caveat interpretation; §9–§14 split/availability/distribution/alignment/stability/value-domain interpretation; §15 validation-discrepancy note; §19 pre-description of what a future scoping memo could evaluate).
- Phase 4bm-X closeout `2026-05-25_phase-4bm-x_closeout.md` and merge-closeout `2026-05-25_phase-4bm-x_merge-closeout.md`.

### 5.3 Phase 4bm-W execution evidence (docs)

- Phase 4bm-W implementation report `2026-05-25_phase-4bm-w_multi-day-v002-descriptive-diagnostics.md` (verdict `DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS`; eight diagnostic groups; split-policy application; embargo; censoring; distribution; alignment; missingness; holdout protection).
- Phase 4bm-W merge-closeout `2026-05-25_phase-4bm-w_merge-closeout.md` (accurate re-verified pytest count **33 passed**; upstream immutability table) and closeout `2026-05-25_phase-4bm-w_closeout.md`.

### 5.4 Predecessor governance / methodology evidence (docs)

- Phase 4bm-V readiness/scope memo, closeout, merge-closeout (allowed/forbidden diagnostics categories; split-policy/holdout constraints; local-output constraints).
- Phase 4bm-U chronological split-policy successor-state report, closeout, merge-closeout.
- Phase 4bm-T chronological split-policy memo, closeout, merge-closeout.
- Phase 4bm-S label-family research-use successor-state report, closeout, merge-closeout.
- Phase 4bm-R label-family research-use decision memo, closeout, merge-closeout.
- Phase 4bm-Q label-family eligibility-gate report, closeout, merge-closeout (60 / 60 PASS; report-level only).
- Phase 4bm-P multi-day v002 label artefact structural QA memo and merge-closeout (`LABEL_STRUCTURAL_QA_PASS`).

### 5.5 Governance / process artefacts reviewed

- `docs/00-meta/process/merge-closeout-standard.md` (Tier 1 merge-closeout ceremony — applies to a future, separately authorized merge phase, not to this branch work).
- `docs/00-meta/process/phase-risk-tiering-standard.md` (§3 escalation; reusable non-authorization blocks).
- `2026-05-17_phase-4bm-a-p1_context-management-standard.md` (thin-prompt context-management standard; honored).
- `2026-05-17_phase-4bm-d-p1_lightweight-claude-code-workspace-standard.md` (lightweight Claude Code workspace standard; honored).
- `docs/00-meta/current-project-state.md` (current-phase narrative and project locks).

### 5.6 Local-evidence verification (read-only)

The Phase 4bm-W local gitignored diagnostic outputs and all predecessor governed evidence artefacts were re-hashed read-only at the start of this phase and matched their expected values byte-for-byte. None was mutated; none was committed. **No diagnostics were rerun; no new artefact was created.**

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

## 6. Phase 4bm-Y scoping decision

`RECOMMEND_AUTHORIZE_ML_READINESS_EVALUATION_MEMO` (Phase 4bm-Y).

This recommended only that a future, separately authorized, docs-only ML-readiness *evaluation* memo *may* be proposed. The present Phase 4bm-Z is the separately authorized realization of that recommendation. Phase 4bm-Y authorized no ML, no training, no scoring, no prediction, no selection, no ranking, no tuning, no strategy, no backtests, no acquisition, and no research execution; it explicitly stated `Phase 4bm-Z is not authorized by Phase 4bm-Y`, and the present phase exists solely because the operator separately authorized it.

## 7. Phase 4bm-W diagnostic verdict

`DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS` (Phase 4bm-W).

This verdict is **descriptive-only**. It is **not** an ML-readiness, strategy-readiness, or backtest-readiness signal. Phase 4bm-Z does not change, re-derive, re-issue, or rerun this verdict; it carries it forward as the evidential baseline for evaluation.

- **0 blocking structural failures.** Every structural and alignment violation counter in the Phase 4bm-W summary aggregates to zero (`censor_rule_mismatch = 0`, `censored_row_not_null = 0`, `direction_domain_violation = 0`, `direction_sign_mismatch_vs_return = 0`, `any_censored_flag_mismatch = 0`, `row_index_violation = 0`, `src_ne_feature_ts = 0`, `out_of_partition_day = 0`, `split_assignment_mismatch = 0`, `invalid_price_row_count = 0`, plus symbol / dataset_version / config-hash constancy and all six feature/label alignment fields).
- **4 non-blocking caveats**, all understood and bounded, each carried forward in §13/§17 as an explicit stated constraint:
  1. **Envelope-terminal censoring asymmetry** — 857 censored rows total (`{1s:14, 5s:39, 15s:170, 60s:634}`), all on the final envelope day (2025-02-28; envelope terminal `1740787199996` ms) which lands entirely inside the test / final holdout; train and validation have zero censored rows.
  2. **538 embargo-excluded earlier-split rows** — train 248, validation 290, test 0; per-row masks only; the 90 v002 label parquets are never rewritten.
  3. **Approximate-quantile method** — fixed-width histogram (range ±0.02, bin width 1e-05); exact additive moments (mean / std / min / max) are *not* approximate.
  4. **`diagnostics_authorized=false` historical manifest flag** — predates Phase 4bm-W; authorization derives from the operator prompt, not from manifest mutation; manifests left byte-identical.

## 8. Evaluation criteria and results

This memo evaluates whether **all** of criteria A–R are satisfied. A future ML-baseline implementation *scoping/design* phase may be *recommended for authorization* only if all are satisfied.

| # | Criterion | Result | Evidence |
| --- | --- | --- | --- |
| **A** | Phase 4bm-Y completed and merged the docs-only ML-readiness scoping memo | **PASS** | §4; Phase 4bm-Y merge-complete, SHA-finalized on `main` (base `2463ceb7…`); decision `RECOMMEND_AUTHORIZE_ML_READINESS_EVALUATION_MEMO` |
| **B** | Phase 4bm-Y's scope is internally complete enough to support a future ML-baseline implementation scoping/design phase | **PASS** | §9–§18; Phase 4bm-Y §8–§18 enumerate task-framing, per-horizon admissibility, train/val/test rules, metric families, leakage controls, baseline families, weighting/imbalance/calibration, cost-aware questions, and implementation prerequisites — a complete question set |
| **C** | Phase 4bm-W diagnostics have 0 blocking structural failures | **PASS** | §7; all structural/alignment counters aggregate to 0 |
| **D** | Phase 4bm-W non-blocking caveats are carried forward as constraints and do not block implementation scoping | **PASS** | §7, §10, §13; all four caveats characterized, bounded, expected; carried forward as stated constraints; none requires remediation before a scoping/design phase |
| **E** | Phase 4bm-U split policy is sufficient for later ML-baseline design | **PASS** | §11; `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` applied verbatim by Phase 4bm-W; `out_of_partition_day = 0`; `split_assignment_mismatch = 0`; chronological, leakage-correct |
| **F** | Train/validation/test usage rules are explicit and enforceable | **PASS** | §11; assignment by `source_transact_time_ms` UTC date; 60s embargo; boundary-crossing exclusion; no shuffle/random/k-fold/bootstrap/resampling; restated and enforceable |
| **G** | Test holdout remains protected from tuning/design | **PASS** | §11; Phase 4bm-W `holdout_protection` block all protected; descriptive summaries only; single-use; this memo performs no tuning/design |
| **H** | Leakage controls are explicit and enforceable | **PASS** | §13; `src_ne_feature_ts = 0`; embargo enforced; train-only transform fitting; censored-rows-label-unavailable; no test-driven decisions; no manifest mutation as governance substitute |
| **I** | Candidate metrics can be scoped without computing them now | **PASS** | §12; class-balance, directional-classification, regression-error, rank/correlation, calibration, cost-aware-descriptive, train/val-stability families named for future selection; none computed |
| **J** | Candidate baseline families can be scoped without training them now | **PASS** | §14; majority/persistence/naive, logistic regression, regularized linear, calibrated tree ensembles, shallow gradient boosting, simple probabilistic references named for future consideration; none trained |
| **K** | Sample-weighting / imbalance / calibration questions are explicitly identified | **PASS** | §15; weighting, imbalance (incl. exact-zero mass), per-horizon censoring masking, calibration requirement, validation-only calibration, test-holdout calibration-leakage all identified as questions |
| **L** | Cost-aware constraints are explicit and include §11.6 8 bps per side / 16 bps round trip | **PASS** | §16; §11.6 = 8 bps per side / 16 bps round trip restated as a locked, non-loosenable constraint; horizon-vs-cost commensurability and latency sensitivity flagged |
| **M** | Horizon-specific constraints are explicit, especially 1s/5s latency sensitivity and 60s censoring concentration | **PASS** | §10; 1s/5s latency/tradability caveats; 15s/60s less-latency-sensitive-but-not-strategy-ready; 60s censoring concentration (634 of 857) all in test split |
| **N** | No diagnostics were rerun | **PASS** | §5.6; Phase 4bm-W outputs re-hashed read-only (MATCH); none rerun; no new diagnostic artefact created |
| **O** | No ML / strategy / backtest work has yet been authorized or run | **PASS** | §17; every predecessor records `ml_authorized=false` / `strategy_authorized=false` / `backtest_authorized=false`; this memo runs none |
| **P** | No manifest or successor-state mutation occurred | **PASS** | §5.6; v002 label/feature manifests, Phase 4bm-S/U successor-states, Phase 4bm-Q gate report byte-identical pre/post (re-hash MATCH) |
| **Q** | No data/microstructure or data/research artefact was committed | **PASS** | §5.6; `git status` shows no `data/microstructure/` entry; `data/research/` only as gitignored untracked local outputs; nothing staged/committed |
| **R** | Retained verdicts and project locks remain unchanged | **PASS** | §23–§24; preserved verbatim from Phase 4bm-Y |

**All evaluation criteria A–R PASS.**

## 9. Supervised-learning task-framing evaluation

Evaluated at memo / governance level only; **nothing is trained, selected, ranked, tuned, or run**. The Phase 4bm-Y §9 task-framing question set is internally complete and admissible for a later implementation scoping/design phase to *resolve* (not for this memo to resolve):

- **Classification vs. regression vs. ordinal framing** — all three remain admissible at scoping level; directional classification (`sign of forward return`), magnitude regression (`forward log-return`), and ordinal/binned framing each have coherent trade-offs. **This memo selects none.**
- **Horizon-specific vs. multi-horizon framing** — per-horizon-independent framing is the admissible default for any first baseline; shared-representation framing is deferred to a strictly later separately authorized stage. **This memo selects neither.**
- **Direction-only vs. magnitude-aware targets** — admissible to consider either `forward_direction_H ∈ {-1, 0, +1}` or the continuous forward return; the large exact-zero-return mass at short horizons (Phase 4bm-W: train 1s zero ≈ 6.41M shrinking to train 60s zero ≈ 0.14M) must be treated explicitly (e.g. as a genuine third class or excluded), decided in a later phase. **This memo selects no target.**
- **Censored-row handling per horizon** — censored rows must be treated as label-unavailable per horizon (never a class, never a zero), carried forward from the envelope-terminal censoring caveat. This is a *constraint*, not a framing decision made here.

**Evaluation result:** the task-framing scope is complete and admissible; no framing decision is required of, or made by, this evaluation memo. A later implementation scoping/design phase, if separately authorized, may resolve which framing to implement first — at design level only.

## 10. Target / horizon admissibility evaluation

Each horizon is discussed **separately**. This memo declares **no horizon ML-ready** and selects **no horizon**; it evaluates only that horizon-specific constraints are explicit and admissible.

- **1s horizon** — **latency-sensitive; admissible to discuss only with explicit latency/tradability caveats.** At a 1-second forward horizon, signal-to-execution latency, order placement, fill latency, and the 16 bps round-trip cost (§16) dominate; any later baseline framing for 1s must explicitly establish whether the horizon is operationally realizable at all before it could be considered. Not declared ML-ready.
- **5s horizon** — **latency-sensitive (less extreme than 1s); admissible only with the same latency/cost-realizability caveats.** Not declared ML-ready.
- **15s horizon** — operationally *less* latency-sensitive than 1s/5s, but **still not strategy-ready**. A later scoping/design phase would define what evidence is needed to evaluate it. Not declared ML-ready.
- **60s horizon** — operationally *least* latency-sensitive of the four, but **still not strategy-ready**. Censoring concentration is largest at 60s (634 of 857 censored rows) and falls entirely in the test split, so horizon-availability-by-split must be a stated constraint for 60s in particular. Not declared ML-ready.

**Evaluation result:** horizon-specific constraints (criterion M) are explicit and admissible; latency sensitivity for 1s/5s and censoring concentration for 60s are carried forward as constraints. No horizon is declared ML-ready and none is selected here.

## 11. Train / validation / test usage evaluation

The Phase 4bm-U policy `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` governs all future ML-baseline design and implementation:

| Split | UTC dates (inclusive) | Partitions | Rows (observed, Phase 4bm-W) |
| --- | --- | --- | --- |
| Train | 2024-12-01 .. 2025-01-14 | 45 | 74,535,688 |
| Validation | 2025-01-15 .. 2025-02-13 | 30 | 56,819,939 |
| Test / final holdout | 2025-02-14 .. 2025-02-28 | 15 | 23,797,822 |
| **Total** | 2024-12-01 .. 2025-02-28 | **90** | **155,153,449** |

Binding usage rules — explicit and enforceable (criteria E/F/G):

- **Train and validation** may be used **only in future, separately authorized implementation phases** — never in this evaluation memo.
- **Test / final holdout remains single-use** and may **not** be used for feature selection, model selection, hyperparameter selection, threshold tuning, strategy design, diagnostic iteration, eligibility rescue, or any tuning/design loop. **No test-holdout tuning/design.**
- **No shuffled cross-validation. No random split. No bootstrap split. No k-fold-over-time. No post-hoc temporal resampling.**
- Rows assigned by `source_transact_time_ms` UTC date.
- **Boundary embargo and boundary-crossing exclusion enforced** — minimum 60-second embargo at train/validation (`T_TV = 2025-01-15T00:00:00Z`) and validation/test (`T_VT = 2025-02-14T00:00:00Z`) boundaries; boundary-crossing rows excluded from the earlier split; never reassigned forward; per-row masks only (no parquet rewrite). Phase 4bm-W observed 538 earlier-split excluded rows (train 248, validation 290, test 0).
- **Split masks must not be materialized for future use unless separately authorized.** Phase 4bm-Z creates no split mask.

**Evaluation result:** the split policy is sufficient (E), the usage rules are explicit and enforceable (F), and the test holdout remains protected from tuning/design (G). The policy was applied verbatim by Phase 4bm-W with `out_of_partition_day = 0` and `split_assignment_mismatch = 0`.

## 12. Metrics-policy evaluation

This memo evaluates that candidate metric families can be **scoped without computing any of them** (criterion I). Permitted candidate metric families (definition only, **no computation**, carried forward from Phase 4bm-Y §12):

- **Class balance / prevalence metrics** — directional class prevalence per split×horizon (descriptive only).
- **Directional classification metrics** — accuracy, balanced accuracy, precision/recall, F1, ROC-AUC, PR-AUC, MCC (candidate families).
- **Regression error metrics** — MAE, RMSE, MAPE-style error on forward returns (candidate families).
- **Rank / correlation metrics** — Spearman / Kendall rank correlation, information coefficient (candidate families).
- **Calibration metrics** — reliability diagrams, Brier score, expected calibration error (candidate families).
- **Cost-aware descriptive metrics** — return-net-of-cost descriptive summaries at the §16 cost level, *descriptive only* (candidate families).
- **Stability metrics across train/validation only** — distribution / metric stability between train and validation, never touching the test holdout (candidate families).

Explicitly **excluded** at every level: **no PnL metrics; no backtest metrics; no strategy metrics.** **Phase 4bm-Z computes no metric of any kind.**

**Evaluation result:** the metric scope is complete and computable-later-only; no metric is computed now. Which metrics are actually computed would be decided in a future implementation phase.

## 13. Leakage-controls evaluation

The leakage controls (criterion H) are explicit and enforceable, carried forward from Phase 4bm-W/X/Y evidence:

- **Feature timestamp at or before label start** — Phase 4bm-W confirmed `source_transact_time_ms == feature_timestamp_ms` for every row (`src_ne_feature_ts = 0`); features are not constructed from future data.
- **No future data in features.**
- **No boundary-crossing labels in earlier splits** — enforced by the 60-second embargo (538 earlier-split rows excluded; test 0).
- **No test-driven feature/model/threshold decisions. No post-hoc horizon selection based on test.**
- **No fitting scalers / imputers / encoders on validation or test** — any such transforms a future baseline might use must be fit on **train only**.
- **No feature engineering based on validation/test diagnostics** unless separately authorized and documented.
- **No manifest mutation as a substitute for governance authorization** — authorization is operator-prompt-driven and recorded in docs/successor-state; the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved.
- **Censored rows treated as label-unavailable** per horizon (never a class, never a zero), carrying forward the envelope-terminal censoring caveat.

**Evaluation result:** leakage controls are explicit, enforceable, and grounded in observed Phase 4bm-W counters (all 0). They are admissible to carry into a later implementation scoping/design phase.

## 14. Baseline-model-family evaluation

This memo evaluates that candidate baseline families can be **scoped without training any of them** (criterion J). Candidate families named for future consideration only (carried forward from Phase 4bm-Y §14):

- **Majority / persistence / naive direction baselines** — the mandatory reference floor any later baseline must beat.
- **Logistic regression** (directional framing).
- **Regularized linear models** (L1 / L2 / elastic-net for regression or classification framing).
- **Calibrated tree ensembles** (e.g. random forests with calibration).
- **Shallow gradient boosting** (depth-limited).
- **Simple probabilistic baselines** (e.g. class-prior / kernel-density references).

**No deep learning** unless a later memo explicitly justifies it. **No model family is selected, implemented, or trained in Phase 4bm-Z.**

**Evaluation result:** the baseline-family scope is complete and consider-later-only. Which families are implemented first would be decided in a future implementation scoping/design phase — at design level only.

## 15. Sample-weighting / class-imbalance / calibration evaluation

The weighting / imbalance / calibration questions (criterion K) are explicitly identified (carried forward from Phase 4bm-Y §15). This memo **answers none of them**; it evaluates only that they are identified for a future phase:

- **Sample weighting** — whether class imbalance or per-row importance requires sample weighting, and if so which scheme.
- **Class imbalance** — whether the directional class distribution (including the large exact-zero mass at short horizons) requires weighting, train-only resampling discipline, or threshold-free metric choices.
- **Per-horizon censoring masking** — whether per-horizon censoring requires masking (treating censored rows as label-unavailable per horizon), given the envelope-terminal asymmetry.
- **Calibration requirement** — whether calibration should be *required* for any probability outputs a later baseline might produce.
- **Validation-only calibration** — whether calibration may be fit on validation only (never test), and how to document it.
- **Test-holdout calibration leakage** — how to avoid test-holdout calibration leakage (the test holdout must never be used to fit or tune calibration).

**Evaluation result:** all relevant weighting / imbalance / calibration questions are explicitly identified and are admissible to resolve in a future implementation scoping/design phase. None is answered here.

## 16. Cost-aware evaluation

Cost-aware constraints (criterion L) are explicit and **include the §11.6 lock**, carried forward from Phase 4bm-Y §16, **without designing strategy, simulating PnL, or running backtests**:

- **§11.6 cost lock** — **8 bps per side / 16 bps round trip**; any cost-aware descriptive evaluation must use this locked cost level and may not loosen it.
- **Signal horizon vs. transaction costs** — whether the descriptive return distribution at a given horizon is even commensurate with 16 bps round-trip cost (especially the 1s / 5s horizons, where dispersion is smallest — Phase 4bm-W train 1s std ≈ 2.44e-04).
- **Latency sensitivity** — explicit treatment of latency sensitivity, especially at 1s and 5s.
- **Slippage and spread caveats** — descriptive caveats on slippage and spread, noting that the v002 family does **not** contain order-book depth.
- **Boundary** — these are *cost-aware descriptive evaluation questions only*. A future phase **must not** design strategy, generate signals, simulate PnL, or run backtests; cost-awareness at evaluation/design level is descriptive, not strategy or backtest.

**Evaluation result:** cost-aware constraints are explicit and include the §11.6 8 bps / 16 bps lock; commensurability of the smallest-horizon return distributions with round-trip cost is flagged as a constraint a later phase must confront. No cost computation, PnL, or backtest is performed here.

## 17. Explicitly forbidden activities carried forward

The following are forbidden in **this** phase and, where stated, in any future ML-baseline implementation scoping/design phase (which would itself remain non-ML / non-strategy / non-backtest until a *further* separately authorized implementation phase):

- training any ML model; running any ML; scoring or evaluating predictions; generating predictions;
- selecting any model; ranking or selecting features; tuning hyperparameters; tuning thresholds; meta-labeling;
- defining or running strategy; generating signals; simulating PnL; running backtests; running walk-forward optimization;
- using the test holdout for tuning or design; eligibility rescue; post-hoc horizon selection based on test;
- materializing split masks for future use (Phase 4bm-Z creates none);
- creating ML artefacts; creating diagnostic artefacts; rerunning Phase 4bm-W diagnostics;
- mutating any manifest, the Phase 4bm-S successor-state artefact, the Phase 4bm-U successor-state artefact, the Phase 4bm-Q gate report, or any other `data/microstructure/` or `data/research/` artefact;
- changing `chronological_split_policy`, `research_eligible`, `eligibility_gate_status`, `diagnostics_authorized`, or `ml_authorized` on any on-disk manifest;
- acquiring data (no additional days / symbols / data families beyond the locked 90-day v002 envelope; no mark-price / order-book / funding / OI / liquidation / cross-venue / additional aggTrades);
- research execution; any public / authenticated / private endpoint call; any WebSocket / user-stream; any credential / `.env` / `.mcp.json` / MCP / Graphify use;
- committing `data/microstructure` or `data/research`.

## 18. Future ML-baseline implementation prerequisites

Before any later **ML-baseline implementation** phase may be *executed*, all of the following must be true (note the additional intermediate step: a separately authorized ML-baseline implementation *scoping/design* phase comes first):

- a **future ML-baseline implementation scoping/design phase completed and merged** (separately authorized; itself docs-only or design-only; trains/scores/predicts nothing);
- **explicit allowed targets/horizons selected at design level only** (which of 1s / 5s / 15s / 60s; direction vs. magnitude framing) — chosen in that scoping/design phase, never in this evaluation memo;
- **explicit leakage controls accepted and operationalized** (§13), including train-only transform fitting and validation-only calibration;
- **explicit metric policy accepted** (§12), specifying which metrics an implementation phase would compute;
- **explicit train/validation/test handling accepted** (§11), including single-use holdout protection and the rule that the test holdout remains unused until a single terminal evaluation;
- **explicit cost-aware descriptive policy accepted** (§16) at the §11.6 8 bps / 16 bps lock, kept non-strategy and non-backtest;
- **explicit non-use of the test holdout for tuning/design** confirmed;
- **explicit local-output / gitignore storage policy** for any implementation outputs (gitignored under `data/research/` or equivalent; never committed);
- **explicit test-suite and boundary requirements** for an implementation phase;
- **no unresolved blocking caveat** (the four Phase 4bm-W caveats remain understood, bounded, non-blocking, and carried forward as constraints);
- **retained verdicts and project locks preserved** (§23–§24).

A future ML-baseline implementation scoping/design phase would, in addition, require its own separately authorized operator prompt, its own branch, its own implementation report + closeout, and (separately) a Tier 1 merge-closeout. None of this is authorized by Phase 4bm-Z.

## 19. Decision

`RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION_SCOPING`.

## 20. Rationale for the chosen decision

All eighteen evaluation criteria A–R (§8) pass on current repo evidence:

- Phase 4bm-Y completed and merged the docs-only ML-readiness scoping memo, and its §8–§18 scope is internally complete enough to support a future ML-baseline implementation scoping/design phase (A, B).
- The Phase 4bm-W diagnostics passed with **0 blocking structural failures** (C) and **4 fully characterized, non-blocking caveats** (D) that require no remediation before implementation scoping, only carry-forward as stated constraints.
- The Phase 4bm-U split policy is sufficient for later ML-baseline design (E); train/validation/test usage rules are explicit and enforceable (F); the test holdout remains protected from tuning/design (G); leakage controls are explicit and enforceable (H).
- Candidate metrics can be scoped without computing them (I); candidate baseline families can be scoped without training them (J); sample-weighting / imbalance / calibration questions are explicitly identified (K); cost-aware constraints are explicit and include the §11.6 8 bps / 16 bps lock (L); horizon-specific constraints (1s/5s latency sensitivity; 60s censoring concentration) are explicit (M).
- No diagnostics were rerun (N); no ML / strategy / backtest work has been authorized or run (O); no manifest or successor-state mutation occurred (P); no `data/microstructure` or `data/research` artefact was committed (Q); and all retained verdicts and project locks remain unchanged (R).

Because every criterion passes — the descriptive diagnostics passed with only understood, non-blocking caveats; the split policy, leakage controls, cost constraints, and horizon-specific constraints are explicit and enforceable; and an ML-baseline implementation *scoping/design* phase is itself a docs-only/design-only governance artefact that trains nothing, scores nothing, predicts nothing, selects nothing, tunes nothing, and runs nothing — the appropriate recommendation is to authorize — separately and in a future phase — an ML-baseline implementation scoping/design phase only, bounded by §21. No prerequisite is missing and no drift was detected, so neither `DEFER_ML_BASELINE_IMPLEMENTATION_PENDING_SPECIFIC_REMEDIATION` nor `DO_NOT_RECOMMEND_ML_BASELINE_IMPLEMENTATION` is warranted. The recommendation is a *recommendation only*; it does not itself authorize any scoping/design phase, any ML, or any execution.

**`RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION_SCOPING` means only:** a future, separately authorized, docs-only or design-only phase may *scope* (propose the exact implementation boundaries for) a possible ML-baseline implementation. It does **not** mean ML implementation is authorized, model training is authorized, model scoring is authorized, prediction generation is authorized, feature selection is authorized, model selection is authorized, hyperparameter tuning is authorized, threshold tuning is authorized, strategy research is authorized, backtests are authorized, acquisition is authorized, or research execution is authorized.

## 21. What a future ML-baseline implementation scoping/design phase would be allowed to evaluate, if separately authorized

A future, separately authorized **ML-baseline implementation scoping/design phase** (provisionally a "Phase 4bn-A"-class phase, **not** authorized here) would be permitted to evaluate, at design level only:

- which target framing to implement first, at design level only;
- which horizons to include or defer, at design level only;
- which train/validation rows are admissible;
- whether censored rows are excluded per horizon;
- which baseline families should be implemented first;
- which metrics should be computed in an implementation phase;
- how train-only fitting of transforms will be enforced;
- how validation-only evaluation/calibration will be handled;
- how the test holdout will remain unused;
- how cost-aware descriptive evaluation will remain non-strategy / non-backtest;
- how outputs will be stored locally and gitignored;
- what tests will be required;
- what implementation boundaries will prevent ML / strategy / backtest drift.

A future ML-baseline implementation scoping/design phase **must not**: train models; score models; generate predictions; select features; rank features; select models through results; tune hyperparameters; tune thresholds; design strategy; generate signals; simulate PnL; run backtests; use the test holdout for tuning/design; materialize reusable split masks unless separately authorized; mutate manifests or successor-state artefacts; or acquire data. It would carry forward the four Phase 4bm-W caveats (§7) as explicit stated constraints, and would require its own separately authorized operator prompt, its own branch, its own implementation report + closeout, and (separately) a Tier 1 merge-closeout. **Any ML-baseline implementation requires a separately authorized implementation phase.**

## 22. What this phase does not authorize

Phase 4bm-Z defines an ML-readiness evaluation and a single governance recommendation only. It does **not**, and **cannot**, authorize:

- any ML-baseline implementation scoping/design phase (it only *recommends* that one may be separately authorized); any ML-baseline implementation; any diagnostics rerun; any new diagnostic artefact; any ML artefact; any split-mask materialization;
- any ML training / model scoring / prediction generation / model selection / feature ranking / feature selection / hyperparameter selection / threshold tuning / meta-labeling; any strategy specification / implementation / signal construction; any PnL simulation / backtest / walk-forward optimization;
- any use of the test window for tuning or design; any eligibility rescue;
- any mutation of any manifest, the Phase 4bm-S successor-state artefact, the Phase 4bm-U successor-state artefact, the Phase 4bm-Q gate report, or any other `data/microstructure/` or `data/research/` artefact;
- any change to `chronological_split_policy`, `research_eligible`, `eligibility_gate_status`, `diagnostics_authorized`, or `ml_authorized` on any on-disk manifest;
- any data acquisition (no additional days / symbols / data families beyond the locked 90-day v002 envelope; no mark-price / order-book / funding / OI / liquidation / cross-venue / additional aggTrades);
- any public / authenticated / private endpoint call; any WebSocket / user-stream; any credential / `.env` / `.mcp.json` / MCP / Graphify use;
- Phase 4bn-A or any successor phase; Phase 5; Phase 4 canonical; paper / shadow; live-readiness; deployment; exchange-write; production-key creation;
- any revision of a retained verdict, any loosening of a project lock, or any amendment of M0 / Phase 4al / Phase 4aw / Phase 4bb-F / Phase 4bl-F / Phase 4bm-A-P1 / Phase 4bm-D-P1.

**Phase 4bm-Z is a docs-only ML-readiness evaluation memo.** **Phase 4bm-Z does not train ML models.** **Phase 4bm-Z does not run ML.** **Phase 4bm-Z does not score models.** **Phase 4bm-Z does not generate predictions.** **Phase 4bm-Z does not select models.** **Phase 4bm-Z does not rank or select features.** **Phase 4bm-Z does not tune hyperparameters.** **Phase 4bm-Z does not tune thresholds.** **Phase 4bm-Z does not define or run strategy.** **Phase 4bm-Z does not generate signals.** **Phase 4bm-Z does not simulate PnL.** **Phase 4bm-Z does not run backtests.** **Phase 4bm-Z does not authorize acquisition.** **Phase 4bm-Z does not authorize research execution.** **Phase 4bm-Z does not create ML artefacts.** **Phase 4bm-Z does not create diagnostic artefacts.** **Phase 4bm-Z does not create split masks.** **Phase 4bm-Z does not use the test holdout for tuning or design.** **Phase 4bm-Z does not mutate any manifest.** **Phase 4bm-Z does not mutate any successor-state artefact.** **Phase 4bm-Z does not commit data/microstructure.** **Phase 4bm-Z does not commit data/research.** **Any ML-baseline implementation requires a separately authorized implementation phase.** **Phase 4bn-A is not authorized by Phase 4bm-Z.**

## 23. Retained verdicts preserved

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

All prior phase results (Phase 4am .. Phase 4bm-Y) preserved verbatim.

## 24. Project locks preserved

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
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (never invoked by Phase 4bm-Z)
- Phase 4bb-F canonical sidecar / path policy
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks
- Phase 4bm-A-P1 thin-prompt context-management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace standard

## 25. Recommended next state

**Remain paused.** Phase 4bm-Z is branch-complete only by this work. Per the Phase 4bk-A workflow standard, it is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1). The evaluation decision is `RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION_SCOPING`; this is a recommendation only and authorizes nothing. **Any ML-baseline implementation requires a separately authorized implementation phase.** **Phase 4bn-A is not authorized by Phase 4bm-Z.** **Recommended state remains paused.**
