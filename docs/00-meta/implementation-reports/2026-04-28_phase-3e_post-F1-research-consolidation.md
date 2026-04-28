# Phase 3e — Post-F1 Research Consolidation / Strategy-Reset Memo

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; **no post-hoc loosening per §11.3.5**); Phase 2i §1.7.3 project-level locks (H0 anchor; BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets); Phase 2p consolidation memo (R3 baseline-of-record; future-resumption pre-conditions); Phase 2x family-review memo (V1 breakout family at useful ceiling under current framework); Phase 2y slippage / cost-policy review (§11.6 = 8 bps HIGH preserved); Phase 3a new-strategy-family discovery memo (F1 ranked rank-1 near-term family candidate); Phase 3b F1 spec memo §§ 1–15 (binding spec); Phase 3c F1 execution-planning memo §§ 1–13; Phase 3d-A / 3d-B1 / 3d-B2 reports; Phase 3d-B2 merge report; `docs/03-strategy-research/v1-breakout-strategy-spec.md`; `docs/05-backtesting-validation/backtesting-principles.md`; `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`; `docs/05-backtesting-validation/cost-modeling.md`; `docs/04-data/data-requirements.md`; `docs/04-data/dataset-versioning.md`; `.claude/rules/prometheus-core.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/implementation-ambiguity-log.md`.

**Phase:** 3e — Docs-only **post-F1 research consolidation / strategy-reset memo.** Consolidates the completed V1 breakout + F1 mean-reversion research arcs, updates canonical project-state documentation, and produces a disciplined operator decision menu for what should happen next.

**Branch:** `phase-3e/post-f1-consolidation`. **Memo date:** 2026-04-28 UTC.

**Status:** Recommendation drafted. **No code change. No backtest. No variant created. No parameter tuned. No threshold changed. No project-level lock changed. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write proposal.** R3 remains baseline-of-record. H0 remains framework anchor. R1a / R1b-narrow / R2 / F1 remain retained as research evidence. Recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

## 1. Plain-English explanation of what Phase 3e is deciding

Phase 3e is a docs-only consolidation phase, the natural successor to Phase 3d-B2's HARD REJECT verdict on F1.

The Prometheus project has now executed two complete strategy research arcs under unchanged framework discipline:

- **The V1 breakout-continuation arc** (Phases 2e through 2w) — one locked baseline (H0), one cleanly-promoted structural redesign (R3), and three post-R3 structural redesigns (R1a, R1b-narrow, R2) of which one was framework-FAILED on §11.6 cost-sensitivity. R3 became the baseline-of-record per Phase 2p §C.1; R1a / R1b-narrow / R2 are retained as research evidence per Phase 2p §D / Phase 2s §13 / Phase 2w §16.3.
- **The F1 mean-reversion-after-overextension arc** (Phases 3a through 3d-B2) — one new strategy family (F1) ranked as the Phase 3a rank-1 near-term candidate, specified at Phase 3b, planned at Phase 3c, implemented at Phase 3d-A, wired to the engine at Phase 3d-B1, and executed at Phase 3d-B2. F1's first-execution-gate verdict was **HARD REJECT** with five separate catastrophic absolute-floor violations across BTC/ETH × MED/HIGH cells.

Phase 3e weighs the resulting question:

> Given that the V1 breakout family is at its useful ceiling (Phase 2x), the framework cost-policy is preserved (Phase 2y), and the rank-1 near-term new family (F1) hard-rejected, **what is the right next docs-only phase, if any?**

What Phase 3e is NOT deciding:

- Not deciding whether to deploy R3 or to begin paper/shadow (forbidden by operator policy).
- Not deciding whether to begin Phase 4 runtime / state / persistence work (forbidden).
- Not deciding whether to lift any §1.7.3 project-level lock.
- Not deciding whether to revise any Phase 2f threshold (Phase 2y closed this).
- Not authorizing any next execution phase, any next implementation phase, any backtest, or any code change.
- Not commencing F1-prime, F1-target-subset, or any F1-derived hypothesis development.

The output is a consolidated record of project state plus an operator decision menu with a single recommended next step (which legitimately may be "remain paused"). Phase 3e produces a memo; the operator decides whether to authorize anything downstream.

---

## 2. Current canonical project state

| Item | State |
|------|-------|
| **R3 (Phase 2j memo §D — Fixed-R + 8-bar time-stop, no trailing)** | **V1 breakout baseline-of-record** per Phase 2p §C.1; locked sub-parameters `exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`; same-bar priority STOP > TAKE_PROFIT > TIME_STOP; protective stop never moved intra-trade. |
| **H0 (Phase 2e locked baseline)** | **V1 breakout framework anchor** per Phase 2i §1.7.3; sole §10.3 / §10.4 / §11.3 / §11.4 / §11.6 comparison anchor for all V1-family candidates. |
| **R1a (Phase 2j memo §C — volatility-percentile setup, X=25 / N=200, on top of R3)** | Retained as **research evidence only** per Phase 2p §D; non-leading; symbol-asymmetric mixed-PROMOTE (ETH-favorable / BTC-degrading); ineligible under §1.7.3 BTCUSDT-primary lock without lock revision. |
| **R1b-narrow (Phase 2r — bias-strength magnitude S=0.0020 on top of R3)** | Retained as **research evidence only** per Phase 2s §13; non-leading; formal §10.3.a-on-both PROMOTE but R3-anchor near-neutral marginal contribution; small-sample caveats (BTC n=10 / ETH n=12 R-window). |
| **R2 (Phase 2u — pullback-retest entry topology on top of R3)** | Retained as **research evidence only** per Phase 2w §16.3; **framework FAILED — §11.6 cost-sensitivity blocks** (BTC HIGH-slip Δexp_H0 −0.014; ETH HIGH-slip Δexp_H0 −0.230). M1 + M3 mechanism support but slippage-fragile. |
| **F1 (Phase 3b §4 — mean-reversion-after-overextension)** | Retained as **research evidence only**; **framework verdict: HARD REJECT** per Phase 3c §7.3 catastrophic-floor predicate (5 separate violations across BTC/ETH × MED/HIGH). M1 BTC PARTIAL (mean +0.024 R below +0.10 threshold; fraction non-neg 55.4% above 50%); M2 BTC FAIL / ETH weak-PASS; M3 PASS-isolated on both symbols. |
| **§1.7.3 project-level locks** | **Preserved verbatim:** BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; one active protective stop max; 0.25% risk per trade; 2× leverage cap; mark-price stops; v002 datasets; one-way mode; isolated margin; no pyramiding; no reversal while positioned; no hedge mode. |
| **Phase 2f thresholds** | **Preserved verbatim:** §10.3.a Δexp ≥ +0.10 R; §10.3.c |maxDD| ratio < 1.5×; §10.4 absolute floors expR > −0.50 AND PF > 0.30; §11.3 V-window no-peeking; §11.4 ETH non-catastrophic; **§11.6 = 8 bps HIGH per side** (Phase 2y closeout). |
| **Phase 3b F1 spec axes** | **Preserved verbatim:** overextension window 8; threshold 1.75 × ATR(20); mean-reference window 8 (frozen SMA(8) at signal close); stop buffer 0.10 × ATR(20); time-stop 8 bars; stop-distance band [0.60, 1.80] × ATR(20). |
| **Paper/shadow planning** | **Not authorized.** Operator policy continues to defer paper/shadow indefinitely. |
| **Phase 4 (runtime / state / persistence) work** | **Not authorized.** No runtime / state / persistence implementation has been started. |
| **Live-readiness work** | **Not authorized.** No production-key creation, no exchange-write capability, no deployment. |
| **MCP / Graphify / `.mcp.json`** | **Not activated, not touched.** |
| **Credentials / `.env` / API keys** | **Not requested, not created, not used.** |

