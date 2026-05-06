# M0 Mechanism-Admissibility Gate

## 1. Status

```text
Status: Binding governance for future Prometheus research phases after Phase 4ak.
```

- **Adopted by:** Phase 4ak — M0 Governance Adoption Phase (merged on
  `main` after operator authorization).
- **Adoption scope:** prospective only.
- **Effective date:** Phase 4ak merge.
- **Effect on history:** none. M0 does **not** revise historical
  verdicts, does **not** retroactively invalidate or alter prior
  phases, and does **not** authorize any strategy, backtest,
  paper / shadow, live-readiness, or exchange-write activity.
- **Effect on existing locks:** none. M0 does not relax §11.6,
  §1.7.3, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8,
  Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, or
  Phase 4w. M0 does not relax any retained verdict.
- **Effect on existing recommendation-only governance:** unchanged.
  Phase 4z 32-item framework, Phase 4z M0–M7 mechanism-check
  redesign, Phase 4aa admissibility framework, and Phase 4ab
  recommendations remain recommendations only. The only Phase 4z /
  Phase 4ag / Phase 4aj fragments now binding are the upstream
  twelve-clause M0 gate restated in §5 below and the post-null
  cooldown rule restated in §6 below.

## 2. Purpose

M0 is an **upstream pre-discovery / pre-hypothesis admissibility
gate**. It applies before any future:

- fresh-hypothesis discovery memo (analogous to Phase 4n / 4t);
- hypothesis-spec memo (analogous to Phase 4o / 4u);
- strategy-spec memo (analogous to Phase 4g / 4p / 4v);
- backtest-plan memo (analogous to Phase 4k / 4q / 4w);
- analysis phase that proposes a new mechanism family;
- reopening of any cooled-down lane after a `NOT_SUPPORTED`
  feasibility verdict.

M0 is designed to prevent:

- old-strategy rescue (R3 / R2 / F1 / D1-A / V2 / G1 / C1 in any
  -prime / -narrow / -relaxed / -extension / hybrid form);
- post-hoc descriptor / threshold / horizon / symbol-universe
  tweaking after a feasibility null;
- price-only single-symbol continuation churn;
- opportunity-rate-only "we have enough trades" false positives
  that lack edge-rate evidence;
- mechanism claims without a predeclared baseline-superiority
  theory;
- backtest-first research (running a backtest and reasoning back
  to a mechanism story).

M0 is **not** a strategy spec, a backtest plan, a live-readiness
gate, or a deployment gate. Passing M0 does not authorize any of
those.

## 3. Relationship to Existing Governance

- **Phase 4m 18-requirement validity gate** (post-V2 strategy-
  research consolidation) remains binding for any future fresh
  hypothesis. M0 **complements** it; M0 does not replace it.
- **Phase 4t 10-dimension candidate scoring matrix** (post-G1
  fresh-hypothesis discovery) remains the project's discovery-
  method tool. M0 **complements** it; M0 does not replace it.
- **Phase 4z 32-item proposed admissibility framework, M0–M7
  mechanism-check redesign, discovery-memo template,
  strategy-spec template additions, backtest-plan template
  additions, and execution-report template additions** remain
  recommendations only. M0 operationalizes one **upstream
  fragment** of the Phase 4z proposal (the upstream theoretical-
  admissibility gate) without adopting the whole proposal.
- **Phase 4ag's original ten-clause M0** is a recommendation only.
  Phase 4ak's binding M0 is the **revised twelve-clause** version
  recorded in §5 below.
- **Phase 4aj M0 reconciliation memo** explained why the upstream
  twelve-clause M0 is the smallest meaningful adoption step;
  Phase 4ak adopts that M0 plus the post-null cooldown rule from
  Phase 4aj §9.

M0 does **not** replace existing strategy-spec, backtest-plan,
execution-report, or validation requirements. Future strategy
work, if it ever resumes, must clear:

```text
M0 (this document)
→ Phase 4m fresh-hypothesis validity gate
→ Phase 4t 10-dimension scoring matrix (inside discovery memo)
→ existing per-phase strategy-spec / backtest-plan / execution-report
  requirements (Phase 4g / 4p / 4v; Phase 4k / 4q / 4w;
  Phase 4l / 4r / 4x precedents)
```

