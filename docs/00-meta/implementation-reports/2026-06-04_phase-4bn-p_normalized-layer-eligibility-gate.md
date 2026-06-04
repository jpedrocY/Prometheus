# Phase 4bn-P — Normalized-Layer Eligibility Gate

## 1. Purpose

Phase 4bn-P executes a **normalized-layer eligibility gate** over the Phase
4bn-O local normalized pre-v002 BTCUSDT Binance USDⓈ-M futures aggTrades
segment (2024-03-01 .. 2024-11-30 inclusive UTC; 275 dates; 400,001,695
events). The gate validates that the local normalized segment is structurally
complete, internally consistent, manifest-consistent, predecessor-consistent,
schema-consistent, path-consistent, sidecar-consistent, and
governance-consistent, and records one local gitignored gate report + sidecar.

The gate is **read-only** with respect to all data artefacts. A passing gate
means only that the local normalized pre-v002 segment is structurally suitable
to proceed to a future, separately-authorized feature-derivation planning/gate
phase. It does **not** make the dataset research-eligible and authorizes no
features, labels, ML, diagnostics, strategy, or any successor.

## 2. Authority and repository state

- **Active local repo path:** `D:\Prometheus`. **Active Claude Code
  lightweight workspace:** `D:\ClaudeRuns\prometheus-light`.
- **GitHub remote:** `origin` → `https://github.com/jpedrocY/Prometheus.git`
  (verified intact).
- **Branch:** `phase-4bn-p/normalized-layer-eligibility-gate`.
- **Base `main` SHA:** `3fd795ceac4fc6804015301f7f21b4ef7b22f78b`
  (`docs(phase-4bn-o): finalize merge closeout shas`). Pre-branch
  `main == origin/main == HEAD` verified in sync; the Phase 4bn-O
  SHA-finalization `3fd795c`, merge-closeout `19ed9b9`, merge `2c6c178`, and
  branch commit `814112c` are present on `main`.
- **Tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (reads local
  normalized artefacts + manifest/sidecars, validates a newly generated
  segment, adjacent to future feature/label derivation, split/holdout policy,
  ML-baseline admissibility — while authorizing none of those).
- **Working-tree expectation:** the untracked transient
  `.claude/scheduled_tasks.lock`; the new tracked code/test/docs; the
  gitignored namespaces `data/microstructure/` (`.gitignore:85`) and
  `data/research/` (`.gitignore:88`) remain uncommitted.

## 3. Phase type and strict scope

**Phase type:** normalized-layer eligibility gate / local gitignored normalized
artefact validation / code + tests + docs + local gate-report.

**Allowed (and the entirety of what was done):** create one bounded read-only
gate runner reusing the locked normalize primitives; add a focused offline test
module; read the Phase 4bn-O normalized segment manifest/sidecar and 275
Parquet+sidecars; recompute SHAs, row counts, footprint; validate schema, paths,
sidecars, manifest field contract, predecessor SHAs, and governance posture;
write one local gitignored gate report + canonical sidecar under
`data/microstructure/gate-reports/normalized/`; create the two tracked Phase
4bn-P docs and update `current-project-state.md` narrowly.

**Forbidden (and not done):** no normalization rerun; no acquisition; no
endpoint / Binance / `data.binance.vision` call; no archive/CHECKSUM download;
no HEAD preflight; no raw-gate rerun; no feature/label/research output; no ML /
model scoring / predictions / diagnostics / strategy / signals / PnL /
backtests; no database / `.duckdb` / `.sqlite`; no Parquet compaction; no
storage migration; no v003; no v002 terminal raw-window read; no sealed-test
read; no published `__v002` Parquet/manifest read or mutation; no
`research_eligible` flip; no `eligibility_gate_status` transition; no
`data/microstructure` or `data/research` commit; no credentials / `.env` /
`.mcp.json` / MCP / Graphify; no successor authorization.

## 4. Evidence base and input boundary

**Committed evidence read:** `docs/00-meta/current-project-state.md`; the
process standards (`merge-closeout-standard.md`,
`phase-risk-tiering-standard.md`, `phase-workflow-standard.md`,
`phase-prompt-template.md`, `operator-report-standard.md`); the Phase 4bn-O
merge-closeout / implementation report / closeout; the Phase 4bn-N versioning
memo; the Phase 4bn-L budget memo; the Phase 4bn-K raw gate; the Phase 4bn-J-R2
acquisition reports; the data specs; committed tooling read-only
(`scripts/phase4bn_o_normalize_pre_v002_aggtrades.py`, `normalize_aggtrades.py`,
`normalize_io.py`, `normalize_manifest.py`, `normalize_validation.py`,
`canonical_paths.py`, `derived_gate.py`, `multiday_derived_gate*.py`, and the
offline test surface). README treated as potentially stale, not used as
current-state authority.

**Approved local reads (read-only):** the Phase 4bn-O normalized segment
manifest + sidecar; the 275 normalized Parquet files + 275 sidecars; the Phase
4bn-J-R2 raw segment manifest, the Phase 4bn-K raw gate report, and the raw
acquisition log (predecessor SHA + verdict verification only).

**Not read:** no v002 terminal raw-window file; no sealed-test file; no
published `__v002` Parquet; no published `__v002` manifest (treated by reference
only — never opened); no feature/label/research/ML/diagnostics artefact; no raw
zip.

## 5. Phase 4bn-O normalized segment carried forward

Phase 4bn-O (merge-complete on `main`) produced the local gitignored normalized
segment under gate here: 275 normalized Parquet (zstd) +275 canonical sidecars
under
`data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o/BTCUSDT/<YYYY>/<MM>/`,
the segment manifest
`…/manifests/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json`
(SHA256 `0e96ae37…d9fa`) + sidecar (SHA256 `5d7dcbef…6402`); 400,001,695
events; total normalized footprint 3,954,532,918 B; non-eligible
(`research_eligible: false`, `eligibility_gate_status: "pending"`).

## 6. Phase 4bn-N manifest/versioning convention carried forward

The gate validates the Phase 4bn-N segment convention: `dataset_family =
"microstructure_normalized_aggtrades_v001"`, `dataset_version = "v002"`,
`version = "v002"`, `schema_version = "v001"`, `segment_label =
"pre_v002_segment"`; version-suffixed segment directory distinct from the
published `__v002/`; full envelope + `__v002` by reference only
(`existing_v002_normalized_reference.read = false`, `mutated = false`); no v003.

## 7. Normalized-layer gate input contract

- Symbol BTCUSDT only; Binance USDⓈ-M futures only; aggTrades only; normalized
  dataset only.
- Segment 2024-03-01 .. 2024-11-30 inclusive UTC; 275 dates; 275 Parquet; 275
  sidecars; 400,001,695 events; total footprint 3,954,532,918 B.
- Manifest path/SHA: `…_4bn_o.json` / `0e96ae37…d9fa`; sidecar SHA
  `5d7dcbef…6402`.
- Predecessor: raw segment manifest `1659e6da…3a3d1`; raw gate report
  `051bed7b…20f9c24`; raw acquisition log `0266210f…88bcf93`.

## 8. Normalized-layer gate implementation path

A bounded read-only runner
`scripts/phase4bn_p_validate_normalized_pre_v002_gate.py` was created. The
existing `multiday_derived_gate` module is hardcoded to the published `__v002`
family and a different manifest shape, so it is not reusable for this segment;
the new runner reuses the locked primitives unchanged
(`NORMALIZED_SCHEMA_V001`, `NORMALIZATION_SCHEMA_VERSION` from
`normalize_aggtrades`; `compute_file_sha256`, `compute_bytes_sha256`,
`write_sha256_sidecar`, `assert_path_under_microstructure` from `normalize_io`)
and `pyarrow.parquet` for metadata/sample reads. Performance discipline mirrors
the Phase 4bm-D multi-day gate: for every one of the 275 files it streams the
Parquet SHA256 (full hash integrity), records the on-disk size, and reads
`ParquetFile.metadata` for the row count + column names (no row-group
materialisation); full-table content checks are bounded to a 10-date sample
(month-firsts + final date). A focused offline test module
`tests/research/microstructure/test_phase4bn_p_normalized_layer_gate.py`
(19 tests) accompanies it. No source module and no locked prior-phase script
was modified.

## 9. Gate checks performed

25 checks, all PASS: manifest SHA + canonical sidecar; manifest required-field
contract; manifest identity/scope; base_commit_sha; window/inventory totals;
predecessor lineage SHAs recorded; non-eligible/by-reference/sealed posture;
manifest forbidden-field scan; 275-contiguous-date coverage; per-file
present/hash-integrity/path-layout/schema/forbidden-columns/row-counts/
adjacency; 10-date deep row-level sample; aggregate rows/footprint/counts;
predecessor raw-manifest/raw-gate(+PASS)/acquisition-log SHA match; published
`__v002` path-disjoint + by-reference.

## 10. Local gate outputs

One local gitignored gate report + canonical sidecar under
`data/microstructure/gate-reports/normalized/`:

- **Report:**
  `microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o__phase-4bn-p__1780599605192__3fd795ceac4f.json`
  — SHA256 `3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134`.
