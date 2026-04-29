# Phase 3l — External Execution-Cost Evidence Review (docs-only)

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (no post-hoc loosening per §11.3.5); Phase 2i §1.7.3 project-level locks; Phase 2p §C.1 (R3 baseline-of-record); **Phase 2y slippage / cost-policy review (§11.6 = 8 bps HIGH preserved verbatim; framework-discipline anchor)**; Phase 2w R2 framework-FAILED — §11.6 cost-sensitivity blocks; Phase 3d-B2 F1 HARD REJECT; Phase 3j D1-A MECHANISM PASS / FRAMEWORK FAIL — other; Phase 3k post-D1-A research consolidation memo (remain-paused primary recommendation; external-cost-evidence review as conditional secondary alternative); `src/prometheus/research/backtest/config.py:62-91` (`SlippageBucket` enum + `DEFAULT_SLIPPAGE_BPS`); `src/prometheus/research/backtest/config.py:118-123` (`taker_fee_rate` + `slippage_bps_map`); `docs/05-backtesting-validation/cost-modeling.md`; `docs/05-backtesting-validation/backtesting-principles.md`; `.claude/rules/prometheus-core.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/implementation-ambiguity-log.md`.

**Phase:** 3l — Docs-only **external execution-cost evidence review.** Collects and evaluates public, non-authenticated execution-cost evidence relevant to Binance USDⓈ-M BTCUSDT and ETHUSDT research assumptions, and assesses whether the current Prometheus cost model and §11.6 = 8 bps HIGH per side remain reasonable, conservative, uncertain, or in need of future independent review.

**Branch:** `phase-3l/external-cost-evidence-review`. **Memo date:** 2026-04-29 UTC.

**Status:** Recommendation drafted. **No code change. No backtest. No variant created. No parameter tuned. No threshold changed. No project-level lock changed. No prior verdict revised.** R3 remains baseline-of-record. H0 remains framework anchor. R1a / R1b-narrow / R2 / F1 / D1-A remain retained research evidence. R2 remains FAILED. F1 remains HARD REJECT. D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write proposal. Recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

## 1. Plain-English explanation of what Phase 3l is deciding

Phase 3l is the docs-only secondary acceptable alternative authorized by Phase 3k (per Phase 3k §10 + §12). Phase 3k's primary recommendation was **remain paused**; the operator selected the secondary acceptable active path: external execution-cost evidence review (docs-only). Phase 3l's role is to:

- Restate the canonical Prometheus cost model from `src/prometheus/research/backtest/config.py` exactly, so any external evidence is compared against the precise values committed in code.
- Collect public, non-authenticated, official-Binance-where-possible evidence about: (a) USDⓈ-M Futures maker/taker fee rates, (b) symbol metadata (tick / lot / min-notional / price-protection / order-type filters) from publicly-available trading-rules pages or the public exchangeInfo REST endpoint documentation, (c) any qualitative spread / depth / mark-vs-trade / funding evidence accessible without credentials, and (d) any officially-published cost-component fees (commissions, funding, insurance / liquidation).
- Assess each cost-model component against the gathered evidence: reasonable, conservative-but-defensible, too-optimistic, evidence-insufficient, or future-revision-warranted. Pick exactly one primary assessment.
- Make a single §11.6 policy recommendation chosen from {keep unchanged; keep unchanged pending stronger evidence; recommend a future docs-only cost-model revision phase}. **Phase 3l does NOT change §11.6.**
- State explicitly that Phase 3l does NOT revise prior verdicts (R2 / F1 / D1-A / R3 / H0 / R1a / R1b-narrow). No backtest is rerun. No candidate is rescued.
- Discuss the symmetric-outcome / anti-circular-reasoning discipline that any future cost-model revision must respect (per Phase 2y framework-discipline anchor preserved at Phase 2y closeout).
- Recommend exactly one next operator decision from a constrained list (remain paused; formal cost-model revision memo docs-only; regime-first framework memo docs-only; 5m timeframe feasibility memo docs-only; new strategy-family discovery [forbidden by Phase 3k §8.4]; ML feasibility memo [forbidden by Phase 3k §8.5]; paper/shadow or Phase 4 [forbidden by every brief since Phase 0]).

What Phase 3l is NOT deciding:

- Not deciding whether to deploy R3 / R3-prime / any candidate or to begin paper/shadow (forbidden).
- Not deciding whether to begin Phase 4 (forbidden).
- Not deciding whether to lift any §1.7.3 project-level lock.
- Not deciding whether to revise any Phase 2f threshold (Phase 2y framework-discipline anchor + Phase 3l brief explicitly forbid threshold changes in this phase).
- Not authorizing any next execution phase, any next implementation phase, any backtest, or any code change.
- Not commencing D1-A-prime / D1-B / V1/D1 hybrid / F1/D1 hybrid / regime-first / ML / new-family-discovery work.
- Not retroactively rescuing R2, F1, or D1-A.

The output is a consolidated record of external evidence available + assessment + a single forward-looking operator decision recommendation. Phase 3l produces a memo; the operator decides whether to authorize anything downstream.

---

## 2. Current project-state restatement

| Item | State |
|------|-------|
| **R3 (Phase 2j memo §D — Fixed-R + 8-bar time-stop, no trailing)** | **V1 breakout baseline-of-record** per Phase 2p §C.1; locked sub-parameters preserved. |
| **H0 (Phase 2e locked baseline)** | **V1 breakout framework anchor** per Phase 2i §1.7.3. |
| **R1a / R1b-narrow** | Retained research evidence only; non-leading. |
| **R2 (Phase 2u — pullback-retest entry topology on top of R3)** | Retained research evidence only; **framework FAILED — §11.6 cost-sensitivity blocks** (BTC HIGH-slip Δexp_H0 −0.014; ETH HIGH-slip Δexp_H0 −0.230). |
| **F1 (Phase 3b §4 — mean-reversion-after-overextension)** | Retained research evidence only; **framework verdict: HARD REJECT** per Phase 3c §7.3 catastrophic-floor predicate; Phase 3d-B2 terminal for F1. |
| **D1-A (Phase 3g §6 — funding-aware directional / carry-aware contrarian)** | Retained research evidence only; **framework verdict: MECHANISM PASS / FRAMEWORK FAIL — other** per Phase 3h §11.2; Phase 3j terminal for D1-A under current locked spec. |
| **Phase 3k consolidation** | Drafted (docs-only); primary recommendation: **remain paused**. Secondary acceptable docs-only alternative: external execution-cost evidence review (Phase 3l, this memo). Tertiary acceptable docs-only alternative: regime-first research framework memo. |
| **§1.7.3 project-level locks** | Preserved verbatim. |
| **Phase 2f thresholds (incl. §11.6 = 8 bps HIGH per side)** | Preserved verbatim. |
| **Paper/shadow planning** | Not authorized. |
| **Phase 4 work** | Not authorized. |
| **Live-readiness / deployment / production-key / exchange-write work** | Not authorized. |
| **MCP / Graphify / `.mcp.json` / credentials** | Not activated; not requested; not used. |

