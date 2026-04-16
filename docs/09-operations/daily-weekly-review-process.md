# Daily and Weekly Review Process

## Purpose

This document defines the routine operational review cadence for the v1 trading system.

Its purpose is to ensure that supervised operation remains disciplined over time by establishing:

- what should be reviewed daily,
- what should be reviewed weekly,
- what must be documented,
- what patterns require escalation,
- and how routine review supports safer operation and continuous improvement.

This document exists because a supervised trading system should not rely only on incident response. It also needs regular review of normal and degraded behavior before problems become normalized.

## Scope

This document applies to the v1 system assumptions:

- Binance USDⓈ-M futures
- BTCUSDT only
- one-way mode
- isolated margin
- one position maximum
- one active protective stop maximum
- supervised operation

This document covers:

- daily operational review
- weekly operational review
- required review artifacts
- escalation thresholds
- and review outputs

This document does **not** define:

- full performance-research workflow
- deep strategy-research iteration
- accounting or tax processes
- or full audit/compliance reporting

## Background

The v1 system is intentionally designed to be:

- tightly scoped,
- safety-first,
- operator-supervised,
- and governed by explicit recovery and incident rules.

The project already defines:

- restart procedure
- incident response
- operator workflow
- API key policy
- secrets management
- validation and execution rules

What remains necessary is the recurring operational review process that ties those documents into ongoing real use.

Without a routine review cadence, it becomes too easy to:

- ignore repeated warnings,
- normalize degraded behavior,
- miss recurring incident patterns,
- or allow small operational drift to become a serious safety issue.

## Review Philosophy

## Core principle

Routine review exists to detect drift early.

It is not only for investigating dramatic failures. It is also for checking whether the system is still behaving in accordance with its documented design.

## Daily vs weekly distinction

### Daily review
Daily review is primarily tactical.

It should answer:
- did the bot behave correctly today,
- were there incidents or warnings,
- is anything unresolved,
- and should the next trading day proceed normally?

### Weekly review
Weekly review is primarily operational and governance-oriented.

It should answer:
- what patterns are emerging,
- are incidents clustering,
- are procedures working,
- are the restrictions still appropriate,
- and do any docs, controls, or workflows need to change?

## Review Artifacts Principle

Every review cycle should leave behind at least a lightweight artifact.

That artifact does not need to be heavy or bureaucratic, but it should be enough to preserve continuity and support future review.

## Daily Review Process

## Daily review objective

The daily review is a short operational check on recent behavior.

It is intended to confirm:

- whether the system behaved correctly,
- whether any incidents occurred,
- whether any intervention was required,
- and whether the system is safe to continue under the current operating assumptions.

## Daily review timing

The daily review should occur:

- after each active trading day,
- or after each meaningful runtime window if the bot was active only part of the day.

For v1, consistency matters more than exact timing.

## Daily review checklist

- [ ] Was the bot active during the review period?
- [ ] Did the bot take any trades?
- [ ] If trades occurred, were entries and exits broadly consistent with expected strategy behavior?
- [ ] Did any incidents occur?
- [ ] Did any warnings occur without becoming incidents?
- [ ] Did any restart or recovery procedure occur?
- [ ] Did any stream-staleness event occur?
- [ ] Did any reconciliation mismatch occur?
- [ ] Did any unexpected open order or unexpected position state appear?
- [ ] Did every live position have confirmed protective stop coverage?
- [ ] Did any stop-placement or stop-update anomaly occur?
- [ ] Did any manual pause, restart, kill-switch, or emergency action occur?
- [ ] Did any credential or authorization anomaly occur?
- [ ] Did logging and monitoring remain intact?
- [ ] Is any issue still unresolved at the end of the review window?
- [ ] Is the system safe to continue into the next supervised run window?

## Daily review notes

The operator should record a brief note covering:

- active or inactive status
- incident summary if any
- manual action summary if any
- unresolved issues
- decision for next run:
  - continue normally
  - continue with caution
  - remain paused
  - require review before resuming

## Daily review output format

A daily review record may be lightweight, but it should contain at minimum:

- review date
- operator name or alias
- bot active yes/no
- trades occurred yes/no
- incidents yes/no
- manual actions yes/no
- unresolved issues yes/no
- next-run decision
- short notes

## Daily decision outcomes

At the end of the daily review, the operator should classify the next step as one of:

### Continue Normally
No meaningful unresolved issue remains.

### Continue with Caution
No blocking issue exists, but operator attention is needed in the next run window.

### Pause Pending Review
The system should not continue until a specific issue is reviewed.

### Escalate
A deeper review, incident follow-up, or control decision is required before continuation.

## Weekly Review Process

## Weekly review objective

The weekly review is a structured operational review intended to detect repeated issues, operational drift, and procedural weaknesses.

It is not meant to be as granular as a daily check. Instead, it focuses on patterns and governance.

## Weekly review timing

The weekly review should occur once per active operational week.

If the system was not active during the week, the weekly review should still record:

- inactive status
- reason for inactivity
- and whether any preparation or maintenance action occurred

## Weekly review checklist

- [ ] How many days was the bot active this week?
- [ ] How many trades were taken this week?
- [ ] How many incidents occurred by severity level?
- [ ] How many warnings occurred that did not escalate?
- [ ] How many restart or recovery procedures were required?
- [ ] How many user-stream stale events occurred?
- [ ] How many market-data stale events occurred?
- [ ] How many reconciliation mismatches occurred?
- [ ] Did any position ever exist without confirmed stop protection?
- [ ] Did any stop-placement or stop-update anomaly occur?
- [ ] Did any unknown execution-status event occur?
- [ ] Did any authorization or credential anomaly occur?
- [ ] Did any manual pause occur?
- [ ] Did the kill switch activate at any point?
- [ ] Did any emergency flattening occur?
- [ ] Did repeated alerts occur in the same class?
- [ ] Did the operator workflow match the documented policy?
- [ ] Did any document, runbook, or threshold appear outdated?
- [ ] Do any controls need refinement before the next week?

## Weekly review notes

The weekly review should summarize:

- operational stability
- incident patterns
- recurring warning patterns
- manual intervention frequency
- whether current operating restrictions remain appropriate
- whether any immediate action items exist

## Weekly review output format

The weekly review should produce a short but structured summary including:

- review week range
- operator/reviewer
- active days count
- trade count
- incident count by severity
- restart count
- stale-stream count
- mismatch count
- manual intervention count
- emergency action count
- key observations
- action items
- recommendation for next week

## Escalation Thresholds

The review process must not normalize abnormal behavior.

The following patterns should trigger deeper review, caution, or pause decisions.

## Immediate escalation triggers

These require strong review and likely immediate escalation:

- any Severity 4 incident
- any open position without confirmed protective stop
- any suspected credential exposure or security incident
- any emergency flattening event
- repeated restart failure
- repeated unresolved reconciliation mismatch
- repeated unknown execution-state events involving exposure

## Weekly-pattern escalation triggers

These may not always require immediate shutdown, but they do require deliberate review:

- repeated Severity 2 incidents of the same class
- multiple Severity 3 incidents in one review period
- repeated stale user-stream conditions
- repeated stale market-data conditions affecting operation
- repeated stop-placement or stop-update anomalies
- repeated manual pauses for the same underlying reason
- repeated operator override due to the same control weakness
- recurring warnings that are starting to look normal
- repeated mismatch between local and exchange state

## Escalation outcomes

When escalation thresholds are met, the result may be:

- continue with tighter supervision
- reduce activity or keep conservative restrictions
- pause new live operation until reviewed
- update docs or thresholds
- update code or alerts before continuing
- require formal incident/postmortem follow-up

## Required Review Records

## Daily record minimum

Every daily review should record at least:

- date
- operator/reviewer
- active or inactive status
- incident presence
- manual action presence
- unresolved issue presence
- next-run decision
- short notes

## Weekly record minimum

Every weekly review should record at least:

- review period
- reviewer
- active days
- trade count
- incident counts by severity
- restart count
- stale-stream count
- mismatch count
- manual intervention count
- emergency action count
- summary observations
- action items
- recommendation for next period

## Relationship to Other Documents

This review process should be used together with:

- incident response
- restart procedure
- operator workflow
- API key policy
- secrets management
- validation checklist

The review process is not a replacement for those documents.

Instead, it acts as the regular supervisory layer that checks whether those policies are working in practice.

## Operational Guidance for V1

Given the v1 design, the operator should pay particular attention to:

- stream health
- reconciliation cleanliness
- protective stop reliability
- unexpected order presence
- restart/recovery frequency
- repeated manual intervention
- and whether the system is drifting away from “simple, controlled, supervised” operation

Because the system is intentionally narrow in v1, repeated abnormalities should be taken seriously rather than dismissed as noise.

## Failure Modes in the Review Process

The review process is intended to guard against these failures:

### 1. No recordkeeping
Problems happen, but no one records them, so the same issues repeat.

### 2. Alert normalization
Warnings happen often enough that they stop being treated as important.

### 3. Reactive-only supervision
The operator responds only to large incidents and misses recurring smaller problems.

### 4. Poor continuity
The next operating period begins without a clear understanding of unresolved issues from the previous one.

### 5. Review drift
The review process exists on paper but stops being performed consistently.

## Decisions

The following decisions are accepted for the daily and weekly review process:

- daily review is required for tactical operational correctness
- weekly review is required for pattern detection and governance
- both daily and weekly reviews must leave lightweight written artifacts
- repeated abnormal patterns must trigger deeper review rather than being normalized
- severe incidents and emergency actions must be visible in both daily and weekly reviews
- the review process is part of supervised operation, not optional administrative overhead
- unresolved issues must influence the next-run decision explicitly

## Open Questions

The following remain open:

1. What exact template format should be standardized for daily reviews?
2. What exact template format should be standardized for weekly reviews?
3. Should the future dashboard generate draft daily/weekly review summaries automatically?
4. What exact threshold of repeated Severity 2 incidents should trigger mandatory pause or escalation?
5. Should daily and weekly review records live inside the repository, outside it, or both?
6. What retention period should apply to review records in v1?

## Next Steps

After this document, the next recommended files are:

1. `docs/11-interface/operator-dashboard-requirements.md`
2. `docs/10-security/permission-scoping.md`
3. `docs/09-operations/release-process.md`

## References

Related internal project documents:

- `docs/09-operations/operator-workflow.md`
- `docs/09-operations/incident-response.md`
- `docs/09-operations/restart-procedure.md`
- `docs/10-security/api-key-policy.md`
- `docs/10-security/secrets-management.md`
- `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`