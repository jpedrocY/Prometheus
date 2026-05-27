# Phase 4bn-A — Multi-Day V002 ML-Baseline Implementation Scoping / Design

**Phase identity:** Phase 4bn-A — Multi-Day V002 ML-Baseline Implementation Scoping / Design (docs-only / design-only ML-baseline implementation scoping phase; the first phase of the ML arc, separately authorized by the Phase 4bm-Z recommendation `RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION_SCOPING`, which defines the exact implementation boundaries for a possible future ML-baseline implementation phase over the multi-day v002 BTCUSDT feature/label family).
**Date:** 2026-05-27.
**Branch:** `phase-4bn-a/multi-day-v002-ml-baseline-implementation-scoping-design`.
**Base SHA:** `main` at `de170ad31b9dd71e9f5c8fac59d4b19472d9e6d0` (Phase 4bm-Z merge-closeout SHA-finalization commit `docs(phase-4bm-z): finalize merge closeout shas`; pre-branch `main == origin/main` verified in sync).
**Tier:** **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3. This phase begins the ML arc by defining the exact implementation boundaries for a future ML-baseline implementation; it is adjacent to ML training, model scoring, prediction generation, feature/model selection, hyperparameter tuning, threshold tuning, strategy research, backtests, acquisition, and research execution while explicitly authorizing none of them, so it escalates to Tier 1.
**Phase type:** docs-only / design-only ML-baseline implementation scoping phase. Adds two new tracked docs files under `docs/00-meta/implementation-reports/` (this memo + the paired closeout) and narrowly updates `docs/00-meta/current-project-state.md`. **No** source / test / committed-script / configuration / manifest / sidecar / gate-report / successor-state mutation. **No** local data artefact created or mutated. **No** diagnostic rerun. **No** ML artefact. **No** acquisition. **No** successor authorization.
**Status:** drafted; pending operator review. Branch-complete only by this work; not merged into `main`; not project-complete.

---

## 0. Required exact phrases

- **Phase 4bn-A is a docs-only / design-only ML-baseline implementation scoping phase.**
- **Phase 4bn-A does not train ML models.**
- **Phase 4bn-A does not run ML.**
- **Phase 4bn-A does not score models.**
- **Phase 4bn-A does not generate predictions.**
- **Phase 4bn-A does not select models through results.**
- **Phase 4bn-A does not rank or select features.**
- **Phase 4bn-A does not tune hyperparameters.**
- **Phase 4bn-A does not tune thresholds.**
- **Phase 4bn-A does not define or run strategy.**
- **Phase 4bn-A does not generate signals.**
- **Phase 4bn-A does not simulate PnL.**
- **Phase 4bn-A does not run backtests.**
- **Phase 4bn-A does not authorize acquisition.**
- **Phase 4bn-A does not authorize research execution.**
- **Phase 4bn-A does not create ML artefacts.**
- **Phase 4bn-A does not create diagnostic artefacts.**
- **Phase 4bn-A does not create reusable split masks.**
- **Phase 4bn-A does not use the test holdout for tuning or design.**
- **Phase 4bn-A does not mutate any manifest.**
- **Phase 4bn-A does not mutate any successor-state artefact.**
- **Phase 4bn-A does not commit data/microstructure.**
- **Phase 4bn-A does not commit data/research.**
- **Any ML-baseline implementation requires a separately authorized implementation phase.**
- **Phase 4bn-B is not authorized by Phase 4bn-A.**
- **Recommended state remains paused.**

> **Successor-naming note.** Phase 4bm-Z was the terminal letter of the `4bm-` series; the next letter-series, opened by this phase, is `4bn-`. By the repo's established within-series convention (`-A`, `-B`, `-C`, …), the next phase after Phase 4bn-A is **`Phase 4bn-B`**. The required exact phrases therefore name `Phase 4bn-B` as the unauthorized future ML-baseline implementation phase. No successor is authorized under any name.

---

## 1. Phase identity

Phase 4bn-A answers a single design / governance question:

> Given that Phase 4bm-Z recommends authorizing ML-baseline implementation scoping, what exact implementation boundaries, targets, horizons, baseline families, metric families, leakage controls, local-output rules, and validation requirements should govern a future ML-baseline implementation phase?

Phase 4bn-A is **docs-only / design-only**. It defines the exact implementation boundaries for a possible future ML-baseline *implementation* phase over the multi-day v002 BTCUSDT feature/label family `microstructure_features_aggtrades_v001 @ v002` (features) and `microstructure_labels_aggtrades_v001 @ v002` (labels) — 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 rows; horizons 1s / 5s / 15s / 60s — under the Phase 4bm-U recorded chronological split policy `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`. It trains nothing, scores nothing, predicts nothing, selects nothing, ranks nothing, tunes nothing, runs nothing, materializes no split mask, creates no ML artefact, mutates no manifest or successor-state artefact, acquires no data, and authorizes no successor implementation. **Phase 4bn-A is a docs-only / design-only ML-baseline implementation scoping phase.** **This is the beginning of the ML phase arc, but it is not ML execution.**

