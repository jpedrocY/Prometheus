# Phase 4bn-AU — Fable Independent-Review Assessment

## 1. Status and standing of the review

This is an **operator-supplied, bounded, non-binding** independent review from Fable, provided to Phase 4bn-AU by the operator. It is recorded and critiqued here against committed repository evidence. It is **not** repository authority: it may challenge reasoning but may not alter repository facts, verdicts, locks, or authorization state. **Fable authorizes nothing.** No further independent review was requested, and no external tool, source, or reviewer was accessed during this phase; the review is treated strictly as a faithful operator-supplied summary, not as a live consultation.

This assessment does not reproduce the Fable response verbatim; it records its structure compactly and compares it to the committed record.

## 2. Recorded Fable ranking and recommendation

- **Ranking:** `A > B > D > C`.
- **Primary recommendation:** **A** — local-only, strategy-independent safety/runtime infrastructure.

## 3. Recorded Fable rationale for A

- A does not depend on a market-edge claim.
- A consumes no predictive holdout, sealed reserve, disputed market data, or new hypothesis.
- A is fully distant from both stopped arcs (`STOP_LONGHORIZON_ML_ARC`, `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`).
- Fake/local failure injection and reconciliation testing can be bounded and falsifiable.
- Defects found would have direct future decision consequences.

## 4. Recorded Fable strongest objection to A

- Runtime infrastructure may become **scaffolding for a system with no viable strategy**.
- Deployment-shaped artifacts may create **sunk-cost pressure** toward paper, shadow, or live operation.

## 5. Recorded Fable clean kill criterion for A

Before implementation, the selected component must have a written, strategy-agnostic acceptance test executable entirely with fake local state. Kill the direction if satisfying that acceptance test requires any of: real or historical market data; network access; credentials; exchange-write semantics; assumptions about a particular strategy's behavior.

## 6. Recorded Fable evidence that would change its ranking

1. A repository scoping pass proves that **no** relevant safety/runtime component is genuinely missing.
2. The high-level project record **materially misstates** evidence reserves, authority hierarchy, or restart conditions.

## 7. Recorded Candidate E as raised by Fable

**E — Forward-Looking Epistemic Protocol and Evidence-Budget Governance.** Purpose as stated by Fable: codify binding rules future research arcs must satisfy before authorization; preregister hypotheses and stopping rules; explicitly account for remaining sealed evidence reserves; define who may authorize use of scarce evidence and under what conditions; decide source admissibility before a research question reaches execution; reduce recurrence of late discovery that a required source is inadmissible; remain docs-only and strategy-independent. Fable's view: **E is distinct from B** (B consolidates past state; E changes future authorization decisions) and **could contend with A for first place**.

## 8. Comparison of Fable's claims to committed repository evidence

| Fable claim | Committed-evidence check | Verdict |
|---|---|---|
| A consumes no scarce evidence and is distant from both stopped arcs | Confirmed: the runtime/safety code (`src/prometheus/state`, `persistence`, `execution/fake_adapter.py`, `operator`, `events`) reads no market data, no reserve, and is unrelated to the aggTrades ML arc or the top-of-book arc | **Correct** |
| A's premise (a component is genuinely missing) | Confirmed by repository audit: reconciliation (absent, spec'd in Phase 4e), fake-exchange divergence injection (partial), restart re-hydration (invariant enforced only in test code, not production), audit-export/redaction (absent) | **Correct; A viable** |
| Runtime infra may be scaffolding for a system with no viable strategy; deployment-shaped sunk-cost risk | Corroborated: the project is paused with two stopped arcs and no authorized strategy; the runtime is dormant and off the current critical path; behind the absolute §19 M0 boundary | **Correct and load-bearing** |
| Clean kill criterion (fake/local acceptance test; no data/network/credentials/exchange-write/strategy assumptions) | Sound; the restart-re-hydration slice satisfies it cleanly (temp SQLite + in-memory state) | **Correct; adopted in substance** |
| Evidence #1 that would lower A ("no component genuinely missing") | Not met — components *are* missing (audit §9 of the main memo) | **Not triggered; A stays viable** |
| Evidence #2 ("high-level record materially misstates reserves/authority/restart") | Partly relevant: `current-project-state.md` is genuinely stale (ends ~Phase 3k), but the reserves, authority hierarchy, and restart conditions are correctly recorded in the authoritative recent 4bn memos; the staleness is navigational, not a misstatement of reserve/authorization facts | **Partially correct; favors B/E housekeeping, not distrust of the record** |
| E is distinct from B and changes future authorization decisions | Confirmed: B would consolidate past state; E would add genuinely-absent decision-control mechanisms (ledger, named authority/quorum, late-inadmissibility rule) | **Correct** |
| E could contend with A for first place | Confirmed and, on this repository audit, E is placed *first*; A second | **Correct** |

