# Phase 4bf — Merge Closeout

**Phase identity:** Phase 4bf — AggTrades Derived-Family Eligibility-Gate Implementation and Execution.
**Date:** 2026-05-10.
**Branch merged:** `phase-4bf/aggtrades-derived-eligibility-gate`.
**Phase 4bf source commit:** `6530fb2 feat(phase-4bf): implement derived aggtrades eligibility gate`.
**Base of merge (`MAIN_BEFORE`):** `29e3f550e28ef4507fc7d008d2df9d53a46d52d8` (Phase 4bf-A merge-closeout commit).
**Merge commit (`MAIN_AFTER`):** `cad383cd5e85dae6b96fa83650d211842d5e070f` (`feat(phase-4bf): merge derived aggtrades eligibility gate`).
**Push:** `origin/main` advanced from `29e3f55` → `cad383c`.
**Status:** merged; pending operator review of this closeout.

---

## 1. Summary

Phase 4bf is now merged into `main`. The merge brings the offline derived-family eligibility gate online and records its first and only authorized execution against the Phase 4bd / Phase 4be normalized aggTrades artefacts. The merge does not change any retained verdict, project lock, governance memo, or M0 admissibility rule, and does not authorize any successor phase.

Real-run result remains `overall_status=pass` with **55 / 55 PASS** validation checks, `research_eligible_after=False`, `no_successor_authorization=True`, all 15 boundary confirmations `True`, and zero pre/post mutation of any input artefact.

---

## 2. Files added by the merge

**Source (5; 4 new + 1 narrow update):**

- `src/prometheus/research/microstructure/derived_gate_io.py` (new; 261 lines)
- `src/prometheus/research/microstructure/derived_gate_report.py` (new; 113 lines)
- `src/prometheus/research/microstructure/derived_gate_checks.py` (new; 786 lines)
- `src/prometheus/research/microstructure/derived_gate.py` (new; 327 lines)
- `src/prometheus/research/microstructure/__init__.py` (narrow update; 8 new public symbols re-exported; docstring extended)

**Tests (6; 1 fixture builder + 5 test files):**

- `tests/research/microstructure/_derived_gate_fixtures.py`
- `tests/research/microstructure/test_derived_gate_io.py` (18 tests)
- `tests/research/microstructure/test_derived_gate_report.py` (7 tests)
- `tests/research/microstructure/test_derived_gate_checks.py` (107 tests)
- `tests/research/microstructure/test_derived_gate.py` (13 tests)
- `tests/research/microstructure/test_derived_gate_no_network.py` (8 parametrized tests; 4 modules × 2 scans)

**Docs (3):**

- `docs/00-meta/implementation-reports/2026-05-07_phase-4bf_aggtrades-derived-family-eligibility-gate.md`
- `docs/00-meta/implementation-reports/2026-05-07_phase-4bf_closeout.md`
- `docs/00-meta/implementation-reports/2026-05-10_phase-4bf_merge-closeout.md` (this file)

Plus the narrow Phase 4bf paragraph + new `Current phase:` block in `docs/00-meta/current-project-state.md`. The Phase 4bf-A block was preserved as historical context.

No source/test/script/data/manifest outside the listed paths was modified by Phase 4bf or by this merge. `.gitignore` was unchanged. `pyproject.toml` was unchanged. `README.md` was unchanged. No `scripts/...` entrypoint was added.

---

## 3. Pre-merge verification

