# Phase 4bn-J — Acquisition-Only BTCUSDT aggTrades 12-Month Phase — STOP REPORT

**Status: STOPPED before acquisition. No data acquired. No code written. No
manifest created. No commit made. Branch-incomplete by design — handoff
report for the operator + downstream phase author (ChatGPT).**

This is a **stop report**, not a closeout. The operator interrupted execution
at the disk-footprint preflight and requested a findings-and-considerations
report instead of either (a) proceeding to acquisition under an amended cap or
(b) writing the full Tier-1 fail-closed doc set. This document records exactly
what was verified, what was found, and the operator-relevant considerations so
the next phase prompt (or a Phase 4bn-I cap amendment) can be authored
correctly.

---

## 0. One-paragraph summary

Phase 4bn-J set out to acquire 12 months of public Binance USDⓈ-M futures
BTCUSDT aggTrades (2024-03-01 .. 2025-02-28 UTC), where only the **275 new
pre-v002 days** (2024-03-01 .. 2024-11-30) are actually fetched and the existing
90-day v002 terminal window (2024-12-01 .. 2025-02-28, including the sealed
2025-02-14 .. 2025-02-28 test split) is left untouched. **The source-policy
preflight PASSED** (the aggTrades bulk-archive source is unambiguously defined
by committed tooling). **The disk-footprint preflight tripped the contractual
5 GiB hard cap**: the real raw-only footprint for 275 days is **~5.5–7.5 GiB**.
The operator clarified that disk is not a real constraint (400 GB free) and that
the 5 GiB cap is too harsh. Because that cap is written into the **merged,
immutable Phase 4bn-I contract**, it cannot be silently overridden from inside
Phase 4bn-J — it requires an explicit operator-authorized amendment. Execution
was therefore stopped here for a governance decision.

**Result state:** `ACQUISITION_NOT_RUN__PREFLIGHT_CAP_EXCEEDED__REMAIN_PAUSED`
(operator-requested stop pending a cap-amendment decision).

---

## 1. Repository state (verified)

- **Working machine:** Desktop. **Repo:** `C:\Prometheus`.
- **Base `main` / `origin/main` SHA (verified equal):**
  `27dbc5723f3f068c34663ec57cd85a0e6b42f501`
  — `docs(phase-4bn-i): finalize merge closeout shas`.
- Predecessor chain confirmed present: `5aed510` (4bn-I merge-closeout),
  `4733d90` (4bn-I merge), `a513c4f` (4bn-I branch), `654befd` (4bn-H finalize).
- **Working branch created:** `phase-4bn-j/acquisition-only-btcusdt-aggtrades-12m`
  (0 commits; no tracked changes; this stop report is the only new file and is
  currently **uncommitted**).
- Only untracked transient at start: `.claude/scheduled_tasks.lock` (not
  committed). Gitignored `data/microstructure/` and `data/research/` namespaces
  remain uncommitted and were not mutated.

---

## 2. Source-policy preflight — RESULT: **PASS (source confirmed via committed tooling)**

Phase 4bn-I §10 flagged a source-policy gap and required the acquisition phase
to confirm the aggTrades bulk-archive source from committed docs **and/or
existing committed acquisition tooling**, failing closed only if confirmation is
insufficient or ambiguous.

### 2.1 The committed `historical-data-spec.md` gap is real
`docs/04-data/historical-data-spec.md` documents only the official Binance
USDⓈ-M **REST** endpoints (klines, mark-price, funding, exchange-info, leverage,
commission). It does **not** mention aggTrades, bulk historical archives,
`data.binance.vision`, archive naming, or archive checksum policy at all. Taken
alone, the spec is silent on this source.

### 2.2 …but committed tooling resolves it unambiguously
The aggTrades bulk-archive source policy is **authoritatively defined by
committed, already-executed tooling** — the same tooling that produced the
existing v002 raw window:

- `scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py` (acquired the v002
  90-day window 2024-12-01 .. 2025-02-28);
- `scripts/phase4az_acquire_btcusdt_aggtrades_archive.py` (single-day precedent);
- `src/prometheus/research/microstructure/aggtrades.py` (Phase 4ax validator);
- `src/prometheus/research/data/binance_bulk.py` (klines/markprice bulk client;
  documents the `data.binance.vision` base, `.CHECKSUM` companion, and the
  exact `<sha256hex>  <filename>` two-space checksum format).

Confirmed source contract (locked in committed code):

