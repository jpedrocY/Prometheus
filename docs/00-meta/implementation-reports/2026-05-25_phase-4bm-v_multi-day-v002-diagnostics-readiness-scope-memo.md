# Phase 4bm-V — Multi-Day V002 Diagnostics Readiness and Scope Memo

**Phase identity:** Phase 4bm-V — Multi-Day V002 Diagnostics Readiness and Scope Memo (docs-only governance / methodology memo; first phase after the multi-day v002 label-family research-use successor-state and chronological split-policy successor-state recordings to evaluate whether a future diagnostics phase may be proposed).
**Date:** 2026-05-25.
**Branch:** `phase-4bm-v/multi-day-v002-diagnostics-readiness-scope-memo`.
**Base SHA:** `main` at `dbb9ce92ab002b0adef11fdd51556617ae222e99` (Phase 4bm-U merge-closeout SHA-finalization commit `docs(phase-4bm-u): finalize merge closeout shas`; pre-branch `main == origin/main` verified in sync).
**Tier:** **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 escalation rules. This is the first phase after the multi-day v002 label-family research-use and chronological split-policy successor-state recordings that evaluates whether diagnostics may be proposed; it is adjacent to research execution, ML, strategy, and backtests but does not authorize any of them, so it escalates to Tier 1.
**Phase type:** docs-only governance / methodology memo. Adds two new tracked docs files under `docs/00-meta/implementation-reports/` (this memo + the paired closeout) and narrowly updates `docs/00-meta/current-project-state.md`. **No** source / test / committed-script / configuration / manifest / sidecar / gate-report / successor-state mutation. **No** local data artefact created. **No** gate rerun. **No** acquisition. **No** successor authorization.
**Status:** drafted; pending operator review. Branch-complete only by this work; not merged into `main`; not project-complete.

---

## 1. Required exact phrases

- **Phase 4bm-V is a docs-only diagnostics readiness and scope memo.**
- **Phase 4bm-V does not run diagnostics.**
- **Phase 4bm-V does not run ML.**
- **Phase 4bm-V does not define or run strategy.**
- **Phase 4bm-V does not run backtests.**
- **Phase 4bm-V does not authorize acquisition.**
- **Phase 4bm-V does not authorize research execution.**
- **Phase 4bm-V does not create diagnostic artefacts.**
- **Phase 4bm-V does not mutate any manifest.**
- **Phase 4bm-V does not mutate any successor-state artefact.**
- **Phase 4bm-V does not commit data/microstructure.**
- **Any diagnostics execution requires a separately authorized diagnostics phase.**
- **Phase 4bm-W is not authorized by Phase 4bm-V.**
- **Recommended state remains paused.**

---

## 2. Phase identity

This memo answers a single governance question:

> Given the multi-day v002 feature/label family `microstructure_labels_aggtrades_v001 @ v002` (BTCUSDT × 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 rows; 4 horizons 1s / 5s / 15s / 60s) is research-use approved **in principle** through the sibling Phase 4bm-S successor-state artefact (`LABEL_FAMILY_RESEARCH_USE_APPROVED_IN_PRINCIPLE`) and now carries a machine-readable chronological split-policy successor-state (Phase 4bm-U `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`), what diagnostics, if any, may be proposed next, under what constraints, and what remains forbidden?

Phase 4bm-V is **docs-only**. It records a diagnostics readiness determination and a diagnostics scope envelope at policy / governance level. It does not run any diagnostic, does not materialize any split mask, does not create any diagnostic artefact, does not mutate any manifest or successor-state artefact, does not run ML / strategy / backtests, does not acquire data, and does not authorize any successor implementation. **Phase 4bm-V is a docs-only diagnostics readiness and scope memo.** **This phase is not diagnostics execution. This phase is not ML. This phase is not strategy research. This phase is not backtesting. This phase is not split-mask materialization. This phase is not acquisition.**

- **Phase name:** Phase 4bm-V — Multi-Day V002 Diagnostics Readiness and Scope Memo.
- **Phase type:** docs-only governance / methodology memo.
- **Branch:** `phase-4bm-v/multi-day-v002-diagnostics-readiness-scope-memo`.
- **Base SHA:** `main` at `dbb9ce92ab002b0adef11fdd51556617ae222e99`.
- **Predecessor anchor:** Phase 4bm-U merge commit `af18a207ee7f53b1b3bd67e59348bfb4b3b0da31` + merge-closeout commit `be87cc8044e3ff1c234635ad4d55f109595c0e99` + SHA-finalization commit `dbb9ce92ab002b0adef11fdd51556617ae222e99` (project-complete on `main`).
- **Authorization:** explicit operator authorization for Phase 4bm-V only.

