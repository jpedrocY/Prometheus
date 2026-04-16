# Secrets Management

## Purpose

This document defines the secrets-management policy for the trading system.

Its purpose is to ensure that sensitive values such as:

- API keys,
- API secrets,
- runtime credentials,
- and other authentication material

are stored, loaded, rotated, revoked, and audited in a way that minimizes the risk of accidental disclosure or operational misuse.

This document exists because secure permissions alone are not enough if the secret material itself is handled poorly.

## Scope

This document applies to secrets used by:

- Binance USDⓈ-M futures bot operation
- local development
- paper / shadow environments
- production deployment
- supporting operational tooling where applicable

This document covers:

- where secrets may and may not live
- environment separation
- approved handling patterns
- startup behavior when secrets are missing or invalid
- rotation and revocation rules
- logging and observability redaction rules

This document does **not** define:

- final secret-manager product selection
- full host hardening
- enterprise IAM architecture
- or network architecture details beyond what is needed for secrets policy

## Background

The project uses Binance API credentials to interact with USDⓈ-M futures trading and account-state endpoints.

These credentials are high-value secrets because misuse can lead to:

- unauthorized trading,
- blocked recovery actions,
- operational compromise,
- or broader account-security risk.

Binance explicitly advises users not to share API keys or secret keys and to revoke keys immediately if unusual activity is detected. The exchange also supports scoped permissions for API keys, which makes disciplined secrets handling even more important because multiple role-specific keys may exist over time.

The project is also explicitly separating:

- development,
- paper / shadow,
- and production environments.

That separation must apply to secrets as well.

## Secrets Management Philosophy

## Core principle

Secrets must be treated as controlled runtime inputs, not as ordinary configuration text.

## Security principle

If a secret is exposed, copied casually, logged, committed, or shared outside its intended trust boundary, that must be treated as a real security failure.

## Operational principle

Secrets handling must support safe operation, safe restart, and safe rotation without requiring unsafe improvisation.

## Least exposure principle

The system should expose as little secret material as possible to:

- code,
- operators,
- logs,
- and surrounding tooling.

## Definitions

### Secret
Any value that grants or contributes to authenticated access.

Examples:
- API secret
- API key where sensitivity requires controlled handling
- signed runtime credential material
- secret-bearing environment variable

### Secret metadata
Non-sensitive information about a secret.

Examples:
- key alias
- environment
- operational role
- creation date
- last rotation date
- status

### Trust boundary
The environment or operational context within which a secret is allowed to exist.

Examples:
- local development machine
- paper / shadow deployment
- production host
- secure runtime process

## Hard Rules

## Rule 1 — No secrets in source code

Secrets must never be hardcoded in:

- application source files
- scripts
- notebooks
- test files
- or examples intended for execution

## Rule 2 — No secrets in version control

Secrets must never be committed to:

- git repositories
- tracked config files
- environment files that are versioned
- or any other source-controlled artifact

## Rule 3 — No secrets in docs

Secrets must never be stored in:

- Markdown docs
- runbooks
- architecture notes
- ADRs
- screenshots
- shared text snippets
- or chat messages

## Rule 4 — No secrets in normal logs

Secrets must never appear in:

- application logs
- debug logs
- monitoring output
- exception traces
- request dumps
- or structured telemetry

## Rule 5 — No informal secret sharing

Secrets must never be shared through:

- email
- chat
- screenshots
- copy-paste to collaborators
- or ad hoc note files

## Rule 6 — Startup fails closed

If required secrets are missing, malformed, unauthorized, or invalid for the intended action, the bot must fail closed:

- enter or remain in safe mode
- block new entries
- raise a visible error
- require correction before normal live operation resumes

## Environment Separation Policy

## Core rule

Development, paper / shadow, and production environments must not share the same secrets.

## Required separation

### Development secrets
Used only for:
- local development
- experimentation
- non-production testing

### Paper / shadow secrets
Used only for:
- controlled dry-run or non-production supervision environments

### Production secrets
Used only for:
- the approved production deployment trust boundary

## Additional rule

Production secrets must not be copied into development environments for convenience.

## Rationale

Environment separation reduces blast radius and prevents low-trust workflows from compromising production credentials.

## Allowed Secret Storage Patterns

## Approved direction

Secrets must be loaded from a controlled runtime source.

For the current project phase, acceptable patterns may include:

- environment variables injected at runtime
- secured runtime configuration outside version control
- later, a dedicated secret-management system

## Important note

The exact implementation tooling may evolve.

This document locks the **policy**, not the final product choice.

## Required properties of any approved storage method

Any approved secret source must support, at minimum:

- restricted access
- separation by environment
- controlled update / replacement
- safe startup loading
- non-disclosure in normal logs
- ability to rotate without rewriting source code

## Forbidden Storage Patterns

The following patterns are forbidden:

- hardcoded credentials in code
- committed `.env` or config files with live secrets
- secrets inside notebooks
- secrets stored in plain-text docs
- secrets stored in UI mockups or screenshots
- secrets embedded in test fixtures intended to be shared
- secrets copied into shell history knowingly where avoidable
- secrets left in disposable scratch files

## Runtime Loading Policy

## Core rule

Secrets must be loaded at runtime from a controlled source and kept out of the codebase.

## Startup expectations

At startup, the system must verify:

- required secrets are present
- required secrets parse correctly
- environment selection is correct
- credentials are suitable for the intended role
- authorization succeeds where validation is appropriate

## Failure behavior

If validation fails:

- do not continue in “best effort” mode
- do not attempt live trading
- do not silently downgrade trust assumptions
- stay blocked until corrected

## In-Memory Exposure Policy

## Principle

The system should keep secret exposure in process memory as limited as practical.

## Rules

- load only the secrets required for the active process role
- do not duplicate secrets unnecessarily across components
- do not serialize secrets into routine status dumps
- do not include secrets in panic/debug output
- clear temporary secret-bearing structures where practical after use

This does not require premature low-level optimization, but it does require disciplined handling.

## Secret Metadata Policy

## Allowed metadata

The project may store safe metadata about secrets, including:

- key alias
- environment
- operational role
- last rotation date
- status
- IP restriction status
- owner / responsible operator

## Forbidden metadata patterns

Do not store:

- raw secret values
- full secret-bearing payloads
- full unmasked keys where avoidable
- reusable signed request examples containing live secret material

## Purpose of metadata

Secret metadata is useful for:

- inventory
- governance
- rotation tracking
- auditing
- and operational clarity

without exposing the underlying secret value.

## Logging and Redaction Policy

## Allowed in logs

Logs may include:

- secret alias
- environment
- role
- validation success/failure state
- masked key identifier where appropriate
- incident category related to secret handling

## Forbidden in logs

Logs must not include:

- raw API secret
- full live API key if avoidable
- signatures
- secret-bearing environment dumps
- full authenticated request payloads if they expose sensitive material
- copied configuration blobs containing secrets

## Redaction rule

If a secret-related error is logged, the output must be redacted by default.

## Rotation Policy

## Core rule

Secret rotation must be a normal supported operational process.

## Rotation categories

### Routine rotation
Rotation performed for hygiene or scheduled review.

### Forced rotation
Rotation performed because:
- trust boundary changed
- environment changed
- operator role changed
- or old secret scope is no longer appropriate

### Emergency revocation / rotation
Immediate invalidation and replacement because compromise is suspected.

## Rotation triggers

Secrets should be rotated when any of the following occurs:

- suspected exposure
- accidental disclosure
- host compromise suspicion
- infrastructure trust-boundary change
- role split or permission redesign
- operational review requiring refresh
- repeated security-relevant authorization anomalies
- explicit operator decision after security review

## Emergency Revocation Policy

## Immediate revocation triggers

Immediate revocation is required when:

- secret appears in logs, docs, screenshots, or chats
- unusual account activity suggests misuse
- host compromise is suspected
- unauthorized API activity is suspected
- production secret is copied into an untrusted environment
- operator cannot trust the secret boundary anymore

## Emergency response principle

Emergency revocation must be treated as a real incident.

It may require:

- bot safe mode
- incident escalation
- key replacement
- account-state verification
- operator review before resumption

## Secret Inventory Policy

The project should maintain a simple internal secret inventory.

## Minimum inventory fields

- secret alias
- environment
- operational role
- permission summary
- IP restriction status where relevant
- create date
- last rotation date
- status:
  - active
  - deprecated
  - revoked
- responsible operator / owner if applicable

## Important limitation

The inventory must contain **metadata only**, never the secret value itself.

## Access Policy

## Principle

Only the minimum required operators, processes, or environments should be able to access a given secret.

## Rules

- development access does not imply production access
- production secrets should remain inside the production trust boundary
- secrets should be granted by role and need, not by convenience
- a process should not receive secrets it does not require for its function

## Operator Handling Rules

Operators must:

- treat secrets as sensitive operational material
- avoid copying them casually
- rotate them when policy requires
- escalate immediately if accidental disclosure occurs

Operators must not:

- paste live secrets into troubleshooting chats
- share screenshots containing secrets
- store them in personal notes
- bypass the policy for convenience
- keep unmanaged copies “just in case”

## Integration with API Key Policy

This document works together with the API key policy.

In particular:

- secrets must follow least privilege through the keys they protect
- withdrawal-disabled keys remain mandatory for bot use
- role-separated keys should remain role-separated in storage and runtime loading
- production keys should remain IP restricted where required

## Incident Relationship

Secret-handling failures are not ordinary warnings.

They should map into the incident-response framework as security incidents.

Examples:
- suspected secret leak
- invalid credential anomaly
- unauthorized API activity
- production secret found in wrong environment

These may trigger:
- safe mode
- escalation
- revocation
- recovery review
- and explicit resumption approval

## What Is Explicitly In Scope

This policy covers:

- where secrets may and may not live
- runtime secret-loading expectations
- environment separation
- redaction rules
- metadata vs secret-value distinction
- rotation and revocation principles
- startup behavior for missing or invalid secrets
- operator handling boundaries

## What Is Explicitly Out of Scope for Now

This document does **not** yet define:

- final secret-manager product choice
- hardware-backed secret storage
- vault architecture
- full host security hardening
- enterprise IAM architecture
- detailed network topology

These may come later, but they are not required to lock the policy now.

## Decisions

The following decisions are accepted for secrets management:

- secrets must not be stored in code, git, docs, screenshots, chats, or normal logs
- development, paper / shadow, and production secrets must be separated
- production secrets must remain inside the production trust boundary
- the bot must load secrets from a controlled runtime source
- startup must fail closed if required secrets are missing or invalid
- secret values must never be exposed in normal observability outputs
- key rotation and emergency revocation must be documented operational procedures
- safe metadata about secrets may be tracked, but secret values may not
- secret-handling failures are security-relevant incidents

## Open Questions

The following remain open:

1. What exact runtime secret-loading method will be used on the NUC deployment?
2. Will v1 production use environment variables only, or a more structured secret source?
3. What exact masked identifier format should be used in logs?
4. Should the project keep a secret inventory inside project docs or only outside the repo for stronger separation?
5. What routine rotation cadence should become the default for production secrets?
6. Should any future operator interface expose secret-health metadata such as “rotation overdue” without exposing sensitive details?

## Next Steps

After this document, the next recommended files are:

1. `docs/09-operations/daily-weekly-review-process.md`
2. `docs/11-interface/operator-dashboard-requirements.md`
3. `docs/10-security/permission-scoping.md`

## References

Binance references:

- Binance USDⓈ-M Futures General Info  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info

- Binance API General Info  
  https://developers.binance.com/docs/algo/general-info

OWASP references:

- OWASP Secrets Management Cheat Sheet  
  https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

- OWASP SAMM Secure Deployment / Secret Management Guidance  
  https://owaspsamm.org/model/implementation/secure-deployment/stream-b/

Related internal project documents:

- `docs/10-security/api-key-policy.md`
- `docs/09-operations/incident-response.md`
- `docs/09-operations/restart-procedure.md`