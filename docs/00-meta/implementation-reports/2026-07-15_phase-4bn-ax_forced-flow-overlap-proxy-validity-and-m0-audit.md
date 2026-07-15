# Phase 4bn-AX — Forced-Flow / Liquidation-Asymmetry Overlap, Proxy-Validity, and M0 Audit

This is the dedicated companion audit to the Phase 4bn-AX main decision memo
(`2026-07-15_phase-4bn-ax_post-fable-candidate-selection-cf1-decision-consequence-forced-flow-overlap-audit.md`).
It adjudicates, on committed repository evidence only, the single omitted family Fable
proposed after the bounded post-phase review: **liquidation-cascade / forced-flow asymmetry
using trade-tape signatures only**. It reads no data, opens no reserve, designs no event
rule or threshold, and authorizes nothing. It exists to determine whether the family is a
genuinely distinct, mechanism-driven event-study family or a rescue-shaped relabeling of
work the committed record has already tested, stopped, cooled down, or rejected.

## 1. Proposed family identity

`Liquidation-cascade / forced-flow asymmetry using trade-tape signatures only.` Proposed by
Fable in the operator-supplied, post-phase, bounded, advisory, non-binding review recorded in
the Phase 4bn-AW merge-closeout §30–§31. It is **not** part of the AW shortlist (CF-1, CF-2,
CF-3), is not selected by AW or Fable, and by the AW merge-closeout's own words "has not passed
repository-grounded overlap, proxy-validity, M0, cooled-down-family, or rescue review." This
audit is that review.

## 2. Mechanism claim

The proposed mechanism (restated from AW merge-closeout §30, not adopted): liquidation cascades
on a leveraged venue create **mechanically forced** sellers (long liquidations) or buyers
(short liquidations); a forced participant transacts on urgency, not information; bursts of
**one-sided, size-clustered aggressor flow** may therefore proxy forced liquidation; forced flow
may **overshoot** and then **partially revert**; a predeclared forced-flow event may be followed
by a conditional, mechanism-based directional drift measurable on existing BTCUSDT aggTrades.

## 3. Observable proxy claim

The proxy is, precisely: a trailing-window signature of aggressor-side flow that is
simultaneously (a) strongly one-sided (buy-vs-sell aggressor imbalance far from balance),
(b) size-clustered (elevated per-trade quantity and/or total quantity), and (c) bursty
(elevated trade arrival count) — with the forced-flow *event* declared when that signature
crosses some threshold, and the *response* measured as forward directional drift (overshoot /
partial reversion) over some horizon. **No claim in this audit is that the proxy identifies
actual liquidations**; the audit's central question is whether that proxy can be defended at
all under committed data and governance.

## 4. Available committed data

BTCUSDT USDⓈ-M **aggTrades** are the only admissible non-reserve substrate for this family
(pre-v002 2024-03-01…2024-11-30, ~400M rows; already normalized/feature/label built per Phase
4bn-AB §6). The committed aggTrades **feature substrate** already computes, per trailing window
1s / 5s / 15s / 60s (source: `src/prometheus/research/microstructure/features_schema.py`
`PER_WINDOW_FEATURE_TEMPLATES`, the finalized Phase 4bh-B / v002 45-column set):

| Existing committed feature (per window) | What it measures |
|---|---|
| `rolling_aggtrade_count_{w}` | trade-arrival burst / activity intensity |
| `rolling_quantity_sum_{w}` | total traded quantity (size) |
| `rolling_quantity_mean_{w}` | mean per-trade size (size clustering) |
| `rolling_aggressive_buy_quantity_{w}` | one-sided aggressor **buy** volume |
| `rolling_aggressive_sell_quantity_{w}` | one-sided aggressor **sell** volume |
| `rolling_aggressive_buy_count_{w}` | one-sided aggressor **buy** trade count |
| `rolling_aggressive_sell_count_{w}` | one-sided aggressor **sell** trade count |
| `rolling_aggressive_flow_ratio_{w}` | aggressor-flow **imbalance ratio** (OFI) |
| `rolling_aggressive_quantity_imbalance_{w}` | signed aggressor **quantity imbalance** |
| `rolling_log_return_past_window_{w}` | trailing return (overshoot context) |

