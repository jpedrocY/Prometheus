# Phase 4bi-A — Feature Artefact Structural QA Memo

## Phase header

- **Phase id:** Phase 4bi-A
- **Phase title:** Feature Artefact Structural QA Memo
- **Phase type:** analysis-and-docs structural QA memo (read-only)
- **Branch:** `phase-4bi-a/feature-artefact-structural-qa`
- **Base:** `main` at `c42f6187f7a3ce3257603a863dbd0dd7770fa36d`
- **Phase 4bh merge ancestor:** `03100d4267e0984342c622c88cb204218f953367`
- **Status:** complete

## Current state

Phase 4bi-A performs a read-only structural QA review of the on-disk Phase 4bh feature parquet and feature manifest against the Phase 4bh-B finalized feature schema contract, the Phase 4bh implementation result, and the Phase 4bh merge-closeout evidence. The output is this tracked analysis memo plus a closeout. **No tracked source, test, or script file is modified. No feature artefact is regenerated. No upstream artefact is mutated. No `research_eligible` flag is flipped. No successor phase is authorized.**

## Inputs reviewed

- Phase 4bh main memo: `docs/00-meta/implementation-reports/2026-05-10_phase-4bh_aggtrades-feature-computation.md`
- Phase 4bh closeout: `docs/00-meta/implementation-reports/2026-05-10_phase-4bh_closeout.md`
- Phase 4bh merge-closeout: `docs/00-meta/implementation-reports/2026-05-10_phase-4bh_merge-closeout.md`
- Phase 4bh-B feature schema finalization memo
- Phase 4bh-A feature-boundary design memo
- Phase 4bg-B successor-state JSON (SHA `8bcc7d01…`)
- Phase 4bf derived-family gate report (SHA `dd4e0c1c…`)
- Phase 4bb-D raw-family gate report (SHA `96f09159…`)
- Phase 4bd normalized parquet (SHA `2b3d6978…`) and derived manifest (SHA `f6f0d947…`)
- Phase 4az raw manifest (SHA `a371edd4…`) and raw zip (SHA `f560c2e5…`)
- M0 (Phase 4ak) twelve-clause gate + post-null cooldown + cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy

## Scope

Phase 4bi-A inspects the existing local gitignored feature artefacts produced by Phase 4bh:

- `data/microstructure/features/microstructure_features_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-features-aggtrades-2025-01-15.parquet` (224,382,279 B);
- paired `.sha256` sidecar (112 B);
- `data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json` (3,851 B);
- paired `.sha256` sidecar (116 B).

It verifies them against the Phase 4bh-B locked schema, the Phase 4bh real-run result, and the Phase 4bh merge-closeout's recorded SHAs.

## Non-scope

Phase 4bi-A did NOT:

- modify source code, tests, scripts, configs, README, pyproject, .gitignore, MCP files, or any prior governance memo;
- rerun the feature kernel; create a new feature parquet; create a new feature manifest;
- modify the existing feature parquet, feature manifest, or any sidecar;
- run the normalizer; rerun the raw eligibility gate; rerun the derived-family gate;
- generate a new raw, derived, or feature-family gate report;
- create a feature-family eligibility gate; create a feature-family successor-state artefact;
- create labels, targets, signals, ML, strategy, or backtests;
- compute PnL, MFE, MAE, R-multiple, equity, position state, alpha, edge, prediction, model score, decision score, entry/exit, or strategy output;
- acquire data; call public endpoints; call Binance APIs; open WebSockets; use private endpoints; request or use credentials; read or create `.env`; create or read `.mcp.json`; enable MCP or Graphify;
- flip `research_eligible` on any actual manifest;
- transition `eligibility_gate_status` on any actual manifest;
- authorize Stage-4 feature-family gate, Stage-5 research-use / ML-use decision, paper / shadow / live, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation;
- revise retained verdicts; change project locks; amend M0;
- authorize Phase 4bi-B, Phase 4bi-C, Phase 4bi-D, Phase 4bj, Phase 4bb-F, Phase 4bb-G, Phase 5, or Phase 4 canonical;
- commit anything under `data/microstructure/`.

