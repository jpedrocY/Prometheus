# Phase 4ag — Research-Program Pivot and Mechanism-Source Triage Memo

## 1. Purpose

Phase 4ag evaluates whether Prometheus should continue investigating
price-only single-symbol directional continuation, or pivot toward a
different mechanism-source family, in light of the cumulative
post-rejection evidence base assembled through Phase 4af.

This memo answers a single triage question:

```text
Given that price-only substrate research found movement but no
directional information, which non-price-only or cross-sectional
mechanism classes remain admissible for future Prometheus research?
```

Phase 4ag is **docs-only**.

Phase 4ag explicitly does **NOT**:

- acquire data,
- download data,
- call APIs,
- call exchange data endpoints,
- modify raw data,
- modify normalized data,
- create or modify any manifest,
- create v003 or any other dataset version,
- run analysis,
- run a backtest,
- run strategy diagnostics,
- rerun the Q1–Q7 5m diagnostic question set,
- compute strategy PnL,
- compute entry / exit returns,
- optimize any parameter,
- select thresholds for any future strategy,
- create a new strategy candidate,
- name a new strategy candidate,
- create a fresh-hypothesis discovery memo,
- create a hypothesis-spec memo,
- create a strategy-spec memo,
- create a backtest-plan memo,
- implement any runtime path,
- imply live-readiness,
- enable exchange-write capability.

Phase 4ag is the conditional secondary alternative the brief describes:
a research-program / mechanism-source triage memo authored after
Phase 4af's directional-persistence findings and after the project's
six terminal strategy rejections.

Phase 4ag's recommendations are **recommendations only** unless
separately adopted by the operator in a future authorization.

---

## 2. Current Evidence Baseline

### 2.1 Six-failure rejection topology

Prometheus has accumulated six terminal strategy rejections over the
V1 / F1 / D1-A / V2 / G1 / C1 research arcs. Each rejection rejects
along a structurally distinct axis. Phase 4ag must respect the full
topology before considering any pivot.

| Strategy | Family signature                          | Failure axis                                                       | Verdict reference            |
| -------- | ----------------------------------------- | ------------------------------------------------------------------ | ---------------------------- |
| R2       | V1 pullback-retest variant                | Cost fragility under §11.6 = 8 bps HIGH                            | Phase 2w §16.1               |
| F1       | Mean-reversion after overextension        | Catastrophic-floor expR with bad full-population expectancy        | Phase 3c §7.3 / Phase 3d-B2  |
| D1-A     | Funding-aware contrarian directional rule | Mechanism PASS / framework FAIL — non-trigger conditions failed    | Phase 3h §11.2 / Phase 3j    |
| V2       | Participation-confirmed breakout (8-feat) | Design-stage incompatibility — zero qualifying trades              | Phase 4l                     |
| G1       | Regime-first breakout continuation        | Regime-gate-meets-setup intersection sparseness — 0 OOS trades     | Phase 4r                     |
| C1       | Volatility-contraction expansion breakout | Fires-and-loses — contraction-tied transitions anti-validated      | Phase 4x                     |

Implications for any future mechanism-source family:

- A new candidate must be **structurally distinct** from this
  rejection topology, not a relabeled variant.
- Cost realism is binding (R2).
- Full-population mechanism expectancy must be tested, not just a
  favourable subset (F1).
- Funding alone is not a directional trigger (D1-A).
- Setup window, structural stop, target, and sizing must be
  co-designed (V2).
- A regime gate cannot be allowed to push joint trigger arrival
  toward zero (G1).
- A precondition that fires at adequate rate but produces losing
  trades fails the mechanism, not only the parameters (C1).

### 2.2 Alt-symbol substrate research arc (Phase 4aa → 4af)

After Phase 4z (research-process redesign recommendations) and the
Phase 4y review boundary, the operator authorized the alt-symbol
substrate-feasibility research arc:

| Phase   | Type                | Outcome                                                                 |
| ------- | ------------------- | ----------------------------------------------------------------------- |
| 4aa     | docs-only           | Alt-symbol market-selection / strategy-admissibility framework          |
| 4ab     | docs-only           | Alt-symbol data-requirements / feasibility plan                         |
| 4ac     | docs-and-data       | Public bulk-archive acquisition; 9 PASS / 26 FAIL strict integrity gate |
| 4ad     | docs-only           | Gap-governance future-use rules A / B / C                               |
| 4ae     | analysis-and-docs   | Substrate-feasibility metrics under Rule B1 common post-gap scope       |
| 4af     | analysis-and-docs   | Regime-continuity / directional-persistence metrics under Rule B1       |

Phase 4ae findings (descriptive substrate-feasibility evidence only):

- Cost-cushion ranking is consistent across all four intervals:
  `SOL > ADA > XRP > ETH > BTC`.
- BTC has the tightest cost cushion but the deepest notional turnover
  proxy and the most stable funding distribution.
- SOL has the widest funding distribution and the most frequent
  funding sign flips alongside the highest cost cushion.
- No single symbol dominated all dimensions.

Phase 4af findings (descriptive regime-continuity / directional
persistence evidence only):

