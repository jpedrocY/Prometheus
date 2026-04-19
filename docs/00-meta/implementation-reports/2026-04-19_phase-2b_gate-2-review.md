# Phase 2b — Gate 2 Review

**Date:** 2026-04-19
**Phase:** 2b — Real BTCUSDT/ETHUSDT Historical Data Download
**Branch:** `phase-2b/real-historical-download` (off `main` at `ddf0013`, not pushed)
**Status at time of report:** Working-tree only. No commits on the Phase 2b branch yet. Awaiting operator Gate 2 approval.

---

## 1. Purpose

This report is the Gate 2 artifact for Phase 2b. It captures the implementation, the TD-006 source verification, a mid-run divergence (GAP-20260419-010 — CSV header-row mismatch) with its resolution, the real bounded download evidence for BTCUSDT + ETHUSDT 15m 2026-03, quality-gate output, and the proposed commit structure.

All 136 tests pass. ruff, ruff format, mypy all pass. Real download completed for both symbols with SHA256 verification matching the pre-run WebFetch checksums.

---

## 2. Operator conditions at Gate 1 (recap)

| # | Condition | Status |
| --- | --- | --- |
| 1 | Dep: `httpx` added via uv | **Satisfied.** Resolved to `httpx==0.28.1` (+ 5 transitive: anyio, certifi, h11, httpcore, idna). 28 packages total. |
| 2 | Official-source verification before coding | **Satisfied.** See §3. |
| 3 | Network scope narrow (data.binance.vision only) | **Satisfied.** 4 network calls total (2 CHECKSUMs + 2 ZIPs). No Binance authenticated endpoints, no `/fapi/*`, no WebSockets, no third-party, no MCP. |
| 4 | Initial scope: BTCUSDT + ETHUSDT 15m 2026-03 | **Satisfied.** No other months; no mark-price / funding / metadata; no full backfill. |
| 5 | Raw/normalized/generated data git-ignored | **Satisfied.** All 10 real artifacts confirmed under git-ignored `data/` paths. |
| 6 | Implementation scope bounded | **Satisfied.** Only the three source files `binance_bulk.py`, `download_state.py`, `ingest.py` + fixtures + tests + narrow `__init__.py` re-exports + narrow configs edit. No exchange adapter, no strategy, no runtime, no CLI, no dashboard. |
| 7 | Tests use mocked network | **Satisfied.** `httpx.MockTransport` in every test; zero network activity in `pytest`. |
| 8 | Correctly log + escalate on source divergence | **Satisfied.** GAP-010 logged HIGH-risk mid-run; escalation sent; awaited approval; applied approved fix; resolved GAP-010 with evidence. |

---

## 3. Official-source verification evidence (TD-006 partial resolution)

Performed via WebFetch before any downloader code was written. Evidence embedded as a block comment at the top of `src/prometheus/research/data/binance_bulk.py` (corrected post-GAP-010 to drop the "no header row" claim).

| Assumption | Verified via | Result |
| --- | --- | --- |
| Base URL `https://data.binance.vision/` | github.com/binance/binance-public-data README | ✓ |
| USD-M futures path `/data/futures/um/monthly/klines/<SYM>/<INTV>/` | Direct WebFetch of `BTCUSDT-15m-2024-01.zip.CHECKSUM` (200 OK, 90 bytes) | ✓ |
| ZIP filename `<SYM>-<INTV>-<YYYY>-<MM>.zip` | Same fetch; filename appeared in checksum body | ✓ |
| `.CHECKSUM` pairing | README + direct fetch | ✓ |
| `.CHECKSUM` format `<64-hex><2 spaces><filename>` | Direct inspection of 2024-01 + 2026-03 files | ✓ |
| CSV column order (12 columns, trailing `ignore`) | README table + real 2026-03 data | ✓ (by position; header labels differ slightly, handled by positional parser) |
| Timestamp unit = UTC milliseconds for USD-M futures | README + real data (`1772323200000` → `2026-03-01T00:00:00Z`) | ✓ |
| Target months 2026-03 exist for BTCUSDT + ETHUSDT | WebFetch returned SHA256 for both | ✓ |
| **No header row** (initial assumption) | Inferred from README table | ✗ **WRONG** — see GAP-010 |

