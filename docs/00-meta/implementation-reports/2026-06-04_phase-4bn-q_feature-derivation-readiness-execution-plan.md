# Phase 4bn-Q — Feature-Derivation Readiness / Execution Plan

## 1. Purpose

Phase 4bn-Q is a **docs-only feature-derivation readiness / feature execution
planning / feature manifest and gate boundary-contract** deliverable. It
determines, from committed repository documentation and committed tooling only,
whether the project can safely authorize a future **feature-only execution**
phase over the Phase 4bn-O / 4bn-P local normalized pre-v002 BTCUSDT Binance
USDⓈ-M futures aggTrades segment (2024-03-01 .. 2024-11-30 inclusive UTC; 275
dates; 400,001,695 events), what that future execution's exact scope, inputs,
outputs, manifest/versioning, budget, preflight, and fail-closed contract must
be, and whether any prerequisite docs-only memo is required first.

This phase **derives no features, creates no feature artefacts, reads no local
normalized/feature/label/research data, creates no `data/microstructure` or
`data/research` artefact, and authorizes no successor.** It does not ask whether
the project can start ML, create labels, find edge, backtest, trade, use the
sealed test split, or make the dataset research-eligible.

## 2. Authority and repository state

- **Active local repo path:** `D:\Prometheus`. **Active Claude Code lightweight
  workspace:** `D:\ClaudeRuns\prometheus-light`.
- **GitHub remote:** `origin` → `https://github.com/jpedrocY/Prometheus.git`
  (verified intact).
- **Branch:** `phase-4bn-q/feature-derivation-readiness-execution-plan`.
- **Base `main` SHA:** `b2b46de6a27311318b2e9d58f5de28e5137b28dd`
  (`docs(phase-4bn-p): finalize merge closeout shas`). Pre-branch
  `main == origin/main == HEAD` verified in sync; the Phase 4bn-P
  SHA-finalization `b2b46de`, merge-closeout `486c8c7`, merge `a10f255`, and
  branch commit `6e75711` are present on `main`.
- **Tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (adjacent to future
  feature artefact generation, future feature-layer eligibility gates, future
  label derivation, future chronological split/holdout policy, future
  ML-baseline admissibility, and local disk/runtime budgets — while authorizing
  none of those).
- **Working-tree expectation:** the untracked transient
  `.claude/scheduled_tasks.lock`; the gitignored namespaces
  `data/microstructure/` (`.gitignore:85`) and `data/research/`
  (`.gitignore:88`) exist locally (Phase 4bn-O normalized outputs + Phase 4bn-P
  gate report) and remain uncommitted.

## 3. Phase type and strict scope

**Phase type:** docs-only / feature-derivation readiness / feature execution
planning / feature manifest and gate boundary-contract.

**Allowed (and the entirety of what was done):** read committed Markdown docs;
inspect committed source, scripts, and tests read-only; identify the existing
feature-derivation tooling and feature manifest/gate conventions; compare them
to the pre-v002 normalized segment; define the future feature-only execution
contract (scope, inputs, outputs, manifest/versioning, budget, preflight,
fail-closed); define required offline tests for any future feature wrapper;
define the future feature-layer eligibility gate; create the two tracked Phase
4bn-Q docs; update `current-project-state.md` narrowly.

**Forbidden (and not done):** no feature derivation; no label derivation; no
normalization rerun; no raw acquisition; no endpoint / Binance /
`data.binance.vision` call; no archive/CHECKSUM download; no HEAD preflight; no
raw-gate or normalized-layer-gate rerun; no local normalized/raw/feature/label
read; no v002 terminal-window read; no sealed-test read; no local
`data/microstructure` or `data/research` artefact read or creation; no
diagnostics; no ML / scoring / predictions; no feature ranking / selection /
pruning / tuning / calibration; no strategy / signals / PnL / backtests; no
manifest / successor-state / gate-report mutation; no `research_eligible` flip;
no `eligibility_gate_status` / `chronological_split_policy` /
`diagnostics_authorized` / `ml_authorized` transition; no database / `.duckdb` /
`.sqlite`; no Parquet compaction; no storage migration; no v003; no ETHUSDT /
mark-price / spot / cross-venue / order-book / tick / extra-horizon; no
credentials / `.env` / `.mcp.json` / MCP / Graphify; no successor authorization.

