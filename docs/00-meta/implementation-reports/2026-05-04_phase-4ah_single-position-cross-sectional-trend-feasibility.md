# Phase 4ah — Single-Position Cross-Sectional Trend / Relative-Strength Feasibility Memo

## 1. Purpose

Phase 4ah evaluates whether a future Prometheus research lane based on
**single-position cross-sectional trend / relative-strength /
symbol-selection** is theoretically and procedurally admissible after
Phase 4ag, while preserving the project's `one position max`
operational lock from `§1.7.3`.

Phase 4ah answers a single feasibility question:

```text
Can cross-sectional trend / relative-strength / symbol-selection be
expressed as single-position research that is structurally distinct
from the project's six rejected strategy designs (R2 / F1 / D1-A /
V2 / G1 / C1) and from multi-position portfolio trading, and that
respects §11.6 cost realism, §1.7.3 operational locks, and the
governance label schemes from Phase 3v / 3w and Phase 4j §11?
```

Phase 4ah is **docs-only**.

Phase 4ah explicitly does **NOT**:

- acquire data,
- download data,
- call APIs,
- call exchange data endpoints,
- modify raw or normalized data,
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
- name a strategy candidate,
- create a fresh-hypothesis discovery memo,
- create a hypothesis-spec memo,
- create a strategy-spec memo,
- create a backtest-plan memo,
- implement any runtime path,
- imply live-readiness,
- enable exchange-write capability.

Phase 4ah is the conditional secondary alternative anticipated by
Phase 4ag's mechanism-source triage matrix; it is now separately
authorized by the operator strictly as docs-only feasibility, **not**
as strategy discovery.

---

## 2. Relationship to Phase 4ag

Phase 4ag was the docs-only Research-Program Pivot and Mechanism-Source
Triage Memo merged at `fa72870`. Phase 4ag's substantive conclusions
relevant to Phase 4ah:

- Continued price-only single-symbol continuation was rated
  `NOT_RECOMMENDED`.
- Cross-sectional trend / relative-strength / symbol-selection was
  rated `ADMISSIBLE_FOR_FUTURE_DOCS_ONLY_STUDY` and identified as the
  strongest non-paused option of the seven Phase 4ag candidate
  families.
- Market-state / regime-transition momentum was rated
  `CONDITIONAL_ONLY` (G1 rescue trap).
- Derivatives positioning / funding / OI / liquidation context was
  rated `CONDITIONAL_ONLY` (D1-A rescue trap).
- Microstructure / order-flow was rated `NOT_RECOMMENDED` at this
  boundary.
- Mark-price stop-domain / execution-realism was rated
  `NOT_RECOMMENDED` now.
- **Remain paused was rated `REMAIN_PAUSED` and held as Phase 4ag's
  primary recommendation.**

Phase 4ag also recorded a proposed ten-clause M0 mechanism-
admissibility gate as a recommendation only, **not** as binding
governance, and explicitly did not authorize Phase 4ah.

Phase 4ah is now separately authorized by the operator. Phase 4ah
honors Phase 4ag's framing: it is docs-only feasibility evaluation,
not strategy discovery, not strategy spec, not backtest plan, not
data acquisition, not analysis execution.

---

## 3. Current Evidence Baseline

### 3.A Rejection topology

A future cross-sectional lane must be structurally distinct from
each of the six terminal strategy rejections:

| Strategy | Family signature                          | Failure axis                                         |
| -------- | ----------------------------------------- | ---------------------------------------------------- |
| R2       | V1 pullback-retest variant                | Cost fragility under §11.6 = 8 bps HIGH              |
| F1       | Mean-reversion after overextension        | Catastrophic-floor expR; bad full-population payoff  |
| D1-A     | Funding-aware contrarian directional rule | Mechanism PASS / framework FAIL — non-trigger fails  |
| V2       | Participation-confirmed breakout (8-feat) | Design-stage incompatibility; zero qualifying trades |
| G1       | Regime-first breakout continuation        | Regime-gate × setup intersection sparseness          |
| C1       | Volatility-contraction expansion breakout | Fires-and-loses contraction anti-validation          |

Adjacency hazards a Phase 4ah-shaped future lane must avoid:

- **R2 / R1a-style adjacency.** A relative-strength filter is *not*
  a substitute for a pullback-retest entry rule; do not allow a
  ranking layer to act as a per-bar volatility-percentile bolt-on
  on top of a V1-shaped breakout.
- **V2 adjacency.** Cross-sectional ranking is *not* a participation-
  feature AND-chain. The ranking output is a single decision: which
  symbol (or none) to focus future research attention on.
- **G1 adjacency.** A relative-strength filter is *not* a top-level
  state machine that suppresses entry evaluation on most bars.
  Ranking must produce a ranked output for every rebalance period.
- **C1 adjacency.** Ranking is *not* a contraction-to-expansion
  transition rule. Ranking is computed on prior-completed bars
  using fixed descriptors.
- **D1-A adjacency.** Funding context cannot become a directional
  trigger inside a ranking layer.
