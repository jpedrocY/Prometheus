# Strategy Taxonomy

## Purpose
Provide a structured map of candidate strategy families relevant to the project.

## Scope
This document defines strategy categories, not final implementations.

## Background
A strategy family is a class of market behavior and trade logic, not a single parameter set.

## Definitions
- **Strategy family**: a broad class of setups with shared structural logic.
- **Regime fit**: the market conditions in which a strategy family is expected to perform better.

## Main Framework / Design / Rules

### Primary Candidate Families
1. Breakout / continuation
2. Pullback continuation
3. Mean reversion
4. Trend following
5. Range-based fade logic
6. Event-driven setups
7. Statistical spread or relative-value logic
8. Market-making or inventory-based logic

### Current Best-Fit Early Candidates
Given current project goals and user background, the most promising early candidates are:
- breakout with trend filter,
- pullback continuation into objective structural zones,
- mean reversion at well-defined range extremes.

### Lower Priority for Early Phases
- market making
- stat-arb
- event/news-driven systems
- complex multi-signal hybrids

## Assumptions
- Early strategy selection should favor objective definitions and modest execution complexity.

## Risks and Failure Modes
- choosing a strategy family because it sounds advanced
- mixing several families before any one is validated
- allowing discretionary narrative logic to hide inside strategy descriptions

## Open Questions
- Which family best balances testability, implementation simplicity, and live robustness?

## Decisions
- Three families will likely form the first comparison set:
  1. breakout + trend filter
  2. pullback continuation
  3. mean reversion

## Next Steps
- build the strategy selection framework
- formalize discretionary concepts into machine-testable candidates

## References
- `strategy-selection-framework.md`
- `price-action-concepts-formalization.md`
