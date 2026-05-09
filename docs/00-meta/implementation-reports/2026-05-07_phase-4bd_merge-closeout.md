# Phase 4bd — Merge Closeout

**Phase identity:** Phase 4bd — AggTrades Normalization Implementation.
**Type:** docs-and-code Stage-0 derived normalization implementation.
**Action:** merge into `main`.
**Date:** 2026-05-07.
**Merge purpose:** bring the Phase 4bd offline aggTrades normalizer (4 source modules + narrow `__init__.py` re-export update + 1 fixture builder + 5 test files + 2 memo files + 1 narrow `current-project-state.md` update) onto `main`, so the Phase 4bd implementation and its real Phase 4az run record become part of the project history. Local Stage-0 derived outputs under `data/microstructure/` remain gitignored and are not committed.

---

## 1. Branches

| Item | Value |
| ---- | ----- |
| Target branch | `main` |
| Source branch | `phase-4bd/aggtrades-normalization-implementation` |

## 2. SHAs

| Item | Value |
| ---- | ----- |
| `main` SHA before merge | `71548e2f47c797991aa05c2f190425812e4e15a4` |
| Phase 4bd commit SHA | `403b6df23c98a35770aa177ad4ccba3e74786613` |
| Merge commit SHA | `d4a68940a126eef4388bee960496c4ae2275b04e` |
| `main` / `origin/main` SHA after push | `d4a68940a126eef4388bee960496c4ae2275b04e` |
| Merge method | `--no-ff`, `ort` strategy |

---

## 3. Files brought forward by the merge

**Source (5):**

- `src/prometheus/research/microstructure/normalize_io.py` (new)
- `src/prometheus/research/microstructure/normalize_aggtrades.py` (new)
- `src/prometheus/research/microstructure/normalize_manifest.py` (new)
- `src/prometheus/research/microstructure/normalize_validation.py` (new)
- `src/prometheus/research/microstructure/__init__.py` (narrow update; 14 new public symbols re-exported; docstring extended; no prior export removed)

**Tests (6):**

- `tests/research/microstructure/_normalize_fixtures.py` (new fixture builder)
- `tests/research/microstructure/test_normalize_io.py` (new; 17 tests)
- `tests/research/microstructure/test_normalize_aggtrades.py` (new; 22 tests)
- `tests/research/microstructure/test_normalize_manifest.py` (new; 14 tests)
- `tests/research/microstructure/test_normalize_validation.py` (new; 7 tests)
- `tests/research/microstructure/test_normalize_no_network.py` (new; 11 tests)

**Docs (3):**

- `docs/00-meta/implementation-reports/2026-05-07_phase-4bd_aggtrades-normalization-implementation.md` (new)
- `docs/00-meta/implementation-reports/2026-05-07_phase-4bd_closeout.md` (new)
- `docs/00-meta/current-project-state.md` (Phase 4bd narrative paragraph + new `Current phase:` block; prior Phase 4bd-A block preserved as historical context)

**Total diff summary from the Phase 4bd merge:**

```text
14 files changed, 4313 insertions(+)
```

---

## 4. Implementation result

- 4 new source modules implemented (`normalize_io.py`, `normalize_aggtrades.py`, `normalize_manifest.py`, `normalize_validation.py`).
- Narrow `__init__.py` re-export update; 14 new public symbols exported (`NORMALIZATION_SCHEMA_VERSION`, `NORMALIZED_SCHEMA_V001`, `NormalizedAggTradeRow`, `NormalizationLineage`, `NormalizationCheckResult`, `NormalizationCheckStatus`, `NormalizationValidationResult`, `NormalizationValidationError`, `NormalizationManifestDraft`, `NormalizationManifestError`, `NormalizationIOError`, `NormalizeAggTradesInput`, `NormalizeAggTradesResult`, `run_normalize_aggtrades`).
- 1 shared fixture builder added (`_normalize_fixtures.py`).
- 5 `normalize_*` test files added.
- 71 new Phase 4bd tests; all pass.
- 27 Phase 4bc normalization checks implemented as the `CHECK_ORDER` tuple `4bc.24.1`..`4bc.24.27` in `normalize_validation.py`.
- Normalizer real run returned `overall_status=pass`.
- Real-run validation checks: **27 / 27 PASS** (writes enabled; 0 FAIL / 0 NOT_APPLICABLE / 0 ERROR).
- Output `event_count` = 1,681,098.
- `invalid_window_candidates` = 0.
- `research_eligible_after` = `False`.
- `no_successor_authorization` = `True`.

---

## 5. Local gitignored Stage-0 derived outputs

```text
data/microstructure/normalized/microstructure_normalized_aggtrades_v001/
    BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet
    Parquet SHA256: 2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa
    Size: 16,145,742 bytes
data/microstructure/normalized/microstructure_normalized_aggtrades_v001/
    BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet.sha256
data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json
    Derived manifest SHA256: f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9
    Size: 2,172 bytes
data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json.sha256
```

