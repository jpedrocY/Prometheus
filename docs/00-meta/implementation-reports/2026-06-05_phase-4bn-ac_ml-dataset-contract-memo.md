# Phase 4bn-AC — ML Dataset Contract Memo

## 1. Purpose

This memo records, **by reference only**, the binding contract that any future
pre-v002 ML dataset builder must obey before it may be separately authorized,
implemented, or run. It defines the allowed and forbidden source scope, the
split binding, the target and feature scope, the excluded columns, the
filtering and alignment rules, the leakage / split-integrity proof obligations,
the train-only transform obligations, the budget-preflight obligations, the
output-namespace posture, the manifest / hash / gate-report binding, the
validation a future builder must carry, and the explicit non-authorization
boundaries.

This phase is **docs-only**. It reads no local data, creates no local data,
adds no code / tests / scripts, creates no split file / research matrix / ML
dataset / ML config / manifest / gate report / sidecar, transitions no manifest
field, and authorizes no successor. It defines a contract the way a
specification defines an interface: future tooling may depend on it, but nothing
is built or run here.

The contract is the conservative **pre-v002-only** path established by the
Phase 4bn-O/P/S/T/W/X local layer-integrity work, the Phase 4bn-Y chronological
split policy, the Phase 4bn-Z ML-baseline readiness verdict, the Phase 4bn-AA
pure split-policy artefact, and the Phase 4bn-AB source-admissibility posture
(`source_admissible_for_dataset_contract = true`).

---

## 2. Authority and repository state

- **Authorized by:** the operator, following the Phase 4bn-AB decision
  `RECOMMEND_AUTHORIZE_ML_DATASET_CONTRACT_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Branch:** `phase-4bn-ac/ml-dataset-contract-memo`.
- **Base `main` SHA:** `46bcdd3862c2b82b268d668f1e2d0180243f0dce`
  (`docs(phase-4bn-ab): finalize merge closeout shas`).
- **Pre-branch sync:** `HEAD == main == origin/main == 46bcdd38…` verified.
- **Predecessor chain on `main`:** Phase 4bn-AB SHA-finalization `46bcdd3`,
  merge-closeout `1d032a4`, merge `d200a8b`, branch `80e032c`; Phase 4bn-AA
  finalization `e749598` present.
- **Remote:** `https://github.com/jpedrocY/Prometheus.git`.
- **Gitignored namespaces:** `data/microstructure/` (`.gitignore:85`),
  `data/research/` (`.gitignore:88`).
- **Working-tree:** only expected untracked transient
  `.claude/scheduled_tasks.lock`.

---

## 3. Phase type and strict scope

- **Phase type:** docs-only / ML dataset contract / pre-v002 source-binding /
  target-feature-filtering / leakage-proof / budget-preflight / no-data-read
  memo.
- **Tier:** Tier 1 — Full Phase per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3, because it defines
  the binding contract any future pre-v002 ML dataset builder must obey
  (targets, admissible features, excluded columns, filtering, split binding,
  manifest/hash/gate binding, leakage-proof obligations, budget-preflight
  obligations, output namespace, non-authorization boundaries). An error here
  could cause downstream leakage, misaligned labels/features, accidental data
  reads, or invalid ML claims — even though this phase is docs-only and reads no
  data.

**Strict scope (all enforced):** no code, no tests, no scripts, no data read,
no data created, no inspection of any file under `data/microstructure/` or
`data/research/`, no inspection of raw zip / normalized / feature / label
Parquet / manifest / gate report / sidecar, no v002-terminal read, no
sealed-test read, no split file, no research matrix, no ML dataset, no ML
config, no manifest, no gate report, no sidecar, no training, no scoring, no
prediction, no diagnostics, no strategy / signals / PnL / backtests, no
`research_eligible` flip, no `eligibility_gate_status` transition, no
`chronological_split_policy` set, no invocation of the Phase 4aw
`flip_research_eligible(...)` always-raises invariant, no successor
authorization.

---

## 4. Evidence base and input boundary

This memo was written from **committed docs + committed source/tests only**.
No local artefact under `data/microstructure/` or `data/research/` was read or
inspected. The README is treated as potentially stale and is **not** used as a
current-state authority.

Committed source grounding (read-only, for contract precision):

- `src/prometheus/research/microstructure/pre_v002_split_policy.py` — the Phase
  4bn-AA split artefact; public API and exact Candidate A windows.
- `src/prometheus/research/microstructure/features_schema_v002.py` and its v001
  base `features_schema.py` — the 17 lineage + 45 feature/quality columns and
  the forbidden-substring guard.
- `src/prometheus/research/microstructure/labels_schema_v002.py` — the 40-column
  label schema (17 lineage + `label_config_hash` + 8 labels + 14 support),
  horizons, direction-threshold policy, null/censoring policy.
- `src/prometheus/research/microstructure/ml_baseline_design_v002.py` — the
  Phase 4bn-B locked design constants (frozen 45-column matrix, excluded 17
  lineage, `FORBIDDEN_MODEL_MATRIX_SUBSTRINGS`, train-only transform rules,
  3-class signed framing) — reused **as column/contract precedent only**; its
  identity is bound to the **v002 terminal** envelope and is **not** the
  pre-v002 binding (see §10).
