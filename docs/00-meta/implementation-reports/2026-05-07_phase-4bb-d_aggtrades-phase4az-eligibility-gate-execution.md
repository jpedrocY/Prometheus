# Phase 4bb-D — AggTrades Phase 4az Eligibility-Gate Execution

**Phase identity:** Phase 4bb-D — AggTrades Phase 4az Eligibility-Gate Execution.
**Type:** docs-and-local-gitignored-output gate-execution phase.
**Date:** 2026-05-07.
**Branch:** `phase-4bb-d/aggtrades-phase4az-eligibility-gate-execution`.
**Status:** drafted; pending operator review.

---

## 1. Phase header

Phase 4bb-D is the first authorized invocation of the offline aggTrades eligibility-gate primitive (Phase 4bb-C) against the real local Phase 4az artefacts. It is a one-shot read-only gate execution. It generates exactly one local gitignored gate report plus its paired SHA256 sidecar under the gitignored `data/microstructure/gate-reports/` namespace and records the result in tracked Markdown.

Phase 4bb-D does **not** implement gate code, modify source code, modify tests, modify scripts, acquire data, normalize data, compute features, train ML, create strategies, run backtests, mutate any Phase 4az artefact, flip `research_eligible`, transition the actual manifest's `eligibility_gate_status` out of `pending`, or authorize any successor phase.

---

## 2. Current state

| Item | Value |
| ---- | ----- |
| Phase 4bb-C merge commit (ancestor verified) | `00bc0d8a704630477bed9563d78f52c05fc9adfa` |
| `main` HEAD at start | `aa612ba2778c97a5150b80064244b90d024bfa54` |
| `origin/main` HEAD | `aa612ba2778c97a5150b80064244b90d024bfa54` |
| Local / origin sync | in sync |
| Phase 4bb-C merge-closeout file | `docs/00-meta/implementation-reports/2026-05-07_phase-4bb-c_merge-closeout.md` (present on `main`) |
| `data/microstructure/` gitignored | confirmed via `git check-ignore -v` (`.gitignore:85`) |
| Phase 4az manifest | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json` (present; 1491 bytes; mtime `2026-05-07 21:55:40 UTC+01:00`) |
| Phase 4az raw zip | `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip` (21,271,119 bytes) |
| Phase 4az sidecar | `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256` (100 bytes) |
| Phase 4az acquisition log | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001_acquisition_log.json` (914 bytes) |
| Manifest `research_eligible` | `false` (verified pre-run and post-run) |
| Manifest `eligibility_gate_status` | `pending` (verified pre-run and post-run) |
| Phase 4bb-C public API | importable via `prometheus.research.microstructure.run_eligibility_gate` |

---

## 3. Inputs reviewed

- Phase 4az manifest, raw `.zip`, paired `.sha256` sidecar, acquisition log.
- Phase 4ba 45-check eligibility-time gate model.
- Phase 4bb-A structural QA (21 / 21 PASS).
- Phase 4bb-B execution plan (file/function-level mapping).
- Phase 4bb-C primitive: `eligibility_io.py`, `eligibility_gate.py`, `eligibility_checks.py`, `eligibility_report.py`, and the `__init__.py` re-exports.
- Existing project locks: §11.6, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6/§7/§8, Phase 4j §11, Phase 4ak M0 + post-null cooldown.

No live endpoints, credentials, `.env`, `.mcp.json`, MCP, or Graphify were consulted.

---

## 4. Scope

- Run `run_eligibility_gate` exactly once against the real Phase 4az artefacts in offline read-only mode.
- Write exactly one gate report JSON plus paired SHA256 sidecar under the gitignored `data/microstructure/gate-reports/`.
- Capture pre-run and post-run SHA256 of every Phase 4az artefact and prove byte-fidelity.
- Capture `git check-ignore -v` for both `data/microstructure/` and `data/microstructure/gate-reports/`.
- Record the result in tracked Markdown (this memo + closeout + a narrow `current-project-state.md` update).

---

## 5. Non-scope

Phase 4bb-D did not:

