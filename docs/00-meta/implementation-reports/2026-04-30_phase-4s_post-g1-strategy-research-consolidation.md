# Phase 4s — Post-G1 Strategy Research Consolidation Memo

**Authority:** Operator authorization for Phase 4s (Phase 4r §"Operator decision menu" Option A primary recommendation: Phase 4s — Post-G1 Strategy Research Consolidation Memo, docs-only). Phase 4r (G1 backtest execution; Verdict C HARD REJECT — terminal for G1 first-spec); Phase 4q (G1 backtest-plan methodology binding); Phase 4p (G1 strategy spec locked); Phase 4o (G1 hypothesis-spec); Phase 4n (Candidate B selection); Phase 4m (post-V2 consolidation; 18-requirement fresh-hypothesis validity gate); Phase 4l (V2 backtest execution; Verdict C HARD REJECT — terminal for V2 first-spec); Phase 4k (V2 backtest-plan methodology); Phase 4j §11 (metrics OI-subset partial-eligibility binding); Phase 4i (V2 acquisition); Phase 4f (external research landscape + V2 candidates); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 3r §8 (mark-price gap governance); Phase 3t §12 (validity gate); Phase 3c §7.3 (catastrophic-floor predicate); Phase 2p §C.1 (R3 baseline-of-record); Phase 2i §1.7.3 (project-level locks); `docs/03-strategy-research/v1-breakout-strategy-spec.md`; `docs/03-strategy-research/v1-breakout-backtest-plan.md`; `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`; `docs/04-data/data-requirements.md`; `docs/07-risk/stop-loss-policy.md`; `docs/07-risk/position-sizing-framework.md`; `docs/07-risk/exposure-limits.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/ai-coding-handoff.md`; `docs/00-meta/implementation-ambiguity-log.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4s — **Post-G1 Strategy Research Consolidation Memo** (docs-only). Records the Phase 4r G1 backtest rejection in the project's strategy-research record, updates the rejection topology, identifies reusable lessons, preserves all retained verdicts and locks, and recommends the next operator choice. **Phase 4s does NOT run a backtest, write any code, acquire data, modify data, modify manifests, modify `src/prometheus/`, modify tests, modify scripts, create a new strategy candidate, create G1-prime / G1-narrow / G1-extension, amend Phase 4p / Phase 4q, or authorize Phase 4t.** **Phase 4s is text-only.**

**Branch:** `phase-4s/post-g1-strategy-research-consolidation`. **Memo date:** 2026-05-03 UTC.

---

## Summary

Phase 4s is the third strategy-rejection consolidation memo in the project record (after Phase 3e for F1; Phase 3k for D1-A; Phase 4m for V2). It records the Phase 4r G1 — Regime-First Breakout Continuation backtest outcome (**Verdict C HARD REJECT**, binding driver **CFP-1 critical** and independent driver **CFP-9**), reaffirms every retained verdict and project lock, updates the rejection topology with **G1's distinct failure mode (regime-gate-meets-setup intersection sparseness)**, distinguishes that mode from the four prior rejection modes (R2 cost-fragility; F1 catastrophic-floor; D1-A mechanism / framework mismatch; V2 design-stage incompatibility), extracts ten reusable insights without authorizing any rescue, comparatively analyzes G1 against V2 (the closest structural analog) and against R2 / F1 / D1-A (the prior rejection family), reaffirms the Phase 4m 18-requirement fresh-hypothesis validity gate as binding for any future ex-ante hypothesis, and recommends **remain paused** as primary with an explicit conditional secondary path for a future docs-only fresh-hypothesis discovery memo *only* if the operator explicitly chooses to continue research. **Phase 4s does NOT authorize any subsequent phase.** **G1 first-spec is terminally HARD REJECTED as retained research evidence only.** **No project lock changed.** **No retained verdict revised.**

## Authority and boundary

- **Authority granted:** create the Phase 4s consolidation memo; create the Phase 4s closeout; recommend a primary and conditional-secondary next operator choice; document G1 rejection mechanism, lessons, and forbidden-rescue observations; reaffirm the Phase 4m 18-requirement fresh-hypothesis validity gate.
- **Authority NOT granted:** create any new strategy candidate (forbidden); name V3 / G2 / H2 / any successor (forbidden); amend Phase 4p G1 strategy-spec or Phase 4q methodology (forbidden); rerun any backtest (forbidden); acquire / modify / patch / regenerate / replace data (forbidden); modify manifests (forbidden); create v003 (forbidden); modify `src/prometheus/`, tests, or existing scripts (forbidden); start Phase 4t or any successor phase (forbidden); authorize paper / shadow / live / exchange-write / production keys / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials (forbidden).
- **Hard rule:** Phase 4s is text-only. No code is written. No data is touched. No backtest is run.
- **Naming hard rule:** Phase 4s must always refer to G1 — Regime-First Breakout Continuation as the rejected first-spec. Phase 4s must NOT introduce any "G1-prime", "G1-narrow", "G1-extension", "G1 hybrid", "V3", "H2", "G2", or any other rescue-implying label.

## Starting state

```text
Branch (Phase 4s):   phase-4s/post-g1-strategy-research-consolidation
main / origin/main:  03a626ff260aaf8608d9ee5f9fc2451a14361bfb (unchanged)
Phase 4r merge:      24ab8355597c033ae57df25d7c5f8ec0c6a21542 (merged)
Phase 4r housekeeping: 03a626ff260aaf8608d9ee5f9fc2451a14361bfb (merged)
Working-tree state:  clean (no tracked modifications); only gitignored
                     transients .claude/scheduled_tasks.lock and
                     data/research/ are untracked and will not be committed.
Quality gates (verified at memo creation):
  ruff check . PASS
  pytest 785 PASS
  mypy strict 0 issues across 82 source files
