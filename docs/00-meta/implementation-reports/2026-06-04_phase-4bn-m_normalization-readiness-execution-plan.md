# Phase 4bn-M — Normalization Readiness / Execution Plan

## 1. Purpose

This memo is a **docs-only normalization-readiness / execution-planning /
boundary-contract** deliverable. It determines, from committed repository
documentation and committed tooling only, whether the project can safely
authorize a future **normalization-only execution phase** for the expanded
12-month BTCUSDT Binance USDⓈ-M futures aggTrades raw envelope, while
preserving every Phase 4bn-L storage budget and deriving **no** features,
**no** labels, **no** ML, **no** diagnostics, **no** strategy outputs, and
**no** research-eligibility transitions.

This phase **runs no normalization**. It produces a predeclared future
execution contract — scope, inputs, outputs, manifest/versioning posture,
budget, preflight, fail-closed stop conditions, required tests, and required
successor validation/gate phases — and a decision among the six options
enumerated in §17. It authorizes nothing executable and authorizes no
successor.

This memo answers the readiness question in §7. It explicitly does **not**
ask whether the project can start ML, create labels, run the model, find
edge, backtest, trade, use the sealed test split, or make the dataset
research-eligible.

## 2. Authority and repository state

- **Active local repo path:** `D:\Prometheus`.
- **Active Claude Code lightweight workspace:** `D:\ClaudeRuns\prometheus-light`.
- **GitHub remote:** `origin` → `https://github.com/jpedrocY/Prometheus.git`
  (verified intact).
- **Branch:** `phase-4bn-m/normalization-readiness-execution-plan`.
- **Base `main` SHA:** `b7767a636a864bcb2eeca6a613c8f7c602a85c5b`
  (`docs(phase-4bn-l): finalize merge closeout shas`). Pre-branch
  `main == origin/main == HEAD` was verified in sync. The Phase 4bn-L
  SHA-finalization commit `b7767a6`, merge-closeout `4479a69`, merge
  `5c7b5a9`, and branch finalization `20022d2` are all present on `main`;
  the Phase 4bn-K SHA-finalization commit `d8d3ba8` is present as the
  predecessor.
- **Tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3. This phase is
  adjacent to future normalized-artefact generation over the expanded
  12-month envelope, future normalized eligibility gates, future feature
  derivation, future label derivation, future holdout/split policy, future
  ML-baseline admissibility, and local disk/runtime budgets — while
  explicitly authorizing no normalization, no features, no labels, no ML,
  no diagnostics, and no downstream use.
- **Working-tree expectation:** only the untracked transient
  `.claude/scheduled_tasks.lock`; the gitignored namespaces
  `data/microstructure/` (`.gitignore:85`) and `data/research/`
  (`.gitignore:88`) exist locally and remain uncommitted.

## 3. Phase type and strict scope

**Phase type:** docs-only / normalization-readiness / execution-planning /
boundary-contract.

**Allowed work performed by this phase:**

- read committed Markdown docs;
- inspect committed source, scripts, and tests read-only;
- identify existing normalization tooling and conventions;
- compare existing tooling to the expanded 12-month raw segment;
- define a future normalization execution contract;
- define exact future input/output paths by convention without reading or
  creating them;
- define future manifest/sidecar/versioning/preflight/fail-closed policy;
- decide whether a future phase can reuse existing tooling directly or
  needs a bounded new wrapper;
- define required offline tests for any future tooling;
- create the two tracked Phase 4bn-M docs and update
  `current-project-state.md` narrowly.

**This phase did NOT and must NOT (within Phase 4bn-M):** run normalization;
read local raw zip contents; read local `data/microstructure` artefacts;
read local `data/research` artefacts; read any local manifest, gate report,
or sidecar under `data/microstructure`; create normalized artefacts;
create features; create labels; run ML; run diagnostics; run strategy /
signals / PnL / backtests; acquire data; call any endpoint; create a
database; compact Parquet; create v003; or authorize any successor.

## 4. Evidence base and input boundary

