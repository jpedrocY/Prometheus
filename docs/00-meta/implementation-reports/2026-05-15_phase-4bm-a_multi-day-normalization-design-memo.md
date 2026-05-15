# Phase 4bm-A — Multi-Day Normalization Design Memo

## 1. Phase identity

- **Phase:** Phase 4bm-A — Multi-Day Normalization Design Memo
- **Type:** docs-only design memo
- **Tier:** Tier 1 (Full Phase) under
  `docs/00-meta/process/phase-risk-tiering-standard.md`
  (Phase 4bl-F). This is the project's first design memo for a new
  derived-family dataset version, so full ceremony applies (new
  semantics, new dataset-version identity, and admissibility decisions
  downstream).
- **Branch:**
  `phase-4bm-a/multi-day-normalization-design-memo`
- **Base commit (`main` / `origin/main` at branch creation):**
  `ac3475acd332978bfe0037a24e5004cec5e84efc` (Phase 4bl-F merge-closeout
  commit on `main`).
- **Predecessor project-complete phase:** Phase 4bl-F — Phase
  Risk-Tiering and Controlled Remediation Standard
  (merge-closeout `2026-05-14_phase-4bl-f_merge-closeout.md`).
- **Status at end of this branch:** branch-complete; not merged; not
  project-complete.

## 2. Purpose and scope

This memo defines, at design level only, how the Prometheus project
will normalize the Phase 4az / Phase 4bl-C v002 multi-day BTCUSDT
aggTrades raw archive into a future normalized derived dataset family.

Phase 4bm-A is **design-only**. It produces no normalized data, no
parquet files, no derived manifests, no successor-state artefacts, no
gate reports. It does not run the Phase 4bd `run_normalize_aggtrades`
orchestrator on the v002 raw manifest. It does not modify any source /
test / script / configuration / governance file beyond a narrow
`current-project-state.md` paragraph addition. It does not authorize
any successor phase.

This memo is the v002 multi-day analogue of
`docs/00-meta/implementation-reports/2026-05-07_phase-4bc_aggtrades-normalization-design.md`
(the v001 single-day design). It transposes the Phase 4bc design onto
the v002 multi-day raw input, preserves the Phase 4bd `NORMALIZED_SCHEMA_V001`
column contract verbatim, and identifies the precise additional
mechanisms needed for multi-day normalization (per-day output files, a
multi-day index manifest, 90-fold validation, and lineage citations
across the v002 raw chain).

The memo's product is a precise, implementable contract that any
future operator-authorized Phase 4bm-B implementation phase must
follow. Phase 4bm-A does not authorize Phase 4bm-B.

## 3. Predecessor lineage

The v002 multi-day normalization design depends on the following
project-complete predecessor chain on `main`:

1. **Phase 4az** (BTCUSDT 2025-01-15 single-day raw acquisition):
   established the `microstructure_raw_aggtrades_v001` family with
   `dataset_version=v001`, the canonical raw zip layout, paired
   `.sha256` sidecars, the acquisition log shape, and the
   `MicrostructureManifest` schema with `research_eligible=false /
   eligibility_gate_status=pending` defaults.

2. **Phase 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E** (raw `__v001`
   eligibility gate design, planning, primitive implementation,
   execution, and successor-state policy memo). Phase 4bb-D PASS
   report SHA `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`
   established the 45-check raw eligibility gate primitive that the
   later Phase 4bl-D extended for multi-day raw evaluation.

3. **Phase 4bb-F** (Gate-Report Output Path Hygiene Memo) and
   **Phase 4bb-F-implementation** (canonical path policy in code).
   These bind every future writer in `data/microstructure/` to the
   canonical sidecar format
   `<sha256_lowercase_hex>  <basename>\n`
   (two spaces; trailing LF; no CRLF; no BOM) and the canonical
   gate-report / successor-state path policy.

4. **Phase 4bb-G** (raw `__v001` successor-state recording). Established
   the Stage-2 admissibility marker pattern for raw families
   (`stage2_raw_admissible`); the raw family's `research_eligible`
   field is permanently `false` by design, with Stage-2 admissibility
   recorded only on a sibling successor-state JSON. Local artefact
   SHA256 `ab6a82e7d2e7aebd2e88986975390e7f2364dd32364b8ea9f0f169ee403ab452`.

5. **Phase 4bc** (v001 normalization design memo). Defines the
   normalized derived family
   `microstructure_normalized_aggtrades_v001`, the 19-column
   `NORMALIZED_SCHEMA_V001` schema, the per-day parquet partition
   convention, the derived-manifest shape, the lineage-citation
   pattern, the eligibility model, the forbidden columns list, and
   the 27-check validation contract. Phase 4bm-A inherits all
   technical decisions from Phase 4bc unchanged; only the dataset
   identity, source lineage, and per-day iteration extend to multi-day.

6. **Phase 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B** (v001
   normalization implementation plan, implementation, structural QA,
   derived-family eligibility-gate design, eligibility-gate
   execution, derived-family research-eligibility decision memo, and
   derived-family successor-state recording). Phase 4bd produced the
   normalized parquet at SHA
   `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa`
   and the derived manifest at SHA
   `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9`
   for the BTCUSDT 2025-01-15 single-day cell. The Phase 4bd code
   modules (`normalize_io.py`, `normalize_aggtrades.py`,
   `normalize_manifest.py`, `normalize_validation.py`) are the
   reusable primitives that any future Phase 4bm-B will import.

7. **Phase 4bl-A / 4bl-B / 4bl-C / 4bl-D / 4bl-D-S1 / 4bl-D-S2 /
   4bl-D-R / 4bl-E** (multi-day v002 raw expansion requirements,
   acquisition design, acquisition execution, raw eligibility gate,
   sidecar canonicalization governance memo, controlled
   canonicalization execution, gate rerun, and raw successor-state
   recording). Phase 4bl-C acquired 90 daily archives covering
   2024-12-01 through 2025-02-28 UTC, totalling 155,153,449 events
   and 1,943,823,208 bytes. Phase 4bl-D-R produced the
   `RAW_MULTIDAY_GATE_PASS` verdict (33 / 33 PASS) at gate-report
   SHA `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46`.
   Phase 4bl-E recorded the v002 Stage-2 raw successor-state at
   SHA `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d`.

