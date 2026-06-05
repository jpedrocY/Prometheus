# Phase 4bn-S — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bn-S — Feature-Only Pre-V002 BTCUSDT aggTrades Segment
  Execution.
- **Type:** feature-only / bounded local gitignored feature artefact generation
  / feature segment manifest + sidecar generation / code + tests + docs.
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bn-S bounded feature wrapper
  (`scripts/phase4bn_s_compute_pre_v002_features.py`), its offline test module,
  the implementation report, the branch closeout, and the narrow
  `current-project-state.md` update onto `main` as project state. The phase
  feature-derived the approved Phase 4bn-O pre-v002 BTCUSDT Binance USDⓈ-M
  futures aggTrades normalized segment (2024-03-01 .. 2024-11-30 inclusive UTC;
  275 days; 400,001,695 events) into a phase-scoped pre-v002 feature segment of
  the v002 feature family `microstructure_features_aggtrades_v001`, producing
  only local gitignored feature artefacts plus one non-eligible feature segment
  manifest + canonical sidecar.
- **Target branch:** `main`.
- **Source branch:** `phase-4bn-s/feature-only-pre-v002-segment`.
- **Risk tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (full 16-section
  merge-closeout required).

## 2. SHAs

- **`main` SHA before merge:** `40f0b3e54392e0e108b8664beedf25169a2d9778`
  (`docs(phase-4bn-r): finalize merge closeout shas`).
- **Branch commit SHA (code + tests + docs):**
  `9679d9ac7251a7bdd6714ef13c0cd9ab88b0e3fe`
  (`data(phase-4bn-s): compute pre-v002 feature segment`).
- **Merge commit SHA:** `8005fb587ea6f7711a064c4c361c77a5b4820327`
  (`data(phase-4bn-s): merge pre-v002 feature segment`).
- **Merge-closeout commit SHA:** `1314c274dd400c9fe92490dd7a031f76b1b81dfd`
  (`docs(phase-4bn-s): add merge closeout`).
- **SHA-finalization commit SHA:** this commit
  (`docs(phase-4bn-s): finalize merge closeout shas`) — its own hash becomes the
  new `main` tip; recorded verbatim in the final operator report after push.
- **Final `main` / `origin/main` SHA after push:** the SHA-finalization commit;
  `main == origin/main` after push (recorded in the final operator report).

## 3. Merge method

- `git merge --no-ff` with the default `ort` strategy.
- Merge commit message: `data(phase-4bn-s): merge pre-v002 feature segment`.
- No `--no-verify`; no `--no-gpg-sign`; no `-c commit.gpgsign=false`; no
  force-push.
- Pushed to `origin/main` with no force, no skip-hooks, no skip-signing
  (recorded at the final operator report after the SHA-finalization commit).

## 4. Files brought forward by the merge

- **Docs (3):**
  - `docs/00-meta/current-project-state.md` (modified — narrow Phase 4bn-S
    paragraph + new `Current phase:` block; prior Phase 4bn-A … 4bn-R
    paragraphs and blocks preserved verbatim as labelled historical context;
    94 insertions, 0 deletions — insertion-only);
  - `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-s_feature-only-pre-v002-segment.md`
    (added — the implementation report, 24 sections);
  - `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-s_closeout.md`
    (added — branch closeout).
- **Scripts (1):** `scripts/phase4bn_s_compute_pre_v002_features.py` (added —
  the bounded feature-only runner; reuses the locked Phase 4bm-H v002 feature
  primitives unchanged).
- **Tests (1):**
  `tests/research/microstructure/test_phase4bn_s_feature_pre_v002.py` (added —
  32 offline tests).
- **Source / config:** none.
- **`data/microstructure/` files:** **none modified or committed.** No
  `data/research/` file. No published manifest, sidecar, prior gate report,
  successor-state artefact, `.gitignore`, `pyproject.toml`, `README.md`, or MCP
  file was modified. No locked prior-phase script and no source module was
  modified.

