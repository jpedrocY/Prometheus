# Phase 4bm-R — Multi-Day V002 Label-Family Research-Use Decision Memo

**Phase identity:** Phase 4bm-R — Multi-Day V002 Label-Family Research-Use Decision Memo (docs-only governance decision memo; multi-day v002 analogue of Phase 4bj-F).
**Date:** 2026-05-25.
**Branch:** `phase-4bm-r/multi-day-v002-label-family-research-use-decision-memo`.
**Base:** `main` at `219c8b0d1f7e74c596ecc9aa50662101dc59a9d3` (Phase 4bm-Q merge-closeout SHA-finalization commit; pre-branch `main == origin/main` verified in sync).
**Tier:** **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3. First-of-kind multi-day v002 label-family research-use governance / admissibility decision; influences whether a future label-family successor-state recording phase may be proposed and later whether chronological-split-policy eligibility can be considered.
**Phase type:** docs-only research-use decision / governance memo. **No** source / test / script / configuration / data / manifest / sidecar / gate-report / successor-state file is mutated. **No** local data artefact is created. **No** gate is rerun. **No** acquisition. **No** successor authorization. The only tracked files changed by Phase 4bm-R are this memo, the paired closeout, and a narrow `docs/00-meta/current-project-state.md` update (new Phase 4bm-R narrative paragraph + new "Current phase:" block; prior Phase 4bm-Q "Current phase:" block preserved as labelled historical context).
**Status:** drafted; pending operator review. Branch-complete only by this work; not merged into `main`; not project-complete.

---

## 1. Required exact phrases

- **Phase 4bm-R is a docs-only label-family research-use decision memo.**
- **Phase 4bm-R does not mutate any manifest.**
- **Phase 4bm-R does not create successor-state JSON.**
- **Phase 4bm-R does not define chronological split policy.**
- **Phase 4bm-R does not authorize diagnostics, ML, strategy, or backtests.**
- **Phase 4bm-R does not authorize acquisition.**
- **Phase 4bm-R does not commit data/microstructure.**
- **LABEL_GATE_PASS from Phase 4bm-Q remains report-level evidence only.**
- **Label-family research-use is not recorded by Phase 4bm-R.**
- **Any label-family research-use recording requires a separately authorized successor-state phase.**
- **Phase 4bm-S is not authorized by Phase 4bm-R.**

## 2. Phase identity, branch, base SHA, risk tier

This memo answers a single governance question:

> Given the Phase 4bm-M label-family boundary design, the Phase 4bm-N label schema finalization, the Phase 4bm-O local label artefact generation, the Phase 4bm-P structural QA PASS (`LABEL_STRUCTURAL_QA_PASS`), and the Phase 4bm-Q label-family eligibility gate PASS (`LABEL_GATE_PASS`, 60 / 60 PASS at the report level; gate report SHA256 `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e`), should the project recommend authorizing a future successor-state recording phase to mark the multi-day v002 label family `microstructure_labels_aggtrades_v001 @ v002` (BTCUSDT × 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 rows; 40-column locked v002 label schema; `label_config_hash = 352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560`) as research-use approved in principle at policy level, under what exact constraints, and with what explicit non-authorizations?

The memo is **docs-only**. It records a policy-level admissibility *recommendation*. It does not mutate any manifest, flip any `research_eligible` flag, transition any `eligibility_gate_status`, mark `stage_5_label_cleared = true`, mark `label_family_research_use_authorized = true`, mark `label_family_eligibility_gate_authorized = true`, change `chronological_split_policy`, run any gate, modify any data file, compute any feature / label / signal / proxy, train any ML model, design any strategy, run any backtest, acquire any data, or authorize any successor implementation.

**Phase 4bm-R is a docs-only label-family research-use decision memo.**

## 3. Predecessor chain

| Phase | Role | Status on `main` | Verdict |
| --- | --- | --- | --- |
| **Phase 4bm-M** | Multi-day v002 label-family boundary / design memo | merge-complete | label-boundary defined at memo level only |
| **Phase 4bm-N** | Multi-day v002 label schema finalization memo | merge-complete | 40-column v002 label schema locked at memo level only |
| **Phase 4bm-O** | Multi-day v002 label kernel implementation + local label artefact generation | merge-complete | 90 per-day label parquets + 90 sidecars + 1 manifest + 1 manifest sidecar locked locally; all gitignored |
| **Phase 4bm-P** | Multi-day v002 label artefact structural QA memo | merge-complete | `LABEL_STRUCTURAL_QA_PASS` |
| **Phase 4bm-Q** | Multi-day v002 label-family eligibility gate design / implementation / execution | merge-complete (merge commit `e2817f6a0c768e5fb19a4cd76c557ee2e0d5583a`; merge-closeout commit `2ba8323d1ae29bc71e5ec6dd0cf18329e3dfbfe3`; SHA-finalization commit `219c8b0d1f7e74c596ecc9aa50662101dc59a9d3`) | `LABEL_GATE_PASS`; 60 / 60 PASS; 0 FAIL / 0 ERROR / 0 NOT_APPLICABLE / 0 blocking failures; report-level only |

