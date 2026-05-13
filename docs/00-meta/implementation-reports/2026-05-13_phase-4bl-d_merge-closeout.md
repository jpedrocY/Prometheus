# Phase 4bl-D — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bl-D — Multi-Day Raw Manifest Eligibility Gate / Raw QA
- **Type:** docs + code + one local gitignored gate-report artefact and
  paired sidecar
- **Action:** merge into `main`
- **Merge purpose:** Bring Phase 4bl-D from branch-complete to
  project-complete status per the Phase 4bk-A workflow standard.
  Phase 4bl-D implemented and ran a multi-day raw eligibility gate
  for the Phase 4bl-C v002 multi-day BTCUSDT aggTrades acquisition
  (90 UTC dates 2024-12-01 through 2025-02-28; 155,153,449 rows;
  1,943,823,208 bytes), with full per-row Phase 4ax
  `validate_aggtrade_payload` validation across every row of every
  file. The gate emitted **`RAW_MULTIDAY_GATE_FAIL`** with 29 / 33
  PASS and 4 / 33 FAIL, driven by a single root cause: the
  pre-existing Phase 4az 2025-01-15 fixture sidecar at
  `data/microstructure/raw/microstructure_raw_aggtrades_v001/
  BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256` uses
  Windows CRLF (`\r\n`, 100 bytes) instead of the canonical
  Phase 4bb-F LF (`\n`, 99 bytes) terminator. Under fail-closed
  discipline, the gate's `parse_canonical_sidecar(...)` rejected the
  CRLF form, marked the `2025-01-15` per-file entry `status = fail`,
  and skipped per-row iteration for that file only; the remaining
  89 dates all ran clean. The branch added one standalone gate
  script (`scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py`;
  stdlib + Phase 4ax `validate_aggtrade_payload` + Phase 4bb-F
  `canonical_paths` only; no `prometheus.runtime` / `execution` /
  `persistence` imports; no `requests` / `httpx` / `aiohttp` /
  `urllib` / `urllib3` / `socket` / `websockets` / `binance` /
  `dotenv` imports; no network I/O; no credentials; no `.env`;
  no `.mcp.json`; no MCP / Graphify; no authenticated REST; no
  private endpoints; no public REST endpoints; no WebSocket; no
  `listenKey`); one offline test suite
  (`tests/research/microstructure/test_phase4bl_d_raw_gate.py`; 41
  tests; all pass); the Phase 4bl-D implementation report; the
  Phase 4bl-D closeout; and one narrow `current-project-state.md`
  update. The gate report and paired SHA256 sidecar live strictly
  under the gitignored `data/microstructure/gate-reports/raw/`
  namespace and are **not committed**. No manifest is mutated; no
  successor phase is authorized; the v002 raw manifest remains
  `research_eligible = false` / `eligibility_gate_status =
  "pending"` (locked invariants for raw families per Phase 4bb-E).
  The FAIL verdict is recorded as descriptive evidence only;
  remediation of the CRLF terminator (mutating a pre-existing
  Phase 4az fixture artefact) is **out of scope** and is deferred
  to a separately authorized governance memo.
- **Target branch:** `main`
- **Source branch:** `phase-4bl-d/multi-day-raw-manifest-eligibility-gate`

## 2. SHAs

- **`main` SHA before merge:** `2576a004c18a76e939303e794317d346c75303d2`
  (Phase 4bl-C SHA-chain-fixup commit on top of the Phase 4bl-C
  merge-closeout `2ec0a9a5b18214aff99fe86a5fcea3702e20313e`).
- **`origin/main` SHA before merge:** `2576a004c18a76e939303e794317d346c75303d2`
  (identical to `main`; up-to-date with origin).
- **Phase 4bl-D branch commit SHA:** `5092a391535f5a188f6ebf0ad232893ba9e46ceb`
  (`docs(phase-4bl-d): multi-day raw manifest eligibility gate (FAIL)`).
- **Merge commit SHA:** `093c42cffc8cf450e7b328da304e787d0be39fa1`
  (`docs(phase-4bl-d): merge multi-day raw manifest eligibility gate (FAIL)`).
- **Merge-closeout commit SHA:** to be filled at commit time of this
  merge-closeout file.
- **Final `main` / `origin/main` SHA after push:** the canonical
  project-complete anchor for Phase 4bl-D is the merge-closeout
  commit recorded in this file. Any one-commit SHA-chain-fixup on
  top of that anchor only records the final-`main` SHA value back
  into §2 of this merge-closeout; it does not change Phase 4bl-D
  lifecycle semantics, consistent with the Phase 4bb-G /
  Phase 4bb-F-implementation / Phase 4bb-F / Phase 4bj-G /
  Phase 4bj-F / Phase 4bj-H / Phase 4bj-I / Phase 4bj-J /
  Phase 4bj-K / Phase 4bl-A / Phase 4bl-B / Phase 4bl-C
  SHA-chain-fixup precedents.

