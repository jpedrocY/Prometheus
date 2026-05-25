# Phase 4bm-S — Merge-Closeout

**Phase identity:** Phase 4bm-S — Multi-Day V002 Label-Family Research-Use Successor-State Recording (docs + local gitignored successor-state JSON + paired canonical Phase 4bb-F sidecar).
**Date:** 2026-05-25.
**Risk tier:** Tier 1 — Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` §3.
**Merge-closeout standard:** `docs/00-meta/process/merge-closeout-standard.md`.

**Phase 4bm-S is now merge-complete on main.**

---

## 1. Phase identity

Phase 4bm-S records the machine-readable label-family research-use successor-state marker for the multi-day v002 label family `microstructure_labels_aggtrades_v001 @ v002` (BTCUSDT × 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 rows; 4 horizons 1s / 5s / 15s / 60s; `label_config_hash = 352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560`) as a sibling successor-state JSON artefact under `data/microstructure/successor-state/labels/`, while preserving the original v002 label manifest and the Phase 4bm-Q label-family eligibility gate report byte-identically. Multi-day v002 label analogue of Phase 4bj-G; v002 label sibling of Phase 4bm-L. Successor-state result: `LABEL_FAMILY_RESEARCH_USE_APPROVED_IN_PRINCIPLE`.

## 2. Source branch

`phase-4bm-s/multi-day-v002-label-family-research-use-successor-state`

## 3. Base SHA

`e2fdbdd6d7388235c2e4495072455c2ae787349d` (Phase 4bm-R merge-closeout SHA-finalization commit; `main == origin/main` before merge).

## 4. Branch tip SHA before merge

`10ba13753b721c2e21abeeed7224c2dbed31264b`

## 5. Merge commit SHA

`3df3c3b16714149e9e6d5a9cd73df25f18e00fe8` (`git merge --no-ff`, strategy `ort`).

## 6. Merge-closeout commit SHA

Recorded in §7 of the SHAs section below after the merge-closeout commit is made (this report is committed by `docs(phase-4bm-s): add merge closeout`). The closeout commit SHA cannot self-reference; it is finalized in the subsequent SHA-finalization commit and captured in the final operator report and git log.

## 7. SHAs section (final SHA-finalization plan)

| Item | SHA |
| --- | --- |
| Base SHA | `e2fdbdd6d7388235c2e4495072455c2ae787349d` |
| Branch tip SHA before merge | `10ba13753b721c2e21abeeed7224c2dbed31264b` |
| Merge commit SHA | `3df3c3b16714149e9e6d5a9cd73df25f18e00fe8` |
| Merge-closeout commit SHA | _to be recorded in the SHA-finalization edit (commit `docs(phase-4bm-s): add merge closeout`)_ |
| SHA-finalization commit SHA | _the commit `docs(phase-4bm-s): finalize merge closeout shas`; captured in the final operator report and in git log; after this commit final `main` == final `origin/main` == this SHA_ |

**SHA-finalization plan:** following the repo convention used for Phase 4bm-R / 4bm-Q / 4bm-P, the merge-closeout commit SHA is filled in by a follow-up SHA-finalization edit (this section), and the SHA-finalization commit's own SHA is captured in the final operator report and git log rather than by impossible self-reference. After the SHA-finalization commit is pushed, final `main` SHA == final `origin/main` SHA == the SHA-finalization commit.

## 8. Validation commands and results

| Command | Result |
| --- | --- |
| `git diff --stat main..<branch>` (pre-merge) | 3 files changed, 326 insertions(+) |
| `git diff --name-status main..<branch>` (pre-merge) | `M current-project-state.md`, `A 2026-05-25_phase-4bm-s_closeout.md`, `A 2026-05-25_phase-4bm-s_multi-day-v002-label-family-research-use-successor-state.md` |
| `git diff --check main..<branch>` (pre-merge) | clean (exit 0) |
| `git status --short` (pre/post merge) | only `data/research/` untracked; no `data/microstructure/` entry |
| Successor-state JSON SHA256 | `081730006c11360692db0a99d59a0ed499f762ef4f86d6e29bdf3016550abfe7` (matches closeout) |
| Successor-state sidecar SHA256 | `05597fe4d568f5644ad9acc914f8a3b429bc7984cf7df3a2ac3f8c7935e02551` (matches closeout) |
| `git check-ignore -v` (JSON + sidecar) | `.gitignore:85: data/microstructure/` for both |
| v002 label manifest SHA256 | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` (byte-identical) |
| v002 label manifest sidecar SHA256 | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` (byte-identical) |
| Phase 4bm-Q gate report SHA256 | `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` (byte-identical) |
| Phase 4bm-Q gate report sidecar SHA256 | `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` (byte-identical) |
| Label parquet / sidecar counts | 90 / 90 |
| `ruff` / `mypy` / `pytest` | deliberately not run (no source / test / script modified; consistent with Tier 1 docs + local gitignored successor-state-recording precedent of Phase 4bj-G / 4bm-F / 4bm-L) |
| Markdown lint | no project-specific gate exists in this repository; none invented |

## 9. File inventory / changed files

Merged tracked changes (3 files, 326 insertions):

- `docs/00-meta/current-project-state.md` (modified — Phase 4bm-S "Current phase:" block prepended; Phase 4bm-R block preserved as labelled historical context)
- `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-s_multi-day-v002-label-family-research-use-successor-state.md` (added)
- `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-s_closeout.md` (added)

This merge-closeout (`2026-05-25_phase-4bm-s_merge-closeout.md`) is committed separately on `main`. No source / test / script / configuration / manifest / sidecar / gate-report / successor-state file was modified by the merge.

## 10. Successor-state JSON path and SHA256

- Path: `data/microstructure/successor-state/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-s__1779715783843__e2fdbdd6d738.json`
- SHA256: `081730006c11360692db0a99d59a0ed499f762ef4f86d6e29bdf3016550abfe7` (7,518 bytes)

## 11. Successor-state sidecar path and SHA256

- Path: `data/microstructure/successor-state/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-s__1779715783843__e2fdbdd6d738.json.sha256`
- SHA256: `05597fe4d568f5644ad9acc914f8a3b429bc7984cf7df3a2ac3f8c7935e02551` (156 bytes; canonical Phase 4bb-F two-space format; LF only; no CRLF; no BOM)

## 12. Confirmation — successor-state JSON and sidecar gitignored and not committed

Both files match `.gitignore:85: data/microstructure/`, do not appear in `git status`, and are not part of the merged tree. They remain local gitignored outputs only.

## 13. Confirmation — no data/microstructure artefact committed

No file under `data/microstructure/` is staged or committed by this merge or by the closeout commits. `git status --short` shows only `data/research/`. **Phase 4bm-S does not commit data/microstructure.**

## 14. Confirmation — v002 label manifest preserved byte-identically

`data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json` SHA256 `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` (unchanged). **Phase 4bm-S preserves the v002 label manifest byte-identically.**

## 15. Confirmation — v002 label manifest sidecar preserved byte-identically

`data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json.sha256` SHA256 `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` (unchanged).

## 16. Confirmation — Phase 4bm-Q gate report preserved byte-identically

`data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-q__1779708036319__3f87123175e0.json` SHA256 `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` (unchanged; gate not re-run). **Phase 4bm-S preserves the Phase 4bm-Q gate report byte-identically.**

## 17. Confirmation — Phase 4bm-Q gate report sidecar preserved byte-identically

`data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-q__1779708036319__3f87123175e0.json.sha256` SHA256 `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` (unchanged).

## 18. Confirmation — successor-state is a sibling artefact only, not a manifest mutation

The successor-state JSON records `successor_state_is_sibling_not_manifest_mutation = true` and `manifest_mutation_performed = false`. **Phase 4bm-S records label-family research-use admissibility as a sibling successor-state artefact only.** **Phase 4bm-S does not mutate any manifest.**

## 19. Confirmation — no flip_research_eligible invocation

The successor-state JSON records `flip_research_eligible_invoked = false`. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked). **Phase 4bm-S does not invoke flip_research_eligible.**

## 20. Confirmation — chronological split policy remains not_yet_defined

The label manifest's `chronological_split_policy` remains `"not_yet_defined"`; the successor-state JSON records `chronological_split_policy_defined = false`. **Chronological split policy remains not_yet_defined.** **Phase 4bm-S does not define chronological split policy.**

## 21. Confirmation — diagnostics / ML / strategy / backtests remain unauthorized

The successor-state JSON records `diagnostics_authorized = false`, `ml_authorized = false`, `strategy_authorized = false`, `backtest_authorized = false`. **Diagnostics / ML / strategy / backtests remain unauthorized.** **Phase 4bm-S does not authorize diagnostics, ML, strategy, or backtests.**

## 22. Confirmation — acquisition remains unauthorized

The successor-state JSON records `acquisition_authorized = false`. No data acquired; no endpoint / WebSocket / credential / `.env` / `.mcp.json` / MCP / Graphify touched. **Phase 4bm-S does not authorize acquisition.**

## 23. Confirmation — Phase 4bm-T and all successors remain unauthorized

`phase_4bm_t_or_successor_authorized = false`, `phase_5_authorized = false`, `paper_shadow_live_deployment_exchange_write_authorized = false`. **Phase 4bm-T is not authorized by Phase 4bm-S.** No successor phase, Phase 5, paper / shadow / live-readiness / deployment / exchange-write / production-key / authenticated-API / private-endpoint / user-stream / WebSocket / MCP / Graphify work is authorized.

## 24. Retained verdicts preserved

H0 (FRAMEWORK ANCHOR), R3 (BASELINE-OF-RECORD), R1a (RETAINED — NON-LEADING), R1b-narrow (RETAINED — NON-LEADING), R2 (FAILED — §11.6), F1 (HARD REJECT), D1-A (MECHANISM PASS / FRAMEWORK FAIL), 5m thread (OPERATIONALLY CLOSED), V2 (HARD REJECT — terminal for V2 first-spec), G1 (HARD REJECT — terminal for G1 first-spec), C1 (HARD REJECT — terminal for C1 first-spec) — all preserved verbatim.

## 25. Project locks preserved

§11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 = 0.25% / 2× / one-position / mark-price stops; Phase 4ak M0 twelve-clause gate; Phase 4al refined no-rescue rule; Phase 4aw `flip_research_eligible` always-raises invariant (never invoked); Phase 4bb-F canonical sidecar/path policy; Phase 4bl-F risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks; Phase 4bm-A-P1 context management standard; Phase 4bm-D-P1 lightweight Claude Code workspace standard; all other locks recorded in `current-project-state.md` and the latest merge-closeout — all preserved verbatim.

## 26. Known caveats

- The successor-state JSON and sidecar are local gitignored outputs; they are not in version control. Any environment that needs the machine-readable marker must regenerate or copy them locally. The deterministic payload reproduces SHA `081730006c…` only if the same `created_at` / timestamp / code-commit reference are re-supplied.
- `ruff` / `mypy` / `pytest` were not run (no source / test / script modified). No markdown-lint gate exists in the repo; none invented.

## 27. Recommended state

**Remain paused.** Phase 4bm-S is now project-complete after this merge-closeout and its SHA-finalization. No successor phase is authorized. **Phase 4bm-T is not authorized by Phase 4bm-S.** **Recommended state remains paused.**