The chain is internally consistent. Each phase preserves the upstream artefacts byte-identically. No verdict has been revised. No project lock has been loosened.

## 4. Evidence reviewed

### 4.1 Phase 4bm-Q evidence (locked input)

- Phase 4bm-Q implementation report: `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-q_multi-day-v002-label-family-eligibility-gate.md`.
- Phase 4bm-Q closeout: `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-q_closeout.md`.
- Phase 4bm-Q merge-closeout: `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-q_merge-closeout.md`.
- Phase 4bm-Q local gitignored gate report JSON (read-only re-hashed in Phase 4bm-R; matches byte-for-byte):
  - path: `data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-q__1779708036319__3f87123175e0.json`
  - SHA256: `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e`
  - 20,259 bytes
  - gitignored under `.gitignore:85: data/microstructure/`
  - not committed
- Phase 4bm-Q local gitignored gate report sidecar (read-only re-hashed in Phase 4bm-R; matches byte-for-byte):
  - SHA256: `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8`
  - 156 bytes
  - canonical Phase 4bb-F two-space format
  - gitignored under `.gitignore:85: data/microstructure/`
  - not committed
- Phase 4bm-Q gate verdict: `LABEL_GATE_PASS` — report-level only.
- Phase 4bm-Q check totals: 60 / 60 PASS (0 FAIL, 0 ERROR, 0 NOT_APPLICABLE, 0 blocking failures); group totals A 15/15, B 10/10, C 11/11, D 6/6, E 7/7, F 4/4, G 7/7.

### 4.2 Phase 4bm-P evidence (locked input)

- Phase 4bm-P implementation report: `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-p_multi-day-v002-label-artefact-structural-qa-memo.md`.
- Phase 4bm-P merge-closeout: `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-p_merge-closeout.md`.
- Phase 4bm-P verdict: `LABEL_STRUCTURAL_QA_PASS` — read-only structural QA of all 90 v002 per-day label parquets + 90 paired canonical Phase 4bb-F sidecars + 1 label manifest + 1 manifest sidecar against the Phase 4bm-N locked 40-column v002 label schema and the Phase 4bm-O run result.

### 4.3 Phase 4bm-O evidence (locked input)

- Phase 4bm-O implementation report: `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-o_multi-day-v002-label-kernel-local-artefacts.md`.
- 90 per-day label parquets (BTCUSDT × 2024-12-01..2025-02-28) created locally under `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/...`; all gitignored.
- 90 paired canonical Phase 4bb-F sidecars (`<parquet>.sha256`); all gitignored.
- v002 label manifest at `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json` (SHA256 `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed`); gitignored.
- v002 label manifest sidecar (SHA256 `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd`); gitignored.
- `label_config_hash = 352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560`.
- 155,153,449 total rows; per-horizon censored counts `{1s: 14, 5s: 39, 15s: 170, 60s: 634}`; `invalid_price_row_count = 0`; envelope terminal `1740787199996` ms UTC (2025-02-28 23:59:59.996Z).

### 4.4 Phase 4bm-N evidence (locked input)

- Phase 4bm-N implementation report: `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-n_multi-day-v002-label-schema-finalization-memo.md`.
- v002 label schema locked at memo level: 40 columns = 17 lineage + 8 label + 14 support + 1 identity (`label_config_hash`); 4 horizons (1s / 5s / 15s / 60s); envelope-terminal-only censoring policy; multi-day cross-day-allowed reference rows; forbidden-substring exclusions for column names.

### 4.5 Phase 4bm-M evidence (locked input)

- Phase 4bm-M implementation report: `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-m_multi-day-v002-label-family-boundary-design-memo.md`.
- Future multi-day v002 label-family boundary defined at policy level: identity, allowed / forbidden label categories, future-data-access policy, leakage / timestamp policy, multi-day horizon / boundary policy, lineage / timestamp / manifest field policy, no-rescue / M0 boundary.

### 4.6 Earlier feature-family chain (already research-use cleared)

- **Phase 4bm-J** — multi-day v002 feature-family eligibility gate: `FEATURE_GATE_PASS`, 50 / 50; gate report SHA `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242`. Merge-complete on `main`.
- **Phase 4bm-K** — multi-day v002 feature-family research-use decision memo: Outcome 1 / Decision form 1 (`FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`). Docs-only. Merge-complete on `main`.
- **Phase 4bm-L** — multi-day v002 feature-family research-use successor-state recording: sibling successor-state JSON SHA `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` + sidecar SHA `c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98`; gitignored; not committed. Merge-complete on `main`.

The upstream feature family is therefore already research-use cleared at policy + successor-state level. Criterion **F** below is satisfied.

### 4.7 V001 precedent

