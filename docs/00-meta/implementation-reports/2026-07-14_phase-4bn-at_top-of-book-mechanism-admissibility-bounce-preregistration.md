# Phase 4bn-AT — Top-of-Book Mechanism Admissibility and Bounce-Decomposition Preregistration

## 1. Phase name

Phase 4bn-AT — Top-of-Book Mechanism Admissibility and Bounce-Decomposition Preregistration.

Docs-only source-admissibility and scientific-preregistration decision phase. This phase decides whether a future, separately authorized top-of-book contract phase is justified. It does **not** acquire, download, capture, parse, normalize, or analyze any market-data record.

## 2. Branch

`phase-4bn-at/top-of-book-mechanism-admissibility-bounce-preregistration`

## 3. Base SHA

`40377e231cc72318c884a11d258775912fe71b4c` (main == origin/main at phase start).

## 4. Phase type

Docs-only source-admissibility and scientific-preregistration **decision** phase. No data pipeline, model, builder, diagnostic, downloader, parser, or capture is run or created. Documentation is committed only.

## 5. Current project state

- Phases 4bn-AH through 4bn-AS are complete and merged on `main`.
- Phase 4bn-AR recorded `INVESTIGATE_AMBIGUOUS` on the long-horizon (5m/30m/1h) fixed baseline run.
- Phase 4bn-AS resolved that ambiguity with `STOP_LONGHORIZON_ML_ARC`.
- Phase 4bn-AS final result state:
  `LONGHORIZON_ML_AMBIGUITY_DECISION_MEMO_MERGED_TO_MAIN__STOP_LONGHORIZON_ML_ARC_RECORDED__NO_SUCCESSOR_EXECUTION_AUTHORIZED__REMAIN_PAUSED`.
- Recommended state entering this phase: remain paused.
- No ML, strategy, PnL, backtest, acquisition, paper, shadow, live, or exchange-write execution is currently authorized.
- All published authorization flags are `false`; `research_eligible = False`; `eligibility_gate_status = PENDING`; `flip_research_eligible(...)` is a permanently-raising invariant (Phase 4aw), never invoked.

The high-level checkpoint `docs/00-meta/current-project-state.md` is authoritative for the pre-4bn strategy arcs but is stale with respect to the 4bn-AH…AS microstructure-ML arc (its document status is dated 2026-04-29 / Phase 3k). The authoritative recent state is the 4bn implementation-report series. Committed repository content governs where it conflicts with any summary.

## 6. Exact authorization boundary

This phase is authorized to:
- inspect committed project documentation and committed source constants;
- inspect official public documentation about Binance USDⓈ-M bookTicker / top-of-book data;
- inspect official archive directory listings and file-name metadata (index metadata only, never file content);
- inspect official Binance public-data repositories and official issue trackers;
- inspect checksum / archive-format / timestamp / terms documentation;
- inspect HTTP response headers or archive-index metadata to establish whether files plausibly exist;
- record URLs, access dates, and source hierarchy;
- assess retrospective versus prospective-only feasibility;
- define and freeze a future data-admissibility contract, causal-alignment rules, a model-free descriptive metric registry, and scientific outcome categories with consequences;
- codify existing negative and stopped project results;
- create the Phase 4bn-AT memo and closeout, committing documentation only.

This phase is **not** authorized to: download any bookTicker or sample archive; open/parse any market-data archive; call live or historical bookTicker endpoints; open a WebSocket; start prospective capture; acquire top-of-book, depth, or any new market data; read feature/label/raw Parquet, v002 terminal, or sealed-test data; load test rows; inspect local generated AQ/AR/model artefacts; implement any downloader/parser/normalizer/aligner/label/feature; rerun any label, model, or diagnostic; perform any strategy/signal/PnL/backtest/replay/paper/shadow/live/exchange-write work; touch credentials/private endpoints/user streams/MCP/Graphify/.mcp.json; or authorize any successor execution phase.

### Documentation-research boundary honored

Fetching ordinary documentation pages, archive directory-index pages, public repository pages, official issue pages, and response headers is permitted and was the only external action taken. No compressed market-data file, CSV, JSON market snapshot, or sample was downloaded. No Binance market-data endpoint was called to inspect a live response. Where required coverage or format could not be established from documentation and archive metadata alone, that uncertainty is recorded (§21–§25) and counted **against** admission — it was never resolved by acquiring data.

## 7. Documents inspected (committed repository)

Governance / process / meta:
- `docs/00-meta/current-project-state.md` (checkpoint; treated as stale past Phase 3k).
- `docs/00-meta/m0-mechanism-admissibility-gate.md` (M0 twelve-clause gate; M0.5 cost realism; M0.8 data feasibility; §7.D microstructure lane `NOT_RECOMMENDED_NOW`).
- `docs/00-meta/process/phase-workflow-standard.md`, `merge-closeout-standard.md`, `operator-report-standard.md`, `phase-risk-tiering-standard.md`, `claude-code-lightweight-workspace-standard.md` (process standards).

Preregistration / contract / verdict lineage:
- Phase 4bn-AE ML-baseline preregistration + contract amendment (`2026-06-05_phase-4bn-ae_...`), including its §8 claim scope and §19 M0 strategy/PnL/backtest hard boundary.
- Phase 4bn-Y chronological-split / holdout policy memo (`2026-06-05_phase-4bn-y_...`); Phase 4bn-AA pre-v002 split-policy artefact (`2026-06-05_phase-4bn-aa_...`); Phase 4bn-AC ML-dataset-contract memo (`2026-06-05_phase-4bn-ac_...`); Phase 4bn-AB source-admissibility memo (`2026-06-05_phase-4bn-ab_...`).
- Phase 4bn-AH…AO reports and closeouts (dataset build, descriptive diagnostics, 15s and long-horizon label build/diagnostics).
- Phase 4bn-AJ fixed pre-v002 baseline run verdict + closeout (the "clean 15s" result).
- Phase 4bn-AK ML-arc decision memo + closeout (`CONTINUE_EXACTLY_ONE_BOUNDED_FOLLOWUP`; §16(b) `bookticker_midprice_data_admissibility_memo` **deferred, not foreclosed**).
- Phase 4bn-AP long-horizon ML-baseline preregistration contract + closeout (contract template).
- Phase 4bn-AQ long-horizon ML-dataset build single-run + closeout (dataset identity).
- Phase 4bn-AR fixed long-horizon baseline run verdict + closeout (`INVESTIGATE_AMBIGUOUS`).
- Phase 4bn-AS long-horizon ML-ambiguity decision memo + closeout + merge-closeout (`STOP_LONGHORIZON_ML_ARC`; consumed-holdout constraint).

Prior microstructure-availability and acquisition lineage (directly relevant to top-of-book source admissibility):
- Phase 4as crypto-microstructure research-reset mechanism map (`2026-05-06_phase-4as_...`).
- Phase 4at Binance microstructure data-availability / capture-feasibility (`2026-05-07_phase-4at_...`) — bookTicker recorded `Hist: FALSE`.
- Phase 4au Binance microstructure capture design specification (`2026-05-07_phase-4au_...`) — bookTicker WS field/schema.
- Phase 4av public-only microstructure capture implementation plan; Phase 4az public aggTrades archive acquisition; Phase 4ba aggTrades dataset eligibility-gate review; Phase 4bb-C aggTrades offline eligibility gate; Phase 4bb-F canonical sidecar / path policy.
- Phase 4bn-L derived-stack storage-and-budget memo (`2026-06-01_phase-4bn-l_...`).

Data / execution reference docs:
- `docs/04-data/timestamp-policy.md`, `data-requirements.md`, `live-data-spec.md`, `historical-data-spec.md`, `dataset-versioning.md`.
- `docs/06-execution-exchange/binance-usdm-order-model.md`, `exchange-adapter-design.md`.

Committed source constants (read, not modified):
- `src/prometheus/research/microstructure/manifest.py` (`research_eligible: bool = False`; `flip_research_eligible` always raises `ManifestImmutableError`).
- `pre_v002_ml_dataset_contract.py` (`LOCKED_COST_BPS_PER_SIDE = 8.0`, `LOCKED_ROUND_TRIP_COST_BPS = 16.0`).
- `pre_v002_split_policy.py` split constants (boundary ms), `canonical_paths.py` sidecar helpers (Phase 4bb-F).

No file under `data/` was read. No Parquet, archive, or generated artefact was opened. No source, test, script, or config was modified.

## 8. External documentation sources and access dates

All accessed **2026-07-14 (UTC)**. Only documentation / index / issue pages and archive-index metadata were fetched; no market-data content was downloaded.

- **T1a** — Binance public-data repository README: `https://github.com/binance/binance-public-data` — documents the archive host `data.binance.vision` and the archive convention for **aggTrades / klines / trades**; each zip paired with a `.CHECKSUM` (SHA256); repository license **MIT**. bookTicker is **not** described in the README.
- **T1b** — Archive directory index (futures um daily bookTicker BTCUSDT): `https://data.binance.vision/?prefix=data%2Ffutures%2Fum%2Fdaily%2FbookTicker%2FBTCUSDT%2F` — the path **exists** (an undocumented futures um bookTicker archive is present), contradicting the README's silence.
- **T1c** — S3 index-metadata endpoint (file-name + LastModified only, no content): `https://s3-ap-northeast-1.amazonaws.com/data.binance.vision?delimiter=/&prefix=data/futures/um/daily/bookTicker/BTCUSDT/` — index retrieved as metadata; the returned page was summarizer-truncated and did **not** allow confirmation of complete 2024-10 / 2024-11 coverage; earliest visible daily key observed circa **2023-05-16**; `.CHECKSUM` companions present alongside `.zip` keys. Coverage of the required 2024-10-02 … 2024-11-30 window **could not be established** from this index probe.
- **T2a** — Official issue tracker, `binance/binance-public-data` issue **#305** ("futures 'book ticker' for ETH and BTC are output out of sequence"): `https://github.com/binance/binance-public-data/issues/305` — **opened 2024-01-16, Closed, no maintainer response / no fix visible**; confirms archived USDⓈ-M futures bookTicker records are **interleaved out of order by event_time and update_id** for BTC/ETH; confirms the 7-column CSV layout `update_id, best_bid_price, best_bid_qty, best_ask_price, best_ask_qty, transaction_time, event_time` (transaction_time / event_time = BIGINT Unix ms).
- **T2b** — Binance Developer Community thread: `https://dev.binance.vision/t/how-and-where-can-i-get-the-history-bookticker-data/36122/1` (thread date **2025-08-16**) — reports `data.binance.vision` "no longer updates for bookTicker for a long time, last update was in 2024"; **no maintainer / staff response** in the thread.
- **T1d** — Official WS field documentation (Individual Symbol Book Ticker Streams, USDⓈ-M): `https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Individual-Symbol-Book-Ticker-Streams` — the page is a client-rendered single-page app and **could not be retrieved as static content**; the live-stream field contract used below (`e, u, s, b, B, a, A, E, T`) is therefore taken from the **committed** Phase 4au capture-design specification, which records it.
- **T3** — Third-party corroboration (candidate-identification only, not admitted): Tardis.dev Binance USDⓈ-M documentation and cryptodatadownload — used only to note that generic futures history is often cited from **2019-11-17**; such sources "must not be admitted merely because they claim coverage" and are listed only as candidates requiring later provenance review.

## 9. Source-quality hierarchy

- **Tier 1 (official primary):** Binance USDⓈ-M API documentation; Binance public-data archive (`data.binance.vision`); Binance public-data GitHub repository README; official checksum / format documentation; official terms / licensing.
- **Tier 2 (official secondary):** Binance GitHub issues and maintainer responses; official announcements / changelogs; Binance Developer Community threads.
- **Tier 3 (reputable third party):** Tardis.dev, cryptodatadownload, etc. — used only to *identify* candidate sources; not admitted on a coverage claim; require a later provenance review before any use.

Excluded outright: anonymous file mirrors; unverified torrents; scraped datasets with no provenance; reconstructed quotes; synthetic top-of-book; any data whose timestamps or update semantics are undocumented.

**Hierarchy result relevant to this decision:** the futures um bookTicker archive is **present in Tier-1 infrastructure** (the archive host) but is **undocumented in Tier-1 specification** (absent from the README and not retrievable from the API-docs SPA). Its schema and its ordering defect are documented only at **Tier 2** (issue #305) and **Tier 3**. Its coverage window and continued availability are asserted only at **Tier 2** (a community report of cessation in 2024) and could not be confirmed from Tier-1 index metadata.

## 10. Confirmation no market data was acquired or read

Confirmed. No bookTicker archive, sample, aggTrades archive, Parquet, CSV, or JSON market snapshot was downloaded, opened, or parsed. The only external fetches were documentation pages, a GitHub issue page, and archive **index metadata** (file-name / LastModified listings). Index metadata is explicitly not market-data content. No Binance market-data endpoint was called to inspect a response. No WebSocket was opened. `test_rows_loaded = 0`.

## 11. Confirmation no local generated outputs were read

Confirmed. No local generated AQ/AR JSON artefacts, model parameters, predictions, feature Parquet, label Parquet, raw aggTrades archive, v002 terminal data, or sealed-test data were read. Nothing under `data/` was opened.

## 12. Confirmation no model, builder, diagnostic, or workflow ran

Confirmed. No model was trained/scored/predicted/calibrated; no dataset builder, normalizer, aligner, label builder, feature builder, diagnostic, baseline run, or workflow was executed; no acquisition/parser/capture script was run or created. Only `git`, documentation reads, and permitted web documentation/index fetches occurred.

## 13. Summary of the closed ML arc

The pre-v002 aggTrades-only long-horizon ML arc is **stopped** (`STOP_LONGHORIZON_ML_ARC`, Phase 4bn-AS). Lineage:

- **Substrate:** BTCUSDT / Binance USDⓈ-M futures / aggTrades, pre-v002 segment 2024-03-01 … 2024-11-30 UTC (275 UTC dates), 45 causal aggTrades features, 3-class strict-sign directional labels.
- **Phase 4bn-AJ (15s):** the L2 multinomial-logistic baseline showed genuine short-horizon directional **information** — validation L2 accuracy 0.54531, uplift **+5.03 pp** over majority and **+2.96 pp** over persistence, balanced-accuracy **+3.56 pp**, macro-F1 **+0.145**; validation date-block and month-block agreement **1.000**; a ≥0.8 confidence tail (0.633) beat the majority floor on every split. Verdict `CONTINUE_ONE_FOLLOWUP`. **But** only **2.47 %** of validation 15s moves (1.20 % holdout) exceeded the locked 16 bps round-trip cost; median |return| ≈ 2.53 bps; the 15s target is "almost never economically relevant" — the information is **economically thin** and forecloses any economic reading.
- **Phase 4bn-AK:** `CONTINUE_EXACTLY_ONE_BOUNDED_FOLLOWUP`, selecting the longer-horizon label memo. Three follow-ups were deferred, including **§16(b) `bookticker_midprice_data_admissibility_memo`** ("bounce-free labels; new data") — "premature now … a heavier new-data-source admissibility path … **Deferred, not foreclosed**." *This present phase is the docs-only execution of that deferred admissibility memo.*
- **Phase 4bn-AL…AQ:** longer-horizon (5m/30m/1h) label memo → contract spec → build → diagnostics → preregistration contract (Phase 4bn-AP: `SUCCESS_ACCURACY_UPLIFT_PP = 2.0` over both floors, `_BALANCED_ACCURACY_UPLIFT_PP = 1.0`, `_MACRO_F1_UPLIFT = 0.03`; fail-closed trichotomy) → dataset build (Phase 4bn-AQ), reusing the same 214/45/14 pre-v002 split.
- **Phase 4bn-AR:** the clean 15s majority-floor win **inverted** at longer horizons. L2 accuracy uplift vs the strong majority floor: **5m −0.222 pp**, **30m −1.348 pp**, **1h −2.868 pp** (holdout similar or worse). Balanced-accuracy uplift +0.78 pp at 5m (below the +1.0 pp bar). Four of eight 5m primary criteria failed. Verdict `INVESTIGATE_AMBIGUOUS`. (Raw-move materiality *rose* with horizon — validation |move| > 16 bps: 5m 34.95 % / 30m 64.28 % / 1h 72.72 % — but predictive skill against the majority floor collapsed; materiality is descriptive context only and entered no target/loss/threshold/verdict.)
- **Phase 4bn-AS:** `STOP_LONGHORIZON_ML_ARC`. The pre-v002 holdout (14 dates, late-2024) is now **consumed** (scored under AR) and is no longer an untouched confirmation set. The only genuinely unseen reserves remaining are the v002 terminal window (2024-12-01 … 2025-02-28) and the sealed test split (2025-02-14 … 2025-02-28, `test_rows_loaded = 0`).

## 14. Independent-review summary and strongest counterargument

An independent Fable review ranked candidate directions: **A** top-of-book mechanism realism; **E** remain paused; **B** volatility/liquidity forecasting; **C** cross-symbol lead–lag; **D** replay/execution infrastructure — recommending **A**, subject to a docs-only admissibility and preregistration phase (this phase). It emphasized: the 15s-strong / 5m-dead pattern is consistent with bid–ask bounce but does not prove it; Candidate A is model-free and creates little rescue surface; every major outcome is potentially informative (bounce dominated / genuine midpoint movement / mixed / data inadmissible); historical bookTicker coverage may be incomplete; no result may reopen a stopped arc automatically; any revised friction estimate applies prospectively only.

The review is **non-binding** and is here compared critically with the committed record rather than accepted because it agrees with the proposed phase.

**Strongest counterargument (adopted as decisive weight, see §51 and §55):** the review's own strongest objection is that Candidate A "may amount to an **expensive autopsy** of a result the project cannot currently act on." Neither `BOUNCE_DOMINATED` nor `MIDPOINT_CONFIRMED` changes any currently-authorized action; the ML arc is stopped, no strategy/model is authorized, and any spread evidence applies prospectively only and cannot revise completed verdicts. When this low decision-relevant information gain is combined with the concrete inadmissibility of the retrospective source and the non-comparability of the prospective substitute (§25–§26, §49–§51), the counterargument is **not defeated** — it prevails.

## 15. Exact market-mechanism question

Did the clean 15-second last-trade directional-information result (Phase 4bn-AJ) represent genuine movement of the **bid/ask midpoint**, or was it substantially caused by predictable **bid–ask trade-price bounce**?

This is a market-mechanism and measurement-validity question about the *nature of the price signal underneath the 15s label*, not a question about model performance.

## 16. Why the question is scientifically distinct from AR rescue

It is distinct because:
- It is **model-free**: it decomposes a price *label* into quote-referenced components; it fits, scores, tunes, and selects **nothing**. There is no classifier, threshold, or weighting to rescue.
- Its object is a **measurement-validity property** of the 15s last-trade label, not the AR long-horizon predictive verdict. It cannot upgrade AR, revise AJ/AK/AR/AS metrics, or reinterpret `INVESTIGATE_AMBIGUOUS` as success.
- It uses already-evaluated dates **only for descriptive decomposition**, never again as unseen / untouched / independent predictive confirmation (the pre-v002 holdout is consumed, §13, §47).
- It requires a *new data family* (top-of-book quotes) that the aggTrades-only substrate cannot express; it is the deferred §16(b) admissibility question (§13), not a re-run of AJ or AR.

It is therefore not a continuation of the stopped long-horizon ML arc, not a rerun of Phase 4bn-AJ or 4bn-AR, not a new model experiment, not a strategy/execution/backtest phase, and not an attempt to revise a failed verdict.

## 17. Bid–ask-bounce mechanism

With a two-sided quote, transactions print alternately near the best bid and best ask even when the underlying fair price is static. Illustratively: bid = 99.99, ask = 100.01, midpoint = 100.00; successive trades alternate 99.99 ↔ 100.01. The **last-trade price** changes sign frequently while the **midpoint does not move**. A directional label built on last-trade price (as `forward_direction_15s` is, from aggTrades only) can therefore encode a large predictable component that is pure microstructure bounce — direction that reverses within a stable spread — rather than genuine information about where the market is going. Features carrying aggressor-side / trade-flow information can predict *which side the next prints land on* without predicting *midpoint movement*. This is the mechanism the project has repeatedly flagged: the 15s aggTrades label "may embed bid-ask bounce (aggTrades-only, no mid/book)."

## 18. Alternative genuine-fast-information explanation

The same 15s-strong / longer-horizon-dead pattern is **also** consistent with genuine, fast, decaying information: order flow briefly and truly moves the midpoint over ~15 s (real short-lived price discovery), after which the edge decays and, at 5m/30m/1h, is swamped by the up-skewed majority floor and mean drift. Under this explanation the midpoint genuinely moves in the labeled direction at 15 s, and the decay — not bounce — explains the horizon inversion. This phase must not presume which explanation is correct; the whole point of a top-of-book decomposition would be to distinguish them.

## 19. Official bookTicker field and timestamp semantics

**Live WebSocket stream (USDⓈ-M `<symbol>@bookTicker`), field contract** (from the committed Phase 4au capture-design spec; the official SPA doc page could not be retrieved as static content, §8 T1d):
- `e` — event type; `u` — order-book **updateId** (sequencing field); `s` — symbol;
- `b` — best bid price; `B` — best bid quantity; `a` — best ask price; `A` — best ask quantity;
- `E` — **event time** (message dispatch time); `T` — **transaction time** (the time the order-book state became effective at the exchange);
- update speed: real-time, pushed on any best-bid/ask change.

**Archived daily file (`data/futures/um/daily/bookTicker/<SYMBOL>/…`), column layout** (from issue #305, T2a): `update_id, best_bid_price, best_bid_qty, best_ask_price, best_ask_qty, transaction_time, event_time`; `transaction_time` and `event_time` are BIGINT Unix milliseconds; `update_id` is an unsigned big integer.

**Timestamp meaning under project policy** (`docs/04-data/timestamp-policy.md`; Phase 4au §14.9/§15): event time = the timestamp the source associates with the event; canonical storage = UTC Unix ms; `transaction_time` is preserved verbatim when Binance provides it; a monotonic clock is used only to break `event_time` ties on live capture. For causal alignment the **authoritative timestamp is `transaction_time` (T)** — the moment the quote became true — with `event_time` (E) secondary.

**Excluded liquidity / what the field is:** bookTicker reports only the **best visible bid and ask and their visible quantities** — the top of the visible book. It excludes all depth beyond the best level, hidden/iceberg liquidity, and queue structure. It is a *visible-top-of-book* object, not a measure of executable cost.

**Critical caveat:** the above live-stream semantics are official; the **archived file's** fidelity to them is *not* officially documented, and issue #305 shows the archival process does **not** preserve record order (§22). The archived `transaction_time`/`event_time` therefore cannot be assumed monotonic or authoritative without empirical inspection, which this phase is forbidden to perform.

## 20. Official archive structure

- Host: `data.binance.vision` (Tier-1 infrastructure), MIT-licensed tooling repo `github.com/binance/binance-public-data`.
- Documented families (README): futures um `{daily, monthly}/{aggTrades, klines, trades, …}/<SYMBOL>/…`, each `.zip` paired with a `.CHECKSUM` (SHA256).
- **bookTicker** is **not** in the README's documented family set, but a futures um daily bookTicker tree **does exist** at `…/daily/bookTicker/<SYMBOL>/…` (T1b) with `.CHECKSUM` companions (T1c). It is thus an **undocumented-but-present** archive family — a Tier-1 host object with no Tier-1 specification.
- aggTrades (the project's actual substrate) is fully documented and archived daily+monthly with checksums; this is why the project chose aggTrades-only (§21, and Phase 4at/4az).

## 21. Known coverage history

- The committed Phase 4at feasibility memo (2026-05-07) recorded bookTicker as `Hist: FALSE` — "no Binance public-archive book-ticker history at full granularity for derivatives … live capture required," and did not list bookTicker among archived families. This was the project's standing position.
- External research for this phase shows the position is **partially outdated**: a futures um daily bookTicker archive for BTCUSDT *does* exist (T1b). However, its documented history is thin: the earliest daily key observed in the index probe was circa **2023-05-16** (not the 2019-11-17 general-futures start cited by Tier-3), and a Tier-2 community report (2025-08-16) states the archive **stopped updating in 2024**.
- The general USDⓈ-M futures market history is cited (Tier-3) from 2019-11-17, but that pertains to trades/klines, not the bookTicker archive, whose own start (~2023) and cessation (~2024) are what matter here.

Net: the archive exists, but its coverage envelope is **documented only weakly and partly by Tier-2/Tier-3 assertion**, and Tier-1 index metadata could not confirm the specific required window (§24).

## 22. Known missing periods and defects

- **Documented, unresolved ordering defect (T2a, issue #305):** archived USDⓈ-M futures bookTicker records for **BTC and ETH** are **interleaved out of order by event_time and update_id**. The issue was opened 2024-01-16 and is **Closed with no maintainer fix / response visible** — i.e. an acknowledged-by-community, unremediated integrity defect in exactly the symbol (BTCUSDT) and family required. Records from different periods are physically interspersed rather than chronologically sorted.
- **Reported cessation (T2b):** bookTicker archive updates reportedly ceased in 2024; the exact last available date is unstated and unconfirmed by Tier-1.
- **Coverage of the required window unconfirmed (T1c):** the index probe could not enumerate 2024-10 / 2024-11 daily keys (summarizer truncation) and thus could not establish that all 59 required evaluation dates are present.
- **Undocumented file semantics:** no Tier-1 specification of the archived file's timestamp meaning, precision guarantees, immutability, or terms exists; the schema is known only from a bug report (T2a) and Tier-3 sources.

These are the "known corrupt, interleaved, or out-of-order files" and "known missing periods" the phase was charged with surfacing; here they are present and material.

## 23. Exact original 15s evaluation dates

Derived from the committed split policy (Phase 4bn-Y §11; Phase 4bn-AA `split_for_date`), **not guessed**. Split working name `CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`, BTCUSDT / USDⓈ-M / aggTrades:

| Segment | UTC range (inclusive) | Count | Role |
|---|---|---|---|
| Train | 2024-03-01 … 2024-09-30 | 214 | model fitting (not required for descriptive decomposition) |
| Embargo (dropped) | 2024-10-01 | 1 | train↔validation boundary purge |
| **Validation** | **2024-10-02 … 2024-11-15** | **45** | model selection / tuning |
| Embargo (dropped) | 2024-11-16 | 1 | validation↔holdout boundary purge |
| **Holdout (dry-run)** | **2024-11-17 … 2024-11-30** | **14** | one-time dry-run; **not** the sealed test |

Boundary constants: `BOUNDARY_TRAIN_VALIDATION_MS = 1727827200000` (2024-10-02T00:00:00Z); `BOUNDARY_VALIDATION_HOLDOUT_MS = 1731801600000` (2024-11-17T00:00:00Z). Date assignment uses the aggTrade `transaction_time` UTC date.

**Required evaluation coverage for a retrospective decomposition = the 59 dates 2024-10-02 … 2024-11-30 UTC (45 validation + 14 holdout; 2024-11-16 excluded).** Train dates may be useful but are not required for a model-free descriptive decomposition. (Note: the two "45"s in the project are distinct — pre-v002 *validation* = 45 dates 2024-10-02…2024-11-15; the *v002-terminal train* = 45 dates 2024-12-01…2025-01-14. This phase concerns only the pre-v002 45+14.)

## 24. Retrospective overlap matrix by required date range

| Required (BTCUSDT bookTicker) | Needed | Established from admissible documentation / Tier-1 index metadata? |
|---|---|---|
| Symbol BTCUSDT um bookTicker archive exists | yes | **Partially** — archive tree exists (T1b), but undocumented in Tier-1 spec |
| Validation 2024-10-02 … 2024-11-15 (45 UTC days) | all 45 | **Not established** — index probe could not enumerate Oct/Nov 2024 keys (T1c); cessation reported in 2024 (T2b) |
| Holdout 2024-11-17 … 2024-11-30 (14 UTC days) | all 14 | **Not established** — same as above |
| Full-day top-of-book coverage per date | all 59 | **Not established** — intraday completeness undocumented |
| Timestamps + sequencing sufficient for causal alignment | required | **Fails** — archived order is defective (T2a #305); archived-file timestamp semantics undocumented |
| Checksums present | required | **Yes** — `.CHECKSUM` companions present (T1c) |
| Provenance / immutability / terms documented | required | **Inadequate** — no Tier-1 spec, terms, or immutability guarantee for this family |

Under the phase's default conservative rule — *incomplete or unestablished validation/holdout coverage does not qualify for `ADMIT_TOB_RETROSPECTIVE_CONTRACT_NEXT`* — the coverage row alone blocks retrospective admission, and the sequencing/provenance rows independently block it.

## 25. Retrospective feasibility assessment

**Verdict: retrospective admission FAILS.** The ADMIT_TOB_RETROSPECTIVE bar requires *all* of: plausibly-established complete coverage of the required dates; timestamp/sequencing semantics that can support causal alignment; adequate checksums *and* provenance; no known defect that invalidates the study; a freezable contract; and sufficient expected information gain. Against that bar:

1. **Coverage — unestablished.** The archive exists but Tier-1 metadata could not confirm all 59 required dates; a Tier-2 report indicates cessation in 2024. Default rule → does not qualify.
2. **Timestamp / sequencing — defective and undocumented.** Issue #305 documents unremediated out-of-order records for BTC/ETH futures bookTicker; the archived file's authoritative-timestamp semantics are not in Tier-1 documentation. Causal alignment (strict at-or-before on a monotonic authoritative timestamp) cannot be assumed valid, and the residual validity could only be checked by parsing samples — which is prohibited.
3. **Checksums — adequate**, but insufficient alone.
4. **Provenance — inadequate.** The family is undocumented in Tier-1 specification; the project's own prior admissibility finding recorded it as unavailable; no terms/immutability guarantee exists.
5. **Known defect invalidating the study — present.** Undocumented + out-of-order timestamps directly threaten the one thing the study needs most: a trustworthy causal quote-to-trade alignment.
6. **Contract — freezable** (frozen in §29–§44), so this criterion is *met*, but it cannot rescue 1–5.
7. **Information gain — low** (§49), independently weak.

Per the explicit rule "documentation uncertainty that cannot be resolved without prohibited data acquisition should count against admission, not justify silent acquisition," items 1, 2, and 5 count against admission. Retrospective admission is **not** granted.

## 26. Prospective-only feasibility assessment

**Verdict: prospective-only admission FAILS for this question.**

- **Technical / legal feasibility:** capturing the live public `<symbol>@bookTicker` WS stream is technically feasible (the project designed such a pipeline in Phase 4au/4av, never built) and uses public market data with officially documented field semantics. In isolation this is the *cleaner* source.
- **Fatal non-comparability / non-answering:** the mechanism question is **retrospective by construction** — it asks whether *the 2024-10…11 clean 15s last-trade result* was bounce or midpoint. Decomposing that result requires **contemporaneous 2024 quotes aligned to the 2024 aggTrades**. A prospective capture beginning in 2026 produces quotes from a **different market regime** (volatility, spread, tick-size, liquidity, participant mix) that **cannot be aligned to 2024 trades at all**. Prospective data can only answer a *different, generic* question ("on 2026 BTCUSDT, how much of 15s last-trade direction is bounce?"), which does not decompose the actual spent result and does not resolve §15.
- **Proportionality:** a meaningful descriptive analogue would need weeks-to-months of continuous capture (high-rate top-of-book), non-trivial storage and message-rate burden, and continuous monitoring/failure-mode handling — real operational cost for a question it cannot actually answer.
- **Rescue / relitigation risk:** fresh 2026 quoted-spread evidence risks being read as revising the completed cost verdicts and the locked 8/16 bps reference, which is forbidden retrospectively (§59). This adds risk without adding decision-relevant value.

Prospective-only is therefore not credible-and-proportionate for §15.

## 27. Terms / provenance assessment

- **Ownership / license:** the tooling repo is MIT; the archive is Binance-owned public data. No Tier-1 terms page was located that governs redistribution of the archived files specifically; the project's standing posture (Phase 4az) is to keep any acquired archive under gitignored `data/microstructure/`, never committed, fetched only from `data.binance.vision`.
- **Checksums:** `.CHECKSUM` SHA256 companions exist for archive files, enabling bit-for-bit verification (checksum-first ordering, Phase 4az precedent). A single match does not guarantee future re-fetch byte-identity (Phase 4ba caveat).
- **Immutability:** not guaranteed; families "may be added or removed by Binance over time" (Phase 4at) — and the bookTicker family's reported cessation illustrates exactly this instability.
- **Schema stability / documentation:** the archived bookTicker schema is undocumented in Tier-1 sources; known only from a bug report (T2a) and Tier-3.
- **Provenance conclusion:** **inadequate for admission.** Checksums are present but the undocumented schema, undocumented immutability, reported cessation, and unremediated ordering defect make provenance insufficient for a causal-alignment-grade study.

## 28. Data-volume and engineering-burden estimate (documentation only)

Order-of-magnitude, from documentation only (no file was sized by download):
- **Retrospective:** BTCUSDT top-of-book updates on a liquid perpetual are frequent (sub-second on best-bid/ask change); a daily bookTicker file is materially larger than the ~21 MiB aggTrades day the project handled. Sixty-plus daily files (59 evaluation + optional train) plus checksums, decompressed and normalized, plausibly land in the low-tens of GiB range — within the Phase 4bn-L raw (10/25 GiB warning/hard) and derived (normalized 100/150, label 75/125, total 250/300 GiB) envelopes **only** if scoped tightly, and would require the ≥500 GiB free-space preflight. This is feasible in principle but non-trivial, and it presupposes admissible data (which §25 denies).
- **Prospective:** continuous high-rate top-of-book capture over weeks-to-months implies a sustained ingestion/monitoring service and steadily growing storage, well beyond a one-shot archive fetch — disproportionate for a question it cannot answer (§26).

Engineering burden either way includes a checksum-verified acquirer or a resilient capture client, an evidence-preserving reorderer (mandatory given #305), a strict causal aligner, and a descriptive metric computer — none authorized, none built.

## 29. Future source-admissibility requirements (frozen, fail-closed)

The following are **frozen now**, before any data read, as exact fail-closed requirements. No field is left TBD or "to be chosen after inspection." No threshold may be relaxed after data inspection. They define what an admissible top-of-book dataset **would** have to satisfy; §25–§26 conclude that no currently-available source meets them, hence the STOP.

## 30. Coverage thresholds (A)

- **Required symbol:** BTCUSDT, Binance USDⓈ-M perpetual, `daily/bookTicker` family only.
- **Required dates:** all **45** validation (2024-10-02…2024-11-15) **and** all **14** holdout (2024-11-17…2024-11-30) UTC dates = **59** dates. Train dates optional.
- **Required UTC-day completeness:** for each required date, top-of-book records must span the full UTC day with **no intraday data gap > 60 s** (a data gap = absence of any record; distinct from a no-update quiet period, which is bounded by the freshness ceiling, §34).
- **Minimum file availability:** 59 / 59 required daily files present, each with a `.CHECKSUM` companion.
- **Permitted missing-file count:** **0**.
- **Permitted partial-day count:** **0**.
- **Retrospective admission requires all 59 evaluation dates: YES** (no partial-coverage admission).

## 31. File-integrity thresholds (B)

- **Checksum requirement:** every daily file bit-for-bit SHA256-verified against its `.CHECKSUM` **before** parse (checksum fetched and parsed first).
- **Permitted checksum failures:** **0**.
- **Permitted unreadable files:** **0**.
- **Schema consistency:** every file conforms exactly to the 7-column layout `update_id, best_bid_price, best_bid_qty, best_ask_price, best_ask_qty, transaction_time, event_time`; any deviation → **dataset fail**.
- **Duplicate-record policy:** exact-duplicate rows (all 7 fields identical) collapse to one, logged; rows sharing `update_id` but differing in any quote field → **quarantine** as an invalid window; if the exact-duplicate rate > **0.5 %** of a day → **reject the day**.
- **Out-of-order-record policy:** records are **known** out-of-order (#305). A deterministic **stable sort** by (`transaction_time` asc, `update_id` asc) is permitted **only** with full reordering evidence (see §36 alignment and below). After sorting, if > **0.5 %** of records still violate `transaction_time` monotonicity beyond the tie window → **reject the day**.
- **Original-order preservation / reordering evidence (mandatory):** the raw layer preserves source bytes exactly; any reorder occurs only in a derived layer and must record: original file SHA256, original record count, pre-sort monotonicity diagnostics, the exact sort keys, post-sort SHA256, post-sort monotonicity proof, and the duplicate policy applied. A reorder without complete evidence → **dataset fail**.

## 32. Quote-validity thresholds (C)

- **bid, ask finite and > 0:** required; else invalid record.
- **bid_qty, ask_qty finite and > 0:** else the quote has no visible liquidity on a side → invalid for alignment (see zero-quantity).
- **bid_price ≤ ask_price:** required.
- **Crossed quote (bid_price > ask_price):** excluded as invalid; **never silently repaired**; counts toward the invalid ceiling.
- **Locked quote (bid_price == ask_price):** excluded from spread/midpoint metrics as degenerate (spread 0), flagged and counted separately; not repaired.
- **Zero-quantity quote:** treated as invalid for alignment; excluded.
- **Invalid-record ceiling:** if invalid quotes (crossed + zero-qty + non-finite) > **1.0 %** of a day → **reject the day**; if > **0.5 %** across the 59 dates → **dataset partition failure**.
- Invalid quotes are **excluded, not repaired**; a ceiling breach is a partition failure, never a silent fix.

## 33. Timestamp-coherence thresholds (D)

- **Authoritative causal timestamp:** `transaction_time` (T).
- **Secondary timestamp:** `event_time` (E), diagnostics only.
- **E/T disagreement:** if |E − T| > 5000 ms for > **1.0 %** of a day → flag for review; > **5.0 %** → **reject the day**.
- **Maximum permitted backward-time frequency:** after the evidence-preserving sort, residual `transaction_time` backward steps beyond the tie window > **0.5 %** of records → **reject the day**.
- **Equal-timestamp ordering:** ties in `transaction_time` resolved by ascending `update_id`; if `update_id` also ties, preserve original stable order and record it.
- **Update-ID ordering:** `update_id` expected non-decreasing within a `transaction_time`; gross violations counted toward the out-of-order ceiling (§31).
- **Timestamp precision:** milliseconds (BIGINT Unix ms).
- **UTC normalization:** all timestamps are UTC ms; date assignment by `transaction_time` UTC date (consistent with the pre-v002 split rule).
- **Date-boundary handling:** each quote assigned to its `transaction_time` UTC date; **no cross-date backfill**.

## 34. Freshness thresholds (E)

- **Quote age** = observation_timestamp − `transaction_time` of the selected at-or-before quote (ms).
- **Maximum quote age for label construction:** **2000 ms**. A label endpoint resolving to a quote older than 2000 ms is **unsupported** (excluded).
- **Maximum stale-quote share:** if > **5.0 %** of a day's alignment points resolve to a stale (>2000 ms) quote → **reject the day**; if > **2.0 %** across the segment → **partition failure**.
- **No-update periods:** the last valid quote remains authoritative up to the 2000 ms ceiling; beyond it the point is unsupported. **No later-quote backfill. No interpolation.**

## 35. Trade/quote alignment rules (F)

- For each observation timestamp `t` (a trade's `transaction_time`, or a 15s target = trade `transaction_time` + 15000 ms), select the **latest valid quote whose `transaction_time` ≤ t**.
- **At-or-before:** choose the maximum quote `transaction_time` ≤ t; tie-break by maximum `update_id`; then original stable order.
- **No future quotes:** a quote with `transaction_time` > t is never used; no nearest-neighbor rule that could select a future quote; no interpolation; no backfill.
- **Alignment tolerance:** the selected quote must satisfy the 2000 ms freshness ceiling; otherwise the point is unsupported.
- **Missing valid quote:** the observation point is dropped from the decomposition and counted against support.
- **Original trade row in support** only if **both** its 15s start-time quote and its 15s target-time quote are supported (valid, fresh, at-or-before).
- **Alignment support-rate floor:** ≥ **95 %** of the originally-evaluated trade rows per day must have both endpoints supported; a day < **90 %** → **reject the day**; segment-wide support < **95 %** → **partition failure**.

## 36. Partition and dataset rejection rules (G)

- **Reject a UTC day** if any of: missing file; checksum failure; unreadable; schema deviation; invalid quotes > 1.0 %; residual out-of-order > 0.5 % after evidence sort; E/T disagreement > 5.0 %; stale alignment > 5.0 %; alignment support < 90 %; exact-duplicate rate > 0.5 %.
- **Reject the whole dataset** if: any of the 59 required dates is rejected (all-59 requirement); or segment-wide invalid > 0.5 %; or segment-wide stale > 2.0 %; or segment-wide support < 95 %; or any reorder lacks complete evidence.
- **Minimum retained date count:** **59 of 59** (no relaxation).
- **Repair:** threshold breaches are **not** repairable; there is no post-inspection relaxation. Fail-closed.

## 37. Future descriptive metric registry (model-free)

Preregistered exact definitions for a later model-free phase. **No model metric is permitted** (no fit, score, predict, calibrate, threshold-tune). All metrics computed on the **supported aligned set** over the **admitted** dates, aggregated at the levels in §40.

1. **Quoted midpoint:** `midpoint = (best_bid + best_ask) / 2`.
2. **Quoted spread:** `spread = best_ask − best_bid`.
3. **Quoted spread (bps):** `spread_bps = spread / midpoint × 10000`.
4. **Half-spread (bps):** `half_spread_bps = spread_bps / 2`.
5. **Quote age:** observation_timestamp − `transaction_time` of the selected at-or-before quote (ms).
6. **Trade-to-midpoint location:** signed and absolute distance between the last trade price and the contemporaneous midpoint, in (a) raw price units, (b) bps, (c) half-spread units.
7. **Trade-price 15s direction:** the frozen strict-sign direction of the last-trade price over 15s (`DIRECTION_THRESHOLD_POLICY_V002`), reproduced **descriptively** — this does **not** rerun or score the old model.
8. **Midpoint 15s direction:** the same strict-sign concept applied to the **causal midpoint** selected at the start and 15s target timestamps.
9. **Label-agreement matrix** (per aligned pair), at minimum the cells: same non-zero direction; both zero; trade non-zero / midpoint zero; trade zero / midpoint non-zero; opposite non-zero directions; missing/invalid support.
10. **Agreement measures:** exact agreement rate; non-zero directional agreement; disagreement rate; opposite-direction rate; trade-only-movement rate; midpoint-only-movement rate; and a preregistered chance-adjusted measure (Cohen's κ on the 3-class agreement) reported alongside, not in place of, the raw rates.
11. **Bounce indicators:** trade-price movement while midpoint unchanged; trade-price reversal within a stable midpoint; fraction of |15s trade-price move| ≤ one contemporaneous quoted spread; fraction ≤ one half-spread; fraction crossing bid-side↔ask-side without same-direction midpoint movement; signed trade/midpoint disagreement conditional on aggressor side.
12. **Spread and freshness distributions** (see §40 aggregation).
13. **Materiality comparison:** absolute 15s trade-price move, midpoint move, and quoted spread; `|trade move| / spread`; `|midpoint move| / spread`; fraction of trade moves exceeding one spread; fraction of midpoint moves exceeding one spread; fraction exceeding the locked 16 bps round-trip reference — **descriptive only**.
14. **Observable-friction-component audit** (§41).

## 38. Trade-price versus midpoint label definitions

- **Trade-price 15s label** (frozen historical definition, reproduced descriptively): `+1` iff `forward_log_return_15s` of the **last-trade (aggTrade) price** is strictly positive, `0` iff exactly zero, `−1` iff strictly negative, `null` iff undefined; strict sign at zero, no deadband, no bp threshold, no optimization. This is `forward_direction_15s` as already locked — used here only for descriptive comparison, never re-fitted or re-scored.
- **Midpoint 15s label** (new descriptive object): the identical strict-sign rule applied to `log(midpoint(t+15s)) − log(midpoint(t))`, where `midpoint(t)` and `midpoint(t+15s)` are the causally-selected at-or-before quotes' midpoints (§35). Undefined (dropped) when either endpoint is unsupported.

The decomposition compares these two labels pointwise; genuine midpoint movement ⇒ high non-zero agreement with midpoint actually moving; bounce ⇒ trade direction non-zero while midpoint direction is zero or opposite.

## 39. Bounce-decomposition registry

For the admitted, supported set, record: (a) trade-only-movement share (trade dir ≠ 0 while midpoint dir = 0); (b) opposite-direction share (both non-zero, opposite sign); (c) sub-spread share (|15s trade move| ≤ one quoted spread) and sub-half-spread share; (d) bid↔ask crossing without same-direction midpoint move; (e) non-zero midpoint-support share (how often the midpoint genuinely moved over 15s); (f) all conditioned additionally on aggressor side and on spread/quote-age buckets (§40). These feed the outcome thresholds (§43).

## 40. Spread / freshness registry

Every distribution in §37 items 5, 12, and §39 is aggregated at: (i) whole evaluation segment; (ii) UTC date (each of the 59); (iii) UTC month (2024-10, 2024-11); (iv) hour of day (0–23 UTC); (v) spread bucket; (vi) quote-age bucket. Date-level and month-level aggregations drive the block-consistency requirements in §43 (mirroring the project's date/month-block dependence policy; no per-row significance testing).

## 41. Quoted-spread and observable-friction-component audit

Record quoted-spread distributions (spread, spread_bps, half_spread_bps) and their variation across the §40 levels. This is the **quoted-spread and observable-friction-component audit** — it is **not** a "true trading cost" or "true-cost" measurement. Top-of-book can *approximate*: best visible bid/ask, midpoint, quoted spread, half-spread, spread variation, quote freshness/lifetime, visible top quantities, whether a trade prints at/inside/outside the visible spread, and a theoretical immediate-crossing spread component. It **cannot** measure total realized round-trip cost (see §42).

## 42. Explicit total-cost limitations

The audit does **not** measure and must never be described as measuring: total slippage; queue position; partial-fill probability; market impact; hidden/iceberg liquidity; excluded liquidity; depth beyond the best quote; order-size-dependent execution; latency between decision and execution; the fee tier applicable to a particular account; or complete realized round-trip trading cost. Any future report must state that these components remain unresolved and separate them explicitly from the quoted-spread numbers. The term "true trading cost" / "true-cost audit" is forbidden except when explaining why the claim is forbidden.

## 43. Future outcome thresholds

For a later descriptive phase to record **exactly one** category, on the supported aligned set over the admitted dates. Definitions: `A` = non-zero directional agreement (P(midpoint dir = trade dir | both non-zero)); `TOM` = trade-only-movement share (P(trade dir ≠ 0 ∧ midpoint dir = 0 | trade dir ≠ 0)); `OPP` = opposite-direction share (P(opposite | both non-zero)); `SUB` = sub-spread trade-move share (P(|15s trade move| ≤ one quoted spread)); `MNZ` = non-zero midpoint-support share (P(midpoint dir ≠ 0)). "Consistent" = the category's conditions hold on ≥ 80 % of admitted dates **and** on both months (2024-10, 2024-11).

- **BOUNCE_DOMINATED** — all of: `A < 0.60` **and** `TOM ≥ 0.50` **and** `SUB ≥ 0.60` **and** `OPP ≥ 0.10`, consistent across ≥ 80 % of dates and both months.
- **MIDPOINT_CONFIRMED** — all of: `A ≥ 0.80` **and** `TOM ≤ 0.25` **and** `MNZ ≥ 0.60` **and** `OPP ≤ 0.05` **and** `SUB ≤ 0.40`, consistent across ≥ 80 % of dates and both months.
- **MIXED_MECHANISM** — integrity screens pass but neither pure region's joint conditions are met (e.g. `0.60 ≤ A < 0.80`, or one pure region's statistics are met while another is not, or date/month consistency for a single category falls below 80 %). The explicit indeterminate region. No threshold may be adjusted to force a cleaner category.
- **DATA_INTEGRITY_FAILURE** — any admissibility screen (§30–§36) fails at execution: fewer than 59 admitted dates, or any coverage/integrity/validity/timestamp/freshness/alignment/partition threshold breached. This is fail-closed and **takes precedence** over any descriptive category.

Execution precedence: evaluate `DATA_INTEGRITY_FAILURE` first; only if all screens pass may exactly one of `BOUNCE_DOMINATED` / `MIDPOINT_CONFIRMED` / `MIXED_MECHANISM` be recorded. No category relies on a single statistic; each defines a clear region, with an explicit mixed region and a fail-closed region. No category is defined as a "success" that authorizes modeling.

## 44. Outcome-consequence table (frozen)

| Future result | Consequence (frozen now) |
|---|---|
| **BOUNCE_DOMINATED** | The clean 15s last-trade result is reinterpreted as substantially measurement-level microstructure bounce. No completed verdict is rewritten. The stopped ML arc remains stopped. No quote-feature model is authorized. No strategy/PnL/backtest path is authorized. The mechanism question closes unless a separate, unrelated hypothesis is later proposed. |
| **MIDPOINT_CONFIRMED** | Genuine 15s midpoint-direction information is descriptively supported. No old arc reopens. No model is automatically authorized. No strategy/PnL/backtest path is authorized. At most a later **docs-only** decision memo may consider whether any genuinely new hypothesis is worth preregistration. |
| **MIXED_MECHANISM** | Both bounce and midpoint movement appear material. No predictive claim is upgraded. No threshold may be adjusted to force a cleaner category. At most a later **docs-only** interpretation memo may be proposed. No model or strategy is authorized. |
| **DATA_INTEGRITY_FAILURE** | Stop the mechanism arc. Quarantine or reject the dataset. Do not repair thresholds post hoc. Do not substitute an unapproved source. Remain paused. |

No outcome may revise previous metrics; revise the locked 8/16 bps reference retrospectively; change `STOP_LONGHORIZON_ML_ARC`; or authorize a model, strategy, backtest, or live work.

## 45. Confirmation no outcome reopens a stopped arc

None of the four outcome categories, and no decision in this memo, reopens the stopped long-horizon ML arc, reinterprets Phase 4bn-AR as continuation success, revises AJ/AK/AR/AS metrics, upgrades any predictive claim, or authorizes another classifier / quote-feature model / directional study. `STOP_LONGHORIZON_ML_ARC` is preserved unchanged.

## 46. Prospective-only comparability limitations

A prospective capture is regime-non-comparable to the pre-v002 late-2024 window and, more fundamentally, **cannot be aligned to the 2024 aggTrades** that constitute the result under examination. It could describe only a different, present-day question. Any prospective quoted-spread evidence would apply **prospectively only** and must never be read as revising the completed cost verdicts or the locked 8/16 bps reference (§59). These limitations are why prospective-only fails for §15 (§26).

## 47. Consumed-holdout interpretation

The 14 pre-v002 holdout dates (2024-11-17 … 2024-11-30) were scored under Phase 4bn-AR and are **consumed**. In any future descriptive decomposition they may be used **only** for measurement decomposition. They must never again be described as unseen, untouched, independent predictive confirmation, or a sealed confirmation reserve. The only genuinely-unseen reserves remain the v002 terminal window (2024-12-01…2025-02-28) and the sealed test split (2025-02-14…2025-02-28, `test_rows_loaded = 0`) — neither of which this phase touches or authorizes.

## 48. Negative-results and boundary-codification appendix

Dedicated appendix; **not** a separate execution arc. Status vocabulary: *closed on current data*, *stopped arc*, *rejected family*, *deferred question*, *data-limited*, *mechanism-limited*, *reopenable only with genuinely new admissible evidence*. "Same-data reuse" = whether the already-evaluated pre-v002 dates may be reused, and for what.

| Item | Current status | What is closed | What remains unknown | Evidence required to reconsider | Evidence explicitly insufficient | Same-data reuse | Future phase type if any | Authorization |
|---|---|---|---|---|---|---|---|---|
| Clean 15s directional information (AJ) | Completed positive **information** finding | That aggTrades features carry short-horizon directional information | Whether it is midpoint movement or bounce | Admissible causal top-of-book decomposition | Any aggTrades-only re-analysis; the consumed holdout as confirmation | Descriptive only | Descriptive (this arc — now stopped) | None |
| 15s economic thinness (AJ §19) | Completed finding; closed on current data | That the 15s edge almost never clears 16 bps round-trip (2.47 %/1.20 %) | — | — | Any spread/mid data re-litigating the locked cost | N/A | None | None |
| Single longer-horizon follow-up (AL–AQ) | Spent (the one bounded follow-up) | The AK-authorized single follow-up is used up | — | — | — | Split reused for AR | None | None |
| Long-horizon ML arc (AR→AS) | **Stopped arc** (`STOP_LONGHORIZON_ML_ARC`) | The 5m/30m/1h directional-ML line | Nothing actionable pending genuinely new evidence | A fresh M0-passing mechanism admissible under §19 | New target/feature/weighting on same data | Descriptive only | None (stopped) | None |
| Breakout / pullback / mean-reversion / funding / regime-first families (H0/R3/R1a/R1b-narrow/R2/F1/D1-A; 5m/V2/G1/C1 threads) | Rejected / retained-as-evidence, non-leading | Those strategy families under locked specs | — | A new M0-passing mechanism distinct from the rejection topology | Re-running rejected families on same data | N/A | None | None |
| Consumed pre-v002 holdout (14 dates) | Data-limited; consumed | Its use as unseen confirmation | — | An untouched reserve (v002 terminal / sealed test) | Reusing it as independent confirmation | Descriptive decomposition only | Descriptive only | None |
| v002 terminal + sealed-test reserves | Reserved, untouched (`test_rows_loaded = 0`) | — | Whether any genuinely new hypothesis would ever justify spending them | A preregistered, M0-passing, single-use plan | Casual/iterative use | Not used here | Docs-only if ever | None |
| Top-of-book mechanism realism (this arc) | **Mechanism-limited + data-limited; stopped this phase** | Whether the 15s label is bounce or midpoint | The decomposition itself | Genuinely new **admissible** top-of-book data (documented schema/timestamps/order/coverage/terms) | The undocumented, out-of-order, cessation-reported archive; regime-non-comparable prospective capture | Descriptive only if ever admissible | Docs-only admissibility re-check first | None |
| Spread / slippage / mid / depth / impact realism | Data-limited; open but blocked | — | Executable-cost realism | Admissible depth + top-of-book + execution data | aggTrades-only; quoted spread alone (cannot express total cost) | N/A | Behind §19 M0 gate | None |
| §19 M0 boundary (4bn-AE) | Binding, preserved | Any strategy/PnL/backtest/live path | — | A separate future M0-style mechanism-admissibility memo clearing all twelve clauses | Any baseline metric, however strong | N/A | M0 memo (docs-only) | None |

## 49. Expected-information-gain assessment

Expected decision-relevant information gain is **low**. The project already documents (AJ/AK/AR/AS) that the 15s aggTrades label "may embed bid-ask bounce" — the bounce hypothesis is a *known, acknowledged limitation*, not a mystery. A clean decomposition would refine "may embed" into "does / does not," which is epistemically valuable as a general methodological lesson (how future hypotheses should define price; guarding against false confidence in last-trade labels), but:
- it changes **no** currently-authorized action (the arc is stopped; no model/strategy is authorized);
- the *general* lesson does not require decomposing this *specific* spent result;
- the only data that could decompose this specific result is inadmissible (§25) or non-comparable (§26).

So the marginal gain over what is already recorded is small, and the means to obtain even that small gain is unavailable on admissible terms.

## 50. Cost and resource assessment

Retrospective (if data were admissible): a checksum-verified acquirer, a mandatory evidence-preserving reorderer (#305), a strict causal aligner, and a descriptive metric computer; low-tens of GiB storage within Phase 4bn-L envelopes with the ≥500 GiB free-space preflight; meaningful engineering time. Prospective: a sustained capture/monitoring service over weeks-to-months with growing storage. **Both cost real engineering and storage; §49 shows the payoff is low; §25–§26 show the retrospective data is inadmissible and the prospective data cannot answer the question.** Cost/benefit favors remaining paused.

## 51. Rescue-risk assessment

Concentrating effort on the project's **only** positive result (the clean 15s finding) creates real rescue pressure — a temptation to read `MIDPOINT_CONFIRMED` as reviving the directional line or as license for a quote-feature model. The outcome-consequence table (§44) neutralizes this by construction: no outcome authorizes a model, reopens the arc, or upgrades a claim. Separately, prospective quoted-spread evidence risks being read as revising completed cost verdicts and the locked 8/16 bps reference — forbidden retrospectively (§59). These rescue/relitigation risks are additional weight **against** proceeding.

## 52. Case for retrospective admission

The honest best case: a futures um daily bookTicker archive for BTCUSDT **does** exist (contradicting the project's earlier "Hist: FALSE"), with `.CHECKSUM` companions; the required window is in 2024, plausibly before the reported cessation; the known out-of-order defect (#305) is in principle addressable by the evidence-preserving reorder this memo freezes (§31, §35); and the full admissibility contract and outcome thresholds are freezable (they are, §29–§44). If coverage of all 59 dates could be confirmed and the archived timestamp semantics validated, a model-free decomposition would be clean and low-rescue.

## 53. Case for prospective-only admission

The honest best case: live `<symbol>@bookTicker` capture uses officially-documented field semantics, is self-provenanced, avoids the archive's ordering/cessation defects, and was already designed (Phase 4au/4av). It could support a *generic present-day* bounce-vs-midpoint description of BTCUSDT 15s last-trade direction.

## 54. Case for stopping / remain paused

Retrospective coverage of the required 2024-10-02…2024-11-30 window is **unconfirmed** from Tier-1 metadata and reportedly ceased in 2024; the archive is **undocumented** in Tier-1 specification; its timestamp/sequencing semantics are undocumented and **documented-defective** (#305, closed with no fix); provenance/immutability/terms are inadequate; and the project's own prior admissibility finding recorded the family as unavailable. Resolving these would require prohibited data acquisition, which counts against admission. Prospective capture cannot align to the 2024 trades and so **cannot answer the actual question**, at real cost and with rescue/relitigation risk. The expected decision-relevant information gain is low regardless of outcome (the "autopsy" objection, §14/§49), and no result can change a currently-authorized action. Remaining paused is preferable to weak, incomplete, or unverifiable data.

## 55. Exact decision

**STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE.**

Phase result state:
`TOP_OF_BOOK_MECHANISM_ADMISSIBILITY_MEMO_COMPLETE__STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`

Neither retrospective nor prospective data can answer the mechanism question credibly and proportionately: the retrospective bookTicker archive is undocumented in Tier-1 specification, of unconfirmed coverage for the required window, reportedly ceased in 2024, and carries an unremediated documented out-of-order defect with undocumented timestamp semantics (provenance and causal-alignment validity inadequate); the prospective analogue is regime-non-comparable and cannot be aligned to the 2024 trades, so it does not answer §15, at disproportionate cost and with rescue/relitigation risk; and the expected information gain does not justify the cost. A causal, falsifiable future contract **is** frozen here (§29–§44), but no currently-available source can execute it on admissible terms.

## 56. Exact decision-precedence mapping

1. **Retrospective first** — evaluated (§24–§25): **fails** (coverage unestablished; sequencing defective/undocumented; provenance inadequate; resolving requires prohibited acquisition → counts against).
2. **Prospective-only next** — evaluated (§26): **fails** (cannot answer the retrospective question; non-comparable; disproportionate; rescue/relitigation risk).
3. **Neither credible and proportionate → STOP** (§55).
4. Not chosen because Candidate A was previously recommended — the independent review is non-binding and was weighed against the committed record; the STOP follows from the evidence, not from deference.
5. Remaining paused is preferred over weak/incomplete/unverifiable data.
6. No fourth decision invented.
7. No genuine official-source contradiction blocks the decision (the archive-exists vs README-silence tension is resolved as "undocumented-but-present," §20 — informative, not a blocking contradiction), so the `..._BLOCKED__OFFICIAL_SOURCE_CONTRADICTION` state is **not** used.
8. Documentation uncertainty unresolvable without prohibited acquisition counted **against** admission.

## 57. Allowed claims

- The 15s aggTrades last-trade directional label **may** embed bid–ask bounce; whether it does is undetermined and, on current admissible data, **cannot** be determined.
- An undocumented futures um daily bookTicker archive for BTCUSDT **exists** on `data.binance.vision` with `.CHECKSUM` companions, but is **undocumented in Tier-1 specification**, carries a documented unremediated out-of-order defect (issue #305), reportedly **ceased updating in 2024**, and has **unconfirmed** coverage of the required 2024-10-02…2024-11-30 window.
- The retrospective top-of-book source is therefore **inadmissible**; the prospective analogue **cannot answer** the specific mechanism question.
- A causal, falsifiable data-admissibility contract, causal-alignment rule, model-free descriptive metric registry, and outcome categories with frozen consequences are **preregistered** here and would apply **only** to genuinely-new admissible data.

## 58. Forbidden claims

- That the 15s result is (or is not) bounce — undetermined.
- That any top-of-book measurement measures "true trading cost" / is a "true-cost audit."
- That any prospective or future quoted-spread evidence revises Phase 4bn-AJ/AK/AR/AS metrics, any completed strategy rejection, any prior materiality decision, or the locked 8 bps/side · 16 bps round-trip reference — such evidence applies **prospectively only**.
- That the consumed pre-v002 holdout is unseen, untouched, independent predictive confirmation, or a sealed reserve.
- That this phase reopens the stopped ML arc, authorizes any model / quote-feature model / classifier / directional study / strategy / backtest / live work, or changes `STOP_LONGHORIZON_ML_ARC`.
- That the aggTrades stack can express total slippage, depth, impact, hidden liquidity, queue position, or complete round-trip cost.

## 59. Preserved project locks

- `STOP_LONGHORIZON_ML_ARC` (Phase 4bn-AS) — preserved.
- Phase 4bn-AE claim scope and §19 M0 strategy/PnL/backtest hard boundary — preserved and unsoftened; any future strategy/PnL/backtest/live path requires a separate M0-style mechanism-admissibility memo clearing all twelve M0 clauses (M0.5 cost realism at 8/16 bps; M0.8 data feasibility; §7.D microstructure lane `NOT_RECOMMENDED_NOW`).
- Locked economic context: **8 bps per side / 16 bps round-trip** — binding and descriptive for all completed phases and verdicts; no new spread observation may retrospectively change Phase 4bn-AJ/AK/AR/AS or any completed materiality decision; future quoted-spread evidence applies prospectively only.
- Phase 4bn-AP contract, Phase 4bn-AQ dataset identity, Phase 4bn-AR evidence, Phase 4bn-AS decision — preserved.
- All prior strategy-arc verdicts (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A; 5m / V2 / G1 / C1 threads) — preserved.
- Manifest immutability: `research_eligible = False`; `eligibility_gate_status = PENDING`; `flip_research_eligible(...)` always-raises invariant (Phase 4aw) — preserved, never invoked.
- Phase 4bb-F canonical sidecar policy and Phase 4bn-L storage/budget caps — preserved as the shape any future (unauthorized) acquisition would have to honor.

## 60. Recommended state

**Remain paused.** The top-of-book mechanism arc is stopped for data inadmissibility; no successor phase is recommended. The frozen contract (§29–§44) remains available only if genuinely-new, fully-admissible top-of-book data (documented schema, timestamps, ordering, coverage, immutability, and terms) ever appears — at which point the appropriate next step would itself be a **docs-only** admissibility re-check, not acquisition.

## 61. Explicit no-successor execution statement

**No successor execution is authorized.** This phase authorizes no data acquisition, no capture, no download, no parsing, no normalization, no alignment, no label/feature construction, no model, no strategy, no signals, no PnL, no backtest, no replay, no simulated fill, no paper/shadow/live/exchange-write, and no successor phase of any kind. It commits documentation only and leaves the project **paused**.
