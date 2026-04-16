# V1 Breakout Validation Checklist

## Purpose

This document defines the formal validation checklist for the v1 breakout strategy.

Its purpose is to determine whether the strategy has earned the right to move from one stage of the project to the next.

This checklist is not meant to answer only whether the strategy is profitable in a backtest. It is meant to answer whether the strategy is:

- based on trustworthy data,
- implemented according to specification,
- simulated honestly,
- robust under realistic assumptions,
- and operationally prepared for the next stage of deployment.

## Scope

This checklist governs promotion through the following stages:

1. research candidate
2. validated backtest candidate
3. paper / shadow candidate
4. tiny live candidate

This document applies specifically to the v1 breakout strategy on Binance USDⓈ-M futures.

It does **not** replace detailed backtest reports, execution runbooks, or live deployment procedures. It is a gate document.

## Background

The current v1 strategy direction is:

- Binance USDⓈ-M futures
- BTCUSDT as primary symbol
- ETHUSDT as secondary comparison symbol
- 15m signal timeframe
- 1h higher-timeframe bias
- breakout continuation with trend filter
- bar-close signal confirmation
- next-bar-open baseline backtest fill model
- structural stop with ATR buffer
- staged stop reduction and trailing exit logic

Because multiple parameters and variants will be tested, the project must treat overfitting and unrealistic simulation as default dangers, not edge cases.

This checklist exists to enforce discipline.

## Promotion Stages

## Stage 1 — Research Candidate

A strategy variant may be called a research candidate when:

- its rules are fully specified,
- its data inputs are defined,
- and a first honest backtest can be run.

This stage is for exploration, not promotion.

## Stage 2 — Validated Backtest Candidate

A strategy variant may be called a validated backtest candidate only when it has passed:

- data-integrity checks,
- specification-conformity checks,
- realistic simulation checks,
- and robustness checks.

This stage is still not enough for live trading.

## Stage 3 — Paper / Shadow Candidate

A strategy variant may be considered for paper or shadow deployment only when it has passed:

- validated backtest review,
- execution-readiness checks,
- and operational-preparedness checks.

## Stage 4 — Tiny Live Candidate

A strategy variant may be considered for tiny live deployment only when it has passed:

- paper / shadow review,
- stream and reconciliation checks,
- stop-placement verification,
- and controlled-operations review.

---

# Validation Gates

## Gate 1 — Data Integrity

### Required checks

- [ ] Historical data source is explicitly documented
- [ ] Binance USDⓈ-M official endpoints were used as canonical source
- [ ] BTCUSDT 15m dataset is complete for the tested periods or invalid windows are explicitly flagged
- [ ] ETHUSDT 15m dataset is complete for the tested periods or invalid windows are explicitly flagged
- [ ] Higher-timeframe 1h bars are aligned correctly with the 15m signal data
- [ ] Mark-price data is stored separately from standard futures klines
- [ ] Funding-rate data is present for all periods relevant to held positions
- [ ] Exchange metadata snapshots are available
- [ ] Leverage bracket snapshots are available
- [ ] Commission-rate assumptions are explicit and documented
- [ ] No missing price bars were silently forward-filled
- [ ] No malformed bars remain unresolved in tested windows
- [ ] Timestamps are stored and interpreted in UTC
- [ ] Canonical timestamps are based on open time where appropriate
- [ ] All invalid data windows are logged explicitly

### Gate outcome
- [ ] Pass
- [ ] Fail
- Notes:

---

## Gate 2 — Strategy Specification Conformity

### Required checks

- [ ] Implemented strategy matches the written v1 breakout strategy specification
- [ ] Higher-timeframe bias logic matches the documented rules
- [ ] Setup-window logic matches the documented rules
- [ ] Breakout trigger uses completed bars only
- [ ] Entry timing matches the documented method
- [ ] Structural stop logic matches the documented method
- [ ] Exit logic matches the documented staged management model
- [ ] Re-entry rules match the documented policy
- [ ] No same-bar look-ahead logic is present
- [ ] No hidden discretionary filters were added outside the written spec
- [ ] All tested variants are documented explicitly

### Gate outcome
- [ ] Pass
- [ ] Fail
- Notes:

---

## Gate 3 — Simulation Realism

### Required checks

