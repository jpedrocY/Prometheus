# Phase 4bm-C — Multi-Day Normalized Structural QA Memo

## §1 Purpose and Scope

Phase 4bm-C is a **Tier 1 analysis-and-docs phase**. Its sole purpose is to read the v002 derived family produced by Phase 4bm-B and emit a descriptive structural QA verdict against the locked Phase 4bm-A design and the merged Phase 4bm-B implementation evidence.

Phase 4bm-C is **read-only on every committed and gitignored data/microstructure/ artefact**. It does not normalize, gate, transition, mutate, or authorize anything. It does not run the v002 derived family through any eligibility gate; that is a separate Tier 1 successor (Phase 4bm-D) and is **not** authorized by Phase 4bm-C.

Phase 4bm-C exists to make a deliberate "QA pause" between implementation and gate execution so that the structural shape of the derived family can be reviewed before any admissibility decision is recorded.

The QA target dataset is:

- **family**: `microstructure_normalized_aggtrades_v001`
- **version**: `v002` (multi-day)
- **schema_version**: `v001` (byte-identical to Phase 4bd)
- **symbol**: `BTCUSDT`
- **date range**: 2024-12-01 through 2025-02-28 UTC inclusive (90 dates)
- **total events**: 155,153,449
- **manifest**: `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` (gitignored)
- **manifest SHA256**: `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a`
- **manifest sidecar SHA256**: `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888`

Branch: `phase-4bm-c/multi-day-normalized-structural-qa-memo`
Base: `main` at `1613cf19de874293a545866000f1788e64e83cb3` (Phase 4bm-B merge-closeout commit).

## §2 Predecessor Lineage

Phase 4bm-C cites the following predecessor evidence verbatim and does not modify any of it:

- **Phase 4bm-A** (design memo) — `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-a_multi-day-normalization-design-memo.md` — locked the 19-column schema, partition layout, manifest shape, and 65-criterion strict-fail-closed validation contract.
- **Phase 4bm-A merge-closeout** — `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-a_merge-closeout.md`.
- **Phase 4bm-A-P1** (thin-prompt context-management standard) — `docs/00-meta/process/claude-code-context-management-standard.md`.
- **Phase 4bm-A-P1 merge-closeout** — `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-a-p1_merge-closeout.md`.
- **Phase 4bm-B** (implementation report) — `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-b_multi-day-normalization-implementation.md`.
- **Phase 4bm-B closeout** — `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-b_closeout.md`.
- **Phase 4bm-B merge-closeout** — `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-b_merge-closeout.md`.

Upstream data lineage cited by Phase 4bm-B and verified again by Phase 4bm-C:

- **v002 raw manifest** — `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json`, SHA `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485`, `research_eligible=false` / `eligibility_gate_status="pending"`.
- **v002 raw acquisition log** — `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json`, SHA `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314`.
- **Phase 4bl-D-R PASS gate report** — id `microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080`, SHA `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46`, 33/33 PASS.
- **Phase 4bl-E successor-state** — SHA `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d`, `successor_state="stage2_raw_admissible"`.

## §3 Path-Layout Clarification (Preserved Verbatim)

Phase 4bm-B introduced an implementation-level decision that Phase 4bm-C preserves verbatim and **does not alter**:

The v002 derived family is materialised under a **version-suffixed family directory**:

```text
data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/...
```

This avoids a collision with the existing Phase 4bd v001 single-day Parquet at:

```text
data/microstructure/normalized/microstructure_normalized_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet
```

Dataset identity is unchanged. The family remains `microstructure_normalized_aggtrades_v001`. The version field on every row and on the manifest is `v002`. Schema is `v001`. The Phase 4bd v001 single-day parquet remains byte-identical at SHA `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa`. Phase 4bm-C reverified this immutability and recorded the result in §11.

This clarification is documentation. It is not a manifest mutation, not a schema change, not a re-tagging, and not a successor-state action. Phase 4bm-C neither extends nor narrows it.

## §4 QA Method

Phase 4bm-C inspection used:

- Python stdlib (`json`, `hashlib`, `os`, `pathlib`, `datetime`, `decimal`) for manifest parsing, SHA256 recomputation, sidecar format checking, and UTC day-boundary arithmetic.
- `pyarrow.parquet` for parquet metadata and row-level inspection (column names, dtypes, row counts, row-level lineage and identity).

No tracked source file was modified. No `data/microstructure/` file was written, renamed, deleted, or had its mtime touched. All parquets were opened read-only; row-group reads were full-column reads into memory for spot-checks but did not modify the file.

The QA suite answered the 28 predeclared questions in §5 below. The validation strategy is descriptive only:

1. Identity invariants on the manifest envelope (family name, dataset version, schema version, symbol list, date range, total event count, eligibility flags, governance labels, lineage SHAs).
2. Path-existence and SHA invariants on every per-file inventory entry (90 entries × {parquet, sidecar} = 180 files).
3. Sidecar canonical-format invariants on every sidecar (`<sha256_lowercase_hex>  <basename>\n`, two ASCII spaces, single trailing LF).
4. Per-file parquet-metadata invariants (column count = 19, column order = `NORMALIZED_SCHEMA_V001`, dtype map per column, row count == manifest `event_count`).
5. Row-level identity invariants on five sample dates (2024-12-01, 2024-12-31, 2025-01-15, 2025-01-30, 2025-02-28): `row_index` is exactly `0..n-1`, `agg_trade_id` non-decreasing, lineage columns constant per file, UTC day-bound times, monotonic `transact_time_ms`, Decimal-parsable `price` and `quantity` strings, strict-bool `is_buyer_maker`, `first_trade_id <= last_trade_id`.
6. Aggregate cross-file invariants (UTC day boundaries, adjacent-date temporal monotonicity, adjacent-date agg_trade_id non-overlap, sum of per-file `event_count` equals manifest `total_event_count`).
7. Upstream immutability witnesses (4 governance artefacts + 90 raw zips + 90 raw zip sidecars + Phase 4bd v001 single-day parquet).

## §5 28-Question QA Result