- Trend-state self-transition probabilities are uniformly very high
  but uniform across symbols. There is **no differentiating
  cross-symbol trend-continuity edge**.
- EMA-slope self-transition probabilities are uniformly high.
  No differentiating edge.
- Post-expansion same-direction follow-through is **at or below 0.50
  across all 80 (symbol, interval, N ∈ {1, 2, 4, 8}) cells**.
- Bar-level sign persistence is consistently slightly below 0.50;
  lag-1 return autocorrelation is near zero on every cell.
- Volatility regimes are persistent but direction-agnostic.
- Cost-adjusted absolute-movement frequencies grow monotonically with
  cost cushion (SOL highest, BTC lowest), but **UP-state and
  DOWN-state conditional fractions are within ±2 percentage points of
  unconditional**. Trend conditioning provides **no cost-adjusted
  directional advantage**.

### 2.3 Cumulative synthesis

Combining the rejection topology and the substrate-feasibility arc
yields a stark synthesis statement:

```text
Price-only directional continuation / substrate research has produced
movement evidence across BTC / ETH / SOL / XRP / ADA, but it has not
produced directional-edge evidence on any tested cell.
```

This is the empirical premise that motivates the Phase 4ag triage.
Phase 4af's primary recommendation was already remain-paused; Phase 4ag
asks the prior question: even if research continues, *which mechanism
source has the best chance of supplying directional information that
price-only OHLC cannot supply on its own?*

---

## 3. External Research / Web Context

External literature search was **available** during Phase 4ag.
Citations below were retrieved via public web search and are
recorded verbatim from the search results.

External literature is used solely for **mechanism-source triage** and
for grounding the Phase 4ag recommendations. It does **not** authorize
data acquisition, hypothesis discovery, strategy specification,
backtesting, implementation, paper-shadow, live-readiness, or any
successor phase.

Phase 4ag did **not** broadly canvass the literature; the searches
below are intentionally narrow and are intended to test specific
mechanism-source families against credible academic / industry work.

### 3.A Cross-sectional / time-series momentum in crypto

Search query (May 2026): "cross-sectional momentum cryptocurrency
academic study 2024 transaction costs".

Representative references retrieved (verbatim from search results):

- Han, Kang, Ryu (2024) — *Time-Series and Cross-Sectional Momentum
  in the Cryptocurrency Market: A Comprehensive Analysis under
  Realistic Assumptions.* SSRN abstract\_id 4675565. Cited finding
  per the search result snippet: evidence of time-series momentum is
  strong, evidence of cross-sectional momentum is weak; the paper
  explicitly incorporates transaction costs (≈ 15 bps).
- Drogen, Hoffstein, Otte — *Cross-sectional Momentum in
  Cryptocurrency Markets.* SSRN abstract\_id 4322637.
- *Cryptocurrency market risk-managed momentum strategies* (2025) —
  ScienceDirect S1544612325011377. Cited: enhanced momentum
  strategies developed for equities may or may not retain efficacy
  in crypto.
- *Cross-sectional interactions in cryptocurrency returns* —
  ScienceDirect S1057521924007415. Cited: low liquidity raises
  transaction costs and contributes to persistence of anomalies.
- *Cryptocurrency momentum has (not) its moments* (2025) — Springer
  s11408-025-00474-9. Cited: crypto momentum is subject to severe
  crashes; volatility management may help.

Implications for Phase 4ag:

- The literature claims at least *some* momentum-shaped effect exists
  in crypto under realistic assumptions, but the strength is concentrated
  in time-series momentum more than cross-sectional momentum, and even
  the time-series effect is sensitive to transaction costs and
  drawdown / crash regimes.
- The Phase 4af bar-level / post-expansion finding that BTC / ETH / SOL /
  XRP / ADA show no directional persistence in the tested cells is
  not directly contradicted by this literature: the literature targets
  longer-horizon ranking effects across larger universes, not 15m–4h
  single-symbol bar-level continuation.
- A future cross-sectional or time-series-momentum-shaped Prometheus
  research lane would still need to clear §11.6 = 8 bps HIGH per
  side, would still need a one-position-max compatible framing
  (i.e. symbol-selection rather than portfolio-allocation), and
  would still need to predeclare an opportunity-rate / sample-size
  viability floor analogous to Phase 4u and Phase 4v.

### 3.B Crypto perpetual futures funding-rate factor research

Search query (May 2026): "crypto perpetual futures funding rate
factor strategy academic 2024".

Representative references retrieved (verbatim from search results):

- *Designing funding rates for perpetual futures in cryptocurrency
  markets.* arXiv 2506.08573.
- Ackerer, Hugonnier, Jermann — *Perpetual Futures Pricing.*
  Wharton finance preprint and Wiley Mathematical Finance
  10.1111/mafi.70018.
- *Exploring Risk and Return Profiles of Funding Rate Arbitrage on
  CEX and DEX.* ScienceDirect S2096720925000818.
- Inan — *Predictability of Funding Rates.* SSRN abstract\_id
  5576424.
