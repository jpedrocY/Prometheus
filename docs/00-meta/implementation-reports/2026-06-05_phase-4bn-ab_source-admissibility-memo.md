# Phase 4bn-AB — Source-Admissibility Memo

## 1. Purpose

This is a **docs-only** source-admissibility memo for the conservative
pre-v002-only research path. It answers one governance question:

> Can the locally produced and locally gated pre-v002 normalized / feature /
> label stack be treated as a **source-admissible** input for future ML
> dataset-contract work or future ML dataset construction — and if so, under
> exactly what restrictions, without mutating manifests, flipping
> `research_eligible`, setting `chronological_split_policy`, or violating the
> Phase 4aw `flip_research_eligible(...)` always-raises invariant? If not, what
> exact blocker remains and what is the next step?

The memo **records a governance verdict** and **defines admissibility
vocabulary**. It authorizes none of the downstream actions it discusses. It
implements nothing in code, reads no local data, creates no artefact, mutates no
manifest, flips no eligibility flag, sets no `chronological_split_policy`, and
authorizes no successor. Its conclusions are determined from committed
documentation and committed source read read-only; every figure carried forward
comes from predecessor implementation reports already merged to `main`.

Phase 4bn-Z identified source admissibility as the gating blocker for any data
use (its §12). Phase 4bn-AA built the pure-code pre-v002 split-policy artefact
with offline tests and no data I/O, and recommended this memo. This memo
**resolves the governance meaning** of "admissible source" for the conservative
pre-v002 path — without reading or mutating the data.

---

## 2. Authority and repository state

- **Phase:** 4bn-AB — Source-Admissibility Memo.
- **Authorization:** separately authorized by the operator following the Phase
  4bn-AA decision
  `RECOMMEND_AUTHORIZE_SOURCE_ADMISSIBILITY_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Branch:** `phase-4bn-ab/source-admissibility-memo`.
- **Base `main` SHA:** `e749598dcdcbfaec1a69f8a4f8f0620e68a25c8a`
  (`docs(phase-4bn-aa): finalize merge closeout shas`).
- **Pre-branch sync:** `HEAD == main == origin/main == e749598d…` verified.
- **Predecessors present on `main`:** Phase 4bn-AA SHA-finalization `e749598`,
  merge-closeout `6cfbf68`, merge `451a51e`, branch `e12e928`; Phase 4bn-Z
  finalization `d9e699e` present as predecessor.
- **Remote:** `https://github.com/jpedrocY/Prometheus.git`.
- **Gitignored data namespaces:** `data/microstructure/` (`.gitignore:85`) and
  `data/research/` (`.gitignore:88`) — both confirmed; both remain uncommitted.

This phase is branch-complete only by its own work; it is **not merged into
`main`** and is **not project-complete**. It becomes project-complete only when
a separately authorized merge phase records its merge-closeout on `main`.

---

## 3. Phase type and strict scope

**Phase type:** docs-only / source-admissibility / eligibility-governance /
ML-data-use-precondition / no-flag-flip memo.

**Tier:** Tier 1 — Full Phase per
`docs/00-meta/process/phase-risk-tiering-standard.md` §3, because the phase
decides how the locally produced and locally gated pre-v002 normalized / feature
/ label stack may become admissible, or not admissible, as a future ML
dataset-construction source without violating the project's eligibility
governance, the Phase 4aw `flip_research_eligible(...)` always-raises invariant,
sealed-test protections, or the no-rescue constraints.

**Strictly out of scope (this phase does none of these):** add code, tests, or
scripts; create or mutate any manifest, sidecar, gate report, split file,
research matrix, ML dataset, ML config, or successor-state artefact; read any
local data (raw zip, normalized / feature / label Parquet, manifest, gate
report, sidecar, v002 terminal file, or sealed-test file); create any local
artefact under `data/microstructure/` or `data/research/`; flip
`research_eligible`; transition `eligibility_gate_status`; set
`chronological_split_policy` in any manifest; invoke or alter the Phase 4aw
`flip_research_eligible(...)` invariant; train / score / predict; run
diagnostics, strategy, signals, PnL, or backtests; or authorize any successor.

---

## 4. Evidence base and input boundary

**Admissible evidence (read-only) used for this memo:**

