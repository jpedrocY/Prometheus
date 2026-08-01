# Phase 4bn-BC — CF-1 M0, Evidence-Budget, and Anti-Rescue Audit

Companion governance audit to
`2026-07-31_phase-4bn-bc_cf1-valid-pass-filter-admissibility-and-consequence-assessment.md`.

This audit maps the assessed continuation — a bounded, non-directional research market-state /
volatility-regime filter built from the already-established CF-1 magnitude forecast object — against
the binding Phase 4ak twelve-clause M0 gate, the Phase 4bn-AE §19 boundary, the stopped-arc locks,
the cooldown rules, and the Phase 4bn-AV evidence-budget governance. It **cites** owners; it does not
rewrite, restate as new, amend, or relax any governance document.

Phase 4bn-BC selected Decision A `REJECT_CF1_FILTER_CONTINUATION__REMAIN_PAUSED` and Decision B
`R3 — NO_CF1_RESERVE_PATH_JUSTIFIED__REMAIN_RESERVED`. This audit records the governance basis for
those decisions and confirms that the rejection itself violates nothing and rescues nothing.

Base `main` == `origin/main` == `HEAD` at branch creation:
`7bb6819ad5f1d5aded1746bf3332ad6f4aa5dc49`.

No data, artefact, reserve, network resource, script, test, linter, or type-checker was used
(main memo §6).

## 1. Binding M0 clauses and applicability

**Owner:** `docs/00-meta/m0-mechanism-admissibility-gate.md` (adopted by Phase 4ak; binding
prospective governance; twelve clauses in §5; post-null cooldown in §6; cooled-down families in §7;
required memo template in §8).

**Applicability under M0 §4.A.** The assessed continuation is not a strategy candidate, not a
strategy-spec path, not a backtest-plan path, and proposes no new mechanism source — it reuses the
already-committed aggTrades substrate and the already-frozen CF-1 forecast object. It would, however,
constitute a fresh research hypothesis in the weak sense and it touches the M0 §7.D cooled-down lane.
It is therefore treated here as **M0-relevant** and mapped clause by clause, in the same posture
Phase 4bn-AY §34 adopted for CF-1 itself.

**Applicability under M0 §4.B.** Phase 4bn-BC itself is a docs-only governance and decision phase
that proposes no market mechanism and authorizes nothing; under §4.B it does not need to clear M0 to
record a rejection. The mapping below is performed because the assessed object would have needed it,
not because the rejection does.

**M0 §4.C.** M0 exempts nothing from any other binding governance and authorizes no phase by itself.
Every future phase still requires explicit operator authorization. That is unchanged.

**Key interpretation, recorded explicitly.** The Phase 4bn-BB valid pass does **not** clear strategy
M0. Phase 4bn-BC may determine whether a non-strategy research filter is admissible to preregister —
and has determined that it is not — but Phase 4bn-BC does **not** state, and may not be read as
stating, that CF-1 or any future filter clears strategy M0.

## 2. Clause-by-clause M0 mapping of the assessed continuation

