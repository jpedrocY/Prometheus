# API Key Policy

## Purpose

This document defines the API key policy for the trading system.

Its purpose is to ensure that API credentials are handled in a way that minimizes account-level risk and supports safe automation.

This policy governs:

- permission scope,
- key role separation,
- storage and handling,
- rotation and revocation,
- environment separation,
- and startup behavior when credentials are missing or invalid.

## Scope

This document applies to:

- Binance USDⓈ-M futures API keys used by the bot,
- local development credentials,
- paper / shadow deployment credentials,
- and future production credentials.

This document does **not** define full host hardening, network architecture, or general secrets-manager implementation details.

## Background

The project is building a production-oriented trading bot for Binance USDⓈ-M futures.

That means API keys are not just configuration values. They are one of the main trust boundaries of the system.

An overly broad or poorly handled key can expose the account to risks such as:

- unauthorized trading,
- unintended transfers,
- operational misuse,
- or severe account damage if the host or secret-handling process is compromised.

Because of this, the bot must follow a least-privilege design.

## Security Principles

## 1. Least privilege

Every API key used by the system must have the narrowest permission scope that still allows the intended function.

### Rule
Do not use a broad “everything enabled” API key if a narrower key can perform the required role.

### Practical meaning
- trading keys should be able to trade, but not withdraw
- monitoring/read keys should not be able to place trades
- unrelated permissions should remain disabled unless explicitly justified

## 2. Role separation

API keys should be separated by operational role wherever practical.

### Recommended role split

#### Trading key
Used for:
- order placement
- order cancellation
- exchange-side trading actions required by the bot

#### Monitoring / account-state key
Used for:
- account-state reads
- position checks
- reconciliation reads
- monitoring flows
- secure non-trading account queries where practical

#### Research / utility key
Optional, later-stage role for:
- controlled read-only research access
- tooling that does not need trade authority

### Why role separation matters
Role separation reduces blast radius.

If one key is exposed, the damage should be limited to that key’s permission scope wherever possible.

## 3. No withdrawal access

### Hard rule
**Withdrawal permission must remain disabled for all bot API keys.**

This applies to:
- local development
- paper / shadow testing
- production deployment

### Rationale
The trading bot has no legitimate operational need to withdraw funds.

Withdrawal capability should therefore remain outside the bot’s trust boundary.

## 4. IP restriction is mandatory for production

### Hard rule
All production bot API keys must use IP restriction.

### Rationale
If a key is exposed but cannot be used from unauthorized IPs, account risk is materially reduced.

### Practical consequence
The final deployment environment must support a stable and trusted outbound IP model before production keys are considered ready.

This may affect later infrastructure choices.

## 5. Fail closed

### Hard rule
If required API credentials are missing, malformed, invalid, or unauthorized for the required action, the bot must fail closed.

### Meaning
The bot must:
- not continue in degraded “maybe it works” mode
- not attempt live trading without validated credentials
- not silently fall back to unsafe assumptions

Instead it must:
- enter safe mode
- block new entries
- raise a visible error

## Permission Policy

## Allowed permission philosophy

The bot should enable only the permissions required to operate the Binance USDⓈ-M futures strategy.

### Required permissions
The exact final set depends on implementation details, but the policy direction is:

- enable only permissions needed for the futures bot workflow
- disable unrelated capabilities by default
- keep all permissions documented explicitly

## Forbidden or discouraged permissions

### Withdrawals
- always disabled

### Unused transfer permissions
- disabled unless a future operational design explicitly requires them

### Unused product permissions
- disabled unless they are required for the actual deployed bot

## Environment Separation

## Core rule

Development, paper/shadow, and production environments must not share the same API keys.

## Required environment separation

### Local development
Use separate credentials from any production deployment.

### Paper / shadow environment
Use distinct credentials where practical and never reuse production keys casually.

### Production
Use dedicated production keys only for the deployed production system.

## Rationale
Environment separation prevents accidental promotion of unsafe habits and reduces the chance that a lower-trust environment compromises a higher-trust key.

## Secret Handling Policy

## Hard rules

### Rule 1
API secrets must never be committed to version control.

### Rule 2
API secrets must never be hardcoded in source files.

### Rule 3
API secrets must never be written into Markdown docs, architecture docs, or runbooks.

### Rule 4
API secrets must never be printed to normal application logs.

### Rule 5
API secrets must be loaded from a controlled secret source.

### Rule 6
Example credentials used in docs or tests must be obviously fake and non-functional.

## Approved handling direction

At a minimum, secrets should be handled through:

- environment variables,
- secured runtime configuration,
- or a dedicated secret-management mechanism later.

The exact tooling may evolve, but the handling rules above are mandatory regardless of implementation method.

## Logging and Observability Rules

## Allowed in logs

Logs may include:
- key role name
- key identifier alias
- environment label
- permission summary
- validation success/failure state

## Forbidden in logs

Logs must not include:
- raw API secret
- full API key if avoidable
- signatures
- full signed payloads containing sensitive material
- raw secret-bearing configuration dumps

## Recommended logging approach

Use:
- aliases
- redaction
- masked identifiers
- and structured error categories

rather than full credential output.

## Key Validation Policy

## Startup validation

At bot startup, required API credentials should be validated for:

- presence
- parseability
- environment suitability
- expected permission scope where practical
- exchange authorization success for required actions

## Runtime validation

The bot should treat these as security-relevant failures:

- invalid key errors
- IP restriction failures
- permission failures
- repeated authorization errors
- signature or timestamp authorization failures

These should not be treated as harmless noise.

## Rotation and Revocation Policy

## Core rule

API keys must be rotatable without changing the security policy.

## Rotation triggers

A key rotation should occur when any of the following happens:

- suspected credential exposure
- accidental secret disclosure
- host compromise suspicion
- operator error involving secret handling
- migration to a new trust boundary
- periodic security review requiring refresh
- role split changes that make old key scope inappropriate

## Immediate revocation triggers

Immediate revocation is required when:

- a key is believed to be leaked
- a key appears in logs, docs, screenshots, or messages
- unauthorized API activity is suspected
- the deployment host is suspected compromised
- IP restriction integrity is compromised
- key purpose is no longer trusted

## Rotation workflow principle

Key rotation should be treated as a normal operational capability, not an emergency-only improvisation.

## Key Inventory Policy

The project should maintain a simple internal inventory of active keys.

### Minimum inventory fields
- key alias
- environment
- operational role
- permission summary
- IP restriction status
- create date
- last rotation date
- owner / responsible operator
- status:
  - active
  - deprecated
  - revoked

### Purpose
This keeps the security posture explicit and avoids “mystery keys” that still exist but are no longer understood.

## WebSocket API Consideration

If authenticated WebSocket API usage is introduced later, the design must account for the rule that a single WebSocket connection is authenticated with one API key by default.

### Practical implication
Connection design should remain compatible with role separation.

This supports the broader policy direction:
- separate keys by role
- separate trust boundaries where practical
- avoid mixing unrelated privileges casually

## Operational Restrictions for V1

For the v1 deployment stage, the following restrictions are required:

- withdrawal permission disabled
- production key IP-restricted
- no sharing of production keys with local experimental tooling
- no embedding credentials in code or docs
- no live startup if key validation fails
- no use of a wider-permission key when a narrower one is sufficient

## Failure Handling Policy

If API-key-related validation fails, the bot must:

1. enter or remain in safe mode
2. block new entries
3. log the security-relevant failure in a redacted form
4. raise an operator-visible alert
5. avoid repeated blind retries without diagnosis
6. require corrected credentials or operator intervention before resuming normal trading

## What Is Explicitly In Scope

This policy covers:

- key permission scope
- role separation
- environment separation
- storage and handling rules
- rotation and revocation principles
- startup and runtime key-failure behavior
- production IP restriction requirements

## What Is Explicitly Out of Scope for Now

This document does **not** yet define:

- full network hardening
- VPN / reverse-proxy architecture
- hardware-backed secret storage
- enterprise secret manager selection
- host OS hardening policy
- team-wide IAM or corporate access control models

These may become relevant later, but they are outside the scope of this phase.

## Decisions

The following decisions are accepted for the API key policy:

- trading-bot API keys must follow least privilege
- withdrawal permission must remain disabled
- production keys must use IP restriction
- keys should be separated by operational role where practical
- secrets must not be stored in code, git, docs, or logs
- local and production keys must be separated
- key rotation and revocation triggers must be documented
- bot startup must fail closed if required API credentials are missing or invalid
- runtime permission and authorization failures are security-relevant events

## Open Questions

The following remain open:

1. Will v1 use a single production trading key or split trading and monitoring keys from the start?
2. What exact secret-loading method will be used on the NUC deployment?
3. What exact IP-restriction/network design will support the final production host?
4. What periodic key-rotation cadence should become the default?
5. Should the project maintain a dedicated key inventory file inside the repo docs, or keep it only outside the repo for security reasons?
6. What exact masked key-identifier format should logs use?

## Next Steps

After this document, the next recommended files are:

1. `docs/09-operations/incident-response.md`
2. `docs/09-operations/operator-workflow.md`
3. `docs/10-security/secrets-management.md`

## References

Binance references:

- Binance USDⓈ-M Futures General Info  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info

- Binance Get API Key Permission  
  https://developers.binance.com/docs/wallet/account/api-key-permission

- Binance USDⓈ-M Futures WebSocket API General Info  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-api-general-info

- Binance USDⓈ-M Futures Error Code  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/error-code