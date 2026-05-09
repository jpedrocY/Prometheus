# Phase 4be — AggTrades Normalized Dataset Structural QA Memo

**Phase identity:** Phase 4be — AggTrades Normalized Dataset Structural QA Memo.
**Type:** docs-and-local-gitignored-output inspection / structural QA memo.
**Date:** 2026-05-07.
**Branch:** `phase-4be/aggtrades-normalized-structural-qa`.
**Status:** drafted; pending operator review.

---

## 1. Phase header

Phase 4be is a structural QA inspection of the Phase 4bd Stage-0 derived normalization artefacts. It is **inspection-only**. It does not modify source code, tests, scripts, raw artefacts, normalized artefacts, manifests, gate reports, project locks, retained verdicts, or M0. It does not run the normalizer, regenerate any artefact, compute features, train ML, create strategies, run backtests, acquire data, or authorize any successor.

Core question: did the Phase 4bd Stage-0 normalized artefacts preserve the Phase 4az raw aggTrades data correctly, without introducing features, labels, signals, row loss, row duplication, timestamp drift, precision loss, manifest lineage errors, or eligibility-state changes?

**Answer:** yes. All 60 structural QA checks PASS.

---

## 2. Current state

| Item | Value |
| ---- | ----- |
| `main` HEAD | `e1734485b82c080f7ff1805ee20b0431bb3144e4` |
| `origin/main` HEAD | `e1734485b82c080f7ff1805ee20b0431bb3144e4` |
| Local / origin sync | in sync |
| Phase 4bd merge commit (ancestor verified) | `d4a68940a126eef4388bee960496c4ae2275b04e` |
| Phase 4bd merge-closeout file | `docs/00-meta/implementation-reports/2026-05-07_phase-4bd_merge-closeout.md` (present on `main`) |
| `data/microstructure/` gitignored | yes (`.gitignore:85`) |
| `data/microstructure/normalized/` gitignored | yes (`.gitignore:85`) |
| pyarrow available | yes (23.0.1) |

---

## 3. Inputs reviewed

- Phase 4bd normalized Parquet (`data/microstructure/normalized/microstructure_normalized_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet`) and paired `.sha256` sidecar.
- Phase 4bd derived manifest (`data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json`) and paired `.sha256` sidecar.
- Phase 4az raw manifest (`data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json`).
- Phase 4az raw zip + sidecar (read-only; for SHA confirmation).
- Phase 4az acquisition log (read-only; for SHA confirmation).
- Phase 4bb-D PASS gate report (read-only; for SHA + ID confirmation).

No live endpoints, credentials, `.env`, `.mcp.json`, MCP, Graphify, or external services were consulted.

---

## 4. Scope

Inspection-only structural QA covering:

- Stage-0 derived artefact existence and SHA confirmation;
- Parquet schema parity vs the Phase 4bc 19-column canonical order;
- row-count / row-index / aggregate-trade-id integrity;
- first / last row spot-check vs Phase 4bb-A QA values;
- timestamp-boundary and half-open UTC-day enforcement;
- precision / type policy (string-Decimal price/quantity; int64 IDs and timestamps; strict bool `is_buyer_maker`);
- per-row lineage column constancy;
- derived manifest field parity;
- raw artefact immutability;
- gitignored-output discipline.

---

## 5. Non-scope

Phase 4be did NOT:

- modify source code, tests, scripts, configs, README, pyproject, `.gitignore`, MCP files, governance files;
- run the normalizer or regenerate any normalized artefact;
- rerun the Phase 4bb-D gate or generate a new gate report;
- create or modify any file under `data/microstructure/`;
- create JSONL, DuckDB, feature, label, signal, proxy, ML, or strategy artefacts;
- acquire data; call Binance APIs / public endpoints / private endpoints; open WebSockets; use credentials, `.env`, or `.mcp.json`;
- compute features, returns, alpha, edge, opportunity rate, taker imbalance, sweep detection, aggressive-flow score, spread, depth, liquidity, slippage, order-flow, execution-quality proxies, regime, momentum, volatility, PnL, MFE, MAE, R-multiple, equity, or position-state columns;
- flip `research_eligible`, transition `eligibility_gate_status`, or authorize Stage-2 / Stage-3 / Stage-4 transition;
- authorize Phase 4bf, Phase 4bg, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation;
- revise retained verdicts, change project locks, or amend M0;
- commit anything under `data/microstructure/`.

---

## 6. Phase 4bd Stage-0 dependency

Phase 4be depends entirely on the Phase 4bd Stage-0 derived artefacts:

- Phase 4bd normalized Parquet SHA256: `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa`.
- Phase 4bd derived manifest SHA256: `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9`.
- Phase 4bd recorded `overall_status=pass`, 27 / 27 validation PASS, `event_count=1681098`, `invalid_window_candidates=0`, `research_eligible_after=False`, `no_successor_authorization=True`.
- Phase 4bd derived manifest defaults: `research_eligible=false`, `eligibility_gate_status=pending`, `feature_computation=forbidden`, `strategy_use=forbidden`.

Phase 4be neither modifies nor regenerates these artefacts.

---

## 7. Inspection method

Structural QA was performed via inline Python (transient; not committed) using:

- stdlib `hashlib`, `json`, `pathlib`;
- `numpy` for row-index contiguity and aggregate-trade-id uniqueness / monotonicity;
- `pyarrow.parquet` for schema and column reads.

The inspection script was discarded after running. No script under `scripts/` was added. No file under `data/microstructure/` was created or modified.

---

## 8. Local artefacts inspected

```text
data/microstructure/normalized/microstructure_normalized_aggtrades_v001/
    BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet
    BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet.sha256
data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json
data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json.sha256
data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json                 (read-only)
data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001_acquisition_log.json (read-only)
data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/
    BTCUSDT-aggTrades-2025-01-15.zip                                                        (read-only)
    BTCUSDT-aggTrades-2025-01-15.zip.sha256                                                 (read-only)
data/microstructure/gate-reports/gate-reports/
    microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json               (read-only)
```

---

## 9. Structural QA checklist and results — 60 / 60 PASS

