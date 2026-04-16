# V1 Breakout Strategy Specification

## Purpose

This document defines the first concrete strategy specification for version 1 of the trading system.

The purpose of this strategy is not to reproduce discretionary chart reading or to maximize complexity. The purpose is to define a rules-based, production-friendly, objectively testable strategy that is compatible with Binance USDⓈ-M futures execution, strong risk control, and staged live deployment.

## Scope

This document defines:

- the selected market and contract,
- the selected base and higher timeframes,
- the selected trend-bias logic,
- the breakout setup structure,
- the trigger conditions,
- the initial stop logic,
- the position sizing philosophy,
- the exit-management logic,
- the no-trade filters,
- the live execution assumptions,
- and the validation requirements.

This document does **not** define all numeric thresholds as immutable final production parameters. Several values below are **research defaults** that must be tested and may be revised after validation.

## Background

The project has already selected **breakout + trend filter** as the first primary strategy family for v1.

That decision was made because this family offers the strongest balance of:

- edge plausibility in crypto,
- rule clarity,
- execution simplicity,
- risk containment,
- and future extensibility.

The current engine target remains:

- Binance USDⓈ-M futures,
- one-way mode,
- isolated margin,
- one symbol first,
- supervised rollout,
- rules-based logic only.

## Strategy Summary

### Selected v1 market

- **Venue:** Binance USDⓈ-M futures
- **Contract type:** perpetual
- **Initial symbol:** **BTCUSDT**
- **First secondary comparison symbol:** **ETHUSDT**

### Why BTCUSDT is selected first

BTCUSDT is the cleanest first symbol for v1 because it combines:

- very high liquidity,
- deep order-book depth,
- comparatively tighter spreads,
- lower idiosyncratic behavior than many altcoin perpetuals,
- and easier live execution under a production-first design.

ETHUSDT remains the first secondary comparison symbol so the project does not accidentally optimize around Bitcoin-specific behavior alone.

### Selected timeframes

- **Signal timeframe:** 15m
- **Higher-timeframe bias:** 1h

### Why 15m is selected first

15m is preferred because it reduces noise, lowers operational churn, and still remains active enough for a crypto futures breakout system.

15m is also a better first anchor for validating a bar-close execution model than a more reactive lower timeframe.

## Market Hypothesis

The v1 strategy is based on the following hypothesis:

> In BTCUSDT perpetual futures, directional moves are more likely to continue when a higher-timeframe trend is already established, short-term price compresses into a relatively tight range, and price then breaks out of that range with clear expansion and a strong close.

This is a continuation hypothesis, not a universal prediction hypothesis.

The system does not attempt to forecast every move. It attempts to participate only in a subset of moves where:

1. directional bias already exists,
2. local compression reduces immediate randomness,
3. breakout confirms re-expansion,
4. and invalidation can be defined clearly.

## Required Data

### Mandatory market data

- 15m OHLCV for the trading symbol
- 1h OHLCV for the trading symbol
- mark price stream for the trading symbol
- exchange symbol metadata from exchange info
- user commission rate
- leverage bracket information
- funding rate history for research and backtesting

### Mandatory live execution data

- user data stream
- open orders state
- position state
- fills / trade confirmations
- mark price updates

## Core Definitions

### ATR

Unless otherwise specified, ATR means **ATR(20)** on the relevant timeframe.

### Setup window

The setup window is the **previous 8 completed 15m candles**.

### Setup high

The highest high of the previous 8 completed 15m candles.

### Setup low

The lowest low of the previous 8 completed 15m candles.

### Setup range width

`setup_high - setup_low`

### Breakout bar

The newly closed 15m candle that attempts to break beyond the setup boundary.

### R

`R` is the initial per-trade risk in price terms:

- for longs: `entry_price - initial_stop`
- for shorts: `initial_stop - entry_price`

## Higher-Timeframe Trend Bias

The strategy only takes long breakouts when the higher-timeframe trend is long-biased, and only takes short breakouts when the higher-timeframe trend is short-biased.

### Long bias rule

Use the **1h** chart.

Long bias is active only when all of the following are true on the latest completed 1h candle:

- 1h EMA(50) > 1h EMA(200)
- latest completed 1h close > 1h EMA(50)
- 1h EMA(50) is rising versus 3 completed 1h candles earlier

### Short bias rule

Short bias is active only when all of the following are true on the latest completed 1h candle:

- 1h EMA(50) < 1h EMA(200)
- latest completed 1h close < 1h EMA(50)
- 1h EMA(50) is falling versus 3 completed 1h candles earlier

### Neutral state

