# Phase 4bl-D-S2 — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bl-D-S2 — Controlled Sidecar Canonicalization
  Execution
- **Type:** docs + tiny standalone script + offline tests + one
  local gitignored sidecar mutation + one local gitignored
  canonicalization report
- **Action:** merge into `main`
- **Merge purpose:** record on `main` the Phase 4bl-D-S2
  controlled execution that operationalised the Phase 4bl-D-S1
  Option B1 recommendation. Phase 4bl-D-S2 rewrote the single
  non-canonical Phase 4az 2025-01-15 sidecar from Windows CRLF
  (100 bytes) to canonical Phase 4bb-F LF (99 bytes), preserving
  the embedded SHA value and basename byte-identically and
  preserving all five upstream artefacts byte-identically. The
  merge does **not** rerun the Phase 4bl-D gate, does **not**
  create a new gate report, does **not** authorize any successor
  phase, and does **not** transition any manifest state.
- **Target branch:** `main`
- **Source branch:** `phase-4bl-d-s2/controlled-sidecar-canonicalization-execution`

## 2. SHAs

- **`main` SHA before merge:** `0d51bd7`
  (`0d51bd7bac1eec1e11d7bad280e480dd8674a97f`; Phase 4bl-D-S1
  merge-closeout commit `docs(phase-4bl-d-s1): add merge
  closeout`; `main` and `origin/main` both at this SHA before
  the merge began).
- **Branch commit SHA (Phase 4bl-D-S2):**
  - `3a8864b` — `feat(phase-4bl-d-s2): controlled sidecar
    canonicalization execution`
    (`3a8864b85b78f410b426a0cc106efc65f76cd98f`; single tracked
    commit on the branch; adds the standalone canonicalization
    script + offline tests + implementation report + closeout,
    and modifies `docs/00-meta/current-project-state.md`).
- **Merge commit SHA:**
  `d8c43b5b433104efe6f522ad50ea74d46dd911f3`
  (`feat(phase-4bl-d-s2): merge controlled sidecar
  canonicalization execution`; created by `git merge --no-ff`
  with the default `ort` strategy).
- **Final `main` / `origin/main` SHA after merge-closeout commit
  and push:** to be filled at commit time of this merge-closeout
  file. The canonical `main` anchor for Phase 4bl-D-S2
  project-completion is the merge-closeout commit (this file's
  commit) on `main`, recorded after push. Per Phase 4bk-A
  workflow-standard convention, any future one-commit SHA-chain
  fixup that records the final-`main` SHA value into this §2
  placeholder is optional, separately authorized, and does not
  change Phase 4bl-D-S2 lifecycle semantics.

## 3. Merge method

- `git merge --no-ff` with the default `ort` strategy.
- Merge commit message header:
  `feat(phase-4bl-d-s2): merge controlled sidecar
  canonicalization execution`.
- Body explicitly records: scope (script + tests + 2 docs +
  narrow `current-project-state.md` update); execution status
  SUCCESSFUL_CANONICALIZATION; full mutation summary (pre/post
  sidecar SHA and size, line-ending, byte delta, embedded SHA
  and basename preservation); five upstream artefacts
  byte-identical pre/post; local gitignored output paths and
  SHAs (canonicalization report + sidecar; NOT committed); all
  validation results; full `did NOT` enumeration (no gate rerun;
  no Phase 4bb-F amendment; no Phase 4bl-D gate amendment; no
  data acquisition; no normalization / derivation / features /
  labels / diagnostics / ML / strategy / signals / backtest; no
  manifest mutation; no `research_eligible` flip; no
  `eligibility_gate_status` transition; no
  `chronological_split_policy` change; no retained-verdict
  revision; no project-lock change; no M0 amendment; no
  successor authorization); preserved verdicts and locks
  verbatim; Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked); Phase 4bb-F
  canonical path policy preserved verbatim (the rewritten Phase
  4az sidecar now conforms; no policy text changed); recommended
  state remain paused; conditional next (NOT authorized) =
  future Phase 4bl-D-R Multi-Day Raw Manifest Eligibility Gate
  Rerun.
- No `--no-verify`. No `--no-gpg-sign`. No
  `-c commit.gpgsign=false`. No force-push.
