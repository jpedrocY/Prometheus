# Phase 4be — Merge Closeout

**Phase identity:** Phase 4be — AggTrades Normalized Dataset Structural QA Memo.
**Type:** docs-and-local-gitignored-output structural QA inspection.
**Action:** merge into `main`.
**Date:** 2026-05-07.
**Merge purpose:** bring the Phase 4be structural QA memo, closeout, and narrow `current-project-state.md` update onto `main`, so the 60-check structural QA result over the Phase 4bd Stage-0 derived aggTrades artefacts becomes part of the project history. No source / test / script / config / data / manifest / gate-report change is brought forward; local Stage-0 outputs under `data/microstructure/` remain gitignored and are not committed.

---

## 1. Branches

| Item | Value |
| ---- | ----- |
| Target branch | `main` |
| Source branch | `phase-4be/aggtrades-normalized-structural-qa` |

## 2. SHAs

| Item | Value |
| ---- | ----- |
| `main` SHA before merge | `e1734485b82c080f7ff1805ee20b0431bb3144e4` |
| Phase 4be commit SHA | `7a45ea33eee2fe4bb07f0c47c3407fdd5145a6de` |
| Merge commit SHA | `273e30d5041d9abc5e5d80466f367a415650f515` |
| `main` / `origin/main` SHA after push | `273e30d5041d9abc5e5d80466f367a415650f515` |
| Merge method | `--no-ff`, `ort` strategy |

---

## 3. Files brought forward by the merge

**Docs only (3):**

- `docs/00-meta/implementation-reports/2026-05-07_phase-4be_aggtrades-normalized-structural-qa.md` (new; 24-section structural QA memo with 60-row check table)
- `docs/00-meta/implementation-reports/2026-05-07_phase-4be_closeout.md` (new)
- `docs/00-meta/current-project-state.md` (Phase 4be narrative paragraph + new `Current phase:` block; prior Phase 4bd block preserved as historical context)

**Total diff summary from the Phase 4be merge:**

```text
3 files changed, 727 insertions(+)
```

No source code, tests, scripts, configs, README, pyproject, `.gitignore`, M0 governance, strategy specs, validation checklists, phase-gates, runtime docs, MCP files, credentials, data files, or manifest files were brought forward.

---

## 4. Structural QA result

```text
Total checks:   60
PASS:           60
FAIL:            0
ERROR:           0
NOT_APPLICABLE:  0
```

The Phase 4bd Stage-0 normalized artefacts are **structurally QA-passed**. This QA result does not transition any stage and does not flip any eligibility flag.

---

## 5. Local gitignored Stage-0 artefacts inspected

```text
data/microstructure/normalized/microstructure_normalized_aggtrades_v001/
    BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet
    Normalized Parquet SHA256:
        2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa
data/microstructure/normalized/microstructure_normalized_aggtrades_v001/
    BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet.sha256
data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json
    Derived manifest SHA256:
        f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9
data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json.sha256
```

All four local outputs are gitignored under `.gitignore:85: data/microstructure/` and are **not** committed. `git check-ignore -v data/microstructure/` and `git check-ignore -v data/microstructure/normalized/` both confirm coverage by the same `.gitignore` rule.

---

## 6. Inspection conclusions

