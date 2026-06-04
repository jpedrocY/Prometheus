# Phase 4bn-P — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bn-P — Normalized-Layer Eligibility Gate for the Pre-V002
  BTCUSDT aggTrades Segment.
- **Type:** normalized-layer eligibility gate / local gitignored normalized
  artefact validation / code + tests + docs + local gate-report.
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bn-P bounded read-only gate runner, its
  offline test module, implementation report, closeout, and the narrow
  `current-project-state.md` update onto `main` as project state. The local
  gitignored normalized-layer gate report + sidecar produced by the run, and
  the Phase 4bn-O normalized segment it validated, are **local gitignored
  artefacts only** and are **not** part of this (or any) commit.
- **Target branch:** `main`.
- **Source branch:** `phase-4bn-p/normalized-layer-eligibility-gate`.
- **Risk tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (full 16-section
  merge-closeout required).

## 2. SHAs

- **`main` SHA before merge:** `3fd795ceac4fc6804015301f7f21b4ef7b22f78b`
  (`docs(phase-4bn-o): finalize merge closeout shas`).
- **Branch commit SHA (code + tests + docs):**
  `6e7571168a8fff5dbeb3cc2cac649a1ae43f643a`
  (`data(phase-4bn-p): gate normalized pre-v002 segment`).
- **Merge commit SHA:** `a10f255a5fabfb507a739fef25360a7e0bae4cdf`
  (`data(phase-4bn-p): merge normalized-layer eligibility gate`).
- **Merge-closeout commit SHA:** `19ed9b9`-analogue recorded in the
  SHA-finalization commit (see below; this file's add commit is
  `docs(phase-4bn-p): add merge closeout`).
- **SHA-finalization commit SHA:** this commit
  (`docs(phase-4bn-p): finalize merge closeout shas`) — its own hash is the new
  `main` tip; recorded verbatim in the final operator report after push.
- **Final `main` / `origin/main` SHA after push:** the SHA-finalization commit;
  `main == origin/main` after push (recorded in the final operator report).

## 3. Merge method

- `git merge --no-ff` with the default `ort` strategy.
- Merge commit message: `data(phase-4bn-p): merge normalized-layer eligibility
  gate`.
- No `--no-verify`; no `--no-gpg-sign`; no `-c commit.gpgsign=false`; no
  force-push.
- Pushed to `origin/main` with no force, no skip-hooks, no skip-signing
  (recorded at the final operator report after the SHA-finalization commit).

## 4. Files brought forward by the merge

- **Docs (3):**
  - `docs/00-meta/current-project-state.md` (modified — narrow Phase 4bn-P
    paragraph + new `Current phase:` block; prior Phase 4bn-A … 4bn-O
    paragraphs and blocks preserved verbatim as labelled historical context);
  - `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-p_normalized-layer-eligibility-gate.md`
    (added — implementation report, 24 sections);
  - `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-p_closeout.md`
    (added — branch closeout).
- **Scripts (1):** `scripts/phase4bn_p_validate_normalized_pre_v002_gate.py`
  (added — bounded read-only normalized-layer gate runner; reuses locked
  normalize primitives unchanged).
- **Tests (1):**
  `tests/research/microstructure/test_phase4bn_p_normalized_layer_gate.py`
  (added — 19 offline tests).
- **Source / config:** none.
- **`data/microstructure/` files:** **none modified or committed.** No
  `data/research/` file. No published manifest, sidecar, prior gate report,
  successor-state artefact, `.gitignore`, `pyproject.toml`, `README.md`, MCP
  file, or locked prior-phase script was modified.

The diff matches the expected change set from the merge authorization prompt
exactly (add 4 files, modify 1 doc).

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 115 +++
 .../2026-06-04_phase-4bn-p_closeout.md             | 148 ++++
 ...hase-4bn-p_normalized-layer-eligibility-gate.md | 352 +++++++++
 ...phase4bn_p_validate_normalized_pre_v002_gate.py | 818 +++++++++++++++++++++
 .../test_phase4bn_p_normalized_layer_gate.py       | 477 ++++++++++++
 5 files changed, 1910 insertions(+)
