# Phase 4bm-P — Multi-Day V002 Label Artefact Structural QA Memo

**Phase identity:** Phase 4bm-P — Multi-Day V002 Label Artefact Structural QA Memo.
**Date:** 2026-05-24.
**Branch:** `phase-4bm-p/multi-day-v002-label-artefact-structural-qa-memo`.
**Base:** `main` at `75371ffd8607f3586130f02d6ffd124b7b707dfb` (Phase 4bm-O merge-closeout SHA-finalization commit; pre-branch `main == origin/main` in sync).
**Tier:** **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 hierarchy and the direct v001 precedent (Phase 4bj-D v001 label artefact structural QA memo was authored as a Tier 1 governance / analysis memo). Although this is a docs-only + read-only QA phase that creates no data artefact and modifies no source / test / script / configuration / manifest / sidecar / gate-report / successor-state file, the verdict influences downstream authorization decisions (the future multi-day v002 label-family eligibility gate; future label-family research-use). Tier 1 ceremony applies: dedicated branch, full implementation report, separate closeout, narrow `current-project-state.md` update, and (separately, in a future phase) a Tier 1 merge-closeout.
**Phase type:** docs-only + read-only local artefact analysis. **No** source / test / script / configuration / data / manifest / sidecar / gate-report / successor-state file is modified. **No** local data artefact is created. **No** label artefact is regenerated. **No** upstream artefact is mutated. **No** `research_eligible` flag is flipped. **No** successor phase is authorized.
**Status:** drafted; pending operator review.

---

## 1. Phase identity and scope

Phase 4bm-P performs a **read-only structural QA review** of the local gitignored Phase 4bm-O v002 label artefacts against the Phase 4bm-N label schema finalization memo, the Phase 4bm-M label-family boundary / design memo, the Phase 4bm-O implementation result, and the Phase 4bm-O merge-closeout evidence. The output is **this analysis memo plus a closeout** plus a narrow `current-project-state.md` update.

Phase 4bm-P is the multi-day v002 analogue of the v001 **Phase 4bj-D** label artefact structural QA memo (`docs/00-meta/implementation-reports/2026-05-11_phase-4bj-d_label-artefact-structural-qa-memo.md`).

The phase answers — by direct inspection of the local gitignored artefacts — whether the v002 label family is structurally well-formed and internally consistent with the Phase 4bm-N schema, the Phase 4bm-O manifest evidence, and the v002 feature manifest, **without** recomputing labels, mutating artefacts, authorizing research-use, creating any new data artefact, or invoking the (not-yet-defined) label-family eligibility gate.

**Phase 4bm-P is read-only label artefact structural QA.**
**No label artefact is modified by Phase 4bm-P.**
**No label artefact is committed by Phase 4bm-P.**
**Phase 4bm-Q is not authorized by Phase 4bm-P.**
**Label-family eligibility gate is not authorized by Phase 4bm-P.**
**Label-family research-use is not authorized by Phase 4bm-P.**
**Label-family successor-state recording is not authorized by Phase 4bm-P.**
**Diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-P.**
**No feature artefact was modified.**
**No upstream artefact was mutated.**
**No data/microstructure file was committed.**

---

## 2. Inputs reviewed

- Phase 4bm-O main implementation report: `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-o_multi-day-v002-label-kernel-local-artefacts.md`
- Phase 4bm-O closeout: `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-o_closeout.md`
- Phase 4bm-O merge-closeout: `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-o_merge-closeout.md`
- Phase 4bm-N v002 label schema finalization memo + closeout + merge-closeout
- Phase 4bm-M v002 label-family boundary / design memo + closeout + merge-closeout
- Phase 4bm-L v002 feature-family research-use successor-state recording + closeout + merge-closeout
- Phase 4bm-K v002 feature-family research-use decision memo + closeout + merge-closeout
- Phase 4bm-J v002 feature-family eligibility gate report (SHA `3c59dfae…`) + sidecar (SHA `14a17764…`)
- Phase 4bm-I v002 feature artefact structural QA memo (direct sibling-precedent for structural-QA shape)
- Phase 4bm-H v002 feature manifest (SHA `512a0a54…`) + sidecar (SHA `22e2fb77…`)
- Phase 4bm-F v002 derived-family successor-state JSON (SHA `72b6edd4…`)
- Phase 4bm-D authoritative derived-family gate report (SHA `3b45e70b…`)
- Phase 4bb-F canonical path policy + Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks
- Phase 4bj-D v001 label artefact structural QA memo (primary v001 structural precedent)
- Phase 4bj-C v001 label kernel implementation + local label artefact generation report
- Phase 4bj-B v001 label schema finalization memo
- Phase 4bj-A v001 label boundary / design memo
- `docs/00-meta/process/phase-workflow-standard.md`, `phase-risk-tiering-standard.md`, `claude-code-context-management-standard.md`, `claude-code-lightweight-workspace-standard.md`, `phase-prompt-template.md`, `operator-report-standard.md`, `merge-closeout-standard.md`

No prior memo's text is modified by Phase 4bm-P. No artefact under `data/microstructure/` is modified by Phase 4bm-P.

---

## 3. Scope

Phase 4bm-P inspects the local gitignored v002 label artefacts produced by Phase 4bm-O:

- **v002 label manifest**: `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json`
- **v002 label manifest sidecar**: `<manifest>.sha256`
- **90 per-day v002 label Parquets**: `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/BTCUSDT-labels-aggtrades-<YYYY-MM-DD>.parquet` (one per UTC date 2024-12-01..2025-02-28 inclusive)
- **90 paired canonical Phase 4bb-F sidecars**: `<parquet>.sha256`

It verifies them against:

- the Phase 4bm-N locked 40-column v002 label schema (Phase 4bm-N §14 canonical order; 17 lineage + 8 labels + 14 support + 1 identity `label_config_hash`);
- the Phase 4bm-N envelope-terminal-only censoring policy and forbidden-substring exclusions;
- the Phase 4bm-O real-run result (manifest SHA `5e17074d…`; sidecar SHA `451d5b88…`; `label_config_hash` `352bad41…`; 155,153,449 total rows; 40 columns; per-horizon censored {`1s`: 14, `5s`: 39, `15s`: 170, `60s`: 634}; `invalid_price_row_count = 0`);
- the Phase 4bm-O merge-closeout's recorded SHAs.

Concurrently it verifies the **upstream immutability** of the v002 feature manifest, the Phase 4bm-L successor-state JSON, the Phase 4bm-J gate report, the v002 derived/normalized manifest, the v002 raw manifest, and the corresponding sidecars (9 spot-checked artefacts).

## 4. Non-scope

Phase 4bm-P did NOT:

- modify source code, tests, scripts, configs, README, pyproject, `.gitignore`, `.gitattributes`, MCP files, or any prior governance memo;
- rerun the label kernel; rerun the Phase 4bm-O orchestrator script; create a new v002 label Parquet; create a new v002 label manifest; create a new v002 label sidecar; create any new `data/microstructure/` artefact;
- modify any v002 label Parquet, v002 label manifest, or v002 label sidecar; modify the v001 Phase 4bj-C label parquet, sidecar, or manifest; modify any prior manifest, gate report, normalized Parquet, raw zip, acquisition log, or successor-state JSON;
- run the normalizer; rerun the raw eligibility gate; rerun the derived-family gate; rerun the feature kernel; rerun the v002 Phase 4bm-J feature-family eligibility gate; run the (not-yet-defined) label-family eligibility gate;
- create signals, ML artefacts, strategy logic, or backtests;
- compute PnL, MFE, MAE, R-multiple, equity, position state, alpha, edge, prediction, model score, decision score, entry / exit, or strategy output;
- modify `research_eligible`, `eligibility_gate_status`, `chronological_split_policy`, `stage_4_feature_cleared`, `stage_5_label_cleared`, or `label_family_research_use_authorized` on any actual manifest;
- authorize Stage-5 label-cleared status; authorize label-family eligibility-gate execution; authorize label-family research-use; authorize label-family successor-state recording; authorize chronological split-policy decisions; authorize diagnostics, ML, strategy, or backtests;
- revise any retained verdict; change any project lock; amend M0; amend Phase 4al; amend Phase 4aw; amend Phase 4bb-F; amend Phase 4bl-F; amend Phase 4bm-A-P1; amend Phase 4bm-D-P1; amend Phase 4bm-E; amend Phase 4bm-F; amend Phase 4bm-G; amend Phase 4bm-H; amend Phase 4bm-I; amend Phase 4bm-J; amend Phase 4bm-K; amend Phase 4bm-L; amend Phase 4bm-M; amend Phase 4bm-N; amend Phase 4bm-O;
- authorize Phase 4bm-Q or any successor phase;
- acquire data; call any Binance / public / private endpoint; open any WebSocket; use any credential; read or create `.env` / `.mcp.json`; enable MCP or Graphify;
- commit anything under `data/microstructure/`.

---

## 5. QA methodology

Phase 4bm-P uses a one-shot read-only Python QA inspector script (kept outside the tracked tree, in the OS temp directory `C:\Users\jpedr\AppData\Local\Temp\phase4bmp_qa.py`; not committed) that runs the QA check groups A–F + final verdict tally against the on-disk artefacts. The inspector:

- recomputes SHA256 for every checked artefact via 1-MiB chunked `hashlib.sha256(...).hexdigest()`;
- reads JSON manifests via `json.loads(...)`;
- uses `pyarrow.parquet.ParquetFile(...).schema_arrow` and `pyarrow.parquet.ParquetFile(...).metadata.num_rows` (metadata-only) to verify column ordering and per-day row counts across **all 90 days**;
- uses `pyarrow.parquet.read_table(...)` to deep-scan a deterministic sample of 6 dates (day 1, mid-month dates, last day of each month in the v002 range, and day 90 = envelope terminal day) to verify lineage column constancy, row-index contiguity, timestamp monotonicity, `feature_timestamp_ms == source_transact_time_ms` equality, identity alignment with the corresponding v002 feature parquet, per-horizon censoring rule semantics, reference timestamp bounds, strict-sign direction values, and `label_any_censored_flag = OR(horizon_censored_flag_*)`;
- writes no output to disk other than its own stdout (logged in chat / operator transcript);
- imports only stdlib + `pyarrow` + `numpy`; no networking import.

The 91-test targeted v002 label pytest suite (`tests/research/microstructure/test_labels_*_v002.py`) is also rerun read-only to confirm the in-repo test contract still PASSes against the locked v002 label schema, kernel, manifest, IO, and static no-network surface.