- Committed process standards (`merge-closeout-standard`,
  `phase-risk-tiering-standard`, `phase-workflow-standard`,
  `phase-prompt-template`, `operator-report-standard`) and
  `current-project-state.md`.
- Committed Phase 4bn-L / 4bn-O / 4bn-P / 4bn-S / 4bn-T / 4bn-U / 4bn-V / 4bn-W
  / 4bn-X / 4bn-Y / 4bn-Z / 4bn-AA implementation reports, merge-closeouts, and
  closeouts (the source of every figure carried forward in §6 – §7).
- Committed source, read-only, for governance grounding:
  `src/prometheus/research/microstructure/manifest.py` (the Phase 4aw
  `flip_research_eligible(...)` always-raises invariant),
  `pre_v002_split_policy.py`, `diagnostics_split_policy_v002.py`,
  `ml_baseline_design_v002.py`, `ml_baseline_dataset_v002.py`,
  `labels_schema_v002.py`, `features_schema_v002.py`, plus the eligibility-field
  surface (`labels_manifest_v002.py`, `features_manifest_v002.py`,
  `multiday_feature_gate_report.py`, `multiday_label_gate_report.py`).
- The Phase 4bn-AA offline test
  (`tests/research/microstructure/test_phase4bn_aa_pre_v002_split_policy.py`).

**Input boundary (not read):** no local Parquet (raw / normalized / feature /
label); no local raw zip; no local manifest or gate report under
`data/microstructure/`; no v002 terminal raw / normalized / feature / label
window; no sealed-test file; no `data/research/` output. `README` is treated as
potentially stale and is **not** used as a current-state authority.

A committed-repository term search confirms the field separation this memo
relies on: `research_eligible`, `eligibility_gate_status`,
`chronological_split_policy`, `ml_authorized`, `diagnostics_authorized`, and
`no_successor_authorization` are **real manifest / gate-report fields** in the
microstructure code; `source_admissib*` does **not** appear anywhere in the
microstructure source. Source admissibility is therefore a **memo-level
governance concept defined here**, not an existing or new manifest field.

---

## 5. Existing eligibility governance and the Phase 4aw invariant

The project's eligibility governance is anchored by the Phase 4aw scaffold in
`src/prometheus/research/microstructure/manifest.py`:

- `MicrostructureManifest` defaults `research_eligible = False` and
  `eligibility_gate_status = EligibilityGateStatus.PENDING`.
- `MicrostructureManifest.flip_research_eligible(...)` **always raises**
  `ManifestImmutableError`. Its docstring states: "Phase 4aw does not implement
  the eligibility gate. Manifests must remain `research_eligible=False` until a
  separately authorized future phase adds a real gate." Only "the future
  eligibility gate (separately authorized) may do so."
- That gate **is not implemented** anywhere in the committed repository.

Downstream artefacts carry and re-assert this invariant as a verifiable flag:
the v002 feature/label manifests and the multiday feature/label gate reports all
record `phase_4aw_flip_research_eligible_invariant_preserved: True`,
`research_eligible=false`, `eligibility_gate_status='pending'`,
`ml_authorized=false`, `diagnostics_authorized=false`, and
`chronological_split_policy='not_yet_defined'` /
`set_manifest_chronological_split_policy: False`. The pre-v002 layer gates
(4bn-P / 4bn-T / 4bn-X) reproduced the same non-eligible posture for the
pre-v002 segment.

**Governance reading (decisive for this memo).** The Phase 4aw invariant
forbids exactly one thing: flipping the **manifest** field `research_eligible`
to `True` through anything other than a separately authorized future eligibility
gate. It does **not** forbid the project from *describing*, in a docs-only memo,
the conditions under which the gated source stack may later be used. A
documentation verdict that records "this stack is admissible as an input to a
future **docs-only** dataset-contract design step, but not yet admissible for
data reads" changes no manifest field, calls no `flip_research_eligible(...)`,
and therefore cannot and does not violate the invariant. This is the same
position Phase 4bn-Z §12 took: admissibility "is not 'flip the flag'; it is
whatever the project's eligibility governance defines as the admissibility
decision, recorded through the proper channel."

---

## 6. Layer-integrity evidence carried forward

All figures below are quoted from the merged Phase 4bn-O … 4bn-X reports; no
local artefact was read to obtain them.

