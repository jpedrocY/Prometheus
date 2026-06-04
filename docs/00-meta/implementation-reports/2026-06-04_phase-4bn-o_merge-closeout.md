# Phase 4bn-O — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bn-O — Normalization-Only Pre-V002 BTCUSDT aggTrades
  Segment Execution.
- **Type:** normalization-only / bounded local gitignored data-artefact
  generation / normalized manifest + sidecar generation / code + tests + docs.
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bn-O bounded normalization runner, its
  offline test module, implementation report, closeout, and the narrow
  `current-project-state.md` update onto `main` as project state. The 275
  normalized Parquet files + sidecars and the normalized segment manifest +
  sidecar produced by the run are **local gitignored artefacts only** and are
  **not** part of this (or any) commit.
- **Target branch:** `main`.
- **Source branch:** `phase-4bn-o/normalization-only-pre-v002-segment`.
- **Risk tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (full 16-section
  merge-closeout required).

## 2. SHAs

- **`main` SHA before merge:** `f55b47ff94637e72ebacc40f1a133a5526afaef6`
  (`docs(phase-4bn-n): finalize merge closeout shas`).
- **Branch commit SHA (code + tests + docs):**
  `814112cf96f8868480ba03da1c0fffc52f7b0ab4`
  (`data(phase-4bn-o): normalize pre-v002 aggtrades segment`).
- **Merge commit SHA:** `2c6c1789ed3b677229c741652699f27b16be21c5`
  (`data(phase-4bn-o): merge normalized pre-v002 segment`).
- **Merge-closeout commit SHA:** recorded in the SHA-finalization commit
  `docs(phase-4bn-o): finalize merge closeout shas` (see §"SHA finalization").
- **SHA-finalization commit SHA:** recorded in the SHA-finalization commit.
- **Final `main` / `origin/main` SHA after push:** recorded in the
  SHA-finalization commit.

## 3. Merge method

- `git merge --no-ff` with the default `ort` strategy.
- Merge commit message: `data(phase-4bn-o): merge normalized pre-v002 segment`.
- No `--no-verify`; no `--no-gpg-sign`; no `-c commit.gpgsign=false`; no
  force-push.
- Push status: pushed to `origin/main` with no force, no skip-hooks, no
  skip-signing (recorded at the final operator report after the
  SHA-finalization commit).

## 4. Files brought forward by the merge

- **Docs (3):**
  - `docs/00-meta/current-project-state.md` (modified — narrow Phase 4bn-O
    paragraph + new `Current phase:` block; prior Phase 4bn-A … 4bn-N
    paragraphs and blocks preserved verbatim as labelled historical context);
  - `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-o_normalization-only-pre-v002-segment.md`
    (added — implementation report, 23 sections);
  - `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-o_closeout.md`
    (added — branch closeout).
- **Scripts (1):** `scripts/phase4bn_o_normalize_pre_v002_aggtrades.py`
  (added — bounded normalization runner; reuses locked Phase 4bd primitives
  unchanged).
- **Tests (1):**
  `tests/research/microstructure/test_phase4bn_o_normalization_pre_v002.py`
  (added — 37 offline tests).
- **Source / config:** none.
- **`data/microstructure/` files:** **none modified or committed.** No
  `data/research/` file. No published manifest, sidecar, prior gate report,
  successor-state artefact, `.gitignore`, `pyproject.toml`, `README.md`, MCP
  file, or locked prior-phase script was modified.

The diff matches the expected change set from the merge authorization prompt
exactly (add 4 files, modify 1 doc).

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              |  110 ++
 .../2026-06-04_phase-4bn-o_closeout.md             |  195 +++
 ...se-4bn-o_normalization-only-pre-v002-segment.md |  424 +++++
 scripts/phase4bn_o_normalize_pre_v002_aggtrades.py | 1700 ++++++++++++++++++++
 .../test_phase4bn_o_normalization_pre_v002.py      |  853 ++++++++++
 5 files changed, 3282 insertions(+)
```

## 6. Verdict

**LOCAL ARTEFACT PRODUCED.** Phase 4bn-O succeeded fully
(`NORMALIZATION_SUCCEEDED__LOCAL_NORMALIZED_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`):
a bounded runner normalized the approved pre-v002 BTCUSDT Binance USDⓈ-M
futures aggTrades raw segment (2024-03-01 .. 2024-11-30 inclusive UTC; 275
dates; 400,001,695 events) into a phase-scoped normalized segment of the v002
family, producing 275 local gitignored normalized Parquet files + 275 canonical
sidecars and one non-eligible normalized segment manifest + sidecar, following
the Phase 4bn-N manifest/versioning convention and honouring the Phase 4bn-L
budget (no warning threshold and no hard cap crossed). All normalized outputs
remain local, gitignored, non-eligible, and uncommitted; `research_eligible`
remains `false`, `eligibility_gate_status` remains `pending`, and no manifest
eligibility transition occurred. The merge lands the code/tests/docs on `main`;
the project remains paused.

## 7. Local gitignored outputs (produced by Phase 4bn-O; NOT committed)

- **Normalized Parquet:** 275 files under
  `data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o/BTCUSDT/<YYYY>/<MM>/BTCUSDT-aggTrades-<YYYY-MM-DD>.parquet`;
  each with a paired canonical two-space `.sha256` sidecar (275 sidecars).
- **Segment manifest:**
  `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json`
  — SHA256 `0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa`.
- **Segment manifest sidecar:** `…_4bn_o.json.sha256` — SHA256
  `5d7dcbefbafcc81f2fcb1977ff9f35b08d58684542608317368c1f60f11e6402`
  (canonical two-space, LF, no BOM).
- **Aggregates:** total normalized footprint **3,954,532,918 B ≈ 3.68 GiB**;
  total events / rows **400,001,695**; runtime **3624.3 s ≈ 60.4 min**;
  temporary workspace peak **58,372,029 B ≈ 55.7 MiB**, post-cleanup **0 B**;
  `D:` free preflight **1,338,178,375,680 B ≈ 1246.3 GiB**, minimum observed
  **1,334,223,179,776 B ≈ 1242.6 GiB**; no warning thresholds crossed; no hard
  caps crossed; no fail-closed stop conditions triggered.
- **Not committed:** confirmed — all paths under `data/microstructure/` are
  gitignored (`git check-ignore -v data/microstructure/` → `.gitignore:85`);
  none staged or tracked.
- **Predecessor evidence:** Phase 4bn-J-R2 raw segment manifest
  (`…__v002_pre_v002_segment_4bn_j_r2.json`, SHA256 `1659e6da…3a3d1`); Phase
  4bn-K PASS gate report (SHA256 `051bed7b…20f9c24`,
  id `microstructure_raw_aggtrades_v001__v002__phase-4bn-k__1780436389489__cf7dc4f7e663`);
  raw acquisition log (SHA256 `0266210f…88bcf93`). All three recomputed and
  matched; all 275 raw zips + 275 raw sidecars verified.

## 8. Validation results

Re-run at merge review (no normalization rerun, no raw-gate rerun, no
acquisition, no endpoint):

- `git diff --check` → clean (no whitespace errors).
- `ruff check scripts/phase4bn_o_normalize_pre_v002_aggtrades.py tests/research/microstructure/test_phase4bn_o_normalization_pre_v002.py`
  → `All checks passed!`.
- `pytest tests/research/microstructure/test_phase4bn_o_normalization_pre_v002.py`
  → **37 passed**.
- `pytest …/test_normalize_io.py …/test_normalize_validation.py
  …/test_normalize_manifest.py …/test_phase4bm_b_multiday_normalization.py`
  → **71 passed** (no regression in the reused primitives).
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- **mypy:** `pyproject.toml` scopes mypy to `src/prometheus`. The new Phase
  4bn-O code lives under `scripts/` and `tests/`, outside mypy's configured
  scope; the runner imports the already-type-checked `src/prometheus` normalize
  primitives unchanged. The repo-standard mypy gate therefore does not cover
  this surface, and mypy was not run on `scripts/` (rationale recorded per the
  merge prompt's repository tooling note).
- Post-run filesystem verification (read-only): 275 parquets; 275 sidecars;
  manifest + sidecar present with the SHA256s in §7; canonical sidecar format;
  **0** `.duckdb`/`.sqlite`; **0** `v003` paths; **0** leftover `.tmp`
  companions; no `data/microstructure` / `data/research` artefact staged or
  tracked; published normalized `__v002` directory and manifest path-disjoint,
  never opened, never written.

## 9. Upstream immutability evidence

The merge review re-verified (during the Phase 4bn-O run) that all read-only
inputs were byte-identical pre/post normalization: the raw segment manifest
(`1659e6da…3a3d1`), the raw gate report (`051bed7b…20f9c24`), the raw
acquisition log (`0266210f…88bcf93`), all 275 raw zips, and all 275 raw zip
sidecars. The published normalized `__v002` family (directory + parquets +
`microstructure_normalized_aggtrades_v001__v002.json`) was **path-disjoint,
never opened, and never written** — immutable by construction (refuse-overwrite;
the runner never opens the published `__v002` manifest). The merge itself
modified no `data/microstructure/` artefact.

## 10. Manifest state preservation

- The Phase 4bn-O normalized **segment manifest** is seeded
  `research_eligible: false`, `eligibility_gate_status: "pending"`,
  `no_successor_authorization: true`; no transition occurred.
- The published normalized `__v002` manifest, the raw segment manifest, and all
  prior manifests are **unchanged** (`research_eligible` / `eligibility_gate_status`
  / `chronological_split_policy` / governance labels all unchanged).
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises
  invariant preserved (never invoked).

## 11. Boundary confirmations

- no source code modified; no test modified beyond the new added module; no
  locked prior-phase script modified;
- no `.gitignore`, `pyproject.toml`, `README.md`, or MCP file modified;
- no published manifest / sidecar / prior gate report / successor-state
  artefact modified;
- no `data/microstructure/` artefact committed; no `data/research/` artefact
  committed or created;
- no write into the published normalized `__v002/` directory; no mutation of
  `microstructure_normalized_aggtrades_v001__v002.json`;
- no v003 created; no `.duckdb` / `.sqlite` / database created; no Parquet
  compaction; no storage migration;
- no `research_eligible` flipped; no `eligibility_gate_status` /
  `chronological_split_policy` / `diagnostics_authorized` / `ml_authorized`
  transitioned;
- no normalizer rerun during merge review; no raw eligibility gate rerun; no
  acquisition; no endpoint / public / Binance / `data.binance.vision` call; no
  archive / CHECKSUM download; no HEAD preflight;
- no v002 terminal raw-window read; no sealed-test read; no published `__v002`
  parquet read;
- no feature kernel; no label kernel; no ML; no diagnostics; no strategy /
  signal / PnL / backtest;
- no credential / `.env` / `.mcp.json` / MCP / Graphify / WebSocket / user
  stream / private / authenticated endpoint used;
- Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved
  (never invoked);
- no retained verdict revised; no project lock loosened; no M0 amendment; no
  successor authorized.

## 12. Retained verdict ledger

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

All preserved verbatim.

## 13. Preserved project locks

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8
- Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down
  families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `flip_research_eligible(...)` always-raises invariant (never
  invoked)
- Phase 4bb-F canonical path + sidecar policy
- Phase 4bn-J-R1 raw-only cap amendment
- Phase 4bn-L derived-stack storage budget
- Phase 4bn-N normalization manifest/versioning convention

All prior phase results preserved verbatim. Phase 4 canonical remains
unauthorized.

## 14. No-rescue constraints

The Phase 4bn-O merge does not, and cannot, be construed as authorising:

- a normalized-layer eligibility gate or any successor (recommended only, NOT
  authorized);
- ML model training / selection, strategy hypothesis generation, signal
  construction, position state, entry/exit rules, or backtest design;
- feature derivation, label derivation, or research outputs;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation; barrier /
  target-before-stop / MFE / MAE / R-multiple / PnL labels;
- mark-price / spot / cross-venue / order-book / tick / additional aggTrades /
  ETHUSDT acquisition; v003 creation;
- reading the v002 terminal raw window or sealed-test split; mutating the
  published `__v002` family;
- database creation / DuckDB / SQLite / Parquet compaction / storage migration;
- transitioning any manifest's `research_eligible` or `eligibility_gate_status`
  from this evidence alone;
- old-strategy alt-symbol rerun, cooled-down-family reopening, or 5m
  research-thread reopening.

## 15. Successor authorization

**None.**

Not authorized (candidates a future operator might consider):

- a normalized-layer eligibility gate (Phase 4bn-O's recommendation — requires
  separate operator authorization);
- a docs-only holdout-boundary memo (only if a future scope touches the v002
  terminal raw window);
- a source-policy documentation memo;
- a process-doc `D:` path-string update;
- feature derivation + feature gate; label derivation + label gate; a
  chronological-split / holdout policy memo;
- ML implementation; strategy implementation; backtest implementation;
- additional aggTrades / 5m / 1m / tick / mark-price / order-book / spot /
  cross-venue / ETHUSDT acquisition;
- v003 creation; storage migration; database creation;
- paper / shadow; live-readiness; deployment; exchange-write; production keys;
  authenticated APIs; private endpoints; user stream; MCP / Graphify /
  `.mcp.json` / credentials;
- Phase 5; Phase 4 canonical.

## 16. Recommended state

**Remain paused.**

Phase 4bn-O is now **merge-complete on `main`** as of merge commit
`2c6c1789ed3b677229c741652699f27b16be21c5` and the subsequent merge-closeout +
SHA-finalization commits. The local normalized segment remains **non-eligible**
(`research_eligible: false`, `eligibility_gate_status: "pending"`). The
**conditional next, NOT authorized** option is a bounded, separately-authorized
**normalized-layer eligibility gate** (validate the segment manifest field
contract, verify forbidden fields absent, validate per-date parquet + sidecar
presence and SHA256s, recompute aggregates, validate predecessor integrity,
confirm `__v002` not mutated and v002 terminal / sealed-test not read, confirm
schema = `NORMALIZED_SCHEMA_V001`, and confirm `research_eligible` stays
`false` / `eligibility_gate_status` stays `"pending"`); such a gate flips no
eligibility and authorizes no successor. It is **not** authorized by this merge.

### Explicit confirmations

- Phase 4bn-N manifest/versioning convention followed: **yes**.
- v003 remains forbidden and absent: **yes**.
- Published normalized `__v002` remained immutable: **yes** (path-disjoint,
  never opened/written).
- v002 terminal window remained by-reference only: **yes** (`read: false`).
- Sealed-test split remained untouched: **yes**
  (`sealed_test_split_touched: false`, `test_holdout_touched: false`,
  `test_rows_loaded: 0`).
- No acquisition was run, no endpoints were called, no archives were
  downloaded, no HEAD preflight was run, no raw gate was rerun, no features
  were derived, no labels were derived, no ML was trained, no model scoring was
  performed, no predictions were generated, no diagnostics were run, no
  strategy/signal/PnL/backtest work was performed, no storage migration
  occurred, no database was created, no Parquet was compacted, no v003 dataset
  was created, no v002 terminal raw window was read, no test holdout was
  touched, no manifest eligibility transition occurred, no `data/research`
  artefacts were created or committed, no `data/microstructure` artefacts were
  committed, and no paper/shadow/live/exchange-write/credentials/MCP/Graphify
  work was authorized.

### Final git status (at SHA-finalization)

Recorded in the final operator report: working tree clean except the expected
untracked transient `.claude/scheduled_tasks.lock` plus the expected gitignored
local `data/microstructure/` and `data/research/` namespaces; `main ==
origin/main` after push.
