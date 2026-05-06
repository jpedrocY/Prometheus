# Phase 4al — Exit Architecture / Trade-Management M0 Admissibility Memo

## 1. Purpose and Non-Authorization

Phase 4al is a **docs-only governance / admissibility memo**.

Phase 4al asks one question and answers it under the now-binding
M0 mechanism-admissibility gate adopted by Phase 4ak:

```text
Is "exit architecture / trade management / payoff-distribution
shaping" admissible as a possible future research lane under the
binding twelve-clause M0 gate and the binding post-null cooldown
rule?
```

Phase 4al is **not** an analysis phase, **not** a backtest, **not** a
backtest-logic audit, **not** a strategy spec, **not** a hypothesis-
spec memo, and **not** a discovery memo. It does not authorize any
successor phase.

Phase 4al explicitly does **NOT**:

- acquire data,
- download data,
- call APIs,
- call exchange data endpoints,
- call `data.binance.vision`,
- modify raw or normalized data,
- create or modify any manifest,
- create `v003` or any other dataset version,
- run any analysis,
- run any backtest,
- run any strategy diagnostic,
- rerun the Q1–Q7 5m diagnostic question set,
- run any backtest-logic audit,
- compute strategy PnL,
- compute entry / exit returns,
- compute MFE / MAE / time-to-MFE / time-to-stop distributions,
- compute realized-R-after-costs accounting,
- create a cumulative equity curve or trade ledger,
- optimize any parameter,
- select thresholds for any future strategy,
- create a new strategy candidate,
- name a new strategy candidate,
- create a fresh-hypothesis discovery memo,
- create a hypothesis-spec memo,
- create a strategy-spec memo,
- create a backtest-plan memo,
- modify `src/prometheus/`, tests, or scripts,
- modify any backtest script (Phase 4l, Phase 4r, Phase 4x, or any
  other),
- implement any runtime path,
- imply live-readiness,
- enable exchange-write capability,
- request or create production keys,
- touch MCP, Graphify, `.mcp.json`, or credentials,
- revise any retained verdict,
- change any project lock,
- relax §11.6, §1.7.3, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 /
  §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, or
  Phase 4w,
- broaden Phase 4ac results beyond data / integrity evidence,
- broaden Phase 4ad Rules A / B / C beyond prospective analysis-time
  scope,
- broaden Phase 4ae / Phase 4af / Phase 4ag / Phase 4ah / Phase 4ai
  findings beyond their prior scopes,
- broaden Phase 4aj recommendations beyond the specific revised M0
  and post-null cooldown rule already adopted by Phase 4ak,
- broaden Phase 4ak adoption beyond §5–§8 of the durable M0
  document,
- adopt the full Phase 4z 32-item framework as binding governance,
- adopt the Phase 4z M0–M7 mechanism-check redesign wholesale,
- adopt the Phase 4aa admissibility framework as binding governance,
- adopt Phase 4ab recommendations as binding governance,
- authorize Phase 4am / Phase 5 / Phase 4 canonical / any successor
  phase.

## 2. Scope

Phase 4al is **text-only**. It is the project's first M0-driven
admissibility decision after the Phase 4ak adoption boundary.

Phase 4al is bounded as follows:

- **In scope.** A clause-by-clause M0 admissibility assessment of
  the candidate research lane defined in §5 below. Determination of
  whether (and under what boundaries) the lane may be proposed for
  a future, separately-authorized analysis-and-docs phase. A
  refined statement of the no-rescue rule for this specific lane.
  Definition of the maximum allowable scope for any future
  Phase 4am, *if* the operator ever authorizes one.

- **Out of scope.** Any forensic computation, any backtest-logic
  audit, any MFE / MAE / time-to-event computation, any realized-R-
  after-costs accounting, any cost-in-R decomposition, any
  intrabar-ambiguity audit, any new strategy candidate, any rescue
  of any historical candidate, any data acquisition, any code
  change, any manifest change, any successor authorization.

## 3. Authority and Inputs Reviewed

Phase 4al treats repository Markdown as authoritative and reads
inputs verbatim. It does not paraphrase governance.

Inputs reviewed:

- `docs/00-meta/current-project-state.md` (post-Phase-4ak
  refresh; latest `main` SHA `9abf1bd`).
- `docs/00-meta/m0-mechanism-admissibility-gate.md` (the durable
  twelve-clause M0 gate, the post-null cooldown rule, the cooled-
  down families list, and the M0 memo template — read verbatim).
- `README.md` and `docs/README.md` (post-Phase-4ak status).
- `docs/00-meta/implementation-reports/2026-05-04_phase-4ak_m0-
  governance-adoption.md`.
- `docs/00-meta/implementation-reports/2026-05-04_phase-4aj_m0-
  governance-reconciliation.md`.
- `docs/00-meta/implementation-reports/2026-05-04_phase-4ai_single-
  position-cross-sectional-trend-analysis.md`.
- `docs/00-meta/implementation-reports/2026-05-04_phase-4ah_single-
  position-cross-sectional-trend-feasibility.md`.
- `docs/00-meta/implementation-reports/2026-05-04_phase-4ag_research-
  program-pivot-mechanism-source-triage.md`.
- The retained verdict ledger (H0 / R3 / R1a / R1b-narrow / R2 /
  F1 / D1-A / V2 / G1 / C1) preserved in the current project state.
- The binding project locks: §11.6 = 8 bps per side; round-trip =
  16 bps; §1.7.3 (0.25% risk per trade; 2× leverage cap; one
  position max; mark-price stops where applicable); Phase 3r §8;
  Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k;
  Phase 4p; Phase 4q; Phase 4v; Phase 4w.
- The Phase 4ai null result (`NOT_SUPPORTED` on the predeclared
  five-symbol cross-sectional ranking lane).
- The Phase 4ak adoption boundary (M0 §5 + post-null cooldown §6 +
  cooled-down families §7 + memo template §8 are binding
  prospective governance; the rest of the Phase 4z proposal remains
  recommendation only).

## 4. Triggering Context

Phase 4ak left the project in a clean adoption posture:

- M0 is binding for any future research phase within §4.A of the
  M0 document.
- The cooled-down families list (§7 of the M0 document) currently
  includes:
    - 7.A price-only single-symbol directional continuation —
      `DEPLETED / NOT_RECOMMENDED`,
    - 7.B cross-sectional trend / relative-strength symbol-selection
      under Phase 4ai descriptors — `COOLED_DOWN_AFTER_NOT_SUPPORTED`,
    - 7.C derivatives-context directional lane —
      `CONDITIONAL_ONLY / HIGH_D1-A_RESCUE_RISK`,
    - 7.D microstructure / order-flow / liquidity-timing —
      `NOT_RECOMMENDED_NOW`,
    - 7.E mark-price stop-domain / execution-realism —
      `NOT_RECOMMENDED_NOW`.
- No successor phase is authorized.
- The recommended state is **remain paused** unless the operator
  separately authorizes a future phase.

The operator separately authorized Phase 4al in order to test the
M0 gate on a candidate lane that the project has *not* previously
analyzed in its own right: **payoff management as the unit of
research, distinct from direction prediction**. This memo is the
first M0 admissibility application after the gate became binding.

## 5. Candidate Mechanism Definition

The candidate research lane evaluated by Phase 4al is named:

```text
exit architecture / trade management / payoff-distribution shaping
```

**Definition (precise).** The candidate lane proposes that
Prometheus has, to date, under-modeled the post-entry path of
trades and the realized-R distribution of exits, and that a
predeclared, descriptive forensic / backtest-logic-audit research
lane focused on this domain may yield project value. The candidate
mechanism is **payoff-distribution shaping based on predeclared
post-entry path behavior**, including all of the following as
descriptive / measurement variables:

- maximum favorable excursion (MFE),
- maximum adverse excursion (MAE),
- time-to-MFE,
- time-to-stop,
- target-before-stop sequencing,
- adverse excursion (intrabar and bar-level),
- favorable excursion (intrabar and bar-level),
- volatility expansion after entry (path-realized volatility),
- stagnation (low-realized-range path segments),
- partial exits (descriptive only; not authorized as a strategy
  rule by this memo),
- break-even movement (descriptive only; same disclaimer),
- trailing exits (descriptive only; same disclaimer),
- time exits (descriptive only; same disclaimer),
- realized R after costs,
- fee-in-R, slippage-in-R, funding-in-R decomposition,
- intrabar ambiguity (same-bar stop / TP sequencing),
- mark-price stop behavior where applicable.

**What the candidate lane is not.** The candidate lane is **not**
direction prediction. It is **not** a new entry mechanism. It is
**not** a strategy candidate. It is **not** a hypothesis about when
to enter, what to enter, or which symbol to enter. It does **not**
propose to make Prometheus better at forecasting price direction.

**What the candidate lane proposes (in research terms).** Two
sub-claims, evaluated separately under M0:

- **Sub-claim A — backtest-logic audit.** The historical backtest
  scripts (Phase 4l, Phase 4r, Phase 4x) implement specific cost,
  slippage, funding, stop / TP sequencing, mark-price-domain, and
  intrabar-ambiguity rules. A predeclared audit may verify that
  realized R after costs is being computed correctly, identify any
  measurement defects, and report a clean-bill or a defect list.
  No verdict revision; no parameter optimization; no successor
  authorization implied.

- **Sub-claim B — exit-path forensic analysis.** A predeclared
  descriptive analysis of the realized payoff distribution of the
  retained-evidence trade populations (R1a, R1b-narrow, R2, F1,
  D1-A, V2, G1, C1) — MFE, MAE, time-to-MFE, time-to-stop, target-
  before-stop sequencing — to characterize *what already happened*
  in those trade populations, without converting the description
  into a new strategy candidate or revising any historical verdict.

Both sub-claims are evaluated in §7 against M0.

## 6. Important Framing Constraints

Phase 4al **must** preserve the following framing, which is the
operator's explicit framing for the lane:

> "We are not trying to rescue failed entries. We are asking whether
> Prometheus has under-modeled payoff management."

The framing implies a set of binding statements that any future
work in this lane must respect.

### 6.A Risk:reward is not edge by itself

A high nominal target-to-stop ratio does not constitute edge.
Realized R after costs is the unit. A fixed +2.0R target with a
−1.0R stop is not "+2 expected R" — it is a payoff geometry whose
expected value depends entirely on the joint distribution of
realized path outcomes.

### 6.B Exit architecture cannot manufacture a signal where none exists

If the entry mechanism has zero directional content, no exit rule
can create one. C1's Phase 4x result (mean_R = −0.36 BTC OOS HIGH;
all 32 variants loss-making at every cost cell) demonstrates that a
trade population can fire in volume and still lose; no
trailing / break-even / partial-exit scheme applied retrospectively
to that population could honestly be called a strategy.

### 6.C Bad exit architecture can destroy a usable signal

The converse is also true. Wrong stop placement, wrong target
geometry, wrong time-stop, wrong intrabar sequencing rules, or
wrong cost accounting can convert a marginally-positive entry
signal into a measured-negative result. This is the project's
diagnostic concern: the existing strategy-research arc may have
correctly rejected entries that could not survive the fixed-stop /
fixed-TP / time-stop / next-bar-open / 8-bps-per-side framework
because that framework is the wrong unit, *or* it may have correctly
rejected them because they have no edge. Phase 4al does not assert
which; it only asserts that the question is admissible at the
audit / forensic / methodology level.

### 6.D Good exit architecture can reveal asymmetric payoff

For weak or sparse entry signals, the realized payoff distribution
may be asymmetric in a way the current backtest framework does not
capture. A future memo may legitimately ask: "is there a payoff
asymmetry visible at the trade-population level?" — but only as a
descriptive observation, never as a license to revive a rejected
candidate.

### 6.E Realized R after costs is the unit

All future work in this lane must report:

- realized R after costs,
- per-trade fee-in-R,
- per-trade slippage-in-R,
- per-trade funding-in-R (where applicable),
- realized-R distribution conditional on cost cell (LOW = 1 bp /
  side; MEDIUM = 4 bps / side; HIGH = 8 bps / side per §11.6).

### 6.F Fees / slippage / funding must be expressed in R

A 16-bps round-trip cost on a 0.50 × ATR(20) stop is **not** the
same fraction of risk as the same cost on a 1.50 × ATR(20) stop.
Cost-in-R depends on the chosen stop geometry. Tight stops can
make round-trip cost an unusually large fraction of initial risk.
This is one of the reasons R2 failed the §11.6 cost-sensitivity
gate and why no future exit-architecture work may be evaluated
without cost-in-R reporting.

### 6.G Leverage is not edge

Leverage affects:

- liquidation distance,
- margin pressure,
- feasible notional given a sizing-equity,
- fee-in-R when fees are quoted as bps of notional,
- operational constraints (cap at 2× per §1.7.3).

Leverage does **not** create directional edge. Any future memo that
implies otherwise is inadmissible at M0.

### 6.H Winner anatomy must be controlled and predeclared

Examining the post-entry path of historical winning trades is
legitimate **only if** the descriptive question is predeclared
before the data is touched. Selecting winners by outcome and then
fitting an exit rule to maximize their realized R is parameter
fitting on past outcomes (in particular: it is fitting on the
realized noise of small samples) and constitutes rescue under
§7.A and §6 of M0.

### 6.I The no-rescue rule must be refined, not removed

The no-rescue rule blocks "tune V2/G1/C1 exits to rescue them."
The rule does not, and should not, block "audit whether the
backtest correctly accounts for fees, slippage, funding, and
intrabar sequencing." §9 below states the refined rule.

## 7. M0 Clause-by-Clause Assessment

This section reads each of the twelve M0 clauses (verbatim from
`docs/00-meta/m0-mechanism-admissibility-gate.md` §5) and assesses
the candidate lane defined in §5 above, treating the two sub-claims
(A audit; B forensic) separately when they diverge.

The status legend is:

```text
PASS         the clause is satisfied on its theoretical face;
FAIL         the clause is structurally violated or unsatisfiable;
CONDITIONAL  the clause is satisfiable only under explicit
             boundary conditions stated in the assessment;
N/A          the clause does not apply to this memo's nature
             (justified in one sentence per M0 §5 instruction).
```

### M0.1 — Mechanism source

> "State the mechanism source. If price-only on a tested substrate,
> the proposal must explicitly justify why it is not within the
> depleted price-only single-symbol continuation lane (see §7)."

**Mechanism source.** The mechanism source for the candidate lane is
**post-entry trade-path geometry and execution / cost accounting**.
It is *derived* from price (because realized paths are price
sequences) but it is not a directional-prediction mechanism on
price. The unit of study is the realized payoff distribution, not
the next-bar price direction.

**Sub-claim A (audit).** The mechanism source is **methodology
implementation**, not market behavior. The audit asks whether the
backtest faithfully implements the documented stop-trigger-domain,
break-even-rule, EMA-slope-method, stagnation-window-role,
fee / slippage / funding rules, and intrabar-ambiguity rules. There
is no market-mechanism claim under sub-claim A; M0.1 is satisfied
because methodology audit is not a market mechanism source.

**Sub-claim B (forensic).** The mechanism source is **realized
post-entry path structure of the retained-evidence trade
populations**. This is descriptive structure, not a mechanism
claim that anything *predicts* anything. M0.1 is satisfied because
the lane does not propose a directional mechanism.

**Status.** **PASS** for both sub-claims.

**Note.** A future memo that converts sub-claim B from "describe
the path structure" into "use the path structure to enter or exit"
exits the descriptive scope and must be re-evaluated under M0 from
scratch as a new mechanism claim, *not* as a continuation of
Phase 4al.

### M0.2 — Non-price-only or structurally distinct source requirement

> "The mechanism source must be **non-price-only** or, if price-only,
> **structurally distinct** from depleted lanes. Structurally
> distinct means the proposal is not a parameter tweak, descriptor
> tweak, interval tweak, symbol-universe expansion, or relabeled
> version of a failed family. The proposal must articulate the
> structural difference in theoretical terms before any data is
> touched."

**Sub-claim A (audit).** The audit lane is **structurally distinct**
from any depleted price-only lane because it is not a directional
proposal. It is a methodology / measurement question on the existing
backtest scripts. M0.2 PASS.

**Sub-claim B (forensic).** The forensic lane is **structurally
distinct** from §7.A price-only single-symbol directional
continuation because it does not propose to predict price. It
proposes to *describe* what happened after entries fired in
historical, retained-evidence trade populations. The substrate of
study is "realized payoff distributions of past entries" — a
distinct unit from "next-bar direction." M0.2 PASS.

**Boundary condition.** The structural distinction collapses if a
future memo silently converts a description of historical
winners' anatomy into a parameter-tuning exercise that re-enters
a depleted lane. The §9 no-rescue refinement (below) and the §7.B
forbidden-rescue / anti-reduction declaration enforce the boundary.

**Status.** **PASS** for both sub-claims, conditional on §9
discipline.

### M0.3 — Baseline-superiority theory versus H0 and R3

> "State, in theoretical terms, why the candidate's primary condition
> should produce positive expectancy versus an unconditioned baseline
> that shares the same geometry. Derive a predicted Δ_R from
> theoretical content. Commit to that predicted Δ_R as the
> *expected outcome* of any future baseline test (Phase 4w M1 / M2
> form for strategy candidates; equivalent baseline differential for
> non-strategy mechanism claims)."

This clause is the most subtle for an audit / forensic lane.

