# Phase 4bl-C — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bl-C — Multi-Day aggTrades Acquisition Execution
- **Type:** docs + code + local gitignored raw acquisition output
- **Action:** merge into `main`
- **Merge purpose:** Bring Phase 4bl-C from branch-complete to
  project-complete status per the Phase 4bk-A workflow standard.
  Phase 4bl-C executed the Phase 4bl-B locked acquisition design and
  performed the project's first multi-day public-archive acquisition.
  It acquired the locked 90 contiguous UTC dates 2024-12-01 through
  2025-02-28 inclusive for BTCUSDT only, exclusively from public
  unauthenticated `data.binance.vision` daily aggTrades archives,
  under the Phase 4bl-B §14 strict integrity gate. The branch added
  one standalone orchestrator script
  (`scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py`,
  stdlib + Phase 4ax / 4aw scaffold only; no `prometheus.runtime /
  execution / persistence` imports; no `requests` / `httpx` /
  `aiohttp` / `urllib3` / `socket` / `websockets` / `binance` /
  `dotenv` imports; only `urllib.request` against the locked
  `data.binance.vision` allowlist; no credentials; no `.env`;
  no `.mcp.json`; no MCP / Graphify; no authenticated REST;
  no private endpoints; no public REST endpoints; no WebSocket;
  no `listenKey`); one offline test suite
  (`tests/research/microstructure/test_phase4bl_c_acquisition_script.py`;
  71 tests; all pass); the Phase 4bl-C implementation report; the
  Phase 4bl-C closeout; and one narrow `current-project-state.md`
  update. The acquisition produced 90 raw `.zip` files + 90 paired
  `.sha256` sidecars under the canonical Phase 4bb-F partition tree,
  plus one v002 multi-day raw manifest + sidecar and one v002
  acquisition log + sidecar — all under the gitignored
  `data/microstructure/` namespace and **none committed**. The
  existing Phase 4az `2025-01-15` one-day fixture was reused in place
  with three-way SHA agreement (recorded SHA ↔ fresh-local SHA ↔
  fresh `.CHECKSUM` companion SHA), byte-identical pre/post. No
  manifest is mutated; no successor phase is authorized; the v002
  raw manifest is `research_eligible=false` /
  `eligibility_gate_status="pending"` (locked invariants for raw
  families per Phase 4bb-E).
- **Target branch:** `main`
- **Source branch:** `phase-4bl-c/multi-day-aggtrades-acquisition-execution`

## 2. SHAs

- **`main` SHA before merge:** `da9d830c2b900c1c5fa09159e79ce2f0b6bbe249`
  (Phase 4bl-B SHA-chain-fixup commit on top of the Phase 4bl-B
  merge-closeout `31e907fcb2034a45257f6f2513fc5b51b48f5e8f`).
- **Phase 4bl-C branch commit SHA:** `04af6a1eb788c3c5d4cf0ca22abe7865ebc09888`
  (`docs(phase-4bl-c): multi-day aggtrades acquisition execution`).
- **Merge commit SHA:** `691e68c2a300264b62ef749fe9bf81f1dd71125b`.
- **Merge-closeout commit SHA:** (recorded immediately after this
  file is committed on `main`).
- **Final `main` / `origin/main` SHA after push:** the canonical
  project-complete anchor for Phase 4bl-C is the merge-closeout
  commit (this file). A one-commit SHA-chain-fixup on top of that
  anchor will record the final-`main` SHA value back into this §2,
  matching the Phase 4bb-G / Phase 4bb-F-implementation / Phase
  4bb-F / Phase 4bj-G / Phase 4bj-F / Phase 4bj-H / Phase 4bj-I /
  Phase 4bj-J / Phase 4bj-K / Phase 4bl-A / Phase 4bl-B
  SHA-chain-fixup precedents. The SHA-chain-fixup commit only
  records the final-`main` SHA value back into this §2; it does not
  change Phase 4bl-C lifecycle semantics.