- Kim, Park (2025) — Path-dependent funding rates as a practical
  alternative.
- Angeris et al. (2023) — Continuous-time arbitrage-free perpetual
  pricing.

Implications for Phase 4ag:

- The funding-rate literature is primarily about pricing,
  arbitrage replication, and CEX/DEX cash-and-carry arbitrage —
  not about funding-rate-as-directional-trigger for one-position
  contrarian or directional speculation.
- D1-A's Phase 3j framework failure (mechanism PASS / framework
  FAIL — other) is consistent with this: funding-as-context can
  carry information about positioning extremes, but funding-alone
  did not survive cost realism on the BTC / ETH non-trigger cells.
- Phase 4f §8 already cited BIS WP 1087 and the Liu / Tsyvinski
  literature in this area; nothing in the May-2026 search overturns
  the existing project understanding that funding remains a
  candidate **context lens**, not a candidate **directional
  trigger**.

### 3.C Other mechanism-source lanes

Phase 4ag did **not** perform fresh web searches for:

- order-flow / microstructure / liquidity-timing literature beyond
  what Phase 4f §8 already referenced (Easley / O'Hara / Yang /
  Zhang 2024);
- mark-price stop-domain / execution-realism literature beyond what
  Phase 3v §8 and the project's stop-loss policy already record;
- regime-classification / transition-momentum literature beyond what
  Phase 3m and Phase 4n already evaluated.

This is intentional. Phase 4ag's role is mechanism-source triage,
not exhaustive literature canvassing. Future docs-only follow-up
phases on individual lanes may, if separately authorized, perform
deeper literature work scoped to their lane.

---

## 4. Mechanism-Family Triage Matrix

The following triage matrix evaluates seven candidate mechanism-source
families against the Phase 4ag boundary criteria.

The verdict column uses the following labels:

```text
ADMISSIBLE_FOR_FUTURE_DOCS_ONLY_STUDY
CONDITIONAL_ONLY
NOT_RECOMMENDED
FORBIDDEN
REMAIN_PAUSED
```

These verdicts are **recommendations only** and do not authorize any
successor phase.

### Family 1 — Continue price-only single-symbol directional continuation

- **Description.** Continue investigating BTC- or ETH-centred
  breakout / continuation rules on OHLC + volume + ATR.
- **Plausibility.** Low after Phase 4af. The substrate has movement
  but no measurable directional persistence on the tested cells.
- **Repo evidence supporting.** None. R2 / V2 / G1 / C1 all rejected
  inside this family. Phase 4af persistence findings ≤ 0.50.
- **Repo evidence against.** Six terminal rejections within or
  adjacent to this family.
- **External evidence supporting.** Han / Kang / Ryu (2024)
  describe time-series momentum as the stronger crypto family but
  not specifically as bar-level single-symbol breakout
  continuation.
- **Required future data.** None new — existing committed datasets
  suffice.
- **Risk of old-strategy rescue.** **Very high.** Any new candidate
  in this family is structurally adjacent to V2 / G1 / C1.
- **Risk of overfitting / data mining.** High. The tested
  parameter spaces have already been combinatorially exhausted at
  V2 / G1 / C1 grids.
- **Cost-realism risk under §11.6.** High — R2 already failed here.
- **Opportunity-rate / sparsity risk.** High — G1 already failed
  here.
- **Governance compatibility.** Compatible with locks but
  governance gates (Phase 4m, Phase 4t, Phase 4z proposed M0) make
  re-entry difficult and rightly so.
- **Complexity.** Low.
- **Compatibility with 0.25% / 2× / one-position / mark-price
  stops.** Compatible.
- **Verdict.** `NOT_RECOMMENDED`.

### Family 2 — Cross-sectional trend / relative-strength / symbol-selection

- **Description.** Rank BTC / ETH / SOL / XRP / ADA (and possibly
  the deferred secondary watchlist) on multi-horizon trend or
  relative-strength signals; select one symbol to trade or none.
  Frame as **single-position symbol-selection**, not multi-position
  portfolio allocation.
- **Plausibility.** Moderate. Phase 4af shows directional
  persistence is uniform across symbols at the bar level but says
  *nothing* about ranking effects across symbols at longer
  horizons. The Han / Kang / Ryu (2024) paper directly addresses
  this lane.
- **Repo evidence supporting.** None directly — the project has
  not previously evaluated cross-sectional ranking. Substrate
  feasibility now exists for SOL / XRP / ADA klines under Phase 4ad
  Rule B1.
- **Repo evidence against.** None directly. Phase 4af bar-level
  null result does not bind cross-sectional ranking.
- **External evidence supporting.** Han / Kang / Ryu (2024); Drogen
  / Hoffstein / Otte; *Cryptocurrency momentum has (not) its
  moments* (2025).
- **Required future data.** Existing Phase 4ac PASS klines suffice
  for descriptive feasibility on BTC 1h / ETH 1h / ADA full-grid
  klines; SOL / XRP would require Phase 4ad Rule B1 governance
  scope (already defined).
