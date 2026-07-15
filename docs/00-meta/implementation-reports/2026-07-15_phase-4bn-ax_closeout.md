# Phase 4bn-AX — Closeout

## 1. Phase name

Phase 4bn-AX — Post-Fable Candidate Selection, CF-1 Decision-Consequence Test, and
Forced-Flow-Asymmetry Overlap Audit.

## 2. Branch

`phase-4bn-ax/post-fable-candidate-selection-cf1-decision-consequence-forced-flow-overlap-audit`.

## 3. Base SHA

`2294f846d6a0614149c57b93755b99e5e2df8006` (`HEAD == main == origin/main` at branch time; tip
after the Phase 4bn-AW merge-closeout SHA-finalization commit). Verified in sync before branching;
the only untracked item was the transient `.claude/scheduled_tasks.lock`, which was not staged,
modified, deleted, cleaned, or committed.

## 4. Phase type

Docs-only, post-Fable final candidate-selection phase (selection decision only). Not a
preregistration, experiment contract, data-read, model-design, feature-definition, event-definition,
threshold-selection, backtest, reserve-spend proposal, data-acquisition proposal, or
strategy-implementation phase.

## 5. Risk tier

Tier 1 / Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` (scientific
direction), though it mutates no eligibility, manifest, verdict, reserve, or lock and produces a
selection decision only.

## 6. Files added

Exactly three, all additions:

1. `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-ax_post-fable-candidate-selection-cf1-decision-consequence-forced-flow-overlap-audit.md` — main decision memo.
2. `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-ax_forced-flow-overlap-proxy-validity-and-m0-audit.md` — dedicated forced-flow audit.
3. `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-ax_closeout.md` — this closeout.

## 7. Confirmation no existing file modified

Confirmed. No existing file was modified, renamed, or deleted. The tracked diff is exactly three
added files. The evidence ledger, `current-project-state.md`, README, M0 gate, process standards,
phase gates, technical-debt register, and all prior reports are untouched.

## 8. Areas inspected

Committed, read-only: the Phase 4bn-AW screening memo, bounded Fable brief, closeout, and
merge-closeout (recording the operator-supplied post-phase Fable review); the Phase 4bn-AK ML
arc-decision memo; the Phase 4bn-AS `STOP_LONGHORIZON_ML_ARC` and Phase 4bn-AT
`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE` lineage (via AK/AS/AT restatement); the Phase 4ak
twelve-clause M0 gate (§6 cooldown, §7 cooled-down families incl. §7.A and §7.D); the Phase 4bn-AV
evidence ledger and spending-authority standard; the Phase 4bn-AB source-admissibility memo; and
committed source (`features_schema.py`, `features_schema_v002.py`) for feature/target capability
confirmation only. Git history/metadata for base-state verification. README and
`current-project-state.md` treated as potentially stale and navigational only.

## 9. Exact selected option

Option A — `SELECT_CF1_REALIZED_VOLATILITY_SUBSTRATE_TEST_FOR_LATER_PREREGISTRATION`.

## 10. CF-1 disposition

**Selected — only as a realized-volatility substrate test.** CF-1 clears every Section-7 selection
condition: mechanism distinct from the stopped directional arc (magnitude/variance via volatility
clustering, not sign); not a target swap; a null materially narrows the admissible trade-tape lane
(high negative-result value); a pass authorizes only a narrow, non-directional later docs-only
market-state-filter assessment, statable without directionality; developable on non-reserve
aggTrades; preregisterable with low researcher freedom; success neither reopens the stopped arc nor
authorizes sizing/gating/execution. Success would **not** establish directional edge or
profitability. CF-3 is not bundled; no metric/horizon/baseline/model/threshold/covariate is selected.

## 11. Forced-flow disposition

**Rejected — not selected, not deferred-with-a-path.** Decisive grounds (any one sufficient):
forced-liquidation identification is necessary but unavailable in committed data (forceOrder WS-only,
no history; no liquidation marker; `liquidation` column forbidden by the feature schema); admissible
aggTrades support only generic order-flow imbalance (already materialized as existing aggressor/burst
features and already tested); the proxy cannot separate forced flow from informed/news/momentum/
inventory confounds even conceptually; the family materially duplicates the stopped directional ML
arc and AW's rejected candidate #4, failing anti-rescue (M0.10/M0.12); and its event definition
requires an open-ended threshold search (high researcher-freedom / multiple testing). It fails
M0.2/M0.4/M0.8/M0.10/M0.12 and is a proxy/mechanism-mismatch scientific inadmissibility.

## 12. CF-2 disposition

Remains blocked on data availability/admissibility for its tradeable form; no acquisition authorized;
not promoted; no capture/acquisition phase designed. Comparison reference only.

## 13. CF-3 disposition

Remains unselected; not bundled into CF-1; funding/calendar covariates not promoted into CF-1; must
remain a non-directional context/regime lens (D1-A / §7.C boundary). Comparison reference only.

## 14. Select-none disposition

Considered as a fully valid option and **not** selected. It is coherent (zero researcher-freedom,
zero momentum risk) but would forfeit the one cheap, clean, high-negative-value scientific test the
substrate can still support; the decisive criterion (decision consequence / negative-result value)
favors selecting CF-1, whose null is decisively informative and whose selection conditions are all
met. A winner was not invented to avoid a paused result; CF-1 was selected on its merits and
forced-flow was killed on its demerits.

## 15. Strongest counterargument

CF-1 is non-directional while the project ultimately needs a directional edge under 16 bps, so even a
CF-1 pass yields no strategy and only more docs-only assessment; reusing the same feature substrate
could read as momentum after repeated negatives. This does not prevail: the phase frames CF-1 as a
substrate test with legitimate non-directional consequences, CF-1's null is high-value and cheap, and
CF-1's decision consequence is therefore not inert. (Full treatment: main memo §27–§28.)

## 16. Checks run

- `git fetch origin`; `git status --short` → only `?? .claude/scheduled_tasks.lock`.
- `git branch --show-current`; `git rev-parse HEAD` / `main` / `origin/main` → all
  `2294f846d6a0614149c57b93755b99e5e2df8006` pre-branch.
- `git log --oneline -10 --decorate` → confirmed tip at the AW SHA-finalization commit.
- `git switch -c phase-4bn-ax/…` → branch created; working tree clean apart from the transient lock.
- Post-write validation (`git status --short`; `git diff --check`; `git diff --name-status`;
  `git diff --stat`) → exactly three added files, no modifications/deletions/renames, no whitespace
  errors; recorded in the final operator report.

## 17. Tests / scripts / data / network not run

Because this is docs-only, the following were **not run**: pytest, Ruff, mypy, any project script,
builder, diagnostic, model, label or feature pipeline, backtest, replay, or runtime process; no data
workflow or acquisition workflow; no network, web search, API, Binance endpoint, credential,
WebSocket, exchange-write function, MCP, Graphify, or `.mcp.json`; no Fable or external reviewer. No
executable surface changed, so none applies.

## 18. Commit SHA self-reference convention

The Phase 4bn-AX phase commit adds exactly the three files in §6 with message
`docs(phase-4bn-ax): decide post-Fable strategy-research candidate`. Its exact SHA cannot be embedded
inside itself; it is recorded in the final operator report and the Git log after commit. No
merge-closeout is created and no SHA-finalization commit is performed by this phase (merge is a
separate, operator-authorized step).

## 19. Local / origin branch equality placeholders

After push, `git rev-parse HEAD` == `git rev-parse phase-4bn-ax/…` ==
`git rev-parse origin/phase-4bn-ax/…` (the phase-branch SHA `<PHASE_COMMIT_SHA>`); recorded exactly
in the final operator report. `main` and `origin/main` remain at
`2294f846d6a0614149c57b93755b99e5e2df8006` (untouched; no merge, no main push).

## 20. Exact final result state

`POST_FABLE_CANDIDATE_SELECTION_RECORDED__SELECT_CF1_REALIZED_VOLATILITY_SUBSTRATE_TEST_FOR_LATER_PREREGISTRATION__FORCED_FLOW_FAMILY_NOT_SELECTED__NO_HYPOTHESIS_EXECUTION_AUTHORIZED__NO_EVIDENCE_RESERVE_SPEND_AUTHORIZED`

## 21. No-execution statement

`No hypothesis, strategy, model, diagnostic, backtest, data acquisition, data reading, paper, shadow, live, or exchange-write execution is authorized by Phase 4bn-AX.`

## 22. No-reserve-spend statement

`No evidence reserve is authorized for spending by Phase 4bn-AX.`

Additional exact statements:

`Phase 4bn-AX selects at most one family for a later docs-only preregistration phase; it does not authorize that preregistration or any execution.`

`No metric, horizon, loss, baseline implementation, model, threshold, block count, covariate list, event definition, or event threshold is authorized by Phase 4bn-AX.`

`CF-1 is selected only as a realized-volatility substrate test; success would not establish directional edge, profitability, or permission to reopen the stopped long-horizon ML arc.`

## 23. Successor-authorization statement

`Phase 4bn-AY or any other successor requires separate operator authorization and a new Claude Code
prompt.` The proposed docs-only successor title —
`Phase 4bn-AY — CF-1 Realized-Volatility Magnitude-Forecasting Substrate-Test Preregistration
(docs-only, low-researcher-freedom)` — is proposed only and is not authorized by this phase.

## 24. Merge note

Merging Phase 4bn-AX into `main` requires a **separate operator prompt**. This phase does not merge,
does not create a merge-closeout, does not push `main`, and does not perform a SHA-finalization
commit. Recommended next operator action: return the three AX files and the final operator report to
ChatGPT for compliance review and a separate merge decision.

## 25. Preserved project locks

Unchanged: both stopped arcs (distinct; not merged/softened/reinterpreted/rescued/reopened); Phase
4aw `flip_research_eligible(...)` always-raising, never invoked; `research_eligible = false`;
`eligibility_gate_status = pending`; all published authorization flags false; the Phase 4bn-AE §19 M0
boundary; the Phase 4ak twelve-clause M0 gate with §6 cooldown and §7 cooled-down families; the
locked 8 bps/side · 16 bps round-trip cost; the Phase 4bn-AV evidence ledger, spending-authority
standard, and late-inadmissibility protocol; all dataset identities and hashes; split/holdout/
sidecar/storage policies; every prior verdict and retained-evidence classification; and every
completed implementation report.
