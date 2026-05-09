# Phase 4bc — AggTrades Normalization Design Memo

**Phase identity:** Phase 4bc — AggTrades Normalization Design Memo.
**Type:** docs-only normalization-design memo.
**Date:** 2026-05-07.
**Branch:** `phase-4bc/aggtrades-normalization-design`.
**Status:** drafted; pending operator review.

---

## 1. Phase header

Phase 4bc is a docs-only design memo for a future normalized derived aggTrades dataset family. It defines the schema, manifest contract, transformation rules, validation checks, eligibility model, and governance for a normalized derived family that **may** in the future be produced from the Phase 4az raw aggTrades archive — only after a separately authorized normalization-implementation phase.

Phase 4bc is **text only**. It does not normalize data, implement code, modify any artefact under `data/microstructure/`, generate derived datasets, compute features, train ML, create strategies, run backtests, or authorize any successor.

---

## 2. Current state

| Item | Value |
| ---- | ----- |
| `main` HEAD | `f231a09baae7872eab2fff62e7cebb11e60c3582` |
| `origin/main` HEAD | `f231a09baae7872eab2fff62e7cebb11e60c3582` |
| Local / origin sync | in sync |
| Phase 4bb-E merge commit (ancestor verified) | `2962a72b481858cab0264657cb0de3b2ee0648d7` |
| Phase 4bb-E merge-closeout file | `docs/00-meta/implementation-reports/2026-05-07_phase-4bb-e_merge-closeout.md` (present on `main`) |
| `data/microstructure/` gitignored | yes (`.gitignore:85`) |
| Phase 4az manifest | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json` (`research_eligible=false`, `eligibility_gate_status=pending`, mtime unchanged since Phase 4az `2026-05-07 21:55`) |
| Phase 4bb-D local gate report | present on this workspace; recomputed SHA256 `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` matches sidecar bit-for-bit |

---

## 3. Inputs reviewed

- Phase 4az acquisition + manifest (BTCUSDT 2025-01-15; 1,681,098 events; raw zip SHA `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`).
- Phase 4ba staged eligibility-gate model + 5-stage ladder + 45-check definition.
- Phase 4bb-A structural QA (21 / 21 PASS).
- Phase 4bb-B execution plan.
- Phase 4bb-C primitive (`eligibility_io.py`, `eligibility_gate.py`, `eligibility_checks.py`, `eligibility_report.py`).
- Phase 4bb-D PASS gate report (`overall_status=pass`; 45 / 45 PASS; 0 invalid-window candidates; report SHA `96f09159...`; `research_eligible_after=False`; `no_successor_authorization=True`).
- Phase 4bb-E successor-state policy memo (Option A default; original v001 manifest immutable; raw-family `research_eligible` permanent false; sibling successor-state manifest only via separately authorized future phase; doubled `gate-reports/gate-reports/` path documented as known and deferred).
- Phase 4aw scaffold types (`MicrostructureManifest`, `RawWriter`, `InvalidWindow`, `EligibilityGateStatus`, `MicrostructureConfig`, `ALLOWLIST_PATTERNS` / `DENYLIST_TOKENS`).
- Phase 4ax aggTrades-only collector primitives (`validate_aggtrade_payload`, `AggTradeValidationError`, `TakerSide`).
- Project locks: §11.6, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6/§7/§8, Phase 4j §11, Phase 4ak M0 + post-null cooldown, Phase 4al refined no-rescue rule + §13 + §14.

No live endpoints, credentials, `.env`, `.mcp.json`, MCP, Graphify, or external services were consulted.

---

## 4. Scope

- Define the proposed normalized derived aggTrades dataset family name and version semantics.
- Define the raw-to-normalized field mapping.
- Define the proposed normalized schema (trade-record-level, lossless, no features / labels / signals).
- Define timestamp semantics, numeric precision, partitioning, manifest contract, invalid-window propagation, and lossless transformation rules.
- Define normalization-time validation checks for any future implementation.
- Define the eligibility model for the normalized derived family, distinguishing Stage 2 (gate-passed) vs Stage 3 (normalized).
- Define `research_eligible` policy for the normalized family.
- Define feature-computation, ML, and strategy boundaries.
- Define an implementation plan and acceptance criteria for a future separately authorized normalization-implementation phase.
- Recommend a conservative bounded successor sequence and explicitly NOT authorize any successor.

---

## 5. Non-scope

Phase 4bc did NOT:

- modify source code;
- modify tests;
- modify scripts;
- implement a normalizer;
- run a normalizer;
- rerun the gate;
- generate a new gate report;
- delete, move, rename, or modify the existing Phase 4bb-D gate report or its sidecar;
- modify `data/microstructure/`;
- modify the Phase 4az manifest, raw zip, sidecar, or acquisition log;
- create a successor manifest;
- create a normalized derived dataset;
- create JSONL, Parquet, DuckDB, feature tables, labels, or derived datasets;
- flip `research_eligible`;
- transition `eligibility_gate_status` out of `pending`;
- acquire data;
- call public endpoints;
- call Binance APIs;
- open WebSockets;
- use private endpoints;
- request or use credentials;
- create `.env`;
- create `.mcp.json`;
- enable MCP or Graphify;
- compute features;
- compute returns, alpha, edge, opportunity rate, taker imbalance, sweep detection, aggressive-flow score, spread, depth, liquidity, slippage, order-flow, or execution-quality proxies;
- train ML;
- create a strategy;
- run backtests;
- revise retained verdicts;
- change project locks;
- amend M0;
- authorize Phase 4bd, Phase 4bb-F, Phase 4bb-G, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation.

---

## 6. Phase 4bb-D PASS gate-report dependency

The future normalizer must cite the Phase 4bb-D PASS gate report as the structural basis for normalizing the Phase 4az raw artefact. The cited evidence must include:

| Field | Value |
| ----- | ----- |
| `report_id` | `microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c` |
| `report_path` (local; gitignored) | `data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json` |
| Report SHA256 | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| Gate `code_commit_sha` | `aa612ba2778c97a5150b80064244b90d024bfa54` |
| `overall_status` | `pass` |
| Total checks / PASS / FAIL / NA / ERROR | `45 / 45 / 0 / 0 / 0` |
| Invalid-window candidates | `0` |
| `research_eligible_after` | `False` |
| `eligibility_gate_status_after` (recommendation only) | `pass` |
| `no_successor_authorization` | `True` |

The future normalizer manifest must record these fields verbatim under `governance_labels` so the lineage is reproducible without consulting the gitignored report file directly. If the operator re-derives the report at a future date by re-invoking `run_eligibility_gate` at the same `code_commit_sha` against the same Phase 4az artefacts, the recomputed report SHA must match `96f09159...` exactly (subject to Phase 4bb-F output-path hygiene if the operator wants the re-derived report to live at a non-doubled path).

---

## 7. Phase 4bb-E successor-state policy dependency

Phase 4bc operates strictly under the conservative posture adopted by Phase 4bb-E:

- The original Phase 4az manifest at `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json` is **immutable**. Phase 4bc will never modify it; any future Phase 4bd normalizer implementation must never modify it.
- Raw-family `research_eligible` is **permanently false**. The raw family `microstructure_raw_aggtrades_v001` is forever excluded from `research_eligible = true`, regardless of any gate or normalization outcome.
- The actual on-disk Phase 4az manifest's `eligibility_gate_status` remains `pending`. It may **only** transition to `pass` via a separately authorized future Phase 4bb-G that writes a sibling successor-state manifest (never overwrites v001). Phase 4bc does not require that transition; the future normalizer may proceed by citing the Phase 4bb-D PASS gate report directly.
- The doubled `gate-reports/gate-reports/` path in the Phase 4bb-D report path is documented as known Phase 4bb-C orchestrator behavior; it is **harmless** for the existing Phase 4bb-D report and does **not** block normalization design. A separately authorized Phase 4bb-F output-path-hygiene phase is the recommended cleanup before any future repeated gate execution but is not a prerequisite for Phase 4bd normalizer implementation.

---

## 8. Normalization objective

The future normalizer's objective is to produce, from a raw Binance USDⓈ-M Futures aggTrades archive (Phase 4az dataset family `microstructure_raw_aggtrades_v001`), a **lossless trade-record-level normalized derived dataset** suitable for downstream descriptive research. The normalizer must:

- read the raw archive read-only (no mutation);
- decompress in-memory;
- iterate every aggTrade row exactly once;
- pass every row through `prometheus.research.microstructure.aggtrades.validate_aggtrade_payload` (already part of the Phase 4ax / Phase 4bb-C surface);
- emit a normalized record per raw row, with deterministic ordering, lossless field mapping, and explicit lineage to the source archive, source manifest, and Phase 4bb-D PASS gate report;
- write the normalized output and its accompanying derived manifest under a separate `data/microstructure/normalized/` namespace (gitignored);
- never modify any raw artefact;
- never compute features, labels, signals, returns, alpha, edge, opportunity rate, or any execution-quality proxy.

The normalized output is **descriptive infrastructure**, not research evidence. Whether it ever becomes `research_eligible = true` depends on a separately authorized Stage-3 eligibility gate for the normalized family (see §17 below).

---

## 9. Proposed normalized dataset family name

**Proposed name:** `microstructure_normalized_aggtrades_v001`.

Rationale:

- The `microstructure_normalized_*` prefix mirrors the Phase 4aw scaffold naming convention (`microstructure_raw_*`, `microstructure_metrics_*`, `microstructure_replay_*`).
- The `aggtrades` segment makes the source family explicit.
- The `v001` suffix is the schema version (see §10–§11). A future schema-incompatible change would bump to `v002`; a backward-compatible additive change to `v001` may continue under the same family name with manifest-level versioning if appropriate (deferred to Phase 4bd planning).
- The family is **derived**. It is **not** the raw family `microstructure_raw_aggtrades_v001` and must not be confused with it.
- The family is **read-only** with respect to its source: any rebuild produces a new manifest record, never an in-place mutation.

Forbidden alternative names (no rescue / no rename of raw): `microstructure_raw_aggtrades_v002`, `microstructure_aggtrades_*` without the `normalized_` infix, or any name that implies mutation of the raw family.

---

## 10. Raw-to-normalized field mapping

The Phase 4az raw archive ships as a single CSV inside the `.zip` with these source columns (per Binance public archive convention; verified by Phase 4bb-A and Phase 4bb-D against the validator):

| Raw column | Phase 4ax canonical key | Description |
| ---------- | ----------------------- | ----------- |
| `agg_trade_id` (or `a`) | `a` | Aggregate trade ID; monotone non-decreasing per file |
| `price` (or `p`) | `p` | Trade price (string-decimal in source) |
| `quantity` (or `q`) | `q` | Trade quantity (string-decimal in source) |
| `first_trade_id` (or `f`) | `f` | First contributing trade ID |
| `last_trade_id` (or `l`) | `l` | Last contributing trade ID; `l >= f` |
| `transact_time` (or `T`) | `T` | UTC milliseconds; trade event time |
| `is_buyer_maker` (or `m`) | `m` | Boolean; `false` ⇒ taker buyer (BUY); `true` ⇒ taker seller (SELL) |

Optional stream-only field `E` (event time at exchange) is not present in the public archive CSV format; the future normalizer may simply not emit it.

The mapping is one-to-one: every raw row produces exactly one normalized row. Order-preserving — the normalized output is sorted by raw `row_index` (the zero-based row position within the source CSV after header detection).

---

## 11. Proposed normalized schema

The proposed normalized schema is **trade-record-level only**. Every column is either a direct lossless image of the raw aggTrade row, or a deterministic lineage / derivation field. **No feature, label, signal, return, alpha, edge, imbalance, sweep, or proxy column appears in this schema.**

Required columns (in declared order):

| Column | Type | Description |
| ------ | ---- | ----------- |
| `dataset_family` | string | Constant: `microstructure_normalized_aggtrades_v001` |
| `dataset_version` | string | Constant: `v001` |
| `source_dataset_family` | string | Constant: `microstructure_raw_aggtrades_v001` |
| `source_dataset_version` | string | Constant: `v001` |
| `symbol` | string | Uppercase Binance USDⓈ-M Futures symbol (e.g. `BTCUSDT`); same value as the source manifest's `symbol` and the archive path's symbol segment |
| `utc_date` | string | `YYYY-MM-DD`; the UTC day implied by the archive filename and confirmed by the source manifest's `start_time_ms` / `end_time_ms` range |
| `agg_trade_id` | int64 | Raw `a`; aggregate trade ID; non-decreasing per file |
| `price` | string | Raw `p` preserved verbatim as an exact-decimal **string** (no float rounding); downstream consumers must parse with `Decimal` to retain bit-for-bit precision |
| `quantity` | string | Raw `q` preserved verbatim as an exact-decimal **string** |
| `first_trade_id` | int64 | Raw `f`; first contributing trade ID |
| `last_trade_id` | int64 | Raw `l`; last contributing trade ID; `l >= f` |
| `transact_time_ms` | int64 | Raw `T`; UTC milliseconds; non-decreasing per file |
| `is_buyer_maker` | bool | Raw `m`; strict bool |
| `source_file_sha256` | string | 64-char lowercase hex SHA256 of the raw `.zip` (i.e. `f560c2e5...` for Phase 4az BTCUSDT 2025-01-15) |
| `source_manifest_sha256` | string | 64-char lowercase hex SHA256 of the raw manifest at the time of normalization (i.e. `a371edd4...` for Phase 4az v001) |
| `source_gate_report_id` | string | Phase 4bb-D `report_id` (e.g. `microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c`) |
| `source_gate_report_sha256` | string | 64-char lowercase hex SHA256 of the cited gate report (e.g. `96f09159...`) |
| `row_index` | int64 | Zero-based row position within the source CSV after header detection; the deterministic ordering key |
| `normalization_schema_version` | string | Constant: `v001` |

**Forbidden columns** (must NOT appear in this schema or any v001-compatible variant): any feature, label, signal, return, alpha, edge, opportunity-rate, taker-imbalance, sweep-detection, aggressive-flow-score, spread, depth, liquidity, slippage, order-flow, execution-quality, regime, trend, momentum, volatility, MFE / MAE, R-multiple, PnL, equity, position, or strategy column. **No derived analytic column may be added without bumping to a separate Stage-4 (feature-cleared) family in a separately authorized phase.**

The schema is intentionally narrow. Anything beyond direct row-image plus lineage belongs to Stage 4 (feature-cleared) and requires a separately authorized M0-cleared hypothesis-spec memo plus a Phase 4ak post-null-cooldown check before it may be designed, let alone implemented.

---

## 12. Timestamp semantics

| Timestamp | Source | Meaning | Storage |
| --------- | ------ | ------- | ------- |
| `transact_time_ms` | raw `T` | Trade event time at the exchange (UTC ms) | int64; non-decreasing per file |
| `utc_date` | derived from archive filename + manifest range | The UTC calendar day the archive represents (`YYYY-MM-DD`) | string |
| **Half-open day bound (lower)** | `utc_date * 86_400_000` | Inclusive | int64 ms |
| **Half-open day bound (upper)** | `(utc_date + 1) * 86_400_000` | Exclusive | int64 ms |
| Archive UTC date | filename slug (e.g. `2025-01-15`) | Canonical day label | string |
| Source manifest reference time (`start_time_ms` / `end_time_ms`) | source manifest fields | First / last `T` observed in raw | int64 ms |
| Derived file creation time (`created_at_utc_ms`) | normalizer wall-clock at write | Record-keeping for the normalized manifest only — never used as a strategy input or analytic | int64 ms |
| Stream-only `E` | NOT present in archive | If a future stream-based source ever produces normalized rows, an `event_time_ms_source` enum (`stream` / `trade_time`) may be added in v002, **NOT v001** | n/a |

Binding rules:

- All timestamps are **UTC milliseconds**, integer, never local-time, never floating point.
- Half-open day bounds: `lower_inclusive_ms <= T < upper_exclusive_ms` for every normalized row in a given `utc_date` partition.
- The future normalizer must **not** compute a `T` value for any row; it must emit raw `T` byte-equal-by-int-parse from the source CSV.
- The `created_at_utc_ms` field is recorded only in the normalized manifest, never on a row, and is never used downstream. (Stage-3 and Stage-4 phases must not include `created_at_utc_ms` as a feature.)

---

## 13. Numeric precision and type policy

The Phase 4ax `validate_aggtrade_payload` already preserves raw `p` and `q` as `Decimal`. The proposed normalized schema continues this discipline:

- `price` and `quantity` are stored **as strings** in the normalized output (Parquet `string` type or equivalent). Downstream consumers must parse with `Decimal` to obtain exact precision.
- Storing as `float64` is **forbidden** for `price` and `quantity`. Float storage corrupts the last-significant-bit precision of Binance string-decimal prices; the normalizer must not introduce such loss.
- All ID fields (`agg_trade_id`, `first_trade_id`, `last_trade_id`) are `int64`. Binance aggregate trade IDs fit comfortably below 2^63.
- All timestamps (`transact_time_ms`) are `int64` UTC milliseconds.
- The `is_buyer_maker` field is `bool` (strict). The Phase 4ax validator already rejects non-bool inputs.
- All hash fields (`source_file_sha256`, `source_manifest_sha256`, `source_gate_report_sha256`) are 64-character lowercase hex strings.
- All version fields (`dataset_version`, `source_dataset_version`, `normalization_schema_version`) are short constant strings.
- All path / family / id fields are constant or look-up strings; no integer encoding.
- The normalizer must **not** convert `price` / `quantity` to a different unit (e.g. satoshis, or shifted-integer encodings); raw string-decimal is preserved verbatim.

---

## 14. Partitioning and path policy

Partitioning is deterministic and symbol/date-based:

```text
data/microstructure/normalized/microstructure_normalized_aggtrades_v001/
    <SYMBOL>/<YYYY>/<MM>/<SYMBOL>-aggTrades-<YYYY-MM-DD>.parquet
