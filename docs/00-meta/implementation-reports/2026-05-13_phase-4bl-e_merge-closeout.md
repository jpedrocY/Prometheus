# Phase 4bl-E — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bl-E — Multi-Day Raw Manifest Successor-State
  Recording
- **Type:** docs + tiny standalone Python stdlib-only recording script
  + offline tests + one local gitignored sibling successor-state JSON
  artefact (with paired SHA256 sidecar)
- **Action:** merge into `main`
- **Merge purpose:** record on `main` the Phase 4bl-E sibling
  successor-state artefact for the raw v002 family
  `microstructure_raw_aggtrades_v001` `v002` under the canonical
  Phase 4bb-F `data/microstructure/successor-state/` namespace. The
  artefact machine-readably records `successor_state =
  "stage2_raw_admissible"`, cites the Phase 4bl-D-R
  `RAW_MULTIDAY_GATE_PASS` (33 / 33 PASS) verbatim, cites the Phase
  4bl-D `RAW_MULTIDAY_GATE_FAIL` predecessor lineage verbatim, cites
  the Phase 4bl-D-S1 governance + Phase 4bl-D-S2 execution
  remediation lineage verbatim, and preserves the v002 raw manifest,
  raw zip, sidecars, acquisition log, Phase 4bl-D / 4bl-D-R / 4bl-D-S2
  reports byte-identically. The merge does **not** rerun any gate,
  does **not** create a new gate report, does **not** mutate the v002
  raw manifest, does **not** flip `research_eligible`, does **not**
  transition `eligibility_gate_status` on the actual manifest, does
  **not** modify any prior `data/microstructure/` artefact, does
  **not** commit any `data/microstructure/` file, does **not** amend
  any governance, and does **not** authorise any successor phase.
- **Target branch:** `main`
- **Source branch:**
  `phase-4bl-e/multi-day-raw-manifest-successor-state-recording`

## 2. SHAs

- **`main` SHA before merge:** `4d91616`
  (`4d9161643656ac1ed6f12fb67389ad3d4b7eb6c8`; Phase 4bl-D-R
  merge-closeout commit `docs(phase-4bl-d-r): add merge closeout`;
  `main` and `origin/main` both at this SHA before the merge began).
- **Branch commit SHA (Phase 4bl-E):**
  - `e2c527a` — `feat(phase-4bl-e): multi-day raw manifest
    successor-state recording`
    (`e2c527a33eadc76899d242b641f01490c119edfd`; single tracked commit
    on the branch; adds the standalone Python stdlib-only recording
    script + offline tests + implementation report + closeout, and
    modifies `docs/00-meta/current-project-state.md`).
- **Merge commit SHA:**
  `e0d92f9e0450492dc30c62450653b8d01911681c`
  (`feat(phase-4bl-e): merge multi-day raw manifest successor-state
  recording`; created by `git merge --no-ff` with the default `ort`
  strategy on `main`).
- **Final `main` / `origin/main` SHA after merge-closeout commit and
  push:** to be filled at commit time of this merge-closeout file.
  The canonical `main` anchor for Phase 4bl-E project-completion is
  the merge-closeout commit (this file's commit) on `main`, recorded
  after push. Per the Phase 4bk-A workflow standard, any future
  one-commit SHA-chain fixup that records the final-`main` SHA value
  into this §2 placeholder is optional, separately authorized, and
  does not change Phase 4bl-E lifecycle semantics.

## 3. Merge method

- `git merge --no-ff` with the default `ort` strategy.
- Merge commit message header:
  `feat(phase-4bl-e): merge multi-day raw manifest successor-state
  recording`.
- Body explicitly records: phase identity (successor-state recording);
  branch tip SHA (`e2c527a`); tracked files (5 — script + tests + main
  memo + closeout + narrow `current-project-state.md` update); local
  gitignored successor-state JSON + paired sidecar (NOT committed);
  ten upstream artefacts byte-identical pre/post; manifest state
  preserved verbatim (`research_eligible: false`,
  `eligibility_gate_status: "pending"`, `date_count: 90`,
  `total_row_count: 155153449`, `total_size_bytes: 1943823208`);
  Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked); full `does NOT`
  enumeration (no gate rerun during merge; no new gate report; no
  Phase 4bl-D gate script modification; no check weakening; no
  sidecar parser relaxation; no Phase 4bb-F amendment; no data
  acquisition; no normalization / derivation / features / labels /
  diagnostics / ML / strategy / signals / backtest; no manifest
  mutation; no `research_eligible` flip; no `eligibility_gate_status`
  transition on the actual manifest; no `chronological_split_policy`
  change; no retained-verdict revision; no project-lock change; no
  M0 amendment; no successor authorization); recommended state
  remain paused; conditional next (NOT authorized) = Phase 4bm-A —
  Multi-Day Normalization Design Memo (docs-only).
- No `--no-verify`. No `--no-gpg-sign`. No
  `-c commit.gpgsign=false`. No force-push.
- Push status: pushed to `origin/main` with no force, no skip-hooks,
  no skip-signing (recorded once the merge-closeout commit is pushed;
  see §16).

## 4. Files brought forward by the merge

