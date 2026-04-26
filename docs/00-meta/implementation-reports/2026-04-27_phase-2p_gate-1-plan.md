# Phase 2p — Gate 1 Plan (Option A: R3 Baseline Consolidation)

**Phase:** 2p — Consolidation at R3 Baseline (docs-only).
**Branch:** `phase-2p/r3-baseline-consolidation`.
**Plan date:** 2026-04-27 UTC.
**Working directory:** `C:\Prometheus`.

---

## 1. Purpose

Phase 2o concluded that the BTC/ETH asymmetry under R1a is best treated as evidence about family limits and conditional edge rather than as a reason to keep executing immediately. R3 remains the research-leading baseline. R1a is useful research evidence but not the current default / deployable path. No further immediate execution phase is justified. The Phase 2o §H.1 primary recommendation was Phase 2p Option A — pause; consolidate at R3; no immediate new redesign.

The operator authorized Phase 2p Option A. This phase is a **short docs-only consolidation phase** that:

- Formally pauses further redesign execution.
- Records R3 as the **baseline-of-record** for any future family work.
- Records R1a as **retained research evidence only** (not the current default / deployable path).
- Defines what would need to happen before execution resumes or readiness planning is considered later.

It is consolidation only. No code changes, no new backtests, no new variants, no new data, no parameter changes, no candidate-set widening, no Phase 4 work, no paper/shadow-readiness planning, no execution-phase start.

## 2. Plain-English statement

The project has produced two PROMOTE verdicts (R3 in Phase 2l; R1a+R3 in Phase 2m). R3's is broad-based; R1a+R3's is symbol-asymmetric. After three docs-only review phases (2n family-level review; 2o asymmetry diagnosis), the operator and the project agree that R3 is the version to operate against going forward, that R1a is research-grade evidence rather than a deployable variant, and that more execution work would be premature treadmill behaviour. Phase 2p makes that consolidation explicit on the record so future phases (planning or operational) start from a clear baseline.

## 3. Branch and status verification commands

Already executed at phase start:

```
git -C c:/Prometheus status --short                       # clean
git -C c:/Prometheus rev-parse --abbrev-ref HEAD          # main (was)
git -C c:/Prometheus log --oneline -5                     # 2o merged at ce884f7
git -C c:/Prometheus checkout -b phase-2p/r3-baseline-consolidation
```

Working tree clean before this phase started. `main` is at `ce884f7` (Phase 2o merge); `origin/main` matches.

## 4. Exact scope

- Read the Phase 2l / 2m / 2n / 2o committed reports in full (already familiar from the immediately preceding phases; re-confirm against on-disk text as needed).
- Read the supporting docs the operator brief cites (strategy spec, backtest plan, validation checklist, backtesting principles, walk-forward validation, cost modeling, position-sizing framework, stop-loss policy, exposure limits).
- Produce a written **consolidation memo** with sections A–J per the operator brief.
- Produce a **Gate 2 pre-commit review** that traces every operator-brief content + process requirement to its Phase 2p artifact.
- Produce the **Phase 2p checkpoint report** (after Gate 2 approval, immediately before commits).
- Stop before any commit, awaiting operator/ChatGPT Gate 2 approval.

## 5. Explicit non-goals (hard boundaries)

Per the operator brief:

- No code changes; no source-file edits.
- No new tests.
- No new backtests, runs, or variants.
- No re-running of any existing variant.
- No parameter changes.
- No widening of the candidate set.
- No new data downloads, no new dataset versions, no manifest changes.
- No Binance API calls (authenticated or public).
- No live-trading code, no exchange-write, no production keys.
- No MCP enablement, no `.mcp.json`, no Graphify indexing.
- No Phase 4 work.
- No paper/shadow-readiness planning. No live-readiness planning.
- No execution-phase start.
- No edits to `docs/12-roadmap/technical-debt-register.md`.
- No `data/` commits.
- No re-derivation, re-ranking, or threshold-tightening / threshold-loosening of the §10.3 / §10.4 / §11.3 / §11.4 / §11.6 framework.
- No quiet replacement of H0 as the formal framework anchor.
- No quiet reopening of execution momentum.
- No quiet movement toward readiness planning.
- No live deployment, paper/shadow readiness, or capital exposure proposal.

