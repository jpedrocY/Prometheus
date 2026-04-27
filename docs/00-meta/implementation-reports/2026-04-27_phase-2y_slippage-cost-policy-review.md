# Phase 2y — Independent Slippage / Cost-Policy Review Memo

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; **no post-hoc loosening per §11.3.5**); Phase 3 Gate 1 plan §10 (committed cost-model defaults); Phase 2e baseline summary (cost-model recorded as locked Phase 3 defaults); Phase 2l / 2m / 2s / 2w slippage-sensitivity sections; Phase 2v §5.1.7 / §5.4 failure condition 9 (§11.6 HIGH-slip cost-sensitivity gate definition); Phase 2w R2 variant comparison report (§11.6 FAIL); Phase 2x family-review memo (Option C fallback recommendation; this is the executed Option C).

**Phase:** 2y — Independent slippage / cost-policy review. **Docs-only.** Framework-calibration audit, not strategy-redesign and not threshold-change.

**Branch:** `phase-2y/slippage-policy-review`. **Memo date:** 2026-04-27 UTC.

**Status:** Recommendation drafted. **No threshold changed.** **No R2 verdict revised.** R3 remains baseline-of-record. R2 remains retained research evidence. H0 remains framework anchor. All §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds preserved verbatim per Phase 2f §11.3.5. Recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

## 1. Plain-English explanation of what Phase 2y is deciding

Phase 2y is a **framework-calibration audit**, not a strategy-redesign phase.

Phase 2w's R2 (pullback-retest entry) candidate produced a striking shape: it cleared the §10.3 framework at MEDIUM slippage on both symbols (BTC §10.3.a + §10.3.c; ETH §10.3.c) AND showed clean mechanism support (M1 PASS on BTC intersection trades at +0.123 R per trade; M3 PASS on R-distance reduction on both symbols), but failed Phase 2f's §11.6 cost-sensitivity gate when re-evaluated at HIGH slippage (BTC Δexp_H0 −0.014; ETH Δexp_H0 −0.230). The framework verdict was therefore **FAILED — §11.6 cost-sensitivity blocks**, even though the candidate's economic mechanism worked as predicted.

This raised an explicit methodological question that the Phase 2x family-review memo §6 / §7 / §8 elevated to operator-decision territory:

> Is R2's §11.6 failure a genuine **strategy-fragility** finding (R2's edge is real but slippage-sensitive, and the threshold is correctly calibrated to identify that fragility), or a **framework-calibration artifact** (the HIGH = 8 bps threshold is over-conservative relative to Binance USDⓈ-M BTCUSDT's actual live slippage profile, and R2's mechanism is more deployable than the gate suggests)?

Phase 2y's job is to audit the framework's HIGH-slippage threshold against the available evidence and recommend one of three policy directions:

1. **Keep HIGH = 8 bps unchanged.** The threshold is correctly conservative for unsupervised research; R2's FAILED verdict consolidates as a real strategy-fragility finding; the framework discipline §11.3.5 (no post-hoc loosening) is preserved as an explicit anchor against threshold-rescue patterns.
2. **Lower HIGH only with external evidence.** If evidence emerges that 8 bps materially exceeds Binance's actual BTCUSDT futures slippage profile at Prometheus-scale notional, a future operator-policy phase could revise §11.6 — but only on the strength of external evidence, not on the strength of "R2 would have cleared at lower thresholds".
3. **Tighten HIGH if current model is too lenient.** Mirror-image of option 2: if evidence emerges that 8 bps understates actual costs, tighten the threshold. This is also a threshold change requiring external evidence.

**Phase 2y itself does not change any threshold.** Phase 2y produces a recommendation; any actual threshold revision is a separate operator-authorized phase with its own evidence-gathering work and Gate 1 / Gate 2 / Gate 2 review structure. The §11.3.5 binding rule (no post-hoc loosening) is the discipline anchor: Phase 2y's recommendation must explicitly forbid threshold-loosening invoked as a post-hoc rescue of any specific candidate's verdict — including R2's.

This memo is also explicitly **not** an R2 rescue phase. R2 stays at its committed FAILED — §11.6 cost-sensitivity blocks verdict regardless of Phase 2y's recommendation. Even if a future evidence-gathering phase justifies a §11.6 revision, that revision applies to *future* candidates evaluated *under* the revised threshold; it does not retroactively re-classify R2 unless the operator separately authorizes such a re-classification (which would be a meaningful policy decision outside Phase 2y's scope).

---

## 2. Current project cost model

The canonical source-of-truth is `src/prometheus/research/backtest/config.py`. The model has four explicit components and one implicit one.

### 2.1 Slippage tiers (per side; `config.py:55-59`)

```python
DEFAULT_SLIPPAGE_BPS: dict[SlippageBucket, float] = {
    SlippageBucket.LOW: 1.0,        # 0.01% per side
    SlippageBucket.MEDIUM: 3.0,     # 0.03% per side  (committed default)
    SlippageBucket.HIGH: 8.0,       # 0.08% per side
}
```

Round-trip slippage = 2 × per-side (entry + exit, both adverse direction):

| Tier | Per-side bps | Round-trip bps |
|------|-------------:|---------------:|
| LOW | 1.0 | 2.0 |
| MEDIUM (committed) | 3.0 | 6.0 |
| HIGH | 8.0 | 16.0 |

### 2.2 Taker fee assumption

`config.py:87`: `taker_fee_rate: float = 0.0005` (committed default). 5 bps per side; 10 bps round-trip. This is consistent with Binance's standard taker tier without VIP volume discounts and without BNB-token-fee discounts. Phase 2e / 2g / 2h / 2i committed this as the Phase 3 default. Maker rate is not used by the strategy spec — H0 / R3 / R1a / R1b-narrow / R2 (committed path) all use market entries for the entry-fill, and STOP_MARKET orders for protective stops (which fill at taker rate when triggered).

### 2.3 Round-trip per-trade transaction-cost stack

| Tier | Slippage (round-trip) | Taker fees (round-trip) | Total bps |
|------|---------------------:|------------------------:|----------:|
| LOW | 2 | 10 | 12 bps |
| MEDIUM (committed) | 6 | 10 | 16 bps |
| HIGH | 16 | 10 | 26 bps |

