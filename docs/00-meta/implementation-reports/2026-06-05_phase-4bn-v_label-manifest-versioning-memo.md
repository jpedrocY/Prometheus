# Phase 4bn-V — Label Manifest / Versioning Memo

## 1. Purpose

This memo is a **docs-only label-manifest / label-versioning /
label-lineage / non-eligible-source precondition / envelope-terminal
boundary-contract** deliverable. It resolves, from committed repository
documentation and committed tooling only, the **label manifest/versioning
ambiguity** and the **non-eligible-source precondition divergence** that
Phase 4bn-U identified as the single binding obstacle to authorizing a
future label-only execution phase over the Phase 4bn-S / 4bn-T local
gitignored pre-v002 BTCUSDT Binance USDⓈ-M futures aggTrades **feature**
segment (2024-03-01 .. 2024-11-30 inclusive UTC; 275 dates;
400,001,695 rows) and its Phase 4bn-O / 4bn-P normalized predecessor.

This phase **derives no labels**, **creates no label artefacts**, and
**creates or mutates no manifest or gate report**. It records, at design
level only, the exact manifest/versioning shape a future pre-v002
**label** segment must use; how that segment links to the Phase 4bn-S
feature segment manifest, the Phase 4bn-T feature-layer gate report, the
Phase 4bn-O normalized segment manifest, and the Phase 4bn-P
normalized-layer gate report; how it must replace the existing Stage-5
research-use successor-state precondition with a non-eligible-source
precondition; how `label_config_hash` must be defined for a non-eligible,
successor-state-free segment; how the label lineage columns must be
re-mapped from Phase 4bm lineage to Phase 4bn lineage; and how the
pre-v002 envelope terminal must be locked — all **without creating v003,
mutating any published `__v002` label manifest or directory, reading or
rewriting the v002 terminal label family, reading the v002 terminal
feature/normalized/raw window, touching the sealed test split, or
flipping research eligibility.**

This memo answers exactly the question Phase 4bn-U deferred:

> What exact manifest/versioning shape should a future pre-v002 label
> segment use; how should it link to the Phase 4bn-S feature segment,
> Phase 4bn-T feature-layer gate, Phase 4bn-O normalized segment, and
> Phase 4bn-P normalized-layer gate; how should it replace the old
> Stage-5 research-use successor-state dependency; how should
> `label_config_hash` be defined for a non-eligible
> successor-state-free segment; how should lineage columns be re-mapped;
> and how should the pre-v002 envelope terminal be represented without
> creating v003, mutating published `__v002` label artefacts, reading the
> v002 terminal window, touching sealed-test dates, or flipping research
> eligibility?

It does **not** ask whether the project can start ML, run the model, find
edge, backtest, trade, use the sealed test split, or make the dataset
research-eligible.

## 2. Authority and repository state

- **Active local repo path:** `D:\Prometheus`. **Active Claude Code
  lightweight workspace:** `D:\ClaudeRuns\prometheus-light`.
- **GitHub remote:** `origin` → `https://github.com/jpedrocY/Prometheus.git`
  (verified intact).
- **Branch:** `phase-4bn-v/label-manifest-versioning-memo`.
- **Base `main` SHA:** `4cf47348fd51061719e36102fab207b541cc6dcd`
  (`docs(phase-4bn-u): finalize merge closeout shas`). Pre-branch
  `main == origin/main == HEAD` was verified in sync. The Phase 4bn-U
  merge-closeout SHA-finalization commit `4cf4734`, merge-closeout
  `062b8f0`, merge `4f0bc5b`, and branch commit `ced0a79` are all present
  on `main`; the Phase 4bn-T SHA-finalization commit `28e1683` is present
  as predecessor.
- **Tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3. This phase
  settles the label manifest/versioning convention and the
  non-eligible-source precondition adjacent to future label artefact
  generation over the Phase 4bn-S / 4bn-T pre-v002 feature segment,
  future label-layer eligibility gates, future chronological
  split/holdout policy, future ML-baseline admissibility, and local
  disk/runtime budgets — while explicitly authorizing no label
  derivation, no ML, no diagnostics, no strategy, no research-eligibility
  flip, and no downstream use.
- **Working-tree expectation:** only the untracked transient
  `.claude/scheduled_tasks.lock`; the gitignored namespaces
  `data/microstructure/` (`.gitignore:85`) and `data/research/`
  (`.gitignore:88`) exist locally (Phase 4bn-O / 4bn-S derived outputs +
  Phase 4bn-P / 4bn-T gate reports) and remain uncommitted.

## 3. Phase type and strict scope

**Phase type:** docs-only / label-manifest / label-versioning /
label-lineage / non-eligible-source precondition / envelope-terminal
boundary-contract.

**Allowed work performed by this phase:**

- read committed Markdown docs;
- inspect committed source, scripts, and tests read-only;
- identify the existing label manifest construction and validation
  conventions and the existing `__v002` label-family manifest / directory
  convention from committed code/docs only;
- define the future pre-v002 label segment manifest naming convention and
  the future label output directory naming convention;
- define the non-eligible-source precondition that replaces the Stage-5
  research-use successor-state precondition for this pre-v002 segment;
- define how `label_config_hash` must be computed/versioned for the
  pre-v002 non-eligible segment;
- define how the label lineage columns must be re-mapped from Phase 4bm
  lineage to Phase 4bn lineage;
- define how `envelope_terminal_unix_ms` must be locked to the pre-v002
  segment terminal;
- define predecessor linkage to the Phase 4bn-S feature segment manifest,
  the Phase 4bn-T feature-layer gate report, the Phase 4bn-O normalized
  segment manifest, the Phase 4bn-P normalized-layer gate report, the
  Phase 4bn-R feature manifest/versioning convention, the published label
  `__v002` family by reference, and the dataset-versioning rules;
- define how the eventual 12-month label envelope is represented by
  reference;
- define what future label execution must write and must not mutate;
- define required offline tests for the future bounded label wrapper and
  label manifest writer;
- define future label-layer gate implications;
- create the two tracked Phase 4bn-V docs and update
  `current-project-state.md` narrowly.

**This phase did NOT and must NOT (within Phase 4bn-V):** derive labels;
create label artefacts; create or mutate any label manifest; run label
gates; read any local raw zip, normalized Parquet, feature Parquet, label
file, gate report, manifest, sidecar, or `data/research` artefact; create
`data/microstructure` or `data/research` outputs; run ML, diagnostics,
strategy, signals, PnL, or backtests; acquire data; call any endpoint;
touch the v002 terminal raw/normalized/feature window; touch the sealed
test split; create a database; compact Parquet; create v003; or authorize
any successor.

## 4. Evidence base and input boundary

**Inputs read (committed repository evidence only):**

- `docs/00-meta/current-project-state.md` (the Phase 4bn-U / 4bn-T /
  4bn-S / 4bn-R / 4bn-P / 4bn-O / 4bn-L paragraphs and `Current phase:`
  blocks);
- the process standards `merge-closeout-standard.md`,
  `phase-risk-tiering-standard.md`, `phase-workflow-standard.md`,
  `phase-prompt-template.md`, `operator-report-standard.md`;
- the Phase 4bn-U label-derivation readiness/execution-plan memo,
  merge-closeout, and closeout; the Phase 4bn-T feature-layer gate
  report, merge-closeout, and closeout; the Phase 4bn-S feature-only
  pre-v002 segment report, merge-closeout, and closeout; the Phase 4bn-R
  feature manifest/versioning memo, merge-closeout, and closeout; the
  Phase 4bn-P normalized-layer gate report, merge-closeout, and closeout;
  the Phase 4bn-O normalization-only segment report, merge-closeout, and
  closeout; the Phase 4bn-L derived-stack storage-budget memo,
  merge-closeout, and closeout;
- the data specs `data-requirements.md`, `historical-data-spec.md`,
  `timestamp-policy.md`, `dataset-versioning.md`, and
  `database-design.md`;
- committed label/manifest/gate tooling read-only:
  `src/prometheus/research/microstructure/labels_schema_v002.py`,
  `labels_manifest_v002.py`, `labels_io_v002.py`, `labels_compute_v002.py`,
  `labels_io.py`, `labels_validation.py`, `label_gate.py`,
  `label_gate_v001.py`, `multiday_label_gate.py`,
  `multiday_label_gate_v002.py`;
  `scripts/phase4bm_o_compute_multiday_labels.py`,
  `scripts/phase4bm_q_run_multiday_label_gate.py`,
  `scripts/phase4bn_s_compute_pre_v002_features.py`,
  `scripts/phase4bn_t_validate_feature_pre_v002_gate.py`; and the
  committed offline test surface under `tests/research/microstructure/`.

**Inputs explicitly NOT used:** any local raw zip, normalized Parquet,
feature Parquet, label file, gate report, manifest, sidecar,
successor-state, or `data/research` artefact; the v002 terminal raw /
normalized / feature window; the sealed v002 test split; no hashing,
counting, or inspection of local gitignored data; no endpoints; no
credentials; no `.env`; no `.mcp.json`; no MCP; no Graphify. **README was
treated as potentially stale and was not used as current-state
authority.** SHA256 digests cited for local gitignored artefacts (the
Phase 4bn-S feature segment manifest + sidecar, the Phase 4bn-T feature
gate report, the Phase 4bn-O normalized segment manifest + sidecar, the
Phase 4bn-P normalized gate report, the pre-v002 raw segment manifest) are
quoted **from committed Markdown evidence** (prior closeouts /
current-project-state), not by reading the local files.

