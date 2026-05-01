# Current Project State

## Purpose

This document defines the current high-level state of the Prometheus trading-system project.

Its purpose is to:

- provide a clear project checkpoint before Claude Code implementation begins,
- summarize what has already been designed,
- identify the current implementation-readiness status,
- define the boundary between documentation/setup/handoff and coding,
- preserve locked decisions across chats and repository updates,
- and act as the high-level project memory checkpoint.

This document should be treated as the single high-level source of truth for project status.

If this document conflicts with a detailed specialist document, the specialist document wins for its domain.

If older chat memory conflicts with repository Markdown files, the repository Markdown files win.

---

## Repository Context

Repository:

```text
https://github.com/jpedrocY/Prometheus
```

The repository Markdown files are the primary source of truth.

ChatGPT project-uploaded files are only a limited continuity cache because of the project-file limit.

Claude Code or any other implementation agent must inspect the repository directly and use uploaded files as a compact high-priority cache, not as the complete project source.

---

## Project Objective

Prometheus is a long-term project to design and build a:

```text
production-oriented, safety-first, operator-supervised trading system
for Binance USDⓈ-M futures
```

Initial live market:

```text
BTCUSDT perpetual
```

The system is:

- initially rules-based,
- not self-learning in v1,
- designed for robustness rather than novelty,
- built for staged and supervised deployment,
- designed to support future AI-assisted research or automation,
- but not dependent on a self-learning live AI component for v1.

Prometheus v1 is not intended to be a lights-out autonomous AI trading agent.

---

## Current Phase

Phase 0 (repo audit), Phase 1 (local development foundation), the Phase 2 historical-data foundation, and **three complete strategy-research arcs** are all complete:

1. The **V1 breakout-continuation arc** (Phases 2e through 2w) producing one locked baseline (H0), one cleanly-promoted structural redesign (R3 — baseline-of-record), and three post-R3 structural redesigns (R1a, R1b-narrow, R2 — retained research evidence).
2. The **F1 mean-reversion-after-overextension arc** (Phases 3a through 3d-B2) producing one new strategy family (F1) which **HARD REJECTED** at first execution per Phase 3c §7.3 catastrophic-floor predicate. Phase 3e is the docs-only post-F1 research consolidation memo with remain-paused recommendation.
3. The **D1-A funding-aware directional / carry-aware arc** (Phases 3f through 3j) producing one new strategy family (D1-A) which **FRAMEWORK FAILED** at first execution per Phase 3h §11.2 (verdict: MECHANISM PASS / FRAMEWORK FAIL — other; catastrophic-floor predicate NOT triggered; cond_i BTC MED expR > 0 FAILED; cond_iv BTC HIGH cost-resilience FAILED).

Phase 3k is the docs-only post-D1-A research consolidation memo with operator decision menu; primary recommendation is **remain paused** with external-cost-evidence review or regime-first framework memo as acceptable secondary / tertiary alternatives.

Phase 3l is the docs-only external execution-cost evidence review (operator selected the Phase 3k secondary acceptable alternative). Primary assessment: **B — current cost model appears conservative but defensible.** §11.6 policy recommendation: **§11.6 remains unchanged pending stronger evidence.** No prior verdict revised; no backtests run; no threshold / strategy-parameter / project-lock changes. R2 remains FAILED — §11.6 cost-sensitivity blocks; F1 remains HARD REJECT; D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other; R3 remains V1 breakout baseline-of-record; H0 remains framework anchor. No formal cost-model revision, regime-first, 5m timeframe feasibility, ML feasibility, new strategy-family discovery, D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, paper/shadow, Phase 4, live-readiness, deployment, MCP, Graphify, `.mcp.json`, credentials, exchange-write, or `data/` work started by Phase 3l. Recommended state remains **paused**.

Phase 3m is the docs-only regime-first research framework memo (operator selected the Phase 3k tertiary acceptable alternative). Phase 3m recommends **remain paused** as primary. The formal regime-first spec / planning memo (docs-only) is documented as a possible future docs-only option but is **not started by Phase 3m** and **not recommended now**. No 5m timeframe feasibility, ML feasibility, new strategy-family discovery, formal cost-model revision, D1-A-prime, D1-B, V1/D1 hybrid, or F1/D1 hybrid work started. No prior verdict revised; no backtests run; no threshold / strategy-parameter / project-lock changes. R3 remains V1 breakout baseline-of-record; H0 remains framework anchor; R2 remains FAILED — §11.6 cost-sensitivity blocks; F1 remains HARD REJECT; D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other. Recommended state remains **paused**.

Phase 3n is the docs-only 5m timeframe feasibility / execution-timing memo. Phase 3n recommends **remain paused** as primary. 5m was framed as a possible *future* execution / timing diagnostics layer only, **not** as a strategy signal layer. No 5m data was downloaded. No v003 dataset was created. No 5m data-requirements / v003 planning memo was started. No 5m diagnostics-spec memo was started. No 5m strategy, implementation, backtest, data acquisition, or analysis was authorized. No formal regime-first spec / planning, ML feasibility, formal cost-model revision, new strategy-family discovery, D1-A-prime, D1-B, V1/D1 hybrid, or F1/D1 hybrid work started. No prior verdict revised; no backtests run; no threshold / strategy-parameter / project-lock changes. R3 remains V1 breakout baseline-of-record; H0 remains framework anchor; R2 remains FAILED — §11.6 cost-sensitivity blocks; F1 remains HARD REJECT; D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other. Recommended state remains **paused**.

Phase 3o is the docs-only 5m diagnostics-spec memo. Phase 3o **predeclared the 5m diagnostic question set Q1–Q7** (with per-question definitions of informative versus non-informative, explicitly forbidden rescue-shaped question forms, diagnostic-term definitions, data-boundary rules, timestamp / leakage guardrails, allowed-vs-forbidden analysis boundary, per-strategy diagnostic mapping, required outputs, and stop conditions) **before any 5m data exists in the repository**. Phase 3o recommends **remain paused** as primary. No 5m data was downloaded. No v003 dataset was created. No 5m diagnostics were executed. No 5m data-requirements / v003 planning memo was started. No 5m diagnostics-execution plan was started. No 5m strategy, implementation, backtest, data acquisition, or analysis was authorized. No formal regime-first spec / planning, ML feasibility, formal cost-model revision, new strategy-family discovery, D1-A-prime, D1-B, V1/D1 hybrid, or F1/D1 hybrid work started. No prior verdict revised; no backtests run; no threshold / strategy-parameter / project-lock changes. R3 remains V1 breakout baseline-of-record; H0 remains framework anchor; R2 remains FAILED — §11.6 cost-sensitivity blocks; F1 remains HARD REJECT; D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other. Recommended state remains **paused**.

Phase 3p is the docs-only 5m diagnostics data-requirements and execution-plan memo. Phase 3p converts the Phase 3o predeclared question set Q1–Q7 into a concrete *future* diagnostics plan: defines exact 5m data requirements (BTCUSDT + ETHUSDT 5m trade-price klines, 5m mark-price klines; strict v002 date-range superset coverage; UTC ms timestamps; no gaps; canonical schema; public Binance endpoints, no credentials); specifies the dataset-versioning approach (recommends supplemental v001-of-5m alongside v002 over a v003 family bump); enumerates manifest + integrity-check evidence required; specifies the per-question diagnostic outputs (Q1–Q7 tables, distributions, classifications); and **predeclares per-question outcome-interpretation rules** (informative / non-informative / ambiguous thresholds; Q4 informative requires monotone decay shape replicable across BTC + ETH with standard-error bands tighter than displacement magnitude; Q5 informative requires |mean signed slippage| > 8 bps in at least one cell with replicability; Q3 critical reminder: even informative outcome cannot license retained-evidence candidate revision; Q7 meta requires ≥3 of Q1–Q6 informative; non-informative Q7 strengthens remain-paused) **before any 5m data exists in the repository**. Phase 3p recommends **remain paused** as primary. No 5m data downloaded. No v003 / supplemental 5m dataset created. No 5m diagnostics executed. No formal regime-first spec / planning, ML feasibility, formal cost-model revision, new strategy-family discovery, D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, paper/shadow, Phase 4, live-readiness, deployment, MCP, Graphify, `.mcp.json`, credentials, exchange-write, or `data/` work started. No prior verdict revised; no backtests run; no threshold / strategy-parameter / project-lock changes. R3 remains V1 breakout baseline-of-record; H0 remains framework anchor; R2 remains FAILED — §11.6 cost-sensitivity blocks; F1 remains HARD REJECT; D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other. Recommended state remains **paused**.

Phase 3q is the docs-and-data 5m supplemental dataset acquisition + integrity-validation phase (Phase 3p Option B: supplemental v001-of-5m alongside v002, v002 untouched). Phase 3q acquired four supplemental v001-of-5m dataset families (`binance_usdm_btcusdt_5m__v001`, `binance_usdm_ethusdt_5m__v001`, `binance_usdm_btcusdt_markprice_5m__v001`, `binance_usdm_ethusdt_markprice_5m__v001`) covering 2022-01..2026-03 (51 monthly archives × 4 families = 204 archives) from public unauthenticated `data.binance.vision` bulk endpoints, with strict superset coverage of the v002-locked retained-evidence trade range. **Verdict — partial pass:** trade-price 5m datasets PASS Phase 3p §4.7 strict integrity gate (446 688 bars each; 0 gaps); mark-price 5m datasets FAIL strict gate due to 4 known upstream Binance maintenance-window gaps each (BTC: 2022-07-30/31, 2022-10-02, 2023-02-24, 2023-11-10; ETH: 2022-07-12, 2022-10-02, 2023-02-24, 2023-11-10), with the same gap pattern verified to be present in locked v002 mark-price 15m datasets. No forward-fill, interpolation, imputation, or §4.7 relaxation applied. Mark-price manifests record `research_eligible: false` and `invalid_windows` verbatim. Phase 3q committed `scripts/phase3q_5m_acquisition.py` (standalone orchestrator, public endpoints only, no credentials, no Interval-enum extension, no `prometheus.research.data.*` modification) and the Phase 3q report + closeout. Local data + manifests are git-ignored per the same convention applied to v002 (≈ 147 MB local footprint, reproducible from public sources via the orchestrator). No diagnostics, Q1–Q7 answers, backtests, or strategy / threshold / project-lock / verdict modifications occurred.

Phase 3r is the docs-only mark-price gap governance memo (Phase 3p §10 / Phase 3q decision menu Option B). Phase 3r recommends **Option B (known invalid-window exclusion for Q6 only)** as the formally adopted governance posture: Phase 3p §4.7 strict integrity gate stays unchanged; mark-price 5m datasets remain `research_eligible: false`; no data is patched, forward-filled, interpolated, imputed, or replaced; Phase 3q manifests are not modified. Phase 3r §8 specifies a full normative **Q6 invalid-window exclusion rule** (known invalid windows are exclusion zones, not patch zones; per-trade exclusion test based on Q6 analysis-window intersection; excluded trades counted and reported by candidate / symbol / side / exit-type / gap-window; Q6 conclusions labeled "conditional on valid mark-price coverage"; no automatic prior-verdict revision; no strategy rescue, parameter change, or live-readiness implication; no silent §8 rule revision; per-trade exclusion algorithm must be predeclared in any future diagnostics-execution phase brief) that any future Q6-running phase must obey *if* Q6 is ever authorized. **Q6 disposition: bounded-conditional optionality.** Q6 stays on the menu but only as a §8-bounded option; Q6 is NOT permanently retired and NOT currently authorized. Q1, Q2 (trade-price base), Q3, Q4, Q5, Q7 unaffected by §8. Phase 3r preserves all prior boundaries: Phase 3p §4.7 unchanged; v002 datasets and manifests unchanged; Phase 3q manifests unchanged; mark-price 5m datasets remain `research_eligible: false`; R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks all preserved verbatim. No diagnostics run; no Q1–Q7 answered; no backtests; no data acquisition / patching / regeneration / modification; no manifest modification; no Phase 3p text modification; no 5m strategy / hybrid / variant; no diagnostics-execution started; no paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials work. Recommended state remains **paused**.

Phase 3s is the diagnostics-and-reporting phase that executed the predeclared Phase 3o / Phase 3p Q1–Q7 diagnostic question set **exactly once** on the v002-locked retained-evidence trade populations (R3, R2, F1, D1-A; R-window MEDIUM-slip canonical runs; 10 031 trades total: 4 974 BTC + 5 057 ETH), using the Phase 3q v001-of-5m supplemental datasets, and applying the Phase 3r §8 Q6 invalid-window exclusion rule verbatim. **Q1, Q2, Q3 (+1R), Q6 (D1-A only), and Q7 meta classified informative under Phase 3p §8 outcome-interpretation rules; Q4 and Q5 classified non-informative; Q3 ambiguous for +2R.** Phase 3r §8 exclusion rule applied with **zero trades excluded empirically** (retained-evidence trade lifetimes ≤ 8 h are too short to straddle the four mark-price gap windows). Headline findings: Q1 — IAE > IFE in 7 of 8 candidate × symbol cells (universal entry-path adverse bias; F1 most pronounced ~0.5 R consumed in first 5 min); Q2 — V1-family wick-dominated stop pathology (R3/R2 wick-fraction 0.571–1.000) vs F1/D1-A sustained-dominated stop pathology (0.269–0.347), the cleanest cross-family mechanism finding; Q3 — +1R intrabar-touch fraction ≥ 25% in 6 of 8 cells (descriptive-only per Phase 3p §8.3 / Phase 3o §6.3); Q6 — D1-A mark-stop lag ~1.3–1.8 5m bars (mark triggers later than trade); Q4 — D1-A funding-decay curve has no monotone shape, SEM > displacement magnitude (non-informative); Q5 — no |signed| > 8 bps cell, consistent with Phase 3l "B — conservative but defensible". **All findings are descriptive only and cannot license verdict revision, parameter change, threshold revision, project-lock revision, strategy rescue, 5m strategy / hybrid / variant proposal, paper/shadow planning, Phase 4, live-readiness, deployment, or any successor authorization.** Phase 3o §6 forbidden question forms, Phase 3o §10 analysis boundary, Phase 3p §8 critical reminders, and Phase 3r §8 binding constraints all preserved. **5m research thread is operationally complete.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks all preserved verbatim. No backtest run. No retained-evidence trade population regenerated. No v002 dataset / manifest modification. No Phase 3q v001-of-5m manifest modification. No data acquisition / download / patch / regeneration / modification. No forward-fill / interpolation / imputation / replacement. No 5m strategy / hybrid / variant. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials. No private endpoints / user stream / WebSocket / public endpoints consulted. No secrets. Recommended state remains **paused**.

