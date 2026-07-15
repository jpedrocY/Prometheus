# Phase 4bn-AX — Post-Fable Candidate Selection, CF-1 Decision-Consequence Test, and Forced-Flow-Asymmetry Overlap Audit

## 1. Phase identity

Phase 4bn-AX — Post-Fable Candidate Selection, CF-1 Decision-Consequence Test, and
Forced-Flow-Asymmetry Overlap Audit. This is a docs-only, post-Fable **final
candidate-selection** phase that makes exactly one repository-grounded selection decision among
three options (select CF-1 as a substrate test; select the forced-flow family; or select none and
remain paused), tests CF-1's decision consequence, and adjudicates the omitted forced-flow family
on committed evidence. Its companion file
(`2026-07-15_phase-4bn-ax_forced-flow-overlap-proxy-validity-and-m0-audit.md`) carries the detailed
forced-flow overlap / proxy-validity / M0 audit; its closeout
(`2026-07-15_phase-4bn-ax_closeout.md`) records the branch/merge posture.

## 2. Branch

`phase-4bn-ax/post-fable-candidate-selection-cf1-decision-consequence-forced-flow-overlap-audit`.

## 3. Base SHA

`2294f846d6a0614149c57b93755b99e5e2df8006` (`HEAD == main == origin/main` at branch time; the
tip after the Phase 4bn-AW merge-closeout SHA-finalization commit). Verified in sync before
branching; the only untracked item was the transient `.claude/scheduled_tasks.lock`, which was
not staged, modified, deleted, cleaned, or committed.

## 4. Phase type

Docs-only **candidate-selection** phase. It reads committed documentation, committed source,
committed tests, and Git history read-only; reasons over the committed screening result, the
operator-supplied post-phase Fable review, the negative-result lineage, the data-capability
record, and the committed feature/label schema; and creates exactly three new documentation
files. It is a selection decision only. It is **not** a preregistration, an experiment contract,
a data-read phase, a model-design phase, a feature-definition phase, an event-definition phase,
a threshold-selection phase, a backtest, a reserve-spend proposal, a data-acquisition proposal,
or a strategy-implementation phase. It authorizes nothing beyond the creation of documentation.

## 5. Risk tier

Tier 1 / Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` — it concerns
scientific direction and the return-to-strategy-research question, so it is treated at the highest
ceremony tier even though it mutates no eligibility, manifest, verdict, reserve, or lock and
produces a selection decision only.

## 6. Exact authorization boundary

Authorized: read committed docs / source / tests / Git metadata; author exactly three new files
(this memo, the forced-flow audit, and a closeout); commit and push the dedicated phase branch.
**Not** authorized: to spend, read, load, inspect, enumerate for content, sample, or score any
evidence reserve; to open the v002 terminal window or v002 sealed test; to open anything under
`data/microstructure/` or `data/research/`, any generated research/model/diagnostic/backtest
output, or any uncommitted local data; to acquire or read any market data; to run pytest / Ruff /
mypy / any project script / builder / diagnostic / model / label / feature pipeline / backtest /
replay / runtime process; to use the network, web search, any API, credentials, WebSocket, MCP,
Graphify, or `.mcp.json`; to run Fable or any external reviewer; to modify any existing file; to
create a preregistration, experiment contract, data-acquisition proposal, reserve-spend proposal,
or successor execution prompt; or to authorize any successor phase. This phase used committed
repository evidence only.

## 7. Areas inspected

Committed, read-only (README and `docs/00-meta/current-project-state.md` treated as potentially
stale and navigational only; recent implementation reports, merge-closeouts, source, and tests
outrank stale summaries):

- **AW lineage:** the Phase 4bn-AW screening memo
  (`…_return-to-strategy-research-candidate-family-screening.md`), its bounded Fable brief, its
  closeout, and its merge-closeout (which records the operator-supplied post-phase Fable review,
  §24–§32).
- **Stopped-arc / decision lineage:** Phase 4bn-AK ML arc-decision memo; Phase 4bn-AS long-horizon
  ML ambiguity decision (`STOP_LONGHORIZON_ML_ARC`); Phase 4bn-AT top-of-book mechanism
  admissibility (`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`); the AJ / AP / AQ / AR results as
  restated through AK / AS / AT.
- **Governance:** the Phase 4ak twelve-clause M0 gate (`docs/00-meta/m0-mechanism-admissibility-gate.md`,
  incl. §6 cooldown and §7 cooled-down families, esp. §7.A directional depletion and §7.D
  order-flow/microstructure); the Phase 4bn-AU post-AT direction review; the Phase 4bn-AV evidence
  ledger, spending-authority standard, and late-inadmissibility protocol; the Phase 4bn-AB
  source-admissibility memo.
- **Committed source / schema (capability confirmation only; none modified):**
  `src/prometheus/research/microstructure/features_schema.py` (the finalized 45-column aggTrades
  feature contract — `PER_WINDOW_FEATURE_TEMPLATES` incl. `rolling_aggressive_flow_ratio`,
  `rolling_aggressive_quantity_imbalance`, `rolling_aggressive_buy/sell_quantity`,
  `rolling_aggressive_buy/sell_count`, `rolling_aggtrade_count`, `rolling_quantity_sum/mean`; the
  `FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS` list barring the `liquidation` token); `features_schema_v002.py`.
- **Git history / metadata:** `git fetch` / `status` / `rev-parse` / `log` for base-state
  verification.

## 8. Confirmation no data or reserve was opened

Confirmed. No feature/label/normalized/raw row, no v002 terminal window, no v002 sealed test, no
generated local research/model/diagnostic/backtest artefact, and nothing under
`data/microstructure/` or `data/research/` was opened, read, listed for content, hashed, sampled,
or scored. The Phase 4bn-AV evidence ledger is preserved exactly:
`PRE_V002_INTERNAL_HOLDOUT = CONSUMED` (descriptive-only), `V002_TERMINAL_WINDOW =
UNTOUCHED_RESERVED`, `V002_SEALED_TEST = UNTOUCHED_RESERVED`, `HIST_TOB_BOOKTICKER_SOURCE =
INADMISSIBLE_OR_UNAVAILABLE`, `test_rows_loaded = 0`. No evidence reserve was spent. No network,
endpoint, credential, or external reviewer was used.

## 9. AW shortlist summary

Phase 4bn-AW generated fourteen candidate families, rejected eleven (one — trade-burst / activity,
M-6 — merged into CF-1), and shortlisted three, provisionally ranked `CF-1 > CF-2 > CF-3`:

- **CF-1** — Microstructure realized-volatility (magnitude) forecasting from aggTrades. Provisional
  first: developable now on non-reserve BTCUSDT aggTrades, most robust mechanism (volatility
  clustering / long memory), cleanest predeclared kill (no incremental skill over a HAR-RV /
  RV-persistence baseline), highest negative-result value, preserves both reserves.
- **CF-2** — Cross-symbol temporal lead–lag / information transmission. Strongest mechanism and the
  only genuinely directional survivor, but its tradeable (multi-symbol aggTrades) form is **blocked**
  on unacquired data; barred from first.
- **CF-3** — Derivatives-context + settlement/session-timing volatility-regime conditioning.
  Developable now (funding + fixed UTC calendar) but weakest decision consequence, a
  non-directional context/regime lens with target overlap onto CF-1's realized-volatility target;
  OI sub-component blocked.

The AW shortlist is provisional and non-authorizing.

## 10. Fable review standing and summary

**Standing.** After AW completed and was pushed, the operator pasted only the bounded AW brief into
a fresh Fable chat. The resulting review is operator-supplied, bounded, post-phase, advisory,
non-binding, and independent of the AW execution agent; it is **incapable** of authorizing any
candidate, phase, data access, or reserve spend (AW merge-closeout §24). It is treated here as
input requiring repository-grounded adjudication, not as authority.

**Summary.** Fable ranking `CF-1 > CF-3 > CF-2` (CF-2 demoted below CF-3 because a blocked
candidate cannot outrank a currently developable one under the screening's own developability
criterion). Fable recommended **CF-1 alone**, framed as a **substrate test rather than a strategy
bet**; do not bundle CF-3; do not authorize CF-2 acquisition. Fable's strongest self-objection: a
perfect volatility forecast may contain zero directional information, so CF-1 could be decision-inert
under the directional 16 bps frame and select-none may be cleaner. Fable proposed one omitted family
(liquidation-cascade / forced-flow asymmetry, trade-tape only) with its own caveats (no official
liquidation feed; proxy freedom; confound overlap; must clear 16 bps). Fable's illustrative 3–5%
QLIKE improvement margin **is not adopted or authorized** and is not repository policy.

## 11. CF-1 scientific claim

*Can trade-flow variables improve volatility-magnitude forecasts beyond a simple persistence /
HAR-RV baseline?* Mechanism: realized variance exhibits clustering and long memory (ARCH/HAR
stylized fact); aggTrades order-flow intensity and trade-size dispersion may carry incremental
information about near-future realized variance beyond past RV. This is a **magnitude / variance**
claim, not a sign / direction claim.

## 12. CF-1 project-decision claim

*Would a pass or fail materially change whether the existing trade-tape substrate deserves further
research?* Yes. The stopped ML arc characterized the substrate on the **directional** axis and
found it economically thin (~2.47% of 15s moves clear 16 bps) and inverted at longer horizons.
CF-1 characterizes the same substrate on the orthogonal **magnitude** axis using a more robust
stylized fact. A pass or a fail each resolves a currently open question about the substrate's
scientific informativeness (see §14).

## 13. CF-1 non-trading boundary

The **trading claim** — *does success imply a profitable directional edge under 16 bps?* — is
explicitly **false** and is not established by this phase, by CF-1's selection, or by any future
CF-1 result unless separately established later. A realized-volatility magnitude forecast contains
no directional sign; success would not by itself produce direction, profitability, position sizing,
trade gating, or execution timing. CF-1 is selected only as a substrate test.

## 14. CF-1 decision-consequence test

The required test states exactly what future project decision changes on pass and on fail, with the
pass consequence narrow and non-directional:

- **CF-1 fail (null: no incremental skill over the HAR-RV / RV-persistence baseline, block-consistent).**
  Consequence: **materially close or narrow the admissible trade-tape research lane.** A null shows
  the aggTrades substrate lacks even magnitude-predictability beyond price-based baselines — that,
  having already shown only thin, non-material directional information, it also carries no
  incremental *magnitude* structure. This lets the project retire the trade-tape substrate as a
  research lane with confidence, at near-zero reserve cost, rather than lingering in "maybe there is
  something." **High negative-result value.**
- **CF-1 pass (incremental, block-consistent skill over the baseline).** Consequence (narrow,
  non-directional): authorize **only** a separate later docs-only assessment of whether a
  realized-volatility forecast could support a **bounded, non-directional market-state / volatility-
  regime filter**, and record the trade-tape substrate as **scientifically informative on the
  magnitude axis**. It does **not** authorize trading, direction, sizing, gating, execution timing,
  reopening the stopped ML arc, or any use of terminal/sealed evidence — each of those requires its
  own separate mechanism and phase.

Both consequences are legitimate project decisions that can be stated **without assuming
directionality**. The pass consequence is deliberately narrow (more docs-only assessment, not
execution); the fail consequence is the high-value one.

## 15. CF-1 novelty / target-swap audit

CF-1 is genuinely distinct from the stopped directional ML arc, not a target swap used to continue
a stopped search:

- **Different target.** The stopped arc fit `forward_direction_<H>` (sign); CF-1 forecasts realized
  **variance / magnitude**. Sign and magnitude are orthogonal — a magnitude forecast yields no
  directional decision.
- **Different, more robust mechanism.** Volatility clustering / long memory in realized variance is
  a stronger, externally-documented stylized fact than short-horizon directional information; CF-1's
  predeclared comparison is against a HAR-RV / variance-persistence baseline, not against a naive
  directional majority.
- **Escapes the depleted lanes.** Being non-directional, CF-1 sits outside the §7.A price-only
  directional depletion and does not re-fit the stopped classifier; its M0.3 route is the
  "equivalent baseline differential for non-strategy mechanism claims," not a Δ_R directional edge.
- **No result-informed reuse.** It does not reuse the consumed pre-v002 internal holdout as
  confirmation (descriptive-only), and its question is fixed ex ante (predeclarable HAR-RV baseline),
  not tuned to prior forensics.

The residual honest caveat: CF-1 reuses the same feature substrate. But reusing a substrate with a
new, orthogonal, more-robust target and mechanism is not a rescue of a stopped *directional* search;
it is the correct next scientific question about the same data.

## 16. CF-1 negative-result value

High. A CF-1 null is the single most decision-relevant outcome the substrate could still produce:
combined with the stopped directional arc, it would let the project state that the admissible
aggTrades trade-tape carries neither material directional nor material magnitude predictability
beyond price-based baselines, closing the lane at near-zero reserve cost and reinforcing the pause
posture. Because the null is clean and cheap, one bounded CF-1 research arc is justified on its
negative-result value alone.

## 17. CF-1 momentum-by-success risk

Real and explicitly bounded. A CF-1 pass could create pressure to reopen directional work, to trade
on a "confident volatility regime," or to touch reserves. The boundary is stated in §13/§14: a pass
authorizes **only** a separate docs-only market-state-filter assessment; it does **not** infer
direction, reopen `STOP_LONGHORIZON_ML_ARC`, authorize sizing / gating / execution timing, or
automatically use terminal or sealed evidence. Each such step needs its own mechanism and separately
authorized phase. This boundary is a condition of the selection, not an afterthought.

## 18. Forced-flow proposed mechanism

Liquidation cascades create mechanically forced sellers/buyers; bursts of one-sided, size-clustered
aggressor flow may proxy forced liquidation; forced flow may overshoot and partially revert; a
predeclared forced-flow event may be followed by conditional directional drift, using existing
BTCUSDT aggTrades only. (Restated, not adopted.)

## 19. Forced-flow overlap summary

**Decisive overlap (see companion audit §4–§11).** The committed 45-column aggTrades feature
substrate already computes, per 1s/5s/15s/60s window, exactly the proxy's ingredients: one-sidedness
(`rolling_aggressive_flow_ratio`, `rolling_aggressive_quantity_imbalance`, aggressor buy/sell
quantity and count), size-clustering (`rolling_quantity_mean`, `rolling_quantity_sum`), and
burstiness (`rolling_aggtrade_count`). The proposed "conditional directional drift" target is the
same `forward_direction_<H>` / `forward_log_return_<H>` family the stopped ML arc already tested.
Forced-flow is therefore a threshold-plus-relabel over already-tested aggressor/burst features
feeding the depleted directional target — it materially duplicates the stopped directional ML arc,
generic order-flow imbalance, trade-burst activity (AW candidate #11, merged into CF-1), and AW's
already-rejected liquidation-cascade proxy (candidate #4).

## 20. Forced-flow proxy-validity summary

**FAIL.** No official liquidation marker exists in committed admissible data (forceOrder is WS-only
with no historical archive → INADMISSIBLE retrospectively; the feature schema even forbids a
`liquidation` column). Existing aggTrades cannot identify forced liquidation specifically, and
one-sided size-clustered aggressor flow cannot distinguish forced (margin-driven) liquidation from
ordinary informed trading, news response, momentum, or inventory unwinding — not even conceptually
on trade-tape data. The mechanism remains "meaningful" only by collapsing into generic order-flow-
imbalance directional prediction, which is already tested and cooled down. The proxy is thus either
invalid (if it claims to identify liquidations) or redundant (if it does not).

## 21. Forced-flow M0 summary

**Fails M0 on multiple binding clauses (companion audit §19):** M0.2 (not structurally distinct — a
relabel over existing features), M0.4 (cannot distance itself from F1 / §7.A given a sign that can
be re-narrated as overshoot or reversion), M0.8 (forceOrder blocking; aggTrades support only generic
OFI), M0.10 (reduces to generic order-flow imbalance and the stopped directional arc), and M0.12
(touches cooled-down §7.D, and §6.A "materially new mechanism source" not satisfied — no new
observable). M0.5/M0.6/M0.7 are adverse (inherits the stopped arc's ~2.47%-clear-16bps thinness with
a smaller conditional sample), and researcher-freedom / multiple-testing are high (open-ended
threshold search). Temporal ordering is the only dimension it passes, which is not sufficient.
**Anti-rescue conclusion: rescue-shaped; rejected.**

## 22. CF-2 blocked posture

CF-2 remains blocked on data availability/admissibility for its meaningful (tradeable-granularity
multi-symbol aggTrades) form; its admissible (coarse kline) form is likely already arbitraged. No
acquisition is authorized. CF-2 is **not promoted**, and this phase does **not** design a prospective
capture or acquisition phase for it. CF-2 is used only as a comparison reference.

## 23. CF-3 non-bundling posture

CF-3 remains unselected. It is **not bundled** into CF-1; funding/calendar covariates are **not**
promoted into the selected family; a fixed calendar is **not** treated as a reason to widen CF-1.
CF-3 must remain a non-directional context/regime lens (D1-A / §7.C boundary) and is used only as a
comparison reference.

## 24. Three-option decision matrix

Consistent ordinal assessment (`STRONG` / `MODERATE` / `WEAK` / `FAIL`); reasoned comparison, no
pseudo-precise weighting.

| # | Criterion | Select CF-1 (substrate test) | Select forced-flow | Select none (remain paused) |
|---|---|---|---|---|
| 1 | Genuine novelty | STRONG (magnitude ≠ direction; robust mechanism) | FAIL (relabel of tested OFI/burst + stopped arc) | n/a (no new family) |
| 2 | Mechanism clarity | STRONG (volatility clustering) | WEAK (forced ≠ observable) | n/a |
| 3 | Observability | STRONG (aggTrades on disk) | FAIL (no liquidation marker) | n/a |
| 4 | Proxy validity | STRONG (RV directly derivable) | FAIL | n/a |
| 5 | Source/data admissibility | STRONG (non-reserve aggTrades) | FAIL (forceOrder blocking) | n/a |
| 6 | Temporal ordering | STRONG (causal features, forward RV) | MODERATE (ordered but unidentified) | n/a |
| 7 | Development without acquisition | STRONG | MODERATE (aggTrades only, but wrong object) | n/a |
| 8 | Development without reserve spend | STRONG | STRONG | STRONG |
| 9 | Falsifiability | STRONG (HAR-RV kill) | WEAK (sign re-narratable) | n/a |
| 10 | Researcher-freedom / multiple testing | MODERATE (few baselines; predeclarable) | FAIL (open-ended thresholds) | STRONG (none) |
| 11 | Anti-rescue compliance | STRONG (non-directional, new target) | FAIL (rescue-shaped) | STRONG |
| 12 | M0 compatibility | MODERATE (non-directional; M0.8 PASS) | FAIL (M0.2/4/8/10/12) | STRONG (nothing to clear) |
| 13 | Negative-result value | STRONG (closes magnitude lane) | WEAK | n/a |
| 14 | Positive-result decision consequence | MODERATE (narrow, non-directional) | WEAK (thin, confounded) | n/a |
| 15 | Directional relevance | WEAK by design (non-directional) | WEAK (thin, confounded) | n/a |
| 16 | Economic relevance under 16 bps | WEAK direct / STRONG as triage | FAIL/Adverse | n/a |
| 17 | Risk of momentum-by-success | MODERATE (bounded in §17) | HIGH (rescue pressure) | LOW |
| 18 | Durable project value | STRONG (first admissible magnitude test) | WEAK | MODERATE (clean pause) |
| 19 | Implementation burden | LOW (data built; RV derivable) | HIGH (event invention) | NONE |
| 20 | Ability to define a later bounded preregistration | STRONG (low-freedom HAR-RV design) | FAIL | n/a |

Net: CF-1 is STRONG or MODERATE on every criterion that bears on selectability and FAIL on none;
forced-flow is FAIL on the decisive identifiability / admissibility / anti-rescue criteria;
select-none is a coherent alternative whose only real edge is zero researcher-freedom and zero
momentum risk.

## 25. Exact selected result

`SELECT_CF1_REALIZED_VOLATILITY_SUBSTRATE_TEST_FOR_LATER_PREREGISTRATION`.

## 26. One-paragraph rationale

CF-1 is the only surviving candidate that is simultaneously genuinely novel relative to both stopped
arcs (a magnitude/variance target driven by volatility clustering, orthogonal to the stopped
directional program and outside the depleted price-only and order-flow lanes), fully developable now
on already-built non-reserve BTCUSDT aggTrades with both scarce reserves untouched, cleanly
falsifiable against a predeclarable HAR-RV / variance-persistence baseline with low researcher
freedom, and carrying a legitimate, non-directional pass/fail decision consequence whose null is
high-value (it would let the project retire the trade-tape substrate on the magnitude axis as it has
effectively done on the directional axis, at near-zero cost). The forced-flow family fails decisively
on proxy validity, source admissibility, M0.2/4/8/10/12, and anti-rescue — it is a threshold-plus-
relabel over aggressor/burst features that already exist and were already tested, pointed at the same
economically-thin directional target, with no committed data able to identify "forced" flow.
Select-none is coherent but would forfeit the one cheap, clean, high-negative-value scientific test
the substrate can still support; a paused project is better served by resolving the magnitude
question than by leaving it permanently open. CF-1 is therefore selected **only as a substrate test**,
with an explicit non-directional, non-execution boundary.

## 27. Strongest counterargument

The strongest case for select-none: CF-1 is non-directional, yet the project ultimately needs a
profitable *directional* edge under 16 bps; a volatility-magnitude forecast, however clean, is not
that edge, so even a CF-1 pass leaves the project with no strategy and only authorizes more docs-only
assessment — arguably "a positive result would not meaningfully advance toward a robust strategy"
(a select-none criterion). Reusing the same feature substrate could also be read as momentum after a
string of negatives, and there is external reason to expect HAR-RV-plus-microstructure improvements
to be small and unsurprising, lowering CF-1's marginal research value.

## 28. Why the counterargument does or does not prevail (decisive criterion)

It does **not** prevail, and the **decisive criterion is decision consequence, specifically the
value of the negative result**. The select-none criterion "a positive result would not advance
toward a robust strategy" is satisfied for CF-1 on the *directional-endpoint* reading — but the
phase mandate explicitly frames CF-1 as a substrate test whose permissible consequences are
non-directional (close/preserve the substrate as scientifically informative; authorize a bounded
market-state-filter assessment), and CF-1 meets **every** Section-7 selection condition: its
mechanism is distinct from the stopped arc, it is not a target swap, its null materially narrows the
admissible lane, its pass authorizes only a narrow non-directional later decision statable without
directionality, it develops on non-reserve data, it can be preregistered with low researcher freedom,
its negative-result value is high, and its success neither reopens the stopped arc nor authorizes
sizing/gating/execution. Forced-flow fails its own kill criteria (unobservable "forced" flow;
reduction to generic OFI / the stopped arc; open-ended thresholds), so it cannot be the winner; and
CF-1's decision consequence is *not* inert (the null is decisively informative and cheap), so
select-none's decisive condition — "CF-1 lacks a legitimate decision consequence" — is not met.
Between a candidate that clears every selection condition and a pause that forfeits a cheap, clean,
high-value scientific test, the evidence supports selection.

## 29. Evidence or reasoning that would change the decision

- **Toward select-none:** committed or admissible evidence that a HAR-RV baseline is either
  trivially unbeatable (so the null is preordained and uninformative) or trivially beatable (so a
  "win" carries no information) — either would gut CF-1's falsifiability and negative-result value and
  flip the decision to remain paused. Likewise, a demonstration that CF-1's null would **not** narrow
  the lane (e.g., because magnitude-predictability is already externally known to be present and thus
  decision-inert here) would remove its decisive advantage.
- **Toward forced-flow (would still not have prevailed here):** admissible, committed data that
  actually **identifies** forced liquidations (an archived forceOrder feed or margin-state marker
  aligned to the 2024 window) plus a bounded, low-freedom event definition anchored in external
  theory — none of which exists in the committed record, and no acquisition is authorized.
- **Toward CF-2/CF-3:** not in scope for reversal here (CF-2 blocked; CF-3 non-directional context
  lens); they are comparison references only.

## 30. Exact future-phase title (proposed only)

`Phase 4bn-AY — CF-1 Realized-Volatility Magnitude-Forecasting Substrate-Test Preregistration (docs-only, low-researcher-freedom)`.

## 31. Confirmation the future phase is proposed only

The Phase 4bn-AY title in §30 is **proposed only**. It is not authorized by this phase, by AW, by
Fable, or by the operator's authorization of Phase 4bn-AX. It requires separate operator
authorization and a new Claude Code prompt before any work begins.

## 32. Confirmation no metric / horizon / model / threshold / event definition is authorized

No metric, horizon, loss function, baseline implementation, model class, block count, covariate
list, event definition, or event threshold is selected or authorized by this phase. Those belong to
a later CF-1 preregistration only if separately authorized. CF-3 is not bundled; no funding/calendar
covariate is promoted into CF-1.

## 33. Confirmation no data / execution / acquisition / reserve spend is authorized

No data read, model, diagnostic, backtest, replay, feature/label build, strategy, signal, paper,
shadow, live, or exchange-write execution is authorized; no data acquisition is authorized; no
evidence reserve is authorized for spending. The v002 terminal window and v002 sealed test remain
`UNTOUCHED_RESERVED`; the consumed pre-v002 internal holdout remains descriptive-only.

## 34. Recommended next operator action

Return the three Phase 4bn-AX files and the final operator report to ChatGPT for compliance review
and a separate merge decision. Do not run Fable. Do not merge from inside this phase. If, after
review, the operator wishes to proceed, the next possible step is to separately authorize the
docs-only Phase 4bn-AY CF-1 substrate-test preregistration (§30) via a new Claude Code prompt — but
the project otherwise remains paused, and remaining paused is a valid operator choice.

## 35. Exact final result state

`POST_FABLE_CANDIDATE_SELECTION_RECORDED__SELECT_CF1_REALIZED_VOLATILITY_SUBSTRATE_TEST_FOR_LATER_PREREGISTRATION__FORCED_FLOW_FAMILY_NOT_SELECTED__NO_HYPOTHESIS_EXECUTION_AUTHORIZED__NO_EVIDENCE_RESERVE_SPEND_AUTHORIZED`

Exact statements:

`No hypothesis, strategy, model, diagnostic, backtest, data acquisition, data reading, paper, shadow, live, or exchange-write execution is authorized by Phase 4bn-AX.`

`No evidence reserve is authorized for spending by Phase 4bn-AX.`

`Phase 4bn-AX selects at most one family for a later docs-only preregistration phase; it does not authorize that preregistration or any execution.`

`No metric, horizon, loss, baseline implementation, model, threshold, block count, covariate list, event definition, or event threshold is authorized by Phase 4bn-AX.`

`Phase 4bn-AY or any other successor requires separate operator authorization and a new Claude Code prompt.`

`CF-1 is selected only as a realized-volatility substrate test; success would not establish directional edge, profitability, or permission to reopen the stopped long-horizon ML arc.`

## 36. Preserved project locks

Unchanged and preserved exactly: `STOP_LONGHORIZON_ML_ARC` and
`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE` (distinct, not merged, softened, reinterpreted, rescued,
or reopened); Phase 4aw `flip_research_eligible(...)` always-raising, never invoked;
`research_eligible = false`; `eligibility_gate_status = pending`; all published authorization flags
false; the Phase 4bn-AE §19 M0 boundary (absolute); the Phase 4ak twelve-clause M0 gate with §6
cooldown and §7 cooled-down families (incl. §7.A directional depletion and §7.D order-flow /
microstructure lane); M0 cooldown and cooled-down-family rules; locked cost 8 bps/side · 16 bps
round-trip; the Phase 4bn-AV evidence ledger, spending-authority standard, and late-inadmissibility
protocol; all dataset identities and hashes; split, holdout, sidecar, and storage policies; every
prior strategy verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1 and the 5m
thread); every retained-evidence classification; and every completed implementation report.
`docs/00-meta/current-project-state.md` is left unchanged by this phase (matching the AH/AI/AJ/AK…AW
docs-only precedent; any additive paragraph would be a separate merge-time decision).
