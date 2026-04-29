# Phase 3k — Post-D1-A Research Consolidation / Strategy-Reset Memo

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; **no post-hoc loosening per §11.3.5**); Phase 2i §1.7.3 project-level locks (H0 anchor; BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets); Phase 2p consolidation memo (R3 baseline-of-record; future-resumption pre-conditions); Phase 2x family-review memo (V1 breakout family at useful ceiling under current framework); Phase 2y slippage / cost-policy review (§11.6 = 8 bps HIGH preserved); Phase 3a new-strategy-family discovery memo (F1 ranked rank-1 near-term family candidate); Phase 3b F1 spec memo §§ 1–15 (binding F1 spec); Phase 3c F1 execution-planning memo §§ 1–13; Phase 3d-A / 3d-B1 / 3d-B2 reports + Phase 3d-B2 merge report; Phase 3e post-F1 research consolidation memo (remain-paused recommendation); Phase 3f research-direction discovery memo (D1 = funding-aware directional / carry-aware as rank-1 active path); Phase 3g D1-A spec memo + methodology sanity audit (binding D1-A spec); Phase 3h D1-A execution-planning memo (binding execution plan with timing-clarification amendments); Phase 3i-A D1-A implementation-controls + Phase 3i-B1 engine-wiring-controls (binding implementation surface); Phase 3j D1-A execution + diagnostics + first-execution-gate evaluation + closeout + merge reports; `docs/03-strategy-research/v1-breakout-strategy-spec.md`; `docs/05-backtesting-validation/backtesting-principles.md`; `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`; `docs/05-backtesting-validation/cost-modeling.md`; `docs/04-data/data-requirements.md`; `docs/04-data/dataset-versioning.md`; `.claude/rules/prometheus-core.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/implementation-ambiguity-log.md`.

**Phase:** 3k — Docs-only **post-D1-A research consolidation / strategy-reset memo.** Consolidates the completed V1 breakout + F1 mean-reversion + D1-A funding-aware research arcs, updates canonical project-state documentation, and produces a disciplined operator decision menu for what should happen next.

**Branch:** `phase-3k/post-d1a-consolidation`. **Memo date:** 2026-04-29 UTC.

**Status:** Recommendation drafted. **No code change. No backtest. No variant created. No parameter tuned. No threshold changed. No project-level lock changed. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write proposal.** R3 remains baseline-of-record. H0 remains framework anchor. R1a / R1b-narrow / R2 / F1 / D1-A remain retained as research evidence. Recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

## 1. Plain-English explanation of what Phase 3k is deciding

Phase 3k is a docs-only consolidation phase, the natural successor to Phase 3j's MECHANISM PASS / FRAMEWORK FAIL — other verdict on D1-A, just as Phase 3e was the natural successor to Phase 3d-B2's HARD REJECT verdict on F1.

The Prometheus project has now executed **three complete strategy research arcs** under unchanged framework discipline:

- **The V1 breakout-continuation arc** (Phases 2e through 2w) — one locked baseline (H0), one cleanly-promoted structural redesign (R3), and three post-R3 structural redesigns (R1a, R1b-narrow, R2) of which one was framework-FAILED on §11.6 cost-sensitivity. R3 became the baseline-of-record per Phase 2p §C.1.
- **The F1 mean-reversion-after-overextension arc** (Phases 3a through 3d-B2) — one new strategy family (F1) ranked as the Phase 3a rank-1 near-term candidate, executed at Phase 3d-B2, **HARD REJECTED** per Phase 3c §7.3 catastrophic-floor predicate (5 catastrophic violations).
- **The D1-A funding-aware directional / carry-aware arc** (Phases 3f through 3j) — Phase 3f selected D1 (funding-aware) as the rank-1 active path post-F1; Phase 3g locked the D1-A spec; Phase 3h drafted the execution plan with timing-clarification amendments; Phase 3i-A implemented the strategy module; Phase 3i-B1 wired it through the engine; Phase 3j executed the precommitted R-window inventory (4 cells) and evaluated the Phase 3h §11 first-execution gate. **Verdict: MECHANISM PASS / FRAMEWORK FAIL — other.** No catastrophic-floor violation; M1 PASS at h=32 BTC (mechanism present); M2 FAIL on both symbols (funding benefit ~21× / ~11× below threshold); M3 PASS-isolated on both symbols (TARGET subset profitable but overwhelmed by 67–68% STOP exits). D1-A's locked spec axes do not produce a positive aggregate edge under §11.6 / §1.7.3 / §10.4 discipline.

Phase 3k weighs the resulting question:

> Given that the V1 breakout family is at its useful ceiling (Phase 2x), the rank-1 near-term new family (F1) hard-rejected, **and** the rank-1 active-path post-F1 family (D1-A) framework-failed under a milder mode but still framework-failed, **what is the right next docs-only phase, if any?**

What Phase 3k is NOT deciding:

- Not deciding whether to deploy R3 or to begin paper/shadow (forbidden by operator policy).
- Not deciding whether to begin Phase 4 runtime / state / persistence work (forbidden).
- Not deciding whether to lift any §1.7.3 project-level lock.
- Not deciding whether to revise any Phase 2f threshold (Phase 2y closed §11.6; Phase 3j did not produce evidence justifying re-opening).
- Not authorizing any next execution phase, any next implementation phase, any backtest, or any code change.
- Not commencing D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, or any successor variant.

The output is a consolidated record of project state plus an operator decision menu with a single recommended next step (which legitimately may be "remain paused" as Phase 3e recommended). Phase 3k produces a memo; the operator decides whether to authorize anything downstream.

---

## 2. Current canonical project state

| Item | State |
|------|-------|
| **R3 (Phase 2j memo §D — Fixed-R + 8-bar time-stop, no trailing)** | **V1 breakout baseline-of-record** per Phase 2p §C.1; locked sub-parameters `exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`; same-bar priority STOP > TAKE_PROFIT > TIME_STOP; protective stop never moved intra-trade. |
| **H0 (Phase 2e locked baseline)** | **V1 breakout framework anchor** per Phase 2i §1.7.3; sole §10.3 / §10.4 / §11.3 / §11.4 / §11.6 comparison anchor for all V1-family candidates. |
| **R1a (Phase 2j memo §C — volatility-percentile setup, X=25 / N=200, on top of R3)** | Retained as **research evidence only** per Phase 2p §D; non-leading; symbol-asymmetric mixed-PROMOTE (ETH-favorable / BTC-degrading). |
| **R1b-narrow (Phase 2r — bias-strength magnitude S=0.0020 on top of R3)** | Retained as **research evidence only** per Phase 2s §13; non-leading; formal §10.3.a-on-both PROMOTE but R3-anchor near-neutral marginal contribution. |
| **R2 (Phase 2u — pullback-retest entry topology on top of R3)** | Retained as **research evidence only** per Phase 2w §16.3; **framework FAILED — §11.6 cost-sensitivity blocks** (BTC HIGH-slip Δexp_H0 −0.014; ETH HIGH-slip Δexp_H0 −0.230). M1 + M3 mechanism support but slippage-fragile. |
| **F1 (Phase 3b §4 — mean-reversion-after-overextension)** | Retained as **research evidence only**; **framework verdict: HARD REJECT** per Phase 3c §7.3 catastrophic-floor predicate (5 separate violations across BTC/ETH × MED/HIGH); Phase 3d-B2 terminal for F1. |
| **D1-A (Phase 3g §6 — funding-aware directional / carry-aware contrarian)** | Retained as **research evidence only**; **framework verdict: MECHANISM PASS / FRAMEWORK FAIL — other** per Phase 3h §11.2 (catastrophic-floor predicate NOT triggered; cond_i BTC MED expR > 0 FAILED; cond_iv BTC HIGH cost-resilience FAILED; M1 BTC h=32 PASS; M2 FAIL both symbols; M3 PASS-isolated both symbols); Phase 3j terminal for D1-A under current locked spec. |
| **§1.7.3 project-level locks** | **Preserved verbatim:** BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; one active protective stop max; 0.25% risk per trade; 2× leverage cap; mark-price stops; v002 datasets; one-way mode; isolated margin; no pyramiding; no reversal while positioned; no hedge mode. |
| **Phase 2f thresholds** | **Preserved verbatim:** §10.3.a Δexp ≥ +0.10 R; §10.3.c \|maxDD\| ratio < 1.5×; §10.4 absolute floors expR > −0.50 AND PF > 0.30 (note: catastrophic-floor predicate triggers iff `expR ≤ −0.50 OR PF ≤ 0.30`; non-catastrophic requires *both* expR > −0.50 AND PF > 0.30); §11.3 V-window no-peeking; §11.4 ETH non-catastrophic; **§11.6 = 8 bps HIGH per side** (Phase 2y closeout, preserved unchanged). |
| **Phase 3b F1 spec axes** | **Preserved verbatim:** overextension window 8; threshold 1.75 × ATR(20); mean-reference window 8 (frozen SMA(8) at signal close); stop buffer 0.10 × ATR(20); time-stop 8 bars; stop-distance band [0.60, 1.80] × ATR(20). |
| **Phase 3g D1-A spec axes** | **Preserved verbatim:** \|Z_F\| ≥ 2.0 over trailing 90 days / 270 events with current-event exclusion; 1.0 × ATR(20) stop; +2.0R fixed target; 32-bar (8-hour) unconditional time-stop; per-funding-event cooldown; band [0.60, 1.80] × ATR(20); contrarian direction; no regime filter. |
| **Paper/shadow planning** | **Not authorized.** Operator policy continues to defer paper/shadow indefinitely. |
| **Phase 4 (runtime / state / persistence) work** | **Not authorized.** No runtime / state / persistence implementation has been started. |
| **Live-readiness work** | **Not authorized.** No production-key creation, no exchange-write capability, no deployment. |
| **MCP / Graphify / `.mcp.json`** | **Not activated, not touched.** |
| **Credentials / `.env` / API keys** | **Not requested, not created, not used.** |

The next operator decision is operator-driven only. Phase 3k does not pre-empt that decision; this section records the state on which any future decision must build.

---

## 3. Research arc summary

The complete three-arc Prometheus strategy-research history through Phase 3j:

### 3.1 V1 breakout-continuation arc (Phase 2e through Phase 2w)

