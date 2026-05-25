# Phase 4bm-Q — Merge-Closeout

**Phase identity:** Phase 4bm-Q — Multi-Day V002 Label-Family Eligibility Gate Design / Implementation / Execution.
**Tier:** Tier 1 — Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` §3.
**Date:** 2026-05-25.
**Status:** **merge-complete on `main`**.

---

## 1. Required exact phrases

- **Phase 4bm-Q is now merge-complete on main.**
- **LABEL_GATE_PASS remains report-level only.**
- **Label-family research-use is not authorized by the Phase 4bm-Q merge.**
- **Label-family successor-state recording is not authorized by the Phase 4bm-Q merge.**
- **Chronological split policy is not authorized by the Phase 4bm-Q merge.**
- **Diagnostics / ML / strategy / backtests are not authorized by the Phase 4bm-Q merge.**
- **No data/microstructure file is committed by the Phase 4bm-Q merge.**
- **No manifest transition is authorized by the Phase 4bm-Q merge.**
- **No successor-state JSON creation is authorized by the Phase 4bm-Q merge.**
- **Phase 4bm-R is not authorized by the Phase 4bm-Q merge.**
- **Recommended state remains paused.**

## 2. Source branch

`phase-4bm-q/multi-day-v002-label-family-eligibility-gate`

## 3. Base SHA

`3f87123175e07a1cc373b15f3fc29d487fae3265` (Phase 4bm-P merge-closeout SHA-finalization on `main`; pre-branch `main == origin/main`).

## 4. Branch tip SHA before merge

`02042b3` — `style(phase-4bm-q): drop unnecessary forward-ref quotes on Callable annotation` (a one-line ruff UP037 auto-fix landed on the branch just before merge; no behavioural change; the fix removes unnecessary string quotes from the `Callable[[], MultidayLabelGateCheckResult]` annotation inside `multiday_label_gate_checks.py::run_all_checks._safe`, which `from __future__ import annotations` already defers).

Earlier branch commits preserved by the merge:

- `848dbbb` — `docs(phase-4bm-q): implementation report + closeout + project-state` (the implementation report, closeout, and narrow `current-project-state.md` update).
- `8b9c5c5` — `feat(phase-4bm-q): multi-day v002 label-family eligibility gate` (4 new source modules + 5 new test files + 1 new orchestrator script + narrow `__init__.py` re-export + narrow `test_import_boundaries.py` word-boundary fix).

## 5. Merge commit SHA

`e2817f6a0c768e5fb19a4cd76c557ee2e0d5583a` — `docs(phase-4bm-q): merge label-family eligibility gate`. Merge strategy: `--no-ff` (true merge commit; preserves the branch in the history).

## 6. Final main SHA at merge time

Merge commit SHA: `e2817f6a0c768e5fb19a4cd76c557ee2e0d5583a`. Merge-closeout commit SHA on `main` (next commit after the merge): `2ba8323d1ae29bc71e5ec6dd0cf18329e3dfbfe3` — `docs(phase-4bm-q): add merge closeout`. SHA-finalization commit (this edit) immediately follows the merge-closeout commit. See §23 for finalized SHAs.

## 7. Validation commands and results

Run from `C:\Prometheus` with the project venv (`.venv\Scripts\python.exe`):

| Command | Result |
|---|---|
| `git status --short` (pre-merge, on phase branch) | only `data/research/` untracked (expected) |
| `git rev-parse main` (pre-merge) | `3f87123175e07a1cc373b15f3fc29d487fae3265` |
| `git rev-parse origin/main` (pre-merge) | `3f87123175e07a1cc373b15f3fc29d487fae3265` (in sync) |
| `git rev-parse phase-4bm-q/...` (pre-merge) | `02042b3...` (branch tip) |
| `git log --oneline -12 --decorate --graph --all` | shows Phase 4bm-P merge-closeout finalized; Phase 4bm-Q commits ahead of main; no unexpected merges |
| `git diff --stat main..phase-4bm-q/...` | 15 files changed, 3934 insertions(+), 1 deletion(-) — matches the closeout file inventory exactly |
| `git diff --name-status main..phase-4bm-q/...` | 12 `A` + 3 `M` — matches expected (see §8) |
| `git diff --check main..phase-4bm-q/...` | clean (exit 0; no whitespace / conflict markers) |
| `pytest tests/research/microstructure/` (full sweep, run from repo root) | **all passing**; no new regression |
| `pytest tests/research/microstructure/test_multiday_label_gate*.py` (post-autofix) | **38 / 38 passed** |
| `ruff check src/prometheus/research/microstructure scripts/phase4bm_q_run_multiday_label_gate.py tests/research/microstructure` (post-autofix) | **All checks passed!** |
| `mypy src/prometheus/research/microstructure/multiday_label_gate*.py` | **Success: no issues found in 4 source files** |
| `git check-ignore -v <gate-report>` | `.gitignore:85: data/microstructure/` (gitignored) |
| `git check-ignore -v <gate-report-sidecar>` | `.gitignore:85: data/microstructure/` (gitignored) |
| `Get-FileHash <gate-report>` | SHA256 `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` (matches expected) |
| `Get-FileHash <sidecar>` | SHA256 `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` (matches expected) |
| `git merge --no-ff phase-4bm-q/... -m "..."` | merged successfully via `ort` strategy; merge commit `e2817f6...` |
| `git status --short` (post-merge, on main) | only `data/research/` untracked (no `data/microstructure/` entry) |

`mypy src/prometheus` (whole package) and whole-repo `pytest` were not invoked at the merge level. Documented baselines unchanged on `main`: 29 mypy errors in 5 files; 15 pytest collection errors from missing `httpx`/`duckdb`; 2 pre-existing subprocess failures in `tests/unit/research/backtest/test_engine_d1a_dispatch.py` — all unrelated to label / feature surfaces and confirmed not introduced by Phase 4bm-Q.

## 8. File inventory / changed files

Total: **15 files changed, 3934 insertions(+), 1 deletion(-)**.

### Added (12)

- `src/prometheus/research/microstructure/multiday_label_gate_io.py`
- `src/prometheus/research/microstructure/multiday_label_gate_checks.py`
- `src/prometheus/research/microstructure/multiday_label_gate_report.py`
- `src/prometheus/research/microstructure/multiday_label_gate.py`
- `scripts/phase4bm_q_run_multiday_label_gate.py`
- `tests/research/microstructure/test_multiday_label_gate_io.py`
- `tests/research/microstructure/test_multiday_label_gate_checks.py`
- `tests/research/microstructure/test_multiday_label_gate_report.py`
- `tests/research/microstructure/test_multiday_label_gate.py`
- `tests/research/microstructure/test_multiday_label_gate_no_network.py`
- `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-q_multi-day-v002-label-family-eligibility-gate.md`
- `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-q_closeout.md`

### Modified narrowly (3)

- `src/prometheus/research/microstructure/__init__.py` — re-export the new Phase 4bm-Q public-API names.
- `tests/research/microstructure/test_import_boundaries.py` — word-boundary fix for the `.env` denylist substring so it no longer collides with the Phase 4bm-N `envelope_terminal_unix_ms` schema field accessed via `self.envelope_terminal_unix_ms` inside the new `MultidayLabelGateReport.to_dict()` body. The original intent (catch `.env`, `.env.local`, `.env "` file references) is preserved by the new word-boundary regex `\.env(?![A-Za-z0-9_])`.
- `docs/00-meta/current-project-state.md` — new Phase 4bm-Q narrative paragraph + new "Current phase:" block; prior Phase 4bm-P paragraph + block preserved verbatim as labelled historical context.

