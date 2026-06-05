# Phase 4bn-T — Feature-Layer Eligibility Gate

## 1. Purpose

Phase 4bn-T executes a bounded, read-only **feature-layer eligibility gate**
over the Phase 4bn-S local, gitignored, non-eligible pre-v002 BTCUSDT Binance
USDⓈ-M futures aggTrades **feature segment** (2024-03-01 .. 2024-11-30 inclusive
UTC; 275 dates; 400,001,695 feature rows). The gate validates that the feature
segment created by Phase 4bn-S is structurally complete, internally consistent,
manifest-consistent, predecessor-consistent, schema-consistent, path-consistent,
sidecar-consistent, governance-consistent, and leakage-boundary-consistent, and
writes exactly one local gitignored feature-layer gate report + canonical
sidecar. It authorizes no successor and flips no eligibility.

**Result:**
`FEATURE_LAYER_GATE_PASSED__LOCAL_FEATURE_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`
(27 / 27 checks PASS; runtime 348.9 s).

## 2. Authority and repository state

- **Active local repo path:** `D:\Prometheus`.
- **Active Claude workspace:** `D:\ClaudeRuns\prometheus-light`.
- **GitHub remote:** `origin` → `https://github.com/jpedrocY/Prometheus.git`
  (verified intact).
- **Branch:** `phase-4bn-t/feature-layer-eligibility-gate`.
- **Base `main` SHA:** `e647435c81d784f610b9cf8b5e2f2dc8ee0e914e`
  (`docs(phase-4bn-s): finalize merge closeout shas`; short `e647435`).
  Pre-branch `main == origin/main == HEAD` verified in sync. Predecessor chain
  confirmed present on `main`: Phase 4bn-S finalization `e647435`,
  merge-closeout `1314c27`, merge `8005fb5`, branch `9679d9a`; Phase 4bn-R
  finalization `40f0b3e`.
- **Working tree at phase start:** only the expected untracked transient
  `.claude/scheduled_tasks.lock`; gitignored `data/microstructure/` present
  locally and uncommitted.

## 3. Phase type and strict scope

