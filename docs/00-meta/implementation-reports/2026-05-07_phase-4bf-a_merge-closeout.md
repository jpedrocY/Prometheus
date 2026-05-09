# Phase 4bf-A — Merge Closeout

**Phase identity:** Phase 4bf-A — AggTrades Derived-Family Eligibility-Gate Design Memo.
**Type:** docs-only derived-family eligibility-gate design memo.
**Action:** merge into `main`.
**Date:** 2026-05-07.
**Merge purpose:** bring the Phase 4bf-A docs-only design memo, closeout, and narrow `current-project-state.md` update onto `main`, so the predeclared future derived-family eligibility-gate design (14 check groups; 55 stable check IDs `4bf.13.1`..`4bf.13.55`; 18 fail-closed rules; future module layout, test plan, public API, and 20 acceptance criteria) becomes part of the project history. No source / test / script / config / data / manifest / gate-report change is brought forward; no gate is run; no Stage transition; no successor authorized.

---

## 1. Branches

| Item | Value |
| ---- | ----- |
| Target branch | `main` |
| Source branch | `phase-4bf-a/aggtrades-derived-eligibility-gate-design` |

## 2. SHAs

| Item | Value |
| ---- | ----- |
| `main` SHA before merge | `2bfe65f0e48ac6ba5ffd3eaf3ee388a2cb4dc1da` |
| Phase 4bf-A commit SHA | `63227b5acd138444a72b694a6f5adc2537f101df` |
| Merge commit SHA | `6c0ea2713e703c47f515e2987187685889197d9a` |
| `main` / `origin/main` SHA after push | `6c0ea2713e703c47f515e2987187685889197d9a` |
| Merge method | `--no-ff`, `ort` strategy |

---

## 3. Files brought forward by the merge

**Docs only (3):**

- `docs/00-meta/implementation-reports/2026-05-07_phase-4bf-a_aggtrades-derived-family-eligibility-gate-design.md` (new; 27-section design memo with the §17 55-row check enumeration)
- `docs/00-meta/implementation-reports/2026-05-07_phase-4bf-a_closeout.md` (new)
- `docs/00-meta/current-project-state.md` (Phase 4bf-A narrative paragraph + new `Current phase:` block; prior Phase 4be block preserved as historical context)

**Total diff summary from the Phase 4bf-A merge:**

```text
3 files changed, 944 insertions(+)
```

No source code, tests, scripts, configs, README, pyproject, `.gitignore`, M0 governance, strategy specs, validation checklists, phase-gates, runtime docs, MCP files, credentials, data files, manifest files, or gate reports were brought forward.

---

## 4. Design result

```text
Type:                 docs-only design memo
Stage transition:     none
Gate executions:      none
Gate reports created: none
Code changes:         none
Test changes:         none
Data changes:         none
Manifest changes:     none
Successor authorized: none
```

---

## 5. Key design conclusions

- **Target family:** `microstructure_normalized_aggtrades_v001`.
- **Future gate inputs:** local artefacts only (derived manifest + sidecar; normalized Parquet + sidecar; raw manifest + raw zip + sidecar + acquisition log; Phase 4bb-D PASS gate report; Phase 4be QA + closeout + merge-closeout files; future Phase 4bf code commit SHA).
- **Future gate output path:** `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v001__<unix_ms>__<short_commit>.json` (gitignored under `.gitignore:85`) plus paired `.sha256`.
- **Future gate report must be gitignored and not committed.**
- **Future gate must refuse overwrite** at writer level (atomic write-then-rename).
- **Future gate must not mutate the existing derived manifest** (`data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json`).
- **Future gate may recommend `eligibility_gate_status_after = pass` or `fail` at report level only;** it must not write that status to the actual derived manifest.
- **Future gate must keep `research_eligible_after = False`** (invariant for derived-family gate).
- **Future gate must keep `no_successor_authorization = True`** (invariant).
- **Stage-3 research eligibility is not reachable from the gate alone.** It requires Phase 4bg-A (or equivalent) and additional governance (Phase 4be evidence; governed invalid-window treatment; raw PASS gate lineage; explicit operator authorization; M0-compatible research-use memo; feature-boundary design; no project lock revision; no retained verdict revision).
- **Future Phase 4bf implementation must implement exactly 55 stable checks**, IDs `4bf.13.1` through `4bf.13.55`.
- **Future Phase 4bf test plan calls for at least 150 tests** (≥ 110 from 1 PASS + 1 FAIL per check; ≥ 15 I/O; ≥ 6 report; ≥ 12 end-to-end; ≥ 8 static no-network).