Pre-run SHA256s captured from WebFetch:
- `BTCUSDT-15m-2026-03.zip` → `ea25e84ddffdcc8b7ba68fb47363daee6a9ef53941f152c9ebf6d4e165d32bf8`
- `ETHUSDT-15m-2026-03.zip` → `8070870b512ab7c312329a7fc1a45217fc7aff5ed7bbb4f805d96caf7c99fd5d`

Both matched the real-run checksums byte-for-byte. Phase 2b resolves the **bulk-CSV slice** of TD-006 only; REST klines and user-stream verifications remain OPEN for later phases.

---

## 4. Mid-run divergence: GAP-20260419-010

### 4.1 What happened

During Step 11 (real bounded download), BTCUSDT-15m-2026-03.zip was downloaded and checksum-verified successfully, then CSV parsing failed on line 1 with:

```
DataIntegrityError: CSV line 1: failed to cast numeric field
  (invalid literal for int() with base 10: 'open_time')
```

Inspection of the downloaded ZIP revealed a header row as the first CSV line:
```
open_time,open,high,low,close,volume,close_time,quote_volume,count,taker_buy_volume,taker_buy_quote_volume,ignore
```

The github.com/binance/binance-public-data README **does not explicitly state** whether the CSV has a header; my TD-006 evidence inferred "no header row" from the README's example table. The real file contradicts that inference.

### 4.2 Response (per Gate 1 condition 3)

Per operator directive "stop immediately, log HIGH-risk GAP, produce escalation prompt, do not implement the conflicting behavior":

1. Halted the real run after the BTCUSDT ZIP landed. ETHUSDT download was never attempted.
2. Logged **GAP-20260419-010** at HIGH risk in `docs/00-meta/implementation-ambiguity-log.md`.
3. Produced a ChatGPT/operator escalation prompt with:
   - root-cause analysis,
   - four options considered,
   - Option A recommended (defensive first-line header detection),
   - four clarification questions,
   - safety-posture status.
4. Did **not** patch the code until operator approval arrived.

### 4.3 Operator-approved fix applied

The operator approved **Option A with stricter header handling**:

- `ingest.py::_is_kline_csv_header(line)` — returns True only if the line has exactly 12 comma-separated fields AND the first field normalized/lowercased equals `"open_time"`.
- `ingest.py::extract_rows_from_zip` — skips the first line iff `_is_kline_csv_header` returns True; otherwise parses it as data. Any non-numeric, non-header first row raises `DataIntegrityError` (loud fail, no silent skipping).
- `binance_bulk.py` TD-006 evidence block — `"No header row"` assertion removed, replaced with a correction citing GAP-010, documenting the observed header format, and noting the defensive parser behavior.

### 4.4 Unit tests added

Nine new tests in `tests/unit/research/data/test_ingest.py` covering the fix (all in the "Header-row handling (GAP-20260419-010)" section):

| Test | What it verifies |
| --- | --- |
| `test_is_header_recognizes_open_time` | Real header line matches the predicate. |
| `test_is_header_case_insensitive` | Case variation doesn't evade detection. |
| `test_is_header_rejects_numeric_first_field` | Numeric first field ≠ header. |
| `test_is_header_rejects_wrong_column_count` | Short rows ≠ header. |
| `test_is_header_rejects_similar_but_wrong_name` | `"open"` ≠ `"open_time"`. |
| `test_extract_skips_header_row` | Header + data → only data. |
| `test_extract_works_without_header` | Header-absent files still parse. |
| `test_extract_header_skip_preserves_data_rows` | Header-present and header-absent paths produce identical row output. |
| `test_extract_rejects_non_numeric_non_header_first_row` | `hello,...` fails loudly (no silent skip). |
| `test_extract_rejects_wrong_column_count_first_row` | Short malformed first row fails loudly. |

(The `test_extract_` suite has 10 entries total including the pre-existing happy-path; numbered above as 9 new. Full suite: 136 tests, up from 126 pre-fix.)

### 4.5 GAP-20260419-010 status

**RESOLVED.** Full evidence in `docs/00-meta/implementation-ambiguity-log.md`.

---

## 5. Commands run (in order)

```
# Pre-flight
uv --version                              → uv 0.11.7
python --version                           → Python 3.12.4
git rev-parse --abbrev-ref HEAD            → main
git status --short                         → (clean except Gate 1 plan untracked)
git rev-list --left-right --count HEAD...@{u}   → 0  0

# Step 1
git checkout -b phase-2b/real-historical-download

# Step 2-3: dep
# edit pyproject.toml (add httpx>=0.27)
uv sync                                    → 28 packages; +6 new (httpx 0.28.1 + 5 transitive)

# Step 4: TD-006 verification (no code yet)
WebFetch https://github.com/binance/binance-public-data  (README fact extraction)
WebFetch https://data.binance.vision/data/futures/um/monthly/klines/BTCUSDT/15m/BTCUSDT-15m-2024-01.zip.CHECKSUM  (confirms path + format)
WebFetch https://data.binance.vision/.../BTCUSDT-15m-2026-03.zip.CHECKSUM  (confirms target exists)
WebFetch https://data.binance.vision/.../ETHUSDT-15m-2026-03.zip.CHECKSUM  (confirms target exists)

# Steps 5-9: write code + tests (no shell invocation)
# Step 10: quality gates
uv run ruff check .           → 6 errors; fixed via edits + ruff --fix
uv run ruff format .          → 5 files reformatted
uv run mypy                   → 1 error; fixed by direct import from .intervals
uv run pytest                 → 126 passed in 1.81s

# Step 11: bounded real download (1st attempt)
uv run python -c <ingest script>   → FAILED at CSV line 1 (header)

# STOP + escalation (GAP-010)
# Apply Option A fix: _is_kline_csv_header + extract_rows_from_zip update
# Apply TD-006 evidence correction in binance_bulk.py
# Add 9 unit tests in test_ingest.py

# Rerun quality gates
uv run ruff check .           → All checks passed!
uv run ruff format .          → 1 file reformatted (test_ingest.py)
uv run mypy                   → Success: 18 source files
uv run pytest                 → 136 passed in 0.85s

# Rerun bounded real download
uv run python -c <ingest script>   → SUCCESS for both BTCUSDT + ETHUSDT

# Post-run verification
find data/ -type f -exec ls -l  → 10 files, 796 KB total
du -sh data/                    → 796K
git check-ignore <ZIP, Parquet, manifest>  → all 3 matched (ignored)

git status                      → working tree as at §11
```

No destructive git. No `--force`. No `git add -f`. No commits. No push. No credentials.

---

## 6. Real bounded download — results

### 6.1 BTCUSDT 15m 2026-03

```json
{
  "symbol": "BTCUSDT",
  "zip_url": "https://data.binance.vision/data/futures/um/monthly/klines/BTCUSDT/15m/BTCUSDT-15m-2026-03.zip",
  "zip_sha256": "ea25e84ddffdcc8b7ba68fb47363daee6a9ef53941f152c9ebf6d4e165d32bf8",
  "was_cached": true,
  "row_count_15m": 2976,
  "row_count_1h": 744,
  "invalid_windows_15m": 0,
  "invalid_windows_1h": 0
}
```

`was_cached=true` because the first-attempt ZIP (checksum-verified) was still on disk when the rerun happened; the downloader correctly skipped re-fetching. SHA256 matches the pre-run WebFetch value exactly.

### 6.2 ETHUSDT 15m 2026-03

```json
{
  "symbol": "ETHUSDT",
  "zip_url": "https://data.binance.vision/data/futures/um/monthly/klines/ETHUSDT/15m/ETHUSDT-15m-2026-03.zip",
  "zip_sha256": "8070870b512ab7c312329a7fc1a45217fc7aff5ed7bbb4f805d96caf7c99fd5d",
  "was_cached": false,
  "row_count_15m": 2976,
  "row_count_1h": 744,
  "invalid_windows_15m": 0,
  "invalid_windows_1h": 0
}
```

Fresh download; SHA256 matches the pre-run WebFetch value exactly.

### 6.3 Combined row-count sanity

| Symbol | 15m rows observed | 15m rows expected (31d × 96) | 1h rows observed | 1h rows expected (31d × 24) |
| --- | --- | --- | --- | --- |
| BTCUSDT | 2976 | 2976 ✓ | 744 | 744 ✓ |
| ETHUSDT | 2976 | 2976 ✓ | 744 | 744 ✓ |

Zero invalid windows — no duplicates, no monotonic violations, no missing bars, no future bars, no partial 1h buckets.

### 6.4 Example real manifest (`binance_usdm_btcusdt_15m__v001.manifest.json`)

