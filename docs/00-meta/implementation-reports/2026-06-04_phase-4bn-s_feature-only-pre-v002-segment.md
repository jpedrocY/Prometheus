# Phase 4bn-S — Feature-Only Pre-V002 BTCUSDT aggTrades Segment Execution

## 1. Purpose

Phase 4bn-S executes the feature-only phase recommended by Phase 4bn-R. It
feature-derives the approved, **local, gitignored, non-eligible** Phase 4bn-O
pre-v002 normalized BTCUSDT Binance USDⓈ-M futures aggTrades segment
(2024-03-01 .. 2024-11-30 inclusive UTC; 275 days; 400,001,695 events) into a
phase-scoped **pre-v002 feature segment** of the existing v002 feature family
`microstructure_features_aggtrades_v001`, writing only local gitignored feature
Parquet artefacts plus one non-eligible feature **segment** manifest and its
canonical sidecar. It authorizes no successor.

The phase reused the locked Phase 4bm-H v002 feature primitives unchanged and
added only a bounded orchestration wrapper. Feature execution **succeeded**:
275 feature Parquets + 275 canonical `.sha256` sidecars and one segment
manifest + sidecar were produced; total feature rows equal the source event
count (400,001,695) exactly; the generated feature segment remains
`research_eligible = false` / `eligibility_gate_status = "pending"` with
`no_successor_authorization = true`.

## 2. Authority and repository state

- **Active local repo path:** `D:\Prometheus`.
- **Active Claude workspace:** `D:\ClaudeRuns\prometheus-light`.
- **GitHub remote:** `origin` → `https://github.com/jpedrocY/Prometheus.git`
  (verified intact).
- **Branch:** `phase-4bn-s/feature-only-pre-v002-segment`.
- **Base `main` SHA (`BASE_SHA_4BN_R_FINAL`):**
  `40f0b3e54392e0e108b8664beedf25169a2d9778`
  (`docs(phase-4bn-r): finalize merge closeout shas`; short `40f0b3e`).
  Pre-branch `main == origin/main == HEAD` verified in sync via
  `git rev-parse`. Predecessor chain confirmed present on `main`: Phase 4bn-R
  finalization `40f0b3e`, merge-closeout `a388ec8`, merge `b7d13e4`, branch
  `4e7851e`; Phase 4bn-Q finalization `014c58a`.
- **Working tree at phase start:** only the expected untracked transient
  `.claude/scheduled_tasks.lock`; gitignored `data/microstructure/` present
  locally and uncommitted.

## 3. Phase type and strict scope