- `tests/research/microstructure/test_phase4bn_aa_pre_v002_split_policy.py` —
  the split-artefact contract tests.

Committed docs grounding: the process standards
(`merge-closeout-standard`, `phase-risk-tiering-standard`,
`phase-workflow-standard`, `phase-prompt-template`, `operator-report-standard`)
and the Phase 4bn-L/O/P/S/T/W/X/Y/Z/AA/AB implementation reports and closeouts.

**Carried-forward numeric evidence** (from committed reports; not re-derived by
reading data here):

- Normalized (4bn-O): 2024-03-01..2024-11-30 inclusive UTC; 275 Parquet;
  400,001,695 rows; footprint 3,954,532,918 B; manifest SHA256
  `0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa`;
  `research_eligible=false`; `eligibility_gate_status=pending`.
- Normalized-layer gate (4bn-P):
  `NORMALIZED_LAYER_GATE_PASSED__LOCAL_NORMALIZED_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`;
  25/25 PASS; report SHA256
  `3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134`.
- Feature (4bn-S): 275 Parquet; 400,001,695 rows; footprint 54,254,406,538 B;
  manifest SHA256
  `4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52`;
  `feature_config_hash`
  `0726b41d48e5f7127728c385b150d90fad91a92b3400c0545649b541e4dd114c`;
  `research_eligible=false`; `eligibility_gate_status=pending`.
- Feature-layer gate (4bn-T):
  `FEATURE_LAYER_GATE_PASSED__LOCAL_FEATURE_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`;
  27/27 PASS; report SHA256
  `db731d1be06295404ef195d9b5b5bad8010ce6ae6efef43ece90c29653d6ab08`.
- Label (4bn-W): 275 Parquet + 275 sidecars; 400,001,695 rows; footprint
  15,654,082,679 B; manifest SHA256
  `69746c88860bff2de197dca0841dc2c6e439a93b06ba4dac9f58312b95e1b161`; manifest
  sidecar SHA256
  `636a4c1a0159364e7d67f502dda48664f18fc16545c993935e6429ccdf868239`;
  `label_config_hash`
  `b3bd5d2b332e9f4b4a6bbf76de533f48993b4d0500e4aab90087404b51558970`;
  `envelope_terminal_unix_ms 1733011199331`
  (`envelope_terminal_utc_date 2024-11-30`); censored counts 1s=3 / 5s=20 /
  15s=42 / 60s=216; invalid-price rows 0; `research_eligible=false`;
  `eligibility_gate_status=pending`; `no_successor_authorization=true`.
- Label-layer gate (4bn-X):
  `LABEL_LAYER_GATE_PASSED__LOCAL_LABEL_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`;
  40/40 PASS; report SHA256
  `ffb5b09215d6efd9b34c3a625421a367c9587b63027c59f2fc9d5c59797a8984`; report
  sidecar SHA256
  `68dd5b5709bb523003ed183ac776e95ad1c82a40deb65e3cda51b2e10e51997c`.

---

## 5. Phase 4bn-AB admissibility posture carried forward

The Phase 4bn-AB source-admissibility verdict is carried verbatim and governs
this contract:

| Term | Value |
|---|---|
| `layer_integrity_passed` | **true** |
| `source_admissible_for_dataset_contract` | **true** |
| `source_admissible_for_data_read` | **false / not yet** |
| `source_admissible_for_dataset_builder` | **false / not yet** |
| `ml_authorized` | **false** |
| `diagnostics_authorized` | **false** |
| `strategy_backtest_authorized` | **false** |
| `manifest_research_eligible` | **false (unchanged)** |
| `manifest_eligibility_gate_status` | **pending (unchanged)** |
| `manifest_chronological_split_policy` | **not set (unchanged)** |

Because `source_admissible_for_dataset_contract = true` while
`source_admissible_for_data_read = false`, Phase 4bn-AC may define the dataset
contract **by reference only**. It may not read data and may not build the
dataset. The Phase 4aw `flip_research_eligible(...)` invariant forbids flipping
the manifest `research_eligible` field outside a future separately-authorized
eligibility gate; a docs-only contract grants no data access and mutates no
manifest, so it does not invoke or alter that invariant.

---

## 6. Dataset-contract question

This memo answers the following, by reference only:

1. **What may a future pre-v002 ML dataset builder read if separately authorized
   later?** Only the pre-v002 feature segment (4bn-S) and label segment (4bn-W)
   for BTCUSDT / Binance USDⓈ-M futures / aggTrades over 2024-03-01..2024-11-30
   (275 dates), with normalized (4bn-O) lineage by reference — and only after a
   **separate** data-read / builder authorization that does not exist yet.
2. **What is it forbidden to read?** The v002 terminal (2024-12-01..2025-02-28),
   the sealed test (2025-02-14..2025-02-28), any full-envelope assembly, any
   non-BTCUSDT symbol, any other data family, any newly acquired or external
   data, any raw zip, and anything under `data/research` from prior experiments.