- [ ] Signal is generated only after the breakout bar has fully closed
- [ ] Baseline fill model uses next-bar open after signal close
- [ ] Entry fees are included
- [ ] Exit fees are included
- [ ] Funding is included in net result calculations
- [ ] Slippage is included in all reported primary results
- [ ] Stop execution is modeled conservatively
- [ ] Spread or execution-friction allowance is accounted for where relevant
- [ ] Position sizing is based on stop distance and account risk, not assumed leverage targets
- [ ] Leverage caps are respected in simulation
- [ ] Symbol rule constraints are respected in simulation
- [ ] No unrealistic fill-at-signal-close assumption is used in the baseline result
- [ ] Mark-price sensitivity for stop behavior is reviewed separately or explicitly deferred with justification

### Gate outcome
- [ ] Pass
- [ ] Fail
- Notes:

---

## Gate 4 — Validation Methodology

### Required checks

- [ ] Development, walk-forward, and final holdout periods are clearly separated
- [ ] No random shuffling was used in time-series validation
- [ ] Walk-forward results are recorded per fold
- [ ] Holdout period remained untouched during parameter development
- [ ] In-sample and out-of-sample results are clearly distinguished
- [ ] Parameter exploration was documented
- [ ] Number of tested variants was recorded
- [ ] No result was selected solely because it had the highest return
- [ ] Stable parameter regions were preferred over sharp peaks
- [ ] Cost sensitivity was tested across multiple slippage assumptions

### Gate outcome
- [ ] Pass
- [ ] Fail
- Notes:

---

## Gate 5 — Robustness

### Required checks

- [ ] Strategy remains viable across walk-forward folds
- [ ] Strategy does not collapse under modest parameter variation
- [ ] Setup-window alternatives were compared
- [ ] Breakout-buffer alternatives were compared
- [ ] Stop-buffer alternatives were compared
- [ ] Trend-filter alternatives were compared
- [ ] Results remain acceptable under conservative fee and slippage assumptions
- [ ] BTCUSDT results are not entirely dependent on one isolated subperiod
- [ ] ETHUSDT comparison was performed
- [ ] Long-side results make structural sense
- [ ] Short-side results make structural sense
- [ ] The strategy does not rely on one extremely narrow winning parameter set
- [ ] Poor-regime behavior is understood and documented

### Gate outcome
- [ ] Pass
- [ ] Fail
- Notes:

---

## Gate 6 — Exit Model Comparison

### Required checks

- [ ] Fixed 2R exit baseline was tested
- [ ] Fixed 3R exit baseline was tested
- [ ] Staged stop-reduction + trailing exit was tested
- [ ] Opposite-signal-only exit was tested
- [ ] Exit-model comparisons use the same cost assumptions
- [ ] Exit-model comparisons use the same validation windows
- [ ] The selected exit logic is justified by robustness, not just headline return
- [ ] Break-even transition behavior was specifically reviewed
- [ ] Trailing-stop behavior was specifically reviewed
- [ ] Stagnation-exit behavior was specifically reviewed

### Gate outcome
- [ ] Pass
- [ ] Fail
- Notes:

---

## Gate 7 — Risk Profile Review

### Required checks

- [ ] Max drawdown is reviewed
- [ ] Worst losing streak is reviewed
- [ ] Return / drawdown is reviewed
- [ ] Expectancy is reviewed
- [ ] Profit factor is reviewed
- [ ] Trade count is sufficient to make the results meaningful
- [ ] Long vs short performance is reviewed separately
- [ ] Cost sensitivity is reviewed
- [ ] Monthly or regime consistency is reviewed
- [ ] The likely pain profile of the system is documented
- [ ] Risk-per-trade assumptions used in the analysis are documented clearly
- [ ] Increased-risk scenarios were treated as sensitivity analysis, not automatic deployment approval

### Gate outcome
- [ ] Pass
- [ ] Fail
- Notes:

---

## Gate 8 — Required Research Artifacts

A strategy variant cannot be promoted without a minimum research artifact package.

### Required artifacts

- [ ] Strategy specification document exists
- [ ] Backtest plan document exists
- [ ] Historical data specification exists
- [ ] Parameter sweep summary exists
- [ ] Walk-forward summary exists
- [ ] Holdout summary exists
- [ ] Cost-sensitivity summary exists
- [ ] Exit-comparison summary exists
- [ ] BTC vs ETH comparison exists
- [ ] Long vs short split report exists
- [ ] Known weaknesses list exists
- [ ] Promotion recommendation note exists