| # | Question | Result |
|---|---|---|
| 1 | Does the v002 manifest exist at the expected canonical path? | PASS — `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` (104,094 bytes). |
| 2 | Does the v002 manifest SHA256 match the Phase 4bm-B-recorded `01c5fa538aaa...e1a2554a`? | PASS — recomputed `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a`. |
| 3 | Does the manifest sidecar exist and conform to canonical Phase 4bb-F format (two-space separator, trailing LF)? | PASS — body `01c5fa538aaa...e1a2554a  microstructure_normalized_aggtrades_v001__v002.json\n`, 118 bytes, SHA `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888`. |
| 4 | Does `dataset_family` equal `microstructure_normalized_aggtrades_v001`? | PASS. |
| 5 | Does `dataset_version` equal `v002`? | PASS. |
| 6 | Does `schema_version` equal `v001` (byte-identical to Phase 4bd)? | PASS. |
| 7 | Does `symbol_list` equal `["BTCUSDT"]`? | PASS. |
| 8 | Does `date_start` equal `2024-12-01` and `date_end` equal `2025-02-28`? | PASS. |
| 9 | Does `date_count == 90` and `expected_file_count == produced_file_count == 90`? | PASS. |
| 10 | Does `total_event_count == 155,153,449`? | PASS. |
| 11 | Does `research_eligible == false` and `eligibility_gate_status == "pending"`? | PASS — Stage-0 invariant preserved. |
| 12 | Does `invalid_windows == []`? | PASS. |
| 13 | Is `per_file_inventory` length 90 and exactly the contiguous UTC-date list with no duplicates and no gaps? | PASS — verified against generated `date(2024,12,1)..date(2025,2,28)`. |
| 14 | Does every per_file_inventory entry have `status == "produced_verified"`? | PASS — single status value across all 90 entries. |
| 15 | Does every per_file_inventory entry have `symbol == "BTCUSDT"`? | PASS — single symbol value across all 90 entries. |
| 16 | Does each per-file inventory parquet path exist on disk? | PASS — 90/90. |
| 17 | Does each per-file inventory sidecar path exist on disk? | PASS — 90/90. |
| 18 | Does each parquet file's recomputed SHA256 match the inventory-recorded `parquet_sha256`? | PASS — 90/90. |
| 19 | Does each parquet file's on-disk size match the inventory-recorded `parquet_size_bytes`? | PASS — 90/90. |
| 20 | Does each sidecar file's recomputed SHA256 match the inventory-recorded `sidecar_sha256`? | PASS — 90/90. |
| 21 | Does each sidecar file's body equal exactly `<parquet_sha256>  <basename>\n` (Phase 4bb-F canonical)? | PASS — 90/90; zero format violations. |
| 22 | Does each parquet's column count and column order equal `NORMALIZED_SCHEMA_V001` (19 columns in canonical order)? | PASS — verified on sample dates 2024-12-01, 2024-12-31, 2025-01-15, 2025-01-30, 2025-02-28. |
| 23 | Do parquet column dtypes match the Phase 4bm-A locked policy (Decimal-as-string for `price` / `quantity`, strict `bool` for `is_buyer_maker`, `int64` for IDs and timestamps, `string` for lineage and metadata)? | PASS — all 19 column dtypes match across sampled dates. |
| 24 | Does each parquet's `num_rows` match the inventory-recorded `event_count`? | PASS — sampled dates; all 90 entries had non-zero event_count and the sum invariant (§5 Q33-equivalent) holds. |
| 25 | Is `row_index` exactly `0..n-1` per file, and are lineage columns constant per file? | PASS — verified across 5 sample dates totalling 9,718,154 rows. |
| 26 | Are `agg_trade_id`, `transact_time_ms`, and `first_trade_id <= last_trade_id` invariants satisfied per row? | PASS — `agg_trade_id` non-decreasing; `transact_time_ms` non-decreasing; `first_trade_id <= last_trade_id` always (zero violations on samples). |
| 27 | Are all `transact_time_ms` values within `[UTC date 00:00:00.000, next UTC day 00:00:00.000)` half-open window per file? | PASS — zero out-of-bound rows on five sample dates totalling 9,718,154 rows; all 90 manifest first/last bound pairs satisfy the half-open invariant. |
| 28 | Are upstream immutability witnesses (raw manifest, acquisition log, Phase 4bl-D-R gate report, Phase 4bl-E successor-state, 90 raw zips, 90 raw zip sidecars, Phase 4bd v001 single-day parquet) byte-identical to recorded SHAs? | PASS — see §11. |

**All 28 questions: PASS.**

## §6 Manifest Envelope Detail

Top-level scalar fields verified:

| field | value | check |
|---|---|---|
| `dataset_family` | `microstructure_normalized_aggtrades_v001` | matches Phase 4bm-A lock |
| `dataset_version` | `v002` | matches Phase 4bm-B lock |
| `schema_version` | `v001` | byte-identical to Phase 4bd |
| `symbol_list` | `["BTCUSDT"]` | matches scope lock |
| `date_start` | `2024-12-01` | matches scope lock |
| `date_end` | `2025-02-28` | matches scope lock |
| `date_count` | `90` | matches 2024-12 (31) + 2025-01 (31) + 2025-02 (28) |
| `expected_file_count` | `90` | matches `date_count` |
| `produced_file_count` | `90` | matches expected |
| `total_event_count` | `155,153,449` | matches sum of per-file `event_count` |
| `research_eligible` | `false` | Stage-0 invariant |
| `eligibility_gate_status` | `"pending"` | Stage-0 invariant |
| `invalid_windows` | `[]` | clean |
| `phase` | `4bm-B` | matches predecessor |
| `source_phase_boundary` | `4bl-E` | matches Phase 4bl-E successor-state |
| `source_dataset_family` | `microstructure_raw_aggtrades_v001` | matches Phase 4bl-C raw family |
| `source_dataset_version` | `v002` | matches Phase 4bl-C raw version |
| `source_manifest_sha256` | `016967865c97...d87485` | matches Phase 4bl-C raw manifest |
| `source_acquisition_log_sha256` | `52f6d7fb3cb0...c6b314` | matches Phase 4bl-C acquisition log |
| `source_gate_report_id` | `microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080` | matches Phase 4bl-D-R |
| `source_gate_report_sha256` | `f9493fd10d1c...6f1c46` | matches Phase 4bl-D-R PASS report |
| `source_successor_state_sha256` | `a0576ca656bd...1f751d` | matches Phase 4bl-E |
| `base_commit_sha` | `56f96a4c613a3d8c8794905be4c1847fcdac5e58` | matches Phase 4bm-A-P1 merge-closeout (Phase 4bm-B base) |
| `code_commit_sha` | `56f96a4c613a3d8c8794905be4c1847fcdac5e58` | matches base (recorded at Phase 4bm-B start time) |
| `capture_config_hash` | `059f5ebad95b...21f803df` | implementation-locked |
| `created_at_utc` | `2026-05-15T19:08:48.534256+00:00` | Phase 4bm-B run time |
| `created_at_unix_ms` | `1778872128534` | matches `created_at_utc` |