## 6. Memo content requirements (per operator brief)

The consolidation memo will have sections A–J:

| § | Title                                            | Brief description                                                                                  |
|---|--------------------------------------------------|----------------------------------------------------------------------------------------------------|
| A | Executive summary                                | What Phase 2p does, why consolidation, plain-English current-state summary                          |
| B | Fixed evidence recap                             | Why H0 anchor; why R3 research-leading; why R1a+R3 preserved as research evidence; what family has demonstrated and not |
| C | Consolidated baseline-of-record                   | R3 = baseline-of-record; exact locked R3 definition; operational implications; non-implications     |
| D | Status of R1a                                    | R1a as research evidence; not deployable / default; what to preserve; what not to over-generalize; one of {closed, dormant, retained-for-future-hypothesis-planning} chosen and justified |
| E | Family-level consolidation judgement              | What the family has earned; what it still lacks; why pause; why not abandon; why not readiness-advance |
| F | Future-resumption criteria                        | Pre-conditions for: another execution phase; paper/shadow planning; Phase 4; family abandonment      |
| G | Recommended next-boundary options                 | Five options compared (A: no immediate phase; B: docs-only hypothesis-planning; C: immediate new execution; D: later paper/shadow for R3; E: later new family) — pros / cons / wasted-effort / EVI |
| H | Recommendation                                   | Primary + fallback with explicit reasoning; explicit on stay-paused / next-likely-path / R3-baseline-of-record |
| I | What would change this recommendation             | Switch conditions for each direction                                                                 |
| J | Explicit non-proposal list                        | What Phase 2p explicitly does not do                                                                 |

## 7. Required preservation rules

The memo must enforce:

1. **The formal H0-anchor judgments are preserved exactly as recorded.** R3 PROMOTES on R via §10.3.a + §10.3.c (Phase 2l). R1a+R3 PROMOTES on R via §10.3.c (BTC) + §10.3.a + §10.3.c (ETH) (Phase 2m). H0 remains the sole §10.3 / §10.4 anchor.
2. **R3 remains the research-leading baseline AND becomes the formal baseline-of-record** unless a real contradiction is found.
3. **R1a remains research evidence only** unless a real contradiction is found.
4. **Execution momentum is not quietly reopened.** The memo's recommendation explicitly stays paused.
5. **Readiness planning is not quietly advanced.** Paper/shadow / Phase 4 / live work all remain deferred per operator policy.
6. **If prior docs conflict, the conflict is surfaced explicitly.** No silent reconciliation.

## 8. Required exact R3 lock specification (§C)

The memo must record the exact locked R3 definition for the formal baseline-of-record:

- `exit_kind = FIXED_R_TIME_STOP`
- `exit_r_target = 2.0`
- `exit_time_stop_bars = 8`
- Same-bar priority remains **STOP > TAKE_PROFIT > TIME_STOP**.
- Setup predicate: `RANGE_BASED` (H0 default; not R1a).
- All other Phase 2j memo §D §C invariants preserved (no break-even, no trailing, no stop movement intra-trade for R3; R1a sub-parameters X = 25 / N = 200 frozen for any future R1a-related research).

## 9. Required R1a status decision (§D)

The memo must choose one of three framings for R1a's status going forward and justify the choice:

- **closed** — R1a is permanently abandoned; no future work on R1a or R1a-prime variants.
- **dormant** — R1a is set aside but could be revived via operator decision; no active planning.
- **retained-for-future-hypothesis-planning** — R1a is retained as a candidate axis for future docs-only spec-writing if a regime-conditional R1a-prime hypothesis is independently developed.

The expected choice (consistent with Phase 2o §F.3 + §H.1 + §I.1) is **retained-for-future-hypothesis-planning**, but the memo must justify the choice independently from prior phases — preserving the option to differ if the analysis surfaces a contradiction.

## 10. Required future-resumption criteria (§F)

