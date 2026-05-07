# Phase 4au — Binance Microstructure Capture Design Specification Memo

## Phase identity

- Phase ID: **4au**.
- Phase title: **Binance Microstructure Capture Design Specification Memo**.
- Type: docs-only Binance microstructure capture-design
  specification memo.
- Authority: separately operator-authorised as a docs-only
  design phase only.
- Branch: `phase-4au/binance-microstructure-capture-design-specification`.
- Base SHA (main at branch creation):
  `4bce0042fcccd32a4b1aeeda3bb19d7d73fb4121`.
- Phase 4au memo commit SHA: recorded in this phase's closeout
  once this memo is committed.

---

## 1. Executive summary

Phase 4at translated Phase 4as §9 into a precise Binance public
market-data availability and capture-feasibility map. Phase 4au
is the separately-authorised next docs-only phase recommended by
Phase 4at. Its purpose is to translate the Phase 4at availability
matrix and §15 capture-design requirements into a precise,
implementation-ready **design specification** for a future
public-only Binance microstructure capture pipeline — without
implementing anything.

Phase 4au's central design conclusion (qualitative; nothing
built):

- A future capture pipeline can be specified at the design
  layer using **public-only** Binance USDⓈ-M Futures endpoints
  (REST and WebSocket) and the bulk archive at
  `data.binance.vision`. No authenticated, user-scope, or
  exchange-write surface is required at any layer.
- The pipeline can be specified as nine cooperating components
  (capture supervisor, per-symbol stream workers, REST polling
  workers, raw event writer, normalizer, replay builder,
  manifest writer, health-check reporter, local operator
  dashboard hook) running entirely outside `prometheus.runtime`,
  `prometheus.execution`, and `prometheus.persistence`.
- A three-layer storage model (raw → normalized → derived) plus
  a fourth manifest layer keeps capture, replay, and research
  cleanly separated; the design recommends a **separate
  `data/microstructure/...` namespace** instead of writing into
  the existing `data/raw/` / `data/normalized/` / `data/derived/`
  / `data/manifests/` paths used by Phase 2 / 3q / 4i / 4ac.
- The seven proposed future dataset family names from Phase 4at
  are restated as design names only and given per-family schema,
  partition, manifest, and invalid-window specifications; **none
  is created**.
- Local order-book reconstruction follows the official Binance
  procedure (REST snapshot + diff-depth stream;
  `U` / `u` / `pu` sequence-number bookkeeping; resync on gap)
  and is specified at the design layer only.
- Every governance boundary already in force (M0 admissibility;
  post-null cooldown; cooled-down families; no-rescue rule;
  Phase 3r §8 mark-price gap governance; Phase 3v §8
  stop-trigger-domain governance; Phase 3w break-even / EMA
  slope / stagnation governance; Phase 4j §11 OI-subset
  governance; §11.6 cost realism; §1.7.3 project-level locks)
  is preserved verbatim.

Phase 4au **does not** acquire data, call any Binance endpoint,
open any WebSocket, download any archive, modify endpoint code,
implement capture, implement replay, implement features, run
scripts, modify manifests, modify governance, modify retained
verdicts or project locks, or authorise any successor phase.

The recommendation is to **remain paused** unless the operator
separately authorises a docs-only **Phase 4av — Public-Only
Microstructure Capture Implementation Plan**, which would
convert this design specification into a docs-only file list,
module boundaries, CLI surface, tests, failure modes, and
validation gates **without implementing capture**. **Phase 4av
is not authorised by Phase 4au.**

---

## 2. Scope and explicit non-scope

### In scope

- A docs-only **capture design specification** for Binance
  USDⓈ-M Futures public market-data relevant to the Phase 4as
  M-1..M-14 mechanism set.
- A capture **architecture overview** (§7) and a public-only
  **endpoint allowlist** (§8) and **denylist** (§9).
- A **dataset family design** (§10) for each Phase 4at-proposed
  family, including per-family purpose, source, layer,
  partition keys, file format, timestamp / sequence fields,
  schema-version field, manifest requirement, default
  `research_eligible`, invalid-window behaviour, and
  governance constraints.
- A **storage layout specification** (§11) recommending a
  separate `data/microstructure/...` namespace.
- A **file format and compression design** (§12) covering
  raw, normalized, derived, and manifest layers.
- A **manifest design specification** (§13) listing all
  required manifest fields.
- A **schema design specification** (§14) covering aggTrades,
  bookTicker, depthDiff, depthSnapshot, forceOrder proxy,
  markPrice, OI / funding metrics, and reconstructed LOB state.
- A **timestamp discipline** (§15).
- A **rate-limit and retry design** (§16).
- A **WebSocket connection design** (§17).
- A **local order-book reconstruction design** (§18).
- A **liquidation proxy design** (§19) with strict
  proxy-only labelling.
- An **OI / funding capture design** (§20) under Phase 4j §11
  governance.
- An **invalid-window governance** specification (§21).
- A **research eligibility gate** specification (§22).
- A **deterministic replay design** (§23).
- A **health-check and operator dashboard design** (§24).
- **Security and credential boundary** rules (§25).
- **Runtime separation** rules (§26).
- A **symbol and scope policy** (§27).
- A **storage and hardware feasibility discussion** (§28).
- **Validation / anti-overfitting implications** (§29).
- **M0 governance implications** (§30).
- A **recommended next phase** (§31), explicit
  **non-recommendations** (§32), the
  **implementation / governance review** (§33), the
  **research interpretation review** (§34), and explicit
  **preservation of verdicts, locks, and no-rescue
  constraints** (§35).

### Out of scope (forbidden in Phase 4au)

- No data acquisition.
- No Binance endpoint calls.
- No WebSocket connections.
- No public-archive downloads.
- No endpoint code creation or modification.
- No capture implementation.
- No replay implementation.
- No feature implementation.
- No order-book reconstruction implementation.
- No backtest or historical strategy script execution.
- No Phase 4aq script re-execution.
- No simulation.
- No predictive statistics computation.
- No source / test / script / data / manifest / governance /
  spec / threshold / lock change.
- No `.gitignore` change.
- No commit of any `data/research/` output.
- No actual dataset directory creation.
- No actual manifest creation.
- No new strategy candidate.
- No exit / entry design.
- No optimisation of R3 or any prior population.
- No R3-prime / R2-prime / R1a-prime / R1b-narrow-prime / H0-prime
  / V2-prime / G1-prime / C1-prime / D1-A-prime / D1-B / V1-D1 /
  F1-D1 / cross-strategy hybrid.
- No verdict revision.
- No lock revision.
- No M0 amendment.
- No reopening of the 5m research thread.
- No authorisation of Phase 4av, Phase 5, Phase 4 canonical,
  paper / shadow, live-readiness, deployment, exchange-write,
  production keys, authenticated APIs, private endpoints, user
  stream, WebSocket implementation, MCP, Graphify, `.mcp.json`,
  credentials, 5m / 1m / aggTrades / tick-data / mark-price 30m
  / 4h, or order-book capture.

---

## 3. Repository verification summary

Repository state at branch creation:

```text
git status                 — clean working tree on main; only
                              gitignored transients
                              (.claude/scheduled_tasks.lock,
                              data/research/) untracked.
git branch --show-current  — main (before branch creation) /
                              phase-4au/... (after).
git log --oneline -16      — Phase 4at merged at 4bce004.
git rev-parse main         — 4bce0042fcccd32a4b1aeeda3bb19d7d73fb4121.
git rev-parse origin/main  — 4bce0042fcccd32a4b1aeeda3bb19d7d73fb4121.
```

Phase 4at files confirmed present on `main`:

- `docs/00-meta/implementation-reports/2026-05-07_phase-4at_binance-microstructure-data-availability-capture-feasibility.md`.
- `docs/00-meta/implementation-reports/2026-05-07_phase-4at_closeout.md`.
- `docs/00-meta/implementation-reports/2026-05-07_phase-4at_merge-closeout.md`.

`main` and `origin/main` are in sync. The working tree contains
no unexpected uncommitted change.

Branch created:

```text
git checkout -b phase-4au/binance-microstructure-capture-design-specification
```

---

## 4. Methodology

Phase 4au is a docs-only capture-design specification memo. It is
built from:

- **static repository inspection** of committed docs (Phase 4at,
  Phase 4as, Phase 4ar, Phase 4aq, Phase 4ap, Phase 4ao,
  Phase 4an, Phase 4al, Phase 4ak, Phase 3v §8, Phase 3r §8,
  Phase 3w, Phase 4j §11, current-project-state, phase-gates,
  M0 governance);
- **public / official documentation references** carried
  forward from Phase 4at — official Binance USDⓈ-M Futures
  developer documentation, the public Binance public-data
  repository (`github.com/binance/binance-public-data`), and
  the bulk-archive endpoint (`data.binance.vision`). Phase 4au
  does **not** call any endpoint, open any WebSocket, or
  download any archive. The Phase 4at memo is treated as the
  citation source of record for endpoint behaviour.

The memo does **not**:

- call any Binance endpoint;
- modify any endpoint code;
- acquire any data;
- open any WebSocket;
- download any archive;
- inspect or modify local `data/research/` outputs;
- run any script (Phase 4aq's script or otherwise);
- implement any feature, ML model, or strategy;
- perform any computation that yields predictive statistics;
- create any actual dataset directory or manifest;
- touch credentials, MCP, `.mcp.json`, or any exchange-write
  surface.

The memo follows the prior-phase docs-only convention used by
Phase 4d, 4e, 4f, 4g, 4h, 4j, 4k, 4m, 4n, 4o, 4p, 4q, 4s, 4t,
4u, 4v, 4w, 4y, 4z, 4aa, 4ab, 4ad, 4ag, 4ah, 4aj, 4ak, 4al,
4an, 4ao, 4ap, 4ar, 4as, and 4at (no `ruff` / `pytest` / `mypy`
execution because no code, test, or script is changed).

---

## 5. Phase 4at baseline (preserved)

Phase 4at established the binding context for Phase 4au. It is
preserved verbatim:

- **Historical archive available** (REST + bulk archive at
  `data.binance.vision`): aggTrades; raw trades; klines;
  mark-price klines (subject to Phase 3r §8 governance);
  premium-index klines; index-price klines.
- **REST history available**: funding-rate history.
- **REST recent only (~30 days rolling) — forward REST polling
  required for extended history**: `openInterestHist`;
  `topLongShortAccountRatio`; `topLongShortPositionRatio`;
  `globalLongShortAccountRatio`; `takerlongshortRatio`. Current
  open interest (`GET /fapi/v1/openInterest`) is also a REST
  snapshot endpoint; forward time-series construction requires
  forward REST polling, not WebSocket capture.
- **WS live-capture required (no public archive at full
  granularity for derivatives)**: book ticker; partial book
  depth; diff book depth; mark-price stream; index-price
  stream; the REST depth snapshot is the snapshot starting
  point for local LOB reconstruction combined with the diff-
  depth WS stream.
- **Public proxy only**: `<symbol>@forceOrder` and
  `!forceOrder@arr` push only the largest one liquidation
  order per 1000 ms per symbol.
- **Authenticated user-scope, NOT admissible for market-wide
  research**: REST `/fapi/v1/forceOrders`; user stream;
  listenKey lifecycle; all private endpoints.

Phase 4at recorded twenty capture-design requirements (process
isolation; public-only allowlist; no credentials; raw immutable
logs; normalised derived tables; manifest + SHA256 versioning;
schema versioning; event/transaction/ingestion-time separation;
symbol allowlist; rate-limit handling; reconnect/resync; explicit
`invalid_window`; deterministic replay; storage layout;
compression; structured logs; health checks; no exchange-write;
no `prometheus.runtime/execution/persistence` coupling; no write
to existing data) and seven proposed future dataset family names
(`microstructure_raw_aggtrades_v001`,
`microstructure_raw_depthdiff_v001`,
`microstructure_raw_bookticker_v001`,
`microstructure_raw_forceorder_proxy_v001`,
`microstructure_raw_markprice_v001`,
`microstructure_metrics_oi_funding_v001`,
`microstructure_replay_lob_v001`). **None was implemented or
created.** Phase 4au inherits all of those constraints verbatim
and turns them into a per-component design specification.

Phase 4at recommended Phase 4au as the cleanest separately-
authorised next docs-only move and explicitly did **not**
authorise it. The operator has now separately authorised
Phase 4au as a docs-only design memo only.

---

## 6. Capture design goals

The future capture pipeline must satisfy the following design
goals. **No goal is implemented by Phase 4au.**

- **Public-only.** All endpoints in scope are public REST or
  WebSocket. No authenticated endpoint, user stream, listenKey,
  or `.env` read is allowed at any layer.
- **Read-only.** No order placement, no leverage / margin
  modification, no account modification, no exchange-write
  surface of any kind.
- **No credentials.** The capture process does not load,
  request, store, or accept any Binance API key. Any code path
  that would touch a key is forbidden by design.
- **Deterministic replay.** Raw → normalized → derived must
  always replay deterministically. Research code consumes
  derived layers through replay only; ad-hoc reads from raw
  logs are forbidden.
- **Immutable raw logs.** Raw logs are append-only and never
  rewritten. Compaction occurs only via deterministic replay
  into a new normalized/derived family with a fresh `__vNNN`
  bump.
- **Manifest-first lineage.** Every file in raw / normalized /
  derived layers is referenced by exactly one manifest entry
  with a paired SHA256.
- **Explicit invalid-window governance.** No silent gap fill,
  forward fill, interpolation, imputation, or replacement;
  every gap or anomaly produces a manifest `invalid_window`
  entry per Phase 3p §4.7 / Phase 3r §8 / Phase 4j §11
  precedent.
- **Layer separation.** Raw / normalized / derived / manifest
  layers are kept in distinct directories with distinct write
  rules.
- **Runtime separation.** The capture pipeline is research
  infrastructure only. It does **not** import
  `prometheus.runtime`, `prometheus.execution`, or
  `prometheus.persistence`, does not write to the runtime
  database, and does not touch any safety-state surface.
- **No paper / live capability.** The pipeline cannot be
  reused as a paper / shadow / live execution path. It is
  purely market-data research infrastructure.
- **Future-research-only.** The pipeline supports Phase 4as
  M-1..M-14 mechanism feasibility study under M0; it does not
  imply edge or authorise strategy work.

---

## 7. Capture architecture overview

The future capture pipeline is specified as nine cooperating
components. **None is implemented in Phase 4au.**

1. **Capture supervisor.** Top-level coordinator. Owns the
   public-only endpoint allowlist (§8). Spawns / monitors per-
   symbol stream workers (component 2) and REST polling workers
   (component 3). Restarts failed components with bounded
   retries. Enforces graceful shutdown.
2. **Per-symbol stream workers.** One worker per
   (symbol, stream) pair; subscribes to a single allowlisted WS
   stream (e.g. `<symbol>@aggTrade`, `<symbol>@bookTicker`,
   `<symbol>@depth@250ms`, `<symbol>@forceOrder`,
   `<symbol>@markPrice`). Buffers and forwards events to the
   raw event writer (component 4). Handles reconnect / heartbeat
   / gap detection per §17.
3. **REST polling workers.** One worker per allowlisted REST
   family (e.g. `fundingRate`, `openInterest`,
   `openInterestHist`, `topLongShortAccountRatio`,
   `globalLongShortAccountRatio`, `takerlongshortRatio`). Polls
   at the documented `period` cadence with jittered exponential
   backoff and rate-limit awareness (§16).
4. **Raw event writer.** Receives events from streams (component
   2) and REST workers (component 3). Writes append-only
   immutable raw files (§12) using an atomic write pattern
   (write-then-rename). Emits per-write SHA256 to the manifest
   writer (component 7).
5. **Normalizer.** Deterministic process that consumes raw
   files for a given (family, symbol, partition) and produces
   normalized Parquet files (§12). Operates batch-only; never
   processes a partial partition. Records its own
   `capture_config_hash` and `code_commit_sha` in the
   normalized manifest entry.
6. **Replay builder.** Deterministic process that consumes
   normalized files and produces derived artefacts: LOB replay
   state (§18), feature-ready event-time-aligned tables, and
   research-friendly aggregations. Operates batch-only.
7. **Manifest writer.** Updates the per-family manifest with
   each new file's metadata, SHA256, time range, event count,
   schema version, capture-config hash, and any
   `invalid_window` entries detected by upstream components.
   Manifest writes are idempotent and atomic.
8. **Health-check reporter.** Emits structured local health
   signals (last event time, ingestion lag, reconnect count,
   gap count, invalid-window count, disk usage, file write
   lag, rate-limit headroom, per-symbol stream status) to a
   local file or socket consumed by the operator dashboard
   (component 9). No remote alerting is required at this layer.
9. **Local operator dashboard hook.** Read-only display of
   the health-check reporter's output. **No live trading or
   exchange-write surface.** No order panel. No
   authenticated-endpoint state. The dashboard is a pure
   research-infrastructure status view.

**Runtime trading dependency:** none. The capture pipeline is
strictly read-only with respect to `prometheus.runtime`,
`prometheus.execution`, and `prometheus.persistence`. The
runtime database is not touched.

---

## 8. Public-only endpoint allowlist

The future capture pipeline operates against the following
**public-only** Binance USDⓈ-M Futures endpoints. Citations are
in the Phase 4at memo (§9 REST market-data map; §10 WebSocket
market-stream map). **Phase 4au calls none of them.**

### 8.1 aggTrade family

- **Purpose:** M-5 / M-6 — aggressive volume / taker imbalance,
  trade burst.
- **Capture mode:** archive (`data.binance.vision/data/futures/um/{daily,monthly}/aggTrades/`) for backfill;
  REST `GET /fapi/v1/aggTrades` for forward catch-up;
  WS `<symbol>@aggTrade` for forward live capture.
- **Cadence:** WS push aggregated every 100 ms for same price +
  same taker side.
- **Timestamp fields:** `T` (trade time); `E` (event time on
  WS).
- **Sequence fields:** `a` (aggregate trade id); `f`/`l` (first
  / last trade id range).
- **Output raw family:** `microstructure_raw_aggtrades_v001`.
- **Risk notes:** insurance-fund / ADL trades excluded from
  aggregation; effective 2025-12-31 the new `nq` field excludes
  RPI orders; any feature must declare which definition it
  uses.
- **Governance:** subject to M0 admissibility for any future
  feature use; no D1-A-style directional reuse.

### 8.2 bookTicker family

- **Purpose:** M-1 (spread); M-2 (top-of-book depth).
- **Capture mode:** WS `<symbol>@bookTicker` (per-symbol) or
  `!bookTicker` (all-market). No public historical archive.
- **Cadence:** real-time on best bid/ask change.
- **Timestamp fields:** `E` (event time); `T` (transaction
  time).
- **Sequence fields:** `u` (order book update id).
- **Output raw family:** `microstructure_raw_bookticker_v001`.
- **Risk notes:** transient orders inflate noise; literature
  reports rapid alpha decay.
- **Governance:** M0 admissibility for any feature; no rank-
  then-V2 / G1 / C1-style reduction.

### 8.3 Partial book depth family

- **Purpose:** M-2 / M-3 (top-N depth and imbalance).
- **Capture mode:** WS `<symbol>@depth5/10/20@100/250/500ms`.
  No public historical archive.
- **Cadence:** per stream cadence (100 / 250 / 500 ms).
- **Timestamp fields:** snapshot per push; no separate event
  time inside snapshot.
- **Sequence fields:** `lastUpdateId` per push.
- **Output raw family:** subordinate to
  `microstructure_raw_depthdiff_v001` (depth diff is preferred
  for full reconstruction); partial depth may be captured
  optionally as a sanity / fallback dataset.
- **Risk notes:** RPI orders excluded; ephemeral orders
  dominate noise.
- **Governance:** M0; no rescue framing.

### 8.4 Diff book depth family

- **Purpose:** M-3 / M-4 (order-book imbalance, depth
  imbalance); M-7 / M-8 (sweep, replenishment); M-14 (regime).
- **Capture mode:** WS `<symbol>@depth` (250 ms default),
  `<symbol>@depth@500ms`, `<symbol>@depth@100ms`. No public
  historical archive.
- **Cadence:** 100 / 250 / 500 ms.
- **Timestamp fields:** `E` (event time); `T` (transaction
  time).
- **Sequence fields:** `U` (first update id), `u` (final
  update id), `pu` (previous final update id).
- **Output raw family:** `microstructure_raw_depthdiff_v001`.
- **Risk notes:** must be combined with REST snapshot
  (component 8.5) per the official Binance procedure (§18);
  any sequence gap forces resync.
- **Governance:** M0; full LOB reconstruction is a Lane C
  prerequisite.

### 8.5 REST depth snapshot

- **Purpose:** snapshot starting point for local LOB
  reconstruction with §8.4.
- **Capture mode:** REST `GET /fapi/v1/depth?symbol=...&limit=1000`.
  Snapshot only.
- **Cadence:** taken when starting / resyncing a
  `microstructure_raw_depthdiff_v001` capture window.
- **Timestamp fields:** snapshot time (server-provided).
- **Sequence fields:** `lastUpdateId`.
- **Output raw family:** subordinate to
  `microstructure_raw_depthdiff_v001` (snapshot files paired
  with the diff window they bracket).
- **Risk notes:** must satisfy the Binance bracketing rule
  `U <= lastUpdateId AND u >= lastUpdateId` for the first
  replayed diff event.
- **Governance:** M0; rate-limit aware.

### 8.6 forceOrder family (proxy only)

- **Purpose:** M-9 (liquidation cascade proxy).
- **Capture mode:** WS `<symbol>@forceOrder` (per-symbol) or
  `!forceOrder@arr` (all-market). No public historical archive.
- **Cadence:** at most one push per second per symbol;
  largest-per-1000 ms snapshot only.
- **Timestamp fields:** order trade time.
- **Sequence fields:** none reliable across the bounded
  snapshot.
- **Output raw family:** `microstructure_raw_forceorder_proxy_v001`.
- **Risk notes:** **proxy only** — never a complete liquidation
  tape. Smaller liquidations are not pushed when a larger one
  exists in the same 1000 ms window. The downstream label
  `proxy_warning = "largest_per_1000ms_snapshot_only"` is
  required (§13).
- **Governance:** M0; M-9 admissible only as context / regime
  overlay.

### 8.7 markPrice family (governance-blocked pending separate authorisation)

- **Purpose:** M-10 / M-11 / M-12 / M-14 context.
- **Capture mode:** WS `<symbol>@markPrice` and
  `!markPrice@arr` for live; REST `GET /fapi/v1/markPriceKlines`
  + `data.binance.vision/data/futures/um/{daily,monthly}/markPriceKlines/`
  for historical bars.
- **Cadence:** live stream per documented cadence; klines per
  bar.
- **Timestamp fields:** `E` (event time on WS); `open_time`
  (klines).
- **Sequence fields:** none.
- **Output raw family:** `microstructure_raw_markprice_v001`.
- **Risk notes:** subject to **Phase 3r §8** mark-price gap
  governance and **Phase 3v §8** stop-trigger-domain
  governance. Mark-price is **not** a runtime stop substitute
  in v1; the mark-price stop-domain forensics path remains
  blocked.
- **Governance:** consumption requires a separately authorised
  data-requirements memo.

### 8.8 indexPrice family

- **Purpose:** optional context.
- **Capture mode:** WS `<pair>@indexPrice` for live; REST
  `GET /fapi/v1/indexPriceKlines` and bulk archive for
  historical bars.
- **Cadence:** live stream per documented cadence; klines per
  bar.
- **Timestamp fields:** `E` (event time on WS); `open_time`
  (klines).
- **Sequence fields:** none.
- **Output raw family:** subordinate to
  `microstructure_raw_markprice_v001` if combined; else
  optional independent family.
- **Risk notes:** composite proxy; per-pair, not per-venue.
- **Governance:** M0; context only.

### 8.9 fundingRate REST

- **Purpose:** M-10 funding context.
- **Capture mode:** REST `GET /fapi/v1/fundingRate` (project
  precedent on disk for v1 scope and Phase 4ac core symbols).
- **Cadence:** per funding event (typically every 4h or 8h
  depending on contract / settlement-frequency policy).
- **Timestamp fields:** `fundingTime`.
- **Sequence fields:** none.
- **Output raw family:** subordinate to
  `microstructure_metrics_oi_funding_v001`.
- **Risk notes:** D1-A precedent — funding is **context only**,
  not a directional trigger.
- **Governance:** existing project funding manifests already
  cover v1 scope; further families require separate
  authorisation.

### 8.10 openInterest REST snapshot

- **Purpose:** M-11 context (current OI).
- **Capture mode:** REST `GET /fapi/v1/openInterest` (snapshot
  endpoint; forward time-series via REST polling).
- **Cadence:** poll cadence chosen by future implementation;
  must respect IP rate-limit budget.
- **Timestamp fields:** snapshot time.
- **Sequence fields:** none.
- **Output raw family:** subordinate to
  `microstructure_metrics_oi_funding_v001`.
- **Risk notes:** **forward REST polling required for any
  time-series; there is no WebSocket stream for current OI.**
- **Governance:** Phase 4j §11 OI-subset governance applies if
  combined with `openInterestHist`.

### 8.11 openInterestHist REST

- **Purpose:** M-11 / M-12 / M-13 / M-14 context.
- **Capture mode:** REST `GET /futures/data/openInterestHist`;
  retains only the **latest 30 days**; forward extension via
  forward REST polling.
- **Cadence:** `period` ∈ {5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h,
  1d}; per-period polling.
- **Timestamp fields:** aggregated bucket time.
- **Sequence fields:** none.
- **Output raw family:**
  `microstructure_metrics_oi_funding_v001`.
- **Risk notes:** 30-day rolling retention limits historical
  reach to existing project precedents (Phase 4i) plus forward
  capture.
- **Governance:** **Phase 4j §11 OI-subset partial-eligibility
  rule** applies verbatim; per-bar exclusion of bars whose
  required OI fields are missing or invalid is binding for any
  future use.

### 8.12 Top-trader / global long-short ratios (REST)

- **Purpose:** positioning context (M-12 / M-13).
- **Capture mode:** REST
  `GET /futures/data/topLongShortAccountRatio`,
  `GET /futures/data/topLongShortPositionRatio`,
  `GET /futures/data/globalLongShortAccountRatio`. Recent only
  (~30 days); forward REST polling.
- **Cadence:** same `period` set as `openInterestHist`.
- **Timestamp fields:** aggregated bucket time.
- **Sequence fields:** none.
- **Output raw family:**
  `microstructure_metrics_oi_funding_v001`.
- **Risk notes:** 30-day window; rate limit per documentation.
- **Governance:** context only; no directional-trigger reuse.

### 8.13 takerlongshortRatio REST

- **Purpose:** M-5 (aggressive volume) bucket-level proxy.
- **Capture mode:** REST `GET /futures/data/takerlongshortRatio`.
  Recent only (~30 days); forward REST polling. aggTrades is
  the more granular alternative for forward research.
- **Cadence:** same `period` set as above; documented 1000 req
  / 5 min / IP limit.
- **Timestamp fields:** bucket time.
- **Sequence fields:** none.
- **Output raw family:**
  `microstructure_metrics_oi_funding_v001` (taker bucket).
- **Risk notes:** aggregated; 30-day window.
- **Governance:** M0; coarse alternative to aggTrades.

---

## 9. Explicit endpoint denylist

The following are **forbidden** at every layer of the capture
pipeline. They remain unauthorised; no future memo derived from
Phase 4au may add them without separate operator authorisation.

- All **private endpoints** (any path requiring an API key).
- All **authenticated endpoints** (any path requiring a signed
  request).
- The **user stream** and the **listenKey** lifecycle.
- The REST `GET /fapi/v1/forceOrders` user-scope endpoint
  (returns the calling user's own liquidations only; not
  market-wide).
- All **order placement** endpoints (e.g. `POST /fapi/v1/order`
  and friends).
- All **account** endpoints (e.g. `GET /fapi/v2/account` and
  friends).
- All **position** endpoints (e.g. `GET /fapi/v2/positionRisk`
  and friends).
- All **leverage / margin** endpoints (e.g.
  `POST /fapi/v1/leverage`, `POST /fapi/v1/marginType`).
- Any endpoint that requires API keys, signatures, or
  account-level scope.
- All **MCP** integrations, **Graphify** integrations,
  **`.mcp.json`** files, and credential-based integrations
  more broadly.

These remain explicitly unauthorised by Phase 4au and by every
prior governance phase. Any code path that could reach a
denylisted endpoint must be removed at design review by
construction.

---

## 10. Dataset family design

The following dataset families are defined **as design only**.
**None is created in Phase 4au.** Each row's
`research_eligible` defaults to `false`; the eligibility gate
(§22) is the only path that may flip it to `true` in a future,
separately-authorised phase.

### 10.1 `microstructure_raw_aggtrades_v001`

- **Purpose:** raw aggressive-trade events for M-5 / M-6.
- **Source:** WS `<symbol>@aggTrade`; REST `GET /fapi/v1/aggTrades`;
  bulk archive aggTrades.
- **Layer:** raw.
- **Partition keys:** symbol, UTC date.
- **File format:** JSONL.zst (raw stream record per line).
- **Timestamp fields:** `event_time_ms` (`E`),
  `transaction_time_ms` (`T`), `ingestion_time_ms`.
- **Sequence fields:** `agg_id` (`a`), first/last trade id.
- **Schema version field:** `schema_version = "v001"`.
- **Manifest requirement:** required (§13).
- **`research_eligible` default:** `false`.
- **Invalid-window behaviour:** sequence gap → resync window;
  duplicate `agg_id` → flag and quarantine (§21).
- **Governance constraints:** M0; no D1-A-style directional
  reuse; aggregation excludes insurance / ADL.

### 10.2 `microstructure_raw_depthdiff_v001`

- **Purpose:** raw diff-depth events for M-3 / M-4 / M-7 /
  M-8 / M-14.
- **Source:** WS `<symbol>@depth(@100/250/500ms)` plus paired
  REST `GET /fapi/v1/depth?limit=1000` snapshots (snapshot
  files stored alongside diff files).
- **Layer:** raw.
- **Partition keys:** symbol, UTC date.
- **File format:** JSONL.zst (one record per WS event); paired
  snapshot files in JSON.zst.
- **Timestamp fields:** `event_time_ms` (`E`),
  `transaction_time_ms` (`T`), `ingestion_time_ms`.
- **Sequence fields:** `U`, `u`, `pu`.
- **Schema version field:** `schema_version = "v001"`.
- **Manifest requirement:** required; manifest tracks both
  diff windows and the bracketing snapshot file.
- **`research_eligible` default:** `false`.
- **Invalid-window behaviour:** any `U/u/pu` mismatch → resync
  window from a fresh snapshot; gap recorded as
  `invalid_window`.
- **Governance constraints:** M0; full LOB reconstruction is
  a Lane C prerequisite; no rank-then-trade reduction.

### 10.3 `microstructure_raw_bookticker_v001`

- **Purpose:** raw best-bid/ask events for M-1 / M-2.
- **Source:** WS `<symbol>@bookTicker` and `!bookTicker`.
- **Layer:** raw.
- **Partition keys:** symbol, UTC date.
- **File format:** JSONL.zst.
- **Timestamp fields:** `event_time_ms` (`E`),
  `transaction_time_ms` (`T`), `ingestion_time_ms`.
- **Sequence fields:** `u`.
- **Schema version field:** `schema_version = "v001"`.
- **Manifest requirement:** required.
- **`research_eligible` default:** `false`.
- **Invalid-window behaviour:** `u` non-monotone → resync;
  impossible spread → quarantine and `invalid_window`.
- **Governance constraints:** M0; M-1 / M-2 admissible as
  context.

### 10.4 `microstructure_raw_forceorder_proxy_v001`

- **Purpose:** liquidation snapshot proxy for M-9.
- **Source:** WS `<symbol>@forceOrder` and `!forceOrder@arr`.
- **Layer:** raw.
- **Partition keys:** symbol, UTC date.
- **File format:** JSONL.zst.
- **Timestamp fields:** order trade time;
  `ingestion_time_ms`.
- **Sequence fields:** none reliable.
- **Schema version field:** `schema_version = "v001"`.
- **Manifest requirement:** required; manifest carries
  `proxy_warning = "largest_per_1000ms_snapshot_only"`.
- **`research_eligible` default:** `false`.
- **Invalid-window behaviour:** disconnect-driven gaps
  recorded; no synthesis; no completion claim.
- **Governance constraints:** M0; M-9 admissible as context /
  regime overlay only; never a directional trigger.

### 10.5 `microstructure_raw_markprice_v001`

- **Purpose:** mark-price live + bar context for M-10 / M-11
  / M-14.
- **Source:** WS `<symbol>@markPrice` / `!markPrice@arr`;
  REST `markPriceKlines` + bulk archive.
- **Layer:** raw.
- **Partition keys:** symbol, UTC date.
- **File format:** JSONL.zst (live) + Parquet (klines bulk).
- **Timestamp fields:** `event_time_ms` (`E`); `open_time`
  (klines); `ingestion_time_ms`.
- **Sequence fields:** none.
- **Schema version field:** `schema_version = "v001"`.
- **Manifest requirement:** required; subject to **Phase 3r §8**
  mark-price gap governance.
- **`research_eligible` default:** `false`; explicit
  `governance_labels = {"phase_3r_section_8":
  "mark_price_gap_exclusion_required"}`.
- **Invalid-window behaviour:** known upstream Binance
  maintenance gaps recorded as `invalid_windows` per
  Phase 3r §8.
- **Governance constraints:** subject to Phase 3r §8 and
  Phase 3v §8; consumption requires a separately authorised
  data-requirements memo. **Mark-price stop-domain forensics
  remains blocked.**

### 10.6 `microstructure_metrics_oi_funding_v001`

- **Purpose:** derived OI / funding / long-short / taker
  context series for M-10 / M-11 / M-12 / M-13 / M-14.
- **Source:** REST `fundingRate`, `openInterest`,
  `openInterestHist`, `topLongShortAccountRatio`,
  `topLongShortPositionRatio`, `globalLongShortAccountRatio`,
  `takerlongshortRatio`.
- **Layer:** normalized (REST polls flatten directly into
  Parquet; raw poll responses stored as JSONL.zst alongside
  for audit).
- **Partition keys:** symbol, UTC date, source endpoint.
- **File format:** Parquet (normalized) + JSONL.zst (audit
  raw).
- **Timestamp fields:** event / bucket time;
  `ingestion_time_ms`.
- **Sequence fields:** none (REST poll).
- **Schema version field:** `schema_version = "v001"`.
- **Manifest requirement:** required; carries
  `retention_warning = "rest_recent_only_30d"` for the
  recent-only families.
- **`research_eligible` default:** `false`; M-11 specifically
  governed by **Phase 4j §11** OI-subset partial-eligibility
  rule.
- **Invalid-window behaviour:** missing OI bar → exclude per
  Phase 4j §11; long-short ratio gap → record `invalid_window`
  with `reason = "rest_retention_gap"`.
- **Governance constraints:** funding is **context only**
  (D1-A precedent); Phase 4j §11 binding for OI subset use.

### 10.7 `microstructure_replay_lob_v001`

- **Purpose:** derived local-order-book replay state for M-3
  / M-4 / M-7 / M-8 (full LOB feature computation).
- **Source:** deterministic replay from
  `microstructure_raw_depthdiff_v001` snapshots + diffs.
- **Layer:** derived.
- **Partition keys:** symbol, UTC date, snapshot interval.
- **File format:** Parquet (event-time-aligned LOB state,
  top-N levels per row).
- **Timestamp fields:** `event_time_ms`,
  `replay_ingestion_time_ms`.
- **Sequence fields:** `replay_seq` (monotone within partition).
- **Schema version field:** `schema_version = "v001"`.
- **Manifest requirement:** required; carries
  `replay_config_hash` and `code_commit_sha`.
- **`research_eligible` default:** `false`.
- **Invalid-window behaviour:** any upstream
  `microstructure_raw_depthdiff_v001` invalid window
  propagates into the derived family verbatim;
  `research_eligible` cannot exceed the upstream eligibility.
- **Governance constraints:** M0; full LOB consumption
  admissible only as Lane C feasibility.

**None of these families is created by Phase 4au.** Creation
requires a future, separately-authorised implementation phase
that itself must satisfy M0 admissibility and the governance
boundaries restated in §35.

---

## 11. Storage layout specification

The future capture pipeline writes only into a **separate
namespace** under `data/microstructure/...`. It does **not**
write into the existing `data/raw/`, `data/normalized/`,
`data/derived/`, or `data/manifests/` paths used by Phase 2 /
3q / 4i / 4ac. **No directory is created by Phase 4au.**

### 11.1 Recommended path structure (design only)

```text
data/microstructure/raw/<family>/<symbol>/<yyyy>/<mm>/<dd>/<file>.jsonl.zst
data/microstructure/raw/<family>/<symbol>/<yyyy>/<mm>/<dd>/<file>.jsonl.zst.sha256
data/microstructure/normalized/<family>/<symbol>/<yyyy>/<mm>/<file>.parquet
data/microstructure/normalized/<family>/<symbol>/<yyyy>/<mm>/<file>.parquet.sha256
data/microstructure/derived/<family>/<symbol>/<yyyy>/<mm>/<file>.parquet
data/microstructure/derived/<family>/<symbol>/<yyyy>/<mm>/<file>.parquet.sha256
data/microstructure/manifests/<family>__v001.json
```

The `<file>` segment encodes a UTC date / hour boundary as
appropriate (raw: per-day or per-hour rotation; normalized:
per-day rotation; derived: per-day rotation).

### 11.2 Why a separate namespace

- Existing project data families (Phase 2 v002 klines /
  funding; Phase 3q v001-of-5m; Phase 4i 30m / 4h / metrics;
  Phase 4ac alt-symbol klines / funding) are committed to
  `data/raw/`, `data/normalized/`, `data/manifests/` and
  are gitignored at the repo root.
- Mixing a brand-new high-volume capture pipeline into the
  same namespace would risk accidentally writing into or near
  manifests with `research_eligible: true` on the locked v1
  scope.
- A separate `data/microstructure/...` namespace lets the
  capture pipeline operate without ever touching existing
  manifests; it also makes gitignore additions trivial (a
  single new `data/microstructure/` ignore line).

### 11.3 Discussion of an alternative shared namespace

A future implementation phase could in principle reuse
`data/raw/`, `data/normalized/`, `data/derived/`, and
`data/manifests/` for the new microstructure families. This
memo recommends **against** that for v1 capture for the reasons
in §11.2, but documents the option for completeness. If the
operator later prefers a shared namespace, the eligibility
gate (§22) and `governance_labels` field (§13) become the
binding safeguards.

### 11.4 Write-rule policy

- **Raw layer:** append-only; never rewritten; never deleted by
  the capture pipeline; rotation produces a new file in the
  same partition.
- **Normalized layer:** deterministic rebuild only; source-of-
  truth is the raw layer plus the `capture_config_hash`.
- **Derived layer:** deterministic replay from normalized;
  reproducible from `replay_config_hash` + `code_commit_sha`.
- **No writes to existing project data families** (Phase 2 /
  3q / 4i / 4ac manifests, parquet files, raw archives).
- **No manifest mutation** outside the new microstructure
  family namespace if a future implementation phase is ever
  authorised.

---

## 12. File format and compression design

### 12.1 Raw layer

- Format: JSON-Lines (one record per line) compressed with
  zstd (`.jsonl.zst`).
- Streaming-friendly: zstd supports framed streaming; partial
  reads are supported.
- Atomic write: write to `<file>.jsonl.zst.tmp`, fsync, rename
  to `<file>.jsonl.zst`, then write
  `<file>.jsonl.zst.sha256`. Files without a paired SHA256 are
  treated as incomplete and excluded by the manifest writer
  (§13) until SHA256 is paired.
- Recovery after partial writes: any `.tmp` file present at
  startup is deleted; the partial coverage window is recorded
  as an `invalid_window` (§21).
- Rotation: per-symbol per-UTC-day (and optionally per-hour for
  high-volume families like depth diff).

### 12.2 Normalized layer

- Format: Parquet with explicit schema; column types pinned
  per `schema_version`.
- Compression: zstd at the column level.
- Atomic write: same write-then-rename pattern as raw layer.
- Pairing: `.parquet.sha256` companion required.
- Rotation: per-symbol per-UTC-day partition.
- No in-place mutation; a deterministic rebuild may produce a
  new normalized file under a fresh `__vNNN` family when
  schema changes.

### 12.3 Derived layer

- Format: Parquet (preferred) or DuckDB-compatible table.
- Compression: zstd.
- Atomic write + SHA256 pairing.
- Rotation: per-symbol per-UTC-day partition.
- Replay metadata recorded in manifest (`replay_config_hash`,
  `code_commit_sha`).

### 12.4 Manifest layer

- Format: JSON (one manifest per family per version,
  `<family>__v001.json`).
- Atomic write (write-then-rename).
- Manifest is updated incrementally as files are written;
  every appended entry carries a paired SHA256 for the file
  it references.

### 12.5 No in-place mutation

No file in any of the four layers is mutated in place. Rebuild
or rebuild-with-schema-bump are the only ways to "change"
content downstream.

---

## 13. Manifest design specification

Future per-family manifests must include the following fields
at minimum. **No manifest is created by Phase 4au.**

```text
{
  "dataset_family":         "<family>",                   // e.g. microstructure_raw_aggtrades
  "version":                "v001",
  "symbol":                 "BTCUSDT",
  "source":                 "binance_usdm_futures_public",
  "endpoint":               "<canonical endpoint identifier>",
  "capture_mode":           "ws_live | rest_polling | bulk_archive | rest_snapshot | replay",
  "start_time_ms":          <UTC ms>,
  "end_time_ms":            <UTC ms>,
  "event_count":            <int>,
  "file_count":             <int>,
  "files": [
    {
      "path":               "<relative path>",
      "size_bytes":         <int>,
      "sha256":             "<hex>",
      "start_time_ms":      <UTC ms>,
      "end_time_ms":        <UTC ms>,
      "event_count":        <int>
    }
  ],
  "schema_version":         "v001",
  "endpoint_docs_reference":"<URL or doc id from Phase 4at>",
  "capture_config_hash":    "<hex>",
  "code_commit_sha":        "<git SHA at capture time>",
  "invalid_windows": [
    {
      "start_time_ms":      <UTC ms>,
      "end_time_ms":        <UTC ms>,
      "family":             "<family>",
      "symbol":             "BTCUSDT",
      "reason":             "<enum from §21>",
      "evidence":           "<short string>",
      "severity":           "info | warn | error",
      "downstream_eligibility_action": "exclude | flag | proxy_only"
    }
  ],
  "retention_warning":      "rest_recent_only_30d | none",
  "proxy_warning":          "largest_per_1000ms_snapshot_only | none",
  "governance_labels":      {
    "phase_3r_section_8":   "<value if applicable>",
    "phase_3v_section_8":   "<value if applicable>",
    "phase_4j_section_11":  "<value if applicable>"
  },
  "research_eligible":      false,
  "eligibility_gate_status": "pending | failed | passed_partial | passed_full"
}
```

### 13.1 Field discipline

- `dataset_family`, `version`, `symbol`, `source`, `endpoint`,
  `capture_mode` are immutable for the lifetime of a manifest.
- `start_time_ms` / `end_time_ms` extend forward only.
- `files[]` is append-only.
- `invalid_windows[]` is append-only.
- `research_eligible` defaults to `false` and may flip to
  `true` only via the eligibility gate (§22).
- `eligibility_gate_status` defaults to `pending`.
- `governance_labels` is the explicit place where Phase 3r §8 /
  Phase 3v §8 / Phase 4j §11 constraints are recorded.
- `retention_warning` records bounded REST retention
  (`openInterestHist` / long-short / taker REST families).
- `proxy_warning` records bounded liquidation visibility for
  `microstructure_raw_forceorder_proxy_v001`.

### 13.2 No actual manifest creation

No JSON manifest, no manifest skeleton, and no manifest schema
file is created in any directory by Phase 4au.

---

## 14. Schema design specification

Future per-family schemas are specified below. **No schema file
is created in Phase 4au.** Field types are illustrative; a
future implementation phase will pin types under
`schema_version = "v001"`.

### 14.1 aggTrades (`microstructure_raw_aggtrades_v001`)

Required:

- `event_time_ms` (int64; Binance `E`)
- `transaction_time_ms` (int64; Binance `T`)
- `ingestion_time_ms` (int64; capture-side wall clock UTC ms)
- `local_monotonic_ns` (int64; capture-side monotonic clock)
- `symbol` (string)
- `agg_id` (int64; Binance `a`)
- `first_trade_id` (int64; Binance `f`)
- `last_trade_id` (int64; Binance `l`)
- `price` (decimal as string; Binance `p`)
- `qty` (decimal as string; Binance `q`)
- `is_buyer_maker` (bool; Binance `m`)
- `schema_version` (string)

Optional:

- `nq` (decimal as string; effective 2025-12-31 onward; RPI-
  excluded normal quantity).

### 14.2 bookTicker (`microstructure_raw_bookticker_v001`)

Required:

- `event_time_ms`, `transaction_time_ms`, `ingestion_time_ms`,
  `local_monotonic_ns`, `symbol`, `update_id` (`u`),
  `bid_price`, `bid_qty`, `ask_price`, `ask_qty`,
  `schema_version`.

### 14.3 depthDiff (`microstructure_raw_depthdiff_v001`)

Required:

- `event_time_ms`, `transaction_time_ms`, `ingestion_time_ms`,
  `local_monotonic_ns`, `symbol`, `first_update_id` (`U`),
  `final_update_id` (`u`), `previous_final_update_id` (`pu`),
  `bids` (list of {price, qty}), `asks` (list of {price, qty}),
  `schema_version`.

### 14.4 depthSnapshot (paired with §14.3)

Required:

- `snapshot_time_ms`, `ingestion_time_ms`, `symbol`,
  `last_update_id`, `bids` (top-1000), `asks` (top-1000),
  `schema_version`.

### 14.5 forceOrder proxy
(`microstructure_raw_forceorder_proxy_v001`)

Required:

- `order_trade_time_ms`, `ingestion_time_ms`,
  `local_monotonic_ns`, `symbol`, `side`, `order_type`,
  `time_in_force`, `qty`, `price`, `avg_price`, `order_status`,
  `last_filled_qty`, `accumulated_filled_qty`, `schema_version`,
  `proxy_warning` (string literal
  `"largest_per_1000ms_snapshot_only"`).

### 14.6 markPrice (`microstructure_raw_markprice_v001`)

Required:

- `event_time_ms`, `ingestion_time_ms`, `symbol`, `mark_price`,
  `index_price`, `estimated_settle_price` (where applicable),
  `funding_rate` (where embedded in WS), `next_funding_time`,
  `schema_version`,
  `governance_labels.phase_3r_section_8` literal.

### 14.7 OI / funding metrics
(`microstructure_metrics_oi_funding_v001`)

Required, varies by source endpoint; see §8.9–§8.13. Common
columns:

- `bucket_time_ms` (or `funding_time_ms`),
  `ingestion_time_ms`, `symbol`, `endpoint`, `schema_version`,
  endpoint-specific value columns
  (`open_interest`, `open_interest_value`, `long_account`,
  `short_account`, `long_short_ratio`, `buy_sell_ratio`,
  `buy_vol`, `sell_vol`, `funding_rate`, `mark_price`).
- `governance_labels.phase_4j_section_11` literal where the
  OI subset rule applies.

### 14.8 Reconstructed LOB state
(`microstructure_replay_lob_v001`)

Required:

- `event_time_ms`, `replay_ingestion_time_ms`, `symbol`,
  `replay_seq`, `top_n` (int; e.g. 20), `bids` (top-N), `asks`
  (top-N), `mid_price`, `spread`, `imbalance_top_n`,
  `replay_config_hash`, `code_commit_sha`, `schema_version`.

### 14.9 Time discipline (cross-family)

Every raw-layer schema records `event_time_ms` and
`ingestion_time_ms` separately; `transaction_time_ms` is
preserved where Binance provides it (`T`); a capture-side
`local_monotonic_ns` is captured to support deterministic
replay of arrival ordering when WS event timestamps tie.

---

## 15. Timestamp discipline

The future capture pipeline must enforce the following timestamp
rules. **None implemented in Phase 4au.**

- **`event_time_ms`** (UTC ms): the canonical event timestamp
  (Binance `E` for WS events, `bucket_time` for REST aggregated
  endpoints, `funding_time` for funding events).
- **`transaction_time_ms`** (UTC ms): preserved verbatim when
  Binance provides it (e.g. `T` field on aggTrade /
  diff-depth / bookTicker WS events).
- **`ingestion_time_ms`** (UTC ms): wall-clock UTC ms at the
  capture process at the moment the event was received.
- **`local_monotonic_ns`** (int): monotonic-clock nanoseconds
  at receipt; used only to deterministically order events
  whose `event_time_ms` ties.
- **UTC canonicalization:** all timestamp fields are in UTC ms;
  no local-timezone storage anywhere in the pipeline.
- **Clock-skew detection:** a future health-check signal
  (§24) records the running difference
  `ingestion_time_ms − event_time_ms` per stream; persistent
  drift beyond a configured bound creates an `invalid_window`
  with `reason = "clock_skew"`.
- **No mixing event-time and ingestion-time in labels:** all
  labels (`bucket_time`, `bar_open_time`, etc.) are
  event-time-anchored. Ingestion-time is a diagnostic surface,
  not a label.
- **Future latency realism:** any future feature must declare
  whether it consumes `event_time_ms` or
  `ingestion_time_ms`-derived state. M0 admissibility (§30)
  requires latency realism.

---

## 16. Rate-limit and retry design

Rate-limit handling and retry are specified at the design
layer only. **No HTTP request is made by Phase 4au.**

### 16.1 Documented endpoint weights and budgets

- `funding-rate` and `funding-info` share a documented
  500 req / 5 min / IP pool (per Phase 4at §9 citations).
- `takerlongshortRatio` and `globalLongShortAccountRatio` share
  a documented 1000 req / 5 min / IP pool.
- `openInterestHist` / top-trader long-short ratios share a
  rolling 30-day retention (no rate-limit issue at typical
  research cadences but the retention limit is binding).
- General USDⓈ-M Futures REST has a `REQUEST_WEIGHT` IP-level
  budget (commonly reported as 2400 / minute in industry
  references; per-endpoint weights apply).

### 16.2 Per-endpoint request budget

A future implementation will maintain a per-endpoint request
budget per IP, with:

- a leaky-bucket or token-bucket counter scoped to the
  documented limit;
- pre-flight "budget remaining" check before every call;
- a hard stop if budget would be exceeded; the call is
  rescheduled.

### 16.3 IP-level limit handling

- The capture pipeline runs from a single IP per symbol set by
  default (no IP rotation; no IP-pool usage).
- If the IP-level `REQUEST_WEIGHT` budget is exceeded, the
  pipeline halts polling for a cooldown window and records an
  `invalid_window` for the affected coverage gap.

### 16.4 Backoff on 429 / 418

- HTTP 429 (rate-limit exceeded) → exponential backoff
  starting at 5 s and doubling up to a hard ceiling
  (e.g. 5 min); on resume, requests are queued in the order
  they were planned.
- HTTP 418 (IP banned) → permanent halt of the affected REST
  worker; operator alert via the dashboard health-check
  channel (§24); no automatic retry; the bann window is
  recorded as an `invalid_window` for the entire duration.

### 16.5 Retry limits

- Transient errors (5xx, network timeout) → up to N retries
  (e.g. N = 3) with jittered exponential backoff before the
  worker is considered failed.
- Failed worker → supervisor (component 1) restarts with a
  fresh state; the failure window is recorded.

### 16.6 REST polling cadence

- Per-endpoint cadence is set to the documented `period` (e.g.
  5 minutes for `openInterestHist period=5m`); polling does
  not exceed the documented cadence.

### 16.7 No hammering / no bypass

- No burst polling that would consume the entire IP-level
  budget on a single endpoint.
- No bypass via parallel IPs, proxies, or unauthenticated key
  rotation.
- **No API key usage.** All allowlisted endpoints are public
  and require no signature.

---

## 17. WebSocket connection design

WebSocket handling is specified at the design layer only. **No
WebSocket connection is opened by Phase 4au.**

- **Subscription model.** One worker per (symbol, stream) pair
  by default. A combined-stream URL
  (`wss://fstream.binance.com/stream?streams=<...>`) is
  acceptable for low-volume families if the worker carries
  per-stream demultiplexing. The default model is
  one-stream-per-worker for safety.
- **Reconnect policy.** Exponential backoff with jitter on
  disconnect; minimum 1 s, maximum 60 s; reconnect attempts
  are unbounded but the disconnect window is always recorded
  as an `invalid_window` until the first valid event after
  reconnect bracketed by a fresh REST snapshot (where
  applicable).
- **Heartbeat / stale-stream detection.** Binance documents
  WS server pings every 3 minutes with 10-minute pong
  expectation. The capture worker enforces a stricter local
  staleness threshold: if no event has been received within a
  configured window (e.g. 60 s for high-volume streams,
  longer for low-volume streams like forceOrder), the stream
  is treated as stale; an `invalid_window` is opened and the
  worker reconnects.
- **Event buffering.** Events are buffered in a bounded
  in-memory queue between the WS worker and the raw event
  writer; queue depth is exposed to the health-check reporter
  (§24).
- **Backpressure handling.** If the queue saturates, the
  worker prefers writing the **oldest** event first
  (FIFO discipline) and refuses new events until headroom is
  restored; persistent saturation causes a managed reconnect
  with `invalid_window` marking.
- **Persistence-before-processing discipline.** Events are
  persisted to raw storage **before** any normalisation,
  feature computation, or replay step. The normalizer
  (component 5) only consumes already-persisted raw files.
- **Gap marking.** Sequence-number gaps (aggTrade `a`;
  bookTicker `u`; diff-depth `U` / `u` / `pu`) trigger an
  `invalid_window` and a managed resync.
- **No order placement surface.** The WS workers subscribe
  only to allowlisted public market streams. They have no code
  path that could send an authenticated request, place an
  order, or open a user stream.

---

## 18. Local order-book reconstruction design

LOB reconstruction follows the official Binance procedure (per
Phase 4at §11). **None implemented by Phase 4au.**

### 18.1 Procedure

1. Open WS `<symbol>@depth` (or `@100ms` / `@500ms`).
2. Buffer incoming events.
3. Fetch REST `GET /fapi/v1/depth?symbol=...&limit=1000`.
4. Drop any buffered event where `u < lastUpdateId`.
5. The first replayed event must satisfy
   `U <= lastUpdateId AND u >= lastUpdateId`.
6. Subsequent events must have `pu == previous_event.u`. Any
   mismatch is a sequence gap → resync.
7. Apply each diff event to the local book (price-level update;
   remove level if quantity is 0).
8. Persist the reconstructed top-N book state per
   `replay_config` cadence (e.g. on every event, or every
   100 ms, or every 250 ms — choice is recorded in
   `replay_config_hash`).

### 18.2 Snapshot interval policy

- A fresh REST snapshot is fetched on capture start, on every
  resync after a sequence gap, and at a configured periodic
  interval (e.g. once per 4 hours per symbol) as a sanity
  cross-check.

### 18.3 Top-N retention policy

- The replay builder (component 6) stores the top-N levels (N
  configurable; default e.g. 20 or 50) per event-time row.
- Full-depth snapshots are retained at the raw layer; the
  derived layer keeps only top-N to bound storage.

### 18.4 Stale-book detection

- If no diff event is applied within a configured staleness
  window, the local book is marked stale; an `invalid_window`
  is opened until a fresh snapshot is fetched and the stream
  is resynced.

### 18.5 Impossible-spread checks

- After every diff application, the replay builder checks
  `best_ask >= best_bid`. Violation triggers an
  `invalid_window` with `reason = "impossible_spread"` and
  forces a resync.

### 18.6 Determinism

- Replay must be deterministic under a fixed
  `replay_config_hash` and `code_commit_sha`. Re-running the
  replay produces byte-identical derived files. Non-determinism
  is treated as a defect.

### 18.7 Phase 4au boundary

**No reconstruction is implemented or attempted by Phase 4au.**
The procedure is described only to inform any future Phase 4av
implementation plan and any further-future implementation
phase.

---

## 19. Liquidation proxy design

The future `microstructure_raw_forceorder_proxy_v001` family
must satisfy the following constraints. **None implemented by
Phase 4au.**

- **forceOrder largest-per-1000ms limitation** is preserved as
  a binding manifest label (`proxy_warning =
  "largest_per_1000ms_snapshot_only"`).
- **Proxy-only label.** Every downstream consumer must read
  the manifest's `proxy_warning` field and treat the data as
  proxy. Features that assume completeness are mis-specified.
- **No complete liquidation tape claim.** Documentation,
  research memos, and dashboards must never claim the
  forceOrder family is a complete liquidation tape.
- **No authenticated forceOrders REST use.** REST
  `/fapi/v1/forceOrders` is denylisted (§9).
- **Future correlation only with aggTrades / OI / price
  context.** Any M-9 study must combine the proxy with
  aggressive-flow, OI, and price-action signals; standalone
  liquidation features that assume completeness are forbidden.
- **No standalone liquidation strategy.** M-9 is admissible
  only as a context / regime overlay per the Phase 4at
  M0-admissibility table; never as a primary directional
  trigger.

---

## 20. OI / funding capture design

The future `microstructure_metrics_oi_funding_v001` family must
satisfy the following constraints. **None implemented by
Phase 4au.**

- **Funding history via REST.** `GET /fapi/v1/fundingRate`
  returns full history per symbol (project precedent on disk
  for v1 scope and Phase 4ac core symbols).
- **Current OI via REST polling.** `GET /fapi/v1/openInterest`
  is a snapshot; forward time-series construction requires
  forward REST polling.
- **OI historical statistics recent-only.**
  `GET /futures/data/openInterestHist` retains only the latest
  30 days; forward extension requires forward REST polling.
- **Long-short ratios recent-only.**
  `topLongShortAccountRatio`, `topLongShortPositionRatio`,
  `globalLongShortAccountRatio` retain only the latest 30 days.
- **takerlongshortRatio recent-only.** Retains only the latest
  30 days; aggTrades (§14.1) is the more granular alternative
  for forward research.
- **Phase 4j §11 OI subset governance.** Any future use of OI
  data must apply per-bar exclusion of bars whose required OI
  fields are missing or invalid; no silent forward fill,
  interpolation, imputation, or replacement; manifest
  `governance_labels.phase_4j_section_11` is the binding
  recorded constraint.
- **D1-A precedent — funding context only.** Funding is
  admissible as a **context lens** only; never as a directional
  trigger. The `governance_labels` manifest field records this
  binding boundary.

---

## 21. Invalid-window governance

Every gap, anomaly, or integrity failure produces an explicit
`invalid_window` manifest entry. **No silent forward-fill,
interpolation, imputation, or replacement** (Phase 3p §4.7 /
Phase 3r §8 / Phase 4j §11 precedent). **None implemented by
Phase 4au.**

### 21.1 Trigger taxonomy

Triggers are enumerated below. Each maps to a `reason` enum
value in the manifest entry.

- `missing_sequence` — sequence number gap (`a` / `u` /
  `pu`).
- `out_of_order_event` — event-time decreases unexpectedly
  beyond a tolerance.
- `duplicate_event` — same `agg_id` or same `(U, u, pu)`.
- `gap_after_reconnect` — WS reconnect crosses an unconfirmed
  sequence boundary.
- `snapshot_mismatch` — REST snapshot `lastUpdateId` does not
  bracket the first replayed diff event per the official
  Binance procedure.
- `clock_skew` — `ingestion_time_ms − event_time_ms` exceeds
  the configured drift bound.
- `symbol_mismatch` — WS event reports a symbol other than the
  subscribed symbol.
- `stale_stream` — no event received within the configured
  staleness window.
- `stale_book` — no diff applied within the configured
  staleness window.
- `impossible_spread` — `best_ask < best_bid`.
- `negative_size` — level quantity < 0.
- `zero_or_invalid_price` — price ≤ 0 or non-finite.
- `archive_checksum_mismatch` — `.CHECKSUM` companion fails
  SHA256.
- `rest_retention_gap` — REST endpoint returns less coverage
  than the requested window (e.g. `openInterestHist` 30-day
  truncation).
- `force_order_proxy_incompleteness` — any indication that
  multiple liquidations occurred in the same 1000 ms window;
  flagged but unresolvable at the public-stream layer.
- `failed_atomic_write` — `.tmp` file present at startup;
  partial write occurred.
- `partial_file_recovery_event` — partial file deleted on
  startup; the affected window is recorded.

### 21.2 Required entry fields

Every `invalid_window` entry carries:

```text
{
  "start_time_ms": <UTC ms>,
  "end_time_ms":   <UTC ms>,
  "family":        "<dataset family>",
  "symbol":        "BTCUSDT",
  "reason":        "<enum from §21.1>",
  "evidence":      "<short string; e.g. seq numbers, file path>",
  "severity":      "info | warn | error",
  "downstream_eligibility_action":
                    "exclude | flag | proxy_only"
}
```

### 21.3 Downstream eligibility action

- `exclude` — the affected window is excluded from any
  research consumption.
- `flag` — the window is consumable but flagged for sensitivity
  reporting.
- `proxy_only` — the window is consumable only under proxy
  governance (e.g. forceOrder).

---

## 22. Research eligibility gate

A future eligibility gate is specified for each manifest. **None
implemented by Phase 4au.**

### 22.1 Gate checks

The gate flips `research_eligible` from `false` to `true` only
if **all** of the following pass:

1. **Raw files present.** Every `files[]` entry has the
   referenced file on disk.
2. **Checksum pass.** Every `files[].sha256` matches the
   on-disk content.
3. **Schema validation pass.** Every file conforms to the
   declared `schema_version`.
4. **Timestamp sanity pass.** All `event_time_ms` values are
   monotone within partition (where the family expects
   monotone) or within tolerance.
5. **Sequence continuity pass.** `agg_id` / `u` / `pu`
   sequences contain no unrecorded gaps; every gap is
   represented in `invalid_windows[]`.
6. **Invalid-window threshold.** The fraction of capture
   coverage marked `invalid_window` (excluding `info` severity)
   does not exceed a per-family threshold (e.g. ≤ 5 % per
   month).
7. **Retention completeness label.** `retention_warning`
   accurately reflects bounded REST retention if applicable.
8. **Proxy limitation label.** `proxy_warning` is correctly
   set for `microstructure_raw_forceorder_proxy_v001`.
9. **Governance labels.** Phase 3r §8 / Phase 3v §8 / Phase 4j
   §11 labels are present and consistent with the family.
10. **Final research_eligible decision.** Only the gate may
    flip `research_eligible` to `true` and set
    `eligibility_gate_status = "passed_full"` (or
    `"passed_partial"` for governance-bounded families like
    OI subset under Phase 4j §11).

### 22.2 Gate output

The gate writes a structured eligibility-gate report
(per-family) recording every check's pass/fail status and the
final decision. The report is itself referenced by the
manifest (`eligibility_gate_status`).

### 22.3 Phase 4au boundary

No eligibility gate is implemented in Phase 4au. The gate is
specified at the design layer only.

---

## 23. Deterministic replay design

Replay must be deterministic at every layer transition. **None
implemented by Phase 4au.**

- **Raw → normalized replay.** Reading the same raw files in
  the same order with the same `capture_config_hash` produces
  byte-identical normalized files.
- **Normalized → derived replay.** Reading the same normalized
  files with the same `replay_config_hash` and
  `code_commit_sha` produces byte-identical derived files.
- **LOB replay (§18).** Same property: same diffs + same
  bracketing snapshot → same top-N LOB state stream.
- **Replay config hash.** A `replay_config_hash` records the
  full set of config inputs (top-N, snapshot interval,
  staleness bounds, schema version, etc.).
- **Reproducibility requirements.** A future research consumer
  can re-derive normalized / derived layers from raw + config
  hashes alone. No hidden state.
- **No ad-hoc reads.** Research code consumes derived layers
  through the replay pipeline only; ad-hoc reads of raw logs
  are forbidden.
- **Replay logs.** Every replay emits a structured replay log
  (start time, end time, source files, output files, config
  hash, code commit SHA, exit status).
- **Replay failure handling.** A failed replay halts before
  writing partial output; partial files are deleted; an
  `invalid_window` is recorded in the manifest with
  `reason = "failed_atomic_write"` if applicable.

---

## 24. Health-check and operator dashboard design

The future health-check reporter (component 8) emits the
following local signals; the operator dashboard (component 9)
displays them read-only. **None implemented by Phase 4au.**

- `last_event_time_per_stream` — UTC ms of the last event
  received per (symbol, stream).
- `ingestion_lag_per_stream` — running mean of
  `ingestion_time_ms − event_time_ms` per stream.
- `reconnect_count_per_stream` — running counter.
- `gap_count_per_stream` — running counter of detected
  sequence gaps.
- `invalid_window_count_per_family` — running counter.
- `disk_usage_per_layer` — disk usage per
  raw / normalized / derived / manifest layer.
- `file_write_lag` — time between event receipt and atomic
  rename completion.
- `rate_limit_status_per_endpoint` — running budget headroom
  for each REST endpoint.
- `per_symbol_stream_status` — connected / reconnecting /
  stale / failed / paused.

### 24.1 Local-only display

The dashboard is **local-only**. It runs on the same host as
the capture pipeline (or a trusted internal host) and does
**not** expose live trading or any exchange-write surface.

### 24.2 No remote alerting at this layer

Remote alerting (e.g. Telegram, n8n) is **out of scope** for
Phase 4au. A future implementation phase may add operator
notifications, but the design defaults to local-only.

### 24.3 No order panel

The dashboard has **no order-placement surface**, **no
authenticated-endpoint state**, **no leverage / margin
controls**, and **no kill-switch surface**. It is a pure
research-infrastructure status view.

---

## 25. Security and credential boundary

The future capture pipeline must satisfy the following security
boundary. **None implemented by Phase 4au; the boundary is
specified at the design layer only.**

- **No API keys.** No code path loads, requests, stores, or
  accepts a Binance API key.
- **No `.env` reads.** The capture process does not read any
  `.env` file by default. If a future configuration mechanism
  is needed, it must be a non-secret config file (e.g. a YAML
  file) without API keys, signatures, or credential material.
- **No authenticated endpoints.** Every endpoint in scope is
  public.
- **No private endpoints.**
- **No order endpoints.**
- **No leverage / margin endpoints.**
- **No user stream / listenKey lifecycle.**
- **No MCP / Graphify / `.mcp.json` integrations.**
- **No secrets in logs.** Structured logs never include any
  credential material. The public-only boundary makes this
  trivially safe — no signature is ever computed.

---

## 26. Runtime separation

The future capture pipeline is research infrastructure only.
**None implemented by Phase 4au.**

- **No imports from `prometheus.runtime`.**
- **No imports from `prometheus.execution`.**
- **No imports from `prometheus.persistence`.**
- **No runtime database writes.** The capture pipeline does not
  open the runtime SQLite database, read from it, or write to
  it.
- **No safety-state mutation.** The runtime safety state
  (kill-switch, runtime mode, exposure gates) is invisible to
  the capture pipeline.
- **No order-router contact.** The pipeline has no code path
  that could enqueue an order, even via a fake adapter.
- **Capture is research infrastructure only.** It exists to
  produce raw / normalized / derived market-data datasets for
  future research feasibility study.

---

## 27. Symbol and scope policy

The future capture pipeline operates against a predeclared
**symbol allowlist**. **None implemented by Phase 4au.**

- **BTCUSDT primary.** The default capture set is BTCUSDT
  (project-locked first-live symbol).
- **ETHUSDT comparison.** ETHUSDT is captured as comparison
  context only.
- **Phase 4ac core symbols only if separately authorised.**
  SOLUSDT / XRPUSDT / ADAUSDT (the Phase 4ac core symbol set)
  may be added later only if a separately-authorised
  symbol-extension memo is approved; the existing Phase 4ac
  klines / funding remain in the project's pre-existing data
  namespaces and are not affected.
- **No alt-symbol rerun of old strategies.** The Phase 4aa /
  Phase 4ad / Phase 4ae / Phase 4af / Phase 4ai precedents
  apply: no R3 / R2 / F1 / D1-A / V2 / G1 / C1 alt-symbol
  rerun.
- **No symbol mining.** A symbol-specific finding must arise
  from a predeclared mechanism-first hypothesis, not from
  observing residuals.
- **Symbol-specific future study requires mechanism-first
  justification.** Any future microstructure feasibility memo
  that proposes a symbol-specific feature must predeclare why
  the symbol's specific liquidity / derivatives structure
  creates the mechanism (per Phase 4as §13 / Phase 4at
  symbol policy).

---

## 28. Storage and hardware feasibility discussion

Qualitative estimates only; **no measurement performed by
Phase 4au**. Where Binance documentation is the source, the
citation is in Phase 4at (§9 / §10).

- **aggTrades** is **manageable historically** because the bulk
  archive at `data.binance.vision` covers the full history per
  symbol and forward catch-up is bounded by REST rate limits.
  Per-symbol monthly archive size is small (aggregated taker-
  side records).
- **Diff book depth and book ticker** are **high volume** —
  per-event records arrive at 100 / 250 / 500 ms cadence (diff)
  and per-best-change cadence (bookTicker). Per-symbol storage
  is in the range of gigabytes per day under reasonable
  compression (qualitative; no measurement). Storage tiers
  (raw → parquet → compacted) and a retention policy are the
  binding controls.
- **forceOrder** is **low volume** because of the
  largest-per-1000 ms snapshot bound. Per-symbol per-day
  storage is small but the dataset is fundamentally a proxy.
- **OI / funding / long-short / takerlongshortRatio** is
  **low volume**: REST polls at the documented `period`
  cadence produce a small number of records per day per
  endpoint per symbol.
- **Compression and partitioning.** zstd compression (raw and
  Parquet) plus per-symbol per-UTC-day partitioning keeps
  storage bounded and supports streaming reads.
- **Retention policy.** A future implementation phase will set
  a per-family retention policy (e.g. raw aggTrades retained
  for 24 months on disk; older months archived offline; full
  reproducibility from the public archive remains the safety
  net).
- **Operator hardware.** A modest server / NUC can plausibly
  run BTCUSDT + ETHUSDT depth-diff + bookTicker + aggTrade +
  forceOrder + REST polling without exotic hardware. Numeric
  sizing requires a future implementation-sizing memo if
  needed; Phase 4au makes no firm numeric commitment.

---

## 29. Validation / anti-overfitting implications

The future capture pipeline must preserve the project's
existing validity / anti-overfitting discipline. None of the
following is authorised by Phase 4au; the requirements are
recorded for future memos that may follow.

- **Chronological validation.** Time-series labels are not
  shuffled; holdouts are chronological with explicit UTC date
  boundaries.
- **No random shuffling.** Standard k-fold CV is inappropriate;
  CSCV / DSR / PBO per Bailey & López de Prado is the
  precedent.
- **No symbol / window mining.** A symbol-specific finding
  must arise from a predeclared hypothesis; window changes do
  not rescue cooled-down candidates.
- **Latency realism.** Decision latency for microstructure
  signals must be modelled (milliseconds for HF; seconds for
  context use); zero-latency is not assumed.
- **Execution-cost realism.** §11.6 = 8 bps slippage per side
  is preserved verbatim; round-trip 16 bps. Microstructure is
  not exempt.
- **Negative controls.** Always-active, randomised, and
  non-mechanism baselines are mandatory.
- **Baseline comparisons.** A microstructure feature is
  admissible only if it can outperform a non-feature baseline
  on M0 admissibility and the predicted-Δ_R discipline.
- **Feature leakage checks.** A feature window that touches
  the prediction target boundary leaks; sequence-number
  validation, event-time vs bar-time separation, and
  predeclared lag conventions are mandatory.
- **No strategy until data quality and mechanism feasibility
  are established.** Capture is infrastructure; strategy work
  is gated independently by M0, the Phase 4m validity gate,
  the Phase 4t scoring matrix, the Phase 4ak post-null
  cooldown rule, and the Phase 4al refined no-rescue rule.

---

## 30. M0 governance implications

- **Capture design is admissible as infrastructure, not
  strategy.** Phase 4au is a research-infrastructure design
  memo. It does not propose a strategy candidate, a feature,
  or a mechanism-feasibility claim. M0 admissibility for
  strategy / mechanism feasibility remains a separate, future,
  separately-authorised concern.
- **Data capture does not imply edge.** The existence of a
  capture pipeline says nothing about whether any
  microstructure mechanism contains edge under §11.6. Any
  future feasibility memo must predeclare an explicit edge-
  rate hypothesis under M0 (Phase 4ak twelve-clause gate).
- **No cooled-down family is reopened.** Cooled-down lanes
  (per Phase 4ak post-null cooldown rule) remain cooled down.
  Capture does not give a cooled-down candidate a fresh path
  back into research.
- **No R3 / R2 / V1-arc rescue.** Capture must not be used as
  a backdoor to re-run R3 / R2 / R1a / R1b-narrow / H0 / F1
  / D1-A / V2 / G1 / C1 with new microstructure features
  added.
- **No D1-A funding-trigger reuse.** Funding is **context
  only**; the `governance_labels` manifest field records this
  binding boundary.
- **No G1-style regime filter without opportunity-rate
  controls.** Any future regime / filter feature must
  predeclare opportunity-rate viability (Phase 4u / Phase 4o
  / Phase 4r precedent — G1 failed because the regime gate
  intersected too sparsely with the entry rule).
- **No C1 / V2-style breakout wrapper hidden under
  microstructure.** Phase 4al refined no-rescue rule applies:
  no silent reduction of microstructure to a rank-then-trade
  variant of any cooled-down candidate.

---

## 31. Recommended next phase

The cleanest separately-authorised next move, **if the operator
chooses to continue after reviewing Phase 4au**, is:

**Phase 4av — Public-Only Microstructure Capture
Implementation Plan**

- **Type:** docs-only implementation plan, not implementation.
- **Purpose:** convert the Phase 4au design specification into
  a precise, file-by-file implementation plan covering: file
  list under a hypothetical `scripts/microstructure_*` /
  `src/prometheus/research/microstructure/*` namespace
  (without committing the files); module boundaries; CLI
  surface (entry-point names; flag parsing; subcommand layout
  for capture / normalize / replay / eligibility-gate); test
  matrix (unit, integration, golden-replay, manifest schema,
  invalid-window scenarios, rate-limit backoff); failure
  modes (every error class enumerated and its required
  behaviour); validation gates (which Phase 4au §22 checks
  must pass before `research_eligible` flips); and an
  implementation order (raw aggTrades first → bookTicker →
  depth diff + LOB replay → forceOrder proxy → metrics →
  health-check / dashboard hook). The plan does **not**
  implement capture, open any WebSocket, or download any
  archive.
- **Boundary:** docs-only; no endpoint calls; no data
  acquisition; no capture implementation; no order-book
  reconstruction implementation; no ML; no strategy
  candidate; no successor authorisation.
- **Authorisation status:** **NOT authorised by Phase 4au.**

### 31.1 Acceptable alternative recommendation

If the operator concludes that more review of the Phase 4au
design is needed before any implementation planning, **remain
paused** is an acceptable alternative.

### 31.2 What Phase 4au does NOT recommend

- No immediate implementation.
- No immediate capture.
- No immediate feature computation.
- No immediate ML or strategy work.
- No paper / shadow / live work.

---

## 32. Explicit non-recommendations

The following are **not** recommended by Phase 4au. Several are
explicitly forbidden by prior governance:

- No immediate implementation.
- No Binance endpoint calls.
- No WebSocket connections.
- No public-archive downloads.
- No capture implementation.
- No order-book reconstruction implementation.
- No replay implementation.
- No feature computation.
- No ML model.
- No new strategy candidate.
- No exit / entry design.
- No paper / live work.
- No credentials.
- No old-strategy alt-symbol rerun.
- No 5m research thread reopening.
- No verdict / lock revision.
- No M0 amendment.
- No D1-A funding-trigger reuse.
- No G1 / V2 / C1 rescue under a microstructure label.
- No authorisation of paper / shadow / live-readiness /
  deployment / exchange-write / production-key creation /
  authenticated APIs / private endpoints / public-endpoint
  calls in code / user stream / WebSocket implementation /
  MCP / Graphify / `.mcp.json` / credentials.

---

## 33. Implementation / governance review

### What changed?

- New file: this memo at
  `docs/00-meta/implementation-reports/2026-05-07_phase-4au_binance-microstructure-capture-design-specification.md`.
- Narrow update to `docs/00-meta/current-project-state.md` —
  Phase 4au narrative paragraph and "Current phase:" block
  update, with the prior Phase 4at block preserved as
  historical context (matching prior-phase convention).

### What did not change?

- No `src/prometheus/` modification.
- No test under `tests/` modified.
- No existing script under `scripts/` modified.
- No data file under `data/raw/`, `data/normalized/`,
  `data/derived/` modified.
- No manifest under `data/manifests/` modified or created.
- No actual dataset directory created under
  `data/microstructure/...`.
- No `research_eligible` flag flipped.
- No v003 created.
- No `.gitignore` modified.
- No specialist governance file modified beyond the narrow
  current-project-state update (no Phase 3r §8 / Phase 3v §8 /
  Phase 3w / Phase 4j §11 / Phase 4k / Phase 4p / Phase 4q /
  Phase 4v / Phase 4w / Phase 4ak / Phase 4al / Phase 4am /
  Phase 4an / Phase 4ao / Phase 4ap / Phase 4aq / Phase 4ar /
  Phase 4as / Phase 4at modification).
- No retained verdict revised.
- No project lock changed.
- No M0 amendment.
- No reopening of the 5m research thread.
- No data acquisition.
- No backtest run.
- No historical strategy script executed.
- No Phase 4aq script re-execution.
- No `data/research/` content committed.
- No Binance endpoint called.
- No WebSocket opened.
- No archive downloaded.
- No code, schema file, manifest skeleton, or schema-as-code
  artefact created.

### Were any locks, verdicts, or safety boundaries affected?

No. The retained verdict ledger and project locks are preserved
verbatim. M0 governance is unchanged. The 5m closure (Phase 3t)
is preserved. The cost lock (§11.6) and project locks (§1.7.3)
are preserved. The stop-trigger-domain governance (Phase 3v §8),
break-even / EMA slope / stagnation governance (Phase 3w §6 /
§7 / §8), mark-price gap governance (Phase 3r §8), and OI
subset governance (Phase 4j §11) are all preserved. The
Phase 4ak M0 gate, post-null cooldown rule, cooled-down
families list, and memo template are all preserved. The
Phase 4al refined no-rescue rule, the Phase 4am audit findings,
the Phase 4an inventory, the Phase 4ao harmonization, the
Phase 4ap forensic plan, the Phase 4aq computation, the
Phase 4ar interpretation, the Phase 4as mechanism map, and the
Phase 4at availability map are all preserved.

### Were any historical scripts, source files, existing data, manifests, or tests modified?

No. Phase 4au is a docs-only design specification memo.

### Is the phase mergeable as docs-only?

Yes. Phase 4au adds two markdown files under
`docs/00-meta/implementation-reports/` plus a narrow update to
`docs/00-meta/current-project-state.md`. Per the operator's
instruction in this prompt, **Phase 4au is not merged in this
prompt**.

---

## 34. Research interpretation review (plain English)

### What did this phase prove?

Phase 4au did not prove anything in the predictive-statistics
sense. As a docs-only design specification memo it documents,
in implementation-ready detail, a future public-only Binance
microstructure capture architecture covering nine cooperating
components, a thirteen-endpoint allowlist, an explicit denylist,
seven proposed dataset family designs, a four-layer storage
model with a recommended separate `data/microstructure/...`
namespace, a per-family schema design, a manifest design with
all required fields, an invalid-window taxonomy with seventeen
trigger reasons, an eligibility-gate design with ten checks,
deterministic-replay rules, a health-check / operator-dashboard
design, security / credential boundaries, runtime-separation
rules, and a symbol / scope policy.

### What did this phase not prove?

Phase 4au did not prove that any specific microstructure
mechanism contains edge. It did not run any computation. It did
not acquire any data. It did not call any Binance endpoint or
download any archive file. It did not authorise any successor
phase. It did not implement any capture, replay, feature, or
strategy. It did not amend M0. It did not modify any verdict
or lock. It did not create a strategy candidate.

### Which original questions did it answer?

The Phase 4au question — "Exactly what public-only Binance
microstructure capture architecture, endpoint allowlist,
storage layout, schema design, manifest discipline, invalid-
window governance, replay discipline, health-check model, and
safety boundary would need to exist before any future capture
implementation could be safely authorized?" — is answered
across §6 (capture design goals), §7 (architecture overview),
§8 (public-only endpoint allowlist), §9 (denylist), §10
(dataset family design), §11 (storage layout), §12 (file
format / compression), §13 (manifest design), §14 (schema
design), §15 (timestamp discipline), §16 (rate-limit / retry),
§17 (WebSocket connection), §18 (LOB reconstruction), §19
(liquidation proxy), §20 (OI / funding capture), §21 (invalid-
window governance), §22 (eligibility gate), §23 (replay), §24
(health-check / dashboard), §25 (security boundary), §26
(runtime separation), §27 (symbol / scope), §28 (storage /
hardware feasibility), §29 (validation / anti-overfitting),
§30 (M0 implications), §31 (recommended next phase Phase 4av).

### Which original questions remain open?

- Whether any of the M-1 → M-14 mechanisms contains edge
  under the project's locked cost realism. **This is not
  answered by Phase 4au and should not be answered by Phase 4au.**
- Whether Phase 4av (a future docs-only implementation plan)
  is the cleanest next move. The memo recommends Phase 4av
  but does **not** authorise it.
- Whether storage and operational overhead for live capture
  is acceptable for the project's host in numeric terms.
  Phase 4au makes only qualitative estimates; a future
  implementation-sizing memo would be required if a numeric
  budget is needed before Phase 4av or after.

### What does it mean for strategy research?

Phase 4au confirms that Lane A (Binance microstructure data
availability / capture feasibility) now has both an exhaustive
public-availability map (Phase 4at) and an
implementation-ready capture design specification (Phase 4au)
at the docs layer. Together they form a complete docs-only
foundation that any future implementation phase can build
against. The cooled-down families list, the six-candidate
rejection topology, the cost lock, the position lock, the
leverage lock, and the mark-price stop lock are all preserved.
M0 remains the binding admissibility framework.

### What does it mean for governance?

Phase 4au reaffirms the binding prospective governance: M0
admissibility, post-null cooldown, §11.6, §1.7.3, Phase 3r §8,
Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k,
Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak adoption,
Phase 4al refined no-rescue + §13 / §14, Phase 4am §11.A audit
findings, Phase 4an inventory, Phase 4ao harmonization,
Phase 4ap forensic plan, Phase 4aq computation result preserved
as descriptive evidence only, Phase 4ar interpretation result
preserved as descriptive interpretation only, Phase 4as
mechanism-map result preserved as docs-only reset evidence
only, and Phase 4at availability map preserved as docs-only
feasibility evidence only. **None is amended.**

### What is the clean next step?

Operator review of Phase 4au. **No successor phase is
authorised by Phase 4au.** Acceptable separately-authorised
future options include remain paused (recommended), Phase 4av
as a docs-only public-only microstructure capture
implementation plan, or further docs-only governance memos on
precise governance questions. None is started or authorised by
Phase 4au.

### What should we not do yet?

- No data acquisition.
- No Binance endpoint calls.
- No public-archive downloads.
- No WebSocket connections.
- No capture implementation.
- No order-book reconstruction implementation.
- No replay implementation.
- No feature implementation.
- No ML model.
- No new strategy candidate.
- No exit / entry design.
- No verdict / lock revision.
- No M0 amendment.
- No reopening of the 5m research thread.
- No 5m / 1m / aggTrades / tick / mark-price / order-book
  acquisition.
- No paper / shadow / live-readiness / deployment /
  exchange-write / production-key creation / authenticated
  APIs / private endpoints / user stream / WebSocket
  implementation / MCP / Graphify / `.mcp.json` / credentials.

---

## 35. Preserved verdicts, locks, and no-rescue constraints

### Retained verdict ledger (preserved verbatim)

- **H0** — FRAMEWORK ANCHOR.
- **R3** — BASELINE-OF-RECORD.
- **R1a** — RETAINED — NON-LEADING.
- **R1b-narrow** — RETAINED — NON-LEADING.
- **R2** — FAILED — §11.6.
- **F1** — HARD REJECT.
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL.
- **5m research thread** — operationally CLOSED (Phase 3t).
- **V2** — HARD REJECT — terminal for V2 first-spec.
- **G1** — HARD REJECT — terminal for G1 first-spec.
- **C1** — HARD REJECT — terminal for C1 first-spec.

### Project locks (preserved verbatim)

- **§11.6** = 8 bps slippage per side; round-trip = 16 bps.
- **§1.7.3** = 0.25 % risk; 2× leverage cap; one position max;
  mark-price stops where applicable.
- **Phase 3r §8** mark-price gap governance.
- **Phase 3v §8** stop-trigger-domain governance.
- **Phase 3w §6 / §7 / §8** break-even / EMA slope /
  stagnation governance.
- **Phase 4j §11** metrics OI-subset partial-eligibility rule.
- **Phase 4k** V2 backtest-plan methodology.
- **Phase 4p** G1 strategy-spec memo.
- **Phase 4q** G1 backtest-plan methodology.
- **Phase 4v** C1 strategy-spec memo.
- **Phase 4w** C1 backtest-plan methodology.
- **Phase 4ak** M0 mechanism-admissibility gate adoption
  (twelve clauses + post-null cooldown + cooled-down families
  list + memo template).
- **Phase 4al** refined no-rescue rule + §13 future-phase
  boundary + §14 data-resolution hierarchy.
- **Phase 4am** §11.A audit findings.
- **Phase 4an** historical-trade-population exit-path inventory.
- **Phase 4ao** exit-path methodology / artefact harmonization.
- **Phase 4ap** V1-Arc Exit-Path Forensic Plan.
- **Phase 4aq** computation result preserved as descriptive
  evidence only.
- **Phase 4ar** interpretation result preserved as descriptive
  interpretation only.
- **Phase 4as** mechanism-map result preserved as docs-only
  reset evidence only.
- **Phase 4at** availability / capture-feasibility result
  preserved as docs-only feasibility evidence only.

### No-rescue constraints (preserved)

- No R3-prime / R2-prime / R1a-prime / R1b-narrow-prime /
  H0-prime / F1-prime / D1-A-prime / D1-B / V2-prime /
  V2-narrow / V2-relaxed / V2 hybrid / G1-prime / G1-narrow /
  G1-extension / G1 hybrid / C1-prime / C1-narrow /
  C1-extension / C1 hybrid / V1-D1 / F1-D1 / any cross-strategy
  hybrid.
- No window / threshold / parameter mining from Phase 4l /
  Phase 4r / Phase 4x forensic numbers.
- No reopening of the 5m research thread.
- No silent reduction of microstructure to a rank-then-trade
  variant of any cooled-down candidate.
- No microstructure use of optional metrics ratio columns
  outside Phase 4j §11.
- No D1-A reuse as a directional trigger; funding remains a
  context lens only if ever used.

### Boundaries not altered

- No M0 amendment.
- No Phase 4m 18-requirement validity-gate amendment.
- No Phase 4t 10-dimension scoring-matrix amendment.
- No Phase 4u opportunity-rate-vs-edge-rate amendment.
- No Phase 4w negative-baseline / PBO / DSR / CSCV amendment.
- No Phase 4z framework adoption.
- No Phase 4al / Phase 4am audit-finding amendment.
- No Phase 4an / Phase 4ao / Phase 4ap / Phase 4aq /
  Phase 4ar / Phase 4as / Phase 4at amendment.

---

## 36. Final status

Phase 4au is complete on branch
`phase-4au/binance-microstructure-capture-design-specification`.

- **Memo:** this file.
- **Closeout:** to be added at
  `docs/00-meta/implementation-reports/2026-05-07_phase-4au_closeout.md`
  in the next commit on this branch.
- **Successor authorisation:** none. **Phase 4av / Phase 5 /
  Phase 4 canonical / paper / shadow / live-readiness /
  deployment / exchange-write / production-key / authenticated
  APIs / private endpoints / user stream / WebSocket
  implementation / MCP / Graphify / `.mcp.json` / credentials
  all remain unauthorised.** Acquisition of 5m / 1m /
  aggTrades / tick / mark-price 30m / 4h / order-book data
  also remains unauthorised.
- **Recommended state:** **paused** unless the operator
  separately authorises a future phase. The merge of Phase 4au
  into `main` is itself a separate operator decision and is
  **not** performed by this prompt.

## End of Phase 4au memo