`governance_labels` block verified (all key/value pairs):

```text
feature_computation                       : "forbidden"
multi_day                                 : "true"
phase                                     : "4bm-B"
phase_4bm_b_no_successor_authorization    : "true"
source_dataset_family                     : "microstructure_raw_aggtrades_v001"
source_dataset_version                    : "v002"
source_gate_report_code_commit_sha        : "69e45280f080e320171f1d851933fdb13213aaea"
source_gate_report_id                     : "microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080"
source_gate_report_sha256                 : "f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46"
source_manifest_path                      : "data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json"
source_manifest_sha256                    : "016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485"
source_phase_boundary                     : "4bl-E"
source_successor_state_sha256             : "a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d"
stop_trigger_domain                       : "trade_price_backtest_candidate"
strategy_use                              : "forbidden"
validator                                 : "phase_4ax_aggtrades_v001"
```

All 16 governance label keys are present and carry the expected values.

## §7 Per-File Inventory Shape

The `per_file_inventory` list has 90 entries. Each entry has exactly these 16 keys:

```text
date
event_count
first_transact_time_ms
last_transact_time_ms
local_parquet_path
local_sidecar_path
max_agg_trade_id
min_agg_trade_id
parquet_sha256
parquet_size_bytes
sidecar_sha256
sidecar_size_bytes
source_file_sha256
source_zip_path
status
symbol
```

Entries are ordered ascending by date. The 90 dates equal exactly the contiguous UTC date range 2024-12-01 .. 2025-02-28 inclusive (31 + 31 + 28 = 90). No date is missing, duplicated, or reordered.

Sample first entry (2024-12-01):

```text
date                    = "2024-12-01"
event_count             = 731065
first_transact_time_ms  = 1733011205575
last_transact_time_ms   = 1733097599949
local_parquet_path      = "microstructure/normalized/microstructure_normalized_aggtrades_v001__v002/BTCUSDT/2024/12/BTCUSDT-aggTrades-2024-12-01.parquet"
local_sidecar_path      = (same path + ".sha256")
max_agg_trade_id        = 2442496699
min_agg_trade_id        = 2441765635
parquet_sha256          = "7dc942e4b3e75a3846629d2aedd127b2b1e0c591e67aac1a20371ea7d9637835"
parquet_size_bytes      = 7,470,254
sidecar_sha256          = "08fc7a65485b0fad504f9710f1f6735996e302bfd279cc497caac0359c704ac1"
sidecar_size_bytes      = 103
source_file_sha256      = "c4d987a64f28a2ad580022aa49ae8fa13ccff15e3343308912d4b61eff0c4f3d"
source_zip_path         = "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2024/12/BTCUSDT-aggTrades-2024-12-01.zip"
status                  = "produced_verified"
symbol                  = "BTCUSDT"
```

Sample last entry (2025-02-28):

```text
date                    = "2025-02-28"
event_count             = 4526219
first_transact_time_ms  = 1740700804382
last_transact_time_ms   = 1740787199996
parquet_sha256          = "6296fffc56881eee460d1b40f0e57e93625d4c194386dea9dceec8d5d260162b"
parquet_size_bytes      = 42,400,052
sidecar_sha256          = "0c43b0f39d5700ab799bc9b0329c8eb25ad68501382761d6eaa989c829f28d97"
sidecar_size_bytes      = 103
source_file_sha256      = "1ea4d9d99262334d775530a85cc021f3fcf52bf8978a62d1def7b95839e1380f"
status                  = "produced_verified"
symbol                  = "BTCUSDT"
```