### Gate outcome
- [ ] Pass
- [ ] Fail
- Notes:

---

## Gate 9 — Paper / Shadow Readiness

### Required checks

- [ ] Candidate parameters are explicitly frozen for the paper / shadow test
- [ ] No active parameter tuning is still happening during promotion
- [ ] Test-order workflow has been reviewed
- [ ] Exchange-side stop placement path is understood
- [ ] User data stream handling requirements are documented
- [ ] Reconciliation expectations are documented
- [ ] Order lifecycle assumptions are documented
- [ ] Operational monitoring requirements are documented
- [ ] Known strategy failure modes are documented
- [ ] Operator supervision assumptions are documented

### Gate outcome
- [ ] Pass
- [ ] Fail
- Notes:

---

## Gate 10 — Tiny Live Readiness

### Required checks

- [ ] Paper / shadow behavior was reviewed before live promotion
- [ ] No unresolved position-state mismatches remain
- [ ] Exchange-side protective stop placement has been verified end-to-end
- [ ] Restart and recovery behavior has been tested
- [ ] Websocket reconnect behavior has been tested
- [ ] User data stream keepalive behavior has been tested
- [ ] Manual kill-switch procedure exists
- [ ] Daily-loss lockout behavior is defined
- [ ] Drawdown pause behavior is defined
- [ ] Rollback path is defined
- [ ] Initial live risk is explicitly set to a conservative deployment level
- [ ] Operator review approved tiny live progression

### Gate outcome
- [ ] Pass
- [ ] Fail
- Notes:

---

# Approval Outcomes

## Pass
The candidate may proceed to the next stage.

## Pass with Restrictions
The candidate may proceed, but only under explicitly documented limits.

Examples:
- reduced symbol scope
- reduced risk
- paper only, not shadow
- shadow only, not live
- extra monitoring requirements

## Revise and Retest
The candidate is promising but not yet ready.

It must be revised and rerun through the relevant failed gates.

## Reject
The candidate should not proceed.

This does not necessarily mean the whole strategy family is invalid. It means this specific implementation or parameterization has not earned promotion.

---

# Sign-Off Section

## Candidate Identification

- Strategy variant name:
- Primary symbol:
- Secondary comparison symbol:
- Signal timeframe:
- Higher timeframe:
- Exit model:
- Validation date:
- Reviewer:

## Gate Summary

- Gate 1 — Data Integrity:
- Gate 2 — Strategy Specification Conformity:
- Gate 3 — Simulation Realism:
- Gate 4 — Validation Methodology:
- Gate 5 — Robustness:
- Gate 6 — Exit Model Comparison:
- Gate 7 — Risk Profile Review:
- Gate 8 — Required Research Artifacts:
- Gate 9 — Paper / Shadow Readiness:
- Gate 10 — Tiny Live Readiness:

## Final Outcome

- [ ] Pass
- [ ] Pass with Restrictions
- [ ] Revise and Retest
- [ ] Reject

### Restrictions / Conditions
- 

### Reviewer Notes
- 

---

# Decisions

The following decisions are accepted for the v1 breakout validation checklist:

- validation is gate-based
- promotion requires passing explicit stage-appropriate checks
- chronological validation is mandatory
- overfitting controls are mandatory
- cost realism is mandatory
- exit-model benchmarking is mandatory
- execution-readiness checks are mandatory before paper / shadow progression
- operational-readiness checks are mandatory before tiny live progression

## Open Questions

The following remain open and will be answered by actual research and testing outcomes:

1. Which exact parameter combination is most robust?
2. Which exit model deserves promotion after direct comparison?
3. How strong must ETHUSDT confirmation be before treating the strategy as cross-symbol robust?
4. What exact drawdown and losing-streak profile is acceptable for promotion?
5. What evidence threshold justifies moving from paper / shadow to tiny live?

## Next Steps

After this document, the next recommended files are:

1. `docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md`
2. `docs/04-data/timestamp-policy.md`
3. `docs/04-data/dataset-versioning.md`

## References

Validation references:

- scikit-learn TimeSeriesSplit  
  https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html

- Bailey et al., The Probability of Backtest Overfitting  
  https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf

Binance execution references:

- Binance USDⓈ-M Futures New Order Test  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/New-Order-Test

- Binance USDⓈ-M Futures User Data Streams  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams