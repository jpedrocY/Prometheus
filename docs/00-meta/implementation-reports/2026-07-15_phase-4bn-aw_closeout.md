# Phase 4bn-AW — Closeout

## 1. Phase name

Phase 4bn-AW — Return-to-Strategy-Research Candidate-Family Screening and Bounded
Independent-Review Preparation.

## 2. Branch

`phase-4bn-aw/return-to-strategy-research-candidate-family-screening`.

## 3. Base SHA

`d90505a2e82c3f018cf68eeff8e7c5c1e92ee1d2` (`HEAD == main == origin/main` at branch time;
tip after the Phase 4bn-AV merge-closeout SHA-finalization commit). The only untracked item
was the transient `.claude/scheduled_tasks.lock`, which was not staged, modified, deleted,
cleaned, or committed.

## 4. Phase type

Docs-only screening and independent-review-preparation phase. Inspects committed
documentation, source, tests, and Git history read-only; creates new documentation files
only. Not a preregistration, experiment design, reserve-spend proposal, data-acquisition
proposal, model-selection, backtest, diagnostic, strategy implementation, or continuation of
either stopped arc.

## 5. Risk tier

Tier 1 / Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` — touches
scientific direction and the return-to-strategy-research question, though it mutates no
eligibility, manifest, verdict, reserve, or lock and produces a provisional non-authorizing
shortlist only.

## 6. Files added

Exactly three, all additions:

1. `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-aw_return-to-strategy-research-candidate-family-screening.md`.
2. `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-aw_bounded-fable-independent-review-brief.md`.
3. `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-aw_closeout.md` (this file).

## 7. Confirmation no existing file was modified

Confirmed. No existing file was modified, renamed, or deleted.
`git diff --name-status <base>..HEAD` shows exactly three `A` (added) entries and nothing
else. `current-project-state.md`, README, M0, the evidence-budget ledger, the scarce-reserve
spending standard, phase gates, the technical-debt register, existing process standards,
existing implementation reports, manifests, split files, sidecars, source, tests, scripts,
configs, and data are all unchanged. No process standard, evidence-ledger update, or
preregistration was created.

## 8. Committed areas inspected

Stopped-arc lineage (Phase 4bn-AK / AS / AT and the AJ/AP/AQ/AR results); project-direction
and governance (Phase 4bn-AU with its Fable assessment; Phase 4bn-AV ledger + standard);
data/admissibility capability (Phase 4bn-AB source-admissibility; Phase 4at availability
matrix; Phase 4bn-Y / 4bn-L references); the M0 twelve-clause gate with the §6 cooldown and
§7 cooled-down families; process standards; committed microstructure source constants
(manifest immutability; locked 8/16 bps; split policy; canonical paths); and Git history /
metadata. Nothing under `data/microstructure/` or `data/research/` was opened.

## 9. Candidate count

Fourteen candidate families were generated; three survived screening (CF-1, CF-2, CF-3).

## 10. Rejected / blocked count

Eleven rejected (including one merged into CF-1). Among the three survivors, CF-2 is
**blocked** on data admissibility (its tradeable form needs unacquired multi-symbol trade-
tape) and CF-3 has a blocked open-interest sub-component; both remain shortlisted in their
admissible forms.

## 11. Shortlist count

Three: CF-1, CF-2, CF-3.

## 12. Provisional first-ranked candidate

CF-1 — Microstructure realized-volatility (magnitude) forecasting. Provisional ranking:
CF-1 > CF-2 (blocked, barred from first) > CF-3. Provisional and non-authorizing.

## 13. Fable-review status

`BOUNDED_FABLE_REVIEW_BRIEF_CREATED__FABLE_NOT_YET_RUN`. Fable has not reviewed the shortlist
during Phase 4bn-AW.

## 14. Confirmation the Fable brief complies with the bounded-review standard

Confirmed. The brief begins with the literal instruction `Do not inspect the repository,
linked files, attachments, or external documents. Use only the bounded summary below.`; the
prompt body is ~849 words (≤ ~900); it requests a response under ~1,200 words; it contains
exactly one first-round decision task (rank / recommend-one-or-none / strongest self-objection
/ one kill criterion / evidence that would change the ranking / at most one genuinely-distinct
omitted family); it contains no repository link, no inspection instruction, no attachment
requirement, no full project history, and no raw logs/SHAs beyond the minimum decision facts;
it does not ask Fable to design the next phase, produce implementation steps, or perform web
research; and it includes no second-round critique request. It states the two stopped arcs,
the consumed-holdout status, the terminal and sealed reserve status, that no reserve spend is
proposed, the screening purpose, the shortlisted candidates only, each candidate's mechanism /
required data / falsification / strongest strength / strongest weakness, the provisional
ranking, and the central decision criteria.

## 15. Checks run

- Base-state verification: `git fetch origin`; `git status --short`; `git branch --show-current`;
  `git rev-parse HEAD` / `main` / `origin/main` (all `d90505a2e82c3f018cf68eeff8e7c5c1e92ee1d2`);
  `git log --oneline -10 --decorate`.
- Pre-commit validation: `git status --short`; `git diff --check`; `git diff --name-status`;
  `git diff --stat` (exactly three added files; no modifications/deletions/renames).
- Post-commit verification: `git status --short`; `git rev-parse HEAD`; `git show --stat
  --oneline HEAD`; `git diff --check <base>..HEAD`; `git diff --name-status <base>..HEAD`.
- Branch-equality verification after push: `git rev-parse HEAD` / branch / `origin/<branch>`.
- Fable prompt word count.

## 16. Tests / scripts / data / network not run

`pytest`, Ruff, mypy, and all project scripts / builders / diagnostics / models / label and
feature pipelines / backtests / replays / data and acquisition workflows were **not run** —
no executable surface changed and execution is forbidden by scope. No data was acquired or
read; no evidence reserve was opened; no network, web search, public/private API, credential,
WebSocket, MCP, Graphify, `.mcp.json`, or external reviewer (including Fable) was used.

## 17. Commit SHA (self-reference convention)

The single Phase 4bn-AW phase commit on this branch. Its literal SHA is recorded in the Phase
4bn-AW operator report (produced after commit and push). This closeout is part of that one
phase commit, so its own commit SHA cannot be embedded in itself; the operator report is the
authoritative record.

## 18. Local branch SHA

Equals the Phase 4bn-AW phase commit SHA (§17); recorded in the operator report as
`<LOCAL_BRANCH_SHA>` and confirmed equal to origin after push.

## 19. Origin branch SHA

Equals the local branch SHA (§18) after
`git push -u origin phase-4bn-aw/return-to-strategy-research-candidate-family-screening`;
recorded in the operator report as `<ORIGIN_BRANCH_SHA>` and confirmed equal.

## 20. Exact final result state

`RETURN_TO_STRATEGY_RESEARCH_CANDIDATE_FAMILIES_SCREENED__PROVISIONAL_SHORTLIST_RECORDED__BOUNDED_FABLE_INDEPENDENT_REVIEW_BRIEF_CREATED__NO_HYPOTHESIS_EXECUTION_AUTHORIZED__NO_EVIDENCE_RESERVE_SPEND_AUTHORIZED`

## 21. No-reserve-spend statement

`No evidence reserve is authorized for spending by Phase 4bn-AW.`

## 22. No-hypothesis-execution statement

`No hypothesis, strategy, model, diagnostic, backtest, data acquisition, data reading, paper, shadow, live, or exchange-write execution is authorized by Phase 4bn-AW.`

`The Phase 4bn-AW shortlist is provisional and non-authorizing.`

`Fable has not reviewed the shortlist during Phase 4bn-AW.`

## 23. Successor-authorization statement

`Any candidate selected after independent review requires a separate preregistration phase, explicit operator authorization, and a new Claude Code prompt.`

`Phase 4bn-AX or any other successor requires separate operator authorization.`

## 24. Note on merge

Merge of this phase branch into `main` requires a **separate operator prompt**. This phase does
not merge to main, does not push main, and does not create a merge-closeout file.

## 25. Preserved project locks

Unchanged: `STOP_LONGHORIZON_ML_ARC` and `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE` (distinct,
not merged, softened, reinterpreted, rescued, or reopened); Phase 4aw `flip_research_eligible(...)`
always-raising, never invoked; `research_eligible = False`; `eligibility_gate_status = PENDING`;
all published authorization flags `false`; the Phase 4bn-AE §19 M0 boundary (absolute); locked
8 bps/side · 16 bps round-trip; the Phase 4ak twelve-clause M0 gate, §6 cooldown, and §7
cooled-down families; the Phase 4bn-AV evidence ledger, spending-authority standard, and late-
inadmissibility protocol; Phase 4bb-F sidecar policy; Phase 4bn-L storage/budget policy; split
and holdout policies; dataset identities and hashes; every prior strategy verdict (H0 / R3 /
R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1 and the 5m thread); every retained-evidence
classification; and every completed implementation report.
