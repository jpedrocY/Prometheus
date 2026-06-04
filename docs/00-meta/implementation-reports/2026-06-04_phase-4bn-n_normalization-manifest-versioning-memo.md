# Phase 4bn-N — Normalization Manifest / Versioning Memo

## 1. Purpose

This memo is a **docs-only normalization-manifest / dataset-versioning /
boundary-contract** deliverable. It resolves, from committed repository
documentation and committed tooling only, the **manifest/versioning
ambiguity** that Phase 4bn-M identified as the single binding obstacle to
authorizing a future normalization-only execution phase over the expanded
12-month BTCUSDT Binance USDⓈ-M futures aggTrades envelope.

This phase **runs no normalization**, **creates no normalized artefacts**,
and **creates or mutates no manifest**. It records, at design level only, the
exact manifest/versioning shape a future pre-v002 normalized aggTrades
segment must use, how that segment links to the existing terminal normalized
`__v002` family, and how the eventual full 12-month normalized envelope is
identified **without creating v003, mutating any published `__v002`
manifest, re-reading or re-normalizing the v002 terminal raw window, touching
the sealed test split, or flipping eligibility.**

This memo answers exactly the question Phase 4bn-M deferred:

> What exact manifest/versioning shape should a future pre-v002 normalized
> aggTrades segment use, how should it link to the existing normalized
> `__v002` terminal family, and how should the eventual 12-month normalized
> envelope be identified without creating v003, mutating published v002
> manifests, or flipping research eligibility?

It does **not** ask whether the project can start ML, create labels, run the
model, find edge, backtest, trade, use the sealed test split, or make the
dataset research-eligible.

## 2. Authority and repository state

- **Active local repo path:** `D:\Prometheus`.
- **Active Claude Code lightweight workspace:** `D:\ClaudeRuns\prometheus-light`.
- **GitHub remote:** `origin` → `https://github.com/jpedrocY/Prometheus.git`
  (verified intact).
- **Branch:** `phase-4bn-n/normalization-manifest-versioning-memo`.
- **Base `main` SHA:** `6d41c2e069ce688fa08b36473fe4449e008bdb18`
  (`docs(phase-4bn-m): finalize merge closeout shas`). Pre-branch
  `main == origin/main == HEAD` was verified in sync. The Phase 4bn-M
  SHA-finalization commit `6d41c2e`, merge-closeout `6d8f9d3`, merge
  `3dad0cb`, and branch commit `844bc5f` are all present on `main`; the
  Phase 4bn-L SHA-finalization commit `b7767a6` is present as predecessor.
- **Tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3. This phase
  settles the manifest/versioning convention adjacent to future normalized
  artefact generation over the expanded 12-month envelope, future normalized
  eligibility gates, future feature derivation, future label derivation,
  future holdout/split policy, future ML-baseline admissibility, and local
  disk/runtime budgets — while explicitly authorizing no normalization, no
  features, no labels, no ML, no diagnostics, and no downstream use.
- **Working-tree expectation:** only the untracked transient
  `.claude/scheduled_tasks.lock`; the gitignored namespaces
  `data/microstructure/` (`.gitignore:85`) and `data/research/`
  (`.gitignore:88`) exist locally and remain uncommitted.

## 3. Phase type and strict scope

**Phase type:** docs-only / normalization-manifest / dataset-versioning /
boundary-contract.

**Allowed work performed by this phase:**

- read committed Markdown docs;
- inspect committed source, scripts, and tests read-only;
- identify the existing normalized manifest construction and validation
  conventions;
- compare the existing normalized `__v001` / `__v002` conventions to the
  pre-v002 segment problem;
- define a future pre-v002 normalized segment manifest naming convention;
- define a future normalized output directory naming convention;
- define predecessor linkage to the raw segment manifest, the raw gate
  report, and the existing normalized `__v002` family;
- define how the eventual 12-month normalized envelope is represented by
  manifest/reference;
- define what future normalization execution must write and must not mutate;
- define required offline tests for the future bounded runner / manifest
  writer;
- create the two tracked Phase 4bn-N docs and update
  `current-project-state.md` narrowly.

**This phase did NOT and must NOT (within Phase 4bn-N):** run normalization;
create normalized artefacts; create or mutate any manifest; derive features;
derive labels; run ML; run diagnostics; run strategy / signals / PnL /
backtests; acquire data; call any endpoint; inspect any local raw zip
contents; read any local `data/microstructure` or `data/research` artefact,
manifest, or gate report; touch the v002 terminal window; touch the sealed
test split; create a database; compact Parquet; create v003; or authorize any
successor.

## 4. Evidence base and input boundary

