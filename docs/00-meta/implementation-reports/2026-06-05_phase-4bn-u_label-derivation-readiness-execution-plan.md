# Phase 4bn-U — Label-Derivation Readiness / Execution Plan

## 1. Purpose

Phase 4bn-U is a **docs-only label-derivation readiness / execution-plan**
phase. It determines — from committed repository Markdown and committed
code / tests only — whether the project can safely authorize a future
**label-only execution** phase for the Phase 4bn-S / 4bn-T pre-v002 BTCUSDT
Binance USDⓈ-M futures aggTrades feature segment (2024-03-01 .. 2024-11-30
inclusive UTC), and, if so, exactly what that future execution scope,
input boundary, output contract, manifest/versioning shape, sealed-test /
v002-terminal boundary, storage/runtime budget, preflight, fail-closed
conditions, required tests, and follow-on label-layer eligibility gate must
be.

Phase 4bn-U **derives no labels**, creates **no label artefacts**, reads
**no local Parquet / manifest / gate-report data**, runs **no ML, no
diagnostics, no strategy, no PnL, no backtests**, performs **no acquisition
and calls no endpoints**, makes **no manifest eligibility transition**, and
**authorizes no successor**. It is a planning memo only.

This phase is **Tier 1 — Full Phase** per
`docs/00-meta/process/phase-risk-tiering-standard.md` §3, because it is
adjacent to future label artefact generation over the pre-v002 feature
segment, future label-layer eligibility gates, future chronological-split /
holdout policy, future ML-baseline admissibility, and local disk/runtime
budgets — while explicitly authorizing none of them.

## 2. Authority and repository state

- **Authorizing input:** the operator Phase 4bn-U prompt, issued after the
  Phase 4bn-T feature-layer gate decision
  `RECOMMEND_AUTHORIZE_LABEL_DERIVATION_READINESS_OR_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Branch:** `phase-4bn-u/label-derivation-readiness-execution-plan`.
- **Base `main` SHA (verified in sync at branch creation):**
  `28e1683646499a910186efdf48d4a5d01a23e630`
  (`docs(phase-4bn-t): finalize merge closeout shas`); pre-branch
  `HEAD == main == origin/main`.
- **Predecessor chain present on `main`:** `28e1683` (4bn-T merge-closeout
  SHA finalize) ← `019bc39` (4bn-T merge-closeout) ← `8149750` (4bn-T merge)
  ← `b9843bd` (4bn-T branch) ← `e647435` (4bn-S merge-closeout SHA finalize).
- **Remote:** `https://github.com/jpedrocY/Prometheus.git`.
- **Working tree at start:** only the expected untracked transient
  `.claude/scheduled_tasks.lock`; gitignored `data/microstructure/` and
  `data/research/` namespaces present locally and untouched.

Phase 4bn-T is merge-complete, SHA-finalized, pushed, and synchronized on
`main`. Phase 4bn-U is branch-complete only by this work; it is **not**
merged and **not** project-complete until a separately authorized merge
phase records its merge-closeout on `main`.

## 3. Phase type and strict scope

**Phase type:** docs-only / label-derivation readiness / label execution
planning / label manifest and gate boundary-contract phase.

**Allowed work performed:** read committed Markdown; inspect committed
source / scripts / tests read-only; identify existing label tooling and
label manifest conventions; compare existing tooling to the pre-v002 feature
segment requirements; define a future label-only execution contract; define
exact future input/output by convention without reading or creating data;
define future manifest/sidecar, holdout/sealed-test/v002-terminal boundary,
preflight, fail-closed, required tests, and the future label-layer
eligibility gate; create two tracked docs; update
`docs/00-meta/current-project-state.md` narrowly.

**Forbidden (and not performed):** no label derivation; no label artefact
generation; no label manifest creation or mutation; no feature / feature-gate
/ normalization / normalized-gate / raw rerun; no acquisition; no endpoint
calls; no local raw / normalized / feature / label / gate-report / manifest
reads under `data/microstructure`; no `data/research` reads or writes; no
v002 terminal-window read; no sealed-test read; no diagnostics; no ML; no
strategy / signals / PnL / backtests; no `research_eligible` flip; no
`eligibility_gate_status` / `chronological_split_policy` /
`diagnostics_authorized` / `ml_authorized` transition; no DuckDB / SQLite /
database; no Parquet compaction; no v003; no successor authorization.

## 4. Evidence base and input boundary

All findings below are grounded **only** in committed artefacts:

- **Committed source** under `src/prometheus/research/microstructure/`,
  notably: `labels_schema_v002.py`, `labels_io_v002.py`,
  `labels_manifest_v002.py`, `labels_compute_v002.py`, `labels_io.py`,
  `labels_validation.py`; the label gates `label_gate*.py` (v001) and
  `multiday_label_gate*.py` (v002); and the feature/normalized peers used by
  the pre-v002 arc.
