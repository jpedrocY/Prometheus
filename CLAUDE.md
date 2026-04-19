# Prometheus Claude Code Instructions

Prometheus is a safety-first, rules-based, operator-supervised trading system for Binance USDⓈ-M futures.

Read first:

@docs/00-meta/current-project-state.md
@docs/00-meta/ai-coding-handoff.md
@docs/09-operations/first-run-setup-checklist.md
@docs/12-roadmap/phase-gates.md
@docs/12-roadmap/technical-debt-register.md

Project rules:

@.claude/rules/prometheus-core.md
@.claude/rules/prometheus-safety.md
@.claude/rules/prometheus-phase-workflow.md
@.claude/rules/prometheus-mcp-and-secrets.md

## Immediate Operating Rule

Start with:

```text
Phase 0 — Handoff Intake and Repo Audit
```

Do not begin broad implementation until Phase 0 is reviewed and Phase 1 is explicitly approved.

## Agent Pack

Project-specific agents live in:

```text
.claude/agents/
```

Prefer:

- `prometheus-orchestrator` for phase planning and coordination.
- `prometheus-safety-guardian` before/after risky changes.
- `prometheus-spec-architect` for ambiguity/spec-gap decisions.
- `prometheus-test-verification-engineer` before declaring a phase complete.

## Hard Limits

- No production Binance keys.
- No exchange-write before approved gate.
- No one-shot full-system implementation.
- No secrets in git, prompts, screenshots, logs, docs, or MCP config.
- Every phase ends with a runnable checkpoint report.