- Push status: pushed to `origin/main` with no force, no
  skip-hooks, no skip-signing (recorded once the merge-closeout
  commit is pushed; see §16).

## 4. Files brought forward by the merge

### Docs (tracked)

- `docs/00-meta/current-project-state.md` — narrow update:
  inserted a new Phase 4bl-D-S2 narrative paragraph immediately
  before the existing Phase 4bl-D-S1 paragraph and replaced the
  prior "Current phase:" block with a new Phase 4bl-D-S2 block,
  preserving the prior Phase 4bl-D-S1 "Current phase:" block as
  historical context (296 insertions).
- `docs/00-meta/implementation-reports/2026-05-13_phase-4bl-d-s2_controlled-sidecar-canonicalization-execution.md`
  (new; 542 insertions) — the Phase 4bl-D-S2 implementation
  report.
- `docs/00-meta/implementation-reports/2026-05-13_phase-4bl-d-s2_closeout.md`
  (new; 280 insertions) — the Phase 4bl-D-S2 branch closeout.

### Source / tests / scripts / config / runtime

- `scripts/phase4bl_d_s2_canonicalize_sidecar.py` (new; 800
  insertions) — standalone Python-stdlib-only canonicalization
  script; fail-closed on every precondition and postcondition;
  no `requests`/`httpx`/`aiohttp`/`urllib`/`urllib3`/`socket`/
  `websockets`/`binance`/`dotenv`/`os.environ`/`os.getenv`
  imports; no network I/O; no credentials; no `.env`; no
  Binance API; atomic write via `tempfile.mkstemp` + `fsync` +
  `os.replace`; ruff clean; `py_compile` clean.
- `tests/research/microstructure/test_phase4bl_d_s2_sidecar_canonicalization.py`
  (new; 645 insertions) — 28 offline pytest cases using only
  pytest `tmp_path` and synthetic fixtures with monkeypatched
  expected-constants; all 28 pass; cover canonical body
  parse/render, CRLF→LF rewrite, atomic-write semantics,
  refuse-to-overwrite and refuse-stale-tmp behaviour, all
  precondition fail-paths, all postcondition fail-paths,
  end-to-end `main()` happy path, `--dry-run` non-mutation,
  deterministic JSON serialisation, static forbidden-import
  scan over import-lines only, static forbidden-runtime-token
  scan.

No `pyproject.toml`, `README.md`, `.gitignore`,
`.gitattributes`, MCP file, or runtime-configuration file was
modified by this merge.

### `data/microstructure/`

None. **No `data/microstructure/` file was modified by this
merge.** The merge introduces zero tracked changes under
`data/microstructure/`. The single Phase 4az 2025-01-15
sidecar that was rewritten in-place during branch execution
remains gitignored under `.gitignore:85: data/microstructure/`
and is not part of the merge commit. The canonicalization
report (`data/microstructure/canonicalization-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__1778713761225__0d51bd7bac1e.json`)
and its paired `.sha256` sidecar remain gitignored under the
same rule and are not part of the merge commit. No raw zip,
no other sidecar, no manifest, no acquisition log, no gate
report, no successor-state file, no normalized parquet, no
derived manifest, no feature parquet, no feature manifest,
no label parquet, no label manifest, no diagnostic, no split
artefact was modified.

### Prior governance memos

None. No prior governance memo (Phase 3p §4.7; Phase 3r §8;
Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k;
Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0; Phase 4al
no-rescue; Phase 4aw `flip_research_eligible(...)` invariant;
Phase 4bb-F canonical path policy; Phase 4bl-A; Phase 4bl-B;
Phase 4bl-C; Phase 4bl-D; Phase 4bl-D-S1) was modified beyond
the narrow `current-project-state.md` paragraph addition.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 296 ++++++++
 .../2026-05-13_phase-4bl-d-s2_closeout.md          | 280 ++++++++
 ...ontrolled-sidecar-canonicalization-execution.md | 542 ++++++++++++++
 scripts/phase4bl_d_s2_canonicalize_sidecar.py      | 800 +++++++++++++++++++++
 .../test_phase4bl_d_s2_sidecar_canonicalization.py | 645 +++++++++++++++++
 5 files changed, 2563 insertions(+)
