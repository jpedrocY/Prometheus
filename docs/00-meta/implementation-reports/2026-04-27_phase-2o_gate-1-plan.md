# Phase 2o — Gate 1 Plan

**Phase:** 2o — Targeted Asymmetry Review / Analysis (docs-only).
**Branch:** `phase-2o/asymmetry-review`.
**Plan date:** 2026-04-27 UTC.
**Working directory:** `C:\Prometheus`.

---

## 1. Purpose

Phase 2n concluded that R3 is the research-leading baseline and that R1a+R3 is a formal but strategically mixed PROMOTE: R1a materially helps ETH and materially hurts BTC relative to the locked R3 baseline. Phase 2n's recommendation was Option A (R3 as research-leading; stop further immediate execution) with Option B (targeted asymmetry review) as the fallback continuation. The operator authorized Option B.

Phase 2o is that targeted asymmetry review. It is a **docs-only judgement / analysis phase** — no code changes, no new backtests, no new variants, no new data, no parameter changes, no candidate-set widening, no Phase 4 work, no paper/shadow / live-readiness planning, no execution-phase start.

The phase examines the existing Phase 2m evidence in depth to decide whether the BTC/ETH asymmetry points to (a) a fixable next hypothesis inside the breakout family, (b) a symbol-specific limitation of R1a, (c) a regime-specific effect, or (d) a reason to stop further immediate execution. It produces a recommendation, not a decision; the operator decides.

## 2. Plain-English statement

Phase 2m showed something curious: R1a's volatility-percentile filter helps ETH a lot and hurts BTC a bit. Both happen on the same data with the same filter; the filter itself works as designed (100% of R1a entries at percentile ≤ 25%). Phase 2o asks "what is going on?" — does this asymmetry tell us about how to fix the strategy further, or does it tell us this is roughly as good as the family gets and we should stop pushing? Phase 2o is the operator's chance to think hard about that question before deciding the next phase.

## 3. Branch and status verification commands

Already executed:

```
git -C c:/Prometheus status --short                       # clean
git -C c:/Prometheus rev-parse --abbrev-ref HEAD          # main
git -C c:/Prometheus log --oneline -5                     # 2n merged at c20da51
git -C c:/Prometheus checkout -b phase-2o/asymmetry-review
```

Working tree clean before this phase started. `main` is at `c20da51` (Phase 2n merge); `origin/main` matches.

## 4. Exact scope

- Read the Phase 2g / 2l / 2m / 2n committed reports plus the supporting strategy / backtesting / risk specs.
- Re-read the Phase 2m run artifacts on disk (`data/derived/backtests/phase-2m-r1a-*/`) **only as committed evidence** — no re-running of the analysis script, no re-derivation of statistics that would constitute new evidence. Citing already-computed numbers from the comparison report is allowed; computing new numbers is not.
- Produce a written **asymmetry-review memo** with sections A–K per the operator brief.
- Produce a **Gate 2 pre-commit review** that traces every operator-brief content + process requirement to its Phase 2o artifact.
- Produce the **Phase 2o checkpoint report** (after Gate 2 approval, immediately before commits).
- Stop before any commit, awaiting operator/ChatGPT Gate 2 approval.

## 5. Explicit non-goals (hard boundaries)

Per the operator brief:

- No code changes; no source-file edits.
- No new tests.
- No new backtests, runs, or variants.
- No re-running of any existing variant.
- No parameter changes.
- No widening of the candidate set (only H0 / R3 / R1a+R3 referenced).
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
- No quiet conversion of ETH-specific strength into a universal recommendation.
- No live deployment, paper/shadow readiness, or capital exposure proposal.

## 6. Memo content requirements (per operator brief)

The asymmetry-review memo will have sections A–K:

| § | Title                                            | Brief description                                                                                  |
|---|--------------------------------------------------|----------------------------------------------------------------------------------------------------|
| A | Executive summary                                | What Phase 2o does, why analysis-only, plain-English BTC/ETH asymmetry summary                      |
| B | Fixed evidence recap                             | R3 / R1a+R3 / asymmetry headlines; what is now known and what is not                                |
| C | Asymmetry diagnosis framework                    | Six candidate explanations evaluated (symbol-specific, regime-composition, sample-fragility, setup-shape, directional-bias, family-limitation) |
| D | BTC-vs-ETH evidence synthesis                    | R-window / V-window / per-fold / per-regime / long/short / trade-frequency-funnel deltas             |
| E | Interpretation of R1a mechanism                  | Implementation correctness; compression-genuineness; whose problem (compression concept vs BTC follow-through) |
| F | Fixability analysis                              | Four future-direction hypotheses (regime-conditional, symbol-conditional, R1a abandonment, different setup redesign) — analysis only |
| G | Family-level implication                         | What this asymmetry implies; R3 confidence; setup-side redesign generally vs R1a specifically       |
| H | Recommendation                                   | Primary + fallback with explicit reasoning; explicit on R3 / R1a / future-execution / phase-closure |
| I | What would change this recommendation            | Switch conditions for each direction                                                                 |
| J | Next-phase options                               | Phase 2p variants compared on pros/cons/wasted-effort/EVI                                            |
| K | Explicit non-proposal list                       | What Phase 2o explicitly does not do                                                                 |