## 3. Merge method

- Command: `git merge --no-ff phase-4bl-d/multi-day-raw-manifest-eligibility-gate -m "docs(phase-4bl-d): merge multi-day raw manifest eligibility gate (FAIL)"`
- Strategy: `ort` (the default).
- Merge commit message: `docs(phase-4bl-d): merge multi-day raw manifest eligibility gate (FAIL)`
  (single subject line followed by a multi-paragraph body recording
  the FAIL verdict, the four failed check IDs, the single root cause,
  the no-remediation discipline, the byte-identical immutability of
  every upstream artefact, the preservation of every retained verdict
  and project lock, and the explicit non-authorization of every
  successor phase).
- Push status: will be pushed to `origin/main` with no force, no
  skip-hooks, no skip-signing.

## 4. Files brought forward by the merge

### Docs (added)

- `docs/00-meta/implementation-reports/2026-05-13_phase-4bl-d_multi-day-raw-manifest-eligibility-gate.md`
  (the Phase 4bl-D main implementation report; 647 lines; 31,466
  bytes; rewritten to faithfully reflect the FAIL outcome; §4.A
  failure analysis records the single root cause and the four
  cascaded check failures; §8 operator decision menu records
  Option A remain paused as primary and Options B / C / D / E all
  as NOT authorized).
- `docs/00-meta/implementation-reports/2026-05-13_phase-4bl-d_closeout.md`
  (the Phase 4bl-D closeout; 249 lines; 10,559 bytes; rewritten to
  reflect the FAIL verdict; records the exact gate result, the
  validation results, the no-successor constraints, and the
  preserved retained-verdict ledger / project locks).

### Docs (modified narrowly)

- `docs/00-meta/current-project-state.md` (new Phase 4bl-D narrative
  paragraph prepended above the Phase 4bl-C paragraph; new "Current
  phase:" Phase 4bl-D block replacing the prior top "Current phase:"
  Phase 4bl-C block; prior Phase 4bl-C "Current phase:" block
  preserved as historical context immediately below the new block
  per the documented standard; +325 lines).

### Source (added)

- `scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py`
  (standalone Python gate script; stdlib + Phase 4ax
  `validate_aggtrade_payload` + Phase 4bb-F `canonical_paths` only;
  no network I/O; no credentials; no `.env`; no `.mcp.json`; no
  authenticated REST; no private endpoints; no public REST
  endpoints; no WebSocket; no `listenKey`; ruff clean; py-compile
  clean; +2,880 lines).

### Tests (added)

- `tests/research/microstructure/test_phase4bl_d_raw_gate.py`
  (41 offline tests using only pytest `tmp_path` and synthetic
  fixtures; covers date list, UTC window, sidecar parsing, path
  discipline, CSV row helpers, `validate_one_file` happy /
  SHA-mismatch / missing-sidecar / duplicate-id / out-of-order /
  out-of-day / multi-CSV-member / row-count-mismatch paths,
  deterministic JSON, refuse-overwrite, forbidden-imports scan,
  check-IDs-match-brief, locked-scope constants; all 41 pass;
  +881 lines).

### Config / data

- None modified. None added. None removed.
- No `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`,
  or MCP file change.
- **No `data/microstructure/` file modified.** No raw zip, no
  raw manifest, no sidecar, no acquisition log, no prior gate
  report, no successor-state, no normalized parquet, no feature
  parquet, no label parquet, no diagnostic artefact, no split
  artefact created or modified through the tracked diff. The
  Phase 4bl-D local gate-report output (one gate-report JSON +
  one paired `.sha256` sidecar under `gate-reports/raw/`) lives
  strictly under the gitignored `data/microstructure/` namespace
  and was produced by the Phase 4bl-D branch gate execution (not
  by the merge). See §7 for full path / SHA / size detail.
- No artefact under `data/raw/`, `data/normalized/`,
  `data/manifests/`, `data/derived/`, or any other project data
  path created or modified.

### Prior source / tests / scripts / governance memos

- None modified. The branch adds new files only; it does not edit
  any pre-existing source module, test, script, or governance memo
  (other than the narrow `current-project-state.md` paragraph
  addition and Current-phase block replacement). The Phase 4aw
  microstructure scaffold modules, the Phase 4ax aggTrades
  validator, the Phase 4bb-F canonical-paths helpers, and all
  prior source modules are unchanged.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              |  325 +++
 .../2026-05-13_phase-4bl-d_closeout.md             |  249 ++
 ...bl-d_multi-day-raw-manifest-eligibility-gate.md |  647 +++++
 ...ase4bl_d_validate_multiday_raw_manifest_gate.py | 2880 ++++++++++++++++++++
 .../microstructure/test_phase4bl_d_raw_gate.py     |  881 ++++++
 5 files changed, 4982 insertions(+)