- **Risk of old-strategy rescue.** Moderate. Cross-sectional
  ranking is structurally distinct from R2 / F1 / D1-A / V2 / G1 /
  C1 (none of those used cross-symbol ranking). The trap to
  avoid is **silent reduction to single-symbol breakout under a
  ranking wrapper** — i.e. picking a symbol via ranking and then
  trading V2-style or G1-style continuation on it.
- **Risk of overfitting / data mining.** Moderate. The literature
  already documents crypto momentum crashes and transaction-cost
  sensitivity; a Prometheus version would have to predeclare
  validation discipline.
- **Cost-realism risk under §11.6.** Moderate. Han / Kang / Ryu
  used 15 bps; §11.6 = 8 bps per side = 16 bps round-trip is
  comparable.
- **Opportunity-rate / sparsity risk.** Lower than G1 because
  ranking always produces an answer (top-ranked symbol exists at
  every rebalance), but rebalance frequency must be predeclared.
- **Governance compatibility.** Compatible with §1.7.3 if framed
  as symbol-selection (still one position max) and *not* as
  portfolio allocation. Phase 4j §11 unused. Phase 3v §8 / Phase
  3w §6 / §7 / §8 governance carries through unchanged.
- **Complexity.** Moderate. Requires a ranking layer above any
  trade-trigger layer. Acceptable for docs-only feasibility.
- **Compatibility with 0.25% / 2× / one-position / mark-price
  stops.** Yes, under symbol-selection framing.
- **Verdict.** `ADMISSIBLE_FOR_FUTURE_DOCS_ONLY_STUDY` — strongest
  candidate among non-paused options.

### Family 3 — Market-state / regime-transition momentum

- **Description.** Make momentum / continuation conditional on
  predeclared market-state transitions (e.g. UP→UP regime
  conditioning at a coarser timeframe), without recreating G1's
  state-machine sparsity trap.
- **Plausibility.** Moderate, but G1 was the project's first
  serious attempt and produced a sparsity-driven rejection. A
  market-state-transition lane would have to be designed as
  *post-conditioning* on market state rather than as a *gate* that
  suppresses entry evaluation.
- **Repo evidence supporting.** Phase 3m's regime-first framework
  memo (recommended remain-paused, not rejected); Phase 4af
  observation that volatility regimes are persistent.
- **Repo evidence against.** Phase 4r G1 rejection — the gate-and-
  trigger intersection problem is real, not theoretical.
  Phase 4af bar-level persistence ≤ 0.50 even after slope and
  trend-state conditioning.
- **External evidence supporting.** Some literature (e.g. Hattori
  2024 on UK-evening BTC peak; Han et al. on regime-aware
  momentum) was already cited in Phase 4f §8.
- **Required future data.** Existing data sufficient for
  feasibility; no acquisition required.
- **Risk of old-strategy rescue.** Moderate-to-high. The trap is
  **G1 with relaxed thresholds** under a different label.
- **Risk of overfitting.** Moderate.
- **Cost-realism risk under §11.6.** Moderate.
- **Opportunity-rate risk.** **High** — same failure mode as G1
  unless the design is fundamentally different.
- **Governance compatibility.** Compatible with locks.
- **Complexity.** Moderate.
- **Compatibility with 0.25% / 2× / one-position / mark-price
  stops.** Compatible.
- **Verdict.** `CONDITIONAL_ONLY` — admissible only if a future
  docs-only memo can articulate why it is **not** a G1 variant
  before a single line of code is written.

### Family 4 — Derivatives positioning / funding / OI / liquidations

- **Description.** Use funding-rate, open-interest, and (if later
  acquired) liquidation data as **context features** for a
  directional rule — not as a directional trigger.
- **Plausibility.** Moderate. D1-A failed when funding was the
  trigger. The literature treats funding as a pricing /
  arbitrage / replication mechanism more than a directional edge.
- **Repo evidence supporting.** Phase 4af descriptively confirmed
  cost-cushion ranking; SOL has the widest funding distribution
  and the most sign-flips, which is itself a feature.
- **Repo evidence against.** D1-A Verdict (mechanism PASS /
  framework FAIL — other). Phase 4j §11 metrics OI-subset rule
  exists and constrains OI use.
- **External evidence supporting.** Inan (2025) on funding-rate
  predictability; the perpetual-futures pricing literature.
- **Required future data.** Funding history exists for BTC / ETH /
  SOL / XRP / ADA in PASS state. Liquidations / aggTrades / OI
  metrics would require future acquisition.
- **Risk of old-strategy rescue.** **High** — must not become
  D1-A-prime.
- **Risk of overfitting.** Moderate.
- **Cost-realism risk under §11.6.** Moderate.
- **Opportunity-rate risk.** Moderate.
- **Governance compatibility.** Phase 4j §11 OI-subset rule
  preserved; Phase 3v §8 stop-trigger-domain governance preserved.
- **Complexity.** Moderate, but rises sharply if liquidations or
  aggTrades are needed.
- **Compatibility with 0.25% / 2× / one-position / mark-price
  stops.** Compatible.
- **Verdict.** `CONDITIONAL_ONLY` — admissible only as **context**,
  never as directional trigger; must explicitly distinguish itself
  from D1-A in any future memo.