## 4. Evidence base and input boundary

**Committed evidence read:** `docs/00-meta/current-project-state.md`; the process
standards (`merge-closeout-standard.md`, `phase-risk-tiering-standard.md`,
`phase-workflow-standard.md`, `phase-prompt-template.md`,
`operator-report-standard.md`); the Phase 4bn-P / 4bn-O / 4bn-N / 4bn-L reports,
merge-closeouts, and closeouts; the data specs (`data-requirements.md`,
`historical-data-spec.md`, `timestamp-policy.md`, `dataset-versioning.md`) and
`database-design.md`; and committed feature/derived tooling read-only:
`scripts/phase4bm_h_compute_multiday_features.py`,
`scripts/phase4bm_j_run_multiday_feature_gate.py`,
`src/prometheus/research/microstructure/features_schema_v002.py`,
`features_compute_v002.py`, `features_io_v002.py`, `features_manifest_v002.py`,
`features_schema.py`, `multiday_feature_gate*.py`, and the v001/v002 feature
implementation-report memos (Phase 4bh-A/B, 4bi-A/B/C/D, 4bm-G/H/I/J/K/L). The
prior normalization arc (Phase 4bn-M/N/O/P) was read as the governing precedent.
README treated as potentially stale, not used as current-state authority.

**Input boundary (hard, fail-closed for this phase):** committed repository
Markdown and committed code/tests only. No local normalized Parquet, raw zip,
feature, label, gate-report, manifest, sidecar, successor-state, or
`data/research` artefact was opened, hashed, counted, or inspected; SHA256
digests cited for local gitignored artefacts are quoted from committed Markdown
evidence (prior closeouts / current-project-state), not by reading local files.
No endpoint, credential, `.env`, `.mcp.json`, MCP, or Graphify.

## 5. Phase 4bn-P normalized-layer gate carried forward

Phase 4bn-P (merge-complete on `main`, SHA `b2b46de`) ran a read-only
normalized-layer eligibility gate over the Phase 4bn-O pre-v002 normalized
segment and recorded
`NORMALIZED_LAYER_GATE_PASSED__LOCAL_NORMALIZED_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`
(25/25 PASS, 15.0 s): 275 Parquet + 275 sidecars validated; recomputed rows
400,001,695 and footprint 3,954,532,918 B exact; schema exactly
`NORMALIZED_SCHEMA_V001`; manifest required-field and forbidden-field contracts
passed; predecessor integrity passed; published `__v002` by-reference and
immutable; v002 terminal raw window unread; sealed-test split untouched. The
segment remains **non-eligible** (`research_eligible: false`,
`eligibility_gate_status: "pending"`); no eligibility transition occurred. Phase
4bn-P's decision was
`RECOMMEND_AUTHORIZE_FEATURE_DERIVATION_READINESS_OR_EXECUTION_PLAN…` — i.e. it
recommended exactly this readiness plan. **A passing normalized-layer gate makes
the segment structurally suitable to proceed to feature-derivation planning; it
does not make the dataset research-eligible and authorizes no feature
derivation.**

## 6. Phase 4bn-O normalized segment carried forward

The future feature input is the Phase 4bn-O local gitignored normalized segment:
manifest
`data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json`
(SHA256 `0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa`) +
sidecar (SHA256 `5d7dcbef…6402`); 275 normalized Parquet (zstd) + 275 canonical
sidecars under
`data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o/BTCUSDT/<YYYY>/<MM>/`;
400,001,695 events; footprint 3,954,532,918 B; schema `NORMALIZED_SCHEMA_V001`
(19 columns); `dataset_version: "v002"`, `segment_label: "pre_v002_segment"`,
`research_eligible: false`, `eligibility_gate_status: "pending"`,
`v002_terminal_window_mode: "by_reference"`, `existing_v002_normalized_reference.{read,mutated}=false`,
`sealed_test_split_touched: false`, `test_rows_loaded: 0`. Built per the Phase
4bn-N manifest/versioning convention.

## 7. Phase 4bn-L budget carried forward

