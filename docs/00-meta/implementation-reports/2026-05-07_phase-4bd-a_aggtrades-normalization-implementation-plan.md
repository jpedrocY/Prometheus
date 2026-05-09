# Phase 4bd-A — AggTrades Normalization Implementation Plan Memo

**Phase identity:** Phase 4bd-A — AggTrades Normalization Implementation Plan Memo.
**Type:** docs-only implementation-plan memo.
**Date:** 2026-05-07.
**Branch:** `phase-4bd-a/aggtrades-normalization-implementation-plan`.
**Status:** drafted; pending operator review.

---

## 1. Phase header

Phase 4bd-A is a docs-only planning memo for a future Phase 4bd AggTrades Normalization Implementation. It translates the Phase 4bc design into a precise file-by-file, function-by-function implementation plan for a future normalizer that would produce **Stage-0 derived normalized artefacts only**.

Phase 4bd-A is **text only**. It does not implement code, modify tests, run a normalizer, create normalized files, create a derived manifest, mutate any artefact under `data/microstructure/`, compute features, train ML, create strategies, run backtests, acquire data, or authorize any successor.

---

## 2. Current state

| Item | Value |
| ---- | ----- |
| `main` HEAD | `53914b88dfaf3459a9fc56c4c7fd31a40e6d5b3e` |
| `origin/main` HEAD | `53914b88dfaf3459a9fc56c4c7fd31a40e6d5b3e` |
| Local / origin sync | in sync |
| Phase 4bc merge commit (ancestor verified) | `07729df9f378452c6d1049172747dcd3e3e34a9d` |
| Phase 4bc merge-closeout file | `docs/00-meta/implementation-reports/2026-05-07_phase-4bc_merge-closeout.md` (present on `main`) |
| `data/microstructure/` gitignored | yes (`.gitignore:85`) |
| Phase 4az manifest | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json` (`research_eligible=false`, `eligibility_gate_status=pending`, mtime unchanged since Phase 4az `2026-05-07 21:55`) |
| Phase 4bb-D local gate report | present on this workspace; recomputed SHA256 `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` matches sidecar bit-for-bit |

---

## 3. Inputs reviewed

- Phase 4az acquisition + manifest (BTCUSDT 2025-01-15; 1,681,098 events; raw zip SHA `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`; raw manifest SHA `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201`; sidecar SHA `b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d`; acquisition log SHA `f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c`).
- Phase 4ba staged eligibility-gate model + 5-stage ladder + 45-check definition.
- Phase 4bb-A structural QA (21 / 21 PASS).
- Phase 4bb-B execution plan.
- Phase 4bb-C primitive (`eligibility_io.py`, `eligibility_gate.py`, `eligibility_checks.py`, `eligibility_report.py`).
- Phase 4bb-D PASS gate report (`overall_status=pass`; 45 / 45 PASS; 0 invalid-window candidates; report SHA `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`; `report_id=microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c`; gate `code_commit_sha=aa612ba2778c97a5150b80064244b90d024bfa54`).
- Phase 4bb-E successor-state policy memo (Option A default; original v001 manifest immutable; raw-family `research_eligible` permanent false; sibling successor-state manifest only via separately authorized future phase; doubled `gate-reports/gate-reports/` path documented and deferred).
- Phase 4bc normalization design memo (proposed family `microstructure_normalized_aggtrades_v001`; 19-column schema; 27-check validation set; 18-criterion future Phase 4bd acceptance criteria; 12 fail-closed rules; deterministic symbol/date partitioning; string-Decimal precision; UTC-ms `int64` timestamps with half-open day bounds).
- Phase 4aw scaffold types (`MicrostructureManifest`, `RawWriter`, `InvalidWindow`, `EligibilityGateStatus`, `MicrostructureConfig`, `ALLOWLIST_PATTERNS` / `DENYLIST_TOKENS`).
- Phase 4ax aggTrades-only collector primitives (`validate_aggtrade_payload`, `AggTradeValidationError`, `TakerSide`).
- Project locks: §11.6, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6/§7/§8, Phase 4j §11, Phase 4ak M0 + post-null cooldown, Phase 4al refined no-rescue rule + §13 + §14.

No live endpoints, credentials, `.env`, `.mcp.json`, MCP, Graphify, or external services were consulted.

---

## 4. Scope

- Translate the Phase 4bc design into a precise file-by-file, function-by-function implementation plan for a future Phase 4bd normalizer.
- Define proposed source modules under `src/prometheus/research/microstructure/` and proposed test modules under `tests/research/microstructure/`.
- Define proposed public API: value objects, enums, exceptions, orchestrator function.
- Define proposed normalizer execution flow with explicit ordering.
- Define proposed raw-to-normalized mapping implementation.
- Define proposed writer and output-path policy.
- Define proposed derived manifest builder.
- Define proposed normalization validation module that maps the Phase 4bc 27 checks to functions.
- Define proposed invalid-window propagation implementation.
- Define proposed no-network / no-credentials / no-feature guards.
- Define proposed test plan and the mapping from Phase 4bc 27 validation checks to future test cases.
- Define acceptance criteria for any future Phase 4bd phase.
- Define fail-closed conditions for any future Phase 4bd phase.
- Recommend a conservative bounded successor sequence and explicitly NOT authorize any successor.

---

## 5. Non-scope

Phase 4bd-A did NOT:

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
- create a derived manifest;
- create a successor manifest;
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
- authorize Phase 4bd, Phase 4be, Phase 4bf, Phase 4bb-F, Phase 4bb-G, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation.

---

## 6. Phase 4bc design dependency

Any future Phase 4bd implementation must conform exactly to the Phase 4bc design memo. The design fields that bind Phase 4bd are:

| Phase 4bc § | Binding rule for Phase 4bd |
| ----------- | -------------------------- |
| §9 (proposed family name) | `dataset_family = microstructure_normalized_aggtrades_v001`; never overwrites the raw family `microstructure_raw_aggtrades_v001` |
| §10 (raw-to-normalized mapping) | one-to-one row mapping; canonical raw column keys `a` / `p` / `q` / `f` / `l` / `T` / `m` (per Phase 4ax validator); deterministic ordering by `row_index` |
| §11 (proposed schema) | exactly the 19 columns enumerated in §11; **no other column may appear** at v001 |
| §12 (timestamp semantics) | `transact_time_ms` is `int64`; UTC ms; non-decreasing per file; half-open day bounds; `created_at_utc_ms` recorded only in the manifest |
| §13 (numeric precision) | `price` and `quantity` stored **as strings**; float storage forbidden; `agg_trade_id` / `first_trade_id` / `last_trade_id` / `transact_time_ms` are `int64`; `is_buyer_maker` is strict `bool` |
| §14 (partitioning) | `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-aggTrades-<YYYY-MM-DD>.parquet`; one Parquet per `(symbol, utc_date)` pair |
| §15 (manifest) | derived manifest at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json`; full lineage in `governance_labels`; `research_eligible=false` and `eligibility_gate_status=pending` defaults |
| §16 (invalid-window propagation) | source-derived propagated verbatim; normalization-time invalid windows abort the run; no per-row exclusion at v001; no silent fill / interpolation / imputation |
| §17 (eligibility model) | normalizer produces Stage-0 derived artefacts only; Stage-1 / 2 / 3 / 4 transitions require separate phases |
| §20–§21 (feature / ML / strategy boundaries) | normalizer must NOT compute any feature / label / signal / proxy / return / alpha / edge / regime / trend / momentum / volatility / MFE / MAE / R / PnL / equity / position / strategy column |
| §24 (27 validation checks) | every check must be implemented and tested |
| §25 (fail-closed rules) | every rule must be implemented |