The forced-flow proxy in §3 is, term for term, a threshold applied to features that **already
exist and were already computed** on this substrate. One-sidedness = `rolling_aggressive_flow_ratio`
/ `rolling_aggressive_quantity_imbalance`; size-clustering = `rolling_quantity_mean` /
`rolling_quantity_sum`; burstiness = `rolling_aggtrade_count`. The committed targets are the
per-horizon `forward_direction_<H>` / `forward_log_return_<H>` labels (Phase 4bn-AB §12). The
proposed "conditional directional drift after a forced-flow event" is therefore the **same
directional target family** already tested in the stopped ML arc, conditioned on a threshold
over already-tested aggressor/burst features.

## 5. Missing official liquidation data

No official liquidation feed is present in committed available data. The Binance USDⓈ-M
**forceOrder** (liquidation) stream is **WS-live-capture only, with no historical archive**;
retrospectively it is INADMISSIBLE and prospective capture is regime-non-comparable (AW screening
memo §11 "Inadmissible or blocking" row; AW screening §15 rejected-candidate #4
"Liquidation-cascade proxy — proxy-only, no history, WS-only"). The committed feature schema
independently confirms the project has **deliberately excluded** liquidation identity from the
substrate: `FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS` bars the literal token `liquidation` (also
`funding`, `open_interest`, `order_book`, `mark_price`) from any feature column, and the schema
docstring states it "does NOT compute … any … order-flow proxy" as an identified liquidation
object. There is **no committed marker, flag, label, or field that identifies a liquidation
event** anywhere in the admissible data. Any "forced-flow" event is therefore an **unverifiable
inference** from ordinary trade-tape aggressor flow.

## 6. Prior feature / family overlap table

| Prior committed work | What it measured | Target used | Mechanism claimed | Does forced-flow materially differ? | Difference observable in committed data? | Difference only a new label on the same proxy? |
|---|---|---|---|---|---|---|
| Stopped long-horizon ML arc (4bn-AH…AS) | 45 causal aggTrades features incl. aggressor imbalance, flow ratio, burst count, size | `forward_direction_<H>` (sign) | short-horizon directional information in order flow | **No** — same features, same directional target, plus an event gate | N/A (no new observable) | **Yes** — a threshold + relabel over the same proxy |
| Trade-burst / activity (M-6), AW cand. #11 | trade-arrival intensity | magnitude/direction | liquidity-demand bursts | Partly (adds one-sidedness) but AW merged this into CF-1 | one-sidedness observable, "forced" not | Largely yes |
| Generic order-flow imbalance (M-2/3/4/7/8), AW cand. #3 | aggressor buy/sell imbalance | direction | order-flow pressure | **No** — forced-flow *is* OFI + a size/burst filter | imbalance observable, "forced" not | **Yes** |
| Liquidation-cascade proxy (M-9), AW cand. #4 | same trade-tape proxy | direction | forced-flow overshoot/reversion | **No** — identical family, already REJECTED by AW | forceOrder not in data | **Yes** — identical |
| Price-only continuation (§7.A DEPLETED) | price only | direction | continuation | Different features, same directional endpoint | — | — |
| D1-A funding-aware contrarian (§7.C) | funding/positioning | direction | crowded-positioning reversion | Different signal source; same reversion intuition | — | — |

The table's load-bearing rows all resolve the same way: the forced-flow family shares the stopped
directional ML arc's target, is a size/burst-filtered special case of generic order-flow imbalance,
and is identical to AW's already-rejected liquidation-cascade proxy candidate #4.

## 7. Generic order-flow-imbalance overlap

**High / near-total.** The forced-flow proxy's one-sidedness component *is* aggressor-flow
imbalance, already materialized as `rolling_aggressive_flow_ratio_{w}` and
`rolling_aggressive_quantity_imbalance_{w}` across four windows and already fed to the stopped
directional baselines. Forced-flow adds only a magnitude threshold and a size/burst co-condition;
it does not introduce a new observable. Under M0 §7.D (microstructure / order-flow / liquidity-
timing lane, `NOT_RECOMMENDED_NOW`) this is the exact lane flagged as not strengthened by any prior
Prometheus finding.

