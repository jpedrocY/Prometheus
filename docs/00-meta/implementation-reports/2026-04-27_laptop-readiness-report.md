# Laptop Readiness Report

**Repo:** `C:\Prometheus`
**Date:** 2026-04-27
**Goal:** Verify laptop can continue full Prometheus work (tests + backtests).
**Scope:** Read-only audit. No code changes, no credentials created, no MCP/Graphify enabled, no backtest run.

---

## 1. Git state

- Branch: `main`, clean, up-to-date with `origin/main`.
- HEAD: `1c60a27 Complete Phase 2s R1b-narrow execution`.
- **Note:** The user described main as "Phase 2s merged in", but `1c60a27` is a direct commit on main, not a merge commit. The PR-based merge sequence visible in recent history is for Phase 2p (`#17`). Phase 2s landed via direct commit. Worth confirming this matches expectations, but it does not block work.

## 2. Toolchain

| Tool | Status |
|---|---|
| System Python | 3.13.7 (system-wide; not used) |
| `.python-version` pin | `3.12` |
| `pyproject.toml` requires | `>=3.11,<3.13` |
| `uv` | `0.11.3` (working) |
| `.venv` | Created by `uv sync` |

## 3. Dependency install

`uv sync --all-groups` → 28 packages installed cleanly (pyarrow 23.0.1, duckdb 1.5.2, pydantic 2.13.2, httpx 0.28.1, numpy 2.4.4, ruff 0.15.11, mypy 1.20.1, pytest 9.0.3, +deps). No errors.

## 4. Verification commands

| Command | Result |
|---|---|
| `uv run pytest` | **429 passed, 2 skipped** in 9.58s |
| `uv run ruff check .` | **All checks passed** |
| `uv run ruff format --check .` | **124 files already formatted** |
| `uv run mypy src` | **Success: no issues found in 49 source files** |

## 5. Data inventory

| Location | Status |
|---|---|
| `data/` (Phase-2 root) | **Does not exist** |
| `research/data/raw/**` | Empty (only `.gitkeep` placeholders) |
| `research/data/normalized/**` | Empty (Hive layout `year=YYYY/month=MM` — template only) |
| `research/data/derived/**` | Empty (only `.gitkeep`) |
| `artifacts/` | Empty |
| `tests/fixtures/market_data/manifests/` | Synthetic BTCUSDT/ETHUSDT 15m fixtures exist (test-only) |

**No production parquet, DuckDB, or manifest files exist on this laptop.** This is by design — `.gitignore` excludes all `data/raw/**`, `data/normalized/**`, `data/derived/**`, `data/manifests/**`, `research/data/{raw,normalized,derived}/**`, and `artifacts/`. Datasets are never committed.

## 6. Can data be regenerated from existing scripts?

**Yes — fully scripted, no credentials required.**

- **Primary regenerator:** [scripts/phase2e_backfill.py](../../../scripts/phase2e_backfill.py) — uses Binance public bulk download + REST (httpx, no API keys) to materialize the locked v002 datasets:
  - `binance_usdm_<sym>_15m__v002` (standard 15m klines)
  - `binance_usdm_<sym>_1h_derived__v002` (derived 1h bars)
  - `binance_usdm_<sym>_markprice_15m__v002` (mark-price 15m)
  - `binance_usdm_<sym>_funding__v002` (funding events)
  - Coverage: BTCUSDT + ETHUSDT, 2022-01 → 2026-03. Idempotent, resumable.
- **Phase-3 backtest entry:** [scripts/phase3_smoke_run.py](../../../scripts/phase3_smoke_run.py) reads from `data/normalized/`, `data/derived/`, `data/derived/exchange_info/*.json`. **It will fail until Phase 2e backfill runs**, since `data/derived/exchange_info/` does not exist.
- **Phase 2s runners:** [scripts/phase2s_R1b_narrow_execution.py](../../../scripts/phase2s_R1b_narrow_execution.py) (and 2g/2l/2m peers) all consume the locked Phase 2e v002 datasets — same dependency.

## 7. Backtest readiness

**Backtests cannot run today on this laptop without first regenerating data.** Per the task instructions, no backfill or backtest was triggered. To enable backtests:

```text
uv run python scripts/phase2e_backfill.py
```

This pulls public Binance bulk archives + REST funding history. No keys, no exchange-write capability, safe under all v1 phase gates.

## 8. Safety posture

- No production credentials present. `.env` absent. `.env.example` only.
- `.mcp.json` absent (only `.mcp.example.json`, `.mcp.graphify.template.json` templates). MCP off as required.
- No exchange-write code paths invoked.
- No code changes made during this audit.

## 9. Verdict

| Capability | Status |
|---|---|
| Edit code, run tests | **Ready** |
| Run lint / format / type-check | **Ready** |
| Continue Phase 3+ implementation work | **Ready** |
| Run a backtest (Phase 2e/2g/2l/2m/2s/3) | **Blocked on data** — run `phase2e_backfill.py` first |

## 10. Recommended next step (no action taken)

If a backtest is needed soon, run `uv run python scripts/phase2e_backfill.py` once. It is research-only, public-data-only, idempotent, and consistent with all phase-gate constraints. Otherwise the laptop is fully ready for code/test/review work.