If neither long nor short bias is active, the strategy does not trade.

## Setup / Consolidation Rules

A valid setup requires short-term compression before breakout.

Use the previous 8 completed 15m candles.

A setup is valid only when all of the following are true:

1. `setup_range_width <= 1.75 * ATR(20)` on 15m
2. absolute net drift over the setup window is limited:
   - `abs(close[-1] - open[-8]) <= 0.35 * setup_range_width`
3. no current open position exists on the symbol
4. no same-direction re-entry is allowed until a new valid setup window has formed after the previous exit

### Why this setup logic is selected

This structure is intended to distinguish a real compression/base from a loose drift or chaotic chop.

The range-width condition ensures the breakout is not simply firing out of an already extended structure.

The net-drift condition reduces the chance that a one-sided grind is mislabeled as a neutral base.

## Entry Trigger Rules

Entries are based on **bar-close confirmation**, not intrabar pokes.

### Long entry trigger

A long signal is generated when all of the following are true on the newly completed 15m breakout bar:

1. long higher-timeframe bias is active
2. a valid setup exists from the previous 8 completed 15m candles
3. breakout bar close > `setup_high + 0.10 * ATR(20)`
4. breakout bar true range >= `1.0 * ATR(20)`
5. breakout bar closes in the **top 25%** of its own high-low range
6. 1h normalized ATR filter is satisfied:
   - `0.20% <= ATR(20) / close <= 2.00%`

### Short entry trigger

A short signal is generated when all of the following are true on the newly completed 15m breakout bar:

1. short higher-timeframe bias is active
2. a valid setup exists from the previous 8 completed 15m candles
3. breakout bar close < `setup_low - 0.10 * ATR(20)`
4. breakout bar true range >= `1.0 * ATR(20)`
5. breakout bar closes in the **bottom 25%** of its own high-low range
6. 1h normalized ATR filter is satisfied:
   - `0.20% <= ATR(20) / close <= 2.00%`

## Entry Execution Method

### Selected entry method

**Enter at market immediately after the 15m signal candle closes.**

### Why market entry is selected for v1

This is an intentional engineering simplification.

The strategy is designed around closed-candle confirmation on a 15m timeframe. Because BTCUSDT is highly liquid and the system is not operating on a microstructure-sensitive horizon, the implementation benefits of bar-close market entry outweigh the added complexity of resting breakout-stop entry logic for v1.

## Initial Stop Logic

### Long initial stop

For a long position:

`initial_stop = min(setup_low, breakout_bar_low) - 0.10 * ATR(20)`

### Short initial stop

For a short position:

`initial_stop = max(setup_high, breakout_bar_high) + 0.10 * ATR(20)`

### Stop-distance filter

A trade is rejected if:

- stop distance < `0.60 * ATR(20)`
- or stop distance > `1.80 * ATR(20)`

### Why this stop logic is selected

The stop is structural rather than arbitrary.

It is placed beyond the setup invalidation zone, with an ATR buffer to reduce trivial trigger-outs from noise.

The stop-distance filter prevents taking trades whose required risk is either unrealistically tight or too wide relative to current volatility.

## Position Sizing Philosophy

### Core principle

Position size is determined by:

1. account equity,
2. allowed account risk,
3. stop distance,
4. symbol constraints,
5. and leverage caps.

Leverage is a **tool**, not a target.

The strategy is sized from **stop distance and account-risk allowance**, not from a desired leverage multiple.

### Deployment-stage risk policy

Risk settings must be stage-specific.

#### Research / simulation phase

Backtests and simulations should analyze multiple per-trade risk levels, including:

- 0.25%
- 0.50%
- 1.00%
- 1.50%
- 2.00%

This is for sensitivity analysis, not for immediate live deployment.

#### Initial live phase

- **starting live risk per trade:** `0.25% of account equity`
- **maximum effective leverage cap:** `2x`
- **maximum concurrent positions:** `1`

#### Future mature phase

A later increase toward `0.50%` or `1.00%` risk per trade may be considered only after:

- strategy validation,
- paper / shadow trading success,
- stable live execution,
- acceptable drawdown behavior,
- and explicit review of worst-case loss clustering.

Risk above `1.00%` per trade should require a much higher burden of proof.

### Position size calculation

Position size is the minimum of:

1. stop-based risk size,
2. max-leverage-based size,
3. leverage-bracket-compliant size,
4. internal hard notional cap.

## Protective Exchange-Side Stop

Immediately after entry, place a protective exchange-side stop.

### Selected protective stop type