| Phase | What it produced |
|-------|------------------|
| **2e** | H0 locked baseline (Phase 2e v002 datasets); BTC R-window expR=−0.459 / ETH expR=−0.475. |
| **2f Gate 1** | §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds pre-declared; §11.3.5 binding rule (no post-hoc loosening). |
| **2g** | Wave-1 parametric variants tested vs H0; **REJECT ALL.** Preserved as historical evidence only. |
| **2h** | Decision memo: structural redesigns warranted; parametric tuning insufficient. |
| **2i** | §1.7.3 project-level locks committed; H0 designated sole §10.3 anchor. |
| **2j** | Structural redesign specs: §C R1a (volatility-percentile setup), §D R3 (Fixed-R + 8-bar time-stop). |
| **2l** | R3 first execution: **PROMOTE — broad-based.** R3 improves expR in all 6 regime-symbol cells; first positive-expR BTC folds (F2, F3); cost-robust at HIGH; bit-identical MARK vs TRADE_PRICE. |
| **2m** | R1a+R3 first execution: **mixed-PROMOTE.** ETH-favorable / BTC-degrading; mechanically correct compression-selection but symbol asymmetry. |
| **2p** | Consolidation memo: **R3 baseline-of-record locked**; R1a retained-for-future-hypothesis-planning research evidence. |
| **2r / 2s** | R1b-narrow spec + first execution: formal §10.3.a-on-both PROMOTE but R3-anchor near-neutral marginal contribution; retained research evidence. |
| **2t / 2u / 2v / 2w** | R2 spec + execution: MED-slip §10.3 PROMOTE with M1 + M3 mechanism support; **§11.6 cost-sensitivity gate FAILS** at HIGH on both symbols; **framework FAILED — slippage-fragile**; retained research evidence. |
| **2x** | V1 breakout family-level review: **family at useful ceiling under current framework**. |
| **2y** | Slippage / cost-policy review: **§11.6 = 8 bps HIGH preserved unchanged**; framework calibration confirmed. |

**V1 breakout arc outcome:** R3 is the strongest single candidate evidence the project has produced. R3 alone produces a clean broad-based PROMOTE; the absolute-aggregate edge has not materialized (R3 BTC R-window expR=−0.240 / ETH=−0.351 — still negative). The family is **alive but not validated for live exposure**.

### 3.2 F1 mean-reversion-after-overextension arc (Phase 3a through Phase 3d-B2)

| Phase | What it produced |
|-------|------------------|
| **3a** | Docs-only new-strategy-family discovery; F1 ranked **rank-1 near-term candidate**. |
| **3b** | Docs-only F1 spec memo: 9 axes locked; falsifiable mechanism predictions M1/M2/M3. |
| **3c** | Docs-only F1 execution-planning memo; precommitted run inventory; first-execution gate definition (§7.2 / §7.3 catastrophic-floor predicate). |
| **3d-A** | F1 implementation-only phase; deliberately non-runnable; H0/R3 controls bit-for-bit. |
| **3d-B1** | F1 engine-wiring phase; Phase 3d-A guard lifted; runner scaffold under Phase 3d-B2 hard guard. |
| **3d-B2** | F1 first-execution: 4 mandatory R-window cells executed; **framework verdict: HARD REJECT** (5 catastrophic floor violations). |
| **3e** | Docs-only post-F1 research consolidation memo; recommendation **remain paused** with operator decision menu. |

**F1 arc outcome:** F1 first-execution HARD REJECT per Phase 3c §7.3 catastrophic-floor predicate. F1 retained as research evidence; F1 family research is concluded as failed. Phase 3d-B2 is terminal for F1; no subsequent F1 phase is proposed.

### 3.3 D1-A funding-aware directional / carry-aware arc (Phase 3f through Phase 3j)

| Phase | What it produced |
|-------|------------------|
| **3f** | Docs-only research-direction discovery memo post-F1: D1 (funding-aware directional / carry-aware) ranked **rank-1 active-path candidate** post-F1; D7 (external execution-cost evidence review) ranked rank-2; D8 (pause) ranked default-no-active-path. The Phase 3e remain-paused recommendation was over-ridden by Phase 3f operator brief authorizing active-path discovery. |
| **3g** | Docs-only D1-A spec memo + methodology sanity audit; 9 axes locked (\|Z_F\| ≥ 2.0; trailing 90 days / 270 events; 1.0 × ATR(20) stop; +2.0R target; 32-bar time-stop; per-funding-event cooldown; band [0.60, 1.80] × ATR; contrarian direction; no regime filter). Falsifiable mechanism predictions M1 (post-entry counter-displacement at h=32), M2 (funding-cost benefit), M3 (TARGET-subset positive contribution). |
| **3h** | Docs-only D1-A execution-planning memo; precommitted run inventory (4 mandatory R-window cells + 1 conditional V); first-execution gate definition (§11.1 conditions i–v + §11.2 verdict mapping; §10.4 catastrophic-floor predicate); timing-clarification amendments (TARGET completed-bar close confirmation + next-bar-open fill; funding-eligibility non-strict ≤). |
| **3i-A** | D1-A implementation-controls phase: D1-A self-contained module + primitives + locked `FundingAwareConfig` + `StrategyFamily.FUNDING_AWARE_DIRECTIONAL` + dispatch surface guard; **D1-A deliberately non-runnable** through engine guard. |
| **3i-B1** | D1-A engine-wiring phase: Phase 3i-A engine guard lifted; full per-bar `_run_symbol_d1a` lifecycle + `FundingAwareLifecycleCounters` event-level identity + 4 new TradeRecord D1-A fields + runner scaffold under Phase 3j hard guard; H0/R3/F1 controls bit-for-bit. |
| **3j** | D1-A first-execution: 4 mandatory R-window cells executed (D1-A R MED MARK, R LOW MARK, R HIGH MARK, R MED TRADE_PRICE); conditional V-window skipped (R-window not PROMOTE); §11.1 first-execution gate evaluated; M1/M2/M3 mechanism checks computed; §13 mandatory diagnostics produced; §14 P.14 hard-block invariants (4 categories) all PASS; **framework verdict: MECHANISM PASS / FRAMEWORK FAIL — other** (catastrophic-floor predicate NOT triggered). |

**D1-A arc outcome:** D1-A first-execution MECHANISM PASS / FRAMEWORK FAIL — other per Phase 3h §11.2. D1-A retained as research evidence; D1-A family research concluded as framework-failed under current locked spec. Phase 3j is terminal for D1-A; no D1-A-prime / D1-B / V1/D1 / F1/D1 hybrid is proposed.

---

## 4. Summary table of all major candidates

R-window evidence: 2022-01-01 → 2025-01-01, MEDIUM slippage, MARK_PRICE stop-trigger, locked Phase 2e v002 datasets, BTCUSDT primary, ETHUSDT comparison.

