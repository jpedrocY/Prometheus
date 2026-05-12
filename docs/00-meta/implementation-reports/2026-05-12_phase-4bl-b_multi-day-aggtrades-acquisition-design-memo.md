# Phase 4bl-B — Multi-Day aggTrades Acquisition Authorization / Design Memo

**Phase identity:** Phase 4bl-B — Multi-Day aggTrades Acquisition Authorization / Design Memo (docs-only).
**Date:** 2026-05-12.
**Phase type:** docs-only design / authorization-gate memo.
**Branch:** `phase-4bl-b/multi-day-aggtrades-acquisition-design-memo`.
**Base:** `main` at `dc2240e7a43047823c8b964d52112432b7a61c79` (Phase 4bl-A SHA-chain-fixup commit on top of the Phase 4bl-A merge-closeout `b9adf68c2662849e344859ec2d7810b9b813ff63`).
**Status:** drafted; pending operator review.

A note on the SHA-chain pattern: the Phase 4bl-A merge-closeout itself anchored its §2 final-`main` value at the merge-closeout commit `b9adf68`. The one-commit fixup on top of that anchor (commit `dc2240e`) only records the final-`main` SHA back into §2 of the Phase 4bl-A merge-closeout; it does not change Phase 4bl-A lifecycle semantics. Phase 4bl-B branches from `dc2240e` because that is the post-fixup `main` state; the canonical "Phase 4bl-A project-complete" anchor remains the merge-closeout commit (`b9adf68`).

---

## 1. Phase identity

- **Phase name:** Phase 4bl-B — Multi-Day aggTrades Acquisition Authorization / Design Memo.
- **Phase type:** docs-only design / authorization-gate memo.
- **Branch:** `phase-4bl-b/multi-day-aggtrades-acquisition-design-memo`.
- **Base SHA:** `main` at `dc2240e7a43047823c8b964d52112432b7a61c79`.
- **Predecessor anchor:** Phase 4bl-A merge-closeout `b9adf68c2662849e344859ec2d7810b9b813ff63` (project-complete).
- **Authorization:** explicit operator authorization for Phase 4bl-B only.

Phase 4bl-B is **strictly docs-only**. It does **not**:

- acquire data of any kind;
- download files;
- call public endpoints, public REST APIs, or public archive endpoints from code;
- call Binance APIs of any kind;
- call authenticated APIs or private endpoints;
- open user streams or WebSockets;
- read, create, or load credentials, API keys, `.env`, or `.mcp.json`;
- enable MCP or Graphify;
- create, modify, move, copy, rename, or delete any file under `data/microstructure/`;
- create raw, normalized, derived, feature, label, gate-report, successor-state, split, segmentation, or diagnostic artefacts;
- create a new dataset manifest, a multi-day manifest, an acquisition log, or any sidecar;
- rerun any eligibility gate (raw / derived / feature / label);
- run kernels, normalizers, or processing scripts;
- compute statistics, returns, or descriptive metrics;
- execute diagnostics or Q1–Q7 question sets;
- train ML, design ML architecture, rank features, or create meta-labeling;
- create a strategy, compute signals, or run backtests;
- compute PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit / strategy output;
- modify any source code, test, script, `scripts/...` entry, `pyproject.toml`, `README.md`, `.gitignore`, or MCP file;
- flip `research_eligible` on any manifest;
- transition `eligibility_gate_status` on any manifest;
- change `chronological_split_policy` on any actual manifest;
- modify project locks, retained verdicts, M0 governance, the post-null cooldown rule, the cooled-down families list, the Phase 4al refined no-rescue rule, or the Phase 4bb-F canonical path policy;
- modify, move, rename, copy, or delete the existing one-day Phase 4az artefacts (raw manifest, raw zip, sidecar, acquisition log);
- authorize Phase 4bl-C execution, Phase 4bl-D, Phase 4bl-E, any Phase 4bm-* / 4bn-* / 4bo-* / 4bp-* / 4bq-* successor, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation.

Tracked changes by Phase 4bl-B are exactly three new docs (this memo + the Phase 4bl-B closeout + narrow paragraph + "Current phase:" block update in `docs/00-meta/current-project-state.md`). No `data/microstructure/` artefact, no local gitignored file, no source / test / script / config / pyproject / README / `.gitignore` / MCP file is created or modified.

---

## 2. Pre-state and motivation

### 2.1 Pre-state at Phase 4bl-B start

The repository is at `main` SHA `dc2240e7a43047823c8b964d52112432b7a61c79`, which is the Phase 4bl-A SHA-chain-fixup commit on top of the Phase 4bl-A merge-closeout `b9adf68c2662849e344859ec2d7810b9b813ff63` (Phase 4bl-A is project-complete on `main`).

The existing one-day fixture remains intact:

| Property | Value |
| --- | --- |
| Source | Binance USDⓈ-M Futures public aggTrades daily archive (`data.binance.vision`) |
| Symbol | `BTCUSDT` |
| Date | `2025-01-15` (one UTC day) |
| Raw zip path | `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip` |
| Raw zip SHA256 | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| Raw zip event count | 1,681,098 |
| Raw zip start_time_ms | 1736899205109 |
| Raw zip end_time_ms | 1736985599991 |
| Raw manifest path | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json` |
| Raw manifest dataset family | `microstructure_raw_aggtrades_v001` |
| Raw manifest version | `v001` |
| Raw manifest `research_eligible` | `false` |
| Raw manifest `eligibility_gate_status` | `"pending"` |
| Raw manifest `code_commit_sha` | `caaad39e40604571758bc58eaac374344c7852e8` |
| Phase 4az gate report id | `microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c` |
| Phase 4az gate report SHA256 | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| Phase 4az gate report status | `pass` (45 / 45) |

The locked label-family research cell remains:

| Property | Value |
| --- | --- |
| Label family | `microstructure_labels_aggtrades_v001` |
| Symbol | `BTCUSDT` |
| Date | `2025-01-15` |
| Row count | 1,681,098 |
| Column count | 39 |
| Horizons | `["1s", "5s", "15s", "60s"]` |
| `censored_per_horizon` | `{"1s": 9, "5s": 42, "15s": 118, "60s": 507}` |
| `invalid_price_row_count` | 0 |
| Label parquet SHA256 | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` |
| Label manifest SHA256 | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` |
| `label_config_hash` | `fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00` |
| `research_eligible` | `false` (unchanged) |
| `eligibility_gate_status` | `"pending"` (unchanged) |
| `chronological_split_policy` | `"not_yet_defined"` (unchanged) |

Phase 4bj-J recorded a no-formal-split determination (Option D) for the locked one-day cell at `data/microstructure/successor-state/microstructure_labels_aggtrades_v001__v001__split_policy__phase-4bj-j.json` (gitignored; SHA256 `7e461eb5508affa9ecd8f9a8127a5528082567a9b7492dd94648002ed37c4fa6`).

Phase 4bj-K recorded the predeclared Label Diagnostic Study Plan (Q1–Q15) as a study-plan-only memo, with no diagnostic execution.

### 2.2 What Phase 4bl-A established

Phase 4bl-A (the immediately preceding docs-only requirements memo, merge-closeout `b9adf68`) evaluated seven multi-day-expansion options A–G and made two recommendations:

- **Primary recommendation:** Option B — BTCUSDT-only, 30 contiguous UTC days minimum (the cleanest forward-research path for a *separately authorized* future Phase 4bl-B acquisition design).
- **Preferred upper bound:** Option C — BTCUSDT-only, 60–90 contiguous UTC days (preferred upper-bound path if storage and bandwidth are not the limiting factor; offers stronger temporal robustness for future descriptive aggregate statistics, neutral-segmentation governance memos, multi-day label diagnostic plans, and future ML-feasibility memos — all of which remain unauthorized).

Phase 4bl-A explicitly did **not** authorize Phase 4bl-B execution or any download. Phase 4bl-A made the requirements list; it did not lock the acquisition design.

### 2.3 Why Phase 4bl-B exists

The operator's Phase 4bl-B authorization explicitly states that **storage and disk space are not a practical constraint** for the acquisition design. That removes the only material reason Phase 4bl-A held Option C back from primary recommendation. Under that constraint, Phase 4bl-B selects the Phase 4bl-A *preferred upper-bound* path (Option C, 90 contiguous UTC days, BTCUSDT-only) and locks the exact acquisition design boundary in advance of any download.

Phase 4bl-B answers the question "what would a future Phase 4bl-C have to do, what exact 90 dates, what paths, what manifest schema, what failure policy, what hash discipline, what gitignore boundary, what relationship to the existing one-day fixture, and what is forbidden?" — without performing any download. Phase 4bl-B is therefore a docs-only authorization-gate memo that turns the Phase 4bl-A requirements into a specific predeclared acquisition design.

### 2.4 Why this design is conservative

The design is conservative because:

- it acquires raw aggTrades archives only (no derived layers, no features, no labels, no diagnostics, no ML, no strategy);
- it sources files only from `data.binance.vision` public daily aggTrades archives (no authenticated APIs, no private endpoints, no live REST, no WebSockets);
- it locks the date range deterministically (no symbol mining, no date mining, no opportunistic post-hoc selection);
- it preserves all Phase 4az / 4bb / 4bc / 4bd / 4be / 4bf / 4bg / 4bh / 4bi / 4bj artefacts byte-identically;
- it makes Phase 4bl-C's allowed surface narrowly scoped (download + checksum verification + manifest writing + acquisition log + gitignored evidence) and explicitly excludes every downstream activity that could touch the post-null cooldown surface, the no-rescue boundary, or the locked retained-verdict ledger.

---

## 3. Acquisition scope decision

Phase 4bl-B locks the future Phase 4bl-C acquisition scope as follows.

### 3.1 Selected path

**Path:** Option C from Phase 4bl-A — BTCUSDT-only, 60–90 contiguous UTC days, preferred upper bound.

**Cardinality:** exactly **90 contiguous UTC days**.

**Symbol:** **`BTCUSDT` only**.

**Date range:** **2024-12-01 through 2025-02-28 inclusive (UTC)**.

### 3.2 Why this exact range

The selected 90-day window has the following properties:

- **Contiguous:** every UTC day in the range is included; no gaps, no skipping, no "trading-day" calendar logic.
- **Span:** December 2024 + January 2025 + February 2025 = 31 + 31 + 28 = **90 days exactly**. (2025 is not a leap year, so February 2025 has 28 days.)
- **Includes the existing fixture day:** `2025-01-15` is the 46th day of the range. The existing one-day Phase 4az artefacts are inside the locked range and must remain byte-identical (see §14 below).
- **Covers weekdays and weekends:** 90 contiguous UTC days include approximately 26 weekend days (Saturdays and Sundays) and 64 weekdays. This provides material for any future weekday-vs-weekend descriptive diagnostic (not authorized).
- **Spans three calendar months:** December 2024, January 2025, February 2025. This provides material for any future per-month descriptive diagnostic (not authorized).
- **Spans calendar-year boundary:** 2024 → 2025 transition is included (December 2024 + January 2025). This provides material for any future year-end / new-year regime descriptive diagnostic (not authorized).
- **Recent enough that public archive availability is expected to be complete** for completed monthly archives plus completed daily archives (operator should verify availability before any Phase 4bl-C authorization; Phase 4bl-B does not perform availability checks).
- **Old enough that all archives are settled** (no in-progress UTC day at acquisition time; no partial-day artefacts).

### 3.3 What this does NOT do

This scope decision:

- does **not** add a second symbol (ETHUSDT / SOLUSDT / BNBUSDT / XRPUSDT / ADAUSDT / DOGEUSDT / any alt) — Phase 4bl-A Options D/E/F (multi-symbol) are explicitly rejected for Phase 4bl-B / Phase 4bl-C scope;
- does **not** extend beyond 90 days — Phase 4bl-A Option G (180+ days) is explicitly rejected for Phase 4bl-B / Phase 4bl-C scope;
- does **not** shrink to fewer than 90 days — Phase 4bl-A Option A (single-day only) and the lower bound of Options B (30 days) and C (60 days) are explicitly rejected for Phase 4bl-B / Phase 4bl-C scope, given the operator's storage-non-constraint clarification;
- does **not** use any non-aggTrades source (no klines, no mark-price, no metrics, no funding, no aggressive-flow, no aggregated-by-second / by-minute / by-hour archives) — only `data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/...`;
- does **not** mix daily archives with monthly archives — daily-only;
- does **not** target the in-progress month (e.g., does not include any UTC day on or after the current date at acquisition time; the locked range ends well before 2026-05-12);
- does **not** allow opportunistic date substitution — if a single date is unavailable in the public archive at Phase 4bl-C execution time, Phase 4bl-C must record the missing date verbatim and report it (see §12 below); it must not silently swap or fill;
- does **not** allow symbol substitution if BTCUSDT is unavailable on a specific UTC day — the symbol is locked.

### 3.4 Phase 4bl-A Options A–G mapping

| Option | Description | Status for Phase 4bl-C scope |
| --- | --- | --- |
| A | Single-day only (existing) | REJECTED |
| B | BTCUSDT, 30 days minimum | REJECTED (operator selected upper bound) |
| C | BTCUSDT, 60–90 days preferred | **SELECTED — 90 days** |
| D | BTCUSDT + ETHUSDT, 30+ days | REJECTED |
| E | BTCUSDT + ETHUSDT + 1 alt, 30+ days | REJECTED |
| F | BTCUSDT + ETHUSDT + multi-alt, 30+ days | REJECTED |
| G | BTCUSDT, 180+ days | REJECTED (out of scope for Phase 4bl-C) |

---

## 4. Exact future date list

The future Phase 4bl-C acquisition MUST acquire exactly the following 90 contiguous UTC daily aggTrades archives for symbol `BTCUSDT`. The list is generated deterministically from the locked range and is the canonical date list for the future Phase 4bl-C run. The list is alphabetically sorted (which is identical to chronologically sorted for ISO-8601 `YYYY-MM-DD` dates).

### 4.1 December 2024 (31 days)

```
2024-12-01
2024-12-02
2024-12-03
2024-12-04
2024-12-05
2024-12-06
2024-12-07
2024-12-08
2024-12-09
2024-12-10
2024-12-11
2024-12-12
2024-12-13
2024-12-14
2024-12-15
2024-12-16
2024-12-17
2024-12-18
2024-12-19
2024-12-20
2024-12-21
2024-12-22
2024-12-23
2024-12-24
2024-12-25
2024-12-26
2024-12-27
2024-12-28
2024-12-29
2024-12-30
2024-12-31
```

### 4.2 January 2025 (31 days)

```
2025-01-01
2025-01-02
2025-01-03
2025-01-04
2025-01-05
2025-01-06
2025-01-07
2025-01-08
2025-01-09
2025-01-10
2025-01-11
2025-01-12
2025-01-13
2025-01-14
2025-01-15    [* = existing Phase 4az fixture day; must remain byte-identical]
2025-01-16
2025-01-17
2025-01-18
2025-01-19
2025-01-20
2025-01-21
2025-01-22
2025-01-23
2025-01-24
2025-01-25
2025-01-26
2025-01-27
2025-01-28
2025-01-29
2025-01-30
2025-01-31
```

### 4.3 February 2025 (28 days)

```
2025-02-01
2025-02-02
2025-02-03
2025-02-04
2025-02-05
2025-02-06
2025-02-07
2025-02-08
2025-02-09
2025-02-10
2025-02-11
2025-02-12
2025-02-13
2025-02-14
2025-02-15
2025-02-16
2025-02-17
2025-02-18
2025-02-19
2025-02-20
2025-02-21
2025-02-22
2025-02-23
2025-02-24
2025-02-25
2025-02-26
2025-02-27
2025-02-28
```

### 4.4 Totals and invariants

- **Total date count:** 31 (Dec 2024) + 31 (Jan 2025) + 28 (Feb 2025) = **90 dates exactly**.
- **No gaps:** the dates are contiguous; every UTC day in `[2024-12-01, 2025-02-28]` is included.
- **No duplicates:** every date appears exactly once.
- **No future dates:** every date is fully completed (well before 2026-05-12).
- **Deterministic:** the list is produced by a date-range generator; no symbol mining, no date mining, no post-hoc reordering, no opportunistic exclusions.
- **Includes existing fixture day:** `2025-01-15` appears exactly once and is the 46th element of the chronologically-sorted list.
- **Locked from this memo forward:** any future Phase 4bl-C run MUST use this exact list and MUST NOT add, remove, substitute, reorder, or alias any date.

---

## 5. Exact future symbol list

The future Phase 4bl-C acquisition MUST use exactly the following symbol list:

```python
SYMBOLS = ["BTCUSDT"]
```

- **Cardinality:** 1.
- **Casing:** uppercase, matching Binance's canonical futures symbol naming.
- **Locked from this memo forward:** any future Phase 4bl-C run MUST NOT add, remove, substitute, alias, or hide any additional symbol. If a future operator wishes to add ETHUSDT or any other symbol, that requires a separately authorized successor phase (Phase 4bl-B', Phase 4bm-*, or equivalent), not Phase 4bl-C.

---

## 6. Source URL pattern

### 6.1 Canonical URL pattern

The future Phase 4bl-C MUST acquire archives from the Binance public archive only, using the following deterministic URL pattern:

```
https://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/BTCUSDT-aggTrades-YYYY-MM-DD.zip
https://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/BTCUSDT-aggTrades-YYYY-MM-DD.zip.CHECKSUM
```

where `YYYY-MM-DD` is the ISO-8601 UTC date of one element of the locked 90-day list.

### 6.2 Concrete example

For the first date in the list (2024-12-01), the canonical URLs are:

```
https://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/BTCUSDT-aggTrades-2024-12-01.zip
https://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/BTCUSDT-aggTrades-2024-12-01.zip.CHECKSUM
```

For the existing fixture day (2025-01-15), the canonical URLs are:

```
https://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/BTCUSDT-aggTrades-2025-01-15.zip
https://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/BTCUSDT-aggTrades-2025-01-15.zip.CHECKSUM
```

These are the same URLs the Phase 4az acquisition resolved (see existing raw manifest `endpoint` value `data.binance.vision/data/futures/um/daily/aggTrades`).

### 6.3 Required acquisition order

For each locked date, Phase 4bl-C MUST:

1. download the `.CHECKSUM` companion file first;
2. parse the first 64 hex characters as the canonical expected SHA256;
3. then download the `.zip` archive;
4. compute the local SHA256 over the downloaded ZIP bytes;
5. verify bit-for-bit equality between the locally computed SHA256 and the parsed companion value;
6. only if equality holds, finalise the local file via atomic write-then-rename;
7. then write the paired `.sha256` sidecar in canonical Phase 4bb-F format (see §10 below).

If the `.CHECKSUM` companion is unavailable (HTTP 404), Phase 4bl-C MUST treat that date as a checksum-failure event (see §12 below) and MUST NOT trust an unverified ZIP. There is no fallback that bypasses checksum verification.

### 6.4 Allowed URL origin

The future Phase 4bl-C is allowed to contact only `data.binance.vision` over HTTPS. Any other origin (e.g., `fapi.binance.com`, `api.binance.com`, `stream.binance.com`, `vision.binance.com`, mirror sites, CDN-proxied alternatives, third-party crypto data services) is **forbidden** for Phase 4bl-C. The origin check MUST be enforced by the acquisition script before any network call is made.

### 6.5 Forbidden URL patterns

The future Phase 4bl-C MUST NOT acquire archives from:

- monthly archives (`/monthly/aggTrades/...`);
- non-aggTrades daily archives (`/daily/klines/...`, `/daily/trades/...`, `/daily/markPriceKlines/...`, `/daily/indexPriceKlines/...`, `/daily/metrics/...`);
- COIN-M Futures archives (`/data/futures/cm/...`);
- Spot archives (`/data/spot/...`);
- Options archives (`/data/option/...`);
- Any URL that includes a Binance API key, signature, listenKey, or `recvWindow` parameter.

---

## 7. Future local path layout

### 7.1 Canonical root

All Phase 4bl-C local outputs MUST live under the gitignored root `data/microstructure/`, which has been gitignored under `.gitignore:85` since Phase 4aw.

### 7.2 Raw zip path layout

Each downloaded raw zip MUST live at exactly:

```
data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/<YYYY>/<MM>/BTCUSDT-aggTrades-<YYYY-MM-DD>.zip
```

Concrete example (first locked date):

```
data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2024/12/BTCUSDT-aggTrades-2024-12-01.zip
```

The existing one-day Phase 4az artefact already lives at this exact path layout for `2025-01-15`:

```
data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip
```

### 7.3 Sidecar path layout

Each raw zip MUST have a paired SHA256 sidecar at exactly:

```
data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/<YYYY>/<MM>/BTCUSDT-aggTrades-<YYYY-MM-DD>.zip.sha256
```

Concrete example:

```
data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2024/12/BTCUSDT-aggTrades-2024-12-01.zip.sha256
```

The existing one-day Phase 4az sidecar already lives at this exact path layout for `2025-01-15`.

### 7.4 Acquisition log path

The Phase 4bl-C run MUST emit exactly one acquisition log at:

```
data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json
```

Note the `v002` suffix: this is the **second** acquisition run for `microstructure_raw_aggtrades_v001` (the first was the Phase 4az single-day acquisition, whose log is at `microstructure_raw_aggtrades_v001__v001_acquisition_log.json`). The acquisition-log filename is per-run, not per-dataset-version.

The acquisition log MUST also have a paired SHA256 sidecar at:

```
data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json.sha256
```

### 7.5 Multi-day manifest path

The Phase 4bl-C run MUST emit exactly one multi-day manifest at:

```
data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json
```

This is a **new sibling manifest**, distinct from the existing one-day manifest at `microstructure_raw_aggtrades_v001__v001.json`. The existing one-day v001 manifest MUST remain byte-identical (see §14 below).

The multi-day manifest MUST also have a paired SHA256 sidecar at:

```
data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json.sha256
```

### 7.6 Staging path layout

The Phase 4bl-C download flow MAY use a temporary staging path during atomic write-then-rename:

```
data/microstructure/staging/microstructure_raw_aggtrades_v001/BTCUSDT/<YYYY>/<MM>/<basename>.tmp
```

Staging files MUST be removed after successful finalisation. Any leftover staging file at acquisition end MUST be recorded in the acquisition log as a failed-finalisation event and MUST NOT be silently retained or treated as valid output.

### 7.7 Forbidden output paths

The future Phase 4bl-C MUST NOT write any file outside `data/microstructure/`. Specifically forbidden:

- writing to `data/raw/`, `data/normalized/`, `data/manifests/` (the pre-Phase-4ay project data paths);
- writing to `data/research/` (gitignored research outputs from other phases);
- writing to `data/derived/`, `data/labels/`, `data/features/`, `data/gate-reports/`, `data/successor-state/` (none of which exist as project paths);
- writing under `src/`, `tests/`, `scripts/`, `docs/`, `.claude/`, or any repository-root directory other than `data/microstructure/`;
- writing to absolute paths outside the repository (e.g., `C:\Users\...`, `~/...`, `/tmp/...`);
- writing to any path containing `..` or any other path-traversal pattern.

The path discipline MUST be enforced by the acquisition script before any file write is performed.

---

## 8. Multi-day manifest design

### 8.1 Overall philosophy

The Phase 4bl-C multi-day manifest is a **new sibling manifest** at `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json`. It is **not** an in-place mutation of the existing one-day v001 manifest. The two manifests coexist; both have `research_eligible: false` and `eligibility_gate_status: "pending"`.

The multi-day manifest is the canonical local index for the 90-day Phase 4bl-C acquisition. It records what was acquired, what was missing, what failed checksum, what failed decompression, what SHA256 each file has, and the full deterministic provenance (base commit SHA, code commit SHA, capture configuration hash, predeclared date list, public archive endpoint).

### 8.2 Required top-level manifest fields

The Phase 4bl-C multi-day manifest MUST contain at minimum the following top-level fields, sorted alphabetically when serialised (canonical JSON):

| Field | Type | Description |
| --- | --- | --- |
| `acquired_file_count` | int | Number of locked dates for which a verified raw zip was successfully written. |
| `acquisition_log_path` | string | Repo-relative path to the Phase 4bl-C acquisition log. |
| `acquisition_log_sha256` | string | SHA256 of the acquisition log file. |
| `base_commit_sha` | string | The `main` SHA from which Phase 4bl-B branched (`dc2240e7a43047823c8b964d52112432b7a61c79`). |
| `capture_config_hash` | string | Deterministic SHA256 hash over the locked acquisition configuration (date list + symbol list + base URL + capture mode + script version + code commit SHA). |
| `capture_mode` | string | Fixed value `"historical_archive"`. |
| `checksum_mismatch_count` | int | Number of locked dates for which the local ZIP SHA256 did not match the published `.CHECKSUM` value. |
| `code_commit_sha` | string | The repo SHA at which Phase 4bl-C is executed (set by Phase 4bl-C, not Phase 4bl-B). |
| `created_at_unix_ms` | int | UTC unix milliseconds at which the manifest was finalised. |
| `created_at_utc` | string | ISO-8601 UTC timestamp matching `created_at_unix_ms`. |
| `dataset_family` | string | Fixed value `"microstructure_raw_aggtrades_v001"`. |
| `dataset_version` | string | Fixed value `"v002"`. |
| `date_count` | int | Fixed value `90`. |
| `date_end` | string | Fixed value `"2025-02-28"`. |
| `date_list` | list[string] | Fixed list of exactly 90 ISO-8601 dates per §4 above. |
| `date_start` | string | Fixed value `"2024-12-01"`. |
| `decompression_failure_count` | int | Number of locked dates for which `unzip` / `zipfile.ZipFile.testzip()` reported a non-trivial error. |
| `eligibility_gate_status` | string | Fixed value `"pending"` (Phase 4bl-C MUST NOT flip this). |
| `endpoint` | string | Fixed value `"data.binance.vision/data/futures/um/daily/aggTrades"`. |
| `endpoint_docs_reference` | string | Fixed value `"https://github.com/binance/binance-public-data#trades (futures aggTrades daily archive convention)"`. |
| `expected_file_count` | int | Fixed value `90`. |
| `governance_labels` | object | See §8.3 below. |
| `invalid_windows` | list[object] | Empty list at acquisition time; reserved for future governed exclusions (Phase 3r §8 / Phase 4j §11 pattern). |
| `missing_file_count` | int | Number of locked dates for which the public archive returned HTTP 404 or equivalent. |
| `per_file_inventory` | list[object] | One entry per locked date; see §8.4 below. |
| `proxy_warning` | string \| null | Fixed value `null` (no proxy is used). |
| `research_eligible` | bool | Fixed value `false` (Phase 4bl-C MUST NOT flip this). |
| `retention_warning` | string \| null | Fixed value `null` (full retention; daily archives kept indefinitely). |
| `schema_version` | string | Fixed value `"v001"` (this is the v001 multi-day manifest schema; not the dataset version). |
| `source` | string | Fixed value `"binance_data_archive"`. |
| `source_class` | string | Fixed value `"public_unauthenticated_daily_archive"`. |
| `symbol_list` | list[string] | Fixed value `["BTCUSDT"]`. |
| `total_row_count` | int | Sum of `row_count` across all successfully acquired files; set by Phase 4bl-C from per-file decompression-and-line-count. |
| `total_size_bytes` | int | Sum of finalised ZIP sizes in bytes. |
| `version` | string | Fixed value `"v002"`. |

### 8.3 Required `governance_labels` block

The `governance_labels` block MUST contain exactly the following fields:

```json
{
  "feature_computation": "forbidden",
  "labels": "forbidden",
  "ml": "forbidden",
  "phase": "4bl-C",
  "source_phase_boundary": "4bl-B",
  "stop_trigger_domain": "trade_price_backtest_candidate",
  "strategy": "forbidden",
  "strategy_use": "forbidden",
  "symbol_scope_source": "archive_path",
  "validator": "phase_4ax_aggtrades_v001"
}
```

Notes:

- `phase` = `"4bl-C"` because the acquisition is performed in Phase 4bl-C, even though the design is locked in Phase 4bl-B.
- `source_phase_boundary` = `"4bl-B"` because the acquisition boundary is set by this memo.
- `validator` = `"phase_4ax_aggtrades_v001"` because Phase 4bl-C MUST use the existing Phase 4ax `validate_aggtrade_payload(...)` validator on a small sample of rows per ZIP at acquisition time (see §11.5 below), not write a new validator.
- All forbidden fields are restated explicitly: feature computation, label computation, ML, strategy work, backtesting — none authorized at acquisition time.

### 8.4 Required `per_file_inventory` schema

Each entry in `per_file_inventory` MUST contain exactly the following fields:

| Field | Type | Description |
| --- | --- | --- |
| `date` | string | ISO-8601 date, one element of the locked list. |
| `expected_url` | string | Canonical `data.binance.vision` URL per §6.1. |
| `expected_checksum_url` | string | Canonical `.CHECKSUM` URL per §6.1. |
| `local_zip_path` | string | Repo-relative path per §7.2. |
| `local_sidecar_path` | string | Repo-relative path per §7.3. |
| `status` | string | One of: `"acquired_verified"`, `"missing_404"`, `"checksum_mismatch"`, `"checksum_companion_unavailable"`, `"decompression_failure"`, `"finalisation_failure"`, `"retry_exhausted"`. |
| `sha256` | string \| null | Hex-encoded SHA256 of the finalised ZIP, or null if not acquired. |
| `sha256_from_companion` | string \| null | Hex-encoded SHA256 parsed from the `.CHECKSUM` companion file, or null if companion unavailable. |
| `size_bytes` | int \| null | Finalised ZIP size in bytes, or null if not acquired. |
| `row_count` | int \| null | Number of aggTrade rows in the decompressed CSV; null if not acquired or not decompressed. |
| `first_trade_time_ms` | int \| null | Smallest `T` (trade time) observed in the decompressed CSV; null if not acquired. |
| `last_trade_time_ms` | int \| null | Largest `T` (trade time) observed in the decompressed CSV; null if not acquired. |
| `min_agg_trade_id` | int \| null | Smallest `a` (aggregate trade id) observed; null if not acquired. |
| `max_agg_trade_id` | int \| null | Largest `a` (aggregate trade id) observed; null if not acquired. |
| `retry_count` | int | Number of retries attempted for this date (initial attempt counted as retry_count = 0). |
| `failure_reason` | string \| null | Free-text reason if `status != "acquired_verified"`; null otherwise. |
| `acquired_at_unix_ms` | int \| null | Unix milliseconds at which the local file was finalised; null if not acquired. |

### 8.5 Existing one-day fixture handling in the multi-day manifest

The `per_file_inventory` entry for `2025-01-15` MUST record the **existing** Phase 4az SHA256 and size, not a redownloaded value. Specifically:

- if the existing file at `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip` is present and its SHA256 matches the recorded Phase 4az value (`f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`), Phase 4bl-C MUST reuse the existing file in-place;
- Phase 4bl-C MUST set `status = "acquired_verified"` for the existing date;
- Phase 4bl-C MUST set `sha256 = "f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e"` (matching the existing local SHA);
- Phase 4bl-C MUST set `sha256_from_companion` to the value parsed from the freshly downloaded `.CHECKSUM` companion file (the published value should match `f560c2e5...`, but Phase 4bl-C MUST verify, not assume);
- Phase 4bl-C MUST NOT overwrite the existing file even if Binance has somehow re-published a different archive for that date with a different SHA; in that case Phase 4bl-C MUST record `status = "checksum_mismatch"`, leave the existing file untouched, and report.

The detailed relationship rule is restated in §14 below.

### 8.6 Non-authorizations recorded in the multi-day manifest

The multi-day manifest MUST embed an explicit non-authorization block (either as a top-level field `non_authorizations` or as part of `governance_labels`) that mirrors the forbidden activities listed in §11.2 and §17 of this memo. The exact field name and structure is up to Phase 4bl-C's script author; the content must be unambiguous and machine-readable.

---

## 9. Acquisition log schema

The Phase 4bl-C acquisition log at `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json` is the per-event record of the acquisition run. It is distinct from the multi-day manifest: the manifest is the index of finalised outputs; the log is the chronological record of network and disk events.

### 9.1 Required top-level acquisition log fields

| Field | Type | Description |
| --- | --- | --- |
| `acquisition_run_id` | string | UUID-like identifier for the run (e.g., `phase-4bl-c-<unix_ms>-<random>`). |
| `base_commit_sha` | string | `dc2240e7a43047823c8b964d52112432b7a61c79`. |
| `code_commit_sha` | string | Repo SHA at which Phase 4bl-C is executed. |
| `started_at_unix_ms` | int | Unix milliseconds at which Phase 4bl-C began. |
| `finished_at_unix_ms` | int | Unix milliseconds at which Phase 4bl-C finished. |
| `wall_clock_seconds` | int | `(finished_at_unix_ms - started_at_unix_ms) / 1000`. |
| `dataset_family` | string | `"microstructure_raw_aggtrades_v001"`. |
| `dataset_version` | string | `"v002"`. |
| `symbol_list` | list[string] | `["BTCUSDT"]`. |
| `date_count` | int | `90`. |
| `date_list` | list[string] | The locked 90-date list. |
| `events` | list[object] | Per-event log, see §9.2 below. |
| `summary` | object | Aggregate summary, see §9.3 below. |

### 9.2 Required per-event schema

Each event in `events` MUST contain at minimum:

| Field | Type | Description |
| --- | --- | --- |
| `timestamp_unix_ms` | int | When the event occurred. |
| `event_type` | string | One of: `"download_checksum_start"`, `"download_checksum_success"`, `"download_checksum_404"`, `"download_zip_start"`, `"download_zip_success"`, `"checksum_match"`, `"checksum_mismatch"`, `"checksum_companion_unavailable"`, `"decompression_test_start"`, `"decompression_test_success"`, `"decompression_failure"`, `"row_sample_validation_start"`, `"row_sample_validation_success"`, `"row_sample_validation_failure"`, `"sidecar_write"`, `"finalisation_success"`, `"finalisation_failure"`, `"retry_attempted"`, `"date_skipped_existing_fixture"`, `"date_status_recorded"`. |
| `date` | string | Affected date (ISO-8601), or `"all"` for run-level events. |
| `details` | object | Free-form structured details (URL, HTTP status, byte count, SHA values, error string). |

### 9.3 Required summary block

The summary MUST contain at minimum:

```json
{
  "expected_file_count": 90,
  "acquired_file_count": <int>,
  "missing_file_count": <int>,
  "checksum_mismatch_count": <int>,
  "decompression_failure_count": <int>,
  "row_sample_validation_failure_count": <int>,
  "total_size_bytes": <int>,
  "total_row_count": <int>,
  "existing_fixture_reused": <bool>,
  "existing_fixture_sha_match": <bool>,
  "non_authorizations_preserved": true,
  "research_eligible_after_acquisition": false,
  "eligibility_gate_status_after_acquisition": "pending"
}
```

### 9.4 Acquisition log immutability

The acquisition log is **append-only during the run** and **immutable after the run**. Phase 4bl-C MUST write the acquisition log atomically (write to `*.tmp` first, then `os.replace` to the final path). Phase 4bl-C MUST NOT modify the acquisition log after finalisation.

---

## 10. Hash and sidecar rules

### 10.1 SHA256 algorithm

All SHA256 hashes MUST be computed with the standard library `hashlib.sha256()` (no third-party hash library). Hash values MUST be reported as **lowercase hex** (64 characters, no leading `0x`, no whitespace).

### 10.2 Chunked reads

Files MUST be hashed in chunked reads (recommended chunk size: 1 MiB = 1048576 bytes) to avoid loading large ZIPs into memory. The chunk size is an implementation detail; it must not affect the hash value.

### 10.3 Sidecar format

Each `.sha256` sidecar file MUST have **exactly** the following byte content (Phase 4bb-F canonical format):

```
<sha256_lowercase_hex>  <basename>\n
```

with:

- exactly two ASCII spaces between the hash and the basename;
- the basename is the file basename only (no directory components);
- a single trailing LF newline (`\n`, byte `0x0A`);
- no BOM, no CRLF, no leading whitespace.

Concrete example for the first locked date:

```
<64-hex-chars>  BTCUSDT-aggTrades-2024-12-01.zip\n
```

The sidecar format is compatible with the `sha256sum` standard format.

### 10.4 Refuse-overwrite

Every file write (raw zip, sidecar, manifest, log) MUST refuse to overwrite an existing file unless the existing file is byte-identical to the new content. Specifically:

- if the target file does not exist: write atomically and proceed;
- if the target file exists and its SHA256 matches the new content: skip the write (no-op);
- if the target file exists and its SHA256 differs from the new content: **refuse** to overwrite. Record the conflict in the acquisition log and the manifest's `per_file_inventory[].failure_reason`. Do not silently overwrite or rename.

The one explicit exception is the multi-day manifest itself: if Phase 4bl-C is re-run from a partial state, it MAY update its own `__v002.json` manifest in place at the end of the run, but only via atomic write-then-rename, and only with the run's authoritative new content.

### 10.5 Atomic write-then-rename

All file writes MUST use atomic write-then-rename:

1. Write content to `<target>.tmp` in the same directory.
2. Flush + fsync (where supported).
3. `os.replace(<target>.tmp, <target>)`.

The atomic write-then-rename pattern guarantees that no half-written file exists at the canonical path. Any leftover `*.tmp` file at run end MUST be treated as a failed-finalisation event and recorded in the log.

### 10.6 Sidecar verification on existing artefacts

For the existing one-day Phase 4az fixture (`2025-01-15`), Phase 4bl-C MUST:

1. read the existing `.zip` and compute its SHA256;
2. verify it matches `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`;
3. read the existing `.zip.sha256` sidecar and verify its content matches the canonical format and the computed hash;
4. if any of these checks fail, set `status = "finalisation_failure"` for that date and do NOT modify the existing files.

This is a read-only verification of existing artefacts. Phase 4bl-C MUST NOT rewrite an existing sidecar even if the canonical format is somehow different from what's already on disk.

---

## 11. Future Phase 4bl-C execution boundaries

This section is the operational contract that any future Phase 4bl-C execution phase MUST honor. Phase 4bl-B locks this; Phase 4bl-C may not relax it.

### 11.1 Allowed surface

The future Phase 4bl-C is allowed to:

- create one new standalone script at `scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py` (or an equivalent filename per the Phase 4bl-C authorization prompt), modeled on `scripts/phase4az_acquire_btcusdt_aggtrades_archive.py`;
- import only Python standard library modules plus the existing Phase 4ax / 4aw scaffold (`from prometheus.research.microstructure.aggtrades import validate_aggtrade_payload, AggTradeValidationError, TakerSide`);
- read the locked 90-date list from this memo (the script MAY hard-code the list, or generate it deterministically from `date_start` / `date_end` constants; either is acceptable as long as the result is exactly the §4 list);
- download exactly the 90 `.CHECKSUM` companion files from `data.binance.vision`;
- download exactly the 90 raw aggTrades `.zip` files from `data.binance.vision`;
- compute SHA256 over each downloaded ZIP and verify against the parsed companion value;
- write exactly 90 raw zip files (or fewer, in case of acquisition failures recorded per §12) to `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/<YYYY>/<MM>/...`;
- write exactly 90 paired `.sha256` sidecars (or fewer, matching the number of acquired ZIPs) to the corresponding paths;
- write exactly one acquisition log at `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json` + its paired sidecar;
- write exactly one multi-day manifest at `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json` + its paired sidecar;
- verify the existing one-day Phase 4az artefacts byte-identically (read-only);
- decompress each ZIP **once** to a temporary in-memory or on-disk staging location for the limited purpose of (a) verifying the ZIP is non-corrupt via `zipfile.ZipFile.testzip()`, (b) sampling a small number of rows (e.g., first 100 rows, last 100 rows, 100 random middle rows) to validate against `validate_aggtrade_payload(...)`, (c) computing `row_count`, `first_trade_time_ms`, `last_trade_time_ms`, `min_agg_trade_id`, `max_agg_trade_id` for the manifest;
- emit a Phase 4bl-C docs report and closeout under `docs/00-meta/implementation-reports/`;
- verify all preserved invariants (existing Phase 4az / 4bb / 4bc / 4bd / 4be / 4bf / 4bg / 4bh / 4bi / 4bj artefact SHAs unchanged pre/post).

### 11.2 Forbidden surface

The future Phase 4bl-C MUST NOT:

- normalize raw aggTrades into a derived Parquet family (Phase 4bd was the normalization phase for the one-day fixture; Phase 4bl-C does **not** normalize multi-day data);
- compute features (Phase 4bh and successors);
- compute labels (Phase 4bj-C and successors);
- run any eligibility gate (raw / derived / feature / label);
- create any successor-state artefact;
- run any diagnostic, including Q1–Q7, Phase 3s diagnostics, Phase 4bj-K label diagnostics, or any new diagnostic;
- compute any descriptive statistic, summary, distribution, ratio, return, or aggregate beyond the per-file `row_count` / `first_trade_time_ms` / `last_trade_time_ms` / `min_agg_trade_id` / `max_agg_trade_id` strictly required for the manifest;
- compute PnL, MFE, MAE, R-multiple, equity, position-state, alpha, edge, prediction, model-score, decision-score, entry-exit, signal, or strategy output;
- train any ML model, evaluate any predictive metric, perform any feature ranking, or perform any meta-labeling;
- create any strategy, run any backtest, or produce any backtest result;
- use authenticated APIs, private endpoints, public-endpoint calls in code (`fapi.binance.com`, `api.binance.com`, etc.), user streams, WebSockets, listenKey lifecycle, MCP, Graphify, `.mcp.json`, or any credential;
- contact any origin other than `data.binance.vision` over HTTPS;
- modify any existing manifest (raw / derived / feature / label / gate-report / successor-state);
- modify any existing source / test / script / `pyproject.toml` / `README.md` / `.gitignore` / MCP file beyond the narrow `scripts/phase4bl_c_*.py` addition and the narrow `current-project-state.md` update;
- flip `research_eligible` on any manifest;
- transition `eligibility_gate_status` on any manifest;
- change `chronological_split_policy` on any manifest;
- modify project locks, retained verdicts, M0 governance, the post-null cooldown rule, the cooled-down families list, the Phase 4al refined no-rescue rule, or the Phase 4bb-F canonical path policy;
- delete, move, copy, or rename any existing `data/microstructure/` artefact;
- commit any `data/microstructure/` artefact to git (all outputs must be gitignored; see §13 below);
- authorize Phase 4bl-D, Phase 4bl-E, any Phase 4bm-* / 4bn-* / 4bo-* / 4bp-* / 4bq-* successor, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, production keys, or any successor phase.

### 11.3 Stop-conditions

The future Phase 4bl-C MUST fail-closed and halt the run in any of the following cases:

- any module imported by the script reaches outside the standard library or the Phase 4ax / 4aw scaffold (static import-boundary scan, similar to Phase 4ax `test_import_boundaries.py`);
- any URL contacted is not under `data.binance.vision` over HTTPS;
- any credential is read, generated, or referenced;
- any `.env` file is read;
- any MCP / Graphify / `.mcp.json` is touched;
- the existing one-day Phase 4az raw zip SHA256 does not match the recorded value `f560c2e5...`;
- the existing one-day Phase 4az raw manifest SHA256 does not match its recorded value (pre/post integrity must hold);
- the locked 90-date list cannot be generated deterministically;
- any output path resolves outside `data/microstructure/`;
- any output file overwrite is attempted with non-identical content;
- the acquisition log cannot be written atomically;
- the multi-day manifest cannot be written atomically;
- the acquired-file count is zero (i.e., every date failed — likely a network / DNS / archive-outage condition);
- any forbidden activity (normalization / features / labels / gates / diagnostics / ML / strategy / backtest / authenticated API / private endpoint) is attempted by the script.

In every stop-condition case, Phase 4bl-C MUST leave the repository in a state that does not require manual cleanup, and MUST emit a docs report explaining the stop-condition.

### 11.4 Re-run policy

Phase 4bl-C MAY be re-run by the operator at a later date (e.g., if a transient network issue caused a partial first run). On re-run:

- the multi-day manifest at `microstructure_raw_aggtrades_v001__v002.json` MUST be updated in place via atomic write-then-rename, reflecting the new authoritative state of the 90 dates;
- the acquisition log SHOULD be rolled to a fresh file with a new `acquisition_run_id` (the old log is preserved on disk; it is not deleted);
- previously-acquired files with matching SHA256 MUST be reused in place (no redownload);
- previously-failed dates MAY be retried;
- the Phase 4bl-C script MUST be deterministic: a fully successful first run followed by a re-run on the same machine and code commit SHA MUST produce the same multi-day manifest content (the only fields that may change are `created_at_unix_ms`, `created_at_utc`, and the `acquisition_log_*` references).

### 11.5 Row-sample validation policy

For each successfully-downloaded ZIP, Phase 4bl-C MUST run a small row-sample validation:

- decompress the ZIP to a temporary in-memory buffer or staging file;
- parse the CSV header (if any; Binance aggTrades dailies are conventionally headerless, with columns `[a, p, q, f, l, T, m]` per Phase 4ax `validate_aggtrade_payload`);
- sample at most 300 rows (first 100, last 100, 100 random middle rows);
- for each sampled row, pass it through the existing `validate_aggtrade_payload(...)` function;
- if any sampled row fails validation, set `status = "row_sample_validation_failure"` for that date and increment `row_sample_validation_failure_count` in the acquisition-log summary;
- do **not** run validation on every row of every ZIP at acquisition time — the Phase 4bl-C scope is acquisition, not full per-row validation. Full per-row validation would be a separately authorized future Phase 4bl-D or equivalent gate phase.

The row-sample validation is a fail-fast smoke check, not a comprehensive integrity gate. The Phase 4az `eligibility_gate` (which IS comprehensive) is run later by a separately authorized future gate phase, not by Phase 4bl-C.

### 11.6 Determinism requirements

Phase 4bl-C MUST be deterministic on the locked inputs:

- the date list is deterministic;
- the URL pattern is deterministic;
- the local path layout is deterministic;
- the SHA256 algorithm is deterministic;
- the sidecar format is deterministic;
- the multi-day manifest schema is deterministic;
- the random-row sampling MAY use a fixed seed (e.g., `random.seed(<integer-derived-from-date-string>)`) so that re-running the same script on the same input produces the same sampled-row set.

### 11.7 No silent activity

The future Phase 4bl-C MUST log every download attempt, every checksum verification, every decompression test, every row-sample validation, every sidecar write, every manifest write, and every retry. The acquisition log is the canonical record. No event may be silently dropped.

---

## 12. Failure / retry / missing-file policy

### 12.1 Retry policy

For each date, Phase 4bl-C MUST attempt download with the following retry discipline:

- **Maximum retries:** 3 per date (initial attempt counted as retry_count = 0; retries are retry_count = 1, 2, 3).
- **Backoff:** exponential, starting at 2 seconds, doubling each retry (2s, 4s, 8s). The script MAY add a small random jitter (up to ±25%) to avoid thundering-herd behavior.
- **Per-date timeout:** 60 seconds per attempt (network read timeout).
- **Total per-date wallclock budget:** 5 minutes (300 seconds) including retries and backoff.

If the date's checksum companion or ZIP cannot be acquired within the per-date budget, Phase 4bl-C MUST record the date with `status = "retry_exhausted"` and continue to the next date. The run is not aborted by a single date failure.

### 12.2 HTTP 404 policy

If the `.zip` or `.CHECKSUM` URL returns HTTP 404, Phase 4bl-C MUST:

- record `status = "missing_404"` (for the zip) or `status = "checksum_companion_unavailable"` (for the checksum);
- increment `missing_file_count` in the manifest;
- NOT retry on 404 (it's a permanent condition);
- continue to the next date.

If the public archive returns 404 for a recent date, the operator may legitimately wait until the daily archive is published (Binance typically publishes daily archives within ~24 hours of UTC day-end). The Phase 4bl-C run records the 404 verbatim and reports it; it does not silently retry forever or block the entire run.

### 12.3 HTTP 5xx / network error policy

For transient HTTP 5xx errors, DNS failures, TCP resets, TLS errors, and other transient network failures:

- Phase 4bl-C MUST retry per §12.1 above;
- after retry exhaustion, the date is recorded with `status = "retry_exhausted"`.

### 12.4 Checksum mismatch policy

If the locally computed SHA256 over the downloaded ZIP does not match the value parsed from the published `.CHECKSUM` companion, Phase 4bl-C MUST:

- record `status = "checksum_mismatch"`;
- increment `checksum_mismatch_count` in the manifest;
- **NOT** retry (a checksum mismatch is not a transient condition; it indicates either upstream corruption or a Binance-side republish);
- delete the staged ZIP (it is untrusted);
- continue to the next date.

### 12.5 Decompression failure policy

If `zipfile.ZipFile.testzip()` reports a non-trivial error on a downloaded ZIP that otherwise passed checksum verification:

- record `status = "decompression_failure"`;
- increment `decompression_failure_count`;
- preserve the finalised ZIP on disk (it is checksum-valid; the failure is reported via the manifest);
- continue to the next date.

### 12.6 Row-sample validation failure policy

If any sampled row fails `validate_aggtrade_payload(...)`:

- record `status = "row_sample_validation_failure"`;
- increment `row_sample_validation_failure_count` in the acquisition log summary;
- preserve the finalised ZIP on disk;
- continue to the next date.

### 12.7 No silent skipping

Phase 4bl-C MUST NOT silently skip any date. Every locked date MUST appear in the multi-day manifest's `per_file_inventory` and the acquisition log's `events`, with explicit `status` and `failure_reason` (if any). A skipped date with no record is a failure-closed condition that MUST halt the run.

### 12.8 No replacement dates

Phase 4bl-C MUST NOT substitute a different date for a failed date. The 90-date list is locked. If a date fails, the failure is recorded; the list is not modified.

### 12.9 No fallback to APIs

Phase 4bl-C MUST NOT fall back to authenticated REST APIs (e.g., `fapi.binance.com /fapi/v1/aggTrades`), private endpoints, or any other Binance API. The public archive is the only allowed source. If the public archive is unavailable, the date is recorded as missing.

### 12.10 Partial completion policy

A Phase 4bl-C run is considered **complete** if the multi-day manifest is finalised, regardless of how many dates were successfully acquired. A run with 88 acquired and 2 missing is a complete run with 2 recorded failures; it is NOT a "failed run" overall. The operator decides whether the acquired-count is sufficient for any future successor phase (Phase 4bl-D, etc.); Phase 4bl-C itself does not gate on the acquired-count.

A Phase 4bl-C run is considered **incomplete** only if the multi-day manifest was not finalised (e.g., the script crashed before atomic-write of the manifest). In that case, the operator may re-run Phase 4bl-C; previously acquired files are reused per §11.4.

### 12.11 Minimum acceptable acquired-file-count

Phase 4bl-B does not lock a minimum acquired-file-count; that is a successor decision. However, Phase 4bl-B notes that:

- if `acquired_file_count < 80` (i.e., more than 10 of the 90 dates failed), the operator SHOULD investigate before authorizing any successor phase;
- if `acquired_file_count < 60`, the operator SHOULD treat the acquisition as effectively failed and authorize either a Phase 4bl-C re-run or a separately authorized rescope memo.

These are operator-guidance thresholds, not gate conditions. Phase 4bl-C records the count and reports; the operator decides.

---

## 13. Gitignore and commit policy

### 13.1 Existing gitignore coverage

The repository has gitignored `data/microstructure/` since Phase 4aw (`.gitignore` line 85). All Phase 4bl-C outputs under `data/microstructure/` are therefore gitignored by default.

### 13.2 Per-output-class verification

Phase 4bl-C MUST verify gitignore coverage for each output path it intends to write **before** writing. Specifically, for each of:

- raw zip path;
- sidecar path;
- multi-day manifest path;
- multi-day manifest sidecar path;
- acquisition log path;
- acquisition log sidecar path;
- staging path;

Phase 4bl-C MUST call `git check-ignore --verbose <path>` and verify the result indicates the path is gitignored. If any path is not gitignored, Phase 4bl-C MUST halt the run as a fail-closed stop-condition (see §11.3 above).

### 13.3 Phase 4bl-C commits docs only

The tracked commits of Phase 4bl-C MUST contain only:

- one new standalone script at `scripts/phase4bl_c_*.py`;
- optionally: one new test file at `tests/research/microstructure/test_phase4bl_c_*.py` (modeled on `test_phase4az_archive_acquisition.py`), containing offline tests that use pytest `tmp_path` only and that do NOT make any network call (no live downloads in CI);
- one new docs file at `docs/00-meta/implementation-reports/<DATE>_phase-4bl-c_*.md`;
- one new docs closeout at `docs/00-meta/implementation-reports/<DATE>_phase-4bl-c_closeout.md`;
- a narrow update to `docs/00-meta/current-project-state.md` (Phase 4bl-C narrative paragraph + new "Current phase:" block).

**No `data/microstructure/` artefact is committed.** Phase 4bl-C's local outputs are visible only on the operator's machine and are reproducible by re-running the script from the public archive.

### 13.4 No widening of gitignore

Phase 4bl-C MUST NOT widen `.gitignore` (i.e., MUST NOT add entries that hide more files). The existing `data/microstructure/` line is sufficient.

### 13.5 No narrowing of gitignore

Phase 4bl-C MUST NOT narrow `.gitignore` (i.e., MUST NOT remove or weaken the existing `data/microstructure/` rule). The existing gitignore coverage is binding.

### 13.6 `.gitattributes` (if any) is unchanged

Phase 4bl-C MUST NOT modify `.gitattributes` (if it exists). Line-ending policy is unchanged.

---

## 14. Relationship to the existing one-day fixture

### 14.1 Existing one-day Phase 4az artefacts are sacrosanct

The existing one-day Phase 4az artefacts MUST remain **byte-identical** before, during, and after the Phase 4bl-C run. Specifically:

| Artefact | Path | Pre-run SHA256 | Post-run SHA256 | Invariant |
| --- | --- | --- | --- | --- |
| Raw zip | `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip` | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | (same) | byte-identical |
| Raw sidecar | `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256` | (recorded by Phase 4az) | (same) | byte-identical |
| Raw v001 manifest | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json` | (recorded by Phase 4az) | (same) | byte-identical |
| Raw v001 manifest sidecar | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json.sha256` | (recorded by Phase 4az) | (same) | byte-identical |
| Phase 4az acquisition log | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001_acquisition_log.json` | (recorded by Phase 4az) | (same) | byte-identical |
| Phase 4az gate report | `data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json` | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` | (same) | byte-identical |

(Same byte-identical invariant applies to every other already-recorded artefact in the Phase 4bb / 4bc / 4bd / 4be / 4bf / 4bg / 4bh / 4bi / 4bj chains. The complete list is verifiable via the per-phase memo SHAs.)

### 14.2 Existing fixture is part of the locked 90-day range

The existing `2025-01-15` fixture is element 46 of the locked 90-date list. Phase 4bl-C must therefore handle the existing-file-overlap case explicitly:

- Phase 4bl-C MUST detect the existing fixture at the canonical path `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip`;
- Phase 4bl-C MUST compute its SHA256 fresh (not trust the existing sidecar blindly);
- Phase 4bl-C MUST compare the fresh local SHA to the recorded Phase 4az value `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`;
- if they match, Phase 4bl-C MUST also download the fresh `.CHECKSUM` companion from `data.binance.vision`, parse its value, and verify it matches the recorded Phase 4az value;
- if all three values match (recorded + fresh-local + fresh-companion), Phase 4bl-C MUST reuse the existing file in place (no redownload of the zip itself);
- Phase 4bl-C MUST emit a `date_skipped_existing_fixture` event in the acquisition log;
- Phase 4bl-C MUST record `status = "acquired_verified"` and `retry_count = 0` for that date in the multi-day manifest.

### 14.3 Conflict handling

If at any point during §14.2 the values disagree (i.e., Binance has somehow republished a different aggTrades archive for `2025-01-15` with a different SHA, or local corruption has occurred):

- Phase 4bl-C MUST NOT overwrite the existing local file;
- Phase 4bl-C MUST record `status = "checksum_mismatch"` for that date;
- Phase 4bl-C MUST log the conflict in detail (recorded SHA, fresh-local SHA, fresh-companion SHA, all three);
- the operator MUST investigate before authorizing any future use of the multi-day dataset.

Phase 4bl-C MUST NOT silently overwrite the existing fixture, even if it appears the upstream archive has been corrected or updated. The existing fixture is the canonical Phase 4az artefact and is byte-locked.

### 14.4 v001 manifest is NOT modified

The existing one-day v001 manifest at `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json` MUST NOT be modified by Phase 4bl-C. The multi-day acquisition uses a **new sibling** v002 manifest at `microstructure_raw_aggtrades_v001__v002.json`. The two manifests coexist; both have `research_eligible: false` / `eligibility_gate_status: "pending"`.

This sibling-manifest pattern preserves the Phase 4bb-E / 4bg-B / 4bi-D / 4bj-G / 4bb-G governance convention: existing locked artefacts are never mutated; new governance state is recorded via sibling artefacts.

### 14.5 Phase 4az gate report is NOT modified

The existing Phase 4az gate report (`microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json`) MUST NOT be modified or referenced as if it covers the multi-day acquisition. The Phase 4az gate report is for the one-day v001 manifest only. The future multi-day v002 manifest will have its own future gate report under a separately authorized future Phase 4bl-D-equivalent eligibility-gate phase (not authorized by Phase 4bl-B).

---

## 15. Phase ladder after Phase 4bl-B

This section enumerates the hypothetical future phase ladder after Phase 4bl-B. **None of these phases are authorized by Phase 4bl-B.** Each requires separate operator authorization.

| Phase | Name | Type | Scope | Authorized by Phase 4bl-B? |
| --- | --- | --- | --- | --- |
| Phase 4bl-C | Multi-Day aggTrades Acquisition Execution | docs-and-code | Execute the design locked by Phase 4bl-B; produce gitignored multi-day raw artefacts. | NO |
| Phase 4bl-D | Multi-Day Raw Manifest Eligibility Gate | docs-and-code | Implement a v002-multi-day eligibility gate analogous to Phase 4bb-C / 4bb-D; produce gate report. | NO |
| Phase 4bl-E | Multi-Day Raw Manifest Successor-State Recording | docs-and-local-gitignored-output | Sibling successor-state artefact per Phase 4bb-G pattern. | NO |
| Phase 4bm-A | Multi-Day Derived (Normalized) Family Design Memo | docs-only | Multi-day analog of Phase 4bc. | NO |
| Phase 4bm-B | Multi-Day Derived Family Implementation | docs-and-code | Multi-day analog of Phase 4bd. | NO |
| Phase 4bm-C | Multi-Day Derived Structural QA Memo | docs-only | Multi-day analog of Phase 4be. | NO |
| Phase 4bm-D | Multi-Day Derived Eligibility Gate | docs-and-code | Multi-day analog of Phase 4bf. | NO |
| Phase 4bm-E | Multi-Day Derived Successor-State | docs-and-local-gitignored-output | Multi-day analog of Phase 4bg-B. | NO |
| Phase 4bn-A | Multi-Day Feature-Boundary Design Memo | docs-only | Multi-day analog of Phase 4bh-A. | NO |
| Phase 4bn-B | Multi-Day Feature Schema Finalization | docs-only | Multi-day analog of Phase 4bh-B. | NO |
| Phase 4bn-C | Multi-Day Feature Implementation | docs-and-code | Multi-day analog of Phase 4bh. | NO |
| Phase 4bn-D | Multi-Day Feature Eligibility Gate | docs-and-code | Multi-day analog of Phase 4bi-B. | NO |
| Phase 4bn-E | Multi-Day Feature Successor-State | docs-and-local-gitignored-output | Multi-day analog of Phase 4bi-D. | NO |
| Phase 4bo-A | Multi-Day Label Boundary / Target Definition | docs-only | Multi-day analog of Phase 4bj-A. | NO |
| Phase 4bo-B | Multi-Day Label Schema Finalization | docs-only | Multi-day analog of Phase 4bj-B. | NO |
| Phase 4bo-C | Multi-Day Label Implementation | docs-and-code | Multi-day analog of Phase 4bj-C. | NO |
| Phase 4bo-D | Multi-Day Label Eligibility Gate | docs-and-code | Multi-day analog of Phase 4bj-E. | NO |
| Phase 4bo-E | Multi-Day Label Successor-State | docs-and-local-gitignored-output | Multi-day analog of Phase 4bj-G. | NO |
| Phase 4bp-A | Multi-Day Label Diagnostic Study Plan | docs-only | Multi-day analog of Phase 4bj-K. | NO |
| Phase 4bp-B | Multi-Day Label Diagnostic Study Execution | analysis-and-docs | Multi-day descriptive label diagnostics (single-day cell would be replaced by multi-day cell). | NO |
| Phase 4bq-A | Multi-Day Chronological Split Policy Design | docs-only | Multi-day analog of Phase 4bj-I; would propose formal train / validation / test partitioning across the 90-day cell. | NO |
| Phase 4bq-B | Multi-Day Split Artefact Recording | docs-and-local-gitignored-output | Multi-day analog of Phase 4bj-J's no-split-determination recording, but reasonably proposing a formal split. | NO |
| Future | ML feasibility memo | docs-only | Feasibility of ML on the multi-day governed cell. | NO |
| Future | Baseline ML diagnostic | docs-and-code | Baseline ML model on the multi-day cell (linear / tree / nearest-baseline). | NO |
| Future | Failure interpretation / fallback selection | docs-only | If baseline ML fails M0 admissibility. | NO |
| Future | Strategy hypothesis under M0 | docs-only | A new strategy hypothesis cleared by M0, using the multi-day evidence as one input. | NO |
| Future | Strategy spec | docs-only | Concrete strategy specification. | NO |
| Future | Backtest plan | docs-only | Predeclared backtest methodology. | NO |
| Future | Backtest execution | docs-and-code | Run the backtest. | NO |
| Future | Paper / shadow | docs-and-runtime | Live observation without exchange-write. | NO |
| Future | Live-readiness | docs-and-runtime | Pre-live gates. | NO |
| Future | Live | runtime | Real exchange-write. | NO |

**Recommended operator decision after Phase 4bl-B merges:** authorize Phase 4bl-C execution as a separate prompt. Phase 4bl-C is the natural next step. Phase 4bl-B explicitly does NOT authorize it.

---

## 16. M0 and no-rescue integration

### 16.1 M0 mechanism-admissibility gate

Phase 4bl-B does **not** propose or admit any new strategy hypothesis. The M0 twelve-clause gate (adopted by Phase 4ak) therefore does **not** trigger for Phase 4bl-B. The M0 gate is a strategy-hypothesis-level gate; Phase 4bl-B is a data-acquisition-design memo.

Phase 4bl-B is, however, upstream of any future ML / strategy / backtest work that would invoke M0. Phase 4bl-B locks the data scope (BTCUSDT, 90 days, public aggTrades) so that any future M0-cleared hypothesis has a clean, deterministic data substrate.

### 16.2 Post-null cooldown rule

Phase 4bl-B is **not** an attempt to revive any of the six cooled-down failed strategies (R2 / F1 / D1-A / V2 / G1 / C1). It is a data-acquisition-design memo that expands the governed substrate from one day to 90 days, BTCUSDT-only. No strategy revival is implied.

The six families remain terminally HARD REJECT / FAILED — §11.6 / FRAMEWORK FAIL on their first-spec evidence, and Phase 4bl-B does not propose to re-evaluate any of them on the expanded substrate. Any such re-evaluation would itself require a separately authorized memo that explicitly addresses the post-null cooldown rule and demonstrates an entirely new mechanism (not a parameter sweep on the failed families).

### 16.3 Phase 4al refined no-rescue rule

Phase 4bl-B explicitly preserves the Phase 4al refined no-rescue rule. The acquired multi-day data MUST NOT be used in any future phase to:

- re-tune any of the six failed strategies on more data;
- re-fit any threshold or filter that was previously fit on the one-day cell;
- re-evaluate any of the six failed strategies under cherry-picked sub-windows of the 90-day range;
- "rescue" any failed hypothesis by appealing to the larger evidence base.

The 90-day acquisition is for **forward** research only — new hypotheses, new ML feasibility, new descriptive diagnostics, all gated by M0 on the forward path.

### 16.4 Phase 4bb-F canonical path policy

Phase 4bl-B explicitly preserves the Phase 4bb-F canonical path policy:

- raw zips at `data/microstructure/raw/<family>/<SYMBOL>/<YYYY>/<MM>/...`;
- manifests at `data/microstructure/manifests/<family>__<version>.json`;
- gate reports at `data/microstructure/gate-reports/<family-subdir>/...` (raw subdir is `gate-reports/` itself by Phase 4bb-D / 4bb-F precedent; multi-day successor would use the same pattern);
- successor-state at `data/microstructure/successor-state/...`;
- paired sidecars in canonical `<sha256>  <basename>\n` format.

### 16.5 Phase 4aw `flip_research_eligible(...)` always-raises invariant

Phase 4bl-B explicitly preserves the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant. The future Phase 4bl-C MUST NOT invoke this method; the future Phase 4bl-D-equivalent eligibility gate MAY only invoke it after explicit eligibility-gate authorization, which Phase 4bl-B does NOT grant.

### 16.6 Cooled-down families list unchanged

The Phase 4ak cooled-down families list is unchanged by Phase 4bl-B:

- R2 (Phase 3c §7.3) — cooled down;
- F1 (Phase 3i) — cooled down;
- D1-A (Phase 3j) — cooled down;
- V2 (Phase 4l) — cooled down;
- G1 (Phase 4r) — cooled down;
- C1 (Phase 4x) — cooled down;
- 5m thread (Phase 3t) — operationally closed;
- microstructure-flavored breakout / pullback / mean-reversion / regime / VRP families (per Phase 4al §14 hierarchy) — cooled down absent fresh M0 evidence.

---

## 17. Explicit non-authorizations

Phase 4bl-B explicitly does **NOT** authorize any of the following. Each line is an authoritative non-authorization that any future implementer (Claude Code or human) must respect.

- Phase 4bl-B does NOT authorize Phase 4bl-C execution. Phase 4bl-C requires a separate authorization prompt.
- Phase 4bl-B does NOT authorize any download. No `data.binance.vision` URL is contacted by Phase 4bl-B.
- Phase 4bl-B does NOT authorize creation of any `data/microstructure/` artefact. No raw zip, no sidecar, no manifest, no log, no gate report, no successor-state, no staging file is created by Phase 4bl-B.
- Phase 4bl-B does NOT authorize modification of any existing `data/microstructure/` artefact.
- Phase 4bl-B does NOT authorize creation or modification of any source code, test, script, or runtime configuration. The standalone script `scripts/phase4bl_c_*.py` is described in this memo but is NOT created by Phase 4bl-B; it will be created by a future Phase 4bl-C.
- Phase 4bl-B does NOT authorize creation or modification of `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, MCP files, or any repo-level configuration.
- Phase 4bl-B does NOT authorize normalization, derivation, feature computation, label computation, ML training, strategy creation, signal generation, backtesting, paper trading, shadow trading, live trading, or exchange-write activity of any kind.
- Phase 4bl-B does NOT authorize creation of any successor-state artefact.
- Phase 4bl-B does NOT authorize creation of any eligibility-gate artefact.
- Phase 4bl-B does NOT authorize creation of any diagnostic, descriptive-statistic, or summary artefact.
- Phase 4bl-B does NOT authorize use of authenticated Binance APIs, private endpoints, public REST endpoints (`fapi.binance.com`, `api.binance.com`), user streams, WebSockets, listenKey lifecycle, MCP, Graphify, `.mcp.json`, or any credential.
- Phase 4bl-B does NOT authorize flipping `research_eligible` on any manifest or transitioning `eligibility_gate_status` on any manifest.
- Phase 4bl-B does NOT authorize changing `chronological_split_policy` on any manifest.
- Phase 4bl-B does NOT authorize Phase 4 canonical, Phase 5, or any successor phase.
- Phase 4bl-B does NOT authorize modification of any project lock, retained verdict, M0 governance, post-null cooldown rule, cooled-down families list, Phase 4al refined no-rescue rule, Phase 4bb-F canonical path policy, or Phase 4aw `flip_research_eligible` always-raises invariant.
- Phase 4bl-B does NOT authorize creation or modification of any TradingView-style chart, dashboard, or operator-facing visualization.
- Phase 4bl-B does NOT authorize live order placement, paper/shadow trading, exchange-write, production-key creation, authenticated APIs, private endpoints, user stream, live WebSocket implementation, MCP, Graphify, `.mcp.json`, credentials, or any live capability.

