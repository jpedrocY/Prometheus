# Phase 4bl-D — Multi-Day Raw Manifest Eligibility Gate / Raw QA

## Status

**Branch-complete only. NOT project-complete.** Per the Phase 4bk-A
workflow standard, Phase 4bl-D is not project-complete until a
separately authorized merge phase records its merge-closeout on
`main`. This phase does not authorize any successor phase, paper /
shadow / live / exchange-write / production-key / authenticated-API /
private-endpoint / user-stream / live-WebSocket / MCP / Graphify /
`.mcp.json` / credentials / data-acquisition / normalization / feature
/ label / diagnostic / ML / strategy / backtest work, manifest
mutation, `research_eligible` flip, or `eligibility_gate_status`
transition.

**Gate verdict: RAW_MULTIDAY_GATE_FAIL** (`overall_status = fail`;
4 / 33 critical-severity checks failed). The gate ran to completion
under strict fail-closed discipline, the four failing checks all
trace to a single root cause on the pre-existing Phase 4az 2025-01-15
fixture sidecar (CRLF line-ending instead of canonical Phase 4bb-F
LF), and the gate report records the failure verbatim. The on-disk
v002 manifest is unchanged, no successor was authorized, no
remediation was attempted, and the result is recorded as descriptive
evidence only.

## 1. Phase identity

- **Phase**: Phase 4bl-D — Multi-Day Raw Manifest Eligibility Gate /
  Raw QA.
- **Type**: docs + code + one local gitignored raw gate-report
  artefact (plus its paired `.sha256` sidecar).
- **Branch**: `phase-4bl-d/multi-day-raw-manifest-eligibility-gate`.
- **Base commit (current `main` and `origin/main` at branch creation)**:
  `2576a004c18a76e939303e794317d346c75303d2`.
  This is the Phase 4bl-C SHA-chain fixup commit one commit after the
  Phase 4bl-C merge-closeout commit
  `2ec0a9a5b18214aff99fe86a5fcea3702e20313e`; the fixup records the
  final-SHA value into the Phase 4bl-C merge-closeout's §2 placeholder
  and does not change Phase 4bl-C lifecycle semantics. Phase 4bl-D
  treats `2576a00` as the current valid base.
- **Predecessor lifecycle anchor**: Phase 4bl-C is project-complete on
  `main`. Phase 4bl-C merge commit `691e68c6` and merge-closeout
  `2ec0a9a5` are the canonical lifecycle anchors.
- **Script path**:
  `scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py`.
- **Test path**:
  `tests/research/microstructure/test_phase4bl_d_raw_gate.py`
  (41 offline tests; tmp_path fixtures only).