```

## Why this memo exists

The project record contains three prior post-rejection consolidation memos (Phase 3e for F1; Phase 3k for D1-A; Phase 4m for V2) and one prior post-arc closure memo (Phase 3t for the 5m diagnostic thread). Each preserves what the corresponding research arc taught the project, what it explicitly did not teach, and why the correct project state was paused. Phase 4r produced a fourth strategy-rejection event under similar structural conditions to V2 but at a different mechanism layer (regime-gate sparseness rather than stop-distance-filter incompatibility). Without an explicit consolidation memo, the G1 outcome would risk being reduced to "another HARD REJECT" rather than carrying its specific lesson — that **regime gates can destroy sample size and prevent expectancy evaluation entirely**, which is a structurally distinct failure mode and should be remembered as such. Phase 4s captures that lesson and updates the rejection topology accordingly.

Phase 4s also reaffirms the **Phase 4m 18-requirement fresh-hypothesis validity gate** as binding for any future ex-ante hypothesis, and explicitly forbids using Phase 4r forensic numbers (the 2.03% active fraction; the 124 always-active baseline trades; the −0.34 mean_R) as parameter-selection inputs for any future strategy work — the same anti-data-snooping discipline applied after V2 (Phase 4l forensic numbers).

## Relationship to Phase 4r

- Phase 4r executed the G1 backtest exactly under the Phase 4q methodology and emitted **Verdict C — G1 framework HARD REJECT**.
- Phase 4r did NOT modify Phase 4p G1 strategy spec, Phase 4q methodology, Phase 4j §11 governance, Phase 4k methodology, or any retained verdict.
- Phase 4r did NOT implement G1 in `src/prometheus/`, modify runtime / execution / persistence / risk / exchange / strategy modules, modify tests, modify existing scripts, acquire data, modify manifests, or create v003.
- Phase 4r local outputs under `data/research/phase4r/` are gitignored / not committed.
- Phase 4r recommended Phase 4s as primary and remain-paused as conditional secondary.
- The operator now explicitly authorized Phase 4s.
- **Phase 4s is the methodologically-disciplined post-mortem of the G1 outcome**, not a rescue mechanism. Phase 4s does not amend any Phase 4p / Phase 4q decision, does not run any G1 rerun, and does not propose any G1-prime / G1-narrow / G1-extension.

## Phase 4r result recap

```text
Train-best variant:                    id=0
Variant label:                         E=0.30 | ATR=[20,80] | Vliq=0.80 |
                                       Fund=[15,85] | K=2

G1 OOS BTC HIGH (train-best):
  trade_count                          0
  mean_R                               0
  total_R                              0
  sharpe                               0
  profit_factor                        0
  max_dd_R                             0

G1 BTC OOS HIGH across all 32 variants: every variant trade_count = 0.

Always-active baseline (id=0, BTC OOS HIGH; same setup, stop, target,
                                            time-stop, cost; no regime gate):
  trade_count                          124
  mean_R                               -0.34
  (loss-making at HIGH cost; confirms breakout-and-stop machinery fired but
   was not profitable under §11.6 = 8 bps)

Inactive-population pseudo-trades (id=0, BTC OOS HIGH):
  trade_count                          124
  mean_R                               -0.34

ETHUSDT comparison:
  Train-best variant id=0 carried from BTC.
  ETH G1 produced 0 qualifying trades for train-best across all windows
  and cost cells.
  ETH cannot rescue BTC.

Mechanism checks:
  M1 (regime-validity negative test):
    diff = active_mean_R - inactive_mean_R = 0.0
    bootstrap CI [0.0, 0.0]
    threshold +0.10R AND CI_lower>0   FAIL
  M2 (regime-gating value-add):
    diff = G1_mean_R - always_active_mean_R = 0.0
    bootstrap CI [0.0, 0.0]
    threshold +0.05R AND CI_lower>0   FAIL
  M3 (inside-regime co-design):
    BTC OOS HIGH mean_R = 0; trade_count = 0
    threshold mean_R>0 AND trade_count>=30 AND no CFP-1/2/3   FAIL
  M4 (cross-symbol robustness):
    ETH diff = 0.0; directional consistency = true (degenerate 0=0)
    trivial PASS; CFP-4 catches it.

Search-space control:
  PBO train -> validation:             0.000
  PBO train -> OOS:                    0.000
  PBO CSCV (S=16; C(16,8)=12,870):     0.500
  DSR per variant:                     all 0.000

Catastrophic-floor predicates:
  CFP-1   TRIGGERED   binding (critical)
                      32 / 32 variants below 30 OOS BTC HIGH trades;
                      train-best variant produced 0 OOS HIGH trades.
  CFP-2   not triggered
  CFP-3   TRIGGERED   subordinate / mechanical (PF=0 under empty arrays)
  CFP-4   TRIGGERED   subordinate / degenerate (M3 BTC FAIL with M4 ETH
                      trivial PASS; ETH cannot rescue BTC)
  CFP-5   not triggered
  CFP-6   not triggered (PBO 0.000 / 0.000 / 0.500; not strictly > 0.50)
  CFP-7   not triggered (no OOS HIGH G1 trades)
  CFP-8   not triggered (sensitivity cells also produce zero trades;
                         degradation 0.0; non-degraded by construction)
  CFP-9   TRIGGERED   independent (BTC OOS active fraction 2.03% < 5%)
  CFP-10  not triggered (audit count = 0)
  CFP-11  not triggered (no future-bar use; no signal dependency;
                          signal_outside_active_count = 0)
  CFP-12  not triggered (audit counts = 0)