No `data/microstructure/` artefact appears in the merge diff. `.gitignore`, `.gitattributes`, `pyproject.toml`, `README.md`, `.mcp.json` (absent), and every other tracked file outside the 15 above remain unchanged.

## 9. Gate report path and SHA256

| Output | Path | SHA256 | Bytes |
|---|---|---|---|
| Gate report JSON | `data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-q__1779708036319__3f87123175e0.json` | `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` | 20,259 |
| Gate report sidecar | `<report>.sha256` | `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` | 156 |

## 10. Confirmation gate report and sidecar are gitignored and not committed

Both files are covered by `.gitignore:85: data/microstructure/`:

```text
$ git check-ignore -v data/microstructure/gate-reports/labels/...phase-4bm-q...json
.gitignore:85:data/microstructure/	data/microstructure/gate-reports/labels/...phase-4bm-q...json

$ git check-ignore -v data/microstructure/gate-reports/labels/...phase-4bm-q...json.sha256
.gitignore:85:data/microstructure/	data/microstructure/gate-reports/labels/...phase-4bm-q...json.sha256
```

`git status --short` post-merge shows only the expected pre-existing untracked entry (`data/research/`); **no `data/microstructure/` entry appears**. The merge diff contains zero `data/microstructure/` paths.

## 11. Confirmation no `data/microstructure` artefact was committed