## 8. Trade-burst / activity overlap

**High.** The burstiness component is `rolling_aggtrade_count_{w}`; the size-clustering component
is `rolling_quantity_mean_{w}` / `rolling_quantity_sum_{w}`. AW candidate #11 (trade-burst /
activity prediction, M-6) was explicitly **merged into CF-1** as the same magnitude family with
low standalone decision consequence (AW screening §15). Reusing burst/size intensity as a
directional event trigger does not escape that disposition; it re-points the same intensity
features at the depleted directional target.

## 9. Continuation / reversion overlap

**High and self-conflicting.** The mechanism asserts overshoot (continuation of forced pressure)
**and** partial reversion — i.e. it spans both short-horizon continuation and short-horizon
reversion depending on the (unspecified) horizon. Short-horizon directional continuation is
DEPLETED (§7.A: R2/F1/V2/G1/C1 + Phase 4af's 80-cell persistence null). Reversion-after-
overextension is the F1 family (catastrophic-floor rejection). A family whose predicted sign
flips with an unfixed horizon can be made to "match" either prior rejection post hoc, which is a
multiple-testing and anti-rescue red flag rather than a distinguishing feature.

## 10. Stopped ML arc overlap

**Decisive.** `STOP_LONGHORIZON_ML_ARC` (Phase 4bn-AS) stopped the aggTrades directional program
on evidence-and-methodology grounds: clean 15s directional information but only ~2.47% of 15s
moves clear 16 bps, inversion at 5m/30m/1h, and a consumed internal holdout. The forced-flow
family predicts a **directional** drift (`forward_direction`/`forward_log_return`) from the **same
aggressor/burst feature substrate** the stopped arc already exhausted. Conditioning on a forced-
flow threshold is precisely a "rerun the same directional target with a new proxy / threshold /
name" move, which the phase mandate and M0.10/M0.12 forbid. The stop must not be reinterpreted as
an invitation to reopen it under an event-study label.

## 11. Cooled-down-family overlap

The family collides with two current M0 §7 entries: **§7.D** microstructure / order-flow /
liquidity-timing (`NOT_RECOMMENDED_NOW` — heavy data burden, high short-horizon cost-realism risk,
not strengthened by any prior finding) and, through its directional target, **§7.A** price-only /
directional continuation depletion is adjacent. It also duplicates AW's own rejected candidate #4
(liquidation-cascade proxy). Under §6 the cooldown is a **family-level** bar; reopening requires a
**materially new mechanism source derived from external theory/evidence, not from the failed
phase's forensics**. Forced-flow supplies no materially new *observable* — it re-thresholds
existing features — so §6.A is not satisfied.

## 12. News / informed-flow / inventory confounds

Even granting the mechanism conceptually, one-sided size-clustered aggressor bursts are produced
by many non-liquidation processes that the trade tape cannot separate: **informed trading** (a
large informed buyer sweeps aggressively), **news response** (a macro print triggers one-sided
urgency), **ordinary inventory liquidation** (a market-maker or fund unwinding non-forcibly), and
**momentum / herding** (aggressors piling into a move). With aggTrades alone there is **no
observable that isolates *forced* (margin-call-driven) flow** from these confounds — no liquidation
flag, no account/margin state, no order-book depletion signature. The asserted mechanism cannot be
separated from news, informed trading, momentum, or inventory effects **even conceptually** on this
data, which is the phase's explicit kill condition.

## 13. Temporal-ordering assessment

The proxy features are causal/trailing by construction (`LEAKAGE_POLICY = causal_only_no_future_
lookahead`; window `(T - w, T]`), and the response labels are strictly forward, so a *mechanical*
temporal ordering (event at T → drift after T) is available and leakage-controlled. Temporal
ordering is therefore the one dimension the family passes. It is **not sufficient**: a well-ordered
event whose *identity* (forced vs. informed vs. news) is unobservable still fails identifiability.

## 14. Proxy-validity assessment

**FAIL.** (a) Existing aggTrades **cannot** identify forced liquidation specifically. (b) **No**
official liquidation marker is present in committed admissible data (forceOrder WS-only, no
history; `liquidation` column forbidden). (c) One-sided, size-clustered aggressor flow **cannot**
distinguish forced liquidation from ordinary informed/news/momentum/inventory flow. (d) The
mechanism "remains meaningful without claiming the proxy literally identifies liquidations" **only
by collapsing into generic order-flow-imbalance / trade-burst directional prediction** — which is
already tested (stopped arc) and cooled down (§7.D). The proxy is therefore either invalid (if it
claims to identify liquidations) or redundant (if it does not).

## 15. Source-admissibility assessment

**FAIL for the asserted mechanism; only the redundant reduction is admissible.** The data required
to *validate* a forced-liquidation proxy (forceOrder, or margin/account state) is inadmissible
retrospectively (WS-only, no archive) and unauthorized to acquire. The AW screening already
rejected the liquidation-cascade proxy on exactly this ground (§15 #4). Admissible aggTrades
support **only** generic order-flow imbalance, which is not the proposed family.

## 16. Researcher-freedom assessment

**High / adverse.** A tradeable forced-flow event requires inventing, with no external anchor: an
one-sidedness cutoff, a size-clustering cutoff, a burst cutoff, the window over which each is
measured (1s/5s/15s/60s or composites), an overshoot vs. reversion decision, a drift horizon, and
a drift-sign convention. Each is a free parameter; the mechanism gives no principled value for any
of them (unlike CF-1's HAR-RV baseline or CF-3's fixed UTC calendar). This is a large garden of
forking paths.

## 17. Multiple-testing assessment

**High risk.** The free-parameter surface in §16 multiplied across four windows and multiple
horizons is a classic multiple-comparisons hazard, aggravated by the continuation/reversion sign
ambiguity (§9) that lets almost any post-hoc result be narrated as "overshoot" or "reversion." A
bounded preregistration would have to fix every knob ex ante; nothing in committed theory or
evidence tells it where to fix them, so the pre-registration would be arbitrary rather than
principled.

## 18. Economic-materiality assessment under 16 bps

**Adverse.** The family's consequence is directional and must clear the locked 8 bps/side · 16 bps
round-trip frame. The stopped arc already measured that only ~2.47% of 15s moves (1.20% holdout)
exceed 16 bps and the median |15s move| is ~2.53 bps (Phase 4bn-AJ via AK §11/§15). Conditional
drift after a rare event inherits this thinness with a *smaller* sample (events are, by
definition, infrequent), worsening both economic materiality and opportunity-rate (M0.6). There is
no committed evidence that forced-flow-conditioned moves are systematically larger than the
already-thin unconditional short-horizon moves.

## 19. M0 clause-by-clause assessment

- **M0.1 mechanism source** — order-flow / microstructure; falls in §7.D. Directional target
  overlaps depleted lanes. **Adverse.**
- **M0.2 non-price-only / structurally distinct** — non-price-only, but **not structurally
  distinct**: it is a threshold + relabel over existing aggressor/burst features feeding the
  depleted directional target. **FAIL.**
- **M0.3 baseline-superiority theory** — no predeclared Δ_R derivable without inventing the event
  definition; the theory ("forced flow overshoots/reverts") predicts no committed effect size.
  **WEAK.**
- **M0.4 rejection-topology distance** — closest traps: F1 (reversion-after-overextension) and the
  §7.A directional depletion; the family cannot articulate structural distance because it shares
  their directional endpoint and can mimic either sign. **FAIL.**
- **M0.5 cost realism (16 bps)** — inherits the stopped arc's demonstrated short-horizon thinness;
  conditional-drift edge is not shown to clear 16 bps. **Adverse.**
- **M0.6 opportunity rate** — rare events → low trade count per window; no theory-derived arrival
  floor. **Adverse.**
- **M0.7 edge rate** — no predeclarable baseline differential without event tuning. **WEAK.**
- **M0.8 data availability/integrity** — forceOrder (needed to validate "forced") is **blocking**
  (WS-only, no history); aggTrades support only generic OFI. **FAIL.**
- **M0.9 governance compatibility** — must stay non-directional to avoid depleted lanes, but the
  family is explicitly directional; tension with §7.A/§7.C posture. **Adverse.**
- **M0.10 forbidden-rescue / anti-reduction** — reduces to generic order-flow imbalance and to the
  stopped short-horizon directional arc, and duplicates AW rejected candidate #4. **FAIL.**
- **M0.11 pre-backtest falsification** — a family whose sign can be re-narrated (overshoot vs.
  reversion) resists a clean pre-declared kill. **WEAK/FAIL.**
- **M0.12 cooldown / non-authorization** — touches cooled-down §7.D (and adjacent §7.A); §6.A
  "materially new mechanism source" **not satisfied** (no new observable; re-thresholding existing
  features off the failed substrate). **FAIL.**

## 20. Anti-rescue conclusion

The family is **rescue-shaped**. It reopens the stopped directional aggTrades program by applying a
new event threshold and a new name ("forced flow" / "liquidation cascade") to the same aggressor/
burst features and the same directional target, on a substrate whose directional signal was already
found economically thin and was stopped. It is simultaneously a relabeling of generic order-flow
imbalance and a duplicate of AW's already-rejected liquidation-cascade proxy. It fails the anti-
rescue test.

## 21. Whether the family is genuinely distinct

**Not genuinely distinct.** On committed data it is not separable from generic order-flow imbalance,
trade-burst activity, informed trading, news response, momentum, or inventory unwinding, and it
shares the stopped ML arc's directional target. Its only genuinely distinct claim — that the proxy
identifies *forced* (margin-driven) flow — is exactly the claim committed data cannot support.

## 22. Whether it is eligible for later preregistration

**Not eligible.** It fails proxy-validity (§14), source-admissibility (§15), M0.2 / M0.4 / M0.8 /
M0.10 / M0.12 (§19), and the anti-rescue test (§20); it carries high researcher-freedom (§16) and
multiple-testing risk (§17); and its economic consequence under 16 bps is adverse (§18). No bounded,
low-freedom, mechanism-faithful preregistration can be constructed from the committed record.

## 23. Exact reason for acceptance, rejection, or deferral

**REJECTED (not selected, not deferred-with-a-path).** Decisive reasons, any one sufficient:
(1) forced-liquidation identification is **necessary to the asserted mechanism but unavailable** in
committed admissible data (no forceOrder history, no liquidation marker); (2) admissible aggTrades
support **only generic order-flow imbalance**, which is cooled down (§7.D) and already materialized
as existing features; (3) the proxy **cannot distinguish** forced flow from informed/news/momentum/
inventory confounds even conceptually; (4) the family **materially duplicates the stopped
directional ML arc** and AW's rejected candidate #4, failing anti-rescue (M0.10/M0.12); (5) the
event definition demands an **open-ended threshold search** (high researcher-freedom / multiple
testing). This is a proxy/mechanism-mismatch scientific inadmissibility, not a fixable data gap that
acquisition would cure — and no acquisition is authorized in any case.

## 24. Confirmation no event definition or threshold was designed

Confirmed. This audit designed **no** event rule, **no** threshold, **no** window choice, **no**
drift horizon, **no** metric, and **no** sign convention. It described the *space* of choices the
family would require only to demonstrate the researcher-freedom and identifiability problems; it
selected none of them.

## 25. Confirmation no data was opened

Confirmed. No feature/label/normalized/raw row, no v002 terminal window, no v002 sealed test, and
nothing under `data/microstructure/` or `data/research/` was opened, read, listed for content,
hashed, sampled, or scored. `test_rows_loaded = 0` posture preserved. All evidence is from committed
Markdown reports and committed source constants (`features_schema.py`, `features_schema_v002.py`)
plus Git metadata. No network, endpoint, credential, or external reviewer was used.