```

## 6. Verdict

**GATE PASS (local artefact validated).** Phase 4bn-P ran a read-only
normalized-layer eligibility gate over the Phase 4bn-O local normalized pre-v002
BTCUSDT Binance USDⓈ-M futures aggTrades segment (2024-03-01 .. 2024-11-30
inclusive UTC; 275 dates; 400,001,695 events) and recorded
`NORMALIZED_LAYER_GATE_PASSED__LOCAL_NORMALIZED_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`
with 25/25 checks PASS in 15.0 s. Every Parquet SHA256 matched its canonical
sidecar and the manifest inventory; the locked 19-column `NORMALIZED_SCHEMA_V001`
held for all 275 files; recomputed total rows (400,001,695) and footprint
(3,954,532,918 B) were exact; predecessor SHAs verified; the published `__v002`
family stayed by-reference and unread; the v002 terminal raw window stayed
unread; the sealed test split stayed untouched. The segment remains
**non-eligible** (`research_eligible: false`, `eligibility_gate_status:
"pending"`); no eligibility transition occurred. The merge lands the
code/tests/docs on `main`; the project remains paused.

## 7. Local gitignored outputs (produced by Phase 4bn-P; NOT committed)

- **Gate report:**
  `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o__phase-4bn-p__1780599605192__3fd795ceac4f.json`
  — SHA256 `3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134`;
  paired canonical `.sha256` sidecar (`<sha>␠␠<basename>\n`, LF, no BOM).
- Records: `phase = phase-4bn-p`; `base_commit_sha =
  3fd795ceac4fc6804015301f7f21b4ef7b22f78b`; `gate_result_state =
  NORMALIZED_LAYER_GATE_PASSED…`; 25/25 checks PASS; `segment_non_eligible:
  true`; `research_eligible_after: false`; `eligibility_gate_status_after:
  pending`; `no_successor_authorization: true`; `v002_terminal_window_read:
  false`; `sealed_test_split_touched: false`; `published_v002_mutated: false`;
  `data_committed: false`.
- **Segment validated (read-only, also gitignored, not committed):** the Phase
  4bn-O normalized segment — manifest
  `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json`
  (SHA256 `0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa`) +
  sidecar (SHA256 `5d7dcbef…6402`); 275 Parquet + 275 sidecars under
  `data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o/`;
  400,001,695 rows; footprint 3,954,532,918 B.
- **Not committed:** confirmed — all paths under `data/microstructure/` are
  gitignored (`git check-ignore -v data/microstructure/` → `.gitignore:85`);
  none staged or tracked.
- **Predecessor evidence:** raw segment manifest `1659e6da…3a3d1`; raw gate
  report `051bed7b…20f9c24` (PASS verdict); raw acquisition log
  `0266210f…88bcf93` — all recomputed and matched.

## 8. Validation results

Re-run at merge review (no real-gate rerun, no normalization rerun, no raw-gate
rerun, no acquisition, no endpoint):

- `git diff --check` → clean (no whitespace errors).
- `ruff check scripts/phase4bn_p_validate_normalized_pre_v002_gate.py tests/research/microstructure/test_phase4bn_p_normalized_layer_gate.py`
  → `All checks passed!`.
- `pytest tests/research/microstructure/test_phase4bn_p_normalized_layer_gate.py`
  → **19 passed**.
- `pytest …/test_normalize_io.py …/test_normalize_validation.py
  …/test_normalize_manifest.py …/test_phase4bn_o_normalization_pre_v002.py`
  → **75 passed** (no regression in the reused primitives).
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- **Original real-gate run (branch, not rerun here):**
  `NORMALIZED_LAYER_GATE_PASSED…`, 25/25 PASS, runtime 15.0 s, gate report
  SHA256 `3452fd9d…af134`.
- **mypy:** `pyproject.toml` scopes mypy to `src/prometheus`. The new Phase
  4bn-P code lives under `scripts/` and `tests/`, outside that scope, and
  imports the already-checked `src/prometheus` primitives unchanged. The
  repo-standard mypy gate does not cover this surface; mypy was not run on
  `scripts/` (rationale recorded per the merge prompt's repository tooling
  note).

## 9. Upstream immutability evidence

The Phase 4bn-P gate is read-only on all data artefacts and the merge modified
no `data/microstructure/` file. The segment manifest, all 275 Parquet, and all
275 sidecars were read (hashed) but not written; their recomputed SHA256s
matched the manifest inventory, confirming integrity without mutation. The
published normalized `__v002` family (directory + parquets +
`microstructure_normalized_aggtrades_v001__v002.json`) was **path-disjoint,
never opened, never written** — immutable by construction. The predecessor raw
segment manifest (`1659e6da…3a3d1`), raw gate report (`051bed7b…20f9c24`), and
raw acquisition log (`0266210f…88bcf93`) were re-hashed and matched. Raw zip
contents were not read.

## 10. Manifest state preservation

- The Phase 4bn-O normalized **segment manifest** remains seeded
  `research_eligible: false`, `eligibility_gate_status: "pending"`,
  `no_successor_authorization: true`; the gate performed no transition (it never
  writes the manifest).
- The published normalized `__v002` manifest and all prior manifests are
  **unchanged**.
- `chronological_split_policy` unchanged/absent; governance labels unchanged.
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
- gate is read-only: no segment manifest / Parquet / sidecar mutation; no write
  into the published `__v002/` directory; no `__v002` manifest mutation;
- no v003 created; no `.duckdb` / `.sqlite` / database created; no Parquet
  compaction; no storage migration;
- no `research_eligible` flipped; no `eligibility_gate_status` /
  `chronological_split_policy` / `diagnostics_authorized` / `ml_authorized`
  transitioned;
- no real-gate rerun at merge review; no normalizer rerun; no raw eligibility
  gate rerun; no acquisition; no endpoint / public / Binance /
  `data.binance.vision` call; no archive / CHECKSUM download; no HEAD preflight;
- no v002 terminal raw-window read; no sealed-test read; no published `__v002`
  Parquet read;
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

The Phase 4bn-P merge does not, and cannot, be construed as authorising:

- a feature-derivation readiness or execution plan, or any successor
  (recommended only, NOT authorized);
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
  from this gate evidence alone (a passing normalized-layer gate makes the
  dataset neither research-eligible nor admissible for ML);
- old-strategy alt-symbol rerun, cooled-down-family reopening, or 5m
  research-thread reopening.

## 15. Successor authorization

**None.**

Not authorized (candidates a future operator might consider):

- a feature-derivation readiness or execution plan (Phase 4bn-P's recommendation
  — requires separate operator authorization);
- feature derivation + feature gate; label derivation + label gate; a
  chronological-split / holdout policy memo;
- a docs-only holdout-boundary memo (only if a future scope touches the v002
  terminal raw window);
- a source-policy documentation memo; a process-doc `D:` path-string update;
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

Phase 4bn-P is now **merge-complete on `main`** as of merge commit
`a10f255a5fabfb507a739fef25360a7e0bae4cdf` and the subsequent merge-closeout +
SHA-finalization commits. The local normalized segment remains **non-eligible**
(`research_eligible: false`, `eligibility_gate_status: "pending"`); no manifest
eligibility transition occurred. The **conditional next, NOT authorized** option
is a separately-authorized **feature-derivation readiness or execution plan**
(which must still derive no labels, run no ML / diagnostics / strategy / PnL /
backtests, flip no eligibility, and use no sealed test split). It is **not**
authorized by this merge.

### Explicit confirmations

- Phase 4bn-P is merge-complete on `main` after this merge.
- Project completion of this phase requires the SHA-finalization commit
  (`docs(phase-4bn-p): finalize merge closeout shas`) per the repository's
  merge-closeout convention.
- Feature-derivation readiness / execution plan / any successor is **NOT
  authorized**.
- `research_eligible` remains `false`; `eligibility_gate_status` remains
  `pending`; no manifest eligibility transition occurred.
- Local normalized outputs and the gate report remain gitignored and
  uncommitted.
- Published normalized `__v002` remained by-reference and immutable; the v002
  terminal raw window remained unread; the sealed-test split remained untouched.
- No acquisition was run, no endpoints were called, no archives were downloaded,
  no HEAD preflight was run, no raw gate was rerun, no normalization was rerun,
  no features were derived, no labels were derived, no ML was trained, no
  diagnostics were run, no backtests were run, no strategy/signal/PnL work was
  performed, no storage migration occurred, no database was created, no Parquet
  was compacted, no v003 dataset was created, no v002 terminal raw window was
  read, no test holdout was touched, no manifest eligibility transition
  occurred, no `data/research` artefacts were created or committed, no
  `data/microstructure` artefacts were committed, and no
  paper/shadow/live/exchange-write/credentials/MCP/Graphify work was authorized.

### Final git status (at SHA-finalization)

Recorded in the final operator report: working tree clean except the expected
untracked transient `.claude/scheduled_tasks.lock` plus the expected gitignored
local `data/microstructure/` and `data/research/` namespaces; `main ==
origin/main` after push.
