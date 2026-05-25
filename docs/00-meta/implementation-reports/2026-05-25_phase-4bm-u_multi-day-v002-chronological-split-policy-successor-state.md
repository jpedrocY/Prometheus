# Phase 4bm-U — Multi-Day V002 Chronological Split-Policy Successor-State Recording

**Phase identity:** Phase 4bm-U — Multi-Day V002 Chronological Split-Policy Successor-State Recording (docs + local gitignored successor-state JSON + paired canonical Phase 4bb-F sidecar; multi-day v002 analogue of the v001 Phase 4bj-J split-policy successor-state recording, recording a *formal-split* policy rather than a *no-split* determination).
**Date:** 2026-05-25.
**Branch:** `phase-4bm-u/multi-day-v002-chronological-split-policy-successor-state`.
**Base SHA:** `main` at `f7c8cb674bc08925df8e5f5765008cc92a403d08` (Phase 4bm-T merge-closeout SHA-finalization commit; pre-branch `main == origin/main` verified in sync).
**Tier:** **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3. First-of-kind multi-day v002 chronological-split-policy successor-state recording; it produces a machine-readable governance marker for the v002 label family and therefore escalates to Tier 1.
**Phase type:** docs + local gitignored output — adds two new tracked docs files under `docs/00-meta/implementation-reports/`, narrowly updates `docs/00-meta/current-project-state.md`, and writes exactly one new local gitignored successor-state JSON + paired canonical Phase 4bb-F sidecar under `data/microstructure/successor-state/labels/`. **No** source / test / committed-script / configuration / manifest / sidecar / gate-report / prior-successor-state mutation.
**Status:** drafted; pending operator review. Branch-complete only by this work; not merged into `main`; not project-complete.

---

## 1. Required exact phrases

- **Phase 4bm-U records chronological split policy as a sibling successor-state artefact only.**
- **Phase 4bm-U does not mutate any manifest.**
- **Phase 4bm-U does not mutate the Phase 4bm-S successor-state artefact.**
- **Phase 4bm-U preserves the v002 label manifest byte-identically.**
- **Phase 4bm-U preserves the Phase 4bm-S successor-state byte-identically.**
- **Phase 4bm-U preserves the Phase 4bm-Q gate report byte-identically.**
- **Phase 4bm-U does not authorize diagnostics, ML, strategy, or backtests.**
- **Phase 4bm-U does not authorize acquisition.**
- **Phase 4bm-U does not authorize research execution.**
- **Phase 4bm-U does not commit data/microstructure.**
- **Phase 4bm-V is not authorized by Phase 4bm-U.**
- **Recommended state remains paused.**

---

## 2. Phase identity

Phase 4bm-U operationalises the Phase 4bm-T memo-level chronological split policy `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` into exactly one machine-readable sibling chronological-split-policy successor-state JSON artefact under `data/microstructure/successor-state/labels/`, while preserving the original v002 label manifest, the v002 label manifest sidecar, the Phase 4bm-S label-family research-use successor-state JSON + sidecar, the Phase 4bm-Q label-family eligibility gate report + sidecar, and every other prior `data/microstructure/` artefact byte-identically. **Phase 4bm-U records chronological split policy as a sibling successor-state artefact only.**

Phase 4bm-U is the **multi-day v002 analogue of Phase 4bj-J** (the v001 split-policy successor-state recording), with the key difference that the v001 cell recorded a *no-split determination* (single UTC day insufficient for formal partitioning) whereas the v002 90-day family records a *formal train / validation / test split* policy — exactly the multi-day expansion that the v001 Phase 4bj-I memo named as the precondition for formal chronological partitioning.

## 3. Branch name

`phase-4bm-u/multi-day-v002-chronological-split-policy-successor-state`

## 4. Base SHA

`f7c8cb674bc08925df8e5f5765008cc92a403d08` (Phase 4bm-T merge-closeout SHA-finalization commit, `docs(phase-4bm-t): finalize merge closeout shas`; the head of `main` at branch time; `main == origin/main` verified in sync). The Phase 4bm-T merge commit `14e52c369031bce37cda83cfc79f345b57c6ff15` and merge-closeout commit `d3ee2f7995ee540b518e19bcd88bfbf3243565c4` are present on `main` immediately below this SHA-finalization commit.

## 5. Predecessor Phase 4bm-T split-policy result

`CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` (Phase 4bm-T — Multi-Day V002 Chronological Split-Policy Memo; docs-only; merge-complete and SHA-finalized on `main`). Phase 4bm-T defined, at memo level only, a conservative formal chronological train / validation / test split for the 90-day v002 label family, with a minimum 60-second boundary embargo, boundary-crossing-row exclusion from the earlier split, a no-shuffle rule, and a single-use final-holdout rule. Phase 4bm-U is the separately authorized successor-state recording phase that encodes that policy machine-readably as a sibling artefact.

## 6. Successor-state JSON path

```text
data/microstructure/successor-state/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-u__1779718408615__f7c8cb674bc0.json
```

Absolute path on the local workstation:

```text
C:\Prometheus\data\microstructure\successor-state\labels\microstructure_labels_aggtrades_v001__v002__phase-4bm-u__1779718408615__f7c8cb674bc0.json
```

Gitignored under `.gitignore:85: data/microstructure/`. **Not committed.**

## 7. Successor-state JSON SHA256

```text
6834ab11a5ac5d93b4d9f14d9b71ef3acb2a279bd8e3189fd22421598675fc9c
```

Size: **6,050 bytes**. ASCII (no BOM). LF line endings only. Two-space indent. Sorted keys (`json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True) + "\n"`). Final newline at EOF. Deterministic except for the explicitly recorded `created_at_unix_ms = 1779718408615` / `created_at_utc = 2026-05-25T14:13:28.615Z` timestamp and the recorded code commit reference (`base_main_commit_sha = code_commit_sha = f7c8cb674bc08925df8e5f5765008cc92a403d08`).

## 8. Successor-state sidecar path

```text
data/microstructure/successor-state/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-u__1779718408615__f7c8cb674bc0.json.sha256
```

Gitignored under `.gitignore:85: data/microstructure/`. **Not committed.**

## 9. Successor-state sidecar SHA256

```text
fa9ae709add4541111e70cfc03d9126ac40f136ea2ce1aa1abe299d3412ac0b6
```

Size: **156 bytes**. Canonical Phase 4bb-F format: `<sha256_lowercase_hex><two ASCII spaces><basename><LF>`. Verified byte-by-byte: bytes 0..63 = lowercase hex JSON SHA256; bytes 64..65 = `0x20 0x20`; basename follows; final byte = `0x0A` (LF); no CRLF; no BOM; total = 156 bytes. Exact content:

```text
6834ab11a5ac5d93b4d9f14d9b71ef3acb2a279bd8e3189fd22421598675fc9c  microstructure_labels_aggtrades_v001__v002__phase-4bm-u__1779718408615__f7c8cb674bc0.json
```

The embedded SHA matches the recomputed SHA256 of the JSON byte-for-byte.

## 10. Successor-state decision

`CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`.

The successor-state JSON records `split_policy_name = "CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO"`, `split_policy_status = "recorded"`, and the full split-policy detail block (train 2024-12-01..2025-01-14 / 45 dates; validation 2025-01-15..2025-02-13 / 30 dates; test 2025-02-14..2025-02-28 / 15 dates; ratio 45/30/15; assignment by `source_transact_time_ms` UTC date; boundary timestamps `2025-01-15T00:00:00Z` and `2025-02-14T00:00:00Z`; minimum 60s embargo; boundary-crossing rows excluded from earlier split; no-shuffle / no-random / no-bootstrap; single-use final holdout with all seven prohibited test-window uses set false) **only on the sibling successor-state artefact**, never on the manifest.

## 11. Confirmation — original v002 label manifest unchanged

`data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json` SHA256 (pre and post Phase 4bm-U): `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` (byte-identical; re-hashed before and after the write). The manifest continues to carry `research_eligible = false`, `eligibility_gate_status = "pending"`, `stage_5_label_cleared = false`, `label_family_research_use_authorized = false`, and `chronological_split_policy = "not_yet_defined"`. **Phase 4bm-U preserves the v002 label manifest byte-identically.** **Phase 4bm-U does not mutate any manifest.**

## 12. Confirmation — original v002 label manifest sidecar unchanged

`data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json.sha256` SHA256 (pre and post): `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` (byte-identical).

## 13. Confirmation — Phase 4bm-Q gate report unchanged

`data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-q__1779708036319__3f87123175e0.json` SHA256 (pre and post): `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` (byte-identical; gate not re-run; read-only re-hash only). **Phase 4bm-U preserves the Phase 4bm-Q gate report byte-identically.**

## 14. Confirmation — Phase 4bm-Q gate report sidecar unchanged

`data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-q__1779708036319__3f87123175e0.json.sha256` SHA256 (pre and post): `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` (byte-identical).