| Layer | Phase | Files | Rows | Footprint (B) | Manifest / config SHA | Gate verdict |
|---|---|---|---|---|---|---|
| Normalized | 4bn-O / 4bn-P | 275 | 400,001,695 | 3,954,532,918 | manifest `0e96ae37…d9fa` | `NORMALIZED_LAYER_GATE_PASSED…` 25/25; report `3452fd9d…f134` |
| Feature | 4bn-S / 4bn-T | 275 | 400,001,695 | 54,254,406,538 | manifest `4881eb87…9b52`; `feature_config_hash 0726b41d…114c` | `FEATURE_LAYER_GATE_PASSED…` 27/27; report `db731d1b…6ab08` |
| Label | 4bn-W / 4bn-X | 275 (+275 sidecars) | 400,001,695 | 15,654,082,679 | manifest `69746c88…b161`; `label_config_hash b3bd5d2b…8970`; sidecar `636a4c1a…8239` | `LABEL_LAYER_GATE_PASSED…` 40/40; report `ffb5b09…8984`; report sidecar `68dd5b57…1997b984`-class |

- Segment span: **2024-03-01 .. 2024-11-30 inclusive UTC (275 dates)**.
- Label envelope terminal: `envelope_terminal_unix_ms = 1733011199331`
  (`envelope_terminal_utc_date 2024-11-30`).
- Per-horizon censored counts: 1s = 3 / 5s = 20 / 15s = 42 / 60s = 216;
  invalid-price rows = 0.
- Every layer is `research_eligible = false`,
  `eligibility_gate_status = pending`, `no_successor_authorization = true`.

**Layer-integrity verdict: TRUE.** All three layers exist locally and passed
their read-only eligibility gates. A passing layer gate proves byte-integrity,
schema conformance, lineage binding, and boundary/censoring correctness only. It
does **not** confer research eligibility and does **not** by itself confer
admissibility for ML use. Layer integrity is necessary but not sufficient for
admissibility.

---

## 7. Phase 4bn-Y / Z / AA readiness chain carried forward

- **Phase 4bn-Y** recorded the chronological split / holdout policy
  (`RECORD_CHRONOLOGICAL_SPLIT_POLICY__REMAIN_PAUSED`): Candidate A —
  `CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`; Train
  2024-03-01..2024-09-30 (214) / embargo 2024-10-01 / Validation
  2024-10-02..2024-11-15 (45) / embargo 2024-11-16 / internal holdout
  2024-11-17..2024-11-30 (14); 214 + 1 + 45 + 1 + 14 = 275; assignment by
  `source_transact_time_ms` UTC date; chronological-only; 1-day boundary purge
  over a formal ≥ 60 s row-level earlier-split floor; v002 terminal and
  published v002 labels by reference only and unread; sealed test
  (2025-02-14..2025-02-28) fully sealed, `test_rows_loaded=0`; full-envelope
  assembly and holdout-boundary memo **not required** for the conservative
  pre-v002-only path; censored labels not imputed; invalid labels
  rejected/filtered.
- **Phase 4bn-Z** recorded ML-baseline readiness
  (`ML_BASELINE_READINESS_RECORDED__PRE_V002_PATH_READY_FOR_SPLIT_POLICY_ARTEFACT__REMAIN_PAUSED`):
  policy-ready but **not** implementation-ready for ML; ML training / ML dataset
  creation / research-matrix creation all **not ready**; split-policy artefact
  required; **source admissibility unresolved (yes)**; full-envelope assembly and
  holdout-boundary memo **not required** for the first conservative
  pre-v002-only path. Its §12 named source admissibility as the gating blocker
  for any data use and explicitly declined to solve it.
- **Phase 4bn-AA** implemented the pre-v002 split-policy artefact
  (`PRE_V002_SPLIT_POLICY_ARTEFACT_IMPLEMENTED__NO_DATA_IO__REMAIN_PAUSED`):
  module `pre_v002_split_policy.py` + offline test (70 tests) encoding Candidate
  A exactly; pure date/window arithmetic; no data I/O; `split_for_date` raises
  for any date outside 2024-03-01..2024-11-30, including the entire v002 terminal
  and sealed-test windows. It set no `chronological_split_policy` manifest field
  (`set_manifest_chronological_split_policy: False`,
  `no_successor_authorization: True`) and never invoked the Phase 4aw invariant.