The diff matches the expected change set from the merge authorization prompt
exactly (add 4 files, modify 1 doc).

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              |   94 +
 .../2026-06-04_phase-4bn-s_closeout.md             |  143 ++
 ...04_phase-4bn-s_feature-only-pre-v002-segment.md |  402 +++++
 scripts/phase4bn_s_compute_pre_v002_features.py    | 1868 ++++++++++++++++++++
 .../test_phase4bn_s_feature_pre_v002.py            |  826 +++++++++
 5 files changed, 3333 insertions(+)
```

The diff matches the expected change set (insertion-only; code + tests + docs;
no data).

## 6. Result / verdict

**FEATURE EXECUTION SUCCEEDED — LOCAL FEATURE SEGMENT NON-ELIGIBLE — REMAIN
PAUSED.** Phase 4bn-S executed the feature-only phase recommended by Phase
4bn-R. It enforced the Phase 4bn-R non-eligible-source precondition (Phase
4bn-P normalized-layer gate report SHA256 `3452fd9d…f134`, PASS 25/25, over the
Phase 4bn-O normalized segment manifest SHA256 `0e96ae37…d9fa`, both verified;
source segment `research_eligible=false` / `eligibility_gate_status=pending`),
read only the approved 275 normalized segment dates (each SHA-verified), and
wrote 275 feature Parquets + 275 canonical `.sha256` sidecars plus one feature
segment manifest + sidecar — all local and gitignored. Total feature rows equal
the source event count (400,001,695) exactly; the locked 62-column
`FEATURE_SCHEMA_V002` (17 lineage + 45 feature/quality) is preserved; the
strictly-causal kernel and backward-only 60 s cross-day tail are preserved
(2024-03-01 used no pre-segment read with `rolling_missing_window_flag`;
2024-11-30 required no forward read into 2024-12-01). The generated feature
segment remains non-eligible (`research_eligible=false`,
`eligibility_gate_status=pending`, `no_successor_authorization=true`,
`source_eligibility_posture="non_eligible_gate_passed_pending"`). Result state
`FEATURE_EXECUTION_SUCCEEDED__LOCAL_FEATURE_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`;
decision
`RECOMMEND_AUTHORIZE_FEATURE_LAYER_ELIGIBILITY_GATE__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
The merge lands the wrapper + tests + report + closeout + narrow state update on
`main`; the project remains paused; the segment remains non-eligible.

## 7. Local gitignored outputs (produced by the phase; NOT committed)

All produced by the real feature execution; all local, gitignored
(`.gitignore:85`, `data/microstructure/`), uncommitted, and confirmed not
staged. `git check-ignore -v data/microstructure/` → `.gitignore:85`.

- **275 feature Parquet files** under
  `data/microstructure/features/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s/BTCUSDT/<YYYY>/<MM>/BTCUSDT-features-aggtrades-<YYYY-MM-DD>.parquet`
  (2024-03-01 .. 2024-11-30).
- **275 canonical `.sha256` feature Parquet sidecars** (one per Parquet;
  two-space body, LF, no BOM).
- **1 feature segment manifest**
  `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s.json`
  — SHA256 `4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52`.
- **1 feature segment manifest sidecar**
  `…__v002_pre_v002_segment_4bn_s.json.sha256`
  — SHA256 `f2ca2f48a5ac8ccfb892d0460cdfbbbb891451b9d94135adb3bff0936c8592e5`.
- **Feature config hash:**
  `0726b41d48e5f7127728c385b150d90fad91a92b3400c0545649b541e4dd114c`;
  **feature schema hash:**
  `bf3d80bcf387970d5ad3dd85d99bd657cfd82527c6fe49f544f53f096a7a0ff5`.
- **Total feature footprint:** 54,254,406,538 bytes (≈50.53 GiB).
- **Total feature rows:** 400,001,695.
- **Schema:** exactly `FEATURE_SCHEMA_V002`, 62 columns (17 lineage + 45
  feature/quality), canonical order.
