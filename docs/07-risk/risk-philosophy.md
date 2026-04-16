# Risk Philosophy

## Purpose
Define the core risk worldview that should govern the system.

## Scope
This is the top-level risk policy document. Specific sizing, stops, and daily limits belong in related subordinate documents.

## Background
A bot does not become safe because its strategy is good. It becomes safer because risk is treated as an external, explicit control system with veto power over strategy behavior.

## Definitions
- **Risk engine**: component or policy layer that can constrain or reject trade intents.
- **Capital preservation**: priority on survival and controlled drawdowns over aggressive opportunity capture.
- **Kill switch**: mechanism that halts or sharply restricts activity under defined failure conditions.

## Main Framework / Design / Rules

### Core Principles
1. Risk control is mandatory and external to signal enthusiasm.
2. Position size is driven by defined risk, not by desired notional.
3. Leverage is a constraint, not an objective.
4. The system should prefer missing a trade over taking uncontrolled risk.
5. Every live trade should be explainable in terms of pre-approved risk policy.
6. Risk policy must remain valid even if the strategy is temporarily wrong.
7. Exchange or data uncertainty should reduce risk, not increase guesswork.

### Policy Implications
- the risk layer can veto any trade intent
- daily loss and drawdown limits are first-class controls
- liquidation distance must matter even when stops exist
- isolated margin and one-way mode simplify early containment
- size increases should be gradual and evidence-based

## Assumptions
- The system should begin under conservative leverage and notional conditions.
- V1 should prioritize containment over capital efficiency.

## Risks and Failure Modes
- stop placement treated as a complete substitute for risk policy
- leverage normalized because the market “usually” behaves
- sizing based on confidence rather than predefined limits
- creeping loosening of limits after wins

## Open Questions
- What exact daily loss threshold should trigger pause mode?
- What liquidation buffer should be required by policy?
- Should there be a volatility-adaptive risk throttle in v1 or later?

## Decisions
- risk policy has veto power over strategy logic
- conservative futures deployment is the intended starting mode
- hard brakes are mandatory before live deployment

## Next Steps
- define sizing framework
- define kill-switch triggers
- define drawdown and exposure constraints

## References
- `position-sizing-framework.md`
- `kill-switches.md`
- `daily-loss-rules.md`
- `../02-market-structure/leverage-liquidation-margin-modes.md`
