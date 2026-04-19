# Prometheus MCP and Secrets Rules

## Secrets

Never read, print, log, commit, summarize, or paste secrets.

Forbidden in git, docs, prompts, screenshots, MCP configs, logs, runtime DB, and tests:

- Binance API keys/secrets.
- Telegram bot tokens.
- n8n webhook secrets.
- dashboard admin passwords.
- private SSH keys.
- `.env` values.
- signed exchange request payloads.
- request signatures.

## MCP Rules

MCP servers may be useful, but every MCP server increases trust surface.

Allowed early MCP categories:

- project-scoped filesystem access to `C:\Prometheus` only,
- documentation lookup such as Context7,
- browser automation such as Playwright only when dashboard exists,
- Graphify or repo-graph tooling only after local install and secret exclusions are verified.

Forbidden MCP categories early:

- Binance production account/exchange-write MCP,
- ERP/company database MCPs,
- MySQL/MariaDB company servers,
- MCP configs with plaintext credentials,
- unrestricted filesystem access outside the project,
- tools that execute arbitrary remote code without operator review.

## Graphify

Graphify may be added after Phase 0 or during Phase 1 if useful. Before indexing, exclude `.env*`, secrets, runtime DBs, logs, backups, local credentials, and private screenshots.