Phase 4bd-A must not deviate from Phase 4bc; any deviation requires a separate amendment phase.

---

## 7. Phase 4bb-D PASS gate-report dependency

The future Phase 4bd normalizer must cite the Phase 4bb-D PASS gate report verbatim. The cited evidence and its embedding in the derived manifest are:

| Field | Value | Embedded in derived manifest? |
| ----- | ----- | :---------------------------: |
| `report_id` | `microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c` | yes — `governance_labels.source_gate_report_id` |
| Report path (local; gitignored) | `data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json` | yes — `governance_labels.source_gate_report_path` (relative, gitignored note) |
| Report SHA256 | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` | yes — `governance_labels.source_gate_report_sha256` |
| Gate `code_commit_sha` | `aa612ba2778c97a5150b80064244b90d024bfa54` | yes — `governance_labels.source_gate_report_code_commit_sha` |
| `overall_status` | `pass` | yes — `governance_labels.source_gate_overall_status` |
| Total checks / PASS / FAIL / NA / ERROR | `45 / 45 / 0 / 0 / 0` | yes — `governance_labels.source_gate_check_summary` |
| Invalid-window candidates | `0` | yes — `governance_labels.source_gate_invalid_window_candidates` |
| `research_eligible_after` | `False` | yes — `governance_labels.source_gate_research_eligible_after` |
| `no_successor_authorization` | `True` | yes — `governance_labels.source_gate_no_successor_authorization` |

The future normalizer must verify these fields against either the local gitignored report (preferred when present) or the tracked Phase 4bb-D / 4bb-E / 4bc Markdown record (fallback). If the local report is present and its recomputed SHA does not match `96f09159...`, the run aborts.

---

## 8. Phase 4bb-E successor-state policy dependency

Any future Phase 4bd implementation operates strictly under Phase 4bb-E's conservative posture:

- **Original Phase 4az manifest is immutable.** The future normalizer must read it read-only and verify pre-run SHA equals post-run SHA. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant continues to apply for raw families.
- **Raw-family `research_eligible` is permanently `false`.** No code path in any future normalizer may flip it.
- **The actual on-disk Phase 4az manifest's `eligibility_gate_status` may remain `pending` indefinitely.** The future normalizer does not require Stage-2 transition; it cites the Phase 4bb-D PASS gate report directly.
- **Doubled `gate-reports/gate-reports/` path is harmless for the existing Phase 4bb-D report.** The future normalizer reads the report at its existing path (with the doubled segment) without modification. A separately authorized Phase 4bb-F output-path-hygiene phase is independent and is NOT a prerequisite for Phase 4bd.

---

## 9. Future Phase 4bd implementation goal

Define a future normalizer that:

- reads the Phase 4az raw archive, raw manifest, sidecar, acquisition log, and Phase 4bb-D PASS report reference **read-only**;
- validates source evidence via Phase 4bb-D citation + SHA recomputation;
- emits one normalized row per raw aggTrade row (one-to-one; lossless; deterministic ordering by `row_index`);
- preserves `price` and `quantity` as Decimal-parsable strings (float storage forbidden);
- preserves `transact_time_ms` as UTC millisecond `int64`;
- writes normalized output only under `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/`;
- writes the derived manifest only under `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json`;
- defaults the derived manifest to `research_eligible=false` and `eligibility_gate_status=pending`;
- produces Stage-0 derived artefacts only;
- does not compute features, labels, signals, returns, alpha, edge, imbalance, sweep, slippage, liquidity, ML, strategy, or backtest outputs;
- returns a result with `no_successor_authorization=true` and `research_eligible_after=false` invariants enforced at the framework layer.

---

## 10. Proposed package / file layout

The future Phase 4bd implementation must add these files (and only these files) under the existing Phase 4aw / 4bb-C package structure:

### Source modules (under `src/prometheus/research/microstructure/`)

| File | Purpose |
| ---- | ------- |
| `normalize_io.py` | read-only source-artefact loaders; local path discipline; output-root guard under `data/microstructure/normalized/`; SHA helpers; atomic write helpers; pyarrow Parquet writer boundary (pyarrow already in project deps via existing modules) |
| `normalize_aggtrades.py` | public orchestrator `run_normalize_aggtrades`; per-row validation pipeline using Phase 4ax `validate_aggtrade_payload`; one-to-one row mapping; deterministic `row_index` handling; normalized-row construction; no-feature-column guard at construction |
| `normalize_manifest.py` | derived-manifest builder using the Phase 4aw `MicrostructureManifest` data model; lineage / `governance_labels` construction (per §7 of this memo); per-Parquet-file SHA256 recording; `event_count` and `file_count` aggregation; invalid-window propagation; `research_eligible=false` / `eligibility_gate_status=pending` defaults |
| `normalize_validation.py` | post-normalization validation runner; implements every Phase 4bc 27 check as a typed `NormalizationCheckResult`; raw-artefact immutability checks (pre-run hash vs post-run hash for manifest / raw zip / sidecar / acquisition log) |
| `__init__.py` | narrow re-export update (add the new public symbols defined in §11 below; preserve all existing Phase 4aw / 4ax / 4bb-C exports) |

**No other source file may be created or modified by Phase 4bd.** The Phase 4aw `MicrostructureManifest`, `RawWriter`, `InvalidWindow`, `InvalidWindowReason`, `InvalidWindowSeverity`, `DownstreamEligibilityAction`, `EligibilityGateStatus`, `MicrostructureConfig`, `ALLOWLIST_PATTERNS`, `DENYLIST_TOKENS` types and the Phase 4ax `validate_aggtrade_payload`, `AggTradeValidationError`, `TakerSide` primitives must be reused as-is.

### Test modules (under `tests/research/microstructure/`)

| File | Purpose |
| ---- | ------- |
| `test_normalize_io.py` | atomic write boundary; refuses paths outside `data/microstructure/normalized/`; SHA helpers; refuses to overwrite existing files; tmp-path-only fixture |
| `test_normalize_aggtrades.py` | row mapping; deterministic ordering; per-row validation; precision preservation; lineage column population; no-feature-column guard |
| `test_normalize_manifest.py` | governance labels; lineage references; `research_eligible=false` / `eligibility_gate_status=pending` defaults; required-field presence; serialise / deserialise round-trip |
| `test_normalize_validation.py` | each of the Phase 4bc 27 checks fires correctly on positive and negative fixtures (54+ targeted test cases minimum) |
| `test_normalize_no_network.py` | static import-boundary scan: no `requests`, `httpx`, `aiohttp`, `urllib.request`, `urllib3`, `socket`, `websockets`, `binance`, `dotenv`; static credential-pattern scan reusing the Phase 4bb-C dynamic `DENYLIST_TOKENS` regex pattern |

**No other test file may be created or modified by Phase 4bd.** A shared fixture builder analogous to Phase 4bb-C's `_eligibility_fixtures.py` may be added at `tests/research/microstructure/_normalize_fixtures.py` if needed; this is permitted but not required.

---

## 11. Proposed public API

The future Phase 4bd implementation must expose this public API (and only this) via `prometheus.research.microstructure`:

| Symbol | Kind | Purpose |
| ------ | ---- | ------- |
| `NormalizeAggTradesInput` | frozen `dataclass` | input record: `manifest_path: Path`; `output_root: Path`; `code_commit_sha: str`; `write_output: bool = True`; `write_manifest: bool = True`; optional `explicit_extra_symbols: tuple[str, ...]`; optional `config: MicrostructureConfig` |
| `NormalizeAggTradesResult` | frozen `dataclass` | result record: `overall_status: NormalizationCheckStatus`; `output_path: Path \| None`; `derived_manifest_path: Path \| None`; `event_count: int`; `file_count: int`; `checks: tuple[NormalizationCheckResult, ...]`; `invalid_window_candidates: tuple[InvalidWindowCandidate, ...]`; `measured_summary: dict[str, Any]`; `boundary_confirmations: dict[str, bool]`; `research_eligible_after: bool` (always `False`); `no_successor_authorization: bool` (always `True`) |
| `NormalizedAggTradeRow` | frozen `dataclass` | row record matching the Phase 4bc 19-column schema exactly |
| `NormalizationManifestDraft` | frozen `dataclass` | manifest builder draft; converts to `MicrostructureManifest` via `to_manifest()` |
| `NormalizationValidationResult` | frozen `dataclass` | validation result: `overall_status: NormalizationCheckStatus`; `checks: tuple[NormalizationCheckResult, ...]`; `boundary_confirmations: dict[str, bool]` |
| `NormalizationCheckResult` | frozen `dataclass` | per-check result: `check_id: str`; `group: str`; `title: str`; `status: NormalizationCheckStatus`; `detail: str`; `evidence: dict[str, Any]` |
| `NormalizationCheckStatus` | `StrEnum` | `PASS` / `FAIL` / `NOT_APPLICABLE` / `ERROR` (matches Phase 4bb-C's `AggTradesEligibilityCheckStatus` shape verbatim) |
| `NormalizationIOError` | `Exception` | I/O failures: missing artefacts; path-discipline violations; SHA mismatches; refuse-to-overwrite |
| `NormalizationValidationError` | `Exception` | validation failures: schema mismatch; row-count mismatch; forbidden columns; lineage missing |
| `run_normalize_aggtrades` | function | `(inp: NormalizeAggTradesInput) -> NormalizeAggTradesResult`; exactly one execution per `(source_manifest, source_file)` pair; refuses to overwrite |

These are **proposed future APIs only** and are NOT implemented in Phase 4bd-A. The names mirror Phase 4bb-C's naming convention (`AggTradesEligibilityGateInput`, `AggTradesEligibilityGateResult`, `AggTradesEligibilityCheckResult`, `AggTradesEligibilityCheckStatus`, etc.) so future readers will recognise the pattern.

---

## 12. Proposed value objects and result models

### `NormalizeAggTradesInput` (frozen)

```text
manifest_path: Path  # must be data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json
output_root: Path    # must be data/microstructure/normalized/ (or a subdirectory thereof)
code_commit_sha: str # current git HEAD SHA at run time
write_output: bool = True       # if False, dry-run only; produces no Parquet, no manifest
write_manifest: bool = True     # if False, produces Parquet but no derived manifest (debugging only)
explicit_extra_symbols: tuple[str, ...] = ()  # default symbol allowlist is ("BTCUSDT", "ETHUSDT")
config: MicrostructureConfig | None = None     # if None, defaults to project allowlist
```

Construction-time validation:

- `manifest_path` is under `data/microstructure/manifests/`; otherwise `NormalizationIOError`.
- `output_root` is under `data/microstructure/`; otherwise `NormalizationIOError`. The orchestrator will further constrain writes to `output_root / "microstructure_normalized_aggtrades_v001" / <SYMBOL> / <YYYY> / <MM>`.
- `code_commit_sha` is a 40-char lowercase hex string; otherwise `NormalizationIOError`.
- `write_output=False` and `write_manifest=True` is rejected (cannot produce a manifest without the underlying file SHAs).

### `NormalizeAggTradesResult` (frozen)

```text
overall_status: NormalizationCheckStatus  # PASS / FAIL / ERROR (NOT_APPLICABLE not used at top level)
output_path: Path | None                  # path to the Parquet file (None if write_output=False or run aborted)
derived_manifest_path: Path | None        # path to the derived manifest (None if write_manifest=False or run aborted)
event_count: int                          # number of normalized rows emitted
file_count: int                           # number of Parquet files emitted (always 1 per (symbol, utc_date))
checks: tuple[NormalizationCheckResult, ...]   # exactly 27 entries (Phase 4bc check IDs 1..27)
invalid_window_candidates: tuple[InvalidWindowCandidate, ...]
measured_summary: dict[str, Any]          # raw_zip_sha_before, raw_zip_sha_after, manifest_sha_before, ...
boundary_confirmations: dict[str, bool]   # 14 boundary keys analogous to Phase 4bb-C
research_eligible_after: bool             # invariant: always False
no_successor_authorization: bool          # invariant: always True
```

### `NormalizedAggTradeRow` (frozen)

Exactly 19 fields matching the Phase 4bc §11 schema:

```text
dataset_family: str
dataset_version: str
source_dataset_family: str
source_dataset_version: str
symbol: str
utc_date: str                # YYYY-MM-DD
agg_trade_id: int
price: str                   # Decimal-parsable
quantity: str                # Decimal-parsable
first_trade_id: int
last_trade_id: int
transact_time_ms: int
is_buyer_maker: bool
source_file_sha256: str
source_manifest_sha256: str
source_gate_report_id: str
source_gate_report_sha256: str
row_index: int
normalization_schema_version: str
```

Construction-time validation:

- `agg_trade_id`, `first_trade_id`, `last_trade_id`, `transact_time_ms`, `row_index` are `int` ≥ 0; `last_trade_id >= first_trade_id`; `transact_time_ms > 0`; `row_index >= 0`.
- `price` and `quantity` parse as positive `Decimal` (the constructor parses-and-restringifies to canonical form to avoid silent mutation; rejects negative / zero / non-decimal).
- `is_buyer_maker` is strict `bool`.
- `dataset_family`, `dataset_version`, `source_dataset_family`, `source_dataset_version`, `symbol`, `utc_date`, `source_gate_report_id`, `normalization_schema_version` are non-empty strings.
- `source_file_sha256`, `source_manifest_sha256`, `source_gate_report_sha256` are 64-char lowercase hex.
- `utc_date` parses as `YYYY-MM-DD`; the implied half-open day bounds contain `transact_time_ms`.
- **No constructor accepts an unknown field.** Construction by keyword-only with strict field set.

### `NormalizationManifestDraft` (frozen)

```text
dataset_family: str           # constant: microstructure_normalized_aggtrades_v001
version: str                  # constant: v001
symbol: str
source: str                   # constant: derived_from_microstructure_raw_aggtrades_v001
endpoint: str                 # constant: derived
capture_mode: str             # constant: derived
start_time_ms: int
end_time_ms: int
event_count: int
file_count: int
files: tuple[FileEntry, ...]  # uses Phase 4aw FileEntry
schema_version: str           # constant: v001
endpoint_docs_reference: str  # constant: derived_no_endpoint
capture_config_hash: str
code_commit_sha: str
invalid_windows: tuple[InvalidWindow, ...]
governance_labels: dict[str, str]   # 14 required keys per §7 + Phase 4bc §15
```

A `to_manifest() -> MicrostructureManifest` method converts the draft to the Phase 4aw manifest type with `research_eligible=False` and `eligibility_gate_status=PENDING` defaults explicit and unchangeable.

### `NormalizationCheckStatus` (`StrEnum`)

Exactly 4 values: `PASS`, `FAIL`, `NOT_APPLICABLE`, `ERROR`. Matches Phase 4bb-C's `AggTradesEligibilityCheckStatus` shape so test fixtures can reuse the same enum-comparison patterns.

---

## 13. Proposed normalizer execution flow

The future `run_normalize_aggtrades(inp)` orchestrator must execute these steps in order, fail-closed at any error:

1. **Verify paths under `data/microstructure/`.** Reject `manifest_path` outside `data/microstructure/manifests/`; reject `output_root` outside `data/microstructure/`. Compute the exact derived paths: `output_path = output_root / "microstructure_normalized_aggtrades_v001" / <SYMBOL> / <YYYY> / <MM> / <SYMBOL>-aggTrades-<YYYY-MM-DD>.parquet`; `derived_manifest_path = data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json`. Reject if either path already exists (refuse-to-overwrite).
2. **Read the source raw manifest.** Use a Phase 4bb-C-style `read_manifest_and_hash` helper. Record `manifest_sha_before` in `measured_summary`. Verify `dataset_family == microstructure_raw_aggtrades_v001` and `version == v001`. Verify `research_eligible == false` and `eligibility_gate_status == pending` (the Phase 4bb-E policy invariant: raw manifest is `pending`).
3. **Read the raw sidecar and raw zip hash.** Compute SHA256 of the raw zip; compare against the sidecar's first 64 hex chars and against the manifest's `files[*].sha256`. Record `raw_zip_sha_before` and `sidecar_sha_before` in `measured_summary`.
4. **Read the acquisition log and hash.** Record `acquisition_log_sha_before` in `measured_summary`.
5. **Verify the Phase 4bb-D PASS gate report reference.** Resolve the report path under the gitignored `data/microstructure/gate-reports/` namespace. If the local report is present, recompute its SHA and compare against the cited `96f09159...`. If the local report is absent, fall back to the tracked Phase 4bb-D / 4bb-E / 4bc Markdown citation (the orchestrator must accept a "tracked-only" mode but log it). Record `source_gate_report_sha_verified` in `measured_summary`.
6. **Iterate the raw zip in-memory** (no disk decompression to a tracked path). Use `zipfile.ZipFile` against the raw zip; verify exactly one CSV member; iterate rows via `csv.reader`.
7. **Validate every raw row** with the Phase 4ax `validate_aggtrade_payload`. Any `AggTradeValidationError` aborts the run with `NormalizationValidationError`.
8. **Map every raw row** to a `NormalizedAggTradeRow` via the §14 mapping. Maintain a strictly-increasing `row_index` counter (zero-based). The orchestrator must assert one-to-one mapping (no row dropped, no row duplicated). Maintain a running set of seen `agg_trade_id` values for duplicate detection.
9. **Enforce the no-feature-column guard.** Construction of `NormalizedAggTradeRow` already rejects unknown fields; the orchestrator additionally asserts that the schema declared in `prometheus.research.microstructure.normalize_aggtrades.NORMALIZED_SCHEMA_V001` equals the Phase 4bc 19-column list verbatim.
10. **Write normalized output atomically.** Use a Phase 4aw `RawWriter`-style atomic write-then-rename pattern, but emit Parquet via `pyarrow.parquet.write_table` to a `.tmp` path, then `os.replace` to the final path. Compute SHA256 of the finalised Parquet. Record `output_file_sha256` in `measured_summary`.
11. **Compute normalized file SHA** for the derived manifest's `files[*].sha256`. Compute aggregate `event_count` (must equal raw `event_count`) and `file_count` (must equal 1 for one symbol/day archive).
12. **Build the derived manifest** via `NormalizationManifestDraft.to_manifest()`. Populate all 14 required `governance_labels` keys. Atomically write the derived manifest at `derived_manifest_path` (write-then-rename). Compute SHA256 of the finalised manifest.
13. **Run the post-normalization validation suite** via `normalize_validation.run_all_checks(...)`. This executes all 27 Phase 4bc check functions in fixed order. Any `FAIL` or `ERROR` result aborts the run *after* writing the derived artefacts (so the operator can inspect the partial outputs) but sets `overall_status = FAIL` and records the failure in `checks`.
14. **Re-hash the raw artefacts.** Compute `raw_zip_sha_after`, `manifest_sha_after`, `sidecar_sha_after`, `acquisition_log_sha_after`. If any pre/post hash differs, set `overall_status = FAIL` and record the immutability violation in the failed check entries (Phase 4bc checks 21–24).
15. **Construct the result.** `NormalizeAggTradesResult` with: `overall_status` (FAIL if any check failed; PASS otherwise); `output_path`, `derived_manifest_path`; `event_count`, `file_count`; tuple of 27 `NormalizationCheckResult` entries; `invalid_window_candidates` (zero entries if Phase 4az source is used and no normalization-time anomalies were detected); `measured_summary` dict with 12+ keys including all pre/post hashes; `boundary_confirmations` dict with 14 keys (analogous to Phase 4bb-C: `no_network_io`, `no_websocket`, `no_credential_read`, `no_env_read`, `no_mcp_or_graphify`, `no_manifest_mutation`, `no_data_microstructure_write_outside_normalized`, `no_feature_computed`, `no_label_computed`, `no_signal_computed`, `no_ml_trained`, `no_strategy_created`, `no_backtest_run`, `research_eligible_after_is_false_for_derived_family`); `research_eligible_after = False` (invariant); `no_successor_authorization = True` (invariant).
16. **Document Stage-0 derived artefact status.** The orchestrator's docstring and the closeout report must state: this run produces Stage-0 derived artefacts only; Stage-1 / 2 / 3 / 4 transitions require separately authorized phases.

---

## 14. Proposed raw-to-normalized mapping implementation

The mapping function `_map_raw_row_to_normalized(raw_row, row_index, lineage)` lives in `normalize_aggtrades.py` and produces a `NormalizedAggTradeRow`:

```text
def _map_raw_row_to_normalized(
    raw_row: AggTradePayload,            # already validated by Phase 4ax
    row_index: int,
    lineage: NormalizationLineage,       # frozen dataclass with constants + source SHAs
) -> NormalizedAggTradeRow:
    return NormalizedAggTradeRow(
        dataset_family="microstructure_normalized_aggtrades_v001",
        dataset_version="v001",
        source_dataset_family="microstructure_raw_aggtrades_v001",
        source_dataset_version="v001",
        symbol=lineage.symbol,                       # uppercase from raw manifest
        utc_date=lineage.utc_date,                   # YYYY-MM-DD from raw manifest start_time
        agg_trade_id=int(raw_row.a),
        price=str(raw_row.p),                        # Decimal -> canonical string
        quantity=str(raw_row.q),                     # Decimal -> canonical string
        first_trade_id=int(raw_row.f),
        last_trade_id=int(raw_row.l),
        transact_time_ms=int(raw_row.T),
        is_buyer_maker=bool(raw_row.m),
        source_file_sha256=lineage.raw_zip_sha,
        source_manifest_sha256=lineage.raw_manifest_sha,
        source_gate_report_id=lineage.gate_report_id,
        source_gate_report_sha256=lineage.gate_report_sha,
        row_index=row_index,
        normalization_schema_version="v001",
    )
