# Phase 4bh-B — Merge Closeout

**Phase identity:** Phase 4bh-B — AggTrades Feature Schema Finalization Memo.
**Phase type:** docs-only feature schema finalization memo.
**Action:** merge into `main`.
**Merge purpose:** record the Phase 4bh-B feature schema finalization (final feature family name; canonical input cited via Phase 4bg-B successor-state JSON only; future output namespace / file path / sidecar / manifest paths; event-aligned output row model with expected `row_count = 1,681,098`; finalized windows {1s, 5s, 15s, 60s}; 45 feature columns; 16 lineage / identity / metadata columns; 61-column total schema; aggressive-side rule; causal trailing-window rule with same-timestamp tie-break; log-return rule; decimal/float policy; null/NaN policy; invalid-window propagation policy; 26-substring forbidden detector; future feature manifest schema; future feature config schema; future Phase 4bh module / test layout; 26 acceptance criteria; 17 fail-closed rules) into `main` without computing any feature, creating any feature dataset / manifest / sidecar / feature-config file, modifying source code / tests / scripts, acquiring data, mutating any manifest, or authorizing any successor phase.
**Date:** 2026-05-10.
**Target branch:** `main`.
**Source branch:** `phase-4bh-b/aggtrades-feature-schema-finalization`.
**`MAIN_BEFORE`:** `714a2730d2a03ffb9ef16daba7eea28fc359611c` (Phase 4bh-A merge-closeout commit on `main` prior to Phase 4bh-B merge).
**Phase 4bh-B source commit:** `f9d2644d8adab25f30f1d1d620c4b43ff8cf03b0` (`docs(phase-4bh-b): finalize aggtrades feature schema`).
**Merge commit (`MAIN_AFTER`, pre-merge-closeout):** `ba3c8d228557af85d1525e673ef869aaa53c2aff` (`docs(phase-4bh-b): merge aggtrades feature schema finalization`).
**Push:** `origin/main` advanced from `714a273` → `ba3c8d2`.
**Merge method:** `git merge --no-ff` with the `ort` strategy.
**Status:** merged; pending operator review of this closeout.

---

## 1. Summary

Phase 4bh-B is now merged into `main`. The merge brings the docs-only feature schema finalization memo into the project record. The Phase 4bh-A Feature Stage-0 design (feature boundary) is converted into an exact, implementable contract for any future Phase 4bh implementation. **No feature is computed; no feature dataset, manifest, sidecar, or feature-config file is created**; no source code, test, or script is added or modified; no data is acquired; no manifest is mutated; no successor phase is authorized.

---

## 2. Files brought forward by the merge

| # | File | Change |
| - | ---- | ------ |
| 1 | `docs/00-meta/implementation-reports/2026-05-10_phase-4bh-b_aggtrades-feature-schema-finalization.md` | new (34-section main memo) |
| 2 | `docs/00-meta/implementation-reports/2026-05-10_phase-4bh-b_closeout.md` | new |
| 3 | `docs/00-meta/current-project-state.md` | narrow Phase 4bh-B paragraph + new "Current phase:" block; prior Phase 4bh-A block preserved as historical context |

**Total diff summary from the Phase 4bh-B merge:** 3 files changed, **1,329 insertions**, 0 deletions. All three files are docs-only and reside under `docs/00-meta/`.

No other files were brought forward by the merge.

---

## 3. Pre-merge verification

| Check | Result |
| ----- | ------ |
| Branch at start of merge step | `phase-4bh-b/aggtrades-feature-schema-finalization` |
| Phase 4bh-B source commit | `f9d2644` (clean working tree; only `.claude/scheduled_tasks.lock` and `data/research/` untracked, both gitignore-covered) |
| `git diff --stat main...HEAD` | 3 files; 1,329 insertions, 0 deletions |
| `git diff --name-only main...HEAD` | docs only |
| `main` synchronized with `origin/main` before merge | yes (`714a273` on both) |
| Phase 4bh-A merge commit ancestor of `main` | `git merge-base --is-ancestor c85b0ec9efd8a00b05eb4f39fe156eb31fe07875 main` → true |
| `docs/00-meta/implementation-reports/2026-05-10_phase-4bh-a_merge-closeout.md` present on `main` | yes |
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
| `data/microstructure/features/` exists | no |
| `data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json` exists | no |
| `MAIN_BEFORE` | `714a2730d2a03ffb9ef16daba7eea28fc359611c` |