**Inputs read (committed repository evidence only):**

- `docs/00-meta/current-project-state.md` (Phase 4bn-M / 4bn-L / 4bn-K /
  4bn-J-R2 paragraphs and `Current phase:` blocks);
- the process standards `merge-closeout-standard.md`,
  `phase-risk-tiering-standard.md`, `phase-workflow-standard.md`,
  `phase-prompt-template.md`, `operator-report-standard.md`;
- the Phase 4bn-M normalization-readiness/execution-plan memo, merge-closeout,
  and closeout; the Phase 4bn-L derived-stack storage-budget memo and
  closeout; the Phase 4bn-K raw archive eligibility-gate report narrative,
  merge-closeout, and closeout; the Phase 4bn-J-R2 acquisition narrative,
  merge-closeout, and closeout;
- the data specs `data-requirements.md`, `historical-data-spec.md`,
  `timestamp-policy.md`, `dataset-versioning.md`, and `database-design.md`;
- committed tooling read-only:
  `src/prometheus/research/microstructure/normalize_manifest.py`,
  `normalize_io.py`, `normalize_validation.py`, `canonical_paths.py`,
  `derived_gate*` / `multiday_derived_gate*`;
  `scripts/phase4bm_b_normalize_multiday_aggtrades.py`,
  `scripts/phase4bn_j_r2_acquire_btcusdt_aggtrades_pre_v002.py`,
  `scripts/phase4bn_k_validate_pre_v002_raw_archive_gate.py`;
  and the committed offline test surface under
  `tests/research/microstructure/`
  (`test_normalize_manifest.py`, `test_normalize_io.py`,
  `test_normalize_validation.py`,
  `test_phase4bm_b_multiday_normalization.py`,
  `test_phase4bn_j_r2_acquisition_script.py`).

**Inputs explicitly NOT used:** any local raw zip contents; the existing
v002 terminal raw window; the sealed v002 test split; any local
`data/microstructure` normalized / feature / label / manifest / gate-report
/ successor-state artefact; any local `data/research` artefact; no hashing,
counting, or inspection of local gitignored data; no endpoints; no
credentials; no `.env`; no `.mcp.json`; no MCP; no Graphify. **README was
treated as potentially stale and was not used as current-state authority.**
SHA256 digests cited for local gitignored artefacts (segment manifest, gate
report, acquisition log) are quoted **from committed Markdown evidence**
(prior closeouts / current-project-state), not by reading the local files.

## 5. Phase 4bn-M finding carried forward

Phase 4bn-M concluded — and merged onto `main` — that:

1. **Normalization tooling primitives are SAFE and directly reusable**
   (`normalize_aggtrades.py` 19-column `NORMALIZED_SCHEMA_V001` +
   `iter_aggtrade_rows_from_csv`; `normalize_io.py` path discipline + atomic
   zstd Parquet + canonical two-space `.sha256` sidecars + refuse-overwrite;
   network-free, credential-free; offline test suite present).
2. **The existing runner
   `scripts/phase4bm_b_normalize_multiday_aggtrades.py` is NOT directly
   reusable and needs a bounded new wrapper** — it is hardcoded to the 90-day
   v002 window (`EXPECTED_DATE_COUNT = 90`, 2024-12-01 .. 2025-02-28,
   `EXPECTED_TOTAL_EVENT_COUNT = 155,153,449`) with locked precondition SHAs
   for the **published v002 raw manifest**, enforces a v002 identity
   cross-check, and has no Phase 4bn-L preflight/budget caps.
3. **Manifest/versioning is AMBIGUOUS and requires this memo** — the pre-v002
   raw segment used a phase-scoped segment manifest while
   `dataset-versioning.md` codifies only monotonic `__vNNN` + predecessor
   linkage and does not settle the normalized segment-manifest /
   predecessor-linked-extension / full-envelope identity; v003 is forbidden.
4. **The sealed-test / v002 terminal boundary is CLEAR for the conservative
   pre-v002-only scope** — the new pre-v002 segment 2024-03-01 .. 2024-11-30
   contains no sealed-test dates; the v002 terminal window 2024-12-01 ..
   2025-02-28 is already normalized as the `__v002` family; a separate
   holdout-boundary memo is required only if a future phase proposes to read
   the v002 terminal raw window.

