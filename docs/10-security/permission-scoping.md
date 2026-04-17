# Permission Scoping

## Purpose

This document defines the permission-scoping model for the v1 Prometheus trading system.

Its purpose is to translate the project’s security principles into practical operational boundaries by defining:

- which environments may hold which credentials,
- which runtime roles require which permissions,
- which actions require trade-capable authority,
- which roles should remain read-only,
- which trust-boundary violations are forbidden,
- and how the system must behave when credential scope is missing, invalid, or broader than allowed.

This document exists because least privilege is not fully implemented by intent alone.

It must also be reflected in:

- environment boundaries,
- runtime role boundaries,
- credential usage rules,
- and explicit action-level permission scope.

## Scope

This document applies to:

- Binance USDⓈ-M futures API credential usage by the bot
- local development
- validation / paper / shadow environments
- production runtime
- operator-facing control surfaces
- research and data tooling where credential scope is relevant

This document covers:

- permission-scoping philosophy,
- environment-based scoping,
- runtime-role scoping,
- action-level permission mapping,
- component trust boundaries,
- single-key versus split-key guidance,
- forbidden combinations,
- and fail-closed enforcement requirements.

This document does **not** define:

- secret-storage product selection,
- full host hardening,
- network topology in depth,
- or enterprise IAM architecture.

## Background

The project already defines several security principles:

- least privilege is mandatory,
- withdrawal permission must remain disabled,
- production keys must use IP restriction,
- environment separation is required,
- secrets must never live in code, git, docs, screenshots, chats, or normal logs,
- and startup must fail closed when credentials are missing or invalid.

The project also already distinguishes operational concerns such as:

- trading runtime,
- research/data workflows,
- operator supervision,
- and deployment/recovery behavior.

What is still needed is a concrete permission-scoping model that says:

- which actor or component may do what,
- with which credential scope,
- in which environment,
- and under which restrictions.

This document provides that bridge.

## Permission-Scoping Philosophy

## Core principle

Every runtime role must have only the minimum permissions required for its function.

## Secondary principle

Logical permission roles should be defined explicitly even if some of them remain physically combined in the first implementation.

This keeps trust boundaries clear while allowing the v1 system to remain operationally simple.

## Practical interpretation

Permission scoping should answer four separate questions:

1. **Which environment is this credential allowed to exist in?**
2. **Which logical role is this credential for?**
3. **Which actions may this role perform?**
4. **Which combinations are explicitly forbidden even if technically possible?**

## Safety principle

Permission scoping is part of capital protection.

A credential that is broader than necessary increases both operational risk and blast radius if the host, code path, or human workflow is compromised.

## Environment-Based Scoping

The project must distinguish permission scope by environment.

## 1. Development Environment

### Purpose
- local coding
- debugging
- experimentation
- low-trust iteration

### Permission requirements
- production trading credentials must not be present
- production secret material must not be copied here for convenience
- if exchange credentials are needed, they should be development/test credentials only
- no live production trade authority is allowed in this environment

### Allowed direction
- public market-data access
- testnet/sandbox credentials if used
- controlled non-production secrets only

## 2. Validation / Research Environment

### Purpose
- backtesting
- dataset generation
- validation analysis
- research experimentation

### Permission requirements
- should normally require no production trade authority
- public market-data access is sufficient for most workflows
- if limited private account reads are ever required for controlled metadata capture, that should be deliberate and narrow, not a default

### Important rule
Research tooling must not casually receive production trade-capable credentials.

## 3. Paper / Shadow Environment

### Purpose
- live behavior validation without real-capital risk
- test-order workflow
- runtime-behavior rehearsal

### Permission requirements
- credentials must be separate from production
- production credentials must not be reused here casually
- if trade authority exists here, it must be scoped to the paper/shadow boundary only
- no withdrawal authority

### Why this matters
Paper/shadow exists to reduce production risk, so it must not share the same trust boundary as production live trading.

## 4. Production Environment

### Purpose
- supervised live trading with real capital

### Permission requirements
- dedicated production credentials only
- no withdrawal authority
- IP restriction mandatory
- only production runtime and explicitly approved operational paths may use production trade-capable credentials
- production credentials must remain inside the production trust boundary

### Important rule
Production credentials must not be copied into development, research, or casual operator tooling.

## Runtime Role Scoping

Permission boundaries should be defined by logical role.

## Role 1 — Trading Runtime Role

### Purpose
This is the live runtime role that executes the supervised trading system.

### Required capabilities
- place strategy-owned orders
- cancel strategy-owned orders
- place and replace protective stops
- read open orders
- read position state
- read fills / trade confirmations
- use private user-stream functionality
- perform reconciliation reads required for safe operation

### Forbidden capabilities
- withdrawals
- unrelated product permissions not required by the bot
- broad non-required account authorities
- use outside the production runtime boundary

### Notes
This is the most sensitive role in the system.

## Role 2 — Monitoring / Operator-View Role