- Phase 4bj-E v001 label-family eligibility gate (single-day BTCUSDT 2025-01-15; 72 / 72 PASS; gate report SHA `b0b5405b…`).
- **Phase 4bj-F** v001 label-family research-use / ML-use decision memo (`docs/00-meta/implementation-reports/2026-05-11_phase-4bj-f_label-family-research-ml-use-decision-memo.md`): selected **Option B / Decision form** — "Label-family research / ML-use admissibility is admissible in principle at policy / governance level; no manifest mutation; successor-state required; explicit non-authorizations for ML / strategy / backtest / acquisition / paper / shadow / live; Phase 4bj-G is not authorized by Phase 4bj-F." Merged on `main`.
- Phase 4bj-G v001 label-family successor-state recording — confirms the docs-only memo → separately-authorized successor-state recording pattern works without ever touching the original manifest.

### 4.8 Governance / process artefacts reviewed

- `docs/00-meta/process/merge-closeout-standard.md`.
- `docs/00-meta/process/phase-risk-tiering-standard.md` (incl. §3 escalation rules and §7 reusable non-authorization blocks).
- `docs/00-meta/implementation-reports/2026-05-17_phase-4bm-a-p1_context-management-standard.md` (thin-prompt context-management standard; honored).
- `docs/00-meta/implementation-reports/2026-05-17_phase-4bm-d-p1_lightweight-claude-code-workspace-standard.md` (lightweight Claude Code workspace standard; honored).

No prior memo's text is modified by Phase 4bm-R. No artefact under `data/microstructure/` is modified by Phase 4bm-R. The Phase 4bm-Q gate report and sidecar are read-only re-hashed only (matches byte-for-byte); they are not rewritten.

## 5. Phase 4bm-Q gate result interpretation

The Phase 4bm-Q gate report records:

- `gate_verdict = "LABEL_GATE_PASS"`,
- `overall_status = "pass"`,
- 60 / 60 PASS (0 FAIL, 0 ERROR, 0 NOT_APPLICABLE, 0 blocking failures),
- group totals A 15/15 (locked preconditions), B 10/10 (inventory / sidecar / gitignore), C 11/11 (schema / lineage / forbidden-substring), D 6/6 (row count / partition / timestamp), E 7/7 (label semantics / censoring / value-domain), F 4/4 (upstream immutability), G 7/7 (non-authorization).

The report-data-model's hard invariants enforce (and Phase 4bm-Q's `MultidayLabelGateReport.__post_init__` raises `MultidayLabelGateReportError` if violated):

- `research_eligible_after = False`
- `eligibility_gate_status_after = "pending"`
- `stage_5_label_cleared_after = False`
- `label_family_research_use_authorized_after = False`
- `chronological_split_policy_after = "not_yet_defined"`
- `label_family_eligibility_gate_authorized_after = False`
- `successor_state_authorized = False`
- `diagnostics_authorized = False`
- `ml_authorized = False`
- `strategy_authorized = False`
- `backtest_authorized = False`
- `acquisition_authorized = False`

These build-time invariants mechanically prevent the verdict from escalating into actual research-use authorization. **LABEL_GATE_PASS from Phase 4bm-Q remains report-level evidence only.**

The PASS is **report-level evidence only** that the on-disk Phase 4bm-O label artefacts satisfy the 60 deterministic offline read-only checks defined in `multiday_label_gate_checks.py`. It does **not** transition the label manifest, create a successor-state, authorize ML / strategy / backtests / acquisition / paper / shadow / live, predict edge, generalize beyond BTCUSDT × 2024-12-01..2025-02-28, or bypass Phase 4ak M0 / Phase 4al refined no-rescue / Phase 4aw `flip_research_eligible` always-raises invariant.

## 6. Label-family artefact identity

| Item | Value |
| --- | --- |
| Family id | `microstructure_labels_aggtrades_v001` |
| Dataset version | `v002` |
| Label schema version | `v001` (Phase 4bm-N locked 40-column v002 label schema) |
| Symbol | `BTCUSDT` |
| Date range | 2024-12-01 .. 2025-02-28 inclusive (90 contiguous UTC dates) |
| Total label rows | 155,153,449 |
| Label partitions (per-day parquets) | 90 |
| Label parquet sidecars (canonical Phase 4bb-F) | 90 |
| Horizons | 1s / 5s / 15s / 60s |
| Per-horizon censored counts | `{1s: 14, 5s: 39, 15s: 170, 60s: 634}` |
| `invalid_price_row_count` | 0 |
| Envelope terminal | `1740787199996` ms UTC (2025-02-28 23:59:59.996Z) |
| Label manifest path | `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json` (gitignored) |
| Label manifest SHA256 | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` |
| Label manifest sidecar SHA256 | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` |
| `label_config_hash` | `352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560` |
| `feature_config_hash` (upstream lineage) | `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d` |
| v002 feature manifest SHA256 (upstream lineage) | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` |
| Phase 4bm-J feature-family gate report SHA256 (upstream lineage) | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` |
| Phase 4bm-L feature-family successor-state SHA256 (upstream lineage) | `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` |
| Phase 4bm-Q gate report SHA256 | `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` |
| Phase 4bm-Q gate report sidecar SHA256 | `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` |
| Current manifest field — `research_eligible` | `false` (unchanged; Phase 4bm-R does not change this) |
| Current manifest field — `eligibility_gate_status` | `"pending"` (unchanged; Phase 4bm-R does not change this) |
| Current manifest field — `stage_5_label_cleared` | `false` (unchanged; Phase 4bm-R does not change this) |
| Current manifest field — `label_family_research_use_authorized` | `false` (unchanged; Phase 4bm-R does not change this) |
| Current manifest field — `label_family_eligibility_gate_authorized` | `false` (unchanged; Phase 4bm-R does not change this) |
| Current manifest field — `chronological_split_policy` | `"not_yet_defined"` (unchanged; Phase 4bm-R does not change this) |

