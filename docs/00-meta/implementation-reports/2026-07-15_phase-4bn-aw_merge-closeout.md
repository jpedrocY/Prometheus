# Phase 4bn-AW — Merge Closeout

## 1. Phase identity

Phase 4bn-AW — Return-to-Strategy-Research Candidate-Family Screening and Bounded
Independent-Review Preparation.

## 2. Phase type and merge action

Docs-only screening and independent-review-preparation phase. This document records the
review and merge of the completed Phase 4bn-AW branch into `main` via a no-fast-forward merge
commit, followed by a narrow SHA-finalization update of this same file on `main`. No
executable surface, evidence reserve, eligibility flag, manifest, verdict, or lock is touched
by the merge. The merge brings forward documentation only.

## 3. Risk tier

Tier 1 / Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` — it concerns
scientific direction and the return-to-strategy-research question, though it mutates no
eligibility, manifest, verdict, reserve, or lock and carries forward a provisional,
non-authorizing shortlist only.

## 4. Source and target branches

- Source: `phase-4bn-aw/return-to-strategy-research-candidate-family-screening`.
- Target: `main`.

## 5. Pre-merge `main` / base SHA

`d90505a2e82c3f018cf68eeff8e7c5c1e92ee1d2` (`HEAD == main == origin/main` at merge time; tip
after the Phase 4bn-AV merge-closeout SHA-finalization commit). Verified in sync before any
mutation. The only untracked item was the transient `.claude/scheduled_tasks.lock`, which was
not staged, modified, deleted, cleaned, or committed.

## 6. Original Phase 4bn-AW phase commit SHA

`1eac3812967f5a8af63b0eee7eda5f378efd12c6` — the single Phase 4bn-AW phase commit adding the
three AW documentation files (screening memo, bounded Fable brief, closeout).

## 7. Merge-closeout branch commit SHA

`caa6444d57a7178645553f9f94d68f04719a3dd3` — the commit on the AW branch that adds this
merge-closeout file (`docs(phase-4bn-aw): add merge closeout`).

## 8. Merge commit SHA

`b1abcb7362eb69a1198b356f0cba5c6de3ce3bc9` — the no-fast-forward merge commit created on
`main` (`docs(phase-4bn-aw): merge return-to-strategy candidate screening`).

## 9. SHA-finalization commit statement

SHA-finalization commit SHA:
this update (`docs(phase-4bn-aw): finalize merge closeout shas`);
its exact SHA equals the resulting final `main` / `origin/main` tip and is
recorded in the final operator report and Git log. Its own SHA is not embedded inside the
commit that creates it.

## 10. Final `main` / `origin/main` statement

After the SHA-finalization commit is pushed, final `main` and `origin/main` will both equal
the SHA-finalization commit SHA (§9). `HEAD == main == origin/main` at completion.

## 11. Merge method

`git merge --no-ff` with an explicit merge commit. No fast-forward, no squash, no rebase, no
amend, no history rewrite, no hook skipping, no signing disablement, no force push.

## 12. Files brought forward

Exactly three AW documentation files, all additions:

1. `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-aw_return-to-strategy-research-candidate-family-screening.md` — AW candidate-family screening memo.
2. `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-aw_bounded-fable-independent-review-brief.md` — AW bounded Fable independent-review brief.
3. `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-aw_closeout.md` — AW closeout.

This merge-closeout file (`2026-07-15_phase-4bn-aw_merge-closeout.md`) is added on the AW
branch before the merge, so the merged base-to-final diff carries **four** added documents in
total.

## 13. Additions-only confirmation

Confirmed additions-only. No existing file was modified, renamed, or deleted by the AW branch
or by the merge. The base-to-final diff contains only added AW documents plus one later
narrow modification of this merge-closeout file solely for SHA finalization.

## 14. Diff summary

- Pre-merge branch diff (`main..AW`): exactly the three added AW files, `754` insertions, no
  modifications / deletions / renames, no whitespace errors (`git diff --check` clean).
- Merged base-to-final diff (`d90505a2..HEAD`): four added AW documents (the three above plus
  this merge-closeout), then one later modification of this merge-closeout solely to finalize
  the exact SHAs. No source, test, script, config, data, manifest, gate, sidecar, split,
  prior report, README, current-project-state, M0, evidence-ledger, phase-gate,
  technical-debt-register, or existing-process-standard file changed.

## 15. Stopped-arc and negative-result summary

Both stopped arcs are preserved exactly, distinct, and not merged, softened, reinterpreted,
rescued, or reopened:

- `STOP_LONGHORIZON_ML_ARC` (Phase 4bn-AS) — the clean 15s directional-information result was
  economically thin (~2.47% of 15s moves clear 16 bps) and inverted at longer horizons
  (5m / 30m / 1h under a naive majority baseline). An evidence-and-methodology stop; the
  pre-v002 internal holdout is now consumed.
- `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE` (Phase 4bn-AT) — whether the 15s signal was real
  midpoint movement or bid-ask bounce could not be answered because the historical
  top-of-book quote source is inadmissible (undocumented, out-of-order, coverage unconfirmed)
  and prospective capture cannot align to the 2024 trades. A source-admissibility /
  measurability stop.

The stop reasons remain distinct (one evidence-and-methodology, one data-admissibility) and
are not merged. The prior negative-result lineage (R2 / F1 / V2 / G1 / C1; the price-only
continuation depletion; the cooled-down cross-sectional lane; the context-only D1-A verdict)
is preserved unchanged.

## 16. AW candidate-generation and screening result

Phase 4bn-AW generated fourteen candidate families from the committed microstructure/
derivatives map, classical externally-documented stylized facts, and cross-asset structure,
then filtered by (i) admissible development without acquisition or reserve spend and (ii)
genuine structural distance from both stopped arcs and every cooled-down/rejected family.
Eleven families were rejected (including one — trade-burst / activity prediction — merged into
CF-1 as the same magnitude family). Three survived into the provisional shortlist: CF-1, CF-2,
CF-3.

## 17. AW provisional shortlist and ranking

Provisional shortlist: CF-1, CF-2, CF-3. AW's provisional repository-grounded ranking:
`CF-1 > CF-2 > CF-3`, with CF-2 explicitly barred from first by its data block. The shortlist
is provisional and non-authorizing; no candidate was selected for preregistration or execution.

- `CF-1` — Microstructure realized-volatility (magnitude) forecasting.
- `CF-2` — Cross-symbol temporal lead–lag / information transmission.
- `CF-3` — Derivatives-context and settlement/session-timing volatility-regime conditioning.

## 18. CF-1 rationale

AW placed CF-1 provisional first because it is developable now on existing, non-reserve
BTCUSDT aggTrades; rests on the most robust externally-documented mechanism (volatility
clustering / long-memory in realized variance); admits a bounded comparison against a
HAR-RV / variance-persistence baseline with the cleanest predeclared kill; preserves both the
terminal and sealed reserves; and carries the highest negative-result value — a null would
materially narrow whether the current trade-tape substrate contains incremental predictable
structure.

## 19. CF-2 blocked status

CF-2 has the strongest mechanism and the only genuinely directional, tradeable decision
consequence among the survivors, but its meaningful (tradeable-granularity) form requires
multi-symbol trade-tape that is not acquired; its admissible (coarse kline) form is likely
already arbitraged. CF-2 is therefore **blocked on data availability/admissibility** and was
barred from first place. No acquisition is authorized.

## 20. CF-3 limitations

CF-3 is fully developable now in its funding-plus-fixed-UTC-calendar form (low researcher
freedom on the calendar), but it is the weakest decision consequence (a non-directional
context/regime lens with no standalone edge), its target overlaps CF-1's realized-volatility
target, and its open-interest sub-component is blocked (30-day retention). It must remain a
context/regime lens, never a directional trigger (D1-A boundary).

## 21. AW strongest counterargument

AW recorded the strongest objection to its own shortlist: repeated negatives suggest the
admissible aggTrades-only substrate most plausibly lacks an exploitable, economically
material, robust directional edge. The project trades directionally under a locked 16 bps
round-trip assumption, yet CF-1 and CF-3 are non-directional — a volatility forecast is not
itself a directional edge — and the one directionally consequential survivor, CF-2, is
blocked. The shortlist may therefore represent novelty-by-target-swap after repeated negative
results, and remaining paused (`SELECT_NONE_AND_REMAIN_PAUSED`) is a legitimate competing
outcome. AW judged the objection not fully defeated; it is the reason AW produced a provisional
shortlist for independent review rather than declaring a winner.

## 22. Bounded Fable prompt compliance

The bounded Fable review brief
(`2026-07-15_phase-4bn-aw_bounded-fable-independent-review-brief.md`) complies with the Phase
4bn-AV bounded-review standard, verified read-only during this merge review:

- It begins with the literal instruction: `Do not inspect the repository, linked files,
  attachments, or external documents. Use only the bounded summary below.`
- The prompt body is ~849 words (≤ ~900-word limit).
- It requests a response under ~1,200 words.
- It contains exactly one first-round decision task (rank the three shortlisted candidates;
  recommend one or recommend none; strongest objection to its own recommendation; one clean
  kill criterion; the evidence/reasoning that would most change the ranking; at most one
  genuinely-distinct omitted family).
- It contains no repository link, no inspection instruction, no attachment requirement, no full
  project handoff, and no external documents.
- It does not request repository inspection, implementation, next-phase design, or web
  research, and includes no second-round critique request.

## 23. Historical clarification that Fable did not run during AW

Phase 4bn-AW ended with `BOUNDED_FABLE_REVIEW_BRIEF_CREATED__FABLE_NOT_YET_RUN`. That
statement is historically correct and is preserved unchanged in the completed AW files. Fable
did not run during Phase 4bn-AW; the bounded Fable review occurred only after the AW phase
commit (`1eac3812967f5a8af63b0eee7eda5f378efd12c6`) was created and pushed. The completed AW
files are not edited to retroactively alter their historical phase status.

## 24. Post-phase Fable review standing

After Phase 4bn-AW completed and was pushed, the operator pasted only the bounded AW review
brief into a completely fresh Fable chat, with the bounded-review safeguards followed (no
repository inspection, no repository link, no attachments, no full handoff, no external
documents, no web research, one first-round decision task, bounded prompt, bounded response,
no implementation or phase-design request). The resulting Fable review is operator-supplied,
post-phase, bounded, independent from the AW execution agent, advisory, and non-binding. It is
incapable of authorizing any candidate, phase, data access, or execution, and is recorded here
only as post-phase operator-supplied independent-review input requiring later
repository-grounded adjudication. It is not represented as repository authority, and the
completed AW screening files are not modified to incorporate it.

## 25. Compact Fable ranking and recommendation

- Fable ranking: `CF-1 > CF-3 > CF-2`.
- Main change from AW: CF-2 was demoted below CF-3 because its meaningful form cannot be
  developed on currently built data; Fable held that a blocked candidate cannot outrank a
  currently developable candidate under the screening's own developability criterion.
- Fable recommendation: recommend CF-1 alone; frame CF-1 as a substrate test rather than a
  strategy bet; do not bundle CF-3; do not authorize CF-2 acquisition.
- Fable rationale for CF-1: a documented mechanism, immediate developability, reserve
  preservation, a clean stopping structure, high informational value from a null, and
  potential bounded downstream uses if successful (position sizing, cost-aware trade gating,
  execution timing — conceptual possible consequences only, not authorized capabilities, and
  not evidence that CF-1 has directional information or a profitable strategy).

## 26. Fable strongest self-objection

Fable's strongest objection to its own recommendation: CF-1 does not answer direction; a
perfect volatility forecast may contain zero directional information; success could leave the
project with no directional edge and could create momentum-by-success or rescue pressure; and
selecting none and remaining paused may be cleaner.

## 27. Fable kill-test structure

Fable's proposed kill-test structure: one predeclared horizon; one primary loss; one baseline;
one ex-ante improvement threshold; contiguous non-overlapping time blocks; improvement required
in a predeclared majority of blocks; and no post-hoc horizon, loss, threshold, or metric
switching.

## 28. Explicit non-adoption of the illustrative 3–5% threshold

Fable gave an illustrative relative QLIKE improvement margin of approximately 3–5%.
`The illustrative 3–5% QLIKE improvement margin proposed by Fable is not adopted or authorized
by the Phase 4bn-AW merge.` It was an advisory example only, has not been justified against
committed repository evidence, and is not repository policy or an authorized threshold.

## 29. Fable ranking-change considerations

Fable's principal ranking-change considerations:

1. If even strong volatility forecasts cannot identify decision-relevant windows under the
   16 bps round-trip frame, CF-1 may be decision-inert and `select none` may become preferred.
2. If admissible multi-symbol trade-tape acquisition becomes a small, bounded, reversible,
   mechanism-faithful step for a prospective lead–lag question, CF-2 could rise.
3. If external evidence already makes HAR-RV-plus-microstructure improvements expected, small,
   and low-novelty, CF-1's marginal research value would fall.

## 30. Omitted liquidation-cascade / forced-flow-asymmetry family

Fable proposed one omitted family: **Liquidation-cascade / forced-flow asymmetry using
trade-tape signatures only**. Proposed mechanism: bursts of one-sided, size-clustered
aggressor flow may represent forced liquidations; forced flow may create short-term overshoot
and partial reversion; this could form a directional, mechanism-based event-study family using
existing BTCUSDT aggTrades.

## 31. Proxy-validity, overlap, and rescue concerns for the omitted family

Fable's own caveats: no official liquidation feed is available; forced flow would be inferred
through proxies; the event definition may introduce researcher freedom; ordinary informed flow,
news response, momentum, inventory liquidation, and generic order-flow imbalance may look
similar; and any conditional drift must still clear the locked 16 bps round-trip assumption.
`The omitted liquidation-cascade / forced-flow-asymmetry family has not passed
repository-grounded overlap, proxy-validity, M0, cooled-down-family, or rescue review.` It is
not part of the AW shortlist, is not selected, and is not authorized; a later
repository-grounded overlap and admissibility audit is required before it could be considered.

## 32. Current post-Fable candidate posture

- CF-1 remains the provisional first-ranked candidate; it is not selected for preregistration
  or execution.
- CF-3 is not selected and must not be silently bundled into CF-1.
- CF-2 remains blocked; no acquisition is authorized.
- The omitted liquidation-cascade / forced-flow-asymmetry family requires a separate
  repository-grounded overlap and admissibility audit.
- `SELECT_NONE_AND_REMAIN_PAUSED` remains a live option.
- No exact CF-1 metric, horizon, baseline, block count, threshold, covariate list, or model is
  authorized. No Fable-suggested numerical threshold is binding. No downstream use such as
  sizing, gating, or execution timing is authorized.

The correct next scientific decision is not yet a CF-1 preregistration. The next possible
phase, if separately authorized, would be a docs-only final candidate-selection and
omitted-family audit phase, provisionally titled **Phase 4bn-AX — Post-Fable Candidate
Selection, CF-1 Decision-Consequence Test, and Forced-Flow-Asymmetry Overlap Audit**. This
title is provisional only; Phase 4bn-AX is not authorized by AW, by Fable, or by this merge.

## 33. Confirmation no final candidate is selected

`No final candidate family is selected for preregistration or execution by the Phase 4bn-AW
merge.`

## 34. Confirmation no reserve was opened or spent

No evidence reserve was opened, read, loaded, inspected, enumerated for content, sampled, or
scored during this merge. The v002 terminal window and v002 sealed test remain
`UNTOUCHED_RESERVED`; `PRE_V002_INTERNAL_HOLDOUT = CONSUMED` (descriptive-only) is unchanged;
`HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE` is unchanged; `test_rows_loaded = 0`
posture preserved. Nothing under `data/microstructure/` or `data/research/` was opened.

## 35. Confirmation no executable surface changed

No source, test, script, config, builder, model, diagnostic, backtest, runtime, feature, or
label surface changed. The merge and finalization carry documentation only.

## 36. Validation results

- Pre-merge: `git fetch origin`; `git status --short`; `git branch --show-current`;
  `git rev-parse main` / `origin/main` (`d90505a2…`); `git rev-parse` local/origin AW branch
  (`1eac3812…`); `git diff --check main..AW` (clean); `git diff --name-status` / `--stat`
  (three added files); `git show --stat --oneline 1eac3812`.
- Post-merge: `git status --short`; `git diff --check d90505a2..HEAD` (clean);
  `git diff --name-status` / `--stat d90505a2..HEAD` (four added documents; no
  modification/deletion/rename before finalization); `git log --oneline -8 --decorate`;
  `git rev-parse main` / `origin/main` equal to the merge commit; final equality
  `HEAD == main == origin/main` after finalization push.
- Because this is docs-only, `pytest`, Ruff, mypy, project scripts, data workflows, models,
  diagnostics, backtests, and runtime processes were **not run** — no executable surface
  changed and execution is outside merge scope.

## 37. Manifest, eligibility, M0, ledger, split, sidecar, storage, and evidence-lock preservation

Unchanged: Phase 4aw `flip_research_eligible(...)` always-raising and never invoked;
`research_eligible = False`; `eligibility_gate_status = PENDING`; all published authorization
flags `false`; the Phase 4bn-AE §19 M0 boundary (absolute); the Phase 4ak twelve-clause M0
gate with the §6 cooldown and §7 cooled-down families; the M0 cooldown and cooled-down-family
rules; the locked 8 bps/side · 16 bps round-trip assumption; dataset identities and hashes;
split and holdout policies; the Phase 4bn-AV evidence ledger; the Phase 4bn-AV
spending-authority and quorum standard; the Phase 4bn-AV late-inadmissibility protocol; Phase
4bb-F sidecar and Phase 4bn-L storage policies; all prior strategy verdicts (H0 / R3 / R1a /
R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1 and the 5m thread); all retained-evidence
classifications; and all previous implementation reports.

## 38. Exact post-merge result state

`RETURN_TO_STRATEGY_RESEARCH_CANDIDATE_FAMILY_SCREENING_MERGED_TO_MAIN__POST_PHASE_BOUNDED_FABLE_REVIEW_RECEIVED__CF1_REMAINS_PROVISIONAL_FIRST_PENDING_REPOSITORY_GROUNDED_SELECTION_DECISION__NO_HYPOTHESIS_EXECUTION_AUTHORIZED__NO_EVIDENCE_RESERVE_SPEND_AUTHORIZED`

Exact statements:

`No final candidate family is selected for preregistration or execution by the Phase 4bn-AW merge.`

`The operator-supplied post-phase Fable review is advisory and non-binding and authorizes nothing.`

`The illustrative 3–5% QLIKE improvement margin proposed by Fable is not adopted or authorized by the Phase 4bn-AW merge.`

`The omitted liquidation-cascade / forced-flow-asymmetry family has not passed repository-grounded overlap, proxy-validity, M0, cooled-down-family, or rescue review.`

`No hypothesis, strategy, model, diagnostic, backtest, data acquisition, data reading, paper, shadow, live, or exchange-write execution is authorized by the Phase 4bn-AW merge.`

`No evidence reserve is authorized for spending by the Phase 4bn-AW merge.`

`Phase 4bn-AX or any other successor requires separate operator authorization and a new Claude Code prompt.`

## 39. Required post-merge operator posture

The project remains paused with respect to execution. CF-1 is the provisional first-ranked
candidate but is not selected; CF-3 is not selected and must not be bundled; CF-2 is blocked
with no acquisition authorized; the omitted forced-flow-asymmetry family awaits a separate
repository-grounded overlap and admissibility audit; and `SELECT_NONE_AND_REMAIN_PAUSED`
remains live. Recommended next operator action: return this merge-closeout and the final
operator report to ChatGPT for review before deciding whether to authorize a docs-only Phase
4bn-AX candidate-selection and omitted-family audit phase. Any successor requires separate
operator authorization and a new Claude Code prompt. No candidate selection, preregistration,
data acquisition, or reserve spend is begun or authorized here.
