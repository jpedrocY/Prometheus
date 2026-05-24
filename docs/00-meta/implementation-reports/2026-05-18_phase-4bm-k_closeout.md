# Phase 4bm-K — Closeout

**Phase identity:** Phase 4bm-K — Multi-Day V002 Feature-Family Research-Use Decision Memo (docs-only).
**Date:** 2026-05-18.
**Phase type:** docs-only research-use decision / governance memo.
**Status:** branch-complete; pending operator review; **NOT** project-complete. Project-completion requires a separately authorized merge phase per `docs/00-meta/process/merge-closeout-standard.md`.

---

## 1. Branch name

`phase-4bm-k/multi-day-v002-feature-family-research-use-decision-memo`

## 2. Base SHA

`89bf2cfb45b7c46f77e23669570e9f380c6a2e91` (Phase 4bm-J merge-closeout SHA-finalization commit; pre-branch `main == origin/main` verified).

## 3. Risk tier

**Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 escalation rules and the v001 Phase 4bi-C v001 feature-family research-use / ML-use decision memo precedent. First-of-kind multi-day v002 feature-family research-use governance decision; touches admissibility for the v002 feature family at policy level; therefore Tier 1 applies (any decision that could affect downstream admissibility escalates to Tier 1 per §3).

## 4. Tracked files added / modified

Added (new tracked files):

- `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-k_multi-day-v002-feature-family-research-use-decision-memo.md` — the main decision memo.
- `docs/00-meta/implementation-reports/2026-05-18_phase-4bm-k_closeout.md` — this closeout.

Modified narrowly:

- `docs/00-meta/current-project-state.md` — narrow Phase 4bm-K narrative paragraph + new "Current phase:" block; prior Phase 4bm-J "Current phase:" block preserved as labelled historical context.

**No** source / test / script / configuration / data / manifest / sidecar / gate-report / successor-state file is modified. **No** `data/microstructure/` artefact is committed. **No** prior memo (other than the narrow `current-project-state.md` update) is modified.

## 5. Decision verdict

**Outcome 1 / Decision form 1 — equivalent to `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`:**

> v002 Feature Stage-5 research-use admissibility is admissible in principle at policy level for the multi-day v002 feature family `microstructure_features_aggtrades_v001 @ v002`, but no manifest mutation occurs in this phase. A separately authorized Phase 4bm-L successor-state recording phase is required before any machine-readable v002 Feature Stage-5 marker exists.

Specifically:

- the v002 feature manifest at `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json` remains `research_eligible = false`, `eligibility_gate_status = "pending"`, and `stage_4_feature_cleared = false` throughout Phase 4bm-K;
- no machine-readable v002 Feature Stage-5 marker exists yet;
- a future Phase 4bm-L would be required to create a sibling successor-state artefact while preserving the v002 feature manifest byte-identically;
- labels, targets, ML, strategy, backtests, diagnostics, and acquisition all remain forbidden / unauthorized;
- v002 Feature Stage-5 admissibility is **not** a strategy hypothesis, predictive claim, edge claim, backtest permission, or M0 bypass;
- Phase 4ak M0 admissibility gate, post-null cooldown rule, cooled-down families list, Phase 4al refined no-rescue rule, Phase 4aw flip-invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model, Phase 4bm-A-P1 thin-prompt context-management standard, and Phase 4bm-D-P1 lightweight Claude Code workspace standard all remain binding.

## 6. Key evidence

| # | Evidence item | Value |
| - | ------------- | ----- |
| 1 | Phase 4bm-J gate verdict | `FEATURE_GATE_PASS` (`overall_status = pass`) |
| 2 | Phase 4bm-J gate report SHA256 | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` |
| 3 | Phase 4bm-J gate sidecar SHA256 | `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125` |
| 4 | Phase 4bm-J check totals | 50 / 50 PASS (0 FAIL / 0 ERROR / 0 NOT_APPLICABLE / 0 blocking failures) |
| 5 | Phase 4bm-I structural QA verdict | `FEATURE_STRUCTURAL_QA_PASS` (confirmed via Phase 4bm-J check A12 PASS) |
| 6 | v002 feature manifest SHA256 | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` |
| 7 | v002 feature manifest sidecar SHA256 | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` |
| 8 | `feature_config_hash` | `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d` |
| 9 | Feature parquet count | 90 |
| 10 | Feature sidecar count | 90 |
| 11 | Total feature row count | 155,153,449 |
| 12 | Feature date range | 2024-12-01 .. 2025-02-28 inclusive (90 contiguous UTC days) |
| 13 | Symbol scope | BTCUSDT (one symbol) |
| 14 | Feature schema column count | 62 (17 lineage / identity / metadata + 45 feature / quality) |
| 15 | v002 derived multi-day index manifest SHA256 | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` (unchanged) |
| 16 | v002 raw manifest SHA256 | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` (unchanged) |
| 17 | Phase 4bm-F v002 derived-family Stage-3 successor-state SHA256 | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` (unchanged) |
| 18 | v001 precedent | Phase 4bi-C — Outcome 1 / Decision form 1 |

## 7. Validation results

Validation commands and results (Phase 4bm-K is docs-only — validation is limited to git hygiene and SHA verification per the brief):