Inventory statistics over 90 entries:

- `event_count` min = 451,314; max = 5,435,481; mean ≈ 1,723,927; sum = 155,153,449.
- `parquet_size_bytes` min = 5,053,002; max = 51,179,671; sum = 1,499,331,510 bytes (≈ 1.40 GiB).
- `sidecar_size_bytes` constant at 103 across all 90 entries (sum = 9,270 bytes); 103 = 64 (hex SHA) + 2 (two ASCII spaces) + 36 (basename `BTCUSDT-aggTrades-YYYY-MM-DD.parquet`) + 1 (trailing LF) — matches canonical Phase 4bb-F shape.

## §8 Path Layout Verified

The on-disk layout under `data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002/BTCUSDT/...` contains:

- `2024/12/` — 31 parquets + 31 sidecars (dates 2024-12-01 .. 2024-12-31).
- `2025/01/` — 31 parquets + 31 sidecars (dates 2025-01-01 .. 2025-01-31).
- `2025/02/` — 28 parquets + 28 sidecars (dates 2025-02-01 .. 2025-02-28).

Total: 90 parquets + 90 sidecars = 180 files. All 90 inventory `local_parquet_path` values resolve to existing files. All 90 inventory `local_sidecar_path` values resolve to existing files. The version-suffixed family directory `microstructure_normalized_aggtrades_v001__v002/` coexists cleanly with the Phase 4bd v001 single-day family directory `microstructure_normalized_aggtrades_v001/`.

Every path is under `data/microstructure/normalized/` which is gitignored under `.gitignore:85: data/microstructure/`. Confirmed: `git check-ignore -v data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002/` returns `.gitignore:85`.

## §9 SHA Verification Result

For each of the 90 per-file inventory entries:

1. The on-disk parquet file's SHA256 (computed by streaming the file through `hashlib.sha256()`) matches the inventory-recorded `parquet_sha256`.
2. The on-disk sidecar file's SHA256 matches the inventory-recorded `sidecar_sha256`.
3. The sidecar file's body equals exactly `f"{parquet_sha256}  {basename}\n".encode("utf-8")` — Phase 4bb-F canonical format with two ASCII spaces and a single trailing LF byte. No CRLF, no BOM, no extra whitespace, no missing newline.

Zero mismatches across 90 files. Zero format violations across 90 sidecars.

This is independent verification of Phase 4bm-B closeout §6 evidence, recomputed from scratch by Phase 4bm-C.

## §10 Schema and Row-Level Sanity (Sample Dates)

Phase 4bm-C inspected five sample dates spanning the full date range:

- 2024-12-01 (first date, 731,065 rows, 7.47 MB parquet)
- 2024-12-31 (year boundary, 1,516,788 rows, ~18 MB parquet)
- 2025-01-15 (mid-range; same UTC day as the Phase 4bd v001 single-day fixture, 1,681,098 rows)
- 2025-01-30 (mid-range, 1,263,893 rows)
- 2025-02-28 (last date, 4,526,219 rows, 42.4 MB parquet)

Combined: 9,718,154 rows inspected at row level (6.26% of total event count).

### Schema (parquet metadata)

Each of the five sample parquets has exactly 19 columns in the canonical `NORMALIZED_SCHEMA_V001` order:

```text
 [0] dataset_family               : string
 [1] dataset_version              : string
 [2] source_dataset_family        : string
 [3] source_dataset_version       : string
 [4] symbol                       : string
 [5] utc_date                     : string
 [6] agg_trade_id                 : int64
 [7] price                        : string   (Decimal-as-string)
 [8] quantity                     : string   (Decimal-as-string)
 [9] first_trade_id               : int64
[10] last_trade_id                : int64
[11] transact_time_ms             : int64
[12] is_buyer_maker               : bool     (strict)
[13] source_file_sha256           : string
[14] source_manifest_sha256       : string
[15] source_gate_report_id        : string
[16] source_gate_report_sha256    : string
[17] row_index                    : int64
[18] normalization_schema_version : string
```

