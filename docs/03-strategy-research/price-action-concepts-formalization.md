# Price-Action Concepts Formalization

## Purpose
Create a bridge from discretionary trading concepts to machine-testable strategy components.

## Scope
This document catalogs candidate concepts and frames the formalization work required. It does not yet finalize rule definitions.

## Background
Concepts such as fair value gaps, trendlines, reversals, and patterns are common in discretionary trading. For a bot, each must be translated into explicit definitions and constraints.

## Definitions
- **Formalization**: expressing a human trading concept as measurable, rule-based logic.
- **Machine-testable**: definable in data and executable without hidden discretion.

## Main Framework / Design / Rules

### Formalization Ladder
Every concept should be translated through:
1. informal concept statement
2. structural definition
3. regime context
4. trigger definition
5. risk definition
6. exit definition
7. invalidation logic
8. testability review

### Candidate Concepts

#### Fair Value Gaps (FVG)
Current status:
- promising candidate
- requires precise structural definition
Questions:
- wick-based or body-based?
- minimum imbalance size?
- partial fill vs full fill treatment?
- continuation-only or reversal-capable?

#### Trendlines
Current status:
- familiar but likely difficult to define honestly
Questions:
- how are anchor points chosen?
- how many touches qualify?
- what invalidates a line?
- how much discretion is hidden in line placement?

#### Reversals
Current status:
- broad concept, needs narrowing
Questions:
- reversal after what preceding move?
- what qualifies as exhaustion or structural change?
- what trigger confirms reversal rather than temporary pullback?

#### Patterns
Current status:
- high discretion risk
Questions:
- which specific patterns are worth formalizing?
- can they be represented without subjective interpretation?

#### Breakout Structures
Current status:
- strong early candidate
Questions:
- breakout of what level?
- close-based or intra-bar?
- confirmation required?
- false-break filters?

#### Pullback Continuation
Current status:
- strong early candidate
Questions:
- how is trend defined?
- what qualifies as a pullback zone?
- what confirms resumption?

#### Mean Reversion
Current status:
- strong candidate if bounded clearly
Questions:
- what defines the range or stretch?
- how is overextension measured?
- when is reversion invalid because regime has changed?

## Assumptions
- Not all discretionary concepts will survive formalization with acceptable quality.

## Risks and Failure Modes
- preserving vague concepts for sentimental reasons
- forcing objective labels onto fundamentally subjective setups
- mixing too many concepts into one strategy

## Open Questions
- Which concept family can be formalized first with the highest integrity?

## Decisions
- Breakout, pullback continuation, and mean reversion are current top candidates.
- Trendlines and broad pattern logic are lower-priority until objectivity can be demonstrated.

## Next Steps
- build one formalization sheet per shortlisted strategy family
- identify required data features for each candidate

## References
- `strategy-selection-framework.md`
- `../01-foundations/trading-paradigm-shift-human-vs-bot.md`