8. **Phase 4bl-F** (Phase Risk-Tiering and Controlled Remediation
   Standard). Establishes the Tier 1 / Tier 2 / Tier 3 / Tier 4
   ceremony calibration, the standing R-SIDECAR-CRLF remediation
   rule, and nine reusable non-authorization blocks. Phase 4bm-A is
   classified Tier 1 by design (new dataset semantics; new
   admissibility decisions downstream).

The Phase 4aw scaffold modules (`MicrostructureManifest`,
`InvalidWindow`, `RawWriter`, `EligibilityGateStatus`,
`MicrostructureConfig`) and the Phase 4ax `aggtrades.py` validator
(`validate_aggtrade_payload`) remain the shared primitives. The
Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant must be preserved end-to-end by any future
Phase 4bm-B implementation.

## 4. Source-data summary (v002 raw inputs)

The v002 raw multi-day artefacts that Phase 4bm-B (if separately
authorized) will consume read-only:

- **Source raw manifest:**
  `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json`
  - SHA256: `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485`
  - size: 105,052 bytes
  - `dataset_family`: `microstructure_raw_aggtrades_v001`
  - `dataset_version`: `v002`
  - `schema_version`: `v001`
  - `symbol_list`: `["BTCUSDT"]`
  - `date_start`: `2024-12-01`
  - `date_end`: `2025-02-28`
  - `date_count`: 90
  - `expected_file_count`: 90
  - `acquired_file_count`: 90
  - `total_size_bytes`: 1,943,823,208
  - `total_row_count`: 155,153,449
  - `research_eligible`: `false` (locked invariant for raw families)
  - `eligibility_gate_status`: `pending` (locked on actual manifest)
  - `acquisition_log_sha256`: `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314`

- **Source raw manifest sidecar:**
  `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json.sha256`
  - SHA256: `adaf97242cfbe922bc9e93a6699e547d1b02fa64a96dd2cdd08df1814ce25e26`
  - size: 111 bytes (canonical Phase 4bb-F format)

- **Source acquisition log:**
  `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json`
  - SHA256: `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314`
  - size: 302,055 bytes

- **Source acquisition log sidecar:**
  `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json.sha256`
  - SHA256: `975bdc544152d1f84f6e700309aad89998e663cb779acc5883bd20652e428958`
  - size: 127 bytes (canonical Phase 4bb-F format)

- **Source raw zips (90 files):** under
  `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/<YYYY>/<MM>/`
  with paired `.sha256` sidecars in canonical Phase 4bb-F format. Per-file
  SHA256, size, row count, and timestamp bounds are recorded verbatim
  in the v002 manifest's `per_file_inventory` field. The Phase 4az
  2025-01-15 zip is reused in place at SHA
  `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`,
  with its sidecar canonicalised by Phase 4bl-D-S2 to SHA
  `c40e6be60753a912063d9a5f5c1617ba31ec987c09121c50adab3ba0226018fc`
  (canonical LF format).

- **Source PASS gate report (v002):**
  `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json`
  - SHA256: `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46`
  - size: 171,342 bytes
  - `overall_status`: `pass`
  - `gate_verdict`: `RAW_MULTIDAY_GATE_PASS`
  - 33 / 33 PASS / 0 FAIL / 0 ERROR / 0 NOT_APPLICABLE
  - 0 invalid_window_candidates
  - full per-row `validate_aggtrade_payload` confirmed across all
    155,153,449 events
  - paired sidecar at SHA
    `84f37b7b424d67dfa0dae06bb51279354b5b37998beb4f9b1cf6b6f617dd8c02`
    (155 bytes; canonical Phase 4bb-F format)

- **Source raw successor-state (v002 Stage-2):**
  `data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v002__stage2_raw_admissible__phase-4bl-e.json`
  - SHA256: `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d`
  - size: 17,603 bytes
  - `successor_state`: `stage2_raw_admissible`
  - `successor_admissibility_status`: `admissible_in_principle_policy_level_only`
  - `successor_research_use_admissible`: `conditional_future_only`
  - paired sidecar at SHA
    `63d97bf54e1063f2fd70024d40639db711e9c24d929074cdd63b2db385302b4f`
    (147 bytes; canonical Phase 4bb-F format)

A future Phase 4bm-B must verify all six lineage SHA256 values above
read-only and fail closed on any mismatch before producing any
normalized output. None of these source artefacts may be modified by
Phase 4bm-B; the Phase 4bd existing precedent demonstrates that
read-only consumption with pre/post hash equality is the correct
discipline.

## 5. Proposed normalized dataset identity

Phase 4bm-A recommends the following identity for the v002 multi-day
normalized derived family:

- **dataset_family:** `microstructure_normalized_aggtrades_v001`
  - Reuses the existing v001 family name. Schema is byte-identical to
    Phase 4bd / Phase 4bc (19 columns, same names, same dtypes, same
    semantics). The family name encodes schema lineage; reusing it
    signals "same schema, different bounded source dataset."
- **dataset_version:** `v002`
  - New version because the bounded source dataset is different
    (90 days of BTCUSDT vs the v001 single-day BTCUSDT 2025-01-15).
    The version bump carries the lineage discrimination, exactly
    mirroring how the raw family uses the same family name with
    `dataset_version=v001` (single day) and `dataset_version=v002`
    (90 days).
- **schema_version:** `v001`
  - Schema version is unchanged. The 19-column
    `NORMALIZED_SCHEMA_V001` contract is preserved verbatim.