### Family 5 — Microstructure / order-flow / liquidity-timing

- **Description.** Use intraday or finer-than-1m order-flow,
  trade-imbalance, depth, or cancellation features for short-horizon
  directional context.
- **Plausibility.** Plausible per Easley / O'Hara / Yang / Zhang
  (2024) and other microstructure literature, but the data
  burden is heavy.
- **Repo evidence supporting.** None directly. Phase 4i did not
  acquire aggTrades; Phase 4ac did not acquire order-book / tick.
- **Repo evidence against.** None directly. Phase 3n / 3o / 3p / 3t
  closed the 5m diagnostic-only thread; finer-than-5m has not
  been justified.
- **External evidence supporting.** Microstructure literature in
  general; specific crypto microstructure papers cited in
  Phase 4f §8.
- **Required future data.** **Significant** — aggTrades and / or
  depth / order-book data; substantial acquisition / governance
  burden.
- **Risk of old-strategy rescue.** Lower (no prior strategy used
  microstructure data).
- **Risk of overfitting.** **High** under HIGH cost when data is
  granular.
- **Cost-realism risk under §11.6.** Critical — short horizons
  amplify cost burden.
- **Opportunity-rate risk.** Moderate.
- **Governance compatibility.** Would require Phase 4ad Rule A
  analogue at higher resolution, plus new manifest governance.
- **Complexity.** **High.**
- **Compatibility with 0.25% / 2× / one-position / mark-price
  stops.** Compatible in principle.
- **Verdict.** `NOT_RECOMMENDED` at this boundary.

### Family 6 — Mark-price stop-domain / execution-realism

- **Description.** Apply Phase 4ad Rule A and Phase 3v §8
  governance to investigate stop-domain behaviour under
  mark-price triggers. This is **execution realism**, not
  directional edge.
- **Plausibility.** High for execution-realism research; **zero**
  for directional-edge research.
- **Repo evidence supporting.** Phase 3s Q6 D1-A mark-stop-lag
  finding (descriptive only); Phase 3v §8 stop-trigger-domain
  governance.
- **Repo evidence against.** None — but the mechanism cannot
  contribute directional information by construction.
- **External evidence supporting.** Project's existing Binance
  USDⓈ-M order-model documentation; perpetual-futures pricing
  literature on mark-price anchoring.
- **Required future data.** Mark-price klines that are currently
  `research_eligible: false` per Phase 4ac (BTC / ETH / SOL / XRP /
  ADA mark-price 30m / 1h / 4h all FAIL strict gate).
- **Risk of old-strategy rescue.** Low (this is not a strategy
  family).
- **Risk of overfitting.** Low.
- **Cost-realism risk.** N/A — not directional.
- **Opportunity-rate risk.** N/A — not directional.
- **Governance compatibility.** Phase 4ad Rule A explicitly
  prepared for this lane.
- **Complexity.** Low to moderate.
- **Compatibility with 0.25% / 2× / one-position / mark-price
  stops.** Directly relevant.
- **Verdict.** `NOT_RECOMMENDED` **as the next step** because it
  does not address the directional-edge problem; it could become
  admissible only if the operator explicitly chooses
  execution-realism research over directional-edge research.

### Family 7 — Remain paused

- **Description.** Take no action.
- **Plausibility.** Always procedurally valid.
- **Repo evidence supporting.** Phase 4af and Phase 4ae primary
  recommendations were already remain-paused; Phase 4z
  recommended no rescue path; Phase 4m / 4t validity and
  scoring frameworks favor *not* discovering candidates under
  pressure.
- **Repo evidence against.** None.
- **External evidence supporting.** None required.
- **Risk of old-strategy rescue.** Zero.
- **Risk of overfitting.** Zero.
- **Cost-realism risk.** N/A.
- **Opportunity-rate risk.** N/A.
- **Governance compatibility.** Trivially compatible.
- **Complexity.** Zero.
- **Compatibility with locks.** Trivially compatible.
- **Verdict.** `REMAIN_PAUSED` — primary recommendation.

### 4.X Summary

| #   | Family                                                | Verdict                                |
| --- | ----------------------------------------------------- | -------------------------------------- |
| 1   | Price-only single-symbol continuation                 | NOT_RECOMMENDED                        |
| 2   | Cross-sectional trend / relative-strength / selection | ADMISSIBLE_FOR_FUTURE_DOCS_ONLY_STUDY  |
| 3   | Market-state / regime-transition momentum             | CONDITIONAL_ONLY                       |
| 4   | Derivatives positioning (context only)                | CONDITIONAL_ONLY                       |
| 5   | Microstructure / order-flow                           | NOT_RECOMMENDED                        |
| 6   | Mark-price stop-domain / execution realism            | NOT_RECOMMENDED (now)                  |
| 7   | Remain paused                                         | REMAIN_PAUSED (primary recommendation) |

---

## 5. Serious Change Assessment

### 5.A Price-only continuation appears depleted

The project has now exhausted the obvious price-only continuation
sub-cases:

- V1 fixed-target + time-stop discipline (R3 baseline-of-record),
  which is conserved as a baseline but not led with;
- V1 pullback-retest variant (R2 — cost-fragile);
- V2 participation-confirmed breakout (V2 — design-stage
  incompatible);
- G1 regime-first breakout continuation (G1 — gate-trigger
  sparsity);
- C1 volatility-contraction-expansion breakout (C1 — fires-and-
  loses).

Phase 4af confirmed bar-level directional persistence ≤ 0.50 across
20 (symbol, interval) cells under Phase 4ad Rule B1. Additional
OHLC-only continuation / substrate-feasibility analysis has low
expected value at this boundary.

This does not retire price-only continuation forever. It does say
that further price-only-continuation work without a fundamentally new
theoretical premise is unlikely to clear Phase 4m / 4t / Phase 4z
gates.

### 5.B Cross-sectional symbol-selection is the cleanest serious pivot

The cross-sectional / relative-strength family is the only mechanism
family that:

1. is structurally distinct from every prior rejection,
2. has credible academic support (Han / Kang / Ryu 2024; Drogen /
   Hoffstein / Otte; the broader crypto-momentum literature),
3. can be framed under §1.7.3 one-position-max as **single-position
   symbol-selection**, *not* multi-position portfolio allocation,
4. uses currently-acquired Phase 4ac data without new acquisition,
5. respects all four governance label schemes prospectively
   (Phase 3v / 3w / 4j),
6. preserves §11.6 cost realism by construction, and
7. has predeclarable opportunity-rate / sample-size viability per
   Phase 4u / 4v precedent.

The avoidance pattern is straightforward:

```text
single-position cross-sectional selection
NOT
multi-position portfolio trading
NOT
single-symbol breakout under a ranking wrapper
```

The trap to avoid in any future Phase 4ah-equivalent memo is
*silent reduction*: ranking N symbols and then trading the top-ranked
symbol with V2-style or G1-style continuation rules. Any future memo
must explicitly forbid this reduction.

### 5.C Derivatives context is plausible but dangerous

Derivatives-context features (funding / OI / liquidations) might
contain incremental information, but the project already learned
from D1-A that funding-as-trigger fails framework promotion. Any
future research must:

- treat derivatives features as **context lenses**, not as
  directional triggers;
- comply with Phase 4j §11 metrics OI-subset rule;
- avoid any framing that recreates D1-A's trigger structure;
- cleanly separate funding-stress avoidance (defensive) from
  funding-position-extreme contrarian rules (D1-A-shaped — forbidden).

### 5.D Microstructure is plausible but expensive

Microstructure / order-flow / liquidity-timing research has the
heaviest data burden of all candidate lanes. AggTrades and /
or order-book / depth data would have to be acquired, governed
under a new gap-governance memo analogous to Phase 4ad Rule A,
and audited at a finer resolution than v002 / Phase 4ac.

Phase 4ag does not recommend opening this lane now. The
expected-value-to-cost ratio is too low at this boundary, and the
cost-realism risk under §11.6 is critical at short horizons.

### 5.E Mark-price stop-domain work is not directional

Mark-price stop-domain feasibility addresses execution realism, not
directional edge. It would be an appropriate next step *if* the
operator decides to deprioritize directional-edge research in favor
of execution-realism preparation work. But it cannot solve the
directional-edge problem identified by Phase 4af.

If the operator authorizes mark-price stop-domain feasibility, it
must be done under Phase 4ad Rule A predeclaration and must not be
framed as live-readiness prep. It must remain docs-only or
analysis-and-docs only, with no exchange-write implication.

---

## 6. Proposed M0 Mechanism-Admissibility Gate

The Phase 4z post-rejection research-process redesign memo proposed
an M0 theoretical-admissibility gate upstream of strategy-spec. Phase
4z's recommendations remain recommendations only. Phase 4ag does
**not** propose adopting Phase 4z wholesale as binding governance.

Phase 4ag does propose recording, as a Phase 4ag-only recommendation,
a narrow ten-clause M0 mechanism-admissibility gate that any future
fresh-hypothesis discovery memo or strategy-spec memo would have to
clear before a single line of strategy code is written.

### Proposed M0 clauses (Phase 4ag recommendation only)

1. **Mechanism source.** State the mechanism source in non-price-only
   or cross-sectional terms unless a specific theoretical reason
   exists to continue price-only.
2. **Baseline-superiority theory.** State why the candidate would
   beat R3 / H0, and why it is not a relabeled variant of R2 / F1 /
   D1-A / V2 / G1 / C1.
3. **Cost realism.** State the cost-realism plausibility under
   §11.6 = 8 bps HIGH per side (round-trip = 16 bps).
4. **Opportunity-rate plausibility.** State the predeclared
   minimum joint-trigger arrival rate per Phase 4u / 4v precedent.
5. **Design-family distance.** State distance from each of the six
   prior rejections, including the closest-prior-failure
   comparison (Phase 4z A31 analogue).
