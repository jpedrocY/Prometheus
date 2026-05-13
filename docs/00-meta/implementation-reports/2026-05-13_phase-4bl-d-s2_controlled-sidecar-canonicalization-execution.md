# Phase 4bl-D-S2 — Controlled Sidecar Canonicalization Execution

## 1. Phase identity

- **Phase:** Phase 4bl-D-S2 — Controlled Sidecar Canonicalization
  Execution
- **Type:** docs + tiny standalone script + offline tests + one
  local gitignored sidecar mutation + one local gitignored
  canonicalization report (with paired SHA256 sidecar)
- **Branch:** `phase-4bl-d-s2/controlled-sidecar-canonicalization-execution`
- **Base commit (`main` / `origin/main` at branch creation):**
  `0d51bd7bac1eec1e11d7bad280e480dd8674a97f`
  (Phase 4bl-D-S1 merge-closeout commit
  `docs(phase-4bl-d-s1): add merge closeout`; in sync with
  `origin/main` at branch creation).
- **Script path:**
  `scripts/phase4bl_d_s2_canonicalize_sidecar.py` (Python standard
  library only; no network imports; no credential reads; no MCP /
  Graphify; no exchange adapters; no `prometheus.runtime` /
  `execution` / `persistence` imports).
- **Offline tests path:**
  `tests/research/microstructure/test_phase4bl_d_s2_sidecar_canonicalization.py`
  (28 offline tests; uses pytest `tmp_path`; static
  forbidden-import scan; static forbidden-runtime-token scan).
- **Local gitignored canonicalization report path:**
  `data/microstructure/canonicalization-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__1778713761225__0d51bd7bac1e.json`
- **Local gitignored canonicalization report sidecar path:**
  same path with `.sha256` suffix.

Phase 4bl-D-S2 is **controlled sidecar metadata canonicalization
only**. It performs **exactly one** mutation: it rewrites the
Phase 4az `BTCUSDT-aggTrades-2025-01-15.zip.sha256` sidecar from
Windows CRLF line terminator to canonical Phase 4bb-F LF. The
embedded SHA256 value, the embedded basename, the associated raw
zip bytes, the v002 raw manifest, the v002 acquisition log, and
the Phase 4bl-D gate report are preserved byte-identically.
Phase 4bl-D-S2 does **not** rerun the Phase 4bl-D gate, does
**not** create or modify any gate report, does **not** amend the
Phase 4bb-F canonical path policy, does **not** amend the Phase
4bl-D gate, does **not** create a successor-state artefact, and
does **not** authorize any successor phase.

## 2. Pre-state

### Phase 4bl-D gate verdict (preserved verbatim; descriptive
evidence only)

- Phase 4bl-D `overall_status`: **fail** (`RAW_MULTIDAY_GATE_FAIL`)
- 4 / 33 critical-severity checks failed; 29 / 33 passed.
- Single root cause: the Phase 4az 2025-01-15 sidecar at
  `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256`
  used Windows CRLF (`\r\n`) line terminator (100 bytes) instead
  of canonical Phase 4bb-F LF (`\n`) terminator (99 bytes for the
  same basename). The 2025-01-15 zip itself was byte-identical
  to the Phase 4az fixture (SHA
  `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`).
- Phase 4bl-D recorded the FAIL as descriptive evidence only and
  did not attempt remediation.

### Phase 4bl-D-S1 Option B1 recommendation (binding inputs)

Phase 4bl-D-S1 evaluated seven options (A, B1, B2, B3, C, D, E)
and recommended **Option B1 — normalize the Phase 4az 2025-01-15
sidecar from CRLF to canonical Phase 4bb-F LF** as the cleanest
practical remediation. The recommendation explicitly required
that any future Phase 4bl-D-S2 execution preserve:

- the raw zip byte-identically (SHA
  `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`);
- the embedded SHA256 value byte-identically;
- the embedded basename byte-identically;
- the v002 raw manifest byte-identically (SHA
  `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485`);
- the v002 acquisition log byte-identically (SHA
  `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314`);
- the Phase 4bl-D gate report byte-identically (SHA
  `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7`).

Phase 4bl-D-S1 also predeclared that:

- the sidecar size must transition from 100 to 99 bytes
  (byte delta `-1`);
- the line terminator must transition from CRLF to LF;
- the mutation type is
  `metadata_sidecar_line_ending_canonicalization`;
