# Phase 4bn-O — Normalization-Only Pre-V002 BTCUSDT aggTrades Segment Execution

## 1. Purpose

Phase 4bn-O executes the **normalization-only** step recommended by Phase
4bn-N: it normalizes **only** the approved pre-v002 BTCUSDT Binance USDⓈ-M
futures aggTrades raw segment (2024-03-01 .. 2024-11-30 inclusive UTC; 275
daily archives; 400,001,695 events) into a **phase-scoped normalized segment**
of the existing v002 normalized family, writing only local gitignored
normalized Parquet + canonical sidecars plus one non-eligible normalized
**segment manifest** + sidecar.

This phase authorizes and performs **no** features, **no** labels, **no** ML,
**no** diagnostics, **no** strategy/signals/PnL/backtests, **no** research
eligibility, **no** database, **no** Parquet compaction, **no** v003, and
**no** downstream use. It reads neither the v002 terminal raw window nor the
sealed v002 test split, and it does not mutate the published normalized
`__v002` family.

## 2. Authority and repository state

- **Active local repo path:** `D:\Prometheus`. **Active Claude Code
  lightweight workspace:** `D:\ClaudeRuns\prometheus-light`.
- **GitHub remote:** `origin` → `https://github.com/jpedrocY/Prometheus.git`
  (verified intact).
- **Branch:** `phase-4bn-o/normalization-only-pre-v002-segment`.
- **Base `main` SHA:** `f55b47ff94637e72ebacc40f1a133a5526afaef6`
  (`docs(phase-4bn-n): finalize merge closeout shas`). Pre-branch
  `main == origin/main == HEAD` verified in sync; the Phase 4bn-N
  SHA-finalization `f55b47f`, merge-closeout `7417a25`, merge `9ee0c4b`, and
  branch commit `0ba6ef0` are present on `main`; the Phase 4bn-M
  SHA-finalization `6d41c2e` is present as predecessor.
- **Tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3. This phase reads
  approved local raw artefacts, writes local normalized artefacts, creates a
  non-eligible normalized segment manifest, and is adjacent to future
  normalized-layer eligibility gates, future feature/label derivation, future
  holdout/split policy, future ML-baseline admissibility, and local
  disk/runtime budgets — while explicitly authorizing none of those.
- **Working-tree expectation:** the untracked transient
  `.claude/scheduled_tasks.lock`; the new tracked code/test/docs; the
  gitignored namespaces `data/microstructure/` (`.gitignore:85`) and
  `data/research/` (`.gitignore:88`) exist locally and remain uncommitted.

## 3. Phase type and strict scope

**Phase type:** normalization-only / bounded local gitignored data-artefact
generation / normalized manifest + sidecar generation / code + tests + docs.

**Allowed (and the entirety of what was done):** read committed Markdown docs
and committed tooling read-only; create one bounded new runner reusing the
locked normalization primitives unchanged; read only the approved pre-v002 raw
inputs (verified by SHA256); normalize the 275-date pre-v002 segment; write
only local gitignored normalized Parquet + canonical sidecars under the §14
segment directory; write one non-eligible normalized segment manifest +
sidecar; add a focused offline test module; create the two tracked Phase
4bn-O docs and update `current-project-state.md` narrowly.

**Forbidden (and not done):** no acquisition; no endpoint / Binance /
`data.binance.vision` call; no archive or CHECKSUM download; no HEAD preflight;
no raw-gate re-run; no v002 terminal raw-window read; no sealed-test read; no
published `__v002` normalized parquet/manifest read or mutation; no features;
no labels; no research outputs; no ML; no diagnostics; no strategy / signals /
PnL / backtests; no database / `.duckdb` / `.sqlite`; no Parquet compaction;
no v003; no `research_eligible` flip; no `eligibility_gate_status` transition;
no `data/microstructure` or `data/research` commit; no credentials / `.env` /
`.mcp.json` / MCP / Graphify; no successor authorization.

## 4. Evidence base and input boundary