### Docs (tracked)

- `docs/00-meta/current-project-state.md` — narrow update: inserted
  a new Phase 4bl-E narrative paragraph immediately before the
  existing Phase 4bl-D-R paragraph and replaced the prior
  "Current phase:" block with a new Phase 4bl-E block, preserving the
  prior Phase 4bl-D-R "Current phase:" block as historical context
  (392 insertions).
- `docs/00-meta/implementation-reports/2026-05-13_phase-4bl-e_multi-day-raw-manifest-successor-state-recording.md`
  (new; 423 insertions) — the Phase 4bl-E implementation report
  (17 sections).
- `docs/00-meta/implementation-reports/2026-05-13_phase-4bl-e_closeout.md`
  (new; 195 insertions) — the Phase 4bl-E branch closeout.

### Source / tests / scripts / config / runtime

- `scripts/phase4bl_e_record_multiday_raw_successor_state.py`
  (new; 1,020 insertions) — standalone Python stdlib-only recording
  script. Python standard library only; no `prometheus.*` /
  `requests` / `httpx` / `aiohttp` / `urllib.request` / `urllib3` /
  `socket` / `websockets` / `binance` / `dotenv` imports; no network
  I/O; no credentials; no `.env`; no `.mcp.json`; no MCP / Graphify;
  no exchange adapters. Verifies ten predeclared input SHAs via
  streaming `hashlib.sha256` (1-MiB chunks); verifies v002 manifest
  state semantics (`research_eligible=false`,
  `eligibility_gate_status="pending"`, `date_count=90`,
  `total_row_count=155153449`, `total_size_bytes=1943823208`);
  verifies the Phase 4bl-D-R gate report's `overall_status="pass"`
  and `gate_verdict="RAW_MULTIDAY_GATE_PASS"`; builds the
  deterministic JSON payload via `json.dumps(payload,
  sort_keys=True, indent=2, ensure_ascii=False)` with no trailing
  newline (matching the Phase 4bb-G raw `__v001` successor-state
  precedent verbatim); atomically writes the JSON via
  `tempfile.mkstemp` + `fsync` + `os.replace`; atomically writes the
  paired SHA256 sidecar in canonical Phase 4bb-F format
  `<sha256_hex>  <basename>\n` (two spaces; trailing LF; no CRLF; no
  BOM); recomputes both output SHAs after write; rechecks all ten
  upstream SHAs post-write for immutability; refuses to overwrite
  either output unless byte-identical (idempotent re-run). ruff
  clean; `py_compile` clean.
- `tests/research/microstructure/test_phase4bl_e_raw_successor_state.py`
  (new; 1,022 insertions) — 45 offline pytest cases using only
  pytest `tmp_path` and synthetic fixtures with monkeypatched
  expected-constants. Tests cover locked identity constants,
  expected-SHA dict shape, Phase 4bl-D-R result block, pure helpers
  (`compute_file_sha256`, `serialize_successor_state`,
  `compose_canonical_sidecar_body`, `derive_short_commit`),
  payload semantic fields, governance labels (every label
  `forbidden`), non-authorizations (every value `false`), boundary
  confirmations (every value `true`), retained verdict ledger,
  preserved locks, no-rescue statement, JSON round-trip, end-to-end
  `run()` happy path via monkeypatched fake repo tree, idempotent
  re-run with pinned timestamps, refuse-overwrite-when-non-identical,
  refusal paths (verdict ≠ PASS, manifest `research_eligible=true`,
  manifest gate status `pass`, wrong row count, wrong date count,
  input SHA mismatch, missing required input), output-path-under-
  successor-state-namespace, upstream byte-identical post-write,
  static forbidden-import scan, static forbidden-runtime-token scan,
  no-`prometheus.*` import scan. All 45 pass.

No `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, MCP
file, or runtime-configuration file was modified by this merge.

The Phase 4bl-D gate script
(`scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py`) was
**not** modified. The Phase 4bl-D-R wrapper script
(`scripts/phase4bl_d_r_rerun_raw_gate.py`) was **not** modified. The
Phase 4bl-D-S2 canonicalization script
(`scripts/phase4bl_d_s2_canonicalize_sidecar.py`) was **not**
modified.

### `data/microstructure/`

None. **No `data/microstructure/` file was modified by this merge.**
The merge introduces zero tracked changes under `data/microstructure/`.
The Phase 4bl-E successor-state JSON
(`data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v002__stage2_raw_admissible__phase-4bl-e.json`)
and its paired `.sha256` sidecar remain gitignored under
`.gitignore:85: data/microstructure/` and are not part of the merge
commit. No raw zip, no sidecar, no manifest, no acquisition log, no
Phase 4bl-D / 4bl-D-R / 4bl-D-S2 report, no other successor-state
file, no normalized parquet, no derived manifest, no feature parquet,
no feature manifest, no label parquet, no label manifest, no
diagnostic, and no split artefact was modified.

### Prior governance memos

None. No prior governance memo (Phase 3p §4.7; Phase 3r §8; Phase 3v
§8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase
4q; Phase 4v; Phase 4w; Phase 4ak M0; Phase 4al no-rescue; Phase 4aw
`flip_research_eligible(...)` invariant; Phase 4bb-F canonical path
policy; Phase 4bb-G raw `__v001` successor-state precedent; Phase
4bl-A; Phase 4bl-B; Phase 4bl-C; Phase 4bl-D; Phase 4bl-D-S1; Phase
4bl-D-S2; Phase 4bl-D-R) was modified beyond the narrow
`current-project-state.md` paragraph addition.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              |  392 ++++++++
 .../2026-05-13_phase-4bl-e_closeout.md             |  195 ++++
 ...i-day-raw-manifest-successor-state-recording.md |  423 ++++++++
 ...ase4bl_e_record_multiday_raw_successor_state.py | 1020 +++++++++++++++++++
 .../test_phase4bl_e_raw_successor_state.py         | 1022 ++++++++++++++++++++
 5 files changed, 3052 insertions(+)
```

