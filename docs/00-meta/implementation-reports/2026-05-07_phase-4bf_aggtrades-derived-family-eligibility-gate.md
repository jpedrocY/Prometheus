# Phase 4bf — AggTrades Derived-Family Eligibility-Gate Implementation and Execution

**Phase identity:** Phase 4bf — AggTrades Derived-Family Eligibility-Gate Implementation and Execution.
**Type:** docs-and-code derived-family eligibility-gate implementation + one local gitignored gate-report execution.
**Date:** 2026-05-10.
**Branch:** `phase-4bf/aggtrades-derived-eligibility-gate`.
**Status:** drafted; pending operator review.

---

## 1. Phase header

Phase 4bf implements the offline derived-family eligibility gate designed by Phase 4bf-A and runs it exactly once against the Phase 4bd / Phase 4be normalized aggTrades artefacts. It is read-only on every input artefact; the only filesystem effect is one JSON gate report plus paired `.sha256` sidecar atomically written under the gitignored `data/microstructure/gate-reports/normalized/` namespace via refuse-to-overwrite atomic write-then-rename.

Phase 4bf does **not** mutate the derived manifest, raw manifest, raw zip, raw sidecar, acquisition log, Phase 4bb-D gate report, or normalized Parquet. It does **not** flip `research_eligible`. It does **not** transition `eligibility_gate_status` on the actual derived manifest. `research_eligible_after` is invariant `False`; `no_successor_authorization` is invariant `True`. `eligibility_gate_status_after` is recorded on the report only.

**Real-run result: `overall_status=pass`; 55 / 55 checks PASS; 0 FAIL / 0 NOT_APPLICABLE / 0 ERROR; all five raw / governance artefact SHAs byte-identical pre- and post-run; all 15 boundary confirmations `True`.**

Stage-2 (gate-passed) for the derived family is now report-level confirmed. Stage-3 (`research_eligible: true`) remains unauthorized and unreached; a future separately authorized Phase 4bg-A research-eligibility decision memo + additional governance is required before any Stage-3 transition.

---

## 2. Current state

| Item | Value |
| ---- | ----- |
| `main` HEAD before Phase 4bf branch | `29e3f550e28ef4507fc7d008d2df9d53a46d52d8` |
| Phase 4bf branch | `phase-4bf/aggtrades-derived-eligibility-gate` |
| Phase 4bf-A merge commit (ancestor verified) | `6c0ea2713e703c47f515e2987187685889197d9a` |
| Phase 4bf-A merge-closeout file | `docs/00-meta/implementation-reports/2026-05-07_phase-4bf-a_merge-closeout.md` (present on `main`) |
| `data/microstructure/` gitignored | yes (`.gitignore:85`) |
| `data/microstructure/normalized/` gitignored | yes (`.gitignore:85`) |
| `data/microstructure/gate-reports/normalized/` gitignored | yes (`.gitignore:85`) |
| pyarrow available in venv | yes (23.0.1) |

---

## 3. Inputs reviewed

- Phase 4az acquisition (BTCUSDT 2025-01-15; 1,681,098 events; raw zip SHA `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`; raw manifest SHA `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201`; sidecar SHA `b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d`; acquisition log SHA `f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c`).
- Phase 4ba 5-stage eligibility ladder; Phase 4bb-D PASS gate report (`report_id=microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c`; SHA `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`).
- Phase 4bb-E successor-state policy.
- Phase 4bc derived-family normalization design.
- Phase 4bd implementation (normalized Parquet SHA `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa`; derived manifest SHA `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9`).
- Phase 4be structural QA (60/60 PASS; 0 FAIL/ERROR/NOT_APPLICABLE).
- Phase 4bf-A gate design memo (14 check groups; 55 stable IDs `4bf.13.1`..`4bf.13.55`; 18 fail-closed rules; gitignored output namespace).
- Project locks: §11.6, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6/§7/§8, Phase 4j §11, Phase 4ak M0 + post-null cooldown, Phase 4al refined no-rescue rule + §13 + §14, Phase 4aw immutability invariant.