Confirmed. `git diff --name-status main~1..main` lists exactly 15 paths (12 `A` + 3 `M`), none of which is under `data/microstructure/`. The only writes inside `data/microstructure/` performed by Phase 4bm-Q are the gate report JSON + paired Phase 4bb-F sidecar under `data/microstructure/gate-reports/labels/`, both gitignored under `.gitignore:85` and present only in the local working tree.

## 12. Confirmation no upstream artefact or manifest was mutated

Confirmed. The Phase 4bm-Q gate is read-only with respect to every upstream artefact. Pre/post upstream immutability re-hash over **290 immutability witnesses** (20 governance lineage artefacts + 90 label parquets + 90 label sidecars + transitive 90 feature parquets via `source_feature_parquet_sha256` lineage) was byte-identical at gate-execution time and remains byte-identical post-merge:

- v002 label manifest: SHA `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` unchanged.
- v002 label manifest sidecar: SHA `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` unchanged.
- v002 feature manifest: SHA `512a0a54…` unchanged; still `research_eligible=false / eligibility_gate_status='pending' / stage_4_feature_cleared=false`.
- v002 derived/normalized manifest: SHA `01c5fa53…` unchanged; still `research_eligible=false / eligibility_gate_status='pending'`.
- v002 raw manifest: SHA `01696786…` unchanged; still `research_eligible=false / eligibility_gate_status='pending'`.
- Phase 4bm-J gate report `3c59dfae…` + sidecar `14a17764…` unchanged.
- Phase 4bm-L successor-state `7eccaa8f…` + sidecar `c2b73330…` unchanged.
- Phase 4bm-D gate report `3b45e70b…` + sidecar `8e74261c…` unchanged.
- Phase 4bm-F successor-state `72b6edd4…` + sidecar `1e9ffb23…` unchanged.
- Phase 4bl-D-R raw gate report `f9493fd1…` unchanged.
- Phase 4bl-E raw successor-state `a0576ca6…` unchanged.
- v002 acquisition log `52f6d7fb…` unchanged.

v002 label manifest still carries `research_eligible=false`, `eligibility_gate_status='pending'`, `stage_5_label_cleared=false`, `label_family_research_use_authorized=false`, `label_family_eligibility_gate_authorized=false`, `chronological_split_policy='not_yet_defined'`. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end and was **never invoked** by Phase 4bm-Q or its merge.

## 13. Confirmation `LABEL_GATE_PASS` is report-level only

Confirmed. The Phase 4bm-Q gate report records `gate_verdict = "LABEL_GATE_PASS"`, but the report data-model's hard invariants enforce:

- `research_eligible_after = False`
- `eligibility_gate_status_after = "pending"`
- `stage_5_label_cleared_after = False`
- `label_family_research_use_authorized_after = False`
- `chronological_split_policy_after = "not_yet_defined"`
- `label_family_eligibility_gate_authorized_after = False`
- `successor_state_authorized = False`
- All authorization flags (`diagnostics_authorized`, `ml_authorized`, `strategy_authorized`, `backtest_authorized`, `acquisition_authorized`) are `False`.

