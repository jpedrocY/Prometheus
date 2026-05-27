# Phase 4bm-X — Multi-Day V002 Descriptive Diagnostics Interpretation Memo

**Phase identity:** Phase 4bm-X — Multi-Day V002 Descriptive Diagnostics Interpretation Memo (docs-only governance / interpretation memo; the first phase after the Phase 4bm-W descriptive diagnostics execution that interprets the executed descriptive diagnostics result and evaluates whether a future ML-readiness scoping memo may be proposed).
**Date:** 2026-05-25.
**Branch:** `phase-4bm-x/multi-day-v002-descriptive-diagnostics-interpretation-memo`.
**Base SHA:** `main` at `e4067c08c88e6dd8354a15bc90e90aa55ddada39` (Phase 4bm-W merge-closeout SHA-finalization commit `docs(phase-4bm-w): finalize merge closeout shas`; pre-branch `main == origin/main` verified in sync).
**Tier:** **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3. This phase interprets the first executed descriptive diagnostics for the multi-day v002 research-use-approved-in-principle feature/label family and may influence whether an ML-readiness scoping memo may be proposed; it is adjacent to ML / strategy / backtests / acquisition / research execution but authorizes none of them, so it escalates to Tier 1.
**Phase type:** docs-only governance / interpretation memo. Adds two new tracked docs files under `docs/00-meta/implementation-reports/` (this memo + the paired closeout) and narrowly updates `docs/00-meta/current-project-state.md`. **No** source / test / committed-script / configuration / manifest / sidecar / gate-report / successor-state mutation. **No** local data artefact created or mutated. **No** diagnostic rerun. **No** acquisition. **No** successor authorization.
**Status:** drafted; pending operator review. Branch-complete only by this work; not merged into `main`; not project-complete.

---

## 0. Required exact phrases

- **Phase 4bm-X is a docs-only descriptive diagnostics interpretation memo.**
- **Phase 4bm-X does not run diagnostics.**
- **Phase 4bm-X does not run ML.**
- **Phase 4bm-X does not define or run strategy.**
- **Phase 4bm-X does not run backtests.**
- **Phase 4bm-X does not authorize acquisition.**
- **Phase 4bm-X does not authorize research execution.**
- **Phase 4bm-X does not create ML artefacts.**
- **Phase 4bm-X does not create diagnostic artefacts.**
- **Phase 4bm-X does not perform feature selection.**
- **Phase 4bm-X does not perform model selection.**
- **Phase 4bm-X does not perform threshold tuning.**
- **Phase 4bm-X does not use the test holdout for tuning or design.**
- **Phase 4bm-X does not mutate any manifest.**
- **Phase 4bm-X does not mutate any successor-state artefact.**
- **Phase 4bm-X does not commit data/microstructure.**
- **Phase 4bm-X does not commit data/research.**
- **Any ML-readiness scoping requires a separately authorized memo phase.**
- **Phase 4bm-Y is not authorized by Phase 4bm-X.**
- **Recommended state remains paused.**

---

## 1. Phase identity

Phase 4bm-X answers a single governance question:

> Given the Phase 4bm-W descriptive diagnostics verdict `DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS`, do the diagnostics support proposing a future ML-readiness scoping memo, and under what constraints?

Phase 4bm-X is **docs-only**. It interprets the already-executed, already-merged Phase 4bm-W descriptive / structural diagnostics over the multi-day v002 BTCUSDT feature/label family `microstructure_labels_aggtrades_v001 @ v002` (90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 rows; horizons 1s / 5s / 15s / 60s), under the Phase 4bm-U recorded chronological split policy `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`. It does not run any diagnostic, does not rerun Phase 4bm-W, does not create any diagnostic or ML artefact, does not materialize any split mask, does not mutate any manifest or successor-state artefact, does not run ML / strategy / backtests, does not acquire data, and does not authorize any successor implementation. **Phase 4bm-X is a docs-only descriptive diagnostics interpretation memo.** **This phase is not diagnostics execution. This phase is not ML. This phase is not strategy research. This phase is not backtesting. This phase is not feature/model/threshold selection. This phase is not acquisition.**