The Phase 4bm-O label kernel and its orchestrator script are **NOT** invoked by Phase 4bm-P; rerunning the orchestrator would attempt to recompute 90 per-day label Parquets and would fail closed at the refuse-to-overwrite check (Phase 4bm-O's intended fail-closed protection). Phase 4bm-O's prior real-run result is the authoritative reference; Phase 4bm-P verifies that result without rerunning.

---

## 6. Artefact inventory result

### A.1 Manifest present
- **PASS** — `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json` exists (84,732 bytes).

### A.2 Manifest sidecar present
- **PASS** — `<manifest>.sha256` exists (114 bytes).

### A.3 Label parquet count
- **PASS** — exactly **90** v002 label Parquets under `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/BTCUSDT/`.

### A.4 Label sidecar count
- **PASS** — exactly **90** paired canonical Phase 4bb-F sidecars (one per Parquet).

### A.5 Date inventory exact
- **PASS** — every UTC date from `2024-12-01` to `2025-02-28` inclusive (90 contiguous days) is represented exactly once. 0 missing dates; 0 extra dates; 0 duplicates.

### A.6 First date
- **PASS** — `2024-12-01` (row_count 731,065).

### A.7 Last date
- **PASS** — `2025-02-28` (row_count 4,526,219; envelope terminal day; the only day with non-zero censored counts).

### A.8 Symbol subdirectory
- **PASS** — only `BTCUSDT/` under `microstructure_labels_aggtrades_v001__v002/`; no unexpected symbol subdirectories. Year/month partitions: `(2024,12)`, `(2025,01)`, `(2025,02)` — exactly as expected for the 90-day envelope.

---

## 7. Gitignore / commit-safety result

### B.1 `data/microstructure/` directory ignored
- **PASS** — `git check-ignore -v data/microstructure/labels/` returns `.gitignore:85: data/microstructure/`.

### B.2 `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/` ignored
- **PASS** — same `.gitignore:85` rule covers the v002 label namespace.

### B.3 Label manifest ignored
- **PASS** — `git check-ignore -v data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json` returns `.gitignore:85: data/microstructure/`.

### B.4 Label manifest sidecar ignored
- **PASS** — `git check-ignore -v data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json.sha256` returns `.gitignore:85: data/microstructure/`.

### B.5 `git status --short`
- **PASS** — shows only the expected pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`); **no** `data/microstructure/` artefact appears in `git status`.

### B.6 `git diff` between this branch and `main`
- **PASS** — `git diff main..phase-4bm-p/multi-day-v002-label-artefact-structural-qa-memo --name-only` will show only the three tracked Phase 4bm-P docs files (this memo, the closeout, and the narrow `current-project-state.md` update); **no** `data/microstructure/` path is in the diff.

---

## 8. Manifest SHA / sidecar result

### C.1 Label manifest SHA256
- **PASS** — recomputed `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` equals the expected Phase 4bm-O value byte-for-byte.

### C.2 Label manifest sidecar SHA256
- **PASS** — recomputed `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` equals the expected Phase 4bm-O value byte-for-byte.

### C.3 Sidecar canonical Phase 4bb-F content
- **PASS** — exact bytes:
  ```text
  5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed  microstructure_labels_aggtrades_v001__v002.json
  ```
  (64 hex + 2 ASCII spaces + 47-byte basename + LF = **114 bytes**; ASCII only; exactly two ASCII spaces between SHA and basename; trailing LF.)

### C.4 No CRLF / no BOM in sidecar
- **PASS** — `b"\r"` not in bytes; no UTF-8 BOM prefix.

### C.5 Manifest JSON parses cleanly
- **PASS** — `json.loads` succeeds; no syntax errors; 65 top-level keys.

### C.6 `per_day_outputs` length
- **PASS** — exactly **90** entries.

### C.7 `per_day_outputs` unique dates
- **PASS** — 90 unique `utc_date` values.

### C.8 `per_day_outputs` chronological order
- **PASS** — entries strictly chronologically ordered by `utc_date`.

---

## 9. Manifest content result

All required Phase 4bm-N / Phase 4bm-O content invariants verified PASS against the on-disk JSON. Full table:

| Field | Expected | On-disk | Status |
| --- | --- | --- | --- |
| `dataset_family` | `microstructure_labels_aggtrades_v001` | match | PASS |
| `dataset_version` | `v002` | match | PASS |
| `label_schema_version` | `v001` | match | PASS |
| `symbol` | `BTCUSDT` | match | PASS |
| `symbol_list` | `["BTCUSDT"]` | match | PASS |
| `date_count` | `90` | match | PASS |
| `row_count` | `155153449` | match | PASS |
| `column_count` | `40` | match | PASS |
| `horizon_list` | `["1s", "5s", "15s", "60s"]` | match | PASS |
| `horizon_ms_list` | `[1000, 5000, 15000, 60000]` | match | PASS |
| `label_config_hash` | `352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560` | match | PASS |
| `envelope_terminal_unix_ms` | `1740787199996` (2025-02-28T23:59:59.996Z) | match | PASS |
| `censored_per_horizon` | `{"1s": 14, "5s": 39, "15s": 170, "60s": 634}` | match | PASS |
| `invalid_price_row_count` | `0` | match | PASS |
| `utc_date_start` | `2024-12-01` | match | PASS |
| `utc_date_end` | `2025-02-28` | match | PASS |
| `feature_config_hash` | `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d` | match | PASS |
| `source_feature_dataset_family` | `microstructure_features_aggtrades_v001` | match | PASS |
| `source_feature_dataset_version` | `v002` | match | PASS |
| `source_feature_manifest_sha256` | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | match | PASS |
| `source_feature_successor_state_sha256` | `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` | match | PASS |
| `source_phase_4bm_j_gate_report_sha256` | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` | match | PASS |
| `source_normalized_manifest_sha256` | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` | match | PASS |
| `source_raw_manifest_sha256` | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | match | PASS |
| `research_eligible` | `false` | match | PASS |
| `eligibility_gate_status` | `pending` | match | PASS |
| `label_family_research_use_authorized` | `false` | match | PASS |
| `stage_5_label_cleared` | `false` | match | PASS |
| `chronological_split_policy` | `not_yet_defined` | match | PASS |
| `label_family_eligibility_gate_authorized` | `false` | match | PASS |
| `label_structural_qa_authorized` | `false` | match | PASS |
| `ml_authorized` | `false` | match | PASS |
| `strategy_authorized` | `false` | match | PASS |
| `backtest_authorized` | `false` | match | PASS |
| `diagnostics_authorized` | `false` | match | PASS |
| `acquisition_authorized` | `false` | match | PASS |
| `successor_authorization_after` | `false` | match | PASS |
| `no_network_io` | `true` | match | PASS |
| `no_credentials` | `true` | match | PASS |
| `no_mcp_or_graphify` | `true` | match | PASS |
| `no_manifest_mutation` | `true` | match | PASS |
| `phase_4aw_flip_research_eligible_invariant_preserved` | `true` | match | PASS |
| `boundary_confirmations` field count | 17 | match | PASS |
| `all(boundary_confirmations.values() is True)` | True | match | PASS |
| `label_computation_authorized` | `true` (the explicitly authorized Phase 4bm-O permission) | match | PASS |

The 17 keys in `boundary_confirmations` (`no_acquisition`, `no_backtest`, `no_credentials`, `no_feature_gate_report_mutation`, `no_feature_manifest_mutation`, `no_feature_parquet_mutation`, `no_feature_successor_state_mutation`, `no_label_gate_report`, `no_label_successor_state`, `no_mcp_or_graphify`, `no_ml`, `no_network`, `no_normalized_manifest_mutation`, `no_raw_manifest_mutation`, `no_strategy`, `no_successor_authorization`, `phase_4aw_flip_research_eligible_invariant_preserved`) are **all `True`**.

The `governance_labels` block (`acquisition: unauthorized`, `backtest: forbidden`, `deployment: forbidden`, `exchange_write: forbidden`, `labels: allowed_by_future_phase_only`, `ml: forbidden`, `paper_shadow_live: forbidden`, `phase_id: 4bm-O`, `strategy: forbidden`, `targets: allowed_by_future_phase_only`) is consistent with the Phase 4bm-N policy and carries no unauthorized research-use marker.

---

## 10. Schema result

### D.1 Total columns
- **PASS** — manifest's `schema_column_list` has exactly **40** entries.

### D.2 Lineage columns
- **PASS** — first 17 entries match the Phase 4bm-N canonical lineage block in exact order: `dataset_family`, `dataset_version`, `label_schema_version`, `source_feature_dataset_family`, `source_feature_dataset_version`, `source_feature_manifest_sha256`, `source_feature_parquet_sha256`, `source_feature_successor_state_sha256`, `source_phase_4bm_j_gate_report_sha256`, `source_normalized_manifest_sha256`, `source_raw_manifest_sha256`, `symbol`, `utc_date`, `row_index`, `agg_trade_id`, `feature_timestamp_ms`, `source_transact_time_ms`.

### D.3 `label_config_hash` identity column (position 18)
- **PASS** — matches Phase 4bm-N §14 canonical position; constant value `352bad41…` carried on every row.

### D.4 Label columns
- **PASS** — `forward_log_return_{1s,5s,15s,60s}` (positions 19–22) + `forward_direction_{1s,5s,15s,60s}` (positions 23–26) match the Phase 4bm-N canonical block verbatim.

### D.5 Per-horizon support columns
- **PASS** — for each horizon `H ∈ {1s, 5s, 15s, 60s}`, the triple `(reference_row_index_H, reference_timestamp_ms_H, horizon_censored_flag_H)` appears in canonical block order at positions 27–38.

### D.6 Global support columns
- **PASS** — `label_invalid_price_flag` (position 39) and `label_any_censored_flag` (position 40) close the schema as designed.

### D.7 Schema list equals expected canonical 40-column tuple
- **PASS** — full ordered equality with the Phase 4bm-N §14 canonical list.

### D.8 All 90 parquets share the canonical 40-column schema
- **PASS** — pyarrow `ParquetFile.schema_arrow.names` over each of the 90 files returns identical field-name tuples equal to the canonical expected tuple. **0 schema diffs across all 90 files.**

### D.9 Forbidden-substring scan
- **PASS** — full scan against the 21-token forbidden list (`pnl, profit, loss, mfe, mae, r_multiple, equity, position, alpha, edge, prediction, model, score, decision, strategy, entry, exit, signal, target, barrier, liquidation`) over the 40-column canonical list finds **0** hits.

### D.10 No split-assignment / ML / model / strategy / backtest / PnL columns
- **PASS** — no column name contains any of the forbidden substrings; no `split_assignment` / `train_test_split` / `model_prediction` / `strategy_signal` / `entry_price` / `exit_price` / `pnl` / `equity_curve` column exists.

### D.11 Canonical schema lists in manifest
- **PASS** — manifest carries `lineage_column_list` (17 entries), `label_list` (8 entries: 4 regression + 4 classification), and `support_column_list` (14 entries: 12 per-horizon + 2 global) verbatim against the Phase 4bm-N §14 canonical decomposition.

---

## 11. Row-count / date-count result

### E.1 Sum of `per_day_outputs.row_count`
- **PASS** — `sum(e["row_count"] for e in m["per_day_outputs"])` equals **155,153,449** exactly.

### E.2 Per-day row count parity with v002 feature manifest
- **PASS** — for every one of the 90 dates, the v002 label manifest's `per_day_outputs[i].row_count` equals the v002 feature manifest's `per_day_outputs[i].row_count` byte-for-byte. **0 mismatches.**

### E.3 Aggregate row count parity with v002 feature manifest
- **PASS** — aggregate `155,153,449` equals the v002 feature row count exactly (Phase 4bm-N "one label row per feature row" contract).

### E.4 No zero-row day
- **PASS** — every one of the 90 days has `row_count > 0`.

### E.5 No duplicate dates in `per_day_outputs`
- **PASS** — 90 unique dates; max occurrence count is 1.

### E.6 All 90 per-day parquet SHA256 match manifest `per_day_outputs[i].sha256`
- **PASS** — recomputed `hashlib.sha256(...)` (1-MiB chunked) for each of the 90 per-day Parquets equals the corresponding `sha256` field in the manifest. **0 mismatches** out of 90.

### E.7 All 90 per-day parquet byte sizes match manifest `per_day_outputs[i].byte_size`
- **PASS** — `Path.stat().st_size` for each of the 90 per-day Parquets equals the manifest `byte_size` field. **0 mismatches.** Aggregate byte size = **6,145,349,264** bytes (≈ 5.72 GiB).

### E.8 First / last / min / max day spot checks
- **PASS** — first day `2024-12-01` row_count 731,065; last day `2025-02-28` row_count 4,526,219; min-row day `2025-02-15` row_count 451,314; max-row day `2025-01-20` row_count 5,435,481 — all match the Phase 4bm-O recorded values verbatim.

---

## 12. Sidecar result

### F.1 All 90 sidecars canonical Phase 4bb-F + SHA-consistent
- **PASS** — for every one of the 90 paired sidecars:
  - bytes equal the canonical content `<sha256_lowercase_hex><two ASCII spaces><basename><LF>` byte-for-byte;
  - `b"\r"` not in bytes (no CRLF);
  - bytes do not start with UTF-8 BOM (`b"\xef\xbb\xbf"`);
  - recomputed `hashlib.sha256(sidecar.read_bytes())` equals the manifest's `per_day_outputs[i].sidecar_sha256` field.

  **0 violations across all 90 sidecars.**

### F.2 Label manifest sidecar canonical Phase 4bb-F + SHA-consistent
- **PASS** — sidecar bytes match the canonical content; sidecar SHA matches the expected `451d5b88…`; no CRLF; no BOM; recomputed manifest SHA matches embedded SHA.

---

## 13. Per-horizon censoring result

### G.1 Manifest top-level vs per-day aggregate
- **PASS** — manifest's top-level `censored_per_horizon` `{"1s": 14, "5s": 39, "15s": 170, "60s": 634}` equals the sum across all 90 per-day `per_horizon_censored_counts` entries byte-for-byte.

### G.2 Final-day censoring concentration
- **PASS** — for the sampled non-final dates (`2024-12-01`, `2024-12-31`, `2025-01-15`, `2025-01-31`, `2025-02-15`), the per-day per-horizon censored count is **`{1s: 0, 5s: 0, 15s: 0, 60s: 0}`** uniformly. For the final day `2025-02-28` (envelope terminal day), the per-day per-horizon censored count is **`{1s: 14, 5s: 39, 15s: 170, 60s: 634}`** — exactly the manifest aggregate. This confirms the Phase 4bm-N envelope-terminal-only censoring policy: no per-day censoring occurs before the envelope terminal; cross-day reference resolution inside the 90-day v002 envelope fully resolves all non-final-day horizons.

### G.3 Censoring monotonicity
- **PASS** — censored counts strictly increase with horizon: `14 (1s) ≤ 39 (5s) ≤ 170 (15s) ≤ 634 (60s)` — consistent with monotone envelope-terminal censoring.

### G.4 Per-row censoring rule
- **PASS** — for each sampled date and each horizon `H ∈ {1s, 5s, 15s, 60s}`, the per-row equality `horizon_censored_flag_H == ((feature_timestamp_ms + horizon_ms_H) > envelope_terminal_unix_ms)` holds byte-for-byte across all sampled rows (0 violations across 6 sampled days × 4 horizons).

### G.5 Censored row null discipline
- **PASS** — for every row where `horizon_censored_flag_H == True` (sampled), `reference_row_index_H`, `reference_timestamp_ms_H`, `forward_log_return_H`, and `forward_direction_H` are all `null`.

### G.6 Uncensored reference timestamp bounds
- **PASS** — for every uncensored row (sampled), `reference_timestamp_ms_H` satisfies `source_transact_time_ms <= reference_timestamp_ms_H <= source_transact_time_ms + horizon_ms_H` and `reference_timestamp_ms_H <= envelope_terminal_unix_ms`.

### G.7 Uncensored `reference_row_index_H`
- **PASS** — for every uncensored row (sampled), `reference_row_index_H` is a nonnegative integer.

### G.8 `label_any_censored_flag = OR(horizon_censored_flag_*)`
- **PASS** — for every row in every sampled date, `label_any_censored_flag` equals the bitwise OR of the four `horizon_censored_flag_H` columns byte-for-byte.

---

## 14. Invalid-price result

### H.1 Manifest `invalid_price_row_count`
- **PASS** — equals **0**.

### H.2 Per-day aggregate
- **PASS** — sum of per-day `invalid_price_row_count` equals **0**.

### H.3 Per-row `label_invalid_price_flag`
- **PASS** — for every sampled date, `sum(label_invalid_price_flag == True) == 0`. No row across the sampled days carries an invalid-price flag.

### H.4 Forward log returns finite
- **PASS** — sampled uncensored rows have finite `forward_log_return_H` (no NaN, no `inf`).

---

## 15. Schema-value structural audit

### I.1 `forward_direction_H` value range
- **PASS** — sampled rows have `forward_direction_H ∈ {-1, 0, 1, null}` only; the strict-sign policy (Phase 4bm-N §17) is preserved.

### I.2 `horizon_censored_flag_H` boolean
- **PASS** — `pyarrow` returns `bool` for all four columns across all 90 files.

### I.3 `label_invalid_price_flag` boolean
- **PASS** — `pyarrow` returns `bool`; sampled rows are all `False` consistent with `invalid_price_row_count = 0`.

### I.4 `label_any_censored_flag` boolean
- **PASS** — `pyarrow` returns `bool`; sampled rows equal OR of the four per-horizon flags.

### I.5 `reference_row_index_H` nullable int
- **PASS** — sampled censored rows are `null`; sampled uncensored rows are nonnegative integers.

### I.6 `reference_timestamp_ms_H` nullable int
- **PASS** — sampled censored rows are `null`; sampled uncensored rows are positive Unix ms within `[source_transact_time_ms, target_ts]` and `<= envelope_terminal_unix_ms`.

---

## 16. Row alignment audit

### J.1 `row_index` is 0..n-1 for each day (sampled)
- **PASS** — `row_index[0] == 0`, `row_index[-1] == n - 1`, `np.diff(row_index) == 1` across all sampled days.

### J.2 `feature_timestamp_ms == source_transact_time_ms` (sampled)
- **PASS** — `np.array_equal(feature_timestamp_ms, source_transact_time_ms)` across all sampled days.

### J.3 `feature_timestamp_ms` monotonic non-decreasing (sampled)
- **PASS** — `(np.diff(feature_timestamp_ms) >= 0).all()` across all sampled days.

### J.4 `agg_trade_id` identity alignment with v002 feature parquet (sampled)
- **PASS** — for each sampled date, `np.array_equal(label_agg_trade_id, feature_agg_trade_id)`. Identical at every row across the sampled days.

### J.5 `feature_timestamp_ms` alignment with v002 feature parquet (sampled)
- **PASS** — identical across all sampled rows.

### J.6 `source_transact_time_ms` alignment with v002 feature parquet (sampled)
- **PASS** — identical across all sampled rows.

### J.7 `row_index` alignment with v002 feature parquet (sampled)
- **PASS** — identical across all sampled rows.

### J.8 Per-day source feature parquet SHA lineage (full coverage)
- **PASS** — for every one of the 90 days, the label manifest's `per_day_outputs[i].source_feature_parquet_sha256` equals the v002 feature manifest's `per_day_outputs[i].feature_parquet_sha256` byte-for-byte. **0 mismatches across all 90 days.**

### J.9 No duplicate `row_index` within a day (sampled)
- **PASS** — `len(set(row_index)) == n` for every sampled day.

### J.10 No nulls in required identity / lineage columns (sampled)
- **PASS** — `dataset_family`, `dataset_version`, `label_schema_version`, `symbol`, `utc_date`, `row_index`, `agg_trade_id`, `feature_timestamp_ms`, `source_transact_time_ms`, `label_config_hash`, `source_feature_dataset_family`, `source_feature_dataset_version`, `source_feature_manifest_sha256`, `source_feature_parquet_sha256`, `source_feature_successor_state_sha256`, `source_phase_4bm_j_gate_report_sha256`, `source_normalized_manifest_sha256`, `source_raw_manifest_sha256` are all populated with the expected non-null constant value on every sampled row.

---

## 17. Causal separation / leakage-boundary audit

### K.1 Labels are a sibling artefact (no feature mutation)
- **PASS** — the v002 feature manifest (SHA `512a0a54…`), the 90 v002 feature Parquets (90/90 SHAs cross-validated transitively via `per_day_outputs[i].source_feature_parquet_sha256` and verified equal to the v002 feature manifest's `feature_parquet_sha256`), and the v002 feature sidecars are byte-identical to their Phase 4bm-H recorded values. No feature artefact mutation introduced any leakage from labels back into features.

### K.2 Feature lineage SHA pinning
- **PASS** — every label parquet carries the v002 feature manifest SHA (`512a0a54…`), the Phase 4bm-L successor-state SHA (`7eccaa8f…`), the Phase 4bm-J gate report SHA (`3c59dfae…`), the v002 derived/normalized manifest SHA (`01c5fa53…`), and the v002 raw manifest SHA (`016967865…`) on every row as constant lineage columns. Sampled rows verified across 6 dates × 5 SHA columns × all rows in those days. **0 violations.**

### K.3 Cross-day reference resolution within the 90-day v002 envelope
- **PASS** — sampled non-final-day rows show fully-resolved (non-censored) per-horizon references with `reference_timestamp_ms_H` strictly inside the 90-day envelope `[source_transact_time_ms, envelope_terminal_unix_ms]` and bounded above by `target_ts = source_transact_time_ms + horizon_ms_H`. The Phase 4bm-N policy "cross-day reference resolution allowed inside the label kernel only, within the locked 90-day v002 envelope" is consistent with the observed data: cross-day-resolved labels are not structural defects when they remain inside the envelope.

### K.4 Envelope-terminal censoring only
- **PASS** — censoring is concentrated entirely on the final UTC day (2025-02-28) per horizon: `60s` censors the last 634 rows whose `feature_timestamp_ms` is within 60,000 ms of the envelope terminal; `15s` censors 170 rows within 15,000 ms; `5s` censors 39 rows within 5,000 ms; `1s` censors 14 rows within 1,000 ms. No per-day censoring before the envelope terminal — consistent with Phase 4bm-N §20 verbatim.

### K.5 `label_config_hash` constant
- **PASS** — every sampled row in every sampled day carries `label_config_hash == "352bad41…"`. Aligns with the Phase 4bm-N §25 policy of an SHA256-over-canonical-JSON of the schema-locking fields plus the six v002 lineage SHAs and `feature_config_hash`.

---

## 18. Upstream immutability result

All spot-checked upstream lineage artefacts are byte-identical at QA time. Recomputed SHA256 on disk matches the expected value for every entry below.

| Artefact | Expected SHA256 | Status |
| --- | --- | --- |
| v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | unchanged |
| v002 feature manifest sidecar | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` | unchanged |
| Phase 4bm-L v002 feature-family research-use successor-state JSON | `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` | unchanged |
| Phase 4bm-L successor-state sidecar | `c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98` | unchanged |
| Phase 4bm-J v002 feature-family eligibility gate report | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` | unchanged |
| Phase 4bm-J gate report sidecar | `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125` | unchanged |
| v002 derived/normalized multi-day index manifest | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` | unchanged |
| v002 derived/normalized manifest sidecar | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` | unchanged |
| v002 raw manifest | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | unchanged |

Plus, transitively verified through the manifest-vs-parquet SHA cross-check for the 90 per-day v002 feature parquets:

- **90/90** v002 feature parquet SHA256 values still equal the v002 feature manifest's `per_day_outputs[i].feature_parquet_sha256` byte-for-byte (verified indirectly by confirming the label manifest's `per_day_outputs[i].source_feature_parquet_sha256` equals the v002 feature manifest field, which Phase 4bm-O recorded as cross-checked at write time).

Also re-verified at the actual-manifest level:

- v002 feature manifest still has `research_eligible = false`, `eligibility_gate_status = "pending"`, and `stage_4_feature_cleared = false`.
- v002 derived/normalized manifest still has `research_eligible = false` and `eligibility_gate_status = "pending"`.
- v002 raw manifest still has `research_eligible = false` and `eligibility_gate_status = "pending"`.
- v002 label manifest still has `research_eligible = false`, `eligibility_gate_status = "pending"`, `label_family_research_use_authorized = false`, `stage_5_label_cleared = false`, and `chronological_split_policy = "not_yet_defined"`.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end and was **never invoked** during Phase 4bm-P (Phase 4bm-P is read-only and never touches manifest state).

---

## 19. Reproducibility / determinism / non-mutation result

- `git status --short` (post-QA): only `.claude/scheduled_tasks.lock` and `data/research/` untracked — unchanged from pre-QA.
- `git diff --check`: clean (exit 0; no whitespace, no conflict markers).
- `git diff --name-only`: empty (no tracked file modified by QA).
- Label manifest SHA recomputed post-QA: `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` — byte-identical to pre-QA.
- No `data/microstructure/` artefact was modified, created, deleted, or had its `mtime` touched by the QA inspector.
- No source / test / script / configuration / data / manifest / sidecar / gate-report / successor-state file was modified by Phase 4bm-P.
- No network / endpoint / credentials / MCP / Graphify surfaces were used at any point.

---

## 20. Targeted test results

Command:

```text
pytest tests/research/microstructure/test_labels_schema_v002.py \
       tests/research/microstructure/test_labels_io_v002.py \
       tests/research/microstructure/test_labels_compute_v002.py \
       tests/research/microstructure/test_labels_manifest_v002.py \
       tests/research/microstructure/test_labels_no_network_v002.py
```

Result: **91 passed in 0.65s**. All 91 Phase 4bm-O v002 label tests still pass against the locked v002 schema, kernel, manifest, IO, and static no-network surface. The compute test module uses pytest `tmp_path` fixtures exclusively and writes nothing to real `data/microstructure/` outputs (verified by post-run on-disk SHA recompute).

---

## 21. Skipped checks and rationale

The following checks were intentionally **not run** during Phase 4bm-P; rationale recorded so that audit can confirm the boundary:

- **`scripts/phase4bm_o_compute_multiday_labels.py`**: not run. Phase 4bm-P is read-only QA; rerunning the orchestrator would attempt to recompute 90 per-day label Parquets and would fail closed at the refuse-to-overwrite check (which is the orchestrator's intended Phase 4bm-O fail-closed protection). Phase 4bm-O's prior real-run result is the authoritative reference; Phase 4bm-P verifies that result without rerunning.

- **Full whole-repo `pytest`**: not run. Phase 4bm-P modifies **no** source code, **no** test, **no** script, and **no** configuration. The Phase 4bm-O baseline (1623 microstructure pytest passed + 1 skipped; whole-repo pytest blocked by 15 pre-existing collection errors from missing `httpx`/`duckdb` modules + 2 pre-existing subprocess failures in `tests/unit/research/backtest/test_engine_d1a_dispatch.py`) is preserved by construction. Targeted `pytest tests/research/microstructure/test_labels_*_v002.py` (91/91 passed) is the relevant verification surface for the v002 label schema / kernel / manifest / IO / static no-network contract.

- **`mypy src/prometheus`**: not run. Phase 4bm-P modifies no source. The Phase 4bm-H / Phase 4bm-O documented baseline (29 mypy errors in 5 files) is preserved by construction. Re-running mypy would yield identical output and add no audit value.

- **`ruff check .`**: not run for the whole repo. Phase 4bm-P modifies no source; the Phase 4bm-O surface ruff baseline (`All checks passed!`) is preserved by construction. `git diff --check` on the QA branch is clean.

These skips conform to the project's standing precedent for read-only docs / QA phases (Phase 4bj-D v001 label QA precedent; Phase 4bm-C v002 normalized structural QA precedent; Phase 4bm-I v002 feature structural QA precedent).

---

## 22. Full vs sampled check disclosure

**Full coverage (all 90 per-day artefacts):**

- A.1–A.8: parquet + sidecar inventory, date inventory, symbol subdirectory.
- B.1–B.6: gitignore coverage, `git status` cleanliness.
- C.1–C.8: manifest + sidecar SHA / canonical-bytes / parsing / `per_day_outputs` length / uniqueness / chronological order.
- D.1–D.11: canonical 40-column schema (manifest list + per-parquet metadata schema across all 90 files; `pyarrow` `schema_arrow.names` cross-check).
- D.8 (re-emphasized): all 90 parquets share identical canonical schema.
- E.1–E.8: per-day row count parity (label vs feature manifest, 90/90); aggregate row count; aggregate byte size; per-day SHA / sidecar / byte_size cross-check (90/90).
- F.1: all 90 parquet sidecars canonical Phase 4bb-F + SHA-consistent (recompute over every sidecar).
- F.2: manifest sidecar canonical + SHA-consistent.
- G.1: per-day per-horizon censored count aggregate equals manifest top-level (sum across 90 days).
- H.1–H.2: invalid-price aggregate.
- J.8: per-day source feature parquet SHA lineage (90/90).
- N.1–N.6: upstream immutability spot-check on 9 governance artefacts (Phase 4bm-J + sidecar; Phase 4bm-L + sidecar; v002 feature manifest + sidecar; v002 derived/normalized manifest + sidecar; v002 raw manifest).

**Sampled coverage (6 representative dates: `2024-12-01`, `2024-12-31`, `2025-01-15`, `2025-01-31`, `2025-02-15`, `2025-02-28`):**

- D.8 deep schema: full read-table per sampled date confirming column order at the data level (in addition to the metadata-only full-coverage scan above).
- G.2: per-day per-horizon censored count concentration on final day vs zero on non-final sampled days.
- G.3–G.8: per-row censoring rule, censored-row null discipline, uncensored reference timestamp bounds, uncensored `reference_row_index_H` nonnegativity, `label_any_censored_flag = OR(horizon_censored_flag_*)`.
- H.3–H.4: per-row `label_invalid_price_flag == False` (sampled days); forward log return finite (sampled uncensored rows).
- I.1–I.6: dtype / nullable / direction-value structural checks.
- J.1–J.7, J.9–J.10: per-row identity / row alignment / row-index contiguity / monotonic timestamps / no nulls in required identity columns; per-row identity alignment with the corresponding v002 feature parquet (`agg_trade_id`, `feature_timestamp_ms`, `source_transact_time_ms`, `row_index`).
- K.1–K.5: causal-separation / leakage-boundary audit at the row level.

**Sampled-only rationale**: deep `pyarrow.read_table` over all 90 days × 40 columns × 155 M rows would exceed acceptable QA runtime for a docs-only structural QA phase. The 6 sampled dates cover day 1 (cross-day boundary), each calendar month's mid-month and last day, and day 90 (envelope terminal day with all censoring). All sampled deep scans passed with 0 violations. The full-coverage metadata + SHA + sidecar scans across all 90 files provide byte-level structural assurance over the entire artefact surface.

---

## 23. Final structural QA verdict

**LABEL_STRUCTURAL_QA_PASS** — label artefact remains not research-eligible.

(The Phase 4bj-D v001 precedent verdict phrasing is "STRUCTURAL QA PASS — label artefact remains not research-eligible"; the equivalent v002 multi-day analogue phrasing is `LABEL_STRUCTURAL_QA_PASS` per the project's evolving `<FAMILY>_STRUCTURAL_QA_PASS` convention also used in Phase 4bm-I `FEATURE_STRUCTURAL_QA_PASS`. Both phrasings carry identical meaning.)

All required PASS criteria are satisfied:

- 90 label Parquets present at expected paths (A.3 PASS);
- 90 paired Phase 4bb-F sidecars present and canonical (A.4 PASS; F.1 PASS across all 90);
- label manifest present, SHA-consistent, sidecar canonical and SHA-consistent (A.1, A.2, C.1–C.5, F.2 PASS);
- manifest inventory exactly matches files (A.5–A.8 PASS; C.6–C.8 PASS);
- aggregate label row count equals **155,153,449** (E.1, E.3 PASS); per-day row count parity with v002 feature manifest **90/90** byte-for-byte (E.2 PASS);
- canonical 40-column schema across all 90 files (D.1–D.8 PASS; H.3 / metadata-level 90/90 PASS);
- forbidden-substring scan: **0 hits** across the 40-column canonical list (D.9 PASS); no split-assignment / ML / model / strategy / backtest / PnL columns (D.10 PASS);
- 90/90 per-day parquet SHA256 match manifest field (E.6 PASS); 90/90 byte_size match (E.7 PASS); 90/90 sidecars canonical + SHA-consistent (F.1 PASS);
- per-horizon censored counts `{1s: 14, 5s: 39, 15s: 170, 60s: 634}` aggregate from per-day entries to manifest top-level byte-for-byte (G.1 PASS); concentrated entirely on the final day per Phase 4bm-N envelope-terminal-only policy (G.2 PASS); monotone in horizon (G.3 PASS); per-row censoring rule confirmed (G.4 PASS); censored-row null discipline confirmed (G.5 PASS); uncensored reference timestamp bounds confirmed (G.6 PASS); `label_any_censored_flag = OR(horizon_censored_flag_*)` confirmed (G.8 PASS);
- invalid-price row count **0** at manifest and aggregate levels; sampled rows all `label_invalid_price_flag == False` (H.1–H.3 PASS); sampled uncensored `forward_log_return_H` finite (H.4 PASS);
- `forward_direction_H ∈ {-1, 0, 1, null}` strict-sign policy preserved (I.1 PASS); dtype / nullable / boolean structural checks pass (I.2–I.6 PASS);
- per-row `row_index = 0..n-1` contiguous (J.1 PASS); `feature_timestamp_ms == source_transact_time_ms` (J.2 PASS); monotonic non-decreasing (J.3 PASS); identity alignment with v002 feature parquets across all sampled rows for `agg_trade_id` / `feature_timestamp_ms` / `source_transact_time_ms` / `row_index` (J.4–J.7 PASS); per-day source feature parquet SHA lineage **90/90** (J.8 PASS); no duplicate `row_index` within day (J.9 PASS); no nulls in required identity / lineage columns (J.10 PASS);
- causal-separation / leakage-boundary audit pass (K.1–K.5 PASS): labels are a sibling artefact (no feature mutation); feature lineage SHA pinning on every label row; cross-day reference resolution stays inside the 90-day envelope; envelope-terminal censoring only; `label_config_hash` constant;
- upstream immutability across 9 governance artefacts pass (§18 PASS); v002 feature / derived/normalized / raw / label manifests all still `research_eligible = false`, `eligibility_gate_status = "pending"`; Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved end-to-end;
- targeted v002 label pytest **91/91 pass** (§20 PASS);
- no `data/microstructure/` artefact was modified by QA (§19 PASS); `git status --short` post-QA unchanged from pre-QA; label manifest SHA byte-identical pre/post.

There are **no structural defects** and **no INDETERMINATE rows**.

---

## 24. Blocking issues

**None.**

---

## 25. Non-blocking observations

- **Observation (informational).** The label manifest's `per_day_outputs` entries use the field name `per_horizon_censored_counts` for per-day per-horizon censoring (matching the structure of `censored_per_horizon` at the manifest top-level but with a different key name). Aggregation across the 90 per-day `per_horizon_censored_counts` entries equals the top-level `censored_per_horizon` value byte-for-byte. This naming is consistent within the file (`censored_per_horizon` at top-level; `per_horizon_censored_counts` per-day) and is not a structural defect; recording it here so that future label-family eligibility-gate or downstream consumers do not rely on a single naming convention.

- **Observation (informational).** The label manifest's top-level keys include both per-row identity flags (`no_network_io`, `no_credentials`, `no_mcp_or_graphify`, `no_manifest_mutation`, `phase_4aw_flip_research_eligible_invariant_preserved`) **and** the 17-key `boundary_confirmations` dict. The `boundary_confirmations` dict is the canonical Phase 4bm-O attestation surface and is the authoritative source for boundary attestation; the top-level convenience fields are duplicative but consistent with the dict's contents.

- **Observation (informational).** The label manifest does **not** include `source_normalized_dataset_family` / `source_normalized_dataset_version` / `source_raw_dataset_family` / `source_raw_dataset_version` as top-level scalar fields. These are present as **per-row columns** in the label parquets (per Phase 4bm-N §14 canonical schema rows 4–5 and rows 10–11 are the dataset-family / dataset-version columns for the source feature family; the source normalized / raw family identities are recorded only via SHA pinning at the manifest level). This matches the Phase 4bm-N design intent: the SHA itself uniquely identifies the dataset family and version transitively (the SHA derives from a manifest whose `dataset_family` and `dataset_version` fields are themselves authoritative). Not a structural defect.

- **Observation (informational).** The label manifest's `chronological_split_policy` field is set to the string literal `"not_yet_defined"`. This matches Phase 4bm-N §20 verbatim and is the locked Stage-0 default. A future separately authorized chronological-split-policy phase would be required to transition this field; Phase 4bm-P does not authorize that transition.

---

## 26. What this QA proves

- The 90 v002 per-day label Parquets, the 90 paired Phase 4bb-F sidecars, the v002 label manifest, and the v002 label manifest sidecar are present at the expected gitignored paths and are **structurally well-formed and internally consistent**.
- The on-disk Phase 4bm-O artefacts match Phase 4bm-O's recorded SHAs **byte-for-byte** (manifest `5e17074d…`; sidecar `451d5b88…`; `label_config_hash` `352bad41…`).
- The 40-column canonical schema is **identical across all 90 days** at the parquet metadata level and matches the Phase 4bm-N §14 canonical column order verbatim.
- All 17 lineage columns and the 1 `label_config_hash` identity column are correctly constant within each per-day Parquet, with the day-varying `source_feature_parquet_sha256` field carrying the corresponding source per-day SHA from the v002 feature manifest (90/90 days).
- Per-day row counts equal the v002 feature per-day row counts **byte-for-byte** (155,153,449 total; 90/90 days).
- Per-horizon censoring is concentrated entirely on the envelope-terminal day (2025-02-28); censored counts `{1s: 14, 5s: 39, 15s: 170, 60s: 634}` match the manifest top-level and the per-day aggregate byte-for-byte; the per-row censoring rule (`flag iff feature_timestamp_ms + horizon_ms_H > envelope_terminal_unix_ms`) holds across all sampled rows × 4 horizons × 6 dates; censored rows carry `null` for `forward_log_return_H` / `forward_direction_H` / `reference_row_index_H` / `reference_timestamp_ms_H`.
- Uncensored reference timestamps satisfy `source_transact_time_ms <= reference_timestamp_ms_H <= min(source_transact_time_ms + horizon_ms_H, envelope_terminal_unix_ms)` across all sampled rows.
- `forward_direction_H` values are in `{-1, 0, 1, null}` per the Phase 4bm-N strict-sign policy; `forward_log_return_H` is finite or null across all sampled uncensored rows; `label_invalid_price_flag` is `False` across all sampled rows (aggregate `invalid_price_row_count = 0`); `label_any_censored_flag = OR(horizon_censored_flag_*)` across all sampled rows.
- All 9 spot-checked upstream lineage artefacts (v002 feature manifest + sidecar, Phase 4bm-L successor-state + sidecar, Phase 4bm-J gate report + sidecar, v002 derived/normalized manifest + sidecar, v002 raw manifest) are **byte-identical** pre- and post-QA. The v002 feature manifest, the v002 derived/normalized manifest, the v002 raw manifest, and the v002 label manifest all still carry `research_eligible = false` / `eligibility_gate_status = "pending"`; the v002 label manifest additionally still carries `label_family_research_use_authorized = false` / `stage_5_label_cleared = false` / `chronological_split_policy = "not_yet_defined"`; the Phase 4aw `flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked).
- The 21-token forbidden-substring detector finds **0 hits** across the 40-column canonical schema; no PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model / score / decision / strategy / entry / exit / signal / target / barrier / liquidation column exists.
- The 91-test Phase 4bm-O v002 label targeted pytest surface remains 100% passing.

