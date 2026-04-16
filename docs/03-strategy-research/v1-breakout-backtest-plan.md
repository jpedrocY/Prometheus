# V1 Breakout Backtest Plan

## Purpose

This document defines the research and validation plan for backtesting the v1 breakout strategy.

The goal of this plan is not to maximize backtest beauty. The goal is to test the strategy honestly, conservatively, and in a way that reduces false confidence before paper trading, shadow trading, or live deployment.

## Scope

This document defines:

- the data scope,
- the backtest simulation assumptions,
- the validation structure,
- the cost model,
- the comparison matrix,
- the core evaluation metrics,
- the promotion criteria,
- and the main anti-overfitting constraints.

This document does **not** define implementation code, final production thresholds, or portfolio-level deployment.

## Background

The project has already selected the following as the v1 strategy direction:

- Binance USDⓈ-M futures,
- BTCUSDT as the primary symbol,
- ETHUSDT as the first secondary comparison symbol,
- 15m signal timeframe,
- 1h higher-timeframe trend bias,
- breakout continuation with trend filter,
- market entry after confirmed bar close,
- structural stop with ATR buffer,
- staged exit management.

Because the strategy is based on **completed 15m candle confirmation**, the backtest must avoid look-ahead leakage in the fill model.

A signal that depends on the final close of a bar cannot be honestly filled at that same close unless a stronger intrabar execution assumption is explicitly justified and modeled. Therefore, the baseline backtest assumption for v1 is:

- detect signal at bar close,
- simulate fill at the next bar open,
- then apply fees, funding, and slippage.

This is intentionally conservative.

## Data Scope

### Primary symbol set

The first backtest phase uses:

- **BTCUSDT perpetual** as the primary research symbol
- **ETHUSDT perpetual** as the first secondary comparison symbol

### Core market data

Use Binance USDⓈ-M futures market data as the primary canonical source.

Required data:

- 15m klines
- 1h klines
- mark price klines for sensitivity analysis
- funding rate history
- exchange information
- leverage bracket information
- commission rate information

### Why these data sources are required

#### 15m and 1h klines
These are required for signal generation and higher-timeframe bias.

#### Mark price data
This is required because live protective stops are intended to work with `MARK_PRICE`, so stop-behavior sensitivity should not rely only on trade-price candles.

#### Funding rate history
This is required because perpetual futures PnL is affected by funding, and ignoring funding can distort long/short performance.

#### Exchange information
This is required to validate symbol constraints, price precision, quantity precision, and minimum tradable increments.

#### Leverage bracket data
This is required because allowable notional and leverage constraints are symbol- and bracket-dependent.

#### Commission rate data
This is required because fee assumptions must be explicit and should match the intended account conditions as closely as possible.

## Data Sources

### Binance endpoints to use

#### Standard futures klines
- `GET /fapi/v1/klines`

#### Mark price klines
- `GET /fapi/v1/markPriceKlines`

#### Funding rate history
- `GET /fapi/v1/fundingRate`

#### Exchange information
- `GET /fapi/v1/exchangeInfo`

#### User commission rate
- `GET /fapi/v1/commissionRate`

#### Notional and leverage brackets
- `GET /fapi/v1/leverageBracket`

## Data Handling Rules

### Time alignment

All 15m and 1h data must be aligned by completed-bar timestamps only.

The backtest must never use partial-bar information from a bar whose close has not yet occurred in simulation time.

### Higher-timeframe derivation

Preferred approach:

- build 1h data from the same canonical futures kline source used for 15m data

Alternative approach:

- if 1h klines are fetched directly, confirm they match the aggregation logic and exchange timestamps

### Missing data handling

If historical data is missing or malformed:

- do not forward-fill price bars blindly
- either remove the affected interval from testing or mark it as invalid for signal generation
- explicitly log all removed or invalid periods

### Point-in-time rule

Only information that would have been known at the simulated decision timestamp may be used.

This includes:

- completed 15m bars only
- completed 1h bars only
- funding values only when historically effective
- symbol constraints only if valid for the test period assumptions

## Simulation Assumptions

## Baseline fill model

### Signal timing
A signal is generated only after the 15m breakout bar has fully closed.

### Entry timing
The baseline v1 backtest assumes entry at:

- **next-bar open**
- plus fees
- plus slippage

### Why this is the baseline
This avoids the common backtest mistake of using the close of the same bar that was required to confirm the signal.

## Exit timing

### Structural and managed exits
Exits triggered by bar-close rules are modeled at the next available executable price under the same conservative philosophy.

### Protective stop behavior
Protective stops should be modeled as stop-triggered exits that are subject to:

- adverse trigger conditions,
- slippage,
- fee application,
- and realistic stop execution assumptions.

### Stop trigger reference
Primary backtest logic should use trade-price bars for the main simulation, but a separate sensitivity analysis should test how results change when stop behavior is evaluated with mark-price information.

## Cost Model

### Required cost components

Every backtest run must include:

- entry fees
- exit fees
- funding payments / receipts
- slippage
- spread allowance where relevant

### Fee assumptions

Baseline assumption:

- assume **taker fees** for entry
- assume **taker fees** for stop exits
- assume **taker fees** for forced market exits
- optionally benchmark maker-style alternatives later, but not in the first honest baseline

### Funding assumptions

Funding must be applied based on historical funding-rate data and position direction.

This is especially important because long and short profitability can diverge materially once funding is included.

### Slippage assumptions

The first backtest phase should run under multiple slippage environments.

Recommended initial slippage buckets:

- **low slippage**
- **medium slippage**
- **high slippage**

These may be implemented as fixed basis-point assumptions at first, then refined later using more detailed market-data research.

### Cost-model philosophy

The strategy should be considered fragile if its edge disappears under modestly conservative cost assumptions.

## Validation Structure

## Layer A — development phase

Purpose:

- shape the initial strategy logic
- reject obviously weak variants
- confirm that the strategy behaves roughly as intended

Rules:

- may be used for exploratory development
- results from this phase are **not** sufficient for promotion

## Layer B — walk-forward validation

Purpose:

- test whether performance survives across rolling or expanding time windows
- evaluate whether the strategy remains viable across multiple market conditions

Rules:

- test windows must always occur after train/development windows
- no random shuffling
- no leakage across folds
- each fold should be logged separately

## Layer C — final holdout

Purpose:

- provide one final research check before paper/shadow deployment

Rules:

- this period should remain untouched during development
- it should be evaluated only after major design choices are already stable
- it should not be repeatedly mined for parameter tuning

## Anti-overfitting Policy

The project must treat overfitting as a default danger, not a rare accident.

Rules:

1. keep the first parameter grid intentionally limited
2. document every tested variant
3. do not treat the single best equity curve as the winner by default
4. prefer stable parameter regions over sharp peaks
5. require robustness across symbols, windows, and cost assumptions
6. preserve a final holdout period
7. avoid adding extra filters unless they improve out-of-sample robustness, not just in-sample appearance

## Comparison Matrix

The first formal comparison matrix should include the following.

### Symbol comparison
- BTCUSDT
- ETHUSDT

### Exit comparison
- fixed 2R exit
- fixed 3R exit
- staged stop reduction + trailing exit
- opposite-signal-only exit

### Trend filter comparison
- EMA 50 / 200
- EMA 20 / 100

### Setup window comparison
- 6 bars
- 8 bars
- 10 bars
- 12 bars

### Breakout buffer comparison
- 0.05 ATR
- 0.10 ATR
- 0.15 ATR

### Stop buffer comparison
- 0.05 ATR
- 0.10 ATR
- 0.15 ATR

### Optional later comparison, not phase 1
- 10m signal timeframe
- alternative trail multipliers
- alternative break-even transition thresholds
- ETHUSDT standalone optimization only after BTCUSDT baseline is understood

## What Is Explicitly Excluded from the First Backtest Phase

The first research pass should **not** include:

- portfolio-level backtesting
- multiple simultaneous symbols in one portfolio
- hedge mode
- partial profit-taking logic
- machine learning overlays
- alternative data
- dynamic leverage policies
- adaptive parameter switching
- large indicator stacks
- highly discretionary structure labels

The purpose of phase 1 is to understand the core strategy, not to build the most complicated simulation possible.

## Metrics to Review

The strategy must be reviewed using a broad set of metrics.