## 5. Phase 4bn-U finding carried forward

Phase 4bn-U (branch `phase-4bn-u/…`, merged at `main` SHA `4cf4734`)
concluded:

1. **Label primitives are reusable; the orchestrator and gate are not.**
   The committed label stack — `labels_schema_v002.py` (40-column
   `LABEL_SCHEMA_V002`), the label kernel
   `compute_aggtrade_labels_v002_for_day`, `labels_validation.py`, the
   gate-check modules — is reusable, but
   `scripts/phase4bm_o_compute_multiday_labels.py` and the
   `multiday_label_gate` input contract are hardcoded to the published
   v002 family (15 locked precondition SHAs, the Phase 4bm-L Stage-5
   successor-state, `EXPECTED_FEATURE_CONFIG_HASH=819cfa7a…`, the v002
   date constants 2024-12-01 .. 2025-02-28 / 90 dates / 155,153,449 rows,
   the single `__v002` manifest basename and output directory). A future
   label phase must add a bounded `phase4bn_*` wrapper + segment-scoped
   gate + segment-scoped path/manifest helpers + new offline tests,
   exactly as Phase 4bn-O / 4bn-S did.
2. **Label manifest/versioning requires this docs-only memo.** The v002
   `label_config_hash` and lineage model bind a Stage-5 feature
   successor-state and Phase 4bm-J/L/F/D lineage that the non-eligible,
   successor-state-free pre-v002 segment does not (and must not) have; the
   envelope terminal must be re-locked to the pre-v002 terminal; segment
   naming must be settled. Phase 4bn-R settled the *feature* manifest,
   not the *label* manifest.
3. **The sealed-test / v002-terminal boundary is clear and safe** for the
   conservative pre-v002-only label scope; a holdout-boundary memo is
   **not** required when `envelope_terminal_unix_ms` is locked to the
   pre-v002 segment terminal (2024-11-30) so forward ≤60 s horizons censor
   at the boundary and never read 2024-12-01+ or 2025-02-14..28 dates.
4. **Label-only execution is feasible in principle but premature** until
   the manifest/versioning shape is settled.

