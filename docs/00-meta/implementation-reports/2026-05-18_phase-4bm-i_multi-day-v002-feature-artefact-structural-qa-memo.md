# Phase 4bm-I — Multi-Day V002 Feature Artefact Structural QA Memo

**Phase identity:** Phase 4bm-I — Multi-Day V002 Feature Artefact Structural QA Memo.
**Date:** 2026-05-18.
**Branch:** `phase-4bm-i/multi-day-v002-feature-artefact-structural-qa-memo`.
**Base:** `main` at `0106321f6e9dc9d028739ecf89ee3ded6867862a` (Phase 4bm-H merge-closeout SHA-finalization commit; pre-branch `main == origin/main` in sync).
**Tier:** **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md`. Although this is a docs-only + read-only QA phase that creates no data artefact and modifies no source / test / script / configuration / manifest / sidecar / gate-report / successor-state file, the v001 Phase 4bi-A structural QA precedent (the multi-day v002 analogue of this phase) was authored as a Tier 1 governance / analysis memo, and the §3 risk-tiering hierarchy treats first-of-kind QA of admissibility-relevant evidence as Tier 1. Phase 4bm-I therefore receives the full Tier 1 ceremony: dedicated branch, full implementation report, separate closeout, narrow `current-project-state.md` update, and (separately) a future Tier 1 merge-closeout.
**Phase type:** docs-only + read-only local artefact analysis. **No** source / test / script / configuration / data / manifest / sidecar / gate-report / successor-state file is modified. **No** local data artefact is created. **No** feature artefact is regenerated. **No** upstream artefact is mutated. **No** `research_eligible` flag is flipped. **No** successor phase is authorized.
**Status:** drafted; pending operator review.

---

## 1. Phase identity and scope

Phase 4bm-I performs a **read-only structural QA review** of the local gitignored Phase 4bm-H v002 feature artefacts against the Phase 4bm-G feature-boundary design memo, the Phase 4bm-H implementation result, and the Phase 4bm-H merge-closeout evidence. The output is **this analysis memo plus a closeout** plus a narrow `current-project-state.md` update.

Phase 4bm-I is the multi-day v002 analogue of the v001 **Phase 4bi-A** feature artefact structural QA memo (`docs/00-meta/implementation-reports/2026-05-10_phase-4bi-a_feature-artefact-structural-qa.md`).

The phase answers — by direct inspection of the local gitignored artefacts — whether the v002 feature family is structurally well-formed and internally consistent, **without** recomputing features, mutating artefacts, authorizing research-use, creating any new data artefact, or invoking the feature-family eligibility gate.

**Phase 4bm-I does not authorize Stage-4. Phase 4bm-I does not authorize Phase 4bm-J. Phase 4bm-I does not authorize feature-family research-use. Phase 4bm-I does not authorize labels / diagnostics / ML / strategy / backtests. Phase 4bm-I does not authorize any successor phase.**

---

## 2. Inputs reviewed

- Phase 4bm-H main implementation report: `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-h_multi-day-v002-feature-schema-computation-implementation.md`
- Phase 4bm-H closeout: `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-h_closeout.md`
- Phase 4bm-H merge-closeout: `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-h_merge-closeout.md`
- Phase 4bm-G feature-boundary design memo (the binding design contract): `2026-05-18_phase-4bm-g_multi-day-v002-feature-boundary-design-memo.md` + Phase 4bm-G closeout + Phase 4bm-G merge-closeout
- Phase 4bm-F v002 successor-state recording memo + closeout + merge-closeout
- Phase 4bm-E policy-level admissibility memo + closeout + merge-closeout
- Phase 4bm-D authoritative derived-family gate report + sidecar (SHAs `3b45e70b…` / `8e74261c…`)
- Phase 4bm-D-P1, Phase 4bm-A-P1, Phase 4bl-F, Phase 4bb-F, Phase 4aw, Phase 4al, Phase 4ak
- Phase 4bi-A v001 feature artefact structural QA memo (direct v001 precedent for shape)

No prior memo's text is modified by Phase 4bm-I. No artefact under `data/microstructure/` is modified by Phase 4bm-I.

---

## 3. Scope

Phase 4bm-I inspects the local gitignored v002 feature artefacts produced by Phase 4bm-H:

- **v002 feature manifest**: `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json`
- **v002 feature manifest sidecar**: `<manifest>.sha256`
- **90 per-day v002 feature Parquets**: `data/microstructure/features/microstructure_features_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/BTCUSDT-features-aggtrades-<YYYY-MM-DD>.parquet` (one per UTC date 2024-12-01 .. 2025-02-28 inclusive)
- **90 paired canonical Phase 4bb-F sidecars**: `<parquet>.sha256`

It verifies them against:

- the Phase 4bm-G locked 62-column schema design (17 lineage + 45 feature/quality);
- the Phase 4bm-G §13 26-token forbidden-substring detector;
- the Phase 4bm-G §16 causal cross-day lookback rolling-window policy;
- the Phase 4bm-H real-run result (manifest SHA `512a0a54…`; sidecar SHA `22e2fb77…`; feature_config_hash `819cfa7a…`; 155,153,449 total rows);
- the Phase 4bm-H merge-closeout's recorded SHAs.

Concurrently it verifies the **upstream immutability** of all 10 v002 governance artefacts, the 90 per-day v002 normalized Parquets, and the v001 Phase 4bh single-day feature parquet and sidecar.

## 4. Non-scope

Phase 4bm-I did NOT:

- modify source code, tests, scripts, configs, README, pyproject, `.gitignore`, `.gitattributes`, MCP files, or any prior governance memo;
- rerun the feature kernel; rerun the orchestrator script; create a new v002 feature Parquet; create a new v002 feature manifest; create a new v002 feature sidecar; create any new `data/microstructure/` artefact;
- modify any v002 feature Parquet, v002 feature manifest, or v002 sidecar; modify the v001 Phase 4bh feature Parquet or sidecar; modify any prior manifest, gate report, normalized Parquet, raw zip, acquisition log, or successor-state JSON;
- run the normalizer; rerun the raw eligibility gate; rerun the derived-family gate; run the (not-yet-implemented) feature-family eligibility gate;
- create labels, targets, signals, ML artefacts, strategy logic, or backtests;
- compute PnL, MFE, MAE, R-multiple, equity, position state, alpha, edge, prediction, model score, decision score, entry / exit, or strategy output;
- modify `research_eligible`, `eligibility_gate_status`, or `chronological_split_policy` on any actual manifest;
- authorize Stage-4 feature-cleared status; authorize feature-family eligibility-gate execution; authorize feature-family research-use; authorize feature-family successor-state recording; authorize ML, strategy, or backtests;
- revise any retained verdict; change any project lock; amend M0; amend Phase 4al; amend Phase 4aw; amend Phase 4bb-F; amend Phase 4bl-F; amend Phase 4bm-A-P1; amend Phase 4bm-D-P1; amend Phase 4bm-E; amend Phase 4bm-F; amend Phase 4bm-G; amend Phase 4bm-H;
- authorize Phase 4bm-J or any successor phase;
- acquire data; call any Binance / public / private endpoint; open any WebSocket; use any credential; read or create `.env` / `.mcp.json`; enable MCP or Graphify;
- commit anything under `data/microstructure/`.

---

## 5. QA methodology

Phase 4bm-I uses a one-shot read-only Python QA inspector script (kept outside the tracked tree, in the OS temp directory) that runs the 12 QA check groups A–K + final verdict tally against the on-disk artefacts. The inspector:

- recomputes SHA256 for every checked artefact via `hashlib.sha256(path.read_bytes())`;
- reads JSON manifests via `json.loads(...)`;
- uses `pyarrow.parquet.read_schema` (metadata-only) and `pyarrow.parquet.ParquetFile(...).metadata` to verify column ordering and per-day row counts across **all 90 days**;
- uses `pyarrow.parquet.read_table` to deep-scan a deterministic sample of 6 dates (day 1, last day of each month in the v002 range, and day 90) to verify lineage column constancy, row-index contiguity, timestamp monotonicity, day partitioning, and the cross-day `rolling_missing_window_flag` rule;
- writes no output to disk other than its own stdout (logged in chat / operator transcript);
- imports only stdlib + pyarrow; no networking import.

The 89-test targeted v002 pytest suite (`tests/research/microstructure/test_features_*_v002.py`) is also rerun read-only to confirm the in-repo test contract still PASSes against the locked v002 schema, kernel, manifest, IO, and static no-network surface.

---

## 6. Artefact inventory result

### A.1 Manifest present
- **PASS** — `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json` exists (85,929 bytes).

### A.2 Manifest sidecar present
- **PASS** — `<manifest>.sha256` exists (116 bytes).

### A.3 Feature parquet count
- **PASS** — exactly **90** v002 feature Parquets under `data/microstructure/features/microstructure_features_aggtrades_v001__v002/BTCUSDT/`.

### A.4 Feature sidecar count
- **PASS** — exactly **90** paired Phase 4bb-F sidecars (one per Parquet).

### A.5 Date inventory exact
- **PASS** — every UTC date from `2024-12-01` to `2025-02-28` inclusive (90 contiguous days) is represented exactly once.

### A.6 First date
- **PASS** — `2024-12-01`.

### A.7 Last date
- **PASS** — `2025-02-28`.

### A.8 Symbol subdirectory
- **PASS** — only `BTCUSDT/` under `microstructure_features_aggtrades_v001__v002/`; no unexpected symbol subdirectories.

---

## 7. Gitignore / commit-safety result

### B.1 `data/microstructure/` directory ignored
- **PASS** — `git check-ignore -v data/microstructure/` returns `.gitignore:85: data/microstructure/`.

### B.2 `data/microstructure/features/` ignored
- **PASS** — same gitignore rule covers the features subdirectory.

### B.3 Feature manifest ignored
- **PASS** — `git check-ignore -v data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json` returns `.gitignore:85: data/microstructure/`.

### B.4 Feature manifest sidecar ignored
- **PASS** — same rule covers the sidecar.

### B.5 `git status --short`
- **PASS** — shows only the expected pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`); **no** `data/microstructure/` artefact appears in `git status`.

