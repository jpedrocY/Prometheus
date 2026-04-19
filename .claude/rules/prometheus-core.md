# Prometheus Core Rules

## Project Identity

Prometheus v1 is rules-based, safety-first, operator-supervised, Binance USDⓈ-M futures focused, BTCUSDT-only for first live scope, not a self-learning live AI, and not lights-out autonomous.

## Locked V1 Scope

- Venue: Binance USDⓈ-M futures.
- Initial live symbol: BTCUSDT perpetual.
- ETHUSDT is research/comparison only.
- One-way mode.
- Isolated margin.
- One symbol.
- One position maximum.
- One active protective stop maximum.
- No pyramiding.
- No reversal while positioned.
- No hedge-mode behavior.

## Strategy Basics

- Strategy: breakout continuation with higher-timeframe trend filter.
- Signal timeframe: 15m.
- Higher-timeframe bias: 1h.
- Completed bars only.
- Entry: market entry after completed 15m signal confirmation.
- Baseline backtest fill: next-bar open after confirmed signal close.
- Initial stop: structural stop plus ATR buffer.

## Architecture Rules

- Modular monolith for v1.
- Strategy and execution remain separate.
- Strategy must not import Binance clients.
- Risk must not place orders.
- UI/dashboard must not bypass backend safety gates.
- Exchange adapter is the only Binance-specific boundary.
- Research storage and live runtime persistence remain separate.