---

## 18. Retained verdict ledger (verbatim)

The following retained verdicts are preserved verbatim through Phase 4bl-B:

- **H0** — FRAMEWORK ANCHOR (Phase 2i §1.7.3). Preserved verbatim.
- **R3** — BASELINE-OF-RECORD (Phase 2p §C.1). Preserved verbatim.
- **R1a** — RETAINED — NON-LEADING (Phase 2m). Preserved verbatim.
- **R1b-narrow** — RETAINED — NON-LEADING (Phase 2s). Preserved verbatim.
- **R2** — FAILED — §11.6 cost-sensitivity blocks (Phase 2w §16.1). Preserved verbatim.
- **F1** — HARD REJECT (Phase 3c §7.3 catastrophic-floor predicate; Phase 3d-B2 terminal). Preserved verbatim.
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL — other (Phase 3h §11.2; Phase 3j terminal). Preserved verbatim.
- **5m thread** — OPERATIONALLY CLOSED (Phase 3t). Preserved verbatim.
- **V2** — HARD REJECT — terminal for V2 first-spec (Phase 4l, structural CFP-1 critical). Preserved verbatim.
- **G1** — HARD REJECT — terminal for G1 first-spec (Phase 4r, CFP-1 critical binding; CFP-9 independent). Preserved verbatim.
- **C1** — HARD REJECT — terminal for C1 first-spec (Phase 4x, CFP-2 binding; CFP-3 / CFP-6 co-binding). Preserved verbatim.