## 3. Merge method

- Command: `git merge --no-ff phase-4bl-c/multi-day-aggtrades-acquisition-execution -m "docs(phase-4bl-c): merge multi-day aggtrades acquisition execution"`
- Strategy: `ort` (the default).
- Merge commit message: `docs(phase-4bl-c): merge multi-day aggtrades acquisition execution`.
- Push status: pushed to `origin/main` with no force, no skip-hooks,
  no skip-signing.

## 4. Files brought forward by the merge

### Docs (added)

- `docs/00-meta/implementation-reports/2026-05-12_phase-4bl-c_multi-day-aggtrades-acquisition-execution.md`
  (the Phase 4bl-C main implementation report, 8 sections, 593 lines).
- `docs/00-meta/implementation-reports/2026-05-12_phase-4bl-c_closeout.md`
  (the Phase 4bl-C closeout, 10 sections, 204 lines).

### Docs (modified narrowly)

- `docs/00-meta/current-project-state.md` (new Phase 4bl-C narrative
  paragraph prepended above the Phase 4bl-B paragraph; new "Current
  phase:" Phase 4bl-C block replacing the prior top "Current phase:"
  Phase 4bl-B block; prior Phase 4bl-B "Current phase:" block
  preserved as historical context immediately below the new block
  per the documented standard; +424 lines).

### Source (added)

- `scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py`
  (standalone Python orchestrator; stdlib + Phase 4ax / 4aw scaffold
  only; +1,957 lines).

### Tests (added)

- `tests/research/microstructure/test_phase4bl_c_acquisition_script.py`
  (71 offline tests; +747 lines).

### Config / data

- None modified. None added. None removed.
- No `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`,
  or MCP file change.
- **No `data/microstructure/` file modified.** No raw zip, no
  manifest, no sidecar, no acquisition log, no gate report, no
  successor-state, no normalized parquet, no feature parquet, no
  label parquet, no diagnostic artefact, no split artefact created
  or modified through the tracked diff. The Phase 4bl-C local
  acquisition output (90 raw zips + 90 sidecars + 1 v002 manifest +
  sidecar + 1 v002 acquisition log + sidecar) lives strictly under
  the gitignored `data/microstructure/` namespace and was produced
  by the Phase 4bl-C branch acquisition execution (not by the
  merge). See §7 for full path / SHA / size detail.
- No artefact under `data/raw/`, `data/normalized/`,
  `data/manifests/`, `data/derived/`, or any other project data
  path created or modified.

### Prior source / tests / scripts / governance memos

- None modified. The branch adds new files only; it does not edit
  any pre-existing source module, test, script, or governance memo
  (other than the narrow `current-project-state.md` paragraph
  addition and Current-phase block replacement). The Phase 4aw
  microstructure scaffold modules, the Phase 4ax aggTrades
  validator, and all prior source modules are unchanged.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              |  424 +++++
 .../2026-05-12_phase-4bl-c_closeout.md             |  204 ++
 ...-c_multi-day-aggtrades-acquisition-execution.md |  593 ++++++
 ...hase4bl_c_acquire_btcusdt_aggtrades_multiday.py | 1957 ++++++++++++++++++++
 .../test_phase4bl_c_acquisition_script.py          |  747 ++++++++
 5 files changed, 3925 insertions(+)