- **Runtime:** 14,321.72 s (≈3.98 h).
- **Temporary workspace peak:** 882,430,048 bytes (≈0.82 GiB); post-cleanup
  0 bytes.
- **D: free preflight:** 1,334,218,002,432 bytes (≈1242.6 GiB); **minimum
  observed:** 1,279,962,128,384 bytes (≈1192.1 GiB).
- **Warning thresholds crossed:** `["feature_warn"]` (50.53 GiB > 50 GiB
  warning); **hard caps crossed:** `false`; no fail-closed stop condition
  triggered.

The pre-existing Phase 4bn-O normalized outputs and Phase 4bn-P
normalized-layer gate report remain local, gitignored, and uncommitted.

## 8. Validation results

Merge-review validation (no real feature execution rerun; no gate / acquisition
/ normalization run):

- `git diff --check` → clean (no whitespace errors).
- `git diff --name-status main..branch` (pre-merge) → exactly the 5 expected
  files (M `current-project-state.md`; A report; A closeout; A script; A test).
- `git diff --stat main..branch` (pre-merge) → `5 files changed, 3333
  insertions(+)`.
- `ruff check scripts/phase4bn_s_compute_pre_v002_features.py
  tests/research/microstructure/test_phase4bn_s_feature_pre_v002.py` → All
  checks passed.
- `pytest tests/research/microstructure/test_phase4bn_s_feature_pre_v002.py`
  → 32 passed.
- `pytest` (combined required suites: Phase 4bn-S + 4bn-P normalized-layer gate
  + 4bn-O normalization + normalize io / validation / manifest) → **126
  passed**.
- `mypy src/prometheus` (repo-standard gate; `files = ["src/prometheus"]`) →
  96 pre-existing errors in 12 files, **identical to `main`**: Phase 4bn-S added
  no file under `src/prometheus` and modified no source module, so the mypy
  surface is unchanged and **zero** new errors were introduced. The new feature
  wrapper lives under `scripts/`, which is out of mypy scope by repo convention;
  no mypy gate applies to it.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- `git status --short` → only `.claude/scheduled_tasks.lock` untracked; no
  `data/microstructure/` or `data/research/` artefact staged or committed.
- The real feature execution was performed once on the branch (not rerun at
  merge): 275 / 275 Parquets + sidecars; manifest + sidecar written; 25 checks
  PASS; source immutability verified pre/post; no `.duckdb` / `.sqlite`; no v003
  path; no `data/research` output; published feature `__v002` neither read nor
  mutated; v002 terminal window and sealed-test split untouched.

## 9. Upstream immutability evidence

The Phase 4bn-S real execution re-hashed every read-only source artefact AFTER
all writes and confirmed each byte-identical pre/post (check `4bn-S.immutability`
PASS):

- Phase 4bn-O normalized segment manifest
  `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json`
  — SHA256 `0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa`
  (pre == post).
- Phase 4bn-P normalized-layer gate report
  `…/gate-reports/normalized/…__phase-4bn-p__1780599605192__3fd795ceac4f.json`
  — SHA256 `3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134`
  (pre == post).
- All 275 source normalized Parquet files — each pre == post SHA256 against the
  segment manifest inventory.

The published normalized `__v002` family, the published feature `__v002`
manifest
(`data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json`)
and Parquet family, the v002 terminal raw/normalized window, and the sealed-test
split were neither read nor mutated. The merge modified no `data/microstructure/`
file.

## 10. Manifest state preservation

- **Source Phase 4bn-O normalized segment manifest:** `research_eligible:
  false`, `eligibility_gate_status: "pending"`; unchanged — no transition.
- **Generated Phase 4bn-S feature segment manifest:** `research_eligible:
  false`, `eligibility_gate_status: "pending"`, `no_successor_authorization:
  true`, `source_eligibility_posture: "non_eligible_gate_passed_pending"`; 18-key
  boundary confirmations all true; 8-flag non-authorization set all false; no
  `chronological_split_policy` field; governance labels mark
  labels/ml/strategy/backtest = forbidden, acquisition = unauthorized.