| Check | Result |
| ----- | ------ |
| Branch at start of merge step | `phase-4bf/aggtrades-derived-eligibility-gate` |
| Phase 4bf source commit | `6530fb2` (clean working tree; only `.claude/scheduled_tasks.lock` and `data/research/` untracked, both gitignore-covered) |
| Source / test / docs all tracked | yes (verified via `git ls-files`) |
| `git check-ignore -v data/microstructure/gate-reports/normalized/` | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/research/` | `.gitignore:89: data/research/` |
| Local Phase 4bf gate report present | `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e.json` (16,518 B) |
| Local Phase 4bf gate-report sidecar present | `microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e.json.sha256` (147 B) |
| Gate-report SHA256 (recomputed vs sidecar) | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` — match |
| Derived manifest `research_eligible` / `eligibility_gate_status` | `false` / `pending` |
| Raw manifest `research_eligible` / `eligibility_gate_status` | `false` / `pending` |
| `main` synchronized with `origin/main` before merge | yes (`29e3f55` on both) |
| Phase 4bf-A merge commit ancestor of main | `git merge-base --is-ancestor 6c0ea2713e703c47f515e2987187685889197d9a main` → true |
| `docs/00-meta/implementation-reports/2026-05-07_phase-4bf-a_merge-closeout.md` present on main | yes |
| `MAIN_BEFORE` | `29e3f550e28ef4507fc7d008d2df9d53a46d52d8` |

---

## 4. Pre-merge SHA evidence — seven input artefacts

The Phase 4bf gate run reads-only and never writes to these paths. Their pre-run SHAs were re-verified at the merge boundary:

| # | Artefact | Path | SHA256 |
| - | -------- | ---- | ------ |
| 1 | derived manifest | `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json` | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| 2 | normalized Parquet | `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet` | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| 3 | raw manifest | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json` | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` |
| 4 | raw zip | `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip` | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| 5 | raw sidecar | `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256` | `b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d` |
| 6 | acquisition log | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001_acquisition_log.json` | `f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c` |
| 7 | Phase 4bb-D gate report | `data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json` | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |

**Seven input artefacts were byte-identical pre/post run.** The Phase 4bf real-run `result.measured_summary` records each artefact's `_sha_before` and `_sha_after` and `_mtime_ns_before` and `_mtime_ns_after`; every pair is identical. Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant was preserved end-to-end (the gate has no path that touches that helper).

---

## 5. Merge command

Executed verbatim from `main`:

```text
git merge --no-ff phase-4bf/aggtrades-derived-eligibility-gate \
  -m "feat(phase-4bf): merge derived aggtrades eligibility gate"