- no v002 manifest field may be mutated;
- the Phase 4bl-D gate may **not** be rerun by Phase 4bl-D-S2;
- no Phase 4bl-D-R authorization flows from Phase 4bl-D-S2 alone;
- no Phase 4bl-E authorization flows from Phase 4bl-D-S2 alone;
- the Phase 4bb-F canonical path policy is **not** amended by
  Phase 4bl-D-S2;
- the Phase 4bl-D gate is **not** amended by Phase 4bl-D-S2.

### Pre-state SHA snapshot (measured at branch creation)

| Artefact | Path | Size (bytes) | SHA256 |
| --- | --- | ---: | --- |
| target sidecar | `data/microstructure/raw/.../BTCUSDT-aggTrades-2025-01-15.zip.sha256` | 100 | `b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d` |
| associated raw zip | `data/microstructure/raw/.../BTCUSDT-aggTrades-2025-01-15.zip` | 21,271,119 | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| v002 raw manifest | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json` | 105,052 | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` |
| v002 acquisition log | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json` | 302,055 | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` |
| Phase 4bl-D gate report | `data/microstructure/gate-reports/raw/.../microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a.json` | 169,637 | `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7` |

Target sidecar pre-body (escaped):

```text
'f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e  BTCUSDT-aggTrades-2025-01-15.zip\r\n'
```

Embedded SHA = `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`
(matches associated raw zip SHA exactly).
Embedded basename = `BTCUSDT-aggTrades-2025-01-15.zip` (matches
expected exactly).
Line terminator = CRLF (two bytes; one `\r` + one `\n`).

## 3. Execution summary

### Mechanism

Phase 4bl-D-S2 ran the standalone script
`scripts/phase4bl_d_s2_canonicalize_sidecar.py` exactly once.
The script is hard-coded to:

- one target sidecar path (refused otherwise);
- one expected embedded SHA;
- one expected basename;
- one expected raw zip SHA + size;
- one expected v002 manifest SHA;
- one expected v002 acquisition log SHA;
- one expected Phase 4bl-D gate report SHA;
- one pre-size (100) → post-size (99) byte-delta of `-1`;
- one CRLF → LF terminator transition;
- one canonicalization-reports root prefix
  (`data/microstructure/canonicalization-reports/raw`);
- one mutation type label
  (`metadata_sidecar_line_ending_canonicalization`).

Atomic write: the script wrote the new 99-byte body to a tempfile
in the target's parent directory (`tempfile.mkstemp` with the
target basename + `.tmp.` prefix), flushed, `os.fsync`'d, and
then `os.replace`'d the tempfile into place. The tempfile and
the target are on the same filesystem, so the rename is atomic.

Precondition checks (all PASS): target sidecar exists; size is
100 bytes; line terminator is CRLF; embedded SHA equals
`f560c2e5...`; embedded basename equals
`BTCUSDT-aggTrades-2025-01-15.zip`; raw zip size is 21,271,119;
raw zip SHA matches; v002 manifest SHA matches; v002 acquisition
log SHA matches; Phase 4bl-D gate report SHA matches.

Mutation: exactly one file rewritten:
`data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256`.

Postcondition checks (all PASS): target sidecar size is 99
bytes; line terminator is LF; embedded SHA unchanged; embedded
basename unchanged; raw zip / v002 manifest / v002 acquisition
log / Phase 4bl-D gate report SHA all unchanged; byte delta is
exactly `-1`.

### Post-state SHA snapshot (measured immediately after mutation)

| Artefact | Path | Size (bytes) | SHA256 |
| --- | --- | ---: | --- |
| target sidecar | `data/microstructure/raw/.../BTCUSDT-aggTrades-2025-01-15.zip.sha256` | 99 | `c40e6be60753a912063d9a5f5c1617ba31ec987c09121c50adab3ba0226018fc` |
| associated raw zip | `data/microstructure/raw/.../BTCUSDT-aggTrades-2025-01-15.zip` | 21,271,119 | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` (unchanged) |
| v002 raw manifest | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json` | 105,052 | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` (unchanged) |
| v002 acquisition log | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json` | 302,055 | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` (unchanged) |
| Phase 4bl-D gate report | `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a.json` | 169,637 | `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7` (unchanged) |

Target sidecar post-body (escaped):

```text
'f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e  BTCUSDT-aggTrades-2025-01-15.zip\n'
```

Embedded SHA = `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`
(unchanged).
Embedded basename = `BTCUSDT-aggTrades-2025-01-15.zip` (unchanged).
Line terminator = LF (one byte; one `\n`).
Byte delta = `99 − 100 = −1`.

### Mutation accounting

- `byte_delta`: `-1`.
- `market_data_mutated`: `false` (raw zip bytes unchanged;
  measured by SHA256).
- `raw_zip_mutated`: `false`.
- `manifest_mutated`: `false` (v002 raw manifest unchanged).
- `acquisition_log_mutated`: `false`.
- `gate_report_mutated`: `false` (Phase 4bl-D gate report
  unchanged).
- `other_sidecars_mutated`: `false`.
- `only_target_sidecar_mutated`: `true`.
- `phase_4bb_f_policy_amended`: `false` (Phase 4bb-F canonical
  path policy preserved verbatim).
- `phase_4bl_d_gate_amended`: `false`.
- `gate_rerun_performed`: `false` (no rerun; Phase 4bl-D-R is
  separately authorized only).
- `successor_authorized`: `false`.

### Why this is metadata canonicalization, not market-data mutation

The mutation changes only the **line terminator** of the sidecar
file. The hex SHA256 value embedded inside the sidecar is
identical pre/post and continues to match the SHA256 of the
associated raw zip. The raw zip bytes are untouched; the zip's
SHA256 is byte-identical pre/post. No row of aggTrade market
data has been modified, dropped, reordered, or recomputed. No
manifest field has been modified. No gate report field has been
modified. No successor-state JSON has been created or modified.

## 4. Canonicalization report inventory

### Local gitignored canonicalization report

- **Path:** `data/microstructure/canonicalization-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__1778713761225__0d51bd7bac1e.json`
- **Size:** 5,241 bytes
- **SHA256:** `8c6457b65a4a3413c7836aea391d6b2cbd82c5cbd6252c6239f7e948e20809d3`
- **Gitignored:** yes (`.gitignore:85: data/microstructure/`).
- **Committed:** no.
- **Schema:** `v001`.
- **Phase fields:** `phase = "Phase 4bl-D-S2"`,
  `phase_id = "4bl-D-S2"`,
  `artefact_type = "sidecar_canonicalization_report"`,
  `dataset_family = "microstructure_raw_aggtrades_v001"`,
  `dataset_version = "v002"`,
  `mutation_type = "metadata_sidecar_line_ending_canonicalization"`.

The report includes verbatim every required field from the Phase
4bl-D-S2 authorization prompt: identity, target paths, pre-state
SHAs and sizes, post-state SHAs and sizes, mutation summary,
execution metadata (`created_at_utc`, `created_at_unix_ms`,
`base_commit_sha`, `code_commit_sha`, `code_commit_sha_short`,
`script_path`, `report_path`, `report_sidecar_path`,
`python_version`, `platform_summary`), and 38 non-authorization
flags (all `false`). The JSON is serialized deterministically
with `sort_keys=True` and `indent=2` and ends with a single LF.

### Local gitignored canonicalization report sidecar

- **Path:** same as the report path with `.sha256` suffix.
- **Size:** 156 bytes
- **SHA256 (self):** `1361c8e02217280f892abd8f72ff6323efac5a33b0dbddf1d51dd37540e403c6`
- **Gitignored:** yes (`.gitignore:85: data/microstructure/`).
- **Committed:** no.
- **Body (canonical Phase 4bb-F format):**
  `8c6457b65a4a3413c7836aea391d6b2cbd82c5cbd6252c6239f7e948e20809d3  microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__1778713761225__0d51bd7bac1e.json\n`
  (two spaces between hash and basename; one trailing LF; no
  CRLF; no BOM; sidecar body recomputed SHA256 matches the JSON
  report SHA256 bit-for-bit).

## 5. Validation commands and results

### Pre-execution git state

- `git status --short` (working tree before any change beyond
  the new script + tests file additions): only the pre-existing
  untracked entries (`.claude/scheduled_tasks.lock`,
  `data/research/`) plus the two new files
  (`scripts/phase4bl_d_s2_canonicalize_sidecar.py`,
  `tests/research/microstructure/test_phase4bl_d_s2_sidecar_canonicalization.py`).
  No `data/microstructure/` file was staged.
- `git rev-parse main` = `0d51bd7bac1eec1e11d7bad280e480dd8674a97f`.
- `git rev-parse origin/main` = `0d51bd7bac1eec1e11d7bad280e480dd8674a97f`.
- `git rev-parse HEAD` (branch HEAD before tracked-docs commit)
  = `0d51bd7bac1eec1e11d7bad280e480dd8674a97f`.
- Branch is exactly 0 commits ahead of `main` at execution time;
  no `data/microstructure/` file is tracked anywhere on the
  branch.

### Compile / lint / test

- `python -m py_compile scripts/phase4bl_d_s2_canonicalize_sidecar.py`
  → OK.
- `python -m py_compile tests/research/microstructure/test_phase4bl_d_s2_sidecar_canonicalization.py`
  → OK.
- `uv run ruff check scripts/phase4bl_d_s2_canonicalize_sidecar.py tests/research/microstructure/test_phase4bl_d_s2_sidecar_canonicalization.py`
  → `All checks passed!` (after the one-time autofix to sort the
  script's import block).
- `uv run pytest tests/research/microstructure/test_phase4bl_d_s2_sidecar_canonicalization.py -v`
  → **28 passed in 0.21s** (0 failed; 0 errors).

The 28 offline tests cover: CRLF / LF / malformed sidecar
parsing; canonical body rendering at exactly 99 bytes with two
spaces and a single trailing LF; atomic write semantics; target
sidecar path discipline; canonicalization-report root path
discipline; happy-path preconditions; refusal when the sidecar
is already LF; refusal when the embedded SHA differs from
expected; refusal when the embedded basename differs (with
same-length wrong basename so the size check is bypassed and
the basename check fires); refusal when the raw zip SHA
differs; end-to-end `main()` invocation against a tmp-path fake
repo with all five expected constants monkeypatched to the
fake stub artefacts' SHAs; deterministic report-JSON
serialization; static forbidden-import scan covering
`requests`, `httpx`, `aiohttp`, `urllib3`, `urllib`,
`websockets`, `binance`, `dotenv`, `python_dotenv`, `socket`,
and dotted subnames; static forbidden-runtime-token scan
covering `API_KEY`, `secret(`, `signature(`, `listenKey`,
`userDataStream`, `/fapi/...` private endpoint paths,
`Graphify`, `os.environ`, `os.getenv`, and `getpass`.

### Execution (one-shot)

- `python scripts/phase4bl_d_s2_canonicalize_sidecar.py --base-commit-sha 0d51bd7bac1eec1e11d7bad280e480dd8674a97f --code-commit-sha 0d51bd7bac1eec1e11d7bad280e480dd8674a97f`
  → **`Phase 4bl-D-S2: controlled sidecar canonicalization SUCCESS`**.
- Script-emitted summary lines verbatim:
  - `target_sidecar: C:\Prometheus\data\microstructure\raw\microstructure_raw_aggtrades_v001\BTCUSDT\2025\01\BTCUSDT-aggTrades-2025-01-15.zip.sha256`
  - `pre:  size=100 sha=b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d line_ending=CRLF`
  - `post: size=99 sha=c40e6be60753a912063d9a5f5c1617ba31ec987c09121c50adab3ba0226018fc line_ending=LF`
  - `byte_delta: -1`
  - `embedded_sha unchanged: True`
  - `embedded_basename unchanged: True`
  - `raw_zip_sha unchanged: True`
  - `v002_manifest_sha unchanged: True`
  - `v002_acquisition_log_sha unchanged: True`
  - `phase_4bl_d_gate_report_sha unchanged: True`
  - `report_path: C:\Prometheus\data\microstructure\canonicalization-reports\raw\microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__1778713761225__0d51bd7bac1e.json`
  - `report_sha256: 8c6457b65a4a3413c7836aea391d6b2cbd82c5cbd6252c6239f7e948e20809d3`
  - `report_size_bytes: 5241`
  - `report_sidecar_path: C:\Prometheus\data\microstructure\canonicalization-reports\raw\microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__1778713761225__0d51bd7bac1e.json.sha256`
  - `report_sidecar_sha256: 1361c8e02217280f892abd8f72ff6323efac5a33b0dbddf1d51dd37540e403c6`
  - `report_sidecar_size_bytes: 156`

### Independent SHA256 recomputation

After execution, an independent Python recomputation of all
seven artefact SHA256s confirmed bit-for-bit:

```text
target_sidecar          : size=99,        sha256=c40e6be60753a912063d9a5f5c1617ba31ec987c09121c50adab3ba0226018fc
raw_zip                 : size=21271119,  sha256=f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e
v002_manifest           : size=105052,    sha256=016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485
v002_acquisition_log    : size=302055,    sha256=52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314
phase_4bl_d_gate_report : size=169637,    sha256=d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7
canon_report            : size=5241,      sha256=8c6457b65a4a3413c7836aea391d6b2cbd82c5cbd6252c6239f7e948e20809d3
canon_report_sidecar    : size=156,       sha256=1361c8e02217280f892abd8f72ff6323efac5a33b0dbddf1d51dd37540e403c6
```

Target sidecar post body, independently read back:
`b'f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e  BTCUSDT-aggTrades-2025-01-15.zip\n'`
(`ends LF only: True`).
Canonicalization report sidecar body, independently read back:
`b'8c6457b65a4a3413c7836aea391d6b2cbd82c5cbd6252c6239f7e948e20809d3  microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__1778713761225__0d51bd7bac1e.json\n'`
(`ends LF only: True`; `two spaces present: True`; exactly one
two-space separator).

### Gitignore confirmations

- `git check-ignore -v data/microstructure/` →
  `.gitignore:85: data/microstructure/	data/microstructure/`.
- `git check-ignore -v data/microstructure/canonicalization-reports/` →
  `.gitignore:85: data/microstructure/	data/microstructure/canonicalization-reports/`.
- `git check-ignore -v data/microstructure/canonicalization-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__1778713761225__0d51bd7bac1e.json` →
  `.gitignore:85: data/microstructure/	<...>`.
- `git check-ignore -v data/microstructure/canonicalization-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__1778713761225__0d51bd7bac1e.json.sha256` →
  `.gitignore:85: data/microstructure/	<...>`.

### Post-execution git state

- `git status --short`:
  ```text
  ?? .claude/scheduled_tasks.lock
  ?? data/research/
  ?? scripts/phase4bl_d_s2_canonicalize_sidecar.py
  ?? tests/research/microstructure/test_phase4bl_d_s2_sidecar_canonicalization.py
  ```
  Only the two new tracked files appear as untracked (to be
  staged with the Phase 4bl-D-S2 docs commit). No
  `data/microstructure/` file is staged. No `data/microstructure/`
  file is tracked anywhere on the branch.
- `git diff --check`: clean.

### Whole-repo validation not rerun

`uv run mypy src/prometheus` and whole-repo `uv run pytest` were
**not** rerun by Phase 4bl-D-S2. The script is standalone (no
`src/prometheus/` modification; no prior test modification; no
prior script modification), and the offline tests live alongside
existing `tests/research/microstructure/` tests but do not
import from or modify any prior test. The latest authoritative
whole-repo validation remains the Phase 4bb-F-implementation
merge baseline.

## 6. Boundary confirmations

The Phase 4bl-D-S2 execution honours every boundary required by
the authorization prompt and the Phase 4bk-A workflow standard:

- exactly one sidecar mutated
  (`BTCUSDT-aggTrades-2025-01-15.zip.sha256`; the script refuses
  to write any other sidecar path);
- no raw zip mutation (zip SHA256 byte-identical pre/post);
- no v002 raw manifest mutation;
- no v002 acquisition log mutation;
- no Phase 4bl-D gate report mutation;
- no other sidecar mutation (e.g. Phase 4az v001 manifest
  sidecar, Phase 4bl-C v002 manifest sidecar, Phase 4bl-D gate
  report sidecar — all untouched);
- no derived parquet, no normalized parquet, no feature parquet,
  no label parquet, no successor-state artefact, no diagnostic,
  no split artefact, no v003 created;
- no Phase 4bb-F canonical path policy amendment (the CRLF
  deviation was remediated under existing Phase 4bb-F policy, not
  by amending it);
- no Phase 4bl-D gate amendment;
- no Phase 4bl-D gate rerun;
- no new gate report created;
- no successor-state artefact created;
- no normalization, derivation, feature computation, label
  computation, diagnostics, label statistics, ML training,
  strategy implementation, signal computation, or backtest
  execution;
- no `research_eligible` flip on any actual manifest;
- no `eligibility_gate_status` transition on any actual
  manifest;
- no `chronological_split_policy` change on any actual
  manifest;
- Phase 4aw
  `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked);
- no data acquisition, no download, no public endpoint call, no
  Binance API call, no authenticated REST, no private endpoint,
  no WebSocket, no user stream, no listenKey lifecycle;
- no credential, no `.env`, no `.mcp.json`, no MCP, no Graphify;
- no `data/microstructure/` artefact committed (the canonicalized
  sidecar, the canonicalization report JSON, and the report
  `.sha256` sidecar all live under the existing
  `.gitignore:85: data/microstructure/` rule; verified via
  `git check-ignore -v`).

## 7. Retained verdict ledger (preserved verbatim)

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED (Phase 3t)
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

## 8. Project locks (preserved verbatim)

- §11.6 = 8 bps per side; round-trip = 16 bps;
- §1.7.3 = 0.25% risk per trade / 2× leverage cap /
  one-position max / mark-price stops;
- Phase 3p §4.7 strict integrity gate;
- Phase 3r §8 mark-price gap governance;
- Phase 3v §8 stop-trigger-domain governance;
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
  governance;
- Phase 4j §11 metrics OI-subset partial-eligibility rule;
- Phase 4k V2 backtest-plan methodology;
- Phase 4p G1 strategy-spec memo;
- Phase 4q G1 backtest-plan methodology;
- Phase 4v C1 strategy-spec memo;
- Phase 4w C1 backtest-plan methodology;
- Phase 4ak M0 twelve-clause mechanism-admissibility gate +
  post-null cooldown rule + cooled-down families list + memo
  template;
- Phase 4al refined no-rescue rule + §13 boundary + §14
  hierarchy;
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant;
- Phase 4bb-F canonical path policy.

All prior phase results preserved verbatim.

## 9. No-rescue constraints

Phase 4bl-D-S2 does **not**, and cannot be construed as
authorising:

- the Phase 4bl-D-R multi-day raw gate rerun;
- the Phase 4bl-E multi-day raw successor-state recording;
- the Phase 4bm-* multi-day derived arc;
- the Phase 4bn-* multi-day feature arc;
- the Phase 4bo-* multi-day label arc;
- the Phase 4bp-* multi-day diagnostics;
- the Phase 4bq-* multi-day chronological split;
- Phase 5;
- Phase 4 canonical;
- successor-state recording for any family;
- `research_eligible` flip / `eligibility_gate_status`
  transition / `chronological_split_policy` change on any actual
  manifest;
- normalization, derived parquet, features, labels, diagnostics,
  label statistics, ML, strategy, signals, or backtests;
- additional aggTrades / 5m / 1m / tick / mark-price 30m / 4h /
  order-book / spot / cross-venue / funding / open-interest data
  acquisition;
- paper / shadow / live-readiness / deployment / exchange-write
  / production-key creation / authenticated APIs / private
  endpoints / public-endpoint calls in code / user stream / live
  WebSocket implementation / MCP / Graphify / `.mcp.json` /
  credentials;
- amendment of the Phase 4bb-F canonical path policy;
- amendment of the Phase 4bl-D gate;
- old-strategy alt-symbol rerun or cooled-down-family reopening
  (R2 / F1 / D1-A / V2 / G1 / C1 first-spec rejections remain
  terminal; the 5m research thread remains operationally closed
  per Phase 3t).

## 10. Successor authorization

**None.**

The natural conditional successor chain implied by the Phase
4bl-D-S1 Option B1 recommendation (Phase 4bl-D-S2 → Phase
4bl-D-R → Phase 4bl-E) requires **two more** separately
authorized operator prompts and is **NOT** authorized by Phase
4bl-D-S2:

- **Phase 4bl-D-R — Multi-Day Raw Manifest Eligibility Gate
  Rerun** (NOT authorized): would re-run the Phase 4bl-D 33-check
  gate against the canonicalized sidecar set and the unchanged
  Phase 4bl-C raw fileset. PASS is likely but not guaranteed.
- **Phase 4bl-E — Multi-Day Raw Manifest Successor-State
  Recording** (NOT authorized): would record a sibling
  successor-state JSON only after Phase 4bl-D-R produces PASS.

## 11. Recommended state

**Remain paused** after Phase 4bl-D-S2 branch completion.

The Phase 4bl-D-S2 branch is complete. Per the Phase 4bk-A
workflow standard, Phase 4bl-D-S2 is **not project-complete**
until a separately authorized merge phase records its
merge-closeout on `main`. No remediation result (PASS or FAIL)
exists yet, and the Phase 4bl-D gate FAIL remains the
authoritative research-evidence record until a separately
authorized Phase 4bl-D-R rerun produces a new verdict.

**Conditional next, NOT authorized:** future operator-authorized
merge of this Phase 4bl-D-S2 branch into `main` with a Phase
4bl-D-S2 merge-closeout, then a separately authorized future
Phase 4bl-D-R Multi-Day Raw Manifest Eligibility Gate Rerun.
Phase 4bl-D-S2 does **not** authorize any of these.
