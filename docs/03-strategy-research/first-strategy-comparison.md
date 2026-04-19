# First Strategy Comparison

## Purpose

This document compares the leading candidate strategy families for the first implemented trading strategy of the project and records the current decision for version 1.

The goal is not to choose the most intellectually interesting or discretionary-familiar setup. The goal is to choose the strategy family with the best combination of:

- edge plausibility,
- rule clarity,
- execution realism,
- risk containment,
- validation robustness,
- and expandability into later versions.

## Scope

This document covers the selection of the **first primary strategy family** for the initial production-oriented system.

It does **not** yet define the full final strategy rules, parameter values, or symbol selection.

## Background

The project is currently targeting a **rules-based first system** on **Binance USDⓈ-M futures**, with the following provisional architectural choices:

- one-way mode for v1,
- isolated margin for v1,
- one symbol first,
- 15-minute timeframe currently preferred over 10-minute,
- operator-supervised deployment,
- strong risk controls,
- strategy logic separate from execution, risk, and UI layers.

This selection is being made under a production-oriented design philosophy: robustness and controllability are prioritized over novelty.

Research on cryptocurrency markets suggests that both **momentum** and **reversal** can exist at intraday horizons, and that the strength of these effects changes with jumps, liquidity, and regime conditions. This implies that a good first system should avoid assuming one universal market behavior and should instead be designed with explicit market-state awareness.

Recent literature also suggests that trend-related technical information remains meaningful in cryptocurrency markets. A 2025 *Journal of Financial and Quantitative Analysis* paper finds that a cryptocurrency trend factor built from multiple technical signals is a reliable predictor in the cross section of crypto returns, is present even in liquid coins, and remains resilient under many research-design changes and transaction-cost assumptions.

## Candidate Strategy Families

### 1. Breakout + trend filter

This family enters in the direction of an established trend when price breaks out of a defined consolidation, range, or structural boundary.

Typical components:

- higher-timeframe directional filter,
- local compression / range identification,
- breakout trigger,
- confirmation filter,
- structural stop,
- fixed or trailing exit logic.

### 2. Pullback continuation

This family waits for an existing trend to retrace into a defined area before entering in the direction of continuation.

Typical components:

- higher-timeframe directional filter,
- pullback zone definition,
- confirmation on rejection or continuation,
- stop below invalidation area,
- target at prior expansion continuation or fixed multiple.

This family may later include carefully formalized ideas such as imbalance zones or FVG-based continuation entries.

### 3. Mean reversion

This family fades stretched moves back toward local equilibrium, range midpoint, or a statistically normalized anchor.

Typical components:

- overextension measure,
- range or equilibrium anchor,
- reversal trigger,
- tighter profit target,
- strict regime filter to avoid fading true expansion.

### 4. FVG-first continuation

This family uses fair value gap logic as the primary entry framework rather than as a secondary contextual tool.

Typical components:

- imbalance detection,
- fill / partial fill logic,
- trend filter,
- trigger confirmation,
- structural invalidation.

### 5. Trendline / pattern-driven systems

This family uses line geometry, chart formations, and visual pattern logic as the primary strategy framework.

Typical components:

- line or pattern construction,
- validity checks,
- breakout / rejection logic,
- stop placement rules,
- target projection.

## Evaluation Criteria

The strategy families are evaluated against the following criteria.

### Edge plausibility

There should be a credible empirical or structural reason to believe the family can work in crypto futures.

### Rule clarity

The setup must be definable as explicit, machine-testable logic without hidden discretionary interpretation.

### Validation robustness

The strategy should be suitable for walk-forward testing, perturbation analysis, and realistic cost modeling without needing subjective labeling.

### Execution simplicity

The strategy should map cleanly into Binance USDⓈ-M futures order and position mechanics.

This matters because Binance’s current futures API distinguishes one-way and hedge modes, changes required `positionSide` behavior across modes, and does not allow `reduceOnly` in hedge mode. Those constraints make simpler position logic more attractive for v1.

