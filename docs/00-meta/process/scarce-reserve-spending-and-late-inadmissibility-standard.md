# Scarce-Reserve Spending Authority and Late-Inadmissibility Consequence Standard

**Binding governance standard for spending scarce predictive-evidence reserves and for
the consequences of discovering a source is inadmissible.**

Owner phase: Phase 4bn-AV — Evidence-Budget Ledger, Scarce-Reserve Spending Authority,
and Late-Inadmissibility Consequence Protocol (docs-only). Created 2026-07-14. Base SHA
`90c7765ba68a9b14416b79bba6f78376d94da225`.

Companion document: [`evidence-budget-ledger.md`](evidence-budget-ledger.md) (the
standing status index this standard governs changes to).

---

## 1. Purpose and scope

This standard closes exactly three governance gaps that Phase 4bn-AU confirmed are
genuinely absent from committed governance:

1. no named reserve-spending **authority** and no binding pre-spend independent-review /
   quorum precondition;
2. no binding pre-spend **sequence** protecting scarce one-shot reserves;
3. no **late-inadmissibility-discovery consequence** protocol for what happens when a
   source is found inadmissible before acquisition, after acquisition, after analysis,
   after a decision, or after downstream reliance.

It governs **only** those three gaps plus a governance index (§22). It is a docs-only
authorization **prerequisite**, not an authorization. It creates no capability and
spends no evidence.

**Out of scope (owned elsewhere; not re-legislated here):** mechanism admissibility (M0);
hypothesis preregistration and verdict contracts (Phase 4bn-AE / AP); anti-rescue and
stopped-arc decisions (Phase 4bn-AS / AT; M0.10); chronological split / holdout /
terminal / sealed-test structure (Phase 4bn-Y and committed split-policy source);
source-admissibility criteria (Phase 4bn-AB); generic phase authorization and merge
workflow (`process/phase-workflow-standard.md`, `process/merge-closeout-standard.md`);
storage budget (Phase 4bn-L). This standard references those documents; it does not
restate or amend them.

## 2. Relationship to existing governance

This standard sits **upstream** of M0 and upstream of any strategy / PnL / backtest /
paper / shadow / live / exchange-write path. It strengthens, and never relaxes, the
Phase 4bn-AE §19 M0 boundary. It adds process preconditions; it removes none. Where this
standard and a specialist document appear to conflict, the specialist document wins in
its own domain and the spend fails closed until reconciled (§21).

## 3. Authority hierarchy

