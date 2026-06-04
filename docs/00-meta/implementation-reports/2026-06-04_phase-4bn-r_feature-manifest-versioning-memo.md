# Phase 4bn-R — Feature Manifest / Versioning Memo

## 1. Purpose

This memo is a **docs-only feature-manifest / feature-versioning /
non-eligible-source precondition / boundary-contract** deliverable. It
resolves, from committed repository documentation and committed tooling
only, the **feature manifest/versioning ambiguity** and the
**non-eligible-source precondition divergence** that Phase 4bn-Q
identified as the single binding obstacle to authorizing a future
feature-only execution phase over the Phase 4bn-O / 4bn-P local
gitignored pre-v002 BTCUSDT Binance USDⓈ-M futures aggTrades normalized
segment (2024-03-01 .. 2024-11-30 inclusive UTC; 275 dates;
400,001,695 events).

This phase **derives no features**, **creates no feature artefacts**,
and **creates or mutates no manifest or gate report**. It records, at
design level only, the exact manifest/versioning shape a future
pre-v002 **feature** segment must use, how that segment links to the
Phase 4bn-O normalized segment manifest and the Phase 4bn-P
normalized-layer gate report, how it must replace the existing Stage-3
research-eligible successor-state precondition with a non-eligible-source
precondition, and how the eventual full 12-month feature envelope is
identified **without creating v003, mutating any published `__v002`
feature manifest or directory, reading or rewriting the v002 terminal
feature family, reading v002 terminal normalized dates, touching the
sealed test split, or flipping research eligibility.**

This memo answers exactly the question Phase 4bn-Q deferred:

> What exact manifest/versioning shape should a future pre-v002 feature
> segment use, how should it link to the Phase 4bn-O normalized segment
> and Phase 4bn-P normalized-layer gate, how should it handle the
> non-eligible-source precondition without requiring a Stage-3
> research-eligible successor-state, and how should the eventual
> 12-month feature envelope be represented without creating v003,
> mutating published `__v002` feature artefacts, reading the v002
> terminal window, touching sealed-test dates, or flipping research
> eligibility?

It does **not** ask whether the project can start ML, create labels,
run the model, find edge, backtest, trade, use the sealed test split, or
make the dataset research-eligible.

## 2. Authority and repository state

- **Active local repo path:** `D:\Prometheus`. **Active Claude Code
  lightweight workspace:** `D:\ClaudeRuns\prometheus-light`.
- **GitHub remote:** `origin` → `https://github.com/jpedrocY/Prometheus.git`
  (verified intact).
- **Branch:** `phase-4bn-r/feature-manifest-versioning-memo`.
- **Base `main` SHA:** `014c58add240e2c0bd2666b971cb76024942f89d`
  (`docs(phase-4bn-q): finalize merge closeout shas`). Pre-branch
  `main == origin/main == HEAD` was verified in sync. The Phase 4bn-Q
  merge-closeout SHA-finalization commit `014c58a`, merge-closeout
  `51a20a2`, merge `7ac685b`, and branch commit `b7f8f2c` are all
  present on `main`; the Phase 4bn-P SHA-finalization commit `b2b46de`
  is present as predecessor.
- **Tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3. This phase
  settles the feature manifest/versioning convention and the
  non-eligible-source precondition adjacent to future feature artefact
  generation over the Phase 4bn-O / 4bn-P pre-v002 normalized segment,
  future feature-layer eligibility gates, future label derivation,
  future chronological split/holdout policy, future ML-baseline
  admissibility, and local disk/runtime budgets — while explicitly
  authorizing no feature derivation, no labels, no ML, no diagnostics,
  no strategy, no research-eligibility flip, and no downstream use.
- **Working-tree expectation:** only the untracked transient
  `.claude/scheduled_tasks.lock`; the gitignored namespaces
  `data/microstructure/` (`.gitignore:85`) and `data/research/`
  (`.gitignore:88`) exist locally (Phase 4bn-O normalized outputs +
  Phase 4bn-P gate report) and remain uncommitted.

## 3. Phase type and strict scope

**Phase type:** docs-only / feature-manifest / feature-versioning /
non-eligible-source precondition / boundary-contract.

**Allowed work performed by this phase:**

- read committed Markdown docs;
- inspect committed source, scripts, and tests read-only;
- identify the existing feature manifest construction and validation
  conventions;
- identify the existing `__v002` feature-family manifest / directory
  convention from committed code/docs only;
- define the future pre-v002 feature segment manifest naming
  convention;
- define the future feature output directory naming convention;
- define the non-eligible-source precondition that replaces the Stage-3
  research-eligible successor-state precondition for this pre-v002
  segment;
- define predecessor linkage to the Phase 4bn-O normalized segment
  manifest, the Phase 4bn-P normalized-layer gate report, the Phase
  4bn-N normalization manifest/versioning convention, the existing
  published feature `__v002` family by reference, and the
  dataset-versioning rules;
- define how the eventual 12-month feature envelope is represented by
  reference;
- define what future feature execution must write and must not mutate;
- define required offline tests for the future bounded feature wrapper
  and feature manifest writer;
- define future feature-layer gate implications;
- create the two tracked Phase 4bn-R docs and update
  `current-project-state.md` narrowly.

**This phase did NOT and must NOT (within Phase 4bn-R):** derive
features; create feature artefacts; create or mutate any feature
manifest; run feature gates; read any local normalized Parquet, feature
file, label file, or `data/research` artefact; read any local
`data/microstructure` manifest or gate report; create
`data/microstructure` or `data/research` outputs; run labels, ML,
diagnostics, strategy, signals, PnL, or backtests; acquire data; call
any endpoint; inspect any raw zip contents; touch the v002 terminal raw
or normalized window; touch the sealed test split; create a database;
compact Parquet; create v003; or authorize any successor.

## 4. Evidence base and input boundary

**Inputs read (committed repository evidence only):**

- `docs/00-meta/current-project-state.md` (Phase 4bn-Q / 4bn-P / 4bn-O
  / 4bn-N / 4bn-L paragraphs and `Current phase:` blocks);
- the process standards `merge-closeout-standard.md`,
  `phase-risk-tiering-standard.md`, `phase-workflow-standard.md`,
  `phase-prompt-template.md`, `operator-report-standard.md`;