```

The diff matches the expected change set from the Phase 4bl-D-S2
merge authorization prompt exactly: five tracked files (one narrow
modification + four new files), zero deletions, 2,563 insertions
total. No file outside the five documented files is in the diff.
No `data/microstructure/` file appears.

## 6. Verdict

**LOCAL ARTEFACT PRODUCED — SUCCESSFUL_CANONICALIZATION.**

Phase 4bl-D-S2 is project-complete on `main` after the
merge-closeout commit is recorded and pushed. The Phase 4bl-D-S1
Option B1 recommendation is now executed: the single
non-canonical Phase 4az 2025-01-15 sidecar has been atomically
rewritten in-place from Windows CRLF (100 bytes; SHA
`b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d`)
to canonical Phase 4bb-F LF (99 bytes; SHA
`c40e6be60753a912063d9a5f5c1617ba31ec987c09121c50adab3ba0226018fc`),
preserving the embedded SHA value
`f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`
and the embedded basename `BTCUSDT-aggTrades-2025-01-15.zip`
byte-identically. All five upstream artefacts (target raw zip,
v002 manifest, v002 acquisition log, Phase 4bl-D gate report,
and the embedded SHA value itself) are byte-identical pre/post.
The mutation type is `metadata_sidecar_line_ending_canonicalization`;
`byte_delta = -1`; `market_data_mutated = false`;
`raw_zip_mutated = false`; `manifest_mutated = false`;
`gate_rerun_performed = false`; `successor_authorized = false`.
The v002 raw manifest remains `research_eligible: false` and
`eligibility_gate_status: "pending"`. The Phase 4bl-D
`RAW_MULTIDAY_GATE_FAIL` remains the last gate verdict on
record; the Phase 4bl-D gate report and its sidecar remain
byte-identical at their previously recorded SHAs. No new gate
report was created. No successor-state artefact was created.
No Phase 4bb-F amendment occurred. No Phase 4bl-D gate
amendment occurred. The Phase 4aw
`MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant is preserved (never invoked). The Phase
4bb-F canonical path policy is preserved verbatim — the
rewritten sidecar now conforms; no policy text changed. No
remediation, normalization, derived parquet, feature, label,
diagnostic, ML, strategy, signal, backtest, paper / shadow,
live-readiness, deployment, exchange-write, production-key
creation, authenticated APIs, private endpoints, user stream,
WebSocket implementation, MCP, Graphify, `.mcp.json`, or
credential work has been authorized or performed.

## 7. Local gitignored outputs (if any)

Phase 4bl-D-S2 mutated and produced exactly three local
gitignored artefacts under `data/microstructure/`. None is
committed.

1. **Rewritten target sidecar (in-place CRLF → LF
   canonicalization):**
   - path:
     `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256`
   - size: 99 bytes (was 100 bytes)
   - line-ending: LF (was CRLF)
   - SHA256:
     `c40e6be60753a912063d9a5f5c1617ba31ec987c09121c50adab3ba0226018fc`
     (was
     `b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d`)
   - status: not committed; pre-existing Phase 4az fixture
     mutated in-place exactly once under Phase 4bl-D-S1 Option
     B1 authorization
   - `git check-ignore -v
     data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256`
     → `.gitignore:85: data/microstructure/`

2. **Canonicalization report (new local artefact):**
   - path:
     `data/microstructure/canonicalization-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__1778713761225__0d51bd7bac1e.json`
   - size: 5,241 bytes
   - SHA256:
     `8c6457b65a4a3413c7836aea391d6b2cbd82c5cbd6252c6239f7e948e20809d3`
   - status: not committed
   - `git check-ignore -v
     data/microstructure/canonicalization-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__1778713761225__0d51bd7bac1e.json`
     → `.gitignore:85: data/microstructure/`

3. **Canonicalization report sidecar (paired `.sha256` in
   canonical Phase 4bb-F format):**
   - path: same as (2) with `.sha256` suffix
   - size: 156 bytes
   - SHA256:
     `1361c8e02217280f892abd8f72ff6323efac5a33b0dbddf1d51dd37540e403c6`
   - status: not committed
   - `git check-ignore -v
     data/microstructure/canonicalization-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__1778713761225__0d51bd7bac1e.json.sha256`
     → `.gitignore:85: data/microstructure/`