No retained verdict is revised by Phase 4bl-B. No retained verdict is silently reframed by Phase 4bl-B. No retained verdict is re-evaluated on the prospective multi-day substrate by Phase 4bl-B.

---

## 19. Preserved locks (verbatim)

The following project locks are preserved verbatim through Phase 4bl-B:

- **§11.6 cost lock** — HIGH cost = 8 bps slippage per side; round-trip = 16 bps slippage. Preserved verbatim.
- **§1.7.3 project-level locks** — 0.25% risk per trade; 2× leverage cap; one position max; mark-price stops. Preserved verbatim.
- **Phase 3p §4.7 strict integrity gate** — preserved verbatim.
- **Phase 3r §8 mark-price gap governance** — preserved verbatim.
- **Phase 3v §8 stop-trigger-domain governance** — preserved verbatim.
- **Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance** — preserved verbatim.
- **Phase 4j §11 metrics OI-subset partial-eligibility rule** — preserved verbatim.
- **Phase 4k V2 backtest-plan methodology** — preserved verbatim.
- **Phase 4p G1 strategy-spec memo** — preserved verbatim.
- **Phase 4q G1 backtest-plan methodology** — preserved verbatim.
- **Phase 4v C1 strategy-spec memo** — preserved verbatim.
- **Phase 4w C1 backtest-plan methodology** — preserved verbatim.
- **Phase 4ak M0 mechanism-admissibility twelve-clause gate** — preserved verbatim.
- **Phase 4ak post-null cooldown rule** — preserved verbatim.
- **Phase 4ak cooled-down families list** — preserved verbatim.
- **Phase 4ak future M0 memo template** — preserved verbatim.
- **Phase 4al refined no-rescue rule** — preserved verbatim.
- **Phase 4al §13 boundary** — preserved verbatim.
- **Phase 4al §14 hierarchy** — preserved verbatim.
- **Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant** — preserved verbatim.
- **Phase 4bb-F canonical path policy** — preserved verbatim.