**Inputs read (committed repository evidence only):**

- `docs/00-meta/current-project-state.md` (latest-state narrative and
  Phase 4bn-L / 4bn-K / 4bn-J-R2 paragraphs and `Current phase:` blocks);
- the process standards `merge-closeout-standard.md`,
  `phase-risk-tiering-standard.md`, `phase-workflow-standard.md`,
  `phase-prompt-template.md`, `operator-report-standard.md`;
- the Phase 4bn-L derived-stack storage-budget memo and closeout;
- the Phase 4bn-K expanded raw archive eligibility-gate report narrative
  and closeout;
- the Phase 4bn-J-R2 acquisition narrative and closeout;
- the data specs `data-requirements.md`, `historical-data-spec.md`,
  `timestamp-policy.md`, `dataset-versioning.md`, and
  `database-design.md`;
- committed tooling read-only:
  `scripts/phase4bm_b_normalize_multiday_aggtrades.py`,
  `scripts/phase4bn_j_r2_acquire_btcusdt_aggtrades_pre_v002.py`,
  `scripts/phase4bn_k_validate_pre_v002_raw_archive_gate.py`,
  `scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py`,
  `scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py`;
  `src/prometheus/research/microstructure/normalize_io.py`,
  `normalize_aggtrades.py`, `normalize_manifest.py`,
  `normalize_validation.py`, `canonical_paths.py`, and the surrounding
  `derived_gate*` / `multiday_derived_gate*` modules;
- the committed offline test surface under `tests/research/microstructure/`
  (`test_normalize_aggtrades.py`, `test_normalize_io.py`,
  `test_normalize_manifest.py`, `test_normalize_no_network.py`,
  `test_normalize_validation.py`,
  `test_phase4bm_b_multiday_normalization.py`).

**Inputs explicitly NOT used:** any local raw zip contents; the existing
v002 terminal raw window; the sealed v002 test split; any local
`data/microstructure` normalized / feature / label / manifest / gate-report
artefact; any local `data/research` artefact; no hashing, counting, or
inspection of local gitignored data; no endpoints; no credentials; no
`.env`; no `.mcp.json`; no MCP; no Graphify. **README was treated as
potentially stale and was not used as current-state authority.**

## 5. Phase 4bn-L budget carried forward

The future normalization phase, if separately authorized, must obey the
Phase 4bn-L derived-stack storage budget verbatim:

- **Raw layer (carried forward, unchanged):** 4.788 GiB
  (5,140,686,147 bytes) already acquired and gate-passed; raw-only
  acquisition cap **10 GiB warning / 25 GiB hard**; no new raw acquisition
  authorized.
- **Normalized layer (future):** **100 GiB warning / 150 GiB hard**
  footprint; **4 h warning / 8 h hard** runtime.
- **Feature layer (future, not in scope):** 50 GiB / 100 GiB; 4 h / 8 h.
- **Label layer (future, not in scope):** 75 GiB / 125 GiB; 4 h / 8 h.
- **Temporary workspace (future):** **50 GiB warning / 100 GiB hard**;
  cleaned on success or fail-closed stop; under an explicit gitignored
  path; pre/post-cleanup footprint reported.
- **Total derived-stack (future, binding aggregate):** **250 GiB warning /
  300 GiB hard** additional footprint beyond raw archives. The total cap is
  lower than the sum of per-stage caps and **binds the aggregate even when
  per-stage caps still have headroom.**
- **`D:` free-space floor:** **≥ 500 GiB free before execution** (else fail
  closed, operator decision); **fail closed if `D:` free space falls below
  350 GiB during execution.**

**Binding rule restated:** if any future normalization preflight estimates
normalized output above **150 GiB**, total derived-stack above **300 GiB**,
or `D:` free space below **500 GiB**, the future phase must **stop before
writing**.

## 6. Phase 4bn-K raw gate carried forward

- **Result:** `RAW_ARCHIVE_GATE_PASSED__LOCAL_RAW_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`;
  **33 / 33 PASS**.