- **Gate report path (gitignored, NOT committed)**:
  `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a.json`
  with paired `.sha256` sidecar at the same path + `.sha256`. The file
  name embeds the run-time `unix_ms = 1778627360966` and the
  leading-12 hex of the script run's `code_commit_sha =
  2576a004c18a76e939303e794317d346c75303d2` per Phase 4bb-F canonical
  path policy.
- **Clear statement**: Phase 4bl-D is a raw QA / gate phase only. It
  reads the local gitignored Phase 4bl-C v002 artefacts (manifest,
  acquisition log, 90 raw aggTrades ZIPs, paired sidecars), performs
  full per-row schema validation across every aggTrade row, and emits
  a deterministic gate report at the report level only. It performs
  no data acquisition, no network I/O, no manifest mutation, no
  successor-state artefact, no normalization, no derived parquet, no
  features, no labels, no diagnostics, no ML, no strategy, no
  backtest, no paper / shadow / live work. It does not authorize
  Phase 4bl-E or any successor.

## 2. Pre-state

Phase 4bl-C result summary, preserved verbatim from
`docs/00-meta/implementation-reports/2026-05-12_phase-4bl-c_multi-day-aggtrades-acquisition-execution.md`:

- `overall_status`: `SUCCESSFUL_ACQUISITION`
- `acquired_file_count`: 90 / 90
- `missing_file_count`: 0
- `checksum_mismatch_count`: 0
- `checksum_companion_unavailable_count`: 0
- `decompression_failure_count`: 0
- `row_sample_validation_failure_count`: 0
- `finalisation_failure_count`: 0
- `retry_exhausted_count`: 0
- `total_size_bytes`: 1,943,823,208 (~1.81 GiB)
- `total_row_count`: 155,153,449
- `wall_clock_seconds`: 717 (~12 min)
- `existing_fixture_reused`: true
- `existing_fixture_sha_match`: true

Local v002 artefacts verified before any Phase 4bl-D work:

| path | SHA256 (recomputed pre-gate) | size |
| --- | --- | --- |
| `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json` | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | 105,052 |
| `…__v002.json.sha256` | `adaf97242cfbe922bc9e93a6699e547d1b02fa64a96dd2cdd08df1814ce25e26` | 111 |
| `…__v002_acquisition_log.json` | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | 302,055 |
| `…__v002_acquisition_log.json.sha256` | `975bdc544152d1f84f6e700309aad89998e663cb779acc5883bd20652e428958` | 127 |

All four recomputed SHA256 values match the Phase 4bl-C recorded
values exactly. Existing Phase 4az 2025-01-15 fixture is byte-identical
at `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/
2025/01/BTCUSDT-aggTrades-2025-01-15.zip` with SHA256
`f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` and
21,271,119 bytes. Raw zip directory counts:
`2024/12/` 31 zips + 31 sidecars = 62 files;
`2025/01/` 31 zips + 31 sidecars = 62 files;
`2025/02/` 28 zips + 28 sidecars = 56 files; total 180 files = 90
zips + 90 sidecars. Existing fixture preservation rule and
no-successor-authorization invariant are honored.

## 3. Script summary

`scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py` is a
standalone Python script that imports only:

- standard library (`argparse`, `contextlib`, `csv`, `hashlib`, `io`,
  `json`, `os`, `platform`, `re`, `subprocess`, `sys`, `tempfile`,
  `time`, `traceback`, `zipfile`, `collections.abc`, `dataclasses`,
  `datetime`, `pathlib`, `typing`);
- the Phase 4ax aggTrades validator (`validate_aggtrade_payload`,
  `AggTradeValidationError`) for per-row schema validation;
- the Phase 4bb-F canonical-path helpers (`CanonicalPathError`,
  `assert_path_under_gate_reports_subdir`,
  `assert_path_under_microstructure`, `compute_file_sha256`,
  `derive_canonical_gate_report_path`, `derive_sidecar_path`,
  `write_paired_sha256_sidecar`).

No-network boundary:

- No `requests` / `httpx` / `aiohttp` / `urllib3` / `urllib.request`
  / `socket` / `websockets` / `binance` / `dotenv` import.
- No public endpoint, authenticated REST, private endpoint, user
  stream, or WebSocket reference in the script.
- No `.env` read. No `.mcp.json` read. No MCP / Graphify.

Path guard:

- All input paths are validated under `data/microstructure/`.
- Manifest-recorded `microstructure/...` paths are explicitly resolved
  via `assert_relative_under_microstructure(...)` which rejects
  backslashes, absolute paths, parent references, dot prefixes,
  dotfiles, and paths not starting with `microstructure/`.

Gitignore guard:

- `git check-ignore` is invoked at gate-run time on
  `data/microstructure/`, `data/microstructure/gate-reports/`, and
  `data/microstructure/gate-reports/raw/` before any write occurs.

Sidecar validation:

- `parse_canonical_sidecar(...)` enforces the Phase 4bb-F canonical
  body shape `<sha>  <basename>\n` (two spaces, trailing newline,
  lowercase 64-char hex SHA256).
- Manifest sidecar, acquisition-log sidecar, and every raw zip
  sidecar are parsed and verified to match their target file's
  recomputed SHA256.
- Manifest sidecar and log sidecar self-SHA256 are also verified
  against the Phase 4bl-C recorded values.

Manifest / log validation:

- Manifest schema required-keys check.
- Acquisition log schema required-keys check.
- Manifest scope-lock check (dataset family, version, schema version,
  symbol list, date range, date count, expected file count).
- Manifest `date_list` equality to deterministically generated 90-day
  list (`2024-12-01` … `2025-02-28` UTC inclusive).
- Counter consistency between manifest and acquisition-log summary
  (acquired file count, total size bytes, total row count).
- Per-file inventory required-keys check.
- `no_extra_dates` and `no_missing_dates` against the locked date set.
- `no_unexpected_statuses` requires every entry's status to be
  `acquired_verified`.

Raw zip scanning:

- For every date in the locked 90-day list, the gate resolves the
  manifest's `local_zip_path` and `local_sidecar_path`, verifies file
  existence, recomputes the zip's SHA256 (chunked, 1 MiB), recomputes
  its size, parses the paired `.sha256` sidecar canonically, and
  cross-checks all three SHA256 values (manifest, computed, sidecar).
- The zip is opened once via `zipfile.ZipFile`, `testzip()` is
  invoked, and the CSV-member set is validated to be exactly one
  CSV.

Full per-row validation:

- The CSV member is streamed via `csv.reader` once per file.
- Header detection mirrors Phase 4az / Phase 4bl-C (`_HEADER_ALIASES`
  for the `agg_trade_id / price / quantity / first_trade_id /
  last_trade_id / transact_time / is_buyer_maker` columns; headerless
  default `("a", "p", "q", "f", "l", "T", "m")`).
- Every row is decoded into a Phase 4ax payload via `_row_to_payload`
  (including strict `is_buyer_maker` `true/True/TRUE/false/False/FALSE`
  coercion) and validated via `validate_aggtrade_payload(payload)`.
- For every row, the gate enforces:
  - UTC-day boundary `start_ms <= T < start_ms_next_day` for the
    file's date;
  - strictly-increasing aggregate trade IDs (i.e. no duplicates and
    no out-of-order rows).
- Per-row `row_count`, `first_T`, `last_T`, `min_a`, `max_a` are
  accumulated and compared exactly to the manifest's `row_count`,
  `first_trade_time_ms`, `last_trade_time_ms`, `min_agg_trade_id`,
  `max_agg_trade_id`.

Row-count / time-bound / id checks:

- Recomputed `total_row_count` and `total_size_bytes` are summed
  across all 90 files and compared exactly to the manifest's
  `total_row_count = 155,153,449` and
  `total_size_bytes = 1,943,823,208`.
- Adjacent-date overlap check: for each consecutive pair of dates in
  the locked date list, the gate asserts
  `min_a(date_n+1) > max_a(date_n)`.
- Existing fixture preservation: 2025-01-15 zip computed SHA256 must
  equal the Phase 4az recorded value
  `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`,
  and its manifest `local_zip_path` must equal the Phase 4az fixture
  path verbatim.

Fail-closed discipline:

- A per-file sidecar parse error stops further per-row validation for
  that file (the row count, time bounds, and agg-id bounds for that
  date are recorded as `None`), but the gate continues processing the
  remaining 89 dates. The aggregate-summary checks then run against
  the remaining files, so any cascading mismatch (e.g.
  `total_row_count`) is also recorded.

Gate report writing:

- The canonical gate-report path is derived via
  `derive_canonical_gate_report_path(family="raw", dataset_family=
  "microstructure_raw_aggtrades_v001", dataset_version="v002",
  phase_id="4bl-d", generated_at_unix_ms=<run unix ms>,
  code_commit_sha=<HEAD>)` under
  `data/microstructure/gate-reports/raw/`. The brief suggested the
  static name
  `microstructure_raw_aggtrades_v001__v002__phase-4bl-d_raw_gate.json`;
  Phase 4bl-D follows the Phase 4bb-F canonical-path policy instead,
  which embeds the run unix-ms and the leading-12-hex of `HEAD`. The
  canonical form is the established convention for every prior gate
  report (Phase 4bb-D / 4bf / 4bi-B / 4bj-E). This deviation is
  recorded here verbatim per the brief.
- The gate report JSON is serialised with
  `json.dumps(..., sort_keys=True, indent=2, ensure_ascii=False)`
  plus a single trailing newline for determinism.
- Atomic write-then-rename via `tempfile.mkstemp` + `os.replace`;
  refuses to overwrite an existing report. Paired `.sha256` sidecar
  is written via `write_paired_sha256_sidecar` with
  `refuse_overwrite=True`.

## 4. Gate result

**Final verdict: `RAW_MULTIDAY_GATE_FAIL`.**

- `overall_status`: **fail**
- `gate_verdict`: **RAW_MULTIDAY_GATE_FAIL**
- `checks_total`: 33
- `checks_passed`: 29
- `checks_failed`: 4
- `checks_error`: 0
- `checks_not_applicable`: 0
- `acquired_file_count_verified`: 89 / 90 reached per-row validation
  (one date, `2025-01-15`, stopped at sidecar-parse step under
  fail-closed discipline; see §4.A)
- `recomputed_total_row_count`: **153,472,351** vs manifest
  `155,153,449` and Phase 4bl-C expected `155,153,449` —
  short by exactly `1,681,098` rows, which is the recorded Phase 4az
  2025-01-15 row count
- `recomputed_total_size_bytes`: **1,943,823,208** (matches manifest
  and Phase 4bl-C expected exactly, including the 21,271,119-byte
  2025-01-15 zip — the zip itself is byte-identical; the failure is
  on its paired sidecar only)
- `all_rows_validated_count`: 153,472,351 (rows that reached the
  Phase 4ax validator)
- `all_schema_validation_errors_count`: 0
- `all_timestamp_boundary_errors_count`: 0
- `all_duplicate_agg_trade_id_errors_count`: 0
- `all_monotonicity_errors_count`: 0
- `adjacent_date_overlap_errors_count`: 0
- `existing_fixture_preservation_zip_sha`: **pass** (2025-01-15 zip
  SHA256 matches Phase 4az recorded value
  `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`
  exactly; manifest `local_zip_path` matches Phase 4az fixture path
  verbatim)
- `manifest_mutated`: false
- `manifest_transition_performed`: false
- `research_eligible_after`: false
- `eligibility_gate_status_after`: `fail_report_level_only` — this
  is a report-level recommendation only; the on-disk manifest's
  `eligibility_gate_status` remains `pending`.
- `no_successor_authorization`: true
- `strict_fail_closed`: true

### 4.A Failure analysis (single root cause; four cascaded checks)

The four failing checks all trace to a single binding root cause:
**the pre-existing Phase 4az 2025-01-15 fixture sidecar uses Windows
CRLF (`\r\n`) line terminator instead of the Phase 4bb-F canonical
LF (`\n`) terminator.** All 89 Phase 4bl-C newly-acquired sidecars,
the v002 manifest sidecar, and the v002 acquisition-log sidecar use
the canonical LF terminator. The fixture sidecar was written on Windows
on 2026-05-07 during the Phase 4az acquisition run and predates the
Phase 4bb-F canonical-path policy.

Direct evidence:

- `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256`
  is **100 bytes** with last bytes `b'.zip\r\n'`.
- A representative Phase 4bl-C sidecar
  (`…/2025/01/BTCUSDT-aggTrades-2025-01-16.zip.sha256`) is **99
  bytes** with last bytes `b'.zip\n'`.
- The 2024-12-01 sidecar is also **99 bytes** with `b'.zip\n'`.
- The manifest sidecar is **111 bytes** with `b'.json\n'`.
- The acquisition-log sidecar is **127 bytes** with `b'.json\n'`.

The Phase 4bb-F canonical sidecar contract requires exactly
`<sha>  <basename>\n` (two spaces; single trailing newline). The
gate's `parse_canonical_sidecar(...)` correctly rejects the CRLF
form, marks `2025-01-15` per-file `status = fail` with
`first_failure_reason = 'sidecar parse failed: GateRuntimeError:
sidecar text does not match canonical format \'<sha>  <basename>\\n\';
got \'f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e
  BTCUSDT-aggTrades-2025-01-15.zip\\r\\n\''`, and under fail-closed
discipline stops further per-row validation for that file (so
`rows_validated = 0`, `computed_row_count = None`,
`computed_first_trade_time_ms = None`, `computed_last_trade_time_ms
= None`, `computed_min_agg_trade_id = None`, `computed_max_agg_trade_id
= None` for the 2025-01-15 record).

The four failed checks are (verbatim from the gate report):

1. `raw_zip_sidecar_integrity` — critical — `sidecar_count = 89` vs
   expected `90`; `sidecar_format_failure_count = 1` (date
   `2025-01-15`); `sidecar_sha_mismatch_count = 0`. (The sidecar's
   recorded hex SHA matches the zip's SHA exactly; only the
   terminator differs.)
2. `per_file_row_count_consistency` — critical — mismatched dates
   `['2025-01-15']` because the gate-recomputed `row_count` is
   `None` (validation skipped) and the manifest entry is `1,681,098`.
3. `per_file_time_bounds_consistency` — critical — mismatched
   bounds `['2025-01-15: first_trade_time_ms',
   '2025-01-15: last_trade_time_ms', '2025-01-15: min_agg_trade_id',
   '2025-01-15: max_agg_trade_id']` because the gate skipped row
   iteration for 2025-01-15 under fail-closed discipline. (Same
   single root cause.)
4. `total_row_count_consistency` — critical —
   `recomputed_total_row_count = 153,472,351` vs
   `manifest_total_row_count = 155,153,449` and
   `phase_4bl_c_expected = 155,153,449`; the shortfall is
   `155,153,449 − 153,472,351 = 1,681,098`, which exactly equals
   the Phase 4az 2025-01-15 row count. (Same single root cause:
   2025-01-15 rows were not iterated because its sidecar parse
   failed.)

Critical observations:

- The 2025-01-15 zip itself is byte-identical to the Phase 4az
  fixture; its recomputed SHA256 (`f560c2e5...`) matches the
  manifest's recorded value and the Phase 4az recorded value
  exactly. The data on disk is uncorrupted. Only the sidecar's
  line terminator differs from canonical.
- All 89 other files passed all checks under full per-row schema
  validation. 153,472,351 aggTrade rows were validated under Phase
  4ax with zero schema errors, zero timestamp-boundary errors, zero
  duplicate aggregate-trade-IDs, zero monotonicity errors, and zero
  adjacent-date overlap errors.
- The fail-closed discipline worked as designed. The gate did NOT
  silently accept CRLF; it did NOT attempt to repair the sidecar;
  it did NOT mutate the on-disk fixture; it did NOT promote
  `research_eligible`; it did NOT transition the on-disk
  `eligibility_gate_status`. It recorded the issue, classified it
  critical, and stopped at the report level.
- The 2025-01-15 zip SHA preservation check
  (`existing_fixture_preservation_zip_sha`) passed independently
  of the sidecar-format failure, because the zip is fine.

### 4.B Per-file status counts

- Per-file `status = pass`: 89 / 90 (every date except 2025-01-15).
- Per-file `status = fail`: 1 / 90 (2025-01-15 only).
- Every passing per-file record has: zip SHA256 matches manifest;
  zip size matches manifest; sidecar canonical format pass; sidecar
  SHA matches zip; ZIP `testzip()` clean; exactly one CSV member;
  every row passes `validate_aggtrade_payload`; row count matches
  manifest exactly; first/last trade times and min/max aggregate
  trade IDs match manifest exactly; UTC-day boundary respected;
  strictly-increasing aggregate trade IDs.

## 5. Local output inventory

- **Gate report**:
  - Path:
    `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a.json`
  - SHA256:
    `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7`
  - Size: 169,637 bytes
- **Gate report sidecar**:
  - Path: same path + `.sha256`
  - Body (canonical Phase 4bb-F format):
    `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7  microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a.json\n`
    (two spaces, trailing LF)
  - SHA256 (self):
    `b201dcd977ea2ef370b502f3840d90d6efd28b10354ca30eafcf155838c7a9c6`
  - Size: 153 bytes
- Neither file is committed. Both are gitignored under
  `.gitignore:85: data/microstructure/`.
- No `data/microstructure/` artefact other than the new gate report
  and its sidecar was created, modified, moved, renamed, or deleted.
- No manifest mutation. No existing-fixture mutation. In particular,
  the 2025-01-15 fixture sidecar's CRLF terminator was NOT repaired
  by Phase 4bl-D — repairing it would be a mutation of a pre-existing
  Phase 4az fixture artefact, which is explicitly out of scope for
  Phase 4bl-D and would require separate authorization.

## 6. Validation commands and results

### Pre-state and path discipline

- `git rev-parse main` and `git rev-parse origin/main`:
  `2576a004c18a76e939303e794317d346c75303d2` for both.
- `git status --short` before any Phase 4bl-D commit shows only the
  pre-existing untracked entry `data/research/` (and a transient
  scheduler lock).
- `git check-ignore -v data/microstructure/`:
  `.gitignore:85:data/microstructure/	data/microstructure/`.
- `git check-ignore -v data/microstructure/gate-reports/raw/`:
  `.gitignore:85:data/microstructure/	data/microstructure/gate-reports/raw/`.
- `git check-ignore -v` on the gate report path and its sidecar:
  both gitignored under `.gitignore:85: data/microstructure/`.

### Lint, compile, tests

- `python -m py_compile scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py`:
  OK.
- `python -m py_compile tests/research/microstructure/test_phase4bl_d_raw_gate.py`:
  OK.
- `uv run ruff check scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py`:
  All checks passed.
- `uv run ruff check tests/research/microstructure/test_phase4bl_d_raw_gate.py`:
  All checks passed.
- `uv run pytest tests/research/microstructure/test_phase4bl_d_raw_gate.py`:
  **41 passed**.
- Whole-repo `pytest` and whole-repo `mypy` were NOT rerun by Phase
  4bl-D (no source-package code was modified). The latest authoritative
  whole-repo validation remains the Phase 4bb-F-implementation merge
  baseline (`ruff` PASS, `mypy` strict 120 source files PASS,
  `pytest tests/research/microstructure/` 915 passed + 1 pre-existing
  labelled skip, whole-repo `pytest` 1698 passed + 1 skipped + 2
  pre-existing simulation failures).

### Gate execution

- Command:
  `python scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py --log-progress`
- `run_wall_clock_seconds`: **880.188** (~14.67 min) for full per-row
  validation across 153,472,351 successfully-iterated rows from 89
  dates plus checksum verification of all 90 zips and sidecars.
- Final stdout summary (verbatim):

  ```text
  [Phase 4bl-D] gate verdict:        RAW_MULTIDAY_GATE_FAIL
  [Phase 4bl-D] overall_status:      fail
  [Phase 4bl-D] checks pass/fail/err/na/total: 29/4/0/0/33
  [Phase 4bl-D] recomputed_total_row_count:  153472351
  [Phase 4bl-D] recomputed_total_size_bytes: 1943823208
  [Phase 4bl-D] report_path:         data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a.json
  [Phase 4bl-D] report_sha256:       d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7
  [Phase 4bl-D] sidecar_path:        data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a.json.sha256
  [Phase 4bl-D] wall_clock_seconds:  880.19
  [Phase 4bl-D] failure_reasons (first 5):
    - sidecar format failures=1, sidecar sha mismatches=0
    - row count mismatches at ['2025-01-15']
    - per-file time/agg-id bounds mismatches: ['2025-01-15: first_trade_time_ms', '2025-01-15: last_trade_time_ms', '2025-01-15: min_agg_trade_id', '2025-01-15: max_agg_trade_id']
    - total_row_count mismatch: recomputed=153472351 manifest=155153449 expected=155153449
  ```

### SHA256 recomputation evidence (upstream artefact immutability)

All five upstream artefacts are byte-for-byte identical pre/post the
gate run; the gate did not modify any input file.

| artefact | path | expected SHA256 | recomputed SHA256 (post-gate) | match |
| --- | --- | --- | --- | --- |
| v002 manifest | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json` | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | ✅ match |
| v002 manifest sidecar | `…__v002.json.sha256` | `adaf97242cfbe922bc9e93a6699e547d1b02fa64a96dd2cdd08df1814ce25e26` | `adaf97242cfbe922bc9e93a6699e547d1b02fa64a96dd2cdd08df1814ce25e26` | ✅ match |
| v002 acquisition log | `…__v002_acquisition_log.json` | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | ✅ match |
| v002 acquisition log sidecar | `…__v002_acquisition_log.json.sha256` | `975bdc544152d1f84f6e700309aad89998e663cb779acc5883bd20652e428958` | `975bdc544152d1f84f6e700309aad89998e663cb779acc5883bd20652e428958` | ✅ match |
| Phase 4az 2025-01-15 zip | `…/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip` | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | ✅ match |

