# Phase 4bh-A — Merge Closeout

**Phase identity:** Phase 4bh-A — AggTrades Feature-Boundary Design Memo.
**Phase type:** docs-only feature-boundary design memo.
**Action:** merge into `main`.
**Merge purpose:** record the Phase 4bh-A feature-boundary design (Feature Stage-0; canonical input, forbidden inputs, proposed feature-family naming, feature-stage model, definitions, allowed and forbidden feature classes, leakage / windowing / aggregation / precision / type / missing-window policies, output / manifest schemas, validation gate sequence, M0 / cooled-down / no-rescue boundaries, acceptance criteria, fail-closed rules) into `main` without computing any feature, creating any feature dataset / manifest / sidecar, modifying source code / tests / scripts, acquiring data, mutating any manifest, or authorizing any successor phase.
**Date:** 2026-05-10.
**Target branch:** `main`.
**Source branch:** `phase-4bh-a/aggtrades-feature-boundary-design`.
**`MAIN_BEFORE`:** `81747263a12b5593282f2f5cfbb17ed413a84cb3` (Phase 4bg-B merge-closeout commit on `main` prior to Phase 4bh-A merge).
**Phase 4bh-A source commit:** `49e1ad1a6c1cfafff804801d73db24e9964160dd` (`docs(phase-4bh-a): design aggtrades feature boundary`).
**Merge commit (`MAIN_AFTER`, pre-merge-closeout):** `c85b0ec9efd8a00b05eb4f39fe156eb31fe07875` (`docs(phase-4bh-a): merge aggtrades feature-boundary design`).
**Push:** `origin/main` advanced from `8174726` → `c85b0ec`.
**Merge method:** `git merge --no-ff` with the `ort` strategy.
**Status:** merged; pending operator review of this closeout.

---

## 1. Summary

Phase 4bh-A is now merged into `main`. The merge brings the docs-only feature-boundary design memo into the project record. **Feature Stage-0** is reached for the proposed (NOT created) future feature family `microstructure_features_aggtrades_v001`. No feature is computed; no feature dataset, manifest, or sidecar is created; no source code, test, or script is added or modified; no data is acquired; no manifest is mutated; no successor phase is authorized.

---

## 2. Files brought forward by the merge

| # | File | Change |
| - | ---- | ------ |
| 1 | `docs/00-meta/implementation-reports/2026-05-10_phase-4bh-a_aggtrades-feature-boundary-design.md` | new (35-section main memo) |
| 2 | `docs/00-meta/implementation-reports/2026-05-10_phase-4bh-a_closeout.md` | new |
| 3 | `docs/00-meta/current-project-state.md` | narrow Phase 4bh-A paragraph + new "Current phase:" block; prior Phase 4bg-B block preserved as historical context |

**Total diff summary from the Phase 4bh-A merge:** 3 files changed, **1,212 insertions**, 0 deletions. All three files are docs-only and reside under `docs/00-meta/`.

No other files were brought forward by the merge.

---

## 3. Pre-merge verification

| Check | Result |
| ----- | ------ |
| Branch at start of merge step | `phase-4bh-a/aggtrades-feature-boundary-design` |
| Phase 4bh-A source commit | `49e1ad1` (clean working tree; only `.claude/scheduled_tasks.lock` and `data/research/` untracked, both gitignore-covered) |
| `git diff --stat main...HEAD` | 3 files; 1,212 insertions, 0 deletions |
| `git diff --name-only main...HEAD` | docs only |
| `main` synchronized with `origin/main` before merge | yes (`8174726` on both) |
| Phase 4bg-B merge commit ancestor of `main` | `git merge-base --is-ancestor f134a7bbcf04b51139b8094ebc13839e50f5302e main` → true |
| `docs/00-meta/implementation-reports/2026-05-10_phase-4bg-b_merge-closeout.md` present on `main` | yes |
| `git check-ignore -v data/microstructure/` | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/successor-state/` | `.gitignore:85: data/microstructure/` |
| Phase 4bg-B successor-state JSON SHA256 (recomputed) | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` — match |
| Normalized Parquet SHA256 (recomputed) | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` — match |
| Derived manifest SHA256 (recomputed) | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` — match |
| Raw manifest SHA256 (recomputed) | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` — match |
| Raw zip SHA256 (recomputed) | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` — match |
| Phase 4bb-D raw gate report SHA256 (recomputed) | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` — match |
| Phase 4bf derived-family gate report SHA256 (recomputed) | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` — match |
| Original raw manifest `research_eligible` / `eligibility_gate_status` | `false` / `pending` |
| Original derived manifest `research_eligible` / `eligibility_gate_status` | `false` / `pending` |
| `MAIN_BEFORE` | `81747263a12b5593282f2f5cfbb17ed413a84cb3` |