The next operator decision is operator-driven only. Phase 3l does not pre-empt that decision; this section records the state on which any future decision must build.

---

## 3. Current Prometheus cost assumptions (canonical from code)

The canonical source is `src/prometheus/research/backtest/config.py`. The cost-model has four explicit components (slippage; taker fee; funding; mark-vs-trade-price stop-trigger sensitivity) and the implicit assumption of next-bar-open market fill.

### 3.1 Taker fee assumption (`config.py:119`)

```python
taker_fee_rate: float = Field(gt=0, lt=1)  # A5 primary: 0.0005
```

Committed default: **`taker_fee_rate = 0.0005` (5 bps per side; 10 bps round-trip).**

Applied at entry and at exit, computed as `notional_at_fill × taker_fee_rate`. This is the standard "regular tier without VIP volume discount and without BNB-token-fee discount" Binance taker rate for USDⓈ-M Futures. Maker rate is not used by the strategy spec — H0 / R3 / R1a / R1b-narrow / R2-committed-path / F1 / D1-A all use market entries; protective stops are STOP_MARKET (which fill at taker rate when triggered).

### 3.2 Slippage tiers (`config.py:84-91`)

```python
DEFAULT_SLIPPAGE_BPS: dict[SlippageBucket, float] = {
    SlippageBucket.LOW: 1.0,        # 0.01% per side
    SlippageBucket.MEDIUM: 3.0,     # 0.03% per side  (committed default)
    SlippageBucket.HIGH: 8.0,       # 0.08% per side  (§11.6 stress-test)
}
```

Round-trip slippage = 2 × per-side (entry + exit, both adverse direction).

| Tier | Per-side bps | Round-trip bps |
|------|-------------:|---------------:|
| LOW | 1.0 | 2.0 |
| MEDIUM (committed) | 3.0 | 6.0 |
| HIGH | 8.0 | 16.0 |

Applied per side at fill: `effective_entry_price = fill_price × (1 + slippage_bps × sign / 10_000)` with `sign = +1 for long, −1 for short` (adverse direction). Mirror-image at exit.

### 3.3 Round-trip transaction-cost stack

| Tier | Slippage round-trip | Taker fees round-trip | Total bps |
|------|--------------------:|----------------------:|----------:|
| LOW | 2 bps | 10 bps | **12 bps** |
| MEDIUM (committed) | 6 bps | 10 bps | **16 bps** |
| HIGH | 16 bps | 10 bps | **26 bps** |

### 3.4 §11.6 cost-sensitivity gate

§11.6 evaluates §10.3 disqualification at HIGH = 8 bps per side. The threshold is preserved verbatim from Phase 2y closeout; **Phase 3l does NOT change §11.6.**

### 3.5 Funding-cost modeling

Per `engine.py` and Phase 2y §2.5: **funding is applied via historical funding-rate joins from the v002 funding-rate dataset**, integrated over each trade's hold period. Mark-price values used where required. Pre-2024 funding events handled with `mark_price=None` per the Phase 2e baseline summary. Funding contributes to net PnL; the trade-log emits a per-trade `funding_pnl` field consumed by reporting. Phase 3j D1-A funding-cost benefit (M2) computed as `funding_pnl / realized_risk_usdt` per trade.

### 3.6 Mark-price vs trade-price stop-trigger (`config.py:70-81`)

```python
class StopTriggerSource(StrEnum):
    MARK_PRICE = "MARK_PRICE"   # default; mirrors live workingType=MARK_PRICE
    TRADE_PRICE = "TRADE_PRICE" # research-only sensitivity diagnostic (Phase 2g GAP-20260424-032)
```

Default: MARK_PRICE (matches the v1 protective-stop spec `workingType=MARK_PRICE`). Phase 2y §2.4 reported MARK and TRADE_PRICE produce bit-identical V1-family results because zero stops gap through on the v002 datasets. Phase 3j §8.6 reported D1-A MED MARK vs MED TRADE_PRICE produces a small but non-zero difference (BTC ΔexpR = −0.05 R; ETH ΔexpR = −0.08 R) because D1-A's intrabar wick exposure is materially larger than V1's. Mark-vs-trade is not a unique D1-A failure source but is a measurable diagnostic axis.

### 3.7 Implicit assumption: next-bar-open market fill

Entries fire on completed-15m-bar close; market order is conceptually submitted at bar close; fill is realized at next-15m-bar open price (with slippage applied). This is the next-bar-open assumption shared by H0 / R3 / R1a / R1b-narrow / R2-committed-path / F1 / D1-A. No explicit latency component is modeled; the next-bar-open assumption implicitly bounds latency at <15 minutes (which is loose for any real low-latency setup).

---

## 4. External official fee evidence

### 4.1 Sources accessed

All fetched 2026-04-29 UTC. URLs as listed in the Phase 3l brief.

- `https://www.binance.com/en/fee/futureFee` — accessed 2026-04-29. **Result:** the page returns "No records found" for unauthenticated visitors. The actual VIP-conditional fee table is gated behind login. The page does not display VIP 0 standard rates publicly.
- `https://www.binance.com/en/support/faq/detail/98488a516eb84e3eb34605683dffd554` ("Binance Futures Fees Explained") — accessed 2026-04-29. **Result:** explains how fees are calculated, references VIP tiers + maker/taker distinction + BNB-discount, but does not list VIP 0 rates verbatim.
- `https://www.binance.com/en/support/faq/binance-futures-fee-structure-fee-calculations-360033544231` ("Binance Futures Fee Structure & Fee Calculations") — accessed 2026-04-29. **Result:** displays an illustrative example: "regular maker commission: 0.02%; taker commission: 0.05%" — the page explicitly notes these are **examples only, not the current fee structure**. Page-level last-updated stamp: **"Updated on 2026-04-28 09:10"** (one day before this Phase 3l memo). Confirms BNB discount: **"Users will receive a 10% discount on standard trading fees when they use BNB to pay for trading fees on the Binance Futures platform for USDⓈ-M Futures."**
- `https://www.binance.com/en/futures/trading-rules/perpetual` — accessed 2026-04-29. **Result:** shows BTCUSDT/ETHUSDT contract specifications (see §6 below). Does not list maker/taker fees directly.
- `https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Exchange-Information` (public REST API documentation, no credentials needed) — accessed 2026-04-29. **Result:** documents `GET /fapi/v1/exchangeInfo` response shape: `status`, `baseAsset`, `quoteAsset`, `marginAsset`, `contractType`, `orderTypes`, `timeInForce`; filters PRICE_FILTER (tickSize), LOT_SIZE (stepSize), MARKET_LOT_SIZE, MIN_NOTIONAL (notional), MAX_NUM_ORDERS (limit 200), PERCENT_PRICE; per-symbol fields include `liquidationFee` (example: 0.010000) and `marketTakeBound` (example: 0.30).

### 4.2 Triangulated VIP 0 rates

The official Binance FAQ does not publish the current VIP 0 rate verbatim on the unauthenticated page; the trading-rules page does not show fee rates; the per-account fee page is gated. However:

- **Binance's own illustrative example**, dated "Updated on 2026-04-28 09:10", uses **"regular maker commission: 0.02%; taker commission: 0.05%"** to teach users how fees apply. While Binance describes these as "examples", the example matches the long-published standard VIP 0 rates that are widely documented elsewhere.
- **A web search for current VIP 0 USDⓈ-M Futures fee rates** (third-party crypto-exchange-comparison sites; secondary-source consensus) returns the same rates: **maker 0.0200%, taker 0.0500%** for VIP 0 on USDⓈ-M Futures. The consensus is consistent across multiple independent third-party sources.
- **No higher-VIP-tier rates are observable** without operator login. VIP tier discounts exist (the FAQ confirms it conceptually) but specific tier-by-tier rates are gated.

**Triangulated public consensus:** USDⓈ-M Futures VIP 0 maker = 0.0200% (2 bps); taker = 0.0500% (5 bps). The Prometheus committed `taker_fee_rate = 0.0005 = 0.05%` matches the consensus VIP 0 taker rate exactly and bit-for-bit. No BNB discount is applied (the project does not assume the operator pays fees in BNB), which is conservative by ~10% per the publicly-documented BNB discount.

### 4.3 Whether the project's taker assumption is reasonable

- **Reasonable / matches public consensus.** The committed 5-bps taker rate is the standard published VIP 0 USDⓈ-M Futures rate. It is neither a discount-tier optimistic assumption nor an above-tier pessimistic one. It is conservative versus a (future) BNB-discount-enabled tier (which would give ~4.5 bps).
- **Maker rate is not used.** The strategy spec uses MARKET entries + STOP_MARKET protective stops; the maker rate (≈ 0.02% / 2 bps VIP 0) does not enter the cost calculation. This is correct given the locked spec; if a future variant uses limit orders for entries (the R2 diagnostic-only limit-at-pullback intrabar fill model), the maker rate would become relevant.
- **No VIP-tier optimism.** The committed value does not assume the operator qualifies for VIP discounts. At Prometheus's tiny-live-scale planned trading volume, VIP 0 is the realistic tier; this is conservative for any future scaled-live tier (which might qualify for VIP 1+ rates).

**Result for §4 question:** the default taker-execution assumption is **realistic for VIP 0** and **conservative for any higher VIP tier** the operator might eventually qualify for. Maker execution is correctly excluded from the locked spec's cost model.

---

## 5. External fee-type evidence

### 5.1 Commission fees