| ID | Check | Result | Evidence |
| -- | ----- | :----: | -------- |
| 1 | Normalized Parquet exists at expected path | PASS | path verified |
| 2 | Normalized Parquet SHA256 matches recorded value | PASS | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| 3 | Parquet sidecar exists and matches Parquet SHA | PASS | sidecar first-64 hex == recomputed Parquet SHA |
| 4 | Derived manifest exists at expected path | PASS | path verified |
| 5 | Derived manifest SHA256 matches recorded value | PASS | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| 6 | Derived manifest sidecar exists and matches manifest SHA | PASS | sidecar first-64 hex == recomputed manifest SHA |
| 7 | Parquet schema = 19 Phase 4bc columns in canonical order | PASS | exact tuple match |
| 8 | No extra columns | PASS | `len(schema) == 19` |
| 9 | No feature/label/signal/proxy/ML/strategy columns | PASS | substring scan over schema names found 0 forbidden tokens |
| 10 | Parquet row count = 1,681,098 | PASS | `num_rows = 1681098` |
| 11 | Derived manifest `event_count` = 1,681,098 | PASS | `event_count = 1681098` |
| 12 | Parquet row count = derived manifest event_count | PASS | equal |
| 13 | `row_index` is contiguous 0..1,681,097 | PASS | `np.array_equal(row_index, arange(N))` |
| 14 | `row_index` has no duplicates | PASS | `len(unique) == N` |
| 15 | `agg_trade_id` has no duplicates | PASS | `unique_agg = 1681098` |
| 16 | `agg_trade_id` is non-decreasing | PASS | `all(ati[1:] >= ati[:-1])` |
| 17 | First row matches recorded raw first values | PASS | `agg_trade_id=2516301323` / `T=1736899205109` / `price='96514.9'` / `quantity='0.091'` / `is_buyer_maker=True` / `row_index=0` |
| 18 | Last row matches recorded raw last values | PASS | `agg_trade_id=2517982420` / `T=1736985599991` / `price='100460.0'` / `quantity='0.059'` / `is_buyer_maker=True` / `row_index=1681097` |
| 19 | First `transact_time_ms` = raw manifest `start_time_ms` | PASS | both = 1736899205109 |
| 20 | Last `transact_time_ms` = raw manifest `end_time_ms` | PASS | both = 1736985599991 |
| 21 | All `transact_time_ms` ∈ [`2025-01-15T00:00:00.000Z`, `2025-01-16T00:00:00.000Z`) | PASS | `min=1736899205109`, `max=1736985599991` |
| 22 | `price` stored as string / Decimal-parsable | PASS | `pyarrow type = string` |
| 23 | `quantity` stored as string / Decimal-parsable | PASS | `pyarrow type = string` |
| 24 | `is_buyer_maker` strict boolean | PASS | `pyarrow type = bool` |
| 25 | `source_file_sha256` constant = raw zip SHA | PASS | `unique=1`, value = `f560c2e5...` |
| 26 | `source_manifest_sha256` constant = raw manifest SHA | PASS | `unique=1`, value = `a371edd4...` |
| 27 | `source_gate_report_id` constant = expected ID | PASS | `unique=1`, value = `microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c` |
| 28 | `source_gate_report_sha256` constant = `96f09159...` | PASS | `unique=1` |
| 29 | `dataset_family` constant = `microstructure_normalized_aggtrades_v001` | PASS | `unique=1` |
| 30 | `dataset_version` constant = `v001` | PASS | `unique=1` |
| 31 | `source_dataset_family` constant = `microstructure_raw_aggtrades_v001` | PASS | `unique=1` |
| 32 | `source_dataset_version` constant = `v001` | PASS | `unique=1` |
| 33 | `symbol` constant = `BTCUSDT` | PASS | `unique=1` |
| 34 | `utc_date` constant = `2025-01-15` | PASS | `unique=1` |
| 35 | `normalization_schema_version` constant = `v001` | PASS | `unique=1` |
| 36 | Derived manifest `dataset_family` = `microstructure_normalized_aggtrades_v001` | PASS | exact |
| 37 | Derived manifest `version` = `v001` | PASS | exact |
| 38 | Derived manifest `symbol` = `BTCUSDT` | PASS | exact |
| 39 | Derived manifest `file_count` = 1 | PASS | exact |
| 40 | Derived manifest `files[*].sha256` = normalized Parquet SHA | PASS | matches `2b3d6978...` |
| 41 | Derived manifest `research_eligible` = `false` | PASS | strict `False` |
| 42 | Derived manifest `eligibility_gate_status` = `pending` | PASS | exact |
| 43 | Derived manifest governance label `feature_computation` = `forbidden` | PASS | exact |
| 44 | Derived manifest governance label `strategy_use` = `forbidden` | PASS | exact |
| 45 | Derived manifest references Phase 4bb-D report ID and SHA | PASS | both ID and SHA match in `governance_labels` |
| 46 | Derived manifest references source raw zip SHA | PASS | `governance_labels.source_raw_zip_sha256 = f560c2e5...` |
| 47 | Derived manifest references source raw manifest SHA | PASS | `governance_labels.source_manifest_sha256 = a371edd4...` |
| 48 | Derived manifest `invalid_windows` = `[]` | PASS | empty list |
| 49 | Raw manifest `research_eligible` remains `false` | PASS | strict `False` |
| 50 | Raw manifest `eligibility_gate_status` remains `pending` | PASS | exact |
| 51 | Raw manifest SHA = `a371edd4...` | PASS | recomputed identical |
| 52 | Raw zip SHA = `f560c2e5...` | PASS | recomputed identical |
| 53 | Raw sidecar SHA = `b80c2768...` | PASS | recomputed identical |
| 54 | Acquisition log SHA = `f88b28b4...` | PASS | recomputed identical |
| 55 | Phase 4bb-D gate report SHA = `96f09159...` | PASS | recomputed identical |
| 56 | Normalized outputs are gitignored and not staged | PASS | `git check-ignore -v data/microstructure/normalized/` returns `.gitignore:85` |
| 57 | `data/microstructure/normalized/` gitignored | PASS | covered by `.gitignore:85: data/microstructure/` |
| 58 | No tracked data files changed | PASS | `git status` shows only Phase 4be docs to be committed |
| 59 | No source/test/script/config files changed by Phase 4be | PASS | `git diff --name-only main...HEAD` shows only docs |
| 60 | No Stage-1 / Stage-2 / Stage-3 / Stage-4 transition authorized | PASS | Phase 4be is inspection-only |

**Summary: 60 / 60 PASS, 0 FAIL, 0 ERROR, 0 NOT_APPLICABLE.**

---

## 10. Parquet schema result

`pyarrow.parquet.read_table(...).schema` reports exactly the 19 canonical columns of `NORMALIZED_SCHEMA_V001` in the predeclared order:

```text
 1 dataset_family                 string
 2 dataset_version                string
 3 source_dataset_family          string
 4 source_dataset_version         string
 5 symbol                         string
 6 utc_date                       string
 7 agg_trade_id                   int64
 8 price                          string  (Decimal-as-string; lossless)
 9 quantity                       string  (Decimal-as-string; lossless)
10 first_trade_id                 int64
11 last_trade_id                  int64
12 transact_time_ms               int64
13 is_buyer_maker                 bool
14 source_file_sha256             string
15 source_manifest_sha256         string
16 source_gate_report_id          string
17 source_gate_report_sha256      string
18 row_index                      int64
19 normalization_schema_version   string
```