- the Phase 4bn-Q feature-derivation readiness/execution-plan memo,
  merge-closeout, and closeout; the Phase 4bn-P normalized-layer gate
  report narrative, merge-closeout, and closeout; the Phase 4bn-O
  normalization-only execution memo, merge-closeout, and closeout; the
  Phase 4bn-N normalization manifest/versioning memo, merge-closeout,
  and closeout; the Phase 4bn-L derived-stack storage-budget memo,
  merge-closeout, and closeout;
- the data specs `data-requirements.md`, `historical-data-spec.md`,
  `timestamp-policy.md`, `dataset-versioning.md`, and
  `database-design.md`;
- committed feature/manifest/derived tooling read-only:
  `src/prometheus/research/microstructure/features_schema_v002.py`,
  `features_compute_v002.py`, `features_io_v002.py`,
  `features_manifest_v002.py`, `features_schema.py`,
  `multiday_feature_gate.py`, `multiday_feature_gate_v002.py`;
  `scripts/phase4bm_h_compute_multiday_features.py`,
  `scripts/phase4bm_j_run_multiday_feature_gate.py`; and the committed
  offline test surface under `tests/research/microstructure/`.

**Inputs explicitly NOT used:** any local normalized Parquet, raw zip,
feature file, label file, gate report, manifest, sidecar,
successor-state, or `data/research` artefact; the v002 terminal raw or
normalized window; the sealed v002 test split; no hashing, counting, or
inspection of local gitignored data; no endpoints; no credentials; no
`.env`; no `.mcp.json`; no MCP; no Graphify. **README was treated as
potentially stale and was not used as current-state authority.** SHA256
digests cited for local gitignored artefacts (the Phase 4bn-O segment
manifest + sidecar, the Phase 4bn-P gate report, the raw segment
manifest, raw gate report, raw acquisition log) are quoted **from
committed Markdown evidence** (prior closeouts / current-project-state),
not by reading the local files.

## 5. Phase 4bn-Q finding carried forward

Phase 4bn-Q (merge-complete on `main`, SHA `014c58a`) concluded:

1. **Feature primitives are SAFE and directly reusable**
   (`features_schema_v002`, `features_compute_v002`,
   `features_io_v002`, `features_manifest_v002`, `features_schema`):
   62-column `FEATURE_SCHEMA_V002` (17 lineage + 45 feature/quality),
   causal-only (`LEAKAGE_POLICY_V002 = "causal_only_no_future_lookahead"`,
   backward-only 60 s cross-day tail), 26-token forbidden-substring
   column guard, canonical two-space `.sha256` sidecars, atomic
   refuse-overwrite writes, network-free, credential-free; offline test
   suite present; **no** label/target/future-return/model columns.
2. **The feature compute orchestrator
   `scripts/phase4bm_h_compute_multiday_features.py` and the feature
   gate `multiday_feature_gate*` (Phase 4bm-J) are NOT directly
   reusable and NEED bounded new wrappers** — both are hardcoded to the
   90-day v002 terminal window (2024-12-01 .. 2025-02-28; count 90;
   155,153,449 events), expect the **published `__v002` normalized
   manifest**, **require the Phase 4bm-F Stage-3 research-eligible
   successor-state**, assume the published `__v002` feature family
   directory, and have **no** Phase 4bn-L preflight/budget caps;
   existing tests do not cover the pre-v002 segment shape.
3. **Feature manifest/versioning + the non-eligible-source precondition
   is AMBIGUOUS and requires this docs-only memo** — (a) the existing
   feature tooling hard-requires a Stage-3 **research-eligible**
   successor-state source that the non-eligible pre-v002 segment does
   not (and must not) have; and (b) the pre-v002 **feature segment**
   manifest/versioning shape and non-eligible posture are not codified
   (Phase 4bn-N settled this only for the normalized layer).
4. **The sealed-test / v002 terminal boundary is CLEAR for the
   conservative causal-only pre-v002 feature scope; a holdout-boundary
   memo is NOT required** — the strictly-causal kernel needs no forward
   read into the v002 terminal window for the segment's last day
   (2024-11-30) and no pre-segment read for its first day (2024-03-01;
   early rows flagged `rolling_missing_window_flag`); no segment date
   overlaps the sealed split (2025-02-14 .. 2025-02-28).

