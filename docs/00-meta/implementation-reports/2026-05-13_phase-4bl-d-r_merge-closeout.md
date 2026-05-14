# Phase 4bl-D-R — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bl-D-R — Multi-Day Raw Manifest Eligibility Gate
  Rerun
- **Type:** docs + tiny standalone wrapper script + offline tests +
  one local gitignored raw gate-rerun report (with paired SHA256
  sidecar)
- **Action:** merge into `main`
- **Merge purpose:** record on `main` the Phase 4bl-D-R rerun of the
  full 33-check Phase 4bl-D raw eligibility-gate protocol against the
  unchanged Phase 4bl-C v002 90-day BTCUSDT aggTrades dataset with
  the Phase 4bl-D-S2-canonicalised 2025-01-15 sidecar in place. The
  rerun produced **`RAW_MULTIDAY_GATE_PASS`** — 33 / 33 PASS / 0 FAIL
  / 0 ERROR / 0 NA — with full per-row Phase 4ax
  `validate_aggtrade_payload` validation across all 155,153,449 rows
  and exact aggregate recomputation matching the manifest. The four
  previously failing Phase 4bl-D checks now pass; the remaining 29
  Phase 4bl-D PASS checks remain PASS. The merge does **not** re-run
  the gate, does **not** create a new gate report, does **not**
  modify the Phase 4bl-D gate script, does **not** weaken any of the
  33 Phase 4bl-D checks, does **not** relax the sidecar parser, does
  **not** amend the Phase 4bb-F canonical path policy, does **not**
  modify any sidecar / raw zip / manifest / acquisition log / prior
  gate report / successor-state, does **not** create a
  successor-state artefact, does **not** transition any manifest
  state, and does **not** authorise any successor phase.
- **Target branch:** `main`
- **Source branch:**
  `phase-4bl-d-r/multi-day-raw-manifest-eligibility-gate-rerun`

## 2. SHAs

- **`main` SHA before merge:** `69e4528`
  (`69e45280f080e320171f1d851933fdb13213aaea`; Phase 4bl-D-S2
  merge-closeout commit `docs(phase-4bl-d-s2): add merge closeout`;
  `main` and `origin/main` both at this SHA before the merge began).
- **Branch commit SHA (Phase 4bl-D-R):**
  - `4d5a1c1` — `feat(phase-4bl-d-r): multi-day raw manifest
    eligibility gate rerun`
    (`4d5a1c182096d76733a580ce0f79e00c20425a13`; single tracked
    commit on the branch; adds the standalone wrapper script +
    offline tests + implementation report + closeout, and modifies
    `docs/00-meta/current-project-state.md`).
- **Merge commit SHA:**
  `8c5309b2e22a11685cab2c7dc56ed5529d83badc`
  (`feat(phase-4bl-d-r): merge multi-day raw manifest eligibility
  gate rerun`; created by `git merge --no-ff` with the default `ort`
  strategy on `main`).
- **Final `main` / `origin/main` SHA after merge-closeout commit
  and push:** to be filled at commit time of this merge-closeout
  file. The canonical `main` anchor for Phase 4bl-D-R
  project-completion is the merge-closeout commit (this file's
  commit) on `main`, recorded after push. Per Phase 4bk-A
  workflow-standard convention, any future one-commit SHA-chain
  fixup that records the final-`main` SHA value into this §2
  placeholder is optional, separately authorized, and does not
  change Phase 4bl-D-R lifecycle semantics.

## 3. Merge method

- `git merge --no-ff` with the default `ort` strategy.
- Merge commit message header:
  `feat(phase-4bl-d-r): merge multi-day raw manifest eligibility
  gate rerun`.