The chain O/P/S/T/W/X established **local layer integrity**; Y recorded the
**split policy**; Z established **policy-readiness** and named source
admissibility as the remaining blocker; AA **operationalized the split policy in
code** with no data use. The one unresolved governance item standing between this
chain and the next docs-only ML step is the source-admissibility question this
memo resolves.

---

## 8. Source-admissibility question

The memo must distinguish four concepts that are routinely conflated:

1. **Layer integrity** — the normalized / feature / label layers exist locally
   and their layer gates passed. *(Structural / lineage / schema / hash /
   boundary integrity only.)*
2. **Source admissibility** — whether those local layers may be **used as future
   ML dataset-construction inputs** under governance, and for which *kind* of
   future step.
3. **Manifest eligibility** — the actual manifest fields
   `research_eligible=false`, `eligibility_gate_status=pending`,
   `chronological_split_policy=not set`.
4. **Authorization** — whether any successor phase, dataset builder, data read,
   ML, diagnostics, strategy, PnL, or backtest is authorized.

Layer integrity (1) is established. This memo decides (2). It must do so without
touching (3) and without granting any of (4). The central subtlety is that
"source admissibility" is **not a single yes/no**: a stack can be admissible as
an input to a **docs-only contract design** (which reads no data) while remaining
**inadmissible for actual data reads, dataset building, and training**. This memo
makes that split explicit.

---

## 9. Admissibility vocabulary and field separation

This memo defines the following terms. Terms 1–7 are **memo-level governance
concepts** (recorded by documentation; they are *not* manifest fields and do not
mutate anything). Terms 8–10 name the **actual manifest / gate-report fields**
that this memo must leave unchanged.

| # | Term | Kind | Meaning | Value from this memo | Recorded by |
|---|---|---|---|---|---|
| 1 | `layer_integrity_passed` | memo concept | normalized / feature / label artefacts exist locally and passed their layer gates | **true** | documentation only |
| 2 | `source_admissible_for_dataset_contract` | memo concept | committed evidence is sufficient to **design** the ML dataset contract in a future **docs-only** phase (no data read) | **true** | documentation only |
| 3 | `source_admissible_for_data_read` | memo concept | a future phase may **read** feature/label data | **false / not yet** | requires a future separately-authorized dataset-builder phase |
| 4 | `source_admissible_for_dataset_builder` | memo concept | a future phase may **implement / run** a dataset builder | **false / not yet** | requires contract + budget preflight + leakage proof + separate authorization |
| 5 | `ml_authorized` | memo concept (mirrors a manifest flag) | model training / scoring / predictions permitted | **false** | future gate + authorization; manifest flag stays `false` |
| 6 | `diagnostics_authorized` | memo concept (mirrors a manifest flag) | diagnostics over outputs / labels / features permitted | **false** | future gate + authorization; manifest flag stays `false` |
| 7 | `strategy_backtest_authorized` | memo concept | strategy / signal / PnL / backtest permitted | **false** | future authorization |
| 8 | `manifest_research_eligible` | **manifest field** | actual `research_eligible` flag | **false (unchanged)** | future eligibility gate only (Phase 4aw invariant) |
| 9 | `manifest_eligibility_gate_status` | **manifest field** | actual `eligibility_gate_status` | **pending (unchanged)** | future eligibility gate only |
| 10 | `manifest_chronological_split_policy` | **manifest field** | actual `chronological_split_policy` | **not set (unchanged)** | future dataset/gate phase only |

**Name for the recorded posture.** The governance posture this memo records is
`source_admissibility_recorded` with `source_admissible_for_dataset_contract =
true` and every data-touching admissibility (`source_admissible_for_data_read`,
`source_admissible_for_dataset_builder`, `ml_authorized`,
`diagnostics_authorized`, `strategy_backtest_authorized`) **false**. This posture
is a **memo result only** — never a manifest field, never an eligibility
transition.

**Which may be recorded by documentation only:** terms 1–7 (this memo records
1 = true, 2 = true, 3–7 = false). **Which require code or manifest mutation:**
8–10 (a real future eligibility gate / dataset phase) — none performed or
authorized here. **Which remain forbidden:** flipping 8 (`research_eligible`),
transitioning 9, or setting 10 by anything other than a separately authorized
future gate; and every data-touching action behind 3–7.