in that order. M0 is the upstream filter; the rest remain in force
unchanged.

## 4. Applicability

### 4.A M0 is required before

- opening a new market-research lane (any mechanism-source family
  not previously documented as admissible);
- reopening a previously cooled-down lane (see §7 for current
  cooled-down families);
- proposing a fresh hypothesis;
- proposing a new mechanism source;
- proposing a strategy candidate (named or unnamed);
- converting feasibility evidence into a discovery memo;
- proposing any strategy-spec or backtest-plan path.

### 4.B M0 is **not** required for

- merge closeouts;
- purely archival documentation;
- typo fixes;
- narrow documentation maintenance with no research implications;
- governance adoption / governance reconciliation work that does
  **not** propose a market mechanism (this Phase 4ak is itself
  governance adoption and did not need to clear M0 to adopt M0);
- closeouts of previously authorized analysis-and-docs phases;
- reading / inspection of repository documentation;
- updates to `docs/00-meta/current-project-state.md` to record
  merges or closeouts.

### 4.C What M0 does not exempt

M0 does **not** exempt any future research from any other binding
governance. It does **not** authorize any future phase by itself.
Each future phase still requires explicit operator authorization.

## 5. The Twelve-Clause M0 Gate

Adopt the following twelve clauses as **binding prospective
governance** for any future memo whose purpose falls within §4.A.

A future M0 memo must address each clause explicitly. A clause may
return `not applicable` only if the memo's nature makes the clause
moot (e.g., a memo proposing a non-strategy research-process change
might have `not applicable` for clause 5). A `not applicable`
return must be justified in one sentence.

### M0.1 Mechanism source

State the mechanism source. If price-only on a tested substrate,
the proposal must explicitly justify why it is not within the
depleted price-only single-symbol continuation lane (see §7).

### M0.2 Non-price-only or structurally distinct source requirement

The mechanism source must be **non-price-only** or, if price-only,
**structurally distinct** from depleted lanes. Structurally
distinct means the proposal is not a parameter tweak, descriptor
tweak, interval tweak, symbol-universe expansion, or relabeled
version of a failed family. The proposal must articulate the
structural difference in theoretical terms before any data is
touched.

### M0.3 Baseline-superiority theory versus H0 and R3

State, in theoretical terms, why the candidate's primary condition
should produce positive expectancy versus an unconditioned baseline
that shares the same geometry. Derive a predicted Δ_R from
theoretical content. Commit to that predicted Δ_R as the
*expected outcome* of any future baseline test (Phase 4w M1 / M2
form for strategy candidates; equivalent baseline differential for
non-strategy mechanism claims).

### M0.4 Rejection-topology distance

State explicit distance from each of:

- R2 (V1 pullback-retest variant; cost-fragility rejection),
- F1 (mean-reversion after overextension; catastrophic-floor),
- D1-A (funding-aware contrarian; mechanism / framework mismatch),
- V2 (participation-confirmed breakout; design-stage),
- G1 (regime-first breakout continuation; gate × setup sparseness),
- C1 (volatility-contraction expansion breakout; fires-and-loses),
- any future rejected strategies added to this list after Phase 4ak.

Identify the **closest-prior-failure trap** and explain in
theoretical terms why the proposal is not that trap.

### M0.5 Cost-realism plausibility under §11.6

State the cost-realism plausibility under:

```text
§11.6 HIGH cost = 8 bps per side
round-trip = 16 bps
```

State predicted gross expectancy and expected cost burden. State
whether the proposal's expected profitability survives the
round-trip cost cell at the descriptive theoretical-content layer
before any backtest is contemplated.

### M0.6 Opportunity-rate plausibility