## Phase 4bh dependency

Phase 4bi-A depends on the merged Phase 4bh implementation:

- Phase 4bh source commit: `fc47a2eb1940156eb6aa9675d5e565e8276be6f0`
- Phase 4bh merge commit: `03100d4267e0984342c622c88cb204218f953367`
- Phase 4bh closeout commit: `c42f6187f7a3ce3257603a863dbd0dd7770fa36d`
- Code commit SHA recorded inside feature outputs: `e99d2f3e5dcea2ceb8daa3428bbe72fd81d77293`
- Phase 4bh real-run result: 1,681,098 rows; compute 48.8 s, write 3.8 s; `validate_feature_dataset` `overall_status = pass` (135 / 135).

Phase 4bi-A reproduces the Phase 4bh validation result independently and adds 67 explicit structural QA checks plus 18 independent causal spot-checks plus a same-timestamp tie-break inspection.

## QA method

The QA was performed by an offline read-only Python orchestrator that:

1. recomputed SHA256 for the feature parquet, feature parquet sidecar, feature manifest, feature manifest sidecar, normalized parquet, normalized manifest, raw manifest, raw zip, Phase 4bb-D gate report, Phase 4bf gate report, and Phase 4bg-B successor-state JSON (read-only);
2. read the feature parquet via `pyarrow.parquet.read_table` (read-only);
3. read the source normalized parquet via `pyarrow.parquet.read_table` (read-only);
4. parsed the feature manifest, normalized manifest, and raw manifest as JSON (read-only);
5. compared every column of the feature parquet against the Phase 4bh-B locked schema, the source columns, and the recorded lineage SHAs;
6. ran 18 independent causal spot-checks at rows 0, 5, 100, 1000, 50000, 100000, 500000, 1000000, 1681097 for windows `1s` and `60s`, computing each window's expected count, aggressive buy / sell quantity (Decimal-exact), aggressive flow ratio, and log return from the source data and comparing to the feature parquet values bit-for-bit (Decimal equality; 1e-12 float tolerance);
7. verified the same-timestamp tie-break on the first same-`transact_time_ms` pair found in the source;
8. invoked `prometheus.research.microstructure.validate_feature_dataset` (which itself is read-only — no writes, no mutation) to reproduce the Phase 4bh `overall_status = pass` (135 / 135);
9. recomputed SHAs of all 7 upstream artefacts post-run to confirm immutability.

The orchestrator wrote a single gitignored JSON summary (`.phase4bi_a_qa_results.json`) and was deleted after the memo was drafted; it never mutated the feature parquet, the feature manifest, any sidecar, or any upstream artefact.

## Feature artefact paths

| Artefact | Path | Status | Size |
| --- | --- | --- | --- |
| feature parquet | `data/microstructure/features/microstructure_features_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-features-aggtrades-2025-01-15.parquet` | exists | 224,382,279 B |
| feature parquet sidecar | same path with `.sha256` suffix | exists | 112 B |
| feature manifest | `data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json` | exists | 3,851 B |
| feature manifest sidecar | same path with `.sha256` suffix | exists | 116 B |

All four are gitignored under `.gitignore:85: data/microstructure/`. None are tracked or staged in git.

## Hash and sidecar verification