| Clause | Mapping | Finding |
|---|---|---|
| **M0.1 Mechanism source** | Not price-only in the depleted sense: the mechanism source is aggTrades trade-arrival intensity and unsigned traded-volume intensity (`rolling_aggtrade_count_60s`, `rolling_quantity_sum_60s`), already committed on disk, feeding a realized-variance magnitude object. The assessed continuation introduces **no new mechanism source at all**; it re-expresses the CF-1 forecast. | Source admissible; but "no new mechanism source" is itself adverse for a fresh-hypothesis claim. |
| **M0.2 Non-price-only / structurally distinct** | The substrate is trade-tape, not price-only, so §7.A depletion is not engaged. However, relative to Phase 4bn-BB the assessed object is a **coarsening of the same forecast under the same features, target, model, loss, horizon, and split** — it is not structurally distinct from the experiment already run. M0.2 requires structural distinctness stated in theoretical terms before any data is touched; a discretization of an already-tested comparison does not supply it. | **ADVERSE.** |
| **M0.3 Baseline-superiority theory (non-strategy route)** | CF-1 used the M0.3 "equivalent baseline differential for non-strategy mechanism claims" route (Phase 4bn-AY §34), discharged by the P1/P2/P3 predicate (strict positivity, ≥ 6/7 block consistency, bootstrap `LB_95 > 0`) rather than a predicted Δ_R magnitude. The same predicate form is available to a state object, so M0.3 is **satisfiable in form**. It is not satisfiable in substance without a theoretical reason to expect a state-level differential that is not simply the already-observed `ρ = 0.036651473671709504` restated — and using that observed value would be prohibited post-hoc selection. | Satisfiable in form; hollow in substance. |
| **M0.4 Rejection-topology distance** | Distance from R2 (cost fragility), F1 (mean-reversion overextension), D1-A (funding-aware contrarian), V2 (participation-confirmed breakout), G1 (regime-first breakout continuation), C1 (volatility-contraction expansion breakout): all six are **directional strategy candidates with entry, exit, sizing, and PnL**. The assessed object has no sign, no entry, no exit, no position, and no PnL. **Closest prior failure trap: G1** — a regime-first construct whose gate was to condition trading. The structural distinction is that G1's regime existed to gate entries, whereas the assessed object is barred from gating anything. | Distance adequate **only** while the no-gating bar holds; the trap is real and is the reason the bar is restated absolutely. |
| **M0.5 Cost realism under §11.6 (8 bps/side, 16 bps round trip)** | **Non-decision-bearing here, and explicitly so.** The assessed object generates no trade, so it incurs no cost and clears no cost. That is not a pass: it means the clause cannot be discharged at all on aggTrades-only evidence. Phase 4bn-AE §19 records that aggTrades-only data cannot support spread, slippage, executable mid, depth, or impact; Phase 4bn-AS §31 records the same. The locked 8/16 bps reference is preserved as descriptive context and entered no Phase 4bn-BB target, model, loss, threshold, weighting, or verdict. | Not applicable to a non-trading research object; **remains an absolute blocker for any trading path**. |
| **M0.6 Opportunity rate** | Not applicable to a non-strategy object: there is no candidate event, no joint trigger, and no per-OOS-window trade count. Justification in one sentence, per M0 §5: the object produces labels, not trades. | Not applicable. |
| **M0.7 Edge rate** | Discharged in the CF-1 manner by an equivalent descriptive edge-rate predicate rather than a Δ_R (M0.7 permits "predeclared IC floor; predeclared median-spread floor; predeclared outperformance-fraction floor" or equivalent). M0.7's explicit recognition that **opportunity-rate viability is not edge-rate viability** applies here in a transposed form: *forecast-skill viability is not decision-relevance viability*. Phase 4bn-BB established forecast skill; it did not establish that the skill changes any state characterization. | Satisfiable in form; the transposed distinction is precisely what the main memo §13 finds unmet. |
| **M0.8 Data availability and integrity** | **PASS.** The required data — the 244-date non-reserve BTCUSDT aggTrades normalized and feature partitions — is already built, on disk, sidecar-verified, and non-reserve. No acquisition is required or implied. No blocked or unavailable source is required. | Pass. |
| **M0.9 Governance compatibility** | Compatible on its face with §11.6, §1.7.3, Phase 3r §8, Phase 3v §8, Phase 3w §6/§7/§8, Phase 4j §11, the M0 document itself, and the §6 cooldown, **because it proposes no trading, no position, no stop, and no metrics/OI use**. Compatibility is achieved by inaction rather than by clearance. | Compatible; not clearance. |
| **M0.10 Forbidden-rescue and anti-reduction** | The assessed object does not reduce to V2 / G1 / C1 / R2 / R1a / R1b-narrow / F1 / D1-A / rank-then-breakout / multi-position / 5m variants / alt-symbol reruns — it has no direction and no position. **Closest rescue trap: a "volatility-regime filter" becoming G1-style regime gating under a research name.** The structural reason it is not that trap is that every gating consumer is prohibited absolutely (Phase 4bn-AE §19) and the object is barred by construction from conditioning any action. Naming is not sufficient and the structural argument is supplied — but the trap's proximity is a standing hazard, and closing the continuation removes it. | Not a rescue as scoped; hazard real. |
| **M0.11 Pre-backtest falsification** | A state-level proper-score or disagreement-rate predicate would be predeclarable, substantive, and capable of terminating the candidate at the docs-only or analysis stage, distinct from downstream catastrophic-floor predicates. | Satisfiable. |
| **M0.12 Post-null cooldown and non-authorization** | The assessed object touches the M0 §7.D microstructure / order-flow / liquidity-timing lane, status `NOT_RECOMMENDED_NOW`. It asserts **no** §6.A "materially new mechanism source" — it introduces no new observable and derives from no new external theory. It relies on the same §7.D posture CF-1 relied on (M0.8 data already on disk; object is magnitude, not short-horizon direction). Passing M0 would authorize no strategy-spec, backtest-plan, backtest, paper/shadow, live-readiness, deployment, exchange-write, credentials, or successor phase. | §7.D not relaxed; no materially-new source asserted; **ADVERSE** for a fresh-hypothesis claim. |

