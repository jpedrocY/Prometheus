# Phase 4bf-A — AggTrades Derived-Family Eligibility-Gate Design Memo

**Phase identity:** Phase 4bf-A — AggTrades Derived-Family Eligibility-Gate Design Memo.
**Type:** docs-only derived-family eligibility-gate design memo.
**Date:** 2026-05-07.
**Branch:** `phase-4bf-a/aggtrades-derived-eligibility-gate-design`.
**Status:** drafted; pending operator review.

---

## 1. Phase header

Phase 4bf-A is a docs-only design memo for a future derived-family eligibility gate that would be applied to the normalized aggTrades family `microstructure_normalized_aggtrades_v001`. It is **design only**. It does not implement code, run a gate, mutate manifests, flip eligibility flags, compute features, train ML, create strategy logic, run backtests, acquire data, or authorize any successor. It does not transition any stage and does not promote `research_eligible` for any family.

Core question: **what exact eligibility gate should the normalized derived family pass before any Stage-2 gate-passed transition, Stage-3 research-eligibility decision, or future feature/ML/strategy work can be considered?**

The memo answers that question conceptually and predeclares the future Phase 4bf gate at the level of: input artefacts, output artefact path discipline, derived manifest mutation policy, eligibility-state policy, research-eligibility policy, check groups, exact check enumeration with stable IDs, fail-closed rules, future implementation modules, future test plan, and acceptance criteria for future Phase 4bf execution.

---

## 2. Current state