## 7. Required preservation rules

The memo must enforce:

1. **The formal H0-anchor judgments are preserved exactly as recorded.** R3 PROMOTES on R via §10.3.a + §10.3.c (Phase 2l). R1a+R3 PROMOTES on R via §10.3.c (BTC) + §10.3.a + §10.3.c (ETH) (Phase 2m).
2. **R3 as the research-leading baseline is preserved unless a real contradiction is found.** Phase 2n committed this framing; Phase 2o does not undo it without explicit evidence.
3. **R1a+R3 as a promoted but non-leading / mixed branch is preserved unless a real contradiction is found.** Phase 2n committed this framing.
4. **ETH-specific strength is not quietly converted into a universal recommendation.** If the analysis surfaces stronger ETH evidence, that evidence is reported under the "specialty / regime-conditional" framing, not under a "universal next variant" framing.
5. **Another execution phase is not recommended unless the memo can justify one clearly and narrowly** with a falsifiable hypothesis, a single-axis structural change, sub-parameters committed singularly, and §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds preserved unchanged.
6. **If prior docs conflict, the conflict is surfaced explicitly.** No silent reconciliation.

## 8. Required candidate explanations to evaluate (§C)

The memo must explicitly evaluate at least these six candidate explanations for the BTC/ETH asymmetry:

1. **Symbol-specific market-behavior explanation** — BTC and ETH have intrinsically different post-compression behaviour on the v002 R-window data; R1a's filter exposes that pre-existing difference rather than creating it.
2. **Regime-composition explanation** — R1a's bottom-quartile filter selects regimes that are well-distributed for one symbol but skewed against the other; the asymmetry is regime-mix-driven.
3. **Trade-count / sample-fragility explanation** — 22 BTC / 23 ETH trades on R, 4 BTC / 8 ETH on V; the asymmetry might be statistical noise.
4. **Setup-selection-shape explanation** — R1a's percentile predicate has a different selection geometry from H0's range-based predicate; the asymmetry is a selection-bias artifact.
5. **Directional-bias interaction explanation** — the breakout-on-bias entry rule interacts with R1a's compression filter differently across symbols (R1a+R3 ETH shorts +0.387 PF 1.906 — ETH shorts dominate; ETH longs catastrophic).
6. **Family-limitation explanation** — the breakout family is approaching its useful-edge ceiling; R1a's asymmetry is a sign that further structural redesign inside the family won't move the needle.

For each: why plausible, what existing evidence supports it, what existing evidence weakens it, whether it points to a fixable next hypothesis or not.

## 9. Required future-direction hypotheses to evaluate (§F)

The memo must evaluate at least four possible future directions **as hypotheses, not as execution approvals**:

1. **Regime-conditional R1a application** — apply R1a's percentile filter only in specified regimes (e.g., only when 1h volatility is in a defined band).
2. **Symbol-conditional use of R1a** — apply R1a only on ETH, leaving BTC under R3 alone (note: this would conflict with Phase 2i §1.7.3 BTC-primary lock unless the operator independently relaxes that).
3. **R1a abandonment while keeping R3** — drop R1a entirely; treat R3 alone as the locked baseline going forward.
4. **A different setup-side redesign altogether** — abandon R1a's percentile-based shape; consider a different setup-validity rule shape (e.g., volatility-contraction-by-time, structural-pattern-based).

For each: potential upside, overfitting risk, policy / project-lock conflict risk, expected value of information, whether it should stay alive or be dropped.

## 10. Proposed files / directories

Phase 2o produces docs only:

- `docs/00-meta/implementation-reports/2026-04-27_phase-2o_gate-1-plan.md` — this plan, committed after Gate 2 approval.
- `docs/00-meta/implementation-reports/2026-04-27_phase-2o_asymmetry-review-memo.md` — main asymmetry-review memo (sections A–K).
- `docs/00-meta/implementation-reports/2026-04-27_phase-2o_gate-2-review.md` — pre-commit review.
- `docs/00-meta/implementation-reports/2026-04-27_phase-2o-checkpoint-report.md` — checkpoint, drafted after Gate 2 approval, immediately before commits.

No other files touched.

## 11. No code / dependency changes

No source code changes. No tests added or modified. No new top-level packages. No new dependencies. No `pyproject.toml` or `uv.lock` change.

## 12. Output artifacts

- **Committed (to git, after Gate 2 approval):** Gate 1 plan, asymmetry-review memo, Gate 2 review, checkpoint report.
- **Not committed:** none — Phase 2o produces no intermediate parquet, no run output, no notebook artifact.
- **Presented to operator / ChatGPT:** concise markdown summaries with tables. No screenshots.