**M0 mapping result.** The assessed continuation is not M0-inadmissible in the way the Phase 4bn-AX
forced-flow family was (which failed M0.2, M0.4, M0.8, M0.10, and M0.12 outright). It is
**M0-permissible in form but adverse on M0.2 and M0.12 and hollow on M0.3/M0.7 in substance**: it
introduces no new mechanism source, is not structurally distinct from the experiment already run, and
cannot state an expected differential without either inventing one or reading it off the observed
Phase 4bn-BB result. This is consistent with, and reinforces, the decision-consequence rejection in
the main memo §13; it is not an independent second basis for it.

## 3. Explicit statement — strategy M0 is not cleared

**Strategy M0 is not cleared.** The Phase 4bn-BB `CF1_VALID_PASS` does not clear strategy M0, did not
attempt to, and cannot. Phase 4bn-BC does not clear strategy M0 and makes no such claim for CF-1 or
for any future filter object. Any strategy, signal, PnL, backtest, paper, shadow, live, or
exchange-write path requires its own separate M0-style mechanism-admissibility memo clearing all
twelve clauses — including M0.5 cost realism at the locked 8 bps/side · 16 bps round trip, execution
feasibility, and slippage/spread assumptions — plus its own separate operator authorization.

`research_eligible = false`; `eligibility_gate_status = pending`; all authorization flags remain
`false`; the Phase 4aw always-raising `flip_research_eligible(...)` behaviour is preserved and was not
invoked.

## 4. Phase 4bn-AE §19 mapping

**Owner:** `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-ae_ml-baseline-preregistration-contract-amendment.md`
§19.

§19 states that **no result, however strong**, authorizes strategy construction, signal generation,
threshold trading, confidence-gated trading, backtesting, PnL computation, position sizing, execution
logic, live-readiness, paper/shadow trading, or exchange-write; and that any path toward those
requires a separate M0-style memo clearing M0.5 cost realism at 8/16 bps, execution feasibility,
slippage/spread assumptions (which aggTrades-only data cannot support), label economic relevance,
strategy admissibility against the retained rejections, the M0 §7.D `NOT_RECOMMENDED_NOW` posture,
and the Phase 4al no-rescue constraints. §19 declares the boundary **absolute** and not softened by
any baseline metric.

Mapping:

- The Phase 4bn-BB valid pass is a metric result. §19 explicitly denies that any metric result
  softens the boundary. The boundary is therefore exactly where it was before Phase 4bn-BB.
- Two of §19's named prohibitions — **threshold trading** and **confidence-gated trading** — are the
  precise failure modes a "volatility-regime filter" would collapse into if it were ever permitted to
  condition an action. This is why the main memo §10 defines the admissible object exclusively as a
  research market-state label and enumerates every prohibited consumer.
- Because aggTrades-only evidence cannot establish executable spread, slippage, executable mid,
  depth, impact, or execution feasibility, §19 remains an **absolute** blocker for every strategy /
  PnL path regardless of the CF-1 outcome. Phase 4bn-AS §31 and Phase 4bn-AT §59 record the same
  boundary in identical terms.

**Result: Phase 4bn-AE §19 is preserved, unsoftened, and undiminished by Phase 4bn-BB, by its merge,
and by Phase 4bn-BC.**