- implement new gate code;
- modify source code;
- modify tests;
- modify scripts;
- acquire data;
- call any Binance endpoint;
- open any WebSocket;
- use private endpoints;
- request or use credentials;
- create `.env`;
- create `.mcp.json`;
- enable MCP or Graphify;
- normalize the Phase 4az dataset;
- create JSONL, Parquet, DuckDB, feature tables, labels, or derived datasets;
- compute features, returns, alpha, edge, opportunity rate, taker imbalance, sweep detection, aggressive-flow score, spread / depth / liquidity / slippage / order-flow / execution-quality proxies;
- train ML;
- create a strategy;
- run a backtest;
- revise any retained verdict;
- change any project lock;
- amend M0;
- flip `research_eligible` for any raw aggTrades family;
- transition the actual manifest `eligibility_gate_status` out of `pending`;
- overwrite, mutate, or modify any Phase 4az artefact;
- commit anything under `data/microstructure/`;
- authorize Phase 4bb-E, Phase 4bc, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation.

---

## 6. Gate invocation method

The gate was invoked exactly once via inline Python (no script created). The invocation imported `run_eligibility_gate` and `AggTradesEligibilityGateInput` directly from the public module surface added by Phase 4bb-C.

```python
from pathlib import Path
from prometheus.research.microstructure import (
    AggTradesEligibilityGateInput,
    run_eligibility_gate,
)

inp = AggTradesEligibilityGateInput(
    manifest_path=Path("data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json"),
    output_root=Path("data/microstructure/gate-reports"),
    code_commit_sha="aa612ba2778c97a5150b80064244b90d024bfa54",
    write_report=True,
    write_successor_manifest=False,
)
result = run_eligibility_gate(inp)
```

`code_commit_sha` was set to the `main` HEAD at the start of Phase 4bb-D (`aa612ba2...`); the branch HEAD remained `aa612ba2...` until the post-execution documentation commit. `write_successor_manifest=False` is the only allowed value for raw families per Phase 4bb-C; setting `True` would have raised `AggTradesGateUnsupportedError` at construction.

The invocation was executed exactly once. No retry was needed and no overwrite or `RawWriterAlreadyExistsError` occurred.

---

## 7. Artefacts inspected