**Sub-claim A (audit).** The candidate lane does **not** claim
positive expectancy. It claims the realized R of historical trades
*may have been mismeasured*, where "mismeasured" means the gap
between *reported R* and *true realized R after costs* under the
documented stop / TP / cost / sequencing rules. The relevant
"baseline" is the existing backtest implementation. The relevant
"superiority claim" is "audit may detect a measurement defect."
The relevant predeclared Δ is therefore not a Δ_R for a strategy
but a Δ_measurement_error: the audit returns either *no defect
detected* (clean bill) or *a defect list* (with magnitude). M0.3 is
satisfied as a measurement claim, not as a baseline-superiority
claim. **CONDITIONAL** — the assessment passes only because the
proposal disclaims any baseline-superiority claim. Predicted Δ_R for
sub-claim A is, by construction, **not applicable**, and the
proposal must declare it as such (§9).

**Sub-claim B (forensic).** The forensic lane does **not** claim
positive expectancy either. It describes realized distributions. The
baseline is the population's realized R itself; the forensic
question is "what shape does this distribution have?" There is no
baseline-superiority claim. M0.3 is satisfied only if the future
forensic memo *explicitly disclaims* any predicted-Δ_R claim and
explicitly forbids converting the descriptive output into a strategy
claim without a fresh ex-ante hypothesis. **CONDITIONAL**.

**Cross-reference.** This is exactly the discipline encoded in
M0.7: opportunity-rate viability is not edge-rate viability. For
this lane, *descriptive viability is not edge-rate viability*. A
shape may be visible without implying that any rule operating on
that shape would produce positive expectancy.

**Status.** **CONDITIONAL** for both sub-claims, conditional on
explicit disclaim of any baseline-superiority claim in any future
memo within this lane.

### M0.4 — Rejection-topology distance

> "State explicit distance from each of: R2 (V1 pullback-retest
> variant; cost-fragility rejection), F1 (mean-reversion after
> overextension; catastrophic-floor), D1-A (funding-aware
> contrarian; mechanism / framework mismatch), V2 (participation-
> confirmed breakout; design-stage), G1 (regime-first breakout
> continuation; gate × setup sparseness), C1 (volatility-contraction
> expansion breakout; fires-and-loses), any future rejected
> strategies added to this list after Phase 4ak. Identify the
> **closest-prior-failure trap** and explain in theoretical terms
> why the proposal is not that trap."

The distance matrix:

| Prior rejection | Closest rescue trap for this lane |
|---|---|
| R2 (cost fragility) | "Maybe R2 would have worked with a wider stop / different TP / break-even." Rescue if the lane tunes exits on R2's trade population. |
| F1 (catastrophic-floor / bad full-population payoff) | "Maybe F1 would have worked with a tighter trailing stop / earlier time-stop." Rescue if the lane tunes exits on F1's trade population. |
| D1-A (mechanism / framework — non-trigger conditions failed) | "Maybe D1-A would have worked with a +1.0R / +1.5R / +2.5R target instead of +2.0R." Rescue if the lane tunes exits on D1-A's trade population. |
| V2 (design-stage incompatibility — zero-trade) | "Maybe V2 would have produced trades with a different stop-distance bound." Rescue if the lane re-runs V2 with widened stop bounds. |
| G1 (regime-gate × setup sparseness — zero-trade) | "Maybe G1 would have produced active trades with looser regime confirmation." Rescue if the lane relaxes regime gates. |
| C1 (fires-and-loses — 149 BTC OOS HIGH trades; mean_R = −0.36) | "Maybe C1 would have worked with a wider TP / partial exit / trailing stop." This is the **closest rescue trap** for this lane because C1 is the only retained-evidence candidate that produced a meaningful sample of executed trades that lost. |

**Closest-prior-failure trap: C1 (fires-and-loses).** The C1
trade population is the only one large enough that a researcher
could plausibly look at MFE / MAE / time-to-MFE distributions and
imagine that "if we had moved the target / partial-exited / trailed
the stop, the realized R would have been positive." That belief —
applied to C1's existing trade population — is rescue. Phase 4l (V2)
and Phase 4r (G1) had zero or near-zero trade populations and
therefore do not present this trap; their rescue trap is parameter
relaxation at entry, which is already explicitly forbidden by
Phase 4y / Phase 4s.

**Structural argument why this lane is not the C1 rescue trap.**

1. The lane's sub-claim A (audit) operates on **methodology**, not
   on C1's trade population in particular. It either applies to the
   backtest implementation as a whole or it does not.
2. The lane's sub-claim B (forensic) is **descriptive**. A future
   memo within sub-claim B that tunes exit parameters on C1's
   trade population is not within sub-claim B; it is the rescue
   trap, and is forbidden by §9.A below.
3. A predeclared payoff-distribution description that happens to
   look at C1's trade population is not the same as a strategy
   that operates on C1's trade population. The §9 refinement
   makes the boundary explicit and enforceable.

**Status.** **CONDITIONAL** — the lane is admissible *only* under
the §9 refinement that prohibits parameter retrofit on any rejected
candidate's trade population. Without §9 enforcement, the lane is
inadmissible at M0.4 because the C1 rescue trap is too easy to fall
into.

### M0.5 — Cost-realism plausibility under §11.6

> "State the cost-realism plausibility under §11.6 HIGH cost = 8 bps
> per side; round-trip = 16 bps. State predicted gross expectancy
> and expected cost burden. State whether the proposal's expected
> profitability survives the round-trip cost cell at the descriptive
> theoretical-content layer before any backtest is contemplated."

The candidate lane does **not** propose profitability. Sub-claim A
proposes a methodology audit. Sub-claim B proposes descriptive
forensic analysis. Neither claims gross expectancy. M0.5 is
nonetheless central, because the lane's *value claim* depends on
realized R after costs and on cost-in-R reporting.

**Sub-claim A (audit).** A future audit must verify that the
backtest scripts apply 16-bps round-trip cost (8 bps per side
taker fee, plus the cost-cell slippage cell as predeclared by
Phase 4k / 4q / 4w). The audit's *value*, if any defect is found,
is to ensure that future verdicts reflect §11.6 correctly. The
audit lane does not propose to relax §11.6. **PASS** — the lane
strengthens cost-realism rather than threatening it.

**Sub-claim B (forensic).** A future forensic analysis must report
realized-R distributions per cost cell (LOW = 1 bp / side; MEDIUM =
4 bps / side; HIGH = 8 bps / side). A descriptive observation that
some payoff structure exists at LOW but disappears at HIGH is
**not** a license to relax §11.6; it is, in fact, evidence that the
mechanism is cost-fragile (R2 pattern). **PASS** — the lane
strengthens cost-realism by requiring per-cost-cell reporting.

**Predicted gross expectancy.** Not applicable. The lane is
descriptive / methodology, not predictive. Any future memo within
this lane that smuggles a gross-expectancy claim must be rejected at
M0.5.

**Status.** **PASS** for both sub-claims, conditional on cost-in-R
reporting being mandatory in any future memo within this lane.

### M0.6 — Opportunity-rate plausibility

> "State the predeclared minimum candidate-event arrival rate, joint-
> trigger arrival rate, and per-OOS-window trade-count floor. Derive
> opportunity-rate floors from theoretical content; do **not** derive
> them from prior failure forensic numbers (e.g., G1's 2.03% active
> fraction, C1's 149 BTC OOS HIGH trade count, V2's zero-trade
> result, Phase 4ai's `frac_selected ≈ 0.49`)."

**Sub-claim A (audit).** The "trade population" for a methodology
audit is the **set of test cases the audit can run** — typically
edge cases, intrabar-ambiguity scenarios, sequencing scenarios. The
opportunity rate for an audit is "every implemented decision path"
and is by construction non-sparse (the audit can synthesize test
inputs that exercise every documented branch). **PASS** — audit
opportunity rate is structurally non-blocking.

**Sub-claim B (forensic).** The trade population for a forensic
analysis is the **retained-evidence trade populations of R1a /
R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1**. Sample sizes vary —
V2 and G1 have zero qualifying trades; C1 has 149 BTC OOS HIGH; F1
and D1-A have larger populations from their Phase 3 arcs. A future
forensic memo must predeclare the per-population sample-size floor
required to make any descriptive claim non-degenerate. The floor
should be derived from theoretical content (e.g., "at least 30
trades to compute a stable empirical CDF of MFE") and not from a
prior-failure forensic number. **CONDITIONAL** — the lane is
admissible only if any future forensic memo predeclares its
sample-size floor before touching the data.

**Status.** **PASS** for sub-claim A; **CONDITIONAL** for sub-claim
B, conditional on predeclared sample-size floors derived from
theoretical content (not from C1's 149 or F1's / D1-A's specific
counts).

### M0.7 — Edge-rate plausibility

> "State the predeclared minimum baseline differential the candidate
> is *expected* to produce versus the closest unconditioned baseline,
> independent of opportunity-rate. State the predicted bootstrap
> confidence-interval lower bound (Phase 4w M1 / M2 form) or
> equivalent descriptive edge-rate predicate (e.g., predeclared IC
> floor; predeclared median-spread floor; predeclared
> outperformance-fraction floor).
>
> This clause must explicitly recognize: opportunity-rate viability
> is not edge-rate viability. C1 satisfied opportunity-rate (rate
> 3.33; 100% pass; 149 trades) and failed edge-rate (M1 –0.244R CI
> strictly negative). Phase 4ai satisfied opportunity-rate (rank-
> quality filter produces an answer on ~ 45% of timestamps) and
> failed edge-rate (`frac_selected > median ≈ 0.49`; spread ≤ 0;
> IC = 0). Both gates must be passed for a future candidate to
> advance."

This clause is, in practice, the binding constraint for the lane.

The candidate lane does **not** make an edge-rate claim. It
explicitly disclaims edge-rate manufacturing.

**Sub-claim A (audit).** No edge-rate claim. The audit's success
condition is *correct measurement*, not *positive differential*. If
the audit returns a clean bill, that is success. If the audit
returns a defect list, that is also success at the methodology
layer (because it identifies a defect). Neither outcome implies
edge. **N/A** — but the proposal must explicitly declare edge-rate
N/A in any future memo, with one-sentence justification per the
M0 §5 instruction.

**Sub-claim B (forensic).** No edge-rate claim. The forensic
analysis's success condition is *descriptive characterization*,
not *predictive differential*. A descriptive observation that
"realized MFE distribution has heavy-right tail in population X"
does **not** imply that any rule predicated on that observation
would produce positive expectancy. **N/A** — same disclaim
requirement.

**Critical recognition.** This clause names exactly the trap this
lane could fall into. Looking at MFE distributions and concluding
"if we had taken profits at the median MFE, expectancy would have
been positive" is **fitting on past noise of small samples**. It is
the C1 rescue trap (M0.4), it is opportunity-rate-dressed-as-edge-
rate (M0.7), and it is rescue (M0.10). A future memo within this
lane that converts a descriptive observation into a strategy claim
without a fresh ex-ante hypothesis is inadmissible.

**Status.** **N/A** for both sub-claims, with mandatory explicit
disclaim in any future memo. The disclaim is a hard requirement; a
future memo that omits it has not satisfied M0.7 and is
inadmissible.

### M0.8 — Data availability and integrity feasibility

> "State which datasets are required. State whether each is research-
> eligible PASS, governed partial under Phase 4ad Rule A / B / C,
> governed by Phase 4j §11 for metrics / OI subset partial
> eligibility, or unavailable and therefore blocking. No data
> acquisition is implied by passing M0."

**Sub-claim A (audit).** No datasets required. The audit operates
on the backtest scripts (Phase 4l, Phase 4r, Phase 4x) and on
synthesized test inputs. **PASS / no acquisition implied.**

**Sub-claim B (forensic).** Required datasets are the **research
output artefacts** of prior phases — the Phase 4l / 4r / 4x trade
ledgers and any retained-evidence trade ledgers from the Phase 2 /
Phase 3 strategy arcs. These are research outputs, not market data
acquisitions. They already exist (or were produced and are
reproducible from existing scripts). For path-level reconstruction
(MFE / MAE within trades), the underlying market data is the
already-acquired Phase 4i 30m / 4h klines and the v002 / 5m
datasets — all governed by their existing manifests. **PASS / no
new acquisition implied** for trade-price MFE / MAE. **GOVERNED
PARTIAL** under Phase 3r §8 + Phase 4ad Rule A if any future
forensic work requires mark-price intrabar reconstruction (Phase 3q
mark-price 5m manifests are `research_eligible: false`; mark-price
30m / 1h / 4h Phase 4ac manifests are `research_eligible: false`
for BTC / ETH; mark-price stop-domain forensic work is therefore
**blocked** at this boundary unless a separately authorized phase
clears governance). **POTENTIALLY BLOCKING** for any sub-component
that requires aggTrades / depth / order-book / cross-venue / spot
data — those are unavailable and a future memo proposing them is
inadmissible at M0.8.

**Status.** **PASS** for sub-claim A; **PASS / GOVERNED PARTIAL /
POTENTIALLY BLOCKING** for sub-claim B depending on the specific
forensic question, with the boundary that no new data acquisition
is implied or authorized by Phase 4al.

### M0.9 — Governance compatibility

> "State explicit compatibility with all binding project governance:
> §11.6, §1.7.3, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8,
> Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w,
> this M0 governance document, the post-null cooldown rule in §6,
> any later project locks. A proposal that is incompatible with any
> of the above on its face is structurally inadmissible at M0 and
> must terminate before discovery."

Compatibility check, by lock:

| Lock | Compatibility |
|---|---|
| §11.6 (8 bps / side; 16 bps round-trip) | **Compatible** — the lane preserves and enforces it; any future memo must report cost-in-R per cost cell. |
| §1.7.3 (0.25% risk; 2× leverage cap; one position max; mark-price stops) | **Compatible** — the lane does not propose changing any of these. |
| Phase 3r §8 (mark-price gap governance) | **Compatible** — any mark-price-domain forensic work must apply Phase 3r §8 verbatim; Phase 4al does not authorize mark-price-domain work. |
| Phase 3v §8 (stop-trigger-domain governance) | **Compatible** — stop-trigger-domain audit is a candidate audit subject; the audit must verify the existing rule is implemented, not relax it. |
| Phase 3w §6 / §7 / §8 (break-even / EMA-slope / stagnation governance) | **Compatible** — break-even and stagnation are within the candidate lane's descriptive scope; the lane must verify rules are implemented as documented, not propose new rules. |
| Phase 4j §11 (metrics OI-subset partial eligibility) | **Compatible** — irrelevant to this lane unless a future memo invokes metrics OI; if it does, the §11 rule applies verbatim. |
| Phase 4k / 4p / 4q / 4v / 4w (V2 / G1 / C1 backtest-plan and strategy-spec discipline) | **Compatible at the audit layer; conditional at the forensic layer.** Audit may verify implementations against these specs. Forensic analysis on V2 / G1 / C1 trade populations must not modify or relax these specs; it must only describe what already happened under them. |

**Status.** **PASS** at the docs-only level. A future memo that
proposes changing any of these locks is inadmissible at M0.9.

### M0.10 — Forbidden-rescue and anti-reduction check

> "State explicitly that the proposal does not reduce to: V2 / V2-
> prime / V2-narrow / V2-relaxed / V2 hybrid; G1 / G1-prime / G1-
> narrow / G1-extension / G1 hybrid; C1 / C1-prime / C1-extension /
> C1 hybrid; R2 / R1a / R1b-narrow rescue; F1 mean-reversion rescue;
> D1-A funding-trigger rescue; rank-then-V2 / G1 / C1 breakout under
> a wrapper; multi-position portfolio trading; 5m strategy / hybrid /
> variant; any prior-strategy alt-symbol rerun. The check must name
> the closest rescue trap and articulate the structural reason the
> proposal is not that trap. Naming alone is not sufficient; a
> structural argument is required."

**Closest rescue trap.** As argued in M0.4: the C1 rescue trap
("look at C1's MFE / MAE distribution and propose a different exit
rule that would have made C1 profitable").

**Structural argument why the proposal is not that trap.** The
proposal is split into two sub-claims. Sub-claim A (audit) does not
operate on any specific candidate's trade population except as a
test case for methodology correctness; it cannot, by construction,
optimize parameters on any candidate. Sub-claim B (forensic) is
explicitly descriptive and is bounded by §9 to forbid converting a
description into an exit rule applied to a rejected candidate. The
boundary is enforceable because:

1. §9.A names the forbidden conversions explicitly,
2. §9.B names the allowed descriptive activities explicitly,
3. The §10 winner-anatomy rules require predeclaration before
   data is touched,
4. M0.7 disclaim requirement makes any edge-rate claim from
   descriptive observation inadmissible at M0,
5. The §13 future-Phase-4am scope explicitly forbids parameter
   tuning on rejected candidates' trade populations.

A future memo that violates any of (1)–(5) is not within the lane;
it is the rescue trap, and is inadmissible.

**Other rescue traps named, structurally distinguished.**

- **R2 cost-fragility rescue.** Not applicable; the lane preserves
  §11.6 cost realism and enforces cost-in-R reporting. R2 cannot
  be rescued by re-evaluating it under cheaper costs because §11.6
  is a project lock.
- **F1 catastrophic-floor rescue.** Not applicable; the lane does
  not propose to retain only F1 winners or cherry-pick F1's TARGET
  subset. F1 was hard-rejected by full-population payoff (Phase 3c
  catastrophic-floor predicate); the lane cannot revive it.
- **D1-A non-trigger rescue.** Not applicable; the lane does not
  use funding as an exit trigger and does not propose alternative
  D1-A targets.
- **V2 / G1 design-stage rescue.** Not applicable; both produced
  zero or near-zero qualifying trades. There is no MFE / MAE
  distribution to forensically describe at usable sample sizes.
- **rank-then-V2 / G1 / C1 wrapper.** Not applicable; the lane is
  not a ranking mechanism.
- **multi-position portfolio.** Not applicable; the lane preserves
  one-position-max.
- **5m strategy.** Not applicable; the lane does not propose 5m
  signals. (Mark-price 5m forensic reconstruction, if ever
  proposed, is governed by Phase 3r §8 / Phase 4ad Rule A and
  would require separate authorization.)
- **alt-symbol prior-strategy rerun.** Not applicable; the lane
  does not propose re-running rejected strategies on alt symbols.

**Status.** **PASS** for both sub-claims, conditional on §9 / §10 /
§13 enforcement.

### M0.11 — Pre-backtest falsification criteria

> "State what descriptive feasibility evidence would kill the
> candidate **before** backtest grid budget is spent. The criterion
> must be predeclared at the M0 stage, substantive enough to
> terminate the candidate at the docs-only or analysis-and-docs
> stage if it fires, distinct from generic catastrophic-floor
> predicates."

This lane has no backtest by design. The pre-backtest falsification
question maps to "what evidence would kill the lane at the
analysis-and-docs stage?"

Predeclared falsification criteria for any future Phase 4am within
this lane:

**For sub-claim A (audit):**

- **CRIT-A1.** If the audit identifies *no* measurement defect in
  any documented decision path (cost / fee / slippage / funding /
  stop-trigger-domain / break-even / EMA-slope / stagnation /
  intrabar sequencing / mark-price stop domain), then the audit
  returns a clean-bill report and the lane is exhausted at the
  audit layer. No successor sub-component is authorized by a
  clean-bill outcome.
- **CRIT-A2.** If the audit identifies measurement defects but the
  defects are not material (i.e., applying the corrected
  measurement to the existing retained-evidence trade populations
  changes realized R after costs by less than a predeclared
  threshold to be set in any future Phase 4am brief, derived from
  theoretical content not from observed defect magnitudes), the
  defects are recorded as documentation-only entries and do not
  authorize any successor strategy work or any verdict revision.

**For sub-claim B (forensic):**

- **CRIT-B1.** If the descriptive analysis shows that realized
  MFE / MAE / time-to-event distributions are *symmetric* or
  *uninformative* across all retained-evidence trade populations
  (no consistent payoff asymmetry that survives sample-size and
  cost-in-R adjustment), the lane is exhausted at the forensic
  layer.
- **CRIT-B2.** If the descriptive analysis shows asymmetry that is
  visible only on subpopulations selected by outcome (e.g., "if
  you select winners by realized R and look at their MFE
  distribution"), the analysis has fitted on past outcomes and is
  by construction inadmissible. The future memo must report this
  outcome as a falsification, not as an opportunity.
- **CRIT-B3.** If the descriptive analysis claims asymmetry but
  the asymmetry disappears under HIGH-cost (8 bps / side; 16 bps
  round-trip) cost-in-R reporting, the lane is exhausted at the
  cost-realism layer (R2 pattern).

**Distinction from CFP-1..CFP-12.** The Phase 4k / 4q / 4w
catastrophic-floor predicates are downstream backtest gates. The
CRIT-A1 .. CRIT-B3 above are upstream audit / forensic gates that
must fire before any backtest is contemplated. They are stricter
than CFPs in the sense that they terminate the lane at the docs-
only / analysis-and-docs stage.

**Status.** **PASS** at the M0 layer, conditional on any future
Phase 4am brief restating CRIT-A1 .. CRIT-B3 (or stricter
substitutes) verbatim before analysis begins.

### M0.12 — Post-null cooldown and non-authorization

> "State whether the mechanism family is currently cooled down by any
> prior `NOT_SUPPORTED` result (see §7). If yes, the proposal must
> identify a materially new mechanism source per §6 and explain why
> it is not a forbidden post-null tweak.
>
> State explicitly that passing M0 does not authorize a strategy-
> spec memo, a backtest-plan memo, a backtest, paper / shadow
> operation, live-readiness preparation, deployment, exchange-write
> capability, production keys, authenticated APIs, private endpoints,
> public-endpoint calls in code, user stream, WebSocket, MCP,
> Graphify, `.mcp.json`, or credentials, any successor phase. Each
> future phase still requires explicit operator authorization."

**Cooldown check.** The candidate lane is **not** in §7.A
(price-only single-symbol directional continuation), **not** in
§7.B (cross-sectional ranking under Phase 4ai descriptors),
**not** in §7.C (derivatives-context directional), **not** in §7.D
(microstructure / order-flow), and **not** in §7.E (mark-price
stop-domain / execution-realism, except as noted below).

The lane has a partial overlap with §7.E because mark-price stop-
domain forensic work, if ever proposed within this lane, would
fall within §7.E and would require separate authorization under
Phase 4ad Rule A predeclaration. Phase 4al does not authorize any
mark-price stop-domain work; any future Phase 4am brief that
includes mark-price stop-domain forensic must clear §7.E
separately or scope the lane to trade-price-only forensic.

**Materially-new requirement.** Because the lane is not in §7,
§6.A's materially-new requirement does not apply. The lane is a
new admissibility question and is being evaluated on its own merits
under M0.

**Non-authorization.** Phase 4al explicitly states that passing M0
does **not** authorize:

- a strategy-spec memo,
- a backtest-plan memo,
- a backtest,
- paper / shadow operation,
- live-readiness preparation,
- deployment,
- exchange-write capability,
- production keys,
- authenticated APIs, private endpoints, public-endpoint calls in
  code, user stream, WebSocket, MCP, Graphify, `.mcp.json`,
  credentials,
- Phase 4am, Phase 5, Phase 4 canonical,
- any successor phase.

Each future phase requires explicit operator authorization.

**Status.** **PASS** — the lane is not cooled down; the non-
authorization clause is honored verbatim.

### M0 assessment summary

| Clause | Status |
|---|---|
| M0.1 | PASS |
| M0.2 | PASS, conditional on §9 |
| M0.3 | CONDITIONAL (no baseline-superiority claim; explicit disclaim required) |
| M0.4 | CONDITIONAL (closest trap C1; admissible only under §9) |
| M0.5 | PASS, conditional on cost-in-R reporting |
| M0.6 | PASS (audit); CONDITIONAL (forensic; predeclared sample-size floor) |
| M0.7 | N/A with mandatory disclaim (no edge-rate claim) |
| M0.8 | PASS / GOVERNED PARTIAL / POTENTIALLY BLOCKING per scope |
| M0.9 | PASS |
| M0.10 | PASS, conditional on §9 / §10 / §13 |
| M0.11 | PASS, conditional on CRIT-A1..CRIT-B3 restatement |
| M0.12 | PASS (lane not cooled down; non-authorization honored) |

The lane **does not structurally fail** any clause. Several clauses
are CONDITIONAL on explicit disclaim, predeclaration, or §9 / §10 /
§13 enforcement. The cumulative structural assessment is therefore
**CONDITIONAL / PARTIAL** rather than unconditional PASS.

## 8. Post-Null Cooldown Assessment

The post-null cooldown rule (M0 §6) states:

> "After a predeclared feasibility phase returns NOT_SUPPORTED, the
> same mechanism family may not be re-opened through parameter /
> descriptor / threshold / symbol-universe / interval / forward-
> horizon / rank-quality-filter / composite-weight / rebalance-
> frequency / any other adjustment unless a future docs-only M0
> memo first identifies a materially new mechanism source that is
> independent of the failed descriptor family. Materially new means
> derived from external theory or external evidence, not from
> observation of the failed phase's forensic results."

The candidate lane is **not** a re-opening of a cooled-down family.
It is a new admissibility question on a research lane that the
project has not previously analyzed in its own right. The Phase 4ai
`NOT_SUPPORTED` verdict does not extend to this lane because:

1. The lane's mechanism source is post-entry path geometry / cost
   accounting, not cross-sectional ranking on price-derived
   descriptors.
2. The lane's substrate is realized payoff distributions of past
   entries, not next-bar direction prediction.
3. The lane explicitly disclaims directional-edge claims (§6.B and
   M0.7).
4. The lane does not use any Phase 4ai forensic number as a tuning
   input. Specifically, no `frac_selected`, no spread-bps, no IC
   value, no Phase 4ai parameter is referenced in the candidate
   lane's design.

The lane therefore **passes the post-null cooldown rule** at the
M0.12 level on its own merits.

**Important boundary.** The post-null cooldown rule continues to
apply *prospectively* to any future analysis or memo that *would*
return `NOT_SUPPORTED` within this lane. If a future Phase 4am
audit returns CRIT-A1 (clean bill) or CRIT-B1 (uninformative
distributions), the *audit / forensic family* enters cooldown and
the §6 rule applies to any subsequent reopening. The cooldown rule
is structural and self-enforcing.

## 9. No-Rescue Refinement

The no-rescue rule has been a project-level discipline since
Phase 4y / Phase 4s / Phase 4m. The rule is **refined here** for
this specific lane, **not removed**.

### 9.A Forbidden activities within this lane

A future memo within the candidate lane is **forbidden** to:

- **9.A.1** Tune or optimize TP / SL / break-even / trailing /
  partial-exit / time-stop parameters on any rejected or retained-
  evidence candidate's trade population (R3 / R1a / R1b-narrow /
  R2 / F1 / D1-A / V2 / G1 / C1) with the intent of producing a
  positive-expectancy outcome.
- **9.A.2** Retrofit exit rules to improve historical realized R
  on any candidate, even if framed as "what if." A "what-if" with
  a parameter chosen after seeing outcomes is parameter fitting on
  past realized noise.
- **9.A.3** Convert any descriptive observation (a visible MFE
  shape, a time-to-event distribution feature, a sequencing
  pattern) into a strategy candidate without a fresh ex-ante
  hypothesis that names the mechanism source independently of
  the observation.
- **9.A.4** Revise any historical verdict (R3 / R2 / F1 / D1-A /
  V2 / G1 / C1) on the basis of audit or forensic findings unless
  a separately authorized verdict-revision phase determines that
  the original verdict's data inputs were materially defective in
  the §11.6 / §1.7.3 / Phase 3r / 3v / 3w / 4j / 4k / 4p / 4q /
  4v / 4w sense and that the defect is not project lock revision.
  Phase 4al does not authorize verdict revision.
- **9.A.5** Imply any paper / shadow / live-readiness path from any
  audit or forensic finding.
- **9.A.6** Imply any exchange-write or production-key authorization
  from any audit or forensic finding.

### 9.B Allowed activities within this lane (subject to separate authorization of any future Phase 4am)

A future memo within the candidate lane **may**, only if separately
authorized:

- **9.B.1** Predeclare an exit-path forensic audit design covering
  MFE / MAE / time-to-MFE / time-to-stop distributions for the
  retained-evidence trade populations. The predeclaration must
  occur before the data is touched.
- **9.B.2** Predeclare target-before-stop sequencing analysis
  (descriptive only) — i.e., for each historical trade, did MFE
  reach +1.0R / +1.5R / +2.0R / +2.5R before MAE reached the stop?
  A descriptive frequency, not a strategy parameter.
- **9.B.3** Predeclare realized-R-after-costs accounting per cost
  cell (LOW / MEDIUM / HIGH) for the retained-evidence populations,
  and verify that the existing backtest scripts compute it
  identically.
- **9.B.4** Predeclare fee-in-R / slippage-in-R / funding-in-R
  decomposition for the retained-evidence populations — purely
  descriptive accounting.
- **9.B.5** Predeclare an intrabar-ambiguity audit — for trades
  where MFE and MAE both occur within a single bar, what
  sequencing assumption was applied (stop-first conservative per
  Phase 4w, or otherwise), and is the assumption applied
  consistently in all backtest scripts?
- **9.B.6** Predeclare a backtest-logic audit covering: cost
  handling, slippage handling, funding handling, stop / TP
  sequencing, mark-price stop domain (subject to §7.E if invoked),
  partial-exit logic if any, break-even logic if any, trailing
  exit logic if any, time-exit logic, and realized R after costs.
- **9.B.7** Report findings as descriptive / measurement claims,
  not as edge-rate claims.

### 9.C Discipline order

The discipline order, from outermost to innermost:

1. The audit / forensic activity must be **predeclared** in a
   future Phase 4am brief before any data or script is read for
   measurement purposes (reading for governance / authority
   purposes is allowed).
2. The activity must be **descriptive / measurement-only** at the
   first pass. No optimization. No parameter tuning. No selection
   on outcome.
3. The findings must be **reported with cost-in-R**, per cost cell.
4. The findings must be **explicitly disclaimed** as not edge-rate
   claims (M0.7) and not baseline-superiority claims (M0.3).
5. Any successor work that would convert a descriptive finding
   into a strategy claim requires a **separately authorized fresh-
   hypothesis discovery memo** under M0 from scratch — not a
   continuation of Phase 4am.

## 10. Winner-Anatomy Boundaries

"Winner anatomy" — the descriptive characterization of trades that
ended with positive realized R — is legitimate only under strict
controls.

### 10.A Allowed winner-anatomy activities

If a future Phase 4am is authorized:

- **10.A.1** Path-behavior summaries (shape descriptors of the
  realized price path during a trade's lifetime).
- **10.A.2** MFE distributions (predeclared bins; predeclared per
  retained-evidence population).
- **10.A.3** MAE distributions (predeclared bins; predeclared per
  retained-evidence population).
- **10.A.4** Time-to-MFE distributions.
- **10.A.5** Time-to-adverse-excursion distributions.
- **10.A.6** Target-before-stop sequencing — descriptive
  frequency, not a strategy rule.
- **10.A.7** Realized-R decomposition (fee-in-R, slippage-in-R,
  funding-in-R, gross-R-from-price-path).
- **10.A.8** Cost-in-R decomposition per cost cell.
- **10.A.9** Exit-sequencing ambiguity audit (intrabar same-bar
  stop / TP cases).

### 10.B Forbidden winner-anatomy activities

The same future Phase 4am **must not**:

- **10.B.1** Choose any parameter (TP / SL / trailing / break-even /
  partial-exit / time-stop) after observing which parameter values
  would have produced positive realized R on any historical
  population.
- **10.B.2** Convert observed historical rescue patterns ("if you
  had moved the TP from +2.0R to +1.5R on C1, mean_R would have
  been positive") into a new strategy without a fresh ex-ante
  specification under M0 from scratch.
- **10.B.3** Revise any prior verdict on the basis of winner-anatomy
  findings.
- **10.B.4** Imply any paper / shadow / live-readiness / deployment /
  exchange-write authorization from winner-anatomy findings.
- **10.B.5** Mine the descriptive output for "promising regions"
  and propose a new strategy on the mined region without a fresh
  ex-ante hypothesis.
- **10.B.6** Report only winners; the descriptive analysis must
  cover the full retained-evidence population (winners and losers
  alike) to avoid selection-on-outcome.

### 10.C Predeclaration discipline

Any winner-anatomy work must:

- name the population *before* opening it;
- name the descriptive variables *before* computing them;
- name the bin / threshold structure *before* computing it;
- report the full population, not a subset selected on outcome;
- report cost-in-R per cost cell;
- explicitly disclaim edge-rate (M0.7) and baseline-superiority
  (M0.3) claims;
- explicitly invoke §9.A forbidden-activity boundaries.

## 11. Backtest-Logic Audit Admissibility

The candidate sub-claim A (backtest-logic audit) is admissible at
M0 under the following scope.

### 11.A In-scope audit subjects (admissible)

A future Phase 4am audit **may** verify:

- **11.A.1** Fee handling — taker fee = 4 bps per side per Phase 4w;
  maker rebates not assumed; fee applied to entry and exit legs.
- **11.A.2** Slippage handling — LOW = 1 bp / side; MEDIUM = 4 bps /
  side; HIGH = 8 bps / side per Phase 4k / 4q / 4w; applied
  symmetrically per side.
- **11.A.3** Funding handling — funding cost included in P&L per
  Phase 4q; funding excluded from C1 first-spec per Phase 4w
  (verify the exclusion is implemented correctly).
- **11.A.4** Stop / TP sequencing — Phase 4q / 4w precedence:
  stop > TP > time-stop; same-bar ambiguity resolved as
  stop-first conservative.
- **11.A.5** Mark-price stop domain — Phase 3v §8 stop-trigger-
  domain governance; verify no `mixed_or_unknown` paths exist;
  verify trade-price vs mark-price domain labels are applied per
  the spec.
- **11.A.6** Partial-exit logic — verify the existing scripts do
  not implement partial exits (none were specified for V2 / G1 /
  C1); confirm absence.
- **11.A.7** Break-even logic — Phase 3w §6 break-even rule;
  verify the rule is implemented as documented (or is `disabled`
  for V2 / G1 / C1 first specs per Phase 4g / 4p / 4v).
- **11.A.8** Trailing-exit logic — verify the existing scripts do
  not implement trailing exits (none were specified); confirm
  absence.
- **11.A.9** Time-exit logic — Phase 4q `T_stop = 16` for G1;
  Phase 4w `T_stop_bars = 2 × N_comp` for C1; verify implemented
  consistently.
- **11.A.10** Realized-R-after-costs accounting — verify that the
  reported realized R for each trade equals
  `((exit_price − entry_price) × side) / initial_R`, minus
  cost-in-R per cost cell, with funding-in-R where applicable.
- **11.A.11** Intrabar ambiguity — verify that same-bar stop / TP
  cases are resolved with the predeclared assumption and that the
  resolution is applied to every applicable trade.

### 11.B Out-of-scope audit subjects (inadmissible)

The same future Phase 4am audit **must not**:

- **11.B.1** Modify the existing scripts (Phase 4l, Phase 4r,
  Phase 4x, or any other) — the audit reports findings; corrective
  action requires separate authorization.
- **11.B.2** Modify any project lock or rule.
- **11.B.3** Revise any verdict on the basis of audit findings —
  the audit may identify defects, but verdict revision requires a
  separately authorized verdict-revision phase under whatever
  governance applies at that future time.
- **11.B.4** Optimize any parameter.
- **11.B.5** Run a new backtest — the audit operates on existing
  results and on synthesized test inputs.
- **11.B.6** Touch credentials, MCP, Graphify, `.mcp.json`,
  exchange-write paths, paper / shadow runtime, or live-readiness
  scaffolding.

**Phase 4al does not perform this audit.** Phase 4al only declares
the audit's admissibility under M0 as a *future* possible phase
subject to separate operator authorization.

## 12. Verdict

Phase 4al's verdict on the candidate lane:

```text
M0 STATUS: CONDITIONAL / PARTIAL — admissible as a future
descriptive forensic / backtest-logic-audit research lane, with
strict boundaries.

NOT admissible as: a strategy lane, a parameter-optimization
lane, a verdict-revision lane, or a paper / shadow / live-
readiness lane.
```

**Rationale.** The lane satisfies M0.1, M0.2, M0.5, M0.8, M0.9,
M0.10, M0.11, and M0.12 on its theoretical face, and satisfies
M0.3, M0.4, M0.6, and M0.7 only under explicit disclaim and
predeclaration discipline (§9 / §10 / §13 enforcement). The lane
does not structurally fail any clause; the cumulative status is
therefore **CONDITIONAL / PARTIAL** rather than unconditional
PASS.

The verdict reflects the operator's framing: the question "has
Prometheus under-modeled payoff management?" is admissible at the
audit / forensic / methodology level. The question "can payoff
management rescue rejected entries?" is **inadmissible** under
§9.A and is not part of this lane.

**Phase 4al does not authorize Phase 4am.** A future Phase 4am
brief, if ever proposed, would require:

- separate operator authorization;
- explicit conformance to §9 / §10 / §13 of this memo;
- explicit conformance to all binding M0 governance;
- explicit conformance to all project locks (§11.6, §1.7.3,
  Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11,
  Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w);
- explicit predeclaration of CRIT-A1..CRIT-B3 (or stricter
  substitutes) before analysis begins.

**Phase 4al does not authorize:** strategy-spec memos, backtest-plan
memos, backtests, paper / shadow operation, live-readiness
preparation, deployment, exchange-write capability, production
keys, authenticated APIs, private endpoints, public-endpoint calls
in code, user stream, WebSocket, MCP, Graphify, `.mcp.json`,
credentials, verdict revision, or lock revision.

## 13. Future Phase 4am Boundary (If Admissible)

If — and only if — the operator separately authorizes a future
phase within the lane, the following defines the maximum allowable
Phase 4am scope.

### 13.A Suggested name

```text
Phase 4am — Exit-Path Forensic Analysis and Backtest-Logic Audit
```

### 13.B Type

Analysis-and-docs only. Standalone-script mode (analogous to Phase
4ae / 4af / 4ai). No `prometheus.runtime/execution/persistence`
imports. No exchange adapters. No network I/O. No `.env`. No
credentials. No Binance API. Pure pyarrow + numpy + stdlib (and
matplotlib optional).

### 13.C Allowed scope

- §9.B.1 .. §9.B.7 activities, subject to predeclaration.
- §10.A.1 .. §10.A.9 winner-anatomy activities, subject to §10.C
  discipline.
- §11.A.1 .. §11.A.11 backtest-logic audit subjects, subject to
  §11.B exclusions.

### 13.D Forbidden scope

- All §9.A activities (forbidden tuning / retrofit / conversion /
  verdict revision / paper / shadow / live implication).
- All §10.B activities (forbidden winner-anatomy uses).
- All §11.B activities (forbidden audit modifications).
- Modifying any backtest script.
- Modifying any project lock.
- Modifying any historical verdict.
- Acquiring data.
- Creating or modifying manifests.
- Creating new strategy candidates.
- Authorizing Phase 4an or any successor.

### 13.E Required predeclaration content

Any Phase 4am brief must predeclare, before data is touched:

1. The audit scope (subset of §11.A activities to perform).
2. The forensic scope (subset of §9.B and §10.A activities to
   perform).
3. The retained-evidence trade populations included.
4. The descriptive variables and their bin / threshold structure.
5. The cost cells (LOW / MEDIUM / HIGH per §11.6).
6. The sample-size floor per population.
7. CRIT-A1..CRIT-B3 falsification criteria (or stricter
   substitutes).
8. The §9.A forbidden-activity boundaries (verbatim).
9. The §10.B forbidden winner-anatomy boundaries (verbatim).
10. The §11.B forbidden audit modifications (verbatim).
11. The mark-price scope (trade-price-only, or invoking §7.E
    separately).
12. The non-authorization clause (no successor phase authorization
    implied by Phase 4am completion).

### 13.F Required reporting content

Any Phase 4am report must include:

1. Audit findings (defect list or clean-bill, per §11.A subject).
2. Forensic findings (descriptive distributions, per §9.B / §10.A
   subject).
3. Cost-in-R reporting per cost cell.
4. Explicit M0.7 disclaim (no edge-rate claim).
5. Explicit M0.3 disclaim (no baseline-superiority claim).
6. Explicit non-authorization statement.
7. Explicit no-verdict-revision statement.
8. Explicit no-rescue statement (§9.A boundaries restated).
9. Recommendation (typically remain-paused; or a conditional
   future docs-only governance memo if a defect is identified).

### 13.G Phase 4am does not authorize

The Phase 4am brief must explicitly state that Phase 4am does not
authorize:

- Phase 4an or any successor;
- strategy work;
- backtest grid budget;
- paper / shadow;
- live-readiness;
- deployment;
- exchange-write;
- production keys;
- authenticated APIs;
- private endpoints;
- public-endpoint calls in code;
- user stream / WebSocket;
- MCP / Graphify / `.mcp.json` / credentials;
- verdict revision;
- lock revision.

## 14. Future Exit-Path Data Resolution Hierarchy

This section is a **future data-resolution recommendation** for any
future Phase 4am or later separately authorized exit-architecture
analysis. It is recorded here only because Phase 4al's verdict is
CONDITIONAL / PARTIAL admissible. If the verdict were FAIL, this
section would not apply.

**Phase 4al does not authorize new data acquisition.** **Phase 4al
does not authorize 5m, 1m, aggTrades, or tick-data work.**
**Phase 4al does not reopen the 5m strategy thread, which remains
operationally CLOSED per Phase 3t.**

### 14.A Recommended timeframe / resolution hierarchy

If a future Phase 4am or later separately authorized analysis
requires lower-timeframe data for exit-path forensics, the
recommended hierarchy is:

```text
15m / 30m / 1h / 4h     signal / event context (already acquired)
5m                      recommended first path-resolution layer
                        for exit forensics
1m                      escalation layer only if 5m ambiguity is
                        too high
aggTrades / tick        final escalation only if 1m still cannot
                        answer key sequencing questions
```

### 14.B Current operator guidance

- Do **not** jump directly to 1m data.
- Treat 5m candles as the recommended **first** lower-timeframe
  path-resolution layer.
- Treat 1m candles as an escalation option only if 5m leaves too
  much stop / TP sequencing ambiguity or cannot resolve tight-stop
  path behavior.
- **5m must be framed strictly as a forensic measurement layer,
  not as a reopened 5m strategy thread, entry timeframe, signal
  timeframe, or strategy lane.** The old 5m strategy thread
  remains operationally CLOSED per Phase 3t and is **not** reopened
  by Phase 4al.
- If lower-timeframe data is later needed, it must be authorized
  **separately** as data-acquisition / data-governance work,
  subject to Phase 3p §4.7, Phase 3q v001-of-5m provenance,
  Phase 3r §8 mark-price gap governance, and Phase 4ad Rules A /
  B / C as applicable.
- Phase 4al itself remains docs-only and does not acquire any
  data.

### 14.C Ambiguity-rate concept (descriptive, for future analysis)

For any future Phase 4am or later separately authorized analysis,
a useful descriptive measure is the **ambiguity rate** — the
fraction of trades for which both the stop and the target occur
inside the same lower-timeframe candle, so that intrabar
sequencing cannot be resolved from the candle alone.

Suggested interpretive bands (descriptive heuristics; not gates):

```text
< 2%      5m is probably enough for exit-path forensics
2% – 10%  5m usable with conservative (stop-first) assumptions
> 10%     consider 1m escalation
> 20%     5m likely too coarse for exit sequencing
```

These bands are heuristic interpretations; any future memo using
them must predeclare the bands before measuring the ambiguity
rate, must report the measured ambiguity rate per retained-
evidence trade population, and must not retroactively adjust the
bands after seeing the measurements (selection on outcome is
forbidden by §10.B.6 and §9.A).

### 14.D Forensic resolution coverage by question

For different forensic questions, the resolution requirements
differ:

- **MFE / MAE magnitude.** 5m is probably enough for a first-pass
  descriptive measurement.
- **Exact stop-before-target sequencing.** 5m may still be
  ambiguous; the ambiguity rate (§14.C) determines whether 1m
  escalation is justified.
- **Mark-price stops.** Future analysis may need *both*
  trade-price and mark-price candles:
    - **trade-price candles** for TP / favorable-path measurement;
    - **mark-price candles** for stop-trigger-path measurement.
  Phase 3r §8 mark-price gap governance and Phase 4ad Rule A apply
  verbatim. Phase 3q mark-price 5m manifests are
  `research_eligible: false` for trade-price-comparable use, and
  Phase 4ac mark-price 30m / 1h / 4h manifests are
  `research_eligible: false` for BTC / ETH / SOL / XRP / ADA, so
  mark-price stop-domain forensic work remains **blocked** until a
  separately authorized phase clears governance under §7.E of M0
  and Phase 4ad Rule A predeclaration.

### 14.E Boundary language (binding for §14)

- Phase 4al does **not** acquire 5m or 1m data.
- Phase 4al does **not** authorize 5m or 1m data acquisition.
- Phase 4al does **not** authorize aggTrades or tick-data
  acquisition.
- Phase 4al does **not** reopen the 5m strategy thread.
- The 5m strategy thread remains operationally CLOSED per
  Phase 3t.
- Phase 4al records §14 only as a future data-resolution
  recommendation if the exit-management lane passes M0 or is
  conditionally admissible (which it is, under §12).
- Any future memo proposing 5m / 1m / aggTrades / tick data
  acquisition must clear M0 §4.A applicability and the relevant
  data-governance documents (Phase 3p §4.7, Phase 3q provenance,
  Phase 3r §8, Phase 4ad Rules A / B / C, Phase 4j §11 if
  applicable). The §6 post-null cooldown rule does not currently
  apply to this lane (§7 of the M0 document does not list it),
  but the rule remains binding *prospectively* for any future
  feasibility null within this lane.

## 15. Decision Menu

Available operator decisions after Phase 4al merges to `main`:

- **Option A — primary.** Remain paused. The Phase 4al admissibility
  finding is recorded; no successor phase is authorized. The
  project remains paused at the post-Phase-4al boundary.
- **Option B — merge-to-main-then-stop.** Merge Phase 4al, then
  stop. (This is the primary procedural recommendation; equivalent
  to Option A under the project's standard workflow.)
- **Option C — conditional tertiary.** Authorize a future
  Phase 4am within the §13 boundary as an analysis-and-docs phase.
  Recommended only if the operator wants to spend Phase 4am budget
  on the audit / forensic lane and accepts the §9 / §10 / §11 / §13
  discipline.
- **Option D — conditional secondary.** Authorize a narrower future
  phase that performs **only** the §11.A backtest-logic audit
  (without §9.B forensic analysis). This is the most conservative
  active-research option and yields documentation value
  unconditionally (clean bill or defect list).
- **Option E — not recommended.** Authorize a fresh-hypothesis
  discovery memo to convert exit-architecture observations into a
  new strategy candidate. Phase 4al explicitly does not endorse
  this; any such future memo would have to clear M0 from scratch
  with a fresh ex-ante hypothesis that does not depend on
  Phase 4am observations.
- **Option F — forbidden.** Tune exit parameters on any rejected /
  retained-evidence candidate's trade population to produce a
  positive-expectancy outcome. This is rescue under §9.A and is
  inadmissible.
- **Option G — forbidden.** Revise any retained verdict on the
  basis of audit / forensic findings without a separately
  authorized verdict-revision phase under whatever governance
  applies at that future time. Phase 4al does not authorize
  verdict revision.
- **Option H — forbidden.** Authorize paper / shadow / live-
  readiness / deployment / exchange-write / production keys /
  authenticated APIs / private endpoints / public-endpoint calls in
  code / user stream / WebSocket / MCP / Graphify / `.mcp.json` /
  credentials. Phase 4al does not authorize any of these.

## 16. Recommendation

**Primary recommendation.** Option A / Option B — remain paused
unless the operator separately authorizes a bounded successor.

**Conditional secondary recommendation.** If the operator wants to
spend research budget on this lane, Option D (narrower §11.A
backtest-logic audit only) is the most conservative active option.
Option C (full §13 Phase 4am) is acceptable but heavier and more
demanding of predeclaration discipline.

**Not recommended.** Option E (fresh-hypothesis discovery from
exit-architecture observations) without first running Option C / D
to characterize what is actually in the data.

**Forbidden.** Options F, G, H.

The verdict on the Phase 4al admissibility question is
**CONDITIONAL / PARTIAL — admissible as a future descriptive
forensic / backtest-logic-audit research lane, with strict
boundaries**.

## 17. Explicit Non-Authorization Statement

Phase 4al does **NOT** authorize:

- Phase 4am;
- Phase 5;
- Phase 4 canonical;
- any other successor phase;
- any strategy spec;
- any backtest plan;
- any backtest;
- any data acquisition;
- any code change;
- any test change;
- any script change;
- any manifest change;
- any v003 dataset creation;
- any data modification;
- any paper / shadow operation;
- any live-readiness preparation;
- any deployment;
- any exchange-write capability;
- any production key creation;
- any credential creation, request, inspection, or storage;
- any authenticated API call;
- any private endpoint call;
- any public-endpoint call in code;
- any user stream;
- any WebSocket;
- any MCP / Graphify / `.mcp.json`;
- any verdict revision (R3 / R2 / F1 / D1-A / V2 / G1 / C1 / R1a /
  R1b-narrow / H0 / 5m thread closure all preserved verbatim);
- any project lock revision (§11.6 / §1.7.3 / Phase 3r §8 /
  Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 4j §11 / Phase 4k /
  Phase 4p / Phase 4q / Phase 4v / Phase 4w all preserved
  verbatim);
- any cooled-down-family reopening;
- any §7.E mark-price stop-domain authorization.

The recommended state remains **paused**. No next phase is
authorized.

## 18. Inputs Preserved

This memo preserves verbatim:

- the retained verdict ledger (H0 FRAMEWORK ANCHOR; R3 BASELINE-OF-
  RECORD; R1a / R1b-narrow RETAINED — NON-LEADING; R2 FAILED —
  §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL —
  other; 5m thread OPERATIONALLY CLOSED; V2 HARD REJECT — terminal
  for V2 first-spec; G1 HARD REJECT — terminal for G1 first-spec;
  C1 HARD REJECT — terminal for C1 first-spec);
- §11.6 = 8 bps per side; round-trip = 16 bps;
- §1.7.3 (0.25% risk per trade; 2× leverage cap; one position max;
  mark-price stops where applicable);
- Phase 3r §8 mark-price gap governance;
- Phase 3v §8 stop-trigger-domain governance;
- Phase 3w §6 / §7 / §8 break-even / EMA-slope / stagnation
  governance;
- Phase 4j §11 metrics OI-subset partial-eligibility rule;
- Phase 4k V2 backtest-plan methodology;
- Phase 4p G1 strategy-spec discipline;
- Phase 4q G1 backtest-plan methodology;
- Phase 4v C1 strategy-spec discipline;
- Phase 4w C1 backtest-plan methodology;
- the Phase 4ak-adopted M0 mechanism-admissibility gate (§5),
  post-null cooldown rule (§6), cooled-down families list (§7),
  and required M0 memo template (§8) of
  `docs/00-meta/m0-mechanism-admissibility-gate.md`;
- the Phase 4z 32-item framework as recommendation only (not
  adopted by Phase 4al);
- the Phase 4z M0–M7 redesign as recommendation only (not
  adopted);
- the Phase 4aa admissibility framework as recommendation only
  (not adopted);
- the Phase 4ab recommendations as recommendation only (not
  adopted).

## 19. Final Status

```text
Phase 4al type:                docs-only governance / admissibility memo
Candidate lane:                exit architecture / trade management /
                               payoff-distribution shaping
M0 verdict:                    CONDITIONAL / PARTIAL — admissible as a
                               future descriptive forensic /
                               backtest-logic-audit research lane,
                               with strict boundaries
Successor authorized:          NONE
Phase 4am authorized:          NO
Strategy work authorized:      NO
Backtest authorized:           NO
Data acquisition authorized:   NO
Verdict revision authorized:   NO
Lock revision authorized:      NO
Paper / shadow authorized:     NO
Live-readiness authorized:     NO
Exchange-write authorized:     NO
Credentials touched:           NO
Recommended project state:     remain paused
```