Tier 1 — Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md`
§3: feature-only / bounded local gitignored feature artefact generation /
feature segment manifest + sidecar generation / code + tests + docs phase.

Phase 4bn-S did **not**: derive or create labels, targets, future returns,
MFE / MAE / R-multiple / barrier outputs; run ML, score models, generate
predictions; run diagnostics; run strategy / signals / PnL / backtests; create
`data/research` outputs; run feature ranking / selection / pruning /
hyperparameter / threshold / calibration tuning; flip `research_eligible`;
transition `eligibility_gate_status`; create a chronological split policy; read
the v002 terminal normalized window, the v002 terminal raw window, the sealed
test split, or the published normalized `__v002` Parquet family; read or mutate
the published feature `__v002` artefacts or manifest; create v003; create a
database, `.duckdb`, or `.sqlite`; compact Parquet; migrate storage; acquire
data; call any endpoint; download any archive; or use credentials / `.env` /
`.mcp.json` / MCP / Graphify / WebSocket / private or authenticated endpoints.
The Phase 4aw `flip_research_eligible(...)` always-raises invariant was never
invoked. No successor is authorized.

## 4. Evidence base and input boundary

Documents and tooling reviewed read-only before execution: the Phase 4bn-R
feature manifest/versioning memo, closeout, and merge-closeout; the Phase
4bn-Q feature-derivation readiness plan; the Phase 4bn-P normalized-layer gate
report; the Phase 4bn-O normalization report and segment manifest; the Phase
4bn-N and 4bn-L memos; the process standards (workflow, risk-tiering,
merge-closeout, operator-report, phase-prompt-template); and the committed
feature tooling (`features_schema_v002.py`, `features_compute_v002.py`,
`features_io.py`, `features_io_v002.py`, `features_manifest_v002.py`,
`features_schema.py`, `multiday_feature_gate*.py`, `scripts/phase4bm_h_*.py`)
and tests.

The exact feature **input** boundary was the Phase 4bn-O normalized segment
only:

- Source normalized segment manifest:
  `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json`
  (SHA256 `0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa`;
  sidecar SHA256
  `5d7dcbefbafcc81f2fcb1977ff9f35b08d58684542608317368c1f60f11e6402`).
- Source normalized-layer gate report:
  `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o__phase-4bn-p__1780599605192__3fd795ceac4f.json`
  (SHA256 `3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134`;
  verdict `NORMALIZED_LAYER_GATE_PASSED__LOCAL_NORMALIZED_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`,
  25 / 25 PASS).
- 275 normalized Parquet files + 275 canonical sidecars for 2024-03-01 ..
  2024-11-30, each SHA-verified against the segment manifest inventory.

No date ≥ 2024-12-01, no v002 terminal normalized/raw file, no sealed-test
file, no `data/research` artefact, and no published normalized/feature
`__v002` Parquet was read.

## 5. Phase 4bn-R feature manifest/versioning convention carried forward

The Phase 4bn-R selected convention was followed exactly:

- Shape: phase-scoped feature **segment** manifest, tied to the existing v002
  feature family, marked a pre-v002 backward segment / extension; not a new
  `__vNNN`, not v003, not a write into the published `__v002` feature family,
  which remains immutable; reads no v002 terminal normalized dates and touches
  no sealed-test dates.
- Inner identity:
  `dataset_family = "microstructure_features_aggtrades_v001"`,
  `dataset_version = "v002"`, `version = "v002"`,
  `feature_schema_version = "v001"`, `segment_label = "pre_v002_segment"`,
  `data_family = "aggTrades"`, `symbol = "BTCUSDT"`,
  `market = "usdm_futures"`, `dataset_category = "features"`.
- Output directory:
  `data/microstructure/features/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s/BTCUSDT/<YYYY>/<MM>/`
  (version-suffixed segment dir distinct from the published `__v002/` feature
  dir).
- Manifest path:
  `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s.json`
  (+ canonical `.sha256`).
- Full-envelope by reference only (`full_intended_envelope_start =
  "2024-03-01"`, `full_intended_envelope_end = "2025-02-28"`) plus an
  `existing_v002_feature_reference` block (`read = false`, `mutated = false`).
  The optional full-envelope reference / assembly manifest was **not** created
  in this phase (deferred per the Phase 4bn-R preferred option).

## 6. Phase 4bn-R non-eligible-source precondition carried forward

The Phase 4bn-R selected non-eligible-source precondition was enforced exactly:

- Source admissibility predecessor is the **Phase 4bn-P normalized-layer gate
  report** (SHA256 `3452fd9d…d322e27af134`, PASS, 25 / 25), not a Stage-3
  successor-state.
- Source normalized segment is the **Phase 4bn-O normalized segment manifest**
  (SHA256 `0e96ae37…ab32d6bdd9fa`), not the published normalized `__v002`
  manifest.
- The source segment was verified to remain `research_eligible = false`,
  `eligibility_gate_status = "pending"`. No `research_eligible: true` was
  required; no Stage-3 successor-state was required or created.
- The generated feature outputs remain `research_eligible = false`,
  `eligibility_gate_status = "pending"`, `no_successor_authorization = true`,
  `source_eligibility_posture = "non_eligible_gate_passed_pending"`. The
  manifest carries **no** Stage-3 successor-state field. The Phase 4aw
  `flip_research_eligible(...)` always-raises invariant was never invoked.

Per-row lineage column documentation (recorded in the manifest
`lineage_column_value_map`): `source_normalized_manifest_sha256` holds the
4bn-O segment manifest SHA; `source_phase_4bm_d_gate_report_sha256` holds the
**Phase 4bn-P normalized-layer gate report SHA** for this segment; and
`source_successor_state_sha256` carries an explicit non-eligible sentinel
(`non_eligible_pre_v002_segment_no_successor_state`) because no Stage-3
successor-state exists for this segment.

## 7. Phase 4bn-L budget carried forward

Feature-layer caps from the Phase 4bn-L derived-stack storage-budget memo were
applied: feature footprint warning 50 GiB / hard cap 100 GiB; runtime warning
4 h / hard cap 8 h; temporary workspace warning 50 GiB / hard cap 100 GiB;
total derived-stack warning 250 GiB / hard cap 300 GiB; D: free-space preflight
floor 500 GiB; in-execution floor 350 GiB. The wrapper measured footprint, D:
free space, temp peak, and elapsed at day/month boundaries; warns on any
warning threshold; fails closed on any hard cap, on preflight estimates over a
hard cap, on D: free below 500 GiB at preflight, or on D: free below 350 GiB
during execution.

## 8. Feature input contract

BTCUSDT only; Binance USDⓈ-M futures only; aggTrades only; Phase 4bn-O pre-v002
normalized layer only; 2024-03-01 .. 2024-11-30 inclusive UTC; 275 dates; 275
normalized Parquet + 275 sidecars; total source rows/events 400,001,695; total
normalized footprint 3,954,532,918 bytes. All input SHAs verified against the
segment manifest and the Phase 4bn-P gate report before any write; all
preconditions PASS (checks 4bn-S.1 .. 4bn-S.7).

## 9. Feature output contract

Feature artefacts only; 2024-03-01 .. 2024-11-30 inclusive UTC; output family
directory
`data/microstructure/features/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s/BTCUSDT/<YYYY>/<MM>/BTCUSDT-features-aggtrades-<YYYY-MM-DD>.parquet`;
every feature Parquet paired with a canonical `.sha256` sidecar; one feature
segment manifest + sidecar under
`data/microstructure/manifests/`. All outputs local and gitignored; none
committed; no `data/research` output; no labels, ML, diagnostics, strategy, or
backtests.

## 10. Implementation path

A bounded new wrapper `scripts/phase4bn_s_compute_pre_v002_features.py` was
created. It reuses the locked feature primitives unchanged:
`compute_aggtrades_features_v002`, `slice_prior_day_tail`,
`write_feature_dataset_v002`, `FeatureLineageV002`, `CROSS_DAY_TAIL_BUFFER_MS`
(from `features_compute_v002`); `build_feature_config_v002`,
`FEATURE_SCHEMA_V002` and policy constants (from `features_schema_v002`);
`feature_dtypes_v002`, `REQUIRED_V002_BOUNDARY_CONFIRMATIONS`,
`REQUIRED_V002_NON_AUTHORIZATION_FLAGS` (from `features_manifest_v002`); and the
atomic / sidecar / path-discipline helpers (from `features_io`). No locked
prior-phase script and no source module was modified.

The full `build_feature_manifest_v002` builder is Stage-3-specific (it requires
a Stage-3 successor-state SHA and hardcodes the Phase 4bm-H published-window
lineage), so the bounded wrapper builds the pre-v002 **segment** manifest
itself from the locked schema constants — the Phase 4bn-R "primitives only"
path. The wrapper adds only: non-eligible-source precondition enforcement
(4bn-O segment manifest + 4bn-P gate report); exact date-range / BTCUSDT-only /
aggTrades-only / forbidden-scope-token / segment-naming guards; a static
no-network posture (no networking import; HEAD read directly from `.git`);
normalized-input SHA verification; Phase 4bn-L preflight and per-day/month
budget enforcement; segment output naming; refuse-overwrite with atomic
write-then-rename; canonical sidecars; and post-write source immutability
re-hashing.

A focused offline test module
`tests/research/microstructure/test_phase4bn_s_feature_pre_v002.py` (32 tests)
was added using temp directories and small synthetic v002 normalized Parquet
fixtures (reusing the locked `_multiday_features_fixtures_v002` writer). No
network, no real local production data, no sealed-test data, and not the full
275-day dataset are touched by the tests.

## 11. Preflight results

All preconditions PASS. Preflight (Phase 4bn-L): D: free at preflight
1,334,218,002,432 bytes (≈1242.6 GiB) ≥ 500 GiB floor; estimated feature
footprint 64,000,271,200 bytes (≈59.6 GiB) ≤ 100 GiB hard cap (above the 50 GiB
warning → recorded warn); estimated temp ≪ 100 GiB; estimated total
derived-stack ≪ 300 GiB. No hard cap exceeded at preflight; execution
authorized to proceed.

## 12. Feature execution result

`FEATURE_EXECUTION_SUCCEEDED__LOCAL_FEATURE_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`.
Produced 275 / 275 feature Parquets; total feature rows 400,001,695 =
source event count (event-aligned, one feature row per source row). Per-day
causal cross-day lookback applied (prior segment day's 60 s tail loaded for
each day ≥ day 2); day 1 (2024-03-01) used no pre-segment read and its early
rows carry `rolling_missing_window_flag = true` per the locked v002 schema;
day 275 (2024-11-30) required no forward read into 2024-12-01. All 25 month /
aggregate / manifest / write / immutability checks PASS.

## 13. Feature artefacts created (gitignored, uncommitted)

- 275 feature Parquet files + 275 canonical `.sha256` sidecars under
  `data/microstructure/features/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s/BTCUSDT/<YYYY>/<MM>/`.
- First date 2024-03-01 (1,434,196 rows); last date 2024-11-30 (651,399 rows);
  sum across the 275-entry inventory = 400,001,695.
- Total feature footprint 54,254,406,538 bytes (≈50.53 GiB).

## 14. Feature manifest and sidecars

- Feature segment manifest:
  `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s.json`
  — SHA256 `4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52`.
- Manifest sidecar:
  `…__v002_pre_v002_segment_4bn_s.json.sha256`
  — SHA256 `f2ca2f48a5ac8ccfb892d0460cdfbbbb891451b9d94135adb3bff0936c8592e5`
  (canonical two-space body
  `4881eb87…  microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s.json\n`).
- `feature_config_hash`
  `0726b41d48e5f7127728c385b150d90fad91a92b3400c0545649b541e4dd114c`;
  `feature_schema_hash`
  `bf3d80bcf387970d5ad3dd85d99bd657cfd82527c6fe49f544f53f096a7a0ff5`.
- The manifest records all required fields: identity / versioning; schema
  description (62 = 17 lineage + 45 feature/quality column names in canonical
  order, dtypes); kernel policy (`leakage_policy =
  "causal_only_no_future_lookahead"`, `cross_day_lookback_policy =
  "causal_cross_day_lookback"`, `cross_day_tail_buffer_ms = 60000`,
  1s/5s/15s/60s windows, boundary / invalid-window / tie-rule / timestamp
  policies, forbidden-substring tokens); window / 275-date inventory with
  per-date feature parquet path+SHA+size, sidecar path+SHA, paired source
  normalized parquet path+SHA, first/last `transact_time_ms`, min/max
  `agg_trade_id`, status; source linkage (4bn-O segment manifest + 4bn-P gate
  report paths/SHAs, `source_normalized_schema_version =
  "NORMALIZED_SCHEMA_V001"`, `source_eligibility_posture =
  "non_eligible_gate_passed_pending"`); `existing_v002_feature_reference`
  (read/mutated false); full-envelope by reference; eligibility / governance
  posture; 18-key boundary confirmations (all true, incl. `no_future_lookahead`
  and `phase_4aw_flip_research_eligible_invariant_preserved`); 8-flag
  non-authorization set (all false, incl. `successor_authorization_after`);
  terminal-window / sealed-test witnesses; partitioning / primary-key / storage
  / sidecar policy; and Phase 4bn-L budget witnesses. No forbidden field is
  present (recursive key-substring scan, declaration subtrees explicitly
  validated).

## 15. Integrity and schema validation

Each feature Parquet has exactly the locked 62-column `FEATURE_SCHEMA_V002`
(17 lineage + 45 feature/quality) in canonical order (first and last day
re-checked post-run; the kernel and the wrapper both assert column order and
the forbidden-substring column guard). `FEATURE_SCHEMA_VERSION_V002 = "v001"`
preserved. Every feature Parquet and the manifest have a canonical `.sha256`
sidecar (LF only, no BOM, two-space separator, basename match). Post-write
source immutability re-hash confirmed the 4bn-O segment manifest, the 4bn-P
gate report, and all 275 normalized Parquets byte-identical pre/post.

## 16. Budget and runtime results

- Measured feature footprint 54,254,406,538 bytes (≈50.53 GiB) — above the
  50 GiB warning, below the 100 GiB hard cap.
- Measured runtime (run body) 14,321.72 s (≈3.98 h) — **below** the 4 h
  warning and the 8 h hard cap (total process ≈14,342 s).
- Measured temp workspace peak (pre-cleanup) 882,430,048 bytes (≈0.82 GiB);
  post-cleanup 0 (atomic `.tmp` renamed into final path each day).
- D: free at preflight 1,334,218,002,432 bytes (≈1242.6 GiB); minimum observed
  during execution 1,279,962,128,384 bytes (≈1192.1 GiB) — never near the
  350 GiB in-execution floor.
- `warning_thresholds_crossed = ["feature_warn"]`; `hard_caps_crossed = false`.

## 17. Gitignore and non-commit verification

`data/microstructure/` is gitignored (`.gitignore:85`) and `data/research/`
(`.gitignore:88`). `git status --short` shows only the two new tracked source
files (`scripts/phase4bn_s_compute_pre_v002_features.py`,
`tests/…/test_phase4bn_s_feature_pre_v002.py`) and the expected untracked
`.claude/scheduled_tasks.lock`. No feature Parquet, sidecar, segment manifest,
or manifest sidecar is staged or tracked. No `data/microstructure` or
`data/research` artefact is committed. `git diff --check` clean.

## 18. Sealed-test and v002 terminal preservation

`v002_terminal_window_mode = "by_reference"`; `existing_v002_terminal_window`
`read = false`, `normalized_dates_read = false`;
`existing_v002_feature_reference` `read = false`, `mutated = false`;
`sealed_test_split_touched = false`; `test_holdout_touched = false`;
`test_rows_loaded = 0`. No date ≥ 2024-12-01 was read. The published feature
`__v002` manifest
(`data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json`)
and Parquet family were neither read nor mutated (refuse-overwrite + distinct
segment basename; the published manifest path was never opened). No v003 path,
no `.duckdb` / `.sqlite`, and no compacted Parquet was created.

## 19. Validation

Commands run from `D:\Prometheus`:

- `git status --short` — only the two new source files + `scheduled_tasks.lock`.
- `git diff --check` — clean.
- `ruff check scripts/phase4bn_s_compute_pre_v002_features.py tests/research/microstructure/test_phase4bn_s_feature_pre_v002.py`
  — All checks passed.
- `pytest tests/research/microstructure/test_phase4bn_s_feature_pre_v002.py`
  — 32 passed.
- `pytest tests/research/microstructure/test_phase4bn_p_normalized_layer_gate.py`
  — passed.
- `pytest tests/research/microstructure/test_phase4bn_o_normalization_pre_v002.py`
  — passed.
- `pytest tests/research/microstructure/test_normalize_io.py
  test_normalize_validation.py test_normalize_manifest.py` — passed
  (combined required-suite run: 126 passed).
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- The wrapper was run once over the real local pre-v002 normalized segment
  (`--dry-run` first, then full run); all 25 checks PASS;
  result `FEATURE_EXECUTION_SUCCEEDED__…__REMAIN_PAUSED`.

## 20. Result state

`FEATURE_EXECUTION_SUCCEEDED__LOCAL_FEATURE_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`.

## 21. Decision

`RECOMMEND_AUTHORIZE_FEATURE_LAYER_ELIGIBILITY_GATE__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
Feature execution succeeded and all outputs / manifests / sidecars were
created; per the Phase 4bn-S decision rules the recommended successor is a
future, separately authorized **feature-layer eligibility gate only**.