```

Binding rules:

- The function **must** assign `row_index` from a strictly-increasing counter maintained by the orchestrator. The mapper must not infer `row_index` from row content.
- The function **must not** add fields not listed in §11 of the Phase 4bc design.
- The function **must not** drop fields listed in §11.
- The function **must not** transform `price` / `quantity` numerically (no rounding, no shifting, no scaling). It only canonicalises the `Decimal` representation as a string by passing through `str(Decimal(raw_row.p))`.
- The function **must not** transform `transact_time_ms`. The raw `T` is already validated `int` ≥ 0 by Phase 4ax.
- The function **must not** call any I/O, any endpoint, or any clock except as mediated by the lineage object (which carries pre-computed constants).

---

## 15. Proposed writer and output-path policy

Implementation in `normalize_io.py`:

- **`assert_output_path_under_normalized(path)`** rejects any path not under `data/microstructure/normalized/`. The `data/microstructure/` namespace boundary is the binding rule; the deeper segment `normalized/` is enforced as the second-level boundary.
- **`atomic_write_parquet(path, table, *, refuse_overwrite=True)`** writes a pyarrow Table via `pyarrow.parquet.write_table` to `path.with_suffix(path.suffix + ".tmp")`, calls `os.fsync` (best-effort under `contextlib.suppress(OSError)`), then `os.replace` to the final `path`. If `refuse_overwrite` and the final path already exists, raises `NormalizationIOError`. Returns the SHA256 of the finalised file.
- **`compute_file_sha256(path)`** reads the file in 1-MiB chunks and returns the lowercase hex SHA256. Uses the existing pattern from Phase 4bb-C `eligibility_io.py`.
- **`atomic_write_json(path, obj, *, refuse_overwrite=True)`** serialises with `json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False)` plus a trailing newline; writes to `.tmp`; `os.replace`. Returns the SHA256 of the finalised file. Used for the derived manifest.
- **All writes go through these helpers.** No direct `open(path, "w")` / `open(path, "wb")` outside the helpers in `normalize_io.py`. No use of `tempfile.mkstemp` outside the helpers (the pattern is encapsulated).
- **No decompression to disk under tracked paths.** The raw zip is iterated via `zipfile.ZipFile.open(member)` and `io.TextIOWrapper`; the CSV is parsed in-memory. No `.tmp` file is created under any non-`data/microstructure/normalized/` path.

The output-path policy is binding: any future Phase 4bd code that writes a Parquet or JSON file outside `data/microstructure/normalized/` (for Parquet) or `data/microstructure/manifests/` (for the derived manifest) fails closed at the helper layer.

---

## 16. Proposed derived manifest builder

Implementation in `normalize_manifest.py`:

```text
def build_normalization_manifest_draft(
    *,
    symbol: str,
    utc_date: str,
    rows: Sequence[NormalizedAggTradeRow],
    output_file_sha256: str,
    output_file_path: Path,
    raw_manifest_sha256: str,
    raw_zip_sha256: str,
    sidecar_sha256: str,
    acquisition_log_sha256: str,
    gate_report_id: str,
    gate_report_sha256: str,
    gate_code_commit_sha: str,
    gate_overall_status: str,
    code_commit_sha: str,
    capture_config_hash: str,
    invalid_windows: Sequence[InvalidWindow],
) -> NormalizationManifestDraft:
    ...
