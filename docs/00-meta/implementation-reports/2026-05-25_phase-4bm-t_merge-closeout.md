# Phase 4bm-T — Merge-Closeout

**Phase identity:** Phase 4bm-T — Multi-Day V002 Chronological Split-Policy Memo (docs-only governance / methodology memo; multi-day v002 analogue of the v001 Phase 4bj-H / 4bj-I / 4bj-J chronological-split-policy phases).
**Date:** 2026-05-25.
**Risk tier:** Tier 1 — Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` §3.
**Merge-closeout standard:** `docs/00-meta/process/merge-closeout-standard.md`.

**Phase 4bm-T is now merge-complete on main.**

---

## 1. Phase identity

Phase 4bm-T recorded, at memo level only, a conservative formal chronological train / validation / test split policy for the 90-day multi-day v002 label family `microstructure_labels_aggtrades_v001 @ v002` (BTCUSDT × 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 rows; 4 horizons 1s / 5s / 15s / 60s; `label_config_hash = 352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560`), which is research-use approved in principle through the sibling Phase 4bm-S successor-state artefact (`LABEL_FAMILY_RESEARCH_USE_APPROVED_IN_PRINCIPLE`). The chosen policy is `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`. **Phase 4bm-T is a docs-only chronological split-policy memo.**

## 2. Source branch

`phase-4bm-t/multi-day-v002-chronological-split-policy-memo`

## 3. Base SHA

`ab1269d4c0b46e95961542e032173eb9a098be32` (Phase 4bm-S merge-closeout SHA-finalization commit; `main == origin/main` before merge).

## 4. Branch tip SHA before merge

`72b3e266deddbc926a3d75fa7327ec282cc30f08`

## 5. Merge commit SHA

`14e52c369031bce37cda83cfc79f345b57c6ff15` (`git merge --no-ff`, strategy `ort`).

## 6. Merge-closeout commit SHA

`d3ee2f7995ee540b518e19bcd88bfbf3243565c4` (commit `docs(phase-4bm-t): add merge closeout`). The closeout commit SHA cannot self-reference; it is filled in by this SHA-finalization commit and captured in the final operator report and git log.

## 7. SHAs section (final SHA-finalization plan)

| Item | SHA |
| --- | --- |
| Base SHA | `ab1269d4c0b46e95961542e032173eb9a098be32` |
| Branch tip SHA before merge | `72b3e266deddbc926a3d75fa7327ec282cc30f08` |
| Merge commit SHA | `14e52c369031bce37cda83cfc79f345b57c6ff15` |
| Merge-closeout commit SHA | `d3ee2f7995ee540b518e19bcd88bfbf3243565c4` (commit `docs(phase-4bm-t): add merge closeout`) |
| SHA-finalization commit SHA | the commit `docs(phase-4bm-t): finalize merge closeout shas` (this edit); captured in the final operator report and in git log; after this commit final `main` == final `origin/main` == this SHA |

**SHA-finalization plan:** following the repo convention used for Phase 4bm-S / 4bm-R / 4bm-Q, the merge-closeout commit SHA is filled in by a follow-up SHA-finalization edit (this section), and the SHA-finalization commit's own SHA is captured in the final operator report and git log rather than by impossible self-reference. After the SHA-finalization commit is pushed, final `main` SHA == final `origin/main` SHA == the SHA-finalization commit.

## 8. Validation commands and results

| Command | Result |
| --- | --- |
| `git diff --stat main..<branch>` (pre-merge) | 3 files changed, 450 insertions(+) |
| `git diff --name-status main..<branch>` (pre-merge) | `M current-project-state.md`, `A 2026-05-25_phase-4bm-t_closeout.md`, `A 2026-05-25_phase-4bm-t_multi-day-v002-chronological-split-policy-memo.md` |
| `git diff --check main..<branch>` (pre-merge) | clean (exit 0) |
| `git status --short` (pre/post merge) | only `data/research/` untracked; no `data/microstructure/` entry |
| Phase 4bm-S successor-state JSON SHA256 | `081730006c11360692db0a99d59a0ed499f762ef4f86d6e29bdf3016550abfe7` (byte-identical; matches Phase 4bm-S closeout) |
| Phase 4bm-S successor-state sidecar SHA256 | `05597fe4d568f5644ad9acc914f8a3b429bc7984cf7df3a2ac3f8c7935e02551` (byte-identical) |
| `git check-ignore -v` (Phase 4bm-S JSON + sidecar) | `.gitignore:85: data/microstructure/` for both |
| v002 label manifest SHA256 | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` (byte-identical) |
| v002 label manifest sidecar SHA256 | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` (byte-identical) |
| Phase 4bm-Q gate report SHA256 | `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` (byte-identical) |
| Phase 4bm-Q gate report sidecar SHA256 | `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` (byte-identical) |
| Label parquet / sidecar counts | 90 / 90 |
| `ruff` / `mypy` / `pytest` | deliberately not run (no source / test / script modified; docs-only Tier 1 governance memo, consistent with the Phase 4bj-H / 4bj-I / 4bm-R docs-only-memo precedent) |
| Markdown lint | no project-specific gate exists in this repository; none invented |

## 9. File inventory / changed files

Merged tracked changes (3 files, 450 insertions):

- `docs/00-meta/current-project-state.md` (modified — Phase 4bm-T "Current phase:" block prepended; Phase 4bm-S block preserved as labelled historical context)
- `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-t_multi-day-v002-chronological-split-policy-memo.md` (added)
- `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-t_closeout.md` (added)

This merge-closeout (`2026-05-25_phase-4bm-t_merge-closeout.md`) is committed separately on `main`. No source / test / script / configuration / manifest / sidecar / gate-report / successor-state file was modified by the merge.

## 10. Chosen split policy name

`CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`.

## 11. Train / validation / test windows

| Split | UTC window (inclusive) | Dates | Share | Permitted use |
| --- | --- | --- | --- | --- |
| Train | 2024-12-01 .. 2025-01-14 | 45 | 50.0% | model fitting only |
| Validation | 2025-01-15 .. 2025-02-13 | 30 | 33.3% | model / hyperparameter / threshold selection only |
| Test / final holdout | 2025-02-14 .. 2025-02-28 | 15 | 16.7% | single-use final confirmatory measurement only |
| Total | 2024-12-01 .. 2025-02-28 | 90 | 100% | — |

Date-count arithmetic: train = 31 (Dec 2024) + 14 (Jan 1–14 2025) = 45; validation = 17 (Jan 15–31 2025) + 13 (Feb 1–13 2025) = 30; test = 15 (Feb 14–28 2025); total = 90. Assignment by source event timestamp UTC date (`source_transact_time_ms`, anchor-row UTC date); deterministic order `(feature_timestamp_ms, agg_trade_id, row_index)` preserved.

## 12. Boundary-crossing / horizon leakage rule

For any future row-level research, a row is invalid for a given split if any required label horizon or forward-looking support window crosses from that split into a later split. Boundary-crossing rows are **excluded from the earlier split**, never reassigned forward, unless a future separately authorized memo defines a stricter rule. Per-row masks only; no parquet rewrite. The Phase 4bm-N / 4bm-M envelope-terminal censoring (`{1s:14, 5s:39, 15s:170, 60s:634}`) at `2025-02-28 23:59:59.996Z` applies additively at the test-window right edge.

## 13. Minimum 60-second boundary embargo

Because the maximum declared label horizon is 60 seconds, a minimum 60-second embargo is required at the train/validation boundary (`2025-01-15 00:00:00Z`) and the validation/test boundary (`2025-02-14 00:00:00Z`) for any future row-level research execution. A larger operational embargo may be recommended if justified but must not be reduced below 60 seconds.

## 14. No-shuffle rule

No random split, shuffled cross-validation, k-fold-over-time, bootstrap, or post-hoc temporal resampling is allowed for this 90-day family unless a later separately authorized methodology memo explicitly supersedes this policy. All partitioning is strictly chronological and forward-in-time.

## 15. Holdout rule

The test / final holdout window (2025-02-14 .. 2025-02-28; 15 dates) is single-use and must not be used for feature selection, model selection, hyperparameter selection, threshold tuning, strategy design, diagnostic iteration, or eligibility rescue. Validation is the only selection/tuning window; train is the only fitting window.

## 16. Confirmation — chronological split policy is defined at memo level only

**The chronological split policy is defined at memo level only.** The policy `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` exists only in the Phase 4bm-T memo + closeout text and the narrow `current-project-state.md` block; it is not encoded in any manifest field or any machine-readable artefact. **Any chronological split-policy recording requires a separately authorized successor-state phase.**

## 17. Confirmation — no chronological split successor-state JSON was created

**Phase 4bm-T does not create chronological split successor-state JSON.** No split artefact, no successor-state JSON, and no split mask were written anywhere; the phase is docs-only.

## 18. Confirmation — no manifest was mutated

**Phase 4bm-T does not mutate any manifest.** The v002 label manifest's `chronological_split_policy` remains `"not_yet_defined"`; SHA `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` byte-identical pre/post. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked).

## 19. Confirmation — Phase 4bm-S successor-state artefact was not mutated

**Phase 4bm-T does not mutate the Phase 4bm-S successor-state artefact.** Successor-state JSON SHA256 `081730006c11360692db0a99d59a0ed499f762ef4f86d6e29bdf3016550abfe7` and sidecar SHA256 `05597fe4d568f5644ad9acc914f8a3b429bc7984cf7df3a2ac3f8c7935e02551` re-hashed byte-identical; both remain gitignored under `.gitignore:85: data/microstructure/`.

## 20. Confirmation — no data/microstructure artefact was committed

**Phase 4bm-T does not commit data/microstructure.** No file under `data/microstructure/` is staged or committed by this merge or by the closeout commits. `git status --short` shows only `data/research/`.

## 21. Confirmation — v002 label manifest preserved byte-identically

`data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json` SHA256 `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` (unchanged).

## 22. Confirmation — v002 label manifest sidecar preserved byte-identically

`data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json.sha256` SHA256 `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` (unchanged).

## 23. Confirmation — Phase 4bm-S successor-state JSON preserved byte-identically

`data/microstructure/successor-state/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-s__1779715783843__e2fdbdd6d738.json` SHA256 `081730006c11360692db0a99d59a0ed499f762ef4f86d6e29bdf3016550abfe7` (unchanged; gitignored).

## 24. Confirmation — Phase 4bm-S successor-state sidecar preserved byte-identically

`data/microstructure/successor-state/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-s__1779715783843__e2fdbdd6d738.json.sha256` SHA256 `05597fe4d568f5644ad9acc914f8a3b429bc7984cf7df3a2ac3f8c7935e02551` (unchanged; gitignored).

## 25. Confirmation — Phase 4bm-Q gate report preserved byte-identically

`data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-q__1779708036319__3f87123175e0.json` SHA256 `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` (unchanged; gate not re-run).

## 26. Confirmation — Phase 4bm-Q gate report sidecar preserved byte-identically

`data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-q__1779708036319__3f87123175e0.json.sha256` SHA256 `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` (unchanged).

## 27. Confirmation — diagnostics / ML / strategy / backtests remain unauthorized

**Phase 4bm-T does not authorize diagnostics, ML, strategy, or backtests.** No diagnostics / ML / strategy / backtest work was performed or authorized. **Phase 4bm-T does not run any research execution.**

## 28. Confirmation — acquisition remains unauthorized

**Phase 4bm-T does not authorize acquisition.** No data acquired; no endpoint called; no WebSocket / user-stream opened; no credential / `.env` / `.mcp.json` read or created; MCP / Graphify not enabled.

## 29. Confirmation — Phase 4bm-U and all successors remain unauthorized

**Phase 4bm-U is not authorized by Phase 4bm-T.** No successor phase, no chronological split-policy successor-state recording phase, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production-key creation, authenticated-API, private-endpoint, user-stream, WebSocket, MCP, or Graphify work is authorized.

## 30. Retained verdicts preserved

H0 (FRAMEWORK ANCHOR), R3 (BASELINE-OF-RECORD), R1a (RETAINED — NON-LEADING), R1b-narrow (RETAINED — NON-LEADING), R2 (FAILED — §11.6), F1 (HARD REJECT), D1-A (MECHANISM PASS / FRAMEWORK FAIL), 5m thread (OPERATIONALLY CLOSED), V2 (HARD REJECT — terminal for V2 first-spec), G1 (HARD REJECT — terminal for G1 first-spec), C1 (HARD REJECT — terminal for C1 first-spec) — all preserved verbatim.

## 31. Project locks preserved

§11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 = 0.25% / 2× / one-position / mark-price stops; Phase 4ak M0 twelve-clause gate; Phase 4al refined no-rescue rule; Phase 4aw `flip_research_eligible` always-raises invariant (never invoked); Phase 4bb-F canonical sidecar/path policy; Phase 4bl-F risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks; Phase 4bm-A-P1 context management standard; Phase 4bm-D-P1 lightweight Claude Code workspace standard; all other locks recorded in `current-project-state.md` and the latest merge-closeout — all preserved verbatim.

## 32. Known caveats

- The 45 / 30 / 15 windows and the 60-second minimum embargo are recorded at memo level only; they become machine-readable only if a future separately authorized chronological-split-policy successor-state recording phase records them as a sibling artefact.
- The split ratio is expressed in UTC dates, not rows; row shares differ slightly because per-day row counts vary. The partition is defined by date boundaries, not row-count targets.
- The boundary-crossing exclusion rule and the 60s embargo are governance constraints on any future row-level research execution; this phase neither runs nor authorizes such execution.
- The Phase 4bm-S successor-state JSON + sidecar, the Phase 4bm-Q gate report + sidecar, and the v002 label manifest + sidecar are local gitignored outputs; they are not in version control. Any environment needing them must regenerate or copy them locally.
- `ruff` / `mypy` / `pytest` were not run (no source / test / script modified). No markdown-lint gate exists in the repo; none invented.

## 33. Recommended state

**Remain paused.** Phase 4bm-T is now project-complete after this merge-closeout and its SHA-finalization. No successor phase is authorized. **Phase 4bm-U is not authorized by Phase 4bm-T.** **Recommended state remains paused.**