```json
{
  "canonical_timestamp_format": "unix_milliseconds",
  "canonical_timezone": "UTC",
  "created_at_utc_ms": 1776630221127,
  "dataset_category": "normalized_kline",
  "dataset_name": "binance_usdm_btcusdt_15m",
  "dataset_version": "binance_usdm_btcusdt_15m__v001",
  "generator": "prometheus.research.data.ingest.ingest_monthly_range",
  "intervals": ["15m"],
  "invalid_windows": [],
  "notes": "Phase 2b bulk ingest from data.binance.vision. Months: 2026-03 to 2026-03.",
  "partitioning": ["symbol", "interval", "year", "month"],
  "pipeline_version": "prometheus@0.0.0",
  "predecessor_version": null,
  "primary_key": ["symbol", "interval", "open_time"],
  "schema_version": "kline_v1",
  "sources": [
    "https://data.binance.vision/data/futures/um/monthly/klines/BTCUSDT/15m/BTCUSDT-15m-2026-03.zip"
  ],
  "symbols": ["BTCUSDT"]
}
```

The corresponding 1h derived manifest (`binance_usdm_btcusdt_1h_derived__v001.manifest.json`) lists `dataset_category: derived_kline`, `sources: ["derived:binance_usdm_btcusdt_15m__v001"]`, and the same 0-entry `invalid_windows`. ETHUSDT manifests are structurally identical with ETH-specific symbol / source values.

### 6.5 Example real download-state file (`_downloads/binance_usdm_btcusdt_15m__state.json`)

```json
{
  "dataset_name": "binance_usdm_btcusdt_15m",
  "last_updated_utc_ms": 1776630221028,
  "months": {
    "2026-03": {
      "status": "NORMALIZED",
      "zip_sha256": "ea25e84ddffdcc8b7ba68fb47363daee6a9ef53941f152c9ebf6d4e165d32bf8",
      "downloaded_at_utc_ms": 1776630221028,
      "verified_at_utc_ms": 1776630221028,
      "normalized_at_utc_ms": 1776630221028,
      "raw_path": "c:\\Prometheus\\data\\raw\\binance_usdm\\klines\\symbol=BTCUSDT\\interval=15m\\year=2026\\month=03\\BTCUSDT-15m-2026-03.zip",
      "normalized_path": "c:\\Prometheus\\data\\normalized\\klines\\symbol=BTCUSDT\\interval=15m\\year=2026\\month=03\\part-0000.parquet",
      "row_count": 2976,
      "last_error": null
    }
  },
  "schema_version": "download_state_v1"
}
```

---

## 7. Disk footprint

| Artifact | Path | Size (bytes) |
| --- | --- | --- |
| BTCUSDT ZIP (raw) | `data/raw/binance_usdm/klines/symbol=BTCUSDT/interval=15m/year=2026/month=03/BTCUSDT-15m-2026-03.zip` | 145,250 |
| ETHUSDT ZIP (raw) | `data/raw/.../symbol=ETHUSDT/.../ETHUSDT-15m-2026-03.zip` | 148,329 |
| BTCUSDT 15m Parquet | `data/normalized/klines/symbol=BTCUSDT/...part-0000.parquet` | 184,934 |
| ETHUSDT 15m Parquet | `data/normalized/klines/symbol=ETHUSDT/...part-0000.parquet` | 186,900 |
| BTCUSDT 1h Parquet | `data/derived/bars_1h/standard/symbol=BTCUSDT/...part-0000.parquet` | 50,074 |
| ETHUSDT 1h Parquet | `data/derived/bars_1h/standard/symbol=ETHUSDT/...part-0000.parquet` | 51,354 |
| BTCUSDT 15m manifest | `data/manifests/binance_usdm_btcusdt_15m__v001.manifest.json` | 928 |
| ETHUSDT 15m manifest | `data/manifests/binance_usdm_ethusdt_15m__v001.manifest.json` | 928 |
| BTCUSDT 1h manifest | `data/manifests/binance_usdm_btcusdt_1h_derived__v001.manifest.json` | 908 |
| ETHUSDT 1h manifest | `data/manifests/binance_usdm_ethusdt_1h_derived__v001.manifest.json` | 908 |
| BTCUSDT download state | `data/manifests/_downloads/binance_usdm_btcusdt_15m__state.json` | 775 |
| ETHUSDT download state | `data/manifests/_downloads/binance_usdm_ethusdt_15m__state.json` | 775 |
| **Total** | `data/` | **796 KB** |