- Parquet schema exactly matches the 19-column Phase 4bc canonical schema (`dataset_family`, `dataset_version`, `source_dataset_family`, `source_dataset_version`, `symbol`, `utc_date`, `agg_trade_id`, `price`, `quantity`, `first_trade_id`, `last_trade_id`, `transact_time_ms`, `is_buyer_maker`, `source_file_sha256`, `source_manifest_sha256`, `source_gate_report_id`, `source_gate_report_sha256`, `row_index`, `normalization_schema_version`).
- No extra columns.
- No feature / label / signal / proxy / return / alpha / edge / imbalance / sweep / spread / depth / liquidity / slippage / order-flow / execution-quality / ML / strategy columns.
- Row count = **1,681,098**.
- Derived manifest `event_count` = **1,681,098**.
- `row_index` is contiguous `0..1,681,097`.
- `row_index` has no duplicates.
- `agg_trade_id` has no duplicates (1,681,098 unique values).
- `agg_trade_id` is non-decreasing.
- First row matches recorded raw values: `agg_trade_id=2516301323`, `transact_time_ms=1736899205109`, `price='96514.9'`, `quantity='0.091'`, `is_buyer_maker=True`, `row_index=0`.
- Last row matches recorded raw values: `agg_trade_id=2517982420`, `transact_time_ms=1736985599991`, `price='100460.0'`, `quantity='0.059'`, `is_buyer_maker=True`, `row_index=1681097`.
- All `transact_time_ms` values fall inside the half-open UTC day `[2025-01-15T00:00:00.000Z, 2025-01-16T00:00:00.000Z)`.
- `price` and `quantity` are stored as Arrow `string` (Decimal-parsable; not float).
- `is_buyer_maker` is strict Arrow `bool`.
- Per-row lineage columns are constant and correct (raw zip SHA, raw manifest SHA, gate report ID, gate report SHA, dataset family / version, source dataset family / version, symbol, utc_date, normalization schema version).
- Derived manifest `dataset_family = microstructure_normalized_aggtrades_v001`.
- Derived manifest `version = v001`.
- Derived manifest `symbol = BTCUSDT`.
- Derived manifest `file_count = 1`.
- Derived manifest `files[*].sha256` = normalized Parquet SHA `2b3d6978...`.
- Derived manifest `research_eligible = false`.
- Derived manifest `eligibility_gate_status = pending`.
- Derived manifest `governance_labels.feature_computation = forbidden`.
- Derived manifest `governance_labels.strategy_use = forbidden`.
- Derived manifest references Phase 4bb-D report ID and SHA correctly.
- Derived manifest references source raw zip SHA and raw manifest SHA correctly.
- Derived manifest `invalid_windows = []`.

---

## 7. Immutability evidence

Pre/post SHAs are byte-for-byte identical for all five raw / governance artefacts:

```text
raw manifest          a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201   IDENTICAL
raw zip               f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e   IDENTICAL
sidecar               b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d   IDENTICAL
acquisition log       f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c   IDENTICAL
Phase 4bb-D gate      96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423   IDENTICAL
```

The original Phase 4az raw manifest still has `research_eligible=false` and `eligibility_gate_status=pending`. The derived manifest still has `research_eligible=false` and `eligibility_gate_status=pending`. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved.

---

## 8. Stage interpretation

- Phase 4bd Stage-0 normalized artefacts are **structurally QA-passed**.
- No formal Stage-2 gate-passed transition is authorized.
- No Stage-3 research eligibility is authorized or reached.
- No Stage-4 feature-cleared status is authorized.
- No feature, ML, strategy, backtest, or acquisition is authorized.

---

## 9. Validation results (post-merge on `main`)

| Check | Result |
| ----- | ------ |
| `pytest tests/research/microstructure/` | 333 passed in 3.57s |
| `pytest` (whole repo) | 1116 passed, 2 failed — failures are **only** the two known pre-existing simulation failures `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt` (`KeyError: 'trade_count'` in `src/prometheus/research/data/storage.py:232`); zero new regressions from Phase 4be |
| `ruff check src/prometheus/research/microstructure tests/research/microstructure` | All checks passed |
| `ruff check .` | All checks passed |
| `mypy src/prometheus/research/microstructure` | Success: no issues found in 15 source files |
| `mypy src/prometheus` (strict, whole project) | Success: no issues found in 97 source files |
| `git diff --check` | clean |
| `git check-ignore -v data/microstructure/` | `.gitignore:85:data/microstructure/	data/microstructure/` |
| `git check-ignore -v data/microstructure/normalized/` | `.gitignore:85:data/microstructure/	data/microstructure/normalized/` |