The future feature phase must obey the Phase 4bn-L derived-stack budget verbatim:

- **Feature layer:** warn **50 GiB** / hard **100 GiB** additional feature
  footprint; runtime warn **4 h** / hard **8 h**.
- **Temporary workspace:** warn **50 GiB** / hard **100 GiB**.
- **Total derived-stack (binding aggregate):** warn **250 GiB** / hard **300
  GiB** additional footprint beyond raw archives.
- **`D:` free-space floor:** ≥ **500 GiB** before execution; **fail closed below
  350 GiB** during execution.
- Stop before writing if the feature preflight estimates feature output > 100
  GiB, total derived-stack > 300 GiB, runtime > 8 h, or `D:` free < 500 GiB.

(Context: the normalized pre-v002 segment is 3.68 GiB. By the merged v002 feature
precedent — 62-column features over the same event population — the feature
footprint is materially larger per event than normalized but still expected to
be well within the 100 GiB feature cap; the future preflight must measure, not
assume.)

## 8. Feature-readiness question

**Answered question:** *Can the project safely authorize a future feature-only
execution phase for the Phase 4bn-O / 4bn-P pre-v002 BTCUSDT Binance USDⓈ-M
futures aggTrades normalized segment, using committed normalized-artefact
conventions and preserving all Phase 4bn-L storage budgets, while deriving no
labels, no ML outputs, no diagnostics, no strategy outputs, no research outputs,
and no research-eligibility transition?*

**Answer (summary; detail in §9–§17):** The feature **primitives** are safe and
reusable, and the sealed-test / v002-terminal boundary is **clear** for the
conservative causal-only pre-v002 scope — so feature execution is technically
approachable via a bounded new wrapper. **However**, two manifest/versioning
contract questions are genuinely unsettled: (a) the existing feature tooling
hard-requires a **research-eligible Stage-3 successor-state** source that the
non-eligible pre-v002 segment does not (and must not) have; and (b) the
pre-v002 **feature segment** manifest/versioning shape and its non-eligible
posture are not yet codified. The clean, precedent-consistent next step is a
docs-only **feature manifest/versioning memo** before any execution — exactly
mirroring how Phase 4bn-N settled the normalized layer before Phase 4bn-O ran.

## 9. Existing feature tooling and conventions

The repository already contains a complete v001 and v002 microstructure feature
stack (Phase 4bh / 4bi for v001; Phase 4bm-G/H/I/J/K/L for v002):

- **Feature schema (`features_schema_v002.py`):** family
  `microstructure_features_aggtrades_v001`, `dataset_version: "v002"`,
  `feature_schema_version: "v001"`; **62 columns** = 17 lineage + 45
  feature/quality, canonical order; 4 trailing windows (1s/5s/15s/60s).
  `LEAKAGE_POLICY_V002 = "causal_only_no_future_lookahead"`; windows are
  right-closed/left-open `(T-window, T]` with same-timestamp tie-break by
  `row_index`; a **26-token forbidden-substring guard** rejects column names
  implying label/target/future/signal/strategy/PnL/model/score/prediction/
  decision/backtest. There are **no label, target, future-return, or model
  columns** in the feature schema.
- **Cross-day policy:** `CROSS_DAY_LOOKBACK_POLICY_V002 =
  "causal_cross_day_lookback"` with `CROSS_DAY_TAIL_BUFFER_MS = 60_000` (= max
  window). For each day ≥ 2 the prior-day **tail** (last 60 s) is loaded as
  read-only **backward** context; day 1 carries `rolling_missing_window_flag =
  True` for rows whose trailing window would extend before the window start.
  This is strictly causal: no forward/next-day read is ever required.
- **Feature I/O (`features_io_v002.py`):** output layout
  `data/microstructure/features/microstructure_features_aggtrades_v001__v002/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-features-aggtrades-<YYYY-MM-DD>.parquet`
  (version-suffixed family directory, mirroring the normalized `__v002` layout)
  with canonical Phase 4bb-F two-space `.sha256` sidecars; manifest
  `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json`;
  atomic write-then-rename + refuse-overwrite.
- **Feature compute orchestrator (`scripts/phase4bm_h_compute_multiday_features.py`):**
  hardcoded to the **90-day v002 terminal window** (`EXPECTED_DATE_START =
  "2024-12-01"`, `EXPECTED_DATE_END = "2025-02-28"`, `EXPECTED_DATE_COUNT = 90`,
  `EXPECTED_TOTAL_EVENT_COUNT = 155_153_449`) with a `LOCKED_PRECONDITIONS`
  table that requires the **published `__v002` normalized manifest** (SHA
  `01c5fa53…`), the v002 raw manifest, the Phase 4bm-D normalized gate report,
  and — critically — the **Phase 4bm-F `stage3_research_eligible`
  successor-state** (SHA `72b6edd4…`). It has no Phase 4bn-L preflight/budget
  caps.
- **Feature gate (`multiday_feature_gate*.py`, Phase 4bm-J):** likewise
  hardcoded to the 90-day v002 window (`EXPECTED_DATE_START = "2024-12-01"`,
  count 90, total feature rows 155,153,449, 62/17/45 column counts) and the same
  Stage-3 research-eligible successor-state precondition.

## 10. Future feature input boundary

The recommended conservative future feature input is **only** the Phase 4bn-O
pre-v002 normalized segment:

- Symbol BTCUSDT only; Binance USDⓈ-M futures only; aggTrades only; normalized
  dataset only; dates 2024-03-01 .. 2024-11-30 inclusive UTC (275 dates).
- Source manifest = the Phase 4bn-O segment manifest (`…_pre_v002_segment_4bn_o.json`,
  SHA `0e96ae37…d9fa`), verified against the Phase 4bn-P gate report; **not** the
  published `__v002` normalized manifest.
- The published normalized `__v002` family is treated **by reference only** and
  is **not read**. Because the feature kernel is strictly causal
  (backward-only, 60 s tail), computing features for the segment's **last** day
  (2024-11-30) needs **no** forward context from 2024-12-01; computing the
  segment's **first** day (2024-03-01) needs no pre-2024-03-01 read (its early
  rows carry `rolling_missing_window_flag = True`, exactly as v002 day 1 did).
  All cross-day tail reads stay **inside** 2024-03-01 .. 2024-11-30.
- Therefore the conservative pre-v002 feature scope reads **no** v002 terminal
  normalized date and **no** sealed-test date. If any future feature window were
  ever to require lookback before 2024-03-01 or forward context after
  2024-11-30, the future phase must **fail closed and require a memo** (see §13).

## 11. Future feature output contract

- **Output family:** feature artefacts only — `microstructure_features_aggtrades_v001`.
  **No** labels, targets, future returns, model outputs, diagnostics, research
  matrices, or `data/research` outputs.
- **Output storage:** under the existing gitignored
  `data/microstructure/features/` convention; Parquet (zstd) canonical; canonical
  two-space `.sha256` sidecars; a single **non-eligible** feature segment
  manifest + sidecar. No database; no `.duckdb`/`.sqlite`; no Parquet
  compaction.
- **Output directory (recommended segment convention, to be confirmed by the
  §12 memo):**
  `data/microstructure/features/microstructure_features_aggtrades_v001__v002_pre_v002_segment_<feature-phase-id>/BTCUSDT/<YYYY>/<MM>/BTCUSDT-features-aggtrades-<YYYY-MM-DD>.parquet`
  — a version-suffixed **segment** directory distinct from the published
  `microstructure_features_aggtrades_v001__v002/` directory, exactly mirroring
  the Phase 4bn-N normalized segment convention.
- **Eligibility posture:** `research_eligible: false`,
  `eligibility_gate_status: "pending"`, `no_successor_authorization: true`;
  Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved
  (never invoked).
- **Schema:** exactly the locked 62-column `FEATURE_SCHEMA_V002` (17 lineage +
  45 feature/quality), causal-only, with the forbidden-substring column guard
  passing.

## 12. Feature manifest and versioning considerations

This is the **binding ambiguity** for the feature layer, and it has two parts:

1. **Source-precondition divergence (new, unsettled).** The existing v002
   feature compute orchestrator and feature gate **hard-require a Stage-3
   research-eligible successor-state** (Phase 4bm-F) for their normalized source.
   The pre-v002 normalized segment is deliberately **non-eligible**
   (`eligibility_gate_status: "pending"`; no Stage-3 successor exists, and Phase
   4bn-P explicitly did **not** flip eligibility). A future feature wrapper must
   therefore source from a **non-eligible, normalized-layer-gate-passed**
   segment (the Phase 4bn-P PASS), **not** from a research-eligible Stage-3
   successor. How a feature wrapper validates that non-eligible source, and what
   eligibility posture the resulting features carry, is not codified anywhere in
   the repo and must be settled before execution.
2. **Segment manifest/versioning shape (analogous to Phase 4bn-N, not yet
   applied to features).** `dataset-versioning.md` codifies only monotonic
   `__vNNN` + predecessor linkage. Phase 4bn-N settled the **normalized** layer's
   pre-v002 segment convention (phase-scoped segment manifest;
   `dataset_version: "v002"`; `segment_label: "pre_v002_segment"`;
   version-suffixed segment directory; full envelope + `__v002` by reference;
   no v003; no `__v002` mutation). The feature layer has **no** corresponding
   codified rule. The natural, precedent-consistent shape is a phase-scoped
   **feature segment manifest**
   `microstructure_features_aggtrades_v001__v002_pre_v002_segment_<feature-phase-id>.json`
   with `dataset_family = "microstructure_features_aggtrades_v001"`,
   `dataset_version = "v002"`, `feature_schema_version = "v001"`,
   `segment_label = "pre_v002_segment"`, predecessor linkage to the Phase 4bn-O
   normalized segment manifest + Phase 4bn-P normalized-layer gate report, and a
   by-reference `existing_v002_feature_reference` block. But this must be
   **explicitly settled** (segment manifest vs predecessor-linked extension vs
   full-envelope reference), together with the §12.1 non-eligible-source
   precondition, in a dedicated docs-only memo.

Because (1) is a genuine new contract question and (2) is unsettled for the
feature layer, the feature manifest/versioning shape is **ambiguous** and a
docs-only **feature manifest/versioning memo** is the predeclared preferred next
step.

## 13. Sealed-test / v002 terminal boundary

- The new pre-v002 feature scope covers 2024-03-01 .. 2024-11-30, which contains
  **no** sealed-test date (2025-02-14 .. 2025-02-28) and **no** v002 terminal
  window date (2024-12-01 .. 2025-02-28).
- The feature kernel is **strictly causal** (`causal_only_no_future_lookahead`),
  with cross-day lookback limited to a 60 s **backward** tail. Computing the
  segment's last day (2024-11-30) requires **no** forward read into the v002
  terminal window; computing the first day (2024-03-01) requires **no** read
  before the segment (early rows flagged `rolling_missing_window_flag`).
- Therefore, for the conservative pre-v002-only feature scope, a
  **holdout-boundary memo is NOT required**. It would become required **only if**
  a future feature phase proposed to read the v002 terminal normalized window or
  sealed-test normalized dates (e.g. to build a single full-envelope feature
  family or to provide forward context) — which the conservative scope explicitly
  does not. Sealing remains enforced at the ML/split layer
  (`iter_partitions(split="test", ...)` always raises; `test_rows_loaded: 0`),
  independent of feature scope.

## 14. Future feature budget and preflight requirements

The future feature execution phase must, **before writing any artefact**,
measure and record: (1) `D:` free space (≥ 500 GiB floor); (2) estimated feature
output footprint (≤ 100 GiB hard); (3) estimated temporary-workspace footprint
(≤ 100 GiB hard); (4) estimated total derived-stack footprint (≤ 300 GiB hard);
(5) estimated runtime (≤ 8 h hard); (6) exact input normalized date coverage
expected (275 dates); (7) exact output partition count expected (275); (8)
whether v002 terminal normalized dates will be read or treated by reference
(must be **by reference**); (9) whether sealed-test dates are in the feature
input or context range (must be **no**); (10) whether any feature window requires
lookback/forward context beyond the pre-v002 segment (must be **no**); (11)
whether a holdout-boundary memo is required (must be **no** for the conservative
scope); (12) whether the §12 feature manifest/versioning memo has been completed
(must be **yes**). During execution it must measure footprint, runtime, and `D:`
free space at day/month boundaries and fail closed on any hard-cap breach.

## 15. Future feature execution requirements

If separately authorized later, feature derivation must: build a **bounded new
wrapper** reusing the locked feature primitives (`features_schema_v002`,
`features_compute_v002`, `features_io_v002`, `features_manifest_v002`) unchanged,
adding the pre-v002 segment source contract, the §12-settled segment naming, the
Phase 4bn-L preflight/budget caps, and a non-eligible-source precondition (the
Phase 4bn-O segment manifest SHA + Phase 4bn-P gate report, **not** a Stage-3
successor); read only the approved 275 normalized segment dates (verified by
SHA256 against the Phase 4bn-O manifest and admitted by the Phase 4bn-P gate);
write only feature Parquet + canonical sidecars under the §11 segment directory
plus a single non-eligible feature segment manifest + sidecar; refuse to
overwrite; atomic write-then-rename; record exact commands, footprint, runtime,
counts, paths, hashes, feature schema, and feature family; measure at day/month
boundaries; clean temporary files on success or fail-closed stop; leave all
outputs non-eligible; commit no data artefact; create no labels, targets,
future returns, ML outputs, diagnostics, research outputs, databases, v003, or
compacted Parquet; carry its own offline test module (segment naming, date
guard, causal/no-leakage, forbidden-column guard, refuse-overwrite, budget-cap,
no-network, no-sealed-read, non-eligible posture) mirroring the Phase 4bn-O /
4bn-P test precedents; preserve the Phase 4aw `flip_research_eligible(...)`
always-raises invariant (never invoked).

## 16. Future fail-closed stop conditions

A future feature phase must fail closed (stop, report partial outputs, leave all
outputs non-eligible and uncommitted) on any of: (1) missing normalized segment
prerequisite; (2) missing normalized sidecar; (3) normalized Parquet hash
mismatch; (4) normalized path outside approved BTCUSDT aggTrades normalized
conventions; (5) any date outside the authorized feature range; (6) ambiguity
about reading v002 terminal / sealed-test normalized dates; (7) any use of
sealed-test data for ML/diagnostics/statistics/strategy/research/tuning; (8) any
feature requiring forward-looking information; (9) any feature requiring future
returns or labels; (10) any feature requiring unavailable lookback context; (11)
preflight cannot estimate feature footprint; (12) preflight feature estimate >
100 GiB; (13) preflight total derived-stack > 300 GiB; (14) `D:` free < 500 GiB
before execution; (15) `D:` free < 350 GiB during execution; (16) temp workspace
> 100 GiB; (17) runtime > 8 h; (18) any output path outside approved gitignored
`data/microstructure/features/` conventions; (19) any `data/research` output;
(20) any label creation; (21) any ML/diagnostics/strategy/PnL/backtest; (22) any
DuckDB/SQLite/database; (23) any Parquet compaction; (24) any v003; (25) any
`research_eligible` flip; (26) any `eligibility_gate_status` → eligible; (27) any
`data/microstructure` or `data/research` commit; (28) any need for ETHUSDT /
mark-price / spot / cross-venue / order-book / tick / extra-horizon; (29) any
deviation from BTCUSDT / Binance USDⓈ-M futures / aggTrades / v002-compatible
semantics; (30) any missing or ambiguous feature manifest/versioning convention
(i.e. the §12 memo not completed); (31) any inability to create canonical
sidecars; (32) any validator/tooling unsafe condition; (33) any feature column
name implying target/label/future/signal/strategy/PnL/model/score/prediction/
backtest; (34) any feature computation that leaks forward information across a
date boundary; (35) any feature computation that requires the sealed test split.

## 17. Feature tooling readiness assessment

- **Feature primitives — `features_schema_v002.py`, `features_compute_v002.py`,
  `features_io_v002.py`, `features_manifest_v002.py`, `features_schema.py`:**
  **directly reusable** (unchanged). Causal-only, no labels/targets/future,
  forbidden-substring column guard, canonical sidecars, atomic refuse-overwrite
  writes, network-free, credential-free; established offline test suite present.