### Core performance metrics
- total return
- net return after fees, funding, and slippage
- max drawdown
- return / drawdown
- expectancy per trade
- profit factor

### Trade quality metrics
- win rate
- average winner
- average loser
- average R per trade
- median R per trade
- long vs short breakdown
- stop-out frequency
- stagnation-exit frequency
- trailing-exit contribution

### Stability metrics
- trade count
- monthly consistency
- yearly consistency if enough history exists
- worst losing streak
- equity-curve smoothness
- sensitivity to cost assumptions
- sensitivity to parameter changes

### Regime-aware metrics
Where possible, split results by:
- high-volatility vs lower-volatility periods
- strong-trend vs choppy periods
- long-only and short-only subsets
- BTCUSDT vs ETHUSDT comparison

## Evaluation Standards

A variant should not be considered promising just because it has the highest return.

A variant is preferable when it shows:

- acceptable drawdown,
- acceptable loss clustering,
- decent trade count,
- stable behavior across windows,
- limited collapse under conservative costs,
- and no dependence on a single razor-thin parameter choice.

## Promotion Criteria

A strategy variant may be considered for paper/shadow deployment only if:

1. it survives walk-forward validation
2. it remains viable under conservative cost assumptions
3. it does not rely on one narrow parameter peak
4. its behavior makes sense on both BTCUSDT and ETHUSDT, even if BTC remains stronger
5. long and short performance are both structurally understandable
6. the chosen exit model either outperforms simpler baselines or clearly justifies itself through robustness
7. the live execution assumptions remain realistic for Binance USDⓈ-M futures

## Required Deliverables from the Backtest Phase

The backtest phase should produce:

1. a dataset summary
2. a parameter sweep summary
3. walk-forward fold results
4. holdout results
5. cost-sensitivity results
6. long/short split results
7. BTC vs ETH comparison
8. exit-model comparison
9. a promotion recommendation
10. a list of unresolved weaknesses

## Decisions

The following decisions are accepted for the v1 backtest plan:

- primary backtest symbol: **BTCUSDT**
- first secondary comparison symbol: **ETHUSDT**
- signal timeframe: **15m**
- higher-timeframe bias: **1h**
- baseline signal source: **standard futures klines**
- baseline fill model: **next-bar open after confirmed signal close**
- cost model includes: **fees + funding + slippage**
- validation structure: **development + walk-forward + final holdout**
- comparison matrix includes: **exits, trend filters, setup windows, breakout buffers, stop buffers**
- first backtest phase excludes portfolio and ML complexity

## Open Questions

The following remain open and should be answered by the backtest results rather than opinion alone:

1. Which exit model is most robust after realistic costs?
2. Does BTCUSDT clearly dominate ETHUSDT for this strategy, or are both similarly viable?
3. Is EMA 50 / 200 materially more robust than EMA 20 / 100?
4. Which setup-window length is most stable across folds?
5. Which breakout buffer and stop buffer are most robust rather than merely most profitable?
6. How sensitive is the strategy to slippage assumptions?
7. Does mark-price-based stop sensitivity materially change the conclusions?
8. Is the staged exit model genuinely better than fixed 2R / 3R exits?
9. Does the strategy degrade sharply during specific volatility regimes?
10. What evidence level is sufficient to move from research to paper/shadow deployment?

## Next Steps

After this document, the next files should be:

1. `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`
2. `docs/04-data/historical-data-spec.md`
3. `docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md`

## References

Binance references:

- Binance USDⓈ-M Futures Kline/Candlestick Data  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Kline-Candlestick-Data

- Binance USDⓈ-M Futures Mark Price Kline/Candlestick Data  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Mark-Price-Kline-Candlestick-Data

- Binance USDⓈ-M Futures Get Funding Rate History  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History

- Binance USDⓈ-M Futures User Commission Rate  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/User-Commission-Rate

- Binance USDⓈ-M Futures Exchange Information  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Exchange-Information

- Binance USDⓈ-M Futures Notional and Leverage Brackets  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Notional-and-Leverage-Brackets

Validation references:

- scikit-learn TimeSeriesSplit  
  https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html

- Bailey et al., The Probability of Backtest Overfitting  
  https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf