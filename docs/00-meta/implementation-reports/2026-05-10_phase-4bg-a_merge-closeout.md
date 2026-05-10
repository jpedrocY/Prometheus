# Phase 4bg-A — Merge Closeout

**Phase identity:** Phase 4bg-A — Derived-Family Research-Eligibility Decision Memo.
**Phase type:** docs-only research-eligibility decision / governance memo.
**Action:** merge into `main`.
**Merge purpose:** record the policy-level Stage-3 admissibility decision (Option B / Decision form 2) for the normalized derived family `microstructure_normalized_aggtrades_v001` into the project record without mutating any manifest, gate report, dataset, source code, test, script, or configuration.
**Date:** 2026-05-10.
**Target branch:** `main`.
**Source branch:** `phase-4bg-a/derived-family-research-eligibility-decision`.
**`MAIN_BEFORE`:** `250afc8c99ce044948a3df6977e0323456ba95e6` (Phase 4bf merge-closeout commit on `main` prior to Phase 4bg-A merge).
**Phase 4bg-A source commit:** `6776f79281926dcf16a710ff95dd563de7efcb94` (`docs(phase-4bg-a): decide derived aggtrades research eligibility`).
**Merge commit (`MAIN_AFTER`, pre-merge-closeout):** `f8bfbc16c852c6c93023f80bb28ab70fc0af24e8` (`docs(phase-4bg-a): merge derived-family research-eligibility decision`).
**Push:** `origin/main` advanced from `250afc8` → `f8bfbc1`.
**Merge method:** `git merge --no-ff` with the `ort` strategy.
**Status:** merged; pending operator review of this closeout.

---

## 1. Summary

Phase 4bg-A is now merged into `main`. The merge brings the Phase 4bg-A docs-only research-eligibility decision memo into the project record. The recorded decision is **Option B / Decision form 2**:

> Stage-3 is admissible in principle at policy level for the normalized derived family `microstructure_normalized_aggtrades_v001`, but no manifest mutation occurs in this phase. A separately authorized successor-state recording phase is required before any machine-readable `research_eligible=true` marker exists.

The merge does not change any retained verdict, project lock, governance memo, or M0 admissibility rule, and does not authorize any successor phase. No source code, tests, scripts, configurations, READMEs, MCP files, runtime configuration, manifests, raw artefacts, gate reports, or `.gitignore` entries were modified.

---

## 2. Files brought forward by the merge

| # | File | Change |
| - | ---- | ------ |
| 1 | `docs/00-meta/implementation-reports/2026-05-10_phase-4bg-a_derived-family-research-eligibility-decision.md` | new (28-section main memo) |
| 2 | `docs/00-meta/implementation-reports/2026-05-10_phase-4bg-a_closeout.md` | new |
| 3 | `docs/00-meta/current-project-state.md` | narrow Phase 4bg-A paragraph + new "Current phase:" block; prior Phase 4bf block preserved as historical context |

**Total diff summary from the Phase 4bg-A merge:** 3 files changed, **986 insertions**, 0 deletions. All three files are docs-only and reside under `docs/00-meta/`.

No other files were brought forward. No files outside the listed paths were modified by Phase 4bg-A or by this merge.

---

## 3. Pre-merge verification

| Check | Result |
| ----- | ------ |
| Branch at start of merge step | `phase-4bg-a/derived-family-research-eligibility-decision` |
| Phase 4bg-A source commit | `6776f79` (clean working tree; only `.claude/scheduled_tasks.lock` and `data/research/` untracked, both gitignore-covered) |
| `git diff --stat main...HEAD` | 3 files; `docs/00-meta/current-project-state.md` (+304), `…_phase-4bg-a_closeout.md` (+149), `…_phase-4bg-a_derived-family-research-eligibility-decision.md` (+533) |
| `git diff --name-only main...HEAD` | docs only |
| `main` synchronized with `origin/main` before merge | yes (`250afc8` on both) |
| Phase 4bf merge commit ancestor of `main` | `git merge-base --is-ancestor cad383cd5e85dae6b96fa83650d211842d5e070f main` → true |
| `docs/00-meta/implementation-reports/2026-05-10_phase-4bf_merge-closeout.md` present on `main` | yes |
| `git check-ignore -v data/microstructure/` | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/gate-reports/normalized/` | `.gitignore:85: data/microstructure/` |
| Phase 4bf gate report present locally | `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e.json` (16,518 B) + paired `.sha256` sidecar |
| Phase 4bf gate report SHA256 (recomputed) | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` — match |
| Normalized Parquet SHA256 (recomputed) | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` — match |
| Derived manifest SHA256 (recomputed) | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` — match |
| Raw manifest SHA256 (recomputed) | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` — match |
| Raw zip SHA256 (recomputed) | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` — match |
| Phase 4bb-D gate report SHA256 (recomputed) | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` — match |
| Original raw manifest `research_eligible` / `eligibility_gate_status` | `false` / `pending` |
| Derived manifest `research_eligible` / `eligibility_gate_status` | `false` / `pending` |
| `MAIN_BEFORE` | `250afc8c99ce044948a3df6977e0323456ba95e6` |

---

## 4. Merge command

Executed verbatim from `main`:

```text
git merge --no-ff phase-4bg-a/derived-family-research-eligibility-decision \
  -m "docs(phase-4bg-a): merge derived-family research-eligibility decision"