- **Phase name:** Phase 4bm-X — Multi-Day V002 Descriptive Diagnostics Interpretation Memo.
- **Phase type:** docs-only governance / interpretation memo.
- **Branch:** `phase-4bm-x/multi-day-v002-descriptive-diagnostics-interpretation-memo`.
- **Base SHA:** `main` at `e4067c08c88e6dd8354a15bc90e90aa55ddada39`.
- **Authorization:** explicit operator authorization for Phase 4bm-X only.

## 2. Branch name

`phase-4bm-x/multi-day-v002-descriptive-diagnostics-interpretation-memo`

## 3. Base SHA

`e4067c08c88e6dd8354a15bc90e90aa55ddada39` (Phase 4bm-W merge-closeout SHA-finalization commit, `docs(phase-4bm-w): finalize merge closeout shas`; the head of `main` at branch time; `main == origin/main` verified in sync). The Phase 4bm-W code/tests/script/`.gitignore` commit `7101357de4f2bf760e2f40c65f36e2ad9f79b59b`, docs/branch-tip commit `440b149aac010be8fdb254613683301f27c19be7`, merge commit `cd8913a273c030dd5a2e6e5e5eeab142fd1ffda4`, and merge-closeout commit `da76f8e07f2cfe6f74816cbc3892ee100bc7b94f` are present on `main` immediately below this SHA-finalization commit (verified by `git log --oneline -16 --decorate`).

## 4. Predecessor chain

| Phase | Role | Status on `main` | Verdict / result |
| --- | --- | --- | --- |
| **Phase 4bm-Q** | Multi-day v002 label-family eligibility gate design / implementation / execution | merge-complete; SHA-finalized | `LABEL_GATE_PASS`; 60 / 60 PASS; report-level only |
| **Phase 4bm-R** | Multi-day v002 label-family research-use decision memo | merge-complete; SHA-finalized | `RECOMMEND_LABEL_RESEARCH_USE_AUTHORIZATION` |
| **Phase 4bm-S** | Multi-day v002 label-family research-use successor-state recording | merge-complete; SHA-finalized | `LABEL_FAMILY_RESEARCH_USE_APPROVED_IN_PRINCIPLE` |
| **Phase 4bm-T** | Multi-day v002 chronological split-policy memo | merge-complete; SHA-finalized | `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` (memo-level) |
| **Phase 4bm-U** | Multi-day v002 chronological split-policy successor-state recording | merge-complete; SHA-finalized | `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` (`split_policy_status = "recorded"`) |
| **Phase 4bm-V** | Multi-day v002 diagnostics readiness and scope memo | merge-complete; SHA-finalized | `RECOMMEND_AUTHORIZE_DESCRIPTIVE_DIAGNOSTICS_PHASE` |
| **Phase 4bm-W** | Multi-day v002 descriptive diagnostics execution | merge-complete; SHA-finalized | `DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS` (descriptive-only) |

Direct predecessors for this memo:

- **Phase 4bm-V** — recommended (but did not authorize) a descriptive / structural diagnostics phase, bounding it to §10–§13 of that memo (decision `RECOMMEND_AUTHORIZE_DESCRIPTIVE_DIAGNOSTICS_PHASE`). All thirteen readiness criteria A–M passed on repo evidence.
- **Phase 4bm-W** — the separately authorized execution of those descriptive / structural diagnostics. Verdict `DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS`: 0 blocking structural failures; 4 non-blocking caveats. Merge-complete, SHA-finalized, project-complete on `main`.