```

Result:

```text
Merge made by the 'ort' strategy.
14 files changed, 4633 insertions(+)
```

Files included:

- 4 new source modules under `src/prometheus/research/microstructure/`,
- narrow `__init__.py` update,
- 1 fixture builder + 5 test files under `tests/research/microstructure/`,
- 2 docs under `docs/00-meta/implementation-reports/`,
- narrow `docs/00-meta/current-project-state.md` update.

Push:

```text
git push origin main
29e3f55..cad383c  main -> main
```

`MAIN_AFTER`: `cad383cd5e85dae6b96fa83650d211842d5e070f`.

---

## 6. Post-merge validation

| Check | Result |
| ----- | ------ |
| Targeted Phase 4bf tests (5 files) | 155 / 155 passed in 1.59 s |
| `pytest tests/research/microstructure/` | 492 passed in 5.19 s |
| Whole-repo `pytest` | 1275 passed, 2 failed (only the pre-existing `KeyError: 'trade_count'` simulation failures in `tests/simulation/test_backtest_real_2026_03.py`; these are unrelated to Phase 4bf and were observed identically pre-merge) |
| `ruff check src/prometheus/research/microstructure tests/research/microstructure` | All checks passed |
| `ruff check .` | All checks passed |
| `mypy src/prometheus/research/microstructure` | Success: no issues found in 19 source files |
| `mypy src/prometheus` (strict, whole project) | Success: no issues found in 101 source files (was 97 prior; +4 new derived_gate_*) |
| `git diff --check` | clean |
| `main == origin/main` | `cad383cd5e85dae6b96fa83650d211842d5e070f` on both |

Phase 4bf introduces zero new test regressions.

---

## 7. Real-run gate evidence (preserved verbatim from Phase 4bf closeout)

| Field | Value |
| ----- | ----- |
| `overall_status` | `pass` |
| Total checks | 55 |
| PASS / FAIL / NOT_APPLICABLE / ERROR | 55 / 0 / 0 / 0 |
| `research_eligible_after` | `False` (raw-family / derived-family invariant) |
| `eligibility_gate_status_after` (recommendation only) | `pass` |
| `no_successor_authorization` | `True` (invariant) |
| Boundary confirmations (count / all `True`) | 15 / 15 |
| Gate report path (gitignored) | `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e.json` |
| Gate report SHA256 | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |
| Sidecar SHA256 (matches) | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |

The boundary confirmations remain:

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

## 8. Filesystem effect of the merge

The only on-disk filesystem effect of Phase 4bf (locally, gitignored, not committed) is the existing pair under `data/microstructure/gate-reports/normalized/`:

```text
microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e.json        (16,518 B)
microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e.json.sha256 (   147 B)
```

Both files are covered by `.gitignore:85: data/microstructure/`. Neither file was created or modified by the merge itself; they predate the merge as Phase 4bf real-run output.

The merge did not write to:

- `data/raw/`, `data/normalized/`, `data/manifests/`, `data/research/`, `data/derived/`,
- the existing `data/microstructure/raw/`, `data/microstructure/normalized/`, `data/microstructure/manifests/`, or `data/microstructure/gate-reports/gate-reports/` paths,
- any source code outside `src/prometheus/research/microstructure/`,
- any tests outside `tests/research/microstructure/`,
- any prior memo, governance file, or strategy document.

---

## 9. Retained verdict ledger (preserved verbatim)

- H0 — FRAMEWORK ANCHOR
- R3 — BASELINE-OF-RECORD
- R1a — RETAINED — NON-LEADING
- R1b-narrow — RETAINED — NON-LEADING
- R2 — FAILED — §11.6
- F1 — HARD REJECT
- D1-A — MECHANISM PASS / FRAMEWORK FAIL
- 5m thread — OPERATIONALLY CLOSED (Phase 3t)
- V2 — HARD REJECT — terminal for V2 first-spec
- G1 — HARD REJECT — terminal for G1 first-spec
- C1 — HARD REJECT — terminal for C1 first-spec

---

## 10. Project locks (preserved verbatim)

- §11.6 = 8 bps per side; round-trip = 16 bps.
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops.
- Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8.
- Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w.
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template.
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy.
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf results — all preserved.

---

## 11. No-rescue constraints

The merge does not loosen, amend, supersede, or redefine any retained verdict, project lock, or governance memo. No rescue path is opened. Specifically:

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
- no flipping of `research_eligible` to `true` on any raw or derived aggTrades family;
- no Stage-3 / Stage-4 transition;
- no M0 amendment derived from Phase 4bf reasoning.

---

## 12. Successor authorization

**None.** The merge does not authorize any successor phase. Specifically:

- no Phase 4bg authorized;
- no Phase 4bg-A authorized;
- no Phase 4bb-F authorized;
- no Phase 4bb-G authorized;
- no Phase 5 / Phase 4 canonical authorized;
- no additional acquisition;
- no Stage-3 / Stage-4 transition;
- no features, labels, ML, strategy, backtest;
- no paper / shadow / live-readiness / deployment;
- no exchange-write / production keys / authenticated APIs / private endpoints / user stream / WebSocket;
- no MCP / Graphify / `.mcp.json` / credentials.

---

## 13. Recommended state

**Remain paused.** A future docs-only Phase 4bg-A research-eligibility decision memo (after this Phase 4bf PASS report is reviewed), a Phase 4bb-F gate-report output-path hygiene memo, and a Phase 4bb-G raw-manifest successor-state recording memo all remain available as separately authorized next steps. None is authorized by this merge.

---

## 14. Cross-references

- Phase 4bf main memo: `docs/00-meta/implementation-reports/2026-05-07_phase-4bf_aggtrades-derived-family-eligibility-gate.md`.
- Phase 4bf closeout: `docs/00-meta/implementation-reports/2026-05-07_phase-4bf_closeout.md`.
- Phase 4bf-A merge closeout (predecessor): `docs/00-meta/implementation-reports/2026-05-07_phase-4bf-a_merge-closeout.md`.
- Phase 4bb-D PASS gate report (cited by Phase 4bf): SHA256 `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`; gate `code_commit_sha aa612ba2778c97a5150b80064244b90d024bfa54`; `report_id microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c`.