- **Committed scripts** under `scripts/`, notably
  `phase4bm_o_compute_multiday_labels.py` (the v002 multiday label
  orchestrator), `phase4bm_q_run_multiday_label_gate.py`, and the pre-v002
  arc scripts `phase4bn_o_normalize_pre_v002_aggtrades.py`,
  `phase4bn_p_validate_normalized_pre_v002_gate.py`,
  `phase4bn_s_compute_pre_v002_features.py`,
  `phase4bn_t_validate_feature_pre_v002_gate.py`.
- **Committed tests** under `tests/research/microstructure/`, notably the
  `test_labels_*`, `test_multiday_label_gate_*`, and `test_phase4bn_*`
  suites.
- **Committed implementation reports** for Phases 4bn-L, 4bn-O, 4bn-P,
  4bn-R, 4bn-S, 4bn-T (and their closeouts / merge-closeouts).
- **Committed process standards** under `docs/00-meta/process/` and the data
  specs under `docs/04-data/` and `docs/08-architecture/database-design.md`.

**Input boundary honoured:** no local Parquet, manifest, sidecar, gate
report, or zip under `data/microstructure/` or `data/research/` was opened,
hashed, counted, or inspected. The README was treated as potentially stale
and **not** used as current-state authority.

## 5. Phase 4bn-T feature-layer gate carried forward

- Result:
  `FEATURE_LAYER_GATE_PASSED__LOCAL_FEATURE_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`;
  **27 / 27 PASS**; runtime 348.9 s.
- Validated the Phase 4bn-S local feature pre-v002 segment: BTCUSDT /
  Binance USDⓈ-M futures / aggTrades; 2024-03-01 .. 2024-11-30 inclusive UTC;
  275 dates; 275 feature Parquet + 275 canonical `.sha256` sidecars;
  400,001,695 rows; 54,254,406,538 bytes (≈50.53 GiB); schema exactly
  `FEATURE_SCHEMA_V002` (62 columns = 17 lineage + 45 feature/quality);
  required-field and forbidden-substring contracts passed; leakage /
  causal-policy validation passed; predecessor integrity passed.
- Feature manifest
  `…/manifests/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s.json`
  SHA256
  `4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52`.
- Gate report (local gitignored, uncommitted)
  `…/gate-reports/features/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s__phase-4bn-t__1780674917156__e647435c81d7.json`
  SHA256
  `db731d1be06295404ef195d9b5b5bad8010ce6ae6efef43ece90c29653d6ab08`.
- Non-eligible posture preserved: `research_eligible=false`,
  `eligibility_gate_status=pending`, `no_successor_authorization=true`; no
  manifest eligibility transition; published feature `__v002` family
  by-reference and immutable; v002 terminal raw/normalized windows unread;
  sealed-test split untouched (`test_rows_loaded=0`).
- Decision carried forward:
  `RECOMMEND_AUTHORIZE_LABEL_DERIVATION_READINESS_OR_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
  — i.e. exactly this Phase 4bn-U.

## 6. Phase 4bn-S feature segment carried forward

- Feature-derived the approved pre-v002 segment 2024-03-01 .. 2024-11-30
  inclusive UTC; 275 feature Parquet + 275 sidecars; 400,001,695 feature
  rows; footprint 54,254,406,538 bytes; schema exactly `FEATURE_SCHEMA_V002`
  (62 columns).
- Feature manifest SHA256 `4881eb87…b52`; manifest sidecar SHA256
  `f2ca2f48…2e5`.
- **`feature_config_hash` = `0726b41d48e5f7127728c385b150d90fad91a92b3400c0545649b541e4dd114c`**;
  `feature_schema_hash` = `bf3d80bc…ff5`.
- Output directory segment
  `data/microstructure/features/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s/BTCUSDT/<YYYY>/<MM>/BTCUSDT-features-aggtrades-<YYYY-MM-DD>.parquet`.
- `research_eligible=false`; `eligibility_gate_status=pending`; no successor.
- Predecessor normalized layer (Phase 4bn-O): 2024-03-01 .. 2024-11-30; 275
  normalized Parquet; 400,001,695 rows; footprint 3,954,532,918 bytes;
  manifest `…__v002_pre_v002_segment_4bn_o.json` SHA256 `0e96ae37…d9fa`
  (sidecar `5d7dcbef…6402`); directory segment
  `…/normalized/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o/…`.
- Predecessor normalized-layer gate (Phase 4bn-P): **25 / 25 PASS**; gate
  report SHA256 `3452fd9d…f134`.

**Critical lineage note (from `feature_config_hash` `0726b41d…`):** this
differs from the published v002 feature family's locked
`EXPECTED_FEATURE_CONFIG_HASH`
(`819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d`) that the
existing v002 label orchestrator hard-asserts. The pre-v002 segment is a
distinct, segment-scoped feature family by manifest, path, and config hash.

## 7. Phase 4bn-L budget carried forward

The future label phase must obey the Phase 4bn-L derived-stack budget caps
verbatim:

| Bound | Warning | Hard cap |
|---|---|---|
| Label-layer footprint | 75 GiB | **125 GiB** |
| Label runtime | 4 hours | **8 hours** |
| Temporary workspace | 50 GiB | **100 GiB** |
| Total derived-stack | 250 GiB | **300 GiB** |

D: drive rules: **≥ 500 GiB free required before execution**; **fail closed
if D: free space falls below 350 GiB during execution**.

Stage-boundary rule: label derivation may run only after the normalized and
feature prerequisites are complete and a label phase is **separately
authorized**; ML may run only after all gates pass plus a separate
chronological-split policy. Phase 4bn-U authorizes none of these.

**Stop-before-write rule (binding for any future label preflight):** if a
future label preflight estimates label output above **125 GiB**, total
derived-stack above **300 GiB**, runtime above **8 h**, or D: free space
below **500 GiB**, it must stop before writing any output.

## 8. Label-readiness question

> Can the project safely authorize a future **label-only execution** phase
> for the Phase 4bn-S / 4bn-T pre-v002 BTCUSDT Binance USDⓈ-M futures
> aggTrades feature segment, using committed feature artefact conventions and
> preserving all Phase 4bn-L storage budgets, while creating no ML outputs,
> no diagnostics, no strategy outputs, no research outputs, no research
> eligibility transition, and no sealed-test usage?

This is **not** the question "can we start ML?", "can we find edge?", "can we
backtest?", "can we trade?", "can we use the sealed test split?", or "can we
make the dataset research-eligible?". The answer those questions all remain
**no / not authorized**.

**Answer (this memo):** A future label-only execution is *feasible and safe
in principle* — the existing causal forward-return/direction label family is
boundary-safe over the pre-v002 segment when the forward-reference envelope
terminal is locked to the segment's own terminal — **but it cannot reuse the
existing v002 label orchestrator/gate directly, and its label manifest /
versioning shape (and the `label_config_hash` lineage model) is not yet
settled for a non-eligible, successor-state-free segment.** The conservative,
evidence-grounded recommendation is therefore to first authorize a
**docs-only label manifest / versioning memo** (see §18), not yet a label
execution.

## 9. Existing label tooling and conventions

The repository already contains a **complete, tested** offline label stack
for the BTCUSDT aggTrades family. Read-only inspection establishes the
following.

**9.1 Label semantics (no barrier / no MFE / MAE / R-multiple).**
`labels_schema_v002.py` defines the family
`microstructure_labels_aggtrades_v001 @ v002`, a **40-column** schema:
17 lineage columns + `label_config_hash` + **8 label columns**
(`forward_log_return_{1s,5s,15s,60s}` regression and
`forward_direction_{1s,5s,15s,60s}` classification ∈ {−1, 0, +1}) + 14
support columns (per-horizon `reference_row_index_*`,
`reference_timestamp_ms_*`, `horizon_censored_flag_*`, plus
`label_invalid_price_flag`, `label_any_censored_flag`). Horizons are
`("1s","5s","15s","60s")` paired with `(1000, 5000, 15000, 60000)` ms.

The labels are **pure causal forward-return / forward-direction**. There is
**no triple-barrier, no stop, no MFE, no MAE, no R-multiple, no target-
before-stop** logic; in fact `barrier`, `mfe`, `mae`, `r_multiple`,
`target`, `signal`, `strategy`, `pnl`, `position`, `prediction`, `model`,
`score`, `decision`, `entry`, `exit`, `liquidation`, etc. are **forbidden
substrings** that the schema validator rejects in any output column name
(`assert_no_forbidden_label_substrings_v002`). The label family is thus a
research artefact, not a strategy/signal/PnL artefact.

**9.2 Anchor / reference / censoring policy (the boundary-critical part).**
The `label_config_hash` locks `ANCHOR_POLICY_V002`,
`FUTURE_REFERENCE_POLICY_V002`, `DIRECTION_THRESHOLD_POLICY_V002`,
`NULL_CENSORING_POLICY_V002`, `DTYPE_POLICY_V002`. The future-reference
policy is bounded by an **`envelope_terminal_unix_ms`**: for each feature row
`R` with `feature_timestamp_ms`, the target is `feature_timestamp_ms + H_ms`;
if the target exceeds `envelope_terminal_unix_ms`, **all horizon labels are
null and `horizon_censored_flag` is true**; otherwise the reference row is the
largest-`row_index` normalized aggTrade row across the envelope with
`transact_time_ms ≤ target`. **Cross-day reference is allowed only within the
envelope.** The anchor price and reference price are read from the
**normalized** per-day Parquet (`trade_price_of_normalized_aggtrade_row`),
**not** from the feature Parquet.

**Implication:** a label run reads BOTH the feature Parquet (for the four
anchor columns `row_index, agg_trade_id, feature_timestamp_ms,
source_transact_time_ms`) AND the normalized Parquet (for trade prices). For
the pre-v002 segment, both already exist locally (Phase 4bn-O normalized +
Phase 4bn-S features). Crucially, if `envelope_terminal_unix_ms` is set to the
**pre-v002 segment terminal** (max `transact_time_ms` over 2024-03-01 ..
2024-11-30), forward horizons near 2024-11-30 censor at that boundary and
**never read 2024-12-01+ (v002 terminal) or 2025-02 (sealed-test) data**.

**9.3 Output path / manifest convention (hardcoded to `__v002`).**
`labels_io_v002.py` hardcodes the v002 output layout
`data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-labels-aggtrades-<YYYY-MM-DD>.parquet`
and the single manifest basename
`data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json`,
with canonical Phase 4bb-F sidecars (`<sha256>␠␠<basename>\n`),
refuse-to-overwrite, and atomic write-then-rename. There is **no**
segment-scoped path helper analogous to the Phase 4bn-S feature
`…__v002_pre_v002_segment_4bn_s` directory.

**9.4 Orchestrator (hardcoded to the published v002 family).**
`scripts/phase4bm_o_compute_multiday_labels.py` hard-binds **15 locked
precondition (path, SHA256) pairs** to the *published* v002 family — the
published feature manifest `…features…__v002.json`
(`512a0a54…`), the **Phase 4bm-L Stage-5 research-use successor-state**
(`7eccaa8f…`), the Phase 4bm-J feature gate report (`3c59dfae…`), the v002
derived/raw manifests, the Phase 4bm-F/D derived successor-state/gate, and
the Phase 4bl-E/D-R raw lineage — plus a hard assertion
`EXPECTED_FEATURE_CONFIG_HASH == 819cfa7a…` and the v002 date constants
`LABEL_UTC_DATE_START_V002="2024-12-01"`,
`LABEL_UTC_DATE_END_V002="2025-02-28"`, `LABEL_DATE_COUNT_V002=90`,
`LABEL_EXPECTED_ROW_COUNT_V002=155_153_449`. The `label_config_hash` it builds
incorporates `source_feature_successor_state_sha256` = the Stage-5
successor-state SHA.

**9.5 Label gate (path-parameterized, but v002-lineage-shaped).**
`multiday_label_gate.py` (Phase 4bm-Q) accepts paths via
`MultidayLabelGateInput`, but that dataclass *requires* the v002 lineage set —
including `phase_4bm_l_successor_state_path` (Stage-5),
`phase_4bm_j_gate_report_path`, `phase_4bm_f_successor_state_path`,
`phase_4bm_d_gate_report_path`, etc. — and writes under
`data/microstructure/gate-reports/labels/`. Its check suite is shaped to the
v002 envelope lineage.

**9.6 Established pre-v002 pattern.** Every prior pre-v002 layer (4bn-O
normalize, 4bn-P normalized-gate, 4bn-S features, 4bn-T feature-gate) created
a **new bounded `phase4bn_*` script** that reuses the shared kernel/validation
modules with segment-scoped preconditions, paths, and a segment-scoped
manifest — rather than reusing the hardcoded v002 multiday orchestrators. The
label layer must follow the same pattern.

## 10. Future label input boundary

A future label-only execution may read, by convention and only after separate
authorization:

- **Feature input (required):** the Phase 4bn-S pre-v002 feature segment only —
  the 275 feature Parquet under
  `data/microstructure/features/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s/BTCUSDT/<YYYY>/<MM>/`,
  covering 2024-03-01 .. 2024-11-30 inclusive UTC, plus their sidecars and the
  segment feature manifest (SHA256 `4881eb87…b52`). Only the four anchor
  columns `row_index, agg_trade_id, feature_timestamp_ms,
  source_transact_time_ms` are needed from each feature Parquet.
- **Normalized input (required for prices):** the Phase 4bn-O pre-v002
  normalized segment only — the 275 normalized Parquet under
  `…/normalized/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o/BTCUSDT/<YYYY>/<MM>/`,
  same date range, plus their sidecars and the segment normalized manifest
  (SHA256 `0e96ae37…d9fa`), for anchor/reference `trade_price`.
- **Predecessor gate / lineage (by reference, read-only):** Phase 4bn-T
  feature-layer gate report (`db731d1b…`) and Phase 4bn-P normalized-layer
  gate report (`3452fd9d…`).

**By reference only (must NOT be read for content):** the published v002
feature / normalized / raw families and manifests; the v002 terminal raw and
normalized windows (2024-12-01 .. 2025-02-28); the **sealed test split
2025-02-14 .. 2025-02-28**.

**Conservative envelope rule (binding recommendation):** label only the
pre-v002 segment first, with `envelope_terminal_unix_ms` = max
`transact_time_ms` over the pre-v002 segment (terminal at 2024-11-30). Do
**not** read v002-terminal or sealed-test dates for horizons, context, or
terminal outcome windows. If any future design would require forward context
after 2024-11-30 (e.g. to avoid censoring the last ≤60 s of 2024-11-30 by
stitching into 2024-12-01), it must **fail closed** and require a separately
authorized **holdout-boundary memo** first (see §13). If label computation
were ever to require price/stop/exit information not present in the feature +
normalized segment, it must require a separate design memo before execution.

## 11. Future label output contract

- **Output family:** label artefacts only. **No** ML outputs, diagnostics,
  strategy signals, backtest/PnL outputs, research matrices, or
  `data/research/` outputs.
- **Output storage:** the existing `data/microstructure/labels/` convention,
  but under a **segment-scoped directory** mirroring Phase 4bn-S, e.g.
  `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002_pre_v002_segment_<label-phase-id>/BTCUSDT/<YYYY>/<MM>/BTCUSDT-labels-aggtrades-<YYYY-MM-DD>.parquet`
  — **not** the existing hardcoded `…__v002/…` path (which is reserved for the
  published v002 label family and whose single manifest basename already
  exists locally, so reuse would hit refuse-to-overwrite). The exact segment
  suffix and directory/manifest naming is one of the items the §18 memo must
  settle.
- **Format:** Parquet canonical (the repo convention), one per-day label
  Parquet per source date, schema exactly `LABEL_SCHEMA_V002` (40 columns) in
  canonical order, with the forbidden-substring guard enforced.
- **Sidecars:** one canonical Phase 4bb-F `.sha256` sidecar per Parquet and
  per manifest (`<sha256>␠␠<basename>\n`).
- **Manifest:** exactly one **new, non-eligible** label segment manifest +
  sidecar, `research_eligible=false`, `eligibility_gate_status=pending`,
  `no_successor_authorization=true`, governance labels forbidding
  feature/strategy/ML use.
- **Prohibited:** no database (DuckDB/SQLite/`.duckdb`/`.sqlite`); no Parquet
  compaction; no v003; no overwrite of any existing artefact; no commit of any
  `data/microstructure/` or `data/research/` artefact.

## 12. Label manifest and versioning considerations

The existing v002 label manifest/versioning shape **does not map cleanly** to
the non-eligible, successor-state-free pre-v002 segment. Specifically:

1. **`label_config_hash` lineage mismatch.** `build_label_config_hash_v002`
   requires `source_feature_successor_state_sha256` (a 64-hex value), and the
   v002 orchestrator feeds it the **Phase 4bm-L Stage-5 research-use
   successor-state** SHA. The pre-v002 feature segment has **no
   successor-state** — it is non-eligible (`research_eligible=false`,
   `eligibility_gate_status=pending`) with only the Phase 4bn-T gate PASS.
   What value the segment's `label_config_hash` should bind in that slot (the
   Phase 4bn-T feature gate report SHA? the Phase 4bn-P normalized gate SHA?
   a sentinel? a re-specified field set?) is **undecided**.
2. **Lineage columns reference absent artefacts.** `LABEL_LINEAGE_COLUMNS_V002`
   includes `source_phase_4bm_j_gate_report_sha256`,
   `source_feature_successor_state_sha256`, and the v002 manifest builder
   additionally records Phase 4bm-L/F/D and Phase 4bl-E/D-R lineage — none of
   which exist for the pre-v002 segment (whose lineage is Phase 4bn-T / 4bn-P /
   4bn-O instead). A segment manifest needs a re-mapped lineage field set.
3. **Envelope terminal differs.** The v002 `envelope_terminal_unix_ms` is the
   2025-02-28 v002 terminal; the segment must lock a **pre-v002 terminal**
   (2024-11-30), which changes the per-horizon censoring footprint materially
   and is part of the hash-locked policy.
4. **Naming / shape choice.** Following the Phase 4bn-R precedent (which
   settled the *feature* manifest as a **phase-scoped pre-v002 segment manifest
   tied to the existing v002 family; no v003; full envelope by reference
   only**), the analogous label choice is a **phase-scoped pre-v002 label
   segment manifest** named
   `microstructure_labels_aggtrades_v001__v002_pre_v002_segment_<label-phase-id>.json`.
   But that precedent did **not** resolve the label-specific
   `label_config_hash` / successor-state question above.

Phase 4bn-R settled feature manifest/versioning, **not** label
manifest/versioning. Because items 1–3 are genuine, label-specific design
decisions not settled by any committed memo, the manifest/versioning shape is
**ambiguous** and should be settled by a **docs-only label manifest /
versioning memo before any label execution** (decision §18; preferred option
per the phase's own preference logic when manifest/versioning is ambiguous).

## 13. Sealed-test / v002 terminal boundary

- **Sealed test split:** 2025-02-14 .. 2025-02-28 — **untouched** and must
  remain untouched. It is **outside** the pre-v002 segment (2024-03-01 ..
  2024-11-30) for both input and, under the conservative envelope rule, for
  outcome/context. No label input date, and no in-envelope forward reference,
  falls in the sealed-test window.
- **v002 terminal window:** 2024-12-01 .. 2025-02-28 — by reference only,
  **unread**. Under the conservative envelope rule (envelope terminal =
  pre-v002 segment terminal at 2024-11-30), forward horizons (max 60 s) near
  2024-11-30 **censor at the segment terminal** rather than reading any
  2024-12-01+ row.
- **Boundary verdict:** **CLEAR and safe — no holdout-boundary memo is
  required** for the conservative pre-v002-only label execution, *provided*
  the future wrapper locks the envelope terminal to the pre-v002 segment and
  never stitches forward references into the v002 terminal or sealed-test
  windows. A holdout-boundary memo becomes **required** only if a future
  design instead wants to read v002-terminal or sealed-test dates for label
  horizons / context / terminal outcomes; in that case the label phase must
  fail closed and that memo must precede it.

## 14. Future label budget and preflight requirements

The future label phase inherits the Phase 4bn-L caps in §7. Before writing any
output it must measure and record:

1. D: free space (must be ≥ 500 GiB).
2. Estimated label output footprint (must be < 125 GiB; warn ≥ 75 GiB).
3. Estimated temporary-workspace footprint (must be < 100 GiB; warn ≥ 50 GiB).
4. Estimated total derived-stack footprint (must be < 300 GiB; warn ≥ 250 GiB).
5. Estimated runtime (must be < 8 h; warn ≥ 4 h).
6. Exact input feature date coverage expected (2024-03-01 .. 2024-11-30; 275
   dates).
7. Exact output partition count expected (275 per-day label Parquet + 275
   sidecars + 1 segment manifest + 1 manifest sidecar).
8. Whether any v002 terminal feature/normalized/raw date will be read or treated
   by reference (must be **by reference only**).
9. Whether sealed-test dates fall in the label input range or in the
   outcome/context range (must be **neither**).
10. Whether any label horizon requires forward context beyond the pre-v002
    segment terminal (if yes → fail closed; require holdout-boundary memo).
11. Whether any label computation requires data not present in the approved
    feature + normalized segment (if yes → fail closed; require design memo).
12. Whether a separate holdout-boundary memo is required before touching
    sealed-test or v002 terminal dates (default: not required under the
    conservative envelope rule; required if §13 escalation triggers).
13. Whether a label manifest/versioning memo is required before execution
    (per this memo: **yes** — see §18).

**Footprint expectation (informational, not authorization):** the pre-v002
feature footprint is ≈50.53 GiB over 400,001,695 rows; the label schema is
40 narrow columns (mostly int64/float64/bool/flags + per-row constant lineage
strings) over the same row count, so a naive estimate sits within the 75 GiB
warning / 125 GiB hard-cap envelope — but the future preflight must measure,
not assume, and stop before writing if any cap would be exceeded.

## 15. Future label execution requirements

If separately authorized later, the label derivation must:

- read **only** approved feature + normalized segment input dates (and any
  separately approved source inputs);
- write **only** approved label artefacts under the segment-scoped gitignored
  `data/microstructure/labels/…__v002_pre_v002_segment_<label-phase-id>/…`
  path;
- create canonical Phase 4bb-F `.sha256` sidecars for every Parquet and
  manifest;
- create only a **new non-eligible** label segment manifest + sidecar;
- **refuse overwrite** of any existing file (atomic write-then-rename);
- record exact commands, footprint, runtime, per-day and total counts, paths,
  hashes, label schema, label family, `label_config_hash`, and
  `envelope_terminal_unix_ms`;
- measure at day / month boundaries;
- clean temporary files on success or on fail-closed stop;
- re-hash all upstream artefacts post-write to confirm byte-identical
  immutability (Phase 4aw `flip_research_eligible(...)` always-raises invariant
  preserved; never invoked);
- leave all outputs non-eligible (`research_eligible=false`,
  `eligibility_gate_status=pending`);
- commit **no** data artefact; create **no** ML outputs, diagnostics, research
  outputs, strategy outputs, PnL/backtests, databases, v003, or compacted
  Parquet.

## 16. Future fail-closed stop conditions

A future label phase must fail closed (abort before writing the label
manifest) on at least:

1. Missing feature segment prerequisite.
2. Missing feature sidecar prerequisite.
3. Feature Parquet hash mismatch.
4. Feature path outside approved BTCUSDT aggTrades feature conventions.
5. Missing Phase 4bn-T feature-layer gate PASS predecessor.
6. Source feature segment not `research_eligible=false`.
7. Source feature segment not `eligibility_gate_status=pending`.
8. Any date outside the authorized label range (2024-03-01 .. 2024-11-30).
9. Any ambiguity about whether to read existing v002 terminal / sealed-test
   dates.
10. Any attempt to use sealed-test data for ML, diagnostics, strategy,
    research, tuning, or split policy.
11. Any label requiring a horizon that crosses into sealed-test dates without a
    separately authorized holdout-boundary memo.
12. Any label requiring v002 terminal dates without a separately authorized
    holdout-boundary memo.
13. Any label requiring missing source data.
14. Preflight cannot estimate label output footprint.
15. Preflight label output estimate exceeds 125 GiB.
16. Preflight total derived-stack estimate exceeds 300 GiB.
17. D: free space below 500 GiB before execution.
18. D: free space below 350 GiB during execution.
19. Temporary workspace exceeds 100 GiB.
20. Runtime exceeds 8 hours.
21. Any output path outside approved gitignored
    `data/microstructure/labels/` conventions.
22. Any attempt to create `data/research/` output.
23. Any attempt to run ML, diagnostics, strategy, PnL, or backtests.
24. Any attempt to create DuckDB / SQLite / database files.
25. Any attempt to compact Parquet.
26. Any attempt to create v003.
27. Any attempt to flip `research_eligible`.
28. Any attempt to transition `eligibility_gate_status` to eligible.
29. Any attempt to commit `data/microstructure` or `data/research`.
30. Any need for ETHUSDT, mark-price, spot, cross-venue, order-book, tick, or
    extra-horizon data not already in committed label policy.
31. Any deviation from BTCUSDT / Binance USDⓈ-M futures / aggTrades /
    v002-compatible semantics.
32. Any missing or ambiguous label manifest/versioning convention.
33. Any inability to create canonical sidecars.
34. Any validator/tooling unsafe condition.
35. Any label column name implying strategy, signal, PnL, model, score,
    prediction, backtest, or diagnostics (forbidden-substring guard).
36. Any label computation that leaks beyond the authorized horizon/context
    boundary.
37. Any label computation that requires the sealed test split.

## 17. Label tooling readiness assessment

**Classification: reusable only through a bounded new wrapper.**

Point-by-point:

- **Hardcoded to the old 90-day v002 window?** Yes — the orchestrator
  `phase4bm_o_compute_multiday_labels.py` hardcodes
  `LABEL_UTC_DATE_START_V002="2024-12-01"` .. `…END="2025-02-28"`,
  `LABEL_DATE_COUNT_V002=90`, `LABEL_EXPECTED_ROW_COUNT_V002=155_153_449`, 15
  locked precondition SHAs, and `EXPECTED_FEATURE_CONFIG_HASH=819cfa7a…`.
- **Expects the published `__v002` manifest?** Yes — it binds
  `…features…__v002.json` (`512a0a54…`) and the single label manifest basename
  `…labels…__v002.json`; the pre-v002 segment manifest
  (`…__v002_pre_v002_segment_4bn_s.json`, `4881eb87…`) is path- and
  hash-disjoint.
- **Assumes full-envelope labels?** Yes — `envelope_terminal_unix_ms` is the
  full v002 envelope terminal; the segment needs the pre-v002 terminal.
- **Touches ML / diagnostics / returns-as-strategy / strategy / research
  outputs?** No — the kernel produces only causal forward-return / direction +
  support columns; there is no ML, diagnostics, strategy, or `data/research`
  write in the label modules.
- **Creates `data/research/` outputs?** No — label outputs go only under
  `data/microstructure/labels/`.
- **Enforces sidecars and manifests?** Yes — canonical Phase 4bb-F sidecars,
  atomic write-then-rename, refuse-to-overwrite, and a multi-day manifest +
  sidecar.
- **Enforces Phase 4bn-L budgets?** No — the existing orchestrator has no
  footprint / runtime / D:-free-space preflight; a new wrapper must add the §14
  preflight and the §7 caps.
- **Protects sealed-test and v002 terminal boundaries?** Partially — the
  envelope-terminal censoring is the mechanism that *can* protect the boundary,
  but only if the wrapper sets the envelope terminal to the pre-v002 terminal;
  the existing orchestrator instead binds the v002 terminal. A new wrapper must
  set and assert the pre-v002 terminal.
- **Tests cover the pre-v002 feature segment shape?** No — the committed
  `test_labels_*` / `test_multiday_label_gate_*` suites are shaped to the v002
  family; new offline tests are required for a segment wrapper/gate.
- **Compatible with v1/V2/G1/C1 hard-reject / no-rescue constraints?** Yes —
  labels are a research artefact, carry no strategy/signal/PnL semantics, and
  do not revive any hard-rejected family; they neither rescue nor re-open V2 /
  G1 / C1 / F1 / D1-A verdicts.
- **Useful as a research artefact even with no ML/strategy authorized?** Yes —
  a non-eligible label segment is a legitimate, governance-bounded research
  artefact (forward returns/directions with explicit censoring), independent of
  any future ML or strategy authorization.

**Conclusion:** the label **kernel / schema / validation / gate-check
modules** are reusable, but a future label phase must add a **bounded new
`phase4bn_*` wrapper script + a segment-scoped gate + segment-scoped path /
manifest helpers + new offline tests**, exactly as the pre-v002 normalize
(4bn-O) and feature (4bn-S) layers did. The orchestrator and gate cannot be
reused directly.

## 18. Decision

**`RECOMMEND_AUTHORIZE_DOCS_ONLY_LABEL_MANIFEST_VERSIONING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.**