The diff matches the expected change set from the Phase 4bl-E merge
authorization prompt exactly: five tracked files (one narrow
modification + four new files), zero deletions, 3,052 insertions
total. No file outside the five documented files is in the diff. No
`data/microstructure/` file appears. No prior source / test / script
was modified. The Phase 4bl-D gate script, the Phase 4bl-D-R wrapper
script, and the Phase 4bl-D-S2 canonicalization script all remain
untouched.

## 6. Verdict

**SUCCESSOR_STATE_RECORDED — sibling successor-state JSON recorded as
report-level / policy-marker evidence only.**

Phase 4bl-E is project-complete on `main` after the merge-closeout
commit is recorded and pushed. The Phase 4bl-E recording script
executed exactly once during branch work and produced a single
deterministic JSON sibling successor-state artefact plus paired
SHA256 sidecar under the gitignored Phase 4bb-F
`data/microstructure/successor-state/` namespace. The artefact
machine-readably records `successor_state =
"stage2_raw_admissible"`, cites the Phase 4bl-D-R
`RAW_MULTIDAY_GATE_PASS` verdict (33 / 33 PASS / 0 FAIL / 0 ERROR /
0 NA across 90 dates) verbatim, cites the Phase 4bl-D
`RAW_MULTIDAY_GATE_FAIL` predecessor lineage verbatim, cites the
Phase 4bl-D-S1 governance + Phase 4bl-D-S2 execution remediation
lineage verbatim, enumerates 39 `*_authorized` flags (all `false`),
enumerates 50 `boundary_confirmations` (all `true`), preserves
every retained verdict verbatim, preserves every project lock
verbatim, and includes an explicit no-rescue statement. The v002
raw manifest remains byte-identical and unmutated; `research_eligible`
remains `false`; `eligibility_gate_status` remains `"pending"`;
`date_count` remains `90`; `total_row_count` remains `155,153,449`;
`total_size_bytes` remains `1,943,823,208`. The Phase 4aw
`MicrostructureManifest.flip_research_eligible(...)` always-raises
invariant is preserved (never invoked; Phase 4bl-E never imports any
`prometheus.*` module). The raw family
`microstructure_raw_aggtrades_v001` `v002` reaches Phase 4ba Stage-2
(gate-passed at sibling-artefact level only). Stage-3
(research-eligible) is unreachable for any raw family by design and
remains unreached. The Phase 4bl-D-R PASS gate report, the Phase
4bl-D FAIL gate report, the Phase 4bl-D-S2 canonicalisation report,
the canonicalised 2025-01-15 sidecar, the 2025-01-15 raw zip, the
v002 raw manifest sidecar, the v002 acquisition log, and the v002
acquisition log sidecar all remain byte-identical at their
previously recorded SHAs and are preserved as historical /
governance evidence. No remediation, normalization, derived parquet,
feature, label, diagnostic, ML, strategy, signal, backtest, paper /
shadow, live-readiness, deployment, exchange-write, production-key
creation, authenticated APIs, private endpoints, user stream,
WebSocket implementation, MCP, Graphify, `.mcp.json`, or credential
work has been authorized or performed.

## 7. Local gitignored outputs (if any)

Phase 4bl-E produced exactly two local gitignored artefacts under
`data/microstructure/successor-state/`. Neither is committed.

1. **Phase 4bl-E successor-state JSON:**
   - path:
     `data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v002__stage2_raw_admissible__phase-4bl-e.json`
   - size: 17,603 bytes
   - SHA256:
     `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d`
   - status: not committed
   - `git check-ignore -v
     data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v002__stage2_raw_admissible__phase-4bl-e.json`
     → `.gitignore:85: data/microstructure/`

2. **Phase 4bl-E paired SHA256 sidecar (canonical Phase 4bb-F format
   `<sha>  <basename>\n`; two spaces; trailing LF):**
   - path: same as (1) with `.sha256` suffix
   - size: 147 bytes
   - SHA256:
     `63d97bf54e1063f2fd70024d40639db711e9c24d929074cdd63b2db385302b4f`
   - status: not committed
   - sidecar parses to a token that matches the recomputed
     successor-state JSON SHA bit-for-bit
   - `git check-ignore -v
     data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v002__stage2_raw_admissible__phase-4bl-e.json.sha256`
     → `.gitignore:85: data/microstructure/`