```

Result:

```text
Merge made by the 'ort' strategy.
3 files changed, 986 insertions(+)
```

Push:

```text
git push origin main
250afc8..f8bfbc1  main -> main
```

`MAIN_AFTER` (pre-merge-closeout): `f8bfbc16c852c6c93023f80bb28ab70fc0af24e8`.

---

## 5. Decision result

**Option B / Decision form 2 selected (verbatim from the Phase 4bg-A main memo §20):**

> Stage-3 is admissible in principle at policy level for the normalized derived family `microstructure_normalized_aggtrades_v001`, but no manifest mutation occurs in this phase. A separately authorized successor-state recording phase is required before any machine-readable `research_eligible=true` marker exists.

Specifically:

- **Stage-3 admissible in principle at policy level** for `microstructure_normalized_aggtrades_v001`;
- **no manifest mutation occurred** in Phase 4bg-A or in this merge;
- a **separately authorized successor-state recording phase** is required before any machine-readable `research_eligible=true` marker exists;
- the **raw family remains permanently `research_eligible=false`** (Phase 4bb-E policy);
- the **derived manifest remains `research_eligible=false` and `eligibility_gate_status=pending`**;
- the **raw manifest remains `research_eligible=false` and `eligibility_gate_status=pending`**;
- **feature computation remains forbidden**;
- **ML remains forbidden**;
- **strategy remains forbidden**;
- **backtests remain forbidden**;
- **acquisition remains unauthorized**;
- **no successor authorized**.

---

## 6. Admissibility evidence

| # | Criterion | Source |
| - | --------- | ------ |
| 1 | Stage-0 derived artefacts exist and are reproducible locally | Phase 4bd implementation report; Phase 4bd merge closeout |
| 2 | Derived manifest references raw lineage | Phase 4bd derived manifest `governance_labels` |
| 3 | Phase 4be structural QA passed 60 / 60 | Phase 4be memo + closeout |
| 4 | Phase 4bf derived-family eligibility gate passed 55 / 55 at report level | Phase 4bf memo + closeout + merge closeout |
| 5 | Phase 4bf gate report SHA256 recorded | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |
| 6 | `invalid_windows = []` | Phase 4bf real-run summary |
| 7 | No features / labels / signals / proxies / ML / strategy / backtest artefacts exist | Phase 4bd-A scope; Phase 4bd implementation; Phase 4be schema check; Phase 4bf check 4bf.13.* feature-absence subgroup |
| 8 | No project lock loosened | retained verdict ledger and lock list (§10) preserved verbatim |
| 9 | No retained verdict revised | retained verdict ledger (§9) preserved verbatim |
| 10 | M0 remains binding prospectively | Phase 4ak adoption preserved |
| 11 | Stage-4 feature-boundary design still required before feature computation | Phase 4ba ladder preserved; Stage-4 not authorized |

---

## 7. Local gitignored artefact state

The Phase 4bg-A merge does not write to `data/microstructure/`. The pre-existing local artefact SHAs are:

| # | Artefact | Path | SHA256 |
| - | -------- | ---- | ------ |
| 1 | normalized Parquet | `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet` | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| 2 | derived manifest | `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json` | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| 3 | raw manifest | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json` | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` |
| 4 | raw zip | `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip` | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| 5 | Phase 4bb-D gate report | `data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json` | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| 6 | Phase 4bf gate report | `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e.json` | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |

All `data/microstructure/` artefacts remain gitignored and not committed. `git check-ignore -v data/microstructure/` confirms `.gitignore:85: data/microstructure/`.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end. Neither manifest's `research_eligible` field nor `eligibility_gate_status` field changed at any point during Phase 4bg-A or the Phase 4bg-A merge.

---

## 8. Validation results

| Check | Result |
| ----- | ------ |
| `pytest tests/research/microstructure/` | 492 passed |
| `ruff check .` | All checks passed |
| `mypy src/prometheus` (strict, whole project) | Success: no issues found in 101 source files |
| Whole-repo `pytest` | 1275 passed, 2 failed (only the pre-existing `KeyError: 'trade_count'` simulation failures in `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt`, both at `src/prometheus/research/data/storage.py:232`; identical pre-merge and post-merge; zero new regressions from Phase 4bg-A) |
| `git diff --check` | clean |
| `git check-ignore -v data/microstructure/` | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/gate-reports/normalized/` | `.gitignore:85: data/microstructure/` |