- **Segment:** BTCUSDT / Binance USDⓈ-M futures / aggTrades;
  **2024-03-01 .. 2024-11-30 inclusive UTC**; **275** daily archives;
  **275** sidecars; **5,140,686,147 bytes**; **400,001,695 rows**;
  **281,600** sampled rows validated.
- **Eligibility:** `research_eligible` remains **false**;
  `eligibility_gate_status` remains **pending**; **no** manifest
  eligibility transition occurred. The raw segment remains
  **non-eligible** in the research sense.
- **Boundary:** the existing v002 terminal window (2024-12-01 .. 2025-02-28)
  was treated **by reference only**; the sealed v002 test split
  (2025-02-14 .. 2025-02-28) was **not** read / counted / sampled / hashed
  / summarized / inspected; the Phase 4aw
  `flip_research_eligible(...)` always-raises invariant was preserved
  (never invoked).
- **A passing raw archive gate does NOT flip `research_eligible`, does NOT
  transition `eligibility_gate_status`, and does NOT authorize
  normalization, features, labels, ML, diagnostics, strategy, or any
  successor.**

## 7. Normalization-readiness question

> **Can the project safely authorize a future normalization-only execution
> phase for the expanded BTCUSDT Binance USDⓈ-M futures aggTrades raw
> envelope, using committed raw artefact conventions and preserving all
> Phase 4bn-L storage budgets, while deriving no features, no labels, no
> ML, no diagnostics, no strategy outputs, and no research eligibility
> transitions?**

This is **not** phrased as: "Can we start ML?"; "Can we create labels?";
"Can we run the model?"; "Can we find edge?"; "Can we backtest?"; "Can we
trade?"; "Can we use the sealed test split?"; or "Can we make the dataset
research-eligible?".