- **Feature compute orchestrator —
  `scripts/phase4bm_h_compute_multiday_features.py`:** **NOT directly reusable;
  needs a bounded new wrapper.** It is hardcoded to the 90-day v002 terminal
  window (2024-12-01 .. 2025-02-28; count 90; 155,153,449 events), expects the
  **published `__v002` normalized manifest**, requires the Phase 4bm-F **Stage-3
  research-eligible successor-state**, assumes the published `__v002` feature
  family directory, and has **no** Phase 4bn-L preflight/budget caps. It does
  **not** touch labels/returns and creates **no** `data/research` output (good),
  and it does enforce sidecars + manifests + immutability (good) — but its window
  and eligible-source preconditions are incompatible with the non-eligible
  pre-v002 segment.
- **Feature gate — `multiday_feature_gate*.py` (Phase 4bm-J):** **NOT directly
  reusable; needs a bounded new wrapper** (same 90-day v002 hardcoding + Stage-3
  successor precondition), exactly as the normalized-layer gate needed the
  bounded Phase 4bn-P runner rather than the published-`__v002`
  `multiday_derived_gate`.
- **Existing tests:** cover the v002 90-day terminal shape; they do **not** cover
  the pre-v002 segment shape — a new offline test module would be required for
  any new wrapper.
- **Overall classification:** the feature layer is **reusable only through a
  bounded new wrapper** (primitives safe; orchestrator + gate need bounded
  segment wrappers), **and** the feature manifest/versioning + non-eligible-source
  precondition is **ambiguous and requires docs-only design first** (§12). The
  sealed-test / v002-terminal boundary is **clear** for the conservative
  causal-only pre-v002 scope (§13).

## 18. Decision

**Result state:** `RECORD_FEATURE_DERIVATION_READINESS_PLAN__REMAIN_PAUSED`.