- **Sidecar:** `…json.sha256` — body
  `3452fd9d…f134  …__3fd795ceac4f.json\n` (canonical two-space, LF, no BOM).
- Records `phase = phase-4bn-p`, `base_commit_sha =
  3fd795ceac4fc6804015301f7f21b4ef7b22f78b`, input normalized manifest path +
  SHA256, input segment directory, `gate_result_state`, `segment_non_eligible:
  true`, `research_eligible_after: false`, `eligibility_gate_status_after:
  pending`, `no_successor_authorization: true`, `v002_terminal_window_read:
  false`, `sealed_test_split_touched: false`, `published_v002_mutated: false`,
  `data_committed: false`, the 25 checks, and the predecessor SHAs.
- Gitignored (`.gitignore:85`), uncommitted.

## 11. Date coverage result

**PASS.** Exactly 275 contiguous daily dates, 2024-03-01 → 2024-11-30
inclusive; no missing date; no duplicate; no date `>= 2024-12-01`; no
sealed-test date; `per_file_inventory` dates equal `date_list` equal the
generated contiguous calendar.

## 12. Path, sidecar, and hash integrity result

**PASS.** All 275 Parquet under
`…/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o/BTCUSDT/<YYYY>/<MM>/`
with basename `BTCUSDT-aggTrades-<DATE>.parquet`; none under the published
`__v002/` directory; no v003 path. Every Parquet SHA256 (recomputed) equals its
paired canonical sidecar **and** the manifest `per_file_inventory` entry; every
sidecar is canonical (`<sha>␠␠<basename>\n`, LF, no BOM). The segment manifest
SHA256 equals `0e96ae37…d9fa` and its sidecar matches.

## 13. Manifest required-field and forbidden-field result

**PASS.** All Phase 4bn-N §12 required fields present with correct values
(identity/family, segment/phase, window/inventory, lineage, existing-v002
reference, full-envelope, governance/eligibility posture, terminal/sealed
witnesses, partitioning/primary-key/storage/sidecar policy, budget witnesses,
`base_commit_sha = f55b47ff…afefe6`). The §13 forbidden-field scan found no
model/label/target/future/signal/PnL/strategy/diagnostic/eligibility-flip/v003
field name (the `governance_labels` subtree, which legitimately declares
`feature_computation: forbidden` / `strategy_use: forbidden`, is contract-checked
separately).

## 14. Schema and Parquet validation result

**PASS.** Every one of the 275 Parquet has exactly the locked 19-column
`NORMALIZED_SCHEMA_V001` in canonical order (validated from Parquet metadata);
the forbidden-substring column guard passed for all files; the 10-date deep
sample confirmed dtypes/semantics, `dataset_version = "v002"`,
`source_dataset_version = "v002"`, `normalization_schema_version = "v001"`,
`symbol = "BTCUSDT"`, `utc_date = <date>`. No feature/label/research/model/
target/future/signal/PnL/strategy/score/prediction/mark-price/funding/
open-interest/order-book/spot/cross-venue/tick/ETHUSDT column.

## 15. Row-count and aggregate validation result

**PASS.** Recomputed total row count (sum of Parquet metadata `num_rows` over
275 files) = **400,001,695** (exact). Recomputed total footprint (Parquet +
sidecar bytes, matching the Phase 4bn-O definition) = **3,954,532,918 B**
(exact). 275 Parquet + 275 sidecars. Adjacent-date non-overlap held for all 274
pairs. The 10 deep-sampled dates' first/last `transact_time_ms`, min/max
`agg_trade_id`, half-open UTC-day bounds, strict agg-id monotonicity (⇒
uniqueness), and per-file row count matched the manifest inventory.

## 16. Predecessor integrity result

**PASS.** Recomputed SHA256 of the raw segment manifest = `1659e6da…3a3d1`; raw
gate report = `051bed7b…20f9c24` (with `overall_status: pass` and a `…PASS`
verdict); raw acquisition log = `0266210f…88bcf93` — all matched the predeclared
values. Raw zip contents were **not** read (raw integrity was already covered by
Phase 4bn-K and Phase 4bn-O).

## 17. Published `__v002` and sealed-test preservation

- The published normalized `__v002` family was **not** read and **not** mutated:
  the segment output directory and manifest are path-disjoint from `__v002`, the
  gate never opens the published `__v002` Parquet or manifest, and the segment
  manifest records `existing_v002_normalized_reference.read = false` /
  `mutated = false` and `v002_terminal_window_mode: "by_reference"`.
- The v002 terminal raw window (2024-12-01 .. 2025-02-28) was **not** read.
- The sealed v002 test split (2025-02-14 .. 2025-02-28) remained **untouched**:
  no segment date overlaps it; `sealed_test_split_touched: false`,
  `test_holdout_touched: false`, `test_rows_loaded: 0`.