This naming follows the precedent set by the raw family
(`microstructure_raw_aggtrades_v001` with `dataset_version=v001` and
`dataset_version=v002` coexisting). Phase 4bm-A explicitly
**rejects** the alternative of introducing a new family name like
`microstructure_normalized_aggtrades_v002`, because schema_version is
unchanged and inventing a new family would imply a schema change that
does not exist. The `dataset_version` field is the correct mechanism
to discriminate bounded source datasets when the schema is identical.

The Phase 4bd v001 derived manifest currently records
`dataset_version=null` (a small omission in the Phase 4bd
implementation). Phase 4bm-A's v002 design records
`dataset_version="v002"` explicitly. Phase 4bm-A does not amend the
Phase 4bd v001 manifest — the v001 derived family remains exactly as
recorded; only the v002 design adds the explicit version field.

## 6. Proposed normalized schema (preserved from Phase 4bc / Phase 4bd verbatim)

The normalized schema for v002 is **byte-identical** to the Phase 4bd
`NORMALIZED_SCHEMA_V001` constant. No new columns. No removed columns.
No reordering. No dtype changes. No semantic changes.

The 19-column canonical schema, in canonical column order:

| # | Column | Dtype | Source |
|---|--------|-------|--------|
| 1 | `dataset_family` | `string` | constant: `microstructure_normalized_aggtrades_v001` |
| 2 | `dataset_version` | `string` | constant: `v002` |
| 3 | `source_dataset_family` | `string` | constant: `microstructure_raw_aggtrades_v001` |
| 4 | `source_dataset_version` | `string` | constant: `v002` |
| 5 | `symbol` | `string` | constant per row partition: `BTCUSDT` |
| 6 | `utc_date` | `string` | constant per row partition: e.g. `2024-12-01` |
| 7 | `agg_trade_id` | `int64` | raw aggTrade `a` |
| 8 | `price` | `string` (Decimal-as-string) | raw aggTrade `p` (lossless) |
| 9 | `quantity` | `string` (Decimal-as-string) | raw aggTrade `q` (lossless) |
| 10 | `first_trade_id` | `int64` | raw aggTrade `f` |
| 11 | `last_trade_id` | `int64` | raw aggTrade `l` |
| 12 | `transact_time_ms` | `int64` | raw aggTrade `T` (UTC ms) |
| 13 | `is_buyer_maker` | `bool` | raw aggTrade `m` |
| 14 | `source_file_sha256` | `string` | constant per row partition: SHA256 of source raw zip for that date |
| 15 | `source_manifest_sha256` | `string` | constant: SHA256 of v002 raw manifest |
| 16 | `source_gate_report_id` | `string` | constant: Phase 4bl-D-R PASS gate report id |
| 17 | `source_gate_report_sha256` | `string` | constant: Phase 4bl-D-R PASS gate report SHA256 |
| 18 | `row_index` | `int64` | deterministic 0..N-1 within each per-day file |
| 19 | `normalization_schema_version` | `string` | constant: `v001` |

Per-row mapping discipline (reused from Phase 4bd):

- One-to-one row mapping: every raw aggTrade row produces exactly one
  normalized row.
- Lossless precision: `price` and `quantity` parsed from raw CSV via
  Python `Decimal` and serialised back to canonical Decimal string form
  preserving every significant digit. **Float storage is forbidden for
  these two columns.** No scientific notation. No truncation. No
  rounding. No re-formatting.
- Timestamps as `int64` UTC ms exactly as supplied by Binance.
- `is_buyer_maker` as strict pyarrow `bool`.
- `row_index` is a deterministic counter starting at 0 within each
  per-day partition, incrementing by 1 per row, in source iteration
  order.
- Schema-equality assertion at output time: the produced pyarrow table
  must match `NORMALIZED_SCHEMA_V001` byte-for-byte (column names in
  canonical order; canonical dtypes; no extras; no missing).

Forbidden column substrings (preserved from Phase 4bc verbatim and
extended where Phase 4bd introduced new patterns):

- any feature column,
- any label column,
- any signal column,
- any return / log-return / forward-return column,
- any alpha / edge / opportunity-rate / predictiveness column,
- any taker-imbalance / sweep / aggressive-flow / order-flow column,
- any spread / depth / liquidity / slippage column,
- any execution-quality / fill-quality column,
- any regime / trend / momentum / volatility column,
- any MFE / MAE / R-multiple / take-profit / stop-loss column,
- any PnL / equity / position / strategy / decision column,
- any prediction / model-score / classification / probability column.

A future Phase 4bm-B must enforce these forbidden substrings via
static schema-equality assertion plus an explicit deny-list scan
against output column names.

## 7. Proposed partitioning, file layout, and output namespace

The normalized v002 output uses the same per-day parquet partition
layout as Phase 4bd, scaled to 90 days:

```
data/microstructure/normalized/
  microstructure_normalized_aggtrades_v001/
    BTCUSDT/
      2024/
        12/
          BTCUSDT-aggTrades-2024-12-01.parquet
          BTCUSDT-aggTrades-2024-12-01.parquet.sha256
          BTCUSDT-aggTrades-2024-12-02.parquet
          BTCUSDT-aggTrades-2024-12-02.parquet.sha256
          ... (31 dates)
      2025/
        01/
          BTCUSDT-aggTrades-2025-01-01.parquet
          BTCUSDT-aggTrades-2025-01-01.parquet.sha256
          ... (31 dates)
        02/
          BTCUSDT-aggTrades-2025-02-01.parquet
          BTCUSDT-aggTrades-2025-02-01.parquet.sha256
          ... (28 dates)
```

Total expected output:
- 90 parquet files,
- 90 paired `.sha256` sidecars in canonical Phase 4bb-F format,
- 1 multi-day index manifest at
  `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json`,
- 1 paired manifest sidecar at
  `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json.sha256`.

Total expected normalized data volume estimate, derived from
extrapolating the Phase 4bd single-day result (224,382,279 bytes for
1,681,098 rows ≈ 133 bytes per row): roughly 20.6 GiB total parquet
storage for 155,153,449 rows. Storage is local-only and gitignored
under `.gitignore:85` (`data/microstructure/`).