Verdict:                               C — G1 framework HARD REJECT.
```

## G1 first-spec verdict

**G1 first-spec is terminally HARD REJECTED as retained research evidence only.** The verdict is binding and not subject to revision under Phase 4r forensic re-interpretation. The G1 strategy specification stands in the project record exactly as Phase 4p locked it; Phase 4q methodology stands exactly as locked; Phase 4r executed both verbatim and produced Verdict C. No rerun, no amendment, no rescue.

## G1 rejection mechanism

The Phase 4r outcome is best understood not as "G1 trades lost money under HIGH cost" but as **"G1 produced no trades at all on the OOS HIGH cell for the train-best variant, because the regime-active windows and breakout-trigger arrival times did not intersect at sufficient frequency."** Two independent forensic observations support this interpretation:

1. **Always-active baseline produces 124 trades on BTC OOS HIGH** at mean_R = −0.34 for the train-best variant. The breakout-and-stop simulation works; the breakout setup fires; the stop / target / time-stop logic completes round-trip trades. Costs are realistic. The mean expectancy is negative under §11.6 = 8 bps slippage, which is consistent with R2's locked verdict and Phase 3l's "B — current cost model conservative but defensible" assessment.
2. **Inactive-population pseudo-trades produce 124 trades** at mean_R = −0.34. Inactive-state breakouts are not profitable either, ruling out the alternative explanation that the regime gate is "filtering out the only profitable subset." The breakout system, as currently configured on Phase 4i v001 30m / 4h klines, does not have a profitable subset that the regime gate excludes.

Therefore G1 failed at the **intersection** of:

- **regime gate sparsity** — the five-dimension AND classifier (HTF trend AND DE_4h ≥ E_min AND ATR percentile in band AND relative-volume ≥ V_liq_min AND funding percentile in band) is, under the Phase 4p locked thresholds, structurally narrow on the v002 / Phase 4i datasets across the locked Phase 4k validation windows;
- **breakout setup arrival timing** — the 30m Donchian breakout (`N_breakout = 12`, `B_atr = 0.10`) plus the structural stop and stop-distance gate happens to fire at moments largely uncorrelated with regime-active windows;
- **sample-size / trade-count floor** — Phase 4p / Phase 4q's 30-trade minimum is appropriate for DSR / bootstrap; the train-best variant's BTC OOS HIGH active population is empty, well below the floor;
- **HIGH-cost realism** — even if a few trades did fire, §11.6 = 8 bps would still apply; the always-active baseline confirms the cost model bites.

This intersection failure is the **specific G1 lesson** for the project record: a regime hypothesis can satisfy every internal-coherence check (Phase 4p classifier predeclared before data; Phase 4q methodology predeclared before code; Phase 4r execution fully deterministic) and still fail at *operational geometry* — the regime gate and the entry trigger live in different statistical timescales, and their intersection on the actual data is too sparse to evaluate.

## Relationship to Phase 4m consolidation

Phase 4m consolidated the post-V2 outcome into the project record. Phase 4m §"Forbidden rescue observations" prohibited:

```text
no V2 with widened stop-distance;
no V2 N1 change;
no V2 stop-filter removal;
no V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
no F1 with extra filters / F1-prime;
no D1-A with extra filters / D1-A-prime / D1-B / V1-D1 hybrid / F1-D1 hybrid;
no R2 with cheaper costs;
no immediate backtest based on Phase 4l observed root cause;
no Phase 4g / Phase 4j / Phase 4k methodology amendment based on Phase 4l result;
no choosing parameters from Phase 4l forensic numbers;
no treating Q1 / Q2 / Q3 / Q6 5m diagnostic findings as rule candidates.
```

Phase 4s extends this discipline to G1 verbatim: see "Forbidden G1 rescue observations" below.

Phase 4m §"Fresh-hypothesis validity gate" defined 18 binding requirements that any future ex-ante hypothesis must satisfy. Phase 4s reaffirms those requirements as binding for any future hypothesis after G1 (see "Fresh-hypothesis validity gate reaffirmation"). The Phase 4m gate is not amended; it is preserved verbatim.

## Updated strategy verdict map

```text
H0           : FRAMEWORK ANCHOR (Phase 2i §1.7.3)
R3           : BASELINE-OF-RECORD (Phase 2p §C.1 — V1 breakout)
R1a          : RETAINED — NON-LEADING (research evidence only)
R1b-narrow   : RETAINED — NON-LEADING (research evidence only)
R2           : FAILED — §11.6 cost-sensitivity gate blocks
                (Phase 2w §16.1; M1 ✓, M3 ✓, M2 ✗ partial mechanism;
                 slippage-fragile)
F1           : HARD REJECT (Phase 3c §7.3 catastrophic-floor predicate;
                Phase 3d-B2 terminal)
D1-A         : MECHANISM PASS / FRAMEWORK FAIL — other (Phase 3h §11.2;
                Phase 3j terminal)
5m diagnostic thread : OPERATIONALLY CLOSED (Phase 3t)
V2           : HARD REJECT — structural CFP-1 critical (Phase 4l;
                terminal for V2 first-spec)
G1           : HARD REJECT — CFP-1 critical AND CFP-9 (Phase 4r;
                terminal for G1 first-spec)
```

No prior verdict is revised by Phase 4s. No project lock is changed by Phase 4s. R3 remains baseline-of-record. H0 remains framework anchor. §11.6 = 8 bps HIGH per side preserved verbatim. §1.7.3 0.25% risk / 2× leverage / one-position locks preserved. v002 verdict provenance preserved. Phase 3q mark-price 5m manifests `research_eligible: false` preserved. Phase 3r §8 mark-price gap governance preserved. Phase 3v §8 stop-trigger-domain governance preserved. Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance preserved. Phase 4j §11 metrics OI-subset partial-eligibility binding rule preserved (unused by G1). Phase 4k V2 backtest-plan methodology preserved. Phase 4p G1 strategy-spec preserved. Phase 4q G1 methodology preserved.

## Updated rejection topology

```text
Strategy   Rejection mode                                  Lesson
---------- ----------------------------------------------- ---------------------------------------------------------
R2         cost-fragility                                  Partial mechanism evidence (M1 ✓, M3 ✓) can fail §11.6
                                                            HIGH-cost survival; slippage realism is a hard gate.
F1         catastrophic-floor / bad full-population         Profitable subsets do not rescue a losing framework;
            expectancy                                       the catastrophic-floor predicate enforces this.