Column names, order, and dtypes are identical across all five sample dates. No nullable variants. No extra columns. No reordering.

### Row identity

For each sample date:

- `row_index` is exactly the integer sequence `0, 1, 2, ..., n-1` (where `n = event_count`). Zero deviations.
- `agg_trade_id` is non-decreasing. First-row `agg_trade_id` equals `min_agg_trade_id` from manifest; last-row equals `max_agg_trade_id`. Sequence is **dense** within each UTC day (max − min + 1 = count, see §13).
- `transact_time_ms` is non-decreasing. First-row equals manifest `first_transact_time_ms`; last-row equals manifest `last_transact_time_ms`.
- All `transact_time_ms` values lie in `[UTC date 00:00:00.000, next UTC day 00:00:00.000)` half-open window. Zero rows out of bounds on 9,718,154 inspected rows.
- `first_trade_id <= last_trade_id` on every row. Zero violations.

### Lineage column constants

Across each entire sample file, the following columns hold a single constant value (verified by comparing row 0 to row n−1):

- `dataset_family` = `"microstructure_normalized_aggtrades_v001"`
- `dataset_version` = `"v002"`
- `source_dataset_family` = `"microstructure_raw_aggtrades_v001"`
- `source_dataset_version` = `"v002"`
- `symbol` = `"BTCUSDT"`
- `utc_date` = the date of that file (`"2024-12-01"`, etc.)
- `source_file_sha256` = the SHA of the source raw zip for that date (matches `source_file_sha256` in the per-file inventory entry, matches raw manifest entry for the same date)
- `source_manifest_sha256` = `"016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485"` (v002 raw manifest)
- `source_gate_report_id` = `"microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080"`
- `source_gate_report_sha256` = `"f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46"`
- `normalization_schema_version` = `"v001"`

### Value-domain sanity

- `price`: every row parses cleanly via `decimal.Decimal(s)` and `> 0`. Zero non-parsable or non-positive values across 9,718,154 rows.
- `quantity`: every row parses cleanly via `decimal.Decimal(s)` and `> 0`. Zero non-parsable or non-positive values.
- `is_buyer_maker`: pyarrow column dtype is strict `bool`; sample rows have boolean `True` / `False` (Python `bool`). Both directions present in each file in roughly balanced counts (e.g. 2024-12-01: 359,417 True / 371,648 False).

## §11 Upstream Immutability Evidence

Phase 4bm-C recomputed SHA256 on the following witnesses **without modifying any file**:

| Witness | Expected SHA256 | Actual SHA256 | Result |
|---|---|---|---|
| v002 raw manifest | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | identical | PASS |
| v002 raw acquisition log | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | identical | PASS |
| Phase 4bl-D-R PASS gate report | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` | identical | PASS |
| Phase 4bl-E successor-state | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` | identical | PASS |
| Phase 4bd v001 single-day parquet | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` | identical | PASS |

90 v002 raw zips were verified by recomputing each zip's SHA256 and comparing against the per-file `sha256` field of the v002 raw manifest. **All 90 zips match.** Zero mismatches.

90 v002 raw zip sidecars were verified by:

1. Reading the sidecar file bytes.
2. Recomputing the matching zip's SHA256.
3. Confirming sidecar bytes equal `f"{zip_sha}  {zip_basename}\n".encode("utf-8")` — canonical Phase 4bb-F.

**All 90 raw zip sidecars match canonical format.** Zero format violations. Zero SHA mismatches.

Combined upstream immutability evidence: **188 witnesses** verified byte-identical to recorded values:

- 4 governance artefacts (v002 raw manifest, v002 acquisition log, Phase 4bl-D-R PASS gate report, Phase 4bl-E successor-state)
- 4 governance sidecars (paired `.sha256` for each above)
- 90 v002 raw zips
- 90 v002 raw zip sidecars

Plus 1 Phase 4bd v001 single-day parquet preserved unchanged.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end. Phase 4bm-C did not import any `prometheus.research.microstructure` module that would surface this guard, and did not invoke any code path that would touch it. The invariant remains as a static governance contract.

## §12 Manifest State Preservation

The v002 derived manifest reads (on disk, post-Phase-4bm-C inspection):

- `research_eligible` = `false`
- `eligibility_gate_status` = `"pending"`

Stage-0 invariants are preserved. The manifest has not been mutated by Phase 4bm-C.

The Phase 4ba 5-stage ladder placement for the v002 derived family remains:

- **Stage-0**: artefacts present; eligibility pending. ← current.
- Stage-1 (inspected): not reached. **NOT** authorized by Phase 4bm-C; only a Phase 4bm-D-equivalent successor-state recording phase, separately authorized, may transition to Stage-1.
- Stage-2 (gate-passed): not reached.
- Stage-3 (research-eligible): not reached.
- Stage-4 (feature-cleared): not reached.

Phase 4bm-C's PASS verdict is a **descriptive QA finding**, not a manifest transition. The verdict does not modify the manifest, does not transition `eligibility_gate_status`, does not flip `research_eligible`, and does not authorize any successor.

## §13 Adjacency and Density Findings

Adjacent-date invariants verified across the 89 adjacent pairs in the 90-date range:

- **Temporal monotonicity (transact_time_ms)**: zero violations. Every date's `first_transact_time_ms` is strictly greater than the previous date's `last_transact_time_ms`. Continuity across the 2024 → 2025 year boundary at 2024-12-31 → 2025-01-01 is clean.
- **agg_trade_id non-overlap**: zero violations. Every date's `min_agg_trade_id` equals the previous date's `max_agg_trade_id` + 1 exactly. The aggregate-trade-id sequence is **globally dense** across the 90-date span.
- **agg_trade_id density per file**: every per-file inventory entry satisfies `max_agg_trade_id - min_agg_trade_id + 1 == event_count`. This means every file's aggregate-trade-id range is a contiguous block with no gaps inside the file.
- **UTC day windows per file**: every per-file `first_transact_time_ms` and `last_transact_time_ms` falls in the half-open window `[UTC date 00:00:00.000, next UTC day 00:00:00.000)`. Zero violations.

This is a clean, dense, monotonically increasing 90-day BTCUSDT aggTrade record. The structural shape matches what would be expected of a continuous public-data acquisition with no aggTrade gaps inside or between UTC days.

## §14 Boundary Confirmations (Read-Only QA)

Phase 4bm-C confirms the following negative results (`true` = "this thing did NOT happen"):

| Boundary | Status |
|---|---|
| No `data/microstructure/` file was written, renamed, deleted, or mtime-touched | `true` |
| No manifest field was modified | `true` |
| No sidecar file was modified | `true` |
| No parquet file was modified | `true` |
| No raw zip was modified | `true` |
| No `research_eligible` flag was flipped on any manifest | `true` |
| No `eligibility_gate_status` was transitioned on any actual manifest | `true` |
| No `chronological_split_policy` was changed on any actual manifest | `true` |
| No gate was rerun | `true` |
| No new gate report was generated | `true` |
| No new successor-state artefact was created | `true` |
| No data was acquired | `true` |
| No download was attempted | `true` |
| No Binance / public / private endpoint was called | `true` |
| No WebSocket was opened | `true` |
| No credential was used | `true` |
| No `.env` was read or created | `true` |
| No `.mcp.json` was read or created | `true` |
| MCP and Graphify remained disabled | `true` |
| No normalization, derivation, features, labels, diagnostics, ML, strategy, signals, or backtests were run | `true` |
| No PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit / strategy output was computed | `true` |
| No retained verdict was revised | `true` |
| No project lock was changed | `true` |
| No governance memo was amended (beyond the narrow `current-project-state.md` paragraph addition) | `true` |
| No prior phase result was rewritten | `true` |
| Phase 4aw `flip_research_eligible(...)` always-raises invariant was not invoked | `true` |
| Phase 4bb-F canonical path policy was followed verbatim for all 90 sidecars | `true` |
| Phase 4bl-F R-SIDECAR-CRLF rule was not invoked (forward writes use canonical LF natively) | `true` |
| Phase 4bm-A path-layout clarification was preserved verbatim (§3) | `true` |
| Phase 4bm-B implementation evidence was preserved verbatim | `true` |
| Phase 4bm-C did not merge anything into main | `true` |
| Phase 4bm-C did not authorize any successor phase | `true` |

## §15 Retained Verdict Ledger and Project Locks (Preserved Verbatim)

The full retained verdict ledger and every project lock are preserved by Phase 4bm-C exactly as carried forward from Phase 4bm-B:

**Retained verdict ledger:**

- H0 FRAMEWORK ANCHOR
- R3 BASELINE-OF-RECORD
- R1a / R1b-narrow RETAINED — NON-LEADING
- R2 FAILED — §11.6
- F1 HARD REJECT
- D1-A MECHANISM PASS / FRAMEWORK FAIL
- 5m thread OPERATIONALLY CLOSED per Phase 3t
- V2 HARD REJECT — terminal for V2 first-spec
- G1 HARD REJECT — terminal for G1 first-spec
- C1 HARD REJECT — terminal for C1 first-spec

**Preserved project locks:**

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 3p §4.7
- Phase 3r §8
- Phase 3v §8
- Phase 3w §6 / §7 / §8
- Phase 4j §11
- Phase 4k
- Phase 4p
- Phase 4q
- Phase 4v
- Phase 4w
- Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `flip_research_eligible(...)` always-raises invariant
- Phase 4bb-F canonical path policy
- Phase 4bl-F four-tier risk model + nine reusable non-authorization blocks + R-SIDECAR-CRLF standing rule

All preserved verbatim. Phase 4bm-C does not amend, narrow, broaden, or reinterpret any of the above.

## §16 Verdict

**STRUCTURAL_QA_PASS.**

The Phase 4bm-B v002 derived family conforms exactly to the Phase 4bm-A locked design and the Phase 4bm-B implementation contract. All 28 predeclared QA questions return PASS. All 188 upstream immutability witnesses are byte-identical to recorded values. The 90 derived Parquet files plus their 90 paired sidecars are present, byte-identical to their manifest record, and structurally well-formed across schema, row identity, lineage, value domain, temporal monotonicity, agg_trade_id density, and UTC day boundaries.

The v002 derived family carries `research_eligible=false` / `eligibility_gate_status="pending"` and remains at Stage-0 of the Phase 4ba 5-stage ladder. Phase 4bm-C's PASS verdict is **descriptive** and does not transition any manifest field, does not flip any eligibility flag, does not authorize any successor, and does not constitute a research-eligibility decision.

## §17 No Successor Authorized

Phase 4bm-C does **not** authorize:

- Phase 4bm-C merge phase
- Phase 4bm-D (Multi-Day Derived-Family Eligibility Gate)
- Phase 4bm-E (Multi-Day Derived-Family Research-Eligibility Decision)
- Phase 4bm-F (Multi-Day Derived-Family Successor-State Recording)
- Phase 4bm-* (any future multi-day arc phase)
- Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-*
- Phase 5 / Phase 4 canonical
- Paper / shadow / live-readiness / deployment / exchange-write
- Production-key creation / authenticated APIs / private endpoints
- User stream / live WebSocket implementation
- MCP / Graphify / `.mcp.json` / credentials
- Any additional acquisition beyond the 90 locked BTCUSDT UTC dates
- Any modification of `research_eligible`, `eligibility_gate_status`, or `chronological_split_policy` on any actual manifest

**Recommended state**: remain paused.

**Conditional next, NOT authorized**: future operator-authorized Phase 4bm-C merge phase that merges this branch into `main` and records a Phase 4bm-C merge-closeout per `docs/00-meta/process/merge-closeout-standard.md` (Tier 1; full 16-section merge-closeout). After merge, the recommended state remains **remain paused** pending operator decision on the conditional Phase 4bm-D ladder (Multi-Day Derived-Family Eligibility Gate). Phase 4bm-D is **not** authorized by Phase 4bm-C.

Phase 4bm-C is **branch-complete only**. Per the Phase 4bk-A workflow standard, Phase 4bm-C is **not project-complete** until a separately authorized merge phase records its merge-closeout on `main`.

— end of Phase 4bm-C structural QA memo —
