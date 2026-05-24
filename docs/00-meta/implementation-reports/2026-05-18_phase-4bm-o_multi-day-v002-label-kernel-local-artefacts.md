# Phase 4bm-O — Multi-Day V002 Label Kernel Implementation + Local Label Artefact Generation

**Phase identity:** Phase 4bm-O — Multi-Day V002 Label Kernel Implementation + Local Label Artefact Generation (code + tests + docs + local gitignored data outputs; multi-day v002 analogue of Phase 4bj-C).
**Date:** 2026-05-24.
**Branch:** `phase-4bm-o/multi-day-v002-label-kernel-local-artefacts`.
**Base:** `main` at `e2574c4ad6497686b974c39bfb351880e38fb0dd` (Phase 4bm-N merge-closeout SHA-finalization commit; pre-branch `main == origin/main` verified in sync).
**Tier:** **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 escalation rules ("any phase that creates features / labels / diagnostics" → Tier 1, period). Phase 4bm-O creates the first multi-day v002 label artefacts (code + tests + local gitignored data) and therefore receives the full Tier 1 ceremony: authorization prompt, dedicated branch, full implementation report, dedicated closeout, narrow `current-project-state.md` update, and (separately, in a future phase) a Tier 1 merge-closeout.
**Phase type:** code + tests + docs + local gitignored label artefacts.
**Status:** branch-complete by this work; not merged into `main`; not project-complete.

---

## 1. Phase header

Phase 4bm-O is the project's first code phase to materialise the finalised Phase 4bm-N v002 label schema as actual local label artefacts. It produces:

- four new v002 source modules at `src/prometheus/research/microstructure/` plus a narrow `__init__.py` re-export update;
- six new test files at `tests/research/microstructure/`;
- one new orchestrator script at `scripts/phase4bm_o_compute_multiday_labels.py`;
- 90 local gitignored per-day label Parquets + 90 paired canonical Phase 4bb-F sidecars;
- 1 local gitignored v002 label manifest + 1 paired canonical Phase 4bb-F sidecar;
- this main memo + a closeout memo + a narrow `current-project-state.md` paragraph + "Current phase:" block update.

Phase 4bm-O does not authorise any successor phase, does not flip `research_eligible` on any actual manifest, does not transition any manifest's `eligibility_gate_status`, and does not produce a label gate report or a label successor-state artefact.

## 2. Scope and boundary

Phase 4bm-O is authorised to:

- add source modules `labels_schema_v002.py`, `labels_io_v002.py`, `labels_compute_v002.py`, `labels_manifest_v002.py` under `src/prometheus/research/microstructure/`;
- narrowly update the package `__init__.py` to re-export the new Phase 4bm-O public API symbols;
- add fixture + test files `_labels_fixtures_v002.py`, `test_labels_schema_v002.py`, `test_labels_io_v002.py`, `test_labels_compute_v002.py`, `test_labels_manifest_v002.py`, `test_labels_no_network_v002.py` under `tests/research/microstructure/`;
- add an offline label-generation orchestrator script at `scripts/phase4bm_o_compute_multiday_labels.py`;
- generate exactly:
  - 90 local gitignored per-day v002 label Parquets under `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/`;
  - 90 paired canonical Phase 4bb-F sidecars;
  - 1 local gitignored v002 label manifest at `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json`;
  - 1 paired canonical Phase 4bb-F sidecar at the same path with `.sha256` suffix;
- add this implementation report + a closeout memo + a narrow `current-project-state.md` paragraph + "Current phase:" block update.

Phase 4bm-O does **NOT**:

- run ML, build models, train classifiers, compute model scores, predictions, embeddings, or learned representations;
- create strategy logic, strategy signals, strategy actions, or position-state outputs;
- run backtests, compute PnL, MFE, MAE, R-multiple, equity curves, alpha, edge, or decision scores;
- create barrier labels, target-before-stop labels, execution-quality labels, or cross-symbol / cross-sectional labels;
- create 30s, 5m, or other horizons beyond `{1s, 5s, 15s, 60s}`;
- acquire data, call any Binance endpoint, open any WebSocket, use any credential, read or create `.env`, create `.mcp.json`, or enable MCP / Graphify;
- modify any source artefact (v002 feature manifest + sidecar, 90 v002 per-day feature parquets + sidecars, Phase 4bm-L successor-state JSON + sidecar, Phase 4bm-J gate report + sidecar, v002 derived multi-day index manifest + sidecar, 90 v002 normalized parquets, Phase 4bm-F successor-state, Phase 4bm-D gate report, v002 raw manifest, v002 acquisition log, Phase 4bl-E raw successor-state, Phase 4bl-D-R raw gate report, prior v001 label artefacts, or any other on-disk governance artefact);
- rerun any prior gate, normalizer, feature kernel, or feature-family eligibility gate;
- create a label-family eligibility gate report or label successor-state artefact;
- flip `research_eligible` on any manifest;
- transition `eligibility_gate_status` on any manifest;
- mark `stage_4_feature_cleared = true` on the v002 feature manifest;
- mark `stage_5_label_cleared = true` on the new v002 label manifest;
- change `chronological_split_policy` on any manifest;
- authorise Phase 4bm-P, multi-day v002 label structural QA, multi-day v002 label-family eligibility gate, multi-day v002 label-family research-use decision, multi-day v002 label-family successor-state recording, multi-day v002 chronological-split-policy memo, multi-day v002 diagnostics, multi-day v002 ML / strategy / backtest, Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-*, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation;
- revise retained verdicts;
- change any project lock;
- amend M0;
- commit anything under `data/microstructure/`.