## 22. Recommended state and successor options

Recommended state: **remain paused**. A future feature-layer eligibility gate
(separately authorized) should: validate the feature segment manifest
required-field contract; verify forbidden fields are absent; validate per-date
feature parquet + sidecar presence and SHA256s; recompute aggregates; validate
predecessor integrity (4bn-O segment manifest + 4bn-P gate report); confirm the
published feature `__v002` was not mutated; confirm the v002 terminal
normalized window and sealed-test split were not read; confirm the schema is
exactly `FEATURE_SCHEMA_V002`; and confirm `research_eligible` remains false and
`eligibility_gate_status` remains pending. A passing feature-layer gate must
not flip eligibility and must not authorize labels, ML, diagnostics, strategy,
or any successor. Acceptable docs-only alternatives (each subject to separate
operator authorization) remain a holdout-boundary memo, a source-policy
documentation memo, or a process-doc path-string update.

## 23. Explicit non-authorizations

No acquisition was run; no endpoint was called; no archive was downloaded; no
HEAD preflight was run; no raw gate was rerun; no normalization was rerun; no
normalized-layer gate was rerun; no feature-layer gate was run; no labels were
derived; no targets / future returns were computed; no ML was trained; no model
scoring or predictions were produced; no diagnostics were run; no strategy /
signal / PnL / backtest work was performed; no storage migration occurred; no
database / `.duckdb` / `.sqlite` was created; no Parquet was compacted; no v003
dataset was created; no v002 terminal normalized window or raw window was read;
no sealed-test data was read; no test holdout was touched; no manifest
eligibility transition occurred; no `chronological_split_policy` was created;
no published normalized / feature `__v002` artefact was read or mutated; no
`data/research` artefact was created; no `data/microstructure` or
`data/research` artefact was committed; and no paper / shadow / live /
exchange-write / credentials / `.env` / `.mcp.json` / MCP / Graphify /
WebSocket work was authorized. No successor is authorized from inside Phase
4bn-S.

## 24. Current-project-state update summary

`docs/00-meta/current-project-state.md` received a narrow update: a new Phase
4bn-S prose paragraph and a new `Current phase:` block recording the
feature-only success, the non-eligible posture, the segment manifest
SHA256 / sidecar SHA256, the 275 / 400,001,695 / 50.53 GiB result, and the
`RECOMMEND_AUTHORIZE_FEATURE_LAYER_ELIGIBILITY_GATE` decision. Prior Phase
4bn-A … 4bn-R paragraphs and `Current phase:` blocks are preserved as labelled
historical context. No other section was changed.