Phase 4bn-M's decision was
`RECOMMEND_AUTHORIZE_DOCS_ONLY_NORMALIZATION_MANIFEST_VERSIONING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
This phase executes exactly that recommended memo. **Finding (3) is the sole
ambiguity this memo resolves; findings (1), (2), and (4) are carried forward
unchanged.**

## 6. Dataset-versioning rules carried forward

`docs/04-data/dataset-versioning.md` binds the following for normalized
datasets:

- **Version identity** is required; the recommended identifier pattern is
  `<dataset_name>__vNNN`, **monotonic per family**, **never reused or
  overwritten**.
- **Every versioned dataset has a manifest** at the dataset-version root,
  with **minimum fields** including dataset name, version ID, category,
  creation timestamp, canonical timezone/format, symbol set, schema version,
  transformation/pipeline version, partitioning rules, primary key, generator
  identity, notes, and **predecessor version if applicable**.
- **Published versions are immutable**: files, schema, and manifest must not
  be silently modified; corrections create a **new version** that records its
  **predecessor**.
- **Publication states** are `draft` / `published` / `deprecated` /
  `superseded`; only `published` versions are used for formal research.
- **Partition folders do not replace version identity** — directory layout is
  a storage concern, version identity is a governance concern.

The doc does **not** codify "segment manifests," predecessor-linked backward
extensions, or how a backward segment relates to an already-published
terminal version. The raw layer resolved that gap by precedent (see §8); this
memo resolves it for the normalized layer by the same precedent (see §10).

## 7. Existing normalized `__v001` / `__v002` conventions

From committed code (`normalize_io.py`, `normalize_manifest.py`,
`scripts/phase4bm_b_normalize_multiday_aggtrades.py`):

- **Dataset family (schema-lineage marker):**
  `microstructure_normalized_aggtrades_v001`. The trailing `v001` here is part
  of the **family name** (the locked Phase 4bd 19-column
  `NORMALIZED_SCHEMA_V001` lineage), **not** a window discriminator.
- **Dataset version (window/source discriminator):** the second suffix.
  `__v001` = the single-day Phase 4bd normalized output; `__v002` = the
  90-day multi-day Phase 4bm-B output covering **2024-12-01 .. 2025-02-28**.
  Schema is byte-identical across both (`schema_version: "v001"`).
- **Normalized partition directory:**
  `data/microstructure/normalized/microstructure_normalized_aggtrades_v001__<version>/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-aggTrades-<YYYY-MM-DD>.parquet`,
  each with a paired canonical `.sha256` sidecar. The Phase 4bm-B runner
  builds `family_dir = f"{NORMALIZED_DATASET_FAMILY}__{NORMALIZED_DATASET_VERSION}"`,
  i.e. the normalized **directory is version-suffixed** so v002 coexists with
  the v001 single-day Parquet.
- **Normalized index manifest:**
  `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__<version>.json`
  with a paired `.sha256` sidecar. The Phase 4bm-B multi-day index manifest is
  a **sibling-shape JSON** (mirroring the raw multi-day manifest), not the
  single-file `MicrostructureManifest` dataclass. It is seeded
  `research_eligible: false`, `eligibility_gate_status: "pending"`, with
  `governance_labels.feature_computation: "forbidden"` and
  `governance_labels.strategy_use: "forbidden"`, plus lineage to the source
  raw manifest, gate report, successor-state, and a
  `phase_4bm_b_no_successor_authorization: "true"` label.

**Key asymmetry vs the raw layer:** raw daily zips for **all** windows live in
one shared, non-version-suffixed tree
(`microstructure_raw_aggtrades_v001/<SYMBOL>/...`), so a backward raw segment
simply adds new dates into the same tree. Normalized **directories are
version-suffixed**, so a backward normalized segment cannot be written into
the published `__v002/` directory without extending — and thereby blurring —
the published, immutable `__v002` family. This asymmetry drives the §10
directory choice.

## 8. Manifest/versioning ambiguity being resolved

The pre-v002 **raw** segment was acquired (Phase 4bn-J-R2) and gate-passed
(Phase 4bn-K) as a **phase-scoped segment manifest** rather than a new
`__vNNN`:

- **Filename:**
  `microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2.json`
  (SHA256 `1659e6da9ccc1c4a49c2f497e1f4a70f8082cac24142c77ac6d5217197b3a3d1`,
  per committed evidence).
- Inside the manifest, `dataset_family = microstructure_raw_aggtrades_v001`,
  `dataset_version = "v002"`, `version = "v002"`, plus a distinguishing
  `segment_label = "pre_v002_segment"` field. **The window discriminator
  (`pre_v002_segment_4bn_j_r2`) lives in the filename, not in
  `dataset_version`.** The segment is a **backward extension of the v002
  envelope**, schema-identical, **not** a new monotonic version.
- The manifest records the full intended envelope by reference
  (`full_intended_envelope_start = 2024-03-01`,
  `full_intended_envelope_end = 2025-02-28`), and by-reference blocks
  `existing_v002_terminal_window` (`read: false`, `overwritten: false`,
  `redownloaded: false`) and `existing_v002_sealed_test_split`
  (`touched: false`), with `research_eligible: false`,
  `eligibility_gate_status: "pending"`, `test_holdout_touched: false`,
  `test_rows_loaded: 0`, and a `non_authorizations` block including
  `v003_creation: "forbidden"` and `v002_terminal_window_read: "forbidden"`.

**The ambiguity:** the normalized layer has no codified rule for whether the
pre-v002 normalized output should be (a) a segment manifest mirroring this raw
precedent, (b) a predecessor-linked extension of `__v002`, or (c) a new
full-envelope version — and `dataset-versioning.md` is silent on backward
segments. Candidate (c) collides with the forbidden v003 boundary and the
monotonic-immutability rule and is rejected outright. This memo selects
between (a) and (b) and defines how the full envelope is identified.

## 9. Candidate shapes considered

1. **Phase-scoped normalized segment manifest (raw-precedent mirror).**
   A sibling-shape JSON
   `microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_<phase-id>.json`
   with `dataset_version: "v002"`, `segment_label: "pre_v002_segment"`, its
   own version-suffixed segment directory, full-envelope-by-reference fields,
   and by-reference v002-terminal / sealed-split blocks. **Pros:** exact
   structural and governance parity with the already-merged raw segment and
   gate precedent; reuses the locked primitives unchanged; leaves the
   published `__v002` family byte-for-byte immutable; no v003; no v002
   terminal raw read. **Cons:** introduces a longer directory/manifest name
   than `__vNNN`.

2. **Predecessor-linked extension of `__v002` (write into the v002 family).**
   Write pre-v002 dates under the existing `microstructure_normalized_aggtrades_v001__v002/`
   directory and link via a `predecessor`/`extends` field. **Pros:** single
   directory for the whole v002 envelope. **Cons:** writes new files into the
   **published, immutable** `__v002` directory, creating parquets the
   published `__v002.json` index manifest does not reference (the manifest is
   refuse-overwrite-protected), i.e. orphaned-within-the-family artefacts;
   blurs the "published version is immutable" boundary; **rejected.**

3. **New full-envelope version (`__v003` or a single rewritten envelope).**
   **Cons:** directly collides with the forbidden v003 boundary and the
   monotonic-immutability rule; would require re-reading / re-normalizing the
   v002 terminal raw window (including sealed-test dates) to produce a single
   envelope; **rejected outright.**

4. **No manifest (rely on the directory only).** **Cons:** violates
   `dataset-versioning.md` Rule 2 ("never run formal validation on an
   untracked dataset version") and the "partition folders do not replace
   version identity" rule; **rejected.**

## 10. Selected normalization segment convention

**Selected: Candidate (1) — a phase-scoped normalized segment manifest,
mirroring the merged raw-layer precedent.**

The future pre-v002 normalized output is represented as a **phase-scoped
normalized segment manifest** — a sibling-shape JSON that is **clearly tied
to the existing v002 normalized family but clearly marked as a pre-v002
backward segment / extension**, not a new monotonic version.

- **Manifest filename (under `data/microstructure/manifests/`):**

  ```text
  microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_<normalization-phase-id>.json
  ```

  with a paired canonical two-space `.sha256` sidecar.
  `<normalization-phase-id>` is the underscored phase id of the future
  separately-authorized normalization-execution phase (e.g. if that phase is
  `4bn-O`, the token is `4bn_o`, yielding
  `microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json`).
  This exactly parallels the raw segment's
  `microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2.json`.

- **Inner identity fields:** `dataset_family =
  "microstructure_normalized_aggtrades_v001"` (reused, schema-identical);
  `dataset_version = "v002"` and `version = "v002"` (a **backward segment of
  the v002 envelope**, not a new version); `schema_version = "v001"`;
  `segment_label = "pre_v002_segment"`. The window discriminator lives in the
  **filename and directory name**, never as a new `dataset_version`.

This selection: (i) reuses the locked normalization primitives unchanged;
(ii) leaves the published normalized `__v002` family — directory, parquets,
sidecars, and `microstructure_normalized_aggtrades_v001__v002.json` manifest —
**byte-for-byte immutable**; (iii) creates **no** v003; (iv) reads **no**
v002 terminal raw window and **no** sealed-test dates; (v) keeps every output
non-eligible and pending.

## 11. Selected full-envelope reference convention

The eventual full 12-month normalized envelope (2024-03-01 .. 2025-02-28) is
identified **by reference, never by rewriting existing v002 artefacts.**

**Primary (required of the future normalization-execution phase):** the
pre-v002 normalized **segment manifest** itself carries the envelope by
reference, mirroring the raw precedent:

- `full_intended_envelope_start = "2024-03-01"`,
  `full_intended_envelope_end = "2025-02-28"`;
- an `existing_v002_normalized_reference` block recording the published
  normalized `__v002` family by reference — the manifest path
  `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json`,
  its window (2024-12-01 .. 2025-02-28), and flags
  `read: false` / `mutated: false` (a read-only SHA256 capture of that
  published manifest **for integrity recording only** is permitted at
  execution time but is **never** a mutation and is **never** required by
  this memo);
- by-reference `existing_v002_terminal_window`
  (`read: false`, `overwritten: false`, `redownloaded: false`,
  `re_normalized: false`) and `existing_v002_sealed_test_split`
  (`touched: false`) blocks, identical in spirit to the raw segment manifest.

**Companion (defined, deferred, optional):** a separate **full-envelope
reference / assembly manifest**

```text
microstructure_normalized_aggtrades_v001__v002_full_envelope_reference_<phase-id>.json
```

may later be written — by the normalization-execution phase **or** by the
normalized-layer gate — **only if** a single 12-month handle is needed
downstream. It is a **thin, non-eligible, by-reference index** that names
exactly two halves: the pre-v002 normalized segment manifest (path + SHA256)
and the published normalized `__v002` manifest (path + SHA256, read-only).
It **must not** re-read or re-normalize the v002 terminal raw window, **must
not** mutate `__v002.json`, **must not** create v003, and **must not** flip
eligibility. **This memo neither creates nor requires the companion manifest;
it only defines its shape so a future phase can produce it cleanly.**

Answer to "segment manifest only / separate reference manifest / both /
neither": **both, sequenced** — the segment manifest is mandatory at
execution; the full-envelope reference manifest is a defined-but-deferred
optional companion.

## 12. Future manifest required fields

The future pre-v002 normalized **segment manifest** must contain at least:

- **Identity / family:** `dataset_family =
  "microstructure_normalized_aggtrades_v001"`; `dataset_version = "v002"`;
  `version = "v002"`; `schema_version = "v001"`;
  `segment_label = "pre_v002_segment"`; `data_family = "aggTrades"`;
  `symbol_list = ["BTCUSDT"]`; `market = "usdm_futures"` (Binance USDⓈ-M
  futures); `dataset_category = "normalized"`.
- **Segment / phase:** `phase` / `phase_id` (the normalization-execution
  phase id); `source_phase_boundary`; `created_at_unix_ms`;
  `created_at_utc`; `code_commit_sha`; `base_commit_sha`;
  `capture_config_hash`.
- **Window / inventory:** `date_start = "2024-03-01"`,
  `date_end = "2024-11-30"`, `date_count` (e.g. 275), `date_list`,
  `expected_file_count`, `produced_file_count`, `total_event_count` /
  `total_row_count`, `per_file_inventory` (per-date parquet path, sidecar
  path, parquet SHA256, sidecar SHA256, parquet size bytes, event count,
  first/last `transact_time_ms`, min/max `agg_trade_id`, source zip SHA256,
  source zip path, status), and the total normalized footprint in bytes.
- **Input lineage (predecessor linkage — see §13/§14 for the rules):**
  `source_dataset_family = "microstructure_raw_aggtrades_v001"`;
  `source_dataset_version = "v002"`; the **input raw segment manifest** path
  (`…__v002_pre_v002_segment_4bn_j_r2.json`) and its **SHA256**
  (`1659e6da…3a3d1`); the **input raw gate report** path / `report_id` and
  its **SHA256** (`051bed7b…20f9c24`); the raw acquisition-log path and
  SHA256 (`0266210f…88bcf93`).
- **Existing-normalized linkage (by reference):**
  `existing_v002_normalized_reference` (published `__v002` manifest path,
  window, `read: false`, `mutated: false`).
- **Full-envelope-by-reference:** `full_intended_envelope_start =
  "2024-03-01"`, `full_intended_envelope_end = "2025-02-28"`.
- **Eligibility / governance posture:** `research_eligible: false`;
  `eligibility_gate_status: "pending"`;
  `governance_labels.feature_computation: "forbidden"`;
  `governance_labels.strategy_use: "forbidden"`;
  `governance_labels.normalization` lineage / validator labels;
  `no_successor_authorization: true`.
- **Sealed-test / terminal boundary witnesses:**
  `v002_terminal_window_mode: "by_reference"`;
  `existing_v002_terminal_window` (`read: false`, `overwritten: false`,
  `redownloaded: false`, `re_normalized: false`);
  `sealed_test_split_touched: false`;
  `existing_v002_sealed_test_split` (`touched: false`);
  `test_holdout_touched: false`; `test_rows_loaded: 0`.
- **Partitioning / storage:** partitioning rule (`<SYMBOL>/<YYYY>/<MM>/`);
  primary key (`symbol, utc_date, agg_trade_id`); storage format (Parquet
  zstd); sidecar policy (canonical two-space `.sha256`); `invalid_windows`.
- **Budget witnesses (Phase 4bn-L):** measured normalized footprint,
  temporary-workspace footprint, runtime, and the cap thresholds honoured.

The optional **full-envelope reference manifest**, if later written, must
contain at minimum: `dataset_family`; `dataset_version = "v002"`;
`reference_type: "full_envelope_assembly"`;
`full_intended_envelope_start/end`; the two member references (segment
manifest path + SHA256; published `__v002` manifest path + SHA256, read-only);
`research_eligible: false`; `eligibility_gate_status: "pending"`;
`v002_terminal_window_mode: "by_reference"`; `sealed_test_split_touched:
false`; `no_successor_authorization: true`.

## 13. Future manifest forbidden fields

The future normalized segment manifest (and the optional reference manifest)
**must not** contain any of:

- model outputs, predictions, scores, or `model_*` fields;
- label outputs, label horizons, barrier/target/MFE/MAE/R-multiple fields, or
  any `label_*` / `target_*` field;
- future returns, forward-looking values, or any `future_*` field;
- signal fields, entry/exit fields, or any `signal_*` field;
- PnL, equity, profit/loss, position, or backtest fields;
- strategy fields, alpha, or edge fields;
- diagnostic scores, statistics, or research-quality metrics;
- any field asserting or implying `research_eligible: true`,
  `eligibility_gate_status` other than `"pending"`, a
  `chronological_split_policy` value, `diagnostics_authorized: true`, or
  `ml_authorized: true`;
- any "research-ready" / "admissible-for-ML" / "approved-for-backtest" claim;
- any `v003`, mark-price, funding, open-interest, order-book, spot,
  cross-venue, tick, or ETHUSDT field.

The locked forbidden-substring guard already enforced by the normalizer on
**column names** (`label`, `target`, `future`, `signal`, `pnl`, `mark_price`,
`funding`, `open_interest`, `order_book`, `strategy`, `prediction`, `model`,
`score`, …) is preserved verbatim and extends in spirit to manifest fields.

## 14. Future normalized output directory convention

The future pre-v002 normalized parquet output uses a **version-suffixed
segment directory distinct from the published `__v002/` directory**:

```text
data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_<normalization-phase-id>/BTCUSDT/<YYYY>/<MM>/BTCUSDT-aggTrades-<YYYY-MM-DD>.parquet
```

each with a paired canonical two-space `.sha256` sidecar.

- This is **not** the generic `microstructure_normalized_aggtrades_v001/`
  directory emitted by the library helper `derive_normalized_output_path`
  (which has no version suffix); the future bounded runner must build a
  segment-suffixed `family_dir`, exactly as Phase 4bm-B built
  `f"{NORMALIZED_DATASET_FAMILY}__{NORMALIZED_DATASET_VERSION}"` for `__v002`.
- It is **not** a new `__vNNN` directory.
- It is **not** the published `__v002/` directory (which remains immutable).

Because normalized directories are version-suffixed (unlike the shared raw
zip tree), the segment directory keeps the pre-v002 normalized parquets
cleanly separate from the published `__v002` parquets, so the published v002
family stays immutable and the segment is self-describing. The existing
`assert_output_path_under_normalized` guard (path under
`data/microstructure/normalized/`) is satisfied by this layout.

## 15. Future normalization execution implications

A future, separately-authorized **normalization-only execution phase** must:

- build a **bounded new runner** reusing the locked primitives
  (`normalize_aggtrades`, `normalize_io`) unchanged, and adding: the pre-v002
  segment manifest as input source; a hard segment-date guard rejecting any
  date `>= 2024-12-01` and any date outside 2024-03-01 .. 2024-11-30; the
  Phase 4bn-L preflight/budget caps; and the §10/§14 segment naming;
- read **only** the approved pre-v002 raw inputs, verified by SHA256 against
  the Phase 4bn-J-R2 segment manifest and admitted by the Phase 4bn-K gate
  report; never open the v002 terminal raw window; never read sealed-test
  raw dates;
- write **only** normalized aggTrades parquet + canonical sidecars under the
  §14 segment directory, plus the §10 segment manifest + sidecar under
  `data/microstructure/manifests/`; refuse to overwrite any finalised file;
  atomic write-then-rename;
- preserve the locked 19-column `NORMALIZED_SCHEMA_V001` verbatim and the
  forbidden-substring column guard;
- leave the published normalized `__v002` directory and
  `microstructure_normalized_aggtrades_v001__v002.json` manifest **byte-for-
  byte unchanged** (read-only-by-reference at most);
- honour the Phase 4bn-L budget (normalized 100 GiB warn / 150 GiB hard, 4 h /
  8 h; temporary workspace 50 GiB / 100 GiB; total derived-stack 250 GiB warn
  / 300 GiB hard; `D:` free ≥ 500 GiB before, fail closed below 350 GiB
  during) and **stop before writing** on any breach;
- leave all outputs non-eligible (`research_eligible: false`,
  `eligibility_gate_status: "pending"`); commit no data artefact; create no
  database, no v003, no compacted Parquet, no features, no labels, no
  research outputs;
- carry its own offline test module (manifest-writer field contract, segment
  naming, date-guard, refuse-overwrite, budget-cap, no-network, no-sealed-read)
  mirroring the Phase 4bn-J-R2 / 4bn-K / 4bm-B test precedents;
- preserve the Phase 4aw `flip_research_eligible(...)` always-raises invariant
  (never invoked).

## 16. Future normalized-layer gate implications

A future, separately-authorized **normalized-layer eligibility gate** (design
level only; **not** run here; analogous to the Phase 4bn-K raw gate and
reusing the committed `derived_gate*` / `multiday_derived_gate*` modules plus
the normalizer's inline strict-fail-closed contract) should validate, at
minimum:

- the segment manifest exists, parses, and matches the §12 required-field
  contract; the §13 forbidden fields are absent;
- every per-date parquet exists with a canonical sidecar; recomputed SHA256s
  match the segment manifest; recomputed aggregates (date count, row count,
  per-date first/last `transact_time_ms`, min/max `agg_trade_id`,
  adjacent-date non-overlap) match;
- the input raw segment manifest SHA256 (`1659e6da…`) and raw gate report
  SHA256 (`051bed7b…`) still match (predecessor integrity);
- the published `__v002` normalized family was not mutated (by-reference);
  the v002 terminal raw window and sealed-test split were not read;
- the schema is exactly `NORMALIZED_SCHEMA_V001` (19 columns) with the
  forbidden-substring guard passing;
- `research_eligible` remains `false` and `eligibility_gate_status` remains
  `"pending"` — **a passing normalized-layer gate does NOT flip eligibility,
  does NOT authorize features / labels / ML / diagnostics / strategy, and
  does NOT authorize any successor.**

## 17. Sealed-test and v002 terminal boundary

- The new pre-v002 normalized segment covers **2024-03-01 .. 2024-11-30**,
  which contains **no** sealed-test dates and **no** v002 terminal-window
  dates.
- The existing v002 terminal window **2024-12-01 .. 2025-02-28** is treated
  **by reference only** (`v002_terminal_window_mode: "by_reference"`); it is
  already normalized as the published `__v002` family and is **not** read,
  re-downloaded, overwritten, or re-normalized by any convention in this memo.
- The sealed v002 test split **2025-02-14 .. 2025-02-28** remains **untouched**
  (`sealed_test_split_touched: false`, `test_holdout_touched: false`,
  `test_rows_loaded: 0`). Sealing is enforced at the ML/split layer
  (`iter_partitions(split="test", ...)` always raises), independent of
  normalization scope.
- Because the conservative pre-v002-only scope reads neither the v002 terminal
  raw window nor sealed-test raw dates, **a holdout-boundary memo is NOT
  required** to proceed. It becomes required **only if** a future phase
  proposes to read the v002 terminal raw window (e.g. to build a single
  rewritten full-envelope version) — which this memo explicitly does not.

## 18. Decision

**Result state:**
`RECORD_NORMALIZATION_MANIFEST_VERSIONING_CONVENTION__REMAIN_PAUSED`.

**Decision:**
`RECOMMEND_AUTHORIZE_NORMALIZATION_ONLY_EXECUTION__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Rationale: the preferred decision when the memo **successfully resolves
manifest/versioning without requiring v003 or v002 terminal raw reads** is
exactly this option. This memo resolves the convention cleanly by mirroring
the already-merged raw-layer segment precedent: a phase-scoped normalized
segment manifest + version-suffixed segment directory marked `pre_v002_segment`
under `dataset_version: "v002"`; predecessor linkage to the raw segment
manifest, raw gate report, and published `__v002` family by reference; the
full 12-month envelope represented by reference (segment manifest fields now;
optional deferred reference manifest later). The resolution requires **no
v003**, **no mutation of any published `__v002` manifest**, **no read or
re-normalization of the v002 terminal raw window**, **no sealed-test read**,
and **no eligibility flip**. Phase 4bn-M already established that the tooling
is safe/boundable (needing only a bounded new runner) and that the
sealed-test / v002 terminal boundary is clear for the conservative
pre-v002-only scope. With manifest/versioning now settled, the cleanest
next technical step is a separately-authorized normalization-only execution
phase honouring §10–§16 and the Phase 4bn-L budget.