D1-A       mechanism / framework mismatch                  Context (here funding) may carry information at the
            ("MECHANISM PASS / FRAMEWORK FAIL — other")     mechanism layer (M1 PASS) without delivering at the
                                                            framework / promotion layer (M2 ✗ in the form required
                                                            for promotion).
V2         design-stage incompatibility                    Setup window / structural stop / target / position sizing
                                                            must be co-designed; importing one element (e.g. stop-
                                                            distance bounds) from a different design produces
                                                            structural rejection at the pre-trade gate.
G1         regime-gate-meets-setup intersection sparseness Regime filters can destroy sample size and prevent
                                                            expectancy evaluation entirely. A regime hypothesis must
                                                            be validated for both selectivity AND opportunity-rate
                                                            preservation, not selectivity alone.
```

The five rejection modes are **structurally distinct**. They do not share a common failure mechanism; they share only the discipline of having been predeclared and tested under §11.6 cost realism with bootstrap / DSR / PBO / CSCV correction.

## Strategy-family lessons after G1

Phase 4f distinguished transferable from non-transferable institutional families. After G1's regime-gate failure, Phase 4f's family typology is preserved; G1 does not change it. Specifically:

- **Time-series momentum / trend-following remains the strongest theoretically transferable family** (Moskowitz / Ooi / Pedersen 2012; Hurst / Ooi / Pedersen 2017; Han / Kang / Ryu 2024). G1's failure is a *first-spec* failure for one regime-gating shape (5-dimension AND-classifier on BTCUSDT 30m / 4h), not a refutation of trend continuation as a research family.
- **Mean-reversion remains de-prioritized** after F1 HARD REJECT; G1's outcome does not shift this.
- **Funding-context as risk-context only** (Phase 4f §"Crypto derivatives-flow indicators") remains a reasonable framing; G1 used funding as a regime *condition*, not a directional trigger, and that framing was not the primary cause of G1's failure (the failure was the AND-conjunction of all five classifier dimensions, not funding alone).
- **5m remains diagnostic-only** (Phase 3t §14.2). G1 did not use 5m, and Phase 4s does not authorize 5m as a strategy signal layer.
- **Market-making / HFT remains rejected** (not transferable to Prometheus substrate).
- **ML-first black-box forecasting remains rejected** (project remains rules-based per §1.7.3).

## Cost-sensitivity lessons after G1

§11.6 = 8 bps HIGH per side is preserved verbatim. After G1, the cost record now includes:

- **Always-active baseline on G1's setup** produced mean_R = −0.34 on BTC OOS HIGH at 8 bps. This adds an *independent data point* consistent with R2's §11.6 cost-fragility verdict and Phase 3l's "B — conservative but defensible" cost-model assessment. The breakout-and-stop machinery configured on Phase 4i v001 30m / 4h with N_breakout = 12 and stop-distance bounds [0.50, 2.20] × ATR(20) does not survive HIGH cost in the always-active configuration.
- **No HIGH-cost relaxation is justified**. Phase 4r does not authorize a Phase 3l-style cost-model revision. The cost model continues to be defended as conservative but appropriate under the project's safety-first posture.

## Regime-gating lessons

The single most actionable lesson of G1 is:

> **A regime classifier's value is bounded by the rate at which entry opportunities arrive *inside* the active state, not by the active state's selectivity alone.**

Specifically, after G1:

- A regime classifier reporting `regime_active` for X% of bars does NOT imply X% of entry opportunities. Entry opportunities are filtered through the entry rule's own arrival statistics; the joint event `(regime_active AND breakout_setup AND stop_distance_passes)` is the binding rate.
- A regime classifier validated only on selectivity (e.g., "regime_active periods have higher trend persistence") can still produce zero qualifying entries if the entry rule's typical arrival timing is concentrated outside `regime_active`.
- AND-conjunction classifiers risk multiplicative narrowing: each additional classifier dimension cuts the active fraction; the joint with the entry rule cuts it further. G1's five-dimension AND classifier intersected with the breakout rule's stop-distance gate to produce zero qualifying entries on the OOS HIGH cell.
- Predeclaring a minimum active fraction (CFP-9 < 5%) is appropriate; predeclaring a minimum active-AND-setup arrival rate would have caught this earlier and could be a useful design discipline for any future regime-first hypothesis (this is an *observation*, not an authorization to amend Phase 4q methodology).
- Always-active and inactive-population baselines are valuable structural negative controls. Phase 4r's M1 / M2 negative tests, even when degenerate under empty active populations, did surface the failure mechanism via the always-active baseline.

## Breakout-mechanism lessons

After G1, the breakout-mechanism record includes:

- **30m Donchian breakout (N_breakout = 12, B_atr = 0.10)** combined with **structural stop (N_stop = 12, S_buffer = 0.10) bounded by [0.50, 2.20] × ATR(20)** produces a viable trade-generation rate (always-active baseline = 124 BTC OOS HIGH trades over ~21 months; ~6 trades / month) but is not profitable under §11.6 = 8 bps. This is consistent with the broader R3-vs-R2 boundary: structural-stop breakout systems can fire at reasonable rates but require either tighter cost models or a profitable mechanism beyond the breakout itself.
- **The 30m timeframe is not refuted as a signal layer.** G1's failure was at the regime intersection, not at the timeframe. Phase 3n / 3p / 3s / 3t's "5m diagnostic-only, not strategy signal" governance is unrelated and remains intact.
- **G1 does not refute regime-first as a research concept.** It refutes *one* particular regime-first first-spec on *one* particular breakout setup on *one* particular dataset.

## Stop / target / sizing lessons after G1

§1.7.3 (0.25% risk / 2× leverage / one-position max / mark-price stops) is preserved verbatim. The stop / target / sizing model used by G1 — fixed-R N_R = 2.0; T_stop = 16; structural stop with [0.50, 2.20] × ATR bounds; 0.25% risk; 2× leverage cap — is structurally consistent with R3 / V2 / G1 design. None of these design elements is implicated in G1's failure; the failure is upstream at the regime / breakout intersection.

After V2 the project lesson was *setup geometry / stop / target / sizing must be co-designed*. After G1 the corresponding lesson is *regime gate / entry rule / sample-size viability must be co-designed*. These are complementary discipline areas; neither rescues the other.

## Data / governance lessons

The data and governance layers performed correctly during G1:

- **Manifest SHA pinning** (`manifest_references.csv`) worked as designed. Six manifests were SHA-pinned at run start.
- **`research_eligible` verification** was applied; the v002 funding manifest's lack of the field was handled by the documented inheritance convention without compromising integrity.
- **Phase 4j §11 metrics OI-subset governance** was preserved but unused by G1. Audit counters confirm zero metrics OI access. The governance rule remains binding for any future phase that *does* use metrics OI.
- **Phase 3r §8 mark-price gap governance** preserved (no mark-price loaded).
- **Phase 3v §8 stop-trigger-domain governance** preserved (`stop_trigger_domain = trade_price_backtest` for research; future runtime would require `mark_price_runtime` separately).
- **Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance** preserved (G1 used `break_even_rule = disabled`, `ema_slope_method = discrete_comparison`, `stagnation_window_role = metric_only`).
- **Phase 4q forbidden-input enforcement** worked. Audit counters: zero metrics OI, zero ratio columns, zero mark-price, zero aggTrades, zero spot, zero cross-venue, zero network I/O, zero credentials, zero `.env` reads, zero writes outside `data/research/phase4r/`.
- **Standalone-script discipline** worked. `scripts/phase4r_g1_backtest.py` has zero `prometheus.runtime / execution / persistence` imports, zero exchange-adapter imports, zero network-capable library imports.

The data / governance layer correctly enforced Phase 4q's stop conditions and produced a clean Verdict C without governance leakage. **The governance layer is not implicated in G1's failure; only the strategy spec and methodology layers were tested.**

## Reusable insights from G1

Ten reusable insights, ordered roughly from most actionable to most general:

1. **Regime-first is theoretically valid as a research concept**, but G1's first-spec implementation was too narrow at the intersection layer. Future regime-first hypotheses, if separately authorized, must validate not just classifier selectivity but classifier-AND-entry-rule arrival rate.
2. **Active-regime fraction alone is not enough**; active-regime entry-rule arrival rate matters. CFP-9's < 5% active-fraction threshold is necessary but not sufficient. A practical design discipline (not an authorization) would be to also predeclare a *minimum active-AND-setup* arrival rate threshold.
3. **Always-active baselines are valuable structural negative controls.** They confirm whether the underlying entry-and-exit machinery fires at a reasonable rate and what it earns without the regime gate. G1's 124-trade always-active baseline at mean_R = −0.34 was the binding diagnostic that distinguished "regime gate too narrow" from "regime gate filters out only profitable subset."
4. **Inactive-population pseudo-trades are valuable** but methodologically inert when active population is empty. Their value is in confirming that the breakout-and-stop machinery is loss-making outside `regime_active` (here: 124 trades at mean_R = −0.34); the regime hypothesis would be falsified more sharply if inactive were *profitable*, but neither outcome would rescue G1.
5. **HIGH-cost realism still matters even when the primary failure is no-trade.** The always-active baseline negative mean_R under §11.6 = 8 bps is not a separate verdict on G1, but it does reaffirm R2's cost-fragility lesson and Phase 3l's "B — conservative but defensible" stance.
6. **Zero-trade outcomes can make PBO / DSR / CSCV methodologically inert.** This is not a defect of those statistics; it is a defect of the strategy under that data. PBO 0.000 / 0.000 / 0.500 and DSR all-zero in this run carry no signal; CFP-6 correctly does not trigger because the methodology is neutralized, not violated.
7. **CFP-9 (regime active fraction < 5%) is important and worked correctly.** It detected sample-size collapse before any over-interpretation of mechanism evidence.
8. **CFP-1 (insufficient trade count) and CFP-9 (active-fraction collapse) are independent drivers** in this run — both triggered, both binding, neither subordinate. CFP-3 (PF=0 mechanical) and CFP-4 (degenerate ETH PASS) are subordinate / mechanical artifacts of the zero-trade root cause.
9. **M1 / M2 negative tests are valuable, but can be degenerate** if active population is empty. The Phase 4q implementation correctly reported "FAIL" for M1 / M2 in this case rather than spuriously passing.
10. **A good hypothesis can still fail at operational geometry.** G1's hypothesis-spec (Phase 4o), strategy-spec (Phase 4p), and methodology (Phase 4q) were internally coherent and predeclared before any data was touched. The failure is real research evidence and is preserved as such.

## Forbidden G1 rescue observations

Phase 4s explicitly forbids (binding for any future phase, including any operator-authorized fresh-hypothesis discovery memo, until and unless a separate explicit operator authorization removes the prohibition):

- **G1 with relaxed classifier thresholds**: forbidden.
- **G1 with E_min lowered** (below 0.30): forbidden.
- **G1 with wider ATR band** (outside the locked {[20, 80], [30, 70]} set): forbidden.
- **G1 with lower V_liq_min** (below 0.80): forbidden.
- **G1 with wider funding band** (outside the locked {[15, 85], [25, 75]} set): forbidden.
- **G1 with K_confirm reduced** (below 2): forbidden.
- **G1 with regime gate removed** (i.e., always-active variant promoted): forbidden.
- **G1 with 30m breakout loosened** (B_atr < 0.10 or N_breakout < 12): forbidden.
- **G1 with stop-distance bounds widened** (outside [0.50, 2.20] × ATR(20)): forbidden.
- **G1 with T_stop / N_R changed** (T_stop ∈ {12, 16} and N_R ∈ {2.0, 2.5} remain reserved as future G1-extension possibilities only, requiring a *separately authorized* governance amendment per Phase 4p §"Threshold grid" — Phase 4s does NOT authorize this).
- **G1-prime / G1-narrow / G1-extension / G1 hybrid**: forbidden.
- **Any Phase 4p G1 strategy-spec amendment based on Phase 4r forensic numbers**: forbidden. Specifically, the 2.03% active fraction, the 124 always-active baseline trades, and the −0.34 mean_R must NOT be used as parameter-selection inputs for any future phase.
- **Any Phase 4q methodology amendment based on Phase 4r forensic numbers**: forbidden.
- **Immediate G1 rerun** with the same or modified parameters: forbidden.
- **Immediate always-active rescue** (i.e., promoting the always-active baseline as a candidate): forbidden — the always-active baseline produced mean_R = −0.34 under HIGH cost; it is not a viable strategy candidate.
- **Immediate data acquisition to rescue G1** (e.g., acquiring mark-price 30m / 4h / aggTrades to "tighten" the regime classifier): forbidden.
- **Using Phase 4r active-fraction numbers as tuning targets** for any future regime-first hypothesis: forbidden. A future regime hypothesis, if separately authorized, must predeclare its active-fraction floor *before* touching data, not back into Phase 4r's observed value.

These prohibitions mirror Phase 4m's V2-rescue prohibitions and apply with equivalent force.

## Comparison with V2 failure

```text
Layer / question                       V2 (Phase 4l)                          G1 (Phase 4r)
-------------------------------------- -------------------------------------- --------------------------------------
Hypothesis predeclared before data?    Phase 4f / 4g / 4h / 4i / 4j / 4k —    Phase 4o / 4p / 4q / 4r — yes, four
                                        yes, six predeclaration phases.        predeclaration phases.