**Decision:**
`RECOMMEND_AUTHORIZE_DOCS_ONLY_FEATURE_MANIFEST_VERSIONING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Rationale (repository-evidence-grounded): the feature **primitives** are safe and
reusable and the sealed-test / v002-terminal boundary is clear for the
conservative causal-only pre-v002 scope (so a holdout-boundary memo is **not**
required), but the feature **manifest/versioning shape is genuinely ambiguous**
for two reasons — (a) the existing feature orchestrator and gate hard-require a
**Stage-3 research-eligible successor-state** source that the non-eligible
pre-v002 segment does not and must not have, so the non-eligible-source feature
precondition must be defined; and (b) the pre-v002 **feature segment**
manifest/versioning convention and non-eligible feature posture are not codified
(Phase 4bn-N settled this only for the normalized layer). The predeclared
preferred decision when feature manifest/versioning is ambiguous is a docs-only
feature manifest/versioning memo before execution. This mirrors the merged
precedent exactly: the normalization arc went readiness-plan (4bn-M) →
manifest/versioning memo (4bn-N) → execution (4bn-O) → gate (4bn-P); the feature
arc should follow the same disciplined sequence. **Phase 4bn-Q authorizes
nothing executable and authorizes no successor.**

The full set of admissible Phase 4bn-Q decision options was:
`RECORD_FEATURE_DERIVATION_READINESS_PLAN__REMAIN_PAUSED`;
`RECOMMEND_AUTHORIZE_FEATURE_ONLY_EXECUTION__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
`RECOMMEND_AUTHORIZE_DOCS_ONLY_FEATURE_MANIFEST_VERSIONING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
(selected);
`RECOMMEND_AUTHORIZE_DOCS_ONLY_HOLDOUT_BOUNDARY_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
`RECOMMEND_AUTHORIZE_SOURCE_POLICY_DOCUMENTATION_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
`RECOMMEND_AUTHORIZE_PROCESS_DOC_PATH_UPDATE__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
`RECOMMEND_CLOSE_ML_BASELINE_ARC__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

## 19. Recommended state and successor options

**Recommended state: remain paused.** Phase 4bn-Q is **branch-complete only**;
not merged into `main`; not project-complete until a separately authorized merge
phase records its merge-closeout on `main` per `merge-closeout-standard.md`
(Tier 1).

**Operator options (each subject to separate operator authorization; none
authorized here):**

- remain paused (default);
- request a merge prompt for Phase 4bn-Q;
- separately authorize a **docs-only feature manifest/versioning memo** (this
  phase's recommendation) — settling the pre-v002 feature segment manifest shape,
  the version-suffixed segment directory, the non-eligible-source precondition
  (sourcing from the Phase 4bn-O segment + Phase 4bn-P gate rather than a Stage-3
  successor), and the by-reference linkage to the published `__v002` feature
  family; **then**, only if separately authorized, a bounded feature-only
  execution wrapper + offline tests honouring §10–§16, followed by a bounded
  feature-layer eligibility gate;
- separately authorize a feature-only execution phase directly (which would have
  to internally resolve the §12 manifest/versioning + non-eligible-source
  precondition and build a bounded new wrapper with offline tests and 4bn-L
  caps) — less clean than settling the memo first;
- separately authorize a docs-only holdout-boundary memo — **not** required for
  the conservative pre-v002-only feature scope; only relevant if a future scope
  reads the v002 terminal normalized window or sealed-test dates;
- separately authorize a source-policy documentation memo;
- separately authorize a process-doc `D:` path-string update;
- reject further ML-baseline successors and **close the ML-baseline arc**.

**Required successor validation/gate phases after any future feature execution
(predeclared, none authorized):** a bounded **feature-layer eligibility gate**
(analogous to Phase 4bn-P / the Phase 4bm-J feature gate, reusing the
`multiday_feature_gate*` checks via a bounded segment wrapper) before any
downstream stage; then, only if separately authorized, label derivation + label
gate; a chronological-split / holdout policy memo before any ML or diagnostics.

## 20. Explicit non-authorizations

Phase 4bn-Q did **not** and does **not** authorize: feature derivation; feature
artefact generation; feature manifest creation or mutation; label derivation;
normalization rerun; raw acquisition; any endpoint / public / Binance /
`data.binance.vision` call; archive / CHECKSUM download; HEAD preflight; raw-gate
or normalized-layer-gate rerun; any local raw/normalized/feature/label read; any
v002 terminal-window read; any sealed-test read; any local `data/microstructure`
or `data/research` artefact read or creation; diagnostics; ML training; model
scoring; predictions; feature ranking / selection / pruning / engineering;
hyperparameter or threshold tuning; calibration fitting; strategy research;
signal generation; PnL simulation; backtests; manifest / successor-state /
gate-report mutation; `research_eligible` flip; `eligibility_gate_status` /
`chronological_split_policy` / `diagnostics_authorized` / `ml_authorized`
transition; `data/research` or `data/microstructure` artefact creation or commit;
storage migration; DuckDB / SQLite / `.duckdb` / `.sqlite` / database creation;
Parquet compaction; v003 creation; ETHUSDT; extra horizons; mark-price; spot;
cross-venue; order book; tick data; paper / shadow; live-readiness; deployment;
exchange-write; production keys; any Phase 5; or any successor phase.

Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread /
V2 / G1 / C1) and every project lock (§11.6 = 8 bps per side; round-trip = 16
bps; §1.7.3; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8;
Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0;
Phase 4al refined no-rescue rule; Phase 4aw `flip_research_eligible(...)`
always-raises invariant (never invoked); Phase 4bb-F canonical path + sidecar
policy; the Phase 4bn-J-R1 raw-only cap amendment; the Phase 4bn-L derived-stack
storage budget; the Phase 4bn-N normalization manifest/versioning convention) is
preserved verbatim. Phase 4 canonical remains unauthorized.

## 21. Current-project-state update summary

`docs/00-meta/current-project-state.md` was updated narrowly: one new Phase
4bn-Q narrative paragraph was appended after the Phase 4bn-P paragraph, and a new
`Current phase:` block for Phase 4bn-Q was inserted ahead of the Phase 4bn-P
block. All prior Phase 4bn-A … 4bn-P paragraphs and `Current phase:` blocks are
preserved verbatim as labelled historical context. No other section of that
document was changed. No code, test, script, data file, configuration,
`.gitignore`, `README.md`, MCP file, manifest, sidecar, gate report, or
successor-state artefact was created or modified. No local data was read; no
local data was created.