## 9. Where Fable was correct, incomplete, or audit-dependent

- **Correct:** A's premise (a component is missing), A's strategy-independence and arc-distance, the deployment-shaped sunk-cost objection, the clean-kill criterion, and the distinctness and contention of E.
- **Incomplete / audit-dependent:** Fable ranked A first **without** the repository scoping pass that Phase 4bn-AU performed. That pass both *confirms* A's premise and *sharpens* the decisive distinction Fable did not have: the missing runtime slice is a **latent, non-current** risk (the runtime is dormant; the defect cannot manifest while paused), whereas the evidence-governance gap is a **live, next-step** risk guarding the project's scarcest irreplaceable asset. With that distinction in hand, the decisive question ("which closes the more material current project risk while preserving the strongest future ability to honestly test a strategy?") resolves to E. Fable's own uncertainty ("E could contend with A for first place") anticipated exactly this.
- **Where Fable's ranking is revised:** Phase 4bn-AU records **E > A > B > C > D**, promoting E to first and A to Fable's first-place position (second). This is a permitted, evidence-grounded departure from the non-binding review, not a rejection of it.

## 10. Does A's missing-component premise hold?

**Yes.** The audit of committed source and tests shows: no reconciliation engine (`RECOVERY_REQUIRED` is a state with no workflow; fully specified but unbuilt in the Phase 4e memo); fake-exchange divergence injection only partial (`FakeOrderOutcome.REJECTED` defined but never emitted; no partial fills/disconnect/orphaned-stop/size-mismatch); restart re-hydration enforced only in test code, not in any production function; audit-export/redaction absent. A is therefore eligible; Fable's lowering-evidence #1 is not met.

## 11. Does E's governance-gap premise hold?

**Yes, for a tightly-scoped E.** The audit confirms three genuinely-absent binding mechanisms: (1) no standing evidence-budget/scarce-reserve **ledger** (reserves re-derived ad hoc each memo); (2) no named reserve-spending **authority** or binding pre-spend independent-review/quorum (the only authority is the generic operator; reviews are advisory); (3) no **late-inadmissibility-discovery consequence** rule (governance is strong pre-execution but silent on post-reliance remediation). The surrounding substance (M0, Phase 4bn-AE preregistration, Phase 4bn-AS anti-rescue, Phase 4bn-Y split/holdout/sealed-reserve structure) already exists and is binding; an E that restated it would be duplicative and must be scoped out. E is eligible only when confined to the three holes plus a consolidated index.

## 12. Fable authorizes nothing

Recorded explicitly: the Fable review is advisory and non-binding. It authorizes no phase, no data, no model, no strategy, no acquisition, and no spending of any reserve. It may inform, but not decide; the committed repository record governs all facts, verdicts, locks, and authorization state.

## 13. Independent-review status string

`POST_AT_INDEPENDENT_REVIEW_PROVIDED__FABLE_RANKING_A_GT_B_GT_D_GT_C__CANDIDATE_E_RAISED`