```

- 5 tracked files: 4,982 insertions, 0 deletions.
- No file deletions.
- No file renames.
- No file moves.
- No binary file changes.
- The diff matches the expected change set from the Phase 4bl-D
  authorization prompt exactly.

## 6. Result / verdict

- **Status:** SUCCESSFUL_MERGE.
- **Verdict:** GATE_REPORT_RECORDED (FAIL) — the Phase 4bl-D
  multi-day raw manifest eligibility gate is now part of the
  canonical project history on `main`. Phase 4bl-D is
  project-complete only after this merge-closeout commit is
  recorded on `main`. The gate produced a FAIL verdict
  (`overall_status = "fail"`; `checks_total / passed / failed /
  error / not_applicable = 33 / 29 / 4 / 0 / 0`) due to one
  pre-existing Phase 4az 2025-01-15 sidecar CRLF terminator. The
  on-disk gate report and paired sidecar remain locally under the
  gitignored `data/microstructure/gate-reports/raw/` namespace;
  they are reproducible from the Phase 4bl-C local artefacts and
  the Phase 4bl-D branch script. The v002 raw manifest remains
  `research_eligible = false` / `eligibility_gate_status =
  "pending"` (locked invariants for raw families per Phase 4bb-E);
  no manifest field is mutated by Phase 4bl-D or by this merge.
  No retained verdict is revised. No project lock is loosened.
  No successor phase is authorized. Remediation of the CRLF
  terminator (mutating a pre-existing Phase 4az fixture artefact)
  is out of scope; it requires a separately authorized governance
  memo.

## 7. Local gitignored outputs

Phase 4bl-D produced the following local artefacts under
`data/microstructure/` (all gitignored under `.gitignore:85`, none
committed; recomputed via `sha256` after the merge and bit-for-bit
match the values embedded in the Phase 4bl-D implementation report
and closeout):

### Phase 4bl-D gate report + sidecar (added by Phase 4bl-D)

- `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a.json`
  - SHA256: `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7`
  - Size: 169,637 bytes
  - `overall_status: "fail"`
  - `checks_total: 33`, `passed: 29`, `failed: 4`, `error: 0`,
    `not_applicable: 0`
  - `research_eligible_after: false`
  - `eligibility_gate_status_after: "fail_report_level_only"`
    (report-level only; the on-disk v002 manifest's
    `eligibility_gate_status` remains `"pending"`)
  - `no_successor_authorization: true`
  - `strict_fail_closed: true`
  - `manifest_mutated: false`, `manifest_transition_performed: false`
  - `created_at_unix_ms: 1778627360966`
  - `created_at_utc: "2026-05-12T23:09:20.966000Z"`
  - `run_wall_clock_seconds: 880.188` (~14.67 minutes)
  - `code_commit_sha: 2576a004c18a76e939303e794317d346c75303d2`
  - Records the four failed critical-severity checks verbatim:
    1. `raw_zip_sidecar_integrity` — 1 sidecar format failure on
       `2025-01-15`; 0 SHA mismatches.
    2. `per_file_row_count_consistency` — `2025-01-15` recomputed
       `row_count = None` vs manifest `1,681,098`.
    3. `per_file_time_bounds_consistency` — `2025-01-15` recomputed
       `first_trade_time_ms` / `last_trade_time_ms` /
       `min_agg_trade_id` / `max_agg_trade_id` all `None` (because
       per-row iteration was skipped after the sidecar failure).
    4. `total_row_count_consistency` — `recomputed_total_row_count
       = 153,472,351` vs `manifest_total_row_count = 155,153,449`;
       shortfall exactly equals the Phase 4az 2025-01-15 row count
       of `1,681,098`.
  - All other 29 checks PASS, including:
    - `all_rows_validated_count = 153,472,351` for the 89 dates
      that ran.
    - `all_schema_validation_errors_count = 0`.
    - `all_timestamp_boundary_errors_count = 0`.
    - `all_duplicate_agg_trade_id_errors_count = 0`.
    - `all_monotonicity_errors_count = 0`.
    - `adjacent_date_overlap_errors_count = 0`.
    - `recomputed_total_size_bytes = 1,943,823,208` matches
      manifest and Phase 4bl-C expected exactly.
    - `existing_fixture_preservation_zip_sha = pass` (2025-01-15
      zip SHA matches the Phase 4az recorded value exactly).
  - **NOT committed.** `git check-ignore -v` returns
    `.gitignore:85: data/microstructure/`.

- `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a.json.sha256`
  - SHA256 (of sidecar file): `b201dcd977ea2ef370b502f3840d90d6efd28b10354ca30eafcf155838c7a9c6`
  - Size: 153 bytes
  - Body: canonical Phase 4bb-F two-space `<sha>  <basename>\n`
    format (two spaces between hash and basename; one trailing LF);
    parsed hash matches the gate-report SHA bit-for-bit.
  - **NOT committed.** `git check-ignore -v` returns
    `.gitignore:85: data/microstructure/`.

### v002 multi-day raw manifest + sidecar (unchanged; Phase 4bl-C)

- `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json`
  - SHA256: `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485`
    (matches Phase 4bl-C recorded value bit-for-bit)
  - Size: 105,052 bytes
  - `research_eligible: false` (locked; unchanged by Phase 4bl-D)
  - `eligibility_gate_status: "pending"` (locked; unchanged)
  - `per_file_inventory` length: 90 (unchanged)
  - **NOT committed.**

### v002 acquisition log + sidecar (unchanged; Phase 4bl-C)

- `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json`
  - SHA256: `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314`
    (matches Phase 4bl-C recorded value bit-for-bit)
  - Size: 302,055 bytes
  - **NOT committed.**

### Phase 4az fixture (unchanged in zip; sidecar CRLF preserved verbatim)

- `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip`
  - SHA256: `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`
  - Size: 21,271,119 bytes
  - **Byte-identical pre/post Phase 4bl-D.**
  - The zip itself is uncorrupted; only the paired sidecar's line
    terminator differs from canonical Phase 4bb-F.

- `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256`
  - Size: 100 bytes (CRLF terminator).
  - Phase 4bl-D **did not** normalize this sidecar to canonical LF.
  - The sidecar is preserved verbatim as a finding, not a fix.
  - Any future remediation requires a separately authorized
    governance memo.

## 8. Validation results

- `git diff --check` (post-merge, pre-merge-closeout-commit): clean.
- `git status` (post-merge, pre-merge-closeout-commit): `On branch
  main`; `Your branch is ahead of 'origin/main' by 1 commit`; no
  staged changes; only the pre-existing untracked entries
  (`.claude/scheduled_tasks.lock`, `data/research/`). No
  `data/microstructure/` artefact staged or tracked.
- `git log --oneline -5 --decorate` (post-merge,
  pre-merge-closeout-commit):
  ```
  093c42c (HEAD -> main) docs(phase-4bl-d): merge multi-day raw manifest eligibility gate (FAIL)
  5092a39 (phase-4bl-d/multi-day-raw-manifest-eligibility-gate) docs(phase-4bl-d): multi-day raw manifest eligibility gate (FAIL)
  2576a00 (origin/main, origin/HEAD) docs(phase-4bl-c): record final main SHA in merge closeout
  2ec0a9a docs(phase-4bl-c): add merge closeout
  691e68c docs(phase-4bl-c): merge multi-day aggtrades acquisition execution
  ```
- `python -m py_compile scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py`
  → OK.
- `python -m py_compile tests/research/microstructure/test_phase4bl_d_raw_gate.py`
  → OK.
- `uv run ruff check scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py tests/research/microstructure/test_phase4bl_d_raw_gate.py`
  → `All checks passed!`
- `uv run pytest tests/research/microstructure/test_phase4bl_d_raw_gate.py`
  → **41 passed in 1.37s**.
- `git check-ignore -v data/microstructure/`
  → `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/gate-reports/raw/`
  → `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a.json`
  → `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a.json.sha256`
  → `.gitignore:85: data/microstructure/`.
- Recomputed Phase 4bl-D gate-report SHA256 (chunked hash, 1 MiB
  buffer): `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7`
  — matches the recorded value bit-for-bit.
- Recomputed Phase 4bl-D gate-report sidecar SHA256:
  `b201dcd977ea2ef370b502f3840d90d6efd28b10354ca30eafcf155838c7a9c6`
  — matches the recorded value bit-for-bit. The sidecar body is in
  canonical Phase 4bb-F two-space `<sha>  <basename>\n` format; the
  parsed hash matches the gate-report SHA bit-for-bit.
- Recomputed v002 manifest SHA256:
  `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485`
  — matches the recorded Phase 4bl-C value bit-for-bit (manifest
  unchanged by Phase 4bl-D).
- Recomputed v002 acquisition log SHA256:
  `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314`
  — matches the recorded Phase 4bl-C value bit-for-bit (log
  unchanged by Phase 4bl-D).
- Recomputed Phase 4az 2025-01-15 raw zip SHA256:
  `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`
  — matches the recorded Phase 4az fixture value bit-for-bit
  (byte-identical pre/post Phase 4bl-D).
- The Phase 4bl-D gate script was **NOT** rerun during the merge
  phase. No `data.binance.vision` call was made during the merge.
  No public endpoint was called. No Binance API was used. No
  WebSocket was opened. No credential was created or read. No
  `.env` was created or modified. No `.mcp.json` was created or
  modified. No MCP / Graphify was enabled.
- Whole-repo `ruff` / `mypy` / whole-repo `pytest` were **not**
  rerun during the merge phase, because Phase 4bl-D does not
  modify any prior source module — it only adds one new standalone
  script and one new offline test file. The latest authoritative
  whole-repo validation remains the Phase 4bb-F-implementation
  merge baseline (`ruff check .` PASS, `mypy` strict 120 source
  files PASS, `pytest tests/research/microstructure/` 915 passed
  + 1 pre-existing labelled skip, whole-repo `pytest` 1698 passed
  + 1 skipped + 2 pre-existing simulation failures).

## 9. Upstream immutability evidence

The following existing local gitignored artefacts must remain
byte-identical pre/post Phase 4bl-D. All values verified via
chunked SHA256 recomputation after the merge:

| Artefact | SHA256 | Pre/post |
| --- | --- | --- |
| Phase 4az raw zip (`BTCUSDT-aggTrades-2025-01-15.zip`) | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | IDENTICAL |
| Phase 4az raw `__v001` manifest | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` | IDENTICAL |
| Phase 4bb-D raw gate report | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` | IDENTICAL |
| Phase 4bd normalized parquet | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` | IDENTICAL |
| Phase 4bd derived manifest | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` | IDENTICAL |
| Phase 4bf derived-family gate report | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` | IDENTICAL |
| Phase 4bg-B derived-family successor-state | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` | IDENTICAL |
| Phase 4bh feature parquet | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` | IDENTICAL |
| Phase 4bh feature manifest | `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718` | IDENTICAL |
| Phase 4bi-B feature-family gate report | `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988` | IDENTICAL |
| Phase 4bi-D feature-family successor-state | `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a` | IDENTICAL |
| Phase 4bj-C label parquet | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` | IDENTICAL |
| Phase 4bj-C label manifest | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` | IDENTICAL |
| Phase 4bj-E label-family gate report | `b0b5405b94b916c2ce182f63b414b83887e4abddf422f18ae36d0bdc7273ead0` | IDENTICAL |
| Phase 4bj-G label-family successor-state | `ce7d391756ef347568374a9ee71e2cfaaa14d4f90ded969ab5771abe3fed2ea5` | IDENTICAL |
| Phase 4bj-J no-split-determination JSON | `7e461eb5508affa9ecd8f9a8127a5528082567a9b7492dd94648002ed37c4fa6` | IDENTICAL |
| Phase 4bb-G raw-family successor-state | `ab6a82e7d2e7aebd2e88986975390e7f2364dd32364b8ea9f0f169ee403ab452` | IDENTICAL |
| Phase 4bl-C v002 raw manifest | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | IDENTICAL |
| Phase 4bl-C v002 acquisition log | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | IDENTICAL |