The 2025-01-15 fixture **sidecar** is preserved verbatim at 100 bytes
with CRLF terminator (the gate did not normalize it). The
fixture **zip** itself is byte-identical to the Phase 4az recorded
value. Per the brief, no `data/microstructure/` artefact other than
the new gate report and its sidecar was created, modified, moved,
renamed, or deleted.

### Counts

- Raw zip count: 90 (verified by gate; matches `expected_file_count`).
- Raw sidecar count on disk: 90; canonical-format-passing sidecars:
  **89 / 90** (2025-01-15 sidecar uses CRLF instead of LF).
- Per-month: 31 (2024-12), 31 (2025-01), 28 (2025-02).

### Post-state git status

- `git status --short` after the gate run shows the new local
  artefacts under `data/microstructure/gate-reports/raw/` as ignored
  (not staged, not tracked), plus the pre-existing untracked entries.
- No tracked file under `data/microstructure/` exists at any point.

## 7. Boundary confirmations

This phase performed:

- no data acquisition;
- no downloads;
- no endpoint calls;
- no normalization;
- no feature computation;
- no label computation;
- no diagnostics;
- no label statistics;
- no ML;
- no strategy;
- no signal;
- no backtest;
- no successor-state artefact creation;
- no manifest mutation (the on-disk v002 manifest's
  `research_eligible` remains `false`, `eligibility_gate_status`
  remains `pending`; manifest mtime is unchanged across the run);
