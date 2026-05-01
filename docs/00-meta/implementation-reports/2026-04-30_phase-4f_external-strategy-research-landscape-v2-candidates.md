# Phase 4f — External Strategy Research Landscape and V2 Hypothesis Candidate Memo (docs-only)

**Authority:** Operator authorization for Phase 4f (return to strategy research because the absence of a viable strategy is the main blocker, per Phase 4e §31 deferred decision); Phase 4e §28 (does NOT authorize implementation); Phase 3t (5m research thread closure); Phase 3u §10 (Phase 4 / 4a prohibition list); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 2i §1.7.3 project-level locks; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/ai-coding-handoff.md`; `docs/00-meta/implementation-ambiguity-log.md`; `docs/03-strategy-research/v1-breakout-strategy-spec.md`; `docs/03-strategy-research/v1-breakout-backtest-plan.md`; `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`; `docs/04-data/data-requirements.md`; `docs/04-data/live-data-spec.md`; `docs/07-risk/stop-loss-policy.md`; `docs/07-risk/position-sizing-framework.md`; `docs/07-risk/exposure-limits.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4f — **External Strategy Research Landscape and V2 Hypothesis Candidate Memo** (docs-only). Surveys external academic and practitioner evidence on systematic trading strategies, evaluates transferability to Prometheus, and predeclares a single bounded V2 candidate hypothesis family. **Phase 4f does NOT backtest. Phase 4f does NOT implement. Phase 4f does NOT download data. Phase 4f does NOT create a strategy variant. Phase 4f does NOT revise any previous verdict. Phase 4f does NOT claim profitability. Phase 4f does NOT authorize paper/shadow/live/exchange-write.**

**Branch:** `phase-4f/external-strategy-research-landscape-v2-candidates`. **Memo date:** 2026-04-30 UTC.

---

## 1. Summary

The post-Phase-4e boundary leaves the project with: a clean strategy-agnostic local runtime foundation (Phase 4a), a clean repository quality gate (Phase 4b/4c), a complete reconciliation-model design specification (Phase 4e) — and **no viable strategy candidate**. R3 remains V1 breakout baseline-of-record but is aggregate-negative on R-window expR; R2 / F1 / D1-A are terminal under current locked spec; the 5m research thread is operationally complete and closed. The operator has explicitly returned focus to strategy research because the absence of a viable strategy is the main blocker.

Phase 4f is a docs-only external research memo. It surveys high-quality academic evidence on time-series momentum, trend-following, breakout strategies, and crypto-market-structure indicators; it distinguishes what institutional algorithmic trading actually does from what is realistically transferable to a single-symbol, fake-adapter-only, supervised v1 trading project; and it predeclares **one** bounded V2 candidate hypothesis family — *V2 — Participation-Confirmed Trend Continuation* — together with a bounded predeclared feature list, a bounded predeclared timeframe matrix, predeclared exclusion rules, and predeclared validation requirements.

**Phase 4f recommends Option B (docs-only V2 strategy-spec memo for Participation-Confirmed Trend Continuation) as primary**, with **Option C (docs-only V2 data-requirements and feasibility memo) as conditional secondary**. Option A (remain paused) is procedurally acceptable but understates the operator-stated motivation. Option D (data acquisition) is acceptable only after a separately authorized data-requirements memo. Option E (immediate exploratory backtests) is rejected because backtesting before predeclaration is exactly the data-snooping pattern Bailey, Borwein, López de Prado, and Zhu document as a leading cause of out-of-sample failure ([Bailey, Borwein, López de Prado, Zhu 2014](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253)). Option F (paper-shadow / live-readiness / exchange-write) is forbidden / not recommended.

**Verification (run on the post-Phase-4e-merge tree, captured by Phase 4f):**

- `ruff check .`: **All checks passed!** (whole-repo Ruff quality gate fully clean).
- `pytest`: **785 passed in 15.54s.** No regressions.
- `mypy` strict: **Success: no issues found in 82 source files.**

**No retained-evidence verdict revised.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved verbatim. **No policy locks changed.** **No code, tests, scripts, data, manifests modified by Phase 4f.** **No data acquired or modified.** **Recommended state remains paused.** **No successor phase has been authorized.**

---

## 2. Authority and boundary

Phase 4f operates strictly inside the post-Phase-4e-merge boundary:

- **Predeclaration discipline preserved verbatim.** Phase 3o §5–§10; Phase 3p §4–§8; Phase 3r §8; Phase 3s diagnostic outputs; Phase 3t consolidation; Phase 3u §10 / §11; Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 3x §6 / §10 (Phase 4a strict-subset framing); Phase 4a's anti-live-readiness statement; Phase 4d review; Phase 4e reconciliation-model design memo.
- **Phase-gate governance respected.** `docs/12-roadmap/phase-gates.md` unchanged.
- **Project-level locks preserved verbatim.** §1.7.3 (BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets).
- **Phase 2f thresholds preserved verbatim.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6.
- **Retained-evidence verdicts preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other.
- **Safety rules preserved verbatim.** `.claude/rules/prometheus-safety.md`.
- **MCP and secrets rules preserved verbatim.** `.claude/rules/prometheus-mcp-and-secrets.md`.
- **Phase 4a–4e runtime / quality / reconciliation governance preserved verbatim.**

Phase 4f adds *external research synthesis and forward-looking predeclared hypothesis content* — without modifying any prior phase memo, any data, any code, any rule, any threshold, any manifest, any verdict, any lock, or any gate.

---

## 3. Starting state

```text
branch:           phase-4f/external-strategy-research-landscape-v2-candidates
parent commit:    da0f7c428ec8da0a4fb9eaf4e7bb96e726f52d9c (post-Phase-4e-merge housekeeping)
working tree:     clean before research
main:             da0f7c428ec8da0a4fb9eaf4e7bb96e726f52d9c (unchanged)

Phase 4a foundation: merged.
Phase 4b/4c cleanup: merged.
Phase 4d review:     merged.
Phase 4e reconciliation-model design memo: merged.
Repository quality gate: fully clean.
research thread:     5m research thread operationally complete (Phase 3t).
v002 datasets:       locked; manifests untouched.
v001-of-5m:          trade-price research-eligible; mark-price research_eligible:false.
```

---

## 4. Why this research phase exists

The cumulative recommendation across Phase 3k → Phase 4e was "remain paused" — a posture that preserved framework discipline while no live-eligible strategy emerged. The operator has now made the reverse decision explicit: *the absence of a viable strategy is the main blocker; return focus to strategy research.* Phase 4f is the structured way to do that without violating the project's anti-data-snooping discipline:

1. **Predeclaration before evidence.** Bailey et al. ([2014](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253)) document that picking the best of many in-sample variants and treating it as "the strategy" is the leading cause of out-of-sample failure. The corrective is *predeclare a bounded hypothesis before looking at data.* Phase 4f predeclares one V2 candidate family, a bounded feature list, a bounded timeframe matrix, and exclusion rules.
2. **External evidence before re-running anything internal.** The project has run V1 / R2 / F1 / D1-A and the 5m diagnostics on internal data. Going back to that data without external grounding risks over-fitting to the same patterns that already failed framework discipline. Phase 4f draws on academic and practitioner sources external to the project to inform the V2 hypothesis.
3. **Anti-rescue discipline.** Phase 3o §6 / Phase 3p §8 / Phase 3r §8 / Phase 3t §13 / Phase 3u §10 / Phase 3v §13 / Phase 3w §14 / Phase 3x §6.7 / Phase 4a §22 all forbid post-hoc rescue of failed candidates. V2 must be a genuinely new ex-ante hypothesis, not a re-parameterized retained-evidence successor.
4. **Bounded-not-unbounded search.** Without a memo like this, the next phase risks an unbounded feature / parameter search. Phase 4f deliberately bounds the V2 design space.

---

## 5. Research method

Phase 4f used only:

- **Project documents** (per §Required reading) — read on the post-Phase-4e-merge tree.
- **Web research** via WebSearch (no WebFetch was needed; result-summary content was sufficient for the topics surveyed).
- **No code execution** other than the required `ruff` / `pytest` / `mypy` verification commands.
- **No data acquisition.**
- **No backtesting.**