3. **Which target family / columns / horizons / initial task?** Family
   `microstructure_labels_aggtrades_v001 @ v002`; primary first-baseline target
   `forward_direction_15s` (3-class signed `{-1, 0, +1}`, zero preserved);
   horizons `{1s, 5s, 15s, 60s}` contract-known but multi-horizon deferred.
4. **Which feature columns are allowed?** Exactly the 45 causal computed
   `FEATURE_SCHEMA_V002` columns.
5. **Which columns are forbidden from the model matrix?** The 17 lineage
   columns, all label columns, all support columns, all split/censor columns,
   raw prices, and any future-looking/post-label/strategy/PnL column.
6. **How are censored/null/invalid targets handled?** Dropped (never imputed)
   for the active horizon, per split, before the model matrix is built.
7. **How is the 4bn-AA split artefact used?** Imported and used as the sole
   split authority (`split_for_timestamp_ms` / `split_for_date`); embargo dates
   dropped; out-of-segment / v002 / sealed dates hard-raise.
8. **What proof must a future builder emit?** A machine-checkable leakage /
   split-integrity proof (§19).
9. **What budget preflight must it satisfy?** The Phase 4bn-L caps, fail-closed
   (§20).
10. **What output namespace / sidecar policy?** Local + gitignored under
    `data/research/microstructure/ml_datasets/pre_v002_contract_v001/`, with a
    Phase 4bb-F canonical sidecar for every output (§21).
11. **What remains blocked before any data read?** Everything: there is no
    data-read authorization, no dataset-builder authorization, no ML
    authorization (§23–§25).
12. **What should the next safest phase be?** A docs-only or readiness-focused
    successor (preferred: an ML dataset builder readiness memo), not a
    data-reading builder (§26–§27).

---

## 7. Dataset contract name and scope

- **Dataset-contract working name:**
  `microstructure_ml_dataset_aggtrades_pre_v002_contract_v001`.

This is a **docs-level contract name only**. No dataset, dataset config file,
manifest, sidecar, or manifest field is created or set by this phase. The name
exists so that a future, separately-authorized builder phase has a stable
reference to this contract.

- **Symbol / market / instrument:** BTCUSDT; Binance USDⓈ-M futures; aggTrades.
- **Segment:** pre-v002 only, 2024-03-01..2024-11-30 inclusive UTC (275 dates;
  400,001,695 rows by reference).
- **Schema basis:** features = `FEATURE_SCHEMA_V002` (62 cols = 17 lineage + 45
  feature/quality); labels = `LABEL_SCHEMA_V002` (40 cols = 17 lineage +
  `label_config_hash` + 8 labels + 14 support).

---

## 8. Permitted source scope

A future builder, **if separately authorized**, may read **only**:

- **Feature source — Phase 4bn-S segment (by reference):** manifest SHA256
  `4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52`;
  `feature_config_hash`
  `0726b41d48e5f7127728c385b150d90fad91a92b3400c0545649b541e4dd114c`; bound to
  the Phase 4bn-T feature-layer gate
  `db731d1be06295404ef195d9b5b5bad8010ce6ae6efef43ece90c29653d6ab08` (27/27
  PASS).
- **Label source — Phase 4bn-W segment (by reference):** manifest SHA256
  `69746c88860bff2de197dca0841dc2c6e439a93b06ba4dac9f58312b95e1b161`;
  `label_config_hash`
  `b3bd5d2b332e9f4b4a6bbf76de533f48993b4d0500e4aab90087404b51558970`; bound to
  the Phase 4bn-X label-layer gate
  `ffb5b09215d6efd9b34c3a625421a367c9587b63027c59f2fc9d5c59797a8984` (40/40
  PASS).
- **Normalized lineage — Phase 4bn-O (by reference only, lineage not features):**
  manifest SHA256
  `0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa`; bound to
  the Phase 4bn-P normalized-layer gate
  `3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134` (25/25
  PASS). The normalized layer is used as lineage provenance; the model matrix is
  built from the **feature** segment, not from normalized rows.

Scope: BTCUSDT only; Binance USDⓈ-M futures only; aggTrades only; pre-v002
segment only (2024-03-01..2024-11-30 inclusive UTC; expected 275 feature
partitions and 275 label partitions).

This permission is **contractual, not operational**: it states what a future
builder *would* be allowed to read *if* a data-read/builder authorization were
separately granted. No such authorization exists today.

---

## 9. Forbidden source scope

A future builder is forbidden to read:

- the **v002 terminal** window 2024-12-01..2025-02-28 (raw / normalized /
  feature / label);
- the **sealed test** 2025-02-14..2025-02-28 (must remain `test_rows_loaded=0`);
- any **full-envelope** pre-v002 + v002 combined assembly;
- any **non-BTCUSDT** symbol;
- any spot, mark-price, index-price, order-book, kline, liquidation, funding,
  open-interest, or cross-venue data;
- any **newly acquired** data;
- any **raw zip** direct read;
- any raw / normalized / feature / label family **not already carried** by the
  pre-v002 chain (in particular the published `__v002` 90-day families and their
  hashes `feature_config_hash 819cfa7a…` / `label_config_hash 352bad41…`);
- any data under `data/research` from prior experiments;
- any external source;
- any private / authenticated API endpoint data, WebSocket, or user stream.