No extra column. No feature / label / signal / proxy / return / alpha / edge / imbalance / sweep / spread / depth / liquidity / slippage / order-flow / execution-quality / ML / strategy column.

---

## 11. Row-count / row-index result

- Parquet row count: 1,681,098.
- Derived manifest `event_count`: 1,681,098.
- `row_index` is exactly `np.arange(0, 1681098)` (contiguous, strictly increasing, no duplicates).
- `agg_trade_id` is monotonically non-decreasing and has 1,681,098 distinct values (no duplicates).

---

## 12. First / last row spot-check result

```text
First (row_index=0):
  agg_trade_id      = 2516301323
  transact_time_ms  = 1736899205109
  price             = "96514.9"
  quantity          = "0.091"
  is_buyer_maker    = True
  first_trade_id    = 5840262657
  last_trade_id     = 5840262665

Last (row_index=1681097):
  agg_trade_id      = 2517982420
  transact_time_ms  = 1736985599991
  price             = "100460.0"
  quantity          = "0.059"
  is_buyer_maker    = True
  first_trade_id    = 5844290447
  last_trade_id     = 5844290451
```

These match the Phase 4bb-A structural QA values bit-for-bit.

---

## 13. Timestamp-boundary result

- `first transact_time_ms` = 1736899205109 = raw manifest `start_time_ms`.
- `last  transact_time_ms` = 1736985599991 = raw manifest `end_time_ms`.
- For every row, `1736899200000 ≤ transact_time_ms < 1736985600000` — i.e. `T ∈ [2025-01-15T00:00:00.000Z, 2025-01-16T00:00:00.000Z)`.

---

## 14. Precision / type result

- `price` and `quantity` are stored as Arrow `string` (Decimal-parsable; no float storage; lossless representation of the raw Binance archive values).
- `is_buyer_maker` is strict Arrow `bool` (no int / 0/1 / "true"/"false").
- `agg_trade_id`, `first_trade_id`, `last_trade_id`, `transact_time_ms`, `row_index` are all Arrow `int64`.
- All other columns are Arrow `string`.

---

## 15. Lineage column result

For every row, the per-row lineage columns are constant and equal the expected values:

| Column | Unique count | Value |
| ------ | -----------: | ----- |
| `dataset_family` | 1 | `microstructure_normalized_aggtrades_v001` |
| `dataset_version` | 1 | `v001` |
| `source_dataset_family` | 1 | `microstructure_raw_aggtrades_v001` |
| `source_dataset_version` | 1 | `v001` |
| `symbol` | 1 | `BTCUSDT` |
| `utc_date` | 1 | `2025-01-15` |
| `source_file_sha256` | 1 | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| `source_manifest_sha256` | 1 | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` |
| `source_gate_report_id` | 1 | `microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c` |
| `source_gate_report_sha256` | 1 | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| `normalization_schema_version` | 1 | `v001` |

---

## 16. Derived manifest result

- `dataset_family = microstructure_normalized_aggtrades_v001`.
- `version = v001`.
- `symbol = BTCUSDT`.
- `event_count = 1,681,098`.
- `file_count = 1`.
- `files[0].sha256 = 2b3d6978...` (matches normalized Parquet SHA bit-for-bit).
- `research_eligible = false`.
- `eligibility_gate_status = pending`.
- `governance_labels.feature_computation = forbidden`.
- `governance_labels.strategy_use = forbidden`.
- `governance_labels.source_gate_report_id = microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c`.
- `governance_labels.source_gate_report_sha256 = 96f09159...`.
- `governance_labels.source_raw_zip_sha256 = f560c2e5...`.
- `governance_labels.source_manifest_sha256 = a371edd4...`.
- `invalid_windows = []`.

---

## 17. Raw artefact immutability result

All five raw / governance artefact SHAs are byte-for-byte identical to the values recorded by Phase 4bd:

```text
raw manifest          a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201   IDENTICAL
raw zip               f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e   IDENTICAL
sidecar               b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d   IDENTICAL
acquisition log       f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c   IDENTICAL
Phase 4bb-D gate      96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423   IDENTICAL
```

The original Phase 4az manifest still has `research_eligible=false / eligibility_gate_status=pending`. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant remains preserved.

---

## 18. Gitignored-output result

- `git check-ignore -v data/microstructure/` returns `.gitignore:85:data/microstructure/	data/microstructure/`.
- `git check-ignore -v data/microstructure/normalized/` returns `.gitignore:85:data/microstructure/	data/microstructure/normalized/`.
- The Phase 4bd normalized Parquet, paired sidecar, derived manifest, and paired sidecar all live under the gitignored namespace and are not staged for commit by Phase 4be.
- `git status` post-write shows only Phase 4be docs (the memo, the closeout, the narrow `current-project-state.md` update) plus pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`).