All four local outputs are gitignored under `.gitignore:85: data/microstructure/` and are **not** committed. `git check-ignore -v data/microstructure/normalized/` and `git check-ignore -v data/microstructure/` both confirm coverage by the same `.gitignore` rule.

---

## 6. Derived manifest state

| Field | Value |
| ----- | ----- |
| `dataset_family` | `microstructure_normalized_aggtrades_v001` |
| `version` | `v001` |
| `symbol` | `BTCUSDT` |
| `event_count` | 1,681,098 |
| `file_count` | 1 |
| `research_eligible` | `false` |
| `eligibility_gate_status` | `pending` |
| `source_gate_report_id` | `microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c` |
| `source_gate_report_sha256` | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| `source_gate_report_code_commit_sha` | `aa612ba2778c97a5150b80064244b90d024bfa54` |
| `feature_computation` | `forbidden` |
| `strategy_use` | `forbidden` |

---

## 7. Stage-0 interpretation

- Phase 4bd produced **Stage-0 derived artefacts only**.
- Stage-1 (inspection) is **not authorized**.
- Stage-2 (gate-passed transition) is **not authorized**.
- Stage-3 (research eligibility) is **not authorized and not reached**.
- Stage-4 (feature-cleared status) is **not authorized**.
- No feature, ML, strategy, backtest, or acquisition is authorized.

The derived family `microstructure_normalized_aggtrades_v001` carries `research_eligible=false` and `eligibility_gate_status=pending`. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end.

---

## 8. Immutability evidence

Pre/post SHAs are byte-for-byte identical for all five raw / governance artefacts:

```text
raw manifest          a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201   IDENTICAL
raw zip               f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e   IDENTICAL
sidecar               b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d   IDENTICAL
acquisition log       f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c   IDENTICAL
Phase 4bb-D gate      96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423   IDENTICAL
```

The original Phase 4az manifest still has `research_eligible=false` and `eligibility_gate_status=pending`.

---

## 9. Validation results (post-merge on `main`)

| Check | Result |
| ----- | ------ |
| Targeted Phase 4bd tests (5 files) | 71 passed in 0.58s |
| `pytest tests/research/microstructure/` | 333 passed in 3.67s — Phase 4aw 114 + Phase 4ax 47 + Phase 4az 35 + Phase 4bb-C 62 + Phase 4bd 71 = 329 distinct file totals; the additional +4 versus the figure recorded in the Phase 4bd memo (329) comes from `test_import_boundaries.py` parametrize automatically picking up the 4 new `normalize_*.py` modules |
| `pytest` (whole repo) | 1116 passed, 2 failed — failures are **only** the two known pre-existing simulation failures `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt` (`KeyError: 'trade_count'` in `src/prometheus/research/data/storage.py:232`); zero new regressions from Phase 4bd |
| `ruff check src/prometheus/research/microstructure tests/research/microstructure` | All checks passed |
| `ruff check .` | All checks passed |
| `mypy src/prometheus/research/microstructure` | Success: no issues found in 15 source files |
| `mypy src/prometheus` (strict, whole project) | Success: no issues found in 97 source files (was 93 prior to Phase 4bd; +4 new `normalize_*.py` modules) |
| `git diff --check` | clean |
| `git check-ignore -v data/microstructure/` | `.gitignore:85:data/microstructure/	data/microstructure/` |
| `git check-ignore -v data/microstructure/normalized/` | `.gitignore:85:data/microstructure/	data/microstructure/normalized/` |

---

## 10. Boundary confirmations

- No script change.
- No config change.
- No `.gitignore` change.
- No `README` change.
- No `pyproject` change.
- No M0 governance change.
- No data acquisition.
- No public endpoint calls.
- No Binance API calls.
- No WebSocket.
- No credential / `.env` / `.mcp.json` / MCP / Graphify.
- No feature computation.
- No labels.
- No strategy signals.
- No ML.
- No strategy.
- No backtest.
- No tracked `data/microstructure/` output.
- Original Phase 4az raw manifest unchanged.
- Phase 4az raw zip unchanged.
- Phase 4az raw sidecar unchanged.
- Phase 4az acquisition log unchanged.
- Phase 4bb-D gate report unchanged.
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
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A results — preserved.

---

## 13. No-rescue constraints

Phase 4bd does not loosen, amend, supersede, or redefine any retained verdict, project lock, governance memo, or M0 clause. No rescue path is opened by Phase 4bd. Specifically:

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

- No Phase 4be authorized.
- No Phase 4bf authorized.
- No Phase 4bb-F authorized.
- No Phase 4bb-G authorized.
- No Phase 5 authorized.
- No Phase 4 canonical authorized.
- No additional acquisition.
- No Stage-1 inspection.
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

**Remain paused.** A future docs-only Phase 4be derived-family eligibility-gate memo, a Phase 4bb-F original-manifest-aware successor-state companion memo, and a Phase 4bb-G `gate-reports/gate-reports/` doubled-path correction memo all remain available as separately authorized next steps. None is authorized by Phase 4bd or by this merge.