- Body explicitly records: gate result (33 / 33 PASS;
  `RAW_MULTIDAY_GATE_PASS`; row count 155,153,449; size
  1,943,823,208 bytes); the four previously failing Phase 4bl-D
  checks now PASS; tracked files (5 — script + tests + main memo
  + closeout + narrow `current-project-state.md` update); local
  gitignored gate-rerun report path and SHAs (NOT committed); six
  upstream artefacts byte-identical pre/post; manifest state
  preserved verbatim (`research_eligible: false`,
  `eligibility_gate_status: "pending"`); `eligibility_gate_status_after
  = pass_report_level_only` (report-level only; no on-disk
  manifest transition); Phase 4aw
  `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked); full `did NOT`
  enumeration (no gate rerun during merge; no new gate report; no
  Phase 4bl-D gate script modification; no check weakening; no
  sidecar parser relaxation; no Phase 4bb-F amendment; no data
  acquisition; no normalization / derivation / features / labels /
  diagnostics / ML / strategy / signals / backtest; no manifest
  mutation; no `research_eligible` flip; no
  `eligibility_gate_status` transition on the actual manifest; no
  `chronological_split_policy` change; no retained-verdict
  revision; no project-lock change; no M0 amendment; no successor
  authorization); recommended state remain paused; conditional
  next (NOT authorized) = Phase 4bl-E Multi-Day Raw Manifest
  Successor-State Recording.
- No `--no-verify`. No `--no-gpg-sign`. No
  `-c commit.gpgsign=false`. No force-push.
- Push status: pushed to `origin/main` with no force, no
  skip-hooks, no skip-signing (recorded once the merge-closeout
  commit is pushed; see §16).

## 4. Files brought forward by the merge

### Docs (tracked)

- `docs/00-meta/current-project-state.md` — narrow update:
  inserted a new Phase 4bl-D-R narrative paragraph immediately
  before the existing Phase 4bl-D-S2 paragraph and replaced the
  prior "Current phase:" block with a new Phase 4bl-D-R block,
  preserving the prior Phase 4bl-D-S2 "Current phase:" block as
  historical context (391 insertions).
- `docs/00-meta/implementation-reports/2026-05-13_phase-4bl-d-r_multi-day-raw-manifest-eligibility-gate-rerun.md`
  (new; 628 insertions) — the Phase 4bl-D-R implementation
  report.
- `docs/00-meta/implementation-reports/2026-05-13_phase-4bl-d-r_closeout.md`
  (new; 183 insertions) — the Phase 4bl-D-R branch closeout.

### Source / tests / scripts / config / runtime

- `scripts/phase4bl_d_r_rerun_raw_gate.py` (new; 474 insertions) —
  thin standalone wrapper around the existing Phase 4bl-D gate
  script. Python standard library + the Phase 4bl-D gate module
  loaded by file path via `importlib.util.spec_from_file_location`
  (with `sys.modules` registration so `@dataclass` resolves
  `cls.__module__`); no `requests`/`httpx`/`aiohttp`/`urllib3`/
  `socket`/`websockets`/`binance`/`dotenv` imports; no network
  I/O; no credentials; no `.env`; no `.mcp.json`; no MCP /
  Graphify; no exchange adapters; no
  `prometheus.runtime`/`execution`/`persistence` imports. The
  wrapper monkey-patches exactly three module-level identity
  constants (`PHASE_ID`, `PHASE_NAME`, `ARTEFACT_TYPE`) and two
  entries of the gate's `GOVERNANCE_LABELS` dict in place
  (`phase = "4bl-d-r"`, `source_phase_boundary = "4bl-D-S2"`)
  before invoking `gate.run_gate(...)` exactly once. The wrapper
  reads back the gate-produced JSON, augments it in memory via a
  pure `augment_report(...)` function, deletes the gate's own
  outputs, and atomically rewrites both with the augmented report
  using deterministic sorted-key JSON and a paired SHA256 sidecar
  in canonical Phase 4bb-F format. Defence-in-depth: refuses to
  rewrite any file whose filename does not contain
  `phase-4bl-d-r`. Ruff clean; `py_compile` clean.
- `tests/research/microstructure/test_phase4bl_d_r_gate_rerun.py`
  (new; 438 insertions) — 23 offline pytest cases using pytest
  `tmp_path` only; verify locked identity constants;
  `augment_report` purity; verbatim preservation of `checks`,
  per-file summary, aggregate summary, `governance_labels`,
  `non_authorizations`, retained verdict ledger, preserved
  locks; predeclared predecessor and remediation lineage values;
  deterministic sorted-key JSON serialisation; and static
  forbidden-import + forbidden-runtime-token scans. All 23 pass.

No `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`,
MCP file, or runtime-configuration file was modified by this
merge.

The Phase 4bl-D gate script
(`scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py`)
was **not** modified.

### `data/microstructure/`

None. **No `data/microstructure/` file was modified by this
merge.** The merge introduces zero tracked changes under
`data/microstructure/`. The Phase 4bl-D-R gate-rerun report
(`data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json`)
and its paired `.sha256` sidecar remain gitignored under
`.gitignore:85: data/microstructure/` and are not part of the
merge commit. No raw zip, no sidecar, no manifest, no
acquisition log, no Phase 4bl-D gate report, no Phase 4bl-D-S2
canonicalisation report, no successor-state file, no normalized
parquet, no derived manifest, no feature parquet, no feature
manifest, no label parquet, no label manifest, no diagnostic,
and no split artefact was modified.

### Prior governance memos

None. No prior governance memo (Phase 3p §4.7; Phase 3r §8;
Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k;
Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0; Phase 4al
no-rescue; Phase 4aw `flip_research_eligible(...)` invariant;
Phase 4bb-F canonical path policy; Phase 4bl-A; Phase 4bl-B;
Phase 4bl-C; Phase 4bl-D; Phase 4bl-D-S1; Phase 4bl-D-S2) was
modified beyond the narrow `current-project-state.md` paragraph
addition.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 391 +++++++++++++
 .../2026-05-13_phase-4bl-d-r_closeout.md           | 183 ++++++
 ...ulti-day-raw-manifest-eligibility-gate-rerun.md | 628 +++++++++++++++++++++
 scripts/phase4bl_d_r_rerun_raw_gate.py             | 474 ++++++++++++++++
 .../microstructure/test_phase4bl_d_r_gate_rerun.py | 438 ++++++++++++++
 5 files changed, 2114 insertions(+)
```

The diff matches the expected change set from the Phase 4bl-D-R
merge authorization prompt exactly: five tracked files (one narrow
modification + four new files), zero deletions, 2,114 insertions
total. No file outside the five documented files is in the diff.
No `data/microstructure/` file appears. No prior source / test /
script was modified. The Phase 4bl-D gate script remains untouched.

## 6. Verdict

**GATE PASS — `RAW_MULTIDAY_GATE_PASS` recorded as report-level
evidence only.**

Phase 4bl-D-R is project-complete on `main` after the
merge-closeout commit is recorded and pushed. The Phase 4bl-D-R
rerun executed the full 33-check Phase 4bl-D raw eligibility-gate
protocol verbatim (no protocol weakening; the existing
Phase 4bl-D gate script
`scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py` was
loaded and invoked unchanged via the thin wrapper) against the
unchanged Phase 4bl-C v002 90-day BTCUSDT aggTrades dataset with
the Phase 4bl-D-S2-canonicalised 2025-01-15 sidecar in place,
emitting verdict **`RAW_MULTIDAY_GATE_PASS`** — 33 / 33 PASS / 0
FAIL / 0 ERROR / 0 NA. Full per-row Phase 4ax
`validate_aggtrade_payload` ran across every row; recomputed
`total_row_count = 155,153,449` (matches manifest exactly);
recomputed `total_size_bytes = 1,943,823,208` (matches manifest
exactly); per-file validation summaries report `status = "pass"`
for all 90 dates; `all_schema_validation_errors_count = 0`;
`all_timestamp_boundary_errors_count = 0`;
`all_duplicate_agg_trade_id_errors_count = 0`;
`all_monotonicity_errors_count = 0`;
`adjacent_date_overlap_errors_count = 0`. The 2025-01-15 file's
per-row `validate_aggtrade_payload` pass count is 1,681,098
(matches the Phase 4az fixture row count exactly); the Phase
4bl-D shortfall of exactly 1,681,098 is fully recovered. The
four previously failing Phase 4bl-D checks
(`raw_zip_sidecar_integrity`, `per_file_row_count_consistency`,
`per_file_time_bounds_consistency`, `total_row_count_consistency`)
all PASS in Phase 4bl-D-R; the remaining 29 Phase 4bl-D PASS
checks remain PASS. Wall-clock: 893.984 seconds (~14.9 minutes),
consistent with the Phase 4bl-D first run (880.188 s). The PASS
is **report-level evidence only**. The v002 raw manifest remains
`research_eligible: false` and `eligibility_gate_status:
"pending"`; no on-disk manifest transition occurred. The Phase
4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant is preserved (never invoked). No
successor-state artefact was created. No Phase 4bb-F amendment
occurred. No Phase 4bl-D gate amendment occurred. The original
Phase 4bl-D FAIL gate report remains byte-identical at its
previously recorded path and SHA, preserved as historical
evidence. The Phase 4bl-D-S2 canonicalisation report remains
byte-identical at its previously recorded path and SHA,
preserved as historical evidence. No remediation,
normalization, derived parquet, feature, label, diagnostic, ML,
strategy, signal, backtest, paper / shadow, live-readiness,
deployment, exchange-write, production-key creation,
authenticated APIs, private endpoints, user stream, WebSocket
implementation, MCP, Graphify, `.mcp.json`, or credential work
has been authorized or performed.

## 7. Local gitignored outputs (if any)

Phase 4bl-D-R produced exactly two local gitignored artefacts
under `data/microstructure/gate-reports/raw/`. Neither is
committed.

1. **Phase 4bl-D-R augmented gate-rerun report:**
   - path:
     `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json`
   - size: 171,342 bytes
   - SHA256:
     `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46`
   - status: not committed
   - `git check-ignore -v
     data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json`
     → `.gitignore:85: data/microstructure/`

2. **Phase 4bl-D-R paired SHA256 sidecar (canonical Phase 4bb-F
   format `<sha>  <basename>\n`; two spaces; trailing LF):**
   - path: same as (1) with `.sha256` suffix
   - size: 155 bytes
   - SHA256:
     `84f37b7b424d67dfa0dae06bb51279354b5b37998beb4f9b1cf6b6f617dd8c02`
   - status: not committed
   - sidecar parses to a token that matches the recomputed
     gate-rerun report SHA bit-for-bit
   - `git check-ignore -v
     data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json.sha256`
     → `.gitignore:85: data/microstructure/`

Predecessor / source references (recorded verbatim inside the
augmented gate-rerun report body):

- Phase 4bl-D predecessor gate report id
  `microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a`
  (SHA `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7`).
- Phase 4bl-D-S2 canonicalisation report id
  `microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__1778713761225__0d51bd7bac1e`
  (SHA `8c6457b65a4a3413c7836aea391d6b2cbd82c5cbd6252c6239f7e948e20809d3`).
- Phase 4az 2025-01-15 raw zip SHA
  `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`.
- Phase 4bl-D-S2 canonicalised 2025-01-15 sidecar SHA
  `c40e6be60753a912063d9a5f5c1617ba31ec987c09121c50adab3ba0226018fc`
  (99 bytes; LF).
- Phase 4bl-C v002 raw manifest SHA
  `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485`.
- Phase 4bl-C v002 acquisition log SHA
  `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314`.

## 8. Validation results

