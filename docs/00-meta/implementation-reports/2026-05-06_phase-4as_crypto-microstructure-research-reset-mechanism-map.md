# Phase 4as — Crypto Microstructure Research Reset and Mechanism Map

## Phase identity

- Phase ID: **4as**.
- Phase title: **Crypto Microstructure Research Reset and Mechanism Map**.
- Type: docs-only research-program reset / mechanism-map memo.
- Authority: separately operator-authorized as a research reset
  phase only.
- Branch: `phase-4as/crypto-microstructure-research-reset-mechanism-map`.
- Base SHA (main at branch creation):
  `12f2b5558b0812a11526da331fa70feb45fcae9d`.
- Phase 4as memo commit SHA: recorded in this phase's closeout once
  this memo is committed.

---

## 1. Executive summary

The V1 / exit-rescue research arc closed at Phase 4ar as
descriptive evidence only. Phase 4aq's V1-arc forensic computation
showed that favorable excursion existed across H0, R3, R1a,
R1b-narrow, and R2 in the primary R-window default cell, but did
not, on average, translate into positive realized `net_R` on either
BTCUSDT or ETHUSDT. Phase 4ar then explicitly rejected exit design,
R3 optimization, R2 rescue, R1a / R1b-narrow promotion, H0
revision, lower-timeframe escalation, verdict revision, and lock
revision as conclusions from Phase 4aq.

Six independent strategy candidates have now been rejected
(R2 cost-fragility; F1 hard reject; D1-A mechanism-pass /
framework-fail; V2 hard reject; G1 hard reject; C1 hard reject) and
the V1-arc descriptive forensic snapshot has been completed without
producing a recoverable edge.

This memo therefore **resets the Prometheus research program**
toward Binance-native crypto microstructure and derivatives-flow
mechanisms (spread, depth, order-book imbalance, aggressive volume
and taker imbalance, trade bursts, liquidity sweeps, book
recovery, liquidation cascade proxies, funding-rate context,
open-interest context, and combined / regime variants of the
above). It does so without:

- acquiring data;
- calling Binance endpoints;
- writing or modifying endpoint code;
- implementing any data capture;
- implementing any feature;
- running any backtest, historical strategy script, or
  Phase 4aq script;
- creating a strategy candidate or a successor strategy
  (no R3-prime / R2-prime / R1a-prime / R1b-narrow-prime /
  H0-prime / V2-prime / G1-prime / C1-prime / D1-A-prime /
  V1-D1 / F1-D1 / any cross-strategy hybrid);
- modifying any data, manifest, existing trade log,
  `src/prometheus/` source, test, script, governance doc,
  retained verdict, project lock, strategy spec, threshold,
  or `.gitignore`;
- committing any local `data/research/` output;
- authorizing any successor phase, paper / shadow / live-
  readiness / deployment / exchange-write work, production-key
  creation, authenticated APIs / private endpoints / public-
  endpoint calls in code / user stream / WebSocket / MCP /
  Graphify / `.mcp.json` / credentials, or 5m / 1m / aggTrades /
  tick-data / mark-price 30m / 4h / order-book capture.

The memo's recommendation is to **remain paused** unless the
operator separately authorizes a future phase. The cleanest
acceptable continuation, if separately authorized later, is a
docs-only **Phase 4at — Binance Microstructure Data Availability /
Capture Feasibility Memo**. Phase 4at is **not** authorized by
Phase 4as.

All retained verdicts and project locks are preserved verbatim.
M0 governance, the post-null cooldown rule, the cooled-down
families list, the Phase 4al refined no-rescue rule, the Phase 4t
10-dimension candidate scoring matrix, the Phase 4m 18-requirement
fresh-hypothesis validity gate, the Phase 3t 5m closure, §11.6,
and §1.7.3 are all binding and unchanged.

---

## 2. Scope and explicit non-scope

### In scope

- A docs-only **research reset** narrative that explains why the
  Prometheus research program should now move away from
  rule-based, lagging OHLCV-indicator families toward
  Binance-native microstructure and derivatives-flow
  mechanisms.
- A **mechanism map** that enumerates candidate microstructure /
  derivatives-flow mechanisms, with per-mechanism plain-English
  hypotheses, plausibility, failure modes, required data,
  granularity, feasibility commentary, leakage / cost / validation
  concerns, and M0 admissibility commentary.
- A **Binance data availability map** that summarises, with
  citations to official Binance docs and reputable sources, what
  is plausibly available historically vs only by future live
  capture (no implementation, no calls).
- **Research validity** and **anti-overfitting** requirements
  appropriate for any future microstructure feasibility / research
  phase.
- A discussion of **ML / AI automation placement** that does not
  authorize any model.
- **Symbol-specific** and **regime / window** discussion that
  preserves no-rescue boundaries.
- A conservative **candidate lane ranking** and a **recommended
  next phase**.
- Explicit **non-recommendations**, the **implementation /
  governance review**, the **plain-English research interpretation
  review**, and the explicit preservation of all retained verdicts
  and project locks.

### Out of scope (forbidden in Phase 4as)