Any attempt to read a forbidden source must **fail closed**.

---

## 10. Manifest / hash / gate-report binding

A future builder must verify, before any row-level processing, that the inputs
it reads match exactly the recorded references:

| Layer | Manifest SHA256 | Config hash | Gate report SHA256 |
|---|---|---|---|
| Normalized (4bn-O/P) | `0e96ae37…d9fa` | — | `3452fd9d…f134` (25/25) |
| Feature (4bn-S/T) | `4881eb87…9b52` | `feature_config_hash 0726b41d…114c` | `db731d1b…6ab08` (27/27) |
| Label (4bn-W/X) | `69746c88…b161` (sidecar `636a4c1a…8239`) | `label_config_hash b3bd5d2b…8970` | `ffb5b092…8984` (sidecar `68dd5b57…997c`) (40/40) |

Binding rules:

- The builder must **hash-verify** every Parquet against its canonical
  `.sha256` sidecar and the manifest `per_day_outputs` inventory **before**
  reading any feature/label rows.
- The builder must verify the segment-scoped `feature_config_hash` and
  `label_config_hash` are exactly the pre-v002 values above, and must
  **reject** the published `__v002` 90-day hashes (`819cfa7a…` / `352bad41…`).
- The committed Phase 4bn-B `ml_baseline_dataset_v002.py` / `…_design_v002.py`
  and the Phase 4bm-W `diagnostics_split_policy_v002.py` are **identity-bound to
  the v002 terminal** (90 partitions / 155,153,449 rows / dates
  2024-12-01..2025-02-28 / split `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`)
  and are therefore **inadmissible** to the pre-v002 segment. They may be reused
  only as **column/contract precedent**; a future builder must bind to the
  pre-v002 hashes, the 275-partition counts, and the Phase 4bn-AA split artefact.
- Any manifest/hash/gate mismatch must **fail closed**.

---

## 11. Split-policy binding

A future builder must import and use, as the **sole** split authority,
`src/prometheus/research/microstructure/pre_v002_split_policy.py`
(`SPLIT_POLICY_NAME = "CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO"`),
recording the module path and its commit SHA in the proof.

Split (Phase 4bn-Y Candidate A, exact):

- **Train:** 2024-03-01 .. 2024-09-30 inclusive (214 dates).
- **Embargo:** 2024-10-01 (dropped).
- **Validation:** 2024-10-02 .. 2024-11-15 inclusive (45 dates).
- **Embargo:** 2024-11-16 (dropped).
- **Internal holdout / dry-run (NOT the sealed test):** 2024-11-17 ..
  2024-11-30 inclusive (14 dates).
- **Total:** 214 + 1 + 45 + 1 + 14 = **275** dates.

Rules:

- Assignment by `source_transact_time_ms` UTC date (the policy clock; local
  timezone cannot affect assignment).
- Use `split_for_timestamp_ms` (or `split_for_date`) from the artefact; embargo
  dates return `EMBARGO` and their rows are dropped from every model-eligible
  split.
- Apply the earlier-split boundary protection (`is_earlier_split_boundary_crossing`
  / `earlier_split_embargo_window_ms`): for each active horizon, an earlier-split
  row whose `T + H` reaches the next split boundary is excluded from the earlier
  split; rows are never reassigned forward.
- Hard **raise** (`PreV002SplitPolicyError`) on any out-of-segment date,
  including every v002-terminal date and every sealed-test date.
- **No** random split, **no** shuffle, **no** k-fold-over-time, **no**
  bootstrap, **no** post-hoc temporal resampling. There is no RNG in split
  assignment.

---

## 12. Target and horizon contract

- **Target family:** `microstructure_labels_aggtrades_v001 @ v002`
  (`label_schema_version v001`).
- **Available horizons (contract-known):** `1s`, `5s`, `15s`, `60s`
  (`[1000, 5000, 15000, 60000]` ms), paired with the 8 label columns
  `forward_log_return_{1s,5s,15s,60s}` and `forward_direction_{1s,5s,15s,60s}`.
- **Primary first-baseline target:** **`forward_direction_15s`** — a locked
  **3-class signed direction** target `{-1, 0, +1}` with the **zero class
  preserved** (no binary collapse). Per the committed
  `DIRECTION_THRESHOLD_POLICY_V002`: `+1` iff `forward_log_return_15s` strictly
  positive, `0` iff exactly zero, `-1` iff strictly negative, `null` iff
  `forward_log_return_15s` is null; strict sign threshold at zero log-return; no
  deadband, no bp threshold, no threshold optimization, no cost-based threshold.
- **Secondary descriptive target (NOT a model target):** `forward_log_return_15s`
  may be used for reporting / cost-context summaries only (e.g. magnitude
  versus the locked 16 bps round-trip cost). It must not be used as a regression
  model target.
- **Multi-horizon:** `1s`/`5s`/`60s` remain contract-known but their model use
  is **deferred**. The first baseline is a single narrow horizon.