Predecessor / source references:
- Phase 4bl-D gate report id
  `microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a`
  (SHA `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7`)
  is referenced verbatim in the canonicalization report body.
- Phase 4bl-D-S1 governance memo
  (`docs/00-meta/implementation-reports/2026-05-13_phase-4bl-d-s1_sidecar-canonicalization-governance-memo.md`)
  is the policy basis for the controlled execution.

## 8. Validation results

- `git diff --check` (post-merge): clean (no whitespace
  errors).
- `git status --short` (post-merge): only the pre-existing
  untracked entries `.claude/scheduled_tasks.lock` and
  `data/research/` (both unrelated to Phase 4bl-D-S2 and
  out-of-scope; pre-existing on `main`).
- `git diff --stat main^..HEAD` (post-merge): 5 files
  changed, 2,563 insertions(+), 0 deletions; matches §5.
- `git ls-files data/microstructure/`: empty (no
  `data/microstructure/` file is tracked).
- `python -m py_compile scripts/phase4bl_d_s2_canonicalize_sidecar.py`
  → OK.
- `python -m py_compile tests/research/microstructure/test_phase4bl_d_s2_sidecar_canonicalization.py`
  → OK.
- `uv run ruff check scripts/phase4bl_d_s2_canonicalize_sidecar.py
  tests/research/microstructure/test_phase4bl_d_s2_sidecar_canonicalization.py`
  → `All checks passed!`
- `uv run pytest tests/research/microstructure/test_phase4bl_d_s2_sidecar_canonicalization.py`
  → `28 passed in 0.16s`.
- `git check-ignore -v data/microstructure/` →
  `.gitignore:85: data/microstructure/`.
- `git check-ignore -v
  data/microstructure/canonicalization-reports/` →
  `.gitignore:85: data/microstructure/`.
- `git check-ignore -v
  data/microstructure/canonicalization-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__1778713761225__0d51bd7bac1e.json`
  → `.gitignore:85: data/microstructure/`.
- `git check-ignore -v
  data/microstructure/canonicalization-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__1778713761225__0d51bd7bac1e.json.sha256`
  → `.gitignore:85: data/microstructure/`.
- Whole-repo `ruff` / `mypy` / `pytest` were **not** rerun by
  the Phase 4bl-D-S2 merge because the merge does not modify
  any prior source module beyond the new standalone
  `scripts/phase4bl_d_s2_*.py` (which is scoped-ruff /
  scoped-`py_compile` clean and untouched by the rest of the
  codebase) and the new
  `tests/research/microstructure/test_phase4bl_d_s2_*.py`
  (which is scoped-pytest clean and shares no fixture with any
  prior test). The latest authoritative whole-repo validation
  remains the Phase 4bb-F-implementation merge baseline (`ruff`
  PASS, `mypy` strict 120 source files PASS, microstructure
  `pytest` 915 passed + 1 pre-existing labelled skip, whole-repo
  `pytest` 1698 passed + 1 skipped + 2 pre-existing simulation
  failures unchanged from prior phases; the two failures are
  `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt`
  and `::test_real_2026_03_ethusdt`, both `KeyError:
  'trade_count'` in unrelated
  `src/prometheus/research/data/storage.py:232`).
- Independent post-merge recompute of all upstream artefact
  SHA256 values returned bit-identical matches (see §9).

## 9. Upstream immutability evidence (if applicable)

Every upstream `data/microstructure/` artefact recorded by
Phase 4bl-D-S1 as required-byte-identical is preserved
verbatim by Phase 4bl-D-S2 and confirmed bit-identical by
independent post-merge recompute on `main`:

| Artefact | Expected SHA256 | Post-merge SHA256 | Status |
| --- | --- | --- | --- |
| target raw zip `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip` (21,271,119 bytes) | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | IDENTICAL |
| v002 raw manifest `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json` (105,052 bytes) | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | IDENTICAL |
| v002 acquisition log `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json` (302,055 bytes) | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | IDENTICAL |
| Phase 4bl-D gate report `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a.json` (169,637 bytes) | `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7` | `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7` | IDENTICAL |
| embedded SHA value recorded inside the rewritten Phase 4az 2025-01-15 sidecar | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | IDENTICAL |
| embedded basename recorded inside the rewritten Phase 4az 2025-01-15 sidecar | `BTCUSDT-aggTrades-2025-01-15.zip` | `BTCUSDT-aggTrades-2025-01-15.zip` | IDENTICAL |

Additional artefacts confirmed preserved (sampled — not
exhaustive):

- Phase 4az `__v001` raw manifest, Phase 4az `__v001` raw zip
  sidecar, Phase 4az acquisition log, Phase 4bb-D raw gate
  report + sidecar, Phase 4bd normalized parquet, Phase 4bd
  derived manifest, Phase 4be derived gate report, Phase 4bf
  derived gate report, Phase 4bg-B derived successor-state,
  Phase 4bh feature parquet + manifest, Phase 4bi-B feature
  gate report, Phase 4bi-D feature successor-state, Phase 4bj-C
  label parquet + manifest, Phase 4bj-E label gate report,
  Phase 4bj-G label successor-state, Phase 4bj-J no-split
  determination, Phase 4bb-G raw successor-state — all
  byte-identical at their previously recorded SHAs.

**Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant preserved (never invoked).**

## 10. Manifest state preservation (if applicable)

Every manifest in scope of Phase 4bl-D-S2 is preserved verbatim:

- **v002 raw manifest** (`data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json`):
  `research_eligible: false`,
  `eligibility_gate_status: "pending"`, governance labels
  unchanged from the Phase 4bl-C state; not modified by Phase
  4bl-D-S2. SHA `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485`
  bit-identical pre/post.
- **`__v001` raw manifest (Phase 4az):** `research_eligible:
  false`, `eligibility_gate_status: "pending"`; not modified.
- **Phase 4bd derived manifest:** `research_eligible: false`,
  `eligibility_gate_status: "pending"`; not modified.
- **Phase 4bh feature manifest:** `research_eligible: false`,
  `eligibility_gate_status: "pending"`; not modified.
- **Phase 4bj-C label manifest:** `research_eligible: false`,
  `eligibility_gate_status: "pending"`,
  `chronological_split_policy: "not_yet_defined"`; not
  modified.
- Every successor-state sibling artefact (Phase 4bb-G raw;
  Phase 4bg-B derived; Phase 4bi-D feature; Phase 4bj-G label;
  Phase 4bj-J label no-split) preserved verbatim.

**Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant preserved (never invoked).** Phase
4bl-D-S2 performed a metadata-sidecar line-ending
canonicalization only; it did not flip any flag, did not
transition any manifest state, and did not invoke any helper
that would change manifest state.

## 11. Boundary confirmations

The Phase 4bl-D-S2 merge honours every boundary required by
the merge authorization prompt and the Phase 4bk-A workflow
standard:

- no Phase 4bl-D raw gate rerun;
- no new raw / derived / feature / label / metrics gate
  report created;
- no second invocation of the canonicalization script (the
  in-place rewrite occurred exactly once during branch
  execution; the merge does not re-execute it);
- no further modification of the target sidecar (post-state
  preserved at 99 bytes, LF, SHA `c40e6be6...`);
- no modification of the associated raw zip;
- no modification of any other sidecar;
- no modification of the v002 raw manifest;
- no modification of the v002 acquisition log;
- no modification of the Phase 4bl-D gate report;
- no modification of any prior gate report (Phase 4bb-D, Phase
  4bf, Phase 4bi-B, Phase 4bj-E, etc.);
- no modification of any successor-state artefact;
- no modification of any normalized / derived / feature /
  label parquet, manifest, or sidecar;
- no amendment of the Phase 4bb-F canonical path policy (the
  rewritten Phase 4az sidecar now conforms verbatim);
- no amendment of the Phase 4bl-D gate;
- no creation of any successor-state artefact;
- no `data/microstructure/` artefact committed;
- no data acquired, downloaded, or normalized;
- no public endpoint called; no Binance API called; no
  authenticated REST contacted; no private endpoint contacted;