All 12 artifacts confirmed git-ignored (`git check-ignore` matched for 3 sampled paths covering all three families: raw ZIP, Parquet, manifest JSON).

---

## 8. Files changed

### 8.1 Tracked files modified (5)

```
.gitignore                          (no further edits this phase; Phase 2 rules already cover data/)
configs/dev.example.yaml            +10 lines (binance_bulk block under research_data)
docs/00-meta/implementation-ambiguity-log.md   +108 lines (GAP-004..009 from Phase 2 + GAP-010 resolved)
pyproject.toml                       +1 line  (httpx dep)
src/prometheus/research/data/__init__.py    rewrite with ~20 extra exports
uv.lock                              regenerated (+ ~260 lines for httpx + transitive)
```

Note: `docs/00-meta/implementation-ambiguity-log.md` currently also shows Phase 2 GAPs 004-009 as "modified" because Phase 2b appends to it; the Phase 2 entries are unchanged and the net diff is exactly the GAP-010 block.

### 8.2 Untracked new files

```
docs/00-meta/implementation-reports/2026-04-19_phase-2b_gate-1-plan.md
docs/00-meta/implementation-reports/2026-04-19_phase-2b_gate-2-review.md   ← this file
src/prometheus/research/data/binance_bulk.py
src/prometheus/research/data/download_state.py
src/prometheus/research/data/ingest.py
tests/integration/test_binance_bulk_end_to_end.py
tests/unit/research/data/test_binance_bulk.py
tests/unit/research/data/test_download_state.py
tests/unit/research/data/test_ingest.py
```

### 8.3 `git status` at Gate 2

```
On branch phase-2b/real-historical-download
Changes not staged for commit:
  modified:   configs/dev.example.yaml
  modified:   docs/00-meta/implementation-ambiguity-log.md
  modified:   pyproject.toml
  modified:   src/prometheus/research/data/__init__.py
  modified:   uv.lock

Untracked files:
  docs/00-meta/implementation-reports/2026-04-19_phase-2b_gate-1-plan.md
  (new source / test modules — see 8.2)
```

---

## 9. Quality-gate results

Final run at Gate 2 time:

```
$ uv run ruff check .
All checks passed!

$ uv run ruff format --check .
43 files already formatted

$ uv run mypy
Success: no issues found in 18 source files

$ uv run pytest
........................................................................ [ 52%]
................................................................         [100%]
136 passed in 0.85s
```

Test count evolution across phases: 2 (Phase 1) → 79 (Phase 2) → 126 (Phase 2b pre-header-fix) → **136** (Phase 2b post-header-fix, including 9 new header tests + 1 wrong-column test).

---

## 10. Quality-check results on real data

All four quality checks on the real ingested klines returned **empty** (= clean data):

| Check | BTCUSDT result | ETHUSDT result |
| --- | --- | --- |
| `check_no_duplicates` | 0 duplicates | 0 duplicates |
| `check_timestamp_monotonic` | 0 violations | 0 violations |
| `check_no_missing_bars` (bounded to 2026-03-01 → 2026-03-31) | 0 gaps | 0 gaps |
| `check_no_future_bars` (vs `utc_now_ms()`) | 0 future bars | 0 future bars |

The `invalid_windows_15m` list in both manifests is therefore `[]`. Derivation produced 744 fully-completed 1h buckets with zero partial buckets, so the derived-1h manifests also have `invalid_windows = []`.

---

## 11. Safety checklist

| Check | Result |
| --- | --- |
| Production Binance API keys | **Not created, not requested, not used.** `data.binance.vision` is a public unauthenticated endpoint. |
| Real secrets / `.env` | **None touched.** `.env.example` unchanged since Phase 2. |
| Exchange-write capability | **None.** Only `GET` requests to `data.binance.vision`. No `POST`/`PUT`/`DELETE` anywhere. |
| Binance authenticated APIs | **None called.** No `/fapi/*` requests. |
| WebSockets | **None.** |
| Third-party market-data sources | **None.** |
| `.mcp.json` | **Not created.** |
| Graphify | **Not enabled.** |
| MCP servers | **Not activated.** |
| Real data committed | **None.** All 12 real artifacts under git-ignored `data/`; confirmed by `git check-ignore`. |
| `.claude/*` | **Not modified.** |
| Runtime DB | **Not touched.** |
| Destructive git | **None.** `git mv` not used this phase; `git rm` not used; `git reset` not used. |
| `git add -f` | **Not used.** |
| Files touched outside approved manifest | **None.** |
| Installs beyond project `.venv` | **None.** |
| Logs containing secrets | **None.** The downloader logs URLs (public) and SHA256s (public); nothing sensitive. |
| Network during tests | **Zero.** All tests use httpx `MockTransport`. Real downloads are only run interactively via `uv run python -c`. |

