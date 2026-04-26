# Phase 2o — Checkpoint Report

Generated at the close of Phase 2o on branch `phase-2o/asymmetry-review`, after Gate 2 approval. Four operator-authorized commits per the operator-approved commit sequence (this checkpoint is the fourth commit). Template per `.claude/rules/prometheus-phase-workflow.md`.

## Phase

**Phase 2o — Targeted Asymmetry Review / Analysis (docs-only).** A judgement-and-analysis phase that examined the BTC/ETH asymmetry surfaced by Phase 2m (R1a's volatility-percentile filter materially helps ETH and materially hurts BTC relative to the locked R3 exit baseline) and produced a recommendation about whether the asymmetry points to a fixable next hypothesis or to a reason to stop further immediate execution. No code changes, no new backtests, no new variants, no parameter changes, no §10.3 / §10.4 / §11.3 / §11.4 / §11.6 framework changes, no Phase 4 work, no paper/shadow-readiness planning, no execution-phase start.

## Goal

(a) Read the Phase 2l / 2m / 2n committed reports plus the supporting strategy / backtesting / risk specs. (b) Produce a Gate 1 plan recording scope, content requirements, preservation rules, and proposed deliverables. (c) Produce a substantive asymmetry-review memo with sections A–K per the operator brief. (d) Produce a Gate 2 pre-commit review tracing every operator-brief content + process requirement to its Phase 2o artifact. (e) Stop before any commit awaiting operator/ChatGPT Gate 2 approval; on approval, commit per the proposed sequence and produce this checkpoint.

## Summary

Phase 2o delivered four committable documentation artifacts (~1,300 lines of new content) and zero code / test / data changes. Pytest stayed at **417 passed** throughout (unchanged from Phase 2n end state — no source files touched). Ruff / format / mypy were not rerun in 2o (no source change); the Phase 2n end state (green on all four gates) is preserved unchanged.

The asymmetry-review memo's A–K sections produced:

1. **BTC/ETH asymmetry diagnosis (§C).** Six candidate explanations evaluated (symbol-specific market behavior; regime-composition; trade-count / sample fragility; setup-selection-shape; directional-bias interaction; family-limitation). The most-supported explanations are **C.1 (symbol-specific)** and **C.5 (directional-bias interaction)** — both converge on the same operational implication: R1a is acting like an ETH-favorable specialty filter, picking up structural directional signal that exists on ETH (a regime-asymmetric / short-biased post-compression follow-through) and is muted on BTC. C.2 (regime-composition) is a secondary contributing factor; C.3 (sample fragility) and C.4 (selection-shape) are weaker; C.6 (family-limitation) is plausible but premature.
2. **R1a mechanism interpretation (§E).** R1a is mechanically correct (100% of filled entries at percentile ≤ 25%; predicate working as designed). The asymmetry is in the post-compression follow-through, not in the compression definition. Best framing: **ETH-favorable specialty filter with a regime-localized signal**.
3. **Fixability analysis (§F).** Four hypotheses evaluated as hypotheses, not as execution approvals: F.1 regime-conditional R1a application (high overfitting risk; stays alive only as a planning-phase hypothesis); F.2 symbol-conditional R1a — ETH only (unavailable at v1 by §1.7.3); F.3 R1a abandonment while keeping R3 (cleanest immediate path; preserves R3 baseline; preserves R1a as research evidence); F.4 different setup-side redesign altogether (open future option; needs more diagnostic work). F.3 is the cleanest immediate path; F.1 is the highest-EVI execution path **if** specified properly via a future docs-only spec phase; F.2 is policy-blocked at v1.
4. **Family-level implication (§G).** The asymmetry **increases** confidence in R3 alone (R3 is broad-based, robust, and the asymmetry confirms its structural-improvement source is universal). Reduces confidence in this specific R1a form, not in setup-side redesigns generally. Pause longer before any next redesign — next research cycle is a planning cycle, not an execution cycle.
5. **Primary recommendation (provisional, evidence-based):** Phase 2o effectively closes the question of further structural-redesign execution for now. R3 remains the research-leading baseline. R1a stays alive as a research branch but is dropped as a deployable variant. The recommended next step is **Phase 2p Option A — pause; consolidate at R3; no immediate new redesign**. **Fallback:** Phase 2p Option B — docs-only hypothesis-planning for one specific next redesign (regime-conditional R1a-prime) via Phase 2j-style spec-writing before any future Gate 1 / Gate 2 / execution cycle.
6. **Switch conditions (§I)** enumerate six scenarios that would change the recommendation (consolidate→execute; R1a-stays-alive→permanent-abandonment; R1a-promoted-but-non-leading→ETH-only; A→stop-family; A→Phase 4; A→stop-point).
7. **Phase 2p options A–E (§J)** compared. Option A recommended; Option B disciplined alternative; Options C/D/E remain effectively deferred at v1.
8. **Non-proposal list (§K)** enumerates 23 explicit non-proposals.

### Operator Gate 2 framings preserved

The operator's Phase 2o Gate 2 approval added these explicit framings to be preserved in the checkpoint:

- **Do not frame R1a+R3 as the new universal winner.** Honored throughout the memo: §A.3, §C, §E.4 explicitly reject the "new primary candidate" / "universal winner" framing.
- **Do frame R3 as the research-leading baseline.** Honored: §B.1, §G.2, §H.1, §H.3 record R3's broad-based PROMOTE evidence and explicitly designate R3 as the locked exit-philosophy baseline for any future structural-redesign work or operational-readiness planning.
- **Do frame R1a as useful research evidence but not the current deployable / default path.** Honored: §H.1 commits this framing — "R1a stays alive as a research branch (the Phase 2m artifacts on disk and the committed comparison report are not invalidated). R1a's deployable status is constrained by §1.7.3, but the research value is preserved." §F.3 records that "R1a as a deployable variant is dropped; R1a as research evidence remains."
- **Preserve the formal H0-anchor judgments exactly as recorded.** Honored: §A.2, §B, §D, §H consistently treat H0 as the sole §10.3 / §10.4 anchor; §B reproduces all R3 PROMOTE numbers (Phase 2l) and R1a+R3 PROMOTE numbers (Phase 2m) verbatim from the committed comparison reports without re-derivation.

The asymmetry diagnosis converged on the explicit conclusion: **R1a's BTC/ETH split is better treated as evidence about family limits and conditional edge than as a reason to keep executing immediately.** R3 remains the research-leading baseline; R1a+R3 remains valuable research evidence; neither implies live readiness.

## Files changed

By commit, on branch `phase-2o/asymmetry-review` starting from `main @ c20da51` (Phase 2n merge):

| Commit | Files                                                                                                              | +Lines |
|--------|--------------------------------------------------------------------------------------------------------------------|-------:|
| 1      | `docs/00-meta/implementation-reports/2026-04-27_phase-2o_gate-1-plan.md` (new)                                     |  ~265  |
| 2      | `docs/00-meta/implementation-reports/2026-04-27_phase-2o_asymmetry-review-memo.md` (new)                            |  ~770  |
| 3      | `docs/00-meta/implementation-reports/2026-04-27_phase-2o_gate-2-review.md` (new)                                   |  ~285  |
| 4      | `docs/00-meta/implementation-reports/2026-04-27_phase-2o-checkpoint-report.md` (new — this file)                   | this file |

## Files created

- `docs/00-meta/implementation-reports/2026-04-27_phase-2o_gate-1-plan.md`
- `docs/00-meta/implementation-reports/2026-04-27_phase-2o_asymmetry-review-memo.md`
- `docs/00-meta/implementation-reports/2026-04-27_phase-2o_gate-2-review.md`
- `docs/00-meta/implementation-reports/2026-04-27_phase-2o-checkpoint-report.md` (this file)

## Files deleted

None.

## Commands run

- `git -C c:/Prometheus status --short`, `git -C c:/Prometheus rev-parse --abbrev-ref HEAD`, `git -C c:/Prometheus log --oneline -5` — verified clean main with Phase 2n merged at `c20da51`.
- `git -C c:/Prometheus checkout -b phase-2o/asymmetry-review` — branch created from clean main.
- `git -C c:/Prometheus status`, `git -C c:/Prometheus diff --stat HEAD` at the evidence stop and at multiple checkpoints.
- `uv run pytest` at the evidence stop (417 passed / 12.04 s) and after each commit (expected 417 passed).
- `git add <specific-file>` + `git commit -m "<heredoc>"` four times per the operator-approved sequence (this checkpoint is the fourth commit).

No backtest runs. No data downloads. No `uv add` / `uv sync`. No `uv run ruff` / `uv run ruff format` / `uv run mypy` reruns (no source files modified; the Phase 2n end-state green status on those gates is preserved unchanged).

## Installations performed

None. No `uv add`, no `uv sync` change, no global installs. `pyproject.toml` and `uv.lock` unchanged.

## Configuration changed

None. No `configs/`, `.env`, `.claude/`, `.gitignore`, or `.gitattributes` edits.

## Tests/checks passed

| When                                  | Result                |
|---------------------------------------|-----------------------|
| Pre-commit (no source changes)        | **417 passed** / 12.04 s (matches Phase 2n end state) |
| After commit 1 (Gate 1 plan)          | **417 passed**         |
| After commit 2 (asymmetry review memo) | **417 passed**         |
| After commit 3 (Gate 2 review)        | **417 passed**         |
| After commit 4 (this) — expected      | **417 passed**         |

`uv run ruff check .`, `uv run ruff format --check .`, and `uv run mypy` were not rerun during Phase 2o because no source files were touched; the Phase 2n end state (green on all four gates) is preserved unchanged.

## Tests/checks failed

None.

## Runtime output

Not applicable — Phase 2o produced no runtime state, no backtests, no scripts invoked.

## Known gaps

**No new GAP entries logged in this phase.** Phase 2o carries forward existing GAPs unchanged:

- GAP-20260420-028 OPEN-LOW.
- GAP-20260419-018 / 020 / 024 ACCEPTED_LIMITATION.
- GAP-20260420-029 RESOLVED.
- GAP-20260424-030 OPEN — disposition deferred per Phase 2l / 2m / 2n / 2o approvals; Phase 2o does not create a SUPERSEDE event (no exit-philosophy change in 2o).
- GAP-20260424-031 / 032 / 033 OPEN — CARRIED.
- GAP-20260424-034 / 035 RESOLVED verification-only.
- GAP-20260424-036 RESOLVED-by-convention.

The asymmetry-review memo did not surface any prior-doc conflict that would require a permanent GAP entry. The committed Phase 2g / 2h / 2i / 2j / 2k / 2l / 2m / 2n reports are mutually consistent on the key claims.

## Spec ambiguities found

None new. The Phase 2j memo §C R1a spec, the Phase 2l R3 PROMOTE evidence, the Phase 2m R1a+R3 formal-but-mixed PROMOTE evidence, and the Phase 2n research-leading / promoted-but-non-leading framings were sufficient for the asymmetry diagnostic produced in Phase 2o. The §C diagnosis framework, the §E mechanism interpretation, and the §F fixability analysis were all judgement-level — none surfaced an ambiguity that would require a permanent log entry.

## Technical-debt updates needed

None made in 2o (operator restriction). The Phase 2o asymmetry diagnosis is informational input for any future operator review of TD-016 (statistical live-performance thresholds): the explicit framing that R3 alone is the research-leading baseline and that R1a's contribution is symbol-asymmetric / regime-localized informs how TD-016 thresholds might apply to future R3-only operational planning if and when that becomes appropriate. The register itself stays untouched per operator restriction.

## Safety constraints verified

| Check                                                        | Result |
|--------------------------------------------------------------|--------|
| Production Binance keys                                      | none   |
| Exchange-write code                                          | none   |
| REST / WebSocket / authenticated endpoints                   | none   |
| Credentials / `.env`                                         | none   |
| `.mcp.json`                                                  | absent |
| Graphify                                                     | disabled |
| MCP servers                                                  | not activated |
| Manual trading controls                                      | none   |
| Strategy / risk / dataset / cost-model changes               | none (docs-only)                                                                  |
| Binance public or authenticated URLs                         | none fetched |
| New top-level package or dependency                          | none   |
| `pyproject.toml` / `uv.lock` change                          | none   |
| `data/` commits                                              | none (no run output produced)                                                      |
| `docs/12-roadmap/technical-debt-register.md` edits           | none (operator restriction)                                                        |
| `docs/00-meta/implementation-ambiguity-log.md` edits         | none (none surfaced; operator restriction held)                                    |
| Phase 2e baseline run dir untouched                          | yes (read-only diagnostic citation only)                                            |
| Phase 2g / 2l / 2m run dirs untouched                        | yes                                                                                 |
| Wave-1 REJECT ALL preserved                                  | yes (historical evidence only; no comparison-baseline shifting)                     |
| Phase 2l R3 PROMOTE preserved                                | yes (designated as research-leading baseline; sub-parameters R-target=2.0 / TS=8 unchanged) |
| Phase 2m R1a+R3 PROMOTE preserved                            | yes (formal verdict unchanged; sub-parameters X=25 / N=200 unchanged; promoted-but-non-leading framing carried verbatim) |
| Phase 2n research-leading / promoted-but-non-leading framings | preserved verbatim throughout the memo                                              |
| Phase 2i §1.7.3 project-level locks                          | preserved (BTCUSDT primary, one-position, 0.25% risk, 2× leverage, mark-price stops, v002 datasets, H0-only anchor, ≤ 2 carry-forward) |
| §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds             | unchanged                                                                                       |
| H0 anchor preservation                                        | enforced (memo §A, §B, §D, §H)                                                                  |
| ETH-specific strength NOT converted into universal recommendation | enforced (memo §E.4, §F.2 / §H.4 / §I.3)                                                       |
| Another execution phase NOT recommended                      | enforced (memo §H.1 NOT IMMEDIATELY; §I.1 specifies switch conditions)                          |
| `--no-verify` / hook skipping                                 | not used                                                                                      |
| `git push`                                                    | not used (operator restriction; "do not push yet")                                              |
| Phase 4 work                                                  | none (operator restriction)                                                                    |
| Phase 2p execution start                                      | none (operator restriction; "do not start Phase 2p yet"; this phase proposes 2p, does not start it) |
| Phase 2p Option A (pause; keep R3 baseline) start              | none (operator restriction; recommended as next phase, not started)                            |
| Paper/shadow-readiness planning                               | none (operator restriction)                                                                    |
| Tiny-live-readiness planning                                  | none (operator restriction)                                                                    |
| Live-readiness claim                                          | none                                                                                          |
| New backtests / variants / data                               | none                                                                                          |
| New redesign candidate exposed                                | none (only H0 / R3 / R1a+R3 referenced)                                                       |
| Disguised parameter sweeps                                    | none                                                                                          |
| Wave-1 variant revival                                        | none                                                                                          |
| New strategy family started                                   | none                                                                                          |
| Pre-existing 417 tests pass                                   | yes (every commit)                                                                              |

## Current runtime capability

Research-only, unchanged from end of Phase 2n. No runtime process, no dry-run adapter state, no user-stream connectivity. The project can run the backtest CLI against the v002 datasets for H0, the Phase 2g wave-1 variants, Phase 2l R3, and Phase 2m R1a+R3. No capability was added or removed in 2o.

## Exchange connectivity status

Zero. No authenticated endpoints contacted. No public endpoints contacted.

## Exchange-write capability status

Disabled by design. No exchange adapter present, no order-placement code path, no credentials available.

## Recommended next step (proposal only — operator decides)

Per Gate 2 approval and the asymmetry-review memo §H + §J:

- **Primary recommendation: Phase 2p Option A — pause further execution; keep R3 baseline; no immediate new redesign.** A short docs-only operator-strategy-review phase consolidating the R3 baseline, formally recording that R1a stays alive as research-only / non-leading / non-deployable, and deferring further redesign work. Cheapest. Preserves discipline. Aligns with the §H.1 primary recommendation.
- **Fallback recommendation: Phase 2p Option B — docs-only hypothesis-planning for one specific next redesign.** A Phase 2j-style spec-writing phase that develops a falsifiable hypothesis for one of: regime-conditional R1a-prime; R1b (Phase 2i-deferred regime-conditional bias); R2 (Phase 2i-deferred pullback entry). Forces explicit binding-test decision. If the spec passes Phase 2i §1.7 binding test, a future execution Gate 1 becomes available. If not, the operator has documented reason to consolidate.
- **Phase 2p is NOT yet started** by the Phase 2o closure. The Phase 2o operator brief explicitly says "do not start Phase 2p yet"; the Gate 2 approval reaffirms this. Phase 2p is the recommended next phase, but its own start gate is a separate operator decision.

Per Gate 2 approval, the following are **NOT** the next step at this time:

- **Phase 4 (runtime / state / persistence)** — stays deferred per operator policy.
- **Paper/shadow / live-readiness planning** — stays deferred per operator policy.
- **Another execution phase** (Phase 2p execution variant or otherwise) — stays deferred ("do not start another execution phase").
- **Phase 2p itself** is not authorized to start by the Phase 2o closure.

## Question for ChatGPT / operator

None. Phase 2o is complete. All operator brief content requirements applied; all process requirements honored; pytest is at 417 throughout (no source files modified); no new GAP entries needed; the Gate 2 approval explicitly preserved the strategic framings (R3 = research-leading baseline; R1a+R3 NOT framed as the new universal winner; R1a = useful research evidence but not the current deployable / default path; formal H0-anchor judgments preserved exactly) which the memo records throughout. The branch `phase-2o/asymmetry-review` is complete and not yet pushed per operator restriction. Awaiting the operator's next-boundary decision (Phase 2p start authorization, or other).