No project lock is modified by Phase 4bl-B. No project lock is silently weakened by Phase 4bl-B. No project lock is amended by Phase 4bl-B.

---

## 20. Current-project-state update plan

This section specifies the exact narrow update Phase 4bl-B makes to `docs/00-meta/current-project-state.md`.

### 20.1 Narrative paragraph

A new Phase 4bl-B narrative paragraph will be appended to the project narrative. The paragraph will be inserted **immediately above** the Phase 4bl-A narrative paragraph (which itself sits above the Phase 4bj-K narrative paragraph), preserving the descending chronological order used throughout the document.

The Phase 4bl-B paragraph will state:

- Phase 4bl-B identity (Multi-Day aggTrades Acquisition Authorization / Design Memo, docs-only design / authorization-gate memo);
- selected scope (BTCUSDT only, 90 contiguous UTC days, 2024-12-01 through 2025-02-28 inclusive);
- explicit non-authorizations (Phase 4bl-C, downloads, modifications, ML, strategy, etc.);
- preserved invariants (existing Phase 4az artefacts byte-identical; retained verdicts; project locks);
- recommended state at end of Phase 4bl-B (Phase 4bl-C conditional primary; remain-paused conditional secondary).

### 20.2 Current phase block update

The current top "Current phase:" block on `main` is Phase 4bl-A's (installed by the Phase 4bl-A merge). It will be replaced with a new Phase 4bl-B block. The prior Phase 4bl-A block will be preserved as historical context immediately below the new block, wrapped with: "Earlier Phase 4bl-A 'Current phase:' block (preserved here for continuity; Phase 4bl-A is no longer the current phase):".