Strategy spec internally coherent?     yes                                    yes
Methodology predeclared verbatim?      yes                                    yes
Execution exactly under methodology?   yes                                    yes
Stop / target / sizing co-designed?    NO — V1-inherited stop-distance        yes (G1 stop-distance bounds derived
                                        filter (0.60-1.80 x ATR) was           from active-regime structure: [0.50,
                                        incompatible with V2's 20/40-bar       2.20] x ATR; setup window N_breakout
                                        Donchian setup, which produces ~3-5    = 12 produces stop distances in band).
                                        x ATR stops; the filter rejected
                                        every raw V2 candidate.
Did entry rule generate any trades?    NO — every variant 0 trades.           Always-active baseline: 124 trades
                                                                                BTC OOS HIGH (mean_R = -0.34).
Were active-regime trades produced?    n/a (no regime gate in V2)             NO for the train-best variant on OOS
                                                                                HIGH; the regime gate filtered out
                                                                                essentially all entries.
Failure mechanism                      design-stage incompatibility            regime-gate-meets-setup intersection
                                        (setup vs stop filter)                 sparseness
Verdict                                C — HARD REJECT (CFP-1 critical)       C — HARD REJECT (CFP-1 critical AND
                                                                                CFP-9 independent)
Always-active baseline                 not run (no regime gate to remove)     124 trades; mean_R = -0.34; loss-making
                                                                                under HIGH cost.
Inactive-population baseline           not run (no regime gate)               124 trades; mean_R = -0.34.
HIGH-cost survival                     not evaluable (zero trades)            not evaluable for G1 (zero trades);
                                                                                the always-active baseline confirms
                                                                                §11.6 = 8 bps would bite.
Lesson                                 setup geometry / stop / target /        regime gate / entry-rule arrival /
                                        sizing must be co-designed.            sample-size viability must be
                                                                                co-designed.
```

Both are *structural first-spec failures* before meaningful expectancy evaluation. Both honor §11.6, §1.7.3, and all governance preserved verbatim. Neither authorizes rescue.

## Comparison with R2 / F1 / D1-A failures

```text
Strategy   Trade count           Did mechanism evidence exist?    Verdict / lesson
---------- --------------------- -------------------------------- -----------------------------------------------
R2         sufficient            yes — M1 ✓, M3 ✓, M2 ✗            FAILED — §11.6 cost-fragility blocked
                                  (partial mechanism)               framework promotion despite partial mechanism
                                                                    evidence. Lesson: cost realism is a hard gate.
F1         sufficient            partial — M1 BTC PARTIAL,         HARD REJECT — Phase 3c §7.3 catastrophic-floor
                                  M3 PASS-isolated but               predicate triggered (5 separate violations).
                                  overwhelmed by 53-54%             Lesson: profitable subsets do not rescue a
                                  STOP exits in wider population.   losing framework expectancy.
D1-A       sufficient            yes — M1 BTC h=32 PASS;           MECHANISM PASS / FRAMEWORK FAIL — other.
                                  M3 PASS-isolated but              Lesson: context (funding) carries information
                                  overwhelmed by 67-68% STOP        at mechanism layer without delivering at
                                  exits at -1.30/-1.24R per         framework / promotion layer.
                                  loser; M2 FAIL on both symbols
                                  (funding benefit far below
                                  threshold).
V2         zero                  not evaluable                     HARD REJECT — design-stage incompatibility.
                                                                    Lesson: setup / stop / target / sizing
                                                                    co-design.
G1         zero (regime gate)    not evaluable for active          HARD REJECT — regime-gate-meets-setup
                                  population; always-active          intersection sparseness. Lesson: regime gate /
                                  baseline negative under HIGH       entry-rule arrival / sample-size viability
                                  cost; inactive-population          co-design.
                                  baseline negative.
```

R2 / F1 / D1-A failed *with mechanism evidence*. V2 / G1 failed *before mechanism evidence was generable*. These are categorically different failure layers, and Phase 4s preserves the distinction in the project record so future hypotheses can target either.

## Implications for future research

Phase 4s does NOT select a new strategy. The implications below are observations only and do not authorize any successor phase or any new candidate.

- Future hypotheses, if separately authorized, must include an **opportunity-rate viability check** before full backtest execution. This means predeclaring not just an active-fraction floor (CFP-9) but also a *joint active-AND-setup arrival rate* floor.
- Future regime hypotheses must predeclare both active-fraction and active-signal-rate floors *before* data is touched, derived from first-principles or external evidence — never from Phase 4r forensic numbers.
- Future breakout hypotheses must compare always-active, inactive, and active regimes as a structural negative-test set (G1's M1 / M2 framework was correctly designed for this).
- Future research must avoid creating ever-narrower AND-gate systems whose joint with an entry rule produces zero candidates. A common failure pattern is "more conditions = more selectivity = better quality"; G1 demonstrates this is not safe under the joint-with-entry-rule constraint.
- Any future strategy family requires a fresh-hypothesis discovery memo under the Phase 4m 18-requirement validity gate before any strategy-spec memo, methodology memo, or backtest is authorized.

## Fresh-hypothesis validity gate reaffirmation

The Phase 4m 18-requirement fresh-hypothesis validity gate is reaffirmed verbatim and is binding for any future ex-ante hypothesis. The 18 requirements are restated here for the project record (preserved exactly as Phase 4m wrote them):

```text
1.  Must be named as a new hypothesis (not a rescue label).
2.  Must be specified before any data is touched.
3.  Must explain why it is new in theory.
4.  Must define entry / stop / target / sizing / cost / timeframe / exit
    together (the V2 / G1 co-design lesson).
5.  Must predeclare data requirements.
6.  Must predeclare mechanism checks.
7.  Must predeclare pass / fail gates including catastrophic-floor predicates.
8.  Must predeclare forbidden comparisons and forbidden rescue interpretations.
9.  Must NOT choose thresholds from prior failed outcomes.
10. Must NOT use Phase 4l V2 root-cause analysis as direct optimization
    target.  (Phase 4s extends this to: must NOT use Phase 4r G1 active-
    fraction or 124-trade baseline numbers as direct optimization target.)
11. Must preserve §11.6 cost sensitivity.
12. Must preserve project locks and governance.
13. Must commit to predeclared chronological train / validation / OOS holdout
    windows before backtest.
14. Must commit to deflated Sharpe / PBO / CSCV correction if grid search.
15. Must distinguish mechanism evidence from framework promotion.
16. Must preserve BTCUSDT-primary / ETHUSDT-comparison protocol.
17. Must NOT propose live-readiness / paper / shadow / Phase 4 canonical as
    part of first phase.
18. Must satisfy separate operator authorization.
```

Phase 4s adds a single observation (NOT a new requirement, not an amendment): **after G1, requirement 4 should be read to include the regime-gate / entry-rule / sample-size-viability co-design lesson** alongside the V2 setup-geometry / stop-filter co-design lesson. Both are subordinate readings of requirement 4; neither is a new gate.

## Candidate future directions, if any

Phase 4s does NOT select a candidate. The following are observations of what *could* be considered if the operator separately authorizes a fresh-hypothesis discovery memo:

- **Structural-R trend continuation** (Phase 4n Candidate A) — recall Phase 4n's rescue-risk note: "trap = V2 but with a wider stop filter". After G1's failure, this candidate's risk profile is *unchanged*; G1 does not change its evaluation.
- **Funding-context trend filter** (Phase 4n Candidate C) — recall Phase 4n's rescue-risk note: "trap = D1-A but with extra filters / D1-A-prime". G1's funding-context-as-regime-condition use does not refute funding as research input, but does not authorize a funding-led candidate either.
- **Structural pullback continuation** (Phase 4n Candidate D) — recall Phase 4n's rescue-risk note: "trap = R2 but with lower assumed costs". G1 does not change this evaluation.
- **A regime-aware *but-not-regime-gated* hypothesis** — a *theoretical* possibility (regime as one of several inputs to a richer entry rule, rather than as a top-level state machine that gates entry). Phase 4s does NOT propose, name, or authorize this; it is recorded only as an open question for any future discovery memo.

Phase 4s recommends *not* selecting any of these now; see "Recommended next operator choice" below.

## Explicitly rejected next moves

The following are explicitly NOT recommended:

- **G1 rescue** (any variant, any threshold change, any classifier relaxation) — rejected.
- **G1 implementation** in `src/prometheus/` — rejected; Phase 4 canonical preconditions are not met.
- **Immediate backtest** of any kind — rejected (data-snooping risk per Bailey / Borwein / López de Prado / Zhu 2014).
- **Data acquisition** of any kind (mark-price, aggTrades, spot, cross-venue, additional intervals) — rejected; G1's failure is not a data-availability failure.
- **Always-active baseline promoted as a candidate** — rejected; the always-active baseline produced mean_R = −0.34 under §11.6 = 8 bps and is not a viable candidate.
- **5m strategy / 5m regime indicator** — rejected (Phase 3t §14.2 closure preserved).
- **Paper / shadow / live operation** — rejected (Phase 4 canonical preconditions not met; no validated strategy candidate exists).
- **Phase 4 canonical** — rejected.
- **Production keys / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials** — rejected.
- **Exchange-write capability** — rejected.

## Recommended next operator choice

**Primary recommendation: Option A — remain paused.**

Rationale: Phase 4r is the project's fifth strategy-rejection event (R2 / F1 / D1-A / V2 / G1). Each rejection has produced a distinct lesson preserved in the project record. The Phase 4m fresh-hypothesis validity gate is binding. There is no internally-derived new hypothesis ready for predeclaration. Authorizing another fresh-hypothesis discovery memo immediately after G1 risks the same pattern as Phase 4n → Phase 4o → Phase 4p → Phase 4q → Phase 4r — predeclaration discipline followed by a structural first-spec failure — without time to consolidate the regime-gate-meets-setup intersection lesson into the project's design-discipline practice. The conservative posture is to *pause* and let the rejection topology settle before considering any new candidate.

**Conditional secondary: Option B — authorize a docs-only fresh-hypothesis discovery memo, only if the operator explicitly chooses to continue research now.**

Acceptable shape of Option B if chosen: a Phase 4t docs-only fresh-hypothesis discovery memo, analogous to Phase 4n, evaluating a *new* candidate space against the Phase 4m 18-requirement validity gate and the Phase 4s rejection topology. Phase 4t (if ever authorized) must NOT propose any G1 / V2 / R2 / F1 / D1-A rescue, must NOT use Phase 4r forensic numbers as input, must predeclare any new candidate's opportunity-rate floor before touching data, and must satisfy separate operator authorization. **Phase 4s does not authorize Phase 4t.**

NOT recommended (any option):

- G1 rescue — REJECTED.
- Immediate G1 implementation — REJECTED.
- Immediate backtest — REJECTED.
- Data acquisition — REJECTED.
- Paper / shadow / live / exchange-write — FORBIDDEN.
- Phase 4 canonical — FORBIDDEN.
- Production-key creation / authenticated APIs / private endpoints / user stream / WebSocket — FORBIDDEN.
- MCP / Graphify / `.mcp.json` / credentials — FORBIDDEN.

## What this does not authorize

Phase 4s does NOT authorize:

- any new strategy candidate (V3 / G2 / H2 / any name);
- any G1 rescue (G1-prime / G1-narrow / G1-extension / G1 hybrid / classifier amendment / threshold amendment / breakout-rule amendment / stop-distance-bound amendment / N_R / T_stop amendment);
- any V2 / F1 / D1-A / R2 rescue;
- amendment of Phase 4p G1 strategy-spec or Phase 4q methodology;
- any backtest, diagnostic, or acquisition rerun;
- modification of `src/prometheus/`, tests, or existing scripts;
- modification of `data/raw/`, `data/normalized/`, or `data/manifests/`;
- creation of new manifests or v003;
- start of Phase 4t or any successor phase;
- paper / shadow / live / exchange-write / production keys / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- start of Phase 4 canonical;
- amendment of any project lock (§11.6 / §1.7.3 / mark-price stops / v002 verdict provenance);
- amendment of any governance rule (Phase 3r / 3v / 3w / 4j §11 / 4k);
- amendment of any retained verdict (R3 / R2 / R1a / R1b-narrow / F1 / D1-A / V2 / G1 / H0).

## Forbidden-work confirmation

Phase 4s does NOT do any of the following:

- run a backtest (any phase);
- write any code;
- create any script (no `scripts/...py` added);
- modify any source under `src/prometheus/`;
- modify any test;
- modify any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`);
- run `scripts/phase4r_g1_backtest.py`;
- run any acquisition / diagnostics / backtest script;
- acquire data;
- download data;
- patch / forward-fill / interpolate / regenerate / replace data;
- modify any manifest;
- create any new manifest;
- create v003;
- modify Phase 4p / Phase 4q / Phase 4j §11 / Phase 4k / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r §8 governance;
- revise any retained verdict;
- change any project lock;
- create any new strategy candidate;
- create G1-prime / G1-narrow / G1-extension / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- propose a 5m strategy / hybrid / variant;
- start Phase 4t / 4 canonical / paper-shadow / live-readiness / deployment / production-key creation / exchange-write capability / authenticated REST / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- consult any private endpoint / user stream / WebSocket / authenticated REST in code;
- store, request, or display any secret.