For each topic, the memo prefers primary academic sources (NBER, Journal of Finance, Journal of Financial Economics, BIS, arXiv, SSRN). Practitioner blogs are used as weak supporting context only and are labelled as such. Influencer / social-media / paid-course claims are excluded from the evidence base.

---

## 6. Source-quality policy

- **Strong evidence** (academic / institutional): peer-reviewed journals, NBER working papers, BIS working papers, AQR / institutional-research white papers, arXiv preprints with multiple citations or peer-reviewed publication.
- **Weak supporting context** (practitioner): exchange documentation, exchange research blogs, well-respected practitioner blogs (e.g., QuantPedia, AQR Insights). Used to confirm or qualify strong evidence; never used as standalone justification for a hypothesis.
- **Excluded**: YouTube, X/Twitter, Discord, Telegram, Reddit, influencer claims, paid courses, unverifiable "high win rate" systems.
- **Conflict resolution**: where strong sources disagree, the memo summarizes the conflict rather than picking a side.
- **Citations**: every non-obvious factual claim in §§7–17 is hyperlinked to its source.

---

## 7. What institutional algorithmic trading actually does

The systematic-trading literature divides institutional algorithmic activity into roughly five categories ([Wikipedia: Algorithmic trading](https://en.wikipedia.org/wiki/Algorithmic_trading); [Wikipedia: Systematic trading](https://en.wikipedia.org/wiki/Systematic_trading)):

| Category | What it tries to exploit | Infrastructure required | Transferable to Prometheus now? |
|---|---|---|---|
| **Market making / liquidity provision (HFT-style)** | Bid-ask spread; rebates per share; very short-horizon mean reversion / order-flow imbalance ([SEC HFT literature review](https://www.sec.gov/marketstructure/research/hft_lit_review_march_2014.pdf); [QuantInsti taxonomy](https://www.quantinsti.com/articles/types-trading-strategies/)). | Co-located servers, microsecond-grade latency, direct exchange connectivity, tick-level data, dedicated risk/quoting engine, market-maker rebate agreements with venue. | **NO.** Latency-dependent; requires authenticated exchange access, depth-of-book feeds, and a market-maker agreement. Forbidden by `.claude/rules/prometheus-safety.md` (no exchange-write before approved gate; no real Binance keys in early phases). |
| **Systematic trend-following / managed futures (CTA-style)** | Time-series momentum; trend persistence over weeks-to-months across diverse asset classes ([Moskowitz, Ooi, Pedersen 2012](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2089463); [Hurst, Ooi, Pedersen 2017](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2993026)). | Daily-bar or higher-resolution data; standard execution venues; volatility-targeted position sizing; diversified universe (typically 50+ markets). | **PARTIALLY.** The *signal mechanic* (price-based time-series momentum) is reproducible on Bitcoin perpetual futures with public data. The *diversification advantage* (50+ markets) is NOT available — Prometheus v1 is BTCUSDT only per §1.7.3. |
| **Statistical arbitrage / multi-signal ML prediction** | Short-horizon cross-sectional return predictability; pairs / basket relative-value; ML feature combinations ([QuantInsti taxonomy](https://www.quantinsti.com/articles/types-trading-strategies/)). | Multi-asset universe; sub-second to multi-minute holding periods; large feature engineering pipeline; substantial validation infrastructure to avoid overfitting ([Bailey et al. 2014](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253)). | **NO** for v1. Single-symbol scope rules out cross-sectional. ML-first black-box approaches are explicitly out of scope per `current-project-state.md` (Phase 4 ML feasibility "not authorized; not proposed"). |
| **Crypto liquidity provision / on-exchange market making** | Spread + maker rebates + funding-rate edge in perpetuals ([BIS Working Paper No. 1087: "Crypto carry"](https://www.bis.org/publ/work1087.pdf)). | Authenticated API; high-throughput connectivity; risk engine; multiple-exchange arbitrage capability. | **NO.** Same prohibitions as institutional market making. |
| **Crypto carry / funding-rate arbitrage** | Persistent positive funding when retail/leveraged longs dominate; spot-vs-perpetual basis ([BIS WP 1087](https://www.bis.org/publ/work1087.pdf); [Schmeling, Schrimpf, Todorov 2023](https://www.bis.org/publ/work1087.pdf)). | Spot-and-perp simultaneous exposure (delta-neutral); cash-and-carry execution; cross-venue capability for capital efficiency. | **NO** for v1. Cash-and-carry requires *spot* exposure; v1 live scope is BTCUSDT *perpetual* only. The crypto-carry literature is informative as **context** (funding-rate dynamics; what drives funding) but is not a standalone v1 strategy. |

**Net institutional-trading takeaway:** the only category whose *signal mechanic* is realistically transferable to a single-symbol, fake-adapter-only, supervised project is **systematic trend-following / time-series momentum**. The diversification advantage is forfeit; the signal-mechanic literature is the relevant evidence base.

---

## 8. What is transferable to Prometheus

- **Time-series momentum / trend-continuation signal logic** ([Moskowitz, Ooi, Pedersen 2012](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2089463)). Adapted to a single symbol.
- **Donchian-channel breakout entry logic** ([Brock, Lakonishok, LeBaron 1992](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1992.tb04681.x)) and the Turtle-system formulation.
- **Volatility-adjusted position sizing** (ATR-based; per Turtle-system tradition; matches Prometheus' existing stop-distance × ATR sizing in `position-sizing-framework.md`).
- **Multi-timeframe trend-bias filtering** (V1 already uses 1h bias on 15m signals; consistent with the literature's higher-timeframe / lower-timeframe layering).
- **Time-of-day / session bucketing** (academic and practitioner evidence on intraday seasonality in BTC; [Hattori 2020 / 2024 on UK tea time peak](https://link.springer.com/article/10.1007/s11156-024-01304-1); [QuantPedia intraday seasonality](https://quantpedia.com/are-there-seasonal-intraday-or-overnight-anomalies-in-bitcoin/); [Eross et al. 2019 on BTC intraday volume/volatility periodicity](https://www.sciencedirect.com/science/article/abs/pii/S1544612319301904)).
- **Funding-rate context as a regime filter or cost-aware weighting** (BIS WP 1087; informative but used here as *context*, not as a standalone signal).
- **Public bulk-archive data** ([data.binance.vision](https://data.binance.vision/) / [binance/binance-public-data](https://github.com/binance/binance-public-data)). Klines, mark-price klines, funding-rate history, premium-index klines, open-interest historical metrics, long/short ratio metrics — all available via the public unauthenticated bulk archive used by Phase 3q.
- **Volume and taker-flow indicators where they are publicly aggregated** (Binance bulk archive aggTrades; CryptoQuant / Coinalyze / Coinglass derived metrics — but only where reproducible from public sources).

---

## 9. What is not transferable to Prometheus

- **HFT / market making latency edge.** Prometheus runs on a NUC; latency is in the tens-of-milliseconds region, not microseconds.
- **Cross-sectional / multi-asset diversification.** v1 is BTCUSDT only.
- **Authenticated / private-endpoint feeds.** User-stream, wallet-state, account-balance feeds, private order-book deltas are forbidden in this project posture.
- **ML-first black-box forecasting.** Excluded per `current-project-state.md` ("Phase 4 ML feasibility not authorized").
- **Maker-rebate-dependent strategies.** Phase 1.7.3 / safety rules forbid live exchange-write before approved gate; no rebate agreement exists.
- **Cross-venue arbitrage.** Single venue (Binance USDⓈ-M); no cross-venue capability.
- **Pump-and-dump / manipulation patterns.** Documented in the literature ([arxiv 2504.15790 Microstructure and Manipulation](https://arxiv.org/abs/2504.15790)) but not appropriate for a supervised, framework-disciplined project.

---

## 10. Evidence on trend following and time-series momentum

The strongest, most-replicated evidence in the systematic-trading literature is for **time-series momentum (TSMOM)** — going long markets with positive recent returns and short markets with negative recent returns.

- **[Moskowitz, Ooi, Pedersen 2012](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2089463)** documented strong positive predictability from a security's own past returns across 58 diverse futures and forwards over 25+ years; the 12-month past return is a positive predictor of the next month's return; the trend persists ~12 months and partially reverses thereafter. Diversified TSMOM portfolios produced significant abnormal returns with low correlation to standard factors and performed best during crisis periods.
- **[Hurst, Ooi, Pedersen 2017](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2993026)** extended this to over a century of data (1903 onwards) across 67 markets; trend-following was profitable in every decade examined; correlations to traditional asset classes remained low; "crisis alpha" was particularly notable.
- **[Brock, Lakonishok, LeBaron 1992](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1992.tb04681.x)** tested moving-average and trading-range-breakout rules on the Dow Jones (1897–1986); rule returns were not consistent with standard null models (random walk, AR(1), GARCH-M, EGARCH). This is the seminal academic source for *breakout* rules specifically.
- **Crypto evidence:** [Liu & Tsyvinski 2018/2021 (NBER WP 24877 / Review of Financial Studies)](https://www.nber.org/papers/w24877) found that cryptocurrency returns are predictable by crypto-specific factors, with a strong time-series momentum effect. [Time-Series and Cross-Sectional Momentum in the Cryptocurrency Market (Han et al. 2024)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4675565) confirmed time-series momentum is robust across data frequencies and that overreaction explains a significant fraction of the time-series momentum premium. [Bitcoin intraday time-series momentum (CentAUR / Reading 2021)](https://centaur.reading.ac.uk/100181/3/21Sep2021Bitcoin%20Intraday%20Time-Series%20Momentum.R2.pdf) reports both intraday momentum and reversal patterns at higher frequencies.

**Synthesis:** trend-following / TSMOM is the most evidence-backed signal mechanic available to a single-asset systematic trader. The Prometheus V1 breakout strategy was already a TSMOM-flavoured design; the fact that V1 / R2 / F1 / D1-A failed framework discipline does not invalidate the signal-mechanic literature — it suggests the *mechanism* is real but the *implementation choices* (entry trigger, stop construction, exit logic, regime filtering) need re-design, not abandonment.

---

## 11. Evidence on breakout / trend-continuation strategies

- **[Brock, Lakonishok, LeBaron 1992](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1992.tb04681.x)** — original academic evidence for trading-range-breakout rules.
- **[Donchian-channel / Turtle-system formulation](https://www.altrady.com/blog/crypto-trading-strategies/turtle-trading-strategy-rules)** (practitioner; weak supporting context) — 20-day breakout (System 1) and 55-day breakout (System 2); volatility-adjusted position sizing using ATR; explicit exit rules and stop placement. The Turtle program of Richard Dennis reportedly earned $175M; the system has been backtested across asset classes.
- **[Volatility compression → expansion patterns](https://www.bookmap.com/blog/narrow-range-breakouts-why-volatility-compression-leads-to-expansion)** (practitioner; weak supporting context) — ATR percentile drops below threshold, then breakouts on volume expansion; Mark Minervini's VCP framework (institutional-equities flavour).
- **[Quantifying Volatility Compression and Expansion (Manamala 2025)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5288827)** — recent SSRN preprint formalizing volatility-compression-then-expansion as a quantitative pattern.

**Synthesis:** the trading-range-breakout literature is consistent with the V1 breakout-continuation framing but adds two refinements that V1 / R2 / F1 / D1-A did not fully exploit:
1. **Volatility compression as a precondition.** A breakout from low-volatility consolidation has historically had different statistical character from a breakout in already-elevated volatility.
2. **Volume / participation expansion as confirmation.** A breakout without volume expansion is more likely to be a false breakout in the practitioner literature; this echoes the academic finding that volume-flow imbalance has predictive content (§13).

---

## 12. Evidence on volume and order flow

- **[Easley, O'Hara, Yang, Zhang 2024 (Microstructure and Market Dynamics in Crypto Markets, SSRN)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4814346)** — order-flow imbalance produces positive correlation in price changes and elevated Roll-measure / Amihud / Kyle's λ / VPIN values in crypto; microstructure measures predict volatility changes; "trend following could be exploited by sophisticated trading algorithms."
- **[Bitcoin wild moves: Evidence from order flow toxicity and price jumps (ScienceDirect 2025)](https://www.sciencedirect.com/science/article/pii/S0275531925004192)** — Volume-Synchronised Probability of Informed Trading (VPIN) significantly predicts future price jumps; positive serial correlation in VPIN and jump size suggests persistent asymmetric-information / momentum effects.
- **[Fragmentation, Price Formation and Cross-Impact in Bitcoin Markets (T&F 2022)](https://www.tandfonline.com/doi/full/10.1080/1350486X.2022.2080083)** — microstructural features explain 10–37% of variation in 500-millisecond future returns in fragmented bitcoin markets; trade-flow imbalance has explanatory power.
- **[CVD / cumulative volume delta](https://bookmap.com/blog/how-cumulative-volume-delta-transform-your-trading-strategy)** (practitioner; weak supporting context) — measures net taker-buy-minus-taker-sell volume; widely used as a participation / flow indicator. CryptoQuant publishes a 90-day spot-taker CVD and a 90-day futures-taker CVD.

**Synthesis on volume/flow as signal vs. confirmation vs. regime:**

- **As pure signal** (trade volume only, no price context): weak and mixed evidence; volume alone is a poor predictor.
- **As confirmation** (volume z-score / relative volume on a price breakout): consistent practitioner support and academic support via VPIN / order-flow-imbalance work; Phase 4f treats this as the strongest volume role.
- **As regime filter** (high-volume vs. low-volume periods): practitioner support for filtering breakouts to high-participation hours / sessions; consistent with intraday-seasonality evidence (§14).
- **As exhaustion / liquidation risk** (extreme volume + extreme funding + extreme long/short ratio): documented in liquidation-cascade analyses ([XT / Medium 2026 microstructure piece](https://medium.com/@XT_com/bitcoin-futures-market-microstructure-liquidation-cascades-funding-regimes-and-open-interest-978b107b4889); [SSRN 5611392 — Anatomy of the Oct 10–11, 2025 cascade](https://papers.ssrn.com/sol3/Delivery.cfm/5611392.pdf?abstractid=5611392&mirid=1)). Useful as a *cost / risk* lens, less so as an entry signal.

---

## 13. Evidence on crypto derivatives-flow indicators

- **Funding rate.** [BIS WP 1087 "Crypto carry" (Schmeling, Schrimpf, Todorov)](https://www.bis.org/publ/work1087.pdf) documents average crypto carry of 6–8% p.a. with peaks above 40%; carry is driven by trend-chasing retail leverage in boom periods and arbitrage-capital scarcity. Carry strongly predicts liquidations: a 10% increase in standardized carry predicts a 22% (of OI) increase in short-position liquidations over the next month. **Implication:** funding-rate percentile is informative as a *regime / cost* lens.
- **Open interest (OI).** Practitioner evidence ([dex.gate.com 2026](https://dex.gate.com/crypto-wiki/article/what-are-crypto-derivatives-market-signals-how-futures-open-interest-funding-rates-and-liquidation-data-predict-market-movements-20260204)) suggests rising OI alongside rising prices indicates new long positioning; rising OI alongside falling prices indicates new short positioning. The OI-delta concept (change in OI between periods) is a derivable feature from public bulk archives.
- **Taker buy/sell imbalance.** Available on Binance public archive (long-short-ratio, taker-buy-sell-volume metrics). Documented predictive content via VPIN / order-flow-imbalance work (§12). Notable caveat: spot-CVD and aggregated-perpetual-CVD are not the same instrument; methodology must be explicit.
- **Long/short ratio.** [Binance research (educational)](https://www.binance.com/en/blog/futures/what-is-longshort-ratio-and-what-does-it-convey-in-cryptocurrency-futures-6728490800036398885) distinguishes account-ratio (gauge retail sentiment) from top-trader-position-ratio (top-20% by margin balance — proxy for whale sentiment). Extreme readings on either are weakly contrarian / liquidation-risk indicators per practitioner sources.
- **Mark-price vs. trade-price divergence.** Phase 3s Q6 already documented this for retained-evidence trade populations (D1-A: mark stops trigger 1.3–1.8 5m bars after trade stops would have; R3 / R2 / F1: < 1 bar lag). The Phase 3v §8 stop-trigger-domain governance encodes the divergence as a first-class label scheme.
- **Liquidation cascades.** [SSRN 5611392 (Ali 2025)](https://papers.ssrn.com/sol3/Delivery.cfm/5611392.pdf?abstractid=5611392&mirid=1) — Oct 2025 cascade; high cross-asset contagion (~20% stronger than 2018 spillovers); reflexive feedback between OI / funding / liquidations. Useful as cost-aware risk regime; not a clean entry signal.

**Synthesis:** derivatives-flow indicators are most defensible as **context / regime / cost-awareness** features rather than primary entry signals. The strongest individual signal-content is in funding-rate percentile (regime) and taker-flow imbalance (confirmation). The literature does not support a "trade liquidation cascades for free profit" narrative; cascades are a cost-and-volatility regime, not an exploitable mispricing for a supervised single-symbol bot.

---

## 14. Evidence on timeframes and session effects

- **Intraday seasonality in BTC.** [Eross, Urquhart, Wolfe 2019](https://www.sciencedirect.com/science/article/abs/pii/S1544612319301904) — BTC trading volume and volatility exhibit deterministic time-of-day periodicities concentrated in EU and US trading hours. [Hattori 2024 (Review of Quantitative Finance and Accounting)](https://link.springer.com/article/10.1007/s11156-024-01304-1) — trading activity, volatility, and illiquidity all peak between 16:00–17:00 UTC ("UK tea time"); 14:00–15:00 GMT peak overlaps NYSE open and is largely absent on weekends. [QuantPedia intraday seasonality](https://quantpedia.com/are-there-seasonal-intraday-or-overnight-anomalies-in-bitcoin/) — a trivial 21:00→23:00 UTC "buy-and-hold-for-2-hours" rule reportedly produces ~33% annualized return with 21% volatility (practitioner; weak evidence; cited only as illustration of intraday non-stationarity).
- **Time-of-day periodicities in BTC volume/volatility.** [Eross et al. 2019](https://www.sciencedirect.com/science/article/abs/pii/S1544612319301904) — the stock market's hours matter for BTC even though BTC is 24/7.
- **Timeframe trade-offs (qualitative consensus from the literature):**
  - **5m**: high signal density, high noise, high cost-sensitivity. The Phase 3s 5m diagnostics are descriptive only and explicitly do not authorize a 5m strategy. *Use 5m only as a timing diagnostic, not as a primary signal.*
  - **15m**: V1's signal timeframe; balances density and noise. Acceptable but not the only choice.
  - **30m**: reduces noise vs. 15m; reduces density. Worth considering as a signal-timeframe alternative.
  - **1h**: V1's bias timeframe; common in practitioner systematic crypto. Stronger trend persistence; lower signal density.
  - **4h**: longer trend; very low density; matches "swing" practitioner literature; would imply small trade count over the ~4-year v002 trade range.
  - **Daily**: matches the Moskowitz / Hurst / Brock canonical literature; very low signal density on a single symbol; would yield ~1500 daily bars over v002 — small N for robust validation.

**Synthesis:** the academic literature consistently shows higher-timeframe signals have stronger trend persistence and lower cost-sensitivity but lower signal density. The Phase 4f recommendation is **15m / 30m / 1h** as the V2 candidate signal-timeframe set, with 1h or 4h as the bias timeframe. **5m is excluded as a primary signal timeframe** but acceptable as a timing-only diagnostic per Phase 3o §6 / Phase 3p §8.

---

## 15. Crypto perpetual futures market-structure implications

- **Perpetual futures pricing.** [Ackerer, Hugonnier, Jermann 2024 (NBER WP 32936; Mathematical Finance forthcoming)](https://www.nber.org/system/files/working_papers/w32936/w32936.pdf); [He & Manela 2024 (arXiv 2212.06888)](https://arxiv.org/html/2212.06888v5) — perpetual futures pricing is now formalized with explicit funding-rate mechanics; perpetual price = discounted expected spot at a random time reflecting the funding specification.
- **Mark-price vs. trade-price.** Mark-price is a smoothed weighted reference designed to mitigate trade-tape manipulation. Phase 3v §8 stop-trigger-domain governance is consistent with this: live runtime / paper / live MUST use `mark_price_runtime`; backtests using trade-price stops are explicitly labeled `trade_price_backtest` and cannot claim live-readiness without a `mark_price_backtest_candidate` modeling step.
- **Funding-window timing.** Binance USDⓈ-M futures have funding events at fixed UTC intervals (typically 8h). Funding-window-proximity is a derivable timing feature.
- **Cost realism.** [Phase 3l external execution-cost evidence review](docs/00-meta/implementation-reports/2026-04-29_phase-3l_external-cost-evidence-review.md) (project-internal) found "B — current cost model appears conservative but defensible." §11.6 = 8 bps HIGH per side stands; any V2 must demonstrate viability under §11.6 cost-sensitivity.

---

## 16. Prometheus prior evidence recap

Phase 4f does not modify any retained-evidence verdict. For clarity:

- **R3** remains V1 breakout baseline-of-record per Phase 2p §C.1.
- **H0** remains the V1 breakout framework anchor per Phase 2i §1.7.3.
- **R1a** and **R1b-narrow** remain retained research evidence only; non-leading.
- **R2** remains FAILED — §11.6 cost-sensitivity blocks per Phase 2w §16.1.
- **F1** remains HARD REJECT per Phase 3c §7.3 catastrophic-floor predicate; Phase 3d-B2 terminal.
- **D1-A** remains MECHANISM PASS / FRAMEWORK FAIL — other per Phase 3h §11.2; Phase 3j terminal under current locked spec.
- **Phase 3t** closed the 5m research thread.
- **Phase 4a** implemented runtime infrastructure but did not validate any strategy.
- **Phase 4e** defined reconciliation governance but did not implement reconciliation.
- **No prior verdict is revised by Phase 4f.**

V2 must be a genuinely new ex-ante hypothesis, not a re-parameterized successor of any retained-evidence candidate.

---

## 17. Lessons from V1 / R2 / F1 / D1-A / 5m diagnostics

Phase 3s diagnostics found (informative-only, descriptive findings, non-actionable per Phase 3o §6 / Phase 3p §8 / Phase 3r §8):

- **Q1** — IAE > IFE in 7 of 8 candidate × symbol cells (universal entry-path adverse bias; F1 most pronounced, ~0.5 R consumed in first 5 min).
- **Q2** — V1-family wick-dominated stop pathology vs. F1 / D1-A sustained-dominated stop pathology — the cleanest cross-family mechanism finding.
- **Q3** — +1R intrabar-touch fraction ≥ 25% in 6 of 8 cells (descriptive only).
- **Q4** — D1-A funding-decay curve has no monotone shape; SEM > displacement magnitude (non-informative).
- **Q5** — no |signed| > 8 bps cell, consistent with Phase 3l "B — conservative but defensible".
- **Q6** — D1-A mark-stop lag ~1.3–1.8 5m bars; R3 / R2 / F1 < 1 bar.
- **Q7 meta** — informative.

These findings are *descriptive only* and **MUST NOT be converted into V2 entry/exit rules** (Phase 3o §6 forbidden question forms; Phase 3p §8 critical reminders; Phase 3r §8; Phase 3t §9 / §13). V2 design relies on **external** evidence (§§7–15 above), not on these internal diagnostics.

The validity gate Phase 3t §12 codified for any future research must apply to V2:

- A genuinely new ex-ante hypothesis (not derived from observed Q1–Q7 patterns).
- Full written specification before testing.
- No conversion of Q3 / Q6 findings into post-hoc rules.
- No rescue framing.
- No reuse of 5m findings as parameter-optimization hints.
- Predeclared evidence thresholds.
- Separate operator authorization for any backtest / data-acquisition phase.

V2 below complies with all seven points.

---

## 18. Candidate strategy families considered

The memo evaluates seven candidate strategy families for V2-suitability:

| Family | Evidence basis | v1 fit | Verdict |
|---|---|---|---|
| Trend continuation / breakout (price-only) | Strong: Moskowitz/Ooi/Pedersen 2012; Hurst/Ooi/Pedersen 2017; Brock/Lakonishok/LeBaron 1992; Liu/Tsyvinski 2018/2021. | High; matches V1 framework. | **CANDIDATE.** Refine entry-trigger and exit logic vs. V1. |
| Mean reversion (intraday) | Mixed: F1 already failed framework discipline; intraday mean-reversion in crypto is documented but cost-sensitive. | Low; F1 HARD REJECT exhausts this region under current spec. | **REJECTED for V2.** |
| Volatility breakout from compression | Practitioner-strong; weak academic basis; partial fit with V1 + ATR filter. | Medium. | **CANDIDATE FEATURE**, not a standalone family. |
| Funding / basis carry | Strong: BIS WP 1087; requires spot exposure; D1-A already failed the directional / contrarian framing. | Low for v1 (no spot leg). | **REJECTED as primary** for v1; **acceptable as context / regime feature**. |
| Liquidation-cascade fading | Practitioner literature; not academically robust as standalone signal. | Low (cost / volatility regime, not a clean entry). | **REJECTED as primary**; **acceptable as risk-aware exclusion zone**. |
| Multi-timeframe momentum | Strong (TSMOM literature with HTF bias). | High; V1 already uses 1h bias on 15m signals. | **CANDIDATE FEATURE**, not a standalone family. |
| Volume-confirmed continuation | Mixed-strong: practitioner-strong; academic basis through VPIN / order-flow-imbalance. | High; not exploited by V1. | **CANDIDATE — primary feature family addition for V2.** |
| Derivatives-flow-confirmed continuation | Mixed: BIS / OI / funding-percentile evidence supports as regime / cost lens. | Medium. | **CANDIDATE FEATURE**, not a standalone family. |

**Synthesis:** the strongest single direction is *trend-continuation/breakout extended with volume/participation and derivatives-flow context*. V2 (§22) operationalizes exactly this combination.

---

## 19. Candidate feature families considered

| Feature family | v1 in use? | Public Binance availability | Evidence strength | V2 candidate? |
|---|---|---|---|---|
| Trend / momentum filter (e.g., 1h/4h return state; Donchian trend state; EMA slope/separation; HH/HL structure) | Partial (1h EMA(50) bias) | Klines bulk archive | Strong (Moskowitz et al.) | **YES** |
| Breakout / range-expansion (Donchian width %ile; ATR %ile; breakout close location; range-expansion ratio) | Partial (V1 breakout) | Klines bulk archive | Strong (Brock et al.) | **YES** |
| Volatility compression / expansion | Partial (ATR filter only) | Klines bulk archive | Medium-strong (Manamala 2025; practitioner) | **YES (compression precondition)** |
| Relative volume / volume z-score / volume %ile by UTC hour | No | Klines bulk archive | Medium (volume confirmation literature) | **YES** |
| Taker buy/sell imbalance | No | Bulk archive metrics; aggTrades | Medium-strong (VPIN / OFI literature) | **YES (confirmation)** |
| Open-interest delta | No | Bulk archive metrics | Medium (BIS / practitioner) | **YES (regime context)** |
| Funding-rate percentile | No (D1-A used directional Z-score) | Bulk archive funding history | Strong (BIS WP 1087) | **YES (regime / cost lens)** |
| Long/short ratio | No | Bulk archive metrics | Weak-medium (sentiment proxy) | **OPTIONAL** (context only) |
| UTC hour bucket / session / volume bucket | No | Derivable from klines | Strong (Hattori 2024; Eross et al. 2019) | **YES (timing / cost-aware)** |
| Mark-price vs. trade-price divergence | Diagnosed by Phase 3s Q6 only | Bulk archive markPriceKlines + klines | Project-internal (Phase 3s; Phase 3v) | **YES (governance / runtime — Phase 3v §8)** |
| Liquidity / spread proxy | No | aggTrades / orderbook (only spot bulk; perp orderbook not in public archive) | Medium (microstructure literature) | **OPTIONAL** (only if reconstructable from public sources) |
| Stop-distance / ATR risk quality | Yes (V1 spec) | Derivable from klines | Strong | **YES (risk gate)** |
| Expected-fee burden / slippage sensitivity | Implicit | Cost-model; §11.6 = 8 bps HIGH | Project-internal (Phase 3l) | **YES (cost gate)** |

---

## 20. Timeframe candidates considered

Phase 4f predeclares the V2 candidate timeframe matrix:

| Role | Candidate timeframes | Rationale |
|---|---|---|
| **Primary signal timeframe** | **15m, 30m, 1h** | Balance density vs. noise vs. cost-sensitivity. |
| **Higher-timeframe bias** | **1h, 4h** | Trend-persistence literature consistent with HTF filtering. |
| **Session / volume bucket** | **30m, 1h** | Time-of-day evidence (Hattori; Eross et al.). |
| **Daily regime** | optional broad context | Daily TSMOM literature (Moskowitz et al.); single-symbol daily N ~1500 over v002. |
| **5m** | execution / timing diagnostics ONLY | 5m is *NOT* a primary signal timeframe per Phase 3o §6 / Phase 3p §8; available only as a diagnostic per Phase 3s. |

**5m-only scalping is excluded.** The 5m thread is closed; reopening it as a strategy timeframe would require a separate, explicitly-justified phase authorization with new ex-ante framing.

---

## 21. Data-source feasibility matrix

For each predeclared V2 feature, classify availability without authenticated/private access:

| V2 feature candidate | Already in v002 | Available from Phase 3q v001-of-5m | Public Binance bulk archive | Public REST only | Authenticated/private (FORBIDDEN) | Not available |
|---|---|---|---|---|---|---|
| 1h/4h return state | YES | YES (5m only) | klines (bulk archive, 1h/4h) | klines REST | — | — |
| Donchian width / trend state (15m/1h) | YES | YES (5m) | klines | klines REST | — | — |
| EMA slope / separation (15m/1h) | YES | YES (5m) | klines | klines REST | — | — |
| HH/HL structure (15m/1h) | YES | YES (5m) | klines | klines REST | — | — |
| ATR percentile / volatility regime | YES (derivable) | YES | klines | klines REST | — | — |
| Breakout close location / range-expansion ratio | YES (derivable) | YES | klines | klines REST | — | — |
| Relative volume / volume z-score | YES (derivable) | YES | klines | klines REST | — | — |
| Volume percentile by UTC hour | YES (derivable) | YES | klines | klines REST | — | — |
| Taker buy/sell imbalance | NO (not currently fetched) | NO | aggTrades bulk archive; metrics | aggTrades REST; metrics | — | — |
| Open-interest historical | NO | NO | metrics bulk archive (`openInterestHist`) | OI history REST | — | — |
| Funding-rate history | YES (v002 funding) | NO (not 5m-relevant) | funding-rate bulk archive | funding-rate REST | — | — |
| Long/short ratio | NO | NO | metrics bulk archive | trading-data REST | — | — |
| Mark-price (15m / 5m) | YES (15m) | YES (5m, with `research_eligible: false` Q6 governance) | markPriceKlines bulk archive | markPriceKlines REST | — | — |
| UTC hour bucket | YES (derivable from open_time) | YES | (no fetch needed) | (no fetch needed) | — | — |
| Funding-window proximity | YES (derivable) | YES | (no fetch needed) | (no fetch needed) | — | — |
| Stop-distance / ATR risk quality | YES (derivable) | YES | klines | klines REST | — | — |
| Expected fee burden | YES (cost-model parameter) | YES | (no fetch needed; §11.6) | (no fetch needed) | — | — |
| Spot-vs-perp basis (informational) | NO | NO | requires spot klines — NOT currently authorized | spot REST | — | — |
| Order-book L2 depth | — | — | NOT in public bulk archive | requires WebSocket / authenticated REST — FORBIDDEN | YES | — |
| Wallet-state / balances | — | — | — | — | YES | — |
| User-stream (private) | — | — | — | — | YES | — |

**Phase 4f does NOT download data.** This matrix exists to inform the data-requirements / feasibility memo (Phase 4g Option C) the operator may authorize next.

**Two new data categories** would need to be acquired in a future authorized data-acquisition phase if V2 is to use them: (a) `metrics` bulk-archive series (open-interest history, long/short ratio, taker-buy-sell-volume); (b) `aggTrades` bulk-archive series (high-resolution taker flow, used for taker-imbalance computation). Neither is currently in v002 or v001-of-5m. Both are public unauthenticated bulk archive resources analogous to klines, so the Phase 3q acquisition pattern applies.

**No private / authenticated / WebSocket data is needed for the predeclared V2 feature set.** This is by design (Phase 4f rejects features that would require live capability).

---

## 22. V2 candidate hypothesis family

### 22.1 Name

**V2 — Participation-Confirmed Trend Continuation.**

### 22.2 Status

- Pre-research hypothesis ONLY.
- NOT implemented.
- NOT backtested.
- NOT validated.
- NOT live-ready.
- NOT a rescue of V1 / R2 / F1 / D1-A.
- NOT derived from Phase 3s Q1–Q7 findings (validity gate per Phase 3t §12).

### 22.3 Core premise

Trade trend-continuation / breakout events on BTCUSDT perpetual **only when four conditions align simultaneously**:

1. **Price structure** signals trend-continuation (Donchian breakout from recent compression with confirming HTF trend bias).
2. **Volatility regime** is in a *post-compression / expansion-friendly* state (ATR percentile within a predeclared band).
3. **Participation / volume** confirms the breakout (relative volume / volume z-score / taker-imbalance above predeclared thresholds at the breakout bar).
4. **Derivatives-flow context** is non-pathological (funding-rate percentile inside a predeclared "neither extreme-overheated nor extreme-fearful" band; OI-delta consistent with new positioning rather than late-cycle blow-off).

The premise is that breakouts confirmed by all four lenses simultaneously have meaningfully different post-trade distribution from breakouts that lack one or more confirmations — this is the *participation-confirmed* part — and that this can be measured *out-of-sample* without rescue framing because the conditions are predeclared *before* any backtest.

### 22.4 Risk and exit framing (predeclared at hypothesis level only)

- **Stop**: structural (Donchian / swing-based) plus ATR buffer; mark-price-runtime domain (Phase 3v §8.4 `mark_price_runtime`).
- **Sizing**: stop-distance × ATR with locked v1 constants (0.25% risk, 2× leverage cap, internal notional cap).
- **Exit**: Fixed-R + unconditional time-stop (R3 baseline-of-record exit family preserved as the canonical baseline; V2 may propose alternatives only with predeclared evidence thresholds).
- **Direction**: long and short symmetric (no contrarian / mean-reversion overlay; the F1 / D1-A failure modes are not re-introduced).
- **Cooldown**: predeclared post-trade cooldown to mitigate liquidation-cascade re-entry risk.

### 22.5 What V2 is NOT

- NOT a 5m strategy (5m timeframe excluded as primary).
- NOT a contrarian / mean-reversion overlay (F1 / D1-A regions are not re-explored).
- NOT a hybrid of any retained-evidence strategy (no "V1/D1 hybrid", no "F1/D1 hybrid").
- NOT a parameter-optimized version of R3 / R2 / F1 / D1-A.
- NOT an ML-first model (no neural networks, no gradient-boosted trees, no opaque feature embeddings).
- NOT a market-making / HFT / latency-dependent design.
- NOT a basis / carry / spot-perpetual-arbitrage strategy.
- NOT a paper/shadow / live-readiness evidence claim.

---

## 23. V2 predeclared feature candidates

Bounded list (no unbounded feature search). Each feature is a *candidate*; a future V2 strategy-spec memo (Phase 4g Option B) would bind specific operationalizations.

**Price / trend (always-on):**

- 1h or 4h return state (sign + magnitude bucket).
- Donchian trend state (price-vs-Donchian-channel position over predeclared lookback).
- EMA slope or EMA separation (e.g., EMA(20) vs. EMA(50) on the bias timeframe; discrete-comparison method per Phase 3w §7.3 unless the spec explicitly justifies fitted-slope).
- Higher-high / higher-low structure (binary or multi-state).

**Breakout / compression (entry-trigger):**

- Donchian width percentile (compression precondition).
- ATR percentile (volatility regime; predeclared band).
- Breakout close location (close vs. breakout level — quartile within breakout bar).
- Range-expansion ratio (current bar range / mean range over predeclared lookback).

**Volume / participation (entry confirmation):**

- Relative volume (current bar volume / mean volume over predeclared lookback).
- Volume z-score (current bar volume z-scored over predeclared lookback).
- Volume percentile by UTC hour (controls for intraday seasonality).
- Breakout-bar volume expansion (breakout bar volume / pre-breakout mean volume).

**Derivatives flow (regime / cost / context):**

- Open-interest delta (OI change over predeclared lookback).
- Taker buy/sell imbalance (taker-buy / total-taker over predeclared lookback).
- Funding-rate percentile (funding history percentile over predeclared lookback; *not* directional Z-score — D1-A's framing is not replicated).
- Long/short ratio (account ratio + top-trader ratio if both available).
- Mark-price vs. trade-price divergence (per Phase 3v §8 governance — runtime path uses `mark_price_runtime`).

**Timing (cost-aware):**

- UTC hour bucket.
- High-volume session bucket (intraday-seasonality regime).
- Funding-window proximity (minutes since / until next 8h funding event).

**Risk quality (always-on):**

- Stop distance / ATR (must satisfy 0.60 × ATR ≤ stop_distance ≤ 1.80 × ATR per existing V1 spec).
- Expected fee burden (estimated round-trip cost in bps; must satisfy §11.6 cost-sensitivity gate at HIGH-slip cell).
- Slippage sensitivity (predeclared tolerance band).

**Bound:** the V2 strategy-spec memo (if authorized) MUST select a maximum of **8 active features** for the entry rule and **3 active features** for the exit / regime gate, predeclared before any backtest. This bounded count is itself a hyperparameter — not an arbitrary cap, but a discipline against over-fitting per Bailey et al. ([2014](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253)).

---

## 24. V2 predeclared timeframe candidates

Per §20:

- **Signal timeframe**: 15m, 30m, or 1h.
- **Higher-timeframe bias**: 1h or 4h.
- **Session / volume bucket**: 30m or 1h.
- **Daily regime**: optional, broad context only.
- **5m**: timing diagnostics ONLY; NOT a primary signal timeframe; NOT a hybrid signal layer.

The V2 strategy-spec memo (if authorized) MUST pick exactly one signal timeframe and one bias timeframe before any backtest, with the choice justified by external evidence (not by internal Phase 3s findings).

---

## 25. V2 predeclared exclusion rules

The V2 strategy-spec / backtest phases (if ever authorized) MUST honor the following exclusions:

1. **No 5m-only scalping** as primary V2 signal.
2. **No private / authenticated data** (no user-stream; no listenKey; no wallet-state; no account-balance; no order-book L2 depth from authenticated WebSocket).
3. **No HFT / market making** infrastructure or strategy.
4. **No post-hoc rescue** of any retained-evidence candidate. V2 candidates that converge to R3 / R2 / F1 / D1-A parameter regions MUST be treated as separate, restricted-scope investigations and predeclared as such.
5. **No new thresholds chosen after looking at outcomes.** All thresholds predeclared before any backtest; once predeclared, only re-bounded by an explicitly authorized re-predeclaration memo.
6. **No more than the bounded set of feature families** in §23 (eight active entry features; three active exit/regime features).
7. **No unbounded parameter search.** Grid-search over each predeclared threshold MUST be predeclared with an explicit search-space size; combinatorial Sharpe / deflated Sharpe correction (Bailey & López de Prado 2014) MUST be reported.
8. **No strategy promotion without chronological validation and cost sensitivity.** Phase 2f Gate 1 / §11.3 / §11.6 framework discipline applies to V2 unchanged.
9. **No live or paper implications.** V2 is research only; any paper/shadow / live-readiness flow is forbidden by Phase 7+ gating.

---

## 26. V2 validation requirements

Any future V2 backtest phase (if ever authorized) MUST satisfy:

- **Predeclaration evidence**: the V2 strategy-spec memo (Phase 4g Option B) commits the bounded feature list, timeframe choice, and threshold grid BEFORE any backtest is run.
- **No look-ahead**: no test-set information used in feature/parameter choice.
- **Chronological holdout**: train / validation / test split uses chronological boundaries; no random shuffling of bars.
- **Cost-sensitivity gate**: V2 MUST pass §11.6 cost-sensitivity at HIGH (8 bps per side) on both BTCUSDT and ETHUSDT (research-eligible only).
- **Catastrophic-floor predicate**: applies (Phase 3c §7.3 still binds).
- **Multi-symbol**: BTCUSDT primary; ETHUSDT comparison-only confirmation. Cross-symbol consistency required.
- **Multi-window**: full v002 trade range with at least two non-overlapping out-of-sample windows.
- **Deflated Sharpe**: per Bailey & López de Prado 2014, when grid search is involved.
- **Mechanism check**: an M1 / M2 / M3 -style decomposition must be predeclared (analogous to Phase 2 / Phase 3 framework).
- **Stop-trigger domain**: backtest MUST be explicitly labeled `trade_price_backtest` (V2's primary backtest is comparable to retained-evidence) AND a `mark_price_backtest_candidate` modeling pass MUST be predeclared as the live-readiness validation step (per Phase 3v §8.5).
- **Governance labels**: `break_even_rule`, `ema_slope_method`, `stagnation_window_role` must be declared per-V2-variant per Phase 3w §6.3 / §7.3 / §8.3.

---

## 27. Cost and slippage realism

§11.6 sets the cost-sensitivity gate at 8 bps HIGH per side. Phase 3l found "B — current cost model appears conservative but defensible." Phase 3s Q5 confirmed at 5m granularity that no cell exceeded |signed| > 8 bps mean slippage on retained-evidence trade populations.

Implications for V2:

- A V2 candidate that is profitable only at LOW cost (e.g., 1–2 bps) but fails at HIGH cost (8 bps) MUST fail the §11.6 gate (per R2's failure pattern).
- A V2 candidate's expected round-trip cost depends on signal timeframe (higher-frequency signals concentrate more turnover → higher aggregate cost) and on participation conditions (low-volume hours have wider spreads in practice).
- V2's UTC-hour-bucket / session feature is partly a *cost-aware* feature: avoiding low-volume hours reduces realized slippage independently of any signal effect.

---

## 28. Overfitting and validation risks

The dominant risk for any V2 candidate is overfitting (Bailey, Borwein, López de Prado, Zhu 2014). Mitigations:

- **Predeclaration**: the V2 strategy-spec memo (Phase 4g Option B) commits the design BEFORE any backtest (this memo contributes to that predeclaration).
- **Bounded search space**: §23 bounded feature count; §25 bounded exclusions; predeclared threshold grid.
- **Combinatorial Sharpe correction / deflated Sharpe**: required at the V2 backtest phase.
- **Multi-symbol cross-check**: BTCUSDT primary, ETHUSDT comparison.
- **Chronological holdout**: at least two non-overlapping out-of-sample windows.
- **No conversion of Phase 3s findings into rules**: Phase 3o §6 forbidden question forms apply.
- **No rescue framing**: V2 is a new ex-ante hypothesis, not a re-parameterized successor.

Combinatorially symmetric cross-validation (CSCV) and the probability of backtest overfitting (PBO) per Bailey et al. ([SSRN 2326253](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253)) provide the canonical statistical machinery; the V2 backtest phase MUST adopt them.

---

## 29. Rejected strategy directions

Phase 4f explicitly rejects or de-prioritizes:

- **Direct HFT market making.** Forbidden by infrastructure and project safety rules.
- **Latency-dependent strategies.** Out of scope for a NUC-deployed supervised v1.
- **ML-first black-box forecasting.** Excluded per `current-project-state.md` (ML feasibility "not authorized; not proposed").
- **Unsupported influencer / paid-course / "high win rate" claims.** Excluded by source-quality policy (§6).
- **Post-hoc rescue of V1 / R2 / F1 / D1-A.** Excluded per Phase 3o §6 / Phase 3p §8 / Phase 3r §8 / Phase 3t §13 / Phase 3u §10 / Phase 3v §13 / Phase 3w §14 / Phase 3x §6.7 / Phase 4a §22.
- **5m-only scalping without flow confirmation.** 5m thread closed (Phase 3t); reopening as a strategy timeframe requires a separate explicitly-justified phase.
- **Strategies requiring private / authenticated data.** Forbidden by safety/secrets rules.
- **Paper / shadow / live-readiness.** Forbidden by phase-gate model.
- **Mean-reversion as standalone family.** F1's HARD REJECT exhausts that region under current spec.
- **Funding/basis/carry as standalone family for v1.** Requires spot leg; v1 is perp only.
- **Liquidation-cascade fading as standalone signal.** Cost / volatility regime, not a clean entry; literature does not support it as a free-edge.
- **Multi-symbol / portfolio routing.** v1 is BTCUSDT only.
- **Hedge mode.** Forbidden by §1.7.3.

---

## 30. Recommended next research phase

Phase 4f recommends:

- **Primary: Option B — docs-only V2 strategy-spec memo for "Participation-Confirmed Trend Continuation".** A Phase-4g-style docs-only memo that operationalizes the §22 hypothesis: chooses one signal timeframe; chooses one bias timeframe; selects the bounded set of active features (≤8 entry, ≤3 exit/regime); specifies predeclared threshold grids; specifies the M1 / M2 / M3 -style mechanism-check decomposition; specifies validation requirements; explicitly declares all four governance labels (`stop_trigger_domain`, `break_even_rule`, `ema_slope_method`, `stagnation_window_role`) per Phase 3v + Phase 3w. The strategy spec would NOT authorize backtest or implementation; that is a separate operator decision after the spec is reviewed.
- **Secondary: Option C — docs-only V2 data-requirements and feasibility memo.** A complementary docs-only memo that operationalizes §21: enumerates exact bulk-archive datasets needed (`metrics` history; `aggTrades` history; whatever else the V2 spec declares); specifies SHA256-verified acquisition plan analogous to Phase 3q; specifies dataset-versioning convention (likely `binance_usdm_btcusdt_metrics__v001`, `binance_usdm_btcusdt_aggtrades__v001`); specifies integrity-check rules; predeclares `research_eligible` semantics. The data-requirements memo would NOT authorize acquisition; that is a separate operator decision.

**Both are docs-only.** The natural ordering depends on operator preference: Option B → C means "design first, then check feasibility"; Option C → B means "verify data availability first, then design against what exists." Either order is acceptable.

**Phase 4f does NOT recommend:**

- **Option A — Remain paused.** Procedurally acceptable but understates the operator-stated motivation (return to strategy research because absence of strategy is the main blocker).
- **Option D — Acquire data immediately.** Forbidden until a docs-only data-requirements memo predeclares what is needed and why.
- **Option E — Run exploratory backtests immediately.** Rejected. Backtesting before predeclaration is the data-snooping pattern Bailey et al. document as the leading cause of out-of-sample failure. Any backtest MUST be predeclared by an explicit strategy-spec memo.
- **Option F — Paper / shadow / live-readiness / exchange-write.** Forbidden by phase-gate model.

---

## 31. What this does not authorize

Phase 4f explicitly does NOT authorize, propose, or initiate any of the following:

- **V2 strategy-spec memo.** Recommended (Option B primary) but a separate operator decision.
- **V2 data-requirements memo.** Recommended (Option C secondary) but a separate operator decision.
- **V2 backtest.** Forbidden until V2 strategy-spec is predeclared and the backtest phase is separately authorized.
- **V2 implementation.** Forbidden until V2 backtest evidence is in.
- **Phase 4 (canonical) authorization.** Per `docs/12-roadmap/phase-gates.md`.
- **Phase 4g or any successor phase.** Phase 4f is a docs-only research memo; the operator must explicitly authorize any successor.
- **Live exchange-write capability.** Architectural prohibition unchanged.
- **Production Binance keys, authenticated APIs, private endpoints, user stream, WebSocket, listenKey lifecycle, production alerting, Telegram / n8n production routes, MCP, Graphify, `.mcp.json`, credentials, exchange-write capability.** None of these is touched, enabled, or implied.
- **Strategy implementation / rescue / new candidate (other than the bounded V2 hypothesis predeclared in this memo).** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved verbatim. V2 is a new ex-ante hypothesis, NOT a rescue.
- **Verdict revision.**
- **Lock change.**
- **Data acquisition / patching / regeneration / modification.** `data/` artefacts preserved verbatim.
- **Diagnostics / Q1–Q7 rerun / backtests.** None run.
- **Phase 3v stop-trigger-domain governance modification.** Preserved verbatim.
- **Phase 3w break-even / EMA slope / stagnation governance modification.** Preserved verbatim.
- **Reconciliation implementation.** Phase 4e reconciliation-model design preserved verbatim, not implemented.
- **Paper/shadow / live-readiness / deployment.** Not authorized.

---

## 32. Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4g / successor phase started.** No subsequent phase has been authorized, scoped, briefed, branched, or commenced.
- **No V2 implementation.**
- **No V2 backtest.**
- **No V2 strategy-spec memo (this memo is a hypothesis-candidate memo, not a strategy spec).**
- **No data acquired.** No `data/` artefact modified. No public Binance endpoint consulted in code.
- **No implementation code written.** Phase 4f is text-only.
- **No real exchange adapter implemented.**
- **No exchange-write capability.**
- **No order placement / cancellation.**
- **No Binance credentials used.** No request, no storage, no `.env` modification.
- **No authenticated REST / private endpoint / public endpoint / user-stream / WebSocket calls.** Phase 4f performs no network I/O via code; all web research used WebSearch tool only, against public web pages.
- **No production alerting / Telegram / n8n production routes.**
- **No MCP enabling / Graphify enabling / `.mcp.json` modification.**
- **No `.env` file creation.**
- **No credential handling modification.**
- **No deployment artefact created.**
- **No paper/shadow runtime created.**
- **No live-readiness implication.**
- **No V1 / R3 / R2 / F1 / D1-A / other strategy implementation.** Existing `prometheus.strategy` modules untouched.
- **No strategy rescue proposal.** V2 is a new ex-ante hypothesis, NOT a re-parameterized successor of any retained-evidence candidate.
- **No 5m strategy / hybrid / retained-evidence successor / new variant created.**
- **No diagnostics run.** No Phase 3o / 3p Q1–Q7 question rerun.
- **No backtests run.**
- **`scripts/phase3q_5m_acquisition.py` not run.**
- **`scripts/phase3s_5m_diagnostics.py` not run.**
- **No data acquisition / download / patch / regeneration / modification.** No `data/` artefact modified.
- **No data manifest modification.** All `data/manifests/*.manifest.json` preserved verbatim.
- **No v002 dataset / manifest modification.**
- **No Phase 3q v001-of-5m manifest modification.**
- **No v003 created.**
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved verbatim.
- **No threshold / parameter / project-lock modifications.**
- **No Phase 3v stop-trigger-domain governance modification.**
- **No Phase 3w break-even / EMA slope / stagnation governance modification.**
- **No `docs/03-strategy-research/v1-breakout-strategy-spec.md` substantive change.**
- **No `docs/03-strategy-research/v1-breakout-backtest-plan.md` substantive change.**
- **No `docs/05-backtesting-validation/v1-breakout-validation-checklist.md` substantive change.**
- **No `docs/07-risk/stop-loss-policy.md` substantive change.**
- **No `docs/06-execution-exchange/binance-usdm-order-model.md` substantive change.**
- **No `docs/12-roadmap/phase-gates.md` substantive change.**
- **No `docs/12-roadmap/technical-debt-register.md` substantive change.**
- **No `docs/00-meta/ai-coding-handoff.md` substantive change.**
- **No `docs/09-operations/first-run-setup-checklist.md` substantive change.**
- **No `docs/00-meta/implementation-ambiguity-log.md` modification.**
- **No `docs/00-meta/current-project-state.md` modification on the Phase 4f branch.** Per the Phase 4f brief.
- **No `.claude/rules/**` modification.**
- **No `pyproject.toml` modification.**
- **No `.gitignore` modification.**
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No `src/prometheus/**` modification.**
- **No `tests/**` modification.**
- **No `scripts/**` modification.**
- **No merge to main.**
- **No successor phase started.**

---

## 33. Remaining boundary

- **Recommended state:** **paused** for any successor phase. Phase 4f deliverables exist as branch-only artefacts pending operator review.
- **Phase 4f output:** docs-only research memo + closeout artefact on the Phase 4f branch.
- **Repository quality gate state:** **fully clean.** Whole-repo `ruff check .` passes; pytest 785 passed; mypy strict 0 issues across 82 source files (verified during Phase 4f startup).
- **5m research thread state:** Operationally complete and closed (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4 (canonical) remains not authorized. Phase 4a executed and merged. Phase 4b/4c quality cleanups merged. Phase 4d review merged. Phase 4e reconciliation-model design memo merged. Phase 4f research memo on this branch.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 + enforced in code by Phase 4a (preserved by 4b / 4c / 4d / 4e / 4f).
- **Break-even rule governance:** RESOLVED by Phase 3w §6 + enforced in code by Phase 4a (preserved).
- **EMA slope method governance:** RESOLVED by Phase 3w §7 + enforced in code by Phase 4a (preserved).
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 + enforced in code by Phase 4a (preserved).
- **Reconciliation governance:** Defined by Phase 4e but NOT yet enforced in code; awaits separately authorized future implementation phase.
- **V2 strategy-research direction:** Predeclared by Phase 4f as **"Participation-Confirmed Trend Continuation"**; bounded feature list, bounded timeframe matrix, predeclared exclusion rules, predeclared validation requirements. NOT implemented; NOT backtested; NOT validated.
- **OPEN ambiguity-log items after Phase 4f:** zero relevant to runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`. All preserved.
- **Branch state:** `phase-4f/external-strategy-research-landscape-v2-candidates` exists locally and (after push) on `origin/phase-4f/external-strategy-research-landscape-v2-candidates`. NOT merged to main.

---

## 34. Next authorization status

**No next phase has been authorized.** Phase 4f's recommendation is **Option B (docs-only V2 strategy-spec memo for Participation-Confirmed Trend Continuation) as primary**, with **Option C (docs-only V2 data-requirements and feasibility memo) as conditional secondary**. Option A (remain paused) is procedurally acceptable but understates the operator-stated motivation. Options D / E are not recommended (data acquisition before requirements memo; backtest before strategy spec). Option F (paper/shadow / live-readiness / exchange-write) is forbidden / not recommended.

Selection of any subsequent phase requires explicit operator authorization for that specific phase. No such authorization has been issued.

The 5m research thread remains operationally complete and closed (per Phase 3t). The implementation-readiness boundary remains reviewed (per Phase 3u). All four Phase 3u §8.5 pre-coding governance blockers remain RESOLVED at the governance level (per Phase 3v + Phase 3w). The Phase 4a safe-slice scope is implemented (per Phase 4a). The Phase 4b script-scope quality-gate restoration is complete (per Phase 4b). The Phase 4c state-package quality-gate residual cleanup is complete (per Phase 4c). The Phase 4d post-4a/4b/4c review is complete (per Phase 4d). The Phase 4e reconciliation-model design memo is complete (per Phase 4e). The Phase 4f external research memo and V2 hypothesis-candidate predeclaration are complete on the Phase 4f branch (this phase). **Recommended state remains paused.**