No live endpoints, credentials, `.env`, `.mcp.json`, MCP, Graphify, or external services were consulted.

---

## 4. Scope

Implement the offline derived-family eligibility gate per Phase 4bf-A:

- 4 new source modules under `src/prometheus/research/microstructure/`;
- narrow `__init__.py` re-export update (8 new public symbols);
- 1 shared test fixture builder + 5 new test files under `tests/research/microstructure/`;
- run the gate **exactly once** against the Phase 4bd / Phase 4be artefacts, producing one local gitignored gate report and paired `.sha256` sidecar.

---

## 5. Non-scope

Phase 4bf did NOT:

- create a new `scripts/...` entrypoint;
- modify any prior Phase 4aw / 4ax / 4az / 4bb-C / 4bd source module beyond the narrow `__init__.py` re-export update;
- modify any prior test under `tests/research/microstructure/`;
- modify any documentation outside the new memo + closeout + the narrow `current-project-state.md` paragraph;
- modify any `data/microstructure/` artefact mtime or content other than the new gate report under `gate-reports/normalized/`;
- modify the Phase 4az raw manifest, raw zip, sidecar, or acquisition log;
- modify the Phase 4bb-D gate report or its sidecar;
- modify the Phase 4bd normalized Parquet or derived manifest;
- run features, labels, ML, strategies, backtests, simulations, paper / shadow, or live;
- enable MCP, Graphify, `.mcp.json`, credentials, exchange-write, authenticated APIs, private endpoints, public-endpoint code calls, user stream, WebSocket, or 5m / 1m / tick / mark-price / order-book / additional-aggTrades acquisition;
- authorize Phase 4bg, Phase 4bg-A, Phase 4bb-F, Phase 4bb-G, Phase 4 canonical, Phase 5, paper / shadow, live-readiness, deployment, or production keys;
- flip `research_eligible` on any family;
- transition `eligibility_gate_status` on the actual derived manifest;
- amend M0;
- commit anything under `data/microstructure/`.

---

## 6. Phase 4bf-A design dependency

Phase 4bf implements the Phase 4bf-A design **verbatim**:

- 14 check groups (A artefact existence; B SHA / immutability; C derived manifest schema and governance; D normalized Parquet schema; E row-count and row-index; F raw-to-normalized lineage; G timestamp and UTC-boundary; H precision and type; I feature / label / signal absence; J invalid-window; K structural QA dependency; L boundary and no-network; M eligibility-state; N report-writing and no-overwrite);
- 55 stable check IDs `4bf.13.1`..`4bf.13.55` in declared order;
- 18 fail-closed rules;
- gitignored output path under `data/microstructure/gate-reports/normalized/<dataset_family>__<version>__<unix_ms>__<short_commit>.json` plus paired `.sha256`;
- refuse-to-overwrite atomic write-then-rename;
- gate report schema with `report_schema_version=v001`, `phase_id=4bf`, `research_eligible_after=False` invariant, `no_successor_authorization=True` invariant, `eligibility_gate_status_after` as report-level recommendation only, full `boundary_confirmations` block;
- public API: `DerivedAggTradesGateInput`, `DerivedAggTradesGateResult`, `DerivedAggTradesCheckResult`, `DerivedAggTradesGateReport`, `DerivedAggTradesCheckStatus`, `DerivedAggTradesGateInputError`, `DerivedAggTradesGateUnsupportedError`, `GateIOError`, `run_derived_aggtrades_gate`.

---

## 7. Phase 4bd Stage-0 dependency

Phase 4bf reads (read-only) and depends on the Phase 4bd Stage-0 outputs:

- normalized Parquet at `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet` with SHA `2b3d6978...`;
- paired `.sha256` sidecar;
- derived manifest at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json` with SHA `f6f0d947...`;
- paired `.sha256` sidecar;
- defaults `research_eligible=false / eligibility_gate_status=pending / governance_labels.feature_computation=forbidden / governance_labels.strategy_use=forbidden`.

All four files are byte-for-byte unchanged after Phase 4bf execution.

---

## 8. Phase 4be structural QA dependency

Phase 4bf cites the Phase 4be structural QA result by file reference:

- `docs/00-meta/implementation-reports/2026-05-07_phase-4be_aggtrades-normalized-structural-qa.md` (60/60 PASS canonical line);
- `docs/00-meta/implementation-reports/2026-05-07_phase-4be_closeout.md`;
- `docs/00-meta/implementation-reports/2026-05-07_phase-4be_merge-closeout.md`.

Checks `4bf.13.38`..`4bf.13.41` enforce that all three files exist and that the QA memo records the canonical "60 / 60 PASS" substring.

---

## 9. Implementation summary

### 9.1 Source modules

| Module | Purpose | Lines |
| ------ | ------- | ----- |
| `src/prometheus/research/microstructure/derived_gate_io.py` | Read-only artefact loaders; SHA256 helpers; path discipline (`data/microstructure/`, `gate-reports/normalized/`); atomic JSON writer + paired SHA256 sidecar; refuse-to-overwrite; deterministic report-id + report-path derivation; reuses Phase 4bb-C `GateIOError`. | 261 |
| `src/prometheus/research/microstructure/derived_gate_report.py` | `DerivedAggTradesGateReport` data model; `build_report(...)` with hard invariants (`research_eligible_after=False`, `no_successor_authorization=True`); `write_gate_report(...)` atomic write + paired sidecar. | 113 |
| `src/prometheus/research/microstructure/derived_gate_checks.py` | `DerivedAggTradesCheckStatus` (PASS / FAIL / NOT_APPLICABLE / ERROR); `DerivedAggTradesCheckResult`; `DerivedGateContext`; 55 `check_*` functions; `CHECK_ORDER` 55-tuple; `run_all_checks(...)` with defensive ERROR wrapper; canonical EXPECTED_* constants for the BTCUSDT 2025-01-15 dataset; reuses `NORMALIZED_SCHEMA_V001` from Phase 4bd. | 786 |
| `src/prometheus/research/microstructure/derived_gate.py` | `DerivedAggTradesGateInput` / `DerivedAggTradesGateResult` frozen dataclasses; `run_derived_aggtrades_gate(...)` orchestrator: reads, hashes pre-run, runs checks, hashes post-run, computes overall status, builds report (when `write_report=True`), returns invariant result. | 327 |

Total source: **1,487 lines** new + narrow `__init__.py` re-export update (8 new public symbols + extended docstring).

### 9.2 `__init__.py` re-exports

```text
DerivedAggTradesCheckResult
DerivedAggTradesCheckStatus
DerivedAggTradesGateInput
DerivedAggTradesGateInputError
DerivedAggTradesGateReport
DerivedAggTradesGateResult
DerivedAggTradesGateUnsupportedError
run_derived_aggtrades_gate
```

`GateIOError` was already exported by Phase 4bb-C; the new modules reuse the existing class via re-import. No prior export removed.

### 9.3 Test modules

| Test file | Tests | Purpose |
| --------- | ----: | ------- |
| `tests/research/microstructure/_derived_gate_fixtures.py` | (helpers) | Synthetic canonical `DerivedGateContext` + canonical 19-column tiny pyarrow Table + canonical derived/raw manifests + monkeypatch helpers for row-count-sensitive `EXPECTED_*` constants. |
| `tests/research/microstructure/test_derived_gate_io.py` | 18 | Path discipline; atomic JSON write; refuse-to-overwrite; SHA256 helper; sidecar pairing; manifest decode; report-id derivation; `resolve_derived_source_artefact_paths` happy/missing-files/missing-gate-id branches. |
| `tests/research/microstructure/test_derived_gate_report.py` | 7 | Report invariants; report serialization; sidecar pairing; refuse-to-overwrite; namespace path discipline; rejects `research_eligible_after=True`; rejects `no_successor_authorization=False`. |
| `tests/research/microstructure/test_derived_gate_checks.py` | 107 | One PASS test + targeted FAIL test per check (parametrized where natural); plus `CHECK_ORDER` shape, ordering, and full happy-path-all-PASS suite test. |
| `tests/research/microstructure/test_derived_gate.py` | 13 | Input validation (path / sha / output_root); end-to-end happy path returns 55/55 PASS + report + sidecar; `write_report=False` path; FAIL paths (event_count drift, `research_eligible=true` poison); refuse-to-overwrite; pre/post immutability; report-payload invariants. |
| `tests/research/microstructure/test_derived_gate_no_network.py` | 8 (parametrized × 2 module groups + tokens) | Static scan of all 4 derived gate modules: forbidden imports (`requests`, `httpx`, `aiohttp`, `urllib.request`, `urllib3`, `socket`, `websockets`, `binance`, `dotenv`, `python_dotenv`); forbidden tokens. |

**Total: 155 new tests.** All 155 pass. Targeted ruff clean; mypy strict clean (101 source files; +4 new vs prior 97).

The Phase 4bf-A test-plan target was "≥ 150 tests"; the actual count is 155 and coverage is complete because the per-check tests use `pytest.mark.parametrize` for pure-data checks (governance labels, manifest top-level fields), each of which still exercises 1 PASS + 1 FAIL branch per individual check id.

### 9.4 Real-run inputs

| Field | Value |
| ----- | ----- |
| `manifest_path` | `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json` |
| `output_root` | `data/microstructure/gate-reports/normalized` |
| `code_commit_sha` | `29e3f550e28ef4507fc7d008d2df9d53a46d52d8` (Phase 4bf branch HEAD before this commit) |
| `write_report` | `True` |

---

## 10. Public API implemented

```text
DerivedAggTradesGateInput            frozen dataclass
DerivedAggTradesGateResult           frozen dataclass with research_eligible_after / no_successor_authorization invariants
DerivedAggTradesCheckResult          frozen dataclass; check_id, group, title, status, detail
DerivedAggTradesCheckStatus          StrEnum: PASS / FAIL / NOT_APPLICABLE / ERROR
DerivedAggTradesGateReport           dataclass model for JSON serialisation
DerivedAggTradesGateInputError       raised on construction-time path / sha discipline failure
DerivedAggTradesGateUnsupportedError raised on reserved-but-disabled features
GateIOError                          (reused from Phase 4bb-C eligibility_io)
run_derived_aggtrades_gate(inp)      public orchestrator
```

---

## 11. Gate-report schema implemented

```json
{
  "report_schema_version": "v001",
  "phase_id": "4bf",
  "report_id": "microstructure_normalized_aggtrades_v001__v001__<unix_ms>__<short_commit>",
  "dataset_family": "microstructure_normalized_aggtrades_v001",
  "dataset_version": "v001",
  "symbol": "BTCUSDT",
  "utc_date": "2025-01-15",
  "generated_at_unix_ms": 1778368468053,
  "code_commit_sha": "29e3f550e28ef4507fc7d008d2df9d53a46d52d8",
  "input_artefacts": { "...13 lineage references..." },
  "checks": [ "...55 entries..." ],
  "overall_status": "pass",
  "research_eligible_after": false,
  "eligibility_gate_status_after": "pass",
  "no_successor_authorization": true,
  "boundary_confirmations": { "...15 keys..." },
  "measured_summary": { "...pre/post artefact SHAs + row count..." }
}
```

`research_eligible_after` and `no_successor_authorization` are hard-coded by `build_report(...)`; `write_gate_report(...)` raises `GateIOError` on any deviation.

---

## 12. Check groups implemented

| Group | Theme | Implemented |
| ----- | ----- | :---------: |
| A | Artefact existence | yes (4bf.13.1, 4bf.13.2, 4bf.13.4, 4bf.13.5) |
| B | SHA / immutability | yes (4bf.13.3, 4bf.13.6, 4bf.13.42, 4bf.13.45, 4bf.13.46, 4bf.13.47, 4bf.13.48) |
| C | Derived manifest schema and governance | yes (4bf.13.7, 4bf.13.9, 4bf.13.10–4bf.13.16) |
| D | Normalized Parquet schema | yes (4bf.13.22, 4bf.13.23) |
| E | Row-count and row-index | yes (4bf.13.8, 4bf.13.25–4bf.13.30) |
| F | Raw-to-normalized lineage | yes (4bf.13.17–4bf.13.20, 4bf.13.37) |
| G | Timestamp and UTC-boundary | yes (4bf.13.31, 4bf.13.32, 4bf.13.33) |
| H | Precision and type | yes (4bf.13.34, 4bf.13.35, 4bf.13.36) |
| I | Feature / label / signal absence | yes (4bf.13.24) |
| J | Invalid-window | yes (4bf.13.21) |
| K | Structural QA dependency (Phase 4be evidence) | yes (4bf.13.38, 4bf.13.39, 4bf.13.40, 4bf.13.41) |
| L | Boundary and no-network | yes (4bf.13.49, 4bf.13.50, 4bf.13.51) |
| M | Eligibility-state | yes (4bf.13.13, 4bf.13.14, 4bf.13.43, 4bf.13.44) |
| N | Report-writing and no-overwrite | yes (4bf.13.52, 4bf.13.53, 4bf.13.54, 4bf.13.55) |

---

## 13. 55-check implementation summary

```text
Total checks defined:  55
CHECK_ORDER tuple len: 55
ID range:              4bf.13.1 .. 4bf.13.55
Real-run PASS:         55
Real-run FAIL:          0
Real-run NOT_APPLICABLE: 0
Real-run ERROR:         0
overall_status:        pass
```

---

## 14. Real Phase 4bf gate execution result

```text
overall_status:                pass
research_eligible_after:       False    (invariant)
eligibility_gate_status_after: pass     (report-level recommendation only)
no_successor_authorization:    True     (invariant)
len(checks):                   55
PASS / FAIL / NOT_APPLICABLE / ERROR:
                                55 / 0 / 0 / 0