```

Example for Phase 4az BTCUSDT 2025-01-15 (illustrative; **not** created by Phase 4bc):

```text
data/microstructure/normalized/microstructure_normalized_aggtrades_v001/
    BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet
```

Binding rules:

- The output base directory `data/microstructure/normalized/` must be entirely under the gitignored `data/microstructure/` namespace (already covered by `.gitignore:85`).
- One Parquet file per `(symbol, utc_date)` pair. No partition-spanning rows. No multi-day files.
- Symbol segment is uppercase Binance USDⓈ-M Futures notation.
- `<YYYY>/<MM>` segments are zero-padded.
- The filename mirrors the raw archive filename (`<SYMBOL>-aggTrades-<YYYY-MM-DD>.parquet`) so the lineage is visually obvious.
- The normalized output **must not** be written under `data/microstructure/raw/`, `data/microstructure/manifests/`, or `data/microstructure/gate-reports/`. Any future normalizer that writes outside `data/microstructure/normalized/` fails closed.
- Parquet is the recommended storage format. JSONL is acceptable as a sanity-check intermediate but **must not** be the canonical artefact (Parquet preserves typed columns including the string-decimal precision discipline more cleanly).

---

## 15. Manifest policy for normalized derived family

The normalized manifest lives at:

```text
data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json
```

It must conform to the Phase 4aw `MicrostructureManifest` schema with the following required fields populated:

| Field | Value (Phase 4az illustrative) |
| ----- | ------------------------------ |
| `dataset_family` | `microstructure_normalized_aggtrades_v001` |
| `version` | `v001` |
| `symbol` | `BTCUSDT` |
| `source` | `derived_from_microstructure_raw_aggtrades_v001` |
| `endpoint` | `derived` (constant; not a Binance endpoint) |
| `capture_mode` | `derived` (constant; not `historical_archive` / `rest` / `ws`) |
| `start_time_ms` | min `transact_time_ms` across all normalized rows |
| `end_time_ms` | max `transact_time_ms` across all normalized rows |
| `event_count` | total number of normalized rows |
| `file_count` | number of Parquet files emitted (one per `(symbol, utc_date)` pair) |
| `files[*].path` | relative path of each Parquet file |
| `files[*].sha256` | 64-char lowercase hex SHA256 of each Parquet file |
| `files[*].event_count` | per-file row count |
| `schema_version` | `v001` |
| `endpoint_docs_reference` | `derived_no_endpoint` (constant) |
| `capture_config_hash` | hash of normalizer config (deterministic) |
| `code_commit_sha` | normalizer code commit SHA at build time |
| `invalid_windows` | propagated per §16 |
| `retention_warning` | none for derived (constant) |
| `proxy_warning` | none for derived (constant) |
| `governance_labels` | see below |
| `research_eligible` | `false` until separately authorized Stage-3 eligibility gate passes |
| `eligibility_gate_status` | `pending` until separately authorized Stage-3 eligibility gate runs |

`governance_labels` minimum required keys:

| Key | Value |
| --- | ----- |
| `phase` | `4bd` (the future normalizer-implementation phase) |
| `source_phase_boundary` | `4bb-D` (cites the gate report) |
| `source_dataset_family` | `microstructure_raw_aggtrades_v001` |
| `source_dataset_version` | `v001` |
| `source_manifest_path` | relative path of the raw manifest |
| `source_manifest_sha256` | 64-char hex SHA of the raw manifest |
| `source_raw_zip_path` | relative path of the raw zip |
| `source_raw_zip_sha256` | 64-char hex SHA of the raw zip |
| `source_gate_report_id` | Phase 4bb-D `report_id` |
| `source_gate_report_sha256` | Phase 4bb-D report SHA `96f09159...` |
| `source_gate_report_code_commit_sha` | Phase 4bb-D gate `code_commit_sha = aa612ba2...` |
| `validator` | `phase_4ax_aggtrades_v001` (the row validator used during normalization) |
| `stop_trigger_domain` | `trade_price_backtest_candidate` (Phase 3v §8 governance) |
| `feature_computation` | `forbidden` |
| `strategy_use` | `forbidden` |

**Forbidden manifest content** for the derived family at v001:

- `feature_computation: allowed` — never;
- `strategy_use: allowed` — never;
- `research_eligible: true` — only if a separately authorized Stage-3 gate passes (see §17);
- `eligibility_gate_status: pass` — only if a separately authorized Stage-3 gate runs and passes (see §17);
- any feature / label / signal field reference;
- any synthetic / forward-filled / interpolated row.

The original Phase 4az v001 raw manifest is **never** modified by the normalizer. The derived manifest is a **new file** at a different path; both manifests coexist.

---

## 16. Invalid-window propagation policy

Phase 4az currently has **zero** invalid-window candidates per the Phase 4bb-D gate result (`len(invalid_window_candidates) = 0`; raw manifest `invalid_windows: []`). The propagation policy must still be defined for future normalizer correctness:

- **Source-derived invalid windows.** The normalizer reads `source_manifest.invalid_windows` and copies every entry verbatim into `derived_manifest.invalid_windows` with an additional `propagated_from = source_manifest` annotation. Source severity / `downstream_eligibility_action` are preserved exactly. The normalizer must **not** invent, drop, or reclassify source invalid windows.
- **Normalization-time invalid windows.** If during the normalization row scan, the normalizer detects a row that fails the Phase 4ax validator (which should never happen on a Phase 4bb-D-PASSed source, but the normalizer must remain defensive), it must:
  - record an `InvalidWindow` entry covering the offending row(s) with `reason = MALFORMED_ROW_AT_NORMALIZATION` (a new normalization-time enum extension that **must** be added to the Phase 4aw `InvalidWindowReason` set as part of the future Phase 4bd implementation, not by Phase 4bc);
  - set `severity = ERROR` and `downstream_eligibility_action = FAIL_CLOSED`;
  - abort the entire normalization run (no partial output is written);
  - record evidence at `(file_path, row_index, raw_row_repr)`.
- **Per-row exclusion.** The normalizer **must not** silently drop, skip, or mask rows. Every raw aggTrade row must produce exactly one normalized row, OR the entire run aborts. There is no per-row exclusion mode at v001.
- **No silent forward-fill / interpolation / imputation.** Phase 3p §4.7 / Phase 3r §8 / Phase 4j §11 governance applies verbatim: no synthetic rows, no forward-filled prices, no interpolated quantities, no imputed `T`, no replaced `is_buyer_maker`. The normalizer is byte-faithful to the raw source.
- **Empty `invalid_windows` is a valid state.** Phase 4az has it. The normalized manifest must explicitly carry `invalid_windows: []` rather than omit the field.

---

## 17. Eligibility model for normalized derived family

The Phase 4ba 5-stage ladder applies to the normalized family in its own right:

- **Stage 0 — acquired (derived).** The normalized Parquet exists on disk under `data/microstructure/normalized/...` plus its derived manifest at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json` with `research_eligible=false` and `eligibility_gate_status=pending`. This is the state immediately after a future Phase 4bd normalizer run completes.
- **Stage 1 — inspected (derived).** A future docs-only structural-QA pass on the normalized output (analogous to Phase 4bb-A on raw). Confirms row count, schema, ordering, lineage. Does not transition manifest fields.
- **Stage 2 — gate-passed (derived).** A future separately authorized Stage-2 eligibility gate for the normalized family (analogous to Phase 4bb-C / Phase 4bb-D on raw, but with normalized-family-specific check set) returns `overall_status=pass`. The original derived manifest may transition `eligibility_gate_status` from `pending` to `pass` only via a sibling successor-state manifest mechanism analogous to Phase 4bb-G (never overwriting v001).
- **Stage 3 — research-eligible normalized.** A separately authorized Stage-3 transition phase flips `research_eligible` from `false` to `true` on the derived manifest. **This is the first stage at which `research_eligible = true` is permitted in the entire microstructure data lineage.** The transition must require: (i) cited Stage-2 gate-passed evidence; (ii) Phase 4ak M0 admissibility memo for any planned downstream feature work; (iii) operator authorization recorded in a tracked memo.
- **Stage 4 — feature-cleared (derived).** A separately authorized Stage-4 transition phase records that a specific predeclared feature-design memo has been adopted as binding governance, opening Stage-4 feature computation under M0.