The Phase 4bd 2025-01-15 single-day v001 normalized parquet is
**not modified, not moved, not renamed, not deleted, not consumed** by
Phase 4bm-B. The v001 normalized family remains exactly as it is on
the operator's local machine (SHA
`2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa`,
under `microstructure_normalized_aggtrades_v001/BTCUSDT/2025/01/`).
The v002 normalized family writes a parallel parquet for the same
date — `BTCUSDT-aggTrades-2025-01-15.parquet` under the same family /
same path tree but with `dataset_version="v002"` recorded inside the
parquet's per-row constants and inside the v002 manifest. The two
parquets coexist; the v002 file is the one to consume for v002 work.

Both parquet files for 2025-01-15 must be byte-identical in their
trade-data columns (raw aggTrades for 2025-01-15 are byte-identical
between v001 and v002 — same source zip, same SHA). They will differ
only in:

- column 2 `dataset_version` (v001 vs v002),
- column 4 `source_dataset_version` (v001 vs v002),
- column 14 `source_file_sha256` (same value; both reference the same
  raw zip),
- column 15 `source_manifest_sha256` (different: v001 cites the v001
  raw manifest; v002 cites the v002 raw manifest),
- column 16 `source_gate_report_id` (different: v001 cites the
  Phase 4bb-D PASS gate report; v002 cites the Phase 4bl-D-R PASS gate
  report),
- column 17 `source_gate_report_sha256` (different),
- column 18 `row_index` (identical 0..1,681,097 sequence),
- column 19 `normalization_schema_version` (both v001; identical).

This coexistence is by design and is governance-safe: each parquet
records its lineage explicitly via lineage columns, and the
multi-day v002 manifest is the single point of consumption for v002
work.

## 8. Proposed multi-day index manifest schema

The v002 derived family uses **one multi-day index manifest** that
aggregates all 90 per-day parquet files, mirroring the Phase 4bl-C
v002 raw manifest's `per_file_inventory` pattern. Per-day
sub-manifests are **not** produced; the multi-day index manifest is
the single source of truth for the v002 derived family.

Manifest path:
`data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json`

Required top-level fields (binding for any future Phase 4bm-B
implementation):

| Field | Type | Value |
|-------|------|-------|
| `dataset_family` | `string` | `microstructure_normalized_aggtrades_v001` |
| `dataset_version` | `string` | `v002` |
| `schema_version` | `string` | `v001` |
| `symbol_list` | `array[string]` | `["BTCUSDT"]` |
| `date_start` | `string` | `2024-12-01` |
| `date_end` | `string` | `2025-02-28` |
| `date_count` | `int` | 90 |
| `date_list` | `array[string]` | 90-element ISO date list |
| `expected_file_count` | `int` | 90 |
| `produced_file_count` | `int` | 90 (on success) |
| `total_event_count` | `int` | 155,153,449 |
| `per_file_inventory` | `array[object]` | 90 entries; see below |
| `source_dataset_family` | `string` | `microstructure_raw_aggtrades_v001` |
| `source_dataset_version` | `string` | `v002` |
| `source_manifest_path` | `string` | path to v002 raw manifest |
| `source_manifest_sha256` | `string` | `016967865c97...d87485` |
| `source_acquisition_log_path` | `string` | path to v002 acquisition log |
| `source_acquisition_log_sha256` | `string` | `52f6d7fb3cb0...c6b314` |
| `source_gate_report_id` | `string` | Phase 4bl-D-R PASS gate report id |
| `source_gate_report_path` | `string` | path to Phase 4bl-D-R PASS gate report |
| `source_gate_report_sha256` | `string` | `f9493fd10d1c...6f1c46` |
| `source_successor_state_path` | `string` | path to Phase 4bl-E successor-state |
| `source_successor_state_sha256` | `string` | `a0576ca656bd...1f751d` |
| `source_phase_boundary` | `string` | `4bl-E` |
| `research_eligible` | `bool` | `false` (locked invariant for derived v002 at Stage-0) |
| `eligibility_gate_status` | `string` | `pending` (locked) |
| `governance_labels` | `object` | see below |
| `invalid_windows` | `array[object]` | empty for v002 (raw gate reported zero) |
| `created_at_unix_ms` | `int` | wall-clock at manifest creation |
| `created_at_utc` | `string` | ISO-8601 UTC |
| `code_commit_sha` | `string` | git commit SHA at Phase 4bm-B execution |
| `base_commit_sha` | `string` | git commit SHA of `main` at branch creation |
| `capture_config_hash` | `string` | normalization-config hash (see below) |
| `phase` | `string` | `4bm-B` |

Per-file inventory entry shape (90 entries; one per date):

| Field | Type | Description |
|-------|------|-------------|
| `date` | `string` | ISO date, e.g. `2024-12-01` |
| `symbol` | `string` | `BTCUSDT` |
| `local_parquet_path` | `string` | repo-relative path under `data/microstructure/` |
| `local_sidecar_path` | `string` | paired `.sha256` path |
| `parquet_sha256` | `string` | 64-char SHA256 of parquet file |
| `sidecar_sha256` | `string` | 64-char SHA256 of sidecar file |
| `parquet_size_bytes` | `int` | byte size of parquet file |
| `event_count` | `int` | row count for this date |
| `first_transact_time_ms` | `int` | minimum transact_time_ms in file |
| `last_transact_time_ms` | `int` | maximum transact_time_ms in file |
| `min_agg_trade_id` | `int` | minimum agg_trade_id in file |
| `max_agg_trade_id` | `int` | maximum agg_trade_id in file |
| `source_file_sha256` | `string` | SHA256 of source raw zip for this date (must match v002 raw manifest entry) |
| `source_zip_path` | `string` | repo-relative path to source raw zip |
| `status` | `string` | `produced_verified` |

Required `governance_labels` block (16 keys; preserved verbatim from
Phase 4bd pattern with the v002 substitutions):

