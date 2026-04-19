# configs/

Example configuration files for Prometheus.

## Policy

- These files are **examples only**. They must never contain real secrets, real API credentials, or production values.
- Real secrets belong in a local `.env` (git-ignored) or a future secrets-management path (see `docs/10-security/secrets-management.md`).
- Copies of these files used for local development (e.g., `dev.local.yaml`) should be git-ignored and not committed.
- All example profiles default to a safe posture: `SAFE_MODE` on start, `exchange_write_enabled: false`, `real_capital_enabled: false`, fake adapter.

## Current files

- `dev.example.yaml` — local development profile (safe defaults, fake adapter).

Additional stage profiles (`validation.example.yaml`, `paper.example.yaml`, `production.example.yaml`) will be added by the phases that use them, per `docs/08-architecture/codebase-structure.md`.