| Field | Value |
|---|---|
| Source class | `public_unauthenticated_daily_archive` |
| Base host (allowlisted) | `data.binance.vision` (HTTPS only) |
| Archive URL pattern | `https://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/BTCUSDT-aggTrades-{YYYY-MM-DD}.zip` |
| Checksum URL | same + `.CHECKSUM` |
| Checksum format | `<sha256hex>  <filename>` (exactly two spaces) |
| Inner schema (headerless order) | `a,p,q,f,l,T,m` (aggId, price, qty, firstId, lastId, tradeTime ms, isBuyerMaker) |
| Integrity | download CHECKSUM first → download zip → SHA256 must match → `testzip()` → bounded row-sample validation via Phase 4ax validator |
| Sidecar | Phase 4bb-F canonical `<sha>␠␠<basename>\n` (LF, no BOM) |
| Manifest seed | `research_eligible=false`, `eligibility_gate_status="pending"` |
| Network discipline | stdlib `urllib` only; host-allowlisted; forbidden-token denylist for `fapi`, order/account endpoints, `api_key`, `.env`, `.mcp.json`, MCP, Graphify, etc. |
| Per-file download cap (existing) | 5 GiB (`MAX_DOWNLOAD_BYTES`) — fine; daily zips are < 100 MiB |

**No credentials, no private endpoint, no authenticated API, no WebSocket, no
user stream, no `.env`, no `.mcp.json`, no MCP, no Graphify** are required or
used by this source. The source-policy preflight therefore **passes**: it is
**not** ambiguous once grounded in committed tooling. (A separate docs-only
source-policy memo to backfill `historical-data-spec.md` with the aggTrades
archive convention would be good hygiene but is **not** required to acquire,
because committed tooling already encodes the contract.)

---

## 3. Disk-footprint preflight — RESULT: **TRIPS the contractual 5 GiB hard cap**

### 3.1 The contract being enforced
Phase 4bn-I §15 and this phase's prompt impose: warning threshold **3 GiB**
additional, **hard cap 5 GiB** additional, and "**if estimated footprint
exceeds 5 GiB, fail closed before acquisition**" (stop condition #13).

### 3.2 Repo convention makes this a RAW-ONLY phase (important)
The repository separates acquisition from derivation into distinct, separately
gated phases:

- **Raw acquisition** — Phase 4bl-C, *acquisition-only*: "MUST NOT normalize,
  derive, compute features, compute labels, run gates…".
- **Normalization** — Phase 4bm-B (separate phase + gate).
- **Features** — Phase 4bm-H/I/J (separate phases + gate).
- **Labels** — Phase 4bm-O/P/Q (separate phases + gate).

Per the phase prompt's own instruction ("if the repository's existing
conventions separate raw acquisition from normalization/feature/label
derivation into later gates, then do not derive … in Phase 4bn-J"),
**Phase 4bn-J is raw-only.** The relevant footprint is therefore **raw zips
only**, not raw+normalized+feature+label.

### 3.3 Per-day size evidence (no sealed data read; committed docs + HEAD metadata)

**Committed-docs evidence (calendar-adjacent v002 window):**
- v002 raw = 90 contiguous days (2024-12-01 .. 2025-02-28) =
  **1,943,823,208 bytes ≈ 1.81 GiB** across 90 zips
  (Phase 4bl-C merge-closeout / Phase 4bl-D gate).
- ⇒ v002 raw average ≈ **21,598,035 B/day ≈ 20.6 MiB/day**.
- Phase 4bl-A independently: a single BTCUSDT futures aggTrades day ≈ 21 MiB.

**Empirical HEAD-only metadata probe (this phase; Content-Length only — no
archive bodies downloaded, nothing written to disk, no v002/sealed data
touched), representative pre-v002 dates:**

| Date | Content-Length | Note |
|---|---|---|
| 2024-03-01 | 17.71 MiB | range start |
| 2024-03-12 | 32.36 MiB | March 2024 ATH ~$73.8k |
| 2024-06-22 | 3.82 MiB | quiet weekend |
| 2024-08-05 | 75.13 MiB | Aug-5 2024 deleveraging crash |
| 2024-09-15 | 8.72 MiB | mid |
| 2024-11-06 | 48.33 MiB | US-election rally |
| 2024-11-30 | 8.02 MiB | range end |

This 7-day sample is **deliberately event-weighted** (I picked the ATH, the
crash, and the election day to test the worst case); its mean (27.7 MiB/day)
over-represents volatility and should **not** be read as the 275-day mean. A
fuller systematic monthly sample was started but the operator interrupted
before it completed.

### 3.4 275-day raw-only estimate

- New segment = 2024-03-01 .. 2024-11-30 = **275 days** (365-day envelope − 90-day
  v002 terminal).
- Central estimate (v002 contiguous-quarter average, the most representative
  single figure): 275 × 20.6 MiB ≈ **5.53 GiB**.
- Conservative/event-aware estimate (HEAD sample): up to 275 × 27.7 MiB ≈
  **7.45 GiB**.
- **Planning range: ~5.5–7.5 GiB raw.**