- No data acquisition.
- No Binance endpoint calls.
- No implementation or modification of endpoint code.
- No data-capture implementation.
- No feature implementation.
- No backtest or historical strategy script execution.
- No Phase 4aq rerun.
- No simulation.
- No predictive statistics computation.
- No source / test / script / data / manifest / governance / spec
  / threshold / lock change.
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
- No authorization of Phase 4at, Phase 5, Phase 4 canonical,
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
git branch --show-current  — main.
git log --oneline -16      — Phase 4ar merged at 12f2b55.
git rev-parse main         — 12f2b5558b0812a11526da331fa70feb45fcae9d.
git rev-parse origin/main  — 12f2b5558b0812a11526da331fa70feb45fcae9d.
git check-ignore -v        — data/research/ ignored at .gitignore:88.
```

Phase 4ar files confirmed present on `main`:

- `docs/00-meta/implementation-reports/2026-05-06_phase-4ar_v1-arc-exit-path-forensic-interpretation.md`.
- `docs/00-meta/implementation-reports/2026-05-06_phase-4ar_closeout.md`.
- `docs/00-meta/implementation-reports/2026-05-06_phase-4ar_merge-closeout.md`.

`main` and `origin/main` are in sync. The working tree contains
no unexpected uncommitted change. `.claude/scheduled_tasks.lock`
and `data/research/` are gitignored / transient.

Branch created:

```text
git checkout -b phase-4as/crypto-microstructure-research-reset-mechanism-map
```

---

## 4. Methodology

Phase 4as is a docs-only reset memo. It is built from:

- **static repository inspection** of committed docs (Phase 4ar,
  Phase 4aq, Phase 4ap, Phase 4ao, Phase 4an, Phase 4am,
  Phase 4al, Phase 4ak, Phase 4t, Phase 4m, Phase 3t, M0
  governance file, current-project-state, phase-gates,
  technical-debt register);
- **public web / literature research** restricted to (a) official
  Binance USDⓈ-M Futures developer documentation, (b) the public
  Binance public-data repository, and (c) reputable academic /
  industry references on market microstructure, order-flow
  imbalance, VPIN, deflated Sharpe / probability of backtest
  overfitting, and crypto LOB dynamics.

Citations are concentrated in §9 (Binance data availability map)
and §11 (research validity / anti-overfitting requirements).

The memo does **not**:

- call any Binance endpoint;
- modify any endpoint code;
- acquire any data;
- inspect or modify local `data/research/` outputs;
- run any script (Phase 4aq's script or otherwise);
- implement any feature;
- perform any computation that yields predictive statistics;
- touch credentials, MCP, or any exchange-write surface.

The memo follows the prior-phase docs-only convention used by
Phase 4d, 4e, 4f, 4g, 4h, 4j, 4k, 4m, 4n, 4o, 4p, 4q, 4s, 4t,
4u, 4v, 4w, 4y, 4z, 4aa, 4ab, 4ad, 4ag, 4ah, 4aj, 4ak, 4al, 4an,
4ao, 4ap, and 4ar (no `ruff` / `pytest` / `mypy` execution because
no code, test, or script is changed).

---

## 5. Why a research reset is justified

The cumulative project record now contains the following:

- **R2** — FAILED — §11.6 cost-sensitivity blocks.
- **F1** — HARD REJECT.
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL.
- **V2** — HARD REJECT (terminal for V2 first-spec).
- **G1** — HARD REJECT (terminal for G1 first-spec).
- **C1** — HARD REJECT (terminal for C1 first-spec).
- **5m research thread** — operationally CLOSED (Phase 3t).
- **V1-arc descriptive forensic snapshot** — completed by
  Phase 4aq; interpreted by Phase 4ar; explicitly does not
  authorise rescue or exit redesign.

Each of those candidates was a rule-based variation built
predominantly on lagging OHLCV indicators (EMAs, ATR-derived
windows, breakout / pullback / mean-reversion / contraction /
funding-Z geometry). Their failure modes are not the same in
detail, but they are all consistent with one theme: **the
information set being used was not sufficient or timely enough to
overcome execution cost, slippage, and selection bias** under the
project's locked §11.6 cost realism.

A research reset is therefore justified for three reasons.

1. **The same family has not produced deployable edge.** The
   correct reaction is not to dig in the same family by default,
   especially after the Phase 4ak-adopted post-null cooldown rule
   classifies several lanes as cooled down.
2. **Phase 4aq made the V1-arc geometry's structural ceiling
   explicit.** Favorable excursion existed but did not translate
   into positive realized `net_R`. That is a strong negative
   signal about exit-only redesign as a primary path.
3. **The closest operationally honest forward direction is to
   widen the information set** to mechanisms that are closer to
   the actual supply / demand and execution-pressure structure
   of the venue, not to add more lagging indicators.

The reset does **not** revise verdicts, change locks, amend M0,
reopen cooled-down lanes, or authorise any new strategy. It
simply re-orients the *next* admissibility question away from
"can we improve the previous geometry?" and toward "are there
mechanisms that the previous geometry never measured?".

---

## 6. Why stay in crypto / Binance

The operator's stated preference is to remain in crypto / Binance.
That preference is consistent with the project's infrastructure
and risk profile. The reset endorses it.

**Reasons to stay in crypto / Binance:**

- existing project repository, governance (M0 + locks +
  six-candidate verdict ledger), runtime architecture, exchange
  adapter design, operator dashboard scaffolding, deployment
  model, and host hardening plan are all already specified
  (and partly implemented) for Binance USDⓈ-M Futures;
- Binance public market data is broadly accessible (REST + WS)
  and has a usable historical snapshot bucket at
  `data.binance.vision`;
- 24/7 markets and high event density make microstructure /
  flow research cheaper to run than on session-bound venues;
- crypto perpetual futures expose **derivatives-native context**
  (funding rates, open interest, mark price, liquidations) that
  is not directly available in equities and equities-style
  futures, and that the project has already validated as a
  research surface (Phase 4i datasets, Phase 4j §11 OI subset
  governance) under M0-style admissibility framing.

**Caveats explicitly acknowledged:**

- Binance microstructure is exchange-specific. Findings on
  Binance USDⓈ-M Futures do not automatically generalise to
  other venues / asset classes. This is acceptable because
  v1 live scope is BTCUSDT only on Binance USDⓈ-M Futures.
- Crypto LOB data is well documented as **noisy** — large
  fractions of resting orders are transient, and ephemeral
  orders degrade the informativeness of LOB-derived directional
  alphas (see literature in §11).
- WebSocket streams require careful synchronisation discipline
  (snapshot + diff with `pu` / `U` / `u` matching for the depth
  diff stream).
- Public REST endpoints have **rate limits** and **historical-
  retention limits** for several derivatives-flow datasets
  (e.g. `openInterestHist` retains only the latest 30 days
  per the official endpoint description).
- Liquidation visibility is **deliberately attenuated** by
  Binance: the `forceOrder` snapshot stream pushes only the
  largest liquidation order per 1000 ms per symbol, and the
  REST `forceOrders` endpoint is an authenticated user-scope
  endpoint, not a public market-wide history.
- Storage and reconstruction complexity is substantial,
  especially for tick-level aggTrades and full-depth diff data.
- Research-validity and overfitting risk remain serious
  irrespective of how rich the data becomes.

**Non-crypto migration is mentioned only as a distant optional
alternative, not as a primary recommendation.** It would require
a separately authorised, far broader scoping memo (new venue,
new contract, new data layer, new execution model, new risk
model, new operator workflow) and would not be the cleanest next
move from where the project sits today.

---

## 7. Why move beyond lagging OHLCV indicators

The research record is consistent with the following structural
observation:

- pure lagging OHLCV-indicator families (EMA states, ATR-based
  windows, breakout / pullback / mean-reversion / contraction /
  funding-Z directional triggers, regime gates derived only from
  closes) have been tested across V1-arc, F1, D1-A, V2, G1, and
  C1 and have not produced deployable edge under §11.6 cost
  realism;
- those families share a common attribute: each variable is, by
  construction, a **function of completed-bar prices**, so the
  information arrives **after** the underlying supply / demand
  and execution-pressure event;
- microstructure literature on professional short-horizon
  trading has long emphasised that liquidity, depth, spread,
  aggressive volume, order-flow imbalance, and derivatives
  positioning are closer to the actual driving variables than
  derived OHLCV quantities (Easley, López de Prado, O'Hara
  literature on VPIN; recent crypto LOB / flow imbalance
  research; see §11);
- this does **not** mean microstructure variables automatically
  contain edge. The same literature is explicit that
  microstructure alphas decay rapidly, are noisy, and are
  vulnerable to overfitting and to execution cost — the same
  problems Prometheus already enforces against.

The reset is therefore not a promise of success. It is a
deliberate change of **information set** subject to the same
M0 admissibility, post-null cooldown, no-rescue, cost-realism,
and chronological-validation discipline that the project has
already codified.

---

## 8. Candidate mechanism map

This map enumerates candidate microstructure / derivatives-flow
mechanisms that may be **in scope for future docs-only feasibility
study**. Each entry is a candidate research direction, **not** a
strategy candidate.

For each mechanism the entry records:

- plain-English hypothesis;
- why it might contain edge;
- why it might fail;
- required data (qualitative);
- data granularity;
- historical vs live-capture feasibility (qualitative);
- likely Binance data source (per official Binance docs;
  see §9);
- possible leakage risks;
- cost / slippage sensitivity;
- validation challenges;
- M0 admissibility concerns;
- suitability for future feasibility study.

The entries are deliberately **conceptual**. They do **not**
predeclare any strategy, threshold, gate, parameter, validation
window, mechanism-check decomposition, or pass / fail rule. Any
of those would belong in a future, separately authorised
hypothesis-spec phase analogous to Phase 4o (G1) or Phase 4u (C1)
that itself sits behind the Phase 4ak twelve-clause M0 gate, the
Phase 4m 18-requirement validity gate, and the Phase 4t
10-dimension scoring matrix.

### M-1 — Spread (top-of-book bid-ask spread)

- **Hypothesis:** transient widening / narrowing of the BTCUSDT
  best bid-ask spread carries information about short-horizon
  imbalance and adverse-selection risk.
- **Why it might contain edge:** a sudden spread widening often
  precedes or accompanies aggressive flow / book consumption;
  a sustained narrowing reflects calm two-sided market making.
- **Why it might fail:** spread on highly liquid BTCUSDT
  perpetuals is generally near tick size most of the time;
  widening events are rare and clustered around news / liquidation
  events, where execution cost is also worst (cost-fragility
  risk in the §11.6 = 8 bps HIGH cost regime).
- **Required data:** best-bid / best-ask top-of-book updates,
  ideally event-time, with monotone sequence numbers.
- **Granularity:** tick / event level preferred; sub-second
  acceptable for diagnostic study.
- **Historical vs live:** live capture via book ticker / partial
  depth streams is straightforward; historical at full
  granularity is generally not retained by Binance public archive
  for derivatives book ticker; Tardis-style third-party archives
  may exist but are out of scope at this admissibility layer.
- **Likely Binance data source:** `<symbol>@bookTicker`
  WS stream; partial book depth `<symbol>@depth5/10/20@100ms`;
  REST `GET /fapi/v1/depth`.
- **Leakage risks:** mixing event-time and bar-time; using a
  spread snapshot taken **after** a forward window starts.
- **Cost / slippage sensitivity:** very high; trading exactly
  when spread widens is the worst-cost regime by construction.
- **Validation challenges:** sample-size / event-rate
  collapse; survivor bias toward calm windows.
- **M0 admissibility concerns:** clauses M0.5 (cost realism)
  and M0.7 (edge-rate plausibility separate from
  opportunity-rate) are the binding constraints.
- **Suitability for future feasibility study:** yes, **as a
  context / regime variable**, not as a primary trigger; not
  yet authorised.

### M-2 — Top-of-book depth (best-bid and best-ask sizes)

- **Hypothesis:** the relative size of the best bid vs best ask
  carries short-horizon directional information.
- **Why it might contain edge:** asymmetric top-of-book size is
  the simplest available proxy for top-of-book pressure.
- **Why it might fail:** retail / market-maker quoting on
  Binance USDⓈ-M Futures is highly transient — a large fraction
  of top-of-book size is replaced or cancelled before being
  consumed, which is well documented in crypto LOB literature.
- **Required data:** best-bid / best-ask sizes from
  `<symbol>@bookTicker` or partial book depth.
- **Granularity:** event-time.
- **Historical vs live:** historical depth at full granularity
  is generally not in the public archive; live capture is
  feasible.
- **Likely Binance data source:** `<symbol>@bookTicker`;
  partial book depth.
- **Leakage risks:** treating a snapshot as "before" when it
  was already updated by the trigger event.
- **Cost / slippage sensitivity:** medium-high.
- **Validation challenges:** noise dominance; ephemeral
  orders.
- **M0 admissibility concerns:** clauses M0.4 (rejection
  topology — must be structurally distinct from prior failed
  candidates) and M0.7 (edge-rate plausibility).
- **Suitability:** yes, as a candidate **input**; not yet
  authorised.

### M-3 — Order-book imbalance (top-N levels)

- **Hypothesis:** the imbalance between aggregated bid size and
  aggregated ask size across the top-N price levels predicts
  short-horizon price direction.
- **Why it might contain edge:** widely studied in equities
  microstructure; recent crypto microstructure research finds
  short-horizon predictability of LOB imbalance under careful
  filtering.
- **Why it might fail:** the predictive horizon is short
  (minutes to seconds); a large fraction of orders is transient;
  and the signal is heavily contaminated by noise and quote
  flickering.
- **Required data:** partial book depth at multiple levels,
  ideally with sequence-number-validated diff updates.
- **Granularity:** event-time / sub-second preferred.
- **Historical vs live:** historical full-depth is not in the
  public archive; live capture via diff book + snapshot is
  feasible following the official local-order-book procedure.
- **Likely Binance data source:**
  `<symbol>@depth@250ms / 500ms / 100ms`,
  `<symbol>@depth5/10/20@100ms`, REST `GET /fapi/v1/depth`.
- **Leakage risks:** unsynchronised snapshot / diff streams;
  using `pu` / `U` / `u` mismatched events.
- **Cost / slippage sensitivity:** medium.
- **Validation challenges:** noise; transient liquidity;
  event-time alignment.
- **M0 admissibility concerns:** clauses M0.6 / M0.7
  (opportunity-rate vs edge-rate separation) and M0.10
  (forbidden-rescue check — must not be a
  "rank-then-V2 / G1 / C1-style breakout").
- **Suitability:** yes, with full local order book
  reconstruction; not yet authorised.

### M-4 — Depth imbalance across deeper levels

- **Hypothesis:** imbalance computed deeper into the book
  (beyond top-of-book) carries additional predictive content
  about absorption capacity and one-sided pressure.
- **Why it might contain edge:** recent literature on deep-book
  OFI suggests deep levels reduce RMSE materially, especially
  in high-tick-size markets.
- **Why it might fail:** deep-level activity is sparser, more
  intermittent, and more easily spoofed.
- **Required data:** full book depth or limited but deep
  partial depth.
- **Granularity:** event-time.
- **Historical vs live:** depth at depth >20 typically
  requires live capture or paid third-party archives; out of
  scope at this layer.
- **Likely Binance data source:** REST `GET /fapi/v1/depth`
  with `limit=1000` snapshot, plus diff stream maintained
  locally.
- **Leakage risks:** same as M-3.
- **Cost / slippage sensitivity:** medium.
- **Validation challenges:** sparser events; spoofing-like
  flickering.
- **M0 admissibility concerns:** same as M-3 plus storage /
  feasibility cost.
- **Suitability:** yes, but only **after** M-3 is studied;
  not yet authorised.

### M-5 — Aggressive volume / taker buy-sell imbalance

- **Hypothesis:** the imbalance between aggressive (market /
  taker) buy volume and aggressive sell volume carries
  short-horizon directional information.
- **Why it might contain edge:** aggressive flow is the closest
  observable proxy for revealed conviction at the venue and is
  central to VPIN-style toxicity research, which has been
  reported on crypto with elevated VPIN levels relative to
  equities / commodities.
- **Why it might fail:** aggressive flow alone reverses
  frequently around liquidity events and is sensitive to
  exclusions of insurance / ADL trades.
- **Required data:** aggregate trade events (`aggTrade`) or
  individual market trades; the maker-side flag determines
  which side was the taker.
- **Granularity:** trade-event level.
- **Historical vs live:** historical aggTrades archives are
  available at `data.binance.vision` and via REST
  `GET /fapi/v1/aggTrades`; live capture via
  `<symbol>@aggTrade` is feasible.
- **Likely Binance data source:** `<symbol>@aggTrade` WS;
  REST `GET /fapi/v1/aggTrades`; bulk archive
  `data.binance.vision/data/futures/um/{daily,monthly}/aggTrades/`.
- **Leakage risks:** computing the imbalance over a window
  whose upper boundary leaks into the prediction target.
- **Cost / slippage sensitivity:** medium (entry into the
  aggressive direction itself raises taker cost).
- **Validation challenges:** insurance-fund / ADL trade
  exclusion handling; aggregation rules.
- **M0 admissibility concerns:** clauses M0.5 (cost realism),
  M0.7 (edge-rate plausibility), and M0.10 (no rank-then-trade
  reduction).
- **Suitability:** yes, **strong candidate** for future
  feasibility study; not yet authorised.

### M-6 — Trade burst / volume impulse

- **Hypothesis:** unusually high trade volume per unit time, or
  a burst of trade events, is predictive of short-horizon
  realised volatility and directional follow-through.
- **Why it might contain edge:** burst events are typically
  associated with information arrival; they are observable in
  near real time.
- **Why it might fail:** bursts are also associated with
  liquidations and with one-sided impulse moves where execution
  cost is worst.
- **Required data:** aggTrades or trade-event stream with
  reliable timestamps.
- **Granularity:** sub-second to event-time.
- **Historical vs live:** historical aggTrades available;
  live capture feasible.
- **Likely Binance data source:** `<symbol>@aggTrade` WS,
  bulk archive aggTrades.
- **Leakage risks:** look-ahead from rolling-window
  z-scores; sample-time vs event-time confusion.
- **Cost / slippage sensitivity:** very high during impulse
  events.
- **Validation challenges:** rare-event statistics;
  selection bias.
- **M0 admissibility concerns:** clauses M0.5 (cost realism)
  and M0.6 / M0.7 (opportunity-rate vs edge-rate).
- **Suitability:** yes, mainly as a **regime / context**
  variable; not yet authorised.

### M-7 — Liquidity sweep / book consumption

- **Hypothesis:** an event in which aggressive flow consumes
  multiple price levels in quick succession produces a
  short-lived directional bias and / or a high-probability mean-
  reversion window.
- **Why it might contain edge:** sweep events are well
  documented in the order-flow literature and are a core
  concept in modern HFT pedagogy.
- **Why it might fail:** sweeps are correlated with
  liquidation cascades (M-9) and with regime transitions; they
  are noisy in retail-driven crypto perpetuals.
- **Required data:** combined aggTrades + depth diff so that
  trades can be located against the prevailing book.
- **Granularity:** event-time, with synchronised aggTrades and
  depth.
- **Historical vs live:** historical full reconstruction is
  hard at the public-archive layer; live capture is feasible.
- **Likely Binance data source:** `<symbol>@aggTrade` +
  `<symbol>@depth*` WS, plus snapshot.
- **Leakage risks:** post-trade book updates being mixed
  into the "pre-sweep" book.
- **Cost / slippage sensitivity:** very high.
- **Validation challenges:** event definition is itself a
  research artifact (and therefore a free parameter — must be
  predeclared).
- **M0 admissibility concerns:** clauses M0.4
  (rejection-topology distance: must be distinct from prior
  rejected candidates) and M0.10 (no rescue framing).
- **Suitability:** yes, but only **after** M-3 / M-5 are
  studied; not yet authorised.

### M-8 — Book recovery / replenishment after sweep

- **Hypothesis:** the speed and side of book replenishment after
  a sweep predicts whether the sweep was absorbed (mean
  reversion likely) or signalling (continuation likely).
- **Why it might contain edge:** the replenishment-side imbalance
  is a candidate liquidity-stress signal.
- **Why it might fail:** replenishment can be performed by
  algorithmic market makers or by spoofing; difficult to
  distinguish.
- **Required data:** full local order book, time-aligned to
  trade events.
- **Granularity:** sub-second event-time.
- **Historical vs live:** live capture only at this layer.
- **Likely Binance data source:** depth diff stream + snapshot.
- **Leakage risks:** the "after-sweep" window leaking into
  the prediction target.
- **Cost / slippage sensitivity:** medium-high.
- **Validation challenges:** event definition; spoofing
  resilience.
- **M0 admissibility concerns:** M0.6 / M0.7.
- **Suitability:** yes, **only after** M-7 is studied; not yet
  authorised.

### M-9 — Liquidation cascade proxies

- **Hypothesis:** clustered liquidation events are predictive of
  short-horizon momentum continuation (cascade) and / or
  immediate mean reversion (exhaustion).
- **Why it might contain edge:** liquidations are a
  derivatives-native, asymmetric, leverage-driven flow;
  cascading liquidations are a documented mechanism in crypto
  perpetual markets.
- **Why it might fail:** Binance's public liquidation visibility
  is **deliberately attenuated**. The `forceOrder` stream
  publishes only the largest liquidation order per 1000 ms per
  symbol, and the REST `GET /fapi/v1/forceOrders` endpoint is
  authenticated and user-scope, not public market-wide history.
  Public liquidation data is therefore **a proxy**, not a
  ground-truth feed.
- **Required data:** liquidation snapshots from `forceOrder`
  stream, complemented by aggressive-flow / OI proxies.
- **Granularity:** sub-second event; bounded resolution.
- **Historical vs live:** historical archive of `forceOrder`
  snapshots is limited (third-party reconstructions exist; out
  of scope here); live capture feasible going forward.
- **Likely Binance data source:** `<symbol>@forceOrder` /
  `!forceOrder@arr` WS; REST `forceOrders` is **authenticated**
  and not appropriate for market-wide research.
- **Leakage risks:** treating a 1000 ms snapshot as a complete
  liquidation list.
- **Cost / slippage sensitivity:** very high (trading into a
  cascade is the worst regime).
- **Validation challenges:** incomplete visibility; rare-event
  statistics; selection bias.
- **M0 admissibility concerns:** clauses M0.5 (cost realism),
  M0.7 (edge-rate plausibility), and M0.8 (data feasibility:
  liquidation visibility is **bounded-conditional**, not full).
- **Suitability:** yes as a **context / regime overlay**, not
  as a primary trigger; not yet authorised.

### M-10 — Funding-rate context

- **Hypothesis:** funding rate level / sign / persistence
  carries information about positioning crowdedness and
  implied directional pressure.
- **Why it might contain edge:** documented in crypto perpetual
  literature; is the *context* dimension that D1-A used as a
  *directional trigger* and that failed in that role.
- **Why it might fail:** D1-A demonstrated that funding-Z as a
  directional trigger is a framework-level mismatch; treating
  funding as a context lens, rather than a directional trigger,
  is the only safe re-use.
- **Required data:** funding-rate history (REST), funding
  settlement events.
- **Granularity:** funding-event level (typically 8 h on
  BTCUSDT, with announcement-driven exceptions).
- **Historical vs live:** historical available via REST
  `GET /fapi/v1/fundingRate`; project already has funding
  history in v002 manifests.
- **Likely Binance data source:** REST
  `GET /fapi/v1/fundingRate` and
  `GET /fapi/v1/fundingInfo`.
- **Leakage risks:** including the next-funding event in the
  pre-event predictor window.
- **Cost / slippage sensitivity:** funding cost itself is a
  realised P&L component; preserved verbatim by §11.6.
- **Validation challenges:** the D1-A precedent — funding is
  not a directional trigger.
- **M0 admissibility concerns:** clause M0.10 — must not be a
  D1-A rescue. Only context-style use is admissible.
- **Suitability:** yes as a context / regime / risk overlay
  only; not as a directional trigger; not yet authorised.

### M-11 — Open-interest (OI) context

- **Hypothesis:** OI level / change carries information about
  positioning (build-up / unwind) and may interact with flow
  signals.
- **Why it might contain edge:** OI is the most-studied
  derivatives-native positioning indicator.
- **Why it might fail:** raw OI alone has historically been a
  weak directional predictor; high overfitting risk.
- **Required data:** OI snapshots; OI history (period >= 5 m
  via `openInterestHist`).
- **Granularity:** 5 m to 1 d (REST endpoint period).
- **Historical vs live:** the `openInterestHist` endpoint
  retains only the latest 30 days per Binance documentation;
  live capture can extend coverage forward; the project already
  has Phase 4i metrics datasets for OI under the Phase 4j §11
  governance.
- **Likely Binance data source:** REST
  `GET /fapi/v1/openInterest`,
  `GET /futures/data/openInterestHist`, plus the live capture
  necessary to extend retention.
- **Leakage risks:** look-ahead from same-bar OI change being
  used to predict same-bar return.
- **Cost / slippage sensitivity:** low (used as context).
- **Validation challenges:** retention window; per-bar
  inclusion under Phase 4j §11.
- **M0 admissibility concerns:** clause M0.8 (data feasibility
  — OI subset is governed-partial under Phase 4j §11) and
  M0.10 (no rescue framing).
- **Suitability:** yes as **context / regime variable** under
  the Phase 4j §11 OI-subset governance; not yet authorised.

### M-12 — Funding + OI interaction

- **Hypothesis:** interaction between funding sign / magnitude
  and OI change captures positioning crowdedness more reliably
  than either alone.
- **Why it might contain edge:** the joint variable
  approximates "are leveraged longs / shorts crowding into
  position?".
- **Why it might fail:** sample-size collapse; funding events
  are sparse (every 8 h); interaction effects are easy to
  overfit.
- **Required data:** funding history + OI history.
- **Granularity:** funding-event level for funding;
  5 m / 15 m / 30 m for OI.
- **Historical vs live:** funding is fully historical; OI
  retention bounded as above.
- **Likely Binance data source:** REST `fundingRate` +
  `openInterestHist` + Phase 4i metrics datasets.
- **Leakage risks:** look-ahead from same-window OI / funding
  values into a same-window directional target.
- **Cost / slippage sensitivity:** low to medium.
- **Validation challenges:** sample size at funding-event
  granularity; multiple-comparison risk.
- **M0 admissibility concerns:** M0.7 / M0.10.
- **Suitability:** yes as **regime / context** combination;
  not yet authorised.

### M-13 — Funding + OI + aggressive-flow interaction

- **Hypothesis:** combining funding context, OI change, and
  aggressive flow distinguishes regime conditions in which
  short-horizon flow signals have higher edge from regimes in
  which they do not.
- **Why it might contain edge:** is a candidate **regime
  classifier**, not a strategy itself.
- **Why it might fail:** combinatorial overfitting risk
  (multiple variables, multiple thresholds).
- **Required data:** all of the above.
- **Granularity:** funding-event + OI-bar + flow-bar.
- **Historical vs live:** mixed (see above).
- **Likely Binance data source:** combination.
- **Leakage risks:** same as combined components.
- **Cost / slippage sensitivity:** depends on use.
- **Validation challenges:** strict predeclaration required;
  PBO / DSR / CSCV-style methodology required if a grid is
  ever used.
- **M0 admissibility concerns:** clauses M0.7 (edge-rate vs
  opportunity-rate), M0.11 (predeclared falsification
  criteria).
- **Suitability:** yes as a **context / regime** layer to a
  separately specified primary mechanism; not yet authorised.

### M-14 — Spread / depth / flow regime interaction

- **Hypothesis:** joint regime classifications over spread,
  depth, and aggressive-flow noise level partition the market
  into windows in which microstructure variables behave
  differently.
- **Why it might contain edge:** even if no individual
  microstructure mechanism contains edge in expectation, a
  regime-aware aggregation could identify windows in which
  an existing M-3 / M-5 / M-7 / M-11 mechanism is more or less
  predictive.
- **Why it might fail:** regime classification is the most
  overfitting-prone research style in the project's history
  (G1's failure mode was regime-gate-meets-setup intersection
  sparseness; Phase 4r CFP-1 and CFP-9 are the precedent).
  A microstructure-driven regime layer must be designed under
  M0 with explicit predeclared opportunity-rate and edge-rate
  separation, not as a free parameter pool.
- **Required data:** all of the above; computed as **windowed
  classifications**, not per-bar features.
- **Granularity:** window level.
- **Historical vs live:** mixed.
- **Likely Binance data source:** combination.
- **Leakage risks:** silently re-enabling cooled-down
  candidates by relabelling them as "regime-aware".
- **Cost / slippage sensitivity:** depends on use.
- **Validation challenges:** the same as M-13 plus
  rejection-topology distance to G1.
- **M0 admissibility concerns:** clauses M0.4 (rejection
  topology vs G1) and M0.10 (no rescue framing).
- **Suitability:** yes only after a primary mechanism (M-3 /
  M-5 / M-7) has been independently validated; not yet
  authorised.

---

## 9. Binance data availability map

The following availability map is taken from official Binance
USDⓈ-M Futures developer documentation and the Binance public-
data repository. Phase 4as does **not** call any of these
endpoints; it only records their availability for the future
docs-only feasibility memo.

### 9.1 Aggregate trade stream (aggTrade)

- WS stream: `<symbol>@aggTrade`. Trades are aggregated for
  fills with the same price and taking side every 100 ms;
  insurance-fund trades and ADL trades are not aggregated.
  Effective 2025-12-31, an additional `nq` field excludes
  RPI-order trades.
- Source: Binance Open Platform — Aggregate Trade Streams
  ([developers.binance.com — Aggregate Trade Streams](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Aggregate-Trade-Streams)).
- REST: `GET /fapi/v1/aggTrades` returns the same aggTrade
  records as the WS stream and as historical archives.
- Historical archive: monthly / daily aggTrades archives
  available at `data.binance.vision` per the official Binance
  public-data repository
  ([github.com/binance/binance-public-data](https://github.com/binance/binance-public-data)).

### 9.2 Diff book depth stream

- WS stream: `<symbol>@depth` (default 250 ms),
  `<symbol>@depth@500ms`, `<symbol>@depth@100ms`.
- Pushes order-book diffs; RPI orders are excluded.
- Local order book is maintained by combining WS diffs with a
  REST depth snapshot (`GET /fapi/v1/depth?symbol=BTCUSDT&
  limit=1000`) using the Binance documented `pu` / `U` / `u`
  matching procedure.
- Sources: Binance Open Platform — Diff Book Depth Streams,
  Local Order Book tutorial, How To Manage A Local Order Book
  Correctly
  ([developers.binance.com — Diff Book Depth Streams](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Diff-Book-Depth-Streams),
  [developers.binance.com — How To Manage A Local Order Book Correctly](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/How-to-manage-a-local-order-book-correctly)).

### 9.3 Partial book depth stream

- WS stream: `<symbol>@depth5/10/20@100ms` (also 250 ms /
  500 ms variants where available).
- Top-N levels (N in {5, 10, 20}). RPI orders excluded.
- Source: Binance Open Platform — Partial Book Depth Streams
  ([developers.binance.com — Partial Book Depth Streams](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Partial-Book-Depth-Streams)).

### 9.4 Best bid/ask (book ticker) stream

- WS stream: `<symbol>@bookTicker` (real-time best bid / ask
  price and quantity); also `!bookTicker` for all symbols.
- Source: Binance Open Platform — All Book Tickers Stream
  ([developers.binance.com — All Book Tickers Stream](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/All-Book-Tickers-Stream)).

### 9.5 Liquidation / forceOrder stream

- WS stream: `<symbol>@forceOrder` (per symbol) or
  `!forceOrder@arr` (all symbols). For each symbol, only the
  **largest one** liquidation order within 1000 ms is pushed
  per snapshot; if no liquidation occurs in that window, no
  message is pushed.
- This is **not** a complete liquidation feed — it is a
  bounded-resolution snapshot.
- The REST endpoint `GET /fapi/v1/forceOrders` is **user-scope
  authenticated**, not a public market-wide history; it is
  **not** appropriate for market-wide microstructure research.
- Source: Binance Open Platform — Liquidation Order Streams
  ([developers.binance.com — Liquidation Order Streams](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Liquidation-Order-Streams)).

### 9.6 Funding rate

- REST: `GET /fapi/v1/fundingRate`. Default `limit=500`,
  max `1000`. Optional `startTime` / `endTime`. Shares a
  500/5min/IP rate limit with `GET /fapi/v1/fundingInfo`.
- Source: Binance Open Platform — Get Funding Rate History
  ([developers.binance.com — Get Funding Rate History](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History)).

### 9.7 Open interest

- REST: `GET /fapi/v1/openInterest` returns current OI for a
  symbol.
- REST: `GET /futures/data/openInterestHist` returns
  historical OI statistics with `period` in
  {`5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `6h`, `12h`, `1d`}.
  **Only the last 30 days of data are retained** per the
  endpoint description.