Rationale, grounded in committed evidence:

- The label **tooling** is *reusable only through a bounded new wrapper*
  (§17), which is acceptable and matches the established pre-v002 pattern —
  this alone does not block a future label execution.
- The sealed-test / v002-terminal **boundary** is *clear and safe* under the
  conservative envelope rule (§13) — so a holdout-boundary memo is **not**
  required, and decision option 4 is not selected.
- The label **manifest / versioning** shape is *genuinely ambiguous* (§12):
  the v002 `label_config_hash` and lineage model bind a Stage-5 feature
  successor-state and Phase 4bm-J/L/F/D lineage that the non-eligible,
  successor-state-free pre-v002 segment does not have, and the envelope
  terminal and segment naming must be re-specified. Phase 4bn-R settled the
  *feature* manifest, not the *label* manifest.

Per the phase's own preference logic — *"Preferred decision if the future
label manifest/versioning shape is ambiguous:
RECOMMEND_AUTHORIZE_DOCS_ONLY_LABEL_MANIFEST_VERSIONING_MEMO"* — the correct,
conservative next step is to authorize a docs-only label manifest/versioning
memo that locks the segment label family naming, the `label_config_hash`
field set for a non-eligible successor-state-free segment, the re-mapped
lineage columns, and the pre-v002 envelope terminal — **before** any label
execution. Label-only execution (option 2) remains the *preferred follow-on
after* that memo settles the shape, but is **not** recommended directly from
this state.

This memo authorizes **none** of: label execution, the manifest/versioning
memo itself, a holdout-boundary memo, ML, diagnostics, strategy, or any
successor. Each requires separate operator authorization after this branch is
merged.

## 19. Recommended state and successor options

**Recommended state: remain paused.** No successor is authorized from inside
Phase 4bn-U.

The decision options considered were:

1. `RECORD_LABEL_DERIVATION_READINESS_PLAN__REMAIN_PAUSED` — viable but
   under-informative given the clear next step identified.
2. `RECOMMEND_AUTHORIZE_LABEL_ONLY_EXECUTION__…` — *preferred follow-on, but
   premature* until the manifest/versioning shape is settled.
3. **`RECOMMEND_AUTHORIZE_DOCS_ONLY_LABEL_MANIFEST_VERSIONING_MEMO__…` —
   selected (§18).**
4. `RECOMMEND_AUTHORIZE_DOCS_ONLY_HOLDOUT_BOUNDARY_MEMO__…` — not selected;
   boundary is clear/safe under the conservative envelope rule (§13).
5. `RECOMMEND_AUTHORIZE_SOURCE_POLICY_DOCUMENTATION_MEMO__…` — not needed;
   source policy (BTCUSDT / Binance USDⓈ-M futures / aggTrades) is settled.
