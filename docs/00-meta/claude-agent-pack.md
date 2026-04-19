# Claude Agent Pack

## Purpose

This document describes the Prometheus-specific Claude Code agent pack.

The pack strengthens Claude Code during phased implementation without weakening the project safety model. It does not replace `docs/00-meta/ai-coding-handoff.md`, `docs/12-roadmap/phase-gates.md`, or `docs/09-operations/first-run-setup-checklist.md`.

## Included Files

```text
CLAUDE.md
.claude/settings.json
.claude/settings.local.example.json
.claude/rules/prometheus-core.md
.claude/rules/prometheus-safety.md
.claude/rules/prometheus-phase-workflow.md
.claude/rules/prometheus-mcp-and-secrets.md
.claude/agents/*.md
.mcp.example.json
.mcp.graphify.template.json
.gitignore.prometheus-claude-additions.txt
prometheus-claude-setup-prompt.md
```

## How to Use

1. Copy this pack into the repository root.
2. Merge `.gitignore.prometheus-claude-additions.txt` into `.gitignore`.
3. Review `.mcp.example.json`.
4. If desired, copy `.mcp.example.json` to `.mcp.json` and enable only approved MCP servers.
5. Restart Claude Code or use `/agents` to refresh project agents.
6. Verify agents with `/agents` or `claude agents`.
7. Start Phase 0 using the prompt in `docs/00-meta/ai-coding-handoff.md`.

## Recommended First Agents

```text
prometheus-orchestrator
prometheus-safety-guardian
prometheus-spec-architect
prometheus-test-verification-engineer
```

## MCP Policy

Do not use JAF ERP MCP config for Prometheus.

Do not configure company MySQL/MariaDB MCP servers, Laravel MCP servers, Phoenix theme MCP servers, Figma tokens, plaintext credentials, or Binance production write tools.

Recommended early MCP servers:

- `filesystem-prometheus`, scoped only to `C:/Prometheus`,
- `context7`, for library documentation,
- `playwright`, later for dashboard testing.

Graphify is optional and should be added only after installation and secret-exclusion rules are verified.
