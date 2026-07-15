# Phase 4bn-AW — Bounded Fable Independent-Review Brief

> The text between the horizontal rules below is the copy-paste-ready Fable prompt.
> The operator pastes it into a completely fresh Fable chat. Nothing else is sent.

---

Do not inspect the repository, linked files, attachments, or external documents. Use only the bounded summary below.

You are an independent reviewer. A paused quantitative crypto-trading research project (BTCUSDT perpetual futures) is deciding whether to reopen strategy research. Two research arcs are already stopped and must not be reopened or rescued:

- STOP_LONGHORIZON_ML_ARC: a machine-learning arc on trade-tape ("aggTrades") features found clean short-horizon (15s) directional information, but it was economically thin (only ~2.5% of 15s moves clear the round-trip cost) and it inverted at longer horizons (5m/30m/1h under-performed a naive majority baseline). Stopped on evidence.
- STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE: a model-free question about whether that 15s signal was real midpoint movement or bid-ask bounce could not be answered, because the historical top-of-book quote data is inadmissible (undocumented, out-of-order, coverage unconfirmed) and prospective capture cannot align to the 2024 trades. Stopped on data.

Evidence-budget status (do not propose spending any of it):
- A small internal holdout is CONSUMED and can never again serve as independent confirmation.
- A "terminal window" reserve and a "sealed test" reserve remain UNTOUCHED and scarce; they are one-shot and are protected for a possible future confirmation stage only.
- No reserve spend is proposed. Every candidate below must be developable using already-built, non-reserve data only.

Locked cost assumption: 8 bps per side / 16 bps round trip. The project trades directionally.

Purpose of the screening: decide whether the committed record supports one or more genuinely new, scientifically defensible strategy-research hypothesis families — distinct from the stopped arcs and from a set of already-rejected families (price-only continuation; cross-sectional relative-strength ranking; funding-as-directional-trigger) — that could justify a *later* preregistration phase. This is screening only; nothing is authorized.

Data facts you may rely on: BTCUSDT trade-tape data is built and available (non-reserve). Multi-symbol candlestick (OHLCV) and funding-rate history are on disk. Multi-symbol trade-tape, order-book/depth, top-of-book quotes, and open-interest history are NOT available without a separate acquisition/capture step (and some cannot answer a historical question at all).

Three shortlisted candidate families (the only ones that survived screening):

CF-1 — Microstructure realized-volatility (magnitude) forecasting.
- Mechanism: volatility clustering / long-memory in realized variance (a robust, externally-documented stylized fact); trade-flow intensity and trade-size dispersion may add information about near-future realized variance beyond past variance.
- Required data: BTCUSDT trade-tape — available now, no reserve.
- Falsification: no out-of-sample skill over a HAR-RV / variance-persistence baseline (predeclared loss, consistent across time blocks) ⇒ stop.
- Strongest strength: fully developable now on built data; strongest mechanism; cleanest kill; a null materially narrows the search; preserves both reserves.
- Strongest weakness: it is non-directional, so even a clean success does not by itself produce a directional edge or clear the 16 bps round-trip frame — decision consequence is indirect.

CF-2 — Cross-symbol return lead-lag / information transmission.
- Mechanism: price discovery concentrates in the most liquid asset (BTC) and diffuses to less-liquid correlated alts with a measurable latency (temporal lead-lag), distinct from cross-sectional ranking.
- Required data: multi-symbol returns at a tradeable granularity. The admissible form (coarse candlesticks) is likely already arbitraged; the tradeable form needs multi-symbol trade-tape that is NOT acquired — so this candidate is BLOCKED on data now.
- Falsification: cross-symbol predictive information ≤ a contemporaneous-only baseline, or no consistent lead direction ⇒ stop.
- Strongest strength: the only survivor with a genuinely directional, tradeable decision consequence.
- Strongest weakness: blocked on data (needs a separate acquisition phase); high multiple-testing surface (pairs × lags × horizons).

CF-3 — Derivatives-context + settlement/session-timing volatility-regime conditioning.
- Mechanism: crowded positioning (funding extremes) and deterministic settlement/session timing precede predictable shifts in the volatility/liquidity regime (not direction); used only as a context/regime lens, never a directional trigger.
- Required data: funding history (on disk, context-only) + a fixed UTC calendar (no data) + trade-tape/candles for the volatility target. Open-interest component is blocked.
- Falsification: no volatility/activity differential between predeclared funding-extreme / calendar windows and matched controls ⇒ stop.
- Strongest strength: fully developable now; the calendar is fixed ex-ante (low researcher freedom).
- Strongest weakness: weakest decision consequence (a context layer with no standalone edge); target overlaps CF-1.

Provisional project ranking: CF-1 first (developable now, strongest mechanism/kill, reserve-preserving, but indirect consequence); CF-2 second (strongest consequence but blocked on data, so barred from first); CF-3 third (developable but weakest consequence, overlaps CF-1). The strongest objection the project itself raises: repeated negatives suggest the substrate may lack an exploitable directional edge, so all three risk being novelty-by-target-swap, and none is a demonstrated tradeable edge — "remain paused" is a live competing option.

Central decision criteria: genuine novelty vs stopped/rejected work; mechanism credibility; admissible development evidence with no reserve spend; reserve preservation; bounded falsifiability; meaningful negative-result value; low rescue / multiple-testing risk; and a clear future decision consequence.

Please provide only:
1. A ranking of the three shortlisted candidates.
2. One recommended candidate, or a recommendation to select none.
3. The strongest objection to your own recommendation.
4. One clean kill criterion for the recommended candidate.
5. The evidence or reasoning that would most likely change your ranking.
6. At most one omitted candidate family — only if it is genuinely distinct from every shortlisted and stopped family.

Keep the full response under approximately 1,200 words.

---