| Key | Value |
|-----|-------|
| `phase` | `4bm-B` |
| `source_phase_boundary` | `4bl-E` |
| `source_dataset_family` | `microstructure_raw_aggtrades_v001` |
| `source_dataset_version` | `v002` |
| `source_manifest_path` | path to v002 raw manifest |
| `source_manifest_sha256` | `016967865c97...d87485` |
| `source_gate_report_id` | Phase 4bl-D-R PASS gate report id |
| `source_gate_report_sha256` | `f9493fd10d1c...6f1c46` |
| `source_gate_report_code_commit_sha` | code commit SHA recorded in Phase 4bl-D-R gate report |
| `source_successor_state_sha256` | `a0576ca656bd...1f751d` |
| `validator` | `phase_4ax_aggtrades_v001` |
| `stop_trigger_domain` | `trade_price_backtest_candidate` |
| `feature_computation` | `forbidden` |
| `strategy_use` | `forbidden` |
| `phase_4bm_b_no_successor_authorization` | `true` |
| `multi_day` | `true` |

The `capture_config_hash` field is a deterministic SHA256 of the
JSON-serialised normalization configuration block (orchestrator
parameters, schema constant version, validator constant version,
input-allowlist boundaries). It exists so any future Phase 4bm-C
structural QA can verify that the Phase 4bm-B run used the exact
configuration recorded.

Manifest write rules (preserved from Phase 4bd; binding):

- atomic write-then-rename via `os.replace`,
- refuse-overwrite at writer level,
- paired `.sha256` sidecar in canonical Phase 4bb-F format
  (`<sha>  <basename>\n`; two spaces; trailing LF),
- `research_eligible = false` invariant (the Phase 4aw
  `MicrostructureManifest.flip_research_eligible(...)` always-raises
  guard must be preserved end-to-end),
- `eligibility_gate_status = "pending"` invariant.

## 9. Eligibility-state model (Phase 4ba 5-stage ladder applied to v002 derived family)

The Phase 4ba 5-stage eligibility ladder applies to the v002
derived family in its own right, independently of the v001 derived
family's existing Stage-3 admissibility:

- **Stage 0 — acquired.** Reached after a future Phase 4bm-B
  execution writes 90 parquets, 90 sidecars, the multi-day index
  manifest, and the manifest sidecar. Default state. Produces no
  research-use claim.
- **Stage 1 — inspected.** Reached after a future Phase 4bm-C
  structural QA memo verifies parquet counts, lineage SHAs,
  schema-column equality, row-count parity vs the v002 raw manifest's
  per-file `row_count`, dtype conformance, partition tree integrity,
  and pre/post immutability of all source artefacts.
- **Stage 2 — gate-passed.** Reached after a future Phase 4bm-D
  derived-family eligibility-gate execution (analogue of Phase 4bf
  for the v002 derived family) emits a PASS gate report under
  `data/microstructure/gate-reports/normalized/`.
- **Stage 3 — research-eligible.** Reached only after a separately
  authorized Phase 4bm-E research-eligibility decision phase
  (analogue of Phase 4bg-A) and a Phase 4bm-F successor-state
  recording phase (analogue of Phase 4bg-B). Derived families may
  reach Stage 3; raw families never can.
- **Stage 4 — feature-cleared.** Out of scope for Phase 4bm-A.
  Authorisation requires its own M0-cleared feature-design memo.

Stage progression preserves the locked invariants:

- the on-disk derived manifest's `research_eligible` field remains
  `false` until a separately authorized successor-state phase
  records the Stage-3 marker on a sibling artefact (precedent: Phase
  4bg-B for v001),
- Stage transitions are recorded as sibling successor-state JSONs
  under `data/microstructure/successor-state/`, never as in-place
  manifest mutations,
- the Phase 4aw `flip_research_eligible(...)` always-raises invariant
  is preserved across every Stage transition,
- every Stage transition requires its own separately authorized
  phase.

Phase 4bm-A reaches none of these stages. Phase 4bm-A is design-only.
Phase 4bm-B (if separately authorized in the future) would be the
first phase to reach Stage 0 for the v002 derived family.

## 10. Forbidden inputs, forbidden outputs, and no-rescue boundary

Forbidden inputs to any future Phase 4bm-B implementation (binding):

- mark-price (any timeframe),
- aggTrades from any source other than the locked v002 raw zips,
- trade-tick / raw trades / 1m / 5m / 15m / 30m / 1h / 4h / kline data,
- spot-market data,
- cross-venue data,
- order-book / depth / book-ticker data,
- private / authenticated REST data,
- user stream / WebSocket / listenKey lifecycle,
- Binance API calls of any kind,
- `data.binance.vision` calls of any kind,
- any network I/O,
- any credential, `.env` read, `.mcp.json` read,
- MCP / Graphify enablement,
- the Phase 4i metrics OI subset,
- optional metrics ratio columns,
- 5m Q1–Q7 diagnostic outputs,
- any Phase 4l / 4r / 4x forensic output as design input,
- any Phase 4aq forensic output as design input,
- the Phase 4az v001 raw zip / manifest / gate report (the v002
  derived family must consume only v002 raw artefacts; the Phase 4az
  2025-01-15 zip is included by virtue of being part of the v002
  90-day archive, but its lineage is cited via the v002 raw manifest's
  per-file inventory, not via a direct v001 manifest reference).

Forbidden outputs from any future Phase 4bm-B implementation
(binding):

- features / labels / signals / proxies / predictions / model scores,
- strategy decisions / entry-exit logic,
- backtest results / PnL / MFE / MAE / R-multiple / equity curves,
- any column whose name contains a forbidden substring (see §6),
- any modification to the v002 raw manifest, raw zips, raw zip
  sidecars, acquisition log, Phase 4bl-D-R PASS gate report,
  Phase 4bl-E successor-state, or any other prior `data/microstructure/`
  artefact,