### Risk containment

Failure modes should be understandable and containable with hard sizing, invalidation, and kill-switch rules.

### Expandability

The family should serve as a useful foundation for future refinements, including pullback variants, regime filters, and later ML-assisted research.

## Comparative Assessment

### Breakout + trend filter

**Strengths**
- High rule clarity.
- Clean mapping to long/short futures execution.
- Strong compatibility with one-way mode.
- Easier alerting, monitoring, and post-trade review.
- Natural fit for higher-timeframe bias plus intraday trigger structure.
- Supported by evidence that crypto markets exhibit momentum / trend-related structure and technically informative trend behavior.

**Weaknesses**
- Vulnerable to false breakouts and chop.
- Can underperform in sideways regimes.
- Needs explicit volatility or regime filters to avoid repeated whipsaws.

**Assessment**
Best overall candidate for v1.

### Pullback continuation

**Strengths**
- Often offers better entry price than pure breakout.
- Potentially better R:R profile.
- Closer to how many discretionary traders naturally think about trend participation.
- Strong candidate for phase-2 refinement once a baseline system exists.

**Weaknesses**
- More ambiguous zone definition.
- Easier to smuggle in discretion through “quality” filters.
- Higher risk of overfitting via layered contextual rules.

**Assessment**
Very strong candidate for v2 research, but not the cleanest first production family.

### Mean reversion

**Strengths**
- Can perform well in ranges and oscillatory conditions.
- Often easier to define mathematically than discretionary pullback logic.
- Potentially complementary to trend systems later.

**Weaknesses**
- Tail risk is more dangerous in leveraged futures.
- Bad entries can be punished quickly during expansions.
- Usually requires stronger regime classification to avoid fading genuine directional moves.

**Assessment**
Valuable later for diversification, but not the safest primary v1 strategy.

### FVG-first continuation

**Strengths**
- Can be expressive of real continuation logic if formalized well.
- May offer attractive pullback entries.
- Potentially a useful sub-variant of pullback continuation.

**Weaknesses**
- Definitions are often inconsistent across discretionary traders.
- Body-vs-wick, gap size thresholds, fill percentages, invalidation logic, and context dependency are often ambiguous.
- High risk of pseudo-objectivity if formalized poorly.

**Assessment**
Should be treated as a later refinement concept, not the first primary family.

### Trendline / pattern-driven systems

**Strengths**
- Intuitive to human traders.
- Easy to understand visually.

**Weaknesses**
- High hidden discretion.
- Ambiguous anchoring and validity rules.
- Difficult to formalize honestly without either oversimplifying or overcomplicating.

**Assessment**
Not suitable as the first primary system.

## Summary Scorecard

| Strategy Family | Edge Plausibility | Rule Clarity | Execution Simplicity | Risk Containment | Expandability | Overall |
|---|---:|---:|---:|---:|---:|---:|
| Breakout + trend filter | 8 | 9 | 9 | 7 | 9 | **8.4** |
| Pullback continuation | 8 | 6 | 8 | 8 | 8 | **7.6** |
| Mean reversion | 7 | 8 | 7 | 5 | 8 | **7.0** |
| FVG-first continuation | 6 | 5 | 7 | 7 | 7 | **6.4** |
| Trendline / pattern-driven | 5 | 4 | 6 | 6 | 6 | **5.4** |

These scores are project judgments, not empirical backtest outputs. They reflect current evidence and implementation priorities.

## Decision

### Selected Family for v1

**Breakout + trend filter** is selected as the first primary strategy family for version 1.

### Why this family was selected

It offers the best balance of:

- evidence-consistent market logic,
- clean rule formalization,
- strong compatibility with Binance futures execution,
- manageable operational complexity,
- and future extensibility.

This choice is also consistent with the broader research picture:

- cryptocurrency markets show intraday predictability with both momentum and reversal behavior, implying that a trend strategy should include explicit filtering rather than assume trend is always dominant,
- technical and trend-related information appears to be meaningfully predictive in crypto markets, including in liquid coins,
- the crypto-trading research landscape is broad and increasingly practical, but this project prioritizes simple, testable structure before later ML or hybrid enhancements.

## Rejected as Primary v1 Choices

### Pullback continuation
Deferred to v2 candidate status because it is highly promising but less objective than breakout-first logic.

### Mean reversion
Deferred because its live failure modes under leverage are harsher and more regime-sensitive.

### FVG-first
Deferred because it is better used as a contextual refinement than a primary initial framework.

### Trendlines / patterns
Deferred because they are too discretion-heavy for the first production strategy.

## Provisional v1 Strategy Shape

The selected family should likely follow this structure:

1. determine higher-timeframe directional bias,
2. identify compression / base / range,
3. require breakout beyond a defined structural boundary,
4. require confirmation by expansion / strength filter,
5. enter in the breakout direction,
6. place stop at structural invalidation,
7. manage exits with fixed-R, structural trailing, or hybrid logic,
8. disable or reduce trading in poor regimes.

This is still a family definition, not the final rule set.

## Execution Notes Relevant to Strategy Design

The strategy should be designed with current Binance USDⓈ-M mechanics in mind:

- one-way mode keeps `positionSide` simpler and uses default `BOTH`, while hedge mode requires explicit `LONG` or `SHORT`,
- `reduceOnly` cannot be sent in hedge mode, which is another reason to keep v1 in one-way mode,
- Binance migrated USDⓈ-M conditional orders such as `STOP_MARKET`, `TAKE_PROFIT_MARKET`, `STOP`, `TAKE_PROFIT`, and `TRAILING_STOP_MARKET` to the Algo Service in December 2025, so stop-loss and take-profit implementation must follow the current algo-order model, not older assumptions,
- test-order endpoints remain useful for shadow-trading and request validation, but they do not replace live reconciliation design,
- user data streams require active keepalive and reconnect discipline: `listenKey`s expire after 60 minutes unless extended, and connections are valid for 24 hours.

## Open Questions

The following questions must be answered before the final strategy specification is written:

1. Which symbol should be used for v1?
2. Should the base timeframe be 15m or 10m?
3. How should higher-timeframe trend bias be defined?
4. How should compression / consolidation be defined?
5. What exact breakout condition is required?
6. What confirmation filter should be used?
7. What stop-placement model should be used?
8. What exit model should be used?
9. What no-trade regime filters should be included?
10. Should re-entry after failed breakout be allowed?

## Decisions

Accepted / provisional decisions at this stage:

- v1 primary strategy family: **breakout + trend filter**
- venue focus: **Binance USDⓈ-M futures**
- margin mode for v1: **isolated**
- position mode for v1: **one-way**
- initial deployment model: **single-symbol, supervised, staged rollout**
- rules-based approach remains mandatory for v1

## Next Steps

The next document should define the strategy family in much greater detail.

Recommended next file:

`docs/03-strategy-research/v1-breakout-strategy-spec.md`

That file should decide:

- symbol,
- timeframe,
- trend filter,
- setup structure,
- trigger logic,
- stop logic,
- exit logic,
- regime filters,
- and validation requirements.

## References

Key sources used in this decision:

- Nguyen & Chan (2024), *Cryptocurrency trading: A systematic mapping study*.
- Wen et al. (2022), *Intraday return predictability in the cryptocurrency markets: Momentum, reversal, or both*.
- Fieberg et al. (2025), *A Trend Factor for the Cross Section of Cryptocurrency Returns*.
- Rohrbach et al. (2017), *Momentum and trend following trading strategies for currencies and bitcoin*.
- Binance USDⓈ-M Futures trade and user-stream documentation.