| Check | Recomputed SHA256 | Expected SHA256 | Result |
| --- | --- | --- | --- |
| feature parquet | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` | MATCH |
| feature parquet sidecar text == recomputed parquet SHA | `618d9b86…1c1691f` | `618d9b86…1c1691f` | MATCH |
| feature manifest | `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718` | `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718` | MATCH |
| feature manifest sidecar text == recomputed manifest SHA | `624e8c5e…7fe718` | `624e8c5e…7fe718` | MATCH |

## Schema verification

- Feature parquet columns count: **61** ✓
- Feature parquet column order matches `FEATURE_SCHEMA_V001` exactly ✓
- Feature / quality column count: **45** ✓
- Lineage / identity / metadata column count: **16** ✓
- Feature manifest `feature_list` matches `FEATURE_NAMES_V001` (45 names in canonical order) ✓
- Feature manifest `window_list = ["1s", "5s", "15s", "60s"]` ✓
- Feature manifest `window_ms_list = [1000, 5000, 15000, 60000]` ✓
- Deferred windows (`30s`, `5m`) absent from columns ✓
- No forbidden column-name substring (out of 26 banned tokens) appears in any feature parquet column name ✓

## Row-count and row-alignment verification

- Feature parquet `num_rows = 1,681,098` ✓
- Feature manifest `row_count = 1,681,098` ✓
- Source normalized parquet `num_rows = 1,681,098` ✓
- Feature parquet rows == source normalized parquet rows ✓
- `row_index` column equals `[0, 1, …, 1,681,097]` (contiguous, ascending) ✓
- `agg_trade_id` column matches source normalized parquet `agg_trade_id` exactly (per-row) ✓
- `source_transact_time_ms` column matches source `transact_time_ms` exactly (per-row) ✓
- `feature_timestamp_ms` equals `source_transact_time_ms` for every row ✓

## Lineage-column verification

All 11 lineage / identity / metadata constants verified across all 1,681,098 rows:

| Column | Constant value |
| --- | --- |
| `dataset_family` | `microstructure_features_aggtrades_v001` |
| `dataset_version` | `v001` |
| `source_dataset_family` | `microstructure_normalized_aggtrades_v001` |
| `source_dataset_version` | `v001` |
| `source_feature_schema_version` | `v001` |
| `symbol` | `BTCUSDT` |
| `utc_date` | `2025-01-15` |
| `source_normalized_parquet_sha256` | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| `source_normalized_manifest_sha256` | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| `source_successor_state_sha256` | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |
| `source_phase_4bf_gate_report_sha256` | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |
| `feature_config_hash` | `49b4ec1fd63688cc11d72ea7286af6efe2bad8ac5c29da0438c0f65d571f0c77` |

All match the Phase 4bh merge-closeout's recorded SHAs and the feature manifest's recorded values.

## Manifest verification

- `dataset_family = microstructure_features_aggtrades_v001` ✓
- `dataset_version = v001` ✓
- `feature_schema_version = v001` ✓
- `symbol = BTCUSDT` ✓
- `utc_date = 2025-01-15` ✓
- `row_count = 1681098` ✓
- `invalid_windows = []` ✓
- `feature_config_hash = 49b4ec1f…571f0c77` ✓
- `research_eligible = false` ✓
- `eligibility_gate_status = "pending"` ✓
- All 8 required governance keys present (`phase_id`, `feature_computation`, `labels`, `ml`, `strategy`, `backtest`, `acquisition`, `stop_trigger_domain`) ✓
- Governance values locked: `phase_id = "4bh"`; `feature_computation = "allowed_by_phase_4bh"`; `labels = "forbidden"`; `ml = "forbidden"`; `strategy = "forbidden"`; `backtest = "forbidden"`; `acquisition = "unauthorized"`; `stop_trigger_domain = "trade_price_backtest_candidate"` ✓
- All 11 boundary confirmations true: `no_labels`, `no_targets`, `no_signals`, `no_ml`, `no_strategy`, `no_backtest`, `no_acquisition`, `no_network`, `no_credentials`, `no_manifest_mutation`, `no_source_artefact_mutation` ✓
- `files[0].sha256 == feature parquet SHA256` ✓
- `files[0].row_count == 1681098` ✓

## Dtype / null / NaN verification

- All count columns (`rolling_aggtrade_count_*`, `rolling_aggressive_buy_count_*`, `rolling_aggressive_sell_count_*` for windows `1s`, `5s`, `15s`, `60s`) have pyarrow type `int64` and `min >= 0` ✓
- All Decimal-as-string columns (`rolling_quantity_sum_*`, `rolling_quantity_mean_*`, `rolling_aggressive_buy_quantity_*`, `rolling_aggressive_sell_quantity_*`, `rolling_aggressive_quantity_imbalance_*`) parse via `decimal.Decimal(...)` for sampled values (5,000 per column × 5 column kinds × 4 windows) ✓
- All ratio columns (`rolling_aggressive_flow_ratio_*`) are either `null` or `float64` in `[0.0, 1.0]` and finite (no NaN, no inf) — verified across all 1,681,098 rows × 4 windows ✓
- All log-return columns (`rolling_log_return_past_window_*`) are either `null` or `float64` finite (no NaN, no inf) — verified across all 1,681,098 rows × 4 windows ✓
- `utc_hour` ∈ `[0, 23]` for all rows ✓
- `utc_minute` ∈ `[0, 59]` for all rows ✓
- `milliseconds_since_day_start` ∈ `[0, 86_399_999]` for all rows ✓

## Quality-flag verification

- `invalid_window_flag` pyarrow type is `bool_()` and every value is strict `bool` ✓
- `rolling_missing_window_flag` pyarrow type is `bool_()` and every value is strict `bool` ✓
- `invalid_window_flag` is `false` for all 1,681,098 rows (consistent with manifest `invalid_windows = []`) ✓
- `rolling_missing_window_flag` is `false` for all 1,681,098 rows ✓

## First / last row verification

**First row (`row_index = 0`):**

- `agg_trade_id` matches source row 0 ✓
- `source_transact_time_ms` matches source row 0 `transact_time_ms` ✓
- `row_index = 0` ✓
- `feature_timestamp_ms == source_transact_time_ms` ✓
- `rolling_aggtrade_count_1s = 1` (only itself in window) ✓
- `rolling_log_return_past_window_*` is `null` for all four windows (no prior reference price) ✓

**Last row (`row_index = 1,681,097`):**

- `agg_trade_id` matches source row 1,681,097 ✓
- `source_transact_time_ms` matches source row 1,681,097 `transact_time_ms` ✓
- `row_index = 1,681,097` ✓

## Independent causal spot-checks

For each of 9 sample rows (`R ∈ {0, 5, 100, 1000, 50000, 100000, 500000, 1000000, 1681097}`) and each of 2 windows (`1s = 1000 ms`, `60s = 60000 ms`) — **18 spot-checks total** — the orchestrator independently:

1. computed `lo = bisect_right(T, T[R] - window_ms)` from the source;
2. counted source rows `j ∈ [lo, R]` to obtain expected `rolling_aggtrade_count`;
3. summed source `quantity` (Decimal-exact) over the buy / sell partition (per `is_buyer_maker = false → buy`) to obtain expected `rolling_aggressive_buy_quantity` and `rolling_aggressive_sell_quantity`;
4. computed expected `rolling_aggressive_flow_ratio = buy / (buy + sell)` (or `null` if denominator is zero);
5. computed expected `rolling_log_return_past_window = ln(price[R] / price[lo - 1])` (or `null` if `lo == 0`).

Every spot-check passed bit-for-bit (Decimal equality for quantities; `|Δ| < 1e-12` for floats). 18 / 18 PASS.

## Same-timestamp tie-break inspection

The orchestrator scanned the first 100,000 source rows for any pair `(i-1, i)` with `T[i] == T[i-1]`. The first such pair occurred at rows `(14, 15)`. Verification:

- `rolling_aggtrade_count_1s[14] = 15`
- `rolling_aggtrade_count_1s[15] = 16`
- Difference is exactly `+1` ✓

This confirms the same-timestamp tie-break rule is structurally respected: when row `15` has the same `T` as row `14`, the trailing `(T - 1000, T]` window for row `15` includes everything row `14`'s window included plus row `15` itself, because of the `row_index <= R` tie-break.

## Upstream immutability evidence

Pre-run vs post-run SHA256 for every upstream artefact (recomputed inside the orchestrator):

| Artefact | SHA256 (pre/post) | Status |
| --- | --- | --- |
| original derived manifest | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` | UNCHANGED |
| normalized parquet | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` | UNCHANGED |
| raw manifest | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` | UNCHANGED |
| raw zip | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | UNCHANGED |
| Phase 4bb-D gate report | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` | UNCHANGED |
| Phase 4bf gate report | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` | UNCHANGED |
| Phase 4bg-B successor-state JSON | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` | UNCHANGED |

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant was preserved end-to-end (never invoked).

The actual on-disk raw manifest still carries `research_eligible = false` and `eligibility_gate_status = "pending"`. The actual on-disk derived manifest still carries `research_eligible = false` and `eligibility_gate_status = "pending"`.

## Gitignore / tracked-file boundary

- `git check-ignore -v data/microstructure/` returns `.gitignore:85:data/microstructure/	data/microstructure/` ✓
- `git check-ignore -v data/microstructure/features/` returns `.gitignore:85:data/microstructure/	data/microstructure/features/` ✓
- `git check-ignore -v data/microstructure/manifests/` returns `.gitignore:85:data/microstructure/	data/microstructure/manifests/` ✓
- No `data/microstructure/` file is tracked or staged in git ✓
- No labels / targets / signals / ML / strategy / backtest artefacts exist as a result of Phase 4bi-A ✓
- No endpoint / network / credential / MCP / Graphify activity occurred ✓

## QA result

**Aggregate: 67 / 67 explicit structural checks PASS; 18 / 18 independent causal spot-checks PASS; same-timestamp tie-break PASS; `validate_feature_dataset` reproduces 135 / 135 PASS (overall_status = pass).**

The on-disk Phase 4bh feature parquet and feature manifest pair is structurally consistent with the Phase 4bh-B locked schema, the Phase 4bh implementation result, and the Phase 4bh merge-closeout's recorded evidence.

## Feature-stage interpretation

Per Phase 4bh-A's feature-stage model:

- **Feature Stage-1 implementation merged** — REACHED by Phase 4bh.
- **Feature Stage-2 local feature artefacts exist with manifest** — REACHED by Phase 4bh.
- **Feature Stage-3 structural QA-passed (memo level)** — REACHED by Phase 4bi-A on the local one-day artefact only.
- **Feature Stage-4 feature-family eligibility-gate-passed** — NOT REACHED. Requires a separately authorized future Phase 4bi-B that designs, implements, and runs a feature-family eligibility gate analogous to Phase 4bb-C / 4bf for the raw and derived families.
- **Feature Stage-5 research-use / ML-use decision** — NOT REACHED.

Phase 4bi-A's "Stage-3 reached at memo level" is a structural QA finding only. It is not a feature-family eligibility-gate verdict, not a research-use approval, and not an ML-use approval. The feature manifest's `research_eligible` field remains `false` and its `eligibility_gate_status` remains `pending`.

## What this phase proves

- The on-disk feature parquet exactly conforms to the Phase 4bh-B 61-column schema (column count, order, types, nullability) ✓
- Feature parquet row count exactly matches the source normalized parquet (1,681,098) ✓
- Per-row identity (`agg_trade_id`, `row_index`, timestamps) matches the source bit-for-bit ✓
- All lineage SHAs match the Phase 4bh merge-closeout's recorded values ✓
- Causal trailing-window semantics hold: independent spot-checks at 9 sampled rows × 2 windows reproduce the kernel's outputs bit-for-bit ✓
- Same-timestamp tie-break (`row_index <= R`) is structurally respected ✓
- Decimal-as-string columns parse via `decimal.Decimal(...)` ✓
- Float columns contain no NaN / inf ✓
- Quality flags are uniformly `false`, consistent with `invalid_windows = []` ✓
- All 7 upstream artefacts are byte-for-byte unchanged ✓
- Feature manifest preserves `research_eligible = false / eligibility_gate_status = pending` ✓
- All 11 boundary confirmations remain true ✓
- The Phase 4bh `validate_feature_dataset` 135 / 135 PASS result is independently reproducible ✓

## What this phase does not prove

- Feature artefacts are NOT feature-family eligibility-gate-passed (Stage-4); a future Phase 4bi-B is required.
- Feature family is NOT research-use approved or ML-use approved.
- No edge claim is made.
- No baseline-superiority claim is made.
- No predictive validity is established.
- No labels, targets, signals, ML, strategy, or backtest exist.
- The Phase 4bh-B contract is exercised only on the single BTCUSDT 2025-01-15 day; multi-day / multi-symbol parity is not verified.
- The kernel's correctness on edge cases beyond the 18 sampled rows is not exhaustively proven; the spot-checks are sampled, not exhaustive.
- No paper / shadow / live-readiness / exchange-write / production keys / authenticated APIs / private endpoints / user stream / live WebSocket / MCP / Graphify / `.mcp.json` / credentials are implied.
- Stage-4, Stage-5, paper / shadow, live, exchange-write, production keys, and any successor phase remain unauthorised.

## Preserved boundaries

- Original raw manifest remains `research_eligible = false / eligibility_gate_status = pending`.
- Original derived manifest remains `research_eligible = false / eligibility_gate_status = pending`.
- Feature manifest remains `research_eligible = false / eligibility_gate_status = pending`.
- Phase 4bg-B successor-state JSON is unchanged.
- Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved.
- M0 (Phase 4ak) twelve-clause gate, post-null cooldown, cooled-down families list, and memo template preserved.
- Phase 4al refined no-rescue rule, §13 boundary, §14 hierarchy preserved.
- §11.6 = 8 bps per side, round-trip = 16 bps preserved.
- §1.7.3 0.25% / 2× / one-position / mark-price stops preserved.
- Phase 3p §4.7 / Phase 3r §8 / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 4j §11 / Phase 4k / Phase 4p / Phase 4q / Phase 4v / Phase 4w preserved.
- All retained verdicts (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread / V2 / G1 / C1) preserved verbatim.

## Recommended future options

- **Primary (NOT authorized by Phase 4bi-A):** remain paused.
- **Conditional next (NOT authorized by Phase 4bi-A):** Phase 4bi-B — Feature-Family Eligibility-Gate Design + Implementation + Execution (analogous to Phase 4bb-C / 4bf for the feature family; designs and runs an offline eligibility gate that checks artefact integrity, schema compliance, governance labels, and lineage; produces a gate report; does not flip `research_eligible`).
- **Conditional cleanup / red-team (NOT authorized by Phase 4bi-A):** Phase 4bh-C — Feature Schema Finalization Review / Red-Team Memo (only if structural QA finds ambiguity worth red-teaming; this Phase 4bi-A QA found no such ambiguity).
- **Conditional cleanup (NOT authorized by Phase 4bi-A):** Phase 4bb-F — Gate Report Output Path Hygiene (cleanup of the doubled `gate-reports/gate-reports/` segment).
- **Conditional raw policy marker (NOT authorized by Phase 4bi-A):** Phase 4bb-G — Raw Manifest Successor-State Recording (sibling successor-state manifest only).

Phase 4bi-A does NOT authorize any successor.

## Closeout / lock preservation

All retained verdicts preserved verbatim:

- H0 FRAMEWORK ANCHOR
- R3 BASELINE-OF-RECORD
- R1a / R1b-narrow RETAINED — NON-LEADING
- R2 FAILED — §11.6
- F1 HARD REJECT
- D1-A MECHANISM PASS / FRAMEWORK FAIL
- 5m thread OPERATIONALLY CLOSED per Phase 3t
- V2 HARD REJECT — terminal for V2 first-spec
- G1 HARD REJECT — terminal for G1 first-spec
- C1 HARD REJECT — terminal for C1 first-spec

All Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak M0 + post-null cooldown + cooled-down families list + memo template, Phase 4al refined no-rescue + §13 + §14, Phase 4am, 4an, 4ao, 4ap, 4aq, 4ar, 4as, 4at, 4au, 4av, 4aw, 4ax, 4ay, 4az, 4ba, 4bb-A, 4bb-B, 4bb-C, 4bb-D, 4bb-E, 4bc, 4bd-A, 4bd, 4be, 4bf-A, 4bf, 4bg-A, 4bg-B, 4bh-A, 4bh-B, 4bh governance preserved verbatim.

**No project lock changed by Phase 4bi-A.** **No retained verdict revised by Phase 4bi-A.** **No successor authorized by Phase 4bi-A.** **Recommended state: remain paused.**
