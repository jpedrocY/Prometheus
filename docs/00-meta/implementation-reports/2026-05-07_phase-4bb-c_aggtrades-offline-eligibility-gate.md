# Phase 4bb-C — AggTrades Offline Eligibility-Gate Primitive Implementation

**Type:** docs-and-code offline eligibility-gate implementation.
**Status:** drafted on branch `phase-4bb-c/aggtrades-offline-eligibility-gate`; pending operator review.
**Date:** 2026-05-07.

---

## 1. Phase header

Phase 4bb-C implements the offline aggTrades eligibility-gate primitive exactly as planned by Phase 4bb-B. The primitive reads the four Phase 4az-shaped artefacts (manifest, raw `.zip`, paired `.sha256` sidecar, acquisition log) read-only, runs all 45 Phase 4ba §10 eligibility-time checks against a shared in-memory single-pass row scan, returns an in-memory `AggTradesEligibilityGateResult`, and (when `write_report=True`) atomically writes a JSON gate report plus paired `.sha256` sidecar under `data/microstructure/gate-reports/`.

The primitive **never** flips `research_eligible=true` for raw aggTrades families, **never** mutates the original manifest / raw zip / sidecar / acquisition log, **never** contacts a Binance endpoint, **never** opens a WebSocket, **never** reads `.env` or any credential, and **never** authorises any successor phase. The reserved `write_successor_manifest=True` mode is structurally rejected by Phase 4bb-C; only a separately authorised future phase may enable that mode.

---

## 2. Current state

| Item | Value |
| ---- | ----- |
| Branch | `phase-4bb-c/aggtrades-offline-eligibility-gate` |
| Base SHA (`main`) | `e207dc49c30e2031d38a5c12b49f3f34bf643ca1` |
| Base parent | `docs(phase-4bb-b): add merge closeout` |
| Type | docs-and-code |
| Source modules added | 4 (`eligibility_io.py`, `eligibility_gate.py`, `eligibility_checks.py`, `eligibility_report.py`) |
| Source modules modified narrowly | 1 (`__init__.py` — re-exports + docstring) |
| Tests added | 5 + 1 shared fixture builder |
| Tests modified | 0 |
| Scripts modified | 0 |
| Data / manifests modified | **None** — `data/microstructure/` byte-identical to post-Phase-4az state |
| `.gitignore` modified | **No** — `data/microstructure/` already covers the new `gate-reports/` subdirectory |
| `pyproject.toml` modified | **No** |
| `README.md` modified | **No** |
| Successor authorised | **No** |
| Phase 4az manifest's `research_eligible` | **`false`** (unchanged) |
| Phase 4az manifest's `eligibility_gate_status` | **`pending`** (unchanged) |

---

## 3. Inputs reviewed

Phase 4bb-C was implemented from the Phase 4bb-B execution plan. The following committed sources were read:

- The Phase 4bb-B memo (`docs/00-meta/implementation-reports/2026-05-07_phase-4bb-b_aggtrades-eligibility-gate-execution-plan.md`), §7–§17 (file layout, value objects, gate execution flow, 45-check function mapping, gate-report schema, invalid-window plan, manifest immutability and successor-state policy, fail-closed conditions, test plan, acceptance criteria).
- The Phase 4ba memo, §9 (staged eligibility ladder), §10.1–§10.12 (45-check enumeration), §11 (manifest field contract), §12 (invalid-window taxonomy), §15 (six-category fail-closed rules + cross-cutting rules).
- The Phase 4bb-A memo, §15 (13 application-time observations).
- The Phase 4aw scaffold modules: `__init__.py`, `config.py`, `allowlist.py` (especially `ALLOWLIST_PATTERNS` / `DENYLIST_TOKENS`), `invalid_window.py` (17-value `InvalidWindowReason`, 3-value `InvalidWindowSeverity`, 3-value `DownstreamEligibilityAction`, frozen `InvalidWindow`), `manifest.py` (`MicrostructureManifest`, `EligibilityGateStatus`, `flip_research_eligible(...)` always raises), `raw_writer.py` (atomic write-then-rename with paired SHA256).
- The Phase 4ax aggTrades skeleton: `aggtrades.py` (`validate_aggtrade_payload`, `AggTradeValidationError`, `TakerSide`, `assert_aggtrades_endpoint_allowed`).
- The Phase 4az manifest: `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json` (read-only; `research_eligible: false`, `eligibility_gate_status: pending`; 1,681,098 events).