---

## 10. Manifest-state preservation

This memo performs no manifest action. After this phase, byte-identically to
before it:

- **`manifest_research_eligible` = false** at every pre-v002 layer (normalized
  `0e96ae37…`, feature `4881eb87…`, label `69746c88…`).
- **`manifest_eligibility_gate_status` = pending** at every layer.
- **`manifest_chronological_split_policy` = not set / not transitioned** in any
  manifest (`set_manifest_chronological_split_policy` remains `False`).
- **`no_successor_authorization` = true** preserved.
- The Phase 4aw `flip_research_eligible(...)` always-raises invariant is
  **preserved and was never invoked**.

No manifest, sidecar, gate report, or successor-state artefact was read,
created, or mutated.

---

## 11. Source-admissibility verdict

**Verdict.** The completed local evidence chain O/P/S/T/W/X/Y/Z/AA makes the
pre-v002 normalized / feature / label stack **source-admissible for future
docs-only ML dataset-contract design only**, and **not** admissible for actual
data reads, dataset-builder implementation, ML training, scoring, predictions,
diagnostics, strategy, PnL, or backtests.

Reasoning, mapped to the readiness questions:

1. **Admissible as a source for ML dataset-contract design?** **Yes.** A dataset
   contract is a docs-only specification; designing it reads no data, builds no
   dataset, and confers no eligibility. The committed evidence — three passed
   layer gates with byte-verified manifests/hashes, the recorded split policy,
   and now the code-level split artefact — is sufficient to specify a contract by
   reference to those committed SHAs without touching the data.
2. **Admissible for dataset-builder implementation?** **No / not yet.** A builder
   reads feature/label Parquet; that is a data read and is blocked.
3. **Admissible for actual data reads?** **No / not yet.** Blocked until a
   separately-authorized dataset-builder phase binds to the passed gates, the
   split artefact, the source scope, a budget preflight, and a leakage proof.
4. **Admissible for ML training?** **No.** `ml_authorized = false`; training sits
   behind every prerequisite in §18 – §20.
5. **Difference between "source-admissible by governance memo" and manifest
   `research_eligible=true`?** A memo-level admissibility verdict is a *recorded
   documentation conclusion about permitted future use*; it changes no manifest
   field and grants no data access. `research_eligible=true` is a *manifest state
   transition* reserved exclusively to a future separately-authorized eligibility
   gate under the Phase 4aw invariant. The first never implies the second.
6. **Can a memo record an admissibility decision without mutating manifests?**
   **Yes** — that is exactly what this memo does; the decision lives in
   documentation, not in any manifest.
7. **Name for that posture?** `source_admissibility_recorded` /
   `source_admissible_for_dataset_contract = true` (memo result, not a field).
8. **If no, what gate/artefact would be required?** Not applicable to the
   contract-design step. For *data use*, a future code-level dataset-builder
   phase with contract + budget preflight + leakage / split-integrity proof is
   required (and, before any eligibility flip, the still-unimplemented Phase 4aw
   eligibility gate).
9. **Does the Phase 4aw invariant forbid all admissibility, or only the manifest
   flip?** **Only the manifest flip.** It forbids flipping `research_eligible`
   outside a future gate; it does not forbid a docs-only admissibility verdict
   that grants no data access.

This is the preferred conservative conclusion permitted by the repository
evidence: admissible for the next docs-only step, not for data use.

---

## 12. Scope admitted for future docs-only dataset-contract design

A future **docs-only** ML dataset-contract memo may, **by reference only**,
specify a dataset contract over:

- **Instrument / source:** BTCUSDT / Binance USDⓈ-M futures / aggTrades **only**.
- **Dates:** pre-v002 **only**, 2024-03-01 .. 2024-11-30 inclusive UTC
  (275 dates).
- **Feature source:** the Phase 4bn-S feature segment (manifest `4881eb87…`,
  `feature_config_hash 0726b41d…`), by reference only.
- **Label source:** the Phase 4bn-W label segment (manifest `69746c88…`,
  `label_config_hash b3bd5d2b…`), by reference only.