- **Published normalized / feature `__v002` manifests:** untouched; no
  transition.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises
  invariant preserved (never invoked).

## 11. Boundary confirmations

- no source code modified; no locked prior-phase script modified; no test
  outside the new module modified;
- no `.gitignore`, `pyproject.toml`, `README.md`, or MCP file modified;
- no published manifest / sidecar / prior gate report / successor-state artefact
  modified;
- no `data/microstructure/` or `data/research/` artefact staged or committed;
- no feature write into the published `__v002` feature directory; no published
  feature `__v002` manifest mutation; no published normalized `__v002` read or
  mutation;
- no v002 terminal normalized window read; no v002 terminal raw window read; no
  sealed-test read;
- no labels / targets / future returns; no ML / model scoring / predictions; no
  diagnostics; no strategy / signal / PnL / backtest; no feature ranking /
  selection / pruning / hyperparameter / threshold / calibration tuning; no
  research-matrix output;
- no acquisition; no endpoint / public / Binance / `data.binance.vision` call;
  no archive / CHECKSUM download; no HEAD preflight; no raw-gate rerun; no
  normalization rerun; no normalized-layer-gate rerun; no feature-layer gate run;
- no `research_eligible` flip; no `eligibility_gate_status` /
  `chronological_split_policy` / `diagnostics_authorized` / `ml_authorized`
  transition;
- no database / `.duckdb` / `.sqlite`; no Parquet compaction; no storage
  migration; no v003;
- no ETHUSDT / mark-price / spot / cross-venue / order-book / tick / extra-horizon
  data;
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
- Phase 4bn-L derived-stack storage budget (feature-layer caps applied this
  phase)
- Phase 4bn-N normalization manifest/versioning convention
- Phase 4bn-R feature manifest/versioning convention + non-eligible-source
  precondition (followed this phase)

All prior phase results preserved verbatim. Phase 4 canonical remains
unauthorized.

## 14. No-rescue constraints

The Phase 4bn-S merge does not, and cannot, be construed as authorising:

- a feature-layer eligibility gate or any successor (recommended only, NOT
  authorized);
- label derivation / label gate; targets; future returns; barrier /
  target-before-stop / MFE / MAE / R-multiple / PnL labels; 30s / 5m / 30m /
  1h / 4h / longer-horizon label generation;
- ML model training / selection / scoring, predictions, strategy hypothesis
  generation, signal construction, position state, entry/exit rules, diagnostics,
  or backtest design;
- feature ranking / selection / pruning / engineering / hyperparameter /
  threshold / calibration tuning;
- paper / shadow / live-readiness / deployment / exchange-write / production-key
  work; Phase 4 canonical or Phase 5 authorisation;
- mark-price / spot / cross-venue / order-book / tick / additional aggTrades /
  ETHUSDT acquisition; extra horizons; v003 creation;
- reading the v002 terminal raw/normalized window or sealed-test split;
  mutating the published normalized or feature `__v002` family;
- database creation / DuckDB / SQLite / Parquet compaction / storage migration;
- transitioning any manifest's `research_eligible` or `eligibility_gate_status`
  from this feature segment alone;
- old-strategy alt-symbol rerun, cooled-down-family reopening, or 5m
  research-thread reopening.

## 15. Successor authorization

**None.**

Not authorized (candidates a future operator might consider):

- a feature-layer eligibility gate (Phase 4bn-S's recommendation — requires
  separate operator authorization; validation-only, must not flip eligibility
  or authorize labels / ML / diagnostics / strategy / any successor);
- a docs-only holdout-boundary memo (only if a future scope reads the v002
  terminal raw/normalized window or sealed-test dates);
- a source-policy documentation memo; a process-doc `D:` path-string update;
- label derivation + label gate; a chronological-split / holdout policy memo;
- ML implementation; strategy implementation; backtest implementation;
- additional aggTrades / 5m / 1m / tick / mark-price / order-book / spot /
  cross-venue / ETHUSDT acquisition; v003 creation; storage migration; database
  creation;