Applied highest-first (identical in spirit to the project's standing hierarchy):

1. Committed repository evidence at the current base SHA.
2. Specialist documents for their own domain.
3. Recent implementation reports / closeouts / merge-closeouts for recent history,
   decisions, evidence status, and authorization boundaries.
4. Committed source and tests for actual implemented behavior.
5. Process standards under `docs/00-meta/process/`.
6. `docs/00-meta/current-project-state.md` as a stale navigational summary where
   corroborated.
7. README as non-authoritative unless corroborated.
8. Chat history, handoffs, ChatGPT, Fable, and other external opinions as secondary
   only.

**Only the human operator may authorize spending a scarce evidence reserve or opening a
successor execution phase.** Advisory reviewers may analyze, recommend, identify
conflicts, verify compliance, and provide mandatory review evidence where this standard
requires it. They may not authorize a spend.

## 4. Definitions

- **Evidence budget** — the finite set of scarce predictive-evidence reserves the
  project holds, tracked in the evidence-budget ledger. It is spent, never replenished.
- **Scarce reserve** — a specific untouched evidence resource whose value depends on
  having never been seen (the v002 terminal window; the v002 sealed test). Reading it
  consumes its independence irreversibly.
- **Consumed evidence** — evidence that has been scored / evaluated / relied upon (the
  pre-v002 internal holdout). It may be described with correct provenance but never
  represented as independent confirmation, and never restored to reserve status.
- **Terminal reserve** — an untouched out-of-time reserve that may be considered only
  after all development and model-selection choices are frozen (the v002 terminal
  window; §10.B).
- **Sealed test** — the final, highest-protection, single-use reserve, spendable only
  under the strictest sequence (the v002 sealed test; §10.C).
- **Independence** — the property that evidence has never influenced, and has never been
  influenced by, the choices being tested. It is lost on the first read and cannot be
  recovered.
- **Spend** — to read, load, inspect, enumerate for content, score, sample, or otherwise
  consume the content of a scarce reserve. Possessing the local files is not a spend;
  reading them is.
- **Proposal** — a docs-only, committed request to spend a specific reserve. A proposal
  is not a spend and not an authorization.
- **Authorization** — an explicit human-operator approval of a specific spend, valid only
  when the mandatory advisory prerequisites exist (§7). Nothing else is authorization.
- **Inadmissibility** — a determination that a source cannot answer the named question
  (e.g. inadmissible provenance, unavailable, non-regime-comparable, leaked, defective,
  or terms-restricted). Distinct sub-kinds are enumerated in §16.

## 5. Roles

- **Operator (human).** The sole final authority for authorizing a spend or opening a
  successor execution phase. Cannot be substituted by any AI or automated actor.
- **ChatGPT compliance reviewer.** Produces a repository-grounded compliance review of a
  spend proposal. Advisory only; authorizes nothing.
- **Independent critical reviewer.** A reviewer distinct from the execution agent (e.g.
  Fable or another bounded reviewer), producing one critical-review memorandum under the
  bounded-context standard (§15). Advisory only; authorizes nothing.
- **Claude Code execution agent.** May draft proposals, run docs-safe checks, and — only
  after a separate authorized execution prompt — perform the authorized spend under
  preflight. Cannot self-authorize.

## 6. Sole-authority rule

- The human operator is the **sole final spending authority**.
- Claude Code cannot self-authorize a spend.
- ChatGPT cannot self-authorize a spend.
- Fable or any other reviewer cannot self-authorize a spend.
- Possession of local files does not authorize reading them.
- A phase recommendation does not authorize execution.
- A merged proposal does not authorize execution unless the operator explicitly approves
  the spend.
- A spend authorization applies **only** to the named reserve, the named question, the
  named analysis, the named code path, and the named phase. It does not generalize.

## 7. Mandatory advisory prerequisites

Operator authorization of a spend is valid only when **both** of the following exist and
are materially complete before approval:

1. a **ChatGPT compliance recommendation** grounded in committed repository evidence;
2. one **independent critical-review memorandum** from a reviewer distinct from the
   execution agent, produced under the bounded-context standard (§15).

Advisory reviewers do not possess authorization power. If either prerequisite is
unavailable or materially incomplete, the spend **fails closed** and must not proceed.

## 8. Decision quorum

- Final authorization requires **one explicit human-operator approval**.
- That approval is valid only when both §7 advisory prerequisites exist.
- **Silence, ambiguity, partial approval, or a recommendation without explicit operator
  approval is not authorization.**
- A **dissenting** advisory review does not automatically veto the operator, but the
  operator must explicitly acknowledge the dissent and record, in a committed decision
  record, why the spend remains proportionate.
- The **sealed test** must use the strictest form of the sequence (§10.C) and **may not
  be spent in the same phase that first proposes its use** — proposal and authorization
  occur in separate phases.

Rationale: the quorum institutionalizes what the project has so far done by hand
(Phase 4bn-AS refused a scarce-reserve spend; Phase 4bn-AT caught inadmissibility before
acquisition) without pretending any AI reviewer holds authorization power. It requires
two independent advisory perspectives plus one human decision, and it fails closed if
either advisory input is missing.

## 9. Spend-proposal contract

A spend proposal is a docs-only committed document that must name, at minimum:

1. the exact reserve (by `evidence_id` from the ledger);
2. the exact question the spend will answer;
3. the mechanism under test;
4. the permitted analysis (exactly what will be computed);
5. the prohibited analysis (what will not be done after viewing);
6. the stopping rule and the single predeclared run;
7. the decision consequence (what project decision changes on each outcome);
8. the value of a negative / null result;
9. the current ledger status of the reserve (which must not be `CONSUMED` or
   `UNKNOWN_OR_AMBIGUOUS`);
10. the cost / engineering proportionality of the spend;
11. confirmation that the question was fixed **before** any reserve content is seen.

A proposal missing any element is incomplete and cannot be authorized.

## 10. Reserve-class burden

A minimal three-level protection hierarchy. Higher classes carry strictly greater
burden.

### 10.A Consumed evidence
- May be used descriptively with correct provenance.
- May **not** be represented as independent confirmation.
- Cannot return to untouched status.

### 10.B Terminal reserve (v002 terminal window)
- May be considered only after all development and model-selection choices are frozen.
- Requires the full pre-spend sequence (§12) and quorum (§8).
- One named question and one predeclared run; no tuning after viewing.

### 10.C Sealed test (v002 sealed test)
- Final and highest-protection reserve.
- May be considered only after terminal evidence supports promotion under existing gates.
- Cannot be used for exploration, debugging, threshold selection, model comparison,
  calibration, or rescue.
- Proposal and authorization must occur in **separate phases**.
- The proposal must include an explicit statement of **what project decision changes**
  after pass or fail, and an explicit **post-spend stop posture**.
- Spending it implies and creates **no** second sealed test.

No new reserve may be invented, and no existing ordinary data may be designated as sealed,
without committed evidence and a separate authorization.

## 11. Automatic refusal conditions

A spend **must be refused** (fail closed) if any of the following holds:

- rescue-shaped reuse of a stopped arc (`STOP_LONGHORIZON_ML_ARC`,
  `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`);
- unclear mechanism;
- unclear decision consequence;
- no valuable negative result;
- data / source admissibility unresolved;
- multiple reserves requested when one would suffice;
- request to use the sealed test before a terminal reserve where the terminal reserve is
  appropriate;
- request to reuse consumed evidence as independent confirmation;
- ambiguous ledger status (`UNKNOWN_OR_AMBIGUOUS`) or `CONSUMED` status;
- missing preregistration or stopping rule;
- missing cost / engineering proportionality;
- missing independent review (either §7 prerequisite absent or incomplete);
- request bundled with strategy tuning, feature search, threshold search, or post-hoc
  model comparison;
- any attempt to change the question after reserve contents are seen.

## 12. Pre-spend sequence

The minimum binding sequence, in order:

1. A docs-only spend proposal is committed (satisfying the §9 contract).
2. The proposal names the exact reserve, question, mechanism, permitted analysis,
   prohibited analysis, stopping rule, decision consequence, and negative-result value.
3. ChatGPT performs a repository-grounded compliance review.
4. A bounded independent reviewer evaluates the proposal (§15).
5. The operator explicitly approves or rejects the spend after reviewing both.
6. A separate Claude Code execution prompt is created only after approval.
7. The execution phase verifies the ledger immediately before any read (§13).
8. The ledger is updated after the spend (§14).

No step may be skipped or reordered. The sealed test adds the §10.C separate-phase
requirement.

## 13. Execution-phase preflight

Before any authorized read, the execution phase must:

- re-verify, against the committed evidence-budget ledger, that the named reserve is
  `UNTOUCHED_RESERVED` (never `CONSUMED`, `INADMISSIBLE_OR_UNAVAILABLE`, `RETIRED`, or
  `UNKNOWN_OR_AMBIGUOUS`);
- re-confirm the authorization names this exact reserve, question, analysis, code path,
  and phase;
- fail closed and stop before any read if any check does not hold.

## 14. Post-spend ledger transition

Immediately after an authorized spend (in the same phase or its immediate closeout):

- transition the reserve's ledger status (typically `UNTOUCHED_RESERVED` → `CONSUMED`);
- append a dated, cited row to the ledger transition history;
- record that the transition is irreversible (consumed cannot return to reserved).

A spend with no committed ledger transition is a governance violation.

## 15. Independent-review bounded-context standard

To prevent the observed "prompt too long" independent-review failure pattern, mandatory
independent review must:

- use a **fresh reviewer chat** for each major reserve-spend decision;
- **not** ask the reviewer to inspect the whole repository;
- **not** attach the full project handoff;
- provide a **bounded decision brief** containing only current state, reserve requested,
  question, mechanism, constraints, candidates, and decision criteria;
- include near the top the literal instruction:
  `Do not inspect the repository, linked files, attachments, or external documents. Use only the bounded summary below.`
- keep the brief compact, normally under approximately **900 words**;
- request a bounded answer, normally under approximately **1,200 words**;
- ask for **one task only** in the first round: rank / recommend, strongest objection,
  kill criterion, and the evidence that would change the ranking;
- conduct critique and phase-design work in **separate follow-up rounds**;
- **not** combine repository intake, literature review, ranking, preregistration, and
  prompt generation into one prompt.

These limits are process safeguards, not hard mathematical guarantees. If the reviewer
still reports a context-limit failure: start a fresh chat; reduce the brief; remove
repository-scanning instructions; **do not resend the failed prompt unchanged**; and
treat an incomplete review as **not satisfying** the §7 advisory prerequisite.

## 16. Late-inadmissibility stages and consequences

The consequence of discovering a source is inadmissible depends on the discovery stage.
For **every** stage: no automatic rescue; no threshold / model / source substitution in
the same phase; no claim that inadmissible evidence "still broadly confirms" the result
without a separately justified descriptive classification; no deletion of historical
audit evidence; no retroactive alteration of source files or prior reports; uncertainty
about impact **fails closed**.

### Stage 0 — Before acquisition or use
- Stop before acquisition / read.
- Record the source as `INADMISSIBLE_OR_UNAVAILABLE` for the named question in the ledger.
- No substitute source may be silently introduced.
- A new source requires a new docs-only admissibility decision.

### Stage 1 — After acquisition but before analysis
- Quarantine the source for decision use.
- Do not analyze it for the affected question.
- Preserve provenance and costs.
- Record that acquisition does not create admissibility.
- No automatic replacement or scope expansion.

### Stage 2 — After analysis but before decision / promotion
- Affected results cannot support any verdict, promotion, eligibility change, reserve
  spending, strategy selection, or execution.
- Results may be retained only as clearly labeled descriptive / non-decision evidence, and
  only if ethically and scientifically appropriate.
- Open a docs-only consequence-assessment phase.
- Stop downstream work.

### Stage 3 — After a decision but before downstream execution
- Freeze the affected decision.
- Block successor execution.
- Trace every dependent conclusion and artifact.
- Classify each dependency (§17) as unaffected, downgraded, withdrawn, or requiring
  re-evaluation.
- Do not silently edit prior reports.
- Create a new corrective decision record.

### Stage 4 — After downstream reliance or implementation
- Enter the strongest governance response.
- Halt affected research / execution pathways.
- Preserve audit history.
- Identify all downstream dependencies.
- Require operator review and a corrective phase before resumption.
- If the impact cannot be bounded, fail closed and **withdraw** the affected evidentiary
  claim.

## 17. Impact classification

When tracing dependents of an inadmissible source, classify each as exactly one of:

- `UNAFFECTED`
- `DESCRIPTIVE_ONLY`
- `DOWNGRADED`
- `WITHDRAWN`
- `RE_EVALUATION_REQUIRED`
- `UNKNOWN_IMPACT_FAIL_CLOSED`

`UNKNOWN_IMPACT_FAIL_CLOSED` is the default when impact cannot be bounded, and it triggers
withdrawal of the affected claim until resolved.

The protocol distinguishes these inadmissibility sub-kinds (technical criteria remain
owned by the specialist source-admissibility documents; this standard only names them):
source inadmissibility; data-quality defect; provenance ambiguity; terms / licensing
restriction; point-in-time leakage; regime non-comparability.

## 18. Fail-closed rules

- Ambiguous ledger status is unspendable and non-independent.
- Missing advisory prerequisite is not authorization.
- Unbounded impact is `UNKNOWN_IMPACT_FAIL_CLOSED` and triggers withdrawal.
- A ledger conflict fails closed and requires a docs-only reconciliation phase.
- When in doubt, evidence is treated as more protected, not less.

## 19. Anti-rescue and anti-substitution rules

- No spend may reopen or rescue a stopped arc.
- No inadmissible source may be silently replaced by a substitute in the same phase.
- No consumed evidence may be re-labeled as independent.
- No question may change after reserve contents are seen.
- No spend may be bundled with tuning, feature / threshold search, or post-hoc model
  comparison.

These reinforce, and never weaken, Phase 4bn-AE, Phase 4bn-AS, and M0.10.

## 20. Audit and non-retroactivity rules

- No deletion of historical audit evidence.
- No retroactive alteration of committed source files or prior reports; corrections are
  made by **new** appended records that cite what they supersede.
- Every status change and every corrective decision is a committed, dated, cited record.

## 21. Conflict-resolution rule

Where this standard and a specialist document (M0, AE, AP, AS, AT, Y, AB, split-policy
source, storage budget) appear to conflict, the specialist document wins in its own
domain, the spend or status change fails closed, and resolution requires a docs-only
reconciliation phase with explicit operator authorization. This standard never overrides
a specialist rule; it only adds preconditions.

## 22. Governance index

| Rule domain | Owner document | This standard's role |
|---|---|---|
| Mechanism admissibility | `docs/00-meta/m0-mechanism-admissibility-gate.md` (M0, twelve clauses; post-null cooldown) | Reference only; sits upstream |
| Preregistration & verdict contract | Phase 4bn-AE preregistration-contract amendment; Phase 4bn-AP contract template | Reference only |
| Anti-rescue / stopped arcs | Phase 4bn-AS (`STOP_LONGHORIZON_ML_ARC`); Phase 4bn-AT (`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`); M0.10 | Reference and reinforce |
| Split / holdout / terminal / sealed structure | Phase 4bn-Y; `pre_v002_split_policy.py`; `diagnostics_split_policy_v002.py` | Reference only; ledger indexes status, not structure |
| Source-admissibility criteria | Phase 4bn-AB; Phase 4bn-AT | Reference; names sub-kinds only |
| Phase authorization & merge workflow | `process/phase-workflow-standard.md`; `process/merge-closeout-standard.md` | Reference only |
| Storage budget | Phase 4bn-L | Reference only (disk, not evidence) |
| **Evidence ledger (status index)** | `evidence-budget-ledger.md` (**new**) | Owned here / companion |
| **Reserve-spending authority & pre-spend quorum** | this standard (**new**) | Owned here |
| **Late-inadmissibility consequence rule** | this standard (**new**) | Owned here |

The new standard fills only the three Phase 4bn-AU gaps. Specialist documents continue to
win in their domains. Conflicts fail closed. The ledger is a status index, not a
replacement for source manifests or split policy. This standard is an authorization
prerequisite, not authorization itself.

## 23. Acceptance criteria

This standard is satisfied when:

- a named sole spending authority (the operator) is recorded;
- the two mandatory advisory prerequisites and the decision quorum are defined;
- a complete spend-proposal contract is defined;
- automatic refusal conditions are enumerated;
- a three-class reserve burden hierarchy is defined;
- the pre-spend sequence, execution preflight, and post-spend ledger transition are
  defined;
- the bounded independent-review standard is defined;
- the five late-inadmissibility stages, the impact classification, and the fail-closed
  rules are defined;
- a governance index maps every rule to its owner without restating specialist content;
- the document adds enforceable mechanisms rather than duplicating M0 / AE / AS / AT / Y.

## 24. No-spend statement

**This standard authorizes no evidence spend.** It defines the process by which a future
spend may be proposed, reviewed, and — only by explicit operator approval — authorized.
It spends nothing, opens nothing, and reads no reserve.
