# Phase 4at Merge Closeout — Binance Microstructure Data Availability and Capture Feasibility Memo

## Merge identity

- **Phase:** 4at.
- **Phase title:** Binance Microstructure Data Availability and
  Capture Feasibility Memo.
- **Phase type:** docs-only Binance microstructure / derivatives-
  flow data availability and capture-feasibility memo.
- **Target branch:** `main`.
- **Source branch:**
  `phase-4at/binance-microstructure-data-availability-capture-feasibility`.
- **Merge method:** `--no-ff` (preserves the Phase 4at branch
  history as a discrete merge node on `main`).
- **Main before merge SHA:** `2bc7a04f5685e6c0ab5b5a45f9d1719943b29be8`.
- **Phase 4at memo commit SHA:** `b0ea38df2d533180c715482ee4be50bf4ed0770e`
  (`docs(phase-4at): map binance microstructure data feasibility`).
- **Phase 4at closeout commit SHA:** `5ddba9a747351facfbc0810e9cfe7a8b0cc84b8a`
  (`docs(phase-4at): add closeout`).
- **Phase 4at correction commit SHA:** `06351df2f9f849fdcf922f65da58e5eae08d922c`
  (`docs(phase-4at): clarify microstructure data availability wording`).
- **Merge commit SHA:** recorded in this merge closeout's final
  operator report (and in the live `git log` on `main`) once the
  merge commit lands. Self-referential SHA-in-content is avoided
  per prior-phase convention.

## Merge purpose

This merge brings the Phase 4at docs-only Binance microstructure
data availability and capture-feasibility memo onto `main`,
together with the Phase 4at closeout and a narrow Phase 4at
update to `docs/00-meta/current-project-state.md`. Phase 4at
translates Phase 4as §9 into a precise availability map for
Binance USDⓈ-M Futures public market data relevant to the
Phase 4as M-1..M-14 mechanism set, with citations to official
Binance Open Platform documentation and the public-data
repository at `github.com/binance/binance-public-data`.

The merge is **docs-only**. It brings forward the Phase 4at
memo, the Phase 4at closeout, and the narrow current-project-
state update. It does **not** authorise any successor phase,
data acquisition, endpoint call, public-archive download,
WebSocket connection, capture code, feature implementation, ML
model, strategy candidate, paper / shadow, live-readiness,
deployment, exchange-write, production-key creation,
authenticated APIs, private endpoints, user stream, MCP,
Graphify, `.mcp.json`, credentials, or any 5m / 1m / aggTrades /
tick / mark-price 30m / 4h / order-book data acquisition.

## Pre-merge wording corrections summary

Two narrow wording corrections were applied to the Phase 4at
memo on the Phase 4at branch in commit
`06351df2f9f849fdcf922f65da58e5eae08d922c`
(`docs(phase-4at): clarify microstructure data availability wording`)
**before** this merge:

- **Correction 1 — §6.2 raw trades / aggTrades granularity
  wording:** the previous wording implied raw trades are a
  "lower-resolution view than aggTrades". This was reworded to
  state correctly that raw trades are a more granular trade-
  level source while aggTrades are a compressed / taker-side
  aggregation, and that aggTrades may still be preferred for
  Lane B research (smaller, historically archived, taker-side
  aligned) but raw trades are not lower-resolution.
- **Correction 2 — §6.9 / §7 current open-interest time-series
  wording:** the previous wording implied that a future current-
  OI time-series would require WS live capture. This was
  reworded to state correctly that current OI is a REST
  snapshot endpoint and that any future time-series would
  require **forward REST polling**, not WebSocket capture. The
  §7 classification matrix row for Current OI was updated to
  `REST_RECENT_ONLY (snapshot; future time-series would require
  forward REST polling)` without introducing a formal ninth
  classification.

The Phase 4at closeout was also updated in the same correction
commit to record the pre-merge correction note. No substantive
availability conclusion changed. No data was acquired. No
Binance endpoint was called. No code, script, source, test,
data, manifest, governance, verdict, lock, or `.gitignore` was
modified. No successor authorisation changed.