Phase 4bn-U's decision was
`RECOMMEND_AUTHORIZE_DOCS_ONLY_LABEL_MANIFEST_VERSIONING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
This phase executes exactly that recommended memo. **Finding (2) is the
sole ambiguity this memo resolves; findings (1), (3), and (4) are carried
forward unchanged.**

## 6. Dataset-versioning rules carried forward

`docs/04-data/dataset-versioning.md` binds the following for versioned
(including label) datasets:

- **Version identity** is required; the recommended identifier pattern is
  `<dataset_name>__vNNN`, **monotonic per family**, **never reused or
  overwritten**.
- **Every versioned dataset has a manifest** at the dataset-version root,
  with minimum fields including dataset name, version ID, category,
  creation timestamp, canonical timezone/format, symbol set, schema
  version, transformation/pipeline version, partitioning rules, primary
  key, generator identity, notes, and **predecessor version if
  applicable**.
- **Published versions are immutable**: files, schema, and manifest must
  not be silently modified; corrections create a **new version** that
  records its **predecessor**.
- **Publication states** are `draft` / `published` / `deprecated` /
  `superseded`; only `published` versions are used for formal research.
- **Partition folders do not replace version identity** — directory
  layout is a storage concern; version identity is a governance concern.

The doc does **not** codify "segment manifests," predecessor-linked
backward extensions, or how a backward label segment relates to an
already-published terminal label version. The raw layer (Phase
4bn-J-R2 / 4bn-K), the normalized layer (Phase 4bn-N / 4bn-O), and the
feature layer (Phase 4bn-R / 4bn-S) each resolved that gap by precedent;
this memo resolves it for the **label layer** by the same precedent (see
§13–§22).

## 7. Existing label `__v002` conventions

From committed code (`labels_schema_v002.py`, `labels_manifest_v002.py`,
`labels_io_v002.py`, `scripts/phase4bm_o_compute_multiday_labels.py`, the
`multiday_label_gate*` modules):

- **Label family (schema-lineage marker):**
  `microstructure_labels_aggtrades_v001` (`LABEL_DATASET_FAMILY_V002`).
  The trailing `v001` is part of the **family name** — the locked Phase
  4bm-N forward-return/direction label column set — **not** a window
  discriminator.
- **Dataset version (window/source discriminator):** the second suffix.
  `__v002` (`LABEL_DATASET_VERSION_V002 = "v002"`) = the 90-day Phase
  4bm-O multi-day label output over the v002 terminal window
  **2024-12-01 .. 2025-02-28** (`LABEL_UTC_DATE_START_V002` /
  `LABEL_UTC_DATE_END_V002`; `LABEL_DATE_COUNT_V002 = 90`;
  `LABEL_EXPECTED_ROW_COUNT_V002 = 155_153_449`).
- **Label schema version:** `LABEL_SCHEMA_VERSION_V002 = "v001"` (the
  label column set is unchanged from v001; only the lineage block
  differs). `LABEL_SCHEMA_V002` has **40 columns** in canonical order:
  **17 lineage** (`LABEL_LINEAGE_COLUMNS_V002`) + **1**
  `label_config_hash` + **8 label** (4 `forward_log_return_{1s,5s,15s,60s}`
  regression + 4 `forward_direction_{1s,5s,15s,60s}` ∈ {−1, 0, +1}
  classification) + **14 support** (per-horizon `reference_row_index_*`,
  `reference_timestamp_ms_*`, `horizon_censored_flag_*`, plus
  `label_invalid_price_flag`, `label_any_censored_flag`). Horizons
  `LABEL_HORIZONS_V002 = ("1s","5s","15s","60s")` paired with
  `LABEL_HORIZON_MS_V002 = (1000, 5000, 15000, 60000)`. A 21-token
  forbidden-substring guard
  (`FORBIDDEN_LABEL_COLUMN_SUBSTRINGS_V002`:
  `pnl, profit, loss, mfe, mae, r_multiple, equity, position, alpha,
  edge, prediction, model, score, decision, strategy, entry, exit,
  signal, target, barrier, liquidation`) rejects any output column name
  implying barrier/MFE/MAE/R-multiple/strategy/signal/PnL/model/score
  semantics (`assert_no_forbidden_label_substrings_v002`). The labels are
  thus a **pure causal forward-return/direction research artefact**, not a
  strategy/signal/PnL artefact.
- **The 17 lineage columns** (`LABEL_LINEAGE_COLUMNS_V002`, canonical
  order): `dataset_family`, `dataset_version`, `label_schema_version`,
  `source_feature_dataset_family`, `source_feature_dataset_version`,
  `source_feature_manifest_sha256`, `source_feature_parquet_sha256`,
  `source_feature_successor_state_sha256`,
  `source_phase_4bm_j_gate_report_sha256`,
  `source_normalized_manifest_sha256`, `source_raw_manifest_sha256`,
  `symbol`, `utc_date`, `row_index`, `agg_trade_id`,
  `feature_timestamp_ms`, `source_transact_time_ms`. **Two of these —
  `source_feature_successor_state_sha256` (the Phase 4bm-L Stage-5
  research-use successor-state) and `source_phase_4bm_j_gate_report_sha256`
  (the Phase 4bm-J feature gate) — are v002-terminal-specific artefacts
  that the non-eligible pre-v002 segment does not have.**
- **Label partition directory (`labels_io_v002.py`):**
  `V002_LABEL_DIR_SEGMENT = f"{LABEL_DATASET_FAMILY}__{LABEL_DATASET_VERSION_V002}"`,
  i.e.
  `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-labels-aggtrades-<YYYY-MM-DD>.parquet`,
  each with a paired canonical two-space `.sha256` sidecar
  (`compose_canonical_sidecar_v002_label`), refuse-to-overwrite, atomic
  write-then-rename. The label **directory is version-suffixed** — exactly
  the same asymmetry the normalized and feature layers have — so a
  backward label segment cannot be written into the published `__v002/`
  directory without blurring the published, immutable family.
- **Label index manifest:**
  `V002_LABEL_MANIFEST_BASENAME = microstructure_labels_aggtrades_v001__v002.json`,
  i.e.
  `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json`,
  paired with a canonical sidecar.
- **Manifest builder (`build_label_manifest_v002`):** seeds
  `research_eligible: False`, `eligibility_gate_status: "pending"`,
  governance labels (`ml`/`strategy`/`backtest`/`acquisition`/
  `paper_shadow_live`/`deployment`/`exchange_write` forbidden/unauthorized
  via `FORBIDDEN_LABEL_GOVERNANCE_VALUES_V002`; `labels`/`targets` =
  `allowed_by_future_phase_only`), a 17-key
  `REQUIRED_LABEL_BOUNDARY_CONFIRMATIONS_V002` set (all `True`, including
  `no_label_gate_report`, `no_label_successor_state`,
  `no_successor_authorization`,
  `phase_4aw_flip_research_eligible_invariant_preserved`), explicit
  `*_authorized: False` flags (`diagnostics_authorized`, `ml_authorized`,
  `strategy_authorized`, `backtest_authorized`, `acquisition_authorized`,
  `successor_authorization_after`, `stage_5_label_cleared`),
  `chronological_split_policy: "not_yet_defined"`, the
  `envelope_terminal_unix_ms`, and pins source lineage SHAs
  (`source_feature_manifest_sha256`, `source_feature_successor_state_sha256`,
  `source_phase_4bm_j_gate_report_sha256`,
  `source_normalized_manifest_sha256`,
  `source_phase_4bm_f_derived_successor_state_sha256`,
  `source_phase_4bm_d_derived_gate_report_sha256`,
  `source_raw_manifest_sha256`, `source_acquisition_log_sha256`,
  `source_phase_4bl_e_raw_successor_state_sha256`,
  `source_phase_4bl_d_r_raw_gate_report_sha256`) plus a `per_day_outputs`
  inventory (each entry: `utc_date`, `path`, `sha256`, `sidecar_path`,
  `sidecar_sha256`, `byte_size`, `row_count`,
  `per_horizon_censored_counts`, `invalid_price_row_count`,
  `source_feature_parquet_sha256`).
- **`label_config_hash` builder (`build_label_config_hash_v002`):** a
  SHA256 over canonical-JSON (sorted keys, ASCII, no whitespace) of the
  label policy fields (`ANCHOR_POLICY_V002`,
  `FUTURE_REFERENCE_POLICY_V002`, `DIRECTION_THRESHOLD_POLICY_V002`,
  `NULL_CENSORING_POLICY_V002`, `DTYPE_POLICY_V002`; the schema/horizon/
  lineage lists) **plus five required hex64 lineage inputs**
  (`source_feature_manifest_sha256`,
  `source_feature_successor_state_sha256`,
  `source_phase_4bm_j_gate_report_sha256`,
  `source_normalized_manifest_sha256`, `source_raw_manifest_sha256`) and
  `feature_config_hash`. Every one of those six inputs is validated by
  `_require_hex64` (must be 64-char lowercase hex).

**Key asymmetries (drive §8–§17).** (i) Like the normalized and feature
layers, label directories are version-suffixed, so a pre-v002 backward
label segment must NOT be written into the published `__v002/` label
directory. (ii) The orchestrator and gate are window-hardcoded to the
90-day v002 terminal window and hard-assert
`EXPECTED_FEATURE_CONFIG_HASH = 819cfa7a…`. (iii) The
`build_label_config_hash_v002` builder hard-requires a 64-hex
`source_feature_successor_state_sha256` — the Phase 4bm-L Stage-5
research-use successor-state — the precondition the non-eligible pre-v002
segment cannot (and must not) satisfy. (iv) **The hashed policy string
`FUTURE_REFERENCE_POLICY_V002` literally embeds
`envelope_terminal_unix_ms=max_source_transact_time_ms_across_v002_90day_envelope`**
— a clause that is factually false for the pre-v002 segment terminal. The
locked **primitives** (schema, kernel, validation, sidecar, gate-check
helpers) are reusable; the **orchestrator, gate, successor-state
precondition, and config-hash policy string** are not.

## 8. Label manifest/versioning ambiguity being resolved

The pre-v002 **raw** segment (Phase 4bn-J-R2 / 4bn-K), the pre-v002
**normalized** segment (Phase 4bn-O / 4bn-P), and the pre-v002 **feature**
segment (Phase 4bn-R / 4bn-S / 4bn-T) were each represented as a
**phase-scoped segment manifest** rather than a new `__vNNN`:

- **Raw:**
  `microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2.json`
  (SHA256 `1659e6da…3a3d1`).
- **Normalized:**
  `microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json`
  (SHA256 `0e96ae37…d9fa`), validated by the Phase 4bn-P gate report
  (SHA256 `3452fd9d…f134`).
- **Feature:**
  `microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s.json`
  (SHA256 `4881eb87…b52`), validated by the Phase 4bn-T gate report
  (SHA256 `db731d1b…6ab08`).

Each keeps `dataset_version: "v002"`, adds `segment_label:
"pre_v002_segment"`, records `full_intended_envelope_*` and by-reference
v002-terminal / sealed-split blocks, and forbids v003.

**The label-layer ambiguity** has four parts, all specific to the label
layer and not settled by any committed memo (Phase 4bn-R settled the
*feature* manifest only):

1. **Segment manifest/versioning shape** — whether the pre-v002 label
   output should be (a) a phase-scoped segment manifest mirroring the
   raw/normalized/feature precedent, (b) a predecessor-linked extension of
   `__v002`, (c) a new full-envelope label version, or (d) directory-only
   with no manifest.
2. **Non-eligible-source precondition** — what a label wrapper must require
   **instead** of the Phase 4bm-L Stage-5 research-use successor-state.
3. **`label_config_hash` divergence** — both the successor-state input
   slot AND the hashed `FUTURE_REFERENCE_POLICY_V002` envelope clause must
   change for the segment.
4. **Lineage column re-mapping** — two of the 17 lineage columns reference
   v002-terminal-specific artefacts that the segment lacks.

This memo selects the shape (§13–§14) and resolves §9–§12.

## 9. Non-eligible-source precondition being resolved

The committed v002 label orchestrator
(`scripts/phase4bm_o_compute_multiday_labels.py`) hard-binds 15 locked
`(path, SHA256)` precondition pairs to the **published** v002 family,
including the **Phase 4bm-L Stage-5 research-use successor-state**
(`phase_4bm_l_successor_state`) and a hard assertion
`EXPECTED_FEATURE_CONFIG_HASH == 819cfa7a…`; and
`build_label_config_hash_v002` feeds the Stage-5 successor-state SHA into
`source_feature_successor_state_sha256`. That Stage-5 successor-state is the
Phase 4bm-L artefact: it exists only because the v002 terminal feature
family went through a Stage-5 research-use flip. **The pre-v002 segment has
no such artefact and must not acquire one** — Phase 4bn-S/4bn-T recorded
`research_eligible: false`, `eligibility_gate_status: "pending"`, and
`no_successor_authorization: true`, and the Phase 4aw
`flip_research_eligible(...)` always-raises invariant must never be
invoked. Therefore the future label wrapper **cannot** reuse the Stage-5
successor-state precondition; it needs a **non-eligible-source
precondition** built on the Phase 4bn-T feature-layer gate PASS (and the
Phase 4bn-P normalized-layer gate PASS) instead. §15 defines that
precondition.

## 10. Label config hash ambiguity being resolved

`build_label_config_hash_v002` cannot be reused verbatim for the pre-v002
segment for **two independent reasons**, both grounded in committed code:

1. **Successor-state input slot.** The builder requires a 64-hex
   `source_feature_successor_state_sha256` (validated by `_require_hex64`).
   The segment has **no** Stage-5 successor-state. Feeding the published
   Stage-5 SHA would be a lie (wrong source family); feeding a fabricated
   sentinel hex is both ugly and risks being misread as a real artefact.
2. **Hashed envelope policy string.** The hashed `FUTURE_REFERENCE_POLICY_V002`
   literally contains
   `envelope_terminal_unix_ms=max_source_transact_time_ms_across_v002_90day_envelope`.
   For the pre-v002 segment the envelope terminal is the **pre-v002
   segment terminal** (max within 2024-11-30), **not** the v002 90-day
   envelope. Reusing the string verbatim would bake a factually false
   policy clause into the segment's `label_config_hash`.

Additionally, the orchestrator's `feature_config_hash` input is hard-set to
`EXPECTED_FEATURE_CONFIG_HASH = 819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d`,
**which is the published v002 feature family's config hash and is NOT
valid for the pre-v002 segment**, whose `feature_config_hash` is
`0726b41d48e5f7127728c385b150d90fad91a92b3400c0545649b541e4dd114c`
(recorded by Phase 4bn-S). §16 defines the segment-scoped builder.

## 11. Label lineage mapping being resolved

`LABEL_SCHEMA_V002` is a **40-column** locked schema with
`label_schema_version = "v001"`. The 17 lineage columns include two that
reference v002-terminal-specific artefacts absent for the segment:

- `source_feature_successor_state_sha256` (Phase 4bm-L Stage-5
  research-use successor-state) — **no segment analog exists**, by design;
- `source_phase_4bm_j_gate_report_sha256` (Phase 4bm-J feature gate) — the
  segment's feature-gate analog is the **Phase 4bn-T feature-layer gate**.

The question is whether retaining the exact 40-column `LABEL_SCHEMA_V002`
(no new `label_schema_version`, no v003) is compatible with honest lineage
for a segment whose lineage is Phase 4bn-T / 4bn-S / 4bn-P / 4bn-O / 4bn-J-R2.
§17 resolves this by **re-mapping (reinterpreting) the per-row values of
those two columns to the Phase 4bn equivalents, keeping the column names
and the 40-column schema verbatim, and recording the authoritative
re-mapping in the segment manifest** — preserving the output schema while
changing only the lineage *values* and the manifest lineage *fields*.

## 12. Envelope terminal policy being resolved

The v002 `envelope_terminal_unix_ms` is the 2025-02-28 v002 terminal
(computed by `_compute_envelope_terminal_unix_ms` over the 90-day v002
envelope). The segment must lock a **pre-v002 terminal** (2024-11-30),
which changes the per-horizon censoring footprint materially and is part
of the hash-locked policy (see §10). §18 defines the pre-v002 envelope
terminal convention.

## 13. Candidate shapes considered

1. **Phase-scoped label segment manifest (raw/normalized/feature-precedent
   mirror).** A sibling-shape JSON
   `microstructure_labels_aggtrades_v001__v002_pre_v002_segment_<label-phase-id>.json`
   with `dataset_version: "v002"`, `label_schema_version: "v001"`,
   `segment_label: "pre_v002_segment"`, its own version-suffixed segment
   directory, full-envelope-by-reference fields, by-reference
   v002-terminal / sealed-split blocks, a non-eligible-source lineage
   block (Phase 4bn-S feature segment manifest + Phase 4bn-T feature-layer
   gate report + Phase 4bn-O / 4bn-P normalized witnesses) replacing the
   Stage-5 successor-state, and a segment-scoped `label_config_hash`.
   **Pros:** exact structural and governance parity with the already-merged
   raw, normalized, and feature segment precedents; reuses the locked label
   primitives unchanged; leaves the published `__v002` label family
   byte-for-byte immutable; no v003; no v002 terminal read. **Cons:**
   longer directory/manifest name than `__vNNN`; requires a segment-scoped
   config-hash builder + tests (§16). **Selected (see §14).**

2. **Predecessor-linked extension of `__v002` (write into the v002 label
   family).** Write pre-v002 label dates under the existing
   `microstructure_labels_aggtrades_v001__v002/` directory and link via a
   `predecessor`/`extends` field. **Cons:** writes new files into the
   **published, immutable** `__v002` label directory, creating parquets the
   published `__v002.json` label manifest does not reference (the manifest
   is refuse-overwrite-protected) — orphaned-within-the-family artefacts;
   blurs the "published-version-is-immutable" boundary; **rejected.**

3. **New full-envelope label version (`__v003` or a single rewritten label
   envelope).** **Cons:** directly collides with the forbidden v003
   boundary and the monotonic-immutability rule; would require reading the
   v002 terminal feature/normalized window (including sealed-test dates) to
   recompute a single 12-month label family; **rejected outright.**

4. **No manifest (rely on the directory only).** **Cons:** violates
   `dataset-versioning.md` ("never run formal validation on an untracked
   dataset version"; "partition folders do not replace version identity");
   a future label-layer gate would have no field-contract to validate;
   **rejected.**

## 14. Selected label segment convention

**Selected: Candidate (1) — a phase-scoped label segment manifest,
mirroring the merged raw-, normalized-, and feature-layer precedents.**

The future pre-v002 label output is represented as a **phase-scoped label
segment manifest** — a sibling-shape JSON **clearly tied to the existing
v002 label family but clearly marked as a pre-v002 backward segment /
extension**, not a new monotonic version.

- **Manifest filename (under `data/microstructure/manifests/`):**

  ```text
  microstructure_labels_aggtrades_v001__v002_pre_v002_segment_<label-phase-id>.json
  ```

  with a paired canonical two-space `.sha256` sidecar.
  `<label-phase-id>` is the underscored phase id of the future
  separately-authorized label-execution phase (e.g. if that phase is
  `4bn-W`, the token is `4bn_w`, yielding
  `microstructure_labels_aggtrades_v001__v002_pre_v002_segment_4bn_w.json`).
  This exactly parallels the feature segment's
  `microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s.json`,
  the normalized segment's `…normalized…__v002_pre_v002_segment_4bn_o.json`,
  and the raw segment's `…raw…__v002_pre_v002_segment_4bn_j_r2.json`.

- **Inner identity fields:** `dataset_family =
  "microstructure_labels_aggtrades_v001"` (reused, schema-identical);
  `dataset_version = "v002"` and `version = "v002"` (a **backward segment
  of the v002 envelope**, not a new version); `label_schema_version =
  "v001"`; `segment_label = "pre_v002_segment"`. The window discriminator
  lives in the **filename and directory name**, never as a new
  `dataset_version` and never as a new `label_schema_version`.

This selection: (i) reuses the locked label primitives unchanged;
(ii) leaves the published label `__v002` family — directory, parquets,
sidecars, and `microstructure_labels_aggtrades_v001__v002.json` manifest —
**byte-for-byte immutable**; (iii) creates **no** v003; (iv) reads **no**
v002 terminal feature/normalized window and **no** sealed-test dates;
(v) keeps every output non-eligible and pending.

**Answer to Q1:** a **phase-scoped label segment manifest** (not a
predecessor-linked extension, not a full-envelope version, not another
shape).

## 15. Selected non-eligible-source precondition

The future label wrapper must replace the Stage-5 research-use
successor-state precondition with the following **non-eligible-source
precondition**:

- **Source feature segment = the Phase 4bn-S feature segment manifest**,
  verified by SHA256 (`4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52`,
  + sidecar `f2ca2f48…92e5`) at
  `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s.json`;
  **not** the published `__v002` feature manifest. Each per-day source
  feature Parquet must verify by SHA256 against that segment manifest's
  `per_file_inventory`. The four anchor columns (`row_index`,
  `agg_trade_id`, `feature_timestamp_ms`, `source_transact_time_ms`) are
  read from each feature Parquet.
- **Feature-layer admissibility predecessor = the Phase 4bn-T
  feature-layer gate report**, not a Stage-5 successor-state. The wrapper
  must verify the Phase 4bn-T gate report exists, parses, carries the PASS
  verdict
  `FEATURE_LAYER_GATE_PASSED__LOCAL_FEATURE_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`,
  and matches its recorded SHA256
  (`db731d1be06295404ef195d9b5b5bad8010ce6ae6efef43ece90c29653d6ab08`).
- **Normalized witnesses = the Phase 4bn-O normalized segment manifest +
  Phase 4bn-P normalized-layer gate report.** The normalized per-day
  Parquet (for anchor/reference `trade_price`) come from the Phase 4bn-O
  segment (manifest SHA256
  `0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa`, +
  sidecar `5d7dcbef…6402`), admitted by the Phase 4bn-P gate report
  (SHA256 `3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134`,
  verdict
  `NORMALIZED_LAYER_GATE_PASSED__LOCAL_NORMALIZED_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`);
  **not** the published `__v002` normalized manifest.
- **The source feature and normalized segments must remain non-eligible.**
  The wrapper must read `research_eligible: false` and
  `eligibility_gate_status: "pending"` from both segment manifests and must
  fail closed if either is otherwise. **No `research_eligible: true`, no
  Stage-5 successor-state, and no `EXPECTED_FEATURE_CONFIG_HASH=819cfa7a…`
  is required for this pre-v002 expansion path; none may be created or
  asserted. The segment `feature_config_hash` is `0726b41d…`.**
- **Generated label outputs must remain non-eligible and pending.** The
  label segment manifest must carry `research_eligible: false`,
  `eligibility_gate_status: "pending"`, `successor_authorization_after:
  false`, `no_successor_authorization: true`, and the Phase 4aw
  `flip_research_eligible(...)` always-raises invariant must never be
  invoked.
- **Generated labels cannot be used** for ML, diagnostics, strategy,
  research, split policy, or backtests until later, separately authorized
  gates/policies. The governance labels must mark
  `ml`/`strategy`/`backtest`/`acquisition`/`paper_shadow_live`/
  `deployment`/`exchange_write` forbidden/unauthorized
  (`FORBIDDEN_LABEL_GOVERNANCE_VALUES_V002`), with `labels`/`targets`
  `allowed_by_future_phase_only`.

In short: the label wrapper's lineage block replaces the v002 manifest's
Phase 4bm-L/F/D and Phase 4bl-E/D-R lineage fields with a
`source_feature_segment_manifest_*` block (Phase 4bn-S), a
`source_feature_layer_gate_report_*` block (Phase 4bn-T), a
`source_normalized_segment_manifest_*` block (Phase 4bn-O), and a
`source_normalized_layer_gate_report_*` block (Phase 4bn-P), and adds an
explicit `source_eligibility_posture: "non_eligible_gate_passed_pending"`
witness. This is the label-layer analogue of how Phase 4bn-S sourced from
the Phase 4bn-O normalized segment manifest + Phase 4bn-P gate report
rather than the published `__v002` normalized manifest + Stage-3
successor-state.

## 16. Selected label_config_hash convention

**Selected: a NEW segment-scoped config-hash builder** (combining the
prompt's options 5(b) and 5(c)) — call it
`build_label_config_hash_v002_pre_v002_segment` — to be added by the
future label-execution phase, with offline tests, **before any label
execution**. The reuse-`build_label_config_hash_v002`-verbatim option
(5a) is **rejected** because the hashed `FUTURE_REFERENCE_POLICY_V002`
string is factually wrong for the segment (§10), so no SHA substitution
alone suffices.

The new builder must:

- **Preserve verbatim** `ANCHOR_POLICY_V002`,
  `DIRECTION_THRESHOLD_POLICY_V002`, `DTYPE_POLICY_V002`,
  `NULL_CENSORING_POLICY_V002`, and the schema / horizon / lineage column
  lists (so the label semantics are provably identical to v002 except for
  the envelope terminal and the source lineage).
- **Replace the future-reference-policy envelope clause** with a
  pre-v002-segment-terminal variant — a policy string identical to
  `FUTURE_REFERENCE_POLICY_V002` except that
  `envelope_terminal_unix_ms=max_source_transact_time_ms_across_v002_90day_envelope`
  becomes
  `envelope_terminal_unix_ms=max_source_transact_time_ms_across_pre_v002_segment_2024-03-01_to_2024-11-30`
  (segment terminal, never the 90-day v002 envelope).
- **Replace the successor-state hash input** with explicitly named
  non-eligible-source fields:
  `source_feature_layer_gate_report_sha256` = Phase 4bn-T gate report SHA
  (`db731d1b…`) and `source_normalized_layer_gate_report_sha256` = Phase
  4bn-P gate report SHA (`3452fd9d…`), in place of the v002
  `source_feature_successor_state_sha256` /
  `source_phase_4bm_j_gate_report_sha256` inputs.
- **Bind** `source_feature_manifest_sha256` = Phase 4bn-S segment manifest
  SHA (`4881eb87…`), `source_normalized_manifest_sha256` = Phase 4bn-O
  segment manifest SHA (`0e96ae37…`), `source_raw_manifest_sha256` =
  pre-v002 raw segment manifest SHA (`1659e6da…`), and
  `feature_config_hash` = `0726b41d…` (**never** `819cfa7a…`).
- **Add a `segment_label: "pre_v002_segment"` discriminator** to the
  hashed payload so the segment's `label_config_hash` is provably distinct
  from the published v002 family's.

The resulting `label_config_hash` is written into the per-row
`label_config_hash` column (column 17 of `LABEL_SCHEMA_V002`) and recorded
in the segment manifest. **This memo specifies the builder's contract
exactly; it neither writes the code nor runs it.** The published v002
feature config hash `819cfa7a…` is explicitly **not valid** for the
pre-v002 segment.

**Answer to Q5:** define a **new segment-scoped config-hash builder**
preserving the label policy fields while replacing the successor-state
lineage with Phase 4bn-T / 4bn-S / 4bn-P / 4bn-O lineage and re-specifying
the envelope-terminal clause; this **requires a future code-level change +
tests before execution**.

## 17. Selected lineage convention

**Selected: keep `LABEL_SCHEMA_V002` exactly (40 columns,
`label_schema_version = "v001"`, column names verbatim) and re-map the
per-row values of the two terminal-specific lineage columns to their
Phase 4bn equivalents, recording the authoritative re-mapping in the
segment manifest.** No new label schema version, no v003. This is the
prompt's preferred approach ("keep output schema exactly `LABEL_SCHEMA_V002`
while changing only manifest lineage fields and `label_config_hash`
semantics"), and it is the only approach that avoids bumping
`label_schema_version` (which would otherwise violate the
no-new-version preference).

Per-row lineage column values for the segment (17 columns):

| Lineage column | Segment value |
|---|---|
| `dataset_family` | `microstructure_labels_aggtrades_v001` (unchanged) |
| `dataset_version` | `v002` (unchanged) |
| `label_schema_version` | `v001` (unchanged) |
| `source_feature_dataset_family` | `microstructure_features_aggtrades_v001` (unchanged) |
| `source_feature_dataset_version` | `v002` (unchanged) |
| `source_feature_manifest_sha256` | Phase 4bn-S feature **segment** manifest SHA (`4881eb87…`) — re-mapped from published `__v002` to segment |
| `source_feature_parquet_sha256` | the per-day Phase 4bn-S feature Parquet SHA (unchanged semantics) |
| `source_feature_successor_state_sha256` | **re-mapped:** Phase 4bn-P **normalized-layer gate report** SHA (`3452fd9d…`) — the non-eligible admissibility witness that *replaces* the absent Stage-5 successor-state |
| `source_phase_4bm_j_gate_report_sha256` | **re-mapped:** Phase 4bn-T **feature-layer gate report** SHA (`db731d1b…`) — the segment's feature-gate analog |
| `source_normalized_manifest_sha256` | Phase 4bn-O normalized **segment** manifest SHA (`0e96ae37…`) — re-mapped from published `__v002` to segment |
| `source_raw_manifest_sha256` | pre-v002 raw **segment** manifest SHA (`1659e6da…`) — re-mapped from published `__v002` to segment |
| `symbol` | `BTCUSDT` (per-row) |
| `utc_date` | per-row source date |
| `row_index` | per-row feature anchor row index |
| `agg_trade_id` | per-row feature anchor aggTrade id |
| `feature_timestamp_ms` | per-row feature anchor timestamp |
| `source_transact_time_ms` | per-row feature anchor source transact time |

The two **re-mapped** columns keep their canonical names (so the 40-column
schema and `label_schema_version "v001"` are unchanged) but, for this
segment only, carry the Phase 4bn admissibility witnesses. The
authoritative re-mapping is recorded in the segment manifest under an
explicit `lineage_column_reinterpretation` block:

```text
lineage_column_reinterpretation:
  source_feature_successor_state_sha256:
    segment_meaning: "non_eligible_admissibility_witness"
    bound_artefact: "phase_4bn_p_normalized_layer_gate_report"
    value: 3452fd9d...f134
    note: "no Stage-5 research-use successor-state exists or is required for this non-eligible segment"
  source_phase_4bm_j_gate_report_sha256:
    segment_meaning: "feature_layer_gate_report"
    bound_artefact: "phase_4bn_t_feature_layer_gate_report"
    value: db731d1b...6ab08