- **Phase name:** Phase 4bn-A — Multi-Day V002 ML-Baseline Implementation Scoping / Design.
- **Phase type:** docs-only / design-only ML-baseline implementation scoping phase.
- **Branch:** `phase-4bn-a/multi-day-v002-ml-baseline-implementation-scoping-design`.
- **Base SHA:** `main` at `de170ad31b9dd71e9f5c8fac59d4b19472d9e6d0`.
- **Authorization:** explicit operator authorization for Phase 4bn-A only.

## 2. Branch name

`phase-4bn-a/multi-day-v002-ml-baseline-implementation-scoping-design`

## 3. Base SHA

`de170ad31b9dd71e9f5c8fac59d4b19472d9e6d0` (Phase 4bm-Z merge-closeout SHA-finalization commit, `docs(phase-4bm-z): finalize merge closeout shas`; the head of `main` at branch time; `main == origin/main` verified in sync). The Phase 4bm-Z docs/branch-tip commit `0c84b6921a013c37da32a72063a79a7f68867ad3`, merge commit `5b86ecf496421e86138179f47c8273aa1837dbd1`, and merge-closeout commit `b8afee7b4e9762e3880d1a782799631d588e78a1` are present on `main` immediately below this SHA-finalization commit (verified by `git log --oneline -16 --decorate`).

## 4. Predecessor chain

| Phase | Role | Status on `main` | Verdict / result |
| --- | --- | --- | --- |
| **Phase 4bm-W** | Multi-day v002 descriptive diagnostics execution | merge-complete; SHA-finalized | `DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS` (descriptive-only) |
| **Phase 4bm-X** | Multi-day v002 descriptive diagnostics interpretation memo | merge-complete; SHA-finalized | `RECOMMEND_AUTHORIZE_ML_READINESS_SCOPING_MEMO` (criteria A–M PASS) |
| **Phase 4bm-Y** | Multi-day v002 ML-readiness scoping memo | merge-complete; SHA-finalized | `RECOMMEND_AUTHORIZE_ML_READINESS_EVALUATION_MEMO` |
| **Phase 4bm-Z** | Multi-day v002 ML-readiness evaluation memo | merge-complete; SHA-finalized | `RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION_SCOPING` (criteria A–R PASS) |

Direct predecessors for this memo:

- **Phase 4bm-W** — the descriptive / structural diagnostics execution. Verdict `DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS`: 0 blocking structural failures; 4 non-blocking caveats (carried forward in §12/§21).
- **Phase 4bm-X** — interpreted the Phase 4bm-W verdict; criteria A–M PASS; recommended an ML-readiness scoping memo.
- **Phase 4bm-Y** — scoped the admissible questions / boundaries for ML-readiness *evaluation*; recommended an ML-readiness evaluation memo.
- **Phase 4bm-Z** — evaluated those questions; criteria A–R PASS; recommended ML-baseline implementation *scoping/design* (decision `RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION_SCOPING`). **This Phase 4bn-A is that separately authorized scoping/design phase.**

