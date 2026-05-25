# Phase 4bm-U — Merge-Closeout

**Phase identity:** Phase 4bm-U — Multi-Day V002 Chronological Split-Policy Successor-State Recording (docs + local gitignored successor-state JSON + paired canonical Phase 4bb-F sidecar; multi-day v002 analogue of the v001 Phase 4bj-J split-policy successor-state recording, recording a formal-split policy rather than a no-split determination).
**Date:** 2026-05-25.
**Risk tier:** Tier 1 — Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` §3.
**Merge-closeout standard:** `docs/00-meta/process/merge-closeout-standard.md`.

**Phase 4bm-U is now merge-complete on main.**

---

## 1. Phase identity

Phase 4bm-U operationalised the Phase 4bm-T memo-level chronological split policy `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` into exactly one machine-readable sibling chronological-split-policy successor-state JSON artefact under `data/microstructure/successor-state/labels/`, while preserving the original v002 label manifest, the v002 label manifest sidecar, the Phase 4bm-S label-family research-use successor-state JSON + sidecar, and the Phase 4bm-Q label-family eligibility gate report + sidecar byte-identically. Successor-state result: `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` (split_policy_status `recorded`). **Phase 4bm-U records chronological split policy as a sibling successor-state artefact only.**

## 2. Source branch

`phase-4bm-u/multi-day-v002-chronological-split-policy-successor-state`

## 3. Base SHA

`f7c8cb674bc08925df8e5f5765008cc92a403d08` (Phase 4bm-T merge-closeout SHA-finalization commit; `main == origin/main` before merge).

## 4. Branch tip SHA before merge

`11e01f3ceb472225d35d43137df9244f99145e13`

## 5. Merge commit SHA

`af18a207ee7f53b1b3bd67e59348bfb4b3b0da31` (`git merge --no-ff`, strategy `ort`).

## 6. Merge-closeout commit SHA

`be87cc8044e3ff1c234635ad4d55f109595c0e99` (commit `docs(phase-4bm-u): add merge closeout`). The closeout commit SHA cannot self-reference; it is filled in by this SHA-finalization commit and captured in the final operator report and git log.

## 7. SHAs section (final SHA-finalization plan)

| Item | SHA |
| --- | --- |
| Base SHA | `f7c8cb674bc08925df8e5f5765008cc92a403d08` |
| Branch tip SHA before merge | `11e01f3ceb472225d35d43137df9244f99145e13` |
| Merge commit SHA | `af18a207ee7f53b1b3bd67e59348bfb4b3b0da31` |
| Merge-closeout commit SHA | `be87cc8044e3ff1c234635ad4d55f109595c0e99` (commit `docs(phase-4bm-u): add merge closeout`) |
| SHA-finalization commit SHA | the commit `docs(phase-4bm-u): finalize merge closeout shas` (this edit); captured in the final operator report and in git log; after this commit final `main` == final `origin/main` == this SHA |

**SHA-finalization plan:** following the repo convention used for Phase 4bm-T / 4bm-S / 4bm-R, the merge-closeout commit SHA is filled in by a follow-up SHA-finalization edit (this section), and the SHA-finalization commit's own SHA is captured in the final operator report and git log rather than by impossible self-reference. After the SHA-finalization commit is pushed, final `main` SHA == final `origin/main` SHA == the SHA-finalization commit.

## 8. Validation commands and results

| Command | Result |
| --- | --- |
| `git diff --stat main..<branch>` (pre-merge) | 3 files changed, 339 insertions(+) |
| `git diff --name-status main..<branch>` (pre-merge) | `M current-project-state.md`, `A 2026-05-25_phase-4bm-u_closeout.md`, `A 2026-05-25_phase-4bm-u_multi-day-v002-chronological-split-policy-successor-state.md` |
| `git diff --check main..<branch>` (pre-merge) | clean (exit 0) |
| `git status --short` (pre/post merge) | only `data/research/` untracked; no `data/microstructure/` entry |
| Phase 4bm-U successor-state JSON SHA256 | `6834ab11a5ac5d93b4d9f14d9b71ef3acb2a279bd8e3189fd22421598675fc9c` (matches closeout) |
| Phase 4bm-U successor-state sidecar SHA256 | `fa9ae709add4541111e70cfc03d9126ac40f136ea2ce1aa1abe299d3412ac0b6` (matches closeout) |
| `git check-ignore -v` (Phase 4bm-U JSON + sidecar) | `.gitignore:85: data/microstructure/` for both |
| Phase 4bm-S successor-state JSON SHA256 | `081730006c11360692db0a99d59a0ed499f762ef4f86d6e29bdf3016550abfe7` (byte-identical) |
| Phase 4bm-S successor-state sidecar SHA256 | `05597fe4d568f5644ad9acc914f8a3b429bc7984cf7df3a2ac3f8c7935e02551` (byte-identical) |
| v002 label manifest SHA256 | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` (byte-identical) |
| v002 label manifest sidecar SHA256 | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` (byte-identical) |
| Phase 4bm-Q gate report SHA256 | `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` (byte-identical) |
| Phase 4bm-Q gate report sidecar SHA256 | `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` (byte-identical) |
| Label parquet / sidecar counts | 90 / 90 |
| `ruff` / `mypy` / `pytest` | deliberately not run (no source / test / committed-script modified; docs + local gitignored successor-state Tier 1 precedent of Phase 4bj-G / 4bj-J / 4bm-F / 4bm-L / 4bm-S) |
| Markdown lint | no project-specific gate exists in this repository; none invented |

## 9. File inventory / changed files

Merged tracked changes (3 files, 339 insertions):

- `docs/00-meta/current-project-state.md` (modified — Phase 4bm-U "Current phase:" block prepended; Phase 4bm-T block preserved as labelled historical context)
- `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-u_multi-day-v002-chronological-split-policy-successor-state.md` (added)
- `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-u_closeout.md` (added)

This merge-closeout (`2026-05-25_phase-4bm-u_merge-closeout.md`) is committed separately on `main`. No source / test / committed-script / configuration / manifest / sidecar / gate-report / successor-state file was modified by the merge.

## 10. Successor-state JSON path and SHA256

- Path: `data/microstructure/successor-state/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-u__1779718408615__f7c8cb674bc0.json`
- SHA256: `6834ab11a5ac5d93b4d9f14d9b71ef3acb2a279bd8e3189fd22421598675fc9c` (6,050 bytes; ASCII; LF only; sorted keys; indent 2; final newline)

## 11. Successor-state sidecar path and SHA256

- Path: `data/microstructure/successor-state/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-u__1779718408615__f7c8cb674bc0.json.sha256`
- SHA256: `fa9ae709add4541111e70cfc03d9126ac40f136ea2ce1aa1abe299d3412ac0b6` (156 bytes; canonical Phase 4bb-F two-space format; LF only; no CRLF; no BOM)

## 12. Confirmation — successor-state JSON and sidecar gitignored and not committed

Both files match `.gitignore:85: data/microstructure/`, do not appear in `git status`, and are not part of the merged tree. They remain local gitignored outputs only.

## 13. Confirmation — no data/microstructure artefact committed

No file under `data/microstructure/` is staged or committed by this merge or by the closeout commits. `git status --short` shows only `data/research/`. **Phase 4bm-U does not commit data/microstructure.**

## 14. Confirmation — v002 label manifest preserved byte-identically

`data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json` SHA256 `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` (unchanged). **Phase 4bm-U preserves the v002 label manifest byte-identically.** The manifest continues to carry `chronological_split_policy = "not_yet_defined"`.

## 15. Confirmation — v002 label manifest sidecar preserved byte-identically

`data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json.sha256` SHA256 `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` (unchanged).

## 16. Confirmation — Phase 4bm-S successor-state JSON preserved byte-identically

`data/microstructure/successor-state/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-s__1779715783843__e2fdbdd6d738.json` SHA256 `081730006c11360692db0a99d59a0ed499f762ef4f86d6e29bdf3016550abfe7` (unchanged; gitignored). **Phase 4bm-U preserves the Phase 4bm-S successor-state byte-identically.**

## 17. Confirmation — Phase 4bm-S successor-state sidecar preserved byte-identically

`data/microstructure/successor-state/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-s__1779715783843__e2fdbdd6d738.json.sha256` SHA256 `05597fe4d568f5644ad9acc914f8a3b429bc7984cf7df3a2ac3f8c7935e02551` (unchanged; gitignored).

## 18. Confirmation — Phase 4bm-Q gate report preserved byte-identically

`data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-q__1779708036319__3f87123175e0.json` SHA256 `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` (unchanged; gate not re-run). **Phase 4bm-U preserves the Phase 4bm-Q gate report byte-identically.**

## 19. Confirmation — Phase 4bm-Q gate report sidecar preserved byte-identically

`data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-q__1779708036319__3f87123175e0.json.sha256` SHA256 `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` (unchanged).

## 20. Confirmation — successor-state is a sibling artefact only, not a manifest mutation

The successor-state JSON records `successor_state_is_sibling_not_manifest_mutation = true`, `manifest_mutation_performed = false`, and `flip_research_eligible_invoked = false`. Any future tool that wishes to interpret the v002 label family as carrying the `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` policy must read this sibling successor-state artefact, never the manifest. **Phase 4bm-U does not mutate any manifest.**

## 21. Confirmation — no manifest mutation

No manifest field was transitioned. The v002 label manifest's `research_eligible = false`, `eligibility_gate_status = "pending"`, `stage_5_label_cleared = false`, `label_family_research_use_authorized = false`, and `chronological_split_policy = "not_yet_defined"` are all unchanged. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked).

## 22. Confirmation — no Phase 4bm-S successor-state mutation

The Phase 4bm-S successor-state JSON and sidecar are byte-identical pre/post (see §16–§17). **Phase 4bm-U does not mutate the Phase 4bm-S successor-state artefact.**

## 23. Confirmation — diagnostics / ML / strategy / backtests remain unauthorized

The successor-state JSON records `diagnostics_authorized = false`, `ml_authorized = false`, `strategy_authorized = false`, and `backtest_authorized = false`. **Phase 4bm-U does not authorize diagnostics, ML, strategy, or backtests.**

## 24. Confirmation — acquisition remains unauthorized

The successor-state JSON records `acquisition_authorized = false`. No data acquired; no endpoint / WebSocket / credential / `.env` / `.mcp.json` / MCP / Graphify touched. **Phase 4bm-U does not authorize acquisition.**

## 25. Confirmation — research execution remains unauthorized

The successor-state JSON records `research_execution_authorized = false`. Phase 4bm-U records a chronological-split governance marker only; it neither runs nor authorizes any row-level research execution, split-mask materialization, diagnostic, or evaluation. **Phase 4bm-U does not authorize research execution.**

## 26. Confirmation — Phase 4bm-V and all successors remain unauthorized

`phase_4bm_v_or_successor_authorized = false`, `phase_5_authorized = false`, `paper_shadow_live_deployment_exchange_write_authorized = false`. **Phase 4bm-V is not authorized by Phase 4bm-U.** No successor phase, Phase 5, paper / shadow / live-readiness / deployment / exchange-write / production-key / authenticated-API / private-endpoint / user-stream / WebSocket / MCP / Graphify work is authorized.

## 27. Retained verdicts preserved

H0 (FRAMEWORK ANCHOR), R3 (BASELINE-OF-RECORD), R1a (RETAINED — NON-LEADING), R1b-narrow (RETAINED — NON-LEADING), R2 (FAILED — §11.6), F1 (HARD REJECT), D1-A (MECHANISM PASS / FRAMEWORK FAIL), 5m thread (OPERATIONALLY CLOSED), V2 (HARD REJECT — terminal for V2 first-spec), G1 (HARD REJECT — terminal for G1 first-spec), C1 (HARD REJECT — terminal for C1 first-spec) — all preserved verbatim.

## 28. Project locks preserved

§11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 = 0.25% / 2× / one-position / mark-price stops; Phase 4ak M0 twelve-clause gate; Phase 4al refined no-rescue rule; Phase 4aw `flip_research_eligible` always-raises invariant (never invoked); Phase 4bb-F canonical sidecar/path policy; Phase 4bl-F risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks; Phase 4bm-A-P1 context management standard; Phase 4bm-D-P1 lightweight Claude Code workspace standard; all other locks recorded in `current-project-state.md` and the latest merge-closeout — all preserved verbatim.

## 29. Known caveats

- The Phase 4bm-U successor-state JSON + sidecar are local gitignored outputs; they are not in version control. Any environment that needs the machine-readable marker must regenerate or copy them locally. The deterministic payload reproduces SHA `6834ab11…` only if the same `created_at_unix_ms = 1779718408615` / code-commit reference are re-supplied.
- The recorded policy lives only in the sibling artefact; the v002 label manifest's `chronological_split_policy` remains `"not_yet_defined"`. Readers must consult the successor-state JSON, not the manifest.
- The split ratio (45/30/15) is expressed in UTC dates, not rows; row shares differ slightly because per-day row counts vary. The boundary-crossing exclusion rule and the 60s embargo are governance constraints on any future row-level research execution; this phase neither runs nor authorizes such execution.
- `ruff` / `mypy` / `pytest` were not run (no source / test / committed-script modified). No markdown-lint gate exists in the repo; none invented.

## 30. Recommended state

**Remain paused.** Phase 4bm-U is now project-complete after this merge-closeout and its SHA-finalization. No successor phase is authorized. **Phase 4bm-V is not authorized by Phase 4bm-U.** **Recommended state remains paused.**