- `git diff --check` (post-merge): clean (no whitespace errors).
- `git status --short` (post-merge): only the pre-existing
  untracked entries `.claude/scheduled_tasks.lock` and
  `data/research/` (both unrelated to Phase 4bl-D-R and
  out-of-scope; pre-existing on `main`).
- `git diff --stat main^..HEAD` (post-merge): 5 files changed,
  2,114 insertions(+), 0 deletions; matches §5.
- `git ls-files data/microstructure/`: empty (no
  `data/microstructure/` file is tracked).
- `python -m py_compile scripts/phase4bl_d_r_rerun_raw_gate.py`
  → OK.
- `python -m py_compile tests/research/microstructure/test_phase4bl_d_r_gate_rerun.py`
  → OK.
- `uv run ruff check scripts/phase4bl_d_r_rerun_raw_gate.py
  tests/research/microstructure/test_phase4bl_d_r_gate_rerun.py`
  → `All checks passed!`
- `uv run pytest tests/research/microstructure/test_phase4bl_d_r_gate_rerun.py`
  → `23 passed in 0.07s`.
- `git check-ignore -v data/microstructure/` →
  `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/gate-reports/` →
  `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/gate-reports/raw/` →
  `.gitignore:85: data/microstructure/`.
- `git check-ignore -v
  data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json`
  → `.gitignore:85: data/microstructure/`.
- `git check-ignore -v
  data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json.sha256`
  → `.gitignore:85: data/microstructure/`.
- The Phase 4bl-D-R gate was **not** rerun during the merge
  (per merge authorization). The single gate execution recorded
  on the branch was performed exactly once during Phase 4bl-D-R
  branch work and produced the report whose SHA is recorded in
  §7 above; that SHA was recomputed bit-identical post-merge.
- Whole-repo `ruff` / `mypy` / whole-repo `pytest` were **not**
  rerun by the Phase 4bl-D-R merge because the merge does not
  modify any prior source module (the Phase 4bl-D gate script
  itself is unchanged; the new
  `scripts/phase4bl_d_r_rerun_raw_gate.py` is a thin standalone
  wrapper which is scoped-ruff / scoped-`py_compile` clean and
  untouched by the rest of the codebase) and does not modify any
  prior test (the new
  `tests/research/microstructure/test_phase4bl_d_r_gate_rerun.py`
  is scoped-pytest clean and shares no fixture with any prior
  test). The latest authoritative whole-repo validation remains
  the Phase 4bb-F-implementation merge baseline (`ruff` PASS,
  `mypy` strict 120 source files PASS, microstructure `pytest`
  915 passed + 1 pre-existing labelled skip, whole-repo `pytest`
  1698 passed + 1 skipped + 2 pre-existing simulation failures
  unchanged from prior phases; the two failures are
  `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt`
  and `::test_real_2026_03_ethusdt`, both
  `KeyError: 'trade_count'` in unrelated
  `src/prometheus/research/data/storage.py:232`).
- Independent post-merge recompute of all upstream artefact
  SHA256 values returned bit-identical matches (see §9).

## 9. Upstream immutability evidence (if applicable)

Every upstream `data/microstructure/` artefact recorded by the
Phase 4bl-D-R authorization prompt as required-byte-identical is
preserved verbatim by the Phase 4bl-D-R merge and confirmed
bit-identical by independent post-merge recompute on `main`:

| Artefact | Expected SHA256 | Post-merge SHA256 | Status |
| --- | --- | --- | --- |
| target raw zip `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip` (21,271,119 bytes) | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | IDENTICAL |
| canonicalised 2025-01-15 sidecar `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256` (99 bytes; LF) | `c40e6be60753a912063d9a5f5c1617ba31ec987c09121c50adab3ba0226018fc` | `c40e6be60753a912063d9a5f5c1617ba31ec987c09121c50adab3ba0226018fc` | IDENTICAL |
| v002 raw manifest `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json` (105,052 bytes) | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | IDENTICAL |
| v002 acquisition log `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json` (302,055 bytes) | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | IDENTICAL |
| Phase 4bl-D original gate report `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a.json` (169,637 bytes) | `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7` | `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7` | IDENTICAL |
| Phase 4bl-D-S2 canonicalisation report `data/microstructure/canonicalization-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__1778713761225__0d51bd7bac1e.json` (5,241 bytes) | `8c6457b65a4a3413c7836aea391d6b2cbd82c5cbd6252c6239f7e948e20809d3` | `8c6457b65a4a3413c7836aea391d6b2cbd82c5cbd6252c6239f7e948e20809d3` | IDENTICAL |

The Phase 4bl-D-R gate-rerun report and paired sidecar
themselves are also confirmed byte-identical post-merge:

| Artefact | Expected SHA256 | Post-merge SHA256 | Status |
| --- | --- | --- | --- |
| Phase 4bl-D-R gate-rerun report (171,342 bytes) | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` | IDENTICAL |
| Phase 4bl-D-R gate-rerun sidecar (155 bytes) | `84f37b7b424d67dfa0dae06bb51279354b5b37998beb4f9b1cf6b6f617dd8c02` | `84f37b7b424d67dfa0dae06bb51279354b5b37998beb4f9b1cf6b6f617dd8c02` | IDENTICAL |

Additional artefacts confirmed preserved by independent
post-merge tree state (sampled — not exhaustive):

- Phase 4az `__v001` raw manifest, Phase 4az `__v001` raw zip
  sidecar (now in canonical LF form per Phase 4bl-D-S2), Phase
  4az acquisition log, Phase 4bb-D raw gate report + sidecar,
  Phase 4bd normalized parquet, Phase 4bd derived manifest,
  Phase 4be derived gate report, Phase 4bf derived gate report,
  Phase 4bg-B derived successor-state, Phase 4bh feature parquet
  + manifest, Phase 4bi-B feature gate report, Phase 4bi-D
  feature successor-state, Phase 4bj-C label parquet + manifest,
  Phase 4bj-E label gate report, Phase 4bj-G label
  successor-state, Phase 4bj-J no-split determination, Phase
  4bb-G raw successor-state — all preserved at their previously
  recorded SHAs.

**Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant preserved (never invoked).**

## 10. Manifest state preservation (if applicable)

Every manifest in scope of Phase 4bl-D-R is preserved verbatim:

- **v002 raw manifest** (`data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json`):
  `research_eligible: false`,
  `eligibility_gate_status: "pending"`, governance labels
  unchanged from the Phase 4bl-C state; not modified by Phase
  4bl-D-R. SHA
  `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485`
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
always-raises invariant preserved (never invoked).** The Phase
4bl-D-R gate-rerun report records
`eligibility_gate_status_after = "pass_report_level_only"` as a
report-level recommendation only; this value does not appear
on any on-disk manifest. No flag flip occurred; no manifest
transition occurred.

## 11. Boundary confirmations

The Phase 4bl-D-R merge honours every boundary required by the
merge authorization prompt and the Phase 4bk-A workflow
standard:

- the Phase 4bl-D-R gate was NOT rerun during the merge (the
  single gate execution occurred exactly once on the branch);
- no new gate report was created by the merge;
- no Phase 4bl-D gate script modification;
- no weakening of any of the 33 Phase 4bl-D checks;
- no sidecar parser relaxation (CRLF still rejected by the
  unchanged Phase 4bl-D gate's canonical parser);
- no Phase 4bb-F canonical path policy amendment (the Phase
  4bl-D-R gate-rerun report filename follows the policy verbatim:
  `<family>__<version>__phase-<id>__<unix_ms>__<short_commit>.json`
  with `phase-<id> = phase-4bl-d-r` lowercase under
  `gate-reports/raw/`);
- no modification of the canonicalised 2025-01-15 sidecar;
- no modification of any other sidecar;
- no modification of any raw zip;
- no modification of the v002 raw manifest;
- no modification of the v002 acquisition log;
- no modification of the Phase 4bl-D gate report;
- no modification of the Phase 4bl-D-S2 canonicalisation
  report;
- no modification of any prior gate report (Phase 4bb-D, Phase
  4bf, Phase 4bi-B, Phase 4bj-E, Phase 4bl-D, etc.);
- no modification of any successor-state artefact (Phase 4bb-G;
  Phase 4bg-B; Phase 4bi-D; Phase 4bj-G; Phase 4bj-J);
- no modification of any normalized / derived / feature / label
  parquet, manifest, or sidecar;
- no creation of any successor-state artefact;
- no `data/microstructure/` artefact committed (the gate-rerun
  report and paired sidecar remain gitignored under
  `.gitignore:85: data/microstructure/`);
- no data acquired, downloaded, or normalized;
- no public endpoint called; no `data.binance.vision` call; no
  Binance API called; no `fapi.binance.com` call; no
  `api.binance.com` call;
- no authenticated REST contacted; no private endpoint contacted;
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
  new tracked files (one wrapper script + one test file + two
  docs) and the narrow `current-project-state.md` paragraph
  addition;
- no `research_eligible` flipped on any actual manifest;
- no `eligibility_gate_status` transitioned on any actual
  manifest;
- no `chronological_split_policy` changed on any actual
  manifest;
- no derived / normalized parquet created;
- no feature parquet computed; no feature manifest created;
- no label parquet computed; no label manifest created;
- no label diagnostics run; no label statistics computed;
- no split artefact created;
- no returns / PnL / MFE / MAE / R-multiple / equity / position
  / alpha / edge / prediction / model-score / decision-score /
  entry-exit / strategy output computed;
- no ML model trained, designed, selected, or feature-ranked;
- no meta-labeling created;
- no strategy created, implemented, or rescued;
- no signal computed;
- no backtest run;
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked);
- Phase 4bb-F canonical path policy preserved verbatim (Phase
  4bl-D-R follows it; no policy text changed);
- Phase 4bl-D `RAW_MULTIDAY_GATE_FAIL` preserved as historical
  evidence — the Phase 4bl-D gate report and its sidecar
  remain byte-identical at their previously recorded SHAs;
- Phase 4bl-D-S2 canonicalisation outcome preserved as
  historical evidence — the canonicalisation report remains
  byte-identical at its previously recorded SHA;
- Phase 4ak M0 twelve-clause gate, post-null cooldown rule,
  cooled-down families list, and memo template preserved;
- Phase 4al refined no-rescue rule + §13 boundary + §14
  hierarchy preserved;
- no retained verdict revised;
- no project lock loosened;
- no M0 amendment;
- no successor authorized;
- no remediation executed beyond the Phase 4bl-D-S2 sidecar
  canonicalisation that occurred under separate operator
  authorization prior to Phase 4bl-D-R; Phase 4bl-D-R itself
  performed no remediation, only a rerun of the unchanged
  Phase 4bl-D gate protocol against the unchanged Phase 4bl-C
  fileset.

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
  applied verbatim by Phase 4bl-D; rerun verbatim by Phase
  4bl-D-R);
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
- Phase 4bl-D 33-check raw eligibility-gate protocol (rerun
  verbatim; no check weakened, added, removed, or relaxed);
- Phase 4bl-D-S1 Option B1 recommendation (operationalised by
  Phase 4bl-D-S2; preserved verbatim);
- Phase 4bl-D-S2 sidecar canonicalisation outcome (Phase
  4bl-D-R's rerun confirms the canonical LF sidecar parses
  correctly under the unchanged gate; preserved verbatim).

All prior phase results preserved verbatim.

## 14. No-rescue constraints

The Phase 4bl-D-R merge does **not**, and cannot be construed
as authorising:

- a second invocation of the Phase 4bl-D-R wrapper or the
  Phase 4bl-D gate (the rerun occurred exactly once during
  branch execution; the merge does not re-execute it; any
  further gate execution requires a separately authorized
  governance decision);
- modification, normalization, replacement, or rewrite of any
  sidecar, raw zip, manifest, acquisition log, gate report, or
  successor-state artefact;
- any further `data/microstructure/` write or modification;
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
- weakening any of the 33 Phase 4bl-D checks;
- relaxing the sidecar parser to accept CRLF;
- creating a new gate report;
- creating a new canonicalisation report;
- old-strategy alt-symbol rerun or cooled-down-family
  reopening (R2 / F1 / D1-A / V2 / G1 / C1 first-spec
  rejections remain terminal; the 5m research thread remains
  operationally closed per Phase 3t);
- transitioning any manifest state from this report-level
  PASS alone;
- Phase 4 canonical;
- Phase 5;
- any other successor phase.

## 15. Successor authorization

**None.**

Phase 4bl-D-R does **not** authorize any successor phase. The
natural conditional successor implied by the Phase 4bl-D-R PASS
result requires a further separately authorized operator prompt
and is **NOT** authorized by this merge:

- **Phase 4bl-E — Multi-Day Raw Manifest Successor-State
  Recording** (NOT authorized): would record a sibling
  successor-state JSON for the v002 raw manifest (analogous to
  the Phase 4bb-G successor-state recording for the Phase 4az
  `__v001` raw manifest), citing the Phase 4bl-D-R PASS gate
  report id and SHA, preserving the v002 raw manifest
  byte-identically (no `research_eligible` flip; no
  `eligibility_gate_status` transition on the actual manifest),
  and producing one local gitignored successor-state artefact
  + paired SHA256 sidecar under
  `data/microstructure/successor-state/`. Phase 4bl-D-R does
  **not** authorize Phase 4bl-E; a separately authorized
  operator prompt is required.

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

Each step requires a separately authorized operator prompt.
Phase 4bl-D-R makes no claim about expected execution
sequencing beyond recording the executed gate rerun and
preserving every retained verdict and project lock verbatim.

## 16. Recommended state

**Remain paused.**

The Phase 4bl-D-R rerun verdict **`RAW_MULTIDAY_GATE_PASS`** is
now the current gate verdict on record on `main`, superseding
the Phase 4bl-D FAIL as the latest gate run, but only at
report level. The original Phase 4bl-D FAIL gate report
remains byte-identical at its previously recorded path and SHA
and is preserved as historical evidence. The v002 raw manifest
remains `research_eligible: false` and `eligibility_gate_status:
"pending"`; no on-disk manifest transition has been authorized.
The canonicalised 2025-01-15 sidecar remains byte-identical at
its Phase 4bl-D-S2 post-state (99 bytes; LF; embedded SHA and
basename preserved verbatim). The 2025-01-15 raw zip remains
byte-identical. The v002 raw manifest, the v002 acquisition
log, and all upstream gate / canonicalisation reports remain
byte-identical. No remediation beyond the Phase 4bl-D-S2
sidecar canonicalisation (which occurred under separate
operator authorization) has been performed. Phase 4bl-D-R
itself performed only a rerun of the unchanged Phase 4bl-D
gate protocol; no remediation occurred during Phase 4bl-D-R.

**Conditional next, NOT authorized:** A future separately
authorized Phase 4bl-E Multi-Day Raw Manifest Successor-State
Recording would be the cleanest non-paused option. Per the
Phase 4bk-A workflow standard, a separately authorized
operator prompt is required before any Phase 4bl-E work may
begin. Phase 4bl-D-R does **not** authorize Phase 4bl-E.

Push status (recorded after merge-closeout commit is
committed and pushed): pushed to `origin/main` with no force,
no skip-hooks, no skip-signing.