---

## 4. Merge command

Executed verbatim from `main`:

```text
git merge --no-ff phase-4bh-b/aggtrades-feature-schema-finalization \
  -m "docs(phase-4bh-b): merge aggtrades feature schema finalization"
```

Result:

```text
Merge made by the 'ort' strategy.
3 files changed, 1329 insertions(+)
```

Push:

```text
git push origin main
714a273..ba3c8d2  main -> main
```

`MAIN_AFTER` (pre-merge-closeout): `ba3c8d228557af85d1525e673ef869aaa53c2aff`.

---

## 5. Design outcome

- **feature schema finalized at policy level**;
- future feature family finalized as `microstructure_features_aggtrades_v001`;
- **feature family not created**;
- **feature dataset not created**;
- **feature manifest not created**;
- **feature config not created**;
- **feature sidecars not created**;
- source code unchanged;
- tests unchanged;
- scripts unchanged;
- no `data/microstructure/` writes (no tracked or untracked artefact created or modified by Phase 4bh-B or by this merge).

---

## 6. Finalized schema summary

- **canonical input:** `microstructure_normalized_aggtrades_v001`;
- **canonical Stage-3 marker:** Phase 4bg-B successor-state artefact only, SHA256 `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e`;
- the **original derived manifest alone must not be interpreted as `research_eligible=true`**;
- **future output row model:** event-aligned, one feature row per normalized aggTrade row;
- **future expected `row_count`:** `1,681,098` for BTCUSDT 2025-01-15;
- **future timestamp cadence:** `feature_timestamp_ms = source transact_time_ms`;
- **future windows:** `{1s, 5s, 15s, 60s}` (`window_ms = [1000, 5000, 15000, 60000]`);
- **deferred windows:** 30s, 5m;
- **future feature columns:** **45** (40 windowed = 4 windows × 10 features + 3 time-context + 2 data-quality);
- **future lineage / identity / metadata columns:** **16**;
- **future total schema columns:** **61**;
- **aggressive-side rule:** `is_buyer_maker = false` ⇒ aggressive buy; `is_buyer_maker = true` ⇒ aggressive sell;
- **causal windowing:** trailing window `(T - window_ms, T]` with same-timestamp tie-break `row_index <= R`;
- **log-return rule:** current row price divided by last observed prior reference price at or before `T - window_ms`; null if unavailable;
- **decimal / float policy:** raw `price` and raw `quantity` never `float`; Decimal-as-string for quantity sums / means / aggressive-side quantities / imbalances; `float64` only for ratios / log returns;
- **null policy:** counts `0`, quantity sums `"0"`, means null on empty windows, ratio null when denominator zero, log return null when prior reference unavailable; **no imputation across invalid windows**;
- **forbidden-substring detector:** **26** forbidden substrings (`label`, `target`, `future`, `signal`, `entry`, `exit`, `pnl`, `profit`, `loss`, `mfe`, `mae`, `r_multiple`, `equity`, `position`, `alpha`, `edge`, `prediction`, `model`, `score`, `decision`, `strategy`, `liquidation`, `funding`, `open_interest`, `order_book`, `mark_price`); future Phase 4bh validation must fail closed if any output column name (lowercased) contains any of these;
- **future feature manifest defaults:** `research_eligible = false`, `eligibility_gate_status = pending`; full lineage SHA references required (source normalized manifest, source normalized Parquet, source successor-state, Phase 4bf gate report);
- **future Phase 4bh modules proposed but not created:** `features_schema.py`, `features_io.py`, `features_compute.py`, `features_manifest.py`, `features_validation.py`, plus narrow `__init__.py` re-export update;
- **future Phase 4bh tests proposed but not created:** `test_features_schema.py`, `test_features_io.py`, `test_features_compute.py`, `test_features_manifest.py`, `test_features_validation.py`, `test_features_no_network.py`, optional shared fixture builder;
- **26 acceptance criteria + 17 fail-closed rules** recorded for any future Phase 4bh implementation.

---

## 7. Finalized future paths (NOT created)

| # | Future path |
| - | ----------- |
| 1 | `data/microstructure/features/microstructure_features_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-features-aggtrades-2025-01-15.parquet` |
| 2 | `data/microstructure/features/microstructure_features_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-features-aggtrades-2025-01-15.parquet.sha256` |
| 3 | `data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json` |

None of these paths exists. The directory `data/microstructure/features/` does not exist. All would be gitignored under the existing `.gitignore:85: data/microstructure/` rule when (and if) a future separately authorized Phase 4bh implementation creates them.

---

## 8. Local gitignored artefact state

The Phase 4bh-B merge does not write to `data/microstructure/`. The pre-existing local artefact SHAs are:

| # | Artefact | SHA256 |
| - | -------- | ------ |
| 1 | normalized Parquet | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| 2 | original derived manifest | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| 3 | raw manifest | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` |
| 4 | raw zip | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| 5 | Phase 4bb-D gate report | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| 6 | Phase 4bf gate report | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |
| 7 | Phase 4bg-B successor-state JSON | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |

All `data/microstructure/` artefacts remain gitignored and not committed. The future feature output namespace was not created and the future feature manifest was not created. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked).

---

## 9. Validation results

| Check | Result |
| ----- | ------ |
| `pytest tests/research/microstructure/` | 492 passed |
| `ruff check .` | All checks passed |
| `mypy src/prometheus` (strict, whole project) | Success: no issues found in 101 source files |
| Whole-repo `pytest` | 1275 passed, 2 failed (only the pre-existing `KeyError: 'trade_count'` simulation failures in `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt`, both at `src/prometheus/research/data/storage.py:232`; identical pre-merge and post-merge; zero new regressions from Phase 4bh-B) |
| `git diff --check` | clean |
| `git check-ignore -v data/microstructure/` | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/successor-state/` | `.gitignore:85: data/microstructure/` |

Phase 4bh-B introduces zero new test regressions.

---

## 10. Boundary confirmations

The following boundary confirmations are recorded; every one is `True` for Phase 4bh-B and for this merge:

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
no_feature_config                                                    True
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
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A results — all preserved.

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
- no M0 amendment derived from Phase 4bh-B reasoning;
- no reopening of any cooled-down family classification.

---

## 14. Successor authorization

**None.** The merge does not authorize any successor phase. Specifically:

- no Phase 4bh-C authorized;
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

## 15. Recommended state

**Remain paused.**

A future docs-only Phase 4bh-C (Feature Schema Finalization Review / Red-Team Memo), a future code + docs + local gitignored output Phase 4bh (AggTrades Feature Schema / Feature Computation Implementation, using the exact Phase 4bh-B finalized schema), a future analysis + docs Phase 4bi-A (Feature Artefact Structural QA Memo), a future code + docs Phase 4bb-F (Gate Report Output Path Hygiene; only before any repeated raw gate execution), and a future docs-only or docs-and-local-gitignored-output Phase 4bb-G (Raw Manifest Successor-State Recording) all remain available as separately authorized next steps. None is authorized by this merge.

---

## 16. Cross-references

- Phase 4bh-B main memo: `docs/00-meta/implementation-reports/2026-05-10_phase-4bh-b_aggtrades-feature-schema-finalization.md`.
- Phase 4bh-B closeout: `docs/00-meta/implementation-reports/2026-05-10_phase-4bh-b_closeout.md`.
- Phase 4bh-A merge closeout (predecessor): `docs/00-meta/implementation-reports/2026-05-10_phase-4bh-a_merge-closeout.md`.
- Phase 4bg-B successor-state artefact (cited; gitignored, not committed): SHA256 `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e`.
- Phase 4bf derived-family gate report (cited; gitignored, not committed): SHA256 `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6`.
- Phase 4bb-D raw gate report (cited; gitignored, not committed): SHA256 `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`.
