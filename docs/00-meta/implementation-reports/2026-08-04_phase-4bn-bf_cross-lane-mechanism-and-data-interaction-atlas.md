# Phase 4bn-BF — Project-Wide Cross-Lane Mechanism and Data-Interaction Atlas

## 1. Phase identity

Phase 4bn-BF — Project-Wide Cross-Lane Mechanism and Data-Interaction Atlas.

A **docs-only research-space reconstruction, external-theory review, data-admissibility mapping, and
candidate-screening** phase. It constructs a project-wide atlas of scientifically meaningful interactions
among Prometheus's mechanism and data families, and screens each interaction against admissibility,
duplication, proxy validity, researcher freedom, and decision consequence.

This is an **interaction-discovery and screening phase**, not an experiment-design phase. It did not begin
with a favoured example. It mapped the full relevant space first and reached its dispositions afterwards.

**Risk tier.** Tier 1 / Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md`. The phase may
influence future scientific direction even though it opens no market data, implements nothing, selects no
research lane, and authorizes no successor. It mutates no eligibility, manifest, verdict, reserve, ledger,
or lock.

```text
Phase 4bn-BF constructs a cross-lane mechanism and data-interaction atlas; it selects no research lane and authorizes no successor phase.
```

## 2. Live base and branch evidence

Verification was performed live in `D:\Prometheus` before any mutation. The expected base was **not**
assumed.

```text
$ git fetch origin
$ git status --short
?? .claude/scheduled_tasks.lock

$ git branch --show-current
main

$ git rev-parse main
d8182d96e11bc11517c3432eeddc1fd6ea4cacb5

$ git rev-parse origin/main
d8182d96e11bc11517c3432eeddc1fd6ea4cacb5

$ git log --oneline --decorate -15
d8182d9 (HEAD -> main, origin/main, origin/HEAD) docs(phase-4bn-be): finalize merge closeout shas
ef38f04 research(phase-4bn-be): merge external-theory new-lane shortlist
0ddf082 (origin/phase-4bn-be/..., phase-4bn-be/...) docs(phase-4bn-be): add merge closeout
6de6217 research(phase-4bn-be): assess external-theory new-lane candidates
fe28cfc docs(phase-4bn-bc): finalize merge closeout shas
4236d19 docs(phase-4bn-bc): merge CF-1 filter-admissibility assessment
6b5de79 (origin/phase-4bn-bc/..., phase-4bn-bc/...) docs(phase-4bn-bc): add merge closeout
6816cf5 docs(phase-4bn-bc): correct M0 clause mapping
bcf3685 docs(phase-4bn-bc): assess CF-1 filter admissibility and consequences
7bb6819 docs(phase-4bn-bb): finalize merge closeout shas
0200d57 research(phase-4bn-bb): merge corrected CF-1 valid-pass execution
4214c65 (origin/phase-4bn-bb/..., phase-4bn-bb/...) docs(phase-4bn-bb): add merge closeout
3451657 docs(phase-4bn-bb): add closeout
6ba76b5 research(phase-4bn-bb): record corrected CF-1 execution verdict
0f5942b feat(phase-4bn-bb): implement corrected CF-1 execution
```

All four required live-state assumptions held:

| Assumption | Observed |
|---|---|
| current branch = `main` | confirmed |
| `main == origin/main` | confirmed |
| `main == d8182d96e11bc11517c3432eeddc1fd6ea4cacb5` | confirmed |
| Phase 4bn-BE merge-closeout and SHA finalization are the current tip | confirmed — `ef38f04` `--no-ff` merge, `d8182d9` SHA-finalization tip |
| no later committed verdict, lock, reserve state, active lane, or authorization shift | confirmed — `d8182d9` is the tip and is the Phase 4bn-BE finalization commit |

The only untracked item throughout was the permitted transient `.claude/scheduled_tasks.lock`. It was
never staged, modified, deleted, cleaned, moved, or committed.

**Branch created after verification:**

```text
phase-4bn-bf/cross-lane-mechanism-data-interaction-atlas
```

No additional branch was created. No work was performed on `main`.

## 3. Authorization boundary

### 3.1 Authorized and performed

Read committed Prometheus documentation, committed source definitions and schemas (inspected, never
executed), and Git metadata, read-only. Read the `D:\Prometheus-Project-Control` continuity files
read-only as context. Perform read-only external bibliographic and primary-source research over public
academic repositories, official exchange documentation, and static official archive-index metadata.
Author exactly two new documentation files under `docs/00-meta/implementation-reports/`. Commit and push
the dedicated phase branch.

### 3.2 Not authorized and not performed

To open, read, list for content, sample, parse, hash, inspect, score, summarize, or enumerate anything
under `data/microstructure/` or `data/research/`; to inspect any Phase 4bn-AZ or Phase 4bn-BB local
artefact; to open any Parquet, local research JSON, prediction, target, manifest, sidecar, reserve
envelope, or market-data archive; to run any builder, feature or label pipeline, model, research runner,
diagnostic, replay, bootstrap, backtest, or test; to run `pytest`, Ruff, or mypy; to call any Binance API
or exchange endpoint, including `exchangeInfo`; to download any archive object or market-data file; to
open a WebSocket; to use credentials, `.env`, authenticated services, MCP, or Graphify; to install a
package, clone an external repository, execute external code, or download an executable or model weights;
to run Kronos or any other model; to open or spend any evidence reserve; to use external data to
calculate a Prometheus result; to modify, delete, or rename any existing tracked file; to write to
`D:\Prometheus-Project-Control`; to invoke Fable or any external reviewer; to select a lane; or to
authorize any successor phase.

This phase is **static repository reasoning plus read-only external literature and documentation research
only**. No scientific value is newly computed from any evidence-bearing data.

### 3.3 Preserved locks and semantic boundaries

Unchanged, unsoftened, and not reinterpreted by this phase:

```text
Prometheus is a research project.
Nothing is authorized to trade.

The project is paused.
No active research lane is open.

Strategy M0 is NOT CLEARED.

research_eligible = false
eligibility_gate_status = pending
all authorization flags = false

CF1_VALID_PASS remains a development-level forecast result only.
It is not a signal, recommendation, strategy, action, profitability result,
economic-materiality result, tradability result, M0 clearance, or
reserve-confirmed result.

REJECT_CF1_FILTER_CONTINUATION__REMAIN_PAUSED remains binding.
STOP_LONGHORIZON_ML_ARC remains binding.
STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE remains binding.
REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH remains binding.
R3 — NO_CF1_RESERVE_PATH_JUSTIFIED__REMAIN_RESERVED remains binding.

PRE_V002_INTERNAL_HOLDOUT   = CONSUMED
V002_TERMINAL_WINDOW        = UNTOUCHED_RESERVED
V002_SEALED_TEST            = UNTOUCHED_RESERVED
HIST_TOB_BOOKTICKER_SOURCE  = INADMISSIBLE_OR_UNAVAILABLE
test_rows_loaded            = 0

The locked economic reference remains:
8 bps per side
16 bps round trip
```

Also preserved: the Phase 4bn-AE §19 absolute strategy / PnL / backtest boundary; the Phase 4ak
twelve-clause M0 gate with its §6 post-null cooldown rule and §7.A–§7.E cooled-down-family list; the
Phase 4bn-AT §58 prohibition on any friction evidence revising completed metrics, completed rejections,
prior materiality decisions, or the locked cost reference; the Phase 4aw always-raising
`flip_research_eligible(...)` invariant (never invoked); the retained verdict ledger (H0, R3, R1a,
R1b-narrow, R2, F1, D1-A, the 5m thread, V2, G1, C1); the Phase 4bn-BB and Phase 4bn-AZ no-rerun
boundaries; every dataset identity and hash; and all split, holdout, sidecar, and storage policies.

Phase 4bn-BE remains merged with:

```text
CANDIDATE_SHORTLIST_PRODUCED__INDEPENDENT_FABLE_REVIEW_REQUIRED__NO_LANE_SELECTED__MERGED_TO_MAIN__NO_SUCCESSOR_AUTHORIZED
```

Its two candidates, `NL-C1` and `NL-C2`, remain **unselected, unranked, un-cleared, and unauthorized**.
Neither is reopened by this phase, and no interaction in this atlas is admitted on the ground that it
combines either candidate with another data family.

Two semantic boundaries govern every card below:

```text
statistically informative ≠ economically material
a feature cross ≠ a mechanism interaction
```

## 4. Repository evidence inspected

Committed and read-only. `README.md` and `docs/00-meta/current-project-state.md` are treated as stale
navigational documents and were not relied upon; recent implementation reports, merge-closeouts, binding
governance documents, and committed source outrank them.

**Binding governance.**

- `docs/00-meta/m0-mechanism-admissibility-gate.md` — the twelve-clause M0 gate; §6 post-null cooldown
  rule and §6.A "materially new" test; §7 cooled-down families (§7.A price-only directional depletion;
  §7.B cross-sectional cooldown; §7.C derivatives-context `CONDITIONAL_ONLY / HIGH_D1-A_RESCUE_RISK`;
  §7.D microstructure / order-flow / liquidity-timing `NOT_RECOMMENDED_NOW`; §7.E mark-price /
  execution-realism `NOT_RECOMMENDED_NOW`).
- `docs/00-meta/process/evidence-budget-ledger.md` — §2 status vocabulary; §5 reserve table; §6
  inadmissible-source registry; §7 transition history.
- `docs/00-meta/process/scarce-reserve-spending-and-late-inadmissibility-standard.md` — spending
  authority, §11 automatic refusal conditions, §15 bounded independent-review standard.

**Process standards under `docs/00-meta/process/`:** `phase-workflow-standard.md`,
`phase-risk-tiering-standard.md`, `operator-report-standard.md`, `merge-closeout-standard.md`,
`claude-code-context-management-standard.md`.

**Scientific and governance lineage.**

- `2026-05-06_phase-4as_crypto-microstructure-research-reset-mechanism-map.md` — the M-1 … M-14 mechanism
  enumeration (§8); the Binance availability map (§9); research-validity requirements (§11); the
  ML-placement boundary (§12).
- `2026-05-07_phase-4at_binance-microstructure-data-availability-capture-feasibility.md` — §6.1–§6.22
  per-family availability matrix and §7 historical-vs-live classification matrix.
- `2026-07-12_phase-4bn-as_longhorizon-ml-ambiguity-decision-memo.md` — `STOP_LONGHORIZON_ML_ARC`.
- `2026-07-14_phase-4bn-at_top-of-book-mechanism-admissibility-bounce-preregistration.md` —
  `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`; §42 total-cost limitations; §58 forbidden claims.
- `2026-07-15_phase-4bn-aw_return-to-strategy-research-candidate-family-screening.md` — §9 stopped-arc
  lineage; §10 reserve ledger; §11 admissible / inadmissible source inventory; §14 the fourteen generated
  candidates; §15 the eleven rejections; CF-1 / CF-2 / CF-3.
- `2026-07-15_phase-4bn-ax_post-fable-candidate-selection-cf1-decision-consequence-forced-flow-overlap-audit.md`
  — CF-1 selection; §13 non-trading boundary; §14 predeclared pass/fail consequence; §17
  momentum-by-success risk.
- `2026-07-15_phase-4bn-ax_forced-flow-overlap-proxy-validity-and-m0-audit.md` —
  `REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`; §4 committed 45-column aggTrades feature
  inventory; §5 missing liquidation data and `FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS`; §6 prior-overlap
  table; §12 confound analysis; §14 proxy-validity standard.
- `2026-07-21_phase-4bn-bb_cf1-corrected-execution-and-verdict.md` and its artefact/leakage companion —
  `CF1_VALID_PASS` (referenced only for boundary statements; no metric recomputed or reinterpreted).
- `2026-07-31_phase-4bn-bc_cf1-valid-pass-filter-admissibility-and-consequence-assessment.md` — §11
  filter-admissibility criteria; §13 decision-consequence test; §14 researcher-freedom assessment; §15
  anti-post-hoc analysis; §21 claim-scope table.
- `2026-07-31_phase-4bn-bc_cf1-m0-evidence-budget-and-anti-rescue-audit.md`.
- `2026-08-03_phase-4bn-be_external-theory-new-lane-discovery-and-admissibility-shortlist.md` — §6.1
  thirteen verified primary sources; §6.2 named-unverified works; §6.3 retrieval limitations; §8.2
  admissibility frame; §8.3 prohibition frame; §9 the N-01 … N-16 negative-search log; §10 the NL-C1 and
  NL-C2 cards.
- `2026-08-03_phase-4bn-be_closeout.md`; `2026-08-04_phase-4bn-be_merge-closeout.md`.

**Committed source definitions and schemas (inspected, not executed).**

- `src/prometheus/research/microstructure/features_schema.py` — `FEATURE_WINDOWS_MS_V001 = (1000, 5000,
  15000, 60000)`; `FEATURE_WINDOW_LABELS_V001 = ("1s", "5s", "15s", "60s")`; the ten
  `PER_WINDOW_FEATURE_TEMPLATES`; the 45-column `FEATURE_NAMES_V001` set including `utc_hour`,
  `utc_minute`, `milliseconds_since_day_start`, `invalid_window_flag`, `rolling_missing_window_flag`; and
  `FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS`, which bars `liquidation`, `funding`, `open_interest`,
  `order_book`, and `mark_price` (among others) from any feature column.

**Roadmap / debt.** `docs/12-roadmap/phase-gates.md` and `docs/12-roadmap/technical-debt-register.md` were
inspected; both are v1-era strategy-promotion and deferral documents. Neither adds a prohibition beyond
those recorded above, and neither is modified.

**Read-only continuity context from `D:\Prometheus-Project-Control`:** `OPERATING_CONVENTIONS.md`,
`DECISIONS.md` (D-001 … D-017), `CURRENT_STATE.md`, `ACTIVE_WORK.md`, `LIMITATIONS.md`. All five were
present and readable.

`CURRENT_STATE.md` carries a **snapshot date of 2026-08-03** and records `main == fe28cfcc…`, i.e. the
Phase 4bn-BC tip. Live committed evidence in `D:\Prometheus` shows `main == d8182d96…` with Phase 4bn-BE
merged. **Live evidence outranks Project-Control and is used throughout.** The lag is recorded here as an
observation only; Project-Control was not modified. `LIMITATIONS.md` §10.2, §10.1, and §6.2 are carried
into this phase's reasoning.

## 5. External-research method

### 5.1 Causal order

Search proceeded in one direction only:

```text
external mechanism theory asserting an interaction
→ the observable that the interaction (not either leg alone) implies
→ the data requirement of BOTH legs
→ Prometheus admissibility of both legs
→ prior-family and stopped-arc distance
→ decision consumer
→ disposition
```

No interaction was generated from an available feature column, an existing implementation capability, a
model family, a Prometheus result, a desire to rescue a stopped arc, or a possible trading use. The
mandate's fifteen mandatory starting interactions (§11 of the authorization) were assessed **after** the
parent-layer matrix was constructed, so that none of them received privileged treatment; every one of the
fifteen is disposed of in §10 or §11 below and is indexed in §19.

### 5.2 The qualifying-interaction test applied to every family

A family was admitted into the atlas as an *interaction* only if it asserted that

```text
mechanism or state A changes the observable consequence of mechanism B
```

or that

```text
the joint state of A and B identifies a mechanism that neither A nor B identifies alone.
```

Families that reduced to "both variables are predictive", "a model can consume both modalities", "the
interaction coefficient is significant", or "a new architecture accepts multiple inputs" were not counted
as interactions and are recorded as such where they arose. Equivalent formulations were collapsed into a
single family; arbitrary Cartesian products of committed feature columns were not enumerated.

### 5.3 External actions performed and not performed

**Performed.** Bibliographic web searches; read-only retrieval of publisher, academic-repository,
institutional, and preprint-server pages; DOI and citation verification; reading of official exchange
documentation content already committed to the Prometheus record.

**Not performed.** No Binance API or exchange endpoint call of any kind, including `exchangeInfo`; no
archive-object download; no market-data download; no historical trade, quote, order-book, liquidation,
funding, open-interest, or derivatives-data acquisition; no authenticated service; no credential or
`.env` use; no WebSocket; no MCP or Graphify; no package installation; no external repository clone; no
execution of external code; no executable or model-weight download. **No external datum was used to
calculate any Prometheus result.** No temporary paper was committed to the repository.

### 5.4 Source-quality standard

The Phase 4bn-BE hierarchy is carried forward unchanged. **Primary — admitted for substantive claims:**
peer-reviewed journal articles; working papers from recognized academic or institutional repositories;
official exchange market-structure and contract documentation; official dataset specifications; authors'
technical appendices and replication documentation. **Secondary — location aid only:** search-result
summaries, bibliographic aggregators, blogs, newsletters, vendor and exchange-marketing material, social
media. Secondary material carries **no substantive claim in this report**.

Publication venue, citation count, and author reputation are not evidence that a mechanism is admissible
for Prometheus. Repository documents outrank external theory absolutely for the status of Prometheus
decisions, locks, prior work, and authorization.

### 5.5 Primary sources newly retrieved or bibliographically verified in this phase

All accessed **2026-08-04 (UTC)**. Twelve sources.

| # | Authors | Title | Year | Venue / institution | Identifier | Mechanism claim supported | Interaction claim supported | Limitation relevant to Prometheus |
|---|---|---|---|---|---|---|---|---|
| X1 | Kyle, A. S. | Continuous Auctions and Insider Trading | 1985 | Econometrica 53(6), 1315–1335 | JSTOR stable `https://www.jstor.org/stable/1913210` | A risk-neutral insider trades against noise traders and competitive market makers; the equilibrium price impact coefficient λ maps order flow into price change | **`1/λ` is market depth.** The price consequence of a given order flow is set by depth: the same flow moves price more in a thin book than a deep one. This is the canonical flow × liquidity interaction | Depth is the load-bearing leg and is a **latent order-book quantity**. Prometheus holds no admissible historical depth. The model also assumes a single strategic insider and a batch auction, neither of which describes a continuous crypto perpetual book |
| X2 | Admati, A. R.; Pfleiderer, P. | A Theory of Intraday Patterns: Volume and Price Variability | 1988 | The Review of Financial Studies 1(1), 3–40 | `https://academic.oup.com/rfs/article-abstract/1/1/3/1601212` | Concentrated-trading patterns arise **endogenously** from the strategic behaviour of discretionary liquidity traders and informed traders | **Clock time × participant composition × volume and price variability.** The volume and volatility consequence of a given clock interval depends on which trader types have chosen to concentrate there — the interaction is between the timing layer and the composition of flow | Participant composition is unobservable in aggTrades. The theory is developed for a session-bound equity market with an opening and a close; Binance USDⓈ-M perpetuals trade 24/7 with no session boundary, so the model's central coordination device is absent |
| X3 | Bessembinder, H.; Seguin, P. J. | Price Volatility, Trading Volume, and Market Depth: Evidence from Futures Markets | 1993 | The Journal of Financial and Quantitative Analysis 28(1), 21–39 | JSTOR stable `https://www.jstor.org/stable/2331149` | Partitioning volume into expected and unexpected components shows unexpected volume shocks have the larger volatility effect, and the effect is asymmetric between positive and negative shocks | **Volume shock × open interest → volatility.** Open interest proxies market depth and **large open interest mitigates volatility**: the volatility consequence of a given volume shock depends on the outstanding positioning state. This is the canonical activity × positioning interaction | The moderator is **open interest**, which for a 2024 window is `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` under the committed 30-day-retention record. The expected/unexpected decomposition is a researcher-chosen time-series model, not an external constant. Sample is eight physical and financial futures markets, not crypto perpetuals |
| X4 | Dufour, A.; Engle, R. F. | Time and the Price Impact of a Trade | 2000 | The Journal of Finance 55(6), 2467–2498 | DOI `10.1111/0022-1082.00297` | Using Hasbrouck's (1991) VAR for prices and trades, as the duration between consecutive transactions decreases, the price impact of trades, the speed of price adjustment to trade information, and the positive autocorrelation of signed trades all **increase** | **Trade duration × price impact.** The price consequence of a trade is conditioned on the elapsed time since the previous trade; active periods are interpreted as periods of increased informed presence and therefore reduced liquidity | The impact leg is measured as a **quote-midpoint revision** in the Hasbrouck VAR. Prometheus has no admissible historical quote series, so the interaction's dependent variable cannot be constructed. Substituting a last-trade price for the midpoint reintroduces exactly the bid–ask bounce the stopped Phase 4bn-AT arc could not resolve |
| X5 | Hasbrouck, J.; Seppi, D. J. | Common factors in prices, order flows, and liquidity | 2001 | Journal of Financial Economics 59(3), 383–411 | `https://www.sciencedirect.com/science/article/abs/pii/S0304405X0000091X` | Returns and order flows are both characterized by common factors; commonality in order flows explains roughly two-thirds of the commonality in returns | **Market-wide flow state × own-instrument response**, and **liquidity proxies × trade-impact coefficients**: bid–ask spread and quote sizes help explain time variation in trade impacts, so the impact of own flow is conditioned on own liquidity as well as on the common component | Requires **synchronous multi-instrument order flow**. Multi-symbol aggTrades are archive-available but **not acquired**, and the liquidity-proxy leg requires quotes and quote sizes, which are inadmissible. Ground truth is 30 Dow stocks |
| X6 | Large, J. | Measuring the resiliency of an electronic limit order book | 2007 | Journal of Financial Markets 10(1), 1–25 | `https://www.sciencedirect.com/science/article/abs/pii/S1386418106000528` | Resiliency is formalized as a continuous-time impulse response over event intensities, estimated with a mutually exciting ten-variate Hawkes process; in over 60% of cases the book does **not** replenish reliably after a large trade, and when it does the half-life is around 20 seconds | **Large trade × replenishment state.** The consequence of a liquidity-consuming event depends on whether and how fast the book replenishes — a burst into a resilient book and a burst into a depleted book are different events with different subsequent price behaviour | The replenishment leg is **limit-order-book event data**. Prometheus has no admissible historical depth or diff-depth series; the mechanism is unobservable in aggTrades by construction. Sample is one LSE equity over 22 trading days in 2002 |
| X7 | Brunnermeier, M. K.; Pedersen, L. H. | Market Liquidity and Funding Liquidity | 2009 | The Review of Financial Studies 22(6), 2201–2238 | DOI `10.1093/rfs/hhn098` | A model linking an asset's market liquidity to traders' funding liquidity; under stated conditions margins are destabilizing and the two liquidities are mutually reinforcing, producing **liquidity spirals** | **Funding-constraint state × market-liquidity state.** Each changes the consequence of the other; the spiral is a joint object that neither leg identifies alone. This is the canonical liquidity × positioning/forced-flow interaction | **Both legs are inadmissible for Prometheus.** Market liquidity requires depth or quotes (`HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE`; depth is prospective-capture-only). Funding-constraint state requires margin, positioning, or liquidation data — open interest is 30-day-retained and `forceOrder` has no public archive |
| X8 | Gârleanu, N.; Pedersen, L. H. | Margin-based Asset Pricing and Deviations from the Law of One Price | 2011 | The Review of Financial Studies 24(6), 1980–2022 | DOI `10.1093/rfs/hhr027` | With heterogeneous-risk-aversion agents facing margin constraints, required returns rise in both beta and margin requirement; binding margin constraints lower risk-free rates and raise Sharpe ratios, especially for high-margin securities | **Margin/funding-constraint state × basis.** A "basis" — a price gap between securities with identical cash flows but different margins — is *generated by* the constraint state, so the observed basis has a different meaning depending on whether constraints bind | Identifying the constraint state requires margin, collateral, or positioning observables that Prometheus does not hold for the study window. The theory is about cash-flow-identical securities with different margins, not about a perpetual and its composite spot index |
| X9 | Cont, R.; Kukanov, A.; Stoikov, S. | The Price Impact of Order Book Events | 2014 | Journal of Financial Econometrics 12(1), 47–88 | DOI `10.1093/jjfinec/nbt003` | Over short intervals, price changes are driven mainly by order-flow imbalance (OFI) at the best bid and ask | **OFI × depth.** There is a linear relation between OFI and price change **with a slope inversely proportional to market depth**; combined with a scaling argument this implies the observed square-root relation between price move magnitude and volume. The moderator is explicitly the depth state | The OFI construct is defined over **limit-order, market-order, and cancellation events at the best quotes** — not over executed aggregate trades. Prometheus's `rolling_aggressive_*` columns are executed-trade imbalances, a strictly coarser object, and the depth moderator is entirely absent. Ground truth is NYSE TAQ for fifty US stocks |
| X10 | Andersen, T. G.; Bollerslev, T. | Intraday periodicity and volatility persistence in financial markets | 1997 | Journal of Empirical Finance 4(2–3), 115–158 | `https://www.sciencedirect.com/science/article/abs/pii/S0927539897000042` | Pervasive intraday periodicity in return volatility has a strong impact on the dynamic properties of high-frequency returns; an explicit periodic modelling procedure integrates standard volatility models with microstructure variables | **Clock time × volatility dynamics.** The measured persistence of volatility is conditioned on the periodic component; failing to account for it distorts the dynamics — so the timing layer changes the observable consequence of the volatility mechanism | The deterministic periodic component in FX and equities is anchored to **session and macro-announcement structure**. Its analogue on a 24/7 perpetual is not established by this source, and the object it conditions is the CF-1 target family on the CF-1 substrate |
| X11 | Kim, C.; Hansen, P. R. | The Quarter-Hour Effect: Periodic Algorithmic Trading and Return Predictability in Cryptocurrency Futures | 2026 (submitted 10 Jul 2026; rev. 16 Jul 2026) | arXiv preprint | `arXiv:2607.09426` | Cryptocurrency markets exhibit periodic bursts in volatility and volume at one-minute, five-minute, and quarter-hour marks on **six Binance perpetual futures contracts**; trade-size roundness declines sharply during volatility bursts, indicating reduced algorithmic participation; opening returns at quarter-hour marks show out-of-sample predictability and order imbalance at openings predicts returns over 4–12 hour horizons, with substantially weaker effects at finer frequencies | **Clock mark × participation composition × volatility/volume**, and **clock mark × order imbalance × forward return.** The venue and instrument family are exactly Prometheus's | Its headline predictability claim is **directional return predictability from order imbalance**, which is the depleted §7.A lane and the substrate of `STOP_LONGHORIZON_ML_ARC`. Preprint, not peer-reviewed at the time of access. The roundness construct has no canonical operationalization (which round increments, what tolerance, what burst threshold). The sample is 2021-01-01 … 2024-10-31, overlapping but not identical to Prometheus's window |
| X12 | Kim, J.; Park, H. | Designing funding rates for perpetual futures in cryptocurrency markets | 2025 (submitted 10 Jun 2025) | arXiv preprint | `arXiv:2506.08573` | Constructs replicating portfolios for perpetual-futures issuers and introduces path-dependent funding rates via path-dependent infinite-horizon BSDEs with arbitrage pricing theory | **None applicable.** Checked specifically for a funding-design × market-state interaction claim (caps/clamps × positioning or volatility); the retrieved record asserts none | Recorded as a **negative external finding**: the most recent funding-design theory located in this phase supplies a pricing/hedging construction, not an interaction between the funding mechanism and any market-state layer. It therefore supports no interaction card |

### 5.6 Primary sources carried forward from the committed Phase 4bn-BE record

The following thirteen sources are already tabulated with full bibliographic detail, mechanism claim, and
Prometheus limitation in `2026-08-03_phase-4bn-be_external-theory-new-lane-discovery-and-admissibility-shortlist.md`
§6.1, which is committed evidence on `main`. They are relied on here at the level of the claims recorded
there, and are **not** re-verified externally in this phase:

S1 Roll (1984, JF, DOI `10.1111/j.1540-6261.1984.tb03897.x`); S2 Corwin & Schultz (2012, JF, DOI
`10.1111/j.1540-6261.2012.01729.x`); S3 Abdi & Ranaldo (2017, RFS, DOI `10.1093/rfs/hhx084`); S4 Ardia,
Guidotti & Kroencke (2024, JFE 161:103916, DOI `10.1016/j.jfineco.2024.103916`); S5 Goyenko, Holden &
Trzcinka (2009, JFE 92:153–181); S6 He, Manela, Ross & von Wachter (2024, `arXiv:2212.06888`) — Prop. 1
frictionless perpetual price and Prop. 2 bound `|F_t − [κ/(κ − (r − r'))]·S_t| ≤ C`, plus the finding that
crypto deviations comove across currencies; S7 Ackerer, Hugonnier & Jermann (2024/2026,
`arXiv:2310.11771`, NBER WP 32936, DOI `10.1111/mafi.70018`); S8 Schmeling, Schrimpf & Todorov (BIS WP
1087) — crypto carry variation attributed mainly to convenience yields from trend-chasing demand and to
limited arbitrage capital; S9 Binance official funding documentation — the published funding formula,
the **depth-derived impact-price premium index**, the ±0.05% clamp, the 8-hour settlement cadence at
00:00/08:00/16:00 UTC, and the maintenance-margin-ratio caps; S10 Lillo & Farmer (2004, SNDE 8(3)); S11
Andersen & Bondarenko (2014, JFM 17(1):1–46); S12 Clark (1973, Econometrica, DOI `10.2307/1913889`); S13
Ané & Geman (2000, JF, DOI `10.1111/0022-1082.00286`).

**Total distinct primary sources drawn on: 25** — 12 newly verified (§5.5) and 13 carried forward
(§5.6).

### 5.7 Retrieval limitations recorded honestly

Consistent with the Phase 4bn-AT §8 and Phase 4bn-BE §6.3 precedent of counting unresolved documentation
uncertainty **against** a candidate rather than resolving it by prohibited means:

- The Wiley full text of X4 (Dufour & Engle 2000) returned **HTTP 402**. Its abstract-level content was
  obtained from a repository record; the paper's full assumption set, sample, and estimation detail are
  **not verified here**, and that gap is counted against any family resting on it.
- X1, X2, X3, X5, X6, X8, X9, and X10 were **bibliographically verified** (venue, volume, pages, and the
  substantive claim as stated in publisher or repository records); full texts were not retrieved. Their
  claims are used at the level verified and no finer.
- X11 and X12 are **preprints**. X11 is used only for the venue-and-instrument-specific observation that
  its stated effects are on Binance perpetual futures; its predictability claim is not adopted.
- The Phase 4bn-BE unresolved facts remain unresolved and are **not** repaired here: the 2024 BTCUSDT
  perpetual tick size, and the 2024 maintenance-margin-ratio cap, Impact Margin Notional, and
  interest-rate parameters. The authoritative route to the first is an `exchangeInfo` call, which this
  phase is forbidden to make.
- A targeted search for peer-reviewed primary theory on a **funding × open-interest interaction specific
  to crypto perpetuals** returned only secondary and vendor material. Under §5.4 that material carries no
  substantive claim, and the absence is recorded in §19 as a genuine negative-search result rather than
  filled with a weaker source.

### 5.8 Official archive metadata and the discrepancy rule

No archive-index metadata page was fetched in this phase, and no archive object was downloaded. The
committed Phase 4at §6 and §7 matrices, which were themselves built from official Binance documentation,
are the sole basis for every data status in §8.

No conflict between current official metadata and a committed Prometheus status was observed in this
phase, because no current official metadata was consulted for that purpose. Consequently
`EXTERNAL_METADATA_DISCREPANCY__COMMITTED_STATUS_UNCHANGED` is **not invoked**. **No committed source
status is revised by this phase.**

## 6. Canonical mechanism inventory

Reconstructed from committed evidence, not assumed from the authorization's illustrative lists.

### 6.1 Phase 4as mechanism map (M-1 … M-14)

| ID | Mechanism family | Parent layer(s) | Committed status note |
|---|---|---|---|
| M-1 | Top-of-book spread | C | Suitable only as context, never a primary trigger; cost-fragility risk |
| M-2 | Top-of-book depth (best bid/ask sizes) | C | Candidate input only |
| M-3 | Order-book imbalance, top-N levels | C | Requires full local book reconstruction |
| M-4 | Depth imbalance across deeper levels | C | Only after M-3 |
| M-5 | Aggressive volume / taker buy–sell imbalance | B | Materialized in the committed 45-column feature set |
| M-6 | Trade burst / volume impulse | B | Materialized; merged into CF-1 by Phase 4bn-AW |
| M-7 | Liquidity sweep / book consumption | B×C | Requires synchronized trades + depth |
| M-8 | Book recovery / replenishment after sweep | C | Live capture only |
| M-9 | Liquidation cascade proxies | E | Bounded visibility; proxy only |
| M-10 | Funding-rate context | D | Context lens only (D1-A precedent) |
| M-11 | Open-interest context | E | Governed partial; 30-day retention |
| M-12 | Funding + OI interaction | D×E | Explicitly an interaction family |
| M-13 | Funding + OI + aggressive-flow interaction | D×E×B | Explicitly a three-way interaction family |
| M-14 | Spread / depth / flow regime interaction | C×B | Explicitly an interaction family; flagged for G1 rejection-topology distance |

**M-12, M-13, and M-14 are already interaction families in the committed record.** Any atlas entry that
re-proposes them is duplicative unless it names a structural distinction; §12 records the mapping.

### 6.2 Candidate families and results downstream of Phase 4as

| ID | Family | Status on `main` |
|---|---|---|
| CF-1 | Microstructure realized-volatility (magnitude) forecasting from aggTrades | Selected, executed, `CF1_VALID_PASS` (development-level); continuation **rejected** (`REJECT_CF1_FILTER_CONTINUATION__REMAIN_PAUSED`); run consumed, no rerun |
| CF-2 | Cross-symbol return lead–lag / information transmission (temporal) | Shortlisted, **never selected**; `BLOCKING` on multi-symbol aggTrades acquisition |
| CF-3 | Derivatives-context + settlement/session-timing volatility-regime conditioning | Shortlisted, **never selected**; explicitly not bundled with CF-1 |
| NL-C1 | Price-only effective-spread estimation for the admissible substrate | Surviving for independent review only; unselected, unranked, un-cleared, unauthorized |
| NL-C2 | Perpetual-futures funding mechanism as a no-arbitrage friction bound | Surviving for independent review only; unselected, unranked, un-cleared, unauthorized |
| D1-A | Funding-aware contrarian | Retained verdict: MECHANISM PASS / FRAMEWORK FAIL — other |
| — | Forced-flow / liquidation-cascade proxy family | `REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH` |
| — | Long-horizon aggTrades directional ML arc | `STOP_LONGHORIZON_ML_ARC` |
| — | Top-of-book bounce-decomposition arc | `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE` |
| N-01 … N-16 | Phase 4bn-BE negative-search families | All rejected with named grounds |

### 6.3 Retained strategy verdicts and cooled-down families

Retained verdicts: **H0** framework anchor; **R3** baseline-of-record; **R1a** and **R1b-narrow** retained
non-leading; **R2** failed §11.6; **F1** hard reject; **D1-A** mechanism pass / framework fail; **5m
thread** operationally closed; **V2**, **G1**, **C1** hard reject.

Cooled-down families (M0 §7): **§7.A** price-only single-symbol directional continuation, DEPLETED;
**§7.B** cross-sectional trend / relative-strength symbol selection, COOLED_DOWN after `NOT_SUPPORTED`,
with symbol-universe expansion explicitly blocked; **§7.C** derivatives-context directional lane,
`CONDITIONAL_ONLY / HIGH_D1-A_RESCUE_RISK`; **§7.D** microstructure / order-flow / liquidity-timing lane,
`NOT_RECOMMENDED_NOW`; **§7.E** mark-price stop-domain / execution-realism lane, `NOT_RECOMMENDED_NOW`.

### 6.4 Layer G — methods, recorded separately as methods and not mechanisms

Linear models; tree models; deep sequence models; foundation models; tokenizers; synthetic generators;
representation learning; meta-labelling; event classifiers; regime classifiers; feature-importance
ranking; anomaly detection.

**A method may test a mechanism. It may not qualify as a mechanism merely because it combines several
inputs.** No layer-G item appears as a leg of any interaction in this atlas, and no card is admitted on
the ground that a model could consume both modalities. Phase 4as §12 records that no ML model or AI
trading agent is authorized; that is unchanged.

## 7. Canonical data inventory

Reconstructed from the committed Phase 4at §6/§7 matrices, the Phase 4bn-AW §11 inventory, the Phase
4bn-AV evidence ledger, and the committed feature schema. **No local data was inspected to build this.**

**Layer A — price geometry and magnitude.** Klines (OHLCV) for BTCUSDT, ETHUSDT and the Phase 4ac core
set (ADA, SOL, XRP) at multiple intervals, already on disk (Phase 2 `v002` + Phase 4i `__v001`).
Last-trade prices derivable descriptively from BTCUSDT aggTrades. Realized-variance objects derivable from
either. Mark-price, premium-index, and index-price klines are archive-available but unacquired.

**Layer B — executed trade activity.** BTCUSDT USDⓈ-M aggTrades, pre-v002 segment, normalized / feature /
label built. The committed feature substrate materializes, per trailing window {1s, 5s, 15s, 60s}:
`rolling_aggtrade_count`, `rolling_quantity_sum`, `rolling_quantity_mean`,
`rolling_aggressive_buy_quantity`, `rolling_aggressive_sell_quantity`, `rolling_aggressive_buy_count`,
`rolling_aggressive_sell_count`, `rolling_aggressive_flow_ratio`,
`rolling_aggressive_quantity_imbalance`, `rolling_log_return_past_window` — forty columns, plus
`utc_hour`, `utc_minute`, `milliseconds_since_day_start`, `invalid_window_flag`,
`rolling_missing_window_flag`. Raw trades and multi-symbol aggTrades are archive-available but
unacquired. The taker buy/sell volume ratio endpoint is 30-day-retained.

**Layer C — liquidity and order-book state.** bookTicker, partial depth, diff depth, and REST depth
snapshots. **None has a Binance public historical archive at the required granularity for derivatives.**
`HIST_TOB_BOOKTICKER_SOURCE` is `INADMISSIBLE_OR_UNAVAILABLE` in the committed ledger for the 2024
mechanism question. Prospective capture is regime-non-comparable to the 2024 substrate.

**Layer D — perpetual anchoring and contract state.** Funding-rate history (`funding__v001`) on disk for
BTCUSDT, ETHUSDT, and the Phase 4ac core set; admissible as a **context lens only** under the D1-A
precedent. Premium-index, index-price, and mark-price klines archive-available, unacquired (mark-price
additionally governed by Phase 3r §8). Contract parameters — 2024 cap, Impact Margin Notional, interest
term, tick size — not established from Tier-1 static documentation.

**Layer E — positioning and forced-flow state.** Open interest current (snapshot only); open-interest
historical statistics, top-trader long/short account and position ratios, and global long/short account
ratio (all 30-day retention); `forceOrder` liquidations (WS live capture only, largest-per-1000 ms
snapshot, **no public archive**); REST `forceOrders` (authenticated user-scope, **not admissible for
market research**). The committed feature schema independently bars `liquidation`, `open_interest`, and
`funding` as feature-column tokens.

**Layer F — cross-market and contextual state.** Multi-symbol klines on disk for the five core symbols;
multi-symbol aggTrades archive-available but unacquired; the composite index price (a cross-venue spot
composite) available only as unacquired index-price klines; deterministic UTC calendar, session, weekend,
and funding-settlement timing, which require **no data at all**; market-wide funding dispersion
computable from the on-disk five-symbol funding history.

**Layer G — methods.** Not data. Recorded in §6.4.

## 8. Data-status table

Status vocabulary is exactly the eight values the authorization permits. Every value is derived from
committed records, committed schemas, and official documentation already recorded in the committed
Prometheus corpus. **No local data was inspected to determine any status.**