---

## 3. Branch name

`phase-4bm-v/multi-day-v002-diagnostics-readiness-scope-memo`

## 4. Base SHA

`dbb9ce92ab002b0adef11fdd51556617ae222e99` (Phase 4bm-U merge-closeout SHA-finalization commit, `docs(phase-4bm-u): finalize merge closeout shas`; the head of `main` at branch time; `main == origin/main` verified in sync). The Phase 4bm-U branch tip before merge `11e01f3ceb472225d35d43137df9244f99145e13`, merge commit `af18a207ee7f53b1b3bd67e59348bfb4b3b0da31`, and merge-closeout commit `be87cc8044e3ff1c234635ad4d55f109595c0e99` are present on `main` immediately below this SHA-finalization commit (verified by `git log --oneline -14 --decorate`).

## 5. Predecessor chain

| Phase | Role | Status on `main` | Verdict / result |
| --- | --- | --- | --- |
| **Phase 4bm-M** | Multi-day v002 label-family boundary / design memo | merge-complete | label-boundary + multi-day horizon / envelope / leakage policy defined at memo level |
| **Phase 4bm-N** | Multi-day v002 label schema finalization memo | merge-complete | 40-column v002 label schema locked at memo level |
| **Phase 4bm-O** | Multi-day v002 label kernel implementation + local label artefact generation | merge-complete | 90 per-day label parquets + 90 sidecars + 1 manifest + 1 manifest sidecar; all gitignored |
| **Phase 4bm-P** | Multi-day v002 label artefact structural QA memo | merge-complete | `LABEL_STRUCTURAL_QA_PASS` |
| **Phase 4bm-Q** | Multi-day v002 label-family eligibility gate design / implementation / execution | merge-complete | `LABEL_GATE_PASS`; 60 / 60 PASS; report-level only |
| **Phase 4bm-R** | Multi-day v002 label-family research-use decision memo | merge-complete | `RECOMMEND_LABEL_RESEARCH_USE_AUTHORIZATION` |
| **Phase 4bm-S** | Multi-day v002 label-family research-use successor-state recording | merge-complete; SHA-finalized | `LABEL_FAMILY_RESEARCH_USE_APPROVED_IN_PRINCIPLE` |
| **Phase 4bm-T** | Multi-day v002 chronological split-policy memo | merge-complete; SHA-finalized | `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` (memo-level) |
| **Phase 4bm-U** | Multi-day v002 chronological split-policy successor-state recording | merge-complete; SHA-finalized | `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` (split_policy_status `recorded`) |