- **F1 adjacency.** Top-ranking is not "pick the symbol that just
  fell the most so it will mean-revert."

### 3.B Phase 4ae / Phase 4af substrate evidence

Phase 4ae found cost-cushion ranking consistent across all four
intervals (15m / 30m / 1h / 4h):

```text
SOL > ADA > XRP > ETH > BTC
```

with no single symbol dominating all dimensions (BTC has the
deepest notional turnover proxy and most stable funding; SOL has
the widest funding distribution and the most frequent funding
sign flips alongside the highest cost cushion).

Phase 4af found, on the same five-symbol set under Phase 4ad
Rule B1 common post-gap scope (`2022-04-03 00:00 UTC` through
`2026-04-30 23:59:59 UTC`):

- Trend-state self-transition probabilities are uniformly very
  high (`P(UP self)` 0.919–0.940; `P(DOWN self)` 0.923–0.940)
  across all 20 cells. **Uniform across symbols** — no
  differentiating cross-symbol trend-continuity edge.
- EMA-slope self-transition probabilities are uniformly very high
  (0.94–0.96 both directions). No differentiating edge.
- Post-expansion same-direction follow-through is **at or below
  0.50 across all 80 (symbol, interval, N ∈ {1, 2, 4, 8})
  cells**.
- Bar-level `frac_sign_repeats_next_1` is consistently slightly
  below 0.50 and lag-1 return autocorrelation is near zero on
  every cell.
- Volatility-regime self-transition probabilities are uniformly
  high (0.91–0.94); high-vol regime overlap is direction-agnostic.
- UP-state and DOWN-state cost-adjusted-move conditional fractions
  are within ±2 percentage points of unconditional.

### 3.C Synthesis

Combining the rejection topology and the substrate-feasibility
evidence yields the Phase 4ah premise:

```text
Single-symbol price-only continuation appears depleted; cross-
sectional selection is interesting because it asks a different
question — not "does this single symbol's history predict its own
direction?" but "does ranking N symbols against each other supply
information that no single-symbol substrate metric supplies?"
```

The Phase 4af null result is a *bar-level same-symbol persistence*
null. It does not bind a *cross-symbol relative-strength* test
because Phase 4af did not compute cross-symbol comparisons. This
is the Phase 4ah feasibility opening — and also its primary
methodological hazard, because a future feasibility study must not
inadvertently reproduce the Phase 4af null under a ranking wrapper.

---

## 4. External Literature / Web Context

External literature search was **available** during Phase 4ah.
Citations below were retrieved via public web search and recorded
verbatim from search results. External literature is used solely
for feasibility context. It does **not** authorize data acquisition,
analysis execution, hypothesis discovery, strategy specification,
backtesting, paper-shadow, live-readiness, or any successor phase.

### 4.A Time-series momentum versus cross-sectional momentum in crypto

Search query (May 2026): "time-series momentum cryptocurrency Han
Kang Ryu transaction costs realistic assumptions".

Headline result:

- **Han, Kang, Ryu (2023, posted Dec 2023; available SSRN
  4675565)** — *Time-Series and Cross-Sectional Momentum in the
  Cryptocurrency Market: A Comprehensive Analysis under Realistic
  Assumptions.*
    - Cited finding (verbatim from search-result snippet):
      "Evidence of time-series momentum is strong, whereas
      evidence of cross-sectional momentum is weak."
    - Cited best-case result: a strategy that buys the market
      when its look-back-period return falls within the top
      third of historical returns; best at 28-day lookback /
      5-day holding; reported Sharpe ≈ 1.51 in their setup.
    - Methodology notes from the snippet: tested only on
      Binance futures coins; accounts for margin mode and
      liquidation; marks-to-market portfolios daily; uses
      transaction costs (~15 bps in their setup).

Implication for Phase 4ah:

- The strongest crypto-momentum signal in the recent literature
  is **time-series**, not cross-sectional.
- Han / Kang / Ryu's "cross-sectional momentum is weak" claim is
  about **traditional long-short portfolio cross-sectional
  momentum** (top decile minus bottom decile in a multi-asset
  universe), not about *single-position symbol-selection by
  relative strength*.
- Single-position symbol-selection — "rank N symbols, then pick
  the top-ranked symbol or none" — is structurally closer to a
  **per-symbol time-series momentum filter applied across a
  small universe**, with an additional "best-of-N" filter, than
  it is to a long-short cross-sectional spread strategy.
- This reframe is what makes the Phase 4ag-recommended lane
  potentially admissible: it inherits the relatively stronger
  time-series-momentum literature while still preserving
  Prometheus's `one position max` lock.
- The reframe carries its own hazard. Selecting the *best of N*
  symbols introduces a selection-bias dimension that is not
  present in either pure single-symbol TSMOM or pure long-short
  cross-sectional. Any future feasibility memo must predeclare
  how this selection bias is handled.

### 4.B Crash / drawdown / volatility-managed crypto momentum

Search query (May 2026): "cryptocurrency momentum crash drawdown
volatility-managed strategy 2024 2025".

Representative references:

- *Cryptocurrency momentum has (not) its moments* (2025) —
  Springer s11408-025-00474-9. Cited: cryptocurrency momentum is
  subject to severe crashes among large-cap cryptocurrencies and
  equal-weighted momentum portfolios; momentum crashes are
  partly forecastable and tend to occur in panic states
  following market declines when volatility is high; volatility
  management is a useful tool for mitigating these crashes.
- *Cryptocurrency market risk-managed momentum strategies*
  (2025) — ScienceDirect S1544612325011377. Cited: risk
  management increases average weekly returns from 3.18% to
  3.47% and annualised Sharpe from 1.12 to 1.42 in their
  reported setup; improvements come from augmented returns
  rather than from mitigating downside risk (a notable
  distinction from equity momentum).
- *Cryptocurrency Volume-Weighted Time Series Momentum* —
  Huang / Sangiorgi / Urquhart (SSRN 4825389). Volume-weighted
  variants are an active topic in this literature.

Implications:

- Even if a single-position symbol-selection lane has
  theoretical traction via a TSMOM-style underlying mechanism,
  crash / drawdown risk is a **first-class feasibility concern**.
- Volatility-managed weighting is a documented mitigation in the
  portfolio literature, but it is **not directly portable to
  single-position selection** because it relies on weighted
  combinations across multiple holdings.
- A Prometheus future feasibility study that cannot use
  multi-position vol-targeting must instead rely on
  symbol-level entry filtering and turnover control — and must
  predeclare both before any analysis runs.

### 4.C Single-asset versus portfolio-factor framing

Search query (May 2026): "single-asset symbol selection relative
strength versus portfolio momentum factor crypto".

Snippet-verbatim observations:

- Time-series momentum analyzes an asset's own historical
  performance (e.g. position relative to its 200-day moving
  average); cross-sectional momentum compares relative
  performance across assets. Time-series excels in clear
  trending markets; cross-sectional shines during sector
  rotation (per the surveyed snippet).
- Practitioner relative-strength models *do* exist as
  single-asset selection (e.g. Portfolio Visualizer's tactical
  allocation models; Kaiko / Hashdex factor product; Hashdex
  HAMO).
- Even where these products exist, they are typically
  multi-position by construction (`top N`, weighted by risk
  parity × momentum), which is *exactly the framing
  Prometheus's `one position max` lock forbids*.

Implications:

- The single-position selection framing Phase 4ah is being
  asked to evaluate is not the *default* framing in the
  practitioner literature. The default is multi-position risk-
  parity-weighted top-N.
- For Prometheus to do single-position selection cleanly, it
  must reframe ranking as "select-one-or-none" rather than as
  "top-N portfolio".
- This reframe is what makes the Phase 4ag recommendation
  potentially compatible with the `one position max` lock — but
  the literature does not directly validate this reframe. Any
  future feasibility study must therefore design the ranking
  output explicitly, rather than inheriting it from a portfolio-
  literature template.

### 4.D Summary of literature implications

```text
- Time-series momentum is the better-documented mechanism source
  in crypto.
- Cross-sectional long-short factor evidence is mixed at best.
- Crash / drawdown risk is real and is partly forecastable.
- Volatility-managed weighting (the standard mitigation) is a
  multi-position technique that does not directly port to single-
  position selection.
- Practitioner relative-strength models are typically multi-
  position; Prometheus's reframe to single-position is novel and
  is its own design problem.
- Cost-realism remains binding (§11.6 = 8 bps HIGH per side).
```

These implications shape the rest of the Phase 4ah memo: the lane
is *admissible for future docs-only study* but it is **not**
strongly endorsed by literature, and its main attraction for
Prometheus is **structural distinctness from the six prior
rejections** rather than literature consensus on edge.

---

## 5. Mechanism Definition

The future mechanism family Phase 4ah evaluates is defined as:

```text
Single-position cross-sectional trend / relative-strength symbol selection.
```

It means:

- Rank a fixed, predeclared symbol universe at predeclared
  rebalance points using predeclared trend / relative-strength
  descriptors computed only on prior-completed bars.
- Ask whether high-ranked symbols have *descriptively better
  forward behavior* than low-ranked symbols across fixed forward
  horizons, measured under §11.6 = 8 bps HIGH cost realism.
- Allow the output of any rebalance period to be "no symbol"
  whenever no symbol passes a predeclared rank-quality filter.
- Preserve `one position max` by structuring the ranking layer to
  produce **at most one selected symbol** for future hypothetical
  consideration.
- Keep ranking computation strictly separate from any future
  entry / exit rule. The ranking layer's job is "which symbol (or
  none)?". Any future entry / exit rule is a separate concern not
  designed by Phase 4ah.

It does **NOT** mean:

- Multi-position portfolio trading.
- Market-neutral long-short portfolios.
- Risk-parity weighted top-N baskets.
- Old-strategy reruns on selected symbols (R3 / R2 / F1 / D1-A /
  V2 / G1 / C1 in any -prime / -narrow / hybrid form).