Phase 4bg-A introduces zero new test regressions.

---

## 9. Boundary confirmations

The following boundary confirmations are recorded; every one is `True` for Phase 4bg-A:

```text
no_source_code_change                                        True
no_test_change                                               True
no_script_change                                             True
no_config_change                                             True
no_README_change                                             True
no_pyproject_change                                          True
no_gitignore_change                                          True
no_M0_governance_change                                      True
no_data_acquisition                                          True
no_public_endpoint_calls                                     True
no_binance_api_calls                                         True
no_websocket                                                 True
no_credential_or_env_or_mcp_or_graphify                      True
no_normalizer_rerun                                          True
no_raw_gate_rerun                                            True
no_derived_gate_rerun                                        True
no_new_gate_report                                           True
no_replacement_derived_manifest                              True
no_replacement_normalized_parquet                            True
no_successor_manifest                                        True
no_feature_computation                                       True
no_labels                                                    True
no_strategy_signals                                          True
no_ml                                                        True
no_strategy                                                  True
no_backtest                                                  True
no_tracked_data_microstructure_output                        True
no_mutation_of_normalized_artefacts                          True
no_mutation_of_raw_artefacts                                 True
no_mutation_of_phase_4bb_d_gate_report                       True
no_mutation_of_phase_4bf_gate_report                         True
raw_family_research_eligible_remains_false                   True
raw_family_eligibility_gate_status_remains_pending           True
derived_family_research_eligible_remains_false               True
derived_family_eligibility_gate_status_remains_pending       True
no_retained_verdict_revised                                  True
no_project_lock_loosened                                     True
no_M0_amendment                                              True
no_successor_authorized                                      True
```

---

## 10. Retained verdict ledger

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

## 11. Preserved project locks

- §11.6 = 8 bps per side; round-trip = 16 bps.
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops.
- Phase 3p §4.7.
- Phase 3r §8.
- Phase 3v §8.
- Phase 3w §6 / §7 / §8.
- Phase 4j §11.
- Phase 4k.
- Phase 4p.
- Phase 4q.
- Phase 4v.
- Phase 4w.
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template.
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy.
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf results — all preserved.

---

## 12. No-rescue constraints

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
- no M0 amendment derived from Phase 4bg-A reasoning;
- no reopening of any cooled-down family classification.

---

## 13. Successor authorization

**None.** The merge does not authorize any successor phase. Specifically:

- no Phase 4bg-B authorized;
- no Phase 4bh-A authorized;
- no Phase 4bh authorized;
- no Phase 4bb-F authorized;
- no Phase 4bb-G authorized;
- no Phase 5 authorized;
- no Phase 4 canonical authorized;
- no additional acquisition;
- no Stage-3 manifest transition;
- no Stage-4 feature-cleared status;
- no features;
- no labels;
- no ML;
- no strategy;
- no backtest;
- no paper / shadow;
- no live-readiness;
- no deployment;
- no exchange-write;
- no production keys;
- no authenticated APIs;
- no private endpoints;
- no user stream;
- no MCP / Graphify / `.mcp.json` / credentials.

---

## 14. Recommended state

**Remain paused.**

A future docs-only Phase 4bg-B (Derived-Family Research-Eligibility Successor-State Policy / Recording memo), a future docs-only Phase 4bh-A (Feature-Boundary Design memo), a future code-and-docs Phase 4bb-F (Gate Report Output Path Hygiene), and a future docs-only or docs-and-local-gitignored-output Phase 4bb-G (Raw Manifest Successor-State Recording) all remain available as separately authorized next steps. None is authorized by this merge.

---

## 15. Cross-references

- Phase 4bg-A main memo: `docs/00-meta/implementation-reports/2026-05-10_phase-4bg-a_derived-family-research-eligibility-decision.md`.
- Phase 4bg-A closeout: `docs/00-meta/implementation-reports/2026-05-10_phase-4bg-a_closeout.md`.
- Phase 4bf merge closeout (predecessor): `docs/00-meta/implementation-reports/2026-05-10_phase-4bf_merge-closeout.md`.
- Phase 4bf real-run gate report (cited; gitignored, not committed): SHA256 `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6`; gate `code_commit_sha 29e3f550e28ef4507fc7d008d2df9d53a46d52d8`; `report_id microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e`.
- Phase 4bb-D raw gate report (cited; gitignored, not committed): SHA256 `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`; gate `code_commit_sha aa612ba2778c97a5150b80064244b90d024bfa54`; `report_id microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c`.
