# Phase 4bm-T — Multi-Day V002 Chronological Split-Policy Memo

**Phase identity:** Phase 4bm-T — Multi-Day V002 Chronological Split-Policy Memo (docs-only governance / methodology memo; multi-day v002 analogue of the v001 Phase 4bj-H / Phase 4bj-I chronological-split-policy memos).
**Date:** 2026-05-25.
**Branch:** `phase-4bm-t/multi-day-v002-chronological-split-policy-memo`.
**Base SHA:** `main` at `ab1269d4c0b46e95961542e032173eb9a098be32` (Phase 4bm-S merge-closeout SHA-finalization commit, `docs(phase-4bm-s): finalize merge closeout shas`; pre-branch `main == origin/main` verified in sync).
**Tier:** **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 escalation rules. First-of-kind multi-day v002 chronological-split-policy memo; it defines the chronological split-policy governance boundary for a research-use-approved-in-principle multi-day v002 label family and may influence a future separately authorized split-policy successor-state recording phase, so it escalates to Tier 1.
**Phase type:** docs-only governance / methodology memo. Adds two new tracked docs files under `docs/00-meta/implementation-reports/` (this memo + the paired closeout) and narrowly updates `docs/00-meta/current-project-state.md`. **No** source / test / script / configuration / manifest / sidecar / gate-report / successor-state mutation. **No** local data artefact created. **No** gate rerun. **No** acquisition. **No** successor authorization.
**Status:** drafted; pending operator review. Branch-complete only by this work; not merged into `main`; not project-complete.

---

## 1. Required exact phrases

- **Phase 4bm-T is a docs-only chronological split-policy memo.**
- **Phase 4bm-T does not create chronological split successor-state JSON.**
- **Phase 4bm-T does not mutate any manifest.**
- **Phase 4bm-T does not mutate the Phase 4bm-S successor-state artefact.**
- **Phase 4bm-T does not commit data/microstructure.**
- **Phase 4bm-T does not authorize diagnostics, ML, strategy, or backtests.**
- **Phase 4bm-T does not authorize acquisition.**
- **Phase 4bm-T does not run any research execution.**
- **The chronological split policy is defined at memo level only.**
- **Any chronological split-policy recording requires a separately authorized successor-state phase.**
- **Phase 4bm-U is not authorized by Phase 4bm-T.**
- **Recommended state remains paused.**

---

## 2. Phase identity, branch, base SHA

This memo answers a single governance question:

> Given the 90-day multi-day v002 label family `microstructure_labels_aggtrades_v001 @ v002` (BTCUSDT × 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 rows; 4 horizons 1s / 5s / 15s / 60s) is now research-use approved **in principle** through the sibling Phase 4bm-S successor-state artefact (`LABEL_FAMILY_RESEARCH_USE_APPROVED_IN_PRINCIPLE`), what chronological split policy should govern any future research use of this dataset, and with what boundary-crossing / horizon-leakage, embargo, no-shuffle, and single-use-holdout guardrails?

The memo is **docs-only**. It records a chronological split policy at policy / governance level. It does not create any split artefact, does not create any chronological split successor-state JSON, does not mutate any manifest, does not mutate the Phase 4bm-S successor-state artefact, does not run diagnostics / ML / strategy / backtests, does not acquire data, and does not authorize any successor implementation. **Phase 4bm-T is a docs-only chronological split-policy memo.**

- **Phase name:** Phase 4bm-T — Multi-Day V002 Chronological Split-Policy Memo.
- **Phase type:** docs-only governance / methodology memo.
- **Branch:** `phase-4bm-t/multi-day-v002-chronological-split-policy-memo`.
- **Base SHA:** `main` at `ab1269d4c0b46e95961542e032173eb9a098be32`.
- **Predecessor anchor:** Phase 4bm-S merge-closeout `320015efefd0e12ea5d3584c8910220d52ddbd0d` + SHA-finalization commit `ab1269d4c0b46e95961542e032173eb9a098be32` (project-complete on `main`).
- **Authorization:** explicit operator authorization for Phase 4bm-T only.