The next operator decision is operator-driven only. Phase 3e does not pre-empt that decision; this section records the state on which any future decision must build.

---

## 3. Research arc summary

The complete two-arc Prometheus strategy-research history through Phase 3d-B2:

### 3.1 V1 breakout-continuation arc (Phase 2e through Phase 2w)

| Phase | What it produced |
|-------|------------------|
| **2e** | H0 locked baseline (Phase 2e v002 datasets); BTC R-window expR=−0.459 / ETH expR=−0.475. |
| **2f Gate 1** | §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds pre-declared; §11.3.5 binding rule (no post-hoc loosening). |
| **2g** | Wave-1 parametric variants tested vs H0; **REJECT ALL.** Preserved as historical evidence only. |
| **2h** | Decision memo: structural redesigns warranted; parametric tuning insufficient. |
| **2i** | §1.7.3 project-level locks committed; H0 designated sole §10.3 anchor. |
| **2j** | Structural redesign specs: §C R1a (volatility-percentile setup), §D R3 (Fixed-R + 8-bar time-stop). |
| **2k** | Phase 2k execution plan; per-variant runner pattern. |
| **2l** | R3 first execution: **PROMOTE — broad-based.** R3 improves expR in all 6 regime-symbol cells; 4/5 BTC + 3/5 ETH folds beat H0; first positive-expR BTC folds (F2, F3); cost-robust at HIGH; bit-identical MARK vs TRADE_PRICE. |
| **2m** | R1a+R3 first execution: **mixed-PROMOTE.** ETH-favorable / BTC-degrading; R1a's compression-selection mechanically correct (100% entries at percentile ≤ 25%); asymmetry in post-compression follow-through. |
| **2n** | Strategy-review: R3 = research-leading; R1a+R3 = promoted-but-non-leading. |
| **2o** | Asymmetry-review: BTC/ETH asymmetry diagnosed as market-structure × strategy interaction (not a fixable rule defect); R1a-as-research-evidence framing. |
| **2p** | Consolidation memo: **R3 baseline-of-record locked**; R1a retained-for-future-hypothesis-planning research evidence; future-resumption pre-conditions documented. |
| **2r / 2s** | R1b-narrow spec + first execution: formal §10.3.a-on-both PROMOTE but R3-anchor near-neutral marginal contribution; retained research evidence; non-leading. |
| **2t / 2u / 2v / 2w** | R2 spec + execution: MED-slip §10.3 PROMOTE with M1 + M3 mechanism support; **§11.6 cost-sensitivity gate FAILS** at HIGH on both symbols; **framework FAILED — slippage-fragile**; retained research evidence. |
| **2x** | V1 breakout family-level review: **family at useful ceiling under current framework** (post-R3 candidates show diminishing absolute-edge return); five next-decision options enumerated. |
| **2y** | Slippage / cost-policy review: **§11.6 = 8 bps HIGH preserved unchanged**; framework calibration confirmed; no threshold revision. |

**V1 breakout arc outcome:** R3 is the strongest single candidate evidence the project has produced. R3 alone produces a clean broad-based PROMOTE; the absolute-aggregate edge has not materialized (R3 BTC R-window expR=−0.240 / ETH=−0.351 — still negative). The family is **alive but not validated for live exposure**; live-readiness, paper/shadow, and Phase 4 all remain deferred per operator policy.

### 3.2 F1 mean-reversion-after-overextension arc (Phase 3a through Phase 3d-B2)