- A ranking wrapper around V2 / G1 / C1 breakout rules.
- A strategy spec.
- A backtest.
- Live symbol rotation.
- A real or paper exchange-side path.
- An implementation slice.

The mechanism is fully separable from any trade trigger. Whether
the selected symbol is then approached with structural breakout,
mean-reversion, contrarian, or any other entry / exit logic is
*outside Phase 4ah's scope* and must remain outside the scope of
any future Phase 4ai feasibility memo.

---

## 6. Proposed Future Research Universe

The Phase 4ah recommended future universe (not authorized by
Phase 4ah) is the **fixed five-symbol Phase 4ac core set**:

```text
BTCUSDT
ETHUSDT
SOLUSDT
XRPUSDT
ADAUSDT
```

Rationale:

- Phase 4ac, Phase 4ad, Phase 4ae, and Phase 4af already govern
  this set under the Phase 4ad Rule B1 common-post-gap scope
  (`2022-04-03 00:00 UTC` through `2026-04-30 23:59:59 UTC`). No
  new manifest governance is required.
- The set is large enough to support five-way ranking and small
  enough to make symbol-mining harder.
- The set already has cost-cushion / regime-continuity descriptive
  evidence on file.

The Phase 4aa deferred secondary watchlist:

```text
BNBUSDT
DOGEUSDT
LINKUSDT
AVAXUSDT
```

should remain **deferred**:

- Acquisition is unauthorized; expanding the universe without
  acquisition would mean reusing existing data, which the
  watchlist does not have governed coverage for.
- A larger universe also raises symbol-mining and multiple-
  testing risk.
- A future operator-authorized data-requirements / acquisition
  phase would have to revisit Phase 4aa / 4ab governance and
  apply Phase 4ad-style gap-governance to any new families.

Recommendation for any future Phase 4ai-equivalent feasibility:

- **Predeclare the universe before any descriptors are
  computed.**
- Do **not** mine the universe by adding or dropping symbols
  after seeing intermediate results.
- Do **not** redefine the universe based on a single symbol's
  "interesting" forward behavior.

---

## 7. Proposed Future Ranking Families

The following ranking-descriptor families are recorded as **possible
future inputs** to a docs-only or analysis-and-docs feasibility
phase. **Phase 4ah does not compute, evaluate empirically, or
authorize any of them.**

### 7.A Multi-horizon relative return

Examples:

- 4h cumulative return rank.
- 12h cumulative return rank.
- 1d cumulative return rank.
- 3d cumulative return rank.
- 7d cumulative return rank.
- Composite / ensemble rank (e.g. average of per-horizon ranks).

Why it might be meaningful:

- Most directly mirrors the Han / Kang / Ryu (2023) crypto-
  TSMOM finding (28d / 5d holding best in their setup) when
  interpreted as a per-symbol input to a "best-of-N"
  selection.
- Trivially preserves prior-completed-bar discipline.

Repo evidence supporting:

- Phase 4af bar-level persistence is ≤ 0.50, but Phase 4af did
  not test 4h–7d cumulative-return ranking across symbols.

Repo evidence challenging:

- Phase 4af persistence patterns are *uniform across symbols*
  at the 15m–4h bar level. If that uniformity extends to longer
  horizons, multi-horizon return ranking would not produce
  meaningful cross-symbol differentiation either.

Risk of overfitting:

- Moderate. The horizon-set is the main parameter and must be
  predeclared before any data is touched.

Cost-realism implication:

- Cost burden depends on rebalance frequency, not on horizon
  depth. A 1d-rebalance with a multi-horizon rank is cheaper
  than a 4h-rebalance. Predeclaration of rebalance frequency is
  mandatory.

Risk of recreating rejected strategy families:

- Low if the ranking stays at the symbol-selection layer.
  High if the selected symbol is then traded with V2 / G1 / C1
  breakout rules.

### 7.B Relative trend state

Examples:

- Distance above/below EMA(50).
- EMA(50) versus EMA(200) state, ranked by gap magnitude.
- EMA-slope rank.
- Trend-state-persistence rank (Phase 4af-style P(self) rank).

Why it might be meaningful:

- Trend-state and EMA-slope persistence are *uniformly high*
  across symbols in Phase 4af; ranking the *gap magnitude*
  rather than the persistence may still differentiate.

Repo evidence challenging:

- Phase 4af shows trend-state self-transition probability does
  not differ across symbols. Ranking on the *gap* dimension is
  the only descriptor in this family that has descriptive
  freedom.

Risk of overfitting:

- Moderate. EMA windows are a parameter; predeclaration is
  mandatory.

Risk of recreating rejected strategy families:

- Moderate. EMA-state was used in V1 / G1 backtests as a bias
  filter; reusing EMA windows in a ranking layer is acceptable
  *only if* the ranking output drives symbol selection rather
  than a trade trigger.

### 7.C Volatility-adjusted relative strength

Examples:

- Return / ATR(20) rank.
- Return / realized-volatility rank.
- Cumulative-return-over-median-range rank.

Why it might be meaningful:

- Phase 4ae's cost-cushion ranking `SOL > ADA > XRP > ETH >
  BTC` is itself a vol-relative metric. A vol-adjusted
  relative-strength rank could either reproduce this static
  ranking (degenerate) or differentiate from it dynamically.
- The Han / Kang / Ryu literature uses volatility scaling
  internally; a vol-adjusted relative-strength rank is the
  family closest to documented research practice.

Risk of overfitting:

- Moderate. ATR / realized-volatility windows are parameters.

Cost-realism implication:

- Vol adjustment can reduce false ranking signals during
  high-vol regimes; this is the Phase 4ag derivatives-context
  D1-A-rescue trap analogue and must be designed not to drift
  into "rank by inverse vol" alone.

### 7.D Volume / notional confirmation

Examples:

- Rank of notional turnover change.
- Rank of volume expansion relative to own history.
- Relative-strength with a minimum liquidity screen.

Why it might be meaningful:

- The Huang / Sangiorgi / Urquhart (SSRN 4825389) crypto
  volume-weighted TSMOM literature is an active sub-area.
- BTC's 1–2 order-of-magnitude turnover dominance from
  Phase 4ae would naturally bias raw notional ranking; the
  feasibility question is whether *relative* notional change
  (versus own history) is informative.

Risk of overfitting:

- Moderate. Volume comparison windows are parameters.

Risk of recreating rejected strategy families:

- Moderate. V2 used per-bar volume confirmation as part of an
  AND-chain. Volume in a ranking layer must produce a
  *cross-symbol* output, not a per-bar entry trigger.

### 7.E Market-state conditional ranking

Examples:

- Rank only when broad market state is coherent (e.g. BTC and
  ETH in same trend state).
- Rank only when a global crypto regime indicator is favorable.
- Rank conditional on volatility regime.

Why it might be meaningful:

- Phase 3m's regime-first framework memo and the literature on
  partly-forecastable crypto-momentum crashes both suggest that
  market-state conditioning may matter.

Repo evidence challenging:

- Phase 4r G1 was a top-level state-machine regime gate and
  failed at the gate-and-trigger intersection. A conditioning
  layer that suppresses entire rebalance periods can recreate
  G1's failure mode by suppressing too many rebalance arrivals.

Risk of overfitting:

- High. Regime conditioning has many free parameters and is
  the most G1-adjacent family in this list.

Risk of recreating rejected strategy families:

- **High.** Any future feasibility memo using this family
  must predeclare exactly how it differs from G1's regime
  gate, with a preregistered active-fraction floor analogous
  to Phase 4q's CFP-9 threshold.

### 7.X Cross-family summary

| Family                                    | Recreation risk | Cost-realism risk | Distinctiveness from prior rejects |
| ----------------------------------------- | --------------- | ----------------- | ---------------------------------- |
| A — Multi-horizon relative return         | Low             | Moderate          | High                                |
| B — Relative trend state                  | Moderate        | Moderate          | Moderate                            |
| C — Volatility-adjusted relative strength | Moderate        | Moderate          | High                                |
| D — Volume / notional confirmation        | Moderate        | Moderate          | High                                |
| E — Market-state conditional ranking      | High (G1)       | Moderate          | Moderate                            |

The cleanest first-pass Phase 4ai-equivalent design would
predeclare a **small composite** drawn primarily from families A
and C, optionally including a single liquidity screen from family
D, with families B and E either omitted entirely or used only for
secondary descriptive comparisons. Phase 4ah does not authorize
this; it only records the ordering.

---

## 8. Anti-Rescue / Anti-Reduction Rules

Any future research that proceeds beyond Phase 4ah must respect
the following binding rules. They are recorded here as Phase 4ah
recommendations for future operator-authorized phases.

1. **No old-strategy alt-symbol reruns.** R3 / R2 / F1 / D1-A /
   V2 / G1 / C1 in any form (including any -prime / -narrow /
   -relaxed / hybrid variant) must not be evaluated on selected
   symbols.
2. **No "rank first, then run V2 / G1 / C1 breakout" structure.**
   Ranking is a symbol-selection layer; it does not become an
   entry trigger by composition with a rejected design.
3. **No threshold tuning after observing ranking results.**
   Ranking descriptors, horizons, and rebalance frequency must
   be predeclared before any data is touched.
4. **No selecting a symbol because it makes an old failed design
   look better.** The motivation for cross-sectional research is
   structural distinctness, not retrospective rescue.
5. **No strategy candidate may be named in Phase 4ah.** Phase 4ah
   does not name a candidate. Phase 4ai (if ever authorized) does
   not name a candidate. Naming a candidate is the responsibility
   of a separately authorized fresh-hypothesis discovery memo
   *if* the project ever reaches that point.
6. **Fixed predeclared ranking descriptors.** No post-hoc
   descriptor selection.
7. **Fixed predeclared symbol universe.** No post-hoc symbol
   addition or removal.
8. **Fixed predeclared rebalance frequency.** No post-hoc
   frequency tuning.
9. **Fixed predeclared comparison protocol.** Top-rank-versus-rest
   and top-rank-versus-median descriptive comparisons must be
   predeclared before any data is touched.
10. **Preserve the option of "no admissible cross-sectional
    effect."** Any future feasibility memo must define what
    descriptive output would falsify the lane, and that
    falsification criterion must be predeclared rather than
    selected after results are seen.
11. **Preserve `one position max`.** No version of this lane
    becomes a multi-position study at any point.
12. **Preserve §11.6 = 8 bps HIGH per side cost realism.** No
    descriptor or comparison may relax the cost gate.

---

## 9. M0 Mechanism-Admissibility Application (Non-Binding)

Phase 4ag recorded a proposed ten-clause M0 mechanism-admissibility
gate as a **recommendation only**, not as binding governance.
Phase 4ah applies M0 as a non-binding diagnostic checklist to the
single-position cross-sectional lane.

Phase 4ah does **not** adopt M0 as binding governance. Adoption
would require a separately authorized future governance phase
that reconciles M0 with Phase 4z / Phase 4m / Phase 4t.

### M0 evaluation for the single-position cross-sectional lane

| #  | Clause                                             | Evaluation                                                                                             |
| -- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| 1  | Mechanism source (non-price-only or cross-sectional) | PASS — the lane is cross-sectional by construction.                                                    |
| 2  | Baseline-superiority theory                        | CONDITIONAL — must be predeclared in any future Phase 4ai memo before data is touched.                 |
| 3  | Cost realism under §11.6 = 8 bps HIGH per side      | CONDITIONAL — depends on rebalance frequency; must be predeclared.                                     |
| 4  | Opportunity-rate plausibility                       | PASS — ranking always produces an output (top symbol or "none"), avoiding G1-style sparsity.           |
| 5  | Design-family distance                             | PASS — distinct from R2 / F1 / D1-A / V2 / G1 / C1 if §8 anti-rescue rules are honored.                |
| 6  | Data feasibility                                   | PASS — Phase 4ac PASS klines + Phase 4ad Rule B1 scope cover the universe.                             |
| 7  | Governance compatibility                           | PASS — §1.7.3 one-position-max preserved by single-position framing; Phase 3v / 3w label schemes hold. |
| 8  | Forbidden-rescue check                             | CONDITIONAL — §8 rules above must be predeclared and enforced.                                         |
| 9  | Falsification criterion                            | CONDITIONAL — must be predeclared in any future Phase 4ai memo.                                        |
| 10 | Non-authorization                                  | PASS — Phase 4ah does not authorize a strategy spec, backtest plan, backtest, or successor phase.      |

Aggregate Phase 4ah M0 reading:

- Five clear PASS outcomes (1, 4, 5, 6, 7, 10).
- Four CONDITIONAL outcomes that are bindable in a future
  Phase 4ai memo (2, 3, 8, 9).
- Zero structural FAILs.

The lane therefore *appears* admissible under a non-binding M0
reading. Phase 4ah does not extend this reading into a governance
adoption.

---

## 10. Future Feasibility Metrics — Not Computed in Phase 4ah

A future analysis-and-docs phase, if separately authorized, could
compute the following descriptive metrics on the predeclared
universe under Phase 4ad Rule B1 scope. **Phase 4ah does not
compute any of them.**

- Top-ranked-versus-bottom-ranked fixed-horizon forward returns
  (descriptive only; no PnL).
- Top-ranked-versus-median fixed-horizon forward returns
  (descriptive only; no PnL).
- Rank persistence (probability that the top-ranked symbol at
  rebalance `t` is still top-ranked at rebalance `t+k`).
- Top-rank turnover (frequency at which the top-ranked symbol
  changes).
- Hit rate of top-ranked symbol *outperforming* the median
  symbol across each forward horizon.
- Cost-adjusted forward-move frequency by rank bucket
  (analogous to the Phase 4af cost-adjusted-move metric, but
  conditioned on rank rather than on trend state).
- Rank concentration by symbol (e.g. fraction of rebalances
  where SOL or BTC is top-ranked).
- Drawdown / crash exposure by rank bucket.
- Turnover-implied cost burden under §11.6 = 8 bps HIGH per
  side (round-trip 16 bps), with a predeclared per-rebalance
  switch cost assumption.
- "No-trade" frequency if no symbol passes predeclared
  rank-quality filters.
- Stability of the above metrics across 15m / 30m / 1h / 4h
  rebalance periods.

Explicit non-claims:

- Phase 4ah does not compute these metrics.
- A future Phase 4ai-equivalent memo would have to predeclare
  the metric set before any data is touched.
- All future metrics would be **descriptive only**, not
  strategy PnL, not strategy backtest, not backtest plan
  evidence.
- No future metric output may be used to retroactively rescue
  R3 / R2 / F1 / D1-A / V2 / G1 / C1.

---

## 11. Feasibility Risks

### 11.A Portfolio-literature mismatch

Most cross-sectional crypto-momentum literature assumes
multi-position long-short or risk-parity-weighted top-N
portfolios. Prometheus has `one position max` per `§1.7.3`. Any
future feasibility study must therefore not inherit a
portfolio-style framing without explicit reframing to single-
position symbol selection.

### 11.B Turnover and cost burden

A short rebalance period with frequent top-rank changes can
recreate R2's cost fragility through turnover alone. Any future
feasibility memo must predeclare rebalance frequency, expected
turnover, and per-rebalance cost assumption *before* computing
descriptive metrics.

### 11.C Symbol-mining risk

Expanding the universe beyond the five-symbol core set without
explicit Phase 4aa-style governance creates a multiple-testing
trap. Phase 4ah recommends keeping the universe fixed at five
symbols.

### 11.D Ranking-wrapper rescue risk

The most dangerous failure mode of this lane is a silent
reduction to "rank on something, then trade V2 / G1 / C1 on the
top symbol." This must be explicitly forbidden in any future
phase brief and verified at each phase boundary.

### 11.E Crash / regime risk

The 2025 literature describes partly-forecastable crypto-momentum
crashes. Volatility-managed weighting is the standard mitigation
in portfolio settings, but it is multi-position by construction.
Single-position selection cannot use vol-targeting in the same
way. Any future feasibility memo must report drawdown / crash
exposure by rank bucket and must not deflect crash exposure into
a vol-target wrapper that secretly assumes multi-position
weighting.

### 11.F Liquidity / notional constraints

Kline notional is a *proxy* for liquidity, not a measure of
order-book depth. The Phase 4ae notional ranking shows BTC
dominates by 1–2 orders of magnitude over the alts; thin-symbol
top-ranking under high turnover could imply implementation cost
beyond §11.6's 8 bps assumption. Any future feasibility memo
must report this risk explicitly.

### 11.G Data scope risk

Five symbols is a small N for cross-sectional inference. The
literature's strongest cross-sectional momentum results use
universes of dozens to hundreds of coins. A five-symbol
single-position study is inherently underpowered for replicating
literature-style cross-sectional spreads. Phase 4ah's response
to this is *not* "expand the universe" (that would re-open
Phase 4aa governance) but "frame the study as feasibility for
single-position TSMOM-style selection within a fixed small
universe, not as cross-sectional factor replication."

---

## 12. Candidate Future Phase Design

The following sketch of a possible future phase is recorded as a
**recommendation only**, not authorization.

```text
Potential future Phase 4ai — Single-Position Cross-Sectional Trend
                              Feasibility Analysis
```

Type:

- analysis-and-docs only.

Required boundaries (drawn from the Phase 4ag / Phase 4ae /
Phase 4af pattern):

- Use existing local normalized data only.
- No data acquisition.
- No data download.
- No API / endpoint calls.
- No manifest changes.
- No backtests.
- No strategy PnL.
- No entry / exit returns.
- No strategy specs.
- No old-strategy reruns.
- No live path.
- No exchange-write.

Required inputs:

- Fixed five-symbol core universe (`BTCUSDT`, `ETHUSDT`,
  `SOLUSDT`, `XRPUSDT`, `ADAUSDT`).
- Phase 4ad Rule B1 common-post-gap scope
  (`2022-04-03 00:00 UTC` through latest available month).
- Predeclared ranking descriptors drawn primarily from
  families 7.A and 7.C with optional liquidity screen from
  7.D.
- Predeclared rebalance frequency.
- Predeclared rank-quality filter for "no-symbol" output.
- Predeclared cost assumption: §11.6 = 8 bps HIGH per side.

Required outputs:

- Descriptive top-versus-rest / top-versus-median comparisons.
- Rank persistence and turnover statistics.
- Cost-adjusted forward-move frequency by rank bucket.
- Drawdown / crash exposure by rank bucket.
- Turnover-implied cost-burden estimate.
- "No-trade" frequency under predeclared rank-quality filter.
- Falsification verdict against predeclared criteria.

State explicitly:

- **Phase 4ai is NOT authorized by Phase 4ah.**
- The operator may equally choose Option A — remain paused.
- A Phase 4ai-equivalent phase does not name a strategy
  candidate, does not write a strategy spec, does not draft a
  backtest plan, and does not authorize successor phases.

---

## 13. Decision Menu

### Option A — Remain paused

Always procedurally valid. Still primary if the operator does not
want to commit to a Phase 4ai feasibility analysis after reading
Phase 4ah.

### Option B — Merge Phase 4ah to main, then stop

Recommended if Phase 4ah is complete and docs-only.

### Option C — Future Phase 4ai single-position cross-sectional trend feasibility analysis

Conditional next research step if the operator wants progress.
This is the cleanest option among non-paused alternatives because
it tests the only Phase 4ag mechanism family rated
`ADMISSIBLE_FOR_FUTURE_DOCS_ONLY_STUDY`.

### Option D — Future docs-only M0 governance reconciliation phase

Possible if the operator wants to formalize admissibility gates
(reconciling the Phase 4ag M0 proposal with Phase 4z, Phase 4m,
Phase 4t) before any analysis. Acceptable; not recommended over
Option C unless governance reconciliation is an operator priority.

### Option E — Future docs-only derivatives-context feasibility memo

Conditional. Higher D1-A rescue risk than Option C; not
recommended at this boundary.

### Option F — Future docs-only microstructure data-admissibility memo

Not recommended now. Heavy data burden; low expected information
gain at this boundary.

### Option G — Fresh-hypothesis discovery memo

Not recommended yet. Both Phase 4ag and Phase 4ah preserve the
position that fresh-hypothesis discovery is premature relative to
the Phase 4m 18-requirement validity gate and Phase 4t 10-
dimension scoring matrix.

### Option H — Strategy spec / backtest / old-strategy alt rerun

Forbidden / not authorized. Old-strategy alt-symbol rescue is
explicitly forbidden by Phase 4aa, Phase 4ab, Phase 4ag, and
reaffirmed by Phase 4ah.

### Option I — Paper / shadow / live / exchange-write

Forbidden / not authorized. No validated strategy exists.
Phase-gate requirements per `docs/12-roadmap/phase-gates.md` are
not met.

---

## 14. Recommendation

```text
Primary recommendation:
Merge Phase 4ah into main, then remain paused unless the operator
separately authorizes a future Phase 4ai single-position cross-
sectional trend feasibility analysis.

