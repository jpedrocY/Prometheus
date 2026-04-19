# Phase 2b — Checkpoint Report

**Date:** 2026-04-19
**Phase:** 2b — Real BTCUSDT/ETHUSDT Historical Data Download
**Branch:** `phase-2b/real-historical-download` (off `main` at `ddf0013`, 5 commits ahead pre-checkpoint, not pushed)
**Status:** COMPLETE. Awaiting operator review before merge; Phase 2c / Phase 3 not started.

---

## Phase

2b — Real BTCUSDT/ETHUSDT Historical Data Download.

## Goal

Close the data-fetch loop that Phase 2 deliberately left open: download real BTCUSDT and ETHUSDT 15m historical klines from the official Binance public bulk source (`data.binance.vision`), feed them through the Phase 2 pipeline, and produce versioned Parquet datasets + derived 1h bars + manifests — all with SHA256 integrity verification, resumability, zero credentials, and zero `/fapi` authenticated API calls.

## Summary

Phase 2b shipped 3 new source modules (`binance_bulk.py`, `download_state.py`, `ingest.py`), 47 new tests (9 of which specifically cover GAP-20260419-010's header-row fix), a bounded real-data run on BTCUSDT + ETHUSDT 15m 2026-03 with checksum-verified SHA256s exactly matching the pre-run WebFetch values, and full Gate 1 / Gate 2 / Checkpoint reports. TD-006 was partially resolved (bulk-CSV slice verified against official Binance sources at coding time). One mid-run divergence from my initial TD-006 inference (GAP-010: the real CSV contains a header row) was caught, escalated, resolved with operator-approved strict header detection, and tested. Test count went from 79 (end of Phase 2) → 136.

## Files changed (by commit)

| Commit | Hash | Summary | Size |
| --- | --- | --- | --- |
| 1 | `48aad43` | add httpx; extend dev config example | 3 files changed, +80 |
| 2 | `32b0adc` | download-state tracking and bulk-download client | 4 files changed, +976 |
| 3 | `a8f7815` | ingest orchestrator with header-aware CSV parsing | 2 files changed, +809 |
| 4 | `539924b` | integration test + research/data `__init__` re-exports | 2 files changed, +308 / −2 |
| 5 | `9f357ca` | GAP-010 ambiguity-log entry + Gate-1/Gate-2 reports | 3 files changed, +1,180 |

Totals: 14 files changed, 3,353 insertions, 2 deletions across 5 commits. All real downloaded data (ZIPs, Parquet, manifests, download-state JSON) remain git-ignored and uncommitted — confirmed via `git check-ignore` at three sampled paths.

## Files created (counts; see Gate 2 review §8 for the full list)

- 3 new source files under `src/prometheus/research/data/`
- 3 new test files under `tests/unit/research/data/`
- 1 new test file under `tests/integration/`
- 3 new docs files under `docs/00-meta/implementation-reports/` (Gate 1 plan, Gate 2 review, this checkpoint)

Modified existing files: `pyproject.toml` (+httpx), `uv.lock`, `configs/dev.example.yaml` (+binance_bulk block), `src/prometheus/research/data/__init__.py` (re-exports), `docs/00-meta/implementation-ambiguity-log.md` (+GAP-010).

## Commands run

```
# Pre-flight
uv --version                          → uv 0.11.7
python --version                       → Python 3.12.4
git status --short                     → clean except Gate 1 plan (expected, carried into branch)
git rev-list --left-right --count HEAD...@{u}   → 0  0

# Step 1
git checkout -b phase-2b/real-historical-download

# Step 2-3: dep
# edit pyproject.toml (add httpx>=0.27)
uv sync                                → 28 packages; +6 new (httpx 0.28.1 + transitive)

# Step 4: TD-006 verification via WebFetch (no code yet)
WebFetch github.com/binance/binance-public-data         (README fact extraction)
WebFetch data.binance.vision/.../BTCUSDT-15m-2024-01.zip.CHECKSUM   (path + format verified)
WebFetch data.binance.vision/.../BTCUSDT-15m-2026-03.zip.CHECKSUM   (target exists, SHA256 captured)
WebFetch data.binance.vision/.../ETHUSDT-15m-2026-03.zip.CHECKSUM   (target exists, SHA256 captured)

# Steps 5-10: write sources, tests, integration test, configs/__init__ updates
# Quality gates (1st run)
uv run ruff check .                    → 6 errors; fixed via targeted edits + ruff --fix
uv run ruff format .                   → 5 files reformatted
uv run mypy                            → 1 error; fixed by direct core.intervals import
uv run pytest                          → 126 passed in 1.81s

# Step 11: bounded real download (1st attempt)
uv run python -c <ingest script>   → FAILED at CSV line 1 (header row present)

# STOP + escalation (GAP-010)
# Edit ingest.py: added _is_kline_csv_header + strict extract_rows_from_zip update
# Edit binance_bulk.py: corrected TD-006 evidence block
# Add 9 new header-handling unit tests to test_ingest.py

# Quality gates (2nd run post-fix)
uv run ruff check .                    → All checks passed!
uv run ruff format .                   → 1 file reformatted (test_ingest.py)
uv run mypy                            → Success: 18 source files
uv run pytest                          → 136 passed in 0.85s

# Step 11: bounded real download (2nd attempt)
uv run python -c <ingest script>   → SUCCESS for both BTCUSDT + ETHUSDT

# Post-run verification
find data/ -type f                     → 12 files (796 KB total)
git check-ignore <ZIP, Parquet, manifest>  → all 3 matched (all ignored)

# Gate 2 preparation
# Write 2026-04-19_phase-2b_gate-2-review.md

# Five commits (Gate 2 approved)
git add pyproject.toml uv.lock configs/dev.example.yaml
git commit -m "phase-2b: add httpx..."                  → 48aad43
git add src/prometheus/research/data/download_state.py src/prometheus/research/data/binance_bulk.py tests/unit/research/data/test_download_state.py tests/unit/research/data/test_binance_bulk.py
git commit -m "phase-2b: download-state tracking..."    → 32b0adc
git add src/prometheus/research/data/ingest.py tests/unit/research/data/test_ingest.py
git commit -m "phase-2b: ingest orchestrator..."        → a8f7815
git add src/prometheus/research/data/__init__.py tests/integration/test_binance_bulk_end_to_end.py
git commit -m "phase-2b: integration test..."           → 539924b
git add docs/00-meta/implementation-ambiguity-log.md docs/00-meta/implementation-reports/2026-04-19_phase-2b_gate-1-plan.md docs/00-meta/implementation-reports/2026-04-19_phase-2b_gate-2-review.md
git commit -m "phase-2b: GAP-010 ambiguity-log entry..." → 9f357ca

# Commit 6 (this commit): checkpoint
git add docs/00-meta/implementation-reports/2026-04-19_phase-2b-checkpoint-report.md
git commit -m "phase-2b: checkpoint report"
```

No destructive git. No `--force`. No `git add -f`. No push. No `/fapi` calls. No credentials.

## Installations performed

Project-local only (inside `.venv/`, git-ignored). Phase 2b added 6 packages on top of the 22 from Phase 2:

- `httpx==0.28.1`
- `anyio==4.13.0` (transitive)
- `certifi==2026.2.25` (transitive)
- `h11==0.16.0` (transitive)
- `httpcore==1.0.9` (transitive)
- `idna==3.11` (transitive)

Total project environment: 28 packages. `uv.lock` regenerated. No global installs. Operator-installed `uv` itself (from Phase 1) reused.

## Configuration changed

- `pyproject.toml`: added `httpx>=0.27` to `[project].dependencies`.
- `uv.lock`: regenerated.
- `configs/dev.example.yaml`: new `binance_bulk:` block under `research_data:` documenting `base_url`, `raw_root`, `state_root`, `user_agent`, `pace_ms` defaults. Documentation-only; no config loader consumes them.
- `src/prometheus/research/data/__init__.py`: extended `__all__` and re-exports with Phase 2b public names.

No other existing files modified.

## Tests / checks passed

| Check | Command | Result |
| --- | --- | --- |
| Lint | `uv run ruff check .` | All checks passed! |
| Format | `uv run ruff format --check .` | 43 files already formatted |
| Type | `uv run mypy` | Success: 18 source files |
| Tests | `uv run pytest` | 136 passed in 0.85s |

Test-count evolution: 2 (Phase 1) → 79 (Phase 2) → 126 (Phase 2b pre-fix) → **136** (Phase 2b post-fix).

Phase 2b added 57 new tests:

- `test_download_state.py` — 11 (state transitions, JSON I/O, atomicity, dataset mismatch)
- `test_binance_bulk.py` — 22 (URL construction, checksum parsing positive/negative, downloader happy path, 429-retry success, retry exhaustion, non-retriable 404, User-Agent header, idempotent cache, stale-cache re-download, pacing observance)
- `test_ingest.py` — 24 (CSV row parsing, ZIP extraction, header detection positive/negative, extract-with/without header, extract-preserves-data, loud-fail on non-header non-numeric, loud-fail on wrong column count, month iteration, expected-bars-for-month)
- `test_binance_bulk_end_to_end.py` — 2 (full pipeline, resume idempotency)

Minus 2 pre-existing tests replaced by expanded versions = 57 net new.

## Tests / checks failed

None at branch tip. One mid-implementation failure (CSV parser hit on real data — GAP-010) was caught, operator-escalated, fixed, and regression-tested.

## Runtime output

No runtime behavior introduced in Phase 2b. The bulk ingest runs only when explicitly invoked (via a Python `-c` script or a future `scripts/fetch_historical_data.py`). No CLI entrypoint added in 2b.

Real bounded ingest returned (both symbols):

```
row_count_15m: 2976     (= 31 days × 96 bars/day)
row_count_1h:   744     (= 31 days × 24 bars/day, derived)
invalid_windows_15m: 0
invalid_windows_1h:  0
```

SHA256 of real ZIPs:
- BTCUSDT-15m-2026-03.zip: `ea25e84ddffdcc8b7ba68fb47363daee6a9ef53941f152c9ebf6d4e165d32bf8`
- ETHUSDT-15m-2026-03.zip: `8070870b512ab7c312329a7fc1a45217fc7aff5ed7bbb4f805d96caf7c99fd5d`

Both match byte-for-byte the pre-run WebFetch checksums captured during TD-006 verification.

## Known gaps

- **TD-006** remains OPEN overall. Phase 2b resolved the bulk-CSV slice only. REST `/fapi/v1/klines` endpoint verification and user-stream verification remain for later phases. No edits to `docs/12-roadmap/technical-debt-register.md` in 2b (per operator instruction to stop and ask before editing that file).
- Mark-price klines, funding-rate history, exchange-info snapshots — all not downloaded in 2b. Each is a separate Phase 2c-family proposal.
- Leverage-bracket and commission-rate endpoints require account authentication; blocked by the no-credentials posture. Future phase after credential gates open.
- `src/prometheus/market_data/` runtime package — not created (Phase 5/6/7 scope).
- No CLI yet. `scripts/fetch_historical_data.py` deferred.
- No CI workflow. Still deferred.
- Legacy `research/data/` tree alongside new top-level `data/` (GAP-007) — not cleaned up this phase.

## Spec ambiguities found

| ID | Status | Summary |
| --- | --- | --- |
| GAP-20260419-010 | **RESOLVED** | Real Binance USD-M bulk CSVs contain a header row as line 1. My TD-006 inference "no header row" was wrong. Option A (strict detection) approved and applied; parser updated; 9 tests added; real run completed. |

No other Phase 2b GAPs needed to be logged. Pre-flight anticipated GAPs (rate limits, ZIP internal member name) did not materialize as issues during execution.

## Technical-debt updates needed

- Per operator instruction, **no edits to `docs/12-roadmap/technical-debt-register.md` in 2b**. TD-006 remains OPEN; operator decides whether to record the partial-resolution annotation (bulk-CSV slice verified) as a follow-up.
- No other TD entries changed.
- No new TD entries added.

## Safety constraints verified

| Constraint | Result |
| --- | --- |
| Production Binance API keys | none created, none requested, none used |
| Real secrets / `.env` | none touched |
| Exchange-write capability | none — only `GET` requests to `data.binance.vision` |
| Binance authenticated APIs | **no `/fapi/*` calls made** |
| WebSockets | none |
| Third-party market-data sources | none |
| `.mcp.json` | not created; git-ignored; confirmed absent |
| Graphify | not enabled; template files still inert |
| MCP servers | not activated |
| Real downloaded data committed | **none** — all 12 real artifacts under git-ignored `data/`; `git check-ignore` confirmed |
| `.claude/*` | not modified |
| Runtime DB | not touched |
| Destructive git | none used |
| `git add -f` | not used |
| Files touched outside approved manifest | **only `.gitignore` untouched this phase** (Phase 2 rules already cover repo-root `data/`) |
| Installs beyond project `.venv` | none |
| Logs containing secrets | none — only public URLs and SHA256s are logged |
| Network during tests | zero — all tests use httpx `MockTransport` |

## Current runtime capability

None. Phase 2b is a research-data foundation extension. `import prometheus.research.data` now re-exports `BulkDownloader`, `ingest_monthly_range`, and related helpers; calling them is an explicit operator action, not a runtime behavior.

## Exchange connectivity status

Read-only, public, unauthenticated, bounded:

- Only `GET` requests.
- Only to `https://data.binance.vision/`.
- Only for public monthly kline ZIPs and their `.CHECKSUM` files.
- No Binance API key ever used.

During Phase 2b execution: 4 real network calls (2 CHECKSUM + 2 ZIP). WebFetch calls during TD-006 verification used the browser-side web-fetch tool, not direct project code.

## Exchange-write capability status

Disabled by absence. The downloader is a pure `GET` client. There is no POST/PUT/DELETE code anywhere in the Phase 2b modules. `configs/dev.example.yaml` continues to declare `exchange_write_enabled: false` and `real_capital_enabled: false` as the safe defaults.

## Branch / commit state at end of Phase 2b (pre-checkpoint)

```
$ git log --oneline -6
9f357ca phase-2b: GAP-010 ambiguity-log entry + Gate-1/Gate-2 reports
539924b phase-2b: integration test + research/data __init__ re-exports
a8f7815 phase-2b: ingest orchestrator with header-aware CSV parsing
32b0adc phase-2b: download-state tracking and bulk-download client
48aad43 phase-2b: add httpx; extend dev config example
ddf0013 Merge pull request #2 from jpedrocY/phase-2/historical-data-foundation
```

After this checkpoint commit lands, the branch is **6 commits ahead of `origin/main`** and has not been pushed. `main` is unchanged at `ddf0013`.

## Recommended next step

Two viable paths forward; operator decides.

1. **Phase 2c — Mark-price klines + funding history + exchange-info snapshots.** Natural next increment. Extends the bulk-download pattern to mark-price klines (bulk-CSV path available), and adds a simpler REST client for funding history and exchange-info (both public endpoints). Keeps the account-authenticated endpoints (`/fapi/v1/leverageBracket`, `/fapi/v2/commissionRate`) deferred to a credential-gate-opening later. Estimated effort: similar to Phase 2b.
2. **Phase 3 — Backtesting and Strategy Conformance.** Consumes Phase 2b's real BTCUSDT + ETHUSDT 15m March 2026 data (1 month) plus the synthetic fixtures from Phase 2. Strategy correctness testable on this slice. Profitability claims would require wider history from Phase 2c + a fuller backfill first.

Either way, the next action is a plan-only proposal, not code. Phase 2c is the lower-risk increment; Phase 3 exercises strategy logic against real data.

## Questions for ChatGPT / operator

1. **Push timing.** Push `phase-2b/real-historical-download` to `origin` now, open a PR into `main`, or hold until Phase 2c / Phase 3 is ready on top? Phase 1 and Phase 2 precedent was push-then-PR-per-phase.
2. **TD-006 annotation.** Would you like a follow-up commit that appends a "Bulk-CSV slice verified" note under TD-006 in `docs/12-roadmap/technical-debt-register.md`? Per Phase 2b instructions I did not edit that file, so this would be a separate small commit on its own branch.
3. **Operator-run backfill.** Now that the bulk ingest works, an operator could run a wider backfill (e.g., 2024-01 → 2026-03) locally using the same `ingest_monthly_range` with an expanded range. Should that be a Phase 2c task, a Phase 2-ops task, or left to the operator's discretion entirely?
4. **Next phase.** Phase 2c first, Phase 3 first, or parallel branches?

None of these block Phase 2b completion. Phase 2b is done.
