# Release Process

## Purpose

This document defines the release and deployment process for the v1 Prometheus trading system.

Its purpose is to ensure that all changes to the system move from development to live trading in a controlled, testable, and safe manner.

The release process exists to protect:

- capital,
- system stability,
- state integrity,
- and operator confidence.

This document defines how code, configuration, and strategy changes are introduced, validated, promoted, and monitored.

It treats deployment as part of the trading system itself.

## Scope

This release process applies to:

- all code changes
- strategy logic changes
- execution logic changes
- risk model changes
- configuration changes
- deployment and runtime setup changes

This document covers:

- environment model
- promotion pipeline
- promotion gates
- release unit definition
- change classification
- deployment discipline
- pre-live checklist
- post-release monitoring
- rollback policy
- release freeze rules
- documentation requirements

This document does **not** cover:

- detailed CI/CD tooling implementation
- infrastructure-as-code specifics
- cloud provider specifics

## Release Philosophy

## Core principle

No direct transition from development to live trading is allowed.

All changes must pass through staged environments with increasing realism and risk exposure.

## Controlled progression

The system must follow this progression:

dev → validation → paper/shadow → tiny live → scaled live

Each stage increases:

- realism
- exposure
- and risk

Each transition requires explicit validation.

## Safety principle

A release is not successful when:

- the code runs

A release is successful when:

- the system behaves safely under real conditions

## Environment Model

The following environments are defined.

## 1. Development

Purpose:
- local development
- debugging
- rapid iteration

Characteristics:
- no real capital
- incomplete data acceptable
- full logging and debug enabled

## 2. Validation (Research)

Purpose:
- backtesting
- walk-forward validation
- dataset-controlled evaluation

Characteristics:
- reproducible datasets
- version-controlled data
- no live exchange interaction

## 3. Paper / Shadow

Purpose:
- validate live behavior without capital risk

Characteristics:
- real market data
- real execution logic
- no real funds (testnet or simulated execution)
- full observability required

## 4. Tiny Live

Purpose:
- first real-capital validation

Characteristics:
- real funds
- minimal exposure
- strict supervision
- full observability
- conservative risk

## 5. Scaled Live

Purpose:
- stable production operation

Characteristics:
- increased capital allocation
- still supervised
- no relaxation of safety rules

## Promotion Pipeline

The promotion pipeline is strictly ordered:

Development → Validation → Paper → Tiny Live → Scaled Live

No stage may be skipped.

## Promotion Gates

Each transition requires explicit approval conditions.

## Dev → Validation

Requirements:

- core logic implemented
- no known logical contradictions
- basic sanity checks pass
- no obvious runtime errors

## Validation → Paper

Requirements:

- backtests completed
- validation checklist satisfied
- no major inconsistencies
- no clear overfitting behavior
- stable across multiple periods

## Paper → Tiny Live

Requirements:

- execution behavior confirmed
- entry/exit lifecycle behaves correctly
- protective stops always placed and confirmed
- no unexplained mismatches
- restart procedure validated
- observability sufficient for supervision

## Tiny Live → Scaled Live

Requirements:

- no critical incidents
- no protection failures
- no unsafe mismatches
- stable performance over defined observation period
- operator confidence established

## Release Unit Definition

Each release must be identifiable and reproducible.

A release should include:

- code version identifier
- strategy version identifier
- dataset version used for validation
- configuration version
- change summary

## Requirement

A release must be traceable.

It must be possible to answer:

- what changed
- why it changed
- what data it was validated on

## Change Classification

Changes must be classified before release.

## Low-Risk Changes

Examples:

- logging improvements
- observability additions
- UI/dashboard updates
- non-critical refactoring

Requirements:

- basic validation
- no strategy-impacting changes

## Medium-Risk Changes

Examples:

- parameter adjustments
- minor strategy logic changes
- execution timing tweaks

Requirements:

- full validation
- paper testing required

## High-Risk Changes

Examples:

- core strategy changes
- risk model changes
- order handling changes
- state model changes
- protection logic changes

Requirements:

- full validation
- extended paper testing
- careful tiny-live rollout

## Deployment Process

Even if manual in v1, deployment must be consistent.

## Requirements

- clearly defined deployment steps
- controlled environment selection
- correct configuration loading
- secure secret handling
- explicit confirmation of environment before activation

## Deployment principle

Deployment must be:

- repeatable
- controlled
- verifiable

## Pre-Live Checklist

Before enabling live trading, the following must be verified.

## Environment

- correct environment selected (not testnet)
- correct symbol (BTCUSDT)
- one-way mode confirmed
- isolated margin confirmed

## Credentials

- API keys valid
- no withdrawal permissions
- IP restrictions active
- correct permissions for trading

## Configuration

- risk parameters correct
- leverage configuration correct
- strategy parameters correct

## System readiness

- observability working
- logs visible
- health indicators correct
- kill switch functional
- pause control functional
- restart procedure tested

## State safety

- no open unintended positions
- no unexpected open orders
- reconciliation clean

## Final confirmation

Operator must explicitly confirm readiness before enabling live trading.

## Post-Release Monitoring

After deployment, the system must be actively monitored.

## Initial monitoring focus

- first entry lifecycle
- stop placement and confirmation
- stream stability
- reconciliation behavior
- incident occurrence

## Monitoring principle

The operator must verify:

- the system behaves as expected under real conditions

## Rollback Policy

Rollback is a safety mechanism.

## Rollback triggers

- unexpected exposure behavior
- missing or uncertain protection
- repeated unsafe mismatches
- execution inconsistency
- unexplained incident spikes
- loss of state certainty

## Rollback actions

Rollback should:

- stop new entries
- activate safe mode if required
- restore previous stable version
- verify exchange state
- confirm protection or flatten exposure

## Critical rule

Rollback is not just reverting code.

It is restoring a safe operational state.

## Incident-Triggered Release Freeze

If a serious issue occurs:

- no new releases should be deployed
- no parameter changes should be made mid-incident
- system must stabilize first

## Freeze principle

Fix the system, understand the issue, then resume changes.

## Release Documentation Requirements

Each release must produce a record.

## Required fields

- release identifier
- date/time
- summary of changes
- change classification
- validation performed
- known risks
- deployment environment
- operator notes

## Documentation principle

Every release must be explainable after the fact.

## Decisions

The following decisions are accepted:

- staged promotion pipeline is mandatory
- no direct development-to-live deployment
- release units must be versioned and traceable
- change classification determines validation depth
- pre-live checklist is required
- rollback must restore safe state, not just code
- incidents trigger release freeze
- releases must be documented

## Open Questions

1. What exact duration should define stability before scaling live exposure?
2. Should automated deployment be introduced in later phases?
3. What tooling should manage versioning and release tracking?
4. Should release approval require a formal checklist confirmation log?

## Next Steps

After this document, the next recommended files are:

1. `docs/10-security/permission-scoping.md`
2. `docs/00-meta/ai-coding-handoff.md`