- `git status --short` (pre-commit): docs-only changes; only the two pre-existing untracked entries `.claude/scheduled_tasks.lock` and `data/research/` plus the new memo + closeout + the narrow `current-project-state.md` update.
- `git diff --check` (pre-commit): clean (no whitespace, no conflict markers).
- `git diff --name-only` (pre-commit): exactly 3 docs paths (the new memo, the new closeout, the narrow `current-project-state.md` update).
- SHA256 of Phase 4bm-J gate report (`3c59dfae…`): **MATCHES** recorded value byte-for-byte.
- SHA256 of Phase 4bm-J gate sidecar (`14a17764…`): **MATCHES** recorded value byte-for-byte.
- SHA256 of v002 feature manifest (`512a0a54…`): **MATCHES** recorded value byte-for-byte.
- SHA256 of v002 feature manifest sidecar (`22e2fb77…`): **MATCHES** recorded value byte-for-byte.
- SHA256 of v002 derived multi-day index manifest (`01c5fa53…`): **MATCHES** recorded value byte-for-byte.
- SHA256 of v002 raw manifest (`01696786…`): **MATCHES** recorded value byte-for-byte.
- SHA256 of Phase 4bm-F v002 derived-family Stage-3 successor-state JSON (`72b6edd4…`): **MATCHES** recorded value byte-for-byte.
- Verified on disk in Phase 4bm-K: v002 feature manifest still carries `research_eligible = false`, `eligibility_gate_status = "pending"`, `stage_4_feature_cleared = false`.
- The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved (never invoked).

## 8. Quality gate results / skipped-check rationale

- `git diff --check`: clean.
- Repo-standard markdown lint or check: no project-specific lightweight markdown gate exists; not run.

**Skipped checks (justified):**

- `ruff check`: **skipped.** Phase 4bm-K modifies no Python source, tests, scripts, or configs. Nothing under `src/prometheus/` or `tests/` or `scripts/` is touched. ruff is a code surface tool; there is no relevant code surface to check.
- `mypy src/prometheus`: **skipped.** Same rationale; no source-code touch. The Phase 4bm-H baseline (`mypy src/prometheus`: 29 errors in 5 files) is preserved by construction.
- `pytest` (targeted or whole-repo): **skipped.** Same rationale; no source / test / script touch. The Phase 4bm-J branch quality gates already locked the codebase status into the Phase 4bm-J merge-closeout on `main`:
  - Phase 4bm-J surface `ruff check` (11 paths): PASS.
  - Whole-repo `ruff check .`: PASS.
  - `pytest tests/research/microstructure/test_multiday_feature_gate*.py`: 53 PASS in 7.86 s.
  - Whole-repo `pytest`: 15 collection errors from missing `httpx` / `duckdb` env modules + 2 pre-existing `test_engine_d1a_dispatch.py` subprocess failures (both env baseline). This baseline is unchanged by Phase 4bm-K because Phase 4bm-K modifies no existing source / test / script.

These skips conform to the project's standing precedent for Tier 1 docs-only governance / research-use decision memos (Phase 4bi-C v001 precedent; Phase 4bg-A v001 derived-family precedent; Phase 4bm-E v002 derived-family precedent).

## 9. Non-authorization boundaries

Phase 4bm-K honors reusable non-authorization blocks **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-SUCCESSOR-STATE**, **N-DERIVATION**, **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK** per `docs/00-meta/process/phase-risk-tiering-standard.md` §7.

Phase 4bm-K does **not**, and **cannot**, authorize:

- Phase 4bm-L (Multi-Day V002 Feature-Family Research-Use Successor-State Recording; the conditional successor; v002 analogue of Phase 4bi-D);
- v002 feature-family successor-state recording (any form);
- multi-day v002 label-family phases (analogues of Phase 4bj-A through Phase 4bj-K);
- multi-day v002 chronological-split-policy memo;
- diagnostics;
- ML training, model selection, feature ranking, meta-labeling;
- strategy specification, implementation, signal construction;
- backtest specification, plan, or execution;
- additional acquisition;
- Phase 5;
- paper / shadow;
- live-readiness;
- deployment;
- exchange-write;
- production-key creation;
- authenticated APIs;
- private endpoints;
- user-stream / live WebSocket implementation;
- public-endpoint calls in code;
- MCP / Graphify / `.mcp.json` / credentials;
- any modification of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` / `stage_4_feature_cleared` on any actual on-disk manifest;
- any committed `data/microstructure/` artefact;
- amending Phase 4ak M0, Phase 4al refined no-rescue rule, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model, Phase 4bm-A-P1, Phase 4bm-D-P1, Phase 4bm-E, Phase 4bm-F, Phase 4bm-G, Phase 4bm-H, Phase 4bm-I, or Phase 4bm-J;
- any successor phase whatsoever.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved (never invoked).

## 10. Recommended state

**Remain paused.**

Phase 4bm-K is branch-complete only by this work. Per the Phase 4bk-A workflow standard, Phase 4bm-K is **NOT** project-complete until a separately authorized merge phase records its merge-closeout on `main` per the full Tier 1 16-section structure. The operator's broader pause decision continues to apply.

## 11. Explicit non-authorization statement

**Phase 4bm-L / successor-state recording / labels / diagnostics / ML / strategy / backtests / additional acquisition / paper-shadow / live-readiness / deployment / exchange-write / production-key creation / authenticated APIs / private endpoints / user-stream / live WebSocket implementation / public-endpoint calls in code / MCP / Graphify / `.mcp.json` / credentials / any modification of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` / `stage_4_feature_cleared` on any actual on-disk manifest / any committed `data/microstructure/` artefact / any successor phase whatsoever — all remain unauthorized after Phase 4bm-K.**

## 12. Required affirmative-decision phrases (verbatim)

- **Feature-family research-use is approved in principle at policy level only.**
- **No machine-readable research-use marker exists after Phase 4bm-K.**
- **Phase 4bm-L is not authorized by Phase 4bm-K.**
- **Successor-state recording is not authorized by Phase 4bm-K.**
- **Labels / diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-K.**
- **No feature artefact was modified.**
- **No upstream artefact was mutated.**
- **No data/microstructure file was committed.**