- paper / shadow; live-readiness; deployment; exchange-write; production keys;
  authenticated APIs; private endpoints; user stream; MCP / Graphify /
  `.mcp.json` / credentials;
- Phase 5; Phase 4 canonical.

## 16. Recommended state

**Remain paused.**

Phase 4bn-S is now **merge-complete on `main`** as of merge commit
`8005fb587ea6f7711a064c4c361c77a5b4820327` and the subsequent merge-closeout +
SHA-finalization commits. Project completion of this phase requires the
SHA-finalization commit (`docs(phase-4bn-s): finalize merge closeout shas`) per
the repository's merge-closeout convention. The local feature segment remains
**non-eligible** (`research_eligible: false`, `eligibility_gate_status:
"pending"`, `no_successor_authorization: true`); no manifest eligibility
transition occurred. v003 remains forbidden and absent; the published feature
`__v002` family remains immutable; the v002 terminal normalized window remains
by-reference only and unread; the sealed-test split remains untouched. The
**conditional next, NOT authorized** option is a separately-authorized
**feature-layer eligibility gate** (validation-only). It is **not** authorized
by this merge.

### Input / output segment (preserved)

- **Exact input normalized segment:** 2024-03-01 .. 2024-11-30 inclusive UTC
  (Phase 4bn-O pre-v002 normalized segment; 275 days; 400,001,695 events).
- **Exact output feature segment:** 2024-03-01 .. 2024-11-30 inclusive UTC.
- **Exact output feature directory:**
  `data/microstructure/features/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s/`
  (version-suffixed segment dir distinct from the published `__v002/` feature
  dir; not the generic `microstructure_features_aggtrades_v001/` dir; not a new
  `__vNNN`; not v003).
- **Exact feature manifest path:**
  `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s.json`
  (SHA256 `4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52`;
  sidecar SHA256
  `f2ca2f48a5ac8ccfb892d0460cdfbbbb891451b9d94135adb3bff0936c8592e5`).

### Explicit confirmations

- Phase 4bn-S is merge-complete on `main` after this merge.
- Project completion requires the SHA-finalization commit
  (`docs(phase-4bn-s): finalize merge closeout shas`).
- Feature-layer eligibility gate / any successor is **NOT authorized**.
- The Phase 4bn-R feature manifest/versioning convention was followed; the Phase
  4bn-R non-eligible-source precondition was followed.
- `research_eligible` remains `false`; `eligibility_gate_status` remains
  `pending`; no manifest eligibility transition occurred.
- v003 remains forbidden and absent; the published feature `__v002`
  manifest/family remained immutable; the v002 terminal normalized window
  remained by-reference only and unread; the sealed-test split remained
  untouched.
- Local feature outputs are gitignored and uncommitted; the pre-existing
  gitignored Phase 4bn-O normalized outputs and Phase 4bn-P normalized-layer
  gate report remain local and uncommitted.
- No acquisition was run, no endpoints were called, no archives were downloaded,
  no HEAD preflight was run, no raw gate was rerun, no normalization was rerun,
  no normalized-layer gate was rerun, no feature-layer gate was run, no labels
  were derived, no targets were created, no future returns were computed, no ML
  was trained, no model scoring was performed, no predictions were generated, no
  diagnostics were run, no backtests were run, no strategy/signal/PnL work was
  performed, no storage migration occurred, no database was created, no Parquet
  was compacted, no v003 dataset was created, no v002 terminal normalized window
  was read, no test holdout was touched, no manifest eligibility transition
  occurred, no `data/research` artefacts were created or committed, no
  `data/microstructure` artefacts were committed, and no
  paper/shadow/live/exchange-write/credentials/MCP/Graphify work was authorized.

### Final git status (at SHA-finalization)

Recorded in the final operator report: working tree clean except the expected
untracked transient `.claude/scheduled_tasks.lock` plus the expected gitignored
local `data/microstructure/` and `data/research/` namespaces; `main ==
origin/main` after push.