**Horizon choice — 15s, with rationale (contract choice, not a performance
claim):** the first narrow horizon is **15s** rather than 60s. The repository
evidence supporting 15s over 60s is the Phase 4bn-W/4bn-X terminal-censor
counts: censored rows are 1s=3 / 5s=20 / **15s=42** / **60s=216** at the segment
terminal — the 60s horizon carries ~5× the censored (dropped) rows of 15s, so
60s loses materially more terminal coverage. 15s is also longer than 1s/5s and
therefore less dominated by ultra-micro tie/noise structure. This is a
data-availability and noise-structure argument from committed counts; it is
**not** a claim about predictive performance. If a future phase prefers 60s, it
must justify it explicitly; this contract selects 15s.

**Target non-authorizations (carried into the contract):** no training; no
target experimentation; no multi-horizon model selection; no regression-only
reframing; no binary collapse; no ordinal / meta-labeling; no barrier / stop /
MFE / MAE / R-multiple / PnL labels.

---

## 13. Target filtering contract

Before the model matrix is built, for the active horizon (15s by default):

- **Drop** rows where the active `forward_direction_15s` is **null**.
- **Drop** rows where the active `forward_log_return_15s` is **null** where the
  target schema requires it (direction null ⇔ log-return null at the same
  horizon, by `DIRECTION_THRESHOLD_POLICY_V002`).
- **Drop** rows where the active `horizon_censored_flag_15s` is **true**.
- **Reject** invalid-price rows (`label_invalid_price_flag = true`); the
  pre-v002 segment has **0** such rows by reference, but the rule is mandatory.
- **Never impute** targets.
- Censored / invalid rows must **never** enter train / validation / internal
  holdout.
- The **internal holdout** (2024-11-17..2024-11-30) is a **dry-run only**: it
  must not be used for model selection, hyperparameter tuning, threshold tuning,
  feature selection, or final claims.
- The **sealed test** remains `test_rows_loaded = 0` and fully excluded.

The builder must record dropped-row counts **by split and reason** (null /
censored / invalid) in its proof.

---

## 14. Feature allowlist contract

- **Allowed model-matrix columns:** exactly the **45 causal computed
  `FEATURE_SCHEMA_V002`** feature/quality columns, in canonical order. These are
  40 windowed columns — the 10 per-window templates
  (`rolling_aggtrade_count`, `rolling_quantity_sum`, `rolling_quantity_mean`,
  `rolling_aggressive_buy_quantity`, `rolling_aggressive_sell_quantity`,
  `rolling_aggressive_buy_count`, `rolling_aggressive_sell_count`,
  `rolling_aggressive_flow_ratio`, `rolling_aggressive_quantity_imbalance`,
  `rolling_log_return_past_window`) over the 4 windows `{1s, 5s, 15s, 60s}` —
  plus 3 time-context columns (`utc_hour`, `utc_minute`,
  `milliseconds_since_day_start`) and 2 data-quality flags
  (`invalid_window_flag`, `rolling_missing_window_flag`). This matches the Phase
  4bn-B `COMPUTED_FEATURE_COLUMN_NAMES` (asserted length 45).
- The allowlist is **exact and frozen**: no feature may be added, and the
  per-column dtype handling follows the committed v002 design
  (decimal-as-string columns parsed via float64 cast; boolean flags cast to
  `{0, 1}`; the remainder native numeric).

Feature non-authorizations:

- **Exclude** the 17 `FEATURE_SCHEMA_V002` lineage columns (see §15).
- **Exclude** all label columns, all support columns, all split columns, all
  censor columns.
- **Exclude** raw prices unless a future dataset-contract revision **explicitly**
  authorizes them.
- **Exclude** any future-looking / post-label column.
- **Exclude** any PnL / strategy / signal / prediction / score / model /
  barrier / stop / MFE / MAE / R-multiple field.
- **No** feature selection / ranking / pruning under this contract.
- **No** new features.
- **No** PCA / embedding / learned-representation features.

---

## 15. Forbidden model-matrix columns

The following must **never** appear in the model matrix, even if present in a
Parquet file:

- **The 17 lineage columns** (`EXCLUDED_LINEAGE_COLUMN_NAMES`): `dataset_family`,
  `dataset_version`, `source_dataset_family`, `source_dataset_version`,
  `feature_schema_version`, `symbol`, `utc_date`, `agg_trade_id`, `row_index`,
  `feature_timestamp_ms`, `source_transact_time_ms`,
  `source_normalized_parquet_per_day_sha256`,
  `source_normalized_manifest_sha256`, `source_successor_state_sha256`,
  `source_phase_4bm_d_gate_report_sha256`, `source_phase_4bm_e_outcome`,
  `feature_config_hash`. (Identity/lineage/split-leak signals; the timestamp/id
  columns are used **only** for split assignment and alignment, never as
  features.)
- **Any column matching the forbidden substrings** (`FORBIDDEN_MODEL_MATRIX_SUBSTRINGS`):
  `forward_log_return`, `forward_direction`, `horizon_censored_flag`, `label_`,
  `split_`, `censored_`.
- All label columns, support columns, reference columns, and the global
  `label_invalid_price_flag` / `label_any_censored_flag`.

The builder must run a **forbidden-column substring scan** over the assembled
matrix columns and **fail closed** on any hit, recording the scan result in the
proof. This complements the schema-side forbidden-substring guards
(`assert_no_forbidden_substrings_v002` for features;
`assert_no_forbidden_label_substrings_v002` for labels).