---

## 19. Interpretation

The Phase 4bd Stage-0 normalized artefacts are **structurally QA-passed**. The 19-column Parquet faithfully preserves the Phase 4az raw aggTrades data: row count parity (1,681,098), strict 1:1 row mapping (`row_index` contiguous + `agg_trade_id` unique non-decreasing), first / last row spot-check parity vs Phase 4bb-A, half-open UTC-day timestamp policy, lossless string-Decimal price / quantity, strict-bool `is_buyer_maker`, constant per-row lineage to Phase 4az raw zip / raw manifest / Phase 4bb-D gate report, and a derived manifest whose contract matches both the Phase 4bc design and the Phase 4bd-A plan.

This is **not** a Stage-1 / Stage-2 / Stage-3 / Stage-4 transition. The derived family carries `research_eligible=false / eligibility_gate_status=pending` exactly as designed. A future separately authorized derived-family eligibility-gate design / execution sequence is still required before any research-eligibility decision.

---

## 20. What this phase proves

- The Phase 4bd normalized Parquet preserves the raw aggTrades data faithfully at the structural level (row count, row order, row identity, timestamps, price / quantity precision, taker side bool, per-row lineage).
- The Phase 4bd derived manifest correctly references the Phase 4bb-D PASS gate by ID and SHA and the Phase 4az raw artefacts by SHA.
- The Phase 4bd defaults `research_eligible=false / eligibility_gate_status=pending / feature_computation=forbidden / strategy_use=forbidden` are all in force on the persisted manifest.
- The Phase 4az raw manifest, raw zip, sidecar, acquisition log, and Phase 4bb-D gate report are byte-for-byte unchanged.
- The Phase 4bd local outputs remain gitignored; no `data/microstructure/` content is committed.

---

## 21. What this phase does not prove

- Does **not** prove research eligibility of any family.
- Does **not** prove research eligibility of the derived family.
- Does **not** authorize Stage-1 inspection beyond this structural QA, Stage-2 gate-passed transition, Stage-3 research eligibility, or Stage-4 feature-cleared status.
- Does **not** prove that any specific feature, label, signal, model, or strategy can be computed from this dataset.
- Does **not** authorize any successor phase, paper / shadow, live-readiness, deployment, exchange-write, or production-key creation.
- Does **not** revisit the Phase 4bb-D gate decision or modify any Phase 4bd computation.

---

## 22. Preserved boundaries

Phase 4be preserves verbatim:

- §11.6 LOCK (cost realism; not exercised).
- §1.7.3 LOCK (project boundaries; not exercised).
- Phase 3p §4.7 LOCK (Phase 2 manifest immutability; not affected).
- Phase 3r §8 LOCK, Phase 3v §8 LOCK, Phase 3w §6 / §7 / §8 LOCK.
- Phase 4j §11 LOCK.
- Phase 4ak M0 + post-null cooldown (no model trained; no successor authorized).
- Phase 4al refined no-rescue + §13 + §14.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant.
- Phase 4ax `validate_aggtrade_payload`.
- Phase 4ba 5-stage ladder (Stage-0 derived; no skip).
- Phase 4bb-D PASS gate (cited; not modified).
- Phase 4bb-E successor-state policy.
- Phase 4bc design (schema, partitioning, governance labels, 27 checks).
- Phase 4bd-A plan.
- Phase 4bd implementation result.

All retained verdicts (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1; 5m thread closed) are preserved verbatim.

---

## 23. Recommended future options (NOT authorized by Phase 4be)

- **Primary:** remain paused.
- **Conditional next** if continuing: Phase 4bf-A — AggTrades Derived-Family Eligibility-Gate Design Memo (docs-only).
- **Conditional alternative:** Phase 4bb-F — Gate Report Output Path Hygiene (before any repeated raw gate executions).
- **Conditional raw policy marker:** Phase 4bb-G — Raw Manifest Successor-State Recording (sibling successor-state manifest only; preserves the original v001 manifest byte-identically and preserves `research_eligible=false`).

Phase 4be does not authorize any of these.

---

## 24. Closeout / lock preservation

Phase 4be is inspection only. No prior verdict, project lock, or governance memo is amended. No successor is authorized. The branch `phase-4be/aggtrades-normalized-structural-qa` carries one commit (`docs(phase-4be): inspect normalized aggtrades artefacts`) with tracked docs / `current-project-state.md` changes only — no `data/microstructure/` content is committed (it remains gitignored and locally reproducible).