## Remaining boundary

```text
R3                  : V1 breakout baseline-of-record (preserved)
H0                  : framework anchor (preserved)
R1a / R1b-narrow    : retained research evidence; non-leading (preserved)
R2                  : FAILED — §11.6 cost-sensitivity blocks (preserved)
F1                  : HARD REJECT (preserved)
D1-A                : MECHANISM PASS / FRAMEWORK FAIL — other (preserved)
V2                  : HARD REJECT (Phase 4l terminal for first-spec; preserved)
G1                  : HARD REJECT (Phase 4r — Verdict C; CFP-1 critical
                       binding driver; CFP-9 independent driver;
                       terminal for G1 first-spec)
5m diagnostic thread : OPERATIONALLY CLOSED (Phase 3t)
§11.6               : 8 bps HIGH per side (preserved verbatim)
§1.7.3              : 0.25% risk / 2× leverage / 1 position / mark-price stops
                      (preserved)
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m
                              (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance
                              (preserved)
Phase 4a runtime            : public API and behavior (preserved)
Phase 4e                    : reconciliation-model design memo (preserved)
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q / 4r
                            : all preserved verbatim
Phase 4s                    : Post-G1 strategy research consolidation memo
                              (this phase; new; docs-only)
Recommended state           : paused
```

## Next authorization status