| Item | Value |
| ---- | ----- |
| `main` HEAD | `2bfe65f0e48ac6ba5ffd3eaf3ee388a2cb4dc1da` |
| `origin/main` HEAD | `2bfe65f0e48ac6ba5ffd3eaf3ee388a2cb4dc1da` |
| Local / origin sync | in sync |
| Phase 4be merge commit (ancestor verified) | `273e30d5041d9abc5e5d80466f367a415650f515` |
| Phase 4be merge-closeout file | `docs/00-meta/implementation-reports/2026-05-07_phase-4be_merge-closeout.md` (present on `main`) |
| `data/microstructure/` gitignored | yes (`.gitignore:85`) |
| `data/microstructure/normalized/` gitignored | yes (`.gitignore:85`) |
| Phase 4bd normalized Parquet | present locally; SHA `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| Phase 4bd derived manifest | present locally; SHA `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9`; `research_eligible=false`, `eligibility_gate_status=pending` |
| Phase 4az raw manifest | unchanged; `research_eligible=false`, `eligibility_gate_status=pending` |

---

## 3. Inputs reviewed

- Phase 4az acquisition (BTCUSDT 2025-01-15 daily archive; 1,681,098 events; raw zip SHA `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`; raw manifest SHA `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201`; sidecar SHA `b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d`; acquisition log SHA `f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c`).
- Phase 4ba 5-stage eligibility ladder + 45-check raw eligibility-gate definition.
- Phase 4bb-A structural QA (21/21 PASS).
- Phase 4bb-B execution plan + Phase 4bb-C primitive (`eligibility_io.py`, `eligibility_gate.py`, `eligibility_checks.py`, `eligibility_report.py`).
- Phase 4bb-D PASS gate report (`overall_status=pass`; 45/45 PASS; report ID `microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c`; report SHA `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`; gate `code_commit_sha=aa612ba2778c97a5150b80064244b90d024bfa54`).
- Phase 4bb-E successor-state policy.
- Phase 4bc derived-family normalization design (19-column schema; 27 normalization-time validation checks; lossless string-Decimal price/quantity; `int64` `transact_time_ms` with half-open UTC-day bounds; deterministic symbol/date partitioning).
- Phase 4bd-A implementation plan.
- Phase 4bd implementation result (`overall_status=pass`; 27/27 PASS; `event_count=1,681,098`; `invalid_window_candidates=0`; `research_eligible_after=False`; `no_successor_authorization=True`; normalized Parquet SHA `2b3d6978...`; derived manifest SHA `f6f0d947...`; raw artefacts byte-identical pre/post).
- Phase 4be structural QA memo (60/60 PASS; 0 FAIL/ERROR/NOT_APPLICABLE; Parquet schema = 19 canonical Phase 4bc columns; row count 1,681,098 = manifest event_count; `row_index` contiguous 0..1681097; `agg_trade_id` 1,681,098 unique non-decreasing; first/last rows match raw bit-for-bit; all `transact_time_ms` ∈ [2025-01-15T00Z, 2025-01-16T00Z); price/quantity Arrow `string`; `is_buyer_maker` strict Arrow `bool`; per-row lineage columns constant; raw artefact SHAs identical).
- Phase 4aw scaffold types (`MicrostructureManifest`, `RawWriter`, `InvalidWindow`, `EligibilityGateStatus`, `MicrostructureConfig`, `ALLOWLIST_PATTERNS` / `DENYLIST_TOKENS`).
- Phase 4ax aggTrades primitives (`validate_aggtrade_payload`, `AggTradeValidationError`, `TakerSide`).
- Project locks: §11.6, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6/§7/§8, Phase 4j §11, Phase 4ak M0 + post-null cooldown, Phase 4al refined no-rescue rule + §13 + §14.

No live endpoints, credentials, `.env`, `.mcp.json`, MCP, Graphify, or external services were consulted.

---

## 4. Scope

- Translate Phase 4ba / Phase 4bb-A..E / Phase 4bc / Phase 4bd / Phase 4be evidence into a precise *future* derived-family eligibility-gate design.
- Define future gate inputs (artefacts read; manifests cited).
- Define future gate outputs (gate report path; sidecar discipline; refuse-to-overwrite).
- Define derived manifest mutation policy (no overwrite; original derived manifest immutable).
- Define eligibility-state policy (gate-level recommendation only; manifest fields untouched without separate authorization).
- Define research-eligibility policy (Stage-3 not reachable from gate alone).
- Define check groups and an explicit ≥40-check enumeration with stable IDs.
- Define fail-closed rules.
- Propose future Phase 4bf implementation file layout, public API, and test plan.
- Define acceptance criteria any future Phase 4bf execution must satisfy.

---

## 5. Non-scope

Phase 4bf-A did **not**:

- modify source code, tests, scripts, configs, README, pyproject, `.gitignore`, MCP files, or governance memos;
- implement a derived-family eligibility gate;
- run any derived-family gate or rerun the raw gate;
- generate a new gate report;
- create a new normalized Parquet, derived manifest, or any other normalized artefact;
- delete, move, rename, or modify any existing `data/microstructure/` file;
- modify the Phase 4az raw manifest, raw zip, sidecar, or acquisition log;
- modify the Phase 4bb-D gate report or its sidecar;
- modify the Phase 4bd normalized Parquet or derived manifest;
- create JSONL, DuckDB, feature, label, signal, proxy, ML, or strategy artefacts;
- acquire data; call Binance APIs / public endpoints / private endpoints; open WebSockets; use credentials, `.env`, or `.mcp.json`;
- compute features, returns, alpha, edge, opportunity rate, taker imbalance, sweep detection, aggressive-flow score, spread, depth, liquidity, slippage, order-flow, execution-quality proxies, regime, momentum, volatility, PnL, MFE, MAE, R-multiple, equity, or position-state columns;
- train ML, create strategy logic, run backtests, or run any simulation;
- flip `research_eligible`, transition `eligibility_gate_status`, or authorize Stage-2 / Stage-3 / Stage-4 transition;
- authorize Phase 4bf, Phase 4bg, Phase 4bg-A, Phase 4bb-F, Phase 4bb-G, Phase 4 canonical, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation;
- revise retained verdicts, change project locks, or amend M0;
- commit anything under `data/microstructure/`.

---

## 6. Phase 4bd Stage-0 dependency

The future derived-family gate operates **entirely on top of** the Phase 4bd Stage-0 derived artefacts and depends on the Phase 4bd commitments holding bit-for-bit:

- normalized Parquet at `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet` with SHA `2b3d6978...`;
- paired `.sha256` sidecar;
- derived manifest at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json` with SHA `f6f0d947...`;
- paired `.sha256` sidecar;
- derived manifest defaults: `research_eligible=false`, `eligibility_gate_status=pending`, `governance_labels.feature_computation=forbidden`, `governance_labels.strategy_use=forbidden`;
- 19-column canonical Phase 4bc schema preserved;
- 1,681,098 rows; `row_index` contiguous; `agg_trade_id` unique non-decreasing;
- per-row lineage columns constant and correct;
- raw artefacts byte-identical to Phase 4az;
- Phase 4bb-D PASS gate report referenced by ID and SHA.

The future derived-family gate must read these artefacts read-only and must not mutate them.

---

## 7. Phase 4be structural QA dependency

Phase 4be returned 60/60 PASS, 0 FAIL, 0 ERROR, 0 NOT_APPLICABLE on the Phase 4bd Stage-0 artefacts. The future Phase 4bf gate cites the Phase 4be result by file reference (memo + closeout + merge-closeout) and treats it as a precondition: if the Phase 4be artefacts are missing, mismatched, or do not record 60/60 PASS, the gate fails closed.

The Phase 4be merge-closeout file is canonical:

```text
docs/00-meta/implementation-reports/2026-05-07_phase-4be_merge-closeout.md
```

---

## 8. Derived-family eligibility objective

The derived-family eligibility gate is **not** a strategy gate, an ML gate, an edge gate, or a profitability gate. It answers exactly:

> Are the Phase 4bd Stage-0 normalized artefacts complete, lineage-preserving, immutable, schema-compliant, feature-free, and structurally suitable to be considered for a *future* research-eligibility decision under separately authorized governance?

It is **not** authorized to answer any of the following:

- Does this dataset have predictive value? (forbidden — feature/ML/strategy work).
- Should features be computed from this dataset? (forbidden — feature-boundary phase).
- Is the dataset fit for paper / shadow / live use? (forbidden — live-readiness phase).
- Should the raw family flip `research_eligible` to `true`? (forbidden — raw family stays `false` permanently per Phase 4bb-E).
- Should the derived family flip `research_eligible` to `true`? (forbidden by gate alone — Stage-3 requires separate authorization with additional governance per §14).

---

## 9. Stage model for the normalized family

| Stage | Name | Required evidence | Authorized by Phase 4bf-A? |
| ----- | ---- | ----------------- | -------------------------- |
| 0 | Acquired | Local Phase 4bd Parquet + sidecar + derived manifest + sidecar | already complete (Phase 4bd) |
| 1 | Inspected | 60/60 structural QA PASS | already complete (Phase 4be) |
| 2 | Gate-passed | Phase 4bf gate-report `overall_status=pass` with all required checks PASS | **NOT** authorized; requires future Phase 4bf execution |
| 3 | Research-eligible | Stage-2 PASS + separate authorization + M0-compatible research-use memo + feature-boundary design | **NOT** authorized; requires future Phase 4bg-A and successor authorization |
| 4 | Feature-cleared | Stage-3 + separately authorized feature-boundary phase | **NOT** authorized |

**Phase 4bf-A itself does not transition any stage.** It only designs the gate that, if executed under separate authorization, could *report-level* recommend a Stage-2 transition.

---

## 10. Proposed derived-family gate scope

The future gate operates on local read-only artefacts only. It must:

- read the derived manifest + sidecar;
- read the normalized Parquet + sidecar;
- read the raw manifest + raw zip + sidecar + acquisition log (read-only, for lineage SHA confirmation);
- read the Phase 4bb-D gate report (read-only, for ID + SHA confirmation);
- reference the Phase 4be QA memo / closeout / merge-closeout (file existence + recorded counts);
- run the proposed check enumeration in §13;
- emit a JSON gate report under a dedicated normalized gate-report namespace;
- never mutate any input artefact;
- never overwrite an existing gate report.

---

## 11. Proposed gate input artefacts

```text
INPUT  derived manifest             data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json
INPUT  derived manifest sidecar     data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json.sha256
INPUT  normalized Parquet           data/microstructure/normalized/microstructure_normalized_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet
INPUT  normalized Parquet sidecar   data/microstructure/normalized/microstructure_normalized_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet.sha256
INPUT  raw manifest                 data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json
INPUT  raw zip                      data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip
INPUT  raw zip sidecar              data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256
INPUT  acquisition log              data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001_acquisition_log.json
INPUT  Phase 4bb-D gate report      data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json
INPUT  Phase 4be QA memo path       docs/00-meta/implementation-reports/2026-05-07_phase-4be_aggtrades-normalized-structural-qa.md
INPUT  Phase 4be closeout path      docs/00-meta/implementation-reports/2026-05-07_phase-4be_closeout.md
INPUT  Phase 4be merge-closeout     docs/00-meta/implementation-reports/2026-05-07_phase-4be_merge-closeout.md
INPUT  code_commit_sha              future Phase 4bf branch HEAD SHA at execution time
```

---

## 12. Proposed gate output artefacts

The future gate must write its output report under a dedicated normalized gate-report namespace:

```text
OUTPUT  data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v001__<unix_ms_at_run>__<short_commit>.json
OUTPUT  data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v001__<unix_ms_at_run>__<short_commit>.json.sha256
```

Both files live under the gitignored `data/microstructure/` namespace and must not be committed.

The gate must:

- refuse to overwrite any existing report file (atomic write-then-rename + refuse-overwrite at the helper layer);
- write the paired `.sha256` sidecar after the JSON file is finalised;
- never write outside `data/microstructure/gate-reports/normalized/`.

---

## 13. Proposed gate report schema

The future report JSON should serialise the following minimum fields:

```json
{
  "report_schema_version": "v001",
  "phase_id": "4bf",
  "report_id": "microstructure_normalized_aggtrades_v001__v001__<unix_ms_at_run>__<short_commit>",
  "dataset_family": "microstructure_normalized_aggtrades_v001",
  "dataset_version": "v001",
  "symbol": "BTCUSDT",
  "utc_date": "2025-01-15",
  "generated_at_unix_ms": <int>,
  "code_commit_sha": "<full_sha>",
  "input_artefacts": {
    "derived_manifest_path": "...",
    "derived_manifest_sha256": "...",
    "normalized_parquet_path": "...",
    "normalized_parquet_sha256": "...",
    "raw_manifest_sha256": "...",
    "raw_zip_sha256": "...",
    "raw_sidecar_sha256": "...",
    "acquisition_log_sha256": "...",
    "raw_gate_report_id": "...",
    "raw_gate_report_sha256": "...",
    "phase_4be_qa_memo_path": "...",
    "phase_4be_closeout_path": "...",
    "phase_4be_merge_closeout_path": "..."
  },
  "checks": [
    {"check_id": "4bf.13.1", "group": "A", "title": "...", "status": "pass|fail|error|not_applicable", "detail": "..."}
  ],
  "overall_status": "pass|fail|error",
  "research_eligible_after": false,
  "eligibility_gate_status_after": "pass|fail",
  "no_successor_authorization": true,
  "boundary_confirmations": {
    "no_manifest_mutation": true,
    "no_normalization_written_outside_namespace": true,
    "no_data_microstructure_write_outside_gate_reports": true,
    "no_feature_computed": true,
    "no_label_computed": true,
    "no_signal_computed": true,
    "no_ml_trained": true,
    "no_strategy_created": true,
    "no_backtest_run": true,
    "no_network_io": true,
    "no_websocket": true,
    "no_credential_read": true,
    "no_env_read": true,
    "no_mcp_or_graphify": true,
    "research_eligible_after_is_false_for_derived_family": true
  }
}
```