All paired `.sha256` sidecars for each artefact also remain
byte-identical pre/post Phase 4bl-D, including the Phase 4az
2025-01-15 sidecar — Phase 4bl-D **did not** normalize the CRLF
terminator; it recorded the deviation as a finding only. The
Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant is preserved (never invoked by Phase 4bl-D
or by the merge).

## 10. Manifest state preservation

- Phase 4az `__v001` raw manifest `research_eligible: false`,
  `eligibility_gate_status: "pending"`: preserved.
- Phase 4bd derived manifest `research_eligible: false`,
  `eligibility_gate_status: "pending"`: preserved.
- Phase 4bh feature manifest `research_eligible: false`,
  `eligibility_gate_status: "pending"`: preserved.
- Phase 4bj-C label manifest `research_eligible: false`,
  `eligibility_gate_status: "pending"`,
  `chronological_split_policy: "not_yet_defined"`: preserved.
- **Phase 4bl-C v002 multi-day raw manifest** `research_eligible:
  false`, `eligibility_gate_status: "pending"` (locked invariants
  for raw families per Phase 4bb-E): preserved.

Phase 4bl-D does **NOT** flip `research_eligible` on any manifest.
Phase 4bl-D does **NOT** transition `eligibility_gate_status` on
any manifest (the gate-report-level
`eligibility_gate_status_after = "fail_report_level_only"` is a
report recommendation only; it is not applied to the on-disk v002
manifest). Phase 4bl-D does **NOT** change
`chronological_split_policy` on any manifest. The label manifest's
`chronological_split_policy` remains `"not_yet_defined"`. The
Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant is preserved (never invoked).

