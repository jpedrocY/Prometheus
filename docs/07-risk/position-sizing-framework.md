# Position Sizing Framework

## Purpose

This document defines the position-sizing framework for the v1 Prometheus trading system.

Its purpose is to translate strategy risk intent into a valid, exchange-compliant, stage-aware position size.

The sizing framework exists to ensure that:

- position size is derived from account risk and stop distance,
- leverage is treated as a tool rather than a target,
- exchange constraints are respected before any order is submitted,
- small-account and tiny-live constraints are handled conservatively,
- risk expansion is gated and deliberate,
- and sizing decisions are observable, testable, and explainable.

This document replaces the previous TBD placeholder for:

```text
docs/07-risk/position-sizing-framework.md
```

## Scope

This document applies to the v1 Prometheus system under the following assumptions:

- venue: Binance USDⓈ-M futures
- first live symbol: BTCUSDT perpetual
- first research comparison symbol: ETHUSDT perpetual
- v1 live symbol scope: BTCUSDT only
- strategy family: breakout continuation with higher-timeframe trend filter
- signal timeframe: 15m
- higher-timeframe bias: 1h
- live entry method: market order after completed-bar signal confirmation
- stop model: structural stop plus ATR buffer
- runtime position mode: one-way mode
- margin mode: isolated margin
- live concurrency: one position maximum
- deployment model: supervised staged rollout

This document covers:

- sizing inputs,
- sizing formula,
- risk budget calculation,
- risk-usage buffer,
- stop-distance validation,
- leverage caps,
- exchange-symbol constraints,
- leverage-bracket constraints,
- internal notional caps,
- rounding behavior,
- rejection behavior,
- stage-specific risk levels,
- future risk expansion pathway,
- approval/rejection output models,
- testing requirements,
- and implementation boundaries.

This document does **not** define:

- the strategy entry signal itself,
- structural stop formula details beyond sizing usage,
- daily loss lockout rules,
- drawdown lockout rules,
- kill-switch mechanics,
- exchange order formatting,
- full liquidation formula implementation,
- paper/live runbook procedure,
- or final production parameter increases.

Those are covered by related documents.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/03-strategy-research/v1-breakout-strategy-spec.md`
- `docs/03-strategy-research/v1-breakout-backtest-plan.md`
- `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`
- `docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md`
- `docs/06-execution-exchange/exchange-adapter-design.md`
- `docs/07-risk/exposure-limits.md`
- `docs/07-risk/stop-loss-policy.md`
- `docs/07-risk/daily-loss-rules.md`
- `docs/07-risk/drawdown-controls.md`
- `docs/07-risk/kill-switches.md`
- `docs/08-architecture/implementation-blueprint.md`
- `docs/08-architecture/state-model.md`
- `docs/08-architecture/internal-event-contracts.md`
- `docs/10-security/permission-scoping.md`

### Authority hierarchy

If this document conflicts with the v1 strategy specification on initial stop logic, the strategy specification wins.

If this document conflicts with exchange-order handling rules, the execution/exchange documents win.

If this document conflicts with runtime safety state, the state model and incident documents win.

If this document conflicts with security/permission rules, the security documents win.

---

## Core Sizing Principles

## 1. Size from risk, not leverage

Position size must be calculated from:

- sizing equity,
- configured risk fraction,
- proposed entry price,
- initial stop price,
- symbol constraints,
- leverage constraints,
- bracket constraints,
- and internal caps.

The bot must not begin with a desired leverage multiple and size backward from it.

## 2. Leverage is a tool, not a target

Leverage may be used to express a valid position size if the risk model approves it.

Leverage is not a goal and should not be increased for activity, excitement, or capital efficiency alone.

If higher leverage is needed to reach the desired risk size, that means the position notional is larger, which also increases fee exposure and can increase operational sensitivity.

## 3. Initial live risk is intentionally conservative

The initial live risk per trade is:

```text
0.25% of sizing equity
```

This is the starting live risk only.

The project may later work toward higher risk such as:

```text
0.50%
0.75%
1.00%
```

but only through explicit review and promotion gates.

## 4. Future risk expansion is allowed but not automatic

The framework should support a future path toward 1% live risk per trade.

It should not assume 1% is approved for initial live deployment.

Risk expansion requires:

- validated backtest evidence,
- successful paper/shadow operation,
- tiny-live operational stability,
- acceptable drawdown behavior,
- no serious protection failures,
- no unresolved execution-state issues,
- and explicit operator approval.

## 5. Higher leverage may be researched later

The initial live effective leverage cap is:

```text
2x
```

Future values such as:

```text
5x
10x
```

may be researched and eventually considered, but only after the system demonstrates stable execution, stop protection, reconciliation, incident handling, and cost robustness.

A larger leverage cap should never be introduced just because it is technically available at the exchange.

## 6. Risk limits must fail closed

If the system cannot validate sizing safely, it must reject the trade.

Examples:

- missing equity reference,
- missing stop price,
- missing symbol metadata,
- missing leverage bracket,
- invalid account mode,
- invalid margin mode,
- stale runtime state,
- active kill switch,
- unresolved incident,
- existing open position.

## 7. Conservative rounding is mandatory

Quantity must be rounded down to a valid exchange step.

The system must not round to nearest if that could increase risk beyond the approved limit.

## 8. Do not scale up to meet minimum quantity

If the calculated quantity is below Binance minimum tradable size after rounding, reject the trade.

Do not increase the position size just to meet exchange minimums.

---

## Definitions

## Sizing equity

The equity amount used by the bot to calculate risk.

Recommended formula:

```text
sizing_equity_usdt = min(account_equity_usdt, strategy_allocated_equity_usdt)
```

## Account equity

The current account-level equity reference available from the exchange/account state.

Implementation should define the exact source carefully and keep it auditable.

## Strategy allocated equity

The maximum amount of account equity allocated to the Prometheus strategy.

This prevents the bot from sizing against the entire futures account if only a portion of the account is intended for the bot.

## Risk fraction

The configured fraction of sizing equity allowed to be risked on a trade.

Example:

```text
0.0025 = 0.25%
0.0100 = 1.00%
```

## Risk amount

The nominal allowed risk in USDT.

```text
risk_amount_usdt = sizing_equity_usdt * risk_fraction
```

## Risk usage fraction

The fraction of the nominal risk amount used for pure stop-distance sizing.

Initial v1 default:

```text
risk_usage_fraction = 0.90
```

This leaves room for fees and slippage.

## Effective stop-risk budget

The stop-distance risk budget after applying the risk-usage buffer.

```text
effective_stop_risk_budget_usdt = risk_amount_usdt * risk_usage_fraction
```

## Stop distance

The distance between proposed entry price and initial stop price.

For a long:

```text
stop_distance = proposed_entry_price - initial_stop_price
```

For a short:

```text
stop_distance = initial_stop_price - proposed_entry_price
```

## Raw stop-risk quantity

The theoretical quantity implied by the effective stop-risk budget.

```text
raw_stop_risk_quantity = effective_stop_risk_budget_usdt / stop_distance
```

## Effective leverage

The position notional divided by sizing equity.

```text
effective_leverage = position_notional_usdt / sizing_equity_usdt
```

## Position notional

For a linear USDT-settled BTCUSDT contract, approximate notional is:

```text
position_notional_usdt = quantity * proposed_entry_price
```

Implementation must verify symbol/contract semantics through exchange metadata.

---

## Stage-Specific Risk Policy

The sizing framework must support stage-specific risk.

## Research / Simulation

Purpose:

- sensitivity analysis,
- understanding strategy behavior,
- comparing risk levels,
- identifying drawdown profile.

Allowed analysis risk levels may include:

```text
0.25%
0.50%
1.00%
1.50%
2.00%
```

These are for analysis, not automatic live approval.

## Paper / Shadow

Purpose:

- validate live behavior without capital risk.

Recommended risk setting:

```text
0.25% simulated risk
```

Additional simulated risk levels may be tested, but should be clearly labeled as simulation.

## Tiny Live

Purpose:

- first real-capital validation.

Starting policy:

```text
risk_fraction = 0.0025
max_effective_leverage = 2.0
risk_usage_fraction = 0.90
max_concurrent_positions = 1
```

The tiny-live configuration should also include a very explicit internal notional cap.

## Early Scaled Live

Potential future policy only after review:

```text
risk_fraction = 0.0050
max_effective_leverage may remain 2.0 unless justified
```

This stage requires a stronger evidence base than tiny live.

## Mature Live

Potential future policy only after stronger validation:

```text
risk_fraction up to 0.0100
```

Reaching 1% live risk requires explicit operator approval and documented evidence.

Risk above 1% per trade should require a much higher burden of proof and is not a v1 default.

---

## Future Risk Expansion Path

The framework should allow the project to work toward 1% live risk over time.

However, risk expansion must be gated.

## Required promotion evidence

Before increasing live risk from 0.25%, the project should review:

- paper/shadow lifecycle correctness,
- tiny-live execution correctness,
- stop placement and stop update reliability,
- no unresolved position/protection mismatches,
- no severe incidents involving exposure,
- slippage and fee behavior,
- realized drawdown versus expected drawdown,
- losing streak behavior,
- operator review notes,
- daily/weekly review patterns,
- strategy performance by long/short side,
- BTCUSDT versus ETHUSDT validation context,
- and cost sensitivity.

## Suggested progression

Recommended progression:

```text
0.25% -> 0.50% -> 0.75% -> 1.00%
```

Each increase should require a review checkpoint.

The system should not jump from 0.25% to 1.00% solely because early results look good.

## Risk expansion lock

Any configured live risk increase should be captured as:

- config version change,
- release note,
- operator approval,
- updated risk review,
- and staged rollout decision.

---

## Future Leverage Expansion Path

Initial live max effective leverage is:

```text
2x
```

Future values such as:

```text
5x
10x
```

may be evaluated, but the framework must treat higher leverage as a risk-gated capability.

## Why higher leverage is not automatically bad

Higher leverage can allow a valid stop-risk position size with less margin tied up.

It can also support a strategy where the stop distance is tight relative to price and the risk model requires a larger notional.

## Why higher leverage is dangerous

Higher leverage may increase:

- liquidation proximity,
- fee sensitivity,
- slippage sensitivity,
- operational urgency,
- psychological pressure,
- and consequence of exchange/API failure.

## Required conditions before increasing leverage cap

Before increasing max effective leverage above 2x, the project should require:

- stable tiny-live operation,
- successful stop placement and replacement history,
- reconciliation reliability,
- conservative liquidation-distance checks,
- cost sensitivity review,
- operator approval,
- and explicit config/release documentation.

## Suggested leverage progression

If eventually justified:

```text
2x -> 3x -> 5x -> 10x
```

Do not jump directly to 10x without intermediate review.

## Leverage and fees

The sizing framework should recognize that reaching a desired risk size through a larger position notional creates larger entry/exit fees.

This is one reason leverage expansion must be tied to cost modeling and notional caps.

---

## Risk Usage Buffer Policy

## Initial v1 policy

Initial live sizing uses a risk-usage buffer:

```text
risk_usage_fraction = 0.90
```

This means only 90% of the configured risk amount is used for stop-distance loss.

Example:

```text
sizing_equity_usdt = 1,000
risk_fraction = 0.0025
risk_amount_usdt = 2.50
risk_usage_fraction = 0.90
effective_stop_risk_budget_usdt = 2.25
```

The remaining approximate budget is reserved for fees, slippage, and execution friction.

## Why this is selected for initial live

This is conservative and simple.

It reduces the chance that a nominal 0.25% risk trade becomes materially larger after fees and slippage.

## Future policy option

The project may later choose to size using the full configured risk amount:

```text
risk_usage_fraction = 1.00
```

and treat slippage/fees as additional cost.

This future change is allowed, but it should be reviewed explicitly because it changes realized loss expectations.

## Requirement for changing risk usage

Changing `risk_usage_fraction` requires:

- config version change,
- risk review,
- backtest/paper comparison,
- operator approval,
- and release note.

It must not be changed silently.

---

## Sizing Pipeline Overview

The sizing calculation should be implemented as a gated pipeline.

Recommended order:

```text
1. Runtime gate checks
2. Account/equity input checks
3. Strategy input checks
4. Stop-distance checks
5. Risk amount calculation
6. Raw stop-risk quantity calculation
7. Leverage cap calculation
8. Exchange bracket cap calculation
9. Internal notional cap calculation
10. Candidate quantity min() selection
11. Exchange step-size rounding down
12. Minimum/maximum tradability checks
13. Actual risk recomputation
14. Liquidation-safety check
15. Approval or rejection output
```

The risk layer should return a structured result at the first hard failure.

---

## Runtime Gate Checks

Before sizing, the risk layer must verify that runtime state permits entry evaluation.

Reject if any of the following are true:

- runtime is in safe mode,
- runtime is recovering,
- runtime is blocked awaiting operator,
- kill switch is active,
- operator pause is active,
- entries are blocked,
- incident state blocks entries,
- reconciliation state is not acceptable,
- market data is stale or unavailable,
- user stream state is unsafe where private state matters,
- an open position already exists,
- an entry order is already in flight,
- a protective stop state is uncertain,
- v1 symbol scope is violated.

## Existing position rule

For v1 live:

```text
if open_position_exists:
    reject new entry
```

No pyramiding, scaling in, or multi-position behavior is allowed in v1.

---

## Account and Equity Checks

## Required inputs

Sizing requires:

- account equity reference,
- strategy allocated equity,
- risk fraction,
- environment/stage,
- account mode confirmation where available,
- margin mode confirmation where available,
- symbol metadata.

## Sizing equity formula

Recommended:

```text
sizing_equity_usdt = min(account_equity_usdt, strategy_allocated_equity_usdt)
```

## Equity unavailable

If sizing equity cannot be determined safely:

```text
reject trade
```

Do not size from stale, missing, or guessed equity.

## Strategy allocation missing

If `strategy_allocated_equity_usdt` is not configured for live operation:

```text
reject live trade
```

This prevents the bot from accidentally sizing from the full futures account.

## Available balance note

Available balance may be used as an additional feasibility check, but it should not replace the strategy allocation boundary.

---

## Strategy Input Checks

Sizing requires a validated strategy candidate.

Required candidate fields:

- symbol,
- side,
- proposed entry reference,
- proposed entry price or executable price assumption,
- initial stop price,
- ATR reference,
- signal timestamp,
- strategy version,
- config version,
- completed-bar references.

Reject if:

- symbol is not BTCUSDT in v1 live,
- side is invalid,
- proposed entry price is missing,
- stop price is missing,
- ATR reference is missing,
- signal is not from completed-bar logic,
- strategy version is unknown,
- config version is unknown.

---

## Stop-Distance Checks

## Long stop distance

```text
stop_distance = proposed_entry_price - initial_stop_price
```

Reject if:

```text
stop_distance <= 0
```

## Short stop distance

```text
stop_distance = initial_stop_price - proposed_entry_price
```

Reject if:

```text
stop_distance <= 0
```

## ATR stop-distance filter

The v1 strategy uses a stop-distance filter:

```text
0.60 * ATR <= stop_distance <= 1.80 * ATR
```

Reject if:

```text
stop_distance < 0.60 * ATR
```

Reject if:

```text
stop_distance > 1.80 * ATR
```

## Why this matters

A stop that is too tight may be noise-sensitive or invalid after exchange rounding.

A stop that is too wide may produce an unattractive position size or weak reward/risk profile.

---

## Risk Amount Calculation

## Nominal risk amount

```text
risk_amount_usdt = sizing_equity_usdt * risk_fraction
```

## Effective stop-risk budget

```text
effective_stop_risk_budget_usdt = risk_amount_usdt * risk_usage_fraction
```

## Required validation

Reject if:

- risk fraction <= 0,
- risk amount <= 0,
- risk usage fraction <= 0,
- risk usage fraction > 1.0 unless explicitly approved by future policy,
- effective stop-risk budget <= 0.

---

## Raw Quantity Calculation

```text
raw_stop_risk_quantity = effective_stop_risk_budget_usdt / stop_distance
```

Reject if:

- raw quantity <= 0,
- raw quantity is not finite,
- stop distance is invalid,
- or risk budget is invalid.

---

## Leverage Cap Calculation

## Max notional by leverage

```text
max_notional_by_leverage = sizing_equity_usdt * max_effective_leverage
```

## Max quantity by leverage

```text
max_quantity_by_leverage = max_notional_by_leverage / proposed_entry_price
```

## Initial live policy

```text
max_effective_leverage = 2.0
```

## Future policy

Future configurations may test:

```text
3x
5x
10x
```

but only after explicit review.

## If leverage cap binds

If the leverage cap reduces position size below raw stop-risk size, this is acceptable if the final rounded quantity remains tradable.

The actual risk will be lower than target.

The result must record:

```text
sizing_limited_by = max_effective_leverage
```

## If leverage cap makes trade too small

If the leverage-capped quantity rounds below minimum tradable quantity:

```text
reject trade
```

Do not increase leverage or position size automatically.

---

## Exchange Symbol Constraints

The risk layer must validate candidate quantity against exchange symbol rules before approval.

Required metadata may include:

- quantity precision,
- price precision,
- `LOT_SIZE`,
- `MARKET_LOT_SIZE`,
- minimum quantity,
- maximum quantity,
- step size,
- notional rules where available,
- allowed order types,
- trigger price constraints where relevant.

Because v1 entry orders are market orders, `MARKET_LOT_SIZE` must be considered where present.

## Metadata unavailable

If required metadata is unavailable:

```text
reject live trade
```

## Metadata stale

If metadata age exceeds allowed configuration:

```text
reject live trade or require metadata refresh
```

## Minimum quantity rule

After rounding down, if:

```text
final_quantity < minQty
```

then:

```text
reject trade
```

Do not scale up to meet `minQty`.

## Step size rule

Quantity must align to exchange step size.

Recommended:

```text
final_quantity = floor_to_step(candidate_quantity, stepSize)
```

---

## Leverage Bracket Constraints

The sizing framework must validate notional against Binance leverage/notional bracket information where required.

Required checks:

- candidate notional fits within allowed bracket,
- effective leverage does not exceed project cap,
- exchange max leverage constraints are not violated,
- maintenance/bracket context is available for liquidation-safety checks where possible.

## Bracket unavailable

If bracket data is required but unavailable:

```text
reject live trade
```

## Bracket changes

If bracket data changes materially:

- log the change,
- refresh risk metadata,
- review sizing behavior if live configuration depends on it.

---

## Internal Hard Notional Cap

The project should enforce a configurable internal maximum notional.

```text
max_notional_internal_usdt
```

This cap should be independent of what the exchange technically allows.

## Why internal cap exists

The exchange may allow more exposure than the project should take.

Internal caps provide an additional capital-preservation boundary.

## Environment-specific caps

The cap should be environment-specific.

Suggested direction:

| Environment | Cap policy |
|---|---|
| Development | No live trading; fake/simulated cap only |
| Validation | Configurable research cap |
| Paper/shadow | Simulated cap matching test scenario |
| Tiny live | Very small explicit hard cap |
| Early scaled live | Increased only after review |
| Mature live | Increased only through release/risk process |

## Cap unavailable

If live environment has no internal notional cap configured:

```text
reject live trade
```

---

## Candidate Quantity Selection

The preliminary candidate quantity should be:

```text
candidate_quantity = min(
    raw_stop_risk_quantity,
    max_quantity_by_leverage,
    max_quantity_by_bracket,
    max_quantity_by_internal_notional_cap,
    max_quantity_by_exchange_symbol_rules
)
```

The system must track which constraint bound the result.

Possible values:

```text
RAW_STOP_RISK
MAX_EFFECTIVE_LEVERAGE
LEVERAGE_BRACKET
INTERNAL_NOTIONAL_CAP
EXCHANGE_MAX_QTY
EXCHANGE_MARKET_LOT_SIZE
```

If multiple constraints bind, record the most restrictive or record all binding constraints.

---

## Quantity Rounding Policy

## Direction

Always round down.

```text
rounded_quantity = floor_to_valid_step(candidate_quantity)
```

## Reason

Rounding to nearest could increase the position size above the approved risk.

## After rounding

Recompute:

```text
rounded_notional = rounded_quantity * proposed_entry_price
actual_stop_risk_usdt = rounded_quantity * stop_distance
actual_stop_risk_fraction = actual_stop_risk_usdt / sizing_equity_usdt
actual_effective_leverage = rounded_notional / sizing_equity_usdt
```

Accept only if:

```text
actual_stop_risk_fraction <= configured_risk_fraction
actual_effective_leverage <= max_effective_leverage
rounded_quantity >= minQty
rounded_quantity <= maxQty
```

---

## Fee and Slippage Awareness

## Initial policy

Initial live sizing uses the risk-usage buffer to leave room for friction.

The sizing output should still estimate fees and slippage where possible.

Recommended fields:

- estimated entry fee,
- estimated stop/exit fee,
- estimated slippage allowance,
- estimated total adverse loss,
- estimated total adverse loss fraction.

## Fee source

Fee assumptions should come from:

- commission-rate metadata where available,
- config fallback where documented,
- or explicit research assumptions.

## Future policy

The project may later choose to use:

```text
risk_usage_fraction = 1.00
```

and count fees/slippage as additional cost outside the nominal stop risk.

That change must be explicit and reviewed.

---

## Funding Awareness

Funding is not normally part of immediate stop-distance sizing.

However, the sizing result should include context that funding affects realized PnL over held positions.

Funding must be modeled in backtests and post-trade analysis.

For very short holdings, funding may be immaterial; for longer trades, it can matter.

The sizing layer should not ignore funding in reports, but it does not need to reduce quantity directly for funding in v1 unless a future policy adds that rule.

---

## Liquidation-Safety Check

The risk layer should include a conservative liquidation-safety gate before live approval.

## Required principle

The expected liquidation price must be meaningfully beyond the initial stop.

For a long:

```text
estimated_liquidation_price < initial_stop_price - liquidation_safety_buffer
```

For a short:

```text
estimated_liquidation_price > initial_stop_price + liquidation_safety_buffer
```

## If liquidation cannot be estimated

If the runtime cannot estimate or verify liquidation safety sufficiently:

```text
reject live trade or require operator review
```

For initial live, rejection is safer.

## Important note

The implementation should avoid pretending that a simplified formula is exact.

Binance maintenance margin, position brackets, margin mode, wallet balance, and account configuration can affect liquidation behavior.

Use exchange/account data where available and keep the check conservative.

---

## Account Mode and Environment Gates

The sizing framework must verify environment assumptions before live approval.

Reject if:

- v1 live symbol is not BTCUSDT,
- account is not in expected one-way mode,
- margin mode is not isolated for the symbol,
- multi-assets mode behavior is unsupported or not validated,
- hedge-mode fields are unexpectedly required,
- live environment is not explicitly enabled,
- production credentials are missing or invalid,
- production IP restriction requirement is not satisfied where applicable.

The risk layer may depend on configuration/state inputs for these checks.

The exchange adapter and configuration layer should provide normalized account/mode facts.

---

## Rejection Categories

The risk layer should return explicit rejection categories.

Recommended categories:

```text
RUNTIME_BLOCKED
SAFE_MODE_ACTIVE
KILL_SWITCH_ACTIVE
OPERATOR_PAUSE_ACTIVE
INCIDENT_BLOCK_ACTIVE
RECONCILIATION_REQUIRED
OPEN_POSITION_EXISTS
ENTRY_ALREADY_IN_FLIGHT
INVALID_SYMBOL
INVALID_SIDE
MISSING_ENTRY_PRICE
MISSING_STOP_PRICE
MISSING_ATR_REFERENCE
INVALID_STOP_DISTANCE
STOP_TOO_TIGHT
STOP_TOO_WIDE
INSUFFICIENT_EQUITY
STRATEGY_ALLOCATION_MISSING
INVALID_RISK_FRACTION
INVALID_RISK_USAGE_FRACTION
RAW_QUANTITY_INVALID
SYMBOL_RULES_UNAVAILABLE
SYMBOL_RULES_STALE
LEVERAGE_BRACKET_UNAVAILABLE
BELOW_MIN_QTY
EXCEEDS_MAX_QTY
EXCEEDS_LEVERAGE_CAP
EXCEEDS_INTERNAL_NOTIONAL_CAP
ACCOUNT_MODE_INVALID
MARGIN_MODE_INVALID
LIQUIDATION_SAFETY_FAILED
FEE_MODEL_UNAVAILABLE
DAILY_LOSS_LOCKOUT
DRAWDOWN_LOCKOUT
UNKNOWN_RISK_ERROR
```

Each rejection should include a human-readable reason.

---

## Approval Output Model

A successful sizing decision should produce a structured approval object.

Recommended fields:

```text
RiskApproval:
  approved: true
  symbol
  side
  strategy_id
  strategy_version
  config_version
  environment
  sizing_stage
  sizing_equity_usdt
  account_equity_usdt
  strategy_allocated_equity_usdt
  configured_risk_fraction
  risk_amount_usdt
  risk_usage_fraction
  effective_stop_risk_budget_usdt
  proposed_entry_price
  initial_stop_price
  stop_distance
  atr_reference
  stop_distance_atr_multiple
  raw_stop_risk_quantity
  max_effective_leverage
  max_quantity_by_leverage
  max_quantity_by_bracket
  max_quantity_by_internal_notional_cap
  max_quantity_by_exchange_rules
  candidate_quantity
  rounded_quantity
  final_quantity
  estimated_notional_usdt
  estimated_effective_leverage
  actual_stop_risk_usdt
  actual_stop_risk_fraction
  estimated_fee_usdt
  estimated_slippage_usdt
  estimated_total_adverse_loss_usdt
  estimated_total_adverse_loss_fraction
  sizing_limited_by
  binding_constraints
  symbol_rule_snapshot_reference
  leverage_bracket_snapshot_reference
  commission_snapshot_reference
  liquidation_safety_status
  calculated_at_utc_ms