| Artefact | Path | Size (bytes) | SHA256 (pre-run) | SHA256 (post-run) | Identical? |
| -------- | ---- | -----------: | ---------------- | ----------------- | ---------- |
| Manifest | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json` | 1491 | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` | yes |
| Raw zip | `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip` | 21,271,119 | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | yes |
| Sidecar | `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256` | 100 | `b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d` | `b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d` | yes |
| Acquisition log | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001_acquisition_log.json` | 914 | `f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c` | `f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c` | yes |

The manifest `mtime_ns` was unchanged across the run (`1778187340311355300` before and after). All four artefacts are byte-identical pre- and post-invocation. The gate is read-only with respect to the Phase 4az dataset, as designed.

`data/microstructure/gate-reports/` did not exist before the run; it was created by the gate's atomic writer.

---

## 8. Gate report output path

| Item | Value |
| ---- | ----- |
| Report path (relative) | `data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json` |
| Sidecar path (relative) | `data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json.sha256` |
| Report size | 17,053 bytes |
| Sidecar size | 140 bytes |
| `git check-ignore -v` for `data/microstructure/` | `.gitignore:85:data/microstructure/` |
| `git check-ignore -v` for `data/microstructure/gate-reports/` | `.gitignore:85:data/microstructure/	data/microstructure/gate-reports/` |
| `git status` shows | both files are ignored, not tracked, not staged |

The report and sidecar are gitignored under the `data/microstructure/` rule from `.gitignore` line 85 (added by Phase 4aw).

The report path contains a doubled `gate-reports/` segment (`.../gate-reports/gate-reports/...`). That is observed Phase 4bb-C orchestrator behavior (the writer composes `output_root / "gate-reports" / filename`). Phase 4bb-D does not modify code; the doubled segment is recorded here as observed behavior. The path is fully gitignored regardless.

---

## 9. Gate report SHA256

| Item | Value |
| ---- | ----- |
| Sidecar contents (first 64 hex chars) | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| Recomputed SHA256 of report JSON | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| Match | yes |

The report's recomputed SHA256 is bit-for-bit identical to its paired sidecar.

---

## 10. Gate execution result

| Field | Value |
| ----- | ----- |
| `overall_status` | `pass` |
| `research_eligible_after` | `False` |
| `eligibility_gate_status_after` (recommendation only) | `pass` |
| `no_successor_authorization` | `True` |
| `len(checks)` | `45` |
| `len(invalid_window_candidates)` | `0` |
| `report_id` | `microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c` |
| `report_path` | `data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json` |

`overall_status = pass` does **not** authorize a transition of the actual manifest's `eligibility_gate_status` from `pending` to `pass`. Per Phase 4bb-B / Phase 4bb-C, any such transition would require a separately authorized successor-manifest phase that runs the gate with `write_successor_manifest=True` after explicit operator approval. Phase 4bb-D used `write_successor_manifest=False`. The actual manifest is unchanged.

`research_eligible_after = False` is the binding raw-family invariant set in Phase 4bb-C orchestrator code; PASS at the gate level does **not** flip this. Per Phase 4ba's staged eligibility ladder, `research_eligible = true` is reserved for Stage 3 (normalized derived family) only and never appears on a raw family.

### Boundary confirmations

All 13 Phase 4bb-C boundary confirmations were `true`:

| Key | Value |
| --- | ----- |
| `no_backtest_run` | `true` |
| `no_credential_read` | `true` |
| `no_data_microstructure_write_outside_gate_reports` | `true` |
| `no_env_read` | `true` |
| `no_feature_computed` | `true` |
| `no_manifest_mutation` | `true` |
| `no_mcp_or_graphify` | `true` |
| `no_ml_trained` | `true` |
| `no_network_io` | `true` |
| `no_normalization_written` | `true` |
| `no_strategy_created` | `true` |
| `no_websocket` | `true` |
| `research_eligible_after_is_false_for_raw_family` | `true` |

---

## 11. 45-check summary

All 45 checks ran and all 45 returned `pass`. There were no `FAIL`, `NOT_APPLICABLE`, or `ERROR` outcomes.

| Group (Phase 4ba §) | Count | PASS | FAIL | NOT_APPLICABLE | ERROR |
| ------------------- | -----:| ----:| ----:| --------------:| -----:|
| 10.1  source             | 5  | 5  | 0 | 0 | 0 |
| 10.2  checksum           | 3  | 3  | 0 | 0 | 0 |
| 10.3  manifest           | 5  | 5  | 0 | 0 | 0 |
| 10.4  schema             | 3  | 3  | 0 | 0 | 0 |
| 10.5  timestamps         | 4  | 4  | 0 | 0 | 0 |
| 10.6  monotonicity       | 3  | 3  | 0 | 0 | 0 |
| 10.7  duplicates         | 2  | 2  | 0 | 0 | 0 |
| 10.8  row count          | 3  | 3  | 0 | 0 | 0 |
| 10.9  symbol / date      | 4  | 4  | 0 | 0 | 0 |
| 10.10 archive integrity  | 4  | 4  | 0 | 0 | 0 |
| 10.11 invalid windows    | 4  | 4  | 0 | 0 | 0 |
| 10.12 cross-cutting      | 5  | 5  | 0 | 0 | 0 |
| **Total**                | **45** | **45** | **0** | **0** | **0** |

Per-check IDs returned by the orchestrator (in fixed order): `10.1.1`, `10.1.2`, `10.1.3`, `10.1.4`, `10.1.5`, `10.2.6`, `10.2.7`, `10.2.8`, `10.3.9`, `10.3.10`, `10.3.11`, `10.3.12`, `10.3.13`, `10.4.14`, `10.4.15`, `10.4.16`, `10.5.17`, `10.5.18`, `10.5.19`, `10.5.20`, `10.6.21`, `10.6.22`, `10.6.23`, `10.7.24`, `10.7.25`, `10.8.26`, `10.8.27`, `10.8.28`, `10.9.29`, `10.9.30`, `10.9.31`, `10.9.32`, `10.10.33`, `10.10.34`, `10.10.35`, `10.10.36`, `10.11.37`, `10.11.38`, `10.11.39`, `10.11.40`, `10.12.41`, `10.12.42`, `10.12.43`, `10.12.44`, `10.12.45`.

---

## 12. Failed / error / not-applicable check details

None. There were zero failing, zero error, and zero not-applicable check results.

---

## 13. Invalid-window candidate summary

The orchestrator returned `0` invalid-window candidates. The Phase 4az manifest's `invalid_windows` array is empty and, after the single-pass row scan, no per-row anomalies were observed (no schema validation failures, no duplicate aggregate IDs, no out-of-order aggregate IDs, no out-of-day timestamps, no zero/negative price or quantity, no impossible spread, no archive checksum mismatch, no retention gaps, no clock skew, no symbol mismatch). This is consistent with Phase 4bb-A's structural QA which found 21 / 21 checks PASS and zero new invalid windows.

---

## 14. Manifest / raw zip / sidecar immutability evidence

Pre-run and post-run SHA256 and size are identical for all four Phase 4az artefacts (manifest, raw zip, sidecar, acquisition log). See §7 for the full table. The manifest `mtime_ns` was unchanged across the run. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` method (which always raises) was not bypassed, and was not even imported by Phase 4bb-D code (Phase 4bb-D wrote no code).

The orchestrator additionally reported its own `manifest_sha_before`, `manifest_sha_after`, `raw_zip_sha_before`, `raw_zip_sha_after`, `sidecar_sha_before`, `sidecar_sha_after` in `result.measured_summary`; this is part of Phase 4bb-C's manifest-immutability hash-equality boundary check. If any pair had differed, the orchestrator would have forced `overall_status = FAIL`. It did not.

`data/microstructure/manifests/`, `data/microstructure/raw/`, and the on-disk Phase 4az files were not modified. The only file system effect of Phase 4bb-D under `data/microstructure/` is the creation of:

- `data/microstructure/gate-reports/gate-reports/` (new directory),
- one report JSON file in that directory,
- one paired SHA256 sidecar in that directory.

All three are gitignored.

---

## 15. Eligibility interpretation

Phase 4bb-D's gate run produced `overall_status = pass`. Per Phase 4ba and Phase 4bb-B, this means:

- the raw Phase 4az artefact has a PASS gate report;
- the raw manifest **remains** `research_eligible = false`;
- the raw manifest **remains** `eligibility_gate_status = pending` unless a separately authorized successor-manifest phase changes it;
- the PASS report does **not** authorize normalization;
- the PASS report does **not** authorize feature computation;
- the PASS report does **not** authorize ML training;
- the PASS report does **not** authorize strategy implementation;
- the PASS report does **not** authorize a backtest;
- the PASS report does **not** authorize additional acquisition;
- the PASS report does **not** authorize paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation.

PASS at Stage 1 (inspected) only signals that the artefact has cleared the structural eligibility-time floor. Movement to Stage 2 (gate-passed) requires a separately authorized phase that records the status transition; Phase 4bb-D was not that phase.

The recommended `eligibility_gate_status_after` field returned by the orchestrator is descriptive only: it indicates what the actual manifest's status *could* be set to in a future authorized phase, not what it *is*. The actual on-disk manifest still reads `eligibility_gate_status: pending`.

---

## 16. What this phase proves

- The Phase 4bb-C primitive is invocable by direct import on the real Phase 4az artefact set.
- The Phase 4bb-C primitive completes one full read-only run without mutating the manifest, the raw zip, the sidecar, or the acquisition log.
- The Phase 4bb-C primitive writes its report and paired SHA256 sidecar atomically under the gitignored `data/microstructure/gate-reports/` namespace and the report's recomputed SHA matches its sidecar bit-for-bit.
- All 45 Phase 4ba §10 checks succeed against the real Phase 4az archive (1,681,098 events; BTCUSDT 2025-01-15 UTC; raw-zip SHA `f560c2e5...`).
- The Phase 4bb-C boundary invariants hold under real-data invocation: `research_eligible_after = False`, `no_successor_authorization = True`, all 13 boundary confirmations `true`.
- The Phase 4bb-A structural QA result (21 / 21 PASS, zero invalid windows) is consistent with the gate's view of the same artefact: the gate observed zero invalid-window candidates.

---

## 17. What this phase does not prove

- That the Phase 4az dataset is **research-eligible**. It is not, by design. `research_eligible` remains `false`.
- That the Phase 4az dataset's `eligibility_gate_status` should be transitioned from `pending` to `pass` on the actual manifest.
- That normalization, feature computation, ML training, strategy work, backtests, paper/shadow, or live-readiness are now authorized. None of those are authorized.
- That the gate report itself is research evidence. It is a structural gate report, not a research finding.
- That any retained verdict (R3 baseline-of-record; R1a / R1b-narrow retained; R2 FAILED §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL; V2 / G1 / C1 HARD REJECT terminal; 5m thread CLOSED; H0 framework anchor) should be revised. None should be revised.
- That any project lock (§11.6, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6/§7/§8, Phase 4j §11, Phase 4ak M0 + post-null cooldown) should be relaxed. None should be relaxed.

---

## 18. Preserved boundaries

| Boundary | Preserved? | Evidence |
| -------- | :--------: | -------- |
| No source code change | yes | `git diff main..HEAD` shows zero source/test/script changes prior to docs commit |
| No test change | yes | same |
| No script change | yes | same |
| No data acquisition | yes | no network I/O at all; no Binance endpoint contact; no archive download |
| No data normalization | yes | no JSONL/Parquet/DuckDB written; no derived dataset created |
| No feature computation | yes | `no_feature_computed` boundary confirmation `true` |
| No ML / strategy / backtest | yes | `no_ml_trained`, `no_strategy_created`, `no_backtest_run` boundary confirmations `true` |
| No credential / `.env` / MCP / Graphify | yes | `no_credential_read`, `no_env_read`, `no_mcp_or_graphify` boundary confirmations `true` |
| No network / WebSocket | yes | `no_network_io`, `no_websocket` boundary confirmations `true` |
| No manifest mutation | yes | manifest SHA pre/post identical; mtime_ns unchanged |
| No raw / sidecar / acquisition-log mutation | yes | SHA pre/post identical for all three |
| No write outside gate-reports | yes | `no_data_microstructure_write_outside_gate_reports` boundary confirmation `true`; only `data/microstructure/gate-reports/...` was created |
| `research_eligible` for raw family stays false | yes | manifest read post-run shows `false`; orchestrator invariant enforced |
| `eligibility_gate_status` stays `pending` | yes | manifest read post-run shows `pending` |
| No successor authorized | yes | `no_successor_authorization = true`; this memo authorizes none |

---

## 19. Recommended future options

- **Primary — remain paused.** No successor phase is authorized by Phase 4bb-D.
- **Conditional next, only if the operator wants formal Stage-2 transition:** future docs-only **Phase 4bb-E — Gate-Report Interpretation / Successor-State Policy Memo**. This memo would define if and how the actual manifest's `eligibility_gate_status` may ever transition from `pending` to `pass` for raw families, what governance evidence is required, and whether `write_successor_manifest=True` is ever appropriate. Phase 4bb-E is **not** authorized by Phase 4bb-D.
- **Conditional alternative, also only after a Stage-2 policy is in place:** future docs-only **Phase 4bc — Normalization-Design Memo** (Phase 4ba Stage 3 reachability). Phase 4bc is **not** authorized by Phase 4bb-D.
- **Not recommended.** Acquiring more aggTrades data; flipping `research_eligible`; computing features; training ML; creating a strategy; running backtests; reopening the 5m research thread; rescuing R2 / F1 / D1-A / V2 / G1 / C1 / V1-arc; touching MCP / Graphify / `.mcp.json` / credentials.
- **Forbidden.** Verdict revision; lock revision; parameter optimization derived from Phase 4bb-D evidence; M0 amendment derived from Phase 4bb-D evidence; paper / shadow / live-readiness / deployment / production-key creation / authenticated APIs / private endpoints / public-endpoint calls in code / user stream / live WebSocket / exchange-write.

---

## 20. Closeout / lock preservation

Phase 4bb-D preserves every retained verdict and project lock verbatim:

- H0 FRAMEWORK ANCHOR;
- R3 BASELINE-OF-RECORD;
- R1a / R1b-narrow RETAINED — NON-LEADING;
- R2 FAILED — §11.6;
- F1 HARD REJECT;
- D1-A MECHANISM PASS / FRAMEWORK FAIL;
- 5m thread OPERATIONALLY CLOSED per Phase 3t;
- V2 HARD REJECT — terminal for V2 first-spec;
- G1 HARD REJECT — terminal for G1 first-spec;
- C1 HARD REJECT — terminal for C1 first-spec;
- §11.6 = 8 bps per side preserved verbatim; round-trip = 16 bps;
- §1.7.3 0.25% / 2× / one-position / mark-price stops;
- Phase 3p §4.7 strict integrity gate (aggTrades equivalent applied verbatim by Phase 4az; reaffirmed by Phase 4ba; structural QA confirmed by Phase 4bb-A; execution plan mapped by Phase 4bb-B; primitive implemented by Phase 4bb-C; primitive run by Phase 4bb-D);
- Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8;
- Phase 4j §11;
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template;
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy;
- Phase 4am, 4an, 4ao, 4ap, 4aq, 4ar, 4as, 4at, 4au, 4av, 4aw, 4ax, 4ay, 4az, 4ba, 4bb-A, 4bb-B, 4bb-C results — all preserved verbatim.

The Phase 4az dataset's eligibility flags are unchanged: `research_eligible` remains `false`, `eligibility_gate_status` remains `pending`. **Phase 4 (canonical), Phase 4bb-E, Phase 4bc, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, public-endpoint calls in code, user stream, live WebSocket implementation, MCP, Graphify, `.mcp.json`, credentials, and additional aggTrades / 5m / 1m / tick / mark-price 30m / 4h / order-book data acquisition all remain unauthorized.**

**Recommended state: remain paused. No next phase authorized.**