## Files brought forward

- `docs/00-meta/implementation-reports/2026-05-07_phase-4at_binance-microstructure-data-availability-capture-feasibility.md`
  — Phase 4at main memo (25 sections; +1,686 lines initially;
  with the §6.2 / §6.9 / §7 wording corrections applied in the
  Phase 4at correction commit).
- `docs/00-meta/implementation-reports/2026-05-07_phase-4at_closeout.md`
  — Phase 4at closeout (+596 lines initially; with the pre-
  merge correction note added in the Phase 4at correction
  commit).
- `docs/00-meta/current-project-state.md`
  — narrow update: Phase 4at narrative paragraph + Phase 4at
  "Current phase:" block + transition lines preserving the
  prior Phase 4as block as historical context (matching prior-
  phase convention; unchanged by the correction commit because
  the current-project-state Phase 4at paragraph did not repeat
  the corrected wording).

This merge closeout adds:

- `docs/00-meta/implementation-reports/2026-05-07_phase-4at_merge-closeout.md`
  — this file.

No other file is changed by this merge.

## Confirmation Phase 4at was docs-only

Phase 4at is a docs-only feasibility memo. The merge brings
forward only:

- the Phase 4at memo,
- the Phase 4at closeout,
- the narrow `current-project-state.md` update,
- this merge closeout.

No script was added or executed. No backtest was run. No data
was acquired. No Binance endpoint was called. No WebSocket was
opened. No archive file was downloaded. No code under
`src/prometheus/` was modified. No test was modified. No
existing script was modified. No `.gitignore` change was made.
No `data/research/` content was committed.

`ruff check`, `pytest`, and `mypy` were **not** run because the
phase is docs-only (no `src/prometheus/`, test, script, or
`scripts/` change of any kind). This matches the docs-only
convention used by prior docs-only phases.

## Phase 4at availability / capture-feasibility result

Phase 4at translates Phase 4as §9 into a precise availability
and capture-feasibility map for Binance USDⓈ-M Futures public
market data relevant to the Phase 4as M-1..M-14 mechanism set.
Phase 4at does **not** acquire data, call any endpoint, open
any WebSocket, download any archive, implement capture, or
authorise any successor phase.

### Historical archive available families

(REST + bulk archive at `data.binance.vision`; project precedent
for klines / mark-price klines / funding history already on
disk at the locked v1 scope):

- **aggTrades** (`<symbol>@aggTrade` WS; REST
  `GET /fapi/v1/aggTrades`; bulk archive
  `data/futures/um/{daily,monthly}/aggTrades/`).
- **Raw trades** (`GET /fapi/v1/trades` /
  `GET /fapi/v1/historicalTrades`; bulk archive
  `data/futures/um/{daily,monthly}/trades/`). Raw trades are
  a more granular trade-level source than aggTrades; aggTrades
  may still be preferred for Lane B research because they are
  smaller, historically archived, and taker-side aligned, but
  raw trades are not lower-resolution.
- **Klines** (`GET /fapi/v1/klines`; bulk archive).
- **Mark-price klines** (`GET /fapi/v1/markPriceKlines`; bulk
  archive; subject to Phase 3r §8 governance).
- **Premium-index klines** (`GET /fapi/v1/premiumIndexKlines`;
  bulk archive).
- **Index-price klines** (`GET /fapi/v1/indexPriceKlines`;
  bulk archive).

### REST history available

- **Funding-rate history** (`GET /fapi/v1/fundingRate`; project
  precedent on disk for the locked v1 scope and the Phase 4ac
  core symbol set).

### REST recent only (~30 days rolling) — forward REST polling required for extended history

- **`GET /futures/data/openInterestHist`**
  (`period` ∈ {5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d}).
- **`GET /futures/data/topLongShortAccountRatio`**.
- **`GET /futures/data/topLongShortPositionRatio`**.
- **`GET /futures/data/globalLongShortAccountRatio`**.
- **`GET /futures/data/takerlongshortRatio`**.