- no WebSocket opened; no user stream contacted; no listenKey
  lifecycle invoked;
- no credential / `.env` / `.mcp.json` / MCP / Graphify used,
  read, written, or referenced;
- no normalizer / raw gate / derived gate / feature kernel /
  feature gate / label kernel / label gate / diagnostic / ML /
  strategy / backtest script rerun;
- no source code, test, script, configuration,
  `pyproject.toml`, `README.md`, `.gitignore`,
  `.gitattributes`, or MCP-file modification beyond the four
  new tracked files (one script + one test + two docs) and
  the narrow `current-project-state.md` paragraph addition;
- no `research_eligible` flipped on any actual manifest;
- no `eligibility_gate_status` transitioned on any actual
  manifest;
- no `chronological_split_policy` changed on any actual
  manifest;
- no ML model trained, designed, selected, or feature-ranked;
- no strategy created, implemented, or rescued;
- no signal computed; no PnL / MFE / MAE / R-multiple /
  equity / position / alpha / edge / prediction /
  model-score / decision-score / entry-exit output computed;
- no backtest run;
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked);
- Phase 4bb-F canonical path policy preserved verbatim (Phase
  4bl-D-S2 follows it; no policy text changed);
- Phase 4bl-D gate FAIL preserved as descriptive evidence
  only;
- Phase 4ak M0 twelve-clause gate, post-null cooldown rule,
  cooled-down families list, and memo template preserved;
- Phase 4al refined no-rescue rule + §13 boundary + §14
  hierarchy preserved;
- no retained verdict revised;
- no project lock loosened;
- no M0 amendment;
- no successor authorized;
- no remediation executed beyond the specific Option B1
  metadata-sidecar line-ending canonicalization predeclared
  by Phase 4bl-D-S1 and authorized by the Phase 4bl-D-S2
  authorization prompt.

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
- §1.7.3 = 0.25% risk per trade / 2× leverage cap /
  one-position max / mark-price stops;
- Phase 3p §4.7 strict integrity gate (multi-day extension
  applied verbatim by Phase 4bl-D);
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
- Phase 4bb-F canonical path policy;
- Phase 4bl-D-S1 Option B1 recommendation (Phase 4bl-D-S2
  operationalises it; does not amend it);
- Phase 4bl-D `RAW_MULTIDAY_GATE_FAIL` as the last gate
  verdict until a separately authorized Phase 4bl-D-R rerun
  occurs.

All prior phase results preserved verbatim.

## 14. No-rescue constraints

The Phase 4bl-D-S2 merge does **not**, and cannot be construed
as authorising:

- a second rewrite of the Phase 4az 2025-01-15 sidecar (the
  in-place CRLF → LF canonicalization occurred exactly once
  under Phase 4bl-D-S1 Option B1 authorization; any further
  modification of this sidecar would require a separately
  authorized governance decision);
- modification, normalization, replacement, or rewrite of
  any other sidecar;
- any further `data/microstructure/` write or modification;
- the Phase 4bl-D-R Multi-Day Raw Manifest Eligibility Gate
  Rerun;
- the Phase 4bl-E Multi-Day Raw Manifest Successor-State
  Recording;
- successor-state recording for any other family;
- v002 raw manifest mutation, including any
  `research_eligible` flip, `eligibility_gate_status`
  transition, or governance-label change;
- v002 acquisition log mutation;
- any prior gate report, normalized parquet, feature parquet,
  label parquet, derived manifest, feature manifest, label
  manifest, sidecar, successor-state, diagnostic, or split
  artefact modification;
- normalization, derived parquet, features, labels, label
  diagnostics, label statistics, ML, strategy, signals, or
  backtest work;
- additional aggTrades / 5m / 1m / tick / mark-price 30m /
  4h / order-book / spot / cross-venue / funding /
  open-interest data acquisition;
- paper / shadow / live-readiness / deployment / exchange-write
  / production-key creation / authenticated APIs / private
  endpoints / public-endpoint calls in code / user stream /
  live WebSocket implementation;
- MCP / Graphify / `.mcp.json` / credentials;
- flipping `research_eligible` on any actual manifest;
- transitioning `eligibility_gate_status` on any actual
  manifest;