## 11. Boundary confirmations (all true)

- `no_gate_rerun_during_merge`: true (the Phase 4bl-D gate script
  was not invoked during the merge phase).
- `no_acquisition_during_merge`: true.
- `no_authenticated_api_usage`: true.
- `no_private_endpoint_usage`: true.
- `no_public_endpoint_call_in_code_during_merge`: true.
- `no_user_stream_or_websocket_usage`: true.
- `no_listenkey_usage`: true.
- `no_credential_creation_or_read`: true (no `.env`, no API key,
  no signed request).
- `no_mcp_file_modification`: true.
- `no_mcp_or_graphify_enabled`: true.
- `no_data_microstructure_modification`: true (every `data/
  microstructure/...` artefact is byte-identical pre/post,
  including the v002 manifest, sidecars, acquisition log, raw
  zips, and the existing Phase 4az 2025-01-15 fixture and its
  CRLF sidecar; the only new artefacts under
  `data/microstructure/` are the Phase 4bl-D gate-report JSON and
  its paired `.sha256` sidecar under the gitignored
  `gate-reports/raw/` namespace, produced by the Phase 4bl-D
  branch gate execution).
- `no_data_microstructure_commit`: true (every `data/
  microstructure/...` artefact remains gitignored under
  `.gitignore:85`; no path entered the diff or the staging area).