6. `RECOMMEND_AUTHORIZE_PROCESS_DOC_PATH_UPDATE__…` — not needed by this phase.
7. `RECOMMEND_CLOSE_ML_BASELINE_ARC__…` — not selected; evidence does not
   warrant closing the arc.

**Suggested operator options after the branch-complete report:** remain
paused; request a merge prompt for Phase 4bn-U; separately authorize the
docs-only label manifest/versioning memo; (only after that memo) separately
authorize label-only execution; or separately authorize a holdout-boundary
memo only if a future design needs v002-terminal / sealed-test dates.

## 20. Explicit non-authorizations

Phase 4bn-U did **not**, and does **not** authorize: label derivation; label
artefact / manifest creation or mutation; feature / feature-gate /
normalization / normalized-gate / raw rerun; acquisition; any public,
authenticated, or private endpoint call; `data.binance.vision` contact;
archive / CHECKSUM downloads; HEAD preflight; any local raw / normalized /
feature / label / gate-report / manifest read under `data/microstructure`;
any `data/research` read or write; any v002 terminal-window read; any
sealed-test read; ML training / model scoring / predictions / feature ranking
/ feature selection / feature pruning; label optimization / threshold tuning /
hyperparameter tuning / calibration fitting; strategy / signals / PnL /
backtests; manifest eligibility transition (`research_eligible`,
`eligibility_gate_status`, `chronological_split_policy`,
`diagnostics_authorized`, `ml_authorized`); storage migration; DuckDB /
SQLite / `.duckdb` / `.sqlite` creation; Parquet compaction; v003 creation;
ETHUSDT / mark-price / spot / cross-venue / order-book / tick data; paper /
shadow / live-readiness / deployment / exchange-write / production keys; MCP /
Graphify / `.env` / `.mcp.json`; Phase 5; or any successor phase. All retained
verdicts (H0, R3, R1a, R1b-narrow, R2, F1, D1-A, 5m thread, V2, G1, C1) and
all project locks (§11.6 8 bps/side, round-trip 16 bps, §1.7.3, the Phase 3/4
governance chain, Phase 4ak M0, Phase 4al no-rescue, Phase 4aw
`flip_research_eligible(...)` always-raises invariant, Phase 4bb-F canonical
path policy, Phase 4bl-F risk tiers, Phase 4bn-L budgets, Phase 4bn-R feature
manifest policy) are preserved verbatim.

## 21. Current-project-state update summary

`docs/00-meta/current-project-state.md` received a single narrow update: a new
Phase 4bn-U entry appended to the compact phase ledger and a new
`Current phase:` block placed ahead of the Phase 4bn-T block. All prior
paragraphs and `Current phase:` blocks are preserved verbatim as labelled
historical context. No other section of that document, and no other tracked
file outside the two Phase 4bn-U report files, was modified.