```

## Rejection Output Model

A rejected sizing decision should produce a structured rejection object.

Recommended fields:

```text
RiskRejection:
  approved: false
  symbol
  side
  strategy_id
  strategy_version
  config_version
  environment
  rejection_category
  rejection_reason
  failed_gate
  sizing_equity_usdt if available
  proposed_entry_price if available
  initial_stop_price if available
  stop_distance if available
  atr_reference if available
  calculated_at_utc_ms
```

---

## Event Contract Expectations

The risk layer should communicate through internal event/command contracts.

## Input command

Recommended command:

```text
risk.evaluate_entry_candidate
```

Minimum payload:

- symbol,
- side,
- proposed entry reference,
- proposed stop reference,
- account equity reference,
- strategy allocated equity reference,
- strategy version,
- config version,
- runtime gate summary,
- symbol metadata reference,
- leverage bracket reference.

## Approval event

Recommended event:

```text
risk.entry_approved
```

Minimum payload:

- approved quantity,
- approved notional,
- approved risk amount,
- effective leverage,
- stop reference,
- binding constraints,
- risk stage/config version.

## Rejection event

Recommended event:

```text
risk.entry_rejected
```

Minimum payload:

- rejection category,
- rejection reason,
- failed gate,
- strategy/config reference,
- relevant numeric context where safe.

---

## Implementation Boundaries

## Risk layer owns

- risk amount calculation,
- stop-distance validation,
- raw quantity calculation,
- leverage cap enforcement,
- internal notional cap enforcement,
- symbol-rule validation using normalized metadata,
- bracket validation using normalized metadata,
- quantity rounding rule,
- risk approval/rejection output.

## Strategy layer owns

- signal generation,
- initial stop proposal,
- ATR reference,
- setup and breakout logic,
- strategy version.

## Exchange adapter owns

- Binance API interaction,
- metadata fetching,
- order placement endpoints,
- signed requests,
- raw exchange response normalization.

## Execution layer owns

- turning risk-approved commands into exchange order actions,
- deterministic client order ID use,
- protective stop submission,
- stop replacement workflow.

## State/reconciliation owns

- whether a position actually exists,
- whether a stop actually exists,
- whether runtime state is clean/recoverable/unsafe.

## Operator/safety owns

- kill switch,
- pause,
- operator review,
- safe-mode behavior,
- recovery approval.

---

## Examples

## Example 1 — Basic valid tiny-live sizing

Inputs:

```text
sizing_equity_usdt = 1,000
risk_fraction = 0.0025
risk_usage_fraction = 0.90
proposed_entry_price = 50,000
initial_stop_price = 49,500
stop_distance = 500
max_effective_leverage = 2.0
```

Risk calculation:

```text
risk_amount_usdt = 1,000 * 0.0025 = 2.50
effective_stop_risk_budget = 2.50 * 0.90 = 2.25
raw_quantity = 2.25 / 500 = 0.0045 BTC
raw_notional = 0.0045 * 50,000 = 225 USDT
effective_leverage = 225 / 1,000 = 0.225x
```

If exchange step size allows the rounded quantity and minimum notional/quantity rules pass, the trade may be approved.

## Example 2 — Leverage cap binds

Inputs:

```text
sizing_equity_usdt = 1,000
max_effective_leverage = 2.0
proposed_entry_price = 50,000
raw_stop_risk_quantity = 0.08 BTC
```

Leverage cap:

```text
max_notional_by_leverage = 1,000 * 2 = 2,000
max_quantity_by_leverage = 2,000 / 50,000 = 0.04 BTC
```

Final candidate cannot exceed:

```text
0.04 BTC
```

If tradable, approve smaller-than-target risk and record:

```text
sizing_limited_by = MAX_EFFECTIVE_LEVERAGE
```

## Example 3 — Below minimum quantity

If candidate quantity rounds down below exchange minimum:

```text
reject trade
```

Do not scale up to minimum.

## Example 4 — Future 1% risk

A future reviewed configuration may use:

```text
risk_fraction = 0.0100
```

But only after promotion criteria are satisfied.

The formula remains the same; the configuration changes.

---

## Configuration Fields

Recommended sizing configuration fields:

```text
risk_fraction
risk_usage_fraction
max_effective_leverage
max_notional_internal_usdt
strategy_allocated_equity_usdt
allow_live_trading
environment
symbol_allowlist
require_isolated_margin
require_one_way_mode
require_symbol_metadata_fresh
require_leverage_bracket_fresh
require_liquidation_safety_check
max_metadata_age_ms
fee_model_reference
slippage_model_reference
```

## Initial tiny-live example

```yaml
risk_fraction: 0.0025
risk_usage_fraction: 0.90
max_effective_leverage: 2.0
max_notional_internal_usdt: null  # must be explicitly set before live
require_isolated_margin: true
require_one_way_mode: true
require_symbol_metadata_fresh: true
require_leverage_bracket_fresh: true
require_liquidation_safety_check: true
```

The implementation should reject live trading if required live fields are null.

---

## Testing Requirements

The implementation must include tests for the following.

## Formula tests

- risk amount calculation,
- risk usage buffer calculation,
- long stop distance,
- short stop distance,
- raw quantity calculation,
- leverage cap calculation,
- actual risk recomputation.

## Stop-distance tests

- stop distance <= 0 rejects,
- stop too tight rejects,
- stop too wide rejects,
- valid stop distance passes.

## Rounding tests

- quantity rounds down,
- rounding does not exceed risk,
- below min quantity rejects,
- max quantity violation rejects,
- step-size alignment passes.

## Constraint tests

- leverage cap binding reduces size,
- bracket cap binding reduces size,
- internal notional cap binding reduces size,
- missing metadata rejects,
- stale metadata rejects,
- missing bracket rejects.

## Runtime gate tests

- safe mode rejects,
- kill switch rejects,
- operator pause rejects,
- open position rejects,
- reconciliation required rejects,
- stale market data rejects.

## Stage tests

- tiny-live config uses 0.25% risk,
- future 1% config is possible but requires explicit config,
- risk usage fraction change is visible in output,
- higher leverage cap change is visible in output.

## Boundary tests

- risk layer does not place orders,
- strategy layer does not compute exchange-rounded final quantity,
- execution layer receives only approved quantity,
- exchange adapter provides metadata but does not approve risk.

---

## V1 Non-Goals

The v1 position-sizing framework does not include:

- Kelly sizing,
- reinforcement-learning sizing,
- martingale or anti-martingale escalation,
- grid averaging,
- pyramiding,
- multiple simultaneous positions,
- portfolio correlation sizing,
- dynamic leverage targeting,
- volatility targeting across many symbols,
- discretionary manual sizing overrides,
- automatic risk increase after winning streaks,
- automatic risk recovery after drawdown,
- autonomous strategy switching.

These may be researched later, but they are not v1 behavior.

---

## Open Questions

The following should be resolved before paper/shadow or tiny live.

## 1. Exact strategy allocated equity source

The project should define whether this is:

- a static config value,
- a runtime operator setting,
- a database-persisted control value,
- or a value derived from exchange account allocation.

## 2. Exact internal notional caps

Tiny-live and later-stage notional caps must be explicitly set.

## 3. Exact liquidation-safety method

Implementation must decide how liquidation estimate is computed or verified.

## 4. Exact fee/slippage estimator

The initial risk-usage buffer is simple, but the system should later include explicit fee/slippage estimates in sizing output.

## 5. Future 1% approval criteria

This document defines the pathway but not the final statistical threshold required to approve 1% live risk.

That should be handled through phase gates and review docs.

## 6. Future leverage increase criteria

This document allows future 5x/10x consideration but does not approve it.

Approval criteria should be tied to phase gates, execution reliability, and drawdown review.

---

## Acceptance Criteria

This position-sizing framework is satisfied when the implementation can demonstrate:

- sizing is based on account/allocated equity and stop distance,
- initial live risk defaults to 0.25%,
- future 1% risk is supported only through explicit config/review,
- initial live leverage cap defaults to 2x,
- future leverage expansion is possible but gated,
- risk-usage buffer defaults to 90%,
- future full-risk sizing is possible but requires review,
- leverage is treated as a cap/tool, not a target,
- quantity is rounded down,
- below-minimum quantity rejects,
- symbol rules are enforced,
- leverage bracket data is enforced,
- internal notional cap is enforced,
- account/margin/mode mismatches reject,
- actual risk is recomputed after rounding,
- rejection reasons are explicit,
- approvals are structured and auditable,
- and the risk layer cannot place orders.

---

## References

Official Binance references to verify during implementation:

- Binance USDⓈ-M Futures Common Definition  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/common-definition

- Binance USDⓈ-M Futures Exchange Information  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Exchange-Information

- Binance USDⓈ-M Futures Notional and Leverage Brackets  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Notional-and-Leverage-Brackets

- Binance USDⓈ-M Futures Account Information  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Account-Information-V2

Implementation must verify these references at coding time because exchange rules and endpoint details can change.

---

## Document Status

- Status: ACTIVE
- Created: 2026-04-18
- Owner: Project operator
- Role: Risk sizing implementation contract