- `no_sidecar_normalization`: true (the Phase 4az 2025-01-15
  CRLF sidecar is preserved verbatim; Phase 4bl-D recorded the
  deviation as a finding, not a fix).
- `no_existing_raw_zip_modification`: true.
- `no_existing_manifest_modification`: true.
- `no_existing_sidecar_modification`: true (including the
  CRLF-terminator sidecar).
- `no_existing_gate_report_modification`: true.
- `no_existing_successor_state_modification`: true.
- `no_source_code_modification`: true (no prior `src/`, `tests/`,
  or `scripts/` file modified; the branch adds two new files only).
- `no_test_modification`: true (no prior test modified).
- `no_script_modification`: true (no prior `scripts/...` modified;
  one new `scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py`
  added).
- `no_pyproject_modification`: true.
- `no_readme_modification`: true.
- `no_gitignore_modification`: true.
- `no_gitattributes_modification`: true.
- `no_governance_memo_modification_beyond_narrow_current_project_state_update`:
  true (only `docs/00-meta/current-project-state.md` was modified
  within governance scope, narrowly per the documented standard).
- `no_normalization_run`: true.
- `no_derivation_run`: true.
- `no_feature_computation`: true.
- `no_label_computation`: true.
- `no_derived_or_feature_or_label_gate_run`: true (only the
  Phase 4bl-D raw gate was executed by the branch; the merge
  itself ran no gate).
- `no_new_successor_state_created`: true.
- `no_diagnostic_executed`: true.
- `no_label_statistic_computed`: true.
- `no_ml_training_or_architecture`: true.
- `no_feature_ranking_or_meta_labeling`: true.
- `no_strategy_created`: true.
- `no_signal_computed`: true.
- `no_backtest_run`: true.
- `no_pnl_mfe_mae_r_multiple_equity_position_alpha_edge_prediction_modelscore_decisionscore_entryexit_strategyoutput`:
  true.
- `no_research_eligible_flip`: true.
- `no_eligibility_gate_status_transition_on_any_actual_manifest`:
  true (the gate-report-level
  `eligibility_gate_status_after = "fail_report_level_only"`
  recommendation does not transition the on-disk v002 manifest).
- `no_chronological_split_policy_change`: true.
- `no_project_lock_modification`: true.
- `no_retained_verdict_revision`: true.
- `no_m0_amendment`: true.
- `no_post_null_cooldown_modification`: true.
- `no_cooled_down_families_list_modification`: true.
- `no_phase_4al_no_rescue_rule_modification`: true.
- `no_phase_4bb_f_canonical_path_policy_modification`: true (the
  CRLF deviation is recorded as a finding; the canonical policy
  is preserved verbatim).
- `no_phase_4aw_flip_research_eligible_invariant_modification`:
  true (the method was not invoked).
- `no_sidecar_remediation_authorization`: true.
- `no_phase_4bb_f_amendment_authorization`: true.
- `no_gate_amendment_authorization`: true.
- `no_phase_4bl_e_authorization`: true.
- `no_phase_4bm_*_authorization`: true.
- `no_phase_4bn_*_authorization`: true.
- `no_phase_4bo_*_authorization`: true.
- `no_phase_4bp_*_authorization`: true.
- `no_phase_4bq_*_authorization`: true.
- `no_phase_5_authorization`: true.
- `no_phase_4_canonical_authorization`: true.
- `no_paper_shadow_authorization`: true.
- `no_live_readiness_authorization`: true.
- `no_exchange_write_authorization`: true.
- `no_production_key_creation_or_request`: true.
- `no_additional_acquisition_beyond_locked_90_dates`: true.
- `no_alt_symbol_acquisition`: true.
- `no_5m_1m_tick_or_mark_price_acquisition_authorized`: true.

## 12. Retained verdict ledger (preserved verbatim)

- **H0** — FRAMEWORK ANCHOR (Phase 2i §1.7.3). Preserved verbatim.
- **R3** — BASELINE-OF-RECORD (Phase 2p §C.1). Preserved verbatim.
- **R1a** — RETAINED — NON-LEADING (Phase 2m). Preserved verbatim.
- **R1b-narrow** — RETAINED — NON-LEADING (Phase 2s). Preserved
  verbatim.
- **R2** — FAILED — §11.6 cost-sensitivity blocks (Phase 2w §16.1).
  Preserved verbatim.