- **Algo order type:** `STOP_MARKET`
- **Close behavior:** `closePosition=true`
- **Working type:** `MARK_PRICE`
- **Price protection:** `TRUE`

### Why this is selected

The system should always have an exchange-side disaster stop in place, even if the engine fails.

Using `closePosition=true` keeps the protective stop aligned with the actual open position rather than relying on fragile quantity bookkeeping in the first version.

Using `MARK_PRICE` reduces sensitivity to last-trade distortions.

## Exit Logic

The strategy uses staged trade management rather than a pure fixed take-profit.

### Exit philosophy

The system should:

1. respect the original structural invalidation,
2. avoid moving to break-even too early,
3. reduce risk only after the trade has proven itself,
4. and preserve the ability to participate in larger continuation moves.

### Stage 1: initial protection

After entry, the original structural stop remains active.

The exchange-side protective stop acts as the hard fail-safe.

### Stage 2: no early stop reduction

The stop is **not** moved immediately after minor favorable movement.

Before the trade reaches at least **+1.0R maximum favorable excursion**, the initial stop remains unchanged unless an operational safety condition requires action.

### Stage 3: first risk reduction

When the trade reaches **+1.0R MFE**, reduce risk but do not necessarily move the stop all the way to break-even.

#### Research default

- move stop from full initial risk to **-0.25R**

This means the trade is still allowed some room to fluctuate, but the original full-loss exposure is reduced materially.

### Stage 4: break-even transition

When the trade reaches **+1.5R MFE**, move the stop to **break-even**.

This transition should happen only after the trade has shown meaningful follow-through.

### Stage 5: transition to trailing mode

When the trade reaches **+2.0R MFE**, activate a trailing stop.

#### Long trailing exit

For a long trade:

`trail_level = highest_high_since_entry - 2.5 * ATR(20)`

If a completed 15m close is below the current trail level, exit the trade at market.

#### Short trailing exit

For a short trade:

`trail_level = lowest_low_since_entry + 2.5 * ATR(20)`

If a completed 15m close is above the current trail level, exit the trade at market.

### Stage 6: optional tighter management beyond +3R

Once the trade reaches **+3.0R MFE**, the system may either:

- keep the same trailing logic,
- or tighten the trailing logic slightly.

For v1, this remains a **benchmarking decision**, not a locked production rule.

### Stage 7: stagnation exit

If, after **8 completed 15m bars** from entry, the trade has not reached at least **+1.0R MFE**, exit the trade at market.

This is intended to remove capital from failed or stalled breakouts rather than letting them drift indefinitely.

### Why this exit design is selected

This design tries to balance three competing needs:

- avoid cutting valid trades too early,
- reduce exposure once the trade proves itself,
- and preserve participation in rare larger trend moves.

## Re-Entry Rules

The strategy does **not** immediately re-enter in the same direction after exit.

A same-direction re-entry is only permitted when:

- a completely new valid 8-bar setup forms,
- and a new breakout signal is generated.

This is intended to reduce repeated chasing after a failed or already extended move.

## No-Trade Filters

A new trade must be rejected if any of the following are true:

1. higher-timeframe bias is neutral
2. setup is not valid
3. 1h normalized ATR filter is outside the allowed range
4. stop-distance filter fails
5. market data is stale
6. user data / position state is stale or unreconciled
7. current spread exceeds the execution safety threshold defined by the execution layer
8. daily loss lockout is active
9. drawdown pause is active
10. exchange or websocket health checks are degraded

## Operational Rules

### One symbol only

Version 1 runs on **BTCUSDT only**.

### One position only

The system allows only **one open position at a time**.

### One-way mode only

The system assumes Binance futures **one-way mode**.

### Isolated margin only

The system assumes **isolated margin**.

### Supervised deployment only

The first live deployment is operator-supervised.

## Failure Modes

This strategy is expected to fail primarily in the following conditions:

### 1. Chop with repeated false breaks

The main expected loss pattern is repeated failed breakout attempts in sideways markets.

### 2. Lagging bias filter during reversals

A higher-timeframe EMA filter can remain aligned with an old trend during the early phase of reversal.

### 3. Breakout exhaustion

Some breakout bars may represent the end of a move rather than the beginning of continuation.

### 4. Volatility shock conditions

Sudden event-driven conditions can invalidate normal breakout behavior and increase slippage.

### 5. Operational execution failure

If user-stream state, stop placement, or reconciliation fails, strategy correctness becomes secondary to operational risk.

## Validation Requirements

The strategy must not be promoted to live trading unless all of the following are satisfied.

### Research validation