## 15. Confirmation — Phase 4bm-S successor-state unchanged

`data/microstructure/successor-state/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-s__1779715783843__e2fdbdd6d738.json` SHA256 (pre and post): `081730006c11360692db0a99d59a0ed499f762ef4f86d6e29bdf3016550abfe7` (byte-identical; gitignored). **Phase 4bm-U preserves the Phase 4bm-S successor-state byte-identically.** **Phase 4bm-U does not mutate the Phase 4bm-S successor-state artefact.**

## 16. Confirmation — Phase 4bm-S successor-state sidecar unchanged

`data/microstructure/successor-state/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-s__1779715783843__e2fdbdd6d738.json.sha256` SHA256 (pre and post): `05597fe4d568f5644ad9acc914f8a3b429bc7984cf7df3a2ac3f8c7935e02551` (byte-identical; gitignored).

## 17. Confirmation — successor-state is a sibling artefact, not a manifest mutation

The successor-state JSON records `successor_state_is_sibling_not_manifest_mutation = true`, `manifest_mutation_performed = false`, and `flip_research_eligible_invoked = false`. The marker exists only as a gitignored sibling successor-state JSON; it is never written to the label manifest. Any future tool that wishes to interpret the v002 label family as carrying the `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` policy must read this successor-state artefact, **not** the original label manifest (whose `chronological_split_policy` remains `"not_yet_defined"`). The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked by Phase 4bm-U).

## 18. Confirmation — no `data/microstructure` artefact committed

Phase 4bm-U writes exactly two new files under `data/microstructure/successor-state/labels/` (the successor-state JSON and its sidecar). Both are gitignored under `.gitignore:85: data/microstructure/` and neither appears in `git status --short` (which shows only the pre-existing untracked `data/research/`). The only tracked changes are this implementation report, the paired closeout, and the narrow `current-project-state.md` update. **Phase 4bm-U does not commit data/microstructure.**

## 19. Confirmation — diagnostics / ML / strategy / backtests remain unauthorized

The successor-state JSON records `diagnostics_authorized = false`, `ml_authorized = false`, `strategy_authorized = false`, and `backtest_authorized = false`. No diagnostics, ML, strategy, or backtest work was performed or authorized. **Phase 4bm-U does not authorize diagnostics, ML, strategy, or backtests.**

## 20. Confirmation — acquisition remains unauthorized

The successor-state JSON records `acquisition_authorized = false`. No data was acquired; no endpoint was called; no WebSocket was opened; no credential / `.env` / `.mcp.json` was read or created; MCP / Graphify was not enabled. **Phase 4bm-U does not authorize acquisition.**

## 21. Confirmation — research execution remains unauthorized

The successor-state JSON records `research_execution_authorized = false`. Phase 4bm-U records a chronological-split governance marker only; it neither runs nor authorizes any row-level research execution, split-mask materialization, diagnostic, or evaluation. **Phase 4bm-U does not authorize research execution.**

## 22. Label-family identity (recorded in the successor-state JSON)

| Item | Value |
| --- | --- |
| `family_id` | `microstructure_labels_aggtrades_v001` |
| `dataset_version` | `v002` |
| `label_schema_version` | `v001` |
| `symbol` | `BTCUSDT` |
| `date_start` | `2024-12-01` |
| `date_end` | `2025-02-28` |
| `expected_date_count` | `90` |
| `label_partition_count` | `90` |
| `label_sidecar_count` | `90` |
| `total_label_rows` | `155153449` |
| `horizons` | `1s`, `5s`, `15s`, `60s` |
| `max_forward_horizon_seconds` | `60` |
| `label_config_hash` | `352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560` |
| `feature_config_hash` | `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d` |

Label parquet/sidecar counts independently verified at **90 / 90** on disk.

## 23. Evidence chain and evidence SHAs (recorded in the successor-state JSON)

Evidence chain: Phase 4bm-S `LABEL_FAMILY_RESEARCH_USE_APPROVED_IN_PRINCIPLE` → Phase 4bm-T `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` memo-level policy.