Predecessor / source references (recorded verbatim inside the
successor-state JSON body):

- Phase 4bl-D-R PASS gate report id
  `microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080`
  (SHA `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46`).
- Phase 4bl-D FAIL gate report id
  `microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a`
  (SHA `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7`).
- Phase 4bl-D-S2 canonicalisation report id
  `microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__1778713761225__0d51bd7bac1e`
  (SHA `8c6457b65a4a3413c7836aea391d6b2cbd82c5cbd6252c6239f7e948e20809d3`).
- Phase 4bl-C v002 raw manifest SHA
  `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485`.
- Phase 4bl-C v002 acquisition log SHA
  `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314`.
- Phase 4bl-D-S2 canonicalised 2025-01-15 sidecar SHA
  `c40e6be60753a912063d9a5f5c1617ba31ec987c09121c50adab3ba0226018fc`
  (99 bytes; LF).
- Phase 4az 2025-01-15 raw zip SHA
  `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`.

## 8. Validation results

- `git diff --check` (post-merge): clean (no whitespace errors).
- `git status --short` (post-merge): only the pre-existing untracked
  entries `.claude/scheduled_tasks.lock` and `data/research/` (both
  unrelated to Phase 4bl-E and out-of-scope; pre-existing on `main`).
- `git diff --stat main^..HEAD` (post-merge): 5 files changed,
  3,052 insertions(+), 0 deletions; matches §5.
- `git ls-files data/microstructure/`: empty (no
  `data/microstructure/` file is tracked).
- `python -m py_compile scripts/phase4bl_e_record_multiday_raw_successor_state.py`
  → OK.
- `python -m py_compile tests/research/microstructure/test_phase4bl_e_raw_successor_state.py`
  → OK.
- `uv run ruff check scripts/phase4bl_e_record_multiday_raw_successor_state.py
  tests/research/microstructure/test_phase4bl_e_raw_successor_state.py`
  → `All checks passed!`
- `uv run pytest tests/research/microstructure/test_phase4bl_e_raw_successor_state.py`
  → `45 passed in 0.53s`.
- `git check-ignore -v data/microstructure/` →
  `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/successor-state/` →
  `.gitignore:85: data/microstructure/`.
- `git check-ignore -v
  data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v002__stage2_raw_admissible__phase-4bl-e.json`
  → `.gitignore:85: data/microstructure/`.
- `git check-ignore -v
  data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v002__stage2_raw_admissible__phase-4bl-e.json.sha256`
  → `.gitignore:85: data/microstructure/`.
- The Phase 4bl-E recording script was **not** rerun during the
  merge (per merge authorization). The single recording execution
  recorded on the branch was performed exactly once during
  Phase 4bl-E branch work and produced the JSON + sidecar whose SHAs
  are recorded in §7 above; both SHAs were recomputed bit-identical
  post-merge.
- The Phase 4bl-D-R raw gate was **not** rerun during the merge.
  The Phase 4bl-D-S2 canonicalisation was **not** rerun. The Phase
  4bl-D gate was **not** rerun. The Phase 4bd normalizer was **not**
  rerun. The Phase 4bf derived-family gate was **not** rerun. The
  Phase 4bh feature kernel was **not** rerun. The Phase 4bi-B
  feature-family eligibility gate was **not** rerun. The Phase 4bj-C
  label kernel was **not** rerun. The Phase 4bj-E label-family
  eligibility gate was **not** rerun.
- Whole-repo `ruff` / `mypy` / whole-repo `pytest` were **not**
  rerun by the Phase 4bl-E merge because the merge does not modify
  any prior source module and does not modify any prior test (the
  new `scripts/phase4bl_e_record_multiday_raw_successor_state.py` is
  a standalone Python stdlib-only recording script which is
  scoped-ruff / scoped-`py_compile` clean and untouched by the rest
  of the codebase; the new
  `tests/research/microstructure/test_phase4bl_e_raw_successor_state.py`
  is scoped-pytest clean and shares no fixture with any prior test).
  The latest authoritative whole-repo validation remains the Phase
  4bb-F-implementation merge baseline (`ruff` PASS, `mypy` strict
  120 source files PASS, microstructure `pytest` 915 passed + 1
  pre-existing labelled skip, whole-repo `pytest` 1698 passed + 1
  skipped + 2 pre-existing simulation failures unchanged from prior
  phases; the two failures are
  `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt`
  and `::test_real_2026_03_ethusdt`, both `KeyError: 'trade_count'`
  in unrelated `src/prometheus/research/data/storage.py:232`).
- Independent post-merge recompute of all upstream artefact SHA256
  values returned bit-identical matches (see §9).

## 9. Upstream immutability evidence (if applicable)

Every upstream `data/microstructure/` artefact recorded by the Phase
4bl-E authorization prompt as required-byte-identical is preserved
verbatim by the Phase 4bl-E merge and confirmed bit-identical by
independent post-merge recompute on `main`:

| Artefact | Expected SHA256 | Post-merge SHA256 | Status |
| --- | --- | --- | --- |
| v002 raw manifest `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json` (105,052 bytes) | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | IDENTICAL |
| v002 raw manifest sidecar `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json.sha256` (111 bytes) | `adaf97242cfbe922bc9e93a6699e547d1b02fa64a96dd2cdd08df1814ce25e26` | `adaf97242cfbe922bc9e93a6699e547d1b02fa64a96dd2cdd08df1814ce25e26` | IDENTICAL |
| v002 acquisition log `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json` (302,055 bytes) | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | IDENTICAL |
| v002 acquisition log sidecar `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json.sha256` (127 bytes) | `975bdc544152d1f84f6e700309aad89998e663cb779acc5883bd20652e428958` | `975bdc544152d1f84f6e700309aad89998e663cb779acc5883bd20652e428958` | IDENTICAL |
| Phase 4bl-D-R PASS gate report `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json` (171,342 bytes) | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` | IDENTICAL |
| Phase 4bl-D-R PASS gate report sidecar `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json.sha256` (155 bytes) | `84f37b7b424d67dfa0dae06bb51279354b5b37998beb4f9b1cf6b6f617dd8c02` | `84f37b7b424d67dfa0dae06bb51279354b5b37998beb4f9b1cf6b6f617dd8c02` | IDENTICAL |
| Phase 4bl-D FAIL gate report `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a.json` (169,637 bytes) | `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7` | `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7` | IDENTICAL |
| Phase 4bl-D-S2 canonicalisation report `data/microstructure/canonicalization-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__1778713761225__0d51bd7bac1e.json` (5,241 bytes) | `8c6457b65a4a3413c7836aea391d6b2cbd82c5cbd6252c6239f7e948e20809d3` | `8c6457b65a4a3413c7836aea391d6b2cbd82c5cbd6252c6239f7e948e20809d3` | IDENTICAL |
| canonicalised 2025-01-15 sidecar `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256` (99 bytes; LF) | `c40e6be60753a912063d9a5f5c1617ba31ec987c09121c50adab3ba0226018fc` | `c40e6be60753a912063d9a5f5c1617ba31ec987c09121c50adab3ba0226018fc` | IDENTICAL |
| 2025-01-15 raw zip `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip` (21,271,119 bytes) | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | IDENTICAL |

The Phase 4bl-E successor-state JSON and paired sidecar themselves
are also confirmed byte-identical post-merge:

| Artefact | Expected SHA256 | Post-merge SHA256 | Status |
| --- | --- | --- | --- |
| Phase 4bl-E successor-state JSON (17,603 bytes) | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` | IDENTICAL |
| Phase 4bl-E successor-state sidecar (147 bytes) | `63d97bf54e1063f2fd70024d40639db711e9c24d929074cdd63b2db385302b4f` | `63d97bf54e1063f2fd70024d40639db711e9c24d929074cdd63b2db385302b4f` | IDENTICAL |

Additional artefacts confirmed preserved by independent post-merge
tree state (sampled — not exhaustive):

- Phase 4az `__v001` raw manifest, Phase 4az `__v001` raw zip sidecar
  (canonical LF form per Phase 4bl-D-S2), Phase 4az acquisition log,
  Phase 4bb-D raw gate report + sidecar, Phase 4bd normalized parquet,
  Phase 4bd derived manifest, Phase 4be derived gate report, Phase
  4bf derived gate report, Phase 4bg-B derived successor-state, Phase
  4bh feature parquet + manifest, Phase 4bi-B feature gate report,
  Phase 4bi-D feature successor-state, Phase 4bj-C label parquet +
  manifest, Phase 4bj-E label gate report, Phase 4bj-G label
  successor-state, Phase 4bj-J no-split determination, Phase 4bb-G
  raw `__v001` successor-state — all preserved at their previously
  recorded SHAs.

**Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant preserved (never invoked).** Phase 4bl-E
never imports any `prometheus.*` module, so the `flip_research_eligible`
codepath is unreachable from Phase 4bl-E by construction.

## 10. Manifest state preservation (if applicable)

Every manifest in scope of Phase 4bl-E is preserved verbatim:

- **v002 raw manifest** (`data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json`):
  `research_eligible: false`, `eligibility_gate_status: "pending"`,
  `date_count: 90`, `total_row_count: 155153449`,
  `total_size_bytes: 1943823208`, `symbol_list: ["BTCUSDT"]`,
  `date_start: "2024-12-01"`, `date_end: "2025-02-28"`, governance
  labels unchanged from the Phase 4bl-C state; not modified by Phase
  4bl-E. SHA
  `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485`
  bit-identical pre/post.
- **`__v001` raw manifest (Phase 4az):** `research_eligible: false`,
  `eligibility_gate_status: "pending"`; not modified.
- **Phase 4bd derived manifest:** `research_eligible: false`,
  `eligibility_gate_status: "pending"`; not modified.
- **Phase 4bh feature manifest:** `research_eligible: false`,
  `eligibility_gate_status: "pending"`; not modified.
- **Phase 4bj-C label manifest:** `research_eligible: false`,
  `eligibility_gate_status: "pending"`,
  `chronological_split_policy: "not_yet_defined"`; not modified.