- no `research_eligible` flip on any manifest;
- no `eligibility_gate_status` transition on any actual manifest;
- no `chronological_split_policy` change on any manifest;
- no commit under `data/microstructure/`;
- no remediation of the 2025-01-15 sidecar CRLF terminator
  (mutating a pre-existing Phase 4az fixture artefact is explicitly
  out of scope for Phase 4bl-D; this is recorded as a finding,
  not a fix);
- no modification to any other `data/microstructure/` artefact
  (the Phase 4az raw fixture, the Phase 4bd derived parquet +
  manifest, the Phase 4bf derived-family gate report, the Phase
  4bg-B successor-state, the Phase 4bh feature parquet + manifest,
  the Phase 4bi-B feature-family gate report, the Phase 4bi-D
  feature-family successor-state, the Phase 4bj-C label parquet +
  manifest, the Phase 4bj-E label-family gate report, the Phase
  4bj-G label successor-state, the Phase 4bj-J no-split
  determination, and the Phase 4bb-G raw successor-state are all
  byte-identical pre/post);
- no authenticated API call; no private endpoint; no user stream;
  no WebSocket; no listenKey; no credentials; no `.env` read; no
  `.mcp.json` read; no MCP; no Graphify.

## 8. Recommended state

**Recommended state**: remain paused after Phase 4bl-D branch
completion. The gate FAIL is recorded as descriptive evidence only;
no remediation is authorized by this phase.

