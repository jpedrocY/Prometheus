# Bot Types and AI Levels

## Purpose
Provide a clear taxonomy of trading bot types and the level of AI involvement they imply.

## Scope
This document is a framing reference, not a final implementation choice.

## Background
The phrase “AI trading bot” is too vague to guide architecture. The project needs a more precise vocabulary.

## Definitions
- **Rule-based bot**: deterministic logic with explicit conditions.
- **Quant/statistical bot**: model-driven or statistically structured logic without necessarily using ML.
- **ML-driven bot**: uses trained models as part of signal generation or risk estimation.
- **LLM-assisted system**: uses an LLM for research, coding, monitoring, summarization, or text workflows.
- **RL trading system**: learns action policies through reward-driven interaction.

## Main Framework / Design / Rules

### Bot Types
1. Rule-based systematic bot
2. Quant/statistical bot
3. ML-assisted signal bot
4. RL-based trading bot
5. Hybrid bot
6. LLM-assisted operations/research system

### AI Involvement Ladder
- Level 0: no AI, only deterministic logic
- Level 1: AI used for research and coding assistance
- Level 2: AI used for offline analysis, labeling, or enrichment
- Level 3: AI/ML used for offline signals that require promotion
- Level 4: AI/ML influences live decisions under strict guardrails
- Level 5: tightly governed automation with extensive controls
- Level 6: self-learning live adaptation

### Current Project Position
The current intended starting point is:
- rule-based trading logic,
- AI for documentation/research/coding support,
- possible later ML additions in constrained roles.

## Assumptions
- The first production-worthy version should stay low on the AI involvement ladder.

## Risks and Failure Modes
- treating all bot categories as equally feasible
- jumping levels before lower levels are stable
- assuming AI sophistication implies trading edge

## Open Questions
- What is the earliest justified live role for ML in this project?

## Decisions
- The first implementation target is rule-based.
- LLMs are support tools first, not live trade authorities.

## Next Steps
- Map candidate strategy families to this framework
- Identify future ML insertion points that do not distort the initial architecture

## References
- `trading-paradigm-shift-human-vs-bot.md`
- `system-maturity-model.md`