- backtest includes fees, funding, and slippage
- walk-forward validation is used
- no random time-series shuffling is used
- parameter sensitivity is acceptable
- multiple market regimes are evaluated
- long and short performance are reviewed separately
- exit-management benchmarks are compared directly

### Required exit benchmarks

Even if the staged management model is the preferred live candidate, the following benchmark variants must also be tested for comparison:

1. fixed 2R exit
2. fixed 3R exit
3. staged stop-reduction + trailing exit
4. opposite-signal-only exit

This is required to check whether the chosen live exit logic is genuinely useful or merely more complicated.

### Execution validation

- signal generation is reproducible from historical data
- live bar-close signal timing is verified
- exchange-side stop placement is verified
- order and position reconciliation is verified
- restart recovery is verified
- websocket reconnect / keepalive logic is verified

## Decisions

The following decisions are accepted for the first concrete strategy specification:

- **strategy family:** breakout continuation with trend filter
- **venue:** Binance USDⓈ-M futures
- **primary contract:** BTCUSDT perpetual
- **first secondary comparison symbol:** ETHUSDT perpetual
- **signal timeframe:** 15m
- **higher timeframe bias:** 1h
- **trend filter:** EMA(50) / EMA(200) with price-location and slope confirmation
- **setup type:** compression-range breakout
- **entry style:** bar-close market entry
- **position mode:** one-way
- **margin mode:** isolated
- **deployment scope:** one symbol, one position, supervised rollout
- **stop model:** structural stop + ATR buffer + exchange-side protection
- **exit philosophy:** staged risk reduction, then trailing, not pure fixed take-profit
- **initial live risk:** 0.25% equity risk per trade

## Open Questions

The following remain open and must be resolved during research and validation, not by assumption:

1. Should the setup window remain 8 bars, or test 6 / 10 / 12 as alternatives?
2. Should the breakout buffer remain 0.10 ATR?
3. Should the breakout expansion threshold remain 1.0 ATR?
4. Is EMA(50)/EMA(200) the best higher-timeframe bias pair, or should EMA(20)/EMA(100) or another simpler filter be compared?
5. Should the normalized ATR regime bounds be adjusted for BTCUSDT after data review?
6. Should the trailing multiplier remain 2.5 ATR?
7. Should the first stop-reduction level be -0.25R, -0.10R, or another benchmarked value?
8. Should the break-even transition happen at +1.5R or +2.0R?
9. Should the trail tighten automatically after +3R, or remain unchanged?
10. Should ETHUSDT be the first secondary implementation after BTCUSDT?
11. Under what evidence threshold should mature live risk increase from 0.25% toward 0.50% or 1.00%?

## Next Steps

The next strategy documents should be:

1. `docs/03-strategy-research/v1-breakout-backtest-plan.md`
2. `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`
3. `docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md`

## References

Binance and market-structure references used for this specification:

- Binance USDⓈ-M Futures New Order REST API  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api

- Binance USDⓈ-M Futures New Algo Order REST API  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/New-Algo-Order

- Binance USDⓈ-M Futures User Data Streams  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams

- Binance USDⓈ-M Futures WebSocket API General Info  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-api-general-info

- Binance USDⓈ-M Futures Exchange Information  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Exchange-Information

- Binance USDⓈ-M Futures Notional and Leverage Brackets  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Notional-and-Leverage-Brackets

- Binance USDⓈ-M Futures User Commission Rate  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/User-Commission-Rate

- Binance USDⓈ-M Futures Funding Rate History  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History

- Binance Derivatives Change Log  
  https://developers.binance.com/docs/derivatives/change-log

Research references:

- Nguyen & Chan (2024), Cryptocurrency trading: A systematic mapping study  
  https://www.sciencedirect.com/science/article/pii/S2667096824000296

- Wen et al. (2022), Intraday return predictability in the cryptocurrency markets: Momentum, reversal, or both  
  https://www.sciencedirect.com/science/article/abs/pii/S1062940822000833

- Fieberg et al. (2025), A Trend Factor for the Cross Section of Cryptocurrency Returns  
  https://www.cambridge.org/core/services/aop-cambridge-core/content/view/4C1509ACBA33D5DCAF0AC24379148178/S0022109024000747a.pdf/trend_factor_for_the_cross_section_of_cryptocurrency_returns.pdf

- Rohrbach et al. (2017), Momentum and trend following trading strategies for currencies and bitcoin  
  https://assets.super.so/e46b77e7-ee08-445e-b43f-4ffd88ae0a0e/files/9c27aa78-9b14-4419-a53d-bc56fa9d43b2.pdf