Phase 4bl-B will:

- prepend a new Phase 4bl-B narrative paragraph above the existing Phase 4bl-A narrative paragraph;
- replace the existing "Current phase:" block (currently Phase 4bl-A) with a new Phase 4bl-B block;
- preserve the prior Phase 4bl-A block as historical context immediately below the new Phase 4bl-B block;
- leave the older preserved-history chain (Phase 4bj-K, Phase 4bj-J, …, Phase 4ba, etc.) unchanged.

### 20.3 No other changes

The Phase 4bl-B update to `current-project-state.md` is strictly limited to:

- the new Phase 4bl-B narrative paragraph;
- the new Phase 4bl-B "Current phase:" block;
- the preservation wrapper for the prior Phase 4bj-K "Current phase:" block.

No other paragraph, no other section, no other content of `current-project-state.md` is modified by Phase 4bl-B.

---

## 21. Final summary

### 21.1 Phase 4bl-B is

A docs-only design / authorization-gate memo that locks the future multi-day aggTrades acquisition design: BTCUSDT-only, 90 contiguous UTC days, 2024-12-01 through 2025-02-28 inclusive, sourced from `data.binance.vision` public daily aggTrades archives only, with a new sibling v002 multi-day manifest, atomic write-then-rename, SHA256 verification against the published `.CHECKSUM` companions, byte-identical preservation of the existing one-day Phase 4az fixture, and gitignored local outputs only.