**Committed evidence read:** `docs/00-meta/current-project-state.md`; the
process standards (`merge-closeout-standard.md`,
`phase-risk-tiering-standard.md`, `phase-workflow-standard.md`,
`phase-prompt-template.md`, `operator-report-standard.md`); the Phase 4bn-N
merge-closeout / versioning memo / closeout; the Phase 4bn-M / 4bn-L / 4bn-K /
4bn-J-R2 reports and closeouts; the data specs (`data-requirements.md`,
`historical-data-spec.md`, `timestamp-policy.md`, `dataset-versioning.md`) and
`database-design.md`; committed tooling read-only —
`src/prometheus/research/microstructure/normalize_aggtrades.py`,
`normalize_manifest.py`, `normalize_io.py`, `normalize_validation.py`,
`canonical_paths.py`, `derived_gate.py`, `multiday_derived_gate.py`,
`scripts/phase4bm_b_normalize_multiday_aggtrades.py`, and the offline test
surface under `tests/research/microstructure/`. README treated as potentially
stale, not used as current-state authority.

**Approved local inputs read (read-only):** the Phase 4bn-J-R2 raw segment
manifest
`data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2.json`
(SHA256 `1659e6da9ccc1c4a49c2f497e1f4a70f8082cac24142c77ac6d5217197b3a3d1`);
its acquisition log (SHA256
`0266210f23cae53ceda83270fd3466f15ffafdd7ded22bca828fc0cb788bcf93`); the
Phase 4bn-K raw gate report
`data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bn-k__1780436389489__cf7dc4f7e663.json`
(SHA256 `051bed7b3a146278e389bd8e265243d30fd541b5f36061d0573f3522920f9c24`,
`overall_status: pass`, verdict `RAW_ARCHIVE_GATE_PASSED…`); and the 275
approved raw aggTrades zips + 275 sidecars for 2024-03-01 .. 2024-11-30 only.
**No input outside the pre-v002 segment was read; no v002 terminal raw file;
no sealed-test file.** All three governance-input SHAs were recomputed locally
and matched the predeclared values exactly.

## 5. Phase 4bn-N manifest/versioning convention carried forward

Per the Phase 4bn-N memo §10/§11/§14 (selected: a phase-scoped normalized
segment manifest mirroring the merged raw-layer precedent), Phase 4bn-O wrote:

- a **phase-scoped normalized segment manifest**
  `microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json`
  with inner `dataset_family = "microstructure_normalized_aggtrades_v001"`,
  `dataset_version = "v002"`, `version = "v002"`, `schema_version = "v001"`,
  `segment_label = "pre_v002_segment"` — a backward segment of the v002
  envelope, **not** a write into published `__v002`, **not** a new `__vNNN`,
  **not** v003;
- a **version-suffixed segment directory distinct from the published `__v002/`
  directory**:
  `data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o/BTCUSDT/<YYYY>/<MM>/BTCUSDT-aggTrades-<YYYY-MM-DD>.parquet`,
  each with a paired canonical two-space `.sha256` sidecar;
- the full 12-month envelope **by reference only**
  (`full_intended_envelope_start = 2024-03-01`,
  `full_intended_envelope_end = 2025-02-28`, plus an
  `existing_v002_normalized_reference` block with `read: false`,
  `mutated: false`). The optional full-envelope reference/assembly manifest was
  **deliberately not created** (deferred per the memo, to avoid scope creep and
  any need to touch the v002 terminal window).

## 6. Phase 4bn-L budget carried forward

The runner enforces the Phase 4bn-L derived-stack budget verbatim: normalized
**100 GiB warn / 150 GiB hard** footprint, **4 h / 8 h** runtime; temporary
workspace **50 GiB / 100 GiB**; total derived-stack **250 GiB warn / 300 GiB
hard**; `D:` free-space floor **≥ 500 GiB before execution**, fail closed
**below 350 GiB during execution**. It preflight-estimates the normalized
footprint, temporary footprint, and total derived-stack footprint; verifies
the `D:` floor; measures footprint, runtime, and `D:` free space at day/month
boundaries; and fails closed (before proceeding) on any hard-cap breach.

## 7. Normalization input contract

- Symbol: **BTCUSDT** only. Market: **Binance USDⓈ-M futures** only. Family:
  **aggTrades** only.
- Segment: **2024-03-01 .. 2024-11-30 inclusive UTC**; **275** dates; **275**
  raw zips; **275** raw `.sha256` sidecars; **400,001,695** total events.
- The runner hard-rejects any date `>= 2024-12-01`, any date `< 2024-03-01`,
  any date `> 2024-11-30`, any sealed-test date (2025-02-14 .. 2025-02-28),
  any symbol other than BTCUSDT, any family other than aggTrades, and any
  forbidden scope token (ETHUSDT / mark-price / spot / order-book / tick /
  cross-venue / funding / open-interest / v003). It accepts no source URL,
  performs no network I/O, and reads no credentials / `.env` / `.mcp.json` /
  MCP / Graphify.
- Before writing, the runner verifies: the raw segment manifest SHA256, the
  raw gate report SHA256 (+ PASS), the raw acquisition-log SHA256; that the
  manifest records the exact 275-date BTCUSDT/aggTrades/usdm-futures segment
  with `research_eligible: false`, `eligibility_gate_status: "pending"`,
  `test_holdout_touched: false`, `test_rows_loaded: 0`, v002 terminal
  `read: false`, sealed-split `touched: false`; and that all 275 raw zips
  exist with SHA256s matching the manifest inventory and paired sidecars.

## 8. Normalization output contract

- Normalized aggTrades only, 2024-03-01 .. 2024-11-30 inclusive UTC.
- Output directory:
  `data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o/BTCUSDT/<YYYY>/<MM>/BTCUSDT-aggTrades-<YYYY-MM-DD>.parquet`.
- Every Parquet paired with a canonical two-space `.sha256` sidecar.
- Segment manifest:
  `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json`
  + paired `.sha256` sidecar.
- All outputs local, gitignored, non-eligible, uncommitted.

## 9. Implementation path

A bounded new runner `scripts/phase4bn_o_normalize_pre_v002_aggtrades.py` was
created. It does **not** modify any locked prior-phase script and does **not**
modify any source module. It reuses the locked Phase 4bd primitives unchanged
via import: `iter_aggtrade_rows_from_csv`, `NORMALIZED_SCHEMA_V001`,
`NORMALIZATION_SCHEMA_VERSION` (from `normalize_aggtrades`), and
`atomic_write_parquet`, `write_sha256_sidecar`, `compute_bytes_sha256`,
`assert_output_path_under_normalized`, `assert_path_under_microstructure`,
`assert_manifest_path_under_manifests` (from `normalize_io`). The bounded
orchestration it adds is exactly: pre-v002 segment-manifest input source;
hard date-range / symbol / family / scope-token guards; the Phase 4bn-L
preflight + budget caps; the §14 segment output naming; the §12 segment
manifest writer with refuse-overwrite, atomic write-then-rename, and canonical
sidecars; raw-input SHA verification + pre/post immutability; and a structural
guard that never writes into / reads the published `__v002` family. The
per-row schema is the locked 19-column `NORMALIZED_SCHEMA_V001` verbatim with
the forbidden-substring column guard; the per-day pipeline re-verifies row
count, agg-id monotonicity/uniqueness, half-open UTC-day bounds, and
first/last/min/max against the raw inventory, mirroring the Phase 4bm-B
contract. A focused offline test module
`tests/research/microstructure/test_phase4bn_o_normalization_pre_v002.py`
(37 tests) accompanies it.

## 10. Preflight results

All 7 preconditions + preflight **PASS** (dry-run and the real run agree):

- raw segment manifest present, SHA256 `1659e6da…3a3d1` matches;
- segment identity/scope locks match (BTCUSDT / aggTrades / binance_usdm_futures
  / `dataset_version: v002` / `segment_label: pre_v002_segment`);
- window contract matches (275 dates, 2024-03-01 .. 2024-11-30, total rows
  400,001,695); non-eligible posture confirmed (`research_eligible: false`,
  `eligibility_gate_status: "pending"`, `test_holdout_touched: false`,
  `test_rows_loaded: 0`, v002 terminal `read: false`, sealed-split
  `touched: false`);
