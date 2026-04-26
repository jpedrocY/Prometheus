# Phase 2j — Gate 1 Plan: Structural Redesign Memo Only

**Working directory:** `C:\Prometheus`
**Plan date:** 2026-04-24
**Branch:** `phase-2j/structural-redesign-memo` (created from `main` at `8a34f20` — verified clean working tree, synchronized with `origin/main` after the Phase 2i PR #10 merge)
**Scope:** Docs-only structural-redesign memo phase. No code, no edits to source, no new backtests, no new variants, no new data, no Binance API calls, no MCP/Graphify, no `.mcp.json`, no Phase 4 work, no fallback-Wave-2 start, no edits to `docs/12-roadmap/technical-debt-register.md`.

---

## Context — why this phase, why now

Phase 2i recommended **Phase 2j Option A — Structural redesign memo only (docs-only)** as the provisional primary path forward, with carry-forward set **R1a + R3** capped at ≤ 2 candidates per Phase 2i Gate 1 condition 1. The operator approved Phase 2i Gate 2 and authorized starting Phase 2j with the same docs-only scope. **Phase 2j writes full rule specs for the two carry-forward candidates** (R1a Volatility-percentile setup; R3 Fixed-R exit with time stop), pins committed sub-parameter values, defines candidate-specific falsifiable hypotheses, and prepares the project for a later operator-approved execution-planning phase. **Phase 2j does not execute the candidates, write code, or run anything.**

---

## 1. Executive summary

Phase 2j produces a single committable structural-redesign memo with full rule specs for R1a and R3, plus a Gate 1 plan, a Gate 2 review, and a checkpoint report. The memo:

- Reproduces the binding Phase 2i §1.7 structural-vs-parametric definition.
- Writes complete rule specs for R1a (Family-S setup-pattern volatility-percentile) and R3 (Family-X fixed-R exit with time stop), each with thesis, exact rule shape, exact inputs, exact timeframes, exact predicate, replaced-vs-kept, committed sub-parameter values, expected mechanism of improvement, expected main failure mode, structural-vs-parametric justification, GAP dispositions, and a falsifiable hypothesis pre-declared against the §10.3 / §10.4 thresholds.
- Provides a side-by-side R1a vs. R3 comparison covering thesis, expected effect on trade count / expectancy / drawdown, implementation complexity, overfitting risk, validation burden, and execution-suitability ranking.
- Restates the common validation framework (H0-only anchor; wave-1 historical-only; §10.3/§10.4/§11.3/§11.4/§11.6 unchanged; R/V split; GAP-036 fold convention; mandatory diagnostics including GAP-032 mark-price sensitivity).
- Issues an execution-readiness assessment for each candidate (ready / needs more docs / drop) and a recommendation among (both advance / R1a only / R3 only / neither without more docs).
- Includes "What would change this recommendation" with explicit switch conditions and an explicit non-proposal list.

**Headline recommendation, provisional and subject to operator review:** the memo will conclude with a recommendation for which candidate(s) advance to a future operator-approved execution-planning phase. The recommendation will not be predetermined — it follows from the spec writing and execution-readiness assessment.

## 2. Plain-English statement

Phase 2i told us "structural redesign of the breakout family is the right next step; carry forward R1a (volatility-percentile setup) and R3 (fixed-R exit) — but pick at most two and don't bundle." Phase 2j writes the actual rule specs. Each spec answers: what exactly is the rule, what numbers does it use, what is it replacing, what is it keeping, how would we know if it failed? At the end, Phase 2j says whether one or both candidates are ready to be planned for execution by a later operator-approved phase. **Phase 2j does not run anything. It does not write code. It writes the rules.**

## 3. Branch and status verification commands

After approval (already in place at start of this phase):

```
git -C c:/Prometheus status --short
git -C c:/Prometheus rev-parse --abbrev-ref HEAD
git -C c:/Prometheus log --oneline -10
git -C c:/Prometheus checkout -b phase-2j/structural-redesign-memo
```

Verified at phase start: clean working tree on `main` at `8a34f20` (Phase 2i PR #10 merge); branch `phase-2j/structural-redesign-memo` created.

## 4. Exact scope

- Read the Phase 2e baseline summary, Phase 2g comparison report, Phase 2h decision memo, Phase 2i Gate 1 plan + redesign-analysis memo + Gate 2 review + checkpoint report. Confirm the recap and design choices below match the on-disk record.
- Produce a written structural-redesign memo with sections A–J per the operator's required structure (executive summary; fixed evidence recap; full R1a spec; full R3 spec; side-by-side comparison; common validation framework restated; execution-readiness assessment; recommendation; "what would change this recommendation"; explicit non-proposal list).
- Pin committed sub-parameter values for both candidates. Each value chosen is justified as a research default (round number, defensible without fitting), not a tuned value. Pre-committed before any execution.
- Produce a Gate 2 pre-commit review.
- Produce a Phase 2j checkpoint report.
- Stop before any commit awaiting operator/ChatGPT Gate 2 approval.

## 5. Explicit non-goals (hard boundaries)

- No code changes. No new tests. No new backtests, runs, or variants.
- No re-running of H0 or any H-* variant.
- No expansion of the carry-forward set beyond R1a + R3 unless a documentation inconsistency forces escalation.
- No introduction of additional candidates (R1b, R2, or any new family).
- No disguised parameter sweeps (each sub-parameter value is committed singularly; if the spec admits a range, that is a fitting risk, not a structural rule, and the memo says so).
- No comparison of R1a or R3 to wave-1 variants (H-A1, H-B2, H-C1, H-D3) as promotion baselines. H0 only.
- No new data downloads, no new dataset versions, no manifest changes.
- No Binance API calls (authenticated or public).
- No live-trading code, no exchange-write, no production keys.
- No MCP enablement, no `.mcp.json`, no Graphify indexing.
- No Phase 4 work.
- No fallback Wave 2 / H-D6 start.
- No edits to `docs/12-roadmap/technical-debt-register.md` (operator restriction held).
- No `data/` commits.
- No re-derivation or re-ranking of the wave-1 result (REJECT ALL preserved per Phase 2g).
- No re-framing of the Phase 2h provisional recommendation or the Phase 2i recommendation (both are inputs).
- No threshold tightening or loosening on §10.3 / §10.4 / §11.3 / §11.4 / §11.6.
- No live deployment, paper/shadow readiness, or capital exposure proposal.

## 6. Required deliverables

Per operator instructions:

1. Gate 1 plan — this file.
2. Structural redesign memo (the meat) — `docs/00-meta/implementation-reports/2026-04-24_phase-2j_structural-redesign-memo.md`.
3. Gate 2 review — `docs/00-meta/implementation-reports/2026-04-24_phase-2j_gate-2-review.md`.
4. Checkpoint report — `docs/00-meta/implementation-reports/2026-04-24_phase-2j-checkpoint-report.md` (written after Gate 2 approval, immediately before commits).

## 7. Sub-parameter value commitment policy

The operator explicitly requires "exact committed sub-parameter values" for both R1a and R3. The memo will commit each value as a single number, not a range, not a sweep. The chosen values are justified as **research defaults** drawn from common literature or aligned with existing project conventions, not as values selected for fitting. Each commit is final for the spec; if the eventual execution phase wants different values, that requires a new operator-approved spec.

For R1a, the memo will commit:
- Percentile threshold (a single number; expected ~25th percentile based on standard volatility-contraction practice).
- Lookback length (a single number; expected ~200 bars based on 50 hours / multi-day vol regime context).
- Minimum sample / warmup rule (the spec must state explicitly when the percentile becomes computable).

For R3, the memo will commit:
- R-multiple take-profit target (a single number; expected 2.0R as the cleanest fixed-target convention).
- Time-stop bar count (a single number; expected 8 bars to align with the existing stagnation-window time horizon in the v1 spec).

If the memo finds that any single sub-parameter value is unjustifiable as a research default (e.g., the analysis shows the value depends on the data in a way that can't be defended without fitting), the memo will say so explicitly and recommend dropping the candidate per operator instruction "If R1a or R3 cannot be specified cleanly without hidden degrees of freedom, say so explicitly."

## 8. Falsifiable hypothesis structure

Each candidate's falsifiable hypothesis takes the form:

> "On R = 2022-01..2025-01 with v002 datasets, [Candidate] (with the committed sub-parameter values from this spec) produces a §10.3-passing result vs. H0 baseline (i.e., either §10.3.a or §10.3.b path, with no §10.3 disqualification floor triggered). The hypothesis is FALSIFIED if [Candidate] does not pass §10.3, OR if it triggers §10.3 disqualification (worse expR / worse PF / |maxDD| > 1.5× baseline)."

The hypothesis is **pre-committed before any execution**. No post-hoc threshold loosening. No "different threshold because the redesign is different" — Phase 2f §11.3.5 thresholds apply unchanged.

## 9. Validation framework (memo will restate)

- H0 (locked Phase 2e baseline re-run on R) is the only comparison anchor.
- Wave-1 variants (H-A1, H-B2, H-C1, H-D3) are historical evidence only, not promotion baselines.
- §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds applied unchanged.
- R/V split per Phase 2f §11.1: R = 2022-01..2025-01; V = 2025-01..2026-04.
- Fold scheme per GAP-20260424-036: 5 rolling folds, fold 1 partial-train, all tests within R.
- Mandatory diagnostics: per-regime expR (volatility regime tagging); MFE distribution; long/short asymmetry; GAP-032 mark-price sensitivity for promoted candidates.
- §1.7.3 project-level locks preserved (BTCUSDT live primary, one-position, isolated margin, 0.25% live risk, 2x leverage, mark-price stops, v002 datasets).

## 10. GAP disposition map (memo will reproduce per-candidate)

Per Phase 2i memo §2.4 (4-candidate matrix; R1a and R3 columns inherited):

| GAP | Topic | R1a (Family S) | R3 (Family X) |
|---|---|---|---|
| GAP-20260424-030 | Break-even rule-text conflict | CARRIED (R1a keeps current exit logic) | **SUPERSEDED** (R3 removes break-even from exit machinery) |
| GAP-20260424-031 | EMA slope wording | CARRIED (R1a keeps current bias rule) | CARRIED (R3 keeps current bias rule) |
| GAP-20260424-032 | Mark-price sensitivity | CARRIED — required report cut for promoted candidate | CARRIED — required report cut for promoted candidate |
| GAP-20260424-033 | Stagnation window classification | CARRIED (R1a keeps current exit including stagnation) | **CARRIED-AND-EXTENDED** (R3's time-stop replaces stagnation; spec must state interpretation) |

The memo's per-candidate spec sections C and D will reproduce the relevant rows verbatim.

## 11. Required diagnostics for any future execution phase

Per Phase 2i memo §2.5.5 (binding for any future execution wave that runs R1a or R3):

- **Per-regime expR**: classify each trade's entry by realized 1h volatility regime (low/medium/high based on trailing percentile) and compute per-regime expR.
- **MFE distribution**: histogram of MFE in R-multiples to characterize where in the trade lifecycle profit is captured or missed.
- **Per-direction long/short asymmetry**: separate expR / PF / win rate for long-only and short-only subsets.
- **GAP-032 mark-price sensitivity**: every promoted candidate must run with `stop_trigger_source=TRADE_PRICE` and report comparison vs. MARK_PRICE.

These are diagnostic requirements, not pre-execution work. Phase 2j does not implement them; Phase 2j records them as the contract any future execution phase inherits.

## 12. Anti-disguised-parameter-sweep discipline

Per the operator's process requirements: "Do not introduce disguised parameter sweeps." The memo's spec sections must commit each sub-parameter to a single value. If at memo-writing time the analysis cannot defend a single value (e.g., "we'd need to test 20%, 25%, 30% to know which percentile works"), the memo declares that candidate **not ready for execution planning** and recommends dropping it per the operator's "say so explicitly" instruction.

The execution-readiness assessment in section G of the memo is the binding output: each candidate is rated as ready / needs-more-docs / drop. A candidate that requires a sweep to commit values is not ready.

## 13. Preservation contracts

The memo preserves:

- **Phase 2g wave-1 verdict (REJECT ALL)** — quoted facts may be cited diagnostically; never re-derived; never re-ranked.
- **H0 as sole comparison anchor** — restated in section F.
- **Phase 2i ≤ 2 carry-forward discipline** — only R1a and R3 are specced; no expansion.
- **Phase 2h provisional recommendation framing** — input to Phase 2i, not target for revision.
- **§10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds** — unchanged.
- **§1.7.3 project-level locks** — unchanged.
- **GAP-20260424-036 fold scheme** — unchanged.

## 14. Proposed files / directories

Phase 2j produces docs only:

- `docs/00-meta/implementation-reports/2026-04-24_phase-2j_gate-1-plan.md` — this plan.
- `docs/00-meta/implementation-reports/2026-04-24_phase-2j_structural-redesign-memo.md` — the main spec memo (sections A–J).
- `docs/00-meta/implementation-reports/2026-04-24_phase-2j_gate-2-review.md` — pre-commit review.
- `docs/00-meta/implementation-reports/2026-04-24_phase-2j-checkpoint-report.md` — checkpoint.

No other files touched. No `src/`, `tests/`, `scripts/`, `configs/`, `pyproject.toml`, `.claude/`, `data/`, or `technical-debt-register.md` edits. No ambiguity-log changes anticipated; if a new GAP surfaces (unlikely given the §1.7 binding test handled prior judgements), it would be appended.

## 15. No code / dependency changes

No source code changes. No tests added or modified. No new top-level packages. No new dependencies. No `pyproject.toml` or `uv.lock` change.

## 16. Output artifacts

- **Committed (to git, after Gate 2 approval):** Gate 1 plan, structural-redesign memo, Gate 2 review, checkpoint report.
- **Not committed:** none — Phase 2j produces no intermediate parquet, no run output, no notebook artifact, no code artifact.
- **Presented to operator / ChatGPT:** concise markdown summaries with tables. No screenshots.

## 17. Safety constraints

| Check | Requirement |
|---|---|
| Production Binance keys | none, not requested, not referenced |
| Exchange-write code | none |
| Credentials | none — no `.env`, no secrets in any artifact |
| `.mcp.json` | not created |
| Graphify | not enabled |
| MCP servers | not activated |
| Manual trading controls | none |
| Strategy logic edits | none |
| Risk engine edits | none |
| Data ingestion edits | none |
| Exchange adapter edits | none |
| Binance public URLs | none fetched |
| `.claude/settings.json` | preserved |
| Destructive git commands | none proposed |
| Changes outside working tree | none |
| New dependencies | none |
| `data/` commits | none |
| `technical-debt-register.md` edits | none (operator restriction) |
| Phase 4 work | none (operator restriction) |
| Fallback Wave 2 / H-D6 start | none (operator restriction) |
| Phase 2k execution-planning work | none (this phase proposes a future execution-planning phase, does not start it) |
| New backtests / variants / data | none |
| Tightening / loosening of any §10.3 / §10.4 / §11.3 / §11.4 / §11.6 threshold | none |
| Re-derivation of wave-1 verdict | none — REJECT ALL preserved |
| Re-framing of Phase 2h or Phase 2i recommendation | none — both are inputs |
| Quietly re-classifying parametric as structural | none — Phase 2i §1.7 binding test applies |
| Comparing redesign candidates to wave-1 variants as baselines | none — H0 only |
| Disguised parameter sweeps | none — single committed value per sub-parameter |
| Expanding carry-forward beyond R1a + R3 | none unless documentation inconsistency forces escalation |

## 18. Ambiguity / spec-gap items to log

None anticipated. The Phase 2i §1.7 binding test handled all structural-vs-parametric judgements made in Phase 2i; Phase 2j inherits that test. If during memo writing a new ambiguity surfaces (e.g., a v1-spec corner case that materially affects R1a or R3 spec writing), the memo will record it inline and propose either:

- a clarification in the memo itself (no new GAP), or
- if the ambiguity is structural and outlasts this phase, a new GAP-20260424-037 entry.

Most likely no new GAP is needed.

## 19. Technical-debt register — no edits

`docs/12-roadmap/technical-debt-register.md` is NOT edited in Phase 2j. TD-016 (statistical live-performance thresholds) is informationally affected by R1a / R3 specs (any future execution result against these specs is direct evidence for TD-016) but the register itself stays untouched per operator restriction.

## 20. Proposed commit structure (end of Phase 2j)

Four commits on `phase-2j/structural-redesign-memo`, after two operator gate approvals (Gate 1 = this plan; Gate 2 = pre-commit review). Pytest runs before each commit and is expected at 396 passed (no code change anywhere).

1. `phase-2j: Gate 1 plan` — this file.
2. `phase-2j: structural redesign memo (R1a + R3)` — the main spec memo.
3. `phase-2j: Gate 2 review` — pre-commit review.
4. `phase-2j: checkpoint report` — phase closure.

No `data/` commits. No `src/` or `tests/` commits. No `pyproject.toml` edits. No merge yet — push and PR decision deferred to operator. No `Co-Authored-By` trailer (consistent with prior phases).

## 21. Gate 2 review format (to be produced at end of 2j)

```
Phase: 2j — Structural Redesign Memo Only
Scope confirmed against Gate 1 plan: yes / no + diffs
Docs written: list
Ambiguity-log appends: list (GAP IDs) — likely empty
Carry-forward discipline: only R1a and R3 specced; no third candidate added
R1a spec completeness: thesis / rule shape / inputs / TF / predicate / replaced-vs-kept / committed sub-params / mechanism / failure mode / structural justification / GAPs / falsifiable hypothesis / candidate-specific diagnostics
R3 spec completeness: same checklist as R1a
Side-by-side comparison: thesis / trade count / expR / drawdown / complexity / overfitting / validation burden / execution-suitability ranking
Common validation framework: H0-only anchor; wave-1 historical-only; thresholds + R/V split + GAP-036 fold scheme + mandatory diagnostics
Execution-readiness assessment: per-candidate ready / needs-more-docs / drop
Recommendation: both / R1a only / R3 only / neither
"What would change this recommendation": present
Explicit non-proposal list: present
Wave-1 result preserved: REJECT ALL stands
H0 anchor preserved: yes
Phase 2i ≤ 2 carry-forward preserved: yes
Threshold preservation: §10.3 / §10.4 / §11.3 / §11.4 / §11.6 unchanged
§1.7.3 project-level locks preserved: yes
Disguised parameter sweeps avoided: yes (single committed value per sub-parameter)
Safety posture: no code, no data, no APIs, no MCP, no Graphify, no TD-register edits
Operator restrictions honoured: yes
Test suite: pytest 396 passed (no code change expected)
Recommended next step: operator decides among advance both / advance one / advance neither / consider fallback / consider Phase 4
Questions for operator: list or "none"
```

## 22. Checkpoint report format

Follows `.claude/rules/prometheus-phase-workflow.md` exactly: Phase, Goal, Summary, Files changed (all docs), Files created (all docs), Commands run (none safety-relevant — pytest + git status/diff), Installations performed (none), Configuration changed (none), Tests/checks passed (pytest 396 expected), Tests/checks failed (none), Known gaps (likely none new; pre-existing GAPs unchanged), Safety constraints verified (full table), Current runtime capability (research-only, unchanged), Exchange connectivity status (zero), Exchange-write capability (disabled), Recommended next step (proposal only).

## 23. Approval gates

- **Gate 1 — this plan.** Pre-approved by the operator's "Approved to start Phase 2j planning/execution only within docs-only scope" message. The plan is committed in commit 1 alongside the redesign memo.
- **Gate 2 — pre-commit review.** After redesign memo + Gate 2 review + checkpoint report drafted, operator reviews diff + pytest output before any `git add` / `git commit`.

## 24. Post-approval execution sequence (docs-only)

1. Verify branch state (working tree should show the Gate 1 plan as untracked; branch is `phase-2j/structural-redesign-memo`).
2. Branch already created (done).
3. Write this Gate 1 plan to `docs/00-meta/implementation-reports/2026-04-24_phase-2j_gate-1-plan.md` (this step).
4. Draft the structural redesign memo at `docs/00-meta/implementation-reports/2026-04-24_phase-2j_structural-redesign-memo.md`, with sections A–J per operator scope: executive summary; fixed evidence recap; full R1a spec; full R3 spec; side-by-side comparison; common validation framework; execution-readiness assessment; recommendation; "what would change this recommendation"; explicit non-proposal list.
5. Draft Gate 2 review at `docs/00-meta/implementation-reports/2026-04-24_phase-2j_gate-2-review.md` using the §21 format.
6. Stop. Show operator `git status`, `git diff --stat`, and `uv run pytest` output (expect 396 passed). Do not run `git add` / `git commit`. Await operator/ChatGPT Gate 2 review.

The Phase 2j checkpoint report (§22) is produced after Gate 2 approval, immediately before the commit sequence (§20).
