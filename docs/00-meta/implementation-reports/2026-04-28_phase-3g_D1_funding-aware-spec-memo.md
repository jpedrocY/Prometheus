# Phase 3g — D1 Funding-Aware Directional / Carry-Aware Strategy Spec Memo

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; **no post-hoc loosening per §11.3.5**); Phase 2i §1.7.3 project-level locks (H0 anchor; BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets); Phase 2j memo §C / §D (R1a setup-validity; R3 exit philosophy; §C.6 single-spec discipline); Phase 2p consolidation memo §C.1 (R3 baseline-of-record); Phase 2x family-review memo (V1 breakout family at useful ceiling); Phase 2y slippage / cost-policy review (§11.6 = 8 bps HIGH per side preserved verbatim; Option (a) closeout); Phase 3a new-strategy-family discovery memo §4.6 / §5 / §6.2 (F6 funding-aware ranked rank-2 near-term family candidate); Phase 3b F1 spec memo §§ 1–15 (binding spec template precedent); Phase 3c F1 execution-planning memo §§ 1–13 with operator-mandated amendments; Phase 3d-A / 3d-B1 / 3d-B2 reports (F1 HARD REJECT; Phase 3d-B2 terminal for F1); Phase 3e post-F1 research consolidation memo (remain-paused recommendation; F1-prime forbidden); Phase 3f next research-direction discovery memo (D1 ranked rank-1 active path); Phase 3f closeout / merge reports; `docs/03-strategy-research/v1-breakout-strategy-spec.md`; `docs/05-backtesting-validation/backtesting-principles.md`; `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`; `docs/05-backtesting-validation/cost-modeling.md`; `docs/04-data/data-requirements.md`; `docs/04-data/dataset-versioning.md`; `.claude/rules/prometheus-core.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/implementation-ambiguity-log.md`.

**Phase:** 3g — Docs-only **D1 funding-aware directional / carry-aware strategy specification memo.** Phase-3b-style: produces a binding strategy-family spec for the D1 funding-aware family. **Specification-only**, not strategy-execution, not backtesting, not parameter search, not paper/shadow, not Phase 4, not live-readiness, not deployment.

**Branch:** `phase-3g/d1-funding-aware-spec`. **Memo date:** 2026-04-28 UTC.

**Status:** Spec drafted. **No code change. No backtest. No variant created. No parameter tuned. No threshold changed. No project-level lock changed. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write proposal.** R3 remains V1-breakout baseline-of-record. H0 remains framework anchor. R1a / R1b-narrow / R2 / F1 remain retained research evidence. F1 framework verdict HARD REJECT. Phase 3d-B2 terminal for F1. §11.6 = 8 bps HIGH per side preserved verbatim. §1.7.3 project-level locks preserved verbatim. Spec is **provisional and falsifiable; the hypothesis may fail at first execution and the project must be prepared for that outcome**.

---

## 1. Plain-English explanation of what Phase 3g is deciding

Phase 3g produces a binding, falsifiable, single-spec specification for the D1 funding-aware directional / carry-aware strategy family. Phase 3g is the analogue of Phase 3b (the F1 spec memo) for the D1 family that Phase 3f recommended as rank-1 active path.

What Phase 3g produces:

- A market hypothesis statement with falsifiable mechanism predictions (M1 / M2 / M3).
- A binding strategy-family definition: one committed conceptual rule per axis (signal definition; entry direction; entry timing; stop; target; time-stop; cooldown; admissibility; funding-accrual handling; regime filter).
- Non-fitting rationale for every chosen rule.
- Required-data confirmation (v002 sufficiency check; derived-feature dataset identification).
- Backtester / engine implications (what new strategy module would be required if a downstream Phase 3h-equivalent execution-planning phase is later authorized).
- A first-execution gate definition (the §10.3-equivalent / §10.4-equivalent / §11.6-equivalent thresholds D1 must meet).
- An overfitting-risk analysis with the binding rules that prevent post-hoc threshold rescue.
- A GO / NO-GO decision for any future Phase 3h execution-planning memo.

What Phase 3g does **not** decide:

- Not deciding whether to implement D1 (separate Phase 3h-equivalent or implementation phase required).
- Not deciding whether to run any backtest (forbidden by Phase 3g operator brief).
- Not deciding whether to begin paper/shadow, Phase 4, live-readiness, or deployment work (forbidden by operator policy).
- Not deciding whether to lift any §1.7.3 project-level lock.
- Not deciding whether to revise any Phase 2f threshold (Phase 2y closed this; preserved through Phase 3e and Phase 3f).
- Not authorizing F1-prime, F1-target-subset, R1a-prime, R1b-prime, R2-prime, or any retroactive V1-family rescue (forbidden by Phase 3e §8.6 + Phase 3f §5.7).

Phase 3g produces a memo. The operator decides whether to authorize a downstream Phase 3h execution-planning phase or whether to remain paused at the post-Phase-3g spec boundary.

---

## 2. Current canonical project state

| Item | State |
|------|-------|
| **R3 (Phase 2j memo §D — Fixed-R + 8-bar time-stop, no trailing)** | **V1 breakout baseline-of-record** per Phase 2p §C.1; locked sub-parameters `exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`; same-bar priority STOP > TAKE_PROFIT > TIME_STOP; protective stop never moved intra-trade. |
| **H0 (Phase 2e locked baseline)** | **V1 breakout framework anchor** per Phase 2i §1.7.3. |
| **R1a / R1b-narrow / R2 / F1** | Retained as **research evidence only**. R2 framework FAILED — §11.6 cost-sensitivity blocks. F1 framework verdict HARD REJECT (Phase 3c §7.3 catastrophic-floor predicate; 5 violations across BTC/ETH × MED/HIGH cells). Phase 3d-B2 terminal for F1. |
| **§1.7.3 project-level locks** | **Preserved verbatim:** BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; one active protective stop max; 0.25% risk per trade; 2× leverage cap; mark-price stops; v002 datasets; one-way mode; isolated margin; no pyramiding; no reversal while positioned; no hedge mode. |
| **Phase 2f thresholds** | **Preserved verbatim:** §10.3.a Δexp ≥ +0.10 R; §10.3.c |maxDD| ratio < 1.5×; §10.4 absolute floors expR > −0.50 AND PF > 0.30; §11.3 V-window no-peeking; §11.4 ETH non-catastrophic; **§11.6 = 8 bps HIGH per side** (Phase 2y closeout). |
| **Paper/shadow planning** | **Not authorized.** Operator policy continues to defer paper/shadow indefinitely. |
| **Phase 4 (runtime / state / persistence) work** | **Not authorized.** |
| **Live-readiness / deployment / production-key / exchange-write work** | **Not authorized.** |
| **MCP / Graphify / `.mcp.json`** | **Not activated, not touched.** |
| **Credentials / `.env` / API keys** | **Not requested, not created, not used.** |

The Phase 3e remain-paused recommendation governs the project's broader posture; Phase 3f authorized one further docs-only direction-discovery; Phase 3g operates within both as the next-step spec memo for the recommended direction.

---

## 3. Why D1 is justified

### 3.1 Phase 3f D1 ranking summary

Phase 3f §8.1 ranked D1 (funding-aware directional / carry-aware) as the rank-1 active docs-only candidate among eight enumerated research directions. The ranking was based on cleanest §5-constraint compliance:

- **§5.1 frequency-vs-edge:** D1's episodic frequency (funding extremes occur ~5–15× per month per symbol per Phase 3a §4.6(f)) avoids F1's catastrophic frequency × per-trade-loss aggregation (F1 fired ~150× more trades than V1 baseline; per-trade negative expR multiplied to total return ≤ −440% on $10K starting equity).
- **§5.2 cost-resilience:** D1 has the lowest expected cost-sensitivity profile among candidates (Phase 3a §4.6(g)). The carry component is a known cost-stack item that can become a benefit when actively harvested.
- **§5.4 BTCUSDT-primary:** BTC funding is more liquid / larger volume / more reliable than ETH funding (Phase 3a §4.6(h)); §1.7.3 BTCUSDT-primary alignment is natural.
- **§5.5 v002 sufficiency:** D1 uniquely leverages v002 funding-rate data not yet exploited as primary signal (V1 breakout used funding only as cost-component; F1 used funding only as cost-component).
- **§5.6 falsifiability:** D1 has falsifiable directional and mechanism predictions (this memo's M1 / M2 / M3 below).
- **§5.7 not a disguised rescue:** D1 is not a V1-breakout setup-axis variant (different mechanism class entirely — funding-derived signal, not price-derived setup). D1 is not an F1-target-subset rescue (different signal source; different target; different exit; different family).

### 3.2 Why funding is a distinct information source

Funding rates on Binance USDⓈ-M perpetuals are **a structurally separate information channel from price action.** Three reasons funding is informationally distinct from V1 breakout / F1 mean-reversion price-derived signals:

1. **Mechanism origin.** Funding rates are determined by the perpetual-vs-mark-price spread maintenance mechanism, not by 15m price-action features (range-width, ATR percentile, displacement-over-ATR). A funding extreme reflects sustained leveraged positioning imbalance — an aggregate market-participant behavior fact — not a chart-pattern fact.
2. **Update cadence.** Funding settles every 8 hours (3 events per day on Binance USDⓈ-M); price-action signals can fire on every 15m bar (96 per day). The signal sources do not share update timing or support set.
3. **Information content.** A funding rate at +0.0001 per 8h (≈ +0.011% per cycle) means longs are paying shorts at an aggregate annualized rate of ~10.95%. This is a *price* of being long that has no analogue in V1's breakout setup or F1's overextension predicate. Both V1 and F1 are agnostic to funding direction at signal time; D1 is signal-determined by funding direction.

The Phase 3a § 6.2 Rank-2 evaluation captured this: "Uniquely leverages a v002 dataset feature (funding rates) the V1 breakout family did not exploit as primary signal." Phase 3f §7.1 elevated this to Rank-1 active path after F1 HARD REJECT made cost-sensitivity the binding gate.

### 3.3 Why D1 is not a V1 breakout variant

D1 uses no V1 breakout mechanism components:

- No range-based setup-validity predicate.
- No 1h binary slope-3 direction-sign bias.
- No EMA(50) / EMA(200) position check.
- No 0.10 × ATR breakout buffer.
- No range-width ≤ 1.75 × ATR(20) consolidation requirement.
- No |close[−1] − open[−8]| ≤ 0.35 × range_width drift cap.
- No ATR-percentile setup filter (R1a-shape).
- No slope-strength magnitude predicate (R1b-narrow-shape).
- No pullback-retest entry-lifecycle (R2-shape).

D1 does **not** depend on a V1 breakout signal at any layer. Phase 2i §1.7 binding-test: D1 is a rule-shape change at the family level, not parameter-tuning of V1 under another label. The setup, entry, exit, and time-stop are all funding-anchored or self-contained — not V1-derived.

### 3.4 Why D1 is not an F1 target-subset rescue

D1 uses no F1 mechanism components:

- No 8-bar cumulative displacement > 1.75 × ATR overextension predicate.
- No SMA(8) frozen target.
- No structural stop with 0.10 × ATR buffer at the start of overextension.
- No 1.75 threshold or 0.10 buffer or [0.60, 1.80] band tied to F1 evidence.
- No same-direction cooldown until unwind (D1's cooldown is funding-event-anchored, not displacement-anchored).
- No mean-reversion-at-SMA(8) target subset selection.

D1's signal source (funding extreme) and D1's target (next funding cycle) are independent of F1's mean-reversion-after-overextension thesis. D1 does not selectively activate on bars where F1's TARGET-eligible subset would have fired; D1 fires on funding-event boundaries, which are uncorrelated with F1's overextension-event boundaries by construction. D1 is not the post-hoc-loosening trap forbidden by Phase 2f §11.3.5 / Phase 3e §5.4 / Phase 3e §8.6 / Phase 3f §5.7.

### 3.5 Why D1 may address F1's high-frequency cost-load failure

F1's HARD REJECT was driven by trade-frequency × per-trade-negative-expR aggregation: 4720 BTC trades × per-trade expR ≈ −0.52 R = R-window total return −546%. Even at LOW slippage F1 was −0.43 R/trade.

D1's expected trade frequency is **structurally lower** by construction:

- Funding extremes occur on the 8-hour funding-event cadence (3 events per day).
- Only extreme funding events (per the threshold below) trigger entries — typically 5–15 events per month per symbol per Phase 3a §4.6(f).
- Each entry triggers at most one position per cycle (cooldown rule); no stacking on the same extreme.
- R-window expected sample size: 60–180 trades per symbol over 36 months (vs F1's 4700+).

This frequency profile is in the same magnitude band as V1 / R3 (33 trades) and well below F1 (4700+). Per-trade negative expR aggregates to bounded total return loss in the worst case, allowing the framework's §10.4 absolute-floor predicate to discriminate cleanly without the catastrophic compounding F1 produced.

### 3.6 Why D1 may address R2's §11.6 slippage-fragility failure

R2's framework FAILED — §11.6 cost-sensitivity blocks. The failure mode was small post-pullback R-distance amplified by 8 bps HIGH slippage; per-trade gain (+0.12 R BTC at MED) was consumed by HIGH-slip cost increase.

D1's structural cost-resilience argument:

- **Stop-distance is 1.0 × ATR** (committed below in §6.7), not constrained by pullback geometry. This is well above R2's small-R-distance regime; per-trade R-multiple potential is structurally larger.
- **Carry is a benefit, not a cost.** D1's contrarian-funding-direction position naturally accrues funding *toward* the strategy (e.g., a SHORT entry at extreme positive funding pays the strategy at each funding settlement). Funding-cost is a built-in tailwind, not a built-in headwind.
- **Round-trip slippage at HIGH (8 bps per side = 16 bps round-trip) on a 1.0 × ATR stop-distance** is a smaller fraction of per-trade R than R2's small post-pullback R-distance experienced. This does not guarantee §11.6 PASS; it makes §11.6 PASS structurally plausible.

D1's §11.6 PASS plausibility is not a guarantee. D1 may still fail §11.6 for reasons not yet observed (e.g., the funding-extreme entry slippage at the 15m bar after a settlement event may be elevated; entry liquidity may be poor at funding-extreme moments). Phase 3g records the plausibility argument as part of the falsifiable hypothesis; the §11.6 outcome is determinable only at any future execution phase.

---

## 4. D1 sub-hypothesis decision

### 4.1 D1-A — Funding-rate extremes as contrarian directional signal

**Hypothesis:** When funding rate is at an extreme positive value (longs paying shorts heavily), the long crowd is over-leveraged and a short-bias position has expected positive directional return at funding-cycle horizons (1–2 cycles). The carry-tailwind partially compensates the short for adverse selection. Symmetric for extreme negative funding.

**Properties:**

- **Self-contained signal source.** Does not depend on a base price-action thesis.
- **Direct falsifiability.** If contrarian post-entry directional displacement at horizon h is not positive (M1 below), the hypothesis falsifies cleanly.
- **No dependency on V1 / F1 / other failed candidates.**
- **Single committed signal predicate** (extreme threshold + direction logic).

### 4.2 D1-B — Funding-aware filter / carry-discount overlay on a directional thesis

**Hypothesis:** Take long signals only when funding is neutral-or-negative (long-cost is favorable); take short signals only when funding is neutral-or-positive (short-cost is favorable). Use funding as a cost-discount filter on top of an existing directional thesis.

**Structural problems:**

- **D1-B requires a base directional thesis it does not supply.** The "existing directional thesis" must be specified independently. Three candidate base theses, none viable:
  - **Base = V1 breakout (H0 / R3).** Then D1-B is structurally another setup-axis filter on top of V1 — analogous to R1a (volatility-percentile) and R1b-narrow (slope-strength). The V1 breakout family is at its useful ceiling per Phase 2x §5; another setup-axis filter is not a family shift, it is another R1a-shape variant inside a closed family. Phase 2i §1.7 binding-test (rule-shape change vs parameter-tuning under another label) classifies D1-B-on-V1 as the latter. Phase 2x §7.2 / Phase 3e §7 treadmill-risk warning applies.
  - **Base = F1 mean-reversion-after-overextension.** Then D1-B is structurally an F1-prime filter — exactly the F1-prime / target-subset rescue forbidden by Phase 3e §5.4 / §8.6 / Phase 3f §5.7. Phase 3d-B2 is terminal for F1; F1-prime is not authorized.
  - **Base = an undeveloped new directional thesis.** Then D1-B's funding component is subordinate to an undeveloped base thesis that would itself require Phase-3a-style discovery + Phase-3b-style spec. D1-B-on-undeveloped-base is not a near-term spec; the base thesis would have to be specified first.
- **D1-B's edge is structurally smaller than D1-A's.** D1-B's edge is the *cost discount* on a base thesis's edge; D1-A's edge is the *direct directional* on funding-extreme events. D1-B requires the base thesis to have positive edge before the cost discount; if the base thesis is V1 (which has not produced positive aggregate edge under the framework) or F1 (HARD REJECTED), the cost discount applied to a no-edge or negative-edge base thesis cannot rescue it.
- **D1-B is not falsifiable in isolation.** D1-B's verdict is entangled with the base thesis's verdict; a D1-B FAIL could be the funding-filter's fault or the base-thesis's fault — not separable.

### 4.3 Sub-hypothesis decision

**Phase 3g specifies D1-A as the first D1 candidate.** D1-B is **NOT** specified as an executable candidate.

Rationale:

- D1-A is structurally cleaner (self-contained, directly falsifiable, no base-thesis dependency).
- D1-B has structural problems on every candidate base thesis (V1 = closed family / R-axis variant trap; F1 = forbidden rescue; undeveloped base = subordinate spec).
- The Phase 3g operator brief explicitly says "Prefer one clean candidate"; D1-A is the clean candidate.
- D1-B may be re-considered in a separately-authorized future phase if and when an independently-developed base directional thesis is operator-defined and falsifiable in isolation. Phase 3g does not propose that.

The remainder of Phase 3g specifies D1-A.

---

## 5. Exact market hypothesis

### 5.1 What funding-rate behavior is expected to predict

When the funding rate at the most recent completed 8-hour funding settlement event is at an extreme positive Z-score (≥ +2.0σ relative to its trailing 90-day distribution), the perpetual-vs-mark-price spread maintenance mechanism has produced sustained long-positioning crowding on Binance USDⓈ-M. The hypothesis predicts:

- Over the next 1–2 funding cycles (8–16 hours = 32–64 × 15m bars), a SHORT position will produce **non-negative directional displacement** at the 32-bar horizon: mean ≥ +0.10 R AND fraction of non-negative outcomes ≥ 50%.
- The SHORT position accrues funding *to the strategy* at each funding settlement during the hold (longs pay shorts); this is a structural cost-discount that should contribute mean ≥ +0.05 R per trade after fee + slippage + funding accounting.
- A subset of trades that reach a +1.0 R take-profit before any time-stop or stop-out should produce mean ≥ +0.30 R aggregate (the M3-style descriptive subset check).

Symmetric mirror-image hypothesis applies to extreme negative funding (≤ −2.0σ): LONG position; longs collect funding at settlements; same M1 / M2 / M3 form.

### 5.2 Why the edge should exist on Binance USDⓈ-M perpetuals

Three structural reasons:

1. **The funding mechanism itself.** Binance's USDⓈ-M perpetual funding rate is computed as `interest_rate + max(min(premium_index, +0.0005), −0.0005)` per 8-hour cycle (clamped). Sustained extremes indicate that the premium-index has been near the ±0.0005 cap for a prolonged period — a strong signal that the perpetual's traders are persistently positioned in one direction relative to the mark price. Persistent positioning imbalance has empirical mean-reversion tendency at multi-cycle horizons in liquid futures markets.
2. **Funding cost discriminates leveraged participants.** Traders paying high funding at extreme rates are typically over-leveraged participants whose positions are vulnerable to price movement away from their bias. When funding is extreme, the threshold for liquidation-cascade or position-closing is structurally lower for the paying side — producing the contrarian directional asymmetry.
3. **Carry tailwind is mechanically a cost discount.** Independent of any directional move, the strategy collects funding on the receiving side of the extreme during each 8-hour settlement of the hold period. This contributes positive R independent of M1 directional outcome — making M1 PASS sufficient but not necessary for net-of-cost positive expR.

The hypothesis is falsifiable at multiple layers (M1 / M2 / M3 below); a clean directional FAIL with positive carry contribution would still produce informative mechanism evidence.

### 5.3 BTCUSDT-primary plausibility

BTCUSDT's funding-rate distribution is typically tighter and more reliable than ETHUSDT's per Phase 3a §4.6(h):

- BTC perpetual has ~10× the daily volume of ETH on Binance USDⓈ-M; deeper liquidity → smoother funding rate.
- BTC funding-extreme events (e.g., during major macro / policy events) tend to be more sustained and less noisy than ETH equivalents.
- BTC's tighter spread profile (Phase 2y §5.1.8) allows tighter execution at funding-event-adjacent 15m bars.
- §1.7.3 BTCUSDT-primary alignment is therefore natural; D1-A's BTC edge is plausibly cleaner than ETH.

This is a plausibility claim, not an empirical claim. F1's Phase 3a §4.1(h) BTC-friendliness plausibility was empirically falsified at first execution (F1 BTC MED expR=−0.52; ETH MED=−0.40 — BTC was *worse* than ETH). Phase 3g records the plausibility honestly: D1's BTC vs ETH outcome at first execution may go either way.

### 5.4 Expected ETH comparison behavior

ETHUSDT is research / comparison only per §1.7.3. Expected ETH behavior at any future execution:

- ETH funding rates can be more erratic (Phase 3a §4.6(h)). The trailing 90-day Z-score normalization should partially compensate for noise differences.
- ETH execution slippage is structurally higher than BTC (Phase 2y §5.1.8); D1-A on ETH may therefore show worse §11.6 cost-sensitivity than BTC.
- ETH is **descriptive comparison only**; D1-A promotion does not depend on ETH PROMOTE per §1.7.3.

The ETH §11.4 non-catastrophic constraint applies (ETH expR > −0.50 AND PF > 0.30); a catastrophic ETH outcome is a HARD REJECT signal per Phase 3c §7.3 precedent.

### 5.5 Why the hypothesis should survive fees, slippage, and funding cost

- **Stop-distance is 1.0 × ATR(20)** (§6.7 below). Per-trade R-multiple potential at +1.0 R take-profit is structurally larger than R2's small-post-pullback R-distance regime.
- **Round-trip taker fee is 0.0005 + 0.0005 = 0.0010 = 10 bps** of notional per round-trip. On a stop-distance of 1.0 × ATR ≈ ~30 bps for BTC (typical ATR / price ≈ 0.003), 10 bps round-trip fee = ~33% of stop-distance = ~0.33 R per trade. A +1.0 R take-profit yields net +0.67 R after fee.
- **HIGH slippage at 8 bps per side = 16 bps round-trip** = ~53% of stop-distance = ~0.53 R per trade additional cost. A +1.0 R take-profit yields net +0.14 R after fee+slip at HIGH. This is plausibly positive but tight; M1 mean must be measurably positive AND M2 funding-tailwind must contribute meaningfully for net-of-all-costs to clear §10.4 at HIGH.
- **Funding accrual is a benefit on the contrarian side.** Average extreme funding ≈ ±0.0005 per 8h (the cap); a 1-cycle hold collects 0.0005 = 5 bps notional; a 2-cycle hold collects 10 bps. On a 1.0 × ATR stop-distance ≈ 30 bps, funding accrual contributes 0.17 R / 0.33 R per trade for 1 / 2 cycle holds — comparable to the round-trip fee/slip cost.

The cost arithmetic is plausibly survivable but tight. Phase 3g records this honestly: D1-A may PASS or FAIL §11.6 = 8 bps HIGH at first execution; the outcome is empirical.

---

## 6. Exact strategy-family definition

Each axis is locked to one committed conceptual rule per Phase 2j §C.6 / §11.3.5 single-spec discipline. No ranges. No "test multiple values" framing. No parameter sweeps. Non-fitting rationale is provided in §7 below.

### 6.1 Funding signal definition

The signal is computed at each 15m bar close as follows:

1. Identify the most recent completed Binance USDⓈ-M 8-hour funding settlement event with `funding_time ≤ bar_close_time`. Funding events occur at 00:00 / 08:00 / 16:00 UTC.
2. Compute the trailing 90-day rolling Z-score of the funding rate at that event:
   - `μ_F` = mean of funding rates over the trailing 90 days of completed funding events (270 events at 3 events/day) **excluding** the current event (no lookahead).
   - `σ_F` = standard deviation of funding rates over the same trailing 90 days.
   - `Z_F = (F_t − μ_F) / σ_F`.
3. The **extreme-funding signal fires** if `|Z_F| ≥ 2.0`.
4. Signal direction: `+2.0 ≤ Z_F` → contrarian SHORT setup. `Z_F ≤ −2.0` → contrarian LONG setup.

### 6.2 Funding lookback / event window

- Lookback for Z-score normalization: **trailing 90 days of completed funding events (270 events)**.
- Each new 15m bar evaluates against the most recent completed funding event prior to that bar's close.
- A given funding event is "fresh" for triggering entries until either (a) a position is opened on it (consuming the event), or (b) a new funding event occurs (new event becomes the most-recent reference).

### 6.3 Entry direction logic

- `Z_F ≥ +2.0` → SHORT entry (contrarian).
- `Z_F ≤ −2.0` → LONG entry (contrarian).

### 6.4 Entry timing

- At each 15m bar close `B`:
  - Compute `Z_F` using the most recent completed funding event prior to `B`.
  - If `|Z_F| ≥ 2.0` AND the funding event has not been previously consumed by an active position AND no D1-A position is currently open AND the cooldown (§6.10) does not block this direction, **register entry candidate at bar `B+1` open**.
- Entry order at bar `B+1` open: market order, contrarian direction.
- Same as V1 / F1 next-bar-open fill assumption.

### 6.5 Allowed directionality

- Symmetric long and short.
- No directional exclusion at any layer.

### 6.6 Timeframe basis

- 15m completed bars for entry timing, stop tracking, target tracking, time-stop counting, M1 horizon counting.
- Funding events resolved at completed 8-hour boundaries (Binance protocol).

### 6.7 Stop definition

- At fill, compute `stop_distance = 1.0 × ATR(20)` where ATR(20) is the Wilder ATR computed on completed 15m bars at the entry bar `B+1`.
- LONG: `stop_price = fill_price − stop_distance`.
- SHORT: `stop_price = fill_price + stop_distance`.
- Stop is **structural at fill, never moved intra-trade** (same invariant as R3 / F1).
- Stop trigger: MARK_PRICE per §1.7.3.

### 6.8 Target / exit definition

- Take-profit at **+1.0 R** (i.e., 1.0 × stop_distance from fill in the favorable direction).
- LONG TP: `tp_price = fill_price + stop_distance`.
- SHORT TP: `tp_price = fill_price − stop_distance`.
- Same-bar priority: STOP > TAKE_PROFIT > TIME_STOP (same as F1 §6.6 / R3 §D.6).

### 6.9 Time stop / max hold rule

- **Unconditional time-stop at 32 × 15m bars after fill** (= 8 hours = exactly one funding cycle).
- If neither STOP nor TARGET has fired by bar `B+1+32`, exit at the close of bar `B+1+32` at TIME_STOP.
- No extension. No conditional re-arming.

### 6.10 Cooldown / re-entry rule

- After any D1-A position closes (STOP / TARGET / TIME_STOP / END_OF_DATA), the **funding event that produced the signal is marked consumed**.
- A new same-direction entry requires a *fresh* funding event with `|Z_F| ≥ 2.0` in the same direction. The funding event must occur **after** the position close timestamp.
- A new opposite-direction entry is allowed at any subsequent funding event regardless of the prior position's direction (no opposite-direction cooldown at the funding-event level).
- No same-direction stacking on a single funding event.

### 6.11 Stop-distance admissibility rule

- D1-A stop_distance is 1.0 × ATR(20) by construction (§6.7).
- Admissibility band: **stop_distance_atr ∈ [0.60, 1.80]**, same band as F1 §4.9 / V1 framework precedent. By construction, D1-A's stop_distance_atr is exactly 1.0, which is inside the band; all entries are admissible.
- The admissibility check is preserved as a guard against any future spec drift that could push the rule outside this band; if the rule ever drifts outside, the entry must be rejected (REJECTED_STOP_DISTANCE).

### 6.12 Funding-accrual handling

- Existing engine `apply_funding_accrual` linear-scan per trade applies unchanged.
- Funding is accrued at every funding settlement that falls within the trade's hold interval `[fill_time, exit_time)`, signed by trade direction (LONG: pays positive funding to longs as cost; SHORT: collects positive funding as benefit).
- D1-A's hypothesis specifically predicts that contrarian-direction positions collect funding as benefit on average; M2 (§10.2) is the falsifiable test.

### 6.13 Regime filter

- **None.** D1-A fires on any funding extreme regardless of price-volatility regime.
- Single-spec discipline per Phase 2j §C.6 / §11.3.5; no regime conditioning to avoid post-hoc fitting.
- A future regime-conditional D1-A-prime is not authorized by Phase 3g and would require a separately-authorized phase with a falsifiable regime-conditional hypothesis.

---

## 7. Non-fitting rationale for every chosen rule

Each axis above is justified by mechanism, project conventions, or data availability — not by likely improvement of results.

| Axis | Committed rule | Non-fitting rationale |
|------|----------------|------------------------|
| Funding signal | 8-hour funding rate at most recent completed event, Z-scored over trailing 90 days | Funding events occur at fixed 8h cadence on Binance USDⓈ-M (protocol fact). 90 days = ~270 events = standard ~3-month stationarity window for crypto markets, large enough for stable second-moment estimate and short enough to track regime shifts. Z-score normalization is a standard tail-extreme statistic. No parameter sweep across alternate windows. |
| Funding lookback | Trailing 90 days, excluding current event | 90-day choice as above. Excluding current event is required to avoid lookahead. |
| Entry direction | Contrarian to funding sign (Z ≥ +2 → SHORT; Z ≤ −2 → LONG) | The hypothesis is contrarian by construction (§5.1). Direction logic follows directly from hypothesis; no alternative directional specification is being tested. |
| Entry timing | Market entry at next 15m bar open after signal | V1 / R3 / F1 precedent; standard "next-bar open after confirmed signal close" pattern; cost-robust by construction. No alternative entry timing being tested. |
| Allowed directionality | Symmetric long and short | The funding-extreme hypothesis is symmetric; no directional asymmetry mechanism is being claimed. |
| Timeframe basis | 15m completed bars for entry / stop / target / time-stop / horizons | V1 / F1 / project convention. 15m is the V1 / F1 signal timeframe per Phase 2i §1.7.3. No alternative timeframe being tested. |
| Stop | 1.0 × ATR(20) at fill, never moved | 1.0 × ATR(20) is the median of the V1 / F1 admissibility band [0.60, 1.80] × ATR (Phase 3b F1 §4.9). It is not fitted to any prior candidate's outcome. "Never moved" is the R3 / F1 invariant per Phase 2j §D / Phase 3b §6. |
| Target | +1.0 R fixed | The smallest natural R-target consistent with V1 framework convention (R3 used +2.0 R; F1 used SMA(8) which produced effective ~0.3–1.0 R targets). +1.0 R is the natural unit-multiplier of stop-distance and the most conservative committed take-profit. Not fitted to outcomes. |
| Time stop | 32 × 15m bars (= 8h = one funding cycle) | Funding cycles are 8 hours by Binance protocol fact. One full funding cycle is the natural maximum-hold horizon for a hypothesis whose carry-tailwind accrues per cycle. 32 bars = 8h × 60min / 15min = 32 (protocol-anchored, not fitted). |
| Cooldown | Per-funding-event consumption; same-direction requires fresh event after close | Prevents same-event stacking (a methodology guard, not a parameter). Opposite-direction allowed at any subsequent event because the hypothesis is symmetric and a sign flip in funding represents a new informational state. |
| Stop-distance admissibility | [0.60, 1.80] × ATR(20) | Same band as F1 §4.9 / V1 framework convention (Phase 3b §4.9). Preserved as a future-drift guard; D1-A's 1.0 × ATR is inside the band by construction. |
| Funding accrual | Existing engine linear-scan per trade | Existing v002 funding-rate dataset + engine `apply_funding_accrual` precedent; no new accrual logic. The hypothesis specifically tests funding accrual as benefit, so accurate accrual is intrinsic to the test. |
| Regime filter | None | Single-spec discipline per Phase 2j §C.6 / §11.3.5. No regime conditioning to avoid post-hoc fitting. |

**No parameter sweep. No ranges. No "test several thresholds" framing.** Each rule has a singular committed conceptual choice.

---

## 8. Required data inputs

### 8.1 v002 dataset sufficiency

**v002 datasets are sufficient for D1-A.** No v003 raw-data bump is required.

### 8.2 Exact raw inputs

- **15m OHLCV** for BTCUSDT and ETHUSDT (existing v002 normalized klines: `usdm_klines_btcusdt_15m__v002` / `usdm_klines_ethusdt_15m__v002` per Phase 2e v002 framing).
- **Mark-price** for BTCUSDT and ETHUSDT (existing v002 mark-price klines) — used for stop-trigger evaluation per §1.7.3 mark-price-stops lock.
- **Funding-rate history** for BTCUSDT and ETHUSDT (existing v002 funding-rate dataset `usdm_funding_rate__v002` per Phase 2e v002 framing). This is the primary signal source for D1-A.
- **Exchange metadata** (existing v002 exchangeInfo snapshot) for tick / step / lot-size constraints.

No 1h derived bars are required. D1-A does **not** use 1h bias filtering (no V1-style 1h slope-3 / EMA(50) / EMA(200) bias). 1h derived bars per Phase 2e remain available for descriptive comparison only (e.g., per-volatility-regime diagnostics in §12).

### 8.3 Derived features needed

D1-A requires the following derived features, all computed at the 15m bar grid:

1. **Wilder ATR(20)** on 15m completed bars. Existing engine primitive (used by V1 / F1).
2. **Funding-rate Z-score series** at funding-event timestamps:
   - `funding_z_score_btcusdt`: per-event Z-score over trailing 90 days.
   - `funding_z_score_ethusdt`: per-event Z-score over trailing 90 days.
3. **Funding-event-aligned-to-15m-bar mapping**: at each 15m bar close, the most recent completed funding event identifier and its Z-score.

These derived features should be packaged as a versioned derived dataset per `dataset-versioning.md` policy.

### 8.4 New derived feature dataset

**One new derived dataset is required:**

- `funding_aware_features__v001` (proposed name following the `dataset-versioning.md` examples).
- Manifest fields:
  - dataset name: `funding_aware_features`
  - dataset version: `v001`
  - dataset category: derived
  - source: `usdm_funding_rate__v002` + `usdm_klines_*__v002` (predecessors)
  - symbols: `BTCUSDT`, `ETHUSDT`
  - intervals: 15m bar grid; 8h funding event grid
  - canonical key: `symbol, bar_open_time` (15m grid) and `symbol, funding_time` (event grid)
  - canonical timezone: UTC; timestamps Unix milliseconds
  - schema:
    - `funding_z_score`: trailing-90-day Z-score per event
    - `funding_event_id`: latest completed funding event reference at each 15m bar
    - `funding_z_score_at_bar`: Z-score of latest completed event at each 15m bar
    - `bars_since_funding_event`: number of completed 15m bars since latest funding event
  - transformation reference: to be defined at any future Phase 3h-equivalent execution-planning phase.

The derived dataset is **a new feature dataset on top of v002**, not a v003 raw-data version. It does not modify any v002 raw or normalized dataset. It does not modify any existing derived dataset.

### 8.5 v003 raw data not needed

D1-A does not require any new raw data source. The Phase 2e v002 funding-rate dataset is sufficient for the hypothesis. No external data (e.g., depth/spread microstructure, social sentiment, on-chain) is required. No new exchange endpoint is required.

---

## 9. Backtester / engine implications

This section is **descriptive / forward-looking only**. Phase 3g does not authorize any of the implementation work below; any actual implementation requires a separately-authorized Phase 3h-equivalent execution-planning phase + Phase 3i-equivalent implementation phase + Phase 3j-equivalent first-execution phase.

### 9.1 Existing engine support

The existing engine **does not currently support** D1-A. The engine has two strategy-family dispatch paths:

- `StrategyFamily.V1_BREAKOUT` (Phase 2 V1 / R3 / R1a / R1b-narrow / R2 dispatch; `_run_symbol_*` methods).
- `StrategyFamily.MEAN_REVERSION_OVEREXTENSION` (Phase 3d-A / 3d-B1 F1 dispatch; `_run_symbol_f1` method).

D1-A would require a third dispatch path, e.g. `StrategyFamily.FUNDING_AWARE_DIRECTIONAL`.

### 9.2 New strategy module

A new self-contained module would be required, structurally analogous to the F1 `MeanReversionStrategy` module:

- `FundingAwareStrategy` module with primitives:
  - `compute_funding_z_score(funding_rates, lookback_days=90)` — primary signal computation.
  - `funding_extreme_event(z_score, threshold=2.0)` — entry detection at the most recent completed funding event.
  - `can_re_enter(direction, funding_event_consumed, position_open)` — cooldown / re-entry logic.
- A locked `FundingAwareConfig` mirroring `MeanReversionConfig` precedent: all axes from §6 frozen as default values; positive validation in `BacktestConfig` requiring `funding_aware_variant` non-None when `strategy_family=FUNDING_AWARE_DIRECTIONAL` and forbidding non-default V1 / F1 strategy_variant.

### 9.3 Config model

The new `FundingAwareConfig` would lock the following defaults (read-only at instantiation, like `MeanReversionConfig` per Phase 3d-A precedent):

```text
funding_z_score_threshold = 2.0
funding_z_score_lookback_days = 90
stop_distance_atr_multiplier = 1.0
take_profit_r_multiple = 1.0
time_stop_bars = 32
cooldown_rule = "per_funding_event"
stop_distance_admissibility_band = [0.60, 1.80]
direction_logic = "contrarian"
regime_filter = None
```

No alternate values would be configurable; the spec is binding.

### 9.4 Diagnostics / report fields

The TradeRecord schema would be extended with D1-specific fields, structurally analogous to F1's Phase 3d-B1 fields:

- `funding_z_score_at_signal`
- `funding_event_id_at_signal`
- `funding_rate_at_signal`
- `bars_since_funding_event_at_signal`
- `funding_accrual_total_R` (existing; verified-applies)
- `entry_to_target_distance_atr`
- `stop_distance_at_signal_atr`

A `FundingAwareLifecycleCounters` model analogous to `F1LifecycleCounters` would track funnel accounting:

- `detected` (count of bars where `|Z_F| ≥ 2.0` was observed)
- `filled` (count of entries that reached fill)
- `rejected_stop_distance` (count of entries rejected by §6.11 admissibility — should be zero by construction)
- `blocked_cooldown` (count of entries blocked by §6.10 cooldown)
- Funnel identity: `detected = filled + rejected_stop_distance + blocked_cooldown`.

### 9.5 Funding-cost modeling

**Existing funding-cost modeling applies unchanged.** The engine's `apply_funding_accrual` linear-scan per trade computes funding accrual at every settlement event within the trade's hold interval, signed by direction. D1-A's hypothesis specifically tests this accrual as a benefit on contrarian-direction trades; no modeling change is required.

### 9.6 Cost model

**Existing cost model applies unchanged.** Round-trip taker fee 0.0005 + 0.0005 = 0.0010; slippage assumptions LOW=1bps / MED=3bps / HIGH=8bps per side per Phase 2y closeout. §11.6 = 8 bps HIGH per side preserved verbatim.

### 9.7 Quality-gate impact

H0 / R3 / V1-family controls and F1 controls must continue to reproduce bit-for-bit on any future Phase 3i-equivalent implementation. The new `FUNDING_AWARE_DIRECTIONAL` dispatch must not perturb V1 or F1 dispatch behavior — same isolation discipline as Phase 3d-B1's F1 wiring.

---

## 10. Falsifiable mechanism predictions

Three M-style mechanism checks, each with explicit PASS / FAIL / PARTIAL interpretation. The patterns mirror Phase 3c §9 F1 mechanism predictions.

### 10.1 M1 — Post-entry directional displacement

**Hypothesis:** Contrarian-funding entries should show favorable post-entry directional displacement at funding-cycle horizons.

**Definition:** For each D1-A trade, compute `counter_displacement_h_R = ((close(B+1+h) − close(B+1)) × trade_direction_sign) / stop_distance` where `trade_direction_sign = +1` for LONG and `−1` for SHORT, at horizons `h ∈ {8, 16, 32}` 15m bars (= 2h, 4h, 8h = 1/4, 1/2, full funding cycle).

**PASS criterion at h=32:** `mean(counter_displacement_32_R) ≥ +0.10 R` AND `fraction(counter_displacement_32_R ≥ 0) ≥ 50%`.

**FAIL:** mean < +0.10 R OR fraction < 50% at h=32.

**PARTIAL:** one of (mean / fraction) PASSES and the other FAILS — same precedent as F1 BTC M1 PARTIAL (mean +0.024 R FAIL but fraction 55.4% PASS).

### 10.2 M2 — Funding-cost benefit

**Hypothesis:** D1-A's contrarian carry-tailwind should contribute a positive funding-accrual benefit per trade on average that materially offsets fee + slippage cost.

**Definition:** For each D1-A trade, compute `funding_benefit_R = funding_accrual_total_R` (engine field, signed by direction; positive when funding flows to the strategy). Aggregate per symbol: `mean(funding_benefit_R)`.

**PASS criterion:** `mean(funding_benefit_R) ≥ +0.05 R per trade per symbol`.

**FAIL:** `mean(funding_benefit_R) < +0.05 R`.

**PARTIAL:** PASS on one symbol, FAIL on the other.

### 10.3 M3 — TARGET-exit subset positive contribution

**Hypothesis:** D1-A's TARGET-exit subset (trades that reach +1.0 R take-profit before any STOP / TIME_STOP) should produce mean ≥ +0.30 R AND aggregate > 0 per symbol.

**Definition:** Filter D1-A trades to TARGET-exit subset only. Compute `mean(net_R)` and `aggregate(net_R)` per symbol.

**PASS criterion:** `mean(net_R) ≥ +0.30 R` AND `aggregate(net_R) > 0` per symbol.

**FAIL:** mean < +0.30 R OR aggregate ≤ 0.

**PARTIAL:** PASS on one symbol, FAIL on the other.

### 10.4 Combined interpretation

The M1 / M2 / M3 verdicts are **descriptive evidence**, not §10.3-equivalent governing thresholds. They inform the verdict mapping in §13. The descriptive-only treatment matches Phase 3c §9 / §11.4 F1 precedent.

A combined M1 PASS + M2 PASS + M3 PASS outcome would be the strongest mechanism evidence; it would still require §10.4-equivalent absolute-floor and §11.6-equivalent cost-resilience clearance for framework PROMOTE.

A combined M1 PARTIAL / M2 PARTIAL / M3 PASS-isolated outcome (which is the F1 precedent at HARD REJECT) would be informative research evidence, but if §10.4-equivalent absolute floors are violated catastrophically the verdict would still be HARD REJECT.

---

## 11. Expected failure modes

Phase 3g records the hypothesis honestly: D1-A may fail at first execution. Anticipated failure modes:

1. **Funding extremes may be continuation signals, not contrarian signals.** If the over-leveraged side wins (price continues in the funding-paying direction), M1 mean would be negative. Empirical funding-extreme behavior in crypto futures is mixed; the contrarian thesis is informed by general market-microstructure logic but is not pre-confirmed for Binance USDⓈ-M.
2. **Carry benefit may be too small versus adverse selection.** If `mean(funding_benefit_R) < +0.05 R` at first execution, the carry-tailwind structural argument fails empirically. Funding rates tend to compress to zero rapidly after extreme readings; the actual carry-during-hold may be smaller than the at-signal extreme suggests.
3. **Sample size may be too low.** At ~5–15 funding extreme events per month per symbol per Phase 3a §4.6(f), R-window expected sample is 60–180 trades per symbol over 36 months. Per-fold (6 half-year folds) sample could be 10–30 trades — comparable to V1 / R3's tight per-fold counts but smaller than F1's 4700. Statistical power may be limited; PROMOTE would require a clean signal that survives sample-fragility.
4. **Funding spikes may coincide with volatility shocks.** Major funding extremes often coincide with macro events / deleveraging cascades / oracle disruptions. Slippage and stop-fire behavior at those moments may be elevated; §11.6 HIGH may FAIL despite the cost-resilience structural argument.
5. **BTC/ETH behavior may diverge.** F1's Phase 3a §4.1(h) BTC-friendliness plausibility was empirically falsified at first execution (F1 BTC was *worse* than ETH). D1-A's Phase 3a §4.6(h) BTC-friendliness plausibility may similarly fail; ETH may be more responsive than BTC, which would create §1.7.3 BTCUSDT-primary lock-eligibility tension.
6. **HIGH-slippage §11.6 may still fail.** D1-A's structural cost-resilience argument is plausibility, not guarantee. At HIGH slip + funding-event-adjacent execution liquidity, the §11.6 gate may still FAIL.
7. **Funding-data alignment / timestamp leakage risk.** Funding events must be aligned to 15m bar timestamps with strict no-lookahead discipline. The "most recent completed funding event prior to bar close" rule is correct but must be implemented carefully; an off-by-one in event-to-bar mapping would constitute lookahead and invalidate any backtest.
8. **Entry timing around 8-hour funding events may introduce settlement leakage.** At the bar containing or immediately following a funding settlement, the funding rate is "fresh" (just published). If the strategy uses the funding rate before the settlement event time has been fully reflected in mark-price / spot-price, or if the funding-rate calculation logic in the dataset has any post-event smoothing, settlement leakage could mistakenly produce edge that does not exist in live trading.
9. **Z-score window edge effects.** The trailing 90-day Z-score normalization assumes a roughly stationary funding-rate distribution over 90 days. During regime shifts (e.g., post-halving, post-major-policy events), the Z-score may produce artifactual extreme readings as the window catches up to the new distribution. This could cause clustered false-positive signals.
10. **Liquidity at funding-event-adjacent 15m bars.** Execution slippage at the 15m bar immediately following an extreme funding event may exceed the §11.6 HIGH = 8 bps assumption. The §11.6 gate is calibrated for general 15m execution; funding-event-adjacent execution may be empirically worse.
11. **R-window vs V-window stationarity.** The Phase 2e R-window (2022-01-01 → 2025-01-01) and V-window (2025-01-01 → 2026-04-01) may differ in funding-rate distribution characteristics. A R-window PASS could fail to replicate in V-window if the funding-rate regime has shifted.

The expected-failure-mode list is **not exhaustive**; first-execution diagnostics may reveal others.

---

## 12. Mandatory diagnostics for any future execution

If a future Phase 3h-equivalent execution-planning phase + Phase 3j-equivalent first-execution phase is authorized, the following diagnostics must be produced. Pattern mirrors Phase 3c §8 / Phase 3d-B2 §12 F1 precedent.

1. **Trade count and frequency** — total n; per-month / per-week / per-day rates.
2. **Long/short split** — count of LONG / SHORT entries; LONG % of total.
3. **Funding-signal distribution** — distribution of `Z_F` at signal events; mean, median, p25, p75, min, max.
4. **Funding-rate-at-entry distribution** — distribution of `funding_rate` (raw, not Z-scored) at signal events; same percentiles.
5. **Per-funding-regime performance** — partition trades by funding-regime tercile (low / mid / high terciles of |Z_F|); per-tercile expR, PF, n.
6. **Per-volatility-regime performance** — partition trades by trailing 1000-bar 1h ATR(20) percentile-rank tercile (same classifier as Phase 2l §6.1 / Phase 2w §11.9 / Phase 3c §9.2); per-tercile expR, PF, n.
7. **Per-fold consistency** — 6 half-year folds (2022H1 / 2022H2 / 2023H1 / 2023H2 / 2024H1 / 2024H2); per-fold n, expR, PF.
8. **Exit-reason fractions** — STOP / TARGET / TIME_STOP / END_OF_DATA percentages.
9. **Funding-accrual contribution** — `mean(funding_accrual_total_R)` per trade per symbol; partition by exit reason.
10. **Fee/slippage/funding decomposition** — per-trade decomposition of net R into gross-R, fee component, slippage component, funding-accrual component. Aggregate across trades.
11. **LOW/MED/HIGH cost sensitivity** — execute four cells: D1-A R LOW MARK / D1-A R MED MARK / D1-A R HIGH MARK / D1-A R MED TRADE_PRICE per Phase 3c §6.1 F1 precedent. Report per-symbol expR / PF / netPct / maxDD per cell.
12. **Mark-price vs trade-price stop-trigger sensitivity** — per Phase 3c precedent.
13. **MFE/MAE distribution** — Maximum Favorable / Adverse Excursion per trade in R-multiples; mean, p25, median, p75, p95.
14. **Stop-distance distribution** — empirical `stop_distance_atr` distribution; should be 1.0 by construction with zero variance.
15. **Hold-time distribution** — bars-held per trade; mean, median, p25, p75, max. By construction max ≤ 32.
16. **Funding-window alignment checks** — verify that the funding event used at each entry signal is the most-recent-completed-prior-to-bar-close, with no off-by-one and no lookahead. Check that no signal fires using a funding event whose `funding_time > bar_close_time`.
17. **BTC/ETH comparison** — side-by-side per-symbol summaries for all metrics above.
18. **Descriptive H0/R3 references only** — H0 / R3 control runs at MED MARK to provide cross-family context. **H0 / R3 are NOT governing anchors for D1-A's first-execution gate** (per §13 below); they are descriptive references only, same precedent as Phase 3c §7.4 / §11.9 / Phase 3d-B2 §15.

P.14-style hard-block invariants (analogous to Phase 3c §8.15 / Phase 3d-B2 §13):

- D1-A emits only STOP / TARGET / TIME_STOP / END_OF_DATA exit reasons.
- Zero TRAILING_BREACH / STAGNATION / TAKE_PROFIT (the V1 multi-stage exit reasons must not appear).
- Exit-reason accounting identity: `STOP + TARGET + TIME_STOP + END_OF_DATA = n`.
- Funnel accounting identity: `detected = filled + rejected_stop_distance + blocked_cooldown`.
- Stop-distance band [0.60, 1.80] enforcement (D1-A is 1.0 by construction; observed `min ≈ 1.0 ≈ max`).
- Frozen stop invariant: stop never moved intra-trade.
- Cooldown enforcement: no same-event same-direction re-entry.
- No look-ahead leakage: funding event used at signal must satisfy `funding_time ≤ bar_close_time`.
- H0 / R3 / F1 controls reproduce bit-for-bit before D1-A interpretation.

---

## 13. Promotion / failure framework

### 13.1 Phase 2 §10.3 V1-family framework remains anchored on H0

The Phase 2 §10.3 (a/b/c) / §10.4 / §11.3 / §11.4 / §11.6 framework was designed to compare V1-family candidates against H0. **It is not directly applicable to D1-A's first-execution gate** because D1-A is a separate strategy family with no V1 baseline equivalent.

- H0 remains the V1-family framework anchor.
- R3 remains the V1-family baseline-of-record.
- Both H0 and R3 are **descriptive cross-family references only** for D1-A; not governing anchors.

### 13.2 D1-A first-execution gate proposal (analogous to Phase 3c §7.2 F1 gate)

The proposed first-execution gate evaluates D1-A against **self-anchored absolute thresholds**, not vs-H0 deltas. Five conditions, all required for PROMOTE:

| # | Condition | Cell | Threshold |
|---|-----------|------|-----------|
| (i) | Absolute BTC MED edge | BTC R MED MARK | `expR > 0` |
| (ii) | M1 BTC mechanism | BTC | `mean(counter_displacement_32_R) ≥ +0.10 R` AND `fraction ≥ 50%` |
| (iii) | ETH MED non-catastrophic | ETH R MED MARK | `expR > −0.50` AND `PF > 0.30` |
| (iv) | BTC HIGH cost-resilience | BTC R HIGH MARK | `expR > 0` |
| (iv) | ETH HIGH non-catastrophic | ETH R HIGH MARK | `expR > −0.50` AND `PF > 0.30` |
| (v) | BTC MED absolute floor | BTC R MED MARK | `expR > −0.50` AND `PF > 0.30` |
| (v) | ETH MED absolute floor | ETH R MED MARK | `expR > −0.50` AND `PF > 0.30` |

This gate is **structurally identical to the Phase 3c §7.2 F1 gate** (with identical operator-mandated amendments §7.2(iv) BTC HIGH > 0 and §11.6 cost-sensitivity blocking; per Phase 2y closeout §11.6 = 8 bps HIGH preserved verbatim). The conditions are pre-declared and must not be loosened post-hoc per Phase 2f §11.3.5.

### 13.3 Verdict mapping (analogous to Phase 3c §7.3)

| Outcome | Definition | Verdict |
|---------|------------|---------|
| **HARD REJECT** | Any catastrophic absolute-floor violation: `expR ≤ −0.50` OR `PF ≤ 0.30` on either symbol at either MED or HIGH slippage on MARK_PRICE cells. | HARD REJECT — no V-window run; D1-A retained as research evidence only; D1-A family research closed. |
| **MECHANISM FAIL** | M1 BTC FAIL (mean < +0.10 R OR fraction < 50% at h=32) AND no catastrophic floor violation. | MECHANISM FAIL — D1-A retained as research evidence; no V-window run unless M1 PASS achievable; framework verdict FAILED. |
| **MECHANISM PASS / FRAMEWORK FAIL — §11.6 cost-sensitivity blocks** | M1 BTC PASS AND BTC MED expR > 0 AND ETH MED non-catastrophic AND M2/M3 mechanism support, BUT BTC HIGH expR ≤ 0 OR ETH HIGH catastrophic. | FRAMEWORK FAIL — §11.6 cost-sensitivity blocks; D1-A retained as research evidence; no V-window run; same precedent as R2. |
| **MECHANISM PASS / FRAMEWORK FAIL — other** | M1 BTC PASS but a non-§11.6 framework condition fails (e.g., BTC MED expR ≤ 0). | FRAMEWORK FAIL — D1-A retained as research evidence; no V-window run. |
| **PROMOTE** | All §13.2 conditions PASS AND no catastrophic-floor violation. | PROMOTE — V-window run authorized for confirmation; D1-A becomes a candidate-of-record candidate (subject to V-window confirmation per Phase 2f §11.3 no-peeking rule). |

**HARD REJECT supersedes MECHANISM PASS** in the verdict mapping: a catastrophic absolute-floor violation is the binding signal regardless of mechanism evidence (same precedent as F1 / R2).

### 13.4 §10.4-style hard reject absolute floors preserved

The §10.4 absolute floors are preserved verbatim:

- `expR > −0.50` per symbol per MED / HIGH cell.
- `PF > 0.30` per symbol per MED / HIGH cell.

A violation on any of `{BTC MED, BTC HIGH, ETH MED, ETH HIGH}` × `{expR ≤ −0.50, PF ≤ 0.30}` triggers HARD REJECT.

### 13.5 §11.6 HIGH-slippage cost gate preserved

§11.6 = 8 bps HIGH per side preserved verbatim per Phase 2y closeout. The §13.2(iv) BTC HIGH expR > 0 condition operationalizes §11.6 for D1-A (same operator-mandated amendment as Phase 3c §7.2(iv) for F1).

### 13.6 Thresholds not loosened

Phase 3g does not loosen any threshold. The D1-A first-execution gate uses §10.4 absolute floors verbatim, the §11.6 HIGH per-side fee verbatim, and the operator-mandated BTC HIGH > 0 strengthening from Phase 3c §7.2(iv). All are pre-declared per Phase 2f §11.3.5 binding rule.

---

## 14. Overfitting risk analysis

### 14.1 Why funding thresholds are vulnerable to fitting

Three vulnerability classes:

1. **Z-score threshold |Z_F| ≥ 2.0** is a single tunable knob that, at any future execution, would produce a different trade count and different per-trade expR. Phase 3a §4.6(i) flagged "moderate overfitting risk" for the funding-aware family at the menu level. A future researcher with access to the empirical results could find a |Z_F| threshold that improves the §13.2 outcome — that is exactly the post-hoc loosening Phase 2f §11.3.5 forbids.
2. **Lookback window N=90 days** is similarly tunable. A different lookback window changes the Z-score distribution; the empirical fit could be improved by tuning. The single committed value 90 days must not be revised after seeing the first-execution data.
3. **Time-stop bars=32** is anchored to one funding cycle (8h × 60min / 15min). A future researcher could try alternative time-stops (e.g., 16 / 64 / 96 bars) and find one that improves the §13.2 outcome — also forbidden post-hoc.

### 14.2 How the single-spec rule prevents this

Per Phase 2j §C.6 / §11.3.5 single-spec discipline:

- **Each axis is locked to one committed value** (§6 + §7).
- **No alternative values are tested at first execution.** The Phase 3c §6.1-equivalent run inventory (4 mandatory R-window cells: D1-A R LOW MARK; D1-A R MED MARK; D1-A R HIGH MARK; D1-A R MED TRADE_PRICE) tests the single committed spec across cost-sensitivity cells only; no alternative parameter values.
- **The first-execution gate is pre-declared (§13).** PROMOTE / HARD REJECT / FRAMEWORK FAIL / MECHANISM FAIL outcomes are determined by the pre-declared §13.2 / §13.3 thresholds; no post-hoc threshold revision.

### 14.3 What must be forbidden in future execution

If a Phase 3h-equivalent execution-planning phase + Phase 3j-equivalent first-execution phase is later authorized, the following must be forbidden:

- **No threshold sweep** on |Z_F| ≥ 2.0; the value is locked. A sweep would be exactly the Phase 2f §11.3.5 forbidden post-hoc loosening.
- **No lookback sweep** on N=90 days; locked.
- **No time-stop sweep** on 32 bars; locked.
- **No regime-conditional D1-A-prime spec** without a separately-authorized phase with an independently-developed regime-conditional hypothesis.
- **No directional-asymmetric D1-A-prime spec** (e.g., "only short on positive funding extremes, not long on negative"); the symmetric direction is locked.
- **No retrospective TARGET-subset selection** to rescue D1-A if M3 PASS but framework FAIL (same Phase 3e §5.4 / §8.6 / Phase 3f §5.7 prohibition).
- **No D1-A-on-V1 hybrid** (D1-A signal AS-A-FILTER on top of V1 / R3 baseline) without a separately-authorized phase. Such a hybrid would be an R-axis variant on V1 (re-opening the closed family) and may also constitute D1-B disguised — both forbidden per §4.

### 14.4 How to avoid post-hoc threshold rescue

The discipline that produced clean PROMOTE / FAIL decisions on R3 / R1a / R1b-narrow / R2 / F1 depends on:

- **Pre-declared single-spec thresholds.** Phase 3g locks all D1-A axes (§6 + §13.2).
- **Catastrophic-floor predicate as binding signal.** A catastrophic violation triggers HARD REJECT regardless of mechanism partial support — same precedent as F1.
- **Framework-calibration question is operator-policy, not strategy-redesign.** §11.6 HIGH-slippage threshold revision requires a separately-authorized framework-calibration phase (Phase 3f Option D7 / Phase 2y / Phase 2x §6 Option C path) with **external Binance live-execution evidence**, not strategy-outcome evidence.

The treadmill that would produce another mixed/failed result is avoided by the pre-declared spec + pre-declared gate + pre-declared no-loosen rule. If D1-A HARD REJECTS or FRAMEWORK FAILS at first execution, **D1-A is closed as research evidence**; no D1-A-prime is auto-authorized.

---

## 15. GO / NO-GO decision for a future Phase 3h execution-planning memo

### 15.1 GO conditions

A Phase 3h execution-planning memo (Phase-3c-style) is **GO (provisional)** if and only if all of the following are true:

1. **D1-A can be specified cleanly without tuning** — confirmed by §6 + §7 single-spec rule commitments.
2. **No threshold sweeps or parameter ranges are required** — confirmed by §6 single-value commitments.
3. **v002 funding data is sufficient** — confirmed by §8.
4. **The hypothesis is not too sample-starved at the framework level** — provisionally OK; expected R-window n=60–180 per symbol is comparable to V1/R3's 33 but smaller than F1's 4700; per-fold n=10–30 per symbol is sample-fragile but inside the band V1/R3/R1b-narrow operated in.
5. **D1-A does not degenerate into V1 breakout, F1-prime, or target-subset rescue** — confirmed by §3.3, §3.4, §4.
6. **Cost sensitivity does not appear structurally fatal** — provisional plausibility per §3.6 / §5.5; final §11.6 outcome is empirical at any future execution.
7. **The operator independently authorizes Phase 3h.** Phase 3g does not authorize Phase 3h.

### 15.2 NO-GO conditions

Phase 3h is **NO-GO** if:

- **D1-A needs threshold sweeps** to produce a credible result. The Phase 3g spec locks single values; if any future researcher proposes a sweep at the Phase 3h-equivalent stage, that would re-open the §11.3.5 post-hoc-loosening trap and Phase 3h must NOT proceed. Phase 3g §7 + §14 rule out sweep framing.
- **v002 funding data is empirically insufficient** (e.g., dataset coverage gaps, Z-score window edge effects more severe than anticipated). Discoverable only at any future Phase 3h-equivalent or Phase 3i-equivalent stage; if discovered, escalation to a v003 data-requirements phase is required and Phase 3h is paused.
- **The hypothesis is too sample-starved at the framework level.** If empirical R-window n is below ~30 per symbol, §10.3 / §11.2 fold-consistency evaluation may not be statistically credible; Phase 3h should NO-GO and a different hypothesis spec should be developed.
- **D1-A degenerates into V1 breakout / F1-prime / target-subset rescue** at the Phase 3h-equivalent stage. If the execution-planning memo proposes hybridizing D1-A with V1 baseline or F1 mean-reversion, or proposes selecting only a TARGET-eligible subset of D1-A trades, Phase 3h must NO-GO and the proposal must be reformulated.
- **Cost sensitivity appears structurally fatal** at the Phase 3h-equivalent stage's pre-execution analysis (e.g., §11.6 HIGH would produce expR ≤ −0.50 by structural argument alone). Phase 3g §3.6 / §5.5 cost-arithmetic sketch is plausible-but-tight; if pre-execution analysis at Phase 3h reveals structural fatality, Phase 3h must NO-GO.

### 15.3 Phase 3g recommendation

**Phase 3g recommends GO (provisional) for a future Phase 3h execution-planning memo for D1-A**, contingent on operator authorization. The spec is single-spec-compliant; the data is v002-sufficient; the hypothesis is falsifiable; the strategy does not degenerate into prior-failed candidates; the cost arithmetic is plausibly survivable.

**Phase 3g does NOT authorize Phase 3h.** Phase 3h requires a separately-authorized operator decision. Phase 3g terminates at the spec memo.

### 15.4 What Phase 3h would NOT do

Even if authorized, a future Phase 3h execution-planning memo would:

- Not authorize execution. Phase 3h is execution-PLANNING, not execution. Phase 3h would produce a Phase-3c-style memo defining the precommitted run inventory, execution gate, mechanism checks, mandatory diagnostics, and P.14-style hard-block invariants. Implementation phase + execution phase + V-window phase would each require their own subsequent operator decisions.
- Not change any threshold. §10.3 / §10.4 / §11.3 / §11.4 / §11.6 = 8 bps HIGH per side preserved.
- Not change any §1.7.3 project-level lock.
- Not propose paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write work.
- Not alter R3's baseline-of-record status, H0's framework-anchor status, or R1a / R1b-narrow / R2 / F1's retained-research-evidence status.
- Not propose any MCP / Graphify / `.mcp.json` / credentials / `data/` commits.

---

## 16. Explicit project-state preservation

Phase 3g is docs-only and explicitly preserves all of the following verbatim:

- **R3 remains V1 breakout baseline-of-record** per Phase 2p §C.1. Locked sub-parameters: `exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`. Same-bar priority STOP > TAKE_PROFIT > TIME_STOP. Phase 2j memo §D.6 invariants preserved.
- **H0 remains the formal V1 breakout framework anchor** per Phase 2i §1.7.3.
- **R1a remains research evidence only** per Phase 2p §D. Retained-for-future-hypothesis-planning. Not deployable; not the current default.
- **R1b-narrow remains research evidence only** per Phase 2s §13.
- **R2 remains research evidence only** per Phase 2w §16.3. Framework verdict FAILED — §11.6 cost-sensitivity blocks. Mechanism evidence (M1 + M3 PASS; M2 FAIL) preserved as descriptive.
- **F1 remains research evidence only.** Framework verdict HARD REJECT per Phase 3c §7.3 catastrophic-floor predicate. Phase 3d-B2 terminal for F1. F1-prime not authorized.
- **No threshold change.** Phase 2f §10.3 / §10.4 / §11.3 / §11.4 / **§11.6 = 8 bps HIGH per side** preserved verbatim per Phase 2f §11.3.5 / Phase 2y closeout / Phase 3e §11 / Phase 3f §11.
- **No project-level lock change.** §1.7.3 BTCUSDT primary live, ETHUSDT research/comparison only, one-symbol-only live, one-position max, 0.25% risk per trade, 2× leverage cap, mark-price stops, v002 datasets, one-way mode, isolated margin, no pyramiding, no reversal while positioned, no hedge mode — all preserved verbatim.
- **No paper/shadow planning is authorized.** Phase 3e §11 / Phase 3f §11 deferral stands.
- **No Phase 4 (runtime / state / persistence) is authorized.** Phase 3e §11 / Phase 3f §11 deferral stands.
- **No live-readiness work is authorized.** No deployment, no exchange-write capability, no production keys.
- **No credentials.** No production / sandbox / testnet API keys requested, created, or used. No `.env` file modified. No secrets in any committed file.
- **No MCP / Graphify / `.mcp.json` activation.** No MCP server enabled; no Graphify integration; no `.mcp.json` file created or modified.
- **No exchange-write paths.** No exchange-write capability proposed, implemented, or enabled. `BacktestAdapter.FAKE` remains the only adapter type in the engine.
- **No `data/` commits.** Phase 3g commits are limited to the two `docs/00-meta/implementation-reports/` files.
- **No code change.** No file in `src/`, `tests/`, `scripts/`, `.claude/` is touched by Phase 3g.
- **No existing-spec change.** `v1-breakout-strategy-spec.md`, `v1-breakout-validation-checklist.md`, `cost-modeling.md`, `backtesting-principles.md`, `phase-gates.md`, `technical-debt-register.md`, `data-requirements.md`, `dataset-versioning.md`, `current-project-state.md`, `ai-coding-handoff.md` all preserved.
- **No execution authorization.** Phase 3g does not authorize Phase 3h. Phase 3h requires a separately-authorized operator decision.
- **No implementation authorization.** Phase 3g does not authorize any code, test, script, or runtime change.
- **No backtest authorization.** Phase 3g does not authorize any backtest run. The Phase 3g §12 / §13 diagnostics and gate definitions are forward-looking specifications only.

---

**End of Phase 3g D1 funding-aware spec memo.** Phase 3g specifies D1-A (funding-rate extreme contrarian directional signal at the most recent completed 8h funding event, |Z_F| ≥ 2.0 over trailing 90 days; 1.0 × ATR(20) stop; +1.0 R take-profit; 32-bar time-stop = one funding cycle; per-funding-event cooldown; symmetric direction; no regime filter) as the binding D1 family spec. D1-B not specified (structural problems on every base-thesis). v002 datasets sufficient; one new derived feature dataset (`funding_aware_features__v001`) required at any future implementation. M1 / M2 / M3 falsifiable mechanism predictions defined. First-execution gate proposed (analogous to Phase 3c §7.2 F1 gate; §10.4 floors and §11.6 = 8 bps HIGH preserved verbatim; operator-mandated BTC HIGH > 0 strengthening preserved). GO (provisional) recommended for any future Phase 3h execution-planning memo, contingent on operator authorization. R3 baseline-of-record / H0 framework anchor / R1a-R1b-narrow-R2-F1 retained-research-evidence preserved verbatim. F1 HARD REJECT preserved; Phase 3d-B2 terminal for F1 preserved. §1.7.3 locks preserved verbatim. No paper/shadow, no Phase 4, no live-readiness, no deployment, no implementation, no execution, no backtest, no parameter tuning, no threshold change, no project-lock change, no MCP / Graphify / `.mcp.json`, no credentials, no `data/` commits, no code change. No next phase started. Awaiting operator review.