---

## 10. Boundary confirmations

- No source code change.
- No test change.
- No script change.
- No config change.
- No `README` change.
- No `pyproject` change.
- No `.gitignore` change.
- No M0 governance change.
- No data acquisition.
- No public endpoint calls.
- No Binance API calls.
- No WebSocket.
- No credential / `.env` / `.mcp.json` / MCP / Graphify.
- No normalizer rerun.
- No raw gate rerun.
- No new gate report.
- No feature computation.
- No labels.
- No strategy signals.
- No ML.
- No strategy.
- No backtest.
- No tracked `data/microstructure/` output.
- No mutation of normalized artefacts.
- No mutation of raw artefacts.
- No mutation of Phase 4bb-D gate report.
- Raw-family `research_eligible` remains `false`.
- Raw-family `eligibility_gate_status` remains `pending`.
- Derived-family `research_eligible` remains `false`.
- Derived-family `eligibility_gate_status` remains `pending`.
- No retained verdict revised.
- No project lock loosened.
- No M0 amendment.
- No successor authorized.

---

## 11. Retained verdict ledger

- H0 — FRAMEWORK ANCHOR
- R3 — BASELINE-OF-RECORD
- R1a — RETAINED — NON-LEADING
- R1b-narrow — RETAINED — NON-LEADING
- R2 — FAILED — §11.6
- F1 — HARD REJECT
- D1-A — MECHANISM PASS / FRAMEWORK FAIL
- 5m thread — OPERATIONALLY CLOSED
- V2 — HARD REJECT — terminal for V2 first-spec
- G1 — HARD REJECT — terminal for G1 first-spec
- C1 — HARD REJECT — terminal for C1 first-spec

---

## 12. Preserved project locks

- §11.6 = 8 bps per side (round-trip = 16 bps).
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops.
- Phase 3p §4.7 strict integrity gate.
- Phase 3r §8.
- Phase 3v §8.
- Phase 3w §6 / §7 / §8.
- Phase 4j §11.
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template.
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy.
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd results — preserved.

---

## 13. No-rescue constraints

Phase 4be does not loosen, amend, supersede, or redefine any retained verdict, project lock, governance memo, or M0 clause. No rescue path is opened. Specifically:

- no R3 / R3-prime;
- no R1a-prime / R1b-narrow-prime;
- no R2-prime;
- no F1-prime;
- no D1-A-prime / D1-B / V1-D1 / F1-D1;
- no V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- no G1-prime / G1-narrow / G1-extension / G1 hybrid;
- no C1-prime / C1-narrow / C1-extension / C1 hybrid;
- no cross-strategy hybrid;
- no reopening of the 5m research thread;
- no flipping of `research_eligible` to `true` on any raw or derived aggTrades family.

---

## 14. Successor authorization

- No Phase 4bf-A authorized.
- No Phase 4bf authorized.
- No Phase 4bg authorized.
- No Phase 4bb-F authorized.
- No Phase 4bb-G authorized.
- No Phase 5 authorized.
- No Phase 4 canonical authorized.
- No additional acquisition.
- No Stage-2 gate-passed transition.
- No Stage-3 research eligibility.
- No Stage-4 feature-cleared status.
- No features.
- No labels.
- No ML.
- No strategy.
- No backtest.
- No paper / shadow.
- No live-readiness.
- No deployment.
- No exchange-write.
- No production keys.
- No authenticated APIs.
- No private endpoints.
- No user stream.
- No MCP / Graphify / `.mcp.json` / credentials.

---

## 15. Recommended state

**Remain paused.** A future docs-only Phase 4bf-A derived-family eligibility-gate design memo, a Phase 4bb-F gate-report output-path hygiene memo, and a Phase 4bb-G raw-manifest successor-state recording memo all remain available as separately authorized next steps. None is authorized by Phase 4be or by this merge.