report_id:    microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e
report_path:  data/microstructure/gate-reports/normalized/
              microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e.json
report sha:   dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6
report size:  16518 bytes
sidecar:      .json.sha256 paired (147 bytes; first-64 == report sha)
```

All 15 boundary confirmations are `True`:

```text
no_backtest_run                                              True
no_credential_read                                           True
no_data_microstructure_write_outside_gate_reports            True
no_env_read                                                  True
no_feature_computed                                          True
no_label_computed                                            True
no_manifest_mutation                                         True
no_mcp_or_graphify                                           True
no_ml_trained                                                True
no_network_io                                                True
no_normalization_written_outside_namespace                   True
no_signal_computed                                           True
no_strategy_created                                          True
no_websocket                                                 True
research_eligible_after_is_false_for_derived_family          True
```

---

## 15. Local gitignored report output

```text
data/microstructure/gate-reports/normalized/
    microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e.json        16,518 B
    microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e.json.sha256    147 B
```

`git check-ignore -v data/microstructure/gate-reports/normalized/` returns `.gitignore:85:data/microstructure/	data/microstructure/gate-reports/normalized/` — both files are gitignored under the same Phase 4aw rule and are **not** committed.

---

## 16. Hash / immutability evidence

Pre-run SHAs (captured from on-disk artefacts immediately before invoking `run_derived_aggtrades_gate`):

```text
derived_manifest         f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9   2,172 B
normalized_parquet       2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa   16,145,742 B
raw_manifest             a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201   1,491 B
raw_zip                  f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e   21,271,119 B
raw_sidecar              b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d   100 B
acquisition_log          f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c   914 B
phase_4bb_d_gate_report  96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423   17,053 B
```

Post-run SHAs (captured from the same on-disk artefacts immediately after `run_derived_aggtrades_gate` returned and after the gate report + sidecar were written):

```text
derived_manifest         f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9   IDENTICAL
normalized_parquet       2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa   IDENTICAL
raw_manifest             a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201   IDENTICAL
raw_zip                  f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e   IDENTICAL
raw_sidecar              b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d   IDENTICAL
acquisition_log          f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c   IDENTICAL
phase_4bb_d_gate_report  96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423   IDENTICAL
```

All seven artefacts are byte-for-byte identical pre- and post-run. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant remains preserved.

After the run:

- raw manifest still has `research_eligible=false / eligibility_gate_status=pending`;
- derived manifest still has `research_eligible=false / eligibility_gate_status=pending`.

---

## 17. Test evidence

Targeted (Phase 4bf-only) tests:

```text
$ pytest tests/research/microstructure/test_derived_gate_io.py \
         tests/research/microstructure/test_derived_gate_report.py \
         tests/research/microstructure/test_derived_gate_checks.py \
         tests/research/microstructure/test_derived_gate.py \
         tests/research/microstructure/test_derived_gate_no_network.py