For perspective, at risk_fraction = 0.0025, sizing equity = 10,000 USDT, max_effective_leverage = 2×, and BTCUSDT prices in the $30K–$70K range over the R-window, typical position notional ranges roughly $4K–$20K depending on stop-distance. The HIGH tier's 26-bps round-trip cost translates to approximately $1–$5 per trade on cost alone, or roughly $0.04–$0.20 per contract at typical contract size. In R-multiple terms, 16 bps slippage at typical risk-distance and at 2× leverage produces a per-trade cost increase of approximately +0.05 to +0.10 R per trade going from MED to HIGH on a long-side stop-distance fill — which is exactly the observed pattern in the candidate slippage-sensitivity tables.

### 2.4 Mark-price stop-trigger policy

`config.py:38-49` defines `StopTriggerSource = {MARK_PRICE, TRADE_PRICE}`, with `MARK_PRICE` as the committed default (mirrors live `workingType=MARK_PRICE` per the v1 protective-stop spec). `TRADE_PRICE` is a research-only sensitivity diagnostic introduced in Phase 2g per GAP-20260424-032. Across all four candidates (R3, R1a+R3, R1b-narrow, R2+R3), MARK_PRICE and TRADE_PRICE produce **bit-identical** results because zero stops gap through on the committed v002 datasets.

### 2.5 How costs are applied in backtests

Per Phase 3 Gate 1 plan §10 and `src/prometheus/research/backtest/engine.py`:

- **Slippage on entry:** `effective_entry_price = fill_price × (1 + slippage_bps × sign / 10_000)`, where `sign = +1 for long`, `−1 for short` (adverse direction at fill).
- **Slippage on exit:** mirror-image at exit fill (adverse direction at exit).
- **Taker fees:** applied at entry and at exit, computed as `notional_at_fill × taker_fee_rate`.
- **Funding:** applied via historical funding-rate joins from the v002 funding-rate dataset; integrated over the trade's hold period. Mark-price values used where required; pre-2024 funding events are handled with `mark_price=None` per the Phase 2e baseline summary.
- **All §10.3 / §10.4 / §11.3 / §11.4 / §11.6 metrics are computed on net-of-cost net-R-multiple values.** Per `docs/05-backtesting-validation/cost-modeling.md`: "all validation is net of cost; all futures research includes funding."

### 2.6 Documentation inconsistency to flag (out-of-scope for Phase 2y)

**The Phase 2l (R3 first execution) variant comparison report at line 331 and the Phase 2m (R1a+R3) variant comparison report at line 350 both state:** "GAP-20260424-032 carry-forward + Phase 2f §11.6 cost-sensitivity gate. LOW = 0 bps; MEDIUM = 5 bps (baseline); HIGH = 15 bps (3× baseline)."

These numerical claims are **stale relative to the canonical config.py** (which committed `LOW=1.0 / MEDIUM=3.0 / HIGH=8.0` per side at Phase 3 Gate 1 and has not changed since). The Phase 2e baseline summary, Phase 2g / 2h / 2i / 2j / 2k variant memos, the Phase 3 Gate 1 plan, the Phase 3 Gate 2 review, and the Phase 2w R2 reports all consistently use the canonical 1 / 3 / 8 bps values. The Phase 2l / 2m text appears to describe a conceptually-proposed cost model rather than the values actually used in those phases' executed runs — the numerical results in those reports are consistent with config.py's committed values, not with the inline-described 0 / 5 / 15.

**This memo's own §4 evidence section uses the canonical config.py values verbatim.** The Phase 2x family-review memo §4.5 inherited the stale "MEDIUM (5 bps, committed)" wording from Phase 2l/2m and has the same inconsistency; the candidate-specific numerical results in Phase 2x §4.5 are unaffected (they came from the actual runs, which used config.py).

**Phase 2y does not "fix" this inconsistency** — that would be out of Phase 2y scope. A future docs-only consistency-cleanup phase could correct the Phase 2l / 2m / 2x text without changing any numerical result. Phase 2y's role is to flag the inconsistency for the operator's awareness, not resolve it.

---

## 3. Why Phase 2y exists

### 3.1 Phase 2w R2's specific failure shape

R2's framework verdict was **FAILED — §11.6 cost-sensitivity blocks**, with this distinguishing pattern:

- **R2 cleared §10.3 cleanly at MEDIUM slippage.** BTC Δexp_H0 +0.184 (above §10.3.a's +0.10 threshold); ΔPF +0.274; |maxDD| ratio 0.448× (well below 1.5× veto). ETH Δexp_H0 +0.043 (below §10.3.a's +0.10 threshold; cleared §10.3.c only); ΔPF +0.133; |maxDD| ratio 0.599×. No §10.3 disqualification floor; no §10.4 hard-reject. §11.4 ETH-as-comparison satisfied.
- **R2 showed M1 + M3 mechanism support.** M1: BTC intersection-trade Δexp = +0.123 R (≥ +0.10 R threshold; PASS). M3: R2 mean stop-distance < R3 mean stop-distance on matched signals on both symbols (BTC ratio 0.844; ETH 0.815; PASS). M2: stop-exit fraction R2 > R3 on both (BTC 0.261 vs 0.242; ETH 0.526 vs 0.424; FAIL). Combined: M1 + M3 pass with M2 fail — the smaller-stop / larger-position-size geometry produced real per-trade-expectancy improvement, not selection of trades with lower stop-out rates.
- **R2 failed §11.6 at HIGH slippage.** BTC Δexp_H0 at HIGH slippage = −0.014 (worse than H0; §10.3 disqualification at HIGH); ETH Δexp_H0 at HIGH = −0.230 (severe disqualification at HIGH). Per Phase 2v §5.1.7 / §5.4 failure condition 9, this triggers the §11.6 framework block.

R2's edge is therefore approximately **proportional to the slippage band**: the per-trade expectancy gain (M1 +0.12 R BTC) is in the same magnitude range as the slippage-induced cost increase between MED and HIGH (~0.10 R per trade, depending on R-distance and side). At HIGH, the gain is consumed by cost.

### 3.2 The methodological question

