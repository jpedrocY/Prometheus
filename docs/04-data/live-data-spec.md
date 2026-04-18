# Live Data Specification

## Purpose

This document defines the live market-data specification for the v1 Prometheus trading system.

Its purpose is to make live market-data behavior explicit enough that the runtime can:

- evaluate the v1 strategy only from completed bars,
- avoid using partial candles as confirmed information,
- detect stale or degraded market-data conditions,
- publish strategy-ready bar events deterministically,
- support higher-timeframe alignment without look-ahead leakage,
- separate market-data truth from account/execution truth,
- and provide the observability needed for supervised operation.

This document fills the live-data gap left by the historical data specification.

The historical data specification defines research datasets, Parquet/DuckDB storage, timestamp policy, and versioning. This document defines how live market data should enter the running bot.

## Scope

This specification applies to live market-data behavior for v1 with the following assumptions:

- venue: Binance USDⓈ-M futures
- primary live symbol: BTCUSDT perpetual
- first research comparison symbol: ETHUSDT perpetual
- live strategy symbol in v1: BTCUSDT only
- signal timeframe: 15m
- higher-timeframe bias: 1h
- strategy execution style: completed-bar confirmation
- live deployment model: supervised
- runtime model: modular monolith
- exchange-side protective stop is mandatory for live positions

This document covers:

- live data source categories,
- market-data stream responsibilities,
- completed-bar publication rules,
- partial-candle handling,
- higher-timeframe alignment,
- mark-price handling,
- market-data freshness,
- stale/degraded stream behavior,
- REST backfill and recovery usage,
- event contracts for live data,
- observability requirements,
- and implementation constraints.

This document does **not** define:

- private user-stream order/account event handling,
- execution order placement,
- reconciliation of open orders or positions,
- historical research dataset storage,
- full database schema,
- frontend dashboard layout,
- or final infrastructure deployment.

Those are covered by other documents.

---

## Background

The v1 strategy depends on strict time discipline.

The strategy uses:

- 15m signal logic,
- 1h higher-timeframe bias,
- breakout continuation,
- bar-close confirmation,
- and market entry after a confirmed signal.

Because Binance kline streams update candles during formation, live market data must distinguish clearly between:

- partial kline updates,
- final closed kline updates,
- strategy-ready completed bars,
- stale market-data state,
- and recovery/backfill state.

A live market-data implementation that accidentally evaluates strategy logic on unfinished bars would violate the project’s timestamp policy and make live behavior diverge from the backtest assumptions.

The live data layer must therefore be treated as a safety-relevant runtime component, not a passive feed reader.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/04-data/historical-data-spec.md`
- `docs/04-data/timestamp-policy.md`
- `docs/04-data/dataset-versioning.md`
- `docs/03-strategy-research/v1-breakout-strategy-spec.md`
- `docs/03-strategy-research/v1-breakout-backtest-plan.md`
- `docs/08-architecture/implementation-blueprint.md`
- `docs/08-architecture/state-model.md`
- `docs/08-architecture/internal-event-contracts.md`
- `docs/08-architecture/observability-design.md`
- `docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md`
- `docs/09-operations/restart-procedure.md`
- `docs/09-operations/incident-response.md`

### Authority hierarchy

If this document conflicts with the timestamp policy on completed-bar usage, the timestamp policy wins.

If this document conflicts with the state model on runtime safety state, the state model wins.

If this document conflicts with order/execution docs on account or position truth, the execution and reconciliation docs win.

---

## Core Principles

## 1. Completed bars only

The live strategy must use only completed bars.

Partial kline updates may be observed, stored temporarily, and used for health/diagnostic display, but they must not be treated as final strategy input.

## 2. Market data is not account truth

Live market data can tell the bot about prices, bars, and reference prices.

It cannot tell the bot whether:

- an order was accepted,
- an order was filled,
- a position exists,
- a protective stop exists,
- or account state is synchronized.

Those facts must come from user-stream events, REST reconciliation, and exchange-authoritative state paths.

## 3. Market data freshness is a trading gate

If required live market data is stale, unavailable, or untrusted, the runtime must block new entries.

A stale data feed is not merely a technical warning. It can invalidate signal timing and trade-management decisions.

## 4. Higher-timeframe alignment must be point-in-time valid

At a 15m decision point, the strategy may only use the most recent fully completed 1h bar that was available at that decision time.

The currently forming 1h candle must not be used for 1h bias.

## 5. Live and historical behavior should remain comparable

The live completed-bar stream should produce bar objects whose fields and timestamp semantics align with the historical data model.

This supports:

- consistent strategy calculation,
- backtest/live parity,
- debugging,
- and post-run review.

## 6. REST is recovery support, not the primary live stream

The preferred live market-data path is streaming.

REST may be used for:

- startup bootstrap,
- recovery after gaps,
- sanity checks,
- fetching missing closed bars,
- and resynchronizing after stream interruption.

The runtime should avoid excessive polling and should not depend on REST polling as the normal live strategy clock unless explicitly approved later.

---

## Live Data Source Categories

The live data layer should distinguish these source categories.

## 1. Standard trade-price kline stream

Purpose:

- observe live 15m and 1h kline updates,
- detect completed candles,
- publish completed bars to the strategy layer.

For v1, the required symbol/interval combinations are:

- BTCUSDT 15m
- BTCUSDT 1h

ETHUSDT live streams are not required for the initial BTCUSDT-only live runtime, though they may be used in paper/shadow research comparisons if explicitly enabled.

## 2. Mark-price stream

Purpose:

- monitor mark-price reference behavior,
- support protective-stop observability,
- support later mark-price-sensitive diagnostics,
- provide runtime context for stop-related operator visibility.

The protective stop itself is exchange-side and uses mark price. The market-data layer may observe mark price, but it does not confirm stop existence or stop execution.

## 3. REST kline backfill

Purpose:

- bootstrap the runtime with enough recent completed bars,
- repair small market-data gaps,
- confirm closed-bar continuity after reconnect,
- and support recovery before strategy evaluation resumes.

## 4. Exchange metadata refresh path

Purpose:

- provide live or near-live symbol metadata needed for data validation and later execution checks.

This includes symbol status, precision, and trading constraints where relevant.

The live data layer may read metadata, but execution/risk layers remain responsible for enforcing order-level constraints.

## 5. Private user stream

The private user stream is not a market-data source.

It belongs to the user-stream/account event layer.

It is listed here only to make the boundary explicit:

- market-data streams support price/time/bar decisions,
- user-stream events support order/account/position/protection truth.

---

## Required Live Market Data for V1

## Mandatory live data

For BTCUSDT v1 live operation, the minimum required market data is:

- BTCUSDT 15m standard kline stream or equivalent completed-bar source
- BTCUSDT 1h standard kline stream or internally derived 1h completed bars
- BTCUSDT mark-price stream or equivalent mark-price reference feed
- REST access to recent standard klines for bootstrap/recovery

## Preferred higher-timeframe approach

The preferred approach for live 1h bias is:

- maintain live 15m completed bars,
- maintain or derive completed 1h bars in a point-in-time-valid way,
- evaluate 1h bias only from completed 1h bars.

Two implementation options are acceptable.

### Option A — Direct 1h live kline stream

The live data layer subscribes to:

- BTCUSDT 15m kline stream
- BTCUSDT 1h kline stream

A 15m strategy evaluation uses the latest completed 1h kline whose close time is less than or equal to the 15m decision time.

### Option B — Internal 1h aggregation from 15m completed bars

The live data layer derives 1h bars from four completed 15m bars.

If this is used, the aggregation logic must match canonical timestamp rules and must be tested.

### Recommended v1 default

Use direct 1h kline stream for initial runtime simplicity, but include tests that verify point-in-time alignment.

Internal aggregation may be added later if live/backtest parity requires it.

---

## Binance Stream Considerations

Binance USDⓈ-M futures currently provides market-data WebSocket stream documentation for kline/candlestick streams and mark-price streams.

Implementation must verify the current official Binance documentation at coding time because endpoint routing and WebSocket details can change.

### Kline stream behavior

The kline stream should be treated as an updating stream for the current candle.

Important implication:

- the bot must inspect whether a kline update represents a closed candle before publishing it as strategy-ready.

### Mark-price stream behavior

The mark-price stream is a reference-price feed.

It may update more frequently than strategy bars and should not be converted into trade-price candles unless explicitly documented as a separate derived view.

### Endpoint version sensitivity

The implementation must not hardcode undocumented assumptions about endpoint paths or connection categories.

If Binance announces endpoint migration, deprecation, or routing changes, the exchange adapter must be updated and tested before live use.

---

## Canonical Live Bar Model

A completed live bar should use a schema compatible with historical kline data.

Minimum required fields:

- `symbol`
- `interval`
- `open_time`
- `close_time`
- `open`
- `high`
- `low`
- `close`
- `volume`
- `quote_asset_volume` where available
- `trade_count` where available
- `taker_buy_base_volume` where available
- `taker_buy_quote_volume` where available
- `is_closed`
- `source`
- `event_time_utc_ms` where available
- `processed_at_utc_ms`

## Primary key

The canonical bar key is:

- `symbol`
- `interval`
- `open_time`

## Timestamp standard

All canonical timestamps must be:

- UTC
- Unix milliseconds

## Close-time rule

`close_time` should be retained for completion checks and debugging, but `open_time` remains the canonical identity key.

## Numeric type policy

Implementation should avoid unsafe floating-point assumptions where practical.

Recommended direction:

- parse exchange price/quantity strings carefully,
- use decimal-safe handling for order/risk-facing values,
- allow numeric arrays for research calculations only where precision implications are understood.

The final implementation may distinguish analytical numeric types from execution/risk numeric types.

---

## Partial Candle Handling

## Definition

A partial candle is a kline update for a candle that has not yet closed.

## Allowed uses of partial candles

Partial candles may be used for:

- stream liveness detection,
- operator display clearly labeled as forming,
- debugging,
- latency measurement,
- and detecting whether the market-data stream is active.

## Forbidden uses of partial candles

Partial candles must not be used for:

- strategy signal confirmation,
- 15m breakout trigger evaluation,
- 1h trend-bias calculation,
- ATR/EMA calculations used for live decisions,
- stop-management decisions based on completed-bar rules,
- backtest/live parity reports as if final,
- or persistence as final canonical bars.

## Rule

A partial candle may exist in memory as a provisional object, but it must not be published to the strategy engine as a completed bar.

---

## Completed-Bar Publication Policy

## Core rule

The market-data layer must publish a completed-bar event only when the bar is confirmed closed.

## Required event

When a completed 15m bar is confirmed, the live data layer should emit an internal event such as:

```text
market_data.completed_bar_available
```

Minimum event payload:

- `symbol`
- `interval`
- `bar_open_time_utc_ms`
- `bar_close_time_utc_ms`
- `bar`
- `source_stream`
- `event_time_utc_ms`
- `processed_at_utc_ms`
- `sequence_reference` where available
- `is_recovery_backfill` yes/no

## Strategy evaluation trigger

For v1, the normal live strategy trigger should be:

1. BTCUSDT 15m completed bar is published.
2. Live data layer identifies the latest completed 1h bar available at that decision time.
3. Runtime safety gates confirm entries may be evaluated.
4. Strategy engine receives a command to evaluate the completed bar.

The strategy engine should receive both:

- the completed 15m bar reference,
- and the latest valid completed 1h context reference.

## Duplicate completed-bar events

If duplicate closed-bar updates arrive for the same canonical bar key:

- do not trigger strategy evaluation twice,
- detect the duplicate,
- compare payloads where practical,
- log or emit a diagnostic event if fields differ materially,
- keep deterministic handling.

## Late completed-bar events

If a completed bar arrives late:

- record the processing delay,
- evaluate whether the delay exceeded freshness thresholds,
- and avoid executing if the runtime no longer trusts signal timing.

The exact late-bar execution policy may be stage-specific.

For v1 live operation, if a 15m signal bar is materially delayed, the safer default is to block the entry and require review rather than enter late under uncertain execution assumptions.

---

## Higher-Timeframe Alignment Rules

## Rule 1 — 1h bias must be completed

The 1h bias must be calculated only from completed 1h bars.

## Rule 2 — 1h context must be available at the 15m decision time

At the time the 15m completed bar is evaluated, the corresponding 1h context must be the latest completed 1h bar whose completion time is not after the 15m bar decision time.

## Rule 3 — no forming 1h bar

The currently forming 1h bar must not be used for EMA, ATR, bias, or trend-slope calculations.

## Rule 4 — missing 1h context blocks entries

If valid 1h context is missing, stale, ambiguous, or misaligned:

- block new entries,
- emit a market-data or strategy-input warning,
- and do not evaluate a live entry signal.

## Example

If the bot receives the completed 15m bar ending at 10:15 UTC, the 1h bias should use the latest fully completed 1h bar available at that time.

The 10:00–11:00 UTC 1h candle is forming and must not be used.

---

## Market-Data Freshness Model

The live data layer must maintain explicit health state for required market-data inputs.

## Required freshness states

Recommended states:

- `HEALTHY`
- `DEGRADED`
- `STALE`
- `UNAVAILABLE`
- `RECOVERING`

## Meaning of each

### `HEALTHY`

Required market-data streams are connected, recent, and producing expected updates.

Strategy evaluation may proceed if all other runtime gates permit it.

### `DEGRADED`

Market data is delayed, intermittent, or otherwise weaker than normal, but not yet fully stale.

New entries may be blocked depending on severity and runtime policy.

### `STALE`

Required data has not updated within the expected tolerance, or the runtime no longer trusts bar completion timing.

New entries must be blocked.

### `UNAVAILABLE`

The required market-data path is disconnected or unusable.

New entries must be blocked.

### `RECOVERING`

The market-data layer is reconnecting, backfilling, or revalidating continuity after interruption.

New entries must remain blocked until recovery confirms state.

---

## Freshness Dimensions

The live data layer should track freshness separately for each required stream or data category.

Minimum dimensions:

- BTCUSDT 15m kline freshness
- BTCUSDT 1h kline freshness or derived 1h freshness
- BTCUSDT mark-price freshness
- REST backfill availability where relevant

## Required tracked fields

For each stream:

- `stream_name`
- `symbol`
- `interval` where applicable
- `last_event_time_utc_ms`
- `last_processed_at_utc_ms`
- `last_completed_bar_open_time_utc_ms` where applicable
- `last_completed_bar_close_time_utc_ms` where applicable
- `last_successful_reconnect_at_utc_ms` if relevant
- `current_health_state`
- `stale_reason` if relevant

## Suggested initial freshness policy

Exact thresholds should be configurable and tested.

A reasonable v1 policy direction:

- mark-price stream is degraded if no update arrives within several expected update intervals,
- kline stream is degraded if update cadence is materially abnormal,
- kline stream is stale if a completed bar is expected but not observed within a configured grace period,
- any missing completed 15m bar near a decision point blocks new entries,
- any missing valid 1h context blocks new entries.

This document does not lock exact numerical thresholds.

Exact thresholds should be set during implementation and validated in paper/shadow testing.

---

## Stream Recovery Policy

## Recovery triggers

Market-data recovery is required when:

- stream disconnects,
- stream becomes stale,
- expected completed bar is missing,
- duplicate or conflicting bar data appears,
- a gap is detected in completed bars,
- reconnect occurs after an interruption,
- or the runtime cannot prove continuity.

## Recovery sequence

Recommended recovery sequence:

1. Mark affected market-data health as `RECOVERING`.
2. Block new entries.
3. Reconnect or restore stream.
4. Fetch recent closed bars through REST.
5. Compare REST-recovered bars with locally held completed bars.
6. Detect missing, duplicate, or conflicting bars.
7. Repair local completed-bar cache if deterministic.
8. Emit recovery result event.
9. Mark data healthy only after continuity is restored.
10. Resume strategy evaluation only if all other runtime gates permit it.

## Recovery backfill rule

Backfilled completed bars may be stored or used to repair the live bar cache.

However, the system must not blindly generate live entries from old missed bars after recovery.

If a signal would have occurred during a stale/disconnected period, the safer v1 policy is:

- record the missed signal opportunity if detectable,
- do not enter late by default,
- require explicit future policy before delayed signal execution.

---

## REST Backfill Policy

REST backfill is allowed for startup and recovery.

## Startup bootstrap

At startup, the live data layer should fetch enough recent completed bars to initialize:

- ATR calculations,
- EMA calculations,
- setup-window calculations,
- higher-timeframe bias,
- and immediate context validation.

The required number of bars should be derived from the strategy’s longest lookback plus a safety buffer.

For v1, this means enough data to support:

- 15m ATR(20),
- 15m setup-window logic,
- 1h EMA(50),
- 1h EMA(200),
- 1h EMA slope comparison,
- and any live initialization checks.

Because EMA(200) requires substantial historical context, startup should not assume that a tiny recent window is sufficient for production-quality bias.

## Recovery backfill

After a disconnect or stale condition, REST should fetch the recent closed-bar range needed to prove continuity.

## Backfill event labeling

Backfilled bars should be labeled distinctly from stream-origin bars.

Suggested field:

- `is_recovery_backfill`

## Backfill and strategy evaluation

Backfill can restore state.

Backfill should not automatically trigger live entry execution for stale historical decision points.

---

## Live Bar Cache Policy

The runtime should maintain a recent in-memory completed-bar cache.

## Purpose

The cache supports:

- strategy calculations,
- indicator updates,
- higher-timeframe alignment,
- gap detection,
- recovery comparison,
- and operator/status summaries.

## Scope

For v1, the live cache should be small and symbol-scoped.

Minimum cache:

- recent BTCUSDT 15m completed bars
- recent BTCUSDT 1h completed bars or derived 1h bars
- recent mark-price updates if needed for status

## Persistence

The completed-bar cache itself does not necessarily need durable persistence in v1 if it can be safely reloaded from REST on startup.

However, recovery events, data-staleness incidents, and runtime state transitions should be recorded through observability and persistence paths as defined elsewhere.

## Cache invalidation

If continuity cannot be proven after recovery:

- invalidate the affected cache,
- reload from REST,
- block strategy evaluation until enough trusted context exists.

---

## Mark-Price Handling

## Purpose of mark price in live data

Mark price is required for:

- operator visibility into reference price,
- monitoring protective-stop context,
- potential stop-related diagnostics,
- and future mark-price sensitivity analysis.

## Boundary rule

Mark-price updates do not confirm protective stop existence or execution.

Stop existence and lifecycle must come from exchange order/algo state and user-stream/reconciliation logic.

## Strategy usage

For v1, the primary strategy signal logic uses standard futures trade-price klines, not mark-price klines.

Mark price should not be substituted into signal calculations unless a separate approved strategy variant is created.

## Stop behavior context

Because the live protective stop uses mark-price triggering, the runtime should display or log mark-price context around stop updates and stop-related incidents where practical.

---

## Data Quality and Gap Handling

## Missing completed bars

If a completed bar is missing:

- block new entries,
- mark the affected stream/data context as degraded or stale,
- attempt REST recovery,
- log the gap,
- and do not silently fabricate or forward-fill the bar.

## Duplicate bars

If duplicate completed bars arrive:

- deduplicate by canonical key,
- avoid double strategy evaluation,
- log duplicates if they are unexpected,
- and compare values where practical.

## Conflicting bar values

If two sources disagree for the same completed bar:

- do not silently choose one without logging,
- prefer official REST recovery for reconciliation where appropriate,
- emit a data-quality warning,
- and block strategy evaluation if the conflict affects live decision context.

## Out-of-order updates

Out-of-order partial updates may occur in networked systems.

The live data layer must ensure that completed-bar publication remains ordered by canonical bar time.

## Invalid values

Bars with invalid values should be rejected or quarantined.

Examples:

- missing open/high/low/close,
- impossible high/low relationships,
- non-positive price values,
- missing canonical timestamps,
- interval mismatch,
- symbol mismatch.

---

## Live Data Event Contracts

The live data layer should communicate through the internal event contract, not ad hoc calls.

## Event family

Live data events belong to the market-data event family.

## Recommended events

### `market_data.stream_connected`

Emitted when a market-data stream connection is established.

Minimum payload:

- `stream_name`
- `symbol`
- `interval` where applicable
- `connected_at_utc_ms`

### `market_data.stream_disconnected`

Emitted when a stream disconnects.

Minimum payload:

- `stream_name`
- `symbol`
- `interval` where applicable
- `disconnected_at_utc_ms`
- `reason` if known

### `market_data.freshness_degraded`

Emitted when a stream becomes delayed or suspicious.

Minimum payload:

- `stream_name`
- `symbol`
- `interval` where applicable
- `last_event_time_utc_ms`
- `last_processed_at_utc_ms`
- `reason`

### `market_data.marked_stale`

Emitted when a stream is stale enough to block normal strategy activity.

Minimum payload:

- `stream_name`
- `symbol`
- `interval` where applicable
- `stale_since_utc_ms`
- `reason`
- `entries_blocked` yes/no

### `market_data.restored`

Emitted when stream/data continuity is restored.

Minimum payload:

- `stream_name`
- `symbol`
- `interval` where applicable
- `restored_at_utc_ms`
- `recovery_method`

### `market_data.completed_bar_available`

Emitted when a completed bar is ready for strategy evaluation.

Minimum payload:

- `symbol`
- `interval`
- `bar_open_time_utc_ms`
- `bar_close_time_utc_ms`
- `source`
- `is_recovery_backfill`
- `processed_at_utc_ms`

### `market_data.gap_detected`

Emitted when completed-bar continuity is broken.

Minimum payload:

- `symbol`
- `interval`
- `expected_open_time_utc_ms`
- `observed_open_time_utc_ms`
- `gap_start_utc_ms`
- `gap_end_utc_ms`
- `entries_blocked` yes/no

### `market_data.backfill_started`

Emitted when REST recovery begins.

Minimum payload:

- `symbol`
- `interval`
- `from_utc_ms`
- `to_utc_ms`
- `reason`

### `market_data.backfill_completed`

Emitted when REST recovery completes.

Minimum payload:

- `symbol`
- `interval`
- `from_utc_ms`
- `to_utc_ms`
- `bars_loaded`
- `continuity_restored` yes/no

---

## Strategy Evaluation Interaction

The market-data layer should not call exchange execution directly.

Recommended interaction:

```text
market-data stream
  -> market_data.completed_bar_available event
  -> runtime/scheduler creates strategy.evaluate_completed_bar command
  -> strategy engine evaluates completed-bar context
  -> risk layer evaluates candidate if signal exists
  -> execution layer receives approved command only after risk and runtime gates pass
```

## Strategy input requirements

A live strategy evaluation command should include:

- completed 15m bar reference,
- latest valid completed 1h bar reference or derived context,
- symbol,
- strategy id,
- runtime entries-allowed flag,
- market-data health state,
- and correlation ID.

## No direct execution

The live data layer must not:

- submit orders,
- size trades,
- confirm positions,
- modify stops,
- or clear incidents.

---

## Entry Blocking Rules from Market Data

The live data layer or safety layer must block new entries when:

- BTCUSDT 15m completed bar stream is stale,
- valid completed 1h context is unavailable,
- required market-data recovery is in progress,
- completed-bar continuity is broken,
- data conflict affects decision context,
- live bar timing is materially delayed,
- or market-data health is `STALE` or `UNAVAILABLE`.

## Position management under market-data failure

If a position is already open and protected, market-data failure should not automatically imply flattening.

However:

- new entries must be blocked,
- strategy-managed stop updates may be blocked or degraded depending on required data,
- exchange-side protective stop must remain the fail-safe,
- operator visibility must show degraded management capability,
- incident classification should follow incident-response policy.

If trade management depends on completed bars and those bars are unavailable, the runtime should enter a cautious state and rely on confirmed exchange-side protection while recovery proceeds.

---

## Market Data Versus User Stream Boundary

## Market data owns

- public price stream intake,
- kline updates,
- completed-bar publication,
- mark-price updates,
- market-data freshness,
- market-data recovery/backfill,
- gap detection.

## User stream owns

- order update intake,
- account update intake,
- position update intake,
- algo/protective stop lifecycle updates,
- private stream health,
- user-stream keepalive and reconnect behavior.

## Reconciliation owns

- comparing local state with exchange position/order/protection truth,
- classifying clean/recoverable/unsafe mismatches,
- deciding whether state is trustworthy after interruption.

## Important rule

A healthy market-data stream does not imply healthy execution state.

A healthy user stream does not imply valid strategy input.

Both health dimensions must be visible separately.

---

## Observability Requirements

The runtime must expose market-data health clearly.

## Required operator-visible fields

At minimum, operator status should show:

- market-data health state,
- BTCUSDT 15m stream health,
- BTCUSDT 1h stream or 1h context health,
- mark-price stream health,
- last completed 15m bar time,
- last completed 1h bar time,
- last market-data event time,
- last market-data processing time,
- current recovery/backfill status,
- whether market-data state is blocking entries.

## Required structured logs/events

The runtime should record:

- stream connect/disconnect,
- stale/degraded transitions,
- completed-bar publication,
- bar gaps,
- duplicate or conflicting bars,
- backfill start/end,
- recovery success/failure,
- entry blocking due to market data.

## Alerting expectations

Alerts should be generated for:

- stale 15m strategy stream,
- missing completed signal bar,
- missing 1h context,
- repeated market-data reconnects,
- backfill failure,
- data conflict in decision context,
- and market-data degradation while a position exists.

Alert severity should follow incident-response policy.

---

## Startup Behavior

At startup, the market-data layer must not immediately mark itself healthy.

Recommended sequence:

1. Runtime starts in safe mode.
2. Load configuration.
3. Initialize observability.
4. Connect required market-data streams.
5. Fetch recent REST bars for required intervals.
6. Build live completed-bar cache.
7. Validate enough context exists for indicators.
8. Confirm 15m and 1h alignment.
9. Mark market-data health according to evidence.
10. Allow strategy evaluation only after restart/reconciliation and all runtime gates permit it.

## Startup insufficient context

If insufficient historical/live context exists to calculate required indicators:

- block entries,
- show clear reason,
- fetch additional bars if safe,
- and do not evaluate live signals until context is sufficient.

---

## Shutdown Behavior

On controlled shutdown, the market-data layer should:

- record stream shutdown events,
- close connections cleanly where possible,
- avoid emitting false stale alerts after intentional shutdown,
- preserve last health summary where useful for restart diagnostics.

On unclean shutdown, restart procedure and market-data recovery must re-establish continuity before normal operation resumes.

---

## Implementation Constraints

## Required module boundary

The live data implementation should live under the market-data module defined by the codebase structure.

Expected direction:

```text
src/prometheus/market_data/
```

Potential submodules:

```text
src/prometheus/market_data/
  models.py
  live_streams.py
  bar_cache.py
  bar_completion.py
  freshness.py
  backfill.py
  alignment.py
```

Exchange-specific WebSocket clients should live under the exchange adapter boundary, not inside strategy logic.

Expected direction:

```text
src/prometheus/exchange/binance_usdm/
```

## Strategy boundary

The strategy layer may consume completed-bar events or completed-bar contexts.

It must not own WebSocket connections.

## Risk boundary

The risk layer may consume validated market context for sizing and approvals.

It must not own live stream state.

## Execution boundary

The execution layer may use mark-price context for diagnostics where approved.

It must not rely on public market data as proof of order or stop state.

---

## Testing Requirements

Live data implementation must include tests for the following.

## Completed-bar tests

- partial kline update is not published to strategy,
- closed kline update is published once,
- duplicate closed update does not trigger duplicate evaluation,
- out-of-order updates do not break completed-bar ordering.

## Higher-timeframe alignment tests

- 15m decision uses only completed 1h context,
- forming 1h bar is ignored,
- missing 1h context blocks entry evaluation,
- direct 1h stream and derived 1h aggregation behave consistently where applicable.

## Freshness tests

- stale stream blocks entries,
- degraded stream emits correct health state,
- restored stream clears market-data block only after continuity validation,
- repeated reconnects create observable warnings.

## Backfill tests

- startup backfill loads sufficient context,
- gap recovery detects missing bars,
- backfilled historical bars do not automatically trigger late live entries,
- conflicting REST/stream values are surfaced.

## Boundary tests

- strategy does not import Binance stream client,
- market-data module does not place orders,
- user-stream/account truth is not inferred from market data.

---

## V1 Non-Goals

The following are not part of the v1 live data spec:

- order-book based execution optimization,
- tick-level alpha generation,
- high-frequency microstructure trading,
- multi-symbol live orchestration,
- portfolio-level market-data routing,
- alternative data feeds,
- machine-learning feature streams,
- cross-exchange data aggregation,
- autonomous signal switching,
- live discretionary charting terminal,
- storing every partial kline update as a permanent dataset.

These may be researched later, but they are not part of the first live-capable implementation.

---

## Open Questions

The following should be resolved during implementation or paper/shadow testing.

## 1. Exact freshness thresholds

The policy requires stale/degraded detection, but exact thresholds should be tuned during implementation.

## 2. Direct 1h stream versus derived 1h bars

The default recommendation is direct 1h stream for runtime simplicity, with point-in-time tests.

A later decision may switch to internally derived 1h bars if parity with historical research benefits from it.

## 3. Late signal handling threshold

The default policy is to avoid entering late after stale or delayed signal delivery.

A precise cutoff should be defined before paper/shadow execution.

## 4. Mark-price display and alert thresholds

Mark-price monitoring is required for context, but exact dashboard alert thresholds should be refined alongside interface docs.

## 5. Persistent storage of live bars

The v1 runtime may not need durable storage for every live bar if REST can reload context.

This should be revisited when database design is finalized.

---

## Acceptance Criteria

This live data specification is satisfied when the implementation can demonstrate:

- partial candles are not used for strategy decisions,
- completed 15m bars are published deterministically,
- 1h bias context is completed and point-in-time valid,
- market-data stale/degraded states are tracked,
- stale required market data blocks new entries,
- REST backfill can restore recent context after reconnect,
- backfilled missed bars do not create automatic late entries,
- market-data health is visible to the operator,
- market-data events are logged and traceable,
- and market data remains separate from account/execution truth.

---

## Document Status

- Status: ACTIVE
- Created: 2026-04-17
- Owner: Project operator
- Role: Live market-data implementation specification
