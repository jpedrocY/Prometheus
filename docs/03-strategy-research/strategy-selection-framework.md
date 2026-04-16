# Strategy Selection Framework

## Purpose
Define how the first implemented strategy family should be chosen.

## Scope
This framework applies to the first serious strategy decision. It can be reused later for additional strategies.

## Background
The project should not choose its first strategy based on familiarity or aesthetic preference alone. The first strategy must be selected based on fit with the project’s current maturity and constraints.

## Definitions
- **Testability**: how cleanly a concept can be defined, coded, and validated.
- **Execution burden**: how demanding the strategy is on the exchange and order model.
- **Operational burden**: how difficult it is to supervise, debug, and recover.

## Main Framework / Design / Rules

### Evaluation Criteria
Score each candidate strategy family on:
1. clarity of formalization
2. backtest honesty
3. execution simplicity
4. fit for 10m–15m horizon
5. cost sensitivity
6. risk clarity
7. regime dependence
8. failure-mode visibility
9. expandability later
10. alignment with user domain knowledge

### Initial Candidate Set
1. Breakout + trend filter
2. Pullback continuation into objective structural zone
3. Mean reversion at range extremes

### Early Selection Bias
The first strategy should favor:
- simple state,
- obvious invalidation,
- manageable order flow,
- clear stop placement,
- clear failure analysis.

## Assumptions
- The best first strategy may not be the most profitable on paper; it may be the most trustworthy to implement.

## Risks and Failure Modes
- choosing a strategy family with hidden discretion
- overvaluing visual appeal
- underestimating operational complexity

## Open Questions
- Should the first selection be driven more by execution simplicity or by market familiarity?
- Which family produces the cleanest objective rule set?

## Decisions
- Final selection is not yet made.
- The shortlist is fixed for now to three core candidate families.

## Next Steps
- perform a full three-way comparison
- derive an initial formalization sheet for each family

## References
- `strategy-taxonomy.md`
- `price-action-concepts-formalization.md`
- `../00-meta/decision-framework.md`