**Both ends of the estimate exceed the contractual 5 GiB hard cap.** Days-to-cap
at the v002 average: 3 GiB warning ≈ day 149; 5 GiB hard cap ≈ day 248 — i.e.,
the cap is breached **before** the 275-day range completes even on the
optimistic average. **Per the Phase 4bn-I contract, this is a fail-closed
condition before acquisition.**

---

## 4. The cap-design inconsistency (root-cause finding for the amendment author)

The Phase 4bn-I 5 GiB cap was justified (its §15) as "**≈ 4× the 90-day v002 raw
+ normalized + feature + label footprint**". That justification does not survive
contact with the actual committed footprint evidence:

- v002 **raw** alone (90 d) ≈ 1.81 GiB.
- v002 **normalized** alone (90 d) ≈ **20.6 GiB** (Phase 4bm-A/B; ~133 B/row ×
  ~1.68 M rows/day × 90 d; ~229 MB/day).
- v002 **label** parquet was estimated by Phase 4bl-A at **14–21 GiB for just
  60–90 days** (~140 B/row).

So the *actual* 90-day raw+normalized+feature+label stack is already on the order
of **tens of GiB**, and "4× of it" would be **~80–120+ GiB**, not 5 GiB. The
5 GiB figure is only even plausibly near-fit for a **raw-only** scope — and even
raw-only for 12 months (275 new days) exceeds it (§3.4). The cap as written is
internally inconsistent with the evidence it cites.

**Implication:** the 5 GiB cap conflates "raw-only acquisition footprint" with
"full derived-stack footprint." A correct cap must (a) name the scope it bounds
(raw-only here), and (b) be set from real per-day evidence.

---

## 5. Operator input (recorded)

> "you mentioned a 5gb hardcap, no need to be so harsh, i have 400gb of disk
> space available … create a stop report mentioning the findings and my
> considerations so that i can give to chatgpt"

Interpretation: disk is **not** the binding constraint; the operator considers
the 5 GiB cap inappropriate; the operator wants a handoff report (not an
in-phase cap override, and not the strict fail-closed Tier-1 doc set) so the
next phase / amendment can be authored externally.

I did **not** override the cap, because it lives in the merged, SHA-finalized
Phase 4bn-I contract and stop-condition set; overriding it from inside
Phase 4bn-J would violate the integrity-bound nature of the phase. That is an
operator/amendment decision, which this report exists to support.

---

## 6. Considerations & options for the next phase prompt / Phase 4bn-I amendment

These are recommendations for ChatGPT to turn into an authorized prompt. None of
them is authorized or performed here.

### 6.1 Recommended: amend the disk-footprint cap (scope-correct, evidence-based)
- Re-state the cap **as raw-only** for the acquisition phase.
- Set the raw-only ceiling from real evidence with headroom — e.g. **hard cap
  ~15–25 GiB raw, warning ~10 GiB** — comfortably above the ~5.5–7.5 GiB
  estimate and trivial against 400 GB. (Even ~12 GiB would clear it, but the
  2024 event days argue for headroom.)
- Keep **runtime** as a real cap (see §6.3); with disk de-fanged, runtime and
  integrity become the binding gates.
- Keep a separate, explicit **derived-stack** cap for any *future* normalization
  /feature/label phase (those are ~tens of GiB and must not silently inherit a
  raw-only number).

### 6.2 Scope stays raw-only and identical otherwise
- Symbol BTCUSDT only; market Binance USDⓈ-M futures; family aggTrades only.
- Fetch only the **275 new pre-v002 days** 2024-03-01 .. 2024-11-30. Do **not**
  re-download, overwrite, open, hash, count, or read the existing v002 window or
  (especially) the sealed test split 2025-02-14 .. 2025-02-28.
- No normalization / features / labels / ML / diagnostics / strategy / PnL /
  backtests; no DuckDB/SQLite DB files; no Parquet compaction; no v003; no
  ETHUSDT / mark-price / spot / cross-venue / order-book / tick / extra-horizon.
- Manifests start `research_eligible=false`, `eligibility_gate_status="pending"`;
  no eligibility transitions; Phase 4aw `flip_research_eligible(...)`
  always-raises invariant preserved.
- Phase 4bb-F canonical sidecars; refuse-overwrite; gitignored; never committed.

### 6.3 New bounded script is required (existing tooling can't cover the range)
- `scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py` is **hardcoded** to
  the 90-day v002 range (`DATE_START=2024-12-01`, `DATE_END=2025-02-28`,
  `EXPECTED_DATE_COUNT=90`) and to the existing fixture date. It cannot be
  pointed at 2024-03-01 .. 2024-11-30 without modification, and that script is a
  locked prior-phase artefact.