---

## 16. Feature / label alignment contract

A future builder must pair feature and label rows by **strict per-day positional
alignment** and verify identical keys on each paired partition:

- `row_index`;
- `agg_trade_id`;
- `feature_timestamp_ms`;
- `source_transact_time_ms`;
- `symbol` / `utc_date` where present.

Alignment rules:

- **No** join-based repair.
- **No** reordering.
- **No** forward-fill / back-fill.
- **No** tolerance merge.
- **No** duplicate-key resolution by heuristic.
- Any key mismatch (count, value, or order) must **fail closed**.

The feature and label segments share these identity columns by construction (the
label segment anchors on the feature row `R` at `feature_timestamp_ms ==
source_transact_time_ms`), so a correct builder verifies — it does not repair —
the alignment. Strict feature/label key-alignment counts must be recorded in the
proof.

---

## 17. Split / filtering execution order for future builder

The builder must execute in exactly this order:

1. Discover the expected **275** feature partitions and **275** label partitions
   from the manifest references (§10).
2. Verify the manifest / config / gate-report hashes (§10) **before** any
   row-level processing.
3. Pair feature and label partitions by **UTC date**.
4. Verify the **positional alignment keys** within each paired partition (§16).
5. Assign split using `source_transact_time_ms` UTC date and the Phase 4bn-AA
   split artefact (§11).
6. **Drop** embargo dates/rows, and apply the per-horizon earlier-split
   boundary protection.
7. Apply active-horizon **censored / null / invalid** target filtering (§13).
8. Build the model matrix from the **45 allowed feature columns only** (§14),
   running the forbidden-column scan (§15).
9. Fit transforms **only on the train split** (§18).
10. Apply train-fitted transforms to validation and internal holdout (§18).
11. Emit the **proof / sidecar metadata** (§19, §21).
12. Write outputs **only** to the local gitignored output namespace (§21) **if**
    a future builder is separately authorized to create outputs.

---

## 18. Train-only transform contract

- Fit standardization / imputation statistics on the **train split only**.
- Standardization rule (`STANDARDIZATION_RULE`): subtract train-mean and divide
  by `max(train-std, epsilon)` (`STANDARDIZATION_EPSILON = 1e-8`); fitted on
  train, never refit.
- Imputation rule (`IMPUTATION_RULE = fixed_zero_for_null_numeric`,
  `IMPUTATION_FILL_VALUE = 0.0`): fixed-zero imputation for null numeric features
  is permitted because it is the **already-locked v002 design** and is fit-free
  (the `rolling_missing_window_flag` / `invalid_window_flag` columns carry the
  missingness signal). It uses no train statistics.
- **Boolean quality flags are not standardized** (`STANDARDIZE_BOOLEAN_FLAGS =
  false`); they pass through as `{0, 1}`.
- **Never** fit on validation; **never** fit on holdout; **never** fit on the
  sealed test.
- **Never** use validation / holdout / test for feature selection.
- All transform metadata must record **train-only provenance** (which split the
  statistics came from, the rule, the epsilon, the fill value).

---

## 19. Leakage / split-integrity proof contract

A future builder must emit a **machine-checkable proof** (JSON, with a canonical
Phase 4bb-F sidecar) containing at least:

- exact policy name
  (`CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`);
- the split-policy **module path and version / commit SHA**;
- date-assignment counts **214 / 1 / 45 / 1 / 14**;
- no missing in-segment dates; no duplicate in-segment dates; no date assigned to
  more than one split;
- no `EMBARGO` date used for train / validation / holdout;
- **zero** out-of-segment dates;
- `v002_terminal_window_read = false`;
- `sealed_test_split_touched = false`;
- `test_rows_loaded = 0`;
- no random / shuffle / k-fold / bootstrap; deterministic assignment by
  `source_transact_time_ms` UTC date;
- for each active horizon, **zero** earlier-split boundary-crossing rows under
  the Phase 4bn-AA helper;
- strict feature/label **key-alignment counts**;
- target null / censor / invalid **rows dropped, by split**;
- active **feature-column list hash** (over the 45 allowed columns, in order);
- **forbidden-column scan** results (must be empty);
- **train-only transform provenance**;
- **budget-preflight** result (§20);
- non-authorization flags all `false` for ML / diagnostics / strategy / PnL /
  backtest / live / exchange-write (mirroring the Phase 4bn-B
  `NON_AUTHORIZATION_FLAGS`).

---

## 20. Budget-preflight contract

A future dataset-building phase must run the **Phase 4bn-L** budget preflight
**before any write** and **fail closed** if any limit is exceeded:

- derived footprint: **warn 75 GiB / hard 125 GiB**;
- total derived-stack: **warn 250 GiB / hard 300 GiB**;
- runtime: **warn 4 h / hard 8 h**;
- temp: **warn 50 GiB / hard 100 GiB**;
- `D:` free space **≥ 500 GiB before start**;
- **fail closed below 350 GiB during**.

No builder may write any output without **recording** the budget-preflight
result in its proof / run manifest.

---

## 21. Output namespace and sidecar contract

If a future builder is separately authorized to create outputs:

- Outputs must be **local and gitignored only**, under
  `data/research/microstructure/` (`.gitignore:88`).
- Working future-only namespace:
  `data/research/microstructure/ml_datasets/pre_v002_contract_v001/`.
- This directory is **not** created, written, or committed by this phase.
- Every future artefact must carry a **Phase 4bb-F canonical sidecar**
  (two-space `.sha256` sidecar) in the same directory.
- Future outputs must **not** imply research eligibility.
- Future outputs must **not** set `chronological_split_policy` in any source
  manifest.
- Future outputs must **not** transition `ml_authorized` or
  `diagnostics_authorized`.
- The contract does **not** authorize creating this namespace or any output; it
  only specifies where outputs would go **if** separately authorized.

---

## 22. Future builder validation requirements

A future builder implementation must carry **offline tests** for:

- manifest / hash / gate binding;
- partition count **275**;
- date range **2024-03-01 .. 2024-11-30**;
- **v002 / sealed exclusion** (hard-raise);
- split assignment via `pre_v002_split_policy.py`;
- **embargo date dropping**;
- horizon validation;
- target **censor / null / invalid** filtering;
- feature allowlist exactly **45** computed columns;
- **forbidden** model-matrix substring scan;
- **no raw price** unless explicitly authorized;
- strict **positional alignment**;
- **train-only** transform fitting;
- output namespace under `data/research` only;
- sidecar metadata;
- **no data output committed**;
- **no eligibility transition**;
- **no ML / training / diagnostics / strategy**.

A future builder phase must **separately decide** whether to (a) implement
**code-only with synthetic tests first**, or (b) implement **and run on real
data**. Given the current caution, this contract **recommends a
dataset-builder readiness or code-only skeleton phase first**, rather than a
full data-reading builder (see §26–§27).

---

## 23. Remaining blockers before data reads

A data read on the pre-v002 segment remains blocked until **all** of:

- this ML dataset contract is recorded (this phase); **and**
- a code-level dataset builder is implemented and bound to the passed gates
  (`3452fd9d…` / `db731d1b…` / `ffb5b09…`), the manifests/hashes, and the Phase
  4bn-AA split artefact; **and**
- the leakage / split-integrity proof and the Phase 4bn-L budget preflight are
  bound into the builder; **and**
- a **separate operator authorization** for data reads is granted
  (`source_admissible_for_data_read` is currently **false**).

---

## 24. Remaining blockers before dataset builder

A dataset builder remains blocked until:

- a recorded dataset contract (this phase); **and**
- a builder-readiness decision (code-only-first vs data-reading) is made; **and**
- the leakage proof + budget preflight are designed into the builder; **and**
- a **separate operator authorization** for the builder is granted
  (`source_admissible_for_dataset_builder` is currently **false**).

---

## 25. Remaining blockers before ML training

ML training remains blocked until:

- all of §23 and §24; **and**
- a per-task target / horizon / filtering decision is locked (this contract
  selects `forward_direction_15s` as the first target); **and**
- a committed **end-to-end trainer** exists (it does **not** today; the only
  committed ML-baseline stack is v002-terminal-bound and inadmissible to
  pre-v002); **and**
- a **separate operator authorization** for ML is granted (`ml_authorized` is
  currently **false**).

---

## 26. Candidate next phases considered

1. **ML dataset builder readiness memo** (docs-only) — decide code-only-first
   vs data-reading-builder, lock the readiness checklist. **Lowest risk; no data
   read.**
2. **Code-only ML dataset builder skeleton** (code + synthetic tests, no data
   read) — implement the builder against the contract with synthetic fixtures
   only.
3. **ML dataset builder implementation** (data-reading) — implement and run on
   real data. **Highest risk; requires data-read authorization that does not
   exist.**
4. **Source-admissibility gate artefact** — a code-level gate for admissibility
   (not required before the contract per Phase 4bn-AB).
5. **Full-envelope reference-assembly memo** — only relevant if a future path
   combines pre-v002 + v002; not required for the conservative pre-v002-only
   path.
6. **Holdout-boundary memo** — only relevant if a future scope touches the v002
   terminal or sealed-test dates; not required here.
7. **Close the ML-baseline arc.**

---

## 27. Selected next recommendation

**Recommend authorizing an ML dataset builder readiness memo (docs-only),
subject to separate operator authorization.** After the contract is recorded,
the next safest step remains docs-only / readiness-focused: decide whether the
builder should be **code-only first** or whether a **data-reading** builder may
be authorized later. This memo does **not** jump to a data-reading builder; the
repository evidence does not support that, and
`source_admissible_for_data_read = false`.

**Alternative**, if a future operator concludes the contract is precise enough
for code-only work but not for data reads:
`RECOMMEND_AUTHORIZE_CODE_ONLY_ML_DATASET_BUILDER_SKELETON__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

No successor is authorized from inside Phase 4bn-AC.

---

## 28. Explicit non-authorizations

Phase 4bn-AC does **not**, and does not authorize anyone to: read or create any
local data; inspect any file under `data/microstructure/` or `data/research/`;
inspect any raw zip / normalized / feature / label Parquet / manifest / gate
report / sidecar; read the v002 terminal window; touch the sealed v002 test
split (`test_rows_loaded = 0`); create a split file / research matrix / ML
dataset / ML config / manifest / sidecar / gate report; mutate any manifest /
sidecar / gate report / successor-state artefact; flip `research_eligible`;
transition `eligibility_gate_status` / `chronological_split_policy` /
`diagnostics_authorized` / `ml_authorized`; invoke or alter the Phase 4aw
`flip_research_eligible(...)` always-raises invariant; train / score / predict;
run diagnostics / strategy / signals / PnL / backtests; acquire data; call any
public / authenticated / private endpoint; download any archive / CHECKSUM; run
a HEAD preflight; rerun any acquisition / raw / normalization / feature / label
execution or any layer gate; create a database / `.duckdb` / `.sqlite`; compact
Parquet; migrate storage; create v003; create or commit any `data/microstructure`
or `data/research` artefact; use credentials / `.env` / `.mcp.json` / MCP /
Graphify; open any WebSocket / user stream; authorize Phase 5, paper / shadow,
live-readiness, deployment, exchange-write, production keys, or any successor
phase.

Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread
/ V2 / G1 / C1) and every project lock (§11.6 = 8 bps per side; round-trip = 16
bps; §1.7.3; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8;
Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0;
Phase 4al refined no-rescue rule; Phase 4aw `flip_research_eligible(...)`
always-raises invariant (never invoked); Phase 4bb-F canonical path + sidecar
policy; the Phase 4bn-J-R1 raw-only cap amendment; the Phase 4bn-L derived-stack
storage budget; the Phase 4bn-N normalization manifest/versioning convention;
the Phase 4bn-R feature manifest/versioning convention; the Phase 4bn-V label
manifest/versioning convention; the Phase 4bn-Y chronological split/holdout
policy; the Phase 4bn-AA pre-v002 split-policy artefact; the Phase 4bn-AB
source-admissibility posture) is preserved verbatim. Phase 4 canonical remains
unauthorized.

---

## 29. Result state

`ML_DATASET_CONTRACT_RECORDED__PRE_V002_CONTRACT_ONLY__NO_DATA_READ__REMAIN_PAUSED`

The dataset contract is recorded; no data reads are authorized; no dataset
builder is authorized; no ML is authorized;
`source_admissible_for_dataset_contract` remains **true**;
`source_admissible_for_data_read` remains **false** until future builder
authorization; `source_admissible_for_dataset_builder` remains **false** until
future builder authorization; manifest state is unchanged.

---

## 30. Decision

`RECOMMEND_AUTHORIZE_ML_DATASET_BUILDER_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`

Rationale: after the contract is recorded, the next safest step is still
docs-only / readiness-focused — decide code-only-first vs data-reading-builder.
Do not jump directly to a data-reading builder; the evidence does not support it
and data-read admissibility is `false`.

---

## 31. Recommended state and successor options

**Recommended state: remain paused. No next phase authorized.**

Operator options (each subject to separate authorization after the
branch-complete report):

- remain paused;
- request a merge prompt for Phase 4bn-AC;
- separately authorize an **ML dataset builder readiness memo** (preferred);
- separately authorize a **code-only ML dataset builder skeleton**;
- separately authorize a **source-admissibility gate artefact** (if preferred);
- separately authorize a **full-envelope reference-assembly memo** only if a
  future path combines pre-v002 + v002 data;
- separately authorize a **holdout-boundary memo** only if a future scope
  touches the v002 terminal or sealed-test dates;
- separately authorize a **source-policy documentation memo**;
- separately authorize a **process-doc `D:` path-string update**;
- reject further ML-baseline successors and **close the ML arc**.

No ML / diagnostics / strategy / PnL / backtest / storage migration / paper /
shadow / live / exchange-write option is valid from this state unless separately
authorized after this branch is merged.

---

## 32. Current-project-state update summary

`current-project-state.md` is updated **additively only**: one new Phase 4bn-AC
paragraph appended after the Phase 4bn-AB paragraph, and one new `Current phase:`
block inserted ahead of the Phase 4bn-AB block. All prior content (Phase 4bn-A …
4bn-AB paragraphs and blocks, every retained verdict and project lock) is
preserved verbatim. No manifest field, eligibility flag, or split-policy field
is set. The update records: dataset contract recorded; contract name
`microstructure_ml_dataset_aggtrades_pre_v002_contract_v001`; pre-v002-only
scope; `forward_direction_15s` first target; 45-column feature allowlist;
forbidden-column policy; censor/null/invalid filtering; Phase 4bn-AA split
binding; leakage-proof and Phase 4bn-L budget-preflight obligations;
`data/research/microstructure/ml_datasets/pre_v002_contract_v001/` output
posture; no data read; no data created; data reads / dataset builder / ML all
remain blocked; result
`ML_DATASET_CONTRACT_RECORDED__PRE_V002_CONTRACT_ONLY__NO_DATA_READ__REMAIN_PAUSED`;
decision
`RECOMMEND_AUTHORIZE_ML_DATASET_BUILDER_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
remain paused; no successor authorized.
