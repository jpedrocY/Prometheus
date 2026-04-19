# Prometheus Phase Workflow

## Implementation Method

Do not implement the full system in one pass.

Build in this order:

```text
Phase 0 — Repo audit
Phase 1 — Local development foundation
Phase 2 — Historical data and validation foundation
Phase 3 — Backtesting and strategy conformance
Phase 4 — Risk, state, and persistence runtime
Phase 5 — Dashboard, observability, and alerts
Phase 6 — Dry-run exchange simulation
Phase 7 — Paper/shadow operation
Phase 8 — Tiny-live preparation
Phase 9 — Scaled-live preparation
```

## Phase Boundary Rule

Each phase must end with a checkpoint report:

```md
## Phase Checkpoint Report

Phase:
Goal:
Summary:
Files changed:
Files created:
Commands run:
Installations performed:
Configuration changed:
Tests/checks passed:
Tests/checks failed:
Runtime output:
Known gaps:
Spec ambiguities found:
Technical-debt updates needed:
Safety constraints verified:
Current runtime capability:
Exchange connectivity status:
Exchange-write capability status:
Recommended next step:
Question for ChatGPT/operator, if any:
```

## ChatGPT Escalation Rule

If setup, installation, environment, account, credentials, system-level config, NUC setup, or unclear safety-sensitive action is needed, stop and produce a ChatGPT Setup Escalation Prompt with current phase, attempted command, full error/output, what appears missing, why Claude stopped, safety constraints, files changed, commands run, and the question for ChatGPT.

## Spec Gap Rule

Do not guess silently. Create/update `docs/00-meta/implementation-ambiguity-log.md`. For safety-relevant open items, update `docs/12-roadmap/technical-debt-register.md`.