- **F1** — HARD REJECT (Phase 3c §7.3 catastrophic-floor predicate;
  Phase 3d-B2 terminal). Preserved verbatim.
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL — other (Phase 3h
  §11.2; Phase 3j terminal). Preserved verbatim.
- **5m thread** — OPERATIONALLY CLOSED (Phase 3t). Preserved
  verbatim.
- **V2** — HARD REJECT — terminal for V2 first-spec (Phase 4l,
  structural CFP-1 critical). Preserved verbatim.
- **G1** — HARD REJECT — terminal for G1 first-spec (Phase 4r,
  CFP-1 critical binding; CFP-9 independent). Preserved verbatim.
- **C1** — HARD REJECT — terminal for C1 first-spec (Phase 4x,
  CFP-2 binding; CFP-3 / CFP-6 co-binding). Preserved verbatim.

All preserved verbatim. No retained verdict is revised by Phase
4bl-D or by this merge.

## 13. Preserved project locks (verbatim)

- **§11.6 cost lock** — HIGH cost = 8 bps slippage per side;
  round-trip = 16 bps slippage. Preserved verbatim.
- **§1.7.3 project-level locks** — 0.25% risk per trade; 2×
  leverage cap; one position max; mark-price stops. Preserved
  verbatim.
- **Phase 3p §4.7 strict integrity gate** — preserved verbatim
  (multi-day extension applied verbatim by Phase 4bl-D gate
  design).
- **Phase 3r §8 mark-price gap governance** — preserved verbatim.
- **Phase 3v §8 stop-trigger-domain governance** — preserved
  verbatim.
- **Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
  governance** — preserved verbatim.
- **Phase 4j §11 metrics OI-subset partial-eligibility rule** —
  preserved verbatim.
- **Phase 4k V2 backtest-plan methodology** — preserved verbatim.
- **Phase 4p G1 strategy-spec memo** — preserved verbatim.
- **Phase 4q G1 backtest-plan methodology** — preserved verbatim.
- **Phase 4v C1 strategy-spec memo** — preserved verbatim.
- **Phase 4w C1 backtest-plan methodology** — preserved verbatim.
- **Phase 4ak M0 mechanism-admissibility twelve-clause gate** —
  preserved verbatim.
- **Phase 4ak post-null cooldown rule** — preserved verbatim.
- **Phase 4ak cooled-down families list** — preserved verbatim.
- **Phase 4ak future M0 memo template** — preserved verbatim.
- **Phase 4al refined no-rescue rule + §13 boundary + §14
  hierarchy** — preserved verbatim.
- **Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant** — preserved verbatim (not invoked).
- **Phase 4bb-F canonical path policy** — preserved verbatim
  (Phase 4bl-D follows it for the gate-report filename and
  identified one pre-existing Phase 4az fixture sidecar that does
  not conform; the deviation is recorded as a finding, not an
  amendment).

All prior phase results preserved verbatim.

## 14. No-rescue constraints

The Phase 4bl-D merge does not, and cannot, be construed as
authorising:

- sidecar normalization (mutating the Phase 4az 2025-01-15 CRLF
  sidecar to canonical LF);
- amendment of the Phase 4bb-F canonical sidecar format to
  grandfather the CRLF terminator;
- amendment of the Phase 4bl-D gate script to accept CRLF as
  canonical-equivalent;
- rerunning the Phase 4bl-D gate;
- transitioning the v002 manifest's `eligibility_gate_status` to
  `"pass"` from this report-level FAIL evidence;
- ML model training, model selection, strategy hypothesis
  generation, or any conversion of acquired multi-day data into
  signals;
- strategy signal construction, strategy logic, position state,
  entry / exit rules, or backtest design;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation;
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL
  labels;
- mark-price / spot / cross-venue / order-book / additional
  aggTrades acquisition beyond the locked 90 BTCUSDT UTC dates;
- 5m / 1m / tick / mark-price 30m / 4h / order-book / spot /
  cross-venue / funding / open-interest data acquisition;
- old-strategy alt-symbol rerun or cooled-down-family reopening;
- 5m research-thread reopening (Phase 3t closure preserved);
- transitioning any manifest's `research_eligible` or
  `eligibility_gate_status` from this FAIL gate report alone;
- changing `chronological_split_policy` on any manifest from this
  evidence alone;
- re-tuning any of the six cooled-down failed strategy families
  (R2 / F1 / D1-A / V2 / G1 / C1) using the acquired multi-day
  data;
- re-fitting any threshold or filter that was previously fit on
  the one-day cell using the 90-day evidence base;
- re-evaluating any of the six failed strategies under
  cherry-picked sub-windows of the 90-day range;
- "rescuing" any failed hypothesis by appealing to the larger
  evidence base.

The Phase 4bl-D gate FAIL is recorded as **descriptive evidence
only**. The four failed checks share a single root cause (the
CRLF terminator); they do not constitute evidence of corrupted
data, missing data, or invalid acquisition. The Phase 4bl-C v002
acquisition itself remains intact: the zip at 2025-01-15 has the
expected byte-for-byte SHA `f560c2e5…`, and the other 89 dates
were fully validated per row with zero schema, timestamp,
duplicate, monotonicity, or boundary errors. The 90-day acquired
multi-day data is **forward research infrastructure only**;
new hypotheses, new ML feasibility studies, and new descriptive
diagnostics remain gated by the Phase 4ak M0 twelve-clause gate
on the forward path. The FAIL is not, by itself, evidence of any
strategy edge or research conclusion.

## 15. Successor authorization

**None.**

This merge-closeout records Phase 4bl-D as project-complete with
a FAIL gate verdict. It does **NOT** authorize any successor
phase. Specifically:

- **Sidecar remediation** (normalizing the Phase 4az 2025-01-15
  CRLF sidecar to canonical LF; amending Phase 4bb-F to
  grandfather CRLF; or amending the gate to accept CRLF as
  canonical-equivalent) is **NOT** authorized. Any such remedy
  mutates either a pre-existing fixture artefact or a governance
  contract and therefore requires a separately authorized
  governance memo.
- Phase 4bl-E (Multi-Day Raw Manifest Successor-State Recording)
  is **NOT** authorized and is not appropriate while the Phase
  4bl-D gate verdict is FAIL.
- Phase 4bm-* (Multi-Day Derived / Normalized Family arc) is
  **NOT** authorized.
- Phase 4bn-* (Multi-Day Feature arc) is **NOT** authorized.
- Phase 4bo-* (Multi-Day Label arc) is **NOT** authorized.
- Phase 4bp-* (Multi-Day Label Diagnostic arc) is **NOT**
  authorized.
- Phase 4bq-* (Multi-Day Chronological Split arc) is **NOT**
  authorized.
- Phase 5 / Phase 4 canonical is **NOT** authorized.
- ML feasibility memo, baseline ML diagnostic,
  failure-interpretation memo, strategy-hypothesis-under-M0 memo,
  strategy spec, backtest plan, backtest execution: **NOT**
  authorized.
- Paper / shadow operation: **NOT** authorized.
- Live-readiness, deployment, exchange-write, production-key
  creation, authenticated APIs, private endpoints, user stream,
  live WebSocket implementation, MCP, Graphify, `.mcp.json`,
  credentials: all **NOT** authorized.
- Additional aggTrades acquisition beyond the 90 locked BTCUSDT
  UTC dates: **NOT** authorized.
- 5m / 1m / tick / mark-price 30m / 4h / order-book / spot /
  cross-venue / funding / open-interest data acquisition: **NOT**
  authorized.

## 16. Recommended state

**Remain paused.**

Phase 4bl-D is now project-complete on `main` after this
merge-closeout commit. The gate FAIL verdict is recorded as
descriptive evidence only; no remediation is authorized by this
merge. No immediate follow-up action is required.

**Conditional next, NOT authorized:**

Future operator-authorized **docs-only sidecar-canonicalization
governance memo** is the cleanest non-paused option. It would
decide among three policy paths:

- (B1) Normalize the Phase 4az 2025-01-15 sidecar to canonical
  LF and re-run a future Phase 4bl-D-equivalent gate. This
  mutates a pre-existing Phase 4az fixture artefact.
- (B2) Amend the Phase 4bb-F canonical sidecar format to
  grandfather the Phase 4az fixture sidecar CRLF terminator.
  This mutates a governance contract.
- (B3) Amend the Phase 4bl-D gate (and any future raw-eligibility
  gate) to accept CRLF as canonical-equivalent. This mutates a
  gate contract.

Each of B1 / B2 / B3 mutates either a pre-existing artefact or a
governance / gate contract and therefore requires separate
operator authorization. Phase 4bl-D does not recommend any of the
three options; Phase 4bl-D's primary recommendation is **remain
paused**.

The natural conditional follow-on after sidecar canonicalization
(**Phase 4bl-E — Multi-Day Raw Manifest Successor-State
Recording**) remains **unauthorized** and is not appropriate while
the Phase 4bl-D gate verdict is FAIL. Phase 4bl-E would record a
sibling successor-state JSON marking the v002 raw manifest as
gate-passed (only after a future Phase 4bl-D-equivalent emits a
PASS), preserving the original v002 manifest byte-identically and
preserving `research_eligible = false` per Phase 4bb-E.

Paper / shadow, live-readiness, deployment, production keys,
authenticated APIs, private endpoints, public-endpoint calls in
code, user stream, WebSocket implementation, MCP, Graphify,
`.mcp.json`, credentials, exchange-write, and any additional
acquisition beyond the 90 locked BTCUSDT UTC dates **all remain
unauthorized**.

---

**End of Phase 4bl-D merge-closeout.**