Per §4.2 above. VIP 0 maker = 0.0200% / taker = 0.0500% (consensus from secondary public sources + Binance's illustrative example dated 2026-04-28). BNB-payment discount: 10% off futures fees, available publicly (Binance FAQ, accessed 2026-04-29). Higher VIP tiers reduce both maker and taker rates progressively but the specific tier-by-tier rates are gated behind login.

### 5.2 Funding fees

Per the Binance FAQ: USDⓈ-M Futures perpetual contracts implement funding payments **between traders** (not paid to the exchange). Funding rate is calculated periodically; for USDⓈ-M perpetuals on BTCUSDT and ETHUSDT, the standard settlement frequency is **every 8 hours (3 events per day)**. Funding accrues over the holder's position duration; long pays short when funding rate is positive; short pays long when funding rate is negative.

The Prometheus cost model integrates funding via the v002 funding-rate dataset (per §3.5). Phase 3j D1-A M2 result confirmed empirically that the **per-trade funding accrual is small** (BTC mean +0.00234 R, ~21× below the M2 +0.05 R threshold; ETH mean +0.00452 R, ~11× below). This is consistent with most D1-A trades exiting on STOP or TARGET within ≤ 32 bars (≤ 8 hours), so most trades cross at most one funding cycle and the per-cycle accrual on a 0.25%-risk position is economically small.

### 5.3 Insurance / clearance / liquidation-related fees

The public exchangeInfo REST documentation lists a per-symbol field `liquidationFee` (example value `0.010000` = 1.000% in the published example). This is a fee applied **on liquidation**, not on normal trade execution. The Prometheus locked spec uses 0.25% risk per trade with a 2× max effective-leverage cap and an internal notional cap; the structural-stop + ATR-buffer geometry intentionally aims to avoid liquidation. Liquidation-edge-case fees are **not** part of the normal backtest cost model and should not be confused with the per-trade taker / slippage / funding stack.

Insurance / clearance fees per se are not separately published as additional execution costs for normal trading; they are part of Binance's market-structure machinery that Prometheus does not directly accrue under non-liquidation conditions.

### 5.4 Distinguishing normal cost stack from liquidation edge cases

For the Prometheus locked spec's normal trading scope (R3 / H0 / R1a / R1b-narrow / R2-committed-path / F1 / D1-A; all with structural-stop or 1.0×ATR stop, none aiming for liquidation), the **normal-trading cost stack is exactly what `config.py` models**:

```text
round-trip cost = 2 × per-side slippage + 2 × taker_fee_rate × notional + funding accrual over hold
```

`liquidationFee` is an edge-case cost not accrued under normal trading. It does not enter `config.py`'s cost computation; this is correct.

---

## 6. Exchange trading-rule / metadata evidence

### 6.1 Public trading-rules page (`https://www.binance.com/en/futures/trading-rules/perpetual`, accessed 2026-04-29)

| Symbol | Min trade amount | Tick size | Price precision | Min notional | Max open orders | Price protection |
|--------|------------------|-----------|-----------------|-------------:|----------------:|------------------:|
| BTCUSDT perpetual | 0.001 BTC | 0.10 USDT | 0.01 | 50 USDT | 200 | 5% |
| ETHUSDT perpetual | 0.001 ETH | 0.01 USDT | 0.01 | 20 USDT | 200 | 5% |

(Quoted verbatim from the trading-rules page text returned by the public fetch.)

### 6.2 Public exchangeInfo REST documentation

Filter shapes per the public REST docs:

- `PRICE_FILTER` — tickSize (e.g., "0.10" for BTCUSDT, "0.01" for ETHUSDT).
- `LOT_SIZE` — stepSize (e.g., "0.001" for both BTCUSDT and ETHUSDT minimum trade amounts).
- `MARKET_LOT_SIZE` — maximum quantity for market orders.
- `MIN_NOTIONAL` — `notional` field (e.g., "50.0" for BTCUSDT, "20.0" for ETHUSDT per the trading-rules page; the docs example shows "5.0" for a different symbol).
- `MAX_NUM_ORDERS` — `limit: 200`.
- `MAX_NUM_ALGO_ORDERS` — algo-order count cap.
- `PERCENT_PRICE` — price-protection band (5% per the trading-rules page).

The public exchangeInfo fields documented include `liquidationFee` (per-symbol, e.g. `0.010000`) and `marketTakeBound` (e.g. `0.30`). These are part of the public REST shape and are consumed by `src/prometheus/core/exchange_info.py`'s `ExchangeInfoSnapshot`.

### 6.3 Whether current Prometheus research notional sizes are likely above minimums

Prometheus's locked spec uses sizing_equity_usdt = 10,000 USDT, risk_fraction = 0.0025 (0.25%), risk_usage_fraction = 0.90 (effective ≈ 22.5 USDT per-trade risk), max_effective_leverage = 2.0, max_notional_internal_usdt = 100,000.

- **Risk per trade ≈ 22.50 USDT.** With BTC stop-distance ≈ 1.0 × ATR(20) at typical R-window prices ($30K–$100K) and ATR ≈ 0.6–1.2% of price, stop_distance ≈ $200–$1200 per BTC; quantity ≈ 0.018–0.11 BTC ≈ $1,800–$5,500 notional at typical BTC prices.
- **ETH analogous:** stop_distance varies similarly; quantity ≈ 0.7–4.5 ETH ≈ $1,000–$15,000 notional at typical ETH prices.

Both symbols' typical Prometheus notional ($1K–$15K) is **comfortably above the 50 USDT BTCUSDT min-notional and the 20 USDT ETHUSDT min-notional** by 2–3 orders of magnitude. Min-notional constraints are not binding at the locked sizing scale.

### 6.4 Whether tick / step constraints are material

- BTCUSDT tick = 0.10 USDT. At BTC price $50K, tick = 0.0002% of price = 0.02 bps. Stop / target prices rounded to 0.10 USDT ticks introduce at most 0.5-tick bias = 0.0001% = 0.01 bps per leg. This is **completely negligible** versus 1–8 bps slippage tiers.
- ETHUSDT tick = 0.01 USDT. At ETH price $3K, tick = 0.0003% of price = 0.03 bps. Half-tick rounding ≈ 0.015 bps. Also negligible.
- BTCUSDT stepSize = 0.001 BTC. At $50K BTC, smallest increment = $50; the locked sizing typically rounds quantity down by < 0.001 BTC, producing < 0.01% sizing-rounding loss. Not material to cost analysis.
- ETHUSDT stepSize = 0.001 ETH. At $3K ETH, smallest increment = $3; same conclusion.

**Tick / step / min-notional constraints are not material at the locked Prometheus research scale.** They become more material at scaled-live equity tiers (operator-driven future decision); not relevant to current research.

---

## 7. Spread / slippage evidence

### 7.1 What was sought

Public, non-authenticated tick-level or aggregate spread/slippage evidence for BTCUSDT and ETHUSDT perpetuals on Binance USDⓈ-M Futures, ideally over the R-window 2022-01-01 → 2025-01-01 to match the strategy backtest's economic regime, or at minimum a current-period snapshot for calibration.

### 7.2 What was actually obtainable from public sources

**Insufficient.** The public Binance pages accessed in §4.1 do **not** publish historical or current spread distributions, depth profiles, or realized impact statistics. Third-party providers (Kaiko, CryptoCompare, academic microstructure databases) typically charge for tick-level data and gate non-trivial query volumes behind subscriptions. Within the Phase 3l brief constraints (no credentials; no authenticated access; no `data/` commits; no fabrication of facts), no rigorous spread / depth / impact dataset is collectable from public Binance pages alone.

### 7.3 What general-knowledge / qualitative public consensus supports

The cryptocurrency-research literature and public Binance order-book observations (qualitative, not measured here) commonly indicate:

- BTCUSDT perpetual on Binance USDⓈ-M is among the **most liquid USDT-perp instruments globally**. Top-of-book spread is typically **≈ 0.1 tick (0.10 USDT) ≈ 0.1–0.3 bps** at typical BTC prices ($30K–$70K range over the R-window).
- ETHUSDT perpetual is **also highly liquid** but typically has spreads slightly wider than BTC's in relative-bps terms; consensus typical top-of-book ≈ 0.3–0.6 bps.
- Spread widens during high-volatility events; intraday distributions are right-skewed; typical 95th-percentile spreads can reach several bps under stress.

These are qualitative consensus statements, not measurements obtained from public Binance data within Phase 3l; **they should not be treated as quantitative evidence for or against the project's slippage tier calibration.**

### 7.4 Plausibility assessment of 1 / 3 / 8 bps per-side tiers

- **LOW = 1 bps per side.** Approximately the typical top-of-book half-spread under normal conditions on BTCUSDT perp; possibly slightly tight relative to typical ETH ≈ 0.3–0.6 bps half-spread. Plausible as a "favorable execution" floor; consistent with the order of magnitude of typical top-of-book conditions on the most-liquid USDT-perps.
- **MEDIUM = 3 bps per side.** Typical "normal-day" execution cost including bid-ask half-spread + a small impact component for ~$5K notional orders. Plausible as the realistic centerpoint.
- **HIGH = 8 bps per side.** Stress-test tier intended (per Phase 2f §11.6) to bracket high-volatility / wide-spread / impactful execution. Per the qualitative consensus, this is plausible as a "stress regime" upper bound — typical 95th-percentile spread under high-volatility conditions on BTCUSDT can exceed normal levels by 3–10×; an 8-bps per-side bound is within the right order of magnitude. The lack of measured Binance-specific evidence prevents a tighter calibration claim.

**Assessment:** the 1 / 3 / 8 bps per-side ladder is **plausible** as labeled tiers (LOW / MEDIUM / HIGH stress) for typical Prometheus-scale BTCUSDT / ETHUSDT execution, but **direct external public evidence specifically validating these calibrations is not obtainable within Phase 3l's docs-only public-sources constraints.** The committed values are not contradicted by any obtained external evidence; nor are they directly quantitatively confirmed.

**Phase 3l explicitly avoids false precision.** The "plausible" assessment is a qualitative match to consensus expectations; it is not a substitute for rigorous tick-level measurement (which is operator-driven and beyond Phase 3l's scope).

---

## 8. Order-book depth evidence

### 8.1 What was sought

Qualitative or quantitative public evidence about BTCUSDT and ETHUSDT perpetual order-book depth at typical Prometheus research notionals ($1K–$15K typical entries; up to $20K under locked spec at 10K equity × 2× leverage; up to $100K notional cap).

### 8.2 What was obtainable

No depth snapshots were retrieved within Phase 3l (no credentials; no public Binance depth-snapshot endpoint accessed; no `data/` commits). Binance does publish the public depth-snapshot endpoint `GET /fapi/v1/depth` without authentication, but Phase 3l's docs-only / no-fabrication / no-`data/`-commit discipline excludes capturing or committing depth snapshots even from public endpoints.

### 8.3 Qualitative depth consensus

Public consensus (industry write-ups; not measured here): BTCUSDT and ETHUSDT perpetuals on Binance USDⓈ-M typically have **top-of-book depth in the millions-of-USD range** during normal conditions. Typical Prometheus research entry notionals ($1K–$15K) are **2–4 orders of magnitude below typical top-of-book depth**, which means market-impact slippage is dominated by spread (not depth) for these notionals in normal conditions.

### 8.4 Implication

At Prometheus's locked research scale, market-impact contribution to round-trip cost is **likely small relative to spread and fees**. This is consistent with the LOW / MED / HIGH tiers being interpretable predominantly as spread regimes rather than impact regimes for the current sizing.

This qualitative interpretation is **not a substitute for measured impact data**, and **Phase 3l does not infer live fill quality beyond what evidence supports**. At meaningfully larger notionals (operator-driven future scaled-live equity tiers), market impact would become the dominant factor; this is an operator-driven future-deployment consideration, not a current-research consideration.

---

## 9. Mark-price vs trade-price stop-trigger evidence

### 9.1 What Phase 2w / Phase 3j showed internally

- **Phase 2w (R2):** R2's stop-trigger sensitivity at MED across MARK and TRADE_PRICE was bit-for-bit identical because zero R2 stops gap through on the v002 datasets. Stop-trigger calibration is not the source of R2's §11.6 failure.
- **Phase 3j (D1-A):** D1-A R MED MARK vs MED TRADE_PRICE produced a small but non-zero difference: BTC ΔexpR = −0.05 R (TRADE worse); ETH ΔexpR = −0.08 R (TRADE worse). Mechanism: D1-A's intrabar wick exposure is materially larger than V1's because D1-A's 1.0×ATR stop sits within the typical 15m bar's intrabar range, whereas V1's structural-stop + 0.10×ATR buffer typically sits outside the typical 15m bar's intrabar range.

### 9.2 External Binance evidence

The public Binance FAQ on conditional-orders / stop-orders documents the existence of `workingType=MARK_PRICE` versus `workingType=CONTRACT_PRICE` (= trade price) options. The MARK_PRICE option triggers stops based on the mark price index (smoothed, less manipulation-prone); the CONTRACT_PRICE option triggers based on last trade price. Binance officially recommends MARK_PRICE for protective stops; the v1 Prometheus protective-stop spec mandates MARK_PRICE (`workingType=MARK_PRICE`).

`priceProtect=TRUE` (also part of the v1 spec) further constrains stop trigger to within a band of mark price (5% per the trading-rules page), reducing gap-through-mid risk.

### 9.3 Whether external evidence supports treating mark and last/trade price differently

**Yes.** Binance's public documentation supports the distinction; the live behavior MARK_PRICE = mark-price-triggered, CONTRACT_PRICE = trade-price-triggered is part of the public exchange model. The Prometheus default (MARK_PRICE) matches the v1 protective-stop spec and the live-runtime intent.

**Phase 3l does NOT change stop-trigger policy.** The diagnostic remains a research sensitivity axis (`StopTriggerSource.TRADE_PRICE` available only as an explicit diagnostic switch). MARK_PRICE remains the committed default.

---

## 10. Funding-cost evidence

### 10.1 Official funding-fee mechanics

Per Binance FAQ + public USDⓈ-M Futures documentation:

- **Funding payments are between traders, not paid to Binance.** Long pays short when funding rate is positive; short pays long when funding rate is negative.
- **Settlement frequency on BTCUSDT and ETHUSDT perpetuals: 8 hours (3 events per day, at 00:00 / 08:00 / 16:00 UTC standard).**
- **Funding rate is bounded** by Binance's risk machinery (typical bound: ±0.75% per 8-hour cycle, though typical realized values are far smaller).
- **Funding accrues only on positions held through the funding settlement timestamp.** Positions opened and closed within a single 8-hour window pay no funding.

### 10.2 Why D1-A M2 failure is consistent with empirically-small funding accrual

D1-A's M2 metric is `funding_pnl / realized_risk_usdt` per trade:

- BTC: mean +0.00234 R per trade (~21× below the M2 PASS threshold of +0.05 R).
- ETH: mean +0.00452 R per trade (~11× below the M2 PASS threshold).

Since D1-A's 32-bar (8-hour) time-stop is exactly one funding-settlement cycle, most D1-A trades cross at most one funding event before exit. With realized risk = 22.5 USDT (0.25% × 9000 USDT after 90% usage) and typical realized funding-rate per cycle on the order of 0.01–0.05% on the position notional, the per-trade funding accrual is on the order of 0.5–2 cents per trade — i.e., 0.001–0.005 R when normalized. The empirical +0.0023 R / +0.0045 R values match this back-of-envelope expectation.

**Funding accrual is empirically small relative to per-trade risk.** This is not a Prometheus cost-model deficiency; it is an accurate empirical reflection of how funding cost actually behaves at the locked sizing scale.

### 10.3 Phase 3l does NOT change D1-A verdict

D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other per Phase 3h §11.2. The M2 FAIL is a real finding about the strategy's hypothesis (the funding-discount sub-hypothesis is empirically falsified at the locked scale), not a cost-model artifact. Phase 3l does not propose any D1-A re-evaluation.

---

## 11. Impact assessment

Of the five primary assessment categories, Phase 3l selects exactly one:

- **A. Current cost model appears broadly reasonable.** Taker-fee assumption matches the publicly-known VIP 0 standard rate exactly. Slippage tiers (1/3/8 bps per side) are plausible given qualitative consensus about BTCUSDT/ETHUSDT perpetual liquidity. Mark-price stop-trigger matches Binance's public stop-order machinery and live-runtime intent. Funding modeling is empirically validated by D1-A's M2 result.
- **B. Current cost model appears conservative but defensible.** Same evidence pattern as (A), with the additional observation that the project does NOT assume any BNB discount (~10% available publicly) or any VIP volume discount. The committed taker rate is therefore conservative for any operator who eventually qualifies for tier discounts, and conservative against the BNB-pay-discount option. The slippage tiers are also plausibly conservative for typical Prometheus-scale notionals on the most-liquid pairs.
- **C. Current cost model appears too optimistic.** No evidence obtained within Phase 3l supports this. Slippage tiers are plausible at the order-of-magnitude level; impact is small at locked sizing scale; funding accrual is empirically small; mark-price stop-trigger matches live intent.
- **D. Evidence is insufficient to revise.** Direct, measured BTCUSDT/ETHUSDT perpetual tick-level spread / depth / impact / funding distributions over the R-window were not obtainable from public, non-authenticated, non-`data/`-committing sources within Phase 3l. The slippage tier calibration specifically lacks rigorous external public corroboration; the assessment in §7.4 is qualitative consensus, not measurement.
- **E. Evidence suggests future formal cost-model revision may be warranted.** No specific evidence-driven trigger is observed. The §11.6 framework discipline anchor (per Phase 2y) is preserved.

### 11.1 Primary assessment selection

**Primary assessment: B — Current cost model appears conservative but defensible.**

Rationale:

- The committed taker-fee rate (`taker_fee_rate = 0.0005 = 0.05%`) matches the publicly-known VIP 0 USDⓈ-M Futures standard taker rate exactly. The model does NOT assume the operator pays in BNB (which would give ~10% off → effective ~0.045%). The model does NOT assume VIP-tier discounts. Both of these are sources of conservatism without exaggeration.
- Slippage tiers (1/3/8 bps per side) are plausible at the order-of-magnitude level for BTCUSDT/ETHUSDT perpetuals at Prometheus research notionals. The MEDIUM tier (3 bps per side / 6 bps round-trip) is a realistic centerpoint that tracks typical normal-conditions execution; HIGH (8 bps / 16 bps round-trip) is a defensible stress-test bound. The lack of measured tick-level public Binance evidence prevents a tighter claim, but no obtained evidence contradicts the calibration either.
- Mark-price stop-trigger (default) matches Binance's public stop-order machinery and the v1 protective-stop spec live-runtime intent. The MARK_PRICE / TRADE_PRICE diagnostic distinction matches the public `workingType` parameter in Binance's order model.
- Funding modeling is empirically validated by D1-A's M2 measurement (per-trade accrual on the order of 0.001–0.005 R, consistent with the 8-hour settlement cycle × locked sizing × realized funding-rate magnitudes).
- Tick / step / min-notional constraints are not material at locked research sizing (§6.3 / §6.4).

**A "B-shape" sub-finding:** the slippage-tier calibration specifically rests on qualitative consensus rather than direct measurement. A future operator-authorized phase could pursue rigorous measurement; that is a legitimate further-evidence pathway, not a Phase 3l conclusion.

---

## 12. §11.6 policy recommendation

Three options:

- **Keep §11.6 unchanged.**
- **Keep §11.6 unchanged pending stronger evidence.**
- **Recommend a future docs-only cost-model revision phase.**

### 12.1 Recommended option

**Phase 3l recommends: KEEP §11.6 UNCHANGED PENDING STRONGER EVIDENCE.**

Rationale:

- **No internal evidence supports revision.** Phase 2y already established this; Phase 3l does not produce new internal evidence (no backtest run; no candidate re-evaluated).
- **No external evidence obtained within Phase 3l directly contradicts the current §11.6 = 8 bps HIGH per side calibration.** Public Binance pages do not publish tick-level spread / depth measurements that would either confirm or refute 8 bps as the right stress-test bound.
- **No external evidence obtained within Phase 3l directly supports relaxing or tightening §11.6.** The qualitative consensus pattern (§7.4) is consistent with 8 bps being a plausible upper-bound stress regime for BTCUSDT/ETHUSDT perpetual at Prometheus-scale notional, but is not measured.
- **The §11.3.5 framework-discipline anchor is preserved.** Per Phase 2y closeout: "no post-hoc loosening of any threshold to rescue a specific candidate's verdict". Phase 3l explicitly does NOT propose §11.6 relaxation; explicitly does NOT rescue R2 / F1 / D1-A (which would require operator-authorized re-classification phases under any hypothetical revised gate, and which would depend on per-candidate independent re-evaluation, not on §11.6 calibration alone).
- **"Pending stronger evidence" framing leaves the door open for a future operator-authorized cost-model revision phase** if and when the operator independently judges that rigorous tick-level Binance-specific evidence-gathering is warranted. Phase 3l does not pre-authorize such a phase.

**Phase 3l does NOT change §11.6.** `DEFAULT_SLIPPAGE_BPS` map (`LOW=1.0 / MEDIUM=3.0 / HIGH=8.0` per side) preserved verbatim. `taker_fee_rate=0.0005` preserved verbatim.

### 12.2 What would warrant a future formal cost-model revision phase

Phase 3l does not authorize one, but documents what evidence would be sufficient to motivate a separately-authorized operator decision:

- **Rigorous, measured BTCUSDT and ETHUSDT perpetual round-trip slippage distribution** at Prometheus-scale notional ($1K–$200K range) over the R-window 2022-01-01 → 2025-01-01, sourced from authenticated tick-level data (Binance API with operator-approved access, third-party paid microstructure provider, or operator-recorded paper/shadow-period live evidence).
- **Per-regime spread / impact decomposition** (e.g., 95th-percentile spread under high-volatility windows; top-5-level impact for typical Prometheus order sizes).
- **Per-symbol fee-tier evidence**: the operator's actual planned VIP tier; whether BNB-pay-discount will be used; any non-standard fee arrangements.
- **Latency measurement** for the planned NUC + Binance live setup (next-bar-open fill realism).

These evidence requirements mirror Phase 2y §5.1 / §5.3. Phase 3l confirms they remain operator-driven and outside the scope of any docs-only follow-on phase that does not also have authenticated-data access.

---

## 13. Effect on prior verdicts

**Phase 3l explicitly does NOT revise any prior verdict.** The following are preserved verbatim:

- **R3 remains V1 breakout baseline-of-record** per Phase 2p §C.1.
- **H0 remains V1 breakout framework anchor** per Phase 2i §1.7.3.
- **R1a, R1b-narrow, R2, F1, D1-A remain retained research evidence only**; non-leading.
- **R2 remains FAILED — §11.6 cost-sensitivity blocks** per Phase 2w §16.1.
- **F1 remains HARD REJECT** per Phase 3c §7.3 catastrophic-floor predicate; Phase 3d-B2 terminal for F1.
- **D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other** per Phase 3h §11.2; Phase 3j terminal for D1-A under current locked spec.

**No backtest is rerun.** No candidate is rescued. No re-classification phase is authorized.

---

## 14. Risk of circular reasoning

### 14.1 Why cost-policy review must not be used to rescue failed candidates

Per Phase 2y §3.3 framework-discipline anchor: "**no post-hoc loosening of any threshold to rescue a specific candidate's verdict.**" Phase 2f §11.3.5 binds this verbatim. If Phase 3l (or any successor cost-policy phase) revised §11.6 because R2 failed at HIGH or because D1-A's cond_iv FAIL was at the §11.6 boundary, the revision would be a disguised post-hoc rescue. The threshold-revision question must be **independent** of any specific candidate's framework outcome.

The temporal proximity between R2's failure → Phase 2y → R2/F1/D1-A failures → Phase 3l makes this discipline particularly important. Phase 3l explicitly affirms it.

### 14.2 Symmetric-outcome discipline

A rigorous cost-policy review must accept any of three possible outcomes:

- **Threshold left unchanged** (Phase 2y outcome; Phase 3l outcome).
- **Threshold tightened** (if measured evidence shows current calibration understates real costs).
- **Threshold relaxed** (if measured evidence shows current calibration overstates real costs).

The phase must accept any outcome before evidence is gathered; an evidence-gathering phase that accepts only one direction is itself a discipline violation. Phase 3l's Phase 3k authorization explicitly required "ex-ante operator commitment to symmetric-outcome discipline ('the outcome could go either way; revision is not the goal')". Phase 3l affirms this: the "B" assessment in §11 is not engineered to support a particular threshold direction; it is a defensible reading of the evidence available within the brief's docs-only public-sources scope.

### 14.3 What evidence would be strong enough for a future revision

- **Rigorous, measured, multi-period, multi-condition tick-level data** demonstrating that the current 8 bps HIGH per-side calibration is materially miscalibrated (in either direction). "Materially" means well outside any defensible interpretation of the current tier (e.g., realized 95th-percentile round-trip slippage measuring 4 bps or 30 bps, not 5–25 bps which is consistent with current calibration).
- **Independent third-party verification** of the dataset and methodology to rule out cherry-picked windows, regime-conditional bias, or sample-size artifacts.
- **Per-symbol evidence** (BTCUSDT and ETHUSDT separately) since the §11.6 / §11.4 gates are evaluated per symbol.
- **Operator-explicit deployment-tier decision**: the cost calibration depends on the operator's actual planned VIP tier and BNB-pay choice; revising the calibration must be paired with operator commitment about which tier the calibration represents.

### 14.4 What evidence would be insufficient

- **Qualitative consensus alone** (as in §7.3 / §7.4 / §8.3 above). Phase 3l's qualitative reading of public discourse is informative but does not justify a threshold revision.
- **Single-regime or single-period measurements** (e.g., a calm-market 1-week sample). The R-window spans 36 months including bull/bear/chop regimes; calibration must be regime-robust.
- **Third-party derived statistics without methodology disclosure** (e.g., "BitDegree says X" without verifiable source data).
- **A specific candidate's (R2, F1, D1-A) framework outcome** — the rescue-prevention rule §11.3.5 forbids this as a threshold-revision motivation.
- **A small Prometheus-internal paper/shadow sample** if/when paper/shadow is authorized — too small to recalibrate a multi-year-windowed framework threshold.

---

## 15. Operator decision menu after Phase 3l

Seven options enumerated below.

### 15.1 Option A — Remain paused

**What it would answer:** Same as Phase 3k §8.1 (preserve current state; surrender strategic direction to operator).

**Why it may be useful:** Compatible with Phase 3l's "B — conservative but defensible" assessment: no urgency to act on cost-policy. Compatible with Phase 3k's primary recommendation to remain paused (Phase 3l's existence over Phase 3k's primary did not change the underlying treadmill / framework-fail pattern; the §11.6 threshold is preserved either way).

**Why it may be dangerous:** Project loses momentum; strategic clarity may degrade. Operator's selection of Phase 3l (an active path) over Phase 3k's primary (remain-paused) is noted; if Phase 3l's outcome reverts to "remain paused", the operator has now had two consecutive opportunities to authorize active research and has chosen to pause both times — which is itself a strong strategic signal but does not require Phase 3l to mandate further inaction.

**Violates current restrictions?** No.

**Should be recommended now?** **YES — primary recommendation.** Phase 3l's "B" assessment supports preserving the framework; no specific evidence-driven trigger justifies an active follow-on phase.

### 15.2 Option B — Formal cost-model revision memo (docs-only)

**What it would answer:** Should `DEFAULT_SLIPPAGE_BPS` and / or `taker_fee_rate` be revised in `config.py` based on evidence beyond Phase 3l's docs-only public-sources scope?

**Why it may be useful:** A docs-only formal revision memo would specify exactly what evidence-gathering is required (rigorous tick-level data; per-symbol distributions; per-regime decomposition; operator-tier-explicit assumptions) and, conditional on evidence-gathering being completed, propose a specific numerical revision (with §11.3.5 + symmetric-outcome discipline).

**Why it may be dangerous:** Phase 3l's "B" assessment does not produce a specific evidence-driven trigger for revision. Authorizing a formal revision memo without a trigger risks becoming the post-hoc-loosening pattern Phase 2y warned against. The memo would also lack actionable evidence-gathering capability under current docs-only / no-credentials / no-`data/`-commits constraints.

**Violates current restrictions?** No (docs-only).

**Should be recommended now?** **NO.** Phase 3l's evidence does not motivate a formal revision memo at this time. If the operator independently gathers external evidence (e.g., Binance API tick-level data via operator-authorized tooling) that supports a calibration revision, a future operator decision can authorize a Phase 3l-prime revision memo.

### 15.3 Option C — Regime-first research framework memo (docs-only)

**What it would answer:** Same as Phase 3k §8.3 (regime-conditional decomposition memo).

**Why it may be useful:** Same as Phase 3k §8.3.

**Why it may be dangerous:** Same as Phase 3k §8.3 (high overfitting / circular-reasoning risk; Phase 4 dependence; risk of becoming the next rank-1 candidate that framework-fails).

**Violates current restrictions?** No (docs-only).

**Should be recommended now?** **NO** in Phase 3l. The regime-first option remains the Phase 3k tertiary alternative if the operator selects it as a separate decision; Phase 3l's evidence does not particularly support or oppose it. Both Phase 3k §8.3 caveats remain binding (anti-circular-reasoning discipline; Phase 4 dependence).

### 15.4 Option D — 5m timeframe feasibility memo (docs-only)

**What it would answer:** Could using a 5m signal timeframe (instead of the current 15m) materially change cost-sensitivity profiles, mechanism-detection horizons, sample-size, or per-regime stationarity for any retained-evidence candidate or future hypothesis?

**Why it may be useful:** A novel docs-only investigation distinct from regime-first or cost-policy-revision. 5m timeframe would multiply trade frequency by ~3× per unit calendar time, narrow the typical bar's intrabar range vs ATR, change the M1-style post-entry counter-displacement horizon characterization, and shift the per-trade cost ratio (since slippage is per-trade and frequency-amplifying).

**Why it may be dangerous:**

- **Frequency × per-trade-expR catastrophic aggregation risk.** F1's catastrophic outcome at 15m fired at ~150× H0/R3 frequency; 5m would compound this concern. If a candidate's per-trade expR is similar to its 15m sibling but trade frequency is 3× higher, aggregate equity loss is 3× larger.
- **Cost-amplification.** Per-trade fixed costs (taker fee + slippage minimum) are amplified at higher frequency; a 5m candidate must produce per-trade-expR positive enough to overcome 3× the aggregate cost burden.
- **No evidence currently authorizes lifting the locked v002-dataset 15m / 1h decomposition.** v002 includes 15m klines; switching to 5m as primary signal may require v003 raw-data work (5m kline fetch from Binance), which is outside the Phase 3l brief.
- **Phase 3l brief does NOT authorize starting 5m timeframe feasibility; it asks Phase 3l to evaluate it as a docs-only menu option.** A docs-only 5m feasibility memo could enumerate required v003 data work, expected sample-size implications, expected cost-amplification, and required mechanism-prediction recalibration.
- **Risk of treadmill expansion.** Phase 3l's framework-fail pattern (R2 / F1 / D1-A) under 15m + locked-spec discipline does not specifically motivate timeframe change as the right response; cost-sensitivity-driven failures at 15m are unlikely to become cost-sensitivity-passing at 5m without independent edge.

**Violates current restrictions?** No (docs-only).

**Should be recommended now?** **NO** in Phase 3l. 5m timeframe feasibility is a legitimate operator-driven future docs-only memo if the operator independently develops a falsifiable hypothesis that benefits from 5m primary signal. Phase 3l's evidence does not specifically motivate it.

### 15.5 Option E — New strategy-family discovery (Phase 3a-style)

**Why it may be useful:** Same as Phase 3k §8.4.

**Why it may be dangerous:** Same as Phase 3k §8.4 (treadmill risk after V1 + F1 + D1-A; rank-3+ candidates ranked below D1 by Phase 3f for documented reasons).

**Violates current restrictions?** **YES — Phase 3l brief explicitly forbids** "Do not authorize ... new strategy discovery, or regime-first work."

**Should be recommended now?** **NO. Forbidden by Phase 3l brief.**

### 15.6 Option F — ML feasibility memo (docs-only)

**Why it may be useful:** Same as Phase 3k §8.5.

**Why it may be dangerous:** Same as Phase 3k §8.5 (severe leakage / overfitting / non-stationarity / cost-sensitivity / explainability risks).

**Violates current restrictions?** **YES — Phase 3l brief explicitly forbids** "Do not authorize ML feasibility ..."

**Should be recommended now?** **NO. Forbidden by Phase 3l brief.**

### 15.7 Option G — Paper/shadow or Phase 4

**Violates current restrictions?** **YES — every brief since Phase 0** explicitly forbids paper/shadow / Phase 4 / live-readiness / deployment work without operator policy lifting that deferral.

**Should be recommended now?** **NO. Forbidden.**

### 15.8 Decision menu summary

| Option | Description | Violates Phase 3l brief? | Recommended now? |
|--------|-------------|:-:|:-:|
| **A** | Remain paused | NO | **YES (primary)** |
| B | Formal cost-model revision memo (docs-only) | NO | NO |
| C | Regime-first framework memo (docs-only) | NO | NO |
| D | 5m timeframe feasibility memo (docs-only) | NO | NO |
| E | New strategy-family discovery memo (docs-only) | YES (Phase 3l brief forbids) | NO (forbidden) |
| F | ML feasibility memo (docs-only) | YES (Phase 3l brief forbids) | NO (forbidden) |
| G | Paper/shadow or Phase 4 | YES (forbidden by every brief) | NO (forbidden) |

### 15.9 Recommended next operator decision

**Phase 3l recommends: REMAIN PAUSED.**

Phase 3l's "B — conservative but defensible" assessment supports preserving the current cost model and §11.6 = 8 bps HIGH per side. No evidence-driven trigger motivates a formal revision; no specific successor candidate is currently developed; treadmill risk after V1 / F1 / D1-A remains elevated. The disciplined response is to surrender strategic direction to operator authority, the same as Phase 3k's primary recommendation. Phase 3l + Phase 3k together leave the operator with a stable post-Phase-3l boundary; the operator may at any future time authorize a separate docs-only memo (formal cost-model revision, regime-first framework, 5m timeframe feasibility) with operator-developed motivation and operator-committed symmetric-outcome discipline.

The recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

## 16. Explicit preservation list

Phase 3l is docs-only and explicitly preserves all of the following verbatim:

- **No threshold changes.** Phase 2f §10.3 / §10.4 / §11.3 / §11.4 / §11.6 = 8 bps HIGH per side preserved. `DEFAULT_SLIPPAGE_BPS` map (LOW=1.0 / MED=3.0 / HIGH=8.0 per side) preserved. `taker_fee_rate=0.0005` preserved.
- **No strategy-parameter changes.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A spec axes preserved verbatim.
- **No project-lock changes.** §1.7.3 locks preserved verbatim.
- **No prior verdict revised.** R2 / F1 / D1-A / R3 / H0 / R1a / R1b-narrow verdicts unchanged.
- **No backtest run.** No engine invocation; no candidate-cell run; no control reproduction.
- **No code change.** No file in `src/`, `tests/`, or `scripts/` touched. `cost-modeling.md`, `backtesting-principles.md`, `phase-gates.md`, `technical-debt-register.md`, `current-project-state.md`, `ai-coding-handoff.md` UNCHANGED.
- **No MCP / Graphify / `.mcp.json` activation.** No MCP server enabled; no Graphify integration; no `.mcp.json` file created or modified.
- **No credentials.** No production / sandbox / testnet API keys requested, created, or used. No `.env` file modified. No secrets in any committed file. No authenticated Binance API calls. No private endpoints accessed.
- **No exchange-write paths.** No exchange-write capability proposed, implemented, or enabled.
- **No `data/` commits.** Phase 3l commits are limited to two new `docs/00-meta/implementation-reports/` files (this memo + closeout report).
- **No next phase started.** Phase 3l is docs-only and terminal-as-of-now. No Phase 3m, no Phase 4, no paper/shadow planning, no formal cost-model revision phase, no regime-first phase, no 5m timeframe feasibility phase authorized.

---

## 17. Sources accessed

External sources accessed during Phase 3l (all public, non-authenticated, no credentials, no `data/` commits; date of access 2026-04-29 UTC):

1. `https://www.binance.com/en/fee/futureFee` — Binance "USDⓈ-M Futures Trading Fee Rate" (gated; requires login for personalized fee table; no public VIP 0 figures returned).
2. `https://www.binance.com/en/support/faq/detail/98488a516eb84e3eb34605683dffd554` — Binance FAQ "Binance Futures Fees Explained" (confirms BNB discount 10%; references VIP tier system; does not list specific rates).
3. `https://www.binance.com/en/support/faq/binance-futures-fee-structure-fee-calculations-360033544231` — Binance FAQ "Binance Futures Fee Structure & Fee Calculations" (illustrative example "regular maker commission: 0.02%; taker commission: 0.05%"; explicitly notes example only; "Updated on 2026-04-28 09:10").
4. `https://www.binance.com/en/futures/trading-rules/perpetual` — Binance "Trading Rules" (BTCUSDT/ETHUSDT contract specifications: tick size, lot size, min notional, price protection 5%, max 200 open orders).
5. `https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Exchange-Information` — Binance public REST API documentation for `GET /fapi/v1/exchangeInfo` (filter shapes; per-symbol field documentation; example values).
6. Web-search corroboration via secondary public sources (TradersUnion crypto-fee summary; BitDegree; CoinPath; HackMD-hosted secondary writeup) — consensus VIP 0 USDⓈ-M Futures rates: maker 0.0200%, taker 0.0500%. Used only as triangulation, not as primary evidence.

**No measurements** (tick-level spread / depth / impact / latency / funding distributions) were captured or committed within Phase 3l. The slippage tier calibration claim is qualitative consensus, not measurement.

**Source freshness caveat.** All fees and trading-rule specifications were accessed 2026-04-29 UTC. Binance fee rates are time-sensitive and may change at the exchange's discretion. The Binance FAQ explicitly notes "The information above may change based on Binance Policies. Please check the Binance platform for the latest updates." Any future use of this evidence for cost-model revision should re-verify currency at the time of revision.

---

**End of Phase 3l external execution-cost evidence review memo.** Phase 3l documents the public, non-authenticated, official-Binance-where-possible execution-cost evidence available; restates the canonical Prometheus cost model; assesses each cost-model component; selects "B — Current cost model appears conservative but defensible" as the primary assessment; recommends "Keep §11.6 unchanged pending stronger evidence" as the §11.6 policy choice; preserves all prior verdicts (R2 FAILED; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; R3 baseline-of-record; H0 framework anchor); and recommends **remain paused** as the next operator decision. R3 remains baseline-of-record; H0 remains framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence. **No threshold changes. No strategy-parameter changes. No project-lock changes. No prior verdict revised. No code / tests / scripts / data / paper-shadow / Phase 4 / live-readiness / deployment / MCP / Graphify / `.mcp.json` / credential / exchange-write change. No next phase started.** Phase 3l is docs-only; the operator decides whether and when to authorize any subsequent phase. Awaiting operator review.
