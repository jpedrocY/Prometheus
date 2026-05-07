# Phase 4at — Binance Microstructure Data Availability and Capture Feasibility Memo

## Phase identity

- Phase ID: **4at**.
- Phase title: **Binance Microstructure Data Availability and Capture Feasibility Memo**.
- Type: docs-only Binance microstructure / derivatives-flow data
  availability and capture-feasibility memo.
- Authority: separately operator-authorized as a docs-only
  feasibility phase only.
- Branch: `phase-4at/binance-microstructure-data-availability-capture-feasibility`.
- Base SHA (main at branch creation):
  `2bc7a04f5685e6c0ab5b5a45f9d1719943b29be8`.
- Phase 4at memo commit SHA: recorded in this phase's closeout
  once this memo is committed.

---

## 1. Executive summary

Phase 4as reset the Prometheus research program toward
Binance-native crypto microstructure and derivatives-flow
mechanisms after Phase 4ar closed the V1 / exit-rescue arc as
descriptive evidence only. Phase 4as mapped fourteen mechanisms
(M-1..M-14) conceptually and ranked five lanes (A → B → C → D → E)
without authorising any acquisition, capture, feature, model, or
strategy. Phase 4at is the separately-authorised next docs-only
phase recommended by Phase 4as. Its purpose is to translate
Phase 4as §9 into a precise Binance public market-data
availability and capture-feasibility map *before* any future
acquisition or capture phase is ever authorised.

Phase 4at's central conclusion (qualitative; no acquisition):

- A substantial subset of Binance USDⓈ-M Futures public
  market-data is **already available historically** via either
  REST endpoints or the bulk archive at `data.binance.vision`
  (klines, mark-price klines, premium-index klines, index-price
  klines, aggTrades, raw trades, funding-rate history, current
  open interest).
- Several derivatives-flow datasets (`openInterestHist`,
  `takerlongshortRatio`, top-trader long/short account and
  position ratios, global long/short account ratio) are exposed
  via REST but **retain only the latest 30 days** per the
  endpoint description and therefore require **forward live
  capture** for any extended history.
- Top-of-book / partial-book / diff-book / book-ticker /
  liquidation snapshot streams are **WebSocket-only**, with no
  Binance public historical archive at full granularity for
  derivatives. Anything beyond the existing `klines` / `markPrice`
  / `premiumIndex` / aggTrades horizon would require a future,
  separately-authorised live capture process.
- Liquidation visibility is **bounded by design**: the
  `forceOrder` snapshot stream pushes only the largest
  liquidation order per 1000 ms per symbol; the REST
  `/fapi/v1/forceOrders` endpoint is **user-scope authenticated**
  and **not admissible for market-wide microstructure research**.
- Local order-book reconstruction from snapshot + diff-depth is
  *technically possible* but requires deterministic capture,
  sequence-number validation, gap detection, resync, invalid-
  window marking, replay, and substantial storage discipline.
  None of that is implemented here.

Phase 4at **does not** acquire data, call any Binance endpoint,
download any archive, open any WebSocket, modify endpoint code,
implement capture, implement features, run scripts, modify
manifests, modify governance, modify retained verdicts or
project locks, or authorise any successor phase.

The recommendation is to **remain paused** unless the operator
separately authorises a docs-only **Phase 4au — Binance
Microstructure Capture Design Specification Memo**, which would
define an implementation design for public-only capture without
implementing it. **Phase 4au is not authorised by Phase 4at.**

All retained verdicts and project locks are preserved verbatim.
M0 governance, the post-null cooldown rule, the cooled-down
families list, the Phase 4al refined no-rescue rule, the Phase 4t
10-dimension scoring matrix, the Phase 4m 18-requirement validity
gate, the Phase 3t 5m closure, §11.6, and §1.7.3 are all binding
and unchanged.

---

## 2. Scope and explicit non-scope

### In scope

- A docs-only **availability and capture-feasibility map** for
  Binance USDⓈ-M Futures public market data relevant to the
  Phase 4as M-1..M-14 mechanism set.
- A historical-vs-live-capture **classification matrix** for
  every relevant data family, using the eight classifications
  named in this memo (see §7).
- A Binance public-archive map (`data.binance.vision` /
  `binance-public-data`).
- A REST market-data map (with citations to official Binance
  Open Platform docs).
- A WebSocket market-stream map (with citations).
- A local order-book reconstruction feasibility discussion.
- A liquidation data feasibility discussion.
- An open-interest / funding feasibility discussion.
- An aggressive-volume / order-flow feasibility discussion.
- A future capture-design requirements list (design only;
  not implemented here).
- A proposed list of future dataset family names (names only;
  not created).
- A data-quality / invalid-window governance list for any
  future capture phase.
- M0 admissibility implications per data family.
- Research validity / anti-overfitting requirements.
- A recommended next phase and explicit non-recommendations.
- Implementation / governance review.
- Plain-English research interpretation review.
- Explicit preservation of all retained verdicts, project
  locks, and no-rescue constraints.

### Out of scope (forbidden in Phase 4at)

- No data acquisition.
- No Binance endpoint calls.
- No public-archive downloads.
- No WebSocket connections.
- No endpoint code creation or modification.
- No capture implementation.
- No feature implementation.
- No backtest or historical strategy script execution.
- No Phase 4aq rerun.
- No simulation.
- No predictive statistics computation.
- No source / test / script / data / manifest / governance /
  spec / threshold / lock change.
- No `.gitignore` change.
- No commit of any `data/research/` output.
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
- No authorisation of Phase 4au, Phase 5, Phase 4 canonical,
  paper / shadow, live-readiness, deployment, exchange-write,
  production keys, authenticated APIs, private endpoints, user
  stream, WebSocket, MCP, Graphify, `.mcp.json`, credentials,
  5m / 1m / aggTrades / tick-data / mark-price 30m / 4h, or
  order-book capture.

---

## 3. Repository verification summary

Repository state at branch creation:

```text
git status                 — clean working tree on main; only
                              gitignored transients
                              (.claude/scheduled_tasks.lock,
                              data/research/) untracked.
git branch --show-current  — main (before branch creation) /
                              phase-4at/... (after).
git log --oneline -16      — Phase 4as merged at 2bc7a04.
git rev-parse main         — 2bc7a04f5685e6c0ab5b5a45f9d1719943b29be8.
git rev-parse origin/main  — 2bc7a04f5685e6c0ab5b5a45f9d1719943b29be8.
```

Phase 4as files confirmed present on `main`:

- `docs/00-meta/implementation-reports/2026-05-06_phase-4as_crypto-microstructure-research-reset-mechanism-map.md`.
- `docs/00-meta/implementation-reports/2026-05-06_phase-4as_closeout.md`.
- `docs/00-meta/implementation-reports/2026-05-06_phase-4as_merge-closeout.md`.

`main` and `origin/main` are in sync. The working tree contains
no unexpected uncommitted change. `.claude/scheduled_tasks.lock`
and `data/research/` remain gitignored / transient.

Branch created:

```text
git checkout -b phase-4at/binance-microstructure-data-availability-capture-feasibility
```

---

## 4. Methodology

Phase 4at is a docs-only feasibility memo. It is built from:

- **static repository inspection** of committed docs (Phase 4as,
  Phase 4ar, Phase 4aq, Phase 4ap, Phase 4ao, Phase 4an,
  Phase 4al, Phase 4ak, Phase 3v §8, Phase 3r §8, Phase 4j §11,
  current-project-state, phase-gates, M0 governance);
- **public web / official documentation research** restricted to
  (a) official Binance USDⓈ-M Futures developer documentation,
  (b) the public Binance public-data repository
  (`github.com/binance/binance-public-data`) and bulk-archive
  endpoint (`data.binance.vision`), and (c) reputable academic
  / industry references relevant to local order-book
  reconstruction, order-flow imbalance, and overfitting /
  selection-bias literature.

Citations are concentrated in §6, §8, §9, §10, §11, §12, and
§19.

The memo does **not**:

- call any Binance endpoint;
- modify any endpoint code;
- acquire any data;
- inspect or modify local `data/research/` outputs;
- run any script (Phase 4aq's script or otherwise);
- implement any feature;
- perform any computation that yields predictive statistics;
- touch credentials, MCP, `.mcp.json`, or any exchange-write
  surface.

The memo follows the prior-phase docs-only convention used by
Phase 4d, 4e, 4f, 4g, 4h, 4j, 4k, 4m, 4n, 4o, 4p, 4q, 4s, 4t,
4u, 4v, 4w, 4y, 4z, 4aa, 4ab, 4ad, 4ag, 4ah, 4aj, 4ak, 4al,
4an, 4ao, 4ap, 4ar, and 4as (no `ruff` / `pytest` / `mypy`
execution because no code, test, or script is changed).

---

## 5. Phase 4as baseline (preserved)

Phase 4as established the binding context for Phase 4at. It is
preserved verbatim:

- the V1 / exit-rescue chapter is closed by Phase 4ar as
  descriptive evidence only;
- Phase 4aq showed favorable excursion existed but did not, on
  average, translate into positive realized `net_R` in the
  primary R-window default cells;
- the project's rule-based, lagging-OHLCV-indicator families
  (V1-arc, F1, D1-A, V2, G1, C1) have been rejected;
- Phase 4as widened the *next* admissibility question toward
  Binance-native microstructure / derivatives-flow mechanisms
  that the previous geometry never measured.

Phase 4as mapped fourteen conceptual mechanisms (**not strategies**;
not authorised):

- M-1 spread; M-2 top-of-book depth; M-3 order-book imbalance
  top-N; M-4 deeper-level depth imbalance; M-5 aggressive volume
  / taker imbalance; M-6 trade burst / volume impulse; M-7
  liquidity sweep / book consumption; M-8 book recovery /
  replenishment after sweep; M-9 liquidation cascade proxies
  (bounded visibility); M-10 funding-rate context (context only,
  not directional trigger); M-11 OI context (under Phase 4j §11);
  M-12 funding + OI interaction; M-13 funding + OI + aggressive-
  flow interaction; M-14 spread / depth / flow regime
  interaction.

Phase 4as ranked five lanes A → B → C → D → E, recommending
**Lane A — Binance microstructure data availability / capture
feasibility (docs-only)** as the cleanest next move. **Phase 4at
is the docs-only execution of Lane A.**

Phase 4as did **not** authorise any mechanism implementation,
data acquisition, capture, feature, ML model, strategy, paper
/ shadow / live-readiness / deployment / exchange-write /
production-key / credentials work. Phase 4at preserves all of
those boundaries verbatim.

---

## 6. Data family availability matrix

The following matrix enumerates the Binance USDⓈ-M Futures public
market-data families relevant to Phase 4as M-1..M-14, with their
sources, availability, and major limitations. **Citations point
to official Binance Open Platform documentation.** No endpoint
is called by Phase 4at.

The matrix uses these per-family fields:

- **Source** — the canonical Binance source (REST / WS /
  archive).
- **Hist** — historical availability (TRUE / PARTIAL / FALSE).
- **Live capture** — required for forward extension? (YES / NO /
  ALREADY-CAPTURED-BY-PROJECT).
- **Retention** — endpoint-side retention if applicable.
- **Symbol coverage** — per-symbol or all-market.
- **Timestamp / sequence** — key fields.
- **Update speed** — typical cadence.
- **Major limitation** — the binding constraint.
- **Phase 4as relevance** — which mechanisms it touches.
- **Future-acquisition status** — must be separately authorised.

### 6.1 aggTrades / aggregate trades

- Source: WS `<symbol>@aggTrade`; REST `GET /fapi/v1/aggTrades`;
  bulk archive `data/futures/um/{daily,monthly}/aggTrades/`
  ([Binance Open Platform — Aggregate Trade Streams](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Aggregate-Trade-Streams);
  [github.com — binance-public-data](https://github.com/binance/binance-public-data);
  [data.binance.vision — futures/um/daily/aggTrades](https://data.binance.vision/?prefix=data%2Ffutures%2Fum%2Fdaily%2FaggTrades%2F)).
- Hist: TRUE (bulk archive monthly + daily).
- Live capture: forward-only NEW additions require WS / REST
  catch-up; existing history is in archive.
- Retention: archive retains since launch (no advertised
  truncation in Binance public-data docs); REST returns most
  recent records when start/end omitted.
- Symbol coverage: per-symbol.
- Timestamp / sequence: aggregate-trade `id`, trade time `T`.
- Update speed: WS push every 100 ms (aggregated for same
  price + same taker side).
- Major limitation: insurance-fund and ADL trades are not
  aggregated; effective 2025-12-31 a new `nq` field excludes
  RPI orders.
- Phase 4as relevance: M-5 (aggressive volume / taker imbalance);
  M-6 (trade burst / volume impulse).
- Future-acquisition status: requires separate authorisation.

### 6.2 Raw trades

- Source: REST `GET /fapi/v1/trades` and `GET /fapi/v1/historicalTrades`;
  bulk archive `data/futures/um/{daily,monthly}/trades/`
  ([github.com — binance-public-data](https://github.com/binance/binance-public-data)).
- Hist: TRUE (bulk archive).
- Live capture: forward-only catch-up via REST.
- Retention: archive retains since launch.
- Symbol coverage: per-symbol.
- Timestamp / sequence: `id`, trade `time`.
- Update speed: REST query.
- Granularity note: raw trades are a more granular trade-level
  source, while aggTrades are a compressed / taker-side
  aggregation. For Prometheus microstructure research,
  aggTrades may still be preferred for Lane B because they are
  smaller, historically archived, and directly aligned with
  taker-side aggregation, but raw trades are not lower-
  resolution.
- Phase 4as relevance: M-5 / M-6 fallback / cross-check.
- Future-acquisition status: requires separate authorisation.

### 6.3 Klines (trade-price)

- Source: REST `GET /fapi/v1/klines`; WS `<symbol>@kline_<interval>`;
  bulk archive `data/futures/um/{daily,monthly}/klines/`
  ([Binance Open Platform — Kline Candlestick Data](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Kline-Candlestick-Data);
  [data.binance.vision — futures/um/daily/klines](https://data.binance.vision/?prefix=data%2Ffutures%2Fum%2Fdaily%2Fklines%2F)).
- Hist: TRUE (bulk archive; project precedent — Phase 2 v002 +
  Phase 4i `__v001` already cover BTCUSDT, ETHUSDT, and the
  Phase 4ac core symbol set at multiple intervals).
- Live capture: ALREADY-CAPTURED-BY-PROJECT for the locked
  symbol set; forward-only catch-up for new months.
- Retention: archive retains since contract launch.
- Symbol coverage: per-symbol.
- Timestamp / sequence: `open_time`.
- Update speed: REST query / WS push per bar.
- Major limitation: aggregated bar; loses sub-bar order.
- Phase 4as relevance: regime / cost-cell context for any
  microstructure feature; not a microstructure variable in
  itself.
- Future-acquisition status: existing project datasets cover
  the locked v1 scope; further families require separate
  authorisation.

### 6.4 Mark-price klines

- Source: REST `GET /fapi/v1/markPriceKlines`; bulk archive
  `data/futures/um/{daily,monthly}/markPriceKlines/`
  ([Binance Open Platform — Mark Price Kline Candlestick Data](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Mark-Price-Kline-Candlestick-Data)).
- Hist: TRUE (bulk archive); subject to Phase 3r §8 mark-price
  gap governance.
- Live capture: forward-only catch-up via REST.
- Retention: archive retains since launch.
- Symbol coverage: per-symbol.
- Timestamp / sequence: `open_time`.
- Update speed: REST query / WS push per bar.
- Major limitation: known upstream invalid windows (per
  Phase 3q / Phase 4i precedent — 2022-07-30/31, 2022-10-02,
  2023-02-24, 2023-11-10).
- Phase 4as relevance: M-10 / M-11 / M-12 / M-13 / M-14 context;
  stop-domain governance per Phase 3v §8.
- Future-acquisition status: requires separate authorisation;
  Phase 3r §8 invalid-window exclusion governance applies if
  ever consumed.

### 6.5 Premium-index klines

- Source: REST `GET /fapi/v1/premiumIndexKlines`; bulk archive
  `data/futures/um/{daily,monthly}/premiumIndexKlines/`
  ([Binance Open Platform — Premium Index Kline Data](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Premium-Index-Kline-Data)).
- Hist: TRUE (bulk archive).
- Live capture: forward-only catch-up via REST.
- Retention: archive retains since launch.
- Symbol coverage: per-symbol.
- Timestamp / sequence: `open_time`.
- Update speed: REST query / WS push per bar.
- Major limitation: derived quantity (mark - index); inherits
  any upstream gap pattern.
- Phase 4as relevance: M-10 / M-12 funding / context lens
  (premium / discount as context).
- Future-acquisition status: requires separate authorisation.

### 6.6 Index-price klines

- Source: REST `GET /fapi/v1/indexPriceKlines`; bulk archive
  `data/futures/um/{daily,monthly}/indexPriceKlines/`
  ([Binance Open Platform — Index Price Kline Candlestick Data](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Index-Price-Kline-Candlestick-Data)).
- Hist: TRUE (bulk archive).
- Live capture: forward-only catch-up.
- Retention: archive retains since launch.
- Symbol coverage: per-pair (e.g. `BTCUSDT`).
- Timestamp / sequence: `open_time`.
- Update speed: REST / WS per bar.
- Major limitation: composite index; not a per-venue tape.
- Phase 4as relevance: optional context only.
- Future-acquisition status: requires separate authorisation.

### 6.7 Funding-rate history

- Source: REST `GET /fapi/v1/fundingRate`
  ([Binance Open Platform — Get Funding Rate History](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History)).
- Hist: TRUE (REST returns historical funding events; project
  precedent — v002 funding history already on disk for BTCUSDT,
  ETHUSDT, and the Phase 4ac core symbol set).
- Live capture: forward-only catch-up via REST.
- Retention: REST `limit` default 500 / max 1000 per page;
  shares 500/5min/IP rate limit with `GET /fapi/v1/fundingInfo`.
- Symbol coverage: per-symbol.
- Timestamp / sequence: `fundingTime`.
- Update speed: per funding event (typically every 4h or 8h
  depending on contract / settlement-frequency policy).
- Major limitation: funding event cadence; sparse compared to
  trade events.
- Phase 4as relevance: M-10 (context only — not a directional
  trigger; D1-A precedent).
- Future-acquisition status: existing project datasets cover
  v1 scope; further families require separate authorisation.

### 6.8 Funding-info / context

- Source: REST `GET /fapi/v1/fundingInfo`
  ([Binance Open Platform — Get Funding Rate History](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History)
  shares the rate-limit pool with this endpoint).
- Hist: PARTIAL (snapshot of contract-level funding parameters;
  not a long-running history).
- Live capture: forward snapshots only.
- Retention: snapshot endpoint.
- Symbol coverage: contract-level.
- Timestamp / sequence: snapshot time.
- Update speed: snapshot.
- Major limitation: snapshot-only.
- Phase 4as relevance: M-10 context lens only.
- Future-acquisition status: requires separate authorisation.

### 6.9 Open interest (current)

- Source: REST `GET /fapi/v1/openInterest`
  ([Binance Open Platform — Open Interest](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Open-Interest)).
- Hist: FALSE (current snapshot only).
- Live capture: forward REST polling required for any
  time-series (this is a snapshot REST endpoint; there is no
  WebSocket stream for current OI).
- Retention: snapshot.
- Symbol coverage: per-symbol.
- Timestamp / sequence: snapshot time.
- Update speed: snapshot.
- Major limitation: must be polled.
- Phase 4as relevance: M-11 context.
- Future-acquisition status: requires separate authorisation.

### 6.10 Open interest historical statistics

- Source: REST `GET /futures/data/openInterestHist`
  ([Binance Open Platform — Open Interest Statistics](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Open-Interest-Statistics)).
- Hist: PARTIAL (only the **latest 30 days** retained per
  endpoint description).
- Live capture: required for any history beyond 30 days; project
  precedent — Phase 4i metrics datasets already hold a partial
  OI series under Phase 4j §11 OI-subset governance.
- Retention: 30 days.
- Symbol coverage: per-symbol.
- Timestamp / sequence: aggregated OI per `period` bucket.
- Update speed: REST query at `period` ∈
  {`5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `6h`, `12h`, `1d`}.
- Major limitation: 30-day rolling window.
- Phase 4as relevance: M-11 / M-12 / M-13 / M-14 context.
- Future-acquisition status: requires separate authorisation;
  Phase 4j §11 OI-subset governance applies.

### 6.11 Top-trader long/short account ratio

- Source: REST `GET /futures/data/topLongShortAccountRatio`
  ([Binance Open Platform — Top Trader Long Short Account Ratio](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Top-Long-Short-Account-Ratio)).
- Hist: PARTIAL (latest 30 days retained).
- Live capture: required for extended history.
- Retention: 30 days.
- Symbol coverage: per-symbol.
- Timestamp / sequence: per `period` bucket.
- Update speed: same `period` set as `openInterestHist`.
- Major limitation: 30-day window; rate limit
  1000 req / 5 min / IP per the public-endpoint family.
- Phase 4as relevance: derivatives positioning context (could
  inform a future M-12 / M-13 / M-14 study). Distinct from
  aggressive flow.
- Future-acquisition status: requires separate authorisation;
  must be admissible only as **context**, not as a directional
  trigger (D1-A precedent).

### 6.12 Top-trader long/short position ratio

- Source: REST `GET /futures/data/topLongShortPositionRatio`
  ([Binance Open Platform — Top Trader Long Short Position Ratio](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Top-Trader-Long-Short-Ratio)).
- Hist: PARTIAL (latest 30 days retained).
- Live capture: required for extended history.
- Retention: 30 days.
- Symbol coverage: per-symbol.
- Timestamp / sequence: per `period` bucket.
- Update speed: as above.
- Major limitation: 30-day window.
- Phase 4as relevance: positioning context.
- Future-acquisition status: requires separate authorisation;
  context-only.

### 6.13 Global long/short account ratio

- Source: REST `GET /futures/data/globalLongShortAccountRatio`
  ([Binance Open Platform — Long Short Ratio (USDⓈ-M)](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Long-Short-Ratio)).
- Hist: PARTIAL (latest 30 days retained).
- Live capture: required for extended history.
- Retention: 30 days.
- Symbol coverage: per-symbol.
- Timestamp / sequence: per `period` bucket.
- Update speed: as above.
- Major limitation: 30-day window.
- Phase 4as relevance: positioning context.
- Future-acquisition status: requires separate authorisation;
  context-only.

### 6.14 Taker buy/sell volume ratio

- Source: REST `GET /futures/data/takerlongshortRatio`
  ([Binance Open Platform — Taker BuySell Volume](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Taker-BuySell-Volume)).
- Hist: PARTIAL (latest 30 days retained).
- Live capture: required for extended history; aggTrade-derived
  taker flow is the more granular alternative for forward
  research.
- Retention: 30 days.
- Symbol coverage: per-symbol.
- Timestamp / sequence: per `period` bucket
  ({`5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `6h`, `12h`, `1d`});
  rate limit 1000 req / 5 min / IP per documentation.
- Update speed: bucket cadence.
- Major limitation: aggregated bucket; coarser than aggTrades;
  30-day window.
- Phase 4as relevance: M-5 (aggressive volume / taker imbalance;
  bucket-level proxy).
- Future-acquisition status: requires separate authorisation.

### 6.15 Liquidation / forceOrder

- Source: WS `<symbol>@forceOrder` and `!forceOrder@arr`
  (all-market) snapshot streams; REST
  `/fapi/v1/forceOrders` is **user-scope authenticated** and
  must NOT be used for market-wide research
  ([Binance Open Platform — Liquidation Order Streams](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Liquidation-Order-Streams)).
- Hist: FALSE (no Binance public archive of force orders).
- Live capture: required; bounded resolution.
- Retention: WS snapshot only — only the largest one
  liquidation order within 1000 ms is pushed per symbol; if no
  liquidation occurs in that window, no message is pushed.
- Symbol coverage: per-symbol or all-market.
- Timestamp / sequence: order trade time.
- Update speed: ≤ 1 push per second per symbol.
- Major limitation: bounded visibility (proxy only). REST is
  authenticated-user-scope and **AUTHENTICATED_USER_SCOPE_NOT_
  ADMISSIBLE_FOR_MARKET_RESEARCH**.
- Phase 4as relevance: M-9 (bounded-visibility liquidation
  cascade proxy).
- Future-acquisition status: requires separate authorisation;
  must be labelled **proxy only**, not a complete liquidation
  tape.

### 6.16 Book ticker (best bid/ask)

- Source: WS `<symbol>@bookTicker`; all-market `!bookTicker`
  ([Binance Open Platform — All Book Tickers Stream](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/All-Book-Tickers-Stream)).
- Hist: FALSE (no Binance public-archive book-ticker history at
  full granularity for derivatives).
- Live capture: required.
- Retention: live only.
- Symbol coverage: per-symbol or all-market.
- Timestamp / sequence: order-book `updateId` (`u`), event time
  `E`, transaction time `T`.
- Update speed: real-time on best bid/ask change.
- Major limitation: forward live capture only.
- Phase 4as relevance: M-1 (spread); M-2 (top-of-book depth).
- Future-acquisition status: requires separate authorisation.

### 6.17 Partial book depth

- Source: WS `<symbol>@depth5/10/20@100ms` (also 250 / 500 ms
  variants where available)
  ([Binance Open Platform — Partial Book Depth Streams](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Partial-Book-Depth-Streams)).
- Hist: FALSE (no Binance public-archive partial-depth history
  for derivatives).
- Live capture: required.
- Retention: live only.
- Symbol coverage: per-symbol.
- Timestamp / sequence: snapshot per push.
- Update speed: per stream cadence (100 / 250 / 500 ms).
- Major limitation: snapshot of top-N; RPI orders excluded.
- Phase 4as relevance: M-2 / M-3 (top-of-book / order-book
  imbalance) at top-N levels.
- Future-acquisition status: requires separate authorisation.

### 6.18 Diff book depth

- Source: WS `<symbol>@depth` (default 250 ms),
  `<symbol>@depth@500ms`, `<symbol>@depth@100ms`
  ([Binance Open Platform — Diff Book Depth Streams](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Diff-Book-Depth-Streams);
  [Binance Open Platform — How To Manage A Local Order Book Correctly](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/How-to-manage-a-local-order-book-correctly)).
- Hist: FALSE.
- Live capture: required (combined with REST snapshot for local
  reconstruction).
- Retention: live only.
- Symbol coverage: per-symbol.
- Timestamp / sequence: `U` (first update id), `u` (final update
  id), `pu` (previous final update id) — used for sequence-
  number validation against the snapshot.
- Update speed: 100 / 250 / 500 ms.
- Major limitation: state must be reconstructed from snapshot
  + diffs; gaps require resync.
- Phase 4as relevance: M-3 / M-4 / M-7 / M-8 / M-14.
- Future-acquisition status: requires separate authorisation.

### 6.19 REST depth snapshot

- Source: REST `GET /fapi/v1/depth?symbol=...&limit=1000` (top
  1000 levels supported)
  ([Binance Open Platform — How To Manage A Local Order Book Correctly](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/How-to-manage-a-local-order-book-correctly)).
- Hist: FALSE (snapshot only).
- Live capture: required for local order-book reconstruction
  start / resync.
- Retention: snapshot.
- Symbol coverage: per-symbol.
- Timestamp / sequence: `lastUpdateId`.
- Update speed: REST query.
- Major limitation: snapshot-only; must be combined with diff
  stream.
- Phase 4as relevance: M-3 / M-4 / M-7 / M-8 reconstruction
  starting point.
- Future-acquisition status: requires separate authorisation.

### 6.20 Mark-price stream

- Source: WS `<symbol>@markPrice` and `!markPrice@arr`
  ([Binance Open Platform — Mark Price](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Mark-Price)).
- Hist: PARTIAL (combined with markPriceKlines historical
  archive; live stream forward-only).
- Live capture: required for sub-bar mark-price events going
  forward.
- Retention: live only.
- Symbol coverage: per-symbol or all-market.
- Timestamp / sequence: event time.
- Update speed: per stream cadence.
- Major limitation: derived quantity; subject to Phase 3v §8
  stop-trigger-domain governance and Phase 3r §8 mark-price
  gap governance.
- Phase 4as relevance: M-10 / M-11 / M-12 context; mark-price
  stop-domain forensics is **blocked** under §1.7.3 and
  Phase 3r §8 unless separately authorised.
- Future-acquisition status: requires separate authorisation.

### 6.21 Composite index / index-price stream

- Source: WS `<pair>@indexPrice` (e.g. `btcusdt@indexPrice`).
- Hist: PARTIAL (indexPriceKlines archive provides historical
  bars; sub-bar live stream is forward-only).
- Live capture: required for sub-bar.
- Retention: live only.
- Symbol coverage: per-pair.
- Timestamp / sequence: event time.
- Update speed: per stream cadence.
- Major limitation: composite proxy.
- Phase 4as relevance: optional context.
- Future-acquisition status: requires separate authorisation.

### 6.22 Out-of-scope (private / authenticated)

- User stream / listenKey / private endpoints / authenticated
  REST (e.g. `GET /fapi/v1/forceOrders` user-scope) are
  **AUTHENTICATED_USER_SCOPE_NOT_ADMISSIBLE_FOR_MARKET_RESEARCH**
  and explicitly out of scope for Phase 4at and any future
  microstructure feasibility / capture phase. They remain
  available only for separately authorised live-runtime work,
  which is itself unauthorised.

---

## 7. Historical vs live-capture classification

This section assigns each Phase 4at-relevant data family one of
the eight predeclared classifications.

- **HISTORICAL_ARCHIVE_AVAILABLE** — bulk archive at
  `data.binance.vision` covers the family historically.
- **REST_HISTORY_AVAILABLE** — REST endpoint returns extended
  historical records.
- **REST_RECENT_ONLY** — REST endpoint returns only a recent
  rolling window.
- **WS_LIVE_CAPTURE_REQUIRED** — only obtainable via live WS
  capture; no historical archive at the required granularity.
- **AUTHENTICATED_USER_SCOPE_NOT_ADMISSIBLE_FOR_MARKET_RESEARCH**
  — endpoint exists but is user-scope authenticated; not
  admissible for market-wide research.
- **PUBLIC_PROXY_ONLY** — partial / bounded public visibility
  (e.g. `forceOrder` 1000 ms snapshot).
- **GOVERNANCE_BLOCKED_PENDING_SEPARATE_AUTHORIZATION** —
  acquisition / use is bounded by an existing project
  governance rule (e.g. Phase 3r §8 mark-price gap governance,
  Phase 4j §11 OI subset governance).
- **NOT_REQUIRED_FOR_CURRENT_MICROSTRUCTURE_RESET** — out of
  scope for Phase 4as / Phase 4at irrespective of availability.

### Classification matrix

| Data family | Classification | Notes |
|---|---|---|
| aggTrades (§6.1) | HISTORICAL_ARCHIVE_AVAILABLE | Bulk archive monthly + daily; forward catch-up via REST/WS. |
| Raw trades (§6.2) | HISTORICAL_ARCHIVE_AVAILABLE | Lower-resolution alternative. |
| Klines (§6.3) | HISTORICAL_ARCHIVE_AVAILABLE | Project precedent — Phase 2 v002 + Phase 4i `__v001`. |
| Mark-price klines (§6.4) | HISTORICAL_ARCHIVE_AVAILABLE + GOVERNANCE_BLOCKED_PENDING_SEPARATE_AUTHORIZATION | Phase 3r §8 invalid-window governance applies. |
| Premium-index klines (§6.5) | HISTORICAL_ARCHIVE_AVAILABLE | Derived; inherits gap pattern. |
| Index-price klines (§6.6) | HISTORICAL_ARCHIVE_AVAILABLE | Composite. |
| Funding rate history (§6.7) | REST_HISTORY_AVAILABLE | Project precedent on disk. |
| Funding-info (§6.8) | REST_RECENT_ONLY | Snapshot. |
| Current OI (§6.9) | REST_RECENT_ONLY (snapshot; future time-series would require forward REST polling) | Forward REST poll; no WebSocket stream for current OI. |
| OI historical statistics (§6.10) | REST_RECENT_ONLY (30 days) → WS_LIVE_CAPTURE_REQUIRED for forward extension + GOVERNANCE_BLOCKED_PENDING_SEPARATE_AUTHORIZATION (Phase 4j §11) | 30-day rolling. |
| Top-trader long/short account (§6.11) | REST_RECENT_ONLY (30 days) → WS_LIVE_CAPTURE_REQUIRED for forward extension | Context only. |
| Top-trader long/short position (§6.12) | REST_RECENT_ONLY (30 days) → WS_LIVE_CAPTURE_REQUIRED for forward extension | Context only. |
| Global long/short account (§6.13) | REST_RECENT_ONLY (30 days) → WS_LIVE_CAPTURE_REQUIRED for forward extension | Context only. |
| Taker buy/sell volume ratio (§6.14) | REST_RECENT_ONLY (30 days) → WS_LIVE_CAPTURE_REQUIRED for forward extension | aggTrades is the more granular alternative. |
| Liquidation / forceOrder WS (§6.15) | WS_LIVE_CAPTURE_REQUIRED + PUBLIC_PROXY_ONLY | Largest-per-1000 ms snapshot. |
| Liquidation / forceOrders REST (§6.15) | AUTHENTICATED_USER_SCOPE_NOT_ADMISSIBLE_FOR_MARKET_RESEARCH | Out of scope. |
| Book ticker (§6.16) | WS_LIVE_CAPTURE_REQUIRED | No public archive. |
| Partial book depth (§6.17) | WS_LIVE_CAPTURE_REQUIRED | No public archive. |
| Diff book depth (§6.18) | WS_LIVE_CAPTURE_REQUIRED | No public archive. |
| REST depth snapshot (§6.19) | WS_LIVE_CAPTURE_REQUIRED (combined w/ §6.18) | Snapshot only. |
| Mark-price stream (§6.20) | WS_LIVE_CAPTURE_REQUIRED + GOVERNANCE_BLOCKED_PENDING_SEPARATE_AUTHORIZATION | Phase 3r §8 / Phase 3v §8. |
| Index-price stream (§6.21) | WS_LIVE_CAPTURE_REQUIRED | Optional context. |
| User stream / private REST (§6.22) | AUTHENTICATED_USER_SCOPE_NOT_ADMISSIBLE_FOR_MARKET_RESEARCH | Out of scope; also NOT_REQUIRED_FOR_CURRENT_MICROSTRUCTURE_RESET. |

---

## 8. Binance public archive map

The public archive is available at `data.binance.vision` and the
companion repository
[`github.com/binance/binance-public-data`](https://github.com/binance/binance-public-data),
which documents directory layout, helper scripts, and the
relationship between archive content and REST endpoints.

### 8.1 Directory layout

For USDⓈ-M Futures the archive uses a hierarchical layout:

```text
data/futures/um/{daily, monthly}/{aggTrades, klines,
  markPriceKlines, premiumIndexKlines, indexPriceKlines,
  trades, ...}/<SYMBOL>/...
```

- Daily and monthly granularities are both provided
  ([data.binance.vision — futures/um/daily/aggTrades](https://data.binance.vision/?prefix=data%2Ffutures%2Fum%2Fdaily%2FaggTrades%2F);
  [data.binance.vision — futures/um/daily/klines](https://data.binance.vision/?prefix=data%2Ffutures%2Fum%2Fdaily%2Fklines%2F)).
- The aggTrades archive content matches the `GET /fapi/v1/aggTrades`
  REST endpoint output.
- The trades archive content matches the `GET /fapi/v1/trades` /
  `GET /fapi/v1/historicalTrades` endpoints.
- Klines / markPriceKlines / premiumIndexKlines / indexPriceKlines
  archives match their REST endpoints.

### 8.2 Checksum / integrity

Each archive file is paired with a `.CHECKSUM` companion that
records a SHA256 of the archive
([github.com — binance-public-data](https://github.com/binance/binance-public-data)).
The project's existing Phase 3q / Phase 4i / Phase 4ac
acquisition scripts already enforce SHA256 verification against
`.CHECKSUM` companions (project precedent). Phase 4at does not
download anything; integrity verification is part of the future
capture-design requirements (§15) only.

### 8.3 Archive limitations

- The public archive does **not** include partial / diff /
  book-ticker / forceOrder data at native granularity. Those are
  WS-only and must be captured forward.
- Some early archive months may have known invalid windows
  (e.g. SOLUSDT / XRPUSDT early-2022 gaps per Phase 4ac
  precedent; mark-price upstream gaps per Phase 3q / Phase 4i
  precedent). Phase 3r §8 / Phase 4ad rules apply to any future
  consumption.
- New families (e.g. metrics) may be added or removed by Binance
  over time; any future capture phase must verify availability
  before relying on a family.

### 8.4 What Phase 4at does not download

Phase 4at does not download any file from `data.binance.vision`
or any other source. The archive map is descriptive only.

---

## 9. REST market-data map

Phase 4as already enumerated the principal REST endpoints
relevant to microstructure. Phase 4at extends and refines that
map with citations to official Binance Open Platform docs. **No
endpoint is called by Phase 4at.**

| Endpoint | Path | History | Retention | Notes |
|---|---|---|---|---|
| Aggregate trades | `GET /fapi/v1/aggTrades` | TRUE | n/a | Same content as bulk archive aggTrades. |
| Raw trades | `GET /fapi/v1/trades` / `GET /fapi/v1/historicalTrades` | TRUE | n/a | Same content as bulk archive trades. |
| Klines | `GET /fapi/v1/klines` | TRUE | n/a | Bulk archive available. |
| Mark-price klines | `GET /fapi/v1/markPriceKlines` | TRUE | n/a | Bulk archive available; Phase 3r §8 governance. |
| Premium-index klines | `GET /fapi/v1/premiumIndexKlines` | TRUE | n/a | Bulk archive available. |
| Index-price klines | `GET /fapi/v1/indexPriceKlines` | TRUE | n/a | Bulk archive available. |
| Funding-rate history | `GET /fapi/v1/fundingRate` | TRUE | n/a (per-page paged) | 500/5min/IP shared with `fundingInfo`. |
| Funding info | `GET /fapi/v1/fundingInfo` | snapshot | snapshot | Shares rate-limit pool. |
| Current OI | `GET /fapi/v1/openInterest` | snapshot | snapshot | Per-symbol. |
| OI historical statistics | `GET /futures/data/openInterestHist` | PARTIAL | **30 days** | `period` = 5m/15m/30m/1h/2h/4h/6h/12h/1d. |
| Top-trader long/short account | `GET /futures/data/topLongShortAccountRatio` | PARTIAL | 30 days | Same `period` set. |
| Top-trader long/short position | `GET /futures/data/topLongShortPositionRatio` | PARTIAL | 30 days | Same `period` set. |
| Global long/short account | `GET /futures/data/globalLongShortAccountRatio` | PARTIAL | 30 days | Same `period` set. |
| Taker buy/sell volume | `GET /futures/data/takerlongshortRatio` | PARTIAL | 30 days | Same `period` set; 1000 req / 5min / IP. |
| Order book snapshot | `GET /fapi/v1/depth` | snapshot | snapshot | `limit=1000` for top-1000 levels. |
| Mark price | `GET /fapi/v1/premiumIndex` and friends | snapshot / TRUE via klines | n/a | Phase 3r §8 governance applies. |

Citations: aggregate trade endpoint and bulk-archive parity
([github.com — binance-public-data](https://github.com/binance/binance-public-data)),
funding-rate history
([Binance Open Platform — Get Funding Rate History](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History)),
open interest endpoints
([Binance Open Platform — Open Interest](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Open-Interest);
[Binance Open Platform — Open Interest Statistics](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Open-Interest-Statistics)),
top-trader / global long-short ratios
([Binance Open Platform — Top Trader Long Short Account Ratio](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Top-Long-Short-Account-Ratio);
[Binance Open Platform — Top Trader Long Short Position Ratio](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Top-Trader-Long-Short-Ratio);
[Binance Open Platform — Long Short Ratio (USDⓈ-M)](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Long-Short-Ratio)),
taker buy/sell volume ratio
([Binance Open Platform — Taker BuySell Volume](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Taker-BuySell-Volume)),
mark-price / premium-index / index-price klines
([Binance Open Platform — Mark Price Kline Candlestick Data](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Mark-Price-Kline-Candlestick-Data);
[Binance Open Platform — Premium Index Kline Data](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Premium-Index-Kline-Data);
[Binance Open Platform — Index Price Kline Candlestick Data](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Index-Price-Kline-Candlestick-Data)).

### 9.1 Rate-limit and request-window observations

- USDⓈ-M Futures REST has a `REQUEST_WEIGHT` rate limit at the
  IP level (the 2400 / minute observation reported in industry
  references is consistent with the project's existing acquisition
  precedents); each endpoint specifies its own request weight.
- `funding-rate` and `funding-info` share a 500 req / 5 min / IP
  pool.
- `takerlongshortRatio` and `globalLongShortAccountRatio`
  document a 1000 req / 5 min / IP limit.
- The `openInterestHist`, `topLongShortAccountRatio`,
  `topLongShortPositionRatio`, and `globalLongShortAccountRatio`
  family share a 30-day rolling retention window, which is the
  binding constraint for any future history.

### 9.2 What Phase 4at does not call

No REST endpoint is called by Phase 4at. The map is descriptive
only.

---

## 10. WebSocket market-stream map

Phase 4as already enumerated the principal WS streams. Phase 4at
extends and refines that map. **No WebSocket connection is opened
by Phase 4at.**

| Stream | Name | Update speed | Sequence fields | Notes |
|---|---|---|---|---|
| Aggregate trade | `<symbol>@aggTrade` | per trade event (aggregated 100 ms for same price + same taker side) | `a` (aggId) | Excludes insurance / ADL. |
| Trade | `<symbol>@trade` | per trade | `t` (tradeId) | Lower aggregation. |
| Kline | `<symbol>@kline_<interval>` | per bar | `t`, `T` | Forward bars. |
| Book ticker | `<symbol>@bookTicker` / `!bookTicker` | real-time on best change | `u`, `T`, `E` | M-1 / M-2. |
| Partial book depth | `<symbol>@depth5/10/20@100ms / 250ms / 500ms` | per cadence | `lastUpdateId` per push | M-2 / M-3 (top-N). |
| Diff book depth | `<symbol>@depth` (250 ms default) / `@500ms` / `@100ms` | per cadence | `U`, `u`, `pu` | Snapshot + diff reconstruction. |
| Liquidation | `<symbol>@forceOrder` / `!forceOrder@arr` | ≤ 1 push / sec | order trade time | Largest-per-1000 ms snapshot. |
| Mark price | `<symbol>@markPrice` / `!markPrice@arr` | per cadence | event time | Phase 3r §8 / 3v §8 governance. |
| Index price | `<pair>@indexPrice` | per cadence | event time | Optional context. |

Citations:
[Aggregate Trade Streams](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Aggregate-Trade-Streams);
[Diff Book Depth Streams](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Diff-Book-Depth-Streams);
[Partial Book Depth Streams](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Partial-Book-Depth-Streams);
[All Book Tickers Stream](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/All-Book-Tickers-Stream);
[Liquidation Order Streams](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Liquidation-Order-Streams);
[How To Manage A Local Order Book Correctly](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/How-to-manage-a-local-order-book-correctly).

### 10.1 What Phase 4at does not stream

No WS connection is opened by Phase 4at. The map is descriptive
only.

---

## 11. Local order-book reconstruction feasibility

Local order-book reconstruction from REST snapshot + diff-depth
stream is **technically possible** but requires a deterministic
capture-and-replay design. The official procedure is documented
by Binance:

1. Open WS stream `<symbol>@depth` (or 100 / 500 ms variants).
2. Buffer incoming events.
3. Fetch REST snapshot
   `GET /fapi/v1/depth?symbol=...&limit=1000`.
4. Drop any event where `u` (final update ID) is less than
   `lastUpdateId` from the snapshot.
5. The first processed event must satisfy
   `U <= lastUpdateId AND u >= lastUpdateId`.
6. Subsequent events must have `pu` equal to the previous
   event's `u`. Any mismatch is a sequence gap and forces a
   resync (drop the local book; refetch the snapshot;
   restart).

Source: [How To Manage A Local Order Book Correctly](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/How-to-manage-a-local-order-book-correctly).

### 11.1 Capture-side requirements

Any future capture phase that reconstructs the LOB must:

- run an isolated capture process per symbol;
- write raw immutable WS events to append-only storage with
  minimal post-processing;
- maintain monotone sequence-number bookkeeping (`U`, `u`, `pu`);
- detect gaps explicitly and mark invalid windows verbatim
  (no silent fill);
- re-snapshot on gap detection and resume cleanly;
- preserve event-time vs ingestion-time vs transaction-time
  separately;
- allow deterministic replay from raw events to a normalised
  book state, with the same code path used in research and any
  future runtime.

### 11.2 Storage burden (qualitative; no measurement performed)

Per Phase 4as §10, BTCUSDT alone at full granularity (aggTrades
+ depth diff + bookTicker) generates gigabytes per day under
moderate compression. A production-discipline capture for the
project's locked v1 scope (BTCUSDT primary, ETHUSDT comparison)
plus reasonable headroom for the Phase 4ac core symbol set is
expected to be well within the capacity of the operator's
existing repository host, but storage tiers (raw → parquet →
compacted) and retention policy must be predeclared in any
future capture-design phase.

### 11.3 Phase 4at boundary

**No capture, snapshot, or reconstruction is implemented or
attempted by Phase 4at.** The procedure is described only to
inform any future, separately-authorised Phase 4au capture
design memo and any further-future implementation phase.

---

## 12. Liquidation data feasibility

Phase 4at confirms, with the official Binance docs, the
following bounded visibility for liquidation data:

- The `<symbol>@forceOrder` stream and the all-market
  `!forceOrder@arr` stream push only the **largest one
  liquidation order within 1000 ms** per symbol; if no
  liquidation occurs in that window, no message is pushed.
- The streams therefore never publish the **full** liquidation
  tape. They publish a **snapshot proxy**.
- The REST endpoint `GET /fapi/v1/forceOrders` is **user-scope
  authenticated**: it returns liquidations for the calling
  account only and is **not appropriate** for market-wide
  microstructure research. It is classified
  AUTHENTICATED_USER_SCOPE_NOT_ADMISSIBLE_FOR_MARKET_RESEARCH.

Sources: [Liquidation Order Streams](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Liquidation-Order-Streams).

### 12.1 Implications for any future research

- Any future M-9 (liquidation cascade proxy) study must label
  the data **proxy only** and must not assume completeness.
- The presence or absence of a liquidation message is itself
  bounded: in a 1000 ms window with multiple liquidations,
  smaller liquidations are not pushed. Cascade-counting
  features that assume completeness are mis-specified.
- Cross-validation against aggressive-flow and OI-change is
  the only feasible way to corroborate liquidation-driven
  hypotheses without the full tape.
- M-9 remains admissible only as a **context / regime overlay**;
  it is not authorised by Phase 4at and is not implemented here.

---

## 13. Open interest / funding feasibility

### 13.1 Funding-rate history

- REST `GET /fapi/v1/fundingRate` provides historical funding
  events per symbol. The project already has `funding__v001`
  manifests on disk for the locked v1 scope and the Phase 4ac
  core symbol set. **No further funding acquisition is
  authorised by Phase 4at.**
- Funding-rate context use is admissible **only as a context
  lens** per Phase 4as §13 and Phase 4ag §10 (Lane D conditional
  framing). The D1-A precedent forbids funding as a directional
  trigger. This boundary is binding for any future research.

### 13.2 Open interest

- REST `GET /fapi/v1/openInterest` is a snapshot.
- REST `GET /futures/data/openInterestHist` retains only the
  **last 30 days** per the endpoint description. Forward
  extension requires live polling.
- The project already has Phase 4i metrics datasets that hold
  partial OI series under the **Phase 4j §11 OI-subset
  partial-eligibility rule**. Per-bar exclusion of bars whose
  required OI fields are missing or invalid is binding for any
  future use.
- M-11 / M-12 / M-13 / M-14 must therefore be designed under
  Phase 4j §11 governance if they ever consume OI data.

### 13.3 Phase 4at boundary

- No funding or OI data is acquired by Phase 4at.
- No Phase 4j §11 amendment is proposed.
- Phase 3r §8 mark-price gap governance is preserved.
- The D1-A precedent (funding is not a directional trigger) is
  preserved.

---

## 14. Aggressive-volume / order-flow feasibility

### 14.1 aggTrades availability

- `data.binance.vision` provides historical aggTrades via the
  `data/futures/um/{daily,monthly}/aggTrades/<SYMBOL>/` archive
  ([data.binance.vision — futures/um/daily/aggTrades](https://data.binance.vision/?prefix=data%2Ffutures%2Fum%2Fdaily%2FaggTrades%2F)).
- REST `GET /fapi/v1/aggTrades` returns the same content for
  forward catch-up.
- WS `<symbol>@aggTrade` provides the live forward stream with
  per-100 ms aggregation for same price + same taker side.

### 14.2 Maker-flag interpretation

The aggTrades schema includes a `m` (maker-side) flag. By
convention:

- `m == true` → the **buyer was the maker** (the trade was
  consumed by an aggressive sell-side taker).
- `m == false` → the **seller was the maker** (the trade was
  consumed by an aggressive buy-side taker).

An aggressive-flow imbalance feature can therefore be derived
from aggTrades in any future research phase without needing a
separate "taker-side" feed.

### 14.3 Limitations

- Insurance-fund and ADL trades are excluded from the
  aggregation
  ([Binance Open Platform — Aggregate Trade Streams](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Aggregate-Trade-Streams)).
- Effective 2025-12-31 the new `nq` field in the aggTrade WS
  stream excludes RPI-order trades from the "normal" volume
  (the original `q` continues to include all market trades).
  Any future feature that consumes aggressive-flow imbalance
  must declare which definition it uses.

### 14.4 Suitability for Lane B

Lane B (aggressive-volume / order-flow imbalance feasibility)
is the cleanest follow-on **mechanism feasibility** lane after
Phase 4at, because aggTrades is already historically available
and live capture is well-supported. **It is not authorised
here.** Lane B can only be opened after a separately authorised
docs-only feasibility memo that satisfies M0 admissibility and
the Phase 4al refined no-rescue rule.

---

## 15. Capture design requirements for a future implementation phase

The following capture-design requirements are recorded **as
design only** for any future, separately-authorised implementation
phase (Phase 4au or a successor). **Phase 4at does not implement
any of them.**

1. **Process isolation.** Capture processes run in their own
   process tree, isolated from `prometheus.runtime`,
   `prometheus.execution`, and `prometheus.persistence`. A
   capture failure must not affect the runtime safety state.
2. **Public-only endpoint allowlist.** Only public Binance
   endpoints (REST + WS) are allowed by default: aggTrade,
   trades, klines, markPriceKlines, premiumIndexKlines,
   indexPriceKlines, funding history, openInterest,
   openInterestHist, top/global long-short ratios,
   takerlongshortRatio, depth (REST + WS), bookTicker,
   forceOrder, markPrice, indexPrice. Any addition requires
   separate authorisation.
3. **No credentials.** Capture processes must not read any
   `.env` or credential file by default. Authenticated /
   private endpoints, user stream, listenKey lifecycle, and
   exchange-write are explicitly out of scope.
4. **Raw immutable logs.** Each WS event must be written
   verbatim to append-only storage with minimal post-processing.
   No silent normalisation or compaction is allowed at the
   capture layer.
5. **Normalised derived tables.** Normalised parquet / DuckDB
   tables are computed in a separate pipeline that consumes the
   raw logs deterministically. Replay from raw → normalised
   must be reproducible.
6. **Manifest versioning.** Each dataset family carries a
   manifest with `__v001` initial label, paired SHA256 of every
   archive / file, sequence-number range, capture window in
   UTC ms, schema version, and `research_eligible` flag (default
   `false`; flipped only by an integrity gate analogous to
   Phase 3p §4.7 / Phase 4i §17).
7. **Schema versioning.** Schema changes bump the dataset
   family `__vNNN`. No silent in-place mutation is allowed.
8. **Event-time / transaction-time / ingestion-time
   separation.** Each event records all three timestamps where
   provided. UTC ms is canonical.
9. **Symbol allowlist.** Capture is scoped to a predeclared
   symbol allowlist (BTCUSDT primary, ETHUSDT comparison; alt
   symbols only if separately authorised).
10. **Rate-limit handling.** REST captures must respect
    documented rate limits (500 / 5min / IP for funding;
    1000 / 5min / IP for taker / long-short; per-endpoint
    request weight for the IP-level pool). Backoff on 429 is
    mandatory. WS reconnects use jittered exponential backoff.
11. **Reconnect / resync rules.** Diff-depth captures must
    re-snapshot on sequence-number gap; aggTrade captures must
    detect aggId gaps and mark invalid windows.
12. **Gap detection and invalid-window creation.** Every
    detected gap creates an explicit `invalid_window` entry in
    the manifest with `start_ms`, `end_ms`, `reason`, and
    `evidence`.
13. **Deterministic replay.** Research code consumes captured
    data only via the deterministic replay pipeline; ad-hoc
    reads from raw logs are not allowed in research.
14. **Local storage layout.** Raw / normalised / derived
    directories are separated. Parquet partitioning by symbol
    + month follows the project's existing convention.
15. **Compression format.** Raw logs use a streaming-friendly
    framing (e.g. zstd-compressed JSON-Lines) to support
    deterministic replay and partial recovery.
16. **Logging.** Capture processes emit structured logs;
    secrets and request signatures are never logged (the
    public-only boundary makes this easy by design).
17. **Health checks.** Each capture process exposes a local
    health-check signal (pid, last-event-ts, lag, gap counts,
    reconnect count) consumed by the operator dashboard.
18. **No exchange-write.** Capture processes have no
    exchange-write surface. Any code path that could submit an
    order is forbidden in the capture process tree.
19. **No `prometheus.runtime` / `execution` / `persistence`
    coupling.** Capture is strictly read-only with respect to
    the runtime safety state. The runtime database is not
    modified by capture.
20. **No `data/raw/` / `data/normalized/` / `data/manifests/`
    write surface for already-captured project data.** New
    capture writes only into new family / version directories;
    existing manifests are not modified.

These design requirements are **not** authorised for
implementation by Phase 4at. They are recorded so that any
future Phase 4au or successor can build against a stable
predeclared baseline.

---

## 16. Proposed future dataset families

The following dataset family names are proposed **as future
design names only**. **None is created by Phase 4at.** Each
would be subject to a separately authorised future capture
design and integrity gate.

- `microstructure_raw_aggtrades_v001` — raw `<symbol>@aggTrade`
  WS events; primary M-5 / M-6 input.
- `microstructure_raw_depthdiff_v001` — raw
  `<symbol>@depth(@100/250/500ms)` WS events; required for any
  M-3 / M-4 / M-7 / M-8 reconstruction.
- `microstructure_raw_bookticker_v001` — raw
  `<symbol>@bookTicker` WS events; required for any M-1 / M-2
  research.
- `microstructure_raw_forceorder_proxy_v001` — raw
  `<symbol>@forceOrder` snapshots; **labelled proxy only**;
  required for any M-9 research; must be paired with §12
  documentation.
- `microstructure_raw_markprice_v001` — raw
  `<symbol>@markPrice` events; subject to Phase 3r §8 / Phase
  3v §8 governance; not authorised by Phase 4at.
- `microstructure_metrics_oi_funding_v001` — derived OI / funding
  series for forward extension beyond the 30-day REST retention,
  under Phase 4j §11 OI-subset governance.
- `microstructure_replay_lob_v001` — derived LOB replay state
  from `microstructure_raw_depthdiff_v001` + REST depth
  snapshots, intended for deterministic feature computation.

**No data acquisition, capture, manifest creation, or
implementation occurs in Phase 4at.** These names are placeholder
candidates for a future, separately-authorised implementation
phase.

---

## 17. Data-quality and invalid-window governance

The following data-quality predicates are recorded **for any
future capture phase**. They mirror prior project precedents
(Phase 3p §4.7, Phase 3r §8, Phase 4j §11, Phase 4ad rules).
Phase 4at does not implement any of them.

- **Missing sequence** (`u` jumps; `aggId` jumps).
- **Out-of-order event** (event-time decreases unexpectedly).
- **Duplicate event** (same `aggId` or same `(U, u, pu)`).
- **Gap after reconnect** (WS reconnect crosses a sequence gap).
- **Snapshot mismatch** (REST snapshot `lastUpdateId` does not
  bracket the first replayed diff event per the Binance
  procedure).
- **Clock skew** (event-time vs ingestion-time exceeds a
  predeclared bound).
- **Symbol mismatch** (WS event reports a symbol other than the
  subscribed symbol).
- **Stale book** (no diff event received for longer than a
  predeclared bound at a given cadence).
- **Impossible spread** (best ask <= best bid).
- **Negative size** (level quantity < 0).
- **Zero / invalid price** (price <= 0 or non-finite).
- **Checksum** if available (archive `.CHECKSUM` mismatch).
- **Archive checksum mismatch** (paired SHA256 fails).
- **Retention-window incompleteness** (REST history shorter
  than expected window for the predeclared period).
- **forceOrder proxy incompleteness** (any indication that
  multiple liquidations occurred in the same 1000 ms window;
  must be flagged but cannot be resolved at the public-stream
  layer).

Each of the above must produce an explicit `invalid_window`
entry in the manifest with reason and evidence. **No silent
forward-fill, interpolation, imputation, or replacement is
allowed**, per Phase 3p §4.7 / Phase 3r §8 / Phase 4j §11
precedents.

---

## 18. M0 admissibility implications

Each major data family is evaluated below against the Phase 4ak
twelve-clause M0 gate, the Phase 4al refined no-rescue rule, the
Phase 4t 10-dimension scoring matrix, the Phase 4m 18-requirement
validity gate, and the Phase 4ak post-null cooldown rule.

| Mechanism / data family | Distinct from cooled-down? | Data feasibility | Leakage risk | Cost realism | Edge / opp-rate | Future study admissibility |
|---|---|---|---|---|---|---|
| M-1 spread (bookTicker / depth) | Yes | WS_LIVE_CAPTURE_REQUIRED | Snapshot-vs-event-time mixing | Very high (widening events are worst-cost) | Edge-rate plausibility low; opp-rate moderate | Future feasibility study acceptable as **context**. |
| M-2 top-of-book depth | Yes | WS_LIVE_CAPTURE_REQUIRED | Same as M-1 | Medium-high | Noisy; transient | Future feasibility study acceptable. |
| M-3 OBI top-N | Yes | WS_LIVE_CAPTURE_REQUIRED | Snapshot / diff sync | Medium | Decay rapid OOS | Future feasibility study acceptable; full LOB. |
| M-4 deeper depth imbalance | Yes | WS_LIVE_CAPTURE_REQUIRED | Same as M-3 | Medium | Sparser | Acceptable only **after** M-3. |
| M-5 aggressive volume / taker | Yes | HISTORICAL_ARCHIVE_AVAILABLE (aggTrades) | Window-boundary leakage | Medium | Strong literature; alpha decay risk | Future feasibility study acceptable; **strong candidate** for Lane B. |
| M-6 trade burst / volume impulse | Yes | HISTORICAL_ARCHIVE_AVAILABLE (aggTrades) | Rolling-window z-score look-ahead | Very high in burst | Selection bias risk | Future feasibility study acceptable as **regime / context**. |
| M-7 sweep / book consumption | Yes | WS_LIVE_CAPTURE_REQUIRED | Snapshot mixing | Very high | Free-parameter event def | Acceptable only **after** M-3. |
| M-8 book recovery | Yes | WS_LIVE_CAPTURE_REQUIRED | Same as M-7 | Medium-high | Spoofing-vulnerable | Acceptable only **after** M-7. |
| M-9 liquidation proxy | Yes | WS_LIVE_CAPTURE_REQUIRED + PUBLIC_PROXY_ONLY | Bounded visibility | Very high in cascade | Rare-event risk | Acceptable as **context / regime overlay** only. |
| M-10 funding context | Borderline (D1-A trap) | REST_HISTORY_AVAILABLE | Look-ahead from next-funding | Funding cost in §11.6 | D1-A precedent | Acceptable as **context only**. |
| M-11 OI context | Yes (Phase 4j §11) | REST_RECENT_ONLY → live capture | Look-ahead from same-bar OI change | Low (context) | Sparse | Acceptable under Phase 4j §11 only. |
| M-12 funding + OI | Yes (composite) | Composite of M-10 / M-11 | Same as components | Low | Sample-size at funding cadence | Acceptable as **context** only. |
| M-13 funding + OI + flow | Yes (composite) | Composite | Window-boundary | Variable | Multiple-comparison risk | Acceptable as **regime context**. |
| M-14 spread / depth / flow regime | Borderline (G1 trap) | All of the above | Re-enabling cooled-down | Variable | Most overfitting-prone | Acceptable only as **regime layer** to a primary mechanism, not as primary. |

The general M0 admissibility result: future microstructure
feasibility memos may proceed lane-by-lane (A → B → C → D → E)
under M0, the post-null cooldown rule, and the no-rescue
boundary. **None is authorised by Phase 4at.**

---

## 19. Research validity and anti-overfitting requirements

Any future microstructure research must preserve the binding
project discipline already codified by Phase 4k / Phase 4q /
Phase 4w / Phase 4ak / Phase 4al / Phase 4as §11. Phase 4at
does not authorise any research; the requirements are recorded
for the future docs-only feasibility memos that may follow.

- **Predeclared hypotheses.** Hypotheses are admissible only
  if they satisfy the Phase 4ak twelve-clause M0 gate and the
  Phase 4m 18-requirement validity gate.
- **Walk-forward / temporal validation.** Time-series labels
  are not shuffled; holdouts are chronological with explicit
  UTC date boundaries.
- **No random shuffling.** Standard k-fold CV is inappropriate
  for time-series microstructure forecasting; CSCV / DSR / PBO
  per Bailey & López de Prado is the precedent.
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
  non-mechanism baselines are mandatory (Phase 4w / Phase 4u
  precedent).
- **Baseline comparisons.** A microstructure feature is
  admissible only if it can outperform a non-feature baseline
  on M0 admissibility and predicted-Δ_R discipline.
- **Endpoint-retention awareness.** Any plan that depends on
  `openInterestHist` or long-short ratio retention beyond
  30 days requires forward live capture (not authorised here).
- **Feature leakage checks.** A feature window that touches
  the prediction target boundary leaks; sequence-number
  validation, event-time vs bar-time separation, and
  predeclared lag conventions are mandatory.

---

## 20. Recommended next phase

The cleanest separately-authorised next move, **if the operator
chooses to continue research after reviewing Phase 4at**, is:

**Phase 4au — Binance Microstructure Capture Design Specification
Memo**

- **Type:** docs-only design specification.
- **Purpose:** translate §15 of this memo into a precise capture
  design covering process isolation, endpoint allowlist,
  storage layout, manifest schema, sequence-number bookkeeping,
  invalid-window governance, deterministic replay, health
  checks, and rate-limit / backoff rules. The memo specifies
  the design exhaustively; it does **not** implement capture,
  open any WebSocket, or download any archive.
- **Boundary:** docs-only; no endpoint calls; no data
  acquisition; no capture implementation; no ML; no strategy
  candidate; no successor authorisation.
- **Authorisation status:** **NOT authorised by Phase 4at.**

Phase 4au would answer: "Exactly what capture design (process
isolation, endpoint allowlist, storage layout, manifest schema,
sequence-number bookkeeping, invalid-window governance,
deterministic replay, health checks, rate-limit / backoff rules)
must be specified before any future capture phase could be
safely authorised, and what predeclared admissibility checklist
must such a capture phase satisfy?"

### Acceptable alternative recommendation

If the operator concludes that the Phase 4at availability map
already shows insufficient feasibility for any forward
microstructure work — e.g. because storage / capture overhead
is unacceptable, or because the bounded-visibility families
(forceOrder; OI-history; long-short ratios) are too thin for
robust research — then **remain paused** is an acceptable
alternative.

---

## 21. Explicit non-recommendations

The following are **not** recommended by Phase 4at. Several are
explicitly forbidden by prior governance:

- No immediate data acquisition.
- No Binance endpoint calls.
- No capture implementation.
- No order-book reconstruction implementation.
- No ML model.
- No new strategy candidate.
- No exit / entry design.
- No paper / live work.
- No old-strategy alt-symbol rerun.
- No 5m research thread reopening.
- No verdict / lock revision.
- No M0 amendment.
- No reduction of microstructure to a "rank-then-V2 / G1 /
  C1-style breakout".
- No D1-A reuse as a directional trigger; funding remains a
  context lens only.
- No authorisation of paper / shadow / live-readiness /
  deployment / exchange-write / production-key creation /
  authenticated APIs / private endpoints / public-endpoint
  calls in code / user stream / WebSocket / MCP / Graphify /
  `.mcp.json` / credentials.

---

## 22. Implementation / governance review

### What changed?

- New file: this memo at
  `docs/00-meta/implementation-reports/2026-05-07_phase-4at_binance-microstructure-data-availability-capture-feasibility.md`.
- Narrow update to `docs/00-meta/current-project-state.md` —
  Phase 4at narrative paragraph and "Current phase:" block
  update, with the prior Phase 4as block preserved as historical
  context (matching prior-phase convention).

### What did not change?

- No `src/prometheus/` modification.
- No test under `tests/` modified.
- No existing script under `scripts/` modified.
- No data file under `data/raw/`, `data/normalized/`,
  `data/derived/` modified.
- No manifest under `data/manifests/` modified or created.
- No `research_eligible` flag flipped.
- No v003 created.
- No `.gitignore` modified.
- No specialist governance file modified beyond the narrow
  current-project-state update (no Phase 3r §8 / Phase 3v §8 /
  Phase 3w / Phase 4j §11 / Phase 4k / Phase 4p / Phase 4q /
  Phase 4v / Phase 4w / Phase 4ak / Phase 4al / Phase 4am /
  Phase 4an / Phase 4ao / Phase 4ap / Phase 4aq / Phase 4ar /
  Phase 4as modification).
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

### Were any locks, verdicts, or safety boundaries affected?

No. The retained verdict ledger and project locks are preserved
verbatim. M0 governance is unchanged. The 5m closure (Phase 3t)
is preserved. The cost lock (§11.6) and project locks (§1.7.3)
are preserved. The stop-trigger-domain governance (Phase 3v §8),
break-even / EMA slope / stagnation governance (Phase 3w §6 /
§7 / §8), mark-price gap governance (Phase 3r §8), and OI subset
governance (Phase 4j §11) are all preserved. The Phase 4ak M0
gate, post-null cooldown rule, cooled-down families list, and
memo template are all preserved. The Phase 4al refined no-rescue
rule, the Phase 4am audit findings, the Phase 4an inventory, the
Phase 4ao harmonization, the Phase 4ap forensic plan, the Phase
4aq computation, the Phase 4ar interpretation, and the Phase
4as mechanism map are all preserved.

### Were any historical scripts, source files, existing data, manifests, or tests modified?

No. Phase 4at is a docs-only feasibility memo.

### Is the phase mergeable as docs-only?

Yes. Phase 4at adds two markdown files under
`docs/00-meta/implementation-reports/` plus a narrow update to
`docs/00-meta/current-project-state.md`. Per the operator's
instruction in this prompt, **Phase 4at is not merged in this
prompt**.

---

## 23. Research interpretation review (plain English)

### What did this phase prove?

Phase 4at did not prove anything in the predictive-statistics
sense. As a docs-only feasibility memo it documents, with
citations to official Binance documentation, what Binance public
market data is available historically (via REST and the
`data.binance.vision` archive) versus only via future live
capture (WS-only families: book ticker, partial / diff depth,
forceOrder, mark-price stream), what retention bounds apply to
the derivatives-flow REST endpoints (`openInterestHist`,
top-trader and global long-short ratios, takerlongshortRatio
all retain only the latest 30 days), and what capture-design
discipline would be required before any future implementation
could be safely authorised.

### What did this phase not prove?

Phase 4at did not prove that any specific microstructure
mechanism contains edge. It did not run any computation. It did
not acquire any data. It did not call any Binance endpoint or
download any archive file. It did not authorise any successor
phase. It did not implement any capture or feature. It did not
produce a new strategy candidate. It did not amend M0. It did
not modify any verdict or lock.

### Which original questions did it answer?

The Phase 4at question — "Exactly what Binance public market
data is available historically versus only via future live
capture for crypto microstructure / derivatives-flow research,
what are the limitations, and what capture design would be
required before any implementation could be safely authorized?"
— is answered across §6 (data family availability matrix), §7
(historical vs live-capture classification), §8 (Binance public
archive map), §9 (REST market-data map), §10 (WebSocket
market-stream map), §11 (local order-book reconstruction
feasibility), §12 (liquidation data feasibility), §13 (OI /
funding feasibility), §14 (aggressive-volume / order-flow
feasibility), §15 (capture design requirements), §16 (proposed
future dataset family names), §17 (data-quality / invalid-window
governance), §18 (M0 admissibility implications), §19 (research
validity / anti-overfitting requirements), and §20 (recommended
next phase Phase 4au).

### Which original questions remain open?

- Whether any of the M-1 → M-14 mechanisms contains edge under
  the project's locked cost realism. **This is not answered by
  Phase 4at and should not be answered by Phase 4at.**
- Whether Phase 4au is the cleanest next move. The memo
  recommends Phase 4au but does **not** authorise it.
- Whether storage and operational overhead for live capture of
  diff-depth / book-ticker / forceOrder is acceptable for the
  project's host. The Phase 4au memo, if ever authorised, would
  surface this question; Phase 4at does not commit to any
  numeric answer.

### What does it mean for strategy research?

Phase 4at confirms that Lane A — Binance microstructure data
availability / capture feasibility — has been mapped exhaustively
at the public-availability layer. The map is consistent with
proceeding to a docs-only Phase 4au capture design memo if the
operator separately authorises it. The cooled-down families
list, the six-candidate rejection topology, the cost lock, the
position lock, the leverage lock, and the mark-price stop lock
are all preserved. M0 remains the binding admissibility
framework.

### What does it mean for governance?

Phase 4at reaffirms the binding prospective governance: M0
admissibility, post-null cooldown, §11.6, §1.7.3, Phase 3r §8,
Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k,
Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak adoption,
Phase 4al refined no-rescue + §13 / §14, Phase 4am §11.A audit
findings, Phase 4an inventory, Phase 4ao harmonization,
Phase 4ap forensic plan, Phase 4aq computation result preserved
as descriptive evidence only, Phase 4ar interpretation result
preserved as descriptive interpretation only, and Phase 4as
mechanism-map result preserved as docs-only reset evidence only.
**None is amended.**

### What is the clean next step?

Operator review of Phase 4at. **No successor phase is authorised
by Phase 4at.** Acceptable separately-authorised future options
include remain paused (recommended), Phase 4au as a docs-only
Binance microstructure capture-design specification memo, or
further docs-only governance memos on precise governance
questions. None is started or authorised by Phase 4at.

### What should we not do yet?

- No data acquisition.
- No Binance endpoint calls.
- No public-archive downloads.
- No WebSocket connections.
- No capture implementation.
- No order-book reconstruction implementation.
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
  exchange-write / production-key creation / authenticated APIs
  / private endpoints / user stream / WebSocket / MCP /
  Graphify / `.mcp.json` / credentials.

---

## 24. Preserved verdicts, locks, and no-rescue constraints

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
- **Phase 3w §6 / §7 / §8** break-even / EMA slope / stagnation
  governance.
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
  Phase 4ar / Phase 4as amendment.

---

## 25. Final status

Phase 4at is complete on branch
`phase-4at/binance-microstructure-data-availability-capture-feasibility`.

- **Memo:** this file.
- **Closeout:** to be added at
  `docs/00-meta/implementation-reports/2026-05-07_phase-4at_closeout.md`
  in the next commit on this branch.
- **Successor authorisation:** none. **Phase 4au / Phase 5 /
  Phase 4 canonical / paper / shadow / live-readiness /
  deployment / exchange-write / production-key / authenticated
  APIs / private endpoints / user stream / WebSocket / MCP /
  Graphify / `.mcp.json` / credentials all remain unauthorised.**
  Acquisition of 5m / 1m / aggTrades / tick / mark-price 30m /
  4h / order-book data also remains unauthorised.
- **Recommended state:** **paused** unless the operator
  separately authorises a future phase. The merge of Phase 4at
  into `main` is itself a separate operator decision and is
  **not** performed by this prompt.

## End of Phase 4at memo