Phase 4bm-U lifecycle SHAs (verified present on `main`): base SHA `f7c8cb674bc08925df8e5f5765008cc92a403d08`; branch tip before merge `11e01f3ceb472225d35d43137df9244f99145e13`; merge commit `af18a207ee7f53b1b3bd67e59348bfb4b3b0da31`; merge-closeout commit `be87cc8044e3ff1c234635ad4d55f109595c0e99`; SHA-finalization commit `dbb9ce92ab002b0adef11fdd51556617ae222e99` (latest finalized `main` state and this phase's base).

The chain is internally consistent. Each phase preserves the upstream artefacts byte-identically. No verdict has been revised. No project lock has been loosened.

## 6. Evidence reviewed

### 6.1 V002 predecessor evidence (docs)

- Phase 4bm-U successor-state report `2026-05-25_phase-4bm-u_multi-day-v002-chronological-split-policy-successor-state.md`, closeout, and merge-closeout.
- Phase 4bm-T chronological split-policy memo `2026-05-25_phase-4bm-t_multi-day-v002-chronological-split-policy-memo.md`, closeout, and merge-closeout.
- Phase 4bm-S research-use successor-state report `2026-05-25_phase-4bm-s_multi-day-v002-label-family-research-use-successor-state.md`, closeout, and merge-closeout.
- Phase 4bm-R research-use decision memo `2026-05-25_phase-4bm-r_multi-day-v002-label-family-research-use-decision-memo.md`, closeout, and merge-closeout.
- Phase 4bm-Q eligibility-gate report `2026-05-25_phase-4bm-q_multi-day-v002-label-family-eligibility-gate.md`, closeout, and merge-closeout (60 / 60 PASS; report-level only).
- Phase 4bm-P structural QA memo `2026-05-18_phase-4bm-p_multi-day-v002-label-artefact-structural-qa-memo.md` and merge-closeout (`LABEL_STRUCTURAL_QA_PASS`).
- Phase 4bm-O label kernel / local artefacts report `2026-05-18_phase-4bm-o_multi-day-v002-label-kernel-local-artefacts.md`.
- Phase 4bm-N label schema finalization `2026-05-18_phase-4bm-n_multi-day-v002-label-schema-finalization.md`.
- Phase 4bm-M label-family boundary design memo `2026-05-18_phase-4bm-m_multi-day-v002-label-family-boundary-design-memo.md` (multi-day horizon / boundary / envelope-terminal censoring / timestamp / leakage policy).
- Feature-family chain `2026-05-18_phase-4bm-l_…` / `2026-05-18_phase-4bm-k_…` / `2026-05-18_phase-4bm-j_…`.
- `docs/00-meta/current-project-state.md` (current-phase narrative and project locks).

### 6.2 Governance / process artefacts reviewed

- `docs/00-meta/process/merge-closeout-standard.md` (Tier 1 merge-closeout ceremony — applies to a future, separately authorized merge phase, not to this branch work).
- `docs/00-meta/process/phase-risk-tiering-standard.md` (§3 escalation; reusable non-authorization blocks).
- `2026-05-17_phase-4bm-a-p1_context-management-standard.md` (thin-prompt context-management standard; honored).
- `2026-05-17_phase-4bm-d-p1_lightweight-claude-code-workspace-standard.md` (lightweight Claude Code workspace standard; honored).

### 6.3 Local-evidence verification (read-only)

All key governed evidence artefacts and both successor-state pairs were re-hashed read-only at the start of this phase and matched their expected values byte-for-byte; all remain gitignored under `.gitignore:85: data/microstructure/` and do not appear in `git status`.

| Artefact | Expected SHA256 | Result |
| --- | --- | --- |
| Phase 4bm-U split-policy successor-state JSON | `6834ab11a5ac5d93b4d9f14d9b71ef3acb2a279bd8e3189fd22421598675fc9c` | MATCH (gitignored) |
| Phase 4bm-U split-policy successor-state sidecar | `fa9ae709add4541111e70cfc03d9126ac40f136ea2ce1aa1abe299d3412ac0b6` | MATCH (gitignored) |
| Phase 4bm-S research-use successor-state JSON | `081730006c11360692db0a99d59a0ed499f762ef4f86d6e29bdf3016550abfe7` | MATCH (gitignored) |
| Phase 4bm-S research-use successor-state sidecar | `05597fe4d568f5644ad9acc914f8a3b429bc7984cf7df3a2ac3f8c7935e02551` | MATCH (gitignored) |
| v002 label manifest | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` | MATCH |
| v002 label manifest sidecar | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` | MATCH |
| Phase 4bm-Q gate report | `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` | MATCH |
| Phase 4bm-Q gate report sidecar | `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` | MATCH |

`git check-ignore -v` confirms both Phase 4bm-U successor-state files are covered by `.gitignore:85: data/microstructure/`; neither appears in `git status`. Label parquet / sidecar counts independently verified on disk at **90 / 90**.

## 7. Dataset identity

| Item | Value |
| --- | --- |
| `family_id` | `microstructure_labels_aggtrades_v001` |
| `dataset_version` | `v002` |
| `label_schema_version` | `v001` (Phase 4bm-N locked 40-column v002 label schema) |
| `symbol` | `BTCUSDT` (one symbol) |
| Date range | 2024-12-01 .. 2025-02-28 inclusive |
| Date count | 90 contiguous UTC dates |
| Partition count (per-day label parquets) | 90 |
| Sidecar count (canonical Phase 4bb-F) | 90 |
| Total rows | 155,153,449 |
| Horizons | 1s / 5s / 15s / 60s |
| Maximum forward horizon | 60s |
| Per-horizon censored counts | `{1s: 14, 5s: 39, 15s: 170, 60s: 634}` |
| `invalid_price_row_count` | 0 |
| Envelope terminal | `1740787199996` ms UTC (2025-02-28 23:59:59.996Z) |
| `label_config_hash` | `352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560` |
| `feature_config_hash` | `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d` |
| Label manifest SHA256 | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` |
| Label manifest sidecar SHA256 | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` |
| Phase 4bm-S research-use successor-state SHA256 | `081730006c11360692db0a99d59a0ed499f762ef4f86d6e29bdf3016550abfe7` |
| Phase 4bm-U split-policy successor-state SHA256 | `6834ab11a5ac5d93b4d9f14d9b71ef3acb2a279bd8e3189fd22421598675fc9c` |
| Current manifest `chronological_split_policy` | `"not_yet_defined"` (unchanged; the recorded policy lives only in the Phase 4bm-U sibling successor-state JSON) |

## 8. Chronological split policy (recorded; governs any future diagnostics)

Recorded policy name: `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` (Phase 4bm-T memo-level; Phase 4bm-U `split_policy_status = "recorded"`).

| Split | UTC date window (inclusive) | Date count | Share (by date) |
| --- | --- | --- | --- |
| **Train** | 2024-12-01 .. 2025-01-14 | 45 | 50.0% |
| **Validation** | 2025-01-15 .. 2025-02-13 | 30 | 33.3% |
| **Test / final holdout** | 2025-02-14 .. 2025-02-28 | 15 | 16.7% |
| **Total** | 2024-12-01 .. 2025-02-28 | 90 | 100% |

Core split-policy rules (binding governance on any future row-level research execution): rows assigned by `source_transact_time_ms` UTC date; boundary timestamps `2025-01-15T00:00:00Z` (`T_TV`) and `2025-02-14T00:00:00Z` (`T_VT`); minimum 60-second boundary embargo (max declared horizon = 60s) at both boundaries; boundary-crossing rows excluded from the earlier split (never reassigned forward); per-row masks only (no parquet rewrite); no random / shuffled / k-fold-over-time / bootstrap / post-hoc temporal resampling split; envelope-terminal censoring at `2025-02-28 23:59:59.996Z` applies additively; test / final holdout is single-use and cannot be used for feature selection, model selection, hyperparameter selection, threshold tuning, strategy design, diagnostic iteration, or eligibility rescue.

## 9. Readiness criteria

Evaluated against repo evidence (read-only). All pass.

| # | Criterion | Result | Evidence |
| --- | --- | --- | --- |
| **A** | Multi-day v002 label family is structurally QA-passed | **PASS** | Phase 4bm-P `LABEL_STRUCTURAL_QA_PASS` |
| **B** | Multi-day v002 label-family eligibility gate passed | **PASS** | Phase 4bm-Q `LABEL_GATE_PASS`; 60 / 60 PASS; report-level only |
| **C** | Label-family research-use successor-state is recorded | **PASS** | Phase 4bm-S `LABEL_FAMILY_RESEARCH_USE_APPROVED_IN_PRINCIPLE`; JSON SHA `081730006c…` (gitignored, MATCH) |
| **D** | Chronological split-policy successor-state is recorded | **PASS** | Phase 4bm-U `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` (`recorded`); JSON SHA `6834ab11…` (gitignored, MATCH) |
| **E** | Train / validation / test windows are known | **PASS** | 45 / 30 / 15 UTC dates (§8) |
| **F** | Boundary embargo and boundary-crossing exclusion rule are known | **PASS** | minimum 60s embargo at `T_TV` / `T_VT`; boundary-crossing rows excluded from earlier split (§8) |
| **G** | Test-holdout use restrictions are known | **PASS** | single-use final holdout; seven prohibited test-window uses (§8) |
| **H** | v002 label manifest remains byte-identical and intentionally unmutated | **PASS** | manifest SHA `5e17074d…` MATCH; `chronological_split_policy = "not_yet_defined"` preserved |
| **I** | Phase 4bm-S and Phase 4bm-U successor-state artefacts are present and gitignored | **PASS** | both JSON + sidecar re-hashed MATCH; `git check-ignore` `.gitignore:85: data/microstructure/` |
| **J** | No diagnostics have yet been run | **PASS** | no diagnostic artefact exists; `git status` shows only `data/research/` (empty/untracked); no row-level research execution recorded anywhere in the chain |
| **K** | No ML / strategy / backtest authorization exists | **PASS** | every predecessor records `ml_authorized = false`, `strategy_authorized = false`, `backtest_authorized = false` |
| **L** | No data/microstructure artefact is committed | **PASS** | `git status --short` shows only `data/research/`; no `data/microstructure/` entry |
| **M** | Retained verdicts and project locks remain unchanged | **PASS** | §17–§18; preserved verbatim from Phase 4bm-U |

**All readiness criteria A–M PASS.**

## 10. Allowed diagnostics categories (for a future separately authorized phase)

Descriptive / structural only. At minimum:

1. **Dataset/split inventory diagnostics** — row counts by split and UTC date; partition counts by split; 90/90 label parquet + sidecar presence; split-date membership audit; train/validation/test date coverage.
2. **Label availability and censoring diagnostics** — per-horizon non-null / null / censored counts; envelope-terminal censoring summary; boundary-embargo exclusion estimates; horizon availability by split.
3. **Label distribution diagnostics** — forward-return distribution by horizon and split; quantiles / winsorized summaries; sign balance / threshold-free direction balance; extreme-return counts; distribution drift across train/validation/test (descriptive only — never used to select features, models, thresholds, or strategies).
4. **Feature/label alignment diagnostics** — timestamp alignment checks; row-count alignment; `source_transact_time_ms` consistency; no cross-split contamination checks; `feature_config_hash` / `label_config_hash` consistency.
5. **Per-day and per-split stability diagnostics** — per-day row-count variation; per-day label-distribution variation; missingness by day/split/horizon; censoring by day/split/horizon.
6. **Boundary-embargo and leakage-guard diagnostics** — boundary-crossing exclusion estimate; embargo rule applicability; test-holdout untouched-for-tuning guarantee; no-shuffle compliance.
7. **Missingness / nullability / value-domain diagnostics** — null/non-null counts; value-domain checks (e.g. `forward_direction ∈ {-1, 0, +1, null}`); `invalid_price_row_count` confirmation.
8. **Report-only QA summaries** — descriptive tabular/JSON summaries of the above, recorded as local gitignored research outputs only.

These are **descriptive and structural**. None of them selects, ranks, tunes, fits, trains, simulates, or designs anything.

## 11. Forbidden diagnostics categories

A future diagnostics phase must **not** do any of the following unless separately authorized later:

1. ML model training
2. Model selection
3. Feature ranking
4. Feature selection
5. Hyperparameter selection
6. Threshold tuning
7. Strategy design
8. Strategy signal generation
9. PnL simulation
10. Backtesting
11. Walk-forward optimization
12. Test-holdout-driven iteration
13. Eligibility rescue
14. Any use of the test window for tuning or design
15. Acquisition
16. Live / paper / shadow / exchange-write work

## 12. Split-policy and holdout constraints

Any future diagnostics phase, if separately authorized, must apply the Phase 4bm-U `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` policy verbatim:

- Assign rows to train / validation / test by `source_transact_time_ms` UTC date per the §8 windows.
- Honor the minimum 60-second boundary embargo at `T_TV` (`2025-01-15T00:00:00Z`) and `T_VT` (`2025-02-14T00:00:00Z`); exclude boundary-crossing rows from the earlier split; never reassign forward.
- Use per-row inclusion/exclusion masks only; never rewrite the 90 v002 label parquets.
- No random / shuffled / k-fold-over-time / bootstrap / post-hoc temporal resampling split.
- Treat envelope-terminal censoring (`2025-02-28 23:59:59.996Z`; `{1s:14, 5s:39, 15s:170, 60s:634}`) as a separate, additive structural asymmetry that any diagnostic must report rather than silently drop.
- **Test-holdout protection.** The test / final holdout window (2025-02-14 .. 2025-02-28; 15 dates) is single-use. A descriptive diagnostics phase may compute **descriptive** structural/availability/distribution summaries on the test window for reporting (e.g. row counts, censoring counts, missingness), but must **not** use the test window for feature selection, model selection, hyperparameter selection, threshold tuning, strategy design, diagnostic iteration, or eligibility rescue. No diagnostic finding on the test window may be fed back into any selection, tuning, or design loop. Any tuning-style read of the test window burns the holdout and invalidates its evidentiary value.

## 13. Local-output constraints for any future diagnostics phase

If separately authorized, a future diagnostics phase:

- reads local gitignored feature/label artefacts (the 90 v002 label parquets + sidecars, the v002 label manifest, and — read-only — the Phase 4bm-S / Phase 4bm-U successor-state JSON + sidecars);
- applies the Phase 4bm-U split policy via per-row masks;
- produces local gitignored diagnostic tables/reports under `data/research/` or another approved gitignored research-output namespace;
- does not commit diagnostic outputs unless the repo standard says otherwise;
- does not read credentials; does not read or create `.env` / `.mcp.json`; does not enable MCP / Graphify;
- does not call any public / authenticated / private endpoint or open any WebSocket;
- does not mutate any manifest;
- does not mutate any successor-state JSON or sidecar;
- does not mutate the Phase 4bm-Q gate report;
- does not use the test holdout for tuning or design;
- does not train models; does not implement strategies; does not run backtests;
- preserves the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant end-to-end (never invoked).

## 14. Non-authorization boundary

This memo defines diagnostics readiness and scope only. It does **not**, and **cannot**, authorize:

- any diagnostics execution, diagnostic artefact creation, or split-mask materialization;
- any mutation of any manifest, the Phase 4bm-S successor-state artefact, the Phase 4bm-U successor-state artefact, the Phase 4bm-Q gate report, or any other `data/microstructure/` artefact;
- any change to `chronological_split_policy` on any actual on-disk manifest (it remains `"not_yet_defined"`);
- any rerun of the label gate, feature gate, label kernel, feature kernel, normalizer, or structural-QA inspector;
- any label generation, feature generation, or data acquisition (no additional days, no additional symbols, no mark-price / order-book / funding / OI / liquidation / cross-venue / aggTrades beyond the locked 90-day v002 envelope);
- any ML training / model selection / feature ranking / feature selection / hyperparameter selection / threshold tuning / meta-labeling; any strategy specification / implementation / signal construction; any PnL simulation / backtest / walk-forward optimization;
- any public / authenticated / private endpoint call; any WebSocket / user-stream; any credential / `.env` / `.mcp.json` / MCP / Graphify use;
- Phase 4bm-W or any successor phase; Phase 5; Phase 4 canonical;
- paper / shadow; live-readiness; deployment; exchange-write; production-key creation;
- any revision of a retained verdict, any loosening of a project lock, or any amendment of M0 / Phase 4al / Phase 4aw / Phase 4bb-F / Phase 4bl-F / Phase 4bm-A-P1 / Phase 4bm-D-P1.

**Phase 4bm-V does not run diagnostics.** **Phase 4bm-V does not run ML.** **Phase 4bm-V does not define or run strategy.** **Phase 4bm-V does not run backtests.** **Phase 4bm-V does not authorize acquisition.** **Phase 4bm-V does not authorize research execution.** **Phase 4bm-V does not create diagnostic artefacts.** **Phase 4bm-V does not mutate any manifest.** **Phase 4bm-V does not mutate any successor-state artefact.** **Phase 4bm-V does not commit data/microstructure.** **Any diagnostics execution requires a separately authorized diagnostics phase.** **Phase 4bm-W is not authorized by Phase 4bm-V.**

## 15. Decision

`RECOMMEND_AUTHORIZE_DESCRIPTIVE_DIAGNOSTICS_PHASE`.

## 16. Rationale for the chosen decision

All thirteen readiness criteria A–M (§9) pass on current repo evidence:

- The multi-day v002 label family is structurally QA-passed (Phase 4bm-P `LABEL_STRUCTURAL_QA_PASS`) and passed a 60 / 60 report-level eligibility gate (Phase 4bm-Q `LABEL_GATE_PASS`).
- Research-use admissibility-in-principle is recorded as a machine-readable sibling artefact (Phase 4bm-S `LABEL_FAMILY_RESEARCH_USE_APPROVED_IN_PRINCIPLE`), and the chronological split policy is recorded as a machine-readable sibling artefact (Phase 4bm-U `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`, `split_policy_status = "recorded"`).
- The train / validation / test windows, the minimum 60-second boundary embargo, the boundary-crossing exclusion rule, the no-shuffle rule, and the single-use holdout rule are all known and unambiguous.
- The v002 label manifest, both successor-state artefacts, and the Phase 4bm-Q gate report are byte-identical to their recorded SHAs and remain gitignored; no `data/microstructure/` artefact is committed.
- No diagnostics have yet been run; no ML / strategy / backtest authorization exists; all retained verdicts and project locks are preserved verbatim.

Because the upstream governance prerequisites for descriptive structural diagnostics are satisfied and intact, and because descriptive / structural diagnostics (§10) neither select, rank, tune, fit, simulate, nor design anything, the appropriate recommendation is to authorize — separately and in a future phase — a **descriptive / structural diagnostics phase only**, bounded by §10–§13. No prerequisite is missing and no drift was detected, so neither `DEFER_DIAGNOSTICS_PENDING_SPECIFIC_REMEDIATION` nor `DO_NOT_AUTHORIZE_DIAGNOSTICS` is warranted. The recommendation is a *recommendation only*; it does not itself authorize any execution.

## 17. What a future diagnostics phase would be allowed to do, if separately authorized

A future, separately authorized **descriptive multi-day v002 diagnostics phase** (provisionally a "Phase 4bm-W"-class phase, not authorized here) would be permitted to perform only the descriptive / structural diagnostics enumerated in §10, under the split-policy / holdout constraints of §12 and the local-output constraints of §13, producing only local gitignored research-output tables/reports. It would remain forbidden from everything in §11 and §14. Such a phase would require its own separately authorized operator prompt, its own branch, its own implementation report + closeout, and (separately) a Tier 1 merge-closeout. **Any diagnostics execution requires a separately authorized diagnostics phase.**

## 18. What this phase does not authorize

See §14. In summary: no diagnostics execution; no diagnostic artefact creation; no split-mask materialization; no ML / strategy / backtest / walk-forward; no manifest or successor-state or gate-report mutation; no acquisition; no research execution; no endpoint / credential / MCP / Graphify work; no successor phase; no Phase 5; no paper / shadow / live-readiness / deployment / exchange-write / production keys. **Phase 4bm-W is not authorized by Phase 4bm-V.**

## 19. Retained verdicts preserved

All preserved verbatim:

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED (per Phase 3t)
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

## 20. Project locks preserved

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
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (never invoked by Phase 4bm-V)
- Phase 4bb-F canonical sidecar / path policy
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks
- Phase 4bm-A-P1 thin-prompt context-management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace standard

All prior phase results (Phase 4am .. Phase 4bm-U) preserved verbatim.

## 21. Validation

This phase is docs-only. Validation gates applied:

1. `git diff --check` — clean (exit 0).
2. `git status --short` — only the expected pre-existing untracked `data/research/`; no `data/microstructure/` entry.
3. `git diff --name-only` (working tree) and `git diff --name-only --cached` — only the three tracked docs paths (this memo, the closeout, and the narrow `current-project-state.md` update); no source / test / committed-script / configuration path; no `data/microstructure/` path.
4. No diagnostic artefact created; no split mask created; no successor-state JSON created or mutated; no manifest modified.
5. Read-only re-hash of the Phase 4bm-U / Phase 4bm-S successor-state JSON + sidecars, the v002 label manifest + sidecar, and the Phase 4bm-Q gate report + sidecar — all eight MATCH expected SHAs byte-for-byte (§6.3).
6. `ruff` / `mypy` / `pytest` — deliberately not run; Phase 4bm-V modifies no source, no test, no committed script, no `pyproject.toml`, no `README.md`, and no `.gitignore`. The latest authoritative whole-repo validation remains the predecessor merges. No project-specific markdown-lint gate exists in this repository; none invented.

## 22. Recommended next state

**Remain paused.** Phase 4bm-V is branch-complete only by this work. Per the Phase 4bk-A workflow standard, it is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1). The diagnostics readiness decision is `RECOMMEND_AUTHORIZE_DESCRIPTIVE_DIAGNOSTICS_PHASE`; this is a recommendation only and authorizes nothing. **Any diagnostics execution requires a separately authorized diagnostics phase.** **Phase 4bm-W is not authorized by Phase 4bm-V.** **Recommended state remains paused.**