These build-time invariants in `MultidayLabelGateReport.__post_init__` raise `MultidayLabelGateReportError` if violated, mechanically preventing the verdict from escalating into actual research-use authorization. **LABEL_GATE_PASS remains report-level only.**

## 14. Confirmation label-family research-use remains unauthorized

Confirmed. **Label-family research-use is not authorized by the Phase 4bm-Q merge.** v002 label manifest `label_family_research_use_authorized=false` unchanged; no research-use decision memo created; no successor-state recording created.

## 15. Confirmation successor-state recording remains unauthorized

Confirmed. **Label-family successor-state recording is not authorized by the Phase 4bm-Q merge.** No successor-state JSON was created under `data/microstructure/successor-state/` by Phase 4bm-Q or its merge.

## 16. Confirmation chronological split policy remains unauthorized

Confirmed. **Chronological split policy is not authorized by the Phase 4bm-Q merge.** v002 label manifest `chronological_split_policy='not_yet_defined'` unchanged.

## 17. Confirmation diagnostics / ML / strategy / backtests remain unauthorized

Confirmed. **Diagnostics / ML / strategy / backtests are not authorized by the Phase 4bm-Q merge.** v002 label manifest authorization flags `diagnostics_authorized=false`, `ml_authorized=false`, `strategy_authorized=false`, `backtest_authorized=false`, `acquisition_authorized=false`, `successor_authorization_after=false` all unchanged.

## 18. Confirmation Phase 4bm-R and all successors remain unauthorized

Confirmed. **Phase 4bm-R is not authorized by the Phase 4bm-Q merge.** No successor phase is authorized — including multi-day v002 label-family research-use decision memo, multi-day v002 label-family research-use successor-state recording, multi-day v002 chronological-split-policy memo, multi-day v002 chronological-split-policy successor-state recording, Phase 4bn-* / 4bo-* / 4bp-* / 4bq-* / Phase 5 / Phase 4 canonical / paper / shadow / live-readiness / deployment / exchange-write / production keys / authenticated APIs / private endpoints / user-stream / WebSocket implementation / MCP / Graphify / `.mcp.json` / credentials / additional acquisition.

Reusable non-authorization blocks honored: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST** (every upstream / sibling manifest remains byte-identical; the only file written by Phase 4bm-Q is the gate report + sidecar, both gitignored), **N-GATE-RERUN** (no prior gate rerun; this is a new gate-report family), **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**, **N-SUCCESSOR-STATE** (no successor-state artefact created). **N-DERIVATION** does not apply — Phase 4bm-Q is the explicitly authorized label-family eligibility gate phase.

## 19. Retained verdicts preserved

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

## 20. Project locks preserved

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 4ak M0 twelve-clause gate
- Phase 4al refined no-rescue rule
- Phase 4aw `flip_research_eligible` always-raises invariant (never invoked by Phase 4bm-Q or its merge)
- Phase 4bb-F canonical sidecar/path policy
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks
- Phase 4bm-A-P1 context management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace standard
- All other locks recorded in `current-project-state.md` and the latest merge-closeout

## 21. Known caveats

