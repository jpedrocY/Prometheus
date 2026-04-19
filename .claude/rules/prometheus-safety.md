# Prometheus Safety Rules

## Exchange Truth and Runtime State

- Exchange state is authoritative.
- Commands are not facts.
- REST acknowledgements are not final truth.
- User-stream and reconciliation paths confirm private state.
- A filled entry is not yet a protected trade.
- A submitted stop is not yet confirmed protection.
- Unknown execution outcomes fail closed.

## Protective Stop Rules

- Every live position must have confirmed exchange-side protection.
- Protective stop: STOP_MARKET.
- Required stop settings: closePosition=true, workingType=MARK_PRICE, priceProtect=TRUE.
- Stop updates use cancel-and-replace.
- Stop uncertainty blocks normal operation.
- A position without confirmed protective stop coverage is an emergency.
- Stop widening is forbidden in v1.

## Risk Rules

- Initial live risk: 0.25% of sizing equity.
- Initial effective leverage cap: 2x.
- Internal notional cap is mandatory before live.
- Leverage is a tool, not a target.
- Missing risk state, metadata, or exchange-state confidence fails closed.

## Kill Switch / Recovery

- Restart always begins in SAFE_MODE.
- Reconciliation is required before normal resumption.
- Kill switch persists across restart.
- Kill switch never auto-clears.
- Manual or non-bot exposure blocks new bot entries.
- No blind retry for exposure-changing actions.

## Forbidden in V1

- Production exchange-write capability before approved gates.
- Real production Binance keys during early coding.
- Arbitrary manual buy/sell.
- Click-to-trade.
- Manual pyramiding.
- Manual reversal.
- Manual stop widening.
- Casual risk/leverage sliders.
- Bypassing reconciliation, incidents, approvals, or kill switch.