## 7. Decision criteria

Each criterion is evaluated against the locked predecessor evidence reviewed in §4.

| # | Criterion | Evaluation | Status |
| --- | --- | --- | --- |
| A | Boundary design is complete and stable | Phase 4bm-M is merge-complete on `main`; defines label-family identity, allowed / forbidden categories, multi-day horizon / envelope policy, leakage / timestamp policy, no-rescue / M0 boundary. No subsequent phase has revised any Phase 4bm-M rule. | **PASS** |
| B | Label schema is finalized and stable | Phase 4bm-N is merge-complete on `main`; locks the 40-column v002 label schema (17 lineage + 8 label + 14 support + 1 identity) verbatim. Phase 4bm-O's run produced a 40-column manifest; Phase 4bm-P verified per-day parquet schema identity across all 90 days; Phase 4bm-Q check C2 (`schema_column_list` equals `LABEL_SCHEMA_V002`) PASS. | **PASS** |
| C | Label artefacts were generated locally and reproducibly | Phase 4bm-O is merge-complete on `main`; produced 90 per-day label parquets + 90 paired canonical Phase 4bb-F sidecars + 1 label manifest + 1 manifest sidecar; all gitignored; `label_config_hash` stable; `invalid_price_row_count = 0`. | **PASS** |
| D | Structural QA passed | Phase 4bm-P is merge-complete on `main`; verdict `LABEL_STRUCTURAL_QA_PASS`. Phase 4bm-Q check A12 (`structural_qa_verdict == "LABEL_STRUCTURAL_QA_PASS"`) PASS — machine-readable lock of Phase 4bm-P PASS into the Phase 4bm-Q report-level evidence. | **PASS** |
| E | Label-family eligibility gate passed | Phase 4bm-Q is merge-complete on `main`; verdict `LABEL_GATE_PASS`; 60 / 60 PASS at first invocation; 0 FAIL / 0 ERROR / 0 NOT_APPLICABLE / 0 blocking failures across all 7 check groups. | **PASS** |
| F | Upstream feature family is already research-use cleared | Phase 4bm-K (research-use decision memo) and Phase 4bm-L (successor-state recording) are both merge-complete on `main`; Phase 4bm-L sibling successor-state JSON SHA `7eccaa8f…` recorded `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE` while preserving the original v002 feature manifest byte-identically. Phase 4bm-Q check F1 (feature manifest still `research_eligible=False / eligibility_gate_status='pending' / stage_4_feature_cleared=False`) PASS — confirms the original manifest was not mutated by Phase 4bm-L's successor-state recording. | **PASS** |
| G | Label manifest remains intentionally pending until a future successor-state recording phase | Phase 4bm-Q check G1–G7 PASS — label manifest still `research_eligible=False`, `eligibility_gate_status='pending'`, `stage_5_label_cleared=False`, `label_family_research_use_authorized=False`, `label_family_eligibility_gate_authorized=False`, `chronological_split_policy='not_yet_defined'`, all 8 non-authorization flags `False`, all 14 immutability flags `True`, `boundary_confirmations` all `True` with `len >= 17`. Manifest immutability re-hashed pre/post the gate run: byte-identical. | **PASS** |
| H | No manifest mutation is required inside this decision memo | Phase 4bm-R is docs-only; it does not touch any manifest; the v002 label manifest at SHA `5e17074d…` will remain byte-identical after Phase 4bm-R's commit; the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant remains preserved end-to-end and is never invoked. | **PASS** |
| I | No chronological split policy is needed to make the research-use decision itself | The research-use decision is upstream of any chronological-split-policy decision. The v001 precedent (Phase 4bj-F) made the research-use decision without defining chronological-split-policy; chronological-split-policy was left for a separately authorized later phase (`chronological_split_policy = "not_yet_defined"` on the label manifest is the correct pending state). | **PASS** |
| J | No diagnostics / ML / strategy / backtests are required or authorized by this decision | The decision is governance-level only. Diagnostics, ML, strategy, and backtests each require their own separately authorized phase prompts under Phase 4ak M0, Phase 4al refined no-rescue, the Phase 4aw invariant, and the operator workflow standards. | **PASS** |
| K | All non-authorization blocks remain intact | Reusable non-authorization blocks from `phase-risk-tiering-standard.md` §7 honored: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**, **N-SUCCESSOR-STATE** (no successor-state artefact created by Phase 4bm-R). **N-DERIVATION** does not apply — Phase 4bm-R is the explicitly authorized label-family research-use decision memo. | **PASS** |
| L | No data/microstructure artefact is committed | Phase 4bm-R writes no file under `data/microstructure/`. The only tracked files changed are this memo, the paired closeout, and the narrow `docs/00-meta/current-project-state.md` update. `git status --short` post-commit will show only the expected pre-existing untracked entries (`.claude/scheduled_tasks.lock` if present; `data/research/` if present); no `data/microstructure/` entry. | **PASS** |
| M | Retained verdicts and project locks are unchanged | H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread / V2 / G1 / C1 all preserved verbatim. §11.6 = 8 bps per side, round-trip = 16 bps, §1.7.3 = 0.25% / 2× / one-position / mark-price stops, Phase 4ak M0 twelve-clause gate, Phase 4al refined no-rescue rule, Phase 4aw `flip_research_eligible` always-raises invariant, Phase 4bb-F canonical sidecar/path policy, Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks, Phase 4bm-A-P1 context management standard, Phase 4bm-D-P1 lightweight Claude Code workspace standard — all preserved verbatim. | **PASS** |