## 5. Long-horizon stop mapping

**Owner:** Phase 4bn-AS (`STOP_LONGHORIZON_ML_ARC`), with lineage through Phase 4bn-AK.

| Test | Finding |
|---|---|
| Does the assessed continuation use any long-horizon directional label family (`microstructure_labels_longhorizon_aggtrades_v001`; 5m / 30m / 1h `forward_direction_<H>`)? | **No.** CF-1 uses no label family at all; it constructs its own non-directional realized-variance target from price. |
| Does it re-fit, relax, recalibrate, reweight, or re-threshold the stopped classifier? | **No.** The frozen object is a 6-parameter OLS HAR extension. |
| Does it change the target to escape the stopped arc's observed failure (the Phase 4bn-AS §24 "result rescue" pattern)? | **No.** The magnitude target was fixed at Phase 4bn-AY §14/§15, before Phase 4bn-BB and independently of the stopped arc's forensics. |
| Does it use the consumed pre-v002 holdout as confirmation? | **No.** It is `CONSUMED`, unopened, and descriptive-only. |
| Does rejecting the continuation reopen, soften, merge, or reinterpret the stop? | **No.** A rejection cannot reopen a stop. |

**`STOP_LONGHORIZON_ML_ARC` is preserved exactly and unchanged.**

## 6. Top-of-book stop mapping

**Owner:** Phase 4bn-AT (`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`); ledger entry
`HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE`.

| Test | Finding |
|---|---|
| Does the assessed continuation use or propose bookTicker, top-of-book, order-book, depth, quote, or midpoint data? | **No.** |
| Does it propose prospective capture as a substitute for the inadmissible retrospective source? | **No.** Phase 4bn-AT records that prospective capture cannot retroactively answer the historical question; nothing here relies on it. |
| Does it revive the bounce-versus-midpoint mechanism question? | **No.** The object is realized-variance magnitude, not label-measurement validity. |
| Does any Phase 4bn-BC statement revise the locked 8/16 bps reference or any completed verdict? | **No.** Phase 4bn-AT §58 forbids this; nothing here does it. |

**`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE` and `HIST_TOB_BOOKTICKER_SOURCE =
INADMISSIBLE_OR_UNAVAILABLE` are preserved exactly and unchanged.**

## 7. Proxy-rescue rejection mapping and §7.D boundedness

**Owner:** Phase 4bn-AX (`REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`, the forced-flow /
liquidation-cascade family).

| Test | Finding |
|---|---|
| Is a proxy substituted for an inadmissible source? | **No.** No liquidation marker, forced-flow event, aggressor-imbalance construct, or `liquidation`-token feature is introduced; the committed feature schema forbids the `liquidation` token outright. |
| Is a threshold-plus-relabel applied over already-tested aggressor/burst features toward a depleted directional target? | **No.** The retained features are two sign-invariant accumulators; the target is non-directional. |
| Would the assessed object re-open the forced-flow family under a new name? | **No.** It has no event definition, no one-sidedness construct, and no directional drift target. |

**M0 §7.D relationship, bounded explicitly.** The microstructure / order-flow / liquidity-timing lane
is `NOT_RECOMMENDED_NOW`, for heavy data burden, high cost-realism risk at short horizons, and not
being strengthened by any prior Prometheus finding. Its two named requirements are M0.5 (cost realism)
and M0.8 (data feasibility) on theoretical content before any acquisition. The bounded relationship
is:

- **M0.8 is PASS** — the required aggTrades data is already built, on disk, sidecar-verified, and
  non-reserve; no acquisition is required or implied by anything in this phase.
- **M0.5 is not discharged and cannot be** on aggTrades-only evidence; it is non-decision-bearing for
  a non-trading research object precisely because that object generates no trade, and it remains an
  absolute blocker for any trading path.
- **§7.D is not relaxed, reinterpreted, narrowed, or cleared** by Phase 4bn-BB, by its merge, or by
  Phase 4bn-BC. No §6 / §6.A "materially new mechanism source" is asserted. The lane's
  `NOT_RECOMMENDED_NOW` status stands.

**`REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH` is preserved exactly and unchanged.**

## 8. Cooldown and cooled-down-family analysis

**Owner:** M0 §6 (post-null cooldown rule), §6.A ("materially new" definition), §6.B (what the
cooldown does not block), §6.C (no implicit decay), §7 (current cooled-down families).

| Family | Status | Engagement by the assessed continuation |
|---|---|---|
| §7.A Price-only single-symbol directional continuation | `DEPLETED / NOT_RECOMMENDED` | **Not engaged.** The object is non-directional and trade-tape-based, not price-only directional. |
| §7.B Cross-sectional trend / relative-strength under Phase 4ai descriptors | `COOLED_DOWN_AFTER_NOT_SUPPORTED` | **Not engaged.** Single symbol; no ranking, no composite, no rebalancing, no symbol-universe expansion. |
| §7.C Derivatives-context directional lane | `CONDITIONAL_ONLY / HIGH_D1-A_RESCUE_RISK` | **Not engaged.** No funding, no open interest, no calendar covariate; Phase 4bn-AX §23 kept CF-3 unbundled and that non-bundling is preserved. |
| §7.D Microstructure / order-flow / liquidity-timing | `NOT_RECOMMENDED_NOW` | **Engaged and bounded** per §7 above. Not relaxed. |
| §7.E Mark-price stop-domain / execution-realism | `NOT_RECOMMENDED_NOW` | **Not engaged.** No stop domain, no execution-realism object. |

**§6 cooldown compliance.** No cooled-down family is reopened by parameter, descriptor, threshold,
symbol-universe, interval, forward-horizon, filter-relaxation, weight-reassignment, or
rebalance-frequency adjustment. No §6.A materially-new mechanism source is claimed. §6.C is respected:
no cooldown has decayed with time, and none is treated as decayed. §6.B is respected in the permitted
direction only — this phase reads and cites prior stopped-arc reports as historical documentation,
which the cooldown explicitly does not block.

**Cooldown result: no cooled-down family is reopened, relaxed, or reinterpreted.**

## 9. Evidence-ledger states

**Owner:** `docs/00-meta/process/evidence-budget-ledger.md` (status index) and
`docs/00-meta/process/scarce-reserve-spending-and-late-inadmissibility-standard.md` (change of
status). Neither document authorizes any spend, and neither is modified by this phase.

| `evidence_id` | Status | Change by Phase 4bn-BC |
|---|---|---|
| `PRE_V002_INTERNAL_HOLDOUT` | `CONSUMED` | None. Terminal under ledger §2 and §3.3; may never return to `UNTOUCHED_RESERVED` and may never be represented as independent confirmation. Not opened. |
| `V002_TERMINAL_WINDOW` | `UNTOUCHED_RESERVED` | None. Not read, loaded, inspected, enumerated for content, scored, or sampled. |
| `V002_SEALED_TEST` | `UNTOUCHED_RESERVED` (highest protection) | None. Not read, loaded, inspected, enumerated for content, scored, or sampled. `test_rows_loaded = 0` preserved. |
| `HIST_TOB_BOOKTICKER_SOURCE` | `INADMISSIBLE_OR_UNAVAILABLE` | None. Not a reserve; not spendable; not silently substituted. |

**No ledger row is added, edited, or deleted by Phase 4bn-BC, and no transition-history row is
appended,** because no status changed. Under ledger §3.1 a same-branch ledger update is required only
for a phase that proposes or completes a spend; Phase 4bn-BC does neither.

## 10. Reserve hierarchy

Per the scarce-reserve standard §10, applied highest-burden-last:

- **§10.A Consumed evidence** — `PRE_V002_INTERNAL_HOLDOUT`. Descriptive use with correct provenance
  only; never independent confirmation; cannot return to untouched status.
- **§10.B Terminal reserve** — `V002_TERMINAL_WINDOW`. May be considered only after all development
  and model-selection choices are frozen, and only under the full pre-spend sequence (§12) and quorum
  (§8); one named question and one predeclared run; no tuning after viewing.
- **§10.C Sealed test** — `V002_SEALED_TEST`. Final, highest-protection, single-use. May be
  considered only after terminal evidence supports promotion under existing gates; cannot be used for
  exploration, debugging, threshold selection, model comparison, calibration, or rescue; proposal and
  authorization must occur in **separate phases**; spending it implies and creates **no** second
  sealed test.

No new reserve is invented and no ordinary data is designated as sealed.

## 11. Reserve-proportionality assessment

The question is whether a future terminal-window confirmation of the CF-1 magnitude result would be
proportionate. It would not.

- **Decision consequence.** A confirmed CF-1 magnitude result would authorize nothing: every
  downstream consumer is barred by Phase 4bn-AE §19 and by the unmet twelve-clause M0 gate for any
  strategy path. Standard §11 lists "unclear decision consequence" as an automatic refusal condition.
- **Negative-result value.** A terminal-window null would say the development-level improvement did
  not reproduce out of time. That is informative, but it would close a lane that Phase 4bn-BC has
  already closed on decision-consequence grounds at zero evidence cost. Standard §11 lists "no
  valuable negative result" as an automatic refusal condition.
- **Proportionality.** The reserve is scarce, irreplaceable, and one-shot. Phase 4bn-AS §25 refused a
  scarce-reserve spend to confirm a sub-threshold, non-actionable finding, reasoning that spending a
  one-shot asset on a result that would remain non-actionable even if confirmed is a poor allocation.
  The same reasoning applies with equal force here. Standard §11 lists "missing cost / engineering
  proportionality" as an automatic refusal condition.
- **Development-level status.** Phase 4bn-AY §20 and §31 state that a development-level pass is not
  reserve-confirmed evidence. That gap is real, but a gap in evidence class is not by itself a reason
  to spend the only asset that could close it.

**Reserve-proportionality result: a CF-1 terminal-reserve proposal would not be proportionate.
Decision B is `R3 — NO_CF1_RESERVE_PATH_JUSTIFIED__REMAIN_RESERVED`.**

## 12. Pre-spend quorum

**Not applicable.** R3 is selected, so no reserve-spend proposal exists, is drafted, or is
recommended, and the pre-spend quorum is not engaged.

For completeness and without adopting, restating as new, or amending it: the quorum remains owned by
the scarce-reserve standard §7, §8, and §12 — one explicit human-operator approval, valid only when
both mandatory advisory prerequisites exist (a repository-grounded ChatGPT compliance recommendation
and one bounded independent critical-review memorandum from a reviewer distinct from the execution
agent, produced under the §15 bounded-context standard), following a committed docs-only proposal
satisfying the §9 contract, with a separate Claude Code execution prompt created only after approval,
an execution-phase preflight under §13, and a post-spend ledger transition under §14. **AI agents
cannot self-authorize reserve access** (standard §6). Phase 4bn-BC creates no reserve proposal of any
kind.

## 13. Sealed-test boundary

The sealed test is the project's highest-protection reserve and its only remaining single-use final
holdout. A terminal-window result would **not** automatically authorize it. Spending it would require
a later, separately justified proposal, made only after terminal evidence supported promotion under
existing gates, under the strictest form of the pre-spend sequence, with proposal and authorization in
**separate phases**, and with an explicit statement of what project decision changes on pass or fail
and an explicit post-spend stop posture. Spending it creates no replacement.

`V002_SEALED_TEST remains UNTOUCHED_RESERVED.` `test_rows_loaded = 0` is preserved. Phase 4bn-BC
creates no sealed-test proposal.

## 14. Anti-rescue checklist

| Anti-rescue test | Finding |
|---|---|
| Is Phase 4bn-BC a rerun, continuation, or repair-in-place of Phase 4bn-BB? | **No.** No value is recomputed, reinterpreted, or reclassified; the runner was not invoked in any mode. |
| Is any Phase 4bn-BB guard relaxed, widened, or made conditional? | **No.** The `> 1e10` condition guard, rank guard, zero-variance guard, non-finite guard, `≥ 100` block minimum, and `≥ 60` training minimum are untouched. |
| Is a remedy, variant, or successor selected after seeing the result? | **No.** No successor, variant, mapping, threshold, regime count, comparator, or consequence rule is selected. The continuation is closed, not redirected. |
| Is the CF-1 lane rescued through another feature, horizon, model, or filter family? | **No.** Per Phase 4bn-AY §30, no neighbouring variant is authorized, and none is proposed here. |
| Is a stopped arc reopened, softened, merged, reinterpreted, or continued? | **No.** §5, §6, §7 above. |
| Is a proxy substituted for an inadmissible source? | **No.** §7 above. |
| Is an adverse block, month, date, or subgroup excluded, reweighted, or reordered? | **No.** No subgroup, month, or block is selected; the reachability hazard is recorded in main memo §15 and prohibited. |
| Is the Phase 4bn-BB pass converted into a trading, economic, or materiality claim? | **No.** Main memo §21 records every such claim as `NOT_SUPPORTED`, `NOT_ESTABLISHED`, or `NOT_CLEARED`. |
| Is a consumed reserve relabelled as independent? | **No.** `PRE_V002_INTERNAL_HOLDOUT` remains `CONSUMED`. |
| Could the rejection itself be a disguised rescue (closing to avoid a falsifying test)? | **No.** The rejection closes the only continuation available and authorizes nothing in its place; it forfeits an outcome rather than preserving one. |

**Anti-rescue verdict: PASS.**

## 15. Anti-duplication checklist

| Duplication test | Finding |
|---|---|
| Does Phase 4bn-BC duplicate a committed governance document? | **No.** It cites owners and creates no standard, ledger, gate, register, or policy. |
| Does Phase 4bn-BC restate or amend M0, Phase 4bn-AE §19, the ledger, or the scarce-reserve standard? | **No.** Each is cited by owner and left unmodified. |
| Would the assessed continuation duplicate the Phase 4bn-BB experiment? | **Substantially yes** — it is a coarsening of the same nested comparison under the same target, features, model, loss, horizon, and split. This is recorded as adverse under M0.2 and is the substance of main memo §13(c). |
| Would it duplicate a previously stopped or rejected family? | **No** — not the long-horizon ML arc, not the ToB arc, not the forced-flow family. |
| Would it duplicate the prohibited Phase 4bn-AY three-feature contract? | **No.** That set remains `STRUCTURALLY_NON_IDENTIFIABLE__PROHIBITED_FOR_FUTURE_EXECUTION` and `rolling_quantity_mean_60s` remains prohibited. |
| Is empirical correlation, distributional overlap, or any data property used as a criterion anywhere in this phase? | **No.** No data was opened; no data property was measured or relied upon. |

**Anti-duplication verdict: PASS for Phase 4bn-BC's own conduct; ADVERSE for the assessed
continuation, consistent with the M0.2 finding.**

## 16. Researcher-freedom assessment

- **Freedom actually exercised by Phase 4bn-BC: none.** No threshold, regime boundary, regime count,
  mapping, transformation, comparator, state criterion, subgroup, block, month, or consequence rule is
  selected. No choice of regime count is forced by binding prior governance, and none is made. No
  row-level prediction was inspected.
- **Freedom that a future object would have carried.** Committed governance forces no regime count,
  no mapping family, no state-level criterion, and no comparator. Unlike CF-1 — whose baseline
  (HAR-RV), loss (QLIKE), horizon, and cadence were each anchored in canonical external theory or
  committed support at Phase 4bn-AY §14–§22 — no canonical external form anchors a state object.
- **Contamination surface.** The committed Phase 4bn-BB record contains no forecast-scale value, so a
  train-only quantile mapping could not be reverse-engineered from `main`; but the per-block `D_i`
  table is now permanently visible, making subgroup and block-ordering contamination **reachable**
  where it previously was not. Phase 4bn-AY §29 already prohibits post-hoc block exclusion and
  block-boundary adjustment; the prohibition is restated, not relaxed.

**Researcher-freedom result: boundable but not forced; adverse, and compounding the
decision-consequence finding rather than substituting for it.**

## 17. Decision-consequence test (governance form)