| Artefact | SHA256 | Status |
| --- | --- | --- |
| v002 label manifest | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` | IDENTICAL |
| v002 label manifest sidecar | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` | IDENTICAL |
| Phase 4bm-Q gate report | `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` | IDENTICAL |
| Phase 4bm-Q gate report sidecar | `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` | IDENTICAL |
| Phase 4bm-S successor-state JSON | `081730006c11360692db0a99d59a0ed499f762ef4f86d6e29bdf3016550abfe7` | IDENTICAL |
| Phase 4bm-S successor-state sidecar | `05597fe4d568f5644ad9acc914f8a3b429bc7984cf7df3a2ac3f8c7935e02551` | IDENTICAL |
| Phase 4bm-T merge commit | `14e52c369031bce37cda83cfc79f345b57c6ff15` | on `main` |
| Phase 4bm-T merge-closeout commit | `d3ee2f7995ee540b518e19bcd88bfbf3243565c4` | on `main` |
| Phase 4bm-T SHA-finalization commit | `f7c8cb674bc08925df8e5f5765008cc92a403d08` | on `main` (base) |
| **NEW** Phase 4bm-U split-policy successor-state JSON | `6834ab11a5ac5d93b4d9f14d9b71ef3acb2a279bd8e3189fd22421598675fc9c` | NEW (gitignored) |
| **NEW** Phase 4bm-U split-policy successor-state sidecar | `fa9ae709add4541111e70cfc03d9126ac40f136ea2ce1aa1abe299d3412ac0b6` | NEW (gitignored) |

The 90 v002 per-day label Parquets and their 90 paired sidecars are byte-identical pre/post Phase 4bm-U by construction (Phase 4bm-U reads no Parquet, runs no kernel, and writes nothing outside the two new files under `data/microstructure/successor-state/labels/`).

## 24. Retained verdicts preserved

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

## 25. Project locks preserved

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 4ak M0 twelve-clause gate
- Phase 4al refined no-rescue rule
- Phase 4aw `flip_research_eligible` always-raises invariant (preserved; never invoked by Phase 4bm-U)
- Phase 4bb-F canonical sidecar/path policy
- Phase 4bl-F risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks
- Phase 4bm-A-P1 context management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace standard

All prior phase results (Phase 4am .. Phase 4bm-T) preserved verbatim.

## 26. Boundary confirmations

The successor-state JSON `boundary_confirmations` block records (all `true`): no manifest mutated; no Phase 4bm-S successor-state mutation; no data committed; no diagnostics; no ML; no strategy; no backtests; no acquisition; no research execution; no successor phase authorized; no endpoint calls; no credentials; no `.env`; no `.mcp.json`; no MCP; no Graphify.

## 27. Validation summary

- Pre-write re-hash of the v002 label manifest, manifest sidecar, Phase 4bm-Q gate report, gate report sidecar, Phase 4bm-S successor-state JSON, and Phase 4bm-S successor-state sidecar — all six MATCH expected SHAs.
- Successor-state JSON + sidecar written by a one-off Python writer at the repo root that was deleted immediately after the successful write and was never committed.
- Sidecar canonical Phase 4bb-F format byte-verified (two spaces; LF terminator; no CRLF; no BOM; 156 bytes; embedded SHA matches JSON SHA).
- Post-write re-hash of all six evidence artefacts — all six byte-identical to pre-write values.
- `git check-ignore -v` confirms both new files gitignored under `.gitignore:85: data/microstructure/`.
- `git status --short` shows only `data/research/` (no `data/microstructure/` entry; new files do not appear).
- `git diff --check` clean (exit 0).
- Label parquet/sidecar counts verified at 90/90.
- `ruff` / `mypy` / `pytest` deliberately not run (no source / test / committed-script modified; consistent with the Tier 1 docs + local gitignored successor-state-recording precedent of Phase 4bj-G / 4bj-J / 4bm-F / 4bm-L / 4bm-S). No project-specific markdown-lint gate exists in this repository; none invented.

## 28. Non-authorization

Phase 4bm-U does **not**, and **cannot**, authorize: Phase 4bm-V or any successor phase; multi-day v002 diagnostics; ML training / model selection / feature ranking / meta-labeling; strategy specification / implementation / signal construction; backtest specification / plan / execution; row-level research execution; split-mask materialization; additional acquisition; public / authenticated / private endpoint calls; WebSocket connections; credentials / `.env` / `.mcp.json` / MCP / Graphify; production-key creation; exchange-write; live-readiness; deployment; paper / shadow / live; Phase 5; Phase 4 canonical; amendment of any project lock; revision of any retained verdict. **Phase 4bm-V is not authorized by Phase 4bm-U.**

## 29. Recommended next state

**Remain paused.** Phase 4bm-U is branch-complete only by this work. Per the Phase 4bk-A workflow standard, it is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1). **Recommended state remains paused.**