State the predeclared minimum candidate-event arrival rate, joint-
trigger arrival rate, and per-OOS-window trade-count floor. Derive
opportunity-rate floors from theoretical content; do **not** derive
them from prior failure forensic numbers (e.g., G1's 2.03% active
fraction, C1's 149 BTC OOS HIGH trade count, V2's zero-trade
result, Phase 4ai's `frac_selected ≈ 0.49`).

### M0.7 Edge-rate plausibility

State the predeclared minimum baseline differential the candidate
is *expected* to produce versus the closest unconditioned baseline,
independent of opportunity-rate. State the predicted bootstrap
confidence-interval lower bound (Phase 4w M1 / M2 form) or
equivalent descriptive edge-rate predicate (e.g., predeclared IC
floor; predeclared median-spread floor; predeclared
outperformance-fraction floor).

This clause must explicitly recognize:

```text
opportunity-rate viability is not edge-rate viability
```

C1 satisfied opportunity-rate (rate 3.33; 100% pass; 149 trades)
and failed edge-rate (M1 –0.244R CI strictly negative). Phase 4ai
satisfied opportunity-rate (rank-quality filter produces an answer
on ~ 45% of timestamps) and failed edge-rate (`frac_selected >
median ≈ 0.49`; spread ≤ 0; IC = 0). Both gates must be passed for
a future candidate to advance.

### M0.8 Data availability and integrity feasibility

State which datasets are required. State whether each is:

- **research-eligible PASS** (e.g., v002 BTCUSDT / ETHUSDT;
  Phase 4i 30m / 4h; Phase 4ac BTC 1h, ETH 1h, ADA full grid,
  SOL / XRP / ADA funding history under their PASS conditions);
- **governed partial** under Phase 4ad Rule A (mark-price invalid-
  window exclusion), Phase 4ad Rule B (SOL / XRP early-2022 kline
  gap scope; B1 default = `2022-04-03` common post-gap start),
  or Phase 4ad Rule C (PASS-only subset);
- **governed by Phase 4j §11** for metrics / OI subset partial
  eligibility;
- **unavailable and therefore blocking** (e.g., aggTrades, depth,
  order book, cross-venue, spot, mark-price 5m / 15m / 30m / 1h /
  4h `research_eligible: false` per Phase 3q / Phase 4ac).

No data acquisition is implied by passing M0. A future memo whose
data requirements include unavailable / blocked sources must declare
the data feasibility status as **blocking** rather than smuggling
in implied acquisition authorization.

### M0.9 Governance compatibility

State explicit compatibility with all binding project governance:

- §11.6 HIGH cost = 8 bps per side;
- §1.7.3 (0.25% risk per trade; 2× leverage cap; one position max;
  mark-price stops where applicable);
- Phase 3r §8 mark-price gap governance;
- Phase 3v §8 stop-trigger-domain governance;
- Phase 3w §6 / §7 / §8 break-even / EMA-slope / stagnation
  governance;
- Phase 4j §11 metrics OI-subset partial-eligibility rule (if
  metrics / OI involved);
- Phase 4k V2 backtest-plan methodology (if V2-adjacent);
- Phase 4p G1 strategy-spec discipline (if G1-adjacent);
- Phase 4q G1 backtest-plan methodology (if G1-adjacent);
- Phase 4v C1 strategy-spec discipline (if C1-adjacent);
- Phase 4w C1 backtest-plan methodology (if C1-adjacent);
- this M0 governance document;
- the post-null cooldown rule in §6 below;
- any later project locks.

A proposal that is incompatible with any of the above on its face
is structurally inadmissible at M0 and must terminate before
discovery.

### M0.10 Forbidden-rescue and anti-reduction check

State explicitly that the proposal does **not** reduce to:

- V2 / V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- G1 / G1-prime / G1-narrow / G1-extension / G1 hybrid;
- C1 / C1-prime / C1-extension / C1 hybrid;
- R2 / R1a / R1b-narrow rescue;
- F1 mean-reversion rescue;
- D1-A funding-trigger rescue;
- rank-then-V2 / G1 / C1 breakout under a wrapper;
- multi-position portfolio trading;
- 5m strategy / hybrid / variant;
- any prior-strategy alt-symbol rerun.

The check must name the closest rescue trap and articulate the
structural reason the proposal is not that trap. Naming alone is
not sufficient; a structural argument is required.

### M0.11 Pre-backtest falsification criteria

State what descriptive feasibility evidence would kill the
candidate **before** backtest grid budget is spent. The criterion
must be:

- predeclared at the M0 stage;
- substantive enough to terminate the candidate at the docs-only or
  analysis-and-docs stage if it fires;
- distinct from generic catastrophic-floor predicates (Phase 4k /
  4q / 4w CFP-1 through CFP-12 are downstream gates, not pre-
  backtest gates).

Examples (illustrative; each future memo must define its own):

- *for a cross-symbol mechanism:* a predeclared minimum cross-
  symbol IC floor on a specific descriptor that the proposal
  argues should outperform;
- *for a derivatives-context mechanism:* a predeclared minimum
  conditional-mean-return differential on a non-trigger
  diagnostic that should be present if the mechanism is real;
- *for a regime mechanism:* a predeclared minimum regime-active
  fraction *and* a predeclared minimum joint trigger-arrival rate
  derived from theory before any data is touched.

### M0.12 Post-null cooldown and non-authorization

State whether the mechanism family is currently cooled down by any
prior `NOT_SUPPORTED` result (see §7). If yes, the proposal must
identify a **materially new mechanism source** per §6 and explain
why it is not a forbidden post-null tweak.

State explicitly that passing M0 does **not** authorize:

- a strategy-spec memo;
- a backtest-plan memo;
- a backtest;
- paper / shadow operation;
- live-readiness preparation;
- deployment;
- exchange-write capability;
- production keys, authenticated APIs, private endpoints,
  public-endpoint calls in code, user stream, WebSocket, MCP,
  Graphify, `.mcp.json`, or credentials;
- any successor phase.

Each future phase still requires explicit operator authorization.

## 6. Post-Null Cooldown Rule

Adopt the following as **binding prospective governance**:

```text
After a predeclared feasibility phase returns NOT_SUPPORTED, the
same mechanism family may not be re-opened through:

  - parameter tweaks,
  - descriptor tweaks,
  - threshold tweaks,
  - symbol-universe expansions,
  - interval changes,
  - forward-horizon changes,
  - rank-quality-filter relaxations,
  - composite-weight reassignments,
  - rebalance-frequency changes,
  - or any other adjustment of the predeclared specification,

unless a future docs-only M0 memo first identifies a materially new
mechanism source that is independent of the failed descriptor
family.

Materially new means derived from external theory or external
evidence, not from observation of the failed phase's forensic
results.

The cooldown applies to the family, not only to the specific
candidate. Reopening requires a fresh upstream M0-style memo and
separate operator authorization.
```

### 6.A What "materially new" means in practice

A reopening memo must show that the new mechanism source is:

- **theoretically distinct** from the failed descriptor family
  (not just numerically different parameters);
- **derived from external evidence or external theory** that did
  not exist (or was not known to the project) at the time of the
  failed feasibility phase, OR derived from a distinct
  mechanism-source family in the Phase 4ag triage matrix;
- **independent of the failed phase's forensic results** (no use
  of `frac_selected ≈ 0.49`, `spread = -16.6 bps`, or any other
  Phase 4ai forensic number as a tuning input or threshold
  derivation, by direct analogy to Phase 4m's "no Phase 4l
  forensic numbers" discipline applied prospectively to all
  future feasibility nulls).