Tier 1 — Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md`
§3: feature-layer eligibility gate / local gitignored feature artefact
validation / code + tests + docs + local gate-report phase.

Phase 4bn-T did **not**: rerun feature execution; mutate the feature segment
manifest, any feature Parquet, any feature sidecar, or the published feature
`__v002` family; read the v002 terminal normalized window, the v002 terminal
raw window, the sealed-test split, the published normalized `__v002` Parquet
family, or any published feature `__v002` Parquet; derive labels / targets /
future returns; run ML / score models / generate predictions; run diagnostics /
strategy / signals / PnL / backtests; rerun the raw gate, normalization, or the
normalized-layer gate; flip `research_eligible`; transition
`eligibility_gate_status`, `chronological_split_policy`,
`diagnostics_authorized`, or `ml_authorized`; create a database / `.duckdb` /
`.sqlite`; compact Parquet; migrate storage; create v003; acquire data; call any
endpoint; download any archive; or use credentials / `.env` / `.mcp.json` / MCP /
Graphify / WebSocket / private or authenticated endpoints. The Phase 4aw
`flip_research_eligible(...)` always-raises invariant was never invoked. No
successor is authorized.

## 4. Evidence base and input boundary

Documents and tooling reviewed read-only before building the gate: the process
standards (workflow, risk-tiering, merge-closeout, operator-report,
phase-prompt-template); the Phase 4bn-S feature-only execution report and
closeout; the Phase 4bn-R feature manifest/versioning memo; the Phase 4bn-P
normalized-layer gate report; the Phase 4bn-O normalization report and segment
manifest; the Phase 4bn-L derived-stack storage-budget memo; the data-domain
docs; the locked feature schema/IO/manifest modules (`features_schema_v002.py`,
`features_schema.py`, `features_io.py`, `normalize_io.py`); and the
directly-analogous Phase 4bn-P normalized-layer gate runner and its tests, which
this gate mirrors in shape and discipline.

The gate's input boundary is the Phase 4bn-S feature segment only:

- Feature segment manifest
  `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s.json`
  (SHA256 `4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52`)
  + canonical sidecar
  (SHA256 `f2ca2f48a5ac8ccfb892d0460cdfbbbb891451b9d94135adb3bff0936c8592e5`).
- 275 feature Parquet files + 275 canonical `.sha256` sidecars.
- Predecessor evidence read read-only for SHA/verdict validation only: the
  Phase 4bn-O normalized segment manifest
  (SHA256 `0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa`) +
  its sidecar
  (SHA256 `5d7dcbefbafcc81f2fcb1977ff9f35b08d58684542608317368c1f60f11e6402`),
  and the Phase 4bn-P normalized-layer gate report
  (SHA256 `3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134`).

No date ≥ 2024-12-01, no v002 terminal normalized/raw file, no sealed-test
file, no published normalized/feature `__v002` Parquet, and no published feature
`__v002` manifest was opened. The published feature `__v002` reference was
treated by-reference only.

## 5. Phase 4bn-S feature segment carried forward

The gated segment is exactly the Phase 4bn-S output: BTCUSDT only; Binance
USDⓈ-M futures only; aggTrades only; feature dataset only; 2024-03-01 ..
2024-11-30 inclusive UTC; 275 dates; 275 feature Parquets + 275 sidecars; total
feature rows 400,001,695 (= source event count, event-aligned); total footprint
54,254,406,538 bytes (parquet + sidecar bytes; ≈50.53 GiB); locked 62-column
`FEATURE_SCHEMA_V002` (17 lineage + 45 feature/quality); `research_eligible =
false`, `eligibility_gate_status = "pending"`, `no_successor_authorization =
true`.

## 6. Phase 4bn-R feature manifest/versioning convention carried forward

The gate validates the Phase 4bn-R convention exactly: a phase-scoped feature
**segment** manifest tied to the existing v002 feature family
`microstructure_features_aggtrades_v001` (`dataset_version = "v002"`, `version =
"v002"`, `feature_schema_version = "v001"`, `segment_label =
"pre_v002_segment"`); version-suffixed segment directory
`…__v002_pre_v002_segment_4bn_s/` path-disjoint from the published `__v002/`
feature directory; non-eligible-source precondition anchored on the Phase 4bn-P
normalized-layer gate report over the Phase 4bn-O normalized segment manifest
(not a Stage-3 successor-state); full-envelope by reference only
(`full_intended_envelope_start = "2024-03-01"`, `full_intended_envelope_end =
"2025-02-28"`); `existing_v002_feature_reference` with `read = false`,
`mutated = false`.

## 7. Feature-layer gate input contract

BTCUSDT only; Binance USDⓈ-M futures only; aggTrades only; feature dataset only;
the Phase 4bn-S pre-v002 feature segment only. Expected: 275 dates; 275 feature
Parquets; 275 feature sidecars; total feature rows 400,001,695; total footprint
54,254,406,538 bytes; feature manifest SHA256
`4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52`; manifest
sidecar SHA256
`f2ca2f48a5ac8ccfb892d0460cdfbbbb891451b9d94135adb3bff0936c8592e5`; schema
`FEATURE_SCHEMA_V002` exactly (62 columns = 17 lineage + 45 feature/quality);
predecessor SHAs as in §4; non-eligible / pending / no-successor posture.

## 8. Feature-layer gate implementation path

The committed feature gate tooling (`multiday_feature_gate*`,
`scripts/phase4bm_j_run_multiday_feature_gate.py`) is hardcoded to the published
`__v002` 90-day terminal window, the published `__v002` feature manifest shape,
and a Stage-3 research-eligible successor-state precondition; it is not reusable
for the non-eligible pre-v002 **segment**. As Phase 4bn-P did for the normalized
layer, Phase 4bn-T therefore added one bounded, read-only gate runner
`scripts/phase4bn_t_validate_feature_pre_v002_gate.py` reusing only the locked
generic SHA / sidecar / path-discipline primitives (`compute_file_sha256`,
`compute_bytes_sha256`, `write_sha256_sidecar`,
`assert_path_under_microstructure`, `NormalizationIOError`) and the locked
feature schema constants (`FEATURE_SCHEMA_V002`, `LINEAGE_COLUMNS_V002`,
`FEATURE_NAMES_V002`, `FEATURE_SCHEMA_VERSION_V002`,
`FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS_V002`). No source module and no locked
prior-phase script was modified. The runner is network-free (no networking
import; static no-network test enforces this) and writes at most one gitignored
gate report + canonical sidecar via atomic refuse-overwrite under
`data/microstructure/gate-reports/features/`.

Performance discipline mirrors Phase 4bn-P: for all 275 files the gate streams
the full Parquet SHA256, records on-disk size, and reads
`ParquetFile.metadata` for the row count and column names (no row-group
materialisation); bounded row-level deep checks run on a predeclared 10-date
sample (month-firsts + 2024-11-30) reading only the identity/lineage columns.
Per-file SHA equality to the manifest inventory transitively confirms the
non-sampled files match what Phase 4bn-S verified.

A focused offline test module
`tests/research/microstructure/test_phase4bn_t_feature_layer_gate.py`
(31 tests) was added using temp directories and small synthetic 62-column
feature Parquet fixtures. No network, no real production data, no sealed-test
data, and not the full 275-day dataset are touched by the tests.

## 9. Gate checks performed

27 checks total, all PASS: manifest SHA; manifest canonical sidecar; manifest
required-fields; identity/scope; base_commit_sha; schema-description
(counts/order/hashes vs `FEATURE_SCHEMA_V002`); leakage/causal/window policy;
window/inventory totals; predecessor lineage SHAs/posture;
non-eligible/by-reference/sealed/boundary/non-authorization posture;
partition/primary-key/storage/sidecar policy; forbidden field-name absence;
275 contiguous in-segment dates; all-files-present; hash integrity
(parquet == sidecar == inventory); path layout + basename; per-file schema ==
`FEATURE_SCHEMA_V002`; forbidden columns absent; per-file row counts;
adjacent-date non-overlap (274 pairs); 10-date deep row-level sample;
recomputed total rows == 400,001,695; recomputed footprint == 54,254,406,538 B;
275 parquets + 275 sidecars; predecessor normalized manifest + sidecar SHA;
predecessor normalized-layer gate SHA + verdict + 25/25 PASS; published `__v002`
path-disjoint / by-reference / not mutated.

## 10. Local gate outputs

Exactly one local gitignored gate report + canonical sidecar (uncommitted):

- `data/microstructure/gate-reports/features/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s__phase-4bn-t__1780674917156__e647435c81d7.json`
  — SHA256 `db731d1be06295404ef195d9b5b5bad8010ce6ae6efef43ece90c29653d6ab08`.
- `…__phase-4bn-t__1780674917156__e647435c81d7.json.sha256`
  — SHA256 `12d2e437f444f8445306f6c3eebbf77821d59428d23dc621f3e39a541bd986ea`
  (canonical two-space body, LF only, no BOM).

The report records `phase = phase-4bn-t`, `base_commit_sha =
e647435c81d784f610b9cf8b5e2f2dc8ee0e914e`, the input feature manifest path +
SHA256, the input feature segment directory, the result state, `segment_non_eligible:
true`, `research_eligible_after: false`, `eligibility_gate_status_after:
pending`, `no_successor_authorization: true`, `feature_execution_rerun: false`,
`v002_terminal_window_read: false`, `sealed_test_split_touched: false`,
`published_v002_mutated: false`, `data_committed: false`, and the predecessor
SHAs / verdict.

## 11. Date coverage result

PASS. Exactly 275 dates; starts 2024-03-01; ends 2024-11-30; contiguous daily
calendar with no missing/duplicate date; no date ≥ 2024-12-01; no v002 terminal
date; no sealed-test date (2025-02-14 .. 2025-02-28); manifest
`per_file_inventory` dates == `date_list` == the generated contiguous calendar.

## 12. Path, sidecar, and hash integrity result

PASS. Every feature Parquet lives under
`…/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s/BTCUSDT/<YYYY>/<MM>/`
with basename `BTCUSDT-features-aggtrades-<YYYY-MM-DD>.parquet`; each is
path-disjoint from the published `__v002` and generic `v001` directories and
contains no v003 path. Each feature Parquet has exactly one canonical `.sha256`
sidecar (`<sha256>  <basename>\n`, two spaces, LF only, no BOM, basename match).
The recomputed SHA256 of every feature Parquet matches its sidecar and the
manifest `per_file_inventory`; the feature segment manifest SHA256 matches its
sidecar and equals the expected
`4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52`.

## 13. Manifest required-field and forbidden-field result

PASS. All Phase 4bn-R required fields are present with the expected values
(identity/versioning; 62/17/45 column counts; `feature_column_names` in canonical
`FEATURE_SCHEMA_V002` order, `lineage_column_names` == `LINEAGE_COLUMNS_V002`,
`computed_feature_column_names` == `FEATURE_NAMES_V002`; `feature_config_hash`
`0726b41d…0ff5`-prefixed locked value and `feature_schema_hash`
`bf3d80bc…0ff5`; causal kernel policy; 1s/5s/15s/60s windows;
`cross_day_tail_buffer_ms = 60000`; window/inventory totals; source lineage;
non-eligible posture; 18-key boundary confirmations all true; 8-flag
non-authorization set all false; partition/primary-key/storage/sidecar policy;
budget witnesses). The recursive forbidden field-name scan (skipping the
governance / non-authorization / boundary / dtype declaration subtrees) found no
forbidden token: no `label_*`/`target_*`/`future_*`, model/prediction/score,
signal/entry/exit, PnL/equity/position/backtest, MFE/MAE/R-multiple/barrier,
mark-price/funding/open-interest/order-book/cross-venue, ETHUSDT, v003,
`chronological_split_policy`, research-ready/admissible/approved-for-backtest, no
`eligibility_gate_status` other than `"pending"`, and no `diagnostics_authorized`
/ `ml_authorized` set true.

## 14. Schema and feature Parquet validation result

PASS. Every feature Parquet's column set equals the locked 62-column
`FEATURE_SCHEMA_V002` in canonical order (metadata for all 275; full
identity-column deep checks on the 10-date sample); `FEATURE_SCHEMA_VERSION_V002
= "v001"`; the 26-token forbidden-substring column guard passes; `dataset_version
= "v002"`, `source_dataset_version = "v002"`, `feature_schema_version = "v001"`,
`symbol = "BTCUSDT"`, `utc_date = <expected date>` confirmed on sampled
first/last rows. No label/target/future/model/prediction/score/signal/PnL/
strategy/diagnostic/backtest/mark-price/funding/open-interest/order-book/spot/
cross-venue/tick/ETHUSDT column is present.

## 15. Row-count and aggregate validation result

PASS. Recomputed total feature rows from Parquet metadata = **400,001,695**
(exact); per-date row counts equal the manifest inventory; recomputed total
footprint (parquet + sidecar bytes) = **54,254,406,538 B** (exact); 275 feature
Parquets + 275 sidecars confirmed. First date 2024-03-01 = 1,434,196 rows; last
date 2024-11-30 = 651,399 rows. Feature rows remain event-aligned one-per-source
row (sampled `row_index = 0..n-1`, `feature_timestamp_ms ==
source_transact_time_ms`).

## 16. Leakage / causal-policy validation result

PASS. `leakage_policy = "causal_only_no_future_lookahead"`,
`cross_day_lookback_policy = "causal_cross_day_lookback"`,
`cross_day_tail_buffer_ms = 60000`. On sampled dates, `feature_timestamp_ms`
equals `source_transact_time_ms` exactly (no future alignment), all source
timestamps fall within the date's UTC bounds, transact times are monotone
non-decreasing, and `agg_trade_id` is strictly increasing. No feature column or
manifest field implies future information; no sealed-test date participates in
any input, output, context, statistic, sample, or quality check.

## 17. Predecessor integrity result

PASS. The Phase 4bn-O normalized segment manifest SHA256 equals
`0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa` and its
sidecar SHA256 equals
`5d7dcbefbafcc81f2fcb1977ff9f35b08d58684542608317368c1f60f11e6402`; the Phase
4bn-P normalized-layer gate report SHA256 equals
`3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134`, with verdict
`NORMALIZED_LAYER_GATE_PASSED__LOCAL_NORMALIZED_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`,
`overall_status = pass`, 25 / 25 checks PASS, `segment_non_eligible = true`,
`research_eligible_after = false`. No raw zip was read; the normalized-layer gate
and normalization were not rerun.

## 18. Published `__v002` and sealed-test preservation

The published feature `__v002` family is path-disjoint from the segment
directory and its manifest basename; `existing_v002_feature_reference` records
`read = false`, `mutated = false`; the published feature `__v002` Parquet files
and manifest were never opened (by reference only). The v002 terminal normalized
window remains by reference only and unread (`existing_v002_terminal_window`
`read = false`, `normalized_dates_read = false`). No feature segment date
overlaps the sealed split 2025-02-14 .. 2025-02-28; `sealed_test_split_touched =
false`, `test_holdout_touched = false`, `test_rows_loaded = 0`. No sealed-test
file was read or used for any statistic/sample/quality check.

## 19. Gitignore and non-commit verification

`data/microstructure/` is gitignored (`.gitignore:85`) and `data/research/`
(`.gitignore:88`). `git status --short` shows only the two new tracked source
files (`scripts/phase4bn_t_validate_feature_pre_v002_gate.py`,
`tests/research/microstructure/test_phase4bn_t_feature_layer_gate.py`) plus the
expected untracked `.claude/scheduled_tasks.lock`. The local gate report +
sidecar are gitignored and uncommitted; no feature Parquet/sidecar/manifest and
no `data/microstructure` or `data/research` artefact is staged or committed.
`git diff --check` clean. No `data/research` output was created. No `.duckdb` /
`.sqlite` / v003 path was created.

## 20. Validation

Commands run from `D:\Prometheus`:

- `git status --short` — only the two new source files + `scheduled_tasks.lock`.
- `git diff --check` — clean.
- `ruff check scripts/phase4bn_t_validate_feature_pre_v002_gate.py tests/research/microstructure/test_phase4bn_t_feature_layer_gate.py`
  — All checks passed.
- `pytest tests/research/microstructure/test_phase4bn_t_feature_layer_gate.py`
  — 31 passed.
- `pytest tests/research/microstructure/test_phase4bn_s_feature_pre_v002.py
  test_phase4bn_p_normalized_layer_gate.py
  test_phase4bn_o_normalization_pre_v002.py` — 88 passed.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- The gate runner was run once over the real local pre-v002 feature segment
  (`--dry-run` first, then full run): 27 / 27 checks PASS; result
  `FEATURE_LAYER_GATE_PASSED__…__REMAIN_PAUSED`; runtime 348.9 s; gate report +
  canonical sidecar created (gitignored, uncommitted).

## 21. Result state

`FEATURE_LAYER_GATE_PASSED__LOCAL_FEATURE_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`.

## 22. Decision

`RECOMMEND_AUTHORIZE_LABEL_DERIVATION_READINESS_OR_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
After raw acquisition, the raw gate, normalization, the normalized-layer gate,
feature derivation, and now the feature-layer gate all passing for the pre-v002
segment, the next clean technical stage is a separately authorized
label-derivation readiness / execution-plan phase. That future step must still
run no ML, no diagnostics, no strategy, no PnL/backtests, flip no eligibility,
and use no sealed test split unless separately governed.