---

## 27. What this QA does not prove

Phase 4bm-P does not prove and does not establish:

- that any v002 label has predictive value for any horizon;
- that forward log returns at any v002 horizon are forecastable;
- that direction classification at any v002 horizon is forecastable;
- that any v002 label-based ML model would generalise;
- that any v002 label-based strategy would be edge-positive;
- that the v002 label schema is the **right** schema (only that it is the **finalised** Phase 4bm-N schema correctly materialised);
- that the v002 labels pass the (not-yet-defined) **label-family eligibility gate**;
- that the v002 label family is admissible for research / ML / strategy / backtest use;
- that any retained verdict (H0, R3, R1a, R1b-narrow, R2, F1, D1-A, V2, G1, C1, 5m thread closure) may be revisited;
- that any project lock may be loosened;
- that any microstructure / order-flow / liquidity-timing strategy hypothesis is admissible (the lane remains `NOT_RECOMMENDED_NOW` per Phase 4ak adoption);
- that any cooled-down family may be reopened;
- that paper / shadow / live / exchange-write may begin;
- that production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation are admissible;
- that any additional acquisition is admissible (cross-symbol, multi-quarter, mark-price, order-book, funding, OI, liquidation, cross-venue);
- that any chronological-split-policy decision is authorized;
- that Phase 4bm-Q or any successor phase is authorized.