`research_eligible_after` is invariant `false` for derived families. `no_successor_authorization` is invariant `true`. `eligibility_gate_status_after` is recommendation only.

---

## 14. Proposed eligibility-state policy

The future gate must follow these binding rules:

1. **Original derived manifest is immutable.** The gate must not modify `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json` (mirroring Phase 4bb-E for the raw family).
2. **`research_eligible` field on the actual manifest** must remain `false` regardless of gate result. The gate has no path to flip it.
3. **`eligibility_gate_status` field on the actual manifest** must remain `pending`. The gate's `eligibility_gate_status_after` is **report-level** only and does not alter the manifest.
4. If a future operator wants a machine-readable Stage-2 marker, that requires a separately authorized successor-state phase or a sibling successor-state manifest (analogous to Phase 4bb-F / Phase 4bb-G for the raw family). Phase 4bf-A does not authorize this.
5. The gate must not write a "v002" derived manifest, a "successor-state" derived manifest, or any companion manifest by itself.

---

## 15. Proposed research_eligible policy

Stage-3 (`research_eligible: true` on the derived family) is **not** allowed from the gate alone. To even be considered later, Stage-3 requires at minimum:

- a Stage-2 derived-family PASS gate report (future Phase 4bf execution);
- the Phase 4be structural QA evidence (60/60 PASS);
- no invalid windows, or a fully governed invalid-window treatment under a separately authorized governance memo;
- documented lineage to the Phase 4bb-D raw PASS gate;
- explicit operator authorization;
- an M0-compatible research-use memo (Phase 4bg-A or equivalent);
- a feature-boundary design that has not yet been implemented;
- no features or labels included in the normalized family;
- no project lock revision;
- no retained verdict revision.

The gate does not take any of these steps. It records evidence so a future memo can.

---

## 16. Proposed check groups

| Group | Theme |
| ----- | ----- |
| A | Artefact existence and sidecar checks |
| B | SHA / immutability checks |
| C | Derived manifest schema and governance checks |
| D | Normalized Parquet schema checks |
| E | Row-count and row-index checks |
| F | Raw-to-normalized lineage checks |
| G | Timestamp and UTC-boundary checks |
| H | Precision and type checks |
| I | Feature / label / signal absence checks |
| J | Invalid-window checks |
| K | Structural QA dependency checks |
| L | Boundary and no-network checks |
| M | Eligibility-state checks |
| N | Report-writing and no-overwrite checks |

---

## 17. Proposed check enumeration (≥ 55 checks; stable IDs)

The future Phase 4bf gate must implement exactly the following check IDs in the listed order. Each check returns one of `pass / fail / error / not_applicable`.