---

## 4. Merge command

Executed verbatim from `main`:

```text
git merge --no-ff phase-4bh-a/aggtrades-feature-boundary-design \
  -m "docs(phase-4bh-a): merge aggtrades feature-boundary design"
```

Result:

```text
Merge made by the 'ort' strategy.
3 files changed, 1212 insertions(+)
```

Push:

```text
git push origin main
8174726..c85b0ec  main -> main
```

`MAIN_AFTER` (pre-merge-closeout): `c85b0ec9efd8a00b05eb4f39fe156eb31fe07875`.

---

## 5. Design outcome

- **Feature Stage-0 reached** for the proposed (NOT created) future feature family;
- proposed future feature family: `microstructure_features_aggtrades_v001`;
- **feature family not created**;
- **feature dataset not created**;
- **feature manifest not created**;
- **feature sidecars not created**;
- source code unchanged;
- tests unchanged;
- scripts unchanged;
- no `data/microstructure/` writes (no tracked or untracked artefact created or modified by Phase 4bh-A or by this merge).

---

## 6. Feature-boundary summary

- **canonical input family** (only eligible): `microstructure_normalized_aggtrades_v001`;
- **canonical Stage-3 marker**: Phase 4bg-B successor-state artefact at `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v001__stage3_research_eligible__phase-4bg-b.json`, SHA256 `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e`;
- the **original derived manifest alone must not be interpreted as `research_eligible=true`**;
- proposed (NOT created) future output namespace: `data/microstructure/features/microstructure_features_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/`;
- proposed (NOT created) future feature manifest: `data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json`;

### Allowed feature categories (design-only; none approved for computation)

- count / intensity;
- volume;
- taker-side flow (using `is_buyer_maker`);
- past / current-only price-path descriptors;
- time-of-day context;
- data-quality / coverage flags.

### Forbidden feature classes

- future returns;
- next-window movement;
- future high / low;
- future realized volatility;
- future volume;
- labels;
- target columns;
- strategy signals;
- entry / exit flags;
- PnL;
- MFE / MAE;
- R-multiple;
- equity curve;
- position state;
- liquidation / funding / OI / order-book / mark-price features unless separately acquired and governed;
- ML embeddings;
- learned representations;
- features using rows after feature timestamp `T`;
- full-day-distribution normalization unless explicitly causal;
- z-scores using future data;
- post-hoc-fitted thresholds;
- any feature intended to revise or rescue retained verdicts.

### Temporal-leakage boundary

- a feature at time `T` may use only rows with `transact_time_ms <= T`;
- trailing windows only;
- centered windows forbidden;
- label construction forbidden;
- full-day statistics forbidden for research feature tables unless explicitly causal.

### Candidate windows (design-only)

`1 s`, `5 s`, `15 s`, `30 s`, `60 s`, `5 min`.

### Future feature-stage model

- Feature Stage-0: feature schema designed (Phase 4bh-A only);
- Feature Stage-1: feature implementation exists but never executed;
- Feature Stage-2: feature artefacts exist locally, gitignored, with manifest;
- Feature Stage-3: feature artefacts structurally QA-passed;
- Feature Stage-4: feature-family eligibility gate-passed;
- Feature Stage-5: research-use / ML-use decision.

### Required future validation sequence

- Phase 4bi-A — Feature Artefact Structural QA;
- Phase 4bi-B — Feature-Family Eligibility-Gate design + implementation + execution;
- Phase 4bi-C — Feature-Family Research-Use Decision Memo;
- Phase 4bi-D — Feature-Family Successor-State Recording, if authorized.

---

## 7. Local gitignored artefact state

The Phase 4bh-A merge does not write to `data/microstructure/`. The pre-existing local artefact SHAs are:

| # | Artefact | SHA256 |
| - | -------- | ------ |
| 1 | normalized Parquet | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| 2 | original derived manifest | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| 3 | raw manifest | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` |
| 4 | raw zip | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| 5 | Phase 4bb-D gate report | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| 6 | Phase 4bf gate report | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |
| 7 | Phase 4bg-B successor-state JSON | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |

All `data/microstructure/` artefacts remain gitignored and not committed. `git check-ignore -v data/microstructure/` confirms `.gitignore:85: data/microstructure/`. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked).

---

## 8. Validation results

| Check | Result |
| ----- | ------ |
| `pytest tests/research/microstructure/` | 492 passed |
| `ruff check .` | All checks passed |
| `mypy src/prometheus` (strict, whole project) | Success: no issues found in 101 source files |
| Whole-repo `pytest` | 1275 passed, 2 failed (only the pre-existing `KeyError: 'trade_count'` simulation failures in `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt`, both at `src/prometheus/research/data/storage.py:232`; identical pre-merge and post-merge; zero new regressions from Phase 4bh-A) |
| `git diff --check` | clean |
| `git check-ignore -v data/microstructure/` | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/successor-state/` | `.gitignore:85: data/microstructure/` |

Phase 4bh-A introduces zero new test regressions.

---

## 9. Boundary confirmations

The following boundary confirmations are recorded; every one is `True` for Phase 4bh-A and for this merge:

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
no_feature_pipeline_run                                              True
no_new_gate_report                                                   True
no_replacement_derived_manifest                                      True
no_replacement_raw_manifest                                          True
no_replacement_normalized_parquet                                    True
no_replacement_successor_state_artefact                              True
no_feature_dataset                                                   True
no_feature_manifest                                                  True
no_feature_sidecar                                                   True
no_feature_computation                                               True
no_labels                                                            True
no_targets                                                           True
no_strategy_signals                                                  True
no_ml                                                                True
no_strategy                                                          True
no_backtest                                                          True
no_tracked_data_microstructure_output                                True
no_mutation_of_normalized_artefacts                                  True
no_mutation_of_raw_artefacts                                         True
no_mutation_of_phase_4bb_d_gate_report                               True
no_mutation_of_phase_4bf_gate_report                                 True
no_mutation_of_phase_4bg_b_successor_state_artefact                  True
raw_family_research_eligible_remains_false                           True
raw_family_eligibility_gate_status_remains_pending                   True
original_derived_manifest_research_eligible_remains_false            True
original_derived_manifest_eligibility_gate_status_remains_pending    True
feature_computation_remains_forbidden                                True
stage_4_not_authorized                                               True
no_retained_verdict_revised                                          True
no_project_lock_loosened                                             True
no_M0_amendment                                                      True
no_successor_authorized                                              True
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
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B results — all preserved.

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
- no flipping of the original derived or raw manifest's `research_eligible` field to `true`;
- no Stage-4 transition;
- no M0 amendment derived from Phase 4bh-A reasoning;
- no reopening of any cooled-down family classification.

---

## 13. Successor authorization

**None.** The merge does not authorize any successor phase. Specifically:

- no Phase 4bh-B authorized;
- no Phase 4bh authorized;
- no Phase 4bi-A authorized;
- no Phase 4bi-B authorized;
- no Phase 4bi-C authorized;
- no Phase 4bi-D authorized;
- no Phase 4bj authorized;
- no Phase 4bb-F authorized;
- no Phase 4bb-G authorized;
- no Phase 5 authorized;
- no Phase 4 canonical authorized;
- no additional acquisition;
- no Stage-4 feature-cleared status;
- no feature computation;
- no labels;
- no targets;
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

A future docs-only Phase 4bh-B (AggTrades Feature Schema Finalization Memo), a future code-and-docs Phase 4bh (AggTrades Feature Schema / Feature Computation Implementation; only after Phase 4bh-A authorization boundaries explicitly permit implementation), a future analysis-and-docs Phase 4bi-A (Feature Artefact Structural QA Memo), a future code-and-docs Phase 4bb-F (Gate Report Output Path Hygiene; only before any repeated raw gate execution), and a future docs-only or docs-and-local-gitignored-output Phase 4bb-G (Raw Manifest Successor-State Recording) all remain available as separately authorized next steps. None is authorized by this merge.

---

## 15. Cross-references

- Phase 4bh-A main memo: `docs/00-meta/implementation-reports/2026-05-10_phase-4bh-a_aggtrades-feature-boundary-design.md`.
- Phase 4bh-A closeout: `docs/00-meta/implementation-reports/2026-05-10_phase-4bh-a_closeout.md`.
- Phase 4bg-B merge closeout (predecessor): `docs/00-meta/implementation-reports/2026-05-10_phase-4bg-b_merge-closeout.md`.
- Phase 4bg-B successor-state artefact (cited; gitignored, not committed): SHA256 `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e`.
- Phase 4bf derived-family gate report (cited; gitignored, not committed): SHA256 `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6`.
- Phase 4bb-D raw gate report (cited; gitignored, not committed): SHA256 `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`.