The §11.6 gate is binary: either the candidate clears at HIGH slippage on both symbols, or it doesn't. R2 doesn't. But the gate's design assumption (Phase 2f §11.6) was that HIGH represents a "stress-test cost regime" — sufficiently above realistic live conditions that a candidate clearing HIGH is robustly cost-insensitive. If HIGH = 8 bps is calibrated to Binance's actual BTCUSDT-perp slippage profile, R2's failure is a real strategy-fragility finding. If HIGH = 8 bps is materially above Binance's actual profile, R2's failure is at least partially a framework-calibration artifact.

This is not a question Phase 2y can answer with internal-only evidence. The internal-evidence picture (slippage-sensitivity tables across R3 / R1a+R3 / R1b-narrow / R2+R3) shows what happens **if** HIGH = 8 bps; it cannot tell us **whether** HIGH = 8 bps is the right calibration.

### 3.3 The framework-discipline anchor

Phase 2f §11.3.5 binds: **no post-hoc loosening of any threshold to rescue a specific candidate's verdict.** This rule was created precisely to prevent the failure mode of "framework verdict came out FAILED, so let's revise the framework". A threshold can be revised with external evidence about the framework's calibration, but it cannot be revised because a specific candidate would otherwise have cleared.

The distinction is: "is this threshold the right threshold for our research methodology?" is a legitimate framework-calibration question; "would lowering this threshold rehabilitate R2?" is a post-hoc-loosening question. Phase 2y must answer the former and explicitly forbid the latter.

### 3.4 What Phase 2y must distinguish

Phase 2y must produce a recommendation that distinguishes:

- **Strategy fragility (R2):** R2's edge is real but slippage-sensitive; under Binance's actual live conditions, R2's edge would also be marginal-or-negative; the FAILED verdict reflects reality.
- **Framework over-conservatism:** HIGH = 8 bps materially exceeds Binance's actual live conditions; under accurate calibration, R2's edge would be more robust than the gate suggests.
- **Framework under-conservatism:** HIGH = 8 bps materially understates Binance's actual live conditions; the gate is too lenient; many already-PROMOTED candidates (R3, R1a+R3, R1b-narrow) would also fail under accurate calibration; R3's apparent cost-robustness is partially misleading.

The distinction can only be made with external evidence about Binance USDⓈ-M BTCUSDT-perp's actual slippage profile at Prometheus-scale notional. Phase 2y enumerates the evidence requirements; gathering the evidence is operator-driven, not Claude-Code-driven.

---

## 4. Evidence available from internal project reports

This section catalogs what the internal evidence shows. It is **necessary but not sufficient** for a §11.6 revision — the cost-sensitivity profiles below are what each candidate produced under the assumption that HIGH = 8 bps; they do not validate that HIGH = 8 bps is the correct calibration.

### 4.1 R3 — cost-robust

Per Phase 2l §8 (R3 first execution slippage sensitivity, R-window):

| Slippage | BTC expR | BTC PF | BTC netPct | BTC maxDD | ETH expR | ETH PF | ETH netPct | ETH maxDD |
|----------|---------:|-------:|-----------:|----------:|---------:|-------:|-----------:|----------:|
| LOW | −0.139 | 0.719 | −1.02% | −1.46% | −0.271 | 0.561 | −2.01% | −3.20% |
| MEDIUM (committed) | −0.240 | 0.560 | −1.77% | −2.16% | −0.351 | 0.474 | −2.61% | −3.65% |
| HIGH | −0.445 | 0.359 | −3.29% | −3.69% | −0.549 | 0.316 | −4.07% | −4.79% |

**R3 clears §11.6 robustly.** Even at HIGH (8 bps), R3's BTC expR (−0.445) is still better than H0 at MEDIUM (−0.459); R3's ETH expR (−0.549) is below H0's −0.475 by less than the §10.3 disqualification floor. No §10.3 disqualification triggered at HIGH. This is the cleanest cost-robustness result the project has produced.

The R3 cost-robustness is **economic-mechanism-driven**: the staged-trailing → fixed-R + time-stop swap captures a structural per-trade improvement large enough to absorb the HIGH-tier cost variation without crossing the disqualification floor.

### 4.2 R1a+R3 — cost-monotone, weaker margin

Per Phase 2m §10:

| Slippage | BTC expR | BTC ΔvH0 | ETH expR | ETH ΔvH0 |
|----------|---------:|---------:|---------:|---------:|
| LOW | −0.319 | +0.140 | −0.022 | +0.453 |
| MEDIUM (committed) | −0.420 | +0.039 | −0.114 | +0.362 |
| HIGH | −0.544 | −0.085 | −0.354 | +0.122 |

**R1a+R3 BTC expR at HIGH (−0.544) is below the §10.4 −0.50 hard-reject boundary in absolute terms but Δn < 0 so §10.4 does not apply by definition.** ΔexpR at HIGH is −0.085 (BTC) — disqualification floor for "expR worsens vs H0" is triggered (Δexp < 0 means R1a+R3 BTC expR is worse than H0 at HIGH). R1a+R3 would technically fail §11.6 at HIGH on the BTC dimension if the §11.6 gate were applied to it (which Phase 2m did not do; §11.6 was only formalized as a hard gate in Phase 2v / 2w in the way that explicitly evaluates HIGH-slip §10.3 disqualification on both symbols).

ETH side: cost-monotone with margin preserved at HIGH (Δexp_H0 +0.122 at HIGH; not disqualified). Phase 2m §10 noted: "ETH at LOW slippage is essentially break-even (expR −0.022, PF 0.965, netPct −0.11%) — confirming that the ETH improvement is robust to cost assumptions."

**Implication for Phase 2y:** R1a+R3 sits closer to the §11.6 boundary than R3. If §11.6 were applied retroactively to R1a+R3 with the same evaluation discipline as R2, the BTC dimension would fail. The Phase 2m PROMOTE verdict precedes the formalization of §11.6 as a hard gate; under the current Phase 2v / 2w gate definition, R1a+R3 would also have a §11.6 issue.

### 4.3 R1b-narrow — cost-monotone, framework-clearing at HIGH

Per Phase 2s §10 (R-window R1b-narrow slippage sensitivity):

| Slippage | BTC expR | ETH expR |
|----------|---------:|---------:|
| LOW | −0.196 | −0.174 |
| MEDIUM (committed) | −0.263 | −0.224 |
| HIGH | −0.389 | −0.371 |

