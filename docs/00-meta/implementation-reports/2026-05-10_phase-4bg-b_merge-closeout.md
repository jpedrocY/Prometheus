# Phase 4bg-B — Merge Closeout

**Phase identity:** Phase 4bg-B — Derived-Family Research-Eligibility Successor-State Policy / Recording Memo.
**Phase type:** docs-and-local-gitignored-output successor-state recording phase.
**Action:** merge into `main`.
**Merge purpose:** record the Phase 4bg-A policy-level Stage-3 admissibility decision in machine-readable form for the normalized derived family `microstructure_normalized_aggtrades_v001` via one local gitignored successor-state JSON + paired SHA256 sidecar, while preserving the original derived manifest, the original raw manifest, the normalized Parquet, the Phase 4bb-D raw gate report, and the Phase 4bf derived-family gate report byte-identically. The merge does not mutate any manifest, run any gate, compute any feature, train any ML, create any strategy, run any backtest, acquire any data, or authorize any successor phase.
**Date:** 2026-05-10.
**Target branch:** `main`.
**Source branch:** `phase-4bg-b/derived-family-research-eligibility-successor-state`.
**`MAIN_BEFORE`:** `db9742a638e6393f3c5d30d1e94148e727368cbb` (Phase 4bg-A merge-closeout commit on `main` prior to Phase 4bg-B merge).
**Phase 4bg-B source commit:** `8bdb155f39def55d4cc157d8aad20bf58b148260` (`docs(phase-4bg-b): record derived aggtrades successor-state policy`).
**Merge commit (`MAIN_AFTER`, pre-merge-closeout):** `f134a7bbcf04b51139b8094ebc13839e50f5302e` (`docs(phase-4bg-b): merge derived-family successor-state recording`).
**Push:** `origin/main` advanced from `db9742a` → `f134a7b`.
**Merge method:** `git merge --no-ff` with the `ort` strategy.
**Status:** merged; pending operator review of this closeout.

---

## 1. Summary

Phase 4bg-B is now merged into `main`. The merge brings the Phase 4bg-B docs-and-local-gitignored-output successor-state recording phase into the project record. The recorded outcome is **Outcome 1 — Record successor state now**: a single local gitignored successor-state JSON artefact and its paired SHA256 sidecar were created under `data/microstructure/successor-state/` during Phase 4bg-B execution. No tracked data file was changed. No manifest mutation occurred at any point.

---

## 2. Files brought forward by the merge

| # | File | Change |
| - | ---- | ------ |
| 1 | `docs/00-meta/implementation-reports/2026-05-10_phase-4bg-b_derived-family-research-eligibility-successor-state.md` | new (24-section main memo) |
| 2 | `docs/00-meta/implementation-reports/2026-05-10_phase-4bg-b_closeout.md` | new |
| 3 | `docs/00-meta/current-project-state.md` | narrow Phase 4bg-B paragraph + new "Current phase:" block; prior Phase 4bg-A block preserved as historical context |

**Total diff summary from the Phase 4bg-B merge:** 3 files changed, **933 insertions**, 0 deletions. All three files are docs-only and reside under `docs/00-meta/`.

No other files were brought forward by the merge. No source code, tests, scripts, configurations, READMEs, MCP files, runtime configurations, manifests, raw artefacts, gate reports, or `.gitignore` entries were modified.

---

## 3. Pre-merge verification

| Check | Result |
| ----- | ------ |
| Branch at start of merge step | `phase-4bg-b/derived-family-research-eligibility-successor-state` |
| Phase 4bg-B source commit | `8bdb155` (clean working tree; only `.claude/scheduled_tasks.lock` and `data/research/` untracked, both gitignore-covered) |
| `git diff --stat main...HEAD` | 3 files; 933 insertions, 0 deletions |
| `git diff --name-only main...HEAD` | docs only |
| `main` synchronized with `origin/main` before merge | yes (`db9742a` on both) |
| Phase 4bg-A merge commit ancestor of `main` | `git merge-base --is-ancestor f8bfbc16c852c6c93023f80bb28ab70fc0af24e8 main` → true |
| `docs/00-meta/implementation-reports/2026-05-10_phase-4bg-a_merge-closeout.md` present on `main` | yes |
| `git check-ignore -v data/microstructure/` | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/successor-state/` | `.gitignore:85: data/microstructure/` |
| Phase 4bg-B successor-state JSON present locally | `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v001__stage3_research_eligible__phase-4bg-b.json` (2,679 B) + paired `.sha256` sidecar (158 B) |
| Phase 4bg-B successor-state SHA256 (recomputed) | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` — match |
| Normalized Parquet SHA256 (recomputed) | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` — match |
| Derived manifest SHA256 (recomputed) | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` — match |
| Raw manifest SHA256 (recomputed) | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` — match |
| Raw zip SHA256 (recomputed) | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` — match |
| Phase 4bb-D raw gate report SHA256 (recomputed) | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` — match |
| Phase 4bf derived-family gate report SHA256 (recomputed) | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` — match |
| Original raw manifest `research_eligible` / `eligibility_gate_status` | `false` / `pending` |
| Original derived manifest `research_eligible` / `eligibility_gate_status` | `false` / `pending` |
| `MAIN_BEFORE` | `db9742a638e6393f3c5d30d1e94148e727368cbb` |