This memo **does not authorize** the successor; the operator decides
separately. **No successor is authorized from inside Phase 4bn-N.**

## 19. Recommended state and successor options

**Recommended state: remain paused.** Phase 4bn-N is **branch-complete only**;
not merged into `main`; not project-complete until a separately authorized
merge phase records its merge-closeout on `main` per
`merge-closeout-standard.md` (Tier 1).

**Operator options (each subject to separate operator authorization; none
authorized here):**

- remain paused;
- request a merge prompt for Phase 4bn-N;
- separately authorize a **normalization-only execution phase** (this memo's
  recommendation) — a bounded new runner over the pre-v002 segment honouring
  §10–§16 and the Phase 4bn-L budget;
- separately authorize a **docs-only holdout-boundary memo** — **not
  required** for the conservative pre-v002-only scope; only relevant if a
  future phase intends to read the v002 terminal raw window;
- separately authorize a **source-policy documentation memo**;
- separately authorize a **process-doc `D:` path-string update** (the Phase
  4bm-D-P1 lightweight-workspace standard still carries old `C:` example
  paths);
- reject further ML-baseline successors and **close the ML-baseline arc**.

**Required successor validation/gate phases after any future normalization
(predeclared, none authorized):** a bounded **normalized-layer eligibility
gate** (§16) before any downstream stage; then, only if separately
authorized, feature derivation + feature gate; label derivation + label gate;
a new chronological-split / holdout policy memo before any ML or diagnostics.