Phase 4bc's explicit position on these stages:

- A future Phase 4bd normalizer-implementation run advances the derived family to **Stage 0 only**.
- All higher stages require additional separately authorized phases.
- Phase 4bc does NOT authorize Stage 1, Stage 2, Stage 3, or Stage 4 transitions.
- Phase 4bc does NOT authorize Phase 4bd itself.

---

## 18. Stage-2 versus Stage-3 transition rules

| Transition | What changes | What is required |
| ---------- | ------------ | ---------------- |
| Stage 0 → Stage 1 | conceptual / docs only | docs-only structural-QA memo for the derived family (analogous to Phase 4bb-A) |
| Stage 1 → Stage 2 | derived-family `eligibility_gate_status` may transition `pending → pass` via a sibling successor-state manifest only | derived-family eligibility-gate primitive (analogous to Phase 4bb-C); single execution against the derived artefacts (analogous to Phase 4bb-D); successor-state policy memo (analogous to Phase 4bb-E); separately authorized successor-state recording phase (analogous to Phase 4bb-G); zero invalid-window candidates introduced by normalization |
| Stage 2 → Stage 3 | derived-family `research_eligible` may transition `false → true` | cited Stage-2 gate-passed evidence; Phase 4ak M0 admissibility; operator authorization; separately authorized Stage-3 transition phase |
| Stage 3 → Stage 4 | feature design and feature-cleared status is recorded | Phase 4ak M0 admissibility for feature work; predeclared feature-design memo; operator authorization; separately authorized Stage-4 transition phase |

