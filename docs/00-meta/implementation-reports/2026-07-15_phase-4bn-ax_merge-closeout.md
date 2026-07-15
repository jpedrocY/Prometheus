# Phase 4bn-AX — Merge Closeout

## 1. Phase identity

Phase 4bn-AX — Post-Fable Candidate Selection, CF-1 Decision-Consequence Test, and
Forced-Flow-Asymmetry Overlap Audit.

## 2. Phase type and merge action

Docs-only, post-Fable final candidate-selection phase (selection decision only). This document
records the review and merge of the completed Phase 4bn-AX branch into `main` via a no-fast-forward
merge commit, followed by a narrow SHA-finalization update of this same file on `main`. No
executable surface, evidence reserve, eligibility flag, manifest, verdict, or lock is touched by the
merge. The merge brings forward documentation only.

## 3. Risk tier

Tier 1 / Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` — it concerns
scientific direction and the return-to-strategy-research candidate-selection question, though it
mutates no eligibility, manifest, verdict, reserve, or lock and carries forward a selection decision
recorded in documentation only.

## 4. Source and target branches

- Source: `phase-4bn-ax/post-fable-candidate-selection-cf1-decision-consequence-forced-flow-overlap-audit`.
- Target: `main`.

## 5. Pre-merge `main` / base SHA

`2294f846d6a0614149c57b93755b99e5e2df8006` (`HEAD == main == origin/main` at merge time; tip after
the Phase 4bn-AW merge-closeout SHA-finalization commit). Verified in sync before any mutation. The
only untracked item was the transient `.claude/scheduled_tasks.lock`, which was not staged,
modified, deleted, cleaned, or committed.

## 6. Original Phase 4bn-AX phase commit SHA

`b53314bf710c0e9d86b0939b0ffbadb7a23103c0` — the single Phase 4bn-AX phase commit adding the three
AX documentation files (main decision memo, forced-flow overlap/proxy-validity/M0 audit, closeout).

## 7. Merge-closeout branch commit SHA

`TO_BE_FILLED_AFTER_MERGE` — the commit on the AX branch that adds this merge-closeout file
(`docs(phase-4bn-ax): add merge closeout`). Its exact SHA is recorded at SHA-finalization (§9) and
in the final operator report.

## 8. Merge commit SHA

`TO_BE_FILLED_AFTER_MERGE` — the no-fast-forward merge commit created on `main`
(`docs(phase-4bn-ax): merge post-Fable candidate selection`). Its exact SHA is recorded at
SHA-finalization (§9) and in the final operator report.

## 9. SHA-finalization commit statement

SHA-finalization commit SHA:
this update (`docs(phase-4bn-ax): finalize merge closeout shas`);
its exact SHA equals the resulting final `main` / `origin/main` tip and is
recorded in the final operator report and Git log. Its own SHA is not embedded inside the
commit that creates it.

## 10. Final `main` / `origin/main` statement

After the SHA-finalization commit is pushed, final `main` and `origin/main` will both equal the
SHA-finalization commit SHA (§9). `HEAD == main == origin/main` at completion.

## 11. Merge method

`git merge --no-ff` with an explicit merge commit. No fast-forward, no squash, no rebase, no amend,
no history rewrite, no hook skipping, no signing disablement, no force push.

## 12. Files brought forward

Exactly three AX documentation files, all additions:

1. `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-ax_post-fable-candidate-selection-cf1-decision-consequence-forced-flow-overlap-audit.md` — AX main decision memo.
2. `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-ax_forced-flow-overlap-proxy-validity-and-m0-audit.md` — AX dedicated forced-flow overlap / proxy-validity / M0 audit.
3. `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-ax_closeout.md` — AX closeout.

This merge-closeout file (`2026-07-15_phase-4bn-ax_merge-closeout.md`) is added on the AX branch
before the merge, so the merged base-to-final diff carries **four** added documents in total.

## 13. Additions-only confirmation

Confirmed additions-only. No existing file was modified, renamed, or deleted by the AX branch or by
the merge. The base-to-final diff contains only added AX documents plus one later narrow modification
of this merge-closeout file solely for SHA finalization.

## 14. Diff summary

- Pre-merge branch diff (`main..AX`): exactly the three added AX files, `932` insertions, no
  modifications / deletions / renames, no whitespace errors (`git diff --check` clean).
- Merged base-to-final diff (`2294f846..HEAD`): four added AX documents (the three above plus this
  merge-closeout), then one later modification of this merge-closeout solely to finalize the exact
  SHAs. No source, test, script, config, data, manifest, gate, sidecar, split, prior report, README,
  current-project-state, M0, evidence-ledger, phase-gate, technical-debt-register, or
  existing-process-standard file changed.

## 15. AW and Fable context

Phase 4bn-AW screened fourteen return-to-strategy candidate families, rejected eleven, and
shortlisted three (provisional ranking `CF-1 > CF-2 > CF-3`, CF-2 barred from first by a data block).
After AW completed and was pushed, the operator pasted only the bounded AW brief into a fresh Fable
chat; the resulting review is operator-supplied, bounded, post-phase, advisory, non-binding, and
incapable of authorizing any candidate, phase, data access, or reserve spend. Fable ranked
`CF-1 > CF-3 > CF-2`, recommended CF-1 alone framed as a substrate test, and proposed one omitted
family (liquidation-cascade / forced-flow asymmetry). Fable's illustrative 3–5% QLIKE improvement
margin was not adopted or authorized. Phase 4bn-AX adjudicated all of this on committed repository
evidence.

## 16. AX three-option decision

Phase 4bn-AX compared exactly three options across a consistent ordinal matrix (twenty criteria):
(A) select CF-1 as a substrate test for later preregistration; (B) select the forced-flow family for
later preregistration; (C) select none and remain paused. It selected exactly one.

## 17. Exact CF-1 selection

`SELECT_CF1_REALIZED_VOLATILITY_SUBSTRATE_TEST_FOR_LATER_PREREGISTRATION`. CF-1 —
microstructure realized-volatility (magnitude) forecasting from existing non-reserve BTCUSDT
aggTrades — is selected **only** as a realized-volatility substrate test, eligible to proceed to a
later, separately authorized docs-only preregistration phase. It is not selected as a trading
strategy, not selected as a directional hypothesis, and its execution is not authorized.

## 18. CF-1 scientific claim

Can trade-flow variables improve realized-volatility magnitude forecasts beyond a simple
persistence / HAR-RV baseline? The mechanism is volatility clustering / long memory in realized
variance; aggTrades order-flow intensity and trade-size dispersion may carry incremental information
about near-future realized variance beyond past RV. This is a magnitude/variance claim, not a
sign/direction claim.

## 19. CF-1 project-decision claim

Would a pass or fail materially change whether the existing admissible BTCUSDT aggTrades substrate
deserves further magnitude-focused research? Yes. The stopped ML arc characterized the substrate on
the directional axis (thin, economically immaterial, inverted at longer horizons); CF-1
characterizes the orthogonal magnitude axis using a more robust stylized fact, so pass or fail each
resolves a currently open question about the substrate's scientific informativeness.

## 20. CF-1 explicit non-trading boundary

CF-1's trading claim remains explicitly **false**. A positive realized-volatility forecast result
would not establish directional edge, profitability, or ability to clear the locked 16 bps
round-trip assumption. CF-1 carries no directional sign and by itself produces no direction,
profitability, position sizing, trade gating, or execution timing. CF-1 is selected only as a
substrate test.

## 21. CF-1 pass/fail consequences

- **Fail / null** (no incremental skill over a HAR-RV / variance-persistence baseline,
  block-consistent): materially close or narrow the admissible aggTrades research lane on the
  magnitude axis, complementing the already-stopped directional lane — high negative-result value at
  near-zero reserve cost.
- **Pass** (incremental, block-consistent skill): authorize only a later, separately approved
  docs-only assessment of whether the magnitude forecast could support a bounded, non-directional
  market-state / volatility-regime filter, and record the substrate as scientifically informative on
  the magnitude axis.

A pass does **not** authorize direction, strategy execution, position sizing, trade gating,
execution timing, reopening the stopped ML arc, terminal evidence, sealed evidence, or paper/shadow/
live trading.

## 22. CF-1 anti-rescue / target-swap conclusion

CF-1 is genuinely distinct from the stopped directional ML arc, not a target swap used to continue a
stopped search: target = realized variance / magnitude rather than sign; mechanism = volatility
clustering / long memory rather than short-horizon directional information; baseline family = HAR-RV
/ variance persistence rather than directional majority; no result-informed reuse of the consumed
internal holdout; no reopening of the directional-classifier family; no use of terminal or sealed
evidence. Residual honest caveat: CF-1 reuses the same aggTrades feature substrate, but substrate
reuse with a new orthogonal target and mechanism is not itself a rescue of a stopped directional
search.

## 23. CF-1 negative-result value

High. A clean null would materially reduce the remaining uncertainty about whether the admissible
aggTrades substrate contains incremental predictive structure beyond price-based baselines: combined
with the stopped directional arc, it would let the project state that the trade-tape carries neither
material directional nor material magnitude predictability beyond price baselines, closing the lane
cheaply and reinforcing the pause posture. One bounded CF-1 research arc is justified on this value
alone.

## 24. CF-1 momentum-by-success risk

Real and explicitly bounded. A CF-1 pass could create pressure to reopen directional work, to trade
on a "confident volatility regime," or to touch reserves. The boundary (§20–§21) confines a pass to
authorizing only a separate docs-only market-state-filter assessment; it does not infer direction,
reopen `STOP_LONGHORIZON_ML_ARC`, authorize sizing/gating/execution timing, or automatically use
terminal or sealed evidence. Each such step needs its own mechanism and separately authorized phase.

## 25. Forced-flow overlap conclusion

Decisive overlap. The committed 45-column aggTrades feature substrate already computes, per
1s/5s/15s/60s window, the proxy's ingredients: aggressive-flow ratio, aggressive-quantity imbalance,
aggressor buy/sell quantity, aggressor buy/sell count, trade count / burst activity, and quantity
sum and mean. The proposed "conditional directional drift" target returns to the same
`forward_direction` / `forward_log_return` family used in the stopped directional ML arc. Forced-flow
therefore materially overlaps generic order-flow imbalance, aggressor-flow imbalance, trade-burst
activity, short-horizon continuation/reversion, the stopped directional ML arc, AW's previously
rejected liquidation-cascade proxy, and cooled-down order-flow / microstructure lanes.

## 26. Forced-flow proxy-validity conclusion

FAIL. No official liquidation marker exists in committed admissible data; historical `forceOrder`
data is unavailable / unsuitable (WS-only, no archive); the feature schema forbids a `liquidation`
column; aggTrades cannot identify forced liquidation specifically; and one-sided, size-clustered
aggressor flow cannot be distinguished from informed trading, news response, ordinary momentum,
inventory liquidation, or generic order-flow imbalance even conceptually. Exact logic: if the proxy
claims liquidation identity it is invalid; if it does not, it collapses into already-tested generic
order flow.

## 27. Forced-flow M0 conclusion

Forced-flow fails the decisive M0 clauses recorded by AX — M0.2 (not structurally distinct), M0.4
(cannot distance itself from F1 / the depleted directional lane), M0.8 (forceOrder blocking;
aggTrades support only generic OFI), M0.10 (reduces to generic order-flow imbalance and the stopped
directional arc), and M0.12 (touches cooled-down §7.D; §6.A "materially new mechanism source" not
satisfied) — with adverse M0.5/M0.6/M0.7 implications and high researcher-freedom / multiple-testing
risk. Temporal ordering is the only dimension it passes, which is not sufficient.

## 28. Forced-flow anti-rescue rejection

`REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`. The forced-flow / liquidation-asymmetry family
is not selected, not deferred with an authorized path, not eligible for later preregistration on the
committed record, and not authorized for event-rule design, data acquisition, or execution. The
rejection is not softened into "blocked" or "promising."

## 29. CF-2 blocked posture

CF-2 (cross-symbol temporal lead–lag) remains blocked on data availability/admissibility for its
meaningful tradeable form. No CF-2 acquisition or prospective capture is authorized; CF-2 is not
promoted. It served only as a comparison reference.

## 30. CF-3 non-bundling posture

CF-3 (derivatives-context + settlement/session-timing volatility-regime conditioning) remains
unselected and is not bundled into CF-1. No funding, calendar, open-interest, or context covariate is
promoted into CF-1. CF-3 must remain a non-directional context/regime lens (D1-A / M0 §7.C boundary).
It served only as a comparison reference.

## 31. Select-none disposition

`SELECT_NONE_AND_REMAIN_PAUSED` was considered as a fully valid option and was not selected. A winner
was not invented to avoid a paused result: CF-1 was selected on its merits (it clears every AX
selection condition) and forced-flow was rejected on its demerits (it fails its kill criteria).
Select-none would have forfeited the one cheap, clean, high-negative-value scientific test the
substrate can still support.

## 32. Strongest counterargument

CF-1 is non-directional while the project ultimately needs an economically viable directional edge
under 16 bps, and even a CF-1 pass could leave the project without a strategy while creating
momentum-by-success.

## 33. Decisive criterion

`DECISION_CONSEQUENCE_AND_NEGATIVE_RESULT_VALUE`. The counterargument did not prevail because CF-1 is
explicitly bounded as a substrate test; its null is high-value and cheap; its pass consequence is
narrow and non-directional; and it clears every AX selection condition while forced-flow fails its
kill criteria. CF-1's decision consequence is therefore not inert.

## 34. Evidence / reasoning that would change the decision

- Toward select-none: committed or admissible evidence that a HAR-RV baseline is either trivially
  unbeatable (null preordained) or trivially beatable (a win uninformative), or that a CF-1 null
  would not narrow the lane — any would gut CF-1's falsifiability and negative-result value.
- Toward forced-flow (still would not have prevailed): admissible, committed data that actually
  identifies forced liquidations (an archived `forceOrder` feed or margin-state marker aligned to the
  2024 window) plus a bounded, externally-anchored event definition — none of which exists, and no
  acquisition is authorized.

## 35. Proposed Phase 4bn-AY title, explicitly not authorized

`Phase 4bn-AY — CF-1 Realized-Volatility Magnitude-Forecasting Substrate-Test Preregistration
(docs-only, low-researcher-freedom)`. This title is **proposed only**. It is not authorized by
Phase 4bn-AX, by AW, by Fable, by this merge, or by the operator's authorization of this merge, and
requires separate operator authorization and a new Claude Code prompt before any work begins.

## 36. Confirmation no metric / horizon / model / threshold / event definition was selected

Confirmed. No metric, horizon, loss function, baseline implementation, model class, block count,
covariate list, threshold, event definition, or event threshold was selected or authorized by Phase
4bn-AX or by this merge. Those belong to a later CF-1 preregistration only if separately authorized.

## 37. Confirmation no reserve was opened or spent

No evidence reserve was opened, read, loaded, inspected, enumerated for content, sampled, or scored
during this phase or merge. The v002 terminal window and v002 sealed test remain
`UNTOUCHED_RESERVED`; `PRE_V002_INTERNAL_HOLDOUT = CONSUMED` (descriptive-only) is unchanged;
`HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE` is unchanged; `test_rows_loaded = 0`
posture preserved. Nothing under `data/microstructure/` or `data/research/` was opened.

## 38. Confirmation no executable surface changed

No source, test, script, config, builder, model, diagnostic, backtest, runtime, feature, or label
surface changed. The merge and finalization carry documentation only.

## 39. Validation results

- Pre-merge: `git fetch origin`; `git status --short` (only the transient lock);
  `git branch --show-current`; `git rev-parse main` / `origin/main` (`2294f846…`);
  `git rev-parse` local/origin AX branch (`b53314b…`); `git diff --check main..AX` (clean);
  `git diff --name-status` / `--stat main..AX` (three added files, 932 insertions);
  `git show --stat --oneline b53314b`.
- Post-merge: `git status --short`; `git diff --check 2294f846..HEAD` (clean);
  `git diff --name-status` / `--stat 2294f846..HEAD` (four added documents; no
  modification/deletion/rename before finalization); `git log --oneline -8 --decorate`;
  `git rev-parse main` / `origin/main` equal to the merge commit; final equality
  `HEAD == main == origin/main` after finalization push.
- Because this is docs-only, `pytest`, Ruff, mypy, project scripts, data workflows, models,
  diagnostics, backtests, and runtime processes were **not run** — no executable surface changed and
  execution is outside merge scope.

## 40. Manifest, eligibility, M0, ledger, split, sidecar, storage, and evidence-lock preservation

Unchanged: Phase 4aw `flip_research_eligible(...)` always-raising and never invoked;
`research_eligible = false`; `eligibility_gate_status = pending`; all published authorization flags
`false`; the Phase 4bn-AE §19 M0 boundary (absolute); the Phase 4ak twelve-clause M0 gate with the §6
cooldown and §7 cooled-down families (incl. §7.A directional depletion and §7.D order-flow /
microstructure lane); the M0 cooldown and cooled-down-family rules; the locked 8 bps/side · 16 bps
round-trip assumption; dataset identities and hashes; split and holdout policies; the Phase 4bn-AV
evidence ledger, spending-authority standard, and late-inadmissibility protocol; Phase 4bb-F sidecar
and Phase 4bn-L storage policies; both stopped arcs (`STOP_LONGHORIZON_ML_ARC` and
`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`, distinct and not merged/softened/reinterpreted/rescued/
reopened); all prior strategy verdicts (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1
and the 5m thread); all retained-evidence classifications; and all previous implementation reports.

## 41. Exact post-merge result state

`POST_FABLE_CANDIDATE_SELECTION_AND_FORCED_FLOW_AUDIT_MERGED_TO_MAIN__CF1_SELECTED_ONLY_FOR_LATER_DOCS_ONLY_PREREGISTRATION__FORCED_FLOW_REJECTED__NO_HYPOTHESIS_EXECUTION_AUTHORIZED__NO_EVIDENCE_RESERVE_SPEND_AUTHORIZED`

Exact statements:

`CF-1 is selected only for a later, separately authorized docs-only realized-volatility substrate-test preregistration.`

`CF-1 selection does not establish directional edge, profitability, ability to clear 16 bps, or permission to reopen the stopped long-horizon ML arc.`

`The forced-flow / liquidation-asymmetry family is rejected on overlap, proxy-validity, M0, and anti-rescue grounds.`

`No metric, horizon, loss, baseline implementation, model, threshold, block count, covariate list, event definition, or event threshold is authorized by the Phase 4bn-AX merge.`

`No hypothesis, strategy, model, diagnostic, backtest, data acquisition, data reading, paper, shadow, live, or exchange-write execution is authorized by the Phase 4bn-AX merge.`

`No evidence reserve is authorized for spending by the Phase 4bn-AX merge.`

`Phase 4bn-AY or any other successor requires separate operator authorization and a new Claude Code prompt.`

## 42. Required post-merge operator posture

The project remains paused with respect to execution. CF-1 is selected only for a later,
separately authorized docs-only preregistration; the forced-flow family is rejected; CF-2 is blocked
with no acquisition authorized; CF-3 is unselected and unbundled; `SELECT_NONE_AND_REMAIN_PAUSED`
remains a live future option. Recommended next operator action: return this merge-closeout and the
final operator report to ChatGPT for review before deciding whether to authorize the docs-only Phase
4bn-AY CF-1 substrate-test preregistration. Any successor requires separate operator authorization
and a new Claude Code prompt. No candidate execution, preregistration, data acquisition, or reserve
spend is begun or authorized here.