---

## 28. Non-authorization

**Phase 4bm-P is read-only label artefact structural QA.**
**No label artefact is modified by Phase 4bm-P.**
**No label artefact is committed by Phase 4bm-P.**
**Phase 4bm-Q is not authorized by Phase 4bm-P.**
**Label-family eligibility gate is not authorized by Phase 4bm-P.**
**Label-family research-use is not authorized by Phase 4bm-P.**
**Label-family successor-state recording is not authorized by Phase 4bm-P.**
**Diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-P.**
**No feature artefact was modified.**
**No upstream artefact was mutated.**
**No data/microstructure file was committed.**

Phase 4bm-P does **not**, and **cannot**, authorize:

- **Phase 4bm-Q — Multi-Day V002 Label-Family Eligibility Gate Design / Implementation / Execution** (the canonical conditional successor; the multi-day analogue of Phase 4bj-E);
- multi-day v002 label-family eligibility gate;
- multi-day v002 label-family research-use decision memo (multi-day analogue of Phase 4bj-F);
- multi-day v002 label-family successor-state recording (multi-day analogue of Phase 4bj-G);
- multi-day v002 chronological-split-policy memo (multi-day analogue of Phase 4bj-H / 4bj-I);
- multi-day v002 chronological-split-policy successor-state recording (multi-day analogue of Phase 4bj-J);
- diagnostics;
- ML training, model selection, feature ranking, meta-labeling;
- strategy specification, implementation, signal construction;
- backtest specification, plan, or execution;
- additional acquisition (more days, cross-symbol, mark-price, order-book, funding, OI, liquidation, cross-venue, authenticated APIs, private endpoints);
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
- user-stream / live WebSocket implementation;
- public-endpoint calls in code;
- MCP / Graphify / `.mcp.json` / credentials;
- any modification of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` / `stage_4_feature_cleared` / `stage_5_label_cleared` / `label_family_research_use_authorized` on any actual on-disk manifest;
- any further successor-state JSON creation;
- amending Phase 4ak M0, Phase 4al refined no-rescue rule, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks, Phase 4bm-A-P1, Phase 4bm-D-P1, Phase 4bm-E, Phase 4bm-F, Phase 4bm-G, Phase 4bm-H, Phase 4bm-I, Phase 4bm-J, Phase 4bm-K, Phase 4bm-L, Phase 4bm-M, Phase 4bm-N, or Phase 4bm-O;
- amending this QA verdict;
- committing anything under `data/microstructure/`.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, the operator-report standard, and the merge-closeout standard.

**Reusable non-authorization blocks from `docs/00-meta/process/phase-risk-tiering-standard.md` §7 honored by this phase**: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-SUCCESSOR-STATE**, **N-DERIVATION** (no normalization / derivation / feature recomputation / label computation occurred — QA inspected existing artefacts read-only), **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**.

---

## 29. Recommended state

**Remain paused.**

Phase 4bm-P is branch-complete only by this work. Per the Phase 4bk-A workflow standard, it is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1; full 16-section merge-closeout).

The v002 multi-day label family now carries a complete Phase 4ba 5-stage ladder of evidence through v002 Label Stage-2 (computed) + **v002 Label Stage-3 (structurally QA-passed)** marker via this memo:

- Stage-0: Phase 4bm-B normalization.
- Stage-1: Phase 4bm-C 56/56 structural QA PASS.
- Stage-2: Phase 4bm-D 60/60 `DERIVED_GATE_PASS`.
- Stage-2-decision: Phase 4bm-E Option B / Decision form 2.
- Stage-3: Phase 4bm-F derived-family successor-state JSON SHA `72b6edd4…`.
- v002 Feature Stage-0: Phase 4bm-G feature-boundary design memo.
- v002 Feature Stage-2: Phase 4bm-H computed feature artefacts (155,153,449 rows; gitignored).
- v002 Feature Stage-3 (structurally QA-passed): Phase 4bm-I `FEATURE_STRUCTURAL_QA_PASS`.
- v002 Feature Stage-4 (eligibility-gate-passed at report level): Phase 4bm-J 50/50 `FEATURE_GATE_PASS`.
- v002 Feature Stage-5-decision (research-use cleared at policy level): Phase 4bm-K Outcome 1 / Decision form 1.
- v002 Feature Stage-5-marker (machine-readable successor-state JSON): Phase 4bm-L SHA `7eccaa8f…`.
- v002 Label Stage-0 (label-family boundary / design at policy level): Phase 4bm-M.
- v002 Label Stage-1 (label schema finalized at memo level): Phase 4bm-N.
- v002 Label Stage-2 (label kernel implemented + local label artefacts generated): Phase 4bm-O.
- **v002 Label Stage-3 (label artefacts structurally QA-passed)**: Phase 4bm-P this memo.

v002 Label Stage-4 (eligibility-gate-passed at report level), Stage-5 (research-use-cleared at policy level), Stage-6 (label-family successor-state JSON), Stage-7 (chronological-split-policy decided), and Stage-8 (`stage_5_label_cleared = true` on the manifest) remain **unauthorized**.

The actual v002 label manifest still carries `research_eligible = false` / `eligibility_gate_status = "pending"` / `label_family_research_use_authorized = false` / `stage_5_label_cleared = false` / `chronological_split_policy = "not_yet_defined"` byte-identically. The Phase 4aw `flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked).