6. **Data feasibility.** State which Phase 4ac / Phase 4i / v002
   datasets are required and whether they are PASS or governed-
   PARTIAL under Phase 4ad / Phase 4j §11.
7. **Governance compatibility.** State conformance with §1.7.3,
   Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11.
8. **Forbidden-rescue check.** State explicitly that the candidate
   does not silently reduce to a prior failed strategy.
9. **Falsification criterion.** State what would falsify the
   mechanism *before* backtesting — i.e. what descriptive
   feasibility evidence would kill the candidate without spending
   backtest grid budget.
10. **Non-authorization.** State that passing M0 does **not**
    authorize a strategy-spec memo, a backtest-plan memo, a
    backtest, or any successor phase.

### Adoption status

Phase 4ag recommends recording these ten clauses as a **Phase 4ag
recommendation only**. Phase 4ag does **not** recommend adopting
them as binding governance during Phase 4ag itself.

If a future docs-only successor phase is authorized to formalize
mechanism-admissibility governance, the Phase 4ag M0 clauses, the
Phase 4z proposed admissibility framework, the Phase 4m 18-requirement
validity gate, and the Phase 4t 10-dimension scoring matrix should be
reconciled at that time.

---

## 7. Candidate Future Research Lanes

The following lanes are **not authorized** by Phase 4ag. They are
recorded for future operator selection.

### Lane A — Single-Position Cross-Sectional Trend / Relative-Strength Feasibility

- **Purpose.** Investigate whether multi-horizon ranking across
  BTC / ETH / SOL / XRP / ADA carries information that
  single-symbol price continuation lacks.
- **Type.** Docs-only first, possibly analysis-and-docs later if
  separately authorized.
- **Constraints.**
    - No strategy.
    - No backtest.
    - No portfolio allocation; preserve one-position max.
    - Frame as symbol-selection research.
    - Predeclare opportunity-rate viability and ranking-rebalance
      frequency before any data is touched.
    - Forbid silent reduction to single-symbol breakout under a
      ranking wrapper.
- **Possible future questions.**
    - Do top-ranked symbols by multi-horizon relative strength
      out-perform bottom-ranked symbols over fixed forward
      horizons descriptively?
    - Does volume-adjusted trend improve persistence across
      symbols where it does not within a symbol?
    - Does market-state conditioning improve cross-sectional
      ranking?
    - Does the effect survive HIGH cost plausibility at the
      descriptive level?

### Lane B — Derivatives-Context Incremental-Information Feasibility

- **Purpose.** Investigate whether funding / OI / (and possibly
  later liquidations) carry incremental directional context.
- **Type.** Docs-only.
- **Constraints.**
    - Funding-alone is **not** an admissible directional trigger;
      D1-A is forbidden to be rescued.
    - OI use must respect Phase 4j §11.
    - No strategy / no backtest at this layer.

### Lane C — Microstructure / Order-Flow Data-Admissibility Memo

- **Purpose.** Decide whether aggTrades / order-book / depth /
  liquidation data are worth acquiring at all in a future phase.
- **Type.** Docs-only.
- **Constraints.**
    - Heavy data burden.
    - No immediate acquisition.
    - No strategy / no backtest.
    - No live / execution inference.

### Lane D — Mark-Price Stop-Domain Feasibility

- **Purpose.** Apply Phase 4ad Rule A to stop-domain / mark-vs-
  trade behavior **only if** a directional mechanism later
  exists.
- **Type.** Docs-only or analysis-and-docs.
- **Constraints.**
    - Not directional.
    - Not recommended as immediate next step.
    - Acceptable only if the operator explicitly prioritizes
      execution realism over directional edge for this slice.

### Lane E — Remain Paused

Always procedurally valid. Phase 4ag's primary recommendation.

---

## 8. Recommended Next Operator Decision

Phase 4ag recommends:

```text
Primary recommendation:
Remain paused.

Conditional research-continuation recommendation:
If the operator wants to continue research, authorize a docs-only
Phase 4ah focused on single-position cross-sectional trend /
relative-strength feasibility and the M0 mechanism-admissibility
gate. Do NOT authorize strategy discovery yet. Do NOT authorize
old-strategy alt-symbol reruns. Do NOT authorize backtests. Do NOT
authorize new data acquisition yet. Do NOT authorize microstructure
data work yet. Do NOT authorize mark-price stop-domain work yet
unless the operator explicitly chooses execution-realism research
over directional-edge research.
```

Rationale:

- After Phase 4af, additional substrate-feasibility analysis on the
  same five-symbol universe at the same intervals is unlikely to
  change the directional-edge picture.
- Cross-sectional / relative-strength research is the cleanest
  Phase 4m / 4t / 4z-compatible non-paused option because it is
  structurally distinct from every prior rejection and uses
  already-acquired Phase 4ac data.
- Derivatives-context (Lane B) is plausible but harder to keep
  distinct from D1-A; not the cleanest first lane.
- Microstructure (Lane C) and mark-price stop-domain (Lane D) work
  is acceptable only under explicit operator framing and is not
  recommended as the next step.
- Remain-paused (Lane E) is always procedurally valid and remains
  the primary recommendation given that the project's six
  rejections already encode strong reasons for slow research
  cadence.