| Phase | What it produced |
|-------|------------------|
| **3a** | Docs-only new-strategy-family discovery survey: eight candidate non-breakout families enumerated; F1 ranked **rank-1 near-term candidate** (BTC-friendly mean-reversion thesis; v002 dataset sufficient; complementary to V1 breakout failure mode #1 chop). |
| **3b** | Docs-only F1 spec memo: 9 axes locked (overextension window 8; threshold 1.75 × ATR; mean-reference SMA(8) frozen at signal close; stop buffer 0.10 × ATR; time-stop 8 bars; stop-distance band [0.60, 1.80] × ATR; cooldown rule; no regime filter; market entry at next-bar open). Single-rule-per-axis discipline; non-fitting rationale; falsifiable mechanism predictions M1/M2/M3. |
| **3c** | Docs-only F1 execution-planning memo: precommitted run inventory (4 mandatory R-window cells + 1 conditional V); first-execution gate definition (§7.2 conditions i–v with operator-mandated amendments §7.2(iv) BTC HIGH expR > 0; §7.3 MECHANISM PASS / FRAMEWORK FAIL — §11.6 cost-sensitivity blocks); §10.4 sequencing requirement (quality gates + H0/R3 control reproduction before F1 interpretation). |
| **3d-A** | F1 implementation-only phase: F1 self-contained module + primitives + locked `MeanReversionConfig` + `StrategyFamily` dispatch surface guard + `TARGET` ExitReason + 68 unit tests; quality gates green; H0/R3 controls bit-for-bit; **F1 deliberately non-runnable** through `BacktestConfig` validator hard guard. |
| **3d-B1** | F1 engine-wiring phase: lifted Phase 3d-A guard; wired `_run_symbol_f1` lifecycle (entry / stop / target / time-stop / cooldown / accounting funnel); added F1 TradeRecord output fields + `F1LifecycleCounters`; runner scaffold under `--phase-3d-b2-authorized` hard guard; 25 new tests (5 BacktestConfig + 20 engine dispatch); quality gates green; H0/R3 controls bit-for-bit. |
| **3d-B2** | F1 first-execution: 4 mandatory R-window cells executed; conditional V-window skipped (R-window hard-rejected); §7.2 first-execution gate evaluated; M1/M2/M3 mechanism checks computed; §8 mandatory diagnostics produced; P.14 hard-block invariants all PASS; **framework verdict: HARD REJECT** (5 catastrophic floor violations). |

**F1 arc outcome:** F1 first-execution HARD REJECT per Phase 3c §7.3 catastrophic-floor predicate. F1 retained as research evidence; F1 family research is concluded as failed. Phase 3d-B2 is terminal for F1; no subsequent F1 phase is proposed.

---

## 4. Summary table of all major candidates

R-window evidence: 2022-01-01 → 2025-01-01, MEDIUM slippage, MARK_PRICE stop-trigger, locked Phase 2e v002 datasets, BTCUSDT primary, ETHUSDT comparison.

| Candidate | Phase | Mechanism tested | Strongest evidence | Failure mode | Final status | Changed baseline? | Retained research value |
|-----------|-------|------------------|--------------------|---------------|---------------|:-:|------------------------|
| **H0** | 2e | Locked baseline (range-based setup; 1h binary slope-3 bias + EMA(50)/EMA(200) position; 0.10 × ATR breakout buffer; staged-trailing exit; 0.10 × ATR structural-stop buffer) | Foundational; bit-for-bit reproducible across phases (Phase 2g, 2k, 2l, 2m, 2s, 2w-A, 3d-A, 3d-B1, 3d-B2) | BTC R-window expR=−0.459 / PF=0.255; ETH expR=−0.475 / PF=0.321 (aggregate negative); chop with repeated false breaks (V1 spec failure mode #1) | **Locked anchor** | N/A (H0 *is* the baseline) | **Foundational.** Sole §10.3 / §10.4 anchor for all V1-family candidates per Phase 2i §1.7.3. Continues to define the framework's reference point. |
| **R3** | 2l | Exit philosophy redesign (Fixed-R take-profit at +2.0 R + unconditional 8-bar time-stop; protective stop never moved intra-trade) | **Strongest single candidate** in the project. Improves expR in all 6 regime-symbol cells; 4/5 BTC + 3/5 ETH folds beat H0; first positive-expR BTC folds (F2 +0.015, F3 +0.100); cost-robust at HIGH; bit-identical MARK vs TRADE_PRICE; zero TRAILING_BREACH / STAGNATION leakage. BTC expR=−0.240 / PF=0.560; ETH expR=−0.351 / PF=0.474. | Aggregate edge still negative; PF<1 on both symbols ("less negative than H0" not "break-even"). | **PROMOTE — baseline-of-record** per Phase 2p §C.1 | **YES** | **Strongest single evidence in the project.** R3 is the deployable variant if and when operator policy authorizes paper/shadow / Phase 4. |
| **R1a + R3** | 2m | Setup-validity predicate (volatility-percentile, X=25 / N=200) on top of R3 | ETH V-window first-ever positive netPct (+0.69%); ETH low_vol PF 1.353 (first cell with positive expR AND PF > 1); ETH shorts PF 1.906 (strongest direction-symbol cell ever); R1a's compression-selection mechanically correct (100% of entries at percentile ≤ 25%, exactly per Phase 2j §C.5 spec). | BTC degraded vs R3 (Δexp_R3 −0.180 R; V-window 0% WR / 4 trades / expR −0.990); BTC R-window expR=−0.420 / PF=0.355; ETH-favorable / BTC-degrading symbol asymmetry; ineligible under §1.7.3 BTCUSDT-primary lock without lock revision. | **mixed-PROMOTE; retained research evidence; non-leading** per Phase 2p §D | NO | Compression-mechanism evidence; ETH-favorability suggests symbol-conditional R1a-prime hypothesis territory (Phase 2o §F.1) but not currently developed. |
| **R1b-narrow + R3** | 2s | Bias-validity predicate (slope-strength magnitude S=0.0020) on top of R3 | Formal §10.3.a-on-both PROMOTE (first such); R-window BTC expR=−0.263 / PF=0.561; ETH expR=−0.224 / PF=0.622; ETH V-window second positive netPct (+0.28%); cost-resilience holds at HIGH on both symbols. | 65–70% trade-count drop (R-window n=10 BTC / 12 ETH); R3-anchor near-neutral marginal contribution; small-sample caveats; not a meaningful absolute-edge improvement. | **PROMOTE / PASS-with-caveats; retained research evidence; non-leading** per Phase 2s §13 | NO | Bias-strength selectivity evidence; magnitude-threshold predicate concept available for future hypothesis development. |
| **R2 + R3** | 2w | Entry-lifecycle topology (pullback-retest with 8-bar validity window; 5-step precedence; fill-time stop-distance re-check) on top of R3 | MED-slip §10.3 PROMOTE on both symbols; M1 (pullback-mechanism) + M3 (filtered-trade-quality) mechanism support per Phase 2w §11.5 / §11.7; clean engine implementation (43 R2-specific tests; bit-identical H0/R3 control reproduction). | **§11.6 HIGH-slip cost-sensitivity gate FAILS** on both symbols (BTC Δexp_H0 −0.014 sub-threshold; ETH Δexp_H0 −0.230 catastrophic). M2 (regime-decomposition) FAIL. The first §11.6 failure in the family arc. Slippage-fragile by construction (small post-pullback R-distance amplified by per-trade cost). | **FRAMEWORK FAILED — §11.6 cost-sensitivity blocks; retained research evidence; non-leading** per Phase 2w §16.3 | NO | Pullback-mechanism evidence + slippage-fragility precedent. R2's failure motivated the Phase 3c §7.2(iv) BTC HIGH > 0 cost-resilience strengthening. |
| **F1** | 3d-B2 | Mean-reversion-after-overextension as a separate strategy family (not a V1 variant): 8-bar cumulative displacement > 1.75 × ATR(20) → market-fill at next-bar open; SMA(8) frozen target; structural stop with 0.10 × ATR buffer; unconditional 8-bar time-stop; same-direction cooldown until unwind | M3 (TARGET-exit subset) PASS on both symbols: BTC mean +0.75 R / aggregate +1149 R; ETH mean +0.87 R / aggregate +1398 R. M1 BTC PARTIAL: fraction non-neg 55.4% (above 50%) but mean only +0.024 R (below +0.10 threshold). The mean-reversion target IS profitable when isolated. | Catastrophic absolute-floor violations: BTC MED expR=−0.5227, BTC HIGH expR=−0.7000 / PF=0.2181, ETH HIGH expR=−0.5712 / PF=0.2997. M2 BTC FAIL (F1 BTC low-vol stop-out 55.6% > H0 46.2%; opposite of chop-regime advantage hypothesis). 4720 BTC + 4826 ETH trades over 36 months (~150× H0/R3); per-trade negative expR multiplied by trade volume produces catastrophic equity loss. | **HARD REJECT — first-execution gate; retained research evidence; non-leading** per Phase 3c §7.3 | NO | TARGET-subset isolated profitability is mechanism-relevant evidence; the wider F1 strategy-as-specified is FAILED because STOP exits (53–54%) overwhelm the TARGET-exit positive contribution. Mechanism evidence may inform any hypothetical future F1-prime spec consideration in a separately-authorized phase. |

---

## 5. F1-specific postmortem

### 5.1 Why F1 was justified as a new family

Phase 3a §4.1 / §6 ranked F1 as the rank-1 near-term family candidate on five distinct grounds:

1. **Mechanism complementarity to V1's documented failure mode.** V1 breakout's failure mode #1 is "chop with repeated false breaks" (`v1-breakout-strategy-spec.md` §"Failure Modes"). F1's mean-reversion thesis is structurally the inverse: F1 expects to thrive in exactly the regime where V1 expects to lose. The two families are not redundant; they address opposite regimes.
2. **Empirical regime-incompatibility evidence on V1.** Phase 2g/2h/2l/2m/2s/2w consistently identified F4 2024H1 as the worst per-fold cell on V1 (H0 BTC F4 = −1.025 R; R3 BTC F4 = −0.870 R; R3 ETH F4 = −0.836 R). R3 reduced the damage but did not solve the regime incompatibility.
3. **§1.7.3 BTCUSDT-primary alignment plausibility.** Phase 3a §4.1(h) argued F1 inverts V1's BTC/ETH asymmetry: BTC's tighter spread + chop tendency favors mean-reversion's tight-stop geometry; ETH's noisier wider-spread profile is hostile to mean-reversion. This was a plausibility claim, not an empirical claim.
4. **v002 dataset sufficiency.** F1 required only existing 15m + ATR(20) + funding-rate data; no v003 raw-data bump.
5. **Falsifiable mechanism predictions.** F1's hypothesis was operationalized as M1 (post-entry counter-displacement at 8-bar horizon ≥ +0.10 R + fraction ≥ 50%), M2 (chop-regime stop-out fraction reduction vs H0 ≥ +0.10 percentage points), M3 (TARGET-exit subset aggregate net-of-cost > 0). All three predictions were testable on v002 data.

The Phase 3a → 3b → 3c → 3d-A → 3d-B1 → 3d-B2 sequence implemented this hypothesis under the same framework discipline that produced R3 / R1a / R1b-narrow / R2.

### 5.2 What F1 proved mechanically

F1's M3 (TARGET-exit subset) PASSES decisively on both symbols. **The SMA(8) mean-reversion target is profitable when isolated:**

- BTC TARGET subset: n=1536, mean +0.7481 R, aggregate +1149.14 R.
- ETH TARGET subset: n=1610, mean +0.8684 R, aggregate +1398.19 R.

This is informative empirical evidence that the **mean-reversion mechanism exists at the SMA(8) horizon** on Binance USDⓈ-M BTCUSDT/ETHUSDT 15m data, in a way that survives round-trip taker fee + MEDIUM slippage + funding cost on the trades that actually reach the target.

F1's M1 (post-entry counter-displacement) is **direction-supported but magnitude-falsified on BTC**:

- BTC h=8 fraction non-neg = 55.38% (above the 50% PASS threshold).
- BTC h=8 mean = +0.0238 R (well below the +0.10 R PASS threshold).

I.e. more than half of F1 BTC trades produce a non-negative 8-bar counter-displacement, but the typical magnitude is small (~+0.024 R), too small to overcome the per-trade cost burden on the wider trade population. M1 ETH is informatively worse: mean turns negative at h≥4 (h=8 mean = −0.0420 R).

F1's M2 (chop-regime stop-out fraction) **CONTRADICTS the Phase 3b §2.3 hypothesis on BTC**: F1's BTC low-vol stop-out fraction (55.56%) is *higher* than H0's (46.15%). The chop-regime advantage F1 was designed to capture is not present on BTC at the F1-as-specified parameter setting. ETH's M2 looks favorable (Δ +0.39) but with a statistically weak H0 baseline (n=12).

Combined: F1's TARGET subset is profitable in isolation; F1's wider strategy-as-specified is not.

### 5.3 Why F1 failed as a full strategy

Three structural reasons:

1. **Trade frequency × per-trade negative expR multiplies into catastrophic equity loss.** F1 fires ~150× more trades than H0/R3 (4720+ BTC trades vs 33). Even a per-trade expR of similar magnitude to H0 (~−0.46 R) compounds to BTC R-window total return of −546% on a $10K starting equity. The strategy-as-specified does not select only the profitable subset prospectively.
2. **Cost-sensitivity slope is steep and uniformly worsening.** Even at LOW slippage (1 bps per side), F1 is decisively negative (BTC expR=−0.4335). HIGH slippage (8 bps per side) catastrophic (BTC expR=−0.7000 / PF=0.2181). F1 is **not cost-resilient** — the same slippage-fragility geometry that failed R2 in Phase 2w fails F1 here, but more severely. F1's stop-distance is constrained to [0.60, 1.80] × ATR by §4.9, so the post-pullback small-R-distance pattern that R2 had is shared structurally.
3. **The chop-regime advantage hypothesis (Phase 3b §2.3) does not hold on BTC.** M2 BTC contradicts it directly. F1 stops out *more* in BTC chop than H0 does. The fundamental regime-complementarity claim is partially falsified by the empirical evidence.

The catastrophic-floor predicate (Phase 3c §7.3) classifies F1's first-execution outcome as HARD REJECT with substantial margin (5 separate violations across BTC/ETH × MED/HIGH cells). HARD REJECT supersedes MECHANISM-FAIL / MECHANISM-PASS / FRAMEWORK-FAIL alternatives in the §7.3 verdict mapping, irrespective of M3's isolated-subset PASS.

### 5.4 Why M3 TARGET subset evidence is not enough to continue F1 automatically

Tempting interpretation: "M3 PASSES; F1's mean-reversion target IS profitable; just filter F1 down to the TARGET-eligible subset." This interpretation is **forbidden by Phase 2j §C.6 / §11.3.5 single-spec discipline** for three reasons:

1. **Selecting the TARGET subset prospectively requires a new predicate that does not currently exist.** The TARGET subset is defined retrospectively (a trade that exited at TARGET); deciding *before entry* whether a fired entry will reach TARGET requires a new predicate that distinguishes target-eligible from non-target-eligible overextension events. Such a predicate is not in the Phase 3b spec; constructing it post-hoc to "rescue" F1 is precisely the §11.3.5 forbidden post-hoc loosening.
2. **R2's precedent confirms this rule.** R2's M1 + M3 mechanism PASSED in Phase 2w; the §11.6 cost-sensitivity gate FAILED. R2 was retained as research evidence with mechanism support but **not** continued as an F1-prime under the same logic. The Phase 2w §16.3 framing established: "mechanism-supported subset" is research evidence, not promotion. F1 inherits the same treatment.
3. **The R2 → F1 → F1-prime chain risks unbounded post-hoc tuning under "research framing"**. Each candidate that fails a framework gate but produces some isolated mechanism-supported subset could justify a "next variant" purely by carving out the subset. This is the treadmill risk Phase 2x §7.2 / Phase 2p §H.4 explicitly warned against.

**Therefore: F1's M3 PASS is recorded as research evidence only.** It is informative; it is not a license to authorize F1-prime. Any future F1-prime spec must come from an **independently developed operator-driven hypothesis** that is falsifiable, mechanism-grounded, and framework-discipline-compliant — not from "select the M3 subset and tune around it".

### 5.5 Why no F1-prime should be started without a separate operator decision

Per Phase 3c §3 and Phase 2f §11.3.5, Phase 3d-B2's HARD REJECT is the binding outcome. No automatic F1-prime authorization follows. If the operator independently develops a falsifiable F1-prime hypothesis (e.g., a regime-conditional overextension predicate; a target-subset selection rule justified ex-ante; a different mean-reference horizon), that hypothesis would require:

1. A separately-authorized Phase 3a-style discovery memo *or* directly a Phase 3b-style spec memo for the new hypothesis.
2. Phase 3c-style execution-planning.
3. Phase 3d-A-style implementation with locked config.
4. Phase 3d-B-style execution + first-execution-gate evaluation.

None of those phases is currently proposed. The operator decides whether and when any of them is authorized. Phase 3e does not propose an F1-prime phase.

---

## 6. Family-level diagnosis

What the project has now empirically learned across the V1 breakout + F1 mean-reversion arcs:

### 6.1 Breakout continuation

**Status:** Demonstrated structural-redesign responsiveness; absolute-aggregate edge has not materialized.

- Two PROMOTE outcomes (R3 broad-based; R1b-narrow formal), one mixed-PROMOTE (R1a+R3), one framework-FAIL (R2). The family responds to disciplined structural redesign in a measurable way, but no candidate has produced positive aggregate net-of-cost expR on R-window.
- R3's improvements are real and broad-based but quantitatively bounded: BTC R-window expR=−0.240 (PF=0.560) versus H0=−0.459 (PF=0.255). R3 reduces the per-trade cost of being wrong by ~50% but does not flip the sign. The "less negative than H0" framing is the precise honest summary.
- The family operates within a regime-incompatibility constraint (chop / range-bound markets) that R3 partially mitigates but does not solve.

### 6.2 Entry timing

**Status:** Pullback-retest entries are slippage-fragile; market entries at next-bar open are cost-robust.

- R2's entry-topology change (pullback-retest with confirmation) PROMOTED at MED slippage but FAILED at HIGH per Phase 2w §11.6. The small post-pullback R-distance geometry amplifies per-trade cost. Pullback-retest is a known slippage-vulnerable entry shape.
- R3 / R1a / R1b-narrow all use the V1 default "market entry at next-bar open after confirmed signal close" — these are cost-robust at HIGH slippage on both symbols.
- F1's market entry at next-bar open is not the issue; F1's overall cost-fragility comes from trade-frequency × negative-expR aggregation, not from the entry shape per se.

### 6.3 Mean reversion after overextension

**Status:** The mean-reversion target exists (M3 PASS) but the wider strategy is not viable as specified.

- F1's TARGET-subset is profitable in isolation on both symbols; this is empirical evidence the SMA(8) mean-reversion target does fire and is cost-survivable on the trades that actually reach it.
- F1's wider strategy fails because (a) trade frequency is ~150× H0, (b) M1 magnitude (+0.024 R) is far below the +0.10 R PASS threshold, and (c) STOP exits (53–54%) overwhelm the TARGET-exit positive contribution.
- The Phase 3b §2.3 chop-regime-advantage hypothesis is partially falsified on BTC: F1 stops out more in BTC chop than H0 does (M2 BTC FAIL).
- Mean-reversion-after-overextension as a strategy family is not viable at the F1-as-specified parameter setting under §1.7.3 / §11.6 discipline. F1 is not a candidate-of-record.

### 6.4 Stop / target asymmetry

**Status:** Tight stops + tight targets are cost-amplifying; structural stops + R-multiple targets are more cost-robust.

- F1's [0.60, 1.80] × ATR stop-distance band produces stop_distance ≈ 1 × ATR on average (similar to V1's band). However F1's frozen SMA(8) target is geometrically *closer* to entry than R3's +2.0 R target (by construction — SMA(8) is a recent mean, +2.0 R is a fixed multiple of stop distance). F1's per-trade R-multiple potential is therefore smaller than R3's, making per-trade cost a larger fraction.
- R3's exit philosophy (+2.0 R fixed take-profit + 8-bar time-stop) produces larger per-trade R-multiples on the winning trades, which is more cost-robust by construction.
- The asymmetry is structural, not parametric: changing F1's target reference does not fix the underlying stop / target geometry without changing the family's mean-reversion thesis.

### 6.5 Trade frequency and cost load

**Status:** High-frequency strategies amplify per-trade negative expR catastrophically; low-frequency strategies preserve framework-discipline informativeness.

- H0 / R3 / R1a / R1b-narrow / R2 produce 22–33 R-window trades per symbol. Per-trade negative expR is bounded in aggregate.
- F1 produces 4720+ R-window trades per symbol. Per-trade negative expR multiplies into ~−540% to ~−440% aggregate equity loss on $10K starting equity.
- Phase 3a §4.1(f) anticipated higher F1 trade frequency ("R-window expected sample size: ≥80–120 trades per symbol"); the empirical 4720+ exceeds that estimate by 50×, suggesting the §4.1(f) estimate was conservative.
- High-frequency strategies are not categorically forbidden, but they require categorically positive per-trade expR (or a clear cost-ratio advantage) to avoid catastrophic aggregation. F1 does not provide either at the as-specified parameter setting.

### 6.6 BTC vs ETH behavior

**Status:** Symbol-specific market-structure effects are persistent across families; §1.7.3 BTCUSDT-primary lock remains correctly calibrated.

- Phase 2x §4.6 / Phase 2o §C diagnosed the V1 breakout-family BTC/ETH asymmetry as a fact about market structure: ETH produces sharper trending moves; BTC produces longer chop/range periods.
- F1 inverts the asymmetry plausibly per Phase 3a §4.1(h): F1 should structurally favor BTC over ETH. Empirically: F1 BTC MED expR=−0.5227 vs ETH=−0.4024; ETH is *less bad* than BTC (the *opposite* of the Phase 3a §4.1(h) plausibility claim). The hypothesized BTC-friendliness of mean-reversion does not show up in the F1 empirical results at the as-specified parameters.
- §1.7.3 BTCUSDT-primary lock is therefore not threatened by F1's results: BTC remains the harder symbol to crack edge on; ETH research-comparison evidence remains informative but not deployment-relevant.

### 6.7 Slippage sensitivity

**Status:** §11.6 = 8 bps HIGH per side is correctly calibrated; cost-sensitivity is the binding gate for entry-axis and high-frequency families.

- Phase 2y closeout confirmed §11.6 = 8 bps HIGH (after analyzing R2's framework-FAIL at HIGH). The threshold has now successfully filtered R2 (MED PROMOTE / HIGH FAIL) and informatively contributed to F1's HARD REJECT (BTC HIGH expR=−0.70 catastrophic).
- The Phase 3c §7.2(iv) operator-mandated amendment ("BTC HIGH expR > 0") strengthens §11.6 for new-family first-execution gates. F1 demonstrates this strengthening was correctly motivated: F1's BTC HIGH expR=−0.70 is far from positive and far from the §10.4 floor of −0.50.
- Cost-sensitivity is now the most consistent failure-mode signal in the project: R2 failed §11.6; F1 failed §11.6 with margin; R3 / H0 / R1a / R1b-narrow are cost-robust by entry-axis preserving and exit-axis-redesigned design. **Future strategy candidates must demonstrate cost-resilience at HIGH slippage; this is a binding pre-execution discipline question.**

---

## 7. Should the active research program pause?

**Recommendation: YES — the active research program should pause / reset.**

Three independent reasons:

1. **The two-arc evidence pattern is consistent.** V1 breakout family is at its useful ceiling under the current framework (Phase 2x). The rank-1 near-term new-family candidate (F1) hard-rejected. Both arcs ran disciplined research under unchanged framework; both produced "less negative than H0 but not positive" outcomes (V1) or catastrophic-floor violations (F1). The pattern suggests that **identifying a positive-aggregate-edge strategy under the current framework + locks + thresholds + costs requires either a fundamentally different family hypothesis or a different framework**, not another candidate variant.
2. **Treadmill risk is now elevated, not merely present.** Phase 2x §7.2 flagged treadmill risk after R2's failure. Phase 3d-B2's HARD REJECT confirms the risk: authorizing another family variant or another spec-writing phase without a strong independently-developed hypothesis risks producing another mixed/failed result that does not advance the strategic question. The right response to elevated treadmill risk is to **pause and let the operator strategically choose**, not to keep pushing variants through framework discipline.
3. **No specific candidate is currently specified.** Phase 3a's family menu had eight candidates; F1 (rank-1) is now framework-FAILED. Phase 3a §6 ranked F2-F8 lower for reasons including overfitting risk (F4 range-bound; F8 ML-assisted), implementation complexity (F7 regime-first), v003 data dependency (F5 BTC/ETH spread/rotation may need new data), and uncertain mechanism (F2 volatility contraction redesigned). Authorizing F2-F8 without operator-driven hypothesis-development would be exactly the "spec-writing under research framing" Phase 2p §H.4 explicitly does not authorize.

The pause is **not** abandonment:

- R3 stays usable as a deployable variant if and when operator policy authorizes paper/shadow / Phase 4.
- R1a / R1b-narrow / R2 / F1 stay as research evidence; their findings inform any future hypothesis-development phase.
- §11.6 = 8 bps HIGH stays as the framework's cost-resilience gate.
- The operator may at any future time independently develop a falsifiable hypothesis and authorize a downstream docs-only phase to evaluate it.

The pause is **operator-strategic**: it surrenders the question "what to research next?" to operator decision, rather than answering it within the research-framework's own logic.

---

## 8. Operator decision menu

Seven options enumerated below. Each option's evaluation is preserved in the same shape Phase 2x §7 / Phase 3a §6 used.

### 8.1 Option A — Remain paused / research reset

**What it would answer:** What state should the project be in while the operator decides the next strategic move?

**Why it may be useful:**
- Preserves all current evidence as-is: R3 baseline-of-record; R1a/R1b-narrow/R2/F1 retained research evidence; §11.6 = 8 bps HIGH preserved; §1.7.3 locks preserved.
- Eliminates treadmill risk completely.
- Surrenders strategic direction to operator authority, where it belongs.
- Compatible with all subsequent options (B, C, D, E, F, G all remain available later).

**Why it may be dangerous:**
- Project loses momentum; strategic clarity may degrade if pause is indefinite.
- Operator may implicitly drift toward "I'll get back to it" without ever authorizing the next move.

**Violates current restrictions?** No.

**Should be recommended now?** **YES — primary recommendation.** This is the disciplined response to the two-arc evidence pattern.

### 8.2 Option B — Authorize a new Phase 3a-style discovery memo for a different strategy family

**What it would answer:** Among non-breakout, non-F1 strategy families, which is the strongest candidate for any potential next research arc?

**Why it may be useful:**
- Phase 3a's eight-candidate menu has seven remaining families (F2 volatility contraction redesigned; F3 trend pullback / continuation; F4 range-bound; F5 BTC/ETH relative strength; F6 funding-aware directional/carry; F7 regime-first framework; F8 ML-assisted forecasting). A fresh discovery memo could re-rank these in light of F1's HARD REJECT and the Phase 3d-B2 mechanism findings.
- Disciplined entry path (docs-only survey before any spec-writing).

**Why it may be dangerous:**
- Repeats the Phase 3a → 3b → 3c → 3d sequence for the next-ranked candidate; commits the project to another full F1-shape research arc which may again hard-reject.
- Treadmill risk: F1's M3-PASS / framework-FAIL pattern may recur on F2-F8 candidates that share F1's high-frequency / tight-target geometry (F2, F4, F6 in particular).
- Phase 3a §5 already classified F2-F8 with various near-term restrictions; the candidates ranked below F1 may be *less* near-term suitable than F1, not equivalently.

**Violates current restrictions?** No (a discovery memo is docs-only; Phase 3e itself is the same shape).

**Should be recommended now?** **NO.** Better deferred until the operator independently determines a non-V1, non-F1 hypothesis is worth surveying. Authorizing Option B now without operator hypothesis-development would be exactly the post-Phase-2w treadmill that Phase 2x §7.2 warned against.

### 8.3 Option C — Revisit Phase 3a second-ranked family (F6 funding-aware directional/carry) as a docs-only spec candidate

**What it would answer:** Is the Phase 3a §6.2 second-ranked family (F6) a credible spec candidate now?

**Why it may be useful:**
- F6 leverages an information source (Binance funding rates, already in v002) that V1 + F1 do not exploit. Funding-rate extremes are a structurally different signal from price-action-derived predicates.
- Phase 3a §4.6 noted F6's BTC-friendliness (BTC funding-rate magnitude > ETH per Binance USDⓈ-M empirical pattern), which complements §1.7.3 BTCUSDT-primary.
- Lower expected trade frequency than F1 (funding-rate extremes are rarer events), reducing the cost-load failure mode that hit F1.

**Why it may be dangerous:**
- Phase 3a §6.2 ranked F6 second, not first, for reasons including (a) funding-rate extremes are mechanically a directional / carry signal, not a market-microstructure signal; (b) the empirical funding-rate distribution may produce too few signals for §10.3 statistical power; (c) the funding-rate cost realism is more delicate than slippage realism (funding accrues over hold time, not at fill).
- Authorizing F6 spec-writing now bypasses the Phase 3a re-ranking exercise that Option B would do; that re-ranking may discover a better-than-F6 candidate in light of F1's HARD REJECT.
- The Phase 3a § 4.6 plausibility claims are weaker than F1's were; weaker plausibility under unchanged discipline likely produces another framework-FAIL.

**Violates current restrictions?** No (a spec memo is docs-only).

**Should be recommended now?** **NO.** Premature without operator-developed hypothesis or fresh discovery survey.

### 8.4 Option D — Revisit paper/shadow / Phase 4 readiness around R3 as governance discussion only (not authorization)

**What it would answer:** What would the operator need to decide / verify / build before authorizing a paper/shadow or Phase 4 phase on the existing R3 baseline-of-record?

**Why it may be useful:**
- R3 is the baseline-of-record per Phase 2p §C.1 and is the strongest single evidence the project has. If the operator wants to make any move toward eventually deploying R3, the gating questions (paper/shadow scope; Phase 4 runtime/state/persistence implementation; operator readiness; production-key timing; NUC / dashboard / alert-route readiness; backup/restore readiness) need to be enumerated.
- A governance discussion is purely documentary and does not commit the project to any execution.

**Why it may be dangerous:**
- Conflating "governance discussion" with "implementation authorization" risks accidentally drifting toward Phase 4 work without the explicit phase-gate approval Phase 2p §H.4 / Phase 2x §7.4 require.
- R3's per-trade negative aggregate edge (BTC R-window expR=−0.240 / ETH=−0.351) means paper/shadow on R3 would expect to lose money cleanly; R3 is "less negative than H0" not "break-even". Deployment on R3 would convert "reduced losses" into real losses unless the regime-incompatibility resolves out-of-sample.
- Phase 2p §F enumerates the future-resumption pre-conditions; revisiting them now without operator-driven readiness signals invites mission creep.

**Violates current restrictions?** Strict reading: Phase 3e operator brief says "Do not start paper/shadow planning". A governance-discussion-only docs phase is on the boundary. If interpreted as "begin planning what eventual paper/shadow would look like", it violates the brief; if interpreted as "review the existing pre-conditions catalog", it does not.

**Should be recommended now?** **NO.** Operator policy continues to defer paper/shadow indefinitely; revisiting it now risks crossing the deferral boundary.

### 8.5 Option E — External execution-cost evidence gathering

**What it would answer:** Are the current §11.6 = 8 bps HIGH-slippage assumption and the canonical taker fee rate (0.0005) calibrated correctly against current Binance USDⓈ-M live execution costs?

**Why it may be useful:**
- The Phase 2y closeout preserved §11.6 at 8 bps "until external execution-cost evidence justifies revision". If the operator independently gathers fresh slippage / fee evidence (e.g., from current Binance fee schedules, current depth/spread profiles, current funding-rate distributions), Phase 2y's preservation could be re-opened.
- Cost-policy evidence is purely external to the strategy research; it does not authorize any strategy work.

**Why it may be dangerous:**
- Risks being misinterpreted as "find a way to pass §11.6 by lowering the threshold". This would be exactly the §11.3.5 forbidden post-hoc loosening. Cost-policy revision must be **independent** of any specific candidate's framework outcome.
- Even if external evidence justifies relaxing §11.6, it would not retroactively rescue R2 or F1; both are framework-FAILED under the rules in place at execution time.

**Violates current restrictions?** No (external evidence gathering is docs/research).

**Should be recommended now?** **NO.** The §11.6 = 8 bps preservation is recent (Phase 2y closeout); no fresh external evidence is currently asserted. Revisiting cost-policy without external trigger risks the post-hoc-loosening trap.

### 8.6 Option F — F1-prime or target-subset hypothesis planning

**What it would answer:** Could a regime-conditional F1-prime spec, or a target-subset selection rule, rescue F1's M3-PASS evidence into a framework-PASSING strategy?

**Why it may be useful:**
- F1's M3-PASS is empirically informative (SMA(8) target subset is profitable in isolation). If a falsifiable, mechanism-grounded, framework-discipline-compliant hypothesis can construct a *prospective* selection predicate (not retrospective TARGET-only filtering), the M3 evidence becomes potentially developable.
- Phase 2p §F.1 / Phase 2o §F.1 contemplated regime-conditional R1a-prime as analogous future hypothesis territory.

**Why it may be dangerous:**
- §5.4 above explains why this is forbidden under §11.3.5 single-spec discipline: "select the M3 subset and tune around it" is exactly post-hoc loosening. Any F1-prime spec must come from independently developed operator hypothesis, not from carving out F1's profitable subset.
- Treadmill risk: each post-hoc subset-rescue attempt invites the next. The discipline that produced clean PROMOTE / FAIL decisions on R3 / R1a / R1b-narrow / R2 / F1 depends on resisting subset-rescue framing.
- No specific F1-prime hypothesis is currently developed by the operator. Authorizing the planning phase without a hypothesis is "spec-writing under research framing".

**Violates current restrictions?** Phase 3e brief says "Do not commence F1-prime [...] hypothesis development." Strict reading: this option violates the brief.

**Should be recommended now?** **NO. Forbidden by Phase 3e brief.** F1-prime planning is reserved for a separately-authorized future operator decision with an independently-developed hypothesis.

### 8.7 Option G — Stop active strategy research for now

**What it would answer:** Should the project stop all active strategy-research work indefinitely?

**Why it may be useful:**
- Strongest possible signal that strategic direction is operator-driven from this point forward.
- Eliminates treadmill risk completely.
- Makes the eventual return-to-research conscious and operator-developed.

**Why it may be dangerous:**
- Effectively the same as Option A (remain paused) but framed more strongly. The functional difference is whether the project state is "paused, awaiting operator decision" (Option A) versus "stopped, awaiting operator restart" (Option G).
- "Stop indefinitely" framing may inadvertently signal that the existing R3 / H0 evidence is stale or invalidated, which is not the case.

**Violates current restrictions?** No.

**Should be recommended now?** **NO** — Option A's pause framing is operationally equivalent and less rhetorically strong. Option G is functionally a stronger version of Option A; both can be revisited if the operator wants to make the stop more explicit later.

### 8.8 Decision menu summary

| Option | Description | Violates Phase 3e brief? | Recommended now? |
|--------|-------------|:-:|:-:|
| **A** | Remain paused / research reset | NO | **YES (primary)** |
| B | New Phase 3a-style discovery memo for a different family | NO | NO |
| C | F6 funding-aware spec candidate revisit | NO | NO |
| D | R3 paper/shadow / Phase 4 governance discussion | Boundary (likely yes) | NO |
| E | External execution-cost evidence gathering | NO | NO |
| F | F1-prime / target-subset hypothesis planning | YES | NO (forbidden) |
| G | Stop active strategy research | NO | NO (Option A is operationally equivalent) |

---

## 9. Recommended next operator decision

**Remain paused.**

Specifically:

- **Hold project state at the post-Phase-3d-B2 boundary.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 retained research evidence; §11.6 = 8 bps HIGH preserved; §1.7.3 locks preserved; no paper/shadow planning; no Phase 4 work; no live-readiness work; no deployment work; no production-key creation; no exchange-write capability; no MCP / Graphify / `.mcp.json`; no credentials.
- **No next research phase authorized.** Phase 3e is docs-only and terminal-as-of-now.
- **Operator decides whether and when to authorize any subsequent phase.** Acceptable future authorizations include: another docs-only discovery / spec / review phase; an operator-developed hypothesis spec memo; a future paper/shadow planning phase (when operator policy lifts that deferral); Phase 4 runtime / state / persistence implementation (when operator policy lifts that deferral). Any such authorization is operator-authority and is not pre-empted by Phase 3e.

This recommendation conforms to the Phase 3e brief constraint that "Acceptable recommendations: remain paused; authorize another docs-only discovery/review phase; or hold for operator strategic choice. Do NOT recommend implementation, backtesting, paper/shadow, Phase 4, or deployment."

The recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

## 10. Update to `docs/00-meta/current-project-state.md`

The canonical project-state document is updated in the same Phase 3e branch / commit to reflect:

- Phase 3d-A merged into `main`.
- Phase 3d-B1 merged into `main`.
- Phase 3d-B2 merged into `main`.
- F1 framework verdict: HARD REJECT.
- F1 retained as research evidence only.
- Phase 3d-B2 terminal for F1.
- R3 remains V1 breakout baseline-of-record.
- H0 remains V1 breakout framework anchor.
- R1a, R1b-narrow, R2, F1 remain retained research evidence only.
- R2 remains FAILED — §11.6 cost-sensitivity blocks.
- §11.6 HIGH = 8 bps per side preserved.
- No next phase authorized.
- No paper/shadow authorized.
- No Phase 4 authorized.
- No live-readiness authorized.
- No deployment authorized.

The diff to `current-project-state.md` is intentionally narrow: it advances the "Current Phase" and "Recently Completed" sections to reflect Phase 3d-A / 3d-B1 / 3d-B2 and Phase 3e, and updates the readiness-status table accordingly. **No threshold change. No strategy-parameter change. No project-lock change. No paper/shadow / Phase 4 / live-readiness / deployment authorization.**

---

## 11. Explicit preservation list

Phase 3e is docs-only and explicitly preserves all of the following verbatim:

- **No threshold changes.** Phase 2f §10.3 / §10.4 / §11.3 / §11.4 / §11.6 = 8 bps HIGH per side preserved.
- **No strategy-parameter changes.** R3 sub-parameters (`exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`); H0 baseline (range-based setup, 1h binary slope-3 bias + EMA(50)/EMA(200), 0.10 × ATR breakout buffer, staged-trailing exit, 0.10 × ATR structural-stop buffer); R1a sub-parameters (volatility-percentile X=25 / N=200); R1b-narrow sub-parameter (slope-strength magnitude S=0.0020); R2 sub-parameters (pullback-retest with 8-bar validity window; 5-step precedence; fill-time stop-distance re-check); F1 spec axes (overextension window 8; threshold 1.75 × ATR(20); mean-reference window 8; stop buffer 0.10 × ATR(20); time-stop 8 bars; stop-distance band [0.60, 1.80] × ATR(20); cooldown rule; no regime filter; market entry at next-bar open). All preserved verbatim.
- **No project-lock changes.** §1.7.3 locks (BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; one active protective stop max; 0.25% risk per trade; 2× leverage cap; mark-price stops; v002 datasets; one-way mode; isolated margin; no pyramiding; no reversal while positioned; no hedge mode) preserved verbatim.
- **No MCP / Graphify / `.mcp.json` activation.** No MCP server enabled; no Graphify integration; no `.mcp.json` file created or modified.
- **No credentials.** No production / sandbox / testnet API keys requested, created, or used. No `.env` file modified. No secrets in any committed file.
- **No exchange-write paths.** No exchange-write capability proposed, implemented, or enabled. `BacktestAdapter.FAKE` remains the only adapter type in the engine.
- **No `data/` commits.** Phase 3e commits are limited to `docs/00-meta/current-project-state.md` and the two new `docs/00-meta/implementation-reports/` files.

---

**End of Phase 3e post-F1 research consolidation memo.** Phase 3e records the post-F1 project-state consolidation, summarizes the V1 breakout + F1 mean-reversion two-arc research history, evaluates seven operator-decision options against the Phase 3e brief constraints, and recommends **remain paused** as the disciplined response to the two-arc evidence pattern. R3 remains V1-breakout baseline-of-record; H0 remains framework anchor; R1a / R1b-narrow / R2 / F1 retained research evidence; §11.6 = 8 bps HIGH preserved; §1.7.3 locks preserved verbatim. **No next phase authorized.** **No paper/shadow / Phase 4 / live-readiness / deployment / MCP / Graphify / `.mcp.json` / credential / exchange-write change.** **No `data/` commits.** Phase 3e is docs-only; the operator decides whether and when to authorize any subsequent phase. Awaiting operator review.
