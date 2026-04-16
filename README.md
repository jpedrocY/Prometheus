# AI-Assisted Trading Bot Project

## Mission
Design, validate, and eventually deploy a production-oriented AI-assisted crypto trading bot with a strong emphasis on robustness, realistic execution, risk control, and operational safety.

## Current Status
This repository is in the research and systems-design phase. The immediate focus is on:
- documentation-first project structure,
- rules-based strategy design,
- Binance USDⓈ-M futures as the primary candidate venue,
- validation standards,
- architecture boundaries,
- risk policy foundations.

## Working Principles
- Markdown is the canonical living memory of the project.
- The first live-capable version should be rules-based, not self-learning.
- The trading engine must be separate from any future UI/dashboard.
- Production safety is more important than novelty.
- Futures are the primary target, but spot remains a useful baseline and control path.

## Documentation
See `docs/README.md` for the documentation map and review order.

## Current Initial Decisions
- Primary venue candidate: Binance USDⓈ-M futures
- V1 style: rules-based
- V1 position mode: one-way
- V1 margin mode: isolated
- Likely initial timeframe: 10m–15m
- Future UI: separate layer/service from the trading engine