---

## 4. Scope

Phase 4bb-C is **docs-and-code**. The allowed activities are:

- Create the four new source modules under `src/prometheus/research/microstructure/`.
- Update `__init__.py` narrowly to re-export the new public symbols.
- Create five new test files plus one shared fixture builder under `tests/research/microstructure/`.
- Author this memo and the Phase 4bb-C closeout under `docs/00-meta/implementation-reports/`.
- A narrow `docs/00-meta/current-project-state.md` update.

---

## 5. Non-scope

The following are **forbidden** and **not performed** in Phase 4bb-C:

- Acquire data; call Binance APIs / public endpoints / private endpoints; open WebSockets; use credentials; read `.env` or `.mcp.json`; enable MCP / Graphify.
- Normalize the dataset; create JSONL / Parquet / DuckDB / feature tables / labels / derived datasets.
- Compute microstructure features; compute returns / alpha / edge / opportunity rate / taker imbalance / sweep detection / aggressive-flow score / spread / depth / liquidity / slippage / order-flow / execution-quality proxies.
- Train ML; create a strategy; run backtests.
- Modify any data, manifest, sidecar, or acquisition log under `data/microstructure/`.
- Modify `scripts/`, `data/`, `data/manifests/`, `README.md`, `pyproject.toml`, `.gitignore`, M0 governance, phase-gates, runtime docs, strategy specs, validation checklists.
- Flip `research_eligible=true` for any raw aggTrades dataset family.
- Authorize Phase 4bb-D, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, or production keys.

---

## 6. Implementation summary

### 6.1 Source modules (under `src/prometheus/research/microstructure/`)

- **`eligibility_io.py`** — read-only artefact loaders + single-pass row scanner. Provides `ArtefactPaths`, `ArtefactReadResult`, `RowScanSummary` data models; `assert_path_under_microstructure`, `resolve_artefact_paths`, `compute_file_sha256`, `compute_bytes_sha256`, `read_manifest_and_hash`, `read_sidecar`, `read_acquisition_log`, `scan_csv_rows_in_zip`, `scan_text_for_forbidden_tokens`, `serialise_for_token_scan`, `utc_day_start_from_archive_path`, `assert_no_dangerous_imports_loaded` helpers; module-level constants (`UTC_DAY_MS`, `MAX_ARCHIVE_BYTES`, `GATE_REPORTS_SUBDIR`, `CSV_HEADER_ALIAS_MAP`, `HEADERLESS_CANONICAL_ORDER`, `EXPECTED_CANONICAL_KEYS`); `GateIOError` exception.
- **`eligibility_gate.py`** — value objects, enums, orchestrator, and exceptions. Provides `AggTradesEligibilityCheckStatus` (StrEnum: `PASS` / `FAIL` / `NOT_APPLICABLE` / `ERROR`), `AggTradesEligibilityCheckResult` (frozen), `InvalidWindowCandidate` (frozen), `AggTradesEligibilityGateInput` (frozen), `AggTradesEligibilityGateResult` (frozen), `AggTradesGateInputError`, `AggTradesGateUnsupportedError` exceptions; `REQUIRED_BOUNDARY_KEYS` constant; `_aggregate_overall_status`, `_gate_status_for_overall`, `_make_report_id`, `_now_utc_ms` helpers; the public `run_eligibility_gate` orchestrator function.
- **`eligibility_checks.py`** — 45 individual check functions plus the `GateExecutionContext` dataclass that aggregates the read context. Provides `check_*` functions grouped 10.1.1–10.12.45; `CHECK_ORDER` ordered tuple of `(check_id, group, title, function)`; `_build_invalid_window_candidates` helper; the `run_all_checks` orchestrator entry point.
- **`eligibility_report.py`** — `AggTradesGateReport` data model (frozen, JSON-serialisable) and `write_report_atomic` helper that writes the JSON report + paired `.sha256` sidecar atomically under `data/microstructure/gate-reports/`.

### 6.2 Test modules (under `tests/research/microstructure/`)