Phase 4bn-Q's decision was
`RECOMMEND_AUTHORIZE_DOCS_ONLY_FEATURE_MANIFEST_VERSIONING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
This phase executes exactly that recommended memo. **Finding (3) is the
sole ambiguity this memo resolves; findings (1), (2), and (4) are
carried forward unchanged.**

## 6. Dataset-versioning rules carried forward

`docs/04-data/dataset-versioning.md` binds the following for versioned
(including feature) datasets:

- **Version identity** is required; the recommended identifier pattern
  is `<dataset_name>__vNNN`, **monotonic per family**, **never reused or
  overwritten**.
- **Every versioned dataset has a manifest** at the dataset-version
  root, with minimum fields including dataset name, version ID,
  category, creation timestamp, canonical timezone/format, symbol set,
  schema version, transformation/pipeline version, partitioning rules,
  primary key, generator identity, notes, and **predecessor version if
  applicable**.
- **Published versions are immutable**: files, schema, and manifest must
  not be silently modified; corrections create a **new version** that
  records its **predecessor**.
- **Publication states** are `draft` / `published` / `deprecated` /
  `superseded`; only `published` versions are used for formal research.
- **Partition folders do not replace version identity** — directory
  layout is a storage concern; version identity is a governance
  concern.

The doc does **not** codify "segment manifests," predecessor-linked
backward extensions, or how a backward feature segment relates to an
already-published terminal feature version. The raw layer (Phase
4bn-J-R2 / 4bn-K) and the normalized layer (Phase 4bn-N / 4bn-O)
resolved that gap by precedent; this memo resolves it for the **feature
layer** by the same precedent (see §10–§13).

## 7. Existing feature `__v002` conventions

From committed code (`features_schema_v002.py`, `features_io_v002.py`,
`features_manifest_v002.py`, `features_schema.py`,
`scripts/phase4bm_h_compute_multiday_features.py`, the
`multiday_feature_gate*` modules):

- **Dataset family (schema-lineage marker):**
  `microstructure_features_aggtrades_v001` (`FEATURE_DATASET_FAMILY`).
  The trailing `v001` is part of the **family name** — the locked Phase
  4bh-B feature/quality column set — **not** a window discriminator.
- **Dataset version (window/source discriminator):** the second suffix.
  `__v001` = the single-day Phase 4bh/4bi feature output; `__v002`
  (`FEATURE_DATASET_VERSION_V002 = "v002"`) = the 90-day Phase 4bm-H
  multi-day feature output over the v002 terminal window
  **2024-12-01 .. 2025-02-28**.
- **Feature schema version:** `FEATURE_SCHEMA_VERSION_V002 = "v001"`
  (the feature/quality column set is unchanged from v001; only the
  lineage block differs). `FEATURE_SCHEMA_V002` has **62 columns** = 17
  lineage + 45 feature/quality, canonical order; 4 trailing windows
  (1s/5s/15s/60s). `LEAKAGE_POLICY_V002 =
  "causal_only_no_future_lookahead"`;
  `CROSS_DAY_LOOKBACK_POLICY_V002 = "causal_cross_day_lookback"` with
  `CROSS_DAY_TAIL_BUFFER_MS = 60_000`; a forbidden-substring guard
  rejects column names implying label/target/future/signal/strategy/
  PnL/model/score/prediction/decision/backtest.
- **Feature partition directory (`features_io_v002.py`):**
  `V002_FEATURE_DIR_SEGMENT = f"{FEATURE_DATASET_FAMILY}__{FEATURE_DATASET_VERSION_V002}"`,
  i.e.
  `data/microstructure/features/microstructure_features_aggtrades_v001__v002/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-features-aggtrades-<YYYY-MM-DD>.parquet`,
  each with a paired canonical two-space `.sha256` sidecar
  (`compose_canonical_sidecar_v002`). The feature **directory is
  version-suffixed** — exactly the same asymmetry the normalized layer
  has — so a backward feature segment cannot be written into the
  published `__v002/` directory without blurring the published,
  immutable family.
- **Feature index manifest:**
  `V002_FEATURE_MANIFEST_BASENAME = f"{FEATURE_DATASET_FAMILY}__{FEATURE_DATASET_VERSION_V002}.json"`,
  i.e.
  `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json`,
  paired with a canonical sidecar.
- **Manifest builder (`build_feature_manifest_v002`):** seeds
  `research_eligible: False`, `eligibility_gate_status: "pending"`,
  governance labels (`labels`/`ml`/`strategy`/`backtest`/`acquisition`
  forbidden/unauthorized via `FORBIDDEN_V002_GOVERNANCE_VALUES`), an
  18-key `REQUIRED_V002_BOUNDARY_CONFIRMATIONS` set (all `True`,
  including `no_future_lookahead`,
  `phase_4aw_flip_research_eligible_invariant_preserved`), an 8-flag
  `REQUIRED_V002_NON_AUTHORIZATION_FLAGS` set (all `False`, including
  `successor_authorization_after`), and pins source lineage SHAs:
  `source_normalized_manifest_sha256`, `source_successor_state_sha256`,
  `source_phase_4bm_d_gate_report_sha256`,
  `source_phase_4bm_f_successor_state_sha256`,
  `source_phase_4bl_d_r_raw_gate_report_sha256`,
  `source_phase_4bl_e_raw_successor_state_sha256`,
  `source_v002_raw_manifest_sha256`,
  `source_v002_acquisition_log_sha256`, plus a `per_day_outputs`
  inventory.

**Key asymmetry (drives §10/§16).** Like the normalized layer, feature
directories are version-suffixed, so a pre-v002 backward feature segment
must NOT be written into the published `__v002/` feature directory. Two
**additional** asymmetries are specific to the feature layer: (i) the
v002 feature manifest builder **hard-pins a Stage-3 research-eligible
successor-state** (`source_successor_state_sha256` /
`source_phase_4bm_f_successor_state_sha256`) — the precondition the
non-eligible pre-v002 segment cannot satisfy; and (ii) the orchestrator
and gate are window-hardcoded to the 90-day v002 terminal window. The
locked **primitives** are reusable; the **orchestrator, gate, and
successor-state precondition** are not, and the manifest must replace
the Stage-3 lineage block with a non-eligible-source lineage block.

## 8. Feature manifest/versioning ambiguity being resolved

The pre-v002 **raw** segment (Phase 4bn-J-R2 / 4bn-K) and the pre-v002
**normalized** segment (Phase 4bn-O / 4bn-P) were each represented as a
**phase-scoped segment manifest** rather than a new `__vNNN`:

- **Raw:**
  `microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2.json`
  (SHA256 `1659e6da…3a3d1`).
- **Normalized:**
  `microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json`
  (SHA256 `0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa`),
  validated by the Phase 4bn-P gate report (SHA256
  `3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134`).

Each keeps `dataset_version: "v002"`, adds `segment_label:
"pre_v002_segment"`, records `full_intended_envelope_*` and by-reference
v002-terminal / sealed-split blocks, and forbids v003.

**The ambiguity** has two parts, both specific to the feature layer:

1. **Source-precondition divergence (new).** The existing v002 feature
   orchestrator and gate hard-require a **Stage-3 research-eligible
   successor-state** (Phase 4bm-F) for their normalized source. The
   pre-v002 normalized segment is deliberately **non-eligible**
   (`eligibility_gate_status: "pending"`; no Stage-3 successor exists,
   and Phase 4bn-P explicitly did **not** flip eligibility). What a
   feature wrapper must require **instead**, and what eligibility
   posture the resulting features must carry, is not codified anywhere
   in the repo.
2. **Segment manifest/versioning shape (analogous to Phase 4bn-N, not
   yet applied to features).** The feature layer has no codified rule
   for whether the pre-v002 feature output should be (a) a segment
   manifest mirroring the raw/normalized precedent, (b) a
   predecessor-linked extension of `__v002`, (c) a new full-envelope
   feature version, or (d) directory-only with no manifest;
   `dataset-versioning.md` is silent on backward segments.

This memo selects the shape and defines the non-eligible-source
precondition.

## 9. Non-eligible-source precondition being resolved

The committed v002 feature manifest builder pins a Stage-3
research-eligible successor-state (`source_successor_state_path` /
`source_successor_state_sha256` and
`source_phase_4bm_f_successor_state_sha256`) as the admissibility
predecessor for feature computation. That successor-state is the Phase
4bm-F `stage3_research_eligible` artefact: it exists only because the
v002 terminal normalized family went through a Stage-3 research-eligible
flip. **The pre-v002 segment has no such artefact and must not acquire
one** — Phase 4bn-P recorded `research_eligible: false`,
`eligibility_gate_status: "pending"`, and `no_successor_authorization:
true`, and the Phase 4aw `flip_research_eligible(...)` always-raises
invariant must never be invoked. Therefore the future feature wrapper
**cannot** reuse the Stage-3 successor-state precondition; it needs a
**non-eligible-source precondition** built on the Phase 4bn-P
normalized-layer gate PASS instead. §12 defines that precondition.

## 10. Candidate shapes considered

1. **Phase-scoped feature segment manifest (raw/normalized-precedent
   mirror).** A sibling-shape JSON
   `microstructure_features_aggtrades_v001__v002_pre_v002_segment_<feature-phase-id>.json`
   with `dataset_version: "v002"`, `feature_schema_version: "v001"`,
   `segment_label: "pre_v002_segment"`, its own version-suffixed
   segment directory, full-envelope-by-reference fields, by-reference
   v002-terminal / sealed-split blocks, and a non-eligible-source
   lineage block (Phase 4bn-O segment manifest + Phase 4bn-P gate
   report) replacing the Stage-3 successor-state. **Pros:** exact
   structural and governance parity with the already-merged raw and
   normalized segment precedents; reuses the locked feature primitives
   unchanged; leaves the published `__v002` feature family
   byte-for-byte immutable; no v003; no v002 terminal read. **Cons:**
   longer directory/manifest name than `__vNNN`. **Selected (see §11).**

2. **Predecessor-linked extension of `__v002` (write into the v002
   feature family).** Write pre-v002 feature dates under the existing
   `microstructure_features_aggtrades_v001__v002/` directory and link
   via a `predecessor`/`extends` field. **Cons:** writes new files into
   the **published, immutable** `__v002` feature directory, creating
   parquets the published `__v002.json` feature manifest does not
   reference (the manifest is refuse-overwrite-protected) — i.e.
   orphaned-within-the-family artefacts; blurs the
   "published-version-is-immutable" boundary; **rejected.**

3. **New full-envelope feature version (`__v003` or a single rewritten
   feature envelope).** **Cons:** directly collides with the forbidden
   v003 boundary and the monotonic-immutability rule; would require
   reading the v002 terminal normalized window (including sealed-test
   dates) to recompute a single 12-month feature family; **rejected
   outright.**

4. **No manifest (rely on the directory only).** **Cons:** violates
   `dataset-versioning.md` ("never run formal validation on an
   untracked dataset version"; "partition folders do not replace
   version identity"); a future feature-layer gate would have no
   field-contract to validate; **rejected.**

## 11. Selected feature segment convention

**Selected: Candidate (1) — a phase-scoped feature segment manifest,
mirroring the merged raw-layer and normalized-layer precedents.**

The future pre-v002 feature output is represented as a **phase-scoped
feature segment manifest** — a sibling-shape JSON that is **clearly tied
to the existing v002 feature family but clearly marked as a pre-v002
backward segment / extension**, not a new monotonic version.

- **Manifest filename (under `data/microstructure/manifests/`):**

  ```text
  microstructure_features_aggtrades_v001__v002_pre_v002_segment_<feature-phase-id>.json
  ```

  with a paired canonical two-space `.sha256` sidecar.
  `<feature-phase-id>` is the underscored phase id of the future
  separately-authorized feature-execution phase (e.g. if that phase is
  `4bn-S`, the token is `4bn_s`, yielding
  `microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s.json`).
  This exactly parallels the normalized segment's
  `microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json`
  and the raw segment's
  `microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2.json`.

- **Inner identity fields:** `dataset_family =
  "microstructure_features_aggtrades_v001"` (reused, schema-identical);
  `dataset_version = "v002"` and `version = "v002"` (a **backward
  segment of the v002 envelope**, not a new version);
  `feature_schema_version = "v001"`; `segment_label =
  "pre_v002_segment"`. The window discriminator lives in the
  **filename and directory name**, never as a new `dataset_version` and
  never as a new `feature_schema_version`.

This selection: (i) reuses the locked feature primitives unchanged;
(ii) leaves the published feature `__v002` family — directory, parquets,
sidecars, and `microstructure_features_aggtrades_v001__v002.json`
manifest — **byte-for-byte immutable**; (iii) creates **no** v003;
(iv) reads **no** v002 terminal normalized window and **no** sealed-test
dates; (v) keeps every output non-eligible and pending.

## 12. Selected non-eligible-source precondition

The future feature wrapper must replace the Stage-3 research-eligible
successor-state precondition with the following **non-eligible-source
precondition**:

- **Source admissibility predecessor = the Phase 4bn-P normalized-layer
  gate report**, not a Stage-3 successor-state. The wrapper must verify
  the Phase 4bn-P gate report exists, parses, carries the PASS verdict
  `NORMALIZED_LAYER_GATE_PASSED__LOCAL_NORMALIZED_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`,
  and matches its recorded SHA256
  (`3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134`)
  at the path
  `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o__phase-4bn-p__1780599605192__3fd795ceac4f.json`.
- **Source normalized segment = the Phase 4bn-O segment manifest**,
  verified by SHA256
  (`0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa`)
  at
  `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json`
  (+ sidecar SHA256 `5d7dcbef…6402`); **not** the published `__v002`
  normalized manifest.
- **The source normalized segment must remain non-eligible.** The
  wrapper must read `research_eligible: false` and
  `eligibility_gate_status: "pending"` from the segment manifest and
  must fail closed if either is otherwise. **No `research_eligible:
  true` and no Stage-3 successor-state is required for this pre-v002
  expansion path; none may be created.**
- **Generated feature outputs must remain non-eligible and pending.**
  The feature segment manifest must carry `research_eligible: false`,
  `eligibility_gate_status: "pending"`, `no_successor_authorization:
  true`, and the Phase 4aw `flip_research_eligible(...)` always-raises
  invariant must never be invoked.
- **Generated features cannot be used** for labels, ML, diagnostics,
  strategy, research, or split policy until later, separately
  authorized gates/policies. The governance labels must mark
  `labels`/`ml`/`strategy`/`backtest`/`acquisition` as
  forbidden/unauthorized.

In short: the feature wrapper's lineage block replaces the v002
manifest's `source_successor_state_*` /
`source_phase_4bm_f_successor_state_sha256` fields with a
`source_normalized_segment_manifest_*` block (Phase 4bn-O) and a
`source_normalized_layer_gate_report_*` block (Phase 4bn-P), and adds an
explicit `source_eligibility_posture: "non_eligible_gate_passed_pending"`
witness. This is the feature-layer analogue of how Phase 4bn-O sourced
from the Phase 4bn-J-R2 raw segment manifest + Phase 4bn-K raw gate
report rather than the published `__v002` raw manifest.

## 13. Selected full-envelope feature reference convention

The eventual full 12-month feature envelope (2024-03-01 .. 2025-02-28)
is identified **by reference, never by rewriting existing v002 feature
artefacts.**

**Primary (required of the future feature-execution phase):** the
pre-v002 feature **segment manifest** itself carries the envelope by
reference:

- `full_intended_envelope_start = "2024-03-01"`,
  `full_intended_envelope_end = "2025-02-28"`;
- an `existing_v002_feature_reference` block recording the published
  feature `__v002` family by reference — the manifest path
  `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json`,
  its window (2024-12-01 .. 2025-02-28), and flags `read: false` /
  `mutated: false` (a read-only SHA256 capture of that published
  manifest **for integrity recording only** is permitted at execution
  time but is **never** a mutation and is **never** required by this
  memo);
- by-reference `existing_v002_terminal_window` (`read: false`,
  `normalized_dates_read: false`) and `existing_v002_sealed_test_split`
  (`touched: false`) blocks, identical in spirit to the normalized
  segment manifest.

**Companion (defined, deferred, optional):** a separate **full-envelope
feature reference / assembly manifest**

```text
microstructure_features_aggtrades_v001__v002_full_envelope_reference_<phase-id>.json
```

may later be written — by the feature-execution phase **or** by the
feature-layer gate — **only if** a single 12-month feature handle is
needed downstream. It is a **thin, non-eligible, by-reference index**
that names exactly two halves: the pre-v002 feature segment manifest
(path + SHA256) and the published feature `__v002` manifest (path +
SHA256, read-only). It **must not** read or recompute the v002 terminal
feature family, **must not** read v002 terminal normalized dates,
**must not** mutate `microstructure_features_aggtrades_v001__v002.json`,
**must not** create v003, and **must not** flip eligibility. **This memo
neither creates nor requires the companion manifest; it only defines its
shape so a future phase can produce it cleanly.**

Answer to "segment manifest only / separate reference manifest / both /
neither": **both, sequenced** — the segment manifest is mandatory at
execution; the full-envelope feature reference manifest is a
defined-but-deferred optional companion.

## 14. Future feature manifest required fields

The future pre-v002 feature **segment manifest** must contain at least:

- **Identity / family:** `dataset_family =
  "microstructure_features_aggtrades_v001"`; `dataset_version =
  "v002"`; `version = "v002"`; `feature_schema_version = "v001"`;
  `segment_label = "pre_v002_segment"`; `data_family = "aggTrades"`;
  `symbol = "BTCUSDT"`; `market = "usdm_futures"` (Binance USDⓈ-M
  futures); `dataset_category = "features"`.
- **Segment / phase:** `phase_id` (the feature-execution phase id);
  `source_phase_boundary`; `created_at_unix_ms`; `created_at_utc`;
  `code_commit_sha`; `base_commit_sha`; `feature_config_hash`.
- **Feature schema:** `feature_column_count = 62`; `lineage_column_count
  = 17`; `feature_quality_column_count = 45`; `feature_column_names`
  (canonical `FEATURE_SCHEMA_V002` order); `lineage_column_names`;
  `computed_feature_column_names`; `feature_dtypes`; `feature_family_id =
  "microstructure_features_aggtrades_v001"`; a `feature_schema_hash` if
  the repo convention supports a stable config hash (the v002 builder's
  `feature_config_hash` satisfies this).
- **Feature kernel policy:** `leakage_policy =
  "causal_only_no_future_lookahead"`; `cross_day_lookback_policy =
  "causal_cross_day_lookback"`; `cross_day_tail_buffer_ms = 60000`;
  `feature_windows_ms` / `feature_window_labels` (1s/5s/15s/60s);
  `window_boundary_policy`; `invalid_window_policy`;
  `same_timestamp_tie_rule`; `timestamp_policy`;
  `forbidden_substring_detector_tokens`.
- **Window / inventory:** `date_start = "2024-03-01"`, `date_end =
  "2024-11-30"`, `date_count` (275), `date_list`, `expected_file_count`
  (275), `produced_file_count`, `total_row_count` /
  `actual_feature_row_count`, `total_footprint_bytes`, and a
  `per_file_inventory` / `per_day_outputs` (per-date feature parquet
  path, parquet SHA256, parquet size bytes, row count, sidecar path,
  sidecar SHA256, paired source normalized per-day parquet SHA256).
- **Non-eligible-source lineage (§12):**
  `source_dataset_family = "microstructure_normalized_aggtrades_v001"`;
  `source_dataset_version = "v002"`;
  `source_normalized_segment_manifest_path` + SHA256 (Phase 4bn-O,
  `0e96ae37…d9fa`);
  `source_normalized_layer_gate_report_path` + SHA256 (Phase 4bn-P,
  `3452fd9d…f134`); `source_normalized_schema_version =
  "NORMALIZED_SCHEMA_V001"` (19 columns);
  `source_eligibility_posture =
  "non_eligible_gate_passed_pending"`. **No** Stage-3 successor-state
  field.
- **Existing-feature linkage (by reference):**
  `existing_v002_feature_reference` (published `__v002` feature manifest
  path, window, `read: false`, `mutated: false`).
- **Full-envelope-by-reference:** `full_intended_envelope_start =
  "2024-03-01"`, `full_intended_envelope_end = "2025-02-28"`.
- **Eligibility / governance posture:** `research_eligible: false`;
  `eligibility_gate_status: "pending"`;
  `governance_labels.feature_computation` posture (allowed-by-this-phase
  with `labels`/`ml`/`strategy`/`backtest`/`acquisition`
  forbidden/unauthorized); `no_successor_authorization: true`; the
  18-key boundary confirmations (all `True`, including
  `no_future_lookahead`,
  `phase_4aw_flip_research_eligible_invariant_preserved`) and the 8-flag
  non-authorization set (all `False`).
- **Sealed-test / terminal boundary witnesses:**
  `v002_terminal_window_mode: "by_reference"`;
  `existing_v002_terminal_window` (`read: false`,
  `normalized_dates_read: false`);
  `sealed_test_split_touched: false`;
  `test_holdout_touched: false`; `test_rows_loaded: 0`.
- **Partitioning / storage:** partitioning rule (`<SYMBOL>/<YYYY>/<MM>/`);
  primary key (`symbol, utc_date, agg_trade_id, row_index`); storage
  format (Parquet zstd); sidecar policy (canonical two-space `.sha256`);
  `invalid_windows`.
- **Budget witnesses (Phase 4bn-L):** measured feature footprint,
  temporary-workspace footprint, runtime, `D:` free space, and the cap
  thresholds honoured.

The optional **full-envelope feature reference manifest**, if later
written, must contain at minimum: `dataset_family`; `dataset_version =
"v002"`; `feature_schema_version = "v001"`; `reference_type:
"full_envelope_assembly"`; `full_intended_envelope_start/end`; the two
member references (segment manifest path + SHA256; published `__v002`
feature manifest path + SHA256, read-only); `research_eligible: false`;
`eligibility_gate_status: "pending"`; `v002_terminal_window_mode:
"by_reference"`; `sealed_test_split_touched: false`;
`no_successor_authorization: true`.

## 15. Future feature manifest forbidden fields

The future feature segment manifest (and the optional reference
manifest) **must not** contain any of:

- label outputs, label horizons, barrier/target/MFE/MAE/R-multiple
  fields, or any `label_*` / `target_*` field;
- future returns, forward-looking values, or any `future_*` field;
- model outputs, predictions, scores, or `model_*` / `score_*` /
  `prediction_*` fields;
- signal fields, entry/exit fields, or any `signal_*` field;
- PnL, equity, profit/loss, position, or backtest fields;
- strategy fields, alpha, or edge fields;
- diagnostic scores, statistics, or research-quality metrics;
- any field asserting or implying `research_eligible: true`,
  `eligibility_gate_status` other than `"pending"`, a
  `chronological_split_policy` value, `diagnostics_authorized: true`, or
  `ml_authorized: true`;
- any "research-ready" / "admissible-for-ML" / "approved-for-backtest"
  claim;
- any Stage-3 research-eligible successor-state reference presented as a
  required precondition for this segment;
- any `v003`, mark-price, funding, open-interest, order-book, spot,
  cross-venue, tick, or ETHUSDT field, and no extra-horizon field.

The locked forbidden-substring guard already enforced by the feature
kernel on **column names** (`label`, `target`, `future`, `signal`,
`pnl`, `strategy`, `prediction`, `model`, `score`, `decision`,
`backtest`, …) is preserved verbatim and extends in spirit to manifest
fields.

## 16. Future feature output directory convention

The future pre-v002 feature parquet output uses a **version-suffixed
segment directory distinct from the published `__v002/` feature
directory**:

```text
data/microstructure/features/microstructure_features_aggtrades_v001__v002_pre_v002_segment_<feature-phase-id>/BTCUSDT/<YYYY>/<MM>/BTCUSDT-features-aggtrades-<YYYY-MM-DD>.parquet
```

each with a paired canonical two-space `.sha256` sidecar.

- This is **not** the published
  `microstructure_features_aggtrades_v001__v002/` directory (which
  remains immutable); the future bounded wrapper must build a
  segment-suffixed `family_dir`, exactly as `features_io_v002` builds
  `V002_FEATURE_DIR_SEGMENT` for `__v002`.
- It is **not** a generic `microstructure_features_aggtrades_v001/`
  directory.
- It is **not** a new `__vNNN` directory.

Because feature directories are version-suffixed, the segment directory
keeps the pre-v002 feature parquets cleanly separate from the published
`__v002` feature parquets, so the published v002 feature family stays
immutable and the segment is self-describing. The existing
`assert_output_path_under_features` guard (path under
`data/microstructure/features/`) is satisfied by this layout.

## 17. Future feature execution implications

A future, separately-authorized **feature-only execution phase** must:

- build a **bounded new wrapper** reusing the locked feature primitives
  (`features_schema_v002`, `features_compute_v002`, `features_io_v002`,
  `features_manifest_v002`, `features_schema`) unchanged, and adding:
  the pre-v002 normalized **segment** source contract (§12); the §12
  non-eligible-source precondition (Phase 4bn-O segment manifest SHA +
  Phase 4bn-P gate report PASS, **not** a Stage-3 successor); a hard
  segment-date guard rejecting any date `>= 2024-12-01` and any date
  outside 2024-03-01 .. 2024-11-30; the §11/§16 segment naming; and the
  Phase 4bn-L preflight/budget caps;
- read **only** the approved 275 normalized segment dates, each verified
  by SHA256 against the Phase 4bn-O segment manifest and admitted by the
  Phase 4bn-P gate report; never open the published `__v002` normalized
  family; never read v002 terminal normalized dates; never read
  sealed-test dates;
- write **only** feature parquet + canonical sidecars under the §16
  segment directory, plus a single non-eligible feature segment manifest
  + sidecar under `data/microstructure/manifests/`; refuse to overwrite
  any finalised file; atomic write-then-rename;
- preserve the locked 62-column `FEATURE_SCHEMA_V002` (17 lineage + 45
  feature/quality) verbatim and the forbidden-substring column guard;
  preserve the strictly-causal kernel (backward-only 60 s cross-day
  tail; first segment day flags `rolling_missing_window_flag`);
- leave the published feature `__v002` directory and
  `microstructure_features_aggtrades_v001__v002.json` manifest
  **byte-for-byte unchanged** (read-only-by-reference at most);
- honour the Phase 4bn-L budget (feature layer 50 GiB warn / 100 GiB
  hard footprint, 4 h warn / 8 h hard runtime; temporary workspace 50
  GiB / 100 GiB; total derived-stack 250 GiB warn / 300 GiB hard; `D:`
  free ≥ 500 GiB before, fail closed below 350 GiB during) and **stop
  before writing** on any breach;
- leave all outputs non-eligible (`research_eligible: false`,
  `eligibility_gate_status: "pending"`, `no_successor_authorization:
  true`); commit no data artefact; create no labels, targets, future
  returns, ML outputs, diagnostics, research outputs, database, v003, or
  compacted Parquet;
- carry its own offline test module (segment naming, date guard,
  non-eligible-source precondition, causal/no-leakage, forbidden-column
  guard, manifest-writer field contract + forbidden-field absence,
  refuse-overwrite, budget-cap, no-network, no-sealed-read, non-eligible
  posture) mirroring the Phase 4bn-O / 4bn-P test precedents;
- preserve the Phase 4aw `flip_research_eligible(...)` always-raises
  invariant (never invoked).

A future feature phase must **fail closed** (stop, report partial
outputs, leave all outputs non-eligible and uncommitted) on any of:
missing/invalid Phase 4bn-O segment manifest or Phase 4bn-P gate report;
gate report not PASS; source segment not `research_eligible: false` /
`eligibility_gate_status: "pending"`; normalized per-day SHA256
mismatch; any date outside 2024-03-01 .. 2024-11-30; any attempt to read
the v002 terminal normalized window or sealed-test dates; any feature
requiring forward-looking information, future returns, labels, or
unavailable lookback; preflight cannot estimate footprint; feature
estimate > 100 GiB; total derived-stack > 300 GiB; `D:` free < 500 GiB
before or < 350 GiB during; temp workspace > 100 GiB; runtime > 8 h; any
output outside the §16 segment directory; any `data/research` output;
any label/ML/diagnostics/strategy/PnL/backtest; any database / Parquet
compaction / v003; any `research_eligible` flip or
`eligibility_gate_status` transition; any `data/microstructure` or
`data/research` commit; any forbidden manifest field.

## 18. Future feature-layer gate implications

A future, separately-authorized **feature-layer eligibility gate**
(design level only; **not** run here; analogous to the Phase 4bn-P
normalized-layer gate and the Phase 4bm-J feature gate, built as a
bounded read-only segment-wrapper rather than the window-hardcoded
`multiday_feature_gate*`) should validate, at minimum:

- the feature segment manifest exists, parses, and matches the §14
  required-field contract; the §15 forbidden fields are absent;
- every per-date feature parquet exists with a canonical sidecar;
  recomputed SHA256s match the segment manifest; recomputed aggregates
  (date count = 275, total feature rows, per-date row counts,
  contiguous in-segment dates, segment footprint) match;
- the schema is exactly the locked 62-column `FEATURE_SCHEMA_V002` (17
  lineage + 45 feature/quality) with the forbidden-substring column
  guard passing; the leakage / cross-day policies match;
- predecessor integrity: the Phase 4bn-O normalized segment manifest
  SHA256 (`0e96ae37…d9fa`) and the Phase 4bn-P gate report SHA256
  (`3452fd9d…f134`, PASS) still match; the per-day source normalized
  parquet SHA256s in `per_day_outputs` are consistent;
- the published `__v002` feature family was not mutated (by-reference);
  the v002 terminal normalized window and sealed-test split were not
  read;
- `research_eligible` remains `false` and `eligibility_gate_status`
  remains `"pending"` — **a passing feature-layer gate does NOT flip
  eligibility, does NOT authorize labels / ML / diagnostics / strategy,
  and does NOT authorize any successor.**

## 19. Sealed-test and v002 terminal boundary

- The new pre-v002 feature segment covers **2024-03-01 .. 2024-11-30**,
  which contains **no** sealed-test dates and **no** v002 terminal-window
  dates.
- The feature kernel is **strictly causal**
  (`causal_only_no_future_lookahead`), with cross-day lookback limited
  to a 60 s **backward** tail. Computing the segment's last day
  (2024-11-30) requires **no** forward read into the v002 terminal
  normalized window (2024-12-01 .. 2025-02-28); computing the first day
  (2024-03-01) requires **no** read before the segment (early rows
  flagged `rolling_missing_window_flag`). All cross-day tail reads stay
  **inside** 2024-03-01 .. 2024-11-30.
- The existing v002 terminal **normalized** window is treated **by
  reference only** (`v002_terminal_window_mode: "by_reference"`); it is
  not read by any convention in this memo. The published feature
  `__v002` family is likewise by reference only and immutable.
- The sealed v002 test split **2025-02-14 .. 2025-02-28** remains
  **untouched** (`sealed_test_split_touched: false`,
  `test_holdout_touched: false`, `test_rows_loaded: 0`). Sealing is
  enforced at the ML/split layer (`iter_partitions(split="test", ...)`
  always raises), independent of feature scope.
- Because the conservative pre-v002-only feature scope reads neither the
  v002 terminal normalized window nor sealed-test dates, **a
  holdout-boundary memo is NOT required** to proceed. It becomes
  required **only if** a future feature phase proposes to read the v002
  terminal normalized window or sealed-test dates (e.g. to build a
  single rewritten full-envelope feature family or to provide forward
  context) — which this memo explicitly does not.

## 20. Decision

**Result state:**
`RECORD_FEATURE_MANIFEST_VERSIONING_CONVENTION__REMAIN_PAUSED`.

**Decision:**
`RECOMMEND_AUTHORIZE_FEATURE_ONLY_EXECUTION__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Rationale (repository-evidence-grounded): the predeclared preferred
decision when the memo **successfully resolves feature
manifest/versioning and the non-eligible-source precondition without
requiring v003 or v002 terminal/sealed-test reads** is exactly this
option. This memo resolves the convention cleanly by mirroring the
already-merged raw-layer and normalized-layer segment precedents: a
phase-scoped feature segment manifest + version-suffixed segment
directory marked `pre_v002_segment` under `dataset_version: "v002"`,
`feature_schema_version: "v001"` (§11/§16); a non-eligible-source
precondition built on the Phase 4bn-O segment manifest + Phase 4bn-P
normalized-layer gate PASS, replacing the Stage-3 research-eligible
successor-state precondition (§12); the full 12-month feature envelope
represented by reference (segment-manifest fields now; optional deferred
full-envelope feature reference manifest later) (§13). The resolution
requires **no v003**, **no mutation of any published `__v002` feature
manifest or directory**, **no read or rewrite of the v002 terminal
feature family**, **no read of v002 terminal normalized dates**, **no
sealed-test read**, and **no eligibility flip**. Phase 4bn-Q already
established that the feature **primitives** are safe and reusable
(needing only bounded new wrappers for the orchestrator and gate) and
that the sealed-test / v002 terminal boundary is clear for the
conservative causal-only pre-v002 scope (so a holdout-boundary memo is
**not** required). With manifest/versioning and the non-eligible-source
precondition now settled, the cleanest next technical step is a
separately-authorized feature-only execution phase honouring §14–§18 and
the Phase 4bn-L budget — exactly mirroring the normalization arc
(readiness 4bn-M → manifest/versioning memo 4bn-N → execution 4bn-O →
gate 4bn-P).