| Test | Result |
|---|---|
| Materially different question from Phase 4bn-BB? | **Not materially** — a coarsening of the same nested comparison. |
| Does pass materially change the project state? | **No** — every consumer of a market-state label is barred by Phase 4bn-AE §19 and the unmet M0 gate. |
| Does fail materially change the project state? | **Not cleanly** — confounded between "no decision-relevant information" and "information lost to discretization". |
| Is it repackaging the known `ρ = 0.036651473671709504` result? | **Substantially yes.** |
| Is the residual content scientifically useful without a trading claim? | **Marginally at best** — descriptive. |
| Does the expected decision-relevant information gain justify a further evidence-opening arc? | **No** — the Phase 4bn-AS §26 and Phase 4bn-AT §49/§54 cost/benefit gates both fail on weaker prospective gains than those precedents rejected. |

## 18. Strongest governance counterargument, and response

**Counterargument.** Phase 4bn-AX §14 and Phase 4bn-AY §31 predeclared, before any data existed, that
a valid pass would permit a bounded non-directional filter assessment. Refusing the continuation after
a positive result can be read as governance drift: the project set a consequence in advance and then
declined it once the antecedent fired. The scarce-reserve standard §19 and M0.10 exist to stop
outcome-driven changes of course; a rejection reached after seeing a favourable result is exactly the
shape those rules distrust. Furthermore, every structural item on the Option-A checklist is `NO`, and
the anti-post-hoc position is objectively defensible because the committed record carries no
forecast-scale information — so the continuation could have been preregistered cleanly.

**Response.** The predeclaration does not bind toward continuation. Its exact words permit "a
separately-authorized docs-only decision phase **assessing whether** the forecast **could** support"
such a filter. That is a question with two admissible answers, and Phase 4bn-BC is the phase
authorized to answer it. Declining on the **same criterion that selected CF-1 in the first place** —
decision consequence, which Phase 4bn-AX §28 named as decisive — is continuity, not drift. Governance
drift would be the reverse: relaxing a boundary, softening a stop, adopting a materiality threshold
that was explicitly never adopted, or reading a magnitude result as authorization. None of that
occurs. Nothing is relaxed, no lock moves, no ledger row changes, no flag flips, no claim is upgraded,
and no evidence is spent. And the outcome-driven-change concern points the other way here: the
decision **forfeits** a possible favourable outcome and authorizes nothing in its place, which is the
opposite of the rescue shape that M0.10 and standard §19 exist to prevent. That the continuation
*could* have been preregistered cleanly establishes admissibility, not desirability; admissibility is
necessary and not sufficient, and §17 is where it fails.

## 19. Final audit verdict

- **M0 mapping:** performed clause by clause. The assessed continuation is M0-permissible in form,
  **adverse on M0.2 and M0.12**, hollow on M0.3 / M0.7 in substance, and PASS on M0.8. §7.D is
  engaged, bounded, and not relaxed.
- **Strategy M0:** **NOT CLEARED**, and not claimed to be cleared for CF-1 or for any future filter.
- **Phase 4bn-AE §19:** preserved, absolute, unsoftened.
- **`STOP_LONGHORIZON_ML_ARC`:** preserved exactly.
- **`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`:** preserved exactly.
- **`REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`:** preserved exactly.
- **Cooldown / cooled-down families:** no family reopened, relaxed, or reinterpreted.
- **Evidence ledger:** unchanged; no row added, edited, or deleted; no transition appended.
- **Reserve posture:** `R3 — NO_CF1_RESERVE_PATH_JUSTIFIED__REMAIN_RESERVED`; no reserve opened or
  spent; no proposal created; pre-spend quorum not engaged.
- **Anti-rescue:** PASS. **Anti-duplication:** PASS for this phase; ADVERSE for the assessed
  continuation. **Researcher freedom:** boundable but not forced; adverse.
- **Decision consequence:** fails, and is the decisive basis for Decision A.

```
PHASE_4BN_BC_GOVERNANCE_AUDIT_PASSED__FILTER_CONTINUATION_NOT_ADMISSIBLE_ON_DECISION_CONSEQUENCE__STRATEGY_M0_NOT_CLEARED__ALL_STOPS_AND_LOCKS_PRESERVED__NO_RESERVE_OPENED_OR_SPENT
```

`No evidence reserve is opened or spent by Phase 4bn-BC.`

`No direction, signal, strategy, position sizing, entry/exit logic, PnL, backtest, paper, shadow, live, or exchange-write authorization follows from Phase 4bn-BC.`