Phase 4bm-W lifecycle SHAs (verified present on `main`): base SHA `348d8a34f45b8d3b5e1caa19ab8e0064a9015474`; code/tests/script/`.gitignore` commit `7101357de4f2bf760e2f40c65f36e2ad9f79b59b`; docs/branch-tip commit `440b149aac010be8fdb254613683301f27c19be7`; merge commit `cd8913a273c030dd5a2e6e5e5eeab142fd1ffda4`; merge-closeout commit `da76f8e07f2cfe6f74816cbc3892ee100bc7b94f`; SHA-finalization commit `e4067c08c88e6dd8354a15bc90e90aa55ddada39` (latest finalized `main` state and this phase's base).

The chain is internally consistent. Each phase preserves the upstream artefacts byte-identically. No verdict has been revised. No project lock has been loosened.

## 5. Evidence reviewed

### 5.1 Phase 4bm-W execution evidence (docs)

- Phase 4bm-W implementation report `2026-05-25_phase-4bm-w_multi-day-v002-descriptive-diagnostics.md` (verdict, eight diagnostic groups, split-policy application, embargo, censoring, distribution, alignment, missingness, holdout protection).
- Phase 4bm-W merge-closeout `2026-05-25_phase-4bm-w_merge-closeout.md` (full 16-section structure; the accurate re-verified pytest count **33 passed**; upstream immutability table).
- Phase 4bm-W closeout `2026-05-25_phase-4bm-w_closeout.md`.

### 5.2 Predecessor governance / methodology evidence (docs)

- Phase 4bm-V readiness/scope memo `2026-05-25_phase-4bm-v_multi-day-v002-diagnostics-readiness-scope-memo.md`, closeout, and merge-closeout (allowed/forbidden diagnostics categories §10–§11; split-policy/holdout constraints §12; local-output constraints §13).
- Phase 4bm-U chronological split-policy successor-state report, closeout, and merge-closeout.
- Phase 4bm-T chronological split-policy memo, closeout, and merge-closeout.
- Phase 4bm-S label-family research-use successor-state report, closeout, and merge-closeout.
- Phase 4bm-R label-family research-use decision memo, closeout, and merge-closeout.
- Phase 4bm-Q label-family eligibility-gate report, closeout, and merge-closeout (60 / 60 PASS; report-level only).
- Phase 4bm-P multi-day v002 label artefact structural QA memo and merge-closeout (`LABEL_STRUCTURAL_QA_PASS`).

### 5.3 Governance / process artefacts reviewed

- `docs/00-meta/process/merge-closeout-standard.md` (Tier 1 merge-closeout ceremony — applies to a future, separately authorized merge phase, not to this branch work).
- `docs/00-meta/process/phase-risk-tiering-standard.md` (§3 escalation; reusable non-authorization blocks).
- `2026-05-17_phase-4bm-a-p1_context-management-standard.md` (thin-prompt context-management standard; honored).
- `2026-05-17_phase-4bm-d-p1_lightweight-claude-code-workspace-standard.md` (lightweight Claude Code workspace standard; honored).
- `docs/00-meta/current-project-state.md` (current-phase narrative and project locks).

### 5.4 Local-evidence verification (read-only)

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

`git check-ignore -v` confirms the diagnostic outputs are covered by `.gitignore:88: data/research/`; neither the diagnostic outputs nor any `data/microstructure/` artefact appears as a staged or committed change. This memo reads all evidence read-only and reruns nothing.

## 6. Diagnostic verdict

`DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS` (Phase 4bm-W).

This verdict is **descriptive-only**. It is **not** an ML-readiness, strategy-readiness, or backtest-readiness signal. Phase 4bm-X does not change, re-derive, or re-issue this verdict; it interprets it.

## 7. Blocking failure review

**0 blocking structural failures.** Every structural and alignment violation counter in the Phase 4bm-W summary aggregates to zero: `censor_rule_mismatch = 0`, `censored_row_not_null = 0`, `direction_domain_violation = 0`, `direction_sign_mismatch_vs_return = 0`, `any_censored_flag_mismatch = 0`, `row_index_violation = 0`, `src_ne_feature_ts = 0`, `out_of_partition_day = 0`, `split_assignment_mismatch = 0`, `invalid_price_row_count = 0`, plus `symbol` / `dataset_version` / `label_config_hash` constancy and all six feature/label alignment fields. No structural impossibility, no schema violation, no leakage-guard breach, and no alignment defect was found. The absence of blocking failures is the precondition that distinguishes a `..._PASS_WITH_CAVEATS` verdict from a defer or do-not-recommend posture.

## 8. Caveat interpretation

Four non-blocking caveats were recorded by Phase 4bm-W. None is a structural defect; each is a *descriptive property of the dataset under the recorded split policy* that any future scoping memo must carry forward as a stated constraint rather than a blocker.

1. **Envelope-terminal censoring asymmetry (857 censored rows, all in the test split).** Per-horizon censored counts `{1s:14, 5s:39, 15s:170, 60s:634}` observed exactly match the recorded v002 manifest expectation (total 857). All censoring falls on the final envelope day (2025-02-28; envelope terminal `1740787199996` ms = 2025-02-28 23:59:59.996Z), which lands entirely inside the test / final holdout. Train and validation have zero censored rows. **Interpretation:** this is a known, expected, additive structural asymmetry — labels at the largest horizons are not computable past the envelope terminal. It is fully characterized, concentrated, and predictable; it is *not* missingness of unknown origin and *not* a defect. It is admissible for a scoping memo provided the scoping memo (a) declares horizon-availability-by-split as a constraint, (b) requires the future implementation to treat censored rows as label-unavailable (not as a class or a zero), and (c) keeps censoring on the test window out of any tuning/design loop (it is descriptive only). It does **not** require remediation before a scoping memo.

2. **538 embargo-excluded earlier-split rows.** The minimum 60-second boundary embargo (sized to the maximum declared horizon, 60s) at `T_TV = 2025-01-15T00:00:00Z` (train embargo 248) and `T_VT = 2025-02-14T00:00:00Z` (validation embargo 290) excludes 538 earlier-split rows total (test split embargo 0). Exclusion is via per-row mask only; the 90 v002 label parquets are never rewritten. **Interpretation:** this is the *intended* leakage-control behavior of the Phase 4bm-U split policy, not a data problem. 538 of 155,153,449 rows (≈ 3.5e-6 of the corpus) is negligible in magnitude and does not threaten train/validation/test viability. It is admissible for a scoping memo provided the scoping memo restates the embargo rule (exclude boundary-crossing rows from the earlier split; never reassign forward; per-row masks only). It does **not** require remediation before a scoping memo.

3. **Approximate-quantile method.** Forward-return quantiles were computed with a fixed-width histogram (range ±0.02, bin width 1e-05); exact additive moments (mean / std / min / max) are **not** approximate. **Interpretation:** the approximation pertains only to descriptive distribution reporting, which is never used for selection / tuning / design and was the explicitly permitted descriptive scope of Phase 4bm-W. A scoping memo does not depend on exact quantiles; if a future *separately authorized* ML-baseline phase ever needed exact quantiles, it could recompute them exactly. This is a known precision caveat on a report field, not a structural defect, and does **not** require remediation before a scoping memo.

4. **`diagnostics_authorized=false` historical manifest flag.** The v002 label/feature manifests carry a historical `diagnostics_authorized=false` flag that predates Phase 4bm-W; authorization for the diagnostics derived from the Phase 4bm-W operator prompt, not from manifest mutation, and the manifests were left byte-identical (`5e17074d…` / `512a0a54…`). **Interpretation:** this is consistent with the project's deliberate separation of governance state from on-disk artefacts — authorization is operator-driven and recorded in docs/successor-state, never by silently flipping a manifest flag. The flag's value is therefore *expected* and *correct as-is*; it should not be mutated by this phase or by any scoping memo. It does **not** require remediation; any future change to a manifest authorization flag would itself require its own separately authorized phase and must honor the Phase 4aw `flip_research_eligible(...)` always-raises invariant.

**Net caveat interpretation:** all four caveats are understood, bounded, and expected; none is a blocking structural failure; none requires remediation *before* an ML-readiness scoping memo may be proposed. Each must, however, be carried forward as an explicit stated constraint inside any future scoping memo.

## 9. Split-policy interpretation

The Phase 4bm-U `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` policy was applied verbatim by Phase 4bm-W; rows assigned by `source_transact_time_ms` UTC date.

| Split | UTC dates (inclusive) | Partitions | Rows (observed) |
| --- | --- | --- | --- |
| Train | 2024-12-01 .. 2025-01-14 | 45 | 74,535,688 |
| Validation | 2025-01-15 .. 2025-02-13 | 30 | 56,819,939 |
| Test / final holdout | 2025-02-14 .. 2025-02-28 | 15 | 23,797,822 |
| **Total** | 2024-12-01 .. 2025-02-28 | **90** | **155,153,449** |

**Interpretation:** observed total equals expected (155,153,449); `out_of_partition_day = 0` and `split_assignment_mismatch = 0` confirm each row's UTC date equals its partition date, so split assignment is unambiguous. The chronological ordering (train earliest, test latest) is leakage-correct; no shuffle / random / k-fold-over-time / bootstrap / post-hoc resampling was used. **Embargo effect:** 538 earlier-split rows excluded (train 248, validation 290, test 0) by per-row mask only — negligible and intended (§8.2). **Test-holdout handling:** the 15-date final holdout was summarized **descriptively only** (row counts, censoring, missingness, distribution descriptors) and was **not** used for feature selection, model selection, hyperparameter selection, threshold tuning, strategy design, diagnostic iteration, or eligibility rescue; the summary `holdout_protection` block records all such uses as protected/false. This split policy is well-specified, leakage-correct, and able to govern future ML scoping.

## 10. Label availability / censoring interpretation

Per-horizon censored counts observed `{1s:14, 5s:39, 15s:170, 60s:634}` (total 857) match the recorded v002 manifest expectation exactly; all 857 fall in the test split (train/validation 0). Censored-row null discipline holds everywhere: per split×horizon the null forward-return count equals the censored count (`censored_row_not_null = 0`), and `label_any_censored_flag == OR(horizon_censored_flag_*)` everywhere (`any_censored_flag_mismatch = 0`). **Interpretation:** label availability is fully understood — labels are available for all rows except the small, characterized, envelope-terminal-censored set at the largest horizons on the final day. Missingness equals censoring (no unexplained nulls). This is a clean, predictable availability profile suitable for ML-readiness scoping, provided the scoping memo treats censored rows as label-unavailable and declares horizon availability by split.

## 11. Label distribution interpretation

Forward-log-return exact additive moments (mean / std / min / max) and direction balance were recorded per split×horizon (descriptive only). Standard deviation grows monotonically with horizon within each split (e.g. train 1s std 2.44e-04 → train 60s std 1.58e-03); the zero-return mass shrinks with horizon (train 1s zero = 6,410,923 → train 60s zero = 143,672); means are small and positive at the scales shown. **Interpretation:** these are physically plausible, internally consistent microstructure return distributions — heavier dispersion at longer horizons, fewer exact-zero ticks at longer horizons — with no degeneracy (no all-zero horizon, no constant column, no impossible sign structure). Quantiles are approximate (§8.3) but moments are exact. No distribution descriptor was used to select features, models, thresholds, or strategies, and none is used here. The distributions reveal **no structural impossibility** for ML-readiness scoping. (Distribution shape is descriptive context only; it is not, and must not be read as, evidence of predictability, edge, or strategy viability.)

## 12. Feature/label alignment interpretation

Across all 90 days: `row_count_mismatch_days = 0`, `row_index_mismatch = 0`, `agg_trade_id_mismatch = 0`, `feature_timestamp_mismatch = 0`, `source_transact_time_mismatch = 0`, `feature_config_hash_mismatch_days = 0`, and `src_ne_feature_ts = 0` (`source_transact_time_ms == feature_timestamp_ms` for every row). Feature `feature_config_hash` is constant (`819cfa7a…`); label `label_config_hash` is constant (`352bad41…`). **Interpretation:** the label family is in **strict 1:1 row alignment** with the v002 feature family — 155,153,449 rows each, per-day parity (90 label parquets/sidecars ↔ 90 feature parquets/sidecars) — joined on a stable, verified key. This is the single most important precondition for any supervised-learning framing: features and labels are unambiguously paired with no row drift, no key collision, and no cross-split contamination. Alignment is fully satisfied.

## 13. Per-day / per-split stability interpretation

Per-day row counts vary across the 90 days with no zero-row day; per-day censoring is zero on every non-final day and concentrated entirely on 2025-02-28; missingness equals censoring everywhere; all per-day structural counters aggregate to 0. **Interpretation:** the corpus is structurally stable day-over-day — no missing partition, no empty day, no per-day anomaly — and the only concentrated irregularity (final-day censoring) is the known, expected envelope-terminal effect already interpreted in §8.1/§10. This stability supports, rather than blocks, scoping.

## 14. Missingness / value-domain interpretation

`forward_direction_H ∈ {-1, 0, +1, null}` on all rows (`direction_domain_violation = 0`); the sign of each non-null forward return matches its non-null direction (`direction_sign_mismatch_vs_return = 0`); the per-row censor rule `horizon_censored_flag_H == (source_transact_time_ms + H_ms > envelope_terminal_unix_ms)` holds everywhere (`censor_rule_mismatch = 0`); `row_index` is contiguous `0..n-1` per partition (`row_index_violation = 0`); `invalid_price_row_count = 0`; symbol / dataset_version constancy holds. **Interpretation:** every value-domain and nullability check passed. There are no out-of-domain values, no contradictory direction/return signs, no invalid prices, and no unexplained missingness. Value-domain integrity is fully satisfied.

## 15. Validation discrepancy interpretation

The Phase 4bm-W branch implementation report and closeout stated **"45 passed"** for the three new pytest suites. Merge-time verification (recorded in the Phase 4bm-W merge-closeout §8) found the accurate re-verified count was **"33 passed"** for those listed suites. **Interpretation:** this is a **documentation overcount only** in the branch docs — *not* a test failure. Every listed suite passed (33/33); no test was skipped, errored, or failed at merge; and the diagnostic verdict is unchanged. The discrepancy concerns a reported integer, not test outcomes, code behavior, or any diagnostic result. The authoritative count is **33 passed** as recorded in the merge-closeout. This discrepancy has **no bearing** on any ML-readiness scoping criterion: the structural and alignment evidence underpinning the verdict is independent of the pytest *count*, and the suites themselves passed. It is noted here for completeness and does not warrant defer or do-not-recommend.

## 16. ML-readiness scoping criteria

Evaluated against repo evidence (read-only). A future ML-readiness *scoping memo* may be proposed only if all of the following are satisfied.

| # | Criterion | Result | Evidence |
| --- | --- | --- | --- |
| **A** | Descriptive diagnostics completed successfully | **PASS** | Phase 4bm-W executed all eight diagnostic groups A–H; execution exit 0; verdict issued |
| **B** | Diagnostic verdict has 0 blocking structural failures | **PASS** | §7; all structural/alignment counters aggregate to 0 |
| **C** | Non-blocking caveats are understood and do not require immediate remediation before a scoping memo | **PASS** | §8; all four caveats characterized, bounded, expected; none blocking |
| **D** | Split policy was applied correctly and can govern future ML scoping | **PASS** | §9; Phase 4bm-U policy applied verbatim; `out_of_partition_day = 0`; `split_assignment_mismatch = 0` |
| **E** | Test holdout was not used for tuning or design | **PASS** | §9; `holdout_protection` block all protected; descriptive summaries only |
| **F** | Feature/label alignment is strict 1:1 across all 90 days | **PASS** | §12; all six alignment fields 0; 90/90 + 90/90; `src_ne_feature_ts = 0` |
| **G** | Label availability and censoring behavior is understood | **PASS** | §10; censored `{1s:14,5s:39,15s:170,60s:634}` = manifest expectation; missingness = censoring |
| **H** | Distribution summaries reveal no structural impossibility for scoping | **PASS** | §11; exact moments consistent; std monotone in horizon; no degeneracy |
| **I** | Missingness / value-domain checks passed | **PASS** | §14; all domain/nullability counters 0 |
| **J** | Local diagnostic outputs exist, are gitignored, and are reproducible via recorded hashes | **PASS** | §5.4; four output SHAs MATCH; `git check-ignore` `.gitignore:88: data/research/` |
| **K** | No manifest or successor-state mutation occurred | **PASS** | §5.4; manifests, Phase 4bm-S/U successor-states, Phase 4bm-Q gate report byte-identical |
| **L** | No ML / strategy / backtest work has yet been authorized or run | **PASS** | Phase 4bm-W report §18; every predecessor records `ml_authorized = false` / `strategy_authorized = false` / `backtest_authorized = false` |
| **M** | Retained verdicts and project locks remain unchanged | **PASS** | §21–§22; preserved verbatim from Phase 4bm-W |

**All ML-readiness scoping criteria A–M PASS.**

## 17. Decision

`RECOMMEND_AUTHORIZE_ML_READINESS_SCOPING_MEMO`.

## 18. Rationale for the chosen decision

All thirteen ML-readiness scoping criteria A–M (§16) pass on current repo evidence:

- Phase 4bm-W completed the scoped descriptive / structural diagnostics with verdict `DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS` — **0 blocking structural failures** (§7) and **4 fully characterized, non-blocking caveats** (§8) that require no remediation before a scoping memo.
- The Phase 4bm-U split policy was applied verbatim and is leakage-correct, the test holdout was protected, feature/label alignment is strict 1:1 across all 90 days, label availability/censoring is fully understood, distributions reveal no structural impossibility, and all missingness/value-domain checks passed (§9–§14).
- The local diagnostic outputs exist, are gitignored, and re-hash to their recorded SHAs; no manifest or successor-state artefact was mutated; no ML / strategy / backtest work has been authorized or run; and all retained verdicts and project locks are preserved verbatim (§5.4, §16, §21–§22).
- The only validation discrepancy (branch docs "45 passed" vs. merge-verified "33 passed") is a documentation overcount with all listed suites passing and the verdict unchanged; it bears on no scoping criterion (§15).

Because the descriptive diagnostics passed with only understood, non-blocking caveats, and because an ML-readiness *scoping memo* is itself a docs-only governance artefact that trains nothing, selects nothing, tunes nothing, and runs nothing, the appropriate recommendation is to authorize — separately and in a future phase — a docs-only ML-readiness scoping memo only, bounded by §19. No prerequisite is missing and no drift was detected, so neither `DEFER_ML_READINESS_SCOPING_PENDING_SPECIFIC_REMEDIATION` nor `DO_NOT_RECOMMEND_ML_READINESS_SCOPING` is warranted. The recommendation is a *recommendation only*; it does not itself authorize any scoping memo, any ML, or any execution.

**`RECOMMEND_AUTHORIZE_ML_READINESS_SCOPING_MEMO` means only:** a future, separately authorized, docs-only memo may define *what* ML-readiness scoping should evaluate. It does **not** mean ML is authorized, model training is authorized, feature selection is authorized, model selection is authorized, threshold tuning is authorized, strategy research is authorized, backtests are authorized, acquisition is authorized, or research execution is authorized.

## 19. What a future ML-readiness scoping memo would be allowed to evaluate, if separately authorized

A future, separately authorized **docs-only ML-readiness scoping memo** (provisionally a "Phase 4bm-Y"-class phase, **not** authorized here) would be permitted to evaluate, at memo / governance level only:

- admissible supervised-learning task framing;
- target / horizon admissibility (which of 1s / 5s / 15s / 60s, and direction vs. magnitude framing);
- train / validation / test usage rules (restating the Phase 4bm-U policy and single-use holdout protection);
- metrics allowed at scoping level;
- leakage controls;
- baseline model families to consider later, **without training them**;
- sample-weighting policy questions;
- class-imbalance policy questions;
- calibration / probability-output policy questions;
- cost-aware evaluation questions, **without backtesting**;
- whether a later ML-baseline implementation phase may be *proposed*.

A future ML-readiness scoping memo **must not**: train any model; select any model; select or rank features; tune hyperparameters; tune thresholds; design strategy; generate signals; simulate PnL; run backtests; use the test holdout for tuning/design; mutate manifests or successor states; or acquire data. It would carry forward the four Phase 4bm-W caveats (§8) as explicit stated constraints, and would require its own separately authorized operator prompt, its own branch, its own implementation report + closeout, and (separately) a Tier 1 merge-closeout. **Any ML-readiness scoping requires a separately authorized memo phase.**

## 20. What this phase does not authorize

Phase 4bm-X defines a descriptive diagnostics interpretation and a single governance recommendation only. It does **not**, and **cannot**, authorize:

- any ML-readiness scoping memo (it only *recommends* that one may be separately authorized); any diagnostics rerun; any new diagnostic artefact; any ML artefact; any split-mask materialization;
- any ML training / model selection / feature ranking / feature selection / hyperparameter selection / threshold tuning / meta-labeling; any strategy specification / implementation / signal construction; any PnL simulation / backtest / walk-forward optimization;
- any use of the test window for tuning or design; any eligibility rescue;
- any mutation of any manifest, the Phase 4bm-S successor-state artefact, the Phase 4bm-U successor-state artefact, the Phase 4bm-Q gate report, or any other `data/microstructure/` or `data/research/` artefact;
- any change to `chronological_split_policy`, `research_eligible`, `eligibility_gate_status`, `diagnostics_authorized`, or `ml_authorized` on any on-disk manifest;
- any data acquisition (no additional days / symbols / data families beyond the locked 90-day v002 envelope; no mark-price / order-book / funding / OI / liquidation / cross-venue / aggTrades);
- any public / authenticated / private endpoint call; any WebSocket / user-stream; any credential / `.env` / `.mcp.json` / MCP / Graphify use;
- Phase 4bm-Y or any successor phase; Phase 5; Phase 4 canonical; paper / shadow; live-readiness; deployment; exchange-write; production-key creation;
- any revision of a retained verdict, any loosening of a project lock, or any amendment of M0 / Phase 4al / Phase 4aw / Phase 4bb-F / Phase 4bl-F / Phase 4bm-A-P1 / Phase 4bm-D-P1.

**Phase 4bm-X does not run diagnostics.** **Phase 4bm-X does not run ML.** **Phase 4bm-X does not define or run strategy.** **Phase 4bm-X does not run backtests.** **Phase 4bm-X does not authorize acquisition.** **Phase 4bm-X does not authorize research execution.** **Phase 4bm-X does not create ML artefacts.** **Phase 4bm-X does not create diagnostic artefacts.** **Phase 4bm-X does not perform feature selection.** **Phase 4bm-X does not perform model selection.** **Phase 4bm-X does not perform threshold tuning.** **Phase 4bm-X does not use the test holdout for tuning or design.** **Phase 4bm-X does not mutate any manifest.** **Phase 4bm-X does not mutate any successor-state artefact.** **Phase 4bm-X does not commit data/microstructure.** **Phase 4bm-X does not commit data/research.** **Any ML-readiness scoping requires a separately authorized memo phase.** **Phase 4bm-Y is not authorized by Phase 4bm-X.**

## 21. Retained verdicts preserved

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

All prior phase results (Phase 4am .. Phase 4bm-W) preserved verbatim.

## 22. Project locks preserved

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
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (never invoked by Phase 4bm-X)
- Phase 4bb-F canonical sidecar / path policy
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks
- Phase 4bm-A-P1 thin-prompt context-management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace standard

## 23. Recommended next state

**Remain paused.** Phase 4bm-X is branch-complete only by this work. Per the Phase 4bk-A workflow standard, it is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1). The interpretation decision is `RECOMMEND_AUTHORIZE_ML_READINESS_SCOPING_MEMO`; this is a recommendation only and authorizes nothing. **Any ML-readiness scoping requires a separately authorized memo phase.** **Phase 4bm-Y is not authorized by Phase 4bm-X.** **Recommended state remains paused.**