### 6.B What the cooldown does not block

The cooldown does **not** block:

- reading / inspecting the failed feasibility report;
- citing the failed feasibility report in future memos;
- using the failed feasibility report's descriptor enumeration as
  evidence of what has been tested (so future memos can avoid
  duplicating it);
- proposing a structurally distinct family in the same broad
  research direction (e.g., a future memo could propose a new
  cross-symbol mechanism that is not a descriptor tweak of
  Phase 4ai, provided §6.A conditions are met).

### 6.C Cooldown duration

The cooldown does not have a fixed duration. It remains in force
until a future M0 memo either (a) clears the cooldown by satisfying
§6.A or (b) is explicitly relaxed by a separately authorized
governance phase. There is no implicit decay over time.

## 7. Current Cooled-Down Families

The following list is current as of the Phase 4ak adoption boundary.
Future phases that find new evidence (e.g., a future feasibility
phase that returns `NOT_SUPPORTED`) should add their family to this
list at adoption time.

### 7.A Price-only single-symbol directional continuation

```text
Status: DEPLETED / NOT_RECOMMENDED
```

**Reason.** R2 (cost fragility), F1 (catastrophic-floor / bad
full-population payoff), V2 (design-stage incompatibility), G1
(regime-gate × setup sparseness), C1 (fires-and-loses contraction
anti-validation), plus Phase 4af's bar-level directional-persistence
null (post-expansion same-direction follow-through ≤ 0.50 across
all 80 (symbol, interval, N ∈ {1, 2, 4, 8}) tested cells).