**All thirteen criteria A–M are satisfied.** There is no missing structural evidence at the policy / governance layer.

## 8. Risk review

### 8.1 Residual structural risks

None observed. Each of the seven Phase 4bm-Q check groups (A–G) covered a distinct structural concern (locked preconditions, inventory, schema / lineage / forbidden-substring, row count / partition / timestamp, label semantics / censoring / value-domain, upstream immutability, non-authorization invariants) and each returned a clean 100% PASS. Upstream immutability was independently witnessed against 290 artefacts (20 governance lineage artefacts + 90 label parquets + 90 label sidecars + transitive 90 feature parquet SHA lineage via `source_feature_parquet_sha256`), all byte-identical pre/post Phase 4bm-Q's gate run.

### 8.2 Scope risks

- **Single-symbol scope.** The label family covers exactly BTCUSDT. Any future generalization claim to additional symbols is out of scope until additional symbols are separately authorized via additional acquisition + normalization + derived + feature + label phases. Phase 4bm-R does not authorize that.
- **90-day envelope scope.** The label family covers exactly 90 contiguous UTC days 2024-12-01 .. 2025-02-28 inclusive. Any future generalization claim to additional days or different date ranges is out of scope until separately authorized.
- **No predictive-validity claim.** Phase 4bm-R's recommendation makes no claim about label predictive value, signal quality, edge, profitability, or out-of-sample generalization. It is a governance signal about local artefact integrity and upstream consistency, not an empirical claim about edge or live readiness.

### 8.3 Process risks

- **Premature manifest mutation.** Mitigated by Phase 4bm-R being docs-only and by the Phase 4aw `flip_research_eligible(...)` always-raises invariant (never invoked).
- **Premature successor-state recording.** Mitigated by Phase 4bm-R's explicit non-authorization of any successor-state recording phase; any such recording requires a separately authorized phase prompt under the Phase 4bk-A workflow standard.
- **Scope creep into chronological-split-policy / diagnostics / ML / strategy / backtests.** Mitigated by explicit non-authorization §10 and the §1 required-exact-phrases lock-in.

### 8.4 Drift risk

If at any future time the Phase 4bm-Q gate report SHA stops matching `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` or the Phase 4bm-Q gate report sidecar SHA stops matching `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8`, or if any of the upstream SHAs cited in §6 drifts, Phase 4bm-R's recommendation must be re-validated before any future successor-state phase proceeds.

## 9. Non-authorization boundary

Phase 4bm-R is **docs-only**. It does NOT:

- modify source code, tests, scripts, configurations, `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, MCP files;
- modify the v002 label parquets / label manifest / label sidecars / Phase 4bm-Q gate report or sidecar / v002 feature manifest or sidecar / Phase 4bm-J feature-family gate report or sidecar / Phase 4bm-L feature-family successor-state JSON or sidecar / v002 derived/normalized manifest or sidecar / v002 raw manifest / v002 acquisition log / Phase 4bm-F derived successor-state / Phase 4bm-D derived gate report / Phase 4bl-D-R raw gate report / Phase 4bl-E raw successor-state / any prior gate report or successor-state artefact;
- create, write, rename, delete, or commit any file under `data/microstructure/`;
- rerun the normalizer, raw eligibility gate, derived-family gate, feature kernel, feature-family eligibility gate, label kernel, structural-QA inspector, or label-family eligibility gate;
- flip `research_eligible`, transition `eligibility_gate_status`, set `stage_5_label_cleared = true`, mark `label_family_research_use_authorized = true`, mark `label_family_eligibility_gate_authorized = true`, mark `stage_4_feature_cleared = true`, or change `chronological_split_policy` on any actual on-disk manifest;
- create a label-family successor-state JSON, a chronological-split-policy successor-state JSON, or any other successor-state artefact;
- acquire data, call any Binance / public / private endpoint, open any WebSocket, use any credential, read or create `.env` / `.mcp.json`, enable MCP or Graphify;
- revise any retained verdict, change any project lock, amend M0, amend Phase 4al, amend Phase 4aw, amend Phase 4bb-F, amend Phase 4bl-F, amend Phase 4bm-A-P1, amend Phase 4bm-D-P1, amend Phase 4bm-E / -F / -G / -H / -I / -J / -K / -L / -M / -N / -O / -P / -Q;
- authorize Phase 4bm-S (any provisional successor; not authorized), multi-day v002 label-family successor-state recording, multi-day v002 chronological-split-policy memo, multi-day v002 chronological-split-policy successor-state recording, multi-day v002 diagnostics, multi-day v002 ML training / model selection / feature ranking / meta-labeling, multi-day v002 strategy specification / implementation / signal construction, multi-day v002 backtest specification / plan / execution, additional acquisition (no additional days, no additional symbols, no mark-price / order-book / funding / OI / liquidation / cross-venue data, no aggTrades acquisition beyond the existing locked v002 90-day envelope), Phase 4bn-* / 4bo-* / 4bp-* / 4bq-*, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production-key creation, authenticated APIs, private endpoints, public-endpoint calls in code, user-stream / live WebSocket implementation, MCP / Graphify / `.mcp.json` / credentials.

**Phase 4bm-R does not mutate any manifest.**
**Phase 4bm-R does not create successor-state JSON.**
**Phase 4bm-R does not define chronological split policy.**
**Phase 4bm-R does not authorize diagnostics, ML, strategy, or backtests.**
**Phase 4bm-R does not authorize acquisition.**
**Phase 4bm-R does not commit data/microstructure.**

## 10. Decision

> **RECOMMEND_LABEL_RESEARCH_USE_AUTHORIZATION.**
>
> The multi-day v002 label family `microstructure_labels_aggtrades_v001 @ v002` (BTCUSDT × 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 rows; 40-column v002 label schema; `label_config_hash = 352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560`) is **admissible in principle at policy / governance level** for research-use, on the strength of the Phase 4bm-M boundary design + Phase 4bm-N schema finalization + Phase 4bm-O local label artefact generation + Phase 4bm-P `LABEL_STRUCTURAL_QA_PASS` + Phase 4bm-Q `LABEL_GATE_PASS` (60 / 60 at report level) evidence chain and the already-cleared upstream feature family (Phase 4bm-K → Phase 4bm-L `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`). The project may, separately and explicitly, authorize a future multi-day v002 label-family research-use successor-state recording phase (the multi-day v002 analogue of Phase 4bj-G) to record a machine-readable label-family research-use admissibility marker as a sibling successor-state JSON artefact, while preserving the original v002 label manifest byte-identically.
>
> **Phase 4bm-R itself does not mutate any manifest, does not create any successor-state JSON, does not define chronological split policy, does not authorize diagnostics / ML / strategy / backtests / acquisition, and does not commit any `data/microstructure/` file.** **Label-family research-use is not recorded by Phase 4bm-R.** **Any label-family research-use recording requires a separately authorized successor-state phase.** **Phase 4bm-S is not authorized by Phase 4bm-R.**

## 11. Rationale for the chosen decision

1. **All thirteen decision criteria are satisfied** (§7, criteria A–M). There is no missing structural evidence and no unresolved structural risk at the policy / governance layer.
2. **Strong v001 precedent.** Phase 4bj-F (the v001 label-family research-use / ML-use decision memo) selected the identical outcome ("admissible in principle at policy / governance level; no manifest mutation; successor-state required; explicit non-authorizations for ML / strategy / backtest / acquisition / paper / shadow / live; Phase 4bj-G is not authorized by Phase 4bj-F") on the basis of a 72 / 72 PASS Phase 4bj-E gate, which is structurally analogous to (and on a smaller single-day scope than) the 60 / 60 PASS Phase 4bm-Q gate.
3. **Strong sibling precedent.** The multi-day v002 feature family was handled by the identical pattern: Phase 4bm-J `FEATURE_GATE_PASS` (50 / 50 at report level) → Phase 4bm-K research-use decision memo (Outcome 1 / Decision form 1) → Phase 4bm-L successor-state recording (sibling successor-state JSON SHA `7eccaa8f…`; original feature manifest byte-identical). The Phase 4bm-R recommendation extends that pattern to labels under identical safeguards.
4. **No new permissions granted.** The recommendation does not unlock ML, strategy, backtests, acquisition, diagnostics, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation. The forbidden / unauthorized state of the v002 label manifest's governance fields remains intact. The Phase 4aw `flip_research_eligible(...)` always-raises invariant is preserved end-to-end and is never invoked by Phase 4bm-R.
5. **Conservative successor.** A future separately authorized successor-state recording phase, if proposed, would be docs + local-gitignored-output only, would preserve the original label manifest byte-identically (SHA `5e17074d…` unchanged), and would not lift any forbidden flag on the manifest. The sibling successor-state JSON would be the only machine-readable indicator of label-family research-use admissibility, and it would live outside the manifest under `data/microstructure/successor-state/labels/` (gitignored), mirroring the Phase 4bm-L feature-family layout.
6. **Reversible.** If at any future time the recommendation is found to be unsound — for example, if a subsequent inspection reveals a structural defect not caught by the 60-check Phase 4bm-Q gate — Phase 4bm-R can be superseded by a subsequent docs-only memo without rolling back any artefact (because no artefact was mutated).

Other decision options considered:

- **DO_NOT_RECOMMEND_LABEL_RESEARCH_USE_AUTHORIZATION.** Would be appropriate only if a structural defect were found in the label family or if a missing evidence link in the predecessor chain existed. Neither condition holds (criteria A–M PASS in §7). Not selected.
- **DEFER_LABEL_RESEARCH_USE_AUTHORIZATION_PENDING_SPECIFIC_REMEDIATION.** Would be appropriate if a specific concrete remediation step were identifiable as a precondition for admissibility (e.g., an additional structural check, a missing lineage SHA, a documented schema ambiguity). No such concrete remediation is identifiable on the present evidence. Not selected.

## 12. What a future successor-state recording phase would be allowed to do (if separately authorized)

A future multi-day v002 label-family research-use successor-state recording phase (informally referred to as Phase 4bm-S; **not** authorized by Phase 4bm-R), if separately authorized by the operator and only under explicit ex-ante authorization, would be allowed to:

1. **Produce exactly one sibling successor-state JSON** under a gitignored namespace (mirroring the Phase 4bm-L feature-family layout — likely `data/microstructure/successor-state/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-s__<timestamp_ms>__<code_commit_sha_prefix>.json` or whichever path layout the prevailing Phase 4bb-F output-path-hygiene policy mandates at that time).
2. **Produce a paired canonical Phase 4bb-F sidecar** matching the artefact's bytes (`<basename>  \\n` two-space format; ASCII / UTF-8 no BOM; LF only).
3. **Cite verbatim** the Phase 4bm-Q gate report id, the Phase 4bm-Q gate report SHA256 `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e`, the Phase 4bm-Q gate report sidecar SHA256 `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8`, the v002 label manifest SHA `5e17074d…`, the v002 label manifest sidecar SHA `451d5b88…`, `label_config_hash = 352bad41…`, `feature_config_hash = 819cfa7a…`, the v002 feature manifest SHA `512a0a54…`, the Phase 4bm-J feature-family gate report SHA `3c59dfae…`, the Phase 4bm-L feature-family successor-state SHA `7eccaa8f…`, the v002 derived manifest SHA `01c5fa53…`, the v002 raw manifest SHA `01696786…`, the Phase 4bm-D derived gate report SHA `3b45e70b…`, the Phase 4bm-F derived successor-state SHA `72b6edd4…`, the Phase 4bl-D-R raw gate report SHA `f9493fd1…`, the Phase 4bl-E raw successor-state SHA `a0576ca6…`, and this Phase 4bm-R decision memo as the policy-decision evidence.
4. **Record `successor_research_eligible = true`** (or whatever final field name is chosen by that phase's design memo) **only on the sibling successor-state artefact**, never on the manifest.
5. **Record `successor_eligibility_gate_status = pass`** (or equivalent) **only on the sibling successor-state artefact**, never on the manifest.
6. **Preserve the v002 label manifest byte-identically** at SHA `5e17074d…`.
7. **Preserve the v002 label manifest sidecar byte-identically** at SHA `451d5b88…`.
8. **Preserve all 90 v002 label parquet SHAs byte-identically.**
9. **Preserve all 90 v002 label parquet sidecar SHAs byte-identically.**
10. **Preserve the Phase 4bm-Q gate report and sidecar byte-identically.**
11. **Preserve the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant** end-to-end (never invoked).
12. **Preserve every retained verdict and project lock** verbatim.

## 13. What this phase does not authorize

Phase 4bm-R does **not**, and **cannot**, authorize any of the following, even by implication:

- **Phase 4bm-S** — any future multi-day v002 label-family research-use successor-state recording (provisional naming only; **not** authorized by Phase 4bm-R). Per Phase 4bk-A, that phase requires a separately authorized operator prompt with explicit scope, name, constraints, and acceptance criteria.
- **Phase 4bm-T+ / 4bn-* / 4bo-* / 4bp-* / 4bq-*** — any subsequent multi-day v002 chronological-split-policy memo, chronological-split-policy successor-state recording, diagnostics, ML training, model selection, feature ranking, meta-labeling, strategy specification / implementation / signal construction, backtest specification / plan / execution, or any further family-level governance work.
- **Phase 5** — any successor numbered phase. **Phase 4 canonical** — any canonical Phase 4 runtime / orchestration / strategy / signal / execution / risk / persistence / deployment / paper / shadow / live work.
- **Manifest mutation** — no manifest field transition on the v002 label manifest, v002 feature manifest, v002 derived/normalized manifest, v002 raw manifest, or any prior manifest.
- **Successor-state JSON creation** — no successor-state JSON of any kind created by Phase 4bm-R itself.
- **Chronological split policy definition** — no `chronological_split_policy` definition or change on any actual on-disk manifest.
- **Diagnostics implementation or execution.**
- **ML implementation, training, model selection, feature ranking, meta-labeling, or any other ML work.**
- **Strategy implementation, signal generation, position-state machine, entry / exit rules, or any other strategy logic.**
- **Backtest implementation, simulator, walk-forward harness, or any other backtest execution.**
- **Additional data acquisition** — no aggTrades / 5m / 1m / tick / mark-price / order-book / spot / cross-venue / multi-day-beyond-90 / multi-symbol / additional-symbol acquisition.
- **Public-endpoint calls in code; Binance API calls (public or authenticated); WebSocket connections; user-stream subscriptions.**
- **Credentials creation, storage, or use; `.env` read or write; `.mcp.json` read or write; MCP enable or configure; Graphify enable or configure.**
- **Production-key creation, scoping, rotation; exchange-write capability; live-readiness preparation; deployment work.**
- **Amendment** of Phase 4ak M0 twelve-clause gate, post-null cooldown rule, cooled-down families list, M0 memo template, Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy, Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant, Phase 4bb-F canonical sidecar/path policy, Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks, Phase 4bm-A-P1 thin-prompt context-management standard, Phase 4bm-D-P1 lightweight Claude Code workspace standard, or any prior Phase 4bm-* phase.
- **Revision** of any retained verdict (H0, R3, R1a, R1b-narrow, R2, F1, D1-A, 5m thread, V2, G1, C1).
- **Loosening** of any project lock (§11.6 = 8 bps per side, round-trip = 16 bps, §1.7.3 = 0.25% / 2× / one-position / mark-price stops, all other locks recorded in `current-project-state.md` and the latest merge-closeout).

**Any label-family research-use recording requires a separately authorized successor-state phase.**
**Phase 4bm-S is not authorized by Phase 4bm-R.**

## 14. Retained verdicts preserved

All retained verdicts preserved verbatim by Phase 4bm-R:

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED per Phase 3t
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

## 15. Project locks preserved

All project locks preserved verbatim by Phase 4bm-R:

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% risk per trade / 2× leverage cap / one-position max / mark-price stops
- Phase 3p §4.7
- Phase 3r §8
- Phase 3v §8 stop-trigger-domain governance
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance
- Phase 4j §11 metrics OI-subset partial-eligibility rule
- Phase 4k
- Phase 4p
- Phase 4q
- Phase 4v
- Phase 4w
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (never invoked by Phase 4bm-R)
- Phase 4bb-F canonical sidecar / path policy
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks
- Phase 4bm-A-P1 thin-prompt context-management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace standard
- All other locks recorded in `current-project-state.md` and the latest merge-closeout

All prior phase results (Phase 4am .. Phase 4bm-Q) preserved verbatim.

## 16. Recommended next state

**Remain paused** unless the operator separately authorizes the conditional-next phase below.

Phase 4bm-R is docs-only. It records a policy-level admissibility recommendation. It does not authorize any successor phase. **Phase 4bm-S is not authorized by Phase 4bm-R.** Per the Phase 4bk-A workflow standard, every successor phase requires a separately authorized operator prompt with explicit scope, name, constraints, and acceptance criteria.

### Conditional next, NOT authorized

| Option | Type | Status |
| --- | --- | --- |
| **Primary** — remain paused | docs-only / no work | **recommended** |
| **Conditional next** — future operator-authorized Phase 4bm-R merge phase (recording Phase 4bm-R on `main` per `merge-closeout-standard.md` Tier 1 ceremony) | docs + merge | **NOT authorized by this memo** |
| **Conditional later** — future operator-authorized multi-day v002 label-family research-use successor-state recording phase (multi-day analogue of Phase 4bj-G), only if the operator separately authorizes such a phase under explicit scope | docs + local gitignored successor-state | **NOT authorized by this memo** |
| **Conditional later** — future operator-authorized multi-day v002 chronological-split-policy memo (multi-day analogue of Phase 4bj-H / -I) | docs-only | **NOT authorized by this memo** |
| **Conditional later** — future operator-authorized multi-day v002 chronological-split-policy successor-state recording (multi-day analogue of Phase 4bj-J) | docs + local gitignored successor-state | **NOT authorized by this memo** |
| Additional acquisition (additional days / symbols / data families beyond the 90 locked v002 dates) | docs + data | **NOT authorized; not in scope** |
| Diagnostics / ML / strategy / backtest work on v002 (or v001) | code + data | **FORBIDDEN by Phase 4bm-R** |
| Paper / shadow / live / exchange-write / production keys / authenticated APIs / private endpoints / WebSocket implementation / MCP / Graphify / `.mcp.json` / credentials | runtime | **FORBIDDEN by Phase 4bm-R** |

**Recommended state: remain paused.**

**No successor phase is authorized by Phase 4bm-R.**