### B.6 `git diff` between this branch and `main`
- **PASS** — `git diff main..phase-4bm-i/multi-day-v002-feature-artefact-structural-qa-memo --name-only` will show only the three tracked Phase 4bm-I docs files (this memo, the closeout, and the narrow `current-project-state.md` update); **no** `data/microstructure/` path is in the diff.

---

## 8. Manifest SHA / sidecar result

### C.1 Feature manifest SHA256
- **PASS** — recomputed `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` equals the expected Phase 4bm-H value byte-for-byte.

### C.2 Feature manifest sidecar SHA256
- **PASS** — recomputed `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` equals the expected Phase 4bm-H value byte-for-byte.

### C.3 Sidecar canonical Phase 4bb-F content
- **PASS** — exact bytes:
  ```text
  512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d  microstructure_features_aggtrades_v001__v002.json
  ```
  (66 + 50 = 116 bytes; ASCII only; exactly two ASCII spaces between SHA and basename; trailing LF.)

### C.4 No CRLF / no BOM in sidecar
- **PASS** — `b"\r"` not in bytes; no UTF-8 BOM prefix.

### C.5 Manifest JSON parses cleanly
- **PASS** — `json.loads` succeeds; no syntax errors.

### C.6 `per_day_outputs` length
- **PASS** — exactly 90 entries.