The full set of admissible Phase 4bn-R decision options was:
`RECORD_FEATURE_MANIFEST_VERSIONING_CONVENTION__REMAIN_PAUSED`;
`RECOMMEND_AUTHORIZE_FEATURE_ONLY_EXECUTION__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
(selected);
`RECOMMEND_AUTHORIZE_DOCS_ONLY_HOLDOUT_BOUNDARY_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
`RECOMMEND_AUTHORIZE_SOURCE_POLICY_DOCUMENTATION_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
`RECOMMEND_AUTHORIZE_PROCESS_DOC_PATH_UPDATE__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
`RECOMMEND_CLOSE_ML_BASELINE_ARC__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

This memo **does not authorize** the successor; the operator decides
separately. **No successor is authorized from inside Phase 4bn-R.**

## 21. Recommended state and successor options

**Recommended state: remain paused.** Phase 4bn-R is **branch-complete
only**; not merged into `main`; not project-complete until a separately
authorized merge phase records its merge-closeout on `main` per
`merge-closeout-standard.md` (Tier 1).

**Operator options (each subject to separate operator authorization;
none authorized here):**

- remain paused (default);
- request a merge prompt for Phase 4bn-R;
- separately authorize a **feature-only execution phase** (this memo's
  recommendation) — a bounded new wrapper over the Phase 4bn-O pre-v002
  normalized segment honouring §11–§18 and the Phase 4bn-L budget,
  followed (only if separately authorized) by a bounded feature-layer
  eligibility gate;
- separately authorize a **docs-only holdout-boundary memo** — **not
  required** for the conservative pre-v002-only feature scope; only
  relevant if a future feature phase intends to read the v002 terminal
  normalized window or sealed-test dates;
- separately authorize a **source-policy documentation memo**;
- separately authorize a **process-doc `D:` path-string update** (the
  Phase 4bm-D-P1 lightweight-workspace standard still carries old `C:`
  example paths);
- reject further ML-baseline successors and **close the ML-baseline
  arc**.

**Required successor validation/gate phases after any future feature
execution (predeclared, none authorized):** a bounded **feature-layer
eligibility gate** (§18) before any downstream stage; then, only if
separately authorized, label derivation + label gate; a
chronological-split / holdout policy memo before any ML or diagnostics.

## 22. Explicit non-authorizations

Phase 4bn-R did **not** and does **not** authorize: feature derivation;
feature artefact generation; feature manifest creation or mutation;
feature gate execution; label derivation; normalization rerun; raw
acquisition; any endpoint / public / Binance / `data.binance.vision`
call; archive or CHECKSUM download; HEAD preflight; raw-gate or
normalized-layer-gate rerun; any local raw / normalized Parquet /
feature / label read; any v002 terminal raw or normalized window read;
any sealed-test read; any local `data/research` or `data/microstructure`
artefact / manifest / gate-report read or creation; diagnostics; ML
training; model scoring; predictions; feature ranking / selection /
pruning / engineering; hyperparameter or threshold tuning; calibration
fitting; strategy research; signal generation; PnL simulation;
backtests; manifest mutation; successor-state mutation; gate-report
mutation; `research_eligible` flip; `eligibility_gate_status`
transition; `chronological_split_policy` transition;
`diagnostics_authorized` or `ml_authorized` transition; `data/research`
or `data/microstructure` artefact creation or commit; storage
migration; DuckDB / SQLite / `.duckdb` / `.sqlite` / database creation;
Parquet compaction; v003 creation; ETHUSDT; extra horizons; mark-price;
spot; cross-venue; order book; tick data; paper / shadow; live-readiness;
deployment; exchange-write; production keys; any Phase 5; or any
successor phase.

Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m
thread / V2 / G1 / C1) and every project lock (§11.6 = 8 bps per side;
round-trip = 16 bps; §1.7.3; Phase 3p §4.7; Phase 3r §8; Phase 3v §8;
Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q;
Phase 4v; Phase 4w; Phase 4ak M0; Phase 4al refined no-rescue rule;
Phase 4aw `flip_research_eligible(...)` always-raises invariant (never
invoked); Phase 4bb-F canonical path + sidecar policy; the Phase
4bn-J-R1 raw-only cap amendment; the Phase 4bn-L derived-stack storage
budget; the Phase 4bn-N normalization manifest/versioning convention) is
preserved verbatim. Phase 4 canonical remains unauthorized.

## 23. Current-project-state update summary

`docs/00-meta/current-project-state.md` was updated narrowly: a new
Phase 4bn-R prose paragraph was appended after the Phase 4bn-Q
paragraph, and a new `Current phase:` block for Phase 4bn-R was inserted
ahead of the Phase 4bn-Q block. All prior Phase 4bn-A … 4bn-Q paragraphs
and `Current phase:` blocks are preserved verbatim as labelled
historical context. No other section of `current-project-state.md` was
changed. No code, test, script, data file, configuration, `.gitignore`,
`README.md`, MCP file, manifest, sidecar, gate report, or
successor-state artefact was created or modified. No local data was
read; no local data was created.