(Forward extension is via REST polling at the documented
`period` cadence, not WebSocket capture.)

Current open interest (`GET /fapi/v1/openInterest`) is also a
REST snapshot endpoint; forward time-series construction
requires forward REST polling, not WebSocket capture (per the
Phase 4at pre-merge correction).

### WS live-capture-required families (no public archive at full granularity for derivatives)

- **Book ticker** (`<symbol>@bookTicker`; `!bookTicker`).
- **Partial book depth** (`<symbol>@depth5/10/20@100/250/500ms`).
- **Diff book depth** (`<symbol>@depth(@100/250/500ms)`).
- **REST depth snapshot** (`GET /fapi/v1/depth?limit=1000`)
  is the snapshot starting point for local order-book
  reconstruction combined with the diff-depth WS stream
  (`U` / `u` / `pu` sequence-number bookkeeping; resync on gap).
- **Mark-price stream** (`<symbol>@markPrice`; `!markPrice@arr`;
  Phase 3r §8 / Phase 3v §8 governance).
- **Index-price stream** (`<pair>@indexPrice`).

### Public-proxy-only liquidation limitation

`<symbol>@forceOrder` and `!forceOrder@arr` push only the
**largest one liquidation order within 1000 ms** per symbol; if
no liquidation occurs in that window, no message is pushed.
Liquidation visibility is therefore bounded by design and any
M-9 study must label the data **proxy only**.

### Authenticated user-scope endpoints not admissible for market-wide research

- REST `/fapi/v1/forceOrders` (user-scope authenticated; not
  appropriate for market-wide microstructure research).
- User stream / listenKey lifecycle / all private endpoints.

These are explicitly classified
`AUTHENTICATED_USER_SCOPE_NOT_ADMISSIBLE_FOR_MARKET_RESEARCH`
and are out of scope for any future microstructure / derivatives-
flow research.

### Capture-design requirements recorded but not implemented

Twenty design requirements recorded in §15 of the Phase 4at
main memo (process isolation; public-only endpoint allowlist;
no credentials; raw immutable logs; normalised derived tables;
manifest versioning with `__v001` initial label and paired
SHA256 verification; schema versioning with explicit `__vNNN`
bump; event-time / transaction-time / ingestion-time
separation; symbol allowlist; rate-limit handling; reconnect /
resync rules; gap detection and explicit `invalid_window`
creation; deterministic replay; local storage layout;
streaming-friendly compression; structured logs (no secrets);
local health-check signal consumed by the operator dashboard;
no exchange-write surface; no `prometheus.runtime/execution/persistence`
coupling; no write to existing `data/raw/` / `data/normalized/`
/ `data/manifests/`). **None implemented by Phase 4at.**

### Proposed future dataset family names recorded but not created

Seven placeholder names: `microstructure_raw_aggtrades_v001`,
`microstructure_raw_depthdiff_v001`,
`microstructure_raw_bookticker_v001`,
`microstructure_raw_forceorder_proxy_v001`,
`microstructure_raw_markprice_v001`,
`microstructure_metrics_oi_funding_v001`,
`microstructure_replay_lob_v001`. **None is created.**

## Recommendation

- **Primary recommendation:** remain paused.
- **Conditional secondary (NOT authorized by this merge):**
  Phase 4au — Binance Microstructure Capture Design
  Specification Memo (docs-only). Translates Phase 4at §15
  capture-design requirements into a precise design specification
  for a public-only capture **without** implementing it. No
  acquisition. No successor authorisation. **Phase 4au is NOT
  authorized by this merge.**
- **Alternative acceptable recommendation:** remain paused
  permanently if the operator concludes that capture overhead
  or bounded-visibility families render any forward
  microstructure work infeasible.
- **NOT recommended:** immediate data acquisition; immediate
  endpoint calls; immediate capture implementation; immediate
  order-book reconstruction implementation; immediate ML model;
  immediate strategy or feature implementation; old-strategy
  alt-symbol rerun; R3 / R2 / V1-arc rescue; 5m thread
  reopening; paper / live work.