- Source: Binance Open Platform — Open Interest, Open Interest
  Statistics
  ([developers.binance.com — Open Interest](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Open-Interest),
  [developers.binance.com — Open Interest Statistics](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Open-Interest-Statistics)).

### 9.8 Mark price / mark-price klines

- REST: `GET /fapi/v1/premiumIndex` and friends; live mark
  price stream available; mark-price klines available
  historically subject to the documented invalid-window
  governance already adopted in the project (Phase 3r §8;
  Phase 4ad rules).

### 9.9 Public-data archive

- `data.binance.vision` provides bulk historical archives for
  klines, trades, aggTrades, mark-price klines, premium index
  klines, and metrics. Project precedent: Phase 4i (BTCUSDT /
  ETHUSDT 30 m / 4 h klines, OI metrics) and Phase 4ac (alt-
  symbol acquisition) used this archive only.
- Source: `github.com/binance/binance-public-data`
  ([github.com — binance-public-data](https://github.com/binance/binance-public-data)).

### 9.10 Historical-vs-live summary (qualitative, no acquisition implied)

- aggTrades, klines, mark-price klines, premium-index klines,
  funding-rate history: largely **available historically** via
  `data.binance.vision` and / or REST.
- Open interest: limited to last 30 days via
  `openInterestHist`; live capture is required for forward
  extension; partial historical OI for project core symbols is
  already on disk under Phase 4i / Phase 4j §11 governance.
- Top-of-book depth, partial / diff book depth, book ticker:
  not retained in Binance's public archive at full granularity
  for derivatives at the level needed for microstructure
  research; **live capture would be required**.
- ForceOrder (liquidation snapshot): only via WS live capture;
  bounded-resolution snapshots only.

This map is **descriptive availability**, not authorisation.
No data is acquired by this phase.

---

## 10. Data complexity and feasibility

Data complexity for microstructure / derivatives-flow research is
**substantial** but generally manageable with modern tooling and
strong planning. The honest summary is:

- **Storage volume.** Live tick / aggTrades and full-depth diff
  capture for BTCUSDT alone can produce gigabytes per day at
  full granularity. Multi-symbol or multi-month capture
  amplifies that.
- **Order-book reconstruction complexity.** Maintaining a
  correct local order book from Binance's diff stream requires
  the documented `pu` / `U` / `u` matching procedure, with a
  REST snapshot starting point and careful gap detection. Lost
  messages must be detected (not silently filled) and the book
  rebuilt from a fresh snapshot.
- **Snapshot vs diff synchronisation.** Mixing snapshot timestamps
  with diff event timestamps incorrectly is a leakage source.
- **Clock / timestamp consistency.** Wall-clock vs event-time
  vs ingestion-time must be tracked separately. Bar boundaries
  must remain bar-boundary-aligned, not snap-aligned to capture
  start.
- **Symbol selection.** Liquidity heterogeneity is real;
  starting with BTCUSDT (project's locked first-live symbol)
  is the right scope, with ETHUSDT as comparison.
- **Local hardware feasibility.** A modest server / NUC can
  capture BTCUSDT and ETHUSDT depth diff plus aggTrades plus
  forceOrder without exotic hardware, provided WebSocket back-
  pressure is handled. Storage can be tiered (raw → parquet
  → compacted).
- **Deterministic replay.** Research code must replay captured
  streams deterministically by event-time; non-deterministic
  scheduling of feature computation is a leakage source.
- **Missing-message handling.** Gaps must be marked and
  excluded, not filled. The project precedent is Phase 3p §4.7
  / Phase 3r §8 / Phase 4j §11 / Phase 4ad rules.
- **Data-integrity checks.** SHA-paired archives, monotone
  sequence numbers, no-gap predicates, and explicit invalid-
  window enumeration follow the existing project pattern.
- **Schema / versioning.** Future capture would require an
  M0-compatible manifest schema and a clear `__v###` family
  bump, with no silent in-place mutation.
- **Why modern tooling helps but does not eliminate research
  risk.** Faster compute and richer libraries make capture and
  feature computation cheaper; they do not protect against
  selection bias, post-hoc parameter tuning, or symbol /
  window mining.

Phase 4as does not implement, configure, or test any of the
above. They are stated only to inform the future Phase 4at
feasibility memo.

---

## 11. Research validity and anti-overfitting requirements

Any future microstructure / derivatives-flow research must
preserve the project's existing validity and anti-overfitting
discipline. The following requirements are stated as binding
**recommendations** for any future feasibility / hypothesis /
backtest phase, mirroring prior Phase 4k / Phase 4q / Phase 4w
discipline. Phase 4as does **not** authorise any of them.

- **Predeclared hypotheses.** A hypothesis is admissible only
  if it satisfies the Phase 4ak twelve-clause M0 gate, the
  Phase 4m 18-requirement validity gate, the Phase 4t
  10-dimension scoring matrix, and the Phase 4al refined
  no-rescue rule.
- **Walk-forward / temporal validation.** Time-series labels
  must not be shuffled. Holdouts must be chronological. The
  project precedent (Phase 4k / Phase 4q / Phase 4w) is a
  predeclared train / validation / OOS split with explicit
  UTC date boundaries; any future microstructure research
  must adopt an equivalent discipline before any data is
  touched.
- **No random shuffling for labels.** Standard k-fold cross-
  validation is **not** appropriate for time-series microstructure
  forecasting. CSCV (combinatorially symmetric cross-validation)
  is the project precedent for grid evaluations
  ([Bailey & López de Prado, "The Deflated Sharpe Ratio"](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551);
  [Bailey, Borwein, López de Prado, Zhu, "The Probability of Backtest Overfitting"](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253)).
- **Holdout discipline.** No window modification post-hoc; no
  silent extension; no symbol mining; no rerun on observed
  forensic numbers (the Phase 4l / Phase 4r / Phase 4x
  precedent).
- **Negative controls.** Always-active, randomised, and
  non-mechanism baselines are mandatory (Phase 4w precedent;
  Phase 4u opportunity-rate vs edge-rate principle).
- **Baseline models.** A microstructure feature is only
  admissible if it can outperform a non-feature baseline on
  M0 admissibility (clause M0.3) and the Phase 4w-style
  predicted-Δ_R discipline.
- **Feature leakage checks.** A feature window that touches
  the prediction target boundary leaks. Sequence-number
  validation, event-time vs bar-time separation, and
  predeclared lag conventions are mandatory.
- **Latency realism.** Any signal computed from the order book
  or aggressive flow must include a realistic decision latency
  (in milliseconds for HF; in seconds for low-frequency
  context use); it is unsafe to assume zero-latency execution.
- **Execution-cost realism.** §11.6 = 8 bps slippage per side
  is **preserved verbatim**. Microstructure is not exempt from
  cost realism; if anything, alphas tied to liquidity events
  carry higher execution cost.
- **Endpoint-retention awareness.** Plans that depend on
  `openInterestHist` retention beyond 30 days require live
  capture (not authorised here). Plans that depend on
  `forceOrder` completeness must acknowledge bounded
  visibility.
- **Sample-size / event-rate constraints.** Predeclared
  minimum trade counts (Phase 4k / Phase 4q / Phase 4w used
  CFP-1 with a 30-trade floor); microstructure events have
  their own event-rate constraints that must be predeclared
  before any data is touched.
- **No post-hoc symbol / window mining.** Symbol-specific or
  window-specific findings must arise from a predeclared
  hypothesis, not from observing residuals across the cooled-
  down lanes.
- **Crypto LOB noise.** Recent literature explicitly warns
  that a large fraction of resting orders is transient, which
  degrades the informativeness of LOB-derived directional
  alphas
  ([arxiv 2506.05764 — Microstructural Dynamics in Cryptocurrency LOBs](https://arxiv.org/html/2506.05764v2);
  [Easley et al. — Microstructure and Market Dynamics in Crypto Markets](https://stoye.economics.cornell.edu/docs/Easley_ssrn-4814346.pdf)).
- **Order-flow toxicity / VPIN context.** Crypto VPIN levels
  are reported substantially higher than for E-mini S&P 500
  and crude oil futures, consistent with elevated information-
  based trading
  ([Easley, López de Prado, O'Hara — VPIN](https://www.quantresearch.org/VPIN.pdf);
  [SSRN 4814346 — Easley et al. on crypto microstructure](https://stoye.economics.cornell.edu/docs/Easley_ssrn-4814346.pdf)).
- **Order-flow imbalance alpha decay.** Recent HF literature
  reports that intraday OFI alphas decay rapidly out-of-sample
  beyond a 1-day horizon, and that early stopping plus small
  batch sizes are necessary to mitigate overfit in neural
  baselines
  ([arxiv 2507.22712 — Order Book Filtration / Directional Signal Extraction](https://arxiv.org/html/2507.22712v1);
  [Forecasting High Frequency OFI Hawkes processes — arxiv 2408.03594](https://arxiv.org/html/2408.03594v1)).

These references inform the future Phase 4at memo's anti-
overfitting requirements; Phase 4as does not authorise any
implementation.

---

## 12. ML / AI automation placement

Phase 4as records that ML / AI methods may eventually have a
role in this new program. **No ML model or AI agent is
authorised by Phase 4as.**

### What ML could look like in this new program (not authorised)

- **Meta-labeling.** A second-stage classifier that decides
  whether to act on a primary mechanism's signal (e.g. M-5
  aggressive-volume imbalance) given a regime context (e.g.
  funding / OI). This is a known López de Prado pattern.
- **Event classification.** Discrete classifiers for sweep /
  liquidation / replenishment events.
- **Regime classification.** Unsupervised or supervised
  partitioning of windows by spread / depth / flow / funding
  / OI joint state.
- **Probability-of-follow-through models.** Conditional
  probability estimators for short-horizon directional
  follow-through given microstructure context.
- **Feature ranking.** SHAP / permutation-importance ranking
  of microstructure features (with explicit awareness that
  ranking is not edge).
- **Anomaly detection.** Detection of out-of-distribution
  microstructure events (suspect data, suspect market state).
- **Data-quality monitoring.** ML-assisted flagging of
  suspect ticks / suspect snapshots / suspect gaps.

### What AI automation can safely do (not authorised here either)

- literature triage;
- endpoint-doc summarisation;
- prompt generation;
- report consistency checks (e.g. a Phase-XX-style merge
  closeout reading another phase's memo for self-consistency);
- scope-drift detection;
- experiment manifest generation;
- audit checklists.

### Hard constraints (binding regardless of authorisation)

- **No ML model is authorised by Phase 4as.**
- **No AI / LLM trading agent is authorised** by Phase 4as,
  any predecessor phase, or any project-level lock.
- LLMs are **research infrastructure** in this project, not
  execution agents. v1 remains **rules-based** per
  current-project-state and the project-level locks.
- Any future ML use must satisfy Phase 4ak M0 admissibility
  (especially M0.5 cost realism, M0.6 / M0.7 opportunity-rate
  vs edge-rate, M0.10 forbidden-rescue check, M0.11 falsification
  criteria) and the Phase 4m 18-requirement validity gate.

---

## 13. Symbol-specific strategy discussion

A symbol-specific microstructure hypothesis is not automatically
illegitimate, but the project history sets clear constraints.

- **Allowed in principle.** A predeclared, mechanism-first
  hypothesis that explains *why a specific symbol's liquidity,
  derivatives positioning, or exchange-side structure produces
  the mechanism* may be admissible — for example, a hypothesis
  that BTCUSDT-only spread / depth / flow interactions behave
  in a particular way because BTCUSDT is the deepest-liquidity
  symbol on the venue.
- **Forbidden after the fact.** Symbol-specific tuning **after
  observing failure** of a generic candidate is a rescue
  pattern and is forbidden by the Phase 4al refined no-rescue
  rule and the M0 cooled-down families list.
- **Old-strategy alt-symbol reruns remain unauthorised.** The
  Phase 4aa / Phase 4ad / Phase 4ae / Phase 4af / Phase 4ai
  precedents already established that re-running R3 / R2 /
  F1 / D1-A / V2 / G1 / C1 on alt symbols is a rescue path,
  not a new mechanism.
- **Predeclaration requirement.** Any future symbol-specific
  microstructure study must predeclare *why* the symbol's
  specific liquidity / derivatives structure creates the
  mechanism, before any data is touched.

The cleanest first move is to study **BTCUSDT** as the locked
first-live symbol, with ETHUSDT as the comparison symbol.
Multi-symbol expansion is **not** authorised.

---

## 14. Testing-window / regime discussion

The project's history with windowing is unambiguous.

- **Locked windows.** Phase 4k / Phase 4q / Phase 4w used
  predeclared train / validation / OOS holdout windows with
  explicit UTC date boundaries. Phase 4l / Phase 4r / Phase 4x
  evaluated against those windows without modification.
- **No post-hoc window mining.** Changing windows after seeing
  results is forbidden and would be classified as a rescue
  attempt.
- **No window change rescues an old strategy.** R2 / F1 / D1-A
  / V2 / G1 / C1 are not rescued by re-windowing. Their
  verdicts are preserved verbatim.
- **Possible future regime-aware framework.** A future,
  separately authorised regime-first or microstructure phase
  may legitimately propose a richer evaluation framework — for
  example: discovery / validation / final holdout / recent-
  regime stress / walk-forward — provided the framework is
  predeclared, the regime classifier itself is predeclared,
  and the framework cannot silently re-enable cooled-down
  candidates.
- **Walk-forward placement.** Walk-forward is appropriate for
  microstructure research because alpha decay literature
  (cited in §11) reports rapid OOS decay; walk-forward is the
  honest framework for stress-testing decay.

Phase 4as does **not** authorise any window change, regime
classifier, or walk-forward implementation. It only records the
acceptable shape of any future window discussion.

---

## 15. Candidate lane ranking

The reset's candidate lanes are ranked **conservatively** below.
The ranking is governance-safe, not strategy-prioritisation. It
is meant to inform **which docs-only feasibility memo would be
the cleanest next move**.

Ranking dimensions:

1. mechanism plausibility;
2. data availability;
3. implementation complexity;
4. overfitting risk;
5. governance safety (M0, post-null cooldown, no-rescue);
6. distance from old-strategy rescue.

### Lane A — Binance microstructure data availability / capture feasibility

- **Plausibility:** N/A (this is a data-availability lane,
  not a mechanism lane).
- **Data availability:** highest — the lane *is* the data
  availability question.
- **Implementation complexity:** lowest — docs-only.
- **Overfitting risk:** none — no model, no backtest.
- **Governance safety:** highest — no successor authorisation,
  no rescue surface.
- **Distance from rescue:** maximal — does not touch any
  prior candidate.
- **Recommendation:** **the cleanest next move** if separately
  authorised. Becomes Phase 4at (see §16).

### Lane B — Aggressive-volume / order-flow imbalance feasibility (M-5 / M-6)

- **Plausibility:** moderate-high. Aggressive flow is closest
  to revealed conviction; VPIN / OFI literature cited above is
  consistent with informational content.
- **Data availability:** high — historical aggTrades available
  via REST and `data.binance.vision`; live capture feasible.
- **Implementation complexity:** moderate (predeclared event-
  time windows; bulk-volume classification or maker-flag
  classification).
- **Overfitting risk:** moderate.
- **Governance safety:** moderate-high.
- **Distance from rescue:** good (no V1 / V2 / G1 / C1
  rescue).
- **Recommendation:** acceptable secondary if authorised after
  Lane A; not yet authorised.

### Lane C — Order-book imbalance / depth feasibility (M-3 / M-4)

- **Plausibility:** moderate. OBI has a long literature; in
  crypto, OBI signal is noisy and short-lived.
- **Data availability:** mixed — historical full-depth not
  retained in Binance public archive at the level needed for
  research; live capture required.
- **Implementation complexity:** higher (full local order
  book reconstruction with snapshot + diff).
- **Overfitting risk:** moderate-high (transient orders;
  noise; many free parameters).
- **Governance safety:** moderate.
- **Distance from rescue:** good.
- **Recommendation:** acceptable tertiary if authorised after
  Lane A and Lane B; not yet authorised.

### Lane D — Liquidation proxy + flow / OI interaction (M-9 / M-12 / M-13)

- **Plausibility:** moderate. Liquidations are a real
  derivatives-native flow but Binance public visibility is
  bounded to per-1000 ms snapshots.
- **Data availability:** lower (forceOrder is bounded; OI
  retention is bounded).
- **Implementation complexity:** moderate-high (combining
  multiple low-frequency proxies).
- **Overfitting risk:** high (rare events, multiple
  dimensions).
- **Governance safety:** moderate (D1-A precedent — funding
  is context, not directional trigger).
- **Distance from rescue:** acceptable; close enough to D1-A
  context-use that M0.10 needs careful application.
- **Recommendation:** acceptable later option; not next; not
  yet authorised.

### Lane E — ML / meta-labeling admissibility (later only)

- **Plausibility:** depends entirely on a predeclared base
  mechanism; otherwise meta-labeling is empty.
- **Data availability:** inherits the base mechanism's data.
- **Implementation complexity:** highest.
- **Overfitting risk:** highest (model-search +
  feature-search + threshold-search).
- **Governance safety:** lowest in the absence of a base
  mechanism.
- **Distance from rescue:** depends.
- **Recommendation:** **not now.** Becomes admissible only
  *after* one of Lanes A → B → C produces a clean predeclared
  mechanism that needs gating; not yet authorised.

### Conservative reset preference

```text
A → B → C → D → E
```

with each lane gated by separate operator authorisation, M0
admissibility, and the post-null cooldown rule.

---

## 16. Recommended next phase

The cleanest next move, **if separately authorised by the
operator after reviewing Phase 4as**, is:

**Phase 4at — Binance Microstructure Data Availability /
Capture Feasibility Memo**

- **Type:** docs-only.
- **Purpose:** translate §9 of this memo into a precise,
  citation-rich availability map; identify exactly what is
  available historically vs only via future live capture for
  each microstructure / derivatives-flow data family;
  enumerate the data-capture design that would be required
  *if* a future capture phase were ever authorised
  (snapshot + diff procedure; sequence-number validation;
  invalid-window governance; manifest / `__v###` versioning;
  storage layout; deterministic replay; integrity checks);
  predeclare the M0-style admissibility checklist for any
  future capture phase.
- **Boundary:** docs-only; no endpoint calls; no data
  acquisition; no capture implementation; no ML; no strategy
  candidate; no successor authorisation.
- **Authorisation status:** **NOT authorised by Phase 4as.**

Phase 4at would answer: "Exactly what Binance public market
data is available historically vs via live capture for
microstructure / derivatives-flow research, what are the
limitations, and what data-capture design would be required
before implementation?" Phase 4at does **not** authorise
capture, nor does it authorise any subsequent feasibility memo
or strategy.

---

## 17. Explicit non-recommendations

The following are **not** recommended by Phase 4as. Several are
explicitly forbidden by prior governance:

- No immediate strategy design.
- No immediate ML model.
- No immediate data capture.
- No immediate endpoint implementation.
- No old-strategy alt-symbol rerun.
- No R3 / R2 / V1-arc rescue.
- No 5m thread reopening.
- No paper / live work.
- No D1-A reuse as directional trigger.
- No window or threshold change against prior memos based on
  Phase 4l / Phase 4r / Phase 4x forensic numbers.
- No reduction of microstructure to a "rank-then-V2 / G1 /
  C1-style breakout".
- No verdict revision.
- No lock revision.
- No M0 amendment.
- No authorisation of paper / shadow / live-readiness /
  deployment / exchange-write / production-key / authenticated
  APIs / private endpoints / public-endpoint calls in code /
  user stream / WebSocket / MCP / Graphify / `.mcp.json` /
  credentials.

---

## 18. Implementation / governance review

### What changed?

- New file: this memo at
  `docs/00-meta/implementation-reports/2026-05-06_phase-4as_crypto-microstructure-research-reset-mechanism-map.md`.
- Narrow update to `docs/00-meta/current-project-state.md` —
  Phase 4as narrative paragraph and "Current phase:" block
  update, with the prior Phase 4ar block preserved as historical
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
  Phase 3w §6 / §7 / §8 / Phase 4j §11 / Phase 4k / Phase 4p /
  Phase 4q / Phase 4v / Phase 4w / Phase 4ak / Phase 4al /
  Phase 4am / Phase 4an / Phase 4ao / Phase 4ap / Phase 4aq /
  Phase 4ar modification).
- No retained verdict revised.
- No project lock changed.
- No M0 amendment.
- No reopening of the 5m research thread.
- No data acquisition.
- No backtest run.
- No historical strategy script executed.
- No Phase 4aq script re-execution.
- No `data/research/` content committed.

### Were any locks, verdicts, or safety boundaries affected?

No. The retained verdict ledger and project locks are preserved
verbatim. M0 governance is unchanged. The 5m closure (Phase 3t)
is preserved. The cost lock (§11.6) and project locks (§1.7.3)
are preserved. The stop-trigger-domain governance (Phase 3v §8),
break-even / EMA slope / stagnation governance (Phase 3w §6 /
§7 / §8), mark-price gap governance (Phase 3r §8), and OI subset
governance (Phase 4j §11) are all preserved. The Phase 4ak M0
gate, post-null cooldown rule, cooled-down families list, and
memo template are all preserved.

### Were any historical scripts, source files, existing data, manifests, or tests modified?

No. Phase 4as is a docs-only research reset memo.

### Is the phase mergeable as docs-only?

Yes. Phase 4as adds two markdown files under
`docs/00-meta/implementation-reports/` plus a narrow update to
`docs/00-meta/current-project-state.md`. Per the operator's
instruction in this prompt, **Phase 4as is not merged in this
prompt**.

---

## 19. Research interpretation review (plain English)

### What did this phase prove?

Phase 4as did not prove anything in the predictive-statistics
sense. As a docs-only reset memo it consolidates the existing
project record (Phase 4ar interpretation; Phase 4aq descriptive
forensic snapshot; six-candidate rejection topology; M0
governance; cost / position / leverage locks; 5m closure) and
documents that the project's research program should now widen
its information set toward Binance-native microstructure and
derivatives-flow mechanisms, while preserving every prior
verdict and lock and without authorising any data acquisition,
capture, model, or strategy.

### What did this phase not prove?

Phase 4as did not prove that any specific microstructure
mechanism contains edge. It did not run any computation. It did
not acquire any data. It did not authorise any successor phase.
It did not authorise any data capture or endpoint call. It did
not produce a new strategy candidate. It did not amend M0. It
did not modify any verdict or lock.

### Which original questions did it answer?

The Phase 4as question — "What new mechanism classes are
plausibly worth studying after the V1 / exits arc closed, and
how should Prometheus evaluate them before any data acquisition,
feature implementation, or strategy design is authorised?" —
is answered across §5 (why a research reset is justified),
§6 (why stay in crypto / Binance), §7 (why move beyond lagging
OHLCV indicators), §8 (candidate mechanism map), §9 (Binance
data availability map), §10 (data complexity / feasibility),
§11 (research validity / anti-overfitting requirements), §12
(ML / AI automation placement), §13 (symbol discussion), §14
(window / regime discussion), §15 (candidate lane ranking),
§16 (recommended next phase Phase 4at), and §17 (explicit
non-recommendations).

### Which original questions remain open?

- Whether any of the M-1 → M-14 mechanisms contains edge under
  the project's locked cost realism. **This is not answered
  by Phase 4as and should not be answered by Phase 4as.**
- Whether Phase 4at would be the cleanest next move. The memo
  recommends Phase 4at but does not authorise it.
- Whether any future microstructure research will eventually
  satisfy M0 admissibility, Phase 4m validity, Phase 4t scoring
  matrix, the Phase 4ak post-null cooldown rule, and the
  Phase 4al refined no-rescue rule. This is operator-driven.

### What does it mean for strategy research?

The reset re-orients the *next* admissibility question from
"can we improve previous geometry?" to "are there mechanisms
the previous geometry never measured?" without authorising any
new mechanism, model, or strategy. The cooled-down families list
is preserved. The six-candidate rejection topology is
preserved. The cost lock, position lock, leverage lock, and
mark-price stop lock are preserved. M0 remains the binding
admissibility framework.

### What does it mean for governance?

Phase 4as reaffirms the binding prospective governance: M0
admissibility, post-null cooldown, §11.6, §1.7.3, Phase 3r §8,
Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k,
Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak adoption,
Phase 4al refined no-rescue + §13 / §14, Phase 4am §11.A audit
findings, Phase 4an inventory, Phase 4ao harmonization,
Phase 4ap forensic plan, Phase 4aq computation result preserved
as descriptive evidence only, and Phase 4ar interpretation
result preserved as descriptive interpretation only. None is
amended.

### What is the clean next step?

Operator review of Phase 4as. **No successor phase is authorised
by Phase 4as.** The clean next step is operator-driven only.
Acceptable, separately-authorised future options include remain
paused (recommended), Phase 4at as a docs-only Binance
microstructure data availability / capture feasibility memo,
or further docs-only governance memos on precise governance
questions. None is started or authorised by Phase 4as.

### What should we not do yet?

- No data acquisition.
- No Binance endpoint calls.
- No data-capture implementation.
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

## 20. Preserved verdicts, locks, and no-rescue constraints

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
  Phase 4ar amendment.

---

## 21. Final status

Phase 4as is complete on branch
`phase-4as/crypto-microstructure-research-reset-mechanism-map`.

- **Memo:** this file.
- **Closeout:** to be added at
  `docs/00-meta/implementation-reports/2026-05-06_phase-4as_closeout.md`
  in the next commit on this branch.
- **Successor authorisation:** none. **Phase 4at / Phase 5 /
  Phase 4 canonical / paper / shadow / live-readiness /
  deployment / exchange-write / production-key / authenticated
  APIs / private endpoints / user stream / WebSocket / MCP /
  Graphify / `.mcp.json` / credentials all remain unauthorised.**
  Acquisition of 5m / 1m / aggTrades / tick / mark-price 30m /
  4h / order-book data also remains unauthorised.
- **Recommended state:** **paused** unless the operator
  separately authorises a future phase. The merge of Phase 4as
  into `main` is itself a separate operator decision and is
  **not** performed by this prompt.

## End of Phase 4as memo