---

## 3. Predecessor chain

| Phase | Role | Status on `main` | Verdict / result |
| --- | --- | --- | --- |
| **Phase 4bm-M** | Multi-day v002 label-family boundary / design memo | merge-complete | label-boundary + multi-day horizon / envelope / leakage policy defined at memo level |
| **Phase 4bm-N** | Multi-day v002 label schema finalization memo | merge-complete | 40-column v002 label schema locked at memo level |
| **Phase 4bm-O** | Multi-day v002 label kernel implementation + local label artefact generation | merge-complete | 90 per-day label parquets + 90 sidecars + 1 manifest + 1 manifest sidecar; all gitignored |
| **Phase 4bm-P** | Multi-day v002 label artefact structural QA memo | merge-complete | `LABEL_STRUCTURAL_QA_PASS` |
| **Phase 4bm-Q** | Multi-day v002 label-family eligibility gate design / implementation / execution | merge-complete | `LABEL_GATE_PASS`; 60 / 60 PASS; report-level only |
| **Phase 4bm-R** | Multi-day v002 label-family research-use decision memo | merge-complete | `RECOMMEND_LABEL_RESEARCH_USE_AUTHORIZATION` |
| **Phase 4bm-S** | Multi-day v002 label-family research-use successor-state recording | merge-complete; SHA-finalized | `LABEL_FAMILY_RESEARCH_USE_APPROVED_IN_PRINCIPLE` |