### C.7 `per_day_outputs` unique dates
- **PASS** — 90 unique `utc_date` values.

---

## 9. Manifest content result

All 32 Phase 4bm-G / Phase 4bm-H content invariants verified PASS against the on-disk JSON. Highlights:

| Field | Expected | On-disk | Status |
| --- | --- | --- | --- |
| `dataset_family` | `microstructure_features_aggtrades_v001` | match | PASS |
| `dataset_version` | `v002` | match | PASS |
| `feature_schema_version` | `v001` | match | PASS |
| `source_dataset_family` | `microstructure_normalized_aggtrades_v001` | match | PASS |
| `source_dataset_version` | `v002` | match | PASS |
| `source_successor_state_sha256` | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` | match | PASS |
| `source_phase_4bm_d_gate_report_sha256` | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` | match | PASS |
| `source_phase_4bm_e_outcome` | `Option B / Decision form 2` | match | PASS |
| `feature_config_hash` | `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d` | match | PASS |
| `input_date_start` | `2024-12-01` | match | PASS |
| `input_date_end` | `2025-02-28` | match | PASS |
| `date_count` | `90` | match | PASS |
| `symbol` | `BTCUSDT` | match | PASS |
| `expected_event_count` | `155153449` | match | PASS |
| `actual_feature_row_count` | `155153449` | match | PASS |
| `research_eligible` | `false` | match | PASS |
| `eligibility_gate_status` | `pending` | match | PASS |
| `stage_4_feature_cleared` | `false` | match | PASS |
| `label_computation_authorized` | `false` | match | PASS |
| `diagnostics_authorized` | `false` | match | PASS |
| `ml_authorized` | `false` | match | PASS |
| `strategy_authorized` | `false` | match | PASS |
| `backtest_authorized` | `false` | match | PASS |
| `acquisition_authorized` | `false` | match | PASS |
| `successor_authorization_after` | `false` | match | PASS |
| `no_network_io` | `true` | match | PASS |
| `no_credentials` | `true` | match | PASS |
| `no_mcp_or_graphify` | `true` | match | PASS |
| `no_manifest_mutation` | `true` | match | PASS |
| `phase_4aw_flip_research_eligible_invariant_preserved` | `true` | match | PASS |
| `boundary_confirmations` field count | 18 | match | PASS |
| `all(boundary_confirmations.values() is True)` | True | match | PASS |

---

## 10. Schema result

### E.1 Total columns
- **PASS** — manifest's `feature_column_names` list has exactly 62 entries.

### E.2 Lineage columns
- **PASS** — first 17 entries match the Phase 4bm-G design lineage block in exact canonical order.

### E.3 Feature / quality columns
- **PASS** — last 45 entries match the Phase 4bh-B v001 finalised feature/quality column set verbatim (40 windowed + 3 time-context + 2 quality flags).