```text
Phase 4t                       : NOT authorized
Phase 4 (canonical)            : NOT authorized
Paper / shadow                 : NOT authorized
Live-readiness                 : NOT authorized
Deployment                     : NOT authorized
Production-key creation        : NOT authorized
Authenticated REST             : NOT authorized
Private endpoints              : NOT authorized
User stream / WebSocket        : NOT authorized
Exchange-write capability      : NOT authorized
MCP / Graphify                 : NOT authorized
.mcp.json / credentials        : NOT authorized
G1 implementation              : NOT authorized
G1-prime / G1-extension axes   : NOT authorized; not proposed
G1-narrow / G1 hybrid          : NOT authorized; not proposed
V2-prime / V2-variant          : NOT authorized; not proposed
Retained-evidence rescue       : NOT authorized; not proposed
5m strategy / hybrid           : NOT authorized; not proposed
ML feasibility                 : NOT authorized; not proposed
New family research            : NOT authorized at this boundary; would
                                  require a separately authorized
                                  fresh-hypothesis discovery memo (Phase 4t)
                                  under the Phase 4m 18-requirement validity
                                  gate.
```

The next step is operator-driven: the operator decides whether to authorize Phase 4t (fresh-hypothesis discovery memo, docs-only) or remain paused. Until then, the project remains at the post-Phase-4s consolidation boundary.

---

**Phase 4s is docs-only. No source code, tests, scripts, data, manifests, or successor phases were created or modified. Recommended state remains paused. No next phase authorized.**