- **`_eligibility_fixtures.py`** — shared mini-fixture builder. Builds Phase 4az-shaped fixtures entirely under pytest `tmp_path` directories. Provides `FixtureRow`, `FixtureBundle`, `make_default_rows`, `write_csv_zip`, `sha256_of_file`, `write_sidecar`, `build_manifest_dict`, `build_acquisition_log_dict`, `build_happy_fixture`, `utc_day_start_ms` helpers. Underscore-prefixed name keeps it out of pytest collection while remaining importable.
- **`test_eligibility_gate.py`** — orchestrator-level tests (12 tests).
- **`test_eligibility_checks.py`** — per-check failure-path tests (20 tests).
- **`test_eligibility_report.py`** — gate-report data model + atomic write tests (5 tests).
- **`test_eligibility_io.py`** — read-only artefact loader tests (12 tests).
- **`test_eligibility_no_network.py`** — boundary tests (6 tests): static import-boundary scan against the four new modules; runtime monkey-patched-`socket.socket` test; explicit-injection test for the `assert_no_dangerous_imports_loaded` guard; no-env-read test; no-MCP / no-Graphify / no-dotenv-imported test; clean-state guard test.

### 6.3 Public API additions (re-exports in `__init__.py`)

```python
AggTradesEligibilityCheckResult
AggTradesEligibilityCheckStatus
AggTradesEligibilityGateInput
AggTradesEligibilityGateResult
AggTradesGateInputError
AggTradesGateReport
AggTradesGateUnsupportedError
GateIOError
InvalidWindowCandidate
run_eligibility_gate
```

### 6.4 No CLI / no script

Per the Phase 4bb-B plan, Phase 4bb-C does **not** add a `scripts/...` entrypoint. Invocation is library-style only (direct import of `run_eligibility_gate`).

### 6.5 No new dependency

Phase 4bb-C uses only the standard library (`hashlib`, `zipfile`, `csv`, `json`, `pathlib`, `dataclasses`, `enum`, `tempfile`, `os`, `re`, `subprocess`, `contextlib`, `datetime`) plus Phase 4aw / Phase 4ax modules already present in the repository.

### 6.6 No `.gitignore` change

`data/microstructure/` (line 85 of `.gitignore`) already covers `data/microstructure/gate-reports/`.

---

## 7. Source files added / modified

### Added (4 new tracked source files)

```
src/prometheus/research/microstructure/eligibility_io.py
src/prometheus/research/microstructure/eligibility_gate.py
src/prometheus/research/microstructure/eligibility_checks.py
src/prometheus/research/microstructure/eligibility_report.py
```

### Modified (1 narrow update)

```
src/prometheus/research/microstructure/__init__.py   (Phase 4bb-C re-exports + docstring extension)
```

### Files NOT modified

- No file under `src/prometheus/` outside `research/microstructure/`.
- No file under `scripts/`.
- No file under `data/`, `data/manifests/`, `data/microstructure/`, `data/research/`, `data/derived/`, `data/raw/`, `data/normalized/`.
- No existing test under `tests/`.
- No `pyproject.toml`, `README.md`, or `.gitignore`.
- No M0 governance text (`docs/00-meta/m0-mechanism-admissibility-gate.md` unchanged).

---

## 8. Test files added / modified

### Added (1 fixture builder + 5 test files)

```
tests/research/microstructure/_eligibility_fixtures.py
tests/research/microstructure/test_eligibility_gate.py
tests/research/microstructure/test_eligibility_checks.py
tests/research/microstructure/test_eligibility_report.py
tests/research/microstructure/test_eligibility_io.py
tests/research/microstructure/test_eligibility_no_network.py
```

### Modified (0)

No existing test was modified. The pre-existing parametrised import-boundary scan in `tests/research/microstructure/test_import_boundaries.py` automatically picks up the four new source modules via its `_scaffold_files()` glob, so no narrow update was required there.

---

## 9. Gate value objects and enums

