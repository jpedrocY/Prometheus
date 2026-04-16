# Timestamp Policy

## Purpose

This document defines the timestamp and time-handling policy for the project.

Its purpose is to ensure that:

- historical data is stored consistently,
- strategy logic uses time correctly,
- backtests remain point-in-time valid,
- live execution logic does not use incomplete information,
- and operational debugging remains traceable.

This document exists because time-related errors can silently invalidate strategy research, execution behavior, and reconciliation logic.

## Scope

This document governs time handling for:

- raw market data,
- normalized datasets,
- derived datasets,
- historical backtests,
- live signal generation,
- live exchange interaction,
- and operational event tracking.

This document does **not** define general clock-synchronization tooling or UI display preferences beyond the canonical-policy rules.

## Background

The project uses Binance USDⓈ-M futures data and execution APIs.

Binance’s current futures APIs and streams use timestamp-based logic extensively, including:

- signed REST requests with millisecond timestamps,
- bar datasets with open and close times,
- user data streams with time-sensitive lifecycle management,
- and kline streams that update unfinished candles before they close.

Because the strategy uses:

- 15m bar-close breakout confirmation,
- 1h higher-timeframe bias,
- and strict no-look-ahead rules,

the project must define a strict time policy that prevents accidental use of partial bars, stale events, or ambiguous timezone conversions.

## Canonical Time Standard

## Canonical timezone

The canonical timezone for all project logic and stored timestamps is:

- **UTC**

### Rule
No canonical market, strategy, execution, or state timestamp may be stored in a local timezone.

### Why this policy is selected
UTC avoids:
- local machine timezone ambiguity,
- daylight-saving issues,
- region-specific conversion mistakes,
- and inconsistent comparisons across systems.

## Canonical timestamp format

The canonical timestamp format is:

- **Unix milliseconds**

### Rule
Canonical timestamps must be stored as numeric UTC millisecond timestamps wherever possible.

### Human-readable representations
ISO-8601 or other human-readable timestamps may be used in:

- reports,
- logs,
- dashboards,
- or debugging outputs,

but they must be derived from canonical UTC timestamps rather than replacing them.

## Bar Time Policy

## Canonical bar key

Every bar is identified canonically by:

- **open_time**

### Rule
For all bar datasets, the canonical primary key must use:

- `symbol`
- `interval`
- `open_time`

### Why this policy is selected
This aligns with Binance’s kline model and keeps bar identity stable across:

- raw data,
- normalized data,
- derived data,
- and backtesting.

## Close time handling

`close_time` must be retained where available, but it is not the canonical bar identifier.

### Purpose of close time
`close_time` is useful for:

- debugging,
- bar-completion checks,
- aggregation verification,
- and event alignment.

But `open_time` remains the identity key.

## Completed-Bar Policy

## Core rule

**Only completed bars may be used for strategy logic.**

This is a hard rule.

## Implications

### Historical backtests
Backtests may only generate signals from bars that were fully completed at the simulated decision time.

### Live trading
Live signal generation must not use partial-candle updates as if they were final bars.

### Higher-timeframe logic
Higher-timeframe bias must be based only on the latest completed higher-timeframe bar, not on a currently forming one.

## Why this policy is necessary

Binance kline streams update the current candle during its formation.

That means a 15m or 1h stream update may represent an unfinished candle.

Using unfinished bars would introduce look-ahead-like contamination or unstable logic in both live trading and research.

## Signal-Time Rules

## 15m signal rule

For the v1 breakout strategy:

- a 15m signal may only be evaluated after the 15m breakout bar has fully closed

### Implication
The strategy must not act on an intrabar breakout that has not yet been confirmed at candle close.

## 1h bias rule

For the v1 breakout strategy:

- the 1h bias may only use the latest completed 1h bar that existed at the 15m decision time

### Implication
If a 15m signal occurs while the current 1h candle is still forming, that partial 1h candle must not be used in the bias calculation.

## Higher-Timeframe Alignment Policy

## Alignment rule

When lower-timeframe and higher-timeframe data are used together:

- the higher-timeframe bar must be the most recent fully completed higher-timeframe bar available at the lower-timeframe decision timestamp

### Example
If a 15m signal is evaluated at the close of a 15m bar, the corresponding 1h bias must come from the most recent completed 1h candle available at that exact decision point.

### Why this policy matters
Without this rule, the system can accidentally use future higher-timeframe information.

This kind of leakage is subtle and dangerous because it may not be visually obvious while still distorting both backtests and live logic.

## Event Time vs Processing Time

## Event time

Event time is:

- the timestamp associated with the event by the exchange or dataset source

Examples:
- kline open time
- kline close time
- funding time
- order update event time
- account update event time

## Processing time

Processing time is:

- the timestamp at which the bot received, handled, or stored the event

## Rule

Where practical, live execution and observability systems should track both:

- event time
- processing time

## Why this matters

Tracking both time concepts helps with:

- debugging delayed events,
- measuring stream latency,
- understanding stale-state problems,
- and investigating reconciliation mismatches.

## REST Request Timestamp Policy

## Signed request timestamps

For signed Binance requests, request timestamps must be generated in:

- UTC
- Unix milliseconds

## Rule

The trading engine must use a reliable current UTC millisecond clock when signing requests.

## recvWindow rule

If `recvWindow` is used, it must be:

- explicitly set,
- documented,
- and kept conservative.

## Why this matters

Signed request validation depends on request time being acceptable to Binance.

Clock drift or inconsistent request-time handling can cause:

- rejected requests,
- intermittent failures,
- and confusing operational behavior.

## Funding Time Policy

## Core rule

Funding is an event-based timestamped dataset.

It must be joined and applied using:

- **funding timestamps**

### Forbidden assumption
Funding must not be assumed to belong automatically to:

- candle open times,
- candle close times,
- or arbitrary bar buckets

unless that transformation is explicitly documented and justified for a derived analysis view.

## Why this policy is selected

Funding is not bar-native market data.

It is a periodic account-impact event and must be treated accordingly in backtesting and reporting.

## Stream Freshness Policy

## Core rule

Live trading must not proceed normally if private or required market streams are stale.

## Freshness concepts

A stream may be considered stale if:

- expected events stop arriving,
- keepalive lifecycle is not maintained,
- reconnect requirements are missed,
- or timing gaps exceed operational expectations.

## Operational implication

If required streams are stale:

- block new entries
- surface the exception clearly
- reconcile state after recovery
- only resume normal strategy actions once state confidence is restored

## User stream lifecycle note

Because Binance user streams require keepalive maintenance and expire if not maintained, stream freshness is not optional operational detail. It is a core time-handling concern.

## Local Timezone Policy

## Core rule

Local timezone settings must never affect canonical trading logic.

### Allowed use of local time
Local time may be used only for:

- UI display,
- operator dashboards,
- human-readable summaries,
- and convenience formatting.

### Forbidden use of local time
Local time must not be used for:

- bar identity,
- signal generation,
- request signing,
- state comparison,
- or canonical data storage.

## Clock Consistency Policy

## System clock expectation

The machine running the bot must maintain reasonably accurate system time.

## Rule

Clock accuracy is an operational dependency for:

- signed request validity,
- event ordering analysis,
- stream freshness checks,
- and reconciliation debugging.

### Operational implication
Large clock drift must be treated as a meaningful system health problem.

## Historical Dataset Rules

## Raw layer

Raw data should preserve source timestamps exactly as returned by the source where practical.

## Normalized layer

Normalized datasets must store timestamps in canonical UTC millisecond form.

## Derived layer

Derived datasets must inherit canonical time rules and must document any transformation that changes bar granularity or event grouping.

## Backtest Time Rules

## Signal generation rule

Signals must be evaluated only on data available at the simulated decision time.

## Fill modeling rule

If a signal depends on a bar close, the baseline simulation must not assume a fill at that same close unless a separate execution model explicitly justifies it.

For the v1 breakout strategy, the baseline simulation rule remains:

- signal generated at confirmed bar close
- baseline fill modeled at next-bar open

## Holdout and walk-forward rule

All validation windows must preserve chronological ordering.

No time-shuffling is allowed.

## Logging and Observability Guidance

Where practical, logs and monitoring should include:

- canonical UTC timestamp,
- event time,
- processing time,
- symbol,
- interval where relevant,
- and event type.

This helps reconstruct failures involving:

- delayed fills,
- stale streams,
- misordered events,
- and reconciliation problems.

## Decisions

The following decisions are accepted for the project timestamp policy:

- canonical timezone is **UTC**
- canonical timestamp format is **Unix milliseconds**
- canonical bar key is **open_time**
- strategy logic may use **completed bars only**
- higher-timeframe logic may use **completed higher-timeframe bars only**
- event time and processing time should be tracked separately where practical
- signed REST request timestamps must use UTC millisecond time
- local timezone is display-only and never canonical
- stale streams must block new entries until resolved
- funding must be joined by funding timestamp, not assumed bar membership
- baseline backtests must preserve time-order integrity and no-look-ahead execution assumptions

## Open Questions

The following remain open:

1. What exact freshness thresholds should define a stale market-data stream?
2. What exact freshness thresholds should define a stale user-data stream?
3. What `recvWindow` value should become the implementation default?
4. What specific operational alert thresholds should be used for clock drift?
5. Should event time and processing time both be persisted in all execution-event logs or only in selected observability tables?

## Next Steps

After this document, the next recommended files are:

1. `docs/04-data/dataset-versioning.md`
2. `docs/09-operations/restart-procedure.md`
3. `docs/10-security/api-key-policy.md`

## References

Binance references:

- Binance USDⓈ-M Futures General Info  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info

- Binance USDⓈ-M Futures Kline/Candlestick Data  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Kline-Candlestick-Data

- Binance USDⓈ-M Futures User Data Streams  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams

- Binance USDⓈ-M Futures Kline/Candlestick Streams  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Kline-Candlestick-Streams