| check_id | group | title | pass criterion | fail-closed behavior | source evidence |
| -------- | :---: | ----- | -------------- | -------------------- | --------------- |
| 4bf.13.1  | A | derived manifest exists | path resolves under `data/microstructure/manifests/` and exists | report `fail` with path; do not proceed | filesystem |
| 4bf.13.2  | A | derived manifest sidecar exists | sibling `.sha256` exists | `fail` | filesystem |
| 4bf.13.3  | B | derived manifest SHA matches sidecar | recomputed SHA == sidecar first-64 hex == cached recorded `f6f0d947...` | `fail` with both values | recompute |
| 4bf.13.4  | A | normalized Parquet exists | Parquet path resolves under `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/` and exists | `fail` | filesystem |
| 4bf.13.5  | A | normalized Parquet sidecar exists | sibling `.sha256` exists | `fail` | filesystem |
| 4bf.13.6  | B | normalized Parquet SHA matches sidecar | recomputed SHA == sidecar == `2b3d6978...` | `fail` | recompute |
| 4bf.13.7  | C | derived manifest event_count == 1,681,098 | exact equality | `fail` with both | manifest |
| 4bf.13.8  | E | normalized Parquet row count == derived manifest event_count | exact equality | `fail` | pyarrow read |
| 4bf.13.9  | C | derived manifest `files[*].sha256` == normalized Parquet SHA | exact equality | `fail` | manifest + recompute |
| 4bf.13.10 | C | derived manifest `dataset_family` == `microstructure_normalized_aggtrades_v001` | exact | `fail` | manifest |
| 4bf.13.11 | C | derived manifest `version` == `v001` | exact | `fail` | manifest |
| 4bf.13.12 | C | derived manifest `symbol` == `BTCUSDT` | exact | `fail` | manifest |
| 4bf.13.13 | M | derived manifest `research_eligible` is `false` | strict `False` | `fail` | manifest |
| 4bf.13.14 | M | derived manifest `eligibility_gate_status` is `pending` | exact | `fail` | manifest |
| 4bf.13.15 | C | derived manifest `governance_labels.feature_computation` is `forbidden` | exact | `fail` | manifest |
| 4bf.13.16 | C | derived manifest `governance_labels.strategy_use` is `forbidden` | exact | `fail` | manifest |
| 4bf.13.17 | F | derived manifest references Phase 4bb-D gate report ID | matches `microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c` | `fail` | manifest |
| 4bf.13.18 | F | derived manifest references Phase 4bb-D gate report SHA | matches `96f09159...` | `fail` | manifest |
| 4bf.13.19 | F | derived manifest references raw manifest SHA | matches `a371edd4...` | `fail` | manifest |
| 4bf.13.20 | F | derived manifest references raw zip SHA | matches `f560c2e5...` | `fail` | manifest |
| 4bf.13.21 | J | derived manifest `invalid_windows` is `[]` or governed | empty list, or every entry has explicit governance reference under a separately authorized invalid-window-policy memo | `fail` if non-empty without governance | manifest |
| 4bf.13.22 | D | Parquet schema exactly equals 19-column canonical schema | tuple equality with `NORMALIZED_SCHEMA_V001` | `fail` with diff | pyarrow schema |
| 4bf.13.23 | D | no extra Parquet columns | `len(schema) == 19` | `fail` | pyarrow schema |
| 4bf.13.24 | I | no feature / label / signal / proxy / ML / strategy columns | substring scan over schema names returns no forbidden tokens (incl. `feature`, `label`, `signal`, `return`, `alpha`, `edge`, `imbalance`, `sweep`, `spread`, `depth`, `liquid`, `slippage`, `order_flow`, `execution_qual`, `ml_`, `strategy`, `mfe`, `mae`, `r_multiple`, `pnl`, `equity`) | `fail` with offending names | pyarrow schema |
| 4bf.13.25 | E | `row_index` contiguous 0..N-1 | `np.array_equal(row_index, arange(N))` | `fail` | pyarrow column |
| 4bf.13.26 | E | `row_index` unique | `len(unique) == N` | `fail` | pyarrow column |
| 4bf.13.27 | E | `agg_trade_id` unique | `len(unique) == N` | `fail` | pyarrow column |
| 4bf.13.28 | E | `agg_trade_id` non-decreasing | `all(ati[1:] >= ati[:-1])` | `fail` | pyarrow column |
| 4bf.13.29 | E | first row matches recorded Phase 4be values | exact tuple equality on `(agg_trade_id, transact_time_ms, price, quantity, is_buyer_maker, row_index)` for `(2516301323, 1736899205109, '96514.9', '0.091', True, 0)` | `fail` | pyarrow row |
| 4bf.13.30 | E | last row matches recorded Phase 4be values | exact tuple equality for `(2517982420, 1736985599991, '100460.0', '0.059', True, 1681097)` | `fail` | pyarrow row |
| 4bf.13.31 | G | all `transact_time_ms` ∈ `[2025-01-15T00:00:00.000Z, 2025-01-16T00:00:00.000Z)` | `(T >= day_start).all() and (T < day_end).all()` | `fail` with bounds | pyarrow column |
| 4bf.13.32 | G | first `transact_time_ms` == raw manifest `start_time_ms` | exact equality (1736899205109) | `fail` | pyarrow + manifest |
| 4bf.13.33 | G | last `transact_time_ms` == raw manifest `end_time_ms` | exact equality (1736985599991) | `fail` | pyarrow + manifest |
| 4bf.13.34 | H | `price` column is Arrow `string` | `schema.field('price').type == pa.string()` | `fail` | pyarrow schema |
| 4bf.13.35 | H | `quantity` column is Arrow `string` | `schema.field('quantity').type == pa.string()` | `fail` | pyarrow schema |
| 4bf.13.36 | H | `is_buyer_maker` is strict Arrow `bool` | `schema.field('is_buyer_maker').type == pa.bool_()` | `fail` | pyarrow schema |
| 4bf.13.37 | F | per-row lineage columns constant and correct | each of 11 lineage / metadata columns has exactly one unique value equal to the expected constant | `fail` with offending column | pyarrow column |
| 4bf.13.38 | K | Phase 4be QA memo file exists | `docs/00-meta/implementation-reports/2026-05-07_phase-4be_aggtrades-normalized-structural-qa.md` exists | `fail` | filesystem |
| 4bf.13.39 | K | Phase 4be closeout file exists | `docs/00-meta/implementation-reports/2026-05-07_phase-4be_closeout.md` exists | `fail` | filesystem |
| 4bf.13.40 | K | Phase 4be merge-closeout file exists | `docs/00-meta/implementation-reports/2026-05-07_phase-4be_merge-closeout.md` exists | `fail` | filesystem |
| 4bf.13.41 | K | Phase 4be records 60/60 PASS | substring scan finds the canonical `60 / 60 PASS` line in the QA memo | `fail` | docs |
| 4bf.13.42 | B | raw manifest SHA unchanged | recomputed == `a371edd4...` | `fail` | recompute |
| 4bf.13.43 | M | raw manifest `research_eligible` remains `false` | strict `False` | `fail` | raw manifest |
| 4bf.13.44 | M | raw manifest `eligibility_gate_status` remains `pending` | exact | `fail` | raw manifest |
| 4bf.13.45 | B | raw zip SHA unchanged | recomputed == `f560c2e5...` | `fail` | recompute |
| 4bf.13.46 | B | raw sidecar SHA unchanged | recomputed == `b80c2768...` | `fail` | recompute |
| 4bf.13.47 | B | acquisition log SHA unchanged | recomputed == `f88b28b4...` | `fail` | recompute |
| 4bf.13.48 | B | Phase 4bb-D gate report SHA unchanged | recomputed == `96f09159...` | `fail` | recompute |
| 4bf.13.49 | L | normalized outputs are gitignored | `git check-ignore -v` returns `.gitignore:85` for both `data/microstructure/` and `data/microstructure/normalized/` | `fail` | git |
| 4bf.13.50 | L | no tracked data files changed by the gate | post-run `git diff --name-only` empty for `data/` | `fail` | git |
| 4bf.13.51 | L | no network / endpoint / credential / MCP / Graphify / `.env` / `.mcp.json` imports in future gate modules | static scan over all 4 future gate modules (analogous to Phase 4bb-C `test_eligibility_no_network.py` and Phase 4bd `test_normalize_no_network.py`); no forbidden imports (`requests`, `httpx`, `aiohttp`, `urllib.request`, `urllib3`, `socket`, `websockets`, `binance`, `dotenv`, `python_dotenv`); no forbidden tokens (`api_key`, `secret`, `signature`, `listenKey`, `userDataStream`, `/fapi/v1/...`, `.env`, `Graphify`, `MCP`, `.mcp.json`, `os.environ`, `getenv`) | runtime-stop / Verdict D | static scan |
| 4bf.13.52 | N | gate report output path under gitignored `data/microstructure/gate-reports/normalized/` | path-discipline assertion at writer layer | runtime-stop | path discipline |
| 4bf.13.53 | N | gate report refuses overwrite | atomic write-then-rename + `os.path.exists(target)` check before rename | runtime-stop | writer |
| 4bf.13.54 | N | result `len(checks)` equals expected count (this enumeration: 55) | exact equality | `fail` | result construction |
| 4bf.13.55 | N | result invariants: `research_eligible_after=False`, `no_successor_authorization=True` | both fields strictly hold | runtime-stop / Verdict D | result construction |

The gate is allowed to add additional checks within the same group taxonomy if useful, provided they remain inspection-only and do not violate any of §14, §15, or §18.

---

## 18. Required fail-closed rules

The future Phase 4bf gate must fail closed (`overall_status` = `fail` or runtime-stop = Verdict D) if any of the following occur:

1. Missing artefact (any of §11 inputs).
2. SHA mismatch (derived manifest, normalized Parquet, raw manifest, raw zip, sidecar, acquisition log, or Phase 4bb-D gate report).
3. Row-count mismatch (Parquet vs derived manifest `event_count`, or vs recorded 1,681,098).
4. Schema mismatch (Parquet schema does not equal `NORMALIZED_SCHEMA_V001` exactly).
5. Extra or forbidden columns (any column not in the 19-column canonical schema, or any forbidden-token column).
6. Feature / label / signal / proxy column detected.
7. Derived manifest `research_eligible` is not `false`.
8. Derived manifest `eligibility_gate_status` is not `pending`.
9. Derived manifest `governance_labels.feature_computation` is not `forbidden` or `governance_labels.strategy_use` is not `forbidden`.
10. Raw manifest state drift (research_eligible / eligibility_gate_status / SHA / mtime).
11. Phase 4be QA evidence not found, or QA memo does not record 60/60 PASS.
12. `invalid_windows` non-empty without a separately authorized governance reference.
13. Network / credential / MCP / Graphify / `.env` / `.mcp.json` token found in any of the future gate modules.
14. Gate report overwrite risk (target file already exists at finalisation time).
15. Any check function raises an unhandled exception (defensive wrapper turns this into `error` status; `overall_status` becomes `fail` if any `error` survives).
16. Any check returns `fail`.
17. The result `research_eligible_after` is anything other than `False`.
18. The result `no_successor_authorization` is anything other than `True`.

---

## 19. Proposed implementation plan for a future Phase 4bf

### 19.1 Future source modules

```text
src/prometheus/research/microstructure/derived_gate_io.py        # read-only loaders, path-discipline, atomic write, sidecar pairing
src/prometheus/research/microstructure/derived_gate_checks.py    # one check_* function per 4bf.13.X check + run_all_checks
src/prometheus/research/microstructure/derived_gate_report.py    # report data model + atomic JSON write + paired SHA256
src/prometheus/research/microstructure/derived_gate.py           # public orchestrator: DerivedAggTradesGateInput / Result + run_derived_aggtrades_gate
src/prometheus/research/microstructure/__init__.py               # narrow re-export update only
```

No existing source module may be modified beyond the narrow `__init__.py` re-export update.

### 19.2 Future test modules

```text
tests/research/microstructure/_derived_gate_fixtures.py            # optional shared fixture builder; reuses _normalize_fixtures
tests/research/microstructure/test_derived_gate_io.py              # path discipline, atomic writes, refuse-to-overwrite, SHA helpers
tests/research/microstructure/test_derived_gate_checks.py          # one PASS + one FAIL per 4bf.13.X check
tests/research/microstructure/test_derived_gate_report.py          # JSON serialisation, sidecar pairing, schema-version field
tests/research/microstructure/test_derived_gate.py                 # end-to-end on tmp_path mini-fixture; happy path + per-failure-pattern
tests/research/microstructure/test_derived_gate_no_network.py      # static scan: forbidden imports + forbidden tokens across all 4 gate modules
```

No existing test may be modified beyond the parametrize automatically picking up the new modules in `test_import_boundaries.py` (analogous to Phase 4bd).

### 19.3 Future `scripts/` entrypoint

**No** new script under `scripts/`. Phase 4bf must be invokable via direct module import only (analogous to Phase 4bb-C / Phase 4bb-D pattern).

### 19.4 Future configuration / dependency

- No new Python dependency; reuse `pyarrow`, `numpy`, stdlib `hashlib`, `json`, `pathlib`, `tempfile`, `os`.
- No `pyproject.toml` modification.
- No `README.md` modification.
- No `.gitignore` modification (`data/microstructure/` already covers the new gate-report subdirectory).

---

## 20. Proposed test plan for a future Phase 4bf

Minimum coverage:

| Test family | Count target | Notes |
| ----------- | -----------: | ----- |
| `test_derived_gate_io.py` | ≥ 15 | atomic Parquet read; atomic JSON write; path under `data/microstructure/gate-reports/normalized/`; refuse-to-overwrite; SHA helper round-trip |
| `test_derived_gate_checks.py` | 1 PASS + 1 FAIL per check | 55 × 2 = 110 tests minimum |
| `test_derived_gate_report.py` | ≥ 6 | JSON schema; sidecar pairing; report_id format; refuse-overwrite at writer; report SHA = recomputed |
| `test_derived_gate.py` | ≥ 12 | end-to-end on tmp_path fixture; happy-path PASS; per-failure-pattern (manifest mutated; Parquet mutated; Phase 4be missing; raw manifest drift; `research_eligible=true` poisoned manifest; missing sidecars); result invariant assertions |
| `test_derived_gate_no_network.py` | ≥ 8 | static scan over the 4 new gate modules; forbidden imports; forbidden tokens; runtime helper `assert_no_dangerous_imports_loaded()` available but not invoked by orchestrator |

Total minimum: **150+ new tests**.

All tests must be offline (`pytest tests/research/microstructure/test_derived_gate_no_network.py` must guarantee no network reachability statically).

---

## 21. Proposed public API (future Phase 4bf only)

```text
DerivedAggTradesGateInput          # frozen dataclass: derived_manifest_path, output_root, code_commit_sha, write_report=True
DerivedAggTradesGateResult         # frozen dataclass: overall_status, research_eligible_after=False, no_successor_authorization=True,
                                   # checks: tuple[DerivedAggTradesCheckResult, ...], invalid_window_candidates, measured_summary,
                                   # boundary_confirmations, report_path
DerivedAggTradesCheckResult        # frozen dataclass: check_id, group, status, detail, evidence
DerivedAggTradesCheckStatus        # StrEnum: PASS / FAIL / NOT_APPLICABLE / ERROR
DerivedAggTradesGateReport         # data model for JSON serialisation
DerivedAggTradesGateInputError     # raised on path discipline / missing input
DerivedAggTradesGateUnsupportedError # raised on reserved-but-disabled features (e.g. successor-state writing)
GateIOError                         # path / write / overwrite errors
run_derived_aggtrades_gate(inp) -> DerivedAggTradesGateResult
```

These are **proposed** future APIs only and are **not** implemented by Phase 4bf-A.

---

## 22. Acceptance criteria for future derived-family gate implementation

A future Phase 4bf execution is acceptable only if:

1. it implements the §17 check list **exactly** (same IDs; same order; same pass criteria).
2. it uses offline local files only (no network, no endpoints, no credentials).
3. it writes only a gate report and paired `.sha256` sidecar under gitignored `data/microstructure/gate-reports/normalized/`.
4. it does **not** modify the derived manifest.
5. it does **not** modify the normalized Parquet.
6. it does **not** modify the raw manifest, raw zip, sidecar, acquisition log, or Phase 4bb-D gate report.
7. it does **not** compute features, labels, signals, proxies, ML, or strategy artefacts.
8. it does **not** train ML, create strategy logic, run backtests, or run any simulation.
9. it does **not** acquire data.
10. `result.research_eligible_after` is invariant `False`.
11. `result.no_successor_authorization` is invariant `True`.
12. `ruff check .` passes.
13. `mypy src/prometheus` strict passes.
14. Whole-repo `pytest` passes with only the two known pre-existing simulation failures (`tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt`).
15. Targeted tests (≥ 150) pass.
16. `git diff --check` clean.
17. No new `scripts/...` entrypoint.
18. No new dependency in `pyproject.toml`.
19. No `.gitignore` change.
20. No successor authorized by the implementation alone.

---

## 23. What Phase 4bf-A proves

- A precise, predeclared design exists for a future derived-family eligibility gate.
- The design respects the Phase 4bb-E / Phase 4bd / Phase 4be precedents (immutable original derived manifest; gate-level `eligibility_gate_status_after` recommendation only; `research_eligible` permanently `false` for raw family; no Stage-3 from gate alone for derived family).
- The check enumeration is bound to stable IDs (`4bf.13.1`..`4bf.13.55`) and to a check-group taxonomy.
- The path-discipline boundary for gate-report output (`data/microstructure/gate-reports/normalized/`) is predeclared.
- The future implementation file layout, public API, and test-plan minimum (≥ 150 new tests) are predeclared.
- The acceptance criteria for any future Phase 4bf execution are explicit.
- All raw / governance / Phase 4bd / Phase 4be artefacts remain unchanged.

---

## 24. What Phase 4bf-A does not prove

- Does **not** prove the derived family is research-eligible.
- Does **not** authorize Stage-2 / Stage-3 / Stage-4 transition.
- Does **not** authorize Phase 4bf, Phase 4bg, Phase 4bg-A, or any successor.
- Does **not** authorize feature / ML / strategy / backtest / acquisition / paper / shadow / live-readiness / deployment / production keys / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials.
- Does **not** modify any prior memo, source module, test, script, governance rule, project lock, or retained verdict.
- Does **not** prove that any feature, label, signal, model, or strategy is computable from this dataset.

---

## 25. Preserved boundaries

Phase 4bf-A preserves verbatim:

- §11.6 LOCK (cost realism; not exercised).
- §1.7.3 LOCK (project boundaries; not exercised).
- Phase 3p §4.7 LOCK (Phase 2 manifest immutability; not affected).
- Phase 3r §8 LOCK, Phase 3v §8 LOCK, Phase 3w §6 / §7 / §8 LOCK.
- Phase 4j §11 LOCK.
- Phase 4ak M0 + post-null cooldown (no model trained; no successor authorized).
- Phase 4al refined no-rescue + §13 + §14.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant.
- Phase 4ax `validate_aggtrade_payload`.
- Phase 4ba 5-stage ladder.
- Phase 4bb-D PASS gate (cited; not modified).
- Phase 4bb-E successor-state policy.
- Phase 4bc design.
- Phase 4bd-A plan.
- Phase 4bd implementation result.
- Phase 4be structural QA result (60/60 PASS).

All retained verdicts (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1; 5m thread closed) preserved verbatim.

---

## 26. Recommended future options (NOT authorized by Phase 4bf-A)

- **Primary:** remain paused.
- **Conditional next** if continuing: **Phase 4bf — AggTrades Derived-Family Eligibility-Gate Implementation and Execution** (docs-and-code plus local gitignored gate-report only; implements this design verbatim; runs the gate exactly once against the Phase 4bd Stage-0 artefacts; produces a local gitignored gate report).
- **Conditional later, only after a derived-family PASS report:** **Phase 4bg-A — Derived-Family Research-Eligibility Decision Memo** (docs-only; would consider whether to flip `research_eligible` to `true` on the derived family under separate authorization and additional governance).
- **Conditional cleanup:** **Phase 4bb-F — Gate Report Output Path Hygiene** (before any future repeated raw gate executions; corrects the doubled `gate-reports/gate-reports/` path observed in Phase 4bb-C orchestrator output).
- **Conditional raw policy marker:** **Phase 4bb-G — Raw Manifest Successor-State Recording** (sibling successor-state manifest only; preserves the original v001 byte-identically and preserves `research_eligible=false`).

Phase 4bf-A does **not** authorize any of these.

---

## 27. Closeout / lock preservation

Phase 4bf-A is design only. No prior verdict, project lock, or governance memo is amended. No successor is authorized. The branch `phase-4bf-a/aggtrades-derived-eligibility-gate-design` carries one commit (`docs(phase-4bf-a): design derived aggtrades eligibility gate`) with tracked docs / `current-project-state.md` changes only — no `data/microstructure/` content is committed (it remains gitignored and locally reproducible).