**Operator decision menu (NOT authorized by Phase 4bl-D)**:

- **Option A — remain paused** (primary). Treat the Phase 4bl-D
  gate report as recorded research evidence: the Phase 4bl-C data
  is empirically clean (all 153,472,351 iterated rows pass every
  Phase 4ax schema check and every per-file and aggregate
  consistency check; all upstream artefact SHAs are byte-identical
  to recorded values; the 2025-01-15 zip is byte-identical to the
  Phase 4az fixture), but the gate cannot issue a PASS verdict
  because the pre-existing Phase 4az 2025-01-15 fixture sidecar's
  CRLF line terminator is non-canonical under Phase 4bb-F. Until
  separately authorized, the v002 raw family remains
  `research_eligible = false` / `eligibility_gate_status = pending`
  on the actual manifest, and no successor (Phase 4bl-E, normalization,
  features, labels, diagnostics, ML, strategy, backtest, paper /
  shadow / live) is authorized.

- **Option B — future docs-only sidecar-canonicalization governance
  memo** (conditional secondary; NOT authorized). A separately
  authorized future memo could decide between:
  - **B1**: normalize the Phase 4az 2025-01-15 sidecar to canonical
    LF and re-run a future Phase 4bl-D-equivalent gate;
  - **B2**: amend the Phase 4bb-F canonical sidecar format to
    explicitly grandfather the Phase 4az fixture sidecar CRLF and
    re-run a future Phase 4bl-D-equivalent gate;
  - **B3**: amend the gate to accept CRLF as canonical-equivalent
    and re-run.
  Each of B1 / B2 / B3 mutates a pre-existing artefact or a
  governance contract and therefore requires separate operator
  authorization. Phase 4bl-D explicitly does NOT recommend any of
  the three; the operator decision is deferred.