**Binding rule:** The original raw family (`microstructure_raw_aggtrades_v001`) is **forever excluded** from `research_eligible = true`. Only the derived normalized family can ever reach Stage 3. Normalization is the **first opportunity** to obtain a research-eligible artefact in the microstructure lineage; even then, it requires the full Stage 0 → Stage 1 → Stage 2 → Stage 3 staircase, none of which is authorized by Phase 4bc.

---

## 19. `research_eligible` policy for normalized family

| Phase / event | `research_eligible` state |
| ------------- | -------------------------- |
| Immediately after Phase 4bd normalizer-implementation run completes | `false` |
| After Stage 1 (inspected) | `false` |
| After Stage 2 (gate-passed; sibling successor-state manifest) | `false` |
| After Stage 3 (research-eligible) | **may** be `true` if and only if a separately authorized Stage-3 transition phase recorded the transition |
| After Stage 4 (feature-cleared) | `true` (carried from Stage 3) |

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant continues to apply for raw families (and remains binding governance). For derived families, the invariant must be relaxed **only** at the Stage-3 transition phase boundary — and even then, the relaxation must be implemented via a sibling successor-state manifest (preserving the Stage-0 derived manifest byte-identically), not via in-place mutation of the original derived manifest. The exact code path for that relaxation is part of future Phase 4bd / Stage-3 design and is **not** specified by Phase 4bc.