### 21.2 Phase 4bl-B is NOT

An acquisition phase, a download phase, a normalization phase, a feature phase, a label phase, an eligibility-gate phase, a successor-state phase, a diagnostic phase, an ML phase, a strategy phase, a backtest phase, a paper / shadow phase, a live-readiness phase, or an authorization for any future phase. Phase 4bl-B is the design and authorization-gate; Phase 4bl-C is the (not-yet-authorized) execution.

### 21.3 What Phase 4bl-B produces

Three tracked docs files:

- `docs/00-meta/implementation-reports/2026-05-12_phase-4bl-b_multi-day-aggtrades-acquisition-design-memo.md` (this memo);
- `docs/00-meta/implementation-reports/2026-05-12_phase-4bl-b_closeout.md`;
- narrow update to `docs/00-meta/current-project-state.md`.

No `data/microstructure/` artefact, no source / test / script change, no `.gitignore` change, no MCP change, no manifest mutation, no verdict revision, no lock modification.

### 21.4 Recommended state at end of Phase 4bl-B

**Phase 4bl-C conditional primary; remain-paused conditional secondary.**

If the operator authorizes Phase 4bl-C separately, it executes the design locked by this memo. If the operator chooses to remain paused, the project remains at the post-Phase-4bl-B / Phase 4bj-K consolidation boundary with no successor authorized.

### 21.5 Strict stop point

Phase 4bl-B work stops here. The next step is **operator review and merge of Phase 4bl-B branch into `main`**, followed by recording the Phase 4bl-B merge-closeout. Phase 4bl-C is NOT authorized by this memo and must be the subject of a separate operator prompt.

---

**End of Phase 4bl-B memo.**
