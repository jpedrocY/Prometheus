# Operator Dashboard Requirements

## Purpose

This document defines the requirements for the v1 operator dashboard.

Its purpose is to specify the minimum interface needed to supervise the v1 trading system safely and effectively.

The v1 dashboard exists to support:

- real-time operator supervision,
- visibility into runtime health and state,
- visibility into exposure and protection,
- visibility into incidents and recovery,
- and access to the limited set of manual control actions that supervised operation requires.

This document exists because v1 is a supervised trading system, not a fully autonomous one.

The operator must be able to determine quickly:

- whether the bot is healthy,
- whether it is allowed to trade,
- whether exposure exists,
- whether that exposure is protected,
- whether any incident or recovery is active,
- and whether immediate human action is required.

This document defines interface requirements.

It does **not** define:

- final visual design mockups,
- frontend implementation details,
- specific web framework choices,
- or discretionary trading workflows.

## Scope

This dashboard requirements document applies to the v1 system assumptions:

- Binance USDⓈ-M futures
- BTCUSDT only in first live-capable scope
- one-way mode
- isolated margin
- one active strategy
- one open position maximum
- one active protective stop maximum
- supervised deployment
- restart begins in safe mode
- incident handling is severity-based
- operator review is required in some blocked/emergency situations

This document covers:

- dashboard philosophy,
- primary operator questions,
- required dashboard sections,
- required controls,
- confirmation and guardrail rules,
- visual-priority rules,
- event-history and audit needs,
- and review-support requirements.

This document does **not** cover:

- manual discretionary trade placement,
- multi-symbol portfolio monitoring,
- mobile-native design requirements,
- full reporting/analytics platform features,
- or a rich charting workstation.

## Background

The project already defines:

- supervised operator responsibilities,
- allowed manual actions,
- restart and recovery behavior,
- incident response expectations,
- runtime state model,
- and observability requirements.

Those documents imply the need for an operator-facing control surface, but they do not yet define the minimum interface requirements clearly in one place.

This dashboard should not be treated as a cosmetic extra.

For v1, it is part of the operational safety boundary because the operator must be able to see when the system is:

- healthy,
- paused,
- blocked,
- recovering,
- incident-affected,
- or managing live exposure under uncertainty.

## Dashboard Philosophy and Goals

## Core philosophy

The v1 operator dashboard is a:

- **supervision and control surface**

It is **not** a discretionary trading terminal.

## What this means

The dashboard should help the operator:

- understand the bot’s current condition,
- detect unsafe or uncertain states quickly,
- review what the bot is doing,
- and take the small set of approved manual control actions.

The dashboard should **not** encourage:

- ad hoc manual trading,
- casual strategy overrides,
- UI-driven discretionary behavior,
- or unnecessary micromanagement of normal strategy logic.

## Core goals

The dashboard should optimize for:

- operational clarity
- exposure and protection visibility
- incident visibility
- recovery visibility
- manual-action discipline
- and low ambiguity in critical states

## Non-goals

The dashboard should not optimize first for:

- rich chart analysis
- deep PnL analytics
- broad portfolio control
- beauty over clarity
- or speculative future autonomy features

## Primary Operator Questions

The dashboard must make it easy to answer the following questions immediately.

## 1. Is the bot healthy right now?

The operator must be able to tell whether the runtime is in:

- healthy operation
- safe mode
- recovery
- blocked-awaiting-operator
- or another constrained state

## 2. Is the bot allowed to trade right now?

The operator must be able to see whether:

- entries are currently allowed
- a pause is active
- a kill switch is active
- operator review is required
- or another control condition is blocking activity

## 3. Is there open exposure?

The operator must be able to determine clearly whether:

- a position exists
- what side it is
- and what the current size is

## 4. If exposure exists, is it protected?

The operator must be able to determine whether:

- a protective stop is confirmed
- protection is pending confirmation
- protection is uncertain
- or an emergency unprotected state exists

This is one of the highest-priority questions in the whole interface.

## 5. Is any incident active?

The operator must be able to determine:

- whether an incident exists
- its class
- its severity
- whether it is contained
- and whether escalation is pending

## 6. Is restart, recovery, or reconciliation active?

The operator must be able to determine whether:

- restart is in progress
- recovery is in progress
- reconciliation is required
- reconciliation is in progress
- or a mismatch remains unresolved

## 7. Is operator action required right now?

The operator must be able to determine clearly whether:

- immediate action is required
- review is required before resumption
- or the system can continue safely without intervention

## 8. What was the last important thing the bot did?

The operator must be able to see recent important actions and state changes without digging through raw backend logs.

## Required Dashboard Sections

The v1 dashboard should include the following required sections.

## Section 1 — Top-Level Status Summary

This should be the highest-priority summary area.

### Required fields

- current primary runtime mode
- entries allowed yes/no
- incident active yes/no
- highest active severity
- operator review required yes/no
- kill switch active yes/no
- pause active yes/no
- open position yes/no
- protection confirmed yes/no
- reconciliation state
- action required now yes/no

### Design requirement

This section must make it difficult to overlook dangerous or blocking states.

## Section 2 — Connectivity and Stream Health

This section should expose the health of the inputs and exchange connectivity the bot relies on.

### Required fields

- exchange connectivity health
- market-data health
- user-stream health
- stale / degraded / healthy status
- last user-stream keepalive success where relevant
- last market-data freshness update where relevant
- current reconnect / restoration state if applicable

### Why required

Stale or degraded streams are not minor technical details in this system.

They directly affect whether the bot is allowed to continue normal operation.

## Section 3 — Position and Protection Panel

This section should focus on live exposure and protection state.

### Required fields

- position present yes/no
- side
- size
- average entry price if position exists
- current trade lifecycle state
- current protection state
- protective stop present yes/no
- last protective-stop confirmation time
- current stop-management stage
- current risk stage if applicable

### Design requirement

This section should be visually clearer and more important than generic statistics.

## Section 4 — Reconciliation and Restart Panel

This section should expose recovery and state-certainty information.

### Required fields

- reconciliation state
- last successful reconciliation time
- reconciliation in progress yes/no
- mismatch class if mismatch exists
- restart currently active yes/no
- restart mode if relevant
- last restart time
- last recovery outcome
- emergency branch active yes/no

### Why required

Restart and reconciliation are core safety behaviors in v1, not hidden technical internals.

## Section 5 — Incidents and Alerts Panel

This section should show current operational problems requiring awareness or action.

### Required fields

- active incident count
- highest active severity
- incident class for each active incident
- containment status
- escalation pending yes/no
- operator review required yes/no
- critical alert summary
- warning alert summary

### Design requirement

Active critical items must not be buried beneath informational history.

## Section 6 — Recent Important Events Feed

This section should show a rolling short-form timeline of important recent events.

### Required event categories to show

- runtime mode changes
- entries and exits
- protective stop placement and updates
- stream stale / restored events
- reconciliation start / result
- restart / recovery events
- incident open / resolve events
- operator actions

### Why required

The operator needs recent context, not only static status boxes.

## Section 7 — Manual Controls Panel

This section should expose the allowed operator actions.

### Required controls

- pause new entries
- clear pause
- activate kill switch
- request controlled restart
- approve recovery resumption
- emergency flatten
- disable live operation if such control exists in the v1 runtime

### Important rule

The dashboard should expose only the control actions allowed by policy.

It should not include casual strategy overrides or manual discretionary trade-entry features.

## Required Controls

The v1 dashboard must support the following controls, with clear state-aware behavior.

## Control 1 — Pause New Entries

### Purpose
Allows the operator to stop new exposure without necessarily disrupting current protected trade management.

### Requirements
- available when runtime is active
- action result must be visible immediately
- pause state must remain obvious until cleared

## Control 2 — Clear Pause

### Purpose
Allows the operator to restore normal entry eligibility after a deliberate pause.

### Requirements
- only available when pause is active
- should be blocked or guarded if another higher-priority blocking condition remains active

## Control 3 — Activate Kill Switch

### Purpose
Allows emergency halt of new strategy progression.

### Requirements
- must require explicit confirmation
- resulting kill-switch state must become highly visible immediately
- follow-up manual review expectations must be visible

## Control 4 — Request Controlled Restart

### Purpose
Allows operator-initiated restart/recovery flow under policy.

### Requirements
- must surface that restart will enter safe mode
- should show resulting recovery/reconciliation state clearly
- action should be logged and auditable

## Control 5 — Approve Recovery Resumption

### Purpose
Allows operator approval where policy requires human clearance before normal operation resumes.

### Requirements
- must only be available when recovery approval is actually required
- must require explicit confirmation
- should record the approval action visibly

## Control 6 — Emergency Flatten

### Purpose
Allows manual de-risking when protection or state certainty cannot be trusted.

### Requirements
- must require strong confirmation
- should visually explain that this is an emergency action
- action result must be logged and surfaced clearly

## Control 7 — Disable Live Operation

### Purpose
Allows suspension of live operation when policy or repeated abnormal behavior requires it.

### Requirements
- resulting blocked/disabled state must be obvious
- follow-up action path should be visible

## Confirmation and Guardrail Requirements

The dashboard must prevent casual unsafe actions.

## Required confirmation actions

The following actions must require explicit confirmation:

- activate kill switch
- approve recovery resumption
- emergency flatten
- disable live operation
- any future action that clears a blocked/emergency state

## Reason / note capture

The interface should support recording a short reason or note for:

- kill-switch activation
- recovery approval
- emergency flatten
- disable live operation
- and other major manual interventions where practical

This is valuable for later review and continuity.

## Guardrail rules

The dashboard should not allow or should strongly guard against:

- clearing a kill switch when unresolved blocking conditions remain
- approving recovery while reconciliation state remains unsafe
- presenting a position as protected when protection state is uncertain
- showing “healthy” status while critical blocking conditions remain active
- normalizing severe warnings visually into background noise

## State-aware action availability

Manual controls should be visibly enabled or disabled based on current runtime state.

Examples:

- recovery approval should not be active when no operator review is required
- clear pause should not be active when no pause exists
- emergency flatten should be guarded and clearly marked as high consequence

## Visual Priority and Alert-Display Rules

The dashboard must make dangerous conditions harder to miss than routine information.

## Highest visual priority conditions

The following should receive the strongest visual emphasis:

- open position without confirmed protective stop
- protection state uncertain while exposure exists
- emergency unprotected exposure
- kill switch active
- blocked awaiting operator
- unsafe mismatch
- user stream stale while exposure exists
- incident severity 4
- recovery blocked with exposure risk

## Medium priority conditions

The following should receive visible but lower emphasis:

- recoverable mismatch
- repeated stream reconnects
- degraded market-data health
- repeated warning-class incidents
- operator pause active
- entries blocked while flat

## Lower priority conditions

The following may be shown in lower-emphasis areas:

- informational lifecycle changes
- clean restart completions
- clean stream-restoration notices
- historical informational events

## Display principle

The dashboard must not visually bury the system’s actual risk state under low-value activity indicators or cosmetic information.

## Event History and Audit Requirements

The dashboard should expose recent and meaningful operational history.

## Required event-history capabilities

The operator should be able to review recent history for:

- runtime mode changes
- incident openings and resolutions
- restart and reconciliation activity
- entries, exits, and stop-related events
- manual actions
- stream stale / restore events

## Required auditability characteristics

The interface should preserve visibility into:

- what action happened
- when it happened
- who triggered it where identity is available
- what state changed
- whether follow-up review is required

## Audit principle

Meaningful operator interventions must not disappear into backend-only logs.

## Daily and Weekly Review Support Requirements

The dashboard does not need to be a full reporting system in v1, but it should support the review workflow.

## Daily review support requirements

The dashboard or its backing data should make it easy to answer:

- was the bot active today
- were there trades today
- were live positions protected
- were there incidents today
- were there warnings today
- was restart or reconciliation required today
- were there manual actions today
- are unresolved issues still open

## Weekly review support requirements

The dashboard or its backing data should make it easy to summarize:

- active days
- trade count
- incident counts by severity
- restart count
- stale-stream count
- mismatch count
- manual intervention count
- emergency action count
- repeated warning patterns

## Support principle

The dashboard should support disciplined review, but should not try to become a large reporting platform in v1.

## Explicit Non-Goals for V1

The following are intentionally not required for the first dashboard version:

- manual discretionary trade placement
- manual chart-driven trade entry
- multi-symbol watchlists
- portfolio-level allocation controls
- rich chart-analysis workspace features
- advanced PnL analytics and attribution dashboards
- role-based multi-user administration beyond current need
- mobile-first design requirements
- social/collaborative features
- non-essential visual complexity

## Decisions

The following decisions are accepted for the v1 operator dashboard requirements:

- the dashboard is a supervision and control surface, not a discretionary trading terminal
- the dashboard must make exposure, protection, incident, and recovery state immediately visible
- top-level system status must have the highest interface priority
- stream and connectivity health must be visible because they directly affect safe operation
- position and protection state must be a first-class dashboard concern
- reconciliation and restart state must be visible to the operator
- the dashboard must expose the limited set of approved manual controls and no more
- dangerous actions must require confirmation
- major manual actions should support reason/note capture where practical
- critical risk states must receive stronger visual emphasis than routine information
- the dashboard should support daily and weekly review workflows without becoming a full analytics platform

## Open Questions

The following remain open for later design and implementation:

1. What exact layout will best present the required sections without visual overload?
2. Should the first dashboard show raw event feed and summary cards together, or separate them more strongly?
3. What exact visual treatment should distinguish warning from critical conditions?
4. Should operator reason/note capture be mandatory or optional for each major manual action?
5. Should the first version be browser-based only, or also support lightweight remote/mobile visibility later?
6. What exact historical lookback controls should be included in the event-history view?

## Next Steps

After this document, the next recommended files are:

1. `docs/09-operations/release-process.md`
2. `docs/10-security/permission-scoping.md`
3. `docs/00-meta/ai-coding-handoff.md`