### Purpose
This role supports operator visibility and monitoring.

### Preferred target posture
- read-only where practical
- no trade authority if a narrower split role is feasible

### v1 practical note
In the first implementation, this role may remain logically combined with the live runtime backend rather than becoming a fully separate credential-owning process.

However, it should still be modeled as a distinct logical role so the system can harden later without redesigning trust boundaries.

### Forbidden capabilities
- direct possession of raw secrets in a frontend client
- discretionary trade authority from a pure UI layer
- unnecessary reuse of broader production credentials when a narrower path is available

## Role 3 — Research / Data Role

### Purpose
This role supports market-data ingestion, research, dataset work, and validation workflows.

### Required capabilities
- public market-data access
- access to local research datasets
- no default need for trade authority
- no default need for private production account authority

### Forbidden capabilities
- live production trade authority
- unrestricted access to production secret material
- casual account-level private access unless explicitly justified for a controlled workflow

## Role 4 — Administrative Setup Role

### Purpose
This is a human-managed setup and governance role, not a normal bot runtime role.

### Typical activities
- creating and reviewing API keys
- configuring permission scopes
- setting IP restrictions
- performing secret rotation
- reviewing key inventory metadata
- preparing environment configuration

### Important rule
This role should remain outside the ordinary bot runtime and should not be treated as an always-on application role.

## Role 5 — Release / Deployment Operator Role

### Purpose
This role handles deployment, environment preparation, release progression, and live enablement.

### Typical capabilities
- deploy approved code/config
- verify correct environment selection
- trigger controlled restart/recovery
- validate runtime readiness before live enablement

### Important rule
This role does not imply discretionary permission to bypass security scoping or change production keys casually.

## Action-Permission Matrix

The following matrix defines which logical roles may perform which categories of action.

## Market and Research Actions

### Read public market data
Allowed roles:
- Research / Data
- Trading Runtime
- Monitoring / Operator-View where needed through backend summaries

### Read local research datasets
Allowed roles:
- Research / Data
- Release / Deployment Operator where required operationally
- Trading Runtime only if explicitly needed for shared logic testing, not as a default production dependency

## Live Trading Actions

### Place entry order
Allowed roles:
- Trading Runtime only

### Place protective stop
Allowed roles:
- Trading Runtime only

### Cancel protective stop
Allowed roles:
- Trading Runtime only

### Replace protective stop
Allowed roles:
- Trading Runtime only

### Place emergency flatten order
Allowed roles:
- Trading Runtime under controlled emergency logic
- Operator-facing control path only through the approved backend action path, not from direct frontend-held credentials

## Live State Read Actions

### Read open orders
Allowed roles:
- Trading Runtime
- Monitoring / Operator-View through controlled backend path
- Release / Deployment Operator when needed operationally

### Read position state
Allowed roles:
- Trading Runtime
- Monitoring / Operator-View through controlled backend path
- Release / Deployment Operator when needed operationally

### Read fills / execution history
Allowed roles:
- Trading Runtime
- Monitoring / Operator-View through controlled backend path
- Release / Deployment Operator when needed operationally

### Use private user stream
Allowed roles:
- Trading Runtime only during normal live operation

## Control Actions

### Pause new entries
Allowed roles:
- Operator-facing control path through backend
- Trading Runtime may internally enforce pause state
- Frontend client should not need raw exchange credentials

### Activate kill switch
Allowed roles:
- Operator-facing control path through backend
- Trading Runtime may honor and persist kill-switch state

### Approve recovery resumption
Allowed roles:
- Operator-facing control path through backend

### Trigger controlled restart
Allowed roles:
- Release / Deployment Operator
- Operator-facing control path through approved backend

## Security / Governance Actions

### Create or modify production API keys
Allowed roles:
- Administrative Setup Role only

### Rotate production credentials
Allowed roles:
- Administrative Setup Role only

### Modify IP restriction settings
Allowed roles:
- Administrative Setup Role only

### Access raw production secret material
Allowed roles:
- Administrative Setup Role only
- production runtime at controlled load time
- never routine frontend/operator UI access

## Component Trust Boundaries

Permission scoping should align with the system architecture.

## Strategy Engine

### Rule
The strategy engine should not directly own exchange credentials.

### Reason
It decides what the system wants to do, not how to authenticate trading actions.

## Risk and Sizing Layer

### Rule
The risk layer should not directly own exchange credentials.

### Reason
It determines acceptable risk and sizing, not exchange authority.

## Execution Layer

### Rule
The execution layer is the component that legitimately uses trade-capable exchange authority.

### Reason
It is responsible for turning approved actions into exchange-safe requests.

## State and Reconciliation Layer

### Rule
This layer may require controlled private read capabilities through the runtime boundary, but it should not become a free-form credential sink.

### Reason
It needs exchange truth for recovery and reconciliation, not broader authority than necessary.

## Observability Layer

### Rule
Observability outputs must not contain raw secret material.

### Reason
Operational visibility must not weaken secrets management.

## Operator Dashboard / Frontend Layer

### Rule
The dashboard frontend must not directly hold live production secrets.

### Reason
Manual controls should flow through approved backend control paths, not through raw secret-bearing client logic.

## Research Tooling

### Rule
Research tooling should remain separate from live production trading authority.

### Reason
Research is a lower-trust, higher-flexibility environment and should not share the production trade boundary.

## Single-Key vs Split-Key Guidance

The current project leaves open whether v1 production will use one trading key or a split-key model.

This document should make that choice explicit at the policy level.

## Preferred target posture

Where practical, the long-term preferred direction is:

- separate trade-capable runtime credentials
- from narrower monitoring/read roles

### Benefits
- reduced blast radius
- clearer trust boundaries
- easier future hardening
- less temptation to reuse broader credentials casually

## Acceptable v1 compromise

For the first supervised production implementation, one production trading key may be acceptable if all of the following are true:

- permissions remain least-privilege
- withdrawal remains disabled
- IP restriction is active
- the key remains inside the production runtime trust boundary
- no lower-trust tooling shares it
- the dashboard/frontend does not directly possess it
- research/development environments do not receive it

## Important rule

Even if a single production key is used in v1, the code and architecture should still model logical roles separately.

This preserves a clean path to later credential separation.

## Forbidden Combinations

The following combinations are explicitly forbidden.

## Environment violations

- production trade-capable credential used in development
- production trade-capable credential used in casual research tooling
- production secret copied into paper/shadow environment for convenience
- production secret copied into operator notes, docs, chats, screenshots, or scratch files

## Permission violations

- any bot credential with withdrawal enabled
- production key without IP restriction
- read-only role given trade authority without explicit necessity
- research role given production trade authority
- monitoring-only process using broad trading credentials when a narrower path is available

## Component trust-boundary violations

- dashboard frontend directly holding live exchange secret material
- strategy engine directly owning raw exchange credentials
- observability or log pipeline receiving unredacted secret material
- generic utility scripts reusing the live production trading credential by default

## Operational violations

- startup proceeding despite missing required credentials
- startup proceeding despite clearly wrong permission scope
- silent fallback to broader-than-expected credential behavior
- production runtime using ad hoc credentials not in the approved inventory/rotation process

## Enforcement and Fail-Closed Rules

Permission scoping must be enforced operationally.

## Startup enforcement

At startup, the system must verify:

- required credentials are present
- environment selection is correct
- the intended role matches the credential provided
- authorization succeeds where required
- permission scope is acceptable for that environment and role

If any of these fail, the runtime must:

- fail closed
- remain or enter safe mode
- block new entries
- surface an operator-visible error
- avoid blind retries without diagnosis

## Runtime enforcement

If runtime authorization failures occur, the system must treat them as security-relevant events.

Examples include:

- invalid key errors
- permission errors
- IP restriction failures
- repeated authorization anomalies
- behavior suggesting wrong credential used in wrong environment

These should trigger:

- redacted logging
- operator-visible alerting
- containment if live safety may be affected
- possible incident classification under the security-related incident path

## Frontend enforcement

The operator dashboard or frontend client must interact through controlled backend paths.

It must not:

- hold raw live exchange secrets
- make direct secret-bearing production exchange calls from an untrusted client context
- or silently broaden control authority outside the defined action paths

## Secrets handling alignment

Permission scoping must remain aligned with secrets-management policy.

This means:

- credential scope and secret storage are linked concerns
- secret material must remain inside the intended trust boundary
- and broader permission scope must not be normalized just because a secret is hard to manage cleanly

## Decisions

The following decisions are accepted for permission scoping in v1:

- permission scoping must be explicit by environment, role, action, and component boundary
- production trade-capable credentials must remain outside development and casual research environments
- the trading runtime role is the only role that legitimately requires live trade authority
- the dashboard/frontend must not directly hold live production secrets
- research and data tooling should remain separate from production trading authority
- logical permission roles should be modeled explicitly even if some remain physically combined in v1
- one production trading key may be acceptable initially only under strict least-privilege and trust-boundary discipline
- withdrawal permission is always forbidden
- production keys without IP restriction are forbidden
- startup and runtime must fail closed on invalid or unsafe permission conditions

## Open Questions

The following remain open:

1. Will the first production implementation use one trade-capable key or split trading and read-oriented roles from day one?
2. What exact exchange endpoints and permissions should be mapped into the final runtime credential-validation routine?
3. Should paper/shadow use a completely distinct credential-management path from development, even if both are non-production?
4. What exact masked key-identifier format should be surfaced in logs and dashboard status?
5. Should future monitoring-only services receive truly separate read-only credentials once the architecture grows beyond the modular monolith phase?

## Next Steps

After this document, the next recommended files are:

1. `docs/00-meta/ai-coding-handoff.md`
2. `docs/09-operations/first-run-setup-checklist.md`
3. `docs/09-operations/paper-shadow-runbook.md`
