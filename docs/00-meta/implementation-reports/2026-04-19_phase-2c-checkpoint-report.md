# Phase 2c — Checkpoint Report

**Date:** 2026-04-19
**Phase:** 2c — Mark-Price Klines, Funding History, and Public Exchange Metadata
**Branch:** `phase-2c/public-market-data-completion` (off `main` at `731088f`, 5 commits ahead pre-checkpoint, not pushed)
**Status:** COMPLETE. Awaiting operator review before merge; Phase 3 / Phase 2d not started.

---

## Phase

2c — Mark-Price Klines, Funding History, and Public Exchange Metadata.

## Goal

Complete the public-market-data foundation that Phase 3's backtester needs for realistic fill + cost modeling: mark-price klines (for stops evaluated against `MARK_PRICE`), funding-rate events (for multi-hour position funding accounting), and exchangeInfo snapshots (for tick/step/minNotional rounding). All three public, all three unauthenticated, and the REST client has zero authentication surface by design — mechanically enforced.

## Summary

Phase 2c shipped 3 new core domain models, 4 new research/data modules (one REST client + three dataset-specific sources), a small refactor to Phase 2b's `BulkDownloader` to serve both kline families, extensions to `storage.py` + `quality.py` + `ingest.py` for the new datasets, 76 new tests (2 of which are mechanical auth-surface guardrails), a complete bounded real-data run for BTCUSDT + ETHUSDT on all three datasets, TD-006 partial-resolution expanded to three new Binance endpoints, and full Gate 1 / Gate 2 / checkpoint reports. Test count: 136 → 212. Zero new runtime dependencies; no `pyproject.toml` / `uv.lock` change.

## Files changed (by commit)

| Commit | Hash | Summary | Size |
| --- | --- | --- | --- |
| 1 | `4ff2ba3` | core data models (3 models + tests) | 7 files, +509 |
| 2 | `4e0a465` | public GET-only REST client + auth guardrails | 2 files, +521 |
| 3 | `35f7d35` | bulk mark-price + BulkFamily refactor + tests | 3 files, +382 / −8 |
| 4 | `08a2a38` | funding-rate REST + exchangeInfo REST + orchestrators + configs | 9 files, +1,378 |
| 5 | `aae98f0` | ambiguity log + Gate-1/Gate-2 reports | 3 files, +1,280 |

Totals: 24 files changed, 4,070 insertions, 8 deletions across 5 commits.

## Files created (counts; see Gate 2 review §8 for the full list)

- 3 new core modules: `mark_price_klines.py`, `events.py`, `exchange_info.py`
- 4 new research/data modules: `binance_rest.py`, `mark_price.py`, `funding_rate.py`, `exchange_info.py`
- 7 new test files covering the above
- 3 new docs files under `docs/00-meta/implementation-reports/` (Gate 1 plan, Gate 2 review, this checkpoint)

Modified existing files: `src/prometheus/core/__init__.py`, `src/prometheus/research/data/{__init__,binance_bulk,ingest,storage,quality}.py`, `configs/dev.example.yaml`, `docs/00-meta/implementation-ambiguity-log.md`.

## Commands run