Phase 4bm-Z lifecycle SHAs (verified present on `main`): base SHA `2463ceb716d31c79ef766e9042fd40a3929f3e5c`; docs/branch-tip commit `0c84b6921a013c37da32a72063a79a7f68867ad3`; merge commit `5b86ecf496421e86138179f47c8273aa1837dbd1`; merge-closeout commit `b8afee7b4e9762e3880d1a782799631d588e78a1`; SHA-finalization commit `de170ad31b9dd71e9f5c8fac59d4b19472d9e6d0` (latest finalized `main` state and this phase's base).

The chain is internally consistent. Each phase preserves the upstream artefacts byte-identically. No verdict has been revised. No project lock has been loosened.

## 5. Evidence reviewed

### 5.1 ML-arc governance evidence (docs)

- Phase 4bm-Z ML-readiness evaluation memo, closeout, and merge-closeout (`RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION_SCOPING`; criteria A–R PASS; §21 future scoping/design boundaries; §16 cost-aware §11.6 lock; §11 split-policy restatement).
- Phase 4bm-Y ML-readiness scoping memo, closeout, merge-closeout (§9–§18 admissibility scope: task-framing, per-horizon admissibility, train/val/test rules, metric families, leakage controls, baseline families, weighting/imbalance/calibration, cost-aware questions, prerequisites).
- Phase 4bm-X interpretation memo, closeout, merge-closeout (criteria A–M PASS; per-area interpretation of split / availability / distribution / alignment / value-domain).
- Phase 4bm-W diagnostics report, closeout, merge-closeout (verdict, 4 caveats, 0 blocking failures, holdout protection, strict 1:1 alignment).

### 5.2 Split / label / feature evidence (docs + manifest)

- Phase 4bm-V diagnostics readiness/scope memo; Phase 4bm-U chronological split-policy successor-state; Phase 4bm-T split-policy memo; Phase 4bm-S label-family research-use successor-state; Phase 4bm-R research-use decision memo; Phase 4bm-Q label-family eligibility gate (60/60 PASS); Phase 4bm-P label artefact structural QA (`LABEL_STRUCTURAL_QA_PASS`).
- `docs/00-meta/process/merge-closeout-standard.md`; `docs/00-meta/process/phase-risk-tiering-standard.md`; Phase 4bm-A-P1 thin-prompt context-management standard; Phase 4bm-D-P1 lightweight Claude Code workspace standard.
- `docs/00-meta/current-project-state.md`.

### 5.3 Feature-surface schema evidence (read-only manifest inspection)

The v002 feature manifest (`512a0a54…`) was read read-only to derive the feature surface (§13) from evidence rather than guesses:

- `feature_schema_version = v001`; `feature_config_hash = 819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d`.
- `feature_windows_ms = [1000, 5000, 15000, 60000]`; `feature_window_labels = [1s, 5s, 15s, 60s]`.
- `feature_column_names`: **62 total = 17 lineage + 45 computed.**
- **17 `lineage_column_names`** (identifiers / timestamps / lineage SHAs — excluded from any model matrix): `dataset_family`, `dataset_version`, `source_dataset_family`, `source_dataset_version`, `feature_schema_version`, `symbol`, `utc_date`, `agg_trade_id`, `row_index`, `feature_timestamp_ms`, `source_transact_time_ms`, `source_normalized_parquet_per_day_sha256`, `source_normalized_manifest_sha256`, `source_successor_state_sha256`, `source_phase_4bm_d_gate_report_sha256`, `source_phase_4bm_e_outcome`, `feature_config_hash`.
- **45 `computed_feature_column_names`**: 10 rolling features × 4 windows (40) — `rolling_aggtrade_count_{w}`, `rolling_quantity_sum_{w}`, `rolling_quantity_mean_{w}`, `rolling_aggressive_buy_quantity_{w}`, `rolling_aggressive_sell_quantity_{w}`, `rolling_aggressive_buy_count_{w}`, `rolling_aggressive_sell_count_{w}`, `rolling_aggressive_flow_ratio_{w}`, `rolling_aggressive_quantity_imbalance_{w}`, `rolling_log_return_past_window_{w}` for `w ∈ {1s,5s,15s,60s}`; plus 5 non-windowed columns — `utc_hour`, `utc_minute`, `milliseconds_since_day_start`, `invalid_window_flag`, `rolling_missing_window_flag`.

### 5.4 Local-evidence verification (read-only)

All Phase 4bm-W diagnostic outputs and predecessor governed artefacts were re-hashed read-only at the start of this phase and matched their expected values byte-for-byte. None was mutated; none was committed. **No diagnostics were rerun; no new artefact created.**

| Artefact | Expected SHA256 | Result |
| --- | --- | --- |
| `descriptive_diagnostics_summary.json` | `f4b825af2e81734007be06acac5083e2d4048b54b5650bc407d87a6fc246198a` | MATCH (gitignored `data/research/`) |
| `descriptive_diagnostics_summary.json.sha256` | `ff52873c983b55cc74a0639d17ea8b3d128cdbee9c77763cd11d2e71b3820473` | MATCH |
| `diagnostics_manifest.json` | `ac10061d2f0257002e094d578bcc6149b1a74ca28c604fd0d0a97e5c51c26e45` | MATCH |
| `diagnostics_manifest.json.sha256` | `644506e392db46da6d27fa46519cac327136b1a05e350e2d9b231c62fce517eb` | MATCH |
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

`git check-ignore -v` confirms the diagnostic outputs are covered by `.gitignore:88: data/research/` and the microstructure artefacts by `.gitignore:85: data/microstructure/`; neither appears as a staged or committed change. This memo reads all evidence read-only and reruns nothing.

## 6. Phase 4bm-Z decision

`RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION_SCOPING` (Phase 4bm-Z; criteria A–R all PASS).

This recommended only that a future, separately authorized, docs-only or design-only ML-baseline implementation *scoping/design* phase *may* be proposed. The present Phase 4bn-A is the separately authorized realization of that recommendation. Phase 4bm-Z authorized no ML implementation, training, scoring, prediction, selection, ranking, tuning, strategy, signals, PnL, backtests, acquisition, or research execution; it explicitly stated `Phase 4bn-A is not authorized by Phase 4bm-Z`, and the present phase exists solely because the operator separately authorized it.

## 7. Design criteria and results

| # | Criterion | Result | Basis |
| --- | --- | --- | --- |
| A | Phase 4bm-Z completed and merged the docs-only ML-readiness evaluation memo | **PASS** | §4; merge `5b86ecf…`, merge-closeout `b8afee7…`, SHA-finalization `de170ad…` on `main` |
| B | Phase 4bm-Z recommended ML-baseline implementation scoping/design | **PASS** | §6; `RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION_SCOPING` |
| C | Future implementation boundary definable without training models in this phase | **PASS** | §8; boundary specified declaratively; nothing trained |
| D | Target framing specifiable without using test holdout for tuning/design | **PASS** | §9, §11; framing fixed from label schema; holdout sealed |
| E | Horizon inclusion/deferral specifiable without declaring any horizon strategy-ready | **PASS** | §10; 15s/60s included for baseline ML only; no horizon strategy-ready |
| F | Train/validation/test handling can enforce the Phase 4bm-U split policy | **PASS** | §11; restates `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` |
| G | Censored-row handling definable per horizon | **PASS** | §12; per-horizon label-unavailable masking |
| H | Feature surface freezable to v002 feature family without new feature engineering | **PASS** | §13; 45 computed columns frozen from manifest; no selection/ranking |
| I | Transform/preprocessing rules can enforce train-only fitting | **PASS** | §14; fit on train only; apply to validation only |
| J | Baseline families selectable for first implementation at design level without result-based selection | **PASS** | §15; families fixed a priori; no result-based selection |
| K | Metric policy specifiable without computing metrics in this phase | **PASS** | §16; candidate metric families named; none computed |
| L | Calibration policy specifiable without fitting calibration in this phase | **PASS** | §17; validation-only calibration policy; nothing fit |
| M | Cost-aware descriptive evaluation specifiable without strategy/backtest/PnL | **PASS** | §18; §11.6 lock; descriptive-only |
| N | Output artefact policy can keep all future outputs local and gitignored | **PASS** | §19; gitignored namespace; nothing committed |
| O | Test/validation requirements specifiable without running implementation | **PASS** | §20; future test list specified; nothing run |
| P | Anti-drift boundaries can prevent ML/strategy/backtest/acquisition drift | **PASS** | §21; explicit non-authorization boundary |
| Q | No diagnostics rerun | **PASS** | §5.4; re-hash MATCH; none rerun |
| R | No ML / scoring / predictions / feature-or-model selection / hp/threshold tuning / strategy / backtest occurred | **PASS** | this memo runs none |
| S | No manifest or successor-state mutation occurred | **PASS** | §5.4; byte-identical pre/post |
| T | No data/microstructure or data/research artefact committed | **PASS** | docs-only; nothing committed under `data/` |
| U | Retained verdicts and project locks remain unchanged | **PASS** | §26–§27; preserved verbatim |

**All design criteria A–U PASS.**

## 8. Proposed implementation boundary for a future ML-baseline implementation phase

A future, separately authorized **ML-baseline implementation** phase (provisionally `Phase 4bn-B`, **not** authorized here) would implement *exactly* the design in §9–§20, and nothing beyond it. The boundary is deliberately conservative: a small number of fixed-a-priori baseline families, trained on train, evaluated on validation, with the test holdout sealed; direction classification only; horizons 15s and 60s only; the frozen v002 feature surface; train-only transform fitting; descriptive ML metrics plus a §11.6-locked cost-commensurability summary; all outputs local and gitignored. The implementation phase produces an **ML evaluation artefact set**, not a strategy, not signals, not a backtest, not PnL. The strict one-way ordering is:

```text
Phase 4bn-A (this memo: design — defines the exact implementation boundary)
   → Phase 4bn-B (future, separately authorized: ML-BASELINE IMPLEMENTATION — trains/evaluates baselines on train/validation only)
      → (only then, if and only if separately authorized) any later baseline-expansion / calibration / horizon / strategy-research phase
```

## 9. Target framing design

- **First implementation target family: direction classification only.** Direction labels taken from the existing v002 label family (`forward_direction_H ∈ {-1, 0, +1}`).
- **Zero direction is its own explicit class** if present in the label schema (the v002 schema preserves the strict-sign `{-1, 0, +1}` policy). The zero/flat class **must not** be merged into up or down, and **must not** be dropped.
- **No forward-return magnitude regression target** in first implementation.
- **No ordinal framing** in first implementation.
- **No meta-labeling.**
- Per-horizon-independent framing: each included horizon is an independent 3-class classification task; **no shared representation** in first implementation.
- Phase 4bn-A selects no model and trains nothing; this fixes the *target family* by design, not by result.

## 10. Horizon inclusion / deferral design

- **Include 15s and 60s** in the first baseline implementation design.
- **Defer 1s and 5s** from first implementation because of latency / tradability sensitivity and cost-commensurability risk (Phase 4bm-Z §10/§16: at 1s/5s, signal-to-execution latency and 16 bps round-trip cost dominate; smallest-horizon dispersion is smallest, e.g. train 1s forward-return std ≈ 2.44e-04). 1s / 5s may be revisited only by later separately authorized phases.
- **60s inclusion carries the test-split censoring caveat** (Phase 4bm-W: 60s censored rows = 634 of 857, all on the final envelope day inside the test split) and **per-horizon censored-row masking** (§12).
- **No horizon is declared strategy-ready. No horizon is declared live-tradable.** Inclusion here means "admissible for a descriptive supervised-learning baseline," nothing more.

## 11. Train / validation / test handling design

Governing policy: Phase 4bm-U `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`.

| Split | UTC dates (inclusive) | Partitions | Rows (observed, Phase 4bm-W) |
| --- | --- | --- | --- |
| Train | 2024-12-01 .. 2025-01-14 | 45 | 74,535,688 |
| Validation | 2025-01-15 .. 2025-02-13 | 30 | 56,819,939 |
| Test / final holdout | 2025-02-14 .. 2025-02-28 | 15 | 23,797,822 |
| **Total** | 2024-12-01 .. 2025-02-28 | **90** | **155,153,449** |

- **Train split**: may be used to fit transforms and train models **only in a future separately authorized implementation phase**.
- **Validation split**: may be used for evaluation and calibration **only under explicit rules in a future separately authorized implementation phase**.
- **Test split / final holdout**: remains **sealed / unused** in the first implementation phase unless a later phase explicitly authorizes a single terminal holdout evaluation. **No test-holdout tuning/design.**
- **No random split. No shuffled cross-validation. No k-fold-over-time. No bootstrap split. No post-hoc temporal resampling.** Rows assigned by `source_transact_time_ms` UTC date.
- Apply the **Phase 4bm-U 60-second boundary embargo** and **boundary-crossing exclusion** (earlier-split rows whose label horizon crosses a boundary are excluded from the earlier split; never reassigned forward; Phase 4bm-W observed 538 excluded — train 248, validation 290, test 0).
- **Split masks**, if needed, must be generated locally in the implementation phase and remain gitignored; **reusable split masks are not authorized by Phase 4bn-A.**

## 12. Censored-row handling design

- Treat censored rows as **label-unavailable per horizon** (a row may be censored at 60s but available at 15s; masking is per-horizon, not per-row-global).
- **Exclude censored rows from the supervised loss and from the metric denominator for that horizon.**
- **Do not impute** censored labels.
- **Do not treat censored rows as zero-return / no-change / flat-class rows.**
- **Report censored-row counts per split × horizon** in future implementation outputs (the known v002 aggregate is `{1s:14, 5s:39, 15s:170, 60s:634}`, all in the test split; for the included horizons the train/validation censored counts are zero, so masking primarily affects the sealed test split — but the rule is stated for completeness and robustness).

## 13. Feature surface design

- **Use only the existing v002 feature family** `microstructure_features_aggtrades_v001 @ v002`; **preserve `feature_config_hash = 819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d`**.
- **No new feature engineering. No feature selection. No feature ranking. No post-hoc feature pruning. No feature generation from validation/test diagnostics.**
- The feature list is **derived from manifest/schema evidence** (§5.3), not guessed.
- **Model feature matrix (frozen by deterministic rule, not selection): the 45 `computed_feature_column_names`** — the 40 rolling features (`rolling_*_{1s,5s,15s,60s}`) plus `utc_hour`, `utc_minute`, `milliseconds_since_day_start`, `invalid_window_flag`, `rolling_missing_window_flag`. The two flag columns are retained as **explicit deterministic missingness/validity indicators** (computed from past windows only — no leakage); the implementation phase must not drop them based on results.
- **Excluded from the model feature matrix:** all **17 `lineage_column_names`** (identifiers, `utc_date`, `agg_trade_id`, `row_index`, `feature_timestamp_ms`, `source_transact_time_ms`, all lineage SHA columns, `feature_config_hash`), all **label columns** and label-derived fields, and any **split-flag** column. Identifiers and timestamps are excluded because they encode row identity / split membership and would leak.

## 14. Transform / preprocessing design

- **Fit scalers / imputers / encoders on train only.** Apply the trained transforms to validation only. **Do not fit anything on validation or test.**
- **No target leakage through preprocessing** (transforms see features only, never labels; statistics computed on train rows only).
- **Missingness handling must be explicit**: the `rolling_missing_window_flag` / `invalid_window_flag` columns are explicit indicators; any imputation of numeric features must be train-fit and documented (e.g. train-median impute) and must never use validation/test statistics.
- **Any class encoding must preserve the zero / flat class** if present (3-class `{-1, 0, +1}` encoding; no collapse to binary).
- **Persist transform metadata only as local gitignored output** in a future implementation phase (e.g. `transform_metadata.json`); never committed.

## 15. Baseline model-family design

First baseline families fixed **a priori at design level** (no result-based selection, no search):

1. **Majority-class / class-prior baseline** — the mandatory reference floor any later baseline must beat.
2. **Persistence / naive-direction baseline** — only if supported by the existing features/labels without leakage (e.g. sign of the most recent past-window log return as a no-cost reference; uses only past-window features already in the v002 matrix).
3. **Multinomial logistic regression** (3-class `{-1,0,+1}`) — optionally **regularized** logistic regression.
4. **Regularized linear classifier family** if compatible with the label encoding (e.g. L1 / L2 multinomial).
5. **Optionally one shallow tree-based baseline** only if complexity and leakage controls are explicitly bounded (e.g. a single depth-limited decision tree with a fixed, pre-declared max-depth — not tuned).

- **No deep learning.**
- **Gradient boosting is deferred** to a later, separately authorized baseline-expansion phase: gradient boosting introduces effective-hyperparameter sensitivity (learning rate, depth, n-estimators, subsampling) whose responsible use entails a search/tuning loop that this conservative first baseline deliberately excludes; deferring it keeps the first implementation reproducible and result-selection-free. It is **not** part of the first baseline.
- **No hyperparameter search. No model-family selection through results. No ensemble selection.** Each family is run once with pre-declared, fixed, documented settings; all families are reported; none is chosen by validation performance in the first implementation.

## 16. Metric policy design

Candidate metrics for the future implementation phase (defined here; **none computed in Phase 4bn-A**):

- class prevalence by split × horizon;
- confusion matrix by split × horizon;
- accuracy;
- balanced accuracy;
- macro F1;
- per-class precision / recall;
- log loss (if probabilistic outputs are produced);
- Brier score / calibration summary (if probabilistic outputs are produced);
- train / validation stability summaries;
- cost-aware descriptive return summaries at the §11.6 cost lock, **without strategy / backtest / PnL** (§18).

Explicitly **forbidden**: PnL metrics; backtest metrics; Sharpe / Sortino / drawdown; hit-rate-as-strategy metric; threshold-tuned metrics; test-set metrics in first implementation; any metric used to design strategy or tune trade thresholds.

## 17. Calibration design

- Calibration may be **evaluated only on validation** in a future implementation phase. **No test calibration.**
- **No threshold tuning. No probability-to-signal conversion.**
- Calibration outputs, if any, remain **descriptive / ML-evaluation only** (reliability summary, Brier score) and **must not create strategy triggers**.

## 18. Cost-aware descriptive evaluation design

- Use **§11.6 = 8 bps per side / 16 bps round trip** as the locked reference.
- **Only descriptive cost-commensurability summaries** are allowed (e.g. what fraction of validation forward-return magnitude at a horizon exceeds 16 bps round-trip cost — descriptive context, not a tradability claim).
- **No PnL simulation. No strategy construction. No entry/exit rules. No trade threshold design. No order/position model. No backtest.**

## 19. Output artefact and gitignore design

Future implementation outputs, if separately authorized, must be **local and gitignored** under an approved namespace, for example:

```text
data/research/microstructure/ml-baselines/phase-4bn-b/
```

(or another approved gitignored namespace under `data/research/`).

Future outputs may include (all local, all gitignored, none committed):

- `ml_baseline_run_manifest.json` + `.sha256`
- `per_horizon_model_summary.json` + `.sha256`
- `metrics_train_validation.csv`
- `calibration_summary.csv`
- `class_balance_summary.csv`
- `feature_schema_used.json`
- `transform_metadata.json`
- model artefacts **only if separately authorized** in the future implementation phase.

**Do not commit implementation outputs. Do not commit model artefacts. Do not commit `data/research`. Do not commit `data/microstructure`.**

**Sidecar policy:** use the canonical Phase 4bb-F sidecar format for JSON / manifest outputs — `<sha256_lowercase_hex><two spaces><basename><LF>` (64 hex + two ASCII spaces + basename + single LF; no CRLF; no BOM).

## 20. Test and validation design

A future implementation phase must include tests for:

- split-policy enforcement (chronological 45/30/15; assignment by `source_transact_time_ms` UTC date);
- test-holdout exclusion (test split sealed / unused);
- train-only transform fitting (no fit on validation/test);
- censored-row exclusion by horizon;
- feature/label row alignment (strict 1:1 join key; `src_ne_feature_ts = 0`);
- no leakage columns in the feature matrix (the 17 lineage columns + labels + split flags excluded);
- no forbidden imports / endpoints / credentials (no network, no `.env`, no `.mcp.json`, no MCP/Graphify);
- output sidecar format (canonical Phase 4bb-F);
- local-output gitignore behaviour;
- no strategy / backtest / PnL functions present in the implementation surface;
- deterministic manifest generation (pinned RNG seed; idempotent outputs);
- CLI dry-run or small-fixture run if applicable.

## 21. Anti-drift / non-authorization boundary

The future implementation phase **must not**, and this design **does not** authorize: training in this phase; model scoring in this phase; prediction generation in this phase; feature ranking; feature selection; model-family selection through results; hyperparameter tuning; threshold tuning; strategy definition; signal generation; PnL simulation; backtests; walk-forward optimization; use of the test holdout for tuning/design; materialization of reusable split masks; manifest mutation; successor-state mutation; data acquisition; research execution; any endpoint / credential / `.env` / `.mcp.json` / MCP / Graphify use. The four Phase 4bm-W caveats are carried forward as constraints: (1) envelope-terminal censoring asymmetry (857 rows, all in test); (2) 538 embargo-excluded earlier-split rows; (3) approximate-quantile method (descriptive only); (4) historical `diagnostics_authorized=false` manifest flag (authorization is operator-prompt-driven, not manifest-mutation-driven; Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved).

## 22. Decision

`RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION`.

## 23. Rationale for the chosen decision

All twenty-one design criteria A–U (§7) pass on current repo evidence:

- Phase 4bm-Z completed and merged the docs-only ML-readiness evaluation memo (criteria A–R PASS) and recommended ML-baseline implementation scoping/design (A, B).
- The full implementation boundary (§8–§20) is specifiable declaratively without training, scoring, predicting, selecting, ranking, tuning, or running anything (C, J, K, L, M, O, R).
- The target framing is fixed from the existing label schema without touching the test holdout (D); horizon inclusion/deferral (15s/60s in, 1s/5s deferred) declares no horizon strategy-ready or live-tradable (E); train/validation/test handling restates and can enforce the Phase 4bm-U split policy with the test holdout sealed (F, and the holdout protection from Phase 4bm-W/Z carried forward); censored-row handling is defined per horizon (G).
- The feature surface is frozen to the 45 computed v002 columns by a deterministic rule derived from manifest evidence, with `feature_config_hash` preserved and no new engineering, selection, or ranking (H); transforms are train-only (I); baseline families are fixed a priori with no result-based selection and gradient boosting deferred with justification (J); metrics, calibration, and cost-aware evaluation are descriptive-only and uncomputed here (K, L, M); outputs are local/gitignored (N); the future test suite is specified (O); anti-drift boundaries are explicit (P).
- No diagnostics were rerun (Q); no ML/strategy/backtest work occurred (R); no manifest or successor-state mutation occurred (S); nothing under `data/` was committed (T); and all retained verdicts and project locks remain unchanged (U).

Because every criterion passes and the design defines a conservative, reproducible, leakage-controlled, result-selection-free first baseline that trains and runs nothing in this phase, the appropriate recommendation is to authorize — separately and in a future phase — an ML-baseline implementation phase that implements *exactly* this design. No prerequisite is missing and no drift was detected, so neither `DEFER_ML_BASELINE_IMPLEMENTATION_PENDING_SPECIFIC_DESIGN_REMEDIATION` nor `DO_NOT_RECOMMEND_ML_BASELINE_IMPLEMENTATION` is warranted. The recommendation is a *recommendation only*; it does not itself authorize any implementation, any ML, or any execution.

**`RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION` means only:** a future, separately authorized implementation phase may implement exactly the Phase 4bn-A design. It does **not** authorize implementation in Phase 4bn-A, model training in Phase 4bn-A, any successor execution by itself, or strategy / signals / PnL simulation / backtests / acquisition / paper / shadow / live-readiness / exchange-write.

## 24. What a future ML-baseline implementation phase would be allowed to implement, if separately authorized

A future, separately authorized **ML-baseline implementation** phase (provisionally `Phase 4bn-B`, **not** authorized here) would be permitted to implement *exactly* this design:

- direction-classification baselines (3-class `{-1,0,+1}`) on the **15s and 60s** horizons only;
- trained on the **train** split, evaluated on the **validation** split, with the **test holdout sealed**;
- using the frozen **45-column v002 computed feature matrix** (`feature_config_hash 819cfa7a…` preserved), with the 17 lineage columns, labels, and split flags excluded;
- with **train-only** transform fitting and **validation-only** calibration evaluation;
- the **fixed a-priori baseline families** of §15 (majority/prior, naive persistence, (regularized) multinomial logistic regression, regularized linear classifier, optionally one bounded shallow tree), each run once with pre-declared settings; **no search; no result-based selection**;
- the **descriptive ML metrics** of §16 and the **§11.6-locked cost-commensurability** summary of §18;
- **per-horizon censored-row masking** (§12) and **Phase 4bm-U split-policy enforcement** (§11);
- **local gitignored outputs only** (§19) with canonical Phase 4bb-F sidecars;
- the **test suite** of §20.

Possible future module / script / test names the implementation phase *might* create (named here for design continuity; **not created by Phase 4bn-A**):

- modules: `src/prometheus/research/microstructure/ml_baseline_design_v002.py`, `ml_baseline_dataset_v002.py`, `ml_baseline_models_v002.py`, `ml_baseline_metrics_v002.py`, `ml_baseline_report_v002.py`;
- script: `scripts/phase4bn_b_run_ml_baseline_v002.py`;
- tests: `tests/research/microstructure/test_ml_baseline_dataset_v002.py`, `test_ml_baseline_split_policy_v002.py`, `test_ml_baseline_no_leakage_v002.py`, `test_ml_baseline_no_network.py`, `test_ml_baseline_outputs_v002.py`.

A future ML-baseline implementation phase **must not**: tune hyperparameters; tune thresholds; select models through results; rank or select features; design strategy; generate signals; simulate PnL; run backtests; run walk-forward optimization; use the test holdout for tuning/design; materialize reusable split masks unless separately authorized; mutate manifests or successor-state artefacts; or acquire data. It would require its own separately authorized operator prompt, its own branch, its own implementation report + closeout, and (separately) a Tier 1 merge-closeout. **Any ML-baseline implementation requires a separately authorized implementation phase.**

## 25. What this phase does not authorize

Phase 4bn-A defines an ML-baseline implementation design and a single governance recommendation only. It does **not**, and **cannot**, authorize:

- any ML-baseline implementation phase (it only *recommends* that one may be separately authorized); any ML training / model scoring / prediction generation; any diagnostics rerun; any new diagnostic artefact; any ML artefact; any split-mask materialization (reusable or otherwise);
- any feature ranking / feature selection / model-family selection through results / hyperparameter tuning / threshold tuning / meta-labeling; any strategy specification / implementation / signal construction; any PnL simulation / backtest / walk-forward optimization;
- any use of the test window for tuning or design; any eligibility rescue;
- any mutation of any manifest, the Phase 4bm-S successor-state artefact, the Phase 4bm-U successor-state artefact, the Phase 4bm-Q gate report, or any other `data/microstructure/` or `data/research/` artefact;
- any change to `chronological_split_policy`, `research_eligible`, `eligibility_gate_status`, `diagnostics_authorized`, or `ml_authorized` on any on-disk manifest;
- any data acquisition (no additional days / symbols / data families beyond the locked 90-day v002 envelope; no mark-price / order-book / funding / OI / liquidation / cross-venue / additional aggTrades);
- any public / authenticated / private endpoint call; any WebSocket / user-stream; any credential / `.env` / `.mcp.json` / MCP / Graphify use;
- Phase 4bn-B or any successor phase; Phase 5; Phase 4 canonical; paper / shadow; live-readiness; deployment; exchange-write; production-key creation;
- any revision of a retained verdict, any loosening of a project lock, or any amendment of M0 / Phase 4al / Phase 4aw / Phase 4bb-F / Phase 4bl-F / Phase 4bm-A-P1 / Phase 4bm-D-P1.

**Phase 4bn-A is a docs-only / design-only ML-baseline implementation scoping phase.** **Phase 4bn-A does not train ML models.** **Phase 4bn-A does not run ML.** **Phase 4bn-A does not score models.** **Phase 4bn-A does not generate predictions.** **Phase 4bn-A does not select models through results.** **Phase 4bn-A does not rank or select features.** **Phase 4bn-A does not tune hyperparameters.** **Phase 4bn-A does not tune thresholds.** **Phase 4bn-A does not define or run strategy.** **Phase 4bn-A does not generate signals.** **Phase 4bn-A does not simulate PnL.** **Phase 4bn-A does not run backtests.** **Phase 4bn-A does not authorize acquisition.** **Phase 4bn-A does not authorize research execution.** **Phase 4bn-A does not create ML artefacts.** **Phase 4bn-A does not create diagnostic artefacts.** **Phase 4bn-A does not create reusable split masks.** **Phase 4bn-A does not use the test holdout for tuning or design.** **Phase 4bn-A does not mutate any manifest.** **Phase 4bn-A does not mutate any successor-state artefact.** **Phase 4bn-A does not commit data/microstructure.** **Phase 4bn-A does not commit data/research.** **Any ML-baseline implementation requires a separately authorized implementation phase.** **Phase 4bn-B is not authorized by Phase 4bn-A.**

## 26. Retained verdicts preserved

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

All prior phase results (Phase 4am .. Phase 4bm-Z) preserved verbatim.

## 27. Project locks preserved

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
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (never invoked by Phase 4bn-A)
- Phase 4bb-F canonical sidecar / path policy
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks
- Phase 4bm-A-P1 thin-prompt context-management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace standard

## 28. Recommended next state

**Remain paused.** Phase 4bn-A is branch-complete only by this work. Per the Phase 4bk-A workflow standard, it is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1). The design decision is `RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION`; this is a recommendation only and authorizes nothing. **Any ML-baseline implementation requires a separately authorized implementation phase.** **Phase 4bn-B is not authorized by Phase 4bn-A.** **Recommended state remains paused.**