- **Split contract:** the Phase 4bn-Y Candidate A policy as operationalized by
  the Phase 4bn-AA `pre_v002_split_policy.py` artefact (214 / 45 / 14;
  embargo 2024-10-01 and 2024-11-16; chronological-only; ≥ 60 s floor + 1-day
  purge; hard v002/sealed exclusion).
- **Targets / features / filtering:** the Phase 4bn-Z §13 – §15 envelope —
  per-horizon `forward_direction_<H>` / `forward_log_return_<H>` as targets;
  the 45 causal computed `FEATURE_SCHEMA_V002` columns as features (17 lineage +
  label/support/split/censor columns excluded); drop censored / null targets;
  reject invalid-price rows; never impute targets.
- **Leakage / split-integrity proof obligations** the eventual builder must
  satisfy (Phase 4bn-Z §16) and the **budget preflight** (Phase 4bn-L caps; D:
  thresholds) it must pass — specified at contract level, executed by nobody
  here.

The contract memo **reads no data**: it names committed SHAs and the split
artefact, and specifies obligations. It is the recommended next step (§22).

---

## 13. Scope not admitted for data reads

The pre-v002 stack is **not** admissible for any data read. Until a future
separately-authorized dataset-builder phase exists (binding to the passed gates,
the split artefact, the source scope, a budget preflight, and a leakage proof),
no phase may open or stream any pre-v002 normalized / feature / label Parquet,
manifest, sidecar, or gate report for ML dataset construction.
`source_admissible_for_data_read = false`.

---

## 14. Scope not admitted for dataset builder / research matrix

No ML dataset builder and no research matrix is admissible or authorized.
`source_admissible_for_dataset_builder = false`. The committed ML-baseline
tooling (`ml_baseline_design_v002.py`, `ml_baseline_dataset_v002.py`,
`diagnostics_split_policy_v002.py`) is hardcoded to the v002 terminal (90
partitions / 155,153,449 rows / `feature_config_hash 819cfa7a…` /
`CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`) and is inadmissible to the
pre-v002 segment; `ml_baseline_splits.py` and `ml_baseline_train.py` do not
exist. A future pre-v002 builder would be a new segment-scoped artefact and is
neither built nor authorized here.

---

## 15. Scope not admitted for ML training / scoring / predictions

No model training, scoring, or prediction is admissible or authorized.
`ml_authorized = false`; `diagnostics_authorized = false`;
`strategy_backtest_authorized = false`. These remain blocked behind the full
prerequisite set in §20 and would each require separate authorization even after
the prerequisites are met.

---

## 16. v002 terminal and sealed-test boundary

- **v002 terminal (2024-12-01 .. 2025-02-28):** by reference only; unread;
  inadmissible to the conservative first ML-baseline path. Published v002
  normalized / feature / label families remain byte-for-byte immutable and
  unread.
- **Sealed test (2025-02-14 .. 2025-02-28):** fully sealed; `test_rows_loaded=0`;
  untouched; single-use, future-authorization only. The pre-v002 internal holdout
  (2024-11-17 .. 2024-11-30) is **not** the sealed test and may never be used for
  final / strategy / production claims.

**No v002 terminal or sealed-test data may be read** under this memo or under the
recommended docs-only contract memo. Source admissibility for the conservative
pre-v002 path requires no v002 terminal read and no sealed-test read.

---

## 17. Full-envelope and holdout-boundary posture

- **Full-envelope assembly is NOT required** for the first conservative
  pre-v002-only path (consistent with Phase 4bn-Y / Z). It would be required only
  before a future pre-v002 + v002 combined path, which is deferred and
  unauthorized.
- **A holdout-boundary memo is NOT required** for the first conservative
  pre-v002-only path; the path touches neither the v002 terminal nor the
  sealed-test dates. It would be required only if a future scope reads the v002
  terminal or sealed-test dates.
- **No additional data scan is required** before the next docs-only step. The
  completed layer gates (25/25, 27/27, 40/40) — the label gate having performed a
  full per-row scan of all 275 label Parquets — already provide the integrity
  evidence the contract memo references; the contract memo reads no data.

---

## 18. Remaining blockers before data reads

Before any pre-v002 **data read** for ML purposes:

1. An **ML dataset contract** (the recommended next docs-only step) specifying
   targets, features, filtering, split binding, leakage obligations, and budget
   preflight.