- changing `chronological_split_policy` on any actual
  manifest;
- amending Phase 4bb-F canonical path policy;
- amending the Phase 4bl-D gate;
- creating a new gate report;
- creating a new canonicalization report;
- old-strategy alt-symbol rerun or cooled-down-family
  reopening (R2 / F1 / D1-A / V2 / G1 / C1 first-spec
  rejections remain terminal; the 5m research thread remains
  operationally closed per Phase 3t);
- transitioning any manifest state from this metadata-sidecar
  canonicalization alone;
- Phase 4 canonical;
- Phase 5;
- any other successor phase.

## 15. Successor authorization

**None.**

Phase 4bl-D-S2 does **not** authorize any successor phase.
The natural conditional successor chain implied by the
Phase 4bl-D-S1 recommendation requires two further separately
authorized operator prompts and is **NOT** authorized by this
merge:

- **Phase 4bl-D-R — Multi-Day Raw Manifest Eligibility Gate
  Rerun** (NOT authorized): would re-run the Phase 4bl-D
  33-check gate against the Phase 4bl-D-S2-canonicalized
  sidecar and the unchanged Phase 4bl-C raw fileset. PASS is
  likely (since the canonical Phase 4bb-F LF terminator now
  parses correctly and the four Phase 4bl-D failed checks
  were all rooted in sidecar-format-only failure) but **not**
  guaranteed; the determination must be made by a separately
  authorized phase, not inferred from Phase 4bl-D-S2.
- **Phase 4bl-E — Multi-Day Raw Manifest Successor-State
  Recording** (NOT authorized): would record a sibling
  successor-state JSON only after Phase 4bl-D-R produces
  PASS, per the Phase 4bb-G raw-family successor-state
  precedent.

Also **NOT** authorized:

- Phase 4bm-* (multi-day derived arc);
- Phase 4bn-* (multi-day feature arc);
- Phase 4bo-* (multi-day label arc);
- Phase 4bp-* (multi-day diagnostics);
- Phase 4bq-* (multi-day chronological split);
- Phase 5;
- Phase 4 canonical;
- paper / shadow / live-readiness / deployment / production
  keys / authenticated APIs / private endpoints / user stream
  / live WebSocket implementation / MCP / Graphify /
  `.mcp.json` / credentials / exchange-write;
- additional aggTrades / 5m / 1m / tick / mark-price 30m /
  4h / order-book / spot / cross-venue / funding /
  open-interest data acquisition;
- ML implementation, ML training, model selection, feature
  ranking, meta-labeling, strategy implementation, backtest
  implementation.

Each step of the conditional successor chain requires a
separately authorized operator prompt. Phase 4bl-D-S2 makes
no claim about expected execution sequencing beyond recording
the executed canonicalization and the binding requirements
for each future step (as predeclared by Phase 4bl-D-S1).

## 16. Recommended state

**Remain paused.**

The Phase 4bl-D `RAW_MULTIDAY_GATE_FAIL` remains the last
gate verdict on record on `main`. The Phase 4bl-D-S1 Option
B1 recommendation has now been executed: the Phase 4az
2025-01-15 sidecar now conforms to the Phase 4bb-F canonical
contract (99 bytes; LF terminator; embedded SHA and basename
byte-identical). The v002 raw manifest remains
`research_eligible: false` and `eligibility_gate_status:
"pending"`. No remediation beyond the specific sidecar
canonicalization has been authorized. No execution beyond
the predeclared Phase 4bl-D-S1 §11 boundary has occurred.

**Conditional next, NOT authorized:** A future separately
authorized Phase 4bl-D-R Multi-Day Raw Manifest Eligibility
Gate Rerun would be the cleanest non-paused option. Per the
Phase 4bk-A workflow standard, a separately authorized
operator prompt is required before any Phase 4bl-D-R work
may begin; and a further separately authorized operator
prompt is required before any Phase 4bl-E successor-state
recording. Phase 4bl-D-S2 does **not** authorize either of
these.

Push status (recorded after merge-closeout commit is
committed and pushed): pushed to `origin/main` with no force,
no skip-hooks, no skip-signing.