---

## 20. Feature-computation boundary

Feature computation is **forbidden at every stage prior to Stage 4** on the derived normalized family. Specifically:

- Phase 4bc does NOT authorize feature design.
- Phase 4bd (future normalizer implementation) must NOT compute features.
- Stage 1 (inspected) must NOT compute features.
- Stage 2 (gate-passed) must NOT compute features.
- Stage 3 (research-eligible) must NOT compute features (the Stage-3 transition itself is purely a manifest-field change with cited evidence).
- Only Stage 4 (feature-cleared) authorizes feature computation, and only under a predeclared feature-design memo cleared by Phase 4ak M0.

Forbidden during all pre-Stage-4 work: returns, alpha, edge, opportunity rate, taker imbalance, sweep detection, aggressive-flow score, spread, depth, liquidity, slippage, order-flow, execution-quality, regime classification, trend-state, momentum, volatility metrics, MFE / MAE, R-multiples, PnL, equity, position state, strategy signals.

The normalized v001 schema (§11) is intentionally narrow to enforce this boundary. Anyone wanting a feature must propose a separate Stage-4 family.

---

## 21. ML / strategy boundary

ML training, strategy implementation, and backtesting are **forbidden at every pre-Stage-4 stage**, and **forbidden at Stage 4 except** for a separately authorized M0-cleared specific candidate. Specifically:

- Phase 4bc does NOT authorize ML training, strategy implementation, or backtesting.
- Phase 4bd does NOT authorize them either.
- Stage 1 / 2 / 3 transitions do NOT authorize them.
- Stage 4 authorizes feature computation only (not ML / strategy / backtest).
- ML / strategy / backtest require their own separately authorized phases on top of Stage 4, each gated by Phase 4ak M0 + post-null cooldown.

This boundary is reaffirmed verbatim by Phase 4bc.

---

## 22. Implementation plan for a future phase

The following plan is **for a future separately authorized Phase 4bd normalizer-implementation phase**. Phase 4bc does **not** authorize Phase 4bd; this section is design only.

Proposed Phase 4bd source modules (under `src/prometheus/research/microstructure/`):

| Module | Purpose |
| ------ | ------- |
| `normalize_io.py` | read-only loaders for raw `.zip` + manifest + sidecar + gate report citation; write-side atomic Parquet writer constrained to `data/microstructure/normalized/`; SHA256 helpers |
| `normalize_aggtrades.py` | core normalizer: per-row validate-and-emit pipeline; deterministic ordering; schema enforcement; lineage column population; invalid-window propagation |
| `normalize_manifest.py` | derived-manifest builder: governance labels; lineage references; per-file SHAs; aggregate counts; `research_eligible=false` / `eligibility_gate_status=pending` defaults |
| `normalize_validation.py` | post-normalization validator: row-count parity; ID monotonicity; timestamp bounds; schema completeness; forbidden-column scan; lineage-field completeness |

Proposed Phase 4bd test modules (under `tests/research/microstructure/`):

| Test file | Purpose |
| --------- | ------- |
| `test_normalize_io.py` | atomic write; refuses paths outside `data/microstructure/normalized/`; SHA helpers |
| `test_normalize_aggtrades.py` | row mapping; deterministic ordering; per-row validation; precision preservation; lineage column population |
| `test_normalize_manifest.py` | governance labels; lineage references; defaults; required-field presence |
| `test_normalize_validation.py` | each validation check fires correctly on positive and negative fixtures |
| `test_normalize_no_network.py` | static import-boundary scan: no `requests`, no `httpx`, no Binance, no `dotenv`, etc. |

Proposed Phase 4bd public API (re-exported via `prometheus.research.microstructure`):

```text
NormalizeAggTradesInput
NormalizeAggTradesResult
NormalizationValidationError
NormalizationIOError
run_normalize_aggtrades(input: NormalizeAggTradesInput) -> NormalizeAggTradesResult
```

Phase 4bd should follow the Phase 4bb-C pattern: pure-stdlib + pyarrow; no `prometheus.runtime/execution/persistence` imports; no network I/O; no credentials; no MCP / Graphify / `.mcp.json`; deterministic outputs; atomic write-then-rename; paired SHA256 sidecars per Parquet file; exactly one execution per `(source_manifest, source_file)` pair (no overwrite by default); `research_eligible_after = False` invariant on the derived manifest; `no_successor_authorization = True` invariant on the result.

---

## 23. Acceptance criteria for a future normalization implementation

A future Phase 4bd normalizer-implementation phase is acceptable only if:

1. It adds normalizer code only under `src/prometheus/research/microstructure/` in the four module names enumerated in §22.
2. It adds test code only under `tests/research/microstructure/` in the five test files enumerated in §22.
3. It writes normalized output only under the gitignored path `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/...`.
4. It writes the derived manifest only at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json`.
5. It does NOT mutate raw data, raw manifests, raw sidecars, raw acquisition logs, or the existing Phase 4bb-D gate report.
6. It does NOT compute features, labels, signals, returns, alpha, edge, opportunity rate, taker imbalance, sweep detection, aggressive-flow score, spread, depth, liquidity, slippage, order-flow, execution-quality proxies, regime classification, trend-state, momentum, volatility metrics, MFE / MAE, R-multiples, PnL, equity, position state, or strategy signals.
7. It does NOT train ML.
8. It does NOT create strategy logic.
9. It does NOT run backtests.
10. It does NOT call any Binance endpoint, public endpoint, private endpoint, WebSocket, user stream, or authenticated API.
11. It does NOT use credentials, `.env`, `.mcp.json`, MCP, or Graphify.
12. It does NOT modify `pyproject.toml`, `README.md`, `.gitignore` (the `data/microstructure/` gitignore line already covers the normalized path), or any unrelated tracked file.
13. It does NOT modify any existing source / test / script under unrelated paths.
14. The normalized manifest preserves all lineage fields enumerated in §15 verbatim, including `source_gate_report_id`, `source_gate_report_sha256`, and `source_gate_report_code_commit_sha`.
15. The normalized validation (§24) passes on the actual Phase 4az source artefact.
16. `ruff check .`, `pytest tests/research/microstructure/`, `pytest` (whole repo, with the two pre-existing simulation failures unchanged), and `mypy` (strict) all pass.
17. The derived manifest has `research_eligible=false` and `eligibility_gate_status=pending`. The normalizer must NOT flip these.
18. No successor phase is authorized by the implementation alone. Phase 4bd produces Stage-0 derived artefacts only.

---

## 24. Normalization-time validation checks

The future Phase 4bd normalizer must run the following checks. Any FAIL aborts the run and writes no derived artefact:

1. Input raw manifest exists at the cited path.
2. Cited Phase 4bb-D PASS gate report `report_id` and SHA are recorded; if the local report file is present, its recomputed SHA matches the cited SHA.
3. Raw manifest SHA computed at run time matches the cited `source_manifest_sha256`.
4. Raw zip SHA computed at run time matches the cited `source_raw_zip_sha256` and the raw manifest's `files[*].sha256`.
5. Raw sidecar contents (first 64 hex chars) match the raw zip SHA bit-for-bit.
6. Raw archive contains exactly one CSV member (Phase 4bb-A and Phase 4bb-D both verified).
7. Raw archive decompresses cleanly (no CRC errors).
8. Every raw row passes `prometheus.research.microstructure.aggtrades.validate_aggtrade_payload`.
9. Normalized row count equals raw `event_count` from the raw manifest exactly.
10. Every normalized row maps to exactly one raw aggTrade row (one-to-one mapping; no row dropped, no row duplicated).
11. No duplicate `agg_trade_id` introduced (already enforced by Phase 4bb-D check `10.7.24` on the raw side).
12. No row dropped unless covered by an explicitly propagated invalid-window entry (and at v001, no invalid-window entries are expected).
13. No row reordered without the deterministic `row_index` ordering rule.
14. First normalized `transact_time_ms` equals raw `start_time_ms` from the raw manifest exactly.
15. Last normalized `transact_time_ms` equals raw `end_time_ms` from the raw manifest exactly.
16. All `transact_time_ms` values are within the half-open day bounds defined by `utc_date` (per §12).
17. All numeric fields parse using the declared precision policy (§13): `agg_trade_id` / `first_trade_id` / `last_trade_id` / `transact_time_ms` parse as `int64`; `price` / `quantity` parse as `Decimal`; `is_buyer_maker` parses as `bool`.
18. No feature / label / signal columns exist in the normalized output (forbidden-column scan).
19. Normalized manifest references every required source-evidence field (§15).
20. Normalized output path is under `data/microstructure/normalized/...` (gitignored boundary check).
21. Original raw manifest hash before run equals raw manifest hash after run (immutability check).
22. Original raw zip hash before run equals raw zip hash after run (immutability check).
23. Original raw sidecar hash before run equals raw sidecar hash after run (immutability check).
24. Original raw acquisition log hash before run equals raw acquisition log hash after run (immutability check).
25. Derived manifest `research_eligible` is `false`.
26. Derived manifest `eligibility_gate_status` is `pending`.
27. No forbidden-import / forbidden-token strings appear anywhere in the new normalizer modules (static scan reusing the Phase 4bb-C `test_eligibility_no_network.py` discipline).

If any of checks 1–27 fail, the run aborts, no Parquet is written, no derived manifest is written, and the failure is reported. If checks 21–24 fail, the operator must investigate immediately because the raw artefacts may have been mutated outside of governance (this should never happen in normal operation).

---

## 25. Fail-closed rules

The following fail-closed rules apply to any future Phase 4bd normalizer-implementation phase, any Stage-1 / Stage-2 / Stage-3 / Stage-4 transition phase for the derived family, and any read of the derived dataset:

- **Original raw artefacts must not be modified.** Any phase that mutates the raw manifest, raw zip, raw sidecar, or raw acquisition log fails closed.
- **Raw-family `research_eligible` must remain `false`.** Any phase that flips raw-family `research_eligible` to `true` fails closed.
- **Existing Phase 4bb-D gate report must not be deleted, moved, renamed, or modified.** Any phase that mutates the existing report fails closed.
- **No commit under `data/microstructure/`.** The gitignored namespace stays gitignored. Any phase that commits a file under `data/microstructure/` fails closed.
- **No silent transition `pending → pass` on a derived manifest field.** Any phase that mutates the derived manifest's `eligibility_gate_status` without explicit operator authorization, without reference to a specific derived-family gate report, without the gate report's `code_commit_sha`, and without preserving the original derived manifest fails closed.
- **No flip of derived-family `research_eligible` outside a Stage-3 transition phase.** Any phase that flips derived-family `research_eligible` to `true` without the full Stage-2 → Stage-3 evidence chain fails closed.
- **No `research_eligible_after = true` invariant violation in any orchestrator code.** The Phase 4aw raw-family invariant remains; any new orchestrator must implement an analogous derived-family invariant that fails closed at the framework layer.
- **No feature / label / signal column in v001 normalized schema.** Any normalizer build that emits a column not listed in §11 fails closed.
- **No row dropped, reordered, or duplicated.** Any normalizer build that violates one-to-one mapping fails closed.
- **No float storage for `price` / `quantity`.** Any normalizer build that stores `price` or `quantity` as `float64` fails closed.
- **No silent forward-fill / interpolation / imputation / replacement.** Phase 3p §4.7 / Phase 3r §8 / Phase 4j §11 governance applies verbatim.
- **No network I/O, credentials, MCP, Graphify, `.mcp.json`, or `.env` in any normalizer module.** Any module that imports `requests`, `httpx`, `aiohttp`, `urllib.request`, `urllib3`, `socket`, `websockets`, `binance`, `dotenv`, or reads `os.environ` for endpoint / credential purposes fails closed via static scan.
- **No data acquisition, feature computation, ML, strategy, backtest, paper / shadow, live-readiness, exchange-write, or production keys.** None of these are authorized by Phase 4bc or by any of the proposed successor phases at the policy level.

---

## 26. What this phase proves

- A precise normalized derived dataset family design exists for raw Binance USDⓈ-M Futures aggTrades, scoped to one symbol and one UTC day at a time (matching the Phase 4az acquisition pattern).
- The normalized schema is trade-record-level only, lossless, and contains zero feature / label / signal / proxy columns.
- The normalized manifest contract preserves full lineage from the derived family back through the Phase 4bb-D PASS gate report, the source manifest, the source raw zip, and the gate `code_commit_sha`.
- The Phase 4ba 5-stage ladder applies to the derived family in its own right; Stage 3 is the first stage at which `research_eligible = true` becomes possible in the entire microstructure data lineage.
- Every transition between stages requires a separately authorized phase. Phase 4bc authorizes none.
- The Phase 4bb-E successor-state policy continues unchanged: original Phase 4az v001 manifest immutable; raw-family `research_eligible` permanent false; doubled `gate-reports/gate-reports/` path documented and deferred to Phase 4bb-F.

---

## 27. What this phase does not prove

- That a normalized derived dataset exists. It does not. Phase 4bc is design-only; no Parquet or derived manifest has been produced.
- That a future Phase 4bd normalizer-implementation phase is authorized. It is not. Phase 4bd requires separate operator authorization.
- That Stage 1, Stage 2, Stage 3, or Stage 4 transitions are authorized. They are not.
- That `research_eligible = true` is now allowed on any aggTrades artefact. It is not.
- That feature computation, ML training, strategy implementation, or backtests are now allowed. They are not.
- That any retained verdict (R3 baseline-of-record; R1a / R1b-narrow retained; R2 FAILED §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL; V2 / G1 / C1 HARD REJECT terminal; 5m thread CLOSED; H0 framework anchor) should be revised. None should be revised.
- That any project lock should be relaxed. None should be relaxed.

---

## 28. Preserved boundaries

| Boundary | Preserved? |
| -------- | :--------: |
| No source code change | yes |
| No test change | yes |
| No script change | yes |
| No config change | yes |
| No `.gitignore` change | yes |
| No M0 governance change | yes |
| No data acquisition | yes |
| No public-endpoint calls | yes |
| No Binance API calls | yes |
| No WebSocket | yes |
| No credential / `.env` / `.mcp.json` / MCP / Graphify | yes |
| No data normalization (Phase 4bc is design only) | yes |
| No feature computation | yes |
| No ML / strategy / backtest | yes |
| No mutation of `data/microstructure/` | yes |
| Original Phase 4az manifest unchanged | yes |
| Phase 4bb-D gate report unchanged | yes |
| `research_eligible` for raw family stays `false` | yes |
| `eligibility_gate_status` stays `pending` | yes |
| No retained verdict revised | yes |
| No project lock loosened | yes |
| No successor authorized | yes |

---

## 29. Recommended future options

- **Primary — remain paused.** No successor phase is authorized by Phase 4bc.
- **Conditional next, only if the operator wants to begin moving toward implementation:** future docs-and-code **Phase 4bd — AggTrades Normalization Implementation** (implements the design defined here; produces Stage-0 derived artefacts only; NOT authorized by Phase 4bc). Alternatively, an intermediate docs-only **Phase 4bd-A — AggTrades Normalization Implementation Plan Memo** (file-by-file plan analogous to Phase 4bb-B) may be inserted before code if the operator prefers an extra planning step.
- **Conditional cleanup, only before any future repeated gate execution:** future code-and-docs **Phase 4bb-F — Gate Report Output Path Hygiene** (fixes the doubled `gate-reports/gate-reports/` path; preserves the existing Phase 4bb-D report at its existing path; adds a regression test). Independent of Phase 4bd.
- **Conditional policy marker, only if the operator wants a machine-readable Stage-2 marker on the raw manifest:** future docs-and-local-gitignored-output (or docs-and-code) **Phase 4bb-G — Raw Manifest Successor-State Recording** (sibling successor-state manifest preserving the original v001 byte-identically and preserving `research_eligible=false`). Independent of Phase 4bd.
- **Not recommended.** Acquiring more aggTrades data; flipping `research_eligible` on any raw or derived family without the full evidence chain; computing features; training ML; creating a strategy; running backtests; reopening the 5m research thread; rescuing R2 / F1 / D1-A / V2 / G1 / C1 / V1-arc; touching MCP / Graphify / `.mcp.json` / credentials.
- **Forbidden.** Verdict revision; lock revision; parameter optimization derived from Phase 4bc reasoning; M0 amendment derived from Phase 4bc reasoning; paper / shadow / live-readiness / deployment / production-key creation / authenticated APIs / private endpoints / public-endpoint calls in code / user stream / live WebSocket / exchange-write.

---

## 30. Closeout / lock preservation

Phase 4bc preserves every retained verdict and project lock verbatim:

- H0 FRAMEWORK ANCHOR;
- R3 BASELINE-OF-RECORD;
- R1a / R1b-narrow RETAINED — NON-LEADING;
- R2 FAILED — §11.6;
- F1 HARD REJECT;
- D1-A MECHANISM PASS / FRAMEWORK FAIL;
- 5m thread OPERATIONALLY CLOSED per Phase 3t;
- V2 HARD REJECT — terminal for V2 first-spec;
- G1 HARD REJECT — terminal for G1 first-spec;
- C1 HARD REJECT — terminal for C1 first-spec;
- §11.6 = 8 bps per side; round-trip = 16 bps;
- §1.7.3 0.25% / 2× / one-position / mark-price stops;
- Phase 3p §4.7 strict integrity gate;
- Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8;
- Phase 4j §11;
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template;
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy;
- Phase 4am, 4an, 4ao, 4ap, 4aq, 4ar, 4as, 4at, 4au, 4av, 4aw, 4ax, 4ay, 4az, 4ba, 4bb-A, 4bb-B, 4bb-C, 4bb-D, 4bb-E results — all preserved verbatim.

The Phase 4az dataset's eligibility flags are unchanged: `research_eligible` remains `false`, `eligibility_gate_status` remains `pending`. Phase 4bb-D gate report and paired sidecar remain untouched at their existing local gitignored path with SHA256 `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`.

**Phase 4 (canonical) remains unauthorized. Phase 4bd / Phase 4bd-A / Phase 4bb-F / Phase 4bb-G / Phase 5 / any successor phase remains unauthorized. Paper / shadow, live-readiness, deployment, production keys, authenticated APIs, private endpoints, public-endpoint calls in code, user stream, live WebSocket implementation, MCP, Graphify, `.mcp.json`, credentials, and additional aggTrades / 5m / 1m / tick / mark-price 30m / 4h / order-book data acquisition all remain unauthorized.**

**Recommended state: remain paused. No next phase authorized.**