Conditional research recommendation:
If the operator wants to continue, Phase 4ai is the cleanest next
research step, because it tests the only Phase 4ag mechanism family
rated ADMISSIBLE_FOR_FUTURE_DOCS_ONLY_STUDY. Phase 4ai must remain
analysis-and-docs only, must use existing local normalized data
only, must predeclare its descriptor set / rebalance frequency /
rank-quality filter / falsification criteria before any descriptor
is computed, and must explicitly forbid silent reduction to
single-symbol breakout under a ranking wrapper.

Do NOT authorize strategy discovery yet.
Do NOT authorize a strategy spec.
Do NOT authorize backtests.
Do NOT authorize old-strategy alt-symbol reruns.
Do NOT authorize data acquisition yet.
```

Rationale:

- The literature is **mixed**: time-series momentum is the
  better-documented crypto family; cross-sectional long-short
  spreads are weak. Single-position selection is a *reframe* of
  cross-sectional ranking under `one position max` — closer to
  per-symbol TSMOM with a best-of-N selection wrapper than to
  long-short factor capture.
- The Phase 4ae / Phase 4af substrate evidence is silent on
  cross-symbol comparisons; Phase 4af's null is per-symbol bar-
  level only.
- Single-position cross-sectional symbol selection is the only
  Phase 4ag mechanism family that combines (a) structural
  distinctness from all six rejections, (b) preservation of
  `§1.7.3` `one position max`, and (c) usability of already-
  acquired Phase 4ac data.
- It is, however, **not strongly endorsed by literature** at
  the single-position-selection reframe; its main attraction
  for Prometheus is *structural distinctness*, which justifies
  a docs-only feasibility study but does **not** justify a
  strategy candidate, a strategy spec, a backtest plan, or any
  successor authorization at this boundary.

---

## 15. Preserved Locks and Boundaries

Phase 4ah preserves every retained verdict and project lock
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
- Phase 3r §8 preserved.
- Phase 3v §8 preserved.
- Phase 3w §6 / §7 / §8 preserved.
- Phase 4j §11 preserved.
- Phase 4k preserved.
- Phase 4p preserved.
- Phase 4q preserved.
- Phase 4v preserved.
- Phase 4w preserved.
- Phase 4z recommendations remain recommendations only.
- Phase 4aa admissibility framework remains recommendation only.
- Phase 4ab recommendations remain recommendations only.
- Phase 4ac results remain data / integrity evidence only.
- Phase 4ad future-use rules remain prospective analysis-time
  scope only.
- Phase 4ae findings remain descriptive substrate-feasibility
  evidence only.
- Phase 4af findings remain descriptive regime-continuity /
  directional-persistence evidence only.
- Phase 4ag recommendations remain recommendations only.
- Phase 4ah recommendations remain recommendations only unless
  separately adopted later.

---

## 16. Explicit Non-Authorization Statement

Phase 4ah does **NOT** authorize:

- Phase 4ai,
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
- strategy candidate naming,
- fresh-hypothesis discovery memo,
- hypothesis-spec memo,
- strategy-spec memo,
- backtest-plan memo,
- implementation,
- runtime code modification,
- test modification,
- script modification,
- old-strategy rescue (R3 / R2 / F1 / D1-A / V2 / G1 / C1 in any
  form, including alt-symbol reruns and any -prime / -narrow /
  -relaxed / hybrid variant),
- multi-position portfolio trading,
- silent reduction of cross-sectional ranking into a V2 / G1 /
  C1-style single-symbol breakout continuation,
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

Phase 4ah is docs-only.

Phase 4ah's primary recommendation is to merge into main and then
**remain paused** unless the operator separately authorizes a
future Phase 4ai single-position cross-sectional trend feasibility
analysis.

Phase 4ah's recommendations are **recommendations only** unless
separately adopted in a future operator-authorized phase.