**Effect under M0.** A future proposal in this family must clear
M0.1 and M0.2 with explicit structural justification. The
structural justification must articulate why the proposal is not
within the depleted lane, not merely that it differs in parameter
values.

### 7.B Cross-sectional trend / relative-strength symbol-selection under Phase 4ai descriptors

```text
Status: COOLED_DOWN_AFTER_NOT_SUPPORTED
```

**Reason.** Phase 4ai's predeclared composite ranking (0.7 ×
multi-horizon relative return + 0.3 × volatility-adjusted relative
strength) and predeclared rank-quality filter (top score ≥ 0.60;
top-second gap ≥ 0.05; top-symbol's raw 24h AND 72h returns > 0)
returned `NOT_SUPPORTED` on the five-symbol Phase 4ac core universe
under Phase 4ad Rule B1: `frac_selected > median ≈ 0.49` in every
primary cell, median `selected − median` spread ≤ 0 bps in every
primary cell, Spearman IC median = 0.0 in every primary cell.

**Blocked actions** (per §6 cooldown rule):

- no rerun with different rank-lookback windows
  (e.g., changing from `(4, 12, 24, 72, 168)` to other values);
- no rerun with different vol-adjustment lookbacks
  (e.g., changing from `(24, 72, 168)`);
- no rerun with different forward horizons
  (e.g., changing from `(4, 12, 24, 72)`);
- no symbol-universe expansion to BNB / DOGE / LINK / AVAX (the
  Phase 4aa deferred secondary watchlist) to "rescue" the lane;
- no rank-quality-filter relaxation (e.g., dropping the positive
  24h AND 72h gate; lowering the top-score threshold below 0.60;
  lowering the top-second gap below 0.05);
- no composite-weight reassignment (e.g., changing 0.7 / 0.3 to
  other weights);
- no rebalance-frequency change;
- no rank-then-breakout wrapper (silent reduction to V2 / G1 /
  C1-style single-symbol breakout under a ranking wrapper is
  separately forbidden by Phase 4ah / 4ai);
- no multi-position conversion (separately forbidden by Phase 4aa /
  4ah / 4ai and by §1.7.3 one-position-max).

**Reopening permitted only if** a future M0 memo identifies a
materially new mechanism source per §6.A.

### 7.C Derivatives-context directional lane

```text
Status: CONDITIONAL_ONLY / HIGH_D1-A_RESCUE_RISK
```

**Reason.** D1-A (Phase 3j) reached MECHANISM PASS / FRAMEWORK
FAIL — other; non-trigger conditions failed. Phase 4ag and Phase 4aj
recorded that derivatives-context features remain admissible only as
**context lenses**, never as directional triggers. A future proposal
in this family must explicitly distinguish itself from D1-A in
theoretical terms before passing M0.4 and M0.10.

### 7.D Microstructure / order-flow / liquidity-timing lane

```text
Status: NOT_RECOMMENDED_NOW
```

**Reason.** Heavy data burden (aggTrades / depth / order-book /
cross-venue all unavailable or unacquired); high cost-realism risk
at short horizons; not strengthened by any prior Prometheus
finding; Phase 4ag and Phase 4aj rated as `NOT_RECOMMENDED` at the
current boundary. A future proposal in this lane must clear M0.5
(cost realism) and M0.8 (data feasibility) on theoretical content
before any acquisition is authorized.

### 7.E Mark-price stop-domain / execution-realism lane

```text
Status: NOT_RECOMMENDED_NOW
```

**Reason.** Not directional. Phase 4ag rated this lane as
`NOT_RECOMMENDED now` because it does not address the directional-
edge problem identified by Phase 4af. It could become admissible
only if the operator explicitly chooses execution-realism research
over directional-edge research and authorizes it under Phase 4ad
Rule A predeclaration.

## 8. Required M0 Memo Template

Any future memo whose purpose falls within §4.A must follow this
template (or a clearly-labeled superset). Sections may be merged
where appropriate but no required section may be omitted.

1. **Purpose and non-authorization.** State the memo's docs-only
   nature; explicitly disclaim authorization of strategy-spec,
   backtest-plan, backtest, paper / shadow, live-readiness,
   deployment, exchange-write, production keys, authenticated APIs,
   private endpoints, MCP, Graphify, `.mcp.json`, or credentials.
2. **Mechanism source** (M0.1).
3. **Baseline-superiority theory** (M0.3) including the predicted
   Δ_R derivation and commitment.
4. **Rejection-topology distance matrix** (M0.4) covering R2, F1,
   D1-A, V2, G1, C1, and any later-rejected strategies, with
   closest-prior-failure trap named and structurally distinguished.
5. **Cost-realism thesis** (M0.5).
6. **Opportunity-rate thesis** (M0.6).
7. **Edge-rate thesis** (M0.7) — separate section, not folded into
   §6.
8. **Data availability and integrity scope** (M0.8).
9. **Governance compatibility** (M0.9) covering all binding locks
   and prior governance.
10. **Forbidden-rescue / anti-reduction declaration** (M0.10) with
    structural argument for the closest rescue trap.
11. **Pre-backtest falsification criteria** (M0.11).
12. **Cooldown check** (M0.12 + §7) — does the proposal touch any
    cooled-down family? If yes, identify the materially-new
    mechanism source per §6.A.
13. **Decision menu** (analogous to Phase 4n / 4t / 4ag / 4aj
    decision menus): Option A primary remain-paused; Option B
    merge-to-main-then-stop; conditional secondary option(s) for
    any future authorization; explicitly forbidden options.
14. **Recommendation.** One primary recommendation; at most one
    conditional secondary; or remain-paused.
15. **Explicit non-authorization statement.** Restate that passing
    M0 does not authorize any successor phase, any acquisition,
    any strategy work, any backtest, paper / shadow, live-
    readiness, deployment, or exchange-write.

## 9. Adoption Limits

Phase 4ak adopts only:

- the **revised twelve-clause M0 gate** (§5);
- the **post-null cooldown rule** (§6);
- the **current cooled-down families list** (§7) as of the
  Phase 4ak adoption boundary;
- the **required future M0 memo template** (§8).

Phase 4ak does **not** adopt:

- the full Phase 4z 32-item proposed admissibility framework;
- the Phase 4z proposed M0–M7 mechanism-check redesign wholesale;
- the Phase 4z proposed discovery-memo template;
- the Phase 4z proposed strategy-spec template additions;
- the Phase 4z proposed backtest-plan template additions;
- the Phase 4z proposed execution-report template additions;
- the Phase 4z five-rule no-rescue enforcement language as
  separate governance (the substantive content of those rules is
  preserved by M0.10 and §6 above);
- the Phase 4aa admissibility framework;
- the Phase 4ab recommendations.

Phase 4ak does **not** change historical verdicts. R3, R2, F1,
D1-A, V2, G1, C1, R1a, R1b-narrow, H0, and the 5m thread closure
remain exactly as recorded.

Phase 4ak does **not** authorize any new market research, any
strategy work, any backtest, any paper / shadow, any live-readiness
preparation, any deployment, any exchange-write capability, any
production keys, any authenticated APIs, any private endpoints, any
public-endpoint calls in code, any user stream, any WebSocket, any
MCP, any Graphify, any `.mcp.json`, or any credentials.

## 10. Final Recommended State

```text
remain paused unless the operator separately authorizes a future phase
```

Phase 4ak does **not** authorize Phase 4al.

Phase 4ak does **not** authorize any other successor phase.

The next step is operator-driven: the operator decides whether and
when to authorize any future phase. Until then, the project remains
paused at the Phase 4ak adoption boundary on `main` with M0 (this
document) as binding prospective governance for any future research
work.