```
# Pre-flight
uv --version                          → uv 0.11.7
python --version                       → Python 3.12.4
git status --short                     → clean except Gate 1 plan untracked
git rev-list --left-right --count HEAD...@{u}   → 0  0

# Step 1
git checkout -b phase-2c/public-market-data-completion

# Step 2: env verify
uv sync                                → 28 packages; no new deps added

# Step 3: TD-006 verification via WebFetch (no code yet)
WebFetch data.binance.vision/.../markPriceKlines/.../2024-01.zip.CHECKSUM (path + format verified)
WebFetch github.com/binance/binance-public-data (mark-price CSV layout check — not documented)
WebFetch data.binance.vision/.../markPriceKlines/BTCUSDT/15m/2026-03.zip.CHECKSUM (target exists, SHA256 captured)
WebFetch data.binance.vision/.../markPriceKlines/ETHUSDT/15m/2026-03.zip.CHECKSUM (target exists)
WebFetch developers.binance.com Get-Funding-Rate-History (endpoint + shared-IP rate limit verified verbatim)
WebFetch developers.binance.com Exchange-Information (endpoint + response shape verified)

# Steps 4-10: write code + tests (no shell invocation)
# Quality gates (1st run)
uv run ruff check .                    → 4 errors; 2 auto-fixed + 2 targeted edits
uv run ruff format .                   → 13 files reformatted
uv run ruff format --check .           → 57 files already formatted
uv run mypy                            → Success: 25 source files
uv run pytest                          → 212 passed in 0.92s

# Step 13: bounded real run
uv run python -c <ingest script for 3 datasets> → SUCCESS
  (mark-price BTC+ETH 15m 2026-03; funding BTC+ETH 2026-03;
   exchangeInfo snapshot)

# Post-run verification
find data/ -type f                     → 24 files (2.1 MB total)
uv run python -c "hashlib check on mark-price ZIPs"
  → BTC 79edfb40...d32bf8 (matches pre-verified WebFetch)
  → ETH d30d71f3...fd5d   (matches pre-verified WebFetch)
git check-ignore <4 sampled data paths> → all ignored

# Gate 2 preparation
# Write 2026-04-19_phase-2c_gate-2-review.md

# Five commits (Gate 2 approved with count-fix)
git add src/prometheus/core/... tests/unit/core/...
git commit -m "phase-2c: core data models..."                       → 4ff2ba3
git add src/prometheus/research/data/binance_rest.py tests/.../test_binance_rest.py
git commit -m "phase-2c: public GET-only REST client..."            → 4e0a465
git add src/prometheus/research/data/{binance_bulk,mark_price}.py tests/.../test_mark_price.py
git commit -m "phase-2c: bulk mark-price + BulkFamily refactor..."  → 35f7d35
git add src/prometheus/research/data/{funding_rate,exchange_info,storage,quality,ingest,__init__}.py \
        configs/dev.example.yaml tests/.../test_{funding_rate,exchange_info}.py
git commit -m "phase-2c: funding-rate REST + exchangeInfo REST..."  → 08a2a38
git add docs/00-meta/implementation-ambiguity-log.md \
        docs/00-meta/implementation-reports/2026-04-19_phase-2c_gate-{1,2}*.md
git commit -m "phase-2c: ambiguity log + Gate-1/Gate-2 reports"     → aae98f0

# Commit 6 (this commit): checkpoint
git add docs/00-meta/implementation-reports/2026-04-19_phase-2c-checkpoint-report.md
git commit -m "phase-2c: checkpoint report"
```

No destructive git. No `--force`. No `git add -f`. No push. No `/fapi/*` authenticated calls. No credentials.

## Installations performed

**None this phase.** `uv sync` confirmed the 28-package environment from Phase 2b still resolves and installs cleanly. No `pyproject.toml` change, no `uv.lock` regeneration — Phase 2c reuses httpx, pyarrow, duckdb, pydantic + dev deps entirely.

## Configuration changed

- `configs/dev.example.yaml`: three new subsections (`mark_price`, `funding`, `exchange_info`) under the existing `research_data:` block, documenting default paths and the operator-flagged 1000ms pacing for `/fapi/v1/fundingRate`. Documentation-only; no loader consumes them.
- `src/prometheus/core/__init__.py`: re-exports extended.
- `src/prometheus/research/data/__init__.py`: re-exports extended with ~30 new Phase 2c names.

No other existing files modified beyond what the module additions required.

## Tests / checks passed

| Check | Command | Result |
| --- | --- | --- |
| Lint | `uv run ruff check .` | All checks passed! |
| Format | `uv run ruff format --check .` | 57 files already formatted |
| Type | `uv run mypy` | Success: 25 source files |
| Tests | `uv run pytest` | **212 passed** in 0.92s |

Test-count evolution: 2 (Phase 1) → 79 (Phase 2) → 136 (Phase 2b) → **212** (Phase 2c, +76 new).

76 new Phase 2c tests:

- `test_mark_price_klines.py` — 9
- `test_events.py` — 10
- `test_exchange_info.py` (core) — 8
- `test_binance_rest.py` — 13 (2 are the mechanical auth-surface guardrails)
- `test_mark_price.py` — 15
- `test_funding_rate.py` — 12
- `test_exchange_info.py` (research/data) — 9

## Tests / checks failed

None at branch tip. No mid-implementation failures this phase (the Phase 2c CSV-parser handles header-present and header-absent bulk files defensively per the GAP-010 lesson; no runtime surprises).

## Runtime output

No runtime surface introduced. Phase 2c is a research-data foundation extension. Real ingests are triggered by explicit operator `uv run python -c` invocations.

Real bounded run returned (all three datasets completed on 2026-04-19):

- Mark-price: BTCUSDT + ETHUSDT 15m 2026-03 → 2976 rows each, SHA256s match WebFetch pre-verified values exactly.
- Funding-rate: BTCUSDT + ETHUSDT 2026-03 → 93 events each (31 days × 3/day cadence), no 429s at 1000ms pacing.
- ExchangeInfo: single snapshot → BTCUSDT + ETHUSDT matched, 877,772-byte raw body SHA `7657b728...2289`, 2,073-byte derived summary.

Zero invalid windows across all five manifests.

## Known gaps

- **Mark-price 1h derivation** — not implemented in Phase 2c. If the backtester needs 1h mark-price bars, Phase 3 can either derive on demand (reusing `derive_1h_from_15m` against `MarkPriceKline`s, requiring a new signature) or fetch Binance's 1h mark-price bulk files directly. Recorded here; not blocking.
- **Account-authenticated endpoints** — `leverageBracket` and `commissionRate` remain deferred to a credential-gated Phase 2d. Phase 3's backtester uses placeholder commissions until then.
- **REST `/fapi/v1/markPriceKlines` fallback** — not implemented. Phase 2c uses bulk only. If bulk ever becomes unavailable, Phase 2c's plan calls for operator escalation rather than silent REST fallback.
- **WebSocket / user-stream** — deferred (Phase 6+).

## Spec ambiguities found

Appended to `docs/00-meta/implementation-ambiguity-log.md`:

| ID | Status | Summary |
| --- | --- | --- |
| GAP-20260419-011 | **RESOLVED** | `DatasetManifest` accepts `intervals=()` for event-type datasets (funding-rate). Confirmed by funding manifests round-tripping cleanly. |
| GAP-20260419-012 | **RESOLVED** | Binance `fundingRate` shares `500/5min/IP` rate limit with `fundingInfo` (operator-flagged at Gate 1). Verbatim confirmed via WebFetch; 1000ms pacing in `BinanceRestClient`. |
| GAP-20260419-013 | **RESOLVED** | Mark-price bulk CSV column layout undocumented in the README. Defensive positional parser; real 2026-03 SHA256s match WebFetch pre-captured values. |

No HIGH-risk escalations required. All 3 GAPs are LOW risk.

## Technical-debt updates needed

- **Per operator directive, no edits to `docs/12-roadmap/technical-debt-register.md` in 2c.** TD-006 remains OPEN overall; three additional slices (bulk mark-price, REST `fundingRate`, REST `exchangeInfo`) are annotated as verified in the per-module TD-006 evidence blocks. An operator-approved register update is a natural follow-up after 2c merges.
- No other TD entries changed.
- No new TD entries introduced.

## Safety constraints verified

| Constraint | Result |
| --- | --- |
| Production Binance API keys | **Not created, not requested, not used.** |
| Real secrets / `.env` | **None touched.** |
| Exchange-write capability | **None.** Only GET requests. |
| Signed requests / HMAC | **None anywhere.** Mechanically asserted. |
| `X-MBX-APIKEY` header | **Never constructed.** Mechanically tested. |
| Account-authenticated endpoints | **Not touched.** `leverageBracket`, `commissionRate`, `/fapi/v1/account/*`, all deferred. |
| WebSockets | **None.** |
| Third-party market-data sources | **None.** |
| `.mcp.json` / Graphify | **Not created / not enabled.** |
| Real downloaded data committed | **None** — all 24 artifacts git-ignored. |
| `.claude/*` / `CLAUDE.md` / current-project-state | **Not modified.** |
| `docs/12-roadmap/technical-debt-register.md` | **Not modified.** |
| Runtime DB | **Not touched.** |
| Destructive git / `git add -f` | **None.** |
| Dependencies added | **None.** No `pyproject.toml` / `uv.lock` changes. |
| Network during tests | **Zero.** `httpx.MockTransport` for all 212 tests. |
| Auth-surface drift in `binance_rest.py` | **Mechanically asserted by tests.** Fails the build if anyone adds `api_key`, `secret`, `sign_request`, etc. |

## Current runtime capability

None. Phase 2c is a research-data foundation extension. The `research.data` package now provides a public-only Binance REST client, three new dataset sources, and typed models covering mark-price klines, funding events, and exchange metadata. Nothing runs automatically — ingests are explicit operator invocations.

## Exchange connectivity status

Read-only, public, unauthenticated, strictly bounded. Endpoints touched in Phase 2c:
- `https://data.binance.vision/data/futures/um/monthly/markPriceKlines/...` (GET, CHECKSUM-verified)
- `https://fapi.binance.com/fapi/v1/fundingRate` (GET, public)
- `https://fapi.binance.com/fapi/v1/exchangeInfo` (GET, public)

Zero authenticated requests. Zero signed requests. Zero WebSocket traffic.

## Exchange-write capability status

**Disabled by absence.** `BinanceRestClient` is GET-only; the class has no signing code, no credential parameter, no HMAC. Two mechanical tests fail the build if the absence is ever violated. `BulkDownloader` is a static-file client (no write semantics exist on `data.binance.vision`). `configs/dev.example.yaml` continues to declare `exchange_write_enabled: false` and `real_capital_enabled: false`.

## Branch / commit state at end of Phase 2c (pre-checkpoint)

```
$ git log --oneline -6
aae98f0 phase-2c: ambiguity log + Gate-1/Gate-2 reports
08a2a38 phase-2c: funding-rate REST + exchangeInfo REST + ingest orchestrators
35f7d35 phase-2c: bulk mark-price + BulkFamily refactor + mark-price tests
4e0a465 phase-2c: public GET-only REST client with auth-surface guardrails
4ff2ba3 phase-2c: core data models (MarkPriceKline, FundingRateEvent, ExchangeInfoSnapshot)
731088f Merge pull request #3 from jpedrocY/phase-2b/real-historical-download
```

After this checkpoint commit lands, the branch is **6 commits ahead of `origin/main`** and has not been pushed. `main` is unchanged at `731088f`.

## Recommended next step

Two reasonable paths forward; operator decides.

1. **Phase 3 — Backtesting and Strategy Conformance.** All four public data foundations are now in place:
   - Standard 15m klines (Phase 2 synthetic + Phase 2b real)
   - Derived 1h bars (Phase 2)
   - Mark-price 15m klines (Phase 2c)
   - Funding-rate events (Phase 2c)
   - ExchangeInfo snapshot with per-symbol filters (Phase 2c)
   Phase 3 can begin strategy + backtester implementation on 2026-03 real data + Phase 2 synthetic fixtures. This is the natural next step — the data loop is now closed.

2. **Phase 2d — account-authenticated public-account data.** Covers `/fapi/v1/leverageBracket` and `/fapi/v2/commissionRate`. Requires credential-gate opening (new phase gate). Lower priority; Phase 3's backtester can proceed with placeholder commissions until Phase 2d lands.

Phase 3 is the higher-value increment given the public-data foundation is complete. Phase 2d is useful but can wait until backtester results indicate commission precision matters for the validation gates.

## Questions for ChatGPT / operator

1. **Push timing.** Push `phase-2c/public-market-data-completion` to `origin` now, open PR #4 into `main`, or stack Phase 3 on top first?
2. **TD-006 annotation.** Now that three more slices are verified, would you like a small follow-up commit that appends the verified slices to `docs/12-roadmap/technical-debt-register.md` TD-006 entry? Per Phase 2c instructions I did not edit that file.
3. **Mark-price 1h derivation.** Phase 3's backtester will probably want 1h mark-price context. Should it be (a) implemented in Phase 3 via a new `derive_1h_from_15m` variant for `MarkPriceKline`, (b) added as a small Phase 2c.1 follow-up commit, or (c) left to when Phase 3 actually exercises it?
4. **Next phase choice.** Phase 3, Phase 2d, or parallel work?

None of these block Phase 2c completion. Phase 2c is done.