- Every successor-state sibling artefact (Phase 4bb-G raw `__v001`;
  Phase 4bg-B derived; Phase 4bi-D feature; Phase 4bj-G label; Phase
  4bj-J label no-split) preserved verbatim.

**Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant preserved (never invoked).** The Phase 4bl-E
successor-state JSON records `manifest_research_eligible_after =
false` and `manifest_eligibility_gate_status_after = "pending"` as
report-level / policy-marker invariants; these values appear only on
the sibling successor-state artefact and not on any on-disk manifest.
Any future tool that wishes to interpret the v002 raw family as
Stage-2-admissible must read the Phase 4bl-E successor-state artefact,
not the v002 manifest's `eligibility_gate_status` field. The v002
manifest's `eligibility_gate_status` field will remain `"pending"`
permanently for the raw family, because the Phase 4ba 5-stage ladder
caps the raw family at Stage-2 (raw families cannot reach Stage-3 by
design). No flag flip occurred; no manifest transition occurred.

## 11. Boundary confirmations

The Phase 4bl-E merge honours every boundary required by the merge
authorization prompt and the Phase 4bk-A workflow standard:

- the Phase 4bl-E recording script was NOT rerun during the merge
  (the single recording execution occurred exactly once on the
  branch);
- the Phase 4bl-D-R raw gate was NOT rerun during the merge;
- the Phase 4bl-D-S2 canonicalisation was NOT rerun during the merge;
- the Phase 4bl-D gate was NOT rerun during the merge;
- the Phase 4bd normalizer was NOT rerun during the merge;
- the Phase 4bf derived-family gate was NOT rerun during the merge;
- the Phase 4bh feature kernel was NOT rerun during the merge;
- the Phase 4bi-B feature-family eligibility gate was NOT rerun
  during the merge;
- the Phase 4bj-C label kernel was NOT rerun during the merge;
- the Phase 4bj-E label-family eligibility gate was NOT rerun during
  the merge;
- no new gate report was created by the merge;
- no new canonicalisation report was created by the merge;
- no new successor-state artefact was created by the merge (the
  single successor-state JSON + sidecar produced during branch work
  remain on disk; the merge did not regenerate them);
- no Phase 4bl-D gate script modification;
- no Phase 4bl-D-R wrapper script modification;
- no Phase 4bl-D-S2 canonicalization script modification;
- no weakening of any of the 33 Phase 4bl-D checks;
- no sidecar parser relaxation;
- no Phase 4bb-F canonical path policy amendment (the Phase 4bl-E
  successor-state JSON filename follows the policy verbatim:
  `<family>__<version>__<stage_marker>__phase-<id>.json` with
  `phase-<id> = phase-4bl-e` lowercase under `successor-state/`);
- no Phase 4bb-G raw `__v001` successor-state precedent amendment
  (Phase 4bl-E is the v002 multi-day analogue of Phase 4bb-G; same
  serialisation, same path discipline, same sidecar format);
- no modification of the canonicalised 2025-01-15 sidecar;
- no modification of any other sidecar;
- no modification of any raw zip;
- no modification of the v002 raw manifest;
- no modification of the v002 acquisition log;
- no modification of the Phase 4bl-D gate report;
- no modification of the Phase 4bl-D-R gate-rerun report;
- no modification of the Phase 4bl-D-S2 canonicalisation report;
- no modification of any prior gate report (Phase 4bb-D, Phase 4bf,
  Phase 4bi-B, Phase 4bj-E, Phase 4bl-D, Phase 4bl-D-R, etc.);
- no modification of any successor-state artefact (Phase 4bb-G;
  Phase 4bg-B; Phase 4bi-D; Phase 4bj-G; Phase 4bj-J);
- no modification of any normalized / derived / feature / label
  parquet, manifest, or sidecar;
- no `data/microstructure/` artefact committed (the Phase 4bl-E
  successor-state JSON and paired sidecar remain gitignored under
  `.gitignore:85: data/microstructure/`);
- no data acquired, downloaded, or normalized;
- no public endpoint called; no `data.binance.vision` call; no
  Binance API called; no `fapi.binance.com` call; no
  `api.binance.com` call;
- no authenticated REST contacted; no private endpoint contacted;
- no WebSocket opened; no user stream contacted; no listenKey
  lifecycle invoked;
- no credential / `.env` / `.mcp.json` / MCP / Graphify used, read,
  written, or referenced;
- no normalizer / raw gate / derived gate / feature kernel /
  feature gate / label kernel / label gate / diagnostic / ML /
  strategy / backtest script rerun;
- no source code, test, script, configuration, `pyproject.toml`,
  `README.md`, `.gitignore`, `.gitattributes`, or MCP-file
  modification beyond the four new tracked files (one recording
  script + one test file + two docs) and the narrow
  `current-project-state.md` paragraph addition;
- no `research_eligible` flipped on any actual manifest;
- no `eligibility_gate_status` transitioned on any actual manifest;
- no `chronological_split_policy` changed on any actual manifest;
- no derived / normalized parquet created;
- no feature parquet computed; no feature manifest created;
- no label parquet computed; no label manifest created;
- no label diagnostics run; no label statistics computed;
- no split artefact created;
- no returns / PnL / MFE / MAE / R-multiple / equity / position /
  alpha / edge / prediction / model-score / decision-score /
  entry-exit / strategy output computed;
- no ML model trained, designed, selected, or feature-ranked;
- no meta-labeling created;
- no strategy created, implemented, or rescued;
- no signal computed;
- no backtest run;
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked; Phase 4bl-E
  never imports any `prometheus.*` module);
- Phase 4bb-F canonical path policy preserved verbatim (Phase 4bl-E
  follows it; no policy text changed);
- Phase 4bb-G raw `__v001` successor-state precedent preserved
  verbatim (Phase 4bl-E is the v002 multi-day analogue);
- Phase 4bl-D `RAW_MULTIDAY_GATE_FAIL` preserved as historical
  evidence — the Phase 4bl-D gate report remains byte-identical at
  its previously recorded SHA;
- Phase 4bl-D-S2 canonicalisation outcome preserved as historical
  evidence — the canonicalisation report remains byte-identical at
  its previously recorded SHA;
- Phase 4bl-D-R `RAW_MULTIDAY_GATE_PASS` preserved as the latest gate
  evidence — the Phase 4bl-D-R gate-rerun report and its paired
  sidecar remain byte-identical at their previously recorded SHAs;
- Phase 4ak M0 twelve-clause gate, post-null cooldown rule,
  cooled-down families list, and memo template preserved;
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
  preserved;
- no retained verdict revised;
- no project lock loosened;
- no M0 amendment;
- no successor authorized;
- no remediation executed beyond the Phase 4bl-D-S2 sidecar
  canonicalisation that occurred under separate operator
  authorization prior to Phase 4bl-D-R / Phase 4bl-E; Phase 4bl-E
  itself performed no remediation, only the recording of a single
  sibling successor-state JSON + paired sidecar.

## 12. Retained verdict ledger

Every retained verdict is preserved verbatim:

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

All preserved verbatim.

## 13. Preserved project locks

Every preserved lock is recorded verbatim:

- §11.6 = 8 bps per side;
- round-trip = 16 bps;
- §1.7.3 = 0.25% risk per trade / 2× leverage cap / one-position
  max / mark-price stops;
- Phase 3p §4.7 strict integrity gate (multi-day extension applied
  verbatim by Phase 4bl-D; rerun verbatim by Phase 4bl-D-R;
  successor-state recording verbatim by Phase 4bl-E);
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
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy;
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant (preserved end-to-end; Phase 4bl-E never
  imports any `prometheus.*` module);
- Phase 4bb-F canonical path policy (Phase 4bl-E follows it
  verbatim — the successor-state filename contains the canonical
  `phase-4bl-e` segment and is written under
  `data/microstructure/successor-state/`);
- Phase 4bb-G raw `__v001` successor-state precedent (Phase 4bl-E is
  the v002 multi-day analogue);
- Phase 4bl-D 33-check raw eligibility-gate protocol (rerun verbatim
  by Phase 4bl-D-R; not invoked by Phase 4bl-E);
- Phase 4bl-D-S1 Option B1 recommendation (operationalised by Phase
  4bl-D-S2; preserved verbatim);
- Phase 4bl-D-S2 sidecar canonicalisation outcome (preserved
  verbatim);
- Phase 4bl-D-R `RAW_MULTIDAY_GATE_PASS` outcome (preserved
  verbatim; cited by Phase 4bl-E as latest gate evidence).

All prior phase results preserved verbatim.

## 14. No-rescue constraints

The Phase 4bl-E merge does **not**, and cannot be construed as
authorising:

- a second invocation of the Phase 4bl-E recording script (the
  recording occurred exactly once during branch execution; the merge
  does not re-execute it; any further successor-state recording
  requires a separately authorized governance decision);
- a second invocation of any prior gate or kernel (Phase 4bl-D-R
  gate; Phase 4bl-D-S2 canonicalisation; Phase 4bl-D gate; Phase 4bd
  normalizer; Phase 4bf derived gate; Phase 4bh feature kernel;
  Phase 4bi-B feature gate; Phase 4bj-C label kernel; Phase 4bj-E
  label gate);
- modification, normalization, replacement, or rewrite of any
  sidecar, raw zip, manifest, acquisition log, gate report,
  canonicalisation report, or successor-state artefact;
- any further `data/microstructure/` write or modification;
- v002 raw manifest mutation, including any `research_eligible`
  flip, `eligibility_gate_status` transition, or governance-label
  change;
- v002 acquisition log mutation;
- any prior gate report, normalized parquet, feature parquet, label
  parquet, derived manifest, feature manifest, label manifest,
  sidecar, successor-state, diagnostic, or split artefact
  modification;
- normalization, derived parquet, features, labels, label
  diagnostics, label statistics, ML, strategy, signals, or backtest
  work;
- additional aggTrades / 5m / 1m / tick / mark-price 30m / 4h /
  order-book / spot / cross-venue / funding / open-interest data
  acquisition;
- paper / shadow / live-readiness / deployment / exchange-write /
  production-key creation / authenticated APIs / private endpoints
  / public-endpoint calls in code / user stream / live WebSocket
  implementation;
- MCP / Graphify / `.mcp.json` / credentials;
- flipping `research_eligible` on any actual manifest;
- transitioning `eligibility_gate_status` on any actual manifest;
- changing `chronological_split_policy` on any actual manifest;
- amending Phase 4bb-F canonical path policy;
- amending Phase 4bb-G raw `__v001` successor-state precedent;
- amending the Phase 4bl-D gate;
- weakening any of the 33 Phase 4bl-D checks;
- relaxing the sidecar parser to accept CRLF;
- creating a new gate report;
- creating a new canonicalisation report;
- creating a new successor-state artefact;
- old-strategy alt-symbol rerun or cooled-down-family reopening
  (R2 / F1 / D1-A / V2 / G1 / C1 first-spec rejections remain
  terminal; the 5m research thread remains operationally closed
  per Phase 3t);
- transitioning any manifest state from this sibling successor-state
  artefact alone;
- Phase 4bm-A — Multi-Day Normalization Design Memo (docs-only);
- Phase 4bm-* (multi-day derived arc);
- Phase 4bn-* (multi-day feature arc);
- Phase 4bo-* (multi-day label arc);
- Phase 4bp-* (multi-day diagnostics);
- Phase 4bq-* (multi-day chronological split);
- Phase 4 canonical;
- Phase 5;
- any other successor phase.

## 15. Successor authorization

**None.**

Phase 4bl-E does **not** authorize any successor phase. The natural
conditional successor implied by the Phase 4bl-E recording requires a
further separately authorized operator prompt and is **NOT**
authorized by this merge:

- **Phase 4bm-A — Multi-Day Normalization Design Memo (docs-only)**
  (NOT authorized): would translate the Phase 4bc derived-family
  normalization design into a v002 multi-day analogue (proposed new
  derived family `microstructure_normalized_aggtrades_v001` `v002`;
  one-to-one row mapping; Decimal-as-string price / quantity; UTC ms
  timestamps; per-day partitioning; manifest cites v002 raw manifest
  SHA + Phase 4bl-E successor-state SHA + Phase 4bl-D-R gate-report
  SHA). Phase 4bl-E does **not** authorize Phase 4bm-A; a separately
  authorized operator prompt is required.

Also **NOT** authorized:

- Phase 4bm-* (multi-day derived arc beyond 4bm-A);
- Phase 4bn-* (multi-day feature arc);
- Phase 4bo-* (multi-day label arc);
- Phase 4bp-* (multi-day diagnostics);
- Phase 4bq-* (multi-day chronological split);
- Phase 5;
- Phase 4 canonical;
- paper / shadow / live-readiness / deployment / production keys /
  authenticated APIs / private endpoints / user stream / live
  WebSocket implementation / MCP / Graphify / `.mcp.json` /
  credentials / exchange-write;
- additional aggTrades / 5m / 1m / tick / mark-price 30m / 4h /
  order-book / spot / cross-venue / funding / open-interest data
  acquisition;
- ML implementation, ML training, model selection, feature ranking,
  meta-labeling, strategy implementation, backtest implementation.

Each step requires a separately authorized operator prompt. Phase
4bl-E makes no claim about expected execution sequencing beyond
recording the executed sibling successor-state artefact and
preserving every retained verdict and project lock verbatim.

## 16. Recommended state

**Remain paused.**

Phase 4bl-E is project-complete on `main` after this merge-closeout
commit is recorded and pushed. The Phase 4bl-E sibling successor-state
JSON artefact + paired SHA256 sidecar are now the canonical
report-level / policy-marker evidence that the raw v002 family
`microstructure_raw_aggtrades_v001` `v002` is at Phase 4ba Stage-2
(`stage2_raw_admissible`). The v002 raw manifest remains
`research_eligible: false` and `eligibility_gate_status: "pending"`;
no on-disk manifest transition has been authorized. The 2025-01-15
raw zip, the canonicalised 2025-01-15 sidecar, the v002 raw manifest
+ sidecar, the v002 acquisition log + sidecar, the Phase 4bl-D-R PASS
gate report + sidecar, the Phase 4bl-D FAIL gate report, and the
Phase 4bl-D-S2 canonicalisation report all remain byte-identical at
their previously recorded SHAs and are preserved as historical /
governance evidence. The Phase 4aw
`MicrostructureManifest.flip_research_eligible(...)` always-raises
invariant is preserved (never invoked; Phase 4bl-E never imports any
`prometheus.*` module). The operator has signalled an intent to
pause for a broader project discussion (complexity, phase usefulness,
energy-market sibling project ideas) before any successor is
authorized.

**Conditional next, NOT authorized:** A future separately authorized
Phase 4bm-A Multi-Day Normalization Design Memo (docs-only) would be
the cleanest non-paused option. Per the Phase 4bk-A workflow
standard, a separately authorized operator prompt is required before
any Phase 4bm-A work may begin. Phase 4bl-E does **not** authorize
Phase 4bm-A.

Push status (recorded after merge-closeout commit is committed and
pushed): pushed to `origin/main` with no force, no skip-hooks, no
skip-signing.