```

The forbidden-substring guard (`assert_no_forbidden_label_substrings_v002`)
on output column names is preserved verbatim; no column name changes, so
the guard's behaviour is identical.

**Answer to Q6:** the 40-column `LABEL_SCHEMA_V002` output is retained
unchanged; the two lineage columns referencing Phase 4bm-J/4bm-L/Stage-5
artefacts are **reinterpreted** (re-mapped per-row to the Phase 4bn-T and
Phase 4bn-P witnesses), recorded authoritatively in the manifest; **no new
label schema version is required** (so the no-v003/no-new-version
preference is honoured); and **no residual ambiguity blocks label
execution** once the §16 segment-scoped config-hash builder and this
re-mapping are implemented with tests.

## 18. Selected pre-v002 envelope-terminal convention

The future pre-v002 label segment must lock `envelope_terminal_unix_ms` to
the **pre-v002 segment terminal**:

- `envelope_terminal_unix_ms` = the **maximum `source_transact_time_ms` /
  `feature_timestamp_ms` within 2024-11-30** (the segment's last date),
  computed over the approved 275-date pre-v002 segment only — **never** the
  v002 90-day envelope. `envelope_terminal_utc_date = "2024-11-30"`.
- For each feature row `R`, the target is `feature_timestamp_ms + H_ms` for
  `H ∈ {1000, 5000, 15000, 60000}` ms. **If the target exceeds
  `envelope_terminal_unix_ms`, all horizon labels are null and
  `horizon_censored_flag_{H}` is true** (and `label_any_censored_flag` is
  true); otherwise the reference row is the largest-`row_index` normalized
  aggTrade row across the segment envelope with `transact_time_ms ≤
  target`. Cross-day reference is allowed **only within** the segment
  envelope (2024-03-01 .. 2024-11-30).
- **No 2024-12-01+ (v002 terminal) row may be read** for horizons,
  reference, or context. **No sealed-test row (2025-02-14 .. 2025-02-28)
  may be read.** Forward ≤60 s horizons near 2024-11-30 censor at the
  segment terminal rather than stitching into 2024-12-01.
- **No holdout-boundary memo is required** under this conservative
  terminal policy. A holdout-boundary memo becomes required **only if** a
  future design proposes to read the v002 terminal window or sealed-test
  dates (e.g. to avoid censoring the last ≤60 s of 2024-11-30 by stitching
  forward) — which this memo explicitly does not.

**Answer to Q7:** the segment terminal is max `transact_time_ms` /
`feature_timestamp_ms` within 2024-11-30; horizons crossing it censor; no
2024-12-01+ or sealed-test rows are read; no holdout-boundary memo
required.

## 19. Selected full-envelope label reference convention

The eventual full 12-month label envelope (2024-03-01 .. 2025-02-28) is
identified **by reference, never by rewriting existing v002 label
artefacts.**

**Primary (required of the future label-execution phase):** the pre-v002
label **segment manifest** itself carries the envelope by reference:

- `full_intended_envelope_start = "2024-03-01"`,
  `full_intended_envelope_end = "2025-02-28"`;
- an `existing_v002_label_reference` block recording the published label
  `__v002` family by reference — the manifest path
  `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json`,
  its window (2024-12-01 .. 2025-02-28), and flags `read: false` /
  `mutated: false` (a read-only SHA256 capture of that published manifest
  **for integrity recording only** is permitted at execution time but is
  **never** a mutation and is **never** required by this memo);
- by-reference `existing_v002_terminal_window`
  (`read: false`, `feature_normalized_raw_dates_read: false`) and
  `existing_v002_sealed_test_split` (`touched: false`) blocks, identical in
  spirit to the feature/normalized segment manifests.

**Companion (defined, deferred, optional):** a separate **full-envelope
label reference / assembly manifest**

```text
microstructure_labels_aggtrades_v001__v002_full_envelope_reference_<phase-id>.json
```

may later be written — by the label-execution phase **or** by the
label-layer gate — **only if** a single 12-month label handle is needed
downstream. It is a **thin, non-eligible, by-reference index** naming
exactly two halves: the pre-v002 label segment manifest (path + SHA256)
and the published label `__v002` manifest (path + SHA256, read-only). It
**must not** read or recompute the v002 terminal label family, **must
not** read v002 terminal feature/normalized/raw dates, **must not** mutate
`microstructure_labels_aggtrades_v001__v002.json`, **must not** create
v003, and **must not** flip eligibility. **This memo neither creates nor
requires the companion manifest; it only defines its shape so a future
phase can produce it cleanly.**

**Answer to Q8/Q9:** the full 12-month envelope is identified **by
reference** (segment-manifest fields now; optional deferred full-envelope
label reference manifest later). To "segment manifest only / separate
reference manifest / both / neither": **both, sequenced** — the segment
manifest is mandatory at execution; the full-envelope label reference
manifest is a defined-but-deferred optional companion.

## 20. Future label manifest required fields

The future pre-v002 label **segment manifest** must contain at least:

- **Identity / family:** `dataset_family =
  "microstructure_labels_aggtrades_v001"`; `dataset_version = "v002"`;
  `version = "v002"`; `label_schema_version = "v001"`; `segment_label =
  "pre_v002_segment"`; `data_family = "aggTrades"`; `symbol = "BTCUSDT"`;
  `market = "usdm_futures"`; `dataset_category = "labels"`.
- **Segment / phase:** `phase_id` (the label-execution phase id);
  `source_phase_boundary`; `created_at_unix_ms`; `created_at_utc`;
  `code_commit_sha`; `base_commit_sha`.
- **Label schema:** `column_count = 40`; `lineage_column_count = 17`;
  `label_column_count = 8`; `support_column_count = 14`;
  `schema_column_list` (canonical `LABEL_SCHEMA_V002` order);
  `lineage_column_list`; `label_list`; `support_column_list`;
  `label_family_id = "microstructure_labels_aggtrades_v001"`;
  `dtype_policy` (`DTYPE_POLICY_V002`).
- **Label kernel policy:** `anchor_policy` (`ANCHOR_POLICY_V002`);
  `future_reference_policy` (the §16 pre-v002-segment-terminal variant);
  `direction_threshold_policy` (`DIRECTION_THRESHOLD_POLICY_V002`);
  `null_censoring_policy` (`NULL_CENSORING_POLICY_V002`); `horizon_list`
  and `horizon_ms_list` (1s/5s/15s/60s → 1000/5000/15000/60000);
  `forbidden_label_column_substrings` (the 21-token guard).
- **Config hash:** `label_config_hash` (from the §16 segment-scoped
  builder); `label_config_hash_input_fields` (the explicit list of hashed
  inputs, including the re-specified envelope clause and the
  non-eligible-source SHAs); `feature_config_hash = "0726b41d…"`
  (segment, **not** `819cfa7a…`).
- **Lineage re-mapping:** the `lineage_column_reinterpretation` block
  (§17).
- **Window / inventory:** `date_start = "2024-03-01"`, `date_end =
  "2024-11-30"`, `date_count = 275`, `date_list`, `expected_file_count =
  275`, `produced_file_count`, `row_count` / `total_row_count`,
  `total_footprint_bytes`, and a `per_day_outputs` inventory (per-date
  label Parquet path, parquet SHA256, byte size, row count,
  `per_horizon_censored_counts`, `invalid_price_row_count`, sidecar path,
  sidecar SHA256, paired `source_feature_parquet_sha256`).
- **Censoring aggregates:** `envelope_terminal_unix_ms` (segment
  terminal); `envelope_terminal_utc_date = "2024-11-30"`;
  `censored_per_horizon`; `invalid_price_row_count`.
- **Non-eligible-source lineage (§15):**
  `source_feature_dataset_family = "microstructure_features_aggtrades_v001"`;
  `source_feature_dataset_version = "v002"`;
  `source_feature_segment_manifest_path` + SHA256 (Phase 4bn-S,
  `4881eb87…`) + sidecar SHA256;
  `source_feature_layer_gate_report_path` + SHA256 (Phase 4bn-T,
  `db731d1b…`);
  `source_normalized_segment_manifest_path` + SHA256 (Phase 4bn-O,
  `0e96ae37…`) + sidecar SHA256;
  `source_normalized_layer_gate_report_path` + SHA256 (Phase 4bn-P,
  `3452fd9d…`);
  `source_normalized_schema_version = "NORMALIZED_SCHEMA_V001"` (19
  columns); `source_feature_schema_version = "FEATURE_SCHEMA_V002"` (62
  columns); `source_raw_segment_manifest_path` + SHA256 (`1659e6da…`);
  `source_eligibility_posture = "non_eligible_gate_passed_pending"`.
  **No** Stage-5 / Phase 4bm-L/F/D successor-state field as a required
  precondition.
- **Existing-label linkage (by reference):** `existing_v002_label_reference`
  (published `__v002` label manifest path, window, `read: false`,
  `mutated: false`).
- **Full-envelope-by-reference:** `full_intended_envelope_start =
  "2024-03-01"`, `full_intended_envelope_end = "2025-02-28"`.
- **Eligibility / governance posture:** `research_eligible: false`;
  `eligibility_gate_status: "pending"`;
  `chronological_split_policy: "not_yet_defined"`; the governance labels
  (`labels`/`targets` = `allowed_by_future_phase_only`;
  `ml`/`strategy`/`backtest`/`acquisition`/`paper_shadow_live`/
  `deployment`/`exchange_write` forbidden/unauthorized);
  the boundary confirmations
  (`REQUIRED_LABEL_BOUNDARY_CONFIRMATIONS_V002`, all `True`, including
  `no_label_gate_report`, `no_label_successor_state`,
  `no_successor_authorization`,
  `phase_4aw_flip_research_eligible_invariant_preserved`); the explicit
  `*_authorized: False` flags (`diagnostics_authorized`, `ml_authorized`,
  `strategy_authorized`, `backtest_authorized`, `acquisition_authorized`,
  `successor_authorization_after`, `stage_5_label_cleared`,
  `label_family_research_use_authorized`);
  `label_computation_authorized: true` (this is a label-compute artefact);
  `no_successor_authorization: true`.
- **Sealed-test / terminal boundary witnesses:**
  `v002_terminal_window_mode: "by_reference"`;
  `existing_v002_terminal_window` (`read: false`,
  `feature_normalized_raw_dates_read: false`);
  `sealed_test_split_touched: false`; `test_holdout_touched: false`;
  `test_rows_loaded: 0`.
- **Label posture:** `label_computation: "non_eligible_pre_v002_segment"`;
  `ml_use: "forbidden"`; `diagnostics_use: "forbidden"`;
  `strategy_use: "forbidden"`; `backtest_use: "forbidden"`.
- **Partitioning / storage:** partitioning rule (`<SYMBOL>/<YYYY>/<MM>/`);
  primary key (`symbol, utc_date, agg_trade_id, row_index`); storage
  format (Parquet); sidecar policy (canonical two-space `.sha256`).
- **Budget witnesses (Phase 4bn-L):** measured label footprint,
  temporary-workspace footprint, runtime, `D:` free space, and the cap
  thresholds honoured.

The optional **full-envelope label reference manifest**, if later written,
must contain at minimum: `dataset_family`; `dataset_version = "v002"`;
`label_schema_version = "v001"`; `reference_type:
"full_envelope_assembly"`; `full_intended_envelope_start/end`; the two
member references (segment manifest path + SHA256; published `__v002`
label manifest path + SHA256, read-only); `research_eligible: false`;
`eligibility_gate_status: "pending"`; `v002_terminal_window_mode:
"by_reference"`; `sealed_test_split_touched: false`;
`no_successor_authorization: true`.

## 21. Future label manifest forbidden fields

The future label segment manifest (and the optional reference manifest)
**must not** contain any of:

- ML outputs, model outputs, scores, predictions, or `model_*` / `score_*`
  / `prediction_*` fields;
- signal fields, entry/exit fields, or any `signal_*` field;
- PnL, equity, profit/loss, position, or backtest fields;
- strategy fields, alpha, or edge fields;
- diagnostic scores, statistics, or research-quality metrics;
- any field asserting or implying `research_eligible: true`,
  `eligibility_gate_status` other than `"pending"`, a
  `chronological_split_policy` value other than `"not_yet_defined"`,
  `diagnostics_authorized: true`, or `ml_authorized: true`;
- any "research-ready" / "admissible-for-ML" / "approved-for-backtest"
  claim;
- any Stage-5 research-use successor-state reference presented as a
  required precondition for this segment, and no field implying
  `stage_5_label_cleared: true` or
  `label_family_research_use_authorized: true`;
- any `v003`, mark-price, funding, open-interest, order-book, spot,
  cross-venue, tick, or ETHUSDT field;
- any extra-horizon field beyond 1s/5s/15s/60s;
- any barrier / target-before-stop / stop / MFE / MAE / R-multiple /
  PnL-label semantics, or any of the 21 forbidden column substrings in any
  output column name.

The locked forbidden-substring guard already enforced by the label kernel
on **column names** (`assert_no_forbidden_label_substrings_v002`) is
preserved verbatim and extends in spirit to manifest fields.

## 22. Future label output directory convention

The future pre-v002 label Parquet output uses a **version-suffixed segment
directory distinct from the published `__v002/` label directory**:

```text
data/microstructure/labels/microstructure_labels_aggtrades_v001__v002_pre_v002_segment_<label-phase-id>/BTCUSDT/<YYYY>/<MM>/BTCUSDT-labels-aggtrades-<YYYY-MM-DD>.parquet
```

each with a paired canonical two-space `.sha256` sidecar.

- This is **not** the published
  `microstructure_labels_aggtrades_v001__v002/` directory (which remains
  immutable); the future bounded wrapper must build a segment-suffixed
  `family_dir`, exactly as `labels_io_v002` builds `V002_LABEL_DIR_SEGMENT`
  for `__v002` and as `phase4bn_s` did for the feature segment.
- It is **not** a generic `microstructure_labels_aggtrades_v001/`
  directory.
- It is **not** a new `__vNNN` directory.

Because label directories are version-suffixed, the segment directory
keeps the pre-v002 label Parquets cleanly separate from the published
`__v002` label Parquets, so the published v002 label family stays immutable
and the segment is self-describing.

**Answer to Q2:** the future pre-v002 label output directory uses
`microstructure_labels_aggtrades_v001__v002_pre_v002_segment_<label-phase-id>`
(not the published `__v002`, not a generic label directory, not a new
`__vNNN`).

## 23. Future label execution implications

A future, separately-authorized **label-only execution phase** must:

- build a **bounded new `phase4bn_*` wrapper** reusing the locked label
  primitives (`labels_schema_v002`, the label kernel
  `compute_aggtrade_labels_v002_for_day` / `labels_compute_v002`,
  `labels_io_v002`, `labels_manifest_v002`'s validation helpers,
  `labels_validation`) unchanged, and adding: the §15 non-eligible-source
  precondition (Phase 4bn-S feature segment manifest SHA + Phase 4bn-T gate
  report PASS + Phase 4bn-O / 4bn-P normalized witnesses, **not** a Stage-5
  successor or `819cfa7a…`); the §16 segment-scoped `label_config_hash`
  builder; the §17 lineage re-mapping; the §18 pre-v002 envelope terminal;
  the §14/§22 segment naming; segment-scoped path/manifest helpers; and the
  Phase 4bn-L preflight/budget caps;
- read **only** the approved 275 feature segment dates (Phase 4bn-S, four
  anchor columns) and the 275 normalized segment dates (Phase 4bn-O, trade
  prices), each verified by SHA256; never open the published `__v002`
  feature/normalized/label families; never read v002 terminal dates; never
  read sealed-test dates;
- write **only** label Parquet + canonical sidecars under the §22 segment
  directory, plus a single non-eligible label segment manifest + sidecar
  under `data/microstructure/manifests/`; refuse to overwrite any finalised
  file; atomic write-then-rename;
- preserve the locked 40-column `LABEL_SCHEMA_V002` verbatim (17 lineage +
  `label_config_hash` + 8 label + 14 support), the canonical column order,
  and the forbidden-substring column guard; preserve the causal
  forward-return/direction semantics (no barrier/stop/MFE/MAE/R-multiple);
- leave the published label `__v002` directory and
  `microstructure_labels_aggtrades_v001__v002.json` manifest
  **byte-for-byte unchanged** (read-only-by-reference at most);
- honour the Phase 4bn-L budget (label-layer 75 GiB warn / 125 GiB hard
  footprint; 4 h warn / 8 h hard runtime; temporary workspace 50 GiB / 100
  GiB; total derived-stack 250 GiB warn / 300 GiB hard; `D:` free ≥ 500 GiB
  before, fail closed below 350 GiB during) and **stop before writing** on
  any breach;
- leave all outputs non-eligible (`research_eligible: false`,
  `eligibility_gate_status: "pending"`, `no_successor_authorization:
  true`); commit no data artefact; create no ML outputs, diagnostics,
  strategy/signal/PnL/backtest outputs, research outputs, database, v003, or
  compacted Parquet;
- carry its own offline test module (segment naming, date guard,
  non-eligible-source precondition, the §16 config-hash builder, the §17
  lineage re-mapping, the §18 envelope-terminal censoring,
  causal/no-leakage, forbidden-column guard, manifest-writer field contract
  + forbidden-field absence, refuse-overwrite, budget-cap, no-network,
  no-sealed-read, non-eligible posture) mirroring the Phase 4bn-O / 4bn-S /
  4bn-P / 4bn-T test precedents;
- preserve the Phase 4aw `flip_research_eligible(...)` always-raises
  invariant (never invoked).

A future label phase must **fail closed** (stop, report partial outputs,
leave all outputs non-eligible and uncommitted) on any of: missing/invalid
Phase 4bn-S feature segment manifest, Phase 4bn-T gate report, Phase 4bn-O
normalized segment manifest, or Phase 4bn-P gate report; any gate report
not PASS; source segment not `research_eligible: false` /
`eligibility_gate_status: "pending"`; feature/normalized per-day SHA256
mismatch; any date outside 2024-03-01 .. 2024-11-30; any attempt to read
the v002 terminal feature/normalized/raw window or sealed-test dates; any
label requiring a horizon crossing the segment terminal that would require
reading 2024-12-01+ data without a separately authorized holdout-boundary
memo; any label requiring data not present in the approved feature +
normalized segment; preflight cannot estimate footprint; label estimate >
125 GiB; total derived-stack > 300 GiB; `D:` free < 500 GiB before or < 350
GiB during; temp workspace > 100 GiB; runtime > 8 h; any output outside the
§22 segment directory; any `data/research` output; any ML / diagnostics /
strategy / PnL / backtest; any database / Parquet compaction / v003; any
`research_eligible` flip or `eligibility_gate_status` transition; any
`data/microstructure` or `data/research` commit; any forbidden manifest
field; any forbidden output-column substring.

## 24. Future label-layer gate implications

A future, separately-authorized **label-layer eligibility gate** (design
level only; **not** run here; analogous to the Phase 4bn-P normalized-layer
gate and the Phase 4bn-T feature-layer gate, built as a bounded read-only
segment-wrapper rather than the v002-lineage-hardcoded `multiday_label_gate*`)
should validate, at minimum:

- the label segment manifest exists, parses, and matches the §20
  required-field contract; the §21 forbidden fields are absent;
- every per-date label Parquet exists with a canonical sidecar; recomputed
  SHA256s match the segment manifest; recomputed aggregates (date count =
  275, total label rows, per-date row counts, contiguous in-segment dates,
  segment footprint, per-horizon censored counts, invalid-price counts)
  match;
- the schema is exactly the locked 40-column `LABEL_SCHEMA_V002` (17
  lineage + `label_config_hash` + 8 label + 14 support) in canonical order
  with the forbidden-substring column guard passing; the
  anchor/reference/direction/censoring/dtype policies match the §16
  segment-scoped `label_config_hash`; the `label_config_hash` recomputes
  from the segment-scoped builder over the recorded inputs;
- the `envelope_terminal_unix_ms` equals the recomputed pre-v002 segment
  terminal; every horizon with `target > envelope_terminal_unix_ms` is
  censored; no reference row lies past 2024-11-30;
- predecessor integrity: the Phase 4bn-S feature segment manifest SHA256
  (`4881eb87…`), the Phase 4bn-T feature-layer gate report SHA256
  (`db731d1b…`, PASS), the Phase 4bn-O normalized segment manifest SHA256
  (`0e96ae37…`), and the Phase 4bn-P normalized-layer gate report SHA256
  (`3452fd9d…`, PASS) still match; the per-day source feature/normalized
  Parquet SHA256s are consistent;
- the published `__v002` label family was not mutated (by-reference); the
  v002 terminal feature/normalized/raw window and sealed-test split were
  not read;
- `research_eligible` remains `false` and `eligibility_gate_status` remains
  `"pending"` — **a passing label-layer gate does NOT flip eligibility,
  does NOT authorize ML / diagnostics / strategy / split policy /
  backtests, and does NOT authorize any successor.**

## 25. Sealed-test and v002 terminal boundary

- The new pre-v002 label segment covers **2024-03-01 .. 2024-11-30**,
  which contains **no** sealed-test dates and **no** v002 terminal-window
  dates.
- The label kernel is **strictly causal**: each forward horizon reads a
  reference row only if `target_timestamp_ms ≤ envelope_terminal_unix_ms`;
  with the envelope terminal locked to the pre-v002 segment terminal
  (2024-11-30; §18), the last ≤60 s of 2024-11-30 **censor** rather than
  reading any 2024-12-01+ row. All in-envelope cross-day references stay
  **inside** 2024-03-01 .. 2024-11-30.
- The existing v002 terminal **feature / normalized / raw** window is
  treated **by reference only** (`v002_terminal_window_mode:
  "by_reference"`); it is not read by any convention in this memo. The
  published label `__v002` family is likewise by reference only and
  immutable.
- The sealed v002 test split **2025-02-14 .. 2025-02-28** remains
  **untouched** (`sealed_test_split_touched: false`,
  `test_holdout_touched: false`, `test_rows_loaded: 0`). Sealing is
  enforced at the ML/split layer (`iter_partitions(split="test", ...)`
  always raises), independent of label scope.
- Because the conservative pre-v002-only label scope reads neither the v002
  terminal window nor sealed-test dates, **a holdout-boundary memo is NOT
  required** to proceed. It becomes required **only if** a future label
  phase proposes to read the v002 terminal window or sealed-test dates
  (e.g. to provide forward context past 2024-11-30) — which this memo
  explicitly does not.

## 26. Decision

**Result state:**
`RECORD_LABEL_MANIFEST_VERSIONING_CONVENTION__REMAIN_PAUSED`.

**Decision:**
`RECOMMEND_AUTHORIZE_LABEL_ONLY_EXECUTION__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Rationale (repository-evidence-grounded): the predeclared preferred
decision when the memo **successfully resolves label manifest/versioning,
`label_config_hash`, lineage, and envelope-terminal policy without
requiring v003 or v002 terminal/sealed-test reads** is exactly this
option. This memo resolves the convention cleanly by mirroring the
already-merged raw-, normalized-, and feature-layer segment precedents:

- a phase-scoped label segment manifest + version-suffixed segment
  directory marked `pre_v002_segment` under `dataset_version: "v002"`,
  `label_schema_version: "v001"` (§14/§22);
- a non-eligible-source precondition built on the Phase 4bn-S feature
  segment manifest + Phase 4bn-T feature-layer gate PASS + Phase 4bn-O /
  4bn-P normalized witnesses, replacing the Stage-5 research-use
  successor-state precondition (§15);
- a new segment-scoped `label_config_hash` builder that preserves the
  label policy fields, re-specifies the envelope-terminal clause, replaces
  the successor-state input with the Phase 4bn-T / 4bn-P witnesses, and
  binds `feature_config_hash = 0726b41d…` (not `819cfa7a…`) (§16);
- the 40-column `LABEL_SCHEMA_V002` retained verbatim with the two
  terminal-specific lineage columns re-mapped to the Phase 4bn witnesses
  and recorded in the manifest (§17);
- the `envelope_terminal_unix_ms` locked to the pre-v002 segment terminal
  so horizons censor at 2024-11-30 and never read 2024-12-01+ (§18);
- the full 12-month label envelope represented by reference
  (segment-manifest fields now; optional deferred full-envelope label
  reference manifest later) (§19).

The resolution requires **no v003**, **no mutation of any published
`__v002` label manifest or directory**, **no read or rewrite of the v002
terminal label family**, **no read of v002 terminal
feature/normalized/raw dates**, **no sealed-test read**, and **no
eligibility flip**. Phase 4bn-U already established that the label
**primitives** are safe and reusable (needing only a bounded new wrapper +
segment-scoped gate) and that the sealed-test / v002 terminal boundary is
clear for the conservative pre-v002 scope (so a holdout-boundary memo is
**not** required). Exactly as the feature arc did (readiness 4bn-Q →
manifest/versioning memo 4bn-R → execution 4bn-S → gate 4bn-T), the
cleanest next technical step is a separately-authorized label-only
execution phase honouring §15–§24 and the Phase 4bn-L budget — including
the §16 segment-scoped config-hash builder and §17 lineage re-mapping
implemented with offline tests before any write. The need for a bounded
new wrapper + config-hash builder + tests does **not** make the convention
ambiguous; the convention is fully specified here, exactly as the Phase
4bn-R feature memo specified a bounded new feature wrapper and still
recommended feature-only execution.