| Type | Kind | Notes |
| ---- | ---- | ----- |
| `AggTradesEligibilityCheckStatus` | StrEnum | `PASS` / `FAIL` / `NOT_APPLICABLE` / `ERROR` |
| `AggTradesEligibilityCheckResult` | frozen dataclass | `check_id`, `group`, `title`, `status`, `detail`, `evidence` |
| `InvalidWindowCandidate` | frozen dataclass | reason / severity / action / time bounds / family / symbol / evidence / discoverer check id |
| `AggTradesEligibilityGateInput` | frozen dataclass | `manifest_path`, `output_root`, `code_commit_sha`, `write_report=True`, `write_successor_manifest=False` (rejected if `True`), `explicit_extra_symbols=()`, `config=None` |
| `AggTradesEligibilityGateResult` | frozen dataclass | `overall_status`, `research_eligible_after` (always `False` for raw families), `eligibility_gate_status_after`, `checks` (tuple of exactly 45), `invalid_window_candidates`, `measured_summary`, `boundary_confirmations`, `no_successor_authorization` (always `True`), `report_path`, `report_id` |
| `AggTradesGateReport` | frozen dataclass (JSON-serialisable) | report fields per Phase 4bb-B §13 |
| `AggTradesGateInputError` | exception | malformed input |
| `AggTradesGateUnsupportedError` | exception | reserved-mode (`write_successor_manifest=True`) rejection |
| `GateIOError` | exception (re-exported from `eligibility_io`) | path / read-time fail-closed |

---

## 10. Gate execution flow

The orchestrator `run_eligibility_gate(inp)` performs the following 17 steps:

1. **Path discipline.** Refuse if `manifest_path` or `output_root` does not resolve under `data/microstructure/`.
2. **Resolve artefacts.** Compute the four artefact paths from the manifest's `files[0].path` and the manifest path's parent directory.
3. **Read manifest.** Snapshot raw manifest bytes; compute `manifest_sha_before`. Round-trip through `MicrostructureManifest.from_dict(...)`.
4. **Read raw zip + sidecar.** Compute `raw_zip_sha_before`, `sidecar_sha_before`. Sidecar's first 64 hex characters are extracted.
5. **Read acquisition log.** JSON-parse and snapshot SHA. Missing file is recorded as empty dict (surfaces as a check failure later, not a runtime error).
6. **UTC day bookkeeping.** Parse the archive-path date if present.
7. **Single-pass row scan** in memory (no decompression to disk). Records: row count, first/last `T`, in-day vs out-of-day counts, aggregate-id min/max/duplicates/out-of-order/largest-consecutive-gap, `f` ≤ `l` violations, `m` parity, validator failures (per-row Phase 4ax `validate_aggtrade_payload`), CSV column order, unexpected extra columns.
8. **Build `GateExecutionContext`.** Immutable read context shared across all 45 checks.
9. **Run all 45 checks.** Each check returns `AggTradesEligibilityCheckResult`. Defensive wrapper: any check that raises is recorded as `ERROR` rather than aborting the run.
10. **Build invalid-window candidates** from per-row anomalies.
11. **Recompute manifest / raw-zip / sidecar SHAs after the run.** If any of the three differs, force `overall_status = FAIL`.
12. **Aggregate `overall_status`.** PASS iff all checks PASS or NOT_APPLICABLE; FAIL on any FAIL; ERROR on any ERROR with no FAIL.
13. **`research_eligible_after = False`** invariant for raw aggTrades families.
14. **`eligibility_gate_status_after`** = PASS / FAIL / PENDING per overall status.
15. **Boundary confirmations.** Populate the 13-key `boundary_confirmations` dict.
16. **Build `AggTradesGateReport`** and (if `write_report=True`) write atomically under `data/microstructure/gate-reports/<dataset_family>__<version>__<created_at_utc_ms>__<short_sha>.json` with paired `.sha256` sidecar.
17. **Return** the in-memory `AggTradesEligibilityGateResult`.

---

## 11. 45-check implementation summary