---

## 4. Merge command

Executed verbatim from `main`:

```text
git merge --no-ff phase-4bg-b/derived-family-research-eligibility-successor-state \
  -m "docs(phase-4bg-b): merge derived-family successor-state recording"
```

Result:

```text
Merge made by the 'ort' strategy.
3 files changed, 933 insertions(+)
```

Push:

```text
git push origin main
db9742a..f134a7b  main -> main
```

`MAIN_AFTER` (pre-merge-closeout): `f134a7bbcf04b51139b8094ebc13839e50f5302e`.

---

## 5. Outcome

**Outcome 1 — Record successor state now (selected by the Phase 4bg-B main memo §11):**

- one local gitignored successor-state JSON created (Phase 4bg-B execution; not committed);
- one local gitignored successor-state SHA256 sidecar created (Phase 4bg-B execution; not committed);
- no tracked data committed at any point;
- the merge brings forward only the three docs files listed in §2.

---

## 6. Local successor-state artefact

| Field | Value |
| ----- | ----- |
| Path | `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v001__stage3_research_eligible__phase-4bg-b.json` |
| Size | `2,679 bytes` |
| SHA256 | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |
| Sidecar path | `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v001__stage3_research_eligible__phase-4bg-b.json.sha256` |
| Sidecar size | `158 bytes` |
| Sidecar SHA256 (matches) | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |
| Gitignore status | gitignored under `.gitignore:85: data/microstructure/`; not staged; not committed |

`git check-ignore -v data/microstructure/successor-state/` returns `.gitignore:85: data/microstructure/`. Both files remain local and reproducible from the Phase 4bg-B main memo §12 schema and the cited input SHAs.

---

## 7. Successor-state interpretation

- `successor_stage = Stage-3`;
- `successor_research_eligible = true`;
- `successor_eligibility_gate_status = pass`;
- **original derived manifest remains `research_eligible=false` and `eligibility_gate_status=pending`**;
- **original raw manifest remains `research_eligible=false` and `eligibility_gate_status=pending`**;
- **raw family remains permanently `research_eligible=false`**;
- any future tooling that wishes to interpret the derived family as Stage-3 must read the successor-state artefact at `data/microstructure/successor-state/...`, **not** the original derived manifest;
- any tool that reads only the original derived manifest must continue to treat the derived family as Stage-1-equivalent (inspected) — the `research_eligible=false` field on the original manifest is byte-immutable;
- **Stage-4 feature-cleared status is NOT authorized**;
- feature computation remains forbidden;
- labels remain forbidden;
- ML remains forbidden;
- strategy remains forbidden;
- backtests remain forbidden;
- acquisition remains unauthorized;
- **no successor phase is authorized** by Phase 4bg-B or by this merge.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked by Phase 4bg-B; not invoked by this merge).

---

## 8. Immutability evidence

| Artefact | SHA256 | Pre/post |
| -------- | ------ | -------- |
| original derived manifest | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` | identical |
| normalized Parquet | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` | identical |
| original raw manifest | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` | identical |
| raw zip | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | identical |
| Phase 4bb-D raw gate report | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` | identical |
| Phase 4bf derived-family gate report | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` | identical |

Both original manifest states preserved post-merge:

- original derived manifest `research_eligible=false / eligibility_gate_status=pending`;
- original raw manifest `research_eligible=false / eligibility_gate_status=pending`.

---

## 9. Validation results

| Check | Result |
| ----- | ------ |
| `pytest tests/research/microstructure/` | 492 passed |
| `ruff check .` | All checks passed |
| `mypy src/prometheus` (strict, whole project) | Success: no issues found in 101 source files |
| Whole-repo `pytest` | 1275 passed, 2 failed (only the pre-existing `KeyError: 'trade_count'` simulation failures in `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt`, both at `src/prometheus/research/data/storage.py:232`; identical pre-merge and post-merge; zero new regressions from Phase 4bg-B) |
| `git diff --check` | clean |
| `git check-ignore -v data/microstructure/` | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/successor-state/` | `.gitignore:85: data/microstructure/` |