The full set of admissible Phase 4bn-V decision options was:
`RECORD_LABEL_MANIFEST_VERSIONING_CONVENTION__REMAIN_PAUSED`;
`RECOMMEND_AUTHORIZE_LABEL_ONLY_EXECUTION__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
(selected);
`RECOMMEND_AUTHORIZE_DOCS_ONLY_HOLDOUT_BOUNDARY_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
(not selected; boundary clear/safe under the conservative envelope rule);
`RECOMMEND_AUTHORIZE_SOURCE_POLICY_DOCUMENTATION_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
(not selected; source policy settled);
`RECOMMEND_AUTHORIZE_PROCESS_DOC_PATH_UPDATE__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
(not selected); `RECOMMEND_CLOSE_ML_BASELINE_ARC__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
(not selected; evidence does not warrant closing the arc).

This memo **does not authorize** the successor; the operator decides
separately. **No successor is authorized from inside Phase 4bn-V.**

## 27. Recommended state and successor options

**Recommended state: remain paused.** Phase 4bn-V is **branch-complete
only**; not merged into `main`; not project-complete until a separately
authorized merge phase records its merge-closeout on `main` per
`merge-closeout-standard.md` (Tier 1).

**Operator options (each subject to separate operator authorization; none
authorized here):**

- remain paused (default);
- request a merge prompt for Phase 4bn-V;
- separately authorize a **label-only execution phase** (this memo's
  recommendation) — a bounded new `phase4bn_*` wrapper over the Phase
  4bn-S feature + Phase 4bn-O normalized pre-v002 segments honouring
  §14–§24 and the Phase 4bn-L budget, followed (only if separately
  authorized) by a bounded label-layer eligibility gate;
- separately authorize a **docs-only holdout-boundary memo** — **not
  required** for the conservative pre-v002-only label scope; only relevant
  if a future label phase intends to read the v002 terminal window or
  sealed-test dates;
- separately authorize a **source-policy documentation memo**;
- separately authorize a **process-doc `D:` path-string update** (the
  Phase 4bm-D-P1 lightweight-workspace standard still carries old `C:`
  example paths);
- reject further ML-baseline successors and **close the ML-baseline arc**.

**Required successor validation/gate phases after any future label
execution (predeclared, none authorized):** a bounded **label-layer
eligibility gate** (§24) before any downstream stage; then, only if
separately authorized, a chronological-split / holdout policy memo before
any ML or diagnostics.

## 28. Explicit non-authorizations

Phase 4bn-V did **not** and does **not** authorize: label derivation;
label artefact generation; label manifest creation or mutation; label gate
execution; feature derivation; feature-layer-gate rerun; normalization
rerun; normalized-layer-gate rerun; raw acquisition; any endpoint /
public / Binance / `data.binance.vision` call; archive or CHECKSUM
download; HEAD preflight; raw-gate rerun; any local raw / normalized
Parquet / feature Parquet / label / gate-report / manifest read under
`data/microstructure`; any `data/research` read or write; any v002 terminal
raw / normalized / feature window read; any sealed-test read; diagnostics;
ML training; model scoring; predictions; feature ranking / selection /
pruning; label optimization / threshold tuning / hyperparameter tuning /
calibration fitting; strategy research; signal generation; PnL simulation;
backtests; manifest mutation; successor-state mutation; gate-report
mutation; `research_eligible` flip; `eligibility_gate_status` transition;
`chronological_split_policy` transition; `diagnostics_authorized` or
`ml_authorized` transition; `data/research` or `data/microstructure`
artefact creation or commit; storage migration; DuckDB / SQLite /
`.duckdb` / `.sqlite` / database creation; Parquet compaction; v003
creation; ETHUSDT; extra horizons beyond 1s/5s/15s/60s; mark-price; spot;
cross-venue; order book; tick data; paper / shadow; live-readiness;
deployment; exchange-write; production keys; any Phase 5; or any successor
phase.

Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m
thread / V2 / G1 / C1) and every project lock (§11.6 = 8 bps per side;
round-trip = 16 bps; §1.7.3; Phase 3p §4.7; Phase 3r §8; Phase 3v §8;
Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase
4v; Phase 4w; Phase 4ak M0; Phase 4al refined no-rescue rule; Phase 4aw
`flip_research_eligible(...)` always-raises invariant (never invoked);
Phase 4bb-F canonical path + sidecar policy; the Phase 4bn-J-R1 raw-only
cap amendment; the Phase 4bn-L derived-stack storage budget; the Phase
4bn-N normalization manifest/versioning convention; the Phase 4bn-R
feature manifest/versioning convention) is preserved verbatim. Phase 4
canonical remains unauthorized.

## 29. Current-project-state update summary

`docs/00-meta/current-project-state.md` was updated narrowly: a new Phase
4bn-V prose paragraph was appended after the Phase 4bn-U paragraph, and a
new `Current phase:` block for Phase 4bn-V was inserted ahead of the Phase
4bn-U block. All prior Phase 4bn-A … 4bn-U paragraphs and `Current phase:`
blocks are preserved verbatim as labelled historical context. No other
section of `current-project-state.md` was changed. No code, test, script,
data file, configuration, `.gitignore`, `README.md`, MCP file, manifest,
sidecar, gate report, or successor-state artefact was created or modified.
No local data was read; no local data was created.