---

## 6. Future check groups

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

## 7. Future proposed source modules

```text
src/prometheus/research/microstructure/derived_gate_io.py
src/prometheus/research/microstructure/derived_gate_checks.py
src/prometheus/research/microstructure/derived_gate_report.py
src/prometheus/research/microstructure/derived_gate.py
src/prometheus/research/microstructure/__init__.py    # narrow re-export update only
```

No new `scripts/...` entrypoint. No new dependency.

## 8. Future proposed test modules

```text
tests/research/microstructure/_derived_gate_fixtures.py
tests/research/microstructure/test_derived_gate_io.py
tests/research/microstructure/test_derived_gate_checks.py
tests/research/microstructure/test_derived_gate_report.py
tests/research/microstructure/test_derived_gate.py
tests/research/microstructure/test_derived_gate_no_network.py
```

## 9. Future proposed public API

```text
DerivedAggTradesGateInput
DerivedAggTradesGateResult
DerivedAggTradesCheckResult
DerivedAggTradesGateReport
DerivedAggTradesCheckStatus
DerivedAggTradesGateInputError
DerivedAggTradesGateUnsupportedError
GateIOError
run_derived_aggtrades_gate
```

These are proposed future names only. Phase 4bf-A does not implement any of them.

---

## 10. Local gitignored artefact state at merge time

- normalized Parquet path: `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet`
- normalized Parquet SHA256: `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa`
- derived manifest path: `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json`
- derived manifest SHA256: `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9`
- raw manifest SHA256: `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201`
- raw zip SHA256: `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`
- Phase 4bb-D gate report SHA256: `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`

Confirmations:

- normalized artefacts remain gitignored and **not committed**.
- derived manifest remains gitignored and **not committed**.
- **no new gate report exists** from Phase 4bf-A (no gate was run).

---

## 11. Manifest state

| Field | Raw | Derived |
| ----- | --- | ------- |
| `research_eligible` | `false` | `false` |
| `eligibility_gate_status` | `pending` | `pending` |

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant remains preserved.

---

## 12. Validation results (post-merge on `main`)

| Check | Result |
| ----- | ------ |
| `pytest tests/research/microstructure/` | 333 passed in 3.84s |
| `pytest` (whole repo) | 1116 passed, 2 failed — failures are **only** the two known pre-existing simulation failures `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt` (`KeyError: 'trade_count'` in `src/prometheus/research/data/storage.py:232`); zero new regressions from Phase 4bf-A |
| `ruff check .` | All checks passed |
| `mypy src/prometheus` (strict, whole project) | Success: no issues found in 97 source files |
| `git diff --check` | clean |
| `git check-ignore -v data/microstructure/` | `.gitignore:85:data/microstructure/	data/microstructure/` |
| `git check-ignore -v data/microstructure/normalized/` | `.gitignore:85:data/microstructure/	data/microstructure/normalized/` |

---

## 13. Boundary confirmations

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
- No derived gate run.
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

## 14. Retained verdict ledger

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

## 15. Preserved project locks

- §11.6 = 8 bps per side (round-trip = 16 bps).
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops.
- Phase 3p §4.7 strict integrity gate.
- Phase 3r §8.
- Phase 3v §8.
- Phase 3w §6 / §7 / §8.
- Phase 4j §11.
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template.
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy.
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd / 4be results — preserved.

---

## 16. No-rescue constraints

Phase 4bf-A does not loosen, amend, supersede, or redefine any retained verdict, project lock, governance memo, or M0 clause. No rescue path is opened. Specifically:

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

## 17. Successor authorization

- No Phase 4bf authorized.
- No Phase 4bg authorized.
- No Phase 4bg-A authorized.
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

## 18. Recommended state

**Remain paused.** A future docs-and-code Phase 4bf gate implementation + execution memo, a Phase 4bg-A derived-family research-eligibility decision memo (after a Stage-2 PASS report), a Phase 4bb-F gate-report output-path hygiene memo, and a Phase 4bb-G raw-manifest successor-state recording memo all remain available as separately authorized next steps. None is authorized by Phase 4bf-A or by this merge.