## 20. Explicit non-authorizations

Phase 4bn-N did **not** and does **not** authorize: normalization; normalized
artefact generation; manifest creation or mutation; feature derivation; label
derivation; raw acquisition; any endpoint / public / Binance /
`data.binance.vision` call; archive or CHECKSUM download; HEAD preflight; any
local raw zip read; any v002 terminal-window read; any sealed-test read; any
local `data/research` or `data/microstructure` artefact / manifest / gate-
report read or creation; diagnostics; ML training; model scoring; predictions;
feature ranking / selection / pruning / engineering; hyperparameter or
threshold tuning; calibration fitting; strategy research; signal generation;
PnL simulation; backtests; manifest mutation; successor-state mutation;
gate-report mutation; `research_eligible` flip; `eligibility_gate_status`
transition; `chronological_split_policy` transition; `diagnostics_authorized`
or `ml_authorized` transition; `data/research` or `data/microstructure`
artefact creation or commit; storage migration; DuckDB / SQLite / `.duckdb` /
`.sqlite` / database creation; Parquet compaction; v003 creation; ETHUSDT;
extra horizons; mark-price; spot; cross-venue; order book; tick data; paper /
shadow; live-readiness; deployment; exchange-write; production keys; any
Phase 5; or any successor phase.

Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m
thread / V2 / G1 / C1) and every project lock (§11.6 = 8 bps per side;
round-trip = 16 bps; §1.7.3; Phase 3p §4.7; Phase 3r §8; Phase 3v §8;
Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v;
Phase 4w; Phase 4ak M0; Phase 4al refined no-rescue rule; Phase 4aw
`flip_research_eligible(...)` always-raises invariant (never invoked);
Phase 4bb-F canonical path + sidecar policy; the Phase 4bn-J-R1 raw-only cap
amendment; the Phase 4bn-L derived-stack storage budget) is preserved
verbatim. Phase 4 canonical remains unauthorized.

## 21. Current-project-state update summary

`docs/00-meta/current-project-state.md` was updated narrowly: a new Phase
4bn-N prose paragraph was appended after the Phase 4bn-M paragraph, and a new
`Current phase:` block for Phase 4bn-N was inserted ahead of the Phase 4bn-M
block. All prior Phase 4bn-A … 4bn-M paragraphs and `Current phase:` blocks
are preserved verbatim as labelled historical context. No other section of
`current-project-state.md` was changed. No code, test, script, data file,
configuration, `.gitignore`, `README.md`, MCP file, manifest, sidecar, gate
report, or successor-state artefact was created or modified. No local data was
read; no local data was created.