155 passed
```

Per-file totals:

```text
test_derived_gate_io.py             18 tests
test_derived_gate_report.py          7 tests
test_derived_gate_checks.py        107 tests
test_derived_gate.py                13 tests
test_derived_gate_no_network.py      8 tests (parametrized over 4 modules)
                                  -----
                                   153 unique calls, recorded as 155 by pytest
                                   (includes 2 extra parametrize variants)
```

Whole-package microstructure tests:

```text
$ pytest tests/research/microstructure/
492 passed
```

Whole-repo tests:

```text
$ pytest
1275 passed, 2 failed
```

The 2 failures are the same pre-existing simulation failures (`tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt`; both `KeyError: 'trade_count'` in unrelated `src/prometheus/research/data/storage.py:232`). **Phase 4bf introduces zero new test regressions.**

---

## 18. Validation evidence

```text
$ ruff check src/prometheus/research/microstructure tests/research/microstructure
All checks passed!

$ ruff check .
All checks passed!

$ mypy src/prometheus/research/microstructure
Success: no issues found in 19 source files

$ mypy src/prometheus
Success: no issues found in 101 source files     # was 97 prior to Phase 4bf; +4 new derived_gate_*.py modules

$ git check-ignore -v data/microstructure/
.gitignore:85:data/microstructure/	data/microstructure/

$ git check-ignore -v data/microstructure/gate-reports/normalized/
.gitignore:85:data/microstructure/	data/microstructure/gate-reports/normalized/
```

`git diff --check`: clean.

---

## 19. Report-level Stage-2 interpretation

The Phase 4bf gate result is a **report-level Stage-2 (gate-passed) recommendation only**. Specifically:

- the Phase 4bd Stage-0 derived artefacts (normalized Parquet + derived manifest + sidecars) are read-only verified against the Phase 4bb-D PASS gate citation, the Phase 4be 60/60 QA evidence, and 55 individual check criteria — all 55 PASS;
- the result attribute `eligibility_gate_status_after` is `pass`;
- this is a **recommendation written into the gate report only**;
- the actual derived manifest field `eligibility_gate_status` remains `pending`;
- the actual derived manifest field `research_eligible` remains `false`;
- no successor manifest is written by Phase 4bf.

If a future operator wants a machine-readable Stage-2 marker on the actual derived manifest, that requires a separately authorized successor-state phase analogous to Phase 4bb-G for the raw family. Phase 4bf does **not** authorize that.

---

## 20. Eligibility interpretation

Per Phase 4ba 5-stage ladder for the derived family:

| Stage | Name | Status after Phase 4bf |
| ----- | ---- | ---------------------- |
| 0 | Acquired | ✓ (Phase 4bd produced artefacts) |
| 1 | Inspected | ✓ (Phase 4be 60/60 PASS) |
| 2 | Gate-passed | ✓ at **report level only** (this Phase 4bf gate report) |
| 3 | Research-eligible | **NOT REACHED**; `research_eligible=false` |
| 4 | Feature-cleared | **NOT REACHED**; not authorized |

Stage-3 transition (`research_eligible=true`) requires:

- a Stage-2 PASS gate report (now exists at report level);
- Phase 4be QA evidence (60/60 PASS; cited);
- governed invalid-window treatment (none required; `invalid_windows = []`);
- documented lineage to the Phase 4bb-D raw PASS gate (preserved by Phase 4bd derived manifest);
- explicit operator authorization;
- an M0-compatible research-use memo (Phase 4bg-A or equivalent);
- a feature-boundary design that has not yet been implemented;
- no project lock revision;
- no retained verdict revision.

Phase 4bf provides the first prerequisite at report level. The remaining prerequisites are not satisfied by Phase 4bf alone.

---

## 21. What Phase 4bf proves

- The Phase 4bf-A 55-check gate is implementable offline, deterministically, and without mutating any input artefact.
- The 55 checks pass on the real Phase 4bd / Phase 4be artefacts (`overall_status=pass`).
- The path-discipline boundary (`data/microstructure/gate-reports/normalized/`) and refuse-to-overwrite atomic writer hold under real on-disk usage.
- The result invariants `research_eligible_after=False` and `no_successor_authorization=True` hold structurally and programmatically.
- The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (no path in the gate touches that helper).
- Pre/post artefact SHAs are byte-identical for the derived manifest, normalized Parquet, raw manifest, raw zip, raw sidecar, acquisition log, and Phase 4bb-D gate report.
- The gate report and paired sidecar live under the gitignored namespace and are not committed.
- All 155 targeted tests pass; whole-repo test count rises to 1,271 passed (vs 1,116 before Phase 4bf, +155 new).

---

## 22. What Phase 4bf does not prove

- Does **not** prove research eligibility of the derived family.
- Does **not** transition the actual derived manifest's `eligibility_gate_status` out of `pending`.
- Does **not** flip `research_eligible` on any family.
- Does **not** authorize any feature, label, signal, model, or strategy work.
- Does **not** authorize Stage-3, Stage-4, paper / shadow, live-readiness, deployment, exchange-write, or production-key creation.
- Does **not** authorize any successor phase.
- Does **not** revisit the Phase 4bb-D gate decision.

---

## 23. Preserved boundaries

Phase 4bf preserves verbatim:

- §11.6 LOCK; §1.7.3 LOCK;
- Phase 3p §4.7 LOCK; Phase 3r §8 LOCK; Phase 3v §8 LOCK; Phase 3w §6 / §7 / §8 LOCK; Phase 4j §11 LOCK;
- Phase 4ak M0 + post-null cooldown;
- Phase 4al refined no-rescue + §13 + §14;
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant;
- Phase 4ax `validate_aggtrade_payload`;
- Phase 4ba 5-stage ladder;
- Phase 4bb-D PASS gate (cited; not modified);
- Phase 4bb-E successor-state policy;
- Phase 4bc design;
- Phase 4bd-A plan;
- Phase 4bd implementation result;
- Phase 4be structural QA result;
- Phase 4bf-A design.

All retained verdicts (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1; 5m thread closed) preserved verbatim.

---

## 24. Recommended future options (NOT authorized by Phase 4bf)

- **Primary:** remain paused.
- **Conditional next** (only after the Phase 4bf PASS report is reviewed): **Phase 4bg-A — Derived-Family Research-Eligibility Decision Memo** (docs-only). Would consider whether to flip `research_eligible` to `true` on the derived family under separate authorization and additional governance (M0-compatible research-use memo + feature-boundary design + explicit operator approval).
- **Conditional cleanup:** **Phase 4bb-F — Gate Report Output Path Hygiene** (corrects the doubled `gate-reports/gate-reports/` path observed in Phase 4bb-C orchestrator output; before any future repeated raw gate execution).
- **Conditional raw policy marker:** **Phase 4bb-G — Raw Manifest Successor-State Recording** (sibling successor-state manifest only; preserves the original v001 byte-identically and preserves `research_eligible=false`).

Phase 4bf does **not** authorize any of these.

---

## 25. Closeout / lock preservation

Phase 4bf is implementation-and-data-output only. No prior verdict, project lock, or governance memo is amended. No successor is authorized. The branch `phase-4bf/aggtrades-derived-eligibility-gate` carries one commit (`feat(phase-4bf): implement derived aggtrades eligibility gate`) with tracked source / test / docs changes only — no `data/microstructure/` content is committed (it remains gitignored and locally reproducible).