Phase 4bm-S lifecycle SHAs (verified present on `main`): base SHA `e2fdbdd6d7388235c2e4495072455c2ae787349d`; branch tip before merge `10ba13753b721c2e21abeeed7224c2dbed31264b`; merge commit `3df3c3b16714149e9e6d5a9cd73df25f18e00fe8`; merge-closeout commit `320015efefd0e12ea5d3584c8910220d52ddbd0d`; SHA-finalization commit `ab1269d4c0b46e95961542e032173eb9a098be32` (latest finalized `main` state and this phase's base).

The chain is internally consistent. Each phase preserves the upstream artefacts byte-identically. No verdict has been revised. No project lock has been loosened.

---

## 4. Evidence reviewed

### 4.1 V002 predecessor evidence

- Phase 4bm-S implementation report `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-s_multi-day-v002-label-family-research-use-successor-state.md`, closeout, and merge-closeout `2026-05-25_phase-4bm-s_merge-closeout.md`.
- Phase 4bm-R decision memo `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-r_multi-day-v002-label-family-research-use-decision-memo.md`, closeout, and merge-closeout.
- Phase 4bm-Q eligibility-gate report `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-q_multi-day-v002-label-family-eligibility-gate.md`, closeout, and merge-closeout.
- Phase 4bm-P structural QA memo `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-p_multi-day-v002-label-artefact-structural-qa-memo.md`.
- Phase 4bm-O label kernel / local artefacts report `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-o_multi-day-v002-label-kernel-local-artefacts.md`.
- Phase 4bm-N label schema finalization `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-n_multi-day-v002-label-schema-finalization.md`.
- Phase 4bm-M label-family boundary design memo `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-m_multi-day-v002-label-family-boundary-design-memo.md` (multi-day horizon / boundary / envelope-terminal censoring / timestamp / leakage policy; §22–§23 in particular).
- Earlier feature-family chain `2026-05-18_phase-4bm-l_…` / `2026-05-18_phase-4bm-k_…` / `2026-05-18_phase-4bm-j_…`.

### 4.2 V001 chronological-split-policy precedent (governing alignment source)

The v001 family path establishes the binding precedent for how the project treats chronological splitting:

- **Phase 4bj-H** — `2026-05-12_phase-4bj-h_label-evaluation-chronological-split-boundary-memo.md`: recorded that no empirical label evaluation may run before a chronological split policy exists; any split must be temporal (never random); any future split policy must be a **sibling artefact**, never a manifest mutation; the original label manifest must keep `chronological_split_policy = "not_yet_defined"` until a separately authorized recording phase; an embargo / purge is required because labels carry overlapping forward horizons up to 60s.
- **Phase 4bj-I** — `2026-05-12_phase-4bj-i_chronological-split-policy-design-memo.md`: selected **Option D** for the v001 single-day cell — declare the single UTC-day cell **insufficient** for a formal train / validation / test split and require multi-day expansion before formal partitioning; recorded a minimum-expansion heuristic of "at least 30 distinct UTC days" before a formal chronological train / validation / test partition could be considered; mandated a **uniform 60s purge / embargo** default at any partition boundary (60s = maximum locked label horizon); forbade random / shuffled / bootstrap splits; required per-row inclusion masks rather than parquet rewrites.
- **Phase 4bj-J** — `2026-05-12_phase-4bj-j_no-split-determination-recording.md`: operationalized Phase 4bj-I Option D into a sibling **no-split determination** JSON for the v001 single-day cell, recording `split_policy_status = recorded`, `determination = no_formal_train_validation_test_split`, `default_purge_embargo_policy = uniform_60s_purge_embargo`, `max_forward_horizon_seconds = 60`; preserved the v001 label manifest byte-identically.

**Interpretation of the precedent for v002.** The v001 cell was rejected for a formal split **only** because it was a single UTC day; Phase 4bj-I expressly conditioned a future formal train / validation / test partition on multi-day expansion of "at least 30 distinct UTC days". The v002 family is exactly that expansion: 90 contiguous UTC dates. The v002 dataset therefore **satisfies the precondition Phase 4bj-I recorded as a prerequisite for formal chronological partitioning**. Phase 4bm-T accordingly adopts a formal chronological train / validation / test policy for v002 (which Phase 4bj-I could not adopt for v001) while preserving, verbatim, the v001 binding guardrails: temporal-only assignment, uniform ≥60s embargo at boundaries, no shuffle / bootstrap / random splits, sibling-artefact recording only, and `chronological_split_policy = "not_yet_defined"` on the manifest until a separately authorized successor-state recording phase.

### 4.3 Governance / process artefacts reviewed

- `docs/00-meta/process/merge-closeout-standard.md` (Tier 1 merge-closeout ceremony — applies to a future, separately authorized merge phase, not to this branch work).
- `docs/00-meta/process/phase-risk-tiering-standard.md` (§3 escalation; §7 reusable non-authorization blocks).
- `docs/00-meta/implementation-reports/2026-05-17_phase-4bm-a-p1_context-management-standard.md` (thin-prompt context-management standard; honored).
- `docs/00-meta/implementation-reports/2026-05-17_phase-4bm-d-p1_lightweight-claude-code-workspace-standard.md` (lightweight Claude Code workspace standard; honored).

No prior memo's text is modified by Phase 4bm-T. No artefact under `data/microstructure/` is modified by Phase 4bm-T. The Phase 4bm-S successor-state JSON + sidecar, the v002 label manifest + sidecar, and the Phase 4bm-Q gate report + sidecar were read-only re-hashed (matches byte-for-byte; see §13.6); none was rewritten.

---

## 5. Local-evidence verification (read-only)

All four governed evidence artefacts and the Phase 4bm-S successor-state pair were re-hashed read-only at the start of this phase and matched their expected values byte-for-byte; all remain gitignored under `.gitignore:85: data/microstructure/` and do not appear in `git status`.

| Artefact | Expected SHA256 | Result |
| --- | --- | --- |
| Phase 4bm-S successor-state JSON | `081730006c11360692db0a99d59a0ed499f762ef4f86d6e29bdf3016550abfe7` | MATCH (gitignored) |
| Phase 4bm-S successor-state sidecar | `05597fe4d568f5644ad9acc914f8a3b429bc7984cf7df3a2ac3f8c7935e02551` | MATCH (gitignored) |
| v002 label manifest | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` | MATCH |
| v002 label manifest sidecar | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` | MATCH |
| Phase 4bm-Q gate report | `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` | MATCH |
| Phase 4bm-Q gate report sidecar | `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` | MATCH |

Label parquet / sidecar counts independently verified on disk at **90 / 90**.

---

## 6. Dataset identity

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
| Phase 4bm-S successor-state SHA256 | `081730006c11360692db0a99d59a0ed499f762ef4f86d6e29bdf3016550abfe7` |
| Phase 4bm-S successor-state sidecar SHA256 | `05597fe4d568f5644ad9acc914f8a3b429bc7984cf7df3a2ac3f8c7935e02551` |
| Current manifest `chronological_split_policy` | `"not_yet_defined"` (unchanged; Phase 4bm-T does not change this) |

---

## 7. Chosen split policy

**Policy name:** `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`.

This policy adopts the conservative formal chronological train / validation / test partition recommended for the 90 contiguous UTC dates, exactly as conditioned by the v001 Phase 4bj-I precedent (which deferred a formal split only until multi-day data existed) and consistent with the Phase 4bm-M v002 multi-day timestamp / leakage / no-shuffle policy.

### 7.1 Split windows

| Split | UTC date window (inclusive) | Date count | Share |
| --- | --- | --- | --- |
| **Train** | 2024-12-01 .. 2025-01-14 | 45 | 50.0% |
| **Validation** | 2025-01-15 .. 2025-02-13 | 30 | 33.3% |
| **Test / final holdout** | 2025-02-14 .. 2025-02-28 | 15 | 16.7% |
| **Total** | 2024-12-01 .. 2025-02-28 | 90 | 100% |

Date-count arithmetic: train = 31 (Dec 2024) + 14 (Jan 1–14 2025) = 45; validation = 17 (Jan 15–31 2025) + 13 (Feb 1–13 2025) = 30; test = 15 (Feb 14–28 2025); total = 90.

### 7.2 Boundary timestamps (UTC)

- **Train → Validation boundary** `T_TV`: between 2025-01-14 23:59:59.999Z and 2025-01-15 00:00:00.000Z; the validation window opens at `2025-01-15 00:00:00.000Z`.
- **Validation → Test boundary** `T_VT`: between 2025-02-13 23:59:59.999Z and 2025-02-14 00:00:00.000Z; the test window opens at `2025-02-14 00:00:00.000Z`.

### 7.3 Assignment rule

Rows are assigned to a split by their **source event timestamp UTC date** — the v002 label row's `source_transact_time_ms` (the feature-row anchor timestamp carried verbatim per Phase 4bm-M §16), interpreted as a UTC calendar date and matched to the per-day partition's `utc_date`. Assignment uses the anchor row's UTC date, never the future reference timestamp's date (consistent with Phase 4bm-M §22 day-boundary handling). Within a UTC day, the canonical deterministic event order `(feature_timestamp_ms, agg_trade_id, row_index)` (Phase 4bm-M §22) is preserved; no reordering is performed for split assignment.

### 7.4 Split ratio

50.0% / 33.3% / 16.7% by date count (45 / 30 / 15 of 90). The ratio is expressed in **dates**, not rows; row shares will differ slightly because per-day row counts vary, and that is acceptable — the partition is defined by UTC date boundaries, not by row-count targets.

---

## 8. Alternative split policies considered and rejected

| Option | Description | Verdict |
| --- | --- | --- |
| **A** | No split; remain `not_yet_defined`; record no policy | Maximally conservative but fails the task: the operator has authorized a policy memo and the dataset now satisfies the v001 Phase 4bj-I multi-day precondition. **Not selected** — leaves the governance question unanswered. |
| **B** | Random / shuffled / k-fold cross-validation / bootstrap split | **FORBIDDEN.** Violates the v001 Phase 4bj-H / 4bj-I no-shuffle rule and Phase 4bm-M §22 (“No random shuffle”). Destroys temporal order and guarantees look-ahead leakage on forward-horizon labels. **Rejected.** |
| **C** | Single 90-day block, no internal partition (treat as one fixture) | Wastes the multi-day expansion that exists precisely to permit a held-out test; provides no out-of-sample discipline. **Not selected.** |
| **D** | Formal chronological 70 / 15 / 15 (or 80 / 10 / 10) with larger train | Defensible, but a smaller validation window weakens model-selection stability over the 90-day regime span, and a 9–15-day validation window is thin for the four-horizon label set. **Not selected** in favour of a 30-day validation that better spans intraday / weekly regime variation. |
| **E** | Chronological split **with the test window earliest** (test → validation → train forward in time) | **FORBIDDEN.** Inverts temporal order; the final holdout must be the latest period so that no train/validation information post-dates it. **Rejected.** |
| **F** | Per-row boundary reassignment that pushes boundary-crossing rows *forward* into the later split | **Rejected** as the default: pushing a train-anchored row’s label into validation would let the later split inherit earlier-split anchors and blur the holdout. The conservative rule is **exclusion from the earlier split**, not forward reassignment (see §9). A stricter forward-aware rule may only be introduced by a future separately authorized memo. |
| **G** | Proceed directly to diagnostics / ML / strategy / backtest on the 90-day cell now | **FORBIDDEN / NOT RECOMMENDED.** Violates M0 admissibility, the Phase 4al refined no-rescue rule, and the project safety posture. A split policy is upstream of, and does not authorize, any empirical work. **Rejected.** |

**Selected:** `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` (the 45 / 30 / 15 formal chronological partition of §7).

---

## 9. Boundary-crossing / horizon-leakage rule

Because v002 labels carry forward horizons up to 60 seconds, a row whose anchor sits near a split boundary has a label-evaluation window that may cross from its split into the next (later) split. Without a guardrail, the earlier split would consume future information that belongs to the later split.

**Binding rule (memo-level governance; enforced by any future separately authorized row-level research execution):**

1. **Boundary-crossing definition.** For a given split, a row is **invalid for that split** if any required label horizon (or any forward-looking support window the future research requires) for that row crosses from the row's split into a later split — i.e. if `source_transact_time_ms + H*1000` (for any required horizon `H`) reaches at or beyond the next boundary `T_TV` or `T_VT`.
2. **Conservative default — exclude from the earlier split.** Boundary-crossing rows must be **excluded from the earlier split**, not reassigned forward into the later split. This preserves the later split (and especially the test holdout) as uncontaminated by earlier-split anchors. This mirrors the v001 Phase 4bj-I / Phase 4bj-J `uniform_60s_purge_embargo` rule (purge rows whose horizon crosses a boundary).
3. **Minimum embargo.** Because the maximum declared label horizon is **60 seconds**, a **minimum 60-second boundary embargo** is required at both the train/validation boundary `T_TV` and the validation/test boundary `T_VT` for any future row-level research execution. Concretely: rows anchored in `[T − 60s, T)` for a boundary `T` are excluded from the earlier split for any analysis using a horizon that crosses `T`. A larger operational embargo (e.g. several minutes) may be recommended by a future memo if justified, but the embargo **must not be reduced below 60 seconds**.
4. **No forward reassignment by default.** A boundary-crossing row may be reassigned forward only if a future, separately authorized memo defines a stricter rule that demonstrably prevents the train (and validation) splits from using validation/test future information. Until then, exclusion at the boundary is the only admissible treatment.
5. **Per-row masks, not parquet rewrites.** Any future research execution that applies this rule must record per-row inclusion / exclusion via masks (per split, per horizon), never by rewriting the v002 label parquets. The 90 label parquets remain byte-identical (Phase 4bm-M §21 / Phase 4bj-I §6.1 precedent).
6. **Envelope-terminal censoring is separate and additive.** The Phase 4bm-N / Phase 4bm-M envelope-terminal censoring at `2025-02-28 23:59:59.996Z` (per-horizon `{1s: 14, 5s: 39, 15s: 170, 60s: 634}`) applies independently of the split-boundary embargo. Rows whose horizon falls beyond the 90-day envelope are already censored (null label + explicit per-horizon censoring flag) and must continue to be handled per their censoring flags; the test-window's right edge therefore carries the structural censoring asymmetry, which any future diagnostic must report.

### 9.1 No-shuffle / no-bootstrap leakage guardrails

No random split, shuffled cross-validation, k-fold over time, bootstrap resampling, or post-hoc temporal resampling is allowed for this 90-day family unless a later separately authorized methodology memo explicitly supersedes this policy. All partitioning is strictly chronological and forward-in-time: every row in the test window post-dates every row in the validation window, which post-dates every row in the train window (subject to the §9 boundary exclusions).

---

## 10. Holdout use rule

The **test / final holdout window (2025-02-14 .. 2025-02-28; 15 dates)** is a **single-use final holdout**. It must **not** be used for:

- feature selection;
- hyperparameter selection;
- threshold tuning;
- model selection;
- strategy design;
- diagnostic iteration;
- eligibility rescue.

The test window may be touched at most once, by a future separately authorized phase, as a final confirmatory measurement after all feature selection, model selection, hyperparameter selection, and threshold tuning have been finalized exclusively on train (fit) and validation (selection). Any repeated read of the test window for tuning purposes burns the holdout and invalidates its evidentiary value. Single-use holdout discipline is binding.

The **validation window (2025-01-15 .. 2025-02-13; 30 dates)** is the only window admissible for model selection, hyperparameter selection, and threshold tuning. The **train window (2024-12-01 .. 2025-01-14; 45 dates)** is the only window admissible for model fitting. No window may borrow future information from a later window (subject to the §9 boundary exclusions).

---

## 11. Future successor-state recording requirements

This memo records the policy at memo level only. A future, separately authorized **chronological-split-policy successor-state recording phase** (the multi-day v002 analogue of the v001 Phase 4bj-J no-split-determination recording, but recording a *formal split* policy rather than a *no-split* determination) would be required to make the policy machine-readable. If and only if separately authorized, that phase would:

1. Produce **exactly one sibling successor-state JSON** under the gitignored `data/microstructure/successor-state/labels/` namespace (mirroring the Phase 4bm-S layout and the Phase 4bb-F canonical filename convention `<dataset_family>__<dataset_version>__<stage_marker>__phase-<phase_id>.json`), plus one paired canonical Phase 4bb-F sidecar (`<json_sha256_hex>  <basename>\n`; two ASCII spaces; LF only; no CRLF; no BOM).
2. Record `split_policy_name = "CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO"`, `split_policy_status = "recorded"`, the three UTC date windows and date counts, the assignment rule (`source_transact_time_ms` UTC date), the boundary-crossing exclusion rule, the minimum 60s embargo, the no-shuffle rule, and the single-use holdout rule — **only on the sibling successor-state artefact**, never on the manifest.
3. Cite verbatim the v002 label manifest SHA `5e17074d…`, the manifest sidecar SHA `451d5b88…`, the Phase 4bm-Q gate report SHA `8a360608…` + sidecar `3913a510…`, the Phase 4bm-S successor-state SHA `081730006c…` + sidecar `05597fe4…`, `label_config_hash = 352bad41…`, `feature_config_hash = 819cfa7a…`, and this Phase 4bm-T memo as the policy-decision evidence.
4. Preserve the v002 label manifest byte-identically at SHA `5e17074d…` (the manifest's `chronological_split_policy` remains `"not_yet_defined"`; the policy is encoded only in the new sibling artefact).
5. Preserve the Phase 4bm-S successor-state JSON + sidecar, the Phase 4bm-Q gate report + sidecar, all 90 label parquets, and all 90 label sidecars byte-identically.
6. Preserve the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant end-to-end (never invoked).
7. Preserve every retained verdict and project lock verbatim.

**Any chronological split-policy recording requires a separately authorized successor-state phase.** No such phase is authorized by Phase 4bm-T.

---

## 12. What the split policy does not authorize

This policy only defines chronological governance. It does **not** run or authorize diagnostics, ML, strategy, or backtests. Specifically, Phase 4bm-T does **not**, and **cannot**, authorize:

- creation of any chronological split successor-state JSON (or any split artefact on disk);
- any mutation of any manifest, the Phase 4bm-S successor-state artefact, the Phase 4bm-Q gate report, or any other `data/microstructure/` artefact;
- any change to `chronological_split_policy` on any actual on-disk manifest (it remains `"not_yet_defined"`);
- any rerun of the label gate, feature gate, label kernel, feature kernel, normalizer, or structural-QA inspector;
- any label generation, feature generation, or data acquisition (no additional days, no additional symbols, no mark-price / order-book / funding / OI / liquidation / cross-venue / aggTrades beyond the locked 90-day v002 envelope);
- any diagnostics definition or execution; any ML training / model selection / feature ranking / meta-labeling; any strategy specification / implementation / signal construction; any backtest specification / plan / execution;
- any public / authenticated / private endpoint call; any WebSocket / user-stream; any credential / `.env` / `.mcp.json` / MCP / Graphify use;
- Phase 4bm-U or any successor phase; Phase 5; Phase 4 canonical;
- paper / shadow; live-readiness; deployment; exchange-write; production-key creation;
- any revision of a retained verdict, any loosening of a project lock, or any amendment of M0 / Phase 4al / Phase 4aw / Phase 4bb-F / Phase 4bl-F / Phase 4bm-A-P1 / Phase 4bm-D-P1.

**Phase 4bm-T does not run any research execution.** **Phase 4bm-U is not authorized by Phase 4bm-T.**

---

## 13. Validation

This phase is docs-only. Validation gates applied:

1. `git diff --check` — clean (exit 0).
2. `git status --short` — only the expected pre-existing untracked `data/research/` (and `.claude/scheduled_tasks.lock` if present); no `data/microstructure/` entry.
3. `git diff --name-only` (working tree) and `git diff --name-only --cached` — only the three tracked docs paths (this memo, the closeout, and the narrow `current-project-state.md` update); no source / test / script / configuration path; no `data/microstructure/` path.
4. No successor-state JSON created; no manifest modified.
5. `ruff` / `mypy` / `pytest` — deliberately not run; Phase 4bm-T modifies no source, no test, no script, no `pyproject.toml`, no `README.md`, and no `.gitignore`. The latest authoritative whole-repo validation remains the predecessor merges. No project-specific markdown-lint gate exists in this repository; none invented.
6. Read-only re-hash of the Phase 4bm-S successor-state JSON + sidecar, the v002 label manifest + sidecar, and the Phase 4bm-Q gate report + sidecar — all six MATCH expected SHAs byte-for-byte (see §5).

---

## 14. Retained verdicts preserved

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

---

## 15. Project locks preserved

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
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (never invoked by Phase 4bm-T)
- Phase 4bb-F canonical sidecar / path policy
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks
- Phase 4bm-A-P1 thin-prompt context-management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace standard

All prior phase results (Phase 4am .. Phase 4bm-S) preserved verbatim.

---

## 16. Recommended next state

**Remain paused.** Phase 4bm-T is branch-complete only by this work. Per the Phase 4bk-A workflow standard, it is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1). The chronological split policy `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` is defined at memo level only; making it machine-readable requires a separately authorized chronological-split-policy successor-state recording phase (§11), which is not authorized here.

**The chronological split policy is defined at memo level only.** **Any chronological split-policy recording requires a separately authorized successor-state phase.** **Phase 4bm-U is not authorized by Phase 4bm-T.** **Recommended state remains paused.**