| Candidate | Phase | Mechanism tested | Strongest evidence | Failure mode | Final status | Changed baseline? | Retained research value |
|-----------|-------|------------------|--------------------|---------------|---------------|:-:|------------------------|
| **H0** | 2e | Locked V1 baseline (range setup; 1h binary slope-3 bias + EMA(50)/EMA(200) position; 0.10 × ATR breakout buffer; staged-trailing exit; 0.10 × ATR structural-stop buffer) | Foundational; bit-for-bit reproducible across 9+ phases through Phase 3j | BTC R-window expR=−0.459 / PF=0.255; ETH expR=−0.475 / PF=0.321 (aggregate negative); chop with repeated false breaks (V1 spec failure mode #1) | **Locked anchor** | N/A (H0 *is* the baseline) | **Foundational.** Sole §10.3 / §10.4 anchor for all V1-family candidates per Phase 2i §1.7.3. Defines the framework's reference point. |
| **R3** | 2l | Exit philosophy redesign (Fixed-R take-profit at +2.0 R + unconditional 8-bar time-stop; protective stop never moved intra-trade) | **Strongest single candidate** in the project. Improves expR in all 6 regime-symbol cells; 4/5 BTC + 3/5 ETH folds beat H0; first positive-expR BTC folds (F2, F3); cost-robust at HIGH; bit-identical MARK vs TRADE_PRICE; zero TRAILING_BREACH / STAGNATION leakage. BTC expR=−0.240 / PF=0.560; ETH expR=−0.351 / PF=0.474. | Aggregate edge still negative; PF<1 on both symbols ("less negative than H0" not "break-even"). | **PROMOTE — baseline-of-record** per Phase 2p §C.1 | **YES** | **Strongest single evidence in the project.** R3 is the deployable variant if and when operator policy authorizes paper/shadow / Phase 4. |
| **R1a + R3** | 2m | Setup-validity predicate (volatility-percentile, X=25 / N=200) on top of R3 | ETH V-window first-ever positive netPct (+0.69%); ETH low_vol PF 1.353 first cell with positive expR AND PF > 1; compression-selection mechanically correct (100% entries at percentile ≤ 25%). | BTC degraded vs R3 (Δexp_R3 −0.180 R; V-window 0% WR / 4 trades); BTC R-window expR=−0.420 / PF=0.355; ETH-favorable / BTC-degrading symbol asymmetry; ineligible under §1.7.3 BTCUSDT-primary lock without lock revision. | **mixed-PROMOTE; retained research evidence; non-leading** per Phase 2p §D | NO | Compression-mechanism evidence; ETH-favorability suggests symbol-conditional R1a-prime hypothesis territory. |
| **R1b-narrow + R3** | 2s | Bias-validity predicate (slope-strength magnitude S=0.0020) on top of R3 | Formal §10.3.a-on-both PROMOTE (first such); R-window BTC expR=−0.263 / PF=0.561; ETH expR=−0.224 / PF=0.622; cost-resilience holds at HIGH on both symbols. | 65–70% trade-count drop (R-window n=10 BTC / 12 ETH); R3-anchor near-neutral marginal contribution; small-sample caveats. | **PROMOTE / PASS-with-caveats; retained research evidence; non-leading** per Phase 2s §13 | NO | Bias-strength selectivity evidence; magnitude-threshold predicate concept available for future hypothesis development. |
| **R2 + R3** | 2w | Entry-lifecycle topology (pullback-retest with 8-bar validity window; 5-step precedence; fill-time stop-distance re-check) on top of R3 | MED-slip §10.3 PROMOTE on both symbols; M1 (pullback-mechanism) + M3 (filtered-trade-quality) mechanism support per Phase 2w §11.5 / §11.7; clean engine implementation. | **§11.6 HIGH-slip cost-sensitivity gate FAILS** on both symbols (BTC Δexp_H0 −0.014 sub-threshold; ETH Δexp_H0 −0.230 catastrophic). M2 (regime-decomposition) FAIL. The first §11.6 failure in the family arc. Slippage-fragile by construction. | **FRAMEWORK FAILED — §11.6 cost-sensitivity blocks; retained research evidence; non-leading** per Phase 2w §16.3 | NO | Pullback-mechanism evidence + slippage-fragility precedent. R2's failure motivated the Phase 3c §7.2(iv) BTC HIGH > 0 cost-resilience strengthening (preserved into Phase 3h §11.1 (iv) for D1-A). |
| **F1** | 3d-B2 | Mean-reversion-after-overextension as a separate strategy family: 8-bar cumulative displacement > 1.75 × ATR(20) → market-fill at next-bar open; SMA(8) frozen target; structural stop with 0.10 × ATR buffer; unconditional 8-bar time-stop; same-direction cooldown until unwind | M3 (TARGET-exit subset) PASS on both symbols: BTC mean +0.75 R / aggregate +1149 R; ETH mean +0.87 R / aggregate +1398 R. M1 BTC PARTIAL: fraction non-neg 55.4% (above 50%) but mean only +0.024 R (below +0.10 R threshold). | Catastrophic absolute-floor violations: BTC MED expR=−0.5227, BTC HIGH expR=−0.7000 / PF=0.2181, ETH HIGH expR=−0.5712 / PF=0.2997. M2 BTC FAIL. 4720 BTC + 4826 ETH trades over 36 months (~150× H0/R3); per-trade negative expR multiplied by trade volume produces catastrophic equity loss. | **HARD REJECT — first-execution gate; retained research evidence; non-leading** per Phase 3c §7.3; Phase 3d-B2 terminal for F1 | NO | TARGET-subset isolated profitability is mechanism-relevant evidence; the wider F1 strategy-as-specified is FAILED because STOP exits (53–54%) overwhelm the TARGET-exit positive contribution. |
| **D1-A** | 3j | Funding-aware directional / carry-aware contrarian: when trailing-90-day funding-rate Z-score \|Z_F\| ≥ 2.0 at completed funding-settlement time, enter contrarian (LONG below −2σ, SHORT above +2σ) at next 15m bar's open; stop = 1.0 × ATR(20); fixed +2.0R target; 32-bar (8-hour) unconditional time-stop; per-funding-event cooldown; band [0.60, 1.80] × ATR(20); no regime filter. | M1 (post-entry counter-displacement at h=32) BTC PASS: mean +0.1748 R AND fraction-non-negative 0.5101 — both above thresholds. The post-extreme-funding contrarian directional mechanism is empirically present. M3 (TARGET-exit subset) PASS on both symbols: BTC n=52, mean +2.143 R, aggregate +111.46 R; ETH n=49, mean +2.447 R, aggregate +119.89 R. Per-trade R magnitudes BETTER than Phase 3h §5.6.5 forecast (winners +1.98 R BTC / +2.26 R ETH vs +1.47 forecast; losers −1.30 R BTC / −1.24 R ETH vs −1.53 forecast). | BTC R MED MARK expR=−0.3217 / PF=0.6467 (cond_i FAIL); ETH R MED MARK expR=−0.1449 / PF=0.8297; BTC R HIGH MARK expR=−0.4755 / PF=0.5145 (cond_iv FAIL — cost-resilience). M2 FAIL on both symbols (BTC mean funding benefit +0.00234 R, ~21× below +0.05 R threshold; ETH +0.00452 R, ~11× below). Empirical win rate ~30% / ~31% vs forecast +51% breakeven (gap of ~21 percentage points). 198 BTC + 179 ETH trades over 36 months (~5× H0/R3, ~30× lower than F1). Catastrophic-floor predicate NOT triggered on any of 4 R-window cells × 2 symbols (all 8 satisfy expR > −0.50 AND PF > 0.30 simultaneously). | **MECHANISM PASS / FRAMEWORK FAIL — other; retained research evidence; non-leading** per Phase 3h §11.2; Phase 3j terminal for D1-A under current locked spec; no D1-A-prime / D1-B / hybrid authorized | NO | M1 directional-mechanism evidence + M3 TARGET-subset isolated profitability. Funding-extreme contrarian signal produces real but small post-entry directional drift insufficient to reach +2.0R target before 1.0 × ATR stop fires (~68% of trades). The mechanism exists; the locked geometry does not capture enough of it. |

---

## 5. D1-A-specific postmortem

### 5.1 Why D1-A was justified after F1

Phase 3f §6 / §7.1 / §8.1 ranked D1 as the rank-1 active-path candidate post-F1 on five distinct grounds:

1. **Mechanism complementarity with F1's documented failure mode.** F1's M2 BTC FAILED (chop-regime stop-out fraction was *higher* than H0, opposite of the Phase 3b §2.3 hypothesis). D1's funding-aware mechanism is structurally different from price-action-derived signals: extreme funding rates measure a directional / carry imbalance that price-only families (V1, F1) do not exploit. D1 explicitly addresses the F1 failure mode by sourcing the signal from a different information channel.
2. **Lowest expected cost-sensitivity profile among Phase 3f candidates.** D1's episodic frequency (extreme funding events occur roughly 1× per few days, not per bar) projects ~50–250 trades per symbol per R-window — orders of magnitude below F1's 4720+ — reducing the trade-frequency × per-trade-cost catastrophic aggregation pattern that drove F1's HARD REJECT.
3. **§1.7.3 BTCUSDT-primary alignment plausibility.** Phase 3a §4.6 / Phase 3f §7.1 noted BTC funding-rate magnitudes typically exceed ETH's on Binance USDⓈ-M, suggesting D1 should structurally favor BTC over ETH. (Empirically Phase 3j showed roughly symmetric BTC/ETH outcomes; the BTC-friendliness plausibility was not strongly validated, see §6.4 below.)
4. **v002 dataset sufficiency.** D1-A required only the existing v002 funding-rate dataset (already used as cost-component by V1 + F1 but never as primary signal). No v003 raw-data bump.
5. **Falsifiable mechanism predictions M1 / M2 / M3.** Phase 3g §10 + Phase 3h §12 operationalized D1's hypothesis as: M1 (post-entry counter-displacement at h=32 ≥ +0.10 R AND fraction ≥ 50% on BTC); M2 (funding-cost benefit mean ≥ +0.05 R per trade per symbol); M3 (TARGET-exit subset mean ≥ +0.30 R AND aggregate > 0 per symbol). All three predictions were testable on v002 data.

The Phase 3f → 3g → 3h → 3i-A → 3i-B1 → 3j sequence implemented this hypothesis under the same framework discipline that produced R3 / R1a / R1b-narrow / R2 / F1.

### 5.2 What D1-A proved mechanically

D1-A's M1 (post-entry counter-displacement at h=32 R, BTC) PASSES both conditions:

- BTC h=32 mean = +0.1748 R (above +0.10 R threshold).
- BTC h=32 fraction non-negative = 0.5101 (above 0.50 threshold).
- ETH h=32 mean = +0.1670 R, fraction = 0.5140 (descriptively also passes; only BTC drives §11.1 (ii)).

**The post-extreme-funding contrarian directional mechanism is empirically present at the 32-bar (8-hour) horizon.** When |Z_F| ≥ 2.0 at a funding-settlement time, the price *does* tend to revert against the funding extreme over the following 32 bars on both BTCUSDT and ETHUSDT. This is the first time in the Prometheus research arc that an M1-style post-entry directional drift mechanism has cleanly passed both threshold and fraction tests on BTC.

D1-A's M3 (TARGET-exit subset) PASSES decisively on both symbols:

- BTC TARGET subset: n=52, mean +2.143 R, aggregate +111.46 R.
- ETH TARGET subset: n=49, mean +2.447 R, aggregate +119.89 R.

Per-trade R magnitudes are BETTER than the Phase 3h §5.6.5 forecast on both winner and loser sides:

- BTC winners +1.979 R vs forecast +1.47 R.
- BTC losers −1.298 R vs forecast −1.53 R.
- ETH winners +2.256 R, losers −1.238 R (analogous improvements).

The geometry (1.0 × ATR stop + completed-bar-close TARGET trigger + next-bar-open fill) is delivering the per-trade R-multiples it was designed to deliver, with a small overshoot on TARGET-subset that reflects bar-close-trigger / next-bar-open fill mechanics (post-trigger bar's open puts fill above target on LONG / below target on SHORT).

### 5.3 Why D1-A failed as a full locked framework

Two structural reasons:

1. **The empirical win rate is far below the forecast breakeven WR.** Phase 3h §5.6.5 forecast a 51% breakeven WR at MED slippage given +1.47 R winners and −1.53 R losers. Empirically: BTC WR = 0.298, ETH WR = 0.313 — gap of ~21 / ~20 percentage points below breakeven. Even with BETTER-than-forecast per-trade R magnitudes, the realized-magnitude breakeven WR is `1.298 / (1.979 + 1.298) ≈ 0.396` on BTC — empirical WR is still 10 percentage points below this realized-magnitude threshold. The directional drift exists at h=32 (M1 PASS) but is too small relative to the 1.0 × ATR stop distance to consistently reach the +2.0 R target before the stop fires. Approximately 68% of D1-A trades exit on STOP at −1.30 R (BTC) / −1.24 R (ETH); only 26–27% reach TARGET.
2. **Cost-resilience fails at HIGH slippage.** BTC R HIGH MARK expR = −0.4755 (cond_iv `BTC HIGH expR > 0` FAILS). Cost-monotonicity is clean (BTC LOW −0.24 → MED −0.32 → HIGH −0.48) but the slope is steep enough that 8 bps HIGH per side pushes BTC near (but not into) the catastrophic-floor predicate. The §11.6 cost-sensitivity gate that has now repeatedly filtered candidates (R2 in Phase 2w; F1 catastrophically in Phase 3d-B2; D1-A non-catastrophically in Phase 3j) blocks D1-A's promotion despite the mechanism PASS.

**Crucially, D1-A does NOT trip the catastrophic-floor predicate** on any of the 4 R-window × 2 symbols cells. The non-catastrophic conjunction `expR > −0.50 AND PF > 0.30` holds on all 8. This is materially milder than F1's HARD REJECT (5 catastrophic violations across BTC/ETH × MED/HIGH). D1-A's framework failure is driven by the absolute-floor (cond_i: BTC MED expR > 0) and cost-resilience (cond_iv: BTC HIGH expR > 0 AND PF > 0.30) conditions, not the catastrophic floor.

### 5.4 Why M1 PASS is not sufficient to promote D1-A

Tempting interpretation: "M1 PASSES on BTC; the mechanism exists; D1-A should be promoted." This interpretation is **forbidden by Phase 3h §11 verdict mapping** for two reasons:

1. **The first-execution gate is a conjunction, not a disjunction.** §11.1 conditions (i) BTC MED expR > 0, (ii) M1 BTC h=32 PASS, (iii) ETH MED non-catastrophic, (iv) BTC HIGH cost-resilience, (v) MED absolute floors must ALL hold for a PROMOTE verdict. M1 (cond_ii) PASS is necessary but not sufficient. Cond_i and cond_iv FAILED on D1-A; the verdict mapping correctly classifies this as MECHANISM PASS / FRAMEWORK FAIL — other.
2. **Mechanism evidence is preserved as research evidence, not promotion authority.** The framework discipline explicitly distinguishes between "the mechanism the strategy claims to exploit empirically exists" (M1 PASS) and "the strategy as specified produces a positive aggregate edge" (cond_i / cond_iv PASS). R2's M1 + M3 PASS in Phase 2w + §11.6 FAIL is the precedent: M1 alone does not promote a candidate.

### 5.5 Why M3 TARGET-subset success is not sufficient to continue D1-A automatically

Tempting interpretation: "M3 PASSES; the +2.0 R target geometry IS profitable when isolated; just filter D1-A down to the TARGET-eligible subset." This interpretation is **forbidden by Phase 2j §C.6 / §11.3.5 single-spec discipline**, identical to the F1 §11.3.5 reasoning preserved into Phase 3h §15:

1. **Selecting the TARGET subset prospectively requires a new predicate that does not currently exist.** The TARGET subset is defined retrospectively (a trade that exited at TARGET); deciding *before entry* whether a fired entry will reach TARGET requires a new predicate that distinguishes target-eligible from non-target-eligible extreme-funding events. Such a predicate is not in the Phase 3g spec; constructing it post-hoc to "rescue" D1-A is precisely the §11.3.5 forbidden post-hoc loosening.
2. **F1's precedent confirms this rule.** F1's M3 PASSED in Phase 3d-B2; F1 was retained as research evidence with mechanism support but **not** continued as an F1-prime under §11.3.5. Phase 3e §5.4 framing established that "mechanism-supported subset" is research evidence, not promotion. D1-A inherits the same treatment exactly.
3. **The R2 → F1 → D1-A → "next-prime" chain risks unbounded post-hoc tuning under "research framing".** Each candidate that fails a framework gate but produces some isolated mechanism-supported subset could justify a "next variant" purely by carving out the subset. This is the treadmill risk Phase 2x §7.2 / Phase 2p §H.4 / Phase 3e §5.4 / Phase 3f §5.7 explicitly warned against. Phase 3j is the third consecutive instance where this rule applies; preserving it is now binding precedent.

**Therefore: D1-A's M3 PASS is recorded as research evidence only.** It is informative; it is not a license to authorize D1-A-prime. Any future D1-A-prime spec must come from an **independently developed operator-driven hypothesis** that is falsifiable, mechanism-grounded, and framework-discipline-compliant — not from "select the M3 subset and tune around it".

### 5.6 Why M2 funding-cost benefit failure matters

D1-A's M2 (funding-cost benefit) FAILS on both symbols by ~21× (BTC) and ~11× (ETH) below the +0.05 R threshold:

- BTC: mean funding_pnl / realized_risk_usdt = +0.00234 R per trade.
- ETH: mean funding_pnl / realized_risk_usdt = +0.00452 R per trade.

This matters for two reasons:

1. **The funding-aware-as-carry-discount sub-hypothesis is empirically falsified.** Phase 3f §7.1 / Phase 3g §5.6 entertained both a "contrarian directional" sub-hypothesis (entry triggered by extreme |Z_F|, profit driven by post-entry mean reversion) and a "cost-discount filter" sub-hypothesis (the contrarian position also collects favorable funding through the next funding cycle, providing a carry tailwind). The Phase 3g locked spec selected the contrarian-directional as primary but retained the carry-discount as a built-in benefit. Empirically, the carry-discount is roughly two orders of magnitude smaller than its claimed scale — most D1-A trades exit on STOP or TARGET within ≤ 32 bars (≤ 8 hours), so most trades cross at most one funding cycle, and the per-cycle accrual on a 0.25%-risk position is negligible.
2. **The "lower-cost-sensitivity than F1" plausibility from Phase 3f §7.1 is partially undermined.** D1-A is indeed less catastrophically cost-sensitive than F1 (no catastrophic-floor violation; LOW → HIGH delta of −0.23 R BTC vs F1's much larger gradient). But the carry component cannot offset fees + slippage in any meaningful sense; cost-resilience must be earned by per-trade R magnitude × WR, not by funding-carry pad. This narrows the design space for any hypothetical D1-A-prime: a successor variant cannot rely on funding carry to rescue cost-sensitivity.

### 5.7 Why no D1-A-prime, D1-B, V1/D1 hybrid, or F1/D1 hybrid should start without a separate operator decision

Per Phase 3h §15 and Phase 2f §11.3.5, Phase 3j's MECHANISM PASS / FRAMEWORK FAIL — other is the binding outcome. No automatic successor authorization follows. If the operator independently develops a falsifiable D1-A-prime / D1-B / V1/D1 / F1/D1 hypothesis (e.g., a regime-conditional |Z_F| threshold; a target-subset selection rule justified ex-ante; a fundamentally different funding-aware mechanism; a hybrid combining D1-A entries with V1's structural stop or F1's mean-reversion target), that hypothesis would require:

1. A separately-authorized Phase 3a-style discovery memo *or* directly a Phase 3b-style spec memo for the new hypothesis.
2. Phase 3c-style execution-planning.
3. Phase 3d-A-style implementation with locked config.
4. Phase 3d-B-style execution + first-execution-gate evaluation.

None of those phases is currently proposed. The operator decides whether and when any of them is authorized. Phase 3k does not propose a D1-A-prime / D1-B / hybrid phase.

### 5.8 Why D1-A is terminal under the current locked spec

D1-A's MECHANISM PASS / FRAMEWORK FAIL — other verdict applies to the locked Phase 3g spec axes verbatim. Under those axes (|Z_F| ≥ 2.0 / 270 events / 1.0 × ATR stop / +2.0 R target / 32-bar time-stop / per-funding-event cooldown / band [0.60, 1.80] × ATR / contrarian / no regime filter), the empirical evidence is:

- M1 mechanism PASS but post-entry drift magnitude (+0.17 R at h=32 BTC) is too small relative to the 1.0 × ATR stop distance.
- WR ~30% vs forecast 51% breakeven — STOP fires before target on roughly 68% of trades.
- M2 carry-discount negligible (~21× / ~11× below threshold).
- Cost-resilience fails at HIGH slippage on BTC (cond_iv FAIL).

**Phase 3j is therefore terminal for D1-A under the current locked spec.** Any further D1-A work would be either (a) repeating the same locked-spec runs (no new information would be obtained), or (b) modifying the spec axes (which requires a separately authorized phase per §5.7). Neither is currently proposed.

---

## 6. Cross-family diagnosis

What the project has now empirically learned across the V1 breakout + F1 mean-reversion + D1-A funding-aware three-arc evidence:

### 6.1 V1 breakout continuation (H0 / R3 / R1a / R1b-narrow)

**Status:** Demonstrated structural-redesign responsiveness; absolute-aggregate edge has not materialized.

- Two PROMOTE outcomes (R3 broad-based; R1b-narrow formal), one mixed-PROMOTE (R1a+R3), one framework-FAIL (R2). The family responds to disciplined structural redesign in a measurable way, but no candidate has produced positive aggregate net-of-cost expR on R-window.
- R3's improvements are real and broad-based but quantitatively bounded: BTC R-window expR=−0.240 (PF=0.560) versus H0=−0.459 (PF=0.255). R3 reduces the per-trade cost of being wrong by ~50% but does not flip the sign.
- The family operates within a regime-incompatibility constraint (chop / range-bound markets) that R3 partially mitigates but does not solve.

### 6.2 R2 — entry timing and cost fragility

**Status:** Pullback-retest entries are slippage-fragile by construction.

- The small post-pullback R-distance geometry amplifies per-trade cost. Pullback-retest is a known slippage-vulnerable entry shape; this lesson is preserved into the Phase 3c §7.2(iv) and Phase 3h §11.1 (iv) BTC HIGH > 0 cost-resilience strengthening.
- All subsequent entry-axis candidates must demonstrate cost-resilience at HIGH slippage; R2's framework-FAIL is the binding precedent.

### 6.3 F1 — high-frequency mean reversion and stop-out pressure

**Status:** The mean-reversion target exists (M3 PASS) but the wider strategy is not viable as specified.

- F1's TARGET-subset is profitable in isolation on both symbols; this is empirical evidence the SMA(8) mean-reversion target does fire and is cost-survivable on the trades that actually reach it.
- F1's wider strategy fails because (a) trade frequency is ~150× H0, (b) M1 magnitude (+0.024 R) is far below the +0.10 R PASS threshold, and (c) STOP exits (53–54%) overwhelm the TARGET-exit positive contribution.
- **Lesson:** High-frequency strategies amplify per-trade negative expR catastrophically. Trade-frequency × per-trade-expR is a binding aggregation discipline.

### 6.4 D1-A — funding extremes, weak but real directional mechanism, and insufficient win rate

**Status:** Directional mechanism (M1) and target geometry (M3) both PASS on BTC; full framework expectation fails on win rate and cost-resilience.

- D1-A's M1 BTC h=32 PASS is the **first M1-style mechanism PASS in the project on BTC**. Both threshold (mean +0.17 R ≥ +0.10 R) and fraction (0.51 ≥ 0.50) cleanly hold. The post-extreme-funding contrarian mechanism empirically exists on Binance USDⓈ-M BTCUSDT/ETHUSDT 15m data.
- D1-A's M3 TARGET-subset PASS is the **second M3 PASS** (after F1's M3 PASS), confirming the +2.0 R target is reachable when the directional drift is strong enough.
- The per-trade R magnitudes are BETTER than the Phase 3h §5.6.5 forecast (winners +1.98 R BTC vs +1.47 forecast; losers −1.30 R BTC vs −1.53 forecast). The geometry is delivering what it was designed to deliver.
- **The framework fails on win rate.** Empirical WR ~30% vs forecast 51% breakeven. The directional drift exists but is too small relative to the 1.0 × ATR stop to reach +2.0 R target most of the time within 32 bars.
- **The "BTC-friendly" plausibility is partially undermined.** Phase 3a §4.6 / Phase 3f §7.1 expected D1-A to favor BTC. Empirically the BTC vs ETH gap is small (BTC MED expR −0.32 vs ETH −0.14; ETH is *less bad*, not BTC), suggesting funding-rate magnitude alone is not a sufficient symbol-friendliness predictor.
- **The "low cost-sensitivity" plausibility is partially supported.** D1-A does not trip the catastrophic-floor predicate (unlike F1). But cost-resilience still fails at HIGH on BTC (cond_iv FAIL), indicating §11.6 = 8 bps HIGH remains a binding gate even for episodic-frequency strategies.

### 6.5 Cost sensitivity (cross-family)

**Status:** §11.6 = 8 bps HIGH per side is now the most consistent failure-mode signal in the project.

- Phase 2y closeout confirmed §11.6 = 8 bps HIGH (after analyzing R2's framework-FAIL at HIGH).
- The threshold has now successfully filtered R2 (MED PROMOTE / HIGH FAIL), F1 (catastrophic at HIGH), and D1-A (cond_iv FAIL at HIGH).
- The Phase 3c §7.2(iv) / Phase 3h §11.1 (iv) operator-mandated amendment ("BTC HIGH expR > 0") strengthens §11.6 for new-family first-execution gates. F1 + D1-A both demonstrate this strengthening was correctly motivated.
- **Cost-sensitivity is now the most consistent failure-mode signal in the project: R2, F1, and D1-A all failed §11.6 / cond_iv. Future strategy candidates must demonstrate cost-resilience at HIGH slippage; this is binding pre-execution discipline.**

### 6.6 Target-subset fallacy (cross-family)

**Status:** TARGET-subset isolated profitability is research evidence, not promotion authority.

- F1 M3 PASS + framework FAIL → research evidence only; no F1-prime.
- D1-A M3 PASS + framework FAIL → research evidence only; no D1-A-prime.
- Pattern: any strategy that produces a profitable TARGET-subset can claim "the target works"; the framework correctly distinguishes between "the target is reachable when reached" (M3) and "the target is reached often enough net-of-stops to produce positive aggregate" (cond_i / cond_iv).
- **Lesson:** Post-hoc selection of profitable subsets is forbidden by §11.3.5. Any prospective subset-selection predicate must come from an independently developed hypothesis, not from carving out a M3-passing subset.

### 6.7 BTC vs ETH asymmetry (cross-family)

**Status:** Symbol-specific market-structure effects are persistent across families; §1.7.3 BTCUSDT-primary lock remains correctly calibrated.

- Phase 2x §4.6 / Phase 2o §C diagnosed the V1 breakout-family BTC/ETH asymmetry as a fact about market structure: ETH produces sharper trending moves; BTC produces longer chop/range periods.
- F1 inverts the asymmetry plausibly per Phase 3a §4.1(h): F1 should structurally favor BTC over ETH. Empirically: F1 BTC MED expR=−0.5227 vs ETH=−0.4024 — ETH was *less bad* than BTC (the *opposite* of the plausibility claim).
- D1-A inverts the asymmetry plausibly per Phase 3a §4.6 / Phase 3f §7.1: BTC funding-rate magnitudes typically exceed ETH's. Empirically: D1-A BTC MED expR=−0.3217 vs ETH=−0.1449 — ETH again *less bad* than BTC.
- §1.7.3 BTCUSDT-primary lock is therefore not threatened by F1 or D1-A's results: BTC remains the harder symbol to crack edge on; ETH research-comparison evidence remains informative but not deployment-relevant.

### 6.8 Trade frequency and sample stability (cross-family)

**Status:** Episodic-frequency strategies (D1-A) preserve fold-level diagnostic resolution better than high-frequency strategies (F1) but do not by themselves rescue framework outcomes.

- H0 / R3 / R1a / R1b-narrow / R2 produce 22–33 R-window trades per symbol — small samples; fold-level resolution limited.
- F1 produces 4720+ R-window trades per symbol — large samples; per-trade negative expR catastrophic in aggregate.
- D1-A produces ~180–200 R-window trades per symbol — middle ground; per-fold heterogeneity visible (BTC F3 2023H1 +0.62 R / F5 2024H1 −0.98 R; ETH similar pattern).
- D1-A's per-fold heterogeneity is informative for stationarity analysis: only 1 of 6 BTC folds (F3 2023H1) is profitable; only 2 of 6 ETH folds. The strategy does not robustly produce positive expected R across half-year folds in the R window. This is a strong negative signal for stationarity but cannot be addressed within the locked spec.
- **Lesson:** Sample size matters for diagnostic quality but does not by itself produce positive aggregate edge. D1-A's middle-ground trade-count gives sharper diagnostics than V1-family small-sample candidates while avoiding F1's catastrophic-frequency aggregation; the diagnostic clarity is a research benefit, not a deployment benefit.

---

## 7. State of the research program

**Recommendation: YES — the active research program should pause / reset (again).**

Phase 3e already recommended remain-paused after F1's HARD REJECT. Phase 3f operator brief over-rode that recommendation by authorizing active-path discovery, which produced D1 / D7 / D8 ranking and led to Phase 3g–3j. The Phase 3j outcome (MECHANISM PASS / FRAMEWORK FAIL — other) is materially milder than F1 but still framework-fail, and three independent reasons now compound for the second pause recommendation:

1. **The three-arc evidence pattern is consistent.** V1 breakout family is at its useful ceiling under the current framework (Phase 2x). Two new-family candidates (F1, D1-A) framework-failed under disciplined research. **Both new-family candidates were Phase 3a / Phase 3f rank-1 picks**; the project has now executed both available "best-near-term" candidates and both have failed. The pattern suggests that **identifying a positive-aggregate-edge strategy under the current framework + locks + thresholds + costs requires either a fundamentally different framework (e.g., regime-first decomposition; ML-feature-engineering with explicit leakage controls) or external evidence justifying revised thresholds, not another rank-2 candidate variant**.
2. **Treadmill risk is now elevated for the second time, not merely present.** Phase 2x §7.2 flagged treadmill risk after R2's failure. Phase 3d-B2 confirmed it (F1 HARD REJECT). Phase 3j now confirms it again (D1-A FRAMEWORK FAIL). Authorizing another rank-3+ family variant or another spec-writing phase without a strong independently-developed hypothesis risks producing a third framework-fail outcome that does not advance the strategic question. The right response to repeatedly elevated treadmill risk is to **pause and let the operator strategically choose**, more strongly than after Phase 3e.
3. **No specific candidate is currently specified.** Phase 3a / Phase 3f menus together identified D2–D6 (volatility contraction redesigned; trend pullback avoiding R2 fragility; range-bound; BTC/ETH relative strength; regime-first framework). Phase 3f §8.3 ranked D2 / D4 / D6 / D5 / D3 below D7 / D8 for documented reasons (overfitting; entry-geometry not currently designed; F1-shape cost-sensitivity risk; §1.7.3 lock-blocked; Phase 4 dependence). Authorizing D2–D6 without operator-driven hypothesis-development would be exactly the "spec-writing under research framing" Phase 2p §H.4 / Phase 3e §8.2 explicitly do not authorize.

The pause is **not** abandonment:

- R3 stays usable as a deployable variant if and when operator policy authorizes paper/shadow / Phase 4.
- R1a / R1b-narrow / R2 / F1 / D1-A stay as research evidence; their findings inform any future hypothesis-development phase.
- §11.6 = 8 bps HIGH stays as the framework's cost-resilience gate.
- The operator may at any future time independently develop a falsifiable hypothesis and authorize a downstream docs-only phase to evaluate it.

The pause is **operator-strategic**: it surrenders the question "what to research next?" to operator decision, more strongly than Phase 3e because the empirical evidence for treadmill risk is now stronger.

---

## 8. Operator decision menu

Eight options enumerated below. Each option's evaluation is preserved in the same shape Phase 2x §7 / Phase 3a §6 / Phase 3e §8 / Phase 3f §7 used.

### 8.1 Option A — Remain paused / research reset

**What it would answer:** What state should the project be in while the operator decides the next strategic move?

**Why it may be useful:**

- Preserves all current evidence as-is: R3 baseline-of-record; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence; §11.6 = 8 bps HIGH preserved; §1.7.3 locks preserved.
- Eliminates treadmill risk completely.
- Surrenders strategic direction to operator authority, where it belongs.
- Compatible with all subsequent options (B, C, D, E, F, G, H all remain available later).

**Why it may be dangerous:**

- Project loses momentum; strategic clarity may degrade if pause is indefinite.
- Operator may implicitly drift toward "I'll get back to it" without ever authorizing the next move.
- Phase 3e already recommended remain-paused; recommending it again risks looking like indecision rather than discipline. (Counter: the empirical evidence for pause is stronger after Phase 3j than after Phase 3d-B2.)

**Violates current restrictions?** No.

**Should be recommended now?** **YES — primary recommendation, candidate 1 of 3 acceptable Phase 3k recommendations.** This is the disciplined response to the three-arc evidence pattern.

### 8.2 Option B — External execution-cost evidence review (docs-only)

**What it would answer:** Are the current §11.6 = 8 bps HIGH-slippage assumption and the canonical taker fee rate (0.0005) calibrated correctly against current Binance USDⓈ-M live execution costs?

**Why it may be useful:**

- §11.6 has now successfully filtered three candidates (R2, F1, D1-A); cost-sensitivity is the most consistent failure-mode signal in the project. The repeated incidence makes external cost-evidence verification more important than after a single failure.
- Phase 2y closeout preserved §11.6 = 8 bps "until external execution-cost evidence justifies revision". Three subsequent failures (one catastrophic, two non-catastrophic) under that threshold provide additional motivation to verify (not loosen) the threshold.
- External cost-evidence review is purely external to the strategy research; it does not authorize any strategy work.
- The verification can equally well CONFIRM §11.6 = 8 bps as the realistic value, in which case it strengthens future framework-fail verdicts (rather than re-opening them).

**What evidence would be useful (per Phase 3k brief §10):**

- Realistic Binance USDⓈ-M taker / maker fee schedules (current vs Phase 2y baseline; tier-dependence; fee-rebate schedules).
- Spread / slippage observations on BTCUSDT / ETHUSDT 15m timescale and at funding-settlement boundaries (relevant to D1-A's entry timing).
- Order book depth at typical Phase 3j position-size scales (~$500 notional at 0.25% risk × $10K equity).
- MARK-vs-TRADE-PRICE stop-trigger behavior under intrabar wick conditions (Phase 3j §8.6 already showed this matters; external evidence would calibrate the gap).
- Latency and fill assumptions (next-bar-open fill realism; partial-fill handling; queue position effects).

**Why it may be dangerous:**

- **Risk of being misinterpreted as "find a way to pass §11.6 by lowering the threshold".** This would be exactly the §11.3.5 forbidden post-hoc loosening. Cost-policy revision must be **independent** of any specific candidate's framework outcome. The external review must be authorized with explicit ex-ante operator commitment that "the outcome could go either way; revision is not the goal".
- Even if external evidence justifies relaxing §11.6, it would not retroactively rescue R2, F1, or D1-A; all three are framework-FAILED under the rules in place at execution time.
- Risk of conflating "cost-evidence review" with "cost-evidence-driven candidate rescue". Phase 3e §8.5 previously declined to recommend Option E (then-named) because §11.6 = 8 bps preservation was recent and no fresh external trigger was asserted. Phase 3j now provides an arguable trigger (the third consecutive cost-sensitivity-related failure) but the §11.3.5 caution is unchanged.

**Violates current restrictions?** No (external evidence gathering is docs/research).

**Should be recommended now?** **YES — secondary recommendation, candidate 2 of 3 acceptable Phase 3k recommendations.** Acceptable if and only if authorized with explicit ex-ante operator commitment to symmetric-outcome discipline. Phase 3k's recommendation framing in §12 below clarifies the conditional nature.

### 8.3 Option C — Regime-first research framework memo (docs-only)

**What it would answer:** Is the regime-first framework approach (decomposing the market into discrete regimes and selecting / sizing strategies conditional on regime, rather than applying one strategy across all regimes) the right framework-level shift after the three-arc evidence?

**Why it may be useful:**

- Repeated mechanism-pass / framework-fail outcomes (R2 M1+M3 PASS / §11.6 FAIL; F1 M3 PASS / catastrophic floor; D1-A M1+M3 PASS / cond_i+cond_iv FAIL) strongly suggest that the *mechanism* exists in some regimes but not in others. Single-regime strategies pay STOP costs in unfavorable regimes that overwhelm TARGET gains in favorable regimes.
- D1-A's per-fold heterogeneity is the clearest project-level signal: BTC F3 2023H1 +0.62 R (PF 2.03; profitable); BTC F5 2024H1 −0.98 R (PF 0.16; catastrophic-fold). If the strategy were regime-conditioned to fire only in F3-like regimes, the M1 + M3 mechanism evidence might compose into framework-PASS.
- A regime-first framework is methodologically distinct from any specific strategy family; it does not violate the §11.3.5 single-spec discipline because regime classification is an ex-ante predicate, not a retrospective subset filter.
- Phase 3a §6.7 / Phase 3f §7.3 ranked F7 / D3 (regime-first) below F1 / D1 because of (a) implementation complexity, (b) dependence on Phase 4 runtime / state / persistence work for live regime tracking, (c) circular-reasoning risk if regime is defined post-hoc to fit known good cells.

**Why it may be dangerous:**

- **High overfitting / circular-reasoning risk.** If "regime" is defined post-hoc to fit the per-fold cells where existing candidates worked, the framework collapses to retrospective subset selection in disguise. Disciplined regime-first work requires regime classification developed from first principles (e.g., volatility-quantile + trend-strength + funding-rate level as orthogonal axes) BEFORE conditioning any strategy on it.
- **Phase 4 dependence.** Live regime tracking requires runtime / state / persistence work currently not authorized. A docs-only regime-first memo can specify the framework but not test it without backtest infrastructure. Phase 3k brief constraints prohibit that backtest infrastructure work.
- **Implementation complexity is high.** A regime-first framework changes how all candidates (V1 / F1 / D1-A retained evidence) are evaluated; existing PROMOTE / FAIL verdicts may need to be re-stated within the regime-decomposition framing.
- **Risk of becoming the next rank-1 candidate that framework-fails.** If a regime-first family is specified and tested under the current §11.6 / §1.7.3 / §10.4 discipline, it could produce a fourth framework-fail (cond_i / cond_iv / catastrophic-floor) outcome under the same pattern that filtered F1 and D1-A.

**What a docs-only regime-first memo would investigate (per Phase 3k brief §11):**

- Regime classification axes (volatility-quantile; trend-strength; funding-rate level; market-microstructure shifts) and their orthogonality.
- Per-regime expected behavior of V1 / R3 / F1 / D1-A retained-evidence candidates (which regime would each candidate's mechanism plausibly favor?).
- Statistical-power requirements (per-regime sample size on R-window v002 datasets; whether v002 has enough data per regime).
- Anti-circular-reasoning discipline (regime classification must be developed BEFORE seeing per-regime outcomes; §11.3.5 analogue).
- Implementation surface estimate (would require new regime-classification module; per-regime engine dispatch; per-regime accounting).
- Live-readiness implications (requires Phase 4 runtime work for live regime tracking; out of Phase 3k scope to authorize).

The memo would NOT implement, backtest, or test the framework. Phase 3k brief constraints prohibit any of those.

**Violates current restrictions?** No (a docs-only memo is on the same boundary as Phase 3a / 3f / 3g spec / discovery memos).

**Should be recommended now?** **YES — tertiary recommendation, candidate 3 of 3 acceptable Phase 3k recommendations.** Acceptable if and only if authorized with explicit ex-ante operator commitment to anti-circular-reasoning discipline. See §12 for the conditional framing.

### 8.4 Option D — New strategy-family discovery memo (docs-only, Phase 3a-style)

**What it would answer:** Among non-V1, non-F1, non-D1-A strategy families, which is the strongest candidate for any potential next research arc?

**Why it may be useful:**

- Phase 3a's eight-candidate menu had F1 (failed) and Phase 3f's seven-candidate menu had D1 (failed). Five remaining non-failed candidates exist conceptually (D2 volatility contraction redesigned; D3 regime-first framework; D4 trend pullback avoiding R2 fragility; D5 BTC/ETH relative strength; D6 range-bound).
- A fresh discovery memo could re-rank these in light of D1-A's framework-fail and the Phase 3j mechanism findings.
- Disciplined entry path (docs-only survey before any spec-writing).

**Why it may be dangerous:**

- Repeats the Phase 3a → 3b → 3c → 3d sequence twice (F1 then D1-A) for a third candidate; commits the project to another full F1/D1-A-shape research arc which may again framework-fail under §11.6 / cond_i / cond_iv discipline.
- **Phase 3f §8.3 already classified D2 / D4 / D6 / D5 / D3 with various near-term restrictions:** D2 has overfitting risk; D4 has no specific entry-geometry redesign; D6 has F1-shape cost-sensitivity risk; D5 is §1.7.3-blocked; D3 has Phase 4 dependence. The candidates ranked below D1 may be *less* near-term suitable than D1, not equivalently — Option D risks producing another framework-fail outcome with weaker prior plausibility than D1 had.
- Treadmill risk is now elevated for the second time (after Phase 3d-B2 + Phase 3j); authorizing Option D without operator hypothesis-development would be exactly the post-Phase-3d-B2 / post-Phase-3j treadmill that Phase 2x §7.2 / Phase 3e §8.2 / Phase 3f §5.7 warned against.

**Violates current restrictions?** No (a discovery memo is docs-only; Phase 3k itself is the same shape).

**Should be recommended now?** **NO.** Better deferred until the operator independently determines a non-V1, non-F1, non-D1-A hypothesis is worth surveying. Authorizing Option D now without operator hypothesis-development would be exactly the post-Phase-3j treadmill the §11.3.5 / §5.7 discipline warns against.

### 8.5 Option E — ML feasibility memo (docs-only, leakage-focused)

**What it would answer:** Could machine-learning techniques (feature engineering; supervised classification of bar-level entry quality; reinforcement-learning policy optimization) produce a positive-aggregate-edge strategy under the same Phase 2f / §1.7.3 / §11.6 discipline that filtered V1-family + F1 + D1-A?

**Why it may be useful:**

- ML methods can in principle exploit non-linear feature interactions that rule-based strategies (V1 / F1 / D1-A) cannot capture. The three-arc evidence shows mechanisms exist (R2 M1+M3, F1 M3, D1-A M1+M3) but the LOCKED rule-based geometry does not capture enough of them. ML could in principle pick up the residual signal.
- Feature engineering on v002 datasets (price-action features; ATR-derived features; funding-rate features; 1h bias features; per-fold regime features) is non-trivial and could surface predictive structure not currently exploited.
- Phase 3a §4.8 ranked F8 (ML-assisted forecasting) as eighth (last) for documented reasons; but the post-D1-A evidence pattern strengthens the argument that rule-based redesign within current discipline is hitting a ceiling.

**Why it may be dangerous (per Phase 3k brief §9):**

- **Leakage risk is severe.** ML feature engineering on financial time series has well-documented leakage failure modes: future-knowledge in training-set targets; cross-fold contamination via shared market events; per-asset shared regime structure; lookahead in normalization / scaling; survivorship in dataset construction. A single overlooked leakage source can invalidate the entire model evaluation.
- **Overfitting risk is severe.** v002 R-window has ~36 months of 15m + 1h data per symbol. With high-dimensional feature spaces, the effective sample size relative to feature count produces high overfitting variance. Cross-validation under stationarity assumptions may not hold (Phase 3j showed D1-A per-fold heterogeneity is large).
- **Small sample size relative to feature engineering ambition.** The R-window has ~50,000 bars per symbol per timeframe; mature ML pipelines for financial forecasting typically need decades of data or many cross-sectional symbols. Prometheus has 2 symbols and 36 months training data.
- **Non-stationarity.** Phase 3j per-fold heterogeneity (BTC F3 2023H1 +0.62 R / F5 2024H1 −0.98 R) is direct evidence that the underlying data-generating process is not stationary across the R-window. Standard ML assumes stationary feature distributions; this is empirically false on Prometheus's data.
- **Cost sensitivity may not be improved by ML.** ML models do not lower fees / slippage; they only reshape the entry / exit signal. If §11.6 filtered R2 / F1 / D1-A on cost-sensitivity, an ML model with similar signal frequency could fail the same gate. Cost-sensitivity is independent of model complexity.
- **Explainability.** Phase 2f / Phase 2i discipline requires falsifiable mechanism predictions (M1 / M2 / M3); rule-based strategies satisfy this by construction. ML models (especially gradient-boosting, neural networks) do not satisfy mechanism-falsifiability without additional explainability work (SHAP; permutation importance; counterfactual analysis). Without it, an ML PROMOTE / FAIL verdict cannot be evaluated under the existing framework.

**If ML is considered later, the safe first step is a docs-only ML feasibility memo, not model training.** The memo would investigate:

- Leakage controls for v002 data (strict purged + embargoed cross-validation; per-fold splits aligned to R-window structure; no future-knowledge in targets; explicit feature-engineering audit).
- Effective sample-size analysis (ratio of sample size to candidate feature count; degrees-of-freedom budget for any candidate model class).
- Stationarity testing (per-fold feature-distribution shift; per-regime label-distribution shift; rolling-window evaluation).
- Cost-sensitivity integration (any ML signal must demonstrate cost-resilience at HIGH slippage in expectation; not retrospectively).
- Explainability requirements (model-class restrictions; falsifiable mechanism prediction analogues to M1 / M2 / M3).
- Implementation surface estimate (would require new ML pipeline + new training/evaluation infrastructure + leakage audit; significant beyond current scope).

**ML is NOT an immediate escape hatch after D1-A failure.** A poorly-disciplined ML attempt could produce a fourth framework-fail in shorter time than V1/F1/D1-A took, or worse, could produce an apparent PROMOTE that is actually a leakage artifact.

**Violates current restrictions?** No (a docs-only feasibility memo is on the same boundary as Phase 3a / 3f / 3g / 3k memos).

**Should be recommended now?** **NO.** Premature without operator-developed hypothesis or strong external trigger. ML feasibility may be a legitimate operator-driven decision in the future but is not the disciplined response to Phase 3j's framework-fail. Phase 3k recommends Option A (pause) or Options B / C as more disciplined immediate next steps.

### 8.6 Option F — D1-A-prime / D1-B / V1/D1 hybrid / F1/D1 hybrid hypothesis planning

**What it would answer:** Could a regime-conditional D1-A-prime spec, a different funding-aware mechanism (D1-B), a V1/D1 hybrid (D1-A entries combined with V1 trend filter or V1 sizing), or an F1/D1 hybrid (D1-A entries combined with F1 mean-reversion target) rescue D1-A's M1 + M3 PASS evidence into a framework-PASSING strategy?

**Why it may be useful:**

- D1-A's M1 + M3 PASS is empirically informative (mechanism + target geometry both work). If a falsifiable, mechanism-grounded, framework-discipline-compliant hypothesis can construct an ex-ante regime-conditioning predicate or a fundamentally different funding-aware geometry, the M1 + M3 evidence becomes potentially developable.

**Why it may be dangerous:**

- §5.7 above explains why this is forbidden under §11.3.5 single-spec discipline: "select the M3 subset and tune around it" is exactly post-hoc loosening. Any D1-A-prime / D1-B / hybrid spec must come from independently developed operator hypothesis, not from carving out D1-A's profitable subset or combining it with previously-failed families.
- **Hybrid families risk inheriting both parents' failure modes.** V1/D1 hybrid would combine V1's chop regime-incompatibility + D1-A's WR insufficiency. F1/D1 hybrid would combine F1's high-frequency cost-aggregation + D1-A's WR insufficiency. The hybrid combinatorics suggest more, not fewer, failure modes.
- Treadmill risk: each post-hoc subset-rescue or hybrid-construction attempt invites the next. The discipline that produced clean PROMOTE / FAIL decisions on R3 / R1a / R1b-narrow / R2 / F1 / D1-A depends on resisting subset-rescue and hybrid-construction framing.
- No specific D1-A-prime / D1-B / hybrid hypothesis is currently developed by the operator. Authorizing the planning phase without a hypothesis is "spec-writing under research framing".

**Violates current restrictions?** **YES — Phase 3k brief constraint:** "Do not authorize D1-A-prime. Do not authorize D1-B. Do not authorize V1/D1 or F1/D1 hybrids." Strict reading: this option violates the brief.

**Should be recommended now?** **NO. Forbidden by Phase 3k brief.** D1-A-prime / D1-B / hybrid planning is reserved for a separately-authorized future operator decision with an independently-developed hypothesis.

### 8.7 Option G — R3 paper/shadow or Phase 4 governance discussion

**What it would answer:** What would the operator need to decide / verify / build before authorizing a paper/shadow or Phase 4 phase on the existing R3 baseline-of-record?

**Why it may be useful:**

- R3 is the baseline-of-record per Phase 2p §C.1 and is the strongest single evidence the project has. If the operator wants to make any move toward eventually deploying R3, the gating questions (paper/shadow scope; Phase 4 runtime/state/persistence implementation; operator readiness; production-key timing; NUC / dashboard / alert-route readiness; backup/restore readiness) need to be enumerated.

**Why it may be dangerous:**

- Conflating "governance discussion" with "implementation authorization" risks accidentally drifting toward Phase 4 work without the explicit phase-gate approval Phase 2p §H.4 / Phase 2x §7.4 require.
- R3's per-trade negative aggregate edge (BTC R-window expR=−0.240 / ETH=−0.351) means paper/shadow on R3 would expect to lose money cleanly; R3 is "less negative than H0" not "break-even". Deployment on R3 would convert "reduced losses" into real losses unless the regime-incompatibility resolves out-of-sample.

**Violates current restrictions?** **YES — Phase 3k brief constraint:** "Do not start paper/shadow planning. Do not start Phase 4. Do not start live-readiness or deployment work." A governance discussion is on the boundary; even at "review the existing pre-conditions catalog" interpretation, it crosses the brief's "Do not start paper/shadow planning" line.

**Should be recommended now?** **NO. Forbidden by Phase 3k brief.** Operator policy continues to defer paper/shadow indefinitely.

### 8.8 Option H — Stop active strategy research for now

**What it would answer:** Should the project stop all active strategy-research work indefinitely?

**Why it may be useful:**

- Strongest possible signal that strategic direction is operator-driven from this point forward.
- Eliminates treadmill risk completely.
- Makes the eventual return-to-research conscious and operator-developed.

**Why it may be dangerous:**

- Effectively the same as Option A (remain paused) but framed more strongly. The functional difference is whether the project state is "paused, awaiting operator decision" (Option A) versus "stopped, awaiting operator restart" (Option H).
- "Stop indefinitely" framing may inadvertently signal that the existing R3 / H0 / F1 / D1-A evidence is stale or invalidated, which is not the case.

**Violates current restrictions?** No.

**Should be recommended now?** **NO** — Option A's pause framing is operationally equivalent and less rhetorically strong. Option H is functionally a stronger version of Option A; both can be revisited if the operator wants to make the stop more explicit later.

### 8.9 Decision menu summary

| Option | Description | Violates Phase 3k brief? | Recommended now? |
|--------|-------------|:-:|:-:|
| **A** | Remain paused / research reset | NO | **YES (primary)** |
| **B** | External execution-cost evidence review (docs-only) | NO | **YES (secondary, conditional)** |
| **C** | Regime-first research framework memo (docs-only) | NO | **YES (tertiary, conditional)** |
| D | New strategy-family discovery memo (docs-only) | NO | NO |
| E | ML feasibility memo (docs-only, leakage-focused) | NO | NO |
| F | D1-A-prime / D1-B / V1/D1 / F1/D1 hybrid hypothesis planning | YES | NO (forbidden) |
| G | R3 paper/shadow or Phase 4 governance discussion | YES | NO (forbidden) |
| H | Stop active strategy research | NO | NO (Option A operationally equivalent) |

---

## 9. ML-specific discussion

ML methods are a legitimate long-term research direction for Prometheus but are **not justified as the immediate next docs-only phase** after Phase 3j's framework-fail. The reasons are documented above in §8.5; they are summarized here for emphasis:

- **ML is not an immediate escape hatch after D1-A failure.** A poorly-disciplined ML attempt could produce a fourth framework-fail in shorter time than V1/F1/D1-A took, or worse, could produce an apparent PROMOTE that is actually a leakage artifact.
- **The risks are severe and well-documented:** leakage (especially time-series target leakage); overfitting (high-dimensional feature spaces vs ~50K bars per symbol); small effective sample size (2 symbols × 36 months R-window); non-stationarity (per-fold heterogeneity already empirically observed in Phase 3j); cost sensitivity (ML signal frequency does not lower fees/slippage); explainability (mechanism-falsifiability discipline not satisfied by default).
- **If ML is considered later**, the safe first step is a docs-only ML feasibility memo focused on (1) leakage controls, (2) effective sample-size analysis, (3) stationarity testing, (4) cost-sensitivity integration, (5) explainability requirements, (6) implementation surface estimate. The memo would NOT train any model, run any backtest, or build any ML pipeline.
- **The operator decides whether and when an ML feasibility memo is authorized.** Phase 3k does not propose one; it documents the constraints under which one would be acceptable.

ML feasibility is reserved for a separately-authorized future operator decision with an independently-developed motivation that addresses the leakage / overfitting / non-stationarity / cost-sensitivity / explainability concerns ex-ante.

---

## 10. External execution-cost discussion

External execution-cost evidence review (Option B above) is the most disciplined option available for an active next docs-only step, IF the operator prefers an active path over remain-paused.

**Why repeated cost-sensitivity issues make external cost evidence important:**

- §11.6 = 8 bps HIGH per side has now successfully filtered THREE candidates (R2 in Phase 2w; F1 in Phase 3d-B2; D1-A in Phase 3j). The threshold is the most consistent failure-mode signal in the project.
- The Phase 2y closeout preserved §11.6 = 8 bps "until external execution-cost evidence justifies revision". Three subsequent failures provide additional motivation to verify (not loosen) the threshold against current Binance USDⓈ-M live execution costs.
- External evidence may CONFIRM 8 bps (in which case future framework-fail verdicts are strengthened), revise it slightly upward (which would produce more framework-fails, not fewer), or revise it slightly downward (which would re-open R2 / F1 / D1-A re-evaluation under new thresholds — but only as research evidence, not as automatic candidate rescue).

**External cost review must NOT loosen §11.6 automatically:**

- §11.3.5 forbids post-hoc threshold loosening to rescue specific candidates. The external review must be authorized with explicit ex-ante operator commitment to "the outcome could go either way; revision is not the goal".
- Cost-policy revision is **independent** of any specific candidate's framework outcome. Even if external evidence justifies relaxing §11.6, R2 / F1 / D1-A remain framework-FAILED under the rules in place at execution time. Re-evaluating those candidates under revised thresholds would itself require a separately authorized phase.
- External cost evidence must be applied symmetrically: confirming evidence STRENGTHENS framework-fail verdicts; revising evidence (in either direction) requires ex-ante symmetric-outcome commitment.

**What evidence would be useful (per Phase 3k brief §10):**

1. **Current Binance USDⓈ-M taker / maker fees.** Tier-dependent fee schedule at typical Phase 3j operator-account-tier scales (~$10K equity); fee-rebate schedules; BNB-discount applicability.
2. **Spread / slippage observations.** BTCUSDT / ETHUSDT 15m timescale; at funding-settlement boundaries (relevant to D1-A's entry timing); at typical R-window volatility regimes.
3. **Order book depth.** At typical Phase 3j position-size scales (~$500 notional); time-of-day effects; pre/during/post funding-settlement effects.
4. **MARK-vs-TRADE-PRICE stop-trigger behavior.** Phase 3j §8.6 already showed MED MARK vs MED TRADE_PRICE produces ~−0.05 R difference on BTC and ~−0.08 R on ETH; external evidence would calibrate the gap against live wick behavior.
5. **Latency and fill assumptions.** Next-bar-open fill realism (the Phase 3g + Phase 3h timing-clarification amendments assume next-bar-open fills are achievable; live evidence would test this); partial-fill handling; queue position effects at small notional.

**Why this may be the safest next research step:**

- Genuinely informative regardless of outcome.
- Does not authorize any strategy work; cannot accidentally drift into implementation / paper-shadow / Phase 4.
- Strengthens framework discipline rather than loosening it (when authorized with symmetric-outcome commitment).
- Is logically prior to any future strategy candidate — calibrating §11.6 against current realism is foundational regardless of which next candidate (if any) the operator eventually authorizes.

This option is recommended as the secondary candidate for Phase 3k's next-decision recommendation.

---

## 11. Regime-first framework discussion

Regime-first framework (Option C above) is the third disciplined option available for an active next docs-only step, IF the operator prefers a methodological framework reset over either remain-paused or external-cost-evidence verification.

**Why repeated mechanism-pass / framework-fail outcomes suggest regime diagnosis may be needed:**

- R2 M1 + M3 PASS / §11.6 FAIL → the pullback mechanism exists but cost-resilience fails uniformly across regimes.
- F1 M3 PASS / catastrophic floor → the mean-reversion target exists but is overwhelmed by aggregate STOP rate.
- D1-A M1 + M3 PASS / cond_i + cond_iv FAIL → the contrarian-after-extreme-funding mechanism exists but win rate is insufficient uniformly.

The pattern suggests that the *mechanism* may exist in some regimes (where M1 / M3 contribute positively) but not in others (where STOPs dominate and aggregate fails). A single-regime strategy pays STOP costs in unfavorable regimes that overwhelm TARGET gains in favorable regimes.

D1-A's per-fold heterogeneity (§6.8) is the clearest project-level signal for regime-conditional behavior:

- BTC F3 2023H1 +0.62 R (PF 2.03; profitable) — only profitable BTC fold.
- BTC F5 2024H1 −0.98 R (PF 0.16; catastrophic-fold) — worst BTC fold.
- BTC F1 2022H1 −0.94 R (also catastrophic-fold).
- BTC F4 2023H2 −0.40 R; BTC F6 2024H2 −0.05 R; BTC F2 2022H2 −0.13 R (intermediate).

If the strategy were regime-conditioned to fire only in F3-like regimes, the M1 + M3 mechanism evidence might compose into framework-PASS — but only if the regime classification is developed from first principles BEFORE conditioning any strategy on it.

**What a docs-only regime-first memo would investigate (per Phase 3k brief §11):**

1. **Regime classification axes.** Volatility-quantile (rolling realized vol percentile); trend-strength (1h slope-3 magnitude); funding-rate level (rolling Z); market-microstructure shifts (BTC / ETH spread dynamics; depth shifts). Their orthogonality (correlation matrix).
2. **Per-regime expected behavior of retained-evidence candidates.** Which regime would each of V1 / R3 / F1 / D1-A's mechanisms plausibly favor? (E.g., V1 trend-strong + low-vol; F1 high-vol after expansion; D1-A funding-extreme + range-bound.)
3. **Statistical-power requirements.** Per-regime sample size on R-window v002 datasets; whether v002 has enough data per regime; confidence-interval analysis for per-regime expR estimates.
4. **Anti-circular-reasoning discipline.** Regime classification must be developed BEFORE seeing per-regime outcomes. The §11.3.5 analogue: "no post-hoc regime-definition loosening to fit known good cells".
5. **Implementation surface estimate.** Would require new regime-classification module; per-regime engine dispatch; per-regime accounting; per-regime first-execution gate evaluation. Significant scope expansion vs current engine.
6. **Live-readiness implications.** Live regime tracking requires Phase 4 runtime / state / persistence work currently not authorized. The memo can specify the framework but cannot validate it without backtest infrastructure (which Phase 3k brief constraints prohibit).

**Critical anti-circular-reasoning discipline for any regime-first memo:**

- The memo must **define regimes from first principles**, not from per-fold outcomes of existing candidates. Defining "F3 2023H1-like regime" by what worked there is exactly the post-hoc loosening §11.3.5 forbids.
- The memo must **propose a falsifiable per-regime mechanism prediction** for each candidate retained-evidence family. The prediction must be testable on independent data (not the data used to define the regimes).
- The memo must **acknowledge the Phase 4 dependence**. Live regime tracking is non-trivial; specifying it on paper does not authorize implementing it.
- The memo must **not propose any regime-conditioned strategy spec** within Phase 3k+1 itself. The memo is exploratory; a follow-on phase (separately authorized) would do per-family per-regime spec work.

This option is recommended as the tertiary candidate for Phase 3k's next-decision recommendation — IF the operator prefers a methodological-framework reset over an external-cost-evidence verification.

---

## 12. Recommended next operator decision

**Primary recommendation: remain paused.**

This is the same recommendation Phase 3e made after F1's HARD REJECT, now strengthened by Phase 3j's MECHANISM PASS / FRAMEWORK FAIL — other outcome (the second consecutive new-family framework-fail). The disciplined response to repeatedly elevated treadmill risk is to **pause and let the operator strategically choose**, rather than authorize another rank-3+ candidate variant or another spec-writing phase without operator-driven hypothesis development.

Specifically:

- **Hold project state at the post-Phase-3j boundary.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence; §11.6 = 8 bps HIGH preserved; §1.7.3 locks preserved; no paper/shadow planning; no Phase 4 work; no live-readiness work; no deployment work; no production-key creation; no exchange-write capability; no MCP / Graphify / `.mcp.json`; no credentials.
- **No next research phase authorized.** Phase 3k is docs-only and terminal-as-of-now.
- **Operator decides whether and when to authorize any subsequent phase.**

**Acceptable alternative active recommendations (per Phase 3k brief §12):**

If the operator prefers an active docs-only path over remain-paused, two acceptable alternatives are:

1. **Authorize external execution-cost evidence review (docs-only).** Per §10 above. Acceptable IFF authorized with explicit ex-ante operator commitment to symmetric-outcome discipline ("the outcome could go either way; revision is not the goal"). Most disciplined active option given §11.6's repeated filtering of R2 / F1 / D1-A.
2. **Authorize regime-first research framework memo (docs-only).** Per §11 above. Acceptable IFF authorized with explicit ex-ante operator commitment to anti-circular-reasoning discipline (regimes defined from first principles, not from per-fold outcomes). Methodologically distinct from any specific strategy family; addresses the cross-family mechanism-pass / framework-fail pattern at framework level.

**Acceptable hold recommendation:**

3. **Hold for operator strategic choice.** If the operator is not ready to choose between (1) remain-paused, (2) external-cost-evidence review, or (3) regime-first memo, holding the decision is itself acceptable. The project state at the post-Phase-3j boundary is stable; no time-sensitive action is required.

**Phase 3k does NOT recommend:**

- Authorizing implementation, backtesting, paper/shadow, Phase 4, live-readiness, or deployment work (forbidden by Phase 3k brief).
- Authorizing D1-A-prime / D1-B / V1/D1 hybrid / F1/D1 hybrid (forbidden by Phase 3k brief).
- Authorizing a new strategy-family discovery memo (Option D — too treadmill-prone after two consecutive framework-fails).
- Authorizing an ML feasibility memo (Option E — premature without operator-developed motivation; risks are severe and well-documented).
- Lifting any Phase 2f threshold, §1.7.3 project-lock, or §11.6 cost-sensitivity gate (forbidden by §11.3.5 / Phase 3k brief).
- Stopping active strategy research as a stronger framing than remain-paused (Option H — operationally equivalent to Option A).

The recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

## 13. Update to `docs/00-meta/current-project-state.md`

The canonical project-state document is updated in the same Phase 3k branch / commit to reflect:

- Phase 3j merged into `main` (Phase 3j merge commit `5c8537b`; merge-report commit `5d18408`).
- D1-A framework verdict: MECHANISM PASS / FRAMEWORK FAIL — other.
- D1-A retained as research evidence only.
- D1-A non-leading.
- Phase 3j terminal for D1-A under current locked spec.
- No D1-A-prime, D1-B, V1/D1 hybrid, or F1/D1 hybrid authorized.
- R3 remains V1 breakout baseline-of-record.
- H0 remains V1 breakout framework anchor.
- R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only.
- F1 remains HARD REJECT.
- Phase 3d-B2 remains terminal for F1.
- R2 remains FAILED — §11.6 cost-sensitivity blocks.
- §11.6 HIGH = 8 bps per side preserved.
- No next phase authorized.
- No paper/shadow authorized.
- No Phase 4 authorized.
- No live-readiness authorized.
- No deployment authorized.

The diff to `current-project-state.md` is intentionally narrow: it advances the "Current Phase" / "Most recent merge" / "Strategy Research Arc Outcomes" / "Immediate Next Tasks" / "Implementation Readiness Status" sections to reflect Phase 3j and Phase 3k. **No threshold change. No strategy-parameter change. No project-lock change. No paper/shadow / Phase 4 / live-readiness / deployment authorization.**

---

## 14. Explicit preservation list

Phase 3k is docs-only and explicitly preserves all of the following verbatim:

- **No threshold changes.** Phase 2f §10.3 / §10.4 / §11.3 / §11.4 / §11.6 = 8 bps HIGH per side preserved. The catastrophic-floor predicate definition (`expR ≤ −0.50 OR PF ≤ 0.30`; non-catastrophic requires `expR > −0.50 AND PF > 0.30`) preserved.
- **No strategy-parameter changes.** R3 sub-parameters; H0 baseline; R1a sub-parameters; R1b-narrow sub-parameter; R2 sub-parameters; F1 spec axes; **D1-A spec axes** (|Z_F| ≥ 2.0; trailing 90 days / 270 events; 1.0 × ATR(20) stop; +2.0R target; 32-bar time-stop; per-funding-event cooldown; band [0.60, 1.80] × ATR(20); contrarian direction; no regime filter). All preserved verbatim.
- **No project-lock changes.** §1.7.3 locks (BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; one active protective stop max; 0.25% risk per trade; 2× leverage cap; mark-price stops; v002 datasets; one-way mode; isolated margin; no pyramiding; no reversal while positioned; no hedge mode) preserved verbatim.
- **No MCP / Graphify / `.mcp.json` activation.** No MCP server enabled; no Graphify integration; no `.mcp.json` file created or modified.
- **No credentials.** No production / sandbox / testnet API keys requested, created, or used. No `.env` file modified. No secrets in any committed file.
- **No exchange-write paths.** No exchange-write capability proposed, implemented, or enabled. `BacktestAdapter.FAKE` remains the only adapter type in the engine.
- **No `data/` commits.** Phase 3k commits are limited to `docs/00-meta/current-project-state.md` and the two new `docs/00-meta/implementation-reports/` files (this memo + closeout report).

---

**End of Phase 3k post-D1-A research consolidation memo.** Phase 3k records the post-D1-A project-state consolidation, summarizes the V1 breakout + F1 mean-reversion + D1-A funding-aware three-arc research history, evaluates eight operator-decision options against the Phase 3k brief constraints, and recommends **remain paused** as the disciplined primary response to the three-arc evidence pattern, with **external execution-cost evidence review (docs-only)** and **regime-first research framework memo (docs-only)** as acceptable secondary / tertiary alternatives if the operator prefers an active path. R3 remains V1-breakout baseline-of-record; H0 remains framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence; §11.6 = 8 bps HIGH preserved; §1.7.3 locks preserved verbatim. **No next phase authorized.** **No paper/shadow / Phase 4 / live-readiness / deployment / MCP / Graphify / `.mcp.json` / credential / exchange-write change.** **No `data/` commits.** Phase 3k is docs-only; the operator decides whether and when to authorize any subsequent phase. Awaiting operator review.