```

The builder constructs the draft with:

- `dataset_family = "microstructure_normalized_aggtrades_v001"`;
- `version = "v001"`;
- `symbol`, `start_time_ms = min(r.transact_time_ms for r in rows)`, `end_time_ms = max(r.transact_time_ms for r in rows)`;
- `event_count = len(rows)`, `file_count = 1`;
- a single `FileEntry(path=relative_output_path, sha256=output_file_sha256, event_count=len(rows))`;
- `governance_labels` populated with all 14 required keys (per §7 of this memo + Phase 4bc §15):
  - `phase = "4bd"`;
  - `source_phase_boundary = "4bb-D"`;
  - `source_dataset_family = "microstructure_raw_aggtrades_v001"`;
  - `source_dataset_version = "v001"`;
  - `source_manifest_path = relative_raw_manifest_path`;
  - `source_manifest_sha256 = raw_manifest_sha256`;
  - `source_raw_zip_path = relative_raw_zip_path`;
  - `source_raw_zip_sha256 = raw_zip_sha256`;
  - `source_gate_report_id = gate_report_id`;
  - `source_gate_report_sha256 = gate_report_sha256`;
  - `source_gate_report_code_commit_sha = gate_code_commit_sha`;
  - `validator = "phase_4ax_aggtrades_v001"`;
  - `stop_trigger_domain = "trade_price_backtest_candidate"`;
  - `feature_computation = "forbidden"`;
  - `strategy_use = "forbidden"`;
- `invalid_windows` set from the propagation policy (§19);
- `research_eligible = False` and `eligibility_gate_status = EligibilityGateStatus.PENDING` (defaults from `to_manifest()`; never accepts `True` / `PASS` at v001 build time).

A `to_manifest()` method converts the draft to the Phase 4aw `MicrostructureManifest` type, leveraging the existing `flip_research_eligible(...)` always-raises invariant to ensure the field cannot be flipped post-construction.

---

## 17. Proposed normalization validation module

Implementation in `normalize_validation.py`. Defines:

```text
@dataclass(frozen=True)
class NormalizationValidationContext:
    inp: NormalizeAggTradesInput
    rows: tuple[NormalizedAggTradeRow, ...]
    output_path: Path
    output_file_sha256: str
    derived_manifest: MicrostructureManifest
    derived_manifest_path: Path
    raw_manifest_sha_before: str
    raw_manifest_sha_after: str
    raw_zip_sha_before: str
    raw_zip_sha_after: str
    sidecar_sha_before: str
    sidecar_sha_after: str
    acquisition_log_sha_before: str
    acquisition_log_sha_after: str
    cited_gate_report_id: str
    cited_gate_report_sha256: str
    cited_gate_code_commit_sha: str

