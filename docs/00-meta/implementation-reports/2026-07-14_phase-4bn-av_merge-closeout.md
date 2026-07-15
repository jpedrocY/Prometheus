# Phase 4bn-AV — Merge-Closeout

## 1. Phase identity

Phase 4bn-AV — Evidence-Budget Ledger, Scarce-Reserve Spending Authority, and
Late-Inadmissibility Consequence Protocol.
Source branch: `phase-4bn-av/evidence-budget-ledger-scarce-reserve-spending-authority-late-inadmissibility-protocol`.
Target branch: `main`.

## 2. Phase type and merge action

Docs-only evidence-governance implementation phase. Merge-only review and closeout: no
source, test, script, config, data, manifest, gate, sidecar, split, or model change; no
data acquisition / read; no model, diagnostic, builder, backtest, replay, or runtime
process. The merge brings five documentation files onto `main` via a `--no-ff` merge
commit; documentation only.

## 3. Risk tier

Tier 1 / Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` — governs
scarce predictive evidence, reserve-spending authority, and source-inadmissibility
consequences, though it mutates no eligibility, manifest, verdict, or lock.

## 4. Source and target branches

- Source: `phase-4bn-av/evidence-budget-ledger-scarce-reserve-spending-authority-late-inadmissibility-protocol`.
- Target: `main`.

## 5. Pre-merge main / base SHA

`90c7765ba68a9b14416b79bba6f78376d94da225` (main == origin/main at merge start; tip after
the Phase 4bn-AU merge-closeout SHA-finalization commit).

## 6. Original AV phase commit SHA

`9909926b991a91da47b9d635f74527fb550003a2` (the single Phase 4bn-AV phase commit that
added the four AV documents).

## 7. Merge-closeout branch commit SHA

`670ab497f287aeb6a54446e713b5fe824b65951c` (this merge-closeout's own commit on the AV
branch, `docs(phase-4bn-av): add merge closeout`).

## 8. Merge commit SHA

`578709009b5738f55c93d71091f69decaf87766f` (the `--no-ff` merge of the AV branch into
`main`).

## 9. SHA-finalization commit statement

The placeholders in §7 and §8 are replaced on `main` by a narrow SHA-finalization update
to this file, committed as `docs(phase-4bn-av): finalize merge closeout shas`. Its exact
SHA equals the resulting final `main` / `origin/main` tip and is recorded in the final
operator report and Git log. The finalization commit's own SHA is not embedded inside the
commit that creates it.

## 10. Final main / origin/main statement

After the SHA-finalization commit is pushed, `main == origin/main` equals that
SHA-finalization commit. Both SHAs are recorded and confirmed equal in the Phase 4bn-AV
final operator report after `git push origin main`.

## 11. Merge method

`git merge --no-ff` of the AV branch into `main`, message
`docs(phase-4bn-av): merge evidence-budget and inadmissibility governance`. No squash, no
rebase, no amend, no fast-forward, no hook-skipping, no signing-disable, no force push.
`.claude/scheduled_tasks.lock` and any local generated artefact excluded.

## 12. Files brought forward

Five documentation files:

1. `docs/00-meta/process/evidence-budget-ledger.md` (standing evidence-budget ledger).
2. `docs/00-meta/process/scarce-reserve-spending-and-late-inadmissibility-standard.md`
   (binding governance standard: spending authority + quorum + late-inadmissibility
   protocol + governance index).
3. `docs/00-meta/implementation-reports/2026-07-14_phase-4bn-av_evidence-budget-ledger-scarce-reserve-spending-authority-late-inadmissibility-consequence-protocol.md`
   (AV implementation report).
4. `docs/00-meta/implementation-reports/2026-07-14_phase-4bn-av_closeout.md` (AV closeout).
5. `docs/00-meta/implementation-reports/2026-07-14_phase-4bn-av_merge-closeout.md` (this
   merge-closeout).

## 13. Additions-only confirmation

`git diff --name-status main..<AV branch>` shows exactly four additions (the ledger, the
standard, the implementation report, and the closeout) with no modifications, deletions,
or renames; this merge-closeout is a fifth addition committed on the AV branch before
merge. No existing file was modified, renamed, or deleted. No `data/microstructure/` or
`data/research/` path is tracked or committed. `.claude/scheduled_tasks.lock` is not
staged.

## 14. Diff summary

- Pre-merge (`main..<AV branch>`, before this merge-closeout): 4 files changed, 1202
  insertions(+); `git diff --check` clean.
- Post-merge (`<base>..HEAD`, after this merge-closeout is included): five added documents;
  no modification / deletion / rename beyond the single later SHA-finalization edit of this
  merge-closeout.

## 15. Anti-duplication conclusion

The three Phase 4bn-AU gaps (standing evidence-budget ledger; named reserve-spending
authority + pre-spend quorum; late-inadmissibility consequence rule) are genuinely absent
and were closed **without** rewriting existing governance. Each new mechanism references
its neighbors (M0, Phase 4bn-AE / AP, Phase 4bn-AS / AT, Phase 4bn-Y, Phase 4bn-AB,
Phase 4bn-L, phase-workflow / merge-closeout standards) rather than restating them.
`STOP_AV_DUPLICATIVE_GOVERNANCE_NO_MATERIAL_NEW_MECHANISM` was not triggered.

## 16. Initial ledger entries and statuses

Populated from committed metadata only; no underlying evidence was opened:

- `PRE_V002_INTERNAL_HOLDOUT` — 2024-11-17 .. 2024-11-30 (14 dates) — **`CONSUMED`**; not
  reusable as independent confirmation; cannot return to reserved.
- `V002_TERMINAL_WINDOW` — 2024-12-01 .. 2025-02-28 (90 dates; 155,153,449 rows by
  reference) — **`UNTOUCHED_RESERVED`**.
- `V002_SEALED_TEST` — 2025-02-14 .. 2025-02-28 (15 dates; `test_rows_loaded = 0`) —
  **`UNTOUCHED_RESERVED`**, highest-protection reserve.
- `HIST_TOB_BOOKTICKER_SOURCE` — **`INADMISSIBLE_OR_UNAVAILABLE`** for the 2024
  top-of-book mechanism question; not a spendable reserve; prospective collection does not
  retroactively answer the historical question.

## 17. Spending authority and advisory quorum

The human operator is the **sole final reserve-spending authority**. Claude Code, ChatGPT,
Fable, or any other AI / reviewer cannot self-authorize evidence access; possession of
files does not authorize reading them; a merged proposal or recommendation does not
authorize spending. Before any future reserve-spend authorization, both advisory
prerequisites must exist: (1) a repository-grounded ChatGPT compliance recommendation, and
(2) one bounded independent critical-review memorandum from a reviewer distinct from the
execution agent. Final authorization requires one explicit operator approval after both
advisory prerequisites exist. Silence, ambiguity, partial approval, incomplete review, or
a recommendation without explicit approval is not authorization. A dissenting independent
review does not automatically veto the operator, but the dissent must be explicitly
acknowledged and the proportionality rationale recorded. AI reviewers hold no
authorization power.

## 18. Bounded independent-review limits

Fresh reviewer chat per major decision; no whole-repository inspection; no full project
handoff pasted into the independent-review prompt; bounded summary only; the literal
instruction `Do not inspect the repository, linked files, attachments, or external
documents. Use only the bounded summary below.`; review brief normally ≤ ~900 words;
reviewer answer normally ≤ ~1,200 words; first round limited to one decision task; critique
and phase design in separate later rounds; an incomplete or context-limit-failed review
does not satisfy the advisory prerequisite; after failure, start a fresh reviewer chat and
reduce the prompt rather than resending the failed long prompt unchanged.

## 19. Reserve-class hierarchy

Three classes of strictly increasing burden: **consumed evidence** (descriptive with
provenance; never independent confirmation; never restored); **terminal reserve** (only
after all development / model-selection choices frozen; full pre-spend sequence + quorum;
one named question, one predeclared run, no tuning after viewing); **sealed test** (final,
highest protection; only after terminal evidence supports promotion under existing gates;
no exploration / debugging / threshold selection / model comparison / calibration /
rescue; proposal and authorization in separate phases; explicit statement of the decision
that changes on pass/fail and an explicit post-spend stop posture; creates no second
sealed test).

## 20. Late-inadmissibility five-stage model

- **Stage 0** — discovered before acquisition / use: stop; record inadmissible; no silent
  substitute; a new source requires a new docs-only admissibility decision.
- **Stage 1** — after acquisition, before analysis: quarantine; preserve provenance /
  costs; acquisition creates no admissibility; no automatic replacement or scope
  expansion.
- **Stage 2** — after analysis, before decision: affected results cannot support any
  verdict / promotion / eligibility / spend / strategy / execution; retain only as labeled
  descriptive evidence; open a docs-only consequence-assessment phase; stop downstream.
- **Stage 3** — after decision, before execution: freeze the decision; block successor;
  trace and classify every dependent; no silent report edits; new corrective record.
- **Stage 4** — after downstream reliance / implementation: strongest response; halt
  affected pathways; preserve audit history; identify dependencies; require operator review
  and a corrective phase; if impact is unbounded, fail closed and withdraw the claim.

## 21. Impact-classification model

Each dependent is classified as exactly one of `UNAFFECTED`, `DESCRIPTIVE_ONLY`,
`DOWNGRADED`, `WITHDRAWN`, `RE_EVALUATION_REQUIRED`, or `UNKNOWN_IMPACT_FAIL_CLOSED` (the
default when impact cannot be bounded, triggering withdrawal). Inadmissibility sub-kinds
named (technical criteria owned by specialist documents): source inadmissibility,
data-quality defect, provenance ambiguity, terms / licensing restriction, point-in-time
leakage, regime non-comparability.

## 22. Fail-closed rules

Ambiguous ledger status is unspendable and non-independent; a missing advisory
prerequisite is not authorization; unbounded impact is `UNKNOWN_IMPACT_FAIL_CLOSED` and
triggers withdrawal; a ledger conflict fails closed and requires a docs-only reconciliation
phase; no automatic rescue; no silent substitution; no same-phase replacement of an
inadmissible source; no deletion of audit history; no retroactive alteration of historical
reports; no claim that a result "still broadly confirms" a conclusion without a separately
justified descriptive classification; when in doubt, evidence is treated as more protected,
not less.

## 23. Strongest counterargument

The project may already have enough surrounding governance (M0, Phase 4bn-AE
preregistration, Phase 4bn-AS anti-rescue, Phase 4bn-Y split / holdout / sealed structure),
which "worked twice" in practice (Phase 4bn-AS refused a scarce-reserve spend; Phase
4bn-AT caught inadmissibility before acquisition), so Phase 4bn-AV may be preventive
paperwork that produces no new capability and no new knowledge while the project is paused
— substituting motion for progress.

## 24. Why the phase adds new enforceable mechanisms

The twice-repeated successes were hand-rolled each time; nothing in committed governance
guaranteed they would recur. Phase 4bn-AV converts three ad-hoc practices into standing,
enforceable mechanisms: a consolidated reserve **ledger** with a fail-closed status
vocabulary and an append-only consumption record (previously re-derived per memo); a named
**spending authority** with a binding two-input advisory quorum and a pre-spend sequence
(previously only a generic operator with non-binding advice); and a **late-inadmissibility
consequence protocol** with staged consequences and impact classification (previously
entirely absent — governance was strong pre-execution but silent on post-reliance
remediation). These guard the project's scarcest irreplaceable asset (the last unseen v002
terminal + sealed test) at the very next research step, and each references rather than
restates its neighbors, so the scope is additive, not duplicative.

## 25. Confirmation no reserve was opened or spent

Confirmed. No evidence reserve was opened, read, loaded, inspected, enumerated for content,
scored, sampled, or consumed by Phase 4bn-AV or by this merge. The pre-v002 internal
holdout remains consumed; the v002 terminal window and v002 sealed test remain scarce
untouched reserves. Nothing under `data/microstructure/` or `data/research/` was opened.
The `test_rows_loaded = 0` posture is preserved.

## 26. Confirmation no executable surface changed

Confirmed. No source, test, script, config, manifest, gate, sidecar, split, dataset, or
model configuration was modified. Only documentation files were added under
`docs/00-meta/process/` and `docs/00-meta/implementation-reports/`.

## 27. Validation results

- `git status --short` → only `?? .claude/scheduled_tasks.lock`.
- `git diff --check main..<AV branch>` → clean.
- `git diff --name-status main..<AV branch>` → four additions only; no
  modification / deletion / rename.
- `git diff --stat main..<AV branch>` → 4 files changed, 1202 insertions(+).
- `git show --stat --oneline 9909926b991a91da47b9d635f74527fb550003a2` → the four AV
  documents, 1202 insertions.
- Post-merge: `git diff --name-status 90c7765ba68a9b14416b79bba6f78376d94da225..HEAD` →
  five added documents; `git diff --check` → clean.
- `pytest`, Ruff, mypy, project scripts, data workflows, models, diagnostics, backtests,
  and runtime processes were **not run** because no executable surface changed and
  execution is outside merge scope.

## 28. Manifest, eligibility, M0, split, sidecar, storage, and evidence-lock preservation

Preserved unchanged: manifest immutability (`flip_research_eligible(...)` always-raises,
never invoked; `research_eligible = False`; `eligibility_gate_status = PENDING`); all
published authorization flags `false`; the Phase 4bn-AE §19 M0 boundary (absolute); locked
cost assumptions (8 bps/side · 16 bps round-trip); dataset identities and hashes; split and
holdout policies; Phase 4bb-F sidecar policy and Phase 4bn-L storage/budget policy;
`STOP_LONGHORIZON_ML_ARC` and `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE` (distinct, not
rewritten, merged, softened, or reopened); all prior strategy verdicts (H0 / R3 / R1a /
R1b-narrow / R2 / F1 / D1-A; 5m / V2 / G1 / C1) and retained-evidence classifications; all
previous implementation reports.

## 29. Exact post-merge result state

`EVIDENCE_BUDGET_LEDGER_AND_SCARCE_RESERVE_SPENDING_STANDARD_MERGED_TO_MAIN__LATE_INADMISSIBILITY_CONSEQUENCE_PROTOCOL_MERGED_TO_MAIN__NO_EVIDENCE_RESERVE_SPEND_AUTHORIZED__NO_SUCCESSOR_EXECUTION_AUTHORIZED`

## 30. Required post-merge operator posture

Remain paused with respect to execution. Return this merge-closeout and the final operator
report to ChatGPT for review before deciding whether to authorize any Phase 4bn-AW or
reserve-spend proposal.

`No evidence reserve is authorized for spending by the Phase 4bn-AV merge.`

`No strategy, research execution, data acquisition, model, diagnostic, backtest, paper, shadow, live, or exchange-write capability is authorized by the Phase 4bn-AV merge.`

`Any future reserve-spend proposal requires a separate docs-only proposal, repository-grounded ChatGPT compliance review, bounded independent critical review, explicit operator approval, and a separate Claude Code execution prompt.`

`Phase 4bn-AW or any other successor requires separate operator authorization.`