Phase 4bg-B introduces zero new test regressions.

---

## 10. Boundary confirmations

The following boundary confirmations are recorded; every one is `True` for Phase 4bg-B and for this merge:

```text
no_source_code_change                                                True
no_test_change                                                       True
no_script_change                                                     True
no_config_change                                                     True
no_README_change                                                     True
no_pyproject_change                                                  True
no_gitignore_change                                                  True
no_M0_governance_change                                              True
no_data_acquisition                                                  True
no_public_endpoint_calls                                             True
no_binance_api_calls                                                 True
no_websocket                                                         True
no_credential_or_env_or_mcp_or_graphify                              True
no_normalizer_rerun                                                  True
no_raw_gate_rerun                                                    True
no_derived_gate_rerun                                                True
no_new_gate_report                                                   True
no_replacement_derived_manifest                                      True
no_replacement_raw_manifest                                          True
no_replacement_normalized_parquet                                    True
no_feature_computation                                               True
no_labels                                                            True
no_strategy_signals                                                  True
no_ml                                                                True
no_strategy                                                          True
no_backtest                                                          True
no_tracked_data_microstructure_output                                True
no_mutation_of_normalized_artefacts                                  True
no_mutation_of_raw_artefacts                                         True
no_mutation_of_phase_4bb_d_gate_report                               True
no_mutation_of_phase_4bf_gate_report                                 True
raw_family_research_eligible_remains_false                           True
raw_family_eligibility_gate_status_remains_pending                   True
original_derived_manifest_research_eligible_remains_false            True
original_derived_manifest_eligibility_gate_status_remains_pending    True
successor_state_record_marks_successor_research_eligible_true        True
no_retained_verdict_revised                                          True
no_project_lock_loosened                                             True
no_M0_amendment                                                      True
no_successor_authorized                                              True
```

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
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A results — all preserved.

---

## 13. No-rescue constraints

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
- no flipping of the original derived or raw manifest's `research_eligible` field to `true`;
- no Stage-4 transition;
- no M0 amendment derived from Phase 4bg-B reasoning;
- no reopening of any cooled-down family classification.

---

## 14. Successor authorization

**None.** The merge does not authorize any successor phase. Specifically:

- no Phase 4bh-A authorized;
- no Phase 4bh authorized;
- no Phase 4bi authorized;
- no Phase 4bg-C authorized;
- no Phase 4bb-F authorized;
- no Phase 4bb-G authorized;
- no Phase 5 authorized;
- no Phase 4 canonical authorized;
- no additional acquisition;
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

## 15. Recommended state

**Remain paused.**

A future docs-only Phase 4bh-A (Feature-Boundary Design memo, no computation), a future code-and-docs Phase 4bh (Feature Schema / Feature Computation implementation, only after Stage-4 authorization), a future code-and-docs Phase 4bb-F (Gate Report Output Path Hygiene, only before any repeated raw gate execution), and a future docs-only or docs-and-local-gitignored-output Phase 4bb-G (Raw Manifest Successor-State Recording) all remain available as separately authorized next steps. None is authorized by this merge.

---

## 16. Cross-references

- Phase 4bg-B main memo: `docs/00-meta/implementation-reports/2026-05-10_phase-4bg-b_derived-family-research-eligibility-successor-state.md`.
- Phase 4bg-B closeout: `docs/00-meta/implementation-reports/2026-05-10_phase-4bg-b_closeout.md`.
- Phase 4bg-A merge closeout (predecessor): `docs/00-meta/implementation-reports/2026-05-10_phase-4bg-a_merge-closeout.md`.
- Phase 4bf derived-family gate report (cited; gitignored, not committed): SHA256 `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6`; `report_id microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e`; gate `code_commit_sha 29e3f550e28ef4507fc7d008d2df9d53a46d52d8`.
- Phase 4bb-D raw gate report (cited; gitignored, not committed): SHA256 `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`; `report_id microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c`; gate `code_commit_sha aa612ba2778c97a5150b80064244b90d024bfa54`.
- Phase 4bg-B successor-state artefact (created locally; gitignored, not committed): SHA256 `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e`.