CHECK_ORDER: tuple[tuple[str, str, str, Callable[[NormalizationValidationContext], NormalizationCheckResult]], ...] = (
    ("4bc.24.1",  "source",       "Input raw manifest exists",                                    check_input_raw_manifest_exists),
    ("4bc.24.2",  "source",       "Cited Phase 4bb-D PASS gate report ID and SHA recorded",        check_gate_report_citation_recorded),
    ("4bc.24.3",  "source",       "Raw manifest SHA matches cited source_manifest_sha256",         check_raw_manifest_sha_matches),
    ("4bc.24.4",  "source",       "Raw zip SHA matches cited source_raw_zip_sha256 + manifest",    check_raw_zip_sha_matches),
    ("4bc.24.5",  "source",       "Raw sidecar contents match raw zip SHA",                        check_sidecar_matches_zip),
    ("4bc.24.6",  "archive",      "Raw archive contains exactly one CSV member",                   check_one_csv_member),
    ("4bc.24.7",  "archive",      "Raw archive decompresses cleanly",                              check_decompression_clean),
    ("4bc.24.8",  "schema",       "Every raw row passes validate_aggtrade_payload",                check_every_row_validates),
    ("4bc.24.9",  "row_count",    "Normalized row count equals raw event_count",                   check_row_count_parity),
    ("4bc.24.10", "row_count",    "Every normalized row maps to exactly one raw aggTrade row",     check_one_to_one_mapping),
    ("4bc.24.11", "duplicates",   "No duplicate agg_trade_id introduced",                          check_no_duplicate_agg_trade_id),
    ("4bc.24.12", "drops",        "No row dropped except per propagated invalid windows",          check_no_silent_drops),
    ("4bc.24.13", "ordering",     "Deterministic row_index ordering",                              check_deterministic_ordering),
    ("4bc.24.14", "timestamps",   "First normalized transact_time_ms equals raw start_time_ms",    check_first_T_parity),
    ("4bc.24.15", "timestamps",   "Last normalized transact_time_ms equals raw end_time_ms",       check_last_T_parity),
    ("4bc.24.16", "timestamps",   "All transact_time_ms within half-open UTC day bounds",          check_T_within_day_bounds),
    ("4bc.24.17", "precision",    "Numeric fields parse under declared precision policy",          check_numeric_precision),
    ("4bc.24.18", "schema",       "No feature/label/signal columns exist",                         check_no_forbidden_columns),
    ("4bc.24.19", "manifest",     "Normalized manifest references all source-evidence fields",     check_manifest_lineage_complete),
    ("4bc.24.20", "path",         "Normalized output path under data/microstructure/normalized/",  check_output_path_under_namespace),
    ("4bc.24.21", "immutability", "Raw manifest hash before == after",                             check_raw_manifest_immutable),
    ("4bc.24.22", "immutability", "Raw zip hash before == after",                                  check_raw_zip_immutable),
    ("4bc.24.23", "immutability", "Raw sidecar hash before == after",                              check_sidecar_immutable),
    ("4bc.24.24", "immutability", "Raw acquisition log hash before == after",                      check_acquisition_log_immutable),
    ("4bc.24.25", "manifest",     "Derived manifest research_eligible is false",                   check_derived_manifest_research_eligible_false),
    ("4bc.24.26", "manifest",     "Derived manifest eligibility_gate_status is pending",           check_derived_manifest_status_pending),
    ("4bc.24.27", "imports",      "No forbidden imports / forbidden tokens in normalizer modules", check_no_forbidden_imports),
)

def run_all_checks(ctx: NormalizationValidationContext) -> NormalizationValidationResult:
    ...
```

Each check returns a `NormalizationCheckResult` with `check_id`, `group`, `title`, `status`, `detail`, `evidence`. A defensive wrapper turns any unexpected exception into `ERROR` status.

---

## 18. Proposed invalid-window propagation implementation

Implementation in `normalize_manifest.py`:

```text
def propagate_invalid_windows(
    *,
    source_invalid_windows: Sequence[InvalidWindow],
    normalization_runtime_invalid_windows: Sequence[InvalidWindow],
) -> tuple[InvalidWindow, ...]:
    ...
```

Behavior:

- Source invalid windows are copied verbatim with one annotation: each entry's `evidence` dict gains a `propagated_from = "source_manifest"` key.
- Normalization-runtime invalid windows are appended after the propagated source entries with `propagated_from = "normalization_run"`.
- If any normalization-runtime window has `severity = ERROR` and `downstream_eligibility_action = FAIL_CLOSED`, the orchestrator must abort the entire run (no Parquet, no derived manifest written; only the in-memory result returned). Phase 4bd implementation detail: this is enforced at step 13 of the §13 execution flow.
- For Phase 4az specifically, both source and runtime are expected to be empty; the resulting `tuple` is `()`.

The Phase 4aw `InvalidWindowReason` enum's 17 values are reused as-is for any normalization-runtime invalid window. If a future Phase 4bd encounters a malformed row it must use the existing reason `MALFORMED_ROW_AT_NORMALIZATION` if the enum already includes it; otherwise it must propose adding the value to the enum in a separate amendment phase rather than introducing a string-literal. Phase 4bd-A does not add any new enum value.

**At v001, the normalizer never emits a per-row exclusion entry.** Every raw row produces exactly one normalized row, OR the entire run aborts. There is no "propagated invalid window covers row 12345" path that drops only that row.

---

## 19. Proposed no-network / no-credentials / no-feature guards

Three guard layers are predeclared:

### Static import-boundary scan

`tests/research/microstructure/test_normalize_no_network.py` reuses the Phase 4bb-C parametrised `test_no_forbidden_imports` pattern (already in `test_import_boundaries.py`) and extends it to cover the four new `normalize_*.py` modules. The forbidden-module list is at minimum:

`requests`, `httpx`, `aiohttp`, `urllib.request`, `urllib3`, `socket`, `websockets`, `binance`, `dotenv`, `python_dotenv`, `os.environ`, `getenv`.

### Static credential-pattern scan

The same test file scans the four new modules (after stripping docstrings / comments) for the Phase 4aw `DENYLIST_TOKENS` set, dynamically built (matching the Phase 4bb-C `eligibility_io.py` pattern). This ensures no literal credential strings, MCP tokens, `.mcp.json` references, or `.env` references appear in the new code.

### No-feature column guard

`normalize_aggtrades.py` declares a module-level constant:

```text
NORMALIZED_SCHEMA_V001: tuple[str, ...] = (
    "dataset_family", "dataset_version",
    "source_dataset_family", "source_dataset_version",
    "symbol", "utc_date",
    "agg_trade_id", "price", "quantity",
    "first_trade_id", "last_trade_id",
    "transact_time_ms", "is_buyer_maker",
    "source_file_sha256", "source_manifest_sha256",
    "source_gate_report_id", "source_gate_report_sha256",
    "row_index", "normalization_schema_version",
)
```

The orchestrator asserts at construction and at write time that the rows' field set equals this constant exactly. Any divergence raises `NormalizationValidationError`. The test `test_normalize_aggtrades.py::test_no_feature_columns` parametrises a forbidden-column list (e.g. `mfe_r`, `mae_r`, `return_1m`, `taker_imbalance`, etc.) and asserts each is rejected at row construction.

---

## 20. Proposed test plan

The Phase 4bd test suite must include at minimum the following test cases. Coverage minimum: every check function in `normalize_validation.py` has both a positive and a negative test fixture; every public API symbol has a construction-time test; every guard layer is exercised.

| Test file | Test function (illustrative) | Purpose |
| --------- | ---------------------------- | ------- |
| `test_normalize_io.py` | `test_atomic_write_parquet_creates_finalised_path` | atomic write semantics |
| | `test_atomic_write_parquet_refuses_overwrite` | refuse-to-overwrite |
| | `test_atomic_write_parquet_rejects_path_outside_normalized` | output-path discipline |
| | `test_atomic_write_json_creates_finalised_path` | derived manifest writer |
| | `test_compute_file_sha256_chunked` | SHA256 helper |
| `test_normalize_aggtrades.py` | `test_run_normalize_aggtrades_happy_path_on_phase4az_fixture` | end-to-end on tmp_path miniature |
| | `test_one_to_one_mapping_no_drops_no_duplicates` | mapping invariant |
| | `test_deterministic_row_index_ordering` | ordering invariant |
| | `test_price_quantity_string_decimal_preservation` | precision invariant |
| | `test_no_feature_columns_rejected_at_row_construction` | no-feature guard |
| | `test_normalized_schema_v001_constant_matches_phase_4bc` | schema-equality assertion |
| | `test_research_eligible_after_is_false_invariant` | invariant assertion |
| | `test_no_successor_authorization_invariant` | invariant assertion |
| | `test_run_aborts_on_aggtrade_validation_failure` | row-level failure path |
| | `test_run_aborts_when_output_path_already_exists` | refuse-to-overwrite at orchestrator layer |
| `test_normalize_manifest.py` | `test_governance_labels_minimum_keys_populated` | 14 governance keys |
| | `test_research_eligible_default_false` | manifest invariant |
| | `test_eligibility_gate_status_default_pending` | manifest invariant |
| | `test_propagate_invalid_windows_source_verbatim` | propagation policy |
| | `test_propagate_invalid_windows_runtime_aborts_on_error` | runtime-window abort |
| | `test_to_manifest_round_trip_preserves_lineage` | manifest serialise/deserialise |
| | `test_flip_research_eligible_still_raises` | Phase 4aw invariant preserved |
| `test_normalize_validation.py` | One PASS test + one FAIL test per check 4bc.24.1 .. 4bc.24.27 (54+ tests minimum) | full check coverage |
| | `test_check_order_has_exactly_27_entries` | check-set completeness |
| | `test_run_all_checks_returns_27_results` | orchestrator output shape |
| | `test_immutability_check_detects_post_run_mutation` | immutability detection |
| | `test_no_forbidden_columns_check_rejects_each_forbidden_class` | parametrised forbidden-class test |
| `test_normalize_no_network.py` | `test_normalize_modules_do_not_import_forbidden_modules_statically` | static import-boundary scan |
| | `test_normalize_modules_do_not_contain_credential_tokens_statically` | static credential-pattern scan |

Coverage minimum: at least 90 new tests across the five files (target: 100+). All tests must use pytest `tmp_path` only; no test writes outside `tmp_path`.

---

## 21. Mapping from Phase 4bc 27 validation checks to future test cases

Each Phase 4bc check ID maps to at least one positive test (PASS path on a clean fixture) and one negative test (deliberate fault injection that produces FAIL):

| Phase 4bc check | Function name | Positive test | Negative test |
| --------------- | ------------- | ------------- | ------------- |
| 4bc.24.1 input raw manifest exists | `check_input_raw_manifest_exists` | `test_check_1_pass` | `test_check_1_fail_missing_manifest` |
| 4bc.24.2 PASS gate ref recorded | `check_gate_report_citation_recorded` | `test_check_2_pass` | `test_check_2_fail_missing_citation` |
| 4bc.24.3 raw manifest SHA match | `check_raw_manifest_sha_matches` | `test_check_3_pass` | `test_check_3_fail_sha_mismatch` |
| 4bc.24.4 raw zip SHA match | `check_raw_zip_sha_matches` | `test_check_4_pass` | `test_check_4_fail_zip_sha_mismatch` |
| 4bc.24.5 sidecar matches zip | `check_sidecar_matches_zip` | `test_check_5_pass` | `test_check_5_fail_sidecar_mismatch` |
| 4bc.24.6 one CSV member | `check_one_csv_member` | `test_check_6_pass` | `test_check_6_fail_two_csv_members` |
| 4bc.24.7 clean decompression | `check_decompression_clean` | `test_check_7_pass` | `test_check_7_fail_corrupt_zip` |
| 4bc.24.8 every row validates | `check_every_row_validates` | `test_check_8_pass` | `test_check_8_fail_malformed_row` |
| 4bc.24.9 row count parity | `check_row_count_parity` | `test_check_9_pass` | `test_check_9_fail_row_count_off_by_one` |
| 4bc.24.10 one-to-one mapping | `check_one_to_one_mapping` | `test_check_10_pass` | `test_check_10_fail_duplicate_emitted` |
| 4bc.24.11 no duplicate agg_trade_id | `check_no_duplicate_agg_trade_id` | `test_check_11_pass` | `test_check_11_fail_duplicate_id` |
| 4bc.24.12 no silent drops | `check_no_silent_drops` | `test_check_12_pass` | `test_check_12_fail_silent_drop` |
| 4bc.24.13 deterministic row_index | `check_deterministic_ordering` | `test_check_13_pass` | `test_check_13_fail_unordered` |
| 4bc.24.14 first T parity | `check_first_T_parity` | `test_check_14_pass` | `test_check_14_fail_first_T_off` |
| 4bc.24.15 last T parity | `check_last_T_parity` | `test_check_15_pass` | `test_check_15_fail_last_T_off` |
| 4bc.24.16 T within day bounds | `check_T_within_day_bounds` | `test_check_16_pass` | `test_check_16_fail_T_outside_bounds` |
| 4bc.24.17 numeric precision | `check_numeric_precision` | `test_check_17_pass` | `test_check_17_fail_float_in_price` |
| 4bc.24.18 no forbidden columns | `check_no_forbidden_columns` | `test_check_18_pass` | `test_check_18_fail_extra_column` |
| 4bc.24.19 manifest lineage complete | `check_manifest_lineage_complete` | `test_check_19_pass` | `test_check_19_fail_missing_governance_label` |
| 4bc.24.20 output path under namespace | `check_output_path_under_namespace` | `test_check_20_pass` | `test_check_20_fail_path_outside_normalized` |
| 4bc.24.21 raw manifest immutable | `check_raw_manifest_immutable` | `test_check_21_pass` | `test_check_21_fail_manifest_mutated_post_run` |
| 4bc.24.22 raw zip immutable | `check_raw_zip_immutable` | `test_check_22_pass` | `test_check_22_fail_zip_mutated_post_run` |
| 4bc.24.23 sidecar immutable | `check_sidecar_immutable` | `test_check_23_pass` | `test_check_23_fail_sidecar_mutated_post_run` |
| 4bc.24.24 acquisition log immutable | `check_acquisition_log_immutable` | `test_check_24_pass` | `test_check_24_fail_log_mutated_post_run` |
| 4bc.24.25 derived manifest research_eligible false | `check_derived_manifest_research_eligible_false` | `test_check_25_pass` | `test_check_25_fail_research_eligible_true` |
| 4bc.24.26 derived manifest status pending | `check_derived_manifest_status_pending` | `test_check_26_pass` | `test_check_26_fail_status_pass` |
| 4bc.24.27 no forbidden imports | `check_no_forbidden_imports` | `test_check_27_pass` | `test_check_27_fail_imports_requests` |

54 tests minimum from this table alone, plus the orchestrator-level / API-level / boundary-level tests in §20. Total minimum: ~90 new tests.

---

## 22. Acceptance criteria for future Phase 4bd

A future Phase 4bd is acceptable only if all of the following hold:

1. It implements the Phase 4bc design exactly (19-column schema; one-to-one mapping; lossless precision; deterministic ordering; UTC-ms `int64` timestamps with half-open day bounds; symbol/date partitioning).
2. It adds source code only in the four `normalize_*` modules and a narrow `__init__.py` re-export update.
3. It adds tests only in the five `test_normalize_*` files (plus optional `_normalize_fixtures.py`).
4. It writes normalized output only under the gitignored `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/...` path.
5. It writes the derived manifest only at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json`.
6. It does NOT mutate raw data, raw manifests, raw sidecars, raw acquisition logs, or the existing Phase 4bb-D gate report.
7. It does NOT compute features, labels, signals, returns, alpha, edge, opportunity rate, taker imbalance, sweep detection, aggressive-flow score, spread, depth, liquidity, slippage, order-flow, execution-quality proxies, regime classification, trend-state, momentum, volatility metrics, MFE / MAE, R-multiples, PnL, equity, position state, or strategy signals.
8. It does NOT train ML.
9. It does NOT create strategy logic.
10. It does NOT run backtests.
11. It does NOT call any Binance endpoint, public endpoint, private endpoint, WebSocket, user stream, or authenticated API.
12. It does NOT use credentials, `.env`, `.mcp.json`, MCP, or Graphify.
13. It does NOT modify `pyproject.toml`, `README.md`, `.gitignore` (the `data/microstructure/` line already covers the normalized path), or any unrelated tracked file.
14. It preserves raw artefact hashes pre/post run for all four artefacts.
15. The normalized row count equals the raw `event_count` exactly.
16. No forbidden columns exist in the normalized schema.
17. `ruff check .`, `pytest tests/research/microstructure/`, `pytest` (whole repo, with the two pre-existing simulation failures unchanged), and `mypy` (strict) all pass.
18. The derived manifest has `research_eligible=false` and `eligibility_gate_status=pending`.
19. `NormalizeAggTradesResult.research_eligible_after = False` and `no_successor_authorization = True` invariants hold.
20. No successor phase is authorized by the implementation alone. Phase 4bd produces Stage-0 derived artefacts only.