## 3. Linkage to Phase 4bm-N schema finalization

Phase 4bm-O implements the Phase 4bm-N-locked 40-column v002 label schema verbatim:

- `dataset_family = "microstructure_labels_aggtrades_v001"`;
- `dataset_version = "v002"`;
- `label_schema_version = "v001"`;
- 40 canonical columns in Phase 4bm-N §14 order: 17 lineage / identity / metadata + 1 `label_config_hash` + 4 regression `forward_log_return_<horizon>` + 4 classification `forward_direction_<horizon>` + 12 per-horizon support + 2 global support;
- 4 horizons `("1s", "5s", "15s", "60s")` paired with `(1000, 5000, 15000, 60000)` ms;
- envelope-terminal censoring at `target_timestamp_ms > envelope_terminal_unix_ms` (no per-day censoring); cross-day reference resolution allowed inside the label kernel only, within the 90-day v002 envelope;
- same-timestamp tie-break: largest `row_index` at that timestamp inside its per-day source parquet;
- `forward_log_return_H = ln(reference_trade_price_H / anchor_trade_price)` with Decimal parsing, Decimal ratio, and `float64` cast at the log step only;
- `forward_direction_H` strict sign from `forward_log_return_H` only: `+1` / `0` / `-1` / `null`;
- `label_invalid_price_flag = true` when anchor or any reference price is `<= 0`;
- `label_any_censored_flag = OR(horizon_censored_flag_*)`;
- no NaN / inf in any output column;
- `chronological_split_policy` default `not_yet_defined`;
- `label_config_hash` is SHA256 over canonical JSON of the schema-locking fields plus the six v002 upstream lineage SHAs and `feature_config_hash` (Phase 4bm-N §25).

## 4. Linkage to Phase 4bm-M Label Stage-0 boundary / design

Phase 4bm-O honours the Phase 4bm-M Label Stage-0 boundary verbatim:

- labels are a sibling artefact family of the v002 feature family; never written into v002 features;
- v002 feature artefacts remain causal and byte-identical;
- labels may use future information only inside the label kernel routine;
- labels preserve lineage to the v002 feature manifest, Phase 4bm-L successor-state, Phase 4bm-J gate report, v002 derived multi-day index manifest, v002 raw manifest, Phase 4bl-E raw successor-state, and Phase 4bl-D-R raw gate report;
- label manifest defaults to `research_eligible: false` / `eligibility_gate_status: "pending"` / `label_family_research_use_authorized: false` / `chronological_split_policy: "not_yet_defined"` / `stage_5_label_cleared: false`.

## 5. Linkage to Phase 4bm-L Feature Stage-5 marker

Phase 4bm-O reads the Phase 4bm-L machine-readable v002 Feature Stage-5 admissibility marker as the sibling-artefact evidence that v002 feature-family research-use is policy-level admissible; the Phase 4bm-L successor-state JSON SHA `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` (sidecar `c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98`) is pinned in every v002 label parquet row and in the v002 label manifest.

## 6. Linkage to Phase 4bm-J `FEATURE_GATE_PASS`

The Phase 4bm-J FEATURE_GATE_PASS evidence (50 / 50 PASS; 0 FAIL; 0 ERROR; 0 NOT_APPLICABLE; gate report SHA `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242`; sidecar `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125`) is pinned in every v002 label parquet row and in the v002 label manifest as `source_phase_4bm_j_gate_report_sha256`.

## 7. Linkage to Phase 4bm-I `FEATURE_STRUCTURAL_QA_PASS`

The Phase 4bm-I structural QA PASS verdict over the Phase 4bm-H feature artefacts is the read-only structural QA layer that precedes the Phase 4bm-J gate; Phase 4bm-J check A12 PASS machine-verifies it. Phase 4bm-O depends on the Phase 4bm-I verdict transitively through the Phase 4bm-J gate report.

## 8. Linkage to Phase 4bj-C v001 label implementation precedent