**Answer (this memo's finding):** Normalization tooling **primitives** are
safe and reusable and the conservative pre-v002-only scope keeps the
sealed-test boundary clear, **but** the manifest/versioning shape for a
pre-v002 normalized segment is **ambiguous** in committed evidence.
Therefore the project can safely *prepare* for normalization, but the
cleanest next technical step is to **resolve the normalization
manifest/versioning convention in a docs-only memo before authorizing
execution** — see §16–§18.

## 8. Existing normalization tooling and conventions

A complete aggTrades-normalization stack already exists and is committed.

**Reusable, network-free primitives (directly reusable, assessed SAFE):**

- `src/prometheus/research/microstructure/normalize_aggtrades.py` —
  `NORMALIZED_SCHEMA_V001` (the locked Phase 4bd 19-column normalized
  schema), `NORMALIZATION_SCHEMA_VERSION`, and the offline CSV row iterator
  `iter_aggtrade_rows_from_csv`.
- `src/prometheus/research/microstructure/normalize_io.py` — path
  discipline (`assert_path_under_microstructure`,
  `assert_output_path_under_normalized`,
  `assert_manifest_path_under_manifests`), in-memory single-CSV ZIP reader,
  **atomic** Parquet writer (`atomic_write_parquet`, zstd, `os.replace`,
  refuse-overwrite), atomic JSON manifest writer, **canonical two-space
  `.sha256` sidecar** writer (`write_sha256_sidecar` →
  `<sha256>␠␠<basename>\n`), and SHA256 helpers. This module imports **no**
  networking library, uses **no** credentials, reads **no** `.env` /
  `.mcp.json`, and writes **only** under `data/microstructure/normalized/`
  and `data/microstructure/manifests/`.
- `normalize_manifest.py`, `normalize_validation.py`, `canonical_paths.py`,
  and the `derived_gate*` / `multiday_derived_gate*` library modules —
  normalized manifest construction, normalized-artefact validators, and
  canonical-path helpers.

**Output / versioning conventions observed in committed code:**

- Normalized partition layout (from `normalize_io.derive_normalized_output_path`
  and the Phase 4bm-B orchestrator):
  `data/microstructure/normalized/microstructure_normalized_aggtrades_v001__<version>/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-aggTrades-<YYYY-MM-DD>.parquet`,
  each with a paired `.sha256` sidecar.
- Normalized index manifest:
  `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__<version>.json`
  with a paired `.sha256` sidecar; manifest seeded `research_eligible: false`,
  `eligibility_gate_status: "pending"`, with governance labels
  `feature_computation: "forbidden"`, `strategy_use: "forbidden"`.
- Existing normalized versions: `__v001` (single-day Phase 4bd) and
  `__v002` (90-day multi-day Phase 4bm-B covering 2024-12-01 .. 2025-02-28).

**Existing runner is NOT directly reusable (assessed NEEDS A BOUNDED NEW
WRAPPER):** `scripts/phase4bm_b_normalize_multiday_aggtrades.py` is
**hardcoded** to the 90-day v002 window
(`EXPECTED_DATE_COUNT = 90`, `EXPECTED_DATE_START = "2024-12-01"`,
`EXPECTED_DATE_END = "2025-02-28"`,
`EXPECTED_TOTAL_EVENT_COUNT = 155,153,449`) and to **locked precondition
SHAs** for the **published v002 raw manifest**
(`microstructure_raw_aggtrades_v001__v002.json`), the Phase 4bl-D-R PASS
gate report, and the Phase 4bl-E successor-state. It also enforces a v002
identity cross-check (`date_count == 90`, `total_row_count == 155,153,449`).
The pre-v002 segment was acquired under a **different, phase-scoped segment
manifest** (`microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2.json`,
275 archives, 400,001,695 rows) with different SHAs, so pointing 4bm-B's
CLI flags at the segment manifest would **fail closed** on the precondition
SHA check and identity check. Additionally, 4bm-B **predates the Phase
4bn-L budget** and has **no disk/runtime preflight caps**.

**Conclusion (tooling):** the underlying primitives are safe and directly
reusable, but a **bounded new normalization runner** is required for the
pre-v002 segment — exactly as Phase 4bn-J-R2 needed a new bounded
acquisition script (because the Phase 4bl-C acquisition script was hardcoded
to the v002 90-day range) and Phase 4bn-K needed a new bounded raw-gate
runner (scoped to the segment manifest). The bounded runner must reuse the
locked primitives unchanged and **add** the Phase 4bn-L preflight/budget
caps that 4bm-B lacks.

## 9. Future normalization input boundary

A future normalization phase, if separately authorized, may read **only**:

- the **new pre-v002 raw segment** 2024-03-01 .. 2024-11-30 inclusive UTC
  (BTCUSDT, Binance USDⓈ-M futures, aggTrades), as recorded in the Phase
  4bn-J-R2 segment manifest and admitted by the Phase 4bn-K raw gate;
- the segment manifest, its sidecar, the acquisition log, its sidecar, and
  the Phase 4bn-K raw gate report and its sidecar, **for integrity
  verification only**.

It may read these **only** to verify SHA256 integrity and to enumerate the
authorized date inventory. **Recommended conservative first execution:**
normalize **only** the pre-v002 segment, and do **not** read the existing
v002 terminal raw window (2024-12-01 .. 2025-02-28) at all, because that
window is **already normalized** by the existing `__v002` normalized family.
The full 12-month normalized envelope can later be assembled **by manifest /
reference** (concatenating the pre-v002 normalized segment with the existing
`__v002` normalized family) rather than by re-reading or re-normalizing the
terminal window. See §11 and §12.

## 10. Future normalization output contract

If separately authorized later, normalization must:

- **Symbol:** BTCUSDT only. **Market:** Binance USDⓈ-M futures.
  **Data family:** aggTrades only.
- **Output family:** **normalized aggTrades only** — no features, no
  labels, no research matrices, no `data/research` outputs.
- **Output storage:** the existing
  `data/microstructure/normalized/microstructure_normalized_aggtrades_v001__<version>/BTCUSDT/<YYYY>/<MM>/`
  convention; **Parquet canonical** (zstd, as `atomic_write_parquet`);
  **canonical two-space `.sha256` sidecars** for every artefact;
  **refuse-overwrite**; atomic write-then-rename.
- **Schema:** preserve the locked Phase 4bd 19-column
  `NORMALIZED_SCHEMA_V001` verbatim (no added column; the existing
  forbidden-substring guard on column names — `label`, `target`, `future`,
  `signal`, `pnl`, `prediction`, `model`, `score`, `strategy`,
  `mark_price`, `funding`, `open_interest`, `order_book`, … — preserved).
- **Manifest:** create **only** a new **non-eligible** normalization
  manifest (`research_eligible: false`, `eligibility_gate_status:
  "pending"`, `feature_computation: "forbidden"`, `strategy_use:
  "forbidden"`); record predecessor linkage to the pre-v002 raw segment
  manifest and the Phase 4bn-K gate report; **no** existing manifest
  mutation.
- **No database; no `.duckdb`; no `.sqlite`; no Parquet compaction; no
  v003; no storage migration.**
- **Leave all outputs non-eligible and gitignored; commit no data
  artefact.**

## 11. Manifest and versioning considerations

`docs/04-data/dataset-versioning.md` codifies a `<dataset_name>__vNNN`
identifier policy: **monotonic**, **never reuse or overwrite** a published
version, manifest required at the dataset-version root with a **predecessor
version** field, and **published versions immutable** (corrections produce a
new version with a recorded predecessor; publication states `draft` /
`published` / `deprecated` / `superseded`).

The committed normalized family already uses `__v001` and `__v002`. The
**ambiguity** is that the pre-v002 *raw* segment was **not** named as a new
`__vNNN`; it was written as a **phase-scoped segment manifest**
(`microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2.json`)
that extends the v002 envelope **backward**. The dataset-versioning doc does
**not** codify "segment manifests," predecessor-linked backward extensions,
or how a backward segment relates to an already-published terminal version.
For the normalized layer this leaves three unresolved candidate shapes:

1. a **segment manifest** for the normalized pre-v002 output, mirroring the
   raw-layer segment-manifest practice (e.g.
   `microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_*.json`);
2. a **predecessor-linked extension** of the existing `__v002` normalized
   family that is later concatenated **by reference** into a full 12-month
   normalized envelope;
3. a **new full-envelope version** — which would collide with the
   forbidden **v003** boundary and with the monotonic-`__vNNN` immutability
   rule, and is therefore **not** an acceptable shape under this memo's
   constraints.

Because committed evidence supports candidate (1) by raw-layer precedent and
candidate (2) by the dataset-versioning predecessor-linkage rule, but does
**not** settle which is canonical for the normalized layer — nor how the
eventual full 12-month normalized envelope is identified — **the
manifest/versioning shape is ambiguous.** This is the binding factor in the
§17 decision.

## 12. Sealed-test / v002 terminal-window boundary

The sealed v002 test split (2025-02-14 .. 2025-02-28) lies **entirely
within** the existing v002 terminal window (2024-12-01 .. 2025-02-28). That
window was **already normalized** by Phase 4bm-B into the `__v002`
normalized family. **Sealing is enforced at the ML / split layer**
(`test_rows_loaded: 0`; `iter_partitions(split="test", ...)` always raises),
**not** at the raw-to-normalized layer: raw-to-normalized transformation
over the sealed-test dates was already performed by Phase 4bm-B and does
**not** itself constitute test-use.

The **new pre-v002 segment** (2024-03-01 .. 2024-11-30) contains **no**
sealed-test dates. Therefore the **conservative pre-v002-only first
normalization does not read the v002 terminal raw window at all and never
touches sealed-test raw dates** — the holdout boundary is **clear for the
conservative scope**, and a separate holdout-boundary memo is **not
required** to proceed with pre-v002-only normalization.

**Conditional flag:** if a future phase ever proposes to **read the v002
terminal raw window** (e.g. to re-normalize it, or to build a single
full-envelope normalized version that re-covers the sealed-test dates under
a new convention), the holdout boundary must be **re-examined first** via a
separate docs-only holdout-boundary memo, because that would change which
raw dates are read and could blur the raw-to-normalized vs test-use line.
**Regardless of normalization scope, the sealed test split must remain
preserved from any ML / diagnostic / statistical / strategy / research use.**

## 13. Future normalization budget and preflight requirements

The future normalization phase must **measure before writing**:

1. `D:` free space (must be ≥ 500 GiB before execution).
2. Estimated normalized output footprint (must be ≤ 150 GiB; ≤ 100 GiB
   without warning).
3. Estimated temporary workspace footprint (≤ 100 GiB; ≤ 50 GiB without
   warning).
4. Estimated total derived-stack footprint (≤ 300 GiB binding aggregate;
   ≤ 250 GiB without warning).
5. Estimated runtime (≤ 8 h; ≤ 4 h without warning).
6. Exact input raw archive **date coverage** expected (pre-v002 segment;
   275 days unless re-scoped).
7. Exact output **partition count** expected.
8. Whether the existing v002 terminal raw dates will be read or **treated
   by reference** (recommended: by reference only).
9. Whether **sealed-test dates** are in the raw-to-normalized input range
   (recommended: **no**, under pre-v002-only scope).
10. Whether a **separate holdout-boundary memo** is required before touching
    sealed-test raw dates (required **only** if the v002 terminal window is
    to be read — see §12).

**Stop before writing** if preflight cannot estimate the normalized output
footprint, or if any estimate exceeds 150 GiB normalized / 300 GiB total /
8 h runtime, or if `D:` free space is below 500 GiB.

## 14. Future normalization execution requirements

If separately authorized later, normalization must:

- read **only** approved raw input dates (verified against the Phase
  4bn-J-R2 segment manifest by SHA256);
- write **only** normalized aggTrades artefacts;
- write **only** under approved gitignored
  `data/microstructure/normalized/` paths (enforced by
  `assert_output_path_under_normalized`);
- create **canonical two-space `.sha256` sidecars** for every artefact;
- create or update **only** a new **non-eligible** normalization manifest;
- **refuse overwrite** of any finalised output;
- record exact commands, footprint, runtime, counts, paths, and hashes;
- measure at **day/month boundaries** and enforce caps per-boundary;
- clean temporary files on success **or** fail-closed stop and report
  pre/post-cleanup footprint;
- leave **all outputs non-eligible** (`research_eligible: false`,
  `eligibility_gate_status: "pending"`);
- **not** commit any data artefact;
- **not** create features, labels, research outputs, databases, v003, or
  compacted Parquet;
- preserve the Phase 4aw `flip_research_eligible(...)` always-raises
  invariant (never invoked) and every retained verdict and project lock.

## 15. Future fail-closed stop conditions

A future normalization phase must **fail closed** on **any** of the
following:

1. Missing raw archive prerequisite.
2. Missing raw sidecar prerequisite.
3. Raw archive hash mismatch.
4. Raw archive path outside approved BTCUSDT aggTrades raw conventions.
5. Any date outside the authorized future normalization range.
6. Any ambiguity about whether to read the existing v002 terminal /
   sealed-test raw dates.
7. Any attempt to use sealed-test data for ML, diagnostics, statistics,
   strategy, or research.
8. Preflight cannot estimate normalized output footprint.
9. Preflight normalized output estimate exceeds **150 GiB**.
10. Preflight total derived-stack estimate exceeds **300 GiB**.
11. `D:` free space below **500 GiB** before execution.
12. `D:` free space below **350 GiB** during execution.
13. Temporary workspace exceeds **100 GiB**.
14. Runtime exceeds **8 hours**.
15. Any output path outside approved gitignored
    `data/microstructure/normalized/` conventions.
16. Any attempt to create `data/research` output.
17. Any attempt to create features.
18. Any attempt to create labels.
19. Any attempt to run ML, diagnostics, strategy, PnL, or backtests.
20. Any attempt to create DuckDB / SQLite / database files.
21. Any attempt to compact Parquet.
22. Any attempt to create v003.
23. Any attempt to flip `research_eligible`.
24. Any attempt to transition `eligibility_gate_status` to eligible.
25. Any attempt to commit `data/microstructure` or `data/research`.
26. Any need for ETHUSDT, mark-price, spot, cross-venue, order-book, tick,
    or extra-horizon data.
27. Any deviation from BTCUSDT / Binance USDⓈ-M futures / aggTrades /
    v002-compatible semantics.
28. Any missing or ambiguous manifest/versioning convention.
29. Any inability to create canonical sidecars.
30. Any validator / tooling unsafe condition.

## 16. Readiness assessment

- **Existing normalization tooling — primitives:** **SAFE and directly
  reusable.** `normalize_aggtrades.py` and `normalize_io.py` are
  network-free, credential-free, path-disciplined, atomic, refuse-overwrite,
  with canonical two-space sidecars and the locked 19-column schema. A solid
  offline test suite already exists (`test_normalize_aggtrades.py`,
  `test_normalize_io.py`, `test_normalize_manifest.py`,
  `test_normalize_no_network.py`, `test_normalize_validation.py`,
  `test_phase4bm_b_multiday_normalization.py`).
- **Existing normalization tooling — runner:** **NEEDS A BOUNDED NEW
  WRAPPER.** `phase4bm_b_normalize_multiday_aggtrades.py` is hardcoded to the
  90-day v002 window and locked v002 precondition SHAs, reads the published
  v002 raw manifest (not the pre-v002 segment manifest), enforces a v002
  identity cross-check, and has no Phase 4bn-L preflight/budget caps. It
  cannot be repointed at the pre-v002 segment. A bounded new runner —
  reusing the locked primitives and adding segment-date guards, the segment
  manifest as source, and the 4bn-L preflight/budget caps — is required,
  with its own offline test module. This mirrors the Phase 4bn-J-R2 (new
  bounded acquisition script) and Phase 4bn-K (new bounded raw-gate runner)
  precedents and is **safe and bounded**, not unsafe.
- **Manifest / versioning:** **AMBIGUOUS.** The pre-v002 raw segment used a
  phase-scoped segment manifest; the dataset-versioning doc codifies only
  monotonic `__vNNN` + predecessor linkage and does not settle the
  normalized segment-manifest / backward-extension / full-envelope shape;
  v003 is forbidden. This must be resolved before execution.
- **Sealed-test / v002 terminal boundary:** **CLEAR for the conservative
  pre-v002-only scope** (sealed-test dates are not in the pre-v002 input
  range and are already normalized in the `__v002` family; raw-to-normalized
  over sealed dates was already done by 4bm-B and is not test-use).
  Conditionally requires a separate holdout-boundary memo **only if** a
  future phase proposes to read the v002 terminal raw window.
- **Budget / preflight / fail-closed:** **fully defined** (§13–§15) and
  consistent with Phase 4bn-L.

**Net:** tooling is safe and boundable, and the holdout boundary is clear
for the conservative scope, but the **manifest/versioning shape is
ambiguous.** Per the decision logic predeclared for this phase, an ambiguous
manifest/versioning shape calls for a **docs-only normalization
manifest/versioning memo before authorizing execution.**

## 17. Decision

**`RECOMMEND_AUTHORIZE_DOCS_ONLY_NORMALIZATION_MANIFEST_VERSIONING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`**

Rationale: normalization **execution** is the preferred decision only when
existing or easily bounded tooling is safe **and** the manifest/versioning
**and** holdout boundaries are clear. Here the tooling is safe/boundable and
the holdout boundary is clear for the conservative pre-v002-only scope, but
the **manifest/versioning shape for a pre-v002 normalized segment is
genuinely ambiguous** (segment manifest vs predecessor-linked extension vs a
forbidden full-envelope v003; and how the eventual full 12-month normalized
envelope is identified). The predeclared preferred decision when the
manifest/versioning shape is ambiguous is exactly this option. Resolving
that convention in a small docs-only memo is the cleanest, lowest-risk next
step and directly unblocks a subsequent normalization-only execution phase.

This memo **does not authorize** the successor; the operator decides
separately. No successor is authorized from inside Phase 4bn-M.

## 18. Recommended state and successor options

**Recommended state: remain paused.** Phase 4bn-M is **branch-complete
only**; not merged into `main`; not project-complete until a separately
authorized merge phase records its merge-closeout on `main` per
`merge-closeout-standard.md` (Tier 1).

**Operator options (each subject to separate operator authorization; none
authorized here):**

- remain paused;
- request a merge prompt for Phase 4bn-M;
- separately authorize a **docs-only normalization manifest/versioning
  memo** (this memo's recommendation) to settle the pre-v002 normalized
  manifest shape, predecessor linkage, and full-envelope identity, after
  which a normalization-only execution phase can be cleanly scoped;
- separately authorize a **normalization-only execution phase** directly,
  accepting that it must internally resolve the manifest/versioning shape
  and build a bounded new runner with offline tests and Phase 4bn-L caps;
- separately authorize a **docs-only holdout-boundary memo** (only needed if
  a future phase intends to read the v002 terminal raw window);
- separately authorize a **source-policy documentation memo**;
- separately authorize a **process-doc `D:` path-string update** (the Phase
  4bm-D-P1 lightweight-workspace standard still carries old `C:` example
  paths);
- reject further ML-baseline successors and **close the ML-baseline arc**.

**Required successor validation/gate phases after any future normalization
(predeclared, none authorized):** a bounded **normalized-layer eligibility
gate** (analogous to the Phase 4bn-K raw gate; the existing
`derived_gate*` / `multiday_derived_gate*` modules plus the normalizer's
inline strict-fail-closed contract are the reusable basis) to verify the
normalized artefacts and manifest before any downstream stage; then, only if
separately authorized, feature derivation + feature gate; label derivation +
label gate; a new chronological-split / holdout policy memo before any ML or
diagnostics. Each is separately authorized.

## 19. Explicit non-authorizations

Phase 4bn-M did **not** and does **not** authorize: normalization; feature
derivation; label derivation; raw acquisition; any endpoint / public /
Binance / `data.binance.vision` call; archive or CHECKSUM download; HEAD
preflight; any local raw zip read; any v002 terminal-window read; any
sealed-test read; any local `data/research` or `data/microstructure`
artefact read or creation; any local gate-report or manifest read under
`data/microstructure`; diagnostics; ML training; model scoring; predictions;
feature ranking / selection / pruning / engineering; hyperparameter or
threshold tuning; calibration fitting; strategy research; signal generation;
PnL simulation; backtests; manifest mutation; successor-state mutation;
gate-report mutation; `research_eligible` flip; `eligibility_gate_status`
transition; `chronological_split_policy` transition; `diagnostics_authorized`
or `ml_authorized` transition; `data/research` or `data/microstructure`
artefact creation or commit; storage migration; DuckDB / SQLite / `.duckdb`
/ `.sqlite` / database creation; Parquet compaction; v003 creation; ETHUSDT;
extra horizons; mark-price; spot; cross-venue; order book; tick data; paper
/ shadow; live-readiness; deployment; exchange-write; production keys; any
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

## 20. Current-project-state update summary

`docs/00-meta/current-project-state.md` was updated narrowly: a new Phase
4bn-M prose paragraph was appended after the Phase 4bn-L paragraph, and a
new `Current phase:` block for Phase 4bn-M was inserted ahead of the Phase
4bn-L block. All prior Phase 4bn-A … 4bn-L paragraphs and `Current phase:`
blocks are preserved verbatim as labelled historical context. No other
section of `current-project-state.md` was changed. No code, test, script,
data file, configuration, `.gitignore`, `README.md`, MCP file, manifest,
sidecar, gate report, or successor-state artefact was created or modified.
No local data was read; no local data was created.