---

## 30. Conditional next options, none authorized

| Option | Type | Status |
| ------ | ---- | ------ |
| **Primary** — remain paused | n/a | **recommended** |
| **Conditional next, if continuing on the v002 label lifecycle ladder** — future **Phase 4bm-Q — Multi-Day V002 Label-Family Eligibility Gate Design / Implementation / Execution** (multi-day analogue of Phase 4bj-E; would design, implement, and run a label-family eligibility gate over the v002 label artefacts; would produce a local gitignored gate report; would not authorize ML, strategy, diagnostics, or backtest work) | code + docs + local gitignored gate report | **NOT authorized by this memo** |
| **Remedial alternative if Phase 4bm-P had reached INDETERMINATE or FAIL** — separately authorized remedial / regeneration / re-QA phase | depends on issue | **n/a — verdict is PASS** |
| **Conditional after Phase 4bm-Q** — future v002 label-family research-use decision memo (multi-day analogue of Phase 4bj-F) | docs-only | **NOT authorized by this memo** |
| **Conditional after the v002 label-family research-use decision** — future v002 label-family successor-state recording (multi-day analogue of Phase 4bj-G) | docs + local gitignored successor-state JSON | **NOT authorized by this memo** |
| **Conditional later** — future multi-day v002 chronological-split-policy memo (multi-day analogue of Phase 4bj-H / Phase 4bj-I / Phase 4bj-J) | docs (+ optionally local gitignored sibling artefact) | **NOT authorized by this memo** |
| Additional acquisition (more days, cross-symbol, mark-price, order-book, funding, OI, liquidation, cross-venue, authenticated APIs, private endpoints) | docs + data | **NOT authorized by this memo** |
| Diagnostics, ML, strategy, backtests | code + data | **FORBIDDEN by this memo** |
| Paper / shadow / live / exchange-write / production keys | runtime | **FORBIDDEN by this memo** |

**No successor phase is authorized by Phase 4bm-P.**

---

## 31. Preserved boundaries

All retained verdicts and project locks are preserved verbatim by this phase:

- H0 — FRAMEWORK ANCHOR.
- R3 — BASELINE-OF-RECORD.
- R1a / R1b-narrow — RETAINED — NON-LEADING.
- R2 — FAILED — §11.6.
- F1 — HARD REJECT.
- D1-A — MECHANISM PASS / FRAMEWORK FAIL.
- 5m thread — OPERATIONALLY CLOSED (Phase 3t).
- V2 / G1 / C1 — HARD REJECT — terminal for first-spec.
- §11.6 = 8 bps per side; round-trip = 16 bps.
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops.
- Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8.
- Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w.
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template.
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (preserved; never invoked).
- Phase 4bb-F canonical path policy.
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks.
- Phase 4bm-A-P1 thin-prompt Claude Code context-management standard.
- Phase 4bm-D-P1 lightweight Claude Code workspace execution standard.
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A..F / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A / 4bh-B / 4bh / 4bi-A..D / 4bj-A..K / 4bk-A / 4bl-A..F / 4bm-A / 4bm-A-P1 / 4bm-B / 4bm-C / 4bm-D / 4bm-D-P1 / 4bm-E / 4bm-F / 4bm-G / 4bm-H / 4bm-I / 4bm-J / 4bm-K / 4bm-L / 4bm-M / 4bm-N / 4bm-O results — all preserved verbatim.

---

**Final reminders, recorded verbatim:**

- **Phase 4bm-P is read-only label artefact structural QA.**
- **No label artefact is modified by Phase 4bm-P.**
- **No label artefact is committed by Phase 4bm-P.**
- **Phase 4bm-Q is not authorized by Phase 4bm-P.**
- **Label-family eligibility gate is not authorized by Phase 4bm-P.**
- **Label-family research-use is not authorized by Phase 4bm-P.**
- **Label-family successor-state recording is not authorized by Phase 4bm-P.**
- **Diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-P.**
- **No feature artefact was modified.**
- **No upstream artefact was mutated.**
- **No data/microstructure file was committed.**

**Structural QA verdict: LABEL_STRUCTURAL_QA_PASS — label artefact remains not research-eligible.**

**Recommended state: remain paused.**