| Data family | Layer | Venue | Instrument scope | Historical window | Fields | Timestamp resolution | Causal-alignment capability | Repository presence per committed records | Acquisition required | Reserve implicated | Source report | Unresolved provenance issue |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT aggTrades, pre-v002 development segment | B (and A via prices) | Binance USDⓈ-M | BTCUSDT | 244 non-reserve dates 2024-03-01 … 2024-10-31 excl. 2024-10-01 | price, quantity, aggressor flag, `transaction_time`, agg-trade id | millisecond | Full — `P_at(u)` boundary operator, embargo and purge policies committed | `AVAILABLE_NON_RESERVE` — normalized / feature / label built | No | No | 4at §6.1; 4bn-AW §11; 4bn-AB | Insurance-fund and ADL trades not aggregated; `nq` RPI field post-dates the window |
| BTCUSDT aggTrades, pre-v002 internal holdout | B | Binance USDⓈ-M | BTCUSDT | 2024-11-17 … 2024-11-30, 14 dates | as above | millisecond | Full | `AVAILABLE_BUT_CONSUMED_FOR_CONFIRMATION` | No | Yes — consumed, terminal | Ledger §5.1 | May never again be represented as independent confirmation |
| v002 terminal window | A, B | Binance USDⓈ-M | BTCUSDT | 2024-12-01 … 2025-02-28, 90 dates | raw / normalized / feature / label | millisecond | Full | `UNTOUCHED_RESERVED` | No | **Yes** | Ledger §5.2 | None; status has never changed |
| v002 sealed test | A, B | Binance USDⓈ-M | BTCUSDT | 2025-02-14 … 2025-02-28, 15 dates | TEST split | millisecond | Full | `UNTOUCHED_RESERVED` (highest protection; `test_rows_loaded = 0`) | No | **Yes** | Ledger §5.3 | None; single-use, creates no replacement |
| Klines (OHLCV), core symbol set | A, F | Binance USDⓈ-M | BTCUSDT, ETHUSDT, ADA, SOL, XRP | Multi-interval, Phase 2 `v002` + Phase 4i `__v001`; Phase 4ad Rule B1 common start `2022-04-03` for SOL/XRP | open, high, low, close, volume, `open_time` | bar `open_time` | Full at bar granularity; sub-bar order lost | `AVAILABLE_NON_RESERVE` | No | No | 4at §6.3; 4bn-AW §11 | Phase 4ad Rule B early-2022 gap scope |
| Raw trades | B | Binance USDⓈ-M | per-symbol | Archive since launch | id, price, qty, time | millisecond | Full | `ARCHIVE_AVAILABLE_NOT_ACQUIRED` | Yes | No | 4at §6.2 | None material |
| Multi-symbol aggTrades (non-BTCUSDT) | B, F | Binance USDⓈ-M | ETHUSDT and others | Archive since launch | as aggTrades | millisecond | Full if acquired | `ARCHIVE_AVAILABLE_NOT_ACQUIRED` | Yes | No | 4bn-AW §11 | None material |
| Funding-rate history | D | Binance USDⓈ-M | BTCUSDT, ETHUSDT, core set | On disk `funding__v001`; REST history available | `fundingTime`, funding rate | 8-hour settlement, 00:00/08:00/16:00 UTC | Full — each value attributable to its own interval | `AVAILABLE_NON_RESERVE` (context lens only, D1-A precedent) | No | No | 4at §6.7; 4bn-AW §11 | 2024 cap / IMN / interest-term values not established from Tier-1 static pages |
| Premium-index klines | D | Binance USDⓈ-M | per-symbol | Archive since launch | OHLC of premium, `open_time` | bar | Full if acquired | `ARCHIVE_AVAILABLE_NOT_ACQUIRED` | Yes | No | 4at §6.5 | Derived quantity; inherits upstream gap pattern |
| Index-price klines | A, D, F | Binance USDⓈ-M | per-pair | Archive since launch | OHLC of composite index, `open_time` | bar | Full if acquired | `ARCHIVE_AVAILABLE_NOT_ACQUIRED` | Yes | No | 4at §6.6 | Composite across spot venues; not a per-venue tape |
| Mark-price klines | A, D | Binance USDⓈ-M | per-symbol | Archive since launch | OHLC of mark, `open_time` | bar | Full if acquired | `ARCHIVE_AVAILABLE_NOT_ACQUIRED` + governed by Phase 3r §8 | Yes | No | 4at §6.4 | Known upstream invalid windows 2022-07-30/31, 2022-10-02, 2023-02-24, 2023-11-10 |
| Funding-info / contract parameters | D | Binance USDⓈ-M | contract-level | Snapshot only | funding interval, cap parameters | snapshot | None historically | `UNKNOWN__DOCUMENTATION_REQUIRED` for 2024 values | Yes (or Tier-1 documentation) | No | 4at §6.8; 4bn-BE §6.3 | The 2024 cap, IMN, and interest-term history is the specific unresolved fact |
| Open interest (current) | E | Binance USDⓈ-M | per-symbol | Snapshot only | OI | snapshot | None historically | `PROSPECTIVE_ONLY` | Yes (forward polling) | No | 4at §6.9 | No WebSocket stream for current OI |
| Open-interest historical statistics | E | Binance USDⓈ-M | per-symbol | **Latest 30 days only** | OI per period bucket | 5m … 1d buckets | Would be full within retention; **zero coverage of a 2024 window** | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` for the study window (endpoint-side status `PARTIAL_OR_WINDOW_INSUFFICIENT`) | Yes, and cannot be back-filled | No | 4at §6.10; 4bn-AW §11 | Phase 4j §11 OI-subset governance applies to the pre-existing Phase 4i partial series |
| Top-trader long/short account and position ratios; global long/short account ratio | E | Binance USDⓈ-M | per-symbol | Latest 30 days | ratio per bucket | bucket | Zero coverage of 2024 | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` for the study window | Yes, and cannot be back-filled | No | 4at §6.11–§6.13 | Context-only precedent (D1-A) |
| Taker buy/sell volume ratio | B | Binance USDⓈ-M | per-symbol | Latest 30 days | ratio per bucket | bucket | Zero coverage of 2024 | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` for the study window | Yes | No | 4at §6.14 | aggTrades is the more granular admissible alternative |
| Liquidation / `forceOrder` | E | Binance USDⓈ-M | per-symbol or all-market | **No public archive** | order price, qty, time | ≤ 1 push / s / symbol, largest only | None retrospectively | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE`; forward form `PROSPECTIVE_ONLY` and proxy-bounded | Not obtainable historically | No | 4at §6.15; 4as §9.5 | Deliberately attenuated visibility; REST form is authenticated user-scope and inadmissible |
| Book ticker (best bid/ask) | C | Binance USDⓈ-M | per-symbol | **No public archive** | best bid/ask price and size, `u`, `E`, `T` | event-time | None retrospectively | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` — ledger `HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE` | Not obtainable historically | No | 4at §6.16; ledger §6.1; 4bn-AT | Third-party retrospective source is Tier-1-undocumented, carries an unremediated out-of-order defect, reportedly ceased in 2024, coverage unconfirmed |
| Partial book depth | C | Binance USDⓈ-M | per-symbol | **No public archive** | top-N levels | 100/250/500 ms | None retrospectively | `PROSPECTIVE_ONLY` | Not obtainable historically | No | 4at §6.17 | RPI orders excluded |
| Diff book depth + REST depth snapshot | C | Binance USDⓈ-M | per-symbol | **No public archive** | diffs with `U`/`u`/`pu`; snapshot `lastUpdateId` | 100/250/500 ms | None retrospectively | `PROSPECTIVE_ONLY` | Not obtainable historically | No | 4at §6.18–§6.19 | State must be reconstructed; gaps require resync |
| Mark-price stream; index-price stream | A, D, F | Binance USDⓈ-M | per-symbol / per-pair | Sub-bar live only | mark / index events | event-time | None retrospectively at sub-bar | `PROSPECTIVE_ONLY` (bar-level via klines is `ARCHIVE_AVAILABLE_NOT_ACQUIRED`) | Yes | No | 4at §6.20–§6.21 | Phase 3r §8 / Phase 3v §8 governance |
| Deterministic UTC calendar, session, weekend, funding-settlement clock | F | n/a | n/a | Unbounded | derived from timestamps | as the paired series | Full | `AVAILABLE_NON_RESERVE` — **requires no data acquisition at all** | No | No | 4bn-AW §22 (CF-3 calendar leg) | None |
| Cross-venue / spot / other-exchange data | F | non-Binance | n/a | n/a | n/a | n/a | n/a | Out of committed scope; no admissibility record exists | Yes, and would require a new source-admissibility decision | No | 4as §6 caveats | Never assessed; not proposed here |

## 9. Complete parent-layer interaction matrix

All fifteen unordered parent pairs receive a disposition. Empty and rejected pairs are **not** omitted.
The pair-level disposition is the disposition of the pair's least-blocked family; per-family dispositions
are in §10.

| Pair | Layers | Families enumerated | Binding structural fact | Pair disposition |
|---|---|---|---|---|
| A×B | price geometry × executed trade activity | 2 | Both legs admissible; the interaction is exactly CF-1's mechanism and target on CF-1's substrate | `DUPLICATIVE_OR_ALREADY_DEPLETED` |
| A×C | price geometry × liquidity state | 3 | Layer C has no admissible history; the surviving price-only route is NL-C1 plus a context variable | `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED` |
| A×D | price geometry × perpetual anchoring | 3 | The basis/premium leg requires unacquired premium- or index-price klines; the funding-only route reopens NL-C2 | `ARCHIVE_AVAILABLE_NOT_ACQUIRED__NO_ACQUISITION_AUTHORIZED` |
| A×E | price geometry × positioning / forced flow | 2 | Layer E has no admissible 2024 history; the theory-canonical moderator is open interest | `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED` |
| A×F | price geometry × cross-market and context | 3 | Multi-symbol klines are on disk, so the cross-symbol volatility family is computable; nothing legitimate consumes it | `DATA_AVAILABLE_BUT_NO_DECISION_CONSUMER` |
| B×C | executed flow × liquidity state | 4 | The canonical microstructure interaction (impact slope inversely proportional to depth) has an entirely inadmissible moderator | `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED` |
| B×D | trade activity × perpetual anchoring | 3 | The admissible funding form is CF-3's family; the premium form requires acquisition | `DUPLICATIVE_OR_ALREADY_DEPLETED` |
| B×E | trade activity × positioning | 2 | Bessembinder–Seguin's volume × open-interest interaction is exact and canonical, and open interest is historically unavailable | `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED` |
| B×F | trade activity × cross-market and context | 3 | The commonality form requires unacquired multi-symbol aggTrades; the admissible clock forms have no legitimate consumer | `ARCHIVE_AVAILABLE_NOT_ACQUIRED__NO_ACQUISITION_AUTHORIZED` |
| C×D | liquidity state × perpetual anchoring | 2 | The premium index is depth-derived by official identity, but the inversion from a clamped 8-hour scalar to a book state is many-to-one | `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED` |
| C×E | liquidity state × positioning / forced flow | 2 | Brunnermeier–Pedersen liquidity spirals require **both** inadmissible layers simultaneously | `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED` |
| C×F | liquidity state × cross-market and context | 2 | Commonality in liquidity and intraday liquidity periodicity both need a liquidity series | `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED` |
| D×E | perpetual anchoring × positioning | 3 | M-12 exactly; funding is on disk and open interest is not | `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED` |
| D×F | perpetual anchoring × cross-market and context | 3 | Both legs of the cross-symbol funding family are admissible; it is a symbol-universe expansion of an unselected candidate in the highest-flagged rescue lane | `HIGH_RESCUE_RISK__DOES_NOT_SURVIVE` |
| E×F | positioning × cross-market and context | 2 | Both legs require positioning data that does not exist historically | `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED` |

**The matrix's central structural finding.** In every theory-supported cross-lane interaction located in
this phase, the *moderating* leg — the state that changes the consequence of the other mechanism — sits in
**layer C (liquidity / order-book state)** or **layer E (positioning / forced-flow state)**. Those are
precisely the two layers with no admissible Prometheus history: layer C has no Binance public archive at
derivatives granularity, and layer E is 30-day-retained or has no archive at all. The layers Prometheus
*can* observe — A, B, D-funding, and F-calendar — are the *moderated* legs, and every admissible pairing
among them is already occupied by CF-1, CF-2, CF-3, NL-C1, NL-C2, D1-A, or a cooled-down lane.

This is not a scarcity of ideas. It is a structural property of the project's data topology, and it is
the reason the shortlist in §20 is empty.

## 10. Two-way interaction cards

Thirty-nine materially distinct two-way families. Each card carries every field required by §19 of the
authorization: **A** identity, **B** mechanism interaction, **C** observable implication, **D** data
requirements, **E** identification (four separate classifications), **F** prior-work distance, **G**
decision consequence, **H** researcher freedom, **I** evidence posture, **J** cost and proportionality,
**K** strongest case against proceeding, **L** disposition.

The four identification classifications are never collapsed:

```text
COMPUTABLE                — can the quantity be produced at all from admissible data
IDENTIFIED                — does the quantity isolate the claimed mechanism
SCIENTIFICALLY_INFORMATIVE — would either outcome teach the project something true
DECISION_RELEVANT         — would either outcome change a legitimate current project decision
```

---

### Pair A×B — price geometry and magnitude × executed trade activity

#### I-AB-1 — Activity intensity as the directing process for price variability

**A. Identity.** `I-AB-1`; A×B; mixture-of-distributions / trade-time subordination. *Does the intensity
of executed trade activity change the magnitude consequence of the price process, beyond what past price
magnitude already implies?*

**B. Mechanism interaction.** Mechanism A: information arrival drives a stochastic clock (S12, S13).
Mechanism B: return magnitude accumulates in that clock rather than in calendar time. Joint claim: the
variance consequence of an interval depends on how many trades filled it, so activity is not a covariate
but the interval's own measure. Neither leg alone identifies this — past variance alone is calendar-timed;
trade counts alone predict nothing about magnitude without the variance object. External source: S12
(Clark 1973), S13 (Ané & Geman 2000), X3 (Bessembinder & Seguin 1993, expected/unexpected decomposition).

**C. Observable implication.** Realized variance over an interval conditioned on contemporaneous or
lagged trade-arrival intensity; predicted to exceed what an activity-blind variance model implies.
Competing explanations: volatility clustering alone; intraday periodicity (X10); a common latent driver.
Contemporaneous **and** predictive forms both exist. The question is forecasting in the predictive form
and structural in the contemporaneous form.

**D. Data requirements.** Layer B: `rolling_aggtrade_count_{w}`, `rolling_quantity_sum_{w}` — committed
columns. Layer A: realized variance from the same rows. Millisecond `transaction_time`; BTCUSDT USDⓈ-M;
244-date non-reserve window. Alignment: causal snapshot at origin, `P_at(u)` boundary operator.
Status `AVAILABLE_NON_RESERVE`. No acquisition. No reserve. No provenance uncertainty.

**E. Identification.** `COMPUTABLE` yes. `IDENTIFIED` partially — activity and variance share a latent
driver and the subordination claim is a representation, not a separation. `SCIENTIFICALLY_INFORMATIVE`
no new information: the project has already run it. `DECISION_RELEVANT` no.

**F. Prior-work distance.** Nearest Prometheus family: **CF-1**, whose corrected feature set is
*literally* `{rolling_aggtrade_count_60s, rolling_quantity_sum_60s}` and whose target is one-hour realized
variance. Nearest stopped arc: none directly. Nearest rescue trap: the CF-1 filter continuation, already
rejected. Structural distinction: **none available.** The distinction would have to be the clock
convention, and M0 §6 names interval changes as a forbidden post-null tweak; Phase 4bn-BE already rejected
the clock formulation as N-02.

**G. Decision consequence.** Pass: nothing changes — the result exists. Fail: contradicts a merged result,
which this phase has no authority to do and which no rerun could establish (the run is consumed).
Invalid: n/a. Legitimate current consumer: **none**. Self-created: yes, in the sense that the only
remaining question is one the project already answered.

**H. Researcher freedom.** Forced: the CF-1 contract froze target, baseline, loss, horizon, and cadence.
Free: everything else, and re-choosing any of it is post-hoc by construction because the author has read
the result. Contamination from known outcomes: **maximal** — `Δ_equal`, `ρ`, `LB_95`, and the seven `D_i`
are public on `main`. Clean preregistration: **not possible**.

**I. Evidence posture.** Non-reserve feasible; but the single evidence-bearing run is consumed and no
rerun is authorized. Acquisition pressure none. Reserve pressure would be immediate and illegitimate (a
"confirm on the terminal window" argument). Development-only: moot.

**J. Cost and proportionality.** Documentation moderate; acquisition none; engineering low; validation
high; governance high (it would relitigate a merged decision). Scientific information gain **zero**.
Decision-relevant gain **zero**.

**K. Strongest case against proceeding.** It is CF-1. Not adjacent to CF-1, not a variant of CF-1 — the
same mechanism, the same target family, and the same two committed feature columns. Phase 4bn-BC already
declined the strictly weaker continuation of it on decision-consequence and anti-duplication grounds; a
straight re-expression is a fortiori worse.

**L. Disposition.** `DUPLICATIVE_OR_ALREADY_DEPLETED`

#### I-AB-2 — Trade-size composition as a moderator of the activity–volatility relation

**A. Identity.** `I-AB-2`; A×B; participant-composition conditioning of volume–volatility. *Does the
composition of executed trade sizes change what a burst of activity implies for realized magnitude?*

**B. Mechanism interaction.** Mechanism A: algorithmic participants place size on round increments;
their withdrawal changes the size distribution (X11). Mechanism B: activity bursts accompany magnitude
bursts. Joint claim: a burst composed of algorithmic flow and a burst composed of discretionary flow have
different magnitude consequences, so composition moderates the activity–volatility link. Neither leg
alone identifies it: size distribution alone says nothing about magnitude; activity alone cannot separate
participant type. External source: X11 (Kim & Hansen 2026), with X2 (Admati & Pfleiderer 1988) supplying
the theoretical reason composition should vary systematically.

**C. Observable implication.** Trade-size roundness computed from the aggTrades quantity field, and its
covariation with realized magnitude within activity bursts. Competing explanations: exchange lot-size and
tick constraints; a mechanical relation between size and count under a fixed notional; the same latent
information driver. Contemporaneous. Structural / descriptive.

**D. Data requirements.** Layer B: raw `quantity` per aggregate trade. Layer A: realized variance.
Millisecond `transaction_time`; BTCUSDT; 244-date non-reserve window. `AVAILABLE_NON_RESERVE`. No
acquisition, no reserve. Provenance uncertainty: insurance-fund and ADL trades are not aggregated, and
their size profile is unknown, which directly contaminates a roundness statistic.

**E. Identification.** `COMPUTABLE` yes. `IDENTIFIED` weak — roundness is an inference about participant
type from a size histogram, with no venue-published mapping. `SCIENTIFICALLY_INFORMATIVE` marginally.
`DECISION_RELEVANT` **no**.

**F. Prior-work distance.** Nearest Prometheus family: CF-1 (magnitude family; AW candidate #11 trade-burst
merged into it). Nearest stopped arc: `STOP_LONGHORIZON_ML_ARC`, reached through X11's companion
directional claim. Nearest rescue trap: the same. Structural distinction: roundness is genuinely not a
committed feature column. Reason the distinction may fail: the outcome variable is still realized
magnitude on the CF-1 substrate, and the only thing added is a new descriptor of the same rows.

**G. Decision consequence.** Pass: the project would know that its substrate carries clock-periodic
algorithmic participation. The only route from there to a project decision is a **reinterpretation of
CF-1's features**, which §17 of the authorization names as a forbidden consumer. Fail: closes a question
this candidate invented. Invalid: recorded, question stays open. Legitimate current consumer: **none**.
Self-created: **yes, explicitly**.

**H. Researcher freedom.** Forced by theory: nothing. Free: which round increments count, what tolerance,
what window, what burst threshold, what magnitude estimator. Contamination: the author knows CF-1 used
60-second count and quantity-sum windows. Clean preregistration: possible in form, but the frozen choices
would be **frozen arbitrariness**, not principle — X11 supplies one operationalization and no canonical
one.

**I. Evidence posture.** Non-reserve feasible. No acquisition pressure. Reserve pressure low. Result
could remain development-only, and would have to.

**J. Cost and proportionality.** Documentation moderate; acquisition none; engineering low-moderate;
validation moderate; governance moderate. Scientific gain low. Decision-relevant gain **zero**.

**K. Strongest case against proceeding.** Its pass changes nothing the project is allowed to act on, and
its fail closes a question nobody asked. The one route by which it could matter — revising how CF-1's
activity features are read — is a prohibited consumer, and pursuing it would put the project in the
position of having built an instrument whose only use is forbidden.

**L. Disposition.** `REJECTED_ABSENT_DECISION_CONSEQUENCE`

---

### Pair A×C — price geometry and magnitude × liquidity and order-book state

#### I-AC-1 — Volatility state as a moderator of quoted liquidity

**A. Identity.** `I-AC-1`; A×C; adverse-selection widening. *Does the volatility state change the quoted
spread and displayed depth that market makers post?*

**B. Mechanism interaction.** Mechanism A: return volatility raises inventory and adverse-selection risk.
Mechanism B: quote setting balances that risk against order flow (X1). Joint claim: the spread and depth
consequence of a given flow environment is conditioned on volatility. Neither leg alone: volatility alone
does not price liquidity; a spread series alone cannot attribute widening to volatility rather than to
flow toxicity. External source: X1 (Kyle 1985) for the depth/λ object; M-1 in the committed map.

**C. Observable implication.** Quoted spread and best-side sizes conditioned on contemporaneous realized
volatility. Competing explanations: order-flow toxicity independent of volatility; scheduled events;
exchange fee-tier changes. Contemporaneous. Structural.

**D. Data requirements.** Layer C: best bid, best ask, and their sizes, at event time with monotone
update ids. Layer A: realized volatility. Binance USDⓈ-M; BTCUSDT; the 2024 window. Alignment would
require quote-to-bar alignment at millisecond resolution. **Status `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE`.**
Acquisition cannot supply the historical leg; prospective capture is regime-non-comparable. No reserve
implicated because the question never reaches evidence.

**E. Identification.** `COMPUTABLE` **no** — the moderated quantity does not exist for the window.
`IDENTIFIED` would be strong if it did. `SCIENTIFICALLY_INFORMATIVE` yes in principle. `DECISION_RELEVANT`
moderate in principle — it bears on M0.5 cost realism.

**F. Prior-work distance.** Nearest Prometheus family: M-1 / M-2. Nearest stopped arc:
`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`, which is the *same* data blocker. Nearest rescue trap: NL-C1,
which reaches spread without quotes. Structural distinction from the stopped arc: the stopped arc asked a
pointwise decomposition question; this asks a conditional-level question. Reason the distinction may fail:
it is irrelevant — both die on the same missing source.

**G. Decision consequence.** Pass and fail are both unreachable. Legitimate current consumer: would have
been the cost-realism record. Self-created: no.

**H. Researcher freedom.** Moot. If the data existed, the volatility estimator and conditioning bins would
be free and unanchored.

**I. Evidence posture.** No non-reserve path. Acquisition pressure **high and illegitimate** — this is
exactly the family that would generate pressure to acquire a Tier-1-undocumented third-party quote
archive. Reserve pressure none.

**J. Cost and proportionality.** Acquisition cost prohibitive and the acquired object would not answer
the 2024 question. Everything else moot.

**K. Strongest case against proceeding.** The moderator does not exist in any admissible form, and the
project has already spent a full phase (4bn-AT) establishing that. Re-proposing it under a conditional
framing does not create data.

**L. Disposition.** `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED`

#### I-AC-2 — Volatility-regime conditioning of price-only spread estimators

**A. Identity.** `I-AC-2`; A×C; estimator-validity conditioning. *Does the volatility state change the
agreement among price-only effective-spread estimators?*

**B. Mechanism interaction.** Mechanism A: the bid–ask bounce leaves a covariance and range signature
(S1–S4). Mechanism B: the estimators' identifying assumption is a constant spread and a random-walk
efficient price over the window, both of which degrade with volatility. Joint claim: estimator
disagreement is conditioned on volatility. External source: S1, S2, S3, S4, with S5 supplying the
validation methodology Prometheus cannot reproduce.

**C. Observable implication.** Cross-estimator disagreement measured within volatility strata.
Competing explanations: the volatility stratification mechanically alters the range decomposition;
tick-binding in calm regimes. Contemporaneous. Structural.

**D. Data requirements.** Layer A and the price face of layer B: OHLC bars or last-trade prices from
klines or aggTrades. `AVAILABLE_NON_RESERVE`. No acquisition, no reserve. Provenance uncertainty: the
2024 tick size remains unestablished (§5.7).

**E. Identification.** `COMPUTABLE` yes. `IDENTIFIED` **no** — there is no admissible quoted-spread ground
truth, so estimator agreement within a stratum cannot be distinguished from shared-assumption agreement.
`SCIENTIFICALLY_INFORMATIVE` marginal. `DECISION_RELEVANT` no.

**F. Prior-work distance.** Nearest Prometheus family: **NL-C1**, of which this is NL-C1 plus a
conditioning variable. Nearest stopped arc: `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`, whose mechanism is
the bounce. Nearest rescue trap: NL-C1 itself. Structural distinction: **none that survives §15** — a
context variable does not create a new mechanism by conditioning an old result, and the authorization
forbids treating interaction with another data family as sufficient to rescue an unselected candidate.

**G. Decision consequence.** Pass would be read as strengthening NL-C1, which is exactly the silent
reopening the authorization prohibits. Fail would be read as weakening it, which is a judgement reserved
to an independent review that has not happened. Legitimate current consumer: **none**. Self-created:
partly.

**H. Researcher freedom.** Forced: the estimator closed forms. Free: bar frequency, stratification
boundaries, agreement tolerance, estimator subset. Contamination: the author knows NL-C1's card, its
`ADVERSE` M0.8 label, and the locked 8 bps reference.

**I. Evidence posture.** Non-reserve feasible; acquisition none; reserve pressure low.

**J. Cost and proportionality.** Low engineering, moderate documentation, **high governance** because the
phase would have to argue it is not reopening NL-C1. Scientific gain low; decision gain zero.

**K. Strongest case against proceeding.** It is a rescue vehicle in the precise shape the authorization
warns about: an unselected candidate, re-entered through the side door of a second data family, in a
neighbourhood the project has already stopped once.

**L. Disposition.** `HIGH_RESCUE_RISK__DOES_NOT_SURVIVE`

#### I-AC-3 — Microstructure-noise variance across sampling frequencies

**A. Identity.** `I-AC-3`; A×C; volatility-signature / noise-variance diagnostic. *Does the sampling
frequency change the measured variance in the way a bid–ask-noise model requires?*

**B. Mechanism interaction.** Mechanism A: the efficient price accumulates variance linearly in time.
Mechanism B: microstructure noise adds a frequency-dependent component. Joint claim: the frequency
dependence identifies the noise magnitude. External sources named without verification in the committed
Phase 4bn-BE §6.2 list; no substantive claim rests on them here.

**C. Observable implication.** The volatility signature plot over sampling frequencies. Competing
explanations: genuine multi-scale volatility; jump contamination. Contemporaneous. Descriptive.

**D. Data requirements.** BTCUSDT aggTrades prices; `AVAILABLE_NON_RESERVE`; no acquisition; no reserve.

**E. Identification.** `COMPUTABLE` yes. `IDENTIFIED` weak. `SCIENTIFICALLY_INFORMATIVE` no.
`DECISION_RELEVANT` no.

**F. Prior-work distance.** Nearest Prometheus family: **AW candidate #13**, "intraday variance-ratio /
microstructure-noise diagnostic on aggTrades", a committed `REJECT` on the grounds that it is a
measurement diagnostic rather than a family and is rescue-adjacent to the stopped ToB bounce question;
re-recorded as Phase 4bn-BE **N-05**. Structural distinction: none.

**G. Decision consequence.** Pass and fail both change nothing. Legitimate current consumer: none.
Self-created: yes.

**H. Researcher freedom.** Frequency grid and estimator entirely free.

**I. Evidence posture.** Non-reserve feasible; irrelevant.

**J. Cost and proportionality.** Low cost, zero gain.

**K. Strongest case against proceeding.** It is a re-proposal of a candidate the project rejected twice,
on both occasions for reasons that this framing does not touch.

**L. Disposition.** `DUPLICATIVE_OR_ALREADY_DEPLETED`

---

### Pair A×D — price geometry and magnitude × perpetual anchoring and contract state

#### I-AD-1 — Volatility state as a moderator of the no-arbitrage band width

**A. Identity.** `I-AD-1`; A×D; limits-to-arbitrage band conditioning. *Does the volatility state change
the width of the band within which the perpetual's premium over its index wanders without provoking
arbitrage?*

**B. Mechanism interaction.** Mechanism A: with round-trip cost `C`, the perpetual price is pinned to the
frictionless no-arbitrage value only within `±C` (S6 Prop. 2). Mechanism B: volatility raises the
arbitrageur's margin requirement and inventory risk, so the effective `C` is state-dependent (X8; X7).
Joint claim: the observed band is not a constant — its width is conditioned on the volatility and
margin state, and the joint reading separates a cost-like component from a risk-like component that
neither leg identifies alone. External sources: S6, S7, S8, X7, X8.

**C. Observable implication.** The premium series' excursion magnitude conditioned on realized
volatility, predicted to widen with volatility. Competing explanations, at full strength: S8 attributes
crypto basis variation **mainly to convenience yields from trend-chasing demand and to limited arbitrage
capital**, both of which also covary with volatility, so a widening band does not isolate cost.
Contemporaneous. Structural.

**D. Data requirements.** Layer D: premium-index klines, or index-price klines plus the perpetual's own
price. Layer A: realized volatility from on-disk klines or aggTrades. Binance USDⓈ-M; BTCUSDT; bar
`open_time`; the 2024 window. **Status of the load-bearing leg: `ARCHIVE_AVAILABLE_NOT_ACQUIRED`.**
Acquisition required and **not authorized**. No reserve implicated. Provenance uncertainty: derived
quantity inheriting upstream gap patterns; Phase 3r §8 governance would apply to any mark-price route.

**E. Identification.** `COMPUTABLE` **no**, on currently held data. `IDENTIFIED` weak even if acquired —
S8's confound is not separable. `SCIENTIFICALLY_INFORMATIVE` moderate. `DECISION_RELEVANT` low; it cannot
discharge M0.5 and cannot revise the locked reference (Phase 4bn-AT §58).

**F. Prior-work distance.** Nearest Prometheus family: **NL-C2's extended form**, which the Phase 4bn-BE
card already names as requiring premium- or index-price klines and already labels blocking. Nearest
stopped arc: none. Nearest rescue trap: D1-A, via any directional reading of a basis. Structural
distinction from NL-C2: conditioning on volatility is a context variable, so **the distinction fails
under §15**.

**G. Decision consequence.** Pass: would add a conditional friction-band statement, prospectively only,
authorizing nothing. Fail: would close a question that NL-C2's own extended form already frames.
Invalid: recorded. Legitimate current consumer: at most "decide whether a documented acquisition question
deserves later operator review" — and this atlas records that question in §18 **without** needing the
experiment. Self-created: partly.

**H. Researcher freedom.** Forced: the frictionless price and the Prop. 2 bound. Free: volatility
estimator, conditioning bins, band summary statistic, window. Contamination: the author knows the locked
8/16 bps reference and the NL-C2 card.

**I. Evidence posture.** No non-reserve path without acquisition. Acquisition pressure **material and
recorded**. Reserve pressure low. Development-only: yes.

**J. Cost and proportionality.** Acquisition cost material; documentation high; engineering low;
validation moderate; governance high (§7.C rescue lane). Gain moderate on the scientific axis, low on the
decision axis.

**K. Strongest case against proceeding.** It requires an unauthorized acquisition to obtain a quantity
that the strongest available source says measures mainly something other than what the project would want
it to measure — and the framing that makes it look new is a context variable bolted onto an unselected
candidate.

**L. Disposition.** `ARCHIVE_AVAILABLE_NOT_ACQUIRED__NO_ACQUISITION_AUTHORIZED`

#### I-AD-2 — Volatility state as a moderator of funding-clamp censoring

**A. Identity.** `I-AD-2`; A×D; censoring-rate conditioning. *Does the volatility state change how often
the published funding rate is pinned inside its clamp dead zone, and therefore how informative funding is?*

**B. Mechanism interaction.** Mechanism A: the published funding rate is an interval-censored transform
of the premium index, pinned at the interest term whenever the premium lies within ±0.05% of it (S9).
Mechanism B: premium magnitude scales with the risk and capital scarcity that also drive volatility (S6,
S8). Joint claim: the censoring probability — the fraction of the funding series that carries no premium
information — is itself a function of the volatility state, so the informativeness of the funding series
is conditioned on layer A.

**C. Observable implication.** The share of settlements at the interest term, stratified by realized
volatility, predicted to fall as volatility rises. Competing explanations: exchange parameter changes;
regime shifts in the interest term. Contemporaneous. Structural.

**D. Data requirements.** Layer D: on-disk `funding__v001` for BTCUSDT. Layer A: realized volatility from
on-disk klines or aggTrades. 8-hour settlements at 00:00/08:00/16:00 UTC aligned to the enclosing
volatility interval. **Both legs `AVAILABLE_NON_RESERVE`.** No acquisition. No reserve. Provenance
uncertainty: the 2024 cap, IMN, and interest-term values are unestablished (§5.7), and the interest term
is the exact quantity the censoring test is about.

**E. Identification.** `COMPUTABLE` yes. `IDENTIFIED` moderate — the censoring structure is a published
contractual identity, but attributing its variation to volatility rather than to a changing interest term
requires the unestablished 2024 parameters. `SCIENTIFICALLY_INFORMATIVE` moderate.
`DECISION_RELEVANT` low.

**F. Prior-work distance.** Nearest Prometheus family: **NL-C2**, whose own §F names "the share of
settlements in the censored dead zone" as its primary test statistic. This card adds a stratifier and
nothing else. Nearest stopped arc: none. Nearest rescue trap: NL-C2, and behind it D1-A. Structural
distinction: **none** — §15 is explicit that a context variable does not create a new mechanism by
conditioning an old result, and §4 forbids treating interaction with another data family as sufficient to
rescue NL-C2.

**G. Decision consequence.** Pass would be read as evidence that NL-C2 is more tractable than its card
concedes — a silent reopening. Fail would pre-empt the independent review that NL-C2 requires and has not
had. Legitimate current consumer: **none**. Self-created: yes.

**H. Researcher freedom.** Forced: the ±0.05% dead-zone half-width, the settlement cadence, and the cap
rule are exchange-published. Free: the volatility estimator, the stratification, the consistency
tolerance. Contamination: the 5 bps half-width is of the same order as the locked 8 bps reference, a
comparison the NL-C2 card already forbids.

**I. Evidence posture.** Non-reserve feasible. No acquisition. Reserve pressure low — the reserves are
aggTrades-family objects and a funding question has no honest claim on them.

**J. Cost and proportionality.** Engineering low; documentation high; governance **very high**, because
the phase's dominant task would be arguing that it is not reopening an unreviewed candidate. Gain low.

**K. Strongest case against proceeding.** The admissibility of both legs is exactly what makes this
dangerous rather than attractive: it is the cheapest available route to advancing NL-C2 without the
independent review NL-C2 was made conditional on, in the lane governance flags as most rescue-prone.

**L. Disposition.** `HIGH_RESCUE_RISK__DOES_NOT_SURVIVE`

#### I-AD-3 — Volatility state as a moderator of mark-price / last-price divergence

**A. Identity.** `I-AD-3`; A×D; stop-domain divergence conditioning. *Does the volatility state change
how far the contract's mark price diverges from its last-trade price?*

**B. Mechanism interaction.** Mechanism A: the mark price is an index-anchored construction used for
liquidation and stop triggering. Mechanism B: the last-trade price is the venue's own tape. Joint claim:
the divergence between the two is a state-dependent object that neither series identifies alone, and
volatility conditions its magnitude. External source: S9 for the construction; Phase 3r §8 and Phase 3v §8
for the governance framing.

**C. Observable implication.** Mark-minus-last divergence stratified by realized volatility. Competing
explanations: index-composition effects; upstream invalid windows. Contemporaneous. Structural.

**D. Data requirements.** Layer D: mark-price klines — `ARCHIVE_AVAILABLE_NOT_ACQUIRED`, additionally
governed by Phase 3r §8 invalid-window rules. Layer A: on-disk klines. Acquisition required and not
authorized. No reserve.

**E. Identification.** `COMPUTABLE` no on held data. `IDENTIFIED` moderate. `SCIENTIFICALLY_INFORMATIVE`
moderate. `DECISION_RELEVANT` **no** — the object is an execution-realism quantity and M0 §7.E records
that lane as `NOT_RECOMMENDED_NOW` precisely because it does not address any open project question.

**F. Prior-work distance.** Nearest Prometheus family: M0 §7.E execution-realism lane; Phase 3v §8
stop-trigger-domain governance. Nearest rescue trap: an execution-realism study that becomes a stop-design
study. Structural distinction: it would be non-directional; but §7.E's objection is not directionality, it
is irrelevance to any open question.

**G. Decision consequence.** Pass: adds a divergence statistic with no consumer. Fail: closes nothing.
Legitimate current consumer: none. Self-created: yes.

**H. Researcher freedom.** Divergence metric, bar interval, and stratification all free and unanchored.

**I. Evidence posture.** Requires acquisition; no reserve pressure.

**J. Cost and proportionality.** Acquisition cost material; governance cost high (Phase 3r §8 invalid-window
predeclaration would be required); gain low.

**K. Strongest case against proceeding.** It is an acquisition proposal in a lane the project has already
labelled not-recommended, for a quantity that would matter only if a strategy existed — and none does or
may.

**L. Disposition.** `ARCHIVE_AVAILABLE_NOT_ACQUIRED__NO_ACQUISITION_AUTHORIZED`

---

### Pair A×E — price geometry and magnitude × positioning and forced-flow state

#### I-AE-1 — Outstanding positioning as a moderator of price volatility

**A. Identity.** `I-AE-1`; A×E; depth-proxy conditioning of volatility. *Does the level of outstanding
open interest change the volatility consequence of the price process?*

**B. Mechanism interaction.** Mechanism A: volatility is generated by information arrival and order flow.
Mechanism B: outstanding open positions represent standing willingness to absorb — market depth in the
futures-market sense. Joint claim, stated directly by the source: **large open interest mitigates
volatility**, so the same shock has a smaller magnitude consequence in a deeply positioned market than in
a thinly positioned one. Neither leg alone identifies it — a volatility series carries no positioning
information and an open-interest series carries no magnitude. External source: **X3 (Bessembinder & Seguin
1993)**, which uses open interest as a proxy for market depth and finds a significantly negative effect of
depth on contemporaneous volatility.

**C. Observable implication.** Realized volatility regressed on volume components with open interest as a
conditioning variable; the depth coefficient predicted negative. Competing explanations: open interest and
volatility are jointly driven by the same participation cycle; open interest is a stock and volatility a
flow, so the relation may be mechanical. Contemporaneous. Structural.

**D. Data requirements.** Layer E: open-interest history over the study window. Layer A: realized
volatility. Binance USDⓈ-M; BTCUSDT; 2024. **Status of the moderating leg: `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE`**
— `openInterestHist` retains only the latest 30 days, so a 2024 window has **zero** coverage and cannot be
back-filled by any authorized or unauthorized means. The Phase 4i partial OI series is governed by Phase
4j §11 and does not cover this substrate. No reserve implicated.

**E. Identification.** `COMPUTABLE` **no**. `IDENTIFIED` strong in principle — this is one of the few
interactions in the atlas with a directly stated, venue-appropriate empirical precedent.
`SCIENTIFICALLY_INFORMATIVE` yes. `DECISION_RELEVANT` moderate — it would bear on whether the project's
magnitude findings are positioning-conditioned.

**F. Prior-work distance.** Nearest Prometheus family: **M-11** (open-interest context) and **M-12**.
Nearest stopped arc: none. Nearest rescue trap: reconstructing open interest from unsigned volume, which
§16 of the authorization names as a prohibited proxy by example. Structural distinction from M-11: M-11
treats OI as a context variable; this treats it as a moderator with a signed theoretical prediction.
Reason the distinction may fail: it is irrelevant — the data does not exist for the window.

**G. Decision consequence.** Unreachable. Legitimate current consumer would have been the magnitude
record. Self-created: no.

**H. Researcher freedom.** Moot. The expected/unexpected volume decomposition in X3 is a researcher-chosen
time-series model, so even with data the design would be under-anchored.

**I. Evidence posture.** No non-reserve path; no path at all for the historical window. Acquisition
pressure is **structurally futile** — forward capture cannot produce a 2024 series. Reserve pressure none.

**J. Cost and proportionality.** Any attempt would spend engineering and governance on an unobtainable
series.

**K. Strongest case against proceeding.** The moderator is not merely unacquired; it is **unrecoverable**.
Binance's 30-day retention means the 2024 open-interest series no longer exists in any admissible public
form, and no forward capture creates it. This is the cleanest possible data block.

**L. Disposition.** `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED`

#### I-AE-2 — Forced-liquidation state as a moderator of price jumps

**A. Identity.** `I-AE-2`; A×E; cascade conditioning of discontinuity. *Does the presence of forced
liquidation change what a price jump implies about subsequent price behaviour?*

**B. Mechanism interaction.** Mechanism A: leveraged positions are closed involuntarily when margin is
breached. Mechanism B: price discontinuities occur. Joint claim: a jump accompanied by forced flow is a
mechanically different event from an information jump, with different continuation and reversion
properties. External source: X7 (Brunnermeier & Pedersen 2009) for the destabilizing-margin channel; M-9
in the committed map.

**C. Observable implication.** Jump-conditioned forward behaviour, stratified by liquidation intensity.
Competing explanations, as recorded in the committed Phase 4bn-AX audit §12: informed trading, news
response, ordinary non-forced inventory unwinding, and momentum herding all produce the same tape
signature. Predictive. Causal in claim, forecasting in form.

**D. Data requirements.** Layer E: a liquidation tape. **Status `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE`** —
`forceOrder` has no public archive, publishes only the largest order per 1000 ms per symbol, and its REST
counterpart is authenticated user-scope and inadmissible for market research. Layer A: on-disk prices. No
reserve implicated.

**E. Identification.** `COMPUTABLE` **no**. `IDENTIFIED` **no**, even with the WS stream, because the feed
is a bounded snapshot rather than a complete tape. `SCIENTIFICALLY_INFORMATIVE` would be yes with a real
tape. `DECISION_RELEVANT` no under current governance.

**F. Prior-work distance.** Nearest Prometheus family: **M-9**; AW rejected candidate #4. Nearest stopped
arc: `STOP_LONGHORIZON_ML_ARC` via the directional endpoint. Nearest rescue trap:
**`REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`**, the exact family. Structural distinction: none.

**G. Decision consequence.** Unreachable, and the family is closed by a binding committed rejection.

**H. Researcher freedom.** Event definition, threshold, and horizon all free; the committed audit records
that the family's predicted sign flips with an unfixed horizon, so it can be made to match either prior
rejection post hoc.

**I. Evidence posture.** No path. Any attempt would require substituting aggressor imbalance, burst
intensity, or unsigned volume for the liquidation leg.

**J. Cost and proportionality.** Not proportionate at any cost.

**K. Strongest case against proceeding.** The only route to an observable is a proxy the project has
already rejected by name, and §16 forbids repairing a rejected interaction by adding another proxy.

**L. Disposition.** `PROXY_DEPENDENT__REJECT`

---

### Pair A×F — price geometry and magnitude × cross-market and contextual state

#### I-AF-1 — Clock periodicity as a moderator of volatility dynamics

**A. Identity.** `I-AF-1`; A×F; intraday periodicity conditioning. *Does the position within the
deterministic UTC clock change the measured persistence of realized volatility?*

**B. Mechanism interaction.** Mechanism A: volatility clusters and is persistent. Mechanism B: a
deterministic periodic component modulates the level. Joint claim, stated by the source: failing to
account for the periodic component distorts the measured dynamics, so the clock position changes what a
given volatility reading implies about the next one. External sources: **X10 (Andersen & Bollerslev
1997)**; **X2 (Admati & Pfleiderer 1988)** for why periodicity should be endogenous rather than incidental.

**C. Observable implication.** Realized-volatility persistence estimated with and without a periodic
adjustment. Competing explanations: the periodicity is itself an artefact of activity periodicity; on a
24/7 venue there is no session boundary to anchor the pattern. Contemporaneous and predictive.
Forecasting.

**D. Data requirements.** Layer A: realized volatility from on-disk klines or aggTrades. Layer F:
`utc_hour`, `utc_minute`, `milliseconds_since_day_start` — already committed feature columns, derived from
timestamps, requiring **no data acquisition at all**. `AVAILABLE_NON_RESERVE`. No reserve.

**E. Identification.** `COMPUTABLE` yes. `IDENTIFIED` moderate. `SCIENTIFICALLY_INFORMATIVE` no — the
object is the CF-1 target on the CF-1 substrate. `DECISION_RELEVANT` no.

**F. Prior-work distance.** Nearest Prometheus family: **CF-3**, defined as "derivatives-context +
settlement/session-timing volatility-regime conditioning", shortlisted and explicitly left unselected and
unbundled; and **Phase 4bn-BE N-06**, which rejected intraday periodicity as a fresh family precisely
because CF-3 already occupies the space. Nearest rescue trap: CF-1, via the target. Structural
distinction: none available.

**G. Decision consequence.** Pass: nothing changes. Fail: nothing closes. Legitimate current consumer:
none. Self-created: yes.

**H. Researcher freedom.** The periodic basis, bin count, and estimator are unanchored on a 24/7 venue,
where X10's session anchor does not exist.

**I. Evidence posture.** Non-reserve feasible; irrelevant.

**J. Cost and proportionality.** Low cost, zero decision gain.

**K. Strongest case against proceeding.** Reviving a family the project has already named, shortlisted,
declined to select, and then rejected again in a later screening is renaming, not discovery.

**L. Disposition.** `DUPLICATIVE_OR_ALREADY_DEPLETED`

#### I-AF-2 — Cross-symbol volatility state as a moderator of own-symbol volatility

**A. Identity.** `I-AF-2`; A×F; common volatility factor. *Does the cross-symbol volatility state change
what own-symbol volatility implies?*

**B. Mechanism interaction.** Mechanism A: own-symbol volatility clusters. Mechanism B: a market-wide
volatility factor moves all crypto perpetuals together. Joint claim: decomposing own volatility into
common and idiosyncratic components requires the cross-symbol state, and the two components have
different persistence. External source: **X5 (Hasbrouck & Seppi 2001)** for the existence and dominance of
common factors in returns and flows.

**C. Observable implication.** Common and idiosyncratic volatility components and their differential
persistence. Competing explanations: a single latent driver with heterogeneous loadings; liquidity-tier
differences among the five core symbols. Contemporaneous and predictive. Structural.

**D. Data requirements.** Layer A and F: multi-symbol klines for BTCUSDT, ETHUSDT, ADA, SOL, XRP — **on
disk**, `AVAILABLE_NON_RESERVE`, subject to Phase 4ad Rule B1's common post-gap start `2022-04-03` for
SOL and XRP. Bar `open_time` alignment. No acquisition. No reserve.

**E. Identification.** `COMPUTABLE` **yes**. `IDENTIFIED` moderate — factor extraction from five series
is under-determined and the decomposition is model-dependent. `SCIENTIFICALLY_INFORMATIVE` marginally.
`DECISION_RELEVANT` **no**.

**F. Prior-work distance.** Nearest Prometheus family: **CF-2** (cross-symbol, temporal, but directional)
and **CF-1** (the volatility target). Nearest cooled-down family: **M0 §7.B**, the cross-sectional
symbol-selection lane, `COOLED_DOWN_AFTER_NOT_SUPPORTED`, whose blocked actions include symbol-universe
expansion. Structural distinction: a volatility factor is not a symbol ranking and is not directional.
Reason the distinction may fail: the object is still a cross-symbol construction over the exact five-symbol
universe whose cross-sectional use returned `NOT_SUPPORTED`, and the natural next step from any positive
finding is a regime or allocation object, which is prohibited.

**G. Decision consequence.** **Pass:** the project would learn that crypto perpetual volatility has a
common factor — a fact the external literature already treats as established, and which changes no
Prometheus decision. **Fail:** would contradict established literature and most plausibly indicate a
measurement problem, not a market fact. **Invalid:** recorded. Legitimate current consumer: **none** —
it closes no open Prometheus mechanism family, resolves no stated data-identification question, and
supports no acquisition question. Self-created: yes.

**H. Researcher freedom.** Forced: nothing. Free: symbol set, interval, volatility estimator, factor
model, number of factors, estimation window, standardization. Contamination: low, since no cross-symbol
volatility quantity exists on `main`. Clean preregistration: possible in form, but every choice would be
frozen arbitrariness.

**I. Evidence posture.** Fully non-reserve. No acquisition. Reserve pressure low. Would remain
development-only.

**J. Cost and proportionality.** Documentation moderate; acquisition none; engineering low; validation
moderate; governance moderate (§7.B adjacency must be confronted). Scientific gain low.
**Decision-relevant gain zero.**

**K. Strongest case against proceeding.** This is the atlas's clearest instance of the failure mode §17
was written for: the data is there, the mechanism is real, the computation is cheap — and no legitimate
decision in the project changes on either branch. Building it would create a capability whose only
downstream uses are prohibited, in a lane that is already cooled down.

**L. Disposition.** `DATA_AVAILABLE_BUT_NO_DECISION_CONSUMER`

#### I-AF-3 — Sampling-frequency dependence of cross-symbol correlation

**A. Identity.** `I-AF-3`; A×F; Epps-effect family. *Does the sampling frequency change measured
cross-symbol correlation in the way asynchronous-trading theory requires?*

**B. Mechanism interaction.** Mechanism A: correlated fundamentals. Mechanism B: asynchronous arrival of
trades across instruments. Joint claim: measured correlation decays toward zero as the sampling interval
shrinks, and the decay profile identifies the asynchrony. Named in the committed Phase 4bn-BE §6.2 list;
no substantive claim rests on an unverified source here.

**C. Observable implication.** The correlation-versus-frequency curve. Competing explanations: genuine
high-frequency decorrelation; microstructure noise. Contemporaneous. Descriptive.

**D. Data requirements.** Synchronous multi-symbol tick data. Multi-symbol aggTrades are
`ARCHIVE_AVAILABLE_NOT_ACQUIRED`; klines are far too coarse to exhibit the effect at the frequencies where
it lives. No reserve.

**E. Identification.** `COMPUTABLE` no on held data. `IDENTIFIED` moderate. `SCIENTIFICALLY_INFORMATIVE`
low. `DECISION_RELEVANT` no.

**F. Prior-work distance.** Nearest Prometheus family: **CF-2**, blocked and unpromoted; recorded as
Phase 4bn-BE **N-09**. Structural distinction: none.

**G. Decision consequence.** Pass and fail both change nothing. Legitimate current consumer: none.

**H. Researcher freedom.** Frequency grid, pair set, and estimator free.

**I. Evidence posture.** Acquisition required; no reserve pressure.

**J. Cost and proportionality.** Acquisition cost material for zero decision gain.

**K. Strongest case against proceeding.** It would spend an unauthorized acquisition to re-derive a
textbook artefact in a family the project already left blocked.

**L. Disposition.** `ARCHIVE_AVAILABLE_NOT_ACQUIRED__NO_ACQUISITION_AUTHORIZED`

---

### Pair B×C — executed trade activity × liquidity and order-book state

#### I-BC-1 — Displayed depth as the moderator of the flow-to-price mapping

**A. Identity.** `I-BC-1`; B×C; price impact conditioned on depth. *Does the displayed liquidity state
change the price displacement produced by a given quantity of aggressive flow?*

**B. Mechanism interaction.** Mechanism A: aggressive order flow consumes resting liquidity and moves
price. Mechanism B: the book's displayed depth determines how much price must move to clear a given
quantity. Joint claim, stated in the sharpest available form by X9: **the relation between order-flow
imbalance and price change is linear with a slope inversely proportional to market depth**, and X1
supplies the structural interpretation that `1/λ` *is* depth. Neither leg alone identifies it: a flow
series without depth cannot distinguish a large move caused by large flow from one caused by a thin book,
and a depth series without flow predicts nothing. This is the canonical cross-lane interaction of market
microstructure and the reference case for the whole atlas. External sources: **X9 (Cont, Kukanov & Stoikov
2014)**, **X1 (Kyle 1985)**, with **X5** on the time variation of impact coefficients.

**C. Observable implication.** Regression of short-horizon price change on order-flow imbalance, with the
slope predicted to scale as the inverse of contemporaneous depth; and the derived square-root relation
between move magnitude and volume. Competing explanations: informed flow arrives when depth is low
(reverse causation through adverse selection); transient displayed liquidity that never intended to be
consumed; spoofing-like flickering. Contemporaneous, with a predictive form. Causal in claim.

**D. Data requirements.** Layer B: signed aggressive quantity — held, as `rolling_aggressive_quantity_imbalance_{w}`
and `rolling_aggressive_flow_ratio_{w}`, though these are **executed-trade** imbalances rather than X9's
best-quote event-based OFI. Layer C: displayed depth at the best quotes, event-time, with sequence-number
validation. Binance USDⓈ-M; BTCUSDT; the 2024 window; millisecond alignment of trades to the prevailing
book. **Status of the moderating leg: `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` / `PROSPECTIVE_ONLY`.**
No public archive exists for derivatives bookTicker, partial depth, or diff depth. No reserve implicated.

**E. Identification.** `COMPUTABLE` **no**. `IDENTIFIED` **strong in principle** — this is one of the
best-identified interactions in microstructure. `SCIENTIFICALLY_INFORMATIVE` yes. `DECISION_RELEVANT`
moderate — a measured impact function would bear directly on M0.5 cost realism, which is the project's
one undischarged blocking clause.

**F. Prior-work distance.** Nearest Prometheus family: **M-3 / M-4 / M-14**, and AW rejected candidate #3.
Nearest stopped arc: `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`, same blocker, different question.
Nearest rescue trap: substituting a trade-tape or range-based quantity for depth. Structural distinction
from the stopped arc: the stopped arc needed quotes to decompose a *label*; this needs depth to *scale* a
flow. Reason the distinction may fail: it does not matter — the same source absence kills both.

**G. Decision consequence.** Unreachable. Had it been reachable, the pass consumer would have been the
cost-realism record and the fail consumer would have been closure of the impact-measurement question.
Self-created: no — this is a genuinely open question the project has never been able to touch.

**H. Researcher freedom.** Moot. Note that the depth aggregation level, the flow window, and the impact
horizon would all be free, and X9's own construction is over quote events rather than trades, so
transferring it to aggTrades would itself be a researcher choice.

**I. Evidence posture.** No non-reserve path. Acquisition pressure is **high in appearance and futile in
fact**: prospective depth capture cannot answer a 2024 question, and the project has a committed finding
(Phase 4bn-AT) that prospective capture is regime-non-comparable. Reserve pressure none.

**J. Cost and proportionality.** Prospective capture would carry substantial storage, reconstruction, and
synchronization cost for a series that cannot address the historical substrate the rest of the project is
built on.

**K. Strongest case against proceeding.** This is the interaction the project would most want, and it is
the one it can least have. The moderating leg is absent from every admissible historical source, and the
only way to obtain it produces a series that cannot be joined to the substrate that carries every other
Prometheus result.

**L. Disposition.** `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED`

#### I-BC-2 — Liquidity fluctuation as the efficiency-restoring counterpart to long-memory flow

**A. Identity.** `I-BC-2`; B×C; long-memory flow with compensating liquidity. *Does liquidity variation
absorb the predictability of long-memory signed flow, keeping returns near-white?*

**B. Mechanism interaction.** Mechanism A: signed order flow is strongly autocorrelated and hence
predictable. Mechanism B: transaction size and liquidity fluctuate anti-correlatedly with flow. Joint
claim: the two together explain how a predictable order-sign process coexists with near-unpredictable
returns — a claim neither leg makes alone. External source: **S10 (Lillo & Farmer 2004)** as recorded in
the committed Phase 4bn-BE table.

**C. Observable implication.** Joint measurement of flow-sign autocorrelation and the compensating
liquidity/impact response. Competing explanations: order splitting alone; herding alone. Contemporaneous.
Structural.

**D. Data requirements.** Layer B: aggressor side per trade — held. Layer C: impact or liquidity response
— **absent**. Status of the moderating leg: `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE`. No reserve.

**E. Identification.** `COMPUTABLE` only for the flow leg. `IDENTIFIED` **no** — measuring only the sign
autocorrelation identifies nothing about efficiency restoration. `SCIENTIFICALLY_INFORMATIVE` no.
`DECISION_RELEVANT` no, and a "flow is predictable and uncompensated" reading would be an invitation back
into the stopped directional programme.

**F. Prior-work distance.** Recorded as Phase 4bn-BE **N-01** with the same grounds. Nearest stopped arc:
`STOP_LONGHORIZON_ML_ARC`, whose substrate already contains the flow-sign features across four windows.

**G. Decision consequence.** Unreachable, and the reachable half is adverse.

**H. Researcher freedom.** Lag grid and estimator free.

**I. Evidence posture.** No path for the compensating leg.

**J. Cost and proportionality.** Not proportionate.

**K. Strongest case against proceeding.** Half of a two-legged mechanism is not a weaker version of the
mechanism; it is a different and already-tested descriptive statistic.

**L. Disposition.** `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED`

#### I-BC-3 — Book resilience as a moderator of the consequence of a trade burst

**A. Identity.** `I-BC-3`; B×C; burst × replenishment. *Does the speed of liquidity replenishment change
what a burst of aggressive trading implies for subsequent price behaviour?*

**B. Mechanism interaction.** Mechanism A: a burst of aggressive flow consumes resting liquidity.
Mechanism B: liquidity providers replenish, or do not. Joint claim: a burst absorbed by fast replenishment
and a burst that leaves the book depleted are different events with different subsequent behaviour —
absorption versus signalling. Neither leg alone: the burst is identical on the tape in both cases.
External source: **X6 (Large 2007)**, which formalizes resiliency as an impulse-response over event
intensities and finds that in over 60% of cases the book does *not* replenish reliably after a large
trade, with a ~20-second half-life when it does.

**C. Observable implication.** Replenishment probability and half-life conditioned on burst size, and the
differential forward price behaviour across the two regimes. Competing explanations: replenishment by
algorithmic quoting that never intends to be consumed; spoofing; the burst and the replenishment sharing
a common driver. Predictive. Causal in claim.

**D. Data requirements.** Layer B: trade bursts — held, as `rolling_aggtrade_count_{w}` and
`rolling_quantity_sum_{w}`. Layer C: post-event book state at sub-second resolution — **absent**;
`PROSPECTIVE_ONLY`. Millisecond synchronization of trades to book updates would be required. No reserve.

**E. Identification.** `COMPUTABLE` **no**. `IDENTIFIED` strong in principle. `SCIENTIFICALLY_INFORMATIVE`
yes. `DECISION_RELEVANT` low under current governance, since the natural consumer is execution timing.

**F. Prior-work distance.** Nearest Prometheus family: **M-7 / M-8**, and AW rejected candidate #3.
Nearest cooled-down family: §7.D. Nearest rescue trap: defining the burst event from the trade tape and
calling the absence of a subsequent move "absorption" — a proxy for replenishment with no independent
validation.

**G. Decision consequence.** Unreachable. Even reachable, the pass consumer is execution-timing, which is
prohibited.

**H. Researcher freedom.** The event definition is itself a research artefact, as the committed Phase 4as
M-7 entry already records; threshold, window, and horizon all free.

**I. Evidence posture.** No path. Acquisition would be prospective-only and regime-non-comparable.

**J. Cost and proportionality.** Not proportionate.

**K. Strongest case against proceeding.** The moderator is unobservable historically, and the tape-only
substitute is precisely the unverifiable inference pattern the project rejected in the forced-flow audit.

**L. Disposition.** `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED`

#### I-BC-4 — Any trade-tape or range-derived stand-in for the liquidity leg

**A. Identity.** `I-BC-4`; B×C; proxy substitution for depth, spread, or resilience. *Can the liquidity
leg of any B×C interaction be reconstructed from quantities Prometheus already holds?*

**B. Mechanism interaction.** None asserted. The card exists because every blocked B×C family generates
pressure toward this move, and the atlas must dispose of it explicitly rather than leave it implicit.
Candidate stand-ins considered: price range as a spread proxy; unsigned volume as a depth proxy; the
absence of a post-burst move as an absorption proxy; realized-volatility inverse as a liquidity proxy;
trade clustering as a metaorder proxy.

**C. Observable implication.** Whatever the stand-in computes — which is, by construction, not the
mechanism leg.

**D. Data requirements.** All stand-ins are computable from held data; that is the hazard, not the
justification.

**E. Identification.** `COMPUTABLE` yes. `IDENTIFIED` **no**. `SCIENTIFICALLY_INFORMATIVE` no.
`DECISION_RELEVANT` no.

**F. Prior-work distance.** Nearest rescue trap: **`REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`**,
whose reasoning transfers exactly. The committed authorization's §16 examples are directly on point:
*price ranges are not quoted spread ground truth*; *unsigned volume is not open interest*; *ordinary
aggressor imbalance is not a liquidation marker*.

**G. Decision consequence.** A result built on a stand-in would be unfalsifiable in the sense that
matters: a null could always be attributed to the proxy rather than the mechanism, and a positive could
never be attributed to the mechanism rather than the proxy.

**H. Researcher freedom.** Unbounded — each stand-in admits an unlimited family of constructions.

**I. Evidence posture.** Would consume non-reserve development evidence to produce an uninterpretable
result.

**J. Cost and proportionality.** Cheap to build, expensive to govern, worthless to consume.

**K. Strongest case against proceeding.** No external theory or official identity establishes a mapping
from any held quantity to displayed depth, quoted spread, or replenishment. §16 requires rejection rather
than repair, and forbids adding a second proxy to fix the first.

**L. Disposition.** `PROXY_DEPENDENT__REJECT`

---

### Pair B×D — executed trade activity × perpetual anchoring and contract state

#### I-BD-1 — Funding state as a moderator of trade activity around settlement

**A. Identity.** `I-BD-1`; B×D; settlement-conditioned activity. *Does the magnitude or sign of the
funding rate change the trade-activity pattern around funding settlement?*

**B. Mechanism interaction.** Mechanism A: funding is a scheduled, deterministic peer-to-peer cash flow
settled at fixed UTC hours (S9). Mechanism B: participants who wish to avoid or capture that cash flow
must trade. Joint claim: the activity consequence of the settlement clock is conditioned on the size of
the payment at stake, so activity around settlement should scale with funding magnitude. External sources:
S9 for the settlement identity; **X2 (Admati & Pfleiderer 1988)** for why traders with timing discretion
concentrate.

**C. Observable implication.** Trade-arrival intensity in windows bracketing 00:00 / 08:00 / 16:00 UTC,
stratified by the contemporaneous funding rate. Competing explanations: the settlement hours coincide with
regional session boundaries; X11's quarter-hour algorithmic periodicity; a common information cycle.
Contemporaneous. Structural.

**D. Data requirements.** Layer B: aggTrades activity — held. Layer D: funding history — held. Layer F
supplies the clock at no cost. All `AVAILABLE_NON_RESERVE`. No acquisition. No reserve. Provenance
uncertainty: the 2024 settlement cadence is assumed to be the documented 8-hour default and is not
independently established for the window.

**E. Identification.** `COMPUTABLE` yes. `IDENTIFIED` weak — session and algorithmic periodicity confound
the settlement hours, and no admissible variable separates them. `SCIENTIFICALLY_INFORMATIVE` low.
`DECISION_RELEVANT` no.

**F. Prior-work distance.** Nearest Prometheus family: **CF-3**, defined as "derivatives-context +
settlement/session-timing volatility-regime conditioning" with funding extremes and a deterministic
calendar as the conditioning variables and realized volatility or activity as the outcome. That is this
card. CF-3 was shortlisted at Phase 4bn-AW, recorded as unselected and explicitly unbundled at Phase
4bn-AX §23, and is not reopened here. Nearest cooled-down family: §7.C. Structural distinction: none.

**G. Decision consequence.** Pass: re-establishes a shortlisted-but-unselected family without the
selection process that family requires. Fail: pre-empts it. Legitimate current consumer: **none**.
Self-created: yes.

**H. Researcher freedom.** Forced: the settlement hours. Free: bracket width, activity measure, funding
stratification, control-window construction.

**I. Evidence posture.** Fully non-reserve; no acquisition; low reserve pressure.

**J. Cost and proportionality.** Cheap to build; the governance cost of distinguishing it from CF-3 exceeds
its scientific yield.

**K. Strongest case against proceeding.** It is CF-3 under an interaction heading. The project has a
committed record of shortlisting CF-3, declining to select it, and declining to bundle it; re-entering it
through the atlas would bypass that record.

**L. Disposition.** `DUPLICATIVE_OR_ALREADY_DEPLETED`

#### I-BD-2 — Premium state as a moderator of aggressive-flow consequence

**A. Identity.** `I-BD-2`; B×D; anchoring-conditioned flow. *Does the perpetual's premium over its index
change what aggressive flow implies?*

**B. Mechanism interaction.** Mechanism A: aggressive flow expresses directional urgency. Mechanism B: a
standing premium indicates that the contract is already displaced from its anchor and that arbitrage
pressure is building (S6 Prop. 2). Joint claim: flow into an already-stretched premium has a different
consequence from flow into a balanced one, because the marginal arbitrageur's participation is
state-dependent. External sources: S6, S7, X8.

**C. Observable implication.** Flow-conditioned premium dynamics. Competing explanations, decisive: S8
attributes premium variation mainly to convenience yields and limited arbitrage capital. Contemporaneous
and predictive. Causal in claim.

**D. Data requirements.** Layer B: held. Layer D: premium-index or index-price klines —
`ARCHIVE_AVAILABLE_NOT_ACQUIRED`. Acquisition required and **not authorized**. No reserve.

**E. Identification.** `COMPUTABLE` no on held data. `IDENTIFIED` weak — the premium's drivers are not
separable. `SCIENTIFICALLY_INFORMATIVE` moderate. `DECISION_RELEVANT` low, and the natural reading is
directional, which §7.C forbids.

**F. Prior-work distance.** Nearest Prometheus family: NL-C2's extended form; M-10. Nearest rescue trap:
**D1-A**, since a premium-conditioned flow object is one step from a funding-aware directional trigger.

**G. Decision consequence.** Pass: would be read directionally, which is prohibited. Fail: closes little.
Legitimate current consumer: none.

**H. Researcher freedom.** Flow window, premium bucketing, and horizon all free; the horizon choice alone
can flip the predicted sign, which the committed forced-flow audit identifies as a multiple-testing red
flag.

**I. Evidence posture.** Acquisition required. Reserve pressure low.

**J. Cost and proportionality.** Acquisition cost material; governance cost high; gain low.

**K. Strongest case against proceeding.** It requires an unauthorized acquisition to build an object whose
most natural interpretation is exactly the directional derivatives-context use that the D1-A verdict and
M0 §7.C have already closed.

**L. Disposition.** `ARCHIVE_AVAILABLE_NOT_ACQUIRED__NO_ACQUISITION_AUTHORIZED`

#### I-BD-3 — Funding sign as a moderator of taker-imbalance interpretation

**A. Identity.** `I-BD-3`; B×D; crowding-conditioned flow. *Does the funding sign change what taker-flow
imbalance implies about positioning?*

**B. Mechanism interaction.** Mechanism A: persistent funding of one sign indicates crowded leveraged
positioning on that side. Mechanism B: taker imbalance measures which side is aggressing now. Joint claim:
aggression *into* a crowded side and aggression *against* it mean different things. External source: S8 on
trend-chasing demand; M-10 and M-12 in the committed map.

**C. Observable implication.** Forward behaviour conditioned on the sign agreement between funding and
taker imbalance. Competing explanations: the two are mechanically linked through the premium index, which
is itself flow-driven. Predictive. Forecasting.

**D. Data requirements.** Both legs held: aggressor imbalance columns and funding history.
`AVAILABLE_NON_RESERVE`. No acquisition. No reserve.

**E. Identification.** `COMPUTABLE` yes. `IDENTIFIED` **no** — funding is not a positioning measurement;
open interest is, and it is unavailable. `SCIENTIFICALLY_INFORMATIVE` low. `DECISION_RELEVANT` no.

**F. Prior-work distance.** Nearest retained verdict: **D1-A**, funding-aware contrarian, MECHANISM PASS /
FRAMEWORK FAIL. Nearest cooled-down family: **§7.C**, `CONDITIONAL_ONLY / HIGH_D1-A_RESCUE_RISK`. Nearest
stopped arc: `STOP_LONGHORIZON_ML_ARC` via the forward-behaviour target. Structural distinction: the card
would claim to be non-directional; but a sign-agreement variable conditioned on forward behaviour is
directional in everything but name.

**G. Decision consequence.** Pass would be a funding-conditioned directional finding, which is the
rejected D1-A shape. Legitimate current consumer: none.

**H. Researcher freedom.** Imbalance window, funding threshold, horizon, and agreement definition all free.

**I. Evidence posture.** Non-reserve feasible, which increases rather than reduces the hazard.

**J. Cost and proportionality.** Cheap to run and expensive to contain.

**K. Strongest case against proceeding.** It is the most direct available route back to D1-A, in the lane
governance flags as most rescue-prone, using only data already on disk. Its cheapness is the argument
against it.

**L. Disposition.** `HIGH_RESCUE_RISK__DOES_NOT_SURVIVE`

---

### Pair B×E — executed trade activity × positioning and forced-flow state

#### I-BE-1 — Open interest as a moderator of the volume-shock-to-volatility mapping

**A. Identity.** `I-BE-1`; B×E; depth-conditioned volume shock. *Does the outstanding positioning state
change the volatility consequence of an unexpected volume shock?*

**B. Mechanism interaction.** Mechanism A: unexpected volume shocks raise volatility, asymmetrically —
positive shocks more than negative. Mechanism B: outstanding open interest represents standing absorptive
capacity. Joint claim, stated directly by X3: **linking volatility to total volume does not extract all
the information**; the shock must be decomposed, and **large open interest mitigates volatility**, so the
magnitude consequence of the same shock differs by positioning state. This satisfies the atlas's
qualifying test in its strongest form: the joint state identifies an absorption mechanism that neither
volume nor open interest identifies alone. External source: **X3 (Bessembinder & Seguin 1993)**.

**C. Observable implication.** Volatility regressed on expected and unexpected volume components
interacted with open interest; the depth interaction predicted negative and the shock asymmetry predicted
positive. Competing explanations: open interest and volume are jointly determined by the participation
cycle; the expected/unexpected split is model-dependent. Contemporaneous. Structural.

**D. Data requirements.** Layer B: aggTrades volume and count — held for BTCUSDT on the 244-date window.
Layer E: open-interest history for the same window — **`HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE`**;
`openInterestHist` retains 30 days and the 2024 series cannot be recovered by any means. Bar-level
alignment would be required. No reserve implicated.

**E. Identification.** `COMPUTABLE` **no**. `IDENTIFIED` **strong in principle** — a signed, externally
predicted interaction coefficient with a named futures-market precedent. `SCIENTIFICALLY_INFORMATIVE`
yes. `DECISION_RELEVANT` moderate — it would speak to whether the project's magnitude findings are
positioning-conditioned, which is a genuine open question.

**F. Prior-work distance.** Nearest Prometheus family: **M-12** (funding + OI) and **M-11**; also CF-1's
target family on the outcome side. Nearest stopped arc: none. Nearest rescue trap: reconstructing open
interest from volume, explicitly named as prohibited in §16 of the authorization. Structural distinction
from CF-1: CF-1 has no positioning leg at all, and the interaction coefficient — not the main effect — is
the object. Reason the distinction may fail: the outcome variable is the CF-1 target, so a positive result
would generate immediate pressure to read it as a CF-1 extension.

**G. Decision consequence.** Unreachable. Had the data existed, a **fail** would have been the more
valuable branch: it would close the "is the substrate's magnitude structure positioning-conditioned?"
question with admissible evidence. Self-created: no.

**H. Researcher freedom.** Moot, but material: X3's expected/unexpected decomposition is a
researcher-chosen ARMA-type model with no canonical crypto form, the interaction functional form is free,
and the open-interest bucketing is free. Even with data, this design would be under-anchored.

**I. Evidence posture.** No non-reserve path; **no path at all** for the historical window, since the
30-day retention means the series is permanently gone. Acquisition pressure structurally futile. Reserve
pressure none.

**J. Cost and proportionality.** Any pursuit would spend governance on an unobtainable series.

**K. Strongest case against proceeding.** The interaction is real, externally predicted, and
venue-appropriate — and the moderating series for 2024 has ceased to exist. This card is the atlas's
clearest demonstration that Prometheus's blocking constraint is data topology, not imagination.

**L. Disposition.** `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED`

#### I-BE-2 — Forced-deleveraging state as a moderator of aggressive-flow consequence

**A. Identity.** `I-BE-2`; B×E; forced versus voluntary flow. *Does the presence of forced deleveraging
change what aggressive flow implies?*

**B. Mechanism interaction.** Mechanism A: margin breaches produce involuntary, price-insensitive selling
or buying. Mechanism B: aggressive flow is otherwise voluntary and information-bearing. Joint claim:
forced and voluntary aggression have different price consequences, so the forced-flow state moderates the
flow-to-price mapping. External source: X7 for the destabilizing-margin channel; M-9 in the committed map.

**C. Observable implication.** Flow-conditioned forward drift stratified by liquidation state. Competing
explanations, recorded verbatim from the committed Phase 4bn-AX §12 audit: informed trading, news
response, ordinary non-forced inventory unwinding, and momentum herding are all indistinguishable from
forced flow on the trade tape. Predictive. Causal in claim.

**D. Data requirements.** Layer B: held. Layer E: a liquidation marker — **none exists**. `forceOrder` has
no public archive and publishes only the largest order per second; the REST endpoint is authenticated
user-scope; and `FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS` bars the token `liquidation` from any feature
column. No reserve.

**E. Identification.** `COMPUTABLE` no. `IDENTIFIED` no. `SCIENTIFICALLY_INFORMATIVE` no.
`DECISION_RELEVANT` no.

**F. Prior-work distance.** This is, term for term, the family rejected as
**`REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`** — one-sidedness from
`rolling_aggressive_flow_ratio`, size-clustering from `rolling_quantity_mean`, burstiness from
`rolling_aggtrade_count`, thresholded and relabelled as a forced-flow event. Structural distinction:
none.

**G. Decision consequence.** Closed by a binding committed rejection.

**H. Researcher freedom.** Unbounded; the committed audit records that the predicted sign flips with the
horizon.

**I. Evidence posture.** No path except a prohibited proxy.

**J. Cost and proportionality.** Not proportionate at any cost.

**K. Strongest case against proceeding.** Presenting the rejected family as an *interaction* rather than a
*trigger* changes the vocabulary and not the observable. The load-bearing leg remains an unverifiable
inference from ordinary trade-tape statistics.

**L. Disposition.** `PROXY_DEPENDENT__REJECT`

---

### Pair B×F — executed trade activity × cross-market and contextual state

#### I-BF-1 — Market-wide flow state as a moderator of own-symbol flow consequence

**A. Identity.** `I-BF-1`; B×F; commonality in order flow. *Does the market-wide flow state change what
own-symbol aggressive flow implies?*

**B. Mechanism interaction.** Mechanism A: own-symbol flow moves own-symbol price. Mechanism B: a common
factor drives flow across instruments simultaneously. Joint claim, from X5: **commonality in order flows
explains roughly two-thirds of the commonality in returns**, so own-symbol flow that is part of a
market-wide move is a different object from idiosyncratic own-symbol flow, and only the joint state
separates them. External source: **X5 (Hasbrouck & Seppi 2001)**.

**C. Observable implication.** Own-symbol price response to flow, decomposed into common and idiosyncratic
components. Competing explanations: index-arbitrage mechanics; a single latent information driver.
Contemporaneous. Structural.

**D. Data requirements.** Layer B for the own symbol: held. Layer B/F for the market-wide leg:
**synchronous multi-symbol aggTrades** — `ARCHIVE_AVAILABLE_NOT_ACQUIRED`. Multi-symbol klines are
available but far too coarse to carry a flow-sign object. Millisecond cross-symbol alignment would be
required. Acquisition required and **not authorized**. No reserve.

**E. Identification.** `COMPUTABLE` **no** on held data. `IDENTIFIED` moderate — X5's own analysis leans on
liquidity proxies that Prometheus also lacks. `SCIENTIFICALLY_INFORMATIVE` moderate.
`DECISION_RELEVANT` low.

**F. Prior-work distance.** Nearest Prometheus family: **CF-2**, shortlisted and `BLOCKING` on exactly this
acquisition. Nearest cooled-down family: §7.B. Structural distinction from CF-2: CF-2 is a temporal
lead–lag in *returns*; this is a contemporaneous decomposition of *flow*. Reason the distinction may fail:
both are blocked on the same unacquired source, and a lead–lag reading is one step away.

**G. Decision consequence.** Pass: would establish flow commonality on the venue, prospectively only, and
authorize nothing. Fail: would contradict established literature and most likely indicate a measurement
problem. Legitimate current consumer: at most the acquisition-review question, which §18 records without
the experiment. Self-created: partly.

**H. Researcher freedom.** Symbol set, alignment interval, factor model, and flow window all free.

**I. Evidence posture.** Requires acquisition of multi-symbol aggTrades — a materially larger acquisition
than any the project has performed. Reserve pressure low.

**J. Cost and proportionality.** Acquisition and storage cost high; engineering high (cross-symbol
millisecond alignment); decision gain low.

**K. Strongest case against proceeding.** It is the most expensive unacquired-data proposal in the atlas
and its best case is a fact the literature already treats as established, with no legitimate current
consumer on either branch.

**L. Disposition.** `ARCHIVE_AVAILABLE_NOT_ACQUIRED__NO_ACQUISITION_AUTHORIZED`

#### I-BF-2 — Clock mark as a moderator of participation composition

**A. Identity.** `I-BF-2`; B×F; periodic algorithmic participation. *Does the position within the
minute/quarter-hour clock change the composition of executed trade activity?*

**B. Mechanism interaction.** Mechanism A: algorithmic participants schedule on round clock marks.
Mechanism B: discretionary participants do not. Joint claim: the composition of flow at a clock mark
differs systematically from composition away from it, and the volume and volatility consequence of the
mark is a consequence of that composition rather than of the clock itself. External sources: **X11 (Kim &
Hansen 2026)**, whose sample is six Binance perpetual futures contracts; **X2 (Admati & Pfleiderer 1988)**
for the strategic-concentration theory.

**C. Observable implication.** Activity, size-composition, and magnitude measured at and away from one-,
five-, and fifteen-minute marks. Competing explanations: exchange-side batching or reporting artefacts;
funding-settlement and session effects at coarser marks. Contemporaneous. Structural / descriptive.

**D. Data requirements.** Layer B: aggTrades with `transaction_time` and quantity — held. Layer F:
`utc_minute` and `milliseconds_since_day_start` — committed columns derived from timestamps, no
acquisition. All `AVAILABLE_NON_RESERVE`. No reserve. Provenance uncertainty: aggTrades aggregate fills at
the same price and taking side every 100 ms, and insurance-fund and ADL trades are excluded from
aggregation, both of which interact with any minute-boundary statistic.

**E. Identification.** `COMPUTABLE` **yes**. `IDENTIFIED` weak — participation composition is inferred,
not observed. `SCIENTIFICALLY_INFORMATIVE` moderate. `DECISION_RELEVANT` **no**.

**F. Prior-work distance.** Nearest Prometheus family: **CF-3** on the timing side and **CF-1** on the
magnitude side; **I-AB-2** on the composition side. Nearest stopped arc: `STOP_LONGHORIZON_ML_ARC`, which
X11's own headline claim — order imbalance at clock openings predicting returns over 4–12 hour horizons —
sits squarely inside. Structural distinction: the composition question is non-directional. Reason the
distinction may fail: the source that motivates it is a directional-predictability paper, and adopting its
framing without its conclusion is a fragile position to hold across a phase boundary.

**G. Decision consequence.** **Pass:** the project learns that its substrate has clock-periodic
composition. The routes onward are (i) reinterpreting CF-1's features — a forbidden consumer; (ii)
sampling-convention change — an interval tweak forbidden by M0 §6; (iii) a trading application —
prohibited absolutely. **Fail:** closes a question this card created. **Invalid:** recorded.
Legitimate current consumer: **none**. Self-created: **yes**.

**H. Researcher freedom.** Forced: the clock marks themselves. Free: bracket width, composition metric,
roundness definition, magnitude estimator, and which marks to test. Contamination: moderate — the author
knows CF-1's window structure and X11's claimed effects.

**I. Evidence posture.** Fully non-reserve. No acquisition. Reserve pressure low. Development-only.

**J. Cost and proportionality.** Engineering low; documentation moderate; governance high (the directional
half of the source must be firewalled explicitly). Scientific gain moderate. Decision gain zero.

**K. Strongest case against proceeding.** Every path from a positive result to a project consequence is
closed by existing governance, and the phase would have spent its discipline importing a framing from a
paper whose principal claim the project is forbidden to pursue.

**L. Disposition.** `REJECTED_ABSENT_DECISION_CONSEQUENCE`

#### I-BF-3 — Common versus idiosyncratic volume shocks

**A. Identity.** `I-BF-3`; B×F; shock-origin conditioning. *Does it matter, for the volatility consequence
of a volume shock, whether the shock is market-wide or symbol-specific?*

**B. Mechanism interaction.** Mechanism A: volume shocks raise volatility (X3). Mechanism B: shocks
decompose into a common component and an idiosyncratic one (X5). Joint claim: the volatility consequence
differs by shock origin, and only the cross-symbol state identifies the origin. This is a qualifying
interaction.

**C. Observable implication.** Volatility response to decomposed volume shocks across the five core
symbols. Competing explanations: liquidity-tier heterogeneity; the Phase 4ad Rule B gap structure;
a single latent driver. Contemporaneous. Structural.

**D. Data requirements.** Layer A/B/F: multi-symbol klines with volume and OHLC for BTCUSDT, ETHUSDT, ADA,
SOL, XRP — **on disk**, `AVAILABLE_NON_RESERVE`, with the Phase 4ad Rule B1 common start `2022-04-03`.
Bar `open_time` alignment. No acquisition. No reserve.

**E. Identification.** `COMPUTABLE` **yes**. `IDENTIFIED` weak — with five series the common/idiosyncratic
split is model-determined rather than data-determined. `SCIENTIFICALLY_INFORMATIVE` low.
`DECISION_RELEVANT` **no**.

**F. Prior-work distance.** Nearest Prometheus family: CF-1's target family, cross-sectionally extended.
Nearest cooled-down family: **§7.B**, whose blocked actions include symbol-universe expansion and
composite-weight reassignment — and a factor decomposition over the same five-symbol universe is a
composite construction over that universe. Structural distinction: it is not a ranking and not
directional. Reason the distinction may fail: the §7.B objection was to composite constructions over this
universe producing `NOT_SUPPORTED`, and a factor model is a composite construction.

**G. Decision consequence.** **Pass:** volume shocks have an origin-dependent volatility consequence — a
fact with no Prometheus consumer, since no allocation, sizing, gating, or regime object may be built.
**Fail:** closes a question the card created. Legitimate current consumer: **none**. Self-created: **yes**.

**H. Researcher freedom.** Forced: nothing. Free: symbol set, interval, shock model, factor count,
estimation window, interaction functional form, volatility estimator. This is an unbounded menu with no
external anchor, and it compounds the consumer failure rather than replacing it.

**I. Evidence posture.** Fully non-reserve; no acquisition; low reserve pressure.

**J. Cost and proportionality.** Low engineering, moderate governance, zero decision gain.

**K. Strongest case against proceeding.** Neither branch changes any legitimate project state, and the
design could not be frozen on principle — only frozen arbitrarily. Both failures are independently
sufficient; the decision-consequence failure is the more fundamental and is recorded as the disposition.

**L. Disposition.** `REJECTED_ABSENT_DECISION_CONSEQUENCE`

---

### Pair C×D — liquidity and order-book state × perpetual anchoring and contract state

#### I-CD-1 — Recovering book state by inverting the published funding identity

**A. Identity.** `I-CD-1`; C×D; premium-index inversion. *Because the premium index is built from
depth-derived impact fill prices, can the published funding series be inverted to recover information
about the book?*

**B. Mechanism interaction.** Mechanism A: the exchange computes an Impact Bid and Impact Ask price as the
average fill price required to execute the Impact Margin Notional on each side of the book, and forms the
premium index from them (S9). Mechanism B: funding is a clamped transform of the averaged premium index.
Joint claim: the funding series therefore carries, in principle, a compressed trace of the book's shape at
the impact notional. Neither leg alone: funding without the identity is an opaque number; the identity
without funding has no data.

**C. Observable implication.** A recovered interval on the impact-price spread per settlement. Competing
explanations: the mapping from a book shape to a single impact-price pair is **many-to-one**, so infinitely
many books produce the same premium; the index is averaged over eight hours; the clamp censors; and the
2024 Impact Margin Notional is unestablished.

**D. Data requirements.** Layer D: funding history — held. Layer C: the Impact Margin Notional, the tick
size, and the book-shape assumptions needed to invert — **absent**; `UNKNOWN__DOCUMENTATION_REQUIRED` for
the 2024 parameters and `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` for anything that could validate the
inversion. No reserve.

**E. Identification.** `COMPUTABLE` only as an unvalidated transform. `IDENTIFIED` **no** — the inversion
is many-to-one, eight-hour-averaged, and interval-censored. `SCIENTIFICALLY_INFORMATIVE` no.
`DECISION_RELEVANT` no.

**F. Prior-work distance.** Nearest stopped arc: **`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`** — this is
the side door into order-book information that the Phase 4bn-BE NL-C2 card explicitly anticipated and
disclaimed, noting that the premium index "cannot produce a midpoint, a spread, or a quote for any
specific instant". Nearest rescue trap: the same. Structural distinction: none that survives, because the
whole point of this card is to obtain book information from a non-book source.

**G. Decision consequence.** A recovered "depth" number of unknown accuracy, about a window in which no
admissible object could check it. Legitimate current consumer: none.

**H. Researcher freedom.** The book-shape assumption required to invert is entirely researcher-chosen.

**I. Evidence posture.** Non-reserve in form; illegitimate in substance.

**J. Cost and proportionality.** Cheap to compute; corrosive to the project's source-admissibility
discipline.

**K. Strongest case against proceeding.** It is a proxy dressed as an identity. The identity runs *from*
the book *to* the premium; running it backwards is not inversion but assumption, and the project has a
committed lock stating that the top-of-book layer is inadmissible for this window. §16 requires rejection,
not repair.

**L. Disposition.** `PROXY_DEPENDENT__REJECT`

#### I-CD-2 — Execution liquidity as a moderator of the arbitrage bound

**A. Identity.** `I-CD-2`; C×D; cost-conditioned no-arbitrage band. *Does the state of the order book
change the width of the band within which the perpetual may deviate from its anchor?*

**B. Mechanism interaction.** Mechanism A: S6 Proposition 2 bounds the deviation by the round-trip
trading cost `C`. Mechanism B: `C` is not a constant — it is set by the spread and the depth the
arbitrageur must cross. Joint claim: the observed band is a *reading* of the contemporaneous book, and the
joint state separates a liquidity component of the bound from the capital and convenience-yield
components S8 identifies. External sources: S6, S8, X1, X9.

**C. Observable implication.** Deviation magnitude conditioned on measured spread and depth. Competing
explanations, decisive: S8 attributes the deviation mainly to convenience yields and limited arbitrage
capital, and X8 adds margin and collateral costs; the liquidity component is one unseparated term among
several. Contemporaneous. Structural.

**D. Data requirements.** Layer C: spread and depth — **`HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE`**.
Layer D: premium or index series — `ARCHIVE_AVAILABLE_NOT_ACQUIRED`. **Both legs blocked, one
permanently.** No reserve.

**E. Identification.** `COMPUTABLE` no. `IDENTIFIED` weak even with data. `SCIENTIFICALLY_INFORMATIVE`
moderate. `DECISION_RELEVANT` moderate — it is the closest any interaction in the atlas comes to bearing
on M0.5.

**F. Prior-work distance.** Nearest Prometheus family: NL-C2 extended form plus M-1/M-2. Nearest stopped
arc: the ToB arc, on the liquidity leg.

**G. Decision consequence.** Unreachable. Self-created: no.

**H. Researcher freedom.** Moot; the decomposition would be unidentified regardless of design.

**I. Evidence posture.** No path.

**J. Cost and proportionality.** Not proportionate.

**K. Strongest case against proceeding.** It requires the one layer that has no history and the one layer
that has not been acquired, to estimate a quantity that the strongest source says is dominated by terms it
cannot separate.

**L. Disposition.** `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED`

---

### Pair C×E — liquidity and order-book state × positioning and forced-flow state

#### I-CE-1 — Funding-constraint state and market-liquidity state as mutual moderators

**A. Identity.** `I-CE-1`; C×E; liquidity spirals. *Does the funding-constraint state of leveraged
participants change the market-liquidity consequence of a shock, and conversely?*

**B. Mechanism interaction.** Mechanism A: traders' ability to obtain funding governs their capacity to
supply liquidity. Mechanism B: market liquidity governs the mark-to-market losses and margins that
constrain funding. Joint claim, stated by the source: under identified conditions **margins are
destabilizing and the two liquidities are mutually reinforcing, producing liquidity spirals**. The spiral
is a joint object; neither leg alone identifies it, and the mutual-reinforcement structure is precisely
what makes this a qualifying interaction rather than a covariate pair. External source: **X7 (Brunnermeier
& Pedersen 2009)**, with **X8 (Gârleanu & Pedersen 2011)** supplying the margin-to-basis channel.

**C. Observable implication.** Joint dynamics of depth/spread and margin/positioning state around stress
episodes, with a predicted amplification regime. Competing explanations: common exposure to an information
shock; exchange-side risk-parameter changes. Contemporaneous with feedback. Causal in claim.

**D. Data requirements.** Layer C: depth or quotes — **`HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE`** /
`PROSPECTIVE_ONLY`. Layer E: margin, positioning, or liquidation state — **`HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE`**;
open interest is 30-day-retained and `forceOrder` has no archive. **Both legs are unavailable
simultaneously**, which makes this the most thoroughly blocked pair in the atlas. No reserve.

**E. Identification.** `COMPUTABLE` **no**. `IDENTIFIED` strong in principle. `SCIENTIFICALLY_INFORMATIVE`
yes — a crypto-perpetual test of the spiral mechanism would be genuinely interesting.
`DECISION_RELEVANT` low for Prometheus, since no lane could consume it.

**F. Prior-work distance.** Nearest Prometheus family: **M-14** (spread/depth/flow regime interaction) and
**M-9**. Nearest cooled-down families: §7.D and §7.C together. Nearest rescue trap: a "stress regime"
object built from held features, which would be a regime classifier over the depleted lanes.

**G. Decision consequence.** Unreachable.

**H. Researcher freedom.** Moot; the stress-episode definition would be a free parameter of the most
overfitting-prone kind, which the committed Phase 4as M-14 entry already flags against the G1 precedent.

**I. Evidence posture.** No path on either leg.

**J. Cost and proportionality.** Not proportionate.

**K. Strongest case against proceeding.** Both legs are structurally unavailable, and any tape-only
substitute would be two proxies stacked, which §16 forbids explicitly.

**L. Disposition.** `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED`

#### I-CE-2 — Book depletion as a moderator of cascade propagation

**A. Identity.** `I-CE-2`; C×E; depletion-conditioned cascade. *Does the depleted state of the book change
how far a forced-liquidation event propagates?*

**B. Mechanism interaction.** Mechanism A: forced liquidations submit price-insensitive orders. Mechanism
B: a depleted book converts a given forced quantity into a larger displacement, which triggers further
liquidations. Joint claim: the cascade is a joint phenomenon of forced flow and book state, and its
propagation depends on the interaction rather than on either leg. External sources: X7; X6 on
replenishment; M-7 / M-9 in the committed map.

**C. Observable implication.** Cascade length and displacement conditioned on pre-event depth. Competing
explanations: as for I-AE-2. Predictive. Causal in claim.

**D. Data requirements.** Both legs absent — depth is `PROSPECTIVE_ONLY` and liquidations have no archive.
No reserve.

**E. Identification.** `COMPUTABLE` no. `IDENTIFIED` no on any admissible source.
`SCIENTIFICALLY_INFORMATIVE` yes in principle. `DECISION_RELEVANT` no.

**F. Prior-work distance.** Nearest Prometheus family: M-7 / M-9. Nearest rescue trap:
`REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`.

**G. Decision consequence.** Unreachable, and the family is adjacent to a binding rejection.

**H. Researcher freedom.** Cascade definition, depth threshold, and horizon all free.

**I. Evidence posture.** No path.

**J. Cost and proportionality.** Not proportionate.

**K. Strongest case against proceeding.** Even the bounded WS liquidation feed publishes only the largest
order per second, so a "cascade" could never be measured completely; combining an incomplete event feed
with an absent book state cannot identify anything.

**L. Disposition.** `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED`

---

### Pair C×F — liquidity and order-book state × cross-market and contextual state

#### I-CF-1 — Market-wide liquidity state as a moderator of own-symbol liquidity

**A. Identity.** `I-CF-1`; C×F; commonality in liquidity. *Does the market-wide liquidity state change
what own-symbol liquidity implies?*

**B. Mechanism interaction.** Mechanism A: own-symbol liquidity varies with own-symbol flow and
volatility. Mechanism B: a common funding or risk-appetite factor moves liquidity across instruments.
Joint claim: own-symbol liquidity decomposes into a common and an idiosyncratic part with different
implications, and only the joint state separates them. External source: **X5 (Hasbrouck & Seppi 2001)**,
which finds that liquidity proxies help explain time variation in trade impacts while the common factors
in those proxies are relatively small — a nuance that itself requires the joint measurement.

**C. Observable implication.** A common liquidity factor and its explanatory share for own-symbol trade
impact. Competing explanations: common volatility rather than common liquidity. Contemporaneous.
Structural.

**D. Data requirements.** Layer C for multiple symbols: spread and depth series — **absent for every
symbol**. No reserve.

**E. Identification.** `COMPUTABLE` no. `IDENTIFIED` moderate. `SCIENTIFICALLY_INFORMATIVE` moderate.
`DECISION_RELEVANT` no.

**F. Prior-work distance.** Nearest Prometheus family: M-1 through M-4 extended cross-symbol; §7.B
adjacency on the cross-symbol construction.

**G. Decision consequence.** Unreachable.

**H. Researcher freedom.** Moot.

**I. Evidence posture.** No path; would require multi-symbol prospective depth capture, a strictly larger
version of an already-futile acquisition.

**J. Cost and proportionality.** Not proportionate.

**K. Strongest case against proceeding.** It multiplies the single-symbol depth block by the number of
symbols.

**L. Disposition.** `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED`

#### I-CF-2 — Clock position as a moderator of liquidity provision

**A. Identity.** `I-CF-2`; C×F; intraday liquidity periodicity. *Does the position within the clock change
the spread and depth that liquidity providers post?*

**B. Mechanism interaction.** Mechanism A: liquidity providers set quotes against expected adverse
selection. Mechanism B: informed and discretionary liquidity traders concentrate at predictable times.
Joint claim, from X2: the concentration is endogenous, so the liquidity consequence of a clock interval is
determined by who has chosen to trade in it. External sources: **X2 (Admati & Pfleiderer 1988)**, **X10
(Andersen & Bollerslev 1997)**, **X11** for the venue-specific periodic pattern.

**C. Observable implication.** Spread and depth by clock bin. Competing explanations: exchange maintenance
windows; funding settlement; regional session overlap. Contemporaneous. Structural.

**D. Data requirements.** Layer C: quote and depth series — **absent**. Layer F: the clock — free. No
reserve.

**E. Identification.** `COMPUTABLE` no. `IDENTIFIED` moderate. `SCIENTIFICALLY_INFORMATIVE` moderate.
`DECISION_RELEVANT` no — the natural consumer is execution timing, which is prohibited.

**F. Prior-work distance.** Nearest Prometheus family: M-1 / M-2 conditioned on CF-3's calendar. Nearest
cooled-down families: §7.D and §7.E.

**G. Decision consequence.** Unreachable, and its consumer would be prohibited even if reachable.

**H. Researcher freedom.** Bin structure free; on a 24/7 venue X2's session anchor does not exist.

**I. Evidence posture.** No path.

**J. Cost and proportionality.** Not proportionate.

**K. Strongest case against proceeding.** The moderated quantity is absent, and the only reason to want it
is a use the project may not make.

**L. Disposition.** `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED`

---

### Pair D×E — perpetual anchoring and contract state × positioning and forced-flow state

#### I-DE-1 — Positioning direction as a moderator of funding-pressure meaning

**A. Identity.** `I-DE-1`; D×E; funding × open interest. *Does funding pressure mean something different
when outstanding positioning is expanding rather than contracting?*

**B. Mechanism interaction.** Mechanism A: the funding rate is the price paid to hold the crowded side.
Mechanism B: open interest measures whether that side is being built or unwound. Joint claim: identical
funding readings carry opposite information depending on the positioning trajectory — high funding with
expanding open interest is crowding, high funding with contracting open interest is an unwind under
constraint. Neither leg alone identifies it: funding is a price and open interest is a quantity, and only
the pair distinguishes a demand shift from a supply withdrawal. External sources: **X8 (Gârleanu &
Pedersen 2011)** for the margin-constraint-to-basis channel; **S8** for the attribution of carry variation
to trend-chasing demand and limited arbitrage capital; **M-12** in the committed map, which already names
this exact interaction.

**C. Observable implication.** Funding level and change interacted with open-interest change; the
crowding and unwind regimes predicted to differ in persistence and in subsequent basis behaviour.
Competing explanations: funding and open interest are jointly driven by price trend; exchange
risk-parameter changes shift both. Contemporaneous with a predictive form. Structural.

**D. Data requirements.** Layer D: funding history — **held**, `AVAILABLE_NON_RESERVE`. Layer E:
open-interest history over the same window — **`HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE`**, 30-day
retention, no back-fill possible. Settlement-to-bucket alignment would be required. No reserve.

**E. Identification.** `COMPUTABLE` **no**. `IDENTIFIED` moderate to strong — the interaction is
well-posed and the two legs are genuinely different objects. `SCIENTIFICALLY_INFORMATIVE` yes.
`DECISION_RELEVANT` low to moderate; the natural consumer under current governance is a context lens, and
§7.C restricts derivatives context to exactly that.

**F. Prior-work distance.** Nearest Prometheus family: **M-12**, verbatim. Nearest retained verdict:
**D1-A**. Nearest cooled-down family: **§7.C**, `CONDITIONAL_ONLY / HIGH_D1-A_RESCUE_RISK`. Nearest
rescue trap: any directional reading. Structural distinction from M-12: none — this *is* M-12, and M-12 is
already recorded as an interaction family "not yet authorised". Reason a claimed distinction would fail:
naming an already-enumerated family is not discovery.

**G. Decision consequence.** Unreachable on admissible data. Legitimate current consumer would have been
narrow. Self-created: no.

**H. Researcher freedom.** Moot, but note that the funding threshold, the OI-change window, and the
regime boundaries are all free, and that Phase 4as M-12 already records sample-size collapse at
funding-event granularity and high interaction-overfitting risk.

**I. Evidence posture.** The funding leg is free and on disk; the positioning leg is permanently gone for
the study window. Acquisition pressure structurally futile for the historical question. Reserve pressure
none.

**J. Cost and proportionality.** Not proportionate given an unobtainable leg.

**K. Strongest case against proceeding.** The interaction is real, is already in the project's own
mechanism map as M-12, and has an unrecoverable moderator. The half that is available — funding alone —
is NL-C2's territory, and pursuing it under an interaction label would be that candidate's reopening
rather than a new family.

**L. Disposition.** `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED`

#### I-DE-2 — Trader-composition ratios as a moderator of funding interpretation

**A. Identity.** `I-DE-2`; D×E; funding × long-short composition. *Does the distribution of positioning
across trader classes change what a funding reading implies?*

**B. Mechanism interaction.** Mechanism A: funding prices the aggregate imbalance. Mechanism B:
top-trader and global long-short ratios describe who holds it. Joint claim: the same funding level means
something different when the crowded side is held by large accounts than when it is held by retail.
External source: S8 on trend-chasing demand as a driver, with the top/global ratio split as the natural
observable; no source located in this phase makes the class-split claim for crypto perpetuals directly.

**C. Observable implication.** Funding interacted with the top-versus-global ratio gap. Competing
explanations: the ratios are exchange-defined constructs whose account classification is not published.
Contemporaneous. Structural.

**D. Data requirements.** Layer D: held. Layer E: top-trader long/short account and position ratios and
the global long/short account ratio — all **30-day retention**, therefore
`HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` for 2024. No reserve.

**E. Identification.** `COMPUTABLE` no. `IDENTIFIED` weak — the account-class definitions are not
externally documented in a way that supports a mechanism claim. `SCIENTIFICALLY_INFORMATIVE` low.
`DECISION_RELEVANT` no.

**F. Prior-work distance.** Nearest Prometheus family: M-11 / M-12 context lens; the committed Phase 4at
§6.11–§6.13 entries mark these as context-only under the D1-A precedent.

**G. Decision consequence.** Unreachable, with a weak claim even if reachable.

**H. Researcher freedom.** Ratio choice, period bucket, and interaction form all free.

**I. Evidence posture.** No path for the window.

**J. Cost and proportionality.** Not proportionate.

**K. Strongest case against proceeding.** The moderating series is both unavailable and weakly grounded:
no primary source located here establishes what the exchange's account classes mean as a mechanism.

**L. Disposition.** `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED`

#### I-DE-3 — Funding as a standalone stand-in for the positioning leg

**A. Identity.** `I-DE-3`; D×E; positioning inferred from funding. *Can the positioning leg of any D×E
interaction be replaced by funding itself?*

**B. Mechanism interaction.** None asserted. The card exists because I-DE-1 and I-DE-2 both generate
pressure toward it, and the atlas must dispose of it explicitly.

**C. Observable implication.** Whatever funding computes — which is a price, not a quantity.

**D. Data requirements.** Funding history, held. That availability is the hazard.

**E. Identification.** `COMPUTABLE` yes. `IDENTIFIED` **no** — funding measures the price of holding the
crowded side, not the size of it, and the whole content of I-DE-1 is the distinction between the two.
`SCIENTIFICALLY_INFORMATIVE` no. `DECISION_RELEVANT` no.

**F. Prior-work distance.** Nearest rescue trap: **D1-A**, which used funding as a standalone signal and
reached MECHANISM PASS / FRAMEWORK FAIL. Nearest binding rejection:
`REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`, whose reasoning — an unverifiable inference of an
unobservable state from an available series — transfers exactly.

**G. Decision consequence.** A positioning claim that cannot be checked against positioning data.

**H. Researcher freedom.** Unbounded.

**I. Evidence posture.** Non-reserve in form; illegitimate in substance.

**J. Cost and proportionality.** Cheap and corrosive.

**K. Strongest case against proceeding.** The authorization's §16 example set is directly on point —
*unsigned volume is not open interest* — and funding is not open interest either. Collapsing a two-leg
interaction onto its available leg does not preserve the interaction; it deletes it.

**L. Disposition.** `PROXY_DEPENDENT__REJECT`

---

### Pair D×F — perpetual anchoring and contract state × cross-market and contextual state

#### I-DF-1 — Cross-symbol funding dispersion as a moderator of own-symbol funding meaning

**A. Identity.** `I-DF-1`; D×F; common versus idiosyncratic funding. *Does the market-wide funding state
change what one symbol's funding implies about its own frictions?*

**B. Mechanism interaction.** Mechanism A: a symbol's funding reflects its own premium and therefore its
own limits to arbitrage. Mechanism B: arbitrage capital is shared across the venue, so scarcity moves all
symbols together — **S6 reports that crypto deviations comove across currencies**, and **S8 attributes
carry variation mainly to convenience yields and limited arbitrage capital**, a common factor. Joint
claim: only the cross-symbol state separates a symbol-specific convenience yield from a market-wide
capital constraint, and neither leg does so alone. This is a genuine qualifying interaction.

**C. Observable implication.** A common funding factor across the five core symbols and the residual
idiosyncratic component, with the common component predicted to load on venue-wide stress. Competing
explanations: the five symbols share a directional beta, so common funding may simply be common trend;
each symbol's clamp and cap parameters differ, so censoring differs across symbols in ways that mimic a
factor. Contemporaneous. Structural.

**D. Data requirements.** Layer D and F: funding history for BTCUSDT, ETHUSDT, ADA, SOL, XRP — **all on
disk**, `AVAILABLE_NON_RESERVE`; optionally multi-symbol klines volume for the market-wide activity leg,
also on disk. Settlement-time alignment across symbols. **No acquisition. No reserve.** Provenance
uncertainty: per-symbol 2024 cap and interest-term parameters are unestablished, and the caps differ
between major and non-major contracts, which directly affects cross-symbol comparability.

**E. Identification.** `COMPUTABLE` **yes** — this is the only two-way family in the atlas whose theory is
current, whose interaction form is genuine, and whose **both legs are on disk**. `IDENTIFIED` weak to
moderate — five series, heterogeneous clamp parameters, and an unresolved cap history.
`SCIENTIFICALLY_INFORMATIVE` moderate. `DECISION_RELEVANT` low.

**F. Prior-work distance.** Nearest Prometheus family: **NL-C2**, which is single-symbol BTCUSDT funding
read as a friction bound and which is unselected, unranked, un-cleared, and awaiting an independent review
that has not occurred. Nearest cooled-down families: **§7.C** (`HIGH_D1-A_RESCUE_RISK`) on the funding
lane and **§7.B** on the cross-symbol construction, whose blocked actions include **symbol-universe
expansion** by name. Nearest retained verdict: D1-A. Structural distinction claimed: the object is a
dispersion statistic, not a bound on one symbol. **Reason the distinction fails:** the data family is
identical, the mechanism source is NL-C2's own source set, and the only change is the symbol universe —
which M0 §6 lists explicitly as a forbidden post-null adjustment and which §15 of this authorization names
as insufficient to create a new mechanism.

**G. Decision consequence.** **Pass:** would be read as evidence that the funding lane is more tractable
than NL-C2's card concedes — advancing an unreviewed candidate through a side door. **Fail:** would
pre-empt the independent review NL-C2 was made conditional on. **Invalid:** recorded. Legitimate current
consumer: **none that does not run through NL-C2**. Self-created: partly.

**H. Researcher freedom.** Forced: settlement cadence, dead-zone half-width, and the cap *rule* — though
not the 2024 cap *values*. Free: symbol set, dispersion statistic, factor count, window, activity measure,
and whether cap-binding settlements are included. Contamination: the author has read the NL-C2 card,
including its concession that a well-arbitraged flagship perpetual should spend most settlements pinned at
the interest term.

**I. Evidence posture.** Fully non-reserve; the funding series is not part of either v002 reserve
envelope, so a confirmation argument would have no honest claim on them. Acquisition pressure none.

**J. Cost and proportionality.** Engineering low; documentation high; **governance very high**, because the
phase's dominant burden would be demonstrating that it is not a symbol-universe expansion of an unreviewed
candidate in the project's most rescue-prone lane.

**K. Strongest case against proceeding.** Its admissibility is precisely what makes it the atlas's most
dangerous entry. It is the cheapest available way to generate a positive-looking funding result before the
independent review that NL-C2 requires, using a symbol-universe expansion that M0 §6 forbids for cooled-down
families and that §7.B blocked by name after a `NOT_SUPPORTED` verdict on this exact five-symbol universe.
The project's own record shows that the moment a positive result exists, pressure follows.

**L. Disposition.** `HIGH_RESCUE_RISK__DOES_NOT_SURVIVE`

#### I-DF-2 — Calendar availability of arbitrage capital as a moderator of funding persistence

**A. Identity.** `I-DF-2`; D×F; weekday/weekend capital availability. *Does the traditional-market calendar
change the persistence of funding deviations on a 24/7 venue?*

**B. Mechanism interaction.** Mechanism A: closing a perpetual-versus-spot deviation requires
balance-sheet capacity. Mechanism B: that capacity may be unevenly available across the traditional
banking and settlement calendar even though the crypto venue never closes. Joint claim: deviations should
persist longer when capital is harder to mobilize. External source: **none located at primary-source
standard.** S8's limited-arbitrage-capital attribution is at the level of a common factor, not a calendar
mechanism; X8 concerns margin constraints, not calendar availability; and the targeted search returned
only secondary and vendor material, which under §5.4 carries no substantive claim.

**C. Observable implication.** Funding persistence by weekday and weekend. Competing explanations: crypto
volume itself is calendar-seasonal; the funding cadence is fixed and unrelated to the banking calendar.
Contemporaneous. Descriptive.

**D. Data requirements.** Funding history on disk plus a free calendar. Both `AVAILABLE_NON_RESERVE`.

**E. Identification.** `COMPUTABLE` yes. `IDENTIFIED` **no** — without a primary source establishing the
capital-availability channel for a 24/7 crypto venue, a weekday effect identifies a calendar regularity,
not a mechanism. `SCIENTIFICALLY_INFORMATIVE` low. `DECISION_RELEVANT` no.

**F. Prior-work distance.** Nearest Prometheus family: **CF-3**'s calendar leg. Nearest rescue trap: NL-C2.

**G. Decision consequence.** Pass would be an unexplained regularity; fail would close nothing.
Legitimate current consumer: none.

**H. Researcher freedom.** Calendar partition, persistence estimator, and window all free.

**I. Evidence posture.** Non-reserve feasible; irrelevant.

**J. Cost and proportionality.** Low cost, negligible gain.

**K. Strongest case against proceeding.** The atlas requires a *mechanism* source, not a plausible story.
This card has an available observable and no primary theory to make it an interaction rather than a
correlation, and the honest response to that is to record the gap rather than to promote the family on a
weaker source.

**L. Disposition.** `INSUFFICIENT_PRIMARY_SOURCE_OR_REPOSITORY_EVIDENCE`

#### I-DF-3 — Composite index state as the anchoring target for funding

**A. Identity.** `I-DF-3`; D×F; funding × premium or index state. *Does the composite spot index state
change what the funding rate implies about the perpetual's displacement?* — the mandatory starting
interaction "funding × premium or index state".

**B. Mechanism interaction.** Mechanism A: funding is a clamped transform of the premium index (S9).
Mechanism B: the premium index is the perpetual's impact prices measured **against a composite index of
spot venues** — a cross-market object. Joint claim: funding is uninterpretable without the anchoring
target, because the same funding value corresponds to different economic displacements depending on the
index's own behaviour; and the perpetual price equals a risk-neutral expectation of spot sampled at a
random time reflecting anchoring intensity (S7). Neither leg alone: funding without the index is a
censored scalar; the index without the perpetual is a spot composite. External sources: **S6, S7, S9**.

**C. Observable implication.** The recovered premium against the index level and its own volatility.
Competing explanations: index-composition changes across venues; S8's convenience-yield attribution.
Contemporaneous. Structural.

**D. Data requirements.** Layer D: funding history — held. Layer D/F: **index-price klines or
premium-index klines** — `ARCHIVE_AVAILABLE_NOT_ACQUIRED`. Acquisition required and **not authorized**.
No reserve. Provenance uncertainty: the composite index is not a per-venue tape, and its constituent
venue set for 2024 is not established here.

**E. Identification.** `COMPUTABLE` **no** on held data — this is precisely NL-C2's "extended form",
which its own card records as blocking without an authorized acquisition. `IDENTIFIED` moderate.
`SCIENTIFICALLY_INFORMATIVE` moderate. `DECISION_RELEVANT` low.

**F. Prior-work distance.** Nearest Prometheus family: **NL-C2 extended form**, verbatim. Structural
distinction: none.

**G. Decision consequence.** Pass and fail both belong to NL-C2's unreviewed question. Legitimate current
consumer: at most the acquisition-review question, recorded in §18 without the experiment.

**H. Researcher freedom.** Alignment interval and premium summary free; the formula itself is forced.

**I. Evidence posture.** Requires acquisition; no reserve pressure.

**J. Cost and proportionality.** Acquisition cost moderate; governance cost high; gain confined to an
unreviewed candidate.

**K. Strongest case against proceeding.** It is NL-C2's own blocked extension, and promoting it here would
authorize by atlas what the authorization forbids by name.

**L. Disposition.** `ARCHIVE_AVAILABLE_NOT_ACQUIRED__NO_ACQUISITION_AUTHORIZED`

---

### Pair E×F — positioning and forced-flow state × cross-market and contextual state

#### I-EF-1 — Market-wide deleveraging as a moderator of own-symbol positioning

**A. Identity.** `I-EF-1`; E×F; common deleveraging. *Does the market-wide deleveraging state change what
own-symbol positioning change implies?*

**B. Mechanism interaction.** Mechanism A: own-symbol open interest falls when positions close. Mechanism
B: a venue-wide margin shock closes positions everywhere at once. Joint claim: an idiosyncratic unwind and
a participation in a venue-wide deleveraging are different events with different consequences, and only
the cross-symbol state distinguishes them. External sources: **X7** for the venue-wide margin channel;
**X5** for the commonality framing.

**C. Observable implication.** Own-symbol open-interest change decomposed into common and idiosyncratic
parts. Competing explanations: common price trend. Contemporaneous. Structural.

**D. Data requirements.** Layer E across symbols: open-interest histories — **all 30-day-retained,
therefore `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` for 2024**; or liquidation tapes, which have no
archive. No reserve.

**E. Identification.** `COMPUTABLE` no. `IDENTIFIED` moderate. `SCIENTIFICALLY_INFORMATIVE` moderate.
`DECISION_RELEVANT` no.

**F. Prior-work distance.** Nearest Prometheus family: M-9 / M-11 extended cross-symbol; §7.B adjacency on
the cross-symbol construction.

**G. Decision consequence.** Unreachable.

**H. Researcher freedom.** Moot.

**I. Evidence posture.** No path for the window on any symbol.

**J. Cost and proportionality.** Not proportionate.

**K. Strongest case against proceeding.** It multiplies an unrecoverable single-symbol series by the
symbol count.

**L. Disposition.** `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED`

#### I-EF-2 — Settlement and session timing as a moderator of positioning change

**A. Identity.** `I-EF-2`; E×F; scheduled-flow positioning. *Does the funding-settlement or session clock
change how outstanding positioning evolves?*

**B. Mechanism interaction.** Mechanism A: funding settles at fixed UTC hours, creating a scheduled cash
flow. Mechanism B: participants adjust position size to capture or avoid it. Joint claim: open-interest
change should show a deterministic pattern around settlement whose amplitude scales with the payment at
stake. External sources: **S9** for the settlement identity; **X2** for discretionary concentration.

**C. Observable implication.** Open-interest change bracketing settlement hours. Competing explanations:
session overlap; the same effect appearing in volume rather than in positioning. Contemporaneous.
Structural.

**D. Data requirements.** Layer E: open-interest history at 5m–1h buckets over the window —
`HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` for 2024. Layer F: clock, free. No reserve.

**E. Identification.** `COMPUTABLE` no. `IDENTIFIED` moderate. `SCIENTIFICALLY_INFORMATIVE` moderate.
`DECISION_RELEVANT` no.

**F. Prior-work distance.** Nearest Prometheus family: M-11 / M-12 with CF-3's calendar. Nearest
cooled-down family: §7.C.

**G. Decision consequence.** Unreachable; and the volume-side analogue that *is* reachable is I-BD-1,
which is CF-3.

**H. Researcher freedom.** Bracket width and bucket period free.

**I. Evidence posture.** No path for the window.

**J. Cost and proportionality.** Not proportionate.

**K. Strongest case against proceeding.** The positioning leg is unavailable, and the available substitute
is an already-shortlisted, already-unselected family.

**L. Disposition.** `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED`

## 11. Theory-required three-way interaction cards

Five three-way families, all below the ten-card ceiling. **No third variable was added to create
novelty.** A family is admitted here only where the external source requires all three legs jointly; where
a third leg would merely condition a two-way result, the family remains in §10 and the third variable is
recorded as a context variable under §15 of the authorization.

Zero survivors is an acceptable outcome for this section and is the outcome reached.

---

### T-1 — Funding × open interest × aggressive flow

**A. Identity.** `T-1`; D×E×B; crowding, capacity, and pressure jointly. *Does the meaning of aggressive
flow depend jointly on the price of holding the crowded side and on whether that side is being built or
unwound?*

**B. Mechanism interaction.** Mechanism A (D): funding prices the crowded side. Mechanism B (E): open
interest measures the size and trajectory of it. Mechanism C (B): aggressive flow is the pressure applied
now. **Why all three are required:** funding without positioning cannot distinguish a demand shift from a
supply withdrawal (I-DE-1); positioning without flow cannot say whether the change is being driven or
absorbed; flow without either cannot say whether it is entering a crowded or an empty book of positions.
X7's margin channel and X8's margin-to-basis channel both require a constraint state *and* a flow to
produce the amplification they predict, and X3 supplies the empirical form in which a positioning
moderator conditions a flow shock. External sources: **X3, X7, X8, S8**; and **M-13** in the committed
Prometheus map, which already names this exact triple.

**C. Observable implication.** Flow consequence measured in three-way strata of funding sign/magnitude and
open-interest trajectory, with amplification predicted where flow pushes into a crowded side under
binding constraints. Competing explanations: all three legs load on a common price trend; the strata
multiply thin. Predictive. Causal in claim.

**D. Data requirements.** B: aggressor columns — held. D: funding — held. **E: open-interest history —
`HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` for 2024, unrecoverable.** No reserve.

**E. Identification.** `COMPUTABLE` **no**. `IDENTIFIED` moderate at best — three-way strata over an
8-hour funding cadence collapse the sample, which Phase 4as M-13 already flags as combinatorial
overfitting risk. `SCIENTIFICALLY_INFORMATIVE` moderate. `DECISION_RELEVANT` low; under §7.C the only
admissible use is a context lens.

**F. Prior-work distance.** Nearest Prometheus family: **M-13**, verbatim, recorded as "not yet
authorised". Nearest retained verdict: D1-A. Nearest rescue trap: a regime classifier over the depleted
lanes, which Phase 4as M-14 flags against the G1 precedent. Structural distinction: none — naming an
already-enumerated triple is not discovery.

**G. Decision consequence.** Unreachable. Self-created: no.

**H. Researcher freedom.** Moot, and severe: three thresholds, three windows, and a stratification scheme,
with sample-size collapse at funding-event granularity.

**I. Evidence posture.** No path; the middle leg cannot be reconstructed.

**J. Cost and proportionality.** Not proportionate.

**K. Strongest case against proceeding.** It is the project's own M-13 with an unobtainable middle leg and
an overfitting profile the committed record already warned about.

**L. Disposition.** `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED`

---

### T-2 — Spread × depth × aggressive flow

**A. Identity.** `T-2`; C×C×B — formally a two-layer triple in which the liquidity layer contributes two
structurally distinct legs; recorded here because the source requires all three. *Does the price
consequence of aggressive flow depend jointly on the cost of crossing and on the quantity available at the
touch?*

**B. Mechanism interaction.** Mechanism A: the spread sets the immediate cost of the first unit. Mechanism
B: depth sets the marginal cost of every subsequent unit. Mechanism C: flow is the quantity demanded.
**Why all three:** X9 finds the OFI-to-price slope inversely proportional to depth, and **X5 finds that
both the bid–ask spread and the quote sizes help explain time variation in trade impacts** — two separate
liquidity legs, not one. Collapsing spread and depth into a single "liquidity" leg loses the distinction
that makes the impact function non-linear. External sources: **X1, X5, X9**; and **M-14** in the committed
map.

**C. Observable implication.** An impact function whose intercept scales with spread and whose slope
scales inversely with depth. Competing explanations: both liquidity legs respond endogenously to the flow.
Contemporaneous. Causal in claim.

**D. Data requirements.** B: held. **C (both legs): `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` /
`PROSPECTIVE_ONLY`.** No reserve.

**E. Identification.** `COMPUTABLE` **no**. `IDENTIFIED` strong in principle.
`SCIENTIFICALLY_INFORMATIVE` yes. `DECISION_RELEVANT` moderate — it is the interaction that would speak
most directly to M0.5.

**F. Prior-work distance.** Nearest Prometheus family: **M-14**, "spread / depth / flow regime
interaction", recorded as admissible only after a primary mechanism is independently validated. Nearest
stopped arc: the ToB arc.

**G. Decision consequence.** Unreachable. Self-created: no — this is a genuinely open question.

**H. Researcher freedom.** Moot; M-14 is already recorded as the project's most overfitting-prone research
style, with the G1 regime-gate failure as precedent.

**I. Evidence posture.** No path; prospective capture is regime-non-comparable to the substrate.

**J. Cost and proportionality.** Not proportionate.

**K. Strongest case against proceeding.** Two of the three legs are permanently unavailable for the
project's substrate, and the committed record already conditions this family on a prior validation that
cannot itself be performed.

**L. Disposition.** `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED`

---

### T-3 — Cross-symbol stress × own-symbol liquidity × own-symbol flow

**A. Identity.** `T-3`; F×C×B; commonality-conditioned impact. *Does the price consequence of own-symbol
flow depend jointly on own-symbol liquidity and on whether the market as a whole is under stress?*

**B. Mechanism interaction.** Mechanism A (F): a venue-wide stress state withdraws shared liquidity
provision. Mechanism B (C): own-symbol liquidity mediates own impact. Mechanism C (B): own flow is the
input. **Why all three:** X5 establishes that flow and liquidity both have common components and that
liquidity proxies explain time variation in impact, so the impact of own flow is conditioned by own
liquidity *and* by the common state; X7's spiral supplies the reason the common state is not merely a
correlate. External sources: **X5, X7**.

**C. Observable implication.** Impact coefficients that vary with own liquidity and shift further in
common-stress episodes. Competing explanations: common information arrival. Contemporaneous. Causal in
claim.

**D. Data requirements.** F: multi-symbol flow or liquidity — `ARCHIVE_AVAILABLE_NOT_ACQUIRED` at best for
flow, unavailable for liquidity. **C: unavailable.** B: held. No reserve.

**E. Identification.** `COMPUTABLE` **no**. `IDENTIFIED` moderate. `SCIENTIFICALLY_INFORMATIVE` moderate.
`DECISION_RELEVANT` low.

**F. Prior-work distance.** Nearest Prometheus family: M-14 extended cross-symbol; CF-2 on the
cross-symbol leg; §7.B and §7.D adjacency.

**G. Decision consequence.** Unreachable.

**H. Researcher freedom.** Moot; a stress-episode definition is the archetypal free parameter.

**I. Evidence posture.** No path; two legs blocked, one of them across every symbol.

**J. Cost and proportionality.** Not proportionate.

**K. Strongest case against proceeding.** It combines the atlas's two worst data blocks and adds a
free-parameter stress definition on top.

**L. Disposition.** `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED`

---

### T-4 — Trade burst × replenishment state × subsequent price behaviour

**A. Identity.** `T-4`; B×C×A; resilience-conditioned burst consequence. *Does what follows a burst of
aggressive trading depend jointly on the burst's size and on whether the book replenished?*

**B. Mechanism interaction.** Mechanism A (B): the burst consumes liquidity. Mechanism B (C): the book
either replenishes or does not — X6 finds that in **over 60% of cases it does not replenish reliably**,
and when it does the half-life is around 20 seconds. Mechanism C (A): the subsequent price path.
**Why all three:** the burst alone is identical on the tape in both regimes; the replenishment state alone
says nothing about price; and the price path alone cannot attribute itself to absorption or to signalling.
The three-way structure is what distinguishes an absorbed burst from an informative one. External source:
**X6 (Large 2007)**, with **X4 (Dufour & Engle 2000)** supplying the complementary finding that impact
rises as inter-trade duration falls.

**C. Observable implication.** Differential forward price behaviour across replenished and depleted
post-burst states. Competing explanations: replenishment by quoting that never intended to be consumed;
spoofing; a common driver of burst and non-replenishment. Predictive. Causal in claim.

**D. Data requirements.** B and A: held. **C: `PROSPECTIVE_ONLY`; no historical archive.** Sub-second
synchronization of trades to book updates would be required. No reserve.

**E. Identification.** `COMPUTABLE` **no**. `IDENTIFIED` strong in principle. `SCIENTIFICALLY_INFORMATIVE`
yes. `DECISION_RELEVANT` low — the natural consumer is execution timing, which is prohibited.

**F. Prior-work distance.** Nearest Prometheus family: **M-7 / M-8**, recorded as admissible only after
M-3 / M-5 are studied. Nearest rescue trap: substituting "no subsequent move" for "replenished", which is
I-BC-4 and is rejected.

**G. Decision consequence.** Unreachable, and its consumer would be prohibited if it were not.

**H. Researcher freedom.** Moot; the burst definition is itself a research artefact, as Phase 4as M-7
already records.

**I. Evidence posture.** No path.

**J. Cost and proportionality.** Not proportionate.

**K. Strongest case against proceeding.** The middle leg is the entire content of the interaction and it
does not exist historically; without it the family degenerates into the already-tested burst features.

**L. Disposition.** `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED`

---

### T-5 — Trade duration × trade impact × informed-participant presence

**A. Identity.** `T-5`; B×C×B; time-conditioned impact. *Does the price impact of a trade depend jointly
on how long it has been since the last trade and on the presence of informed participants that short
durations signal?* — the mandatory starting interaction "trade duration × liquidity recovery".

**B. Mechanism interaction.** Mechanism A: inter-trade duration measures market activity intensity.
Mechanism B: the price impact of a trade is a quote revision. Mechanism C: informed-participant presence
is what links them. **Why all three:** X4 finds that as duration falls, **the price impact of trades, the
speed of price adjustment, and the positive autocorrelation of signed trades all rise together**, and
interprets the joint movement as increased informed presence and therefore reduced liquidity. Duration
alone is a timing statistic; impact alone is a liquidity statistic; only jointly do they identify the
informed-presence channel that X4 asserts. External source: **X4 (Dufour & Engle 2000)**, whose full text
could not be retrieved (§5.7) and whose claims are used only at the level verified.

**C. Observable implication.** Impact coefficients in a Hasbrouck-style price–trade VAR, conditioned on
duration. Competing explanations: durations and volatility share a common driver; the impact measure is
contaminated by bounce if a trade price replaces the midpoint. Contemporaneous with dynamics. Causal in
claim.

**D. Data requirements.** Duration: derivable from held aggTrades timestamps. **Impact: requires a quote
midpoint series — `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE`.** No reserve.

**E. Identification.** `COMPUTABLE` **no**. `IDENTIFIED` moderate. `SCIENTIFICALLY_INFORMATIVE` moderate.
`DECISION_RELEVANT` low.

**F. Prior-work distance.** Nearest Prometheus family: AW candidate #11 (trade-burst / activity), merged
into CF-1; duration is the reciprocal face of arrival intensity, which Phase 4bn-BE recorded as **N-13**
duplication. Nearest stopped arc: **`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`** — substituting a
last-trade price for the midpoint reintroduces exactly the bounce question that arc could not resolve.
Structural distinction: the duration leg is genuinely not the CF-1 object. Reason it fails: the
*dependent* variable is unavailable, and the only available substitute is the one the stopped arc ruled
out.

**G. Decision consequence.** Unreachable. Self-created: no.

**H. Researcher freedom.** Moot; VAR lag order, duration conditioning, and impact horizon all free.

**I. Evidence posture.** No path for the impact leg.

**J. Cost and proportionality.** Not proportionate.

**K. Strongest case against proceeding.** Its dependent variable is a quote revision, and the project has a
committed lock stating that its quote source is inadmissible for this window. Building it on last-trade
prices would be the stopped arc's question under a new name.

**L. Disposition.** `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED`

## 12. Existing-family and stopped-arc overlap matrix

Every atlas family is mapped explicitly against the committed record. `—` means no material overlap.

| Family | Phase 4as M-family | CF / NL family | Stopped arc or binding rejection | Cooled-down family (M0 §7) | Retained verdict | Overlap verdict |
|---|---|---|---|---|---|---|
| I-AB-1 | M-6 | **CF-1 (exact)** | — | — | — | Total |
| I-AB-2 | M-6 | CF-1, CF-3 | `STOP_LONGHORIZON_ML_ARC` (via X11's directional half) | — | — | High |
| I-AC-1 | M-1, M-2 | NL-C1 | `STOP_TOB_..._DATA_INADMISSIBLE` | §7.D, §7.E | — | High (data), moderate (question) |
| I-AC-2 | — | **NL-C1 (exact + context variable)** | `STOP_TOB_...` | §7.D, §7.E | — | Total |
| I-AC-3 | — | AW #13 / BE N-05 | `STOP_TOB_...` (rescue-adjacent) | §7.D | — | Total |
| I-AD-1 | M-10 | **NL-C2 extended form** | — | §7.C | D1-A | High |
| I-AD-2 | M-10 | **NL-C2 (exact + context variable)** | — | §7.C | D1-A | Total |
| I-AD-3 | M-10 | — | — | §7.E | — | Moderate |
| I-AE-1 | **M-11** | CF-1 (outcome side) | — | §7.C | — | Moderate |
| I-AE-2 | **M-9** | AW #4 | **`REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`** | §7.D | — | Total |
| I-AF-1 | — | **CF-3**; BE N-06 | — | — | — | Total |
| I-AF-2 | — | CF-1 target, CF-2 adjacency | — | **§7.B** | — | Moderate |
| I-AF-3 | — | CF-2; BE N-09 | — | §7.B | — | High |
| I-BC-1 | **M-3, M-4, M-14** | AW #3 | `STOP_TOB_...` (same blocker) | §7.D | — | High (data) |
| I-BC-2 | M-5 | BE N-01 | `STOP_LONGHORIZON_ML_ARC` (flow leg materialized) | §7.D | — | High |
| I-BC-3 | **M-7, M-8** | AW #3 | — | §7.D | — | High |
| I-BC-4 | M-1…M-8 | — | **`REJECTED_AS_RESCUE_SHAPED_PROXY_...`** | §7.D | — | Total |
| I-BD-1 | M-10 | **CF-3 (exact)** | — | §7.C | D1-A | Total |
| I-BD-2 | M-10 | NL-C2 extended form | — | §7.C | **D1-A** | High |
| I-BD-3 | M-5, M-10 | — | `STOP_LONGHORIZON_ML_ARC` (forward target) | **§7.C** | **D1-A** | Total |
| I-BE-1 | **M-11, M-12** | CF-1 (outcome side) | — | §7.C | — | Moderate |
| I-BE-2 | **M-9** | AW #4 | **`REJECTED_AS_RESCUE_SHAPED_PROXY_...` (exact)** | §7.D | — | Total |
| I-BF-1 | M-5 | **CF-2 (same acquisition block)** | — | §7.B | — | High |
| I-BF-2 | M-6 | CF-1, CF-3 | `STOP_LONGHORIZON_ML_ARC` (via X11) | — | — | High |
| I-BF-3 | M-6 | CF-1 target, cross-sectional | **§7.B** | §7.B | — | Moderate |
| I-CD-1 | M-1, M-2 | NL-C2 | **`STOP_TOB_..._DATA_INADMISSIBLE` (side door)** | §7.D | — | Total |
| I-CD-2 | M-1, M-2 | NL-C2 extended form | `STOP_TOB_...` | §7.D, §7.C | — | High |
| I-CE-1 | **M-14, M-9** | — | — | §7.C, §7.D | — | Moderate |
| I-CE-2 | **M-7, M-9** | AW #4 | `REJECTED_AS_RESCUE_SHAPED_PROXY_...` | §7.D | — | High |
| I-CF-1 | M-1…M-4 | — | — | §7.B, §7.D | — | Moderate |
| I-CF-2 | M-1, M-2 | CF-3 calendar leg | — | §7.D, §7.E | — | Moderate |
| I-DE-1 | **M-12 (exact)** | — | — | **§7.C** | **D1-A** | Total |
| I-DE-2 | M-11, M-12 | — | — | §7.C | D1-A | High |
| I-DE-3 | M-10 | — | **`REJECTED_AS_RESCUE_SHAPED_PROXY_...`** (reasoning) | §7.C | **D1-A** | Total |
| I-DF-1 | M-10 | **NL-C2 + symbol-universe expansion** | — | **§7.B, §7.C** | D1-A | Total |
| I-DF-2 | M-10 | CF-3 calendar leg | — | §7.C | — | Moderate |
| I-DF-3 | M-10 | **NL-C2 extended form (exact)** | — | §7.C | — | Total |
| I-EF-1 | M-9, M-11 | — | — | §7.B, §7.C | — | Moderate |
| I-EF-2 | M-11, M-12 | CF-3 | — | §7.C | — | High |
| T-1 | **M-13 (exact)** | — | — | §7.C | D1-A | Total |
| T-2 | **M-14 (exact)** | — | `STOP_TOB_...` | §7.D | G1 (regime-gate precedent) | Total |
| T-3 | M-14 cross-symbol | CF-2 leg | — | §7.B, §7.D | — | High |
| T-4 | **M-7, M-8** | AW #11 → CF-1 | — | §7.D | — | High |
| T-5 | M-6 | AW #11 → CF-1; BE N-13 | **`STOP_TOB_...`** (impact leg) | §7.D | — | High |

**Reading of the matrix.** Of forty-four families, **eleven overlap totally** with a named committed
family, rejection, or candidate; a further fourteen overlap highly. The three families the project's own
mechanism map already records as interactions — **M-12, M-13, M-14** — reappear here as I-DE-1, T-1, and
T-2 respectively, and all three are blocked on layer C or layer E. Nothing in this atlas reopens, softens,
merges, or reinterprets any stopped arc, binding rejection, retained verdict, or cooled-down family.

## 13. Data-admissibility matrix

Each family is scored on whether each leg is admissible now, from committed records only.

| Family | Leg 1 status | Leg 2 (and 3) status | Both legs admissible now? | Acquisition would unblock? | Reserve implicated |
|---|---|---|---|---|---|
| I-AB-1 | `AVAILABLE_NON_RESERVE` | `AVAILABLE_NON_RESERVE` | **Yes** | n/a | No |
| I-AB-2 | `AVAILABLE_NON_RESERVE` | `AVAILABLE_NON_RESERVE` | **Yes** | n/a | No |
| I-AC-1 | `AVAILABLE_NON_RESERVE` | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` | No | **No** — prospective only, regime-non-comparable | No |
| I-AC-2 | `AVAILABLE_NON_RESERVE` | `AVAILABLE_NON_RESERVE` | **Yes** | n/a | No |
| I-AC-3 | `AVAILABLE_NON_RESERVE` | `AVAILABLE_NON_RESERVE` | **Yes** | n/a | No |
| I-AD-1 | `AVAILABLE_NON_RESERVE` | `ARCHIVE_AVAILABLE_NOT_ACQUIRED` | No | **Yes** | No |
| I-AD-2 | `AVAILABLE_NON_RESERVE` | `AVAILABLE_NON_RESERVE` | **Yes** | n/a | No |
| I-AD-3 | `AVAILABLE_NON_RESERVE` | `ARCHIVE_AVAILABLE_NOT_ACQUIRED` | No | **Yes** (Phase 3r §8 governed) | No |
| I-AE-1 | `AVAILABLE_NON_RESERVE` | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` | No | **No** — 30-day retention, unrecoverable | No |
| I-AE-2 | `AVAILABLE_NON_RESERVE` | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` | No | **No** | No |
| I-AF-1 | `AVAILABLE_NON_RESERVE` | `AVAILABLE_NON_RESERVE` (free calendar) | **Yes** | n/a | No |
| I-AF-2 | `AVAILABLE_NON_RESERVE` | `AVAILABLE_NON_RESERVE` | **Yes** | n/a | No |
| I-AF-3 | `AVAILABLE_NON_RESERVE` | `ARCHIVE_AVAILABLE_NOT_ACQUIRED` | No | **Yes** | No |
| I-BC-1 | `AVAILABLE_NON_RESERVE` | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` | No | **No** | No |
| I-BC-2 | `AVAILABLE_NON_RESERVE` | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` | No | **No** | No |
| I-BC-3 | `AVAILABLE_NON_RESERVE` | `PROSPECTIVE_ONLY` | No | **No** for the historical question | No |
| I-BC-4 | `AVAILABLE_NON_RESERVE` | proxy substitute | Yes, and that is the defect | n/a | No |
| I-BD-1 | `AVAILABLE_NON_RESERVE` | `AVAILABLE_NON_RESERVE` | **Yes** | n/a | No |
| I-BD-2 | `AVAILABLE_NON_RESERVE` | `ARCHIVE_AVAILABLE_NOT_ACQUIRED` | No | **Yes** | No |
| I-BD-3 | `AVAILABLE_NON_RESERVE` | `AVAILABLE_NON_RESERVE` | **Yes** | n/a | No |
| I-BE-1 | `AVAILABLE_NON_RESERVE` | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` | No | **No** — unrecoverable | No |
| I-BE-2 | `AVAILABLE_NON_RESERVE` | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` | No | **No** | No |
| I-BF-1 | `AVAILABLE_NON_RESERVE` | `ARCHIVE_AVAILABLE_NOT_ACQUIRED` | No | **Yes**, at material cost | No |
| I-BF-2 | `AVAILABLE_NON_RESERVE` | `AVAILABLE_NON_RESERVE` (free calendar) | **Yes** | n/a | No |
| I-BF-3 | `AVAILABLE_NON_RESERVE` | `AVAILABLE_NON_RESERVE` | **Yes** | n/a | No |
| I-CD-1 | `AVAILABLE_NON_RESERVE` | `UNKNOWN__DOCUMENTATION_REQUIRED` + inversion assumption | No | **No** | No |
| I-CD-2 | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` | `ARCHIVE_AVAILABLE_NOT_ACQUIRED` | No | **Partially** — one leg only | No |
| I-CE-1 | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` | No | **No** — both legs | No |
| I-CE-2 | `PROSPECTIVE_ONLY` | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` | No | **No** | No |
| I-CF-1 | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` (all symbols) | `AVAILABLE_NON_RESERVE` | No | **No** | No |
| I-CF-2 | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` | free calendar | No | **No** | No |
| I-DE-1 | `AVAILABLE_NON_RESERVE` | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` | No | **No** — unrecoverable | No |
| I-DE-2 | `AVAILABLE_NON_RESERVE` | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` | No | **No** | No |
| I-DE-3 | `AVAILABLE_NON_RESERVE` | proxy substitute | Yes, and that is the defect | n/a | No |
| I-DF-1 | `AVAILABLE_NON_RESERVE` | `AVAILABLE_NON_RESERVE` | **Yes** | n/a | No |
| I-DF-2 | `AVAILABLE_NON_RESERVE` | free calendar | **Yes** | n/a | No |
| I-DF-3 | `AVAILABLE_NON_RESERVE` | `ARCHIVE_AVAILABLE_NOT_ACQUIRED` | No | **Yes** | No |
| I-EF-1 | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` | No | **No** | No |
| I-EF-2 | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` | free calendar | No | **No** | No |
| T-1 | `AVAILABLE_NON_RESERVE` ×2 | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` | No | **No** | No |
| T-2 | `AVAILABLE_NON_RESERVE` | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` ×2 | No | **No** | No |
| T-3 | `AVAILABLE_NON_RESERVE` | blocked + unacquired | No | **No** | No |
| T-4 | `AVAILABLE_NON_RESERVE` ×2 | `PROSPECTIVE_ONLY` | No | **No** for the historical question | No |
| T-5 | `AVAILABLE_NON_RESERVE` | `HISTORICALLY_INADMISSIBLE_OR_UNAVAILABLE` | No | **No** | No |

**Counts.** Both legs admissible now: **13 of 44**. Blocked by an unrecoverable or prospective-only leg:
**19**. Blocked pending an unauthorized acquisition: **6**. Admissible only by substituting a prohibited
proxy: **2**. Blocked on documentation or an inversion assumption: **1**. Remaining families are counted
under the closest applicable heading above.

**No family in the atlas implicates any evidence reserve.** `PRE_V002_INTERNAL_HOLDOUT` is not proposed
for reuse as confirmation by any family; `V002_TERMINAL_WINDOW` and `V002_SEALED_TEST` are required by
none.

## 14. Proxy and identification failures

The following substitutions were considered and rejected. Each is recorded because a blocked family
generates pressure toward it, and because §16 of the authorization requires that a rejected interaction be
**rejected, not repaired**.

| # | Proposed stand-in | For the missing mechanism leg | Why the mapping is not established | Where it arose |
|---|---|---|---|---|
| P-1 | Aggressor imbalance, burst intensity, or size clustering | Forced liquidation / deleveraging | No admissible liquidation marker exists; the committed Phase 4bn-AX §12 audit records that informed trading, news response, ordinary inventory unwinding, and herding all produce the same tape signature | I-AE-2, I-BE-2, I-CE-2 |
| P-2 | Unsigned volume or trade count | Open interest | Volume is a flow and open interest is a stock; no theory or official identity maps one to the other. Named as prohibited by example in the authorization §16 | I-AE-1, I-BE-1, I-DE-1 |
| P-3 | High–low price range | Quoted spread ground truth | The range-based estimators estimate the **effective** spread under a model; they are not a measurement of the quoted spread, and S5's validation methodology requires quote data Prometheus cannot obtain. Named as prohibited by example in §16 | I-AC-1, I-BC-4, I-CD-2 |
| P-4 | Absence of a post-burst price move | Book replenishment / absorption | Absorption and information-free flow are observationally identical on the tape; X6's resiliency object is defined over book events, not over price outcomes | I-BC-3, I-BC-4, T-4 |
| P-5 | Inverse realized volatility | Market liquidity / depth | Volatility and liquidity are correlated but not identified by one another; using one as the other assumes the very interaction under test (I-AC-1) | I-BC-4, I-CE-1 |
| P-6 | Trade clustering | Metaorder identity | aggTrades carries no parent-order identity; recorded already as Phase 4bn-BE **N-07** | I-BC-4 |
| P-7 | Inverting the published funding/premium identity | Order-book depth state | The book-to-impact-price map is many-to-one, eight-hour-averaged, and clamp-censored; running it backwards substitutes a researcher-chosen book-shape assumption for data | I-CD-1 |
| P-8 | Funding rate | Positioning / open interest | Funding is the price of holding the crowded side, not its size; the entire content of the D×E interaction is the distinction between price and quantity | I-DE-3 |
| P-9 | Last-trade price change | Quote-midpoint revision (price impact) | Reintroduces the bid–ask bounce question that `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE` could not resolve | T-5, I-BC-1 |
| P-10 | Trade-size roundness | Participant class (algorithmic vs discretionary) | An inference from a size histogram with no venue-published mapping; additionally contaminated because insurance-fund and ADL trades are excluded from aggregation and their size profile is unknown | I-AB-2, I-BF-2 |

**No family was repaired by adding a second proxy**, and none is admitted on the ground that a proxy is
"good enough for a first look".

## 15. Researcher-freedom comparison

Every family was assessed for the full menu the authorization enumerates: horizons, windows, symbols,
thresholds, transformations, aggregation choices, state definitions, lag choices, feature families, model
families, comparison metrics, subgroup menus, and exclusion rules.

**What is forced, and by what.**

| Choice | Forced for which families | Forcing authority |
|---|---|---|
| Funding settlement cadence (8h at 00:00/08:00/16:00 UTC) | I-AD-2, I-BD-1, I-DF-1, I-DF-2, I-EF-2, T-1 | Official exchange design (S9) |
| Clamp dead-zone half-width (±0.05%) and the cap **rule** | I-AD-2, I-DF-1 | Official exchange design (S9) — note the 2024 cap **values** are not established |
| Frictionless no-arbitrage price and the `±C` bound | I-AD-1, I-CD-2, I-DF-3 | External theory (S6 Prop. 1 and 2) |
| Closed-form spread estimators | I-AC-2 | External theory (S1–S4) |
| Clock marks and UTC calendar | I-AF-1, I-BF-2, I-CF-2, I-DF-2, I-EF-2 | Deterministic; no data required |
| Sign of the depth-to-volatility and depth-to-impact effects | I-AE-1, I-BE-1, I-BC-1, T-2 | External theory (X1, X3, X9) — the *sign* is forced, not the functional form |
| CF-1 target, baseline, loss, horizon, cadence | I-AB-1 | Committed Prometheus preregistration (frozen, and consumed) |
| Feature-column prohibitions (`liquidation`, `funding`, `open_interest`, `order_book`, `mark_price`) | all | Committed source `FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS` |
| Block structure (UTC date/month) | all | Committed project convention |

**What remains free in every family.** Volatility estimator; activity window among {1s, 5s, 15s, 60s} and
beyond; interaction functional form; stratification boundaries; agreement or consistency tolerances;
symbol subset; factor count; shock-decomposition model; event and burst definitions; horizon; and
exclusion rules for cap-binding or invalid windows.

**Comparison across the 13 families whose legs are both admissible.**

| Family | Free-parameter count | Baseline externally forced? | Any threshold forced? | Contamination from known Prometheus outcomes | Clean preregistration possible? |
|---|---|---|---|---|---|
| I-AB-1 | Low (contract frozen) | Yes (HAR-RV) | Yes | **Maximal** — the result is public on `main` | **No** |
| I-AB-2 | High | No | No | Moderate | Form yes; principle no |
| I-AC-2 | Moderate | Partly (estimator over-identification) | No | Moderate (NL-C1 card, 8 bps reference) | Form yes; principle weak |
| I-AC-3 | High | No | No | Low | Form yes; principle no |
| I-AD-2 | Low–moderate | Yes (published formula) | Partly (dead zone) | Moderate (5 bps vs 8 bps proximity) | Yes |
| I-AF-1 | High | No | No | Moderate (CF-1 target) | Form yes; principle no |
| I-AF-2 | High | No | No | Low | Form yes; principle no |
| I-BC-4 | Unbounded | No | No | Low | **No** |
| I-BD-1 | Moderate | Partly (settlement hours) | No | Moderate (CF-3 record) | Form yes |
| I-BD-3 | High | No | No | Moderate (D1-A record) | Form yes; principle no |
| I-BF-2 | High | No | No | Moderate | Form yes; principle no |
| I-BF-3 | **Very high** | No | No | Low | Form yes; **principle no** |
| I-DE-3 | Unbounded | No | No | Moderate | **No** |
| I-DF-1 | Moderate–high | Partly (published constants) | Partly | Moderate–high (NL-C2 card) | Form yes; principle contested |
| I-DF-2 | Moderate | **No** | No | Low | Form yes; no mechanism to preregister |

**Finding.** Researcher freedom was assessed for every family and was **never the first binding ground**.
In every case a stronger ground — data inadmissibility, duplication, rescue risk, absent decision consumer,
or an unestablished proxy mapping — bound first. `REJECTED_RESEARCHER_FREEDOM` is therefore **not used as
a disposition anywhere in this atlas**, and that absence is recorded deliberately rather than filled by
forcing a family into the category. Researcher freedom nonetheless *compounds* the rejection in I-AB-2,
I-AC-3, I-AF-1, I-AF-2, I-BF-2, and especially **I-BF-3**, where the design could only ever be frozen
arbitrarily rather than on principle.

The atlas applied the authorization's test directly: *a candidate does not survive merely because choices
could be frozen; the question is whether the frozen choices would be principled or merely frozen
arbitrariness.* Of the thirteen dual-admissible families, only **I-AD-2** and **I-DF-1** have externally
forced constants at their core — and both are rejected on rescue grounds, not on freedom grounds.

## 16. Decision-consumer comparison

Each family was asked the four questions §17 of the authorization requires, separately.

| Family | What changes on pass | What changes on fail | On invalid | Legitimate current consumer | Self-created question? |
|---|---|---|---|---|---|
| I-AB-1 | Nothing — the result exists | Would contradict a merged result no rerun could revisit | n/a | **None** | Yes |
| I-AB-2 | Only via CF-1 reinterpretation — **forbidden** | Closes a question the card invented | Recorded | **None** | **Yes** |
| I-AC-1 | Would have narrowed the cost-realism record | Would have closed the spread-measurement question | — | Would have been the cost-realism record | No |
| I-AC-2 | Read as strengthening NL-C1 — a silent reopening | Pre-empts the review NL-C1 requires | Recorded | **None** | Partly |
| I-AC-3 | Nothing | Nothing | — | **None** | Yes |
| I-AD-1 | Conditional friction statement, prospective only | Closes a question NL-C2's extended form already frames | Recorded | At most the acquisition question, recorded in §18 without the experiment | Partly |
| I-AD-2 | Read as advancing NL-C2 without its review | Pre-empts that review | Recorded | **None** | Yes |
| I-AD-3 | Adds a divergence statistic | Closes nothing | Recorded | **None** | Yes |
| I-AE-1 | Would have conditioned the magnitude record on positioning | Would have closed that question | — | Would have been the magnitude record | No |
| I-AE-2 | Closed by binding rejection | Closed by binding rejection | — | **None** | No |
| I-AF-1 | Nothing | Nothing | — | **None** | Yes |
| I-AF-2 | A fact the literature treats as established | Most likely indicates a measurement problem | Recorded | **None** | Yes |
| I-AF-3 | Re-derives a textbook artefact | Nothing | — | **None** | Yes |
| I-BC-1 | Would have spoken directly to **M0.5** | Would have closed the impact question | — | Would have been the cost-realism record — the strongest consumer in the atlas | **No** |
| I-BC-2 | Adverse — invites the stopped programme | Nothing | — | **None** | No |
| I-BC-3 | Execution-timing — **prohibited** | Closes the resilience question | — | **None** under current governance | No |
| I-BC-4 | Uninterpretable either way | Uninterpretable either way | — | **None** | n/a |
| I-BD-1 | Re-establishes an unselected family | Pre-empts it | Recorded | **None** | Yes |
| I-BD-2 | Would be read directionally — prohibited | Closes little | Recorded | **None** | Partly |
| I-BD-3 | A funding-conditioned directional finding — the D1-A shape | Closes little | Recorded | **None** | No |
| I-BE-1 | Would have conditioned magnitude on positioning | **Would have closed a genuinely open question** | — | Would have been the magnitude record | **No** |
| I-BE-2 | Closed by binding rejection | Closed by binding rejection | — | **None** | No |
| I-BF-1 | Establishes flow commonality, prospective only | Most likely a measurement problem | Recorded | At most the acquisition question | Partly |
| I-BF-2 | Every onward route is closed by governance | Closes a question the card created | Recorded | **None** | **Yes** |
| I-BF-3 | No consumer | Closes a question the card created | Recorded | **None** | **Yes** |
| I-CD-1 | An unvalidatable depth number | Nothing | — | **None** | Yes |
| I-CD-2 | Closest approach to M0.5 among C×D | Closes the liquidity-component question | — | Would have been M0.5 | No |
| I-CE-1 | A crypto test of the spiral mechanism | Closes it | — | **None** for Prometheus — no lane could consume it | No |
| I-CE-2 | Cascade propagation understanding | Closes it | — | **None** | No |
| I-CF-1 | Liquidity commonality | Closes it | — | **None** | No |
| I-CF-2 | Execution timing — prohibited | Closes it | — | **None** | No |
| I-DE-1 | Would have separated crowding from unwinding | Would have closed M-12 | — | Context lens only under §7.C | **No** |
| I-DE-2 | Weak class-composition claim | Closes little | — | **None** | No |
| I-DE-3 | An uncheckable positioning claim | Nothing | — | **None** | n/a |
| I-DF-1 | Read as advancing NL-C2 before its review | Pre-empts that review | Recorded | **None that does not run through NL-C2** | Partly |
| I-DF-2 | An unexplained calendar regularity | Closes nothing | Recorded | **None** | Yes |
| I-DF-3 | Belongs to NL-C2's unreviewed question | Same | Recorded | At most the acquisition question | Partly |
| I-EF-1 | Common-deleveraging decomposition | Closes it | — | **None** | No |
| I-EF-2 | Settlement positioning pattern | Closes it | — | **None** | No |
| T-1 | Would have closed **M-13** | Same | — | Context lens only | **No** |
| T-2 | Would have closed **M-14** and spoken to M0.5 | Same | — | Would have been the cost-realism record | **No** |
| T-3 | Commonality-conditioned impact | Closes it | — | **None** | No |
| T-4 | Execution timing — prohibited | Closes the resilience question | — | **None** | No |
| T-5 | Duration-conditioned impact | Closes it | — | **None** | No |

**Findings, stated adversely as the authorization requires.**

1. **Every family whose pass has a genuinely legitimate consumer is data-blocked.** I-BC-1, I-BE-1,
   I-DE-1, T-1, T-2, and I-AE-1 are the six families whose results would have changed a real project
   record — the cost-realism record, the magnitude record, or the M-12/M-13/M-14 closure — and every one of
   them requires layer C or layer E.
2. **Every family that is computable now has no legitimate consumer, or has one only through an unselected
   candidate.** Of the thirteen dual-admissible families, seven are duplicative or rescue-shaped, three
   fail the consumer test outright, two are proxy substitutions, and one lacks a primary source.
3. **Nine families are self-created questions** — the fail branch would close only a question the card
   itself invented. The authorization requires that circularity be stated explicitly, and it is stated in
   each card's §G.
4. No family was admitted by inventing a consumer. Where the only available consumer was "decide whether a
   documented acquisition question deserves later operator review", the atlas records that question
   directly in §18 **without** running the experiment, which is the cheaper and more honest route.

## 17. Evidence and reserve-pressure comparison

| Dimension | Finding across all 44 families |
|---|---|
| Families requiring an evidence reserve for a first question | **Zero** |
| Families requiring `PRE_V002_INTERNAL_HOLDOUT` reuse as confirmation | **Zero** |
| Families requiring `V002_TERMINAL_WINDOW` | **Zero** |
| Families requiring `V002_SEALED_TEST` | **Zero** |
| Families with foreseeable *later* reserve pressure | I-AB-1 (immediate and illegitimate — a "confirm the CF-1 result" argument); I-AD-2 and I-DF-1 (a "confirm the band" argument, which the NL-C2 card already records as anticipated and unjustified) |
| Families whose reserves have no honest claim on them | All funding-family cards — the v002 reserves are aggTrades-family objects, so a funding question cannot claim them |
| Anticipated confirmation demand | Low for every family, because no family predicts anything out of sample; the blocked families predict nothing because they cannot be run, and the admissible families are levels and decompositions rather than forecasts |
| Could a result remain development-only? | Yes for every admissible family — and this is a structural property, not a promise |

**Reserve posture of this phase.** No reserve was opened, read, listed for content, enumerated, sampled,
scored, spent, proposed, or recommended. No ledger transition was made and no transition row was added.
`test_rows_loaded = 0` is preserved.

## 18. Acquisition-dependency comparison

Six families are blocked pending an acquisition that is **not authorized by this phase and not requested
by it**. They are recorded so that a future operator review has the question in one place.

| Family | Data family that would need acquisition | Archive status per committed records | Approximate burden | Would acquisition make the family survivable? |
|---|---|---|---|---|
| I-AD-1 | Premium-index or index-price klines, BTCUSDT | `Hist: TRUE` bulk archive | Low — bar-level, single symbol | **No.** It would still be NL-C2's extended form plus a context variable, and S8's confound is not separable |
| I-AD-3 | Mark-price klines, BTCUSDT | `Hist: TRUE`, governed by Phase 3r §8 | Low | **No.** §7.E records the execution-realism lane as not-recommended, and the objection is irrelevance, not availability |
| I-AF-3 | Multi-symbol aggTrades | `Hist: TRUE` bulk archive | **High** — tick-level, multi-symbol | **No.** Duplicative of CF-2 and consumer-free |
| I-BD-2 | Premium-index or index-price klines | `Hist: TRUE` | Low | **No.** Its natural reading is directional, which §7.C closes |
| I-BF-1 | Multi-symbol aggTrades, synchronous | `Hist: TRUE` bulk archive | **High** — the largest acquisition in the atlas | **No.** Best case is an already-established literature fact with no current consumer |
| I-DF-3 | Index-price or premium-index klines | `Hist: TRUE` | Low | **No.** It is NL-C2's own blocked extended form |

**Finding.** **No acquisition in this list would convert a blocked family into a survivor.** Every one of
the six fails at least one non-data screen — duplication, rescue risk, or absent decision consumer — after
the data block is removed. The atlas therefore records **no acquisition question that deserves operator
review on its own merits**, and requests none.

Separately and importantly: the nineteen families blocked on layer C or layer E are **not** acquisition
questions at all. Their data does not exist in any admissible public form for the study window, and
prospective capture is regime-non-comparable to the substrate that carries every Prometheus result. No
amount of authorization creates a 2024 order book or a 2024 open-interest series.

## 19. Negative-search log

Negative evidence is a project asset. Nothing rejected here is suppressed, and no family is omitted
because the shortlist turned out to be empty.

### 19.1 Complete disposition tally

Forty-four materially distinct interaction families reached a disposition — **thirty-nine two-way** and
**five three-way**.

| Disposition | Count | Families |
|---|---:|---|
| `DUPLICATIVE_OR_ALREADY_DEPLETED` | 4 | I-AB-1, I-AC-3, I-AF-1, I-BD-1 |
| `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED` | 20 | I-AC-1, I-AE-1, I-BC-1, I-BC-2, I-BC-3, I-BE-1, I-CD-2, I-CE-1, I-CE-2, I-CF-1, I-CF-2, I-DE-1, I-DE-2, I-EF-1, I-EF-2, T-1, T-2, T-3, T-4, T-5 |
| `ARCHIVE_AVAILABLE_NOT_ACQUIRED__NO_ACQUISITION_AUTHORIZED` | 6 | I-AD-1, I-AD-3, I-AF-3, I-BD-2, I-BF-1, I-DF-3 |
| `DATA_AVAILABLE_BUT_NO_DECISION_CONSUMER` | 1 | I-AF-2 |
| `PROXY_DEPENDENT__REJECT` | 5 | I-AE-2, I-BC-4, I-BE-2, I-CD-1, I-DE-3 |
| `REJECTED_RESEARCHER_FREEDOM` | 0 | — (see §15 for why this is a deliberate absence) |
| `REJECTED_ABSENT_DECISION_CONSEQUENCE` | 3 | I-AB-2, I-BF-2, I-BF-3 |
| `HIGH_RESCUE_RISK__DOES_NOT_SURVIVE` | 4 | I-AC-2, I-AD-2, I-BD-3, I-DF-1 |
| `POTENTIALLY_NEW__REQUIRES_INDEPENDENT_REVIEW` | **0** | — |
| `INSUFFICIENT_PRIMARY_SOURCE_OR_REPOSITORY_EVIDENCE` | 1 | I-DF-2 |
| **Total** | **44** | |

No interaction is described anywhere in this report as approved, selected, M0-cleared, authorized,
validated, or ready.

### 19.2 The fifteen mandatory starting interactions, individually indexed

The authorization required each of these to be assessed explicitly, without presuming survival. None
survived.

| # | Mandatory starting interaction | Atlas card | Disposition |
|---|---|---|---|
| 1 | trade activity × price or volatility | I-AB-1 | `DUPLICATIVE_OR_ALREADY_DEPLETED` |
| 2 | aggressive flow × displayed liquidity | I-BC-1 | `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED` |
| 3 | trade bursts × liquidity resilience | I-BC-3 (and T-4) | `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED` |
| 4 | liquidity state × volatility magnitude | I-AC-1 | `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED` |
| 5 | trade activity × funding | I-BD-1 | `DUPLICATIVE_OR_ALREADY_DEPLETED` |
| 6 | trade activity × premium or basis state | I-BD-2 | `ARCHIVE_AVAILABLE_NOT_ACQUIRED__NO_ACQUISITION_AUTHORIZED` |
| 7 | funding × premium or index state | I-DF-3 | `ARCHIVE_AVAILABLE_NOT_ACQUIRED__NO_ACQUISITION_AUTHORIZED` |
| 8 | funding × open interest | I-DE-1 | `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED` |
| 9 | funding × open interest × aggressive flow | T-1 | `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED` |
| 10 | cross-symbol activity × own-symbol response | I-BF-1 | `ARCHIVE_AVAILABLE_NOT_ACQUIRED__NO_ACQUISITION_AUTHORIZED` |
| 11 | cross-symbol funding × market-wide activity | I-DF-1 | `HIGH_RESCUE_RISK__DOES_NOT_SURVIVE` |
| 12 | session or settlement timing × trade activity | I-BF-2 (and I-BD-1) | `REJECTED_ABSENT_DECISION_CONSEQUENCE` |
| 13 | session or settlement timing × liquidity | I-CF-2 | `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED` |
| 14 | volatility magnitude × funding or premium state | I-AD-2 (funding form); I-AD-1 (premium form) | `HIGH_RESCUE_RISK__DOES_NOT_SURVIVE`; `ARCHIVE_AVAILABLE_NOT_ACQUIRED__NO_ACQUISITION_AUTHORIZED` |
| 15 | trade duration × liquidity recovery | T-5 (and I-BC-3) | `SCIENTIFICALLY_MEANINGFUL_BUT_DATA_BLOCKED` |

**Note on item 7.** "Funding × premium or index state" is partly an *intra-layer* relation: the premium
index is a layer-D construction. The atlas assesses it at its genuinely cross-lane face — funding against
the **composite spot index**, which is a cross-market (layer F) object — and records that the intra-layer
face is the published contractual identity at the heart of the unselected NL-C2 candidate, which this
phase does not reopen.

### 19.3 Interactions already represented by existing named families

The authorization required these to be identified explicitly. **An old name does not confer continuing
admissibility, and an old rejection is not assumed exhaustive** — each mapping below states which it is.

| Existing family | Interaction it already represents | Atlas card | Still admissible? |
|---|---|---|---|
| M-1 / M-2 | Spread and top-of-book depth as context | I-AC-1, I-CF-2 | **No** — layer C has no admissible history |
| M-3 / M-4 | Order-book imbalance across levels | I-BC-1 | **No** — same block |
| M-5 | Aggressive volume / taker imbalance | I-BC-1, I-BC-2, I-BD-3 | Leg admissible; every interaction partner is not |
| M-6 | Trade burst / volume impulse | I-AB-1, I-BF-2, T-4 | Leg admissible; merged into CF-1 as a family |
| M-7 / M-8 | Sweep and replenishment | I-BC-3, T-4, I-CE-2 | **No** — layer C |
| M-9 | Liquidation cascade proxies | I-AE-2, I-BE-2, I-CE-2 | **No** — no liquidation marker; and the family carries a binding rejection |
| M-10 | Funding-rate context | I-AD-2, I-BD-1, I-DF-1, I-DF-3 | Leg admissible as a **context lens only**; every proposed use here is duplicative or rescue-shaped |
| M-11 | Open-interest context | I-AE-1, I-BE-1, I-EF-1 | **No** — 30-day retention makes the 2024 series unrecoverable |
| **M-12** | **Funding + OI interaction** | **I-DE-1** | **No** — the OI leg is unrecoverable |
| **M-13** | **Funding + OI + aggressive-flow interaction** | **T-1** | **No** — same |
| **M-14** | **Spread / depth / flow regime interaction** | **T-2** | **No** — two of three legs unavailable |
| CF-1 | Activity → realized-variance magnitude | I-AB-1 | Result exists; lane closed by `REJECT_CF1_FILTER_CONTINUATION__REMAIN_PAUSED` |
| CF-2 | Cross-symbol temporal lead–lag | I-BF-1, I-AF-3, T-3 | Blocked on unacquired multi-symbol aggTrades; unselected |
| CF-3 | Derivatives context + settlement/session timing → volatility regime | I-BD-1, I-AF-1, I-DF-2, I-EF-2 | Computable; **unselected**, and not reopened here |
| NL-C1 | Price-only effective-spread estimation | I-AC-2, I-AC-1 | Unselected, un-cleared, awaiting independent review; not reopened |
| NL-C2 | Funding as a no-arbitrage friction bound | I-AD-1, I-AD-2, I-DF-1, I-DF-3, I-CD-1 | Unselected, un-cleared, awaiting independent review; not reopened |
| D1-A | Funding as a directional trigger | I-BD-3, I-DE-3, I-BD-2 | Retained verdict MECHANISM PASS / FRAMEWORK FAIL; §7.C `HIGH_D1-A_RESCUE_RISK` |

### 19.4 Families considered and not carried into a card

Recorded for completeness; each failed the §5.2 qualifying test at the first step and is therefore not an
interaction at all.

| Considered | Why it is not an interaction |
|---|---|
| "Combine aggTrades features and funding in one model" | A feature concatenation; asserts no moderation and no joint identification |
| "A deep sequence model over multiple modalities" | A method, not a mechanism (§6.4); model novelty is not mechanism novelty |
| "A foundation model or tokenizer applied to the substrate" | Layer G; asserts no mechanism and would additionally require an unauthorized model download |
| "Synthetic generation of order-book states to fill the layer-C gap" | Manufactures the missing leg; a proxy with no validation path, and worse than P-1 through P-10 because the substitute is generated rather than observed |
| "Regime classifier over spread, depth, flow, funding, and OI jointly" | This is M-14 / M-13 restated; additionally the committed record flags regime classification as the project's most overfitting-prone style, with G1 as precedent |
| "Interaction term significance testing across all committed feature pairs" | An arbitrary Cartesian product over 45 columns; the authorization forbids enumerating feature crosses as interactions |
| "Acquire depth or quotes prospectively, then form a hypothesis" | Inverts the causal order; already rejected as AW #14 and Phase 4bn-BE **N-16** |

### 19.5 Negative external-search results

Recorded because their absence shaped dispositions:

- **No primary source was located** establishing a funding × open-interest interaction *specific to crypto
  perpetuals*. The search returned only secondary and vendor material, which carries no substantive claim
  under §5.4. I-DE-1 therefore rests on X8, S8, and the project's own M-12, not on a venue-specific source.
- **X12 (Kim & Park 2025)**, the most recent funding-rate-design theory located, asserts **no** interaction
  between funding-rate design parameters (caps, clamps) and any market-state layer. This is recorded as a
  genuine negative: the newest theory in the funding lane supplies a pricing and hedging construction, not
  a new interaction mechanism, and therefore supplies no §6.A "materially new mechanism source" for the
  §7.C cooled-down lane.
- **No primary source was located** for a calendar-availability-of-arbitrage-capital mechanism on a 24/7
  venue, which is why I-DF-2 carries `INSUFFICIENT_PRIMARY_SOURCE_OR_REPOSITORY_EVIDENCE` rather than a
  stronger rejection.

## 20. Surviving interaction shortlist

```text
Surviving interactions: 0
```

The permitted range was **0 through 5**. Zero was treated throughout as an acceptable and possibly
preferable outcome, and it remained the live outcome until the final screening pass. No interaction was
promoted to reach a non-zero count.

No interaction carries the disposition `POTENTIALLY_NEW__REQUIRES_INDEPENDENT_REVIEW`.

**Why the closest candidates did not survive, stated plainly.**

- **I-DF-1** (cross-symbol funding dispersion) was the only family in the atlas with current external
  theory, a genuine joint-identification claim, and **both legs already on disk**. It fails because it is a
  symbol-universe expansion of an unselected, unreviewed candidate in the lane M0 §7.C flags as most
  rescue-prone, over the exact five-symbol universe that returned `NOT_SUPPORTED` under §7.B — and M0 §6
  names symbol-universe expansion as a forbidden post-null adjustment.
- **I-AD-2** (funding-clamp censoring conditioned on volatility) is cheap, admissible, and anchored in
  exchange-published constants. It fails because NL-C2's own preregistration sketch already names the
  censoring share as its primary test statistic, so this is NL-C2 plus a context variable — and §15 is
  explicit that a context variable does not create a new mechanism by conditioning an old result.
- **I-BE-1** (volume shock × open interest) has the best external interaction source in the atlas, a
  signed prediction, and a futures-market precedent. It fails because the moderating series for 2024 does
  not exist and cannot be recovered.
- **I-BC-1** (flow × depth) is the canonical interaction of the entire field and would speak directly to
  the project's one undischarged blocking M0 clause. It fails on the same structural absence.
- **I-AF-2** and **I-BF-3** are computable today on data already held and fail the decision-consumer test
  outright.

## 21. Strongest case for selecting none

Stated at full strength, and not rebutted.

**The atlas's negative result is structural, not circumstantial.** Prometheus's admissible data covers the
*moderated* legs of market-microstructure interactions — prices, executed trades, the published funding
scalar, and a free calendar — and none of the *moderating* legs. Every interaction that market theory
treats as identified requires a liquidity state or a positioning state to condition on, and Binance
publishes neither historically: derivatives book ticker and depth have no public archive, open interest
and long-short ratios retain thirty days, and the liquidation feed is a deliberately attenuated
largest-per-second snapshot with no archive at all. This is not a gap that authorization, budget, or
engineering can close. Prospective capture produces a series that cannot be joined to the 2024 substrate
on which every Prometheus result rests, and the project has a committed finding to exactly that effect.

**What remains computable is already spoken for.** Thirteen of forty-four families have both legs on disk.
Four are CF-1, CF-3, or their re-expressions. Four are NL-C1 or NL-C2 with a context variable attached —
which is precisely the rescue shape the authorization warned against, and which would advance two
unselected candidates past the independent review they were made conditional on. Two are prohibited
proxies. Three fail the decision-consumer test outright: their pass authorizes nothing the project may do,
and their fail closes only a question the candidate itself invented. There is no residue.

**Cheapness is an argument against, not for.** The families that are easiest to run — I-AD-2 at a few
lines of arithmetic over a small on-disk series, I-DF-1 over five funding series — are the ones that would
do the most governance damage, because they generate positive-looking results in the project's most
rescue-prone lane before the review that lane requires. The project's own record shows what follows a
positive result: Phase 4bn-BB's valid pass produced immediate pressure for a filter continuation, which
Phase 4bn-BC had to spend a full phase declining. Running a cheap funding interaction now would recreate
that pressure with weaker evidence and no selection process behind it.

**Nothing here has a legitimate current consumer.** The six families whose results would genuinely have
changed a project record — the cost-realism record via I-BC-1, I-CD-2, and T-2; the magnitude record via
I-AE-1 and I-BE-1; the M-12 closure via I-DE-1 — are all data-blocked. The families that are runnable have
consumers that are either forbidden (trade gating, sizing, timing, execution, reinterpretation of a
completed result) or circular. Under §17, that is decisive on its own.

**The honest summary.** The project asked whether there were untested cross-mechanism interactions worth
opening a lane for. There are many that are scientifically real, and the atlas names them. There are none
that Prometheus can identify with admissible data, distinguish structurally from its own prior work, and
consume through a legitimate decision. Selecting none is not a failure of imagination or of search
breadth; it is the correct reading of a data topology the project has spent several phases establishing.

**Remaining paused is a valid outcome.**

## 22. Exact phase result

```text
NO_ADMISSIBLE_CROSS_LANE_INTERACTION_IDENTIFIED__REMAIN_PAUSED
```

No interaction survives all screens. No lane is selected. No candidate is ranked, recommended, preferred,
or cleared. No successor phase is authorized.

The pre-branch fail-closed state `LIVE_STATE_MISMATCH__NO_PHASE_STARTED` did **not** apply: live
verification passed against `d8182d96e11bc11517c3432eeddc1fd6ea4cacb5` before any mutation (§2).

## 23. Independent-review packet

**No independent-review packet is produced, because no interaction survives.**

The authorization requires a neutral `Independent Cross-Lane Review Packet` only "if one or more
interactions survive". The surviving count is zero (§20), so the condition is not met and no packet is
constructed. Producing one anyway would misrepresent the phase's result by implying that something is
awaiting review.

Two points are recorded so that this absence is not misread:

1. **The pending Phase 4bn-BE review is unaffected.** `NL-C1` and `NL-C2` still require an independent
   Fable review before either could become a proposed lane, under the conditions recorded in the Phase
   4bn-BE closeout §17. That requirement is neither discharged, weakened, nor advanced by this phase, and
   **Fable was not invoked here**.
2. **Nothing in this atlas is a substitute for that review**, and no finding here should be read as
   evidence for or against either candidate. Where an atlas card touches NL-C1 or NL-C2, it is rejected
   precisely so that the pending review is not pre-empted.

## 24. Non-authorization statement

```text
Phase 4bn-BF constructs a cross-lane mechanism and data-interaction atlas; it selects no research lane and authorizes no successor phase.
```

```text
An interaction surviving Phase 4bn-BF means only that it is worthy of independent adversarial review; it does not mean approved, selected, M0-cleared, preregistered, or authorized.
```

```text
No market data, local research artefact, evidence reserve, model, signal, strategy, backtest, PnL, paper, shadow, live, or exchange-write activity is authorized by Phase 4bn-BF.
```

```text
No data acquisition is authorized by Phase 4bn-BF.
```

```text
Remaining paused is a valid outcome.
```

No stopped arc is softened, merged, reinterpreted, reopened, or rescued. No retained verdict is revised.
No project lock is loosened. No M0 clause is marked `PASS` for anything. No committed data-source status is
revised. No Prometheus scientific value is computed, recomputed, reinterpreted, narrowed, or softened by
this phase.
