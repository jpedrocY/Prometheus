# Phase 4bm-T — Closeout

**Phase identity:** Phase 4bm-T — Multi-Day V002 Chronological Split-Policy Memo (docs-only governance / methodology memo).
**Date:** 2026-05-25.
**Branch:** `phase-4bm-t/multi-day-v002-chronological-split-policy-memo`.
**Base SHA:** `main` at `ab1269d4c0b46e95961542e032173eb9a098be32` (Phase 4bm-S merge-closeout SHA-finalization commit).
**Risk tier:** Tier 1 — Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` §3.
**Status:** branch-complete only by this work; not merged into `main`; not project-complete.

---

## 1. Required exact phrases

- **Phase 4bm-T is a docs-only chronological split-policy memo.**
- **Phase 4bm-T does not create chronological split successor-state JSON.**
- **Phase 4bm-T does not mutate any manifest.**
- **Phase 4bm-T does not mutate the Phase 4bm-S successor-state artefact.**
- **Phase 4bm-T does not commit data/microstructure.**
- **Phase 4bm-T does not authorize diagnostics, ML, strategy, or backtests.**
- **Phase 4bm-T does not authorize acquisition.**
- **Phase 4bm-T does not run any research execution.**
- **The chronological split policy is defined at memo level only.**
- **Any chronological split-policy recording requires a separately authorized successor-state phase.**
- **Phase 4bm-U is not authorized by Phase 4bm-T.**
- **Recommended state remains paused.**

---

## 2. What Phase 4bm-T did

Phase 4bm-T recorded, at memo level only, a conservative formal chronological train / validation / test split policy for the 90-day multi-day v002 label family `microstructure_labels_aggtrades_v001 @ v002` (BTCUSDT × 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 rows; 4 horizons 1s / 5s / 15s / 60s), which is research-use approved in principle through the sibling Phase 4bm-S successor-state artefact.

The chosen policy is **`CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`**, aligned with the v001 Phase 4bj-H / 4bj-I / 4bj-J precedent (which deferred a formal split for the v001 single-day cell only until multi-day data — "at least 30 distinct UTC days" — existed; v002's 90 dates satisfy that precondition) and with the Phase 4bm-M v002 multi-day timestamp / leakage / no-shuffle / envelope-terminal-censoring policy.

Tracked changes (3 files): this closeout, the chronological split-policy memo, and a narrow `docs/00-meta/current-project-state.md` update (new Phase 4bm-T "Current phase:" block prepended; prior Phase 4bm-S block preserved as labelled historical context). No local data artefact created.

---

## 3. Chosen split policy (summary)

| Split | UTC window (inclusive) | Dates | Share | Permitted use |
| --- | --- | --- | --- | --- |
| Train | 2024-12-01 .. 2025-01-14 | 45 | 50.0% | model fitting only |
| Validation | 2025-01-15 .. 2025-02-13 | 30 | 33.3% | model / hyperparameter / threshold selection only |
| Test / final holdout | 2025-02-14 .. 2025-02-28 | 15 | 16.7% | single-use final confirmatory measurement only |
| Total | 2024-12-01 .. 2025-02-28 | 90 | 100% | — |

- **Assignment rule:** by source event timestamp UTC date (`source_transact_time_ms`, anchor row UTC date); deterministic order `(feature_timestamp_ms, agg_trade_id, row_index)` preserved.
- **Boundary leakage / embargo rule:** because the maximum declared label horizon is 60 seconds, a minimum 60-second embargo is required at the train/validation boundary (`2025-01-15 00:00:00Z`) and the validation/test boundary (`2025-02-14 00:00:00Z`). Boundary-crossing rows (any required horizon reaching at/after the next boundary) are **excluded from the earlier split**, never reassigned forward, unless a future separately authorized memo defines a stricter rule. A larger operational embargo may be recommended but must not drop below 60s. Per-row masks only; no parquet rewrite. Envelope-terminal censoring (per-horizon `{1s:14, 5s:39, 15s:170, 60s:634}`) applies additively at the 2025-02-28 right edge.
- **No-shuffle rule:** no random / shuffled / k-fold-over-time / bootstrap / post-hoc resampling split unless a later separately authorized methodology memo supersedes this policy.
- **Holdout rule:** the test window is single-use; it must not be used for feature selection, model selection, hyperparameter selection, threshold tuning, strategy design, diagnostic iteration, or eligibility rescue.

---

## 4. Validation commands and results

| Command | Result |
| --- | --- |
| `git status --short` | only `data/research/` untracked; no `data/microstructure/` entry |
| `git diff --check` | clean (exit 0) |
| `git diff --name-only` (working tree) | only the three tracked docs paths |
| `git diff --name-only --cached` (after staging) | only the three tracked docs paths |
| Phase 4bm-S successor-state JSON re-hash | `081730006c11360692db0a99d59a0ed499f762ef4f86d6e29bdf3016550abfe7` (MATCH; gitignored) |
| Phase 4bm-S successor-state sidecar re-hash | `05597fe4d568f5644ad9acc914f8a3b429bc7984cf7df3a2ac3f8c7935e02551` (MATCH; gitignored) |
| v002 label manifest re-hash | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` (MATCH) |
| v002 label manifest sidecar re-hash | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` (MATCH) |
| Phase 4bm-Q gate report re-hash | `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` (MATCH) |
| Phase 4bm-Q gate report sidecar re-hash | `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` (MATCH) |
| Label parquet / sidecar counts | 90 / 90 |
| `ruff` / `mypy` / `pytest` | deliberately not run (no source / test / script modified; docs-only Tier 1 governance memo) |
| Markdown lint | no project-specific gate exists in this repository; none invented |

---

## 5. Files changed

- `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-t_multi-day-v002-chronological-split-policy-memo.md` (new)
- `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-t_closeout.md` (new — this file)
- `docs/00-meta/current-project-state.md` (modified — narrow Phase 4bm-T "Current phase:" block prepended; prior Phase 4bm-S block preserved as labelled historical context)

No source / test / script / configuration file changed. No `data/microstructure/` file created, modified, or committed. No successor-state JSON created. No manifest mutated. The Phase 4bm-S successor-state artefact was not mutated.

---

## 6. Boundary confirmations

- No source code modified. No test modified. No script modified. No `pyproject.toml` / `README.md` / `.gitignore` / MCP file modified.
- No `data/microstructure/` file created, modified, moved, renamed, deleted, or committed.
- No chronological split successor-state JSON created. No split artefact created on disk.
- No manifest mutated; `chronological_split_policy` remains `"not_yet_defined"` on the v002 label manifest.
- The Phase 4bm-S successor-state JSON + sidecar were not mutated (read-only re-hash MATCH).
- No label gate / feature gate rerun. No label / feature generation. No data acquisition.
- No diagnostics defined or run. No ML defined or trained. No strategy defined or tested. No backtest defined or run.
- No endpoint called; no WebSocket / user-stream; no credential / `.env` / `.mcp.json` / MCP / Graphify.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked).
- No retained verdict revised; no project lock changed; no M0 amendment.
- No successor phase authorized. **Phase 4bm-U is not authorized by Phase 4bm-T.**

---

## 7. Retained verdicts preserved

H0 (FRAMEWORK ANCHOR), R3 (BASELINE-OF-RECORD), R1a / R1b-narrow (RETAINED — NON-LEADING), R2 (FAILED — §11.6), F1 (HARD REJECT), D1-A (MECHANISM PASS / FRAMEWORK FAIL), 5m thread (OPERATIONALLY CLOSED per Phase 3t), V2 (HARD REJECT — terminal), G1 (HARD REJECT — terminal), C1 (HARD REJECT — terminal) — all preserved verbatim.

---

## 8. Project locks preserved

§11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 = 0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k / 4p / 4q / 4v / 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy; Phase 4aw `flip_research_eligible(...)` always-raises invariant (never invoked); Phase 4bb-F canonical sidecar/path policy; Phase 4bl-F risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks; Phase 4bm-A-P1 context management standard; Phase 4bm-D-P1 lightweight Claude Code workspace standard — all preserved verbatim. All prior phase results (Phase 4am .. Phase 4bm-S) preserved verbatim.

---

## 9. Caveats

- The chosen 45 / 30 / 15 windows and the 60-second minimum embargo are recorded at memo level only; they become machine-readable only if a future separately authorized chronological-split-policy successor-state recording phase records them as a sibling artefact (§11 of the memo).
- The split ratio is expressed in UTC dates, not rows; row shares differ slightly because per-day row counts vary. The partition is defined by date boundaries, not row-count targets.
- The boundary-crossing exclusion rule and the 60s embargo are governance constraints on any future row-level research execution; this phase neither runs nor authorizes such execution.
- `ruff` / `mypy` / `pytest` were not run (no source / test / script modified). No markdown-lint gate exists in the repo; none invented.

---

## 10. Recommended state

**Remain paused.** Phase 4bm-T is branch-complete only by this work. **The chronological split policy is defined at memo level only.** **Any chronological split-policy recording requires a separately authorized successor-state phase.** **Phase 4bm-U is not authorized by Phase 4bm-T.** **Recommended state remains paused.**