Phase 4bj-C (v001 label kernel implementation + local gitignored label artefact generation; merged on `main`) is the primary structural precedent for Phase 4bm-O. Phase 4bm-O reuses the v001 `labels_io` atomic writers + canonical Phase 4bb-F sidecar writer verbatim and adopts the same module decomposition (`_schema`, `_io`, `_compute`, `_manifest`) for the v002 family, transposed to the multi-day envelope and the 40-column v002 schema. Phase 4bm-O reuses the v001 Phase 4bj-C `labels_io.atomic_write_label_parquet` / `atomic_write_label_manifest` / `write_label_sha256_sidecar` helpers, the v001 `labels_io.LabelIOError`, and the v001 path-discipline asserts (`assert_label_path_under_data_microstructure`, `assert_output_path_under_labels`, `assert_label_manifest_path_under_manifests`).

Phase 4bj-C verdicts do **not** transitively authorise any v002 label computation: this phase is separately authorised by an explicit operator prompt.

## 9. Implementation files added / modified

Source modules added (4):

| File | Description |
|---|---|
| `src/prometheus/research/microstructure/labels_schema_v002.py` | 40-column v002 schema constants + horizons + forbidden-substring detector + 5 policy descriptors + `build_label_config_hash_v002` |
| `src/prometheus/research/microstructure/labels_io_v002.py` | v002 path helpers (`derive_v002_label_parquet_path`, `derive_v002_label_manifest_path`) + canonical Phase 4bb-F sidecar composer |
| `src/prometheus/research/microstructure/labels_compute_v002.py` | `compute_aggtrade_labels_v002_for_day` (per-day multi-day kernel with cross-day reference resolution bounded by `envelope_terminal_unix_ms`) + `load_normalized_day_ref` + `write_label_dataset_v002` + `LabelLineageV002` / `LabelComputationSummaryV002` / `LabelMultiDaySummaryV002` / `NormalizedDayRef` dataclasses + `LabelComputationErrorV002` |
| `src/prometheus/research/microstructure/labels_manifest_v002.py` | `build_label_manifest_v002` (locked governance defaults; 17 boundary confirmations all true; 90-entry `per_day_outputs` schema; aggregate row count, column count, censored counts, invalid-price counts, envelope-terminal timestamp) |

Source narrowly updated (1):

- `src/prometheus/research/microstructure/__init__.py` — adds the Phase 4bm-O public API re-exports (sorted into the existing alphabetical-by-section convention).

Test files added (6):

| File | Tests | Notes |
|---|---|---|
| `tests/research/microstructure/_labels_fixtures_v002.py` | helpers | `build_normalized_table_v002`, `build_feature_table_v002`, `write_temp_parquet` |
| `tests/research/microstructure/test_labels_schema_v002.py` | 17 | identity / horizon / column constants; canonical 40-column order; forbidden-substring detector; `label_config_hash` determinism + payload composition + v001 ≠ v002 |
| `tests/research/microstructure/test_labels_io_v002.py` | 12 | path discipline; derived paths; canonical Phase 4bb-F sidecar two-space format; rejects bad symbol / bad date / wrong root / short SHA / uppercase SHA / basename newline; LF-only |
| `tests/research/microstructure/test_labels_compute_v002.py` | 18 | smoke test; anchor alignment; lineage propagation; envelope-terminal censoring; tie-break (same-timestamp largest row_index); cross-day reference resolution; cross-day largest row in next day; cross-day target-beyond-envelope censoring; strict-sign direction; Decimal-into-float64 formula; invalid anchor / reference price; no NaN / inf; row-alignment mismatch fails; atomic write + refuse-overwrite; `load_normalized_day_ref` round-trip + rejects missing file |
| `tests/research/microstructure/test_labels_manifest_v002.py` | 18 | required field presence; governance defaults locked; boundary confirmations all true; schema introspection; per-day outputs validation; rejections (lower-case symbol, non-BTCUSDT, bad date, negative counts, length mismatch, bad horizon keys, short SHA, overriding locked governance key); extras allowed when unique; censored / invalid-price round-trip |
| `tests/research/microstructure/test_labels_no_network_v002.py` | 21 | static no-network / no-credential scan over the 4 v002 modules + the orchestrator script; case-sensitive token scan after stripping docstrings / comments; whitelist-aware (no false positives on `no_mcp_or_graphify`) |

Total new tests: **91** (all passing).

Script added (1):

- `scripts/phase4bm_o_compute_multiday_labels.py` — Phase 4bm-O orchestrator. Locks 14 precondition SHAs (v002 feature manifest + sidecar, Phase 4bm-L successor-state + sidecar, Phase 4bm-J gate report + sidecar, v002 derived multi-day index manifest + sidecar, Phase 4bm-F successor-state, Phase 4bm-D gate report, v002 raw manifest, v002 acquisition log, Phase 4bl-E successor-state, Phase 4bl-D-R gate report); resolves 90-day inventories from the v002 feature manifest's `per_day_outputs` and v002 derived manifest's `per_file_inventory`; computes `envelope_terminal_unix_ms` as `max(last_transact_time_ms)` across the envelope; refuses to overwrite any existing label parquet, sidecar, manifest, or manifest sidecar; processes 90 days with a rolling current-day / next-day normalized reference (cross-day lookup is bounded by 60s and naturally lands in the immediately following day or stays within the current day); writes per-day Parquet + sidecar atomically; builds and writes the v002 label manifest + sidecar atomically; performs post-write SHA verification of all 14 governance preconditions + 90 feature parquets + 90 normalized parquets (= 194 total immutability witnesses).

Docs added (2):

- `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-o_multi-day-v002-label-kernel-local-artefacts.md` (this file)
- `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-o_closeout.md`

Docs narrowly updated (1):

- `docs/00-meta/current-project-state.md` — narrow update to record Phase 4bm-O branch-complete status (new paragraph + new "Current phase:" block; prior Phase 4bm-N "Current phase:" block preserved as labelled historical context).

No `.gitignore` change. No `pyproject.toml` change. No `README.md` change. No existing source / test / script outside the new modules / fixtures / tests is modified. No prior implementation report, closeout, or merge-closeout is modified. No prior governance memo is modified. No prior gate report, successor-state JSON, manifest, sidecar, or parquet is modified.

## 10. Tests added / modified

See §9. All 91 new tests are in `tests/research/microstructure/test_labels_*_v002.py` plus the fixture helper `_labels_fixtures_v002.py`. No existing test file was modified. Existing v001 label tests (`test_labels_*.py`), v002 feature tests (`test_features_*_v002.py`), and all other microstructure tests remain unchanged and continue to pass.

## 11. Label kernel design

The v002 kernel `compute_aggtrade_labels_v002_for_day` is invoked per UTC day. For each day:

1. validates feature table (`row_index == np.arange(n_feat)`, `feature_timestamp_ms == source_transact_time_ms`, identity columns present);
2. validates current-day normalized reference (row count parity with feature table, `agg_trade_id` parity, `transact_time_ms` parity);
3. parses every current-day price into `Decimal` via `getcontext().prec = 50` (deferred to `load_normalized_day_ref`, executed once per day);
4. for each horizon `H ∈ {1s, 5s, 15s, 60s}`:
   - computes `target_ts = feat_ts_ms + H_ms` vectorised over the day;
   - sets `horizon_censored_flag_H = true` where `target_ts > envelope_terminal_unix_ms`;
   - vectorised `searchsorted` on the current day's `transact_time_ms` and the next day's `transact_time_ms` to compute the per-row reference index;
5. for each anchor row, picks the **next day's** reference if non-empty (it is globally later than every current-day row); otherwise picks the **current day's** reference (always non-negative for non-censored anchors); records `reference_row_index_H` (local per-day), `reference_timestamp_ms_H`, and computes `forward_log_return_H = math.log(float(Decimal(ref) / Decimal(anchor)))`;
6. derives `forward_direction_H` from the strict sign of the log return (+1 / 0 / -1 / null);
7. flags `label_invalid_price_flag = true` if anchor ≤ 0 or any reference ≤ 0 (defensive; counts the row at most once);
8. flags `label_any_censored_flag = OR(horizon_censored_flag_*)`;
9. assembles the 40-column canonical schema (string / int64 / nullable int64 / nullable float64 / nullable int8 / bool) in Phase 4bm-N §14 column order;
10. returns `(table, LabelComputationSummaryV002)`.

The 40-column schema is materialised in canonical order and the kernel asserts the column order matches `LABEL_SCHEMA_V002` byte-for-byte before returning.

## 12. Reference-row lookup policy

For each (anchor row `R`, horizon `H`):

- `target_timestamp_ms = feature_timestamp_ms[R] + horizon_ms[H]`;
- if `target > envelope_terminal_unix_ms`: censored — all five per-horizon columns null; `horizon_censored_flag_H = true`;
- else: compute the candidate in the current day via `searchsorted(cur_ts, target, side='right') - 1` (always non-negative since `target >= anchor_ts >= cur_ts[0]`) and the candidate in the next day via `searchsorted(next_ts, target, side='right') - 1` (may be `-1` if next-day's first row is later than target);
- if next-day candidate `>= 0`, choose it (the next day is globally later than every current-day row because daily parquets do not overlap in `agg_trade_id` and Phase 4bm-D verified strict cross-day monotonicity);
- otherwise choose the current-day candidate;
- `reference_row_index_H` = chosen local row_index (per-day);
- `reference_timestamp_ms_H` = chosen row's `transact_time_ms`;
- `reference_trade_price_H` = chosen row's price (`Decimal`).

The choice rule "prefer next-day if non-empty" is correct because: anchor is in day `D`, so `target` is at least `cur_ts[0]` (where the current-day candidate is non-negative); horizons are bounded by 60 000 ms (60 s), so a target that lands past `last_ts(D)` lands in the first 60 s of day `D+1`. Any row in day `D+1` with `ts <= target` is globally later than every row in day `D`; conversely if day `D+1` has no row with `ts <= target` then the reference must be the last current-day row.

The same-timestamp tie-break (largest `row_index` at the same timestamp inside the per-day source parquet) is automatically handled by `searchsorted(side='right') - 1`, because each per-day normalized parquet has `row_index == np.arange(n)` and is sorted by `(transact_time_ms ASC, row_index ASC)` per the Phase 4bm-B normalisation contract.

## 13. Cross-day horizon handling

The implementation rolls one normalized day forward per iteration: at iteration `i`, the previously-loaded "next day" becomes the new "current day"; if `i + 1 < 90`, a new "next day" is loaded. Day 90's `next_day` is `None`. Each per-day load reads only the columns required by the label kernel (`transact_time_ms`, `price`, `agg_trade_id`, `utc_date`, `row_index`) — never the full normalized schema — and parses prices to `Decimal` once per row. Memory footprint stays bounded at one day's transact_time_ms array + one day's `Decimal` price list (~60 MB peak per day at v002 row densities).

## 14. Censoring policy

Per Phase 4bm-N §20 verbatim, censoring is **envelope-terminal only**. The kernel computes `envelope_terminal_unix_ms` exactly once per run as the maximum `last_transact_time_ms` across the 90 entries of the v002 derived multi-day index manifest's `per_file_inventory`. Censoring is per-horizon independent; censored rows preserve `null` for `forward_log_return_H`, `forward_direction_H`, `reference_row_index_H`, `reference_timestamp_ms_H`, and set `horizon_censored_flag_H = true`. `label_any_censored_flag = OR(horizon_censored_flag_*)`. No per-day censoring is performed; horizons may cross UTC day boundaries inside the v002 90-day envelope.

## 15. Invalid-price policy

If anchor or any reference price is `<= 0`, the kernel sets `label_invalid_price_flag = true` (counted once per row) and nulls the affected horizon's label and direction columns. The reference row's `reference_row_index_H` and `reference_timestamp_ms_H` are still populated because the row identity is valid; only the price-derived values null out. This mirrors Phase 4bj-B §14 verbatim with no v002 deviation. Defensively, any case that would produce `NaN` or `inf` (e.g. degenerate `Decimal` ratio rounding) is treated as invalid price and null-flagged.

## 16. `label_config_hash` value and construction

`build_label_config_hash_v002` builds canonical JSON (sorted keys, ASCII, no whitespace) over exactly:

- `dataset_family`, `dataset_version`, `label_schema_version`
- `label_list`, `support_column_list`, `lineage_column_list`
- `horizon_list`, `horizon_ms_list`
- `anchor_policy`, `future_reference_policy`, `direction_threshold_policy`, `null_censoring_policy`, `dtype_policy`
- `source_feature_manifest_sha256`, `source_feature_successor_state_sha256`, `source_phase_4bm_j_gate_report_sha256`, `source_normalized_manifest_sha256`, `source_raw_manifest_sha256`, `feature_config_hash`

and SHA256s the UTF-8 encoding. The resulting hex is recorded as the `label_config_hash` field on every label parquet row (constant across all 90 per-day parquets) and in the label manifest's `label_config_hash` field.

Real-run value computed by `scripts/phase4bm_o_compute_multiday_labels.py` over the v002 envelope:

```
label_config_hash = 352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560
```

## 17. Execution command

```
python scripts/phase4bm_o_compute_multiday_labels.py \
    --code-commit-sha 252f7ce5dd494097c0ee42c7213579ba5823e30e
```

Pre-run preconditions verified for 14 governance artefacts (all MATCH); 90 per-day feature + 90 per-day normalized parquet SHAs verified pre-run (all MATCH); refuse-to-overwrite pre-write check for 92 outputs (90 parquets + 1 manifest + 1 manifest sidecar) all PASS. Post-run upstream immutability re-hashed: 14 + 90 + 90 = 194 artefacts, all byte-identical pre/post.

## 18. Local gitignored outputs

All outputs are gitignored under `.gitignore:85` (`data/microstructure/`) and are NOT committed.

| Output | Path |
|---|---|
| Label parquet root | `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/BTCUSDT-labels-aggtrades-<YYYY>-<MM>-<DD>.parquet` |
| Label parquet count | **90** (one per UTC date 2024-12-01 .. 2025-02-28 inclusive) |
| Label parquet aggregate byte size | **6,145,349,264** bytes (≈ 5.72 GiB across 90 per-day Parquets) |
| Label sidecar count | **90** (canonical Phase 4bb-F format `<sha256_lowercase_hex><two ASCII spaces><basename><LF>`) |
| Label manifest path | `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json` |
| Label manifest SHA256 | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` |
| Label manifest byte size | 84,732 bytes |
| Label manifest sidecar path | `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json.sha256` |
| Label manifest sidecar SHA256 | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` |
| Label manifest sidecar byte size | 114 bytes |
| Label manifest sidecar content | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed  microstructure_labels_aggtrades_v001__v002.json\n` (canonical Phase 4bb-F two-space format; ASCII / UTF-8 no BOM; LF only; no CRLF) |

Total local gitignored artefacts created: **182** (90 + 90 + 1 + 1).

## 19. Aggregate output summary

| Field | Value |
|---|---|
| `row_count` (aggregate across 90 per-day label parquets) | **155,153,449** (equals the v002 feature row count exactly) |
| `column_count` | **40** |
| `date_count` | **90** |
| `horizons` | `["1s", "5s", "15s", "60s"]` |
| `horizon_ms_list` | `[1000, 5000, 15000, 60000]` |
| `envelope_terminal_unix_ms` | `1740787199996` (= 2025-02-28T23:59:59.996Z) |
| `censored_per_horizon` | `{"1s": 14, "5s": 39, "15s": 170, "60s": 634}` |
| `invalid_price_row_count` | `0` (matches the Phase 4bl-D-R + Phase 4bm-D upstream PASS evidence — no invalid prices across the 90-day envelope) |

## 20. Per-day output summary

The 90 per-day label parquet inventory (utc_date, byte size, row count, per-horizon censored counts, invalid-price row count, label parquet SHA, label sidecar SHA, source feature parquet SHA) is recorded in the v002 label manifest's `per_day_outputs` list. Spot facts:

- first day: `2024-12-01` (row_count = 731,065)
- last day: `2025-02-28` (row_count = 4,526,219; this is also the envelope-terminal day and contributes the 634 `horizon_censored_flag_60s = true` rows, the 170 `horizon_censored_flag_15s = true` rows, the 39 `horizon_censored_flag_5s = true` rows, and the 14 `horizon_censored_flag_1s = true` rows)
- min row count day: `2025-02-15` (row_count = 451,314)
- max row count day: `2025-01-20` (row_count = 5,435,481)
- total label row count across all 90 days: **155,153,449**
- per-day row count parity with v002 feature parquets: verified 90 / 90 by the orchestrator.

## 21. Pre/post SHA immutability table

| Upstream artefact | SHA256 (expected) | Status |
|---|---|---|
| v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | MATCH pre + MATCH post |
| v002 feature manifest sidecar | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` | MATCH pre + MATCH post |
| Phase 4bm-L successor-state JSON | `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` | MATCH pre + MATCH post |
| Phase 4bm-L successor-state sidecar | `c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98` | MATCH pre + MATCH post |
| Phase 4bm-J gate report | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` | MATCH pre + MATCH post |
| Phase 4bm-J gate report sidecar | `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125` | MATCH pre + MATCH post |
| v002 derived multi-day index manifest | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` | MATCH pre + MATCH post |
| v002 derived multi-day index manifest sidecar | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` | MATCH pre + MATCH post |
| Phase 4bm-F derived successor-state JSON | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` | MATCH pre + MATCH post |
| Phase 4bm-D derived gate report | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` | MATCH pre + MATCH post |
| v002 raw manifest | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | MATCH pre + MATCH post |
| v002 acquisition log | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | MATCH pre + MATCH post |
| Phase 4bl-E raw successor-state JSON | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` | MATCH pre + MATCH post |
| Phase 4bl-D-R raw gate report | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` | MATCH pre + MATCH post |
| 90 per-day v002 feature parquets | per-day SHAs from `microstructure_features_aggtrades_v001__v002.json::per_day_outputs[].feature_parquet_sha256` | 90 / 90 MATCH pre + 90 / 90 MATCH post |
| 90 per-day v002 normalized parquets | per-day SHAs from `microstructure_normalized_aggtrades_v001__v002.json::per_file_inventory[].parquet_sha256` | 90 / 90 MATCH pre + 90 / 90 MATCH post |

Total immutability witnesses: **194** (14 governance + 90 feature parquets + 90 normalized parquets), all byte-identical pre/post the Phase 4bm-O run.

## 22. Quality gate results

- `ruff check` — Phase 4bm-O surface: **PASS** (12 files: 4 source modules + 1 `__init__.py` update + 1 script + 6 test files; after one auto-fixable round of import-sort + Yoda-condition fixes, the second invocation reports "All checks passed!").
- `pytest tests/research/microstructure/test_labels_*_v002.py` — **91 / 91 passed**.
- `pytest tests/research/microstructure/` — **1623 passed, 1 skipped** (the skipped test is pre-existing baseline; no new regression).
- `git diff --check` — clean (exit 0).
- Static no-network / no-credential scan over 4 source modules + the orchestrator script — PASS.

`mypy src/prometheus` and whole-repo `pytest` were not invoked at Phase 4bm-O level. Per the Phase 4bm-H precedent (and the documented project baseline of 29 mypy errors in 5 files plus 15 pytest collection errors from missing `httpx` / `duckdb` and 2 `test_engine_d1a_dispatch.py` subprocess failures), no new mypy category or pytest failure is expected to be introduced by Phase 4bm-O: the new modules avoid third-party deps beyond the existing pyarrow/numpy/Decimal idioms used by v001 labels + v002 features, and the new tests target the new modules only. Any future Phase 4bm-O merge phase may rerun these checks.

## 23. Validation commands and results

| Command | Result |
|---|---|
| `git status --short` (pre-execution) | only `.claude/scheduled_tasks.lock` and `data/research/` untracked (expected) |
| `git branch --show-current` | `phase-4bm-o/multi-day-v002-label-kernel-local-artefacts` |
| `git rev-parse main` | `e2574c4ad6497686b974c39bfb351880e38fb0dd` |
| `git rev-parse origin/main` | `e2574c4ad6497686b974c39bfb351880e38fb0dd` (in sync) |
| `git log --oneline -12 --decorate` | latest main commit is `e2574c4 docs(phase-4bm-n): finalize merge closeout shas` (matches expectation) |
| `python scripts/phase4bm_o_compute_multiday_labels.py --dry-run` | preconditions OK (14 / 14); resolved 90 / 90 per-day inventories; `envelope_terminal_unix_ms = 1740787199996` (2025-02-28T23:59:59.996Z) |
| `python scripts/phase4bm_o_compute_multiday_labels.py --code-commit-sha 252f7ce5dd494097c0ee42c7213579ba5823e30e` | DONE: total_row_count = 155,153,449; manifest + sidecar written; 194 / 194 upstream immutability witnesses PASS post-run |
| `git status --short` (post-execution) | unchanged: only `.claude/scheduled_tasks.lock` and `data/research/` untracked (no `data/microstructure/` entry; the 182 new files are gitignored under `.gitignore:85`) |
| `git check-ignore -v data/microstructure/labels/` | covered by `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/` | covered by `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json` | covered by `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json.sha256` | covered by `.gitignore:85: data/microstructure/` |
| 90 label parquets exist | YES (90 / 90 verified) |
| 90 label sidecars exist | YES (90 / 90 verified) |
| 1 label manifest exists | YES |
| 1 label manifest sidecar exists | YES |
| Label manifest `row_count` | **155,153,449** |
| Label manifest `column_count` | **40** |
| Label manifest `date_count` | **90** |
| Label manifest `research_eligible` | `false` |
| Label manifest `eligibility_gate_status` | `"pending"` |
| Label manifest `label_family_research_use_authorized` | `false` |
| Label manifest `stage_5_label_cleared` | `false` |
| Label manifest `chronological_split_policy` | `"not_yet_defined"` |

## 24. Skipped checks and rationale

`mypy src/prometheus` and whole-repo `pytest` were skipped at Phase 4bm-O level. Rationale:

- Phase 4bm-O modules mirror the v001 Phase 4bj-C and v002 Phase 4bm-H idioms verbatim for `numpy` / `pyarrow` / `Decimal` usage; no new third-party dependency or unusual annotation pattern is introduced.
- The documented baseline of 29 mypy errors in 5 files and 15 pytest collection errors (missing `httpx` / `duckdb` modules) plus 2 `test_engine_d1a_dispatch.py` subprocess failures is unchanged on `main` and is unrelated to label / feature surfaces.
- The targeted Phase 4bm-O test sweep (91 new tests + 1623 microstructure tests) all pass with no new regression.
- Any future Phase 4bm-O merge phase may rerun the full mypy + whole-repo pytest passes if the operator wishes to record them at merge-closeout time.

## 25. What this phase proves

- a deterministic, reproducible, leakage-safe, envelope-bounded v002 label kernel exists and runs to completion over the v002 envelope;
- the v002 label artefacts conform to the Phase 4bm-N 40-column schema verbatim;
- the v002 label artefacts preserve the byte-immutability discipline of Phase 4bm-H / Phase 4bm-J / Phase 4bm-L / Phase 4bm-M / Phase 4bm-N: all 194 upstream artefacts remain byte-identical pre/post the run;
- the 155,153,449 aggregate label row count matches the v002 feature row count exactly (per-day parity verified for every one of the 90 days);
- the v002 label `label_config_hash` is deterministic across reruns and includes every schema-locking field plus the six v002 lineage SHAs and `feature_config_hash`;
- the v002 label manifest carries the locked governance defaults (`research_eligible = false`, `eligibility_gate_status = "pending"`, `label_family_research_use_authorized = false`, `stage_5_label_cleared = false`, `chronological_split_policy = "not_yet_defined"`);
- the v002 label parquets and label manifest are gitignored under `.gitignore:85` and are not committed.

## 26. What this phase does not prove

- that any v002 label has predictive value;
- that forward log returns at any v002 horizon are forecastable;
- that direction classification at any v002 horizon is forecastable;
- that any v002 label-based ML model would generalise;
- that any v002 label-based strategy would be edge-positive;
- that the v002 label schema is the **right** schema (only that it is the **finalised** Phase 4bm-N schema correctly materialised);
- that any future v002 label phase is authorized.

## 27. Non-authorization

Phase 4bm-O does **not**, and **cannot**, authorize:

- Phase 4bm-P (any provisional successor; not authorized);
- multi-day v002 label structural QA (multi-day analogue of Phase 4bj-D);
- multi-day v002 label-family eligibility gate (multi-day analogue of Phase 4bj-E);
- multi-day v002 label-family research-use decision (multi-day analogue of Phase 4bj-F);
- multi-day v002 label-family successor-state recording (multi-day analogue of Phase 4bj-G);
- multi-day v002 chronological-split-policy memo (multi-day analogue of Phase 4bj-H / 4bj-I);
- multi-day v002 chronological-split-policy successor-state recording (multi-day analogue of Phase 4bj-J);
- multi-day v002 diagnostics;
- multi-day v002 ML training, model selection, feature ranking, meta-labeling;
- multi-day v002 strategy specification, implementation, signal construction;
- multi-day v002 backtest specification, plan, or execution;
- additional acquisition (no additional days, no additional symbols, no mark-price / order-book / funding / OI / liquidation / cross-venue data, no aggTrades acquisition beyond the existing locked v002 90-day envelope);
- Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-*;
- Phase 5;
- Phase 4 canonical;
- paper / shadow;
- live-readiness;
- deployment;
- exchange-write;
- production-key creation;
- authenticated APIs;
- private endpoints;
- public-endpoint calls in code;
- user-stream / live WebSocket implementation;
- MCP / Graphify / `.mcp.json` / credentials;
- any modification of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` / `stage_4_feature_cleared` / `stage_5_label_cleared` on any actual on-disk manifest;
- any committed `data/microstructure/` artefact;
- amending Phase 4ak M0, Phase 4al refined no-rescue rule, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks, Phase 4bm-A-P1, Phase 4bm-D-P1, Phase 4bm-E, Phase 4bm-F, Phase 4bm-G, Phase 4bm-H, Phase 4bm-I, Phase 4bm-J, Phase 4bm-K, Phase 4bm-L, Phase 4bm-M, or Phase 4bm-N;
- any further successor-state JSON creation;
- any successor phase whatsoever.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, the operator-report standard, and the merge-closeout standard.

Reusable non-authorization blocks honored: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST** (the v002 feature / derived / raw manifests remain byte-identical; a new sibling v002 label manifest is the only manifest written, and it is gitignored), **N-GATE-RERUN**, **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**, **N-SUCCESSOR-STATE** (no successor-state artefact created by Phase 4bm-O). **N-DERIVATION** does NOT apply — Phase 4bm-O is the explicitly authorized label-kernel computation phase.

## 28. Recommended state

**Remain paused.**

Phase 4bm-O is branch-complete by this work. Per the Phase 4bk-A workflow standard, Phase 4bm-O is **NOT** project-complete until a separately authorized merge phase records its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1; full 16-section merge-closeout). The operator's broader pause decision continues to apply.

