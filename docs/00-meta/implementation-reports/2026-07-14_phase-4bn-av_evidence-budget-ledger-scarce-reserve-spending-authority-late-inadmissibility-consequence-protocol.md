# Phase 4bn-AV — Evidence-Budget Ledger, Scarce-Reserve Spending Authority, and Late-Inadmissibility Consequence Protocol

## 1. Phase identity, branch, base SHA, phase type, risk tier

- **Phase name:** Phase 4bn-AV — Evidence-Budget Ledger, Scarce-Reserve Spending
  Authority, and Late-Inadmissibility Consequence Protocol.
- **Branch:** `phase-4bn-av/evidence-budget-ledger-scarce-reserve-spending-authority-late-inadmissibility-protocol`.
- **Base SHA:** `90c7765ba68a9b14416b79bba6f78376d94da225` (`HEAD == main == origin/main`
  at branch time; tip after the Phase 4bn-AU merge-closeout SHA-finalization commit).
- **Phase type:** Docs-only evidence-governance implementation phase. Creates new
  documentation files only; changes no data, code, model, strategy, verdict, eligibility
  state, split, manifest, or existing governance file.
- **Risk tier:** Tier 1 / Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md`
  — it governs scarce predictive evidence, reserve-spending authority, and the
  consequences of source inadmissibility, so it is treated at the highest ceremony tier
  even though it mutates no eligibility, manifest, verdict, or lock.

## 2. Exact post-AU authorization

Phase 4bn-AU is project-complete and merged (final post-AU main SHA
`90c7765ba68a9b14416b79bba6f78376d94da225`). Phase 4bn-AU selected
`RECOMMEND_FORWARD_LOOKING_EPISTEMIC_PROTOCOL_AND_EVIDENCE_BUDGET_SUCCESSOR` and proposed
Phase 4bn-AV as a docs-only governance phase. The operator explicitly authorized Phase
4bn-AV as a docs-only governance phase only: it may inspect committed documentation,
source, tests, and Git history; create new documentation files only; define the three
missing binding mechanisms selected by Phase 4bn-AU; and commit and push the dedicated
phase branch. It is not authorized to spend or inspect any reserve, open a research arc,
design or test a strategy, acquire or read market data, modify existing governance,
implement code or tests, or authorize any successor execution.

## 3. Three confirmed governance gaps

Phase 4bn-AU (§11) confirmed three genuinely-absent binding mechanisms:

1. **No standing evidence-budget / scarce-reserve ledger.** Reserves were named and
   described only ad hoc inside individual phase memos and re-derived each time; there
   was no consolidated inventory and no cumulative consumption record. (The only artifact
   literally called a "ledger" was the unrelated retained-verdict ledger.)
2. **No named reserve-spending authority or binding pre-spend independent-review /
   quorum.** The only authority was the generic operator; independent review was
   explicitly advisory and non-binding; no quorum / independent-sign-off requirement
   gated spending a one-shot reserve.
3. **No late-inadmissibility-discovery consequence rule.** Governance was strong at
   pre-execution fail-closed gating but had no protocol for what happens if a source is
   found inadmissible after a result was produced and relied upon.

## 4. Anti-duplication audit

For each proposed mechanism, the existing owner, whether it is already binding, whether
AV needs only a reference, and the exact missing mechanism AV adds:

| Proposed rule | Existing owner | Already binding? | AV needs reference only? | Exact missing mechanism AV adds |
|---|---|---|---|---|
| Mechanism admissibility | M0 gate | Yes | Yes | None (referenced) |
| Hypothesis preregistration / verdict contract | Phase 4bn-AE / AP | Yes | Yes | None (referenced) |
| Anti-rescue / stopped-arc handling | Phase 4bn-AS / AT; M0.10 | Yes | Yes | None (referenced / reinforced) |
| Chronological split / holdout / terminal / sealed structure | Phase 4bn-Y; committed split-policy source | Yes | Yes | None (referenced; ledger indexes status only) |
| Source-admissibility criteria | Phase 4bn-AB; Phase 4bn-AT | Yes | Yes | None (sub-kinds named only) |
| Generic phase authorization / merge workflow | `process/phase-workflow-standard.md`; `merge-closeout-standard.md` | Yes | Yes | None (referenced) |
| Storage budget | Phase 4bn-L | Yes | Yes | None (disk, not evidence) |
| **Standing evidence-budget ledger** | — (absent) | No | No | New consolidated reserve status index + consumption record + fail-closed status vocabulary |
| **Named reserve-spending authority + pre-spend quorum** | — (absent) | No | No | Sole-operator authority; two mandatory advisory prerequisites; binding quorum; pre-spend sequence; refusal conditions |
| **Late-inadmissibility consequence rule** | — (absent) | No | No | Five-stage consequence protocol; impact classification; corrective-record and non-retroactivity rules |

Conclusion: the three gaps are closable **without** substantively rewriting existing
governance. Each new mechanism references its neighbors rather than restating them. The
kill condition `STOP_AV_DUPLICATIVE_GOVERNANCE_NO_MATERIAL_NEW_MECHANISM` was **not**
triggered.

## 5. Existing documents inspected

Committed, read-only:

- Phase 4bn-AU: post-AT direction memo, Fable independent-review assessment, closeout,
  merge-closeout.
- Phase 4bn-Y chronological-split / holdout policy memo (exact split geometry, sealed-test
  window, seven prohibited uses, `test_rows_loaded = 0`, v002 terminal scope).
- Phase 4bn-AT top-of-book mechanism-admissibility memo (historical retrospective source
  status; `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`).
- Phase 4bn-AR fixed long-horizon baseline run verdict (internal-holdout consumption).
- Core governance / process: `m0-mechanism-admissibility-gate.md`; `decision-framework.md`
  (via prior memos); process standards under `docs/00-meta/process/`
  (`phase-workflow-standard.md`, `phase-risk-tiering-standard.md`,
  `merge-closeout-standard.md`, `operator-report-standard.md`,
  `phase-prompt-template.md`).
- Referenced (as owners in the index; grounded through the AU/AT/Y/AR memos above):
  Phase 4bn-AE preregistration-contract amendment; Phase 4bn-AB source-admissibility
  memo; Phase 4bn-AP contract template; Phase 4bn-L storage/budget memo; Phase 4bn-AA
  split-policy artefact; `docs/12-roadmap/phase-gates.md`;
  `docs/12-roadmap/technical-debt-register.md`.

No file under `data/microstructure/` or `data/research/` was opened. No source, test,
script, config, or prior report was modified. No script, test, builder, diagnostic,
model, backtest, or runtime process was executed. No network or external source was used.

## 6. New files created

Exactly four additions; no existing file modified:

1. `docs/00-meta/process/evidence-budget-ledger.md` — the standing evidence-budget ledger.
2. `docs/00-meta/process/scarce-reserve-spending-and-late-inadmissibility-standard.md` —
   the binding governance standard (spending authority + quorum + late-inadmissibility
   protocol + governance index).
3. `docs/00-meta/implementation-reports/2026-07-14_phase-4bn-av_evidence-budget-ledger-scarce-reserve-spending-authority-late-inadmissibility-consequence-protocol.md` —
   this implementation report.
4. `docs/00-meta/implementation-reports/2026-07-14_phase-4bn-av_closeout.md` — the phase
   closeout.

## 7. Evidence-ledger design

The ledger is a status index usable **without** reading any underlying evidence. It
defines a minimal finite status vocabulary — `UNTOUCHED_RESERVED`, `CONSUMED`,
`INADMISSIBLE_OR_UNAVAILABLE`, `RETIRED`, `UNKNOWN_OR_AMBIGUOUS` — where
`UNKNOWN_OR_AMBIGUOUS` **fails closed** (cannot support independence, cannot be spent,
cannot support promotion, requires operator review). Each entry carries the required
fields (`evidence_id`, name, family/split/category, exact scope from committed metadata,
status, independence, permitted use, prohibited use, authority to change status, last
authoritative phase/report, last status-change date, notes). It defines update rules
(same-branch update; no silent transition; consumed is terminal; citations required;
derived from committed evidence only), a conflict / fail-closed rule (ledger conflicts
fail closed and require a docs-only reconciliation phase), an append-only transition
history, required fields for future entries, and explicit evidence-source and no-open
statements.

## 8. Initial ledger state and provenance

Recorded from committed metadata without opening any evidence:

- **Pre-v002 internal holdout** (`PRE_V002_INTERNAL_HOLDOUT`): 2024-11-17 .. 2024-11-30
  (14 dates); status **`CONSUMED`** (scored under Phase 4bn-AR; arc stopped at Phase
  4bn-AS). Not reusable as independent confirmation; cannot return to reserved.
- **v002 terminal window** (`V002_TERMINAL_WINDOW`): 2024-12-01 .. 2025-02-28 (90 dates;
  155,153,449 rows, by reference only); status **`UNTOUCHED_RESERVED`**; permitted use
  only after the terminal-reserve pre-spend sequence is satisfied.
- **v002 sealed test** (`V002_SEALED_TEST`): 2025-02-14 .. 2025-02-28 (15 dates;
  `test_rows_loaded = 0`); status **`UNTOUCHED_RESERVED`**, highest protection; permitted
  use only under the strictest sequence, with proposal and authorization in separate
  phases.
- **Historical retrospective top-of-book source** (`HIST_TOB_BOOKTICKER_SOURCE`): status
  **`INADMISSIBLE_OR_UNAVAILABLE`** for the 2024 mechanism question (Phase 4bn-AT). Not a
  reserve; not spendable; prospective collection does not retroactively answer the
  historical question.

Provenance: Phase 4bn-Y (split geometry / reserves), Phase 4bn-AR (holdout consumption),
Phase 4bn-AS (stop), Phase 4bn-AT (source status), Phase 4bn-AU (restated status). No row
count, date, hash, or content was invented; all quantitative values are carried forward
verbatim from committed reports.

## 9. Spending-authority design

The operator is the **sole final spending authority**. The standard distinguishes
proposal, compliance review, independent critical review, operator authorization,
execution prompt, actual spend, and ledger update. The minimum binding sequence is:
docs-only proposal → repository-grounded ChatGPT compliance review → bounded independent
critical review → explicit operator approval → separate Claude Code execution prompt →
execution-phase ledger preflight → post-spend ledger update. Claude Code, ChatGPT, and
Fable cannot self-authorize; possession of files does not authorize reading them; a
recommendation or a merged proposal is not authorization; an authorization binds only the
named reserve, question, analysis, code path, and phase. A complete refusal-conditions
list is enumerated (rescue-shaped reuse, unclear mechanism / consequence, no negative-
result value, unresolved admissibility, multiple reserves when one suffices, sealed
before terminal, consumed-as-independent, ambiguous status, missing preregistration /
proportionality / independent review, bundling with tuning / search / post-hoc
comparison, changing the question after seeing contents).

## 10. Decision-quorum rationale

Final authorization requires one explicit human-operator approval, valid only when both
mandatory advisory prerequisites exist: (1) a ChatGPT compliance recommendation grounded
in committed repository evidence, and (2) one independent critical-review memorandum from
a reviewer distinct from the execution agent. Advisory reviewers hold no authorization
power. Silence, ambiguity, partial approval, or a recommendation without explicit
operator approval is not authorization. If either advisory prerequisite is unavailable or
materially incomplete, spending fails closed. A dissenting review does not automatically
veto the operator, but the operator must explicitly acknowledge the dissent and record
why the spend remains proportionate. The sealed test uses the strictest form and may not
be spent in the phase that first proposes it. This institutionalizes the twice-repeated
hand-rolled diligence (Phase 4bn-AS refusing a spend; Phase 4bn-AT catching
inadmissibility) without granting any AI reviewer authorization power.

## 11. Bounded independent-review standard

To prevent the "prompt too long" failure pattern: fresh reviewer chat per major decision;
no whole-repository inspection; no full-handoff attachment; a bounded decision brief
(current state, reserve, question, mechanism, constraints, candidates, criteria) with the
literal instruction `Do not inspect the repository, linked files, attachments, or external
documents. Use only the bounded summary below.`; brief normally under ~900 words; answer
normally under ~1,200 words; one first-round task (rank/recommend, strongest objection,
kill criterion, evidence that would change the ranking); critique and phase-design in
separate rounds. These are process safeguards, not guarantees; on a context-limit
failure, start fresh, reduce the brief, remove repo-scanning instructions, never resend
the failed prompt unchanged, and treat an incomplete review as not satisfying the
advisory prerequisite.

## 12. Reserve-class hierarchy

Three classes of strictly increasing burden: **consumed evidence** (descriptive with
provenance; never independent confirmation; never restored); **terminal reserve** (only
after all development / model-selection choices frozen; full sequence + quorum; one
named question, one predeclared run, no tuning after viewing); **sealed test** (final,
highest protection; only after terminal evidence supports promotion under existing gates;
no exploration / debugging / threshold selection / model comparison / calibration /
rescue; proposal and authorization in separate phases; explicit statement of the decision
that changes on pass/fail; explicit post-spend stop posture; creates no second sealed
test). No new reserve may be invented and no ordinary data designated as sealed without
committed evidence and separate authorization.

## 13. Late-inadmissibility stage model

Five discovery stages, each with defined consequences: **Stage 0** (before acquisition /
use) — stop, record inadmissible, no silent substitute, new source needs a new
admissibility decision; **Stage 1** (after acquisition, before analysis) — quarantine,
preserve provenance/costs, acquisition creates no admissibility, no automatic
replacement; **Stage 2** (after analysis, before decision) — affected results cannot
support any verdict/promotion/eligibility/spend/strategy/execution, retain only as
labeled descriptive evidence, open a docs-only consequence-assessment phase, stop
downstream; **Stage 3** (after decision, before execution) — freeze decision, block
successor, trace and classify every dependent, no silent report edits, new corrective
record; **Stage 4** (after downstream reliance / implementation) — strongest response,
halt affected pathways, preserve audit history, identify dependencies, require operator
review and a corrective phase, and if impact is unbounded, fail closed and withdraw the
claim. For every stage: no automatic rescue; no same-phase substitution; no
"still broadly confirms" without a separately justified descriptive classification; no
deletion of audit evidence; no retroactive alteration; uncertainty fails closed.

## 14. Impact-classification model

Each dependent of an inadmissible source is classified as exactly one of `UNAFFECTED`,
`DESCRIPTIVE_ONLY`, `DOWNGRADED`, `WITHDRAWN`, `RE_EVALUATION_REQUIRED`, or
`UNKNOWN_IMPACT_FAIL_CLOSED` (the default when impact cannot be bounded, triggering
withdrawal). The protocol distinguishes inadmissibility sub-kinds (source
inadmissibility, data-quality defect, provenance ambiguity, terms / licensing
restriction, point-in-time leakage, regime non-comparability) while leaving the technical
criteria to the specialist source-admissibility documents.

## 15. Fail-closed behavior

Ambiguous ledger status is unspendable and non-independent; a missing advisory
prerequisite is not authorization; unbounded impact is `UNKNOWN_IMPACT_FAIL_CLOSED` and
triggers withdrawal; a ledger conflict fails closed and requires a docs-only
reconciliation phase; when in doubt, evidence is treated as more protected, not less.

## 16. Anti-rescue and anti-substitution protections

No spend may reopen or rescue a stopped arc; no inadmissible source may be silently
replaced in the same phase; no consumed evidence may be re-labeled as independent; no
question may change after reserve contents are seen; no spend may be bundled with tuning,
feature / threshold search, or post-hoc model comparison. These reinforce and never
weaken Phase 4bn-AE, Phase 4bn-AS, and M0.10.

## 17. Governance index

The standard's §22 maps every rule domain to its owner: M0 (mechanism admissibility),
Phase 4bn-AE / AP (preregistration / verdict), Phase 4bn-AS / AT and M0.10 (anti-rescue /
stopped arcs), Phase 4bn-Y and split-policy source (split / holdout / terminal / sealed
structure), Phase 4bn-AB / AT (source admissibility), the phase-workflow and
merge-closeout standards (authorization / merge), Phase 4bn-L (storage budget), and the
two new AV documents (evidence ledger; reserve-spending authority + late-inadmissibility
rule). Specialist documents win in their domains; conflicts fail closed; the ledger is a
status index, not a replacement for source manifests or split policy; the standard is an
authorization prerequisite, not authorization itself.

## 18. Confirmation no existing governance was modified

Confirmed. No existing file was modified, renamed, or deleted. `current-project-state.md`,
README, M0, phase gates, technical-debt register, existing process standards, existing
implementation reports, manifests, split files, sidecars, source, tests, scripts,
configs, and data are all unchanged. `git diff --name-status <base>..HEAD` shows exactly
four `A` (added) entries and nothing else.

## 19. Confirmation no evidence was read or spent

Confirmed. No evidence reserve was opened. The pre-v002 internal holdout remains consumed;
the v002 terminal window and v002 sealed test remain scarce untouched reserves, not read,
loaded, inspected, enumerated for content, scored, sampled, or consumed. Nothing under
`data/microstructure/` or `data/research/` was opened. The `test_rows_loaded = 0` posture
is preserved.

## 20. Confirmation no research, data, code, tests, scripts, models, or runtime work occurred

Confirmed. No research arc was opened; no strategy, hypothesis, model, feature, label, or
data source was designed or tested; no data was acquired or read; no code, test, config,
schema, manifest, or data file was created; no project script, test, builder, diagnostic,
model, backtest, replay, paper, shadow, live, or runtime process was executed; no network,
public / private API, credential, WebSocket, MCP, Graphify, or `.mcp.json` was used. Only
`git`, local document reads, and repository text search were used.

## 21. Kill-criterion assessment

None of the kill criteria triggered:

- closing the gaps did **not** require modifying existing governance (references only);
- the standard does **not** merely restate M0 / AE / AS / Y / phase-workflow rules (the
  anti-duplication audit in §4 shows three net-new mechanisms);
- the ledger was populated **without** reading underlying evidence (committed metadata
  only);
- defining authority did **not** require granting authorization power to an AI agent (the
  operator is the sole authority; reviewers are advisory);
- the protocol required **no** new strategy, hypothesis, model, feature, label, or data
  source;
- the protocol required **no** acquisition, network access, credentials, or code;
- the work did **not** expand into an unbounded governance rewrite (exactly four files;
  bounded scope);
- current reserve status **was** establishable from committed records;
- the required file paths did **not** conflict with repository structure (all four target
  paths were free);
- **no** unexpected working-tree change existed at branch time (only the transient lock).

## 22. Strongest counterargument

The strongest case against this phase: the project may already have enough surrounding
governance (M0, Phase 4bn-AE preregistration, Phase 4bn-AS anti-rescue, Phase 4bn-Y
split/holdout/sealed structure), which "worked twice" in practice (Phase 4bn-AS refused a
scarce-reserve spend; Phase 4bn-AT caught inadmissibility before acquisition), so AV may
be preventive paperwork that produces no new capability and no new knowledge while the
project is paused — substituting motion for progress.

## 23. Why the final scope adds enforceable mechanisms rather than duplicating prior rules

The counterargument does not prevail because the twice-repeated successes were
**hand-rolled each time**; nothing in committed governance guaranteed they would recur.
AV converts three ad-hoc practices into standing, enforceable mechanisms: a consolidated
reserve **ledger** with a fail-closed status vocabulary and an append-only consumption
record (previously re-derived per memo); a named **spending authority** with a binding
two-input advisory quorum and a pre-spend sequence (previously only a generic operator
with non-binding advice); and a **late-inadmissibility consequence protocol** with staged
consequences and impact classification (previously entirely absent — governance was
strong pre-execution but silent on post-reliance remediation). These guard the project's
scarcest irreplaceable asset (the last unseen v002 terminal + sealed test) at the very
next research step, and each references rather than restates its neighbors (§4), so the
scope is additive, not duplicative.

## 24. Exact no-spend statement

`No evidence reserve is authorized for spending by Phase 4bn-AV.`

`No strategy, research execution, data acquisition, model, diagnostic, backtest, paper, shadow, live, or exchange-write capability is authorized by Phase 4bn-AV.`

## 25. Exact no-successor statement

`Any future reserve-spend proposal requires a separate docs-only proposal, repository-grounded ChatGPT compliance review, bounded independent critical review, explicit operator approval, and a separate Claude Code execution prompt.`

`Phase 4bn-AW or any other successor requires separate operator authorization.`

## 26. Recommended next operator action

Return the four Phase 4bn-AV files and the operator report to ChatGPT for compliance
review, plain-language interpretation, and a separate merge decision. Do not authorize a
reserve spend, a successor phase, or a Phase 4bn-AW prompt until a separate operator
prompt does so explicitly. The project remains paused with respect to execution.

## 27. Exact final result state

`EVIDENCE_BUDGET_LEDGER_CREATED__SCARCE_RESERVE_SPENDING_AUTHORITY_AND_PRE_SPEND_REVIEW_QUORUM_RECORDED__LATE_INADMISSIBILITY_CONSEQUENCE_PROTOCOL_RECORDED__NO_EVIDENCE_RESERVE_SPEND_AUTHORIZED__NO_SUCCESSOR_EXECUTION_AUTHORIZED`

## 28. Preserved project locks

Unchanged: `STOP_LONGHORIZON_ML_ARC`; `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE` (distinct,
not rewritten, merged, softened, or reopened); Phase 4aw `flip_research_eligible(...)`
always-raising, never invoked or weakened; `research_eligible = False`;
`eligibility_gate_status = PENDING`; all published authorization flags `false`; the Phase
4bn-AE §19 M0 boundary (absolute); locked 8 bps/side · 16 bps round-trip; Phase 4bb-F
sidecar policy; Phase 4bn-L storage/budget policy; split policies; dataset identities and
hashes; all completed strategy verdicts and retained-evidence classifications; all prior
reports.