## 23. Recommended state and successor options

Recommended state: **remain paused**. Acceptable operator options (each subject
to separate authorization): remain paused; request a merge prompt for Phase
4bn-T; if the gate passed (it did), separately authorize a label-derivation
readiness or execution-plan phase; separately authorize a holdout-boundary memo
only if a future scope touches the v002 terminal raw/normalized window or
sealed-test dates; separately authorize a source-policy documentation memo;
separately authorize a process-doc `D:` path-string update; or reject further
ML-baseline successors and close the ML arc. No successor is authorized from
inside Phase 4bn-T.

## 24. Explicit non-authorizations

A passing feature-layer gate does **not** make the dataset research-eligible and
does not authorize label derivation, ML, diagnostics, strategy, PnL/backtests, a
chronological split policy, storage migration, v003, paper/shadow/live,
exchange-write, or any successor. No acquisition was run; no endpoint was
called; no archive was downloaded; no HEAD preflight was run; the raw gate,
normalization, and normalized-layer gate were not rerun; feature execution was
not rerun; no labels/targets/future returns were computed; no ML was trained; no
model scoring or predictions were produced; no diagnostics/strategy/signal/PnL/
backtest work was performed; no storage migration occurred; no database /
`.duckdb` / `.sqlite` was created; no Parquet was compacted; no v003 dataset was
created; no v002 terminal raw/normalized window was read; no sealed-test data
was read; no test holdout was touched; no manifest eligibility transition
occurred; no published normalized / feature `__v002` artefact was read or
mutated; no `data/research` artefact was created; no `data/microstructure` or
`data/research` artefact was committed; and no paper / shadow / live /
exchange-write / credentials / `.env` / `.mcp.json` / MCP / Graphify / WebSocket
work was authorized. The Phase 4aw `flip_research_eligible(...)` always-raises
invariant was preserved (never invoked).

## 25. Current-project-state update summary

`docs/00-meta/current-project-state.md` received a narrow update: a new Phase
4bn-T prose paragraph and a new `Current phase:` block recording the
feature-layer gate PASS (27 / 27), the non-eligible / pending / no-successor
posture, the feature manifest SHA256 / sidecar SHA256, the gate report path +
SHA256, the 275 / 275 / 400,001,695 / 54,254,406,538 B result, and the
`RECOMMEND_AUTHORIZE_LABEL_DERIVATION_READINESS_OR_EXECUTION_PLAN` decision.
Prior Phase 4bn-A … 4bn-S paragraphs and `Current phase:` blocks are preserved
as labelled historical context. No other section was changed.