- Recommended: a **new, small, parameterized acquisition script** that **reuses**
  the proven phase4bl-C patterns verbatim — same host allowlist, same URL/path
  pattern, same CHECKSUM-first ordering, same SHA256 + `testzip()` + row-sample
  validation, same Phase 4bb-F sidecars, same refuse-overwrite, same
  non-eligible manifest seed, same per-day cap enforcement — with the date range
  set to the 275-day pre-v002 segment and an explicit guard that **rejects any
  date ≥ 2024-12-01** (so it can never touch v002 / sealed data).
- Required tests (offline, no network): exact 275-date generation; reject any
  post-2024-11-30 date; BTCUSDT-only; aggTrades-only; refuse-overwrite; sidecar
  format; manifest non-eligible seed; per-day cap fail-closed; URL allowlist
  rejects credentials/private/WS/userStream.

### 6.4 Runtime
- 275 days × 2 HTTP round-trips (CHECKSUM + zip) with conservative pacing, ~5.5–
  7.5 GiB total transfer + per-day decompress/inventory. Expected well under the
  4 h wall-clock cap (the 90-day v002 normalization orchestrator alone ran ~24
  min; raw acquisition is lighter per day), but it should be **measured per-day
  and cap-enforced** during the run. The 4 h runtime cap looks fine to keep.

### 6.5 Sealed-test & holdout posture (unchanged)
- Sealed v002 test split 2025-02-14 .. 2025-02-28 stays sealed; `test_rows_loaded:
  0` and the `iter_partitions(split="test", …)` raise pattern preserved. The
  275-day backward extension never touches it. No new holdout/split policy is
  defined by acquisition; that remains a separate docs-only memo before any ML.

---

## 7. What was and was NOT done in this session

**Done (read-only / metadata-only):**
- Verified repo state and SHAs; created the working branch.
- Read Phase 4bn-I execution plan, `historical-data-spec.md`, the committed
  acquisition tooling (`phase4bl_c`, `phase4az`, `binance_bulk.py`,
  `aggtrades.py`), and footprint evidence across the 4bl/4bm reports.
- Ran a **HEAD-only** Content-Length metadata probe of 7 pre-v002 dates (no
  archive bodies, no files written, no v002/sealed data touched).
- Wrote this stop report.

**NOT done (deliberately):**
- No archive downloaded; **no data acquired**; no `data/microstructure/`
  artefact created; no manifest/sidecar written.
- No acquisition/normalization/feature/label/ML/diagnostics/strategy/PnL/
  backtest code run.
- No new acquisition script written; no existing script modified.
- No DB/`.duckdb`/`.sqlite` created; no Parquet compaction; no v003.
- No manifest eligibility transition; `flip_research_eligible` never invoked.
- No sealed test split opened/read/hashed/counted/sampled.
- No credentials/private endpoint/WebSocket/user stream/`.env`/`.mcp.json`/MCP/
  Graphify used.
- **No `current-project-state.md` change. No commit. No push. No merge.**
- `data/research/` untouched; nothing under `data/microstructure/` or
  `data/research/` staged or committed.

---

## 8. Result, decision, and recommended next state

- **Phase result state:**
  `ACQUISITION_NOT_RUN__PREFLIGHT_CAP_EXCEEDED__REMAIN_PAUSED`
  (operator-requested stop for a cap-amendment decision).
- **Decision (this report):** `RECORD_ACQUISITION_ONLY_RESULT__REMAIN_PAUSED` —
  stop, report findings, await an operator/ChatGPT decision on the cap.
- **Recommended next state:** author a Phase 4bn-I cap amendment (or a Phase
  4bn-J-revised prompt) that (1) re-scopes the cap as **raw-only**, (2) sets a
  raw-only ceiling ~15–25 GiB from §3–4 evidence, (3) keeps the 4 h runtime cap
  and all other fail-closed conditions, and (4) authorizes a new bounded
  275-day raw-only acquisition script + tests per §6.3. Then a separate
  acquisition execution phase can run within the corrected contract.
- **No successor is authorized by this report.** No ML / diagnostics / strategy
  / PnL / backtest / storage-migration / DB-creation / Parquet-compaction / v003
  / paper / shadow / live / exchange-write is recommended or authorized.

---

## 9. Explicit non-authorization statement

No ML was trained; no model scoring was performed; no predictions were
generated; no diagnostics were run; no strategy/signal/PnL/backtest work was
performed; no storage migration occurred; no database was created; no Parquet
was compacted; no v003 dataset was created; no test holdout was touched; no
manifest eligibility transition occurred; no `data/research/` artefacts were
created or committed; no `data/microstructure/` artefacts were created or
committed; and no paper/shadow/live/exchange-write/credentials/MCP/Graphify work
was authorized. Phase 4bn-J remains **branch-incomplete and stopped**; nothing
was merged or pushed.