- raw acquisition log present, SHA256 `0266210f…88bcf93` matches;
- raw gate report present, SHA256 `051bed7b…20f9c24` matches, `overall_status:
  pass`, verdict `RAW_ARCHIVE_GATE_PASSED…`;
- all 275 raw zips + 275 sidecars verified (each zip SHA256 matched the
  inventory; all dates inside the segment);
- preflight footprint/runtime/free-space within Phase 4bn-L caps: `D:` free at
  preflight **1,338,178,375,680 B ≈ 1246.3 GiB** (≥ 500 GiB floor); estimated
  normalized **6,400,027,120 B ≈ 5.96 GiB** (≤ 150 GiB hard, ≤ 100 GiB warn);
  estimated total derived-stack ≈ 5.99 GiB (≤ 300 GiB hard). No warning
  threshold crossed at preflight.

## 11. Normalization execution result

**PASS.** The runner normalized all **275** pre-v002 dates
(2024-03-01 .. 2024-11-30 inclusive UTC) in a single bounded run, wall-clock
**3624.3 s (≈ 60.4 min)**, exit code 0. `produced_file_count = 275`,
`total_event_count = total_row_count = 400,001,695` (exactly matches the raw
segment manifest / Phase 4bn-K recomputed total). Adjacent-date non-overlap
held for all 274 pairs; per-day row count, agg-id uniqueness + monotonicity,
half-open UTC-day bounds, and first/last/min/max all matched the raw inventory
for every date.

## 12. Normalized artefacts created

- **275** normalized Parquet files (zstd) under
  `data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o/BTCUSDT/<YYYY>/<MM>/BTCUSDT-aggTrades-<YYYY-MM-DD>.parquet`.
- **275** paired canonical `.sha256` sidecars (one per Parquet).
- Total normalized footprint **3,954,532,918 B ≈ 3.68 GiB**.
- All outputs local, gitignored (`.gitignore:85`), non-eligible, uncommitted.

## 13. Manifest and sidecars

- Segment manifest:
  `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json`
  — SHA256 **`0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa`**.
- Manifest sidecar:
  `…_4bn_o.json.sha256` — SHA256
  **`5d7dcbefbafcc81f2fcb1977ff9f35b08d58684542608317368c1f60f11e6402`**;
  body `0e96ae37…d9fa  microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json\n`
  (canonical two-space, LF, no BOM).
- The manifest carries every Phase 4bn-N §12 required field: identity/family,
  segment/phase, window/inventory (275-entry `per_file_inventory` with per-date
  parquet path, sidecar path, parquet SHA256, sidecar SHA256, parquet size,
  event count, first/last `transact_time_ms`, min/max `agg_trade_id`, source
  zip SHA256/path, status), `total_normalized_footprint_bytes`, predecessor
  lineage (raw segment manifest / gate report id+SHA / acquisition log, all
  SHAs matching), `existing_v002_normalized_reference` (read=false,
  mutated=false), `full_intended_envelope_*`, governance/eligibility posture,
  terminal/sealed-test witnesses, partitioning/primary-key/storage/sidecar
  policy, `invalid_windows: []`, and the Phase 4bn-L `budget_witnesses` block.
  The §13 forbidden fields are absent (verified by the in-runner
  `assert_manifest_field_contract` scan and the offline test suite).

## 14. Integrity and schema validation

- **Raw immutability (pre/post):** the segment manifest, the gate report, the
  acquisition log, all 275 raw zips, and all 275 raw zip sidecars were
  re-hashed after the run and were byte-identical to their pre-run SHA256s.
- **Schema:** every Parquet has exactly the locked 19-column
  `NORMALIZED_SCHEMA_V001` in canonical order with expected dtypes; the
  forbidden-substring column guard passed; per-row `dataset_version = "v002"`,
  `source_dataset_version = "v002"`, `normalization_schema_version = "v001"`,
  consistent with the v002-family lineage.
- **No forbidden output:** no feature/label/research column; no model / label /
  target / future / signal / PnL / strategy / score / prediction / mark-price /
  funding / open-interest / order-book / spot / cross-venue / tick / ETHUSDT
  field.

## 15. Budget and runtime results

Measured vs Phase 4bn-L caps — **no warning threshold and no hard cap crossed**:

| Witness | Measured | Warn | Hard |
| --- | --- | --- | --- |
| Normalized footprint | 3.68 GiB (3,954,532,918 B) | 100 GiB | 150 GiB |
| Runtime | 3624.3 s (≈ 1.01 h) | 4 h | 8 h |
| Temp workspace (pre-cleanup peak) | 55.7 MiB (58,372,029 B) | 50 GiB | 100 GiB |
| Temp workspace (post-cleanup) | 0 B | — | — |
| Total derived-stack | 3.68 GiB | 250 GiB | 300 GiB |
| `D:` free (preflight) | 1246.3 GiB | floor 500 GiB | — |
| `D:` free (min observed) | 1242.6 GiB (1,334,223,179,776 B) | floor 350 GiB | — |

`warning_thresholds_crossed: []`, `hard_caps_crossed: false`. Footprints
measured at every day/month boundary; `D:` free space measured at every day
boundary; temporary `.tmp` companions cleaned on success (0 leftover).

## 16. Gitignore and non-commit verification

`git check-ignore -v data/microstructure/` → `.gitignore:85`;
`git check-ignore -v data/research/` → `.gitignore:88`. After the run,
`git status --short` shows only the tracked new code/test/docs files plus the
untracked `.claude/scheduled_tasks.lock`; **no** `data/microstructure/` or
`data/research/` artefact is tracked or staged. No data artefact is committed.

## 17. Sealed-test and v002 terminal preservation

- The segment covers 2024-03-01 .. 2024-11-30 only — **no** sealed-test date
  (2025-02-14 .. 2025-02-28) and **no** v002 terminal-window date
  (2024-12-01 .. 2025-02-28) was read.
- The published normalized `__v002` family (directory + parquets + sidecars +
  `microstructure_normalized_aggtrades_v001__v002.json`) was **not** read and
  **not** mutated. The segment outputs live in a path-disjoint
  `…__v002_pre_v002_segment_4bn_o/` directory; the runner refuses to overwrite
  any finalised file and never opens the published `__v002` manifest. The
  manifest records `existing_v002_normalized_reference` with `read: false`,
  `mutated: false`, `v002_terminal_window_mode: "by_reference"`,
  `sealed_test_split_touched: false`, `test_holdout_touched: false`,
  `test_rows_loaded: 0`.

## 18. Validation

Commands run and results (from `D:\Prometheus`):

- `git status --short` → only `.claude/scheduled_tasks.lock`, the new runner
  script, the new test module, and the Phase 4bn-O docs (no data artefact);
- `git diff --check` → clean (no output);
- `ruff check scripts/phase4bn_o_normalize_pre_v002_aggtrades.py tests/research/microstructure/test_phase4bn_o_normalization_pre_v002.py`
  → `All checks passed!`;
- `pytest tests/research/microstructure/test_phase4bn_o_normalization_pre_v002.py`
  → **37 passed**;
- `pytest …/test_normalize_io.py …/test_normalize_validation.py
  …/test_normalize_manifest.py …/test_phase4bm_b_multiday_normalization.py`
  → **71 passed** (no regression in the reused primitives);
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
- `git check-ignore -v data/research/` → `.gitignore:88`;
- post-run filesystem verification: 275 parquets, 275 sidecars, manifest +
  sidecar present with the SHA256s in §13; canonical sidecar format; **0**
  `.duckdb`/`.sqlite` files; **0** `v003`-named paths; **0** leftover `.tmp`
  companions; no `data/microstructure` / `data/research` artefact staged or
  tracked; published normalized `__v002` directory and manifest path-disjoint,
  never opened, never written (immutable by construction).

The narrowest sufficient validation for the changed surface was run (the new
runner + test module, plus the reused-primitive regression set). No
markdown-lint tooling exists in the repo standard, so none was run.

## 19. Result state

`NORMALIZATION_SUCCEEDED__LOCAL_NORMALIZED_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`.

Normalization succeeded fully (275/275 parquets + sidecars + segment manifest +
sidecar); all outputs are local, gitignored, non-eligible
(`research_eligible: false`, `eligibility_gate_status: "pending"`) and
uncommitted; no eligibility transition occurred; the project remains paused.