```

- 5 tracked files: 3,925 insertions, 0 deletions.
- No file deletions.
- No file renames.
- No file moves.
- No binary file changes.
- The diff matches the expected change set from the Phase 4bl-C
  authorization prompt exactly.

## 6. Result / verdict

- **Status:** SUCCESSFUL_MERGE.
- **Verdict:** LOCAL ARTEFACT PRODUCED — the Phase 4bl-C multi-day
  aggTrades acquisition execution is now part of the canonical
  project history on `main`. Phase 4bl-C is project-complete only
  after this merge-closeout commit is recorded on `main`. The 90
  raw zips + paired sidecars and the v002 multi-day manifest +
  log (with their paired sidecars) remain locally on disk under the
  gitignored `data/microstructure/` namespace; they are reproducible
  from the public `data.binance.vision` archive by re-running the
  orchestrator script with the Phase 4ax / 4aw scaffold and the
  existing one-day fixture in place. The v002 raw manifest is
  `research_eligible=false` / `eligibility_gate_status="pending"`
  (locked invariants for raw families per Phase 4bb-E). No retained
  verdict is revised. No project lock is loosened. No successor
  phase is authorized.

## 7. Local gitignored outputs

Phase 4bl-C produced the following local artefacts under
`data/microstructure/` (all gitignored under `.gitignore:85`, none
committed; recomputed via `sha256sum` after the merge and bit-for-bit
match the values embedded in the manifest, the manifest sidecar, the
acquisition log, and the log sidecar):

### v002 multi-day manifest + sidecar (added by Phase 4bl-C)

- `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json`
  - SHA256: `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485`
  - Size: 105,052 bytes
  - `research_eligible: false` (locked)
  - `eligibility_gate_status: "pending"` (locked)
  - `dataset_family: "microstructure_raw_aggtrades_v001"`,
    `dataset_version: "v002"`, `schema_version: "v001"`
  - `acquired_file_count: 90` / `expected_file_count: 90`
  - `missing_file_count: 0`, `checksum_mismatch_count: 0`,
    `decompression_failure_count: 0`
  - `total_size_bytes: 1,943,823,208`
  - `total_row_count: 155,153,449`
  - `per_file_inventory` length: 90 (all entries
    `status: "acquired_verified"`)
  - `base_commit_sha: dc2240e7a43047823c8b964d52112432b7a61c79`,
    `code_commit_sha: da9d830c2b900c1c5fa09159e79ce2f0b6bbe249`
  - `capture_config_hash: 168dc5aa49abbb1bc7a260fc8dfd2a8cdab4e881b90f645fe91a07be5a34f8a6`
  - `acquisition_log_sha256: 52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314`
    (cross-matches on-disk log file's recomputed SHA bit-for-bit)
  - `governance_labels`: `phase: 4bl-C`,
    `source_phase_boundary: 4bl-B`,
    `validator: phase_4ax_aggtrades_v001`,
    `stop_trigger_domain: trade_price_backtest_candidate`,
    `feature_computation: forbidden`,
    `labels: forbidden`,
    `ml: forbidden`,
    `strategy: forbidden`
  - **NOT committed.** `git check-ignore -v` returns
    `.gitignore:85: data/microstructure/`.

- `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json.sha256`
  - SHA256 (of sidecar file): `adaf97242cfbe922bc9e93a6699e547d1b02fa64a96dd2cdd08df1814ce25e26`
  - Size: 111 bytes
  - Body: canonical Phase 4bb-F two-space `<sha>  <basename>\n`
    format; parsed hash matches manifest SHA bit-for-bit.
  - **NOT committed.** `git check-ignore -v` returns
    `.gitignore:85: data/microstructure/`.

### v002 acquisition log + sidecar (added by Phase 4bl-C)

- `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json`
  - SHA256: `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314`
  - Size: 302,055 bytes
  - `overall_status: "SUCCESSFUL_ACQUISITION"` (top-level)
  - `wall_clock_seconds: 717` (top-level)
  - `acquisition_run_id: "phase-4bl-C-1778622616325-1080b925"`
  - `started_at_utc: "2026-05-12T21:50:16.325000+00:00"`
  - `finished_at_utc: "2026-05-12T22:02:13.858000+00:00"`
  - `errors` array length: 0
  - `events` array length: 629 (1 `run_started`, 1 `run_finished`,
    1 `date_skipped_existing_fixture`, 1 `existing_fixture_verified`,
    179 `download_attempt`, 179 `download_success`, 89
    `checksum_match`, 89 `finalisation_success`, 89 `sidecar_write`)
  - `summary.existing_fixture_reused: true`,
    `summary.existing_fixture_sha_match: true`,
    `summary.non_authorizations_preserved: true`,
    `summary.research_eligible_after_acquisition: false`,
    `summary.eligibility_gate_status_after_acquisition: "pending"`
  - **NOT committed.** `git check-ignore -v` returns
    `.gitignore:85: data/microstructure/`.

- `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json.sha256`
  - SHA256 (of sidecar file): `975bdc544152d1f84f6e700309aad89998e663cb779acc5883bd20652e428958`
  - Size: 127 bytes
  - Body: canonical Phase 4bb-F two-space `<sha>  <basename>\n`
    format; parsed hash matches log SHA bit-for-bit.
  - **NOT committed.** `git check-ignore -v` returns
    `.gitignore:85: data/microstructure/`.

### Raw aggTrades zips + paired sidecars (added by Phase 4bl-C, except the reused 2025-01-15 fixture)

- 90 raw `.zip` files under the canonical Phase 4bb-F partition tree:
  - `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2024/12/` — 31 zips (2024-12-01 .. 2024-12-31).
  - `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/` — 31 zips (2025-01-01 .. 2025-01-31; **the 2025-01-15 entry is the reused Phase 4az fixture**, byte-identical pre/post).
  - `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/02/` — 28 zips (2025-02-01 .. 2025-02-28).
- 90 paired `.sha256` sidecars in the same directories (one per zip;
  canonical Phase 4bb-F two-space format).
- Aggregate size: 1,943,823,208 bytes (~1.81 GiB) across the 90 zips.
- Aggregate aggTrade event count: 155,153,449 events.
- **None committed.** `git check-ignore -v` on representative
  paths (2024/12 first, 2025/02 last, 2025/01/15 fixture) returns
  `.gitignore:85: data/microstructure/`. The per-date SHA is
  recorded in the v002 manifest's `per_file_inventory[].sha256`
  field; the sidecar embeds the same SHA in canonical two-space
  `<sha>  <basename>\n` format.

### Existing Phase 4az fixture (preserved in place)

- `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip`
  - SHA256: `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`
  - Size: 21,271,119 bytes
  - Status: **reused in place; byte-identical pre/post Phase 4bl-C.**
  - Three-way agreement: recorded SHA ↔ fresh local-recomputation
    SHA ↔ fresh `.CHECKSUM` companion SHA — all three matched
    bit-for-bit.
  - Existing paired `.zip.sha256` sidecar preserved byte-identical
    (not opened for write by Phase 4bl-C).
  - The v002 manifest's `per_file_inventory` entry for `2025-01-15`
    records `status: "acquired_verified"`, `sha256: f560c2e5…`,
    `size_bytes: 21271119`, `row_count: 1681098`.

## 8. Validation results

- `git diff --check` (post-merge): clean.
- `git status` (post-merge, pre-merge-closeout-commit): `On branch
  main`; `Your branch is ahead of 'origin/main' by 1 commit`; no
  staged changes; only the pre-existing untracked entries
  (`.claude/scheduled_tasks.lock`, `data/research/`). No
  `data/microstructure/` artefact staged or tracked.
- `git log --oneline -6 --decorate` (post-merge,
  pre-merge-closeout-commit):
  ```
  691e68c (HEAD -> main) docs(phase-4bl-c): merge multi-day aggtrades acquisition execution
  04af6a1 (origin/phase-4bl-c/..., phase-4bl-c/...) docs(phase-4bl-c): multi-day aggtrades acquisition execution
  da9d830 (origin/main, origin/HEAD) docs(phase-4bl-b): record final main SHA in merge closeout
  31e907f docs(phase-4bl-b): add merge closeout
  1e9051e docs(phase-4bl-b): merge multi-day aggtrades acquisition design memo
  e5eb8ca docs(phase-4bl-b): multi-day aggtrades acquisition authorization / design memo
  ```
- `python -m py_compile scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py`
  → OK.
- `python -m py_compile tests/research/microstructure/test_phase4bl_c_acquisition_script.py`
  → OK.
- `uv run ruff check scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py tests/research/microstructure/test_phase4bl_c_acquisition_script.py`
  → `All checks passed!`
- `uv run pytest tests/research/microstructure/test_phase4bl_c_acquisition_script.py`
  → **71 passed in 0.36s**.
- `git check-ignore -v data/microstructure/`
  → `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json`
  → `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json.sha256`
  → `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json`
  → `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json.sha256`
  → `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2024/12/BTCUSDT-aggTrades-2024-12-01.zip`
  → `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip`
  → `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/02/BTCUSDT-aggTrades-2025-02-28.zip`
  → `.gitignore:85: data/microstructure/`.
- Recomputed v002 manifest SHA256 (`sha256sum`):
  `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485`
  — matches the recorded value bit-for-bit.
- Recomputed v002 manifest sidecar SHA256:
  `adaf97242cfbe922bc9e93a6699e547d1b02fa64a96dd2cdd08df1814ce25e26`
  — matches the recorded value bit-for-bit.
- Recomputed v002 acquisition log SHA256:
  `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314`
  — matches the recorded value bit-for-bit and matches the
  manifest's embedded `acquisition_log_sha256` field bit-for-bit.
- Recomputed v002 log sidecar SHA256:
  `975bdc544152d1f84f6e700309aad89998e663cb779acc5883bd20652e428958`
  — matches the recorded value bit-for-bit.
- Recomputed existing 2025-01-15 raw zip SHA256:
  `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`
  — matches the recorded Phase 4az fixture value bit-for-bit
  (byte-identical pre/post Phase 4bl-C).
- Raw zip count: `find data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/ -name '*.zip' | wc -l`
  → 90 zips.
- Raw sidecar count: `find data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/ -name '*.sha256' | wc -l`
  → 90 sidecars.
- The Phase 4bl-C acquisition script was **NOT** rerun during the
  merge phase. No `data.binance.vision` call was made during the
  merge. No public endpoint was called. No Binance API was used.
  No WebSocket was opened. No credential was created or read.
  No `.env` was created or modified. No `.mcp.json` was created or
  modified. No MCP / Graphify was enabled.
- Whole-repo `ruff` / `mypy` / whole-repo `pytest` were **not**
  rerun during the merge phase, because Phase 4bl-C does not modify
  any prior source module — it only adds one new standalone script
  and one new offline test file. The latest authoritative whole-repo
  validation remains the Phase 4bb-F-implementation merge baseline
  (`ruff check .` PASS, `mypy` strict 120 source files PASS,
  `pytest tests/research/microstructure/` 915 passed + 1 pre-existing
  labelled skip, whole-repo `pytest` 1698 passed + 1 skipped + 2
  pre-existing simulation failures).

## 9. Upstream immutability evidence

The following existing local gitignored artefacts must remain
byte-identical pre/post Phase 4bl-C. All values verified via
`sha256sum --check` after the merge:

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

All paired `.sha256` sidecars for each artefact also remain
byte-identical pre/post Phase 4bl-C. The Phase 4aw
`MicrostructureManifest.flip_research_eligible(...)` always-raises
invariant is preserved (never invoked by Phase 4bl-C or by the merge).

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
- **New v002 multi-day raw manifest** `research_eligible: false`,
  `eligibility_gate_status: "pending"` (locked invariants for raw
  families per Phase 4bb-E): set at acquisition time and never
  flipped.

Phase 4bl-C does **NOT** flip `research_eligible` on any manifest.
Phase 4bl-C does **NOT** transition `eligibility_gate_status` on any
manifest. Phase 4bl-C does **NOT** change `chronological_split_policy`
on any manifest. The label manifest's `chronological_split_policy`
remains `"not_yet_defined"`. The Phase 4aw
`MicrostructureManifest.flip_research_eligible(...)` always-raises
invariant is preserved (never invoked).

## 11. Boundary confirmations (all true)

- `no_acquisition_rerun_during_merge`: true (no `data.binance.vision`
  call, no public endpoint call, no Binance API call, no WebSocket,
  no orchestrator-script invocation during the merge phase).
- `no_authenticated_api_usage`: true.
- `no_private_endpoint_usage`: true.
- `no_public_endpoint_call_in_code_during_merge`: true.
- `no_user_stream_or_websocket_usage`: true.
- `no_listenkey_usage`: true.
- `no_credential_creation_or_read`: true (no `.env`, no API key, no
  signed request).
- `no_mcp_file_modification`: true.
- `no_mcp_or_graphify_enabled`: true.
- `no_data_microstructure_modification`: true (every `data/
  microstructure/...` artefact is byte-identical pre/post, including
  the new v002 manifest, sidecars, log, and the existing 2025-01-15
  fixture).
- `no_data_microstructure_commit`: true (every `data/
  microstructure/...` artefact remains gitignored under
  `.gitignore:85`; no path entered the diff or the staging area).
- `no_existing_raw_zip_modification`: true (the 2025-01-15 fixture
  has SHA `f560c2e5…` pre and post; the existing sidecar is
  preserved byte-identical).
- `no_existing_manifest_modification`: true.
- `no_existing_sidecar_modification`: true.
- `no_existing_gate_report_modification`: true.
- `no_existing_successor_state_modification`: true.
- `no_source_code_modification`: true (no prior `src/`,
  `tests/`, or `scripts/` file modified; the branch adds two new
  files only).
- `no_test_modification`: true (no prior test modified).
- `no_script_modification`: true (no prior `scripts/...` modified;
  one new `scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py`
  added).
- `no_pyproject_modification`: true.
- `no_readme_modification`: true.
- `no_gitignore_modification`: true.
- `no_gitattributes_modification`: true.
- `no_governance_memo_modification_beyond_narrow_current_project_state_update`:
  true (only `docs/00-meta/current-project-state.md` was modified
  within governance scope, narrowly per the documented standard).
- `no_normalization_run`: true (no normalized parquet created or
  modified by Phase 4bl-C).
- `no_derivation_run`: true.
- `no_feature_computation`: true.
- `no_label_computation`: true.
- `no_gate_run`: true (no raw / derived / feature / label
  eligibility gate executed by Phase 4bl-C).
- `no_gate_report_created`: true.
- `no_successor_state_created`: true.
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
- `no_eligibility_gate_status_transition`: true.
- `no_chronological_split_policy_change`: true.
- `no_project_lock_modification`: true.
- `no_retained_verdict_revision`: true.
- `no_m0_amendment`: true.
- `no_post_null_cooldown_modification`: true.
- `no_cooled_down_families_list_modification`: true.
- `no_phase_4al_no_rescue_rule_modification`: true.
- `no_phase_4bb_f_canonical_path_policy_modification`: true.
- `no_phase_4aw_flip_research_eligible_invariant_modification`: true
  (the method was not invoked by Phase 4bl-C or the merge).
- `no_phase_4bl_d_authorization`: true.
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
4bl-C or by this merge.

## 13. Preserved project locks (verbatim)

- **§11.6 cost lock** — HIGH cost = 8 bps slippage per side;
  round-trip = 16 bps slippage. Preserved verbatim.
- **§1.7.3 project-level locks** — 0.25% risk per trade; 2×
  leverage cap; one position max; mark-price stops. Preserved
  verbatim.
- **Phase 3p §4.7 strict integrity gate** — preserved verbatim
  (aggTrades multi-day extension applied verbatim by Phase 4bl-C
  acquisition).
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
  (Phase 4bl-C raw zips, sidecars, manifest, log, and log sidecar
  all live under the canonical Phase 4bb-F partition layout and
  sidecar format).

All prior phase results preserved verbatim.

## 14. No-rescue constraints

The Phase 4bl-C merge does not, and cannot, be construed as
authorising:

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
  `eligibility_gate_status` from this evidence alone;
- changing `chronological_split_policy` on any manifest from this
  evidence alone;
- re-tuning any of the six cooled-down failed strategy families
  (R2 / F1 / D1-A / V2 / G1 / C1) using the acquired multi-day data;
- re-fitting any threshold or filter that was previously fit on the
  one-day cell using the acquired 90-day evidence base;
- re-evaluating any of the six failed strategies under cherry-picked
  sub-windows of the 90-day range;
- "rescuing" any failed hypothesis by appealing to the larger
  evidence base.

The 90-day acquired multi-day data is **forward research
infrastructure only**. New hypotheses, new ML feasibility studies,
new descriptive diagnostics are all gated by the Phase 4ak M0
twelve-clause gate on the forward path. The acquisition is not, by
itself, evidence of any strategy edge or research conclusion.

## 15. Successor authorization

**None.**

This merge-closeout records Phase 4bl-C as project-complete. It
does **NOT** authorize any successor phase. Specifically:

- Phase 4bl-D (Multi-Day Raw Manifest Eligibility Gate / Raw QA) is
  **NOT** authorized. Phase 4bl-D requires its own separate
  authorization prompt. It would translate the Phase 4bb-D
  raw-eligibility-gate pattern into a v002-multi-day analogue and
  emit one gate report under `data/microstructure/gate-reports/raw/`
  per the Phase 4bb-F canonical path policy. Phase 4bl-D is the
  natural conditional successor; it is not authorized by this merge.
- Phase 4bl-E (Multi-Day Raw Manifest Successor-State Recording) is
  **NOT** authorized.
- Phase 4bm-* (Multi-Day Derived / Normalized Family arc) is
  **NOT** authorized.
- Phase 4bn-* (Multi-Day Feature arc) is **NOT** authorized.
- Phase 4bo-* (Multi-Day Label arc) is **NOT** authorized.
- Phase 4bp-* (Multi-Day Label Diagnostic arc) is **NOT** authorized.
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
- Additional aggTrades acquisition beyond the 90 locked BTCUSDT UTC
  dates: **NOT** authorized.
- 5m / 1m / tick / mark-price 30m / 4h / order-book / spot /
  cross-venue / funding / open-interest data acquisition: **NOT**
  authorized.

## 16. Recommended state

**Remain paused.**

Phase 4bl-C is now project-complete on `main` after this
merge-closeout commit. No immediate follow-up action is required.

**Conditional next, NOT authorized:**

Phase 4bl-D — Multi-Day Raw Manifest Eligibility Gate / Raw QA is
the cleanest non-paused option. It would translate the Phase 4bb-D
raw-eligibility-gate pattern into a v002-multi-day analogue: run a
~45-check eligibility gate over the 90-day per-file inventory and
v002 manifest, cross-check every per-date `sha256` recorded in
`per_file_inventory` against a fresh recomputation of the on-disk
zip, verify decompression integrity and full per-row schema
validation (going beyond the bounded 300-row sample done by
Phase 4bl-C), check agg-id monotonicity and timestamp boundaries on
every row of every day, verify no overlapping or duplicate
aggregate trade IDs across adjacent days, and emit one gate report
under `data/microstructure/gate-reports/raw/` per the Phase 4bb-F
canonical path policy. The gate report would record
`research_eligible_after = false` (raw families are permanently
ineligible per Phase 4bb-E) and `eligibility_gate_status_after =
pass_report_level_only` as a report-level recommendation. Phase
4bl-D is **NOT** authorized by this merge. It requires a separate
operator authorization prompt.

---

**End of Phase 4bl-C merge-closeout.**