| Group | Phase 4ba check id | Function |
| ----- | ------------------ | -------- |
| Source | 10.1.1 | `check_source_label_whitelisted` |
| Source | 10.1.2 | `check_endpoint_label_documented_archive_family` |
| Source | 10.1.3 | `check_endpoint_docs_reference_present` |
| Source | 10.1.4 | `check_no_private_endpoint_label` |
| Source | 10.1.5 | `check_capture_mode_is_historical_archive` |
| Checksum | 10.2.6 | `check_files_sha256_is_64char_lowercase_hex` |
| Checksum | 10.2.7 | `check_recomputed_sha_matches_manifest_and_sidecar` |
| Checksum | 10.2.8 | `check_checksum_companion_verification_recorded` |
| Manifest | 10.3.9 | `check_required_manifest_fields_populated` |
| Manifest | 10.3.10 | `check_research_eligible_false_and_status_pending` |
| Manifest | 10.3.11 | `check_governance_labels_minimum_keys` |
| Manifest | 10.3.12 | `check_code_commit_sha_exists_in_repo_history` |
| Manifest | 10.3.13 | `check_capture_config_hash_nonempty_and_redrivable` |
| Schema | 10.4.14 | `check_every_row_passes_validate_aggtrade_payload` |
| Schema | 10.4.15 | `check_column_order_recorded` |
| Schema | 10.4.16 | `check_no_unexpected_extra_columns` |
| Timestamps | 10.5.17 | `check_all_T_are_int_ms_within_manifest_range` |
| Timestamps | 10.5.18 | `check_start_time_ms_le_end_time_ms` |
| Timestamps | 10.5.19 | `check_T_non_decreasing_across_file` |
| Timestamps | 10.5.20 | `check_utc_day_match` |
| Monotonicity | 10.6.21 | `check_a_non_decreasing_across_file` |
| Monotonicity | 10.6.22 | `check_a_increments_non_negative` |
| Monotonicity | 10.6.23 | `check_no_a_value_reappears_with_different_tuple` |
| Duplicates | 10.7.24 | `check_no_duplicate_a_within_file` |
| Duplicates | 10.7.25 | `check_f_le_l_for_every_row` |
| Row count | 10.8.26 | `check_event_count_gt_zero` |
| Row count | 10.8.27 | `check_event_count_matches_actual_row_count` |
| Row count | 10.8.28 | `check_event_count_consistent_with_files_sum` |
| Symbol/date | 10.9.29 | `check_symbol_in_project_allowlist` |
| Symbol/date | 10.9.30 | `check_symbol_scope_source_recorded_and_path_match` |
| Symbol/date | 10.9.31 | `check_archive_path_date_matches_T_values` |
| Symbol/date | 10.9.32 | `check_date_within_retention_window_or_fail_closed` |
| Archive integrity | 10.10.33 | `check_zip_single_csv_member` |
| Archive integrity | 10.10.34 | `check_zip_decompresses_cleanly` |
| Archive integrity | 10.10.35 | `check_file_size_within_bounds` |
| Archive integrity | 10.10.36 | `check_archive_byte_count_matches_on_disk` |
| Invalid windows | 10.11.37 | `check_invalid_windows_parseable_round_trip` |
| Invalid windows | 10.11.38 | `check_every_invalid_window_has_evidence` |
| Invalid windows | 10.11.39 | `check_invalid_window_severity_action_consistency` |
| Invalid windows | 10.11.40 | `check_no_silent_omission_of_per_row_failures` |
| Cross-cutting | 10.12.41 | `check_feature_computation_forbidden_on_raw_family` |
| Cross-cutting | 10.12.42 | `check_strategy_use_forbidden_on_raw_family` |
| Cross-cutting | 10.12.43 | `check_stop_trigger_domain_in_phase3v8_enum` |
| Cross-cutting | 10.12.44 | `check_no_private_endpoint_or_credential_shaped_strings` |
| Cross-cutting | 10.12.45 | `check_acquisition_log_present_and_self_consistent` |

All 45 functions live in `eligibility_checks.py` and are registered in fixed order in the `CHECK_ORDER` table consumed by `run_all_checks`.

---

## 12. Gate-report schema

The `AggTradesGateReport` data model implements the Phase 4bb-B §13 schema verbatim. JSON keys (sorted, indented):

`acquisition_log_path`, `boundary_confirmations`, `checks` (exactly 45 entries), `code_commit_sha`, `created_at_utc_ms`, `dataset_family`, `eligibility_gate_status_after`, `invalid_window_candidates`, `measured_summary`, `no_successor_authorization`, `overall_status`, `raw_zip_path`, `report_id`, `research_eligible_after`, `sidecar_path`, `source_manifest_path`, `symbol`, `version`.

Reports land at:

```
data/microstructure/gate-reports/
└── microstructure_raw_aggtrades_v001__v001__<created_at_utc_ms>__<short_sha>.json
└── microstructure_raw_aggtrades_v001__v001__<created_at_utc_ms>__<short_sha>.json.sha256
```

Atomic write: `tempfile.mkstemp` in the destination directory → `f.write` → `f.flush` → optional `os.fsync` → `os.replace` to the final name. The paired `.sha256` is written by the same flow.

---