**R1b-narrow PROMOTES at HIGH on both symbols** under Phase 2s's reading. At HIGH (3× baseline as the Phase 2s text describes — though the canonical config.py 8 bps HIGH is closer to 2.7× the canonical 3 bps MED), BTC expR (−0.389) and ETH expR (−0.371) are both still better than H0 at MEDIUM (BTC −0.459 / ETH −0.475). No §10.3 disqualification triggered at HIGH. R1b-narrow's PROMOTE verdict survives the §11.6 evaluation.

**Implication:** R1b-narrow's improvement is also cost-robust, although its absolute improvement is smaller and concentrated in trade-count reduction rather than per-trade-expectancy gain (R3-anchor BTC Δexp_R3 = −0.023; near-neutral marginal contribution).

### 4.4 R2+R3 — cost-fragile (the §11.6 failure case)

Per Phase 2w-B §5.3 / Phase 2w §7.2:

| Slippage | BTC expR | BTC ΔvH0 | BTC §10.3 | ETH expR | ETH ΔvH0 | ETH §10.3 |
|----------|---------:|---------:|-----------|---------:|---------:|-----------|
| LOW | −0.180 | **+0.279** | PROMOTE | −0.481 | **−0.006** | **DISQUALIFIED** |
| MEDIUM (committed) | −0.275 | +0.184 | PROMOTE | −0.432 | +0.043 | PROMOTE |
| HIGH | −0.473 | **−0.014** | **DISQUALIFIED** | −0.705 | **−0.230** | **DISQUALIFIED** |

Two related findings:

- **R2+R3 BTC §11.6 disqualification at HIGH is narrow** (Δexp_H0 −0.014; just below the 0 boundary). At HIGH = 7 bps or HIGH = 6 bps, BTC would clear; the failure is sensitive to the exact threshold value.
- **R2+R3 ETH disqualifies even at LOW** (Δexp_H0 −0.006). This is unique to R2 across the family arc — no other candidate disqualifies at LOW. The ETH cost-fragility is structural, not threshold-driven; it would persist under almost any reasonable HIGH revision.

R2's combined picture: BTC is *near-boundary* on §11.6 (could be re-classified by small calibration adjustments); ETH is *structurally* cost-fragile (would not re-classify under realistic calibration revisions). Per Phase 2w §11.4 ETH-as-comparison, both symbols must clear; the ETH fragility alone is sufficient to FAIL the gate even if BTC's threshold-sensitivity were resolved favorably.

### 4.5 R2+R3 — fill-model sensitivity (informative for live realism)