---

## 9. Decision Menu

### Option A — Remain paused

Primary recommendation. No further action.

### Option B — Merge Phase 4ag to main, then stop

Recommended if Phase 4ag is complete and the operator wants the
mechanism-source triage record committed without authorizing any
successor phase.

### Option C — Future docs-only Phase 4ah single-position cross-sectional trend / relative-strength feasibility memo

Conditional best research-continuation option if the operator wants
research progress.

### Option D — Future docs-only Phase 4ah derivatives-context incremental-information feasibility memo

Conditional, but higher D1-A rescue risk than Option C.

### Option E — Future docs-only Phase 4ah microstructure / order-flow data-admissibility memo

Not recommended now. High complexity / data burden.

### Option F — Future docs-only or analysis-and-docs mark-price stop-domain feasibility under Phase 4ad Rule A

Not recommended now unless the operator explicitly prioritizes
execution realism over directional edge.

### Option G — Fresh-hypothesis discovery memo

Not recommended now. Inconsistent with Phase 4z, Phase 4af, and
Phase 4ag findings.

### Option H — Strategy-spec / backtest / old-strategy alt-symbol rerun

Forbidden / not authorized. Old-strategy alt-symbol rescue is
explicitly forbidden by Phase 4aa, Phase 4ab, and reaffirmed by
Phase 4ag.

### Option I — Paper / shadow / live / exchange-write

Forbidden / not authorized. No validated strategy exists.
Phase-gate requirements per `docs/12-roadmap/phase-gates.md` are
not met.

---

## 10. Preserved Locks and Boundaries

Phase 4ag preserves every retained verdict and project lock
verbatim:

- H0 remains FRAMEWORK ANCHOR.
- R3 remains BASELINE-OF-RECORD.
- R1a remains RETAINED — NON-LEADING.
- R1b-narrow remains RETAINED — NON-LEADING.
- R2 remains FAILED — §11.6.
- F1 remains HARD REJECT.
- D1-A remains MECHANISM PASS / FRAMEWORK FAIL.
- 5m thread remains operationally CLOSED.
- V2 remains HARD REJECT — terminal for V2 first-spec.
- G1 remains HARD REJECT — terminal for G1 first-spec.
- C1 remains HARD REJECT — terminal for C1 first-spec.
- §11.6 HIGH cost = 8 bps per side preserved.
- §1.7.3 project-level locks preserved verbatim:
    - 0.25% risk per trade,
    - 2× leverage cap,
    - one position max,
    - mark-price stops where applicable.
- Phase 3r §8 mark-price gap governance preserved.
- Phase 3v §8 stop-trigger-domain governance preserved.
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
  governance preserved.
- Phase 4j §11 metrics OI-subset partial-eligibility rule preserved.
- Phase 4k V2 backtest-plan methodology preserved.
- Phase 4p G1 strategy-spec memo preserved.
- Phase 4q G1 backtest-plan methodology preserved.
- Phase 4v C1 strategy-spec memo preserved.
- Phase 4w C1 backtest-plan methodology preserved.
- Phase 4z recommendations remain recommendations only.
- Phase 4aa admissibility framework remains recommendation only.
- Phase 4ab recommendations remain recommendations only.
- Phase 4ac results remain data / integrity evidence only.
- Phase 4ad Rules A / B / C remain prospective analysis-time scope
  rules only.
- Phase 4ae findings remain descriptive substrate-feasibility
  evidence only.
- Phase 4af findings remain descriptive regime-continuity /
  directional-persistence evidence only.
- Phase 4ag recommendations remain recommendations only unless
  separately adopted later.

---

## 11. Explicit Non-Authorization Statement

Phase 4ag does **NOT** authorize:

- Phase 4ah,
- data acquisition,
- data download,
- API calls,
- endpoint calls,
- raw data modification,
- normalized data modification,
- manifest creation,
- manifest modification,
- v003 or any other dataset version,
- analysis execution,
- backtests,
- strategy diagnostics,
- Q1–Q7 rerun,
- strategy PnL computation,
- entry / exit return computation,
- parameter optimization,
- threshold selection,
- new strategy candidate creation,
- fresh-hypothesis discovery memo,
- hypothesis-spec memo,
- strategy-spec memo,
- backtest-plan memo,
- implementation,
- runtime code modification,
- test modification,
- script modification,
- old-strategy rescue (R2 / F1 / D1-A / V2 / G1 / C1 in any form,
  including alt-symbol reruns and any -prime / -narrow / -relaxed /
  hybrid variant),
- paper / shadow,
- live-readiness,
- deployment,
- production keys,
- authenticated APIs,
- private endpoints,
- public-endpoint calls in code,
- user stream,
- WebSocket,
- exchange-write,
- MCP,
- Graphify,
- `.mcp.json`,
- credentials,
- successor phase.

Phase 4ag is docs-only.

Phase 4ag's primary recommendation is **remain paused**.

Phase 4ag's recommendations are **recommendations only** unless
separately adopted in a future operator-authorized phase.