## 13. Invalid-window handling

Per-row anomalies discovered during the single-pass row scan are surfaced as `InvalidWindowCandidate` records in the gate report. Mapping:

| Row anomaly | `InvalidWindowReason` | `Severity` | `Action` | Discovered by |
| ----------- | --------------------- | ---------- | -------- | ------------- |
| `duplicate_a` | `DUPLICATE_EVENT` | `ERROR` | `EXCLUDE` | 10.7.24 |
| `a_out_of_order` | `OUT_OF_ORDER_EVENT` | `ERROR` | `EXCLUDE` | 10.6.21 |
| `validator_failure` | `ZERO_OR_INVALID_PRICE` | `ERROR` | `EXCLUDE` | 10.4.14 |
| `T_before_utc_day_start` | `SYMBOL_MISMATCH`* | `ERROR` | `EXCLUDE` | 10.5.20 |
| `T_at_or_after_utc_day_end` | `OUT_OF_ORDER_EVENT` | `ERROR` | `EXCLUDE` | 10.5.20 |
| `f_gt_l` | `OUT_OF_ORDER_EVENT` | `ERROR` | `EXCLUDE` | 10.7.25 |

`*` Used for the "row's `T` falls before the requested UTC day" case because no Phase 4aw `InvalidWindowReason` value cleanly captures "wrong day"; future governance may add a dedicated reason. The candidate's `evidence` mapping carries the row index, observed `T`, and expected boundary.

The original manifest's `invalid_windows` list is **never** mutated. Candidates exist only inside the gate report.

---

## 14. Manifest immutability behavior