Per Phase 2w §11.6 (the diagnostic-only limit-at-pullback intrabar fill model, run #10):

| Symbol | Δ expR (limit-at-pullback − next-bar-open) | Δ trades | Small divergence? |
|--------|-------------------------------------------:|---------:|:-:|
| BTCUSDT | **+0.2371** | small | **NO** |
| ETHUSDT | −0.0214 | small | **YES** |

**BTC fill-model divergence is LARGE.** The diagnostic-only limit-at-pullback fill (which would fill at the touch bar's pullback level intrabar at zero slippage) produces BTC expR ≈ −0.038 vs the committed next-bar-open path's −0.275 — a difference of +0.24 R per trade. Per Phase 2v Gate 2 clarification, the committed next-bar-open-after-confirmation fill model is the only path eligible for §10.3 governing evaluation; the diagnostic informs interpretation only.

**Implication for Phase 2y:** the BTC live-realism question is open. If actual Binance executions are closer to limit-at-pullback intrabar than to next-bar-open (which would require limit-order-routing capabilities the protocol does not currently use), R2's BTC edge would be substantially larger than the committed model captures. If actual Binance executions are closer to next-bar-open (which is what the protocol currently uses), the committed model is correct. The fill-model question is **separate from the slippage-tier-calibration question** but is part of the broader "is the framework's cost model appropriate?" audit.

### 4.6 Cross-cutting pattern across the family arc

A clear pattern emerges:

| Improvement axis | Cost-sensitivity | §11.6 verdict |
|------------------|------------------|---------------|
| Exit-machinery (R3) | cost-robust | clears |
| Setup-validity (R1a) | cost-monotone, narrow margin on BTC at HIGH | borderline (technically not evaluated under R2-era §11.6 gate definition; would likely fail BTC dimension) |
| Bias-validity (R1b-narrow) | cost-monotone, framework-clearing at HIGH | clears |
| Entry-lifecycle (R2) | cost-fragile (ETH disqualifies even at LOW) | FAILS |

**Exit-machinery improvements are cost-robust. Entry-axis improvements are cost-fragile.** This is consistent with the M1 mechanism reading: R3's improvement is structural (replacing a destructive trailing topology) and large enough to absorb cost variation; R2's improvement is geometric (smaller R-distance → larger payoff per ATR of follow-through) and operates at a magnitude comparable to realistic cost variation. The cost-sensitivity profile is informative about the *nature* of each candidate's edge, not just about whether the threshold is correctly calibrated.

---

## 5. External evidence requirements

What evidence would responsibly support a §11.6 revision? This is the operator-driven gathering work; Claude Code cannot collect this evidence within Phase 2y (no Binance API access, no credentials, no MCP tooling, no live order-book or trade-tick subscriptions).

### 5.1 What kinds of evidence matter

#### 5.1.1 Binance USDⓈ-M futures fee schedule

The committed `taker_fee_rate = 0.0005` (5 bps) is the standard taker tier without VIP volume discounts and without BNB-token-fee discount. Operator must verify:

- **Current Binance USDⓈ-M futures taker rate.** Standard tier as of evidence-gathering date.
- **Volume tier discounts.** VIP tiers can reduce taker rate to ~3.5 bps at higher volume; Prometheus's tiny-live initial volume is unlikely to qualify.
- **BNB-token-fee discount.** Holding BNB for fee payment provides ~10% discount; whether the operator intends to use this is a deployment-time decision.
- **Maker rate.** Currently unused by the strategy (all entries are market; protective stops are STOP_MARKET); becomes relevant only if a future variant uses limit orders (R2's diagnostic limit-at-pullback intrabar would require this).
- **Fee asymmetry.** Spot vs futures, USDⓈ-M vs COIN-M.

**Source:** Binance public futures fee documentation. ChatGPT can verify currency of the rate; operator confirms account-tier specifics.

#### 5.1.2 BTCUSDT-perp historical bid/ask spread distribution

Per-side slippage of 1 / 3 / 8 bps at LOW / MEDIUM / HIGH is a labeled tier; the underlying assumption is that these bracket realistic conditions. Operator should gather:

- **BTCUSDT-perp historical bid/ask spread distribution** (intraday + intraday × regime-conditional).
- **ETHUSDT-perp historical spread distribution** for the §11.4 comparison-symbol calibration.
- **Spread-width vs volatility regime correlation** (does spread widen during high-volatility bars where R2 candidates would fire?).

**Source:** Binance public market data + third-party microstructure providers (Kaiko, CryptoCompare, academic papers). Operator-driven; potentially ChatGPT-supplemented.

#### 5.1.3 BTCUSDT-perp depth and impact for typical Prometheus order sizes

The slippage tier interpretation depends on order size. At Prometheus-scale notional ($4K–$20K typical entries; up to ~$200K cap with 2× leverage and 10K equity), market-impact slippage is dominated by spread, not depth. As scale increases (operator's later sizing-equity choices), impact could become the dominant factor.

- **Order-book depth at typical Prometheus notionals** at BTCUSDT-perp top-of-book + first 5 levels.
- **Realized impact for market orders at those notionals** (does a $5K market order move the touch by 1 bp? 5 bps?).
- **ETHUSDT-perp depth comparison.**

**Source:** Binance public market-data + tick-level data. Operator-driven.

#### 5.1.4 Expected order-size distribution for Prometheus

Operator's planned tiny-live and scaled-live equity tiers determine the relevant notional range. At committed `risk_fraction = 0.0025` and `max_effective_leverage = 2.0`:

- 10K equity → notional up to ~$20K typical.
- 50K equity → notional up to ~$100K typical.
- 100K equity → notional up to ~$200K typical.

**Source:** Operator-driven (deployment-time decision).

#### 5.1.5 Market-vs-limit execution assumptions

The current cost model assumes 100% market-order execution for entries (next-bar-open per H0 / R3 / R1a / R1b-narrow / R2 committed path). The R2 diagnostic-only limit-at-pullback intrabar fill model showed BTC Δexp +0.24 R divergence — substantial. Operator should clarify:

- **Is limit-order routing realistic for Prometheus's planned execution architecture?** The current spec uses MARKET entries; switching would be a meaningful spec change with its own phase-gate evidence.
- **What fill-rate would limit orders achieve?** Intrabar limit fills require crossing the bid (or being filled passively); the assumption that 100% of pullback-bar limits would fill at the pullback level is the strongest assumption R2's diagnostic made.

**Source:** Operator decision + Binance API behavior documentation + microstructure research.

#### 5.1.6 Maker/taker behavior for protective stops

Protective stops are STOP_MARKET (per the v1 protective-stop spec, `closePosition=true / workingType=MARK_PRICE / priceProtect=TRUE`). When triggered, they fill at taker rate. The current cost model applies taker fee at exit consistently with this.

- **Verify Binance USDⓈ-M STOP_MARKET fill behavior** (taker fee; market price at trigger).
- **Verify priceProtect behavior** (which limits stop-trigger to within a band of mark price; reduces gap-through risk).

**Source:** Binance API documentation. Already partially verified by GAP-20260424-032 (mark-price stop-trigger reproducibility).

#### 5.1.7 Latency assumptions

The current cost model has no explicit latency component. For a strategy that fires at completed-15m-bar close and submits market orders for the next-15m-bar-open, the latency between bar close and order submission is implicit in the next-bar-open assumption.

- **Realized order-submission latency for Prometheus's planned NUC + Binance setup.** Sub-second is typical; multi-second latency would shift fills materially.
- **Whether next-bar-open fills are achievable in practice** (submitting at 15m bar close, receiving fill at next bar's open, accounting for clock-skew between exchange and host).

**Source:** Operator's pre-deployment paper/shadow phase (which is itself currently NOT authorized; this evidence-gathering would partially overlap with paper/shadow scope).

#### 5.1.8 ETH-vs-BTC differential slippage

The current cost model uses identical slippage tiers across BTC and ETH. ETH-perp typically has wider spreads and shallower depth than BTC-perp; differential tiering may be more accurate. R2's ETH disqualification at LOW slippage (Δexp_H0 −0.006) hints that ETH may sit in a different realistic-cost regime than BTC, but the internal evidence is consistent with multiple interpretations (genuine ETH strategy fragility OR ETH realistic costs higher than BTC).

- **ETHUSDT-perp vs BTCUSDT-perp historical spread differential.**
- **ETHUSDT-perp depth differential.**

**Source:** Same as §5.1.2, with ETH-specific data.

### 5.2 What Claude Code CANNOT do

Within Phase 2y's docs-only constraints:

- **Cannot fetch Binance public fee schedule.** No web fetching authorized; would require WebFetch / WebSearch tools or operator-provided data.
- **Cannot fetch historical BTCUSDT/ETHUSDT-perp tick data, order-book snapshots, or volume profile.** Requires Binance API access and credentials, neither of which is authorized.
- **Cannot run Kaiko / CryptoCompare / third-party data lookups.** Same restriction.
- **Cannot perform microstructure analysis on data not already in the repo.** The `data/` tree is git-ignored and contains only the v002 datasets (klines, mark-price, funding); no spread / depth / impact data exists in the repo.

### 5.3 What the operator (or ChatGPT in a separate session) must provide

If a future evidence-gathering phase is authorized, the following must be sourced externally:

1. **Current Binance USDⓈ-M taker / maker fee rates** (with operator's account tier confirmed).
2. **BTCUSDT-perp historical bid/ask spread distribution** (per-bar or per-tick aggregates over a representative window — at minimum, the R-window 2022-01-01 → 2025-01-01 to match the strategy backtest's economic regime).
3. **ETHUSDT-perp comparable spread distribution.**
4. **BTCUSDT-perp depth profile at top-of-book + first 5 levels** (over the same window; even quarterly snapshots would be informative).
5. **Realized market-order impact for $5K, $20K, $100K, $200K notionals at BTCUSDT-perp** (if available; this is a harder ask).
6. **Operator's planned equity tiers for tiny-live and scaled-live** (informs the relevant notional range).
7. **Whether the live execution architecture will use limit orders for entries** (informs the fill-model question).

This external evidence-gathering is **outside Phase 2y scope.** Phase 2y enumerates the requirements; a future operator-authorized phase (Phase 2z or later) would gather and analyze the evidence.

---

## 6. Three policy options

### Option (a) — Keep HIGH = 8 bps unchanged

The §11.6 threshold remains as committed in `config.py:55-59`. The cost model is unchanged. R2's FAILED verdict consolidates as a real strategy-fragility finding. Future candidates are evaluated under the same gate. The framework discipline anchor §11.3.5 is preserved as an explicit defense against threshold-rescue patterns.

### Option (b) — Lower HIGH only with external evidence

The §11.6 threshold is *not* changed in Phase 2y. A future operator-authorized phase (call it Phase 2z) would:

1. Gather the external evidence enumerated in §5.3 (operator-driven; ChatGPT-supported where appropriate).
2. Compute the empirically-grounded HIGH-slippage threshold from that evidence (e.g., 95th-percentile realized round-trip slippage at Prometheus-scale notional under volatile conditions).
3. Compare the empirical threshold to the current 8-bps HIGH.
4. If the empirical threshold is materially below 8 bps (say, 5 bps or 6 bps), recommend a §11.6 revision.
5. The revision applies to **future candidates evaluated under the revised gate**; whether it retroactively re-classifies R2's verdict is a separate operator policy decision.

Option (b) is conditional: the evidence-gathering phase decides whether to revise; the revision itself requires its own Gate 1 / Gate 2 / Gate 2 review structure.

### Option (c) — Tighten HIGH if current model is too lenient

Mirror-image of Option (b). The same external-evidence-gathering phase could produce evidence that 8 bps materially understates Binance's actual live conditions — in which case the HIGH threshold should be tightened, the §11.6 gate should be more stringent, and many already-PROMOTED candidates (including R3, R1a+R3, R1b-narrow) would need re-evaluation under the revised threshold.

---

## 7. Per-option evaluation

### 7.1 Option (a) — Keep HIGH = 8 bps unchanged

- **What it would mean for R2:** R2's FAILED — §11.6 cost-sensitivity blocks verdict consolidates. R2 stays retained as research evidence. The mechanism evidence (M1 + M3 PASS; M2 FAIL) is preserved as descriptive, not deployable. R2 is **not rehabilitated** by Phase 2y; nor by any future Phase 2z if the evidence-gathering phase confirms that 8 bps is correctly calibrated.
- **What it would mean for future candidates:** Same disciplined gate. Entry-axis structural redesigns with cost-fragile geometries continue to face the §11.6 hurdle. Candidates whose improvement is robust to cost variation (R3-style exit-machinery improvements) continue to clear cleanly.
- **Risk of post-hoc threshold loosening:** **ZERO.** Option (a) is the explicit defense against post-hoc loosening — by maintaining the threshold, it preserves the §11.3.5 binding rule.
- **Whether it preserves framework discipline:** **YES.** This is the disciplined path.

### 7.2 Option (b) — Lower HIGH only with external evidence

- **What it would mean for R2:** Phase 2y itself does NOT lower HIGH. A future Phase 2z evidence-gathering phase might. If Phase 2z produces evidence supporting a §11.6 revision to (say) 5–6 bps:
  - **For BTC:** R2+R3 BTC at HIGH slippage = 5 bps would produce expR somewhere between LOW (−0.180) and MED (−0.275) depending on linearity; likely Δexp_H0 stays positive. BTC dimension would clear at the revised HIGH.
  - **For ETH:** R2+R3 ETH disqualifies at LOW (Δexp_H0 −0.006). The ETH cost-fragility is structural, not threshold-driven; ETH would likely **still** disqualify under any reasonable HIGH revision.
  - **Combined:** §11.4 ETH-as-comparison would still block; R2 would still FAIL the combined verdict.
  - **Net for R2:** no realistic threshold revision rehabilitates R2's framework verdict, given ETH's structural cost-fragility.
- **What it would mean for future candidates:** The revised threshold becomes the gate. Future entry-axis candidates whose BTC fragility was at-the-threshold would clear; future candidates with structural ETH cost-fragility (analogous to R2's ETH) would still face the §11.4 block.
- **Risk of post-hoc threshold loosening:** **MODERATE if Phase 2z is invoked without rigorous external-evidence requirements; LOW if invoked with the §5.3 evidence requirements honored.** The risk is that the evidence-gathering phase becomes a "find evidence to support a revision we already want" phase rather than an honest calibration audit. The §11.3.5 binding rule must be preserved as an explicit constraint on Phase 2z's design (Phase 2z's recommendation must be evidence-driven, not candidate-driven).
- **Whether it preserves framework discipline:** **CONDITIONAL.** Preserved if the external-evidence requirement is rigorously honored; eroded if the evidence requirement is satisfied with low-quality data or with data that selectively supports a desired revision.

### 7.3 Option (c) — Tighten HIGH if current model is too lenient

- **What it would mean for R2:** Phase 2z evidence-gathering would also have to consider this branch. If evidence shows 8 bps **understates** actual costs (e.g., volatile-regime realized round-trip slippage frequently exceeds 16 bps), the HIGH threshold tightens (to e.g. 12 bps per side). R2 stays FAILED; the framework verdict is reinforced.
- **What it would mean for future candidates:** A more stringent gate. R3 might still clear at a tightened HIGH (its absolute improvement is large); R1a+R3 BTC dimension would more clearly fail; R1b-narrow's near-clearing margin becomes thinner.
- **What it would mean for already-PROMOTED candidates:** R3, R1a+R3, R1b-narrow's PROMOTE verdicts are not retroactively revised by Phase 2y. A future operator-policy phase could decide whether to re-evaluate them under the revised gate; that is a separate decision outside Phase 2y's scope.
- **Risk of post-hoc threshold loosening:** Option (c) is the *opposite* of loosening; the post-hoc-revision risk is symmetric — invoking Option (c) selectively to disqualify retroactively is also a discipline violation. The protection is the same: the revision must be evidence-driven.
- **Whether it preserves framework discipline:** **CONDITIONAL.** Same as Option (b).

### 7.4 Net comparison

| Option | R2 outcome | Future candidates | Loosening risk | Discipline | Recommended? |
|--------|-----------|-------------------|----------------|------------|--------------|
| (a) Keep unchanged | FAILED stands | Same gate | ZERO | PRESERVED | **PRIMARY** |
| (b) Lower with evidence | FAILED still stands (ETH structural) | Lower bar | LOW–MODERATE (conditional) | CONDITIONAL | Fallback only |
| (c) Tighten with evidence | FAILED reinforced | Higher bar | LOW–MODERATE (conditional) | CONDITIONAL | Not primary; possible if evidence supports |

**Critical observation:** Option (b) does NOT rehabilitate R2 even if the evidence supports lowering HIGH, because R2's ETH dimension is structurally cost-fragile (disqualifies at LOW). This means Option (b) is **not a vehicle for R2 rescue**; it is a framework-calibration question that happens to have an R2-failure trigger. This is exactly the right epistemic posture: the threshold-revision question is independent of R2's outcome.

---

## 8. Recommendation

This recommendation is **provisional and evidence-based, not definitive**. The operator decides.

### 8.1 Primary recommendation

**§11.6 should remain unchanged for now (Option (a)).**

Rationale:

1. **No internal evidence supports revision.** All available cost-sensitivity data (R3, R1a+R3, R1b-narrow, R2+R3) was generated under HIGH = 8 bps. Internal data shows what each candidate produces under that calibration; it cannot validate the calibration itself. Without external Binance-cost-realism evidence, any revision would be a §11.3.5 violation.
2. **The R2 §11.6 failure is informative regardless of calibration.** R2's ETH dimension disqualifies even at LOW slippage (Δexp_H0 −0.006) — this is a structural cost-fragility finding, not a threshold-calibration artifact. No realistic HIGH revision rehabilitates R2's combined framework verdict, given §11.4 ETH-as-comparison. R2 staying FAILED is the right outcome under either calibration.
3. **R3's cost-robustness is genuine evidence about exit-axis improvements.** R3 clears HIGH cleanly. R3's absolute improvement absorbs the HIGH-tier cost variation without crossing the disqualification floor. This is informative whether HIGH = 8 bps is correctly calibrated or not — R3's improvement is structurally large enough to be cost-robust regardless.
4. **The framework-discipline anchor §11.3.5 must be preserved.** Lowering HIGH because R2 fails at HIGH is exactly the post-hoc-loosening pattern the rule was designed to prevent. Even if Phase 2y framed the revision as "framework calibration", the temporal proximity to R2's failure would erode the discipline anchor. The disciplined response is: keep the threshold; treat R2's failure as a real finding; document the calibration question for a future evidence-driven phase if and when external evidence is gathered.

### 8.2 Recommended discipline for any future threshold revision

Any future threshold revision (whether tightening or loosening) should require **all** of:

1. **External evidence about Binance USDⓈ-M BTCUSDT-perp's actual round-trip slippage profile** at Prometheus-scale notional, gathered per §5.3 specifications.
2. **External evidence about Binance USDⓈ-M ETHUSDT-perp's comparable profile** (for §11.4 calibration).
3. **A separately-authorized phase** with its own Gate 1 / Gate 2 / Gate 2 review structure. The phase must explicitly forbid invoking the revision as a rescue of any specific candidate's verdict. The §11.3.5 binding rule applies verbatim.
4. **The revision applies to candidates evaluated under the revised gate going forward.** Whether previously-evaluated candidates (R3, R1a+R3, R1b-narrow, R2+R3) are retroactively re-classified is a separate operator-policy decision outside the threshold-revision phase.
5. **The revision must be a numerical update to `config.py:55-59`'s `DEFAULT_SLIPPAGE_BPS` map**, not a redefinition of the §11.6 gate's structural shape. The gate evaluates §10.3 disqualification at HIGH; the threshold value is parameterized, not the gate logic.

### 8.3 R2 should remain failed unless and until such evidence exists

R2's framework verdict is **FAILED — §11.6 cost-sensitivity blocks**, classified as retained research evidence per Phase 2w §16.3 + Phase 2x §3.5. Phase 2y does NOT rehabilitate R2.

If a future evidence-gathering phase produces evidence supporting a §11.6 revision:

- The revised gate applies to future candidates.
- R2's verdict can be re-evaluated under the revised gate **only by operator-authorized re-classification phase**, not by mechanical recomputation.
- The re-classification, if authorized, must consider:
  - Whether R2 clears under the revised gate (BTC plausibly yes; ETH structurally no).
  - Whether the revised gate's calibration is independent of R2's specific cost-sensitivity profile (i.e., the revision must be evidence-grounded, not R2-tuned).
  - Whether the operator's deployment scope still anchors on §1.7.3 (BTCUSDT-primary, ETHUSDT research/comparison) — if so, ETH's structural cost-fragility may not block deployment of an R2-style entry mechanism on BTC alone, depending on what the operator considers a deployable variant.
- The re-classification, even if it nominally clears R2 under a revised gate, does not by itself authorize R2 deployment; deployment authorization is a separate phase-gate decision.

### 8.4 What the recommendation explicitly does NOT recommend

- **No threshold change in Phase 2y.**
- **No R2 verdict revision in Phase 2y.**
- **No paper/shadow planning.** Operator restriction stands.
- **No Phase 4 (runtime / state / persistence) work.** Operator restriction stands.
- **No live-readiness or deployment work.** Operator restriction stands.
- **No exchange-write capability, no production keys, no MCP / Graphify, no `.mcp.json`, no credentials, no `data/` commits.**
- **No project-level lock change.** §1.7.3 (BTCUSDT-primary, ETHUSDT research/comparison only, one-position max, 0.25% risk, 2× leverage cap, mark-price stops, v002 datasets) preserved.
- **No fix to the Phase 2l / 2m / 2x text inconsistency about slippage values.** That correction belongs in a separate docs-only consistency-cleanup phase if the operator authorizes one.

### 8.5 What would change this recommendation

- **Operator independently authorizes Phase 2z evidence-gathering.** Recommendation Option (a) becomes "remain unchanged pending Phase 2z output". Phase 2z scope is operator-defined; Phase 2y enumerates the §5.3 evidence requirements as a starting point.
- **Operator independently provides external evidence about Binance USDⓈ-M slippage at Prometheus-scale notional.** Phase 2z's purpose is reduced; the threshold-revision question can be evaluated directly. Phase 2y still does not authorize the revision; a Phase 2z-equivalent decision is required.
- **Operator independently judges that the R2 §11.6 failure is sufficiently demotivating to authorize family-shift planning** (Phase 2x Option D). Phase 2y is informational input to that judgment; the family-shift authorization is a separate operator decision.

---

## 9. Explicit project-state preservation statement

Phase 2y **explicitly preserves** the following project state:

- **No threshold is changed.** `config.py:55-59` `DEFAULT_SLIPPAGE_BPS` map (LOW = 1.0 / MEDIUM = 3.0 / HIGH = 8.0 bps per side) preserved verbatim. Phase 2f §10.3 / §10.4 / §11.3 / §11.4 / **§11.6** thresholds preserved verbatim per §11.3.5. `taker_fee_rate = 0.0005` preserved.
- **No R2 verdict is revised.** R2's framework verdict remains **FAILED — §11.6 cost-sensitivity blocks** per Phase 2w §16.1. R2 remains retained research evidence per Phase 2w §16.3.
- **R3 remains baseline-of-record** per Phase 2p §C.1. Locked sub-parameters (`exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`) preserved.
- **R2 remains retained research evidence.** Not deployable; not the current default; M1 + M3 mechanism evidence preserved as descriptive.
- **R1a (volatility-percentile setup predicate) remains retained research evidence.** Phase 2p §D framing preserved.
- **R1b-narrow (bias-strength magnitude predicate) remains retained research evidence.** Phase 2s §13 framing preserved.
- **H0 remains framework anchor.** Phase 2i §1.7.3 sole §10.3 / §10.4 anchor preserved.
- **No paper/shadow planning is authorized.** Phase 2p §F.2 / post-Phase-2w / Phase 2x §6 deferrals stand.
- **No Phase 4 (runtime / state / persistence) is authorized.** Phase 2p §F.3 / post-Phase-2w / Phase 2x §6 deferrals stand.
- **No live-readiness work, no deployment work, no exchange-write capability, no production keys, no MCP / Graphify, no credentials.**
- **No project-level locks change.** §1.7.3 preserved verbatim.
- **No `data/` commits.**
- **No code change.** No file in `src/`, `tests/`, or `scripts/` is touched by Phase 2y.
- **No spec change.** v1-breakout-strategy-spec.md, validation-checklist, cost-modeling, backtesting-principles, phase-gates, technical-debt-register all preserved.
- **No documentation correction.** The Phase 2l / 2m / 2x slippage-value text inconsistency (flagged in §2.6) is documented for operator awareness; correction is outside Phase 2y scope.

---

## 10. GO / NO-GO recommendation

**GO** for **Option (a) — keep §11.6 = 8 bps HIGH unchanged.** Recommended primary. Aligns with the framework discipline anchor §11.3.5 (no post-hoc loosening). No internal evidence supports revision; external evidence has not been gathered; R2's failure is informative whether the threshold is correctly calibrated or not. Phase 2y closes with the threshold preserved.

**GO (provisional, conditional on operator authorization)** for a **future Phase 2z external-evidence-gathering phase** if and when the operator independently judges that the framework-calibration question is worth resolving. Phase 2z would gather the §5.3 external evidence (Binance fee schedule, BTCUSDT-perp historical spread / depth profile, ETHUSDT-perp comparison, expected order-size distribution, market-vs-limit execution assumptions, latency assumptions, ETH-vs-BTC differential) and produce a recommendation about whether §11.6 should be revised. Phase 2z is **not authorized by Phase 2y**; it is a fallback path.

**NO-GO** for **any threshold revision in Phase 2y itself.** §11.6 = 8 bps HIGH stays. §10.3 / §10.4 / §11.3 / §11.4 thresholds also unchanged. The §11.3.5 binding rule is preserved verbatim.

**NO-GO** for **any R2 verdict revision in Phase 2y.** R2 stays FAILED — §11.6 cost-sensitivity blocks. R2 stays retained research evidence. Even if a future Phase 2z produces evidence supporting a §11.6 revision, R2 is **not** automatically rehabilitated — the ETH structural cost-fragility (disqualifies at LOW slippage) remains regardless of HIGH-threshold calibration; §11.4 ETH-as-comparison continues to block.

**NO-GO** for **paper/shadow planning, Phase 4 (runtime / state / persistence), live-readiness, deployment, exchange-write capability, production keys, MCP / Graphify activation, credentials, and `data/` commits.** All Phase 2x-affirmed restrictions stand.

The recommended next operator decision is one of:

1. **Accept Phase 2y's primary recommendation.** §11.6 stays at 8 bps. R2 stays FAILED. Project remains in the post-Phase-2x consolidated pause state.
2. **Authorize Phase 2z external-evidence-gathering.** Operator-driven evidence-collection per §5.3 specifications. Phase 2z is docs-only / data-only; no code changes; no threshold changes (Phase 2z produces a recommendation, not a revision). Phase 2y does not pre-authorize Phase 2z.
3. **Treat Phase 2y as completing the Option C exploration the Phase 2x family-review memo recommended as fallback.** With Option C completed and producing a "remain unchanged" recommendation, the operator can choose between (i) staying paused indefinitely (Phase 2x Option A), (ii) authorizing new strategy-family planning (Phase 2x Option D), or (iii) authorizing Phase 2z.

---

**End of Phase 2y slippage / cost-policy review memo.** Sections 1–10 complete. **Recommendation: §11.6 = 8 bps HIGH stays unchanged.** R2 stays FAILED. R3 remains baseline-of-record. H0 remains framework anchor. Framework discipline §11.3.5 preserved verbatim. Future threshold revision (if ever) requires external evidence per §5.3 and a separately-authorized phase. No threshold changed; no R2 verdict revised; no paper/shadow / Phase 4 / live-readiness / deployment / project-lock change. **NO-GO for any threshold revision in Phase 2y itself; GO for keeping the framework unchanged.** Documentation inconsistency about slippage values in Phase 2l / 2m / 2x text flagged for future docs-only consistency cleanup, out of Phase 2y scope. Awaiting operator review.