2. A **code-level dataset builder** that binds to the passed gates (`3452fd9d…` /
   `db731d1b…` / `ffb5b09…`), the manifests/hashes (`0e96ae37…` / `4881eb87…` +
   `0726b41d…` / `69746c88…` + `b3bd5d2b…`), and the Phase 4bn-AA split artefact.
3. A **leakage / split-integrity proof** (Phase 4bn-Z §16) and a **budget
   preflight** (Phase 4bn-L caps; D: ≥ 500 GiB before / fail closed < 350 GiB
   during).
4. **Separate operator authorization** for the data-reading phase. Source
   admissibility for data reads stays `false` until all of the above exist.

---

## 19. Remaining blockers before dataset builder

Before a dataset builder may be **implemented or run**: a recorded dataset
contract (the obligations a builder must satisfy), the §18 leakage proof and
budget preflight bound into the builder, and separate authorization. The builder
must write outputs local and gitignored only, commit nothing, flip no
eligibility, and carry the full non-authorization evidence block.

---

## 20. Remaining blockers before ML training

ML training on the pre-v002 path stays blocked until **all** of the following are
each separately satisfied and authorized (Phase 4bn-Z §20, carried forward and
unchanged):

1. ML-baseline readiness memo recorded (**done, 4bn-Z**).
2. Code-level pre-v002 split-policy artefact + offline tests (**done, 4bn-AA**).
3. **Source admissibility resolved** for the relevant step — this memo resolves
   it **for docs-only dataset-contract design only**; admissibility for data
   reads / dataset building / training remains **unresolved / false**.
4. An ML dataset contract / builder with its leakage / split-integrity proof.
5. A budget preflight for dataset construction.
6. A per-task target / horizon / filtering decision.
7. A committed end-to-end trainer (does not exist; a later separately-authorized
   phase even after 1 – 6).

---

## 21. Candidate next phases considered

- **(A) ML dataset contract memo (docs-only).** Reads no data; leans on the now
  fully-assembled evidence chain (three passed gates + recorded split + code
  split artefact + this admissibility verdict); operationalizes the next safe
  step without approaching the data, the v002 terminal, or the sealed test.
  **Lowest risk; highest leverage; recommended.**
- **(B) Separate code-level source-admissibility gate artefact before any
  contract.** Considered against the preferred conservative direction. The
  repository evidence does **not** require it before a docs-only contract memo,
  because the contract memo reads no data and the only governance question it
  needs settled — "may the gated pre-v002 stack be named, by reference, as a
  contract source?" — is settled by this memo. A code-level admissibility gate
  conflates with the still-unimplemented Phase 4aw eligibility gate and is
  heavier than the next step needs; it would become relevant only at the
  data-read / eligibility-flip boundary, not at contract design. **Not selected.**
- **(C) ML dataset builder readiness memo.** Premature; a builder reads data and
  is blocked until a contract exists.
- **(D) Full-envelope reference-assembly memo.** Only relevant to a future
  pre-v002 + v002 combined path; **not required** for the conservative path; would
  expand scope toward the v002 terminal.
- **(E) Holdout-boundary memo.** Only required if a future scope touches the v002
  terminal or sealed-test dates; the conservative path touches neither;
  **not required**.
- **(F) Source-policy documentation memo / process-doc `D:` path-string update.**
  Valid minor housekeeping options, but they do not advance the ML arc.
- **(G) Remain paused / close the ML arc.** Valid operator options, but the arc
  has a clear, low-risk next step, so closing is not recommended.

---

## 22. Selected next recommendation

**Recommend a docs-only Phase 4bn-AC — ML Dataset Contract Memo** (working name;
subject to separate operator authorization):

- Specify, **by reference only**, the pre-v002 dataset contract: targets,
  features, filtering, split binding to the Phase 4bn-AA artefact, leakage /
  split-integrity obligations, and the Phase 4bn-L budget preflight the eventual
  builder must satisfy.
- **No data read; no dataset built; no eligibility flip; no
  `chronological_split_policy` set; no v002/sealed contact.**

This is the safest technical step that makes real progress without reading data,
because the source stack is admissible for contract **design** (this memo's
verdict) while data reads, dataset building, and training each remain later,
separately-authorized phases. A separate code-level source-admissibility gate is
**not** required before the contract memo; the repository evidence supports
proceeding to the docs-only contract.

---

## 23. Explicit non-authorizations

This phase authorizes **none** of: any merge phase for 4bn-AB; an ML dataset
contract memo; a source-admissibility gate artefact; an ML dataset builder
readiness memo; an ML dataset builder; a research matrix; a model; scores or
predictions; diagnostics; strategy / signals / PnL / backtests; a full-envelope
reference-assembly memo; a holdout-boundary memo; a source-policy documentation
memo; a process-doc `D:` path-string update; any eligibility flip or
`eligibility_gate_status` transition; any `chronological_split_policy` manifest
field; any storage migration / database / Parquet compaction / v003; any
acquisition / endpoint call / archive download / HEAD preflight; any raw /
normalization / feature / label execution or layer-gate re-run; any paper /
shadow / live / exchange-write / production-key / credentials / MCP / Graphify
work; any Phase 5; or any other successor. No successor is authorized from inside
Phase 4bn-AB.

---

## 24. Result state

`SOURCE_ADMISSIBILITY_RECORDED__PRE_V002_STACK_ADMISSIBLE_FOR_DATASET_CONTRACT_ONLY__REMAIN_PAUSED`

Meaning: the completed O/P/S/T/W/X/Y/Z/AA chain is sufficient to let the project
**design the ML dataset contract next** (a docs-only step that reads no data),
but **not** sufficient to read data, build a dataset, train ML, run diagnostics,
or mutate any manifest. Layer integrity = true;
`source_admissible_for_dataset_contract` = true;
`source_admissible_for_data_read` = false;
`source_admissible_for_dataset_builder` = false; `ml_authorized` = false;
`diagnostics_authorized` = false; `strategy_backtest_authorized` = false;
`manifest_research_eligible` = false (unchanged);
`manifest_eligibility_gate_status` = pending (unchanged);
`manifest_chronological_split_policy` = not set (unchanged); Phase 4aw invariant
preserved (never invoked).

---

## 25. Decision

`RECOMMEND_AUTHORIZE_ML_DATASET_CONTRACT_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`

Rationale: source admissibility is now resolved sufficiently for the next
docs-only step. The gated source stack + recorded split policy + code-level split
artefact + this admissibility verdict together let the project design the dataset
contract by reference, without reading data, flipping eligibility, or approaching
the v002 terminal / sealed test. The stricter alternative
(`RECOMMEND_AUTHORIZE_SOURCE_ADMISSIBILITY_GATE_ARTEFACT…`) is **not** selected
because the repository evidence shows no code-level gate is required before a
docs-only contract memo that reads no data.

---

## 26. Recommended state and successor options

**Recommended state: remain paused. No next phase authorized by this memo.**

Acceptable operator options after this branch's branch-complete report:

- remain paused;
- request a merge prompt for Phase 4bn-AB;
- separately authorize an **ML dataset contract memo** (the recommendation);
- separately authorize a **source-admissibility gate artefact** (if the operator
  prefers a code-level gate before any contract work — not required by the
  evidence);
- separately authorize an **ML dataset builder readiness memo**;
- separately authorize a **full-envelope reference-assembly memo** only if a
  future path combines pre-v002 + v002 data;
- separately authorize a **holdout-boundary memo** only if a future scope touches
  the v002 terminal or sealed-test dates;
- separately authorize a **source-policy documentation memo** or a **process-doc
  `D:` path-string update**;
- reject further ML-baseline successors and **close the ML arc**.

No ML / diagnostics / strategy / PnL / backtest / storage-migration / paper /
shadow / live / exchange-write option is valid from this state unless separately
authorized after this branch is merged.

---

## 27. Current-project-state update summary

`docs/00-meta/current-project-state.md` is amended **additively only**: one new
Phase 4bn-AB paragraph (recording phase type, tier, branch, base SHA, the
source-admissibility verdict, the admissibility-vocabulary values, the result
state / decision, and the full non-authorization posture) plus one new
`Current phase:` block at the top of the `Current phase:` history. All prior
Phase 4bn-A … 4bn-AA paragraphs and blocks, every retained verdict, and every
project lock are preserved verbatim. No other section is modified.