## 20. Decision

`RECOMMEND_AUTHORIZE_NORMALIZED_LAYER_ELIGIBILITY_GATE__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Per the decision rules, normalization succeeded fully and outputs / manifest /
sidecars were created cleanly with no v003, no `__v002` mutation, no v002
terminal raw read, and no sealed-test touch — so the recommended next technical
step is a future, separately-authorized **normalized-layer eligibility gate**
only. No successor is authorized from inside Phase 4bn-O. No features, labels,
ML, diagnostics, strategy, PnL, backtests, storage migration, v003, or
paper/shadow/live work is recommended or authorized from this state.

## 21. Recommended state and successor options

**Recommended state: remain paused.** Phase 4bn-O is **branch-complete only**;
not merged into `main`; not project-complete until a separately authorized
merge phase records its merge-closeout on `main` per
`merge-closeout-standard.md` (Tier 1).

**Operator options (each subject to separate operator authorization; none
authorized here):**

- remain paused;
- request a merge prompt for Phase 4bn-O;
- (if normalization succeeded) separately authorize a **normalized-layer
  eligibility gate** — a bounded read-only gate validating the segment
  manifest field contract, forbidden-field absence, per-date parquet+sidecar
  presence/SHA256s, recomputed aggregates, predecessor integrity, `__v002`
  non-mutation, schema = `NORMALIZED_SCHEMA_V001`, and that `research_eligible`
  stays `false` / `eligibility_gate_status` stays `"pending"` (a passing gate
  flips nothing and authorizes no successor);
- separately authorize a docs-only holdout-boundary memo (only relevant if a
  future phase intends to read the v002 terminal raw window);
- separately authorize a source-policy documentation memo;
- separately authorize a process-doc `D:` path-string update;
- reject further ML-baseline successors and close the ML-baseline arc.

No feature / label / ML / diagnostics / strategy / PnL / backtest / storage
migration / paper / shadow / live / exchange-write option is valid from this
state unless separately authorized after this branch is merged.

## 22. Explicit non-authorizations

Phase 4bn-O did **not** and does **not** authorize: acquisition; any endpoint
/ public / Binance / `data.binance.vision` call; archive or CHECKSUM download;
HEAD preflight; raw-gate re-run; feature derivation; label derivation;
research outputs; ML training; model scoring; predictions; diagnostics;
strategy / signals / PnL / backtests; storage migration; database / `.duckdb`
/ `.sqlite` creation; Parquet compaction; v003 creation; v002 terminal
raw-window read; sealed-test read; published `__v002` read or mutation;
`research_eligible` flip; `eligibility_gate_status` /
`chronological_split_policy` / `diagnostics_authorized` / `ml_authorized`
transition; `data/microstructure` or `data/research` commit; credentials /
`.env` / `.mcp.json` / MCP / Graphify; WebSocket / user stream / private /
authenticated endpoint; paper / shadow; live-readiness; deployment;
exchange-write; production keys; Phase 5; or any successor phase.

Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m
thread / V2 / G1 / C1) and every project lock (§11.6 = 8 bps per side;
round-trip = 16 bps; §1.7.3; Phase 3p §4.7; Phase 3r §8; Phase 3v §8;
Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v;
Phase 4w; Phase 4ak M0; Phase 4al refined no-rescue rule; Phase 4aw
`flip_research_eligible(...)` always-raises invariant (never invoked); Phase
4bb-F canonical path + sidecar policy; the Phase 4bn-J-R1 raw-only cap
amendment; the Phase 4bn-L derived-stack storage budget; the Phase 4bn-N
normalization manifest/versioning convention) is preserved verbatim. Phase 4
canonical remains unauthorized.

## 23. Current-project-state update summary

`docs/00-meta/current-project-state.md` was updated narrowly: one new Phase
4bn-O narrative paragraph was appended after the Phase 4bn-N paragraph, and a
new `Current phase:` block for Phase 4bn-O was inserted ahead of the Phase
4bn-N block. All prior Phase 4bn-A … 4bn-N paragraphs and `Current phase:`
blocks are preserved verbatim as labelled historical context. No other section
of that document was changed.