## 29. Conditional next options, none authorized

| Option | Type | Status |
| --- | --- | --- |
| **Primary** — remain paused | docs-only / no work | **recommended** |
| **Conditional next** — future operator-authorized Phase 4bm-O merge phase | docs + merge | **NOT authorized by this memo** |
| **Conditional later** — future Phase 4bm-P (Multi-Day V002 Label Artefact Structural QA Memo; provisional name) | docs + read-only analysis | **NOT authorized** |
| **Conditional later** — future label-family eligibility gate (multi-day analogue of Phase 4bj-E) | code + docs + local gitignored gate report | **NOT authorized** |
| **Conditional later** — future label-family research-use decision (multi-day analogue of Phase 4bj-F) | docs-only | **NOT authorized** |
| **Conditional later** — future label-family successor-state recording (multi-day analogue of Phase 4bj-G) | docs + local gitignored successor-state | **NOT authorized** |
| **Conditional later** — future multi-day v002 chronological-split-policy memo | docs-only | **NOT authorized** |
| Acquisition (additional days / symbols / data families beyond the 90 locked v002 dates) | docs + data | **NOT authorized; not in scope** |
| Diagnostics / ML / strategy / backtest work on v002 (or v001) | code + data | **FORBIDDEN by Phase 4bm-O** |
| Paper / shadow / live / exchange-write / production keys | runtime | **FORBIDDEN by Phase 4bm-O** |

## 30. Required exact phrases (verbatim, per task brief)

- **Phase 4bm-O implements the Phase 4bm-N label schema and generates local gitignored label artefacts only.**
- **No label artefact is committed by Phase 4bm-O.**
- **Phase 4bm-P is not authorized by Phase 4bm-O.**
- **Label artefact structural QA is not authorized by Phase 4bm-O.**
- **Label-family eligibility gate is not authorized by Phase 4bm-O.**
- **Label-family research-use is not authorized by Phase 4bm-O.**
- **Diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-O.**
- **No feature artefact was modified.**
- **No upstream artefact was mutated.**
- **No data/microstructure file was committed.**