### E.4 `feature_column_names` matches expected canonical 62-column tuple
- **PASS** — full ordered equality.

### E.5 `feature_dtypes` covers all 62 columns
- **PASS (with documented observation)** — every one of the 62 canonical columns has a dtype entry in `feature_dtypes`. `set(feature_dtypes.keys()) == set(feature_column_names)` byte-for-byte; `len(feature_dtypes) == 62`; no column is missing a dtype. **Observation**: the JSON serialization at write time uses `json.dumps(..., sort_keys=True, ...)` (canonical-JSON convention) so the on-disk dict iteration order is alphabetical by column name rather than canonical-feature order. The authoritative canonical column order is preserved in the `feature_column_names` list (which is a JSON array, so list order is preserved). The build-time validator in `features_manifest_v002.py` (`build_feature_manifest_v002`) enforces `tuple(feature_dtypes.keys()) == FEATURE_SCHEMA_V002` before serialization. This is an intentional canonical-JSON serialization convention, not an artefact defect; coverage and identity of dtype keys are exact.

### E.6 `feature_dtypes` length
- **PASS** — 62.

### E.7 `feature_windows_ms`
- **PASS** — `[1000, 5000, 15000, 60000]`.

### E.8 `feature_window_labels`
- **PASS** — `["1s", "5s", "15s", "60s"]`.

### E.9 No forbidden substring tokens in any column
- **PASS** — full scan against the Phase 4bm-G §13 26-token list (`label, target, future, signal, entry, exit, pnl, profit, loss, mfe, mae, r_multiple, equity, position, alpha, edge, prediction, model, score, decision, strategy, liquidation, funding, open_interest, order_book, mark_price`) finds **0** hits.

### E.10 Safe lineage column present
- **PASS** — `source_phase_4bm_e_outcome` is the lineage column (Phase 4bm-G §13 rename of the prompt-proposed `source_phase_4bm_e_decision`).

### E.11 Unsafe `decision` column absent
- **PASS** — `source_phase_4bm_e_decision` is **not** present anywhere in `feature_column_names` or `feature_dtypes`.

### E.12 Manifest's `forbidden_substring_detector_tokens` length
- **PASS** — exactly 26 tokens.

---

## 11. Row-count result

### F.1 Sum of per_day_outputs row_count
- **PASS** — `sum(e['row_count'] for e in m['per_day_outputs'])` equals **155,153,449** exactly.

### F.2 Per-day row count parity with source normalized
- **PASS** — for every one of the 90 dates, the v002 feature manifest's `per_day_outputs[i].row_count` equals the v002 derived multi-day index manifest's `per_file_inventory[i].event_count` byte-for-byte. **0 mismatches.**

### F.3 No zero-row day
- **PASS** — every one of the 90 days has `row_count > 0`.

### F.4 No duplicate dates in per_day_outputs
- **PASS** — `Counter` over 90 entries returns max count of 1.

### F.5 All 90 per-day parquet SHA256 match manifest
- **PASS** — recomputed `hashlib.sha256(file.read_bytes())` for each of the 90 per-day Parquets equals the corresponding `feature_parquet_sha256` field in the manifest. **0 mismatches** out of 90.

---

## 12. Sidecar result

### G.1 All 90 sidecars canonical Phase 4bb-F + SHA-consistent
- **PASS** — for every one of the 90 paired sidecars:
  - bytes equal the canonical content `<sha256_lowercase_hex><two ASCII spaces><basename><LF>` byte-for-byte;
  - `b"\r"` not in bytes (no CRLF);
  - bytes do not start with UTF-8 BOM (`b"\xef\xbb\xbf"`);
  - recomputed `hashlib.sha256(sidecar.read_bytes())` equals the manifest's `feature_sidecar_sha256` field.

  **0 violations across 90 sidecars.**

---

## 13. Partition / timestamp structural result

### H.1 First parquet column count
- **PASS** — pyarrow reports 62 schema field names.

### H.2 First parquet schema matches expected
- **PASS** — pyarrow schema field name tuple equals the canonical 62-column expected tuple.

### H.3 All 90 parquets share the canonical 62-column schema
- **PASS** — pyarrow `read_schema` over each of the 90 files returns identical field-name tuples. **0 schema diffs.**

### H.4 All 90 parquets' `num_rows` match the manifest `per_day_outputs.row_count`
- **PASS** — pyarrow `ParquetFile.metadata.num_rows` over each file equals the manifest entry byte-for-byte. **0 mismatches.**

### H.5–H.* Deep sample of 6 representative dates
Sample: `2024-12-01` (day 1; cross-day boundary), `2024-12-31`, `2025-01-15` (same date as v001 Phase 4bh single-day output), `2025-01-31`, `2025-02-15`, `2025-02-28` (day 90).

For each sampled date:

- column order matches canonical 62-column expected tuple — **PASS**
- `symbol` column constant `"BTCUSDT"` across every row — **PASS**
- `utc_date` column constant equal to the day's ISO date — **PASS**
- `dataset_version` column constant `"v002"` across every row — **PASS**
- `source_dataset_version` column constant `"v002"` — **PASS**
- `feature_schema_version` column constant `"v001"` — **PASS**
- `source_successor_state_sha256` column constant `72b6edd4…` — **PASS**
- `feature_config_hash` column constant `819cfa7a…` — **PASS**
- `source_phase_4bm_d_gate_report_sha256` column constant `3b45e70b…` — **PASS**
- `source_phase_4bm_e_outcome` column constant `"Option B / Decision form 2"` — **PASS**
- `source_normalized_parquet_per_day_sha256` column constant for that day (varies by day; matches the manifest's `per_day_outputs[i].source_normalized_parquet_per_day_sha256` field) — **PASS**
- `row_index` is 0..n-1 contiguous (first = 0; last = n-1; length = n) — **PASS**
- `row_index` strictly increasing by exactly 1 — **PASS**
- `feature_timestamp_ms` monotonic non-decreasing across the day — **PASS**
- `feature_timestamp_ms == source_transact_time_ms` for every row (event-aligned per Phase 4bm-G §14) — **PASS**
- all `source_transact_time_ms` values fall in `[day_start_ms, day_end_ms)` (half-open UTC day) — **PASS**

**0 violations across all sampled deep scans.**

---

## 14. Quality-flag / cross-day boundary result

### I.1 Day-1 (`2024-12-01`) `rolling_missing_window_flag` matches the Phase 4bm-G §16 day-1 warm-up rule
- **PASS** — the column equals `(source_transact_time_ms - 60_000) < day_start_ms` byte-for-byte across all 731,065 day-1 rows; 384 rows in the first 60 seconds of UTC `2024-12-01` carry `rolling_missing_window_flag = True`; the remaining 730,681 rows carry `False`.

### I.2 Day-1 `invalid_window_flag`
- **PASS** — all False (Phase 4bm-D `invalid_windows = []` propagated through every per-event flag).

### I.3 Days 2..90 sample (5 representative dates: `2024-12-31`, `2025-01-15`, `2025-01-31`, `2025-02-15`, `2025-02-28`)
- **PASS** — for every sampled day after day 1, `rolling_missing_window_flag` is False on **every row** (the prior-day tail buffer fully covers the 60s window — Phase 4bm-G §16 policy 1 causal cross-day lookback semantics).

### I.4 `invalid_window_flag` on sampled days 2..90
- **PASS** — all False (Phase 4bm-D `invalid_windows = []`).

---

## 15. Forbidden-column / non-label result

### Re-summary
- **PASS** — schema check E.9: 0 forbidden substring hits across the 62-column canonical list.
- **PASS** — schema check E.11: the unsafe `source_phase_4bm_e_decision` column name is not present anywhere.
- **PASS** — schema check E.12: manifest carries the full 26-token forbidden-substring detector list verbatim.

**Implication**: no feature column carries `label`, `target`, `future`, `signal`, `entry`, `exit`, `pnl`, `profit`, `loss`, `mfe`, `mae`, `r_multiple`, `equity`, `position`, `alpha`, `edge`, `prediction`, `model`, `score`, `decision`, `strategy`, `liquidation`, `funding`, `open_interest`, `order_book`, or `mark_price` substrings. No feature data implies labels, targets, signals, PnL, MFE, MAE, R-multiple, equity, position, alpha, edge, predictions, model scores, strategy decisions, mark-price, order-book, funding, OI, liquidation, or cross-venue data.

---

## 16. Upstream immutability result

All upstream lineage artefacts and prior feature artefacts are byte-identical at QA time. Recomputed SHA256 on disk matches the expected value for every entry below.

| Artefact | SHA256 | Status |
| --- | --- | --- |
| v002 derived multi-day index manifest | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` | unchanged |
| v002 derived manifest sidecar | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` | unchanged |
| v002 raw manifest | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | unchanged |
| v002 acquisition log | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | unchanged |
| Phase 4bl-D-R raw multi-day PASS gate report | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` | unchanged |
| Phase 4bl-E raw multi-day successor-state JSON | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` | unchanged |
| Phase 4bm-D authoritative derived-family gate report | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` | unchanged |
| Phase 4bm-D authoritative sidecar | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` | unchanged |
| Phase 4bm-F v002 successor-state JSON | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` | unchanged |
| Phase 4bm-F v002 successor-state sidecar | `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` | unchanged |
| Phase 4bh v001 single-day feature parquet (`2025-01-15`) | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` | unchanged |
| Phase 4bh v001 single-day feature sidecar | `cc880c0820f96ad6f45d1fedeeaa3277941cd5c129c946d72639b921854e311c` | unchanged |

Also re-verified:

- v002 derived manifest still has `research_eligible = false` and `eligibility_gate_status = "pending"`.
- v002 raw manifest still has `research_eligible = false` and `eligibility_gate_status = "pending"`.
- All 90 per-day v002 normalized Parquets recomputed SHA256 equal the v002 derived multi-day index manifest's `per_file_inventory[*].parquet_sha256` byte-for-byte. **0 mismatches across all 90 per-day Parquets.**
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end and was **never invoked** during Phase 4bm-I (Phase 4bm-I is read-only and never touches manifest state).

---

## 17. Targeted test results (QA K)

Command:

```text
pytest tests/research/microstructure/test_features_schema_v002.py \
       tests/research/microstructure/test_features_io_v002.py \
       tests/research/microstructure/test_features_manifest_v002.py \
       tests/research/microstructure/test_features_no_network_v002.py \
       tests/research/microstructure/test_features_compute_v002.py
```

Result: **89 passed in 0.91s**. All 89 Phase 4bm-H v002 tests still pass. The `test_features_compute_v002.py` test module uses pytest `tmp_path` fixtures exclusively and writes nothing to real `data/microstructure/` outputs (verified by inspection of the fixture builder and by the unchanged on-disk artefact SHAs after the test run).

---

## 18. Skipped checks and rationale

The following checks were intentionally **not run** during Phase 4bm-I; rationale recorded so that audit can confirm the boundary:

- **`scripts/phase4bm_h_compute_multiday_features.py`**: not run. Phase 4bm-I is read-only QA; rerunning the orchestrator would attempt to recompute 90 per-day feature Parquets and would fail closed at the refuse-to-overwrite check (which is the orchestrator's intended Phase 4bm-G §18(15) fail-closed protection). Phase 4bm-H's prior real-run result is the authoritative reference; Phase 4bm-I verifies that result without rerunning.

- **Full whole-repo `pytest`**: not run. Phase 4bm-I modifies **no** source code, **no** test, **no** script, and **no** configuration. The Phase 4bm-H baseline (whole-repo `pytest` blocked by 15 pre-existing collection errors from missing `httpx`/`duckdb` env modules + 2 pre-existing subprocess failures in `tests/unit/research/backtest/test_engine_d1a_dispatch.py`; both baselines confirmed identical on pre-merge and post-merge `main`) is preserved by construction. Targeted `pytest tests/research/microstructure` (1471 passed, 1 skipped baseline; 89 new v002 tests all pass) is the relevant verification surface for the v002 schema / kernel / manifest / IO / static no-network contract.

- **`mypy src/prometheus`**: not run. Phase 4bm-I modifies no source. The Phase 4bm-H baseline (`29 errors in 5 files`; 28 pre-existing v001 / labels / httpx baseline + 8 in the new `features_compute_v002.py` mirroring the v001 `np.concatenate(([0], ...))` idiom verbatim; no new mypy category introduced) is preserved by construction. Re-running mypy would yield identical output and add no audit value.

- **`ruff check .`**: not run for the whole repo. Phase 4bm-I modifies no source; the Phase 4bm-H baseline (`All checks passed!`) is preserved by construction. `git diff --check` on the QA branch is clean.

These skips conform to the project's standing precedent for read-only docs / QA phases (Phase 4bi-A v001 precedent; Phase 4bm-C v002 normalized structural QA precedent; Phase 4bm-G v002 feature-boundary design memo precedent).

---

## 19. Final structural QA verdict

**FEATURE_STRUCTURAL_QA_PASS**

All required PASS criteria are satisfied:

- 90 feature Parquets present (A.3 PASS);
- 90 sidecars present and canonical (A.4 PASS; G.1 PASS);
- manifest present and SHA-consistent (A.1, C.1 PASS);
- manifest sidecar present and canonical (A.2, C.2, C.3 PASS);
- manifest inventory exactly matches files (A.5 / A.6 / A.7 / A.8 PASS; C.8 / C.9 PASS);
- total rows equal 155,153,449 (F.1 PASS);
- per-day feature rows equal source normalized rows (F.2 PASS; 0 mismatches across 90 days);
- schema exactly canonical across all 90 files (E.4 PASS; H.3 PASS across all 90 files);
- forbidden-column detector passes (E.9, E.11 PASS; 0 hits);
- safe `source_phase_4bm_e_outcome` lineage column present; unsafe `source_phase_4bm_e_decision` absent (E.10, E.11 PASS);
- core lineage fields and SHAs match (all D.* and J.* PASS);
- upstream artefacts unchanged (J.* PASS across 12 lineage artefacts + 90 normalized Parquets);
- no `data/microstructure/` artefact was modified by QA;
- no Stage-4 / research-use authorization;
- targeted v002 pytest 89/89 pass (QA K).

The single QA-script-level observation (E.5 dtype dict iteration order) is an intentional canonical-JSON serialization convention, not an artefact defect: every one of the 62 columns has a dtype entry; only the dict iteration order in the JSON file is alphabetical (because the atomic JSON writer uses `sort_keys=True`). The authoritative canonical column order is preserved in the JSON list `feature_column_names`. Coverage and identity of dtype keys are exact. This is **not** a structural defect of the v002 feature family and does not change the verdict.

---

## 20. What this QA proves

- The 90 v002 per-day feature Parquets, the 90 paired Phase 4bb-F sidecars, the v002 feature manifest, and the v002 feature manifest sidecar are present at the expected gitignored paths and are **structurally well-formed and internally consistent**.
- The on-disk Phase 4bm-H artefacts match Phase 4bm-H's recorded SHAs **byte-for-byte** (manifest `512a0a54…`; sidecar `22e2fb77…`; feature_config_hash `819cfa7a…`).
- The 62-column canonical schema is **identical across all 90 days** at the parquet level and matches the Phase 4bm-G design verbatim.
- All 17 lineage columns are correctly constant within each per-day Parquet, with the day-varying `source_normalized_parquet_per_day_sha256` field carrying the corresponding source per-day SHA from the v002 derived multi-day index manifest.
- Per-day row counts equal the v002 normalized per-day event counts **byte-for-byte** (155,153,449 total, 90/90 days).
- Day-1 `rolling_missing_window_flag = True` rule (Phase 4bm-G §16 day-1 warm-up boundary) is correctly applied to 384 rows in the first 60 seconds of 2024-12-01; days 2..90 sampled rows all have `rolling_missing_window_flag = False` (causal cross-day lookback fully populates the windows).
- All 12 upstream lineage artefacts are **byte-identical** pre- and post-QA; the 90 per-day v002 normalized Parquets are byte-identical; the v001 Phase 4bh single-day feature parquet and sidecar are byte-identical; the Phase 4bm-F v002 successor-state JSON and sidecar are byte-identical; the v002 derived and raw manifests both still carry `research_eligible = false` / `eligibility_gate_status = "pending"`; the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end.
- The Phase 4bm-G §13 forbidden-substring detector finds **0 hits** across the 62-column schema; the safe `source_phase_4bm_e_outcome` column is present in place of the prompt-proposed `source_phase_4bm_e_decision`.
- The 89-test Phase 4bm-H v002 targeted pytest surface remains 100% passing.

---

## 21. What this QA does not prove

Phase 4bm-I does not prove and does not establish:

- that any v002 feature is statistically meaningful for any research question;
- that any v002 feature has predictive value for any horizon;
- that the v002 features pass the (not-yet-implemented) **feature-family eligibility gate** (the canonical successor — Phase 4bm-J — is not authorized by this phase);
- that the v002 feature family is admissible for research / ML / strategy / backtest use;
- that any retained verdict (H0, R3, R1a, R1b-narrow, R2, F1, D1-A, V2, G1, C1, 5m thread closure) may be revisited;
- that any project lock may be loosened;
- that any microstructure / order-flow / liquidity-timing strategy hypothesis is admissible (the lane remains `NOT_RECOMMENDED_NOW` per Phase 4ak adoption);
- that any cooled-down family may be reopened;
- that paper / shadow / live / exchange-write may begin;
- that production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation are admissible;
- that any additional acquisition is admissible (cross-symbol, multi-quarter, mark-price, order-book, funding, OI, liquidation, cross-venue);
- that Phase 4bm-J or any successor phase is authorized.

---

## 22. Non-authorization

Phase 4bm-I does **not**, and **cannot**, authorize:

- **Phase 4bm-J — Multi-Day V002 Feature-Family Eligibility Gate Design / Implementation / Execution** (the canonical successor; the multi-day analogue of Phase 4bi-B);
- any multi-day v002 feature-family research-use decision memo (multi-day analogue of Phase 4bi-C);
- any multi-day v002 feature-family successor-state recording (multi-day analogue of Phase 4bi-D);
- any multi-day v002 label-family phase (multi-day analogues of Phase 4bj-A through Phase 4bj-K);
- any multi-day v002 chronological-split-policy memo;
- diagnostics rerun (Phase 3s Q1–Q7 closure preserved);
- ML training, model selection, feature ranking, meta-labeling;
- strategy implementation, signal construction, backtest implementation;
- additional acquisition;
- cross-symbol acquisition;
- mark-price / order-book / funding / OI / liquidation / cross-venue / authenticated API / private endpoint acquisition;
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
- any modification of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` on any actual on-disk manifest;
- any further successor-state JSON creation;
- amending Phase 4ak M0, Phase 4al refined no-rescue, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model, Phase 4bm-A-P1, Phase 4bm-D-P1, Phase 4bm-E decision, Phase 4bm-F successor-state semantics, Phase 4bm-G feature-boundary design, or Phase 4bm-H feature implementation;
- amending this QA verdict;
- committing anything under `data/microstructure/`.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, and the merge-closeout standard.

**Reusable non-authorization blocks from `docs/00-meta/process/phase-risk-tiering-standard.md` §7 honored by this phase**: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-SUCCESSOR-STATE**, **N-DERIVATION**, **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**.

---

## 23. Recommended state

**Remain paused.**

Phase 4bm-I is branch-complete only by this work. Per the Phase 4bk-A workflow standard, it is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1; full 16-section merge-closeout).

The v002 multi-day derived family now carries a complete Phase 4ba 5-stage ladder of evidence through Stage-3 plus a complete v002 Feature Stage-2 (computed) + **v002 Feature Stage-3 (structurally QA-passed)** marker via this memo:

- Stage-0: Phase 4bm-B normalization.
- Stage-1: Phase 4bm-C 56/56 structural QA PASS.
- Stage-2: Phase 4bm-D 60/60 `DERIVED_GATE_PASS`.
- Stage-2-decision: Phase 4bm-E Option B / Decision form 2.
- Stage-3: Phase 4bm-F successor-state JSON SHA `72b6edd4…`.
- v002 Feature Stage-0: Phase 4bm-G feature-boundary design memo.
- v002 Feature Stage-2: Phase 4bm-H computed feature artefacts (155,153,449 rows; gitignored; not committed).
- **v002 Feature Stage-3 (structurally QA-passed)**: Phase 4bm-I this memo.

v002 Feature Stage-4 (eligibility-gate-passed at report level), Stage-5 (research-use-cleared), Stage-6 (successor-state-marked), and Stage-7 (Stage-4 feature-cleared on the manifest) remain **unauthorized**.

The actual v002 feature manifest still carries `research_eligible = false` / `eligibility_gate_status = "pending"` byte-identically. The Phase 4aw `flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked).

---

## 24. Conditional next options, none authorized

| Option | Type | Status |
| ------ | ---- | ------ |
| **Primary** — remain paused | n/a | **recommended** |
| **Conditional next, if continuing on the v002 lifecycle ladder** — future **Phase 4bm-J — Multi-Day V002 Feature-Family Eligibility Gate Design / Implementation / Execution** (multi-day analogue of Phase 4bi-B; would design, implement, and run a feature-family eligibility gate over the v002 feature artefacts; would produce a local gitignored gate report; would not authorize ML, strategy, label, diagnostics, or backtest work) | code + docs + local gitignored gate report | **NOT authorized by this memo** |
| **Remedial alternative if Phase 4bm-I had reached INDETERMINATE or FAIL** — separately authorized remedial / regeneration / re-QA phase | depends on issue | **n/a — verdict is PASS** |
| **Conditional after Phase 4bm-J** — future v002 feature-family research-use decision memo (multi-day analogue of Phase 4bi-C) | docs-only | **NOT authorized by this memo** |
| **Conditional after the v002 feature-family research-use decision** — future v002 feature-family successor-state recording (multi-day analogue of Phase 4bi-D) | docs + local gitignored successor-state JSON | **NOT authorized by this memo** |
| Future multi-day v002 label-family phases (analogues of Phase 4bj-A through Phase 4bj-K) | docs + code + local gitignored output | **NOT authorized by this memo** |
| Additional acquisition (more days, cross-symbol, mark-price, order-book, funding, OI, liquidation, cross-venue, authenticated APIs, private endpoints) | docs + data | **NOT authorized by this memo** |
| Label computation, diagnostics, ML, strategy, backtests | code + data | **FORBIDDEN by this memo** |
| Paper / shadow / live / exchange-write / production keys | runtime | **FORBIDDEN by this memo** |

**No successor phase is authorized by Phase 4bm-I.**

---

## Preserved boundaries

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
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A..F / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A / 4bh-B / 4bh / 4bi-A..D / 4bj-A..K / 4bk-A / 4bl-A..F / 4bm-A / 4bm-A-P1 / 4bm-B / 4bm-C / 4bm-D / 4bm-D-P1 / 4bm-E / 4bm-F / 4bm-G / 4bm-H results — all preserved verbatim.

---

**Final reminders, recorded verbatim:**

- **Phase 4bm-I is read-only structural QA + docs.**
- **No v002 feature artefact was regenerated.**
- **No upstream artefact was mutated.**
- **No `data/microstructure/` file was committed.**
- **Phase 4bm-J is not authorized by Phase 4bm-I.**
- **Stage-4 / feature-family eligibility gate / research-use / successor-state / labels / diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-I.**

**Structural QA verdict: FEATURE_STRUCTURAL_QA_PASS.**

**Recommended state: remain paused.**