## 13. Safety constraints (apply throughout Phase 2o)

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
| Phase 2p work | none (this is the phase that proposes 2p, not starts it) |
| Paper/shadow / tiny-live planning | none (operator restriction) |
| New backtests / variants / data | none |
| Tightening / loosening of any §10.3 / §10.4 / §11.3 / §11.4 / §11.6 threshold | none |
| H0 anchor preservation | enforced |
| R3 research-leading framing preservation | enforced |
| R1a+R3 promoted-but-non-leading framing preservation | enforced |

## 14. Ambiguity / spec-gap items

**No new GAP entries proposed in Phase 2o.** Phase 2o carries forward existing GAPs unchanged. If the asymmetry review surfaces a doc inconsistency that meets the bar for a permanent GAP entry, the memo will surface it but Phase 2o will NOT edit the ambiguity log unilaterally.

## 15. Technical-debt register — no edits

`docs/12-roadmap/technical-debt-register.md` is NOT edited in Phase 2o. The accumulated R3 + R1a+R3 evidence base is informational input for any future operator review of TD-016, but the register itself stays untouched per operator restriction.

## 16. Proposed commit structure (end of Phase 2o)

Four commits on `phase-2o/asymmetry-review`, after operator gate approvals (Gate 1 = this plan; Gate 2 = pre-commit review). Pytest runs before each commit and is expected at **417 passed** (no code change anywhere).

1. `phase-2o: Gate 1 plan` — this file's content.
2. `phase-2o: asymmetry review memo` — the sections-A–K narrative.
3. `phase-2o: Gate 2 review`.
4. `phase-2o: checkpoint report`.

No `data/` commits. No `src/` or `tests/` commits. No `pyproject.toml` edits. No merge yet — push and PR decision deferred to operator. No `Co-Authored-By` trailer (consistent with prior phases).

## 17. Gate 2 review format

```
Phase: 2o — Targeted Asymmetry Review / Analysis
Scope confirmed against Gate 1 plan: yes / no + diffs
Docs written: list
Memo sections A–K: present / complete / threshold-preserving check
H0 anchor preservation: enforced
R3 research-leading framing preservation: enforced
R1a+R3 promoted-but-non-leading framing preservation: enforced
ETH-specific strength NOT converted into universal recommendation: confirmed
Recommendation: primary + fallback recorded with reasoning
What-would-change-recommendation switch conditions: present
Next-phase options analysis: present (≥ 5 options)
Non-proposal list: present
Wave-1 / Phase 2l / Phase 2m / Phase 2n results preservation: confirmed
Threshold preservation: §10.3 / §10.4 / §11.3 / §11.4 / §11.6 unchanged
Safety posture: no code, no data, no APIs, no MCP, no Graphify, no TD-register edits
Operator restrictions honoured: yes
Test suite: pytest 417 passed (no code change expected)
Recommended next step: operator chooses among the Phase 2p options
Questions for operator: list or "none"
```

## 18. Checkpoint report format

Follows `.claude/rules/prometheus-phase-workflow.md` exactly. Phase 2o checkpoint includes: Phase, Goal, Summary, Files changed (all docs), Files created (all docs), Commands run (none safety-relevant — pytest + git status/diff), Installations performed (none), Configuration changed (none), Tests/checks passed (pytest 417 expected), Tests/checks failed (none expected), Known gaps (none new), Safety constraints verified (full table), Current runtime capability (research-only, unchanged), Exchange connectivity status (zero), Exchange-write capability (disabled), Recommended next step (proposal only — operator decides among Phase 2p options).

## 19. Approval gates

Two operator approvals bracket Phase 2o:

- **Gate 1 — this plan.** Approve or redirect the scope, the memo content requirements, the preservation rules, and the proposed deliverables.
- **Gate 2 — pre-commit review.** After the asymmetry-review memo + Gate 2 review are drafted, the operator reviews the diff + pytest output before any `git add` / `git commit`.

## 20. Post-approval execution sequence (docs-only)

After Gate 1 approval, proceed in this order and **stop before any `git add` / `git commit`**:

1. **Verify branch state.** Already on `phase-2o/asymmetry-review` from clean main.
2. **Write this approved Gate 1 plan** to `docs/00-meta/implementation-reports/2026-04-27_phase-2o_gate-1-plan.md` (this file).
3. **Draft the asymmetry-review memo** at `docs/00-meta/implementation-reports/2026-04-27_phase-2o_asymmetry-review-memo.md`, structured around §§ 6–9 of this plan plus the section-A–K content requirements.
4. **Draft Gate 2 review** at `docs/00-meta/implementation-reports/2026-04-27_phase-2o_gate-2-review.md` using the §17 format.
5. **Stop.** Show operator `git status`, `git diff --stat`, and `uv run pytest` output (expect 417 passed). Do **not** run `git add` / `git commit`. Await operator/ChatGPT Gate 2 review.

The Phase 2o checkpoint report (§18) is produced after Gate 2 approval, immediately before the commit sequence (§16).

**Awaiting operator/ChatGPT Gate 2 approval to commit, after the memo + Gate 2 review are drafted at the stop point.**