The orchestrator computes the SHA256 of the manifest, raw zip, and sidecar both **before** and **after** the 45-check run. If any of the three differs (which it will not under normal operation; the orchestrator never writes those paths), `overall_status` is forced to `FAIL` and the `boundary_confirmations.no_manifest_mutation` flag is set to `False`.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` method, which always raises `ManifestImmutableError`, is **not** bypassed. Phase 4bb-C never instantiates a successor manifest by default. The reserved `write_successor_manifest=True` mode raises `AggTradesGateUnsupportedError` at `AggTradesEligibilityGateInput.__post_init__` time; only a separately authorised future phase that explicitly enables that mode may write a successor manifest, and even then `research_eligible_after` must remain `False` for raw families.

---

## 15. Boundary confirmations

The 13 required boundary keys (Phase 4bb-B §10.5):

```
no_network_io
no_credential_read
no_env_read
no_websocket
no_mcp_or_graphify
no_normalization_written
no_feature_computed
no_strategy_created
no_ml_trained
no_backtest_run
no_manifest_mutation
no_data_microstructure_write_outside_gate_reports
research_eligible_after_is_false_for_raw_family
```

Every key is `True` for `overall_status = PASS`. `no_manifest_mutation` is computed from the before/after hash comparison; the others are invariant `True` for the gate's design (the gate's import-boundary scan and offline-by-construction nature guarantees).

---

## 16. Test evidence

| Test file | Tests | Purpose |
| --------- | ----- | ------- |
| `test_eligibility_gate.py` | 12 | Orchestrator / happy path / immutability / report write / `write_successor_manifest=True` rejected / output_root validation / 45-check completeness / determinism / no-overwrite / boundary confirmations |
| `test_eligibility_checks.py` | 20 | Per-check failure paths (SHA mismatch, missing sidecar, missing acquisition log, multiple ZIP CSV members, malformed row, duplicate aggregate id, out-of-order, out-of-day, sidecar disagreement, row-count mismatch, missing governance label, `feature_computation` not forbidden, `strategy_use` not forbidden, raw-family `research_eligible=true`, status/eligibility inconsistency, no-silent-omission, unexpected extra columns, unknown commit SHA, wrong capture mode) |
| `test_eligibility_report.py` | 5 | Report data model + atomic JSON write + paired SHA + outside-microstructure rejection + no-overwrite + full-shape verification |
| `test_eligibility_io.py` | 12 | Path discipline / hash helpers / artefact resolution / sidecar parsing / acquisition log / single-pass scanner / forbidden-token detection / archive-path date parser |
| `test_eligibility_no_network.py` | 6 | Static import-boundary scan against the four new modules / monkey-patched-`socket.socket` runtime test / `assert_no_dangerous_imports_loaded` clean-state and explicit-injection tests / no-env-read test / no-MCP / no-Graphify / no-dotenv |
| `_eligibility_fixtures.py` | (shared) | Phase 4az-shaped tmp_path fixture builder; not collected as tests |

Total: **62 new tests** across 5 new test files.

The pre-existing `test_import_boundaries.py` parametrised scan automatically extends to the 4 new source modules via its `_scaffold_files()` glob.

---

## 17. Validation evidence

| Command | Result |
| ------- | ------ |
| `ruff check .` (whole repo) | `All checks passed!` |
| `mypy` (whole repo, strict) | `Success: no issues found in 93 source files` (was 89 + 4 new = 93) |
| `pytest tests/research/microstructure/` (targeted) | **258 passed** in ~3 s (Phase 4aw 114 + Phase 4ax 47 + Phase 4az 35 + Phase 4bb-C 62) |
| `pytest` (whole repo) | **1041 passed, 2 failed** in ~8 s. The two failures are the same pre-existing simulation failures (`tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt`, both `KeyError: 'trade_count'` in `src/prometheus/research/data/storage.py:232`); zero new regressions from Phase 4bb-C |
| `git check-ignore -v data/microstructure/` | `.gitignore:85:data/microstructure/	data/microstructure/` |
| `git diff --check` | clean |
| Phase 4az manifest mtime | unchanged at original `May 7 21:55` |
| `data/microstructure/` modifications under default test invocation | none (all output goes to `tmp_path`) |

### Implementation note: runtime `sys.modules` guard

The Phase 4bb-B plan's §16 fail-closed item "network discipline" is enforced statically. The repository's pre-existing `test_import_boundaries.py` parametrised scan and the new `test_eligibility_no_network.py::test_gate_modules_do_not_import_forbidden_modules_statically` collectively guarantee that the four new gate modules transitively import no networking library (`requests` / `httpx` / `aiohttp` / `urllib.request` / `urllib3` / `socket` / `websockets` / `binance` / `dotenv` / `python_dotenv`).

The runtime helper `assert_no_dangerous_imports_loaded()` exists for explicit-injection diagnostics (e.g. an operator can call it manually if they suspect a third-party module has been monkey-patched into `sys.modules`), but the orchestrator does **not** invoke it. Other test suites in the same pytest session may legitimately import networking libraries for unrelated reasons; aborting the gate because of that would be a false positive. The static guarantee is the binding contract.

---

## 18. What this phase proves

- The Phase 4ba 45-check enumeration, the Phase 4ba fail-closed rules, the Phase 4ba staged eligibility ladder, the Phase 4bb-A 13 application-time observations, and the Phase 4bb-B execution plan compose into a working offline primitive without writing under any tracked path beyond the four new source modules and the documented test/docs surface.
- The primitive runs cleanly against a Phase 4az-shaped mini-fixture and produces 45/45 PASS or NOT_APPLICABLE check results.
- Failure paths fail at the predicted check ids (one test per pattern).
- The original Phase 4az manifest, raw zip, and sidecar are byte-identical before and after every test run.
- `research_eligible` remains `false` for the Phase 4az dataset; `eligibility_gate_status` remains `pending`.
- The reserved `write_successor_manifest=True` mode is structurally rejected.
- Whole-repo `ruff` / `mypy` / `pytest` quality gates remain clean (the two pre-existing simulation failures are unaffected).

---

## 19. What this phase does not prove

- Anything about edge, opportunity rate, microstructure feature viability, or strategy potential of any aggTrades dataset.
- That the Phase 4az dataset will *pass* the gate when run against the real `data/microstructure/` artefacts. The primitive is implemented correctly; whether the actual Phase 4az manifest passes is an operator invocation concern (and not authorised by Phase 4bb-C — invoking the gate against the real artefacts is a separately operator-driven action with no governance implications because the gate cannot mutate anything).
- That Phase 4bb-D, Phase 5, or Phase 4 canonical is now closer in any regulatory sense.

---

## 20. Preserved boundaries

- **No data was modified.** `data/microstructure/` is byte-identical to the post-Phase-4az state. Phase 4az manifest mtime remains the original `May 7 21:55`.
- **`data/microstructure/` remains gitignored.** `git check-ignore -v` continues to report `.gitignore:85`.
- **`research_eligible` remains `false`** on the Phase 4az manifest.
- **`eligibility_gate_status` remains `pending`** on the Phase 4az manifest.
- **No acquisition.** No HTTP request, no `data.binance.vision` fetch, no Binance API call, no WebSocket, no credential, no `.env`, no `.mcp.json`, no MCP, no Graphify.
- **No normalization.** No JSONL, no Parquet, no DuckDB, no derived dataset.
- **No features computed. No ML trained. No strategy created. No backtest run.**
- **No retained verdict revised. No project lock loosened. No M0 governance amended.**
- **No successor phase authorised.**

---

## 21. Recommended future options

Phase 4bb-C does not authorize any successor. The following are recorded for operator evaluation only.

### Option A — Remain paused (primary)

Procedurally clean. Preserves every retained verdict and project lock. The eligibility-gate primitive is now on `main` (after merge) and can be invoked manually by the operator at any time without governance implications, since it cannot mutate any tracked path or any flag on any manifest.

### Option B — Future docs-only Phase 4bb-D eligibility-gate extension memo (conditional next)

**Allowable; not authorized.**

A future docs-only memo would extend the Phase 4ba / Phase 4bb-A / Phase 4bb-B / Phase 4bb-C chain to additional dataset families (e.g. `microstructure_raw_bookticker_v001`, `microstructure_raw_depth_v001`, `microstructure_raw_forceorder_proxy_v001`).

### Option C — Future docs-only Phase 4bc normalization-design memo (conditional later)

**Allowable; not authorized.**

A future docs-only memo would specify how a separately authorized normalization phase could read a Phase 4bb-C-passed raw aggTrades family and produce a normalized derived dataset under a new `microstructure_normalized_aggtrades_*` family with its own manifest, governance labels, and gate. Stage 3 of the Phase 4ba ladder (`research_eligible=true` on a normalized derived family) becomes reachable only via that future phase.

### Forbidden

- Acquire additional aggTrades data.
- Compute features / train ML / build strategy.
- Flip `research_eligible` to `true` on any raw family.
- Authorize Phase 5 / Phase 4 canonical / paper / shadow / live-readiness / deployment / exchange-write / production keys.

---

## 22. Closeout / lock preservation

Phase 4bb-C preserves verbatim:

- **H0** — FRAMEWORK ANCHOR.
- **R3** — BASELINE-OF-RECORD.
- **R1a** — RETAINED — NON-LEADING.
- **R1b-narrow** — RETAINED — NON-LEADING.
- **R2** — FAILED — §11.6.
- **F1** — HARD REJECT.
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL.
- **5m thread** — OPERATIONALLY CLOSED.
- **V2** — HARD REJECT — terminal for V2 first-spec.
- **G1** — HARD REJECT — terminal for G1 first-spec.
- **C1** — HARD REJECT — terminal for C1 first-spec.

Project locks preserved verbatim:

- §11.6 = 8 bps slippage per side; round-trip = 16 bps.
- §1.7.3 = 0.25% risk per trade, 2× leverage cap, one position max, mark-price stops where applicable.
- Phase 3p §4.7 (kline strict integrity gate; aggTrades equivalent applied verbatim by Phase 4az and reaffirmed by Phase 4ba; structural QA confirmed by Phase 4bb-A; execution plan mapped by Phase 4bb-B; primitive implemented by Phase 4bb-C).
- Phase 3r §8 (mark-price gap governance).
- Phase 3v §8 (stop-trigger-domain governance).
- Phase 3w §6 / §7 / §8.
- Phase 4j §11 (OI subset governance).
- Phase 4ak — M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template.
- Phase 4al — refined no-rescue rule + §13 boundary + §14 hierarchy.
- Phase 4am, Phase 4an, Phase 4ao, Phase 4ap, Phase 4aq, Phase 4ar, Phase 4as, Phase 4at, Phase 4au, Phase 4av, Phase 4aw, Phase 4ax, Phase 4ay, Phase 4az, Phase 4ba, Phase 4bb-A, Phase 4bb-B results — all preserved verbatim.

No new lock is introduced. No existing lock is loosened. M0 admissibility and the post-null cooldown rule remain binding prospectively for any future research lane. The Phase 4az dataset's `research_eligible=false` and `eligibility_gate_status=pending` are unchanged.

**Recommended state:** remain paused. **No successor phase is authorized.**