---

## 12. Ambiguity-log entries (Phase 2b)

| ID | Status | Summary |
| --- | --- | --- |
| GAP-20260419-010 | **RESOLVED** | Real Binance USD-M bulk CSVs have a header row; TD-006 evidence corrected; parser updated with strict header detection; 9 new tests. |

No other Phase 2b GAPs needed to be filed. (Pre-flight assumptions — rate limits, ZIP internal member name — were anticipated in the Gate 1 plan §27 as possibly-needed GAP slots; both turned out to be fine in practice and no entry was created.)

---

## 13. Proposed commit structure

Five small reviewable commits + a post-Gate-2 checkpoint commit. Same cadence as Phase 2.

| # | Title | Contents |
| --- | --- | --- |
| 1 | `phase-2b: add httpx; extend dev config example` | `pyproject.toml`, `uv.lock`, `configs/dev.example.yaml` (binance_bulk subkeys) |
| 2 | `phase-2b: download-state tracking and bulk-download client` | `src/prometheus/research/data/download_state.py`, `src/prometheus/research/data/binance_bulk.py`, their unit tests |
| 3 | `phase-2b: ingest orchestrator with header-aware CSV parsing` | `src/prometheus/research/data/ingest.py`, `test_ingest.py` (including all header-handling tests) |
| 4 | `phase-2b: integration test + research/data __init__ re-exports` | `tests/integration/test_binance_bulk_end_to_end.py`, `src/prometheus/research/data/__init__.py` |
| 5 | `phase-2b: GAP-010 ambiguity-log entry + Gate-1/Gate-2 reports` | `docs/00-meta/implementation-ambiguity-log.md`, both Phase 2b implementation-reports docs |
| 6 (post-Gate-2) | `phase-2b: checkpoint report` | Checkpoint report. Any TD-006 status annotation bundled here if operator approves. |

All commit messages follow Phase 1/2 convention (no `Co-Authored-By`).

No push. No PR during Phase 2b execution. Operator decides when to push and merge.

---

## 14. Items explicitly out of scope (confirmed untouched)

- `CLAUDE.md`
- `README.md`
- `docs/00-meta/current-project-state.md`
- `docs/12-roadmap/technical-debt-register.md` (TD-006 remains OPEN; partial annotation deferred to operator preference)
- All specialist docs under `docs/03-*` through `docs/12-*` (except the ambiguity log, which Phase 2b appends to)
- `.claude/` (agents, rules, settings)
- `.mcp.example.json`, `.mcp.graphify.template.json` (templates untouched)
- `.mcp.json` — not created
- `research/`, `infra/`, `notebooks/` top-level directories
- No strategy, risk, execution, exchange adapter, persistence, operator, runtime, dashboard, or market_data runtime modules introduced
- No real data of any kind committed

---

## 15. Recommended next step

Two viable paths forward; operator decides.

1. **Phase 2c — Mark-price klines + funding history + exchange-info snapshots.** The natural next increment. Reuses `BulkDownloader` for mark-price (bulk), introduces a REST client for funding + exchange-info (simpler endpoints than kline pagination). Keeps the account-authenticated endpoints (`leverageBracket`, `commissionRate`) deferred to a credential-phase-gate-opening later.

2. **Phase 3 — Backtesting and Strategy Conformance.** Begins with Phase 2b's real BTCUSDT + ETHUSDT 15m March 2026 data (1 month of real history) plus synthetic fixtures. Strategy correctness is provable on this slice; profitability claims would need wider history from Phase 2c / fuller backfill first.

Either way, the next action is a plan-only proposal. Phase 2b's implementation closes the data-fetch loop.

**Awaiting operator Gate 2 approval.**