- **FORBIDDEN:** verdict revision; lock revision; parameter
  optimization; strategy resurrection; M0 amendment; reopening
  the 5m research thread; data acquisition without separately
  authorised data-requirements memo; paper / shadow / live-
  readiness / deployment / exchange-write / production-key
  creation / authenticated APIs / private endpoints / public-
  endpoint calls in code / user stream / WebSocket / MCP /
  Graphify / `.mcp.json` / credentials.

## Implementation / governance review

### What changed

- New file: `docs/00-meta/implementation-reports/2026-05-07_phase-4at_binance-microstructure-data-availability-capture-feasibility.md`
  (Phase 4at main memo, with the pre-merge §6.2 / §6.9 / §7
  wording corrections applied).
- New file: `docs/00-meta/implementation-reports/2026-05-07_phase-4at_closeout.md`
  (Phase 4at closeout, with the pre-merge correction note
  added).
- Narrow update: `docs/00-meta/current-project-state.md`
  (Phase 4at narrative paragraph + Phase 4at "Current phase:"
  block; prior Phase 4as block preserved as historical context).
- New file (this merge): `docs/00-meta/implementation-reports/2026-05-07_phase-4at_merge-closeout.md`.

### What did not change

- No `src/prometheus/` modification.
- No test modification.
- No existing-script modification.
- No data / manifest / `research_eligible` / v003 change.
- No `.gitignore` modification.
- No retained verdict revised.
- No project lock changed.
- No M0 amendment.
- No 5m / 1m / aggTrades / tick / mark-price 30m / 4h /
  order-book acquisition.
- No reopening of the 5m research thread.
- No backtest run.
- No historical strategy script executed.
- No endpoint code modification.
- No endpoint call.
- No WebSocket opened.
- No public-archive download.
- No capture implementation.
- No feature implementation.

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
Phase 4ar interpretation, and the Phase 4as mechanism map are
all preserved.

### Is the merge docs-only?

Yes. The merge brings forward two new memos under
`docs/00-meta/implementation-reports/` plus a narrow update to
`docs/00-meta/current-project-state.md`, plus this merge
closeout. No code, test, script, data, manifest, governance,
or lock change occurs.

## Research interpretation review (plain English)

### What did this phase prove?

Phase 4at did not prove anything in the predictive-statistics
sense. As a docs-only feasibility memo it documents, with
citations to official Binance Open Platform documentation, what
Binance public market data is available historically (REST +
`data.binance.vision` archive) versus only via future live
capture (WS-only families) versus only via forward REST polling
(snapshot REST endpoints; the 30-day-rolling derivatives-flow
endpoints). It records retention bounds, bounded liquidation
visibility, the official local-order-book reconstruction
procedure, twenty capture-design requirements, fourteen data-
quality predicates, M0 admissibility implications per
mechanism, and an eight-classification matrix.

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
(eight-classification matrix), §8 (Binance public archive map),
§9 (REST market-data map), §10 (WebSocket market-stream map),
§11 (local order-book reconstruction feasibility), §12
(liquidation feasibility), §13 (OI / funding feasibility),
§14 (aggressive-volume / order-flow feasibility), §15 (capture
design requirements), §16 (proposed future dataset family
names), §17 (data-quality / invalid-window governance), §18
(M0 admissibility implications), §19 (research validity / anti-
overfitting requirements), and §20 (recommended next phase
Phase 4au).

### Which original questions remain open?

- Whether any of the M-1 → M-14 mechanisms contains edge under
  the project's locked cost realism. **This is not answered by
  this merge.**
- Whether Phase 4au is the cleanest next move. The memo
  recommends Phase 4au but does **not** authorise it.
- Whether storage and operational overhead for live capture is
  acceptable for the project's host. The Phase 4au memo, if
  ever authorised, would surface this question; this merge does
  not commit to any numeric answer.

### What does it mean for strategy research?