---

## 23. Fail-closed conditions

Any future Phase 4bd implementation must fail closed if any of these conditions arise:

- **Path discipline.** `manifest_path` outside `data/microstructure/manifests/`; `output_root` outside `data/microstructure/`; computed `output_path` outside `data/microstructure/normalized/`; computed `derived_manifest_path` outside `data/microstructure/manifests/`.
- **Refuse-to-overwrite.** Either output path already exists at run start, OR a `.tmp` companion already exists at run start.
- **Read-only discipline.** Any attempt to open a Phase 4az artefact in write or append mode fails closed.
- **Source SHA mismatch.** `manifest_sha_before` ≠ recorded raw manifest SHA in the cited Phase 4bb-D context, or `raw_zip_sha_before` ≠ manifest's `files[*].sha256`, or sidecar contents don't match.
- **Gate-report citation mismatch.** Local report present but recomputed SHA ≠ `96f09159...`.
- **Raw manifest state drift.** Raw manifest `research_eligible` ≠ `false` or `eligibility_gate_status` ≠ `pending` at run start (Phase 4bb-E policy invariant).
- **Manifest immutability.** `manifest_sha_after` ≠ `manifest_sha_before`, or `raw_zip_sha_after` ≠ `raw_zip_sha_before`, or sidecar/log SHA differs pre/post.
- **Row-count parity.** Normalized row count ≠ raw `event_count`.
- **Schema integrity.** Any `NormalizedAggTradeRow` constructed with a field set ≠ `NORMALIZED_SCHEMA_V001`.
- **Precision integrity.** `price` or `quantity` contains a non-decimal character, or is constructed from `float`, or is non-positive.
- **Timestamp integrity.** `transact_time_ms` outside half-open day bounds; non-monotonic across rows; non-`int`.
- **Boundary discipline.** Any boundary confirmation in the result is `False` (e.g. `no_network_io = False`, `no_feature_computed = False`, `research_eligible_after_is_false_for_derived_family = False`).
- **Successor authorization.** `no_successor_authorization = False` is an internal-error FAIL.
- **Static governance shape.** The derived manifest's `governance_labels` is missing any of the 14 required keys, or contains `feature_computation = "allowed"` or `strategy_use = "allowed"`, or contains `research_eligible = true`.
- **Static import / token scan.** `test_normalize_no_network.py` flags any forbidden import or credential token.
- **Validation FAIL.** Any of the 27 validation checks returns `FAIL` or `ERROR`.