## 18. Gitignore and non-commit verification

`git check-ignore -v data/microstructure/` → `.gitignore:85`;
`git check-ignore -v data/research/` → `.gitignore:88`. After the gate run,
`git status --short` shows only the new tracked runner/test/docs plus the
untracked `.claude/scheduled_tasks.lock`; no `data/microstructure/` or
`data/research/` artefact is tracked or staged. The gate report + sidecar are
gitignored and uncommitted. No `.duckdb`/`.sqlite` and no `v003` path exist.

## 19. Validation

Commands run and results (from `D:\Prometheus`):

- `git status --short` → only `.claude/scheduled_tasks.lock`, the new runner,
  the new test module, and the Phase 4bn-P docs (no data artefact);
- `git diff --check` → clean;
- `ruff check scripts/phase4bn_p_validate_normalized_pre_v002_gate.py tests/research/microstructure/test_phase4bn_p_normalized_layer_gate.py`
  → `All checks passed!`;
- `pytest …/test_phase4bn_p_normalized_layer_gate.py` → **19 passed**;
- `pytest …/test_normalize_io.py …/test_normalize_validation.py
  …/test_normalize_manifest.py …/test_phase4bn_o_normalization_pre_v002.py`
  → **75 passed** (no regression);
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`;
- real gate run → `NORMALIZED_LAYER_GATE_PASSED…`, 25/25 checks pass, runtime
  15.0 s; gate report SHA256 `3452fd9d…f134`.

mypy is scoped to `src/prometheus` in `pyproject.toml`; the new gate code lives
under `scripts/` + `tests/` (outside that scope) and imports the
already-checked `src/prometheus` primitives unchanged, so the repo-standard
mypy gate does not cover this surface and was not run on `scripts/`.

## 20. Result state

`NORMALIZED_LAYER_GATE_PASSED__LOCAL_NORMALIZED_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`.

The local normalized pre-v002 segment passed every gate check (25/25). It
remains **non-eligible** (`research_eligible: false`,
`eligibility_gate_status: "pending"`); no eligibility transition occurred; the
project remains paused.

## 21. Decision

`RECOMMEND_AUTHORIZE_FEATURE_DERIVATION_READINESS_OR_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Per the decision rules, with raw acquisition, raw gate, normalization, and now
the normalized-layer gate all passed for the pre-v002 segment, the next clean
technical stage is a separately-authorized feature-derivation readiness/execution
plan. That future step must still not derive labels, run ML, run diagnostics,
run strategy, run PnL/backtests, flip eligibility, or use the sealed test split.
No successor is authorized from inside Phase 4bn-P.

## 22. Recommended state and successor options

**Recommended state: remain paused.** Phase 4bn-P is **branch-complete only**;
not merged into `main`; not project-complete until a separately authorized merge
phase records its merge-closeout on `main`.

**Operator options (each subject to separate operator authorization; none
authorized here):**

- remain paused;
- request a merge prompt for Phase 4bn-P;
- separately authorize a **feature-derivation readiness or execution plan**
  (this phase's recommendation);
- separately authorize a docs-only holdout-boundary memo (only if a future
  scope touches the v002 terminal raw window);
- separately authorize a source-policy documentation memo;
- separately authorize a process-doc `D:` path-string update;
- reject further ML-baseline successors and close the ML-baseline arc.

No feature / label / ML / diagnostics / strategy / PnL / backtest / storage
migration / paper / shadow / live / exchange-write option is valid from this
state unless separately authorized after this branch is merged.

## 23. Explicit non-authorizations

Phase 4bn-P did **not** and does **not** authorize: normalization rerun;
acquisition; any endpoint / Binance / `data.binance.vision` call; archive /
CHECKSUM download; HEAD preflight; raw-gate rerun; feature derivation; label
derivation; research outputs; ML training; model scoring; predictions;
diagnostics; strategy / signals / PnL / backtests; storage migration; database
/ `.duckdb` / `.sqlite` creation; Parquet compaction; v003 creation; v002
terminal raw-window read; sealed-test read; published `__v002` read or mutation;
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

## 24. Current-project-state update summary

`docs/00-meta/current-project-state.md` was updated narrowly: one new Phase
4bn-P narrative paragraph was appended after the Phase 4bn-O paragraph, and a
new `Current phase:` block for Phase 4bn-P was inserted ahead of the Phase
4bn-O block. All prior Phase 4bn-A … 4bn-O paragraphs and `Current phase:`
blocks are preserved verbatim as labelled historical context. No other section
of that document was changed.