This merge confirms that Lane A — Binance microstructure data
availability / capture feasibility — has been mapped
exhaustively at the public-availability layer. The map is
consistent with proceeding to a docs-only Phase 4au capture
design memo if the operator separately authorises it. The
cooled-down families list, the six-candidate rejection
topology, the cost lock, the position lock, the leverage lock,
and the mark-price stop lock are all preserved. M0 remains the
binding admissibility framework.

### What does it mean for governance?

This merge reaffirms the binding prospective governance: M0
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

Operator review of Phase 4at on `main` after this merge lands.
**No successor phase is authorised by this merge.** The clean
next step is operator-driven only. Acceptable separately-
authorised future options include remain paused (recommended),
Phase 4au as a docs-only Binance microstructure capture-design
specification memo, or further docs-only governance memos on
precise governance questions. None is started or authorised by
this merge.

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
- No 5m / 1m / aggTrades / tick / mark-price 30m / 4h /
  order-book acquisition.
- No paper / shadow / live-readiness / deployment /
  exchange-write / production-key creation / authenticated APIs
  / private endpoints / user stream / WebSocket / MCP /
  Graphify / `.mcp.json` / credentials.

## Retained verdict ledger (preserved verbatim)

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

## Preserved project locks

- **M0 governance** — binding prospectively only.
- **§11.6** — 8 bps slippage per side; round-trip = 16 bps.
- **§1.7.3** — 0.25 % risk per trade; 2× leverage cap; one
  position max; mark-price stops where applicable.
- **Phase 3r §8** — mark-price gap governance.
- **Phase 3v §8** — stop-trigger-domain governance.
- **Phase 3w §6 / §7 / §8** — break-even / EMA slope /
  stagnation governance.
- **Phase 4j §11** — metrics OI-subset partial-eligibility rule.
- **Phase 4k** — V2 backtest-plan methodology.
- **Phase 4p** — G1 strategy-spec memo.
- **Phase 4q** — G1 backtest-plan methodology.
- **Phase 4v** — C1 strategy-spec memo.
- **Phase 4w** — C1 backtest-plan methodology.
- **Phase 4ak** — M0 mechanism-admissibility gate adoption
  (twelve clauses + post-null cooldown + cooled-down families
  list + memo template).
- **Phase 4al** — refined no-rescue rule + §13 future-phase
  boundary + §14 data-resolution hierarchy.
- **Phase 4am** — §11.A audit findings.
- **Phase 4an** — historical-trade-population exit-path inventory.
- **Phase 4ao** — exit-path methodology / artefact harmonization.
- **Phase 4ap** — V1-Arc Exit-Path Forensic Plan.
- **Phase 4aq** — computation result preserved as descriptive
  evidence only.
- **Phase 4ar** — interpretation result preserved as descriptive
  interpretation only.
- **Phase 4as** — mechanism-map result preserved as docs-only
  reset evidence only.
- **Phase 4at** — availability / capture-feasibility result
  preserved as docs-only feasibility evidence only.

## No-rescue constraints (preserved)

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

## Successor authorisation status

**No successor phase is authorised by this merge.** The
following remain unauthorised:

- Phase 4au;
- Phase 5;
- Phase 4 canonical;
- data acquisition;
- Binance endpoint calls;
- public-archive downloads;
- WebSocket connections;
- endpoint implementation;
- data-capture implementation;
- order-book reconstruction implementation;
- feature implementation;
- ML model;
- strategy candidate;
- entry / exit design;
- old-strategy alt-symbol reruns;
- R3 / R2 / V1-arc rescue;
- 5m research thread reopening;
- 5m / 1m / aggTrades / tick / mark-price 30m / 4h / order-book
  data acquisition;
- paper / shadow;
- live-readiness;
- deployment;
- exchange-write;
- production keys;
- authenticated APIs;
- private endpoints;
- user stream;
- WebSocket;
- MCP;
- Graphify;
- `.mcp.json`;
- credentials.

## Final status

Phase 4at is being merged into `main` via `--no-ff` to preserve
the Phase 4at branch history as a discrete merge node. Phase 4at
is docs-only. **Recommended state remains paused unless the
operator separately authorizes a future phase.** No next phase
is authorized.

## End of Phase 4at merge closeout