---

## 24. What this phase proves

- A precise file-by-file, function-by-function implementation plan exists for a future Phase 4bd AggTrades Normalization Implementation, fully consistent with the Phase 4bc design.
- The proposed package layout (4 source modules + narrow `__init__.py` update + 5 test files) mirrors the Phase 4bb-C precedent and reuses Phase 4aw / 4ax types without modification.
- The proposed public API (`NormalizeAggTradesInput`, `NormalizeAggTradesResult`, `NormalizedAggTradeRow`, `NormalizationManifestDraft`, `NormalizationValidationResult`, `NormalizationCheckResult`, `NormalizationCheckStatus`, `NormalizationIOError`, `NormalizationValidationError`, `run_normalize_aggtrades`) is fully specified in shape and invariant.
- The proposed execution flow (16 steps) is fail-closed at every boundary: path discipline, source-evidence citation, schema integrity, immutability hash equality, validation suite, boundary confirmations.
- The Phase 4bc 27 validation checks are mapped one-to-one to functions in `normalize_validation.py` and to test cases in `test_normalize_validation.py`.
- The Phase 4bc 18-criterion acceptance criteria + 12 fail-closed rules are enumerated.
- The static no-network, no-credentials, and no-feature-column guards are predeclared with binding test scope.

---

## 25. What this phase does not prove

- That a Phase 4bd implementation has been written. It has not. Phase 4bd-A is plan-only.
- That a future Phase 4bd is authorized. It is not. Phase 4bd requires separate operator authorization.
- That a normalized derived dataset exists. It does not.
- That `research_eligible = true` is now allowed on any aggTrades artefact. It is not.
- That feature computation, ML training, strategy implementation, or backtests are now allowed. They are not.
- That any retained verdict (R3 baseline-of-record; R1a / R1b-narrow retained; R2 FAILED §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL; V2 / G1 / C1 HARD REJECT terminal; 5m thread CLOSED; H0 framework anchor) should be revised. None should be revised.
- That any project lock should be relaxed. None should be relaxed.

---

## 26. Preserved boundaries

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
| No data normalization (Phase 4bd-A is plan only) | yes |
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

## 27. Recommended future options

- **Primary — remain paused.** No successor phase is authorized by Phase 4bd-A.
- **Conditional next, only if the operator wants to begin moving toward implementation:** future docs-and-code **Phase 4bd — AggTrades Normalization Implementation** (implements the design defined in the Phase 4bc memo per the Phase 4bd-A plan; produces Stage-0 derived artefacts only; NOT authorized by Phase 4bd-A).
- **Conditional cleanup, only before any future repeated gate execution:** future code-and-docs **Phase 4bb-F — Gate Report Output Path Hygiene** (independent of Phase 4bd; fixes the doubled `gate-reports/gate-reports/` path; preserves the existing Phase 4bb-D report at its existing path; adds a regression test).
- **Conditional policy marker, only if the operator wants a machine-readable Stage-2 marker on the raw manifest:** future docs-and-local-gitignored-output (or docs-and-code) **Phase 4bb-G — Raw Manifest Successor-State Recording** (independent of Phase 4bd; sibling successor-state manifest preserving the original v001 byte-identically and preserving `research_eligible=false`).
- **Not recommended.** Acquiring more aggTrades data; flipping `research_eligible` on any raw or derived family without the full evidence chain; computing features; training ML; creating a strategy; running backtests; reopening the 5m research thread; rescuing R2 / F1 / D1-A / V2 / G1 / C1 / V1-arc; touching MCP / Graphify / `.mcp.json` / credentials.
- **Forbidden.** Verdict revision; lock revision; parameter optimization derived from Phase 4bd-A reasoning; M0 amendment derived from Phase 4bd-A reasoning; paper / shadow / live-readiness / deployment / production-key creation / authenticated APIs / private endpoints / public-endpoint calls in code / user stream / live WebSocket / exchange-write.

---

## 28. Closeout / lock preservation

Phase 4bd-A preserves every retained verdict and project lock verbatim:

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
- Phase 4am, 4an, 4ao, 4ap, 4aq, 4ar, 4as, 4at, 4au, 4av, 4aw, 4ax, 4ay, 4az, 4ba, 4bb-A, 4bb-B, 4bb-C, 4bb-D, 4bb-E, 4bc results — all preserved verbatim.

The Phase 4az dataset's eligibility flags are unchanged: `research_eligible` remains `false`, `eligibility_gate_status` remains `pending`. Phase 4bb-D gate report and paired sidecar remain untouched at their existing local gitignored path with SHA256 `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`.

**Phase 4 (canonical) remains unauthorized. Phase 4bd / Phase 4be / Phase 4bf / Phase 4bb-F / Phase 4bb-G / Phase 5 / any successor phase remains unauthorized. Paper / shadow, live-readiness, deployment, production keys, authenticated APIs, private endpoints, public-endpoint calls in code, user stream, live WebSocket implementation, MCP, Graphify, `.mcp.json`, credentials, and additional aggTrades / 5m / 1m / tick / mark-price 30m / 4h / order-book data acquisition all remain unauthorized.**

**Recommended state: remain paused. No next phase authorized.**