- any modification to the Phase 4bd v001 normalized parquet,
  Phase 4bd v001 derived manifest, Phase 4bf v001 derived gate report,
  Phase 4bg-B v001 successor-state, Phase 4bh feature parquet, Phase
  4bh feature manifest, Phase 4bi-B feature gate report, Phase 4bi-D
  feature successor-state, Phase 4bj-C label parquet, Phase 4bj-C
  label manifest, Phase 4bj-E label gate report, Phase 4bj-G label
  successor-state, or Phase 4bj-J no-split determination,
- any successor-state recording (that requires a separately authorized
  Phase 4bm-F or equivalent),
- any gate report (that requires a separately authorized Phase 4bm-D
  or equivalent),
- any commit under `data/microstructure/` (always gitignored).

No-rescue boundary (preserved from Phase 4al refined no-rescue rule
and Phase 4ak twelve-clause M0 gate; binding):

- No retained verdict is revised by Phase 4bm-A or by any future
  Phase 4bm-B (H0, R3, R1a, R1b-narrow, R2, F1, D1-A, 5m thread, V2,
  G1, C1 all preserved verbatim).
- No project lock is changed (§11.6 = 8 bps per side; round-trip = 16
  bps; §1.7.3 = 0.25% / 2× / one-position / mark-price stops; Phase
  3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j
  §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak
  M0; Phase 4al refined no-rescue; Phase 4aw `flip_research_eligible(...)`
  always-raises; Phase 4bb-F canonical path policy; Phase 4bl-F
  R-SIDECAR-CRLF rule and tier model).
- The cooled-down families list (Phase 4ak M0 §5–§8) is preserved:
  price-only single-symbol directional continuation (DEPLETED);
  cross-sectional trend / relative-strength symbol-selection under
  Phase 4ai descriptors (COOLED_DOWN); derivatives-context
  directional lane (CONDITIONAL_ONLY); microstructure / order-flow /
  liquidity-timing lane (NOT_RECOMMENDED_NOW); mark-price stop-domain
  / execution-realism lane (NOT_RECOMMENDED_NOW). Phase 4bm-A does
  not reopen any of these; v002 normalization is data-infrastructure
  work, not strategy work.
- Normalization is descriptive transformation only. It does not imply
  edge, opportunity, or admissibility for any cooled-down family.

## 11. Phase 4bb-F canonical path policy and Phase 4bl-F R-SIDECAR-CRLF rule

All sidecars produced by any future Phase 4bm-B implementation must
conform to the Phase 4bb-F canonical sidecar format verbatim:

- body: `<sha256_lowercase_hex>  <basename>\n`
- exactly two ASCII spaces between the SHA and the basename,
- exactly one trailing newline (`\n`, byte `0x0A`),
- no carriage return (no `\r`, no `\r\n`),
- no BOM,
- no trailing whitespace beyond the single LF,
- no additional content (no comments, no blank lines, no extra
  newlines).

This applies to:

- 90 parquet sidecars (`*.parquet.sha256`),
- 1 multi-day manifest sidecar
  (`microstructure_normalized_aggtrades_v001__v002.json.sha256`).

The Phase 4bl-F standing rule R-SIDECAR-CRLF authorizes a future
Tier 2 controlled phase to canonicalize a single Phase 4bb-F sidecar
from CRLF to canonical LF without a separately authorized governance
memo, subject to the five Phase 4bl-F criteria. R-SIDECAR-CRLF is a
**remediation rule**; it does not apply to Phase 4bm-B's forward
writes. Phase 4bm-B writers must produce canonical LF format from the
start; if any Phase 4bm-B sidecar is later found to be non-canonical,
that is a Phase 4bm-B implementation defect to be repaired before
merge, not a remediation event for R-SIDECAR-CRLF.

The Phase 4bb-F canonical path placement convention is preserved:

- gate reports (future Phase 4bm-D output) under
  `data/microstructure/gate-reports/normalized/<dataset_family>__<dataset_version>__phase-<phase-id>__<unix_ms>__<short_commit>.json`,
- successor-state artefacts (future Phase 4bm-F output) under
  `data/microstructure/successor-state/<dataset_family>__<dataset_version>__<stage_marker>__phase-<phase-id>.json`,
- normalized parquets (future Phase 4bm-B output) under
  `data/microstructure/normalized/<dataset_family>/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-aggTrades-<YYYY-MM-DD>.parquet`,
- manifests (future Phase 4bm-B output) under
  `data/microstructure/manifests/<dataset_family>__<dataset_version>.json`.

All paths are gitignored under `.gitignore:85`
(`data/microstructure/`).

## 12. Validation and acceptance criteria for any future Phase 4bm-B

Any future Phase 4bm-B implementation must produce evidence for
**all** of the following acceptance criteria. A failure of any
criterion is a Phase 4bm-B fail-closed condition.

### 12.1 Source-artefact precondition checks (10 criteria)

1. v002 raw manifest exists at the recorded path.
2. v002 raw manifest SHA256 matches `016967865c97...d87485`.
3. v002 raw manifest sidecar SHA256 matches `adaf972442cfb...e25e26`.
4. v002 acquisition log exists and SHA256 matches `52f6d7fb3cb0...c6b314`.
5. v002 acquisition log sidecar SHA256 matches `975bdc544152...428958`.
6. Phase 4bl-D-R PASS gate report exists and SHA256 matches `f9493fd10d1c...6f1c46`.
7. Phase 4bl-D-R gate report sidecar SHA256 matches `84f37b7b424d...8c02`.
8. Phase 4bl-E successor-state exists and SHA256 matches `a0576ca656bd...1f751d`.
9. Phase 4bl-E successor-state sidecar SHA256 matches `63d97bf54e10...6af8`.
10. All 90 v002 raw zip files exist at their recorded paths and each
    SHA256 matches the corresponding `per_file_inventory` entry.

### 12.2 Per-day normalization checks (extension of Phase 4bc 27-check suite × 90 dates)

For each of the 90 dates, the Phase 4bc / Phase 4bd 27-check
validation suite must PASS:

11. Output parquet exists at the canonical path.
12. Output sidecar exists in canonical Phase 4bb-F format.
13. Parquet schema-column-equality vs `NORMALIZED_SCHEMA_V001`.
14. Parquet `event_count` matches the v002 raw manifest's per-file
    `row_count`.
15. `row_index` is contiguous 0..N-1 within the file.
16. `agg_trade_id` is non-decreasing within the file.
17. No duplicate `agg_trade_id` within the file.
18. `transact_time_ms` is monotonically non-decreasing within the file
    (same-timestamp tie-break by `agg_trade_id`).
19. All `transact_time_ms` values lie within the half-open UTC day
    bound `[date_start_ms, date_start_ms + 86_400_000)` for that date.
20. `price` and `quantity` are stored as Decimal-as-string with
    no float storage and no lossy rounding.
21. `is_buyer_maker` is strict pyarrow `bool`.
22. Per-row lineage columns (`dataset_family`, `dataset_version`,
    `source_dataset_family`, `source_dataset_version`,
    `source_file_sha256`, `source_manifest_sha256`,
    `source_gate_report_id`, `source_gate_report_sha256`,
    `normalization_schema_version`) are constant across all rows in
    the file and match the recorded values.
23. `symbol` is constant `BTCUSDT` across all rows.
24. `utc_date` is constant for that date.
25. First row's `transact_time_ms` matches the v002 raw manifest's
    `first_trade_time_ms` for that date.
26. Last row's `transact_time_ms` matches the v002 raw manifest's
    `last_trade_time_ms` for that date.
27. Minimum `agg_trade_id` matches the v002 raw manifest's
    `min_agg_trade_id` for that date.
28. Maximum `agg_trade_id` matches the v002 raw manifest's
    `max_agg_trade_id` for that date.
29. No forbidden column substring appears in the parquet schema
    (deny-list scan).
30. Output parquet SHA256 matches the value recorded in the per-file
    inventory entry.
31. Output sidecar parses cleanly under canonical Phase 4bb-F format
    and the parsed SHA matches the recomputed parquet SHA bit-for-bit.

(Phase 4bc's 27 checks plus four multi-day extension checks
[10, 25–28, 30, 31]; the implementation may consolidate where Phase
4bc's check IDs already cover these — the count is illustrative,
not normative.)

### 12.3 Aggregate / multi-day checks (8 criteria)

32. Multi-day index manifest exists at the canonical path.
33. Multi-day index manifest sidecar exists in canonical Phase 4bb-F
    format.
34. Multi-day manifest's `produced_file_count` equals 90.
35. Multi-day manifest's `total_event_count` equals 155,153,449
    (matches v002 raw manifest exactly).
36. Sum of per-file `event_count` across all 90 entries equals
    `total_event_count`.
37. `date_list` length equals 90 and matches the v002 raw manifest's
    `date_list` exactly.
38. `per_file_inventory` length equals 90 with no missing dates and
    no duplicate dates.
39. Adjacent-date overlap check: for each consecutive pair of dates
    `(D, D+1)`, the maximum `last_transact_time_ms` of date D is
    strictly less than the minimum `first_transact_time_ms` of date
    D+1.

### 12.4 Lineage / immutability checks (10 criteria)

40. v002 raw manifest pre/post SHA256 identical (source not modified).
41. v002 raw manifest sidecar pre/post SHA256 identical.
42. v002 acquisition log pre/post SHA256 identical.
43. v002 acquisition log sidecar pre/post SHA256 identical.
44. All 90 v002 raw zip pre/post SHA256 identical.
45. All 90 v002 raw zip sidecar pre/post SHA256 identical.
46. Phase 4bl-D-R PASS gate report pre/post SHA256 identical.
47. Phase 4bl-D-R gate report sidecar pre/post SHA256 identical.
48. Phase 4bl-E successor-state pre/post SHA256 identical.
49. Phase 4bl-E successor-state sidecar pre/post SHA256 identical.

### 12.5 Governance / boundary checks (12 criteria)

50. Multi-day manifest's `research_eligible` is `false`.
51. Multi-day manifest's `eligibility_gate_status` is `"pending"`.
52. Multi-day manifest's `governance_labels.feature_computation` is
    `"forbidden"`.
53. Multi-day manifest's `governance_labels.strategy_use` is
    `"forbidden"`.
54. Multi-day manifest's `governance_labels.phase_4bm_b_no_successor_authorization`
    is `true`.
55. Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
    always-raises invariant preserved (must not have been called).
56. No file under `data/microstructure/` is staged in git.
57. No tracked `data/microstructure/` file changed.
58. No network I/O attempted.
59. No credential read attempted.
60. No `.env` or `.mcp.json` read or write attempted.
61. No call to any Binance / public / private endpoint.

### 12.6 Quality-gate checks (4 criteria)

62. `ruff check .` passes (whole repo).
63. `mypy --strict src/prometheus/research/microstructure/` passes
    (whole package).
64. `pytest tests/research/microstructure/` passes (no new
    regressions; pre-existing labelled skips preserved).
65. `git diff --check` clean; `git status` shows only the tracked
    Phase 4bm-B docs / scripts / tests plus the pre-existing
    untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`).

### 12.7 Failure handling (binding)

If any criterion 1–65 fails, Phase 4bm-B must:

- emit `FAIL_CLOSED` status,
- not produce a partial multi-day manifest,
- preserve any per-day parquets already written (each is independently
  verifiable via its sidecar; partial output is recoverable evidence,
  not corruption),
- record the failure in the Phase 4bm-B implementation report,
- not authorize Phase 4bm-C / 4bm-D / 4bm-E / 4bm-F.

## 13. Future Phase 4bm-* implementation ladder, recommendations, and non-authorizations

Phase 4bm-A is the first phase in the v002 multi-day normalization
arc. The natural future phase ladder, per Phase 4bc → Phase 4bd → Phase
4be → Phase 4bf → Phase 4bg-A → Phase 4bg-B precedent transposed to
v002:

- **Phase 4bm-B** — Multi-Day Normalization Implementation (code +
  docs + local-gitignored output). Tier 1. Implements this design
  exactly. Produces 90 normalized parquets, 90 sidecars, 1 multi-day
  index manifest, 1 manifest sidecar. Preserves all 49 pre/post
  source-artefact SHA256 values. Reaches Stage-0 for the v002 derived
  family. **NOT authorized by Phase 4bm-A.**

- **Phase 4bm-C** — Multi-Day Normalized Dataset Structural QA Memo
  (analysis-and-docs + local read-only). Tier 1. Performs read-only
  structural QA against the Phase 4bm-B output. Reaches Stage-1 for
  the v002 derived family. **NOT authorized by Phase 4bm-A.**

- **Phase 4bm-D** — Multi-Day Derived-Family Eligibility-Gate Design +
  Implementation + Execution (code + docs + local-gitignored
  output). Tier 1. Translates the Phase 4bf v001 derived-family gate
  primitive to v002 multi-day scope. Produces a gate report under
  `data/microstructure/gate-reports/normalized/`. Reaches Stage-2
  (report-level) for the v002 derived family. **NOT authorized by
  Phase 4bm-A.**

- **Phase 4bm-E** — Multi-Day Derived-Family Research-Eligibility
  Decision Memo (docs-only). Tier 1. Decides whether the v002 derived
  family is admissible in principle for Stage-3 research-eligibility,
  given the predecessor evidence chain. **NOT authorized by Phase
  4bm-A.**

- **Phase 4bm-F** — Multi-Day Derived-Family Successor-State Recording
  (docs + local-gitignored output). Tier 1. Records the Stage-3
  research-eligibility marker on a sibling successor-state JSON,
  preserving the on-disk derived manifest byte-identically. **NOT
  authorized by Phase 4bm-A.**

After Phase 4bm-F, the natural extension is a multi-day feature arc
(Phase 4bn-* equivalent) and a multi-day label arc (Phase 4bo-*
equivalent), each requiring separate authorization, separate M0
admissibility, and separate operator-driven decisions.

### Recommended state

**Remain paused.**

The operator has signalled an intent to pause for a broader project
discussion (complexity, phase usefulness, possible energy-market
sibling project) before any technical successor is authorized. Phase
4bm-A satisfies the Phase 4bl-F merge-closeout's recommended
"Conditional next, NOT authorized" by producing the design memo
analogue of Phase 4bc for the v002 raw family. The recommended state
after Phase 4bm-A is to remain paused and let the operator decide
whether to authorize Phase 4bm-B or pivot to a different lane.

### Non-authorization clauses (reusable Phase 4bl-F blocks invoked verbatim)

Phase 4bm-A invokes the following reusable non-authorization blocks
from `docs/00-meta/process/phase-risk-tiering-standard.md`
(Phase 4bl-F):

- **N-ACQUISITION** — Phase 4bm-A does not authorize any new data
  acquisition (no additional aggTrades / 5m / 1m / tick / mark-price
  / order-book / spot / cross-venue / funding / open-interest data).
- **N-ENDPOINT** — Phase 4bm-A does not authorize any call to any
  Binance endpoint, public endpoint, or private endpoint, and does
  not authorize any WebSocket / user stream / listenKey lifecycle.
- **N-CREDENTIALS** — Phase 4bm-A does not authorize any credential
  use, `.env` read, or `.mcp.json` read or create; does not enable
  MCP or Graphify; does not authorize production keys / authenticated
  APIs / private endpoints.
- **N-MANIFEST** — Phase 4bm-A does not modify any existing manifest,
  does not flip `research_eligible` on any actual manifest, does not
  transition `eligibility_gate_status` on any actual manifest, does
  not change `chronological_split_policy` on any actual manifest.
- **N-GATE-RERUN** — Phase 4bm-A does not rerun any gate (raw v001,
  raw v002, derived v001, feature, label). Does not generate any new
  gate report.
- **N-SUCCESSOR-STATE** — Phase 4bm-A does not create any
  successor-state artefact. The Stage progression for the v002
  derived family begins (if ever) at Phase 4bm-B, not at Phase 4bm-A.
- **N-DERIVATION** — Phase 4bm-A does not run normalization,
  derivation, features, labels, diagnostics, ML, strategy, signals,
  or backtests. It is design-only.
- **N-DIAGNOSTICS-ML-STRATEGY** — Phase 4bm-A does not authorize ML
  training, ML model design, feature ranking, meta-labeling, strategy
  implementation, signal generation, backtest execution, or any
  computation of PnL / MFE / MAE / R-multiple / equity / position /
  alpha / edge / prediction / model-score / decision-score /
  entry-exit / strategy output.
- **N-PHASE-5** — Phase 4bm-A does not authorize Phase 4 canonical,
  Phase 5, paper / shadow, live-readiness, deployment, or
  exchange-write.
- **N-VERDICT-LOCK** — Phase 4bm-A does not revise any retained
  verdict (H0, R3, R1a, R1b-narrow, R2, F1, D1-A, 5m thread, V2, G1,
  C1) and does not change any project lock. It does not amend M0
  governance, the post-null cooldown rule, the cooled-down families
  list, the memo template, the Phase 4al refined no-rescue rule, the
  §13 boundary, the §14 hierarchy, the Phase 4aw
  `flip_research_eligible(...)` always-raises invariant, the Phase
  4bb-F canonical path policy, or the Phase 4bl-F R-SIDECAR-CRLF
  rule and tier model.

### Conditional next, not authorized

- Future operator-authorized merge of this Phase 4bm-A branch into
  `main` with a Phase 4bm-A merge-closeout per
  `docs/00-meta/process/merge-closeout-standard.md`. Tier 1.
- Followed conditionally by a separately authorized future
  **Phase 4bm-B — Multi-Day Normalization Implementation** that
  implements this design exactly. Tier 1.
- Or alternatively, remain-paused while the operator considers
  broader project direction.

None of the above is authorized by Phase 4bm-A.