Phase 3t is the docs-only post-5m-diagnostics consolidation and research-thread closure memo. Phase 3t records what the 5m research thread (Phases 3o → 3p → 3q → 3r → 3s) taught the project, what it explicitly did not teach, and why the correct project state remains paused. **The 5m research thread is operationally complete and closed.** Phase 3t consolidates the strategic answers: useful timing information exists inside 15m bars, descriptively only (Q1 universal entry-path adverse bias; Q2 V1-family-vs-F1/D1A stop pathology differentiation; Q3 +1R intrabar-touch frequency in adverse-exit trades; Q6 D1-A mark-stop lag); regime-first remains unanswered and risky (Phase 3m's "remain paused" recommendation stands; Phase 3s did not test regime-classification questions); 5m helped diagnostically but finer-than-5m data is not justified (sub-minute / tick would add noise without offsetting signal-to-noise ratio gain); no implementation-grade new hypothesis emerged (informative findings are not strategy candidates per §9.1; Phase 3o §6 forbidden question forms preserved). **Informative diagnostics do not revise verdicts, do not authorize strategy rescue, do not authorize parameter changes, do not authorize a 5m strategy, do not authorize Phase 4 / paper-shadow / live-readiness / deployment.** Phase 3t §12 records the validity gate for any future research: a genuinely new ex-ante hypothesis (not derived from observed Q1–Q7 patterns); full written specification before testing; no conversion of Q3 / Q6 findings into post-hoc rules; no rescue framing; no reuse of 5m findings as parameter-optimization hints; predeclared evidence thresholds; separate operator authorization. R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false` — all preserved verbatim. No diagnostics rerun; no Q1–Q7 rerun; no backtests; no data acquisition / patching / regeneration / modification; no manifest modification; no Phase 3p §4.7 amendment; no 5m strategy / hybrid / retained-evidence successor / new variant proposal; no paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials work. **Recommended state remains paused.**

Phase 3u is the docs-only implementation-readiness and Phase-4 boundary review, a forward-looking memo evaluating whether the project should later move toward implementation-readiness / Phase-4 boundary work or remain paused. **Phase 3u recommends remain paused as primary.** Phase 3u answers the originally-asked questions: implementation-readiness work CAN help future strategy discovery indirectly, but only under strict §10 prohibitions, only after pre-coding blockers are resolved, and only if the operator has consciously chosen to deprioritize research; **Phase 4 (canonical) remains unauthorized** because canonical Phase 4 framing assumes strategy evidence which the project does not have; **any future Phase 4a, if ever authorized, must be local-only / fake-exchange / dry-run / exchange-write-free**, with no production keys, no live-readiness implication, no paper-shadow commitment, no MCP / Graphify / `.mcp.json` / credentials; **fresh-hypothesis research remains paused** for now (Phase 3t §14.2 + Phase 3u §14); current documentation is sufficiently synchronized after Phase 3t for Phase 3u purposes; **pre-coding blockers must be resolved before any coding phase**, with **GAP-20260424-032 (mark-price vs trade-price stop) as the highest-priority blocker** (HIGH risk; the §1.7.3 mark-price-stops lock and the Phase 3s Q6 D1-A finding are now both on record and must be reconciled in any future runtime stop-handling specification). Phase 3u offers a conditional secondary alternative (docs-only ambiguity-resolution memo, especially resolving GAP-20260424-032) that produces unconditional documentation value but is not endorsed over remain-paused, and a conditional tertiary alternative (docs-only Phase 4a safe-slice scoping memo) acceptable only with explicit anti-live-readiness preconditions. Phase 3u does NOT recommend Phase 4 canonical, paper/shadow, live-readiness, deployment, production-key creation, exchange-write capability, fresh-hypothesis research, MCP / Graphify / `.mcp.json` / credentials, strategy rescue, 5m strategy / hybrid / retained-evidence successor / new variant. R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false` — all preserved verbatim. No code, tests, scripts, data, manifests modified; no diagnostics rerun; no backtests; no data acquisition / patching / regeneration / modification; no Phase 3p §4.7 amendment; no Phase 4 / Phase 4a authorization; no paper/shadow / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials work; no private endpoints / user stream / WebSocket / public endpoints consulted; no secrets stored or requested. **Recommended state remains paused.**

Phase 3v is the docs-only GAP-20260424-032 stop-trigger domain ambiguity resolution memo. **GAP-20260424-032 (Backtest uses trade-price stops; live uses MARK_PRICE stops) is RESOLVED at the governance level by Phase 3v.** The resolution preserves historical retained-evidence backtests under their original `trade_price_backtest` provenance with all verdicts unchanged (R3 baseline-of-record; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; H0 framework anchor; R1a / R1b-narrow retained research evidence only) and preserves the §1.7.3 mark-price-stop lock for any future runtime / paper / live operation. Phase 3v §8 specifies a binding eight-clause rule: future evidence and runtime artifacts must carry an explicit **stop-trigger-domain label** with valid values `trade_price_backtest` | `mark_price_runtime` | `mark_price_backtest_candidate`; **`mixed_or_unknown` is invalid and fails closed at any decision boundary** (block trade / block verdict / block persist / block evidence-promotion); future backtests intended to support paper/shadow/live readiness must explicitly use or validate `mark_price_backtest_candidate` modeling, or disclose that they are not live-readiness evidence; Phase 3s Q6 D1-A mark-stop-lag finding remains descriptive only and does NOT revise verdicts, change stop-policy, or authorize strategy rescue; future Phase 4a (if ever authorized) may implement labels and fail-closed validation locally subject to Phase 3u §10 prohibitions (no order placement; no exchange-write; no paper-shadow / live-readiness implication); GAP-20260424-032 is RESOLVED in `docs/00-meta/implementation-ambiguity-log.md` with the Phase 3v memo as resolution evidence. Three remaining OPEN ambiguity-log items (GAP-20260424-030 break-even rule conflict — MEDIUM risk; GAP-20260424-031 EMA slope wording — LOW-MEDIUM risk; GAP-20260424-033 stagnation window — LOW risk) preserved unchanged and remain pre-coding blockers per Phase 3u §8.5. R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`; `docs/07-risk/stop-loss-policy.md` substantive content; `docs/06-execution-exchange/binance-usdm-order-model.md` mark-price stop discipline — all preserved verbatim. No code, tests, scripts, data, manifests modified beyond the ambiguity-log GAP-20260424-032 RESOLVED update. No diagnostics rerun. No backtests. No data acquisition / patching / regeneration / modification. No verdict revision. No strategy-parameter / threshold / project-lock changes. No §11.6 change. No §1.7.3 change. No stop-loss-policy substantive change. No 5m strategy / hybrid / retained-evidence successor / new variant. No Phase 4 / Phase 4a authorization. No paper/shadow / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials. No private endpoints / user stream / WebSocket / public endpoints consulted. No secrets stored or requested. **Recommended state remains paused.**

Phase 3w is the docs-only remaining ambiguity-log resolution memo. **GAP-20260424-030 (break-even rule conflict), GAP-20260424-031 (EMA slope wording), and GAP-20260424-033 (stagnation window) are RESOLVED at the governance level by Phase 3w using the same Phase 3v §8 pattern (historical provenance preserved; future runtime / paper / live forced to label semantic choice explicitly; `mixed_or_unknown` fails closed; no retained verdict revised; no strategy parameter / threshold / lock changed; no Phase 4 / 4a authorization).** **All four Phase 3u §8.5 currently-OPEN pre-coding blockers are now RESOLVED at the governance level** (GAP-20260424-032 by Phase 3v; GAP-20260424-030 / 031 / 033 by Phase 3w). Phase 3w §6.1 / §7.1 / §8.1 record canonical historical provenance per-candidate: H0 / R1a / R1b-narrow / R2 used `break_even_rule = enabled_plus_1_5R_mfe`, `ema_slope_method = discrete_comparison`, `stagnation_window_role = active_rule_predeclared`; R3 (baseline-of-record) used `break_even_rule = disabled`, `ema_slope_method = discrete_comparison`, `stagnation_window_role = not_active`; F1 / D1-A used `break_even_rule = disabled`, `ema_slope_method = not_applicable`, `stagnation_window_role = not_active`. Phase 3w §6.3 / §7.3 / §8.3 specify future-runtime guardrail label schemes that any future runtime / paper / live phase or future research backtest (if ever authorized — Phase 3w does NOT authorize any) must declare as first-class config / persistence labels; `mixed_or_unknown` is invalid and fails closed at any decision boundary for all four schemes. Three governance label schemes added by Phase 3w: `break_even_rule` ∈ {`disabled`, `enabled_plus_1_5R_mfe`, `enabled_plus_2_0R_mfe`, `enabled_<other_predeclared>`}; `ema_slope_method` ∈ {`discrete_comparison`, `fitted_slope`, `other_predeclared`, `not_applicable`}; `stagnation_window_role` ∈ {`not_active`, `metric_only`, `active_rule_predeclared`}. Combined with the Phase 3v `stop_trigger_domain` scheme, the project record now has four binding governance label schemes for any future evidence or runtime artefact. After Phase 3w, `docs/00-meta/implementation-ambiguity-log.md` has zero OPEN entries that constitute pre-coding blockers per Phase 3u §8.5; pre-tiny-live items (`ACCEPTED_LIMITATION` / `DEFERRED`) remain as documented. Existing artefacts (Phase 2 / Phase 3 backtest manifests; Phase 3q v001-of-5m manifests; Phase 3s diagnostic outputs) are NOT retroactively modified by Phase 3w; the label requirement applies prospectively. R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks (including mark-price stops); v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`; `docs/03-strategy-research/v1-breakout-strategy-spec.md` substantive content (lines 156–172, 380, 415, 564); `docs/03-strategy-research/v1-breakout-backtest-plan.md`; `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`; `docs/07-risk/stop-loss-policy.md`; `docs/06-execution-exchange/binance-usdm-order-model.md`; Phase 3v §8 stop-trigger-domain governance — all preserved verbatim. No code, tests, scripts, data, manifests modified beyond the ambiguity-log GAP-20260424-030 / 031 / 033 RESOLVED updates. No diagnostics rerun. No Q1–Q7 rerun. No backtests. No H-D3 / H-C2 / H-D5 sensitivity analysis. No data acquisition / patching / regeneration / modification. No spec / backtest-plan / validation-checklist / stop-loss-policy / runtime-doc substantive edit. No verdict revision. No strategy-parameter / threshold / project-lock changes. No 5m strategy / hybrid / retained-evidence successor / new variant. No Phase 4 / Phase 4a authorization. No paper/shadow / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials. No private endpoints / user stream / WebSocket / public endpoints consulted. No secrets stored or requested. **Recommended state remains paused.**

Phase 3x is the docs-only Phase 4a safe-slice scoping memo (operator selected the Phase 3u §16.3 conditional tertiary alternative / Phase 3w §17.2 conditional secondary alternative now that all four Phase 3u §8.5 pre-coding governance blockers are RESOLVED at the governance level by Phase 3v + Phase 3w). **The Phase 4a safe-slice scope is now defined in the project record by Phase 3x.** Phase 3x defines what a possible future Phase 4a execution phase would be — a strictly local-only, fake-exchange, dry-run, exchange-write-free, strategy-agnostic implementation scope — and what it must categorically not be. **Phase 3x does NOT authorize Phase 4a execution.** Phase 3x is a scoping memo only; Phase 4a execution would require a separate, explicit operator decision. Phase 3x §6 prohibition list (binding on any future Phase 4a execution authorization brief): no live exchange-write capability; no production Binance keys; no authenticated APIs / private endpoints / user stream / WebSocket; no paper/shadow; no live-readiness implication; no deployment; no strategy commitment / rescue / new candidate; no verdict revision; no lock change; no MCP / Graphify / `.mcp.json` / credentials; no data acquisition / patching / regeneration / modification; no regime-first / ML / cost-model-revision work. Phase 3x §9 candidate Phase 4a scope (ten components, each evaluated as appropriate under §6 prohibition list): runtime mode / state model; runtime control state persistence (SQLite / local; SAFE_MODE startup; kill-switch persists across restart; never auto-clears); internal event contracts (typed local events; no exchange-write events); risk sizing skeleton (local calculation only; fail-closed on missing metadata; respect 0.25% risk and 2× leverage cap as locked constants); exposure gate skeleton (one-symbol-only live lock; one-position max; no pyramiding / no reversal; fake-position state only); stop-validation skeleton (must enforce Phase 3v `stop_trigger_domain` labels; `mark_price_runtime` required for any future runtime / live path; no order placement; no stop widening); break-even / EMA / stagnation governance label plumbing (Phase 3w `break_even_rule`, `ema_slope_method`, `stagnation_window_role` labels; `mixed_or_unknown` fails closed); fake-exchange adapter (local deterministic only; no Binance credentials; no private endpoints; no WebSocket; no real order placement); read-only operator state view (no control buttons that imply live execution; no production alerting); test harness (fail-closed behavior tests; restart safety tests; kill-switch persistence tests; label validation tests; fake-exchange lifecycle tests; no live integration tests). The four governance label schemes (Phase 3v §8.4 + Phase 3w §6.3 / §7.3 / §8.3) become enforceable in code at the Phase 4a layer if Phase 4a is ever authorized; `mixed_or_unknown` invalid and fails closed at any decision boundary in code, not only in policy text. Phase 3x §17 / §18 recommendation: Option A (remain paused) primary; Option B (authorize future Phase 4a execution as local-only safe-slice) conditional secondary now procedurally well-grounded; Option C (more docs-only preparation: Phase 4a execution-plan memo, label-enforcement design memo, or documentation-refresh memo) conditional tertiary; Option D (return to research / sensitivity analysis) NOT recommended; Option E (Phase 4 canonical / paper-shadow / live-readiness / exchange-write) FORBIDDEN / NOT RECOMMENDED. R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks (including mark-price stops); v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`; Phase 3v §8 stop-trigger-domain governance; Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance — all preserved verbatim. No code, tests, scripts, data, manifests modified by Phase 3x. No diagnostics rerun. No Q1–Q7 rerun. No backtests. No H-D3 / H-C2 / H-D5 sensitivity analysis. No mark-price-stop sensitivity analysis. No data acquisition / patching / regeneration / modification. No `data/manifests/*.manifest.json` modification. No spec / backtest-plan / validation-checklist / stop-loss-policy / runtime-doc / phase-gates / technical-debt-register / ai-coding-handoff / first-run-setup-checklist substantive edit. No `docs/00-meta/implementation-ambiguity-log.md` modification (all four pre-coding blockers remain RESOLVED per Phase 3v / 3w; pre-tiny-live items remain documented). No verdict revision. No strategy-parameter / threshold / project-lock changes. No 5m strategy / hybrid / retained-evidence successor / new variant. No Phase 4 / Phase 4a execution authorization. No paper/shadow / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials. No private endpoints / user stream / WebSocket / public endpoints consulted. No secrets stored or requested. **Recommended state remains paused.**

Phase 4a is the **Local Safe Runtime Foundation** implementation phase (operator selected the Phase 3x §18.2 Option B conditional secondary alternative; Phase 4a authorization brief recorded the operator commitment to consciously deprioritize further strategy research in order to build strategy-agnostic local runtime safety infrastructure for the duration of Phase 4a only). **Phase 4a is local-only / fake-exchange / dry-run / exchange-write-free / strategy-agnostic.** Phase 4a implemented the ten Phase 3x §9 safe-slice components: (1) runtime mode / state model (`prometheus.state` package: `RuntimeMode` `StrEnum` SAFE_MODE / RUNNING / BLOCKED / EMERGENCY / RECOVERY_REQUIRED; `RuntimeControlState` frozen pydantic record; pure-function transitions `enter_safe_mode`, `enter_running`, `enter_blocked`, `enter_emergency`, `enter_recovery_required`, `activate_kill_switch`, `clear_kill_switch`; startup defaults to SAFE_MODE; unknown state fails closed); (2) runtime control state persistence (`prometheus.persistence.runtime_store.RuntimeStore` with SQLite WAL / `foreign_keys=ON` / `synchronous=FULL` / `busy_timeout=5000`; single-row `runtime_control` table; append-only `runtime_mode_event` audit table; append-only `governance_label_audit` table; persisted RUNNING does NOT auto-resume RUNNING; kill-switch state persists across restart; never auto-clears); (3) internal event contracts (`prometheus.events`: `MessageEnvelope`, `MessageClass`, `RuntimeModeChangedEvent`, `KillSwitchEvent`, `FakeExchangeLifecycleEvent` with `is_fake = True` invariant, `GovernanceLabelEvent`); (4) governance label enforcement (`prometheus.core.governance` as single source of truth for `StopTriggerDomain`, `BreakEvenRule`, `EmaSlopeMethod`, `StagnationWindowRole` schemes; `is_fail_closed`, `require_valid`, four `parse_*` strict parsers; `mixed_or_unknown` fails closed at every governance-relevant decision boundary by importing from this single module); (5) risk sizing skeleton (`prometheus.risk.sizing.compute_sizing(SizingInputs) -> SizingResult` with locked v1 constants `LOCKED_LIVE_RISK_FRACTION = 0.0025`, `LOCKED_LIVE_LEVERAGE_CAP = 2.0`); (6) exposure gate skeleton (`prometheus.risk.exposure.evaluate_entry_candidate(...) -> ExposureDecision` enforcing BTCUSDT-only / one-position max / no-pyramiding / no-reversal / entry-in-flight blocks / unprotected-position blocks / manual-exposure blocks); (7) stop-validation skeleton (`prometheus.risk.stop_validation.validate_initial_stop / validate_stop_update` enforcing `stop_trigger_domain` governance, side-vs-entry, ATR filter, risk-reducing-only direction); (8) fake-exchange adapter (`prometheus.execution.fake_adapter.FakeExchangeAdapter` deterministic local in-memory state machine; injectable clock; methods `submit_entry_order`, `confirm_fake_fill`, `mark_entry_unknown_outcome`, `submit_protective_stop`, `confirm_fake_protective_stop`, `mark_stop_submission_failed`, `trigger_fake_stop`; emits `FakeExchangeLifecycleEvent` with `is_fake = True`; **no Binance code; no network I/O; no credentials**); (9) read-only operator state view (`prometheus.operator.state_view.format_state_view(...)` pure function + `prometheus.cli` minimal `inspect-runtime --db PATH` subcommand; **no controls; no exchange actions; no production alerting**); (10) test harness (`tests/unit/runtime/`: 10 test files, 117 tests). **Test evidence:** 117 Phase 4a tests passed; 785/785 project-total tests passed; ruff clean for Phase 4a code; mypy strict passed across 82 source files (no issues); full-repo ruff has 29 pre-existing issues in Phase 3q / 3s scripts which are unchanged by Phase 4a. **Phase 4 canonical remains unauthorized.** **Phase 4b / any successor phase remains unauthorized.** **Paper/shadow, live-readiness, deployment, production keys, authenticated APIs, private endpoints, user stream, WebSocket, MCP, Graphify, `.mcp.json`, credentials, and exchange-write all remain unauthorized.** **No strategy was implemented or validated by Phase 4a.** **No retained verdicts were revised.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks (including mark-price stops); v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`; Phase 3v §8 stop-trigger-domain governance; Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance — all preserved verbatim. **No project locks changed.** Existing artefacts (Phase 2 / Phase 3 backtest manifests; Phase 3q v001-of-5m manifests; Phase 3s diagnostic outputs; existing `prometheus.strategy` modules) NOT modified by Phase 4a. `.gitignore` modified narrowly to anchor `state/`/`runtime/`/`cache/` patterns to repository root only (so source-code packages and test directories named `state` or `runtime` are not accidentally ignored); no secret/credential ignore rule weakened. No diagnostics run; no Q1–Q7 rerun; no backtests; no data acquisition / patching / regeneration / modification; no manifest modification; no Phase 3p §4.7 amendment; no 5m strategy / hybrid / retained-evidence successor / new variant proposal; no paper/shadow / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials work. No private endpoints / user stream / WebSocket / public endpoints consulted. No secrets stored or requested. **Recommended state remains paused.** **No next phase authorized.**

Phase 4b is the **Repository Quality Gate Restoration** phase (operator selected the Phase 4a §25.2 Option B successor: a narrow targeted code-hygiene phase to make full-repo Ruff pass by fixing the known pre-existing Ruff issues in the Phase 3q / Phase 3s standalone scripts that Phase 4a's report flagged as residual quality debt). **Phase 4b is quality-gate restoration only.** Phase 4b restored the scripts Ruff quality gate by fixing **29 known pre-existing Ruff issues** in `scripts/phase3q_5m_acquisition.py` (16 issues) and `scripts/phase3s_5m_diagnostics.py` (13 issues) via behavior-preserving lint-only edits: removed unused `datetime.datetime`, `datetime.timezone`, `dataclasses` imports; renamed `attempt` → `_attempt` and `ot` → `_ot` (unused loop variables); added `strict=True` to three `zip()` calls; renamed ambiguous `l` → `lo` in OHLC sanity loops (and atomically updated downstream references); converted one if/else block to a ternary; split 18 long lines via adjacent f-string literals, multi-line dict/list reformat, and multi-line `print` / `write_text` calls. **Test evidence:** `ruff check scripts` passed cleanly (`All checks passed!`); pytest passed (785 tests in 13.53s; identical pass count to pre-Phase-4b — no regressions); mypy strict passed across 82 source files (0 issues). However, `ruff check .` (whole repo) still reports **2 residual pre-existing Ruff issues in Phase 4a state code** that were latent during Phase 4a's narrower verification: `src/prometheus/state/__init__.py:20:1` I001 (import block un-sorted: ruff wants `.control` before `.errors` alphabetically) and `src/prometheus/state/transitions.py:49:5` SIM103 (collapse `if incident_active: return True; return False` → `return bool(incident_active)`). **Both were verified as pre-existing relative to Phase 4b** by `git stash` test on the unmodified post-Phase-4a-merge tree (which reported 31 errors: 29 in scripts + the same 2 in `state/`). They are **out of Phase 4b scope** per the brief's strict constraint forbidding modification of Phase 4a runtime code unless caused by the script cleanup; they are **documented and not fixed by Phase 4b**, with a separately-authorized narrow follow-up phase (estimated < 5 minutes of behavior-preserving edits) recommended. Phase 4b does NOT invent success. **Phase 4 canonical remains unauthorized.** **Phase 4c / any successor phase remains unauthorized.** **Paper/shadow, live-readiness, deployment, production keys, authenticated APIs, private endpoints, user stream, WebSocket, MCP, Graphify, `.mcp.json`, credentials, and exchange-write all remain unauthorized.** **No strategy was implemented or validated by Phase 4b.** **No retained verdicts were revised.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks (including mark-price stops); v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`; Phase 3v §8 stop-trigger-domain governance; Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance; Phase 4a runtime code (state, persistence, events, governance, risk, fake_adapter, operator, cli) — all preserved verbatim. **No project locks changed.** Phase 4b modified only `scripts/phase3q_5m_acquisition.py` and `scripts/phase3s_5m_diagnostics.py` (lint-only). No code under `src/prometheus/`, no tests, no data, no manifests, no specs, no thresholds, no parameters, no project locks, no prior verdicts modified. `scripts/phase3q_5m_acquisition.py` not run. `scripts/phase3s_5m_diagnostics.py` not run. No diagnostics rerun. No backtests. No data acquisition / patching / regeneration / modification. No 5m strategy / hybrid / retained-evidence successor / new variant. No paper/shadow / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials work. No private endpoints / user stream / WebSocket / public endpoints consulted. No secrets stored or requested. **Recommended state remains paused.** **No next phase authorized.**

Phase 4c is the **State Package Ruff Residual Cleanup** phase (operator selected the Phase 4b §16.2 Option B successor: a tiny code-hygiene phase to fix exactly the two residual ruff issues that Phase 4b documented as latent in `src/prometheus/state/`). **Phase 4c is lint-only quality-gate restoration.** Phase 4c fixed exactly two residual ruff issues via behavior-preserving lint-only edits: (1) `src/prometheus/state/__init__.py:20:1` I001 — reordered four relative-import lines alphabetically (`.control` → `.errors` → `.mode` → `.transitions`); set of imported names identical, `__all__` unchanged, public API unchanged; (2) `src/prometheus/state/transitions.py:49:5` SIM103 — collapsed final `if incident_active: return True; return False` block in `_derive_entries_blocked` to `return bool(incident_active)`; function signature declares `incident_active: bool` so `bool(incident_active)` is an identity wrapper; truth table unchanged for every input. **Test evidence:** `ruff check src/prometheus/state` passed cleanly; `ruff check .` (whole repo) passed cleanly — **whole-repo Ruff quality gate fully restored** (zero ruff errors across the entire repository); pytest passed (785 tests in 12.59s; no regressions); mypy strict passed across 82 source files (0 issues). **Phase 4 canonical remains unauthorized.** **Phase 4d / any successor phase remains unauthorized.** **Paper/shadow, live-readiness, deployment, production keys, authenticated APIs, private endpoints, user stream, WebSocket, MCP, Graphify, `.mcp.json`, credentials, and exchange-write all remain unauthorized.** **No strategy was implemented or validated by Phase 4c.** **No retained verdicts were revised.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks (including mark-price stops); v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`; Phase 3v §8 stop-trigger-domain governance; Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance; Phase 4a public API and runtime behavior — all preserved verbatim. **No project locks changed.** Phase 4c modified only `src/prometheus/state/__init__.py` and `src/prometheus/state/transitions.py` (lint-only). No tests, scripts, data, manifests, specs, thresholds, parameters, project locks, or prior verdicts modified. No diagnostics rerun. No backtests. No data acquisition / patching / regeneration / modification. No 5m strategy / hybrid / retained-evidence successor / new variant. No paper/shadow / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials work. No private endpoints / user stream / WebSocket / public endpoints consulted. No secrets stored or requested. **Recommended state remains paused.** **No next phase authorized.**

Phase 4d is the **Post-4a/4b/4c Runtime Foundation Review and Next-Slice Decision** memo (docs-only). Phase 4d reviewed the merged Phase 4a local safe runtime foundation, the Phase 4b/4c quality-gate restoration, and the current post-Phase-4c boundary; ranked seven candidate next moves; and recommended a posture. **Phase 4d was docs-only.** No source code, tests, scripts, data, manifests, or strategy docs were modified by Phase 4d. **Whole-repo quality gates remain clean** (verified during Phase 4d): `ruff check .` passed (`All checks passed!`); pytest passed (`785 passed in 12.89s`; no regressions); mypy strict passed (`Success: no issues found in 82 source files`). **Phase 4d recommendation:** Option A (remain paused) is primary; Option D (docs-only reconciliation-model design memo specifying how a future reconciliation engine would interact with `RuntimeMode.RECOVERY_REQUIRED`, the runtime control persistence layer, the fake-exchange adapter, and the operator-review-required flag) is conditional secondary; Option C (richer fake-exchange lifecycle / failure-mode test slice — extending the fake adapter with cancel-and-replace stop lifecycle, partial fills, multiple-stop / orphaned-stop detection, stream-stale simulation, mark-price-vs-trade-price reference divergence, plus tests) and Option B (structured runtime logging / audit export slice — JSON-Lines structured logging, CLI export subcommand, defensive redaction, plus tests) are acceptable conditional alternatives only if separately authorized and preferably preceded by docs-only scoping (analogous to Phase 3x → Phase 4a); Option E (strategy-readiness gate design memo) is NOT recommended now (designing for a strategy that does not exist creates rhetorical drift toward strategy work); Option F (return-to-research / fresh hypothesis discovery) is NOT recommended now (per cumulative Phase 3t §14.2 + Phase 3u §14 + Phase 3v §17 + Phase 3w §17 + Phase 3x §18 + Phase 4a §22); Option G (Phase 4 canonical / paper-shadow / live-readiness / exchange-write) is FORBIDDEN / NOT recommended (per `docs/12-roadmap/phase-gates.md`, none of these gates is met). **Phase 4 canonical remains unauthorized.** **Phase 4e / any successor phase remains unauthorized.** **Paper/shadow, live-readiness, deployment, production keys, authenticated APIs, private endpoints, user stream, WebSocket, MCP, Graphify, `.mcp.json`, credentials, and exchange-write all remain unauthorized.** **No implementation code changed in Phase 4d.** **No strategy was implemented or validated by Phase 4d.** **No retained verdicts were revised.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks (including mark-price stops); v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`; Phase 3v §8 stop-trigger-domain governance; Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance; Phase 4a public API and runtime behavior — all preserved verbatim. **No project locks changed.** No diagnostics rerun. No backtests. No data acquisition / patching / regeneration / modification. No 5m strategy / hybrid / retained-evidence successor / new variant. No paper/shadow / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials work. No private endpoints / user stream / WebSocket / public endpoints consulted. No secrets stored or requested. **Recommended state remains paused.** **No next phase authorized.**

Phase 4e is the **Reconciliation-Model Design Memo** (docs-only) (operator selected the Phase 4d Option D conditional secondary alternative). Phase 4e defined the future reconciliation model for the local safe runtime foundation: state domains to compare (runtime control state; persisted runtime state; fake-exchange position state; fake-exchange order/stop state; future exchange snapshot state — design placeholder, forbidden; operator state view; governance labels; kill-switch state; operator-review-required flag; recovery-required status); classification taxonomy (13 classifications: `clean_consistent`, `local_only_no_external_exposure`, `fake_exchange_unknown_outcome`, `unprotected_position`, `stop_missing`, `stop_orphaned`, `multiple_stops`, `position_size_mismatch`, `side_mismatch`, `symbol_mismatch`, `stale_observation`, `governance_label_mismatch`, `unknown_or_unclassified` — with `unknown_or_unclassified` failing closed); input/output value-object contracts (`ReconciliationInput`, `ReconciliationResult`); `RuntimeMode.RECOVERY_REQUIRED` binding rules (transitions to / stays in `RECOVERY_REQUIRED` on unknown outcome, stale observation, unprotected position, mismatched position/stop state, governance-label mismatch, any non-clean classification, or any failed reconciliation precondition; requires explicit operator review before any return to `SAFE_MODE` or `RUNNING`); `operator_review_required` contract (persists across restart; never auto-clears; clearing it does NOT auto-resume `RUNNING`); kill-switch dominance (kill-switch dominates reconciliation; reconciliation must NOT clear kill-switch; reconciliation may recommend operator review but must NOT auto-clear emergency states; kill-switch persistence remains mandatory); persistence/audit requirements (append-only `reconciliation_event` table with run_id, UTC timestamps, classification, observed/local state summaries, recommended action, applied action, operator-review status, runtime-mode-after; persistence write failure fails closed; no secrets in audit); future event-contract family (7 design-only event types: `ReconciliationStarted`, `ReconciliationCompleted`, `ReconciliationMismatchDetected`, `ReconciliationActionRecommended`, `ReconciliationRecoveryRequired`, `OperatorReviewRequired`, `ReconciliationAuditRecorded`); fake-exchange test requirements (13 failure modes the richer fake adapter must simulate: partial fills; unknown entry outcome; missing protective stop; stop submission timeout; stop confirmation delay; orphaned stop; multiple stops; stale observation; position side mismatch; position size mismatch; mark-price-vs-trade-price reference divergence; cancel-and-replace lifecycle; local/fake state divergence); recovery-action taxonomy (10 actions: `no_action_clean`, `block_entries`, `enter_safe_mode`, `enter_emergency`, `enter_recovery_required`, `require_operator_review`, `record_audit_event`, `mark_fake_order_unknown`, `mark_fake_stop_unknown`, `future_real_exchange_action_required_but_forbidden` — the last is an explicit forbidden placeholder that falls back to `enter_recovery_required` + `require_operator_review` + `record_audit_event` until a separately authorized live phase exists); eleven fail-closed boundaries (missing local state; missing fake/external observation; stale observation; unknown runtime mode; unknown classification; `mixed_or_unknown` governance label; missing stop-trigger-domain; unprotected position; operator-review-required state; persistence write failure; event-validation failure). **Phase 4e was docs-only.** **Phase 4e does NOT implement reconciliation.** **Reconciliation governance is defined but not yet enforced in code.** Any future reconciliation implementation requires separate operator authorization. **Whole-repo quality gates remain clean** (verified during Phase 4e): `ruff check .` passed (`All checks passed!`); pytest passed (`785 passed in 12.81s`; no regressions); mypy strict passed (`Success: no issues found in 82 source files`). **Phase 4e recommendation:** Option A (remain paused) primary; Option B (docs-only richer-fake-exchange scoping memo) conditional secondary — preferred over Option C reconciliation-first because reconciliation needs richer divergence scenarios to test against; Option C (reconciliation engine against current bounded adapter) acceptable but suboptimal; Option D (structured runtime logging / audit export — independent of reconciliation; operator-visible value) acceptable conditional alternative; Option E (strategy-readiness gate) NOT recommended now (designing for a strategy that does not exist creates rhetorical drift toward strategy work); Option F (Phase 4 canonical / paper-shadow / live-readiness / exchange-write) FORBIDDEN / NOT recommended (per `docs/12-roadmap/phase-gates.md`, none of these gates is met). **Phase 4 canonical remains unauthorized.** **Phase 4f / any successor phase remains unauthorized.** **Paper/shadow, live-readiness, deployment, production keys, authenticated APIs, private endpoints, user stream, WebSocket, MCP, Graphify, `.mcp.json`, credentials, and exchange-write all remain unauthorized.** **No implementation code changed in Phase 4e.** **No strategy was implemented or validated by Phase 4e.** **No retained verdicts were revised.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks (including mark-price stops); v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`; Phase 3v §8 stop-trigger-domain governance; Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance; Phase 4a public API and runtime behavior — all preserved verbatim. **No project locks changed.** No diagnostics rerun. No backtests. No data acquisition / patching / regeneration / modification. No 5m strategy / hybrid / retained-evidence successor / new variant. No paper/shadow / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials work. No private endpoints / user stream / WebSocket / public endpoints consulted. No secrets stored or requested. **Recommended state remains paused.** **No next phase authorized.**

Phase 4f is the **External Strategy Research Landscape and V2 Hypothesis Candidate Memo** (docs-only) (operator selected return-to-research because the absence of a viable strategy is the main blocker). Phase 4f surveyed external systematic-trading evidence (academic and practitioner literature including Moskowitz / Ooi / Pedersen 2012 — TSMOM; Hurst / Ooi / Pedersen 2017 — A Century of Evidence on Trend-Following; Brock / Lakonishok / LeBaron 1992 — BLT classical technical-rule evidence; Liu / Tsyvinski 2018 / 2021 NBER — crypto-asset returns; BIS WP 1087 — crypto carry; Easley / O'Hara / Yang / Zhang 2024 — crypto microstructure; Bailey / Borwein / López de Prado / Zhu 2014 — PBO data-snooping discipline; Hattori 2024 — UK-evening BTC peak; Eross / Urquhart / Wolfe 2019 — BTC intraday periodicities; Han / Kang / Ryu 2024 — cryptocurrency time-series momentum; Manamala 2025 — volatility compression) and distinguished transferable from non-transferable institutional families: HFT / liquidity-provision / market-making is non-transferable to the operator's substrate; CTA / time-series momentum / trend-following is the strongest transferable family; volume / order-flow is strongest as confirmation / regime context, not a standalone signal; crypto derivatives-flow indicators (funding, basis, open interest, taker imbalance) are best treated as context / regime / cost lenses; 5m remains diagnostic-only, not primary signal. Phase 4f predeclared **V2 — Participation-Confirmed Trend Continuation** as a new ex-ante hypothesis candidate. **V2 is pre-research only: not implemented; not backtested; not validated; not live-ready; not a rescue of R3 / R2 / F1 / D1-A.** V2 core premise: trade trend-continuation / breakout events on BTCUSDT perpetual only when **price structure**, **volatility regime**, **participation / volume**, and **derivatives-flow context** align. V2 timeframe matrix: signal candidates 15m / 30m / 1h; bias candidates 1h / 4h; session / volume bucket candidates 30m / 1h; 5m diagnostic-only, not primary signal. V2 bounded feature policy: maximum **8** active entry features; maximum **3** active exit / regime features; all thresholds must be predeclared before any backtest. V2 validation requirements: predeclaration before backtest; chronological holdout (no shuffle / no bootstrap leakage); §11.6 HIGH cost sensitivity (8 bps per side floor); BTCUSDT primary + ETHUSDT comparison; deflated Sharpe / probability-of-backtest-overfitting (PBO) treatment if a grid search is performed; no live / paper implications from any V2 backtest. **Phase 4f was docs-only.** **Whole-repo quality gates remain clean** (verified during Phase 4f): `ruff check .` passed (`All checks passed!`); pytest passed (`785 passed`; no regressions); mypy strict passed (`Success: no issues found in 82 source files`). **Phase 4f recommendation:** Option B (docs-only V2 strategy-spec memo) is primary — predeclares V2 entry-feature set, exit / regime-feature set, all thresholds, and validation methodology *before* any backtest is run; Option C (docs-only V2 data-requirements and feasibility memo) is conditional secondary; Option A (remain paused) is procedurally acceptable; Option D (immediate data acquisition) is NOT recommended (parameter-tuning risk); Option E (immediate exploratory backtest) is REJECTED (data-snooping risk per Bailey / Borwein / López de Prado / Zhu 2014); Option F (paper/shadow / live-readiness / exchange-write) is FORBIDDEN. **No implementation code changed in Phase 4f.** **No data was acquired by Phase 4f.** **No backtests were run by Phase 4f.** **No strategy was implemented or validated by Phase 4f.** **No retained verdicts were revised.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks (including mark-price stops); v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`; Phase 3v §8 stop-trigger-domain governance; Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance; Phase 4a public API and runtime behavior; Phase 4e reconciliation-model design memo — all preserved verbatim. **No project locks changed.** **Phase 4 canonical remains unauthorized.** **Phase 4g / any successor phase remains unauthorized.** **V2 strategy-spec memo, V2 data-requirements / feasibility memo, V2 implementation, V2 backtests, V2 data acquisition all remain unauthorized.** **Paper/shadow, live-readiness, deployment, production keys, authenticated APIs, private endpoints, user stream, WebSocket, MCP, Graphify, `.mcp.json`, credentials, and exchange-write all remain unauthorized.** No diagnostics rerun. No Q1–Q7 rerun. No data acquisition / patching / regeneration / modification. No v002 dataset / manifest modification. No Phase 3q v001-of-5m manifest modification. No v003 dataset created. No `scripts/phase3q_5m_acquisition.py` or `scripts/phase3s_5m_diagnostics.py` execution. No private endpoints / user stream / WebSocket / public endpoints consulted in code. No secrets stored or requested. **Recommended state remains paused.** **No next phase authorized.**

Phase 4g is the **V2 Strategy-Spec Memo: Participation-Confirmed Trend Continuation** (docs-only) (operator selected the Phase 4f Option B primary recommendation). Phase 4g operationalized the Phase 4f V2 candidate hypothesis family into a precise, predeclared, bounded strategy specification: it selected exactly one signal timeframe (**30m**), one higher-timeframe bias (**4h**, EMA(20)/(50) discrete-comparison state), and one session / volume bucket (**1h**) from the Phase 4f §24 candidate matrix; it selected exactly **8 active entry features** (HTF trend bias state; Donchian breakout state; Donchian width percentile compression precondition; range-expansion ratio; relative volume + volume z-score; volume percentile by UTC hour; taker buy/sell imbalance; OI delta direction + funding-rate percentile band) and **3 active exit / regime features** (time-since-entry counter; ATR percentile regime; HTF bias state continuity), matching the Phase 4f §23 bound exactly; it predeclared the threshold grid for each chosen feature with **512 combinatorial variants** over 9 non-fixed binary axes (N1 Donchian breakout lookback; P_w max Donchian width percentile cap; V_rel_min relative volume min; V_z_min volume z-score min; T_imb_min taker-imbalance min; OI_dir OI delta direction policy; funding band; N_R fixed-R take-profit; T_stop time-stop horizon); it predeclared the **M1 / M2 / M3 mechanism-check decomposition** (M1 price-structure: ≥50% trades reaching +0.5R MFE on BTC AND ETH; M2 participation: ≥+0.10R differential vs. participation-relaxed degenerate variant on BTC AND ETH; M3 derivatives-context: ≥+0.05R differential AND §11.6 HIGH cost-resilience non-degraded); and it declared all four governance labels (`stop_trigger_domain` research = `trade_price_backtest`, future runtime = `mark_price_runtime`, future mark-price validation = `mark_price_backtest_candidate`; `break_even_rule = disabled`; `ema_slope_method = discrete_comparison`; `stagnation_window_role = metric_only`; `mixed_or_unknown` invalid / fail-closed for all four schemes). **Phase 4g was docs-only.** **V2 remains pre-research only: not implemented; not backtested; not validated; not live-ready; not a rescue of R3 / R2 / F1 / D1-A.** V2 is structurally distinct from R3 / R2 / F1 / D1-A (V2 uses 30m signal vs. V1's 15m; 4h bias vs. V1's 1h; Donchian-channel-based trend state vs. V1's EMA(50)/(200) state; longer compression lookback; REQUIRES participation / volume confirmation which V1 does not; REQUIRES non-pathological derivatives-flow context which V1 does not; symmetric long / short with trend-continuation directional bias, NOT a contrarian funding trade like D1-A). **Whole-repo quality gates remain clean** (verified during Phase 4g): `ruff check .` passed (`All checks passed!`); pytest passed (`785 passed in 12.59s`; no regressions); mypy strict passed (`Success: no issues found in 82 source files`). **Phase 4g recommendation:** Phase 4h V2 Data Requirements and Feasibility Memo (docs-only) primary; remain paused conditional secondary; immediate data acquisition NOT recommended; immediate backtest REJECTED (data-snooping risk per Bailey / Borwein / López de Prado / Zhu 2014); V2 implementation REJECTED; paper/shadow / live-readiness / exchange-write FORBIDDEN. **No implementation code changed in Phase 4g.** **No data acquired by Phase 4g.** **No backtests run by Phase 4g.** **No strategy was implemented or validated by Phase 4g.** **No retained verdicts were revised.** **No Phase 4f text modified.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks (including mark-price stops); v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`; Phase 3v §8 stop-trigger-domain governance; Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance; Phase 4a public API and runtime behavior; Phase 4e reconciliation-model design memo; Phase 4f V2 hypothesis predeclaration — all preserved verbatim. **No project locks changed.** **Phase 4 canonical remains unauthorized.** **Phase 4h / any successor phase remains unauthorized.** **V2 data-requirements / feasibility memo, V2 implementation, V2 backtests, V2 data acquisition all remain unauthorized.** **Paper/shadow, live-readiness, deployment, production keys, authenticated APIs, private endpoints, user stream, WebSocket, MCP, Graphify, `.mcp.json`, credentials, and exchange-write all remain unauthorized.** No diagnostics rerun. No Q1–Q7 rerun. No data acquisition / patching / regeneration / modification. No v002 dataset / manifest modification. No Phase 3q v001-of-5m manifest modification. No v003 dataset created. No `scripts/phase3q_5m_acquisition.py` or `scripts/phase3s_5m_diagnostics.py` execution. No private endpoints / user stream / WebSocket / public endpoints consulted in code. No secrets stored or requested. **Recommended state remains paused.** **No next phase authorized.**

Phase 4h is the **V2 Data Requirements and Feasibility Memo** (docs-only) (operator selected the Phase 4g §38 / Phase 4f §30 primary recommendation). Phase 4h translated the locked Phase 4g V2 strategy spec (signal 30m; bias 4h; session / volume bucket 1h; 8 entry features + 3 exit / regime features; 512-variant threshold grid; M1 / M2 / M3 mechanism-check decomposition; four governance labels) into an exact, predeclared data-requirements and feasibility plan covering: required dataset families; public-source availability; dataset-versioning convention (`binance_usdm_<symbol>_<interval>__v001` for new families: 30m klines × 2, 4h klines × 2, `metrics` × 2; mark-price 30m / 4h DEFERRED; aggTrades OPTIONAL / DEFERRED); directory-layout proposal; manifest-field schema; per-family integrity-check rules; strict `research_eligible` rules (per Phase 3p §4.7 / Phase 3r §8 — no forward-fill, no silent patching); invalid-window handling (Phase 3r §8 semantics; `metrics`-family extension if gaps detected); point-in-time-valid alignment / timestamp policy (UTC ms canonical; bar `open_time` primary key; bar-completed-only decisioning; 30m signal bar / 4h bias bar / 1h session bucket completion required; no future-funding / OI / flow values); cost / slippage data assumptions (§11.6 = 8 bps HIGH per side preserved verbatim); and a Phase 4i acquisition execution plan preview (public bulk archive only, no credentials, no private endpoints, paired SHA256 verification, fail-closed integrity-check stop conditions). **Feasibility verdict: POSITIVE under defined boundary.** All Phase 4g V2 features can be supported by public unauthenticated Binance bulk / public data; no private / authenticated / spot / order-book / user-stream data required; no credentials required; no feasibility blocker identified; Phase 4h does NOT recommend revising Phase 4g. **Phase 4h was docs-only.** **V2 remains pre-research only: not implemented; not backtested; not validated; not live-ready; not a rescue of R3 / R2 / F1 / D1-A.** Minimum future Phase 4i acquisition set: BTCUSDT 30m trade-price klines; ETHUSDT 30m trade-price klines; BTCUSDT 4h trade-price klines; ETHUSDT 4h trade-price klines; BTCUSDT `metrics`; ETHUSDT `metrics`. Funding-rate history reuses existing v002 funding manifests. **Whole-repo quality gates remain clean** (verified during Phase 4h): `ruff check .` passed (`All checks passed!`); pytest passed (`785 passed in 12.87s`; no regressions); mypy strict passed (`Success: no issues found in 82 source files`). **Phase 4h recommendation:** Phase 4i V2 Public Data Acquisition and Integrity Validation (docs-and-data, public bulk archives only, no credentials) primary; remain paused conditional secondary; revise V2 spec NOT recommended; immediate V2 backtest REJECTED; V2 implementation REJECTED; paper/shadow / live-readiness / exchange-write FORBIDDEN. **No implementation code changed in Phase 4h.** **No data acquired by Phase 4h.** **No data downloaded by Phase 4h.** **No manifests modified by Phase 4h.** **No backtests run by Phase 4h.** **No strategy was implemented or validated by Phase 4h.** **No retained verdicts were revised.** **No Phase 4f / 4g text modified.** **No Phase 3r §8 mark-price gap governance modified.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks (including mark-price stops); v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`; Phase 3r §8 mark-price gap governance; Phase 3v §8 stop-trigger-domain governance; Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance; Phase 4a public API and runtime behavior; Phase 4e reconciliation-model design memo; Phase 4f V2 hypothesis predeclaration; Phase 4g V2 strategy spec — all preserved verbatim. **No project locks changed.** **Phase 4 canonical remains unauthorized.** **Phase 4i / any successor phase remains unauthorized.** **V2 data acquisition, V2 implementation, V2 backtests all remain unauthorized.** **Paper/shadow, live-readiness, deployment, production keys, authenticated APIs, private endpoints, user stream, WebSocket, MCP, Graphify, `.mcp.json`, credentials, and exchange-write all remain unauthorized.** No diagnostics rerun. No Q1–Q7 rerun. No data acquisition / patching / regeneration / modification. No v002 dataset / manifest modification. No Phase 3q v001-of-5m manifest modification. No v003 dataset created. No `scripts/phase3q_5m_acquisition.py` or `scripts/phase3s_5m_diagnostics.py` execution. No private endpoints / user stream / WebSocket / public endpoints consulted in code. No secrets stored or requested. **Recommended state remains paused.** **No next phase authorized.**

Phase 4i is the **V2 Public Data Acquisition and Integrity Validation** phase (docs-and-data) (operator selected the Phase 4h §37 primary recommendation). Phase 4i acquired exactly the six Phase 4h-predeclared minimum V2 dataset families from public unauthenticated `data.binance.vision` bulk archives for the date range 2022-01-01 through 2026-03-31 UTC: BTCUSDT 30m trade-price klines; ETHUSDT 30m trade-price klines; BTCUSDT 4h trade-price klines; ETHUSDT 4h trade-price klines; BTCUSDT `metrics`; ETHUSDT `metrics`. **Phase 4i did NOT acquire mark-price 30m / 4h** (DEFERRED per Phase 4h §20). **Phase 4i did NOT acquire aggTrades** (OPTIONAL / DEFERRED per Phase 4h §7.E). **Phase 4i did NOT re-acquire funding-rate history** (v002 funding manifests reused per Phase 4h §22). Phase 4i added the standalone acquisition orchestrator `scripts/phase4i_v2_acquisition.py` (public unauthenticated `data.binance.vision` only, no credentials, no `.env`, no API-key support, no authenticated REST, no private endpoints, no WebSocket, no user-stream, no listenKey lifecycle), normalized acquired data to Parquet under the existing repository partition convention, generated six new manifests under `data/manifests/`, and ran the Phase 4h §17 strict integrity-check evidence specification on each dataset. Total archives acquired: 3 306 (204 monthly klines + 3 102 daily metrics) at 8 parallel workers, ~11 minutes wall-clock, with SHA256-verification of every raw archive against its paired `.CHECKSUM` companion file. `data/raw/**` and `data/normalized/**` are gitignored (locally reproducible from public sources via the orchestrator script); the six new manifests are committed (force-added past the existing `data/manifests/**` gitignore rule per the Phase 4i brief's "Allowed commit contents" clause). **Phase 4i verdict: PARTIAL PASS** — 4 of 6 datasets are research-eligible; 2 of 6 (metrics) FAIL Phase 4h §17.4 strict gate. **Research-eligible datasets:** `binance_usdm_btcusdt_30m__v001` (74 448 bars, 0 gaps); `binance_usdm_ethusdt_30m__v001` (74 448 bars, 0 gaps); `binance_usdm_btcusdt_4h__v001` (9 306 bars, 0 gaps); `binance_usdm_ethusdt_4h__v001` (9 306 bars, 0 gaps). **Not research-eligible datasets:** `binance_usdm_btcusdt_metrics__v001`; `binance_usdm_ethusdt_metrics__v001`. **Metrics failure reason:** intra-day 5-minute missing observations (BTC: 5 699 missing across 4 years; ETH: 3 631 missing; ~0.03 % of expected 4-year coverage); NaNs in optional ratio columns (`count/sum_toptrader_long_short_ratio`, `count_long_short_ratio`, `sum_taker_long_short_vol_ratio`) concentrated in early-2022 data (~97% NaN for early-2022 ratio columns; ~0% NaN for 2026-03 ratio columns); the required `sum_open_interest` and `sum_open_interest_value` columns are FULLY POPULATED (zero NaN) for both symbols across the entire 4-year coverage. **Phase 4i did NOT relax strict gate rules.** **Phase 4i did NOT patch, forward-fill, interpolate, or silently omit data.** All gaps and NaN counts are recorded verbatim in `quality_checks.gap_locations`, `invalid_windows`, and `nonfinite_violations` of the affected manifests. **Phase 4i stops for operator review** per the brief failure-path. **Immediate V2 backtest remains REJECTED** per the Phase 4i brief's "If any family is not research_eligible, Phase 4i must stop for operator review and must not proceed to any backtest or successor phase." **V2 implementation remains REJECTED.** A future docs-only metrics governance memo analogous to Phase 3r §8 (e.g., proposing per-bar exclusion when an alignment-required metrics record is missing OR a partial-eligibility scheme limited to the OI subset) is **conditional secondary only** and is **NOT started by this merge**. **Whole-repo quality gates remain clean** (verified during Phase 4i): `ruff check .` passed (`All checks passed!`); pytest passed (`785 passed in 12.75s`; no regressions); mypy strict passed (`Success: no issues found in 82 source files`). **V2 remains pre-research only: not implemented; not backtested; not validated; not live-ready; not a rescue of R3 / R2 / F1 / D1-A.** **No retained verdicts were revised.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks (including mark-price stops); v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`; Phase 3r §8 mark-price gap governance; Phase 3v §8 stop-trigger-domain governance; Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance; Phase 4a public API and runtime behavior; Phase 4e reconciliation-model design memo; Phase 4f V2 hypothesis predeclaration; Phase 4g V2 strategy spec; Phase 4h V2 data-requirements / feasibility memo — all preserved verbatim. **No project locks changed.** **Phase 4 canonical remains unauthorized.** **Phase 4j / any successor phase remains unauthorized.** **Paper/shadow, live-readiness, deployment, production keys, authenticated APIs, private endpoints, user stream, WebSocket, MCP, Graphify, `.mcp.json`, credentials, and exchange-write all remain unauthorized.** No diagnostics run. No Q1–Q7 run. No backtests run. No mark-price 30m / 4h acquired. No aggTrades acquired. No spot data acquired. No cross-venue data acquired. No funding-rate re-acquired. No v002 dataset / manifest modification. No Phase 3q v001-of-5m manifest modification. No v003 dataset created. No `scripts/phase3q_5m_acquisition.py` or `scripts/phase3s_5m_diagnostics.py` execution. No `prometheus.research.data.*` extension. No `Interval` enum extension. No private endpoints / user stream / WebSocket / authenticated REST consulted in code. No secrets stored or requested. **Recommended state remains paused.** **No next phase authorized.**

Phase 4j is the **V2 Metrics Data Governance Memo** (docs-only) (operator selected the Phase 4i §"Operator decision menu" Option B conditional secondary alternative — docs-only metrics governance memo analogous to Phase 3r §8). Phase 4j adopts the **Phase 4j §11 metrics OI-subset partial-eligibility rule** as the binding governance for the Phase 4i metrics partial-pass evidence. The rule mirrors Phase 3r §8 mark-price gap governance, transposed from per-trade exclusion (Q6 mark-price) to per-bar exclusion (V2 candidate setup metrics OI). **Metrics manifests remain globally `research_eligible: false`.** Phase 4i metrics manifests (`binance_usdm_btcusdt_metrics__v001.manifest.json` and `binance_usdm_ethusdt_metrics__v001.manifest.json`) are NOT modified. **No corrected metrics manifests are created. No `__v002` metrics manifests are created. No v003 is created.** **Feature-level partial-eligibility is allowed only for the OI subset:** `create_time`, `symbol`, `sum_open_interest`, `sum_open_interest_value`. **Optional ratio columns remain `feature_eligible: false` and forbidden for V2 first backtest:** `count_toptrader_long_short_ratio`, `sum_toptrader_long_short_ratio`, `count_long_short_ratio`, `sum_taker_long_short_vol_ratio`. **Per-bar exclusion rule:** any 30m V2 signal bar is OI-feature-eligible only if all six aligned 5-minute metrics records (at offsets 0, 5, 10, 15, 20, 25 minutes from the bar's open_time) are present AND each has non-NaN `sum_open_interest` AND non-NaN `sum_open_interest_value`; any 30m signal bar failing this check is excluded from V2 candidate setup generation entirely. **No forward-fill, interpolation, imputation, replacement, synthetic OI data, or silent omission is allowed.** **Future V2 backtest must report exclusion counts** (per-symbol, per-day, per-30m-bar with reason `metrics_oi_missing_or_invalid`, cumulative) **and the required sensitivity analysis** comparing main-cell V2 results vs. the exclude-entire-affected-days sensitivity cell (a stricter variant that ALSO excludes any 30m bar whose date contains ANY metrics `invalid_window`). **OI delta computation rule:** for each OI-feature-eligible 30m signal bar, `oi_delta = oi_at(bar_open + 25min) - oi_at(bar_open - 5min)` — i.e., last completed 5-minute OI of current 30m window vs. last completed 5-minute OI of previous 30m window (point-in-time clear; no future records; no partial windows; no mean-over-window aggregation). The rule is **immutable from operator approval (this merge) forward**; future amendments require a separately authorized governance memo amending Phase 4j §11 explicitly. **Immediate V2 backtest remains unauthorized.** **Future V2 backtest-plan memo (Phase 4j conditional secondary; future Phase 4k) is conditional secondary only and is NOT started by this merge.** **V2 implementation remains unauthorized.** **Optional ratio-column activation remains unauthorized.** **OI feature removal from V2 remains unauthorized.** **Mark-price 30m / 4h acquisition remains unauthorized.** **`aggTrades` acquisition remains unauthorized.** **Phase 4j was docs-only.** **Whole-repo quality gates remain clean** (verified during Phase 4j): `ruff check .` passed (`All checks passed!`); pytest passed (`785 passed in 12.53s`; no regressions); mypy strict passed (`Success: no issues found in 82 source files`). **V2 remains pre-research only: not implemented; not backtested; not validated; not live-ready; not a rescue of R3 / R2 / F1 / D1-A.** **No data acquired by Phase 4j.** **No data modified by Phase 4j.** **No manifests modified by Phase 4j.** **No source code modified by Phase 4j.** **No tests modified by Phase 4j.** **No backtests run by Phase 4j.** **No retained verdicts were revised.** **No Phase 4f / 4g / 4h / 4i text modified.** **No Phase 4i acquisition script modified or executed.** **No Phase 3r §8 governance modified.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks (including mark-price stops); v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`; Phase 3r §8 mark-price gap governance; Phase 3v §8 stop-trigger-domain governance; Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance; Phase 4a public API and runtime behavior; Phase 4e reconciliation-model design memo; Phase 4f V2 hypothesis predeclaration; Phase 4g V2 strategy spec; Phase 4h V2 data-requirements / feasibility memo; Phase 4i V2 acquisition + integrity report; Phase 4i metrics manifests `research_eligible: false` — all preserved verbatim. **No project locks changed.** **Phase 4 canonical remains unauthorized.** **Phase 4k / any successor phase remains unauthorized.** **Paper/shadow, live-readiness, deployment, production keys, authenticated APIs, private endpoints, user stream, WebSocket, MCP, Graphify, `.mcp.json`, credentials, and exchange-write all remain unauthorized.** No diagnostics run. No Q1–Q7 run. No backtests run. No mark-price 30m / 4h acquired. No aggTrades acquired. No spot data acquired. No cross-venue data acquired. No funding-rate re-acquired. No v002 dataset / manifest modification. No Phase 3q v001-of-5m manifest modification. No Phase 4i manifest modification. No v003 dataset created. No `scripts/phase3q_5m_acquisition.py` or `scripts/phase3s_5m_diagnostics.py` or `scripts/phase4i_v2_acquisition.py` execution. No private endpoints / user stream / WebSocket / authenticated REST consulted in code. No secrets stored or requested. **Recommended state remains paused.** **No next phase authorized.**

Phase 4k is the **V2 Backtest-Plan Memo** (docs-only) (operator selected the Phase 4j §1 / §17.2 recommended next phase: docs-only V2 backtest-plan memo under the Phase 4j §11 metrics OI-subset partial-eligibility rule). **Phase 4k authored a complete predeclared V2 backtest methodology before any V2 backtest code or execution exists.** Phase 4k locks the future V2 backtest plan to the Phase 4g V2 strategy spec (signal 30m, bias 4h, session bucket 1h, 8 entry + 3 exit / regime active features, 512-variant predeclared threshold grid, M1 / M2 / M3 mechanism-check decomposition, four governance labels), the Phase 4i acquired dataset inputs (4 research-eligible kline datasets `binance_usdm_btcusdt_30m__v001`, `binance_usdm_ethusdt_30m__v001`, `binance_usdm_btcusdt_4h__v001`, `binance_usdm_ethusdt_4h__v001`; 2 globally non-research-eligible metrics datasets `binance_usdm_btcusdt_metrics__v001`, `binance_usdm_ethusdt_metrics__v001` used only via Phase 4j §11 OI subset; existing v002 funding manifests reused; no mark-price 30m / 4h; no aggTrades; no optional metrics ratio columns), the Phase 4j §11 metrics OI-subset partial-eligibility rule (binding), the 11 active V2 features predeclared per-feature implementation plans (HTF trend bias state; Donchian breakout state; Donchian width percentile; range-expansion ratio; relative volume + volume z-score; volume percentile by UTC hour; taker buy/sell imbalance via kline `taker_buy_volume`; OI delta direction + funding-rate percentile band; time-since-entry counter; ATR percentile regime; HTF bias state continuity), the Phase 4j §11 per-bar exclusion algorithm restated verbatim (six aligned 5-minute records required at offsets 0, 5, 10, 15, 20, 25 minutes from 30m bar open with non-NaN OI; bars failing the check excluded from V2 candidate setup generation; no forward-fill / interpolation / imputation / synthetic data / silent omission), the categorical optional-ratio-column non-access enforcement (forbidden by Phase 4j §11.3 / §14), the signal-generation truth table per Phase 4g §13, the entry execution model (MARKET-at-next-30m-open per Phase 4g §13), the exit model (initial structural stop + 0.10 × ATR(20) buffer with 0.60 × ATR(20) ≤ stop distance ≤ 1.80 × ATR(20); fixed-R take-profit `N_R ∈ {2.0, 2.5}`; unconditional time-stop `T_stop ∈ {12, 16}` 30m bars; stop-precedence stop > take-profit > time-stop; conservative stop-first tie-break), the cost / slippage cells (LOW = 1 bp, MEDIUM = 4 bps, HIGH = 8 bps per side preserved verbatim per §11.6 = 8 bps HIGH; funding cost included; no maker rebate; no live fee assumption; no cost-model relaxation), the position-sizing constraints (0.25% risk; 2× leverage cap; one position; BTCUSDT primary; ETHUSDT comparison only; no pyramiding; no reversal while positioned; lot-size rounding; below-min-quantity rejects), the threshold-grid handling policy (Phase 4g §29 fixed at 512 variants; Phase 4k recommends Option B — full PBO / deflated Sharpe / CSCV with 512 variants reported and no further reduction; deterministic lexicographic variant ordering; no early exit on bad variants; no outcome-driven threshold selection), the chronological train / validation / OOS holdout split with **exact UTC date boundaries: train 2022-01-01 00:00:00 UTC through 2023-06-30 23:30:00 UTC (~18 months); validation 2023-07-01 00:00:00 UTC through 2024-06-30 23:30:00 UTC (~12 months); out-of-sample holdout 2024-07-01 00:00:00 UTC through 2026-03-31 23:30:00 UTC (~21 months — primary V2 evidence cell)**, the no-data-shuffle / no-leakage / no-window-modification-post-hoc discipline, the optional walk-forward extension (4 rolling 12-month OOS windows; if omitted must be justified), the BTCUSDT-primary / ETHUSDT-comparison protocol (cross-symbol consistency required; ETH cannot rescue BTC failure; no cross-symbol optimization; no choosing BTC-only or ETH-only after seeing outcomes; same 512 variants evaluated independently per symbol), the M1 / M2 / M3 mechanism-check implementation per Phase 4g §30 (M1 ≥ 50% trades reach +0.5R MFE on BOTH symbols; M2 ≥ +0.10R uplift over participation-relaxed degenerate variant on BOTH symbols with bootstrap-by-trade B = 10 000 stat-significance; M3 ≥ +0.05R uplift over derivatives-relaxed degenerate variant AND §11.6 HIGH cost-resilience non-degraded with ε = 0.05R; minimum bar M1 PASS + M2 PASS + M3 PASS + §11.6 HIGH cost-survival + cross-symbol consistency + OOS persistence), the §11.6 HIGH cost-sensitivity gate preserved verbatim (V2 candidates failing §11.6 HIGH on either symbol FAIL framework promotion per R2's failure pattern), 12 catastrophic-floor predicates predeclared (CFP-1 insufficient trade count; CFP-2 negative OOS expectancy under HIGH cost; CFP-3 catastrophic drawdown >10R or PF<0.50; CFP-4 BTC-fails-with-ETH-passes; CFP-5 train-only with OOS failure; CFP-6 excessive PBO > 0.5; CFP-7 regime/month overconcentration > 50%; CFP-8 sensitivity-cell failure under exclude-entire-affected-days; CFP-9 excluded-bar-fraction anomaly > 5%; CFP-10 optional-ratio-column access detected; CFP-11 per-bar exclusion algorithm deviation from Phase 4j §16; CFP-12 forbidden data access), the Verdict A / B / C / D classification taxonomy (A V2 framework PASS — research-promotable, NOT implementation authorization; B V2 framework PARTIAL PASS — research evidence only; C V2 framework HARD REJECT — analogous to F1 / D1-A; D V2 framework INCOMPLETE — methodology stop), the deflated Sharpe correction per Bailey & López de Prado (2014) and Probability of Backtest Overfitting (PBO) per Bailey / Borwein / López de Prado / Zhu (2014) with combinatorially symmetric cross-validation (CSCV) S = 16 chronologically-respecting sub-samples (12 870 combinations) and minimum train-window trade count `T >= 30` per variant for DSR computation, 22 required reporting tables (run metadata; dataset manifest references with SHA pinning; parameter grid; train / validation / OOS split; per-variant trade summaries BTC + ETH × 3 windows × MEDIUM-slip; BTC-train-best variant identification + cost-cell sensitivity; M1 / M2 / M3 mechanism-check tables; cost-sensitivity comparison; PBO; deflated-Sharpe summary; CSCV S = 16 sub-sample rankings; metrics-OI exclusion table; main-cell vs. exclude-entire-affected-days sensitivity; trade distribution by year / month / regime; verdict declaration; forbidden-work confirmation), 10 required plot artefacts (cumulative-R curves BTC + ETH per window; variant-by-window Sharpe heatmap; DSR distribution histograms; PBO sub-sample rank distribution; drawdown curve; trade-distribution histogram; monthly-bucketed cumulative-R; excluded-bar count timeseries; sensitivity-cell vs. main-cell mean_R), 16 stop conditions (manifest missing / SHA mismatch; data file not found / corrupted; CFP-10 / CFP-11 / CFP-12; lookahead detected; timestamp misalignment; trades on excluded bars; trade-count-insufficient on > 50% variants; validation report incomplete; authentication-API / private-endpoint / live-API access attempt; credential read / store attempt; network I/O outside `data.binance.vision` public bulk; write attempt to `data/raw/` / `data/normalized/` / `data/manifests/`; pytest test count regression; ruff / mypy violation), and the reproducibility requirements (public unauthenticated source only; SHA256 verification; deterministic variant ordering; pinned RNG seeds; idempotent rerun; manifest SHA pinning in report; standalone-script pattern at `scripts/phase4l_v2_backtest.py` with no `prometheus.runtime.*` / `prometheus.execution.*` / `prometheus.persistence.*` / network-I/O imports; no test modification; preserved whole-repo quality gate). **Phase 4k recommendation: Phase 4l V2 Backtest Execution (docs-and-code) primary; remain paused conditional secondary; methodology refinement / Phase 4j §11 amendment / V2 spec amendment / mark-price 30m+4h acquisition / aggTrades acquisition NOT recommended; immediate V2 implementation REJECTED; paper / shadow / live-readiness / exchange-write FORBIDDEN.** **Phase 4l is NOT authorized by the Phase 4k merge.** **Phase 4k was docs-only.** **Whole-repo quality gates remain clean** (verified during Phase 4k): `ruff check .` passed (`All checks passed!`); pytest passed (`785 passed in 12.48s`; no regressions); mypy strict passed (`Success: no issues found in 82 source files`). **V2 remains pre-research only: not implemented; not backtested; not validated; not live-ready; not a rescue of R3 / R2 / F1 / D1-A.** **No data acquired by Phase 4k.** **No data modified by Phase 4k.** **No manifests modified by Phase 4k.** **No source code modified by Phase 4k.** **No tests modified by Phase 4k.** **No scripts modified by Phase 4k.** **No backtests run by Phase 4k.** **No V2 backtest code written by Phase 4k.** **No V2 implementation by Phase 4k.** **No retained verdicts were revised.** **No Phase 4f / 4g / 4h / 4i / 4j text modified.** **No Phase 4i acquisition script modified or executed.** **No Phase 4j §11 governance modified.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks (including mark-price stops); v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`; Phase 3r §8 mark-price gap governance; Phase 3v §8 stop-trigger-domain governance; Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance; Phase 4a public API and runtime behavior; Phase 4e reconciliation-model design memo; Phase 4f V2 hypothesis predeclaration; Phase 4g V2 strategy spec; Phase 4h V2 data-requirements / feasibility memo; Phase 4i V2 acquisition + integrity report; Phase 4i metrics manifests `research_eligible: false`; Phase 4j §11 metrics OI-subset partial-eligibility rule — all preserved verbatim. **No project locks changed.** **Phase 4 canonical remains unauthorized.** **Phase 4l / any successor phase remains unauthorized.** **Paper/shadow, live-readiness, deployment, production keys, authenticated APIs, private endpoints, user stream, WebSocket, MCP, Graphify, `.mcp.json`, credentials, and exchange-write all remain unauthorized.** No diagnostics run. No Q1–Q7 run. No backtests run. No mark-price 30m / 4h acquired. No aggTrades acquired. No spot data acquired. No cross-venue data acquired. No funding-rate re-acquired. No v002 dataset / manifest modification. No Phase 3q v001-of-5m manifest modification. No Phase 4i manifest modification. No v003 dataset created. No `scripts/phase3q_5m_acquisition.py` or `scripts/phase3s_5m_diagnostics.py` or `scripts/phase4i_v2_acquisition.py` execution. No private endpoints / user stream / WebSocket / authenticated REST consulted in code. No secrets stored or requested. **Recommended state remains paused.** **No next phase authorized.**

Current phase:

```text
Phase 4k merged into main (V2 Backtest-Plan Memo, docs-only).
Phase 4k authored a complete predeclared V2 backtest methodology before any V2 backtest code or execution exists.
Phase 4k locks the future V2 backtest plan to: Phase 4g V2 strategy spec; Phase 4i acquired dataset inputs; Phase 4j §11 metrics OI-subset governance; 512-variant threshold grid; PBO / deflated Sharpe / CSCV treatment; chronological train / validation / OOS split; BTCUSDT-primary / ETHUSDT-comparison protocol; M1 / M2 / M3 mechanism checks; catastrophic-floor predicates; required reporting tables and plots; stop conditions; reproducibility requirements.
Phase 4k selected exact validation windows: train 2022-01-01 through 2023-06-30 UTC; validation 2023-07-01 through 2024-06-30 UTC; OOS holdout 2024-07-01 through 2026-03-31 UTC.
Phase 4k recommendation: Phase 4l V2 Backtest Execution (docs-and-code) is primary; remain paused is conditional secondary.
Phase 4l is NOT authorized by this merge.
No V2 backtest was run.
No V2 backtest code was written.
No V2 implementation occurred.
No data was acquired.
No data was modified.
No manifests were modified.
No source code, tests, or scripts were modified.
V2 remains pre-research only: not implemented; not backtested; not validated; not live-ready; not a rescue of R3 / R2 / F1 / D1-A.
Whole-repo quality gates remain clean: ruff check . passed; pytest 785 passed; mypy strict 0 issues across 82 source files.
No retained verdicts were revised.
No project locks changed.
Phase 4 (canonical) remains unauthorized.
Phase 4l / any successor phase remains unauthorized.
Paper/shadow, live-readiness, deployment, production keys, authenticated APIs, private endpoints, user stream, WebSocket, MCP, Graphify, .mcp.json, credentials, and exchange-write all remain unauthorized.
All four Phase 3u §8.5 pre-coding governance blockers remain RESOLVED at governance level (GAP-20260424-032 by Phase 3v; GAP-20260424-030 / 031 / 033 by Phase 3w).
Four governance label schemes binding prospectively: stop_trigger_domain | break_even_rule | ema_slope_method | stagnation_window_role.
mixed_or_unknown is invalid and fails closed for all four schemes.
Phase 4j §11 metrics OI-subset partial-eligibility rule is binding from the Phase 4j merge forward; immutable absent a separately authorized governance amendment.
Phase 4k V2 backtest-plan methodology is binding from this merge forward; immutable absent a separately authorized governance amendment.
Recommended state: paused.
No next phase authorized.
```

Most recent merge:

```text
main HEAD:                          95fd3edaa69369af496800c157e298afa508803e
Merge title:                        Merge Phase 4k (V2 backtest-plan memo, docs-only) into main
Phase 4k memo commit:               c26eb27bda53262cb92742295488b5e23137e5bc
Phase 4k closeout commit:           352a9fbfdded244fa281f43e5afa9356364fa9fe
Phase 4k merge commit:              95fd3edaa69369af496800c157e298afa508803e
```

## Strategy Research Arc Outcomes

The two complete strategy-research arcs produced these outcomes:

### V1 breakout arc (Phase 2e through Phase 2w)

- **H0** — locked Phase 2e baseline; remains the **framework anchor**.
- **R3** (Fixed-R take-profit + unconditional time-stop, Phase 2p §C.1) — **baseline-of-record**.
- **R1a** (volatility-percentile setup predicate) — retained as **research evidence**; **non-leading**.
- **R1b-narrow** (bias-strength magnitude threshold) — retained as **research evidence**; **non-leading**.
- **R2** (pullback-retest entry) — final verdict **FAILED — §11.6 cost-sensitivity gate blocks**. M1 ✓, M3 ✓, M2 ✗ (mechanism partially supported); slippage-fragile. Retained as **research evidence** per Phase 2p §D framing.

### F1 mean-reversion arc (Phase 3a through Phase 3d-B2)

- **F1** (mean-reversion-after-overextension; 8-bar cumulative displacement > 1.75 × ATR(20) → SMA(8) frozen target; structural stop with 0.10 × ATR buffer; 8-bar unconditional time-stop; same-direction cooldown until unwind). Phase 3a discovery rank-1 near-term family candidate; Phase 3b spec; Phase 3c execution-planning; Phase 3d-A implementation (deliberately non-runnable); Phase 3d-B1 engine wiring (runnable but guarded); Phase 3d-B2 first execution + first-execution-gate evaluation. **Final verdict: HARD REJECT** (Phase 3c §7.3 catastrophic-floor predicate; 5 separate violations across BTC/ETH × MED/HIGH cells: BTC MED expR=−0.5227, BTC HIGH expR=−0.7000 / PF=0.2181, ETH HIGH expR=−0.5712 / PF=0.2997). M1 BTC PARTIAL (mean +0.024 R below +0.10 threshold; fraction 55.4%); M2 BTC FAIL / ETH weak-PASS; M3 PASS-isolated on both symbols (TARGET subset profitable when isolated, but overwhelmed by 53–54% STOP exits in the wider trade population). **Phase 3d-B2 is terminal for F1.** F1 retained as **research evidence**; **non-leading**; no F1-prime authorized.

### D1-A funding-aware arc (Phase 3f through Phase 3j)

- **D1-A** (funding-aware directional / carry-aware contrarian; trailing-90-day funding-rate Z-score |Z_F| ≥ 2.0 at completed funding-settlement time → enter contrarian at next 15m bar's open; stop = 1.0 × ATR(20); fixed +2.0R target; 32-bar (8-hour) unconditional time-stop; per-funding-event cooldown; band [0.60, 1.80] × ATR(20); contrarian direction; no regime filter). Phase 3f research-direction discovery (post-F1 rank-1 active-path candidate); Phase 3g spec memo + methodology audit; Phase 3h execution-planning memo with timing-clarification amendments; Phase 3i-A implementation-controls (deliberately non-runnable); Phase 3i-B1 engine-wiring (runnable but guarded); Phase 3j first execution + first-execution-gate evaluation. **Final verdict: MECHANISM PASS / FRAMEWORK FAIL — other** (Phase 3h §11.2; catastrophic-floor predicate NOT triggered; cond_i BTC MED expR > 0 FAILED with BTC R MED expR=−0.3217; cond_iv BTC HIGH cost-resilience FAILED with BTC R HIGH expR=−0.4755 / PF=0.5145). M1 BTC h=32 PASS (mean +0.1748 R AND fraction-non-negative 0.5101 — both above thresholds); M2 FAIL on both symbols (BTC funding benefit +0.00234 R ~21× below +0.05 R threshold; ETH +0.00452 R ~11× below); M3 PASS-isolated on both symbols (TARGET subset BTC mean +2.143 R / aggregate +111.46 R; ETH mean +2.447 R / aggregate +119.89 R — overwhelmed by 67–68% STOP exits at −1.30 / −1.24 R mean per loser). Empirical WR ~30% / ~31% vs forecast +51% breakeven. **Phase 3j is terminal for D1-A under the current locked spec.** D1-A retained as **research evidence**; **non-leading**; **no D1-A-prime, D1-B, V1/D1 hybrid, or F1/D1 hybrid authorized**.

No next strategy phase is authorized.

No paper/shadow planning is authorized.

No Phase 4 (risk/state/persistence runtime) work is authorized.

No live-readiness, deployment, exchange-write, or production-key work is authorized.

The next step is operator-driven only: the operator decides whether and when any subsequent phase is authorized. Until then, the project remains at the post-Phase-3j / Phase-3k consolidation boundary.

---

## Recently Completed Pre-Handoff Documents

The following formerly pending documents have now been created:

```text
docs/09-operations/first-run-setup-checklist.md
docs/00-meta/ai-coding-handoff.md
```

These files complete the practical setup and AI implementation handoff layer.

## First-Run Setup Checklist Status

`docs/09-operations/first-run-setup-checklist.md` now defines the guided setup path for:

- current local environment assumptions,
- repository setup at `C:\Prometheus`,
- GitHub Desktop tracking,
- AntiGravity IDE usage,
- Claude Code extension usage,
- ChatGPT-guided setup support,
- local development setup,
- Python/tooling setup,
- configuration skeletons,
- historical data and research storage,
- runtime database/log/state preparation,
- dry-run runtime setup,
- dashboard and monitor setup,
- Telegram/n8n alert-route setup,
- dedicated NUC preparation,
- host hardening checks,
- backup/restore verification,
- paper/shadow readiness,
- production Binance key timing,
- tiny-live readiness,
- emergency access and recovery readiness.

It explicitly preserves the rule:

```text
Do not create production Binance trade-capable API keys until the correct approved phase gate.
```

## AI Coding Handoff Status

`docs/00-meta/ai-coding-handoff.md` now defines the implementation contract for Claude Code.

It includes:

- repository reading order,
- authority hierarchy,
- locked v1 decisions,
- non-negotiable safety constraints,
- forbidden actions,
- phased implementation plan,
- runnable checkpoints,
- acceptance criteria per phase,
- dual-AI workflow with ChatGPT,
- Claude Code installation authority,
- installation escalation protocol,
- checkpoint reporting protocol,
- ambiguity/spec-gap protocol,
- local development first / NUC later plan,
- migration-to-NUC expectations,
- and copy-paste prompts for Claude Code.

The handoff explicitly requires:

```text
phased implementation
not one-shot generation
runnable checkpoint after every phase
no production exchange-write capability before approved gates
no production Binance keys during early coding
dry-run and paper/shadow before tiny live
operator approval before promotion
```

---

## Locked V1 Decisions

## Market and venue

- Venue: Binance USDⓈ-M futures.
- Initial live symbol: BTCUSDT perpetual.
- First secondary research/comparison symbol: ETHUSDT perpetual.
- V1 live scope: BTCUSDT only.
- ETHUSDT remains research/comparison only until separately approved.

## Strategy

- Strategy family: breakout continuation with higher-timeframe trend filter.
- Signal timeframe: 15m.
- Higher-timeframe bias: 1h.
- Entry style: completed-bar confirmation, then market entry.
- Baseline backtest fill assumption: next-bar open after confirmed signal close.
- Initial stop: structural stop plus ATR buffer.
- Trade management: staged risk reduction and strategy-managed trailing.
- Strategy uses completed bars only.

## Execution

- Runtime account mode: one-way mode.
- Margin mode: isolated margin.
- One symbol first.
- One position maximum.
- No pyramiding in v1.
- No reversal entry while positioned in v1.
- No hedge-mode behavior in v1.
- Entry order: normal MARKET order.
- Protective stop: exchange-side algo/conditional STOP_MARKET.
- Protective stop settings:
  - `closePosition=true`
  - `workingType=MARK_PRICE`
  - `priceProtect=TRUE`
- Stop updates: cancel-and-replace.
- User stream: primary live private-state source.
- REST: placement, cancellation, reconciliation, and recovery.
- Exchange state is authoritative.
- No blind retry for exposure-changing actions.

## Risk

- Initial live risk per trade: 0.25% of sizing equity.
- Initial effective leverage cap: 2x.
- Leverage is a tool to reach valid risk-based position size, not a target.
- Future risk path may work toward 1.00% only after staged validation and review.
- Future leverage caps such as 5x or 10x may be researched later, but are not initial live defaults.
- Internal notional cap is mandatory for live operation.
- Missing risk state, metadata, or exchange-state confidence fails closed.

## Deployment

- Deployment is supervised and staged.
- V1 is not lights-out autonomous.
- Standard rollout path:
  - research,
  - validation,
  - dry-run,
  - paper/shadow,
  - tiny live,
  - scaled live.
- Restart always begins in safe mode.
- Reconciliation is required before normal resumption.
- Incidents are severity-classified.
- Kill switch is persistent and never auto-clears.
- Tiny-live default host: dedicated local NUC / mini PC used only for Prometheus.
- The NUC has an attached desk monitor showing the operator dashboard during operation.
- Dashboard should be always available when the monitor is on.
- Telegram and/or n8n may be used for alert routing, but not as high-risk approval surfaces in v1.
- Production Binance trade-capable keys must not be created until the correct approved phase gate.

---

## Locked Architecture Direction

## Core architecture

- Modular monolith for v1.
- Strict strategy/risk/execution separation.
- Research and live runtime remain separate concerns.
- Exchange state outranks local state.
- Local persistence exists for restart safety and operational continuity.
- Observability is state-centric, not vanity-metric-centric.
- Operator dashboard is a supervision and control surface, not a discretionary trading terminal.
- Manual controls are for safety, recovery, governance, and audit.

## Core runtime principles

- Commands are not facts.
- REST acknowledgements are not final truth.
- User-stream and reconciliation paths confirm state.
- A filled entry is not yet a protected trade.
- A submitted stop is not yet confirmed protection.
- A position without confirmed protection is an emergency state.
- Unknown execution outcomes fail closed.
- Manual/non-bot exposure blocks new bot entries.
- Rollback does not clear safety state.
- Backup restore does not prove exchange truth.
- Approval cannot make unknown state known.

---

## Dashboard / NUC / Alerting Direction

The live operator environment is explicitly centered on:

```text
dedicated local NUC / mini PC
+ attached desk monitor
+ always-on Prometheus dashboard
```

The dashboard should be:

- polished,
- information-rich,
- Binance-like in density where useful,
- focused on Prometheus-specific safety and execution state,
- always visible during operation where practical.

Dashboard should show:

- runtime mode,
- entries allowed/blocked,
- open positions,
- open normal orders,
- open algo/protective orders,
- protective stop state,
- unknown execution outcomes,
- stream health,
- reconciliation state,
- incidents,
- alerts,
- daily loss,
- drawdown,
- risk state,
- host/NUC health,
- release/config state,
- Telegram/n8n route state.

A future TradingView-like candle/setup/trade visualization is allowed and desirable for rule verification.

It should remain read-only and must not become chart trading.

Forbidden in v1:

- arbitrary manual buy/sell,
- click-to-trade,
- manual pyramiding,
- manual reversal,
- manual stop widening,
- casual risk/leverage sliders,
- bypassing reconciliation,
- bypassing kill switch,
- bypassing incidents or approvals.

---

## Completed / Substantially Defined Documentation

The following documentation areas are substantially defined.

## 1. Meta, Setup, and Handoff

```text
docs/00-meta/current-project-state.md
docs/00-meta/ai-coding-handoff.md
docs/09-operations/first-run-setup-checklist.md
docs/12-roadmap/phase-gates.md
docs/12-roadmap/technical-debt-register.md
```

Defined:

- current high-level project memory checkpoint,
- Claude Code implementation handoff,
- repository reading order,
- phased implementation method,
- dual-AI workflow,
- installation escalation protocol,
- first-run setup path,
- phase gates,
- technical-debt tracking,
- implementation ambiguity/spec-gap log requirement.

## 2. Strategy and Research

```text
docs/03-strategy-research/first-strategy-comparison.md
docs/03-strategy-research/v1-breakout-strategy-spec.md
docs/03-strategy-research/v1-breakout-backtest-plan.md
```

Defined:

- v1 strategy family selection,
- BTCUSDT primary symbol,
- ETHUSDT comparison symbol,
- 15m/1h timeframe structure,
- breakout setup and trigger logic,
- completed-bar-only strategy logic,
- initial structural stop logic,
- staged stop management,
- backtest assumptions,
- anti-overfitting principles,
- validation methodology.

## 3. Data Layer

```text
docs/04-data/historical-data-spec.md
docs/04-data/timestamp-policy.md
docs/04-data/dataset-versioning.md
docs/04-data/live-data-spec.md
docs/04-data/data-requirements.md
```

Defined:

- official Binance USDⓈ-M futures data as canonical v1 historical source,
- Parquet + DuckDB research data stack,
- UTC Unix milliseconds as canonical timestamps,
- completed-bar-only strategy policy,
- dataset versioning and manifests,
- live market-data stream behavior,
- partial-candle restrictions,
- live 15m/1h alignment,
- mark-price context,
- stale market-data gating,
- research storage vs runtime DB separation,
- data setup/runbook requirements connected through the first-run setup checklist.

## 4. Backtesting and Validation

```text
docs/05-backtesting-validation/v1-breakout-validation-checklist.md
```

Defined:

- promotion gates,
- data integrity checks,
- strategy conformity checks,
- simulation realism checks,
- robustness checks,
- exit model comparison,
- risk profile review,
- execution readiness review,
- paper/shadow and tiny-live candidate requirements.

## 5. Execution and Exchange

```text
docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md
docs/06-execution-exchange/exchange-adapter-design.md
docs/06-execution-exchange/binance-usdm-order-model.md
docs/06-execution-exchange/user-stream-reconciliation.md
docs/06-execution-exchange/failure-recovery.md
docs/06-execution-exchange/position-state-model.md
```

Defined:

- market entry after completed 15m signal close,
- normal MARKET entry order model,
- algo/conditional STOP_MARKET protective stop model,
- deterministic client IDs,
- normal order IDs versus algo order IDs,
- ACK preferred for initial market entry response,
- REST acknowledgement not final truth,
- user stream as live private-state source,
- `ORDER_TRADE_UPDATE` / `ACCOUNT_UPDATE` / `ALGO_UPDATE` responsibilities,
- stream staleness and reconciliation behavior,
- clean flat state,
- clean protected-position state,
- unknown execution outcome handling,
- orphaned/multiple stop handling,
- manual/non-bot exposure handling,
- exchange adapter boundaries,
- no blind retry for exposure-changing actions,
- position state normalization,
- one-way `BOTH` semantics,
- `positionAmt` sign interpretation.

## 6. Risk

```text
docs/07-risk/position-sizing-framework.md
docs/07-risk/exposure-limits.md
docs/07-risk/stop-loss-policy.md
docs/07-risk/kill-switches.md
docs/07-risk/daily-loss-rules.md
docs/07-risk/drawdown-controls.md
```

Defined:

- sizing from stop distance and equity risk,
- sizing equity uses strategy allocation boundary,
- initial live risk 0.25%,
- future path toward 1% risk only after staged review,
- initial risk-usage buffer 90%,
- quantity rounded down,
- below-minimum quantity rejects,
- leverage cap and notional cap enforcement,
- BTCUSDT-only live scope,
- one position maximum,
- no pyramiding,
- no reversal while positioned,
- manual exposure blocks entries,
- no stop/no trade,
- stop widening forbidden,
- unprotected live position emergency,
- kill switch behavior,
- daily loss lockouts,
- drawdown controls.

## 7. Runtime Architecture

```text
docs/08-architecture/implementation-blueprint.md
docs/08-architecture/codebase-structure.md
docs/08-architecture/state-model.md
docs/08-architecture/internal-event-contracts.md
docs/08-architecture/runtime-persistence-spec.md
docs/08-architecture/observability-design.md
docs/08-architecture/event-flows.md
docs/08-architecture/database-design.md
docs/08-architecture/deployment-model.md
```

Defined:

- modular monolith architecture,
- component ownership boundaries,
- strategy/risk/execution separation,
- runtime modes,
- trade lifecycle states,
- protection states,
- reconciliation states,
- control flags,
- commands/events/queries,
- message envelope,
- durable persistence requirements,
- runtime database design,
- state transition/event log transaction rules,
- event flows,
- deployment stages,
- NUC deployment model,
- alert/dashboard hooks,
- state-centric observability.

## 8. Operations

```text
docs/09-operations/first-run-setup-checklist.md
docs/09-operations/restart-procedure.md
docs/09-operations/incident-response.md
docs/09-operations/operator-workflow.md
docs/09-operations/daily-weekly-review-process.md
docs/09-operations/release-process.md
docs/09-operations/rollback-procedure.md
```

Defined:

- practical first-run setup path,
- safe-mode-first restart,
- reconciliation before resumption,
- clean/recoverable/unsafe mismatch classification,
- incident severity model,
- containment-first incident response,
- operator responsibilities,
- allowed manual actions,
- daily/weekly review cadence,
- release stages and promotion gates,
- rollback for code/config/risk/database/deployment/docs,
- rollback does not bypass reconciliation or clear safety flags.

## 9. Security

```text
docs/10-security/api-key-policy.md
docs/10-security/secrets-management.md
docs/10-security/permission-scoping.md
docs/10-security/audit-logging.md
docs/10-security/host-hardening.md
docs/10-security/disaster-recovery.md
```

Defined:

- least privilege,
- no withdrawal permission,
- production IP restriction,
- environment separation,
- secrets never in code/git/docs/screenshots/chats/logs,
- fail-closed credential behavior,
- key rotation/revocation principles,
- audit logging for safety/security actions,
- dedicated NUC host baseline,
- monitor/dashboard model,
- physical security,
- power/internet/outbound-IP readiness,
- disaster recovery,
- backup/restore,
- credential compromise handling.

## 10. Operator Interface

```text
docs/11-interface/operator-dashboard-requirements.md
docs/11-interface/manual-control-actions.md
docs/11-interface/approval-workflows.md
docs/11-interface/dashboard-metrics.md
docs/11-interface/alerting-ui.md
```

Defined:

- dashboard is supervision/control surface,
- dashboard is always-on on the dedicated NUC monitor where practical,
- top-level runtime status,
- connectivity/stream health,
- position/protection panel,
- open normal orders,
- open algo/protective orders,
- reconciliation/restart panel,
- incidents and alerts,
- recent important events,
- limited manual controls,
- forbidden discretionary manual trading controls,
- approval workflows,
- dashboard metrics catalog,
- Telegram/n8n alerting behavior,
- alert acknowledgement vs resolution,
- TradingView-like read-only chart/review concept.

## 11. Roadmap / Governance

```text
docs/12-roadmap/phase-gates.md
docs/12-roadmap/technical-debt-register.md
```

Defined:

- staged development and deployment gates,
- Claude Code readiness gate,
- first-run setup readiness gate,
- production key readiness gate,
- risk increase gate,
- leverage increase gate,
- notional cap increase gate,
- demotion/pause triggers,
- evidence artifacts,
- technical-debt categories,
- pre-Claude blockers,
- pre-tiny-live blockers,
- implementation ambiguity/spec-gap log requirement.

---

## Immediate Next Tasks

No new strategy phase, paper/shadow planning, Phase 4 runtime implementation, live-readiness, or deployment work is currently authorized.

The next step is operator-driven:

1. Operator reviews Phase 3j final outputs:
   - `docs/00-meta/implementation-reports/2026-04-29_phase-3j_D1A_execution-diagnostics.md`
   - `docs/00-meta/implementation-reports/2026-04-29_phase-3j_closeout-report.md`
   - `docs/00-meta/implementation-reports/2026-04-29_phase-3j_merge-report.md`
2. Operator reviews Phase 3k consolidation memo and decision menu:
   - `docs/00-meta/implementation-reports/2026-04-29_phase-3k_post-D1A-research-consolidation.md`
   - `docs/00-meta/implementation-reports/2026-04-29_phase-3k_closeout-report.md`
3. Operator decides whether and when to authorize any subsequent phase. Phase 3k primary recommendation is **remain paused**; acceptable secondary / tertiary alternatives are **external execution-cost evidence review (docs-only)** or **regime-first research framework memo (docs-only)**, each conditional on explicit ex-ante operator commitment to symmetric-outcome / anti-circular-reasoning discipline. Implementation, backtesting, paper/shadow, Phase 4, live-readiness, deployment, D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, and ML-feasibility authorizations are **NOT** recommended by Phase 3k.
4. Until that authorization, the project remains at the post-Phase-3j / Phase-3k consolidation boundary.

Implementation/code work that proceeds without explicit operator authorization for a specific phase is forbidden.

---

## Claude Code Start Instruction

Phase 0 (repo audit), Phase 1 (local development foundation), the Phase 2 strategy/backtesting research arc (through Phase 2w), the Phase 3 F1 mean-reversion research arc (Phase 3a through Phase 3d-B2 + Phase 3e consolidation), and the Phase 3 D1-A funding-aware research arc (Phase 3f through Phase 3j) are complete and merged to `main`. Phase 3k is the docs-only post-D1-A research consolidation memo with operator decision menu.

Claude Code must not begin any subsequent strategy phase, paper/shadow planning, Phase 4 runtime implementation, live-readiness, or deployment work without explicit operator authorization for that specific phase. Phase 3k's recommended next operator decision is **remain paused** with **external execution-cost evidence review (docs-only)** or **regime-first research framework memo (docs-only)** as acceptable secondary / tertiary alternatives. Any subsequent phase requires explicit operator authorization beyond Phase 3k. **No D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, or ML-training authorization flows from Phase 3k.**

The AI coding handoff at `docs/00-meta/ai-coding-handoff.md` remains the authoritative reference for phased implementation method, safety constraints, and reporting protocol. Phase-gate governance at `docs/12-roadmap/phase-gates.md` and the technical-debt register at `docs/12-roadmap/technical-debt-register.md` continue to bound any future phase.

---

## Current 25-File Project Upload Recommendation

For a future ChatGPT project-file continuity cache, use these 25 files.

The repo remains authoritative and should still be inspected directly.

```text
docs/00-meta/current-project-state.md
docs/00-meta/ai-coding-handoff.md
docs/09-operations/first-run-setup-checklist.md
docs/12-roadmap/phase-gates.md
docs/12-roadmap/technical-debt-register.md
docs/03-strategy-research/v1-breakout-strategy-spec.md
docs/05-backtesting-validation/v1-breakout-validation-checklist.md
docs/04-data/data-requirements.md
docs/04-data/live-data-spec.md
docs/04-data/timestamp-policy.md
docs/06-execution-exchange/exchange-adapter-design.md
docs/06-execution-exchange/binance-usdm-order-model.md
docs/06-execution-exchange/user-stream-reconciliation.md
docs/06-execution-exchange/failure-recovery.md
docs/06-execution-exchange/position-state-model.md
docs/07-risk/position-sizing-framework.md
docs/07-risk/exposure-limits.md
docs/07-risk/stop-loss-policy.md
docs/07-risk/kill-switches.md
docs/08-architecture/implementation-blueprint.md
docs/08-architecture/state-model.md
docs/08-architecture/internal-event-contracts.md
docs/08-architecture/runtime-persistence-spec.md
docs/08-architecture/database-design.md
docs/08-architecture/deployment-model.md
```

If a future chat focuses heavily on setup/dashboard/alerts rather than coding handoff, temporarily swap in:

```text
docs/08-architecture/event-flows.md
docs/10-security/host-hardening.md
docs/10-security/disaster-recovery.md
docs/11-interface/dashboard-metrics.md
docs/11-interface/alerting-ui.md
docs/11-interface/manual-control-actions.md
docs/11-interface/approval-workflows.md
```

by removing less immediately needed strategy/data/risk documents, because the repository remains the full source of truth.

---

## Implementation Readiness Status

Current readiness:

```text
Strategy/research (V1 breakout):  Phase 2 research arc complete
                                  H0 anchor; R3 baseline-of-record;
                                  R1a, R1b-narrow, R2 retained as research evidence
Strategy/research (F1 mean-rev):  Phase 3 research arc complete
                                  F1 HARD REJECT (Phase 3d-B2 first execution);
                                  retained as research evidence; non-leading;
                                  Phase 3d-B2 terminal for F1
Strategy/research (D1-A funding): Phase 3 research arc complete
                                  D1-A MECHANISM PASS / FRAMEWORK FAIL - other
                                  (Phase 3j first execution);
                                  retained as research evidence; non-leading;
                                  Phase 3j terminal for D1-A under current locked spec
Historical/live data design:      docs strong; Phase 2e v002 datasets locked
Validation plan:                  implemented through Phase 3j
Risk model:                       docs strong; runtime not yet implemented
Execution model:                  docs strong; runtime not yet implemented
Runtime architecture:             docs strong; runtime not yet implemented
Operations:                       docs strong; runtime not yet implemented
Security:                         docs strong; runtime not yet implemented
Interface/dashboard/alerts:       docs strong; not yet implemented
Roadmap/governance:               strong
AI coding handoff:                created
First-run setup checklist:        created
Claude Code Phase 0 readiness:    completed
Phase 1 local-dev foundation:     completed
Phase 2 data foundation:          completed
Phase 2 strategy research arc:    completed (Phase 2w merged)
Phase 3 F1 research arc:          completed (Phase 3d-B2 merged + Phase 3e consolidation)
Phase 3 D1-A research arc:        completed (Phase 3j merged at 5c8537b;
                                  merge-report 5d18408 / 5d18408+a7f6531)
Phase 3k consolidation memo:      drafted (docs-only; remain-paused primary
                                  recommendation; external-cost-evidence or
                                  regime-first memo as acceptable secondary /
                                  tertiary alternatives)
Phase 4 runtime implementation:   NOT authorized
Paper/shadow planning:            NOT authorized
Live-readiness / deployment:      NOT authorized
Production-key work:              NOT authorized
Exchange-write capability:        NOT authorized
F1-prime / target-subset spec:    NOT authorized; not proposed
D1-A-prime / D1-B / hybrid spec:  NOT authorized; not proposed
ML feasibility memo:              NOT authorized; not proposed
New family research:              NOT authorized; not proposed
```

The project has completed three strategy/backtesting research arcs (V1 breakout through Phase 2w; F1 mean-reversion through Phase 3d-B2; D1-A funding-aware through Phase 3j). Phase 3k is the docs-only post-D1-A consolidation memo with operator decision menu; recommended next operator decision is **remain paused** with external-cost-evidence review or regime-first framework memo as acceptable secondary / tertiary alternatives.

It is not ready for Phase 4 runtime implementation, paper/shadow operation, exchange-write capability, production Binance keys, or live trading. No subsequent phase has been authorized; the next step requires explicit operator authorization for that specific phase.

---

## Document Status

- Status: ACTIVE
- Updated: 2026-04-29
- Owner: Project operator
- Role: High-level project memory checkpoint after Phase 3j + Phase 3k consolidation