- **Option C — Phase 4bl-E without remediating Phase 4bl-D FAIL**
  (NOT recommended; NOT authorized). Running Phase 4bl-E (multi-day
  raw successor-state recording) directly without first resolving
  the Phase 4bl-D FAIL would be inconsistent with the project's
  established `<gate-passes-first>` precedent (Phase 4bb-D PASS →
  Phase 4bb-G; Phase 4bf PASS → Phase 4bg-B; Phase 4bi-B PASS →
  Phase 4bi-D; Phase 4bj-E PASS → Phase 4bj-G). Phase 4bl-D
  explicitly does NOT recommend this path.

**Explicitly NOT authorized by Phase 4bl-D**:

- Phase 4bl-E / Phase 5 / any successor phase remains unauthorized.
- Paper / shadow, live-readiness, deployment, production keys,
  authenticated APIs, private endpoints, public-endpoint calls in
  code, user stream, WebSocket implementation, MCP, Graphify,
  `.mcp.json`, credentials, exchange-write, and any additional
  acquisition beyond the 90 locked BTCUSDT UTC dates all remain
  unauthorized.
- M0 mechanism-admissibility gate and the post-null cooldown rule
  remain binding prospective governance for any future research
  lane.

## 9. Retained verdicts preserved verbatim

- H0 — FRAMEWORK ANCHOR
- R3 — BASELINE-OF-RECORD
- R1a — RETAINED — NON-LEADING
- R1b-narrow — RETAINED — NON-LEADING
- R2 — FAILED — §11.6
- F1 — HARD REJECT
- D1-A — MECHANISM PASS / FRAMEWORK FAIL
- 5m thread — OPERATIONALLY CLOSED
- V2 — HARD REJECT — terminal for V2 first-spec
- G1 — HARD REJECT — terminal for G1 first-spec
- C1 — HARD REJECT — terminal for C1 first-spec

## 10. Preserved project locks

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% risk per trade / 2× leverage cap / one-position
  max / mark-price stops
- M0 (Phase 4ak) twelve-clause gate remains binding
- Phase 4ak post-null cooldown rule remains binding
- Phase 4ak cooled-down families list remains binding
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
  remains binding
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant remains binding (never invoked by Phase
  4bl-D)
- Phase 3v §8 stop-trigger-domain governance remains binding
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
  governance remains binding
- Phase 4bb-F canonical path policy remains binding (Phase 4bl-D
  follows it for the gate report filename and identified one
  pre-existing fixture sidecar that does not conform — recorded
  as a finding, not amended)