- **Branch-time ruff autofix.** A ruff UP037 finding (an unnecessary string quoting on a forward-reference `Callable` annotation in `multiday_label_gate_checks.py::_safe`) was discovered during the merge-time re-validation. The fix was a one-line, behavioural-no-op autofix (removing the quotes; `from __future__ import annotations` defers all annotations anyway). It was committed on the phase branch as `02042b3 style(phase-4bm-q): drop unnecessary forward-ref quotes on Callable annotation` before the merge, so the merge reflects a clean `ruff check` over the Phase 4bm-Q surface.
- **`test_import_boundaries.py` narrow change.** The Phase 4bm-N v002 label schema field `envelope_terminal_unix_ms` is exposed on the new `MultidayLabelGateReport` dataclass via `self.envelope_terminal_unix_ms` inside `to_dict()`, which trips a pre-existing bare-substring `.env` denylist scan. The narrow fix replaces the bare substring with a word-boundary regex (`\.env(?![A-Za-z0-9_])`), preserving the original intent (catch `.env` file references) while accommodating legitimate `envelope_*` identifiers introduced by the locked v002 schema. Documented in the implementation report §11 and the closeout §4.
- **Targeted (not whole-package) `mypy` and whole-repo `pytest`.** `mypy src/prometheus` (whole package) and whole-repo `pytest` were not invoked at Phase 4bm-Q or merge level per the documented project baseline (29 mypy errors in 5 files; 15 pytest collection errors from missing `httpx`/`duckdb`; 2 pre-existing subprocess failures in `tests/unit/research/backtest/test_engine_d1a_dispatch.py`). All baselines unchanged on `main`; Phase 4bm-Q introduces zero new mypy errors on the 4 new modules and zero new pytest failures.
- **`code_commit_sha` in the gate report.** Set to `3f87123175e0…` (the base SHA, operator-supplied as `code_commit_sha`). The actual implementation commits on the phase branch are `8b9c5c5`, `848dbbb`, and `02042b3`. The gate is reproducible against the local artefacts at any of these SHAs (the gate is read-only with respect to data and the source modules are byte-identical at any branch SHA after `02042b3`).

## 22. Recommended state

**Remain paused.** **Recommended state remains paused.**

Phase 4bm-Q is now merge-complete on `main`. No successor phase is authorized. The operator may, separately and explicitly, authorize a future multi-day v002 label-family research-use decision memo (multi-day analogue of Phase 4bj-F) — but that is a docs-only decision phase, **not** an authorization for any data work, and it is **not** authorized by this merge-closeout. Phase 4bm-R, label-family research-use, label-family successor-state recording, chronological-split-policy, diagnostics, ML, strategy, backtests, acquisition, manifest mutation, successor-state JSON creation, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user streams, WebSockets, MCP, Graphify, `.mcp.json`, and credentials all remain unauthorized.

## 23. Finalized SHAs

| Item | SHA |
|---|---|
| Phase 4bm-Q merge commit | `e2817f6a0c768e5fb19a4cd76c557ee2e0d5583a` |
| Phase 4bm-Q merge-closeout commit (this memo, initial commit on `main`) | `2ba8323d1ae29bc71e5ec6dd0cf18329e3dfbfe3` |
| Phase 4bm-Q SHA-finalization commit (the follow-on commit that finalizes this section) | recorded in the corresponding operator report and in `git log` immediately after this memo was added; per the prior-phase repo convention (Phase 4bm-P / Phase 4bm-O / Phase 4bm-N merge-closeout SHA-finalization), the SHA-finalization commit's own SHA is **not** self-referenced inside this memo (cannot be known at edit time without amending the commit it is supposed to record), and is captured only in the operator report and in `git log` |
| Final `main` SHA after SHA-finalization push | recorded in the operator report; equal to the SHA-finalization commit SHA above |
| Final `origin/main` SHA after push | recorded in the operator report; equal to the final `main` SHA |
| `main == origin/main` after push | **yes** |

**LABEL_GATE_PASS remains report-level only.** **Label-family research-use is not authorized by the Phase 4bm-Q merge.** **Label-family successor-state recording is not authorized by the Phase 4bm-Q merge.** **Chronological split policy is not authorized by the Phase 4bm-Q merge.** **Diagnostics / ML / strategy / backtests are not authorized by the Phase 4bm-Q merge.** **No data/microstructure file is committed by the Phase 4bm-Q merge.** **No manifest transition is authorized by the Phase 4bm-Q merge.** **No successor-state JSON creation is authorized by the Phase 4bm-Q merge.** **Phase 4bm-R is not authorized by the Phase 4bm-Q merge.** **Recommended state remains paused.**