The memo must define explicit pre-conditions for four scenarios:

1. **Another execution phase is justified.** A falsifiable single-axis structural hypothesis with sub-parameters committed singularly per Phase 2j-style discipline; pre-Gate-1 spec; satisfies Phase 2i §1.7 binding test.
2. **Paper/shadow-readiness planning is justified later.** Operator independently lifts the paper/shadow restriction; R3 evidence is judged sufficient to begin operational scaffolding; absolute-edge expectation re-examined.
3. **Phase 4 becomes appropriate later.** Operator independently lifts the Phase 4 restriction; operational-infrastructure case made independently of strategy candidate.
4. **Abandoning the family becomes appropriate later.** A future structural-redesign attempt produces a clean §10.3 disqualification; or accumulated evidence shows absolute-edge gap is too large; or alternative-family hypothesis with credible mechanism emerges.

## 11. Proposed files / directories

Phase 2p produces docs only:

- `docs/00-meta/implementation-reports/2026-04-27_phase-2p_gate-1-plan.md` — this plan, committed after Gate 2 approval.
- `docs/00-meta/implementation-reports/2026-04-27_phase-2p_consolidation-memo.md` — main consolidation memo (sections A–J).
- `docs/00-meta/implementation-reports/2026-04-27_phase-2p_gate-2-review.md` — pre-commit review.
- `docs/00-meta/implementation-reports/2026-04-27_phase-2p-checkpoint-report.md` — checkpoint, drafted after Gate 2 approval, immediately before commits.

No other files touched.

## 12. No code / dependency changes

No source code changes. No tests added or modified. No new top-level packages. No new dependencies. No `pyproject.toml` or `uv.lock` change.

## 13. Output artifacts

- **Committed (to git, after Gate 2 approval):** Gate 1 plan, consolidation memo, Gate 2 review, checkpoint report.
- **Not committed:** none — Phase 2p produces no intermediate parquet, no run output, no notebook artifact.
- **Presented to operator / ChatGPT:** concise markdown summaries with tables. No screenshots.

## 14. Safety constraints (apply throughout Phase 2p)

| Check | Requirement |
|---|---|
| Production Binance keys | none, not requested, not referenced |
| Exchange-write code | none |
| Credentials | none — no `.env`, no secrets in any artifact |
| `.mcp.json` | not created |
| Graphify | not enabled |
| MCP servers | not activated |
| Manual trading controls | none |
| Strategy / risk / data / cost-model edits | none (docs-only) |
| Binance public URLs | none fetched |
| `.claude/settings.json` | preserved |
| Destructive git commands | none proposed |
| Changes outside working tree | none |
| New dependencies | none |
| `data/` commits | none |
| `technical-debt-register.md` edits | none (operator restriction) |
| Phase 4 work | none (operator restriction) |
| Phase 2q work | none (this is a closure phase; does not propose / start a 2q execution) |
| Paper/shadow / tiny-live planning | none (operator restriction) |
| New backtests / variants / data | none |
| Tightening / loosening of any §10.3 / §10.4 / §11.3 / §11.4 / §11.6 threshold | none |
| H0 anchor preservation | enforced |
| R3 research-leading framing preservation | enforced |
| R3 promotion to formal baseline-of-record | recorded explicitly |
| R1a research-evidence-only framing preservation | enforced |

## 15. Ambiguity / spec-gap items

**No new GAP entries proposed in Phase 2p.** Phase 2p carries forward existing GAPs unchanged. If the consolidation review surfaces a doc inconsistency that meets the bar for a permanent GAP entry, the memo will surface it but Phase 2p will NOT edit the ambiguity log unilaterally.

## 16. Technical-debt register — no edits

`docs/12-roadmap/technical-debt-register.md` is NOT edited in Phase 2p. The accumulated R3 + R1a+R3 evidence base is informational input for any future operator review of TD-016, but the register itself stays untouched per operator restriction.

## 17. Proposed commit structure (end of Phase 2p)

Four commits on `phase-2p/r3-baseline-consolidation`, after operator gate approvals (Gate 1 = this plan; Gate 2 = pre-commit review). Pytest runs before each commit and is expected at **417 passed** (no code change anywhere).

1. `phase-2p: Gate 1 plan` — this file's content.
2. `phase-2p: consolidation memo` — the sections-A–J narrative.
3. `phase-2p: Gate 2 review`.
4. `phase-2p: checkpoint report`.

No `data/` commits. No `src/` or `tests/` commits. No `pyproject.toml` edits. No merge yet — push and PR decision deferred to operator. No `Co-Authored-By` trailer (consistent with prior phases).

## 18. Gate 2 review format

```
Phase: 2p — Consolidation at R3 Baseline (Option A)
Scope confirmed against Gate 1 plan: yes / no + diffs
Docs written: list
Memo sections A–J: present / complete / threshold-preserving check
H0 anchor preservation: enforced
R3 research-leading framing preservation: enforced
R3 promotion to formal baseline-of-record: recorded
R1a research-evidence-only framing preservation: enforced
R1a status framing chosen and justified: closed / dormant / retained-for-future-hypothesis-planning
Execution momentum NOT quietly reopened: confirmed
Readiness planning NOT quietly advanced: confirmed
Recommendation: primary + fallback recorded with reasoning
Future-resumption criteria for execution / paper-shadow / Phase 4 / family-abandonment: present
What-would-change-recommendation switch conditions: present
Next-boundary options analysis: present (≥ 5 options)
Non-proposal list: present
Wave-1 / Phase 2l / Phase 2m / Phase 2n / Phase 2o results preservation: confirmed
Threshold preservation: §10.3 / §10.4 / §11.3 / §11.4 / §11.6 unchanged
Safety posture: no code, no data, no APIs, no MCP, no Graphify, no TD-register edits
Operator restrictions honoured: yes
Test suite: pytest 417 passed (no code change expected)
Recommended next step: operator decides among the next-boundary options
Questions for operator: list or "none"
```

## 19. Checkpoint report format

Follows `.claude/rules/prometheus-phase-workflow.md` exactly. Phase 2p checkpoint includes: Phase, Goal, Summary, Files changed (all docs), Files created (all docs), Commands run (none safety-relevant — pytest + git status/diff), Installations performed (none), Configuration changed (none), Tests/checks passed (pytest 417 expected), Tests/checks failed (none expected), Known gaps (none new), Safety constraints verified (full table), Current runtime capability (research-only, unchanged), Exchange connectivity status (zero), Exchange-write capability (disabled), Recommended next step (proposal only — operator decides among the next-boundary options).

## 20. Approval gates

Two operator approvals bracket Phase 2p:

- **Gate 1 — this plan.** Approve or redirect the scope, the memo content requirements, the preservation rules, and the proposed deliverables.
- **Gate 2 — pre-commit review.** After the consolidation memo + Gate 2 review are drafted, the operator reviews the diff + pytest output before any `git add` / `git commit`.

## 21. Post-approval execution sequence (docs-only)

After Gate 1 approval, proceed in this order and **stop before any `git add` / `git commit`**:

1. **Verify branch state.** Already on `phase-2p/r3-baseline-consolidation` from clean main.
2. **Write this approved Gate 1 plan** to `docs/00-meta/implementation-reports/2026-04-27_phase-2p_gate-1-plan.md` (this file).
3. **Draft the consolidation memo** at `docs/00-meta/implementation-reports/2026-04-27_phase-2p_consolidation-memo.md`, structured around §§ 6–10 of this plan plus the section-A–J content requirements.
4. **Draft Gate 2 review** at `docs/00-meta/implementation-reports/2026-04-27_phase-2p_gate-2-review.md` using the §18 format.
5. **Stop.** Show operator `git status`, `git diff --stat`, and `uv run pytest` output (expect 417 passed). Do **not** run `git add` / `git commit`. Await operator/ChatGPT Gate 2 review.

The Phase 2p checkpoint report (§19) is produced after Gate 2 approval, immediately before the commit sequence (§17).

**Awaiting operator/ChatGPT Gate 2 approval to commit, after the memo + Gate 2 review are drafted at the stop point.**
